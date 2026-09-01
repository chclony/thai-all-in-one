/* Thai All-in-One — synteza mowy (SpeechSynthesis).
   Moduł nigdy nie wypisuje tekstu tajskiego do DOM — dostaje go wyłącznie
   z prywatnej mapy DB.voiceText() i przekazuje bezpośrednio do syntezatora. */
(function (global) {
  'use strict';

  var NO_VOICE_MSG = 'Na tym urządzeniu nie wykryto tajskiego głosu systemowego. ' +
    'Zainstaluj język/głos tajski w ustawieniach systemu lub skorzystaj z innej przeglądarki.';

  var Speech = {
    supported: 'speechSynthesis' in global,
    voice: null,          // głos domyślny (pierwszy tajski)
    voices: [],           // wszystkie głosy systemowe
    thaiVoices: [],       // wyłącznie tajskie, w kolejności przydatności
    unlocked: false,
    warned: false
  };

  function pickVoice() {
    if (!Speech.supported) return null;
    var all = global.speechSynthesis.getVoices() || [];
    Speech.voices = all;
    var thai = all.filter(function (v) {
      var lang = (v.lang || '').toLowerCase().replace('_', '-');
      return lang === 'th-th' || lang === 'th' || lang.indexOf('th-') === 0;
    });
    if (!thai.length) {
      /* Zapis \u… zamiast liter tajskich — w kodzie źródłowym również ich nie trzymamy. */
      thai = all.filter(function (v) { return /thai|\u0E44\u0E17\u0E22/i.test(v.name || ''); });
    }
    /* Głosy lokalne brzmią lepiej i działają bez internetu. */
    thai.sort(function (a, b) { return (b.localService ? 1 : 0) - (a.localService ? 1 : 0); });
    Speech.thaiVoices = thai;
    Speech.voice = thai[0] || null;
    return Speech.voice;
  }

  if (Speech.supported) {
    pickVoice();
    global.speechSynthesis.addEventListener('voiceschanged', function () {
      pickVoice();
      if (typeof Speech.onVoiceChange === 'function') Speech.onVoiceChange();
    });
    /* Niektóre przeglądarki wypełniają listę głosów z opóźnieniem. */
    setTimeout(pickVoice, 400);
    setTimeout(pickVoice, 1500);
  }

  Speech.hasThaiVoice = function () { return !!Speech.voice; };
  Speech.missingVoiceMessage = NO_VOICE_MSG;

  /* Nazwa głosu pochodzi z systemu i bywa zapisana pismem tajskim.
     Zanim trafi na ekran, usuwamy z niej wszystkie znaki tajskie. */
  function safeName(name) {
    var clean = String(name || '').replace(/[\u0E00-\u0E7F]/g, '').replace(/\s+/g, ' ').trim();
    return clean || 'głos systemowy';
  }

  Speech.voiceLabel = function () {
    if (!Speech.supported) return 'Ta przeglądarka nie obsługuje syntezy mowy.';
    if (!Speech.voice) return NO_VOICE_MSG;
    return 'Wykryty głos: ' + safeName(Speech.voice.name) + ' (' + Speech.voice.lang + ')' +
      (Speech.voice.localService ? ' — głos lokalny, działa offline.' : ' — głos sieciowy, wymaga internetu.');
  };

  /* iOS i część przeglądarek mobilnych odtwarzają mowę dopiero po geście użytkownika.
     Pierwsze dotknięcie ekranu wypuszcza pustą wypowiedź, która odblokowuje kanał. */
  Speech.unlock = function () {
    if (Speech.unlocked || !Speech.supported) return;
    try {
      var u = new SpeechSynthesisUtterance(' ');
      u.volume = 0;
      global.speechSynthesis.speak(u);
      Speech.unlocked = true;
      pickVoice();
    } catch (e) { /* brak wsparcia — obsłużone niżej komunikatem */ }
  };

  Speech.stop = function () {
    Speech.cancelParts();
    if (!Speech.supported) return;
    try { global.speechSynthesis.cancel(); } catch (e) {}
  };

  /* --------------------------------------------------- głosy dla ról ------

     W scenie z dwoma rozmówcami obie kwestie wypowiedziane tym samym głosem
     zlewają się w monolog. Ucho rozdziela mówiących zanim zrozumie słowa —
     jeżeli tego sygnału nie ma, ćwiczenie jest trudniejsze niż rzeczywistość,
     ale w niewłaściwy sposób.

     Gdy system ma dwa głosy tajskie, każda rola dostaje własny. Gdy ma jeden
     — a tak jest najczęściej — różnicujemy wysokością i tempem. To namiastka:
     dwie osoby różnią się barwą, nie samą wysokością. Ale namiastka wystarcza,
     żeby słuchacz wiedział, kto właśnie mówi. */

  var FEMALE_HINT = /female|kobie|\bf\b|premwadee|kanya|narisa/i;
  var MALE_HINT = /male|m\u0119\u017Ac|\bm\b|somsak|niwat/i;

  function voiceGender(v) {
    var n = (v && v.name) || '';
    if (FEMALE_HINT.test(n)) return 'female';
    if (MALE_HINT.test(n)) return 'male';
    return null;
  }

  /* role: klucz roli ('A' / 'B'), gender: 'female' | 'male' | null.
     Zwraca { voice, pitch, rate, distinct } — distinct mówi, czy rozróżnienie
     opiera się na osobnym głosie, czy tylko na wysokości. */
  Speech.roleProfile = function (role, gender) {
    var list = Speech.thaiVoices || [];
    var second = role === 'B';
    if (list.length >= 2) {
      var pick = null;
      if (gender) {
        for (var i = 0; i < list.length; i++) {
          if (voiceGender(list[i]) === gender) { pick = list[i]; break; }
        }
      }
      if (!pick) pick = list[second ? 1 : 0];
      return { voice: pick, pitch: 1, rate: 1, distinct: true };
    }
    /* Jeden głos: rozsuwamy role wysokością i odrobiną tempa. Zakres jest
       celowo wąski — poza nim silniki zaczynają brzmieć jak nagranie puszczone
       z innej prędkości i psują kontur tonalny, o który tu przecież chodzi. */
    var pitch = second ? 0.82 : 1.06;
    if (gender === 'female') pitch += 0.14;
    if (gender === 'male') pitch -= 0.08;
    return {
      voice: list[0] || Speech.voice,
      pitch: Math.max(0.6, Math.min(1.5, pitch)),
      rate: second ? 1.04 : 0.98,
      distinct: false
    };
  };

  /* opts: { rate, pitch, voice, onstart, onend, onerror } */
  Speech.speak = function (text, opts) {
    opts = opts || {};
    if (!Speech.supported) {
      if (opts.onerror) opts.onerror('unsupported');
      return false;
    }
    if (!Speech.voice) pickVoice();
    if (!Speech.voice) {
      if (opts.onerror) opts.onerror('no-voice');
      return false;
    }
    Speech.stop();
    var u = new SpeechSynthesisUtterance(text);
    /* Lista głosów potrafi się przebudować w trakcie działania (system
       doinstalował głos, przeglądarka wróciła z uśpienia). Obiekt trzymany
       od poprzedniego odtworzenia bywa wtedy nieważny i przypisanie rzuca
       wyjątkiem — wolimy wypowiedź głosem domyślnym niż ciszę i błąd. */
    var wanted = opts.voice || Speech.voice;
    try { u.voice = wanted; } catch (e) { wanted = Speech.voice; }
    u.lang = (wanted && wanted.lang) || 'th-TH';
    u.rate = opts.rate || 1;
    u.pitch = opts.pitch || 1;
    /* Głośność. Domyślnie pełna; wartość poniżej jedynki wykorzystuje dryl
       odruchu, w którym kwestia jest podana ZA CICHO — to jest jeden
       z czterech realnych powodów, dla których nie rozumie się rozmówcy,
       i jedyny, którego nie da się oddać tempem ani hałasem tła. */
    u.volume = (typeof opts.volume === 'number') ? Math.max(0, Math.min(1, opts.volume)) : 1;
    if (opts.onstart) u.onstart = opts.onstart;
    u.onend = function () { if (opts.onend) opts.onend(); };
    u.onerror = function () {
      if (opts.onend) opts.onend();
      if (opts.onerror) opts.onerror('speech-error');
    };
    try {
      global.speechSynthesis.speak(u);
      /* Chrome bywa wstrzymany po powrocie do karty. */
      if (global.speechSynthesis.paused) global.speechSynthesis.resume();
      return true;
    } catch (e) {
      if (opts.onerror) opts.onerror('speech-error');
      return false;
    }
  };

  /* ------------------------------------------------ mowa po kawałku ------

     Tempo dydaktyczne nie może iść przez utterance.rate: rate rozciąga kontur
     tonalny razem z czasem, a w języku tonalnym kontur jest znaczeniem.
     Zamiast tego mówimy wypowiedź wyraz po wyrazie — każdy przy rate 1,0,
     czyli z konturem dokładnie takim, jaki wypuszcza silnik — i wydłużamy
     PAUZY między nimi. Wolniej robi się cała wypowiedź, nie pojedynczy ton.

     Granice wyrazów w piśmie tajskim wyznacza generator
     tools/generators/build-tts-split.py i zapisuje jako same długości. */

  Speech.speakParts = function (parts, opts) {
    opts = opts || {};
    var list = (parts || []).filter(function (p) { return p && p.trim(); });
    if (!list.length) { if (opts.onerror) opts.onerror('empty'); return false; }
    if (list.length === 1) return Speech.speak(list[0], opts);

    var gap = opts.gap == null ? 260 : opts.gap;
    var i = 0, cancelled = false;
    var timer = null;

    function step() {
      if (cancelled) return;
      if (i >= list.length) { if (opts.onend) opts.onend(); return; }
      var text = list[i++];
      Speech.speak(text, {
        rate: opts.rate,
        pitch: opts.pitch,
        voice: opts.voice,
        onstart: i === 1 && opts.onstart ? opts.onstart : null,
        onend: function () {
          if (cancelled) return;
          timer = global.setTimeout(step, gap);
        },
        onerror: function (reason) {
          cancelled = true;
          if (opts.onerror) opts.onerror(reason);
        }
      });
    }

    Speech.cancelParts = function () {
      cancelled = true;
      if (timer) global.clearTimeout(timer);
      timer = null;
    };
    step();
    return true;
  };

  Speech.cancelParts = function () {};

  global.Speech = Speech;
})(window);
