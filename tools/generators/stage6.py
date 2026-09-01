#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Etap 6 — uzupelnienie bazy powyzej 10 000 rekordow.

Skrypt robi trzy rzeczy i jest w calosci idempotentny:

  1. CZYSZCZENIE. Usuwa 16 rekordow, ktore audyt wskazal jako faktyczne
     duplikaty (ta sama fonetyka ORAZ to samo zdanie tajskie, przy praktycznie
     tym samym polskim znaczeniu). Polskie warianty znaczeniowe przenosi do
     pola polishAlternatives rekordu zachowanego, zeby nie stracic mozliwosci
     wyszukania. Naprawia relatedWords wskazujace na usuniete ID.
     Homofon „sâwm” (widelec / naprawiac) zostaje — to dwa rozne slowa tajskie.

  2. ODZYSK. Odtwarza pule etapu 5 z tych samych plikow zrodlowych. Wszystko,
     co juz jest w bazie, odpada na deduplikacji; zostaje dokladnie material
     odlozony wtedy z powodu limitu 2000 rekordow na poziom B2.

  3. UZUPELNIENIE. Buduje nowy material etapu 6 (rdzen + wzorce zdaniowe)
     i zapisuje data/supplemental-practical.json z taka liczba rekordow, zeby
     baza mialla dokladnie TARGET pozycji. Nadwyzka idzie do reserve-stage7.json.

Na koniec przelicza categories.json, metadata.json i manifest.json.

Uruchomienie (z katalogu tools/generators):
    python3 stage6.py
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Builder, strip_tones                                     # noqa: E402

# --- material etapu 5, potrzebny do odzysku odlozonych rekordow -------------
from lex_b2_core_a import CORE_A                                            # noqa: E402
from lex_b2_core_b import CORE_B                                            # noqa: E402
from lex_b2_core_c import CORE_C                                            # noqa: E402
from lex_b2_core_d import CORE_D                                            # noqa: E402
from lex_b2_core_e import CORE_E                                            # noqa: E402
from lex_b2_core_f import CORE_F                                            # noqa: E402
from lex_b2_core_g import CORE_G                                            # noqa: E402
from lex_b2_idioms import CORE_IDIOM                                        # noqa: E402
from lex_b2_register import CORE_REGISTER                                   # noqa: E402
from lex_b2_tpl_a import TPL_A                                              # noqa: E402
from lex_b2_tpl_b import TPL_B as B2_TPL_B                                  # noqa: E402
from lex_b2_tpl_c import TPL_C as B2_TPL_C                                  # noqa: E402
from lex_b2_tpl_d import TPL_D as B2_TPL_D                                  # noqa: E402
from lex_b2_tpl_e import TPL_E                                              # noqa: E402
from lex_b2_tpl_f import TPL_F                                              # noqa: E402

# --- material etapu 6 -------------------------------------------------------
from lex_s6_verbs import VERBS                                              # noqa: E402
from lex_s6_adj import ADJ                                                  # noqa: E402
from lex_s6_react import REACT                                              # noqa: E402
from lex_s6_travel import TRAVEL                                            # noqa: E402
from lex_s6_safety import SAFETY                                            # noqa: E402
from lex_s6_life import LIFE                                                # noqa: E402
from lex_s6_tpl import TPL                                                  # noqa: E402
from lex_s6_tpl_b import TPL_B                                              # noqa: E402
from lex_s6_tpl_c import TPL_C                                              # noqa: E402
from lex_s6_tpl_d import TPL_D                                              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")
HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = "1.5.0"
UPDATED = "2026-08-16"

SUPP_FILE = "supplemental-practical.json"
TARGET = 10200                     # 10 000 z zapasem 200 (widelki 100-300)

REGISTER = {"n": "neutralny", "f": "formalny", "i": "nieformalny", "p": "potoczny"}

SRC_CORE = "Rdzeń opracowany ręcznie — etap 6 (zweryfikowany)"
SRC_TPL = "Wzorzec zdaniowy z białej listy słów — etap 6"
SRC_RECOVER = "Materiał odłożony w etapie 5, odzyskany w etapie 6"

# ---------------------------------------------------------------- czyszczenie
# Rekordy do usuniecia: te same zdanie tajskie i to samo znaczenie praktyczne
# co rekord zachowany. Lista pochodzi z tools/audit-quality.py (punkt 2).
DROP_IDS = [
    "srv-adj-0031", "srv-adj-0033", "a1-shop-0092", "a1-verb-0612",
    "a1-adj-0073", "a1-adj-0028", "a1-transport-0062", "a1-num-0027",
    "a1-time-0109", "a1-resto-0040", "a1-verb-0610", "a1-adj-0204",
    "a1-time-0099", "a1-verb-0085", "a1-verb-0435", "b1-shop-0025",
]
# Polskie warianty znaczeniowe przenoszone do rekordu zachowanego,
# zeby wyszukiwarka nadal je znajdowala.
MERGE_ALTERNATIVES = {
    "a1-resto-0004": ["kubek"],
    "a1-adj-0013": ["zły, wściekły"],
    "a1-verb-0023": ["odpocząć"],
    "srv-verb-0025": ["wysiąść"],
    "srv-shop-0017": ["torba na zakupy"],
}
# Zastapienia w relatedWords po usunieciu rekordu.
REDIRECT = {
    "srv-adj-0031": "srv-basic-0005", "srv-adj-0033": "srv-basic-0025",
    "a1-shop-0092": "srv-shop-0017", "a1-verb-0612": "srv-verb-0025",
    "a1-adj-0073": "srv-resto-0011", "a1-adj-0028": "srv-resto-0019",
    "a1-transport-0062": "srv-transport-0025", "a1-num-0027": "srv-num-0022",
    "a1-time-0109": "srv-time-0019", "a1-resto-0040": "a1-resto-0004",
    "a1-verb-0610": "a1-verb-0023", "a1-adj-0204": "a1-adj-0013",
    "a1-time-0099": "a1-time-0011", "a1-verb-0085": "a1-verb-0614",
    "a1-verb-0435": "a1-verb-0634", "b1-shop-0025": "b2-shop-0017",
}

# Poziom przypisany rekordom z poszczegolnych wzorcow etapu 6.
TPL_LEVEL = {
    "YAALUEM": "A2", "HAIPHOMEENG": "B1", "MAIWAI": "B1", "KHOEIMAI": "A2",
    "TAWNGKAAN": "B1", "SAAMAAT": "B1", "PHRAWMJA": "B1", "TEMJAI": "B1",
    "WAIKAWN": "B1", "KANTHOE": "A2", "MIIKHRAI": "A2", "TRONGNAIDII": "A2",
    "MAIMIILOEI": "A2", "THAEWNII": "A2", "MAICHAIADJ": "B1",
    "BAWKYANGNGAI": "A2", "LAEWRUEYANG": "A2", "MAIRUUYANGNGAI": "A2",
    "PHISEET": "B1", "SONGSAI": "B1", "DIIKWAANII": "A2", "ANNAIDII": "A2",
    "HAAIPAINAI": "B1", "KIIKHRANG": "A2", "WANNAIBAANG": "A2",
    "PHAEALLERG": "A2", "PHOEMIIK": "A2", "THAMJAAK": "A2",
    "BAEPMAIPHET": "A2", "DUAIKAN": "A2", "THAMMAITAWNG": "A2",
    "KHONUEN": "B1", "WANUEN": "A2", "HAIREWNOI": "A2", "HAAM": "A2",
    "KHAWNGKHRAI": "A2", "JAAIKHAA": "A2", "SAMRAPDEK": "A2",
    "RAAKHAATHAORAI": "A2", "THUKKHON": "A2",
}

CORE_S6 = VERBS + ADJ + REACT + TRAVEL + SAFETY + LIFE
TPL_S6 = TPL + TPL_B + TPL_C + TPL_D
B2_CORE_PLAIN = CORE_A + CORE_B + CORE_C + CORE_D + CORE_E + CORE_F + CORE_G
B2_TPL_ALL = TPL_A + B2_TPL_B + B2_TPL_C + B2_TPL_D + TPL_E + TPL_F

ICON = {"Jedzenie i napoje": "food", "Restauracja": "resto", "Transport": "transport",
        "Hotel": "hotel", "Zakupy i pieniądze": "shop", "Zdrowie": "health",
        "Miejsca i orientacja": "map", "Podstawy i grzeczność": "hello",
        "Ludzie i rodzina": "people", "Czas i daty": "clock", "Liczby i liczenie": "num",
        "Czasowniki": "verb", "Cechy i opinie": "star", "Awarie i pomoc": "alert",
        "Small talk": "chat", "Dom i codzienność": "home", "Praca i nauka": "work",
        "Pytania": "question", "Pogoda i przyroda": "weather",
        "Gramatyka użytkowa": "dict"}


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as fh:
        return json.load(fh)


def save(fn, payload):
    with open(os.path.join(DATA, fn), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)


# ============================================================== 1. CZYSZCZENIE
def cleanup(manifest):
    """Usuwa duplikaty z plikow poziomow. Dziala tylko wtedy, gdy jest co usunac."""
    vocab = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "vocabulary"]
    removed, merged, fixed = 0, 0, 0

    for fn in vocab:
        data = load(fn)
        recs = data["records"]
        before = len(recs)
        recs = [r for r in recs if r["id"] not in DROP_IDS]
        removed += before - len(recs)

        for rec in recs:
            extra = MERGE_ALTERNATIVES.get(rec["id"])
            if extra:
                alts = rec.get("polishAlternatives") or []
                for a in extra:
                    if a not in alts:
                        alts.append(a)
                        merged += 1
                rec["polishAlternatives"] = alts
            rel = rec.get("relatedWords") or []
            if any(x in REDIRECT for x in rel):
                new = []
                for x in rel:
                    y = REDIRECT.get(x, x)
                    if y != rec["id"] and y not in new:
                        new.append(y)
                fixed += 1
                rec["relatedWords"] = new

        if before != len(recs) or merged or fixed:
            data["count"] = len(recs)
            data["records"] = recs
            save(fn, data)
    return removed, merged, fixed


# =============================================== wspolny konstruktor rekordow
class Pool(object):
    def __init__(self, base_records):
        self.builder = Builder()
        for rec in base_records:
            prefix, num = rec["id"].rsplit("-", 1)
            self.builder.counter[prefix] = max(self.builder.counter.get(prefix, 0), int(num))
            self.builder.ids.add(rec["id"])
            self.builder.seen_key.add((strip_tones(rec["polish"]).lower(), rec["ttsThai"]))
        self.seen_polish = {strip_tones(r["polish"]).lower() for r in base_records}
        self.seen_thai = {r["ttsThai"] for r in base_records}
        self.rejected = collections.Counter()
        self.base_index = {}
        for rec in base_records:
            self.base_index.setdefault(rec["polish"],
                                       (rec["thaiPhonetic"], rec["ttsThai"],
                                        rec["category"], rec["subcategory"], rec["frequency"]))

    def build(self, level, pl, ph, th, cat, sub, rtype, tags, freq, reg,
              note, literal, ex, source):
        key = strip_tones(pl).lower()
        if key in self.seen_polish:
            self.rejected["polskie hasło już istnieje"] += 1
            return None
        if th in self.seen_thai:
            self.rejected["zdanie tajskie już istnieje"] += 1
            return None
        rec = self.builder.make(level, pl, ph, th, cat, sub, rtype, tags,
                                freq=freq, register=REGISTER[reg], notes=note,
                                literal=literal, examples=[ex])
        if rec is None:
            self.rejected["para (polski, tajski) już istnieje"] += 1
            return None
        self.seen_polish.add(key)
        self.seen_thai.add(th)
        rec["source"] = source
        return rec

    def run_templates(self, templates, level_of, tag_level, source):
        out = []
        for tpl in templates:
            for rec_pl, base_pl, ex_pl in tpl["items"]:
                if base_pl not in self.base_index:
                    raise SystemExit("Wzorzec %s wskazuje na nieznane hasło: %r"
                                     % (tpl["key"], base_pl))
                ph_b, th_b, _c, _s, freq_b = self.base_index[base_pl]
                ph = tpl["ph"].replace("{ph}", ph_b)
                th = tpl["th"].replace("{th}", th_b)
                ex = (ex_pl,
                      tpl["ex_ph"].replace("{ph}", ph_b),
                      tpl["ex_th"].replace("{th}", th_b))
                lvl = level_of(tpl)
                tags = sorted({"zwroty", tpl["cat"].split()[0].lower(),
                               "wzorzec", tag_level})
                rec = self.build(lvl, rec_pl, ph, th, tpl["cat"], tpl["sub"], tpl["ty"],
                                 tags, max(2, min(5, freq_b - 1)), tpl["reg"],
                                 tpl["note"], tpl["lit"], ex, source)
                if rec:
                    out.append(rec)
        return out


def main():
    manifest = load("manifest.json")
    removed, merged, fixed = cleanup(manifest)

    vocab_files = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "vocabulary"]
    vocab_files = [f for f in vocab_files if f != SUPP_FILE]
    base_records = []
    for fn in vocab_files:
        base_records.extend(load(fn)["records"])

    pool = Pool(base_records)

    # Hasla przeniesione do polishAlternatives musza dalej dzialac jako klucze
    # bialych list — inaczej wzorce etapu 5 przestalyby sie odtwarzac.
    by_id = {r["id"]: r for r in base_records}
    for keep_id, alts in MERGE_ALTERNATIVES.items():
        keep = by_id.get(keep_id)
        if not keep:
            continue
        for alias in alts:
            pool.base_index.setdefault(alias, (keep["thaiPhonetic"], keep["ttsThai"],
                                               keep["category"], keep["subcategory"],
                                               keep["frequency"]))

    # ------------------------------------------------- 2. ODZYSK Z ETAPU 5
    def run_core_b2(source, rows, extra_tag):
        out = []
        for pl, ph, th, cat, sub, rtype, freq, reg, note, literal, ex in rows:
            pool.base_index.setdefault(pl, (ph, th, cat, sub, freq))
            tags = sorted({cat.split()[0].lower(), sub.split()[0].lower(),
                           "słownictwo", "b2", extra_tag})
            rec = pool.build("B2", pl, ph, th, cat, sub, rtype, tags, freq, reg,
                             note, literal, ex, source)
            if rec:
                out.append(rec)
        return out

    recovered = []
    recovered += run_core_b2(SRC_RECOVER, B2_CORE_PLAIN, "rozmowa")
    recovered += run_core_b2(SRC_RECOVER, CORE_IDIOM, "idiom")
    recovered += run_core_b2(SRC_RECOVER, CORE_REGISTER, "rejestr")
    recovered += pool.run_templates(B2_TPL_ALL, lambda t: "B2", "b2", SRC_RECOVER)

    # ------------------------------------------------ 3. NOWY MATERIAL ETAPU 6
    core_new = []
    for lvl, pl, ph, th, cat, sub, rtype, freq, reg, note, literal, ex in CORE_S6:
        pool.base_index.setdefault(pl, (ph, th, cat, sub, freq))
        tags = sorted({cat.split()[0].lower(), sub.split()[0].lower(),
                       "słownictwo", lvl.lower(), "praktyka"})
        rec = pool.build(lvl, pl, ph, th, cat, sub, rtype, tags, freq, reg,
                         note, literal, ex, SRC_CORE)
        if rec:
            core_new.append(rec)

    tpl_new = pool.run_templates(TPL_S6, lambda t: TPL_LEVEL[t["key"]],
                                 "praktyka", SRC_TPL)

    # rdzen recznie opracowany idzie pierwszy — to material najcenniejszy
    supply = core_new + recovered + tpl_new
    need = TARGET - len(base_records)
    if need < 0:
        raise SystemExit("Baza ma juz %d rekordow, wiecej niz cel %d."
                         % (len(base_records), TARGET))
    if len(supply) < need:
        raise SystemExit(
            "Za mało materiału: mam %d nowych rekordów, potrzeba %d.\n"
            "Rozszerz białe listy w tools/generators/lex_s6_tpl*.py."
            % (len(supply), need))

    used, deferred = supply[:need], supply[need:]
    save(SUPP_FILE, {"file": SUPP_FILE, "count": len(used), "records": used})

    with open(os.path.join(HERE, "reserve-stage7.json"), "w", encoding="utf-8") as fh:
        json.dump({"note": "Hasła gotowe, odłożone na etap 7 (cel 10 200 osiągnięty).",
                   "count": len(deferred),
                   "records": [{"polish": r["polish"], "thaiPhonetic": r["thaiPhonetic"],
                                "ttsThai": r["ttsThai"], "category": r["category"],
                                "subcategory": r["subcategory"], "level": r["level"]}
                               for r in deferred]}, fh, ensure_ascii=False, indent=1)

    counts, total, dlg_files = refresh_counters()

    # ------------------------------------------------------------------ raport
    print("=" * 60)
    print("ETAP 6 — UZUPEŁNIENIE BAZY")
    print("=" * 60)
    print("  usunięte duplikaty            %5d" % removed)
    print("  scalone warianty polskie      %5d" % merged)
    print("  naprawione relatedWords       %5d" % fixed)
    print("  baza po czyszczeniu           %5d" % len(base_records))
    print("-" * 60)
    print("  odzyskane z rezerwy etapu 5   %5d" % len(recovered))
    print("  nowy rdzeń etapu 6            %5d" % len(core_new))
    print("  nowe rekordy wzorcowe         %5d" % len(tpl_new))
    print("  pula łącznie                  %5d" % len(supply))
    print("  odrzucone duplikaty           %5d" % sum(pool.rejected.values()))
    for why, n in pool.rejected.most_common():
        print("     %-34s %5d" % (why, n))
    print("  zapisane do %s  %5d" % (SUPP_FILE, len(used)))
    print("  odłożone na etap 7            %5d" % len(deferred))
    print("-" * 60)
    for fn, c in counts.items():
        print("  %-28s %5d" % (fn, c))
    print("  %-28s %5d" % ("RAZEM rekordów", total))
    for fn, d in dlg_files.items():
        print("  %-28s %5d dialogów, %d kwestii" % (fn, d["count"], d["lineCount"]))
    return 0


def refresh_counters():
    manifest = load("manifest.json")
    known = {f["file"] for f in manifest["dataFiles"]}
    if SUPP_FILE not in known:
        manifest["dataFiles"].append({"file": SUPP_FILE, "kind": "vocabulary",
                                      "level": "A2/B1", "count": 0})
    manifest["plannedFiles"] = [f for f in manifest.get("plannedFiles", [])
                                if f["file"] != SUPP_FILE]

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

    metadata = load("metadata.json")
    metadata["version"] = VERSION
    metadata["levels"] = dict(levels)
    metadata["totalRecords"] = len(final)
    metadata["dialogues"] = total_dlg
    metadata["dialogueLines"] = total_lines
    metadata["exampleSentences"] = examples
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
