import AxeBuilder from "@axe-core/playwright";
import { expect, type Page } from "@playwright/test";

export const TCP = "Entrega confiável no TCP (confirmações e janela deslizante)";

/** Varredura automática do axe. Pega parte dos problemas, não todos. */
export async function semViolacoes(page: Page) {
  const resultado = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
    .analyze();
  expect(resultado.violations.map((v) => `${v.id}: ${v.help}`)).toEqual([]);
}

/** `1.4.10 Realinhar (AA)`: nada pode exigir rolagem para o lado. */
export async function semRolagemHorizontal(page: Page) {
  const largura = await page.evaluate(() => document.documentElement.scrollWidth);
  const janela = await page.evaluate(() => window.innerWidth);
  expect(largura).toBeLessThanOrEqual(janela);
}

/**
 * `2.5.8 Tamanho do alvo mínimo (AA)`: 24x24 CSS px em tudo que é clicável.
 * O axe não cobre esse critério, então medimos aqui.
 */
export async function alvosGrandesOSuficiente(page: Page) {
  const pequenos: string[] = [];
  for (const alvo of await page.getByRole("button").all()) {
    if (!(await alvo.isVisible())) continue;
    const caixa = await alvo.boundingBox();
    const nome = (await alvo.textContent())?.trim() ?? "(sem texto)";
    if (!caixa || caixa.width < 24 || caixa.height < 24) {
      pequenos.push(`${nome}: ${caixa?.width}x${caixa?.height}`);
    }
  }
  expect(pequenos).toEqual([]);
}

/** Consentir, informar um universo e chegar à tela de estudo (tarefa T1). */
export async function entrar(page: Page, universo = "futebol") {
  await page.goto("/");
  await page.getByLabel("Li e concordo").check();
  await page.getByRole("button", { name: "Continuar" }).click();
  await page.getByLabel(/Interesse/).fill(universo);
  await page.getByRole("button", { name: "Adicionar interesse" }).click();
  await expect(page.getByRole("status")).toContainText("adicionado");
  await page.getByRole("button", { name: "Começar a estudar" }).click();
}

/** Pedir a explicação e esperar a primeira mensagem do chat. */
export async function pedirExplicacao(page: Page, conceito = TCP) {
  // pelo nome, e não pela posição: a ordem da lista muda quando entram
  // conceitos novos
  await page.getByLabel("O que você quer entender?").selectOption({ label: conceito });
  await page.getByRole("button", { name: "Começar a explicar" }).click();
  await expect(page.getByRole("heading", { name: /Passo 1 de 6/ })).toBeVisible();
}

export async function avancarAte(page: Page, passo: number) {
  for (let n = 2; n <= passo; n++) {
    await page.getByRole("button", { name: "Próximo passo" }).click();
    await expect(page.getByRole("heading", { name: new RegExp(`Passo ${n} de 6`) })).toBeVisible();
  }
}

export async function perguntar(page: Page, texto: string) {
  await page.getByLabel("Sua pergunta sobre este conceito").fill(texto);
  await page.getByRole("button", { name: "Enviar" }).click();
}
