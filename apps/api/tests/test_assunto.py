"""Assunto digitado no chat → conteúdo da biblioteca (decisão D7)."""
import pytest

from app.services.assunto import reconhece

TCP = "tcp-entrega-confiavel"


@pytest.mark.parametrize(
    "texto",
    [
        "TCP",
        "quero entender o tcp",
        "como funciona a janela deslizante?",
        "Retransmissão",
        "entrega confiável",
        "o que é ACK",
    ],
)
def test_reconhece_o_tcp_pelas_palavras_do_aluno(texto):
    assert reconhece(texto).conceito.slug == TCP


@pytest.mark.parametrize("texto", ["fotossíntese", "me explica o que é DNS", "quero aprender", "   "])
def test_assunto_fora_da_biblioteca_nao_e_forcado(texto):
    r = reconhece(texto)
    assert r.conceito is None
    # nunca um beco sem saída: sempre há o que sugerir
    assert [c.slug for c in r.sugestoes] == [TCP]


def test_rota_reconhece_o_assunto(client, auth):
    r = client.post("/v1/assuntos/reconhecer", json={"texto": "janela deslizante"}, headers=auth)
    assert r.status_code == 200
    body = r.json()
    assert body["encontrado"] is True
    assert body["conceito"]["slug"] == TCP


def test_rota_assunto_desconhecido_traz_sugestoes(client, auth):
    body = client.post("/v1/assuntos/reconhecer", json={"texto": "fotossíntese"}, headers=auth).json()
    assert body["encontrado"] is False
    assert body["conceito"] is None
    assert body["sugestoes"][0]["slug"] == TCP


def test_rota_exige_consentimento(client):
    token = client.post("/v1/session").json()["token"]
    r = client.post(
        "/v1/assuntos/reconhecer",
        json={"texto": "tcp"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 403
