import { expect, test } from "@playwright/test";
import {
  alvosGrandesOSuficiente,
  avancarAte,
  botaoContinuar,
  entrar,
  parte,
  pedirExplicacao,
  perguntar,
  semRolagemHorizontal,
  semViolacoes,
} from "./helpers";

/**
 * Os cuidados de acessibilidade da interface de chat (requisitos.md e
 * decisoes-de-design.md DD09–DD17).
 *
 * Um chat é uma lista que cresce sozinha — o padrão de interface que mais
 * costuma quebrar para quem usa leitor de tela ou ampliação. Cada teste aqui
 * trava uma dessas garantias. O axe não cobre nenhuma delas: ele não sabe se
 * a página rolou sozinha nem se o foco foi roubado.
 */

test('o histórico é uma região viva role="log" e educada', async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);

  const log = page.getByRole("log");
  await expect(log).toHaveAttribute("aria-live", "polite");
  // só adições: alternar a versão técnica altera uma mensagem já lida, e
  // relê-la inteira seria ruído (DD09)
  await expect(log).toHaveAttribute("aria-relevant", "additions");
  await expect(log).toHaveAccessibleName(/Conversa/);
});

test("mensagem nova não rouba o foco nem rola a tela (DD10)", async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);

  const continuar = botaoContinuar(page);
  await continuar.click();
  await expect(parte(page, 2)).toBeVisible();

  // o foco continua onde a pessoa o deixou: o app não o leva para a mensagem
  await expect(continuar).toBeFocused();

  // O clique vai por `dispatchEvent` de propósito: um clique normal do
  // Playwright rola a página sozinho para alcançar o botão, e isso mascararia
  // justamente o que queremos medir — se o APP rola ao receber mensagem.
  const antes = await page.evaluate(() => window.scrollY);
  await continuar.dispatchEvent("click");
  await expect(parte(page, 3)).toBeVisible();
  expect(await page.evaluate(() => window.scrollY)).toBe(antes);
});

test('"Ir para a última mensagem" leva o foco a pedido de quem clicou', async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);
  await avancarAte(page, 2);

  await page.getByRole("button", { name: "Ir para a última mensagem" }).click();
  const focado = await page.evaluate(() => document.activeElement?.tagName);
  expect(focado).toBe("LI");
});

test("a resposta da pergunta de transferência não aparece junto com ela (DD08)", async ({
  page,
}) => {
  await entrar(page);
  await pedirExplicacao(page);
  await avancarAte(page, 6);

  const resposta = page.getByRole("group").getByRole("paragraph");
  await expect(resposta).toBeHidden();
  await page.getByText("Mostrar a resposta").click();
  await expect(resposta).toBeVisible();
});

test("a folha de troca de universo fecha com Esc e devolve o foco (DD16)", async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);

  const abrir = page.getByRole("button", { name: "Trocar universo" });
  await abrir.click();
  await expect(page.getByRole("heading", { name: "Trocar de universo" })).toBeVisible();

  await page.keyboard.press("Escape");
  await expect(page.getByRole("heading", { name: "Trocar de universo" })).toHaveCount(0);
  // o `<dialog>` nativo devolve o foco a quem o abriu (WCAG 2.4.3)
  await expect(abrir).toBeFocused();
});

test("alvos de clique têm pelo menos 24x24 px (WCAG 2.5.8)", async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);
  await avancarAte(page, 3);
  await alvosGrandesOSuficiente(page);
});

test("a 320px com texto enorme, a conversa reflui sem rolagem lateral", async ({ page }) => {
  // 320px equivale a 1280px com 400% de zoom (WCAG 1.4.10)
  await page.setViewportSize({ width: 320, height: 640 });
  await entrar(page);

  await page.getByRole("button", { name: "Leitura" }).click();
  await page.getByLabel("Enorme").check();
  await page.getByLabel(/Alto contraste/).check();
  await page.getByRole("button", { name: "Salvar preferências" }).click();
  await page.getByRole("button", { name: "Estudar" }).click();

  await pedirExplicacao(page);
  await avancarAte(page, 3); // o passo 3 é a tabela, o pior caso para reflow
  await semRolagemHorizontal(page);
  await semViolacoes(page);

  await perguntar(page, "quem ganhou o jogo ontem?");
  await expect(page.getByRole("heading", { name: "Fora deste conceito" })).toBeVisible();
  await semRolagemHorizontal(page);
  await alvosGrandesOSuficiente(page);
});

test("dá para conversar só com o teclado", async ({ page, isMobile }) => {
  test.skip(isMobile, "teste de teclado físico roda no projeto desktop");
  await entrar(page);
  await pedirExplicacao(page);

  // avançar uma parte com o teclado
  await botaoContinuar(page).focus();
  await page.keyboard.press("Enter");
  await expect(parte(page, 2)).toBeVisible();

  // perguntar sem tocar no mouse: o Enter no campo envia o formulário
  await page.getByLabel("Sua pergunta sobre este conceito").focus();
  await page.keyboard.type("o que é a janela?");
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { name: "Resposta" })).toBeVisible();
});

test("a numeração das partes não aparece na tela, mas existe para quem ouve", async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);
  await avancarAte(page, 3);

  // O título visível é só o nome da parte. `toHaveText` não serve aqui:
  // ele devolve o texto inteiro, inclusive o trecho que só o leitor de tela
  // alcança. O que queremos é o que a pessoa enxerga — os nós de texto
  // diretos do título, sem o <span> recortado.
  const titulo = page.getByRole("heading", { name: /parte 3 de 6/ });
  const visivel = await titulo.evaluate((h) =>
    [...h.childNodes]
      .filter((n) => n.nodeType === Node.TEXT_NODE)
      .map((n) => n.textContent)
      .join("")
      .trim(),
  );
  expect(visivel).toBe("Quem é quem");

  // mas o nome acessível carrega a posição, porque a barra de progresso é
  // decorativa e não entra na leitura (DD19)
  await expect(titulo).toHaveAccessibleName("Quem é quem — parte 3 de 6");

  // e nenhum "Passo N de 6" sobrou na interface
  await expect(page.getByText(/Passo \d de \d/)).toHaveCount(0);
});
