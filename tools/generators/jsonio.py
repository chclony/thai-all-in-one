#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zapis plików danych w formacie przyjętym w projekcie.

Pliki data/*.json są zapisywane z wcięciem 1 — tak wyglądają od pierwszej
sesji i tak porównuje je walidator z kopiami dla trybu file://.

Jest jednak wyjątek. Wcięcie rozbija każdą tablicę na osobne wiersze, więc
techniczne tablice krótkie i liczbowe („ttsSplit”: [2, 6, 3, 4]) kosztowałyby
po kilkadziesiąt bajtów samych znaków nowej linii. Przy 51 tysiącach tekstów
to były cztery megabajty powietrza w plikach dociąganych na żądanie.

Dlatego tablice wymienione w ONE_LINE składamy z powrotem w jeden wiersz.
Treść JSON-a jest identyczna — zmienia się wyłącznie formatowanie.
"""

import json
import re

# Klucze, których tablice mają zostać w jednym wierszu.
#
# „s”, „ids” i „weights” pochodzą z coverage.json (sesja R). To jest ten sam
# przypadek co ttsSplit, tylko większy: korpus pokrycia ma kilkanaście tysięcy
# kwestii, a każda z nich niesie tablicę numerów haseł długości jednej kwestii.
# Z wcięciem 1 plik ma kilka megabajtów samych znaków nowej linii i wcięć,
# w jednym wierszu — kilkaset kilobajtów. Treść jest identyczna.
ONE_LINE = ("ttsSplit", "rules", "s", "ids", "weights")

_PATTERNS = [
    re.compile(r'("%s": )\[\s*([^\[\]{}]*?)\s*\]' % key, re.S)
    for key in ONE_LINE
]


def _collapse(text):
    def fix(match):
        inner = " ".join(part.strip() for part in match.group(2).split())
        inner = re.sub(r",\s*", ", ", inner)
        return match.group(1) + "[" + inner + "]"
    for pattern in _PATTERNS:
        text = pattern.sub(fix, text)
    return text


def dump(payload, path):
    text = json.dumps(payload, ensure_ascii=False, indent=1)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(_collapse(text))
        fh.write("\n")
