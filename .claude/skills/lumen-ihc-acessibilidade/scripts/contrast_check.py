#!/usr/bin/env python3
"""
Verificador de contraste WCAG 2.x (relação de luminância relativa).

Uso:
    python3 contrast_check.py "#1A1A1A" "#FFFFFF"
    python3 contrast_check.py --palette paleta.json

paleta.json: lista de pares {"nome": "...", "texto": "#hex", "fundo": "#hex",
             "grande": false, "componente": false}

Critérios verificados:
    1.4.3  Contraste mínimo (AA): 4,5:1 texto normal; 3:1 texto grande
    1.4.6  Contraste melhorado (AAA): 7:1 texto normal; 4,5:1 texto grande
    1.4.11 Contraste não textual (AA): 3:1 para componentes e gráficos
Texto grande = pelo menos 18pt (24px) ou 14pt (~18,66px) em negrito.

Fórmula: (L1 + 0,05) / (L2 + 0,05), com L = luminância relativa sRGB.
Observação: o WCAG 3 (em rascunho) discute outro modelo (APCA); este script
segue a fórmula normativa do WCAG 2.2.
"""
import json
import sys


def channel(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color):
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    if len(h) != 6:
        raise ValueError(f"cor inválida: {hex_color}")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def evaluate(fg, bg, large=False, component=False):
    r = ratio(fg, bg)
    out = {"texto": fg, "fundo": bg, "relacao": round(r, 2)}
    if component:
        out["1.4.11 (AA, 3:1)"] = r >= 3
    else:
        out["1.4.3 AA"] = r >= (3 if large else 4.5)
        out["1.4.6 AAA"] = r >= (4.5 if large else 7)
    return out


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    if args[0] == "--palette":
        with open(args[1], encoding="utf-8") as f:
            pairs = json.load(f)
        for p in pairs:
            res = evaluate(p["texto"], p["fundo"], p.get("grande", False),
                           p.get("componente", False))
            flags = ", ".join(f"{k}: {'passa' if v else 'FALHA'}"
                              for k, v in res.items() if isinstance(v, bool))
            print(f"{p.get('nome', '?'):<28} {res['relacao']:>5}:1  {flags}")
        return
    fg, bg = args[0], args[1]
    large = "--grande" in args
    comp = "--componente" in args
    res = evaluate(fg, bg, large, comp)
    print(f"{fg} sobre {bg}: {res['relacao']}:1")
    for k, v in res.items():
        if isinstance(v, bool):
            print(f"  {k}: {'passa' if v else 'FALHA'}")


if __name__ == "__main__":
    main()
