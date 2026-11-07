"""Banco de dados com SQLAlchemy 2.x (modo síncrono, mais simples de aprender).

Em Docker usamos PostgreSQL; nos testes, SQLite em memória.
"""
from collections.abc import Iterator
from datetime import UTC, datetime

from sqlalchemy import JSON, ForeignKey, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy.pool import StaticPool

from app.config import get_settings


def utcnow() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


class User(Base):
    """Usuário anônimo: nenhum nome ou e-mail é coletado (minimização, LGPD)."""

    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    consent_version: Mapped[str | None] = mapped_column(String(20))
    consent_at: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    interests: Mapped[list["Interest"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    reading_prefs: Mapped[dict] = mapped_column(JSON, default=dict)
    # apagar o usuário apaga também as avaliações dele (LGPD, art. 18, VI)
    feedback: Mapped[list["Feedback"]] = relationship(cascade="all, delete-orphan")


class Interest(Base):
    __tablename__ = "interests"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    label: Mapped[str] = mapped_column(String(60))
    depth: Mapped[int]
    user: Mapped[User] = relationship(back_populates="interests")


class Explanation(Base):
    """Explicação gerada ou curada. Não guarda quem pediu: é reaproveitável."""

    __tablename__ = "explanations"
    id: Mapped[int] = mapped_column(primary_key=True)
    concept_slug: Mapped[str] = mapped_column(String(80), index=True)
    interest_label: Mapped[str] = mapped_column(String(60), index=True)
    level: Mapped[str] = mapped_column(String(20))
    provider: Mapped[str] = mapped_column(String(40))
    prompt_version: Mapped[str] = mapped_column(String(20))
    # approved = curada por pessoa | verified = gerada por IA e aprovada na
    # autoverificacao (ADR 0003) | under_review = alguem marcou "esta errada"
    # | rejected = reprovada na revisao manual. So os dois primeiros sao servidos.
    status: Mapped[str] = mapped_column(String(20))
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


class Feedback(Base):
    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(primary_key=True)
    explanation_id: Mapped[int] = mapped_column(ForeignKey("explanations.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    kind: Mapped[str] = mapped_column(String(20))
    comment: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


def _make_engine(url: str):
    if url.startswith("sqlite"):
        kwargs = {"connect_args": {"check_same_thread": False}}
        if url in ("sqlite://", "sqlite:///:memory:"):
            kwargs["poolclass"] = StaticPool
        return create_engine(url, **kwargs)
    return create_engine(url, pool_pre_ping=True)


engine = _make_engine(get_settings().database_url)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def init_db() -> None:
    """Cria as tabelas. Em um projeto maior, use migrações (Alembic)."""
    Base.metadata.create_all(engine)


def get_db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session
