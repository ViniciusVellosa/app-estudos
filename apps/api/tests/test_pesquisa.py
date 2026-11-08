"""Pesquisa na web de assuntos fora da biblioteca (decisão D8).

A API do Gemini não é chamada aqui: um pesquisador falso devolve o que a
busca devolveria. O que se testa é o que o app faz com isso.
"""
import pytest

from app.main import app
from app.services.pesquisa import (
    AssuntoRecusado,
    Fonte,
    PesquisaError,
    interpreta,
)

TEXTO = (
    "Uma árvore B é uma estrutura de dados em árvore balanceada usada em bancos de dados "
    "e sistemas de arquivos. Cada nó guarda várias chaves em ordem e tem vários filhos, o que "
    "reduz a altura da árvore e o número de acessos ao disco.\n\n"
    "Todas as folhas ficam no mesmo nível. Quando um nó enche, ele é dividido e a chave do meio "
    "sobe para o nó pai; quando fica com poucas chaves, ele empresta de um irmão ou é fundido.\n\n"
    "A busca, a inserção e a remoção levam tempo logarítmico no número de chaves."
)
RESPOSTA = f"TITULO: Árvore B\nTERMOS: nó; chaves; folhas; inventado\nTEXTO:\n{TEXTO}"
FONTES = [Fonte("Wikipédia — Árvore B", "https://pt.wikipedia.org/wiki/%C3%81rvore_B")]


class PesquisadorFalso:
    name = "falso"

    def __init__(self, resultado=None, erro=None):
        self.resultado = resultado
        self.erro = erro
        self.chamadas = 0

    def pesquisar(self, assunto):
        self.chamadas += 1
        if self.erro:
            raise self.erro
        return self.resultado


@pytest.fixture
def com_pesquisa(client):
    falso = PesquisadorFalso(resultado=interpreta(RESPOSTA, FONTES))
    app.state.pesquisador = falso
    yield falso
    app.state.pesquisador = None


# ------------------------------------------------------------ interpretação


def test_interpreta_o_formato_e_descarta_termo_que_nao_esta_no_texto():
    r = interpreta(RESPOSTA, FONTES)
    assert r.titulo == "Árvore B"
    assert r.texto.startswith("Uma árvore B")
    assert "inventado" not in r.termos  # o validador procuraria por ele no texto
    assert "nó" in r.termos


def test_recusa_de_assunto_que_nao_e_de_estudo():
    with pytest.raises(AssuntoRecusado):
        interpreta("RECUSA: isso não é um assunto de estudo", FONTES)


def test_sem_fonte_nao_ha_referencia():
    # sem fonte externa, seria a IA conferindo a si mesma
    with pytest.raises(PesquisaError):
        interpreta(RESPOSTA, [])


def test_texto_curto_nao_serve_de_referencia():
    with pytest.raises(PesquisaError):
        interpreta("TITULO: X\nTERMOS: a\nTEXTO:\ncurto demais", FONTES)


# ------------------------------------------------------------ rota


def test_assunto_fora_da_biblioteca_e_pesquisado_com_fontes(client, auth, com_pesquisa):
    body = client.post("/v1/assuntos/reconhecer", json={"texto": "árvore B"}, headers=auth).json()
    assert body["encontrado"] is True
    assert body["pesquisado"] is True
    assert body["conceito"]["title"] == "Árvore B"
    assert body["fontes"][0]["url"].startswith("https://")


def test_mesmo_assunto_nao_pesquisa_duas_vezes(client, auth, com_pesquisa):
    for _ in range(2):
        client.post("/v1/assuntos/reconhecer", json={"texto": "Árvore B"}, headers=auth)
    assert com_pesquisa.chamadas == 1


def test_biblioteca_vem_antes_da_pesquisa(client, auth, com_pesquisa):
    body = client.post("/v1/assuntos/reconhecer", json={"texto": "tcp"}, headers=auth).json()
    assert body["conceito"]["slug"] == "tcp-entrega-confiavel"
    assert body["pesquisado"] is False
    assert com_pesquisa.chamadas == 0


def test_falha_na_pesquisa_vira_mensagem_e_sugestoes(client, auth):
    app.state.pesquisador = PesquisadorFalso(erro=PesquisaError("falha ao pesquisar (HTTP 429)"))
    try:
        body = client.post("/v1/assuntos/reconhecer", json={"texto": "árvore B"}, headers=auth).json()
    finally:
        app.state.pesquisador = None
    assert body["encontrado"] is False
    assert "Não consegui pesquisar" in body["motivo"]
    # o detalhe técnico (429) fica no log, não na tela do aluno
    assert "429" not in body["motivo"]
    assert body["sugestoes"]


def test_assunto_pesquisado_serve_explicacao_e_perguntas(client, auth, com_pesquisa):
    slug = client.post("/v1/assuntos/reconhecer", json={"texto": "árvore B"}, headers=auth).json()[
        "conceito"
    ]["slug"]
    interesse = client.post("/v1/me/interests", json={"label": "futebol", "depth": 2}, headers=auth).json()

    # modo curated nos testes: sem IA, a explicação padrão é o texto pesquisado
    exp = client.post(
        "/v1/explanations", json={"concept_slug": slug, "interest_id": interesse["id"]}, headers=auth
    ).json()
    assert exp["neutral_text"].startswith("Uma árvore B")

    r = client.post(
        f"/v1/concepts/{slug}/questions", json={"pergunta": "o que acontece quando um nó enche?"}, headers=auth
    ).json()
    assert r["status"] != "fora_do_conceito"

    fontes = client.get(f"/v1/concepts/{slug}/fontes").json()
    assert fontes[0]["titulo"].startswith("Wikipédia")


def test_le_as_fontes_no_formato_real_do_sdk_do_gemini():
    """Monta a resposta com os tipos do próprio SDK, para pegar nome de campo errado."""
    from google.genai import types

    from app.services.pesquisa import fontes_de

    resposta = types.GenerateContentResponse(
        candidates=[
            types.Candidate(
                content=types.Content(role="model", parts=[types.Part(text=RESPOSTA)]),
                grounding_metadata=types.GroundingMetadata(
                    web_search_queries=["árvore B estrutura de dados"],
                    grounding_chunks=[
                        types.GroundingChunk(web=types.GroundingChunkWeb(uri="https://a.example/1", title="Fonte A")),
                        types.GroundingChunk(web=types.GroundingChunkWeb(uri="https://a.example/1", title="Fonte A")),
                        types.GroundingChunk(web=types.GroundingChunkWeb(uri="https://b.example/2", title="Fonte B")),
                    ],
                ),
            )
        ]
    )
    assert resposta.text.startswith("TITULO:")
    assert [f.titulo for f in fontes_de(resposta)] == ["Fonte A", "Fonte B"]


def test_gemini_pesquisador_monta_a_chamada_com_google_search(monkeypatch):
    from google.genai import types

    from app.config import Settings
    from app.services import pesquisa

    capturado = {}

    class Modelos:
        def generate_content(self, model, contents, config):
            capturado.update(model=model, config=config)
            return types.GenerateContentResponse(
                candidates=[
                    types.Candidate(
                        content=types.Content(role="model", parts=[types.Part(text=RESPOSTA)]),
                        grounding_metadata=types.GroundingMetadata(
                            grounding_chunks=[
                                types.GroundingChunk(web=types.GroundingChunkWeb(uri="https://x.example", title="X"))
                            ]
                        ),
                    )
                ]
            )

    p = pesquisa.GeminiPesquisador(Settings(llm_api_key="k", llm_model="gemini-3.8-flash"))
    p.client = type("C", (), {"models": Modelos()})()
    r = p.pesquisar("árvore B")
    assert r.titulo == "Árvore B"
    assert capturado["model"] == "gemini-3.8-flash"
    assert capturado["config"].tools[0].google_search is not None
