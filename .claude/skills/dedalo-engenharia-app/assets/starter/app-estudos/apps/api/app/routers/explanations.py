from fastapi import APIRouter, HTTPException, Request, Response, status
from sqlalchemy import select

from app.config import get_settings
from app.content import load_concepts
from app.db import Explanation, Feedback, Interest
from app.schemas import ConceptOut, ExplanationOut, ExplanationRequest, FeedbackIn, NeutralOut
from app.security import ConsentedUser, CurrentUser, DbDep
from app.services.explanations import get_explanation

router = APIRouter(prefix="/v1", tags=["conteúdo"])


@router.get("/concepts", response_model=list[ConceptOut])
def list_concepts():
    return [
        ConceptOut(slug=c.slug, title=c.title, discipline=c.discipline)
        for c in load_concepts().values()
    ]


@router.get("/concepts/{slug}/neutral", response_model=NeutralOut)
def neutral_explanation(slug: str):
    concept = load_concepts().get(slug)
    if concept is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conteúdo não encontrado.")
    return NeutralOut(slug=concept.slug, title=concept.title, base_text=concept.base_text)


@router.post("/explanations", response_model=ExplanationOut)
def request_explanation(
    body: ExplanationRequest,
    request: Request,
    user: ConsentedUser,
    db: DbDep,
):
    concept = load_concepts().get(body.concept_slug)
    if concept is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conteúdo não encontrado.")
    interest = db.scalar(
        select(Interest).where(Interest.id == body.interest_id, Interest.user_id == user.id)
    )
    if interest is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Interesse não encontrado.")
    generator = request.app.state.generator  # None quando o provedor é "curated"
    return get_explanation(
        db, concept, interest.label, interest.depth, body.level, generator, get_settings()
    )


@router.post("/explanations/{explanation_id}/feedback", status_code=204)
def send_feedback(
    explanation_id: int,
    body: FeedbackIn,
    user: CurrentUser,
    db: DbDep,
):
    explanation = db.get(Explanation, explanation_id)
    if explanation is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Explicação não encontrada.")
    db.add(Feedback(explanation_id=explanation.id, user_id=user.id, kind=body.kind, comment=body.comment))
    if body.kind == "errada":
        # sai de circulação até alguém revisar (python -m app.review)
        explanation.status = "under_review"
    db.commit()
    return Response(status_code=204)
