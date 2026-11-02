# syntax=docker/dockerfile:1
# Back-end FastAPI com uv (padrão do guia oficial: docs.astral.sh/uv/guides/integration/docker)
# Versões verificadas em 29/10/2026 — confira as atuais antes de fixar.

FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1 UV_PYTHON_DOWNLOADS=0
WORKDIR /app
# 1) só as dependências (camada reaproveitada enquanto o uv.lock não muda)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --extra llm
# 2) o código
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --extra llm

FROM python:3.14-slim
# usuário sem privilégios de root
RUN groupadd --system app && useradd --system --gid app --home /app app
WORKDIR /app
COPY --from=builder --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1
USER app
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --retries=5 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/v1/health')" || exit 1
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
