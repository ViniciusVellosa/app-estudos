"""Configuração lida de variáveis de ambiente (12-factor).

Nada de segredo no código: chaves e senhas vêm do .env (fora do Git) ou dos
secrets do ambiente de execução.
"""
from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Dois caminhos porque o .env do projeto fica na raiz do repositório (é o
    # que o Compose usa), mas a API costuma ser rodada de dentro de apps/api.
    # Sem o primeiro, `uv run fastapi dev` e `python -m app.smoke` ignorariam
    # a configuração em silêncio e cairiam nos padrões. O último vence, então
    # um .env dentro de apps/api sobrepõe o da raiz, se alguém quiser isso.
    model_config = SettingsConfigDict(env_file=("../../.env", ".env"), extra="ignore")

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

    consent_version: str = "2026-1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
