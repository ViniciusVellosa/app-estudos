#!/usr/bin/env python3
"""Cria um novo projeto a partir do projeto-base do Dédalo.

Uso:
    python3 scripts/novo_projeto.py <pasta-destino> [--nome "Nome do App"]

Copia assets/starter/app-estudos para a pasta de destino (que precisa estar
vazia ou não existir), troca o nome do app e lembra os próximos passos.
Nunca sobrescreve arquivos existentes.
"""
import argparse
import shutil
import sys
from pathlib import Path

STARTER = Path(__file__).resolve().parent.parent / "assets" / "starter" / "app-estudos"
DEFAULT_NAME = "Estudos do Seu Jeito"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("destino")
    ap.add_argument("--nome", default=DEFAULT_NAME)
    args = ap.parse_args()

    dest = Path(args.destino).expanduser().resolve()
    if dest.exists() and any(dest.iterdir()):
        print(f"A pasta {dest} já tem arquivos. Escolha uma pasta vazia.")
        return 1
    shutil.copytree(STARTER, dest, dirs_exist_ok=True)

    if args.nome != DEFAULT_NAME:
        for rel in ["apps/web/index.html", "apps/web/src/App.tsx"]:
            path = dest / rel
            path.write_text(path.read_text(encoding="utf-8").replace(DEFAULT_NAME, args.nome),
                            encoding="utf-8")

    print(f"Projeto criado em {dest}\n")
    print("Próximos passos:")
    print("  1. cd", dest)
    print("  2. git init && git add . && git commit -m 'chore: projeto-base'")
    print("  3. cp .env.example .env   (troque POSTGRES_PASSWORD)")
    print("  4. docker compose up --build")
    print("     sem Docker: veja 'Rodar sem Docker' no README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
