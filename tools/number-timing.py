#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pomiar czasu reakcji w ćwiczeniach liczbowych — na danych testowych.

To NIE jest piąty test. Testy odpowiadają na pytanie „czy działa”; ten
program odpowiada na pytanie „ile to trwa”, i jego wynik jest liczbą, a nie
werdyktem.

CO TU JEST NAPRAWDĘ MIERZONE
----------------------------
Nie da się zmierzyć czasu reakcji człowieka bez człowieka. Zautomatyzowana
przeglądarka odpowiada w kilka milisekund i gdyby wpisać tę wartość do
raportu jako „medianę czasu reakcji”, byłaby to liczba opisująca szybkość
maszyny, a nie opanowanie liczebników.

Mierzymy więc coś, co da się zmierzyć bez człowieka i co ma sens: PODŁOGĘ
POMIARU. Zegar ćwiczenia rusza w chwili wyrenderowania zadania, a bodziec
dźwiękowy potrzebuje czasu na start i na wybrzmienie. Suma tych opóźnień to
minimum, poniżej którego żaden człowiek nie zejdzie — nie dlatego, że jest
wolny, tylko dlatego, że wcześniej po prostu nie usłyszał jeszcze liczby.

Ta podłoga jest potrzebna do jednej konkretnej rzeczy: żeby sprawdzić, czy
progi opanowania zapisane w danych (`masteryMs`) w ogóle są osiągalne. Próg
niższy od podłogi byłby progiem, którego nikt nigdy nie przekroczy, a taki
próg nie mierzy nauki, tylko wyświetla porażkę.

Uruchomienie:
    python3 tools/number-timing.py .
"""

import functools
import http.server
import json
import os
import socketserver
import statistics
import sys
import threading

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Brak playwright. Instalacja: pip install playwright && playwright install chromium")
    sys.exit(2)

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
PORT = int(os.environ.get("TIMING_PORT", "8399"))
ROUNDS = 25


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main():
    handler = functools.partial(Quiet, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:%d/index.html" % PORT)
        page.wait_for_function("() => window.DB && DB.ready", timeout=60000)
        page.evaluate("() => App.go('numbers')")
        page.wait_for_function("() => window.Numbers && Numbers.loaded()", timeout=30000)

        for mode in ["dictation", "price", "clock", "produce", "change", "sequence"]:
            samples = page.evaluate("""(args) => {
              const out = [];
              for (let i = 0; i < args.rounds; i++) {
                const box = document.querySelector('#numbers-area');
                box.innerHTML = '';
                const t0 = performance.now();
                Numbers.RENDER[args.mode](box, function () {});
                // Zegar zadania rusza w środku renderowania; czytamy jego
                // wskazanie zaraz po powrocie z funkcji, czyli w najwcześniejszym
                // momencie, w jakim człowiek mógłby w ogóle zacząć odpowiadać.
                const timer = box.querySelector('.num-timer-text');
                const shown = timer ? timer.textContent : '';
                out.push({ render: performance.now() - t0, shown: shown });
              }
              return out;
            }""", {"mode": mode, "rounds": ROUNDS})
            renders = [s["render"] for s in samples]
            defn = page.evaluate("(m) => Numbers.drillDef(m)", mode)
            rows.append({
                "mode": mode,
                "label": defn["label"],
                "limitMs": defn["limitMs"],
                "masteryMs": defn["masteryMs"],
                "renderMedian": statistics.median(renders),
                "renderMax": max(renders),
            })

        # Ile trwa sam bodziec. Syntezator w środowisku bezgłowym nie mówi,
        # więc bierzemy długość zapisu fonetycznego i tempo mowy przyjęte
        # w warstwie dźwiękowej — to jest oszacowanie, i tak jest opisane.
        speech = page.evaluate("""() => {
          const out = [];
          for (let i = 0; i < 200; i++) {
            const n = Numbers.pickNumber('high');
            const said = Numbers.say(n);
            if (!said) continue;
            const syls = said.thaiPhonetic.split('-').length;
            out.push(syls);
          }
          return out;
        }""")
        browser.close()
    httpd.shutdown()

    # Tempo mowy tajskiej w rejestrze neutralnym to około 4,5 sylaby na
    # sekundę. Przy tempie „wolno” z drabiny z sesji L wychodzi około 3.
    syl_median = statistics.median(speech)
    stimulus_natural = syl_median / 4.5 * 1000
    stimulus_slow = syl_median / 3.0 * 1000

    print("=" * 74)
    print("CZAS REAKCJI W ĆWICZENIACH LICZBOWYCH — POMIAR NA DANYCH TESTOWYCH")
    print("=" * 74)
    print("Mierzona jest PODŁOGA pomiaru, nie czas reakcji człowieka:")
    print("przygotowanie zadania plus wybrzmienie bodźca. Poniżej tej wartości")
    print("nie zejdzie nikt, bo wcześniej nie usłyszał jeszcze liczby.")
    print("-" * 74)
    print("%-26s %9s %9s %9s" % ("ćwiczenie", "render", "próg", "limit"))
    for r in rows:
        print("%-26s %7.1f ms %6d ms %6d ms"
              % (r["label"], r["renderMedian"], r["masteryMs"], r["limitMs"]))
    print("-" * 74)
    print("mediana długości liczby: %.0f sylab" % syl_median)
    print("wybrzmienie bodźca: ~%.0f ms w tempie naturalnym, ~%.0f ms w wolnym"
          % (stimulus_natural, stimulus_slow))
    floor = statistics.median([r["renderMedian"] for r in rows]) + stimulus_natural
    print("PODŁOGA POMIARU: ~%.0f ms" % floor)
    print("-" * 74)

    bad = [r for r in rows if r["masteryMs"] < floor]
    if bad:
        print("PRÓG NIEOSIĄGALNY w: %s" % ", ".join(r["label"] for r in bad))
        print("Próg niższy od podłogi nie mierzy nauki, tylko wyświetla porażkę.")
        return 1
    print("Wszystkie progi opanowania leżą powyżej podłogi pomiaru —")
    print("są więc osiągalne, a zapas nad podłogą to realny czas na decyzję.")
    for r in rows:
        print("  %-24s zapas na decyzję: %5.0f ms" % (r["label"], r["masteryMs"] - floor))
    return 0


sys.exit(main())
