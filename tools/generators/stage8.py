#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Etap 8 (sesja G) — sesja naprawcza.

Nie dokłada poziomu ani nowego materiału. Poprawia to, co już jest, w miejscu,
z zachowaniem identyfikatorów. Trzy zadania:

1. **Polszczyzna.** Usuwa konwencję wstawki słownikowej („Poproszę: woda”)
   z pola `polish`, z przykładów i z kwestii dialogowych. Odmianę liczy
   `polish_grammar.py` na Morfeuszu, reguły zdaniowe trzyma `fix_polish.py`.
2. **Klasyfikatory.** Zastępuje `an` właściwym klasyfikatorem tam, gdzie
   rzeczownik ma swój własny. Buduje `data/classifiers.json` i rozbudowuje
   temat „Klasyfikatory” w `data/grammar.json`.
3. **Przykłady.** Uzupełnia rekordy typu `word` do dwóch przykładów.

Skrypt jest idempotentny: wszystkie trzy przebiegi rozpoznają stan docelowy
i przy powtórnym uruchomieniu nie zmieniają niczego.

Uruchomienie:

    cd tools/generators
    python3 stage8.py
    cd ../..
    python3 tools/build-offline-data.py
    python3 tools/validate.py
"""
import json
import os
import re
import sys
from collections import Counter

import classifiers as CL
import engine
import fix_polish as FP
import polish_grammar as PG

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "data")

VOCAB = [
    "survival.json", "a1-part-01.json", "a1-part-02.json",
    "a2-part-01.json", "a2-part-02.json",
    "b1-part-01.json", "b1-part-02.json", "b1-part-03.json",
    "b2-part-01.json", "b2-part-02.json",
    "supplemental-practical.json", "core-lexicon-01.json", "core-lexicon-02.json",
]
DIALOG = ["dialogues-part-01.json", "dialogues-part-02.json", "dialogues-part-03.json"]

stats = Counter()


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def save(name, payload):
    with open(os.path.join(DATA, name), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)


# ===========================================================================
# ZADANIE 1 — polszczyzna
# ===========================================================================
# Rekordy, w których zepsuta jest strona tajska, więc sama poprawka polska nie
# wystarcza. Cztery sztuki, każda opisana w raporcie sesji G.
THAI_REPAIRS = {
    # „phǒm pai kàp phǒm” = „idę razem ze sobą”; zaimek odsyła sam do siebie
    "a1-basic-0008": ("khun pai kàp phǒm", "คุณไปกับผม", "Idziesz razem ze mną."),
    "a1-basic-0009": ("khun pai kàp chǎn", "คุณไปกับฉัน", "Idziesz razem ze mną."),
    # „jà klàp mûea waan” = czas przyszły + „wczoraj”; sprzeczność także po tajsku
    "a1-time-0017": ("phǒm klàp mûea waan", "ผมกลับเมื่อวาน", "Wróciłem wczoraj."),
    "a1-time-0040": ("rao jəə kan mûea waan", "เราเจอกันเมื่อวาน", "Widzieliśmy się wczoraj."),
    "srv-time-0004": ("rao jəə kan mûea waan", "เราเจอกันเมื่อวาน", "Widzieliśmy się wczoraj."),
}

# Wzorzec „trochę za X” — zostają tylko przymiotniki, przy których brzmi
# naturalnie. Trzy pozostałe dostają inne sformułowanie.
TROCHE_ZA = {
    "a1-adj-0112": "aż za dobre",
    "a1-adj-0142": "trochę przepełnione",
    "a2-gram-0523": "trochę za bardzo — wzorzec nadmiaru",
}


def refresh_phonetics(obj, phonetic):
    """Przelicza pola pochodne po zmianie zapisu fonetycznego."""
    obj["thaiPhonetic"] = phonetic
    obj["pronunciationPolish"] = engine.polish_read(phonetic)
    obj["syllables"] = engine.syllables(phonetic)
    obj["toneGuide"] = engine.tone_guide(phonetic)
    obj["difficulty"] = engine.difficulty(phonetic)


def fix_record_polish(rec):
    """Przepisuje `polish`, `polishAlternatives` i przykłady jednego rekordu."""
    changed = False

    rep = THAI_REPAIRS.get(rec["id"])
    if rep and rec["thaiPhonetic"] != rep[0]:
        refresh_phonetics(rec, rep[0])
        rec["ttsThai"] = rep[1]
        rec["polish"] = rep[2]
        rec["notes"] = (rec.get("notes", "") + " Rekord poprawiony w sesji G: "
                        "poprzednia wersja miała sprzeczne zdanie tajskie.").strip()
        stats["thai_repaired"] += 1
        changed = True
    elif rec["id"] in TROCHE_ZA and rec["polish"] != TROCHE_ZA[rec["id"]]:
        rec["polish"] = TROCHE_ZA[rec["id"]]
        stats["troche_za"] += 1
        changed = True
    else:
        new, ok = FP.fix_text(rec["polish"], rec["thaiPhonetic"])
        if ok:
            rec["polish"] = new
            stats["polish_records"] += 1
            changed = True

    alts = []
    for a in rec.get("polishAlternatives", []):
        na, ok = FP.fix_text(a)
        if ok:
            stats["polish_alternatives"] += 1
            changed = True
        alts.append(na)
    if alts:
        rec["polishAlternatives"] = alts

    for ex in rec.get("examples", []):
        new, ok = FP.fix_text(ex["polish"], ex.get("thaiPhonetic", ""))
        if ok:
            ex["polish"] = new
            stats["polish_examples"] += 1
            changed = True
    return changed


# ===========================================================================
# ZADANIE 2 — klasyfikatory
# ===========================================================================
# `an` jest poprawne jako zaimek („an níi” = ten tutaj) — tych wystąpień nie
# ruszamy. Poprawiamy tylko `an` postawione przy rzeczowniku, który ma własny
# klasyfikator.
AN_PRONOUN = re.compile(r"\ban\s+(níi|nán|nǎi|ùen|lá)\b")
AN_TOKEN = re.compile(r"\ban\b")


def fix_classifier(obj):
    """Poprawia klasyfikator w jednym obiekcie (rekord albo przykład)."""
    ph = obj.get("thaiPhonetic", "")
    th = obj.get("ttsThai", "")
    if "อัน" not in th or not AN_TOKEN.search(ph):
        return None
    # zaimkowe „an níi” zostaje
    if AN_PRONOUN.search(ph) and len(AN_TOKEN.findall(ph)) == len(AN_PRONOUN.findall(ph)):
        return None

    hit = None
    for noun_th, (cls_ph, cls_th) in CL.CORRECTIONS.items():
        if noun_th in th:
            hit = (noun_th, cls_ph, cls_th)
            break
    if hit is None:
        return None
    _noun, cls_ph, cls_th = hit

    def repl(m):
        after = ph[m.end():m.end() + 8]
        if re.match(r"\s+(níi|nán|nǎi|ùen|lá)\b", after):
            return "an"
        return cls_ph

    new_ph = AN_TOKEN.sub(repl, ph)
    if new_ph == ph:
        return None
    obj["ttsThai"] = th.replace("อัน", cls_th)
    if "thaiPhonetic" in obj and "syllables" in obj:
        refresh_phonetics(obj, new_ph)
    else:
        obj["thaiPhonetic"] = new_ph
    return cls_ph


def build_classifiers_json():
    """Buduje `data/classifiers.json`."""
    records = []
    for i, entry in enumerate(CL.CLASSIFIERS, 1):
        ph, th, level, expl, nouns, examples = entry
        records.append({
            "id": "cls-%03d" % i,
            "classifier": ph,
            "pronunciationPolish": engine.polish_read(ph),
            "ttsThai": th,
            "level": level,
            "explanation": expl,
            "nouns": [
                {"polish": pl, "thaiPhonetic": nph,
                 "pronunciationPolish": engine.polish_read(nph), "ttsThai": nth}
                for pl, nph, nth in nouns
            ],
            "examples": [
                {"polish": pl, "thaiPhonetic": eph,
                 "pronunciationPolish": engine.polish_read(eph), "ttsThai": eth,
                 "audioFile": ""}
                for pl, eph, eth in examples
            ],
            "wordOrder": "rzeczownik + liczba + klasyfikator",
        })
    start = len(records)
    for j, (ph, th, level, expl, npl, nph, nth) in enumerate(CL.EXTRA, start + 1):
        records.append({
            "id": "cls-%03d" % j,
            "classifier": ph,
            "pronunciationPolish": engine.polish_read(ph),
            "ttsThai": th,
            "level": level,
            "explanation": expl,
            "nouns": [{"polish": npl, "thaiPhonetic": nph,
                       "pronunciationPolish": engine.polish_read(nph), "ttsThai": nth}],
            "examples": [{
                "polish": "Dwie sztuki — %s." % npl,
                "thaiPhonetic": "%s sǎwng %s" % (nph, ph),
                "pronunciationPolish": engine.polish_read("%s sǎwng %s" % (nph, ph)),
                "ttsThai": "%sสอง%s" % (nth, th),
                "audioFile": "",
            }],
            "wordOrder": "rzeczownik + liczba + klasyfikator",
        })
    payload = {"file": "classifiers.json", "count": len(records), "records": records}
    save("classifiers.json", payload)
    stats["classifier_records"] = len(records)
    return len(records)


GRAMMAR_EXPLANATION = (
    "Tajski nie liczy rzeczowników wprost. Między rzeczownikiem a liczbą musi "
    "stanąć klasyfikator — słowo mówiące, do jakiej klasy przedmiotów należy "
    "policzona rzecz. Szyk jest stały i odwrotny do polskiego: "
    "RZECZOWNIK + LICZBA + KLASYFIKATOR. „bia sǎwng khùat” to dosłownie "
    "„piwo dwie butelki”, czyli dwa piwa. Przy liczbie „jeden” mowa potoczna "
    "zwykle przestawia szyk: rzeczownik + klasyfikator + nùeng. "
    "Klasyfikator wybiera się według kształtu i przeznaczenia rzeczy, nie "
    "według znaczenia: ręcznik i koc dostają „phǔen” (płaskie tkaniny), "
    "klucz „dàwk” (wąski trzon), nóż „lêm” (ostrze, tak jak książka), "
    "łyżka i widelec „khan” (przedmiot z trzonkiem, tak jak samochód). "
    "„an” to worek na drobiazgi bez własnego klasyfikatora — postawione przy "
    "rzeczowniku, który swój klasyfikator ma, jest błędem. „an” pełni za to "
    "drugą, poprawną rolę: zaimka („an níi” — ten tutaj, „an nǎi” — który). "
    "Pełną tabelę klasyfikatorów zawiera plik danych classifiers.json."
)

GRAMMAR_PATTERNS = [
    ("Dwie osoby.", "sǎwng khon", "สองคน"),
    ("Dwa psy.", "mǎa sǎwng tua", "หมาสองตัว"),
    ("Poproszę dwa bilety.", "khǎw tǔa sǎwng bai", "ขอตั๋วสองใบ"),
    ("Poproszę jeszcze jeden ręcznik.", "khǎw phâa chét tua ìik phǔen nùeng", "ขอผ้าเช็ดตัวอีกผืนหนึ่ง"),
    ("Ile jest kluczy?", "mii kunjae kìi dàwk", "มีกุญแจกี่ดอก"),
    ("Poproszę jeszcze jedną łyżkę.", "khǎw cháwn ìik khan nùeng", "ขอช้อนอีกคันหนึ่ง"),
    ("Dwie książki.", "nǎng-sǔe sǎwng lêm", "หนังสือสองเล่ม"),
    ("Poproszę dwa ryże smażone.", "khǎw khâo phàt sǎwng jaan", "ขอข้าวผัดสองจาน"),
    ("Poproszę dwie butelki wody.", "khǎw náam plào sǎwng khùat", "ขอน้ำเปล่าสองขวด"),
    ("Dwa domy.", "bâan sǎwng lǎng", "บ้านสองหลัง"),
    ("Dwa mango.", "má-mûang sǎwng lûuk", "มะม่วงสองลูก"),
    ("Dwie pary butów.", "rawng tháo sǎwng khûu", "รองเท้าสองคู่"),
    ("Dwie tabletki.", "yaa sǎwng mét", "ยาสองเม็ด"),
    ("Dwa jajka.", "khài sǎwng fawng", "ไข่สองฟอง"),
    ("Poproszę dwa plastry.", "khǎw phlaastəə sǎwng phàen", "ขอพลาสเตอร์สองแผ่น"),
    ("Poproszę jedno mydło.", "khǎw sabùu nùeng kâwn", "ขอสบู่หนึ่งก้อน"),
    ("Dwa samochody.", "rót yon sǎwng khan", "รถยนต์สองคัน"),
    ("Ten tutaj.", "an níi", "อันนี้"),
    ("Który z nich?", "an nǎi", "อันไหน"),
    ("Poproszę dwie sztuki.", "khǎw sǎwng an", "ขอสองอัน"),
]


def extend_grammar():
    data = load("grammar.json")
    for topic in data["records"]:
        if topic["title"] != "Klasyfikatory":
            continue
        topic["explanation"] = GRAMMAR_EXPLANATION
        topic["patterns"] = [
            {"polish": pl, "thaiPhonetic": ph,
             "pronunciationPolish": engine.polish_read(ph), "ttsThai": th}
            for pl, ph, th in GRAMMAR_PATTERNS
        ]
        topic["tip"] = ("Kolejność jest odwrotna niż po polsku: najpierw rzecz, "
                        "potem liczba, na końcu klasyfikator. Nie zgadujesz "
                        "klasyfikatora — uczysz się go razem z rzeczownikiem, "
                        "tak jak rodzaju gramatycznego w polskim.")
        topic["classifierTable"] = [
            {"classifier": c[0], "ttsThai": c[1], "use": c[3].split(".")[0]}
            for c in CL.CLASSIFIERS
        ]
        stats["grammar_topic"] = 1
        break
    save("grammar.json", data)


# ===========================================================================
# ZADANIE 3 — drugi przykład dla rekordów typu `word`
# ===========================================================================
# Ramy zdaniowe: (polski szablon, fonetyka, pismo). {x} to hasło rekordu.
FRAMES = {
    "verb": ("Chcę {x}.", "yàak {ph} khráp", "อยาก{th}ครับ"),
    # bez „to jest”, żeby nie wymuszać uzgodnienia rodzaju na haśle podanym
    # w formie słownikowej („to jest bardzo suchy” byłoby błędem)
    "adj": ("Bardzo {x}.", "{ph} mâak khráp", "{th}มากครับ"),
    "num": ("Razem {x}.", "ruam {ph} khráp", "รวม{th}ครับ"),
    "noun": ("Czy jest {x}?", "mii {ph} mǎi khráp", "มี{th}ไหมครับ"),
    # wyrazy funkcyjne: żadna rama treściowa nie da sensownego zdania,
    # więc pokazujemy samo użycie słowa
    "func": ("Użyj słowa „{x}”.", "chái kham wâa {ph} khráp", "ใช้คำว่า{th}ครับ"),
}

# Rama zapasowa na wypadek, gdy pierwsza powtórzyłaby przykład już obecny
# w rekordzie. Bez niej sto jeden rekordów zostawało z jednym przykładem.
FRAMES_ALT = {
    "verb": ("Czy mogę {x}?", "{ph} dâai mǎi khráp", "{th}ได้ไหมครับ"),
    "adj": ("Trochę {x}.", "{ph} nít nòi khráp", "{th}นิดหน่อยครับ"),
    "num": ("Poproszę {x}.", "khǎw {ph} khráp", "ขอ{th}ครับ"),
    "noun": ("Gdzie jest {x}?", "{ph} yùu thîi nǎi khráp", "{th}อยู่ที่ไหนครับ"),
    "func": ("Powtórz słowo „{x}”.", "phûut kham wâa {ph} ìik khráng khráp",
             "พูดคำว่า{th}อีกครั้งครับ"),
}

FUNC_SUBCATS = {
    ("Gramatyka użytkowa", "Spójniki"),
    ("Gramatyka użytkowa", "Partykuły"),
    ("Gramatyka użytkowa", "Wskaźniki"),
    ("Pytania", "Słowa pytające"),
    ("Podstawy i grzeczność", "Zaimki"),
}


def classify(rec):
    """Rodzaj ramy zdaniowej. Kategoria jest pewniejsza niż rozbiór hasła:
    „długi” ma w słowniku także czytanie rzeczownikowe."""
    cat, sub = rec["category"], rec["subcategory"]
    if (cat, sub) in FUNC_SUBCATS:
        return "func"
    if cat == "Liczby i liczenie":
        return "num"
    pl = rec["polish"].rstrip(".!?").strip()
    if not pl:
        return None
    if cat == "Cechy i opinie":
        return "adj"
    if cat == "Czasowniki" or PG.is_infinitive(pl):
        return "verb"
    first = pl.split()[0]
    if PG._has_reading(first, ("adj",)) and not PG._has_reading(first, ("subst",)):
        return "adj"
    if PG.forms(pl) is not None:
        return "noun"
    return "func"


def add_example(rec):
    if rec["type"] != "word" or len(rec.get("examples", [])) >= 2:
        return False
    kind = classify(rec)
    if kind is None:
        stats["examples_skipped"] += 1
        return False
    pl_word = rec["polish"].rstrip(".!?").strip()
    if kind == "noun":
        pl_word = PG.inflect(pl_word, "nom")
    taken_ph = {e["thaiPhonetic"] for e in rec["examples"]}
    taken_pl = {e["polish"] for e in rec["examples"]}
    for frames in (FRAMES, FRAMES_ALT):
        tpl_pl, tpl_ph, tpl_th = frames[kind]
        text = tpl_pl.replace("{x}", pl_word)
        text = text[:1].upper() + text[1:]
        ph = tpl_ph.replace("{ph}", rec["thaiPhonetic"])
        th = tpl_th.replace("{th}", rec["ttsThai"])
        if ph in taken_ph or text in taken_pl:
            continue
        rec["examples"].append({
            "polish": text, "thaiPhonetic": ph, "ttsThai": th, "audioFile": "",
        })
        stats["examples_added"] += 1
        return True
    stats["examples_duplicate"] += 1
    return False


# ===========================================================================
# Przebieg
# ===========================================================================
def count_colons(objs):
    return sum(1 for o in objs if ":" in o.get("polish", ""))


def main():
    if not PG.morfeusz_available() and not PG._CACHE:
        print("Brak Morfeusza i pusty inflect-cache.json — nie da się odmienić haseł.",
              file=sys.stderr)
        return 1

    before = Counter()
    after = Counter()

    for fn in VOCAB:
        data = load(fn)
        recs = data["records"]
        before["records"] += len(recs)
        before["colon"] += count_colons(recs)
        before["colon_ex"] += sum(count_colons(r.get("examples", [])) for r in recs)
        before["multi_example_words"] += sum(
            1 for r in recs if r["type"] == "word" and len(r.get("examples", [])) >= 2)
        before["word"] += sum(1 for r in recs if r["type"] == "word")

        for rec in recs:
            fix_record_polish(rec)
            cls = fix_classifier(rec)
            if cls:
                stats["cls_" + cls] += 1
                stats["classifier_fixes"] += 1
            for ex in rec.get("examples", []):
                cls = fix_classifier(ex)
                if cls:
                    stats["cls_" + cls] += 1
                    stats["classifier_fixes"] += 1
            add_example(rec)

        after["records"] += len(recs)
        after["colon"] += count_colons(recs)
        after["colon_ex"] += sum(count_colons(r.get("examples", [])) for r in recs)
        after["multi_example_words"] += sum(
            1 for r in recs if r["type"] == "word" and len(r.get("examples", [])) >= 2)
        after["examples"] += sum(len(r.get("examples", [])) for r in recs)
        data["count"] = len(recs)
        save(fn, data)

    for fn in DIALOG:
        data = load(fn)
        for d in data["records"]:
            for line in d.get("lines", []):
                new, ok = FP.fix_text(line["polish"], line.get("thaiPhonetic", ""))
                if ok:
                    line["polish"] = new
                    stats["polish_dialogues"] += 1
                cls = fix_classifier(line)
                if cls:
                    stats["cls_" + cls] += 1
                    stats["classifier_fixes"] += 1
        data["count"] = len(data["records"])
        save(fn, data)

    build_classifiers_json()
    extend_grammar()
    update_support_files()
    update_metadata(after)
    PG.save_cache()

    print("=" * 58)
    print("ETAP 8 (SESJA G) — SESJA NAPRAWCZA")
    print("=" * 58)
    print("  rekordów przed / po           %5d / %d" % (before["records"], after["records"]))
    print("  rekordów z dwukropkiem        %5d / %d" % (before["colon"], after["colon"]))
    print("  przykładów z dwukropkiem      %5d / %d" % (before["colon_ex"], after["colon_ex"]))
    print("  word z 2+ przykładami         %5d / %d"
          % (before["multi_example_words"], after["multi_example_words"]))
    print("-" * 58)
    for k in sorted(stats):
        print("  %-28s %5d" % (k, stats[k]))
    print("-" * 58)
    print("WYNIK: GOTOWE")
    return 0


def update_support_files():
    """Dopisuje classifiers.json do manifestu i do listy plików aplikacji."""
    manifest = load("manifest.json")
    files = [f["file"] for f in manifest["supportFiles"]]
    entry = {"file": "classifiers.json", "kind": "classifiers",
             "count": stats["classifier_records"]}
    if "classifiers.json" in files:
        for f in manifest["supportFiles"]:
            if f["file"] == "classifiers.json":
                f["count"] = stats["classifier_records"]
    else:
        manifest["supportFiles"].append(entry)
    save("manifest.json", manifest)

    loader = os.path.join(ROOT, "js", "data-loader.js")
    src = open(loader, encoding="utf-8").read()
    if "classifiers.json" not in src:
        src = src.replace(
            "var SUPPORT = ['categories.json', 'grammar.json', 'pronunciation.json', 'metadata.json'];",
            "var SUPPORT = ['categories.json', 'grammar.json', 'pronunciation.json',\n"
            "                 'metadata.json', 'classifiers.json'];")
        src = src.replace(
            "      case 'pronunciation.json': DB.pronunciation = json; break;",
            "      case 'pronunciation.json': DB.pronunciation = json; break;\n"
            "      case 'classifiers.json': DB.classifiers = rows; break;")
        src = src.replace(
            "    pronunciation: null,",
            "    pronunciation: null,\n    classifiers: [],")
        open(loader, "w", encoding="utf-8").write(src)
        stats["loader_wired"] = 1


def update_metadata(after):
    meta = load("metadata.json")
    meta["conventions"]["colon"] = (
        "Zniesiona w sesji G. Wstawki słownikowe w mianowniku („Poproszę: woda”) "
        "zostały przepisane na poprawną polszczyznę z odmianą („Poproszę wodę”). "
        "Dwukropek zostaje wyłącznie tam, gdzie jest poprawny po polsku: "
        "wprowadza cytat albo wyliczenie."
    )
    meta["exampleSentences"] = after["examples"]
    meta["classifiers"] = {
        "file": "classifiers.json",
        "count": stats["classifier_records"],
        "wordOrder": "rzeczownik + liczba + klasyfikator",
        "note": "Pełny wykaz klasyfikatorów z listą rzeczowników i przykładami liczenia.",
    }
    meta["updated"] = "2026-08-18"
    save("metadata.json", meta)


if __name__ == "__main__":
    sys.exit(main())
