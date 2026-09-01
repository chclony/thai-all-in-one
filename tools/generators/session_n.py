# -*- coding: utf-8 -*-
"""Sesja N — generator nowych haseł leksykalnych i zdań aktywujących.

Uruchomienie (z katalogu tools/generators):
    python3 session_n.py

CO TEN SKRYPT ROBI I DLACZEGO TAK
---------------------------------
Baza miała 1 353 hasła leksykalne, z czego 887 dawało się wprowadzić do
ścieżki. Ograniczeniem nie była liczba zdań (6 202), tylko liczba cegiełek.
Ta sesja dokłada cegiełki — ale samo hasło do niczego nie służy.

Warunek dydaktyczny kursu brzmi: nowe hasło musi mieć zdanie, w którym
występuje, a którego WSZYSTKIE pozostałe sylaby uczący się już zna. Dlatego
dla każdego hasła generujemy co najmniej trzy zdania z szablonów zbudowanych
wyłącznie z materiału podstawowego. Zdania są osobnymi rekordami typu
`sentence` — tylko takie liczy generator ścieżki jako aktywujące. Pole
`examples` wewnątrz hasła tej roli nie pełni.

TRZY KONTROLE PRZED ZAPISEM
---------------------------
1. **Pokrycie sylabiczne.** Każda sylaba każdego zdania musi leżeć w zbiorze
   sylab bazy powiększonym o sylaby samego hasła. Zdanie, które tego nie
   spełnia, jest odrzucane; hasło z mniej niż trzema zdaniami nie wchodzi.
2. **Duplikaty.** Po zapisie fonetycznym bez tonów i po znaczeniu polskim,
   wobec całej istniejącej bazy i wewnątrz nowej partii.
3. **Polska odmiana.** Szablony wstawiają hasło w wymaganym przypadku przez
   `polish_grammar` — konwencja „Poproszę: woda” nie może wrócić tylnymi
   drzwiami. Hasła, których nie da się odmienić sensownie (partykuły,
   spójniki, wyrażenia z wielokropkiem), dostają szablony bezprzypadkowe.
"""

import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, HERE)

import engine as E
import polish_grammar as PG

from lex_n_nature import NATURE, CAT as NATURE_CAT
from lex_n_move import MOVE
from lex_n_people import PEOPLE
from lex_n_life import LIFE
from lex_n_work import WORK
from lex_n_lang import LANG
from lex_n_extra import EXTRA
from lex_n_society import SOCIETY
from lex_n_mind import MIND
from lex_n_act import ACT
from lex_n_balance import BALANCE
from lex_n_close import CLOSE

SOURCE = "Sesja N — rozszerzenie leksykalne (pokrycie mowy potocznej)"
LICENSE = "Do weryfikacji przed publiczną publikacją"

TYPE_MAP = {"n": "noun", "v": "verb", "adj": "adjective", "adv": "adverb", "w": "word"}

BASE_FILES = [
    "survival.json", "core-lexicon-01.json", "core-lexicon-02.json",
    "a1-part-01.json", "a1-part-02.json",
    "a2-part-01.json", "a2-part-02.json", "supplemental-practical.json",
    "b1-part-01.json", "b1-part-02.json", "b1-part-03.json",
    "b2-part-01.json", "b2-part-02.json",
]


# --------------------------------------------------------------------- pomoc
def strip_tone(s):
    d = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in d if not unicodedata.combining(c))


def norm_ph(s):
    """Klucz porównawczy fonetyki: Z TONAMI, bez dywizów i spacji.

    Tony muszą zostać. Pierwsza wersja tej funkcji je zdejmowała i odrzuciła
    kilkadziesiąt poprawnych haseł jako „duplikaty”: „thâm” (jaskinia, ถ้ำ)
    kolidowało z „tham” (robić, ทำ), „kàw” (wyspa) z „kâw” (no i), „sǎai”
    (piasek) z „sàai” (w lewo). To nie są duplikaty, tylko pary minimalne —
    czyli dokładnie ten materiał, na którym stoi Moduł 0. Zdejmowanie tonów
    przy deduplikacji kasowałoby najcenniejsze hasła w całej bazie.
    """
    return re.sub(r"[\s\-]+", "", (s or "").lower())


def norm_ph_loose(s):
    """Klucz bez tonów — wyłącznie do RAPORTOWANIA par homofonicznych."""
    return re.sub(r"[\s\-]+", "", strip_tone(s))


def norm_pl(s):
    """Klucz porównawczy znaczenia polskiego."""
    s = strip_tone(s)
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[^a-z0-9ąćęłńóśźż ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------- baza wyjściowa
base_records = []
for fn in BASE_FILES:
    base_records.extend(load(fn)["records"])

KNOWN_SYL = set()
for r in base_records:
    KNOWN_SYL |= set(r.get("syllables") or [])

base_ph = {norm_ph(r["thaiPhonetic"]) for r in base_records}
base_ph_loose = defaultdict(set)
for r in base_records:
    base_ph_loose[norm_ph_loose(r["thaiPhonetic"])].add(r["thaiPhonetic"])
homophones = []
# Znaczenia zajęte w bazie. Pierwsza wersja patrzyła wyłącznie na hasła
# leksykalne — i przepuściła 17 kolizji w rodzaju „jak długo?”, które w bazie
# istnieje jako pytanie (naan thâo-rài khráp), a nie jako hasło. Dwa różne
# zwroty tajskie pod jednym polskim tłumaczeniem to w słowniku szum: uczący
# się nie ma jak zgadnąć, który wybrać. Filtrujemy po CAŁEJ bazie.
base_pl = defaultdict(set)
for r in base_records:
    base_pl[norm_pl(r["polish"])].add(norm_ph(r["thaiPhonetic"]))
base_ids = {r["id"] for r in base_records}

# Zdania i znaczenia już obecne w bazie. Szablon, który trafi w istniejące
# zdanie, tworzy duplikat międzysesyjny — audyt wyłapał ich 61 w pierwszym
# przebiegu („mii hâwng wâang mǎi khráp” istniało już w materiale hotelowym).
# Szablonów jest po 5-10 na typ, a potrzebne są 3, więc kolizję po prostu
# pomijamy i bierzemy następny szablon.
base_sent_ph = {norm_ph(r["thaiPhonetic"]) for r in base_records}
base_sent_pl = {norm_pl(r["polish"]) for r in base_records}
used_sent_ph, used_sent_pl = set(), set()
skipped_collisions = []


# ------------------------------------------------------------------- szablony
# Każdy szablon: (polski, fonetyka, pismo, przypadek).
# {P} = hasło po polsku w danym przypadku, {F} = fonetyka, {T} = pismo tajskie.
# Przypadek None znaczy „wstaw formę słownikową” — dla partykuł i spójników.

T_NOUN = [
    ("Mam {P}.",                 "phǒm mii {F} khráp",            "ผมมี{T}ครับ",            "acc"),
    ("Czy jest {P}?",            "mii {F} mǎi khráp",             "มี{T}ไหมครับ",           "nom"),
    ("Nie mam {P}.",             "phǒm mâi mii {F} khráp",        "ผมไม่มี{T}ครับ",         "gen"),
    ("Poproszę {P}.",            "khǎw {F} khráp",                "ขอ{T}ครับ",              "acc"),
    ("Lubię {P}.",               "phǒm châwp {F} khráp",          "ผมชอบ{T}ครับ",           "acc"),
    ("Gdzie jest {P}?",          "{F} yùu thîi nǎi khráp",        "{T}อยู่ที่ไหนครับ",       "nom"),
    ("Chcę {P}.",                "phǒm yàak dâi {F} khráp",       "ผมอยากได้{T}ครับ",       "acc"),
    ("{P} jest bardzo dobry.",   "{F} dii mâak khráp",            "{T}ดีมากครับ",           "nom"),
    ("Szukam {P}.",              "phǒm hǎa {F} yùu khráp",        "ผมหา{T}อยู่ครับ",        "gen"),
    ("Widzę {P}.",               "phǒm hěn {F} khráp",            "ผมเห็น{T}ครับ",          "acc"),
]

T_VERB = [
    ("Chcę {P}.",                "phǒm yàak {F} khráp",           "ผมอยาก{T}ครับ",          None),
    ("Nie {P1}.",                "phǒm mâi {F} khráp",            "ผมไม่{T}ครับ",           None),
    ("Czy mogę {P}?",            "{F} dâi mǎi khráp",             "{T}ได้ไหมครับ",          None),
    ("Muszę {P}.",               "phǒm tâwng {F} khráp",          "ผมต้อง{T}ครับ",          None),
    ("Lubię {P}.",               "phǒm châwp {F} khráp",          "ผมชอบ{T}ครับ",           None),
    ("Właśnie {P1}.",            "phǒm kamlang {F} yùu khráp",    "ผมกำลัง{T}อยู่ครับ",     None),
    ("Już {P1}.",                "phǒm {F} láew khráp",           "ผม{T}แล้วครับ",          None),
    ("Pomogę {P}.",              "phǒm chûai {F} khráp",          "ผมช่วย{T}ครับ",          None),
]

T_ADJ = [
    ("To jest bardzo {P}.",      "an níi {F} mâak khráp",         "อันนี้{T}มากครับ",       None),
    ("To nie jest {P}.",         "an níi mâi {F} khráp",          "อันนี้ไม่{T}ครับ",       None),
    ("Czy to jest {P}?",         "an níi {F} mǎi khráp",          "อันนี้{T}ไหมครับ",       None),
    ("Dziś jest bardzo {P}.",    "wan níi {F} mâak khráp",        "วันนี้{T}มากครับ",       None),
    ("To jest za bardzo {P}.",   "an níi {F} kooen pai khráp",    "อันนี้{T}เกินไปครับ",    None),
    ("Tamto jest bardziej {P}.", "an nán {F} kwàa khráp",         "อันนั้น{T}กว่าครับ",     None),
]

T_ADV = [
    ("Robię to {P}.",            "phǒm tham {F} khráp",           "ผมทำ{T}ครับ",            None),
    ("Idę {P}.",                 "phǒm pai {F} khráp",            "ผมไป{T}ครับ",            None),
    ("Czy {P}?",                 "{F} mǎi khráp",                 "{T}ไหมครับ",             None),
    ("Nie {P}.",                 "mâi {F} khráp",                 "ไม่{T}ครับ",             None),
    ("Jest {P}.",                "pen {F} khráp",                 "เป็น{T}ครับ",            None),
]

T_WORD = [
    ("Rozumiem — {P}.",          "khâo jai láew {F} khráp",       "เข้าใจแล้ว{T}ครับ",      None),
    ("Tak, {P}.",                "châi {F} khráp",                "ใช่{T}ครับ",             None),
    ("Nie, {P}.",                "mâi châi {F} khráp",            "ไม่ใช่{T}ครับ",          None),
    ("{P} — mówię to.",          "phǒm phûut wâa {F} khráp",      "ผมพูดว่า{T}ครับ",        None),
    ("Powiedz {P}.",             "phûut {F} sì khráp",            "พูด{T}สิครับ",           None),
]

TEMPLATES = {
    "noun": T_NOUN, "verb": T_VERB, "adjective": T_ADJ,
    "adverb": T_ADV, "word": T_WORD,
}

# Hasła, których nie da się wstawić do szablonu przypadkowego: wielokropek
# w środku, spójniki, partykuły zdaniowe. Dostają szablony słowa.
UNINFLECTABLE = re.compile(r"…|\.\.\.")


def polish_slot(label, case):
    """Hasło po polsku w wymaganym przypadku, bez glos w nawiasach."""
    core = re.sub(r"\s*\(.*?\)\s*", " ", label).strip()
    core = core.split(" / ")[0].split(",")[0].strip()
    if not core:
        return None
    if case is None:
        return core
    try:
        out = PG.inflect(core, case)
    except Exception:
        return None
    return out or core


def polish_verb_1sg(label):
    """Forma pierwszej osoby dla szablonów typu „Właśnie jem”."""
    core = re.sub(r"\s*\(.*?\)\s*", " ", label).strip()
    core = core.split(" / ")[0].split(",")[0].strip()
    try:
        if PG.is_infinitive(core):
            return PG.past_1sg(core)
    except Exception:
        pass
    return None


def syllables_of(ph):
    out = []
    for w in ph.split():
        c = w.strip(".,!?;:")
        if c:
            out += c.split("-")
    return out


# ------------------------------------------------------------------- budowa
rejected = []            # (hasło, powód)
dup_ph, dup_pl = [], []
seen_ph, seen_pl = set(), set()

lexemes, sentences = [], []
counters = Counter()


def new_id(level, cat, kind):
    pref = {"Survival": "srv"}.get(level, level.lower())
    key = "n%s-%s-%s" % (kind, pref, E.slug(cat))
    counters[key] += 1
    return "%s-%04d" % (key, counters[key])


def build_sentences(label, ph, th, rtype, level, cat, sub, lex_syl):
    """Zdania aktywujące. Zwraca listę rekordów albo pustą listę."""
    out = []
    allowed = KNOWN_SYL | set(lex_syl)
    for pl_pat, ph_pat, th_pat, case in TEMPLATES[rtype]:
        if "{P1}" in pl_pat:
            slot = polish_verb_1sg(label)
        else:
            slot = polish_slot(label, case)
        if not slot:
            continue
        polish = pl_pat.replace("{P1}", slot).replace("{P}", slot)
        # zdanie nie może zaczynać się od małej litery po podmianie
        polish = polish[0].upper() + polish[1:] if polish else polish
        s_ph = ph_pat.replace("{F}", ph)
        s_th = th_pat.replace("{T}", th)
        syl = syllables_of(s_ph)
        bad = [s for s in syl if s not in allowed]
        if bad:
            continue
        kph, kpl = norm_ph(s_ph), norm_pl(polish)
        if kph in base_sent_ph or kph in used_sent_ph:
            skipped_collisions.append((polish, s_ph, "fonetyka już w bazie"))
            continue
        if kpl in base_sent_pl or kpl in used_sent_pl:
            skipped_collisions.append((polish, s_ph, "polskie zdanie już w bazie"))
            continue
        used_sent_ph.add(kph)
        used_sent_pl.add(kpl)
        out.append((polish, s_ph, s_th, syl))
        if len(out) >= 4:
            break
    return out


def make_records(entry, cat_default=None):
    """Jedna krotka wejściowa -> hasło + zdania, albo None z powodem."""
    if cat_default is not None:
        level, label, ph, th, sub, freq, kind, notes, literal = entry
        cat = cat_default
    else:
        level, label, ph, th, sub, freq, kind, cat, notes, literal = entry

    rtype = TYPE_MAP[kind]
    if UNINFLECTABLE.search(label) or UNINFLECTABLE.search(ph):
        rtype = "word"

    kph, kpl = norm_ph(ph), norm_pl(label)

    if kph in base_ph:
        dup_ph.append((label, ph, "istnieje w bazie"))
        return None
    if kph in seen_ph:
        dup_ph.append((label, ph, "powtórka w tej sesji"))
        return None
    if kpl in base_pl:
        dup_pl.append((label, ph, "znaczenie już w bazie"))
        return None
    if kpl in seen_pl:
        dup_pl.append((label, ph, "znaczenie powtórzone w tej sesji"))
        return None

    # Para minimalna z istniejącym hasłem to nie błąd, tylko materiał —
    # notujemy ją, żeby dało się ją potem wykorzystać w ćwiczeniach tonalnych.
    twins = base_ph_loose.get(norm_ph_loose(ph), set()) - {ph}
    if twins:
        homophones.append((label, ph, sorted(twins)))

    lex_syl = E.syllables(ph)
    sents = build_sentences(label, ph, th, rtype, level, cat, sub, lex_syl)
    if len(sents) < 3:
        rejected.append((label, ph, "zdań aktywujących: %d (wymagane 3)" % len(sents)))
        return None

    seen_ph.add(kph)
    seen_pl.add(kpl)

    rid = new_id(level, cat, "lex")
    lex = {
        "id": rid,
        "type": rtype,
        "polish": label,
        "polishAlternatives": [],
        "thaiPhonetic": ph,
        "pronunciationPolish": E.polish_read(ph),
        "ttsThai": th,
        "syllables": lex_syl,
        "toneGuide": E.tone_guide(ph),
        "category": cat,
        "subcategory": sub,
        "level": level,
        "difficulty": E.difficulty(ph),
        "frequency": freq,
        "register": "neutralny",
        "tags": ["sesja-n", E.slug(cat), level.lower(), "leksyka"],
        "literalMeaning": literal,
        "notes": notes,
        "commonMistakes": E.common_mistakes(ph),
        "examples": [{"polish": s[0], "thaiPhonetic": s[1], "ttsThai": s[2],
                      "audioFile": ""} for s in sents[:3]],
        "relatedWords": [],
        "audioFile": "",
        "source": SOURCE,
        "license": LICENSE,
    }

    out_sents = []
    for i, (spl, sph, sth, syl) in enumerate(sents, 1):
        out_sents.append({
            "id": new_id(level, cat, "act"),
            "type": "sentence",
            "polish": spl,
            "polishAlternatives": [],
            "thaiPhonetic": sph,
            "pronunciationPolish": E.polish_read(sph),
            "ttsThai": sth,
            "syllables": syl,
            "toneGuide": E.tone_guide(sph),
            "category": cat,
            "subcategory": sub,
            "level": level,
            "difficulty": E.difficulty(sph),
            "frequency": max(2, freq - 1),
            "register": "neutralny",
            "tags": ["sesja-n", "zdanie-aktywujące", E.slug(cat), level.lower()],
            "literalMeaning": "",
            "notes": "Zdanie aktywujące hasło „%s” — zbudowane wyłącznie "
                     "z materiału wcześniejszego." % label,
            "commonMistakes": E.common_mistakes(sph),
            "examples": [{"polish": spl, "thaiPhonetic": sph, "ttsThai": sth,
                          "audioFile": ""}],
            "relatedWords": [rid],
            "audioFile": "",
            "source": SOURCE,
            "license": LICENSE,
        })
    lex["relatedWords"] = [s["id"] for s in out_sents]
    return lex, out_sents


def main():
    batches = [(NATURE, NATURE_CAT), (MOVE, None), (PEOPLE, None),
               (LIFE, None), (WORK, None), (LANG, None), (EXTRA, None),
               (SOCIETY, None), (MIND, None), (ACT, None), (BALANCE, None), (CLOSE, None)]

    total_in = 0
    for data, cat_default in batches:
        for entry in data:
            total_in += 1
            got = make_records(entry, cat_default)
            if got:
                lexemes.append(got[0])
                sentences.extend(got[1])

    # ---- rozdział na pliki: równomiernie, ale hasło razem ze swoimi zdaniami
    groups = []
    by_lex = defaultdict(list)
    for s in sentences:
        by_lex[s["relatedWords"][0]].append(s)
    for lex in lexemes:
        groups.append([lex] + by_lex[lex["id"]])

    n_files = 4
    files = [[] for _ in range(n_files)]
    for i, g in enumerate(groups):
        files[i % n_files].extend(g)

    written = []
    for i, recs in enumerate(files, 1):
        fn = "lexicon-%02d.json" % i
        with open(os.path.join(DATA, fn), "w", encoding="utf-8") as f:
            json.dump({"file": fn, "count": len(recs), "records": recs},
                      f, ensure_ascii=False, indent=1)
        written.append((fn, len(recs)))

    # ------------------------------------------------------------- raport
    print("=" * 74)
    print("  SESJA N — GENERATOR LEKSYKI")
    print("=" * 74)
    print("kandydatów na wejściu           %5d" % total_in)
    print("odrzuconych — duplikat fonetyki %5d" % len(dup_ph))
    print("odrzuconych — duplikat znaczenia%5d" % len(dup_pl))
    print("odrzuconych — za mało zdań      %5d" % len(rejected))
    print("szablonów pominiętych (kolizja) %5d" % len(skipped_collisions))
    print("-" * 74)
    print("NOWYCH HASEŁ LEKSYKALNYCH       %5d" % len(lexemes))
    print("NOWYCH ZDAŃ AKTYWUJĄCYCH        %5d" % len(sentences))
    print("     zdań na hasło (średnio)     %5.2f"
          % (len(sentences) / max(1, len(lexemes))))

    print("\nPLIKI")
    for fn, n in written:
        print("  %-20s %5d rekordów" % (fn, n))

    print("\nNOWE HASŁA — POZIOMY")
    for k, v in Counter(r["level"] for r in lexemes).most_common():
        print("  %-12s %5d" % (k, v))

    print("\nNOWE HASŁA — TYPY")
    for k, v in Counter(r["type"] for r in lexemes).most_common():
        print("  %-12s %5d" % (k, v))

    print("\nNOWE HASŁA — KATEGORIE")
    for k, v in sorted(Counter(r["category"] for r in lexemes).items(),
                       key=lambda kv: -kv[1]):
        print("  %-26s %5d" % (k, v))

    if rejected:
        print("\nHASŁA ODRZUCONE Z BRAKU ZDAŃ AKTYWUJĄCYCH")
        for label, ph, why in rejected[:40]:
            print("  %-34s %-22s %s" % (label[:34], ph[:22], why))
        if len(rejected) > 40:
            print("  … oraz %d dalszych" % (len(rejected) - 40))

    if homophones:
        print("\nPARY MINIMALNE Z ISTNIEJĄCĄ BAZĄ — %d (materiał, nie błąd)"
              % len(homophones))
        for label, ph, twins in homophones[:20]:
            print("  %-28s %-16s kontra %s" % (label[:28], ph, ", ".join(twins)))
        if len(homophones) > 20:
            print("  … oraz %d dalszych" % (len(homophones) - 20))

    if dup_ph or dup_pl:
        print("\nDUPLIKATY (pierwsze 25 z każdego rodzaju)")
        for label, ph, why in dup_ph[:25]:
            print("  fonetyka  %-30s %-20s %s" % (label[:30], ph[:20], why))
        for label, ph, why in dup_pl[:25]:
            print("  znaczenie %-30s %-20s %s" % (label[:30], ph[:20], why))

    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
