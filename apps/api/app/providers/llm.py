"""Gerador com modelo de linguagem (LLM).

Dois backends:
- "anthropic": API da Anthropic (Claude) com saída estruturada
  (`client.messages.parse(output_format=ModeloPydantic)`; o SDK envia o schema
  em `output_config.format` e valida a resposta).
- "openai_compatible": qualquer servidor compatível com a API de chat da
  OpenAI. Cobre o **Gemini**, pela camada de compatibilidade do Google em
  https://generativelanguage.googleapis.com/v1beta/openai/ (verificado na
  documentação oficial em 07/11/2026), e também modelos locais e gratuitos
  (Ollama ≥ 0.5 em http://localhost:11434/v1).

Os SDKs são dependências opcionais (`uv sync --extra llm`). Confira na
documentação do provedor, na data, o nome do modelo e os parâmetros.

Mesmo com saída estruturada, o provedor garante só o FORMATO, não o
conteúdo. Por isso a resposta passa sempre pelo Pydantic, pela autoverificação
(app/services/verification.py) e pelos validadores anti-alucinação
(app/validators/grounding.py).

As duas classes também implementam `StructuredChat.ask`: é por ele que a
autoverificação faz as próprias perguntas, reaproveitando cliente e chave.

Segurança (OWASP Top 10 para aplicações com LLM, 2025):
- LLM01 injeção de prompt: o interesse do aluno entra delimitado e escapado,
  como dado, nunca como instrução;
- LLM02 vazamento de dados: nenhum identificador do aluno vai para o provedor;
- LLM05 tratamento de saída: a saída é validada antes de chegar ao aluno e o
  front-end a exibe como texto, nunca como HTML;
- LLM09 desinformação: texto-base revisado + autoverificação (ADR 0003) +
  validadores determinísticos;
- LLM10 consumo sem limite: max_tokens, timeout e cache de explicações.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

from pydantic import BaseModel, ConfigDict, ValidationError

from app.config import Settings, get_settings
from app.providers.base import ExplanationRequestData, GenerationError, M
from app.schemas import ExplanationPayload, Refusal

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "explicacao_sistema.md"


class GenerationResult(BaseModel):
    """Envelope único: explicação nos seis passos OU recusa."""

    model_config = ConfigDict(extra="forbid")
    resultado: ExplanationPayload | Refusal


@lru_cache
def system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def user_message(req: ExplanationRequestData) -> str:
    """Monta a mensagem com as entradas delimitadas e escapadas.

    O rótulo do interesse vem do aluno: é escapado para não fechar as tags e
    não carrega nenhum identificador pessoal.
    """
    # O texto-base vem primeiro: é igual para todos os alunos e pode ser
    # reaproveitado pelo cache de prompt do provedor; o que varia vem depois.
    parts = [
        f"<texto_base>\n{escape(req.concept.base_text)}\n</texto_base>",
        f"<conceito>{escape(req.concept.title)}</conceito>",
        f"<nivel>{escape(req.level)}</nivel>",
        f"<interesse rotulo={quoteattr(req.interest_label)} profundidade=\"{req.depth}\"/>",
    ]
    if req.feedback:
        parts.append(f"<correcoes>{escape(req.feedback)}</correcoes>")
    return "\n".join(parts)


def descreve_falha(exc: Exception) -> str:
    """Mensagem de falha com o código HTTP, quando houver.

    Sem isso, um 429 (limite de uso) e um 500 do provedor chegam ao log como
    o mesmo "falha ao chamar o provedor", e descobrir qual dos dois é custa
    várias tentativas — cada uma gastando cota.

    Só o tipo e o código: o corpo da resposta não entra, para não arrastar
    nada que o provedor devolva junto.
    """
    codigo = getattr(exc, "status_code", None)
    return (
        f"falha ao chamar o provedor: {type(exc).__name__}"
        + (f" (HTTP {codigo})" if codigo else "")
    )


class AnthropicGenerator:
    name = "llm:anthropic"

    def __init__(self, settings: Settings):
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover
            raise GenerationError("instale o extra 'llm' (pacote anthropic)") from exc
        if not settings.llm_api_key or not settings.llm_model:
            raise GenerationError("defina LLM_API_KEY e LLM_MODEL")
        self.client = anthropic.Anthropic(
            api_key=settings.llm_api_key,
            timeout=settings.llm_timeout_s,
            max_retries=settings.llm_max_retries,
        )
        self.settings = settings

    def ask(self, system: str, user: str, output_model: type[M]) -> M:
        try:
            response = self.client.messages.parse(
                model=self.settings.llm_model,
                max_tokens=self.settings.llm_max_output_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
                output_format=output_model,
            )
        except ValidationError as exc:
            raise GenerationError("resposta fora do formato") from exc
        except Exception as exc:  # rede, limite de uso, tempo esgotado
            raise GenerationError(descreve_falha(exc)) from exc
        if response.stop_reason == "max_tokens":
            raise GenerationError("resposta cortada por max_tokens; aumente LLM_MAX_OUTPUT_TOKENS")
        if response.stop_reason == "refusal" or response.parsed_output is None:
            raise GenerationError("o modelo recusou ou não devolveu a saída estruturada")
        return response.parsed_output

    def generate(self, req: ExplanationRequestData) -> ExplanationPayload | Refusal:
        return self.ask(system_prompt(), user_message(req), GenerationResult).resultado


class OpenAICompatibleGenerator:
    name = "llm:openai_compatible"

    def __init__(self, settings: Settings):
        try:
            import openai
        except ImportError as exc:  # pragma: no cover
            raise GenerationError("instale o extra 'llm' (pacote openai)") from exc
        if not settings.llm_model:
            raise GenerationError("defina LLM_MODEL")
        self.client = openai.OpenAI(
            api_key=settings.llm_api_key or "nao-usado-localmente",
            base_url=settings.llm_base_url or None,
            timeout=settings.llm_timeout_s,
            max_retries=settings.llm_max_retries,
        )
        self.settings = settings

    def ask(self, system: str, user: str, output_model: type[M]) -> M:
        """Pede a resposta já no formato do modelo Pydantic.

        Usa `chat.completions.parse`, o auxiliar do SDK que monta o
        `response_format` de JSON Schema e devolve o objeto validado. É a
        forma que a documentação do Gemini mostra para a camada compatível
        com a OpenAI, e evita montar o schema à mão — o nosso tem união e
        referências internas, que cada provedor aceita de um jeito.
        """
        extras = {}
        if self.settings.llm_reasoning_effort:
            extras["reasoning_effort"] = self.settings.llm_reasoning_effort
        try:
            resp = self.client.chat.completions.parse(
                model=self.settings.llm_model,
                max_tokens=self.settings.llm_max_output_tokens,
                temperature=0,
                response_format=output_model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                **extras,
            )
            choice = resp.choices[0]
            if choice.finish_reason == "length":
                raise GenerationError("resposta cortada por max_tokens")
            parsed = getattr(choice.message, "parsed", None)
            if parsed is not None:
                return parsed
            # Provedor que aceitou o pedido mas devolveu só texto: ainda dá
            # para aproveitar, desde que o texto seja o JSON pedido.
            data = json.loads(choice.message.content or "")
        except GenerationError:
            raise
        except json.JSONDecodeError as exc:
            raise GenerationError("o modelo não devolveu JSON válido") from exc
        except Exception as exc:
            raise GenerationError(descreve_falha(exc)) from exc
        try:
            return output_model.model_validate(data)
        except ValidationError as exc:
            raise GenerationError(f"resposta fora do formato: {exc.error_count()} erro(s)") from exc

    def generate(self, req: ExplanationRequestData) -> ExplanationPayload | Refusal:
        return self.ask(system_prompt(), user_message(req), GenerationResult).resultado


def build_llm_generator(settings: Settings | None = None):
    settings = settings or get_settings()
    if settings.llm_backend == "anthropic":
        return AnthropicGenerator(settings)
    return OpenAICompatibleGenerator(settings)
