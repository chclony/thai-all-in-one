#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generuje kopie plików danych w formie skryptów JS, dzięki którym aplikacja
działa także po otwarciu index.html bezpośrednio z dysku (protokół file://).

Powód: przeglądarki blokują fetch() dla adresów file://, ale znacznik <script>
działa bez przeszkód. Każdy plik data/X.json dostaje bliźniaka data/X.js,
który dopisuje swoją zawartość do obiektu window.__THAI_DATA__.

Pliki JSON pozostają źródłem prawdy — pliki JS są generowane i nie należy
ich edytować ręcznie. Uruchom ten skrypt po każdej zmianie w katalogu data/:

    python3 tools/build-offline-data.py
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

HEADER = (
    "/* PLIK GENEROWANY AUTOMATYCZNIE — nie edytuj ręcznie.\n"
    "   Źródło: data/{name}\n"
    "   Generator: tools/build-offline-data.py\n"
    "   Cel: praca aplikacji po otwarciu index.html z dysku (file://). */\n"
)


def main():
    if not os.path.isdir(DATA):
        print("Nie znaleziono katalogu data/", file=sys.stderr)
        return 1

    sources = sorted(f for f in os.listdir(DATA) if f.endswith(".json"))
    if not sources:
        print("Brak plików JSON w katalogu data/", file=sys.stderr)
        return 1

    total_bytes = 0
    print("=" * 58)
    print("GENEROWANIE DANYCH DLA TRYBU file://")
    print("=" * 58)

    for name in sources:
        src = os.path.join(DATA, name)
        with open(src, encoding="utf-8") as fh:
            payload = json.load(fh)

        # separators bez spacji: plik jest tylko do odczytu maszynowego
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

        # Dane wstawiamy jako łańcuch przekazany do JSON.parse, a nie jako
        # literał obiektu JavaScriptu. Silnik parsuje JSON.parse osobną,
        # znacznie szybszą ścieżką — przy plikach rzędu 2 MB różnica na wolnym
        # urządzeniu to kilkaset milisekund. U+2028 i U+2029 są w JSON-ie
        # legalne, a w kodzie JavaScriptu łamią łańcuch, więc je uciekamy.
        literal = json.dumps(body, ensure_ascii=False)
        literal = literal.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")

        out_name = name[:-5] + ".js"
        out_path = os.path.join(DATA, out_name)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(HEADER.format(name=name))
            fh.write("window.__THAI_DATA__ = window.__THAI_DATA__ || {};\n")
            fh.write("window.__THAI_DATA__[%s] = JSON.parse(%s);\n" % (json.dumps(name), literal))

        size = os.path.getsize(out_path)
        total_bytes += size
        print("  %-26s -> %-26s %6.1f kB" % (name, out_name, size / 1024))

    print("-" * 58)
    print("  Wygenerowano %d %s, łącznie %.1f kB"
          % (len(sources),
             "plik" if len(sources) == 1 else "plików",
             total_bytes / 1024))
    print("WYNIK: GOTOWE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
