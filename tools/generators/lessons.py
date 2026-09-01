#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator ścieżki nauki — data/lessons.json.

WARUNEK DYDAKTYCZNY (bez zmian od pierwszej wersji, sprawdzany przez
tools/validate.py i przez ten skrypt):

  1. Lekcja wprowadza od 2 do 12 nowych haseł leksykalnych (word/verb/noun/
     adjective/adverb). To one — i tylko one — poszerzają zasób sylab.
  2. Każde nowe hasło musi natychmiast dać się użyć: w tej samej lekcji leży
     przynajmniej jedno zdanie zawierające to hasło, którego WSZYSTKIE
     pozostałe sylaby uczący się już zna.
  3. Żadne zdanie w lekcji nie zawiera sylaby spoza zasobu znanego po tej
     lekcji.

CO SIĘ ZMIENIŁO W SESJI O
=========================

Górny limit nowych haseł na lekcję rośnie z 6 do 12. Sam limit nic by nie
dał — ograniczeniem nie była liczba, tylko BUDŻET REKORDÓW. Lekcja mieści
8–15 rekordów. Przy zdaniach aktywujących „jeden do jednego” dziesięć nowych
haseł wymaga dziesięciu zdań, razem dwadzieścia rekordów: warunek 8–15
pęka, zanim pęknie cokolwiek innego.

Sesja O dołożyła do bazy zdania PAROWE i TRÓJKOWE — takie, w których naraz
stoją dwa albo trzy nowe hasła. Generator umie je teraz wykorzystać:

  faza A  bierze hasła z tematu lekcji, płacąc za każde jednym zdaniem,
  faza B  „dogęszcza” — szuka haseł, które aktywuje ZDANIE JUŻ WZIĘTE.
          Takie hasło kosztuje jeden rekord zamiast dwóch.

Fazy przeplatają się, dopóki starcza budżetu. Efekt: lekcja typu
10 haseł + 5 zdań zamiast 5 haseł + 5 zdań, przy identycznym warunku
dydaktycznym i identycznym limicie rekordów.

ZGODNOŚĆ WSTECZNA IDENTYFIKATORÓW
=================================

Ścieżka jest generowana od nowa, więc granice lekcji się przesuwają. Gdyby
identyfikatory nadawać po kolei, `lesson-057` znaczyłoby po przebudowie coś
innego niż przed nią, a zapisany postęp wskazywałby na cudzą lekcję. Dlatego:

  * Przed pierwszą przebudową obecna ścieżka jest kopiowana do
    `data/lessons-legacy.json`. To jedyne źródło prawdy o starym układzie;
    korzysta z niego także migracja postępu (js/progress-migration.js).
  * Każda nowa lekcja jest porównywana ze starymi po zbiorze NOWYCH HASEŁ
    (`newWordIds`) miarą ZAWIERANIA: ile procent materiału starej lekcji
    znalazło się w nowej. Dopasowanie jest zachłanne i jeden-do-jednego.
  * Przy zawieraniu >= 0.60 nowa lekcja PRZEJMUJE stary identyfikator.

    Dlaczego zawieranie, a nie Jaccard. Nowa lekcja jest gęstsza: wprowadza
    około dziewięciu haseł zamiast czterech, więc pochłania mniej więcej
    dwie stare lekcje. Jaccard takiej pary wynosi najwyżej 4/9 = 0.44 i
    ŻADNA para nie przekroczyłaby progu 0.50 — miara karałaby nas za to,
    że nowa lekcja daje więcej. Zawieranie pyta o właściwą rzecz: czy ktoś,
    kto zaliczył starą lekcję, przerobił większość tego, co niesie nowa.
    Przy 0.60 odpowiedź brzmi tak, a identyfikator ma prawo przetrwać.
  * Jedna nowa lekcja przejmuje co najwyżej JEDEN stary identyfikator, choć
    materiałowo bywa spadkobierczynią dwóch. Drugą starą lekcję obsługuje
    migracja postępu, przeliczając ją przez znane hasła.
  * Lekcje bez dopasowania dostają identyfikatory z puli `lesson-501` w górę,
    czyli takiej, która w starej ścieżce (1..314) wystąpić nie mogła.
    Nowy identyfikator nigdy więc nie koliduje ze starym zapisem.
  * Pole `number` niesie pozycję w ścieżce i JEST zmienne. Pole `id` jest
    trwałe. Cały interfejs adresuje lekcje przez `id`; `number` służy tylko
    do wyświetlania „lekcja 57 z 320”.
  * Każda lekcja niesie `legacyId` (stary identyfikator albo null) i
    `idOrigin` ('zachowany' / 'nowy'), żeby dało się to zweryfikować
    z zewnątrz — korzysta z tego test funkcjonalny.

ROZDZIAŁY I KAMIENIE MILOWE
===========================

Przy 320 lekcjach lista bez podziału jest nieczytelna. Generator dzieli
ścieżkę na rozdziały po kilkanaście lekcji, łamiąc je na granicach poziomu
i tematu, i opisuje, co daje ukończenie każdego z nich. Wynik trafia do
`lessons.json` w polu `chapters`; ekran Kurs czyta go wprost.
"""

import json
import os
import shutil
import sys
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
DATA = os.path.join(ROOT, 'data')

VOCAB_FILES = [
    'survival.json', 'core-lexicon-01.json', 'core-lexicon-02.json',
    'a1-part-01.json', 'a1-part-02.json',
    'a2-part-01.json', 'a2-part-02.json', 'supplemental-practical.json',
    'b1-part-01.json', 'b1-part-02.json', 'b1-part-03.json',
    'b2-part-01.json', 'b2-part-02.json',
    # Sesja N — 935 haseł i 3 740 zdań aktywujących „jeden do jednego”.
    'lexicon-01.json', 'lexicon-02.json', 'lexicon-03.json', 'lexicon-04.json',
    # Sesja O — hasła złożeniowe i zdania parowe/trójkowe. Bez tego wiersza
    # gęste lekcje nie mają z czego powstać.
    'lexicon-05.json', 'lexicon-06.json', 'lexicon-07.json', 'lexicon-08.json',
    'lexicon-09.json', 'lexicon-10.json', 'lexicon-11.json', 'lexicon-12.json',
]
DIALOGUE_FILES = ['dialogues-part-01.json', 'dialogues-part-02.json',
                  'dialogues-part-03.json']

LEX_TYPES = {'word', 'noun', 'verb', 'adjective', 'adverb'}
LEVEL_ORDER = ['Survival', 'A1', 'A2', 'B1', 'B2']
LEVEL_RANK = {l: i for i, l in enumerate(LEVEL_ORDER)}

# Sufity, nie kwoty: generator bierze tyle, ile da radę ułożyć.
LESSONS_PER_LEVEL = [
    ('Survival', 34),
    ('A1', 73),
    ('A2', 99),
    ('B1', 70),
    ('B2', 62),
]

MIN_RECORDS, MAX_RECORDS = 8, 15
MIN_NEW, MAX_NEW = 2, 14

# Ile rekordów wolno zająć fazie wprowadzania haseł. Reszta do MAX_RECORDS
# zostaje na zdania powtórkowe, żeby lekcja nie była samą listą nowości.
TAKE_BUDGET = 15

LEGACY_FILE = 'lessons-legacy.json'
ID_MATCH_THRESHOLD = 0.60
NEW_ID_BASE = 500          # nowe identyfikatory od lesson-501 w górę

CHAPTER_TARGET = 14
CHAPTER_MIN, CHAPTER_MAX = 10, 18


def load(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as f:
        return json.load(f)['records']


def norm_level(lv):
    """Poziomy zapisane jako 'A1/A2' sprowadzamy do niższego z pary."""
    if lv in LEVEL_RANK:
        return lv
    for part in str(lv).replace('/', ' ').split():
        if part in LEVEL_RANK:
            return part
    return 'A1'


# --------------------------------------------------------------------- dane
records = []
for f in VOCAB_FILES:
    records.extend(load(f))
dialogues = []
for f in DIALOGUE_FILES:
    dialogues.extend(load(f))

by_id = {r['id']: r for r in records}
grammar = load('grammar.json')

for r in records:
    r['_lvl'] = norm_level(r.get('level'))
    r['_syl'] = set(r.get('syllables') or [])

lexemes = [r for r in records if r['type'] in LEX_TYPES and r['_syl']]
usages = [r for r in records if r['type'] not in LEX_TYPES and r['_syl']]

usage_by_syl = defaultdict(list)
for u in usages:
    for s in u['_syl']:
        usage_by_syl[s].append(u)


def usages_for(lex):
    """Zdania kandydujące dla leksemu: muszą zawierać wszystkie jego sylaby."""
    syls = sorted(lex['_syl'], key=lambda s: len(usage_by_syl[s]))
    if not syls or not usage_by_syl[syls[0]]:
        return []
    return [u for u in usage_by_syl[syls[0]] if lex['_syl'] <= u['_syl']]


USAGES_OF = {}
for lex in lexemes:
    USAGES_OF[lex['id']] = usages_for(lex)

# ------------------------------------------------------- indeks gęstości
# COACT[id zdania] = leksemy, które to zdanie w całości zawiera.
# Powstaje przez odwrócenie USAGES_OF, więc nic nie liczymy dwa razy.
#
# To jest struktura, na której stoi cała gęstość lekcji. Zdanie parowe
# „Mam marchewkę i kapustę” zawiera dwa leksemy; wprowadzenie obu naraz
# kosztuje trzy rekordy (dwa hasła + zdanie) zamiast czterech.
COACT = defaultdict(list)
for lex in lexemes:
    for u in USAGES_OF[lex['id']]:
        COACT[u['id']].append(lex)

# Moc zdania = ile haseł WIELOSYLABOWYCH potrafi wprowadzić.
#
# Liczenie wszystkich haseł byłoby mylące: długie zdanie „Widzę tu X”
# zawiera w sobie phǒm, hěn, thîi, nîi — same jednosylabowe słówka funkcyjne,
# które uczący się poznał w pierwszych lekcjach. Taka „moc” jest pozorna,
# bo wszystkie te hasła są już zużyte. Zdanie parowe „Mam marchewkę
# i kapustę” ma moc 2 i to jest moc prawdziwa.
POWER = {}
for uid, v in COACT.items():
    POWER[uid] = sum(1 for x in v if len(x['_syl']) >= 2)
for lex in lexemes:
    USAGES_OF[lex['id']].sort(
        key=lambda u: (-POWER.get(u['id'], 0), len(u['_syl']), u['id']))

# Ile zdań na hasło oglądamy, szukając grupy. Pełna lista bywa liczona
# w tysiącach dla haseł jednosylabowych, a posortowana po mocy — te
# najlepsze i tak leżą na początku.
USAGE_SCAN = 140


def lex_key(r):
    """Kolejność nauczania: poziom, częstotliwość, łatwość, długość, podaż zdań."""
    return (
        LEVEL_RANK[r['_lvl']],
        -int(r.get('frequency') or 0),
        int(r.get('difficulty') or 0),
        len(r['_syl']),
        -min(len(USAGES_OF[r['id']]), 40),
        r['id'],
    )


lexemes.sort(key=lex_key)


def usage_key(r):
    """Krótsze i częstsze zdanie jest lepszym pierwszym kontaktem z hasłem."""
    return (
        len(r['_syl']),
        -int(r.get('frequency') or 0),
        int(r.get('difficulty') or 0),
        r['id'],
    )


usages.sort(key=usage_key)

# ------------------------------------------------------- gramatyka i dialogi
for g in grammar:
    g['_lvl'] = norm_level(g.get('level'))
grammar.sort(key=lambda g: (LEVEL_RANK[g['_lvl']], g['id']))

for d in dialogues:
    d['_lvl'] = norm_level(d.get('level'))

dialogues_by_level = defaultdict(list)
for d in dialogues:
    dialogues_by_level[d['_lvl']].append(d)
for lv in dialogues_by_level:
    dialogues_by_level[lv].sort(key=lambda d: d['id'])

used_dialogues = set()


def pick_dialogue(level, category):
    """Dialog do lekcji: najpierw ten sam poziom i temat, potem sam poziom,
       potem poziom sąsiedni. Preferujemy dialogi jeszcze nieużyte."""
    rank = LEVEL_RANK[level]
    tiers = [
        [d for d in dialogues_by_level[level] if d.get('category') == category],
        dialogues_by_level[level],
    ]
    for step in (1, -1, 2, -2, 3, -3, 4, -4):
        j = rank + step
        if 0 <= j < len(LEVEL_ORDER):
            lv = LEVEL_ORDER[j]
            tiers.append([d for d in dialogues_by_level[lv]
                          if d.get('category') == category])
            tiers.append(dialogues_by_level[lv])
    for tier in tiers:
        fresh = [d for d in tier if d['id'] not in used_dialogues]
        if fresh:
            used_dialogues.add(fresh[0]['id'])
            return fresh[0]
    for tier in tiers:
        if tier:
            return tier[0]
    return None


# ----------------------------------------------------------------- budowanie
known = set()            # znane sylaby
used_records = set()     # rekordy już wykorzystane w ścieżce
lessons = []

lex_queue = list(lexemes)
lex_pos = 0


def compact_queue():
    """Usuwa z kolejki hasła już wprowadzone. Bez tego okno LOOKAHEAD liczy
       zużyte pozycje i im dalej w kurs, tym mniej realnych kandydatów widzi
       generator — przy 1 700 wprowadzonych hasłach okno pokazywałoby prawie
       same trupy."""
    global lex_queue, lex_pos
    lex_queue = [r for r in lex_queue if r['id'] not in used_records]
    lex_pos = 0


def U_PLURAL(n, few, many):
    """Polska liczba mnoga dla 2-4 kontra 5+."""
    n10, n100 = n % 10, n % 100
    if n == 1:
        return 'nowe hasło'
    if 2 <= n10 <= 4 and not (12 <= n100 <= 14):
        return few
    return many


def best_sample(items, labels=()):
    """Do celu lekcji bierzemy wypowiedź wyglądającą jak pełne zdanie."""
    def rank(u):
        pl = (u.get('polish') or '').strip()
        low = pl.lower()
        shows = 1 if any(l and l.lower()[:5] in low for l in labels) else 0
        full = 1 if (pl[:1].isupper() and pl[-1:] in '.?!') else 0
        return (-shows, -full, -min(len(pl), 60), u['id'])
    return sorted(items, key=rank)[0] if items else None


def clean_label(text):
    """Etykieta hasła do tytułu lekcji: bez glos w nawiasach i bez ogonów."""
    t = str(text or '').split('(')[0]
    t = t.split(' / ')[0].split(',')[0]
    return t.strip(' .:;—-')


# Ile haseł z KOLEJKI ŻYWYCH oglądamy, szukając materiału na lekcję.
# Kolejka jest po każdej lekcji zagęszczana (patrz compact_queue), więc okno
# nie zatyka się hasłami już zużytymi. Zatykają je natomiast hasła, które
# czekają na brakujące sylaby — a tych po sesji O jest kilkaset. Okno 320
# (tyle miała sesja N) kończyło się na nich i generator ogłaszał wyczerpanie
# poziomu, mając 430 haseł gotowych do wprowadzenia tuż za oknem. Stąd 900.
LOOKAHEAD = 900

CURRICULUM = [
    'Podstawy i grzeczność',
    'Liczby i liczenie',
    'Jedzenie i napoje',
    'Restauracja',
    'Transport',
    'Miejsca i orientacja',
    'Zakupy i pieniądze',
    'Czasowniki',
    'Hotel',
    'Pytania',
    'Czas i daty',
    'Cechy i opinie',
    'Zdrowie',
    'Ludzie i rodzina',
    'Dom i codzienność',
    'Small talk',
    'Awarie i pomoc',
    'Pogoda i przyroda',
    'Praca i nauka',
    'Gramatyka użytkowa',
]
theme_pos = 0


def activatable(cand, extra_syl):
    """Czy hasło da się dziś użyć: istnieje WOLNE zdanie, w całości pokryte
       znanym zasobem powiększonym o sylaby tego hasła."""
    trial = extra_syl | cand['_syl']
    for u in USAGES_OF[cand['id']]:
        if u['id'] in used_records:
            continue
        if u['_syl'] <= (known | trial):
            return u
    return None


def activatable_by_picked(cand, picked):
    """Czy hasło aktywuje któreś ze zdań JUŻ wziętych do tej lekcji.
       To jest sedno gęstości: takie hasło nie zajmuje dodatkowego rekordu."""
    for u in picked:
        if cand['_syl'] <= u['_syl']:
            return u
    return None


def theme_supply(level):
    """Ile haseł da się dziś wprowadzić, w rozbiciu na kategorie."""
    counts = Counter()
    looked = 0
    for cand in lex_queue[lex_pos:]:
        if looked >= LOOKAHEAD:
            break
        if cand['id'] in used_records:
            continue
        if LEVEL_RANK[cand['_lvl']] > LEVEL_RANK[level]:
            continue
        looked += 1
        if activatable(cand, set()):
            counts[cand.get('category') or 'Inne'] += 1
    return counts


def choose_theme(level):
    """Temat lekcji z kolejności programowej. Kategorię pomijamy, jeśli nie ma
       dziś z czego jej uczyć — wróci na następnym obrocie."""
    global theme_pos
    counts = theme_supply(level)
    if not counts:
        return None
    for step in range(len(CURRICULUM)):
        cat = CURRICULUM[(theme_pos + step) % len(CURRICULUM)]
        if counts.get(cat, 0) >= 2:
            theme_pos = (theme_pos + step + 1) % len(CURRICULUM)
            return cat
    return counts.most_common(1)[0][0]


def build_lesson(level, number):
    """Buduje jedną lekcję. Zwraca None, jeśli na tym poziomie nie da się już
       spełnić warunków dydaktycznych."""
    global lex_pos

    theme = choose_theme(level)

    new_lex = []
    new_syl = set()
    activations = {}   # id leksemu -> zdanie, które go aktywuje
    picked_usages = []
    picked_ids = set()
    taken = set()

    def commit(group, act):
        """Wprowadza grupę haseł aktywowanych jednym zdaniem."""
        for x in group:
            new_lex.append(x)
            taken.add(x['id'])
            new_syl.update(x['_syl'])
            activations[x['id']] = act
        if act['id'] not in picked_ids:
            picked_usages.append(act)
            picked_ids.add(act['id'])

    def best_group(cand):
        """Szuka najlepszej GRUPY haseł, którą da się wprowadzić jednym
           zdaniem razem z `cand`.

           Zwraca (grupa, zdanie) albo (None, None). Grupa zawsze zawiera
           `cand`. Reguła doboru: zdanie musi być w całości pokryte zasobem
           znanym powiększonym o sylaby CAŁEJ grupy — czyli dokładnie warunek
           dydaktyczny nr 3, tyle że liczony dla kilku haseł naraz."""
        best, best_act, best_score = None, None, None
        for u in USAGES_OF[cand['id']][:USAGE_SCAN]:
            if u['id'] in used_records:
                continue
            free = [x for x in COACT.get(u['id'], ())
                    if x['id'] not in used_records and x['id'] not in taken
                    and LEVEL_RANK[x['_lvl']] <= LEVEL_RANK[level]]
            if cand not in free:
                free.append(cand)
            cover = set()
            for x in free:
                cover |= x['_syl']
            if not (u['_syl'] <= (known | new_syl | cover)):
                continue
            # Minimalny zestaw: hasła wnoszące sylaby, których jeszcze nie ma.
            need = u['_syl'] - (known | new_syl)
            group = [x for x in free if (x['_syl'] & need) or x is cand]
            # Reszta zdania to hasła już fonetycznie znane — wchodzą gratis
            # pod względem sylab, kosztują tylko slot rekordu.
            bonus = [x for x in free if x not in group]
            slots = TAKE_BUDGET - (len(new_lex) + len(picked_usages))
            cost_sentence = 0 if u['id'] in picked_ids else 1
            room = min(MAX_NEW - len(new_lex), slots - cost_sentence)
            if room < len(group):
                continue
            group = group + bonus[:room - len(group)]
            score = (-len(group), len(u['_syl']), u['id'])
            if best_score is None or score < best_score:
                best, best_act, best_score = group, u, score
            if len(group) >= 4:
                # Cztery hasła na jedno zdanie to sufit tego, co dają dane
                # sesji O (zdania trójkowe plus hasła fonetycznie znane).
                # Dalsze szukanie tylko kosztuje czas.
                break
        return best, best_act

    def take(cand, only_free=False):
        """Dodaje hasło (i jego towarzyszy) do lekcji.
           `only_free` = bierz tylko to, co mieści się w zdaniu JUŻ wziętym."""
        if cand['id'] in taken or cand['id'] in used_records:
            return False
        if len(new_lex) >= MAX_NEW:
            return False
        act = activatable_by_picked(cand, picked_usages)
        if act is not None:
            if len(new_lex) + len(picked_usages) + 1 > TAKE_BUDGET:
                return False
            commit([cand], act)
            return True
        if only_free:
            return False
        group, act = best_group(cand)
        if not group:
            return False
        commit(group, act)
        return True

    def densify():
        """Faza B — dogęszczanie. Przechodzimy kolejkę i bierzemy wszystko, co
           mieści się w zdaniach już wybranych."""
        added = 0
        looked = 0
        for cand in lex_queue[lex_pos:]:
            if len(new_lex) >= MAX_NEW or looked >= LOOKAHEAD:
                break
            if cand['id'] in used_records or cand['id'] in taken:
                continue
            if LEVEL_RANK[cand['_lvl']] > LEVEL_RANK[level]:
                continue
            looked += 1
            if take(cand, only_free=True):
                added += 1
        return added

    # Faza A — hasła z tematu lekcji, przeplatane dogęszczaniem.
    if theme:
        looked = 0
        for cand in lex_queue[lex_pos:]:
            if len(new_lex) >= MAX_NEW or looked >= LOOKAHEAD:
                break
            if cand['id'] in used_records:
                continue
            if LEVEL_RANK[cand['_lvl']] > LEVEL_RANK[level]:
                continue
            looked += 1
            if cand.get('category') != theme:
                continue
            if take(cand):
                densify()

    # Faza A' — dopełnienie z czoła kolejki, gdy w temacie zabrakło haseł.
    looked2 = 0
    for cand in lex_queue[lex_pos:]:
        if len(new_lex) >= MAX_NEW or looked2 >= LOOKAHEAD:
            break
        if cand['id'] in used_records or cand['id'] in taken:
            continue
        if LEVEL_RANK[cand['_lvl']] > LEVEL_RANK[level]:
            continue
        looked2 += 1
        if take(cand):
            densify()

    densify()

    if len(new_lex) < MIN_NEW:
        return None

    for x in new_lex:
        used_records.add(x['id'])
    while lex_pos < len(lex_queue) and lex_queue[lex_pos]['id'] in used_records:
        lex_pos += 1
    for u in picked_usages:
        used_records.add(u['id'])

    pool_syl = known | new_syl

    target = min(MAX_RECORDS,
                 max(MIN_RECORDS, len(new_lex) + len(picked_usages) + 3))

    def fill(pred):
        for u in usages:
            if len(new_lex) + len(picked_usages) >= target:
                return
            if u['id'] in used_records:
                continue
            if not (u['_syl'] <= pool_syl):
                continue
            if not pred(u):
                continue
            picked_usages.append(u)
            picked_ids.add(u['id'])
            used_records.add(u['id'])

    fill(lambda u: bool(u['_syl'] & new_syl)
         and LEVEL_RANK[u['_lvl']] <= LEVEL_RANK[level])
    fill(lambda u: bool(u['_syl'] & new_syl))
    fill(lambda u: LEVEL_RANK[u['_lvl']] <= LEVEL_RANK[level])
    fill(lambda u: True)

    if len(new_lex) + len(picked_usages) < MIN_RECORDS:
        for x in new_lex:
            used_records.discard(x['id'])
        for u in picked_usages:
            used_records.discard(u['id'])
        return None

    known.update(new_syl)

    ids = [x['id'] for x in new_lex] + [u['id'] for u in picked_usages]
    cats = Counter([x.get('category') for x in new_lex])
    category = theme if theme and cats.get(theme) else cats.most_common(1)[0][0]

    gram = grammar[(number - 1) % len(grammar)]
    same_level_gram = [g for g in grammar if g['_lvl'] == level]
    if same_level_gram:
        gram = same_level_gram[(number - 1) % len(same_level_gram)]

    dlg = pick_dialogue(level, category)

    labels = [clean_label(x['polish']) for x in new_lex]
    labels = [l for l in labels if l]

    title = '%s: %s' % (category, ', '.join(labels[:3]))
    if len(title) > 62:
        title = '%s: %s' % (category, ', '.join(labels[:2]))
    if len(title) > 62:
        title = title[:59].rstrip(' ,') + '…'

    act_ids = set(u['id'] for u in activations.values())
    acts = [u for u in picked_usages if u['id'] in act_ids]
    _s = best_sample(acts or picked_usages, labels)
    sample = _s['polish'] if _s else ''
    goal = ('Poznajesz %d %s (%s) i od razu składasz z nich wypowiedzi — '
            'np. „%s”. Wszystkie pozostałe słowa w tej lekcji znasz z lekcji '
            'wcześniejszych. Powtarzasz przy tym temat: %s.') % (
        len(new_lex),
        U_PLURAL(len(new_lex), 'nowe hasła', 'nowych haseł'),
        ', '.join(labels[:4]) + ('…' if len(labels) > 4 else ''),
        sample.rstrip('.'),
        gram['title'][0].lower() + gram['title'][1:],
    )

    pass_needed = max(6, int(round(len(ids) * 0.8)))

    return {
        'id': None,               # nadawane po dopasowaniu do starej ścieżki
        'number': number,
        'title': title,
        'level': level,
        'category': category,
        'goal': goal,
        'newWordIds': [x['id'] for x in new_lex],
        'recordIds': ids,
        'grammarId': gram['id'],
        'grammarTitle': gram['title'],
        'dialogueId': dlg['id'] if dlg else None,
        'dialogueTitle': dlg['title'] if dlg else None,
        'pass': {
            'questions': len(ids),
            'required': pass_needed,
            'accuracy': 80,
            'text': 'Zalicz %d z %d odpowiedzi (80%%) w sprawdzianie lekcji.'
                    % (pass_needed, len(ids)),
        },
        'activations': {k: v['id'] for k, v in activations.items()},
    }


number = 0
for level, want in LESSONS_PER_LEVEL:
    made = 0
    guard = 0
    while made < want and guard < want * 40:
        guard += 1
        number += 1
        lesson = None
        for _ in range(len(CURRICULUM)):
            lesson = build_lesson(level, number)
            if lesson is not None:
                break
        if lesson is None:
            number -= 1
            break
        lessons.append(lesson)
        made += 1
        compact_queue()
    sys.stderr.write('  %-9s %d lekcji\n' % (level, made))

# --------------------------------------------------------------- weryfikacja
errors = []
seen_syl = set()
for i, L in enumerate(lessons):
    new_ids = set(L['newWordIds'])
    new_syl = set()
    for wid in L['newWordIds']:
        new_syl |= by_id[wid]['_syl']
    after = seen_syl | new_syl
    for rid in L['recordIds']:
        r = by_id[rid]
        if rid in new_ids:
            continue
        missing = r['_syl'] - after
        if missing:
            errors.append('lekcja %d: rekord %s zawiera nieznane sylaby %s'
                          % (L['number'], rid, sorted(missing)))
    for wid in L['newWordIds']:
        act = L['activations'].get(wid)
        if not act:
            errors.append('lekcja %d: hasło %s nie ma zdania aktywującego'
                          % (L['number'], wid))
            continue
        a = by_id[act]
        if not (a['_syl'] <= after):
            errors.append('lekcja %d: zdanie aktywujące %s wykracza poza zasób'
                          % (L['number'], act))
        if not (by_id[wid]['_syl'] <= a['_syl']):
            errors.append('lekcja %d: zdanie %s nie zawiera hasła %s'
                          % (L['number'], act, wid))
        if act not in L['recordIds']:
            errors.append('lekcja %d: zdanie aktywujące %s nie jest w lekcji'
                          % (L['number'], act))
    if not (MIN_RECORDS <= len(L['recordIds']) <= MAX_RECORDS):
        errors.append('lekcja %d: %d rekordów poza zakresem 8-15'
                      % (L['number'], len(L['recordIds'])))
    if len(set(L['recordIds'])) != len(L['recordIds']):
        errors.append('lekcja %d: powtórzone ID w lekcji' % L['number'])
    seen_syl = after

all_ids = [rid for L in lessons for rid in L['recordIds']]
if len(all_ids) != len(set(all_ids)):
    errors.append('rekordy powtarzają się między lekcjami')

if errors:
    sys.stderr.write('\nBŁĘDY DYDAKTYCZNE:\n')
    for e in errors[:40]:
        sys.stderr.write('  ' + e + '\n')
    sys.exit(1)

# ------------------------------------------------- zgodność identyfikatorów
legacy_path = os.path.join(DATA, LEGACY_FILE)
lessons_path = os.path.join(DATA, 'lessons.json')

# Migawkę starej ścieżki robimy RAZ. Drugie uruchomienie generatora nie może
# nadpisać migawki już przebudowaną ścieżką — inaczej stracilibyśmy punkt
# odniesienia i dla identyfikatorów, i dla migracji postępu.
if not os.path.exists(legacy_path) and os.path.exists(lessons_path):
    shutil.copyfile(lessons_path, legacy_path)
    sys.stderr.write('Zapisano migawkę starej ścieżki: %s\n' % LEGACY_FILE)

legacy = []
if os.path.exists(legacy_path):
    with open(legacy_path, encoding='utf-8') as f:
        legacy = json.load(f)['records']

legacy_words = {L['id']: set(L.get('newWordIds') or []) for L in legacy}
legacy_order = {L['id']: L.get('number') or 0 for L in legacy}


def containment(old, new):
    """Jaka część materiału STAREJ lekcji leży w nowej. Miara niesymetryczna
       i to jest w niej najważniejsze — patrz uzasadnienie w nagłówku."""
    if not old:
        return 0.0
    return len(old & new) / float(len(old))


# Kandydaci na dopasowanie: tylko te stare lekcje, które dzielą z nową choć
# jedno hasło. Bez tego filtra porównywalibyśmy 320 x 314 par na pusto.
word_to_legacy = defaultdict(set)
for lid, words in legacy_words.items():
    for w in words:
        word_to_legacy[w].add(lid)

pairs = []
for idx, L in enumerate(lessons):
    mine = set(L['newWordIds'])
    cands = set()
    for w in mine:
        cands |= word_to_legacy.get(w, set())
    for lid in cands:
        score = containment(legacy_words[lid], mine)
        if score >= ID_MATCH_THRESHOLD:
            # Przy remisie wygrywa lekcja bliższa pozycją.
            dist = abs(legacy_order.get(lid, 0) - L['number'])
            pairs.append((-score, dist, idx, lid))

pairs.sort()
assigned_new, assigned_old = {}, set()
for negscore, dist, idx, lid in pairs:
    if idx in assigned_new or lid in assigned_old:
        continue
    assigned_new[idx] = (lid, -negscore)
    assigned_old.add(lid)

next_free = NEW_ID_BASE + 1
for idx, L in enumerate(lessons):
    if idx in assigned_new:
        lid, score = assigned_new[idx]
        L['id'] = lid
        L['legacyId'] = lid
        L['idOrigin'] = 'zachowany'
        L['idMatch'] = round(score, 3)
    else:
        L['id'] = 'lesson-%03d' % next_free
        next_free += 1
        L['legacyId'] = None
        L['idOrigin'] = 'nowy'
        L['idMatch'] = 0.0

kept = sum(1 for L in lessons if L['idOrigin'] == 'zachowany')

# ------------------------------------------------------------- rozdziały
def build_chapters(ls):
    """Dzieli ścieżkę na rozdziały po kilkanaście lekcji. Cięcia stawiamy na
       granicy poziomu zawsze, a wewnątrz poziomu tam, gdzie zmienia się temat
       i rozdział ma już przyzwoitą długość."""
    out = []
    cur = []
    for L in ls:
        if cur:
            same_level = cur[-1]['level'] == L['level']
            long_enough = len(cur) >= CHAPTER_MIN
            theme_break = cur[-1]['category'] != L['category']
            if (not same_level
                    or len(cur) >= CHAPTER_MAX
                    or (long_enough and theme_break
                        and len(cur) >= CHAPTER_TARGET)):
                out.append(cur)
                cur = []
        cur.append(L)
    if cur:
        out.append(cur)

    # Sklejanie ogarkow. Ciecie na granicy poziomu potrafi zostawic rozdzial
    # z jedna lekcja — „rozdzial 3: jedna lekcja” wyglada jak usterka, a nie
    # jak etap kursu. Taki kawalek dolaczamy do sasiada z tego samego poziomu:
    # najpierw do poprzedniego, a gdy poprzedni jest z innego poziomu — do
    # nastepnego. Jesli caly poziom ma mniej lekcji niz CHAPTER_MIN, zostaje
    # osobnym rozdzialem, bo do niczego nie pasuje.
    merged = []
    for group in out:
        if (merged and len(group) < CHAPTER_MIN
                and merged[-1][-1]['level'] == group[0]['level']
                and len(merged[-1]) + len(group) <= CHAPTER_MAX + CHAPTER_MIN):
            merged[-1].extend(group)
        else:
            merged.append(group)
    for i in range(len(merged) - 1):
        if (merged[i] and len(merged[i]) < CHAPTER_MIN
                and merged[i][-1]['level'] == merged[i + 1][0]['level']):
            merged[i + 1] = merged[i] + merged[i + 1]
            merged[i] = []
    return [g for g in merged if g]


groups = build_chapters(lessons)

chapters = []
for i, g in enumerate(groups, 1):
    cats = Counter(L['category'] for L in g)
    lead = [c for c, _ in cats.most_common(2)]
    words = sum(len(L['newWordIds']) for L in g)
    title = ' i '.join(lead) if len(lead) > 1 else lead[0]
    chapters.append({
        'id': 'chapter-%02d' % i,
        'number': i,
        'title': title,
        'level': g[0]['level'],
        'lessonIds': [L['id'] for L in g],
        'fromNumber': g[0]['number'],
        'toNumber': g[-1]['number'],
        'lessons': len(g),
        'newWords': words,
        'themes': [c for c, _ in cats.most_common()],
        'milestone': ('Po tym rozdziale masz w czynnym użyciu %d nowych haseł '
                      'i prowadzisz rozmowę na temat: %s.')
                     % (words, ', '.join(lead).lower()),
    })

chapter_of = {}
for ch in chapters:
    for lid in ch['lessonIds']:
        chapter_of[lid] = ch['id']
for L in lessons:
    L['chapterId'] = chapter_of.get(L['id'])

# ------------------------------------------------------------------- zapis
for L in lessons:
    L.pop('activations', None)

total_new_words = sum(len(L['newWordIds']) for L in lessons)

payload = {
    'file': 'lessons.json',
    'count': len(lessons),
    'description': ('Ścieżka nauki. Lekcje ułożone tak, żeby każde nowe hasło '
                    'dało się natychmiast użyć w zdaniu zbudowanym wyłącznie '
                    'ze znanego materiału.'),
    'levels': dict(Counter(L['level'] for L in lessons)),
    'newWords': total_new_words,
    'idCompatibility': {
        'legacyFile': LEGACY_FILE,
        'threshold': ID_MATCH_THRESHOLD,
        'kept': kept,
        'fresh': len(lessons) - kept,
        'legacyCount': len(legacy),
        'note': ('Identyfikator lekcji jest trwały; pole number zmienia się '
                 'przy przebudowie ścieżki. Lekcje bez odpowiednika w starej '
                 'ścieżce dostają numery od %d w górę.' % (NEW_ID_BASE + 1)),
    },
    'chapters': chapters,
    'records': lessons,
}

with open(lessons_path, 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)

avg_new = total_new_words / float(len(lessons)) if lessons else 0
sys.stderr.write('\nZapisano %s: %d lekcji, %d rekordów, %d dialogów.\n'
                 % (lessons_path, len(lessons), len(all_ids), len(used_dialogues)))
sys.stderr.write('Nowych haseł leksykalnych: %d (średnio %.2f na lekcję).\n'
                 % (total_new_words, avg_new))
sys.stderr.write('Sylab w obiegu po ostatniej lekcji: %d.\n' % len(seen_syl))
sys.stderr.write('Rozdziałów: %d. Identyfikatory zachowane: %d z %d starych.\n'
                 % (len(chapters), kept, len(legacy)))
