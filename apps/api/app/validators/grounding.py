"""Validadores anti-alucinação das explicações.

Ideia central: a IA não é fonte de verdade técnica. Ela adapta um texto-base
revisado; estes validadores conferem, de forma determinística, sinais de que a
adaptação saiu do texto-base. Não provam que a explicação está certa (isso
exige revisão humana), mas barram erros comuns antes de chegarem ao aluno.

Checagens:
1. trecho_base de cada linha do mapeamento existe no texto-base;
2. a cena respeita o limite de palavras (evita "detalhes sedutores");
3. onde_falha não está vazio (já garantido pelo schema) nem é genérico;
4. a reformulação técnica não usa termos do universo do aluno;
5. a reformulação técnica usa termos-chave do conceito;
6. nenhum trecho bate com armadilhas conhecidas do conceito
   (ex.: descrever o TCP como "pare-e-espere").
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from difflib import SequenceMatcher

from app.schemas import ExplanationPayload

MAX_SCENE_WORDS = 80
QUOTE_MIN_SIMILARITY = 0.85
MIN_KEY_TERMS = 2
GENERIC_LIMITS = {"nenhum", "nao ha", "não há", "n/a", "-", "nada"}


@dataclass
class ConceptRules:
    """Regras de um conceito, lidas do front-matter do texto-base."""

    base_text: str
    key_terms: list[str] = field(default_factory=list)
    forbidden_patterns: list[str] = field(default_factory=list)


@dataclass
class ValidationReport:
    ok: bool
    errors: list[str] = field(default_factory=list)

    def as_feedback(self) -> str:
        """Texto curto para devolver ao modelo numa nova tentativa."""
        return "Corrija os seguintes problemas: " + "; ".join(self.errors)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def quote_in_source(quote: str, source: str) -> bool:
    """O trecho aparece no texto-base (exato ou quase exato)?"""
    q, s = normalize(quote), normalize(source)
    if not q:
        return False
    if q in s:
        return True
    matcher = SequenceMatcher(None, s, q, autojunk=False)
    match = matcher.find_longest_match(0, len(s), 0, len(q))
    if match.size == 0:
        return False
    # compara o trecho com a janela do texto-base em torno do melhor casamento
    start = max(0, match.a - match.b)
    window = s[start : start + len(q)]
    return SequenceMatcher(None, window, q, autojunk=False).ratio() >= QUOTE_MIN_SIMILARITY


# Palavras comuns da língua que aparecem em qualquer texto e não identificam
# universo nenhum. Sem esta lista, "direta" e "forma" num mapeamento de Marvel
# reprovavam uma reformulação técnica correta (log de 09/11/2026).
PALAVRAS_COMUNS = {
    "como", "para", "pela", "pelo", "pelas", "pelos", "sobre", "entre", "cada",
    "todo", "toda", "todos", "todas", "outro", "outra", "outros", "outras",
    "mesmo", "mesma", "quando", "onde", "isso", "esse", "essa", "este", "esta",
    "forma", "modo", "maneira", "parte", "partes", "tipo", "tipos", "vez", "vezes",
    "direta", "direto", "diretamente", "indireta", "indireto", "simples", "unico",
    "unica", "varios", "varias", "muito", "muitos", "pouco", "poucos", "grande",
    "grandes", "pequeno", "pequena", "novo", "nova", "primeiro", "primeira",
    "sempre", "nunca", "ainda", "apenas", "somente", "tambem", "depois", "antes",
    "propria", "proprio", "proprias", "proprios", "possui", "possuem",
    "pode", "podem", "deve", "devem", "fazer", "faz", "fazem", "usar", "usa",
    "usam", "uso", "ter", "tem", "sendo", "estar", "estao", "seus",
    "suas", "dele", "dela", "deles", "delas", "nosso", "nossa", "alguns",
    "algumas", "qualquer", "nenhum", "nenhuma", "sem", "com", "ate",
}


def universe_terms(payload: ExplanationPayload, base_text: str) -> set[str]:
    """Palavras próprias do universo do aluno.

    Uma palavra do lado "universo" do mapeamento só conta como do universo se
    não estiver no texto-base, não for palavra comum da língua e não aparecer
    nas partes técnicas que o próprio modelo escreveu sem analogia (conceito e
    coluna técnica do mapeamento): se ele a usou ali, ela é vocabulário geral.
    """
    neutras = set(normalize(base_text).split())
    neutras |= set(normalize(payload.conceito).split())
    for row in payload.mapeamento:
        neutras |= set(normalize(row.tecnico).split())
    words: set[str] = set()
    for row in payload.mapeamento:
        for w in normalize(row.universo).split():
            if len(w) >= 4 and w not in neutras and w not in PALAVRAS_COMUNS:
                words.add(w)
    return words


def validate_explanation(payload: ExplanationPayload, rules: ConceptRules) -> ValidationReport:
    errors: list[str] = []

    for i, row in enumerate(payload.mapeamento, start=1):
        if not quote_in_source(row.trecho_base, rules.base_text):
            errors.append(
                f"mapeamento linha {i}: trecho_base não encontrado no texto-base "
                f"({row.trecho_base[:60]!r})"
            )

    scene_words = len(payload.cena.split())
    if scene_words > MAX_SCENE_WORDS:
        errors.append(f"cena com {scene_words} palavras (máximo {MAX_SCENE_WORDS})")

    limits = [normalize(x) for x in payload.onde_falha]
    if all(len(x) < 10 or x in GENERIC_LIMITS for x in limits):
        errors.append("onde_falha precisa citar ao menos um limite concreto da analogia")

    reform = normalize(payload.reformulacao_tecnica)
    reform_words = set(reform.split())
    leaked = sorted(universe_terms(payload, rules.base_text) & reform_words)
    if leaked:
        errors.append(f"reformulacao_tecnica usa termos do universo: {', '.join(leaked)}")

    if rules.key_terms:
        present = [t for t in rules.key_terms if normalize(t) in reform]
        needed = min(MIN_KEY_TERMS, len(rules.key_terms))
        if len(present) < needed:
            errors.append(
                "reformulacao_tecnica não usa os termos-chave do conceito "
                f"(esperado ao menos {needed} de: {', '.join(rules.key_terms)})"
            )

    full_text = " ".join(
        [payload.conceito, payload.cena, payload.reformulacao_tecnica]
        + [f"{r.universo} {r.tecnico}" for r in payload.mapeamento]
    )
    norm_full = normalize(full_text)
    for pattern in rules.forbidden_patterns:
        if re.search(pattern, norm_full):
            errors.append(f"contradiz o texto-base (armadilha conhecida: /{pattern}/)")

    return ValidationReport(ok=not errors, errors=errors)
