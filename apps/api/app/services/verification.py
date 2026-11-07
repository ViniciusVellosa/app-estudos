"""Autoverificação da resposta antes de exibi-la (decisão D6, ADR 0003).

Substitui a revisão humana do ADR 0002. O método é o Chain-of-Verification
(Dhuliawala et al., 2024), em três chamadas ao modelo:

1. **perguntas** — a partir do rascunho, o modelo lista as afirmações técnicas
   e escreve uma pergunta de verificação para cada uma;
2. **resposta** — cada pergunta é respondida numa chamada separada, **sem o
   rascunho no contexto** e com o texto-base como única referência. É o que
   impede o modelo de repetir o próprio erro: perguntado com o rascunho à
   vista, ele concorda consigo mesmo;
3. **veredito** — de posse das respostas, o modelo julga o rascunho.

Depois disso ainda correm os validadores determinísticos
(`app/validators/grounding.py`). Reprovado duas vezes, o aluno vê a explicação
padrão, nunca o rascunho.

Limite conhecido e assumido no ADR 0003: um modelo que verifica a si mesmo
reduz erros, mas não os elimina (Huang et al., 2024). Por isso a referência da
checagem é uma fonte fixa e revisada — o texto-base do conceito —, e não a
memória do modelo.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Protocol
from xml.sax.saxutils import escape

from pydantic import BaseModel, ConfigDict, Field

from app.content import Concept
from app.providers.base import GenerationError, StructuredChat
from app.schemas import ExplanationPayload

log = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "verificacao_sistema.md"

# Teto de perguntas de checagem: com 3, a verificação custa 5 chamadas ao
# modelo (1 + 3 + 1). Subir isso melhora pouco e multiplica custo e espera.
MAX_PERGUNTAS = 3

# O que o modelo responde quando o texto-base não cobre a pergunta.
NAO_CONSTA = "NAO_CONSTA"


@lru_cache
def system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


# ---------- saídas estruturadas de cada etapa ----------

class CheckQuestions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    perguntas: list[str] = Field(min_length=1, max_length=6)


class CheckAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resposta: str = Field(min_length=1)


class VerdictOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    aprovada: bool
    motivos: list[str] = Field(default_factory=list, max_length=3)


# ---------- resultado para quem chama ----------

@dataclass
class Verdict:
    aprovada: bool
    motivos: list[str] = field(default_factory=list)

    def as_feedback(self) -> str:
        """Texto curto devolvido ao gerador na nova tentativa."""
        return "A verificação reprovou a resposta anterior: " + "; ".join(self.motivos)


class SelfVerifier(Protocol):
    name: str

    def verify(self, rascunho: str, concept: Concept) -> Verdict: ...


class NullVerifier:
    """Aprova sempre. É o verificador do modo `curated`.

    Explicação curada é escrita e revisada por pessoa e já passa pelos
    validadores na carga (`seed_curated`): submetê-la a autoverificação
    gastaria chamadas de IA para conferir texto humano.
    """

    name = "sem-autoverificacao"

    def verify(self, rascunho: str, concept: Concept) -> Verdict:
        return Verdict(aprovada=True)


class LlmSelfVerifier:
    """Autoverificação em três etapas, com o texto-base como referência."""

    name = "autoverificacao"

    def __init__(self, chat: StructuredChat, max_perguntas: int = MAX_PERGUNTAS):
        self.chat = chat
        self.max_perguntas = max_perguntas

    def verify(self, rascunho: str, concept: Concept) -> Verdict:
        try:
            perguntas = self._perguntas(rascunho, concept)[: self.max_perguntas]
            # Cada resposta é uma chamada própria e NÃO recebe o rascunho.
            checagem = [(p, self._responder(p, concept)) for p in perguntas]
            return self._veredito(rascunho, concept, checagem)
        except GenerationError as exc:
            # Falhar fechado: sem verificação não há exibição (RNF04).
            log.warning("autoverificação indisponível para %s: %s", concept.slug, exc)
            return Verdict(False, [f"não foi possível verificar a resposta ({exc})"])

    # -- etapas --

    def _perguntas(self, rascunho: str, concept: Concept) -> list[str]:
        user = "\n".join([
            "<etapa>perguntas</etapa>",
            _tag("texto_base", concept.base_text),
            _tag("rascunho", rascunho),
        ])
        return self.chat.ask(system_prompt(), user, CheckQuestions).perguntas

    def _responder(self, pergunta: str, concept: Concept) -> str:
        user = "\n".join([
            "<etapa>resposta</etapa>",
            _tag("texto_base", concept.base_text),
            _tag("pergunta", pergunta),
        ])
        return self.chat.ask(system_prompt(), user, CheckAnswer).resposta

    def _veredito(
        self, rascunho: str, concept: Concept, checagem: list[tuple[str, str]]
    ) -> Verdict:
        pares = "\n".join(
            f"<par><pergunta>{escape(p)}</pergunta><resposta>{escape(r)}</resposta></par>"
            for p, r in checagem
        )
        user = "\n".join([
            "<etapa>veredito</etapa>",
            _tag("texto_base", concept.base_text),
            _tag("rascunho", rascunho),
            f"<checagem>\n{pares}\n</checagem>",
        ])
        out = self.chat.ask(system_prompt(), user, VerdictOut)
        if out.aprovada:
            return Verdict(True)
        # Reprovar sem dizer o porquê não ajuda a próxima tentativa.
        return Verdict(False, out.motivos or ["reprovada na autoverificação, sem motivo declarado"])


def _tag(nome: str, conteudo: str) -> str:
    """Delimita e escapa a entrada: nada aqui pode virar instrução (OWASP LLM01)."""
    return f"<{nome}>\n{escape(conteudo)}\n</{nome}>"


def draft_text(payload: ExplanationPayload) -> str:
    """Põe a explicação em texto corrido, que é o que o verificador analisa."""
    linhas = [
        f"CONCEITO: {payload.conceito}",
        f"CENA (analogia): {payload.cena}",
        "QUEM E QUEM:",
        *(f"  - {r.universo} = {r.tecnico}" for r in payload.mapeamento),
        "ONDE A ANALOGIA FALHA:",
        *(f"  - {x}" for x in payload.onde_falha),
        f"EM TERMOS TECNICOS: {payload.reformulacao_tecnica}",
        f"PERGUNTA: {payload.pergunta_transferencia.pergunta}",
        f"RESPOSTA ESPERADA: {payload.pergunta_transferencia.resposta_esperada}",
    ]
    return "\n".join(linhas)


def build_verifier(chat: StructuredChat | None) -> SelfVerifier:
    """Sem cliente de IA não há autoverificação: o modo curado dispensa."""
    return LlmSelfVerifier(chat) if chat is not None else NullVerifier()
