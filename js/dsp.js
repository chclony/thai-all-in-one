/* Thai All-in-One — przetwarzanie dźwięku (Web Audio).

   Ten moduł nie wie nic o tajskim ani o nauce. Robi cztery rzeczy:

     1. rozciąga i skraca dźwięk w czasie BEZ zmiany wysokości (WSOLA),
     2. generuje szum tła trzech rodzajów — restauracja, ulica, dworzec,
     3. generuje syntetyczne odpowiedzi impulsowe do pogłosu (splot),
     4. filtruje pasmo tak, jak robi to łącze telefoniczne.

   Plus piąta rzecz, bez której reszta jest za wolna: pamięć podręczna
   gotowych buforów z eksmisją najdawniej używanego (LRU).

   DLACZEGO WSOLA, A NIE playbackRate
   ----------------------------------
   Zmiana playbackRate przesuwa całe widmo: wolniej znaczy niżej. W języku
   tonalnym to katastrofa — kontur tonalny JEST znaczeniem, a nie ozdobą.
   Zdanie odtworzone przy 0,7 miałoby wszystkie tony obniżone o pięć półtonów
   i uczący się trenowałby na materiale, którego nikt nigdy nie powiedział.

   WSOLA (Waveform Similarity Overlap-Add) tnie sygnał na zachodzące na siebie
   okna i skleja je z innym krokiem, niż zostały wycięte. Kluczowy jest wybór
   miejsca sklejenia: zanim doklei kolejne okno, algorytm przeszukuje otoczenie
   punktu wycięcia i wybiera przesunięcie, przy którym nowe okno najlepiej
   pasuje falowo do tego, co już leży w buforze. Dzięki temu okresy krtaniowe
   trafiają na siebie, a nie w poprzek — częstotliwość podstawowa zostaje
   nietknięta, zmienia się wyłącznie czas.

   Wszystko liczone jest w przeglądarce, bez żadnej biblioteki. Funkcje
   operujące na Float32Array są czyste (nie dotykają AudioContext), więc dają
   się przetestować także poza przeglądarką. */
(function (global) {
  'use strict';

  var DSP = {
    /* Parametry WSOLA. Okno 46 ms przy 44,1 kHz to kompromis: krótsze rozmywa
       niskie głosy męskie, dłuższe rozmazuje szybkie przejścia spółgłoskowe. */
    FRAME: 2048,
    HOP: 1024,          // krok syntezy = pół okna, okno Hanna sumuje się do 1
    SEARCH: 384,        // ile próbek w tył i w przód szukamy dopasowania
    CORR_STEP: 2        // co drugą próbkę — dwa razy szybciej, wynik ten sam
  };

  /* ------------------------------------------------------------ kontekst */

  var ctx = null;

  DSP.supported = function () {
    return !!(global.AudioContext || global.webkitAudioContext);
  };

  DSP.context = function () {
    if (ctx) return ctx;
    var C = global.AudioContext || global.webkitAudioContext;
    if (!C) return null;
    ctx = new C();
    return ctx;
  };

  /* Przeglądarki mobilne trzymają kontekst uśpiony do pierwszego gestu. */
  DSP.resume = function () {
    var c = DSP.context();
    if (c && c.state === 'suspended' && c.resume) {
      try { c.resume(); } catch (e) {}
    }
    return c;
  };

  /* ------------------------------------------------- rozciąganie w czasie */

  function hann(n) {
    var w = new Float32Array(n);
    for (var i = 0; i < n; i++) w[i] = 0.5 - 0.5 * Math.cos(2 * Math.PI * i / n);
    return w;
  }

  var windowCache = {};
  function windowOf(n) {
    if (!windowCache[n]) windowCache[n] = hann(n);
    return windowCache[n];
  }

  /* Najlepsze przesunięcie sklejenia: maksimum znormalizowanej korelacji
     między ogonem tego, co już zsyntetyzowane, a kandydatem na nowe okno. */
  function bestOffset(input, guess, tailRef, tailLen, search, step) {
    var best = 0, bestScore = -Infinity;
    var lo = Math.max(-search, -guess);
    var hi = Math.min(search, input.length - guess - tailLen - 1);
    for (var off = lo; off <= hi; off += step) {
      var sum = 0, energy = 0;
      var base = guess + off;
      for (var i = 0; i < tailLen; i += step) {
        var v = input[base + i];
        sum += tailRef[i] * v;
        energy += v * v;
      }
      /* Normalizacja przez energię kandydata — bez niej algorytm zawsze
         wybierałby najgłośniejszy fragment zamiast najlepiej pasującego. */
      var score = energy > 1e-9 ? sum / Math.sqrt(energy) : 0;
      if (score > bestScore) { bestScore = score; best = off; }
    }
    return best;
  }

  /* factor > 1 skraca (mowa szybsza), factor < 1 wydłuża (mowa wolniejsza).
     Wysokość dźwięku nie zmienia się w żadnym przypadku. */
  DSP.stretchChannel = function (input, factor) {
    if (!input || !input.length) return new Float32Array(0);
    if (Math.abs(factor - 1) < 1e-3) return input.slice();

    var N = DSP.FRAME, Hs = DSP.HOP;
    var Ha = Math.max(1, Math.round(Hs * factor));
    var win = windowOf(N);
    var outLen = Math.ceil(input.length / factor) + N;
    var out = new Float32Array(outLen);
    var norm = new Float32Array(outLen);

    var tailLen = Math.min(Hs, N >> 1);
    var tailRef = new Float32Array(tailLen);

    /* Pozycja analizy liczona jest z numeru ramki, a nie doliczana krok po
       kroku. To nie kosmetyka: przesunięcie sklejenia potrafi mieć niezerową
       średnią, a doliczane do pozycji kumulowałoby się przez sto kilkadziesiąt
       ramek i wynik wychodził o ponad ćwierć za krótki. Przesunięcie ma
       poprawiać MIEJSCE sklejenia, nie tempo. */
    var frame = 0, writePos = 0;
    var limit = input.length - N - DSP.SEARCH - 1;
    while (writePos + N < outLen) {
      var readPos = Math.round(frame * Ha);
      if (readPos > limit) break;
      var offset = 0;
      if (frame > 0) {
        /* Wzorzec: to, co już leży w buforze wyjściowym w miejscu sklejenia. */
        for (var t = 0; t < tailLen; t++) {
          var d = norm[writePos + t];
          tailRef[t] = d > 1e-6 ? out[writePos + t] / d : 0;
        }
        offset = bestOffset(input, readPos, tailRef, tailLen, DSP.SEARCH, DSP.CORR_STEP);
      }
      frame++;
      var src = readPos + offset;
      if (src < 0) src = 0;
      if (src + N >= input.length) src = input.length - N - 1;
      if (src < 0) break;

      for (var i = 0; i < N; i++) {
        var w = win[i];
        out[writePos + i] += input[src + i] * w;
        norm[writePos + i] += w;
      }
      writePos += Hs;
    }

    var end = Math.min(writePos + N, outLen);
    for (var k = 0; k < end; k++) {
      if (norm[k] > 1e-6) out[k] /= norm[k];
    }
    return out.subarray(0, end);
  };

  DSP.stretchBuffer = function (buffer, factor) {
    var c = DSP.context();
    if (!c || !buffer) return buffer;
    if (Math.abs(factor - 1) < 1e-3) return buffer;
    var chans = [];
    var len = 0;
    for (var ch = 0; ch < buffer.numberOfChannels; ch++) {
      var s = DSP.stretchChannel(buffer.getChannelData(ch), factor);
      chans.push(s);
      len = Math.max(len, s.length);
    }
    var out = c.createBuffer(buffer.numberOfChannels, len, buffer.sampleRate);
    for (var j = 0; j < chans.length; j++) out.getChannelData(j).set(chans[j]);
    return out;
  };

  /* --------------------------------------------------------- szum tła */

  /* Powtarzalny generator liczb losowych. Ten sam poziom trudności ma dawać
     ten sam szum — inaczej dwa podejścia do tego samego zadania nie dałyby
     się porównać, a to jest ćwiczenie, nie tapeta. */
  function rng(seed) {
    var s = seed >>> 0 || 1;
    return function () {
      s ^= s << 13; s >>>= 0;
      s ^= s >> 17;
      s ^= s << 5; s >>>= 0;
      return s / 4294967296;
    };
  }

  function whiteInto(data, rand, gain) {
    for (var i = 0; i < data.length; i++) data[i] += (rand() * 2 - 1) * gain;
  }

  /* Jednobiegunowy filtr dolnoprzepustowy — tani i wystarczający do szumu. */
  function lowpass(data, sr, cutoff) {
    var a = Math.exp(-2 * Math.PI * cutoff / sr);
    var z = 0;
    for (var i = 0; i < data.length; i++) {
      z = data[i] * (1 - a) + z * a;
      data[i] = z;
    }
  }

  function highpass(data, sr, cutoff) {
    var a = Math.exp(-2 * Math.PI * cutoff / sr);
    var z = 0, prev = 0;
    for (var i = 0; i < data.length; i++) {
      var x = data[i];
      z = a * (z + x - prev);
      prev = x;
      data[i] = z;
    }
  }

  /* Gwar ludzki: kilka pasm szumu modulowanych w tempie sylaby (3-5 Hz),
     każde z własną fazą. Pojedyncze pasmo brzmi jak szum; sześć pasm
     o różnych rytmach zaczyna brzmieć jak sala pełna rozmów. */
  function babble(data, sr, rand, voices, gain) {
    var tmp = new Float32Array(data.length);
    for (var v = 0; v < voices; v++) {
      tmp.fill(0);
      whiteInto(tmp, rand, 1);
      var centre = 250 + rand() * 1400;         // pasmo formantowe mowy
      lowpass(tmp, sr, centre * 1.6);
      highpass(tmp, sr, centre * 0.55);
      var rate = 2.6 + rand() * 2.6;            // sylab na sekundę
      var phase = rand() * Math.PI * 2;
      var pause = rand();
      /* Obwiednie liczymy co STEP próbek i interpolujemy liniowo. Najszybsza
         z nich zmienia się 5 razy na sekundę, więc 689 punktów na sekundę to
         przesada z zapasem — a dwa wywołania Math.sin na próbkę razy siedem
         głosów razy osiem sekund to siedemnaście milionów operacji, czyli
         zauważalna zwłoka przed pierwszym dźwiękiem. */
      var STEP = 64;
      var slow = 2 * Math.PI * (0.13 + pause * 0.2);
      var fast = 2 * Math.PI * rate;
      var prev = 0, next = 0;
      for (var i = 0; i < data.length; i++) {
        if ((i & (STEP - 1)) === 0) {
          prev = next;
          var t2 = Math.min(i + STEP, data.length) / sr;
          var e2 = 0.5 + 0.5 * Math.sin(fast * t2 + phase);
          var s2 = 0.55 + 0.45 * Math.sin(slow * t2 + pause * 6);
          next = e2 * e2 * Math.max(0, s2);
          if (i === 0) {
            var e0 = 0.5 + 0.5 * Math.sin(phase);
            var s0 = 0.55 + 0.45 * Math.sin(pause * 6);
            prev = e0 * e0 * Math.max(0, s0);
          }
        }
        var frac = (i & (STEP - 1)) / STEP;
        data[i] += tmp[i] * (prev + (next - prev) * frac) * gain;
      }
    }
  }

  /* Krótkie uderzenia: sztućce, talerze, drzwi. */
  function clatter(data, sr, rand, perSecond, gain, tone) {
    var count = Math.max(1, Math.round(data.length / sr * perSecond));
    for (var k = 0; k < count; k++) {
      var at = Math.floor(rand() * (data.length - sr * 0.2));
      var len = Math.floor(sr * (0.02 + rand() * 0.06));
      var freq = tone * (0.7 + rand() * 0.9);
      var amp = gain * (0.4 + rand() * 0.6);
      for (var i = 0; i < len; i++) {
        var e = Math.exp(-i / (len * 0.28));
        data[at + i] += Math.sin(2 * Math.PI * freq * i / sr) * e * amp * (0.6 + rand() * 0.4);
      }
    }
  }

  /* Przejeżdżający pojazd: szerokopasmowy szum z obwiednią i zjazdem widma. */
  function passBy(data, sr, rand, count, gain) {
    for (var k = 0; k < count; k++) {
      var len = Math.floor(sr * (1.2 + rand() * 1.8));
      var at = Math.floor(rand() * Math.max(1, data.length - len));
      var tmp = new Float32Array(len);
      whiteInto(tmp, rand, 1);
      lowpass(tmp, sr, 420 + rand() * 500);
      for (var i = 0; i < len; i++) {
        var x = i / len;
        var env = Math.sin(Math.PI * x);
        data[at + i] += tmp[i] * env * env * gain;
      }
    }
  }

  var NOISE_KINDS = {
    restaurant: {
      label: 'restauracja',
      build: function (data, sr, rand) {
        babble(data, sr, rand, 7, 0.42);
        clatter(data, sr, rand, 1.6, 0.11, 2600);
        var hum = new Float32Array(data.length);
        whiteInto(hum, rand, 1);
        lowpass(hum, sr, 180);
        for (var i = 0; i < data.length; i++) data[i] += hum[i] * 0.5;
      }
    },
    street: {
      label: 'ulica',
      build: function (data, sr, rand) {
        var rumble = new Float32Array(data.length);
        whiteInto(rumble, rand, 1);
        lowpass(rumble, sr, 140);
        for (var i = 0; i < data.length; i++) data[i] += rumble[i] * 1.4;
        passBy(data, sr, rand, 4, 0.55);
        babble(data, sr, rand, 2, 0.12);
        clatter(data, sr, rand, 0.35, 0.06, 900);
      }
    },
    station: {
      label: 'dworzec',
      build: function (data, sr, rand) {
        var hall = new Float32Array(data.length);
        whiteInto(hall, rand, 1);
        lowpass(hall, sr, 2400);
        highpass(hall, sr, 90);
        for (var i = 0; i < data.length; i++) data[i] += hall[i] * 0.5;
        babble(data, sr, rand, 5, 0.3);
        /* Komunikat z głośnika: pasmo mowy, mocno ograniczone i modulowane. */
        var pa = new Float32Array(data.length);
        whiteInto(pa, rand, 1);
        lowpass(pa, sr, 2600);
        highpass(pa, sr, 480);
        var start = data.length * 0.25, span = data.length * 0.4;
        for (var j = 0; j < data.length; j++) {
          if (j < start || j > start + span) continue;
          var t = (j - start) / sr;
          var env = Math.max(0, Math.sin(2 * Math.PI * 3.1 * t));
          data[j] += pa[j] * env * 0.55;
        }
        clatter(data, sr, rand, 0.5, 0.14, 1600);
      }
    }
  };

  DSP.noiseKinds = function () {
    return Object.keys(NOISE_KINDS).map(function (k) {
      return { id: k, label: NOISE_KINDS[k].label };
    });
  };

  /* Bufor szumu do zapętlenia. Osiem sekund wystarcza, żeby ucho nie
     rozpoznało pętli, a nie wystarcza, żeby generowanie trwało zauważalnie. */
  DSP.noiseBuffer = function (kind, seconds, seed) {
    var c = DSP.context();
    if (!c) return null;
    var def = NOISE_KINDS[kind] || NOISE_KINDS.restaurant;
    var sr = c.sampleRate;
    var len = Math.floor(sr * (seconds || 8));
    var buf = c.createBuffer(2, len, sr);
    var rand = rng(seed || 1337);
    var left = buf.getChannelData(0);
    def.build(left, sr, rand);
    /* Drugi kanał to ten sam materiał z opóźnieniem i inną obwiednią —
       tanie rozsunięcie w przestrzeni, bez liczenia wszystkiego dwa razy. */
    var right = buf.getChannelData(1);
    var shift = Math.floor(sr * 0.017);
    for (var i = 0; i < len; i++) right[i] = left[(i + shift) % len] * 0.92;
    normalise(buf);
    return buf;
  };

  function normalise(buffer) {
    var peak = 0, ch, i, d;
    for (ch = 0; ch < buffer.numberOfChannels; ch++) {
      d = buffer.getChannelData(ch);
      for (i = 0; i < d.length; i++) if (Math.abs(d[i]) > peak) peak = Math.abs(d[i]);
    }
    if (peak < 1e-6) return;
    var g = 0.92 / peak;
    for (ch = 0; ch < buffer.numberOfChannels; ch++) {
      d = buffer.getChannelData(ch);
      for (i = 0; i < d.length; i++) d[i] *= g;
    }
  }

  /* -------------------------------------------------------------- pogłos */

  /* Odpowiedź impulsowa: szum z obwiednią wykładniczą plus kilka wczesnych
     odbić. Same wczesne odbicia dają wrażenie wielkości pomieszczenia,
     ogon — jego pochłanialności. */
  var ROOMS = {
    room:       { label: 'mały pokój', rt60: 0.35, damp: 4200, early: 5 },
    restaurant: { label: 'sala restauracji', rt60: 0.85, damp: 2800, early: 8 },
    hall:       { label: 'hala dworca', rt60: 2.20, damp: 1800, early: 12 }
  };

  DSP.roomKinds = function () {
    return Object.keys(ROOMS).map(function (k) { return { id: k, label: ROOMS[k].label }; });
  };

  DSP.impulse = function (kind) {
    var c = DSP.context();
    if (!c) return null;
    var def = ROOMS[kind] || ROOMS.room;
    var sr = c.sampleRate;
    var len = Math.max(1, Math.floor(sr * def.rt60 * 1.1));
    var buf = c.createBuffer(2, len, sr);
    var rand = rng(4711);
    for (var ch = 0; ch < 2; ch++) {
      var d = buf.getChannelData(ch);
      whiteInto(d, rand, 1);
      lowpass(d, sr, def.damp);
      /* -60 dB po czasie rt60 */
      var k = Math.log(1000) / (def.rt60 * sr);
      for (var i = 0; i < len; i++) d[i] *= Math.exp(-k * i);
      for (var e = 0; e < def.early; e++) {
        var at = Math.floor(sr * (0.004 + rand() * def.rt60 * 0.18));
        if (at < len) d[at] += (rand() > 0.5 ? 1 : -1) * 0.35 * Math.exp(-k * at);
      }
    }
    return buf;
  };

  /* ------------------------------------------------------------- telefon */

  /* Łącze telefoniczne przepuszcza mniej więcej 300-3400 Hz. Dla polskiego
     ucha najważniejsza strata jest u góry: znika szum przydechu, po którym
     rozróżnia się kh od k. Dlatego to osobne ćwiczenie, a nie efekt. */
  DSP.telephoneChain = function (destination) {
    var c = DSP.context();
    if (!c) return null;
    var hp = c.createBiquadFilter();
    hp.type = 'highpass'; hp.frequency.value = 300; hp.Q.value = 0.9;
    var lp = c.createBiquadFilter();
    lp.type = 'lowpass'; lp.frequency.value = 3400; lp.Q.value = 0.9;
    var peak = c.createBiquadFilter();
    peak.type = 'peaking'; peak.frequency.value = 1600; peak.Q.value = 1.1; peak.gain.value = 5;
    var shaper = c.createWaveShaper();
    shaper.curve = softClip(2.2);
    hp.connect(lp); lp.connect(peak); peak.connect(shaper);
    if (destination) shaper.connect(destination);
    return { input: hp, output: shaper };
  };

  function softClip(amount) {
    var n = 1024, curve = new Float32Array(n);
    for (var i = 0; i < n; i++) {
      var x = (i / (n - 1)) * 2 - 1;
      curve[i] = Math.tanh(x * amount) / Math.tanh(amount);
    }
    return curve;
  }

  /* ------------------------------------------- pamięć podręczna buforów */

  /* Syntezowanie i przetwarzanie tego samego zdania po raz dwudziesty to
     czysta strata. Trzymamy gotowe bufory pod kluczem opisującym wszystko,
     co wpłynęło na ich zawartość, i wyrzucamy najdawniej używany, kiedy
     zabraknie miejsca. Limit liczony jest w bajtach, bo o pamięć chodzi —
     liczba pozycji nic nie mówi, gdy jedna waży 40 kB, a druga 3 MB. */
  function Cache(limitBytes) {
    this.limit = limitBytes;
    this.map = new Map();       // Map trzyma kolejność wstawiania
    this.bytes = 0;
    this.hits = 0;
    this.misses = 0;
    this.evictions = 0;
  }

  Cache.prototype.sizeOf = function (buffer) {
    if (!buffer || !buffer.length) return 0;
    return buffer.length * (buffer.numberOfChannels || 1) * 4;
  };

  Cache.prototype.get = function (key) {
    if (!this.map.has(key)) { this.misses++; return null; }
    var val = this.map.get(key);
    /* Odczyt odświeża pozycję: usuwamy i wstawiamy na koniec kolejki. */
    this.map['delete'](key);
    this.map.set(key, val);
    this.hits++;
    return val;
  };

  Cache.prototype.set = function (key, buffer) {
    if (!buffer) return buffer;
    var size = this.sizeOf(buffer);
    if (size > this.limit) return buffer;       // za duże, nie warto
    if (this.map.has(key)) {
      this.bytes -= this.sizeOf(this.map.get(key));
      this.map['delete'](key);
    }
    this.map.set(key, buffer);
    this.bytes += size;
    while (this.bytes > this.limit && this.map.size > 1) {
      var oldest = this.map.keys().next().value;
      this.bytes -= this.sizeOf(this.map.get(oldest));
      this.map['delete'](oldest);
      this.evictions++;
    }
    return buffer;
  };

  Cache.prototype.clear = function () {
    this.map.clear();
    this.bytes = 0;
  };

  Cache.prototype.stats = function () {
    var total = this.hits + this.misses;
    return {
      entries: this.map.size,
      bytes: this.bytes,
      limit: this.limit,
      hits: this.hits,
      misses: this.misses,
      evictions: this.evictions,
      hitRate: total ? this.hits / total : 0
    };
  };

  DSP.Cache = Cache;
  /* 24 MB to około czterdziestu sekund dźwięku stereo przy 44,1 kHz —
     w praktyce kilkadziesiąt przetworzonych zdań plus komplet szumów. */
  DSP.cache = new Cache(24 * 1024 * 1024);

  /* Wygenerowanie ośmiosekundowego gwaru to kilkadziesiąt milionów operacji.
     Bez pamięci podręcznej każde włączenie ćwiczenia liczyłoby to od nowa. */
  DSP.noise = function (kind, level) {
    var key = 'noise:' + kind + ':' + (level || 0);
    var hit = DSP.cache.get(key);
    if (hit) return hit;
    return DSP.cache.set(key, DSP.noiseBuffer(kind, 8, 1337 + (level || 0) * 17));
  };

  DSP.room = function (kind) {
    var key = 'ir:' + kind;
    var hit = DSP.cache.get(key);
    if (hit) return hit;
    return DSP.cache.set(key, DSP.impulse(kind));
  };

  global.DSP = DSP;

  /* Testy uruchamiane poza przeglądarką korzystają z samych funkcji czystych. */
  if (typeof module !== 'undefined' && module.exports) module.exports = DSP;
})(typeof window !== 'undefined' ? window : this);
