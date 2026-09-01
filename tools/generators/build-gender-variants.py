#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dopisuje do bazy warianty żeńskie form zależnych od płci mówiącego.

    python3 tools/generators/build-gender-variants.py

Co robi:
  * rekordy słownika — dodaje opcjonalne pole genderVariant.female
    (fonetyka, zapis polski, opis tonów, ukryte dane TTS),
  * przykłady w tablicy examples — to samo,
  * dialogi — oznacza płeć ról (roleGender) i każdej kwestii (speakerGender),
    kwestiom ról bez ustalonej płci dokłada genderVariant.female,
    kwestie ról o ustalonej płci doprowadza do formy zgodnej z rolą,
  * wzorce w grammar.json i przykłady w pronunciation.json — to samo co rekordy.

Treść domyślna rekordu pozostaje formą męską — to rozszerzenie schematu,
nie zmiana. Starsza wersja aplikacji czyta bazę tak jak dotąd.

Skrypt jest idempotentny: ponowne uruchomienie przelicza warianty od nowa
na podstawie treści męskiej.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gender_forms as GF  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")

# --- płeć ról w dialogach ---------------------------------------------------
# Oznaczamy tylko role, w których płeć wynika wprost z nazwy — kelnerka jest
# kobietą, kelner mężczyzną. Role opisane rzeczownikiem rodzaju męskiego,
# ale w praktyce bezosobowym (Turysta, Klient, Pasażer, Lekarz, Pracownik),
# zostają „any” i podążają za ustawieniem użytkownika.
ROLE_FEMALE = {
    "Kelnerka", "Sprzedawczyni", "Recepcjonistka", "Farmaceutka", "Kasjerka",
    "Masażystka", "Przewodniczka", "Współlokatorka", "Urzędniczka", "Znajoma",
    "Nowa znajoma", "Sekretarka", "Partnerka", "Księgowa", "Sąsiadka", "Tajka",
}
ROLE_MALE = {
    "Kelner", "Sprzedawca", "Recepcjonista", "Farmaceuta", "Kasjer",
    "Policjant", "Konduktor", "Ochroniarz", "Znajomy", "Znajomy A",
    "Znajomy B", "Kolega", "Kolega z pracy", "Przyjaciel", "Sąsiad",
    "Współlokator", "Urzędnik",
}

NOTE_CHAN = ("Forma żeńska — kobieta mówi chǎn zamiast phǒm oraz khâ zamiast khráp. "
             "chǎn to zaimek codzienny, dobry w rozmowie na mieście i wśród znajomych; "
             "w urzędzie albo rozmowie służbowej kobieta powie dì-chǎn.")
NOTE_DICHAN = ("Forma żeńska — kobieta mówi dì-chǎn zamiast phǒm oraz khâ zamiast khráp. "
               "dì-chǎn to zaimek formalny, właściwy w urzędzie, banku i rozmowie służbowej; "
               "w rozmowie swobodnej wystarczy chǎn.")
NOTE_PARTICLE = ("Forma żeńska — kobieta kończy tę wypowiedź cząstką khâ "
                 "(w pytaniu khá) zamiast męskiego khráp.")
NOTE_MARK = "Forma żeńska —"

stats = {
    "records": 0, "recordsWithVariant": 0, "examples": 0, "examplesWithVariant": 0,
    "dialogues": 0, "dialoguesWithRoleGender": 0, "lines": 0, "linesWithVariant": 0,
    "linesFixedFemale": 0, "linesFixedMale": 0, "notes": 0,
    "grammar": 0, "pronunciation": 0, "lexicon": 0, "labelsRemoved": 0,
}


def clean(variant):
    """Usuwa pola pomocnicze przed zapisem."""
    return {k: v for k, v in variant.items() if not k.startswith("_")}


def add_note(rec, variant):
    """Dopisuje wyjaśnienie różnicy do pola notes (raz, bez powielania)."""
    note = rec.get("notes") or ""
    if NOTE_MARK in note:
        return
    if variant.get("_usesPronoun"):
        extra = NOTE_DICHAN if variant.get("_pronoun") == GF.DICHAN else NOTE_CHAN
    else:
        extra = NOTE_PARTICLE
    rec["notes"] = (note + " " + extra).strip() if note else extra
    stats["notes"] += 1


def process_record(rec):
    rec.pop("genderVariant", None)
    rec.pop("genderLexicon", None)
    reg = rec.get("register", "neutralny")
    stats["records"] += 1

    # Hasło o samej formie („ja (mężczyzna)”) uczy jednej konkretnej postaci
    # i nie podlega przełączaniu — razem z przykładami, które je powtarzają.
    if GF.is_gender_lexicon(rec.get("polish", "")):
        rec["genderLexicon"] = True
        stats["lexicon"] += 1
        for ex in rec.get("examples", []) or []:
            stats["examples"] += 1
            ex.pop("genderVariant", None)
        return

    variant = GF.build_variant(rec, reg)
    if variant:
        rec["genderVariant"] = {"female": clean(variant)}
        stats["recordsWithVariant"] += 1
        add_note(rec, variant)
    for ex in rec.get("examples", []) or []:
        stats["examples"] += 1
        ex.pop("genderVariant", None)
        clean_pl = GF.strip_speaker_label(ex.get("polish", ""))
        if clean_pl != ex.get("polish", ""):
            ex["polish"] = clean_pl
            stats["labelsRemoved"] += 1
        ev = GF.build_variant(ex, reg)
        if ev:
            ex["genderVariant"] = {"female": clean(ev)}
            stats["examplesWithVariant"] += 1


def role_gender(name):
    if name in ROLE_FEMALE:
        return "female"
    if name in ROLE_MALE:
        return "male"
    return "any"


def process_dialogue(dlg):
    stats["dialogues"] += 1
    roles = dlg.get("roles", {})
    rg = {k: role_gender(v) for k, v in roles.items()}
    dlg["roleGender"] = rg
    if any(v != "any" for v in rg.values()):
        stats["dialoguesWithRoleGender"] += 1

    for line in dlg.get("lines", []):
        stats["lines"] += 1
        line.pop("genderVariant", None)
        g = rg.get(line.get("role"), "any")
        line["speakerGender"] = g
        if g == "female":
            # Scenariusz przesądza — kwestia ma brzmieć po kobiecemu od razu.
            if GF.has_male_form(line.get("thaiPhonetic", "")):
                GF.to_female_fixed(line)
                stats["linesFixedFemale"] += 1
        elif g == "male":
            if GF.has_female_form(line.get("thaiPhonetic", "")):
                for key, kind in (("thaiPhonetic", "ph"), ("pronunciationPolish", "pl"),
                                  ("ttsThai", "th"), ("toneGuide", "tone")):
                    if line.get(key):
                        line[key] = GF.to_male(line[key], kind)
                stats["linesFixedMale"] += 1
        else:
            variant = GF.build_variant(line)
            if variant:
                line["genderVariant"] = {"female": clean(variant)}
                stats["linesWithVariant"] += 1


def process_support(node, register="neutralny"):
    """grammar.json / pronunciation.json — te same reguły, płytko."""
    n = 0
    if isinstance(node, dict):
        if isinstance(node.get("thaiPhonetic"), str):
            node.pop("genderVariant", None)
            node.pop("genderLexicon", None)
            if GF.is_gender_lexicon(node.get("polish", "")):
                node["genderLexicon"] = True
                return n
            v = GF.build_variant(node, register)
            if v:
                node["genderVariant"] = {"female": clean(v)}
                n += 1
        for v in node.values():
            n += process_support(v, register)
    elif isinstance(node, list):
        for v in node:
            n += process_support(v, register)
    return n


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as f:
        return json.load(f)


def save(fn, payload):
    with open(os.path.join(DATA, fn), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
        f.write("\n")


def main():
    manifest = load("manifest.json")
    vocab = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "vocabulary"]
    dialogs = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "dialogues"]

    print("=" * 58)
    print("WARIANTY ZALEŻNE OD PŁCI MÓWIĄCEGO")
    print("=" * 58)

    for fn in vocab:
        data = load(fn)
        for rec in data["records"]:
            process_record(rec)
        save(fn, data)
        print("  %-28s %5d rekordów" % (fn, len(data["records"])))

    for fn in dialogs:
        data = load(fn)
        for dlg in data["records"]:
            process_dialogue(dlg)
        save(fn, data)
        print("  %-28s %5d dialogów" % (fn, len(data["records"])))

    gram = load("grammar.json")
    stats["grammar"] = process_support(gram)
    save("grammar.json", gram)
    pron = load("pronunciation.json")
    stats["pronunciation"] = process_support(pron)
    save("pronunciation.json", pron)

    meta = load("metadata.json")
    meta["genderVariants"] = {
        "field": "genderVariant.female",
        "default": "męska",
        "records": stats["recordsWithVariant"],
        "examples": stats["examplesWithVariant"],
        "dialogueLines": stats["linesWithVariant"],
    }
    save("metadata.json", meta)

    print("-" * 58)
    print("  rekordów słownika               %6d" % stats["records"])
    print("  z wariantem żeńskim             %6d" % stats["recordsWithVariant"])
    print("  przykładów                      %6d" % stats["examples"])
    print("  przykładów z wariantem          %6d" % stats["examplesWithVariant"])
    print("  haseł o samej formie (bez zmian)%6d" % stats["lexicon"])
    print("  usuniętych etykiet „(mężczyzna)” %5d" % stats["labelsRemoved"])
    print("  dopisanych wyjaśnień w notes    %6d" % stats["notes"])
    print("  dialogów                        %6d" % stats["dialogues"])
    print("  dialogów z oznaczoną płcią ról  %6d" % stats["dialoguesWithRoleGender"])
    print("  kwestii razem                   %6d" % stats["lines"])
    print("  kwestii z wariantem żeńskim     %6d" % stats["linesWithVariant"])
    print("  kwestii poprawionych na żeńskie %6d" % stats["linesFixedFemale"])
    print("  kwestii poprawionych na męskie  %6d" % stats["linesFixedMale"])
    print("  wzorców gramatycznych           %6d" % stats["grammar"])
    print("  przykładów wymowy               %6d" % stats["pronunciation"])
    print("WYNIK: GOTOWE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
