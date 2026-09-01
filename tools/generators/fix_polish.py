# -*- coding: utf-8 -*-
"""Usunięcie konwencji „Poproszę: woda” z pola `polish` (etap 8, sesja G).

Konwencja wstawki słownikowej w mianowniku objęła 2 959 rekordów (29 % bazy)
i 4 906 wystąpień razem z przykładami. Uczący się czytał „Poproszę: woda”
zamiast „Poproszę wodę” — czyli uczył się polskiego zdania, którego nie da się
wypowiedzieć.

Moduł zamienia każde takie wystąpienie na zdanie z poprawną odmianą. Sposób
odmiany zależy od nagłówka wzorca, dlatego każdy z nagłówków ma tu własną
regułę. Reguła mówi, w jakim przypadku ma stanąć wstawka i jak zbudować zdanie.

Nagłówki, przy których dwukropek jest poprawną polszczyzną (wprowadza cytat
albo wyliczenie: „Neutralnie: poproszę rachunek”), są wypisane w `KEEP` i
zostają nietknięte.
"""
import re

import polish_grammar as pg

# ---------------------------------------------------------------------------
# Nagłówki, przy których dwukropek jest poprawny i ma zostać
# ---------------------------------------------------------------------------
KEEP = {
    "Grzecznie",
    "Formalnie powiesz", "Neutralnie", "Potocznie",
    "Powiem tak", "Czy dobrze rozumiem", "Proponuję kompromis",
    "I jeszcze jedno", "Zwróć uwagę na jedną rzecz", "Najpierw najważniejsze",
    "A co powiesz na taki układ", "Popatrzmy na to z innej strony",
    "Jedna rzecz do poprawy", "Mamy dwa rozwiązania do wyboru",
    "Mamy dwa rozwiązania", "Upieczemy dwie pieczenie",
    "Spotkajmy się w połowie drogi", "Muszę powiedzieć wprost",
    "Liczby mówią same za siebie",
}

# ---------------------------------------------------------------------------
# Reguły: nagłówek -> (szablon dla rzeczownika, szablon dla bezokolicznika)
#
# W szablonach:
#   {nom} {gen} {dat} {acc} {inst} {loc}  — wstawka w danym przypadku
#   {v}        — bezokolicznik bez zmian
#   {past1}    — 1. os. lp. czasu przeszłego („jadłem”)
#   {jaki}     — jaki / jaka / jakie, uzgodnione ze wstawką
#   {adj:X}    — przymiotnik X uzgodniony ze wstawką (mianownik)
#   {adjacc:X} — przymiotnik X uzgodniony, w bierniku
#   {past:X}   — czasownik w czasie przeszłym uzgodniony z rodzajem wstawki
#   {p}        — znak końca zdania przepisany z oryginału
# ---------------------------------------------------------------------------
RULES = {
    # --- prośby i chęci -----------------------------------------------------
    "Poproszę": ("Poproszę {acc}{p}", None),
    "Chcę": ("Chcę {acc}{p}", "Chcę {v}{p}"),
    "Lubię": ("Lubię {acc}{p}", "Lubię {v}{p}"),
    "Bardzo lubię": ("Bardzo lubię {acc}{p}", "Bardzo lubię {v}{p}"),
    "Chcę kupić": ("Chcę kupić {acc}{p}", None),
    "Gdzie mogę kupić": ("Gdzie mogę kupić {acc}{p}", None),
    "Chcę zjeść": ("Chcę zjeść {acc}{p}", None),
    "Chcę wypić": ("Chcę wypić {acc}{p}", None),
    "Poproszę dokładkę": ("Poproszę dokładkę {gen}{p}", None),
    "Poproszę zimne": ("Poproszę {adjacc:zimny} {acc}{p}", None),
    "Poproszę bez": ("Poproszę bez {gen}{p}", None),
    "Bez dodatku": ("Bez dodatku {gen}{p}", None),
    "Nie mam": ("Nie mam {gen}{p}", None),

    # --- czasowniki modalne -------------------------------------------------
    "Muszę": (None, "Muszę {v}{p}"),
    "Nie mogę": (None, "Nie mogę {v}{p}"),
    "Czy mogę tutaj": (None, "Czy mogę tutaj {v}{p}"),
    "Czy możesz": (None, "Czy możesz {v}{p}"),
    "Jeszcze nie": (None, "Jeszcze nie {past1}{p}"),
    "Już": (None, "Już {past1}{p}"),

    # --- opinie o potrawach i miejscach ------------------------------------
    "Poleciłbyś to, co dotyczy": ("Poleciłbyś {acc}{p}", None),
    "Zdecydowanie polecam to, co dotyczy": ("Zdecydowanie polecam {acc}{p}", None),
    "Słyszałem dobre opinie o tym, co dotyczy": ("Słyszałem dobre opinie o {loc}{p}", None),
    "Czy naprawdę jest dobre to, co dotyczy": ("Czy {nom} naprawdę jest {adj:dobry}{p}", None),
    "Nie bardzo przypadło mi do gustu to, co dotyczy": ("Nie bardzo {past:przypad} mi do gustu {nom}{p}", None),
    "Przypadło ci do gustu to, co dotyczy": ("{Past:przypad} ci do gustu {nom}{p}", None),
    "Nigdy jeszcze nie próbowałem tego, co dotyczy": ("Nigdy jeszcze nie próbowałem {gen}{p}", None),
    "Próbowałeś kiedyś tego, co dotyczy": ("Próbowałeś kiedyś {gen}{p}", None),
    "Ciekaw jestem, jakie jest to, co dotyczy": ("Ciekaw jestem, {jaki} jest {nom}{p}", None),
    "Jakie jest to, co dotyczy": ("{Jaki} jest {nom}{p}", None),

    # --- miejsca ------------------------------------------------------------
    "Trafiłem przypadkiem na to, co dotyczy": ("Trafiłem przypadkiem na {acc}{p}", None),
    "Gdzie trafiłeś na to, co dotyczy": ("Gdzie trafiłeś na {acc}{p}", None),
    "Pojechałem tam specjalnie dla tego, co dotyczy": ("Pojechałem tam specjalnie dla {gen}{p}", None),
    "Pojechałeś tam wyłącznie dla tego, co dotyczy": ("Pojechałeś tam wyłącznie dla {gen}{p}", None),
    "Podobno warto zobaczyć to, co dotyczy": ("Podobno warto zobaczyć {acc}{p}", None),
    "Kto mówi, że warto zobaczyć": ("Kto mówi, że warto zobaczyć {acc}{p}", None),
    "Koniecznie chcę dotrzeć tam, gdzie jest": ("Koniecznie chcę dotrzeć do {gen}{p}", None),
    "Kiedy chcesz dotrzeć tam, gdzie jest": ("Kiedy chcesz dotrzeć do {gen}{p}", None),
    "Jak dojechać": ("Jak dojechać do {gen}{p}", None),
    "Jadę do": ("Jadę do {gen}{p}", None),
    "Czy daleko do": ("Czy daleko do {gen}{p}", None),
    "Spotkajmy się tu": ("Spotkajmy się przy {loc}{p}", None),

    # --- usterki i sprawy do załatwienia -----------------------------------
    "Mam problem z tym, co dotyczy": ("Mam problem z {inst}{p}", None),
    "Jak rozwiązać sprawę": ("Jak rozwiązać sprawę {gen}{p}", None),
    "Chcę zgłosić sprawę": ("Chcę zgłosić sprawę {gen}{p}", None),
    "Gdzie mogę zgłosić sprawę": ("Gdzie mogę zgłosić sprawę {gen}{p}", None),
    "Czy mógłby pan zająć się sprawą": ("Czy mógłby pan zająć się sprawą {gen}{p}", None),
    "Proszę zająć się sprawą": ("Proszę zająć się sprawą {gen}{p}", None),
    "Szkoda, że nie ma tego, co dotyczy": ("Szkoda, że nie ma {gen}{p}", None),
    "Naprawdę nie ma tu tego, co dotyczy": ("Naprawdę nie ma tu {gen}{p}", None),

    # --- pieniądze i formalności -------------------------------------------
    "To zależy od tego, co dotyczy": ("To zależy od {gen}{p}", None),
    "Chciałbym zapytać o to, co dotyczy": ("Chciałbym zapytać o {acc}{p}", None),
    "Kogo najlepiej zapytać o to, co dotyczy": ("Kogo najlepiej zapytać o {acc}{p}", None),

    # --- mieszkanie ---------------------------------------------------------
    "Jeszcze nie zdecydowałem w sprawie": ("Jeszcze nie zdecydowałem w sprawie {gen}{p}", None),
    "Zdecydowałeś już w sprawie": ("Zdecydowałeś już w sprawie {gen}{p}", None),

    # --- praca --------------------------------------------------------------
    "Kto odpowiada za to, co dotyczy": ("Kto odpowiada za {acc}{p}", None),
    "Nie odpowiadam za to, co dotyczy": ("Nie odpowiadam za {acc}{p}", None),
    "Nie wyszło zgodnie z założeniem to, co dotyczy": ("{Nom} nie {wyszedl} zgodnie z założeniem{p}", None),
    "Czy wyszło zgodnie z założeniem to, co dotyczy": ("Czy {nom} {wyszedl} zgodnie z założeniem{p}", None),
    "Jak ustaliliśmy sprawę": ("Jak ustaliliśmy sprawę {gen}{p}", None),
    "Zostajemy przy ustaleniu w sprawie": ("Zostajemy przy ustaleniu w sprawie {gen}{p}", None),
    "Chciałbym porozmawiać o tym, co dotyczy": ("Chciałbym porozmawiać o {loc}{p}", None),
    "Możemy teraz porozmawiać o tym, co dotyczy": ("Możemy teraz porozmawiać o {loc}{p}", None),
    "Muszę przygotować to, co dotyczy": ("Muszę przygotować {acc}{p}", None),
    "Czy trzeba przygotować też to, co dotyczy": ("Czy trzeba przygotować też {acc}{p}", None),

    # --- rzeczy przy sobie, braki ------------------------------------------
    "Zawsze noszę przy sobie to, co dotyczy": ("Zawsze noszę przy sobie {acc}{p}", None),
    "Nosisz przy sobie to, co dotyczy": ("Nosisz przy sobie {acc}{p}", None),
    "Brakuje mi tego, co dotyczy": ("Brakuje mi {gen}{p}", None),
    "Brakuje ci tego, co dotyczy": ("Brakuje ci {gen}{p}", None),

    # --- zdrowie ------------------------------------------------------------
    "Martwię się o to, co dotyczy": ("Martwię się o {acc}{p}", None),
    "Nie musisz się martwić o to, co dotyczy": ("Nie musisz się martwić o {acc}{p}", None),

    # --- hotel --------------------------------------------------------------
    "Chciałbym poznać szczegóły w sprawie": ("Chciałbym poznać szczegóły w sprawie {gen}{p}", None),
    "Gdzie sprawdzę szczegóły w sprawie": ("Gdzie sprawdzę szczegóły w sprawie {gen}{p}", None),
    "Zarezerwowałem z wyprzedzeniem to, co dotyczy": ("Zarezerwowałem z wyprzedzeniem {acc}{p}", None),
    "Czy trzeba rezerwować z wyprzedzeniem to, co dotyczy": ("Czy trzeba rezerwować z wyprzedzeniem {acc}{p}", None),

    # --- transport ----------------------------------------------------------
    "Pojadę": ("Pojadę {inst}{p}", None),
    "Ile kosztuje przejazd": ("Ile kosztuje przejazd {inst}{p}", None),

    # --- towarzystwo --------------------------------------------------------
    "Idę razem z kimś": ("Idę razem z {inst}{p}", None),

    # --- wzorce czasownikowe ------------------------------------------------
    "Nie mam czasu, żeby": (None, "Nie mam czasu, żeby {v}{p}"),
    "Masz czas, żeby": (None, "Masz czas, żeby {v}{p}"),
    "O mało nie zapomniałem": (None, "O mało nie zapomniałem {v}{p}"),
    "Zapomniałeś": (None, "Zapomniałeś {v}{p}"),
    "Nauczyłem się już, jak": (None, "Nauczyłem się już, jak {v}{p}"),
    "Od kogo nauczyłeś się, jak": (None, "Od kogo nauczyłeś się, jak {v}{p}"),
    "Zapomniałem, jak": (None, "Zapomniałem, jak {v}{p}"),
    "Naucz mnie, proszę, jak": (None, "Naucz mnie, proszę, jak {v}{p}"),
    "Powinienem był od razu": (None, "Powinienem był od razu {v}{p}"),
    "Czemu nie od razu": (None, "Czemu nie od razu {v}{p}"),
    "Nie ma sensu": (None, "Nie ma sensu {v}{p}"),
    "Jest sens": (None, "Czy jest sens {v}{p}"),
    "Warto by spróbować": (None, "Warto by spróbować {v}{p}"),
    "Próbowałeś już kiedyś": (None, "Próbowałeś już kiedyś {v}{p}"),
    "Wolałbym najpierw": (None, "Wolałbym najpierw {v}{p}"),
    "Może najpierw": (None, "Może najpierw {v}{p}"),
    "Coraz sprawniej mi idzie": (None, "Coraz sprawniej mi idzie {v}{p}"),
    "Idzie ci coraz sprawniej": (None, "Idzie ci coraz sprawniej {v}{p}"),
    "Umówmy się, żeby razem": (None, "Umówmy się, żeby razem {v}{p}"),
    "Na kiedy umówimy się, żeby": (None, "Na kiedy umówimy się, żeby {v}{p}"),
    "Nie chce mi się dziś": (None, "Nie chce mi się dziś {v}{p}"),
    "Nie chce ci się dziś": (None, "Nie chce ci się dziś {v}{p}"),
    "Zamierzam przestać": (None, "Zamierzam przestać {v}{p}"),
    "Kiedy zamierzasz przestać": (None, "Kiedy zamierzasz przestać {v}{p}"),
    "Zdarza mi się czasem": (None, "Zdarza mi się czasem {v}{p}"),
    "Zdarza ci się czasem": (None, "Zdarza ci się czasem {v}{p}"),
    "Przyzwyczaiłem się do tego, żeby": (None, "Przyzwyczaiłem się do tego, żeby {v}{p}"),
    "Przyzwyczaiłeś się już": (None, "Przyzwyczaiłeś się już {v}{p}"),
}

# ---------------------------------------------------------------------------
# Zaimki: wstawka nie jest rzeczownikiem, więc odmiana idzie z tabeli
# ---------------------------------------------------------------------------
PRONOUN_INST = {
    "ty": "tobą",
    "on / ona": "nim / nią",
    "my": "nami",
    "oni": "nimi",
    "ja (mężczyzna)": "mną",
    "ja (kobieta)": "mną",
}

# ---------------------------------------------------------------------------
# Okoliczniki czasu — wstawka jest przysłówkiem albo nazwą dnia,
# więc każdy wariant ma własną formę zamiast odmiany przez przypadek.
# ---------------------------------------------------------------------------
TIME_WHEN = {          # „Do zobaczenia …”, „Wrócę …”
    "dzisiaj": "dzisiaj", "jutro": "jutro", "rano": "rano",
    "po południu": "po południu", "wieczorem": "wieczorem", "w nocy": "w nocy",
    "teraz": "teraz", "później": "później", "zaraz": "zaraz",
    "poniedziałek": "w poniedziałek", "wtorek": "we wtorek", "środa": "w środę",
    "czwartek": "w czwartek", "piątek": "w piątek", "sobota": "w sobotę",
    "niedziela": "w niedzielę",
    "godzina": "za godzinę", "minuta": "za minutę", "dzień": "za dzień",
    "tydzień": "za tydzień", "miesiąc": "za miesiąc", "rok": "za rok",
}

TIME_FREE = {          # „Czy masz czas …?”
    "dzisiaj": "dzisiaj", "jutro": "jutro", "rano": "rano",
    "po południu": "po południu", "wieczorem": "wieczorem", "w nocy": "w nocy",
    "teraz": "teraz", "później": "później", "zaraz": "zaraz",
    "wczoraj": "wczoraj",
    "poniedziałek": "w poniedziałek", "wtorek": "we wtorek", "środa": "w środę",
    "czwartek": "w czwartek", "piątek": "w piątek", "sobota": "w sobotę",
    "niedziela": "w niedzielę",
}
# przy jednostkach czasu pytamy o wolną jednostkę, nie o termin
TIME_FREE_UNIT = {
    "godzina": "wolną godzinę", "minuta": "wolną minutę", "dzień": "wolny dzień",
    "tydzień": "wolny tydzień", "miesiąc": "wolny miesiąc", "rok": "wolny rok",
}

# ---------------------------------------------------------------------------
# Klasyfikator tajski -> polski rzeczownik miary („dwie butelki mleka”)
# ---------------------------------------------------------------------------
THAI_COUNTER_PL = {
    "khùat": "butelka", "kâew": "szklanka", "jaan": "talerz", "thûai": "filiżanka",
    "chín": "kawałek", "bai": "sztuka", "an": "sztuka", "tua": "sztuka",
    "lûuk": "sztuka", "hàw": "paczka", "thǔng": "torebka", "khan": "sztuka",
    "phǔen": "sztuka", "lêm": "sztuka", "phàen": "kawałek", "dàwk": "sztuka",
    "cháwn": "łyżka", "chaam": "miska", "fawng": "sztuka", "mét": "ziarnko",
    "múue": "porcja",
}

# ---------------------------------------------------------------------------
# Rekordy bez sensu — przepisywane punktowo (patrz raport sesji G)
# ---------------------------------------------------------------------------
EXACT_REWRITE = {
    # Cena / liczba osób / sztuki: 0 i 1 miały błędną odmianę i zerowy sens
    "Cena: 0 bahtów.": "Zero bahtów.",
    "Cena: 1 bahtów.": "Jeden baht.",
    "Liczba osób: 0.": "Zero osób.",
    "Sztuk: 0.": "Zero sztuk.",
    # „jà klàp mûea waan” = czas przyszły + wczoraj; sprzeczność także po tajsku
    "Wrócę: wczoraj.": "Wróciłem wczoraj.",
    "Do zobaczenia: wczoraj.": "Widzieliśmy się wczoraj.",
    # „phǒm pai kàp phǒm” — zaimek odsyła sam do siebie
    "Idę razem z kimś: ja (mężczyzna).": "Idziesz razem ze mną.",
    "Idę razem z kimś: ja (kobieta).": "Idziesz razem ze mną.",
}


# ---------------------------------------------------------------------------
# Budowanie zdania
# ---------------------------------------------------------------------------
_JAKI = {"m1": "jaki", "m2": "jaki", "m3": "jaki", "f": "jaka", "n": "jakie"}


def _cap(s):
    return s[:1].upper() + s[1:] if s else s


def render(template, tail, punct, counter=None):
    """Wypełnia szablon wstawką `tail`."""
    out = template

    def sub(pat, value):
        nonlocal out
        out = out.replace(pat, value)

    if "{v}" in out:
        sub("{v}", tail)
    if "{past1}" in out:
        sub("{past1}", pg.past_1sg(tail))

    for case in pg.CASES:
        for pat, val in (("{%s}" % case, pg.inflect(tail, case)),
                         ("{%s}" % case.capitalize(), _cap(pg.inflect(tail, case)))):
            if pat in out:
                sub(pat, val)

    if "{jaki}" in out or "{Jaki}" in out:
        w = _JAKI.get(pg.gender_of(tail), "jakie")
        if pg.number_of(tail) == "pl":
            w = "jacy" if pg.gender_of(tail) == "m1" else "jakie"
        sub("{jaki}", w)
        sub("{Jaki}", _cap(w))

    if "{wyszedl}" in out:
        g, n = pg.gender_of(tail), pg.number_of(tail)
        if n == "pl":
            form = "wyszli" if g == "m1" else "wyszły"
        elif g == "f":
            form = "wyszła"
        elif g.startswith("n"):
            form = "wyszło"
        else:
            form = "wyszedł"
        sub("{wyszedl}", form)

    m = re.search(r"\{([Pp])ast:([^}]+)\}", out)
    while m:
        form = pg.past(m.group(2), tail)
        if m.group(1) == "P":
            form = _cap(form)
        out = out[: m.start()] + form + out[m.end():]
        m = re.search(r"\{([Pp])ast:([^}]+)\}", out)

    m = re.search(r"\{adj:([^}]+)\}", out)
    while m:
        out = out[: m.start()] + pg.adj_agree(m.group(1), tail) + out[m.end():]
        m = re.search(r"\{adj:([^}]+)\}", out)

    m = re.search(r"\{adjacc:([^}]+)\}", out)
    while m:
        f = pg._adj_forms(m.group(1), pg.gender_of(tail), pg.number_of(tail))
        form = f["acc"] if f else m.group(1)
        out = out[: m.start()] + form + out[m.end():]
        m = re.search(r"\{adjacc:([^}]+)\}", out)

    out = out.replace("{p}", punct)
    return re.sub(r"\s+", " ", out).strip()


def _counter_from_thai(thai_phonetic):
    """Znajduje klasyfikator w zdaniu tajskim, żeby policzyć po polsku."""
    tokens = thai_phonetic.split()
    for i, t in enumerate(tokens):
        if t in ("sǎwng",) and i + 1 < len(tokens):
            nxt = tokens[i + 1]
            if nxt in THAI_COUNTER_PL:
                return THAI_COUNTER_PL[nxt]
    return None


def fix_text(text, thai_phonetic=""):
    """Przepisuje jedno zdanie. Zwraca (nowy_tekst, czy_zmieniono)."""
    if text in EXACT_REWRITE:
        return EXACT_REWRITE[text], True
    if ":" not in text:
        return text, False

    head, tail = text.split(":", 1)
    head = head.strip()
    tail = tail.strip()
    if head in KEEP:
        return text, False

    punct = ""
    if tail and tail[-1] in ".?!":
        punct, tail = tail[-1], tail[:-1].strip()
    if not tail:
        return text, False

    # --- wzorce liczebnikowe -------------------------------------------------
    num = re.fullmatch(r"(\d+)(?:\s+\w+)?", tail)
    if head in ("Cena", "Liczba osób", "Sztuk") and num:
        n = int(num.group(1))
        noun = {"Cena": "baht", "Liczba osób": "osoba", "Sztuk": "sztuka"}[head]
        return _cap(pg.counted(n, noun)) + (punct or "."), True

    # --- „Poproszę dwie sztuki: mleko” — liczymy właściwym pojemnikiem -------
    if head == "Poproszę dwie sztuki":
        counter = _counter_from_thai(thai_phonetic) or "sztuka"
        return ("Poproszę %s %s%s" % (pg.counted(2, counter),
                                      pg.inflect(tail, "gen"), punct or ".")), True

    # --- okoliczniki czasu ---------------------------------------------------
    if head in ("Do zobaczenia", "Wrócę"):
        when = TIME_WHEN.get(tail)
        if when:
            return "%s %s%s" % (head, when, punct or "."), True
    if head == "Czy masz czas":
        if tail in TIME_FREE_UNIT:
            return "Czy masz %s%s" % (TIME_FREE_UNIT[tail], punct or "?"), True
        when = TIME_FREE.get(tail)
        if when:
            return "Czy masz czas %s%s" % (when, punct or "?"), True

    # --- zaimki po „z” -------------------------------------------------------
    if head == "Idę razem z kimś" and tail in PRONOUN_INST:
        return "Idę razem z %s%s" % (PRONOUN_INST[tail], punct or "."), True

    rule = RULES.get(head)
    if rule is None:
        return text, False

    noun_tpl, verb_tpl = rule
    if verb_tpl and pg.is_infinitive(tail):
        return render(verb_tpl, tail, punct or "."), True
    if noun_tpl and pg.forms(tail) is not None:
        return render(noun_tpl, tail, punct or "."), True
    if verb_tpl:
        return render(verb_tpl, tail, punct or "."), True
    return text, False
