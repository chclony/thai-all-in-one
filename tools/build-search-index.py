#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generuje data/search-index.json — lekki indeks całej bazy.

Po co: pełne pliki poziomów ważą ponad 21 MB. Wczytanie ich przy starcie
zajmuje na wolnym telefonie kilka sekund i blokuje wątek na czas parsowania.
Indeks zawiera tylko to, co jest potrzebne, żeby hasło ZNALEŹĆ i pokazać
na liście: identyfikator, polskie znaczenie, fonetykę, poziom, kategorię,
typ, częstotliwość, trudność i nazwę pliku, w którym leży pełny rekord.

Pełny rekord — z przykładami, uwagami i danymi dla syntezatora mowy — dociąga
się dopiero wtedy, gdy użytkownik faktycznie otworzy hasło albo wejdzie na
ekran, który potrzebuje całych rekordów.

Format rekordu to tablica, nie obiekt — nazwy pól powtórzone 10 755 razy
zajmowałyby więcej niż same dane:

  [id, polish, thaiPhonetic, pronunciationPolish, femPhonetic, level,
   category, type, frequency, difficulty, fileIndex]

Pismo tajskie (ttsThai) do indeksu NIE trafia — tak samo jak nie trafia
do żadnego innego miejsca widocznego dla użytkownika.

PODZIAŁ NA CZĘŚCI (sesja O)
===========================

Baza urosła z 15 285 do 20 792 rekordów, a indeks z 2,7 do 3,6 MB. Pomiar
z dławieniem procesora x4 pokazał, gdzie leży koszt:

    pobranie 3,6 MB   865 ms
    JSON.parse         77 ms
    budowa obiektów    33 ms

Wąskim gardłem jest TRANSFER, nie przetwarzanie. Wniosek jest praktyczny:
nie ma sensu optymalizować parsowania ani formatu rekordu — trzeba przestać
ściągać przy starcie rzeczy, które przy starcie nie są potrzebne.

Indeks jest więc dzielony po poziomach na dwie części:

    search-index.json         Survival + A1  — CZOŁO, wczytywane przed startem
    search-index-rest.json    A2 + B1 + B2   — reszta, dociągana w tle

Czoło wystarcza pierwszemu ekranowi (zwrot dnia, liczniki, podpowiedzi
powtórek dla początkującego). Reszta rusza natychmiast po pierwszym renderze
i wpada zwykle zanim użytkownik zdąży wejść do słownika; gdyby nie zdążyła,
`DB.ensureIndex()` na nią poczeka.

Dlaczego podział po poziomach, a nie po równych kawałkach: kolejność
poziomów to kolejność, w jakiej materiał jest komukolwiek potrzebny.
Uczący się na A1 może przez tydzień nie dotknąć wpisów B2, a osoba na B2
i tak dociąga wszystko przy pierwszym wejściu do słownika. Podział na
równe paczki dałby ten sam rozmiar czoła, ale czoło zawierałoby losową
mieszankę i pierwszy ekran musiałby czekać na resztę.

Dlaczego dwie części, a nie pięć: każda część to osobne żądanie i osobna
pozycja w pamięci podręcznej trybu offline. Przy pięciu plikach zysk na
czole jest już znikomy (Survival+A1 to i tak najmniejsze poziomy), a koszt
stały rośnie pięciokrotnie.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def main():
    manifest = load("manifest.json")
    vocab = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "vocabulary"]
    dialog_files = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "dialogues"]

    files = list(vocab)
    rows = []
    for fi, fn in enumerate(files):
        for r in load(fn)["records"]:
            fem = ((r.get("genderVariant") or {}).get("female") or {}).get("thaiPhonetic") or ""
            rows.append([
                r["id"],
                r.get("polish", ""),
                r.get("thaiPhonetic", ""),
                r.get("pronunciationPolish", ""),
                fem,
                r.get("level", ""),
                r.get("category", ""),
                r.get("type", ""),
                int(r.get("frequency") or 0),
                int(r.get("difficulty") or 0),
                fi,
            ])

    # Dialogi indeksujemy osobno i płytko — na liście dialogów wystarczy tytuł.
    dlg_rows = []
    for fi, fn in enumerate(dialog_files):
        for d in load(fn)["records"]:
            dlg_rows.append([
                d["id"],
                d.get("title", ""),
                d.get("level", ""),
                d.get("category", ""),
                len(d.get("lines", [])),
                fi,
            ])

    # Czoło indeksu — poziomy, od których zaczyna każdy uczący się.
    HEAD_LEVELS = {"Survival", "A1"}
    head_rows = [r for r in rows if r[5] in HEAD_LEVELS]
    rest_rows = [r for r in rows if r[5] not in HEAD_LEVELS]

    payload = {
        "file": "search-index.json",
        "count": len(head_rows),
        "totalRecords": len(rows),
        "parts": ["search-index-rest.json"],
        "headLevels": sorted(HEAD_LEVELS),
        "fields": ["id", "polish", "thaiPhonetic", "pronunciationPolish",
                   "femPhonetic", "level", "category", "type", "frequency",
                   "difficulty", "fileIndex"],
        "files": files,
        "dialogueFields": ["id", "title", "level", "category", "lines", "fileIndex"],
        "dialogueFiles": dialog_files,
        "dialogues": dlg_rows,
        "records": head_rows,
    }

    out = os.path.join(DATA, "search-index.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, separators=(",", ":"))

    rest = {
        "file": "search-index-rest.json",
        "count": len(rest_rows),
        "of": "search-index.json",
        "records": rest_rows,
    }
    out_rest = os.path.join(DATA, "search-index-rest.json")
    with open(out_rest, "w", encoding="utf-8") as fh:
        json.dump(rest, fh, ensure_ascii=False, separators=(",", ":"))

    size = os.path.getsize(out)
    size_rest = os.path.getsize(out_rest)
    print("  search-index.json          %d haseł (czoło), %d dialogów, %.1f kB"
          % (len(head_rows), len(dlg_rows), size / 1024))
    print("  search-index-rest.json     %d haseł (reszta), %.1f kB"
          % (len(rest_rows), size_rest / 1024))
    print("  RAZEM                      %d haseł, %.1f kB"
          % (len(rows), (size + size_rest) / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
