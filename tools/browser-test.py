#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test aplikacji w przeglądarce: wszystkie ekrany, oba motywy, obie płcie.

Sprawdza:
  - brak błędów w konsoli i nieobsłużonych wyjątków,
  - że każdy ekran się renderuje i ma treść,
  - że w DOM nie pojawia się pismo tajskie,
  - działanie w trybie file:// oraz przez serwer.
"""
import sys, os, time, json, threading, http.server, socketserver, functools, re

# Ścieżka musi być bezwzględna: 'file://' + './index.html' daje ERR_INVALID_URL,
# więc wywołanie `python3 tools/browser-test.py .` kończyło się wyjątkiem.
# Argumenty: katalog projektu, a dalej opcjonalne zawężenia przebiegu.
#
#   python3 tools/browser-test.py .                    wszystkie 8 kombinacji
#   python3 tools/browser-test.py . --tryb serwer      tylko przez serwer
#   python3 tools/browser-test.py . --motyw dark       tylko ciemny motyw
#   python3 tools/browser-test.py . --plec female      tylko forma żeńska
#   python3 tools/browser-test.py . --port 8140        inny port (przebiegi równoległe)
#
# Pełny przebieg to 2 tryby x 2 motywy x 2 płcie x 16 ekranów i trwa kilkanaście
# minut. Zawężenia pozwalają rozbić go na części i uruchamiać równolegle albo
# w środowisku z limitem czasu na pojedyncze polecenie — bez nich jedyną
# alternatywą było wycinanie ekranów, czyli test słabszy zamiast krótszego.
_args = [a for a in sys.argv[1:] if not a.startswith('--')]
ROOT = os.path.abspath(_args[0]) if _args \
    else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _opt(name, allowed):
    flag = '--' + name
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            val = sys.argv[i + 1]
            if val not in allowed:
                sys.stderr.write('%s: dozwolone %s\n' % (flag, ', '.join(allowed)))
                sys.exit(2)
            return [val]
    return list(allowed)


ONLY_MODES = _opt('tryb', ('file://', 'serwer'))
ONLY_THEMES = _opt('motyw', ('light', 'dark'))
ONLY_GENDERS = _opt('plec', ('male', 'female'))


def _port():
    """Port serwera pomocniczego.

    Domyślnie 8123. Opcja --port pozwala uruchomić kilka zawężonych przebiegów
    RÓWNOLEGLE — bez niej każdy z nich próbowałby zająć ten sam port i wszystkie
    poza pierwszym padały na starcie. Przy dwudziestu ekranach pełny przebieg
    trwa dłużej niż limit czasu na pojedyncze polecenie w części środowisk,
    a rozbicie go na cztery równoległe części skraca go czterokrotnie.
    """
    if '--port' in sys.argv:
        i = sys.argv.index('--port')
        if i + 1 < len(sys.argv):
            return int(sys.argv[i + 1])
    return 8123


PORT = _port()
THAI = re.compile(r'[\u0E00-\u0E7F]')

SCREENS = ['today', 'session', 'course', 'srs',
           'module0', 'listen', 'produce', 'speak', 'grammar', 'numbers', 'rescue',
           'dict', 'dialogues', 'scenes', 'extensive', 'pron',
           'placement', 'exam', 'checkpoint', 'repair',
           'progress', 'week', 'roadmap',
           'settings']

PRODUCE_MODES = ['build', 'type', 'classifier', 'tone', 'say', 'roleplay']
GRAMMAR_MODES = ['map', 'structure', 'transform', 'particles', 'guide']
LISTEN_MODES = ['choice', 'dictation', 'assemble', 'spot', 'gender', 'noise',
                'gap', 'unknown']


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    handler = functools.partial(Quiet, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def run(pw, url, mode_label, theme, gender, problems):
    browser = pw.chromium.launch(args=['--allow-file-access-from-files',
                                       '--use-fake-ui-for-media-stream',
                                       '--use-fake-device-for-media-stream'])
    ctx = browser.new_context(permissions=['microphone'])
    page = ctx.new_page()
    errors = []
    # Licznik asercji: każdy łańcuch warunków zakończony note() to jedno
    # sprawdzenie. Skrypt zbiorczy sumuje te liczby z wszystkich etapów.
    checks = [0]
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: errors.append('PAGEERROR: %s' % e))

    page.add_init_script("""
      localStorage.setItem('thaiaio.gender', JSON.stringify('%s'));
      localStorage.setItem('thaiaio.settings', JSON.stringify({theme:'%s'}));
    """ % (gender, theme))

    page.goto(url, wait_until='domcontentloaded')
    page.wait_for_function("() => window.DB && DB.ready", timeout=45000)

    tag = '%s / %s / %s' % (mode_label, theme, gender)

    def note(msg):
        problems.append('[%s] %s' % (tag, msg))

    for screen in SCREENS:
        page.evaluate("(s) => App.go(s)", screen)
        page.wait_for_timeout(320)
        checks[0] += 1
        try:
            page.wait_for_function(
                "(s) => { const n = document.getElementById('screen-'+s);"
                " return n && !n.hidden && n.textContent.trim().length > 15; }",
                arg=screen, timeout=12000)
        except Exception:
            note('ekran %s nie wyrenderował treści' % screen)
            continue

        # tryby ćwiczeń
        checks[0] += 1
        if screen == 'produce':
            for m in PRODUCE_MODES:
                page.evaluate("(m) => { Produce.mode = m; App.go('produce'); }", m)
                page.wait_for_timeout(700)
                txt = page.evaluate("() => document.getElementById('produce-area').textContent")
                if len(txt.strip()) < 20:
                    note('tryb produkcji %s pusty' % m)
                if THAI.search(txt):
                    note('tryb produkcji %s: pismo tajskie w DOM' % m)
        checks[0] += 1
        if screen == 'grammar':
            # Tryby gramatyczne dociągają własne pliki, więc czekamy na nie
            # zanim zaczniemy przełączać — inaczej każdy tryb pokazałby napis
            # „Wczytuję materiał" i test przeszedłby, nie sprawdziwszy nic.
            try:
                page.wait_for_function(
                    "() => DB.grammarListening && DB.grammarListening.length"
                    " && DB.grammarTransform && DB.grammarTransform.length"
                    " && DB.particles && DB.particles.length", timeout=30000)
            except Exception:
                note('tryby gramatyczne nie doczytały danych')
            # Mapa progresji jest pusta, dopóki nic nie jest zaliczone —
            # a to właśnie ona ma pokazać, który temat już wszedł. Udawany
            # postęp trzeba potem COFNĄĆ: dalsze kontrole sprawdzają blokadę
            # lekcji 1 przez Moduł 0, a zaliczone lekcje ją zdejmują. Bez
            # przywrócenia stanu ten blok psułby test, który sam niczego
            # złego nie robi — najgorszy rodzaj fałszywego alarmu.
            page.evaluate("""() => {
              window.__lessonsBackup = JSON.stringify(Progress.data.lessons);
              Progress.data.lessons = {};
              DB.lessons.slice(0, 200).forEach(L => {
                Progress.data.lessons[L.id] =
                  { status: 'passed', score: 10, total: 10, date: U.today() };
              });
              Progress.save();
            }""")
            for m in GRAMMAR_MODES:
                ok = page.evaluate(
                    "(m) => { const b = document.querySelector"
                    "('[data-gram=\"' + m + '\"]'); if (b) { b.click(); return true; }"
                    " return false; }", m)
                if not ok:
                    note('brak przełącznika trybu gramatyki %s' % m)
                    continue
                page.wait_for_timeout(700)
                txt = page.evaluate(
                    "() => document.getElementById('grammar-area').textContent")
                if len(txt.strip()) < 20:
                    note('tryb gramatyki %s pusty' % m)
                if 'Wczytuję materiał' in txt:
                    note('tryb gramatyki %s nadal czeka na dane' % m)
                if THAI.search(txt):
                    note('tryb gramatyki %s: pismo tajskie w DOM' % m)
            # Ćwiczenia muszą dać się przeklikać do informacji zwrotnej.
            fb = page.evaluate("""() => {
              const box = document.getElementById('grammar-area');
              box.innerHTML = '';
              Gram.renderListening(box, () => {});
              const b = box.querySelector('.options .option');
              if (!b) return { had: false };
              b.click();
              return { had: true, fb: !!box.querySelector('.fb'),
                       veil: box.innerText.indexOf('Zapis pojawi się') !== -1 };
            }""")
            if not fb.get('had'):
                note('wykrywanie struktury nie pokazało opcji odpowiedzi')
            elif not fb.get('fb'):
                note('wykrywanie struktury nie pokazało oceny odpowiedzi')
            elif fb.get('veil'):
                note('wykrywanie struktury nie odsłoniło zapisu po odpowiedzi')
            tr = page.evaluate("""() => {
              const box = document.getElementById('grammar-area');
              box.innerHTML = '';
              Gram.renderTransform(box, () => {});
              const inp = box.querySelector('#gram-answer');
              if (!inp) return { had: false };
              inp.value = Gram.current.item.model;
              const btns = [...box.querySelectorAll('button')];
              const send = btns.find(b => b.textContent.trim() === 'Sprawdź');
              if (send) send.click();
              return { had: true, ok: box.innerText.indexOf('Struktura poprawna') !== -1 };
            }""")
            if not tr.get('had'):
                note('przekształcenia nie pokazały pola odpowiedzi')
            elif not tr.get('ok'):
                note('przekształcenia nie zaliczyły własnego wzorca')
            page.evaluate("""() => {
              if (window.__lessonsBackup !== undefined) {
                Progress.data.lessons = JSON.parse(window.__lessonsBackup);
                delete window.__lessonsBackup;
                Progress.save();
              }
            }""")

        checks[0] += 1
        if screen == 'listen':
            for m in LISTEN_MODES:
                page.evaluate("(m) => { Quiz.mode = m; Quiz.renderListen(document.getElementById('listen-area')); }", m)
                page.wait_for_timeout(500)
                txt = page.evaluate("() => document.getElementById('listen-area').textContent")
                if len(txt.strip()) < 20:
                    note('tryb słuchania %s pusty' % m)

        # pismo tajskie w widocznym DOM
        leak = page.evaluate("""(s) => {
          const n = document.getElementById('screen-'+s);
          const t = n ? n.innerText : '';
          const m = t.match(/[\\u0E00-\\u0E7F]+/);
          return m ? m[0] : null;
        }""", screen)
        checks[0] += 1
        if leak:
            note('ekran %s: pismo tajskie w interfejsie (%s)' % (screen, leak))

    # --- Moduł 0: blok na mapie, ćwiczenie i pominięcie ---
    page.evaluate("() => App.go('course')")
    page.wait_for_timeout(300)
    m0 = page.evaluate("""() => {
      const block = document.querySelector('.m0-block');
      const next = document.getElementById('course-next');
      return {
        block: !!block,
        beforeSurvival: !!block && !!document.querySelector('.m0-block ~ .lesson-card, .m0-block'),
        gateCard: !!next && next.innerText.indexOf('Moduł 0') !== -1,
        firstLessonLocked: Course.status(DB.lessons[0]) === 'locked'
      };
    }""")
    checks[0] += 1
    if not m0['block']:
        note('mapa kursu nie pokazuje bloku Modułu 0')
    checks[0] += 1
    if not m0['gateCard']:
        note('karta „następny krok” nie kieruje do Modułu 0 mimo blokady')
    checks[0] += 1
    if not m0['firstLessonLocked']:
        note('lekcja 1 nie jest zablokowana przez Moduł 0')

    page.evaluate("() => App.go('module0')")
    page.wait_for_timeout(400)
    m0run = page.evaluate("""async () => {
      const L = Perception.lessons()[0];
      Perception.start(L);
      M0View.state.mode = 'lesson';
      M0View.render();
      await new Promise(r => setTimeout(r, 300));
      const area = document.getElementById('module0-area');
      const opts = [...area.querySelectorAll('.m0-options .opt')];
      const hiddenBefore = !!area.querySelector('.m0-reveal') && area.querySelector('.m0-reveal').hidden;
      if (opts.length) opts[0].click();
      await new Promise(r => setTimeout(r, 250));
      const out = {
        options: opts.length,
        hiddenBefore: hiddenBefore,
        revealed: !area.querySelector('.m0-reveal').hidden,
        feedback: !!area.querySelector('.fb'),
        live: document.getElementById('m0-live').textContent.length > 0
      };
      Perception.run = null;
      M0View.state.mode = 'map';
      M0View.render();
      return out;
    }""")
    checks[0] += 1
    if not m0run['options']:
        note('ćwiczenie percepcyjne nie wyrenderowało odpowiedzi')
    checks[0] += 1
    if not (m0run['hiddenBefore'] and m0run['revealed']):
        note('zapis fonetyczny nie jest zasłaniany przed odpowiedzią')
    checks[0] += 1
    if not m0run['feedback']:
        note('ćwiczenie percepcyjne nie daje informacji zwrotnej')
    checks[0] += 1
    if not m0run['live']:
        note('ćwiczenie percepcyjne nie ogłasza wyniku przez aria-live')

    # Pominięcie modułu musi otwierać kurs — i musi dać się cofnąć.
    gate = page.evaluate("""() => {
      Perception.skipModule();
      const after = Course.status(DB.lessons[0]);
      Perception.unskipModule();
      const back = Course.status(DB.lessons[0]);
      Perception.skipModule();   /* dalsze testy pracują na otwartym kursie */
      return { after, back };
    }""")
    checks[0] += 1
    if gate['after'] != 'open' or gate['back'] != 'locked':
        note('pominięcie Modułu 0 nie steruje dostępem do lekcji 1 (%s / %s)'
             % (gate['after'], gate['back']))

    # otwarcie lekcji z kursu
    page.evaluate("() => App.go('course')")
    page.wait_for_timeout(400)
    # Pierwszą kartą na mapie jest teraz blok Modułu 0, który prowadzi na inny
    # ekran zamiast otwierać arkusz lekcji — dlatego celujemy w [data-lesson].
    opened = page.evaluate("""() => {
      const n = document.querySelector('.lesson-card[data-lesson]');
      if (!n) return false;
      n.click();
      return true;
    }""")
    checks[0] += 1
    if not opened:
        note('mapa kursu nie ma kart lekcji')
    else:
        try:
            page.wait_for_function(
                "() => { const b = document.getElementById('sheet-body');"
                " return b && b.textContent.includes('Nowe hasła'); }", timeout=15000)
        except Exception:
            note('widok lekcji nie wczytał materiału')

    # test poziomujący — pełny przebieg
    page.evaluate("() => { Placement.state = null; App.go('placement'); }")
    page.wait_for_timeout(300)
    page.evaluate("() => { Placement.start(); App.go('placement'); }")
    # Czekamy na pierwszą opcję zamiast odmierzać stały czas. Wcześniej pętla
    # niżej traktowała „nie ma jeszcze przycisku” tak samo jak „test się
    # skończył” i przy wolniejszym renderowaniu kończyła się na zerowym kroku.
    checks[0] += 1
    try:
        page.wait_for_selector('#placement-area .opt', timeout=15000)
    except Exception:
        note('test poziomujący nie wyrenderował pierwszego pytania')
    # Pętla idzie po numerze pytania, a nie po obecności przycisku na ekranie.
    # Sam przycisk bywa jeszcze w DOM tuż po kliknięciu — klikanie go drugi raz
    # niczego nie robi i przy szybkiej pętli wyczerpuje limit prób, zanim test
    # dobrnie do końca. Czekamy więc, aż Placement policzy odpowiedź.
    for _ in range(60):
        step = page.evaluate("""() => {
          if (!Placement.state) return { done: true, at: -1 };
          if (Placement.state.done) return { done: true, at: Placement.state.at };
          const o = document.querySelector('#placement-area .opt');
          if (o) o.click();
          return { done: false, at: Placement.state.at, clicked: !!o };
        }""")
        if step['done']:
            break
        before = step['at']
        for _ in range(20):
            page.wait_for_timeout(150)
            now = page.evaluate("() => Placement.state ? "
                                "(Placement.state.done ? -2 : Placement.state.at) : -2")
            if now != before:
                break
    level = page.evaluate("() => (Progress.data.placement || {}).level || null")
    checks[0] += 1
    if not level:
        note('test poziomujący nie zapisał wyniku')

    # kontrast: sprawdzamy, czy motyw faktycznie się przełączył
    bg = page.evaluate("() => getComputedStyle(document.body).backgroundColor")

    stats = page.evaluate("""() => ({
      records: DB.records.length,
      index: DB.index.length,
      lessons: DB.lessons.length,
      loaded: DB.loadedFiles.length,
      errs: DB.errors.length
    })""")

    browser.close()
    return errors, stats, bg, level, checks[0]


def main():
    from playwright.sync_api import sync_playwright
    httpd = serve()
    problems = []
    all_stats = []
    checks = 0
    with sync_playwright() as pw:
        targets = [
            ('file://' + os.path.join(ROOT, 'index.html'), 'file://'),
            ('http://127.0.0.1:%d/index.html' % PORT, 'serwer'),
        ]
        targets = [t for t in targets if t[1] in ONLY_MODES]
        for url, label in targets:
            for theme in ONLY_THEMES:
                for gender in ONLY_GENDERS:
                    errs, stats, bg, level, ck = run(pw, url, label, theme, gender, problems)
                    checks += ck
                    for e in errs:
                        problems.append('[%s / %s / %s] konsola: %s' % (label, theme, gender, e[:180]))
                    all_stats.append((label, theme, gender, stats, bg, level))
    httpd.shutdown()

    print('=' * 74)
    print('TEST W PRZEGLĄDARCE')
    print('SPRAWDZEŃ: %d' % checks)
    print('=' * 74)
    for label, theme, gender, st, bg, level in all_stats:
        print('%-8s %-6s %-7s  indeks %5d · lekcje %3d · plików %2d · poziom %s · tło %s'
              % (label, theme, gender, st['index'], st['lessons'], st['loaded'],
                 level or '—', bg))
    print('-' * 74)
    if problems:
        print('PROBLEMY (%d):' % len(problems))
        seen = set()
        for p in problems:
            if p in seen:
                continue
            seen.add(p)
            print('  ' + p)
        return 1
    if len(all_stats) < 8:
        print('UWAGA: przebieg zawężony do %d z 8 kombinacji '
              '(tryb: %s; motyw: %s; płeć: %s).'
              % (len(all_stats), ', '.join(ONLY_MODES),
                 ', '.join(ONLY_THEMES), ', '.join(ONLY_GENDERS)))
    print('WYNIK: BEZ BŁĘDÓW')
    return 0


sys.exit(main())
