"""Contratos de entrada e saída da API (Pydantic v2).

O ExplanationPayload é o formato dos seis passos. Ele é usado tanto para
explicações curadas (escritas à mão) quanto para as geradas por IA, e é o
primeiro filtro contra respostas malformadas do modelo.
"""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MappingRow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    universo: str = Field(min_length=1, description="Elemento do universo do aluno")
    tecnico: str = Field(min_length=1, description="Elemento técnico correspondente")
    trecho_base: str = Field(min_length=5, description="Citação literal do texto-base")


class TransferQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    pergunta: str = Field(min_length=10)
    resposta_esperada: str = Field(min_length=5)


class ExplanationPayload(BaseModel):
    """Os seis passos (modelo Teaching-With-Analogies adaptado)."""

    model_config = ConfigDict(extra="forbid")
    conceito: str = Field(min_length=20)
    cena: str = Field(min_length=20, max_length=700)
    mapeamento: list[MappingRow] = Field(min_length=3, max_length=6)
    onde_falha: list[str] = Field(min_length=1)
    reformulacao_tecnica: str = Field(min_length=20)
    pergunta_transferencia: TransferQuestion


class Refusal(BaseModel):
    """O modelo pode recusar quando não há analogia fiel. Melhor que inventar."""

    model_config = ConfigDict(extra="forbid")
    status: Literal["sem_analogia_fiel"]
    motivo: str = Field(min_length=5)


# ---------- API ----------

class SessionOut(BaseModel):
    token: str
    user_id: str


class ConsentIn(BaseModel):
    version: str = Field(min_length=1, max_length=20)
    accepted: bool


class InterestIn(BaseModel):
    label: str = Field(min_length=2, max_length=60)
    depth: int = Field(ge=1, le=3, description="1 conhece pouco, 3 fã profundo")


class InterestOut(InterestIn):
    id: int


class ReadingPrefs(BaseModel):
    font_scale: float = Field(default=1.0, ge=1.0, le=3.0)
    theme: Literal["claro", "escuro", "alto-contraste", "sistema"] = "sistema"
    reduced_motion: bool = False


class ConceptOut(BaseModel):
    slug: str
    title: str
    discipline: str


class NeutralOut(BaseModel):
    slug: str
    title: str
    base_text: str


class ExplanationRequest(BaseModel):
    concept_slug: str
    interest_id: int
    level: Literal["iniciante", "intermediario"] = "iniciante"


class ExplanationOut(BaseModel):
    id: int | None
    concept_slug: str
    interest_label: str | None
    provider: str
    status: Literal["approved", "draft", "neutral"]
    personalized: bool
    payload: ExplanationPayload | None
    neutral_text: str | None = None
    notice: str | None = None
    created_at: datetime | None = None


class FeedbackIn(BaseModel):
    kind: Literal["util", "errada", "confusa"]
    comment: str | None = Field(default=None, max_length=500)
