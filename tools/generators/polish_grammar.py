# -*- coding: utf-8 -*-
"""Odmiana polska dla generatorów Thai All-in-One (etap 8, sesja G).

Powód powstania: konwencja „Poproszę: woda” omijała polską deklinację i objęła
2 959 rekordów. Żeby ją usunąć, trzeba umieć odmienić każde hasło słownikowe
przez przypadki — ręcznie byłoby to kilka tysięcy form.

Dwa tryby pracy:

1. **Z Morfeuszem 2** (`pip install morfeusz2`) — pełna morfologia SGJP.
   Moduł generuje formy i zapisuje je do `inflect-cache.json`.
2. **Bez Morfeusza** — moduł czyta wyłącznie `inflect-cache.json`.
   Dzięki temu repozytorium jest samowystarczalne: kolejne sesje odtworzą
   dane bez instalowania czegokolwiek.

Cache jest źródłem prawdy dla ręcznych poprawek. Formy wpisane w
`OVERRIDES` mają pierwszeństwo przed Morfeuszem — tam trafiają wyrazy,
których słownik nie zna (nazwy potraw, zapożyczenia) albo odmienia inaczej,
niż wymaga tego kontekst kursu.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = os.path.join(HERE, "inflect-cache.json")

CASES = ["nom", "gen", "dat", "acc", "inst", "loc"]

# ---------------------------------------------------------------------------
# Morfeusz — opcjonalny
# ---------------------------------------------------------------------------
try:
    import morfeusz2
    _MORF = morfeusz2.Morfeusz()
except Exception:  # pragma: no cover - zależy od środowiska
    _MORF = None


def morfeusz_available():
    return _MORF is not None


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
def _load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


_CACHE = _load_cache()


def save_cache():
    with open(CACHE_PATH, "w", encoding="utf-8") as fh:
        json.dump(_CACHE, fh, ensure_ascii=False, indent=1, sort_keys=True)


# ---------------------------------------------------------------------------
# Wyjątki i wyrazy nieodmienne
# ---------------------------------------------------------------------------
# Wyrazy, które w kursie zostają bez zmian we wszystkich przypadkach.
INDECLINABLE = {
    "pad", "thai", "tom", "yam", "som", "tam", "khao", "soi", "kafe", "menu",
    "taxi", "wifi", "sms", "atm", "usd", "spa", "tuk-tuk", "tuktuk",
    "mango", "kakao", "espresso", "latte", "sushi", "chili", "curry",
    "boa", "euro", "kimono", "jury", "alibi", "tabu", "bikini",
}

# Hasła, których Morfeusz nie rozstrzyga poprawnie w kontekście kursu.
# Klucz: hasło w mianowniku (małe litery). Wartość: formy przypadków.
OVERRIDES = {
    "mango": {c: "mango" for c in CASES},
    "chili": {c: "chili" for c in CASES},
    "curry": {c: "curry" for c in CASES},
    "menu": {c: "menu" for c in CASES},
    "taxi": {c: "taxi" for c in CASES},
    "wi-fi": {c: "wi-fi" for c in CASES},
    "pad thai": {c: "pad thai" for c in CASES},
    "siedem-jedenaście": {c: "siedem-jedenaście" for c in CASES},
    "powerbank": {
        "nom": "powerbank", "gen": "powerbanku", "dat": "powerbankowi",
        "acc": "powerbank", "inst": "powerbankiem", "loc": "powerbanku",
    },
    "zameldowanie": {
        "nom": "zameldowanie", "gen": "zameldowania", "dat": "zameldowaniu",
        "acc": "zameldowanie", "inst": "zameldowaniem", "loc": "zameldowaniu",
    },
    "wymeldowanie": {
        "nom": "wymeldowanie", "gen": "wymeldowania", "dat": "wymeldowaniu",
        "acc": "wymeldowanie", "inst": "wymeldowaniem", "loc": "wymeldowaniu",
    },
    "tuk-tuk": {
        "nom": "tuk-tuk", "gen": "tuk-tuka", "dat": "tuk-tukowi",
        "acc": "tuk-tuka", "inst": "tuk-tukiem", "loc": "tuk-tuku",
    },
}

# Przyimki — od nich zaczyna się ogon frazy, którego nie odmieniamy.
PREPS = {
    "z", "ze", "w", "we", "na", "do", "o", "od", "po", "przy", "dla", "bez",
    "nad", "pod", "za", "przed", "u", "ku", "obok", "wokół", "i", "oraz",
}


# ---------------------------------------------------------------------------
# Analiza pojedynczego wyrazu przez Morfeusza
# ---------------------------------------------------------------------------
ADJ_TAGS = ("adj", "ppas", "pact")


def _generate(lemma):
    """Wszystkie formy leksemu: lista (forma, tag)."""
    if _MORF is None:
        return []
    try:
        return [(f[0], f[2]) for f in _MORF.generate(lemma)]
    except Exception:
        return []


def _analyse(word):
    """Rozbiór formy: lista (lemat, tag). Lemat bez kwalifikatora po dwukropku."""
    if _MORF is None:
        return []
    try:
        return [(seg[2][1].split(":")[0], seg[2][2]) for seg in _MORF.analyse(word)]
    except Exception:
        return []


def _has_reading(word, kinds):
    return any(tag.split(":")[0] in kinds for _, tag in _analyse(word))


def _noun_lemma(word):
    """Lemat rzeczownikowy formy + liczba, w jakiej podano hasło."""
    best = None
    for lemma, tag in _analyse(word):
        if not tag.startswith("subst"):
            continue
        number = "pl" if ":pl:" in tag else "sg"
        is_nom = _case_of(tag, "nom")
        # hasła słownikowe podajemy w mianowniku; pojedyncza ma pierwszeństwo
        score = (2 if is_nom else 0) + (1 if number == "sg" else 0)
        if best is None or score > best[0]:
            best = (score, lemma, number)
    if best is None:
        return None
    return best[1], best[2]


def _case_of(tag, case):
    for p in tag.split(":"):
        if case in p.split("."):
            return True
    return False


def _gender_of(tag):
    for p in tag.split(":"):
        s = p.split(".")
        for g in ("m1", "m2", "m3", "f", "n"):
            if g in s:
                return g
    return "n"


def _guess_gender(word):
    if word.endswith(("a", "ść", "ń", "ź")):
        return "f"
    if word.endswith(("o", "e", "ę", "um")):
        return "n"
    return "m3"


def _noun_forms(word, force_number=None):
    """Formy rzeczownika: {case: forma, _gender, _number}."""
    low = word.lower()
    if low in OVERRIDES:
        o = dict(OVERRIDES[low])
        o["_gender"] = _guess_gender(low)
        o["_number"] = "sg"
        return o
    if low in INDECLINABLE:
        o = {c: word for c in CASES}
        o["_gender"] = "n"
        o["_number"] = "sg"
        return o

    res = _noun_lemma(word)
    if res is None:
        return None
    lemma, number = res
    if force_number:
        number = force_number
    forms_all = _generate(lemma)
    if not forms_all:
        return None

    gender, out = None, {}
    for f, tag in forms_all:
        if not tag.startswith("subst"):
            continue
        if (":pl:" in tag) != (number == "pl"):
            continue
        if gender is None:
            gender = _gender_of(tag)
        for c in CASES:
            if c not in out and _case_of(tag, c):
                out[c] = f
    if "nom" not in out:
        return None
    for c in CASES:
        out.setdefault(c, out["nom"])
    out["_gender"] = gender or "n"
    out["_number"] = number
    return out


def _adj_tag_profile(tag):
    """Klasa tagu + kwalifikatory za rodzajem (stopień, aspekt, negacja).

    Bez tego „dobry” rozwijało się do stopnia wyższego („lepszy”), a imiesłów
    bierny „smażony” do imiesłowu czynnego („smażący”) — oba leksemy dzielą
    lemat, różnią się dopiero ogonem tagu.
    """
    parts = tag.split(":")
    idx = None
    for i, p in enumerate(parts):
        if set(p.split(".")) & {"m1", "m2", "m3", "f", "n"}:
            idx = i
            break
    extras = tuple(parts[idx + 1:]) if idx is not None else ()
    return parts[0], extras


def _adj_forms(word, gender, number):
    """Formy przymiotnika (lub imiesłowu) uzgodnione z rzeczownikiem."""
    variants = []
    for lemma, tag in _analyse(word):
        cls, extras = _adj_tag_profile(tag)
        if cls in ADJ_TAGS and (lemma, cls, extras) not in variants:
            variants.append((lemma, cls, extras))
    if not variants:
        return None
    want_pl = number == "pl"
    target_m1 = want_pl and gender == "m1"

    for lemma, cls, extras in variants:
        exact, loose = {}, {}
        for f, tag in _generate(lemma):
            fcls, fextras = _adj_tag_profile(tag)
            if fcls != cls or fextras != extras:
                continue
            if (":pl:" in tag) != want_pl:
                continue
            gset = _gender_set(tag)
            if not gset:
                continue
            if want_pl:
                hit = ("m1" in gset) if target_m1 else bool(gset - {"m1"})
                strict = hit and (gset == {"m1"} if target_m1 else "m1" not in gset)
            else:
                hit = gender in gset
                strict = hit and len(gset) == 1
            if not hit:
                continue
            for c in CASES:
                if _case_of(tag, c):
                    if strict:
                        exact.setdefault(c, f)
                    loose.setdefault(c, f)
        out = dict(loose)
        out.update(exact)
        if out:
            for c in CASES:
                out.setdefault(c, out.get("nom", word))
            return out
    return None


def _gender_set(tag):
    for p in tag.split(":"):
        s = set(p.split("."))
        if s & {"m1", "m2", "m3", "f", "n"}:
            return s & {"m1", "m2", "m3", "f", "n"}
    return set()


# ---------------------------------------------------------------------------
# Frazy
# ---------------------------------------------------------------------------
_WORD_RE = re.compile(r"^[\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ-]+$", re.UNICODE)


def _noun_reading(word):
    """(jest rzeczownikiem, ma formę mianownika)."""
    is_noun = nom = False
    for _, tag in _analyse(word):
        if tag.startswith("subst"):
            is_noun = True
            if _case_of(tag, "nom"):
                nom = True
    return is_noun, nom


def _pick_head(core):
    """Rzeczownik główny frazy.

    Reguła składniowa, nie kolejnościowa: wyraz jest przydawką tylko wtedy,
    gdy ma czytanie przymiotnikowe **i** dalej stoi rzeczownik, z którym może
    się uzgodnić. Inaczej sam jest ośrodkiem frazy.

    Dzięki temu „starszy brat” daje `brat` (starszy uzgadnia się z m1), ale
    „umowa najmu” daje `umowa` — bo „najem” jest rodzaju męskiego i żeńska
    „umowa” nie może być jego przydawką. Reguła czysto kolejnościowa myliła
    się w obu wypadkach.
    """
    fallback = None
    for i, t in enumerate(core):
        if not _WORD_RE.match(t):
            continue
        low = t.lower()
        if low in INDECLINABLE and len(core) > 1:
            if fallback is None:
                f = _noun_forms(t)
                if f:
                    fallback = (i, f)
            continue
        f = _noun_forms(t)
        if f is None:
            continue
        if _has_reading(t, ADJ_TAGS) and low not in OVERRIDES and _modifies_later(t, core, i):
            if fallback is None:
                fallback = (i, f)
            continue
        return i, f
    return fallback if fallback else (None, None)


def _modifies_later(word, core, idx):
    """Czy `word` może być przydawką któregoś z dalszych rzeczowników."""
    for j in range(idx + 1, len(core)):
        t = core[j]
        if not _WORD_RE.match(t):
            continue
        is_noun, nom = _noun_reading(t)
        if not is_noun or not nom:
            continue
        nf = _noun_forms(t)
        if nf is None:
            continue
        af = _adj_forms(word, nf["_gender"], nf["_number"])
        if af and af.get("nom", "").lower() == word.lower():
            return True
    return False


def _phrase_forms(phrase):
    """Odmiana frazy rzeczownikowej. Ogon od przyimka zostaje bez zmian."""
    phrase = phrase.strip()
    if not phrase:
        return None

    paren = ""
    m = re.search(r"\s*(\([^)]*\))\s*$", phrase)
    if m:
        paren = " " + m.group(1)
        phrase = phrase[: m.start()].strip()

    tokens = phrase.split()
    cut = len(tokens)
    for i, t in enumerate(tokens):
        if i > 0 and t.lower() in PREPS:
            cut = i
            break
    core, tail = tokens[:cut], tokens[cut:]
    tail_str = (" " + " ".join(tail)) if tail else ""

    head_i, head_forms = _pick_head(core)
    if head_forms is None:
        return None

    gender = head_forms["_gender"]
    number = head_forms["_number"]

    slots = []
    for i, t in enumerate(core):
        if i == head_i:
            slots.append(("noun", head_forms))
            continue
        af = _adj_forms(t, gender, number) if _WORD_RE.match(t) else None
        slots.append(("adj", af) if af else ("fixed", t))

    out = {}
    for c in CASES:
        parts = []
        for i, (kind, val) in enumerate(slots):
            w = val if kind == "fixed" else val[c]
            # Morfeusz zwraca formy małą literą — nazwy własne muszą zachować wielką
            if core[i][:1].isupper() and w[:1].islower():
                w = w[:1].upper() + w[1:]
            parts.append(w)
        out[c] = " ".join(parts) + tail_str + paren
    out["_gender"] = gender
    out["_number"] = number
    return out


def forms(phrase):
    """Formy frazy — z cache'u albo z Morfeusza. None, gdy nie da się odmienić."""
    key = phrase.strip()
    if key in _CACHE:
        return _CACHE[key]

    if "/" in key:
        parts = [p.strip() for p in key.split("/")]
        subs = [forms(p) for p in parts]
        if any(s is None for s in subs):
            _CACHE[key] = None
            return None
        out = {c: " / ".join(s[c] for s in subs) for c in CASES}
        out["_gender"] = subs[0]["_gender"]
        out["_number"] = subs[0]["_number"]
        _CACHE[key] = out
        return out

    if _MORF is None:
        return None

    out = _phrase_forms(key)
    _CACHE[key] = out
    return out


def inflect(phrase, case):
    """Fraza w zadanym przypadku. Gdy odmiana nieznana — fraza bez zmian."""
    f = forms(phrase)
    return phrase if f is None else f.get(case, phrase)


def gender_of(phrase):
    f = forms(phrase)
    return f["_gender"] if f else "n"


def number_of(phrase):
    f = forms(phrase)
    return f["_number"] if f else "sg"


# ---------------------------------------------------------------------------
# Uzgodnienie czasu przeszłego i zaimków
# ---------------------------------------------------------------------------
def past(stem, phrase):
    """„przypad” + rodzaj hasła -> przypadł / przypadła / przypadło / przypadły.

    `stem` podajemy bez końcówki rodzajowej.
    """
    g, n = gender_of(phrase), number_of(phrase)
    if n == "pl":
        return stem + ("li" if g == "m1" else "ły")
    if g == "f":
        return stem + "ła"
    if g in ("n", "n1", "n2"):
        return stem + "ło"
    return stem + "ł"


def adj_agree(base_m, phrase):
    """„dobry” -> dobra / dobre / dobrzy — uzgodnienie z hasłem."""
    g, n = gender_of(phrase), number_of(phrase)
    if _MORF is not None:
        af = _adj_forms(base_m, "m1" if (n == "pl" and g == "m1") else g, n)
        if af:
            return af["nom"]
    # rezerwa bez Morfeusza
    stem = base_m[:-1] if base_m.endswith(("y", "i")) else base_m
    if n == "pl":
        return stem + "e"
    if g == "f":
        return stem + "a"
    if g.startswith("n"):
        return stem + "e"
    return base_m


def demonstrative(phrase):
    """ten / ta / to / ci / te — uzgodnione z hasłem."""
    g, n = gender_of(phrase), number_of(phrase)
    if n == "pl":
        return "ci" if g == "m1" else "te"
    if g == "f":
        return "ta"
    if g.startswith("n"):
        return "to"
    return "ten"


def demonstrative_case(phrase, case):
    g, n = gender_of(phrase), number_of(phrase)
    table_sg = {
        "m": {"nom": "ten", "gen": "tego", "dat": "temu", "acc": "ten", "inst": "tym", "loc": "tym"},
        "m_anim": {"nom": "ten", "gen": "tego", "dat": "temu", "acc": "tego", "inst": "tym", "loc": "tym"},
        "f": {"nom": "ta", "gen": "tej", "dat": "tej", "acc": "tę", "inst": "tą", "loc": "tej"},
        "n": {"nom": "to", "gen": "tego", "dat": "temu", "acc": "to", "inst": "tym", "loc": "tym"},
    }
    table_pl = {
        "m1": {"nom": "ci", "gen": "tych", "dat": "tym", "acc": "tych", "inst": "tymi", "loc": "tych"},
        "other": {"nom": "te", "gen": "tych", "dat": "tym", "acc": "te", "inst": "tymi", "loc": "tych"},
    }
    if n == "pl":
        return table_pl["m1" if g == "m1" else "other"][case]
    if g == "f":
        return table_sg["f"][case]
    if g.startswith("n"):
        return table_sg["n"][case]
    if g in ("m1", "m2"):
        return table_sg["m_anim"][case]
    return table_sg["m"][case]


# ---------------------------------------------------------------------------
# Liczebniki
# ---------------------------------------------------------------------------
_UNITS = {
    0: "zero", 1: "jeden", 2: "dwa", 3: "trzy", 4: "cztery", 5: "pięć",
    6: "sześć", 7: "siedem", 8: "osiem", 9: "dziewięć", 10: "dziesięć",
    11: "jedenaście", 12: "dwanaście", 13: "trzynaście", 14: "czternaście",
    15: "piętnaście", 16: "szesnaście", 17: "siedemnaście", 18: "osiemnaście",
    19: "dziewiętnaście",
}
_TENS = {
    20: "dwadzieścia", 30: "trzydzieści", 40: "czterdzieści", 50: "pięćdziesiąt",
    60: "sześćdziesiąt", 70: "siedemdziesiąt", 80: "osiemdziesiąt", 90: "dziewięćdziesiąt",
}
_HUNDREDS = {
    100: "sto", 200: "dwieście", 300: "trzysta", 400: "czterysta", 500: "pięćset",
    600: "sześćset", 700: "siedemset", 800: "osiemset", 900: "dziewięćset",
}

# forma żeńska liczebnika (dwie osoby, jedna sztuka)
_FEM = {1: "jedna", 2: "dwie"}
_NEU = {1: "jedno", 2: "dwa"}


def numeral(n, gender="m"):
    """Liczebnik główny słownie. `gender` wpływa tylko na 1 i 2."""
    if n in (1, 2):
        if gender == "f":
            return _FEM[n]
        if gender.startswith("n"):
            return _NEU[n]
        return _UNITS[n]
    if n > 20 and n % 10 in (1, 2) and n % 100 not in (11, 12):
        # w liczebnikach złożonych rodzaj widać na ostatnim składniku
        rest = n % 10
        base = n - rest
        # w liczebnikach złożonych „jeden” jest nieodmienne: dwadzieścia jeden osób
        tail = "jeden" if rest == 1 else numeral(rest, gender)
        return numeral(base, gender) + " " + tail
    if n in _UNITS:
        return _UNITS[n]
    if n in _TENS:
        return _TENS[n]
    if n in _HUNDREDS:
        return _HUNDREDS[n]
    if n == 1000:
        return "tysiąc"
    if n == 10000:
        return "dziesięć tysięcy"
    if n == 1000000:
        return "milion"
    if n < 100:
        t = (n // 10) * 10
        return _TENS[t] + " " + _UNITS[n % 10]
    if n < 1000:
        h = (n // 100) * 100
        rest = n % 100
        return _HUNDREDS[h] + (" " + numeral(rest, gender) if rest else "")
    return str(n)


def count_form(n):
    """Który przypadek rzeczownika po liczebniku: 'nom_sg', 'nom_pl', 'gen_pl'."""
    if n == 1:
        return "nom_sg"
    last2 = n % 100
    last = n % 10
    if 2 <= last <= 4 and not (12 <= last2 <= 14):
        return "nom_pl"
    return "gen_pl"


def counted(n, lemma_sg):
    """„3 + baht” -> „trzy bahty”; „5 + osoba” -> „pięć osób”; „1 + baht” -> „jeden baht”."""
    f = forms(lemma_sg)
    gender = f["_gender"] if f else _guess_gender(lemma_sg)
    num = numeral(n, gender)
    kind = count_form(n)
    if f is None:
        return "%s %s" % (num, lemma_sg)
    if kind == "nom_sg":
        noun = f["nom"]
    elif kind == "nom_pl":
        noun = _plural(lemma_sg, "nom")
    else:
        noun = _plural(lemma_sg, "gen")
    return "%s %s" % (num, noun)


def _plural(lemma_sg, case):
    """Forma liczby mnogiej hasła podanego w liczbie pojedynczej."""
    key = "PL:" + lemma_sg
    if key in _CACHE:
        cached = _CACHE[key]
        return cached.get(case, lemma_sg) if cached else lemma_sg
    low = lemma_sg.lower()
    if low in OVERRIDES or low in INDECLINABLE:
        return lemma_sg
    if _MORF is None:
        return lemma_sg
    pf = _noun_forms(lemma_sg, force_number="pl")
    if not pf:
        _CACHE[key] = None
        return lemma_sg
    out = {c: pf[c] for c in CASES}
    _CACHE[key] = out
    return out.get(case, lemma_sg)


# ---------------------------------------------------------------------------
# Rozpoznawanie bezokolicznika
# ---------------------------------------------------------------------------
_INF_END = ("ć", "c")


def is_infinitive(phrase):
    """Czy fraza jest bezokolicznikiem („uczyć się”, „robić zdjęcia”)."""
    first = phrase.strip().split()[0] if phrase.strip() else ""
    if not first.endswith(_INF_END):
        return False
    if _MORF is None:
        return True
    return _has_reading(first, ("inf",))


def past_1sg(phrase):
    """Bezokolicznik -> 1. os. lp. rodzaju męskiego: „jeść” -> „jadłem”.

    Potrzebne przy wzorcach `láew` i `yang mâi dâai`, które po polsku wymagają
    czasu przeszłego, a nie bezokolicznika („Już jadłem”, a nie „Już jeść”).
    Warianty rozdzielone ukośnikiem odmieniane są osobno.
    """
    phrase = phrase.strip()
    if "/" in phrase:
        return " / ".join(past_1sg(p.strip()) for p in phrase.split("/"))
    tokens = phrase.split()
    if not tokens:
        return phrase
    head = tokens[0]
    key = "PAST1SG:" + head
    if key in _CACHE:
        form = _CACHE[key]
    elif _MORF is None:
        form = None
    else:
        form = None
        for f, tag in _generate(head):
            if tag.startswith("praet") and ":sg:" in tag and _gender_set(tag) & {"m1", "m2", "m3"}:
                form = f + "em"
                break
        _CACHE[key] = form
    if not form:
        return phrase
    return " ".join([form] + tokens[1:])
