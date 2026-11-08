import type { Explanation } from "../api";
import { PARTES } from "./partes";

/**
 * O conteúdo de uma parte da explicação dentro de uma mensagem do chat.
 *
 * Em `tecnica`, qualquer parte mostra a reformulação sem analogia, mantendo
 * a posição — é o que RF04 exige: alternar sem perder o ponto em que se
 * estava.
 */
export function ParteMensagem({
  explicacao,
  parte,
  tecnica,
}: {
  explicacao: Explanation;
  parte: number;
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
        <p className="etiqueta-tecnica">Sem comparação</p>
        <p>{p.reformulacao_tecnica}</p>
      </>
    );
  }

  switch (PARTES[parte - 1]) {
    case "O conceito":
      return <p>{p.conceito}</p>;
    case "A cena":
      return <p>{p.cena}</p>;
    case "Quem é quem":
      // Frases em vez de tabela: tabela não combina com conversa e, a 320px,
      // virava uma pilha de células difícil de seguir.
      return (
        <ul className="lista-correspondencia">
          {p.mapeamento.map((linha, i) => (
            <li key={i}>
              <strong>{linha.universo}</strong>
              <span aria-hidden="true"> → </span>
              <span className="visualmente-oculto">: no conceito, </span>
              {linha.tecnico}
            </li>
          ))}
        </ul>
      );
    case "Onde a comparação não vale":
      return (
        <ul className="lista-limites">
          {p.onde_falha.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      );
    case "Em termos técnicos":
      return <p>{p.reformulacao_tecnica}</p>;
    default:
      return <Transferencia pergunta={p.pergunta_transferencia} />;
  }
}

function Transferencia({
  pergunta,
}: {
  pergunta: { pergunta: string; resposta_esperada: string };
}) {
  return (
    <>
      <p>{pergunta.pergunta}</p>
      {/* A resposta fica escondida de propósito: ver junto com a pergunta
          anula o efeito da recuperação ativa (DD08). */}
      <details className="resposta-escondida">
        <summary>Mostrar a resposta</summary>
        <p>{pergunta.resposta_esperada}</p>
      </details>
    </>
  );
}
