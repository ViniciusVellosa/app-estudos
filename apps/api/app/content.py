"""Leitura do conteúdo revisado (textos-base e explicações curadas).

O conteúdo fica em arquivos versionados no Git (pasta content/), e não no
banco, para que a revisão técnica aconteça por pull request: quem revisa vê
exatamente o que mudou no texto-base.
"""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml

from app.config import get_settings
from app.schemas import ExplanationPayload
from app.validators.grounding import ConceptRules

FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


@dataclass
class Concept:
    slug: str
    title: str
    discipline: str
    base_text: str
    key_terms: list[str] = field(default_factory=list)
    forbidden_patterns: list[str] = field(default_factory=list)

    @property
    def rules(self) -> ConceptRules:
        return ConceptRules(self.base_text, self.key_terms, self.forbidden_patterns)


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


@lru_cache
def load_concepts() -> dict[str, Concept]:
    root = Path(get_settings().content_dir) / "concepts"
    concepts: dict[str, Concept] = {}
    for path in sorted(root.glob("*.md")):
        match = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
        if not match:
            raise ValueError(f"{path} sem front-matter YAML")
        meta = yaml.safe_load(match.group(1))
        concept = Concept(
            slug=meta["slug"],
            title=meta["title"],
            discipline=meta.get("discipline", ""),
            base_text=match.group(2).strip(),
            key_terms=meta.get("key_terms", []),
            forbidden_patterns=meta.get("forbidden_patterns", []),
        )
        concepts[concept.slug] = concept
    return concepts


def load_curated(concept_slug: str, interest_label: str) -> ExplanationPayload | None:
    """Explicação escrita à mão (Mágico de Oz) para o par conceito/interesse."""
    path = (
        Path(get_settings().content_dir)
        / "explanations"
        / concept_slug
        / f"{slugify(interest_label)}.json"
    )
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    data.pop("_meta", None)
    return ExplanationPayload.model_validate(data)
