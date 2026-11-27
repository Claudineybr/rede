#!/usr/bin/env python3
"""Clona o repo PK e converte: tira a TAG '🕸️ PK', põe '🍿Clau',
renomeia para .html e separa filmes de séries.

Uso: python3 pk_to_clau.py <dir_origem> <dir_destino>
"""
import os
import re
import sys

TAG_ANTIGA = "\U0001F578\uFE0F PK"   # 🕸️ PK
TAG_NOVA = "\U0001F37FClau"          # 🍿Clau


def classificar(base):
    """Retorna 'serie', 'filme' ou None."""
    # Séries: nome termina em _S<num>E<num>  (ex: 100088_S1E1)
    if re.search(r"_S\d+E\d+$", base):
        return "serie"
    # Filmes: nome é só dígitos  (ex: 1000837)
    if re.match(r"^\d+$", base):
        return "filme"
    return None


def converter(src, dst):
    filmes_dir = os.path.join(dst, "filmes")
    series_dir = os.path.join(dst, "series")
    os.makedirs(filmes_dir, exist_ok=True)
    os.makedirs(series_dir, exist_ok=True)

    n_filmes = n_series = n_skip = 0

    for nome in sorted(os.listdir(src)):
        if not nome.endswith(".json"):
            continue

        base = nome[:-5]
        categoria = classificar(base)
        if categoria is None:
            n_skip += 1
            continue

        with open(os.path.join(src, nome), "r", encoding="utf-8") as fh:
            conteudo = fh.read()

        # Troca a TAG em todo o arquivo (title + JSON-LD name)
        conteudo = conteudo.replace(TAG_ANTIGA, TAG_NOVA)

        destino = filmes_dir if categoria == "filme" else series_dir
        with open(os.path.join(destino, base + ".html"), "w", encoding="utf-8") as fh:
            fh.write(conteudo)

        if categoria == "filme":
            n_filmes += 1
        else:
            n_series += 1

    print(f"Filmes: {n_filmes}")
    print(f"Series: {n_series}")
    print(f"Ignorados: {n_skip}")
    return n_filmes, n_series


def main():
    if len(sys.argv) != 3:
        print("Uso: python3 pk_to_clau.py <dir_origem> <dir_destino>", file=sys.stderr)
        sys.exit(2)
    converter(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
