#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mapa migracji postępu — data/progress-migration.json.

    python3 tools/generators/progress_map.py

PO CO TO JEST
=============

Sesja O przebudowała ścieżkę: 314 lekcji po ~3,7 hasła zamieniło się w 333
lekcje po ~9. Dziewięćdziesiąt pięć identyfikatorów przetrwało (patrz
lessons.py, sekcja o zgodności wstecznej), reszta lekcji jest nowa —
materiałowo zwykle spadkobierczyni dwóch starych naraz.

Gdyby zostawić to bez migracji, użytkownik, który zaliczył sto lekcji,
zobaczyłby po aktualizacji kurs otwarty na lekcji pierwszej. Zapisany stan
by nie zniknął — po prostu wskazywałby identyfikatory, których w nowej
ścieżce nie ma.

CO ZAWIERA PLIK
===============

Wyłącznie to, czego przeglądarka nie ma skąd wziąć: **skład starych lekcji**.
Skład nowych leży już w `lessons.json`, który i tak jest wczytywany.

    { "version", "generated",
      "legacy":  { "lesson-001": ["id-hasła", ...], ... },
      "legacyOrder": ["lesson-001", ...],
      "direct":  { "stary-id": "nowy-id", ... } }

`direct` to lekcje, które zachowały identyfikator — dla nich migracja jest
przepisaniem stanu jeden do jednego. Reszta idzie przez przeliczenie po
hasłach, co robi js/progress-migration.js.

Plik waży kilkadziesiąt kilobajtów, więc jest wczytywany zawsze razem
z pozostałymi plikami wsparcia. Wersja z lazy-fetch odpadła: w trybie
file:// (aplikacja otwarta z dysku) fetch nie działa, a dokładanie osobnej
ścieżki tylko dla migracji byłoby drugim mechanizmem ładowania danych.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data")

LEGACY = "lessons-legacy.json"
OUT = "progress-migration.json"


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as f:
        return json.load(f)


def main():
    legacy_path = os.path.join(DATA, LEGACY)
    if not os.path.exists(legacy_path):
        sys.stderr.write("Brak %s — nie ma z czego migrować. "
                         "Uruchom najpierw generators/lessons.py.\n" % LEGACY)
        return 1

    legacy = load(LEGACY)
    current = load("lessons.json")
    manifest = load("manifest.json")

    legacy_words = {}
    legacy_order = []
    for L in legacy["records"]:
        legacy_order.append(L["id"])
        legacy_words[L["id"]] = list(L.get("newWordIds") or [])

    direct = {}
    for L in current["records"]:
        if L.get("legacyId"):
            direct[L["legacyId"]] = L["id"]

    payload = {
        "file": OUT,
        "version": manifest.get("version"),
        "generated": manifest.get("updated"),
        "legacyCount": len(legacy_order),
        "currentCount": current["count"],
        "directCount": len(direct),
        "description": ("Skład lekcji starej ścieżki oraz mapa identyfikatorów, "
                        "które przetrwały przebudowę. Wykorzystuje to "
                        "js/progress-migration.js przy pierwszym uruchomieniu "
                        "po aktualizacji."),
        "legacyOrder": legacy_order,
        "legacy": legacy_words,
        "direct": direct,
        "records": [],
    }

    out_path = os.path.join(DATA, OUT)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    size = os.path.getsize(out_path) / 1024.0
    print("Zapisano %s: %d starych lekcji, %d haseł, %d identyfikatorów "
          "zachowanych, %.1f kB"
          % (OUT, len(legacy_order),
             sum(len(v) for v in legacy_words.values()), len(direct), size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
