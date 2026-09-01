#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reguły przekształcania form zależnych od płci mówiącego.

Moduł pomocniczy — sam nic nie zapisuje. Używają go:
  tools/generators/build-gender-variants.py  (generowanie pola genderVariant)
  tools/validate.py                          (kontrola kompletności)

CO JEST ZALEŻNE OD PŁCI MÓWIĄCEGO W TAJSKIM
-------------------------------------------
1. Cząstka grzecznościowa na końcu wypowiedzi:
   mężczyzna  — khráp  (zawsze, w zdaniu i w pytaniu)
   kobieta    — khâ    w zdaniu oznajmującym
                khá    w pytaniu oraz po cząstce ná
2. Zaimek „ja”:
   mężczyzna  — phǒm
   kobieta    — chǎn      (mowa codzienna, także uprzejma)
                dì-chǎn   (rejestr formalny: urząd, bank, rozmowa służbowa)

To jest obowiązek gramatyczny, nie wybór stylistyczny. Mężczyzna nie może
powiedzieć khâ, kobieta nie może powiedzieć khráp.

PUŁAPKA: phǒm to także rzeczownik „włosy” (ผม). „yaa sà phǒm” to szampon,
a nie „szampon mnie”. Rozpoznajemy to po poprzedzającym słowie (HAIR_PREV)
oraz po polskim tłumaczeniu.
"""

import re

# --- fonetyka ---------------------------------------------------------------
KHRAP = "khráp"
KHA_STAT = "khâ"          # zdanie oznajmujące
KHA_QUEST = "khá"         # pytanie i po „ná”
PHOM = "phǒm"
CHAN = "chǎn"
DICHAN = "dì-chǎn"

# --- pismo tajskie (wyłącznie do pola technicznego ttsThai) -----------------
TH_KHRAP = "\u0e04\u0e23\u0e31\u0e1a"        # ครับ
TH_KHA_STAT = "\u0e04\u0e48\u0e30"           # ค่ะ
TH_KHA_QUEST = "\u0e04\u0e30"                # คะ
TH_PHOM = "\u0e1c\u0e21"                     # ผม
TH_CHAN = "\u0e09\u0e31\u0e19"               # ฉัน
TH_DICHAN = "\u0e14\u0e34\u0e09\u0e31\u0e19" # ดิฉัน

# --- zapis polski -----------------------------------------------------------
PL_KHRAP = "khrap"
PL_KHA = "kha"
PL_PHOM = "phom"
PL_CHAN = "czan"
PL_DICHAN = "di-czan"

# --- tony -------------------------------------------------------------------
TONE = {
    KHRAP: "khráp — ton wysoki",
    KHA_STAT: "khâ — ton opadający",
    KHA_QUEST: "khá — ton wysoki",
    PHOM: "phǒm — ton rosnący",
    CHAN: "chǎn — ton rosnący",
    DICHAN: "dì — ton niski; chǎn — ton rosnący",
}

# Rejestry, w których kobieta mówi dì-chǎn zamiast chǎn.
FORMAL_REGISTERS = {"formalny"}

# Słowa, po których „phǒm” znaczy „włosy”, a nie „ja”.
# „pào” (suszyć nadmuchem) i „rân/ráan tàt” dołożone w sesji N: „thîi pào phǒm”
# to suszarka do włosów, a „ráan tàt phǒm” fryzjer — w obu phǒm jest
# rzeczownikiem, nie zaimkiem.
HAIR_PREV = {"sà", "wǐi", "tàt", "yáwm", "sǐi", "yaa", "sà-", "rákʼ", "pào"}
HAIR_WORDS = ("włos", "szampon", "fryzjer", "czesa", "uczesa", "suszark")

# Hasła, których TEMATEM jest sama forma zależna od płci: „ja (mężczyzna)”,
# „partykuła grzecznościowa (kobieta)”, wzorzec „Dziękuję (mężczyzna).” w lekcji
# o cząstkach. Tutaj nawias to znaczenie hasła, a nie etykieta doklejona przez
# generator — takie wpisy uczą jednej konkretnej formy i nie wolno ich przełączać.
# Inaczej ekran pokazałby „ja (mężczyzna) — chǎn”, czyli wprost sprzeczność.
_LEXICON_LABEL = re.compile(r"\((mężczyzna|kobieta)\)\s*\.?\s*$")

# Etykieta „(mężczyzna)” doklejona na końcu zdania przykładowego była obejściem
# dla bazy, która nie znała płci mówiącego. Teraz płeć niesie struktura rekordu,
# więc etykieta jest zbędna — i szkodliwa, bo w formie żeńskiej kłóciłaby się
# z treścią („Grzecznie: dziękuję (mężczyzna). — khàwp-khun khâ”).
_SPEAKER_LABEL = re.compile(r"\s*\((mężczyzna|kobieta)\)(?=\s*\.?\s*$)")


def is_gender_lexicon(polish):
    """Czy hasło opisuje samą formę zależną od płci."""
    return bool(polish) and bool(_LEXICON_LABEL.search(polish.strip()))


def strip_speaker_label(polish):
    """Usuwa doklejoną etykietę płci mówiącego z końca zdania."""
    if not polish:
        return polish
    return _SPEAKER_LABEL.sub("", polish, count=1)


# Słowa pytajne, po których kobieta mówi khá zamiast khâ.
QUESTION_PREV = {
    "mǎi", "mái", "ná", "nâ", "rǔe", "rěu", "rǔe-plào", "plào",
    "à-rai", "arai", "nǎi", "thîi-nǎi", "thâo-rài", "mûea-rài",
    "yang-ngai", "yàang-rai", "khrai", "tham-mai", "kìi", "bàep-nǎi",
    "an-nǎi", "wan-nǎi", "châi-mǎi", "châi", "ròk", "lâ", "làw",
}

_TOK = re.compile(r"\s+")
_PUNCT = "\u201e\u201d\u2018\u2019.,?!\u2026\"'()"

_RE_MALE = re.compile(r"(?<![a-z\u00e0-\u017e-])(khráp|khràp|phǒm)(?![a-z\u00e0-\u017e-])", re.I)
_RE_FEMALE = re.compile(r"(?<![a-z\u00e0-\u017e-])(dì-chǎn|chǎn|khâ|khá)(?![a-z\u00e0-\u017e-])", re.I)


def has_male_form(text):
    """Czy tekst fonetyczny zawiera formę męską (cząstkę lub zaimek)."""
    return bool(text) and bool(_RE_MALE.search(text))


def has_female_form(text):
    return bool(text) and bool(_RE_FEMALE.search(text))


def _tokens(text):
    text = (text or "").strip()
    return _TOK.split(text) if text else []


def _bare(tok):
    return tok.strip(_PUNCT)


def _is_question(polish, phonetic):
    if polish and polish.strip().endswith("?"):
        return True
    return False


def _pronoun_flags(toks, polish=""):
    """Dla każdego wystąpienia phǒm mówi, czy to zaimek, czy „włosy”."""
    low = (polish or "").lower()
    hairy = any(w in low for w in HAIR_WORDS)
    flags = []
    for i, t in enumerate(toks):
        if _bare(t) != PHOM:
            continue
        prev = _bare(toks[i - 1]) if i else ""
        if prev in HAIR_PREV:
            flags.append(False)
        elif hairy and i > 0:
            # W haśle o włosach zaimkiem jest tylko phǒm na początku zdania.
            flags.append(False)
        else:
            flags.append(True)
    return flags


def _particle_choice(toks, idx, question):
    """khâ czy khá dla cząstki stojącej na pozycji idx."""
    prev = _bare(toks[idx - 1]) if idx else ""
    if prev in QUESTION_PREV:
        return KHA_QUEST
    return KHA_QUEST if question else KHA_STAT


def plan(phonetic, polish="", register="neutralny"):
    """Zwraca plan zamiany albo None, jeśli nie ma czego zmieniać.

    Plan: {'particles': [khâ|khá, ...], 'pronouns': [chǎn|dì-chǎn, ...],
           'pronounFlags': [bool, ...]}  — w kolejności wystąpień w tekście.
    """
    toks = _tokens(phonetic)
    if not toks:
        return None
    question = _is_question(polish, phonetic)
    pronoun = DICHAN if register in FORMAL_REGISTERS else CHAN

    particles, pronouns = [], []
    flags = _pronoun_flags(toks, polish)
    for i, t in enumerate(toks):
        b = _bare(t)
        if b in (KHRAP, "khràp"):
            particles.append(_particle_choice(toks, i, question))
    for use in flags:
        if use:
            pronouns.append(pronoun)
    if not particles and not pronouns:
        return None
    return {"particles": particles, "pronouns": pronouns, "pronounFlags": flags}


def female_phonetic(phonetic, pl):
    """Fonetyka w formie żeńskiej według gotowego planu."""
    toks = _tokens(phonetic)
    parts = list(pl["particles"])
    prons = list(pl["pronouns"])
    flags = list(pl["pronounFlags"])
    out = []
    for t in toks:
        b = _bare(t)
        if b in (KHRAP, "khràp") and parts:
            out.append(t.replace(b, parts.pop(0)))
        elif b == PHOM and flags:
            use = flags.pop(0)
            out.append(t.replace(b, prons.pop(0)) if use and prons else t)
        else:
            out.append(t)
    return " ".join(out)


def _replace_ordered(text, needle, replacements):
    """Zamienia kolejne wystąpienia needle na kolejne elementy replacements.

    Element None oznacza „zostaw bez zmian”. Gdy replacements się skończą,
    reszta wystąpień zostaje nietknięta.
    """
    out, pos, i = [], 0, 0
    while True:
        hit = text.find(needle, pos)
        if hit == -1 or i >= len(replacements):
            out.append(text[pos:])
            break
        out.append(text[pos:hit])
        rep = replacements[i]
        out.append(needle if rep is None else rep)
        pos = hit + len(needle)
        i += 1
    return "".join(out)


def female_tts(tts, pl):
    """Pismo tajskie w formie żeńskiej (pole techniczne, nigdy na ekranie)."""
    if not tts:
        return tts
    parts = [TH_KHA_QUEST if p == KHA_QUEST else TH_KHA_STAT for p in pl["particles"]]
    if parts:
        n_thai = tts.count(TH_KHRAP)
        if n_thai and n_thai < len(parts):
            # Zapis ze znakiem powtórzenia ๆ: jedno ครับ, dwa khráp.
            parts = parts[:n_thai]
        tts = _replace_ordered(tts, TH_KHRAP, parts)
    if pl["pronouns"]:
        pron_th = TH_DICHAN if pl["pronouns"][0] == DICHAN else TH_CHAN
        seq = [pron_th if use else None for use in pl["pronounFlags"]]
        tts = _replace_ordered(tts, TH_PHOM, seq)
    return tts


def female_pron_pl(pron_pl, phonetic, pl):
    """Zapis „czytaj po polsku” w formie żeńskiej.

    Fonetyka i zapis polski mają w bazie tę samą liczbę wyrazów, więc idziemy
    po indeksach. Gdy się rozjadą (zdarza się w kilku rekordach), wracamy do
    prostej zamiany napisów.
    """
    if not pron_pl:
        return pron_pl
    src = _tokens(phonetic)
    dst = _tokens(pron_pl)
    parts = list(pl["particles"])
    flags = list(pl["pronounFlags"])
    prons = list(pl["pronouns"])
    if len(src) == len(dst):
        out = []
        for s, d in zip(src, dst):
            b = _bare(s)
            if b in (KHRAP, "khràp") and parts:
                parts.pop(0)
                out.append(d.replace(PL_KHRAP, PL_KHA))
            elif b == PHOM and flags:
                use = flags.pop(0)
                if use and prons:
                    rep = PL_DICHAN if prons.pop(0) == DICHAN else PL_CHAN
                    out.append(d.replace(PL_PHOM, rep))
                else:
                    out.append(d)
            else:
                out.append(d)
        return " ".join(out)
    # zapas
    txt = re.sub(r"\bkhrap\b", PL_KHA, pron_pl)
    if prons:
        rep = PL_DICHAN if prons[0] == DICHAN else PL_CHAN
        txt = re.sub(r"\bphom\b", rep, txt)
    return txt


def female_tone_guide(guide, pl):
    """Opis tonów dopasowany do formy żeńskiej."""
    if not guide:
        return guide
    parts = [TONE[p] for p in pl["particles"]]
    guide = _replace_ordered(guide, TONE[KHRAP], parts)
    if pl["pronouns"]:
        rep = TONE[DICHAN] if pl["pronouns"][0] == DICHAN else TONE[CHAN]
        seq = [rep if use else None for use in pl["pronounFlags"]]
        guide = _replace_ordered(guide, TONE[PHOM], seq)
    return guide


# --- kierunek odwrotny: forma męska ----------------------------------------
# Potrzebny tylko w dialogach, gdzie rola ma płeć wynikającą ze scenariusza
# (kelner, policjant) i kwestia musi brzmieć po męsku niezależnie od ustawienia.
_MALE_MAP_PH = [(DICHAN, PHOM), (CHAN, PHOM), (KHA_STAT, KHRAP), (KHA_QUEST, KHRAP)]
_MALE_MAP_TH = [(TH_DICHAN, TH_PHOM), (TH_CHAN, TH_PHOM),
                (TH_KHA_STAT, TH_KHRAP), (TH_KHA_QUEST, TH_KHRAP)]
_MALE_MAP_PL = [(PL_DICHAN, PL_PHOM), (PL_CHAN, PL_PHOM), (PL_KHA, PL_KHRAP)]
_MALE_MAP_TONE = [(TONE[DICHAN], TONE[PHOM]), (TONE[CHAN], TONE[PHOM]),
                  (TONE[KHA_STAT], TONE[KHRAP]), (TONE[KHA_QUEST], TONE[KHRAP])]


def to_male(text, kind):
    """kind: 'ph' | 'th' | 'pl' | 'tone'."""
    if not text:
        return text
    table = {"ph": _MALE_MAP_PH, "th": _MALE_MAP_TH,
             "pl": _MALE_MAP_PL, "tone": _MALE_MAP_TONE}[kind]
    for a, b in table:
        if kind in ("ph", "pl"):
            text = re.sub(r"(?<![a-z\u00e0-\u017e-])" + re.escape(a) + r"(?![a-z\u00e0-\u017e-])",
                          b, text)
        else:
            text = text.replace(a, b)
    return text


def to_female_fixed(node, register="neutralny"):
    """Wymusza formę żeńską w samym rekordzie (rola kobieca w dialogu)."""
    src = node.get("thaiPhonetic", "")
    pl = plan(src, node.get("polish", ""), register)
    if not pl:
        return False
    if node.get("pronunciationPolish"):
        node["pronunciationPolish"] = female_pron_pl(node["pronunciationPolish"], src, pl)
    node["thaiPhonetic"] = female_phonetic(src, pl)
    if node.get("ttsThai"):
        node["ttsThai"] = female_tts(node["ttsThai"], pl)
    if node.get("toneGuide"):
        node["toneGuide"] = female_tone_guide(node["toneGuide"], pl)
    return True


def build_variant(node, register="neutralny"):
    """Buduje zawartość genderVariant.female dla rekordu, przykładu albo kwestii.

    Zwraca None, jeśli w tekście nie ma formy zależnej od płci.
    """
    phonetic = node.get("thaiPhonetic", "")
    pl = plan(phonetic, node.get("polish", ""), register)
    if not pl:
        return None
    out = {"thaiPhonetic": female_phonetic(phonetic, pl)}
    if node.get("pronunciationPolish"):
        out["pronunciationPolish"] = female_pron_pl(node["pronunciationPolish"], phonetic, pl)
    if node.get("ttsThai"):
        out["ttsThai"] = female_tts(node["ttsThai"], pl)
    if node.get("toneGuide"):
        out["toneGuide"] = female_tone_guide(node["toneGuide"], pl)
    out["_usesPronoun"] = bool(pl["pronouns"])
    out["_pronoun"] = pl["pronouns"][0] if pl["pronouns"] else None
    return out
