import logging

from fastapi import APIRouter, HTTPException, Request, Response, status
from sqlalchemy import select

from app.config import get_settings
from app.content import load_concepts
from app.db import Explanation, Feedback, Interest
from app.schemas import (
    AssuntoIn,
    AssuntoOut,
    ConceptOut,
    ExplanationOut,
    ExplanationRequest,
    FeedbackIn,
    FonteOut,
    NeutralOut,
    QuestionIn,
    QuestionOut,
)
from app.security import ConsentedUser, CurrentUser, DbDep
from app.services.assunto import reconhece
from app.services.explanations import get_explanation, universe_terms_for
from app.services.pesquisa import (
    AssuntoRecusado,
    PesquisaError,
    fontes_do_conceito,
    obter_conceito,
    pesquisar_assunto,
)
from app.services.questions import answer_question

log = logging.getLogger(__name__)

router = APIRouter(prefix="/v1", tags=["conteúdo"])


@router.get("/concepts", response_model=list[ConceptOut])
def list_concepts():
    return [
        ConceptOut(slug=c.slug, title=c.title, discipline=c.discipline)
        for c in load_concepts().values()
    ]


def _concept_out(c) -> ConceptOut:
    return ConceptOut(slug=c.slug, title=c.title, discipline=c.discipline)


@router.post("/assuntos/reconhecer", response_model=AssuntoOut)
def recognize_subject(body: AssuntoIn, request: Request, user: ConsentedUser, db: DbDep):
    """O aluno digita o assunto no chat (D7).

    1. Se o assunto está na biblioteca, usa o conteúdo revisado.
    2. Senão, e com a pesquisa ativa, a IA pesquisa na web e monta um texto de
       referência com fontes (D8). A pesquisa fica guardada para reuso.
    3. Sem pesquisa, diz que ainda não há material e sugere o que existe.

    O texto do aluno não é guardado como foi escrito, nem ligado a quem pediu.
    """
    r = reconhece(body.texto)
    sugestoes = [_concept_out(c) for c in r.sugestoes]
    if r.conceito is not None:
        return AssuntoOut(encontrado=True, conceito=_concept_out(r.conceito), sugestoes=sugestoes)

    pesquisador = getattr(request.app.state, "pesquisador", None)
    if pesquisador is None:
        return AssuntoOut(encontrado=False, conceito=None, sugestoes=sugestoes)
    try:
        p = pesquisar_assunto(db, body.texto, pesquisador)
    except AssuntoRecusado as exc:
        return AssuntoOut(encontrado=False, conceito=None, sugestoes=sugestoes, motivo=str(exc))
    except PesquisaError as exc:
        log.warning("pesquisa falhou: %s", exc)
        return AssuntoOut(
            encontrado=False,
            conceito=None,
            sugestoes=sugestoes,
            motivo="Não consegui pesquisar esse assunto agora. Tente de novo em instantes.",
        )
    return AssuntoOut(
        encontrado=True,
        conceito=ConceptOut(slug=p.slug, title=p.titulo, discipline="Pesquisado na web"),
        sugestoes=sugestoes,
        pesquisado=True,
        fontes=[FonteOut(**f) for f in p.fontes],
    )


@router.get("/concepts/{slug}/fontes", response_model=list[FonteOut])
def concept_sources(slug: str, db: DbDep):
    return [FonteOut(titulo=f.titulo, url=f.url) for f in fontes_do_conceito(db, slug)]


@router.get("/concepts/{slug}/neutral", response_model=NeutralOut)
def neutral_explanation(slug: str, db: DbDep):
    concept = obter_conceito(db, slug)
    if concept is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conteúdo não encontrado.")
    return NeutralOut(slug=concept.slug, title=concept.title, base_text=concept.base_text)


@router.post("/explanations", response_model=ExplanationOut)
def request_explanation(
    body: ExplanationRequest,
    request: Request,
    user: ConsentedUser,
    db: DbDep,
):
    concept = obter_conceito(db, body.concept_slug)
    if concept is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conteúdo não encontrado.")
    interest = db.scalar(
        select(Interest).where(Interest.id == body.interest_id, Interest.user_id == user.id)
    )
    if interest is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Interesse não encontrado.")
    generator = request.app.state.generator  # None quando o provedor é "curated"
    return get_explanation(
        db,
        concept,
        interest.label,
        interest.depth,
        body.level,
        generator,
        get_settings(),
        verifier=request.app.state.verifier,
    )


@router.post("/concepts/{slug}/questions", response_model=QuestionOut)
def ask_question(
    slug: str,
    body: QuestionIn,
    request: Request,
    user: ConsentedUser,
    db: DbDep,
):
    """Pergunta livre, resposta só dentro do conceito (RF11, decisão D5).

    A pergunta não é gravada. Quem decide se ela é do assunto é um porteiro
    determinístico, antes de qualquer chamada de IA.
    """
    concept = obter_conceito(db, slug)
    if concept is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conteúdo não encontrado.")

    universo: list[str] = []
    if body.interest_id is not None:
        interest = db.scalar(
            select(Interest).where(
                Interest.id == body.interest_id, Interest.user_id == user.id
            )
        )
        if interest is not None:
            universo = universe_terms_for(db, concept.slug, interest.label)

    # O gerador de IA também é o chat da resposta; sem ele, resposta extrativa.
    answer = answer_question(
        body.pergunta,
        concept,
        universo=universo,
        chat=request.app.state.generator,
        verifier=request.app.state.verifier,
    )
    return QuestionOut(
        status=answer.status,
        resposta=answer.texto,
        trechos=answer.trechos,
        concept_title=concept.title,
    )


@router.post("/explanations/{explanation_id}/feedback", status_code=204)
def send_feedback(
    explanation_id: int,
    body: FeedbackIn,
    user: CurrentUser,
    db: DbDep,
):
    explanation = db.get(Explanation, explanation_id)
    if explanation is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Explicação não encontrada.")
    db.add(Feedback(explanation_id=explanation.id, user_id=user.id, kind=body.kind, comment=body.comment))
    if body.kind == "errada" and explanation.provider != "curated":
        # Conteúdo gerado por IA sai de circulação na hora: na dúvida, o aluno
        # seguinte vê a explicação padrão (RNF03, ADR 0003).
        #
        # Conteúdo curado, não: foi escrito e revisado por pessoa, e um clique
        # anônimo não pode derrubá-lo — qualquer participante do teste de
        # usabilidade tiraria do ar o material dos próximos. A avaliação fica
        # registrada e aparece em `python -m app.review`, que é onde alguém
        # decide.
        explanation.status = "under_review"
    db.commit()
    return Response(status_code=204)
