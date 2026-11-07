"""Testes de API: fluxo principal, fallback da IA e direitos LGPD."""
from app.content import load_concepts
from app.db import SessionLocal
from app.schemas import Refusal
from app.services.explanations import NOTICE_AI_VERIFIED, get_explanation

SLUG = "tcp-entrega-confiavel"


def test_health(client):
    assert client.get("/v1/health").json() == {"status": "ok"}


def test_interest_requires_consent(client):
    token = client.post("/v1/session").json()["token"]
    r = client.post(
        "/v1/me/interests",
        json={"label": "futebol", "depth": 2},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 403


def test_curated_explanation_flow(client, auth):
    interest = client.post("/v1/me/interests", json={"label": "Futebol", "depth": 2}, headers=auth).json()
    r = client.post(
        "/v1/explanations",
        json={"concept_slug": SLUG, "interest_id": interest["id"]},
        headers=auth,
    )
    body = r.json()
    assert r.status_code == 200
    assert body["personalized"] is True
    assert body["provider"] == "curated"
    assert len(body["payload"]["onde_falha"]) >= 1


def test_unknown_interest_falls_back_to_neutral(client, auth):
    interest = client.post("/v1/me/interests", json={"label": "xadrez", "depth": 1}, headers=auth).json()
    body = client.post(
        "/v1/explanations",
        json={"concept_slug": SLUG, "interest_id": interest["id"]},
        headers=auth,
    ).json()
    assert body["personalized"] is False
    assert body["neutral_text"]
    assert body["notice"]


def test_wrong_feedback_takes_explanation_out_of_circulation(client, auth):
    interest = client.post("/v1/me/interests", json={"label": "futebol", "depth": 2}, headers=auth).json()
    req = {"concept_slug": SLUG, "interest_id": interest["id"]}
    first = client.post("/v1/explanations", json=req, headers=auth).json()
    r = client.post(f"/v1/explanations/{first['id']}/feedback", json={"kind": "errada"}, headers=auth)
    assert r.status_code == 204
    second = client.post("/v1/explanations", json=req, headers=auth).json()
    assert second["personalized"] is False


def test_delete_me_erases_everything(client, auth):
    from sqlalchemy import func, select

    from app.db import Feedback, Interest, User

    interest = client.post("/v1/me/interests", json={"label": "futebol", "depth": 3}, headers=auth).json()
    exp = client.post(
        "/v1/explanations", json={"concept_slug": SLUG, "interest_id": interest["id"]}, headers=auth
    ).json()
    assert exp["id"] is not None  # explicação curada, com id para avaliar
    r = client.post(f"/v1/explanations/{exp['id']}/feedback", json={"kind": "util"}, headers=auth)
    assert r.status_code == 204
    export = client.get("/v1/me/export", headers=auth).json()
    assert export["feedback"][0]["kind"] == "util"  # acesso inclui as avaliações (art. 18, II)
    user_id = export["user_id"]

    assert client.delete("/v1/me", headers=auth).status_code == 204
    assert client.get("/v1/me/export", headers=auth).status_code == 401
    with SessionLocal() as db:
        assert db.get(User, user_id) is None
        assert db.scalar(select(func.count()).select_from(Interest).where(Interest.user_id == user_id)) == 0
        assert db.scalar(select(func.count()).select_from(Feedback).where(Feedback.user_id == user_id)) == 0


def test_revoking_consent_deletes_interests(client, auth):
    client.post("/v1/me/interests", json={"label": "anime", "depth": 3}, headers=auth)
    client.post("/v1/consent", json={"version": "2026-1", "accepted": False}, headers=auth)
    export = client.get("/v1/me/export", headers=auth).json()
    assert export["interests"] == []


class FakeGenerator:
    """Simula o LLM sem chamar a internet (nada de custo nem chave no CI)."""

    name = "llm:fake"

    def __init__(self, results):
        self.results = list(results)
        self.calls = 0

    def generate(self, req):
        self.calls += 1
        return self.results.pop(0)


def test_llm_refusal_returns_neutral(client):
    concept = load_concepts()[SLUG]
    gen = FakeGenerator([Refusal(status="sem_analogia_fiel", motivo="universo sem fluxo ordenado")])
    with SessionLocal() as db:
        out = get_explanation(db, concept, "culinária", 1, "iniciante", gen)
    assert out.personalized is False
    assert "fiel" in out.notice


def test_llm_bad_output_is_retried_then_falls_back(client):
    from app.content import load_curated

    concept = load_concepts()[SLUG]
    bad = load_curated(SLUG, "futebol").model_copy(
        update={"cena": "O treinador só manda o próximo depois de confirmar que o anterior chegou."}
    )
    gen = FakeGenerator([bad, bad])
    with SessionLocal() as db:
        out = get_explanation(db, concept, "pokemon", 2, "iniciante", gen)
    assert gen.calls == 2  # uma nova tentativa com as correções
    assert out.personalized is False


def test_llm_valid_draft_is_served_after_verification(client):
    """ADR 0003: não há mais portão humano; o que passa na verificação é exibido.

    Aqui o verificador é o NullVerifier (padrão), então quem decide são os
    validadores. Os três caminhos da autoverificação estão em
    tests/test_verification.py.
    """
    from app.content import load_curated

    concept = load_concepts()[SLUG]
    good = load_curated(SLUG, "futebol")
    gen = FakeGenerator([good])
    with SessionLocal() as db:
        out = get_explanation(db, concept, "basquete", 2, "iniciante", gen)
    assert out.personalized is True
    assert out.status == "verified"
    assert out.notice == NOTICE_AI_VERIFIED  # o aluno sabe que não houve professor
