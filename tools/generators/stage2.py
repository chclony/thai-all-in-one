#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Etap 2 — domkniecie poziomu A1.

Skrypt DOPISUJE dane do istniejacych plikow, nigdy ich nie nadpisuje od zera:

  1. wczytuje survival.json, a1-part-01.json, a1-part-02.json i dialogi,
  2. zasiewa Builder istniejacymi kluczami i licznikami ID (unikalnosc w calej bazie),
  3. buduje rekordy rdzenne z lex_a1_stage2.CORE2S,
  4. buduje rekordy szablonowe z lex_a1_stage2.TEMPLATES2 (biale listy slow),
  5. przycina pule do dokladnie TARGET rekordow w a1-part-02.json,
  6. dopisuje dialogi z lex_dialogues2.DIALOGUES2,
  7. przelicza categories.json, metadata.json i manifest.json.

Uruchomienie (z katalogu tools/generators):
    python3 stage2.py

Skrypt jest idempotentny: powtorne uruchomienie wykryje, ze wszystkie hasla
juz sa w bazie, i nic nie doda.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Builder, strip_tones, polish_read, tone_guide  # noqa: E402
from lex_a1_stage2 import CORE2S, TEMPLATES2                       # noqa: E402
from lex_dialogues2 import DIALOGUES2                              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")
VERSION = "1.1.0"
UPDATED = "2026-08-13"

TARGET_A1_02 = 1000          # docelowa liczba rekordow w a1-part-02.json
TEMPLATE_QUOTA = 46          # ile miejsc rezerwujemy na rekordy szablonowe

SRC_CORE = "Rdzeń opracowany ręcznie — etap 2 (zweryfikowany)"
SRC_TPL = "Wzorzec zdaniowy z białej listy słów — etap 2"

VOCAB_FILES = ["survival.json", "a1-part-01.json", "a1-part-02.json"]

# ---------------------------------------------------------------- WZORCE PRZYKLADOW
# Polska strona przykladu jest zawsze pisana recznie w leksyce; tutaj powstaje
# wylacznie strona tajska.
PAT = {
    "MONTH":   ("phǒm maa duean {ph} khráp", "ผมมาเดือน{th}ครับ"),
    "NUMBAHT": ("{ph} bàat khráp", "{th}บาทครับ"),
    "WHERE":   ("{ph} yùu thîi nǎi khráp", "{th}อยู่ที่ไหนครับ"),
    "HAVE":    ("mii {ph} mǎi khráp", "มี{th}ไหมครับ"),
    "ORDER":   ("khǎw {ph} nòi khráp", "ขอ{th}หน่อยครับ"),
    "VERY":    ("{ph} mâak khráp", "{th}มากครับ"),
    "TOOMUCH": ("{ph} pai nòi khráp", "{th}ไปหน่อยครับ"),
    "ABIT":    ("{ph} nít nòi khráp", "{th}นิดหน่อยครับ"),
    "ISIT":    ("{ph} mǎi khráp", "{th}ไหมครับ"),
}


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as fh:
        return json.load(fh)


def save(fn, payload):
    with open(os.path.join(DATA, fn), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)


def make_example(ex, ph, th):
    """Zwraca (polski, fonetyka, tajski) dla przykladu uzycia."""
    if len(ex) == 3:
        return ex
    pl, pat = ex
    tpl_ph, tpl_th = PAT[pat]
    return (pl, tpl_ph.replace("{ph}", ph), tpl_th.replace("{th}", th))


def refresh_counters():
    """Przelicza categories.json, metadata.json i manifest.json na podstawie
    faktycznej zawartosci katalogu data/. Uzywane przez stage2.py i przez
    stage2_cleanup.py, zeby liczniki nigdy nie rozjechaly sie z danymi."""
    final = []
    counts = {}
    for fn in VOCAB_FILES:
        data = load(fn)
        counts[fn] = data["count"]
        final.extend(data["records"])
    dlg_file = load("dialogues-part-01.json")
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
            "Pytania": "question", "Pogoda i przyroda": "weather"}

    categories = [{
        "id": "cat-%02d" % i,
        "name": name,
        "icon": ICON.get(name, "dot"),
        "count": cnt,
        "subcategories": [{"name": s, "count": c} for s, c in sorted(subs[name].items())],
    } for i, (name, cnt) in enumerate(sorted(cats.items()), 1)]
    save("categories.json", {"file": "categories.json", "count": len(categories),
                             "records": categories})

    # ----------------------------------------------------- metadane i manifest
    grammar = load("grammar.json")
    pron = load("pronunciation.json")

    metadata = load("metadata.json")
    metadata["version"] = VERSION
    metadata["levels"] = dict(levels)
    metadata["totalRecords"] = len(final)
    metadata["dialogues"] = dlg_file["count"]
    metadata["dialogueLines"] = dlg_file["lineCount"]
    metadata["grammarTopics"] = grammar["count"]
    metadata["updated"] = UPDATED
    save("metadata.json", metadata)

    manifest = load("manifest.json")
    manifest["version"] = VERSION
    manifest["updated"] = UPDATED
    manifest["cacheKey"] = "thai-aio-data-v" + VERSION
    for f in manifest["dataFiles"]:
        if f["file"] in counts:
            f["count"] = counts[f["file"]]
        elif f["file"] == "dialogues-part-01.json":
            f["count"] = dlg_file["count"]
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
    manifest["totalDialogues"] = dlg_file["count"]
    save("manifest.json", manifest)
    return counts, final, dlg_file


def main():
    # ----------------------------------------------------- stan istniejacy
    existing = {fn: load(fn) for fn in VOCAB_FILES}
    all_records = []
    for fn in VOCAB_FILES:
        all_records.extend(existing[fn]["records"])

    builder = Builder()
    # licznik ID: kontynuujemy numeracje, nie zaczynamy od zera
    for rec in all_records:
        rid = rec["id"]
        prefix, num = rid.rsplit("-", 1)
        builder.counter[prefix] = max(builder.counter.get(prefix, 0), int(num))
        builder.ids.add(rid)
        builder.seen_key.add((strip_tones(rec["polish"]).lower(), rec["ttsThai"]))

    # dodatkowa deduplikacja po samym polskim hasle
    seen_polish = {strip_tones(r["polish"]).lower() for r in all_records}
    rejected = []

    def build(level, pl, ph, th, cat, sub, rtype, tags, freq, note, literal, ex, source):
        key = strip_tones(pl).lower()
        if key in seen_polish:
            rejected.append((pl, "haslo juz istnieje w bazie"))
            return None
        rec = builder.make(level, pl, ph, th, cat, sub, rtype, tags,
                           freq=freq, notes=note, literal=literal,
                           register="uprzejmy" if ("khráp" in ph or "khâ" in ph) else "neutralny",
                           examples=[ex])
        if rec is None:
            rejected.append((pl, "para (polski, tajski) juz istnieje"))
            return None
        seen_polish.add(key)
        rec["source"] = source
        return rec

    # ----------------------------------------------------- rekordy rdzenne
    core_records = []
    core_index = {}
    for pl, ph, th, cat, sub, rtype, freq, note, literal, ex in CORE2S:
        rec = build("A1", pl, ph, th, cat, sub, rtype,
                    sorted({cat.split()[0].lower(), sub.split()[0].lower(), "słownictwo"}),
                    freq, note, literal, make_example(ex, ph, th), SRC_CORE)
        if rec:
            core_records.append(rec)
        core_index[pl] = (ph, th, cat, sub, freq)

    # ----------------------------------------------------- rekordy szablonowe
    tpl_records = []
    for tpl in TEMPLATES2:
        for rec_pl, base_pl, ex_pl in tpl["items"]:
            if base_pl not in core_index:
                raise SystemExit("Wzorzec %s wskazuje na nieznane haslo: %s" % (tpl["key"], base_pl))
            ph_b, th_b, cat_b, sub_b, freq_b = core_index[base_pl]
            ph = tpl["ph"].replace("{ph}", ph_b)
            th = tpl["th"].replace("{th}", th_b)
            ex = (ex_pl,
                  tpl["ex_ph"].replace("{ph}", ph_b),
                  tpl["ex_th"].replace("{th}", th_b))
            rec = build("A1", rec_pl, ph, th, tpl["cat"], tpl["sub"], tpl["ty"],
                        sorted({"zwroty", tpl["cat"].split()[0].lower(), "wzorzec"}),
                        max(2, freq_b - 1), tpl["note"], tpl["lit"], ex, SRC_TPL)
            if rec:
                tpl_records.append(rec)

    # ----------------------------------------------------- przyciecie do celu
    need = TARGET_A1_02 - existing["a1-part-02.json"]["count"]
    if need < 0:
        raise SystemExit("Plik a1-part-02.json ma juz wiecej niz %d rekordow." % TARGET_A1_02)

    tpl_take = min(TEMPLATE_QUOTA, len(tpl_records), need)
    core_take = need - tpl_take
    if core_take > len(core_records):
        raise SystemExit("Za malo rekordow rdzennych: mam %d, potrzeba %d."
                         % (len(core_records), core_take))

    # nadmiar rdzenia odkladamy na etap 3 — wypadaja hasla o najnizszej frekwencji.
    # Hasla bazowe wzorcow sa chronione: rekord szablonowy bez swojego slowa
    # bazowego zostawilby w bazie dziure dydaktyczna.
    protected = {base for tpl in TEMPLATES2 for _, base, _ in tpl["items"]}
    order = sorted(range(len(core_records)),
                   key=lambda i: (core_records[i]["polish"] not in protected,
                                  -core_records[i]["frequency"], i))
    keep = set(order[:core_take])
    core_used = [r for i, r in enumerate(core_records) if i in keep]
    deferred = [r for i, r in enumerate(core_records) if i not in keep]

    new_records = core_used + tpl_records[:tpl_take]
    if len(new_records) != need:
        raise SystemExit("Blad arytmetyki: %d != %d" % (len(new_records), need))

    part2 = existing["a1-part-02.json"]
    part2["records"].extend(new_records)
    part2["count"] = len(part2["records"])
    save("a1-part-02.json", part2)

    if deferred:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "reserve-stage3.json"), "w", encoding="utf-8") as fh:
            json.dump({"note": "Hasla gotowe, odlozone na etap 3 (limit A1 wyczerpany).",
                       "count": len(deferred),
                       "records": [{"polish": r["polish"], "thaiPhonetic": r["thaiPhonetic"],
                                    "ttsThai": r["ttsThai"], "category": r["category"],
                                    "subcategory": r["subcategory"]} for r in deferred]},
                      fh, ensure_ascii=False, indent=1)

    # ----------------------------------------------------- dialogi
    dlg_file = load("dialogues-part-01.json")
    seen_titles = {d["title"] for d in dlg_file["records"]}
    next_num = max(int(d["id"].rsplit("-", 1)[1]) for d in dlg_file["records"]) + 1
    added_dlg = 0
    for title, sit, level, ra, rb, lines, note in DIALOGUES2:
        if title in seen_titles:
            continue
        if not 4 <= len(lines) <= 16:
            raise SystemExit("Dialog „%s” ma %d kwestii (dozwolone 4-16)." % (title, len(lines)))
        dlg_file["records"].append({
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
        seen_titles.add(title)
        next_num += 1
        added_dlg += 1
    dlg_file["count"] = len(dlg_file["records"])
    dlg_file["lineCount"] = sum(len(d["lines"]) for d in dlg_file["records"])
    save("dialogues-part-01.json", dlg_file)

    counts, final, dlg_file = refresh_counters()


    # ----------------------------------------------------- raport
    print("=" * 58)
    print("ETAP 2 — DOMKNIECIE POZIOMU A1")
    print("=" * 58)
    print("  rekordy rdzenne dopisane   %5d" % len(core_used))
    print("  rekordy szablonowe dopisane%5d" % tpl_take)
    print("  odrzucone duplikaty        %5d" % len(rejected))
    print("  odlozone na etap 3         %5d" % len(deferred))
    print("  nowe dialogi               %5d" % added_dlg)
    print("-" * 58)
    for fn in VOCAB_FILES:
        print("  %-26s %5d" % (fn, counts[fn]))
    print("  %-26s %5d" % ("dialogues-part-01.json", dlg_file["count"]))
    print("  %-26s %5d" % ("RAZEM rekordow", len(final)))
    print("  %-26s %5d" % ("kwestii w dialogach", dlg_file["lineCount"]))
    for pl, why in rejected[:15]:
        print("  ODRZUCONO: %-40s %s" % (pl, why))
    return 0


if __name__ == "__main__":
    sys.exit(main())
