# Resultados da avaliação — Etapa 4 (Avaliar)

Data: 09/11/2026 · Versão avaliada: commit `54c6a6d`, com as correções registradas
em `melhorias.md`.

## 1. O que foi feito

| Método | Tipo | Documento | Situação |
|---|---|---|---|
| Avaliação heurística (Nielsen + acessibilidade, carga cognitiva e transparência da IA) | Analítico, por especialista | `avaliacao-heuristica.md` | Concluída |
| Percurso cognitivo com as personas Ana, Rafael e Caio | Analítico, por especialista | `percurso-cognitivo.md` | Concluído |
| Auditoria WCAG 2.2 AA (automatizada e checklist manual) | Analítico, ferramentas + especialista | `auditoria-wcag.md` | Concluída, com itens não verificáveis declarados |
| Teste de usabilidade com 3 a 5 participantes + SUS | Empírico, com usuários | `protocolo-teste.md`, `sus.md` | **Não aplicado no prazo** (ver a seção 4) |

As avaliações analíticas foram feitas por especialista com apoio de IA (Claude,
com a skill Lumen de IHC e acessibilidade) e devem ser revisadas pelos
integrantes do grupo. As evidências estão em `evidencias/`.

## 2. Principais achados

**Avaliação heurística:** 14 problemas, nenhum de severidade 4.

| Severidade | Encontrados | Corrigidos |
|---|---|---|
| 4 — catástrofe | 0 | — |
| 3 — maior | 3 | **3** |
| 2 — menor | 9 | 2 (um em parte) |
| 1 — cosmético | 2 | 1 |

Os três de severidade 3, corrigidos antes de qualquer teste com usuários, como o
método recomenda:

- **P03** — o consentimento mostrava uma nota de desenvolvimento ao usuário;
- **P04** — o menu "Leitura" não indicava que as cores ficavam ali (tarefa T4);
- **P05** — a versão técnica voltava à analogia a cada parte, obrigando o perfil
  do Caio a clicar de novo em todas (DD39).

**Percurso cognitivo:** o caminho das seis tarefas é descobrível pelas três
personas. O achado mais importante não é de interface, e sim de **preparação do
teste**: no modo pré-gravado só existe analogia para "futebol", e os universos
das três personas (série de animação, jogo de tiro tático) recebem a explicação
padrão. Num teste com usuários nessas condições, o valor central do app (a
analogia) não apareceria.

**Auditoria WCAG 2.2 AA:** nenhuma violação nas regras automáticas do axe (A e
AA) em todo o fluxo, nos dois formatos e nos três temas; 13 itens manuais
aprovados, 1 com observação de severidade 1 (hierarquia de títulos), 5 sem
aplicação ou não verificáveis aqui. O estilo vidro mantém o texto das
explicações em contraste AAA (≥ 7:1) no pior ponto do fundo; textos secundários
e links ficam em AA.

## 3. O que a avaliação permite afirmar, e o que não permite

**Permite:** que a interface não tem barreiras graves detectáveis por inspeção;
que as tarefas do teste são executáveis do início ao fim; que o app atende aos
critérios automatizáveis da WCAG 2.2 AA e à maior parte do checklist manual.

**Não permite:** afirmar que o app é fácil de usar para os estudantes, que a
analogia ajuda a aprender, nem que ele é acessível para pessoas com baixa visão.
Essas perguntas só o teste com usuários responde, e a ferramenta automática
cobre apenas parte dos critérios de acessibilidade. Também não há nota SUS: a
nota é a percepção de usuários reais, e não pode ser estimada.

## 4. Limitação: o teste com usuários

O teste de usabilidade com participantes e o questionário SUS, previstos na
proposta do projeto, **não foram aplicados dentro do prazo**. Os instrumentos
estão prontos (`protocolo-teste.md`, atualizado para a interface de chat, e
`sus.md`, na versão brasileira validada). Não foram usados participantes
simulados: dados de usuários inventados não medem nada e não seriam honestos.

Para aplicar o teste, falta:

1. preparar as explicações pré-gravadas para os universos dos participantes
   (perguntados no convite), ou usar a IA com uma cota que aguente as sessões;
2. recrutar de 3 a 5 pessoas de fora do grupo, se possível incluindo uma pessoa
   com baixa visão;
3. aplicar o protocolo e calcular o SUS com
   `scripts/sus_calculator.py` (skill Lumen).

## 5. Próximos passos

Em ordem de prioridade, a partir de `melhorias.md`:

1. Aplicar o teste com usuários e o SUS.
2. Tratar os problemas de severidade 2 registrados: P02 ("Está errada" sem
   motivo nem destino), P06 (progresso invisível para quem enxerga), P07
   (espera da IA sem estimativa), P08 ("Nova conversa" sem confirmação),
   P12 (analogias pré-gravadas), P14 (conteúdo pré-gravado fora do texto de
   referência), P15 (retorno de "Continuar este conteúdo").
3. Ouvir o fluxo com NVDA e TalkBack e testar a fonte do sistema em aparelho.
4. Menu recolhível no celular com texto ampliado (resto de P01).

## Fontes

- Nielsen, J. — heurísticas de usabilidade e escala de severidade.
- Wharton, C. et al. (1994). *The cognitive walkthrough method: a practitioner's guide*.
- W3C. *Web Content Accessibility Guidelines (WCAG) 2.2*, 2023.
- Lourenço, Carmona & Lopes (2022) — SUS em português do Brasil (`sus.md`).
