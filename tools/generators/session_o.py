# -*- coding: utf-8 -*-
"""Sesja O — domknięcie leksykonu i zdania aktywujące o dużej gęstości.

Uruchomienie (z katalogu tools/generators):
    python3 session_o.py

CO ZMIENIA SIĘ WOBEC SESJI N
----------------------------
Sesja N dołożyła 906 haseł, każde z trzema–czterema zdaniami aktywującymi
zbudowanymi z materiału wcześniejszego. Zdania te miały jedną wspólną cechę:
każde wprowadzało **dokładnie jedno** nowe hasło. To wystarczało, dopóki
lekcja wprowadzała 2–6 haseł — sześć nowych słów i sześć zdań mieści się
w limicie 8–15 rekordów na lekcję.

Ta sesja ma dowieźć ścieżkę wprowadzającą 3 000 słów. Przy 320 lekcjach to
9,4 hasła na lekcję. Rachunek jest bezlitosny:

    15 rekordów na lekcję  =  10 nowych haseł  +  5 zdań

czyli **jedno zdanie musi aktywować średnio dwa nowe hasła**. Zdania „jeden
do jednego" tego nie umieją: dziesięć haseł potrzebowałoby dziesięciu zdań,
razem dwadzieścia rekordów, a limit lekcji wynosi piętnaście.

Dlatego generator produkuje trzy warstwy zdań:

    warstwa 1 — solo    : jedno hasło w zdaniu (jak w sesji N),
    warstwa 2 — para    : dwa nowe hasła w jednym zdaniu,
    warstwa 3 — trójka  : trzy nowe hasła w jednym zdaniu.

Warstwa 1 jest potrzebna, bo drugie hasło pary bywa już znane z wcześniejszej
lekcji — wtedy zdanie parowe działa jak solowe. Warstwy 2 i 3 są tym, co
w ogóle umożliwia gęstą lekcję.

KOMÓRKI
-------
Zdanie parowe ma sens tylko dla haseł, które trafią do TEJ SAMEJ lekcji.
Generator ścieżki wybiera hasła po kolei: poziom, częstość, trudność. Hasła
z jednej kategorii i jednego poziomu leżą więc w kolejce obok siebie.
Wykorzystujemy to: hasła grupujemy w **komórki po cztery** (kategoria +
poziom + sąsiedztwo w module) i dla każdej komórki generujemy komplet
sześciu zdań parowych i dwóch trójkowych. Lekcja bierze dwie–trzy komórki
i ma z czego złożyć aktywacje.

DOBÓR MATERIAŁU — SKŁADANIE Z ZNANYCH SYLAB
-------------------------------------------
Sesja N zostawiła diagnozę: ścieżka nasyca się nie na braku haseł, tylko na
kolejności, w jakiej sylaby wchodzą do obiegu. Hasło z dwiema nieznanymi
sylabami czeka, aż obie wejdą skądinąd.

Odpowiedzią jest warstwa złożeniowa. Tajski buduje ogromną część słownika
kompozycyjnie: `kaan-` + czasownik daje rzeczownik odczasownikowy,
`khwaam-` + przymiotnik rzeczownik abstrakcyjny, `nák-`/`phûu-`/`châang-`
nazwy wykonawców, `khrûeang-` urządzenia, `ráan-` sklepy, `rót-` pojazdy,
`nám-` płyny, `hâwng-` pomieszczenia. To są prawdziwe, częste wyrazy — a nie
sztuczne sklejki — i mają tę własność, że **nie wnoszą ani jednej nowej
sylaby**. Hasło złożone z sylab już znanych da się wprowadzić natychmiast,
a nie za sto lekcji. Stąd przewaga takich haseł w modułach tej sesji.

TRZY KONTROLE PRZED ZAPISEM (jak w sesji N, bez zmian)
------------------------------------------------------
1. Pokrycie sylabiczne każdego zdania: sylaby bazy + sylaby wprowadzanych
   haseł, nic poza tym.
2. Duplikaty: fonetyka Z TONAMI (pary minimalne to materiał, nie duplikaty)
   i znaczenie polskie, wobec całej bazy i wewnątrz partii.
3. Polska odmiana przez `polish_grammar` — bez konwencji „Poproszę: woda”.

Dodatkowo szablony są **automatycznie filtrowane**: szablon, którego własne
sylaby nie leżą w zasobie bazy, wypada z zestawu przed użyciem. Dzięki temu
literówka w szablonie nie przecieka do danych jako zdanie nie do wymówienia.
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

import engine as E          # noqa: E402
import polish_grammar as PG  # noqa: E402

SOURCE = "Sesja O — domknięcie leksykonu (ścieżka 3 000 słów)"
LICENSE = "Do weryfikacji przed publiczną publikacją"

TYPE_MAP = {"n": "noun", "v": "verb", "adj": "adjective", "adv": "adverb", "w": "word"}

BASE_FILES = [
    "survival.json", "core-lexicon-01.json", "core-lexicon-02.json",
    "a1-part-01.json", "a1-part-02.json",
    "a2-part-01.json", "a2-part-02.json", "supplemental-practical.json",
    "b1-part-01.json", "b1-part-02.json", "b1-part-03.json",
    "b2-part-01.json", "b2-part-02.json",
    "lexicon-01.json", "lexicon-02.json", "lexicon-03.json", "lexicon-04.json",
]

OUT_FILES = 8               # lexicon-05.json … lexicon-12.json
CELL = 4                    # ile haseł w komórce parowanej


# --------------------------------------------------------------------- pomoc
def strip_tone(s):
    d = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in d if not unicodedata.combining(c))


def norm_ph(s):
    """Klucz fonetyczny Z TONAMI. Uzasadnienie w session_n.py: zdejmowanie
       tonów kasuje pary minimalne, czyli najcenniejszy materiał bazy."""
    return re.sub(r"[\s\-]+", "", (s or "").lower())


def norm_ph_loose(s):
    return re.sub(r"[\s\-]+", "", strip_tone(s))


def norm_pl(s):
    s = strip_tone(s)
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[^a-z0-9ąćęłńóśźż ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as f:
        return json.load(f)


def syllables_of(ph):
    out = []
    for w in ph.split():
        c = w.strip(".,!?;:")
        if c:
            out += c.split("-")
    return out


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

base_pl = defaultdict(set)
for r in base_records:
    base_pl[norm_pl(r["polish"])].add(norm_ph(r["thaiPhonetic"]))

base_sent_ph = {norm_ph(r["thaiPhonetic"]) for r in base_records}
base_sent_pl = {norm_pl(r["polish"]) for r in base_records}
used_sent_ph, used_sent_pl = set(), set()

homophones = []
skipped_collisions = 0


# ------------------------------------------------------------------- szablony
# Szablon solowy: (polski, fonetyka, pismo, przypadek).
T_NOUN = [
    ("Widzę tu {P}.",             "phǒm hěn {F} thîi nîi khráp",   "ผมเห็น{T}ที่นี่ครับ",     "acc"),
    ("Czy macie {P}?",            "mii {F} mǎi khráp",             "มี{T}ไหมครับ",           "acc"),
    ("Nie znam {P}.",             "phǒm mâi rúu-jàk {F} khráp",    "ผมไม่รู้จัก{T}ครับ",      "gen"),
    ("Potrzebuję {P}.",           "phǒm tâwng-kaan {F} khráp",     "ผมต้องการ{T}ครับ",       "gen"),
    ("{P} jest tutaj.",           "{F} yùu thîi nîi khráp",        "{T}อยู่ที่นี่ครับ",       "nom"),
    ("Pytam o {P}.",              "phǒm thǎam rûeang {F} khráp",   "ผมถามเรื่อง{T}ครับ",     "acc"),
    ("To jest {P}.",              "nîi khue {F} khráp",            "นี่คือ{T}ครับ",          "nom"),
    ("Interesuje mnie {P}.",      "phǒm sǒn-jai {F} khráp",        "ผมสนใจ{T}ครับ",          "nom"),
]

T_VERB = [
    ("Umiem {P}.",                "phǒm {F} pen khráp",            "ผม{T}เป็นครับ",          None),
    ("Nie chcę {P}.",             "phǒm mâi yàak {F} khráp",       "ผมไม่อยาก{T}ครับ",       None),
    ("Czy wolno {P}?",            "{F} dâi mǎi khráp",             "{T}ได้ไหมครับ",          None),
    ("Uczę się {P}.",             "phǒm rian {F} khráp",           "ผมเรียน{T}ครับ",         None),
    ("Zaczynam {P}.",             "phǒm rôoem {F} khráp",          "ผมเริ่ม{T}ครับ",         None),
    ("Trzeba {P} powoli.",        "tâwng {F} cháa cháa khráp",     "ต้อง{T}ช้าๆครับ",        None),
]

T_ADJ = [
    ("Dzisiaj jest {P}.",         "wan níi {F} khráp",             "วันนี้{T}ครับ",          None),
    ("To wcale nie jest {P}.",    "an níi mâi {F} looei khráp",    "อันนี้ไม่{T}เลยครับ",    None),
    ("Czy tam jest {P}?",         "thîi nân {F} mǎi khráp",        "ที่นั่น{T}ไหมครับ",      None),
    ("Robi się {P}.",             "chák chák kâw {F} khráp",       "ชักๆก็{T}ครับ",          None),
    ("Zbyt {P} dla mnie.",        "{F} kooen pai sǎm-ràp phǒm khráp", "{T}เกินไปสำหรับผมครับ", None),
]

T_ADV = [
    ("Proszę mówić {P}.",         "chûai phûut {F} nàwi khráp",    "ช่วยพูด{T}หน่อยครับ",    None),
    ("Idę tam {P}.",              "phǒm pai thîi nân {F} khráp",   "ผมไปที่นั่น{T}ครับ",     None),
    ("Robię to {P}.",             "phǒm tham {F} khráp",           "ผมทำ{T}ครับ",            None),
    ("Czy da się {P}?",           "{F} dâi mǎi khráp",             "{T}ได้ไหมครับ",          None),
]

T_WORD = [
    ("Zawsze mówię {P}.",         "phǒm phûut wâa {F} khráp",      "ผมพูดว่า{T}ครับ",        None),
    ("Rozumiem — {P}.",           "khâo jai láew {F} khráp",       "เข้าใจแล้ว{T}ครับ",      None),
    ("A więc {P}.",               "kâw {F} khráp",                 "ก็{T}ครับ",              None),
    ("Proszę powiedzieć {P}.",    "chûai phûut {F} nàwi khráp",    "ช่วยพูด{T}หน่อยครับ",    None),
]

SOLO = {"noun": T_NOUN, "verb": T_VERB, "adjective": T_ADJ,
        "adverb": T_ADV, "word": T_WORD}

# Szablon parowy: (polski, fonetyka, pismo, przypadek1, przypadek2).
# {P1}/{F1}/{T1} — hasło pierwsze, {P2}/{F2}/{T2} — drugie.
PAIR = {
    ("noun", "noun"): [
        ("Mam {P1} i {P2}.",              "phǒm mii {F1} kàp {F2} khráp",      "ผมมี{T1}กับ{T2}ครับ",      "acc", "acc"),
        ("Czy jest {P1} albo {P2}?",      "mii {F1} rǔe {F2} mǎi khráp",       "มี{T1}หรือ{T2}ไหมครับ",    "nom", "nom"),
        ("Szukam {P1} i {P2}.",           "phǒm hǎa {F1} kàp {F2} khráp",      "ผมหา{T1}กับ{T2}ครับ",      "gen", "gen"),
    ],
    ("noun", "adjective"): [
        ("{P1} jest bardzo {P2}.",        "{F1} {F2} mâak khráp",              "{T1}{T2}มากครับ",          "nom", None),
        ("Czy {P1} jest {P2}?",           "{F1} {F2} mǎi khráp",               "{T1}{T2}ไหมครับ",          "nom", None),
    ],
    ("noun", "verb"): [
        ("Chcę {P2} {P1}.",               "phǒm yàak {F2} {F1} khráp",         "ผมอยาก{T2}{T1}ครับ",       "acc", None),
        ("Nie mogę {P2} {P1}.",           "phǒm {F2} {F1} mâi dâi khráp",      "ผม{T2}{T1}ไม่ได้ครับ",     "gen", None),
    ],
    ("noun", "adverb"): [
        ("Widzę {P1} {P2}.",              "phǒm hěn {F1} {F2} khráp",          "ผมเห็น{T1}{T2}ครับ",       "acc", None),
    ],
    ("noun", "word"): [
        ("Tak, {P2} — mam {P1}.",         "châi {F2} phǒm mii {F1} khráp",     "ใช่{T2}ผมมี{T1}ครับ",      "acc", None),
    ],
    ("verb", "verb"): [
        ("Lubię {P1} i {P2}.",            "phǒm châwp {F1} láe {F2} khráp",    "ผมชอบ{T1}และ{T2}ครับ",     None, None),
        ("Muszę {P1}, potem {P2}.",       "phǒm tâwng {F1} láew {F2} khráp",   "ผมต้อง{T1}แล้ว{T2}ครับ",   None, None),
    ],
    ("verb", "adjective"): [
        ("Lubię {P1} — to jest {P2}.",    "phǒm châwp {F1} man {F2} khráp",    "ผมชอบ{T1}มัน{T2}ครับ",     None, None),
        ("Nie chcę {P1}, bo {P2}.",       "phǒm mâi yàak {F1} phráw {F2} khráp", "ผมไม่อยาก{T1}เพราะ{T2}ครับ", None, None),
    ],
    ("verb", "adverb"): [
        ("Proszę {P1} {P2}.",             "chûai {F1} {F2} nàwi khráp",        "ช่วย{T1}{T2}หน่อยครับ",    None, None),
    ],
    ("verb", "word"): [
        ("{P2} — chcę {P1}.",             "{F2} phǒm yàak {F1} khráp",         "{T2}ผมอยาก{T1}ครับ",       None, None),
    ],
    ("adjective", "adjective"): [
        ("To jest {P1}, ale nie {P2}.",   "an níi {F1} tàe mâi {F2} khráp",    "อันนี้{T1}แต่ไม่{T2}ครับ", None, None),
        ("Czy to {P1} czy {P2}?",         "an níi {F1} rǔe {F2} khráp",        "อันนี้{T1}หรือ{T2}ครับ",   None, None),
    ],
    ("adjective", "adverb"): [
        ("To jest {P2} {P1}.",            "an níi {F2} {F1} khráp",            "อันนี้{T2}{T1}ครับ",       None, None),
    ],
    ("adjective", "word"): [
        ("{P2} — to jest {P1}.",          "{F2} an níi {F1} khráp",            "{T2}อันนี้{T1}ครับ",       None, None),
    ],
    ("adverb", "adverb"): [
        ("Mówię {P1} i {P2}.",            "phǒm phûut {F1} láe {F2} khráp",    "ผมพูด{T1}และ{T2}ครับ",     None, None),
    ],
    ("adverb", "word"): [
        ("{P2} — mówię {P1}.",            "{F2} phǒm phûut {F1} khráp",        "{T2}ผมพูด{T1}ครับ",        None, None),
    ],
    ("word", "word"): [
        ("Mówię {P1} i {P2}.",            "phǒm phûut wâa {F1} {F2} khráp",    "ผมพูดว่า{T1}{T2}ครับ",     None, None),
    ],
}

# Szablon trójkowy: klucz to posortowana krotka typów. Sloty numerowane
# w obrębie typu: {Pn1} {Pn2} {Pn3}, {Pv1} {Pv2}, {Pa1} {Pa2}, {Pd1} (adverb),
# {Pw1} (word). Czwarty element krotki to przypadki polskie kolejnych slotów
# rzeczownikowych — reszta typów przypadku nie odmienia.
TRIPLE = {
    ("adjective", "noun", "verb"): [
        ("Chcę {Pv1} {Pn1}, bo jest {Pa1}.", "phǒm yàak {Fv1} {Fn1} phráw man {Fa1} khráp",
         "ผมอยาก{Tv1}{Tn1}เพราะมัน{Ta1}ครับ", {"n1": "acc"}),
    ],
    ("adjective", "noun", "noun"): [
        ("{Pn1} i {Pn2} są {Pa1}.", "{Fn1} kàp {Fn2} {Fa1} khráp",
         "{Tn1}กับ{Tn2}{Ta1}ครับ", {"n1": "nom", "n2": "nom"}),
    ],
    ("noun", "noun", "noun"): [
        ("Mam {Pn1}, {Pn2} i {Pn3}.", "phǒm mii {Fn1} {Fn2} kàp {Fn3} khráp",
         "ผมมี{Tn1}{Tn2}กับ{Tn3}ครับ", {"n1": "acc", "n2": "acc", "n3": "acc"}),
    ],
    ("noun", "noun", "verb"): [
        ("Chcę {Pv1} {Pn1} i {Pn2}.", "phǒm yàak {Fv1} {Fn1} kàp {Fn2} khráp",
         "ผมอยาก{Tv1}{Tn1}กับ{Tn2}ครับ", {"n1": "acc", "n2": "acc"}),
    ],
    ("adjective", "adjective", "noun"): [
        ("{Pn1} jest {Pa1} i {Pa2}.", "{Fn1} {Fa1} láe {Fa2} khráp",
         "{Tn1}{Ta1}และ{Ta2}ครับ", {"n1": "nom"}),
    ],
    ("adjective", "adjective", "adjective"): [
        ("To jest {Pa1}, {Pa2} i {Pa3}.", "an níi {Fa1} {Fa2} láe {Fa3} khráp",
         "อันนี้{Ta1}{Ta2}และ{Ta3}ครับ", {}),
    ],
    ("verb", "verb", "verb"): [
        ("Lubię {Pv1}, {Pv2} i {Pv3}.", "phǒm châwp {Fv1} {Fv2} láe {Fv3} khráp",
         "ผมชอบ{Tv1}{Tv2}และ{Tv3}ครับ", {}),
    ],
    ("adjective", "verb", "verb"): [
        ("Chcę {Pv1} i {Pv2} — to jest {Pa1}.", "phǒm yàak {Fv1} láe {Fv2} man {Fa1} khráp",
         "ผมอยาก{Tv1}และ{Tv2}มัน{Ta1}ครับ", {}),
    ],
    ("adverb", "verb", "verb"): [
        ("Proszę {Pv1} i {Pv2} {Pd1}.", "chûai {Fv1} láe {Fv2} {Fd1} nàwi khráp",
         "ช่วย{Tv1}และ{Tv2}{Td1}หน่อยครับ", {}),
    ],
    ("adverb", "noun", "verb"): [
        ("Chcę {Pv1} {Pn1} {Pd1}.", "phǒm yàak {Fv1} {Fn1} {Fd1} khráp",
         "ผมอยาก{Tv1}{Tn1}{Td1}ครับ", {"n1": "acc"}),
    ],
    ("adverb", "adjective", "noun"): [
        ("{Pn1} jest {Pd1} {Pa1}.", "{Fn1} {Fd1} {Fa1} khráp",
         "{Tn1}{Td1}{Ta1}ครับ", {"n1": "nom"}),
    ],
    ("noun", "verb", "verb"): [
        ("Chcę {Pv1} i {Pv2} {Pn1}.", "phǒm yàak {Fv1} láe {Fv2} {Fn1} khráp",
         "ผมอยาก{Tv1}และ{Tv2}{Tn1}ครับ", {"n1": "acc"}),
    ],
    ("noun", "noun", "word"): [
        ("Tak, {Pw1} — mam {Pn1} i {Pn2}.", "châi {Fw1} phǒm mii {Fn1} kàp {Fn2} khráp",
         "ใช่{Tw1}ผมมี{Tn1}กับ{Tn2}ครับ", {"n1": "acc", "n2": "acc"}),
    ],
    ("adjective", "noun", "word"): [
        ("{Pw1} — {Pn1} jest {Pa1}.", "{Fw1} {Fn1} {Fa1} khráp",
         "{Tw1}{Tn1}{Ta1}ครับ", {"n1": "nom"}),
    ],
    ("word", "word", "word"): [
        ("Mówię {Pw1}, {Pw2} i {Pw3}.", "phǒm phûut wâa {Fw1} {Fw2} {Fw3} khráp",
         "ผมพูดว่า{Tw1}{Tw2}{Tw3}ครับ", {}),
    ],
}


# ------------------------------------------------- automatyczny filtr szablonów
def template_fixed_syllables(ph_pattern):
    """Sylaby własne szablonu — bez miejsc na hasła."""
    cleaned = re.sub(r"\{[A-Za-z0-9]+\}", " ", ph_pattern)
    return syllables_of(cleaned)


dropped_templates = []


def prune(templates, ph_index):
    """Wyrzuca szablony, których sylaby nie leżą w zasobie bazy."""
    out = []
    for t in templates:
        bad = [s for s in template_fixed_syllables(t[ph_index]) if s not in KNOWN_SYL]
        if bad:
            dropped_templates.append((t[0], sorted(set(bad))))
            continue
        out.append(t)
    return out


for k in list(SOLO):
    SOLO[k] = prune(SOLO[k], 1)
for k in list(PAIR):
    PAIR[k] = prune(PAIR[k], 1)
for k in list(TRIPLE):
    TRIPLE[k] = prune(TRIPLE[k], 1)


# ------------------------------------------------------------- polska odmiana
UNINFLECTABLE = re.compile(r"…|\.\.\.")

# Hasło bywa całą wypowiedzią, nie wyrazem: „Masz dzieci?”, „Nie, dziękuję.”
# Wstawione wprost do szablonu „Mówię: {P}.” dawało „Mówię: Masz dzieci?.” —
# zdanie z dwoma znakami końca i bez sygnału, gdzie zaczyna się cytat.
# Takie hasła cytujemy i nie odmieniamy.
UTTERANCE_END = ("?", "!", ".", "…")


def is_utterance(label):
    t = (label or "").strip()
    if not t:
        return False
    if t.endswith(UTTERANCE_END):
        return True
    # Wielowyrazowe hasło zaczynające się wielką literą też jest wypowiedzią
    # („Do zobaczenia wkrótce”), nawet bez kropki na końcu.
    return " " in t and t[:1].isupper()


def core_label(label):
    core = re.sub(r"\s*\(.*?\)\s*", " ", label).strip()
    if is_utterance(core):
        # Przecinek wewnątrz wypowiedzi należy do niej („Nie, dziękuję.”),
        # więc tu NIE tniemy po przecinku.
        return core.split(" / ")[0].strip()
    return core.split(" / ")[0].split(",")[0].strip()


def polish_slot(label, case):
    core = core_label(label)
    if not core:
        return None
    if is_utterance(core):
        return "„%s”" % core.rstrip(".")
    if case is None:
        return core
    try:
        out = PG.inflect(core, case)
    except Exception:
        return None
    return out or core


def tidy(text):
    """Porządkuje interpunkcję po podstawieniu cytatu."""
    t = re.sub(r"”\s*\.", "”.", text)
    t = t.replace("?.", "?").replace("!.", "!")
    t = re.sub(r"\s+", " ", t).strip()
    return t


# ------------------------------------------------------------------- budowa
rejected, dup_ph, dup_pl = [], [], []
seen_ph, seen_pl = set(), set()
counters = Counter()


def new_id(level, cat, kind):
    pref = {"Survival": "srv"}.get(level, level.lower())
    key = "o%s-%s-%s" % (kind, pref, E.slug(cat))
    counters[key] += 1
    return "%s-%04d" % (key, counters[key])


def register_sentence(polish, s_ph):
    """Zwraca True, jeżeli zdanie jest nowe i można je przyjąć."""
    global skipped_collisions
    kph, kpl = norm_ph(s_ph), norm_pl(polish)
    if kph in base_sent_ph or kph in used_sent_ph:
        skipped_collisions += 1
        return False
    if kpl in base_sent_pl or kpl in used_sent_pl:
        skipped_collisions += 1
        return False
    used_sent_ph.add(kph)
    used_sent_pl.add(kpl)
    return True


def upper1(s):
    s = tidy(s)
    if not s:
        return s
    # Pierwszy znak bywa cudzysłowem — wielką literę stawiamy na literze.
    for i, ch in enumerate(s):
        if ch.isalpha():
            return s[:i] + ch.upper() + s[i + 1:]
    return s


def build_solo(label, ph, th, rtype, allowed, want=2):
    out = []
    for pl_pat, ph_pat, th_pat, case in SOLO[rtype]:
        slot = polish_slot(label, case)
        if not slot:
            continue
        polish = upper1(pl_pat.replace("{P}", slot))
        s_ph = ph_pat.replace("{F}", ph)
        s_th = th_pat.replace("{T}", th)
        syl = syllables_of(s_ph)
        if any(s not in allowed for s in syl):
            continue
        if not register_sentence(polish, s_ph):
            continue
        out.append((polish, s_ph, s_th, syl))
        if len(out) >= want:
            break
    return out


class Word(object):
    """Przyjęte hasło wraz z tym, co potrzebne do złożenia zdania."""

    __slots__ = ("rid", "label", "ph", "th", "rtype", "level", "cat", "sub",
                 "freq", "syl", "record", "sentences")

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)


def make_lexeme(entry):
    """Krotka wejściowa -> Word albo None (z zapisem powodu odrzucenia)."""
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

    twins = base_ph_loose.get(norm_ph_loose(ph), set()) - {ph}
    if twins:
        homophones.append((label, ph, sorted(twins)))

    lex_syl = E.syllables(ph)
    allowed = KNOWN_SYL | set(lex_syl)
    solo = build_solo(label, ph, th, rtype, allowed)
    if len(solo) < 2:
        rejected.append((label, ph, "zdań solowych: %d (wymagane 2)" % len(solo)))
        return None

    seen_ph.add(kph)
    seen_pl.add(kpl)
    rid = new_id(level, cat, "lex")

    rec = {
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
        "tags": ["sesja-o", E.slug(cat), level.lower(), "leksyka"],
        "literalMeaning": literal,
        "notes": notes,
        "commonMistakes": E.common_mistakes(ph),
        "examples": [{"polish": s[0], "thaiPhonetic": s[1], "ttsThai": s[2],
                      "audioFile": ""} for s in solo[:2]],
        "relatedWords": [],
        "audioFile": "",
        "source": SOURCE,
        "license": LICENSE,
    }
    return Word(rid=rid, label=label, ph=ph, th=th, rtype=rtype, level=level,
                cat=cat, sub=sub, freq=freq, syl=set(lex_syl), record=rec,
                sentences=list(solo))


def sentence_record(w_list, polish, s_ph, s_th, syl, layer):
    """Rekord zdania. `w_list` to hasła, które to zdanie aktywuje."""
    head = w_list[0]
    labels = ", ".join("„%s”" % w.label for w in w_list)
    note = ("Zdanie aktywujące %s (%s %s) — poza tymi hasłami zbudowane "
            "wyłącznie z materiału wcześniejszego."
            % (labels, layer, "hasło" if len(w_list) == 1 else "hasła"))
    return {
        "id": new_id(head.level, head.cat, "act"),
        "type": "sentence",
        "polish": polish,
        "polishAlternatives": [],
        "thaiPhonetic": s_ph,
        "pronunciationPolish": E.polish_read(s_ph),
        "ttsThai": s_th,
        "syllables": syl,
        "toneGuide": E.tone_guide(s_ph),
        "category": head.cat,
        "subcategory": head.sub,
        "level": head.level,
        "difficulty": E.difficulty(s_ph),
        "frequency": max(2, head.freq - 1),
        "register": "neutralny",
        "tags": ["sesja-o", "zdanie-aktywujące", layer, E.slug(head.cat),
                 head.level.lower()],
        "literalMeaning": "",
        "notes": note,
        "commonMistakes": E.common_mistakes(s_ph),
        "examples": [{"polish": polish, "thaiPhonetic": s_ph, "ttsThai": s_th,
                      "audioFile": ""}],
        "relatedWords": [w.rid for w in w_list],
        "audioFile": "",
        "source": SOURCE,
        "license": LICENSE,
    }


def build_pair(a, b):
    """Zdanie z dwoma nowymi hasłami. Zwraca rekord albo None."""
    key = (a.rtype, b.rtype)
    tpls = PAIR.get(key)
    swap = False
    if not tpls:
        tpls = PAIR.get((b.rtype, a.rtype))
        swap = True
    if not tpls:
        return None
    x, y = (b, a) if swap else (a, b)
    allowed = KNOWN_SYL | x.syl | y.syl
    for pl_pat, ph_pat, th_pat, c1, c2 in tpls:
        s1 = polish_slot(x.label, c1)
        s2 = polish_slot(y.label, c2)
        if not s1 or not s2:
            continue
        polish = upper1(pl_pat.replace("{P1}", s1).replace("{P2}", s2))
        s_ph = ph_pat.replace("{F1}", x.ph).replace("{F2}", y.ph)
        s_th = th_pat.replace("{T1}", x.th).replace("{T2}", y.th)
        syl = syllables_of(s_ph)
        if any(s not in allowed for s in syl):
            continue
        if not register_sentence(polish, s_ph):
            continue
        return sentence_record([x, y], polish, s_ph, s_th, syl, "para")
    return None


SLOT_LETTER = {"noun": "n", "verb": "v", "adjective": "a",
               "adverb": "d", "word": "w"}


def build_triple(trio):
    """Zdanie z trzema nowymi hasłami."""
    key = tuple(sorted(w.rtype for w in trio))
    tpls = TRIPLE.get(key)
    if not tpls:
        return None
    # sloty numerujemy w obrębie typu, w kolejności wystąpienia w komórce
    used = Counter()
    slots = {}
    for w in trio:
        letter = SLOT_LETTER[w.rtype]
        used[letter] += 1
        slots["%s%d" % (letter, used[letter])] = w
    allowed = KNOWN_SYL
    for w in trio:
        allowed = allowed | w.syl
    for pl_pat, ph_pat, th_pat, cases in tpls:
        polish, s_ph, s_th = pl_pat, ph_pat, th_pat
        ok = True
        for name, w in slots.items():
            slot = polish_slot(w.label, cases.get(name))
            if not slot:
                ok = False
                break
            polish = polish.replace("{P%s}" % name, slot)
            s_ph = s_ph.replace("{F%s}" % name, w.ph)
            s_th = s_th.replace("{T%s}" % name, w.th)
        if not ok or "{" in polish or "{" in s_ph or "{" in s_th:
            continue
        polish = upper1(polish)
        syl = syllables_of(s_ph)
        if any(s not in allowed for s in syl):
            continue
        if not register_sentence(polish, s_ph):
            continue
        return sentence_record(list(trio), polish, s_ph, s_th, syl, "trójka")
    return None


# ------------------------------------------------------------------- przebieg
def main():
    from lex_o_kaan import KAAN
    from lex_o_people import PEOPLE
    from lex_o_things import THINGS
    from lex_o_food import FOOD
    from lex_o_body import BODY
    from lex_o_nature import NATURE
    from lex_o_city import CITY
    from lex_o_verbs import VERBS
    from lex_o_adj import ADJ
    from lex_o_talk import TALK
    from lex_o_school import SCHOOL
    from lex_o_time import TIME
    from lex_o_geo import GEO
    from lex_o_culture import CULTURE
    from lex_o_home import HOME
    from lex_o_temple import TEMPLE
    from lex_o_more import MORE
    from lex_o_num import NUM
    from lex_o_road import ROAD
    from lex_o_close import CLOSE

    batches = [("kaan", KAAN), ("people", PEOPLE), ("things", THINGS),
               ("food", FOOD), ("body", BODY), ("nature", NATURE),
               ("city", CITY), ("verbs", VERBS), ("adj", ADJ),
               ("talk", TALK), ("school", SCHOOL), ("time", TIME),
               ("geo", GEO), ("culture", CULTURE), ("home", HOME),
               ("temple", TEMPLE), ("more", MORE),
               ("num", NUM), ("road", ROAD), ("close", CLOSE)]

    total_in = 0
    words = []
    for name, data in batches:
        for entry in data:
            total_in += 1
            w = make_lexeme(entry)
            if w:
                words.append(w)

    # ------------------------------------------------- komórki i zdania gęste
    # Komórka = cztery kolejne hasła z tej samej kategorii i poziomu. Kolejka
    # generatora ścieżki sortuje po (poziom, częstość, trudność), więc hasła
    # jednej komórki wpadają do tej samej lekcji albo do sąsiednich.
    cells = defaultdict(list)
    for w in words:
        cells[(w.cat, w.level)].append(w)

    pair_records, triple_records = [], []
    pair_by_word = defaultdict(list)
    for key, group in cells.items():
        for i in range(0, len(group), CELL):
            cell = group[i:i + CELL]
            if len(cell) < 2:
                continue
            # Nie generujemy wszystkich sześciu par komórki — to sześć zdań
            # na cztery hasła, czyli więcej materiału, niż lekcja jest w stanie
            # unieść, i niepotrzebny ciężar pliku. Bierzemy DWA SKOJARZENIA
            # DOSKONAŁE: (0-1, 2-3) oraz (0-2, 1-3). Każde hasło ma wtedy dwa
            # różne zdania parowe z dwoma różnymi partnerami, a generator
            # ścieżki ma wybór, gdy jeden z partnerów już wypadł.
            plans = [(0, 1), (2, 3), (0, 2), (1, 3)]
            for a_i, b_i in plans:
                if max(a_i, b_i) >= len(cell):
                    continue
                rec = build_pair(cell[a_i], cell[b_i])
                if rec:
                    pair_records.append(rec)
                    pair_by_word[cell[a_i].rid].append(rec["id"])
                    pair_by_word[cell[b_i].rid].append(rec["id"])
            for trio in ((0, 1, 2), (1, 2, 3)):
                if max(trio) >= len(cell):
                    continue
                rec = build_triple([cell[t] for t in trio])
                if rec:
                    triple_records.append(rec)
                    for t in trio:
                        pair_by_word[cell[t].rid].append(rec["id"])

    # ------------------------------------------------------ rekordy solowe
    solo_records = []
    for w in words:
        for (polish, s_ph, s_th, syl) in w.sentences:
            solo_records.append(sentence_record([w], polish, s_ph, s_th, syl, "solo"))

    solo_by_word = defaultdict(list)
    for r in solo_records:
        solo_by_word[r["relatedWords"][0]].append(r["id"])

    for w in words:
        w.record["relatedWords"] = (solo_by_word[w.rid] + pair_by_word[w.rid])[:8]

    # ------------------------------------------- rozdział na pliki po grupach
    by_lex = defaultdict(list)
    for r in solo_records:
        by_lex[r["relatedWords"][0]].append(r)
    # zdania parowe i trójkowe przypisujemy do pierwszego hasła — trafiają
    # do tego samego pliku co ono, więc plik zawsze da się wczytać sam.
    for r in pair_records + triple_records:
        by_lex[r["relatedWords"][0]].append(r)

    groups = [[w.record] + by_lex[w.rid] for w in words]
    files = [[] for _ in range(OUT_FILES)]
    for i, g in enumerate(groups):
        files[i % OUT_FILES].extend(g)

    written = []
    for i, recs in enumerate(files, 5):
        fn = "lexicon-%02d.json" % i
        with open(os.path.join(DATA, fn), "w", encoding="utf-8") as f:
            json.dump({"file": fn, "count": len(recs), "records": recs},
                      f, ensure_ascii=False, indent=1)
        written.append((fn, len(recs)))

    # ------------------------------------------------------------- raport
    n_sent = len(solo_records) + len(pair_records) + len(triple_records)
    print("=" * 74)
    print("  SESJA O — GENERATOR LEKSYKI")
    print("=" * 74)
    print("kandydatów na wejściu             %5d" % total_in)
    print("odrzuconych — duplikat fonetyki   %5d" % len(dup_ph))
    print("odrzuconych — duplikat znaczenia  %5d" % len(dup_pl))
    print("odrzuconych — za mało zdań        %5d" % len(rejected))
    print("szablonów pominiętych (kolizja)   %5d" % skipped_collisions)
    print("szablonów odrzuconych (sylaby)    %5d" % len(dropped_templates))
    print("-" * 74)
    print("NOWYCH HASEŁ LEKSYKALNYCH         %5d" % len(words))
    print("ZDAŃ SOLOWYCH   (1 nowe hasło)    %5d" % len(solo_records))
    print("ZDAŃ PAROWYCH   (2 nowe hasła)    %5d" % len(pair_records))
    print("ZDAŃ TRÓJKOWYCH (3 nowe hasła)    %5d" % len(triple_records))
    print("RAZEM ZDAŃ AKTYWUJĄCYCH           %5d" % n_sent)
    print("     zdań na hasło (średnio)      %5.2f" % (n_sent / max(1, len(words))))
    print("     gęstość aktywacji            %5.2f nowych haseł na zdanie"
          % ((len(solo_records) + 2 * len(pair_records) + 3 * len(triple_records))
             / max(1, n_sent)))

    print("\nPLIKI")
    for fn, n in written:
        print("  %-20s %5d rekordów" % (fn, n))

    print("\nNOWE HASŁA — POZIOMY")
    for k, v in Counter(w.level for w in words).most_common():
        print("  %-12s %5d" % (k, v))

    print("\nNOWE HASŁA — TYPY")
    for k, v in Counter(w.rtype for w in words).most_common():
        print("  %-12s %5d" % (k, v))

    print("\nNOWE HASŁA — KATEGORIE")
    for k, v in sorted(Counter(w.cat for w in words).items(), key=lambda kv: -kv[1]):
        print("  %-26s %5d" % (k, v))

    if dropped_templates:
        print("\nSZABLONY ODRZUCONE PRZEZ FILTR SYLABICZNY")
        for t, bad in dropped_templates:
            print("  %-38s brak sylab: %s" % (t[:38], ", ".join(bad)))

    if rejected:
        print("\nHASŁA ODRZUCONE Z BRAKU ZDAŃ (pierwsze 30 z %d)" % len(rejected))
        for label, ph, why in rejected[:30]:
            print("  %-34s %-22s %s" % (label[:34], ph[:22], why))

    if homophones:
        print("\nPARY MINIMALNE Z BAZĄ — %d (materiał, nie błąd)" % len(homophones))
        for label, ph, twins in homophones[:15]:
            print("  %-28s %-16s kontra %s" % (label[:28], ph, ", ".join(twins)))

    if dup_ph or dup_pl:
        print("\nDUPLIKATY (pierwsze 15 z każdego rodzaju)")
        for label, ph, why in dup_ph[:15]:
            print("  fonetyka  %-30s %-20s %s" % (label[:30], ph[:20], why))
        for label, ph, why in dup_pl[:15]:
            print("  znaczenie %-30s %-20s %s" % (label[:30], ph[:20], why))
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
