import { describe, expect, it } from "vitest";
import type { Explanation } from "../api";
import {
  PARTES,
  parteAoTrocarDeUniverso,
  posicaoDaParte,
  temVersaoTecnica,
  tituloDaParte,
  totalDePartes,
} from "./partes";

const comAnalogia = { payload: {} } as Explanation;
const padrao = { payload: null } as Explanation;

describe("partes da explicação no chat", () => {
  it("a explicação com analogia tem seis partes; a padrão, uma só", () => {
    expect(totalDePartes(comAnalogia)).toBe(6);
    expect(totalDePartes(padrao)).toBe(1);
  });

  it("o título da mensagem não mostra a numeração", () => {
    // "Passo 3 de 6 — Quem é quem" é vocabulário interno vazando para a tela
    expect(tituloDaParte(comAnalogia, 3)).toBe(PARTES[2]);
    expect(tituloDaParte(comAnalogia, 3)).not.toMatch(/\d/);
    expect(tituloDaParte(padrao, 1)).toBe("Explicação padrão");
  });

  it("mas a posição continua existindo para quem usa leitor de tela (DD19)", () => {
    // a barra de progresso é decorativa, então a posição tem de estar em texto
    expect(posicaoDaParte(comAnalogia, 3)).toBe(" — parte 3 de 6");
  });

  it("a explicação padrão não anuncia posição, porque tem uma parte só", () => {
    expect(posicaoDaParte(padrao, 1)).toBe("");
  });

  it("não oferece versão técnica na parte que já é a versão técnica", () => {
    expect(temVersaoTecnica(comAnalogia, 2)).toBe(true);
    expect(temVersaoTecnica(comAnalogia, 5)).toBe(false);
  });

  it("não oferece versão técnica na explicação padrão, que não tem analogia", () => {
    expect(temVersaoTecnica(padrao, 1)).toBe(false);
  });

  it("trocar de universo mantém o ponto atual (RF09)", () => {
    expect(parteAoTrocarDeUniverso(comAnalogia, 3)).toBe(3);
  });

  it("trocar para um universo sem explicação personalizada não deixa num ponto inexistente", () => {
    expect(parteAoTrocarDeUniverso(padrao, 4)).toBe(1);
  });

  it("antes da primeira parte, a troca cai na parte 1", () => {
    expect(parteAoTrocarDeUniverso(comAnalogia, 0)).toBe(1);
  });
});
