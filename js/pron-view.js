/* Thai All-in-One — prezentacja oceny wymowy.

   Wykres jest tu ilustracją, nie nośnikiem treści. Ktoś, kto go nie widzi,
   musi dostać dokładnie tę samą informację: dlatego każdy wynik ma opis
   tekstowy, tabelę z liczbami i ocenę słowną mówiącą, co konkretnie zrobić
   inaczej. Sam procent nie uczy niczego — „62%” nie podpowiada, że trzeba
   zejść niżej na drugiej sylabie.

   Oś czasu jest znormalizowana per sylaba: każda sylaba dostaje równy wycinek
   szerokości, a wewnątrz niego kontur rozciąga się na własnym czasie trwania.
   Dzięki temu wzorzec i nagranie leżą jedno na drugim mimo różnego tempa,
   a pionowe linie podziału odpowiadają realnym granicom sylab. */
(function (global) {
  'use strict';

  var PronView = {};

  var W = 340, H = 190, padL = 30, padR = 10, padT = 14, padB = 40;
  var plotW = W - padL - padR, plotH = H - padT - padB;

  function svgEl(name, attrs) {
    var n = document.createElementNS('http://www.w3.org/2000/svg', name);
    Object.keys(attrs || {}).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    return n;
  }

  function yOf(chao) {
    var c = Math.max(0.5, Math.min(5.5, chao));
    return padT + plotH - ((c - 0.5) / 5) * plotH;
  }

  /* Zamienia punkty jednej sylaby na współrzędne w jej wycinku wykresu. */
  function segmentPath(points, slot, slots, span) {
    if (!points || !points.length) return [];
    var start = span && span.startMs !== undefined ? span.startMs : points[0].t * 1000;
    var end = span && span.endMs !== undefined ? span.endMs : points[points.length - 1].t * 1000;
    if (end <= start) end = start + 1;
    var slotW = plotW / slots;
    return points.map(function (p) {
      var w = Math.max(0, Math.min(1, (p.t * 1000 - start) / (end - start)));
      return {
        x: padL + slot * slotW + w * slotW,
        y: yOf(p.c)
      };
    });
  }

  function polyline(pts, cls) {
    return svgEl('polyline', {
      points: pts.map(function (p) { return (Math.round(p.x * 10) / 10) + ',' + (Math.round(p.y * 10) / 10); }).join(' '),
      class: cls
    });
  }

  /* ------------------------------------------------------- opis tekstowy */

  PronView.describe = function (result) {
    if (!result || !result.ok) return result && result.message ? result.message : 'Brak oceny.';
    var parts = [];
    parts.push('Wykres porównuje przebieg wysokości Twojego głosu z wzorcem, w skali od 1 (dół zakresu) do 5 (góra zakresu).');
    parts.push('Wynik ' + result.score + ' na 100, ' + result.grade + '. Trafionych tonów: '
      + result.hits + ' z ' + result.total + '.');
    result.syllables.forEach(function (s) {
      var line = 'Sylaba ' + (s.index + 1) + ', ' + s.label + ': wzorzec ton ' + s.expectedTone + ', ';
      line += s.producedTone ? ('Twój ton ' + s.producedTone) : 'Twojego tonu nie dało się odczytać';
      line += s.ok ? ' — zgodnie' : ' — niezgodnie';
      if (s.measured) line += ', czas ' + s.measured.voicedMs + ' milisekund';
      if (s.lengthVerdict && s.lengthVerdict !== 'w porządku') {
        line += ', samogłoska ' + s.lengthVerdict;
      }
      parts.push(line + '.');
    });
    if (result.distance !== null) {
      parts.push('Odległość konturów po wyrównaniu czasowym: ' + String(result.distance).replace('.', ',')
        + ' stopnia skali.');
    }
    return parts.join(' ');
  };

  /* ------------------------------------------------------------- wykres */

  PronView.chart = function (result) {
    var fig = U.el('figure', { class: 'chart-block pron-chart-block' });
    var n = result.syllables.length || 1;

    var svg = svgEl('svg', {
      viewBox: '0 0 ' + W + ' ' + H,
      class: 'pron-chart',
      role: 'img',
      'aria-label': PronView.describe(result)
    });

    /* Siatka poziomów Chao. Podpisy słowne, nie tylko cyfry — „4” samo
       w sobie nic nie znaczy dla kogoś, kto pierwszy raz widzi tę skalę. */
    [[5, 'góra'], [4, ''], [3, 'środek'], [2, ''], [1, 'dół']].forEach(function (row) {
      var y = yOf(row[0]);
      svg.appendChild(svgEl('line', { x1: padL, y1: y, x2: W - padR, y2: y, class: 'grid' }));
      var t = svgEl('text', { x: padL - 5, y: y + 3.5, class: 'axis', 'text-anchor': 'end' });
      t.textContent = row[1] ? (row[0] + ' ' + row[1]) : String(row[0]);
      svg.appendChild(t);
    });

    /* Granice sylab i podpisy pod osią. */
    var slotW = plotW / n;
    result.syllables.forEach(function (s, i) {
      if (i > 0) {
        svg.appendChild(svgEl('line', {
          x1: padL + i * slotW, y1: padT, x2: padL + i * slotW, y2: padT + plotH, class: 'sylline'
        }));
      }
      var cx = padL + (i + 0.5) * slotW;
      var lab = svgEl('text', { x: cx, y: H - padB + 14, class: 'axis syl', 'text-anchor': 'middle' });
      lab.textContent = s.plain;
      svg.appendChild(lab);
      var tone = svgEl('text', {
        x: cx, y: H - padB + 26,
        class: 'axis' + (s.ok ? ' good' : ' miss'), 'text-anchor': 'middle'
      });
      tone.textContent = s.ok ? s.expectedTone : (s.expectedTone + ' ≠ ' + (s.producedTone || '?'));
      svg.appendChild(tone);
    });

    /* Wzorzec — linia przerywana. Nagranie — linia ciągła z punktami.
       Rozróżnienie nie opiera się wyłącznie na kolorze. */
    result.syllables.forEach(function (s, i) {
      var refPts = segmentPath(s.refPoints, i, n, (result.reference.syllables[i] || null));
      if (refPts.length > 1) svg.appendChild(polyline(refPts, 'ref-line'));
      var usrPts = segmentPath(s.userPoints, i, n, s.measured);
      if (usrPts.length > 1) {
        svg.appendChild(polyline(usrPts, 'user-line' + (s.ok ? '' : ' miss')));
        svg.appendChild(svgEl('circle', { cx: usrPts[0].x, cy: usrPts[0].y, r: 2.6, class: 'user-dot' }));
      } else if (!usrPts.length) {
        var q = svgEl('text', {
          x: padL + (i + 0.5) * slotW, y: padT + plotH / 2, class: 'axis miss', 'text-anchor': 'middle'
        });
        q.textContent = 'brak głosu';
        svg.appendChild(q);
      }
    });

    fig.appendChild(svg);

    var legend = U.el('p', { class: 'chart-legend muted' });
    legend.appendChild(U.el('span', { class: 'key key-ref', 'aria-hidden': 'true' }));
    legend.appendChild(document.createTextNode(' wzorzec (linia przerywana) \u00a0 '));
    legend.appendChild(U.el('span', { class: 'key key-user', 'aria-hidden': 'true' }));
    legend.appendChild(document.createTextNode(' Twoje nagranie (linia ciągła)'));
    fig.appendChild(legend);

    return fig;
  };

  /* ------------------------------------------------------------- tabela */

  PronView.table = function (result) {
    var table = U.el('table', { class: 'data-table' });
    table.appendChild(U.el('caption', { text: 'Ocena sylaba po sylabie' }));
    var thead = U.el('thead');
    var hr = U.el('tr');
    ['Sylaba', 'Ton wzorcowy', 'Twój ton', 'Zgodność', 'Samogłoska', 'Czas'].forEach(function (h) {
      hr.appendChild(U.el('th', { scope: 'col', text: h }));
    });
    thead.appendChild(hr);
    table.appendChild(thead);

    var tbody = U.el('tbody');
    result.syllables.forEach(function (s) {
      var tr = U.el('tr', { class: s.ok ? '' : 'row-miss' });
      tr.appendChild(U.el('th', { scope: 'row', text: s.label }));
      tr.appendChild(U.el('td', { text: s.expectedTone }));
      tr.appendChild(U.el('td', { text: s.producedTone || 'nie odczytano' }));
      tr.appendChild(U.el('td', { text: s.ok ? 'zgodny' : 'inny' }));
      tr.appendChild(U.el('td', {
        text: s.expectedLength
          ? ((s.expectedLength === 'long' ? 'długa' : 'krótka')
             + (s.lengthVerdict && s.lengthVerdict !== 'w porządku' ? ' — ' + s.lengthVerdict : ' — w porządku'))
          : 'nie oceniana'
      }));
      tr.appendChild(U.el('td', { text: s.measured ? s.measured.voicedMs + ' ms' : '—' }));
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    return table;
  };

  /* -------------------------------------------------------- całość oceny */

  var GRADE_TEXT = {
    'trafnie': 'Tony się zgadzają.',
    'blisko': 'Blisko — większość tonów trafiona, ale nie wszystkie.',
    'do poprawy': 'Tony wymagają poprawy.'
  };

  /* opts: { compact: true } — zwarta wersja do listy kwestii w dialogu. */
  PronView.render = function (result, opts) {
    opts = opts || {};
    var box = U.el('div', { class: 'pron-result' });

    if (!result || !result.ok) {
      box.appendChild(U.el('p', { class: 'fb bad', role: 'status',
        text: (result && result.message) || 'Nie udało się ocenić tego nagrania.' }));
      return box;
    }

    var head = U.el('p', { class: 'pron-head ' + (result.grade === 'trafnie' ? 'ok' : (result.grade === 'blisko' ? 'near' : 'bad')), role: 'status' });
    head.appendChild(U.el('strong', { text: GRADE_TEXT[result.grade] + ' ' }));
    head.appendChild(document.createTextNode(
      result.hits + ' z ' + result.total + ' '
      + U.plural(result.total, 'tonu trafiony', 'tonów trafione', 'tonów trafionych')
      + ' · wynik ' + result.score + '/100.'));
    box.appendChild(head);

    if (!opts.compact) {
      box.appendChild(PronView.chart(result));
      box.appendChild(PronView.table(result));
    }

    if (result.advice.length) {
      var h = U.el('p', { class: 'muted', text: opts.compact ? 'Co poprawić:' : 'Co konkretnie poprawić:' });
      box.appendChild(h);
      var ul = U.el('ul', { class: 'advice-list' });
      result.advice.slice(0, opts.compact ? 2 : 6).forEach(function (a) {
        ul.appendChild(U.el('li', { text: a }));
      });
      box.appendChild(ul);
    }

    if (!opts.compact) {
      box.appendChild(U.el('p', { class: 'muted small', text: PronView.footnote(result) }));
    }
    return box;
  };

  /* Uczciwa nota pod wynikiem: skąd wzorzec i na ile skala jest już dopasowana
     do głosu tej osoby. Bez tego liczba na górze udaje większą pewność, niż ma. */
  PronView.footnote = function (result) {
    var parts = [];
    parts.push(result.reference.source === 'lektor'
      ? 'Wzorzec policzony z nagrania lektora tym samym algorytmem co Twoje nagranie.'
      : 'Wzorzec modelowy, zbudowany z zapisu tonów — opisuje ton wzorcowy w izolacji, '
        + 'bez melodii całego zdania.');
    if (result.normalisation.personalised) {
      parts.push('Skala dopasowana do Twojego głosu: środek ' + result.normalisation.centre
        + ' Hz, zakres ±' + String(result.normalisation.halfSpan).replace('.', ',')
        + ' półtonu, z ' + result.normalisation.samples + ' '
        + U.plural(result.normalisation.samples, 'nagrania', 'nagrań', 'nagrań') + '.');
    } else {
      parts.push('Skala liczona z tego jednego nagrania — po trzech nagraniach aplikacja '
        + 'pozna Twój zakres głosu i ocena będzie dokładniejsza.');
    }
    if (result.distance !== null) {
      parts.push('Odległość konturów po wyrównaniu czasowym: '
        + String(result.distance).replace('.', ',') + ' stopnia skali (0 = pokrywają się).');
    }
    parts.push('Czas analizy: ' + result.analysis.analysisMs + ' ms.');
    return parts.join(' ');
  };

  /* Przykładowy wynik — używany przez tools/a11y-check.py i function-test.py,
     żeby dało się sprawdzić kartę oceny bez dostępu do mikrofonu. */
  PronView.sampleResult = function () {
    var rec = { thaiPhonetic: 'khàwp-khun mâak', syllables: ['khàwp', 'khun', 'mâak'] };
    var expected = ToneScore.expected(rec.thaiPhonetic, rec.syllables);
    var ref = ToneScore.modelContour(expected);
    var syl = expected.map(function (e, i) {
      var span = ref.syllables[i];
      var produced = i === 2 ? 'średni' : e.tone;
      var pts = (ToneScore.SHAPES[produced] || ToneScore.SHAPES['średni']).map(function (c, k, arr) {
        return { t: (span.startMs + span.durationMs * k / (arr.length - 1)) / 1000, c: c };
      });
      return {
        index: i, label: e.label, plain: e.plain,
        expectedTone: e.tone, producedTone: produced,
        confidence: 0.8, ok: produced === e.tone,
        measured: { startMs: span.startMs, endMs: span.endMs,
                    durationMs: span.durationMs, voicedMs: span.durationMs, voicedFrames: 12 },
        userPoints: pts, refPoints: span.points,
        expectedLength: e.lengthConfident ? e.length : null,
        lengthVerdict: i === 2 ? 'za krótka' : (e.lengthConfident ? 'w porządku' : null),
        lengthRatio: 1,
        fix: produced === e.tone ? '' : ToneScore.fix(produced, e.tone)
      };
    });
    return {
      ok: true, empty: false, score: 71, grade: 'blisko',
      hits: 2, total: 3, distance: 0.74,
      syllables: syl, expected: expected,
      user: { centre: 132, halfSpan: 4, personalised: true, samples: 7, points: [] },
      reference: { points: ref.points, syllables: ref.syllables, source: 'model' },
      normalisation: { centre: 132, halfSpan: 4, personalised: true, samples: 7, offset: 0 },
      advice: [syl[2].fix, 'mâak: samogłoska jest tu długa — przeciągnij ją mniej więcej dwa razy dłużej niż krótką. W tajskim długość odróżnia słowa tak samo jak ton.'],
      analysis: { analysisMs: 48, voicedRatio: 0.62, duration: 1.1 }
    };
  };

  /* ================================================ STEROWNIK NAGRYWANIA

     Jeden przycisk, jedna ścieżka: nagranie -> analiza F0 -> ocena -> wykres.
     Używają go trzy miejsca (Wymowa hasła, role-play, „Wymów poprawnie”),
     więc obsługa mikrofonu, komunikaty o braku dostępu i pomiar czasu reakcji
     są napisane raz. */

  var active = null;   // jednocześnie nagrywa tylko jedno miejsce

  PronView.stopAll = function () {
    if (active) { try { active(); } catch (e) {} active = null; }
  };

  PronView.canRecord = function () {
    return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && global.MediaRecorder);
  };

  PronView.micMessage = function () {
    if (DB.localMode) {
      return 'Nagrywanie wymaga uruchomienia aplikacji przez serwer lub adres https — '
        + 'przy otwarciu prosto z dysku przeglądarka blokuje mikrofon. '
        + 'Reszta ekranu działa normalnie: możesz odsłuchać wzór i powtarzać na głos.';
    }
    return 'Ta przeglądarka nie pozwala nagrywać dźwięku, więc ocena wymowy jest niedostępna. '
      + 'Możesz ćwiczyć, powtarzając wzór na głos.';
  };

  /* Kontur wzorcowy z nagrania lektora, jeśli hasło je ma. Wynik trzymamy
     w pamięci — analiza tego samego pliku przy każdej próbie byłaby czystą
     stratą czasu. */
  var refCache = {};
  PronView.reference = function (rec) {
    if (!rec || !rec.audioFile || DB.localMode || !Pitch.supported) return Promise.resolve(null);
    if (refCache[rec.audioFile] !== undefined) return Promise.resolve(refCache[rec.audioFile]);
    return Pitch.fromUrl('audio/' + rec.audioFile).then(function (a) {
      refCache[rec.audioFile] = a;
      return a;
    })['catch'](function () {
      refCache[rec.audioFile] = null;
      return null;
    });
  };

  /* opts:
       promptAt   — znacznik czasu pokazania polecenia (do pomiaru reakcji),
       compact    — zwarta karta wyniku (lista kwestii w dialogu),
       label      — napis na przycisku,
       maxMs      — twardy limit nagrania,
       onResult(result, meta) — meta: { blob, url, reactionMs, speakMs } */
  PronView.control = function (rec, opts) {
    opts = opts || {};
    var wrap = U.el('div', { class: 'pron-control' });
    var out = U.el('div', { class: 'pron-inline' });

    var recBtn = U.el('button', {
      class: 'btn', type: 'button',
      text: opts.label || 'Nagraj siebie i oceń'
    });
    var playBtn = U.el('button', {
      class: 'btn ghost', type: 'button', text: 'Odsłuchaj nagranie', disabled: 'disabled'
    });
    var row = U.el('div', { class: 'btn-row' }, [recBtn, playBtn]);
    wrap.appendChild(row);

    var status = U.el('p', { class: 'muted', role: 'status' });
    var meter = U.el('div', { class: 'meter', 'aria-hidden': 'true' });
    var meterFill = U.el('i');
    meter.appendChild(meterFill);
    var statusRow = U.el('div', { class: 'rec-status' }, [status, meter]);
    wrap.appendChild(statusRow);
    wrap.appendChild(out);

    if (!PronView.canRecord() || !Pitch.supported) {
      recBtn.disabled = true;
      status.textContent = PronView.micMessage();
      return wrap;
    }

    var state = { recorder: null, stream: null, url: null, ctx: null, raf: null, startedAt: 0 };

    function cleanup() {
      if (state.raf) { cancelAnimationFrame(state.raf); state.raf = null; }
      if (state.stream) {
        state.stream.getTracks().forEach(function (t) { t.stop(); });
        state.stream = null;
      }
      if (state.ctx) { try { state.ctx.close(); } catch (e) {} state.ctx = null; }
      meterFill.style.width = '0%';
      recBtn.classList.remove('recording');
      /* Zachowujemy dopisek z etykiety, żeby po nagraniu nadal było wiadomo,
         której kwestii dotyczy przycisk — inaczej w dialogu z sześcioma
         kwestiami wszystkie nazywałyby się tak samo. */
      recBtn.textContent = 'Nagraj ponownie'
        + (opts.label ? opts.label.replace(/^Nagraj/, '') : ' i oceń');
      active = null;
    }

    function stop() {
      if (state.recorder && state.recorder.state === 'recording') state.recorder.stop();
      else cleanup();
    }
    wrap.stopRecording = stop;

    /* Wskaźnik poziomu. Bez niego najczęstsza przyczyna złej oceny — mówienie
       za cicho albo za daleko od mikrofonu — jest dla użytkownika niewidoczna. */
    function watchLevel(stream) {
      var C = global.AudioContext || global.webkitAudioContext;
      if (!C) return;
      try {
        state.ctx = new C();
        var src = state.ctx.createMediaStreamSource(stream);
        var an = state.ctx.createAnalyser();
        an.fftSize = 1024;
        src.connect(an);
        var buf = new Float32Array(an.fftSize);
        var tick = function () {
          an.getFloatTimeDomainData(buf);
          var sum = 0;
          for (var i = 0; i < buf.length; i++) sum += buf[i] * buf[i];
          var rms = Math.sqrt(sum / buf.length);
          meterFill.style.width = Math.min(100, Math.round(rms * 320)) + '%';
          state.raf = requestAnimationFrame(tick);
        };
        tick();
      } catch (e) { /* wskaźnik jest dodatkiem — brak go nie psuje nagrywania */ }
    }

    function evaluate(blob, speakMs, reactionMs) {
      status.textContent = 'Liczę kontur wysokości dźwięku…';
      U.clear(out);
      Pitch.fromBlob(blob).then(function (analysis) {
        return PronView.reference(rec).then(function (reference) {
          var result = ToneScore.evaluate(rec, analysis, reference);
          if (result.ok) ToneScore.observe(analysis);
          status.textContent = result.ok
            ? ('Ocena gotowa — analiza zajęła ' + analysis.analysisMs + ' ms.')
            : '';
          U.clear(out).appendChild(PronView.render(result, { compact: opts.compact }));
          if (opts.onResult) opts.onResult(result, { blob: blob, url: state.url,
                                                     reactionMs: reactionMs, speakMs: speakMs });
        });
      })['catch'](function (err) {
        status.textContent = '';
        U.clear(out).appendChild(U.el('p', { class: 'fb bad', role: 'status',
          text: 'Nie udało się przeanalizować nagrania: ' + (err && err.message ? err.message : 'nieznany błąd') + '.' }));
        if (opts.onResult) opts.onResult(null, { error: err });
      });
    }

    recBtn.addEventListener('click', function () {
      if (state.recorder && state.recorder.state === 'recording') { stop(); return; }
      Player.stop();
      PronView.stopAll();
      var reactionMs = opts.promptAt ? (Date.now() - opts.promptAt) : null;

      navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
        state.stream = stream;
        var chunks = [];
        state.recorder = new MediaRecorder(stream);
        state.startedAt = Date.now();
        state.recorder.ondataavailable = function (e) { if (e.data.size) chunks.push(e.data); };
        state.recorder.onstop = function () {
          var speakMs = Date.now() - state.startedAt;
          var blob = new Blob(chunks, { type: state.recorder.mimeType || 'audio/webm' });
          if (state.url) URL.revokeObjectURL(state.url);
          state.url = URL.createObjectURL(blob);
          playBtn.disabled = false;
          cleanup();
          if (speakMs < 250 || !blob.size) {
            status.textContent = 'Nagranie było za krótkie. Naciśnij, powiedz zwrot i naciśnij ponownie.';
            return;
          }
          evaluate(blob, speakMs, reactionMs);
        };
        state.recorder.start();
        active = stop;
        watchLevel(stream);
        recBtn.classList.add('recording');
        recBtn.textContent = 'Zatrzymaj nagrywanie';
        status.textContent = 'Nagrywam… powiedz zwrot i naciśnij ponownie.';
        U.clear(out);
        setTimeout(function () {
          if (state.recorder && state.recorder.state === 'recording') stop();
        }, opts.maxMs || 12000);
      })['catch'](function () {
        status.textContent = 'Brak zgody na dostęp do mikrofonu. Możesz jej udzielić w ustawieniach przeglądarki.';
      });
    });

    playBtn.addEventListener('click', function () {
      if (!state.url) return;
      Player.stop();
      var el = new Audio(state.url);
      el.play()['catch'](function () {
        U.toast('Nie udało się odtworzyć nagrania.');
      });
    });

    return wrap;
  };

  global.PronView = PronView;
})(window);
