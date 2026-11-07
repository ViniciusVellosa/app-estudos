# Dados da pesquisa

As respostas vieram de um formulário eletrônico **sem identificação** (sem nome,
e-mail ou telefone; ver o plano de pesquisa, seção 5.3). O cuidado aqui é um só:
o que foi prometido no texto de apresentação tem que valer na planilha.

## 1. Nome e telefone não entram

Nem no nome do arquivo, nem em coluna, nem dentro do texto. Cada pessoa vira um
código: **R01, R02…** para quem respondeu o questionário, **P1, P2…** para as
conversas opcionais.

Se alguém mencionar outra pessoa na resposta ("aí a Marina me explicou"), troque
por "[colega]".

## 2. Áudio não entra

Se alguém responder por mensagem de voz, transcreva o conteúdo para a planilha e
**apague o áudio**. Voz identifica a pessoa, e nenhuma pseudonimização resolve isso.

O mesmo vale para print de conversa: a captura mostra nome e foto de perfil.
**Não salve print aqui.**

## 3. O que pode ficar nesta pasta

| Pode | Não pode |
|---|---|
| `respostas-anonimizado.csv` — a planilha tabulada, com códigos | Áudio, vídeo, print de conversa |
| `P1-notas.md` — anotações das conversas opcionais | Lista de contatos ou telefones |

O `.gitignore` do projeto já barra o lado direito nesta pasta: passam apenas
arquivos `.md` e CSV com sufixo `-anonimizado`. É rede de segurança, não
substituto da conferência — confira o arquivo antes de salvar.

## Descarte

O convite promete uma data de descarte. Cumpra:

- **Apagar até:** 09/11/2026, como informado no texto de apresentação do formulário

Descartar inclui a planilha de respostas do Google Forms e o próprio formulário, não só este CSV. Se o CSV for enviado ao GitHub, apagá-lo depois não o remove do histórico. Por isso o `.gitignore` **ignora todo o conteúdo desta pasta, exceto este README** — o CSV de respostas fica só na sua máquina.

---

**Fontes:** Res. CNS 510/2016, art. 17 (sigilo e destino dos dados); LGPD
(Lei 13.709/2018), art. 11 (dado sensível) e art. 18 (direito à eliminação).
