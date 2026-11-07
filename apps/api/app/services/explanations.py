"""Regra de negócio: escolher, gerar, verificar e servir explicações.

Fluxo de POST /v1/explanations:
1. explicação já aprovada no banco (curada) ou já verificada, para
   conceito+interesse+nível — é o cache, e evita gastar IA de novo;
2. se não houver e o provedor for "llm": gera, **autoverifica** (D6, ADR 0003),
   passa pelos validadores determinísticos e, se algo reprovar, tenta de novo
   uma única vez com os motivos;
3. recusa do modelo, falha ou segunda reprovação devolvem a explicação neutra
   (o texto-base revisado) com um aviso que diz o motivo.

O aluno nunca fica sem resposta e **nunca** recebe conteúdo reprovado.

Estados de uma explicação no banco:

| status         | significa                                    | é servida?     |
|----------------|----------------------------------------------|----------------|
| `approved`     | curada, escrita e revisada por pessoa        | sim            |
| `verified`     | gerada por IA, aprovada na autoverificação   | sim, com aviso |
| `under_review` | alguém marcou "está errada" (RF05)           | não            |
| `rejected`     | reprovada na revisão manual                  | não            |
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
from app.services.verification import NullVerifier, SelfVerifier, draft_text
from app.validators.grounding import validate_explanation

log = logging.getLogger(__name__)

NOTICE_NO_PERSONALIZED = (
    "Ainda não há explicação personalizada revisada para esse interesse. "
    "Mostrando a explicação padrão."
)
NOTICE_NOT_VERIFIED = (
    "Não conseguimos confirmar a explicação adaptada ao seu interesse. "
    "Para não mostrar algo errado, aqui está a explicação padrão."
)
NOTICE_NO_FAITHFUL_ANALOGY = (
    "Não encontramos uma comparação fiel com esse interesse para este conteúdo. "
    "Mostrando a explicação padrão."
)
NOTICE_AI_VERIFIED = (
    "Explicação adaptada por IA ao seu interesse. Ela passou pela conferência "
    "automática, mas não foi revisada por um professor."
)

# Os dois estados que podem chegar ao aluno.
SERVED = ("approved", "verified")


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
    if notice is None and row.status == "verified":
        notice = NOTICE_AI_VERIFIED
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


def universe_terms_for(db: Session, concept_slug: str, interest_label: str) -> list[str]:
    """Termos da analogia que o aluno está lendo, para o porteiro do RF11.

    Sem isso, perguntar "e se o zagueiro errar o passe?" seria recusado como
    fora do conceito — e a cena do zagueiro foi o próprio app que ofereceu.
    """
    label = slugify(interest_label)
    row = db.scalar(
        select(Explanation)
        .where(
            Explanation.concept_slug == concept_slug,
            Explanation.interest_label == label,
            Explanation.status.in_(SERVED),
        )
        .order_by(Explanation.id.desc())
    )
    termos = [interest_label]
    if row:
        termos += [linha.get("universo", "") for linha in row.payload.get("mapeamento", [])]
    return [t for t in termos if t]


def generate_validated(
    generator: ExplanationGenerator,
    data: ExplanationRequestData,
    verifier: SelfVerifier | None = None,
) -> tuple[ExplanationPayload | Refusal | None, list[str]]:
    """Gera, autoverifica e valida; reprovou, tenta mais uma vez com os motivos.

    A ordem está no ADR 0003: primeiro a autoverificação, que julga o
    conteúdo, depois os validadores determinísticos, que conferem forma e
    ancoragem no texto-base. Duas tentativas no total — a terceira raramente
    acerta e o aluno está esperando.
    """
    verifier = verifier or NullVerifier()
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

        verdict = verifier.verify(draft_text(result), data.concept)
        if not verdict.aprovada:
            errors.extend(verdict.motivos)
            data.feedback = verdict.as_feedback()
            continue

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
    verifier: SelfVerifier | None = None,
) -> ExplanationOut:
    settings = settings or get_settings()
    label = slugify(interest_label)

    # Cache: curada ou já verificada antes. Vale para qualquer aluno, porque
    # a explicação não guarda nada de quem pediu.
    cached = db.scalar(
        select(Explanation)
        .where(
            Explanation.concept_slug == concept.slug,
            Explanation.interest_label == label,
            Explanation.level == level,
            Explanation.status.in_(SERVED),
        )
        .order_by(Explanation.id.desc())
    )
    if cached:
        return to_out(cached)

    if generator is None:
        return neutral(concept, interest_label, NOTICE_NO_PERSONALIZED)

    data = ExplanationRequestData(concept, interest_label, depth, level)
    result, errors = generate_validated(generator, data, verifier)
    if isinstance(result, Refusal):
        log.info("recusa do modelo para %s/%s: %s", concept.slug, label, result.motivo)
        return neutral(concept, interest_label, NOTICE_NO_FAITHFUL_ANALOGY)
    if result is None:
        log.warning("reprovada duas vezes %s/%s: %s", concept.slug, label, errors)
        return neutral(concept, interest_label, NOTICE_NOT_VERIFIED)

    verified = Explanation(
        concept_slug=concept.slug,
        interest_label=label,
        level=level,
        provider=generator.name,
        prompt_version=settings.prompt_version,
        status="verified",
        payload=result.model_dump(),
    )
    db.add(verified)
    db.commit()
    return to_out(verified)
