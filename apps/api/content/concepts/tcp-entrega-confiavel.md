---
slug: tcp-entrega-confiavel
title: Entrega confiável no TCP (confirmações e janela deslizante)
discipline: Redes de Computadores
reviewed_by: "PREENCHER: nome de quem revisou"
reviewed_at: "PREENCHER: data"
aliases: [tcp, protocolo tcp, entrega confiável, transmissão confiável, janela deslizante, confirmação, confirmações, ack, retransmissão, número de sequência, controle de erros, camada de transporte]
key_terms: [segmento, confirmação, ACK, janela, número de sequência, retransmissão]
# Armadilhas: frases que descrevem o protocolo "pare-e-espere", não o TCP.
# Os padrões são aplicados ao texto normalizado (minúsculas, sem acentos).
forbidden_patterns:
  - "(so|somente|apenas) (manda|envia|transmite)[^.]{0,60}depois de (confirmar|receber a confirmacao)"
  - "um (pacote|segmento) (de cada vez|por vez)"
  - "espera (cada|a) confirmacao (antes|para)"
---
O TCP oferece entrega confiável sobre uma rede que pode perder, duplicar ou
reordenar pacotes. Cada segmento enviado carrega um número de sequência que
identifica a posição dos seus bytes no fluxo de dados. O receptor devolve uma
confirmação (ACK) informando o próximo número de sequência que espera receber.

O remetente não precisa esperar a confirmação de cada segmento antes de enviar
o próximo. Ele pode ter vários segmentos em trânsito ao mesmo tempo, até o
limite da janela. A janela é a quantidade de dados que pode estar enviada e
ainda não confirmada. Quando chegam confirmações, a janela desliza e novos
segmentos podem ser enviados.

Se a confirmação de um segmento não chega dentro do tempo limite, o remetente
faz a retransmissão desse segmento. O receptor usa os números de sequência
para colocar os dados na ordem correta e descartar duplicatas.

O tamanho da janela também é ajustado pelo controle de fluxo, que evita
sobrecarregar o receptor, e pelo controle de congestionamento, que evita
sobrecarregar a rede.
