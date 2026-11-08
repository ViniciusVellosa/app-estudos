"""Reconhece o assunto que o aluno digitou no chat (decisão D7).

O aluno escreve com as próprias palavras ("quero entender TCP", "janela
deslizante"). Aqui esse texto é casado com os conteúdos da biblioteca, que são
os únicos com material de referência para a autoverificação (D6, ADR 0003).

Por que não deixar a IA explicar qualquer assunto: sem um texto-base de
referência, a IA verificaria a si mesma sem nada externo para comparar, e
esse é justamente o caso em que a autocorreção falha (Huang et al., 2024).
Assunto fora da biblioteca recebe uma resposta honesta e sugestões.

É determinístico e não chama IA: rápido, de graça e testável. O texto
digitado não é gravado.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from app.content import Concept, load_concepts

# Palavras que aparecem em qualquer pedido e não dizem qual é o assunto.
VAZIAS = {
    "a", "o", "as", "os", "um", "uma", "de", "da", "do", "das", "dos", "e", "em",
    "no", "na", "nos", "nas", "por", "para", "pra", "com", "sem", "que", "como",
    "funciona", "funcionam", "quero", "queria", "entender", "aprender", "estudar",
    "explica", "explique", "explicar", "me", "sobre", "qual", "quais", "ser", "sao", "isso", "assunto", "conteudo", "materia", "coisa", "tipo",
}


def normaliza(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto.lower())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", texto).strip()


def _palavras(texto: str) -> set[str]:
    return {p for p in normaliza(texto).split() if len(p) >= 3 and p not in VAZIAS}


def _contem_expressao(texto_norm: str, expressao: str) -> bool:
    exp = normaliza(expressao)
    return bool(exp) and re.search(rf"(^| ){re.escape(exp)}( |$)", texto_norm) is not None


@dataclass
class Resultado:
    conceito: Concept | None
    sugestoes: list[Concept]


def pontua(texto: str, conceito: Concept) -> int:
    """Expressão inteira conhecida vale mais que palavra solta do título."""
    texto_norm = normaliza(texto)
    pontos = 0
    for exp in [*conceito.aliases, *conceito.key_terms, conceito.title]:
        if _contem_expressao(texto_norm, exp):
            pontos = max(pontos, 2 + len(normaliza(exp).split()))
    comuns = _palavras(texto) & (_palavras(conceito.title) | _palavras(conceito.slug.replace("-", " ")))
    return max(pontos, len(comuns))


def reconhece(texto: str) -> Resultado:
    conceitos = list(load_concepts().values())
    if not normaliza(texto):
        return Resultado(None, conceitos)
    pontuados = sorted(((pontua(texto, c), c) for c in conceitos), key=lambda x: -x[0])
    melhor_pontos, melhor = pontuados[0] if pontuados else (0, None)
    if melhor is None or melhor_pontos == 0:
        return Resultado(None, conceitos)
    return Resultado(melhor, [c for p, c in pontuados if c is not melhor and p > 0])
