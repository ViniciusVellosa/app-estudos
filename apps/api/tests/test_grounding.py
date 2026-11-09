"""Testes dos validadores anti-alucinação.

O caso "pokemon_pare_e_espere" é um teste de regressão de um erro real
encontrado durante o projeto: uma analogia que soava certa, mas descrevia o
protocolo pare-e-espere em vez do TCP com janela deslizante.
"""
import copy

import pytest
from pydantic import ValidationError

from app.content import load_concepts, load_curated
from app.schemas import ExplanationPayload
from app.validators.grounding import quote_in_source, validate_explanation

SLUG = "tcp-entrega-confiavel"


@pytest.fixture
def concept():
    return load_concepts()[SLUG]


@pytest.fixture
def good():
    return load_curated(SLUG, "futebol")


def test_curated_explanation_passes(concept, good):
    report = validate_explanation(good, concept.rules)
    assert report.ok, report.errors


def test_pokemon_stop_and_wait_regression(concept, good):
    bad = copy.deepcopy(good.model_dump())
    bad["cena"] = (
        "O treinador só manda o próximo Pokémon para a batalha depois de confirmar "
        "que o anterior chegou."
    )
    bad["mapeamento"][0] = {
        "universo": "treinador manda um Pokémon por vez",
        "tecnico": "envio de segmentos",
        "trecho_base": "Cada segmento enviado carrega um número de sequência",
    }
    report = validate_explanation(ExplanationPayload.model_validate(bad), concept.rules)
    assert not report.ok
    assert any("armadilha" in e for e in report.errors)


def test_invented_quote_is_rejected(concept, good):
    bad = copy.deepcopy(good.model_dump())
    bad["mapeamento"][1]["trecho_base"] = "O ACK é enviado a cada 200 milissegundos pelo roteador"
    report = validate_explanation(ExplanationPayload.model_validate(bad), concept.rules)
    assert not report.ok
    assert any("trecho_base" in e for e in report.errors)


def test_universe_words_leaking_into_technical_text(concept, good):
    bad = copy.deepcopy(good.model_dump())
    bad["reformulacao_tecnica"] += " É como o atacante gritando para o técnico."
    report = validate_explanation(ExplanationPayload.model_validate(bad), concept.rules)
    assert not report.ok
    assert any("termos do universo" in e for e in report.errors)


def test_long_scene_is_rejected(concept, good):
    bad = copy.deepcopy(good.model_dump())
    bad["cena"] = " ".join(["bola"] * 95)
    report = validate_explanation(ExplanationPayload.model_validate(bad), concept.rules)
    assert any("cena com" in e for e in report.errors)


def test_generic_limit_is_rejected(concept, good):
    bad = copy.deepcopy(good.model_dump())
    bad["onde_falha"] = ["nenhum"]
    report = validate_explanation(ExplanationPayload.model_validate(bad), concept.rules)
    assert any("onde_falha" in e for e in report.errors)


def test_schema_requires_all_six_steps(good):
    data = good.model_dump()
    del data["onde_falha"]
    with pytest.raises(ValidationError):
        ExplanationPayload.model_validate(data)


@pytest.mark.parametrize(
    "quote,expected",
    [
        ("o remetente faz a retransmissão desse segmento", True),
        ("O remetente faz a retransmissao desse segmento!", True),  # sem acento e pontuação
        ("o remetente envia tudo de uma vez sem janela", False),
    ],
)
def test_quote_matching(concept, quote, expected):
    assert quote_in_source(quote, concept.base_text) is expected


def test_palavras_comuns_nao_contam_como_do_universo(concept, good):
    """Log de 09/11: "direta" e "forma" num mapeamento de Marvel reprovavam."""
    payload = good.model_copy(deep=True)
    payload.mapeamento[0].universo = "Tony Stark fala de forma direta com a armadura"
    payload.reformulacao_tecnica += " A comunicação ocorre de forma direta."
    report = validate_explanation(payload, concept.rules)
    assert not any("termos do universo" in e for e in report.errors)


def test_nome_proprio_do_universo_ainda_e_barrado(concept, good):
    payload = good.model_copy(deep=True)
    payload.mapeamento[0].universo = "Tony Stark envia bolas numeradas"
    payload.reformulacao_tecnica += " Como Stark faria."
    report = validate_explanation(payload, concept.rules)
    assert any("stark" in e for e in report.errors)
