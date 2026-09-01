#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Etap 3 — poziom A2.

Skrypt TWORZY nowe pliki danych i AKTUALIZUJE liczniki, nigdy nie rusza
zawartosci poziomow Survival i A1:

  1. wczytuje cala istniejaca baze (survival + A1 + dialogi etapu 1-2),
  2. zasiewa Builder kluczami i licznikami ID — unikalnosc w calej bazie,
  3. buduje indeks hasel bazowych (istniejace rekordy + nowy rdzen A2),
  4. buduje rekordy rdzenne z lex_a2_core_[a-d],
  5. buduje rekordy wzorcowe z lex_a2_tpl_[a-e] (biale listy slow),
  6. deduplikuje potrojnie: po polskim hasle, po parze (polski, tajski)
     oraz po samym zdaniu tajskim,
  7. dzieli pule na data/a2-part-01.json i data/a2-part-02.json (po 1000),
  8. zapisuje 40 dialogow A2 do data/dialogues-part-02.json,
  9. przelacza plik dialogow z listy plannedFiles do dataFiles w manifescie,
 10. przelicza categories.json, metadata.json i manifest.json.

Uruchomienie (z katalogu tools/generators):
    python3 stage3.py

Skrypt jest idempotentny: przy powtornym uruchomieniu wykrywa, ze hasla juz
sa w bazie, i odtwarza pliki A2 od zera z tego samego materialu zrodlowego.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Builder, strip_tones, polish_read, tone_guide          # noqa: E402
from lex_a2_core_a import CORE_A                                          # noqa: E402
from lex_a2_core_b import CORE_B                                          # noqa: E402
from lex_a2_core_c import CORE_C                                          # noqa: E402
from lex_a2_core_d import CORE_D                                          # noqa: E402
from lex_a2_tpl_a import TPL_A                                            # noqa: E402
from lex_a2_tpl_b import TPL_B                                            # noqa: E402
from lex_a2_tpl_c import TPL_C                                            # noqa: E402
from lex_a2_tpl_d import TPL_D                                            # noqa: E402
from lex_a2_tpl_e import TPL_E                                            # noqa: E402
from lex_a2_tpl_f import TPL_F                                            # noqa: E402
from lex_a2_dialogues_a import DIALOGUES_A2_A                             # noqa: E402
from lex_a2_dialogues_b import DIALOGUES_A2_B                             # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")
VERSION = "1.2.0"
UPDATED = "2026-08-14"

BASE_FILES = ["survival.json", "a1-part-01.json", "a1-part-02.json"]
A2_FILES = ["a2-part-01.json", "a2-part-02.json"]
DLG_NEW = "dialogues-part-02.json"
TARGET_PER_FILE = 1000

SRC_CORE = "Rdzeń opracowany ręcznie — etap 3 A2 (zweryfikowany)"
SRC_TPL = "Wzorzec zdaniowy z białej listy słów — etap 3 A2"

REGISTER = {"n": "neutralny", "f": "formalny", "i": "nieformalny", "p": "potoczny"}

CORE_ALL = CORE_A + CORE_B + CORE_C + CORE_D
TPL_ALL = TPL_A + TPL_B + TPL_C + TPL_D + TPL_E + TPL_F
DIALOGUES_A2 = DIALOGUES_A2_A + DIALOGUES_A2_B

# ---------------------------------------------------------------- WZORCE PRZYKLADOW
# Uzywane tylko tam, gdzie leksyka podala przyklad w postaci ("polski", "KLUCZ").
# Polska strona zawsze pochodzi z leksyki i jest pisana recznie.
PAT3 = {
    "WHERE":   ("{ph} yùu thîi nǎi khráp", "{th}อยู่ที่ไหนครับ"),
    "HAVE":    ("mii {ph} mǎi khráp", "มี{th}ไหมครับ"),
    "ORDER":   ("khǎw {ph} nòi khráp", "ขอ{th}หน่อยครับ"),
    "WANT":    ("phǒm yàak dâai {ph} khráp", "ผมอยากได้{th}ครับ"),
    "NEED":    ("phǒm tâwng-kaan {ph} khráp", "ผมต้องการ{th}ครับ"),
    "LIKE":    ("phǒm châwp {ph} mâak khráp", "ผมชอบ{th}มากครับ"),
    "THIS":    ("nîi khue {ph} khráp", "นี่คือ{th}ครับ"),
    "VERY":    ("{ph} mâak khráp", "{th}มากครับ"),
    "ISIT":    ("{ph} mǎi khráp", "{th}ไหมครับ"),
    "HOWMUCH": ("{ph} thâo-rài khráp", "{th}เท่าไหร่ครับ"),
}


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as fh:
        return json.load(fh)


def save(fn, payload):
    with open(os.path.join(DATA, fn), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)


def make_example(ex, ph, th):
    """Zwraca (polski, fonetyka, tajski). Polska strona nigdy nie jest sklejana."""
    if len(ex) == 3:
        return ex
    pl, key = ex
    tpl_ph, tpl_th = PAT3[key]
    return (pl, tpl_ph.replace("{ph}", ph), tpl_th.replace("{th}", th))


def main():
    # ------------------------------------------------------------ stan istniejacy
    existing = {fn: load(fn) for fn in BASE_FILES}
    base_records = []
    for fn in BASE_FILES:
        base_records.extend(existing[fn]["records"])

    builder = Builder()
    for rec in base_records:
        prefix, num = rec["id"].rsplit("-", 1)
        builder.counter[prefix] = max(builder.counter.get(prefix, 0), int(num))
        builder.ids.add(rec["id"])
        builder.seen_key.add((strip_tones(rec["polish"]).lower(), rec["ttsThai"]))

    seen_polish = {strip_tones(r["polish"]).lower() for r in base_records}
    seen_thai = {r["ttsThai"] for r in base_records}
    rejected = collections.Counter()

    # indeks hasel bazowych dla wzorcow: najpierw istniejaca baza, potem rdzen A2
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
        rec = builder.make("A2", pl, ph, th, cat, sub, rtype, tags,
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
        tags = sorted({cat.split()[0].lower(), sub.split()[0].lower(), "słownictwo", "a2"})
        rec = build(pl, ph, th, cat, sub, rtype, tags, freq, reg, note, literal,
                    make_example(ex, ph, th), SRC_CORE)
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
            tags = sorted({"zwroty", tpl["cat"].split()[0].lower(), "wzorzec", "a2"})
            rec = build(rec_pl, ph, th, tpl["cat"], tpl["sub"], tpl["ty"], tags,
                        max(2, min(5, freq_b - 1)), tpl["reg"], tpl["note"], tpl["lit"],
                        ex, SRC_TPL)
            if rec:
                tpl_records.append(rec)

    pool = core_records + tpl_records
    need = TARGET_PER_FILE * len(A2_FILES)
    if len(pool) < need:
        raise SystemExit("Za mało rekordów A2: mam %d, potrzeba %d. "
                         "Rozszerz białe listy w lex_a2_tpl_*.py." % (len(pool), need))

    used, deferred = pool[:need], pool[need:]

    for i, fn in enumerate(A2_FILES):
        chunk = used[i * TARGET_PER_FILE:(i + 1) * TARGET_PER_FILE]
        save(fn, {"file": fn, "count": len(chunk), "records": chunk})

    if deferred:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "reserve-stage4.json"), "w", encoding="utf-8") as fh:
            json.dump({"note": "Hasła gotowe, odłożone na etap 4 (limit A2 wyczerpany).",
                       "count": len(deferred),
                       "records": [{"polish": r["polish"], "thaiPhonetic": r["thaiPhonetic"],
                                    "ttsThai": r["ttsThai"], "category": r["category"],
                                    "subcategory": r["subcategory"]} for r in deferred]},
                      fh, ensure_ascii=False, indent=1)

    # ------------------------------------------------------------ dialogi
    dlg_old = load("dialogues-part-01.json")
    next_num = max(int(d["id"].rsplit("-", 1)[1]) for d in dlg_old["records"]) + 1
    old_titles = {d["title"] for d in dlg_old["records"]}

    dlg_records = []
    for title, sit, level, ra, rb, lines, note in DIALOGUES_A2:
        if title in old_titles:
            raise SystemExit("Dialog „%s” już istnieje w etapie 1-2." % title)
        if not 4 <= len(lines) <= 16:
            raise SystemExit("Dialog „%s” ma %d kwestii (dozwolone 4-16)." % (title, len(lines)))
        dlg_records.append({
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
        next_num += 1

    save(DLG_NEW, {"file": DLG_NEW, "count": len(dlg_records),
                   "lineCount": sum(len(d["lines"]) for d in dlg_records),
                   "records": dlg_records})

    counts, total, dlg_files = refresh_counters()

    # ------------------------------------------------------------ raport
    print("=" * 58)
    print("ETAP 3 — POZIOM A2")
    print("=" * 58)
    print("  rekordy rdzenne zbudowane  %5d" % len(core_records))
    print("  rekordy wzorcowe zbudowane %5d" % len(tpl_records))
    print("  odrzucone duplikaty        %5d" % sum(rejected.values()))
    for why, n in rejected.most_common():
        print("     %-34s %5d" % (why, n))
    print("  zapisane do plików A2      %5d" % len(used))
    print("  odłożone na etap 4         %5d" % len(deferred))
    print("  nowe dialogi               %5d" % len(dlg_records))
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

    # ---- pliki danych: dopisz nowe pozycje i usun je z listy planowanych
    known = {f["file"] for f in manifest["dataFiles"]}
    for fn in A2_FILES:
        if fn not in known:
            manifest["dataFiles"].append({"file": fn, "kind": "vocabulary",
                                          "level": "A2", "count": 0})
    if DLG_NEW not in known:
        manifest["dataFiles"].append({"file": DLG_NEW, "kind": "dialogues",
                                      "level": "A2", "count": 0})
    added = set(A2_FILES) | {DLG_NEW}
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
