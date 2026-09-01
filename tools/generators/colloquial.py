#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reguły redukcji: forma słownikowa -> forma potoczna.

Moduł pomocniczy — sam nic nie zapisuje. Używają go:
  tools/generators/build-colloquial.py   (generowanie pola colloquial)
  tools/validate.py                      (kontrola poprawności)

PO CO TO JEST
-------------
Syntezator mowy czyta formą słownikową: każda sylaba wymówiona osobno,
wolno, z pełnym konturem tonalnym. Prawdziwy rozmówca mówi inaczej —
skraca samogłoski nieakcentowane, upraszcza zbitki spółgłoskowe, zlewa
sylaby i gubi część wygłosów. Ktoś wytrenowany wyłącznie na czystym TTS
rozumie nagranie i nie rozumie człowieka.

Pole `colloquial` daje drugi zapis tego samego zdania — taki, jaki uczący
się faktycznie usłyszy na ulicy. Interfejs pokazuje oba obok siebie,
a w trybie potocznym syntezator dostaje wariant zredukowany.

SIEDEM REGUŁ
------------
Reguły idą w ustalonej kolejności; każda zapisuje swój identyfikator,
więc przy każdym zdaniu widać, co i dlaczego się zmieniło.

  1. lex          leksykon form utrwalonych (sawàt-dii -> wàt-dii)
  2. cluster-r    /r/ znika ze zbitki nagłosowej (khráp -> kháp)
  3. cluster-l    /l/ znika ze zbitki nagłosowej (plaa -> paa)
  4. r-l          pojedyncze /r/ w nagłosie brzmi jak /l/ (rót -> lót)
  5. coda-drop    wygłosowe -p/-k sylaby nieakcentowanej gubi się
  6. vowel-short  samogłoska długa w sylabie nieakcentowanej skraca się
  7. tone-lax     ton rosnący w sylabie nieakcentowanej spłaszcza się do wysokiego

„Sylaba nieakcentowana” ma tu znaczenie ścisłe: w tajskim wyrazie
wielosylabowym akcent pada na sylabę ostatnią, więc reguły 5-7 dotyczą
wyłącznie sylab niebędących ostatnią sylabą swojego wyrazu. Wyraz
jednosylabowy nie jest redukowany — w mowie potocznej nadal niesie pełny ton.

CZEGO TU NIE MA — I DLACZEGO
----------------------------
Reguła 5 jest z całej siódemki najmniej pewna. Tajskie wygłosy zwarte są
niezwolnione, ale nie znikają: znacznie częściej ulegają zwarciu krtaniowemu
niż wypadają. Dlatego jest zawężona do dwóch wygłosów (-p, -k; -t tajski
trzyma najmocniej, por. สวัสดี -> หวัดดี, gdzie -t zostaje) i do pozycji
przed spółgłoską zwartą lub nosową. Wszędzie tam, gdzie istnieje forma
utrwalona, pierwszeństwo ma leksykon z reguły 1 i dalsze reguły już tego
wyrazu nie ruszają.

Nie ma tu też upodobnień międzywyrazowych ani zlewania granic wyrazów —
to zjawiska ciągłe, których zapis literowy nie odda bez wprowadzania
symboli, których uczący się nie zna.
"""

import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# --- opis reguł (używany też w README i w interfejsie) ----------------------

RULES = [
    ("lex", "forma utrwalona",
     "Zwrot ma w mowie potocznej własną, ustaloną postać — nie wynika ona z reguł ogólnych."),
    ("cluster-r", "zbitka bez /r/",
     "W zbitce nagłosowej kr-, khr-, pr-, phr-, tr-, thr- /r/ znika: khráp brzmi kháp."),
    ("cluster-l", "zbitka bez /l/",
     "W zbitce nagłosowej kl-, khl-, pl-, phl- /l/ znika: plaa brzmi paa."),
    ("r-l", "/r/ jak /l/",
     "Pojedyncze /r/ w nagłosie wymawiane jest jak lekkie /l/: rót brzmi lót."),
    ("coda-drop", "zgubiony wygłos",
     "Wygłosowe -p lub -k sylaby nieakcentowanej gubi się przed następną spółgłoską."),
    ("vowel-short", "skrócona samogłoska",
     "Samogłoska długa w sylabie nieakcentowanej skraca się do krótkiej."),
    ("tone-lax", "spłaszczony ton",
     "Ton rosnący w sylabie nieakcentowanej nie zdąży się wznieść i brzmi jak wysoki."),
]

RULE_IDS = [r[0] for r in RULES]
RULE_ORDER = {r: i for i, r in enumerate(RULE_IDS)}

# --- budowa sylaby ----------------------------------------------------------

ONSETS = ["khr", "khl", "khw", "phr", "phl", "thr", "kr", "kl", "kw",
          "pr", "pl", "tr", "ch", "kh", "ph", "th", "ng",
          "b", "d", "f", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "w", "y"]

# Wygłosy właściwe. -w i -y to półsamogłoski wchodzące w skład dyftongu
# (khǎw, láew), nie spółgłoski wygłosowe — nie wolno ich ruszać.
CODAS = ["ng", "p", "t", "k", "m", "n"]

# Samogłoski długie i ich krótkie odpowiedniki.
LONG_TO_SHORT = {
    "aa": "a", "ii": "i", "uu": "u", "ee": "e", "oo": "o",
    "\u0259\u0259": "\u0259",          # əə -> ə
}

TONE_MARKS = "\u0300\u0301\u0302\u030c"        # grave, acute, circumflex, caron
RISING = "\u030c"
HIGH = "\u0301"

_ONSET_RE = re.compile("^(" + "|".join(sorted(ONSETS, key=len, reverse=True)) + ")")
_CODA_RE = re.compile("(" + "|".join(sorted(CODAS, key=len, reverse=True)) + ")$")

# Jądra samogłoskowe faktycznie występujące w tej transkrypcji. Reguły ruszające
# samogłoskę albo ton działają WYŁĄCZNIE wtedy, gdy jądro należy do tej listy.
#
# Powód jest praktyczny: część haseł ma wyraz wielosylabowy zapisany bez dywizu
# („kradàat”), a wtedy naiwny rozbiór daje jądro „adaa”, którego w języku nie ma.
# Bez tej kontroli reguła skracania samogłoski przeniosłaby znak tonu na inną
# sylabę niż ta, do której należy — czyli zrobiłaby z wyrazu inny wyraz.
VALID_NUCLEI = {
    "a", "aa", "i", "ii", "u", "uu", "e", "ee", "o", "oo",
    "ae", "aae", "oe", "ooe", "ue", "aw", "aaw", "ia", "ua", "uea",
    "ai", "aai", "ao", "aao", "oi", "oei", "ui", "uai", "ueai", "awi",
    "aew", "ew", "iao", "iaw", "iu", "iw",
    "\u0259", "\u0259\u0259",
}


def _nfd(s):
    return unicodedata.normalize("NFD", s or "")


def _nfc(s):
    return unicodedata.normalize("NFC", s or "")


def _bare(s):
    """Sylaba bez znaków tonu — do dopasowywania wzorców literowych."""
    return "".join(c for c in _nfd(s) if c not in TONE_MARKS)


# --- leksykon form utrwalonych ---------------------------------------------
# Klucz: wyraz w formie słownikowej (z tonami). Wartość: forma potoczna.
# Wyłącznie postacie poświadczone w mowie codziennej i w potocznej pisowni —
# nie wymyślamy tu nic, czego Tajowie sami nie piszą.

LEXICON = {
    "khráp": "kháp",              # ครับ -> คับ
    "khràp": "kháp",
    "sawàt-dii": "wàt-dii",       # สวัสดี -> หวัดดี
    "khàwp-khun": "khàp-khun",    # skrócenie jądra, wygłos zostaje
    "à-rai": "rai",               # อะไร -> ไร
    "mǎi": "mái",                 # ไหม -> มั้ย (partykuła pytajna)
    "yàang-rai": "yang-ngai",     # อย่างไร -> ยังไง
    "dì-chǎn": "chán",            # ดิฉัน -> ชั้น
    "chǎn": "chán",               # ฉัน -> ชั้น
    "thâo-rài": "thâo-rai",       # เท่าไร -> เท่าไหร่
}

# --- pismo tajskie dla syntezatora -----------------------------------------
# Znacznie węższa lista niż fonetyczna: syntezator musi umieć to przeczytać.
# Wszystkie pozycje to normalne potoczne pisownie, które silniki TTS znają.
# (pattern, replacement, gdzie wolno podmieniać: 'any' | 'end' | 'start')

TH_KHRAP = "\u0e04\u0e23\u0e31\u0e1a"                       # ครับ
TH_KHAP = "\u0e04\u0e31\u0e1a"                              # คับ
TH_SAWATDII = "\u0e2a\u0e27\u0e31\u0e2a\u0e14\u0e35"        # สวัสดี
TH_WATDII = "\u0e2b\u0e27\u0e31\u0e14\u0e14\u0e35"          # หวัดดี
TH_ARAI = "\u0e2d\u0e30\u0e44\u0e23"                        # อะไร
TH_RAI = "\u0e44\u0e23"                                     # ไร
TH_MAI_Q = "\u0e44\u0e2b\u0e21"                             # ไหม
TH_MAI_COLL = "\u0e21\u0e31\u0e49\u0e22"                    # มั้ย
TH_YANGRAI = "\u0e2d\u0e22\u0e48\u0e32\u0e07\u0e44\u0e23"   # อย่างไร
TH_YANGNGAI = "\u0e22\u0e31\u0e07\u0e44\u0e07"              # ยังไง
TH_DICHAN = "\u0e14\u0e34\u0e09\u0e31\u0e19"                # ดิฉัน
TH_CHAN = "\u0e09\u0e31\u0e19"                              # ฉัน
TH_CHAN_COLL = "\u0e0a\u0e31\u0e49\u0e19"                   # ชั้น

TH_SUBS = [
    (TH_KHRAP, TH_KHAP, "any"),
    (TH_SAWATDII, TH_WATDII, "any"),
    (TH_YANGRAI, TH_YANGNGAI, "any"),
    (TH_ARAI, TH_RAI, "any"),
    (TH_DICHAN, TH_CHAN_COLL, "any"),
    # ไหม to także „jedwab” — podmieniamy wyłącznie na końcu wypowiedzi,
    # czyli tam, gdzie to na pewno partykuła pytajna.
    (TH_MAI_Q, TH_MAI_COLL, "end"),
    # ฉัน bywa cząstką dłuższych wyrazów — tylko na początku wypowiedzi
    # albo po spacji mamy pewność, że to zaimek.
    (TH_CHAN, TH_CHAN_COLL, "start"),
]


def colloquial_thai(thai):
    """Potoczna pisownia tajska dla syntezatora. Zwraca (tekst, czy_zmieniono)."""
    if not thai:
        return thai, False
    out = thai
    for pat, rep, where in TH_SUBS:
        if where == "any":
            out = out.replace(pat, rep)
        elif where == "end":
            if out.endswith(pat):
                out = out[:-len(pat)] + rep
        elif where == "start":
            if out.startswith(pat):
                out = rep + out[len(pat):]
            out = out.replace(" " + pat, " " + rep)
    return out, out != thai


# --- reguły fonetyczne ------------------------------------------------------

_CLUSTER_R = [("khr", "kh"), ("phr", "ph"), ("thr", "th"),
              ("kr", "k"), ("pr", "p"), ("tr", "t")]
_CLUSTER_L = [("khl", "kh"), ("phl", "ph"), ("kl", "k"), ("pl", "p")]

# Wygłos gubi się tylko przed spółgłoską zwartą albo nosową.
_BLOCKING_ONSETS = ("p", "ph", "b", "t", "th", "d", "k", "kh", "j", "ch", "m", "n", "ng")

_PUNCT = ".,?!\u2026:;\u201e\u201d\u2018\u2019\"'()"


def _split_mark(syl):
    """Rozdziela sylabę na litery bez tonu i pozycję znaku tonu wśród nich.

    Znak tonu nigdy nie jest przenoszony: wszystkie reguły edytują litery
    wokół niego, a on zostaje przy swojej samogłosce. Naiwne składanie sylaby
    od nowa przesuwało go na pierwszą samogłoskę i zmieniało wyraz w inny wyraz.
    """
    plain, mark, pos = [], "", -1
    for c in _nfd(syl):
        if c in TONE_MARKS:
            mark, pos = c, len(plain) - 1
        else:
            plain.append(c)
    return plain, mark, pos


def _join_mark(plain, mark, pos):
    if not mark or pos < 0 or pos >= len(plain):
        return _nfc("".join(plain))
    return _nfc("".join(plain[:pos + 1]) + mark + "".join(plain[pos + 1:]))


def _parse(text):
    """(nagłos, jądro, wygłos) dla łańcucha bez znaków tonu."""
    m = _ONSET_RE.match(text)
    onset = m.group(1) if m else ""
    rest = text[len(onset):]
    m2 = _CODA_RE.search(rest)
    coda = m2.group(1) if m2 and len(rest) > len(m2.group(1)) else ""
    return onset, rest[:len(rest) - len(coda)], coda


def _reduce_syllable(syl, unstressed, next_syl, used):
    """Reguły 2-7 na jednej sylabie."""
    plain, mark, pos = _split_mark(syl)
    text = "".join(plain)
    onset, nucleus, coda = _parse(text)
    if not nucleus:
        return syl

    cut = []          # indeksy liter do usunięcia
    swap = {}         # indeks -> nowa litera
    new_mark = mark

    # 2-3. uproszczenie zbitki nagłosowej: gubi się druga litera zbitki,
    #      czyli /r/ albo /l/. Litera nagłosu nigdy nie nosi znaku tonu.
    for src, dst in _CLUSTER_R:
        if onset == src:
            cut.append(len(dst))
            used.add("cluster-r")
            break
    else:
        for src, dst in _CLUSTER_L:
            if onset == src:
                cut.append(len(dst))
                used.add("cluster-l")
                break

    # 4. pojedyncze /r/ w nagłosie brzmi jak /l/
    if onset == "r":
        swap[0] = "l"
        used.add("r-l")

    # 5. zgubiony wygłos — sylaba nieakcentowana, wygłos -p albo -k,
    #    następna sylaba zaczyna się spółgłoską zwartą lub nosową.
    if unstressed and coda in ("p", "k") and nucleus in VALID_NUCLEI and next_syl:
        nxt = "".join(_split_mark(next_syl)[0])
        nm = _ONSET_RE.match(nxt)
        if nm and nm.group(1) in _BLOCKING_ONSETS:
            cut.append(len(text) - 1)
            used.add("coda-drop")

    # 6. skrócenie samogłoski nieakcentowanej — usuwamy drugą literę pary.
    if unstressed and nucleus in LONG_TO_SHORT:
        cut.append(len(onset) + 1)
        used.add("vowel-short")

    # 7. ton rosnący w sylabie nieakcentowanej spłaszcza się do wysokiego.
    if unstressed and mark == RISING and nucleus in VALID_NUCLEI:
        new_mark = HIGH
        used.add("tone-lax")

    if not cut and not swap and new_mark == mark:
        return syl

    out, new_pos = [], pos
    for i, ch in enumerate(plain):
        if i in cut:
            if i <= pos:
                new_pos -= 1
            continue
        out.append(swap.get(i, ch))
    return _join_mark(out, new_mark, new_pos)


def _reduce_word(word, used):
    """Redukuje jeden wyraz (ciąg sylab połączonych dywizem)."""
    head, tail, core = "", "", word
    while core and core[0] in _PUNCT:
        head += core[0]
        core = core[1:]
    while core and core[-1] in _PUNCT:
        tail = core[-1] + tail
        core = core[:-1]
    if not core:
        return word

    # 1. leksykon — forma utrwalona wygrywa i zamyka sprawę tego wyrazu.
    if core in LEXICON:
        used.add("lex")
        return head + LEXICON[core] + tail

    parts = core.split("-")
    last = len(parts) - 1
    out = [_reduce_syllable(syl, i < last, parts[i + 1] if i < last else None, used)
           for i, syl in enumerate(parts)]
    return head + "-".join(out) + tail


def reduce_phonetic(phonetic):
    """Zwraca (forma potoczna, posortowana lista użytych reguł)."""
    if not phonetic:
        return phonetic, []
    used = set()
    words = [_reduce_word(w, used) for w in phonetic.split(" ")]
    out = " ".join(words)
    rules = sorted(used, key=lambda r: RULE_ORDER[r])
    return out, rules


def syllable_count(phonetic):
    """Liczba sylab w zapisie fonetycznym."""
    n = 0
    for w in (phonetic or "").split():
        core = w.strip(_PUNCT)
        if core:
            n += len(core.split("-"))
    return n


def build(phonetic, thai=None, polish_read=None):
    """Pełny wariant potoczny albo None, jeżeli nic się nie zmienia.

    polish_read — funkcja transkrybująca na zapis „czytaj po polsku”
    (przekazywana z zewnątrz, żeby moduł nie zależał od generatora).
    """
    if not phonetic:
        return None
    reduced, rules = reduce_phonetic(phonetic)
    th, th_changed = colloquial_thai(thai)
    if reduced == phonetic and not th_changed:
        return None

    out = {"thaiPhonetic": reduced, "rules": rules}
    if polish_read:
        out["pronunciationPolish"] = polish_read(reduced)
    if thai:
        out["ttsThai"] = th
    return out
