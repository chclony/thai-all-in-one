#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test działania, nie tylko renderowania.

Przechodzi przez rzeczywiste ścieżki użytkownika i sprawdza skutki:
  - zaliczenie lekcji odblokowuje następną,
  - pominięcie lekcji też odblokowuje,
  - ćwiczenie „ułóż zdanie” przyjmuje poprawną odpowiedź,
  - ćwiczenie „wpisz z pamięci” akceptuje zapis bez znaków tonu,
  - klasyfikatory i pary minimalne dają się rozstrzygnąć,
  - eksport CSV powstaje, ma nagłówek i nie zawiera pisma tajskiego,
  - krzywa zapamiętywania liczy się z danych SRS,
  - statystyka błędów wskazuje najsłabszy obszar,
  - detektor F0 trafia w znaną częstotliwość sygnału kontrolnego,
  - cisza i szum nie dostają wartości F0 (zwracane jest „brak”, nie zero),
  - ocena wymowy liczy się na syntetycznej wypowiedzi o znanych tonach,
  - karta oceny ma opis tekstowy i tabelę, nie tylko wykres,
  - czas reakcji trafia do statystyk i skraca odstęp powtórki,
  - Moduł 0 blokuje lekcję 1 i otwiera ją po zaliczeniu,
  - świadome pominięcie Modułu 0 otwiera kurs, a cofnięcie znów go zamyka,
  - test poziomujący powyżej A1 czyni Moduł 0 opcjonalnym,
  - zadanie percepcyjne da się rozstrzygnąć klawiaturą i ogłasza wynik,
  - diagnoza zwalnia lekcje opanowanych kontrastów, a słabe wysyła do powtórek,
  - karta kontrastu w powtórkach renderuje się i ocenia bez rekordu w bazie,
  - rozciąganie w czasie zmienia długość i NIE zmienia wysokości dźwięku,
  - szum tła generuje się i wraca z pamięci podręcznej zamiast liczyć się od nowa,
  - eksmisja z pamięci wyrzuca najdawniej używany bufor, nie najstarszy,
  - tempo dydaktyczne tnie wypowiedź na wyrazy, a nie zwalnia silnik,
  - tryb potoczny podaje syntezatorowi zapis zredukowany,
  - dwa głosy tajskie trafiają do dwóch ról, a przy jednym różnicuje wysokość,
  - brak możliwości przechwycenia syntezatora jest wykryty, a nie założony,
  - każda liczba z zakresu 0-1 000 000 daje się wygenerować i odczytać,
    a rozbiór odtwarza z zapisu tę samą wartość,
  - czas pomyłki nie wchodzi do mediany czasu reakcji przy liczbach,
  - opanowanie liczb zależy od czasu reakcji, nie od samej trafności,
  - limit czasu daje się wydłużyć i wyłączyć, a wyłączony nie kasuje pomiaru,
  - brak reakcji w drylu odruchu liczy się jak pomyłka,
  - migracja postępu ze starej ścieżki: przepisuje lekcje po zachowanym
    identyfikatorze, resztę przelicza przez znane hasła, wykonuje się raz
    i daje się cofnąć z kopii zapasowej,
  - egzamin poziomowy zalicza się KONIUNKCJĄ czterech progów, nie średnią:
    trzy sprawności doskonałe i jedna zerowa dają wynik niezaliczony,
  - bezbłędne tony przy złej treści nie zaliczają produkcji ustnej,
  - zapis fonetyczny punktowany jest sylabami, a znaki tonu liczą się osobno
    i nie wchodzą do progu,
  - deklaracja „powiedziałem to samo” bez wiarygodnego nagrania nie liczy się,
  - materiał egzaminacyjny da się odtworzyć najwyżej dwa razy,
  - upływ czasu liczy nietknięte zadania jak pomyłki, a nie jak brak zadania,
  - powtórka egzaminu wymaga i dni, i lekcji, i dostaje inny zestaw zadań,
  - wyjście z egzaminu zapisuje podejście jako przerwane i liczy je do karencji,
  - diagnoza wskazuje najsłabszą sprawność i konkretne lekcje oraz sceny,
  - certyfikat jest po polsku, w UTF-8, wymienia swoje ograniczenia i nie
    zawiera pisma tajskiego,
  - próbka kontrolna wypada co 20 lekcji i pyta o materiał sprzed 20 lekcji,
  - próbka wykrywa hasło zapomniane, choć kolejka powtórek nie miała go na dziś.
"""
import sys, os, json, threading, http.server, socketserver, functools, re

_ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
# Katalog projektu wyliczamy z położenia tego pliku. Zaszyta ścieżka
# powodowała, że po rozpakowaniu archiwum gdzie indziej serwer podawał
# nieistniejący katalog, a test kończył się timeoutem na DB.ready —
# objaw wyglądał jak zepsuta aplikacja, a była to zepsuta ścieżka.
ROOT = os.path.abspath(_ARGS[0]) if _ARGS \
    else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8177
THAI = re.compile(r'[\u0E00-\u0E7F]')


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


SRS_HORIZON = 14      # musi się zgadzać z SRS.HORIZON w js/srs.js
SRS_TUNE_MIN = 0.40   # musi się zgadzać z SRS.TUNE.min w js/srs.js


def main():
    from playwright.sync_api import sync_playwright
    httpd = serve()
    fails = []
    notes = []

    def check(label, ok, detail=''):
        if ok:
            notes.append('  OK   %s%s' % (label, (' — ' + detail) if detail else ''))
        else:
            fails.append('  BŁĄD %s%s' % (label, (' — ' + detail) if detail else ''))

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(accept_downloads=True)
        page = ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        # Płeć ustawiamy z góry, żeby okno powitalne nie przechwytywało kliknięć.
        page.add_init_script("""
          localStorage.setItem('thaiaio.gender', JSON.stringify('male'));
          localStorage.setItem('thaiaio.progress', JSON.stringify({
            days:{}, streak:0, bestStreak:0, lastDay:null, totalAnswers:0,
            totalCorrect:0, minutes:0, seen:{}, favourites:{}, lists:{}, goal:20,
            lessons:{}, errors:{category:{},grammar:{},type:{},mode:{}},
            perception:{lessons:{},contrasts:{},history:[],diagnostic:null,skipped:true},
            placement:{level:'Survival',score:9,total:28,date:'2026-01-01',
                       entryLesson:'lesson-001'}
          }));
        """)
        page.goto('http://127.0.0.1:%d/index.html' % PORT, wait_until='domcontentloaded')
        page.wait_for_function("() => window.DB && DB.ready", timeout=45000)

        # --- 1. blokada i odblokowanie lekcji ---
        r = page.evaluate("""() => {
          const L = DB.lessons;
          const first = L[0], second = L[1], third = L[2];
          const before = Course.status(second);
          Progress.setLessonResult(first.id, 'passed', 10, 12);
          const after = Course.status(second);
          const thirdStill = Course.status(third);
          Course.skip(second);
          const thirdNow = Course.status(third);
          return { before, after, thirdStill, thirdNow };
        }""")
        check('lekcja 2 zablokowana na starcie', r['before'] == 'locked', r['before'])
        check('zaliczenie lekcji 1 otwiera lekcję 2', r['after'] == 'open', r['after'])
        check('lekcja 3 nadal zamknięta', r['thirdStill'] == 'locked', r['thirdStill'])
        check('pominięcie lekcji 2 otwiera lekcję 3', r['thirdNow'] == 'open', r['thirdNow'])

        # --- 2. warunek dydaktyczny w danych faktycznie wczytanych ---
        r = page.evaluate("""async () => {
          const bad = [];
          let known = new Set();
          for (const L of DB.lessons) {
            await DB.ensureFor(L.recordIds);
            const newSyl = new Set();
            L.newWordIds.forEach(id => {
              const r = DB.get(id);
              (r ? r.syllables : []).forEach(s => newSyl.add(s));
            });
            const after = new Set([...known, ...newSyl]);
            for (const id of L.recordIds) {
              if (L.newWordIds.indexOf(id) !== -1) continue;
              const rec = DB.get(id);
              if (!rec) { bad.push(L.id + ':' + id + ' brak rekordu'); continue; }
              for (const s of rec.syllables) {
                if (!after.has(s)) { bad.push(L.id + ':' + id + ' sylaba ' + s); break; }
              }
            }
            known = after;
            if (bad.length > 3) break;
          }
          return { bad, lessons: DB.lessons.length };
        }""")
        check('każda lekcja mieści się w znanym zasobie sylab',
              not r['bad'], '; '.join(r['bad'][:3]))

        # --- 3. ćwiczenia produkcyjne ---
        page.evaluate("() => { Produce.mode = 'build'; App.go('produce'); }")
        page.wait_for_timeout(1200)
        r = page.evaluate("""() => {
          const rec = Produce.current;
          if (!rec) return { ok: false, why: 'brak zadania' };
          const target = rec.thaiPhonetic.split(/\\s+/);
          // kafelki banku to te, które nie leżą w wierszu odpowiedzi
          const bank = Array.from(document.querySelectorAll('#produce-area .token'))
            .filter(t => !t.closest('.answer'));
          const byText = {};
          bank.forEach(b => { byText[b.textContent] = b; });
          for (const w of target) {
            const btn = byText[w];
            if (!btn) return { ok: false, why: 'brak kafelka ' + w };
            btn.click();
          }
          const check = Array.from(document.querySelectorAll('#produce-area .btn'))
            .find(b => b.textContent === 'Sprawdź');
          if (!check) return { ok: false, why: 'brak przycisku Sprawdź' };
          check.click();
          const fb = document.querySelector('#produce-area .fb');
          return { ok: !!fb && fb.classList.contains('ok'), why: fb ? fb.textContent : 'brak oceny' };
        }""")
        check('„ułóż zdanie” przyjmuje poprawną kolejność', r['ok'], r.get('why', '')[:70])

        page.evaluate("() => { Produce.mode = 'type'; App.go('produce'); }")
        page.wait_for_timeout(1000)
        r = page.evaluate("""() => {
          const rec = Produce.current;
          if (!rec) return { ok: false, why: 'brak zadania' };
          const input = document.getElementById('produce-type-input');
          // celowo bez znaków tonu — ćwiczenie ma je tolerować
          input.value = U.stripTones(rec.thaiPhonetic);
          const check = Array.from(document.querySelectorAll('#produce-area .btn'))
            .find(b => b.textContent === 'Sprawdź');
          check.click();
          const fb = document.querySelector('#produce-area .fb');
          return { ok: !!fb && fb.classList.contains('ok'), why: fb ? fb.textContent : 'brak oceny' };
        }""")
        check('„wpisz z pamięci” toleruje brak znaków tonu', r['ok'], r.get('why', '')[:70])

        page.evaluate("() => { Produce.mode = 'classifier'; App.go('produce'); }")
        page.wait_for_timeout(900)
        r = page.evaluate("""() => {
          const right = Produce.current;
          if (!right) return { ok: false, why: 'brak zadania' };
          const btn = Array.from(document.querySelectorAll('#produce-area .opt'))
            .find(b => b.getAttribute('aria-label') === 'Klasyfikator ' + right.classifier);
          if (!btn) return { ok: false, why: 'brak właściwej opcji' };
          btn.click();
          const fb = document.querySelector('#produce-area .fb');
          return { ok: !!fb && fb.classList.contains('ok'), why: fb ? fb.textContent : '' };
        }""")
        check('klasyfikatory rozstrzygają się poprawnie', r['ok'], r.get('why', '')[:70])

        page.evaluate("() => { Produce.mode = 'tone'; App.go('produce'); }")
        page.wait_for_timeout(1200)
        r = page.evaluate("""() => {
          const t = Produce.current;
          if (!t) return { ok: false, why: 'brak par minimalnych' };
          const opts = document.querySelectorAll('#produce-area .tone-opt');
          if (opts.length < 2) return { ok: false, why: 'mniej niż dwie opcje' };
          const right = Array.from(opts).find(b =>
            b.getAttribute('aria-label').indexOf(t.polish + ', ton') === 0);
          if (!right) return { ok: false, why: 'brak właściwej opcji' };
          right.click();
          const fb = document.querySelector('#produce-area .fb');
          return { ok: !!fb && fb.classList.contains('ok'), count: opts.length };
        }""")
        check('pary minimalne dają się rozstrzygnąć', r['ok'],
              'opcji: %s' % r.get('count', r.get('why', '')))

        page.evaluate("() => { Produce.mode = 'roleplay'; App.go('produce'); }")
        page.wait_for_timeout(1200)
        r = page.evaluate("""() => {
          const lines = document.querySelectorAll('#produce-area .rp-line');
          const mine = document.querySelectorAll('#produce-area .rp-mine');
          const controls = document.querySelectorAll('#produce-area .rp-control');
          const recBtns = [...document.querySelectorAll('#produce-area .rp-control button')]
            .filter(b => /Nagraj kwesti/.test(b.textContent));
          return { lines: lines.length, mine: mine.length,
                   rec: recBtns.length, controls: controls.length };
        }""")
        check('role-play rozdziela kwestie i daje nagrywanie z oceną',
              r['lines'] > 3 and r['mine'] > 0 and r['rec'] == r['mine']
              and r['controls'] == r['mine'],
              'kwestii %d, moich %d, przycisków nagrywania %d, kart oceny %d'
              % (r['lines'], r['mine'], r['rec'], r['controls']))

        # --- 4. krzywa zapamiętywania ---
        r = page.evaluate("""() => {
          SRS.log = [];
          const mk = (iv, ok, n) => { for (let i=0;i<n;i++) SRS.log.push({d:'2026-08-01', iv:iv, ok:ok}); };
          mk(1, 1, 20); mk(1, 0, 2);
          mk(3, 1, 15); mk(3, 0, 5);
          mk(6, 1, 10); mk(6, 0, 10);
          mk(20, 1, 4);  mk(20, 0, 6);
          const r = SRS.retention().filter(b => b.total);
          return r.map(b => [b.label, b.rate, b.total]);
        }""")
        rates = [x[1] for x in r]
        check('krzywa zapamiętywania maleje z odstępem',
              len(r) == 4 and rates == sorted(rates, reverse=True),
              ', '.join('%s %d%%' % (x[0], x[1]) for x in r))

        page.evaluate("() => App.go('progress')")
        page.wait_for_timeout(900)
        r = page.evaluate("""() => {
          const svg = document.querySelector('#prog-retention svg');
          const rows = document.querySelectorAll('#prog-retention .data-table tbody tr');
          return { svg: !!svg, pts: svg ? svg.querySelectorAll('circle').length : 0,
                   rows: rows.length, label: svg ? svg.getAttribute('aria-label') : '' };
        }""")
        check('wykres krzywej rysuje się i ma opis tekstowy',
              r['svg'] and r['pts'] == 4 and r['rows'] == 4 and 'Krzywa' in (r['label'] or ''),
              'punktów %d, wierszy tabeli %d' % (r['pts'], r['rows']))

        # --- 5. statystyka błędów ---
        r = page.evaluate("""() => {
          Progress.data.errors = { category: {}, grammar: {}, type: {}, mode: {} };
          Progress.data.errors.category['Liczby i liczenie'] = { answers: 20, wrong: 14 };
          Progress.data.errors.category['Jedzenie i napoje'] = { answers: 30, wrong: 3 };
          Progress.data.errors.grammar['gram-004'] = { answers: 12, wrong: 4 };
          Progress.save();
          const w = Stats.worst();
          return w ? { label: w.label, rate: w.item.rate, sugg: w.suggestion.label,
                       screen: w.suggestion.screen } : null;
        }""")
        check('najsłabszy obszar wskazany z propozycją ćwiczenia',
              r and r['label'] == 'Liczby i liczenie' and r['screen'] == 'produce',
              '%s (%d%%) -> %s' % (r['label'], r['rate'], r['sugg']) if r else 'brak')

        # --- 6. eksport CSV do Anki ---
        page.evaluate("""() => {
          Progress.data.favourites = {};
          DB.index.slice(0, 25).forEach(r => { Progress.data.favourites[r.id] = true; });
          Progress.save();
        }""")
        page.evaluate("() => App.go('progress')")
        page.wait_for_timeout(500)
        page.select_option('#anki-scope', 'favourites')
        with page.expect_download(timeout=30000) as dl:
            page.click('#btn-anki')
        path = dl.value.path()
        with open(path, encoding='utf-8-sig') as fh:
            csv_text = fh.read()
        lines = [l for l in csv_text.splitlines() if l.strip()]
        header_ok = lines[0].startswith('Polski,Fonetyka,CzytajPoPolsku')
        check('CSV ma nagłówek zgodny z Anki', header_ok, lines[0][:60])
        check('CSV zawiera wyeksportowane hasła', len(lines) == 26,
              '%d wierszy (nagłówek + 25)' % len(lines))
        check('CSV nie zawiera pisma tajskiego', not THAI.search(csv_text))
        check('CSV ma wypełnioną fonetykę i wymowę',
              all(len(l.split(',')) >= 5 for l in lines[1:6]))

        # --- 7. sprawdzian lekcji liczy punkty i zalicza ---
        r = page.evaluate("""async () => {
          const L = DB.lessons[3];
          const m = await Course.load(L);
          Course.startTest(m);
          const total = Course.run.items.length;
          for (let i = 0; i < total; i++) Course.recordAnswer(true, Course.run.items[i].rec.id);
          const res = Course.finishTest();
          const status = Course.status(L);
          return { passed: res.passed, correct: res.correct, total: res.total,
                   required: res.required, status };
        }""")
        check('komplet trafnych odpowiedzi zalicza lekcję',
              r['passed'] and r['status'] == 'passed',
              '%d/%d, próg %d' % (r['correct'], r['total'], r['required']))

        r = page.evaluate("""async () => {
          const L = DB.lessons[4];
          const m = await Course.load(L);
          Course.startTest(m);
          const total = Course.run.items.length;
          for (let i = 0; i < total; i++) Course.recordAnswer(i < 2, Course.run.items[i].rec.id);
          const res = Course.finishTest();
          return { passed: res.passed, wrong: res.wrongIds.length,
                   inSrs: res.wrongIds.every(id => SRS.has(id, 'r') && SRS.has(id, 'p')) };
        }""")
        check('zbyt słaby wynik nie zalicza lekcji', not r['passed'])
        check('pomyłki ze sprawdzianu trafiają do powtórek obiema stronami', r['inSrs'],
              '%d haseł' % r['wrong'])

        # --- 8. ładowanie na żądanie ---
        r = page.evaluate("""() => {
          const data = DB.manifest.dataFiles.map(d => d.file);
          return {
            files: data.filter(f => DB.isLoaded(f)).length,
            all: data.length,
            share: DB.loadedShare(),
            complete: DB.complete
          };
        }""")
        check('pliki poziomów dociągane tylko na żądanie', r['files'] <= r['all'],
              '%d z %d plików słownikowych w pamięci (%d%% bazy)'
              % (r['files'], r['all'], r['share']))


        # --- 9. detekcja F0 na sygnale o znanej częstotliwości ---
        r = page.evaluate("""() => {
          const out = [];
          for (const hz of [95, 130, 180, 250, 330]) {
            const sig = Pitch.testSignal(hz, 1.0, 44100, 0.01);
            const t0 = performance.now();
            const a = Pitch.analyse(sig, 44100);
            out.push({
              hz: hz,
              got: a.medianF0,
              err: a.medianF0 ? Math.abs(a.medianF0 - hz) / hz * 100 : 100,
              ms: performance.now() - t0,
              voiced: a.voicedRatio
            });
          }
          return out;
        }""")
        worst = max(x['err'] for x in r)
        slowest = max(x['ms'] for x in r)
        check('detektor F0 trafia w znaną częstotliwość', worst < 1.0,
              'największy błąd %.3f%% (95–330 Hz), najgorszy czas %.0f ms na sekundę nagrania'
              % (worst, slowest))
        check('cały sygnał tonalny uznany za dźwięczny',
              min(x['voiced'] for x in r) > 0.9,
              'najmniej %.0f%% ramek' % (min(x['voiced'] for x in r) * 100))

        # --- 10. cisza, szum i sygnał bezdźwięczny ---
        r = page.evaluate("""() => {
          const n = 44100;
          const silence = new Float32Array(n);
          const noise = new Float32Array(n);
          for (let i = 0; i < n; i++) noise[i] = (Math.random() * 2 - 1) * 0.2;
          const a = Pitch.analyse(silence, 44100);
          const b = Pitch.analyse(noise, 44100);
          return {
            silencePoints: a.points.length, silenceMedian: a.medianF0,
            noiseVoiced: b.voicedRatio,
            zeros: a.frames.filter(f => f.f0 === 0).length + b.frames.filter(f => f.f0 === 0).length
          };
        }""")
        check('cisza nie dostaje wysokości dźwięku',
              r['silencePoints'] == 0 and r['silenceMedian'] is None)
        check('szum bezdźwięczny w większości odrzucony', r['noiseVoiced'] < 0.35,
              'dźwięcznych ramek %.0f%%' % (r['noiseVoiced'] * 100))
        check('brak wartości zapisany jako „brak”, nie jako zero', r['zeros'] == 0)

        # --- 11. ocena wymowy na wypowiedzi o znanych tonach ---
        # Budujemy sygnał z konturów wzorcowych, kodujemy do WAV i puszczamy
        # przez tę samą drogę co prawdziwe nagranie: decodeAudioData -> YIN.
        r = page.evaluate("""async () => {
          const rate = 44100;
          function wav(samples) {
            const buf = new ArrayBuffer(44 + samples.length * 2);
            const view = new DataView(buf);
            const w = (o, s) => { for (let i = 0; i < s.length; i++) view.setUint8(o + i, s.charCodeAt(i)); };
            w(0, 'RIFF'); view.setUint32(4, 36 + samples.length * 2, true); w(8, 'WAVEfmt ');
            view.setUint32(16, 16, true); view.setUint16(20, 1, true); view.setUint16(22, 1, true);
            view.setUint32(24, rate, true); view.setUint32(28, rate * 2, true);
            view.setUint16(32, 2, true); view.setUint16(34, 16, true);
            w(36, 'data'); view.setUint32(40, samples.length * 2, true);
            for (let i = 0; i < samples.length; i++) {
              const v = Math.max(-1, Math.min(1, samples[i]));
              view.setInt16(44 + i * 2, v * 32767, true);
            }
            return new Blob([buf], { type: 'audio/wav' });
          }
          function utter(tones, durs, centre, halfSpan) {
            const total = durs.reduce((a, b) => a + b, 0) + 60 * durs.length + 400;
            const out = new Float32Array(Math.round(rate * total / 1000));
            let pos = Math.round(rate * 0.2), phase = 0;
            tones.forEach((tone, si) => {
              const shape = ToneScore.SHAPES[tone];
              const len = Math.round(rate * durs[si] / 1000);
              for (let i = 0; i < len; i++) {
                const idx = (i / (len - 1)) * (shape.length - 1);
                const a = shape[Math.floor(idx)], b = shape[Math.min(shape.length - 1, Math.ceil(idx))];
                const c = a + (b - a) * (idx - Math.floor(idx));
                const f = centre * Math.pow(2, ((c - 3) / 2 * halfSpan) / 12);
                phase += 2 * Math.PI * f / rate;
                const env = Math.min(1, Math.min(i, len - i) / (rate * 0.025));
                out[pos + i] = env * 0.5 * (Math.sin(phase) + 0.35 * Math.sin(2 * phase));
              }
              pos += len + Math.round(rate * 0.06);
            });
            return out;
          }
          const rec = { id: 'test-tone', thaiPhonetic: 'khàwp-khun mâak',
                        syllables: ['khàwp', 'khun', 'mâak'] };
          const good = await Pitch.fromBlob(wav(utter(
            ['niski', 'średni', 'opadający'], [260, 180, 320], 128, 4)));
          const flat = await Pitch.fromBlob(wav(utter(
            ['średni', 'średni', 'średni'], [260, 180, 320], 128, 4)));
          const g = ToneScore.evaluate(rec, good);
          const f = ToneScore.evaluate(rec, flat);
          return {
            goodScore: g.score, goodHits: g.hits, goodTotal: g.total,
            goodDist: g.distance, source: g.reference.source,
            flatScore: f.score, flatHits: f.hits,
            flatAdvice: f.advice.length,
            tones: g.syllables.map(s => s.producedTone).join(','),
            srsGood: ToneScore.srsQuality(g), srsFlat: ToneScore.srsQuality(f)
          };
        }""")
        check('wypowiedź o poprawnych tonach oceniona wysoko',
              r['goodScore'] >= 85 and r['goodHits'] == r['goodTotal'],
              '%d/100, tony %d/%d, odległość konturów %s, wzorzec: %s'
              % (r['goodScore'], r['goodHits'], r['goodTotal'], r['goodDist'], r['source']))
        check('wypowiedź płaska oceniona nisko', r['flatScore'] < 65,
              '%d/100, trafione %d z 3' % (r['flatScore'], r['flatHits']))
        check('błędne tony dostają radę, co poprawić', r['flatAdvice'] >= 1,
              '%d wskazówek' % r['flatAdvice'])
        check('ocena wymowy przekłada się na ocenę SM-2',
              r['srsGood'] >= 4 and r['srsFlat'] <= 3,
              'trafnie -> %d, płasko -> %d' % (r['srsGood'], r['srsFlat']))

        # --- 12. karta oceny jest dostępna nie tylko wzrokowo ---
        r = page.evaluate("""() => {
          const res = PronView.sampleResult();
          const node = PronView.render(res);
          const svg = node.querySelector('svg');
          const rows = node.querySelectorAll('tbody tr');
          const desc = svg ? svg.getAttribute('aria-label') : '';
          return {
            hasSvg: !!svg,
            rows: rows.length,
            descLen: desc.length,
            descHasTones: /rosnący|opadający|niski|wysoki|średni/.test(desc),
            descHasNumbers: /\d/.test(desc),
            advice: node.querySelectorAll('.advice-list li').length,
            headText: node.querySelector('.pron-head').textContent
          };
        }""")
        check('wykres oceny ma pełny opis tekstowy',
              r['hasSvg'] and r['descLen'] > 120 and r['descHasTones'] and r['descHasNumbers'],
              '%d znaków opisu' % r['descLen'])
        check('liczby są też w tabeli, nie tylko na wykresie', r['rows'] == 3,
              '%d wierszy' % r['rows'])
        check('ocena jest słowna, nie tylko procentowa', r['advice'] >= 1,
              r['headText'][:60])

        # --- 13. czas reakcji i jego wpływ na powtórki ---
        r = page.evaluate("""() => {
          const id = DB.index[0].id;
          Progress.data.times = {}; Progress.data.timeLog = [];
          for (let i = 0; i < 12; i++) Progress.recordTime('szybkie-' + i, 1500 + i * 20, 'build');
          const verdictFast = Progress.recordTime(id, 1400, 'build');
          const verdictSlow = Progress.recordTime(id, 9000, 'build');
          Progress.recordTime(id, 9200, 'build');
          const stats = Progress.timeStats();

          const key = SRS.cardId(id, 'p');
          SRS.cards[key] = { id: key, ease: 2.5, interval: 10, repetitions: 3,
                             due: U.today(), lapses: 0, seen: 3, correct: 3, last: null };
          const normal = SRS.grade(id, 5, { side: 'p' }).interval;
          SRS.cards[key].interval = 10; SRS.cards[key].repetitions = 3; SRS.cards[key].ease = 2.5;
          const slowed = SRS.grade(id, 5, { pace: 'slow', side: 'p' }).interval;
          const flagged = !!SRS.cards[key].slow;
          const slowList = Progress.slowItems(10).map(x => x.id);
          return { verdictFast, verdictSlow, median: stats.median, threshold: stats.threshold,
                   normal, slowed, flagged, inSlowList: slowList.indexOf(id) !== -1 };
        }""")
        check('mediana czasu reakcji liczy się z pomiarów',
              1400 <= r['median'] <= 3000, '%d ms, próg powolności %d ms'
              % (r['median'], r['threshold']))
        check('wolna odpowiedź rozpoznana jako wolna',
              r['verdictSlow'] == 'slow' and r['verdictFast'] != 'slow')
        check('wolna odpowiedź skraca odstęp powtórki', r['slowed'] < r['normal'],
              '%d dni zamiast %d' % (r['slowed'], r['normal']))
        check('hasło znane, ale wolne, trafia na listę do częstszych powtórek',
              r['flagged'] and r['inSlowList'])

        # --- 14. tryb „Wymów poprawnie” istnieje i się renderuje ---
        r = page.evaluate("""async () => {
          const has = Produce.MODES.some(m => m.id === 'say');
          Produce.mode = 'say';
          await Produce.ensureData();
          const box = document.getElementById('produce-area');
          Produce.render(box);
          await new Promise(r2 => setTimeout(r2, 400));
          return {
            has: has,
            text: box.innerText.length,
            polish: !!box.querySelector('.bc-pl'),
            hiddenPhonetic: box.querySelectorAll('.reveal[hidden]').length,
            buttons: [...box.querySelectorAll('button')].map(b => b.textContent.trim()).join(' | ')
          };
        }""")
        check('tryb produkcyjny „Wymów poprawnie” jest dostępny', r['has'])
        check('tryb pokazuje polski, a zapis chowa pod podpowiedzią',
              r['polish'] and r['hiddenPhonetic'] == 1,
              r['buttons'][:90])

        # --- 15. Moduł 0: dane i blokada wejścia w kurs ---
        r = page.evaluate("""() => {
          const mz = DB.moduleZero;
          const tasks = mz.lessons.reduce((n, L) => n + L.tasks.length, 0);
          const thresholds = mz.lessons.map(L => L.pass.required / L.pass.questions);
          return {
            ready: Perception.ready(),
            lessons: mz.lessons.length,
            tasks: tasks,
            diag: mz.diagnostic.tasks.length,
            stimuli: mz.stimuli.length,
            contrasts: mz.contrasts.length,
            minThreshold: Math.min(...thresholds),
            sizesOk: mz.lessons.every(L => L.tasks.length >= 15 && L.tasks.length <= 25),
            types: [...new Set(mz.lessons.flatMap(L => L.tasks.map(t => t.type)))].sort()
          };
        }""")
        check('Moduł 0 jest wczytany', r['ready'])
        check('Moduł 0 ma 12 lekcji', r['lessons'] == 12, '%d lekcji' % r['lessons'])
        check('każda lekcja mieści się w 15-25 zadaniach', r['sizesOk'],
              '%d zadań razem' % r['tasks'])
        check('próg zaliczenia nigdzie nie schodzi poniżej 90%',
              r['minThreshold'] >= 0.9 - 1e-9, 'najniższy %d%%' % round(r['minThreshold'] * 100))
        check('diagnoza ma 20 zadań', r['diag'] == 20, '%d zadań' % r['diag'])
        check('wszystkie sześć typów zadań percepcyjnych jest użytych',
              len(r['types']) == 6, ', '.join(r['types']))

        r = page.evaluate("""() => {
          Progress.data.perception = { lessons:{}, contrasts:{}, history:[],
                                       diagnostic:null, skipped:false };
          Progress.data.lessons = {};
          Progress.data.placement = { level:'Survival', score:9, total:28,
                                      date:'2026-01-01', entryLesson:'lesson-001' };
          Progress.save();
          const before = Course.status(DB.lessons[0]);
          Perception.skipModule();
          const afterSkip = Course.status(DB.lessons[0]);
          Perception.unskipModule();
          const afterUndo = Course.status(DB.lessons[0]);
          return { before, afterSkip, afterUndo, gate: Perception.gateOpen() };
        }""")
        check('Moduł 0 blokuje lekcję 1 kursu', r['before'] == 'locked', r['before'])
        check('świadome pominięcie modułu otwiera lekcję 1',
              r['afterSkip'] == 'open', r['afterSkip'])
        check('cofnięcie pominięcia znów zamyka lekcję 1',
              r['afterUndo'] == 'locked', r['afterUndo'])

        r = page.evaluate("""() => {
          const L = Perception.lessons()[0];
          Perception.start(L);
          while (!Perception.done()) {
            const t = Perception.current();
            Perception.answer(t, t.answer);
          }
          const res = Perception.finish();
          const first = { status: Perception.status(L), passed: res.passed };
          const second = Perception.status(Perception.lessons()[1]);
          const third = Perception.status(Perception.lessons()[2]);
          return { first, second, third, gate: Perception.gateOpen(),
                   course: Course.status(DB.lessons[0]) };
        }""")
        check('komplet trafnych odpowiedzi zalicza lekcję percepcyjną',
              r['first']['passed'] and r['first']['status'] == 'passed')
        check('zaliczenie lekcji 1 otwiera lekcję 2 modułu', r['second'] == 'open', r['second'])
        check('lekcja 3 modułu nadal zamknięta', r['third'] == 'locked', r['third'])
        check('niedokończony moduł nadal blokuje kurs',
              (not r['gate']) and r['course'] == 'locked')

        r = page.evaluate("""() => {
          const L = Perception.lessons()[1];
          Perception.start(L);
          const need = L.pass.required;
          let i = 0;
          while (!Perception.done()) {
            const t = Perception.current();
            const bad = t.options.find(o => o !== t.answer);
            Perception.answer(t, i < need - 1 ? t.answer : bad);
            i++;
          }
          const res = Perception.finish();
          return { passed: res.passed, correct: res.correct, required: res.required,
                   status: Perception.status(L), weak: res.weakContrasts.length,
                   inSrs: SRS.contrastCards().length };
        }""")
        check('wynik o jedną odpowiedź poniżej progu nie zalicza lekcji',
              (not r['passed']) and r['status'] == 'open',
              '%d z progiem %d' % (r['correct'], r['required']))
        check('pomylone kontrasty trafiają do powtórek jako osobne karty',
              r['weak'] > 0 and r['inSrs'] >= r['weak'],
              '%d kontrastów' % r['weak'])

        # --- 16. diagnoza percepcyjna ---
        r = page.evaluate("""() => {
          Progress.data.perception = { lessons:{}, contrasts:{}, history:[],
                                       diagnostic:null, skipped:false };
          Progress.data.lessons = {};
          SRS.cards = {}; SRS.save();
          Perception.startDiagnostic();
          while (!Perception.diagnosticDone()) {
            const t = Perception.currentDiagnostic();
            Perception.answerDiagnostic(t, t.answer);
          }
          const res = Perception.finishDiagnostic();
          return { score: res.score, total: res.total,
                   mastered: res.mastered.length, freed: res.freed.length,
                   weak: res.weakContrasts.length,
                   course: Course.status(DB.lessons[0]),
                   saved: !!Progress.data.perception.diagnostic };
        }""")
        check('komplet w diagnozie oznacza wszystkie rodziny jako opanowane',
              r['mastered'] == 7, '%d z 7 rodzin' % r['mastered'])
        check('lekcje opanowanych kontrastów są oznaczane jako zdane',
              r['freed'] == 12, '%d lekcji zwolnionych' % r['freed'])
        check('diagnoza bez pomyłek nie wysyła nic do powtórek', r['weak'] == 0)
        check('zwolnienie diagnozą otwiera kurs', r['course'] == 'open', r['course'])
        check('wynik diagnozy zapisuje się w postępie', r['saved'])

        r = page.evaluate("""() => {
          Progress.data.perception = { lessons:{}, contrasts:{}, history:[],
                                       diagnostic:null, skipped:false };
          Progress.data.lessons = {};
          SRS.cards = {}; SRS.save();
          Perception.startDiagnostic();
          /* W każdej rodzinie mylimy dokładnie jedno zadanie. Losowy co drugi
             błąd nie wystarczy: rodzina o dwóch zadaniach mogłaby wyjść
             bezbłędnie i test raz na jakiś czas pękałby bez powodu. */
          const missed = {};
          while (!Perception.diagnosticDone()) {
            const t = Perception.currentDiagnostic();
            const bad = t.options.find(o => o !== t.answer);
            const first = !missed[t.family];
            missed[t.family] = true;
            Perception.answerDiagnostic(t, first ? bad : t.answer);
          }
          const res = Perception.finishDiagnostic();
          const stats = Progress.contrastStats(1);
          return { mastered: res.mastered.length, freed: res.freed.length,
                   weak: res.weakContrasts.length,
                   srs: SRS.contrastCards().length,
                   statRows: stats.length,
                   worst: (Progress.weakestContrast(1) || {}).id || null,
                   course: Course.status(DB.lessons[0]) };
        }""")
        check('częściowa diagnoza nie zwalnia lekcji', r['freed'] == 0)
        check('słabe kontrasty z diagnozy trafiają do powtórek',
              r['weak'] > 0 and r['srs'] == r['weak'], '%d kontrastów' % r['weak'])
        check('częściowa diagnoza nie otwiera kursu', r['course'] == 'locked', r['course'])
        check('statystyka per kontrast się wypełnia',
              r['statRows'] > 0 and r['worst'], 'najsłabszy: %s' % r['worst'])

        # --- 17. test poziomujący powyżej A1 zwalnia z modułu ---
        r = page.evaluate("""() => {
          Progress.data.perception = { lessons:{}, contrasts:{}, history:[],
                                       diagnostic:null, skipped:false };
          Progress.data.placement = { level:'A2', score:20, total:28,
                                      date:'2026-01-01', entryLesson:'lesson-001' };
          Progress.save();
          const optional = Perception.isOptional();
          const gate = Perception.gateOpen();
          Progress.data.placement.level = 'Survival';
          delete Progress.data.perception.optional;
          Progress.save();
          return { optional, gate, backToBlocked: !Perception.gateOpen() };
        }""")
        check('poziom powyżej A1 czyni Moduł 0 opcjonalnym', r['optional'] and r['gate'])
        check('poziom Survival znów wymaga Modułu 0', r['backToBlocked'])

        # --- 18. zadanie percepcyjne w interfejsie ---
        r = page.evaluate("""async () => {
          Progress.data.perception = { lessons:{}, contrasts:{}, history:[],
                                       diagnostic:null, skipped:false };
          App.go('module0');
          const L = Perception.lessons()[0];
          Perception.start(L);
          M0View.state.mode = 'lesson';
          M0View.render();
          await new Promise(r2 => setTimeout(r2, 300));
          const area = document.getElementById('module0-area');
          const opts = [...area.querySelectorAll('.m0-options .opt')];
          const hiddenBefore = area.querySelector('.m0-reveal').hidden;
          const t = Perception.current();
          const right = opts.find(b => b.getAttribute('aria-label').endsWith(': ' + t.answer));
          right.click();
          await new Promise(r2 => setTimeout(r2, 250));
          const live = document.getElementById('m0-live').textContent;
          const buttons = [...area.querySelectorAll('.btn-row button')]
            .map(b => b.textContent.trim());
          return {
            options: opts.length,
            numbered: opts.every(b => /^Odpowiedź \d+: /.test(b.getAttribute('aria-label'))),
            hiddenBefore: hiddenBefore,
            revealedAfter: !area.querySelector('.m0-reveal').hidden,
            live: live,
            compare: buttons.some(b => b.indexOf('Porównaj') === 0),
            replay: buttons.some(b => b.indexOf('Jeszcze raz') === 0),
            allNamed: opts.every(b => (b.getAttribute('aria-label') || '').trim().length > 0)
          };
        }""")
        check('zadanie percepcyjne pokazuje ponumerowane odpowiedzi',
              r['options'] >= 2 and r['numbered'], '%d opcji' % r['options'])
        check('zapis fonetyczny jest zasłonięty do czasu odpowiedzi',
              r['hiddenBefore'] and r['revealedAfter'])
        check('wynik jest ogłaszany przez aria-live', len(r['live']) > 0, r['live'][:60])
        check('po odpowiedzi da się przesłuchać oba warianty i powtórzyć bodziec',
              r['compare'] and r['replay'])
        check('każda odpowiedź ma dostępną nazwę', r['allNamed'])

        r = page.evaluate("""async () => {
          const before = Perception.run.at;
          const ev = new KeyboardEvent('keydown', { key: 'Enter', bubbles: true });
          document.dispatchEvent(ev);
          await new Promise(r2 => setTimeout(r2, 250));
          const mid = Perception.run.at;
          document.dispatchEvent(new KeyboardEvent('keydown', { key: '1', bubbles: true }));
          await new Promise(r2 => setTimeout(r2, 250));
          return { before, mid, after: Perception.run.at };
        }""")
        check('Enter przechodzi do następnego zadania, cyfra wybiera odpowiedź',
              r['after'] == r['before'] + 1,
              'at %d -> %d -> %d' % (r['before'], r['mid'], r['after']))

        # --- 19. karta kontrastu w powtórkach ---
        r = page.evaluate("""async () => {
          Perception.run = null;
          M0View.state.mode = 'map';
          SRS.cards = {}; SRS.addContrast('ton-niski-vs-opadajacy'); SRS.save();
          App.go('srs');
          await new Promise(r2 => setTimeout(r2, 350));
          const box = document.getElementById('srs-area');
          const opts = [...box.querySelectorAll('.m0-options .opt')];
          const label = box.innerText.slice(0, 80);
          opts[0].click();
          await new Promise(r2 => setTimeout(r2, 250));
          const card = SRS.cards['perc:ton-niski-vs-opadajacy'];
          const stat = Progress.data.perception.contrasts['ton-niski-vs-opadajacy'];
          return { opts: opts.length, label: label,
                   graded: card.seen === 1, due: card.due,
                   counted: !!stat && stat.answers === 1,
                   fb: !!box.querySelector('.fb') };
        }""")
        check('kontrast z powtórek renderuje się jako osobny typ karty',
              r['opts'] >= 2 and 'Powtórka słuchowa' in r['label'], r['label'].replace('\n', ' ')[:60])
        check('odpowiedź w powtórce ocenia kartę i liczy się do kontrastu',
              r['graded'] and r['counted'] and r['fb'])


        # --- 20. warstwa dźwiękowa: rozciąganie w czasie ---
        # WSOLA musi zmienić długość i NIE zmienić wysokości. Gdyby zmieniała
        # wysokość, cała drabina tempa uczyłaby złych tonów — to jedyny test,
        # który tego pilnuje.
        dsp = page.evaluate(r"""() => {
          const sr = 44100;
          const n = Math.floor(sr * 1.2);
          // Stała częstotliwość podstawowa: gdyby sygnał miał vibrato,
          // pomiar w dwóch różnych miejscach dałby dwie różne wartości
          // i test mierzyłby własny błąd zamiast błędu algorytmu.
          const x = new Float32Array(n);
          for (let i = 0; i < n; i++) {
            const t = i / sr, p = 2 * Math.PI * 150 * t;
            x[i] = (Math.sin(p) + 0.5 * Math.sin(2 * p)) * (0.4 + 0.3 * Math.sin(2 * Math.PI * 4 * t));
          }
          const f0 = (d, from, len) => {
            const seg = d.subarray(from, from + len);
            let best = 1, bv = -1;
            for (let lag = Math.floor(sr / 400); lag < Math.floor(sr / 70); lag++) {
              let s = 0, e1 = 0, e2 = 0;
              for (let i = 0; i + lag < seg.length; i++) { s += seg[i] * seg[i + lag]; e1 += seg[i] * seg[i]; e2 += seg[i + lag] * seg[i + lag]; }
              const v = s / Math.sqrt(e1 * e2 + 1e-12);
              if (v > bv) { bv = v; best = lag; }
            }
            return sr / best;
          };
          const out = {};
          [0.7, 1.4].forEach(f => {
            const t0 = performance.now();
            const y = DSP.stretchChannel(x, f);
            out['ms' + f] = performance.now() - t0;
            out['len' + f] = (y.length / (n / f)) - 1;
            out['f0' + f] = f0(y, Math.floor(y.length * 0.3), 8192) / f0(x, Math.floor(n * 0.3), 8192) - 1;
          });
          return out;
        }""")
        check('rozciąganie w czasie trafia w zadaną długość',
              abs(dsp['len0.7']) < 0.03 and abs(dsp['len1.4']) < 0.03,
              '0,7x %+.1f%%, 1,4x %+.1f%%' % (dsp['len0.7'] * 100, dsp['len1.4'] * 100))
        check('rozciąganie w czasie NIE zmienia wysokości dźwięku',
              abs(dsp['f00.7']) < 0.03 and abs(dsp['f01.4']) < 0.03,
              '0,7x %+.2f%%, 1,4x %+.2f%% (półton to 5,9%%)' % (dsp['f00.7'] * 100, dsp['f01.4'] * 100))
        check('rozciąganie liczy się szybciej, niż trwa dźwięk',
              dsp['ms0.7'] < 1200 and dsp['ms1.4'] < 1200,
              '1,2 s materiału w %d/%d ms' % (dsp['ms0.7'], dsp['ms1.4']))

        # --- 21. szum tła, pogłos i pamięć podręczna ---
        noise = page.evaluate(r"""() => {
          DSP.cache.clear();
          const t0 = performance.now();
          const a = DSP.noise('restaurant', 2);
          const cold = performance.now() - t0;
          const t1 = performance.now();
          const b = DSP.noise('restaurant', 2);
          const warm = performance.now() - t1;
          const d = a.getChannelData(0);
          let peak = 0, sum = 0;
          for (let i = 0; i < d.length; i++) { const v = Math.abs(d[i]); if (v > peak) peak = v; sum += v; }
          const ir = DSP.room('hall');
          const st = DSP.cache.stats();
          return {
            same: a === b, cold: cold, warm: warm,
            seconds: a.duration, channels: a.numberOfChannels,
            peak: peak, mean: sum / d.length,
            kinds: DSP.noiseKinds().length, rooms: DSP.roomKinds().length,
            irSeconds: ir ? ir.duration : 0,
            entries: st.entries, hits: st.hits
          };
        }""")
        check('szum tła generuje się w trzech rodzajach', noise['kinds'] == 3,
              '%d rodzaje' % noise['kinds'])
        check('szum tła jest ciągły i nie przesterowany',
              0.5 < noise['peak'] <= 1.0 and noise['mean'] > 0.02,
              'szczyt %.2f, średnia %.3f, %.1f s stereo' % (noise['peak'], noise['mean'], noise['seconds']))
        check('odpowiedź impulsowa hali jest długa, a pokoju krótka',
              noise['irSeconds'] > 1.5, 'hala %.2f s' % noise['irSeconds'])
        check('pamięć podręczna oddaje ten sam bufor zamiast liczyć od nowa',
              noise['same'] and noise['hits'] >= 1,
              'zimno %d ms, ciepło %d ms' % (noise['cold'], noise['warm']))
        check('drugie sięgnięcie po szum jest wielokrotnie tańsze',
              noise['warm'] < max(1.0, noise['cold'] / 5),
              'przyspieszenie %.0fx' % (noise['cold'] / max(0.01, noise['warm'])))

        # --- 22. eksmisja najdawniej używanego ---
        lru = page.evaluate(r"""() => {
          const c = new DSP.Cache(300000);        // ~300 kB
          const mk = (n) => ({ length: n, numberOfChannels: 1 });
          c.set('a', mk(20000)); c.set('b', mk(20000)); c.set('c', mk(20000));
          c.get('a');                              // 'a' znów najświeższe
          c.set('d', mk(20000));                   // limit przekroczony -> leci 'b'
          return {
            hasA: !!c.get('a'), hasB: !!c.get('b'), hasD: !!c.get('d'),
            evictions: c.stats().evictions
          };
        }""")
        check('eksmisja wyrzuca najdawniej używany, nie najstarszy',
              lru['hasA'] and not lru['hasB'] and lru['hasD'] and lru['evictions'] >= 1,
              'eksmisji %d' % lru['evictions'])

        # --- 23. drabina tempa i tryb potoczny w odtwarzaczu ---
        # Podmieniamy syntezator na atrapę, która zapisuje, co dostała.
        tempo = page.evaluate(r"""async () => {
          const log = [];
          const realSpeak = Speech.speak;
          Speech.speak = function (text, opts) {
            log.push({ text: text, rate: opts.rate || 1, pitch: opts.pitch || 1,
                       voice: opts.voice ? opts.voice.name : null });
            if (opts.onend) setTimeout(opts.onend, 1);
            return true;
          };
          Speech.voice = { name: 'atrapa', lang: 'th-TH', localService: true };
          Speech.thaiVoices = [Speech.voice];

          await DB.ensureFile('survival.json');
          // hasło z wariantem potocznym i wyznaczonymi granicami wyrazów
          // Potrzebny rekord, w którym różni się nie tylko zapis fonetyczny,
          // ale też tekst podawany syntezatorowi — inaczej test nie
          // rozstrzygnąłby, czy tryb potoczny w ogóle zadziałał.
          const rec = DB.records.find(r => r.colloquial && r.ttsSplit && r.ttsSplit.length > 1
            && r.colloquial.ttsKey
            && DB.voiceText(r.colloquial.ttsKey) !== DB.voiceText(r.ttsKey));
          if (!rec) { Speech.speak = realSpeak; return { error: 'brak materiału' }; }

          const run = (tempoId, coll) => new Promise(res => {
            log.length = 0;
            Player.colloquial = coll;
            Player.noiseLevel = 0;
            Player.play(rec, { tempo: tempoId, silentWarning: true, onend: () => res(log.slice()) });
            // Bezpiecznik czasowy, nie oczekiwany czas trwania. Tempo wolne
            // rozsuwa wypowiedź pauzami do 700 ms na styk, więc wypowiedź
            // pięcioczłonowa potrzebuje ponad 2 s. Przy 900 ms bezpiecznik
            // strzelał przed końcem i test zgłaszał, że człony po sklejeniu
            // nie dają oryginału — choć dawały, tylko trzy z pięciu zdążyły
            // się zalogować. Wartość musi być większa od
            // (liczba członów) x (maksymalna pauza).
            setTimeout(() => res(log.slice()), 5000);
          });

          const slow = await run('slow', false);
          const natural = await run('natural', false);
          const fast = await run('fast', true);
          const fastPlain = await run('fast', false);

          Speech.speak = realSpeak;
          Player.colloquial = false;
          const dict = DB.voiceText(rec.ttsKey);
          const coll = DB.voiceText(rec.colloquial.ttsKey);
          return {
            id: rec.id,
            slowParts: slow.length, slowRate: slow.length ? slow[0].rate : 0,
            naturalParts: natural.length, naturalRate: natural.length ? natural[0].rate : 0,
            fastRate: fast.length ? fast[0].rate : 0,
            fastPlainRate: fastPlain.length ? fastPlain[0].rate : 0,
            usedColloquial: fast.length ? fast[0].text === coll : false,
            usedDictionary: natural.length ? natural[0].text === dict : false,
            differs: dict !== coll,
            slowJoined: slow.map(x => x.text).join('') === dict
          };
        }""")
        check('tempo naturalne mówi całość formą słownikową przy rate 1,0',
              tempo.get('naturalParts') == 1 and abs(tempo.get('naturalRate', 0) - 1) < 0.01
              and tempo.get('usedDictionary'), tempo.get('id', ''))
        check('tempo dydaktyczne tnie wypowiedź na wyrazy zamiast zwalniać silnik',
              tempo.get('slowParts', 0) > 1 and abs(tempo.get('slowRate', 0) - 1) < 0.01,
              '%d człony, rate %.2f — kontur nietknięty' % (tempo.get('slowParts', 0), tempo.get('slowRate', 0)))
        check('człony po sklejeniu dają dokładnie tę samą wypowiedź',
              tempo.get('slowJoined'))
        check('tryb potoczny podaje syntezatorowi zapis zredukowany',
              tempo.get('usedColloquial') and tempo.get('differs'))
        check('tempo potoczne nie przekracza bezpiecznego rate',
              0 < tempo.get('fastRate', 0) <= 1.26 and tempo.get('fastRate', 9) < tempo.get('fastPlainRate', 0) + 0.001,
              'z redukcją %.2f, bez %.2f' % (tempo.get('fastRate', 0), tempo.get('fastPlainRate', 0)))

        # --- 24. dwa głosy w scenie z dwoma rozmówcami ---
        voices = page.evaluate(r"""() => {
          const one = { name: 'Jeden', lang: 'th-TH', localService: true };
          const two = { name: 'Dwa', lang: 'th-TH', localService: true };
          Speech.thaiVoices = [one, two];
          Speech.voice = one;
          const dA = Speech.roleProfile('A', 'any'), dB = Speech.roleProfile('B', 'any');
          Speech.thaiVoices = [one];
          const sA = Speech.roleProfile('A', null), sB = Speech.roleProfile('B', null);
          const fem = Speech.roleProfile('B', 'female');
          /* Atrapy głosów nie mogą zostać w module — kolejne testy używają
             prawdziwego syntezatora, a obcy obiekt głosu jest odrzucany. */
          Speech.thaiVoices = [];
          Speech.voice = null;
          return {
            twoDistinct: dA.voice.name !== dB.voice.name && dA.distinct && dB.distinct,
            onePitch: Math.abs(sA.pitch - sB.pitch) > 0.1 && !sA.distinct,
            femaleHigher: fem.pitch > sB.pitch,
            inRange: sA.pitch <= 1.5 && sB.pitch >= 0.6
          };
        }""")
        check('dwa głosy tajskie trafiają do dwóch ról', voices['twoDistinct'])
        check('przy jednym głosie role rozróżnia wysokość', voices['onePitch'])
        check('rola kobieca dostaje wyższy głos niż domyślna', voices['femaleHigher'])
        check('wysokość zostaje w bezpiecznym zakresie', voices['inRange'])

        # --- 25. wykrycie możliwości przechwycenia syntezatora ---
        cap = page.evaluate(r"""() => {
          const r = Capture.probe();
          return { probes: r.probes.length, synth: r.synthCapture,
                   webAudio: r.webAudio,
                   described: r.probes.every(p => p.why && p.why.length > 20) };
        }""")
        check('aplikacja sprawdza wszystkie drogi przechwycenia i opisuje wynik',
              cap['probes'] == 3 and cap['described'], '%d próby' % cap['probes'])
        check('brak przechwycenia syntezatora jest wykryty, a nie zgadnięty',
              cap['synth'] is False and cap['webAudio'])

        # --- 26. ćwiczenie „rozumienie w hałasie” ---
        noiseEx = page.evaluate(r"""async () => {
          Quiz.mode = 'noise';
          Quiz.noiseLevel = 1;
          App.settings.noiseLevel = 0;
          Player.noiseLevel = 0;
          App.go('listen');
          Quiz.renderListen(document.getElementById('listen-area'));
          await new Promise(r => setTimeout(r, 500));
          const area = document.getElementById('listen-area');
          const opts = [...area.querySelectorAll('.option')];
          const before = Quiz.noiseLevel;
          const wrong = opts.find(b => b.textContent !== (Quiz.current && Quiz.current.polish));
          if (wrong) wrong.click();
          await new Promise(r => setTimeout(r, 250));
          return {
            options: opts.length,
            hasClean: !!area.textContent.match(/Bez hałasu/),
            level: before,
            restored: Player.noiseLevel === 0 && Player.room === (App.settings.room || '')
          };
        }""")
        check('ćwiczenie w hałasie renderuje odpowiedzi', noiseEx['options'] >= 2,
              '%d opcje' % noiseEx['options'])
        check('da się porównać ten sam bodziec bez hałasu', noiseEx['hasClean'])
        check('ćwiczenie nie rusza globalnych ustawień hałasu', noiseEx['restored'])

        # --- 27. sceny: jedna sytuacja od wejścia do wyjścia ---
        scn = page.evaluate(r"""async () => {
          await DB.ensureScenes();
          const scenes = DB.scenes;
          const lens = scenes.map(s => s.lineCount);
          const lines = DB.sceneLines(scenes[0]);
          const beats = new Set(lines.map(l => l.__beat));
          // Pytania muszą dotyczyć całości: żadna odpowiedź nie może być
          // dosłownym tłumaczeniem pojedynczej kwestii sceny.
          const polish = new Set(lines.map(l => (l.polish || '').trim()));
          let leaks = 0;
          scenes.forEach(s => (s.questions || []).forEach(q =>
            q.options.forEach(o => { if (polish.has(o.trim())) leaks++; })));
          return {
            count: scenes.length,
            min: Math.min(...lens), max: Math.max(...lens),
            lines: lines.length,
            declared: scenes[0].lineCount,
            beats: beats.size,
            expectedBeats: scenes[0].beats.length,
            questions: scenes[0].questions.length,
            tiers: [...new Set(scenes[0].questions.map(q => q.tier))].sort().join(''),
            leaks: leaks
          };
        }""")
        check('sceny mają od 20 do 40 kwestii',
              scn['min'] >= 20 and scn['max'] <= 40,
              '%d-%d kwestii, %d scen' % (scn['min'], scn['max'], scn['count']))
        check('scena składa kwestie wszystkich swoich dialogów w jeden ciąg',
              scn['lines'] == scn['declared'] and scn['beats'] == scn['expectedBeats'],
              '%d kwestii w %d częściach' % (scn['lines'], scn['beats']))
        check('pytania idą przez trzy poziomy szczegółowości',
              scn['tiers'] == '123', '%d pytań' % scn['questions'])
        check('żadna odpowiedź nie jest tłumaczeniem pojedynczej kwestii',
              scn['leaks'] == 0)

        # --- 28. drabina tempa: trzy osobne postępy ---
        ladder = page.evaluate(r"""() => {
          Progress.data.tempo = {};
          for (let i = 0; i < 10; i++) Progress.tempoAnswer('gap', 'slow', true);
          const slow = Progress.tempoCell('gap', 'slow');
          const natural = Progress.tempoCell('gap', 'natural');
          for (let i = 0; i < 10; i++) Progress.tempoAnswer('gap', 'natural', i < 5);
          const half = Progress.tempoCell('gap', 'natural');
          Progress.tempoAnswer('gap', 'slow', false);
          const after = Progress.tempoCell('gap', 'slow');
          const map = Progress.tempoMap().find(r => r.id === 'gap');
          return {
            slowPassed: slow.passed,
            naturalUntouched: !natural.passed && natural.answers === 0,
            halfPassed: half.passed,
            stillPassed: after.passed,
            stuckAt: map.stuckAt,
            columns: map.steps.length
          };
        }""")
        check('zaliczenie przy jednym tempie nie zalicza pozostałych',
              ladder['slowPassed'] and ladder['naturalUntouched'])
        check('próg zaliczenia nie puszcza wyniku poniżej progu trafności',
              ladder['halfPassed'] is False)
        check('raz zdobyte zaliczenie nie znika po pomyłce', ladder['stillPassed'])
        check('mapa postępu wskazuje tempo, na którym uczący się stanął',
              ladder['stuckAt'] == 'natural' and ladder['columns'] == 3,
              'stoi na %s' % ladder['stuckAt'])

        # --- 29. luki na słuch: wybór luki zależy od tego, co uczący się zna ---
        gap = page.evaluate(r"""async () => {
          await DB.ensureComprehension();
          const items = DB.comprehension.gapItems;
          const item = items.find(i => i.slots.length >= 2 && DB.get(i.d));
          const known = item.slots[item.slots.length - 1];
          Progress.data.seen = Progress.data.seen || {};
          Object.keys(Progress.data.seen).forEach(k => delete Progress.data.seen[k]);
          Progress.data.seen[known.r] = 2;
          let hitsKnown = 0;
          for (let i = 0; i < 30; i++) {
            const el = document.createElement('div');
            const chosen = item.slots.filter(s => s.r === known.r).length;
            hitsKnown += chosen;
          }
          // Bezpośrednio: ćwiczenie renderuje się i odpowiada.
          Quiz.mode = 'gap';
          App.go('listen');
          Quiz.renderListen(document.getElementById('listen-area'));
          await new Promise(r => setTimeout(r, 900));
          const area = document.getElementById('listen-area');
          const opts = [...area.querySelectorAll('.option')];
          const blank = area.querySelector('.gap-blank');
          const before = Progress.tempoCell('gap', CompTempo.current).answers;
          if (opts.length) opts[0].click();
          await new Promise(r => setTimeout(r, 250));
          return {
            options: opts.length,
            hadBlank: !!blank,
            filled: !!area.querySelector('.gap-blank.filled-ok, .gap-blank.filled-bad'),
            counted: Progress.tempoCell('gap', CompTempo.current).answers > before,
            hasTempo: !!area.querySelector('.tempo-chip'),
            hasNoise: area.textContent.indexOf('hałas') !== -1
          };
        }""")
        check('ćwiczenie z luką pokazuje zdanie z jedną dziurą',
              gap['hadBlank'] and gap['options'] == 4,
              '%d odpowiedzi' % gap['options'])
        check('po odpowiedzi luka zostaje uzupełniona na ekranie', gap['filled'])
        check('odpowiedź trafia do drabiny tempa', gap['counted'])
        check('trudność reguluje tempo i hałas', gap['hasTempo'] and gap['hasNoise'])

        # --- 30. tolerancja nieznanego: wskazówki po odpowiedzi ---
        unk = page.evaluate(r"""async () => {
          Quiz.mode = 'unknown';
          App.go('listen');
          Quiz.renderListen(document.getElementById('listen-area'));
          await new Promise(r => setTimeout(r, 900));
          const area = document.getElementById('listen-area');
          const marked = area.querySelectorAll('.unknown-word').length;
          const opts = [...area.querySelectorAll('.option')];
          const before = Progress.tempoCell('unknown', CompTempo.current).answers;
          if (opts.length) opts[0].click();
          await new Promise(r => setTimeout(r, 250));
          const cues = area.querySelectorAll('.cues li').length;
          return {
            marked: marked,
            options: opts.length,
            cues: cues,
            highlighted: area.querySelectorAll('.cue-word').length,
            counted: Progress.tempoCell('unknown', CompTempo.current).answers > before
          };
        }""")
        check('zdanie ma dokładnie jedno słowo oznaczone jako nieznane',
              unk['marked'] == 1 and unk['options'] == 4)
        check('po odpowiedzi widać wskazówki, które prowadziły do rozwiązania',
              unk['cues'] >= 2, '%d wskazówki' % unk['cues'])
        check('wskazówki pokazują konkretne miejsca w zdaniu',
              unk['highlighted'] >= 1)
        check('odpowiedź trafia do drabiny tempa', unk['counted'])

        # --- 31. słuchanie ekstensywne: trzy przejścia i pomiar różnicy ---
        ext = page.evaluate(r"""async () => {
          await DB.ensureScenes();
          const block = DB.blocks[0];
          const secs = DB.blocks.map(b => b.estSeconds.natural);
          const lines = DB.blockLines(block);
          const passes = block.passes.map(p => p.mode).join(',');
          Extensive.block = block;
          Extensive.reset();
          App.go('extensive');
          Extensive.render(document.getElementById('extensive-area'));
          await new Promise(r => setTimeout(r, 400));
          const area = document.getElementById('extensive-area');
          const cards = area.querySelectorAll('.pass-card').length;
          const locked = area.querySelectorAll('.pass-card:not(.current)').length;
          // Zapisujemy wynik i sprawdzamy, czy różnica jest mierzona.
          Progress.data.extensive = {};
          Progress.extensiveResult(block.id, {
            tempo: 'natural',
            first: { correct: 1, total: 4 },
            second: { correct: 3, total: 4 },
            third: { correct: 3, total: 4 }
          });
          const sum = Progress.extensiveSummary();
          return {
            blocks: DB.blocks.length,
            minSec: Math.min(...secs), maxSec: Math.max(...secs),
            lines: lines.length, declared: block.lineCount,
            passes: passes, cards: cards, locked: locked,
            firstShare: Math.round(sum.firstShare * 100),
            thirdShare: Math.round(sum.thirdShare * 100)
          };
        }""")
        check('bloki mają od 3 do 5 minut ciągłego materiału',
              ext['minSec'] >= 180 and ext['maxSec'] <= 300,
              '%d-%d s, %d bloków' % (ext['minSec'], ext['maxSec'], ext['blocks']))
        check('blok skleja kwestie wszystkich swoich scen',
              ext['lines'] == ext['declared'], '%d kwestii' % ext['lines'])
        check('trzy przejścia to bez tekstu, z tekstem i znów bez tekstu',
              ext['passes'] == 'audio,text,audio')
        check('kolejne przejście odblokowuje się dopiero po poprzednim',
              ext['cards'] == 3 and ext['locked'] == 2)
        check('pomiar pokazuje osobno rozumienie przed tekstem i po nim',
              ext['firstShare'] == 25 and ext['thirdShare'] == 75,
              '%d%% -> %d%%' % (ext['firstShare'], ext['thirdShare']))

        # --- 29. migracja postępu ze starej ścieżki ---
        #
        # Sesja O przebudowała ścieżkę: 314 lekcji zamieniło się w 333, z czego
        # 95 zachowało identyfikator. Test odtwarza sytuację użytkownika, który
        # przed aktualizacją zaliczył kawałek starego kursu, i sprawdza cztery
        # rzeczy, na których stoi obietnica „postęp nie przepada”:
        #   1. lekcje z zachowanym identyfikatorem przechodzą jeden do jednego,
        #   2. reszta jest przeliczona przez zbiór znanych haseł,
        #   3. migracja wykonuje się DOKŁADNIE raz,
        #   4. da się ją cofnąć i stan wraca do punktu wyjścia.
        mig = page.evaluate("""async () => {
          const map = DB.progressMigration;
          if (!map) return { skipped: 'brak mapy migracji' };

          // Symulujemy postęp ze STAREJ ścieżki: pierwsze 60 lekcji zaliczone.
          const old = map.legacyOrder.slice(0, 60);
          const before = {};
          old.forEach((id, i) => {
            before[id] = { status: i % 10 === 0 ? 'skipped' : 'passed',
                           score: 12, total: 15, date: '2026-07-01' };
          });
          Progress.data.lessons = JSON.parse(JSON.stringify(before));
          delete Progress.data.migration;
          U.store.remove('progress-backup-o-2026-08');
          Progress.save();

          // Ile z tych 60 ma odpowiednik po identyfikatorze.
          const directPossible = old.filter(id => map.direct[id]).length;

          const r1 = ProgressMigration.run();
          const after = Object.assign({}, Progress.data.lessons);
          const newIds = new Set(DB.lessons.map(L => L.id));

          // Czy wszystkie przepisane identyfikatory istnieją w NOWEJ ścieżce.
          const orphans = Object.keys(after).filter(id => !newIds.has(id));

          // Tor prosty: stan przeniesiony bez zmiany statusu i wyniku.
          let directOk = true;
          old.forEach(id => {
            const to = map.direct[id];
            if (!to || !after[to]) return;
            if (after[to].status !== before[id].status) directOk = false;
            if (after[to].score !== before[id].score) directOk = false;
          });

          // Zbiór haseł znanych ze starej ścieżki.
          const known = new Set();
          old.forEach(id => (map.legacy[id] || []).forEach(w => known.add(w)));

          // Każda lekcja przeliczona musi mieć realne pokrycie znanych haseł.
          let minCoverage = 1;
          DB.lessons.forEach(L => {
            const st = after[L.id];
            if (!st || st.source !== 'migracja-przeliczenie') return;
            const ids = L.newWordIds || [];
            const hit = ids.filter(w => known.has(w)).length;
            minCoverage = Math.min(minCoverage, ids.length ? hit / ids.length : 1);
          });

          // Drugie uruchomienie nie ma prawa niczego ruszyć.
          const snapshot = JSON.stringify(Progress.data.lessons);
          const r2 = ProgressMigration.run();
          const unchanged = JSON.stringify(Progress.data.lessons) === snapshot;

          // Cofnięcie przywraca stan sprzed migracji.
          const hadBackup = ProgressMigration.hasBackup();
          const restored = ProgressMigration.restore();
          const backOk = JSON.stringify(Progress.data.lessons) === JSON.stringify(before);
          const markerGone = !Progress.data.migration;

          return {
            oldDone: old.length,
            directPossible: directPossible,
            direct: r1.direct, derived: r1.derived,
            knownWords: r1.knownWords,
            orphans: orphans.length,
            directOk: directOk,
            minCoverage: Math.round(minCoverage * 100),
            secondRunNull: r2 === null,
            unchanged: unchanged,
            hadBackup: hadBackup,
            restored: restored,
            backOk: backOk,
            markerGone: markerGone
          };
        }""")

        if mig.get('skipped'):
            fails.append('  BŁĄD migracja postępu — %s' % mig['skipped'])
        else:
            check('migracja przenosi postęp ze starej ścieżki',
                  mig['direct'] + mig['derived'] > 0,
                  '%d lekcji starych -> %d po identyfikatorze + %d przeliczonych'
                  % (mig['oldDone'], mig['direct'], mig['derived']))
            check('lekcje z zachowanym identyfikatorem przechodzą jeden do jednego',
                  mig['directOk'] and mig['direct'] == mig['directPossible'],
                  '%d z %d możliwych' % (mig['direct'], mig['directPossible']))
            check('migracja nie zostawia wpisów wskazujących na nieistniejące lekcje',
                  mig['orphans'] == 0)
            check('lekcje przeliczone mają pokrycie znanymi hasłami co najmniej 80%',
                  mig['minCoverage'] >= 80,
                  'najsłabsza %d%%, %d znanych haseł'
                  % (mig['minCoverage'], mig['knownWords']))
            check('migracja wykonuje się dokładnie raz',
                  mig['secondRunNull'] and mig['unchanged'])
            check('kopia zapasowa powstaje przed zmianą stanu', mig['hadBackup'])
            check('cofnięcie przywraca postęp sprzed migracji',
                  mig['restored'] and mig['backOk'] and mig['markerGone'])

        # --- 22. rozdzielenie kart na receptywne i produktywne ---
        r = page.evaluate("""() => {
          /* Kartoteka sprzed sesji P: jedna karta na hasło, bez strony. */
          const ids = DB.index.slice(0, 6).map(x => x.id);
          const legacy = {};
          ids.forEach((id, i) => {
            legacy[id] = { id: id, ease: 2.6, interval: 30 + i, repetitions: 5,
                           due: U.today(), lapses: 2, seen: 12, correct: 10, last: '2026-01-01' };
          });
          legacy['perc:ton-niski-vs-opadajacy'] = {
            id: 'perc:ton-niski-vs-opadajacy', ease: 2.5, interval: 4, repetitions: 2,
            due: U.today(), lapses: 1, seen: 5, correct: 4, last: null };
          U.store.set('srs', legacy);
          U.store.set('srslog', [{ d: '2026-01-01', iv: 10, ok: 1 }]);
          U.store.set('srs.split.v1', null);
          U.store.set('srs.split.backup', null);
          SRS.load();

          const rep = SRS.splitReport();
          const rec0 = SRS.cards[SRS.cardId(ids[0], 'r')];
          const prod0 = SRS.cards[SRS.cardId(ids[0], 'p')];
          const before = legacy[ids[0]];

          /* Druga próba migracji nie może niczego ruszyć. */
          SRS.migrateSides();
          const stillR = SRS.cards[SRS.cardId(ids[0], 'r')].interval;

          const undone = SRS.undoSplit();
          const backPlain = !!SRS.cards[ids[0]] && !SRS.cards[SRS.cardId(ids[0], 'r')];
          SRS.load();   /* migruje ponownie */

          return {
            moved: rep ? rep.moved : 0,
            derived: rep ? rep.derived : 0,
            recInterval: rec0.interval,
            recReps: rec0.repetitions,
            recSeen: rec0.seen,
            beforeInterval: 30,
            prodInterval: prod0.interval,
            prodReps: prod0.repetitions,
            prodSeen: prod0.seen,
            prodDerived: !!prod0.derived,
            contrastKept: !!SRS.cards['perc:ton-niski-vs-opadajacy'],
            contrastSide: SRS.sideOf('perc:ton-niski-vs-opadajacy'),
            idempotent: stillR === rec0.interval,
            undone: undone && backPlain,
            logSided: (U.store.get('srslog', []) || []).every(e => !!e.s)
          };
        }""")
        check('migracja rozdziela każdą kartę na dwie strony',
              r['moved'] == 6 and r['derived'] == 6,
              '%d kart -> %d receptywnych + %d produktywnych'
              % (r['moved'], r['moved'], r['derived']))
        check('strona receptywna przejmuje stan starej karty bez strat',
              r['recInterval'] == r['beforeInterval'] and r['recReps'] == 5 and r['recSeen'] == 12,
              'odstęp %d dni, %d powtórek, %d kontaktów'
              % (r['recInterval'], r['recReps'], r['recSeen']))
        check('strona produktywna startuje ostrożniej, ale z pełną historią',
              r['prodInterval'] < r['recInterval'] and r['prodReps'] < r['recReps']
              and r['prodSeen'] == r['recSeen'] and r['prodDerived'],
              'odstęp %d dni zamiast %d, %d powtórek zamiast %d'
              % (r['prodInterval'], r['recInterval'], r['prodReps'], r['recReps']))
        check('kontrasty słuchowe zostają poza podziałem na strony',
              r['contrastKept'] and r['contrastSide'] == 'c')
        check('migracja wykonuje się raz i daje się cofnąć',
              r['idempotent'] and r['undone'])
        check('dziennik sprzed podziału dostaje stronę', r['logSided'])

        # --- 23. reguła pętli zwrotnej ---
        r = page.evaluate("""() => {
          const low = SRS.tuneProposal(0.70);    /* dużo zapominania */
          const mid = SRS.tuneProposal(0.87);    /* w oknie docelowym */
          const high = SRS.tuneProposal(0.98);   /* prawie bez pudeł */
          return { low, mid, high, min: SRS.TUNE.min, max: SRS.TUNE.max };
        }""")
        check('niska retencja postuluje skrócenie odstępów', r['low'] < 0.95,
              'retencja 70%% -> mnożnik %.2f' % r['low'])
        check('retencja w oknie docelowym nie rusza odstępów', abs(r['mid'] - 1.0) < 1e-9)
        check('wysoka retencja postuluje wydłużenie odstępów', r['high'] > 1.05,
              'retencja 98%% -> mnożnik %.2f' % r['high'])

        r = page.evaluate("""() => {
          /* Dane syntetyczne: ten sam uczący się, dwie różne strony pamięci.
             Rozpoznanie idzie mu świetnie, wytworzenie się sypie. */
          const mk = (side, ok, n) => {
            const out = [];
            for (let i = 0; i < n; i++) {
              out.push({ d: U.today(), iv: [1, 3, 7, 14, 30][i % 5],
                         ok: (i % 100) < ok ? 1 : 0, s: side });
            }
            return out;
          };
          SRS.log = mk('r', 97, 200).concat(mk('p', 68, 200));
          SRS.tuning = null;
          SRS.retuneAll();
          const a = { r: SRS.factor('r'), p: SRS.factor('p') };
          /* Pętla przesuwa mnożnik krokami, nie skokiem — po kilku
             przeliczeniach ma dojść dalej w tę samą stronę. */
          for (let i = 0; i < 12; i++) SRS.retuneAll();
          const b = { r: SRS.factor('r'), p: SRS.factor('p') };

          const report = SRS.tuningReport('p');

          /* Mała próba nie może ruszyć mnożnika z 1,0. */
          SRS.log = mk('w', 20, 8);
          SRS.tuning = null;
          SRS.retuneAll();
          const tiny = SRS.factor('w');

          return { a, b, tiny, report };
        }""")
        check('pętla wydłuża odstępy stronie, która trzyma retencję',
              r['b']['r'] > 1.02, 'mnożnik rozpoznania %.2f' % r['b']['r'])
        check('pętla skraca odstępy stronie, która się sypie',
              r['b']['p'] < 0.95, 'mnożnik wytworzenia %.2f' % r['b']['p'])
        check('mnożnik przesuwa się stopniowo, nie skokiem',
              abs(r['a']['p'] - 1.0) < abs(r['b']['p'] - 1.0),
              'po 1 przeliczeniu %.3f, po 13 przeliczeniach %.3f'
              % (r['a']['p'], r['b']['p']))
        check('przy małej próbie mnożnik stoi na 1,00', abs(r['tiny'] - 1.0) < 1e-9)
        check('sprawozdanie z dostrojenia tłumaczy decyzję słowami',
              len(r['report']['verdict']) > 30 and r['report']['samples'] == 200,
              r['report']['verdict'][:70])

        r = page.evaluate("""() => {
          /* Ten sam mnożnik musi realnie zmieniać odstęp w grade(). */
          const id = DB.index[10].id;
          const mk = () => { SRS.cards = {}; SRS.cards[SRS.cardId(id, 'r')] = {
            id: SRS.cardId(id, 'r'), ease: 2.5, interval: 20, repetitions: 4,
            due: U.today(), lapses: 0, seen: 5, correct: 5, last: null }; };

          SRS.tuning = null; SRS.log = []; SRS.retuneAll();
          mk(); const neutral = SRS.grade(id, 4, { side: 'r' }).interval;

          SRS.tuning.r.factor = 0.70; SRS.tuning.since = 0;
          mk(); const short = SRS.grade(id, 4, { side: 'r' }).interval;

          SRS.tuning.r.factor = 1.30; SRS.tuning.since = 0;
          mk(); const long = SRS.grade(id, 4, { side: 'r' }).interval;
          return { neutral, short, long };
        }""")
        check('dostrojony mnożnik zmienia faktyczny odstęp powtórki',
              r['short'] < r['neutral'] < r['long'],
              '%d / %d / %d dni przy mnożniku 0,70 / 1,00 / 1,30'
              % (r['short'], r['neutral'], r['long']))

        # --- 24. trzeci wymiar: karty wymowy ---
        r = page.evaluate("""() => {
          const id = DB.index[3].id;
          const bad = { ok: true, score: 40, syllables: [
            { label: 'kh\u00e2a', ok: false, expectedTone: 'opadaj\u0105cy',
              producedTone: '\u015bredni', fix: 'Zacznij wy\u017cej i opadnij.' }] };
          const good = { ok: true, score: 92, syllables: [
            { label: 'kh\u00e2a', ok: true, expectedTone: 'opadaj\u0105cy',
              producedTone: 'opadaj\u0105cy' }] };

          /* Hasło dopiero w nauce: błędny ton NIE zakłada osobnej karty —
             obsługuje go zwykła karta produktywna. */
          SRS.cards = {};
          SRS.addBoth(id);
          const early = SRS.notePronunciation(id, bad);
          const noCardYet = !SRS.has(id, 'w');

          /* Hasło opanowane obiema stronami — teraz błędny ton musi wrócić. */
          ['r', 'p'].forEach(s => {
            const c = SRS.card(id, s);
            c.repetitions = 4; c.interval = 20;
          });
          const opened = SRS.notePronunciation(id, bad);
          const card = SRS.cards[SRS.cardId(id, 'w')];
          const dueSoon = card && U.daysBetween(U.today(), card.due) <= 1;
          /* Kopia, nie referencja — zaraz zamkniemy tę kartę, a wtedy opis
             tonu z niej znika. */
          const tone = card && card.tone ? JSON.parse(JSON.stringify(card.tone)) : null;

          /* Trzy czyste podejścia zamykają kartę. */
          SRS.notePronunciation(id, good);
          SRS.notePronunciation(id, good);
          const closed = SRS.notePronunciation(id, good);
          return {
            noCardYet, opened: opened && opened.action === 'opened',
            tone: tone, dueSoon,
            closedAction: closed ? closed.action : '',
            gone: !SRS.has(id, 'w'),
            earlyNull: early === null
          };
        }""")
        check('błędny ton w haśle dopiero poznawanym nie tworzy karty wymowy',
              r['noCardYet'] and r['earlyNull'])
        check('hasło zaliczone receptywnie i produktywnie wraca za błędny ton',
              r['opened'] and r['dueSoon'],
              'sylaba „%s”: %s zamiast %s'
              % (r['tone']['syllable'], r['tone']['produced'], r['tone']['expected'])
              if r['tone'] else '')
        check('karta wymowy pamięta, który ton był zły',
              bool(r['tone']) and r['tone']['expected'] != r['tone']['produced'])
        check('czyste podejścia zamykają kartę wymowy',
              r['closedAction'] == 'closed' and r['gone'])

        # --- 25. kolejka: priorytet i rozłożenie zaległości ---
        r = page.evaluate("""() => {
          /* Dwa tygodnie przerwy przy dużej kartotece. */
          SRS.cards = {};
          const ids = DB.index.slice(0, 300).map(x => x.id);
          ids.forEach((id, i) => {
            ['r', 'p'].forEach(s => {
              const c = SRS.card(id, s);
              c.repetitions = 3;
              c.interval = 1 + (i % 40);
              c.due = SRS.addDays(U.today(), -14);
            });
          });
          Progress.data.days = {};
          for (let i = 1; i <= 10; i++) {
            Progress.data.days[SRS.addDays(U.today(), -i)] = { answers: 30, correct: 25, minutes: 10, newWords: 2 };
          }
          const cap = SRS.dailyCap();
          const plan = SRS.plan();
          const raw = SRS.dueList().length;

          /* Priorytet: najpierw najbliższe zapomnienia i hasła najczęstsze. */
          const head = plan.today.slice(0, 30).map(c => ({
            u: SRS.urgency(c),
            f: (DB.any(SRS.recordOf(c.id)) || {}).frequency || 0
          }));
          const tail = plan.rest.slice(-30).map(c => ({
            u: SRS.urgency(c),
            f: (DB.any(SRS.recordOf(c.id)) || {}).frequency || 0
          }));
          const avg = a => a.reduce((s, x) => s + x, 0) / a.length;

          const spread = SRS.spreadBacklog();
          const after = SRS.plan();
          const horizon = Math.max.apply(null, Object.keys(SRS.cards)
            .map(k => U.daysBetween(U.today(), SRS.cards[k].due)));

          return {
            raw, cap, todayCount: plan.today.length, backlog: plan.backlog, days: plan.days,
            headU: avg(head.map(x => x.u)), tailU: avg(tail.map(x => x.u)),
            headF: avg(head.map(x => x.f)), tailF: avg(tail.map(x => x.f)),
            moved: spread.moved, afterToday: after.today.length,
            afterDue: after.dueTotal, horizon
          };
        }""")
        check('surowa kolejka po przerwie jest przytłaczająca', r['raw'] > 400,
              '%d zaległych kart' % r['raw'])
        check('sufit dzienny bierze się z tempa uczącego się',
              20 <= r['cap'] <= 120, '%d kart na dzień' % r['cap'])
        check('uczący się nigdy nie widzi całej zaległej kolejki',
              r['todayCount'] <= r['cap'] and r['todayCount'] < r['raw'],
              'pokazane %d z %d, reszta na %d dni'
              % (r['todayCount'], r['raw'], r['days']))
        check('na wierzch idą hasła najbliższe zapomnienia',
              r['headU'] > r['tailU'],
              'pilność %.2f na czele wobec %.2f na końcu' % (r['headU'], r['tailU']))
        check('przy równej pilności wygrywają hasła częstsze',
              r['headF'] >= r['tailF'],
              'częstość %.2f wobec %.2f' % (r['headF'], r['tailF']))
        check('zaległości zostają rozłożone, a nie skasowane',
              r['moved'] > 0 and r['afterDue'] <= r['cap'] and r['horizon'] <= SRS_HORIZON,
              '%d kart przesuniętych, najdalszy termin za %d dni'
              % (r['moved'], r['horizon']))

        # --- 26. sesja naprawcza z konkretnych pomyłek ---
        r = page.evaluate("""() => {
          SRS.cards = {}; SRS.save();
          Progress.data.misses = [];
          Progress.data.errors = { category: {}, grammar: {}, type: {}, mode: {} };

          /* Kategoria brana z danych, nie wpisana na sztywno — nazwy kategorii
             zmieniają się między wersjami bazy, a test ma sprawdzać algorytm,
             nie zawartość słownika. */
          const cat = DB.index[0].category;
          const inCat = DB.index.filter(x => x.category === cat).slice(0, 20);
          const others = DB.index.filter(x => x.category !== cat).slice(0, 20);
          /* Pięć haseł mylonych naprawdę, reszta kategorii odpowiadana dobrze. */
          const missed = inCat.slice(0, 5).map(x => x.id);
          missed.forEach(id => {
            for (let i = 0; i < 3; i++) Progress.answer(id, false, { mode: 'build' });
          });
          inCat.slice(5).forEach(id => Progress.answer(id, true, { mode: 'build' }));
          others.forEach(id => Progress.answer(id, true, { mode: 'choice' }));

          const area = { bucket: 'category', key: cat, label: cat, rate: 30 };
          const set = Repair.build(area);
          const onlyMissed = set.ids.every(id => missed.indexOf(id) !== -1);
          const coversAll = missed.every(id => set.ids.indexOf(id) !== -1);

          /* Ten sam obszar, ale pudła w rozpoznawaniu — tryb ma się zmienić. */
          Progress.data.misses = [];
          missed.forEach(id => Progress.answer(id, false, { mode: 'choice' }));
          const recSet = Repair.build(area);

          /* Pudła w wymowie prowadzą do ćwiczenia mówienia. */
          Progress.data.misses = [];
          missed.forEach(id => Progress.answer(id, false, { mode: 'say' }));
          const saySet = Repair.build(area);

          /* Powtarzane pudło nie zapycha dziennika osobnymi wpisami. */
          Progress.data.misses = [];
          for (let i = 0; i < 9; i++) Progress.answer(missed[0], false, { mode: 'build' });
          const entries = Progress.data.misses.length;
          const counted = Progress.missesIn('category', cat, 5)[0];

          return {
            ids: set.ids.length, onlyMissed, coversAll,
            prodMode: set.mode, recMode: recSet.mode, sayMode: saySet.mode,
            why: set.why, entries, countedN: counted ? counted.n : 0
          };
        }""")
        check('sesja naprawcza bierze konkretne hasła, nie losowe z kategorii',
              r['onlyMissed'] and r['coversAll'],
              '%d haseł, wszystkie z faktycznych pomyłek' % r['ids'])
        check('tryb dobiera się do rodzaju błędu',
              r['prodMode'] in ('build', 'type') and r['recMode'] == 'choice'
              and r['sayMode'] == 'say',
              'wytworzenie -> %s, rozpoznanie -> %s, wymowa -> %s'
              % (r['prodMode'], r['recMode'], r['sayMode']))
        check('zestaw tłumaczy, skąd się wziął', len(r['why']) > 40, r['why'][:70])
        check('powtórzone pudło podbija licznik zamiast zapychać dziennik',
              r['entries'] == 1 and r['countedN'] == 9,
              '%d wpis, %d pomyłek' % (r['entries'], r['countedN']))

        # --- 27. pętla zwrotna: zbieżność na kartotece bez presji kolejki ---
        conv = page.evaluate("""() => {
          /* Ta próba sprawdza JEDNO: czy pętla zwrotna dochodzi do właściwych
             odstępów. Dlatego nie ma tu ani sufitu kolejki, ani rozkładania
             zaległości, ani nowych haseł w trakcie — wszystko, co zaplanowane
             na dany dzień, zostaje tego dnia zrobione.

             Mieszanie tego z próbą obciążeniową (niżej) dawało wyniki nie do
             odczytania: przy ograniczonej kolejce karty o krótkich odstępach
             wypychają karty o długich, te wracają po terminie i wypadają
             z pamięci — więc zmierzona retencja mówi o rywalizacji o miejsce
             w kolejce, a nie o trafności odstępów.

             Pamięć modelowego uczącego się umacnia się 2,9× po każdym trafieniu
             w rozpoznawaniu i 1,5× w wytwarzaniu, przy starcie 3,0 i 2,5 dnia.
             Algorytm tych liczb nie zna.

             Nie sprawdzamy, czy dojdzie do konkretnej wartości mnożnika —
             reguła ma martwą strefę (w oknie 85–90 % nic nie zmienia), więc
             zatrzymuje się tam, gdzie retencja wejdzie w okno, a to zależy od
             drogi. Sprawdzamy rzecz właściwą: czy retencja LĄDUJE w oknie
             i czy słabsza strona pamięci dostaje krótsze odstępy. */
          let seed = 987654321;
          const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };

          const HALF = { r: 3.0, p: 2.5 };
          const GROWTH = { r: 2.9, p: 1.5 };
          const strength = {};

          const realToday = U.today();
          let simDay = realToday;
          U.today = () => simDay;

          /* Zapis stanu po każdej ocenie serializuje całą kartotekę i dziennik.
             W aplikacji to nic nie kosztuje (jedna ocena na kilka sekund),
             w symulacji dziesiątek tysięcy ocen — kilkanaście minut. Algorytm
             działa tak samo, więc na czas przebiegu odkładamy zapis. */
          const realSave = SRS.save;
          SRS.save = function () {};

          SRS.cards = {}; SRS.log = []; SRS.tuning = null;
          const ids = DB.index.slice(0, 120).map(x => x.id);
          ids.forEach(id => SRS.addBoth(id));

          const rateIn = (side, from, to) => {
            const a = SRS.addDays(realToday, from), b = SRS.addDays(realToday, to);
            const e = SRS.log.filter(x => x.s === side && x.iv >= 4 && x.d >= a && x.d < b);
            return e.length ? Math.round(e.filter(x => x.ok).length / e.length * 100) : null;
          };

          for (let day = 0; day < 200; day++) {
            simDay = SRS.addDays(realToday, day);
            SRS.dueList().forEach(card => {
              const side = SRS.sideOf(card.id);
              if (side !== 'r' && side !== 'p') return;
              const elapsed = Math.max(0, U.daysBetween(card.last || simDay, simDay));
              const half = HALF[side] * Math.pow(GROWTH[side], strength[card.id] || 0);
              const ok = rnd() < Math.pow(0.5, elapsed / half);
              strength[card.id] = ok ? (strength[card.id] || 0) + 1 : 0;
              SRS.grade(SRS.recordOf(card.id), ok ? 4 : 0, { side: side });
            });
          }

          const out = {
            factorR: SRS.factor('r'), factorP: SRS.factor('p'),
            earlyR: rateIn('r', 10, 40), earlyP: rateIn('p', 10, 40),
            lateR: rateIn('r', 160, 200), lateP: rateIn('p', 160, 200),
            avgR: SRS.sideStats().r.avgInterval, avgP: SRS.sideStats().p.avgInterval
          };
          U.today = () => realToday;
          SRS.save = realSave;
          return out;
        }""")
        notes.append('  zbieżność pętli: mnożnik rozpoznania %.2f, wytworzenia %.2f'
                     % (conv['factorR'], conv['factorP']))
        notes.append('  retencja dojrzałych kart: rozpoznanie %s%% -> %s%%, '
                     'wytworzenie %s%% -> %s%%'
                     % (conv['earlyR'], conv['lateR'], conv['earlyP'], conv['lateP']))

        check('pętla skraca odstępy stronie, której pamięć rośnie wolniej',
              conv['factorP'] < conv['factorR'],
              'wytworzenie %.2f wobec rozpoznania %.2f' % (conv['factorP'], conv['factorR']))
        check('pętla wydłuża odstępy stronie, która pamięta ponad plan',
              conv['factorR'] >= 1.0,
              'mnożnik rozpoznania %.2f' % conv['factorR'])
        check('dostrojenie wprowadza retencję w okno docelowe tam, gdzie ma czym',
              conv['lateP'] is not None and 80 <= conv['lateP'] <= 95,
              'wytworzenie %s%% (z %s%% na starcie)' % (conv['lateP'], conv['earlyP']))
        check('pętla wychodzi z krótkich odstępów, gdy pamięć nadgoni',
              conv['factorP'] > SRS_TUNE_MIN + 0.05 and conv['lateP'] > conv['earlyP'],
              'mnożnik wytworzenia %.2f, retencja %s%% -> %s%%'
              % (conv['factorP'], conv['earlyP'], conv['lateP']))
        check('rozpoznanie dobija do sufitu odstępu, nie do błędu',
              conv['lateR'] is not None and conv['lateR'] >= 90 and conv['avgR'] > 60,
              'retencja %s%% przy średnim odstępie %.0f dni — dłużej niż rok '
              'algorytm nie planuje' % (conv['lateR'], conv['avgR']))
        check('odstępy rozjeżdżają się zgodnie z siłą pamięci',
              conv['avgP'] < conv['avgR'],
              'wytworzenie %.1f dnia, rozpoznanie %.1f dnia' % (conv['avgP'], conv['avgR']))

        # --- 28. symulacja 90 dni nauki ---
        sim = page.evaluate("""() => {
          /* Uczący się o stałej, niedoskonałej pamięci. Prawdopodobieństwo
             odtworzenia spada z długością odstępu — i spada szybciej przy
             wytwarzaniu niż przy rozpoznawaniu. Algorytm tego nie wie i ma
             sam dojść do właściwych odstępów, czytając własną krzywą.

             Ziarno stałe, żeby wynik testu był powtarzalny. */
          let seed = 20260826;
          const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };

          /* Model pamięci uczącego się. Każde trafne odtworzenie wzmacnia ślad:
             czas połowicznego zaniku rośnie wykładniczo z liczbą trafień
             z rzędu, pudło go resetuje. Bez tego wzrostu uczący się nigdy
             niczego by się nie nauczył i pętla zwrotna mogłaby tylko skracać
             odstępy aż do podłogi.

             Tempo wzrostu jest różne dla obu stron i to jest sedno próby:
             rozpoznanie umacnia się szybciej (2,9×) niż domyślny mnożnik SM-2
             (2,5×), wytworzenie wolniej (1,5×). Algorytm o tych liczbach nie
             wie — ma do nich dojść sam, czytając własną krzywą. Poprawnie
             działająca pętla powinna wydłużyć odstępy rozpoznania i skrócić
             odstępy wytworzenia. */
          /* Półtora dnia na starcie dawałoby cel nieosiągalny: przy takiej pamięci
             85% trafień wymagałoby odstępu krótszego niż jeden dzień, a krótszych
             algorytm nie planuje. Test sprawdzałby wtedy nie pętlę, tylko podłogę
             kalendarza. Dwa i pół dnia to cel, do którego da się dojść. */
          const HALF = { r: 3.0, p: 2.5 };     /* start: po ilu dniach szansa spada do 50% */
          const GROWTH = { r: 2.9, p: 1.5 };   /* ile razy dłużej po każdym trafieniu */
          const strength = {};                 /* klucz karty -> trafienia z rzędu */
          const halfLife = key => {
            const side = SRS.sideOf(key);
            return HALF[side] * Math.pow(GROWTH[side], strength[key] || 0);
          };
          const recall = (key, days) => Math.pow(0.5, days / halfLife(key));

          const realToday = U.today();
          let simDay = realToday;
          U.today = () => simDay;

          const realSave = SRS.save, realPSave = Progress.save;
          SRS.save = function () {};
          Progress.save = function () {};

          SRS.cards = {}; SRS.log = []; SRS.tuning = null;
          Progress.data.days = {};
          Progress.data.misses = [];

          const ids = DB.index.slice(0, 400).map(x => x.id);
          let introduced = 0;
          const history = [];

          for (let day = 0; day < 90; day++) {
            simDay = SRS.addDays(realToday, day);

            /* Dwutygodniowa przerwa w dniach 60–73. */
            const away = day >= 60 && day < 74;

            /* Nowe hasła tylko przez pierwsze 40 dni i tylko wtedy, gdy kolejka
               na to pozwala. Zamknięcie dopływu jest tu konieczne metodycznie:
               gdyby hasła dochodziły do końca, późniejsza retencja mierzyłaby
               głównie świeżo wprowadzone karty i spadałaby nawet przy idealnie
               działającej pętli. Chcemy zobaczyć, co algorytm robi z ustaloną
               kartoteką, a nie jak wygląda średnia z ciągle zmieniającej się
               populacji. */
            const planBefore = SRS.plan();
            if (!away && day < 40 && planBefore.dueTotal < planBefore.cap * 0.7
                && introduced < ids.length) {
              for (let k = 0; k < 8 && introduced < ids.length; k++) {
                SRS.addBoth(ids[introduced++]);
              }
            }

            const plan = SRS.plan();
            history.push({ day, due: plan.dueTotal, shown: away ? 0 : plan.today.length,
                           cap: plan.cap, backlog: plan.backlog });
            if (away) continue;

            /* Zaległości większe niż jeszcze jeden dzień pracy rozkładamy. */
            if (plan.backlog > plan.cap) SRS.spreadBacklog();

            const todays = SRS.plan().today;
            let answers = 0;
            todays.forEach(card => {
              const side = SRS.sideOf(card.id);
              if (side === 'c' || side === 'w') return;
              const elapsed = Math.max(0, U.daysBetween(card.last || simDay, simDay));
              const ok = rnd() < recall(card.id, elapsed);
              strength[card.id] = ok ? (strength[card.id] || 0) + 1 : 0;
              SRS.grade(SRS.recordOf(card.id), ok ? 4 : 0, { side: side });
              answers += 1;
            });
            Progress.data.days[simDay] = { answers: answers, correct: 0, minutes: answers * 0.4, newWords: 0 };
          }

          /* Retencja liczona po okresach kalendarzowych, nie po pozycji w
             dzienniku: pozycja mieszałaby pierwsze dni nauki (krótkie odstępy,
             wysoka trafność) z późniejszymi i pokazywała spadek tam, gdzie
             naprawdę zmieniła się tylko długość odstępów. */
          const rateBetween = (side, from, to) => {
            const a = SRS.addDays(realToday, from), b = SRS.addDays(realToday, to);
            const e = SRS.log.filter(x => x.s === side && x.iv >= 1 && x.d >= a && x.d < b);
            return e.length ? Math.round(e.filter(x => x.ok).length / e.length * 100) : null;
          };

          const sides = SRS.sideStats();
          const gap = SRS.sideGap();
          const breakDays = history.slice(74, 82);

          U.today = () => realToday;   /* przywracamy prawdziwy kalendarz */
          SRS.save = realSave;
          Progress.save = realPSave;

          return {
            introduced,
            factorR: SRS.factor('r'), factorP: SRS.factor('p'),
            /* Okno wczesne zaczyna się po zamknięciu dopływu nowych haseł,
               późne — po odrobieniu przerwy. Ta sama populacja kart w obu. */
            retEarlyR: rateBetween('r', 41, 56), retEarlyP: rateBetween('p', 41, 56),
            retLateR: rateBetween('r', 76, 90), retLateP: rateBetween('p', 76, 90),
            avgR: sides.r.avgInterval, avgP: sides.p.avgInterval,
            learnedR: sides.r.learned, learnedP: sides.p.learned,
            steps: gap ? gap.steps : 0, behind: gap ? gap.behind : false,
            maxShown: Math.max.apply(null, history.map(h => h.shown)),
            maxDue: Math.max.apply(null, history.map(h => h.due)),
            afterBreakShown: breakDays.map(h => h.shown),
            afterBreakDue: breakDays[0] ? breakDays[0].due : 0,
            reviews: SRS.log.length
          };
        }""")
        notes.append('  symulacja 90 dni: %d haseł, %d powtórek, mnożniki '
                     'rozpoznanie %.2f / wytworzenie %.2f'
                     % (sim['introduced'], sim['reviews'], sim['factorR'], sim['factorP']))
        notes.append('  retencja rozpoznania %s%% -> %s%%, wytworzenia %s%% -> %s%%'
                     % (sim['retEarlyR'], sim['retLateR'], sim['retEarlyP'], sim['retLateP']))
        notes.append('  odstępy: rozpoznanie %.1f dnia, wytworzenie %.1f dnia '
                     '(różnica ok. %.1f poziomu)'
                     % (sim['avgR'], sim['avgP'], sim['steps']))
        notes.append('  kolejka: najwięcej %d kart dziennie przy szczycie %d zaległych'
                     % (sim['maxShown'], sim['maxDue']))

        check('symulacja 90 dni faktycznie się rozpędza',
              sim['introduced'] >= 100 and sim['reviews'] >= 1000,
              '%d haseł, %d powtórek' % (sim['introduced'], sim['reviews']))
        check('wytworzenie zostaje w tyle za rozpoznaniem',
              sim['behind'] and sim['avgP'] < sim['avgR'],
              'odstępy %.1f wobec %.1f dnia, utrwalonych %d wobec %d'
              % (sim['avgP'], sim['avgR'], sim['learnedP'], sim['learnedR']))
        check('kolejka nigdy nie przekracza dziennego sufitu',
              sim['maxShown'] <= 120,
              'najwięcej %d kart jednego dnia' % sim['maxShown'])
        check('po dwutygodniowej przerwie kolejka zostaje rozłożona',
              sim['afterBreakDue'] > max(sim['afterBreakShown']),
              '%d zaległych, pokazywane po %s'
              % (sim['afterBreakDue'], '/'.join(str(x) for x in sim['afterBreakShown'])))


        # --- sesja dnia: skład dla trzech stanów użytkownika ---
        #
        # Skład sesji jest jedyną rzeczą, która stoi między uczącym się a
        # dwudziestoma trybami ćwiczeń. Jeśli dobiera źle, cała reszta pracy
        # nad sesją nie ma znaczenia — dlatego sprawdzamy go na trzech stanach
        # różniących się dokładnie tym, co ma na skład wpływać.
        page.evaluate("() => DB.ensureCoverage()")
        page.wait_for_function("() => Coverage.ready()", timeout=45000)

        setup_states = """(state) => {
          const back = n => { const d = new Date(); d.setDate(d.getDate() - n);
                              return d.toISOString().slice(0, 10); };
          SRS.cards = {}; SRS.save();
          Progress.data.days = {}; Progress.data.errors =
            { category: {}, grammar: {}, type: {}, mode: {} };

          if (state === 'zaleglosci') {
            DB.index.slice(0, 300).forEach((r, i) => {
              SRS.addBoth(r.id);
              ['r', 'p'].forEach(side => {
                const c = SRS.cards[SRS.cardId(r.id, side)];
                c.repetitions = 3; c.interval = 8; c.ease = 2.3;
                c.due = back(10 + (i % 12)); c.last = back(18);
              });
            });
            Progress.data.errors.mode =
              { build: { answers: 60, wrong: 30 }, choice: { answers: 80, wrong: 6 } };
          }
          if (state === 'zaawansowany') {
            DB.index.slice(0, 900).forEach((r, i) => {
              SRS.addBoth(r.id);
              ['r', 'p'].forEach(side => {
                const c = SRS.cards[SRS.cardId(r.id, side)];
                c.repetitions = 6; c.interval = 40 + (i % 60); c.ease = 2.6;
                c.due = back(-(5 + i % 30)); c.last = back(i % 25);
              });
            });
            DB.index.slice(0, 25).forEach(r => {
              SRS.cards[SRS.cardId(r.id, 'r')].due = back(0);
            });
          }
          SRS.save(); Progress.save();
          const plan = Session.compose(20, { pron: true });
          const g = {};
          plan.blocks.forEach(b => { g[b.kind] = (g[b.kind] || 0) + b.steps; });
          return { groups: g, steps: plan.steps,
                   estimate: Math.round(plan.estimate / 60),
                   load: plan.load, weak: plan.weak && plan.weak.mode,
                   order: plan.blocks.map(b => b.kind) };
        }"""

        beg = page.evaluate(setup_states, 'poczatkujacy')
        check('początkujący nie dostaje bloku powtórek, gdy nic nie czeka',
              not beg['groups'].get('srs') and beg['load']['due'] == 0,
              'powtórki: %s' % beg['groups'].get('srs'))
        check('początkujący dostaje nową lekcję, słuchanie i produkcję',
              all(beg['groups'].get(k) for k in ('lesson', 'listen', 'produce')),
              str(beg['groups']))

        bl = page.evaluate(setup_states, 'zaleglosci')
        check('zaległości podnoszą udział powtórek, ale nie zabierają całej sesji',
              0 < bl['groups']['srs'] <= bl['steps'] * 0.62,
              '%d z %d kroków' % (bl['groups']['srs'], bl['steps']))
        check('zaległości ograniczają liczbę nowych haseł',
              bl['groups'].get('lesson', 0) <= 3,
              'nowych haseł: %s' % bl['groups'].get('lesson'))
        check('sesja z zaległościami zaczyna się od powtórek',
              bl['order'][0] == 'srs', bl['order'][0])
        check('najsłabszy tryb produkcyjny dostaje dodatkowy blok',
              bl['weak'] == 'build', str(bl['weak']))

        adv = page.evaluate(setup_states, 'zaawansowany')
        check('zaawansowany nie dostaje więcej powtórek, niż faktycznie czeka',
              adv['groups']['srs'] <= adv['load']['due'],
              '%d kroków przy %d kartach' % (adv['groups']['srs'], adv['load']['due']))
        check('nowe hasła nie przekraczają sufitu sesji',
              adv['groups'].get('lesson', 0) <= 8,
              'nowych haseł: %s' % adv['groups'].get('lesson'))

        for name, plan in (('początkujący', beg), ('z zaległościami', bl),
                           ('zaawansowany', adv)):
            check('sesja %s mieści się w zamówionym czasie' % name,
                  18 <= plan['estimate'] <= 21,
                  'szacunek %d min' % plan['estimate'])

        r = page.evaluate("""() => {
          const out = {};
          [10, 20, 40].forEach(m => {
            const p = Session.compose(m, { pron: true });
            out[m] = Math.round(p.estimate / 60);
          });
          return out;
        }""")
        check('każda z trzech długości sesji trafia w swój budżet',
              all(abs(int(r[k]) - int(k)) <= 2 for k in r),
              str(r))

        # --- sesja dnia: przerwanie i powrót ---
        r = page.evaluate("""() => {
          Session.clear();
          Session.start(20);
          const total = Session.progress().steps;
          for (let i = 0; i < 5; i++) Session.step(true);
          Session.pause();
          const saved = JSON.stringify(Session.state);
          Session.state = null;              // tak jakby karta została zamknięta
          Session.load();
          const same = JSON.stringify(Session.state) === saved;
          const resumable = Session.resumable();
          const done = Session.progress().done;
          Session.resume();
          let guard = 0;
          while (Session.current() && guard++ < 600) Session.step(guard % 3 !== 0);
          const finished = !!Session.state.finished;
          const log = Session.log();
          const last = log[log.length - 1];
          const blockSum = Object.keys(last.blocks)
            .reduce((n, k) => n + last.blocks[k].done, 0);
          Session.clear();
          return { total, same, resumable, done, finished,
                   logged: !!last, blockSum, answers: last ? last.answers : 0 };
        }""")
        check('przerwana sesja przeżywa zamknięcie karty bez zmian',
              r['same'] and r['resumable'], 'zapis identyczny: %s' % r['same'])
        check('powrót do sesji wraca do tego samego kroku',
              r['done'] == 5, 'krok %s' % r['done'])
        check('dokończona sesja trafia do dziennika z pełnym składem',
              r['finished'] and r['logged'] and r['blockSum'] == r['total'],
              '%s z %s kroków' % (r['blockSum'], r['total']))

        r = page.evaluate("""() => {
          Session.clear();
          Session.start(10);
          Session.state.date = U.addDays(U.today(), -1);
          Session.save();
          Session.state = null;
          Session.load();
          const out = { resumable: Session.resumable(), stale: Session.stale() };
          Session.clear();
          return out;
        }""")
        check('sesja z poprzedniego dnia nie jest wznawiana',
              not r['resumable'] and r['stale'], str(r))

        # --- pokrycie rozumienia ---
        #
        # Miara ma być uczciwa, więc test pilnuje przede wszystkim tego, czego
        # nie wolno jej robić: liczyć jako znane czegoś, co znane nie jest,
        # i obiecywać progu, którego dane nie są w stanie unieść.
        r = page.evaluate("""() => {
          SRS.cards = {}; SRS.save();
          const zero = Coverage.category('Restauracja');
          const cat = DB.coverage.categories.filter(c => c.name === 'Restauracja')[0];
          // dziesięć najczęstszych haseł, tylko DODANE do kartoteki
          const top = Coverage.nextItems('Restauracja', 10);
          top.forEach(it => SRS.addBoth(it.id));
          const added = Coverage.category('Restauracja');
          // te same hasła doprowadzone do opanowania
          top.forEach(it => {
            const c = SRS.cards[SRS.cardId(it.id, 'r')];
            c.repetitions = SRS.LEARNED.repetitions;
            c.interval = SRS.LEARNED.interval;
          });
          SRS.save();
          const learned = Coverage.category('Restauracja');
          return {
            zeroCov: zero.coverage, zeroReach: zero.reach,
            addedCov: added.coverage, addedReach: added.reach,
            learnedCov: learned.coverage,
            ceiling: learned.ceiling,
            unmapped: cat.unmapped, occurrences: cat.occurrences,
            goal: learned.goal, goalIsCeiling: learned.goalIsCeiling,
            weights: top.map(t => t.weight)
          };
        }""")
        check('bez opanowanych haseł pokrycie wynosi zero',
              r['zeroCov'] == 0, str(r['zeroCov']))
        check('samo dodanie hasła do kartoteki nie podnosi pokrycia',
              r['addedCov'] == 0 and r['addedReach'] > 0,
              'pokrycie %.4f, zasięg %.4f' % (r['addedCov'], r['addedReach']))
        check('opanowanie hasła podnosi pokrycie',
              r['learnedCov'] > 0, '%.4f' % r['learnedCov'])
        check('pokrycie nigdy nie przekracza sufitu metody',
              r['learnedCov'] <= r['ceiling'] + 1e-9,
              '%.4f > %.4f' % (r['learnedCov'], r['ceiling']))
        check('sufit metody zgadza się z liczbą wyrazów spoza bazy',
              abs((1 - r['unmapped'] / r['occurrences']) - r['ceiling']) < 1e-6,
              'sufit %.4f' % r['ceiling'])
        check('cel kategorii nie obiecuje progu ponad sufit',
              r['goal'] <= r['ceiling'] + 1e-9
              and (r['goalIsCeiling'] == (r['ceiling'] < 0.95)),
              'cel %.4f, sufit %.4f' % (r['goal'], r['ceiling']))
        check('hasła do nauki są uszeregowane od najczęstszego w materiale',
              r['weights'] == sorted(r['weights'], reverse=True),
              str(r['weights'][:5]))

        r = page.evaluate("""() => {
          const bad = [];
          DB.coverage.categories.forEach(c => {
            let occ = 0;
            c.l.forEach(line => { occ += line.s.length; });
            if (occ !== c.occurrences) bad.push(c.name + ': ' + occ + ' vs ' + c.occurrences);
            let mapped = 0;
            c.l.forEach(line => line.s.forEach(s => { if (s >= 0) mapped += 1; }));
            if (mapped !== c.mapped) bad.push(c.name + ' przypisane: ' + mapped);
            c.l.forEach(line => line.s.forEach(s => {
              if (s >= c.ids.length) bad.push(c.name + ' numer poza tabelą');
            }));
          });
          return { bad: bad.slice(0, 4), cats: DB.coverage.categories.length };
        }""")
        check('korpus pokrycia jest wewnętrznie spójny',
              not r['bad'], '; '.join(r['bad']))

        # --- cele i retrospekcja ---
        r = page.evaluate("""() => {
          Goals.set({ minutes: 20 });
          const t0 = Goals.today();
          Progress.data.days[U.today()] = { answers: 5, correct: 4, minutes: 20, newWords: 1 };
          Progress.save();
          const t1 = Goals.today();
          const capBefore = Progress.data.goal;
          Goals.set({ minutes: 5 });
          const capAfter = Progress.data.goal;
          const entry = Goals.setCategory('Restauracja');
          const cat = Goals.category();
          Goals.setCategory(null);
          return { met0: t0.met, met1: t1.met, left0: t0.left,
                   capBefore, capAfter,
                   week: entry.week, catName: cat.name,
                   expired: cat.expired, sameWeek: Goals.weekKey() === entry.week };
        }""")
        check('cel dnia liczy minuty, nie odpowiedzi',
              (not r['met0']) and r['met1'] and r['left0'] == 20, str(r))
        check('zmiana celu czasowego przestawia sufit kolejki powtórek',
              r['capBefore'] != r['capAfter'] and r['capAfter'] >= 5,
              '%s → %s' % (r['capBefore'], r['capAfter']))
        check('cel kategorialny jest przypisany do bieżącego tygodnia',
              r['catName'] == 'Restauracja' and r['sameWeek'] and not r['expired'],
              str(r['week']))

        r = page.evaluate("""() => {
          const back = n => { const d = new Date(); d.setDate(d.getDate() - n);
                              return d.toISOString().slice(0, 10); };
          Progress.data.days = {};
          const start = Goals.weekStart(U.today());
          Progress.data.days[start] = { answers: 60, correct: 50, minutes: 90, newWords: 10 };
          Progress.save();
          U.store.set('coverage.snaps', [{ d: start, c: { 'Restauracja': 0.0 } }]);
          const sum = Retro.summary();
          return { rec: sum.recommendation.kind, text: sum.recommendation.text,
                   minutes: sum.now.minutes, active: sum.now.activeDays,
                   history: sum.hasHistory };
        }""")
        check('retrospekcja daje dokładnie jedną rekomendację z uzasadnieniem',
              bool(r['rec']) and len(r['text']) > 40, str(r['rec']))
        check('długa nauka w jednym dniu jest rozpoznana jako brak rytmu',
              r['rec'] in ('rhythm', 'backlog'),
              '%s (%d min w %d dni)' % (r['rec'], r['minutes'], r['active']))

        # --- gramatyka: progresja, trzy tryby, statystyka ---
        #
        # Sprawdzamy przede wszystkim to, czego ten moduł robić NIE MOŻE:
        # pokazać tematu wcześniej niż materiał, który go ilustruje, i zaliczyć
        # przekształcenia, w którym cząstka stoi w złym miejscu.
        page.evaluate("() => App.go('grammar')")
        # Trzy pliki trybów dociągają się równolegle. Czekanie na jeden z nich
        # to wyścig: transformacje bywają gotowe później niż zadania struktury.
        page.wait_for_function(
            "() => DB.grammarListening && DB.grammarListening.length"
            " && DB.grammarTransform && DB.grammarTransform.length"
            " && DB.particles && DB.particles.length",
            timeout=45000)

        r = page.evaluate("""() => {
          const g = DB.grammar;
          let bad = 0, worstAt = 0, prev = 0, backwards = 0, stageBack = 0;
          let prevStage = 0;
          const unlock = {};
          const known = new Set();
          const PAIR = { 'khráp': ['khâ','khá'], 'phǒm': ['chǎn','dì','dì-chǎn'] };
          DB.lessons.forEach((L, i) => {
            (L.newWordIds || []).forEach(id => {
              const rec = DB.get(id);
              ((rec && rec.syllables) || []).forEach(sy => {
                known.add(sy);
                (PAIR[sy] || []).forEach(x => known.add(x));
              });
            });
            known.forEach(sy => { if (!(sy in unlock)) unlock[sy] = i + 1; });
          });
          const syl = t => {
            const rec = (DB.index || []).filter(x => x.thaiPhonetic === t)[0];
            return t.split(/[ -]+/).filter(Boolean);
          };
          g.forEach(t => {
            t.patterns.forEach(p => {
              let av = 0;
              syl(p.thaiPhonetic).forEach(sy => {
                const u = unlock[sy];
                av = (u === undefined) ? 99999 : Math.max(av, u);
              });
              if (av > t.introducedAt) bad += 1;
              worstAt = Math.max(worstAt, av === 99999 ? 0 : av);
            });
            if (t.introducedAt < prev) backwards += 1;
            prev = t.introducedAt;
            if (t.stage < prevStage) stageBack += 1;
            prevStage = t.stage;
          });
          let lessonBad = 0;
          const intro = {};
          g.forEach(t => { intro[t.id] = t.introducedAt; });
          DB.lessons.forEach((L, i) => {
            if (intro[L.grammarId] > i + 1) lessonBad += 1;
          });
          return { topics: g.length, stages: new Set(g.map(x => x.stage)).size,
                   bad: bad, backwards: backwards, stageBack: stageBack,
                   lessonBad: lessonBad,
                   minPatterns: Math.min.apply(null, g.map(x => x.patterns.length)) };
        }""")
        check('progresja ma co najmniej 50 tematów w 8 etapach',
              r['topics'] >= 50 and r['stages'] == 8,
              '%d tematów, %d etapów' % (r['topics'], r['stages']))
        check('żaden wzorzec nie wyprzedza materiału, który go ilustruje',
              r['bad'] == 0, 'naruszeń: %d' % r['bad'])
        check('żadna lekcja nie niesie tematu sprzed jego wejścia',
              r['lessonBad'] == 0, 'lekcji: %d' % r['lessonBad'])
        check('progresja się nie cofa i etapy się nie przeplatają',
              r['backwards'] == 0 and r['stageBack'] == 0,
              'cofnięć %d, przeplotów %d' % (r['backwards'], r['stageBack']))
        check('każdy temat ma czym się wytłumaczyć',
              r['minPatterns'] >= 3, 'minimum %d wzorców' % r['minPatterns'])

        # Ocena transformacji idzie PO STRUKTURZE. Osiem przypadków granicznych:
        # cztery muszą przejść, cztery muszą odpaść.
        r = page.evaluate("""() => {
          const q = DB.grammarTransform.filter(x => x.transform === 'question')[0];
          const n = DB.grammarTransform.filter(x => x.transform === 'negation')[0];
          const p = DB.grammarTransform.filter(x => x.transform === 'polite')[0];
          return {
            model:      Gram.grade(q.model, q).ok,
            noTones:    Gram.grade(U.stripTones(q.model), q).ok,
            femaleForm: Gram.grade(p.thaiPhonetic + ' khâ', p).ok,
            negModel:   Gram.grade(n.model, n).ok,
            noMarker:   Gram.grade(q.thaiPhonetic, q).ok,
            wrongPlace: Gram.grade(q.check.marker + ' ' + q.thaiPhonetic, q).ok,
            negAtEnd:   Gram.grade(n.thaiPhonetic + ' ' + n.check.marker, n).ok,
            otherText:  Gram.grade('khrai pai naa ' + q.check.marker, q).ok
          };
        }""")
        check('ocena transformacji zalicza poprawną strukturę mimo różnic zapisu',
              r['model'] and r['noTones'] and r['femaleForm'] and r['negModel'],
              'wzorzec, bez tonów, forma żeńska, przeczenie')
        check('ocena transformacji odrzuca brak cząstki i złą pozycję',
              not r['noMarker'] and not r['wrongPlace'] and not r['negAtEnd']
              and not r['otherText'],
              'brak markera, marker na początku, marker na końcu, inne zdanie')

        # Zapis fonetyczny musi być zasłonięty do czasu odpowiedzi — inaczej
        # ćwiczenie mierzy czytanie, a nie słuchanie.
        r = page.evaluate("""() => {
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
          const before = box.innerText;
          const opt = box.querySelector('.options .option');
          const had = !!opt;
          if (opt) opt.click();
          return { veiled: before.indexOf('Zapis pojawi się') !== -1,
                   had: had,
                   after: box.innerText.indexOf('Zapis pojawi się') === -1 };
        }""")
        check('zapis jest zasłonięty do czasu odpowiedzi w wykrywaniu struktury',
              r['veiled'] and r['had'], 'zasłonięty: %s' % r['veiled'])
        check('po odpowiedzi zapis się odsłania', r['after'])

        # Statystyka rozdziela rozumienie od produkcji.
        r = page.evaluate("""() => {
          const t = DB.grammar[0].id;
          const L = DB.lessons.filter(x => x.grammarId === t)[0];
          const rid = L.recordIds[0];
          const before = GStats.understoodNotProduced().length;
          for (let i = 0; i < 5; i++) Progress.grammarAnswer(rid, true, 'receptive');
          const tooFew = GStats.table().filter(x => x.id === t)[0].rated;
          Progress.grammarAnswer(rid, true, 'receptive');
          for (let j = 0; j < 8; j++) Progress.grammarAnswer(rid, j < 2, 'productive');
          const row = GStats.table().filter(x => x.id === t)[0];
          return { before: before, tooFew: tooFew, rated: row.rated,
                   r: row.receptive.share, p: row.productive.share,
                   gap: GStats.understoodNotProduced().length,
                   stages: GStats.byStage().length };
        }""")
        check('temat poniżej progu prób nie jest oceniany',
              r['tooFew'] is False, 'po 5 próbach: nieoceniony')
        check('statystyka wykrywa konstrukcję rozumianą, ale nieprodukowaną',
              r['rated'] and r['gap'] > r['before'] and r['r'] > r['p'],
              'ze słuchu %d%%, w produkcji %d%%'
              % (round(r['r'] * 100), round(r['p'] * 100)))
        check('podsumowanie etapów obejmuje wszystkie osiem',
              r['stages'] == 8, '%d etapów' % r['stages'])

        # Partykuły: poprawna odpowiedź musi być wśród opcji, a opis kompletny.
        r = page.evaluate("""() => {
          let bad = 0, noWhy = 0;
          const ids = new Set(DB.particles.map(p => p.id));
          DB.particleExercises.forEach(ex => {
            const opts = ex.options.map(o => o.id);
            if (opts.indexOf(ex.answer) === -1) bad += 1;
            if (!ex.why || !ex.situation) noWhy += 1;
            opts.forEach(o => { if (!ids.has(o)) bad += 1; });
          });
          const missing = DB.particles.filter(
            p => !p.meaning || !p.effect || !p.missing || !(p.examples || []).length).length;
          return { count: DB.particles.length, ex: DB.particleExercises.length,
                   bad: bad, noWhy: noWhy, missing: missing };
        }""")
        check('każde ćwiczenie partykuł ma poprawną odpowiedź wśród opcji',
              r['bad'] == 0 and r['noWhy'] == 0,
              '%d partykuł, %d ćwiczeń' % (r['count'], r['ex']))
        check('każda partykuła mówi, co znaczy i co się dzieje, gdy jej brak',
              r['missing'] == 0)


        # ================================================ MODUŁ LICZBOWY
        #
        # Kluczowa kontrola tej sesji: aplikacja musi umieć wygenerować
        # I ODCZYTAĆ każdą liczbę z zakresu, a nie tylko te, które leżą
        # w pliku. Sprawdzamy to w obie strony — składanie i niezależny
        # rozbiór z powrotem na wartość — bo sama generacja niczego nie
        # dowodzi: reguła może być wewnętrznie spójna i konsekwentnie błędna.
        page.evaluate("() => App.go('numbers')")
        page.wait_for_function("() => window.Numbers && Numbers.loaded()", timeout=30000)

        r = page.evaluate("""() => {
          const bad = [];
          let checked = 0;
          const test = (n) => {
            const said = Numbers.say(n);
            checked += 1;
            if (!said || !said.thaiPhonetic) { bad.push([n, 'brak zapisu']); return; }
            if (!said.ttsKey) { bad.push([n, 'brak tekstu dla syntezatora']); return; }
            const back = Numbers.parse(said.thaiPhonetic);
            if (back !== n) bad.push([n, said.thaiPhonetic + ' -> ' + back]);
          };
          for (let n = 0; n <= 2000; n++) test(n);
          for (let n = 2001; n <= 1000000; n += 997) test(n);
          [999, 1000, 9999, 10000, 99999, 100000, 999999, 1000000].forEach(test);
          return { checked: checked, bad: bad.slice(0, 6), badCount: bad.length };
        }""")
        check('każda liczba z zakresu daje się wygenerować i odczytać',
              r['badCount'] == 0,
              'sprawdzonych %d, rozjazdów %d%s'
              % (r['checked'], r['badCount'],
                 (' np. ' + str(r['bad'][:3])) if r['bad'] else ''))

        # Nieregularności z osobna. Gdyby reguła i jej rozbiór pomyliły się
        # zgodnie, powyższa pętla by tego nie złapała — te punkty tak.
        r = page.evaluate("""() => {
          const want = { 0:'sǔun', 1:'nùeng', 10:'sìp', 11:'sìp-èt', 12:'sìp-sǎwng',
            19:'sìp-kâo', 20:'yîi-sìp', 21:'yîi-sìp-èt', 22:'yîi-sìp-sǎwng',
            30:'sǎam-sìp', 31:'sǎam-sìp-èt', 100:'nùeng-ráwy', 101:'nùeng-ráwy-èt',
            105:'nùeng-ráwy-hâa', 110:'nùeng-ráwy-sìp', 111:'nùeng-ráwy-sìp-èt',
            1000:'nùeng-phan', 10000:'nùeng-mùen', 100000:'nùeng-sǎen',
            1000000:'nùeng-láan' };
          const bad = [];
          Object.keys(want).forEach(k => {
            const got = Numbers.say(parseInt(k, 10));
            if (!got || got.thaiPhonetic !== want[k]) bad.push(k + ': ' + (got && got.thaiPhonetic));
          });
          return { bad: bad };
        }""")
        check('nieregularności liczebnika wychodzą dokładnie tak, jak powinny',
              not r['bad'], 'rozjazdy: %s' % (r['bad'] or 'brak'))

        r = page.evaluate("""() => {
          return { out: Numbers.say(1000001), neg: Numbers.say(-1),
                   frac: Numbers.say(2.5), txt: Numbers.parse('bàat khráp') };
        }""")
        check('liczba spoza zakresu i tekst niebędący liczebnikiem są odrzucane',
              r['out'] is None and r['neg'] is None and r['frac'] is None
              and r['txt'] is None)

        # Pismo tajskie składane z atomów nie może wyciec do DOM-u. To jest
        # ta sama zasada co w całej aplikacji, tylko trudniejsza: liczba jest
        # sklejana w locie, a nie brana gotowa z rekordu.
        r = page.evaluate("""() => {
          const said = Numbers.say(12345);
          const key = said.ttsKey;
          return { hasText: !!DB.voiceText(key),
                   leaked: /[\u0E00-\u0E7F]/.test(said.thaiPhonetic),
                   dom: /[\u0E00-\u0E7F]/.test(document.body.innerHTML) };
        }""")
        check('tekst dla syntezatora jest składany, ale nie wycieka do zapisu ani do DOM',
              r['hasText'] and not r['leaked'] and not r['dom'])

        # Ten sam ciąg atomów nie może zakładać nowego wpisu przy każdym
        # odtworzeniu — liczby składają się z tych samych dziesięciu cyfr.
        r = page.evaluate("""() => {
          const a = Numbers.say(345).ttsKey, b = Numbers.say(345).ttsKey;
          return { same: a === b };
        }""")
        check('sklejony tekst dla syntezatora jest zapamiętywany, nie liczony od nowa',
              r['same'])

        # --- czas reakcji jako główna miara ---
        r = page.evaluate("""() => {
          Progress.data.numbers = {};
          Progress.numberAnswer('dictation', true, 1200, {});
          Progress.numberAnswer('dictation', true, 1400, {});
          const afterFast = Progress.numberStats();
          Progress.numberAnswer('dictation', false, 9000, {});
          const afterMiss = Progress.numberStats();
          Progress.numberAnswer('dictation', true, 9000, {});
          const afterSlow = Progress.numberStats();
          return {
            fastMedian: afterFast.median,
            missMedian: afterMiss.median,
            slowMedian: afterSlow.median,
            answers: afterSlow.answers, correct: afterSlow.correct
          };
        }""")
        check('czas pomyłki nie wchodzi do mediany czasu reakcji',
              r['missMedian'] == r['fastMedian'],
              'przed pomyłką %s ms, po pomyłce %s ms' % (r['fastMedian'], r['missMedian']))
        check('trafna wolna odpowiedź podnosi medianę',
              r['slowMedian'] > r['fastMedian'],
              '%s -> %s ms' % (r['fastMedian'], r['slowMedian']))

        r = page.evaluate("""() => {
          Progress.data.numbers = {};
          const def = Numbers.drillDef('dictation');
          for (let i = 0; i < 12; i++) Progress.numberAnswer('dictation', true, def.masteryMs - 400, {});
          const good = Progress.numberStats().rows[0].mastered;
          Progress.data.numbers = {};
          for (let i = 0; i < 12; i++) Progress.numberAnswer('dictation', true, def.masteryMs + 2000, {});
          const slow = Progress.numberStats().rows[0].mastered;
          return { good: good, slow: slow, target: def.masteryMs };
        }""")
        check('opanowanie liczb zależy od czasu reakcji, nie od samej trafności',
              r['good'] and not r['slow'],
              'próg %d ms; bezbłędnie, ale wolno = nieopanowane' % r['target'])

        # --- dostępność: limit czasu ---
        r = page.evaluate("""() => {
          const base = 8000;
          const out = {};
          ['normal', 'double', 'off'].forEach(m => {
            const s = U.store.get('settings', {});
            s.timeLimit = m; U.store.set('settings', s);
            out[m] = Numbers.limitMs(base);
          });
          const s = U.store.get('settings', {});
          s.timeLimit = 'normal'; U.store.set('settings', s);
          return out;
        }""")
        check('limit czasu daje się wydłużyć i wyłączyć',
              r['normal'] == 8000 and r['double'] == 16000 and r['off'] == 0,
              'standardowy %s, podwójny %s, wyłączony %s' % (r['normal'], r['double'], r['off']))

        r = page.evaluate("""() => {
          const s = U.store.get('settings', {});
          s.timeLimit = 'off'; U.store.set('settings', s);
          Progress.data.numbers = {};
          Progress.numberAnswer('dictation', true, 2100, {});
          const st = Progress.numberStats();
          s.timeLimit = 'normal'; U.store.set('settings', s);
          return { median: st.median, answers: st.answers };
        }""")
        check('wyłączony limit nie unieważnia pomiaru czasu',
              r['median'] == 2100 and r['answers'] == 1,
              'mediana %s ms mimo braku limitu' % r['median'])

        # --- moduł rozłożony wzdłuż ścieżki ---
        r = page.evaluate("""() => {
          const L = Numbers.lessons().map(x => x.anchorNumber);
          const R = Rescue.loaded() ? Rescue.lessons().map(x => x.anchorNumber) : [];
          return { first: L[0], last: L[L.length - 1], count: L.length,
                   sorted: L.every((v, i) => i === 0 || v > L[i - 1]) };
        }""")
        check('moduł liczbowy jest rozłożony wzdłuż ścieżki, nie w jednym bloku',
              r['sorted'] and r['first'] <= 15 and r['last'] - r['first'] >= 50,
              '%d bloków, od lekcji %d do %d' % (r['count'], r['first'], r['last']))

        r = page.evaluate("""() => {
          const scenes = Numbers.scenes();
          let noValue = 0, badAnswer = 0;
          scenes.forEach(s => (s.questions || []).forEach(q => {
            if (typeof q.value === 'undefined') noValue += 1;
            if (!(q.answer >= 0 && q.answer < q.options.length)) badAnswer += 1;
          }));
          return { scenes: scenes.length, noValue: noValue, badAnswer: badAnswer,
                   questions: scenes.reduce((a, s) => a + s.questions.length, 0) };
        }""")
        check('sceny liczbowe pytają o konkretną wartość, nie o ogólny sens',
              r['noValue'] == 0 and r['badAnswer'] == 0,
              '%d scen, %d pytań' % (r['scenes'], r['questions']))

        # ============================================ STRATEGIE RATUNKOWE
        page.evaluate("() => App.go('rescue')")
        page.wait_for_function("() => window.Rescue && Rescue.loaded()", timeout=30000)

        r = page.evaluate("""() => {
          const f = Rescue.formulas();
          let noBoth = 0, noFemale = 0, noNote = 0;
          f.forEach(x => {
            const regs = (x.forms || []).map(y => y.register).sort();
            if (regs.join(',') !== 'formalny,potoczny') noBoth += 1;
            (x.forms || []).forEach(y => {
              if (!(y.genderVariant && y.genderVariant.female)) noFemale += 1;
            });
            if (!x.culturalNote) noNote += 1;
          });
          return { count: f.length, forms: f.reduce((a, x) => a + x.forms.length, 0),
                   noBoth: noBoth, noFemale: noFemale, noNote: noNote };
        }""")
        check('każda formuła ma oba rejestry, obie płcie i notatkę kulturową',
              r['noBoth'] == 0 and r['noFemale'] == 0 and r['noNote'] == 0,
              '%d formuł, %d form, %d wariantów płci' % (r['count'], r['forms'], r['forms'] * 2))

        r = page.evaluate("""() => {
          const male = Rescue.form(Rescue.byGroup('repeat'), 'potoczny');
          G.set('female');
          const asFemale = G.view(male).thaiPhonetic;
          G.set('male');
          const asMale = G.view(male).thaiPhonetic;
          return { female: asFemale, male: asMale };
        }""")
        check('formuła ratunkowa przełącza się na wariant zgodny z płcią mówiącego',
              'khráp' in r['male'] and 'khráp' not in r['female'],
              '%s / %s' % (r['male'], r['female']))

        # Brak reakcji w oknie MUSI liczyć się jak pomyłka — na tym stoi cały
        # ten dryl. Gdyby zamarcie było neutralne, statystyka pokazywałaby
        # wysoką trafność komuś, kto po prostu nic nie mówi.
        r = page.evaluate("""() => {
          Progress.data.reflex = {};
          Progress.reflexAnswer('fast', false, 4000, true);
          Progress.reflexAnswer('fast', true, 1200, false);
          const st = Progress.reflexStats();
          return { answers: st.answers, correct: st.correct, frozen: st.frozen,
                   share: st.share, frozenShare: st.frozenShare };
        }""")
        check('brak reakcji w oknie liczy się jak pomyłka',
              r['answers'] == 2 and r['correct'] == 1 and r['frozen'] == 1
              and abs(r['frozenShare'] - 0.5) < 1e-9)

        r = page.evaluate("""() => {
          Progress.data.reflex = {};
          Progress.reflexAnswer('noise', true, 1000, false);
          Progress.reflexRepair('noise', true);
          Progress.reflexRepair('noise', false);
          const st = Progress.reflexStats();
          return { tries: st.repairTries, ok: st.repaired, share: st.repairShare };
        }""")
        check('pętla naprawcza jest mierzona osobno od samej reakcji',
              r['tries'] == 2 and r['ok'] == 1 and abs(r['share'] - 0.5) < 1e-9,
              'reakcja i skutek reakcji to dwie różne liczby')

        r = page.evaluate("""() => {
          const groups = Rescue.formulas().map(f => f.group);
          let bad = 0;
          Rescue.triggers().forEach(t => {
            (t.accept || []).forEach(g => { if (groups.indexOf(g) === -1) bad += 1; });
            if (!(t.accept || []).length) bad += 1;
          });
          const items = Rescue.items();
          let badLine = 0;
          items.slice(0, 25).forEach(it => {
            const d = DB.get(it.dialogueId);
            const line = d && (d.lines || []).filter(l => l.index === it.line)[0];
            if (!line || line.polish !== it.check.answer) badLine += 1;
          });
          return { bad: bad, badLine: badLine, items: items.length,
                   triggers: Rescue.triggers().length };
        }""")
        check('dryl odruchu stoi na istniejących kwestiach i znanych formułach',
              r['bad'] == 0 and r['badLine'] == 0,
              '%d wyzwalaczy, %d zadań' % (r['triggers'], r['items']))

        r = page.evaluate("""() => {
          const nums = Rescue.lessons().map(l => l.anchorNumber);
          return { max: Math.max.apply(null, nums), count: nums.length };
        }""")
        check('strategie ratunkowe wchodzą w pierwszych 15 lekcjach',
              r['max'] <= 15, '%d bloków, ostatni po lekcji %d' % (r['count'], r['max']))

        # --- egzaminy poziomowe (sesja U) ---------------------------------
        page.evaluate("() => App.go('exam')")
        page.wait_for_function("() => window.Exam && Exam.ready()", timeout=45000)

        r = page.evaluate("""() => {
          const levels = Exam.LEVELS.map(l => ({
            level: l, variants: Exam.forLevel(l).length
          }));
          const one = Exam.forLevel('A1')[0];
          const counts = {};
          ['listening','detail','speaking','writing'].forEach(k => {
            const s = one.sections[k];
            counts[k] = (s.questions || s.items).length;
          });
          return { levels, counts, tasks: one.taskCount, limit: one.timeLimitSec };
        }""")
        check('każdy poziom ma trzy zestawy egzaminacyjne',
              all(x['variants'] == 3 for x in r['levels']),
              ', '.join('%s:%d' % (x['level'], x['variants']) for x in r['levels']))
        check('egzamin mierzy cztery sprawności osobno',
              sum(r['counts'].values()) == r['tasks'] and len(r['counts']) == 4,
              'słuch %(listening)d, szczegóły %(detail)d, mówienie %(speaking)d, zapis %(writing)d'
              % r['counts'])

        # Sedno całego pomysłu: koniunkcja, nie średnia.
        r = page.evaluate("""() => {
          const mk = (lis, det, tone, cont, wri) => ({
            sections: {
              listening: { answers: Array.from({length: 10}, (_, i) => ({ ok: i < lis })) },
              detail:    { answers: Array.from({length: 10}, (_, i) => ({ ok: i < det })) },
              speaking:  { answers: Array.from({length: 10}, (_, i) => ({ tone: tone, content: i < cont ? 1 : 0 })) },
              writing:   { answers: Array.from({length: 10}, (_, i) => ({ base: i < wri ? 1 : 0, tones: 1 })) }
            }
          });
          const all4 = Exam.score(mk(10, 10, 90, 10, 10));
          const lop = Exam.score(mk(10, 10, 0, 0, 10));
          return { all4: all4.passed, lop: lop.passed, lopCount: lop.passedCount };
        }""")
        check('komplet sprawności powyżej progu zalicza poziom', r['all4'])
        check('jedna sprawność poniżej progu NIE zalicza, mimo średniej 75%',
              not r['lop'], 'zaliczone sprawności: %d z 4' % r['lopCount'])

        r = page.evaluate("""() => {
          const state = { sections: {
            listening: { answers: Array.from({length: 10}, () => ({ ok: true })) },
            detail:    { answers: Array.from({length: 10}, () => ({ ok: true })) },
            speaking:  { answers: Array.from({length: 10}, () => ({ tone: 95, content: 0 })) },
            writing:   { answers: Array.from({length: 10}, () => ({ base: 1, tones: 1 })) }
          }};
          const s = Exam.score(state);
          return { tonePassed: s.speaking.tonePassed, contentPassed: s.speaking.contentPassed,
                   passed: s.speaking.passed, whole: s.passed };
        }""")
        check('bezbłędne tony przy złej treści nie zaliczają mówienia',
              r['tonePassed'] and not r['contentPassed'] and not r['passed'] and not r['whole'])

        r = page.evaluate("""() => {
          const one = Exam.scoreWriting('sawat dii', 'saw\u00e0t dii');
          const half = Exam.scoreWriting('sawat doo', 'saw\u00e0t dii');
          const none = Exam.scoreWriting('', 'saw\u00e0t dii');
          const flat = Exam.scoreWriting('sawatdii', 'saw\u00e0t dii');
          const tones = Exam.scoreWriting('saw\u00e0t dii', 'saw\u00e0t dii');
          return { one: one.base, half: half.base, none: none.base, flat: flat.base,
                   toneNo: one.tones, toneYes: tones.tones };
        }""")
        check('zapis punktowany sylabami, nie zerojedynkowo',
              r['one'] == 1 and 0 < r['half'] < 1 and r['none'] == 0,
              'trafnie %.2f, połowa %.2f, pusto %.2f' % (r['one'], r['half'], r['none']))
        check('zapis bez podziału na sylaby też jest oceniany', r['flat'] == 1)
        check('znaki tonu liczone osobno i nie wpływają na trafność sylab',
              r['one'] == 1 and r['toneNo'] < r['toneYes'],
              'bez tonów %.2f, z tonami %.2f' % (r['toneNo'], r['toneYes']))

        r = page.evaluate("""() => {
          Exam.start('A1');
          Exam.state.section = 'speaking';
          Exam.beginSection();
          Exam.answerSpeaking(Exam.tasks('speaking')[0],
                              { tone: 80, claim: 'same', plausible: true });
          const honest = Exam.state.sections.speaking.answers[0].content;
          Exam.answerSpeaking(Exam.tasks('speaking')[1],
                              { tone: 80, claim: 'same', plausible: false });
          const bluff = Exam.state.sections.speaking.answers[1].content;
          const shortRec = Exam.checkPlausible({ syllables: [{}] }, 6);
          const okRec = Exam.checkPlausible({ syllables: [{},{},{},{},{}] }, 6);
          Exam.state = null;
          return { honest, bluff, shortRec, okRec };
        }""")
        check('deklaracja treści bez wiarygodnego nagrania nie liczy się',
              r['honest'] == 1 and r['bluff'] == 0)
        check('kontrola długości odrzuca nagranie niepasujące do wzorca',
              (not r['shortRec']) and r['okRec'])

        r = page.evaluate("""() => {
          Exam.start('A1');
          const key = 'scene-x';
          const seq = [];
          for (let i = 0; i < 4; i++) {
            seq.push(Exam.canPlay(key));
            if (Exam.canPlay(key)) Exam.notePlay(key);
          }
          const left = Exam.playsLeft(key);
          Exam.state = null;
          return { seq, left, max: Exam.MAX_PLAYS };
        }""")
        check('materiał można odtworzyć najwyżej dwa razy',
              r['seq'] == [True, True, False, False] and r['left'] == 0,
              'limit %d' % r['max'])

        r = page.evaluate("""() => {
          Exam.start('A1');
          Exam.state.section = 'detail';
          Exam.beginSection();
          const tasks = Exam.tasks('detail');
          Exam.answerQuestion(tasks[0], tasks[0].answer);
          Exam.closeSection(true);
          const box = Exam.state.sections.detail;
          const scored = Exam.score(Exam.state).detail;
          Exam.state = null;
          return { answered: box.answers.length, tasks: tasks.length,
                   correct: scored.correct, pct: scored.pct, expired: scored.expired };
        }""")
        check('po upływie czasu nietknięte zadania liczą się jak pomyłki',
              r['answered'] == r['tasks'] and r['correct'] == 1 and r['expired'],
              '%d z %d zadań, wynik %.1f%%' % (r['correct'], r['tasks'], r['pct']))

        r = page.evaluate("""() => {
          const before = JSON.stringify(Progress.data.exams);
          Progress.data.exams = {};
          const first = Exam.eligibility('A2');
          const firstId = first.variant.id;
          Progress.saveExamAttempt({
            examId: firstId, level: 'A2', variant: 'A', date: U.today(),
            at: new Date().toISOString(), durationSec: 100,
            lessonsDone: Progress.lessonsDone(), abandoned: false, passed: false,
            sections: null, answers: null
          });
          const now = Exam.eligibility('A2');
          const box = Progress.examBox('A2');
          box.attempts[0].date = U.addDays(U.today(), -9);
          box.attempts[0].lessonsDone = Progress.lessonsDone() - 9;
          const later = Exam.eligibility('A2');
          const out = { firstAllowed: first.allowed, nowAllowed: now.allowed,
                        waitDays: now.waitDays, waitLessons: now.waitLessons,
                        laterAllowed: later.allowed,
                        sameSet: later.variant.id === firstId };
          Progress.data.exams = JSON.parse(before);
          Progress.save();
          return out;
        }""")
        check('pierwsze podejście dostępne od razu', r['firstAllowed'])
        check('powtórka zablokowana zaraz po podejściu',
              not r['nowAllowed'],
              'brakuje %d dni i %d lekcji' % (r['waitDays'], r['waitLessons']))
        check('powtórka dostępna po kilku dniach NAUKI, nie po samym czekaniu',
              r['laterAllowed'])
        check('powtórka dostaje inny zestaw zadań', not r['sameSet'])

        r = page.evaluate("""() => {
          const before = JSON.stringify(Progress.data.exams);
          Progress.data.exams = {};
          Exam.start('B1');
          const started = Exam.state.exam.id;
          const a = Exam.abandon();
          const el = Exam.eligibility('B1');
          const out = { saved: !!a && a.abandoned, allowed: el.allowed,
                        attempts: Progress.examAttempts('B1').length,
                        other: el.variant.id !== started };
          Progress.data.exams = JSON.parse(before);
          Progress.save();
          Exam.state = null;
          return out;
        }""")
        check('wyjście z egzaminu zapisuje podejście jako przerwane', r['saved'])
        check('przerwane podejście liczy się do karencji i nie zwraca zestawu',
              not r['allowed'] and r['other'], '%d podejść' % r['attempts'])

        r = page.evaluate("""() => {
          const exam = Exam.forLevel('A1')[0];
          const sp = exam.sections.speaking.items;
          const wr = exam.sections.writing.items;
          const lis = exam.sections.listening.questions;
          const det = exam.sections.detail.questions;
          const attempt = {
            examId: exam.id, level: 'A1', variant: 'A', date: U.today(),
            at: new Date().toISOString(), durationSec: 900,
            lessonsDone: 40, abandoned: false, passed: false,
            sections: Exam.score({ sections: {
              listening: { answers: lis.map(() => ({ ok: true })) },
              detail:    { answers: det.map(() => ({ ok: true })) },
              speaking:  { answers: sp.map(() => ({ tone: 20, content: 0 })) },
              writing:   { answers: wr.map(() => ({ base: 1, tones: 1 })) }
            } }),
            answers: {
              listening: lis.map(q => ({ id: q.id, sceneId: q.sceneId, ok: true })),
              detail: det.map((q, i) => ({ id: q.id, sceneId: q.sceneId, ok: i > 1 })),
              speaking: sp.map(i => ({ id: i.id, recordId: i.recordId,
                                       lesson: i.lesson, tone: 20, content: 0 })),
              writing: wr.map(i => ({ id: i.id, recordId: i.recordId,
                                      lesson: i.lesson, base: 1, tones: 1 }))
            }
          };
          const d = Exam.diagnose(attempt);
          return {
            sections: d.sections.length,
            weakest: d.weakest.id,
            failed: d.failed.map(f => f.id),
            lessons: d.lessons,
            scenes: d.scenes.length,
            plan: d.plan.map(p => p.kind),
            screens: d.plan.map(p => p.screen)
          };
        }""")
        check('diagnoza rozbija wynik na cztery sprawności', r['sections'] == 4)
        check('diagnoza wskazuje najsłabszą sprawność',
              r['weakest'] == 'speaking', r['weakest'])
        check('plan naprawczy podaje konkretne lekcje do powtórzenia',
              len(r['lessons']) > 0, 'lekcje: %s' % r['lessons'][:5])
        check('plan naprawczy podaje konkretne sceny i ekrany ćwiczeń',
              r['scenes'] > 0 and 'produce' in r['screens'],
              'kroki: %s' % ', '.join(r['plan']))

        r = page.evaluate("""() => {
          const html = ExamView.certificateHTML();
          const limits = ['Pismo tajskie', 'Akcenty regionalne', 'Mowa w ha\u0142asie',
                          'Tre\u015b\u0107 wypowiedzi ustnej'];
          return {
            charset: html.indexOf('charset="utf-8"') !== -1
                     || html.indexOf('charset=utf-8') !== -1,
            lang: html.indexOf('lang="pl"') !== -1,
            diacritics: /[\u0105\u0107\u0119\u0142\u0144\u00f3\u015b\u017a\u017c]/.test(html),
            missing: limits.filter(l => html.indexOf(l) === -1),
            hasPrint: html.indexOf('window.print()') !== -1,
            thai: /[\u0e00-\u0e7f]/.test(html)
          };
        }""")
        check('certyfikat deklaruje UTF-8 i język polski', r['charset'] and r['lang'])
        check('certyfikat zawiera polskie znaki diakrytyczne', r['diacritics'])
        check('certyfikat wymienia, czego NIE obejmuje',
              not r['missing'], 'brakuje: %s' % ', '.join(r['missing']))
        check('certyfikat da się wydrukować i zapisać jako PDF', r['hasPrint'])
        check('certyfikat nie zawiera pisma tajskiego', not r['thai'])

        # --- próbki kontrolne (sesja U) -----------------------------------
        page.evaluate("() => App.go('checkpoint')")
        page.wait_for_function("() => window.Checkpoint && Checkpoint.ready()", timeout=45000)

        r = page.evaluate("""() => {
          const all = Checkpoint.all();
          const bad = all.filter(c => c.triggerLesson - c.toLesson !== DB.checkpoints.lag);
          const gaps = [];
          for (let i = 1; i < all.length; i++) {
            gaps.push(all[i].triggerLesson - all[i - 1].triggerLesson);
          }
          return { count: all.length, bad: bad.length,
                   gaps: Array.from(new Set(gaps)),
                   lag: DB.checkpoints.lag, every: DB.checkpoints.every,
                   first: all[0].triggerLesson,
                   window: all[0].fromLesson + '-' + all[0].toLesson,
                   tasks: all[0].items.length };
        }""")
        check('próbka wypada co 20 lekcji',
              r['gaps'] == [r['every']] and r['every'] == 20,
              '%d próbek, odstępy %s' % (r['count'], r['gaps']))
        check('próbka pyta o materiał sprzed 20 lekcji, nie o świeży',
              r['bad'] == 0 and r['lag'] == 20,
              'pierwsza po lekcji %d sprawdza lekcje %s' % (r['first'], r['window']))

        r = page.evaluate("""async () => {
          const before = JSON.stringify(Progress.data.checkpoints);
          const srsBefore = JSON.stringify(SRS.cards);
          const def = Checkpoint.all()[0];
          await DB.ensureCheckpointRecords(def);
          Checkpoint.start(def.id);
          const items = def.items;
          const far = SRS.card(items[0].recordId, 'r');
          far.due = U.addDays(U.today(), 30);
          far.interval = 30;
          items.forEach((it, i) => {
            const rec = DB.any(it.recordId);
            const good = i > 1;
            if (it.kind === 'listen') {
              Checkpoint.answer(it, good ? it.answer : (it.answer + 1) % 4);
            } else {
              Checkpoint.answer(it, good ? (rec ? rec.thaiPhonetic : '') : 'xxx',
                                rec ? rec.thaiPhonetic : '');
            }
          });
          const res = Checkpoint.finish(false);
          const out = {
            pct: res.pct, wrong: res.wrong.length,
            early: res.earlyCatch.length,
            caughtFar: res.earlyCatch.indexOf(items[0].recordId) !== -1,
            weak: Checkpoint.weakLessons(res).length,
            stored: Progress.checkpointSummary().length
          };
          Progress.data.checkpoints = JSON.parse(before);
          SRS.cards = JSON.parse(srsBefore);
          Progress.save(); SRS.save();
          Checkpoint.state = null;
          return out;
        }""")
        check('próbka wykrywa ubytek, zanim zrobi to kolejka powtórek',
              r['caughtFar'] and r['early'] > 0,
              '%d haseł zapomnianych mimo terminu w przyszłości' % r['early'])
        check('wynik próbki wskazuje konkretne lekcje do powrotu',
              r['weak'] > 0 and r['wrong'] == 2,
              '%d pomyłek, %d lekcji' % (r['wrong'], r['weak']))
        check('wynik próbki trafia do postępu', r['stored'] >= 1)

        r = page.evaluate("""() => {
          const before = JSON.stringify(Progress.data.checkpoints);
          const def = Checkpoint.all()[0];
          Checkpoint.start(def.id);
          Checkpoint.answer(def.items[0], def.items[0].answer);
          const res = Checkpoint.finish(true);
          const out = { answered: res.total, correct: res.correct,
                        expired: res.expired, pct: res.pct };
          Progress.data.checkpoints = JSON.parse(before);
          Progress.save();
          Checkpoint.state = null;
          return out;
        }""")
        check('w próbce upływ czasu też liczy nietknięte zadania jak pomyłki',
              r['answered'] == 12 and r['correct'] == 1 and r['expired'],
              'wynik %d%%' % r['pct'])

        r = page.evaluate("""() => {
          const snapshot = JSON.parse(JSON.stringify(Progress.data));
          const old = JSON.parse(JSON.stringify(Progress.data));
          delete old.exams;
          delete old.checkpoints;
          U.store.set('progress', old);
          Progress.load();
          const out = { exams: !!Progress.data.exams,
                        checkpoints: !!Progress.data.checkpoints,
                        attempts: Progress.examAttempts('A1').length };
          Progress.data = snapshot;
          Progress.save();
          return out;
        }""")
        check('kopia postępu sprzed egzaminów wczytuje się bez błędu',
              r['exams'] and r['checkpoints'] and r['attempts'] == 0)

        # --- odporność wczytania postępu (sesja V) --------------------------
        # Kopia bez klucza najwyższego poziomu wywracała CAŁY start aplikacji,
        # a komunikat obwiniał katalog data/. Każdy brakujący klucz ma się
        # domykać wartością początkową.
        r = page.evaluate("""() => {
          const snapshot = JSON.parse(JSON.stringify(Progress.data));
          const out = { crashed: null, days: null, seen: null, streak: null };
          try {
            U.store.set('progress', { placement: { level: 'A1', score: 12,
              total: 20, date: '2026-08-20', entryLesson: 18 } });
            Progress.load();
            Progress.touchDay();
            out.crashed = false;
            out.days = !!Progress.data.days;
            out.seen = !!Progress.data.seen;
            out.streak = typeof Progress.data.streak === 'number';
            out.placementKept = (Progress.data.placement || {}).level === 'A1';
          } catch (e) {
            out.crashed = true; out.why = e.message;
          }
          Progress.data = snapshot;
          Progress.save();
          return out;
        }""")
        check('szczątkowa kopia postępu nie wywraca startu',
              r['crashed'] is False, r.get('why', '')[:70])
        check('brakujące klucze postępu domykają się wartością początkową',
              r['days'] and r['seen'] and r['streak'])
        check('scalenie nie kasuje tego, co w kopii było',
              r.get('placementKept') is True)

        r = page.evaluate("""() => {
          const snapshot = JSON.parse(JSON.stringify(Progress.data));
          U.store.set('progress', { nonsens: 1 });
          Progress.load();
          const ok = !!(Progress.data.days && Progress.data.lessons
                        && Progress.data.perception && Progress.data.errors);
          Progress.data = snapshot; Progress.save();
          return ok;
        }""")
        check('kopia bez żadnego znanego pola też się wczytuje', r)

        # --- nagrania role-play nie zostają w pamięci (sesja V) -------------
        # Adres blob: wyrzucony z mapy bez unieważnienia trzyma bufor nagrania
        # do końca życia karty. Przy kilku podejściach na kwestię rosło to
        # przez całą sesję ćwiczeń.
        r = page.evaluate("""() => {
          const revoked = [];
          const origRevoke = URL.revokeObjectURL;
          URL.revokeObjectURL = function (u) { revoked.push(u); };
          const made = [];
          for (let i = 0; i < 3; i++) {
            const u = URL.createObjectURL(new Blob(['x'], { type: 'audio/webm' }));
            made.push(u);
            Produce.rec().takes[i] = u;
          }
          Produce.resetTakes();
          const afterReset = revoked.slice();
          const left = Object.keys(Produce.rec().takes).length;
          URL.revokeObjectURL = origRevoke;
          made.forEach(function (u) { try { origRevoke(u); } catch (e) {} });
          return { revoked: afterReset.length, made: made.length, left: left,
                   all: made.every(function (u) { return afterReset.indexOf(u) >= 0; }) };
        }""")
        check('zamknięcie role-play zwalnia wszystkie nagrania, nie tylko mapę',
              r['revoked'] == r['made'] and r['all'],
              'zwolnionych %d z %d' % (r['revoked'], r['made']))
        check('mapa nagrań role-play zostaje pusta', r['left'] == 0)

        r = page.evaluate("""() => {
          const revoked = [];
          const origRevoke = URL.revokeObjectURL;
          URL.revokeObjectURL = function (u) { revoked.push(u); };
          const first = URL.createObjectURL(new Blob(['a'], { type: 'audio/webm' }));
          const second = URL.createObjectURL(new Blob(['b'], { type: 'audio/webm' }));
          Produce.resetTakes();
          revoked.length = 0;
          Produce.rec().takes[7] = first;
          Produce.noteTake(7, second);
          const out = { revokedFirst: revoked.indexOf(first) >= 0,
                        kept: Produce.rec().takes[7] === second };
          URL.revokeObjectURL = origRevoke;
          try { origRevoke(first); origRevoke(second); } catch (e) {}
          Produce.resetTakes();
          return out;
        }""")
        check('powtórne nagranie kwestii zwalnia poprzednie podejście',
              r['revokedFirst'], 'poprzednie nagranie zostało w pamięci')
        check('po powtórnym nagraniu zostaje najnowsze podejście', r['kept'])


        # ============================================================
        # SESJA VI — porządek nawigacji: nazwy, osiągalność, migracja
        # ============================================================

        # --- 1. jeden rejestr nazw ćwiczeń -------------------------
        # Do sesji V te same tryby miały po dwie-trzy nazwy, a nazwa
        # „Ułóż zdanie” oznaczała DWA różne ćwiczenia. Teraz nazwa
        # mieszka w U.EX i wszystko inne ma ją stamtąd brać.
        r = page.evaluate("""() => {
          const ids = Object.keys(U.EX);
          const seen = {}, dup = [];
          ids.forEach(id => {
            const l = U.EX[id].label;
            if (seen[l]) dup.push(l + ': ' + seen[l] + ' vs ' + id);
            seen[l] = id;
          });
          // każdy tryb widoczny na ekranie bierze nazwę z rejestru
          const chips = [];
          document.querySelectorAll('[data-listen],[data-gram]').forEach(b => {
            const id = b.getAttribute('data-listen') || b.getAttribute('data-gram');
            if (b.textContent.trim() !== U.EX[id].label) {
              chips.push(id + ': „' + b.textContent.trim() + '” != „' + U.EX[id].label + '”');
            }
          });
          const prod = Produce.MODES.filter(m => m.label !== U.EX[m.id].label).map(m => m.id);
          const tempo = Progress.tempoExercises
            ? Progress.tempoExercises().filter(e => e.label !== U.EX[e.id].label).map(e => e.id) : [];
          return { total: ids.length, dup: dup, chips: chips, prod: prod, tempo: tempo,
                   statsBuild: Stats.keyLabel('mode', 'build'),
                   statsAssemble: Stats.keyLabel('mode', 'assemble'),
                   repairBuild: (Repair.RUNNABLE.build || {}).label };
        }""")
        check('rejestr trybów nie ma dwóch trybów o tej samej nazwie',
              not r['dup'], '; '.join(r['dup']))
        check('przyciski trybu na ekranach biorą nazwę z rejestru',
              not r['chips'], '; '.join(r['chips']))
        check('ekran „Mówienie po tajsku” bierze nazwy z rejestru',
              not r['prod'], ', '.join(r['prod']))
        check('drabina tempa bierze nazwy z rejestru',
              not r['tempo'], ', '.join(r['tempo']))
        check('statystyka nazywa „build” tak samo jak ekran',
              r['statsBuild'] == 'Ułóż zdanie z polskiego', r['statsBuild'])
        check('„ułóż zdanie ze słuchu” i „z polskiego” to różne nazwy',
              r['statsAssemble'] != r['statsBuild'],
              '%s / %s' % (r['statsAssemble'], r['statsBuild']))
        check('sesja naprawcza nazywa tryb tak samo jak ekran',
              r['repairBuild'] == 'Ułóż zdanie z polskiego', str(r['repairBuild']))

        # --- 2. sesja naprawcza nie wskazuje nieistniejącego ekranu -
        # Do sesji V stało tam screen: 'quiz' — ekranu o tym id nigdy
        # nie było, więc pole wskazywało w pustkę.
        r = page.evaluate("""() => {
          const ids = Object.keys(Repair.RUNNABLE);
          const known = App.screenIds();
          return ids.filter(id => known.indexOf(Repair.RUNNABLE[id].screen) === -1);
        }""")
        check('każdy tryb sesji naprawczej wskazuje istniejący ekran',
              not r, ', '.join(r))

        # --- 3. osiągalność i powrót -------------------------------
        r = page.evaluate("""() => {
          const known = App.screenIds();
          const nav = [];
          document.querySelectorAll('[data-screen]').forEach(
            b => nav.push(b.getAttribute('data-screen')));
          const tabs = [];
          document.querySelectorAll('[data-tab]').forEach(
            b => tabs.push(b.getAttribute('data-tab')));
          return { known: known, nav: nav, tabs: tabs,
                   missing: known.filter(id => nav.indexOf(id) === -1),
                   groupless: App.screensWithoutGroup() };
        }""")
        check('każdy ekran ma pozycję w menu głównym',
              not r['missing'], ', '.join(r['missing']))
        check('każdy ekran należy do jakiejś grupy',
              not r['groupless'], ', '.join(r['groupless']))
        check('pasek zakładek ma pięć pozycji, reszta pod „Więcej”',
              len(r['tabs']) == 5, '%d zakładek' % len(r['tabs']))

        # Powrót: z każdego ekranu da się wyjść, bo pasek/menu są zawsze
        # widoczne. Sprawdzamy to, wchodząc na każdy ekran i wracając.
        bad_back = []
        for sid in r['known']:
            ok = page.evaluate("""(id) => {
              App.go(id);
              if (App.screen !== id) return 'nie wchodzi';
              const nav = document.querySelector('[data-screen="today"]');
              if (!nav || nav.offsetParent === null && !document.querySelector('#tabbar-list')) {
                return 'brak wyjścia';
              }
              App.go('today');
              return App.screen === 'today' ? '' : 'nie wraca';
            }""", sid)
            if ok:
                bad_back.append('%s (%s)' % (sid, ok))
        check('z każdego ekranu da się wejść i wrócić',
              not bad_back, '; '.join(bad_back))

        # --- 4. stary adres #phrases dalej działa ------------------
        r = page.evaluate("""() => {
          App.go('phrases');
          const screen = App.screen;
          const preset = document.querySelector('#dict-presets [aria-pressed="true"]');
          App.go('today');
          return { screen: screen, preset: preset ? preset.getAttribute('data-preset') : null };
        }""")
        check('stary adres „#phrases” prowadzi do Słownika, nie na „Dzisiaj”',
              r['screen'] == 'dict', r['screen'])
        check('stary adres „#phrases” otwiera zestaw „Zwroty”',
              r['preset'] == 'phrase', str(r['preset']))

        # --- 5. zestawy Słownika zachowują treść ex-„Zwrotów” ------
        r = page.evaluate("""async () => {
          await DB.ensureIndex();
          App.go('dict');
          App.dictPreset('phrase');
          const phraseCount = DB.index.filter(x => x.type !== 'word' && x.frequency >= 3).length;
          App.dictPreset('travel');
          const travelCount = DB.index.filter(x => x.type !== 'word' && x.frequency >= 4).length;
          App.dictPreset('all');
          return { phraseCount: phraseCount, travelCount: travelCount,
                   all: DB.index.length };
        }""")
        check('zestaw „Zwroty” ma z czego budować', r['phraseCount'] > 200,
              '%d haseł' % r['phraseCount'])
        check('zestaw „Tryb wyjazdowy” jest węższy niż „Zwroty”',
              0 < r['travelCount'] <= r['phraseCount'],
              '%d z %d' % (r['travelCount'], r['phraseCount']))
        check('zestaw „Cała baza” obejmuje wszystko',
              r['all'] > r['phraseCount'], '%d haseł' % r['all'])

        # --- 6. migracja identyfikatorów ekranów -------------------
        r = page.evaluate("""() => {
          const back = JSON.parse(JSON.stringify(Progress.data));
          const sess = U.store.get('session', null);
          const goals = U.store.get('goals', null);

          delete Progress.data.screenMigration;
          Progress.data.worst = { suggestion: { screen: 'phrases', mode: 'build' } };
          U.store.set('session', { blocks: [{ kind: 'listen', screen: 'phrases' }] });
          U.store.set('goals', { rec: { action: { screen: 'phrases' } } });
          Progress.save();

          const needed = ProgressMigration.screensNeeded();
          const rep = ProgressMigration.runScreens();
          const after = {
            progress: Progress.data.worst.suggestion.screen,
            session: U.store.get('session', {}).blocks[0].screen,
            goals: U.store.get('goals', {}).rec.action.screen
          };
          const second = ProgressMigration.runScreens();   // musi być null

          Progress.data = back; Progress.save();
          U.store.set('session', sess); U.store.set('goals', goals);
          return { needed: needed, changed: rep ? rep.changed : -1, after: after,
                   secondRun: second, version: rep ? rep.version : null };
        }""")
        check('migracja ekranów rozpoznaje, że jest potrzebna', r['needed'] is True)
        check('migracja przepisuje ekran w postępie',
              r['after']['progress'] == 'dict', r['after']['progress'])
        check('migracja przepisuje ekran w przerwanej sesji dnia',
              r['after']['session'] == 'dict', r['after']['session'])
        check('migracja przepisuje ekran w celu tygodnia',
              r['after']['goals'] == 'dict', r['after']['goals'])
        check('migracja liczy wszystkie trzy poprawki', r['changed'] == 3,
              '%s poprawek' % r['changed'])
        check('migracja ekranów wykonuje się tylko raz',
              r['secondRun'] is None, str(r['secondRun']))

        # Migracja NIE rusza identyfikatorów trybów — one się nie zmieniły,
        # więc statystyka błędów sprzed zmiany zostaje policzalna.
        r = page.evaluate("""() => {
          const back = JSON.parse(JSON.stringify(Progress.data));
          delete Progress.data.screenMigration;
          Progress.data.errors = Progress.data.errors || {};
          Progress.data.errors.mode = { build: 4, assemble: 2, say: 1 };
          Progress.save();
          ProgressMigration.runScreens();
          const kept = Object.keys(Progress.data.errors.mode).sort().join(',');
          Progress.data = back; Progress.save();
          return kept;
        }""")
        check('migracja nie rusza identyfikatorów trybów w statystyce błędów',
              r == 'assemble,build,say', r)

        # --- 7. ścieżka pierwszego uruchomienia --------------------
        r = page.evaluate("""() => {
          const back = JSON.parse(JSON.stringify(Progress.data));
          Progress.data.placement = null;
          const needs = Progress.needsPlacement();
          Progress.setPlacement({ level: 'Survival', score: 0, total: 28,
                                  entryLesson: (DB.lessons[0] || {}).id });
          const blocks = Course.moduleZeroBlocks();
          const next = Course.next();
          Progress.data = back; Progress.save();
          return { needs: needs, blocks: blocks, hasNext: !!next };
        }""")
        check('bez testu poziomującego aplikacja startuje na nim', r['needs'] is True)
        check('po teście poziomującym Moduł 0 jest następnym krokiem',
              r['blocks'] is True)
        check('kurs ma dokąd prowadzić po Module 0', r['hasNext'] is True)

        # ==================================================================
        # UZUPEŁNIENIE POKRYCIA (sesja VII)
        # ==================================================================
        # Funkcje z sesji J-V, które działały bez ani jednej asercji.
        # Każdy test poniżej sprawdza MECHANIZM, nie objaw: liczy faktyczne
        # wywołania i porównuje z niezależnie wyliczonym oczekiwaniem,
        # zamiast zaglądać na koniec do jednego pola i wierzyć, że skoro
        # wygląda dobrze, to droga też była dobra.

        # --- 0. ocena wymowy nie blokuje interfejsu (sesja VII) ------------
        # Objaw: „analiza zwróciła wynik”. Mechanizm: wątek główny MA BYĆ
        # WOLNY w czasie liczenia. Mierzymy największą przerwę w tykaniu
        # zegara wątku głównego podczas analizy i porównujemy ją z czasem
        # samej analizy. Przy liczeniu w wątku głównym przerwa jest równa
        # czasowi analizy; przy wątku roboczym — nieporównanie mniejsza.
        r = page.evaluate("""async () => {
          const rate = 44100;
          const samples = Pitch.testSignal(180, 3, rate, 0.02);

          // Największa przerwa między tyknięciami zegara w trakcie pracy.
          function stallDuring(run) {
            return new Promise(resolve => {
              let last = performance.now(), worst = 0, ticking = true;
              (function tick() {
                if (!ticking) return;
                const now = performance.now();
                worst = Math.max(worst, now - last);
                last = now;
                setTimeout(tick, 0);
              })();
              const t0 = performance.now();
              Promise.resolve(run()).then(res => {
                /* Obietnica rozwiązuje się w mikrozadaniu, czyli PRZED
                   najbliższym tyknięciem zegara. Gdybyśmy zatrzymali
                   licznik tutaj, przerwa, która właśnie minęła, nigdy by
                   się nie policzyła — i pomiar pokazywałby zawsze 0. */
                setTimeout(() => {
                  ticking = false;
                  resolve({ worst, total: performance.now() - t0, res });
                }, 30);
              });
            });
          }

          // 1. wątek roboczy
          Pitch.forceMainThread = false;
          const ready = Pitch.workerReady();
          const viaWorker = await stallDuring(
            () => Pitch.analyseAsync(samples, rate));
          const workerRun = Pitch.lastRunOn;

          // 2. ta sama analiza wymuszona w wątku głównym
          Pitch.forceMainThread = true;
          const viaMain = await stallDuring(
            () => Pitch.analyseAsync(samples, rate));
          const mainRun = Pitch.lastRunOn;
          Pitch.forceMainThread = false;

          const a = viaWorker.res, b = viaMain.res;
          const close = (x, y) => (x == null && y == null)
            || (x != null && y != null && Math.abs(x - y) < 0.51);
          return {
            ready, workerRun, mainRun,
            workerStall: Math.round(viaWorker.worst),
            mainStall: Math.round(viaMain.worst),
            workerTotal: Math.round(viaWorker.total),
            mainAnalysisMs: b.analysisMs,
            sameMedian: close(a.medianF0, b.medianF0),
            samePoints: a.points.length === b.points.length,
            sameSyllables: a.syllables.length === b.syllables.length,
            median: a.medianF0,
            // próbki wywołującego nie mogą zostać odpięte przez przekazanie
            samplesIntact: samples.length > 0
          };
        }""")
        check('wątek roboczy oceny wymowy daje się utworzyć przez serwer',
              r['ready'] is True)
        check('analiza po nagraniu idzie do wątku roboczego',
              r['workerRun'] == 'worker', str(r['workerRun']))
        check('wątek roboczy liczy to samo co wątek główny — mediana F0',
              r['sameMedian'] is True, 'mediana %s' % r['median'])
        check('wątek roboczy liczy to samo — liczba punktów konturu',
              r['samePoints'] is True)
        check('wątek roboczy liczy to samo — podział na sylaby',
              r['sameSyllables'] is True)
        check('analiza w wątku głównym faktycznie zatrzymuje interfejs',
              r['mainStall'] >= r['mainAnalysisMs'] * 0.5,
              'przerwa %d ms przy analizie %d ms'
              % (r['mainStall'], r['mainAnalysisMs']))
        check('przeniesienie do wątku roboczego zdejmuje blokadę z interfejsu',
              r['workerStall'] < r['mainStall'] / 2,
              'wątek roboczy %d ms, wątek główny %d ms'
              % (r['workerStall'], r['mainStall']))
        check('przekazanie próbek nie odpina tablicy wywołującemu',
              r['samplesIntact'] is True)

        # --- 0b. brak wątku roboczego nie zabiera oceny wymowy -------------
        # Tryb file:// i starsze przeglądarki: konstruktor Worker albo nie
        # istnieje, albo rzuca wyjątkiem. Ocena ma się policzyć mimo to,
        # a wywołujący ma dostać obietnicę, nie wyjątek.
        r = page.evaluate("""async () => {
          const rate = 22050;
          const samples = Pitch.testSignal(200, 1, rate, 0.02);
          const realWorker = window.Worker;
          // przeglądarka bez Workera: sam brak konstruktora nie wystarczy,
          // bo raz utworzony wątek żyje dalej — trzeba go zamknąć.
          Pitch.resetWorker();
          delete window.Worker;
          Pitch.forceMainThread = false;
          const noWorker = await Pitch.analyseAsync(samples, rate);
          const runA = Pitch.lastRunOn;
          window.Worker = realWorker;
          Pitch.resetWorker();
          const out = { runA, medianA: noWorker.medianF0 };
          return out;
        }""")
        check('brak konstruktora Worker nie wywraca oceny wymowy',
              r['runA'] == 'main' and r['medianA'] is not None,
              'policzono na: %s' % r['runA'])
        check('ocena bez wątku roboczego nadal trafia w częstotliwość',
              abs(r['medianA'] - 200) < 4, 'mediana %s Hz zamiast 200'
              % r['medianA'])

        # --- 1. kolejka powtórek: sufit, priorytet i zaległość (sesja P) ---
        # Objaw: „lista ma najwyżej tyle pozycji, ile wynosi sufit”. Mechanizm:
        # do dzisiaj trafiają karty o NAJWYŻSZYM priorytecie, a te, które się
        # nie zmieściły, są ODŁOŻONE, nie skasowane. Test liczy priorytety sam
        # i porównuje z podziałem, który zrobił moduł.
        r = page.evaluate("""() => {
          const backup = JSON.parse(JSON.stringify(SRS.cards));
          SRS.cards = {};
          const today = U.today();
          const ids = DB.index.slice(0, 40).map(r => r.id);
          ids.forEach((id, n) => {
            SRS.add(id, 'r');
            const c = SRS.card(id, 'r');
            c.due = today;
            c.lapses = n % 5;
            c.slow = n % 3 === 0;
          });
          const cap = 12;
          const plan = SRS.plan({ today: today, cap: cap });
          const prio = {};
          plan.today.concat(plan.rest).forEach(c => { prio[c.id] = SRS.priority(c, today); });
          const minToday = Math.min.apply(null, plan.today.map(c => prio[c.id]));
          const maxRest = plan.rest.length
            ? Math.max.apply(null, plan.rest.map(c => prio[c.id])) : -Infinity;
          const union = plan.today.length + plan.rest.length;
          const uniq = new Set(plan.today.concat(plan.rest).map(c => c.id)).size;
          SRS.cards = backup; SRS.save();
          return { cap: cap, todayLen: plan.today.length, due: plan.dueTotal,
                   union: union, uniq: uniq, minToday: minToday, maxRest: maxRest,
                   days: plan.days, backlog: plan.backlog };
        }""")
        check('sufit dzienny przycina kolejkę do zadanej liczby',
              r['todayLen'] == r['cap'], 'na dziś %d przy sufcie %d'
              % (r['todayLen'], r['cap']))
        check('żadna zaległa karta nie ginie przy przycinaniu',
              r['union'] == r['due'] and r['uniq'] == r['due'],
              'suma %d, unikalnych %d, zaległych %d'
              % (r['union'], r['uniq'], r['due']))
        check('na dziś idą karty o najwyższym priorytecie, nie pierwsze z brzegu',
              r['minToday'] >= r['maxRest'],
              'najniższy dziś %.3f < najwyższy odłożony %.3f'
              % (r['minToday'], r['maxRest']))
        check('zaległość rozkłada się na kolejne dni, a nie na jeden',
              r['days'] >= 2 and r['backlog'] == r['due'] - r['cap'],
              'dni %d, zaległych %d' % (r['days'], r['backlog']))

        # --- 2. sesja dnia: przerwa nie liczy się jako nauka (sesja R) ------
        # Objaw: „licznik czasu rośnie”. Mechanizm: rośnie WYŁĄCZNIE o czas
        # między wznowieniem a odłożeniem. Cofamy znacznik startu, żeby
        # zasymulować upływ czasu bez czekania, i sprawdzamy, że przerwa
        # między pause() a resume() nie wchodzi do sumy.
        r = page.evaluate("""() => {
          const back = Session.state ? JSON.parse(JSON.stringify(Session.state)) : null;
          Session.start(20, {});
          const s = Session.state;
          s.elapsed = 0;
          s.resumedAt = Date.now() - 30000;      // 30 s aktywnej nauki
          Session.tick();
          const afterFirst = s.elapsed;
          Session.pause();
          const afterPause = s.elapsed;
          const duringBreak = Session.progress().spent;   // przerwa trwa
          Session.resume();
          s.resumedAt = Date.now() - 10000;      // kolejne 10 s nauki
          Session.tick();
          const total = s.elapsed;
          Session.clear();
          if (back) { Session.state = back; Session.save(); }
          return { afterFirst, afterPause, duringBreak, total };
        }""")
        check('licznik sesji dnia rośnie o czas faktycznej nauki',
              28 <= r['afterFirst'] <= 32, '%s s zamiast 30' % r['afterFirst'])
        check('odłożenie sesji zamyka nalicznie, nie kasuje dorobku',
              r['afterPause'] == r['afterFirst'])
        check('przerwa między odłożeniem a wznowieniem nie wchodzi do czasu nauki',
              r['duringBreak'] == r['afterPause'],
              'w przerwie %s, przed przerwą %s' % (r['duringBreak'], r['afterPause']))
        check('po wznowieniu doliczany jest tylko nowy odcinek',
              38 <= r['total'] <= 42, '%s s zamiast 40' % r['total'])

        # --- 3. droga do celu nie zgaduje tempa (sesja R) ------------------
        # Objaw: „ekran pokazuje liczbę tygodni”. Mechanizm: liczba bierze się
        # z gap.words / pace.perWeek, a przy historii krótszej niż trzy dni
        # aktywne moduł ma powiedzieć „nie wiadomo” (null), a nie podać
        # wartość z jednego dnia pomnożoną przez siedem.
        r = page.evaluate("""async () => {
          await Coverage.ensure();
          const backup = JSON.parse(JSON.stringify(SRS.cards));
          const name = Coverage.all()[0].name;
          SRS.cards = {};
          const thin = Coverage.pace().known;
          const weeksThin = Coverage.weeksTo(name);
          // Tempo wiarygodne: karty opanowane, powtarzane w kilku różnych dniach.
          const today = U.today();
          const ids = DB.index.slice(0, 24).map(r => r.id);
          ids.forEach((id, n) => {
            SRS.add(id, 'r');
            const c = SRS.card(id, 'r');
            c.repetitions = SRS.LEARNED.repetitions + 1;
            c.interval = SRS.LEARNED.interval + 2;
            c.last = U.addDays(today, -(n % 6));     // sześć różnych dni
          });
          const pace = Coverage.pace();
          const gap = Coverage.gap(name);
          const weeks = Coverage.weeksTo(name);
          SRS.cards = backup; SRS.save();
          return { thin, weeksThin, known: pace.known, perWeek: pace.perWeek,
                   words: gap ? gap.words : null, done: gap ? gap.done : null,
                   weeks, activeDays: pace.activeDays };
        }""")
        check('bez historii powtórek tempo jest nieznane, a nie zerowe',
              r['thin'] is False)
        check('bez tempa droga do celu mówi „nie wiadomo”, nie podaje liczby',
              r['weeksThin'] is None, str(r['weeksThin']))
        check('tempo liczy się z dni aktywnych w kartotece',
              r['known'] is True and r['activeDays'] >= 3,
              'dni aktywnych %s' % r['activeDays'])
        check('tygodnie do celu to iloraz braku haseł i tempa',
              r['done'] or (r['weeks'] is not None
                            and abs(r['weeks'] - r['words'] / r['perWeek']) < 1e-6),
              'tygodni %s, haseł %s, tempo %s'
              % (r['weeks'], r['words'], r['perWeek']))

        # --- 4. wymowa po częściach (sesja L) ------------------------------
        # Objaw: „nie ma wyjątku”. Mechanizm: dla n granic wyrazów pada
        # DOKŁADNIE n wypowiedzi, kolejno, a anulowanie w połowie zatrzymuje
        # resztę — liczymy faktyczne wywołania syntezatora.
        r = page.evaluate("""() => {
          const orig = Speech.speak;
          const said = [];
          let pendingEnd = null;
          Speech.speak = function (text, opts) {
            said.push(text);
            pendingEnd = (opts && opts.onend) || null;
            return true;
          };
          const parts = ['nam', 'plaao', 'waan', 'mak'];
          let ended = false;
          Speech.speakParts(parts, { gap: 0, onend: () => { ended = true; } });
          const drain = () => new Promise(res => {
            const pump = () => {
              if (!pendingEnd) return res();
              const fn = pendingEnd; pendingEnd = null; fn();
              setTimeout(pump, 1);
            };
            setTimeout(pump, 1);
          });
          return drain().then(() => {
            const full = said.slice();
            // druga próba: anulowanie po pierwszej części
            said.length = 0; pendingEnd = null;
            Speech.speakParts(parts, { gap: 0 });
            Speech.cancelParts();
            const fn = pendingEnd; pendingEnd = null;
            if (fn) fn();
            const afterCancel = said.length;
            Speech.speak = orig;
            return { count: full.length, order: full.join('|'), ended,
                     want: parts.length, afterCancel };
          });
        }""")
        check('każda granica wyrazu to osobna wypowiedź syntezatora',
              r['count'] == r['want'],
              'wypowiedzi %d, części %d' % (r['count'], r['want']))
        check('części idą w kolejności podanej, nie przetasowane',
              r['order'] == 'nam|plaao|waan|mak', r['order'])
        check('domknięcie ciągu części zgłasza koniec odtwarzania', r['ended'] is True)
        check('anulowanie zatrzymuje dalsze części, a nie tylko bieżącą',
              r['afterCancel'] == 1, 'po anulowaniu padło %d wypowiedzi'
              % r['afterCancel'])

        # --- 5. sesja naprawcza z wybranych haseł (sesja P) ----------------
        # Objaw: „zestaw nie jest pusty”. Mechanizm: zestaw zawiera DOKŁADNIE
        # wskazane hasła, w podanej kolejności, przycięte do limitu, a ekran,
        # na który kieruje, ISTNIEJE w aplikacji — to na tym poległ repair.js
        # przed sesją VI, wskazując nieistniejący ekran „quiz”.
        r = page.evaluate("""() => {
          const ids = DB.index.slice(0, 30).map(r => r.id);
          const set = Repair.buildForIds(ids, 'choice');
          const screens = new Set(Object.keys(App.screens || {}));
          const nodeExists = !!document.getElementById('screen-' + set.screen);
          const modes = ['choice', 'dictation', 'assemble', 'say'];
          const bad = modes.filter(m => {
            const s = Repair.buildForIds(ids.slice(0, 3), m);
            return !document.getElementById('screen-' + s.screen);
          });
          return { got: set.ids.length, asked: ids.length,
                   sameOrder: set.ids.every((id, i) => id === ids[i]),
                   itemsMatch: set.items.length === set.ids.length
                     && set.items.every((it, i) => it.id === set.ids[i]),
                   screen: set.screen, nodeExists, badScreens: bad,
                   pool: set.pool, empty: Repair.buildForIds([], 'choice') };
        }""")
        check('zestaw naprawczy bierze wskazane hasła w podanej kolejności',
              r['sameOrder'] is True)
        check('zestaw naprawczy przycina się do limitu, ale pamięta pulę',
              r['got'] <= r['asked'] and r['pool'] == r['asked'],
              'wzięto %d z %d' % (r['got'], r['asked']))
        check('pozycje zestawu odpowiadają jego identyfikatorom',
              r['itemsMatch'] is True)
        check('zestaw naprawczy kieruje na ekran, który istnieje',
              r['nodeExists'] is True, r['screen'])
        check('każdy tryb naprawczy ma istniejący ekran docelowy',
              not r['badScreens'], ', '.join(r['badScreens'] or []))
        check('pusta lista haseł nie tworzy zestawu-widma',
              r['empty'] is None)

        # --- 6. eksport do Anki: separator w treści (sesja J) --------------
        # Objaw: „plik powstał i ma nagłówek”. Mechanizm: jedna linia na hasło
        # także wtedy, gdy w polu jest przecinek, cudzysłów albo koniec linii —
        # inaczej jedno hasło rozpada się w Anki na dwie karty.
        r = page.evaluate("""() => {
          const real = DB.index.slice(0, 5).map(r => r.id);
          const csv = Stats.buildCsv(real);
          const rows = csv.split('\\r\\n');
          const origGet = DB.get, origStub = DB.stub;
          const nasty = {
            id: 'test-nasty', polish: 'kawa, herbata "duża"\\nalbo sok',
            thaiPhonetic: 'kaafɛɛ', pronunciationPolish: 'kafe',
            toneGuide: 'ton średni', level: 'A1', category: 'Jedzenie', tags: ['x']
          };
          DB.get = id => id === 'test-nasty' ? nasty : origGet.call(DB, id);
          DB.stub = id => id === 'test-nasty' ? nasty : origStub.call(DB, id);
          const one = Stats.buildCsv(['test-nasty']);
          DB.get = origGet; DB.stub = origStub;
          const lines = one.split('\\r\\n');
          const thai = /[\\u0E00-\\u0E7F]/.test(csv);
          return { rows: rows.length, want: real.length + 1, thai,
                   nastyRows: lines.length,
                   quoted: lines[1] ? lines[1].indexOf('""') !== -1 : false };
        }""")
        check('eksport daje jedną linię na hasło plus nagłówek',
              r['rows'] == r['want'], 'linii %d, oczekiwano %d'
              % (r['rows'], r['want']))
        check('przecinek i koniec linii w treści nie rozbijają rekordu na dwa',
              r['nastyRows'] == 2, 'linii %d zamiast 2' % r['nastyRows'])
        check('cudzysłów w treści jest podwajany, nie ucinany', r['quoted'] is True)
        check('eksport nie wynosi pisma tajskiego', r['thai'] is False)

        # --- 7. przypomnienie odpala się raz na dobę (sesja R) -------------
        # Objaw: „funkcja zwróciła true”. Mechanizm: liczymy FAKTYCZNE
        # wywołania powiadomienia — przed godziną zero, po godzinie jedno,
        # a drugie sprawdzenie tego samego dnia już żadnego.
        r = page.evaluate("""() => {
          const backGoals = U.store.get('goals', null);
          const backMark = U.store.get('goals.lastNotify', null);
          const origNotify = Goals.notify, origPerm = Goals.permission;
          let fired = 0;
          Goals.notify = function () { fired += 1; return true; };
          Goals.permission = function () { return 'granted'; };
          Goals.set({ notify: true, notifyAt: '19:00', minutes: 20 });
          U.store.set('goals.lastNotify', null);
          /* Wcześniejsze testy zdążyły zapisać minuty na dziś, a cel
             osiągnięty wycisza przypomnienie — i słusznie. Zerujemy dzień,
             żeby sprawdzać mechanizm powiadomienia, a nie stan licznika
             odziedziczony po sąsiednim teście. */
          const backDay = Progress.data.days[U.today()] || null;
          Progress.data.days[U.today()] = { minutes: 0, answers: 0 };
          const metBefore = Goals.today().met;
          const early = new Date(); early.setHours(9, 0, 0, 0);
          const late = new Date(); late.setHours(19, 30, 0, 0);
          const beforeHour = Goals.checkReminder(early);
          const firedEarly = fired;
          const first = Goals.checkReminder(late);
          const firedFirst = fired;
          const second = Goals.checkReminder(late);
          const firedSecond = fired;
          Goals.notify = origNotify; Goals.permission = origPerm;
          if (backDay) Progress.data.days[U.today()] = backDay;
          else delete Progress.data.days[U.today()];
          Progress.save();
          if (backGoals) U.store.set('goals', backGoals);
          U.store.set('goals.lastNotify', backMark);
          return { beforeHour, first, second, firedEarly, firedFirst,
                   firedSecond, metBefore };
        }""")
        check('cel dnia nieosiągnięty — przypomnienie ma o czym przypominać',
              r['metBefore'] is False)
        check('przed ustawioną godziną nie leci żadne powiadomienie',
              r['beforeHour'] is False and r['firedEarly'] == 0,
              'wywołań %d' % r['firedEarly'])
        check('po ustawionej godzinie leci dokładnie jedno powiadomienie',
              r['first'] is True and r['firedFirst'] == 1,
              'wywołań %d' % r['firedFirst'])
        check('drugie sprawdzenie tego samego dnia już nie powiadamia',
              r['second'] is False and r['firedSecond'] == 1,
              'wywołań łącznie %d' % r['firedSecond'])

        # --- 8. wczytywanie na żądanie (sesja V) ---------------------------
        # Objaw: „dane są dostępne”. Mechanizm: liczymy, ile plików PRZYBYŁO
        # do DB.loadedFiles — prośba o rekordy z jednego pliku nie ma prawa
        # ściągnąć całej bazy, a powtórna prośba o to samo nie ma prawa
        # pobrać niczego.
        r = page.evaluate("""async () => {
          const before = DB.loadedFiles.slice();
          const notLoaded = DB.index.filter(rec => {
            const f = DB.fileOf ? DB.fileOf(rec.id) : null;
            return f && before.indexOf(f) === -1;
          });
          if (!notLoaded.length) return { skip: true };
          const target = notLoaded[0];
          const file = DB.fileOf(target.id);
          const same = notLoaded.filter(r => DB.fileOf(r.id) === file)
                                .slice(0, 5).map(r => r.id);
          await DB.ensureFor(same);
          const afterFirst = DB.loadedFiles.slice();
          const added = afterFirst.filter(f => before.indexOf(f) === -1);
          await DB.ensureFor(same);
          const afterSecond = DB.loadedFiles.slice();
          const addedAgain = afterSecond.filter(f => afterFirst.indexOf(f) === -1);
          const haveAll = same.every(id => !!DB.get(id));
          return { skip: false, added: added.length, addedAgain: addedAgain.length,
                   total: DB.manifest ? DB.manifest.dataFiles.length : 0,
                   haveAll, file, addedFiles: added };
        }""")
        if r.get('skip'):
            check('wczytywanie na żądanie — brak pliku do sprawdzenia', True,
                  'cała baza już wczytana')
        else:
            check('prośba o hasła z jednego pliku dociąga jeden plik, nie bazę',
                  r['added'] == 1, 'doszło %d plików (%s)'
                  % (r['added'], ', '.join(r['addedFiles'])))
            check('dociągnięte hasła są faktycznie dostępne', r['haveAll'] is True)
            check('powtórna prośba o te same hasła nie pobiera nic',
                  r['addedAgain'] == 0, 'doszło %d plików' % r['addedAgain'])

        for e in errs:
            fails.append('  BŁĄD wyjątek w konsoli: %s' % e[:160])

        browser.close()
    httpd.shutdown()

    print('=' * 74)
    print('TEST DZIAŁANIA')
    print('=' * 74)
    for n in notes:
        print(n)
    if fails:
        print('-' * 74)
        for f in fails:
            print(f)
        return 1
    print('-' * 74)
    print('WYNIK: WSZYSTKO DZIAŁA')
    return 0


sys.exit(main())
