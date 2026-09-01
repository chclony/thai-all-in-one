#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dopisuje do bazy wariant potoczny zapisu fonetycznego.

    python3 tools/generators/build-colloquial.py

Co dostaje pole `colloquial`:
  * rekordy należące do ścieżki nauki (132 lekcje) wraz z ich przykładami,
  * wszystkie kwestie wszystkich dialogów,
  * wzorce w grammar.json,
  * wszystkie powyższe również w wariancie żeńskim (genderVariant.female).

ZAKRES — DLACZEGO NIE CAŁA BAZA
-------------------------------
Redukcja jest własnością MOWY CIĄGŁEJ, nie wyrazu. Pojedyncze słowo podane
w izolacji Taj też wymówi formą słownikową — dopiero wpuszczone w zdanie
skraca się i zlewa z sąsiadami. Wariant potoczny ma więc sens tam, gdzie
uczący się ćwiczy słuchanie zdań: w kursie i w dialogach.

Jest też koszt. Pole dla całej bazy (37 640 tekstów) waży 7,7 MB, czyli
o ponad jedną trzecią powiększa każdy plik poziomu — a te dociągane są na
żądanie i ich waga była tematem osobnej sesji. Zakres kursowy to 1,3 MB.

Poza tym zakresem tryb potoczny odtwarza formę słownikową i mówi o tym
wprost w interfejsie. Pełną bazę można wygenerować przełącznikiem --all.

Reguły siedzą w colloquial.py i są współdzielone z walidatorem — walidator
przelicza wariant od nowa i porównuje z zapisanym, więc ręczna zmiana pola
w danych zostanie wykryta jako błąd.

Skrypt jest idempotentny: liczy wszystko od nowa z formy słownikowej.
Wywołany z --dry-run niczego nie zapisuje, tylko pokazuje statystykę.
"""

import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import colloquial as CO   # noqa: E402
import engine             # noqa: E402
import jsonio             # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")

VOCAB = ("survival", "a1-part", "a2-part", "b1-part", "b2-part",
         "core-lexicon", "supplemental")
DIALOGUES = ("dialogues-part",)

stats = collections.Counter()
rule_hits = collections.Counter()
scope_path = collections.Counter()      # osobno: materiał ścieżki nauki i dialogów


def variant(node, count_in_path):
    """Dokłada (albo usuwa) pole colloquial w jednym węźle z fonetyką."""
    ph = node.get("thaiPhonetic")
    if not ph:
        node.pop("colloquial", None)
        return
    built = CO.build(ph, node.get("ttsThai"), engine.polish_read)
    if not built:
        node.pop("colloquial", None)
        stats["bez zmian"] += 1
        return
    node["colloquial"] = built
    stats["z wariantem"] += 1
    if count_in_path:
        scope_path["teksty"] += 1
    for r in built["rules"]:
        rule_hits[r] += 1
        if count_in_path:
            scope_path[r] += 1


def strip(node):
    """Usuwa pole colloquial poza zakresem — skrypt musi być idempotentny
    także po zmianie zakresu albo po przesunięciu rekordu w ścieżce nauki."""
    if isinstance(node, list):
        for item in node:
            strip(item)
        return
    if not isinstance(node, dict):
        return
    node.pop("colloquial", None)
    for key in ("examples", "lines", "patterns", "genderVariant", "female"):
        if key in node:
            strip(node[key])


def walk(node, in_path):
    """Rekurencyjnie obchodzi rekord, przykłady, kwestie i warianty żeńskie."""
    if isinstance(node, list):
        for item in node:
            walk(item, in_path)
        return
    if not isinstance(node, dict):
        return
    if "thaiPhonetic" in node:
        variant(node, in_path)
    for key in ("examples", "lines", "patterns", "genderVariant"):
        if key in node:
            walk(node[key], in_path)
    if "female" in node and isinstance(node.get("female"), dict):
        walk(node["female"], in_path)


def lesson_ids():
    """Identyfikatory rekordów należących do ścieżki nauki (132 lekcje)."""
    path = os.path.join(DATA, "lessons.json")
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as fh:
        rows = json.load(fh).get("records", [])
    ids = set()
    for lesson in rows:
        ids.update(lesson.get("recordIds") or [])
    return ids


def main():
    dry = "--dry-run" in sys.argv
    everything = "--all" in sys.argv
    in_path_ids = lesson_ids()

    files = sorted(f for f in os.listdir(DATA) if f.endswith(".json"))
    touched = []
    for name in files:
        base = name[:-5]
        is_vocab = any(base.startswith(p) for p in VOCAB)
        is_dlg = any(base.startswith(p) for p in DIALOGUES)
        if not (is_vocab or is_dlg or base == "grammar"):
            continue
        path = os.path.join(DATA, name)
        with open(path, encoding="utf-8") as fh:
            payload = json.load(fh)
        for rec in payload.get("records", []):
            in_path = is_dlg or base == "grammar" or (rec.get("id") in in_path_ids)
            if in_path or everything:
                walk(rec, in_path)
            else:
                strip(rec)
        if not dry:
            jsonio.dump(payload, path)
        touched.append(name)

    print("=" * 70)
    print("WARIANT POTOCZNY ZAPISU FONETYCZNEGO" +
          ("  (próba, bez zapisu)" if dry else "") +
          ("  [zakres: CAŁA BAZA]" if everything else "  [zakres: kurs i dialogi]"))
    print("=" * 70)
    print("plików przetworzonych: %d" % len(touched))
    print("tekstów z wariantem:   %d" % stats["z wariantem"])
    print("tekstów bez zmian:     %d" % stats["bez zmian"])
    print("-" * 70)
    print("%-14s %-24s %8s %8s" % ("reguła", "nazwa", "razem", "ścieżka"))
    for rid, label, _desc in CO.RULES:
        print("%-14s %-24s %8d %8d" % (rid, label, rule_hits[rid], scope_path[rid]))
    print("-" * 70)
    print("w materiale ścieżki nauki i dialogów: %d tekstów" % scope_path["teksty"])
    print("Pamiętaj o: python3 tools/build-offline-data.py && python3 tools/validate.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
