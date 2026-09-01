# -*- coding: utf-8 -*-
"""Silnik budowy rekordow Thai All-in-One."""
import re, unicodedata

TONE_MARKS = {
    "\u0301": ("wysoki", "á"),
    "\u0300": ("niski", "à"),
    "\u0302": ("opadający", "â"),
    "\u030c": ("rosnący", "ǎ"),
    "\u0304": ("średni", "ā"),
}

def _decomp(s):
    return unicodedata.normalize("NFD", s)

def strip_tones(s):
    d = _decomp(s)
    return unicodedata.normalize("NFC", "".join(c for c in d if c not in TONE_MARKS))

def syllables(ph):
    parts = re.split(r"[\s\-]+", ph.strip())
    return [p for p in parts if p]

def tone_of(syl):
    d = _decomp(syl)
    for c in d:
        if c in TONE_MARKS:
            return TONE_MARKS[c][0]
    return "średni"

def tone_guide(ph):
    out = []
    for s in syllables(ph):
        out.append("%s — ton %s" % (s, tone_of(s)))
    return "; ".join(out)

def polish_read(ph):
    """Zapis pomocniczy: jak Polak ma to przeczytać (bez znaków tonów)."""
    s = strip_tones(ph).lower()
    s = re.sub(r"(?<![aiu])aw(?![aeiou\u0259])", "o", s)   # ɔː
    s = s.replace("ch", "cz")
    s = s.replace("j", "d\u017a")
    s = s.replace("ai", "aj").replace("oi", "oj").replace("ui", "uj").replace("ao", "au")
    s = re.sub(r"ue(?!a)", "y", s)                       # ɯ ~ polskie y
    s = s.replace("oe", "e").replace("\u0259\u0259", "ee").replace("\u0259", "e")
    s = re.sub(r"w(?=[aeiouy])", "\u0142", s)
    s = re.sub(r"y(?=[aeiou])", "j", s)
    return s

def difficulty(ph):
    syl = syllables(ph)
    hard = sum(1 for s in syl if tone_of(s) in ("opadający", "rosnący"))
    d = 1 + (len(syl) > 1) + (len(syl) > 3) + (hard > 0) + (hard > 2)
    return max(1, min(5, d))

_MISTAKE_RULES = [
    (r"\bkh|kh", "kh to polskie „k” z wyraźnym przydechem, nie „ch”."),
    (r"ph", "ph to „p” z przydechem — nigdy nie czytaj tego jak „f”."),
    (r"th", "th to „t” z przydechem — nigdy jak angielskie „th”."),
    (r"^ng|[\s\-]ng", "ng na początku sylaby to jeden dźwięk, jak w „bank” bez „k”."),
    (r"aa|ii|uu|oo|ee", "Samogłoska długa — trzymaj ją wyraźnie dłużej niż w polskim."),
    (r"[aeiou]{1,2}[ptk]$", "Końcowe -p, -t, -k są niezwolnione: zatrzymujesz dźwięk, nie wybuchasz nim."),
    (r"r", "Tajskie „r” bywa wymawiane jak lekkie „l” — nie warcz po polsku."),
]

def common_mistakes(ph, extra=""):
    hints = []
    low = ph.lower()
    for pat, hint in _MISTAKE_RULES:
        if re.search(pat, low) and hint not in hints:
            hints.append(hint)
        if len(hints) >= 2:
            break
    tones = {tone_of(s) for s in syllables(ph)}
    if "opadający" in tones:
        hints.append("Ton opadający zaczyna się wysoko i spada — Polacy często robią z niego zwykłe zdanie oznajmujące.")
    elif "rosnący" in tones:
        hints.append("Ton rosnący brzmi jak polskie pytanie: głos idzie w górę do końca sylaby.")
    if extra:
        hints.append(extra)
    return " ".join(hints[:3])

SLUG = {
    "Podstawy i grzeczność": "basic", "Jedzenie i napoje": "food", "Restauracja": "resto",
    "Miejsca i orientacja": "place", "Transport": "transport", "Hotel": "hotel",
    "Zakupy i pieniądze": "shop", "Zdrowie": "health", "Ludzie i rodzina": "people",
    "Dom i codzienność": "home", "Praca i nauka": "work", "Czasowniki": "verb",
    "Cechy i opinie": "adj", "Liczby i liczenie": "num", "Czas i daty": "time",
    "Pytania": "quest", "Awarie i pomoc": "help", "Small talk": "talk",
    "Pogoda i przyroda": "nature", "Gramatyka użytkowa": "gram",
}

def slug(cat):
    return SLUG.get(cat, "misc")

class Builder:
    def __init__(self):
        self.counter = {}
        self.seen_key = set()
        self.ids = set()

    def new_id(self, level, cat):
        pref = {"Survival": "srv"}.get(level, level.lower())
        key = "%s-%s" % (pref, slug(cat))
        self.counter[key] = self.counter.get(key, 0) + 1
        return "%s-%04d" % (key, self.counter[key])

    def make(self, level, polish, ph, th, cat, sub, rtype, tags,
             freq=3, register="neutralny", notes="", literal="", mistakes_extra="",
             examples=None, related=None, alternatives=None):
        key = (strip_tones(polish).lower(), th)
        if key in self.seen_key:
            return None
        self.seen_key.add(key)
        rid = self.new_id(level, cat)
        self.ids.add(rid)
        exs = []
        for ex in (examples or []):
            exs.append({
                "polish": ex[0],
                "thaiPhonetic": ex[1],
                "ttsThai": ex[2],
                "audioFile": "",
            })
        return {
            "id": rid,
            "type": rtype,
            "polish": polish,
            "polishAlternatives": alternatives or [],
            "thaiPhonetic": ph,
            "pronunciationPolish": polish_read(ph),
            "ttsThai": th,
            "syllables": syllables(ph),
            "toneGuide": tone_guide(ph),
            "category": cat,
            "subcategory": sub,
            "level": level,
            "difficulty": difficulty(ph),
            "frequency": freq,
            "register": register,
            "tags": tags,
            "literalMeaning": literal,
            "notes": notes,
            "commonMistakes": common_mistakes(ph, mistakes_extra),
            "examples": exs,
            "relatedWords": related or [],
            "audioFile": "",
            "source": "Baza projektu Thai All-in-One",
            "license": "Do weryfikacji przed publiczną publikacją",
        }
