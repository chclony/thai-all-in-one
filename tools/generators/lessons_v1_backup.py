#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator ścieżki nauki — data/lessons.json.

Zasada dydaktyczna, której pilnuje ten skrypt:

  1. Lekcja wprowadza od 2 do 6 nowych haseł leksykalnych (typ word/verb/noun/
     adjective/adverb). To one — i tylko one — poszerzają zasób sylab uczącego się.
  2. Każde nowe hasło musi natychmiast dać się użyć: w tej samej lekcji leży
     przynajmniej jedno zdanie, pytanie albo zwrot, który to hasło zawiera
     i którego WSZYSTKIE pozostałe sylaby uczący się już zna.
  3. Żadne zdanie w lekcji nie zawiera sylaby spoza zasobu znanego po tej lekcji.

Punkt 2 jest formalnym zapisem wymagania „żadna lekcja nie wprowadza słowa,
którego nie da się użyć w zdaniu z wcześniejszych lekcji”. Punkt 3 gwarantuje,
że uczący się nigdy nie widzi materiału, do którego brakuje mu podstaw.

Skrypt weryfikuje oba warunki po wygenerowaniu i kończy się błędem, jeśli
którykolwiek nie jest spełniony.
"""

import json
import os
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
    # Sesja N — 935 nowych haseł i 3 740 zdań aktywujących. Bez tego wiersza
    # nowa leksyka istnieje w słowniku, ale ścieżka jej nie widzi.
    'lexicon-01.json', 'lexicon-02.json', 'lexicon-03.json', 'lexicon-04.json',
]
DIALOGUE_FILES = ['dialogues-part-01.json', 'dialogues-part-02.json', 'dialogues-part-03.json']

LEX_TYPES = {'word', 'noun', 'verb', 'adjective', 'adverb'}
LEVEL_ORDER = ['Survival', 'A1', 'A2', 'B1', 'B2']
LEVEL_RANK = {l: i for i, l in enumerate(LEVEL_ORDER)}

# Ile lekcji na poziom. Suma = 132.
# Sesja N wydłuża ścieżkę ze 132 do 260 lekcji. Ograniczeniem nie była nigdy
# liczba lekcji, tylko liczba haseł zdolnych wejść do lekcji: przy 887
# aktywowalnych hasłach dalsze lekcje nie miałyby czego wprowadzać. Po sesji
# aktywowalnych jest 1 852, więc ścieżka ma z czego rosnąć.
#
# Liczby poniżej są SUFITAMI, nie kwotami: generator bierze tyle, ile da radę
# ułożyć, i zatrzymuje się sam. Sprawdzone doświadczalnie — przy 130 lekcjach
# A2 wychodzi 1 185 nowych haseł, przy 150 również 1 185. Ścieżka nasyca się
# na ~291 lekcjach i tego progu nie przeskoczy dokładaniem lekcji: ogranicza
# go kolejność, w jakiej sylaby wchodzą do obiegu, a nie miejsce w programie.
# Pozostałe ~667 aktywowalnych haseł czeka w słowniku na materiał, który
# wprowadzi brakujące sylaby — to zadanie dla kolejnej sesji.
#
# Podział między poziomy ma znaczenie i nie jest dowolny. Układ 34/90/130/90/25
# daje tyle samo haseł (1 185) w 291 lekcjach zamiast 315, ale zjada ogon
# kursu: B1 spada do 37 lekcji, B2 do zera, bo A2 zabiera materiał, z którego
# wyższe poziomy miałyby budować. Gęstsza ścieżka bez B2 jest gorsza od
# rzadszej z pełnym ogonem — stąd sufity poniżej.
LESSONS_PER_LEVEL = [
    ('Survival', 34),
    ('A1', 78),
    ('A2', 104),
    ('B1', 74),
    ('B2', 60),
]

MIN_RECORDS, MAX_RECORDS = 8, 15
MIN_NEW, MAX_NEW = 2, 6


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

# Indeks: sylaba -> zdania, w których występuje.
usage_by_syl = defaultdict(list)
for u in usages:
    for s in u['_syl']:
        usage_by_syl[s].append(u)

# Zdania kandydujące dla danego leksemu: muszą zawierać wszystkie jego sylaby.
def usages_for(lex):
    syls = sorted(lex['_syl'], key=lambda s: len(usage_by_syl[s]))
    if not syls or not usage_by_syl[syls[0]]:
        return []
    out = [u for u in usage_by_syl[syls[0]] if lex['_syl'] <= u['_syl']]
    return out


USAGES_OF = {}
for lex in lexemes:
    USAGES_OF[lex['id']] = usages_for(lex)

# Kolejność nauczania leksemów: poziom, potem częstotliwość, potem łatwość,
# a przy remisie — hasła krótsze i takie, które mają dużo gotowych zdań.
def lex_key(r):
    return (
        LEVEL_RANK[r['_lvl']],
        -int(r.get('frequency') or 0),
        int(r.get('difficulty') or 0),
        len(r['_syl']),
        -min(len(USAGES_OF[r['id']]), 40),
        r['id'],
    )


lexemes.sort(key=lex_key)

# Zdania sortujemy od najkrótszych i najczęstszych — krótsze zdanie jest
# lepszym pierwszym kontaktem z nowym słowem.
def usage_key(r):
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
    tiers = []
    tiers.append([d for d in dialogues_by_level[level] if d.get('category') == category])
    tiers.append(dialogues_by_level[level])
    for step in (1, -1, 2, -2, 3, -3, 4, -4):
        j = rank + step
        if 0 <= j < len(LEVEL_ORDER):
            lv = LEVEL_ORDER[j]
            tiers.append([d for d in dialogues_by_level[lv] if d.get('category') == category])
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


def covered(rec, extra):
    return rec['_syl'] <= (known | extra)


def U_PLURAL(n, few, many):
    """Polska liczba mnoga dla 2-4 kontra 5+."""
    n10, n100 = n % 10, n % 100
    if n == 1:
        return 'nowe hasło'
    if 2 <= n10 <= 4 and not (12 <= n100 <= 14):
        return few
    return many


def best_sample(items, labels=()):
    """Do celu lekcji bierzemy wypowiedź, która wygląda jak pełne zdanie,
       a nie jak urwany fragment słownikowy. Pierwszeństwo ma zdanie, w którym
       widać po polsku któreś z nowych haseł — sylaby bywają wspólne dla
       homofonów (widelec i naprawić to oba sâwm) i sam zapis fonetyczny
       nie wystarcza, żeby uznać zdanie za ilustrację hasła."""
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


LOOKAHEAD = 260          # ile haseł z kolejki oglądamy, szukając tematu lekcji

# Kolejność tematyczna kursu. Zaczynamy od tego, czego uczący się potrzebuje
# w pierwszej godzinie w Tajlandii, a dopiero potem schodzimy do abstrakcji.
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
theme_pos = 0            # wskaźnik obrotu po CURRICULUM


def activatable(cand, extra_syl):
    """Czy hasło da się dziś użyć: istnieje wolne zdanie, w całości pokryte
       znanym zasobem powiększonym o sylaby tego hasła."""
    trial = extra_syl | cand['_syl']
    for u in USAGES_OF[cand['id']]:
        if u['id'] in used_records:
            continue
        if u['_syl'] <= (known | trial):
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
    """Temat lekcji bierzemy z kolejności programowej, obracając wskaźnik.
       Kategorię pomijamy, jeśli nie ma dziś z czego jej uczyć — wróci na
       następnym obrocie, gdy dojdą podstawy."""
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
    scan = lex_pos

    taken = set()

    def take(cand):
        if cand['id'] in taken:
            return False
        act = activatable(cand, new_syl)
        if act is None:
            return False
        new_lex.append(cand)
        taken.add(cand["id"])
        new_syl.update(cand['_syl'])
        activations[cand['id']] = act
        if act['id'] not in [u['id'] for u in picked_usages]:
            picked_usages.append(act)
        return True

    # Przebieg 1 — hasła z tematu lekcji.
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
            take(cand)

    # Przebieg 2 — dopełnienie z czoła kolejki, gdy w temacie zabrakło haseł
    # możliwych do wprowadzenia. Kolejka jest posortowana poziomami, ale nie
    # wolno się na pierwszym wyższym poziomie zatrzymać: hasła pominięte
    # wcześniej leżą dalej i wciąż czekają na swoją kolej.
    looked2 = 0
    for cand in lex_queue[lex_pos:]:
        if len(new_lex) >= MIN_NEW or looked2 >= LOOKAHEAD:
            break
        if cand['id'] in used_records or cand['id'] in taken:
            continue
        if LEVEL_RANK[cand['_lvl']] > LEVEL_RANK[level]:
            continue
        looked2 += 1
        take(cand)

    if len(new_lex) < MIN_NEW:
        return None

    for x in new_lex:
        used_records.add(x['id'])
    # Hasła pominięte zostają w kolejce — wrócą, gdy dojdą im brakujące podstawy.
    # Wskaźnik przesuwamy tylko przez te, które są już zużyte.
    while lex_pos < len(lex_queue) and lex_queue[lex_pos]['id'] in used_records:
        lex_pos += 1
    for u in picked_usages:
        used_records.add(u['id'])

    pool_syl = known | new_syl

    # Dopełniamy lekcję zdaniami w pełni pokrytymi, najpierw takimi, które
    # zawierają nowe hasła.
    target = min(MAX_RECORDS, max(MIN_RECORDS, len(new_lex) + 7))
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
            used_records.add(u['id'])

    fill(lambda u: bool(u['_syl'] & new_syl) and LEVEL_RANK[u['_lvl']] <= LEVEL_RANK[level])
    fill(lambda u: bool(u['_syl'] & new_syl))
    fill(lambda u: LEVEL_RANK[u['_lvl']] <= LEVEL_RANK[level])
    fill(lambda u: True)

    if len(new_lex) + len(picked_usages) < MIN_RECORDS:
        # Za mało materiału — cofamy rezerwację.
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

    # Cel opisujemy przez konkret: zdanie, które uczący się po lekcji ułoży sam.
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
        'id': 'lesson-%03d' % number,
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
            'text': 'Zalicz %d z %d odpowiedzi (80%%) w sprawdzianie lekcji.' % (pass_needed, len(ids)),
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
        # Pusty temat nie kończy poziomu — obracamy program dalej i próbujemy
        # kolejnej kategorii. Dopiero gdy żadna nie ma czego wprowadzić,
        # poziom jest naprawdę wyczerpany.
        for _ in range(len(CURRICULUM)):
            lesson = build_lesson(level, number)
            if lesson is not None:
                break
        if lesson is None:
            number -= 1
            break
        lessons.append(lesson)
        made += 1
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
            errors.append('%s: rekord %s zawiera nieznane sylaby %s' % (L['id'], rid, sorted(missing)))
    for wid in L['newWordIds']:
        act = L['activations'].get(wid)
        if not act:
            errors.append('%s: hasło %s nie ma zdania aktywującego' % (L['id'], wid))
            continue
        a = by_id[act]
        if not (a['_syl'] <= after):
            errors.append('%s: zdanie aktywujące %s wykracza poza znany zasób' % (L['id'], act))
        if not (by_id[wid]['_syl'] <= a['_syl']):
            errors.append('%s: zdanie %s nie zawiera hasła %s' % (L['id'], act, wid))
        if act not in L['recordIds']:
            errors.append('%s: zdanie aktywujące %s nie jest w lekcji' % (L['id'], act))
    if not (MIN_RECORDS <= len(L['recordIds']) <= MAX_RECORDS):
        errors.append('%s: %d rekordów poza zakresem 8-15' % (L['id'], len(L['recordIds'])))
    if len(set(L['recordIds'])) != len(L['recordIds']):
        errors.append('%s: powtórzone ID w lekcji' % L['id'])
    seen_syl = after

all_ids = [rid for L in lessons for rid in L['recordIds']]
if len(all_ids) != len(set(all_ids)):
    errors.append('rekordy powtarzają się między lekcjami')

if errors:
    sys.stderr.write('\nBŁĘDY DYDAKTYCZNE:\n')
    for e in errors[:40]:
        sys.stderr.write('  ' + e + '\n')
    sys.exit(1)

# ------------------------------------------------------------------- zapis
for L in lessons:
    L.pop('activations', None)

payload = {
    'file': 'lessons.json',
    'count': len(lessons),
    'description': ('Ścieżka nauki. Lekcje ułożone tak, żeby każde nowe hasło dało się '
                    'natychmiast użyć w zdaniu zbudowanym wyłącznie ze znanego materiału.'),
    'levels': dict(Counter(L['level'] for L in lessons)),
    'records': lessons,
}

out = os.path.join(DATA, 'lessons.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)

sys.stderr.write('\nZapisano %s: %d lekcji, %d rekordów, %d dialogów.\n'
                 % (out, len(lessons), len(all_ids), len(used_dialogues)))
sys.stderr.write('Nowych haseł leksykalnych: %d. Sylab w obiegu po ostatniej lekcji: %d.\n'
                 % (sum(len(L['newWordIds']) for L in lessons), len(seen_syl)))
