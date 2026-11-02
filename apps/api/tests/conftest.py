import os

# Configura o ambiente de teste ANTES de importar o app.
# SQLite em memória por padrão; TEST_DATABASE_URL roda os mesmos testes no PostgreSQL (CI).
os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", "sqlite://")
os.environ["EXPLANATION_PROVIDER"] = "curated"
os.environ.setdefault("CONTENT_DIR", os.path.join(os.path.dirname(__file__), "..", "content"))

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(autouse=True)
def banco_limpo():
    """Cada teste começa com o banco vazio (evita um teste depender de outro)."""
    from app.db import Base, engine

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth(client):
    """Sessão com consentimento dado e um interesse cadastrado."""
    token = client.post("/v1/session").json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    r = client.post("/v1/consent", json={"version": "2026-1", "accepted": True}, headers=headers)
    assert r.status_code == 204
    return headers
