import { useEffect, useRef, useState } from "react";
import type { Interest } from "../api";

/**
 * Trocar de universo sem sair da explicação (RF09, decisões D4 e DD04).
 *
 * É um `<dialog>` nativo aberto com `showModal()`, e não uma div com ARIA: o
 * elemento nativo já prende o foco, fecha com Esc e devolve o foco ao botão
 * que o abriu (WCAG 2.1.2 e 2.4.3). Reimplementar isso à mão é a forma mais
 * comum de quebrar um diálogo para quem usa teclado.
 */
export function TrocarUniverso({
  aberto,
  interesses,
  atualId,
  onEscolher,
  onCriar,
  onFechar,
}: {
  aberto: boolean;
  interesses: Interest[];
  atualId: number;
  onEscolher: (id: number, rotulo?: string) => void;
  onCriar: (label: string, depth: number) => Promise<Interest | null>;
  onFechar: () => void;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  const [novo, setNovo] = useState("");
  const [erro, setErro] = useState("");

  useEffect(() => {
    const dialogo = ref.current;
    if (!dialogo) return;
    if (aberto && !dialogo.open) dialogo.showModal();
    if (!aberto && dialogo.open) dialogo.close();
  }, [aberto]);

  async function criar(e: React.FormEvent) {
    e.preventDefault();
    if (novo.trim().length < 2) {
      setErro("Escreva um universo com pelo menos 2 letras, por exemplo: xadrez.");
      return;
    }
    setErro("");
    const criado = await onCriar(novo.trim(), 2);
    if (criado) {
      setNovo("");
      onEscolher(criado.id, criado.label);
    }
  }

  return (
    <dialog ref={ref} onClose={onFechar} aria-labelledby="t-trocar" className="folha">
      <h2 id="t-trocar">Trocar de universo</h2>
      {/* Dizer antes o que vai acontecer com a leitura (WCAG 3.2.5, DD04).
          Sem prometer um número de passo: se o novo universo não tiver
          explicação personalizada, a conversa cai na explicação padrão, que
          tem um passo só. Promessa que o app nem sempre cumpre é pior do
          que promessa nenhuma. */}
      <p className="dica">
        Você continua no mesmo ponto da explicação, agora com o novo universo. O que já
        leu permanece na conversa.
      </p>

      <ul className="lista-universos">
        {interesses.map((i) => (
          <li key={i.id}>
            <button
              type="button"
              className="secundario universo"
              aria-current={i.id === atualId ? "true" : undefined}
              onClick={() => onEscolher(i.id)}
            >
              {i.label}
              {/* Estado dito em texto, não só por cor ou realce (WCAG 1.4.1) */}
              {i.id === atualId && <span className="marca-atual"> — em uso agora</span>}
            </button>
          </li>
        ))}
      </ul>

      <form onSubmit={criar} noValidate>
        <label htmlFor="novo-universo">Usar outro universo</label>
        <input
          id="novo-universo"
          type="text"
          value={novo}
          maxLength={60}
          autoComplete="off"
          aria-describedby={erro ? "novo-universo-erro" : undefined}
          aria-invalid={erro ? true : undefined}
          onChange={(e) => setNovo(e.target.value)}
        />
        {erro && (
          <p id="novo-universo-erro" className="erro">
            {erro}
          </p>
        )}
        <div className="acoes">
          <button type="submit">Usar este universo</button>
          <button type="button" className="secundario" onClick={onFechar}>
            Cancelar
          </button>
        </div>
      </form>
    </dialog>
  );
}
