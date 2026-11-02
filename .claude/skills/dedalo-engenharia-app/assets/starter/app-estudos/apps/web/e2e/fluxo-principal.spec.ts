import AxeBuilder from "@axe-core/playwright";
import { expect, test, type Page } from "@playwright/test";

const TCP = "Entrega confiável no TCP (confirmações e janela deslizante)";

// Fluxo das tarefas do teste de usabilidade: consentir, informar interesse,
// pedir explicação, alternar para a explicação neutra, aumentar a fonte.

async function semViolacoes(page: Page) {
  const resultado = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
    .analyze();
  expect(resultado.violations.map((v) => `${v.id}: ${v.help}`)).toEqual([]);
}

async function semRolagemHorizontal(page: Page) {
  const largura = await page.evaluate(() => document.documentElement.scrollWidth);
  const janela = await page.evaluate(() => window.innerWidth);
  expect(largura).toBeLessThanOrEqual(janela);
}

test("aluno consente, informa interesse e recebe a explicação nos seis passos", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1, name: "Antes de começar" })).toBeVisible();
  await semViolacoes(page);

  await page.getByLabel("Li e concordo").check();
  await page.getByRole("button", { name: "Continuar" }).click();

  await expect(page.getByRole("heading", { level: 1, name: "Seus interesses" })).toBeFocused();
  await page.getByLabel(/Interesse/).fill("Futebol");
  await page.getByRole("button", { name: "Adicionar interesse" }).click();
  await expect(page.getByRole("status")).toContainText("adicionado");
  await page.getByRole("button", { name: "Começar a estudar" }).click();

  // escolha o conceito pelo nome: a ordem da lista muda quando entram conceitos novos
  await page.getByLabel("O que você quer entender?").selectOption({ label: TCP });
  await page.getByRole("button", { name: "Explicar" }).click();
  await expect(page.getByRole("heading", { name: "4. Onde a comparação falha" })).toBeVisible();
  await expect(page.getByRole("status")).toContainText("Explicação pronta");
  await semViolacoes(page);
  await semRolagemHorizontal(page);

  await page.getByRole("button", { name: "Ver explicação sem analogia" }).click();
  await expect(page.getByRole("heading", { name: "Explicação padrão" })).toBeVisible();
});

test("texto ampliado e alto contraste continuam acessíveis e sem rolagem lateral", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 640 }); // equivale a 1280px com 400% de zoom (WCAG 1.4.10)
  await page.goto("/");
  await page.getByLabel("Li e concordo").check();
  await page.getByRole("button", { name: "Continuar" }).click();
  await page.getByLabel(/Interesse/).fill("futebol");
  await page.getByRole("button", { name: "Adicionar interesse" }).click();
  await page.getByRole("button", { name: "Começar a estudar" }).click();

  await page.getByRole("button", { name: "Leitura" }).click();
  await page.getByLabel("Enorme").check();
  await page.getByLabel(/Alto contraste/).check();
  await page.getByRole("button", { name: "Salvar preferências" }).click();
  await expect(page.getByRole("status")).toContainText("salvas");

  await page.getByRole("button", { name: "Estudar" }).click();
  await page.getByLabel("O que você quer entender?").selectOption({ label: TCP });
  await page.getByRole("button", { name: "Explicar" }).click();
  await expect(page.getByRole("heading", { name: "3. Quem é quem" })).toBeVisible();
  await semRolagemHorizontal(page);
  await semViolacoes(page);
});

test("dá para usar só com o teclado", async ({ page, isMobile }) => {
  test.skip(isMobile, "teste de teclado físico roda no projeto desktop");
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1, name: "Antes de começar" })).toBeVisible();
  await page.keyboard.press("Tab");
  await expect(page.getByRole("link", { name: "Pular para o conteúdo" })).toBeFocused();
  // marca o consentimento e avança só com Tab, Espaço e Enter
  await page.getByLabel("Li e concordo").focus();
  await page.keyboard.press("Space");
  await page.keyboard.press("Tab");
  await expect(page.getByRole("button", { name: "Continuar" })).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { level: 1, name: "Seus interesses" })).toBeFocused();
  await page.keyboard.press("Tab");
  await expect(page.getByLabel(/Interesse/)).toBeFocused();
  await page.keyboard.type("futebol");
  await page.keyboard.press("Enter"); // envia o formulário
  await expect(page.getByRole("status")).toContainText("adicionado");
});
