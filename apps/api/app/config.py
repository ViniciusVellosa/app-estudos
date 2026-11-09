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
    # Modelo só para ESCREVER a explicação (rascunho da analogia). Vazio = o
    # mesmo LLM_MODEL. Permite um modelo maior onde a qualidade aparece para o
    # aluno, e um modelo leve (com cota maior) na referência e na verificação,
    # que fazem a maior parte das chamadas. Se ele bater no limite de uso, a
    # explicação é escrita com LLM_MODEL.
    llm_model_explicacao: str = ""
    llm_api_key: str = Field(default="", repr=False)
    llm_base_url: str = ""  # para servidores compatíveis com OpenAI (ex.: Ollama local)
    llm_timeout_s: float = 30.0
    # O SDK repete sozinho em 429 e 5xx, com espera entre as tentativas. Isso
    # é bom em produção e péssimo para diagnosticar: um limite de uso (429)
    # chega como tempo esgotado depois de dois minutos, escondendo a causa.
    llm_max_retries: int = 1
    # Quanto o modelo pode "pensar" antes de responder, nos provedores que
    # expõem isso (Gemini, OpenAI). Vazio = não enviar o parâmetro.
    #
    # "low" é o padrão aqui de propósito: as perguntas de checagem da
    # autoverificação são julgamentos curtos contra um texto que já está no
    # pedido, e raciocínio longo nelas custa tempo sem ganho claro — Huang et
    # al. (2024) mostram que mais autorraciocínio não melhora de forma
    # confiável. Nos modelos Gemini 3 o raciocínio não pode ser desligado.
    llm_reasoning_effort: Literal["", "none", "low", "medium", "high"] = "low"
    llm_max_output_tokens: int = 1500
    prompt_version: str = "1"

    # Pesquisa na web de assuntos fora da biblioteca (decisão D8). "gemini"
    # usa a ferramenta google_search da API do Gemini, com a mesma chave
    # LLM_API_KEY. Vazio = só a biblioteca de conteúdos.
    # "ia" = sem busca: a própria IA escreve a referência com o conhecimento
    # dela (decisão D9). "gemini" tenta a busca e, se falhar, usa "ia".
    pesquisa_provider: Literal["", "gemini", "ia"] = ""
    # Perguntas de checagem por explicação na autoverificação (D6). Cada uma
    # é uma chamada a mais ao modelo; 1 economiza cota (ver verification.py).
    autoverificacao_perguntas: int = Field(default=1, ge=1, le=6)
    pesquisa_model: str = ""  # vazio = o mesmo LLM_MODEL

    consent_version: str = "2026-1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
