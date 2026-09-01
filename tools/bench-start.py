#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pomiar czasu startu — do momentu, w którym aplikacja jest GOTOWA DO UŻYCIA.

Zastępuje `tools/bench-start.js`, który był martwy. Tamten czekał na
wypełnienie `#today-word`, czyli na treść ekranu „Dzisiaj”. Świeży profil
nie startuje jednak na „Dzisiaj”, tylko na teście poziomującym — element
`#today-word` nigdy się nie wypełniał, a pomiar kończył się timeoutem 120 s
zamiast liczbą. Narzędzie nie mierzyło niczego od chwili, w której start
aplikacji przestał prowadzić prosto na ekran główny.

Co robi teraz:

  1. CZEKA NA TREŚĆ EKRANU, KTÓRY JEST FAKTYCZNIE AKTYWNY. Nie zakłada,
     na czym aplikacja wystartuje — pyta o to `App.screen` i czeka, aż ten
     ekran ma treść i coś, w co da się kliknąć. Dzięki temu ten sam pomiar
     działa dla świeżego profilu (test poziomujący) i dla powrotu (Dzisiaj),
     a jak dojdzie kiedyś trzeci ekran startowy, nie trzeba go tu dopisywać.

  2. MIERZY OSOBNO DWA PRZYPADKI, bo to dwie różne ścieżki kodu:
       · pierwsze uruchomienie — pusty magazyn, aplikacja idzie na test
         poziomujący,
       · powrót uczącego się — zapisany postęp z UKOŃCZONYM testem
         poziomującym, aplikacja idzie na „Dzisiaj” i musi odtworzyć stan
         nauki (kartoteka powtórek, seria dni, pokrycie).

  3. Przyjmuje KROTNOŚĆ DŁAWIENIA CPU jako parametr (`--dławienie`).

Użycie:

    python3 tools/bench-start.py                       oba profile, file:// i serwer, x4
    python3 tools/bench-start.py --dławienie 1         bez dławienia
    python3 tools/bench-start.py --tryb serwer         tylko przez serwer
    python3 tools/bench-start.py --profil powrot       tylko powrót uczącego się
    python3 tools/bench-start.py --indeks pelny        czekaj na pełny indeks w tle
    python3 tools/bench-start.py --proby 7             siedem powtórzeń zamiast pięciu

Wynik jest zestawiany z WARTOŚCIAMI ODNIESIENIA z sesji V (przy dławieniu
x4), więc widać nie tylko liczbę, ale i to, czy start się nie cofnął.
"""
import functools
import http.server
import json
import os
import socketserver
import statistics
import sys
import threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Wartości odniesienia z sesji V, dławienie CPU x4, mediana z pięciu prób.
# Klucz: (tryb, indeks) -> (pierwsze uruchomienie, powrót uczącego się).
REFERENCE = {
    ('file://', 'czolo'): (766, 792),
    ('serwer', 'czolo'): (1097, 1115),
    ('serwer', 'pelny'): (1360, 1887),
}

# Odchylenie, przy którym mówimy o regresji, a nie o szumie pomiaru.
# Pomiar startu na wspólnej maszynie potrafi skakać o kilkanaście procent
# między przebiegami, więc próg niżej byłby generatorem fałszywych alarmów.
TOLERANCE = 0.25

SHIMS = """
  Object.defineProperty(window, 'speechSynthesis', {
    configurable: true,
    value: { speak() {}, cancel() {}, resume() {},
             getVoices: () => [], addEventListener() {} }
  });
  window.SpeechSynthesisUtterance = function (t) { this.text = t; };
"""

# Profil powrotu: ukończony test poziomujący, pominięty Moduł 0, trochę
# historii. To jest stan, w którym aplikacja MA co odtwarzać — pusty postęp
# z samym `placement` mierzyłby prawie to samo, co pierwsze uruchomienie.
RETURNING = """
  localStorage.setItem('thaiaio.gender', JSON.stringify('male'));
  localStorage.setItem('thaiaio.progress', JSON.stringify(%s));
  localStorage.setItem('thaiaio.srs', JSON.stringify(%s));
"""


def _returning_seed():
    days = {}
    for i in range(14):
        days['2026-08-%02d' % (i + 1)] = {'minutes': 18, 'answers': 40, 'correct': 32}
    lessons = {}
    for i in range(1, 41):
        lessons['lesson-%03d' % i] = {'state': 'passed', 'score': 10, 'of': 12}
    progress = {
        'days': days, 'streak': 14, 'bestStreak': 14, 'lastDay': '2026-08-14',
        'totalAnswers': 560, 'totalCorrect': 448, 'minutes': 252,
        'seen': {}, 'favourites': {}, 'lists': {}, 'goal': 20,
        'lessons': lessons,
        'errors': {'category': {}, 'grammar': {}, 'type': {}, 'mode': {}},
        'perception': {'lessons': {}, 'contrasts': {}, 'history': [],
                       'diagnostic': None, 'skipped': True},
        'placement': {'level': 'A1', 'score': 18, 'total': 28,
                      'date': '2026-08-01', 'entryLesson': 'lesson-023'},
    }
    cards = {}
    for i in range(1, 121):
        cards['rec-%04d:r' % i] = {
            'id': 'rec-%04d:r' % i, 'due': '2026-08-14', 'interval': 6,
            'ease': 2.5, 'repetitions': 3, 'lapses': 0, 'last': '2026-08-08',
        }
    return json.dumps(progress, ensure_ascii=False), \
        json.dumps({'cards': cards}, ensure_ascii=False)


# Gotowość: ekran FAKTYCZNIE AKTYWNY ma treść i coś do kliknięcia.
# Nie pytamy o konkretny identyfikator ekranu — o to właśnie rozbił się
# poprzedni pomiar.
READY = """
  () => {
    if (!window.DB || !DB.ready || !window.App || !App.screen) return false;
    const node = document.getElementById('screen-' + App.screen);
    if (!node || node.hidden) return false;
    const text = (node.textContent || '').trim();
    if (text.length < 40) return false;
    const clickable = node.querySelector(
      'button:not([disabled]), a[href], .opt, .option, input, select');
    return !!clickable;
  }
"""

READY_FULL_INDEX = """
  () => {
    if (!window.DB || !DB.ready || !window.App || !App.screen) return false;
    if (!DB.indexComplete) return false;
    const node = document.getElementById('screen-' + App.screen);
    if (!node || node.hidden) return false;
    return (node.textContent || '').trim().length >= 40;
  }
"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve(port):
    socketserver.TCPServer.allow_reuse_address = True
    last = None
    for p in range(port, port + 20):
        try:
            httpd = socketserver.TCPServer(
                ('127.0.0.1', p), functools.partial(Quiet, directory=ROOT))
        except OSError as e:
            last = e
            continue
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        return httpd, p
    raise last


def _flag(name, default=None):
    flag = '--' + name
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


def measure(pw, url, profile, throttle, runs, full_index):
    """Jeden scenariusz: n uruchomień, zwraca listę czasów w ms."""
    browser = pw.chromium.launch(
        args=['--allow-file-access-from-files', '--no-sandbox'])
    times, info = [], None
    progress, srs = _returning_seed()
    for _ in range(runs):
        ctx = browser.new_context()
        page = ctx.new_page()
        page.add_init_script(SHIMS)
        if profile == 'powrot':
            page.add_init_script(RETURNING % (progress, srs))
        if throttle > 1:
            cdp = ctx.new_cdp_session(page)
            cdp.send('Emulation.setCPUThrottlingRate', {'rate': throttle})
        page.goto(url, wait_until='commit')
        page.wait_for_function(READY_FULL_INDEX if full_index else READY,
                               timeout=120000)
        info = page.evaluate("""() => ({
          ready: performance.now(),
          screen: App.screen,
          heap: performance.memory
            ? Math.round(performance.memory.usedJSHeapSize / 1048576) : null,
          inMemory: DB.records.length,
          total: DB.count ? DB.count() : DB.records.length,
          indexLen: DB.index ? DB.index.length : 0,
          indexComplete: !!DB.indexComplete,
          files: DB.loadedFiles.length,
          localMode: DB.localMode
        })""")
        times.append(info['ready'])
        ctx.close()
    browser.close()
    return sorted(times), info


def main():
    throttle = float(_flag('dławienie', _flag('dlawienie', '4')))
    runs = int(_flag('proby', _flag('próby', '5')))
    mode = _flag('tryb', 'oba')
    profile = _flag('profil', 'oba')
    index = _flag('indeks', 'czolo')
    if mode not in ('oba', 'file', 'serwer'):
        sys.stderr.write('--tryb: dozwolone file, serwer, oba\n')
        return 2
    if profile not in ('oba', 'pierwszy', 'powrot'):
        sys.stderr.write('--profil: dozwolone pierwszy, powrot, oba\n')
        return 2
    if index not in ('czolo', 'pelny'):
        sys.stderr.write('--indeks: dozwolone czolo, pelny\n')
        return 2

    httpd, port = serve(8790)
    targets = []
    if mode in ('oba', 'file'):
        targets.append(('file://', 'file://' + os.path.join(ROOT, 'index.html')))
    if mode in ('oba', 'serwer'):
        targets.append(('serwer', 'http://127.0.0.1:%d/index.html' % port))
    profiles = ['pierwszy', 'powrot'] if profile == 'oba' else [profile]

    print('=' * 74)
    print('CZAS STARTU — dławienie CPU x%g, prób na scenariusz: %d, indeks: %s'
          % (throttle, runs, 'pełny' if index == 'pelny' else 'czoło'))
    print('=' * 74)
    print('%-9s %-22s %7s %7s %7s %7s  %s'
          % ('TRYB', 'PROFIL', 'MED', 'ŚR', 'MIN', 'MAKS', 'ODNIESIENIE'))
    print('-' * 74)

    from playwright.sync_api import sync_playwright
    rows, regress = [], []
    with sync_playwright() as pw:
        for mode_label, url in targets:
            for prof in profiles:
                times, info = measure(pw, url, prof, throttle, runs,
                                      index == 'pelny')
                med = statistics.median(times)
                ref = REFERENCE.get((mode_label, index))
                want = ref[0 if prof == 'pierwszy' else 1] if ref else None
                mark = ''
                if want and abs(throttle - 4) < 0.01:
                    delta = (med - want) / want
                    mark = '%d ms  %+.0f%%' % (want, delta * 100)
                    if delta > TOLERANCE:
                        mark += '  REGRESJA'
                        regress.append('%s / %s: %d ms wobec %d ms'
                                       % (mode_label, prof, round(med), want))
                elif want:
                    mark = '%d ms (przy x4)' % want
                name = ('pierwsze uruchomienie' if prof == 'pierwszy'
                        else 'powrót uczącego się')
                print('%-9s %-22s %7d %7d %7d %7d  %s'
                      % (mode_label, name, round(med),
                         round(statistics.fmean(times)), round(times[0]),
                         round(times[-1]), mark))
                rows.append({
                    'tryb': mode_label, 'profil': prof, 'ekran': info['screen'],
                    'medianaMs': round(med), 'sredniaMs': round(statistics.fmean(times)),
                    'minMs': round(times[0]), 'maksMs': round(times[-1]),
                    'czasyMs': [round(t) for t in times],
                    'odniesienieMs': want, 'dlawienie': throttle,
                    'indeks': index, 'indeksKompletny': info['indexComplete'],
                    'hasel w indeksie': info['indexLen'],
                    'rekordowWPamieci': info['inMemory'],
                    'plikowWczytanych': info['files'],
                    'stertaMB': info['heap'], 'trybLokalny': info['localMode'],
                })
    httpd.shutdown()

    print('-' * 74)
    for r in rows:
        print('  %-9s %-22s ekran startowy: %-11s indeks %5d · plików %2d'
              % (r['tryb'], r['profil'], r['ekran'],
                 r['hasel w indeksie'], r['plikowWczytanych']))

    out = os.path.join(ROOT, 'tools', '.test-results')
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, 'bench-start.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print('\nSzczegóły zapisane w %s' % os.path.relpath(path, ROOT))

    if regress:
        print('\nREGRESJA STARTU (próg %+.0f%%):' % (TOLERANCE * 100))
        for r in regress:
            print('  ' + r)
        return 1
    print('\nWYNIK: START W NORMIE')
    return 0


if __name__ == '__main__':
    sys.exit(main())
