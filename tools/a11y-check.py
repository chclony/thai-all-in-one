#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Przegląd dostępności — wszystkie ekrany, oba motywy.

Sprawdza automatycznie to, co da się sprawdzić automatycznie:
  1. każdy element interaktywny ma dostępną nazwę,
  2. pola formularzy mają etykietę,
  3. nic interaktywnego nie wypada z kolejności focusu (tabindex ujemny
     na elemencie, który powinien być osiągalny klawiaturą),
  4. focus jest widoczny (obrys w stanie :focus-visible),
  5. kontrast tekstu do tła spełnia WCAG AA (4.5:1, a 3:1 dla dużego tekstu)
     w obu motywach — także w karcie oceny wymowy, którą wstrzykujemy na
     ekran, bo bez mikrofonu nie powstałaby sama,
  6. przełączniki mają aria-pressed, listy wyników aria-live,
  7. nagłówki nie przeskakują poziomów.
"""
import sys, os, re, json, threading, http.server, socketserver, functools

# Argumenty: katalog projektu, a dalej opcjonalne zawężenia przebiegu.
#
#   python3 tools/a11y-check.py .                    oba motywy, 24 ekrany
#   python3 tools/a11y-check.py . --motyw dark       tylko ciemny motyw
#   python3 tools/a11y-check.py . --ekrany today,srs tylko wskazane ekrany
#   python3 tools/a11y-check.py . --port 8156        inny port
#
# Zawężenia istnieją po to, żeby przebieg dało się pociąć na kawałki
# mieszczące się w limicie czasu pojedynczego polecenia. Bez nich jedyną
# alternatywą było wycinanie ekranów na stałe, czyli test słabszy zamiast
# krótszego.
_ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
ROOT = os.path.abspath(_ARGS[0]) if _ARGS \
    else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _flag(name, default=None):
    flag = '--' + name
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


PORT = int(_flag('port', 8155))

SCREENS = ['today', 'session', 'course', 'srs',
           'module0', 'listen', 'produce', 'speak', 'grammar', 'numbers', 'rescue',
           'dict', 'dialogues', 'scenes', 'extensive', 'pron',
           'placement', 'exam', 'checkpoint', 'repair',
           'progress', 'week', 'roadmap',
           'settings']

_ONLY_SCREENS = _flag('ekrany')
if _ONLY_SCREENS:
    want = [x.strip() for x in _ONLY_SCREENS.split(',') if x.strip()]
    unknown = [x for x in want if x not in SCREENS]
    if unknown:
        sys.stderr.write('--ekrany: nieznane ekrany: %s\n' % ', '.join(unknown))
        sys.exit(2)
    SCREENS = [s for s in SCREENS if s in want]

_ONLY_THEME = _flag('motyw')
THEMES = ('light', 'dark')
if _ONLY_THEME:
    if _ONLY_THEME not in THEMES:
        sys.stderr.write('--motyw: dozwolone light, dark\n')
        sys.exit(2)
    THEMES = (_ONLY_THEME,)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    """Serwer statyczny; przy zajętym porcie schodzi na pierwszy wolny wyżej."""
    global PORT
    handler = functools.partial(Quiet, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    last = None
    for port in range(PORT, PORT + 20):
        try:
            httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
        except OSError as e:
            last = e
            continue
        PORT = port
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        return httpd
    raise last


AUDIT_JS = r"""
(screen) => {
  const out = { names: [], labels: [], focus: [], contrast: [], live: [], headings: [] };
  const root = document.getElementById('screen-' + screen);
  if (!root) return out;

  const INTERACTIVE = 'button, a[href], input, select, textarea, [tabindex]';

  function accName(el) {
    const aria = el.getAttribute('aria-label');
    if (aria && aria.trim()) return aria.trim();
    const by = el.getAttribute('aria-labelledby');
    if (by) {
      const t = by.split(/\s+/).map(id => {
        const n = document.getElementById(id);
        return n ? n.textContent : '';
      }).join(' ').trim();
      if (t) return t;
    }
    if (el.id) {
      const lab = document.querySelector('label[for="' + CSS.escape(el.id) + '"]');
      if (lab && lab.textContent.trim()) return lab.textContent.trim();
    }
    if (el.closest('label')) return el.closest('label').textContent.trim();
    const title = el.getAttribute('title');
    if (title && title.trim()) return title.trim();
    return (el.textContent || '').trim();
  }

  function visible(el) {
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }

  // --- 1 i 2: nazwy dostępne i etykiety pól ---
  root.querySelectorAll(INTERACTIVE).forEach(el => {
    if (!visible(el)) return;
    const name = accName(el);
    const desc = el.tagName.toLowerCase() + (el.id ? '#' + el.id : '')
      + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/)[0] : '');
    if (!name) out.names.push(desc);
    if (/^(input|select|textarea)$/.test(el.tagName.toLowerCase()) && !name) {
      out.labels.push(desc);
    }
    // --- 3: kolejność focusu ---
    const ti = el.getAttribute('tabindex');
    if (ti !== null && parseInt(ti, 10) < 0 && !el.disabled) {
      out.focus.push(desc + ' (tabindex=' + ti + ')');
    }
    if (ti !== null && parseInt(ti, 10) > 0) {
      out.focus.push(desc + ' (tabindex dodatni ' + ti + ' — łamie naturalną kolejność)');
    }
  });

  // --- 5: kontrast ---
  function toRgb(str) {
    const m = str.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(',').map(x => parseFloat(x));
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }
  function lum(c) {
    const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
  }
  function bgOf(el) {
    let n = el;
    while (n && n !== document.documentElement) {
      const c = toRgb(getComputedStyle(n).backgroundColor);
      if (c && c.a > 0.9) return c;
      n = n.parentElement;
    }
    return toRgb(getComputedStyle(document.body).backgroundColor);
  }
  function ratio(a, b) {
    const l1 = lum(a), l2 = lum(b);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  }

  const seen = new Set();
  root.querySelectorAll('*').forEach(el => {
    if (!visible(el)) return;
    const own = Array.from(el.childNodes)
      .filter(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (!own.length) return;
    const s = getComputedStyle(el);
    // Tekst w SVG bierze kolor z właściwości fill, nie color. Czytanie samego
    // `color` dawało fałszywy wynik pozytywny: podpisy osi na wykresach nigdy
    // nie były naprawdę sprawdzane.
    const isSvgText = el.namespaceURI === 'http://www.w3.org/2000/svg';
    const paint = (isSvgText && s.fill && s.fill !== 'none') ? s.fill : s.color;
    const fg = toRgb(paint), bg = bgOf(el);
    if (!fg || !bg) return;
    const size = parseFloat(s.fontSize);
    const bold = parseInt(s.fontWeight, 10) >= 700;
    const large = size >= 24 || (size >= 18.66 && bold);
    const need = large ? 3.0 : 4.5;
    const r = ratio(fg, bg);
    if (r < need) {
      const key = s.color + '|' + s.fontSize + '|' + el.className;
      if (seen.has(key)) return;
      seen.add(key);
      out.contrast.push({
        sel: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string'
          ? '.' + el.className.trim().split(/\s+/).join('.') : ''),
        ratio: Math.round(r * 100) / 100,
        need: need,
        sample: own[0].textContent.trim().slice(0, 40)
      });
    }
  });

  // --- 6: przełączniki i obszary żywe ---
  root.querySelectorAll('.chip, [data-produce], [data-listen]').forEach(el => {
    if (!visible(el)) return;
    if (!el.hasAttribute('aria-pressed')) {
      out.live.push('przełącznik bez aria-pressed: ' + (el.textContent || '').trim().slice(0, 30));
    }
  });

  // --- 7: poziomy nagłówków ---
  let prev = 0;
  root.querySelectorAll('h1,h2,h3,h4').forEach(h => {
    if (!visible(h)) return;
    const lvl = parseInt(h.tagName[1], 10);
    if (prev && lvl > prev + 1) {
      out.headings.push('skok z h' + prev + ' do h' + lvl + ': ' + h.textContent.trim().slice(0, 40));
    }
    prev = lvl;
  });

  return out;
}
"""

# Obrys focusu trzeba sprawdzić na elemencie NAPRAWDĘ sfokusowanym klawiszem.
# getComputedStyle(el, ':focus-visible') nie działa — to pseudoklasa, nie
# pseudoelement, i przeglądarka zwraca dla niej style zwykłego stanu.
FOCUS_STATE_JS = r"""
() => {
  const el = document.activeElement;
  if (!el || el === document.body) return null;
  const s = getComputedStyle(el);
  const outline = s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0;
  const shadow = s.boxShadow && s.boxShadow !== 'none';
  return {
    tag: el.tagName.toLowerCase() + (el.id ? '#' + el.id : ''),
    visible: !!(outline || shadow),
    inScreen: !!el.closest('.screen:not([hidden])') || !!el.closest('header, nav, footer')
  };
}
"""

REACHABLE_JS = r"""
(screen) => {
  const root = document.getElementById('screen-' + screen);
  if (!root) return { count: 0 };
  const items = Array.from(root.querySelectorAll(
    'button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), textarea'))
    .filter(el => {
      const s = getComputedStyle(el);
      if (s.display === 'none' || s.visibility === 'hidden') return false;
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    });
  return { count: items.length };
}
"""


def main():
    from playwright.sync_api import sync_playwright
    httpd = serve()
    problems = []
    checked = 0
    checks = 0

    with sync_playwright() as pw:
        for theme in THEMES:
            browser = pw.chromium.launch()
            ctx = browser.new_context()
            page = ctx.new_page()
            page.add_init_script("""
              localStorage.setItem('thaiaio.gender', JSON.stringify('male'));
              localStorage.setItem('thaiaio.settings', JSON.stringify({theme:'%s'}));
              localStorage.setItem('thaiaio.progress', JSON.stringify({
                days:{}, streak:0, bestStreak:0, lastDay:null, totalAnswers:0,
                totalCorrect:0, minutes:0, seen:{}, favourites:{}, lists:{}, goal:20,
                lessons:{}, errors:{category:{},grammar:{},type:{},mode:{}},
                perception:{lessons:{},contrasts:{},history:[],diagnostic:null,skipped:false},
                placement:{level:'A1',score:18,total:28,date:'2026-01-01',entryLesson:'lesson-023'}
              }));
            """ % theme)
            page.goto('http://127.0.0.1:%d/index.html' % PORT, wait_until='domcontentloaded')
            page.wait_for_function("() => window.DB && DB.ready", timeout=45000)

            for screen in SCREENS:
                page.evaluate("(s) => App.go(s)", screen)
                page.wait_for_timeout(700)

                # Karta oceny wymowy pojawia się dopiero po nagraniu, więc
                # w przeglądzie automatycznym wstawiamy przykładowy wynik.
                # Inaczej najbardziej złożony nowy widok nigdy nie zostałby
                # sprawdzony pod kątem kontrastu i nazw dostępnych.
                # Moduł 0 sprawdzamy dwa razy: mapę modułu i samo ćwiczenie
                # po udzieleniu odpowiedzi. Ćwiczenie jest tu najważniejsze —
                # to ono musi dać się obsłużyć bez patrzenia na ekran, a mapa
                # nie pokazuje ani opcji odpowiedzi, ani informacji zwrotnej.
                if screen == 'module0':
                    page.evaluate("""() => {
                      const L = Perception.lessons()[0];
                      Perception.start(L);
                      M0View.state.mode = 'lesson';
                      M0View.render();
                    }""")
                    page.wait_for_timeout(400)
                    page.evaluate("""() => {
                      const t = Perception.current();
                      const btns = [...document.querySelectorAll('#module0-area .m0-options .opt')];
                      const hit = btns.find(b => b.getAttribute('aria-label').endsWith(': ' + t.answer));
                      if (hit) hit.click();
                    }""")
                    page.wait_for_timeout(350)

                # Ćwiczenia liczbowe i dryl odruchu mają odliczanie, pole
                # tekstowe i informację zwrotną — i wszystko to musi dać się
                # obsłużyć bez patrzenia na ekran. Sam wejściowy stan ekranu
                # sprawdziłby połowę widoku, więc przechodzimy przez trzy
                # tryby liczbowe różniące się sposobem odpowiadania (wpisanie,
                # wybór, ustawianie) i przez dryl po udzieleniu odpowiedzi.
                if screen == 'numbers':
                    for mode in ('price', 'clock', 'dictation'):
                        page.evaluate("""(m) => {
                          const chip = [...document.querySelectorAll('#numbers-modes .chip')]
                            .find(c => c.textContent && c.textContent.length);
                          window.__numMode = m;
                        }""", mode)
                    page.evaluate("""() => {
                      const box = document.querySelector('#numbers-area');
                      box.innerHTML = '';
                      Numbers.renderPrice(box, function () {});
                    }""")
                    page.wait_for_timeout(400)
                    page.evaluate("""() => {
                      const b = document.querySelector('#numbers-area .options .option');
                      if (b) b.click();
                    }""")
                    page.wait_for_timeout(400)

                if screen == 'rescue':
                    page.evaluate("""() => {
                      const b = document.querySelector('#rescue-area .options .option');
                      if (b) b.click();
                    }""")
                    page.wait_for_timeout(500)

                # Ekran gramatyki sprawdzamy w stanie ĆWICZENIA, nie na mapie
                # progresji. Mapa to lista do czytania; dopiero ćwiczenie ma
                # opcje odpowiedzi, informację zwrotną i pole tekstowe, czyli
                # wszystko, co musi dać się obsłużyć bez patrzenia na ekran.
                # Bierzemy wykrywanie struktury po udzieleniu odpowiedzi,
                # bo tam odsłania się zasłonięty zapis — a odsłonięcie jest
                # zmianą treści, którą czytnik ekranu musi ogłosić.
                if screen == 'grammar':
                    # Pliki trybów dociągają się na żądanie. Bez czekania
                    # audyt trafiłby na napis „Wczytuję materiał" i przeszedłby
                    # bez sprawdzenia czegokolwiek — czyli najgorszy możliwy
                    # wynik: zielony, a nic nie zbadany.
                    page.wait_for_function(
                        "() => DB.grammarListening && DB.grammarListening.length",
                        timeout=45000)
                    page.evaluate("""() => {
                      Progress.data.lessons = {};
                      DB.lessons.slice(0, 200).forEach(L => {
                        Progress.data.lessons[L.id] =
                          { status: 'passed', score: 10, total: 10, date: U.today() };
                      });
                      Progress.save();
                      const box = document.getElementById('grammar-area');
                      box.innerHTML = '';
                      Gram.axis = 'intent';
                      Gram.renderListening(box, () => {});
                    }""")
                    page.wait_for_timeout(400)
                    rendered = page.evaluate("""() => {
                      const b = document.querySelector('#grammar-area .options .option');
                      if (b) b.click();
                      return !!b;
                    }""")
                    if not rendered:
                        problems.append(
                            '  %s/%s: ćwiczenie wykrywania struktury nie '
                            'wyrenderowało opcji — audyt nie miał czego '
                            'sprawdzić' % (screen, theme))
                    page.wait_for_timeout(350)

                if screen == 'speak':
                    page.evaluate("""() => {
                      const box = document.getElementById('speak-area');
                      if (box && window.PronView && !box.querySelector('.pron-result')) {
                        box.appendChild(PronView.render(PronView.sampleResult()));
                      }
                    }""")
                    page.wait_for_timeout(250)
                checked += 1
                res = page.evaluate(AUDIT_JS, screen)

                # Kolejność focusu i widoczność obrysu: przechodzimy
                # tabulatorem przez pierwsze pozycje ekranu tak, jak zrobiłby
                # to ktoś korzystający wyłącznie z klawiatury.
                reach = page.evaluate(REACHABLE_JS, screen)
                kb = {'reachable': True, 'outline': True}
                if reach['count']:
                    page.evaluate("(s) => { const r = document.getElementById('screen-'+s);"
                                  " const f = r.querySelector('button:not([disabled]), a[href],"
                                  " input:not([disabled]), select:not([disabled])');"
                                  " if (f) f.focus(); }", screen)
                    steps = min(reach['count'], 8)
                    seen_focus = []
                    for _ in range(steps):
                        st = page.evaluate(FOCUS_STATE_JS)
                        if st:
                            seen_focus.append(st)
                            if not st['visible']:
                                kb['outline'] = False
                        page.keyboard.press('Tab')
                        page.wait_for_timeout(40)
                    if not seen_focus:
                        kb['reachable'] = False

                tag = '%s / %s' % (theme, screen)
                # Osiem kontroli na widok: nazwy dostępne, etykiety pól,
                # kolejność focusu, aria-live, poziomy nagłówków, kontrast,
                # osiągalność klawiaturą i widoczny obrys focusu.
                checks += 8
                for n in res['names']:
                    problems.append('[%s] element bez dostępnej nazwy: %s' % (tag, n))
                for n in res['labels']:
                    problems.append('[%s] pole bez etykiety: %s' % (tag, n))
                for n in res['focus']:
                    problems.append('[%s] kolejność focusu: %s' % (tag, n))
                for n in res['live']:
                    problems.append('[%s] %s' % (tag, n))
                for n in res['headings']:
                    problems.append('[%s] nagłówki: %s' % (tag, n))
                for c in res['contrast']:
                    problems.append('[%s] kontrast %.2f:1 (wymagane %.1f) — %s — „%s”'
                                    % (tag, c['ratio'], c['need'], c['sel'], c['sample']))
                if not kb.get('reachable'):
                    problems.append('[%s] pierwszy element nie przyjmuje focusu' % tag)
                if not kb.get('outline'):
                    problems.append('[%s] focus bez widocznego obrysu' % tag)

            browser.close()

    httpd.shutdown()
    print('=' * 74)
    print('PRZEGLĄD DOSTĘPNOŚCI — %d widoków (%d ekranów × %d motywy)'
          % (checked, len(SCREENS), len(THEMES)))
    print('SPRAWDZEŃ: %d' % checks)
    print('=' * 74)
    if problems:
        uniq = []
        for p in problems:
            if p not in uniq:
                uniq.append(p)
        print('DO POPRAWY (%d):' % len(uniq))
        for p in uniq:
            print('  ' + p)
        return 1
    print('WYNIK: BEZ ZASTRZEŻEŃ')
    return 0


sys.exit(main())
