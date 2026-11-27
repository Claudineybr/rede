#!/usr/bin/env python3
"""Clona o repo PK e converte: tira a TAG '🕸️ PK', põe '🍿Clau',
renomeia para .html e separa filmes de séries.

- Filmes  -> <destino>/oneplayer/<id>.html
- Séries  -> <destino>/series_html/<id>s01e01.html  (padrão da pasta)
Arquivos que já existem no destino NÃO são sobrescritos.

Uso: python3 pk_to_clau.py <dir_origem> <dir_destino>
"""
import os
import re
import sys

TAG_ANTIGA = "\U0001F578\uFE0F PK"   # 🕸️ PK
TAG_NOVA = "\U0001F37FClau"          # 🍿Clau

RE_SERIE = re.compile(r"^(.+)_S(\d+)E(\d+)$")


def nome_destino(base):
    """Retorna (categoria, nome_do_arquivo) ou (None, None) se ignorar."""
    # Séries: nome termina em _S<num>E<num>  (ex: 100088_S1E1)
    m = RE_SERIE.match(base)
    if m:
        ident, temporada, episodio = m.group(1), int(m.group(2)), int(m.group(3))
        # padrão já usado em series_html/: 100010s01e01.html
        nome = f"{ident.lower()}s{temporada:02d}e{episodio:02d}.html"
        return "serie", nome
    # Filmes: nome é só dígitos  (ex: 1000837)
    if re.match(r"^\d+$", base):
        return "filme", base + ".html"
    return None, None


def converter(src, dst):
    pasta_filmes = os.path.join(dst, "oneplayer")
    pasta_series = os.path.join(dst, "series_html")
    os.makedirs(pasta_filmes, exist_ok=True)
    os.makedirs(pasta_series, exist_ok=True)

    novos_filmes = novos_series = existentes = ignorados = 0

    for nome in sorted(os.listdir(src)):
        if not nome.endswith(".json"):
            continue

        categoria, nome_saida = nome_destino(nome[:-5])
        if categoria is None:
            ignorados += 1
            continue

        pasta = pasta_filmes if categoria == "filme" else pasta_series
        destino = os.path.join(pasta, nome_saida)

        if os.path.exists(destino):
            existentes += 1
            continue

        with open(os.path.join(src, nome), "r", encoding="utf-8") as fh:
            conteudo = fh.read()

        # Troca a TAG em todo o arquivo (title + JSON-LD name)
        conteudo = conteudo.replace(TAG_ANTIGA, TAG_NOVA)

        with open(destino, "w", encoding="utf-8") as fh:
            fh.write(conteudo)

        if categoria == "filme":
            novos_filmes += 1
        else:
            novos_series += 1

    print(f"Filmes novos oneplayer/: {novos_filmes}")
    print(f"Series novas series_html/: {novos_series}")
    print(f"Ja existiam (nao sobrescritos): {existentes}")
    print(f"Ignorados: {ignorados}")
    return novos_filmes, novos_series, existentes


def main():
    if len(sys.argv) != 3:
        print("Uso: python3 pk_to_clau.py <dir_origem> <dir_destino>", file=sys.stderr)
        sys.exit(2)
    converter(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
