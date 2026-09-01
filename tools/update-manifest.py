#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wpisuje nowe pliki słownika do manifestu i przelicza liczniki.

    python3 tools/update-manifest.py

Manifest był dotąd pisany ręcznie. Przy czterech nowych plikach i przyroście
o kilka tysięcy rekordów ręczne liczenie przestaje być wykonalne — i jest
dokładnie tym miejscem, w którym baza i jej opis się rozjeżdżają. Skrypt
liczy wszystko z plików, więc rozjazd jest niemożliwy.
"""
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# Sesja N dołożyła lexicon-01..04, sesja O — lexicon-05..12. Lista jest
# jawna, a nie zbierana z katalogu, żeby przypadkowy plik roboczy nie
# wszedł do manifestu i stamtąd do pakietu offline.
NEW_FILES = ["lexicon-%02d.json" % i for i in range(1, 13)]

VERSION = "1.15.0"
UPDATED = "2026-08-26"


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as f:
        return json.load(f)


def main():
    man = load("manifest.json")

    existing = {e["file"] for e in man["dataFiles"]}
    for fn in NEW_FILES:
        recs = load(fn)["records"]
        levels = sorted({r["level"] for r in recs})
        entry = {
            "file": fn,
            "kind": "vocabulary",
            "level": "/".join(levels),
            "count": len(recs),
        }
        if fn in existing:
            for i, e in enumerate(man["dataFiles"]):
                if e["file"] == fn:
                    man["dataFiles"][i] = entry
        else:
            man["dataFiles"].append(entry)

    # --- przeliczenie liczników z plików, nie z pamięci
    # totalRecords liczy WYŁĄCZNIE rekordy słownika. Pliki dialogowe mają
    # własny licznik totalDialogues — wliczenie ich tutaj rozjeżdżało manifest
    # z walidatorem dokładnie o 184.
    total = 0
    per_level = Counter()
    for e in man["dataFiles"]:
        recs = load(e["file"])["records"]
        e["count"] = len(recs)
        if e["kind"] != "vocabulary":
            continue
        total += len(recs)
        for r in recs:
            per_level[r["level"]] += 1

    order = ["Survival", "A1", "A2", "B1", "B2"]
    man["levels"] = {k: per_level[k] for k in order if per_level[k]}
    for k in sorted(per_level):
        if k not in man["levels"]:
            man["levels"][k] = per_level[k]

    man["totalRecords"] = total
    man["version"] = VERSION
    man["updated"] = UPDATED
    man["cacheKey"] = "thai-aio-data-v" + VERSION

    with open(os.path.join(DATA, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)

    print("manifest %s — plików %d, rekordów %d"
          % (VERSION, len(man["dataFiles"]), total))
    for k, v in man["levels"].items():
        print("  %-10s %6d" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
