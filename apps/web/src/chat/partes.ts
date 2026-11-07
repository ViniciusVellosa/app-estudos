/**
 * Regras das partes da explicação no chat (RF10, decisões D2 e D3).
 *
 * As seis partes vêm do modelo Teaching-With-Analogies (Glynn, 1991) e estão
 * nos critérios de aceite de RF03. A estrutura fica; o que não aparece na
 * tela é o **vocabulário interno** dela. Ninguém diz "estou no passo 3 de 6"
 * ao explicar algo a um colega, e um aplicativo que fala assim parece a
 * engrenagem de si mesmo.
 *
 * Então: título humano na mensagem, posição dita de duas formas —
 * visualmente pela barra de progresso, e para leitor de tela por um trecho
 * oculto no próprio título, já que a barra é decorativa (DD19).
 */
import type { Explanation } from "../api";

/** O que cada parte entrega, no vocabulário de quem lê. */
export const PARTES = [
  "O conceito",
  "A cena",
  "Quem é quem",
  "Onde a comparação não vale",
  "Em termos técnicos",
  "Para testar se ficou claro",
] as const;

/** A parte 5 já é a versão sem analogia: nela o botão de alternar não cabe. */
export const PARTE_TECNICA = 5;

export function totalDePartes(e: Explanation): number {
  return e.payload ? PARTES.length : 1;
}

/** Título visível da mensagem. Sem numeração: ela vai no rótulo acessível. */
export function tituloDaParte(e: Explanation, n: number): string {
  return e.payload ? PARTES[n - 1] : "Explicação padrão";
}

/**
 * O complemento que só o leitor de tela ouve. A barra de progresso é
 * decorativa (`aria-hidden`), então a posição precisa existir em texto.
 */
export function posicaoDaParte(e: Explanation, n: number): string {
  return e.payload ? ` — parte ${n} de ${PARTES.length}` : "";
}

export function temVersaoTecnica(e: Explanation, n: number): boolean {
  return Boolean(e.payload) && n !== PARTE_TECNICA;
}

/**
 * Ao trocar de universo, a pessoa volta ao mesmo ponto (RF09, DD04).
 * Se o novo universo cair na explicação padrão, que tem uma parte só, o
 * número é limitado ao que existe — em vez de deixar a conversa num ponto
 * inexistente.
 */
export function parteAoTrocarDeUniverso(novo: Explanation, parteAtual: number): number {
  return Math.min(Math.max(parteAtual, 1), totalDePartes(novo));
}
