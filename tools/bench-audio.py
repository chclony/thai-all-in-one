#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pomiary warstwy dźwiękowej.

    python3 tools/bench-audio.py .           # pełny pomiar
    python3 tools/bench-audio.py . 11        # 11 prób zamiast 7

CO MIERZYMY

1. OPÓŹNIENIE ODTWARZANIA — od kliknięcia „Odtwórz” do pierwszego dźwięku,
   w obu trybach (file:// i serwer), na zimno i na ciepło, w trzech tempach.

   Silnika mowy w przeglądarce headless nie ma, więc podstawiamy atrapę,
   która zgłasza dźwięk w następnej klatce. Mierzona liczba to koszt SAMEJ
   APLIKACJI — jedyny, na który mamy wpływ. Realny silnik systemowy dokłada
   do tego swoje opóźnienie; ile, mówi docs/ograniczenia-tts.md.

2. PAMIĘĆ PODRĘCZNA — ile daje trzymanie gotowych buforów.

   Osobno dla dwóch rzeczy, które naprawdę kosztują:
     * generowanie ośmiosekundowego szumu tła (miliony operacji),
     * dekodowanie nagrania i rozciągnięcie go w czasie.

   Do drugiego pomiaru bench sam tworzy nagranie kontrolne w audio/ i kasuje
   je po sobie — inaczej nie byłoby czego dekodować, bo nagrań lektorskich
   w projekcie nie ma.
"""
import functools
import http.server
import math
import os
import socketserver
import statistics
import struct
import sys
import threading

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 \
    else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = int(sys.argv[2]) if len(sys.argv) > 2 else 7
PORT = 8127
BENCH_WAV = os.path.join(ROOT, "audio", "_bench.wav")

SHIM = r"""
window.__bench = { events: [] };
(function () {
  var voices = [
    { name: 'Bench Thai', lang: 'th-TH', localService: true, default: true },
    { name: 'Bench Thai Two', lang: 'th-TH', localService: true }
  ];
  var fake = {
    speaking: false, paused: false, pending: false,
    getVoices: function () { return voices; },
    addEventListener: function () {},
    removeEventListener: function () {},
    cancel: function () {}, resume: function () {}, pause: function () {},
    speak: function (u) {
      window.__bench.events.push({ kind: 'speak', t: performance.now() });
      requestAnimationFrame(function () {
        window.__bench.events.push({ kind: 'start', t: performance.now() });
        if (u.onstart) u.onstart({});
        setTimeout(function () { if (u.onend) u.onend({}); }, 4);
      });
    }
  };
  Object.defineProperty(window, 'speechSynthesis', { configurable: true, value: fake });
  window.SpeechSynthesisUtterance = function (t) {
    this.text = t; this.rate = 1; this.pitch = 1; this.volume = 1; this.lang = 'th-TH';
  };
})();
"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    handler = functools.partial(Quiet, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def make_wav(path, seconds=2.0, sr=44100, f0=140.0):
    """Nagranie kontrolne: ton krtaniowy z formantami i obwiednią sylabową.

    Nie udaje mowy tajskiej — ma tylko obciążyć dekoder i algorytm rozciągania
    tak, jak obciążyłoby je prawdziwe zdanie o tej samej długości.
    """
    n = int(sr * seconds)
    frames = bytearray()
    for i in range(n):
        t = i / sr
        p = 2 * math.pi * f0 * t
        s = (math.sin(p) + 0.5 * math.sin(2 * p) + 0.3 * math.sin(3 * p)
             + 0.2 * math.sin(5 * p))
        env = 0.35 + 0.35 * math.sin(2 * math.pi * 3.5 * t)
        frames += struct.pack("<h", int(max(-1, min(1, s * env * 0.45)) * 32767))
    data = bytes(frames)
    with open(path, "wb") as fh:
        fh.write(b"RIFF" + struct.pack("<I", 36 + len(data)) + b"WAVE")
        fh.write(b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, sr, sr * 2, 2, 16))
        fh.write(b"data" + struct.pack("<I", len(data)) + data)


# --- 1. opóźnienie odtwarzania ---------------------------------------------

MEASURE = r"""
async (opts) => {
  const wait = (ms) => new Promise(r => setTimeout(r, ms));
  let rec;
  if (opts.warm) {
    rec = DB.index.find(r => DB.isLoaded(r.__file));
    if (rec) await DB.ensureFor([rec.id]);
  } else {
    rec = DB.index.find(r => !DB.isLoaded(r.__file));
  }
  if (!rec) return { error: 'brak rekordu w wybranym stanie' };

  window.__bench.events.length = 0;
  Player.noiseLevel = opts.noise || 0;
  const item = opts.warm ? (window.G ? G.view(DB.get(rec.id)) : DB.get(rec.id))
                         : Object.assign({}, rec, { __stub: true });

  const btn = document.createElement('button');
  document.body.appendChild(btn);
  const t0 = performance.now();
  Player.play(item, { btn: btn, tempo: opts.tempo, silentWarning: true });

  for (let i = 0; i < 500; i++) {
    if (window.__bench.events.some(e => e.kind === 'start')) break;
    await wait(8);
  }
  btn.remove();
  Player.stop();
  Player.noiseLevel = 0;
  const speak = window.__bench.events.find(e => e.kind === 'speak');
  const start = window.__bench.events.find(e => e.kind === 'start');
  if (!speak || !start) return { error: 'brak dźwięku' };
  return { toSpeak: speak.t - t0, toSound: start.t - t0, engine: Player.lastEngine };
}
"""


def latency(page, rows, label):
    for warm, state in ((False, "zimno (dociąga plik poziomu)"),
                        (True, "ciepło (plik w pamięci)")):
        # Każda próba na zimno zjada jeden niewczytany plik poziomu, a plików
        # jest szesnaście — na trzy tempa wypada najwyżej po cztery próby.
        tries = RUNS if warm else min(RUNS, 4)
        for tempo in ("slow", "natural", "fast"):
            vals, engines = [], set()
            for _ in range(tries):
                out = page.evaluate(MEASURE, {"warm": warm, "tempo": tempo})
                if out.get("error"):
                    break
                vals.append(out["toSound"])
                engines.add(out["engine"])
            if vals:
                rows.append((label, state, tempo, statistics.median(vals),
                             min(vals), max(vals), ",".join(sorted(engines)),
                             len(vals)))


NOISE_LATENCY = r"""
async () => {
  const wait = (ms) => new Promise(r => setTimeout(r, ms));
  const rec = DB.index.find(r => DB.isLoaded(r.__file));
  await DB.ensureFor([rec.id]);
  const item = window.G ? G.view(DB.get(rec.id)) : DB.get(rec.id);
  const out = {};
  for (const [name, clear] of [['szum liczony przy kliknięciu', true],
                               ['szum przygotowany wcześniej', 'prewarm'],
                               ['szum z pamięci', false]]) {
    if (clear === true) DSP.cache.clear();
    if (clear === 'prewarm') {
      DSP.cache.clear();
      Player.noiseKind = 'restaurant'; Player.noiseLevel = 2;
      Player.prewarm();
      await wait(400);
      Player.noiseLevel = 0;
    }
    window.__bench.events.length = 0;
    const btn = document.createElement('button');
    const t0 = performance.now();
    Player.play(item, { btn: btn, noise: { kind: 'restaurant', level: 2 }, silentWarning: true });
    for (let i = 0; i < 500; i++) {
      if (window.__bench.events.some(e => e.kind === 'start')) break;
      await wait(8);
    }
    const s = window.__bench.events.find(e => e.kind === 'start');
    out[name] = s ? s.t - t0 : -1;
    Player.stop();
  }
  return out;
}
"""

# --- 2. pamięć podręczna ----------------------------------------------------

CACHE_BENCH = r"""
async () => {
  const out = { noise: {}, buffer: {}, stats: null };

  // a) generowanie szumu tła
  for (const kind of ['restaurant', 'street', 'station']) {
    DSP.cache.clear();
    let t0 = performance.now();
    DSP.noise(kind, 2);
    const cold = performance.now() - t0;
    t0 = performance.now();
    DSP.noise(kind, 2);
    const warm = performance.now() - t0;
    out.noise[kind] = { cold: cold, warm: warm };
  }

  // b) dekodowanie nagrania i rozciągnięcie w czasie
  const tempos = { slow: { factor: 0.7 }, natural: { factor: 1.0 }, fast: { factor: 1.4 } };
  for (const name of Object.keys(tempos)) {
    DSP.cache.clear();
    try {
      let t0 = performance.now();
      await Player.loadProcessed('audio/_bench.wav', tempos[name]);
      const cold = performance.now() - t0;
      t0 = performance.now();
      await Player.loadProcessed('audio/_bench.wav', tempos[name]);
      const warm = performance.now() - t0;
      out.buffer[name] = { cold: cold, warm: warm };
    } catch (e) {
      out.buffer[name] = { error: String(e).slice(0, 60) };
    }
  }
  out.stats = DSP.cache.stats();
  return out;
}
"""


def run_mode(pw, url, label, rows, extra):
    browser = pw.chromium.launch(args=["--allow-file-access-from-files", "--no-sandbox",
                                       "--autoplay-policy=no-user-gesture-required"])
    page = browser.new_context().new_page()
    page.add_init_script(SHIM)
    page.add_init_script("localStorage.setItem('thaiaio.gender', JSON.stringify('male'));")
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_function("() => window.DB && DB.ready", timeout=45000)

    latency(page, rows, label)
    extra[label] = {
        "noise": page.evaluate(NOISE_LATENCY),
        "cache": page.evaluate(CACHE_BENCH)
    }
    browser.close()


def main():
    from playwright.sync_api import sync_playwright
    make_wav(BENCH_WAV)
    httpd = serve()
    rows, extra = [], {}
    try:
        with sync_playwright() as pw:
            run_mode(pw, "file://" + os.path.join(ROOT, "index.html"), "file://", rows, extra)
            run_mode(pw, "http://127.0.0.1:%d/index.html" % PORT, "serwer", rows, extra)
    finally:
        httpd.shutdown()
        if os.path.exists(BENCH_WAV):
            os.remove(BENCH_WAV)

    print("=" * 78)
    print("OPÓŹNIENIE ODTWARZANIA — od kliknięcia do pierwszego dźwięku")
    print("mediana z %d prób, atrapa silnika zgłasza dźwięk natychmiast" % RUNS)
    print("=" * 78)
    print("%-8s %-30s %-8s %9s %7s %7s %5s"
          % ("tryb", "stan", "tempo", "mediana", "min", "max", "prób"))
    for label, state, tempo, med, lo, hi, _eng, k in rows:
        print("%-8s %-30s %-8s %7.1f ms %6.1f %6.1f %5d"
              % (label, state, tempo, med, lo, hi, k))
    print("-" * 78)
    print("silniki użyte: %s" % ", ".join(sorted(set(r[6] for r in rows if r[6]))))

    for label in ("file://", "serwer"):
        block = extra.get(label)
        if not block:
            continue
        print()
        print("=" * 78)
        print("PAMIĘĆ PODRĘCZNA DŹWIĘKU — %s" % label)
        print("=" * 78)
        n = block["noise"]
        print("opóźnienie odtworzenia z szumem tła (poziom 2):")
        for k, v in n.items():
            print("  %-22s %7.1f ms" % (k, v))
        print()
        print("%-28s %10s %10s %10s" % ("operacja", "bez cache", "z cache", "zysk"))
        for kind, v in block["cache"]["noise"].items():
            gain = v["cold"] / max(0.01, v["warm"])
            print("%-28s %8.1f ms %8.2f ms %8.0fx" % ("szum: " + kind, v["cold"], v["warm"], gain))
        for name, v in block["cache"]["buffer"].items():
            if "error" in v:
                print("%-28s %s" % ("nagranie " + name, v["error"]))
            else:
                gain = v["cold"] / max(0.01, v["warm"])
                print("%-28s %8.1f ms %8.2f ms %8.0fx"
                      % ("nagranie: tempo " + name, v["cold"], v["warm"], gain))
        st = block["cache"]["stats"]
        print("stan pamięci: %d pozycji, %.1f MB z %d MB, trafień %d, chybień %d, eksmisji %d"
              % (st["entries"], st["bytes"] / 1048576, st["limit"] / 1048576,
                 st["hits"], st["misses"], st["evictions"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
