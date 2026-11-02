import { useState } from "react";
import type { Explanation } from "../api";

type Props = {
  explanation: Explanation;
  neutralText: string | null;
  onShowNeutral: () => void;
  onFeedback: (kind: "util" | "errada" | "confusa") => void;
  feedbackSent: boolean;
};

/**
 * Mostra a explicação nos seis passos, em blocos curtos com títulos
 * (navegáveis por leitor de tela). A explicação sem analogia está sempre a um
 * toque (diretriz de controle do usuário e de carga cognitiva).
 */
export function ExplanationView({ explanation, neutralText, onShowNeutral, onFeedback, feedbackSent }: Props) {
  const [showNeutral, setShowNeutral] = useState(!explanation.personalized);
  const [showAnswer, setShowAnswer] = useState(false);
  const p = explanation.payload;

  function toggleNeutral() {
    if (!showNeutral) onShowNeutral();
    setShowNeutral(!showNeutral);
  }

  return (
    <article aria-labelledby="titulo-explicacao">
      <h2 id="titulo-explicacao">Explicação</h2>

      {explanation.notice && <p className="aviso">{explanation.notice}</p>}
      {explanation.provider.startsWith("llm") && (
        <p className="dica">Texto adaptado por inteligência artificial a partir de um conteúdo revisado.</p>
      )}

      {p && (
        <div className="acoes">
          <button type="button" className="secundario" aria-pressed={showNeutral} onClick={toggleNeutral}>
            {showNeutral ? "Voltar para a explicação com analogia" : "Ver explicação sem analogia"}
          </button>
        </div>
      )}

      {showNeutral || !p ? (
        <section aria-labelledby="t-neutra">
          <h3 id="t-neutra">Explicação padrão</h3>
          {(neutralText ?? explanation.neutral_text ?? "")
            .split(/\n\s*\n/)
            .map((par, i) => (
              <p key={i}>{par}</p>
            ))}
        </section>
      ) : (
        <>
          <section className="passo" aria-labelledby="t1">
            <h3 id="t1">1. O conceito</h3>
            <p>{p.conceito}</p>
          </section>
          <section className="passo" aria-labelledby="t2">
            <h3 id="t2">2. A cena</h3>
            <p>{p.cena}</p>
          </section>
          <section className="passo" aria-labelledby="t3">
            <h3 id="t3">3. Quem é quem</h3>
            <table>
              <caption className="visualmente-oculto">Correspondência entre a cena e o conceito técnico</caption>
              <thead>
                <tr>
                  <th scope="col">Na cena</th>
                  <th scope="col">No conceito</th>
                </tr>
              </thead>
              <tbody>
                {p.mapeamento.map((row, i) => (
                  <tr key={i}>
                    <td data-rotulo="Na cena">{row.universo}</td>
                    <td data-rotulo="No conceito">{row.tecnico}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
          <section className="passo" aria-labelledby="t4">
            <h3 id="t4">4. Onde a comparação falha</h3>
            <ul>
              {p.onde_falha.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </section>
          <section className="passo" aria-labelledby="t5">
            <h3 id="t5">5. Agora em termos técnicos</h3>
            <p>{p.reformulacao_tecnica}</p>
          </section>
          <section className="passo" aria-labelledby="t6">
            <h3 id="t6">6. Teste o que você entendeu</h3>
            <p>{p.pergunta_transferencia.pergunta}</p>
            <button type="button" className="secundario" aria-expanded={showAnswer} onClick={() => setShowAnswer(!showAnswer)}>
              {showAnswer ? "Esconder resposta" : "Mostrar resposta"}
            </button>
            {showAnswer && <p>{p.pergunta_transferencia.resposta_esperada}</p>}
          </section>
        </>
      )}

      {explanation.id !== null && (
        <section className="passo" aria-labelledby="t-avaliar">
          <h3 id="t-avaliar">Essa explicação ajudou?</h3>
          {feedbackSent ? (
            <p role="status">Obrigado! Sua avaliação foi registrada.</p>
          ) : (
            <div className="acoes">
              <button type="button" className="secundario" onClick={() => onFeedback("util")}>Ajudou</button>
              <button type="button" className="secundario" onClick={() => onFeedback("confusa")}>Ficou confusa</button>
              <button type="button" className="perigo" onClick={() => onFeedback("errada")}>Tem um erro</button>
            </div>
          )}
        </section>
      )}
    </article>
  );
}
