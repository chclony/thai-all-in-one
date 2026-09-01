#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analiza luki leksykalnej — ile słów brakuje do rozumienia mowy potocznej.

Uruchomienie:  python3 tools/gap-analysis.py

Pytanie, na które ten skrypt odpowiada, brzmi: ilu haseł brakuje bazie do tego,
żeby uczący się rozumiał zwykłą rozmowę. Odpowiedź wymaga trzech rzeczy:
modelu pokrycia, listy odniesienia i zliczenia, ile z tej listy baza już ma.

MODEL POKRYCIA
--------------
Pokrycie tekstu przez N najczęstszych haseł opisujemy rozkładem
Zipfa-Mandelbrota: f(r) = C / (r + b)^a, gdzie r to ranga hasła. Parametry
`a` i `b` dobieramy metodą najmniejszych kwadratów do czterech punktów
zaczepienia zmierzonych na korpusach MÓWIONYCH (nie pisanych):

    1 000 haseł -> 85 %      3 000 haseł -> 93 %
    2 000 haseł -> 90 %      5 000 haseł -> 95 %

Te cztery punkty są zgodne z tym, co daje się odczytać z korpusów mowy dla
języków o podobnej strukturze leksykalnej. Mowa potoczna ma pokrycie WYŻSZE
niż pismo przy tej samej liczbie haseł — powtarza się w niej wąski rdzeń
czasowników, zaimków i partykuł. Dlatego liczenie na frekwencji pisanej
zaniżyłoby wymaganie i dałoby fałszywy komfort.

OGRANICZENIE, KTÓRE TRZEBA POWIEDZIEĆ WPROST
--------------------------------------------
Model jest interpolacją między czterema punktami, a nie pomiarem na korpusie
tajskim. Liczby wychodzące z niego są rzędem wielkości, nie wynikiem pomiaru.
Drugie źródło niepewności: „hasło” w tej bazie to jednostka słownikowa, a
tajski składa gęsto — „nám khǎeng” (lód) to dwa hasła albo jedno, zależnie
od decyzji. Liczby wahają się od tego o kilkanaście procent.

Wynik jest więc dobry do odpowiedzi „czy 586 wystarczy” (nie wystarcza,
i to nie o mało), a nie do obietnicy „po 2 137 hasłach zrozumiesz 90 %”.
"""
import json
import os
import sys
import unicodedata
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, os.path.join(ROOT, "tools", "generators"))

LEX_TYPES = {"word", "noun", "verb", "adjective", "adverb"}

# --------------------------------------------------------------- model Zipfa
ANCHORS = [(1000, 0.85), (2000, 0.90), (3000, 0.93), (5000, 0.95)]


def coverage(n, a, b, total=60000):
    """Udział tekstu pokryty przez n najczęstszych haseł."""
    if n <= 0:
        return 0.0
    num = sum(1.0 / (r + b) ** a for r in range(1, int(n) + 1))
    den = sum(1.0 / (r + b) ** a for r in range(1, total + 1))
    return num / den


def fit():
    """Dopasowanie a i b do punktów zaczepienia — przeszukanie siatki."""
    best, best_err = None, 1e9
    a = 0.80
    while a <= 1.40:
        b = 0.0
        while b <= 60.0:
            err = sum((coverage(n, a, b) - c) ** 2 for n, c in ANCHORS)
            if err < best_err:
                best_err, best = err, (a, b)
            b += 1.0
        a += 0.01
    return best


def words_for(target, a, b):
    """Ile haseł potrzeba do zadanego pokrycia."""
    lo, hi = 1, 40000
    while lo < hi:
        mid = (lo + hi) // 2
        if coverage(mid, a, b) < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


# ------------------------------------------------------------------ baza
def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as f:
        return json.load(f)


def norm(s):
    """Zapis bez znaków tonów i bez dywizów — do porównywania haseł."""
    d = unicodedata.normalize("NFD", (s or "").lower())
    d = "".join(c for c in d if not unicodedata.combining(c))
    return d.replace("-", " ").replace("  ", " ").strip()


def main():
    manifest = load("manifest.json")
    vocab = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "vocabulary"]

    records = []
    for fn in vocab:
        records.extend(load(fn)["records"])

    lex = [r for r in records if r["type"] in LEX_TYPES and r.get("syllables")]
    usages = [r for r in records if r["type"] not in LEX_TYPES and r.get("syllables")]

    # warunek dydaktyczny: istnieje zdanie zawierające wszystkie sylaby hasła
    by_syl = defaultdict(list)
    for u in usages:
        for s in set(u["syllables"]):
            by_syl[s].append(u)

    activatable = 0
    for r in lex:
        syls = set(r["syllables"])
        rare = min(syls, key=lambda s: len(by_syl[s]))
        if any(syls <= set(u["syllables"]) for u in by_syl[rare]):
            activatable += 1

    lessons = load("lessons.json")["records"]
    in_path = sum(len(l.get("newWordIds") or []) for l in lessons)

    a, b = fit()

    print("=" * 74)
    print("  ANALIZA LUKI LEKSYKALNEJ — pokrycie mowy potocznej")
    print("=" * 74)
    print("\nModel: Zipf-Mandelbrot f(r) = C / (r + b)^a")
    print("  dopasowane parametry:  a = %.2f   b = %.0f" % (a, b))
    print("  kontrola dopasowania do punktów zaczepienia:")
    for n, c in ANCHORS:
        print("    %5d haseł -> oczekiwane %.1f %%, model daje %.1f %%"
              % (n, c * 100, coverage(n, a, b) * 100))

    print("\nSTAN OBECNY")
    print("  haseł leksykalnych w bazie          %5d  -> pokrycie %.1f %%"
          % (len(lex), coverage(len(lex), a, b) * 100))
    print("  z tego spełnia warunek dydaktyczny  %5d  -> pokrycie %.1f %%"
          % (activatable, coverage(activatable, a, b) * 100))
    print("  wprowadza ścieżka nauki (%d lekcji) %5d -> pokrycie %.1f %%"
          % (len(lessons), in_path, coverage(in_path, a, b) * 100))

    print("\nCELE")
    for target in (0.90, 0.95):
        n = words_for(target, a, b)
        print("  pokrycie %.0f %% wymaga %5d haseł  (brakuje %5d do stanu ścieżki,"
              " %5d do zasobu bazy)"
              % (target * 100, n, max(0, n - in_path), max(0, n - activatable)))

    print("\nROZKŁAD HASEŁ LEKSYKALNYCH — KATEGORIE")
    cnt = Counter(r.get("category") for r in lex)
    allcnt = Counter(r.get("category") for r in records)
    print("  %-26s %8s %8s" % ("kategoria", "hasła", "rekordy"))
    for k, v in sorted(cnt.items(), key=lambda kv: -kv[1]):
        print("  %-26s %8d %8d" % (k, v, allcnt[k]))

    print("\nROZKŁAD HASEŁ LEKSYKALNYCH — POZIOMY")
    for k, v in Counter(r.get("level") for r in lex).most_common():
        print("  %-12s %6d" % (k, v))

    print("\nTYPY REKORDÓW")
    for k, v in Counter(r["type"] for r in records).most_common():
        print("  %-14s %6d" % (k, v))

    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
