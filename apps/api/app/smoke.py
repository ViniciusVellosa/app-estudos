"""Teste de fumaça da IA: uma chamada de verdade, para conferir a configuração.

    uv run python -m app.smoke
    uv run python -m app.smoke tcp-entrega-confiavel "one piece"
    uv run python -m app.smoke --pesquisa "árvore B" "one piece"

Em Docker: docker compose exec api python -m app.smoke

Gera uma explicação, roda a autoverificação (ADR 0003) e os validadores, e
diz onde parou. Serve para responder "a chave e o modelo estão certos?" sem
abrir o navegador e sem gastar uma sessão de teste descobrindo que não.

Não imprime a chave nem nenhuma parte dela.
"""
from __future__ import annotations

import sys

from app.config import get_settings
from app.content import load_concepts
from app.providers.base import ExplanationRequestData, GenerationError
from app.schemas import Refusal
from app.services.explanations import generate_validated
from app.services.verification import LlmSelfVerifier


def pesquisa(argv: list[str]) -> int:
    """Pesquisa um assunto na web (D8) e, se der certo, gera a explicação."""
    from app.services.pesquisa import Concept, GeminiPesquisador, PesquisaError

    settings = get_settings()
    assunto = argv[0] if argv else "árvore B"
    interesse = argv[1] if len(argv) > 1 else "futebol"
    print(f"pesquisa ............ {settings.pesquisa_provider or '(DESLIGADA: defina PESQUISA_PROVIDER=gemini)'}")
    print(f"modelo .............. {settings.pesquisa_model or settings.llm_model or '(VAZIO)'}")
    print(f"chave ............... {'definida' if settings.llm_api_key else 'VAZIA'}")
    try:
        r = GeminiPesquisador(settings).pesquisar(assunto)
    except PesquisaError as exc:
        print(f"\nERRO na pesquisa: {exc}")
        return 1
    print(f"\ntítulo: {r.titulo}\ntermos: {', '.join(r.termos)}\nfontes:")
    for f in r.fontes:
        print(f"  - {f.titulo}: {f.url}")
    print(f"\n{r.texto}\n")
    conceito = Concept(slug="web-teste", title=r.titulo, discipline="", base_text=r.texto, key_terms=r.termos)
    return explica(settings, conceito, interesse)


def main(argv: list[str]) -> int:
    if argv[:1] == ["--pesquisa"]:
        return pesquisa(argv[1:])
    settings = get_settings()
    slug = argv[0] if argv else "tcp-entrega-confiavel"
    interesse = argv[1] if len(argv) > 1 else "futebol"

    print(f"provedor ............ {settings.explanation_provider}")
    print(f"backend ............. {settings.llm_backend}")
    print(f"modelo .............. {settings.llm_model or '(VAZIO)'}")
    print(f"base_url ............ {settings.llm_base_url or '(padrão do SDK)'}")
    print(f"chave ............... {'definida' if settings.llm_api_key else 'VAZIA'}")
    print()

    if settings.explanation_provider != "llm":
        print("EXPLANATION_PROVIDER não é 'llm': nada a testar.")
        print("Para ligar a IA, ajuste o .env. O app funciona sem ela (modo curated).")
        return 1
    if not settings.llm_model:
        print("ERRO: LLM_MODEL está vazio.")
        return 1
    if not settings.llm_api_key and settings.llm_backend == "openai_compatible":
        print("AVISO: LLM_API_KEY vazia. Só funciona em servidor local (Ollama).")

    concept = load_concepts().get(slug)
    if concept is None:
        print(f"ERRO: conceito '{slug}' não existe em content/concepts/.")
        return 1
    return explica(settings, concept, interesse)


def explica(settings, concept, interesse: str) -> int:
    from app.providers.llm import build_llm_generator

    try:
        generator = build_llm_generator(settings)
    except GenerationError as exc:
        print(f"ERRO ao montar o provedor: {exc}")
        return 1

    print(f"pedindo '{concept.title}' com o universo '{interesse}'…")
    dados = ExplanationRequestData(concept, interesse, 2, "iniciante")
    resultado, erros = generate_validated(generator, dados, LlmSelfVerifier(generator))

    if isinstance(resultado, Refusal):
        print(f"\nO modelo RECUSOU, o que é um resultado válido: {resultado.motivo}")
        return 0
    if resultado is None:
        print("\nREPROVADA nas duas tentativas. O aluno veria a explicação padrão.")
        for erro in erros:
            print(f"  - {erro}")
        return 2

    print("\nAPROVADA na autoverificação e nos validadores.\n")
    print(f"  conceito: {resultado.conceito}")
    print(f"  cena:     {resultado.cena}")
    print("  mapeamento:")
    for linha in resultado.mapeamento:
        print(f"    - {linha.universo} = {linha.tecnico}")
    print("  onde falha:")
    for item in resultado.onde_falha:
        print(f"    - {item}")
    print(f"  técnica:  {resultado.reformulacao_tecnica}")
    if erros:
        print("\n(houve uma tentativa reprovada antes desta:)")
        for erro in erros:
            print(f"  - {erro}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
