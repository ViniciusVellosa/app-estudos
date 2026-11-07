import { useEffect, useRef, useState } from "react";
import {
  api,
  ApiError,
  ensureSession,
  forgetSession,
  type Concept,
  type Interest,
  type ReadingPrefs,
} from "./api";
import { Chat } from "./chat/Chat";

type Screen = "carregando" | "consentimento" | "interesses" | "estudar" | "preferencias" | "meus-dados";

const TITLES: Record<Screen, string> = {
  carregando: "Carregando",
  consentimento: "Antes de começar",
  interesses: "Seus interesses",
  estudar: "Estudar",
  preferencias: "Preferências de leitura",
  "meus-dados": "Meus dados",
};

const DEFAULT_PREFS: ReadingPrefs = { font_scale: 1, theme: "sistema", reduced_motion: false };

function applyPrefs(p: ReadingPrefs) {
  const root = document.documentElement;
  root.style.setProperty("--font-scale", String(p.font_scale));
  root.dataset.theme = p.theme;
  root.dataset.reducedMotion = String(p.reduced_motion);
}

export default function App() {
  const [screen, setScreen] = useState<Screen>("carregando");
  const [status, setStatus] = useState(""); // mensagens anunciadas pelo leitor de tela
  const [error, setError] = useState("");
  const [interests, setInterests] = useState<Interest[]>([]);
  const [concepts, setConcepts] = useState<Concept[]>([]);
  const [prefs, setPrefs] = useState<ReadingPrefs>(DEFAULT_PREFS);
  const titleRef = useRef<HTMLHeadingElement>(null);
  const firstScreenShown = useRef(false);

  // A cada troca de tela: título da aba e foco no título (orientação para
  // leitor de tela). Na primeira tela o foco fica no início da página, para
  // que o link "Pular para o conteúdo" seja o primeiro item do Tab.
  useEffect(() => {
    document.title = `${TITLES[screen]} — Estudos do Seu Jeito`;
    if (screen === "carregando") return;
    if (firstScreenShown.current) titleRef.current?.focus();
    firstScreenShown.current = true;
  }, [screen]);

  useEffect(() => {
    (async () => {
      try {
        await ensureSession();
        const p = await api.getPrefs();
        setPrefs(p);
        applyPrefs(p);
        setConcepts(await api.concepts());
        try {
          const list = await api.interests();
          setInterests(list);
          setScreen(list.length ? "estudar" : "interesses");
        } catch (e) {
          if (e instanceof ApiError && e.status === 403) setScreen("consentimento");
          else throw e;
        }
      } catch (e) {
        if (e instanceof ApiError && e.status === 401) {
          forgetSession(); // sessão apagada: começa de novo
          window.location.reload();
          return;
        }
        setError("Não foi possível conectar ao servidor. Verifique sua conexão e recarregue a página.");
      }
    })();
  }, []);

  function go(next: Screen) {
    setError("");
    setStatus("");
    setScreen(next);
  }

  return (
    <>
      <a className="pular botao" href="#conteudo">Pular para o conteúdo</a>
      <header className="topo">
        <div className="topo-conteudo">
          <p><strong>Estudos do Seu Jeito</strong></p>
          {interests.length > 0 && (
            <nav aria-label="Principal">
              <div className="acoes">
                <button type="button" className="secundario" aria-current={screen === "estudar" ? "page" : undefined} onClick={() => go("estudar")}>Estudar</button>
                <button type="button" className="secundario" aria-current={screen === "interesses" ? "page" : undefined} onClick={() => go("interesses")}>Interesses</button>
                <button type="button" className="secundario" aria-current={screen === "preferencias" ? "page" : undefined} onClick={() => go("preferencias")}>Leitura</button>
                <button type="button" className="secundario" aria-current={screen === "meus-dados" ? "page" : undefined} onClick={() => go("meus-dados")}>Meus dados</button>
              </div>
            </nav>
          )}
        </div>
      </header>

      <main id="conteudo">
        <h1 ref={titleRef} tabIndex={-1}>{TITLES[screen]}</h1>
        {/* Região viva: anuncia resultados sem mover o foco (WCAG 4.1.3).
            Na conversa ela fica só para leitor de tela: a própria mensagem
            que chegou já é a confirmação visual, e repetir "parte 3 de 6"
            acima do chat devolve à tela a engrenagem que tiramos dela. */}
        <p
          role="status"
          aria-live="polite"
          className={status && screen !== "estudar" ? "" : "visualmente-oculto"}
        >
          {status}
        </p>
        {error && <p role="alert" className="erro">{error}</p>}

        {screen === "consentimento" && (
          <Consent
            onAccept={async () => {
              await api.consent(true);
              go("interesses");
            }}
          />
        )}
        {screen === "interesses" && (
          <Interests
            interests={interests}
            onChange={setInterests}
            onDone={() => go("estudar")}
            setStatus={setStatus}
            setError={setError}
          />
        )}
        {/* A conversa fica montada e apenas escondida nas outras telas.
            Desmontar apagaria o histórico, e a tarefa T4 do teste de
            usabilidade pede justamente que a pessoa vá ajustar a leitura no
            meio da explicação: voltar e encontrar a conversa vazia seria um
            problema sério. `hidden` tira o conteúdo da árvore de
            acessibilidade, então nada escondido é lido ou tabulável. */}
        {interests.length > 0 && (
          <div hidden={screen !== "estudar"}>
            <Chat
              concepts={concepts}
              interests={interests}
              onInteresses={setInterests}
              setStatus={setStatus}
              setError={setError}
            />
          </div>
        )}
        {screen === "preferencias" && (
          <Prefs
            prefs={prefs}
            onSave={async (p) => {
              applyPrefs(p);
              setPrefs(await api.putPrefs(p));
              setStatus("Preferências salvas.");
            }}
          />
        )}
        {screen === "meus-dados" && <MyData setStatus={setStatus} />}
      </main>
    </>
  );
}

function Consent({ onAccept }: { onAccept: () => Promise<void> }) {
  const [checked, setChecked] = useState(false);
  return (
    <section aria-labelledby="t-termo">
      <h2 id="t-termo">Como usamos seus dados</h2>
      <ul>
        <li>Você não precisa informar nome nem e-mail.</li>
        <li>Guardamos só os interesses que você escolher (por exemplo, um jogo ou esporte) e suas preferências de leitura.</li>
        <li>Usamos os interesses apenas para adaptar as explicações. Se a explicação for gerada por IA, só o nome do interesse é enviado, nunca algo que identifique você.</li>
        <li>Você pode ver, mudar ou apagar tudo a qualquer momento em “Meus dados”.</li>
      </ul>
      <p className="dica">Este texto é um modelo: adapte-o ao termo de consentimento aprovado no seu projeto.</p>
      <label>
        <input type="checkbox" checked={checked} onChange={(e) => setChecked(e.target.checked)} /> Li e concordo
      </label>
      <div className="acoes">
        <button type="button" disabled={!checked} onClick={onAccept}>Continuar</button>
      </div>
    </section>
  );
}

function Interests(props: {
  interests: Interest[];
  onChange: (i: Interest[]) => void;
  onDone: () => void;
  setStatus: (s: string) => void;
  setError: (s: string) => void;
}) {
  const [label, setLabel] = useState("");
  const [depth, setDepth] = useState(2);
  const [fieldError, setFieldError] = useState("");

  async function add(e: React.FormEvent) {
    e.preventDefault();
    if (label.trim().length < 2) {
      setFieldError("Escreva um interesse com pelo menos 2 letras, por exemplo: futebol.");
      return;
    }
    setFieldError("");
    try {
      const created = await api.addInterest(label.trim(), depth);
      props.onChange([...props.interests, created]);
      props.setStatus(`Interesse “${created.label}” adicionado.`);
      setLabel("");
    } catch (err) {
      props.setError(err instanceof Error ? err.message : "Não foi possível salvar.");
    }
  }

  async function remove(i: Interest) {
    await api.removeInterest(i.id);
    props.onChange(props.interests.filter((x) => x.id !== i.id));
    props.setStatus(`Interesse “${i.label}” removido.`);
  }

  return (
    <>
      <p>Conte do que você gosta. Vamos usar isso para criar comparações nas explicações.</p>
      <form onSubmit={add} noValidate>
        <label htmlFor="interesse">Interesse (jogo, série, esporte, música…)</label>
        <p id="interesse-dica" className="dica">Evite informar religião, saúde, política ou outros dados sensíveis.</p>
        <input
          id="interesse"
          type="text"
          value={label}
          maxLength={60}
          autoComplete="off"
          aria-describedby={fieldError ? "interesse-dica interesse-erro" : "interesse-dica"}
          aria-invalid={fieldError ? true : undefined}
          onChange={(e) => setLabel(e.target.value)}
        />
        {fieldError && <p id="interesse-erro" className="erro">{fieldError}</p>}
        <fieldset>
          <legend>Quanto você conhece desse assunto?</legend>
          {[
            [1, "Conheço pouco"],
            [2, "Conheço bem"],
            [3, "Sou fã e conheço os detalhes"],
          ].map(([value, text]) => (
            <label key={value}>
              <input type="radio" name="profundidade" checked={depth === value} onChange={() => setDepth(value as number)} />
              {text}
            </label>
          ))}
        </fieldset>
        <div className="acoes">
          <button type="submit">Adicionar interesse</button>
        </div>
      </form>

      {props.interests.length > 0 && (
        <>
          <h2>Seus interesses</h2>
          <ul>
            {props.interests.map((i) => (
              <li key={i.id}>
                {i.label}{" "}
                <button type="button" className="perigo" onClick={() => remove(i)} aria-label={`Remover ${i.label}`}>
                  Remover
                </button>
              </li>
            ))}
          </ul>
          <div className="acoes">
            <button type="button" onClick={props.onDone}>Começar a estudar</button>
          </div>
        </>
      )}
    </>
  );
}

function Prefs({ prefs, onSave }: { prefs: ReadingPrefs; onSave: (p: ReadingPrefs) => Promise<void> }) {
  const [draft, setDraft] = useState(prefs);
  const themes: [ReadingPrefs["theme"], string][] = [
    ["sistema", "Igual ao do celular/computador"],
    ["claro", "Claro"],
    ["escuro", "Escuro"],
    ["alto-contraste", "Alto contraste (amarelo sobre preto)"],
  ];
  const sizes: [number, string][] = [
    [1, "Normal"],
    [1.25, "Grande"],
    [1.5, "Muito grande"],
    [2, "Enorme"],
  ];
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSave(draft);
      }}
    >
      <fieldset>
        <legend>Tamanho do texto</legend>
        {sizes.map(([v, t]) => (
          <label key={v}>
            <input type="radio" name="tamanho" checked={draft.font_scale === v} onChange={() => setDraft({ ...draft, font_scale: v })} />
            {t}
          </label>
        ))}
      </fieldset>
      <fieldset>
        <legend>Cores</legend>
        {themes.map(([v, t]) => (
          <label key={v}>
            <input type="radio" name="tema" checked={draft.theme === v} onChange={() => setDraft({ ...draft, theme: v })} />
            {t}
          </label>
        ))}
      </fieldset>
      <label>
        <input type="checkbox" checked={draft.reduced_motion} onChange={(e) => setDraft({ ...draft, reduced_motion: e.target.checked })} /> Reduzir animações
      </label>
      <div className="acoes">
        <button type="submit">Salvar preferências</button>
      </div>
    </form>
  );
}

function MyData({ setStatus }: { setStatus: (s: string) => void }) {
  const [data, setData] = useState<string>("");
  const [confirming, setConfirming] = useState(false);
  return (
    <>
      <p>Você pode ver tudo o que guardamos sobre você e apagar seus dados quando quiser.</p>
      <div className="acoes">
        <button
          type="button"
          className="secundario"
          onClick={async () => {
            setData(JSON.stringify(await api.exportData(), null, 2));
            setStatus("Seus dados estão abaixo.");
          }}
        >
          Ver meus dados
        </button>
        {!confirming && (
          <button type="button" className="perigo" onClick={() => setConfirming(true)}>Apagar todos os meus dados</button>
        )}
      </div>
      {data && <pre tabIndex={0} aria-label="Seus dados">{data}</pre>}
      {confirming && (
        <section aria-labelledby="t-apagar" className="aviso">
          <h2 id="t-apagar">Apagar tudo?</h2>
          <p>Seus interesses, preferências e avaliações serão apagados. Isso não pode ser desfeito.</p>
          <div className="acoes">
            <button
              type="button"
              className="perigo"
              onClick={async () => {
                await api.deleteMe();
                forgetSession();
                window.location.reload();
              }}
            >
              Sim, apagar tudo
            </button>
            <button type="button" className="secundario" onClick={() => setConfirming(false)}>Cancelar</button>
          </div>
        </section>
      )}
    </>
  );
}
