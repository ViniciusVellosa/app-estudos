"""Sessão anônima por token.

Não há cadastro com nome, e-mail ou senha: o aluno recebe um token aleatório
que o front-end guarda. No banco fica só o hash do token. Isso reduz os dados
pessoais tratados (LGPD, art. 6º, III — necessidade) e a carga cognitiva do
login (WCAG 3.3.8).
"""
import hashlib
import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import User, get_db

bearer = HTTPBearer(auto_error=False)


def new_token() -> str:
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


DbDep = Annotated[Session, Depends(get_db)]


def current_user(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    db: DbDep,
) -> User:
    if creds is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sessão não encontrada.")
    user = db.scalar(select(User).where(User.token_hash == hash_token(creds.credentials)))
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sessão inválida ou apagada.")
    return user


CurrentUser = Annotated[User, Depends(current_user)]


def consented_user(user: CurrentUser) -> User:
    if not user.consent_at:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Antes de informar interesses, leia e aceite o termo de consentimento.",
        )
    return user


ConsentedUser = Annotated[User, Depends(consented_user)]
