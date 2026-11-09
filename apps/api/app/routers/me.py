"""Sessão, consentimento, interesses, preferências e direitos do titular (LGPD)."""
import uuid

from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy import select

from app.config import get_settings
from app.db import Interest, User, utcnow
from app.schemas import (
    ConsentIn,
    InterestIn,
    InterestOut,
    ReadingPrefs,
    SessionOut,
)
from app.security import ConsentedUser, CurrentUser, DbDep, hash_token, new_token

router = APIRouter(prefix="/v1", tags=["aluno"])


@router.post("/session", response_model=SessionOut, status_code=201)
def create_session(db: DbDep):
    token = new_token()
    user = User(id=str(uuid.uuid4()), token_hash=hash_token(token))
    db.add(user)
    db.commit()
    return SessionOut(token=token, user_id=user.id)


@router.post("/consent", status_code=204)
def give_consent(body: ConsentIn, user: CurrentUser, db: DbDep):
    if body.version != get_settings().consent_version:
        raise HTTPException(status.HTTP_409_CONFLICT, "Versão do termo desatualizada.")
    if body.accepted:
        user.consent_version, user.consent_at = body.version, utcnow()
    else:
        # revogar consentimento apaga os interesses (LGPD, art. 8º, §5º)
        user.consent_version, user.consent_at = None, None
        user.interests.clear()
    db.commit()
    return Response(status_code=204)


@router.get("/me/interests", response_model=list[InterestOut])
def list_interests(user: ConsentedUser):
    return [InterestOut(id=i.id, label=i.label, depth=i.depth) for i in user.interests]


@router.post("/me/interests", response_model=InterestOut, status_code=201)
def add_interest(body: InterestIn, user: ConsentedUser, db: DbDep):
    if len(user.interests) >= 5:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Você já tem 5 universos guardados. Remova um em “Meus dados” para usar outro.")
    interest = Interest(user_id=user.id, label=body.label.strip(), depth=body.depth)
    db.add(interest)
    db.commit()
    return InterestOut(id=interest.id, label=interest.label, depth=interest.depth)


@router.delete("/me/interests/{interest_id}", status_code=204)
def delete_interest(interest_id: int, user: ConsentedUser, db: DbDep):
    interest = db.scalar(
        select(Interest).where(Interest.id == interest_id, Interest.user_id == user.id)
    )
    if interest is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Interesse não encontrado.")
    db.delete(interest)
    db.commit()
    return Response(status_code=204)


@router.get("/me/reading-prefs", response_model=ReadingPrefs)
def get_prefs(user: CurrentUser):
    return ReadingPrefs(**(user.reading_prefs or {}))


@router.put("/me/reading-prefs", response_model=ReadingPrefs)
def put_prefs(body: ReadingPrefs, user: CurrentUser, db: DbDep):
    user.reading_prefs = body.model_dump()
    db.commit()
    return body


@router.get("/me/export")
def export_my_data(user: CurrentUser):
    """Acesso e portabilidade (LGPD, art. 18, II e V)."""
    return {
        "user_id": user.id,
        "consent_version": user.consent_version,
        "consent_at": user.consent_at,
        "interests": [{"label": i.label, "depth": i.depth} for i in user.interests],
        "reading_prefs": user.reading_prefs,
        "feedback": [
            {"explanation_id": f.explanation_id, "kind": f.kind, "comment": f.comment, "created_at": f.created_at}
            for f in user.feedback
        ],
    }


@router.delete("/me", status_code=204)
def delete_me(user: CurrentUser, db: DbDep):
    """Eliminação (LGPD, art. 18, VI): apaga usuário, interesses e avaliações."""
    db.delete(user)
    db.commit()
    return Response(status_code=204)
