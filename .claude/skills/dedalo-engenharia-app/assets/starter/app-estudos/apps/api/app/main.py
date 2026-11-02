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

log = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    init_db()
    with SessionLocal() as db:
        seeded = seed_curated(db)
        log.info("explicações curadas carregadas: %s", seeded)
    app.state.generator = None
    if settings.explanation_provider == "llm":
        from app.providers.llm import build_llm_generator

        try:
            app.state.generator = build_llm_generator(settings)
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
