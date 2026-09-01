#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator progresji gramatycznej — data/grammar.json + przypisanie do lekcji.

CO ROBI
=======

1. Bierze ciąg dydaktyczny z `grammar_curriculum.py` (8 etapów).
2. Dla każdego tematu dobiera wzorce Z BAZY — nie pisze ich ręcznie.
3. Liczy, od której lekcji temat wolno pokazać: wszystkie sylaby wszystkich
   jego wzorców muszą być w obiegu.
4. Rozstawia tematy na ścieżce w kolejności dydaktycznej, nigdy przed
   dostępnością materiału.
5. Nadpisuje `grammarId` w `lessons.json` — koniec z rotacją.

DLACZEGO WZORCE POCHODZĄ Z BAZY
===============================

Zdanie napisane ręcznie na potrzeby tematu nie ma pisma tajskiego do syntezy,
wariantu żeńskiego ani zapisu potocznego, a jego sylaby nie muszą w ogóle
wchodzić do obiegu kursu. Zdanie wzięte z bazy ma to wszystko i przeszło już
walidację. Koszt: temat dostaje takie przykłady, jakie w bazie są — a nie
takie, jakie byłyby najładniejsze. To uczciwsza wymiana, niż się wydaje,
bo przykład spoza zasobu i tak nie nauczyłby niczego.

CO SIĘ DZIEJE Z LEKCJAMI MIĘDZY TEMATAMI
========================================

Tematów jest kilkadziesiąt, lekcji 333. Temat nie jest więc przypisany do
jednej lekcji, tylko OTWIERA blok lekcji i zostaje ich tematem aż do
otwarcia następnego. Lekcja otwierająca ma rolę `wprowadzenie`, pozostałe
`utrwalenie`. Dzięki temu każda lekcja ma nadal poprawne `grammarId`,
a konstrukcja dostaje kilka lekcji na osadzenie się, zamiast mignąć raz.
"""

import json
import os
import sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import grammar_progression as GP           # noqa: E402
from grammar_curriculum import CURRICULUM, STAGES   # noqa: E402
import jsonio                           # noqa: E402

DATA = GP.DATA

PLACEHOLDER = __import__('re').compile(r'\.\.\.|…|__')

MIN_PATTERNS = 3      # poniżej tego temat nie ma czym się wytłumaczyć
WANT_PATTERNS = 6
PATTERN_SLACK = 25    # o ile lekcji wolno przykładowi opóźnić temat

# 26 tematów sprzed sesji S. Lista jest zamrożona świadomie — służy wyłącznie
# do raportowania, co przetrwało rewizję, a nie do żadnej decyzji.
ORIGINAL_IDS = {'gram-%03d' % i for i in range(1, 27)}

LEVEL_BY_STAGE = {1: 'Survival', 2: 'Survival', 3: 'A1', 4: 'A1',
                  5: 'A2', 6: 'B1', 7: 'B1', 8: 'A2'}


def main():
    corpus = GP.Corpus()
    pool = corpus.sentence_pool()
    old = {r['id']: r for r in GP.load_records('grammar.json')}
    stage_title = {n: t for n, t, _ in STAGES}
    stage_note = {n: d for n, _, d in STAGES}

    topics = []
    dropped = []

    for order, spec in enumerate(CURRICULUM, 1):
        tid = spec['id']
        base = old.get(tid, {})
        sel = dict(spec.get('select') or {})
        sel.setdefault('want', WANT_PATTERNS)

        # Wzorce stare i dobrane idą do jednej puli, a z niej bierzemy
        # NAJWCZEŚNIEJ DOSTĘPNE.
        #
        # Zachowanie starych wzorców bezwarunkowo wygląda na szacunek dla
        # pracy poprzednich sesji, a jest pułapką: dostępność tematu to
        # najpóźniejszy z jego wzorców, więc jedno ręcznie napisane zdanie
        # z rzadką sylabą przesuwa CAŁY temat o sto lekcji. „Czasownik się
        # nie odmienia” trafiłby do lekcji 42 — po czterdziestu lekcjach,
        # w których uczący się już tego czasownika używał.
        #
        # Przy równej dostępności pierwszeństwo ma wzorzec stary: jest pisany
        # pod temat, a dobrany tylko do niego pasuje.
        cand = []
        for p in base.get('patterns') or []:
            ph = p.get('thaiPhonetic', '')
            # Ten sam filtr, co przy doborze: rekord szablonowy z wielokropkiem
            # nie jest zdaniem. Musi stać także tutaj, bo generator bywa
            # uruchamiany na własnym wyniku i bez tego przepuściłby raz
            # wpuszczony szablon w nieskończoność.
            if PLACEHOLDER.search(ph):
                continue
            av = corpus.available_from(ph)
            if av is not None:
                q = dict(p)
                q.setdefault('sourceId', '')
                cand.append((av, 0, q))
        old_expressible = len(cand)

        args = dict(sel)
        args['want'] = sel['want'] * 3
        for p in GP.select_patterns(corpus, pool, **args):
            av = corpus.available_from(p['thaiPhonetic'])
            cand.append((av, 1, GP.clean_pattern(p)))

        cand.sort(key=lambda x: (x[0], x[1], len(x[2]['thaiPhonetic'])))
        patterns, seen, floor_av = [], set(), None
        for av, _rank, p in cand:
            if p['thaiPhonetic'] in seen:
                continue
            # Szósty przykład nie jest wart odsunięcia całego tematu o pół
            # kursu. Dostępność tematu to najpóźniejszy z wzorców, więc gdy
            # kolejny kandydat wchodzi do obiegu znacznie później niż
            # komplet minimalny, kończymy — lepszy temat z czterema
            # przykładami w lekcji 40 niż z sześcioma w lekcji 104.
            if floor_av is not None and av > floor_av + PATTERN_SLACK:
                break
            seen.add(p['thaiPhonetic'])
            patterns.append(p)
            if len(patterns) == MIN_PATTERNS:
                floor_av = av
            if len(patterns) >= sel['want']:
                break
        dropped_patterns = len(base.get('patterns') or []) - old_expressible
        if len(patterns) < MIN_PATTERNS:
            dropped.append((tid, spec.get('title') or base.get('title'),
                            len(patterns)))
            continue

        avail = corpus.topic_available_from(patterns)
        stage = spec['stage']
        rec = OrderedDict()
        rec['id'] = tid
        rec['order'] = order
        rec['stage'] = stage
        rec['stageTitle'] = stage_title[stage]
        rec['family'] = spec['family']
        rec['title'] = spec.get('title') or base.get('title')
        rec['level'] = spec.get('level') or base.get('level') \
            or LEVEL_BY_STAGE[stage]
        rec['explanation'] = spec.get('explanation') or base.get('explanation')
        rec['contrast'] = spec['contrast']
        rec['tip'] = spec.get('tip') or base.get('tip') or ''
        rec['patterns'] = patterns
        rec['availableFrom'] = avail
        rec['patternsDropped'] = dropped_patterns
        # Pochodzenie liczone z numeru, nie z obecności w pliku: generator
        # bywa uruchamiany na własnym wyniku i wtedy „obecny w pliku" znaczy
        # tylko tyle, że poprzedni przebieg go zapisał.
        rec['source'] = 'zachowany' if tid in ORIGINAL_IDS else 'nowy'
        if base.get('classifierTable'):
            rec['classifierTable'] = base['classifierTable']
        rec['tags'] = sorted(set((base.get('tags') or []) +
                                 ['gramatyka', spec['family']]))
        topics.append(rec)

    # numeracja porządkowa po odrzuceniu tematów bez materiału
    for i, t in enumerate(topics, 1):
        t['order'] = i

    at = GP.assign_to_lessons(topics, corpus.total_lessons)
    for t, pos in zip(topics, at):
        t['introducedAt'] = pos

    lessons_payload = GP.load('lessons.json')
    lessons = lessons_payload['records']
    for t, pos in zip(topics, at):
        t['introducedIn'] = lessons[pos - 1]['id']

    # ------------------------------------------------ przypisanie do lekcji
    by_lesson = {}
    cur = None
    for i, L in enumerate(lessons, 1):
        opening = [t for t in topics if t['introducedAt'] == i]
        if opening:
            cur = opening[-1]
        by_lesson[i] = (cur, bool(opening))

    if by_lesson[1][0] is None:
        raise SystemExit('pierwsza lekcja bez tematu — sprawdź dostępność '
                         'materiału dla tematu nr 1')

    # Powtórka: temat wcześniejszy, wracający co kilka lekcji. Bierzemy go
    # rotacyjnie SPOŚRÓD JUŻ OTWARTYCH — rotacja jest tu na miejscu, bo
    # utrwalanie nie ma progresji, ma równomiernie wracać.
    changed = 0
    for i, L in enumerate(lessons, 1):
        topic, is_open = by_lesson[i]
        prior = [t for t in topics if t['introducedAt'] < topic['introducedAt']]
        review = prior[(i - 1) % len(prior)] if prior else None
        if L.get('grammarId') != topic['id']:
            changed += 1
        L['grammarId'] = topic['id']
        L['grammarTitle'] = topic['title']
        L['grammarStage'] = topic['stage']
        L['grammarRole'] = 'wprowadzenie' if is_open else 'utrwalenie'
        L['grammarReviewId'] = review['id'] if review else None
        L['grammarReviewTitle'] = review['title'] if review else None
        L['goal'] = rewrite_goal(L.get('goal', ''), topic, is_open)

    counts = Counter(L['grammarId'] for L in lessons)
    for t in topics:
        t['lessons'] = counts.get(t['id'], 0)

    # ------------------------------------------------------------- zapis
    payload = OrderedDict()
    payload['file'] = 'grammar.json'
    payload['count'] = len(topics)
    payload['description'] = (
        'Progresja gramatyczna w ośmiu etapach. Temat wchodzi do kursu '
        'dopiero wtedy, gdy wszystkie sylaby wszystkich jego wzorców są '
        'w obiegu — kolejność jest dydaktyczna, nie rotacyjna.')
    payload['stages'] = [
        OrderedDict([('number', n), ('title', t), ('note', d),
                     ('topics', sum(1 for x in topics if x['stage'] == n))])
        for n, t, d in STAGES]
    payload['patterns'] = sum(len(t['patterns']) for t in topics)
    payload['records'] = topics

    jsonio.dump(payload, os.path.join(DATA, 'grammar.json'))
    # lessons.json zapisuje generator ścieżki bez końcowej pustej linii —
    # trzymamy się tej samej konwencji, żeby dwa narzędzia nie przepychały
    # się o jeden bajt przy każdym uruchomieniu.
    with open(os.path.join(DATA, 'lessons.json'), 'w', encoding='utf-8') as f:
        json.dump(lessons_payload, f, ensure_ascii=False, indent=1)

    # ------------------------------------------------------------- raport
    e = sys.stderr.write
    e('Tematów gramatycznych: %d (zachowanych %d, nowych %d)\n'
      % (len(topics),
         sum(1 for t in topics if t['source'] == 'zachowany'),
         sum(1 for t in topics if t['source'] == 'nowy')))
    e('Wzorców razem: %d (średnio %.1f na temat)\n'
      % (payload['patterns'], payload['patterns'] / float(len(topics))))
    e('Zmieniono przypisanie w %d z %d lekcji.\n' % (changed, len(lessons)))
    for n, t, _ in STAGES:
        sub = [x for x in topics if x['stage'] == n]
        if not sub:
            continue
        e('  etap %d %-28s tematów %2d, lekcje %3d-%3d\n'
          % (n, t, len(sub), sub[0]['introducedAt'], sub[-1]['introducedAt']))
    if dropped:
        e('\nOdrzucone z braku materiału (mniej niż %d wzorców):\n'
          % MIN_PATTERNS)
        for tid, title, k in dropped:
            e('  %-10s %-46s %d\n' % (tid, (title or '')[:46], k))


def rewrite_goal(goal, topic, is_open):
    """Podmienia zdanie o temacie gramatycznym w celu lekcji.

    Stary tekst brzmiał „Powtarzasz przy tym temat: X.” dla każdej lekcji,
    bo temat i tak był losowy. Teraz lekcja albo temat OTWIERA, albo go
    utrwala, i cel ma to powiedzieć.
    """
    marker = ' Powtarzasz przy tym temat: '
    head = goal.split(marker)[0] if marker in goal else goal
    head = head.rstrip()
    low = topic['title'][0].lower() + topic['title'][1:]
    if is_open:
        tail = (' Nowy temat gramatyczny: %s — i wszystkie przykłady do niego '
                'złożone są ze słów, które już znasz.' % low)
    else:
        tail = ' Utrwalasz przy tym temat: %s.' % low
    return head + tail


if __name__ == '__main__':
    main()
