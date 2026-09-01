#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator trzech nowych trybów gramatycznych.

  data/grammar-listening.json  — wykrywanie struktury ze słuchu
  data/grammar-transform.json  — przekształcanie zdań
  data/particles.json          — partykuły końcowe

WYKRYWANIE STRUKTURY (zadanie 2)
================================

Uczący się słyszy zdanie i mówi, CZYM ono jest, a nie co znaczy. Trzy osie:

  intencja  — stwierdzenie / pytanie / prośba / rozkaz / przeczenie
  czas      — przeszłość / teraźniejszość / przyszłość / nieokreślony
  rejestr   — grzeczny / neutralny

To umiejętność osobna od słownikowej i ważniejsza przy niepełnym słownictwie.
Kto usłyszy `mǎi` na końcu, wie, że ma odpowiedzieć — choćby nie zrozumiał
ani jednego wyrazu przed nim. Kto nie usłyszy, będzie milczał i wyjdzie na
niegrzecznego.

Klasyfikacja idzie po markerach, których pozycja w tajskim jest sztywna.
Zdania niejednoznaczne SĄ ODRZUCANE — ćwiczenie z dwiema poprawnymi
odpowiedziami uczy nieufności do ćwiczenia, nie do języka.

TRANSFORMACJE (zadanie 3)
=========================

Dane zdanie plus polecenie („na pytanie", „na przeczenie", „na formę
grzeczną", „na czas przeszły"). Ocena idzie PO STRUKTURZE: liczy się, czy
wymagany marker stanął we właściwym miejscu i czy trzon zdania ocalał.
Dlatego każdy element niesie `check` — opis reguły, nie gotową odpowiedź.

Wzorcowa odpowiedź jest w danych, ale służy do POKAZANIA po ocenie, nie do
porównywania znak w znak. Gdyby ocena szła przez równość łańcuchów,
odrzucałaby odpowiedzi poprawne, a tylko inaczej sformułowane — a to najszybszy
sposób, żeby uczący się przestał ufać ocenie.

PARTYKUŁY (zadanie 4)
=====================

Opis każdej partykuły plus ćwiczenie: to samo zdanie, cztery partykuły,
jedna sytuacja. Wybór jest sytuacyjny, bo partykuły nie mają odpowiedników
słownikowych — mają warunki użycia.
"""

import json
import os
import re
import sys
from collections import OrderedDict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import grammar_progression as GP     # noqa: E402
import jsonio                        # noqa: E402

DATA = GP.DATA

W = r'(?:^|[ ])'
E = r'(?:$|[ ])'


def has(text, word):
    return re.search(W + re.escape(word) + E, text) is not None


def ends_with(text, word):
    """Zakończenie na CAŁYM wyrazie, nie na zbiegu liter.

    Bez granicy wyrazu `sà-mǎi` (modny) kończy się na `mǎi` i całe zdanie
    zostaje uznane za pytanie. Dywiz łączy sylaby jednego wyrazu, więc musi
    się liczyć jako część wyrazu, nie jako granica.
    """
    return re.search(r'(?:^|[ ])' + re.escape(word) + r'$',
                     text.strip()) is not None


# --------------------------------------------------------------------------
# OŚ 1 — INTENCJA
# --------------------------------------------------------------------------
QUESTION_WORDS = ['à-rai', 'thîi nǎi', 'mûea-rài', 'mûea rài', 'khrai',
                  'yang-ngai', 'yang ngai', 'thâo-rài', 'thâo rài', 'kìi',
                  'nǎi', 'tham-mai', 'tham mai']
POLITE = ['khráp', 'khâ', 'khá']
ASPECT_MARKERS = ['láew', 'jà', 'kamlang', 'khoei', 'yang', 'yùu', 'dâai']
# Partykuły końcowe modyfikujące wydźwięk. Zdanie, które już je ma, nie
# nadaje się na źródło transformacji: cząstka dokładana „na koniec" stanęłaby
# ZA nimi, a kolejność partykuł w tajskim jest sztywna i `ná láew khráp`
# jest po prostu niepoprawne.
FINAL_PARTICLES = ['ná', 'nòi', 'dûai', 'sì', 'sí', 'loei', 'lâ', 'là', 'ròk']
MODALS = ['tâwng', 'yàak', 'khuan', 'àat', 'khong', 'dâai', 'chûai', 'khǎw']


def junk(text):
    """Rekordy z powtórzonym czasownikiem („phǒm tâwng tâwng" — „muszę
    musieć") są artefaktem generatora zdań, nie materiałem. Na wzorzec
    gramatyczny się nie nadają, bo ilustrują usterkę, nie konstrukcję."""
    toks = text.split()
    return any(a == b for a, b in zip(toks, toks[1:]))


def strip_polite(text):
    out = text.strip()
    for p in POLITE:
        out = re.sub(re.escape(p) + r'$', '', out).strip()
    return out


def intent_of(text):
    """Intencja wypowiedzi albo None, gdy sygnały się nakładają.

    Kolejność testów nie jest dowolna: prośba bije pytanie, bo `chûai … dâai
    mǎi` ma `mǎi` na końcu i formalnie jest pytaniem — ale odpowiedzią na nie
    jest czynność, nie informacja. Uczący się, który usłyszy tam „pytanie",
    odpowie „tak" i nic nie zrobi.
    """
    core = strip_polite(text)
    if not core:
        return None

    # `khǎw-thôot` to utrwalone „przepraszam", nie prośba o rzecz — mimo
    # że zaczyna się od tego samego `khǎw`.
    apology = re.search(r'^kh[ǎa]w[ -]?thôot', core) is not None
    request = (not apology) and (has(core, 'chûai') or has(core, 'khǎw')
                                 or ends_with(core, 'nòi'))
    question = (ends_with(core, 'mǎi') or ends_with(core, 'rǔe yang')
                or ends_with(core, 'rǔe plào') or ends_with(core, 'châi mǎi')
                or any(has(core, q) for q in QUESTION_WORDS))
    negation = has(core, 'mâi') or has(core, 'yàa')

    if request:
        return 'prosba'
    if question:
        return 'pytanie'
    if negation:
        return 'przeczenie'
    # Rozkaz: goły czasownik na początku, bez podmiotu, bez cząstki
    # aspektowej i krótko. `ao láew` to nie „bierz!", tylko „już wziąłem" —
    # sam czasownik na początku nie wystarcza, musi NIE być tam nic innego.
    if (re.match(r'^(nâng|duu|fang|maa|pai|kin|ao|dùem|phûut|yùt|raw|khâo|klàp)'
                 + E, core)
            and len(core.split()) <= 3
            and not any(has(core, m) for m in ASPECT_MARKERS)):
        return 'rozkaz'
    return 'stwierdzenie'


INTENT_LABEL = OrderedDict([
    ('stwierdzenie', 'Stwierdzenie'),
    ('pytanie', 'Pytanie'),
    ('prosba', 'Prośba'),
    ('rozkaz', 'Polecenie'),
    ('przeczenie', 'Przeczenie'),
])

INTENT_WHY = {
    'pytanie': 'Na końcu stoi cząstka pytajna albo w środku słowo pytające. '
               'To jedyny sygnał — melodia zdania niczego tu nie zdradza, '
               'bo jest zajęta przez tony.',
    'prosba': 'Konstrukcja prośby: `chûai`, `khǎw` albo zmiękczające `nòi`. '
              'Cząstka pytajna na końcu nie robi z tego pytania o informację '
              '— odpowiedzią ma być czynność.',
    'rozkaz': 'Goły czasownik na początku, bez podmiotu i bez cząstki '
              'łagodzącej. Tajski nie ma osobnej formy rozkaźnika, więc '
              'poleceniem jest właśnie brak wszystkiego innego.',
    'przeczenie': '`mâi` stoi bezpośrednio przed czasownikiem. Zawsze tam '
                  'i tylko tam.',
    'stwierdzenie': 'Brak cząstki pytajnej, brak konstrukcji prośby, brak '
                    '`mâi`. Zdanie po prostu opisuje stan rzeczy.',
}


# --------------------------------------------------------------------------
# OŚ 2 — CZAS
# --------------------------------------------------------------------------
PAST_WORDS = ['mûea waan', 'mûea kîi', 'mûea cháo', 'mûea-waan']
FUTURE_WORDS = ['phrûng-níi', 'phrûng níi', 'dǐao']


def time_of(text):
    core = strip_polite(text)
    past = ends_with(core, 'láew') or any(has(core, w) for w in PAST_WORDS) \
        or has(core, 'khoei')
    future = has(core, 'jà') or any(has(core, w) for w in FUTURE_WORDS)
    now = has(core, 'kamlang') or has(core, 'tawn níi')
    hits = [x for x in (past, future, now) if x]
    if len(hits) != 1:
        return None
    if past:
        return 'przeszlosc'
    if future:
        return 'przyszlosc'
    return 'terazniejszosc'


TIME_LABEL = OrderedDict([
    ('przeszlosc', 'Przeszłość'),
    ('terazniejszosc', 'Teraz'),
    ('przyszlosc', 'Przyszłość'),
    ('nieokreslony', 'Bez oznaczenia czasu'),
])

TIME_WHY = {
    'przeszlosc': '`láew` na końcu albo okolicznik przeszłości. Czasownik '
                  'wygląda identycznie jak w każdym innym czasie — jedyna '
                  'informacja leży w cząstce.',
    'przyszlosc': '`jà` przed czasownikiem albo okolicznik przyszłości. '
                  '`jà` niesie przy tym zamiar, nie samą przyszłość.',
    'terazniejszosc': '`kamlang` albo `tawn níi`. Bez nich zdanie o czasie '
                      'teraźniejszym w ogóle by go nie oznaczało.',
    'nieokreslony': 'Żadnej cząstki czasu. Czas trzeba wziąć z tego, co padło '
                    'wcześniej w rozmowie — i tak działa większość zdań.',
}


# --------------------------------------------------------------------------
def build_listening(corpus, pool, topics):
    """Zadania: posłuchaj i wskaż konstrukcję.

    Materiał: te same zdania, którymi kurs ilustruje gramatykę, plus szerszy
    zasób z bazy. Każde zadanie zna lekcję, od której jest wyrażalne, więc
    tryb da się ograniczyć do materiału już przerobionego.
    """
    items = []
    seen = set()
    for p in pool:
        ph = p['thaiPhonetic']
        if not ph or ph in seen:
            continue
        if not p['polish']:
            continue
        syls = corpus.syllables(ph)
        if not (3 <= len(syls) <= 10) or junk(ph):
            continue
        av = corpus.available_from(ph)
        if av is None:
            continue
        intent = intent_of(ph)
        if intent is None:
            continue
        tm = time_of(ph)
        seen.add(ph)
        core = strip_polite(ph)
        polite = core != ph.strip()
        items.append(OrderedDict([
            ('id', 'gl-%05d' % (len(items) + 1)),
            ('sourceId', p['_src']),
            ('polish', p['polish']),
            ('thaiPhonetic', ph),
            ('pronunciationPolish', p.get('pronunciationPolish', '')),
            ('ttsThai', p.get('ttsThai', '')),
            ('availableFrom', av),
            ('intent', intent),
            ('time', tm or 'nieokreslony'),
            ('polite', polite),
        ]))
    return items


LISTEN_CAP = 1800
TRANSFORM_CAP = 1800


def balance(items, key, cap):
    """Próbka reprezentatywna zamiast wszystkiego, co da się wygenerować.

    Pełny przemiał bazy daje kilkanaście tysięcy zadań i dziesięć megabajtów
    pliku. Wartość ćwiczenia nie rośnie po tysiącu pozycji — nikt ich nie
    zrobi — a plik dociągany na żądanie rośnie liniowo i psuje start.

    Próbkujemy więc równomiernie w DWÓCH wymiarach naraz: po kategorii
    (żeby rzadka intencja nie zniknęła pod częstą) i po dostępności (żeby
    uczący się po dziesiątej lekcji miał z czego ćwiczyć, a nie dostał
    materiału wyłącznie z końca kursu).
    """
    groups = {}
    for it in items:
        groups.setdefault(it[key], []).append(it)
    quota = max(1, cap // max(1, len(groups)))
    out = []
    for k in sorted(groups):
        g = sorted(groups[k], key=lambda x: (x['availableFrom'], x['id']))
        if len(g) <= quota:
            out.extend(g)
            continue
        stride = len(g) / float(quota)
        out.extend(g[int(i * stride)] for i in range(quota))
    out.sort(key=lambda x: (x['availableFrom'], x['id']))
    for i, it in enumerate(out, 1):
        it['id'] = '%s%05d' % (it['id'][:3], i)
    return out


# --------------------------------------------------------------------------
# TRANSFORMACJE
# --------------------------------------------------------------------------
TRANSFORMS = [
    OrderedDict([
        ('id', 'question'),
        ('title', 'Zamień na pytanie'),
        ('instruction', 'Zamień to zdanie w pytanie, na które da się '
                        'odpowiedzieć „tak” albo „nie”.'),
        ('rule', 'Dołóż `mǎi` na samym końcu, przed cząstką grzecznościową. '
                 'Nic więcej się nie zmienia — ani szyk, ani czasownik.'),
        ('marker', 'mǎi'),
        ('position', 'koniec'),
    ]),
    OrderedDict([
        ('id', 'negation'),
        ('title', 'Zamień na przeczenie'),
        ('instruction', 'Zaprzecz temu zdaniu.'),
        ('rule', 'Wstaw `mâi` bezpośrednio przed czasownikiem. Nie na '
                 'początku zdania i nie na końcu — tylko tam.'),
        ('marker', 'mâi'),
        ('position', 'przed czasownikiem'),
    ]),
    OrderedDict([
        ('id', 'polite'),
        ('title', 'Zamień na formę grzeczną'),
        ('instruction', 'Powiedz to samo do osoby, której nie znasz.'),
        ('rule', 'Dołóż cząstkę grzecznościową na samym końcu: `khráp` '
                 '(mężczyzna) albo `khâ` (kobieta). Reszta zdania bez zmian.'),
        ('marker', 'khráp'),
        ('position', 'koniec'),
    ]),
    OrderedDict([
        ('id', 'past'),
        ('title', 'Zamień na czas przeszły'),
        ('instruction', 'Powiedz, że to już się stało.'),
        ('rule', 'Dołóż `láew` na końcu wypowiedzi. Czasownik zostaje '
                 'nietknięty — nie ma czego odmieniać.'),
        ('marker', 'láew'),
        ('position', 'koniec'),
    ]),
    OrderedDict([
        ('id', 'future'),
        ('title', 'Zamień na czas przyszły'),
        ('instruction', 'Powiedz, że masz zamiar to zrobić.'),
        ('rule', 'Wstaw `jà` bezpośrednio przed czasownikiem.'),
        ('marker', 'jà'),
        ('position', 'przed czasownikiem'),
    ]),
    OrderedDict([
        ('id', 'request'),
        ('title', 'Zamień na grzeczną prośbę'),
        ('instruction', 'Poproś o to zamiast tego żądać.'),
        ('rule', 'Dołóż `nòi` przed cząstką grzecznościową. `nòi` nie znaczy '
                 'tu „trochę” — zmniejsza ciężar prośby.'),
        ('marker', 'nòi'),
        ('position', 'koniec'),
    ]),
]

VERBS = ['pai', 'maa', 'kin', 'ao', 'duu', 'tham', 'séu', 'súe', 'yàak',
         'dùem', 'phûut', 'rian', 'nawn', 'klàp', 'khâo', 'àwk', 'hǎa',
         'sòng', 'chái', 'nâng', 'fang', 'rúu', 'khít', 'mii', 'yùu']


def first_verb(text):
    toks = text.split()
    for i, t in enumerate(toks):
        if t in VERBS:
            return i, t
    return None, None


def build_transforms(corpus, pool):
    """Elementy do przekształceń.

    Bierzemy wyłącznie zdania proste, twierdzące, bez cząstek, które
    polecenie miałoby dokładać — inaczej „zamień na przeczenie” dostawałoby
    zdanie już zaprzeczone.
    """
    items = []
    seen = set()
    for p in pool:
        ph = p['thaiPhonetic']
        if not ph or ph in seen or not p['polish']:
            continue
        core = strip_polite(ph)
        syls = corpus.syllables(ph)
        if not (3 <= len(syls) <= 8) or junk(ph):
            continue
        av = corpus.available_from(ph)
        if av is None:
            continue
        if intent_of(ph) != 'stwierdzenie':
            continue
        if any(ends_with(core, fp) for fp in FINAL_PARTICLES):
            continue
        # Cząstka grzecznościowa w ŚRODKU wypowiedzi znaczy, że rekord skleja
        # dwie wypowiedzi („Rozumiem, dziękuję"). Doklejanie czegokolwiek na
        # koniec takiego zlepka trafia w niewłaściwe zdanie.
        if any(has(core, pp) for pp in POLITE):
            continue
        vi, verb = first_verb(core)
        if verb is None:
            continue
        seen.add(ph)
        for t in TRANSFORMS:
            if has(core, t['marker']):
                continue          # już tam jest, nie ma czego ćwiczyć
            if t['id'] == 'polite' and core != ph.strip():
                continue
            # „Zamień na grzeczną prośbę" ma sens tylko wtedy, gdy zdanie
            # jest poleceniem — czyli zaczyna się od czasownika. Doklejenie
            # `nòi` do „Słyszałem dobre opinie" nie tworzy prośby, tylko
            # zdanie bez sensu.
            if t['id'] == 'request' and (vi != 0
                                         or any(has(core, m)
                                                for m in ASPECT_MARKERS)):
                continue
            # Przeczenie i czas przyszły wstawiają cząstkę PRZED czasownik.
            # Przy czasowniku modalnym („muszę brać") nie wiadomo, przed
            # który — `mâi tâwng ao` i `tâwng mâi ao` znaczą co innego,
            # a polecenie po polsku tego nie rozstrzyga. Takie zdania
            # odpadają, zamiast dawać zadanie z dwiema dobrymi odpowiedziami.
            if t['id'] in ('negation', 'future'):
                if vi > 1:
                    continue
                if any(has(core, m) for m in MODALS):
                    continue
            model = expected(core, ph, t, vi)
            if not model:
                continue
            items.append(OrderedDict([
                ('id', 'gt-%05d' % (len(items) + 1)),
                ('sourceId', p['_src']),
                ('transform', t['id']),
                ('polish', p['polish']),
                ('thaiPhonetic', ph),
                ('pronunciationPolish', p.get('pronunciationPolish', '')),
                ('ttsThai', p.get('ttsThai', '')),
                ('availableFrom', av),
                ('model', model),
                ('check', OrderedDict([
                    ('marker', t['marker']),
                    ('alternatives', ['khâ', 'khá'] if t['id'] == 'polite'
                     else []),
                    ('position', t['position']),
                    ('after', core.split()[vi - 1] if vi else ''),
                    ('before', core.split()[vi] if vi is not None else ''),
                    ('keep', [s for s in core.split()
                              if s not in POLITE][:8]),
                ])),
            ]))
    return items


def expected(core, full, t, vi):
    """Wzorcowa odpowiedź. Do POKAZANIA po ocenie, nie do porównywania."""
    toks = core.split()
    tail = full.strip()[len(core):].strip()
    if t['position'] == 'koniec':
        out = toks + [t['marker']]
        if tail:
            out += tail.split()
        return ' '.join(out)
    out = toks[:vi] + [t['marker']] + toks[vi:]
    if tail:
        out += tail.split()
    return ' '.join(out)


# --------------------------------------------------------------------------
# PARTYKUŁY KOŃCOWE
# --------------------------------------------------------------------------
PARTICLES = [
    OrderedDict([
        ('id', 'khrap'),
        ('particle', 'khráp / khâ'),
        ('gloss', 'cząstka grzecznościowa'),
        ('meaning', 'Nie znaczy nic — sygnalizuje szacunek dla rozmówcy. '
                    '`khráp` mówi mężczyzna, `khâ` kobieta, `khá` kobieta '
                    'w pytaniu.'),
        ('effect', 'Podnosi całą wypowiedź o poziom uprzejmości, niezależnie '
                   'od jej treści.'),
        ('missing', 'Wobec obcej osoby, kogoś starszego albo kogoś, kto cię '
                    'obsługuje — brak jest odebrany jako opryskliwość. To '
                    'najczęstszy błąd Polaka, bo w polszczyźnie milczenie '
                    'w tym miejscu nie znaczy nic.'),
        ('register', 'każdy'),
        ('rude_without', True),
    ]),
    OrderedDict([
        ('id', 'na'),
        ('particle', 'ná'),
        ('gloss', 'szukanie zgody'),
        ('meaning', 'Prosi rozmówcę o przyzwolenie: „dobrze?”, „zgoda?”.'),
        ('effect', 'Zamienia polecenie w propozycję, a stwierdzenie '
                   'w zaproszenie do potwierdzenia.'),
        ('missing', 'Bez `ná` propozycja brzmi jak decyzja podjęta za '
                    'rozmówcę.'),
        ('register', 'neutralny'),
        ('rude_without', False),
    ]),
    OrderedDict([
        ('id', 'noi'),
        ('particle', 'nòi'),
        ('gloss', 'zmiękczenie prośby'),
        ('meaning', 'Dosłownie „trochę”, ale w prośbie nie mówi o ilości — '
                    'zmniejsza jej ciężar.'),
        ('effect', 'Zamienia żądanie w prośbę o drobiazg.'),
        ('missing', 'Prośba bez `nòi` brzmi jak polecenie, choćby miała '
                    '`khráp` na końcu.'),
        ('register', 'neutralny'),
        ('rude_without', False),
    ]),
    OrderedDict([
        ('id', 'duai'),
        ('particle', 'dûai'),
        ('gloss', 'też, przy okazji'),
        ('meaning', '„Również”, „razem”. W prośbie dokłada „proszę, przy '
                    'okazji”.'),
        ('effect', 'Dołącza wypowiedź do czegoś, co już zostało ustalone.'),
        ('missing', 'Bez `dûai` prośba wygląda na nową i osobną, a nie na '
                    'dopisek do poprzedniej.'),
        ('register', 'neutralny'),
        ('rude_without', False),
    ]),
    OrderedDict([
        ('id', 'si'),
        ('particle', 'sì'),
        ('gloss', 'nacisk, zachęta'),
        ('meaning', 'Popycha rozmówcę do działania: „no dawaj”, „śmiało”.'),
        ('effect', 'Wobec kogoś bliskiego brzmi serdecznie, wobec obcego — '
                   'jak popędzanie.'),
        ('missing', 'Bez `sì` zachęta jest neutralna. To partykuła, którą '
                    'lepiej pominąć niż wstawić w złej sytuacji.'),
        ('register', 'poufały'),
        ('rude_without', False),
    ]),
    OrderedDict([
        ('id', 'la'),
        ('particle', 'lâ / là'),
        ('gloss', 'domaganie się'),
        ('meaning', 'Po słowie pytającym domaga się odpowiedzi: `à-rai lâ` — '
                    '„no co?”.'),
        ('effect', 'Sygnalizuje, że rozmówca czegoś oczekiwał i tego nie '
                   'dostał.'),
        ('missing', 'Bez `lâ` pytanie jest zwykłym pytaniem. Z `lâ` niesie '
                    'niecierpliwość — i tak zostanie odebrane.'),
        ('register', 'poufały'),
        ('rude_without', False),
    ]),
    OrderedDict([
        ('id', 'loei'),
        ('particle', 'loei'),
        ('gloss', 'wzmocnienie'),
        ('meaning', 'Na końcu wypowiedzi: „w ogóle”, „zupełnie”, „od razu”.'),
        ('effect', 'Wzmacnia to, co przed nim — najczęściej przeczenie albo '
                   'ocenę.'),
        ('missing', 'Bez `loei` zdanie jest słabsze, niż mówiący zamierzał.'),
        ('register', 'neutralny'),
        ('rude_without', False),
    ]),
    OrderedDict([
        ('id', 'rok'),
        ('particle', 'ròk'),
        ('gloss', 'sprostowanie'),
        ('meaning', 'Prostuje cudze założenie: „ależ nie, przecież”.'),
        ('effect', 'Najuprzejmiejszy sposób zaprzeczenia rozmówcy — łagodzi '
                   'sam akt niezgody.'),
        ('missing', 'Samo `mâi` bez `ròk` zaprzecza wprost i w rozmowie '
                    'z obcą osobą bywa odebrane ostro.'),
        ('register', 'neutralny'),
        ('rude_without', False),
    ]),
]

# Ćwiczenie sytuacyjne: jedno zdanie, cztery partykuły, jedna sytuacja.
SITUATIONS = [
    ('Prosisz kelnera o rachunek. Widzisz go pierwszy raz w życiu.',
     'khrap', ['na', 'si', 'la'],
     'Do obcej osoby w sytuacji usługowej cząstka grzecznościowa jest '
     'obowiązkowa. `sì` popędzałoby, `lâ` brzmiałoby jak pretensja.'),
    ('Umawiasz się z koleżanką i chcesz, żeby potwierdziła godzinę.',
     'na', ['si', 'rok', 'loei'],
     '`ná` prosi o przyzwolenie — dokładnie to, czego tu potrzeba. '
     '`sì` byłoby naciskiem, a nie pytaniem o zgodę.'),
    ('Prosisz kogoś, żeby mówił wolniej. Nie chcesz zabrzmieć jak polecenie.',
     'noi', ['si', 'la', 'loei'],
     '`nòi` zmniejsza ciężar prośby. Bez niego zostaje goły rozkaz „mów '
     'wolniej”.'),
    ('Zamawiasz drugie piwo, po tym jak przed chwilą zamówiłeś pierwsze.',
     'duai', ['si', 'la', 'rok'],
     '`dûai` dokłada zamówienie do poprzedniego. Bez niego brzmi jak '
     'zamówienie od zera.'),
    ('Kolega waha się, czy spróbować potrawy. Zachęcasz go.',
     'si', ['khrap', 'rok', 'la'],
     '`sì` popycha do działania i wobec kolegi brzmi serdecznie. Do obcej '
     'osoby lepiej go nie używać.'),
    ('Ktoś twierdzi, że nie lubisz ostrego jedzenia. To nieprawda.',
     'rok', ['na', 'si', 'duai'],
     '`ròk` prostuje cudze założenie, łagodząc samą niezgodę. Suche `mâi` '
     'byłoby ostrzejsze.'),
    ('Pytasz drugi raz, bo pierwszy raz nikt ci nie odpowiedział.',
     'la', ['khrap', 'duai', 'rok'],
     '`lâ` niesie oczekiwanie, które nie zostało spełnione. To dokładnie ta '
     'sytuacja — ale wobec obcej osoby zabrzmi niecierpliwie.'),
    ('Mówisz, że coś zupełnie ci nie odpowiada.',
     'loei', ['na', 'noi', 'khrap'],
     '`loei` wzmacnia przeczenie. Bez niego zdanie brzmi łagodniej, niż '
     'chciałeś.'),
]


def build_particles(corpus, pool):
    by_id = {p['id']: p for p in PARTICLES}

    # Przykłady użycia z bazy — po jednym zdaniu na partykułę, najwcześniej
    # dostępne. Partykuła bez przykładu jest definicją, nie nauką.
    patterns = {
        'khrap': (r'khráp$', None),
        'na': (r'ná(?: khráp)?$', None),
        'noi': (r'nòi(?: (?:ná )?khráp)?$', None),
        'duai': (r'dûai(?: khráp)?$', None),
        'si': (r's[íì](?: khráp)?$', None),
        'la': (r'l[âà]$', None),
        'loei': (r'loei(?: khráp)?$', None),
        'rok': (r'ròk(?: khráp)?$', None),
    }
    for pid, (rx, _) in patterns.items():
        got = GP.select_patterns(corpus, pool, include=rx, want=4,
                                 min_syl=2, need_space=False)
        by_id[pid]['examples'] = [GP.clean_pattern(g) for g in got]
        avs = [corpus.available_from(g['thaiPhonetic']) for g in got]
        by_id[pid]['availableFrom'] = max(avs) if avs else None

    exercises = []
    for i, (sit, right, wrong, why) in enumerate(SITUATIONS, 1):
        opts = [right] + list(wrong)
        exercises.append(OrderedDict([
            ('id', 'gp-%03d' % i),
            ('situation', sit),
            ('options', [OrderedDict([
                ('id', o),
                ('particle', by_id[o]['particle']),
                ('gloss', by_id[o]['gloss']),
            ]) for o in opts]),
            ('answer', right),
            ('why', why),
        ]))
    return PARTICLES, exercises


# --------------------------------------------------------------------------
def main():
    corpus = GP.Corpus()
    pool = corpus.sentence_pool()
    topics = GP.load_records('grammar.json')
    e = sys.stderr.write

    listen = balance(build_listening(corpus, pool, topics),
                     'intent', LISTEN_CAP)
    jsonio.dump(OrderedDict([
        ('file', 'grammar-listening.json'),
        ('count', len(listen)),
        ('description', 'Wykrywanie konstrukcji ze słuchu: intencja, czas '
                        'i rejestr wypowiedzi. Zdania o nakładających się '
                        'sygnałach są odrzucone.'),
        ('axes', OrderedDict([
            ('intent', [OrderedDict([('id', k), ('label', v),
                                     ('why', INTENT_WHY[k])])
                        for k, v in INTENT_LABEL.items()]),
            ('time', [OrderedDict([('id', k), ('label', v),
                                   ('why', TIME_WHY[k])])
                      for k, v in TIME_LABEL.items()]),
        ])),
        ('intents', dict(Counter(i['intent'] for i in listen))),
        ('times', dict(Counter(i['time'] for i in listen))),
        ('records', listen),
    ]), os.path.join(DATA, 'grammar-listening.json'))
    e('grammar-listening.json: %d zadań, intencje %s\n'
      % (len(listen), dict(Counter(i['intent'] for i in listen))))

    trans = balance(build_transforms(corpus, pool),
                    'transform', TRANSFORM_CAP)
    jsonio.dump(OrderedDict([
        ('file', 'grammar-transform.json'),
        ('count', len(trans)),
        ('description', 'Przekształcenia zdań. Ocena idzie po strukturze: '
                        'liczy się marker we właściwym miejscu i zachowany '
                        'trzon, nie zgodność znak w znak.'),
        ('transforms', TRANSFORMS),
        ('kinds', dict(Counter(i['transform'] for i in trans))),
        ('records', trans),
    ]), os.path.join(DATA, 'grammar-transform.json'))
    e('grammar-transform.json: %d zadań, rodzaje %s\n'
      % (len(trans), dict(Counter(i['transform'] for i in trans))))

    particles, exercises = build_particles(corpus, pool)
    jsonio.dump(OrderedDict([
        ('file', 'particles.json'),
        ('count', len(particles)),
        ('description', 'Partykuły końcowe: znaczenie, wydźwięk i sytuacje, '
                        'w których ich brak jest niegrzeczny.'),
        ('exercises', exercises),
        ('records', particles),
    ]), os.path.join(DATA, 'particles.json'))
    e('particles.json: %d partykuł, %d ćwiczeń sytuacyjnych\n'
      % (len(particles), len(exercises)))


if __name__ == '__main__':
    main()
