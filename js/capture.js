/* Thai All-in-One — czy da się przechwycić wyjście syntezatora.

   CAŁA WARSTWA DŹWIĘKU STOI NA JEDNYM PYTANIU
   -------------------------------------------
   Żeby rozciągnąć mowę w czasie bez zmiany wysokości, nałożyć na nią pogłos
   albo przepuścić przez filtr telefoniczny, trzeba mieć jej PRÓBKI. Web Audio
   API potrafi to wszystko — ale tylko na buforze, który dostanie na wejściu.

   SpeechSynthesis takiego wejścia nie daje. Wypowiedź trafia prosto na wyjście
   systemowe i nie przechodzi przez graf Web Audio. Nie jest to przeoczenie
   ani błąd konkretnej przeglądarki: w specyfikacji Web Speech API nie ma
   żadnego węzła, strumienia ani zdarzenia, które wypuszczałoby sygnał.
   Na iOS i Androidzie mowa powstaje w ogóle poza procesem karty.

   Ten moduł nie udaje, że jest inaczej. Sprawdza po kolei wszystkie drogi,
   którymi dałoby się ten sygnał zdobyć, zapisuje wynik każdej próby i na tej
   podstawie mówi reszcie aplikacji, którym silnikiem ma odtwarzać.

   TRZY DROGI, KTÓRE SPRAWDZAMY
   ----------------------------
   1. Bezpośrednie wyjście z syntezatora — hipotetyczne API, którego nie ma
      w żadnej przeglądarce. Sprawdzamy mimo to, bo sprawdzenie kosztuje
      mikrosekundę, a gdyby kiedyś się pojawiło, aplikacja skorzysta z niego
      bez zmiany ani jednej linii.
   2. Przechwycenie dźwięku karty (getDisplayMedia z audio). Istnieje na
      komputerach w przeglądarkach opartych na Chromium, wymaga bezpiecznego
      kontekstu, gestu użytkownika i wyboru w oknie systemowym przy KAŻDYM
      uruchomieniu. Do tego mowa systemowa zwykle i tak omija ten strumień,
      bo powstaje poza kartą. Dlatego jest to świadomy eksperyment
      w Ustawieniach, a nie domyślne działanie.
   3. Gotowe nagranie w katalogu audio/ — jedyna droga, która działa zawsze
      i wszędzie. Nagrań w tym projekcie nie ma, ale kod jest gotowy.

   Gdy żadna nie zadziała, zostaje wariant zapasowy opisany w README:
   syntezator mówi bezpośrednio, tempo robimy pauzami między wyrazami,
   a warunki akustyczne dokładamy RÓWNOLEGLE, jako drugi dźwięk w tle. */
(function (global) {
  'use strict';

  var Capture = {
    checked: false,
    result: null,
    stream: null,
    active: false
  };

  function secure() {
    return global.isSecureContext === true ||
      location.protocol === 'https:' ||
      location.hostname === 'localhost' ||
      location.hostname === '127.0.0.1';
  }

  /* Sprawdzenie nie odtwarza niczego i nie prosi o żadne zgody. */
  Capture.probe = function () {
    if (Capture.checked) return Capture.result;

    var probes = [];

    /* 1. Bezpośrednie wyjście syntezatora. */
    var direct = !!(global.speechSynthesis &&
      (global.speechSynthesis.getAudioStream ||
       global.speechSynthesis.captureStream ||
       (global.SpeechSynthesisUtterance &&
        global.SpeechSynthesisUtterance.prototype &&
        'audioStream' in global.SpeechSynthesisUtterance.prototype)));
    probes.push({
      id: 'direct',
      label: 'Bezpośrednie wyjście syntezatora',
      available: direct,
      why: direct ? 'Przeglądarka udostępnia strumień mowy.'
        : 'Web Speech API nie przewiduje dostępu do sygnału mowy — nie ma takiego strumienia w żadnej przeglądarce.'
    });

    /* 2. Przechwycenie dźwięku karty. */
    var display = !!(global.navigator && navigator.mediaDevices &&
      typeof navigator.mediaDevices.getDisplayMedia === 'function');
    var displayOk = display && secure();
    probes.push({
      id: 'display',
      label: 'Przechwycenie dźwięku karty',
      available: displayOk,
      why: !display ? 'Przeglądarka nie ma getDisplayMedia (tak jest na iOS i w Firefoksie).'
        : !secure() ? 'Wymaga adresu https lub localhost — w trybie file:// jest niedostępne.'
        : 'Dostępne, ale wymaga zgody przy każdym uruchomieniu, a mowa systemowa zwykle omija strumień karty.'
    });

    /* 3. Nagranie lektora. */
    probes.push({
      id: 'file',
      label: 'Nagranie w katalogu audio/',
      available: true,
      why: 'Działa zawsze — pełne przetwarzanie na buforze. Wymaga dodania plików.'
    });

    Capture.result = {
      probes: probes,
      /* Silnik buforowy jest dostępny dla nagrań zawsze; dla syntezatora
         wyłącznie wtedy, gdy któraś z dwóch pierwszych dróg zadziała. */
      synthCapture: direct || false,
      canTryDisplay: displayOk,
      webAudio: !!(global.DSP && DSP.supported())
    };
    Capture.checked = true;
    return Capture.result;
  };

  /* Eksperyment uruchamiany ręcznie z Ustawień. Prosi o przechwycenie karty,
     mierzy, czy w strumieniu w ogóle coś słychać w czasie wypowiedzi, i mówi
     wprost, co z tego wyszło. Zwraca obietnicę z opisem wyniku. */
  Capture.tryDisplay = function (sampleText) {
    var res = Capture.probe();
    if (!res.canTryDisplay) {
      return Promise.resolve({ ok: false, message: 'Ta przeglądarka nie pozwala przechwycić dźwięku karty.' });
    }
    return navigator.mediaDevices.getDisplayMedia({ video: true, audio: true })
      .then(function (stream) {
        var tracks = stream.getAudioTracks();
        if (!tracks.length) {
          stop(stream);
          return { ok: false, message: 'Zgoda dotyczyła obrazu bez dźwięku — nie zaznaczono „udostępnij dźwięk”.' };
        }
        return measure(stream, sampleText).then(function (level) {
          stop(stream);
          if (level < 0.002) {
            return {
              ok: false,
              message: 'Strumień działa, ale mowa syntezatora do niego nie trafia — ' +
                'powstaje poza kartą. Zostaje wariant zapasowy.'
            };
          }
          return { ok: true, message: 'Udało się: sygnał mowy jest w strumieniu (poziom ' + level.toFixed(3) + ').' };
        });
      })['catch'](function (err) {
        return { ok: false, message: 'Przechwycenie odrzucone: ' + (err && err.name ? err.name : 'błąd') + '.' };
      });
  };

  function stop(stream) {
    try { stream.getTracks().forEach(function (t) { t.stop(); }); } catch (e) {}
  }

  /* Mierzy szczytowy poziom w strumieniu w czasie krótkiej wypowiedzi. */
  function measure(stream, text) {
    var ctx = DSP.context();
    if (!ctx) return Promise.resolve(0);
    var src = ctx.createMediaStreamSource(stream);
    var an = ctx.createAnalyser();
    an.fftSize = 1024;
    src.connect(an);
    var buf = new Float32Array(an.fftSize);
    var peak = 0;

    return new Promise(function (resolve) {
      var done = false;
      var timer = global.setInterval(function () {
        an.getFloatTimeDomainData(buf);
        for (var i = 0; i < buf.length; i++) {
          var v = Math.abs(buf[i]);
          if (v > peak) peak = v;
        }
      }, 40);
      var finish = function () {
        if (done) return;
        done = true;
        global.clearInterval(timer);
        try { src.disconnect(); } catch (e) {}
        resolve(peak);
      };
      global.setTimeout(finish, 3000);
      if (text && global.Speech && Speech.supported) {
        Speech.speak(text, { onend: function () { global.setTimeout(finish, 200); } });
      }
    });
  }

  global.Capture = Capture;
})(window);
