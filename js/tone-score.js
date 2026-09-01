/* Thai All-in-One — ocena wymowy tonalnej.

   Dlaczego surowe herce są bezużyteczne
   -------------------------------------
   Ton tajski nie jest wysokością bezwzględną. Bas mówiący tonem wysokim
   schodzi niżej niż sopran mówiący tonem niskim, a obaj mówią poprawnie.
   Znaczenie niesie PRZEBIEG względem własnego zakresu mówiącego. Dlatego
   zanim cokolwiek porównamy, przeliczamy kontur na skalę pięciostopniową
   Chao (1 = dno zakresu, 5 = szczyt) — tę samą, w której od stu lat opisuje
   się tony azjatyckie: ton średni to 33, niski 21, opadający 51, wysoki 45,
   rosnący 214.

   Przeliczenie idzie przez półtony (logarytm), nie przez herce liniowo, bo
   ucho słyszy stosunki częstotliwości, a nie ich różnice. Punktem odniesienia
   jest mediana głosu użytkownika i rozstęp jego zakresu, liczone z jego
   dotychczasowych nagrań i trzymane w ustawieniach — im więcej nagra, tym
   celniejsza jest skala.

   Skąd bierze się wzorzec
   -----------------------
   Zadanie zakładało kontur wyliczony z nagrania syntezatora tego samego
   zdania. Tego się w przeglądarce zrobić nie da: strumień SpeechSynthesis
   nie jest dostępny dla Web Audio API — żadna przeglądarka nie pozwala go
   przechwycić ani przekierować do analizy. Zamiast udawać, że jest inaczej,
   moduł ma dwie drogi i za każdym razem mówi wprost, której użył:

     1. „lektor” — hasło ma plik w katalogu audio/. Wtedy wzorzec liczymy tym
        samym torem YIN, co nagranie użytkownika. To wzorzec prawdziwy.
     2. „model” — pliku nie ma (stan domyślny tej aplikacji). Wzorzec budujemy
        z zapisu fonetycznego: znak tonu nad sylabą wyznacza kształt, a długość
        samogłoski i typ tonu — czas jego trwania.

     Model opisuje ton wzorcowy w izolacji. Nie zna koartykulacji, akcentu
     zdaniowego ani opadania linii tonalnej pod koniec wypowiedzi. Ocena
     kształtu pojedynczej sylaby jest przy nim rzetelna, ocena melodii całego
     długiego zdania — orientacyjna. Jest to napisane także w interfejsie. */
(function (global) {
  'use strict';

  var ToneScore = {};

  /* ================================================= ZAKRES GŁOSU */

  var STORE_KEY = 'voice';
  var MAX_SAMPLES = 40;
  var DEFAULT_HALF_SPAN = 4;     // półtonów w każdą stronę, gdy brak danych

  ToneScore.voiceData = function () {
    var v = U.store.get(STORE_KEY, null);
    if (!v || !Array.isArray(v.samples)) v = { samples: [] };
    return v;
  };

  /* Zakres liczony z dotychczasowych nagrań. Mediana median opisuje środek
     głosu, a mediana rozstępów — jego rozpiętość w mowie. Pojedyncze nagranie
     bywa nietypowe (szept, krzyk), więc bierzemy medianę, nie średnią. */
  ToneScore.voiceRange = function () {
    var v = ToneScore.voiceData();
    var ok = v.samples.filter(function (s) { return s && s.m > 0 && s.lo > 0 && s.hi > s.lo; });
    if (ok.length < 3) {
      return { median: null, halfSpan: DEFAULT_HALF_SPAN, samples: ok.length, personalised: false };
    }
    var med = Pitch.median(ok.map(function (s) { return s.m; }));
    var spans = ok.map(function (s) { return 12 * Math.log(s.hi / s.lo) / Math.LN2 / 2; });
    var half = Pitch.median(spans);
    if (!(half > 0)) half = DEFAULT_HALF_SPAN;
    half = Math.min(9, Math.max(2.5, half));
    return { median: med, halfSpan: half, samples: ok.length, personalised: true };
  };

  /* Zapisujemy statystykę nagrania, nie samo nagranie. Głos zmienia się
     z porą dnia i nastrojem, więc trzymamy ostatnie czterdzieści prób. */
  ToneScore.observe = function (analysis) {
    if (!analysis || !analysis.medianF0 || !analysis.p10 || !analysis.p90) return null;
    if (analysis.points.length < 8) return null;
    var v = ToneScore.voiceData();
    v.samples.push({
      m: Math.round(analysis.medianF0 * 10) / 10,
      lo: Math.round(analysis.p10 * 10) / 10,
      hi: Math.round(analysis.p90 * 10) / 10,
      d: U.today()
    });
    if (v.samples.length > MAX_SAMPLES) v.samples = v.samples.slice(-MAX_SAMPLES);
    U.store.set(STORE_KEY, v);
    return ToneScore.voiceRange();
  };

  ToneScore.resetVoice = function () { U.store.remove(STORE_KEY); };

  /* Herce -> skala Chao 1–5 względem podanego środka i rozpiętości. */
  function toChao(hz, centre, halfSpan) {
    if (!hz || !centre) return null;
    var st = 12 * Math.log(hz / centre) / Math.LN2;
    var c = 3 + 2 * (st / halfSpan);
    if (c < 0.4) c = 0.4;
    if (c > 5.6) c = 5.6;
    return c;
  }
  ToneScore.toChao = toChao;

  /* Normalizacja całego konturu. Gdy użytkownik nie ma jeszcze historii,
     odnosimy nagranie do jego własnej mediany — skala jest wtedy poprawna
     w obrębie tej jednej wypowiedzi, ale nie porównuje się między nagraniami. */
  ToneScore.normalise = function (analysis, range) {
    range = range || ToneScore.voiceRange();
    var centre = range.personalised ? range.median : analysis.medianF0;
    var half = range.halfSpan;
    if (!range.personalised) {
      /* Bez historii rozpiętość bierzemy z tego nagrania — z dolnym
         ograniczeniem, żeby monotonna wypowiedź nie została sztucznie
         rozciągnięta na całą skalę. */
      if (analysis.p10 && analysis.p90 && analysis.p90 > analysis.p10) {
        half = Math.min(9, Math.max(3, 12 * Math.log(analysis.p90 / analysis.p10) / Math.LN2 / 2));
      }
    }
    return {
      centre: centre,
      halfSpan: half,
      personalised: !!range.personalised,
      samples: range.samples,
      points: (analysis.points || []).map(function (p) {
        return { t: p.t, c: toChao(p.f, centre, half), f: p.f };
      }).filter(function (p) { return p.c !== null; })
    };
  };

  /* ============================================ WZORZEC MODELOWY */

  /* Kształty pięciu tonów w skali Chao. Punkty rozłożone równomiernie
     w czasie trwania sylaby. */
  var SHAPES = {
    'średni':     [3.05, 3.0, 2.95, 2.85],
    'niski':      [2.2, 1.95, 1.75, 1.6],
    'opadający':  [4.4, 4.75, 3.9, 2.6, 1.8],
    'wysoki':     [3.6, 4.15, 4.55, 4.6],
    'rosnący':    [2.4, 1.85, 2.1, 3.1, 4.0]
  };

  /* Ton opadający i rosnący potrzebują czasu — w mowie są wyraźnie dłuższe
     niż płaskie. Sylaba z długą samogłoską też. */
  var BASE_MS = 260;

  ToneScore.SHAPES = SHAPES;

  /* Długość samogłoski z zapisu fonetycznego.

     Oceniamy ją tylko tam, gdzie zapis jest jednoznaczny: podwojona litera
     to samogłoska długa, pojedyncza zamknięta spółgłoską to krótka. Zapisy
     dwuznaczne w tej transkrypcji — „aw” (raz ɔɔ długie, raz dyftong aw),
     „ae”, „ia”, „ua”, „uea” — zostawiamy bez werdyktu, bo lepiej nie ocenić
     niż ocenić błędnie. */
  ToneScore.vowelLength = function (syllable) {
    var s = U.fold(syllable || '');
    if (!s) return { length: null, confident: false };
    if (/aa|ii|uu|ee|oo/.test(s)) return { length: 'long', confident: true };
    if (/uea|aw|oe|ue|ae|ia|ua/.test(s)) return { length: 'long', confident: false };
    if (/ai|ao|oi|ui|iu|eo/.test(s)) return { length: 'short', confident: false };
    if (/[aeiou][bcdfghjklmnpqrstvwxyz]+$/.test(s)) return { length: 'short', confident: true };
    return { length: 'short', confident: false };
  };

  /* Oczekiwany opis sylab z samego zapisu fonetycznego. */
  ToneScore.expected = function (phonetic, syllableList) {
    var list = (syllableList && syllableList.length) ? syllableList : U.syllables(phonetic);
    return list.map(function (syl) {
      var tone = U.toneOf(syl);
      var len = ToneScore.vowelLength(syl);
      var ms = BASE_MS * (len.length === 'long' ? 1 : 0.66);
      if (tone === 'opadający' || tone === 'rosnący') ms *= 1.18;
      return {
        label: syl,
        plain: U.stripTones(syl),
        tone: tone,
        length: len.length,
        lengthConfident: len.confident,
        modelMs: Math.round(ms)
      };
    });
  };

  /* Kontur wzorcowy zbudowany z modelu. Zwraca punkty w skali Chao razem
     z granicami sylab — w tej samej postaci co kontur zmierzony. */
  ToneScore.modelContour = function (expected, gapMs) {
    gapMs = gapMs === undefined ? 40 : gapMs;
    var points = [], spans = [], t = 0;
    expected.forEach(function (e, i) {
      var shape = SHAPES[e.tone] || SHAPES['średni'];
      var start = t;
      for (var k = 0; k < shape.length; k++) {
        points.push({ t: (start + e.modelMs * k / (shape.length - 1)) / 1000, c: shape[k] });
      }
      spans.push({ startMs: start, endMs: start + e.modelMs, durationMs: e.modelMs,
                   voicedMs: e.modelMs, points: points.slice(-shape.length) });
      t = start + e.modelMs + (i < expected.length - 1 ? gapMs : 0);
    });
    return { points: points, syllables: spans, totalMs: t, source: 'model' };
  };

  /* =================================================== WYRÓWNANIE */

  /* Próbkowanie konturu na równą siatkę — DTW potrzebuje szeregów, nie
     rozrzuconych punktów. Luki (odcinki bezdźwięczne) zostają puste. */
  function grid(points, stepMs, fromMs, toMs) {
    var out = [];
    if (!points.length) return out;
    var from = fromMs === undefined ? points[0].t * 1000 : fromMs;
    var to = toMs === undefined ? points[points.length - 1].t * 1000 : toMs;
    var i = 0;
    for (var ms = from; ms <= to; ms += stepMs) {
      while (i < points.length - 1 && points[i + 1].t * 1000 < ms) i++;
      var a = points[i], b = points[Math.min(i + 1, points.length - 1)];
      var am = a.t * 1000, bm = b.t * 1000;
      if (ms < am - 60 || ms > bm + 60) { out.push(null); continue; }
      if (bm === am) { out.push(a.c); continue; }
      var w = Math.min(1, Math.max(0, (ms - am) / (bm - am)));
      out.push(a.c * (1 - w) + b.c * w);
    }
    return out;
  }
  ToneScore.grid = grid;

  /* Dynamiczne wyrównanie czasowe. Uczący się mówi wolniej niż wzorzec —
     bez wyrównania każda różnica tempa byłaby liczona jako błąd tonu.
     Zwracamy średnią odległość na ścieżce, w jednostkach skali Chao. */
  ToneScore.dtw = function (a, b) {
    var A = a.filter(function (x) { return x !== null; });
    var B = b.filter(function (x) { return x !== null; });
    if (!A.length || !B.length) return { distance: null, path: [] };
    var n = A.length, m = B.length;
    var prev = new Float64Array(m + 1), cur = new Float64Array(m + 1);
    var back = [];
    var i, j;
    for (j = 0; j <= m; j++) prev[j] = Infinity;
    prev[0] = 0;
    for (i = 1; i <= n; i++) {
      cur[0] = Infinity;
      var row = new Uint8Array(m + 1);
      for (j = 1; j <= m; j++) {
        var cost = Math.abs(A[i - 1] - B[j - 1]);
        var d1 = prev[j - 1], d2 = prev[j], d3 = cur[j - 1];
        var best = d1, dir = 1;
        if (d2 < best) { best = d2; dir = 2; }
        if (d3 < best) { best = d3; dir = 3; }
        cur[j] = cost + best;
        row[j] = dir;
      }
      back.push(row);
      var tmp = prev; prev = cur; cur = tmp;
    }
    /* Odtworzenie ścieżki — potrzebne, żeby policzyć jej długość i podać
       odległość na krok, a nie sumę zależną od czasu trwania. */
    var steps = 0;
    i = n; j = m;
    while (i > 0 && j > 0) {
      var d = back[i - 1][j];
      steps++;
      if (d === 1) { i--; j--; }
      else if (d === 2) { i--; }
      else { j--; }
    }
    var total = prev[m];
    return {
      distance: steps ? total / steps : null,
      steps: steps,
      lenA: n,
      lenB: m
    };
  };

  /* ============================================== ROZPOZNANIE TONU */

  /* Który ton uczący się faktycznie wyprodukował. Decydują trzy cechy:
     poziom środkowy, różnica koniec–początek i to, gdzie w sylabie leży
     skrajny punkt. Rozpoznanie działa na konturze znormalizowanym, więc
     progi są takie same dla każdego głosu. */
  ToneScore.classify = function (points) {
    if (!points || points.length < 3) return { tone: null, confidence: 0 };
    var vals = points.map(function (p) { return p.c; });
    var n = vals.length;
    function mean(from, to) {
      var s = 0, k = 0;
      for (var i = Math.max(0, from); i < Math.min(n, to); i++) { s += vals[i]; k++; }
      return k ? s / k : null;
    }
    var head = mean(0, Math.max(1, Math.round(n * 0.3)));
    var tail = mean(Math.round(n * 0.7), n);
    var mid = mean(0, n);
    var delta = tail - head;

    var maxI = 0, minI = 0;
    for (var i = 1; i < n; i++) {
      if (vals[i] > vals[maxI]) maxI = i;
      if (vals[i] < vals[minI]) minI = i;
    }
    var range = vals[maxI] - vals[minI];
    var out, conf;

    if (delta <= -0.75 && maxI < n * 0.65) {
      out = 'opadający';
      conf = Math.min(1, Math.abs(delta) / 1.8);
    } else if (delta >= 0.75 && minI < n * 0.75) {
      out = 'rosnący';
      conf = Math.min(1, delta / 1.8);
    } else if (mid >= 3.65) {
      out = 'wysoki';
      conf = Math.min(1, (mid - 3.2) / 1.0);
    } else if (mid <= 2.45) {
      out = 'niski';
      conf = Math.min(1, (2.9 - mid) / 1.0);
    } else {
      out = 'średni';
      conf = Math.min(1, 1 - Math.abs(mid - 3) / 0.8) * (range < 1.2 ? 1 : 0.6);
    }
    return {
      tone: out,
      confidence: Math.max(0.15, Math.min(1, conf)),
      head: head, tail: tail, mid: mid, delta: delta, range: range
    };
  };

  /* ===================================================== OCENA */

  /* Podpowiedź nastawiona na PRODUKCJĘ, nie na rozpoznanie ze słuchu:
     mówi, co zrobić z własnym głosem. */
  var FIX = {
    'średni>wysoki': 'Ta sylaba wyszła na poziomie zwykłej mowy. Ton wysoki trzeba trzymać wyraźnie wyżej i nie pozwolić mu opaść na końcu.',
    'średni>niski': 'Zejdź niżej i utrzymaj tę wysokość do końca sylaby. Ton niski leży pod poziomem zwykłej mowy i jest płaski.',
    'średni>opadający': 'Brakuje spadku. Zacznij wysoko i pozwól głosowi zjechać w dół w obrębie jednej sylaby — jak przy zawiedzionym „ooo”.',
    'średni>rosnący': 'Brakuje podjazdu. Ton rosnący najpierw lekko opada, a potem wyraźnie idzie w górę — jak polskie pytanie „tak?”.',
    'wysoki>średni': 'Wyszło za wysoko. Ton średni jest płaski, na poziomie zwykłej mowy — nie podnoś go.',
    'wysoki>opadający': 'Zacząłeś wysoko, ale nie zszedłeś. Ton opadający musi skończyć wyraźnie niżej, niż się zaczął.',
    'niski>średni': 'Wyszło za nisko. Ton średni leży na poziomie zwykłej mowy, bez schodzenia w dół.',
    'niski>opadający': 'Cała sylaba wyszła nisko i płasko. Ton opadający zaczyna się wysoko — dopiero potem spada.',
    'niski>rosnący': 'Zostałeś na dole. Ton rosnący z dołu wychodzi w górę — końcówka musi być wyraźnie wyżej.',
    'opadający>średni': 'Za dużo ruchu. Ton średni jest płaski — trzymaj jedną wysokość przez całą sylabę.',
    'opadający>rosnący': 'Kontur wyszedł odwrotnie. Rosnący idzie z dołu w górę, opadający z góry w dół — sprawdź, gdzie kończysz.',
    'opadający>wysoki': 'Opadasz tam, gdzie trzeba utrzymać wysokość. Ton wysoki zostaje u góry do samego końca.',
    'rosnący>średni': 'Za dużo ruchu w górę. Ton średni jest płaski i neutralny.',
    'rosnący>opadający': 'Kontur wyszedł odwrotnie. Zacznij wysoko i zjedź w dół, nie odwrotnie.',
    'rosnący>niski': 'Podnosisz głos tam, gdzie trzeba go trzymać nisko i płasko.',
    'rosnący>wysoki': 'Ton wysoki nie jest podjazdem z dołu — zaczyna się już wysoko i tam zostaje.',
    'wysoki>rosnący': 'Ton rosnący ma początek nisko. Ty zacząłeś od razu u góry, więc słychać ton wysoki.',
    'wysoki>niski': 'Wyszło u góry zamiast na dole. Ton niski leży pod poziomem zwykłej mowy.',
    'niski>wysoki': 'Wyszło na dole zamiast u góry. Ton wysoki jest wyraźnie nad poziomem zwykłej mowy.',
    'średni>średni': ''
  };

  ToneScore.fix = function (produced, expected) {
    if (!produced || produced === expected) return '';
    return FIX[produced + '>' + expected]
      || ('Wyszedł ton ' + produced + ', a powinien ' + expected + '. Posłuchaj wzoru i powtórz samą tę sylabę.');
  };

  function pointsIn(points, startMs, endMs) {
    return points.filter(function (p) {
      var ms = p.t * 1000;
      return ms >= startMs && ms <= endMs;
    });
  }

  /* Główne wejście modułu.

     rec       — rekord (potrzebne: thaiPhonetic, syllables, audioFile),
     analysis  — wynik Pitch.analyse na nagraniu użytkownika,
     reference — opcjonalny wynik Pitch.analyse nagrania lektora.

     Zwraca komplet: ocena liczbowa, słowna, rozpis na sylaby, oba kontury
     w skali Chao i dane do wykresu oraz do tabeli. */
  ToneScore.evaluate = function (rec, analysis, reference) {
    var expected = ToneScore.expected(rec.thaiPhonetic, rec.syllables);
    var range = ToneScore.voiceRange();
    var user = ToneScore.normalise(analysis, range);

    if (!user.points.length || analysis.voicedRatio < 0.04) {
      return {
        ok: false,
        empty: true,
        message: 'W nagraniu nie słychać głosu — same szumy albo cisza. '
          + 'Nagraj jeszcze raz, mów wyraźnie i bliżej mikrofonu.',
        expected: expected,
        analysis: analysis,
        normalisation: user
      };
    }

    /* --- wzorzec --- */
    var ref, refSource;
    if (reference && reference.points && reference.points.length > 6) {
      var refNorm = ToneScore.normalise(reference, { personalised: false, halfSpan: DEFAULT_HALF_SPAN, samples: 0 });
      var refSyl = Pitch.segment(reference, expected.length).map(function (s) {
        return {
          startMs: s.startMs, endMs: s.endMs, durationMs: s.durationMs, voicedMs: s.voicedMs,
          points: pointsIn(refNorm.points, s.startMs, s.endMs)
        };
      });
      ref = { points: refNorm.points, syllables: refSyl, totalMs: reference.duration * 1000 };
      refSource = 'lektor';
    } else {
      ref = ToneScore.modelContour(expected);
      refSource = 'model';
    }

    /* --- korekta środka przy braku historii ---
       Bez własnego zakresu środkiem skali jest mediana tego jednego nagrania,
       a to zakłada, że przeciętna wysokość wypowiedzi wypada na tonie średnim.
       Dla krótkiej wypowiedzi to nieprawda: „khǎw-thóot” składa się z tonu
       rosnącego i wysokiego, więc jej mediana leży wysoko i przy naiwnym
       wyśrodkowaniu ton wysoki wygląda na średni. Przesuwamy więc kontur tak,
       żeby jego mediana pokryła się z medianą wzorca — czyli usuwamy stałe
       przesunięcie, a zostawiamy kształt, bo tylko kształt niesie ton.
       Przy własnym zakresie (od trzeciego nagrania) korekty nie robimy:
       wtedy odniesieniem jest realna mediana głosu użytkownika. */
    var offset = 0;
    if (!user.personalised) {
      var mu = Pitch.median(user.points.map(function (p) { return p.c; }));
      var mr = Pitch.median(ref.points.map(function (p) { return p.c; }));
      if (mu !== null && mr !== null) {
        offset = Math.max(-1.5, Math.min(1.5, mr - mu));
        user.points.forEach(function (p) {
          p.c = Math.max(0.4, Math.min(5.6, p.c + offset));
        });
      }
    }

    /* --- podział nagrania na tyle sylab, ile ma zapis --- */
    var userSyl = Pitch.segment(analysis, expected.length);

    /* --- odległość konturów po normalizacji i wyrównaniu czasowym --- */
    var step = 20;
    var gu = grid(user.points, step);
    var gr = grid(ref.points, step);
    var dtw = ToneScore.dtw(gu, gr);

    /* --- ocena per sylaba --- */
    var meanVoiced = Pitch.median(userSyl.map(function (s) { return s.voicedMs || s.durationMs; })) || 1;
    var syllables = expected.map(function (e, i) {
      var seg = userSyl[i] || null;
      var pts = seg ? pointsIn(user.points, seg.startMs, seg.endMs) : [];
      var got = ToneScore.classify(pts);
      var refPts = (ref.syllables[i] || {}).points || [];
      var toneOk = got.tone === e.tone;

      /* Długość samogłoski: porównujemy jądro dźwięczne tej sylaby z medianą
         jąder w tej wypowiedzi, więc ocena nie zależy od tempa mówienia. */
      var lengthVerdict = null, ratio = null;
      if (seg && e.lengthConfident && expected.length > 1) {
        ratio = (seg.voicedMs || seg.durationMs) / meanVoiced;
        if (e.length === 'long' && ratio < 0.85) lengthVerdict = 'za krótka';
        else if (e.length === 'short' && ratio > 1.45) lengthVerdict = 'za długa';
        else lengthVerdict = 'w porządku';
      } else if (seg && e.lengthConfident) {
        /* Wypowiedź jednosylabowa — nie ma z czym porównać wewnątrz niej,
           więc odnosimy się do typowego czasu trwania sylaby w mowie. */
        var ms = seg.voicedMs || seg.durationMs;
        if (e.length === 'long' && ms < 150) lengthVerdict = 'za krótka';
        else if (e.length === 'short' && ms > 320) lengthVerdict = 'za długa';
        else lengthVerdict = 'w porządku';
      }

      return {
        index: i,
        label: e.label,
        plain: e.plain,
        expectedTone: e.tone,
        producedTone: got.tone,
        confidence: got.confidence,
        ok: toneOk,
        measured: seg ? {
          startMs: seg.startMs, endMs: seg.endMs,
          durationMs: seg.durationMs, voicedMs: seg.voicedMs,
          voicedFrames: seg.voicedFrames
        } : null,
        userPoints: pts,
        refPoints: refPts,
        expectedLength: e.lengthConfident ? e.length : null,
        lengthVerdict: lengthVerdict,
        lengthRatio: ratio ? Math.round(ratio * 100) / 100 : null,
        fix: toneOk ? '' : ToneScore.fix(got.tone, e.tone)
      };
    });

    /* --- punktacja --- */
    var hits = syllables.filter(function (s) { return s.ok; }).length;
    var toneScore = expected.length ? hits / expected.length : 0;
    var dist = dtw.distance;
    var shapeScore = dist === null ? 0.5 : Math.max(0, Math.min(1, 1 - (dist - 0.35) / 1.5));
    var lengthMisses = syllables.filter(function (s) {
      return s.lengthVerdict && s.lengthVerdict !== 'w porządku';
    }).length;
    var lengthPenalty = Math.min(0.12, lengthMisses * 0.06);

    var score = Math.round(Math.max(0, (toneScore * 0.62 + shapeScore * 0.38 - lengthPenalty)) * 100);
    var grade = score >= 80 ? 'trafnie' : (score >= 60 ? 'blisko' : 'do poprawy');

    /* --- ocena słowna --- */
    var advice = [];
    if (grade === 'trafnie' && !lengthMisses) {
      advice.push('Wszystkie tony w tej wypowiedzi trafione. Powiedz to jeszcze raz w normalnym tempie, żeby się utrwaliło.');
    }
    syllables.forEach(function (s) {
      if (!s.ok && s.fix) advice.push(s.label + ': ' + s.fix);
    });
    syllables.forEach(function (s) {
      if (s.lengthVerdict === 'za krótka') {
        advice.push(s.label + ': samogłoska jest tu długa — przeciągnij ją mniej więcej dwa razy dłużej niż krótką. '
          + 'W tajskim długość odróżnia słowa tak samo jak ton.');
      } else if (s.lengthVerdict === 'za długa') {
        advice.push(s.label + ': samogłoska jest tu krótka — utnij ją wyraźnie, sylaba ma być zwarta.');
      }
    });
    if (grade !== 'trafnie' && dist !== null && dist > 1.1 && hits >= expected.length - 1) {
      advice.push('Tony są rozpoznawalne, ale przebieg jest zbyt płaski — mówisz na jednej wysokości. '
        + 'Przesadź z różnicą między górą a dołem: w tajskim to nie jest emocja, tylko treść.');
    }
    if (analysis.voicedRatio < 0.25) {
      advice.push('Duża część nagrania to cisza albo szum. Zacznij mówić zaraz po wciśnięciu przycisku i nie oddalaj się od mikrofonu.');
    }

    return {
      ok: true,
      empty: false,
      score: score,
      grade: grade,
      hits: hits,
      total: expected.length,
      distance: dist === null ? null : Math.round(dist * 100) / 100,
      dtw: dtw,
      syllables: syllables,
      expected: expected,
      user: user,
      reference: { points: ref.points, syllables: ref.syllables, source: refSource },
      normalisation: {
        centre: user.centre ? Math.round(user.centre) : null,
        halfSpan: Math.round(user.halfSpan * 10) / 10,
        personalised: user.personalised,
        samples: range.samples,
        offset: Math.round(offset * 100) / 100
      },
      advice: advice,
      analysis: analysis
    };
  };

  /* Ocena wymowy jako ocena SM-2. Trafna wymowa podnosi kartę mocniej niż
     rozpoznanie ze słuchu — powiedzenie czegoś poprawnie jest trudniejsze. */
  ToneScore.srsQuality = function (result) {
    if (!result || !result.ok) return null;
    if (result.score >= 85) return 5;
    if (result.score >= 70) return 4;
    if (result.score >= 55) return 3;
    return 2;
  };

  global.ToneScore = ToneScore;
})(window);
