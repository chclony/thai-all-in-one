# -*- coding: utf-8 -*-
"""Liczebniki tajskie liczone regułami, nie wypisane z listy.

To jest jedyne źródło prawdy o tym, jak brzmi liczba w tym projekcie. Czytają
z niego trzy strony:

  * generator `tools/generators/numbers.py`, który buduje `data/numbers.json`,
  * walidator `tools/validate.py`, który sprawdza każdy zapisany liczebnik
    przeciw regule arytmetycznej, a nie przeciw obecności pól,
  * `js/numbers.js`, który jest odwzorowaniem tego pliku jeden do jednego —
    aplikacja musi umieć wygenerować liczbę, której w danych nie ma.

Odwzorowanie w JS nie jest kopią z lenistwa. Ćwiczenie „dyktando liczbowe”
losuje liczbę z zakresu 0–1 000 000; gdyby każda musiała mieć wpis w pliku,
plik miałby milion pozycji. Zamiast tego plik trzyma ATOMY (cyfry, pozycje,
nieregularności) i PUNKTY KONTROLNE, a resztę składa reguła — po obu stronach
ta sama.

NIEREGULARNOŚCI, których ta reguła pilnuje
------------------------------------------
1. Jedność „1” po czymkolwiek to `èt`, nie `nùeng`: 11 = sìp-èt, 21 = yîi-sìp-èt,
   101 = nùeng-ráwy-èt. Samo 1 to `nùeng`.
2. Dziesiątka „2” to `yîi-sìp`, nie `sǎwng-sìp`. Tylko dziesiątka — 200 to
   normalne `sǎwng-ráwy`.
3. Dziesiątka „1” jest niema: 10 to `sìp`, nie `nùeng-sìp`. Setka, tysiąc
   i wyżej „1” wypowiadają: 100 to `nùeng-ráwy`.
4. Powyżej miliona liczy się w milionach: 2 000 000 to `sǎwng-láan`.
5. Zero pojawia się wyłącznie samodzielnie. W środku liczby pozycja pusta jest
   pomijana, nie wymawiana: 105 to `nùeng-ráwy-hâa`, nie `…sǔun-sìp-hâa`.

Zapis: cała liczba jest JEDNYM wyrazem sklejonym dywizami, tak jak `sìp-èt`
i `yîi-sìp` leżą w bazie od pierwszej sesji. Dywiz łączy sylaby wyrazu, spacja
rozdziela wyrazy — więc `sìi-sìp-hâa bàat` to liczba i jednostka, dwa wyrazy.
"""

import re

# --- atomy ------------------------------------------------------------------

DIGITS = [
    ("sǔun", "ศูนย์"),
    ("nùeng", "หนึ่ง"),
    ("sǎwng", "สอง"),
    ("sǎam", "สาม"),
    ("sìi", "สี่"),
    ("hâa", "ห้า"),
    ("hòk", "หก"),
    ("jèt", "เจ็ด"),
    ("pàet", "แปด"),
    ("kâo", "เก้า"),
]

ET = ("èt", "เอ็ด")            # „jeden” w pozycji jedności po czymkolwiek
YII = ("yîi", "ยี่")            # „dwa” w pozycji dziesiątek

# Pozycje od najwyższej. Wartość, zapis fonetyczny, pismo dla syntezatora.
POSITIONS = [
    (100000, "sǎen", "แสน"),
    (10000, "mùen", "หมื่น"),
    (1000, "phan", "พัน"),
    (100, "ráwy", "ร้อย"),
    (10, "sìp", "สิบ"),
]

MILLION = ("láan", "ล้าน")

MAX = 1000000


class NumberError(ValueError):
    pass


def _parts_below_million(n):
    """Człony liczby 1..999 999 jako pary (fonetyka, pismo)."""
    out = []
    rest = n
    for value, ph, th in POSITIONS:
        d = rest // value
        rest -= d * value
        if d == 0:
            continue
        if value == 10:
            # Dziesiątki: 1 nieme, 2 nieregularne, reszta zwyczajnie.
            if d == 1:
                out.append((ph, th))
            elif d == 2:
                out.append((YII[0] + "-" + ph, YII[1] + th))
            else:
                out.append((DIGITS[d][0] + "-" + ph, DIGITS[d][1] + th))
        else:
            out.append((DIGITS[d][0] + "-" + ph, DIGITS[d][1] + th))
    if rest:
        # Jedność. „1” po czymkolwiek to èt, samodzielne 1 to nùeng.
        if rest == 1 and out:
            out.append(ET)
        else:
            out.append(DIGITS[rest])
    return out


def read(n):
    """Zwraca (fonetyka, pismo dla syntezatora) dla liczby całkowitej 0..1 000 000."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise NumberError("liczebnik musi być liczbą całkowitą, jest %r" % (n,))
    if n < 0 or n > MAX:
        raise NumberError("liczba %d poza zakresem modułu (0..%d)" % (n, MAX))
    if n == 0:
        return DIGITS[0]

    chunks = []
    millions = n // 1000000
    if millions:
        head = _parts_below_million(millions) if millions > 1 else [DIGITS[1]]
        chunks.extend(head)
        chunks.append(MILLION)
    chunks.extend(_parts_below_million(n % 1000000))

    ph = "-".join(c[0] for c in chunks)
    th = "".join(c[1] for c in chunks)
    return ph, th


def phonetic(n):
    return read(n)[0]


def thai(n):
    return read(n)[1]


# --- droga powrotna ---------------------------------------------------------
#
# Sama generacja niczego nie dowodzi: reguła może być wewnętrznie spójna
# i konsekwentnie błędna. Dlatego obok czytania stoi rozbiór — niezależny kod,
# który z zapisu fonetycznego odtwarza wartość. Walidator i test działania
# sprawdzają, że parse(read(n)) == n dla całego zakresu. Błąd, który przeżyje
# obie strony, musiałby być popełniony dwa razy w przeciwnych kierunkach.

_UNIT_BY_PHON = {ph: i for i, (ph, _) in enumerate(DIGITS)}
_POS_BY_PHON = {ph: value for value, ph, _ in POSITIONS}


def parse(text):
    """Z zapisu fonetycznego z powrotem na liczbę. None, gdy to nie liczebnik."""
    if not text:
        return None
    syls = [s for s in re.split(r"[\s\-]+", text.strip()) if s]
    if not syls:
        return None

    total = 0          # zamknięte miliony
    group = 0          # bieżąca grupa poniżej miliona
    pending = None     # cyfra czekająca na swoją pozycję
    seen = False

    for syl in syls:
        if syl == MILLION[0]:
            if pending is not None:
                group += pending
                pending = None
            if group == 0:
                return None            # „láan” bez mnożnika
            total += group * 1000000
            group = 0
            seen = True
            continue
        if syl == YII[0]:
            if pending is not None:
                return None
            pending = 2
            seen = True
            continue
        if syl == ET[0]:
            if pending is not None:
                return None
            group += 1
            seen = True
            continue
        if syl in _POS_BY_PHON:
            value = _POS_BY_PHON[syl]
            d = 1 if pending is None else pending
            if value != 10 and pending is None:
                return None            # setka i wyżej wymagają mnożnika
            group += d * value
            pending = None
            seen = True
            continue
        if syl in _UNIT_BY_PHON:
            if pending is not None:
                return None
            pending = _UNIT_BY_PHON[syl]
            seen = True
            continue
        return None                     # wyraz spoza systemu liczbowego

    if pending is not None:
        group += pending
    if not seen:
        return None
    return total + group


# --- opis nieregularności ---------------------------------------------------

def irregular_kinds(n):
    """Które nieregularności widać w zapisie liczby n. Lista identyfikatorów."""
    kinds = []
    if n == 0:
        return kinds
    body = n % 1000000
    if body % 10 == 1 and body > 10:
        kinds.append("et")
    if 10 <= body % 100 < 20 and body % 100 != 10:
        kinds.append("teens")
    if (body // 10) % 10 == 2:
        kinds.append("yii")
    if 10 <= body < 100 or (body % 100) // 10 == 1:
        if (body % 100) // 10 == 1:
            kinds.append("silent-one")
    if n >= 1000000:
        kinds.append("million")
    if "0" in str(body)[1:] and body >= 100:
        kinds.append("skip-zero")
    return sorted(set(kinds))


IRREGULAR_LABELS = {
    "et": "jedność „1” po czymkolwiek brzmi èt, nie nùeng",
    "teens": "jedenaście–dziewiętnaście: dziesiątka niema, jedność przez èt",
    "yii": "dziesiątka „2” to yîi-sìp, nigdy sǎwng-sìp",
    "silent-one": "dziesiątka „1” jest niema: sìp, nie nùeng-sìp",
    "million": "powyżej miliona liczy się w milionach",
    "skip-zero": "pozycja pusta jest pomijana, nie wymawiana jako sǔun",
}
