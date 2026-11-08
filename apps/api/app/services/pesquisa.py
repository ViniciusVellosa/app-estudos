"""Pesquisa na web do assunto pedido pelo aluno (decisão D8).

Quando o assunto digitado não está na biblioteca, a IA pesquisa na web
(Grounding with Google Search, da API do Gemini) e escreve um texto de
referência com fontes. Esse texto passa a ser o texto-base do assunto: a
explicação com analogia é gerada a partir dele, a autoverificação (D6) confere
a explicação contra ele, e os validadores exigem que cada correspondência da
analogia cite um trecho literal dele.

Por que pesquisar antes de explicar: sem uma referência externa, a IA
verificaria a si mesma sem nada para comparar, que é o caso em que a
autocorreção falha (Huang et al., 2024). A busca traz essa referência de fora,
com fontes que o aluno pode abrir.

O texto do aluno vai para a IA só como assunto. Nada que identifique o aluno
é enviado, e o assunto é guardado normalizado, sem ligação com quem pediu.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import Settings
from app.content import Concept, load_concepts, slugify
from app.db import Pesquisa
from app.services.assunto import normaliza

log = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "pesquisa_sistema.md"

# Um texto de referência curto demais não sustenta uma analogia de seis partes.
MIN_TEXTO = 300


class PesquisaError(Exception):
    """A pesquisa não pôde ser feita ou não produziu uma referência usável."""


class AssuntoRecusado(PesquisaError):
    """O pedido não é um assunto de estudo."""


@dataclass
class Fonte:
    titulo: str
    url: str


@dataclass
class ResultadoPesquisa:
    titulo: str
    texto: str
    termos: list[str]
    fontes: list[Fonte] = field(default_factory=list)


class Pesquisador(Protocol):
    name: str

    def pesquisar(self, assunto: str) -> ResultadoPesquisa: ...


@lru_cache
def system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def interpreta(resposta: str, fontes: list[Fonte]) -> ResultadoPesquisa:
    """Lê o formato TITULO/TERMOS/TEXTO e confere se a referência é usável."""
    texto = (resposta or "").strip()
    recusa = re.match(r"^RECUSA:\s*(.+)", texto, re.DOTALL)
    if recusa:
        raise AssuntoRecusado(recusa.group(1).strip())

    titulo = re.search(r"^TITULO:\s*(.+)$", texto, re.MULTILINE)
    termos = re.search(r"^TERMOS:\s*(.+)$", texto, re.MULTILINE)
    corpo = re.search(r"^TEXTO:\s*\n?(.*)$", texto, re.MULTILINE | re.DOTALL)
    if not (titulo and corpo):
        raise PesquisaError("a pesquisa voltou fora do formato combinado")

    corpo_txt = corpo.group(1).strip()
    if len(corpo_txt) < MIN_TEXTO:
        raise PesquisaError("a pesquisa voltou com texto curto demais para servir de referência")
    if not fontes:
        # Sem fonte não há referência externa: seria a IA conferindo a si mesma.
        raise PesquisaError("a pesquisa não trouxe nenhuma fonte da web")

    # Só valem termos que estão de fato no texto: os validadores procuram por eles.
    corpo_norm = normaliza(corpo_txt)
    lista = [t.strip() for t in (termos.group(1) if termos else "").split(";")]
    lista = [t for t in lista if t and normaliza(t) and normaliza(t) in corpo_norm][:8]

    return ResultadoPesquisa(titulo.group(1).strip()[:200], corpo_txt, lista, fontes)


class GeminiPesquisador:
    """Pesquisa com a ferramenta google_search da API do Gemini (SDK google-genai)."""

    name = "gemini:google_search"

    def __init__(self, settings: Settings):
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:  # extra "llm" não instalado
            raise PesquisaError("instale o pacote google-genai (uv sync --extra llm)") from exc
        if not settings.llm_api_key:
            raise PesquisaError("defina LLM_API_KEY")
        self.types = types
        self.model = settings.pesquisa_model or settings.llm_model
        if not self.model:
            raise PesquisaError("defina PESQUISA_MODEL ou LLM_MODEL")
        self.client = genai.Client(
            api_key=settings.llm_api_key,
            http_options=types.HttpOptions(timeout=int(settings.llm_timeout_s * 1000)),
        )

    def pesquisar(self, assunto: str) -> ResultadoPesquisa:
        types = self.types
        try:
            resposta = self.client.models.generate_content(
                model=self.model,
                contents=f"Assunto pedido pelo estudante: {assunto}",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt(),
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                ),
            )
        except Exception as exc:  # rede, chave, limite de uso
            codigo = getattr(exc, "code", None) or getattr(exc, "status_code", None)
            # A mensagem do Google diz QUAL limite estourou (por minuto, por
            # dia, ou cota zero no plano). Vai para o log e para o teste
            # rápido; o aluno nunca vê (a rota troca por uma frase simples).
            detalhe = (getattr(exc, "message", None) or str(exc) or "").strip().replace("\n", " ")
            raise PesquisaError(
                f"falha ao pesquisar: {type(exc).__name__}"
                + (f" (HTTP {codigo})" if codigo else "")
                + (f": {detalhe[:400]}" if detalhe else "")
            ) from exc
        return interpreta(resposta.text or "", fontes_de(resposta))


def fontes_de(resposta) -> list[Fonte]:
    """Fontes da busca, sem repetir endereço (groundingMetadata.groundingChunks)."""
    vistas: dict[str, Fonte] = {}
    for candidato in getattr(resposta, "candidates", None) or []:
        meta = getattr(candidato, "grounding_metadata", None)
        for chunk in getattr(meta, "grounding_chunks", None) or []:
            web = getattr(chunk, "web", None)
            url = getattr(web, "uri", None)
            if url and url not in vistas:
                vistas[url] = Fonte(titulo=(getattr(web, "title", None) or url)[:200], url=url)
    return list(vistas.values())[:8]


# ---------------------------------------------------------------- conceitos


def conceito_da_pesquisa(p: Pesquisa) -> Concept:
    return Concept(
        slug=p.slug,
        title=p.titulo,
        discipline="Pesquisado na web",
        base_text=p.texto_base,
        key_terms=list(p.termos or []),
        forbidden_patterns=[],
    )


def obter_conceito(db: Session, slug: str) -> Concept | None:
    """Conteúdo da biblioteca ou, se não houver, um assunto já pesquisado."""
    conceito = load_concepts().get(slug)
    if conceito is not None:
        return conceito
    p = db.scalar(select(Pesquisa).where(Pesquisa.slug == slug))
    return conceito_da_pesquisa(p) if p else None


def fontes_do_conceito(db: Session, slug: str) -> list[Fonte]:
    p = db.scalar(select(Pesquisa).where(Pesquisa.slug == slug))
    return [Fonte(**f) for f in (p.fontes or [])] if p else []


def pesquisar_assunto(db: Session, assunto: str, pesquisador: Pesquisador) -> Pesquisa:
    """Devolve a pesquisa guardada para o assunto, ou pesquisa e guarda."""
    chave = normaliza(assunto)[:200]
    guardada = db.scalar(select(Pesquisa).where(Pesquisa.assunto == chave))
    if guardada:
        return guardada

    r = pesquisador.pesquisar(assunto)
    slug = "web-" + (slugify(r.titulo)[:70] or "assunto")
    existente = db.scalar(select(Pesquisa).where(Pesquisa.slug == slug))
    if existente:
        # outro jeito de pedir o mesmo conceito: reaproveita a mesma referência
        return existente
    p = Pesquisa(
        slug=slug,
        assunto=chave,
        titulo=r.titulo,
        texto_base=r.texto,
        termos=r.termos,
        fontes=[{"titulo": f.titulo, "url": f.url} for f in r.fontes],
        modelo=pesquisador.name,
    )
    db.add(p)
    db.commit()
    log.info("assunto pesquisado: %s (%s fontes)", slug, len(r.fontes))
    return p
