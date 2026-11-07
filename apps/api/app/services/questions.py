"""Perguntas livres do aluno, respondidas só dentro do conceito (RF11, D5).

Três saídas possíveis, e nenhuma outra:

| status             | quando                                               |
|--------------------|------------------------------------------------------|
| `respondida`       | é sobre o conceito e o texto-base responde            |
| `fora_do_conceito` | não é sobre o conceito: recusa educada com duas saídas|
| `sem_base`         | é sobre o conceito, mas o texto-base não cobre        |

O **porteiro de assunto é determinístico**, de propósito. Três razões:

1. roda com `EXPLANATION_PROVIDER=curated`, que é o modo das sessões de teste
   de usabilidade — a recusa precisa funcionar sem rede e sem chave;
2. é testável sem IA, então o comportamento é o mesmo em toda execução;
3. não gasta chamada de modelo para descobrir que a pergunta era "quem ganhou
   o jogo ontem?".

Limite assumido: a comparação é léxica, por raiz de palavra. Uma pergunta
sobre o conceito escrita inteiramente com outras palavras pode ser recusada
por engano. É o erro menos grave dos dois — recusar com as duas saídas
visíveis custa um clique; responder fora do conceito quebra a promessa do D5.

Com IA ligada, a resposta é redigida pelo modelo a partir do texto-base e
passa pela autoverificação (ADR 0003) antes de sair; reprovada, vira
`sem_base`. Sem IA, a resposta é extraída do próprio texto-base.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Literal
from xml.sax.saxutils import escape

from pydantic import BaseModel, ConfigDict, Field

from app.content import Concept
from app.providers.base import GenerationError, StructuredChat
from app.services.verification import SelfVerifier
from app.validators.grounding import normalize

log = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "resposta_sistema.md"

# Palavras sem valor para decidir assunto. Lista curta e explícita: um
# dicionário grande esconderia o critério de quem lê este arquivo.
STOPWORDS = {
    "aquilo", "como", "qual", "quais", "quando", "onde", "porque", "por", "que",
    "para", "com", "sem", "dos", "das", "num", "numa", "nos", "nas", "pelo",
    "pela", "isso", "isto", "esse", "essa", "este", "esta", "aquele", "aquela",
    "meu", "minha", "seu", "sua", "nosso", "nossa", "eles", "elas", "voce",
    "voces", "ele", "ela", "eu", "me", "te", "lhe", "ser", "sao", "estar",
    "estao", "ter", "tem", "tenho", "foi", "era", "sera", "pode",
    "posso", "podem", "deve", "fazer", "faz", "explica", "explicar", "diga",
    "dizer", "fala", "falar", "sobre", "mais", "menos", "muito", "pouco",
    "tudo", "nada", "entao", "tambem", "ainda", "sempre", "nunca", "agora",
    "antes", "depois", "aqui", "ali", "lado", "coisa", "jeito", "forma",
    "exemplo", "caso", "vez", "acontece", "acontecer", "funciona", "funcionar",
    "significa", "significar", "entendi", "entender", "nao", "sim",
}

MIN_TOKEN = 3        # abaixo disso a palavra não distingue assunto
MIN_RAIZ = 4         # casamento por raiz: "perde" casa com "perder"
MAX_FRASES = 2       # quantas frases do texto-base compõem a resposta extraída

RECUSA = (
    'Só consigo responder sobre "{titulo}". Essa pergunta é de outro assunto. '
    "Quer continuar neste conceito ou escolher outro?"
)
SEM_BASE = (
    "Isso é sobre {titulo}, mas não está no material que eu confiro antes de "
    "responder. Prefiro dizer que não sei a arriscar um palpite."
)


@dataclass
class Answer:
    status: Literal["respondida", "fora_do_conceito", "sem_base"]
    texto: str
    trechos: list[str] = field(default_factory=list)


class GroundedAnswer(BaseModel):
    """Saída estruturada da resposta gerada por IA."""

    model_config = ConfigDict(extra="forbid")
    consta: bool = Field(description="o texto-base responde à pergunta?")
    resposta: str = Field(default="", max_length=800)


@lru_cache
def system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


# ------------------------------------------------------------- vocabulário

def tokens(texto: str) -> list[str]:
    """Palavras com valor semântico, normalizadas (sem acento, minúsculas)."""
    return [t for t in normalize(texto).split() if len(t) >= MIN_TOKEN and t not in STOPWORDS]


def casa(token: str, vocabulario: set[str]) -> bool:
    """Casamento por raiz: evita falhar em plural e flexão verbal."""
    if token in vocabulario:
        return True
    raiz = token[:MIN_RAIZ]
    if len(token) < MIN_RAIZ:
        return False
    return any(v.startswith(raiz) for v in vocabulario if len(v) >= MIN_RAIZ)


@lru_cache
def _vocabulario(concept_slug: str, base_text: str, titulo: str, chaves: tuple[str, ...]) -> frozenset[str]:
    palavras = set(tokens(base_text)) | set(tokens(titulo))
    for termo in chaves:
        palavras.update(tokens(termo))
    return frozenset(palavras)


def vocabulario_do_conceito(concept: Concept) -> frozenset[str]:
    return _vocabulario(
        concept.slug, concept.base_text, concept.title, tuple(concept.key_terms)
    )


def no_conceito(pergunta: str, concept: Concept, universo: list[str] | None = None) -> bool:
    """A pergunta trata do conceito atual?

    `universo` traz os termos da analogia que o aluno está lendo. Sem isso,
    perguntar "e se o zagueiro errar o passe?" seria recusado — o que seria
    um erro grosseiro, já que a cena do zagueiro foi o app que ofereceu.
    """
    vocab = set(vocabulario_do_conceito(concept))
    for termo in universo or []:
        vocab.update(tokens(termo))
    return any(casa(t, vocab) for t in tokens(pergunta))


# ---------------------------------------------------- resposta sem IA

def frases(texto: str) -> list[str]:
    cruas = re.split(r"(?<=[.!?])\s+|\n{2,}", texto)
    return [f.strip() for f in cruas if len(f.strip()) > 20]


def extrair_do_texto_base(pergunta: str, concept: Concept) -> Answer:
    """Resposta extrativa: devolve as frases do texto-base que mais casam.

    Não é geração: é recorte do material revisado. Nunca inventa, e é o que
    permite demonstrar RF11 no teste de usabilidade sem IA (Mágico de Oz).
    """
    perguntados = tokens(pergunta)
    pontuadas = []
    for frase in frases(concept.base_text):
        vocab = set(tokens(frase))
        pontos = sum(1 for t in perguntados if casa(t, vocab))
        if pontos:
            pontuadas.append((pontos, frase))
    if not pontuadas:
        return Answer("sem_base", SEM_BASE.format(titulo=concept.title))
    pontuadas.sort(key=lambda par: -par[0])
    escolhidas = [f for _, f in pontuadas[:MAX_FRASES]]
    return Answer("respondida", " ".join(escolhidas), escolhidas)


# ---------------------------------------------------- resposta com IA

def gerar_com_ia(
    pergunta: str, concept: Concept, chat: StructuredChat, verifier: SelfVerifier
) -> Answer:
    user = "\n".join([
        f"<texto_base>\n{escape(concept.base_text)}\n</texto_base>",
        f"<conceito>{escape(concept.title)}</conceito>",
        f"<pergunta>{escape(pergunta)}</pergunta>",
    ])
    try:
        saida = chat.ask(system_prompt(), user, GroundedAnswer)
    except GenerationError as exc:
        log.warning("resposta indisponível para %s: %s", concept.slug, exc)
        return Answer("sem_base", SEM_BASE.format(titulo=concept.title))

    if not saida.consta or not saida.resposta.strip():
        return Answer("sem_base", SEM_BASE.format(titulo=concept.title))

    # D6 vale para a resposta do chat, não só para a explicação (RNF04).
    veredito = verifier.verify(f"PERGUNTA: {pergunta}\nRESPOSTA: {saida.resposta}", concept)
    if not veredito.aprovada:
        log.info("resposta reprovada na autoverificação (%s): %s", concept.slug, veredito.motivos)
        return Answer("sem_base", SEM_BASE.format(titulo=concept.title))

    return Answer("respondida", saida.resposta.strip())


# ------------------------------------------------------------- entrada

def answer_question(
    pergunta: str,
    concept: Concept,
    universo: list[str] | None = None,
    chat: StructuredChat | None = None,
    verifier: SelfVerifier | None = None,
) -> Answer:
    """Porteiro primeiro, resposta depois. Nunca o contrário."""
    if not no_conceito(pergunta, concept, universo):
        return Answer("fora_do_conceito", RECUSA.format(titulo=concept.title))
    if chat is not None and verifier is not None:
        return gerar_com_ia(pergunta, concept, chat, verifier)
    return extrair_do_texto_base(pergunta, concept)
