#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sesja F — uzupelnienie rdzenia slownikowego.

DIAGNOZA, KTORA TEN ETAP NAPRAWIA

Baza miala 10 200 rekordow, ale tylko 763 typu „word” i 1 217 unikalnych
tokenow sylabicznych. Dziesiec tysiecy rekordow stalo na slowniku rzedu
tysiaca jednostek — reszta to warianty zdaniowe tego samego materialu.
Dodatkowo systemy zamkniete (kolory, warzywa, czesci ciala, godziny, pory dnia,
liczebniki porzadkowe) mialy zero albo prawie zero rekordow, co blokowalo
cale klasy wypowiedzi.

CO ROBI TEN SKRYPT

Buduje data/core-lexicon-01.json i data/core-lexicon-02.json wylacznie
z rekordow typu „word” — krotkich hasel slownikowych w mianowniku, kazde
z 2-3 przykladami uzycia. Nie generuje zdan: zdan w bazie jest juz 6 202.

Skrypt jest idempotentny — odtwarza oba pliki od zera z tego samego materialu
zrodlowego i nie dotyka plikow poziomow Survival, A1, A2, B1, B2 ani
supplemental-practical.json.

Uruchomienie (z katalogu tools/generators):
    python3 stage7.py
"""
import collections
import json
import re
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Builder, strip_tones                                     # noqa: E402

# --- systemy zamkniete ------------------------------------------------------
from lex_f_colors import COLORS                                             # noqa: E402
from lex_f_veg import VEG                                                   # noqa: E402
from lex_f_body import BODY                                                 # noqa: E402
from lex_f_time import TIME                                                 # noqa: E402
from lex_f_daypart import DAYPART                                           # noqa: E402

# --- rdzen otwarty ----------------------------------------------------------
from lex_f_verbs_a import VERBS_A                                           # noqa: E402
from lex_f_verbs_b import VERBS_B                                           # noqa: E402
from lex_f_adj import ADJ                                                   # noqa: E402
from lex_f_adv import ADV                                                   # noqa: E402
from lex_f_house import HOUSE                                               # noqa: E402
from lex_f_things import THINGS                                             # noqa: E402
from lex_f_world import WORLD                                               # noqa: E402
from lex_f_food import FOOD                                                 # noqa: E402
from lex_f_gram import GRAM                                                 # noqa: E402
from lex_f_verbs_c import VERBS_C                                          # noqa: E402
from lex_f_adj_b import ADJ_B                                              # noqa: E402
from lex_f_adv_b import ADV_B                                              # noqa: E402
from lex_f_people import PEOPLE                                            # noqa: E402
from lex_f_health import HEALTH                                            # noqa: E402
from lex_f_travel import TRAVEL                                            # noqa: E402
from lex_f_life import LIFE                                               # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")
HERE = os.path.dirname(os.path.abspath(__file__))

VERSION = "1.6.0"
UPDATED = "2026-08-17"
SOURCE = "Rdzeń leksykalny — sesja F (zweryfikowany)"

FILE_01 = "core-lexicon-01.json"
FILE_02 = "core-lexicon-02.json"

def thai_key(text):
    """Klucz dedup dla zapisu tajskiego.

    Tajski nie stawia spacji miedzy wyrazami, ale w bazie zdarzaja sie
    warianty z odstepem i bez (np. przy znaku powtorzenia). Bez tej
    normalizacji „นานๆ ที” i „นานๆที” trafialyby do bazy jako dwa hasla.
    """
    return re.sub(r"\s+", "", text)


REGISTER = {"n": "neutralny", "f": "formalny", "i": "nieformalny", "p": "potoczny"}

ICON = {"Jedzenie i napoje": "food", "Restauracja": "resto", "Transport": "transport",
        "Hotel": "hotel", "Zakupy i pieniądze": "shop", "Zdrowie": "health",
        "Miejsca i orientacja": "map", "Podstawy i grzeczność": "hello",
        "Ludzie i rodzina": "people", "Czas i daty": "clock", "Liczby i liczenie": "num",
        "Czasowniki": "verb", "Cechy i opinie": "star", "Awarie i pomoc": "alert",
        "Small talk": "chat", "Dom i codzienność": "home", "Praca i nauka": "work",
        "Pytania": "question", "Pogoda i przyroda": "weather",
        "Gramatyka użytkowa": "dict"}

# Kolejnosc ma znaczenie: systemy zamkniete ida pierwsze, zeby w razie
# jakiegokolwiek limitu to one trafily do bazy w calosci.
GROUPS = [
    ("kolory", COLORS),
    ("warzywa", VEG),
    ("części ciała", BODY),
    ("godziny", TIME),
    ("pory dnia, liczebniki porządkowe, zwierzęta", DAYPART),
    ("czasowniki I", VERBS_A),
    ("czasowniki II", VERBS_B),
    ("przymiotniki", ADJ),
    ("przysłówki", ADV),
    ("dom i wyposażenie", HOUSE),
    ("ubrania, elektronika, dokumenty, narzędzia", THINGS),
    ("natura, miasto, praca, szkoła", WORLD),
    ("jedzenie", FOOD),
    ("przyimki i spójniki", GRAM),
    ("czasowniki III", VERBS_C),
    ("przymiotniki II", ADJ_B),
    ("przysłówki II", ADV_B),
    ("ludzie, rodzina, zawody", PEOPLE),
    ("zdrowie i apteka", HEALTH),
    ("podróż i pieniądze", TRAVEL),
    ("pojęcia, czas wolny, święta, pogoda", LIFE),
]


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as fh:
        return json.load(fh)


def save(fn, payload):
    with open(os.path.join(DATA, fn), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)


class Pool(object):
    """Deduplikacja trzystopniowa, zgodnie z zasadami z README generatorow."""

    def __init__(self, base_records):
        self.builder = Builder()
        for rec in base_records:
            prefix, num = rec["id"].rsplit("-", 1)
            self.builder.counter[prefix] = max(self.builder.counter.get(prefix, 0), int(num))
            self.builder.ids.add(rec["id"])
            self.builder.seen_key.add((strip_tones(rec["polish"]).lower(), rec["ttsThai"]))
        self.seen_polish = {strip_tones(r["polish"]).lower() for r in base_records}
        for rec in base_records:
            for alt in rec.get("polishAlternatives") or []:
                self.seen_polish.add(strip_tones(alt).lower())
        self.seen_thai = {thai_key(r["ttsThai"]) for r in base_records}
        self.rejected = collections.Counter()
        self.dropped_headwords = []
        # hasla odrzucone przez dedup nadal moga byc celem relacji — zapamietujemy
        # ich zapis tajski, zeby wskazac rekord bazowy o tym samym brzmieniu
        self.alias_thai = {}
        self.pending_alias = []

    def build(self, level, pl, ph, th, cat, sub, freq, reg, note, literal,
              examples, alternatives):
        key = strip_tones(pl).lower()
        self.alias_thai.setdefault(key, th)
        if key in self.seen_polish:
            self.rejected["polskie hasło już istnieje"] += 1
            self.dropped_headwords.append(pl)
            return None
        if thai_key(th) in self.seen_thai:
            self.rejected["zdanie tajskie już istnieje"] += 1
            self.dropped_headwords.append(pl)
            # Hasło jest nowe, powtarza się tylko zapis tajski — czyli w bazie
            # siedzi synonim. Kasowanie hasła zabrałoby je z wyszukiwarki, więc
            # trafia do polishAlternatives rekordu, który już to słowo pokrywa.
            self.pending_alias.append((pl, thai_key(th)))
            return None
        tags = sorted({cat.split()[0].lower().strip(","), sub.split()[0].lower(),
                       "słownictwo", level.lower(), "rdzeń"})
        rec = self.builder.make(level, pl, ph, th, cat, sub, "word", tags,
                                freq=freq, register=REGISTER[reg], notes=note,
                                literal=literal, examples=examples,
                                alternatives=alternatives)
        if rec is None:
            self.rejected["para (polski, tajski) już istnieje"] += 1
            self.dropped_headwords.append(pl)
            return None
        self.seen_polish.add(key)
        self.seen_thai.add(thai_key(th))
        rec["source"] = SOURCE
        return rec


def merge_aliases(pool, vocab_files):
    """Dopisuje do rekordow bazowych hasla utracone na kolizji zapisu tajskiego.

    Jesli kandydat mial nowe polskie haslo, ale ten sam zapis tajski co rekord
    juz obecny w bazie, to znaczy, ze baza pokrywa to slowo pod innym
    tlumaczeniem („swinia" i „wieprzowina" to jedno หมู). Skasowanie kandydata
    bez sladu zabraloby haslo z wyszukiwarki — dlatego laduje ono w
    polishAlternatives rekordu, ktory to slowo pokrywa.

    Funkcja jest idempotentna: przy powtornym uruchomieniu warianty juz obecne
    sa pomijane, a pliki bez zmian nie sa przepisywane.
    """
    if not pool.pending_alias:
        return 0

    wanted = {}
    for pl, tkey in pool.pending_alias:
        wanted.setdefault(tkey, [])
        if pl not in wanted[tkey]:
            wanted[tkey].append(pl)

    added = 0
    for fn in vocab_files:
        data = load(fn)
        dirty = False
        for rec in data["records"]:
            names = wanted.get(thai_key(rec["ttsThai"]))
            if not names:
                continue
            alts = rec.get("polishAlternatives") or []
            known = {strip_tones(x).lower() for x in alts}
            known.add(strip_tones(rec["polish"]).lower())
            for pl in names:
                if strip_tones(pl).lower() in known:
                    continue
                alts.append(pl)
                known.add(strip_tones(pl).lower())
                added += 1
                dirty = True
            rec["polishAlternatives"] = alts
        if dirty:
            save(fn, data)
    return added


def main():
    manifest = load("manifest.json")
    vocab_files = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "vocabulary"]
    vocab_files = [f for f in vocab_files if f not in (FILE_01, FILE_02)]

    base_records = []
    for fn in vocab_files:
        base_records.extend(load(fn)["records"])

    pool = Pool(base_records)

    built = []
    per_group = []
    # relacje zapisujemy po polskim hasle, ID nadaje Builder — rozwiazujemy je
    # dopiero wtedy, gdy caly material jest zbudowany
    related_by_id = {}

    for name, rows in GROUPS:
        got = 0
        for (level, pl, ph, th, cat, sub, freq, reg,
             note, literal, examples, related, alternatives) in rows:
            rec = pool.build(level, pl, ph, th, cat, sub, freq, reg, note,
                             literal, examples, alternatives)
            if rec is None:
                continue
            related_by_id[rec["id"]] = related
            built.append(rec)
            got += 1
        per_group.append((name, len(rows), got))

    # --------------------------------------------------- rozwiazanie relacji
    def norm(text):
        return re.sub(r"\s*\(.*?\)", "", strip_tones(text)).strip().lower()

    index = {}
    for rec in base_records + built:
        for form in [rec["polish"]] + list(rec.get("polishAlternatives") or []):
            index.setdefault(strip_tones(form).lower(), rec["id"])
            index.setdefault(norm(form), rec["id"])

    by_thai = {}
    for rec in base_records + built:
        by_thai.setdefault(rec["ttsThai"], rec["id"])

    linked, unresolved = 0, collections.Counter()
    for rec in built:
        refs = []
        for key in related_by_id.get(rec["id"], []):
            k = strip_tones(key).lower()
            rid = index.get(k) or index.get(norm(key))
            if rid is None:
                rid = by_thai.get(pool.alias_thai.get(k))
            if rid is None:
                unresolved[key] += 1
                continue
            if rid != rec["id"] and rid not in refs:
                refs.append(rid)
        rec["relatedWords"] = refs
        linked += len(refs)

    aliases_added = merge_aliases(pool, vocab_files)

    # ------------------------------------------------------- podzial na pliki
    half = (len(built) + 1) // 2
    part1, part2 = built[:half], built[half:]
    save(FILE_01, {"file": FILE_01, "count": len(part1), "records": part1})
    save(FILE_02, {"file": FILE_02, "count": len(part2), "records": part2})

    counts, total, dlg_files, stats = refresh_counters()

    # -------------------------------------------------------------- raport
    print("=" * 62)
    print("SESJA F — UZUPEŁNIENIE RDZENIA SŁOWNIKOWEGO")
    print("=" * 62)
    print("  baza wejściowa                    %5d" % len(base_records))
    print("-" * 62)
    print("  %-34s %5s %5s" % ("grupa", "pula", "przyj."))
    for name, total_rows, got in per_group:
        print("  %-34s %5d %5d" % (name, total_rows, got))
    print("-" * 62)
    print("  zbudowane rekordy typu word       %5d" % len(built))
    print("  odrzucone przez deduplikację      %5d" % sum(pool.rejected.values()))
    for why, n in pool.rejected.most_common():
        print("     %-32s %5d" % (why, n))
    print("  ustanowione powiązania            %5d" % linked)
    print("  hasła dopisane jako warianty      %5d" % aliases_added)
    if unresolved:
        print("  nierozwiązane klucze relacji      %5d" % sum(unresolved.values()))
        for key, n in unresolved.most_common(12):
            print("     %-32s %5d" % (key, n))
    print("-" * 62)
    print("  %-34s %5d" % (FILE_01, len(part1)))
    print("  %-34s %5d" % (FILE_02, len(part2)))
    print("-" * 62)
    for fn, c in counts.items():
        print("  %-34s %5d" % (fn, c))
    print("  %-34s %5d" % ("RAZEM rekordów", total))
    print("-" * 62)
    print("  rekordy typu word w całej bazie   %5d" % stats["words"])
    print("  unikalne tokeny sylabiczne        %5d" % stats["tokens"])
    print("  przykłady zdań                    %5d" % stats["examples"])
    return 0


def refresh_counters():
    manifest = load("manifest.json")
    known = {f["file"] for f in manifest["dataFiles"]}
    for fn in (FILE_01, FILE_02):
        if fn not in known:
            manifest["dataFiles"].append({"file": fn, "kind": "vocabulary",
                                          "level": "A1/A2", "count": 0})
    manifest["plannedFiles"] = [f for f in manifest.get("plannedFiles", [])
                                if f["file"] not in (FILE_01, FILE_02)]
    save("manifest.json", manifest)

    vocab_files = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "vocabulary"]
    dialog_files = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "dialogues"]

    counts, final = {}, []
    for fn in vocab_files:
        data = load(fn)
        data["count"] = len(data["records"])
        save(fn, data)
        counts[fn] = data["count"]
        final.extend(data["records"])

    dlg_files = {}
    for fn in dialog_files:
        d = load(fn)
        d["count"] = len(d["records"])
        d["lineCount"] = sum(len(x["lines"]) for x in d["records"])
        save(fn, d)
        dlg_files[fn] = d
        counts[fn] = d["count"]

    cats = collections.Counter()
    subs = collections.defaultdict(collections.Counter)
    levels = collections.Counter()
    for r in final:
        cats[r["category"]] += 1
        subs[r["category"]][r["subcategory"]] += 1
        levels[r["level"]] += 1

    categories = [{
        "id": "cat-%02d" % i,
        "name": name,
        "icon": ICON.get(name, "dot"),
        "count": cnt,
        "subcategories": [{"name": s, "count": c} for s, c in sorted(subs[name].items())],
    } for i, (name, cnt) in enumerate(sorted(cats.items()), 1)]
    save("categories.json", {"file": "categories.json", "count": len(categories),
                             "records": categories})

    grammar = load("grammar.json")
    pron = load("pronunciation.json")
    total_dlg = sum(d["count"] for d in dlg_files.values())
    total_lines = sum(d["lineCount"] for d in dlg_files.values())
    examples = sum(len(r.get("examples", [])) for r in final)
    words = sum(1 for r in final if r["type"] == "word")
    tokens = set()
    for r in final:
        for s in r["syllables"]:
            tokens.add(s.lower())

    metadata = load("metadata.json")
    metadata["version"] = VERSION
    metadata["levels"] = dict(levels)
    metadata["totalRecords"] = len(final)
    metadata["dialogues"] = total_dlg
    metadata["dialogueLines"] = total_lines
    metadata["exampleSentences"] = examples
    metadata["grammarTopics"] = grammar["count"]
    metadata["updated"] = UPDATED
    metadata["lexicalCore"] = {
        "wordRecords": words,
        "uniqueSyllableTokens": len(tokens),
        "note": "Miara realnego zasobu słownictwa: liczba rekordów typu word "
                "oraz liczba różnych sylab występujących w bazie.",
    }
    save("metadata.json", metadata)

    manifest["version"] = VERSION
    manifest["updated"] = UPDATED
    manifest["cacheKey"] = "thai-aio-data-v" + VERSION
    for f in manifest["dataFiles"]:
        if f["file"] in counts:
            f["count"] = counts[f["file"]]
    for f in manifest["supportFiles"]:
        if f["file"] == "categories.json":
            f["count"] = len(categories)
        elif f["file"] == "grammar.json":
            f["count"] = grammar["count"]
        elif f["file"] == "pronunciation.json":
            f["count"] = len(pron.get("tones", [])) + len(pron.get("minimalPairs", []))
    manifest["levels"] = dict(levels)
    manifest["categories"] = [c["name"] for c in categories]
    manifest["totalRecords"] = len(final)
    manifest["totalDialogues"] = total_dlg
    save("manifest.json", manifest)

    return counts, len(final), dlg_files, {
        "words": words, "tokens": len(tokens), "examples": examples}


if __name__ == "__main__":
    sys.exit(main())
