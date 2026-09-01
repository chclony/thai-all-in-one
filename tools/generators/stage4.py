#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Etap 4 — poziom B1.

Skrypt TWORZY pliki B1, DOPISUJE dialogi B1 do data/dialogues-part-02.json
i przelicza liczniki. Nigdy nie rusza zawartosci poziomow Survival, A1 i A2.

  1. wczytuje cala istniejaca baze (Survival + A1 + A2 + wszystkie dialogi),
  2. zasiewa Builder kluczami i licznikami ID — unikalnosc w calej bazie,
  3. buduje indeks hasel bazowych (istniejace rekordy + nowy rdzen B1),
  4. buduje rekordy rdzenne z lex_b1_core_[a-g], lex_b1_react, lex_b1_connect,
  5. buduje rekordy wzorcowe z lex_b1_tpl_[a-e] (biale listy slow),
  6. deduplikuje trzystopniowo: po polskim hasle, po parze (polski, tajski)
     oraz po samym zdaniu tajskim — wobec CALEJ bazy,
  7. dzieli pule na b1-part-01/02/03.json (850 + 850 + 800),
  8. dopisuje 40 dialogow B1 do dialogues-part-02.json,
  9. przelicza categories.json, metadata.json i manifest.json.

Uruchomienie (z katalogu tools/generators):
    python3 stage4.py

Skrypt jest idempotentny: pliki B1 odtwarza od zera z tego samego materialu
zrodlowego, a dialogi B1 dopisuje tylko wtedy, gdy jeszcze ich nie ma.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Builder, strip_tones, polish_read, tone_guide            # noqa: E402
from lex_b1_core_a import CORE_A                                            # noqa: E402
from lex_b1_core_b import CORE_B                                            # noqa: E402
from lex_b1_core_c import CORE_C                                            # noqa: E402
from lex_b1_core_d import CORE_D                                            # noqa: E402
from lex_b1_core_e import CORE_E                                            # noqa: E402
from lex_b1_core_f import CORE_F                                            # noqa: E402
from lex_b1_core_g import CORE_G                                            # noqa: E402
from lex_b1_react import CORE_REACT                                         # noqa: E402
from lex_b1_connect import CORE_CONNECT                                     # noqa: E402
from lex_b1_tpl_a import TPL_A                                              # noqa: E402
from lex_b1_tpl_b import TPL_B                                              # noqa: E402
from lex_b1_tpl_c import TPL_C                                              # noqa: E402
from lex_b1_tpl_d import TPL_D                                              # noqa: E402
from lex_b1_tpl_e import TPL_E                                              # noqa: E402
from lex_b1_dialogues_a import DIALOGUES_B1_A                               # noqa: E402
from lex_b1_dialogues_b import DIALOGUES_B1_B                               # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")
VERSION = "1.3.0"
UPDATED = "2026-08-15"

BASE_FILES = ["survival.json", "a1-part-01.json", "a1-part-02.json",
              "a2-part-01.json", "a2-part-02.json"]
B1_FILES = [("b1-part-01.json", 850), ("b1-part-02.json", 850), ("b1-part-03.json", 800)]
DLG_FILE = "dialogues-part-02.json"

SRC_CORE = "Rdzeń opracowany ręcznie — etap 4 B1 (zweryfikowany)"
SRC_TPL = "Wzorzec zdaniowy z białej listy słów — etap 4 B1"

REGISTER = {"n": "neutralny", "f": "formalny", "i": "nieformalny", "p": "potoczny"}

CORE_ALL = (CORE_A + CORE_B + CORE_C + CORE_D + CORE_E + CORE_F + CORE_G
            + CORE_REACT + CORE_CONNECT)
TPL_ALL = TPL_A + TPL_B + TPL_C + TPL_D + TPL_E
DIALOGUES_B1 = DIALOGUES_B1_A + DIALOGUES_B1_B


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as fh:
        return json.load(fh)


def save(fn, payload):
    with open(os.path.join(DATA, fn), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)


def main():
    # ------------------------------------------------------------ stan istniejacy
    base_records = []
    for fn in BASE_FILES:
        base_records.extend(load(fn)["records"])

    builder = Builder()
    for rec in base_records:
        prefix, num = rec["id"].rsplit("-", 1)
        builder.counter[prefix] = max(builder.counter.get(prefix, 0), int(num))
        builder.ids.add(rec["id"])
        builder.seen_key.add((strip_tones(rec["polish"]).lower(), rec["ttsThai"]))

    seen_polish = {strip_tones(r["polish"]).lower() for r in base_records}
    seen_thai = {r["ttsThai"] for r in base_records}
    rejected = collections.Counter()

    base_index = {}
    for rec in base_records:
        base_index.setdefault(rec["polish"],
                              (rec["thaiPhonetic"], rec["ttsThai"],
                               rec["category"], rec["subcategory"], rec["frequency"]))

    def build(pl, ph, th, cat, sub, rtype, tags, freq, reg, note, literal, ex, source):
        """Trzystopniowa deduplikacja wobec CALEJ bazy."""
        key = strip_tones(pl).lower()
        if key in seen_polish:
            rejected["polskie hasło już istnieje"] += 1
            return None
        if th in seen_thai:
            rejected["zdanie tajskie już istnieje"] += 1
            return None
        rec = builder.make("B1", pl, ph, th, cat, sub, rtype, tags,
                           freq=freq, register=REGISTER[reg], notes=note,
                           literal=literal, examples=[ex])
        if rec is None:
            rejected["para (polski, tajski) już istnieje"] += 1
            return None
        seen_polish.add(key)
        seen_thai.add(th)
        rec["source"] = source
        return rec

    # ------------------------------------------------------------ rekordy rdzenne
    core_records = []
    for pl, ph, th, cat, sub, rtype, freq, reg, note, literal, ex in CORE_ALL:
        base_index.setdefault(pl, (ph, th, cat, sub, freq))
        tags = sorted({cat.split()[0].lower(), sub.split()[0].lower(), "słownictwo", "b1"})
        rec = build(pl, ph, th, cat, sub, rtype, tags, freq, reg, note, literal,
                    ex, SRC_CORE)
        if rec:
            core_records.append(rec)

    # ------------------------------------------------------------ rekordy wzorcowe
    tpl_records = []
    for tpl in TPL_ALL:
        for rec_pl, base_pl, ex_pl in tpl["items"]:
            if base_pl not in base_index:
                raise SystemExit("Wzorzec %s wskazuje na nieznane hasło: %r"
                                 % (tpl["key"], base_pl))
            ph_b, th_b, _cat_b, _sub_b, freq_b = base_index[base_pl]
            ph = tpl["ph"].replace("{ph}", ph_b)
            th = tpl["th"].replace("{th}", th_b)
            ex = (ex_pl,
                  tpl["ex_ph"].replace("{ph}", ph_b),
                  tpl["ex_th"].replace("{th}", th_b))
            tags = sorted({"zwroty", tpl["cat"].split()[0].lower(), "wzorzec", "b1"})
            rec = build(rec_pl, ph, th, tpl["cat"], tpl["sub"], tpl["ty"], tags,
                        max(2, min(5, freq_b - 1)), tpl["reg"], tpl["note"], tpl["lit"],
                        ex, SRC_TPL)
            if rec:
                tpl_records.append(rec)

    pool = core_records + tpl_records
    need = sum(n for _fn, n in B1_FILES)
    if len(pool) < need:
        raise SystemExit("Za mało rekordów B1: mam %d, potrzeba %d. "
                         "Rozszerz białe listy w lex_b1_tpl_*.py." % (len(pool), need))

    used, deferred = pool[:need], pool[need:]

    offset = 0
    for fn, size in B1_FILES:
        chunk = used[offset:offset + size]
        offset += size
        save(fn, {"file": fn, "count": len(chunk), "records": chunk})

    if deferred:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "reserve-stage5.json"), "w", encoding="utf-8") as fh:
            json.dump({"note": "Hasła gotowe, odłożone na etap 5 (limit B1 wyczerpany).",
                       "count": len(deferred),
                       "records": [{"polish": r["polish"], "thaiPhonetic": r["thaiPhonetic"],
                                    "ttsThai": r["ttsThai"], "category": r["category"],
                                    "subcategory": r["subcategory"]} for r in deferred]},
                      fh, ensure_ascii=False, indent=1)

    # ------------------------------------------------------------ dialogi
    dlg = load(DLG_FILE)
    existing_titles = set()
    for fn in ("dialogues-part-01.json", DLG_FILE):
        existing_titles |= {d["title"] for d in load(fn)["records"]}
    all_dlg_nums = []
    for fn in ("dialogues-part-01.json", DLG_FILE):
        all_dlg_nums += [int(d["id"].rsplit("-", 1)[1]) for d in load(fn)["records"]]
    next_num = max(all_dlg_nums) + 1

    added = 0
    for title, sit, level, ra, rb, lines, note in DIALOGUES_B1:
        if title in existing_titles:
            continue                       # idempotencja: dialog już dopisany
        if not 4 <= len(lines) <= 16:
            raise SystemExit("Dialog „%s” ma %d kwestii (dozwolone 4-16)."
                             % (title, len(lines)))
        dlg["records"].append({
            "id": "dlg-%04d" % next_num,
            "type": "dialogue",
            "title": title,
            "situation": sit,
            "category": sit,
            "level": level,
            "roles": {"A": ra, "B": rb},
            "notes": note,
            "tags": ["dialog", sit.split()[0].lower(), level.lower()],
            "lines": [{
                "index": n,
                "role": r,
                "polish": pl,
                "thaiPhonetic": ph,
                "pronunciationPolish": polish_read(ph),
                "toneGuide": tone_guide(ph),
                "ttsThai": th,
                "audioFile": "",
            } for n, (r, pl, ph, th) in enumerate(lines, 1)],
            "source": "Baza projektu Thai All-in-One",
            "license": "Do weryfikacji przed publiczną publikacją",
        })
        existing_titles.add(title)
        next_num += 1
        added += 1

    dlg["count"] = len(dlg["records"])
    dlg["lineCount"] = sum(len(d["lines"]) for d in dlg["records"])
    save(DLG_FILE, dlg)

    counts, total, dlg_files = refresh_counters()

    # ------------------------------------------------------------ raport
    reakcje = sum(1 for r in used if r["subcategory"] == "Reakcje")
    print("=" * 58)
    print("ETAP 4 — POZIOM B1")
    print("=" * 58)
    print("  rekordy rdzenne zbudowane  %5d" % len(core_records))
    print("  rekordy wzorcowe zbudowane %5d" % len(tpl_records))
    print("  odrzucone duplikaty        %5d" % sum(rejected.values()))
    for why, n in rejected.most_common():
        print("     %-34s %5d" % (why, n))
    print("  zapisane do plików B1      %5d" % len(used))
    print("  w tym rekordy reakcji      %5d" % reakcje)
    print("  odłożone na etap 5         %5d" % len(deferred))
    print("  nowe dialogi B1            %5d" % added)
    print("-" * 58)
    for fn, c in counts.items():
        print("  %-26s %5d" % (fn, c))
    print("  %-26s %5d" % ("RAZEM rekordów", total))
    for fn, d in dlg_files.items():
        print("  %-26s %5d dialogów, %d kwestii" % (fn, d["count"], d["lineCount"]))
    return 0


def refresh_counters():
    """Przelicza categories.json, metadata.json i manifest.json na podstawie
    faktycznej zawartosci katalogu data/."""
    manifest = load("manifest.json")

    known = {f["file"] for f in manifest["dataFiles"]}
    for fn, _size in B1_FILES:
        if fn not in known:
            manifest["dataFiles"].append({"file": fn, "kind": "vocabulary",
                                          "level": "B1", "count": 0})
    added = {fn for fn, _ in B1_FILES}
    manifest["plannedFiles"] = [f for f in manifest.get("plannedFiles", [])
                                if f["file"] not in added]

    vocab_files = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "vocabulary"]
    dialog_files = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "dialogues"]

    counts, final = {}, []
    for fn in vocab_files:
        data = load(fn)
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

    # plik dialogow etapu 3 obejmuje teraz takze poziom B1
    for f in manifest["dataFiles"]:
        if f["file"] == "dialogues-part-02.json":
            f["level"] = "A2/B1"

    cats = collections.Counter()
    subs = collections.defaultdict(collections.Counter)
    levels = collections.Counter()
    for r in final:
        cats[r["category"]] += 1
        subs[r["category"]][r["subcategory"]] += 1
        levels[r["level"]] += 1

    ICON = {"Jedzenie i napoje": "food", "Restauracja": "resto", "Transport": "transport",
            "Hotel": "hotel", "Zakupy i pieniądze": "shop", "Zdrowie": "health",
            "Miejsca i orientacja": "map", "Podstawy i grzeczność": "hello",
            "Ludzie i rodzina": "people", "Czas i daty": "clock", "Liczby i liczenie": "num",
            "Czasowniki": "verb", "Cechy i opinie": "star", "Awarie i pomoc": "alert",
            "Small talk": "chat", "Dom i codzienność": "home", "Praca i nauka": "work",
            "Pytania": "question", "Pogoda i przyroda": "weather",
            "Gramatyka użytkowa": "dict"}

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

    metadata = load("metadata.json")
    metadata["version"] = VERSION
    metadata["levels"] = dict(levels)
    metadata["totalRecords"] = len(final)
    metadata["dialogues"] = total_dlg
    metadata["dialogueLines"] = total_lines
    metadata["grammarTopics"] = grammar["count"]
    metadata["updated"] = UPDATED
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
    return counts, len(final), dlg_files


if __name__ == "__main__":
    sys.exit(main())
