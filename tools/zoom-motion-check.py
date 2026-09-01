#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dostępność przy powiększeniu tekstu do 200% i przy redukcji ruchu.

Uzupełnia a11y-check.py, który bada nazwy dostępne, kolejność focusu,
kontrast i aria-live przy zwykłej wielkości tekstu. Tu sprawdzamy trzy
rzeczy, których tamten nie widzi:

  1. WCAG 1.4.10 (Reflow) — przy tekście powiększonym do 200% treść nie
     wymaga przewijania w dwóch osiach naraz.
  2. Nic interaktywnego nie wychodzi poza prawą krawędź ekranu i żaden
     cel dotykowy nie zapada się poniżej 22 px.
  3. PRZYCINANIE — element, którego zawartość jest szersza niż on sam.
     To groźniejsze od przewijania: do przyciętej treści nie da się
     dojechać. Wykrywamy najgłębsze źródło, nie skutek propagacji.
  4. prefers-reduced-motion — żadna animacja ani przejście nie zostaje
     aktywne, gdy użytkownik prosi o ograniczenie ruchu.

Powiększenie tekstu do 200% odwzorowujemy realnie wąskim widokiem: 200%
tekstu na ekranie 360 px daje ok. 180 px w jednostkach CSS. Jest to
wierniejsze niż właściwość `zoom`, która zaburza pomiar scrollWidth.
"""
import functools
import http.server
import os
import socketserver
import sys
import threading

SCREENS = ['today', 'session', 'course', 'srs',
           'module0', 'listen', 'produce', 'speak', 'grammar', 'numbers', 'rescue',
           'dict', 'dialogues', 'scenes', 'extensive', 'pron',
           'placement', 'exam', 'checkpoint', 'repair',
           'progress', 'week', 'roadmap',
           'settings']

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8711

SHIM = ("Object.defineProperty(window,'speechSynthesis',{configurable:true,value:{"
        "speak(){},cancel(){},resume(){},getVoices:()=>[],addEventListener(){}}});"
        "window.SpeechSynthesisUtterance=function(t){this.text=t;};")

SEED = ("localStorage.setItem('thaiaio.gender',JSON.stringify('male'));"
        "localStorage.setItem('thaiaio.progress',JSON.stringify({placement:{level:'A1',"
        "score:12,total:20,date:'2026-08-20',entryLesson:18}}));")

LAYOUT = """() => {
  const de = document.documentElement, vw = de.clientWidth;
  const out = { over: Math.max(0, de.scrollWidth - vw), past: [], tiny: [], clipped: [] };
  const sec = document.querySelector('#screen-' + App.screen);
  if (!sec) return out;
  const skip = (el) => el.classList.contains('sr-only') || el.closest('.table-scroll');
  for (const el of sec.querySelectorAll('button,a,input,select,textarea,[tabindex]')) {
    if (skip(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const name = (el.textContent || el.id || el.tagName).trim().slice(0, 40);
    if (r.right > vw + 1.5) out.past.push(name + ' [prawa ' + Math.round(r.right) + ']');
    if (r.width > 0 && (r.width < 22 || r.height < 22)) out.tiny.push(name);
  }
  for (const el of sec.querySelectorAll('*')) {
    if (skip(el) || el.clientWidth === 0) continue;
    if (el.scrollWidth <= el.clientWidth + 1) continue;
    let deeper = false;
    for (const c of el.querySelectorAll('*')) {
      if (!skip(c) && c.clientWidth > 0 && c.scrollWidth > c.clientWidth + 1) { deeper = true; break; }
    }
    if (deeper) continue;
    out.clipped.push(el.tagName + '.' + (el.className || '').toString().slice(0, 24)
      + ' (' + el.scrollWidth + ' > ' + el.clientWidth + ' px) | '
      + (el.textContent || '').trim().slice(0, 34));
  }
  return out;
}"""

MOTION = """() => {
  const moving = [];
  for (const el of document.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (cs.animationName && cs.animationName !== 'none')
      moving.push('animacja ' + cs.animationName + ' na ' + (el.id || el.className || el.tagName));
    if (cs.transitionDuration && parseFloat(cs.transitionDuration) > 0)
      moving.push('przejście ' + cs.transitionDuration + ' na ' + (el.id || el.className || el.tagName));
  }
  return moving.slice(0, 5);
}"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    """Serwer statyczny na PORT, a jeśli zajęty — na pierwszym wolnym wyżej.

    Bez `allow_reuse_address` dwa przebiegi pod rząd zderzały się z gniazdem
    w stanie TIME_WAIT po poprzednim: test kończył się `Address already in
    use` zamiast wynikiem. Przy uruchamianiu etapami zdarza się to regularnie,
    bo zadania idą jedno po drugim.
    """
    global PORT
    socketserver.TCPServer.allow_reuse_address = True
    last = None
    for port in range(PORT, PORT + 20):
        try:
            httpd = socketserver.TCPServer(('127.0.0.1', port),
                                           functools.partial(Quiet, directory=ROOT))
        except OSError as e:
            last = e
            continue
        PORT = port
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        return httpd
    raise last


def main():
    from playwright.sync_api import sync_playwright
    httpd = serve()
    problems, checked, checks = [], 0, 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--no-sandbox'])
        passes = [
            ('tekst 200% (telefon)', {'width': 180, 'height': 520}, 'no-preference'),
            ('tekst 200% (tablet)', {'width': 384, 'height': 700}, 'no-preference'),
            ('redukcja ruchu', {'width': 390, 'height': 844}, 'reduce'),
        ]
        for label, viewport, motion in passes:
            ctx = browser.new_context(viewport=viewport, reduced_motion=motion)
            page = ctx.new_page()
            page.add_init_script(SHIM)
            page.add_init_script(SEED)
            page.goto('http://127.0.0.1:%d/index.html' % PORT, wait_until='commit')
            page.wait_for_function('() => window.DB && window.DB.ready && window.App',
                                   timeout=120000)
            for screen in SCREENS:
                page.evaluate('(s) => App.go(s)', screen)
                page.wait_for_timeout(120)
                checked += 1
                # Przebieg z redukcją ruchu bada jedną rzecz; przebiegi
                # z powiększonym tekstem cztery: przewijanie w poziomie,
                # wyjście poza krawędź, wielkość celu i przycięcie treści.
                checks += 1 if motion == 'reduce' else 4
                if motion == 'reduce':
                    for m in page.evaluate(MOTION):
                        problems.append('[%s/%s] ruch mimo prośby o redukcję: %s'
                                        % (label, screen, m))
                    continue
                r = page.evaluate(LAYOUT)
                if r['over'] > 2:
                    problems.append('[%s/%s] przewijanie w poziomie %d px'
                                    % (label, screen, r['over']))
                for x in r['past'][:3]:
                    problems.append('[%s/%s] poza krawędzią: %s' % (label, screen, x))
                for x in r['tiny'][:3]:
                    problems.append('[%s/%s] cel mniejszy niż 22 px: %s' % (label, screen, x))
                for x in r['clipped'][:3]:
                    problems.append('[%s/%s] treść przycięta: %s' % (label, screen, x))
            ctx.close()
        browser.close()
    httpd.shutdown()

    print('=' * 74)
    print('POWIĘKSZENIE TEKSTU I REDUKCJA RUCHU — %d widoków' % checked)
    print('SPRAWDZEŃ: %d' % checks)
    print('=' * 74)
    if problems:
        print('PROBLEMY (%d):' % len(problems))
        for p in problems:
            print('  ' + p)
        return 1
    print('WYNIK: BEZ ZASTRZEŻEŃ')
    return 0


sys.exit(main())
