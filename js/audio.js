/* Thai All-in-One — odtwarzanie.

   Kolejność źródeł: 1) nagranie lektora (audioFile), 2) synteza mowy,
   3) czytelny komunikat. Nowe odtworzenie zawsze przerywa poprzednie.

   CZTERY RZECZY, KTÓRE TEN MODUŁ DOKŁADA DO SUROWEJ SYNTEZY
   ---------------------------------------------------------
   1. DRABINA TEMPA — 0,7x dydaktyczne, 1,0x naturalne, 1,4x potoczne.
   2. MOWA POŁĄCZONA — w trybie potocznym syntezator dostaje zredukowany
      zapis (pole colloquial), a nie formę słownikową.
   3. WARUNKI AKUSTYCZNE — szum tła, pogłos, pasmo telefoniczne.
   4. DWA GŁOSY — w scenie z dwoma rozmówcami role brzmią różnie.

   DWA SILNIKI I DLACZEGO AŻ DWA
   -----------------------------
   Silnik BUFOROWY dostaje próbki dźwięku i robi z nimi wszystko: rozciąga
   w czasie bez zmiany wysokości (WSOLA), splata z odpowiedzią impulsową,
   filtruje pasmo. Wymaga jednak sygnału na wejściu — czyli nagrania albo
   przechwyconego wyjścia syntezatora.

   Przechwycić wyjścia syntezatora się nie da (szczegóły: js/capture.js oraz
   docs/ograniczenia-tts.md), a nagrań w tym projekcie nie ma. W praktyce
   działa więc silnik SYNTEZATOROWY i to on musi odzyskać tyle realizmu,
   ile się da bez dostępu do próbek:

     * tempo wolne  — wypowiedź cięta na wyrazy, każdy przy rate 1,0,
       wydłużone pauzy między nimi. Kontur każdego tonu zostaje nietknięty.
     * tempo szybkie — zredukowany zapis (krótszy sam z siebie) plus
       ograniczony rate. Część przyspieszenia bierze się z fonetyki,
       a nie z silnika.
     * akustyka — szum i pogłos idą RÓWNOLEGLE, jako drugi dźwięk mieszany
       na wyjściu. Mowy nie filtrujemy, bo jej nie mamy; ale szum, który
       maskuje mowę, maskuje ją tak samo skutecznie niezależnie od tego,
       czy siedzi w tym samym buforze.

   Czego ten wariant nie odtwarza: pogłosu NA GŁOSIE i pasma telefonicznego
   NA GŁOSIE. Jedno i drugie wymaga próbek mowy. Aplikacja mówi o tym wprost
   w Ustawieniach, zamiast udawać, że filtr działa. */
(function (global) {
  'use strict';

  var TEMPOS = [
    { id: 'slow', factor: 0.7, label: 'dydaktyczne',
      hint: 'Wolno, wyraz po wyrazie — do rozbierania zdania na części.' },
    { id: 'natural', factor: 1.0, label: 'naturalne',
      hint: 'Tak, jak mówi syntezator: wyraźnie i w jednym ciągu.' },
    { id: 'fast', factor: 1.4, label: 'potoczne',
      hint: 'Tempo zbliżone do rozmowy — z redukcjami mowy połączonej.' }
  ];

  /* Powyżej tej wartości rate zaczyna wyraźnie deformować kontur tonalny.
     Resztę przyspieszenia bierzemy z krótszego zapisu potocznego. */
  var MAX_RATE = 1.25;

  var Audio2 = {
    rate: 1,
    tempo: 'natural',       // 'slow' | 'natural' | 'fast'
    colloquial: false,      // czy syntezator dostaje wariant zredukowany
    noiseKind: 'restaurant',
    noiseLevel: 0,          // 0 = cisza, 1-3 = coraz trudniej
    room: '',               // '' | 'room' | 'restaurant' | 'hall'
    phone: false,
    current: null,
    activeBtn: null,
    repeatTimer: null,
    ambience: null,
    lastEngine: '',         // 'buffer' | 'synth' | 'synth-parts' | 'synth-rate'
    lastNote: ''
  };

  Audio2.tempos = function () { return TEMPOS.slice(); };

  Audio2.tempoDef = function (id) {
    for (var i = 0; i < TEMPOS.length; i++) {
      if (TEMPOS[i].id === (id || Audio2.tempo)) return TEMPOS[i];
    }
    return TEMPOS[1];
  };

  function markStart(btn) {
    if (Audio2.activeBtn && Audio2.activeBtn !== btn) Audio2.activeBtn.classList.remove('playing');
    Audio2.activeBtn = btn || null;
    if (btn) {
      btn.classList.add('playing');
      btn.setAttribute('aria-pressed', 'true');
    }
  }

  function markEnd() {
    if (Audio2.activeBtn) {
      Audio2.activeBtn.classList.remove('playing');
      Audio2.activeBtn.setAttribute('aria-pressed', 'false');
      Audio2.activeBtn = null;
    }
  }

  Audio2.setRate = function (rate) {
    Audio2.rate = parseFloat(rate) || 1;
    U.store.set('rate', Audio2.rate);
  };

  Audio2.setTempo = function (id) {
    Audio2.tempo = Audio2.tempoDef(id).id;
    return Audio2.tempo;
  };

  /* --------------------------------------------------- warunki akustyczne */

  /* Szum tła i pogłos budujemy jako osobny, równoległy tor. Dzięki temu
     działają także wtedy, gdy mowa idzie prosto z syntezatora i nie mamy
     do niej dostępu. Poziom trudności steruje stosunkiem sygnału do szumu:
     to jedyna wielkość, która w tym ćwiczeniu naprawdę coś znaczy. */
  var NOISE_GAIN = { 1: 0.18, 2: 0.34, 3: 0.55 };

  Audio2.noiseGain = function (level) {
    return NOISE_GAIN[level] || 0;
  };

  /* override: { kind, level, room } — ustawienia na jedno odtworzenie.

     Ćwiczenie „rozumienie w hałasie” ma własny, rosnący poziom trudności,
     niezależny od suwaka w Ustawieniach. Pierwsza wersja podmieniała pola
     globalne i przywracała je po chwili — i przy dwóch renderowaniach pod
     rząd druga zapamiętywała jako „stan użytkownika” to, co ustawiła
     pierwsza. Ustawienie przekazywane przez argument nie ma jak wyciec. */
  Audio2.startAmbience = function (override) {
    Audio2.stopAmbience();
    var cfg = override || {};
    var kind = cfg.kind || Audio2.noiseKind;
    var level = cfg.level == null ? Audio2.noiseLevel : cfg.level;
    var room = cfg.room == null ? Audio2.room : cfg.room;
    if (!level || !global.DSP || !DSP.supported()) return null;
    var ctx = DSP.resume();
    if (!ctx) return null;

    var buffer = DSP.noise(kind, level);
    if (!buffer) return null;

    var src = ctx.createBufferSource();
    src.buffer = buffer;
    src.loop = true;
    var gain = ctx.createGain();
    gain.gain.value = 0;

    if (room && ctx.createConvolver) {
      var ir = DSP.room(room);
      if (ir) {
        var conv = ctx.createConvolver();
        conv.buffer = ir;
        var wet = ctx.createGain();
        wet.gain.value = 0.5;
        gain.connect(conv);
        conv.connect(wet);
        wet.connect(ctx.destination);
      }
    }
    gain.connect(ctx.destination);
    src.connect(gain);

    var target = Audio2.noiseGain(level);
    var now = ctx.currentTime;
    /* Szum wchodzi płynnie: nagłe włączenie samo w sobie jest sygnałem,
       po którym słuchacz wie, że zaraz coś usłyszy. */
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(target, now + 0.35);
    try { src.start(0); } catch (e) {}

    Audio2.ambience = { src: src, gain: gain, ctx: ctx };
    return Audio2.ambience;
  };

  Audio2.stopAmbience = function () {
    var amb = Audio2.ambience;
    Audio2.ambience = null;
    if (!amb) return;
    try {
      var now = amb.ctx.currentTime;
      amb.gain.gain.cancelScheduledValues(now);
      amb.gain.gain.setValueAtTime(amb.gain.gain.value, now);
      amb.gain.gain.linearRampToValueAtTime(0, now + 0.25);
      amb.src.stop(now + 0.3);
    } catch (e) {
      try { amb.src.stop(); } catch (e2) {}
    }
  };

  /* Wygenerowanie ośmiosekundowego gwaru to kilkaset milisekund liczenia.
     Puszczone przy pierwszym kliknięciu opóźniłoby dźwięk o tyle samo, więc
     robimy to wcześniej — w wolnej chwili po zmianie ustawień. Kolejne
     odtworzenia biorą gotowy bufor z pamięci podręcznej. */
  Audio2.prewarm = function () {
    if (!Audio2.noiseLevel || !global.DSP || !DSP.supported()) return;
    var idle = global.requestIdleCallback || function (fn) { return setTimeout(fn, 120); };
    idle(function () {
      try {
        DSP.noise(Audio2.noiseKind, Audio2.noiseLevel);
        if (Audio2.room) DSP.room(Audio2.room);
      } catch (e) {}
    });
  };

  Audio2.stop = function () {
    clearTimeout(Audio2.repeatTimer);
    Audio2.repeatTimer = null;
    if (Audio2.current) {
      try {
        if (Audio2.current.pause) { Audio2.current.pause(); Audio2.current.currentTime = 0; }
        else if (Audio2.current.stop) Audio2.current.stop();
      } catch (e) {}
      Audio2.current = null;
    }
    Speech.stop();
    Audio2.stopAmbience();
    markEnd();
  };

  /* ------------------------------------------------------- wybór tekstu */

  /* W trybie potocznym syntezator dostaje zredukowany zapis, o ile rekord go
     ma. Wariant istnieje dla materiału kursu i wszystkich dialogów — poza tym
     zakresem odtwarzamy formę słownikową i mówimy o tym w interfejsie. */
  Audio2.voiceSource = function (item) {
    var coll = item && item.colloquial;
    if (Audio2.colloquial && coll && coll.ttsKey) {
      return { key: coll.ttsKey, split: coll.ttsSplit || null, colloquial: true };
    }
    return { key: item && item.ttsKey, split: (item && item.ttsSplit) || null, colloquial: false };
  };

  /* Tekst pocięty na wyrazy — granice trzymamy jako same długości, więc
     pismo tajskie nie musi (i nie może) opuścić prywatnej mapy w DB. */
  function parts(text, split) {
    if (!text) return [];
    if (!split || !split.length) return [text];
    var out = [], at = 0, i;
    for (i = 0; i < split.length; i++) {
      out.push(text.substr(at, split[i]));
      at += split[i];
    }
    if (at < text.length) out.push(text.substr(at));
    return out.filter(function (p) { return p && p.trim(); });
  }

  Audio2.parts = parts;

  /* ------------------------------------------------------------- główna */

  /* item: rekord, przykład albo kwestia dialogu (ma audioFile i ttsKey)
     opts: { btn, rate, tempo, role, gender, onend, silentWarning, noAmbience } */
  Audio2.play = function (item, opts) {
    opts = opts || {};
    Audio2.stop();
    if (!item) return;

    /* Wpis skrócony nie ma jeszcze klucza głosu — pełny rekord leży w pliku
       poziomu, który dociągamy dopiero teraz. Przycisk zostaje wciśnięty na
       czas pobierania, żeby było widać, że coś się dzieje. */
    if (item.__stub && item.id && global.DB && DB.ensureFor) {
      var waiting = opts.btn || null;
      if (waiting) waiting.classList.add('loading');
      DB.ensureFor([item.id]).then(function () {
        if (waiting) waiting.classList.remove('loading');
        var full = DB.get(item.id);
        if (!full) { U.toast('Nie udało się wczytać wymowy tego hasła.'); return; }
        Audio2.play(global.G ? G.view(full) : full, opts);
      });
      return;
    }

    var tempo = Audio2.tempoDef(opts.tempo || Audio2.tempo);
    var btn = opts.btn || null;
    var ambience = opts.noAmbience ? null : Audio2.startAmbience(opts.noise);

    var finished = false;
    var finish = function () {
      if (finished) return;
      finished = true;
      markEnd();
      Audio2.current = null;
      if (ambience) Audio2.stopAmbience();
      if (opts.onend) opts.onend();
    };

    /* Etap 1 — nagranie lektora. Tu działa pełny tor buforowy. */
    if (item.audioFile) {
      Audio2.lastEngine = 'buffer';
      Audio2.lastNote = 'Nagranie: pełne przetwarzanie na buforze.';
      playFile(item, tempo, btn, finish, opts);
      return;
    }
    speakFallback();

    /* Etap 2 — synteza mowy z ukrytego pola technicznego. */
    function speakFallback() {
      var src = Audio2.voiceSource(item);
      var text = DB.voiceText(src.key);
      if (!text) { warn(); finish(); return; }
      Speech.unlock();
      markStart(btn);

      var profile = opts.role
        ? Speech.roleProfile(opts.role, opts.gender || null)
        : { voice: null, pitch: 1, rate: 1, distinct: true };

      var baseRate = (opts.rate || Audio2.rate || 1) * (profile.rate || 1);
      var handlers = {
        pitch: profile.pitch,
        voice: profile.voice,
        volume: (typeof opts.volume === 'number') ? opts.volume : 1,
        onend: finish,
        onerror: function (reason) {
          markEnd();
          if (ambience) Audio2.stopAmbience();
          if (reason === 'no-voice' || reason === 'unsupported') warn();
        }
      };

      var ok;
      if (tempo.factor < 1) {
        var chunks = parts(text, src.split);
        if (chunks.length > 1) {
          /* Pauzy dobrane tak, żeby CAŁA wypowiedź trwała mniej więcej
             1/factor razy dłużej. Sama mowa zostaje bez zmian. */
          var gap = Math.round(360 * (1 / tempo.factor - 1) * 2.2);
          Audio2.lastEngine = 'synth-parts';
          Audio2.lastNote = 'Tempo wolne zrobione pauzami — kontury tonalne nietknięte.';
          handlers.rate = baseRate;
          handlers.gap = Math.max(160, Math.min(700, gap));
          ok = Speech.speakParts(chunks, handlers);
        } else {
          /* Brak wyznaczonych granic wyrazów: nie ma czego rozsuwać, więc
             zostaje rate — i uczciwa informacja, co to kosztuje. */
          Audio2.lastEngine = 'synth-rate';
          Audio2.lastNote = 'Brak granic wyrazów dla tego hasła — tempo wolne rozciąga także kontur tonalny.';
          handlers.rate = baseRate * tempo.factor;
          ok = Speech.speak(text, handlers);
        }
      } else if (tempo.factor > 1) {
        /* Część przyspieszenia bierze się z krótszego zapisu potocznego,
           reszta z rate — ograniczonego, żeby kontur przetrwał. */
        var textFactor = src.colloquial ? 1.08 : 1;
        Audio2.lastEngine = 'synth-rate';
        Audio2.lastNote = src.colloquial
          ? 'Tempo potoczne: zredukowany zapis plus ograniczone przyspieszenie.'
          : 'Tempo potoczne: samo przyspieszenie — to hasło nie ma wariantu potocznego.';
        handlers.rate = baseRate * Math.min(MAX_RATE, tempo.factor / textFactor);
        ok = Speech.speak(text, handlers);
      } else {
        Audio2.lastEngine = 'synth';
        Audio2.lastNote = '';
        handlers.rate = baseRate;
        ok = Speech.speak(text, handlers);
      }
      if (!ok) { markEnd(); if (ambience) Audio2.stopAmbience(); }
    }

    /* Etap 3 — komunikat dla użytkownika. */
    function warn() {
      if (opts.silentWarning) return;
      U.toast(Speech.supported ? Speech.missingVoiceMessage
        : 'Ta przeglądarka nie obsługuje syntezy mowy. Zainstaluj aplikację lub użyj innej przeglądarki.');
    }
  };

  /* ------------------------------------------------------ tor buforowy */

  /* Nagranie przechodzi przez pełne przetwarzanie: rozciągnięcie w czasie bez
     zmiany wysokości, pogłos przez splot, pasmo telefoniczne. Gotowy bufor
     ląduje w pamięci podręcznej pod kluczem opisującym wszystko, co na niego
     wpłynęło — dwudzieste odtworzenie tego samego zdania nic już nie kosztuje. */

  var pending = {};

  Audio2.processedKey = function (url, tempo) {
    return 'buf:' + url + ':' + tempo.factor;
  };

  function loadProcessed(url, tempo) {
    var key = Audio2.processedKey(url, tempo);
    var hit = DSP.cache.get(key);
    if (hit) return Promise.resolve(hit);
    if (pending[key]) return pending[key];
    pending[key] = fetch(url)
      .then(function (r) { return r.arrayBuffer(); })
      .then(function (raw) {
        return new Promise(function (resolve, reject) {
          DSP.context().decodeAudioData(raw, resolve, reject);
        });
      })
      .then(function (buffer) {
        var out = DSP.stretchBuffer(buffer, tempo.factor);
        DSP.cache.set(key, out);
        delete pending[key];
        return out;
      })['catch'](function (err) {
        delete pending[key];
        throw err;
      });
    return pending[key];
  }

  Audio2.loadProcessed = loadProcessed;

  /* Odtworzenie bez przetwarzania: element <audio> zamiast grafu Web Audio.
     Używane, gdy Web Audio nie ma — i gdy fetch nie działa, czyli w trybie
     file://, gdzie przeglądarka blokuje pobieranie plików z dysku. Nagranie
     zagra, ale bez rozciągania w czasie, pogłosu i pasma telefonicznego. */
  function playPlain(url, tempo, btn, finish, opts) {
    var el = new Audio(url);
    /* Tu playbackRate jest jedynym, co mamy — i zmienia wysokość dźwięku.
       Dlatego przy tempie innym niż naturalne odtwarzamy bez zmian tempa,
       zamiast po cichu zafałszować kontury tonalne. */
    el.playbackRate = opts.rate || Audio2.rate;
    Audio2.lastEngine = 'file-plain';
    Audio2.lastNote = tempo.factor === 1
      ? 'Nagranie bez przetwarzania (brak Web Audio albo tryb file://).'
      : 'Nagranie bez przetwarzania — w tym trybie drabina tempa nie działa, '
        + 'bo zmiana prędkości odtwarzania psułaby kontury tonalne.';
    el.onended = finish;
    el.onerror = finish;
    Audio2.current = el;
    markStart(btn);
    var p = el.play();
    if (p && p['catch']) p['catch'](finish);
  }

  function playFile(item, tempo, btn, finish, opts) {
    var url = 'audio/' + item.audioFile;
    if (!global.DSP || !DSP.supported()) {
      playPlain(url, tempo, btn, finish, opts);
      return;
    }
    markStart(btn);
    loadProcessed(url, tempo).then(function (buffer) {
      var ctx = DSP.resume();
      var src = ctx.createBufferSource();
      src.buffer = buffer;
      var node = src;
      if (Audio2.phone) {
        var chain = DSP.telephoneChain(null);
        src.connect(chain.input);
        node = chain.output;
      }
      if (Audio2.room && ctx.createConvolver) {
        var ir = DSP.room(Audio2.room);
        if (ir) {
          var conv = ctx.createConvolver();
          conv.buffer = ir;
          var wet = ctx.createGain();
          wet.gain.value = 0.35;
          node.connect(conv);
          conv.connect(wet);
          wet.connect(ctx.destination);
        }
      }
      node.connect(ctx.destination);
      src.onended = finish;
      Audio2.current = src;
      src.start(0);
    })['catch'](function () {
      /* Najczęstsza przyczyna: tryb file://, w którym fetch odmawia dostępu
         do dysku. Zamiast ciszy dajemy nagranie bez przetwarzania. */
      Audio2.current = null;
      playPlain(url, tempo, btn, finish, opts);
    });
  }

  /* --------------------------------------------------------- sekwencje */

  /* Odtwarza listę pozycji po kolei (całe dialogi). Kwestie różnych ról
     dostają różne głosy — patrz Speech.roleProfile. */
  Audio2.playSequence = function (items, opts) {
    opts = opts || {};
    var i = 0;
    Audio2.stop();
    var ambience = opts.noAmbience ? null : Audio2.startAmbience(opts.noise);
    var done = function () {
      if (ambience) Audio2.stopAmbience();
      if (opts.onend) opts.onend();
    };
    (function next() {
      if (i >= items.length) { done(); return; }
      var item = items[i++];
      if (opts.onstep) opts.onstep(item, i - 1);
      Audio2.play(item, {
        rate: opts.rate,
        tempo: opts.tempo,
        btn: opts.btn,
        role: item && item.role,
        gender: item && (item.__speaker || item.__gender),
        noAmbience: true,
        onend: function () { Audio2.repeatTimer = setTimeout(next, 450); }
      });
    })();
  };

  /* Powtarza tę samą pozycję kilka razy — nauka przez naśladowanie. */
  Audio2.repeat = function (item, times, opts) {
    opts = opts || {};
    var left = times || 3;
    (function loop() {
      if (left-- <= 0) { if (opts.onend) opts.onend(); return; }
      Audio2.play(item, {
        rate: opts.rate,
        tempo: opts.tempo,
        btn: opts.btn,
        onend: function () { Audio2.repeatTimer = setTimeout(loop, 700); }
      });
    })();
  };

  /* Przycisk „posłuchaj” używany na wszystkich ekranach. */
  Audio2.button = function (item, label, opts) {
    opts = opts || {};
    var btn = U.el('button', {
      class: 'btn gold play-btn',
      type: 'button',
      'aria-pressed': 'false',
      'aria-label': 'Posłuchaj wymowy'
    });
    btn.appendChild(U.icon('play'));
    btn.appendChild(U.el('span', { text: label || 'Posłuchaj' }));
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      Audio2.play(item, { btn: btn, role: opts.role, gender: opts.gender,
                          tempo: opts.tempo, noise: opts.noise });
    });
    return btn;
  };

  global.Player = Audio2;
})(window);
