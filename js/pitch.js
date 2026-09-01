/* Thai All-in-One — detekcja wysokości dźwięku (F0).

   Po co to jest
   -------------
   Aplikacja od dawna pozwalała nagrać własny głos, ale nikt tego nagrania nie
   oceniał. Uczący się słyszał wzór, słyszał siebie i musiał sam rozstrzygnąć,
   czy trafił w ton — a właśnie tego początkujący nie potrafi. Bez informacji
   zwrotnej błędny ton utrwala się tak samo skutecznie jak dobry.

   Ten moduł liczy kontur częstotliwości podstawowej nagrania: szereg par
   (czas, herce) plus podział na sylaby wyznaczony z obwiedni energii.
   Wszystko w przeglądarce, offline, bez żadnej biblioteki zewnętrznej.

   Algorytm
   --------
   YIN (de Cheveigné, Kawahara 2002), napisany od zera. W skrócie:

     1. funkcja różnicowa  d(τ) = Σ (x[j] − x[j+τ])²  — szuka przesunięcia,
        przy którym sygnał najlepiej pokrywa się sam ze sobą,
     2. skumulowana średnia znormalizowana d'(τ) — usuwa zafałszowanie na
        rzecz małych τ, przez które zwykła autokorelacja regularnie myli się
        o oktawę w górę,
     3. próg bezwzględny: bierzemy PIERWSZE minimum poniżej progu, nie
        najgłębsze — drugie minimum bywa głębsze i leży oktawę niżej,
     4. interpolacja paraboliczna wokół znalezionego τ — bez niej rozdzielczość
        przy 300 Hz byłaby rzędu 3 %, a różnica między tonem wysokim a średnim
        w mowie bywa mniejsza.

   Cisza, szum i głoski bezdźwięczne
   ---------------------------------
   Ramka bez wyraźnej okresowości nie dostaje F0 równego zeru — dostaje
   wartość null. Zero jest liczbą i wpada na wykres jako gwałtowny spadek do
   dna, czyli jako informacja, której w sygnale nie ma. Dźwięczność
   rozstrzygamy trzema warunkami naraz: energia ramki nad progiem szumu tła
   (liczonym z samego nagrania), aperiodyczność poniżej progu i F0 w zakresie
   ludzkiej mowy. Krótkie „wyspy” dźwięczności krótsze niż 30 ms wycinamy —
   to prawie zawsze trzask albo szum szczelinowy.

   Parametry okna
   --------------
   Analiza idzie po 12 kHz (nagranie jest wcześniej decymowane): przy tej
   częstotliwości najkrótszy okres w zakresie mowy ma 30 próbek, a najdłuższy
   171, więc okno całkowania 30 ms mieści komplet okresów nawet dla głosu
   niskiego. Skok 10 ms daje 100 punktów na sekundę — tyle wystarcza, żeby
   zobaczyć kształt tonu tajskiego, i jest na tyle mało, żeby telefon policzył
   to szybciej, niż trwa samo nagranie. */
(function (global) {
  'use strict';

  var Pitch = {};

  Pitch.PARAMS = {
    rate: 12000,        // częstotliwość analizy po decymacji
    fMin: 70,           // dolna granica głosu ludzkiego (bas)
    fMax: 400,          // górna granica (wysoki głos kobiecy w mowie)
    windowMs: 30,       // okno całkowania funkcji różnicowej
    hopMs: 10,          // skok między ramkami
    threshold: 0.15,    // próg bezwzględny YIN
    voicedMax: 0.45,    // powyżej tej aperiodyczności uznajemy ramkę za bezdźwięczną
    minVoicedMs: 30,    // krótsze wyspy dźwięczności odrzucamy
    minSyllableMs: 90   // krótszych szczytów energii nie uznajemy za sylabę
  };

  Pitch.supported = !!(global.AudioContext || global.webkitAudioContext);

  /* ------------------------------------------------------------ statystyka */

  Pitch.median = function (list) {
    if (!list || !list.length) return null;
    var a = list.slice().sort(function (x, y) { return x - y; });
    var m = Math.floor(a.length / 2);
    return a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2;
  };

  Pitch.percentile = function (list, p) {
    if (!list || !list.length) return null;
    var a = list.slice().sort(function (x, y) { return x - y; });
    var i = (a.length - 1) * p;
    var lo = Math.floor(i), hi = Math.ceil(i);
    if (lo === hi) return a[lo];
    return a[lo] + (a[hi] - a[lo]) * (i - lo);
  };

  /* --------------------------------------------------------- przygotowanie */

  /* Decymacja z filtrem antyaliasingowym. Filtr jest prosty — średnia biegnąca
     o długości współczynnika decymacji — ale to wystarcza: interesuje nas
     przebieg okresowości poniżej 400 Hz, a nie wierność barwy. Bez filtru
     składowe powyżej 6 kHz zawinęłyby się w pasmo analizy i podniosły
     aperiodyczność ramek dźwięcznych. */
  function resample(input, from, to) {
    if (!from || from <= to * 1.02) return { data: input, rate: from };
    var ratio = from / to;
    var win = Math.max(1, Math.round(ratio));
    var outLen = Math.floor(input.length / ratio);
    var out = new Float32Array(outLen);
    for (var i = 0; i < outLen; i++) {
      var centre = i * ratio;
      var start = Math.max(0, Math.round(centre - win / 2));
      var end = Math.min(input.length, start + win);
      var sum = 0;
      for (var j = start; j < end; j++) sum += input[j];
      out[i] = end > start ? sum / (end - start) : 0;
    }
    return { data: out, rate: to };
  }

  /* Usunięcie składowej stałej. Część mikrofonów telefonowych ma wyraźny
     offset, który zawyża energię ciszy i psuje próg szumu. */
  function removeDc(data) {
    var sum = 0, i;
    for (i = 0; i < data.length; i++) sum += data[i];
    var mean = sum / (data.length || 1);
    if (Math.abs(mean) < 1e-6) return data;
    for (i = 0; i < data.length; i++) data[i] -= mean;
    return data;
  }

  /* --------------------------------------------------------------- YIN */

  /* Zwraca { tau, f0, aperiodicity } dla jednej ramki albo null. */
  function yinFrame(data, offset, W, tauMin, tauMax, rate, threshold) {
    var diff = new Float32Array(tauMax + 1);
    var tau, j, delta, sum;

    /* Funkcję różnicową liczymy od τ = 1, choć szukamy dopiero od tauMin.
       Normalizacja skumulowana dzieli d(τ) przez średnią z WSZYSTKICH
       poprzednich τ, więc jeśli zacząć ją dopiero przy tauMin, pierwsze
       wartości dzielą się przez średnią z jednego albo dwóch wyrazów i wychodzą
       zawyżone. Skutek był konkretny: głos powyżej 370 Hz nie mieścił się
       w progu przy prawdziwym okresie i detektor łapał dopiero drugie minimum,
       czyli oktawę niżej. */
    for (tau = 1; tau <= tauMax; tau++) {
      sum = 0;
      for (j = 0; j < W; j++) {
        delta = data[offset + j] - data[offset + j + tau];
        sum += delta * delta;
      }
      diff[tau] = sum;
    }

    /* Skumulowana średnia znormalizowana. Wartość 1 oznacza „nic
       szczególnego”, wartości bliskie 0 — wyraźną okresowość. */
    var cmnd = new Float32Array(tauMax + 1);
    var running = 0;
    cmnd[0] = 1;
    for (tau = 1; tau <= tauMax; tau++) {
      running += diff[tau];
      cmnd[tau] = running > 0 ? diff[tau] * tau / running : 1;
    }

    /* Pierwsze minimum poniżej progu — nie najgłębsze w całym zakresie.
       Najgłębsze bywa wielokrotnością okresu, co daje błąd oktawowy w dół. */
    var best = -1;
    for (tau = tauMin; tau <= tauMax; tau++) {
      if (cmnd[tau] < threshold) {
        while (tau + 1 <= tauMax && cmnd[tau + 1] < cmnd[tau]) tau++;
        best = tau;
        break;
      }
    }
    if (best < 0) {
      /* Bez trafienia w próg bierzemy globalne minimum i zwracamy je razem
         z jego aperiodycznością — o dźwięczności rozstrzygnie warstwa wyżej. */
      var min = Infinity;
      for (tau = tauMin; tau <= tauMax; tau++) {
        if (cmnd[tau] < min) { min = cmnd[tau]; best = tau; }
      }
      if (best < 0) return null;
    }

    /* Interpolacja paraboliczna przez trzy sąsiednie punkty. */
    var t = best;
    var refined = t;
    if (t > tauMin && t < tauMax) {
      var a = cmnd[t - 1], b = cmnd[t], c = cmnd[t + 1];
      var denom = 2 * (2 * b - a - c);
      if (Math.abs(denom) > 1e-9) refined = t + (c - a) / denom;
    }
    if (refined <= 0) return null;

    return { tau: refined, f0: rate / refined, aperiodicity: cmnd[best] };
  }

  /* ------------------------------------------------------- korekty konturu */

  /* Skok o oktawę to najczęstsza pomyłka każdego detektora F0. Poprawiamy ją
     względem mediany otoczenia: jeśli ramka leży dwa razy wyżej albo dwa razy
     niżej niż sąsiedztwo, mnożymy ją przez 0,5 lub 2. */
  function fixOctaves(frames) {
    var i, k, near, ref;
    for (i = 0; i < frames.length; i++) {
      if (!frames[i].voiced) continue;
      near = [];
      for (k = Math.max(0, i - 4); k <= Math.min(frames.length - 1, i + 4); k++) {
        if (k !== i && frames[k].voiced) near.push(frames[k].f0);
      }
      if (near.length < 3) continue;
      ref = Pitch.median(near);
      if (!ref) continue;
      var r = frames[i].f0 / ref;
      if (r > 1.75 && r < 2.3) frames[i].f0 /= 2;
      else if (r > 0.42 && r < 0.58) frames[i].f0 *= 2;
    }
  }

  /* Mediana ruchoma po ramkach dźwięcznych — wygładza pojedyncze wyskoki,
     nie rozmywając prawdziwych zmian tonu (średnia by je rozmyła). */
  function medianSmooth(frames, span) {
    var out = frames.map(function (f) { return f.f0; });
    var half = Math.floor(span / 2);
    for (var i = 0; i < frames.length; i++) {
      if (!frames[i].voiced) continue;
      var box = [];
      for (var k = Math.max(0, i - half); k <= Math.min(frames.length - 1, i + half); k++) {
        if (frames[k].voiced) box.push(frames[k].f0);
      }
      if (box.length >= 3) out[i] = Pitch.median(box);
    }
    for (var j = 0; j < frames.length; j++) {
      if (frames[j].voiced) frames[j].f0 = out[j];
    }
  }

  /* Krótkie wyspy dźwięczności są prawie zawsze artefaktem: trzask klawisza,
     szum szczelinowy, przydech. Zbyt krótkie przerwy w środku dźwięcznego
     odcinka domykamy — to zwykle zwarcie krtaniowe albo spółgłoska zwarta. */
  function tidyVoicing(frames, hopMs, minMs) {
    var minLen = Math.max(1, Math.round(minMs / hopMs));
    var i, j;
    for (i = 0; i < frames.length; i++) {
      if (!frames[i].voiced) continue;
      j = i;
      while (j + 1 < frames.length && frames[j + 1].voiced) j++;
      if (j - i + 1 < minLen) {
        for (var k = i; k <= j; k++) { frames[k].voiced = false; frames[k].f0 = null; }
      }
      i = j;
    }
    /* Domykanie luk: maksymalnie dwie ramki (20 ms). */
    for (i = 1; i < frames.length - 1; i++) {
      if (frames[i].voiced) continue;
      var prev = frames[i - 1].voiced ? frames[i - 1] : null;
      var nxt = null;
      for (j = i + 1; j <= Math.min(frames.length - 1, i + 2); j++) {
        if (frames[j].voiced) { nxt = frames[j]; break; }
      }
      if (prev && nxt) {
        var steps = j - (i - 1);
        for (var m = i; m < j; m++) {
          var w = (m - (i - 1)) / steps;
          frames[m].voiced = true;
          frames[m].f0 = prev.f0 * (1 - w) + nxt.f0 * w;
          frames[m].filled = true;
        }
      }
    }
  }

  /* ----------------------------------------------------- granice sylab */

  /* Sylaby wyznaczamy z obwiedni energii, nie z F0: w tajskim sylaba bywa
     w całości dźwięczna albo zaczyna się spółgłoską bezdźwięczną, więc sam
     kontur nie wystarcza. Szukamy szczytów energii oddalonych od siebie
     o co najmniej 90 ms i wyraźnie wyższych niż dolina między nimi. */
  function findSyllables(frames, hopMs, minMs, prominence) {
    prominence = prominence === undefined ? 4 : prominence;
    var db = frames.map(function (f) { return f.db; });
    if (!db.length) return [];

    /* Wygładzenie obwiedni oknem 50 ms — bez niego każde drgnięcie amplitudy
       w środku samogłoski udaje osobny szczyt. */
    var span = Math.max(1, Math.round(50 / hopMs));
    var half = Math.floor(span / 2);
    var smooth = db.map(function (_, i) {
      var sum = 0, n = 0;
      for (var k = Math.max(0, i - half); k <= Math.min(db.length - 1, i + half); k++) {
        sum += db[k]; n++;
      }
      return sum / n;
    });

    var maxDb = Math.max.apply(null, smooth);
    var floor = maxDb - 28;                 // 28 dB poniżej szczytu to już tło
    var minDist = Math.max(2, Math.round(minMs / hopMs));

    /* 1. kandydaci na szczyty */
    var peaks = [];
    for (var i = 1; i < smooth.length - 1; i++) {
      if (smooth[i] < floor) continue;
      if (smooth[i] >= smooth[i - 1] && smooth[i] > smooth[i + 1]) peaks.push(i);
    }
    if (!peaks.length) {
      var top = 0;
      for (var t = 0; t < smooth.length; t++) if (smooth[t] > smooth[top]) top = t;
      peaks = [top];
    }

    /* 2. łączenie szczytów, między którymi nie ma prawdziwej doliny.
       Warunek: dolina musi zejść co najmniej 4 dB poniżej niższego ze szczytów
       i szczyty muszą dzielić minimum 90 ms — inaczej to jedna sylaba. */
    var merged = [peaks[0]];
    for (var p = 1; p < peaks.length; p++) {
      var prev = merged[merged.length - 1], cur = peaks[p];
      var valley = Infinity;
      for (var v = prev; v <= cur; v++) valley = Math.min(valley, smooth[v]);
      var lower = Math.min(smooth[prev], smooth[cur]);
      if (cur - prev < minDist || lower - valley < prominence) {
        if (smooth[cur] > smooth[prev]) merged[merged.length - 1] = cur;
      } else {
        merged.push(cur);
      }
    }

    /* 3. granice: najgłębsza dolina między sąsiednimi szczytami, a na skrajach
       miejsce, w którym energia schodzi 12 dB poniżej szczytu. */
    var bounds = [];
    for (var s = 0; s < merged.length; s++) {
      var peak = merged[s];
      var startLimit = s === 0 ? 0 : bounds[s - 1].end;
      var start, end, x;

      if (s === 0) {
        start = 0;
        for (x = peak; x >= 0; x--) {
          if (smooth[x] < smooth[peak] - 12 || smooth[x] < floor) { start = x; break; }
        }
      } else {
        start = startLimit;
      }

      if (s === merged.length - 1) {
        end = smooth.length - 1;
        for (x = peak; x < smooth.length; x++) {
          if (smooth[x] < smooth[peak] - 12 || smooth[x] < floor) { end = x; break; }
        }
      } else {
        var nextPeak = merged[s + 1];
        var lowest = peak;
        for (x = peak; x <= nextPeak; x++) if (smooth[x] < smooth[lowest]) lowest = x;
        end = lowest;
      }
      if (end <= start) end = Math.min(smooth.length - 1, start + 1);
      bounds.push({ start: start, end: end, peak: peak });
    }

    /* 4. odcinki bez jądra dźwięcznego nie są sylabami. Szum szczelinowy /s/
       albo przydech na początku wypowiedzi tworzy własny szczyt energii, ale
       należy do sylaby, która po nim następuje — po tajsku sylaba zawsze ma
       jądro samogłoskowe, więc odcinek bez ramek dźwięcznych doklejamy do
       sąsiada: najpierw do następnego (nagłos), a jeśli go nie ma — do
       poprzedniego (wygłos). */
    function voicedIn(b) {
      var n = 0;
      for (var i3 = b.start; i3 <= b.end; i3++) if (frames[i3].voiced) n++;
      return n;
    }
    var kept = [];
    for (var q = 0; q < bounds.length; q++) {
      if (voicedIn(bounds[q]) >= 2) { kept.push(bounds[q]); continue; }
      var after = null;
      for (var w2 = q + 1; w2 < bounds.length; w2++) {
        if (voicedIn(bounds[w2]) >= 2) { after = bounds[w2]; break; }
      }
      if (after) after.start = Math.min(after.start, bounds[q].start);
      else if (kept.length) kept[kept.length - 1].end = Math.max(kept[kept.length - 1].end, bounds[q].end);
      else kept.push(bounds[q]);
    }
    if (!kept.length) kept = bounds;

    return kept.map(function (b) { return describe(frames, b, smooth); });
  }

  /* Wspólny opis odcinka — używany zarówno przy pierwszym podziale, jak i po
     wymuszeniu liczby sylab. */
  function describe(frames, b, smooth) {
    var pts = [];
    for (var i = b.start; i <= b.end; i++) {
      if (frames[i].voiced) pts.push({ t: frames[i].t, f: frames[i].f0 });
    }
    /* Długość samogłoski mierzymy na jądrze dźwięcznym, nie na całym odcinku.
       Odcinek zawiera także nagłos bezdźwięczny (/s/, /kh/, przydech), a to
       nie jest samogłoska — wliczanie go zamieniłoby każdą sylabę zaczynającą
       się od spółgłoski szczelinowej w „za długą”. */
    var nucleusMs = pts.length
      ? Math.round((pts[pts.length - 1].t - pts[0].t) * 1000) + (frames[1] ? Math.round((frames[1].t - frames[0].t) * 1000) : 10)
      : 0;
    return {
      startMs: Math.round(frames[b.start].t * 1000),
      endMs: Math.round(frames[b.end].t * 1000),
      durationMs: Math.round((frames[b.end].t - frames[b.start].t) * 1000),
      voicedMs: nucleusMs,
      peakDb: smooth ? Math.round(smooth[b.peak !== undefined ? b.peak : b.start] * 10) / 10 : null,
      points: pts,
      voicedFrames: pts.length,
      startFrame: b.start,
      endFrame: b.end
    };
  }

  /* Podział na z góry znaną liczbę sylab.

     Zapis fonetyczny mówi, ile sylab POWINNO być — i to jest informacja, której
     szkoda nie wykorzystać. Zamiast przyjmować pierwszy podział, jaki wyjdzie
     z obwiedni, próbujemy kilku progów wyrazistości szczytu i wybieramy ten,
     który daje właściwą liczbę. Dopiero gdy żaden nie trafi, dzielimy odcinek
     najdłuższy albo scalamy parę o najpłytszej dolinie — bo lepiej porównać
     sylaba w sylabę z drobnym błędem granicy niż przesunąć całe porównanie
     o jedną pozycję. */
  Pitch.segment = function (analysis, wanted) {
    var frames = analysis.frames;
    if (!frames || !frames.length) return [];
    var hop = analysis.hopMs || Pitch.PARAMS.hopMs;
    var min = Pitch.PARAMS.minSyllableMs;
    if (!wanted || wanted < 1) return analysis.syllables;

    var tries = [4, 3, 2.5, 2, 5, 6, 8, 1.5];
    var best = null;
    for (var i = 0; i < tries.length; i++) {
      var got = findSyllables(frames, hop, min, tries[i]);
      if (got.length === wanted) return got;
      if (!best || Math.abs(got.length - wanted) < Math.abs(best.length - wanted)) best = got;
    }
    var out = (best || []).slice();

    /* Za mało: dzielimy najdłuższy odcinek w jego wewnętrznym minimum energii. */
    var guard = 0;
    while (out.length && out.length < wanted && guard++ < 12) {
      var longest = 0;
      for (var k = 1; k < out.length; k++) {
        if (out[k].durationMs > out[longest].durationMs) longest = k;
      }
      var seg = out[longest];
      var a = seg.startFrame, b = seg.endFrame;
      if (b - a < 4) break;
      var cut = a + Math.round((b - a) / 2);
      var lowest = cut;
      for (var x = a + 2; x <= b - 2; x++) {
        if (frames[x].db < frames[lowest].db) lowest = x;
      }
      if (lowest > a + 1 && lowest < b - 1) cut = lowest;
      out.splice(longest, 1,
        describe(frames, { start: a, end: cut }, null),
        describe(frames, { start: cut, end: b }, null));
    }

    /* Za dużo: scalamy sąsiadów o najmniejszej różnicy energii na granicy. */
    guard = 0;
    while (out.length > wanted && out.length > 1 && guard++ < 12) {
      var pick = 0, bestGap = Infinity;
      for (var m = 0; m + 1 < out.length; m++) {
        var gap = Math.abs((out[m].peakDb || 0) - (out[m + 1].peakDb || 0))
          + (out[m + 1].startMs - out[m].endMs) / 10;
        if (gap < bestGap) { bestGap = gap; pick = m; }
      }
      var merged = describe(frames,
        { start: out[pick].startFrame, end: out[pick + 1].endFrame }, null);
      out.splice(pick, 2, merged);
    }
    return out;
  };

  /* ------------------------------------------------------------- analiza */

  /* samples: Float32Array (jeden kanał), rate: częstotliwość próbkowania.
     Zwraca komplet danych potrzebnych do oceny i do wykresu. */
  Pitch.analyse = function (samples, rate, opts) {
    opts = opts || {};
    var P = Pitch.PARAMS;
    var t0 = (global.performance && performance.now) ? performance.now() : Date.now();

    if (!samples || !samples.length || !rate) {
      return emptyResult(0, 0);
    }

    var down = resample(samples, rate, opts.rate || P.rate);
    var data = removeDc(down.data.slice ? down.data.slice(0) : down.data);
    var r = down.rate;

    var W = Math.round((opts.windowMs || P.windowMs) * r / 1000);
    var hop = Math.round((opts.hopMs || P.hopMs) * r / 1000);
    var tauMin = Math.max(2, Math.floor(r / (opts.fMax || P.fMax)));
    var tauMax = Math.min(Math.ceil(r / (opts.fMin || P.fMin)), W);
    var frameLen = W + tauMax;
    var duration = samples.length / rate;

    if (data.length < frameLen + hop) {
      return emptyResult(duration, (global.performance && performance.now ? performance.now() : Date.now()) - t0);
    }

    /* 1. energia wszystkich ramek — potrzebna do progu szumu, zanim
       zaczniemy rozstrzygać o dźwięczności. */
    var frames = [];
    var offset = 0, i;
    while (offset + frameLen < data.length) {
      var sum = 0;
      for (i = 0; i < W; i++) sum += data[offset + i] * data[offset + i];
      var rms = Math.sqrt(sum / W);
      frames.push({
        t: (offset + W / 2) / r,
        rms: rms,
        db: 20 * Math.log10(rms + 1e-9),
        f0: null,
        voiced: false,
        aperiodicity: 1,
        offset: offset
      });
      offset += hop;
    }
    if (!frames.length) {
      return emptyResult(duration, (global.performance && performance.now ? performance.now() : Date.now()) - t0);
    }

    /* 2. próg szumu z samego nagrania. Percentyl 15 opisuje tło (pauzy,
       szum mikrofonu), a nie mowę — nawet w nagraniu bez wyraźnej ciszy. */
    var rmsList = frames.map(function (f) { return f.rms; });
    var quiet = Pitch.percentile(rmsList, 0.15) || 0;
    var loud = Pitch.percentile(rmsList, 0.95) || 0;
    /* Próg musi zostać wyraźnie poniżej poziomu mowy, także wtedy, gdy
       w nagraniu w ogóle nie ma ciszy (materiał kontrolny, zdanie bez pauz).
       Bez górnego ograniczenia percentyl 15 zrównałby się z poziomem mowy
       i próg wyciąłby całe nagranie. */
    var noiseFloor = Math.min(Math.max(quiet * 2.5, loud * 0.05), loud * 0.25);
    noiseFloor = Math.max(noiseFloor, 1e-4);

    /* 3. YIN tylko dla ramek z energią — liczenie funkcji różnicowej dla
       ciszy to czysta strata czasu procesora. */
    for (i = 0; i < frames.length; i++) {
      var f = frames[i];
      if (f.rms < noiseFloor) continue;
      var res = yinFrame(data, f.offset, W, tauMin, tauMax, r, opts.threshold || P.threshold);
      if (!res) continue;
      f.aperiodicity = res.aperiodicity;
      if (res.aperiodicity <= (opts.voicedMax || P.voicedMax)
          && res.f0 >= (opts.fMin || P.fMin) && res.f0 <= (opts.fMax || P.fMax)) {
        f.f0 = res.f0;
        f.voiced = true;
      }
    }

    fixOctaves(frames);
    medianSmooth(frames, 5);
    tidyVoicing(frames, (opts.hopMs || P.hopMs), opts.minVoicedMs || P.minVoicedMs);

    var voiced = frames.filter(function (x) { return x.voiced; });
    var points = voiced.map(function (x) {
      return { t: Math.round(x.t * 1000) / 1000, f: Math.round(x.f0 * 10) / 10 };
    });

    var syllables = findSyllables(frames, (opts.hopMs || P.hopMs), opts.minSyllableMs || P.minSyllableMs);
    var f0List = voiced.map(function (x) { return x.f0; });
    var t1 = (global.performance && performance.now) ? performance.now() : Date.now();

    return {
      sampleRate: rate,
      analysisRate: r,
      duration: duration,
      hopMs: (opts.hopMs || P.hopMs),
      frames: frames.map(function (x) {
        return { t: x.t, f0: x.voiced ? x.f0 : null, db: x.db, voiced: x.voiced };
      }),
      points: points,
      syllables: syllables,
      voicedRatio: frames.length ? voiced.length / frames.length : 0,
      noiseFloor: noiseFloor,
      medianF0: Pitch.median(f0List),
      p10: Pitch.percentile(f0List, 0.10),
      p90: Pitch.percentile(f0List, 0.90),
      analysisMs: Math.round(t1 - t0)
    };
  };

  function emptyResult(duration, ms) {
    return {
      sampleRate: 0, analysisRate: 0, duration: duration || 0, hopMs: Pitch.PARAMS.hopMs,
      frames: [], points: [], syllables: [], voicedRatio: 0, noiseFloor: 0,
      medianF0: null, p10: null, p90: null, analysisMs: Math.round(ms || 0)
    };
  }

  /* --------------------------------------------------------- wejście audio */

  var ctx = null;

  function audioContext() {
    if (ctx) return ctx;
    var C = global.AudioContext || global.webkitAudioContext;
    if (!C) return null;
    ctx = new C();
    return ctx;
  }

  /* Zamienia dowolny obiekt AudioBuffer na jeden kanał (średnia kanałów). */
  Pitch.mono = function (buffer) {
    if (buffer.numberOfChannels === 1) return buffer.getChannelData(0);
    var len = buffer.length;
    var out = new Float32Array(len);
    for (var c = 0; c < buffer.numberOfChannels; c++) {
      var ch = buffer.getChannelData(c);
      for (var i = 0; i < len; i++) out[i] += ch[i] / buffer.numberOfChannels;
    }
    return out;
  };

  /* Dekodowanie nagrania z MediaRecorder. Działa też w trybie file://, bo
     decodeAudioData dostaje gotowy ArrayBuffer, a nie adres do pobrania. */
  Pitch.fromBlob = function (blob) {
    var ac = audioContext();
    if (!ac) return Promise.reject(new Error('Ta przeglądarka nie obsługuje Web Audio API.'));
    return blob.arrayBuffer().then(function (buf) {
      return new Promise(function (resolve, reject) {
        var done = false;
        var ok = function (decoded) { if (!done) { done = true; resolve(decoded); } };
        var fail = function (e) { if (!done) { done = true; reject(e || new Error('Nie udało się odczytać nagrania.')); } };
        var p = ac.decodeAudioData(buf, ok, fail);
        if (p && p.then) p.then(ok)['catch'](fail);
      });
    }).then(function (buffer) {
      return Pitch.analyseAsync(Pitch.mono(buffer), buffer.sampleRate);
    });
  };

  /* Analiza pliku z katalogu audio/ — używana wtedy, gdy hasło ma nagranie
     lektora i można z niego wyliczyć prawdziwy kontur wzorcowy. */
  Pitch.fromUrl = function (url) {
    var ac = audioContext();
    if (!ac) return Promise.reject(new Error('Ta przeglądarka nie obsługuje Web Audio API.'));
    return fetch(url).then(function (res) {
      if (!res.ok) throw new Error('Nie znaleziono nagrania wzorcowego.');
      return res.arrayBuffer();
    }).then(function (buf) {
      return new Promise(function (resolve, reject) {
        var p = ac.decodeAudioData(buf, resolve, reject);
        if (p && p.then) p.then(resolve)['catch'](reject);
      });
    }).then(function (buffer) {
      return Pitch.analyseAsync(Pitch.mono(buffer), buffer.sampleRate);
    });
  };

  /* Sygnał kontrolny: ton o znanej częstotliwości z lekkim vibrato i szumem.
     Służy testom (tools/function-test.py) do sprawdzenia, czy detektor nadal
     trafia w częstotliwość, oraz pomiarowi czasu analizy. */
  Pitch.testSignal = function (hz, seconds, rate, noise) {
    rate = rate || 44100;
    seconds = seconds || 1;
    noise = noise === undefined ? 0.01 : noise;
    var n = Math.round(rate * seconds);
    var out = new Float32Array(n);
    var phase = 0;
    for (var i = 0; i < n; i++) {
      var f = hz * (1 + 0.004 * Math.sin(2 * Math.PI * 4 * i / rate));  // lekkie vibrato
      phase += 2 * Math.PI * f / rate;
      /* Trzy harmoniczne — czysta sinusoida jest dla detektora F0 zadaniem
         łatwiejszym niż głos, więc test na niej niczego by nie dowodził. */
      out[i] = 0.6 * Math.sin(phase) + 0.25 * Math.sin(2 * phase) + 0.12 * Math.sin(3 * phase);
      if (noise) out[i] += (Math.random() * 2 - 1) * noise;
    }
    return out;
  };

  /* ================== ANALIZA POZA WĄTKIEM GŁÓWNYM ======================

     Pitch.analyse na nagraniu 3 s przy dławieniu x4 liczyła się 166 ms.
     Przez ten czas wątek główny nie obsługiwał niczego: interfejs stał
     w miejscu dokładnie w chwili, w której uczący się czeka na ocenę
     wymowy. Sama analiza nie dotyka DOM ani Web Audio — to czysta
     arytmetyka na tablicy próbek — więc nadaje się do wątku roboczego
     bez żadnych ustępstw.

     Wątek roboczy nie zawsze jest dostępny: w trybie file:// przeglądarki
     odmawiają jego utworzenia (origin „null”), starsze przeglądarki nie
     mają go wcale. Dlatego analyseAsync ZAWSZE zwraca obietnicę, a to,
     czy policzył ją wątek roboczy, czy główny, jest szczegółem — widocznym
     w Pitch.lastRunOn, żeby dało się to sprawdzić testem. */

  var worker = null;
  var workerBroken = false;
  var nextId = 1;
  var pending = {};

  Pitch.WORKER_URL = 'js/pitch-worker.js';

  /* Wymuszenie ścieżki zapasowej — używane przez test i przez tryb file://. */
  Pitch.forceMainThread = false;

  /* Na czym policzyła się OSTATNIA analiza: 'worker' albo 'main'. */
  Pitch.lastRunOn = null;

  function workerUrl() {
    /* Adres liczymy względem pliku pitch.js, a nie względem dokumentu —
       aplikacja bywa serwowana z podkatalogu i ścieżka względna dokumentu
       trafiałaby wtedy w próżnię. */
    try {
      if (global.document && document.currentScript && document.currentScript.src) {
        return new URL('pitch-worker.js', document.currentScript.src).href;
      }
      var tags = global.document ? document.getElementsByTagName('script') : [];
      for (var i = 0; i < tags.length; i++) {
        if (tags[i].src && tags[i].src.indexOf('pitch.js') !== -1) {
          return new URL('pitch-worker.js', tags[i].src).href;
        }
      }
    } catch (e) { /* zostaje ścieżka domyślna */ }
    return Pitch.WORKER_URL;
  }

  function ensureWorker() {
    if (Pitch.forceMainThread || workerBroken) return null;
    if (worker) return worker;
    if (typeof global.Worker !== 'function') { workerBroken = true; return null; }
    try {
      worker = new global.Worker(workerUrl());
    } catch (e) {
      /* file:// — przeglądarka nie pozwala utworzyć wątku roboczego. */
      workerBroken = true;
      worker = null;
      return null;
    }
    worker.onmessage = function (ev) {
      var d = ev.data || {};
      var slot = pending[d.id];
      if (!slot) return;
      delete pending[d.id];
      if (d.ok) slot.resolve(d.result);
      else slot.reject(new Error(d.error || 'Analiza w wątku roboczym nie powiodła się.'));
    };
    worker.onerror = function () {
      /* Awaria wątku nie może zabrać ze sobą oceny wymowy: przełączamy się
         na wątek główny i domykamy wszystko, co czekało. */
      workerBroken = true;
      var stuck = pending;
      pending = {};
      Object.keys(stuck).forEach(function (id) {
        var slot = stuck[id];
        try {
          Pitch.lastRunOn = 'main';
          slot.resolve(Pitch.analyse(slot.samples, slot.rate, slot.opts));
        } catch (e) { slot.reject(e); }
      });
      try { worker.terminate(); } catch (e) {}
      worker = null;
    };
    return worker;
  }

  Pitch.workerReady = function () { return !!ensureWorker(); };

  /* Zamyka wątek roboczy i zapomina, że próba się nie udała. Potrzebne
     testowi ścieżki zapasowej (raz utworzony wątek żyje do końca strony,
     więc bez tego nie dałoby się sprawdzić zachowania bez Workera) oraz
     przy zwalnianiu zasobów po wyjściu z ekranu wymowy. */
  Pitch.resetWorker = function () {
    if (worker) { try { worker.terminate(); } catch (e) {} }
    worker = null;
    workerBroken = false;
    pending = {};
  };

  Pitch.analyseAsync = function (samples, rate, opts) {
    var w = ensureWorker();
    if (!w) {
      /* Ścieżka zapasowa: liczymy tu, ale interfejs dostaje obietnicę,
         więc wywołujący ma JEDNĄ ścieżkę kodu niezależnie od środowiska. */
      Pitch.lastRunOn = 'main';
      try {
        return Promise.resolve(Pitch.analyse(samples, rate, opts));
      } catch (e) {
        return Promise.reject(e);
      }
    }
    var id = nextId++;
    return new Promise(function (resolve, reject) {
      pending[id] = { resolve: resolve, reject: reject,
                      samples: samples, rate: rate, opts: opts };
      /* Kopia próbek idzie przekazaniem własności (bez kopiowania przez
         strukturę), a oryginał zostaje nietknięty u wywołującego — kontur
         wzorcowy bywa porównywany z tym samym buforem po analizie. */
      var copy = (samples && samples.slice) ? samples.slice(0) : samples;
      Pitch.lastRunOn = 'worker';
      try {
        w.postMessage({ cmd: 'analyse', id: id, samples: copy,
                        rate: rate, opts: opts || null },
                      copy && copy.buffer ? [copy.buffer] : []);
      } catch (e) {
        delete pending[id];
        Pitch.lastRunOn = 'main';
        resolve(Pitch.analyse(samples, rate, opts));
      }
    });
  };

  global.Pitch = Pitch;
  /* `window` w karcie, `self` w wątku roboczym — bez tego importScripts
     w pitch-worker.js wywracałby się na nieznanej nazwie. */
})(typeof self !== 'undefined' ? self : this);
