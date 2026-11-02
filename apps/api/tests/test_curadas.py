"""Toda explicação escrita à mão precisa passar nos mesmos validadores da IA.

Sem este teste, uma explicação curada reprovada só gera um aviso no log ao
subir a API e some para o aluno sem ninguém perceber.
"""
import json
from pathlib import Path

import pytest

from app.config import get_settings
from app.content import load_concepts, load_curated
from app.validators.grounding import validate_explanation

ROOT = Path(get_settings().content_dir) / "explanations"
CURADAS = sorted(ROOT.glob("*/*.json"))


@pytest.mark.parametrize("path", CURADAS, ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_curada_passa_nos_validadores(path):
    concept = load_concepts().get(path.parent.name)
    assert concept, f"pasta {path.parent.name} não corresponde a nenhum conceito em content/concepts"
    meta = json.loads(path.read_text(encoding="utf-8")).get("_meta", {})
    payload = load_curated(concept.slug, meta.get("interest_label", path.stem))
    assert payload is not None
    report = validate_explanation(payload, concept.rules)
    assert report.ok, report.errors


def test_existe_ao_menos_uma_curada():
    assert CURADAS, "crie ao menos uma explicação escrita à mão para o teste de usabilidade"
