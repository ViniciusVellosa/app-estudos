"""Configuração lida de variáveis de ambiente (12-factor).

Nada de segredo no código: chaves e senhas vêm do .env (fora do Git) ou dos
secrets do ambiente de execução.
"""
from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./dev.db"
    content_dir: str = "content"
    cors_origins: list[str] = ["http://localhost:5173"]

    # Motor de explicações: "curated" funciona sem IA (Mágico de Oz).
    explanation_provider: Literal["curated", "llm"] = "curated"
    llm_backend: Literal["anthropic", "openai_compatible"] = "anthropic"
    llm_model: str = ""
    llm_api_key: str = Field(default="", repr=False)
    llm_base_url: str = ""  # para servidores compatíveis com OpenAI (ex.: Ollama local)
    llm_timeout_s: float = 30.0
    llm_max_output_tokens: int = 1500
    prompt_version: str = "1"

    # Só explicações aprovadas aparecem para o aluno? (True no teste de usabilidade)
    serve_only_approved: bool = True

    consent_version: str = "2026-1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
