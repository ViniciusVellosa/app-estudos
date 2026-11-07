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


def test_wrong_feedback_on_curated_is_recorded_without_removing_it(client, auth):
    """RF05 em conteúdo escrito à mão: registra, mas não derruba.

    Um clique anônimo não pode tirar do ar material revisado por pessoa — no
    teste de usabilidade, o primeiro participante a cumprir a tarefa T5
    deixaria os seguintes sem explicação. Quem decide é a revisão
    (`python -m app.review`).
    """
    from sqlalchemy import func, select

    from app.db import Feedback

    interest = client.post("/v1/me/interests", json={"label": "futebol", "depth": 2}, headers=auth).json()
    req = {"concept_slug": SLUG, "interest_id": interest["id"]}
    first = client.post("/v1/explanations", json=req, headers=auth).json()
    assert first["provider"] == "curated"

    r = client.post(f"/v1/explanations/{first['id']}/feedback", json={"kind": "errada"}, headers=auth)
    assert r.status_code == 204

    second = client.post("/v1/explanations", json=req, headers=auth).json()
    assert second["personalized"] is True, "conteúdo curado continua em circulação"

    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(Feedback)) == 1


def test_wrong_feedback_on_ai_content_takes_it_out_of_circulation(client):
    """Em conteúdo gerado por IA, a dúvida tira do ar na hora (RNF03)."""
    from app.content import load_curated

    concept = load_concepts()[SLUG]
    gen = FakeGenerator([load_curated(SLUG, "futebol")])
    with SessionLocal() as db:
        gerada = get_explanation(db, concept, "pokemon", 2, "iniciante", gen)
    assert gerada.status == "verified"

    token = client.post("/v1/session").json()["token"]
    cabecalho = {"Authorization": f"Bearer {token}"}
    client.post("/v1/consent", json={"version": "2026-1", "accepted": True}, headers=cabecalho)
    r = client.post(
        f"/v1/explanations/{gerada.id}/feedback", json={"kind": "errada"}, headers=cabecalho
    )
    assert r.status_code == 204

    with SessionLocal() as db:
        de_novo = get_explanation(db, concept, "pokemon", 2, "iniciante", None)
    assert de_novo.personalized is False


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


# --------------------------------------------------------------- RF09


def test_troca_de_universo_guarda_uma_explicacao_por_interesse(client):
    """RF09: trocar de universo e voltar, sem perder nem refazer nada.

    A explicação é indexada por conceito + interesse + nível, então cada
    universo tem a sua. Voltar ao anterior é leitura do cache: nenhuma
    chamada nova de IA, e o texto é exatamente o mesmo de antes.
    """
    from app.content import load_curated

    concept = load_concepts()[SLUG]
    outra = load_curated(SLUG, "futebol").model_copy(
        update={"cena": "No tabuleiro, várias peças avançam antes de o adversário responder."}
    )
    gen = FakeGenerator([outra])

    with SessionLocal() as db:
        futebol = get_explanation(db, concept, "futebol", 2, "iniciante", gen)  # curada
        xadrez = get_explanation(db, concept, "xadrez", 2, "iniciante", gen)  # gerada

    assert gen.calls == 1, "o universo curado não deve gastar IA"
    assert futebol.interest_label == "futebol"
    assert xadrez.interest_label == "xadrez"
    assert futebol.payload != xadrez.payload
    assert futebol.concept_slug == xadrez.concept_slug  # o conceito não muda

    with SessionLocal() as db:
        de_volta = get_explanation(db, concept, "futebol", 2, "iniciante", gen)
    assert gen.calls == 1, "voltar ao universo anterior não regenera"
    assert de_volta.payload == futebol.payload


def test_endpoint_aceita_trocar_de_interesse_no_mesmo_conceito(client, auth):
    """A troca pela API é o mesmo POST com outro interest_id."""
    primeiro = client.post(
        "/v1/me/interests", json={"label": "futebol", "depth": 2}, headers=auth
    ).json()
    segundo = client.post(
        "/v1/me/interests", json={"label": "One Piece", "depth": 3}, headers=auth
    ).json()

    a = client.post(
        "/v1/explanations",
        json={"concept_slug": SLUG, "interest_id": primeiro["id"]},
        headers=auth,
    )
    b = client.post(
        "/v1/explanations",
        json={"concept_slug": SLUG, "interest_id": segundo["id"]},
        headers=auth,
    )
    assert a.status_code == 200 and b.status_code == 200
    assert a.json()["concept_slug"] == b.json()["concept_slug"] == SLUG
    # sem IA e sem explicação curada para "One Piece", o app mostra a padrão
    # em vez de inventar: é o comportamento do modo Mágico de Oz.
    assert a.json()["personalized"] is True
    assert b.json()["personalized"] is False
    assert b.json()["notice"]


def test_interesse_de_outro_usuario_nao_serve_para_explicar(client, auth):
    outro = client.post("/v1/session").json()["token"]
    cabecalho = {"Authorization": f"Bearer {outro}"}
    client.post("/v1/consent", json={"version": "2026-1", "accepted": True}, headers=cabecalho)
    alheio = client.post(
        "/v1/me/interests", json={"label": "futebol", "depth": 2}, headers=cabecalho
    ).json()

    r = client.post(
        "/v1/explanations",
        json={"concept_slug": SLUG, "interest_id": alheio["id"]},
        headers=auth,
    )
    assert r.status_code == 404
