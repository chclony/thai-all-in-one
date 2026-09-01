#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Jedno polecenie uruchamiające cały zestaw testów.

Do tej sesji testy uruchamiało się pięcioma poleceniami — validate.py,
function-test.py, a11y-check.py, browser-test.py i zoom-motion-check.py —
i samodzielnie składało się z nich obraz całości. Ten skrypt robi to za
Ciebie i kończy się kodem niezerowym, jeśli cokolwiek padło.

    python3 tools/run-all-tests.py                 wszystko po kolei
    python3 tools/run-all-tests.py --tylko browser tylko etap przeglądarkowy
    python3 tools/run-all-tests.py --tylko a11y    tylko dostępność
    python3 tools/run-all-tests.py --lista         co się z czego składa
    python3 tools/run-all-tests.py --od-zera       zapomnij wyniki cząstkowe
    python3 tools/run-all-tests.py --podsumowanie  sam raport, bez uruchamiania
    python3 tools/run-all-tests.py --budzet 240    przerwij po 240 s, resztę potem

DLACZEGO ETAPAMI, A NIE JEDNYM CIĄGIEM
--------------------------------------
Środowisko, w którym ten projekt powstaje, ma dwa ograniczenia i oba
przewracają naiwny przebieg „uruchom pięć rzeczy pod rząd”:

  1. Pojedyncze polecenie ma limit czasu. Pełny `browser-test.py` to osiem
     kombinacji po ok. 65 s, czyli grubo ponad limit — przerywany jest
     w połowie i nie zostawia po sobie ŻADNEGO wyniku, bo drukuje wszystko
     dopiero na końcu.
  2. Procesy w tle bywają zabijane przez restart kontenera, więc ucieczka
     w `nohup ... &` też nie jest rozwiązaniem.

Dlatego przebieg jest pocięty na ZADANIA (patrz TASKS): każde mieści się
w limicie, a jego wynik ląduje na dysku natychmiast po zakończeniu,
w `tools/.test-results/`. Ponowne uruchomienie widzi, co już przeszło,
i robi wyłącznie resztę. Przerwany przebieg nie zaczyna od zera.

Wynik cząstkowy przestaje być ważny, gdy zmieni się to, co testuje —
dlatego przy każdym zapisie trzymamy ODCISK wejścia (rozmiary i czasy
modyfikacji plików `js/`, `data/`, `css/`, `index.html` oraz samego
narzędzia). Zmiana kodu albo danych unieważnia zapamiętane wyniki tych
etapów, których dotyczy, i każe je przeliczyć. Nie ma więc ryzyka, że
zielone podsumowanie opisuje poprzednią wersję aplikacji.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = os.path.join(ROOT, 'tools', '.test-results')

# Limit czasu na POJEDYNCZE zadanie. Dobrany tak, żeby najdłuższe zadanie
# (jedna kombinacja browser-testu, ok. 65 s) miało zapas na wolniejszą
# maszynę, a zawieszone zadanie nie zjadło całego przebiegu.
TASK_TIMEOUT = 600


# --- definicja etapów i zadań ----------------------------------------------
#
# Etap to nazwa, którą podaje się w `--tylko`. Zadanie to jedno wywołanie
# mieszczące się w limicie czasu pojedynczego polecenia. Etapy „szybkie”
# mają po jednym zadaniu; browser i a11y są pocięte, bo w całości nie
# mieszczą się w limicie.

def _browser_tasks():
    out = []
    for mode in ('file://', 'serwer'):
        for theme in ('light', 'dark'):
            for gender in ('male', 'female'):
                key = 'browser-%s-%s-%s' % (
                    'file' if mode == 'file://' else 'serwer', theme, gender)
                out.append({
                    'key': key,
                    'label': 'przeglądarka: %s / %s / %s' % (mode, theme, gender),
                    'cmd': ['tools/browser-test.py', ROOT,
                            '--tryb', mode, '--motyw', theme, '--plec', gender,
                            '--port', str(8180 + len(out))],
                })
    return out


A11Y_SCREENS = [
    ['today', 'session', 'course', 'srs', 'module0', 'listen'],
    ['produce', 'speak', 'grammar', 'numbers', 'rescue', 'dict'],
    ['dialogues', 'scenes', 'extensive', 'pron', 'placement', 'exam'],
    ['checkpoint', 'repair', 'progress', 'week', 'roadmap', 'settings'],
]


def _a11y_tasks():
    out = []
    for theme in ('light', 'dark'):
        for i, group in enumerate(A11Y_SCREENS, 1):
            out.append({
                'key': 'a11y-%s-%d' % (theme, i),
                'label': 'dostępność: %s, grupa %d/%d' % (theme, i, len(A11Y_SCREENS)),
                'cmd': ['tools/a11y-check.py', ROOT, '--motyw', theme,
                        '--ekrany', ','.join(group),
                        '--port', str(8150 + len(out))],
            })
    return out


STAGES = [
    {
        'name': 'validate',
        'title': 'Walidacja bazy',
        # Etapy danych zależą tylko od data/ i od samego walidatora —
        # zmiana w js/ ich nie unieważnia.
        'watch': ['data', 'tools/validate.py'],
        'tasks': [{'key': 'validate', 'label': 'walidacja bazy',
                   'cmd': ['tools/validate.py']}],
    },
    {
        'name': 'function',
        'title': 'Test działania',
        'watch': ['data', 'js', 'index.html', 'tools/function-test.py'],
        'tasks': [{'key': 'function', 'label': 'test działania',
                   'cmd': ['tools/function-test.py', ROOT]}],
    },
    {
        'name': 'a11y',
        'title': 'Dostępność',
        'watch': ['data', 'js', 'css', 'index.html', 'tools/a11y-check.py'],
        'tasks': _a11y_tasks(),
    },
    {
        'name': 'zoom',
        'title': 'Powiększenie tekstu i redukcja ruchu',
        'watch': ['data', 'js', 'css', 'index.html', 'tools/zoom-motion-check.py'],
        'tasks': [{'key': 'zoom', 'label': 'powiększenie i redukcja ruchu',
                   'cmd': ['tools/zoom-motion-check.py', ROOT]}],
    },
    {
        'name': 'browser',
        'title': 'Test w przeglądarce',
        'watch': ['data', 'js', 'css', 'index.html', 'tools/browser-test.py'],
        'tasks': _browser_tasks(),
    },
    {
        # Obietnica „uczący się nigdy nie widzi pisma tajskiego” była przez
        # trzynaście sesji zdaniem w raporcie. Od tej sesji jest etapem
        # testów: dane, interfejs i oba eksporty sprawdzane osobno.
        'name': 'tajski',
        'title': 'Brak pisma tajskiego u uczącego się',
        'watch': ['data', 'js', 'index.html', 'tools/thai-script-check.py'],
        'tasks': [{'key': 'tajski', 'label': 'pismo tajskie: dane, ekrany, eksporty',
                   'cmd': ['tools/thai-script-check.py', '--port', '8199',
                           '--json', 'tools/.test-results/thai-script.json']}],
    },
]


# --- odcisk wejścia --------------------------------------------------------

def _fingerprint(paths):
    """Odcisk plików wejściowych etapu.

    Liczony z nazw, rozmiarów i czasów modyfikacji, a nie z treści —
    treść 118 MB danych czytałaby się dłużej niż niejeden test, a do
    wykrycia „coś się zmieniło, przelicz” w zupełności wystarczy metryka.
    """
    h = hashlib.sha256()
    for rel in sorted(paths):
        p = os.path.join(ROOT, rel)
        if os.path.isfile(p):
            st = os.stat(p)
            h.update(('%s|%d|%d' % (rel, st.st_size, int(st.st_mtime))).encode())
        elif os.path.isdir(p):
            for dirpath, dirnames, filenames in os.walk(p):
                dirnames.sort()
                for fn in sorted(filenames):
                    fp = os.path.join(dirpath, fn)
                    st = os.stat(fp)
                    h.update(('%s|%d|%d' % (os.path.relpath(fp, ROOT),
                                            st.st_size, int(st.st_mtime))).encode())
    return h.hexdigest()[:16]


def _state_path(key):
    return os.path.join(STATE_DIR, key + '.json')


def _load_state(key):
    try:
        with open(_state_path(key), encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def _save_state(key, payload):
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = _state_path(key) + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    # Podmiana atomowa: przerwanie w trakcie zapisu nie zostawia
    # uciętego pliku, który przy następnym przebiegu udawałby wynik.
    os.replace(tmp, _state_path(key))


# --- odczyt wyniku z tego, co narzędzie wypisało ---------------------------

def _parse(name, out):
    """Wyciąga z wyjścia narzędzia liczbę asercji i zakres.

    Narzędzia mówią różnymi jednostkami i nie ma sensu tego udawać:
    validate liczy rekordy i błędy, function-test asercje OK/BŁĄD,
    reszta sprawdzenia na widokach. Zbieramy jedno i drugie, a raport
    pokazuje osobno „asercje” i „zakres”.
    """
    res = {'asercje': 0, 'zakres': ''}
    for line in out.splitlines():
        s = line.strip()
        if s.startswith('SPRAWDZEŃ:'):
            try:
                res['asercje'] += int(s.split(':', 1)[1].strip())
            except ValueError:
                pass
        if name == 'function':
            if s.startswith('OK ') or s.startswith('BŁĄD '):
                res['asercje'] += 1
        if name == 'validate' and s.startswith('Błędy:'):
            res['zakres'] = s
        if name == 'validate' and 'rekordów słownika' in s:
            res['zakres'] = s
    if name == 'validate':
        for line in out.splitlines():
            if 'Błędy:' in line:
                res['zakres'] = line.strip()
                # Walidator nie ma pojęcia „asercji” — ma reguły
                # przebiegające po rekordach. Liczymy jego wypowiedziane
                # kontrole: każda linia statystyki to jedna zmierzona rzecz.
    if name == 'validate':
        res['asercje'] = sum(1 for l in out.splitlines()
                             if l.startswith('  ') and not l.strip().startswith(
                                 ('BŁĄD', 'OSTRZEŻENIE')) and l.strip())
    return res


def _run_task(stage, task, fp):
    cmd = [sys.executable, '-u'] + [
        os.path.join(ROOT, task['cmd'][0])] + list(task['cmd'][1:])
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                              timeout=TASK_TIMEOUT)
        rc, out = proc.returncode, (proc.stdout or '') + (proc.stderr or '')
    except subprocess.TimeoutExpired as e:
        rc = 124
        out = ((e.stdout or '') if isinstance(e.stdout, str) else '') + \
              '\nPRZEKROCZONY LIMIT CZASU ZADANIA (%d s)' % TASK_TIMEOUT
    dt = time.time() - t0
    parsed = _parse(stage['name'], out)
    payload = {
        'key': task['key'], 'stage': stage['name'], 'label': task['label'],
        'rc': rc, 'ok': rc == 0, 'seconds': round(dt, 1),
        'asercje': parsed['asercje'], 'zakres': parsed['zakres'],
        'fingerprint': fp, 'when': time.strftime('%Y-%m-%d %H:%M:%S'),
        # Przy porażce trzymamy ogon wyjścia — inaczej trzeba by
        # powtarzać dziesięciominutowy przebieg tylko po to, żeby
        # zobaczyć, co właściwie nie przeszło.
        'output': out if rc != 0 else out[-2000:],
    }
    _save_state(task['key'], payload)
    return payload


def _fmt_time(sec):
    if sec < 60:
        return '%.1f s' % sec
    return '%d min %02d s' % (int(sec) // 60, int(sec) % 60)


def main():
    argv = sys.argv[1:]
    budget = 0.0
    if '--budzet' in argv:
        i = argv.index('--budzet')
        if i + 1 >= len(argv):
            sys.stderr.write('--budzet wymaga liczby sekund\n')
            return 2
        budget = float(argv[i + 1])

    only = None
    if '--tylko' in argv:
        i = argv.index('--tylko')
        if i + 1 >= len(argv):
            sys.stderr.write('--tylko wymaga nazwy etapu\n')
            return 2
        only = argv[i + 1]
        names = [s['name'] for s in STAGES]
        if only not in names:
            sys.stderr.write('--tylko: dozwolone %s\n' % ', '.join(names))
            return 2

    if '--lista' in argv:
        print('Etapy i zadania (zadanie = jedno wywołanie mieszczące się '
              'w limicie czasu):\n')
        for st in STAGES:
            print('  %-9s %-38s zadań: %d' % (st['name'], st['title'],
                                              len(st['tasks'])))
            for t in st['tasks']:
                print('             · %s' % t['label'])
        return 0

    if '--od-zera' in argv and os.path.isdir(STATE_DIR):
        shutil.rmtree(STATE_DIR)
        print('Wyniki cząstkowe skasowane.\n')

    stages = [s for s in STAGES if only is None or s['name'] == only]
    report_only = '--podsumowanie' in argv

    results = {}
    started = time.time()
    stopped_early = False
    for st in stages:
        fp = _fingerprint(st['watch'])
        todo = []
        for task in st['tasks']:
            prev = _load_state(task['key'])
            if prev and prev.get('fingerprint') == fp and prev.get('ok'):
                results[task['key']] = dict(prev, cached=True)
            else:
                todo.append(task)
        if report_only:
            for task in todo:
                prev = _load_state(task['key'])
                if prev:
                    results[task['key']] = dict(prev, cached=True,
                                                stale=prev.get('fingerprint') != fp)
            continue
        if todo:
            print('%s — %d zadań do wykonania (%d z pamięci)'
                  % (st['title'], len(todo), len(st['tasks']) - len(todo)))
        for task in todo:
            # Budżet czasu na CAŁE wywołanie. Bez niego przy limicie czasu
            # polecenia ostatnie zadanie ginie w połowie i nie zapisuje
            # niczego — a tak przebieg kończy się sam, z raportem i jasnym
            # „uruchom ponownie”. Zadanie, które już trwa, dokańczamy:
            # przerwane w połowie nie zostawiłoby wyniku.
            if budget and (time.time() - started) > budget:
                stopped_early = True
                break
            sys.stdout.write('  · %-46s ' % task['label'])
            sys.stdout.flush()
            r = _run_task(st, task, fp)
            results[task['key']] = r
            print('%s  %s' % ('OK  ' if r['ok'] else 'BŁĄD',
                              _fmt_time(r['seconds'])))
        if stopped_early:
            print('  … budżet %s wyczerpany, reszta przy następnym '
                  'uruchomieniu' % _fmt_time(budget))
            break

    # --- podsumowanie zbiorcze ---
    print()
    print('=' * 74)
    print('PODSUMOWANIE ZBIORCZE')
    print('=' * 74)
    print('%-11s %-9s %6s %10s  %s' % ('ETAP', 'WYNIK', 'ZADAŃ', 'ASERCJI', 'CZAS'))
    print('-' * 74)

    total_a = total_t = 0
    failed_stages, missing = [], []
    for st in stages:
        rs = [results.get(t['key']) for t in st['tasks']]
        done = [r for r in rs if r]
        brak = len(rs) - len(done)
        if brak:
            missing.append((st['name'], brak))
        bad = [r for r in done if not r['ok']]
        stale = [r for r in done if r.get('stale')]
        a = sum(r['asercje'] for r in done)
        t = sum(r['seconds'] for r in done)
        total_a += a
        total_t += t
        if bad:
            verdict = 'BŁĄD'
            failed_stages.append(st['name'])
        elif brak or stale:
            verdict = 'NIEPEŁNY'
        else:
            verdict = 'przeszedł'
        print('%-11s %-9s %3d/%-3d %10d  %s'
              % (st['name'], verdict, len(done), len(rs), a, _fmt_time(t)))
    print('-' * 74)
    print('%-11s %-9s %10d %s' % ('RAZEM', '', total_a, _fmt_time(total_t)))

    for st in stages:
        for t in st['tasks']:
            r = results.get(t['key'])
            if r and not r['ok']:
                print()
                print('NIE PRZESZŁO: %s (kod %s)' % (r['label'], r['rc']))
                for line in (r.get('output') or '').strip().splitlines()[-25:]:
                    print('  ' + line)

    zakres = [results[t['key']].get('zakres') for st in stages
              for t in st['tasks'] if results.get(t['key'])
              and results[t['key']].get('zakres')]
    if zakres:
        print()
        print('Walidacja: %s' % zakres[0])

    print()
    if failed_stages:
        print('WYNIK: SĄ BŁĘDY — %s' % ', '.join(failed_stages))
        return 1
    if missing or any(r.get('stale') for r in results.values()):
        print('WYNIK: PRZEBIEG NIEPEŁNY — uruchom ponownie, żeby dokończyć '
              'brakujące zadania.')
        return 1
    print('WYNIK: WSZYSTKO PRZESZŁO')
    return 0


if __name__ == '__main__':
    sys.exit(main())
