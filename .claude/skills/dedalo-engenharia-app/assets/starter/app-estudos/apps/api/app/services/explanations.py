"""Regra de negócio: escolher, gerar, validar e servir explicações.

Fluxo de POST /v1/explanations:
1. explicação aprovada no banco (curada ou revisada) para conceito+interesse+nível;
2. se não houver e o provedor for "llm": gera, valida, tenta de novo uma vez;
3. se a IA falhar, recusar ou a explicação ainda não estiver revisada,
   devolve a explicação neutra (texto-base) com um aviso claro.
O aluno nunca fica sem resposta e nunca recebe conteúdo reprovado.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.content import Concept, load_concepts, load_curated, slugify
from app.db import Explanation
from app.providers.base import ExplanationGenerator, ExplanationRequestData, GenerationError
from app.schemas import ExplanationOut, ExplanationPayload, Refusal
from app.validators.grounding import validate_explanation

log = logging.getLogger(__name__)

NOTICE_NO_PERSONALIZED = (
    "Ainda não há explicação personalizada revisada para esse interesse. "
    "Mostrando a explicação padrão."
)
NOTICE_IN_REVIEW = (
    "Geramos uma explicação com o seu interesse, mas ela ainda está em revisão. "
    "Por enquanto, veja a explicação padrão."
)
NOTICE_NO_FAITHFUL_ANALOGY = (
    "Não encontramos uma comparação fiel com esse interesse para este conteúdo. "
    "Mostrando a explicação padrão."
)
NOTICE_AI_DRAFT = "Explicação adaptada por IA ao seu interesse e ainda não revisada por um professor."


def seed_curated(db: Session) -> int:
    """Copia as explicações curadas (arquivos) para o banco como aprovadas."""
    count = 0
    for concept in load_concepts().values():
        folder = Path(get_settings().content_dir) / "explanations" / concept.slug
        for path in sorted(folder.glob("*.json")):
            meta = json.loads(path.read_text(encoding="utf-8")).get("_meta", {})
            label = meta.get("interest_label", path.stem)
            level = meta.get("level", "iniciante")
            exists = db.scalar(
                select(Explanation).where(
                    Explanation.concept_slug == concept.slug,
                    Explanation.interest_label == slugify(label),
                    Explanation.level == level,
                    Explanation.provider == "curated",
                )
            )
            payload = load_curated(concept.slug, label)
            report = validate_explanation(payload, concept.rules)
            if not report.ok:
                # conteúdo curado também passa pelos validadores
                log.warning("curada reprovada %s: %s", path, report.errors)
                continue
            if exists:
                # arquivo editado depois da primeira carga: atualiza o conteúdo,
                # mas não devolve à circulação algo marcado como errado
                if exists.payload != payload.model_dump():
                    exists.payload = payload.model_dump()
                    count += 1
                continue
            db.add(
                Explanation(
                    concept_slug=concept.slug,
                    interest_label=slugify(label),
                    level=level,
                    provider="curated",
                    prompt_version="-",
                    status=meta.get("status", "approved"),
                    payload=payload.model_dump(),
                )
            )
            count += 1
    db.commit()
    return count


def neutral(concept: Concept, interest_label: str | None, notice: str) -> ExplanationOut:
    return ExplanationOut(
        id=None,
        concept_slug=concept.slug,
        interest_label=interest_label,
        provider="neutral",
        status="neutral",
        personalized=False,
        payload=None,
        neutral_text=concept.base_text,
        notice=notice,
    )


def to_out(row: Explanation, notice: str | None = None) -> ExplanationOut:
    return ExplanationOut(
        id=row.id,
        concept_slug=row.concept_slug,
        interest_label=row.interest_label,
        provider=row.provider,
        status=row.status,
        personalized=True,
        payload=ExplanationPayload.model_validate(row.payload),
        notice=notice,
        created_at=row.created_at,
    )


def generate_validated(
    generator: ExplanationGenerator, data: ExplanationRequestData
) -> tuple[ExplanationPayload | Refusal | None, list[str]]:
    """Gera e valida; em caso de reprovação, uma nova tentativa com as correções."""
    errors: list[str] = []
    for _attempt in range(2):
        try:
            result = generator.generate(data)
        except GenerationError as exc:
            errors.append(str(exc))
            data.feedback = f"A resposta anterior falhou: {exc}. Siga o formato pedido."
            continue
        if isinstance(result, Refusal):
            return result, errors
        report = validate_explanation(result, data.concept.rules)
        if report.ok:
            return result, errors
        errors.extend(report.errors)
        data.feedback = report.as_feedback()
    return None, errors


def get_explanation(
    db: Session,
    concept: Concept,
    interest_label: str,
    depth: int,
    level: str,
    generator: ExplanationGenerator | None,
    settings: Settings | None = None,
) -> ExplanationOut:
    settings = settings or get_settings()
    label = slugify(interest_label)

    approved = db.scalar(
        select(Explanation)
        .where(
            Explanation.concept_slug == concept.slug,
            Explanation.interest_label == label,
            Explanation.level == level,
            Explanation.status == "approved",
        )
        .order_by(Explanation.id.desc())
    )
    if approved:
        return to_out(approved)

    if generator is None:
        return neutral(concept, interest_label, NOTICE_NO_PERSONALIZED)

    draft = db.scalar(
        select(Explanation).where(
            Explanation.concept_slug == concept.slug,
            Explanation.interest_label == label,
            Explanation.level == level,
            Explanation.status == "draft",
        )
    )
    if draft is None:
        data = ExplanationRequestData(concept, interest_label, depth, level)
        result, errors = generate_validated(generator, data)
        if isinstance(result, Refusal):
            log.info("recusa do modelo para %s/%s: %s", concept.slug, label, result.motivo)
            return neutral(concept, interest_label, NOTICE_NO_FAITHFUL_ANALOGY)
        if result is None:
            log.warning("geração reprovada %s/%s: %s", concept.slug, label, errors)
            return neutral(concept, interest_label, NOTICE_NO_PERSONALIZED)
        draft = Explanation(
            concept_slug=concept.slug,
            interest_label=label,
            level=level,
            provider=generator.name,
            prompt_version=settings.prompt_version,
            status="draft",
            payload=result.model_dump(),
        )
        db.add(draft)
        db.commit()

    if settings.serve_only_approved:
        return neutral(concept, interest_label, NOTICE_IN_REVIEW)
    return to_out(draft, NOTICE_AI_DRAFT)
