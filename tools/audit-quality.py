#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audyt jakości bazy Thai All-in-One (etap 6).

Odpowiada na pytania kontrolne przed uzupełnieniem bazy do 10 000 rekordów:
liczby rzeczywiste, duplikaty w czterech ujęciach, braki pól, martwe odwołania,
zgodność liczników w manifeście i metadanych, pochodzenie rekordów.

Uruchomienie:  python3 tools/audit-quality.py
"""
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
THAI = re.compile(r"[\u0E00-\u0E7F]")

REQUIRED = ["id", "type", "polish", "thaiPhonetic", "pronunciationPolish", "ttsThai",
            "syllables", "toneGuide", "category", "subcategory", "level",
            "difficulty", "frequency", "register", "tags", "examples"]


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as fh:
        return json.load(fh)


def norm(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def table(title, headers, rows):
    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(str(cell)))
    line = "  ".join("-" * w for w in widths)
    print("\n" + title)
    print(line)
    print("  ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers)))
    print(line)
    for r in rows:
        print("  ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)))
    print(line)


SESSION_N = "Sesja N — rozszerzenie leksykalne (pokrycie mowy potocznej)"
LEX_TYPES = {"word", "noun", "verb", "adjective", "adverb"}


def audit_session_n(records):
    """Kontrola materiału sesji N. Zwraca liczbę znalezionych problemów.

    Sesja N dołożyła 935 haseł i 3 740 zdań aktywujących. Materiał jest
    odfiltrowywalny po polu `source`, więc da się go skontrolować osobno —
    i trzeba, bo wchodził hurtem z szablonów, a nie ręcznie po jednym.

    Sprawdzamy pięć rzeczy, każdą z osobnym powodem:

    1. **Warunek dydaktyczny.** Każde nowe hasło musi mieć w bazie co najmniej
       trzy zdania, w których występuje. Bez tego hasło nie wejdzie do ścieżki
       i jest martwym wpisem w słowniku.
    2. **Zamknięcie sylabiczne zdań.** Zdanie aktywujące ma być zbudowane
       z materiału wcześniejszego plus samo hasło. Gdyby wnosiło własne nowe
       sylaby, przestałoby być aktywujące i stałoby się kolejną przeszkodą.
    3. **Duplikaty wewnątrz sesji** po fonetyce z tonami i po znaczeniu.
    4. **Odwołania.** relatedWords hasła muszą wskazywać istniejące rekordy.
    5. **Polska odmiana.** Zdania nie mogą wracać do konwencji „Poproszę: woda”
       — dwukropek przed hasłem w mianowniku był błędem usuniętym w sesji G
       i nie wolno mu wejść tylnymi drzwiami.
    """
    mine = [r for r in records if r.get("source") == SESSION_N]
    if not mine:
        print("\nSESJA N: brak materiału w bazie")
        return 0

    lex = [r for r in mine if r["type"] in LEX_TYPES]
    sent = [r for r in mine if r["type"] not in LEX_TYPES]
    ids = {r["id"] for r in records}

    # 1. warunek dydaktyczny — liczony na CAŁEJ bazie, nie tylko na sesji
    by_syl = collections.defaultdict(list)
    for r in records:
        if r["type"] in LEX_TYPES:
            continue
        for sy in set(r.get("syllables") or []):
            by_syl[sy].append(r)
    thin = []
    for r in lex:
        syls = set(r.get("syllables") or [])
        if not syls:
            thin.append((r["id"], r["polish"], 0))
            continue
        rare = min(syls, key=lambda s: len(by_syl[s]))
        n = sum(1 for u in by_syl[rare] if syls <= set(u["syllables"]))
        if n < 3:
            thin.append((r["id"], r["polish"], n))

    # 2. zamknięcie sylabiczne zdań aktywujących
    base_syl = set()
    for r in records:
        if r.get("source") != SESSION_N:
            base_syl |= set(r.get("syllables") or [])
    lex_syl = {r["id"]: set(r.get("syllables") or []) for r in lex}
    leaky = []
    for r in sent:
        owner = (r.get("relatedWords") or [None])[0]
        allowed = base_syl | lex_syl.get(owner, set())
        extra = [s for s in (r.get("syllables") or []) if s not in allowed]
        if extra:
            leaky.append((r["id"], ", ".join(sorted(set(extra))[:4])))

    # 3. duplikaty wewnątrz sesji
    seen_ph, seen_pl = {}, {}
    dph, dpl = [], []
    for r in lex:
        kph = re.sub(r"[\s-]+", "", r["thaiPhonetic"].lower())
        kpl = norm(re.sub(r"\(.*?\)", "", r["polish"]))
        if kph in seen_ph:
            dph.append((r["id"], seen_ph[kph], r["thaiPhonetic"]))
        else:
            seen_ph[kph] = r["id"]
        if kpl in seen_pl:
            dpl.append((r["id"], seen_pl[kpl], r["polish"]))
        else:
            seen_pl[kpl] = r["id"]

    # 4. martwe odwołania
    dead = [(r["id"], w) for r in mine
            for w in (r.get("relatedWords") or []) if w not in ids]

    # 5. nawrót konwencji „Poproszę: woda”
    colon = [(r["id"], r["polish"]) for r in mine
             if re.search(r":\s*\S", r.get("polish", ""))]

    print("\n" + "=" * 72)
    print("KONTROLA SESJI N")
    print("=" * 72)
    print("  haseł leksykalnych              %5d" % len(lex))
    print("  zdań aktywujących               %5d" % len(sent))
    print("  zdań na hasło                   %5.2f"
          % (len(sent) / max(1, len(lex))))
    print("  haseł poniżej 3 zdań            %5d" % len(thin))
    print("  zdań wnoszących obce sylaby     %5d" % len(leaky))
    print("  duplikatów fonetyki w sesji     %5d" % len(dph))
    print("  duplikatów znaczenia w sesji    %5d" % len(dpl))
    print("  martwych odwołań                %5d" % len(dead))
    print("  nawrotów konwencji z dwukropkiem%5d" % len(colon))

    for label, rows in (("HASŁA PONIŻEJ PROGU 3 ZDAŃ", thin),
                        ("ZDANIA Z OBCYMI SYLABAMI", leaky),
                        ("DUPLIKATY FONETYKI", dph),
                        ("DUPLIKATY ZNACZENIA", dpl),
                        ("MARTWE ODWOŁANIA", dead),
                        ("DWUKROPEK PRZED HASŁEM", colon)):
        if rows:
            print("\n  " + label)
            for row in rows[:15]:
                print("    " + "  ".join(str(c) for c in row))
            if len(rows) > 15:
                print("    … oraz %d dalszych" % (len(rows) - 15))

    return len(thin) + len(leaky) + len(dph) + len(dpl) + len(dead) + len(colon)


def main():
    manifest = load("manifest.json")
    metadata = load("metadata.json")
    vocab = [f for f in manifest["dataFiles"] if f["kind"] == "vocabulary"]
    dialog = [f for f in manifest["dataFiles"] if f["kind"] == "dialogues"]

    print("=" * 72)
    print("AUDYT JAKOŚCI BAZY THAI ALL-IN-ONE")
    print("=" * 72)

    # ---------------------------------------------------------- [1] liczby
    records, rows = [], []
    for d in vocab:
        data = load(d["file"])
        n = len(data["records"])
        rows.append([d["file"], d["level"], data.get("count", "-"), n,
                     "OK" if data.get("count") == n == d["count"] else "ROZBIEŻNOŚĆ"])
        records.extend(data["records"])
    dlg_records = []
    for d in dialog:
        data = load(d["file"])
        n = len(data["records"])
        rows.append([d["file"], d["level"], data.get("count", "-"), n,
                     "OK" if n == d["count"] else "ROZBIEŻNOŚĆ"])
        dlg_records.extend(data["records"])
    rows.append(["RAZEM słownik", "", "", len(records), ""])
    rows.append(["RAZEM dialogi", "", "", len(dlg_records), ""])
    table("[1] RZECZYWISTA LICZBA REKORDÓW",
          ["plik", "poziom", "pole count", "faktycznie", "zgodność"], rows)

    # ------------------------------------------------------ [2] duplikaty
    ids = collections.Counter(r.get("id") for r in records)
    dup_id = {k: v for k, v in ids.items() if v > 1}

    # Nie każde powtórzenie jest błędem, a liczenie ich razem zamieniało ten
    # audyt w narzędzie, które co przebieg melduje te same dziewięć „problemów”
    # i uczy, żeby je ignorować. Dwa powtórzenia są ZAMIERZONE:
    #
    #  · PARA GRZECZNOŚCIOWA — to samo zdanie z partykułą i bez niej
    #    („súe tǔa dâai thîi nǎi” / „...khráp”) albo w formie męskiej i
    #    żeńskiej („kàp phǒm” / „kàp chǎn”). Polskie tłumaczenie jest jedno,
    #    bo polszczyzna tej różnicy nie koduje — i to jest właśnie powód,
    #    dla którego oba rekordy istnieją.
    #
    #  · HOMOFON — dwa różne wyrazy tajskie o identycznym brzmieniu
    #    (ส้อม „widelec” i ซ่อม „naprawiać”, oba `sâwm`). Rozróżnia je
    #    wyłącznie kontekst, więc dla uczącego się to materiał, nie usterka.
    #    Poznajemy je po tym, że zapis tajski się RÓŻNI.
    #
    # Prawdziwym duplikatem jest dopiero zgodność tłumaczenia I fonetyki —
    # to nadal liczymy jako błąd, poniżej, w `dup_pair`.
    POLITE = ('khráp', 'khâ', 'khá', 'khráb', 'ná', 'kháp')
    PRONOUN = ('phǒm', 'chǎn', 'dì-chǎn')

    def _strip_markers(text):
        toks = [t for t in (text or '').split() if t]
        toks = [t for t in toks if t not in POLITE and t not in PRONOUN]
        return ' '.join(toks)

    by_pl = collections.defaultdict(list)
    for r in records:
        by_pl[norm(r.get("polish"))].append(r)
    dup_pl, polite_pairs = {}, {}
    for k, rs in by_pl.items():
        if len(rs) < 2:
            continue
        bare = {_strip_markers(norm(x.get("thaiPhonetic"))) for x in rs}
        (polite_pairs if len(bare) == 1 else dup_pl)[k] = len(rs)

    by_ph = collections.defaultdict(list)
    for r in records:
        by_ph[norm(r.get("thaiPhonetic"))].append(r)
    dup_ph, homophones = {}, {}
    for k, rs in by_ph.items():
        if len(rs) < 2:
            continue
        scripts = {x.get("ttsThai") for x in rs}
        (homophones if len(scripts) == len(rs) else dup_ph)[k] = len(rs)

    pair = collections.Counter((norm(r.get("polish")), norm(r.get("thaiPhonetic")))
                               for r in records)
    dup_pair = {k: v for k, v in pair.items() if v > 1}

    dlg_ids = collections.Counter(d.get("id") for d in dlg_records)
    dup_dlg = {k: v for k, v in dlg_ids.items() if v > 1}
    dlg_titles = collections.Counter(norm(d.get("title")) for d in dlg_records)
    dup_title = {k: v for k, v in dlg_titles.items() if v > 1}

    table("[2] DUPLIKATY", ["kryterium", "kluczy zdublowanych", "rekordów nadmiarowych"], [
        ["ID rekordu", len(dup_id), sum(dup_id.values()) - len(dup_id)],
        ["polskie tłumaczenie", len(dup_pl), sum(dup_pl.values()) - len(dup_pl)],
        ["  z tego pary grzecznościowe (zamierzone)", len(polite_pairs),
         sum(polite_pairs.values()) - len(polite_pairs)],
        ["fonetyka", len(dup_ph), sum(dup_ph.values()) - len(dup_ph)],
        ["  z tego homofony (zamierzone)", len(homophones),
         sum(homophones.values()) - len(homophones)],
        ["tłumaczenie + fonetyka", len(dup_pair), sum(dup_pair.values()) - len(dup_pair)],
        ["ID dialogu", len(dup_dlg), sum(dup_dlg.values()) - len(dup_dlg)],
        ["tytuł dialogu", len(dup_title), sum(dup_title.values()) - len(dup_title)],
    ])
    if dup_pl:
        print("\n    przykłady powtórzonego polskiego hasła (do 10):")
        for k, v in list(sorted(dup_pl.items(), key=lambda x: -x[1]))[:10]:
            print("      %-46s x%d" % (k[:46], v))
    if dup_ph:
        print("\n    przykłady powtórzonej fonetyki (do 10):")
        for k, v in list(sorted(dup_ph.items(), key=lambda x: -x[1]))[:10]:
            print("      %-46s x%d" % (k[:46], v))

    # ------------------------------------------------------- [3] braki pól
    miss = collections.Counter()
    empty = collections.Counter()
    for r in records:
        for f in REQUIRED:
            if f not in r:
                miss[f] += 1
            elif r[f] in ("", [], None):
                empty[f] += 1
    ex_miss = sum(1 for r in records for ex in r.get("examples", [])
                  if not (ex.get("polish") and ex.get("thaiPhonetic") and ex.get("ttsThai")))
    rows = [[f, miss.get(f, 0), empty.get(f, 0)] for f in REQUIRED
            if miss.get(f) or empty.get(f)]
    if not rows:
        rows = [["(wszystkie pola obecne i niepuste)", 0, 0]]
    rows.append(["przykłady z brakiem pola", ex_miss, ""])
    table("[3] BRAKUJĄCE POLA WYMAGANE PRZEZ SCHEMAT",
          ["pole", "brak klucza", "pusta wartość"], rows)

    # ------------------------------------------------- [4] relatedWords
    all_ids = set(ids)
    broken, with_rel, total_rel = [], 0, 0
    for r in records:
        rel = r.get("relatedWords") or []
        if rel:
            with_rel += 1
        for ref in rel:
            total_rel += 1
            if ref not in all_ids:
                broken.append((r["id"], ref))
    table("[4] ODWOŁANIA W relatedWords", ["miara", "wartość"], [
        ["rekordów z odwołaniami", with_rel],
        ["odwołań łącznie", total_rel],
        ["odwołań do nieistniejących ID", len(broken)],
    ])
    for rid, ref in broken[:10]:
        print("      %s -> %s" % (rid, ref))

    # ------------------------------------------- [5] manifest vs metadata
    lvl_actual = collections.Counter(r["level"] for r in records)
    rows = []
    for lv in ("Survival", "A1", "A2", "B1", "B2"):
        m = manifest["levels"].get(lv)
        d = metadata["levels"].get(lv)
        a = lvl_actual.get(lv, 0)
        rows.append([lv, m, d, a, "OK" if m == d == a else "ROZBIEŻNOŚĆ"])
    rows.append(["totalRecords", manifest["totalRecords"], metadata["totalRecords"],
                 len(records),
                 "OK" if manifest["totalRecords"] == metadata["totalRecords"] == len(records)
                 else "ROZBIEŻNOŚĆ"])
    rows.append(["dialogi", manifest["totalDialogues"], metadata["dialogues"],
                 len(dlg_records),
                 "OK" if manifest["totalDialogues"] == metadata["dialogues"] == len(dlg_records)
                 else "ROZBIEŻNOŚĆ"])
    lines = sum(len(d["lines"]) for d in dlg_records)
    rows.append(["kwestii w dialogach", "-", metadata.get("dialogueLines"), lines,
                 "OK" if metadata.get("dialogueLines") == lines else "ROZBIEŻNOŚĆ"])
    ex_total = sum(len(r.get("examples", [])) for r in records)
    rows.append(["przykładów zdań", "-", metadata.get("exampleSentences"), ex_total,
                 "OK" if metadata.get("exampleSentences") == ex_total else "ROZBIEŻNOŚĆ"])
    cats_actual = sorted({r["category"] for r in records})
    rows.append(["kategorii", len(manifest["categories"]), "-", len(cats_actual),
                 "OK" if sorted(manifest["categories"]) == cats_actual else "ROZBIEŻNOŚĆ"])
    table("[5] ZGODNOŚĆ LICZNIKÓW manifest.json / metadata.json",
          ["licznik", "manifest", "metadata", "faktycznie", "zgodność"], rows)

    # ----------------------------------------------------- [7] pochodzenie
    src = collections.Counter(r.get("source", "(brak pola source)") for r in records)
    core = sum(v for k, v in src.items() if "rdze" in k.lower() or "ręcz" in k.lower()
               or "reczn" in k.lower() or "weryf" in k.lower())
    tpl = len(records) - core
    rows = [[k[:52], v, "%.1f%%" % (100.0 * v / len(records))]
            for k, v in src.most_common()]
    table("[7] POCHODZENIE REKORDÓW (pole source)",
          ["source", "rekordów", "udział"], rows)
    print("    rdzeń zweryfikowany : %d (%.1f%%)" % (core, 100.0 * core / len(records)))
    print("    materiał wzorcowy   : %d (%.1f%%)" % (tpl, 100.0 * tpl / len(records)))

    # ------------------------------------------------- kontrola sesji N
    sesja_n = audit_session_n(records)

    # --------------------------------------------------------- podsumowanie
    problems = (len(dup_id) + len(dup_pl) + len(dup_ph) + len(dup_pair)
                + len(dup_dlg) + len(dup_title) + sum(miss.values())
                + sum(empty.values()) + len(broken) + ex_miss + sesja_n)
    print("\n" + "-" * 72)
    print("WYNIK AUDYTU:", "BEZ ZASTRZEŻEŃ" if problems == 0
          else "ZNALEZIONO %d PROBLEMÓW" % problems)
    return 0


if __name__ == "__main__":
    sys.exit(main())
