import { expect, test } from "@playwright/test";
import {
  avancarAte,
  botaoContinuar,
  entrar,
  escrever,
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

  await entrar(page);
  await semViolacoes(page);

  // tudo dentro do chat: assunto e universo escritos com as palavras do aluno (D7)
  await escrever(page, "quero entender TCP");
  await expect(page.getByText(/Combinado, vamos estudar Entrega confiável no TCP/)).toBeVisible();
  // a fala do aluno aparece como mensagem dele
  await expect(page.getByRole("log").getByText("quero entender TCP")).toBeVisible();

  await escrever(page, "futebol");
  await expect(parte(page, 1)).toBeVisible();
  await expect(page.getByRole("status")).toContainText("Explicação pronta");
  await semViolacoes(page);
  await semRolagemHorizontal(page);
});

test("T1b — assunto fora da biblioteca: resposta honesta e sugestões", async ({ page }) => {
  await entrar(page);
  await escrever(page, "fotossíntese");
  await expect(page.getByText(/Ainda não tenho material de referência sobre “fotossíntese”/)).toBeVisible();
  // nunca um beco sem saída: a sugestão leva ao conteúdo que existe
  await page.getByRole("button", { name: /Entrega confiável no TCP/ }).click();
  await expect(page.getByText(/Combinado, vamos estudar/)).toBeVisible();
  // e o foco vai para o campo, onde o aluno escreve o universo
  await expect(page.getByLabel("Universo para a comparação")).toBeFocused();
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

  await page.getByRole("button", { name: "Voltar para a conversa" }).click();
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

  await expect(page.getByRole("heading", { name: "Fora deste conteúdo" })).toBeVisible();
  // a recusa nomeia o conceito atual, em vez de só dizer "não posso"
  await expect(page.getByText(/Só consigo responder sobre/)).toBeVisible();
  // duas saídas explícitas: nunca um beco sem saída (DD05)
  await expect(page.getByRole("button", { name: "Continuar este conteúdo" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Escolher outro conteúdo" })).toBeVisible();
  // e as ações da explicação continuam ao alcance depois da pergunta
  await expect(page.getByRole("button", { name: "Ver versão técnica" })).toBeVisible();
  await semViolacoes(page);
});

test("T6b — pergunta dentro do conceito é respondida", async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);

  await perguntar(page, "o que o receptor devolve quando recebe um segmento?");

  await expect(page.getByRole("heading", { name: "Resposta" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Fora deste conteúdo" })).toHaveCount(0);
});

test("RF09 — trocar de universo de dentro da explicação", async ({ page }) => {
  await entrar(page);
  await pedirExplicacao(page);
  await avancarAte(page, 2);

  await page.getByRole("button", { name: "Trocar universo" }).click();
  await expect(page.getByText(/Qual universo você quer usar agora/)).toBeVisible();
  // o pedido veio do aluno: o foco vai para o campo
  await expect(page.getByLabel("Universo para a comparação")).toBeFocused();
  await semViolacoes(page);

  await escrever(page, "xadrez");

  // o nome novo aparece na conversa, e o que foi lido antes continua lá —
  // é o que permite comparar as duas analogias, que é o motivo de RF09
  await expect(page.getByText(/Agora usando xadrez/)).toBeVisible();
  await expect(page.getByRole("heading", { name: /A cena — parte 2 de 6/ })).toBeVisible();
  // sem explicação escrita à mão para "xadrez", o app mostra a padrão em vez
  // de inventar: é o comportamento do modo Mágico de Oz, e precisa ficar dito
  await expect(page.getByRole("heading", { name: "Explicação padrão" })).toBeVisible();
});

test("D8 — assunto pesquisado na web mostra as fontes antes de explicar", async ({ page }) => {
  // A API do Gemini não roda no teste: a resposta da pesquisa é simulada aqui.
  await page.route("**/v1/assuntos/reconhecer", (rota) =>
    rota.fulfill({
      json: {
        encontrado: true,
        conceito: { slug: "web-arvore-b", title: "Árvore B", discipline: "Pesquisado na web" },
        sugestoes: [],
        pesquisado: true,
        fontes: [
          { titulo: "Árvore B — Wikipédia", url: "https://pt.wikipedia.org/wiki/%C3%81rvore_B" },
          { titulo: "B-tree — CLRS, cap. 18 (resumo)", url: "https://example.edu/btree" },
        ],
        motivo: null,
      },
    }),
  );
  await entrar(page);
  await escrever(page, "árvore B");
  await expect(page.getByText(/Pesquisei sobre Árvore B na web/)).toBeVisible();
  await expect(page.getByRole("link", { name: /Árvore B — Wikipédia/ })).toHaveAttribute(
    "href",
    "https://pt.wikipedia.org/wiki/%C3%81rvore_B",
  );
  await expect(page.getByText(/Combinado, vamos estudar Árvore B/)).toBeVisible();
  await semViolacoes(page);
  await semRolagemHorizontal(page);
});

test("D8 — pesquisa que falha vira mensagem clara, sem detalhe técnico", async ({ page }) => {
  await page.route("**/v1/assuntos/reconhecer", (rota) =>
    rota.fulfill({
      json: {
        encontrado: false,
        conceito: null,
        sugestoes: [{ slug: "tcp-entrega-confiavel", title: "Entrega confiável no TCP (confirmações e janela deslizante)", discipline: "Redes" }],
        pesquisado: false,
        fontes: [],
        motivo: "Não consegui pesquisar esse assunto agora. Tente de novo em instantes.",
      },
    }),
  );
  await entrar(page);
  await escrever(page, "árvore B");
  await expect(page.getByText(/Não consegui pesquisar esse assunto agora/)).toBeVisible();
  await expect(page.getByRole("button", { name: /Entrega confiável no TCP/ })).toBeVisible();
});

test("D9 — referência sem fontes avisa o aluno antes de explicar", async ({ page }) => {
  await page.route("**/v1/assuntos/reconhecer", (rota) =>
    rota.fulfill({
      json: {
        encontrado: true,
        conceito: { slug: "web-redes-p2p", title: "Redes peer-to-peer", discipline: "Escrito pela IA, sem fontes" },
        sugestoes: [],
        pesquisado: true,
        fontes: [],
        motivo: null,
      },
    }),
  );
  await entrar(page);
  await escrever(page, "redes peer to peer");
  await expect(page.getByText(/sem fontes da web/)).toBeVisible();
  await expect(page.getByText(/Combinado, vamos estudar Redes peer-to-peer/)).toBeVisible();
  await semViolacoes(page);
});
