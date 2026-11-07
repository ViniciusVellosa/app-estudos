import { expect, test } from "@playwright/test";
import {
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
 * As tarefas do teste de usabilidade, automatizadas.
 *
 * Cada teste aqui corresponde a uma tarefa do protocolo da Etapa 4
 * (`docs/etapa-4-avaliacao/protocolo-teste.md`). Automatizar não substitui o
 * teste com pessoas — mede se o caminho **existe e funciona**, não se é
 * descobrível, que é o que as sessões com participantes respondem.
 *
 * Roda nos dois projetos do Playwright, celular e desktop (RNF07).
 */

test("T1 — chegar à explicação, do consentimento à primeira mensagem", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1, name: "Antes de começar" })).toBeVisible();
  await semViolacoes(page);

  await page.getByLabel("Li e concordo").check();
  await page.getByRole("button", { name: "Continuar" }).click();
  await expect(page.getByRole("heading", { level: 1, name: "Seus interesses" })).toBeFocused();

  await page.getByLabel(/Interesse/).fill("futebol");
  await page.getByRole("button", { name: "Adicionar interesse" }).click();
  await page.getByRole("button", { name: "Começar a estudar" }).click();

  await pedirExplicacao(page);
  await expect(page.getByRole("status")).toContainText("Explicação pronta");
  await semViolacoes(page);
  await semRolagemHorizontal(page);
});

test("T2 — chegar à parte em que a comparação falha", async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);
  await avancarAte(page, 4);

  await expect(
    page.getByRole("heading", { name: /Onde a comparação não vale — parte 4 de 6/ }),
  ).toBeVisible();
  // uma parte por mensagem: a parte 5 ainda não foi revelada (RF10)
  await expect(parte(page, 5)).toHaveCount(0);
  await semViolacoes(page);
});

test("T3 — achar a versão técnica sem perder o ponto atual", async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);
  await avancarAte(page, 3);

  const alternar = page.getByRole("button", { name: "Ver versão técnica" });
  await expect(alternar).toHaveAttribute("aria-pressed", "false");
  await alternar.click();

  // a mesma parte, trocada no lugar (RF04, DD03)
  await expect(parte(page, 3)).toBeVisible();
  await expect(page.getByRole("log").getByText("Sem comparação", { exact: true })).toBeVisible();
  const voltar = page.getByRole("button", { name: "Voltar para a comparação" });
  await expect(voltar).toHaveAttribute("aria-pressed", "true");

  // e volta, no mesmo lugar
  await voltar.click();
  await expect(alternar).toHaveAttribute("aria-pressed", "false");
  await expect(parte(page, 3)).toBeVisible();

  // continuar segue da parte 3 para a 4: alternar não perdeu o lugar, que é
  // o que o critério de aceite de RF04 exige
  await alternar.click();
  await botaoContinuar(page).click();
  await expect(parte(page, 4)).toBeVisible();

  // a parte 3 fica no histórico como foi lida, em versão técnica, e sem
  // botões: mensagem antiga é leitura, não controle
  await expect(page.getByRole("log").getByText("Sem comparação", { exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "Voltar para a comparação" })).toHaveCount(0);
});

test("T4 — ajustar a leitura no meio da explicação, sem perder a conversa", async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);
  await avancarAte(page, 2);

  await page.getByRole("button", { name: "Leitura" }).click();
  await page.getByLabel("Enorme").check();
  await page.getByLabel(/Alto contraste/).check();
  await page.getByRole("button", { name: "Salvar preferências" }).click();
  await expect(page.getByRole("status")).toContainText("salvas");

  await page.getByRole("button", { name: "Estudar" }).click();
  // a conversa continua onde estava: desmontar o chat apagaria o histórico
  await expect(parte(page, 2)).toBeVisible();
  await semRolagemHorizontal(page);
  await semViolacoes(page);
});

test("T5 — reportar que a explicação tem um erro", async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);

  await page.getByRole("button", { name: "Está errada" }).click();
  await expect(page.getByText("Obrigado, vamos conferir.")).toBeVisible();
  await expect(page.getByRole("status")).toContainText("Vamos conferir");
});

test("T6 — perguntar fora do conceito e receber recusa com saída", async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);

  await perguntar(page, "quem ganhou o jogo ontem?");

  await expect(page.getByRole("heading", { name: "Fora deste conceito" })).toBeVisible();
  // a recusa nomeia o conceito atual, em vez de só dizer "não posso"
  await expect(page.getByText(/Só consigo responder sobre/)).toBeVisible();
  // duas saídas explícitas: nunca um beco sem saída (DD05)
  await expect(page.getByRole("button", { name: "Continuar este conceito" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Escolher outro conceito" })).toBeVisible();
  // e as ações da explicação continuam ao alcance depois da pergunta
  await expect(page.getByRole("button", { name: "Ver versão técnica" })).toBeVisible();
  await semViolacoes(page);
});

test("T6b — pergunta dentro do conceito é respondida", async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);

  await perguntar(page, "o que o receptor devolve quando recebe um segmento?");

  await expect(page.getByRole("heading", { name: "Resposta" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Fora deste conceito" })).toHaveCount(0);
});

test("RF09 — trocar de universo de dentro da explicação", async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);
  await avancarAte(page, 2);

  const abrir = page.getByRole("button", { name: "Trocar universo" });
  await abrir.click();
  await expect(page.getByRole("heading", { name: "Trocar de universo" })).toBeVisible();
  // o universo em uso é dito em texto, não só por cor (DD13)
  await expect(page.getByText("em uso agora")).toBeVisible();
  await semViolacoes(page);

  await page.getByLabel("Usar outro universo").fill("xadrez");
  await page.getByRole("button", { name: "Usar este universo" }).click();

  // o nome novo aparece na conversa, e o que foi lido antes continua lá —
  // é o que permite comparar as duas analogias, que é o motivo de RF09
  await expect(page.getByText(/Agora usando xadrez/)).toBeVisible();
  await expect(page.getByRole("heading", { name: /A cena — parte 2 de 6/ })).toBeVisible();
  // sem explicação escrita à mão para "xadrez", o app mostra a padrão em vez
  // de inventar: é o comportamento do modo Mágico de Oz, e precisa ficar dito
  await expect(page.getByRole("heading", { name: "Explicação padrão" })).toBeVisible();
  // a folha fechou sozinha depois da escolha
  await expect(page.getByRole("heading", { name: "Trocar de universo" })).toHaveCount(0);
});
