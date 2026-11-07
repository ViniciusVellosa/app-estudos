import { describe, expect, it } from "vitest";
import type { Explanation } from "../api";
import {
  PASSOS,
  passoAoTrocarDeUniverso,
  temVersaoTecnica,
  tituloDoPasso,
  totalDePassos,
} from "./passos";

const comAnalogia = { payload: {} } as Explanation;
const padrao = { payload: null } as Explanation;

describe("passos da explicação no chat", () => {
  it("a explicação com analogia tem seis passos; a padrão, um só", () => {
    expect(totalDePassos(comAnalogia)).toBe(6);
    expect(totalDePassos(padrao)).toBe(1);
  });

  it("o título diz a posição, para quem não vê a trilha do desktop (DD19)", () => {
    expect(tituloDoPasso(comAnalogia, 3)).toBe(`Passo 3 de 6 — ${PASSOS[2]}`);
    expect(tituloDoPasso(padrao, 1)).toBe("Explicação padrão");
  });

  it("não oferece versão técnica no passo que já é a versão técnica", () => {
    expect(temVersaoTecnica(comAnalogia, 2)).toBe(true);
    expect(temVersaoTecnica(comAnalogia, 5)).toBe(false);
  });

  it("não oferece versão técnica na explicação padrão, que não tem analogia", () => {
    expect(temVersaoTecnica(padrao, 1)).toBe(false);
  });

  it("trocar de universo mantém o passo atual (RF09)", () => {
    expect(passoAoTrocarDeUniverso(comAnalogia, 3)).toBe(3);
  });

  it("trocar para um universo sem explicação personalizada não deixa num passo inexistente", () => {
    expect(passoAoTrocarDeUniverso(padrao, 4)).toBe(1);
  });

  it("antes do primeiro passo, a troca cai no passo 1", () => {
    expect(passoAoTrocarDeUniverso(comAnalogia, 0)).toBe(1);
  });
});
