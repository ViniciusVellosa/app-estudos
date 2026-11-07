/**
 * Regras dos passos da explicação no chat (RF10, decisões D2 e D3).
 *
 * Ficam separadas do componente porque são decisões de produto, não de
 * desenho de tela — e porque assim dá para testá-las sem montar o React.
 */
import type { Explanation } from "../api";

/** Os seis passos do modelo Teaching-With-Analogies adaptado. */
export const PASSOS = [
  "O conceito",
  "A cena",
  "Quem é quem",
  "Onde a comparação falha",
  "Em termos técnicos",
  "Teste o que você entendeu",
] as const;

/** O passo 5 já é a versão sem analogia: nele o botão de alternar não cabe. */
export const PASSO_TECNICO = 5;

export function totalDePassos(e: Explanation): number {
  return e.payload ? PASSOS.length : 1;
}

export function tituloDoPasso(e: Explanation, n: number): string {
  if (!e.payload) return "Explicação padrão";
  return `Passo ${n} de ${PASSOS.length} — ${PASSOS[n - 1]}`;
}

/**
 * Onde faz sentido oferecer "Ver versão técnica" (RF04, DD03).
 *
 * Só na explicação com analogia, e nunca no passo que já É a versão técnica:
 * um botão que não muda nada custa um clique e ensina a pessoa a desconfiar
 * dos botões.
 */
export function temVersaoTecnica(e: Explanation, n: number): boolean {
  return Boolean(e.payload) && n !== PASSO_TECNICO;
}

/**
 * Ao trocar de universo, o aluno volta ao mesmo passo (RF09, DD04).
 * Se o novo universo cair na explicação padrão, que tem um passo só, o
 * número é limitado ao que existe — em vez de deixar a conversa num passo
 * inexistente.
 */
export function passoAoTrocarDeUniverso(novo: Explanation, passoAtual: number): number {
  return Math.min(Math.max(passoAtual, 1), totalDePassos(novo));
}
