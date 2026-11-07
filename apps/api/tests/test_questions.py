"""Pergunta livre restrita ao conceito (RF11, decisão D5).

O que estes testes protegem é a promessa feita ao aluno na interface: o campo
aceita qualquer texto, mas a resposta nunca sai do conceito que ele escolheu.
Os três critérios de aceite de RF11 (requisitos.md) viram um teste cada.
"""
import pytest

from app.content import load_concepts
from app.services.questions import answer_question, no_conceito

SLUG = "tcp-entrega-confiavel"
TITULO = "Entrega confiável no TCP (confirmações e janela deslizante)"


@pytest.fixture
def conceito():
    return load_concepts()[SLUG]


# ------------------------------------------------- porteiro de assunto

@pytest.mark.parametrize(
    "pergunta",
    [
        "o que acontece se o ACK se perder?",
        "como funciona a janela deslizante?",
        "para que serve o número de sequência?",
        "o remetente precisa esperar a confirmação?",
        "e se a rede reordenar os pacotes?",
    ],
)
def test_reconhece_pergunta_do_conceito(conceito, pergunta):
    assert no_conceito(pergunta, conceito) is True


@pytest.mark.parametrize(
    "pergunta",
    [
        "quem ganhou o jogo ontem?",
        "me explica o que é DNS",
        "qual é a capital da Austrália?",
        "você pode escrever meu trabalho inteiro?",
    ],
)
def test_reconhece_pergunta_de_outro_assunto(conceito, pergunta):
    assert no_conceito(pergunta, conceito) is False


def test_pergunta_na_linguagem_da_analogia_e_aceita(conceito):
    """A cena foi o app que ofereceu; recusá-la seria incoerente.

    Sem os termos do universo, "e se o zagueiro errar o passe?" cairia como
    fora do conceito — um erro grosseiro aos olhos de quem está lendo a
    explicação do futebol naquele momento.
    """
    universo = ["futebol", "zagueiro", "passe", "treinador"]
    assert no_conceito("e se o zagueiro errar o passe?", conceito) is False
    assert no_conceito("e se o zagueiro errar o passe?", conceito, universo) is True


def test_casamento_por_raiz_cobre_plural_e_flexao(conceito):
    # "segmentos" no plural, "perde" em vez de "perder"
    assert no_conceito("os segmentos podem se perde no caminho?", conceito) is True


# --------------------------------------------- critérios de aceite RF11

def test_pergunta_dentro_do_conceito_e_respondida(conceito):
    r = answer_question("o que o receptor devolve quando recebe um segmento?", conceito)
    assert r.status == "respondida"
    assert r.trechos, "a resposta extrativa precisa citar o texto-base"
    # cada trecho é recorte literal do material revisado, não geração
    for trecho in r.trechos:
        assert trecho in conceito.base_text


def test_pergunta_fora_do_conceito_e_recusada_com_as_duas_saidas(conceito):
    r = answer_question("me explica o que é DNS", conceito)
    assert r.status == "fora_do_conceito"
    assert TITULO in r.texto  # a recusa nomeia o conceito atual
    assert r.trechos == []


def test_pergunta_do_conceito_sem_cobertura_vira_nao_sei(conceito, monkeypatch):
    """Dentro do assunto, mas o texto-base não traz: diz que não sabe.

    Forçamos o caso esvaziando as frases do texto-base, para não depender de
    achar uma pergunta que o material por acaso não cubra.
    """
    import app.services.questions as mod

    monkeypatch.setattr(mod, "frases", lambda _texto: [])
    r = answer_question("como funciona a janela deslizante?", conceito)
    assert r.status == "sem_base"
    assert "não sei" in r.texto or "não está no material" in r.texto


# ------------------------------------------------------------ pela API

def interesse(client, auth, label="futebol"):
    return client.post(
        "/v1/me/interests", json={"label": label, "depth": 2}, headers=auth
    ).json()


def test_endpoint_responde_dentro_do_conceito(client, auth):
    r = client.post(
        f"/v1/concepts/{SLUG}/questions",
        json={"pergunta": "o que é a janela?"},
        headers=auth,
    )
    assert r.status_code == 200
    corpo = r.json()
    assert corpo["status"] == "respondida"
    assert corpo["concept_title"] == TITULO


def test_endpoint_recusa_fora_do_conceito(client, auth):
    r = client.post(
        f"/v1/concepts/{SLUG}/questions",
        json={"pergunta": "quem ganhou o jogo ontem?"},
        headers=auth,
    )
    assert r.json()["status"] == "fora_do_conceito"


def test_endpoint_usa_o_universo_do_interesse_informado(client, auth):
    """Com interest_id, os termos da analogia entram no porteiro."""
    i = interesse(client, auth, "futebol")
    client.post(
        "/v1/explanations",
        json={"concept_slug": SLUG, "interest_id": i["id"]},
        headers=auth,
    )
    # "atacante" e "gritar" só existem na cena do futebol, não no texto-base
    pergunta = {"pergunta": "e se o atacante não gritar?"}
    sem = client.post(f"/v1/concepts/{SLUG}/questions", json=pergunta, headers=auth).json()
    com = client.post(
        f"/v1/concepts/{SLUG}/questions",
        json={**pergunta, "interest_id": i["id"]},
        headers=auth,
    ).json()
    assert sem["status"] == "fora_do_conceito"
    assert com["status"] != "fora_do_conceito"


def test_endpoint_exige_consentimento(client):
    token = client.post("/v1/session").json()["token"]
    r = client.post(
        f"/v1/concepts/{SLUG}/questions",
        json={"pergunta": "o que é a janela?"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 403


def test_endpoint_404_para_conceito_inexistente(client, auth):
    r = client.post(
        "/v1/concepts/nao-existe/questions",
        json={"pergunta": "o que é a janela?"},
        headers=auth,
    )
    assert r.status_code == 404


def test_pergunta_vazia_e_rejeitada_pelo_schema(client, auth):
    r = client.post(f"/v1/concepts/{SLUG}/questions", json={"pergunta": ""}, headers=auth)
    assert r.status_code == 422
