#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Raport kontrolny calej bazy Thai All-in-One.

Uzupelnia tools/validate.py: validate.py odpowiada na pytanie „czy baza jest
poprawna", ten skrypt na pytanie „co w niej wlasciwie jest".

Uruchomienie:  python3 tools/audit.py
"""
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
THAI = re.compile(r"[\u0E00-\u0E7F]")


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as fh:
        return json.load(fh)


def main():
    manifest = load("manifest.json")
    vocab = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "vocabulary"]
    dialog = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "dialogues"]

    records, per_file = [], {}
    for fn in vocab:
        rows = load(fn)["records"]
        per_file[fn] = len(rows)
        records.extend(rows)

    ids = collections.Counter(r["id"] for r in records)
    dup_ids = {k: v for k, v in ids.items() if v > 1}

    no_examples = [r["id"] for r in records if not r.get("examples")]
    no_level = [r["id"] for r in records if not r.get("level")]
    no_phon = [r["id"] for r in records if not r.get("thaiPhonetic")]
    no_tts = [r["id"] for r in records if not THAI.search(r.get("ttsThai", ""))]
    no_tone = [r["id"] for r in records if not r.get("toneGuide")]

    examples = [ex["polish"] for r in records for ex in r.get("examples", [])]
    ex_unique = len(set(examples))

    levels = collections.Counter(r["level"] for r in records)
    registers = collections.Counter(r["register"] for r in records)
    types = collections.Counter(r["type"] for r in records)
    cats = collections.Counter(r["category"] for r in records)

    b1 = [r for r in records if r["level"] == "B1"]
    b1_reactions = [r for r in b1 if r["subcategory"] == "Reakcje"]
    b1_examples = {ex["polish"] for r in b1 for ex in r.get("examples", [])}
    b1_registers = collections.Counter(r["register"] for r in b1)
    slang = [r for r in b1 if "SLANG" in (r.get("notes") or "")]
    b1_src = collections.Counter(r["source"] for r in b1)

    b2 = [r for r in records if r["level"] == "B2"]
    b2_examples = {ex["polish"] for r in b2 for ex in r.get("examples", [])}
    b2_registers = collections.Counter(r["register"] for r in b2)
    b2_src = collections.Counter(r["source"] for r in b2)
    b2_reg_sets = [r for r in b2 if (r.get("notes") or "").startswith("REJESTR ")]
    b2_idioms = [r for r in b2 if "IDIOM" in (r.get("notes") or "")]
    b2_slang = [r for r in b2 if "SLANG" in (r.get("notes") or "")]
    b2_colloc = [r for r in b2 if "KOLOKACJA" in (r.get("notes") or "")]

    dlg_ids, dlg_total, line_total, per_dlg_file = set(), 0, 0, {}
    dlg_levels = collections.Counter()
    for fn in dialog:
        d = load(fn)
        per_dlg_file[fn] = (len(d["records"]), sum(len(x["lines"]) for x in d["records"]))
        for x in d["records"]:
            dlg_ids.add(x["id"])
            dlg_levels[x["level"]] += 1
        dlg_total += len(d["records"])
        line_total += per_dlg_file[fn][1]
    dup_dlg = dlg_total - len(dlg_ids)

    # wyciek pisma tajskiego do pol widocznych
    leaks = 0
    for r in records:
        for k, v in r.items():
            if k == "ttsThai":
                continue
            if isinstance(v, str) and THAI.search(v):
                leaks += 1

    w = lambda label, value: print("  %-42s %s" % (label, value))     # noqa: E731

    print("=" * 64)
    print("RAPORT KONTROLNY BAZY THAI ALL-IN-ONE")
    print("=" * 64)
    print("\n[1] LICZBA REKORDÓW")
    for fn in vocab:
        w(fn, per_file[fn])
    w("RAZEM rekordów słownika", len(records))
    print("\n    wg poziomu:")
    for lv in ("Survival", "A1", "A2", "B1"):
        if lv in levels:
            w("      " + lv, levels[lv])
    print("\n[2] DIALOGI")
    for fn in dialog:
        c, l = per_dlg_file[fn]
        w(fn, "%d dialogów, %d kwestii" % (c, l))
    w("RAZEM dialogów", dlg_total)
    w("RAZEM kwestii", line_total)
    print("\n    wg poziomu:")
    for lv, c in sorted(dlg_levels.items()):
        w("      " + lv, c)

    print("\n[3] KONTROLA SPÓJNOŚCI")
    w("duplikaty ID rekordów", len(dup_ids))
    w("duplikaty ID dialogów", dup_dlg)
    w("rekordy bez przykładów", len(no_examples))
    w("rekordy bez poziomu", len(no_level))
    w("rekordy bez fonetyki", len(no_phon))
    w("rekordy bez opisu tonów", len(no_tone))
    w("rekordy bez ukrytego pola TTS", len(no_tts))
    w("wycieki pisma tajskiego do pól widocznych", leaks)

    print("\n[4] PRZYKŁADY ZDAŃ")
    w("przykładów łącznie", len(examples))
    w("w tym unikalnych", ex_unique)
    w("nowych unikalnych przykładów B1", len(b1_examples))

    print("\n[5] ETAP 4 — POZIOM B1")
    w("rekordów B1", len(b1))
    w("rekordy naturalnych reakcji", len(b1_reactions))
    w("rekordy oznaczone ostrzeżeniem o slangu", len(slang))
    print("\n    rejestr:")
    for reg, c in b1_registers.most_common():
        w("      " + reg, c)
    print("\n    pochodzenie:")
    for s, c in b1_src.most_common():
        w("      " + s[:38], c)

    print("\n[6] ETAP 5 — POZIOM B2")
    w("rekordów B2", len(b2))
    w("nowych unikalnych przykładów B2", len(b2_examples))
    w("wpisy porównujące rejestr (formalny/neutralny/potoczny)", len(b2_reg_sets))
    w("rekordy oznaczone jako IDIOM", len(b2_idioms))
    w("rekordy oznaczone ostrzeżeniem o slangu", len(b2_slang))
    w("rekordy oznaczone jako KOLOKACJA", len(b2_colloc))
    print("\n    rejestr:")
    for reg, c in b2_registers.most_common():
        w("      " + reg, c)
    print("\n    pochodzenie:")
    for s, c in b2_src.most_common():
        w("      " + s[:38], c)

    print("\n[7] CAŁA BAZA — ROZKŁADY")
    print("    rejestr:")
    for reg, c in registers.most_common():
        w("      " + reg, c)
    print("\n    typ rekordu:")
    for t, c in types.most_common():
        w("      " + t, c)
    print("\n    kategorie (10 największych):")
    for c_, n in cats.most_common(10):
        w("      " + c_, n)

    print("\n" + "-" * 64)
    problems = (len(dup_ids) + dup_dlg + len(no_examples) + len(no_level)
                + len(no_phon) + len(no_tts) + leaks)
    print("WYNIK:", "BEZ ZASTRZEŻEŃ" if problems == 0 else "ZNALEZIONO %d PROBLEMÓW" % problems)
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
