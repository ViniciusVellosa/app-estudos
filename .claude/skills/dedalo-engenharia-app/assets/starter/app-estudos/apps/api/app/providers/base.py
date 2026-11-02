"""Contrato dos geradores de explicação (padrão Strategy / ports & adapters).

O serviço de explicações só conhece esta interface. Trocar o provedor de IA,
usar um modelo local ou desligar a IA não muda nada fora desta pasta.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.content import Concept
from app.schemas import ExplanationPayload, Refusal


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
