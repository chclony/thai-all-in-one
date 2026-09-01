#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dowód, że pismo tajskie nie dociera do uczącego się.

Projekt obiecuje jedno: uczący się NIGDY nie widzi znaków tajskich. Do tej
pory ta obietnica była w raportach zdaniem oznajmującym. Zdanie oznajmujące
nie jest dowodem — to narzędzie ma nim być.

Obietnica jest dziurawa dokładnie w trzech miejscach i każde sprawdzamy
osobno, bo każde może pęknąć niezależnie:

  1. DANE. W bazie pismo tajskie JEST — w polu `ttsThai`, bo syntezator mowy
     musi dostać tekst tajski, inaczej nic nie powie. Umowa brzmi: to pole
     jest jedynym miejscem, w którym wolno mu być. Sprawdzenie przechodzi po
     KAŻDYM polu KAŻDEGO rekordu we wszystkich plikach danych i pilnuje, żeby
     znak tajski nie pojawił się nigdzie indziej. Lista pól zwolnionych jest
     zamknięta i wypisana niżej — nowe pole z tajskim obleje test, dopóki
     ktoś świadomie go tu nie dopisze.

  2. INTERFEJS. Pole `ttsThai` może być czyste w danych, a mimo to trafić do
     ekranu, bo ktoś wyrenderował rekord w całości. Sprawdzenie ładuje
     aplikację w przeglądarce, obchodzi wszystkie ekrany i wszystkie tryby
     ćwiczeń i czyta WIDOCZNY tekst (`innerText`, nie `innerHTML` — liczy się
     to, co widzi oko).

  3. EKSPORTY. Uczący się może wynieść z aplikacji dwie rzeczy: talię do Anki
     (CSV) i kopię postępu (JSON). Jedno i drugie ogląda się poza aplikacją,
     więc filtr widoku już nie zadziała. Sprawdzenie wywołuje obie funkcje
     eksportu na REALNYM materiale i skanuje wynik.

Uruchomienie:

    python3 tools/thai-script-check.py            wszystkie trzy etapy
    python3 tools/thai-script-check.py --dane     tylko dane (bez przeglądarki)
    python3 tools/thai-script-check.py --json X   zapisz wynik do pliku

Kod wyjścia 0 = obietnica dotrzymana. Cokolwiek innego = złamana.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')

# Pismo tajskie plus znaki tajskie w bloku rozszerzonym.
THAI = re.compile(r'[\u0E00-\u0E7F]')

# Jedyne pola, w których pismo tajskie jest dozwolone. Klucz to nazwa pola
# na dowolnym poziomie zagnieżdżenia. Świadomie NIE ma tu wildcardów —
# zwolnienie ma być decyzją, a nie efektem ubocznym wzorca.
ALLOWED_FIELDS = {
    'ttsThai',      # wejście syntezatora mowy
    'thaiScript',   # pole źródłowe w wykazie klasyfikatorów
}


# ------------------------------------------------------------------ [1] dane

def walk(node, path, hits, allowed_depth=False):
    """Rekurencyjny przegląd struktury JSON w poszukiwaniu znaków tajskich."""
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, path + '.' + k, hits, allowed_depth or k in ALLOWED_FIELDS)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, '%s[%d]' % (path, i), hits, allowed_depth)
    elif isinstance(node, str):
        if not allowed_depth and THAI.search(node):
            hits.append((path, node[:60]))


def check_data():
    print('[1] DANE — pismo tajskie poza polami zwolnionymi')
    files = sorted(f for f in os.listdir(DATA) if f.endswith('.json'))
    hits, scanned, allowed_hits = [], 0, 0
    for fn in files:
        with open(os.path.join(DATA, fn), encoding='utf-8') as fh:
            doc = json.load(fh)
        before = len(hits)
        walk(doc, fn, hits)
        scanned += 1
        if len(hits) > before:
            print('    %-32s %d wycieków' % (fn, len(hits) - before))

    # Ile razy tajski wystąpił w miejscu dozwolonym — dla porównania skali.
    for fn in files:
        with open(os.path.join(DATA, fn), encoding='utf-8') as fh:
            raw = fh.read()
        allowed_hits += len(THAI.findall(raw))

    print('    plików przeskanowanych              %6d' % scanned)
    print('    znaków tajskich w plikach łącznie   %6d' % allowed_hits)
    print('    pola zwolnione                      %s' % ', '.join(sorted(ALLOWED_FIELDS)))
    print('    WYCIEKI POZA POLA ZWOLNIONE         %6d' % len(hits))
    for p, s in hits[:10]:
        print('      %s -> %s' % (p, s))
    return {'files': scanned, 'thaiCharsTotal': allowed_hits,
            'leaks': len(hits), 'examples': hits[:10]}


# ------------------------------------------- [2] interfejs i [3] eksporty

SCREENS = ['today', 'session', 'course', 'srs',
           'module0', 'listen', 'produce', 'speak', 'grammar', 'numbers',
           'rescue', 'dict', 'dialogues', 'scenes', 'extensive', 'pron',
           'placement', 'exam', 'checkpoint', 'repair',
           'progress', 'week', 'roadmap', 'settings']

PRODUCE_MODES = ['build', 'type', 'classifier', 'tone', 'say', 'roleplay']
GRAMMAR_MODES = ['map', 'structure', 'transform', 'particles', 'guide']
LISTEN_MODES = ['choice', 'dictation', 'assemble', 'spot', 'gender', 'noise',
                'gap', 'unknown']


def check_browser(port):
    import functools
    import http.server
    import socketserver
    import threading
    from playwright.sync_api import sync_playwright

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

    handler = functools.partial(Quiet, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(('127.0.0.1', port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    ui_leaks, export_leaks = [], []
    checked_screens = 0
    stats = {}

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--no-sandbox'])
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto('http://127.0.0.1:%d/index.html' % port,
                  wait_until='domcontentloaded')
        page.wait_for_function('() => window.DB && DB.ready', timeout=60000)

        print('\n[2] INTERFEJS — widoczny tekst na wszystkich ekranach')
        for screen in SCREENS:
            page.evaluate('(s) => App.go(s)', screen)
            page.wait_for_timeout(300)
            checked_screens += 1
            modes = []
            if screen == 'produce':
                modes = [('Produce', m) for m in PRODUCE_MODES]
            elif screen == 'grammar':
                modes = [('Grammar', m) for m in GRAMMAR_MODES]
            elif screen == 'listen':
                modes = [('Listen', m) for m in LISTEN_MODES]

            passes = [None] + modes
            for entry in passes:
                if entry:
                    obj, m = entry
                    page.evaluate(
                        '([o,m,s]) => { if (window[o]) { window[o].mode = m; }'
                        ' App.go(s); }', [obj, m, screen])
                    page.wait_for_timeout(500)
                txt = page.evaluate(
                    "(s) => { const n = document.getElementById('screen-'+s);"
                    ' return n ? (n.innerText || n.textContent || "") : ""; }',
                    screen)
                found = THAI.findall(txt or '')
                if found:
                    label = screen if not entry else '%s/%s' % (screen, entry[1])
                    ui_leaks.append((label, ''.join(found[:20])))

        # Pasek nawigacji, nagłówek, stopka — wszystko poza kontenerem ekranu.
        chrome_txt = page.evaluate(
            '() => document.body.innerText || document.body.textContent || ""')
        if THAI.search(chrome_txt or ''):
            ui_leaks.append(('obudowa aplikacji',
                             ''.join(THAI.findall(chrome_txt)[:20])))

        print('    ekranów sprawdzonych                %6d' % checked_screens)
        print('    trybów ćwiczeń dodatkowo            %6d'
              % (len(PRODUCE_MODES) + len(GRAMMAR_MODES) + len(LISTEN_MODES)))
        print('    WYCIEKI W INTERFEJSIE               %6d' % len(ui_leaks))
        for s, t in ui_leaks[:10]:
            print('      %s -> %s' % (s, t))

        print('\n[3] EKSPORTY DLA UCZĄCEGO SIĘ')

        # --- eksport CSV do Anki, na realnym materiale ---------------------
        csv_info = page.evaluate("""
          async () => {
            const ids = (DB.index || []).slice(0, 1200).map(r => r.id);
            await DB.ensureFor(ids);
            const csv = Stats.buildCsv(ids);
            return { rows: ids.length, len: csv.length, csv: csv };
          }
        """)
        csv_found = THAI.findall(csv_info['csv'])
        if csv_found:
            export_leaks.append(('CSV do Anki', ''.join(csv_found[:20])))
        print('    CSV do Anki: rekordów %d, znaków %d, wycieków %d'
              % (csv_info['rows'], csv_info['len'], len(csv_found)))

        # --- eksport postępu, po sztucznym zapełnieniu kartoteki -----------
        # Kartoteka i dziennik muszą być NIEPUSTE, inaczej test przechodzi
        # dlatego, że nie ma czego wyeksportować, a nie dlatego, że eksport
        # jest czysty. Dlatego najpierw zakładamy karty i ocenimy część z nich.
        prog_info = page.evaluate("""
          () => {
            const ids = (DB.index || []).slice(0, 400).map(r => r.id);
            ids.forEach(id => SRS.addBoth(id));
            /* Dwa przejścia, nie jedno: dziennik powtórek dostaje wpis
               dopiero przy DRUGIM podejściu do karty, bo pierwsze nie ma
               jeszcze przerwy do zmierzenia. Po jednym przejściu dziennik
               zostałby pusty i etap eksportu przechodziłby dlatego, że nie
               ma czego skanować. */
            ids.slice(0, 120).forEach((id, i) => SRS.grade(id, 3 + (i % 3)));
            ids.slice(0, 120).forEach((id, i) => SRS.grade(id, 3 + (i % 3)));
            const payload = JSON.stringify(Progress.exportData());
            return { cards: Object.keys(SRS.cards || {}).length,
                     logged: (SRS.log || []).length,
                     len: payload.length, payload: payload };
          }
        """)
        prog_found = THAI.findall(prog_info['payload'])
        if prog_found:
            export_leaks.append(('kopia postępu JSON',
                                 ''.join(prog_found[:20])))
        print('    Kopia postępu JSON: kart %d, wpisów dziennika %d, znaków %d,'
              ' wycieków %d' % (prog_info['cards'], prog_info['logged'],
                                prog_info['len'], len(prog_found)))

        # --- indeks wyszukiwarki: to, co widać w słowniku ------------------
        idx_info = page.evaluate("""
          () => {
            const s = JSON.stringify(DB.index || []);
            return { entries: (DB.index || []).length, len: s.length, s: s };
          }
        """)
        idx_found = THAI.findall(idx_info['s'])
        if idx_found:
            export_leaks.append(('indeks wyszukiwarki',
                                 ''.join(idx_found[:20])))
        print('    Indeks wyszukiwarki: pozycji %d, znaków %d, wycieków %d'
              % (idx_info['entries'], idx_info['len'], len(idx_found)))

        stats = {
            'screens': checked_screens,
            'csvRows': csv_info['rows'], 'csvChars': csv_info['len'],
            'progressCards': prog_info['cards'],
            'progressLog': prog_info['logged'],
            'progressChars': prog_info['len'],
            'indexEntries': idx_info['entries'],
        }

        browser.close()
    httpd.shutdown()

    return {'uiLeaks': len(ui_leaks), 'uiExamples': ui_leaks[:10],
            'exportLeaks': len(export_leaks),
            'exportExamples': export_leaks[:10], **stats}


def main():
    only_data = '--dane' in sys.argv
    out_path = None
    if '--json' in sys.argv:
        i = sys.argv.index('--json')
        if i + 1 < len(sys.argv):
            out_path = sys.argv[i + 1]
    port = 8199
    if '--port' in sys.argv:
        i = sys.argv.index('--port')
        if i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])

    print('=' * 74)
    print('KONTROLA PISMA TAJSKIEGO — interfejs i eksporty dla uczącego się')
    print('=' * 74)

    result = {'data': check_data()}
    if not only_data:
        result['browser'] = check_browser(port)

    total = result['data']['leaks']
    if 'browser' in result:
        total += result['browser']['uiLeaks'] + result['browser']['exportLeaks']

    # Liczba asercji dla skryptu zbiorczego: dane + ekrany + tryby + eksporty.
    checks = result['data']['files']
    if 'browser' in result:
        checks += (result['browser']['screens']
                   + len(PRODUCE_MODES) + len(GRAMMAR_MODES)
                   + len(LISTEN_MODES) + 3)

    print('\n' + '-' * 74)
    print('SPRAWDZEŃ: %d' % checks)
    print('WYCIEKÓW ŁĄCZNIE: %d' % total)
    print('WYNIK:', 'PISMO TAJSKIE NIE DOCIERA DO UCZĄCEGO SIĘ' if total == 0
          else 'OBIETNICA ZŁAMANA')

    result['checks'] = checks
    result['leaksTotal'] = total
    if out_path:
        with open(out_path, 'w', encoding='utf-8') as fh:
            json.dump(result, fh, ensure_ascii=False, indent=1)

    return 0 if total == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
