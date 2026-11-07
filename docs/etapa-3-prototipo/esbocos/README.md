# Esboços de baixa fidelidade — Etapa 3

Cinco telas, cada uma num arquivo com o quadro de **celular (320 px)** e o de
**desktop (1280 px)** lado a lado, mais uma legenda numerada que liga cada
marca a um requisito, uma persona ou um critério WCAG.

| Arquivo | Tela | Requisitos |
|---|---|---|
| [`e1-tela-inicial.svg`](e1-tela-inicial.svg) | Escolher o conceito e o universo | RF02, RF03, RNF07 |
| [`e2-chat-explicacao.svg`](e2-chat-explicacao.svg) | Chat com a explicação, um passo por mensagem | RF10, D3 |
| [`e3-trocar-universo.svg`](e3-trocar-universo.svg) | Trocar de universo de dentro da explicação | RF09, D4 |
| [`e4-versao-tecnica.svg`](e4-versao-tecnica.svg) | Versão técnica sem perder o passo atual | RF04, D2 |
| [`e5-pergunta-fora-do-conceito.svg`](e5-pergunta-fora-do-conceito.svg) | Pergunta fora do conceito e "não sei" | RF11, D5, D6 |

As decisões que esses esboços registram estão explicadas, uma a uma, em
[`../decisoes-de-design.md`](../decisoes-de-design.md).

## Por que são de baixa fidelidade mesmo sendo digitais

Baixa fidelidade não quer dizer "feito à mão": quer dizer **pouco compromisso
com a aparência final**, para que a discussão fique na estrutura e no fluxo.
Por isso aqui não há cor, tipografia escolhida, ícone nem imagem — o texto
corrido aparece como barras cinzas e só os elementos interativos têm rótulo
escrito. Quem olha discute onde fica o botão e o que ele faz, não se o azul
está bom.

O custo dessa escolha é conhecido: wireframe em tela parece mais "pronto" do
que rascunho a lápis, e quem revisa tende a criticar menos. Compensamos
deixando explícito, no rodapé de cada quadro, que é esboço datado de 07/11/2026.

## A ordem real do processo

O repositório já tinha um app funcionando antes desta etapa, com os seis
passos numa única tela. **Isso precisa ficar registrado com honestidade**, e
vale separar dois casos:

| Tela | Veio antes ou depois do código? |
|---|---|
| e1 — inicial | **Depois.** Documenta o que já existia, com os ajustes de rótulo |
| e2, e3, e4, e5 — chat, troca de universo, versão técnica e recusa | **Antes.** Nada disso existe no código. Estes esboços são projeto, não documentação |

As quatro telas novas vieram das três divergências registradas na seção 6 dos
Cenários (Etapa 2), confrontadas com as decisões D1 a D6 de 07/11/2026. É a
iteração que a ISO 9241-210:2019 pede no seu princípio (4): o cenário mostrou
que o protótipo não servia, e o protótipo mudou.

## Como os arquivos foram gerados

Os SVG saem de um script, para que os dez quadros tenham a mesma grade, as
mesmas medidas e o mesmo peso de traço. O script está no diretório de trabalho
desta sessão, não no repositório: o artefato da etapa é o SVG, que abre em
qualquer navegador, no Word e no editor de slides.

Para inserir num documento ou num slide, abra o `.svg` e use diretamente — é
vetorial, então não embaça ao ampliar.

## Fontes

- **HOUDE, S.; HILL, C.** What do prototypes prototype? In: *Handbook of
  Human-Computer Interaction*. Elsevier, 1997.
- **ISO 9241-210:2019** — Ergonomia da interação humano-sistema, parte 210:
  design centrado no ser humano, princípio (4) processo iterativo.
- **ROSSON, M. B.; CARROLL, J. M.** *Usability Engineering.* Morgan Kaufmann,
  2002 — a divergência entre cenário de atividade e protótipo como motor do
  redesenho.
- **W3C.** *Web Content Accessibility Guidelines (WCAG) 2.2*, 2023.
