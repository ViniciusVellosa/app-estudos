"""Ponto de entrada da API.

Rodar localmente:  uv run fastapi dev app/main.py
Documentação:      http://localhost:8000/docs
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import SessionLocal, init_db
from app.providers.base import GenerationError
from app.routers import explanations, me
from app.services.explanations import seed_curated
from app.services.verification import LlmSelfVerifier, NullVerifier

log = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    init_db()
    with SessionLocal() as db:
        seeded = seed_curated(db)
        log.info("explicações curadas carregadas: %s", seeded)
    app.state.generator = None
    # Sem IA não há o que autoverificar: o conteúdo curado é escrito por pessoa
    # e já passou pelos validadores na carga.
    app.state.verifier = NullVerifier()
    if settings.explanation_provider == "llm":
        from app.providers.llm import build_llm_generator

        try:
            generator = build_llm_generator(settings)
            app.state.generator = generator
            # O gerador também implementa StructuredChat: a autoverificação
            # reaproveita cliente, chave e tempo limite já configurados.
            app.state.verifier = LlmSelfVerifier(generator)
            log.info("IA ativa (%s) com autoverificação", generator.name)
        except GenerationError as exc:
            # o app continua funcionando só com conteúdo curado
            log.error("IA desativada: %s", exc)
    yield


app = FastAPI(title="App de Estudos — API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(me.router)
app.include_router(explanations.router)


@app.get("/v1/health", tags=["infra"])
def health():
    return {"status": "ok"}
