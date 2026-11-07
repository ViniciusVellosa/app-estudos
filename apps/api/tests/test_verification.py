"""Autoverificação da IA (decisão D6, ADR 0003), sem rede.

Dois grupos de teste:

1. **Unidade** — o verificador em si: o veredito, o teto de perguntas, o
   comportamento quando a IA falha e, o mais importante, a garantia de que a
   etapa de checagem **não recebe o rascunho**. Essa é a propriedade que faz o
   método valer: perguntado com o rascunho à vista, o modelo concorda consigo
   mesmo.
2. **Integração** — os três caminhos que o ADR 0003 promete ao aluno:
   aprovada, reprovada uma vez (passa na segunda) e reprovada duas vezes
   (explicação padrão com aviso). Nenhum deles pode exibir conteúdo reprovado.
"""
import pytest

from app.content import load_concepts, load_curated
from app.db import SessionLocal
from app.providers.base import GenerationError
from app.services.explanations import (
    NOTICE_AI_VERIFIED,
    NOTICE_NOT_VERIFIED,
    get_explanation,
)
from app.services.verification import (
    CheckAnswer,
    CheckQuestions,
    LlmSelfVerifier,
    NullVerifier,
    VerdictOut,
    draft_text,
)

SLUG = "tcp-entrega-confiavel"
# Frase que só existe no rascunho: é o rastro que procuramos nas mensagens.
MARCA_DO_RASCUNHO = "zagueiro canhoto do time reserva"


@pytest.fixture
def conceito():
    return load_concepts()[SLUG]


@pytest.fixture
def boa():
    return load_curated(SLUG, "futebol")


class FakeChat:
    """Chat falso. Responde pelo TIPO pedido, não pela ordem das chamadas.

    Assim o teste do teto de perguntas não precisa adivinhar quantas chamadas
    vão acontecer: é justamente isso que ele está medindo.
    """

    name = "fake"

    def __init__(self, perguntas, veredito, resposta="sim, o texto-base diz isso", erro=None):
        self.perguntas = perguntas
        self.veredito = veredito
        self.resposta = resposta
        self.erro = erro
        self.mensagens: list[str] = []

    def ask(self, system, user, output_model):
        self.mensagens.append(user)
        if self.erro is not None:
            raise self.erro
        if output_model is CheckQuestions:
            return CheckQuestions(perguntas=self.perguntas)
        if output_model is CheckAnswer:
            return CheckAnswer(resposta=self.resposta)
        return self.veredito


def chat_que_aprova(n_perguntas=2):
    return FakeChat(
        perguntas=[f"pergunta {i}" for i in range(n_perguntas)],
        veredito=VerdictOut(aprovada=True),
    )


# --------------------------------------------------------------- unidade

def test_aprova_quando_o_veredito_e_positivo(conceito):
    verificador = LlmSelfVerifier(chat_que_aprova())
    assert verificador.verify("um rascunho qualquer", conceito).aprovada is True


def test_reprova_e_devolve_os_motivos(conceito):
    chat = FakeChat(
        perguntas=["o remetente espera cada confirmação?"],
        resposta="não; vários segmentos ficam em trânsito, até o limite da janela",
        veredito=VerdictOut(aprovada=False, motivos=["a cena descreve pare-e-espere, não a janela"]),
    )
    veredito = LlmSelfVerifier(chat).verify("rascunho errado", conceito)
    assert veredito.aprovada is False
    assert "pare-e-espere" in veredito.motivos[0]
    # os motivos viram instrução de correção para a próxima tentativa
    assert "pare-e-espere" in veredito.as_feedback()


def test_reprovada_sem_motivo_ainda_traz_uma_justificativa(conceito):
    """Reprovar calado não ajuda a nova tentativa a acertar."""
    chat = FakeChat(perguntas=["p"], veredito=VerdictOut(aprovada=False, motivos=[]))
    veredito = LlmSelfVerifier(chat).verify("rascunho", conceito)
    assert veredito.aprovada is False
    assert veredito.motivos


def test_a_etapa_de_checagem_nao_ve_o_rascunho(conceito, boa):
    """O coração do método: a resposta independente não pode ver o rascunho.

    Se visse, o modelo repetiria o próprio erro ao confirmar a si mesmo
    (Chain-of-Verification, Dhuliawala et al., 2024).
    """
    rascunho = draft_text(boa.model_copy(update={"cena": f"O {MARCA_DO_RASCUNHO} recebe a bola."}))
    chat = chat_que_aprova(n_perguntas=2)
    LlmSelfVerifier(chat).verify(rascunho, conceito)

    etapa_perguntas, *etapas_resposta, etapa_veredito = chat.mensagens
    assert "<etapa>perguntas</etapa>" in etapa_perguntas
    assert MARCA_DO_RASCUNHO in etapa_perguntas  # aqui o rascunho é o insumo

    for msg in etapas_resposta:
        assert "<etapa>resposta</etapa>" in msg
        assert MARCA_DO_RASCUNHO not in msg, "a checagem independente recebeu o rascunho"
        assert "<rascunho>" not in msg
        assert conceito.base_text[:40] in msg  # mas recebe a fonte técnica fixa

    assert "<etapa>veredito</etapa>" in etapa_veredito
    assert MARCA_DO_RASCUNHO in etapa_veredito  # no veredito ele volta, para comparação


def test_limita_o_numero_de_perguntas_de_checagem(conceito):
    """Teto de chamadas: 1 (perguntas) + 3 (respostas) + 1 (veredito)."""
    chat = FakeChat(
        perguntas=[f"p{i}" for i in range(6)], veredito=VerdictOut(aprovada=True)
    )
    LlmSelfVerifier(chat, max_perguntas=3).verify("rascunho", conceito)
    assert len(chat.mensagens) == 5


def test_falha_da_ia_na_verificacao_reprova(conceito):
    """Falha fechada: sem conseguir verificar, não se exibe (RNF04)."""
    chat = FakeChat(
        perguntas=["p"], veredito=VerdictOut(aprovada=True),
        erro=GenerationError("tempo esgotado"),
    )
    veredito = LlmSelfVerifier(chat).verify("rascunho", conceito)
    assert veredito.aprovada is False
    assert "não foi possível verificar" in veredito.motivos[0]


def test_modo_curado_nao_gasta_chamada_de_ia(conceito):
    assert NullVerifier().verify("qualquer coisa", conceito).aprovada is True


# ------------------------------------------------------------ integração

class FakeGenerator:
    """Gera o que lhe mandarem, na ordem, e conta as tentativas."""

    name = "fake"

    def __init__(self, resultados):
        self.resultados = list(resultados)
        self.calls = 0
        self.feedbacks: list[str | None] = []

    def generate(self, req):
        self.calls += 1
        self.feedbacks.append(req.feedback)
        return self.resultados.pop(0)


class FakeVerifier:
    """Reprova as primeiras `reprovar` vezes e aprova daí em diante."""

    name = "fake"

    def __init__(self, reprovar=0):
        self.reprovar = reprovar
        self.calls = 0

    def verify(self, rascunho, concept):
        from app.services.verification import Verdict

        self.calls += 1
        if self.calls <= self.reprovar:
            return Verdict(False, ["a cena contradiz o texto-base"])
        return Verdict(True)


def pedir(conceito, gerador, verificador, interesse):
    with SessionLocal() as db:
        return get_explanation(db, conceito, interesse, 2, "iniciante", gerador, verifier=verificador)


def test_aprovada_na_primeira_tentativa_e_exibida_com_aviso(client, conceito, boa):
    gerador, verificador = FakeGenerator([boa]), FakeVerifier(reprovar=0)
    saida = pedir(conceito, gerador, verificador, "basquete")

    assert gerador.calls == 1
    assert verificador.calls == 1
    assert saida.personalized is True
    assert saida.status == "verified"
    assert saida.notice == NOTICE_AI_VERIFIED  # o aluno sabe que não houve professor


def test_reprovada_uma_vez_passa_na_segunda_tentativa(client, conceito, boa):
    gerador, verificador = FakeGenerator([boa, boa]), FakeVerifier(reprovar=1)
    saida = pedir(conceito, gerador, verificador, "volei")

    assert gerador.calls == 2
    assert saida.personalized is True
    assert saida.status == "verified"
    # a segunda tentativa recebeu os motivos da reprovação
    assert gerador.feedbacks[0] is None
    assert "contradiz o texto-base" in gerador.feedbacks[1]


def test_reprovada_duas_vezes_mostra_a_explicacao_padrao(client, conceito, boa):
    gerador, verificador = FakeGenerator([boa, boa]), FakeVerifier(reprovar=2)
    saida = pedir(conceito, gerador, verificador, "xadrez")

    assert gerador.calls == 2
    assert verificador.calls == 2
    assert saida.personalized is False
    assert saida.payload is None, "rascunho reprovado não pode chegar ao aluno"
    assert saida.neutral_text  # o texto-base revisado toma o lugar
    assert saida.notice == NOTICE_NOT_VERIFIED


def test_reprovada_duas_vezes_nao_fica_no_banco(client, conceito, boa):
    """Nada reprovado é guardado: o próximo aluno não pode receber do cache."""
    from sqlalchemy import select

    from app.db import Explanation

    pedir(conceito, FakeGenerator([boa, boa]), FakeVerifier(reprovar=2), "sinuca")
    with SessionLocal() as db:
        linhas = db.scalars(
            select(Explanation).where(Explanation.interest_label == "sinuca")
        ).all()
    assert linhas == []


def test_a_verificacao_roda_antes_dos_validadores(client, conceito, boa):
    """Ordem do ADR 0003: autoverificação primeiro, validadores depois.

    O rascunho aqui é reprovado pelos validadores (descreve pare-e-espere).
    Se a ordem estivesse trocada, o verificador nem seria chamado.
    """
    ruim = boa.model_copy(
        update={"cena": "O treinador só manda o próximo depois de confirmar que o anterior chegou."}
    )
    gerador, verificador = FakeGenerator([ruim, ruim]), FakeVerifier(reprovar=0)
    saida = pedir(conceito, gerador, verificador, "futsal")

    assert verificador.calls == 2, "o verificador deve ser consultado nas duas tentativas"
    assert saida.personalized is False
