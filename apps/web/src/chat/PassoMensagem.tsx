import type { Explanation } from "../api";
import { PASSOS, tituloDoPasso } from "./passos";

/**
 * O conteúdo de um passo da explicação dentro de uma mensagem do chat.
 *
 * Em `tecnica`, qualquer passo mostra a reformulação sem analogia, mantendo o
 * número do passo — é o que RF04 exige: alternar sem perder o ponto em que se
 * estava.
 */
export function PassoMensagem({
  explicacao,
  passo,
  tecnica,
}: {
  explicacao: Explanation;
  passo: number;
  tecnica: boolean;
}) {
  const p = explicacao.payload;

  if (!p) {
    return (
      <>
        {(explicacao.neutral_text ?? "").split(/\n\s*\n/).map((par, i) => (
          <p key={i}>{par}</p>
        ))}
      </>
    );
  }

  if (tecnica) {
    return (
      <>
        <p className="etiqueta-tecnica">Versão técnica, sem comparação</p>
        <p>{p.reformulacao_tecnica}</p>
      </>
    );
  }

  switch (PASSOS[passo - 1]) {
    case "O conceito":
      return <p>{p.conceito}</p>;
    case "A cena":
      return <p>{p.cena}</p>;
    case "Quem é quem":
      return (
        <table>
          <caption className="visualmente-oculto">
            {tituloDoPasso(explicacao, passo)}: correspondência entre a cena e o conceito
          </caption>
          <thead>
            <tr>
              <th scope="col">Na cena</th>
              <th scope="col">No conceito</th>
            </tr>
          </thead>
          <tbody>
            {p.mapeamento.map((linha, i) => (
              <tr key={i}>
                <td data-rotulo="Na cena">{linha.universo}</td>
                <td data-rotulo="No conceito">{linha.tecnico}</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    case "Onde a comparação falha":
      return (
        <ul>
          {p.onde_falha.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      );
    case "Em termos técnicos":
      return <p>{p.reformulacao_tecnica}</p>;
    default:
      return <Transferencia pergunta={p.pergunta_transferencia} passo={passo} />;
  }
}

function Transferencia({
  pergunta,
  passo,
}: {
  pergunta: { pergunta: string; resposta_esperada: string };
  passo: number;
}) {
  const id = `resposta-passo-${passo}`;
  return (
    <>
      <p>{pergunta.pergunta}</p>
      {/* A resposta fica escondida de propósito: ver junto com a pergunta
          anula o efeito da recuperação ativa (DD08). */}
      <details>
        <summary>Mostrar a resposta</summary>
        <p id={id}>{pergunta.resposta_esperada}</p>
      </details>
    </>
  );
}
