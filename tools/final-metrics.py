#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wszystkie liczby raportu końcowego, mierzone od zera.

Raport zamykający projekt nie może powtarzać liczb z wcześniejszych raportów.
Każda liczba w `docs/raport-koncowy.md` ma pochodzić z jednego przebiegu tego
narzędzia i dać się odtworzyć jednym poleceniem:

    python3 tools/final-metrics.py                    wydruk czytelny
    python3 tools/final-metrics.py --json PLIK        dodatkowo zapis do JSON

CO SIĘ TU LICZY, A CZEGO NIE
----------------------------
„Rekord” to wpis w pliku słownikowym (`kind: vocabulary` w manifeście).
Dialogi, sceny, lekcje i ćwiczenia gramatyczne mają własne pliki i własne
liczniki — świadomie NIE wpadają do jednej sumy, bo „ile jest rekordów”
i „ile jest materiału” to dwa różne pytania i mieszanie ich daje liczbę,
której nie da się zinterpretować.

„Hasło leksykalne” to rekord typu word / noun / verb / adjective / adverb.
Zdanie, pytanie i zwrot są materiałem ćwiczeniowym, nie jednostką słownika,
więc do zasobu słownictwa się nie liczą.

SYLABA liczona jest z pola `syllables`, które generatory zapisują przy
rekordzie — a nie z ponownego dzielenia fonetyki w tym skrypcie. Powód:
podział na sylaby jest decyzją generatora (dywiz łączy sylaby wewnątrz
wyrazu), a liczenie go tutaj drugi raz własną regułą dałoby liczbę zbliżoną,
lecz inną, i nie byłoby wiadomo, która jest prawdziwa.
"""
import collections
import itertools
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')

LEX_TYPES = {'word', 'noun', 'verb', 'adjective', 'adverb'}

# Punkty odniesienia z sesji V. Trzymamy je tutaj po to, żeby raport mógł
# pokazać RÓŻNICĘ, a nie po to, żeby je przepisać.
SESSION_V = {
    'records': 20792,
    'lexemes': 3513,
    'syllableTokens': 1977,
    'syllableOccurrences': 125237,
    'verified': 2460,
}


def load(fn):
    with open(os.path.join(DATA, fn), encoding='utf-8') as fh:
        return json.load(fh)


def pct(part, whole):
    return 100.0 * part / whole if whole else 0.0


# --------------------------------------------------------------- model Zipfa
# Ten sam model co w tools/gap-analysis.py — powielony celowo, żeby raport
# dało się odtworzyć jednym plikiem. Punkty zaczepienia z korpusów MÓWIONYCH.
ANCHORS = [(1000, 0.85), (2000, 0.90), (3000, 0.93), (5000, 0.95)]


def coverage(n, a, b, total=60000):
    if n <= 0:
        return 0.0
    num = sum(1.0 / (r + b) ** a for r in range(1, int(n) + 1))
    den = sum(1.0 / (r + b) ** a for r in range(1, total + 1))
    return num / den


def fit_zipf():
    best, best_err = None, 1e9
    a = 0.80
    while a <= 1.40:
        b = 0.0
        while b <= 60.0:
            err = sum((coverage(n, a, b) - c) ** 2 for n, c in ANCHORS)
            if err < best_err:
                best, best_err = (a, b), err
            b += 1.0
        a += 0.01
    return best


def words_for(target, a, b):
    lo, hi = 1, 40000
    while lo < hi:
        mid = (lo + hi) // 2
        if coverage(mid, a, b) >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo


# ------------------------------------------------------------------- pomiary

def main():
    man = load('manifest.json')
    vocab_files = [f['file'] for f in man['dataFiles'] if f['kind'] == 'vocabulary']
    dlg_files = [f['file'] for f in man['dataFiles'] if f['kind'] == 'dialogues']

    records = []
    for fn in vocab_files:
        records.extend(load(fn)['records'])

    out = {}

    # --- 1. objętość ------------------------------------------------------
    examples = [ex for r in records for ex in r.get('examples', [])]
    ex_unique = len({ex['polish'] for ex in examples})

    dlg_count = dlg_lines = 0
    dlg_levels = collections.Counter()
    for fn in dlg_files:
        d = load(fn)
        dlg_count += len(d['records'])
        for x in d['records']:
            dlg_lines += len(x['lines'])
            dlg_levels[x['level']] += 1

    scenes = load('scenes.json')
    lessons = load('lessons.json')
    grammar = load('grammar.json')
    numbers = load('numbers.json')
    module0 = load('module-zero.json')

    out['volume'] = {
        'records': len(records),
        'vocabFiles': len(vocab_files),
        'examples': len(examples),
        'examplesUnique': ex_unique,
        'dialogues': dlg_count,
        'dialogueLines': dlg_lines,
        'scenes': scenes['count'],
        'sceneLines': scenes['lineCount'],
        'sceneQuestions': scenes['questionCount'],
        'lessons': lessons['count'],
        'lessonChapters': len(lessons['chapters']),
        'lessonNewWords': lessons['newWords'],
        'grammarTopics': grammar['count'],
        'grammarPatterns': grammar['patterns'],
        'grammarStages': len(grammar['stages']),
        'grammarListening': load('grammar-listening.json')['count'],
        'grammarTransform': load('grammar-transform.json')['count'],
        'numbers': numbers['count'],
        'numberDrills': len(numbers['drills']),
        'numberLessons': len(numbers['lessons']),
        'numberScenes': len(numbers['scenes']),
        'classifiers': load('classifiers.json')['count'],
        'exams': load('exams.json')['count'],
        'checkpoints': load('checkpoints.json')['count'],
        'rescue': load('rescue.json')['count'],
        'particles': load('particles.json')['count'],
        'module0Families': len(module0['families']),
        'module0Contrasts': len(module0['contrasts']),
        'comprehensionGaps': load('comprehension.json')['gapCount'],
        'comprehensionInference': load('comprehension.json')['inferenceCount'],
        'searchIndex': load('search-index.json')['count'],
    }

    # --- 2. rozkłady ------------------------------------------------------
    out['levels'] = dict(collections.Counter(r['level'] for r in records))
    out['types'] = dict(collections.Counter(r['type'] for r in records))
    out['registers'] = dict(collections.Counter(r['register'] for r in records))
    out['categories'] = dict(collections.Counter(r['category'] for r in records))
    out['dialogueLevels'] = dict(dlg_levels)
    out['lessonLevels'] = dict(lessons['levels'])

    # --- 3. sylaby --------------------------------------------------------
    syl = collections.Counter()
    for r in records:
        for s in r['syllables']:
            syl[s] += 1
    total_syl = sum(syl.values())
    ranked = [n for _, n in syl.most_common()]
    cum = list(itertools.accumulate(ranked))
    curve = {}
    for n in (50, 100, 200, 300, 500, 750, 1000, 1250, 1500, 1750, len(syl)):
        n = min(n, len(syl))
        curve[n] = round(pct(cum[n - 1], total_syl), 2)
    out['syllables'] = {
        'unique': len(syl),
        'occurrences': total_syl,
        'curve': curve,
        'top20': syl.most_common(20),
    }

    # --- 4. hasła leksykalne i pokrycie mowy ------------------------------
    lexemes = [r for r in records if r['type'] in LEX_TYPES]
    a, b = fit_zipf()
    path_words = lessons['newWords']
    out['lexical'] = {
        'lexemes': len(lexemes),
        'pathWords': path_words,
        'zipfA': round(a, 3), 'zipfB': round(b, 1),
        'coverageBase': round(100 * coverage(len(lexemes), a, b), 1),
        'coveragePath': round(100 * coverage(path_words, a, b), 1),
        'needFor90': words_for(0.90, a, b),
        'needFor95': words_for(0.95, a, b),
    }
    out['lexical']['gapTo95FromPath'] = max(
        0, out['lexical']['needFor95'] - path_words)
    out['lexical']['gapTo95FromBase'] = max(
        0, out['lexical']['needFor95'] - len(lexemes))

    lex_cat = collections.Counter(r['category'] for r in lexemes)
    out['lexicalByCategory'] = dict(lex_cat)
    out['lexicalByLevel'] = dict(collections.Counter(r['level'] for r in lexemes))

    # Czy próg 95% jest w danej kategorii OSIĄGALNY OBECNĄ METODĄ.
    #
    # Pytanie nie brzmi „ile brakuje”, tylko „czy jest z czego to dobrać”.
    # Metoda budowania bazy jest jedna: hasła pochodzą z białych list, a to,
    # co z tych list zostało niewykorzystane, leży w plikach
    # `tools/generators/reserve-stage*.json`. Rezerwa jest więc górnym
    # ograniczeniem na to, o ile kategoria może jeszcze urosnąć BEZ nowego
    # materiału źródłowego. Jeśli rezerwa jest mniejsza niż luka do progu,
    # kategoria jest nieosiągalna obecną metodą — i żaden kod tego nie zmieni,
    # bo brakuje nie przetwarzania, tylko słów.
    #
    # Zapotrzebowanie kategorii przybliżamy jej udziałem w bazie: kategoria
    # zajmująca 10% materiału potrzebuje 10% z needFor95. To przybliżenie,
    # bo prawdziwy rozkład częstości różni się między kategoriami — ale
    # zaniża wymaganie dla kategorii dużych, więc błąd idzie na KORZYŚĆ
    # projektu i wynik „nieosiągalne” jest tym bardziej wiarygodny.
    gen_dir = os.path.join(ROOT, 'tools', 'generators')
    reserve = collections.Counter()
    reserve_files = 0
    for fn in sorted(os.listdir(gen_dir)):
        if fn.startswith('reserve-stage') and fn.endswith('.json'):
            reserve_files += 1
            with open(os.path.join(gen_dir, fn), encoding='utf-8') as fh:
                for r in json.load(fh)['records']:
                    if r.get('category'):
                        reserve[r['category']] += 1

    need95 = out['lexical']['needFor95']
    cat_all = collections.Counter(r['category'] for r in records)
    detail, unreachable, zero_reserve = {}, 0, 0
    for cat, n in cat_all.items():
        have = lex_cat[cat]
        want = round(need95 * n / len(records))
        gap = max(0, want - have)
        have_res = reserve[cat]
        ok = have_res >= gap
        if not ok:
            unreachable += 1
        if have_res == 0:
            zero_reserve += 1
        detail[cat] = {'have': have, 'want': want, 'gap': gap,
                       'reserve': have_res, 'reachable': ok}
    out['reachability'] = {
        'categories': len(cat_all),
        'unreachable': unreachable,
        'zeroReserve': zero_reserve,
        'reserveTotal': sum(reserve.values()),
        'reserveFiles': reserve_files,
        'detail': detail,
    }

    # --- 5. weryfikacja językowa ------------------------------------------
    src = collections.Counter(r['source'] for r in records)
    verified = sum(n for s, n in src.items() if '(zweryfikowany)' in s)
    handmade = sum(n for s, n in src.items()
                   if 'opracowan' in s and '(zweryfikowany)' not in s)
    generated = len(records) - verified - handmade
    out['verification'] = {
        'verified': verified,
        'verifiedPct': round(pct(verified, len(records)), 1),
        'handmadeUnverified': handmade,
        'generated': generated,
        'generatedPct': round(pct(generated, len(records)), 1),
        'bySource': dict(src.most_common()),
    }

    # --- 6. różnice wobec sesji V -----------------------------------------
    now = {
        'records': len(records),
        'lexemes': len(lexemes),
        'syllableTokens': len(syl),
        'syllableOccurrences': total_syl,
        'verified': verified,
    }
    out['deltaVsSessionV'] = {
        k: {'sesjaV': SESSION_V[k], 'teraz': now[k], 'roznica': now[k] - SESSION_V[k]}
        for k in SESSION_V
    }

    # --- 7. ekrany i tryby ------------------------------------------------
    # Ekrany czytamy z bloku `var SCREENS = [ ... ];`, a nie z całego pliku:
    # ten sam wzorzec `{ id: ..., label: ... }` mają też grupy menu, więc
    # szukanie po całym app.js doliczało pozycje, które ekranami nie są.
    app = open(os.path.join(ROOT, 'js', 'app.js'), encoding='utf-8').read()
    block = re.search(r'var SCREENS = \[(.*?)\n  \];', app, re.S)
    screens = re.findall(r"\{ id: '([a-z0-9]+)', label: '([^']+)'",
                         block.group(1) if block else '')
    out['screens'] = [{'id': i, 'label': l} for i, l in screens]
    out['screenGroups'] = re.findall(r"\{ id: '([a-z]+)', +label: '([^']+)' \}",
                                     re.search(r'var GROUPS = \[(.*?)\];',
                                               app, re.S).group(1))
    # Tryby ćwiczeń wewnątrz ekranów — czytane z testu przeglądarkowego,
    # który jest jedynym miejscem trzymającym ich pełną listę.
    bt = open(os.path.join(ROOT, 'tools', 'browser-test.py'), encoding='utf-8').read()
    out['modes'] = {
        name.lower(): re.findall(r"'([a-z0-9]+)'", m.group(1))
        for name, m in ((n, re.search(r'%s_MODES = \[(.*?)\]' % n, bt, re.S))
                        for n in ('PRODUCE', 'GRAMMAR', 'LISTEN')) if m
    }

    # ------------------------------------------------------------- wydruk
    W = 74
    print('=' * W)
    print('LICZBY RAPORTU KOŃCOWEGO — pomiar w tej sesji')
    print('=' * W)

    v = out['volume']
    print('\n[1] OBJĘTOŚĆ')
    for label, key in [
            ('rekordy słownika', 'records'), ('przykłady zdań', 'examples'),
            ('   w tym unikalne', 'examplesUnique'),
            ('dialogi', 'dialogues'), ('kwestie w dialogach', 'dialogueLines'),
            ('sceny', 'scenes'), ('kwestie w scenach', 'sceneLines'),
            ('pytania do scen', 'sceneQuestions'),
            ('lekcje ścieżki nauki', 'lessons'), ('rozdziały', 'lessonChapters'),
            ('hasła wprowadzane przez ścieżkę', 'lessonNewWords'),
            ('tematy gramatyczne', 'grammarTopics'),
            ('wzorce gramatyczne', 'grammarPatterns'),
            ('ćwiczenia gramatyki ze słuchu', 'grammarListening'),
            ('ćwiczenia przekształceń', 'grammarTransform'),
            ('pozycje liczbowe', 'numbers'), ('klasyfikatory', 'classifiers'),
            ('zestawy egzaminacyjne', 'exams'),
            ('próbki kontrolne', 'checkpoints'),
            ('scenariusze ratowania rozmowy', 'rescue'),
            ('luki do uzupełnienia w dialogach', 'comprehensionGaps'),
            ('pozycje w indeksie czołowym', 'searchIndex')]:
        print('  %-36s %8d' % (label, v[key]))

    print('\n[2] ROZKŁAD REKORDÓW WG POZIOMU')
    for k in ('Survival', 'A1', 'A2', 'B1', 'B2'):
        if k in out['levels']:
            print('  %-36s %8d  %5.1f%%'
                  % (k, out['levels'][k], pct(out['levels'][k], len(records))))

    print('\n[3] ROZKŁAD REKORDÓW WG TYPU')
    for k, n in sorted(out['types'].items(), key=lambda x: -x[1]):
        print('  %-36s %8d  %5.1f%%' % (k, n, pct(n, len(records))))

    print('\n[4] ROZKŁAD REKORDÓW WG KATEGORII')
    for k, n in sorted(out['categories'].items(), key=lambda x: -x[1]):
        print('  %-36s %8d  %5.1f%%' % (k, n, pct(n, len(records))))

    s = out['syllables']
    print('\n[5] INWENTARZ SYLABICZNY')
    print('  unikalnych tokenów sylabicznych      %8d' % s['unique'])
    print('  wystąpień                            %8d' % s['occurrences'])
    print('  krzywa pokrycia:')
    for n, c in s['curve'].items():
        print('    %5d sylab -> %6.2f%%' % (n, c))

    lx = out['lexical']
    print('\n[6] HASŁA LEKSYKALNE I POKRYCIE MOWY POTOCZNEJ')
    print('  model Zipfa-Mandelbrota: a = %.2f, b = %.0f' % (lx['zipfA'], lx['zipfB']))
    print('  haseł w bazie                        %8d -> %5.1f%%'
          % (lx['lexemes'], lx['coverageBase']))
    print('  wprowadza ścieżka nauki              %8d -> %5.1f%%'
          % (lx['pathWords'], lx['coveragePath']))
    print('  do 90%% pokrycia potrzeba             %8d' % lx['needFor90'])
    print('  do 95%% pokrycia potrzeba             %8d' % lx['needFor95'])
    print('  brakuje od stanu ścieżki             %8d' % lx['gapTo95FromPath'])

    rc = out['reachability']
    print('\n[6b] OSIĄGALNOŚĆ PROGU 95% W KATEGORIACH (test rezerwy źródłowej)')
    print('  %-26s %6s %6s %6s %8s %s'
          % ('kategoria', 'hasła', 'potrz.', 'luka', 'rezerwa', 'osiągalne'))
    for cat, d in sorted(rc['detail'].items(), key=lambda x: -x[1]['want']):
        print('  %-26s %6d %6d %6d %8d %s'
              % (cat, d['have'], d['want'], d['gap'], d['reserve'],
                 'tak' if d['reachable'] else 'NIE'))
    print('  kategorii łącznie                    %8d' % rc['categories'])
    print('  NIEOSIĄGALNYCH obecną metodą         %8d' % rc['unreachable'])
    print('  w tym z zerową rezerwą źródłową      %8d' % rc['zeroReserve'])
    print('  rezerwa źródłowa łącznie             %8d haseł w %d plikach'
          % (rc['reserveTotal'], rc['reserveFiles']))

    ver = out['verification']
    print('\n[7] WERYFIKACJA JĘZYKOWA')
    print('  zweryfikowane (źródło z adnotacją)   %8d  %5.1f%%'
          % (ver['verified'], ver['verifiedPct']))
    print('  ręczne, bez adnotacji weryfikacji    %8d' % ver['handmadeUnverified'])
    print('  materiał wzorcowy z białych list     %8d  %5.1f%%'
          % (ver['generated'], ver['generatedPct']))

    print('\n[8] RÓŻNICE WOBEC SESJI V')
    print('  %-28s %10s %10s %10s' % ('miara', 'sesja V', 'teraz', 'różnica'))
    for k, d in out['deltaVsSessionV'].items():
        print('  %-28s %10d %10d %+10d' % (k, d['sesjaV'], d['teraz'], d['roznica']))

    print('\n[9] EKRANY I TRYBY')
    print('  ekranów %d w %d grupach' % (len(out['screens']), len(out['screenGroups'])))
    for mode, lst in out['modes'].items():
        print('  tryby %-10s %2d: %s' % (mode, len(lst), ', '.join(lst)))

    if '--json' in sys.argv:
        i = sys.argv.index('--json')
        with open(sys.argv[i + 1], 'w', encoding='utf-8') as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
        print('\nZapisano: %s' % sys.argv[i + 1])

    print('\nSPRAWDZEŃ: %d' % (len(out['volume']) + len(out['levels'])
                               + len(out['types']) + len(out['categories'])
                               + len(out['syllables']['curve']) + len(lx) + len(out['reachability']['detail'])
                               + len(ver) + len(out['deltaVsSessionV'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
