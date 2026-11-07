import { useRef, useState } from "react";
import { api, type Concept, type Explanation, type Interest } from "../api";
import { ParteMensagem } from "./ParteMensagem";
import { TrocarUniverso } from "./TrocarUniverso";
import {
  parteAoTrocarDeUniverso,
  posicaoDaParte,
  temVersaoTecnica,
  tituloDaParte,
  totalDePartes,
} from "./partes";

/**
 * A conversa (RF10, decisão D3): uma parte da explicação por mensagem, no
 * ritmo de quem lê.
 *
 * Três regras de acessibilidade mandam no desenho deste componente:
 *
 * - o histórico é `role="log"` com `aria-live="polite"` e
 *   `aria-relevant="additions"`: anuncia a mensagem que chegou pronta, e não
 *   cada alteração dentro das anteriores (WCAG 4.1.3);
 * - **nada rola nem recebe foco sozinho.** Não há `scrollIntoView` nem
 *   `focus()` automático aqui, de propósito: movimento automático desorienta
 *   quem lê uma janela ampliada de poucos caracteres. Quem quiser descer usa
 *   "Ir para a última mensagem";
 * - as ações ficam na mensagem atual, com rótulo em texto e alvo grande
 *   (WCAG 2.5.8).
 *
 * A numeração das partes não aparece no título da mensagem: ela vai na barra
 * de progresso, para quem vê, e num trecho oculto do título, para quem ouve.
 */

type Mensagem =
  | { id: number; papel: "app"; tipo: "parte"; parte: number; explicacao: Explanation; tecnica: boolean }
  | { id: number; papel: "app"; tipo: "info" | "aviso" | "recusa" | "esperando"; texto: string }
  | { id: number; papel: "app"; tipo: "resposta"; texto: string; trechos: string[] }
  | { id: number; papel: "aluno"; tipo: "pergunta"; texto: string };

let proximoId = 0;
const novoId = () => ++proximoId;

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
  const [conceito, setConceito] = useState(concepts[0]?.slug ?? "");
  const [interesseId, setInteresseId] = useState(interests[0]?.id ?? 0);
  const [explicacao, setExplicacao] = useState<Explanation | null>(null);
  const [mensagens, setMensagens] = useState<Mensagem[]>([]);
  const [parteAtual, setParteAtual] = useState(0);
  const [ocupado, setOcupado] = useState(false);
  const [trocando, setTrocando] = useState(false);
  const [pergunta, setPergunta] = useState("");
  const [avaliados, setAvaliados] = useState<number[]>([]);
  const ultimaRef = useRef<HTMLLIElement>(null);

  const titulo = concepts.find((c) => c.slug === conceito)?.title ?? "";
  const universo = interests.find((i) => i.id === interesseId)?.label ?? "";
  const total = explicacao ? totalDePartes(explicacao) : 0;
  const terminou = explicacao !== null && parteAtual >= total;

  const acrescenta = (...novas: Mensagem[]) => setMensagens((m) => [...m, ...novas]);

  function mensagensDaExplicacao(e: Explanation, parte: number): Mensagem[] {
    const msgs: Mensagem[] = [];
    if (e.notice) msgs.push({ id: novoId(), papel: "app", tipo: "aviso", texto: e.notice });
    msgs.push({ id: novoId(), papel: "app", tipo: "parte", parte, explicacao: e, tecnica: false });
    return msgs;
  }

  async function comecar(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setOcupado(true);
    const espera: Mensagem = {
      id: novoId(),
      papel: "app",
      tipo: "esperando",
      // DD22: a autoverificação são várias chamadas ao modelo; a espera é
      // uma mensagem, e não uma tela travada.
      texto: "Preparando e conferindo a explicação",
    };
    acrescenta(espera);
    setStatus("Preparando a explicação…");
    try {
      const resultado = await api.explain(conceito, interesseId);
      setExplicacao(resultado);
      setParteAtual(1);
      setMensagens((m) => [
        ...m.filter((x) => x.id !== espera.id),
        ...mensagensDaExplicacao(resultado, 1),
      ]);
      setStatus(resultado.personalized ? "Explicação pronta." : "Explicação padrão pronta.");
    } catch (err) {
      setMensagens((m) => m.filter((x) => x.id !== espera.id));
      setStatus("");
      setError(err instanceof Error ? err.message : "Não foi possível gerar a explicação.");
    } finally {
      setOcupado(false);
    }
  }

  function continuar() {
    if (!explicacao || parteAtual >= total) return;
    const n = parteAtual + 1;
    setParteAtual(n);
    acrescenta({ id: novoId(), papel: "app", tipo: "parte", parte: n, explicacao, tecnica: false });
    setStatus(`${tituloDaParte(explicacao, n)}${posicaoDaParte(explicacao, n)}.`);
  }

  function alternarTecnica(id: number) {
    setMensagens((m) =>
      m.map((msg) =>
        msg.id === id && msg.tipo === "parte" ? { ...msg, tecnica: !msg.tecnica } : msg,
      ),
    );
    const alvo = mensagens.find((m) => m.id === id);
    if (alvo?.tipo === "parte") {
      // A mudança acontece dentro de uma mensagem já anunciada; o aviso curto
      // vai pela região de status, para o log não reler o texto inteiro.
      setStatus(
        alvo.tecnica
          ? "De volta à explicação com comparação."
          : "Agora em termos técnicos, sem comparação.",
      );
    }
  }

  // `rotuloNovo` vem junto porque um universo recém-criado ainda não chegou à
  // lista `interests` neste render: sem ele, a conversa anunciaria "outro
  // universo" justo quando a pessoa acabou de escrever o nome.
  async function trocarUniverso(novoId_: number, rotuloNovo?: string) {
    setTrocando(false);
    if (!explicacao || novoId_ === interesseId) return;
    setInteresseId(novoId_);
    setOcupado(true);
    const rotulo = rotuloNovo ?? interests.find((i) => i.id === novoId_)?.label ?? "outro universo";
    const espera: Mensagem = {
      id: novoId(),
      papel: "app",
      tipo: "esperando",
      texto: `Trocando para ${rotulo}`,
    };
    acrescenta(espera);
    try {
      const resultado = await api.explain(conceito, novoId_);
      const parte = parteAoTrocarDeUniverso(resultado, parteAtual);
      setExplicacao(resultado);
      setParteAtual(parte);
      setMensagens((m) => [
        ...m.filter((x) => x.id !== espera.id),
        {
          id: novoId(),
          papel: "app",
          tipo: "info",
          texto: `Agora usando ${rotulo}. O que você leu antes continua acima, para comparar.`,
        },
        ...mensagensDaExplicacao(resultado, parte),
      ]);
      setStatus(`Universo trocado para ${rotulo}.`);
    } catch (err) {
      setMensagens((m) => m.filter((x) => x.id !== espera.id));
      setError(err instanceof Error ? err.message : "Não foi possível trocar de universo.");
    } finally {
      setOcupado(false);
    }
  }

  async function criarInteresse(label: string, depth: number) {
    try {
      const criado = await api.addInterest(label, depth);
      onInteresses([...interests, criado]);
      return criado;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Não foi possível salvar o universo.");
      return null;
    }
  }

  async function perguntar(e: React.FormEvent) {
    e.preventDefault();
    const texto = pergunta.trim();
    if (!texto || !explicacao) return;
    setPergunta("");
    setOcupado(true);
    acrescenta({ id: novoId(), papel: "aluno", tipo: "pergunta", texto });
    const espera: Mensagem = {
      id: novoId(),
      papel: "app",
      tipo: "esperando",
      texto: "Conferindo no material",
    };
    acrescenta(espera);
    try {
      const r = await api.ask(conceito, texto, interesseId);
      const resposta: Mensagem =
        r.status === "fora_do_conceito"
          ? { id: novoId(), papel: "app", tipo: "recusa", texto: r.resposta }
          : { id: novoId(), papel: "app", tipo: "resposta", texto: r.resposta, trechos: r.trechos };
      setMensagens((m) => [...m.filter((x) => x.id !== espera.id), resposta]);
      setStatus(r.status === "fora_do_conceito" ? "Pergunta fora do conceito." : "Resposta pronta.");
    } catch (err) {
      setMensagens((m) => m.filter((x) => x.id !== espera.id));
      setError(err instanceof Error ? err.message : "Não foi possível responder agora.");
    } finally {
      setOcupado(false);
    }
  }

  async function avaliar(e: Explanation, kind: "util" | "errada" | "confusa") {
    if (e.id === null) return;
    await api.feedback(e.id, kind);
    setAvaliados((a) => [...a, e.id as number]);
    setStatus(
      kind === "errada"
        ? "Obrigado. Vamos conferir essa explicação."
        : "Obrigado! Sua avaliação foi registrada.",
    );
  }

  function recomecar() {
    setExplicacao(null);
    setMensagens([]);
    setParteAtual(0);
    setStatus("Escolha outro conceito.");
  }

  // ---------------------------------------------------------------- telas

  if (!explicacao && mensagens.length === 0) {
    return (
      <section className="cartao-inicio" aria-labelledby="t-inicio">
        <h2 id="t-inicio">Qual conteúdo você quer entender?</h2>
        <p className="dica">
          A explicação começa por uma comparação com algo que você gosta, em partes curtas.
          Você pode ver a versão técnica a qualquer momento.
        </p>
        <form onSubmit={comecar}>
          {/* DD01: o conceito vem antes do universo. O conteúdo técnico é o
              assunto; o universo é só como ele vai ser contado. */}
          {/* O título do cartão já faz a pergunta; o rótulo nomeia o campo */}
          <label htmlFor="conceito">Conteúdo</label>
          <select id="conceito" value={conceito} onChange={(ev) => setConceito(ev.target.value)}>
            {concepts.map((c) => (
              <option key={c.slug} value={c.slug}>
                {c.title}
              </option>
            ))}
          </select>
          <label htmlFor="usar-interesse">Explicar usando</label>
          <select
            id="usar-interesse"
            value={interesseId}
            onChange={(ev) => setInteresseId(Number(ev.target.value))}
          >
            {interests.map((i) => (
              <option key={i.id} value={i.id}>
                {i.label}
              </option>
            ))}
          </select>
          <div className="acoes">
            <button type="submit" disabled={ocupado} aria-disabled={ocupado}>
              {ocupado ? "Preparando…" : "Começar a explicar"}
            </button>
          </div>
        </form>
      </section>
    );
  }

  const ultimaId = mensagens[mensagens.length - 1]?.id;
  // As ações ficam na última PARTE, não na última mensagem: depois de uma
  // pergunta, "Ver versão técnica" e "Trocar universo" precisam continuar ao
  // alcance. Nas partes anteriores elas somem — histórico é leitura.
  const ultimaParteId = [...mensagens].reverse().find((m) => m.tipo === "parte")?.id;
  const progresso = total > 0 ? Math.round((Math.max(parteAtual, 1) / total) * 100) : 0;

  return (
    <div className="conversa">
      <header className="conversa-topo">
        <h2 className="conversa-assunto">{titulo}</h2>
        <p className="conversa-meta">
          <span className="chip">{universo}</span>
          {explicacao?.payload && (
            <span className="dica">
              parte {Math.max(parteAtual, 1)} de {total}
            </span>
          )}
        </p>
        {/* Decorativa: a posição já está dita em texto logo acima e no
            título de cada mensagem, então a barra fica fora da leitura. */}
        <div className="progresso" aria-hidden="true">
          <span className="progresso-feito" style={{ width: `${progresso}%` }} />
        </div>
        <p className="dica conversa-limite">
          Respondo perguntas sobre este conteúdo. Fora dele, eu aviso.
        </p>
      </header>

      <div
        role="log"
        aria-live="polite"
        aria-relevant="additions"
        aria-label="Conversa sobre o conceito"
        className="log"
      >
        <ol className="mensagens">
          {mensagens.map((m) => (
            <li
              key={m.id}
              ref={m.id === ultimaId ? ultimaRef : undefined}
              tabIndex={-1}
              className={`mensagem ${m.papel} ${m.tipo}`}
            >
              {m.papel === "aluno" ? (
                <>
                  <h3 className="rotulo-mensagem">Você perguntou</h3>
                  <p>{m.texto}</p>
                </>
              ) : m.tipo === "parte" ? (
                <>
                  <h3>
                    {tituloDaParte(m.explicacao, m.parte)}
                    <span className="visualmente-oculto">
                      {posicaoDaParte(m.explicacao, m.parte)}
                    </span>
                  </h3>
                  <ParteMensagem explicacao={m.explicacao} parte={m.parte} tecnica={m.tecnica} />
                  {m.id === ultimaParteId && (
                    <AcoesDaMensagem
                      mensagem={m}
                      avaliada={m.explicacao.id !== null && avaliados.includes(m.explicacao.id)}
                      onTecnica={() => alternarTecnica(m.id)}
                      onTrocar={() => setTrocando(true)}
                      onErrada={() => avaliar(m.explicacao, "errada")}
                    />
                  )}
                </>
              ) : m.tipo === "recusa" ? (
                <>
                  <h3 className="rotulo-mensagem">Fora deste conceito</h3>
                  <p>{m.texto}</p>
                  {/* Nunca um beco sem saída: duas saídas explícitas (DD05) */}
                  <div className="acoes acoes-mensagem">
                    <button type="button" onClick={() => setStatus("Continuando neste conceito.")}>
                      Continuar este conceito
                    </button>
                    <button type="button" className="secundario" onClick={recomecar}>
                      Escolher outro conceito
                    </button>
                  </div>
                </>
              ) : m.tipo === "resposta" ? (
                <>
                  <h3 className="rotulo-mensagem">Resposta</h3>
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
                <p>{m.texto}</p>
              )}
            </li>
          ))}
        </ol>
      </div>

      <div className="acoes barra-acoes">
        {!terminou && (
          <button type="button" onClick={continuar} disabled={ocupado} aria-disabled={ocupado}>
            Continuar
          </button>
        )}
        {terminou && (
          <button type="button" className="secundario" onClick={recomecar}>
            Estudar outro conteúdo
          </button>
        )}
        <button type="button" className="texto" onClick={() => ultimaRef.current?.focus()}>
          Ir para a última mensagem
        </button>
      </div>

      <form onSubmit={perguntar} className="caixa-pergunta">
        {/* Rótulo visível, nunca só placeholder (DD12, WCAG 3.3.2) */}
        <label htmlFor="pergunta">Sua pergunta sobre este conceito</label>
        <div className="linha-pergunta">
          <input
            id="pergunta"
            type="text"
            value={pergunta}
            maxLength={300}
            autoComplete="off"
            onChange={(ev) => setPergunta(ev.target.value)}
          />
          <button type="submit" disabled={ocupado || !pergunta.trim()}>
            Enviar
          </button>
        </div>
      </form>

      <TrocarUniverso
        aberto={trocando}
        interesses={interests}
        atualId={interesseId}
        onEscolher={trocarUniverso}
        onCriar={criarInteresse}
        onFechar={() => setTrocando(false)}
      />
    </div>
  );
}

function AcoesDaMensagem({
  mensagem,
  avaliada,
  onTecnica,
  onTrocar,
  onErrada,
}: {
  mensagem: { parte: number; explicacao: Explanation; tecnica: boolean };
  avaliada: boolean;
  onTecnica: () => void;
  onTrocar: () => void;
  onErrada: () => void;
}) {
  const { explicacao, parte, tecnica } = mensagem;
  return (
    <div className="acoes acoes-mensagem">
      {temVersaoTecnica(explicacao, parte) && (
        <button type="button" className="secundario" aria-pressed={tecnica} onClick={onTecnica}>
          {tecnica ? "Voltar para a comparação" : "Ver versão técnica"}
        </button>
      )}
      <button type="button" className="secundario" onClick={onTrocar}>
        Trocar universo
      </button>
      {explicacao.id !== null &&
        (avaliada ? (
          <p className="dica">Obrigado, vamos conferir.</p>
        ) : (
          <button type="button" className="perigo" onClick={onErrada}>
            Está errada
          </button>
        ))}
    </div>
  );
}
