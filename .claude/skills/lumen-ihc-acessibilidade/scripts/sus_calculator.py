#!/usr/bin/env python3
"""
Calculadora do SUS (System Usability Scale).

Uso:
    python3 sus_calculator.py respostas.csv
    python3 sus_calculator.py respostas.csv --json

Formato do CSV: uma linha por participante, 10 colunas com as respostas
(1 a 5) na ordem dos itens Q1..Q10. Uma primeira coluna de identificação
é opcional (detectada se houver 11 colunas). Cabeçalho é opcional.

Pontuação (Brooke, 1996):
    itens ímpares  -> resposta - 1
    itens pares    -> 5 - resposta
    soma x 2,5     -> escore de 0 a 100

Interpretação incluída:
    - média de referência: 68 (Sauro, 2011)
    - escala de notas "curva" de Sauro & Lewis (2016)
    - adjetivos de Bangor, Kortum & Miller (2009) (aproximação por faixas)
    - faixas de aceitabilidade de Bangor et al. (2008)
    - subescalas de Lewis & Sauro (2009): Usabilidade (itens 1,2,3,5,6,7,8,9)
      e Aprendizibilidade (itens 4 e 10), reescaladas para 0-100. Uso
      exploratório: Lewis & Sauro (2017) recomendam relatar o escore geral.

O SUS não é diagnóstico: mostra o quanto, não o porquê. Combine com
observação de tarefas (teste de usabilidade) para saber o que corrigir.
"""
import csv
import json
import math
import statistics
import sys

# Escala curva de Sauro & Lewis (2016), "Quantifying the User Experience", 2ª ed.
CURVED_GRADES = [
    (84.1, "A+"), (80.8, "A"), (78.9, "A-"), (77.2, "B+"), (74.1, "B"),
    (72.6, "B-"), (71.1, "C+"), (65.0, "C"), (62.7, "C-"), (51.7, "D"),
    (0.0, "F"),
]

# Adjetivos de Bangor, Kortum & Miller (2009, JUS 4(3)): médias de SUS por
# adjetivo = 12,5 / 20,3 / 35,7 / 50,9 / 71,4 / 85,5 / 90,9. Os cortes abaixo
# são os pontos médios entre médias vizinhas — orientação, não corte oficial.
ADJECTIVES = [
    (88.2, "Melhor imaginável"), (78.5, "Excelente"), (61.2, "Bom"),
    (43.3, "OK / Razoável"), (28.0, "Ruim"), (16.4, "Péssimo"),
    (0.0, "Pior imaginável"),
]

# Faixas de aceitabilidade (Bangor et al., 2008): >70 aceitável,
# 50-70 marginal, <50 não aceitável.
def acceptability(score):
    if score > 70:
        return "Aceitável"
    if score >= 50:
        return "Marginalmente aceitável"
    return "Não aceitável"

# t crítico bicaudal 95% para gl pequenos (n-1); acima de 30 usa 1,96 aprox.
T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365,
       8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160,
       14: 2.145, 15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093,
       20: 2.086, 25: 2.060, 30: 2.042}


def t_crit(df):
    if df in T95:
        return T95[df]
    if df > 30:
        return 1.96
    keys = sorted(k for k in T95 if k <= df)
    return T95[keys[-1]]


def grade(score, table):
    for cut, label in table:
        if score >= cut:
            return label
    return table[-1][1]


def score_participant(resp):
    if len(resp) != 10:
        raise ValueError(f"esperava 10 respostas, recebi {len(resp)}: {resp}")
    for r in resp:
        if r < 1 or r > 5:
            raise ValueError(f"resposta fora da escala 1-5: {resp}")
    contrib = [(r - 1) if i % 2 == 0 else (5 - r) for i, r in enumerate(resp)]
    total = sum(contrib) * 2.5
    learn_items = [contrib[3], contrib[9]]            # itens 4 e 10
    usab_items = [c for i, c in enumerate(contrib) if i not in (3, 9)]
    usability = sum(usab_items) * (100 / 32)          # 8 itens x 4 pontos
    learnability = sum(learn_items) * (100 / 8)       # 2 itens x 4 pontos
    return total, usability, learnability


def read_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(2048)
        f.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        for line in csv.reader(f, dialect):
            if not line or all(not c.strip() for c in line):
                continue
            cells = [c.strip() for c in line]
            pid = None
            if len(cells) == 11:
                pid, cells = cells[0], cells[1:]
            try:
                nums = [int(float(c)) for c in cells]
            except ValueError:
                continue  # cabeçalho
            rows.append((pid or f"P{len(rows) + 1}", nums))
    return rows


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    rows = read_csv(sys.argv[1])
    if not rows:
        sys.exit("Nenhuma linha válida encontrada.")
    results = []
    for pid, resp in rows:
        t, u, l = score_participant(resp)
        results.append({"participante": pid, "sus": t, "usabilidade": round(u, 1),
                        "aprendizibilidade": round(l, 1)})
    scores = [r["sus"] for r in results]
    n = len(scores)
    mean = statistics.mean(scores)
    sd = statistics.stdev(scores) if n > 1 else 0.0
    margin = t_crit(n - 1) * sd / math.sqrt(n) if n > 1 else float("nan")
    summary = {
        "n": n,
        "media": round(mean, 1),
        "desvio_padrao": round(sd, 1),
        "ic95": [round(max(0, mean - margin), 1), round(min(100, mean + margin), 1)] if n > 1 else None,
        "nota_curva_sauro_lewis": grade(mean, CURVED_GRADES),
        "adjetivo_bangor_aprox": grade(mean, ADJECTIVES),
        "aceitabilidade_bangor_2008": acceptability(mean),
        "acima_da_media_68": mean > 68,
        "media_usabilidade": round(statistics.mean(r["usabilidade"] for r in results), 1),
        "media_aprendizibilidade": round(statistics.mean(r["aprendizibilidade"] for r in results), 1),
    }
    if "--json" in sys.argv:
        print(json.dumps({"participantes": results, "resumo": summary},
                         ensure_ascii=False, indent=2))
        return
    print("Participante   SUS    Usab.  Aprend.")
    for r in results:
        print(f"{r['participante']:<12} {r['sus']:6.1f} {r['usabilidade']:6.1f} {r['aprendizibilidade']:7.1f}")
    print("-" * 40)
    print(f"n = {n} | média = {summary['media']} | DP = {summary['desvio_padrao']}")
    if summary["ic95"]:
        print(f"IC 95%: {summary['ic95'][0]} a {summary['ic95'][1]}")
    print(f"Nota (escala curva Sauro & Lewis): {summary['nota_curva_sauro_lewis']}")
    print(f"Adjetivo aproximado (Bangor et al.): {summary['adjetivo_bangor_aprox']}")
    print(f"Aceitabilidade (Bangor et al., 2008): {summary['aceitabilidade_bangor_2008']}")
    print(f"Acima da média de referência (68)? {'sim' if summary['acima_da_media_68'] else 'não'}")
    print("Subescalas Usab./Aprend. são exploratórias: Lewis & Sauro (2017) "
          "recomendam relatar o escore geral.")
    if n < 5:
        print("Atenção: com menos de 5 participantes o intervalo de confiança é muito largo.")


if __name__ == "__main__":
    main()
