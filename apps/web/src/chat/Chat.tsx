import { useEffect, useRef, useState } from "react";
import { api, type Concept, type Explanation, type Fonte, type Interest } from "../api";
import { ParteMensagem } from "./ParteMensagem";
import {
  parteAoTrocarDeUniverso,
  posicaoDaParte,
  temVersaoTecnica,
  tituloDaParte,
  totalDePartes,
} from "./partes";

/**
 * A conversa, no modelo dos chats de IA (RF10, decisões D3 e D7).
 *
 * Tudo acontece dentro do chat: o app pergunta o assunto, o aluno escreve com
 * as próprias palavras; o app pergunta o universo, o aluno escreve; a
 * explicação chega em mensagens curtas, uma parte por vez.
 *
 * O campo de digitação muda de papel conforme a conversa (`modo`):
 * - "assunto": o texto vira o conteúdo a estudar (reconhecido na biblioteca);
 * - "universo": o texto vira o universo da comparação;
 * - "pergunta": o texto vira uma pergunta sobre o conteúdo (RF11).
 *
 * Regras de acessibilidade que mandam no desenho:
 * - histórico em `role="log"`, `aria-live="polite"`, `aria-relevant="additions"`:
 *   anuncia a mensagem que chegou pronta (WCAG 4.1.3);
 * - mensagem do app que chega não rola a tela nem rouba o foco (DD10). Só o
 *   gesto do próprio aluno (enviar, tocar numa sugestão) leva o foco ao campo;
 * - as ações ficam numa barra fixa acima do campo, sempre no mesmo lugar: o
 *   botão "Continuar" não some debaixo do dedo nem do foco a cada parte.
 */

type Sugestao = { rotulo: string; texto: string };

type Mensagem =
  | { id: number; papel: "app"; tipo: "texto"; texto: string; fontes?: Fonte[] }
  | { id: number; papel: "app"; tipo: "parte"; parte: number; explicacao: Explanation; tecnica: boolean }
  | { id: number; papel: "app"; tipo: "aviso" | "esperando"; texto: string }
  | { id: number; papel: "app"; tipo: "recusa"; texto: string }
  | { id: number; papel: "app"; tipo: "resposta"; texto: string }
  | { id: number; papel: "aluno"; tipo: "texto"; texto: string };

type Modo = "assunto" | "universo" | "pergunta";

let proximoId = 0;
const novoId = () => ++proximoId;

const PLACEHOLDER: Record<Modo, string> = {
  assunto: "O que você quer entender? Ex.: TCP",
  universo: "Um jogo, série, esporte, anime…",
  pergunta: "Pergunte sobre este conteúdo",
};

const ROTULO_CAMPO: Record<Modo, string> = {
  assunto: "Assunto que você quer entender",
  universo: "Universo para a comparação",
  pergunta: "Sua pergunta sobre este conteúdo",
};

const mesmoNome = (a: string, b: string) =>
  a.trim().toLocaleLowerCase("pt-BR") === b.trim().toLocaleLowerCase("pt-BR");

export function Chat({
  concepts,
  interests,
  onInteresses,
  setStatus,
  setError,
}: {
  concepts: Concept[];
  interests: Interest[];
  onInteresses: (lista: Interest[]) => void;
  setStatus: (s: string) => void;
  setError: (s: string) => void;
}) {
  const [modo, setModo] = useState<Modo>("assunto");
  const [conceito, setConceito] = useState<Concept | null>(null);
  const [interesse, setInteresse] = useState<Interest | null>(null);
  const [explicacao, setExplicacao] = useState<Explanation | null>(null);
  const [parteAtual, setParteAtual] = useState(0);
  // H7 / persona Caio (avaliação heurística, P06): quem escolhe a versão
  // técnica continua nela nas partes seguintes, em vez de clicar de novo a
  // cada parte. Volta à comparação com o mesmo botão.
  const [modoTecnico, setModoTecnico] = useState(false);
  const [mensagens, setMensagens] = useState<Mensagem[]>(() => [boasVindas()]);
  const [sugestoes, setSugestoes] = useState<Sugestao[]>(() => sugestoesDeAssunto(concepts));
  const [texto, setTexto] = useState("");
  const [ocupado, setOcupado] = useState(false);
  const [avaliados, setAvaliados] = useState<number[]>([]);
  const campoRef = useRef<HTMLTextAreaElement>(null);
  const ultimaRef = useRef<HTMLLIElement>(null);
  const alunoRef = useRef<HTMLLIElement>(null);
  const rolarParaAluno = useRef(false);

  // As sugestões iniciais dependem da lista de conteúdos, que chega depois.
  useEffect(() => {
    if (modo === "assunto" && !conceito) setSugestoes(sugestoesDeAssunto(concepts));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [concepts]);

  // Só rola quando quem agiu foi o aluno: a mensagem dele aparece acima do
  // campo. Mensagem do app chegando nunca move a tela (DD10).
  useEffect(() => {
    if (rolarParaAluno.current) {
      rolarParaAluno.current = false;
      // "start": a fala do aluno sobe para o alto da tela e a resposta, quando
      // chegar, aparece logo abaixo dela, sem a tela se mexer de novo.
      alunoRef.current?.scrollIntoView({ block: "start" });
    }
  }, [mensagens]);

  const total = explicacao ? totalDePartes(explicacao) : 0;
  const terminou = explicacao !== null && parteAtual >= total;
  const ultimaParte = [...mensagens].reverse().find((m) => m.tipo === "parte") as
    | Extract<Mensagem, { tipo: "parte" }>
    | undefined;

  const acrescenta = (...novas: Mensagem[]) => setMensagens((m) => [...m, ...novas]);
  const tira = (id: number) => setMensagens((m) => m.filter((x) => x.id !== id));

  function esperando(textoEspera: string): Mensagem {
    const msg: Mensagem = { id: novoId(), papel: "app", tipo: "esperando", texto: textoEspera };
    acrescenta(msg);
    return msg;
  }

  function falaDoAluno(t: string) {
    rolarParaAluno.current = true;
    acrescenta({ id: novoId(), papel: "aluno", tipo: "texto", texto: t });
  }

  // ------------------------------------------------------------ assunto

  async function escolherAssunto(t: string) {
    falaDoAluno(t);
    setSugestoes([]);
    setOcupado(true);
    // Pode ser uma pesquisa na web (D8), que leva alguns segundos
    const espera = esperando("Procurando e pesquisando esse assunto");
    try {
      const r = await api.reconhecerAssunto(t);
      tira(espera.id);
      if (r.encontrado && r.conceito) {
        setConceito(r.conceito);
        if (r.pesquisado && r.fontes.length > 0) {
          acrescenta({
            id: novoId(),
            papel: "app",
            tipo: "texto",
            texto: `Pesquisei sobre ${r.conceito.title} na web. Vou usar estas fontes como referência e conferir a explicação com elas:`,
            fontes: r.fontes,
          });
        } else if (r.pesquisado) {
          // D9: sem busca na web, a referência é escrita pela própria IA. O
          // aluno precisa saber disso para dar à explicação o peso certo.
          acrescenta({
            id: novoId(),
            papel: "app",
            tipo: "aviso",
            texto:
              `Não tenho material revisado sobre ${r.conceito.title}, então a explicação vai se basear ` +
              "no conhecimento da própria IA, sem fontes da web. Eu confiro antes de mostrar, " +
              "mas vale comparar com o material da sua disciplina.",
          });
        }
        perguntarUniverso(
          `Combinado, vamos estudar ${r.conceito.title}. ` +
            "Agora me diga um universo que você conhece bem: um jogo, uma série, um esporte, um anime… " +
            "Vou começar explicando com uma comparação com ele.",
        );
      } else {
        const temSugestoes = r.sugestoes.length > 0;
        acrescenta({
          id: novoId(),
          papel: "app",
          tipo: "texto",
          texto: r.motivo
            ? `${r.motivo}${temSugestoes ? " Se quiser, posso explicar:" : ""}`
            : `Ainda não tenho material de referência sobre “${t}”, então prefiro não arriscar ` +
              "uma explicação que pode estar errada. Por enquanto, consigo explicar:",
        });
        setSugestoes(r.sugestoes.map((c) => ({ rotulo: c.title, texto: c.title })));
        setStatus("Não deu para usar esse assunto. Veja a mensagem.");
      }
    } catch (err) {
      tira(espera.id);
      setError(err instanceof Error ? err.message : "Não foi possível procurar o conteúdo.");
      setSugestoes(sugestoesDeAssunto(concepts));
    } finally {
      setOcupado(false);
    }
  }

  // ------------------------------------------------------------ universo

  function perguntarUniverso(fala: string) {
    acrescenta({ id: novoId(), papel: "app", tipo: "texto", texto: fala });
    setModo("universo");
    setSugestoes(interests.map((i) => ({ rotulo: i.label, texto: i.label })));
  }

  async function escolherUniverso(t: string) {
    falaDoAluno(t);
    setSugestoes([]);
    setOcupado(true);
    try {
      let escolhido = interests.find((i) => mesmoNome(i.label, t)) ?? null;
      if (!escolhido) {
        escolhido = await api.addInterest(t, 2);
        onInteresses([...interests, escolhido]);
      }
      const anterior = interesse;
      setInteresse(escolhido);
      setModo("pergunta");
      if (explicacao && anterior && conceito) {
        await trocarUniverso(conceito, escolhido);
      } else if (conceito) {
        await comecarExplicacao(conceito, escolhido);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Não foi possível usar esse universo.");
      setSugestoes(interests.map((i) => ({ rotulo: i.label, texto: i.label })));
    } finally {
      setOcupado(false);
    }
  }

  function mensagensDaExplicacao(e: Explanation, parte: number): Mensagem[] {
    const msgs: Mensagem[] = [];
    if (e.notice) msgs.push({ id: novoId(), papel: "app", tipo: "aviso", texto: e.notice });
    msgs.push({ id: novoId(), papel: "app", tipo: "parte", parte, explicacao: e, tecnica: modoTecnico && temVersaoTecnica(e, parte) });
    return msgs;
  }

  async function comecarExplicacao(c: Concept, i: Interest) {
    // DD22: a autoverificação são várias chamadas ao modelo; a espera é uma
    // mensagem na conversa, e não uma tela travada.
    const espera = esperando("Preparando e conferindo a explicação");
    setStatus("Preparando a explicação…");
    try {
      const resultado = await api.explain(c.slug, i.id);
      setExplicacao(resultado);
      setParteAtual(1);
      setMensagens((m) => [...m.filter((x) => x.id !== espera.id), ...mensagensDaExplicacao(resultado, 1)]);
      setStatus(resultado.personalized ? "Explicação pronta." : "Explicação padrão pronta.");
    } catch (err) {
      tira(espera.id);
      setStatus("");
      setError(err instanceof Error ? err.message : "Não foi possível gerar a explicação.");
    }
  }

  async function trocarUniverso(c: Concept, i: Interest) {
    const espera = esperando(`Trocando para ${i.label}`);
    try {
      const resultado = await api.explain(c.slug, i.id);
      const parte = parteAoTrocarDeUniverso(resultado, parteAtual);
      setExplicacao(resultado);
      setParteAtual(parte);
      setMensagens((m) => [
        ...m.filter((x) => x.id !== espera.id),
        {
          id: novoId(),
          papel: "app",
          tipo: "texto",
          texto: `Agora usando ${i.label}. O que você leu antes continua acima, para comparar.`,
        },
        ...mensagensDaExplicacao(resultado, parte),
      ]);
      setStatus(`Universo trocado para ${i.label}.`);
    } catch (err) {
      tira(espera.id);
      setError(err instanceof Error ? err.message : "Não foi possível trocar de universo.");
    }
  }

  // ------------------------------------------------------------ explicação

  function continuar() {
    if (!explicacao || parteAtual >= total) return;
    const n = parteAtual + 1;
    setParteAtual(n);
    acrescenta({
      id: novoId(),
      papel: "app",
      tipo: "parte",
      parte: n,
      explicacao,
      tecnica: modoTecnico && temVersaoTecnica(explicacao, n),
    });
    setStatus(`${tituloDaParte(explicacao, n)}${posicaoDaParte(explicacao, n)}.`);
  }

  function alternarTecnica() {
    if (!ultimaParte) return;
    const id = ultimaParte.id;
    setModoTecnico(!ultimaParte.tecnica);
    setMensagens((m) =>
      m.map((msg) => (msg.id === id && msg.tipo === "parte" ? { ...msg, tecnica: !msg.tecnica } : msg)),
    );
    // A mudança é dentro de uma mensagem já anunciada: o aviso curto vai pela
    // região de status, para o log não reler o texto inteiro (DD09).
    setStatus(ultimaParte.tecnica ? "De volta à explicação com comparação." : "Agora em termos técnicos, sem comparação.");
  }

  function pedirTrocaDeUniverso() {
    perguntarUniverso("Qual universo você quer usar agora? Pode ser um que já usou ou um novo.");
    focarCampo();
  }

  function outroConteudo() {
    acrescenta({ id: novoId(), papel: "app", tipo: "texto", texto: "O que você quer entender agora?" });
    setConceito(null);
    setExplicacao(null);
    setParteAtual(0);
    setModoTecnico(false);
    setModo("assunto");
    setSugestoes(sugestoesDeAssunto(concepts));
    setStatus("Escolha outro conteúdo.");
    focarCampo();
  }

  async function avaliar(e: Explanation, kind: "util" | "errada" | "confusa") {
    if (e.id === null) return;
    await api.feedback(e.id, kind);
    setAvaliados((a) => [...a, e.id as number]);
    setStatus(kind === "errada" ? "Obrigado. Vamos conferir essa explicação." : "Obrigado! Sua avaliação foi registrada.");
  }

  // ------------------------------------------------------------ pergunta

  async function perguntar(t: string) {
    if (!conceito) return;
    falaDoAluno(t);
    setOcupado(true);
    const espera = esperando("Conferindo no material");
    try {
      const r = await api.ask(conceito.slug, t, interesse?.id);
      const resposta: Mensagem =
        r.status === "fora_do_conceito"
          ? { id: novoId(), papel: "app", tipo: "recusa", texto: r.resposta }
          : { id: novoId(), papel: "app", tipo: "resposta", texto: r.resposta };
      setMensagens((m) => [...m.filter((x) => x.id !== espera.id), resposta]);
      setStatus(r.status === "fora_do_conceito" ? "Pergunta fora do conteúdo." : "Resposta pronta.");
    } catch (err) {
      tira(espera.id);
      setError(err instanceof Error ? err.message : "Não foi possível responder agora.");
    } finally {
      setOcupado(false);
    }
  }

  // ------------------------------------------------------------ envio

  function focarCampo() {
    // gesto do próprio aluno: levar o foco ao campo é o que ele espera
    requestAnimationFrame(() => campoRef.current?.focus());
  }

  function enviar(t: string) {
    const limpo = t.trim();
    if (!limpo || ocupado) return;
    setError("");
    setTexto("");
    if (modo === "assunto") void escolherAssunto(limpo);
    else if (modo === "universo") void escolherUniverso(limpo);
    else void perguntar(limpo);
  }

  function aoEnviar(e: React.FormEvent) {
    e.preventDefault();
    enviar(texto);
  }

  function aoTeclar(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    // Enter envia; Shift+Enter quebra a linha, como nos chats de IA
    if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
      e.preventDefault();
      enviar(texto);
    }
  }

  // ------------------------------------------------------------ tela

  const ultimaId = mensagens[mensagens.length - 1]?.id;
  const ultimoAlunoId = [...mensagens].reverse().find((m) => m.papel === "aluno")?.id;
  const ultimaRecusaId = [...mensagens].reverse().find((m) => m.tipo === "recusa")?.id;
  const avaliada =
    ultimaParte?.explicacao.id != null && avaliados.includes(ultimaParte.explicacao.id);

  return (
    <div className="conversa">
      {conceito && (
        <p className="conversa-contexto">
          <span className="visualmente-oculto">Estudando: </span>
          <strong>{conceito.title}</strong>
          {interesse && (
            <>
              <span aria-hidden="true"> · </span>
              <span className="visualmente-oculto">, comparando com </span>
              <span className="chip">{interesse.label}</span>
            </>
          )}
        </p>
      )}

      <div role="log" aria-live="polite" aria-relevant="additions" aria-label="Conversa" className="log">
        <ol className="mensagens">
          {mensagens.map((m) => (
            <li
              key={m.id}
              ref={(el) => {
                if (m.id === ultimaId) ultimaRef.current = el;
                if (m.id === ultimoAlunoId) alunoRef.current = el;
              }}
              tabIndex={-1}
              className={`mensagem ${m.papel} ${m.tipo}`}
            >
              {m.papel === "aluno" ? (
                <>
                  <span className="visualmente-oculto">Você: </span>
                  <p>{m.texto}</p>
                </>
              ) : m.tipo === "parte" ? (
                <>
                  <h3>
                    {tituloDaParte(m.explicacao, m.parte)}
                    <span className="visualmente-oculto">{posicaoDaParte(m.explicacao, m.parte)}</span>
                  </h3>
                  <ParteMensagem explicacao={m.explicacao} parte={m.parte} tecnica={m.tecnica} />
                </>
              ) : m.tipo === "recusa" ? (
                <>
                  <h3>Fora deste conteúdo</h3>
                  <p>{m.texto}</p>
                  {m.id === ultimaRecusaId && (
                    // Nunca um beco sem saída: duas saídas explícitas (DD05)
                    <div className="acoes acoes-mensagem">
                      <button type="button" className="secundario" onClick={() => { setStatus("Continuando neste conteúdo."); focarCampo(); }}>
                        Continuar este conteúdo
                      </button>
                      <button type="button" className="secundario" onClick={outroConteudo}>
                        Estudar outro conteúdo
                      </button>
                    </div>
                  )}
                </>
              ) : m.tipo === "resposta" ? (
                <>
                  <h3 className="visualmente-oculto">Resposta</h3>
                  <p>{m.texto}</p>
                </>
              ) : m.tipo === "aviso" ? (
                <p className="aviso">{m.texto}</p>
              ) : m.tipo === "esperando" ? (
                <p className="dica">
                  {m.texto}
                  <span className="pontinhos" aria-hidden="true">
                    <i />
                    <i />
                    <i />
                  </span>
                </p>
              ) : (
                <>
                  <p>{m.texto}</p>
                  {m.tipo === "texto" && m.fontes && m.fontes.length > 0 && (
                    <ol className="fontes">
                      {m.fontes.map((f) => (
                        <li key={f.url}>
                          <a href={f.url} target="_blank" rel="noopener noreferrer">
                            {f.titulo}
                            <span className="visualmente-oculto"> (abre em nova aba)</span>
                          </a>
                        </li>
                      ))}
                    </ol>
                  )}
                </>
              )}
            </li>
          ))}
        </ol>
      </div>

      <div className="rodape-chat">
        {/* Ações e sugestões: uma barra só, sempre no mesmo lugar */}
        <div className="barra-sugestoes" role="group" aria-label="Ações e sugestões">
          {modo === "pergunta" && explicacao && ultimaParte && (
            <>
              {!terminou ? (
                <button type="button" onClick={continuar} disabled={ocupado} aria-disabled={ocupado}>
                  Continuar
                </button>
              ) : (
                <button type="button" onClick={outroConteudo}>
                  Estudar outro conteúdo
                </button>
              )}
              {temVersaoTecnica(ultimaParte.explicacao, ultimaParte.parte) && (
                <button type="button" className="secundario" aria-pressed={ultimaParte.tecnica} onClick={alternarTecnica}>
                  {ultimaParte.tecnica ? "Voltar para a comparação" : "Ver versão técnica"}
                </button>
              )}
              <button type="button" className="secundario" onClick={pedirTrocaDeUniverso} disabled={ocupado}>
                Trocar universo
              </button>
              {ultimaParte.explicacao.id !== null &&
                (avaliada ? (
                  <span className="dica">Obrigado, vamos conferir.</span>
                ) : (
                  <button type="button" className="perigo" onClick={() => avaliar(ultimaParte.explicacao, "errada")}>
                    Está errada
                  </button>
                ))}
            </>
          )}
          {modo !== "pergunta" &&
            sugestoes.map((s) => (
              <button
                key={s.rotulo}
                type="button"
                className="secundario sugestao"
                disabled={ocupado}
                onClick={() => {
                  enviar(s.texto);
                  focarCampo();
                }}
              >
                {s.rotulo}
              </button>
            ))}
        </div>

        <form onSubmit={aoEnviar} className="caixa-mensagem">
          <label htmlFor="mensagem" className="visualmente-oculto">
            {ROTULO_CAMPO[modo]}
          </label>
          <textarea
            id="mensagem"
            ref={campoRef}
            rows={1}
            value={texto}
            maxLength={modo === "pergunta" ? 300 : modo === "universo" ? 60 : 200}
            placeholder={PLACEHOLDER[modo]}
            autoComplete="off"
            onChange={(ev) => setTexto(ev.target.value)}
            onKeyDown={aoTeclar}
          />
          <button type="submit" className="enviar" disabled={ocupado || !texto.trim()} aria-label="Enviar">
            <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false">
              <path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
        </form>
        <p className="dica rodape-aviso">
          {modo === "universo"
            ? "Evite informar religião, saúde, política ou outros dados sensíveis."
            : "Respondo só sobre o conteúdo escolhido e confiro a resposta antes de mostrar."}
          <button type="button" className="texto" onClick={() => ultimaRef.current?.focus()}>
            Ir para a última mensagem
          </button>
        </p>
      </div>
    </div>
  );
}

function boasVindas(): Mensagem {
  return {
    id: novoId(),
    papel: "app",
    tipo: "texto",
    texto:
      "Oi! O que você quer entender hoje? Escreva com suas palavras. " +
      "Depois eu pergunto um universo de que você gosta e explico comparando com ele.",
  };
}

function sugestoesDeAssunto(concepts: Concept[]): Sugestao[] {
  return concepts.map((c) => ({ rotulo: c.title, texto: c.title }));
}
