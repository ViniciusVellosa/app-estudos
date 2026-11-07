"""Contrato dos geradores de explicação (padrão Strategy / ports & adapters).

O serviço de explicações só conhece esta interface. Trocar o provedor de IA,
usar um modelo local ou desligar a IA não muda nada fora desta pasta.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TypeVar

from pydantic import BaseModel

from app.content import Concept
from app.schemas import ExplanationPayload, Refusal

M = TypeVar("M", bound=BaseModel)


@dataclass
class ExplanationRequestData:
    concept: Concept
    interest_label: str  # só o rótulo: nenhum dado que identifique o aluno
    depth: int
    level: str
    feedback: str | None = None  # erros da tentativa anterior, se houver


class GenerationError(Exception):
    """Falha de rede, tempo esgotado ou resposta fora do formato."""


class ExplanationGenerator(Protocol):
    name: str

    def generate(self, req: ExplanationRequestData) -> ExplanationPayload | Refusal: ...


class StructuredChat(Protocol):
    """Uma pergunta ao modelo com a resposta validada por um modelo Pydantic.

    É o contrato mínimo de que a autoverificação precisa (ADR 0003). Os
    geradores de IA já têm cliente, chave e tempo limite configurados, então
    implementam este protocolo e servem de chat para o verificador — sem
    segunda conexão nem segunda chave.
    """

    name: str

    def ask(self, system: str, user: str, output_model: type[M]) -> M: ...
