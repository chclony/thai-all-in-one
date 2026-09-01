#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Etap 2 — sprzatanie artefaktow jezykowych z etapu 1.

README generatorow ostrzegal, ze rekordy szablonowe etapu 1 powstaly z iloczynu
kartezjanskiego wzorzec x slownik, przez co czesc polskich hasel brzmi sztucznie
(sztandarowy przyklad: „troche za urocze"). Ten skrypt:

  1. usuwa z a1-part-02.json wskazane rekordy, ktorych POLSKA strona jest
     nienaturalna (tajska konstrukcja jest poprawna, ale nie da sie jej sensownie
     oddac po polsku dla tych konkretnych slow),
  2. w ich miejsce dopisuje tyle samo rekordow rdzennych z rezerwy etapu 2,
     dzieki czemu plik nadal ma dokladnie 1000 pozycji,
  3. ujednoznacznia hasla, ktore po polsku wygladaly identycznie, choc znacza
     co innego (np. „wolny" = powolny vs „wolny" = niezajety),
  4. przelicza liczniki.

Skrypt jest idempotentny — powtorne uruchomienie nie znajduje juz nic do zmiany.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Builder, strip_tones                    # noqa: E402
from lex_a1_stage2 import CORE2S                           # noqa: E402
from stage2 import (DATA, VOCAB_FILES, SRC_CORE, load, save,  # noqa: E402
                    make_example, refresh_counters)

# Rekordy do usuniecia: (polskie haslo, fonetyka) — para jednoznacznie wskazuje rekord.
DROP = [
    ("trochę za kiepskie", "yâe pai nòi"),
    ("trochę za smaczne", "à-ròi pai nòi"),
    ("trochę za ładne", "sǔai pai nòi"),
    ("trochę za urocze", "nâa rák pai nòi"),
    ("trochę za tanie", "thùuk pai nòi"),
    ("trochę za czyste", "saàat pai nòi"),
    ("trochę za nowe", "mài pai nòi"),
    ("trochę za zmęczone", "nùeai pai nòi"),
    ("trochę za głodne", "hǐw pai nòi"),
    ("trochę za najedzone", "ìm pai nòi"),
    ("trochę za spragnione", "hǐw náam pai nòi"),
    ("trochę za chore", "mâi sabaai pai nòi"),
    ("trochę za szczęśliwe", "dii jai pai nòi"),
    ("trochę za smutne", "sǐa jai pai nòi"),
    ("trochę za zdenerwowane", "kròot pai nòi"),
    ("trochę za przestraszone", "klua pai nòi"),
    ("trochę za znudzone", "bùea pai nòi"),
    ("trochę za fajne", "sanùk pai nòi"),
    ("trochę za bezpieczne", "plàwt phai pai nòi"),
    ("trochę za wolne", "wâang pai nòi"),
]

# Ujednoznacznienie hasel, ktore po polsku dublowaly sie co do znaku.
RENAME = [
    ("bardzo wolne", "cháa mâak", "bardzo powolne"),
    ("nie wolne", "mâi cháa", "nie powolne"),
    ("Czy to jest wolne?", "cháa mǎi khráp", "Czy to jest powolne?"),
    ("trochę za wolne", "cháa pai nòi", "trochę za powolne"),
    ("bardzo wolne", "wâang mâak", "całkiem wolne (niezajęte)"),
    ("nie wolne", "mâi wâang", "zajęte (nie ma wolnych)"),
    ("Gdzie jest toaleta?", "hâwng náam yùu thîi nǎi", "Gdzie jest toaleta? (nieformalnie)"),
    ("Czy w pobliżu jest bankomat?", "thǎew níi mii tûu ee-thii-em mǎi",
     "Czy w pobliżu jest bankomat? (nieformalnie)"),
]


def main():
    part2 = load("a1-part-02.json")
    records = part2["records"]
    by_key = {(r["polish"], r["thaiPhonetic"]): r for r in records}

    # --------------------------------------------------------- usuwanie
    drop_ids = set()
    missing = []
    for pl, ph in DROP:
        rec = by_key.get((pl, ph))
        if rec is None:
            missing.append(pl)
        else:
            drop_ids.add(rec["id"])

    # zadne inne haslo nie moze wskazywac na usuwany rekord
    all_records = []
    for fn in VOCAB_FILES:
        all_records.extend(load(fn)["records"])
    for r in all_records:
        for ref in r.get("relatedWords", []):
            if ref in drop_ids:
                raise SystemExit("Rekord %s wskazuje na usuwany %s — przerywam." % (r["id"], ref))

    kept = [r for r in records if r["id"] not in drop_ids]
    removed = len(records) - len(kept)

    # --------------------------------------------------------- uzupelnienie z rezerwy
    builder = Builder()
    seen_polish = set()
    for r in all_records:
        if r["id"] in drop_ids:
            continue
        prefix, num = r["id"].rsplit("-", 1)
        builder.counter[prefix] = max(builder.counter.get(prefix, 0), int(num))
        builder.ids.add(r["id"])
        builder.seen_key.add((strip_tones(r["polish"]).lower(), r["ttsThai"]))
        seen_polish.add(strip_tones(r["polish"]).lower())

    reserve_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reserve-stage3.json")
    reserve = []
    if os.path.exists(reserve_path):
        reserve = [r["polish"] for r in json.load(open(reserve_path, encoding="utf-8"))["records"]]
    core_by_pl = {row[0]: row for row in CORE2S}

    added = []
    still_reserved = []
    for pl in reserve:
        if len(added) >= removed:
            still_reserved.append(pl)
            continue
        row = core_by_pl.get(pl)
        if row is None or strip_tones(pl).lower() in seen_polish:
            still_reserved.append(pl)
            continue
        p, ph, th, cat, sub, rtype, freq, note, literal, ex = row
        rec = builder.make("A1", p, ph, th, cat, sub, rtype,
                           sorted({cat.split()[0].lower(), sub.split()[0].lower(), "słownictwo"}),
                           freq=freq, notes=note, literal=literal,
                           register="uprzejmy" if ("khráp" in ph or "khâ" in ph) else "neutralny",
                           examples=[make_example(ex, ph, th)])
        if rec is None:
            still_reserved.append(pl)
            continue
        rec["source"] = SRC_CORE
        seen_polish.add(strip_tones(p).lower())
        kept.append(rec)
        added.append(p)

    if len(kept) != part2["count"]:
        raise SystemExit("Po wymianie plik ma %d rekordow zamiast %d."
                         % (len(kept), part2["count"]))

    part2["records"] = kept
    part2["count"] = len(kept)
    save("a1-part-02.json", part2)

    with open(reserve_path, "w", encoding="utf-8") as fh:
        json.dump({"note": "Hasla gotowe, odlozone na etap 3 (limit A1 wyczerpany).",
                   "count": len(still_reserved),
                   "records": [{"polish": p} for p in still_reserved]},
                  fh, ensure_ascii=False, indent=1)

    # --------------------------------------------------------- ujednoznacznienie
    renamed = 0
    for fn in VOCAB_FILES:
        data = load(fn)
        touched = False
        for r in data["records"]:
            for pl, ph, new_pl in RENAME:
                if r["polish"] == pl and r["thaiPhonetic"] == ph:
                    r["polish"] = new_pl
                    touched = True
                    renamed += 1
        if touched:
            save(fn, data)

    counts, final, dlg = refresh_counters()

    print("=" * 58)
    print("SPRZATANIE ARTEFAKTOW JEZYKOWYCH")
    print("=" * 58)
    print("  usuniete rekordy nienaturalne %5d" % removed)
    print("  dopisane rekordy z rezerwy    %5d" % len(added))
    print("  ujednoznacznione hasla        %5d" % renamed)
    print("  pozostalo w rezerwie          %5d" % len(still_reserved))
    if missing:
        print("  (juz wczesniej usuniete: %s)" % ", ".join(missing[:5]))
    print("-" * 58)
    for fn in VOCAB_FILES:
        print("  %-26s %5d" % (fn, counts[fn]))
    print("  %-26s %5d" % ("RAZEM rekordow", len(final)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
