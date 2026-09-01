/* Thai All-in-One — moduł liczbowy.

   Liczby w mowie nie są podzbiorem słownictwa. Uczący się może znać wszystkie
   dziesięć cyfr i mimo to nie wyłapać ceny powiedzianej w tempie kasjera —
   bo to jest umiejętność percepcyjna, a nie pamięciowa. Mierzy się ją CZASEM
   REAKCJI, nie liczbą znanych haseł, i dlatego ten moduł ma własne ćwiczenia,
   własną statystykę i własny próg opanowania.

   SILNIK
   ------
   Liczba nie jest wyszukiwana w danych — jest składana regułą, tą samą, którą
   liczy `tools/generators/thai_numbers.py`. Gdyby każda liczba musiała mieć
   wpis w pliku, plik miałby milion pozycji; a ćwiczenie i tak musiałoby umieć
   wygenerować tę jedną, której akurat brakuje. Plik trzyma więc ATOMY (cyfry,
   pozycje, èt, yîi, láan) i punkty kontrolne, a resztę robi arytmetyka.

   Pismo tajskie składamy przez DB.composeVoice(), które łączy ukryte teksty
   atomów i zwraca nowy token. Znaki tajskie nie opuszczają prywatnej mapy
   w data-loaderze ani na chwilę — tak samo jak przy każdym innym haśle. */
(function (global) {
  'use strict';

  var Numbers = { ready: false, drill: null };

  Numbers.ensureData = function () { return DB.ensureNumbers(); };
  Numbers.loaded = function () { return !!(DB.numbers && DB.numbers.atoms); };

  function data() { return DB.numbers || null; }

  /* ------------------------------------------------------------ silnik */

  function atoms() { return data().atoms; }

  /* Człony liczby 1..999 999 jako pary { ph, key }. Trzy nieregularności
     siedzą właśnie tutaj i nigdzie indziej:
       - dziesiątka „1” jest niema (sìp, nie nùeng-sìp),
       - dziesiątka „2” to yîi-sìp, nigdy sǎwng-sìp,
       - jedność „1” po czymkolwiek to èt, nie nùeng. */
  function partsBelowMillion(n) {
    var a = atoms(), out = [], rest = n;
    a.positions.forEach(function (pos) {
      var d = Math.floor(rest / pos.value);
      rest -= d * pos.value;
      if (!d) return;
      if (pos.value === 10) {
        if (d === 1) out.push({ ph: pos.thaiPhonetic, key: pos.ttsKey });
        else if (d === 2) out.push({ ph: a.yii.thaiPhonetic + '-' + pos.thaiPhonetic,
                                     key: [a.yii.ttsKey, pos.ttsKey] });
        else out.push({ ph: a.digits[d].thaiPhonetic + '-' + pos.thaiPhonetic,
                        key: [a.digits[d].ttsKey, pos.ttsKey] });
      } else {
        out.push({ ph: a.digits[d].thaiPhonetic + '-' + pos.thaiPhonetic,
                   key: [a.digits[d].ttsKey, pos.ttsKey] });
      }
    });
    if (rest) {
      if (rest === 1 && out.length) out.push({ ph: a.et.thaiPhonetic, key: a.et.ttsKey });
      else out.push({ ph: a.digits[rest].thaiPhonetic, key: a.digits[rest].ttsKey });
    }
    return out;
  }

  Numbers.MAX = 1000000;

  /* Zwraca { thaiPhonetic, ttsKey } dla liczby całkowitej 0..1 000 000. */
  Numbers.say = function (n) {
    if (!Numbers.loaded()) return null;
    if (typeof n !== 'number' || n % 1 !== 0 || n < 0 || n > Numbers.MAX) return null;
    var a = atoms();
    if (n === 0) return pack([{ ph: a.digits[0].thaiPhonetic, key: a.digits[0].ttsKey }]);

    var chunks = [];
    var millions = Math.floor(n / 1000000);
    if (millions) {
      chunks = chunks.concat(millions > 1 ? partsBelowMillion(millions)
        : [{ ph: a.digits[1].thaiPhonetic, key: a.digits[1].ttsKey }]);
      chunks.push({ ph: a.million.thaiPhonetic, key: a.million.ttsKey });
    }
    chunks = chunks.concat(partsBelowMillion(n % 1000000));
    return pack(chunks);
  };

  function pack(chunks) {
    var keys = [];
    chunks.forEach(function (c) {
      if (Array.isArray(c.key)) keys = keys.concat(c.key);
      else keys.push(c.key);
    });
    return {
      thaiPhonetic: chunks.map(function (c) { return c.ph; }).join('-'),
      ttsKey: DB.composeVoice(keys)
    };
  }

  /* Droga powrotna. Sama generacja niczego nie dowodzi — reguła może być
     wewnętrznie spójna i konsekwentnie błędna. Test działania sprawdza, że
     parse(say(n)) === n dla całego zakresu; błąd, który to przeżyje, musiałby
     być popełniony dwa razy w przeciwnych kierunkach. */
  Numbers.parse = function (text) {
    if (!Numbers.loaded() || !text) return null;
    var a = atoms();
    var unit = {}, posv = {};
    a.digits.forEach(function (d, i) { unit[d.thaiPhonetic] = i; });
    a.positions.forEach(function (p) { posv[p.thaiPhonetic] = p.value; });

    var syls = String(text).trim().split(/[\s\-]+/).filter(Boolean);
    var total = 0, group = 0, pending = null, seen = false;
    for (var i = 0; i < syls.length; i++) {
      var s = syls[i];
      if (s === a.million.thaiPhonetic) {
        if (pending !== null) { group += pending; pending = null; }
        if (!group) return null;
        total += group * 1000000; group = 0; seen = true; continue;
      }
      if (s === a.yii.thaiPhonetic) {
        if (pending !== null) return null;
        pending = 2; seen = true; continue;
      }
      if (s === a.et.thaiPhonetic) {
        if (pending !== null) return null;
        group += 1; seen = true; continue;
      }
      if (Object.prototype.hasOwnProperty.call(posv, s)) {
        var v = posv[s];
        if (v !== 10 && pending === null) return null;
        group += (pending === null ? 1 : pending) * v;
        pending = null; seen = true; continue;
      }
      if (Object.prototype.hasOwnProperty.call(unit, s)) {
        if (pending !== null) return null;
        pending = unit[s]; seen = true; continue;
      }
      return null;
    }
    if (pending !== null) group += pending;
    return seen ? total + group : null;
  };

  /* Element gotowy do podania odtwarzaczowi: liczba plus jednostka. */
  Numbers.item = function (n, unitRecordId) {
    var said = Numbers.say(n);
    if (!said) return null;
    var out = { thaiPhonetic: said.thaiPhonetic, ttsKey: said.ttsKey, polish: String(n) };
    if (unitRecordId) {
      var u = recordById(unitRecordId);
      if (u) {
        out.thaiPhonetic += ' ' + u.thaiPhonetic;
        out.ttsKey = DB.composeVoice([said.ttsKey, u.ttsKey]);
      }
    }
    return out;
  };

  function recordById(id) {
    var recs = (data() && data().records) || [];
    for (var i = 0; i < recs.length; i++) if (recs[i].id === id) return recs[i];
    return null;
  }
  Numbers.record = recordById;

  Numbers.section = function (id) {
    return ((data() && data().records) || []).filter(function (r) { return r.section === id; });
  };

  Numbers.lessons = function () { return (data() && data().lessons) || []; };
  Numbers.scenes = function () { return (data() && data().scenes) || []; };
  Numbers.drills = function () { return (data() && data().drills) || []; };
  Numbers.drillDef = function (id) {
    var list = Numbers.drills();
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  };

  /* --------------------------------------------------- limit czasu

     Ćwiczenie liczbowe mierzy szybkość, więc limit czasu jest jego treścią,
     a nie ozdobą. To jednak nie znaczy, że limit ma być nieusuwalny: ktoś
     z ograniczeniem ruchowym albo korzystający z czytnika ekranu potrzebuje
     na samo wpisanie odpowiedzi więcej czasu niż wynosi całe okno — i wtedy
     ćwiczenie nie mierzy już percepcji, tylko sprawność motoryczną.

     Mnożnik jest w ustawieniach i obejmuje WSZYSTKIE ćwiczenia z limitem
     w aplikacji, także dryl odruchu. Wyłączenie limitu nie unieważnia pomiaru
     czasu — czas nadal jest mierzony i pokazywany, przestaje tylko odcinać
     odpowiedź. Rozdzielenie tych dwóch rzeczy jest tu istotne: mierzyć da się
     bez presji, karać bez pomiaru już nie. */
  var LIMIT_CHOICES = [
    { id: 'normal', label: 'standardowy', factor: 1 },
    { id: 'long', label: 'półtora raza dłuższy', factor: 1.5 },
    { id: 'double', label: 'dwa razy dłuższy', factor: 2 },
    { id: 'triple', label: 'trzy razy dłuższy', factor: 3 },
    { id: 'off', label: 'bez limitu', factor: 0 }
  ];
  Numbers.limitChoices = function () { return LIMIT_CHOICES.slice(); };

  Numbers.limitMode = function () {
    var s = U.store.get('settings', {});
    return s.timeLimit || 'normal';
  };

  Numbers.limitFactor = function () {
    var mode = Numbers.limitMode();
    for (var i = 0; i < LIMIT_CHOICES.length; i++) {
      if (LIMIT_CHOICES[i].id === mode) return LIMIT_CHOICES[i].factor;
    }
    return 1;
  };

  /* Limit dla konkretnego ćwiczenia. 0 znaczy „bez odliczania”. */
  Numbers.limitMs = function (baseMs) {
    var f = Numbers.limitFactor();
    return f ? Math.round(baseMs * f) : 0;
  };

  Numbers.limitNote = function (baseMs) {
    var ms = Numbers.limitMs(baseMs);
    if (!ms) return 'Limit czasu wyłączony. Czas reakcji jest nadal mierzony '
      + 'i liczy się do statystyk — nie przerywa tylko odpowiedzi.';
    var f = Numbers.limitFactor();
    return 'Limit: ' + (ms / 1000).toFixed(1).replace('.', ',') + ' s'
      + (f !== 1 ? ' (wydłużony ' + f + '×)' : '')
      + '. Możesz go wydłużyć albo wyłączyć w Ustawieniach.';
  };

  /* ----------------------------------------------------- zegar ćwiczenia

     Jeden licznik dla wszystkich trybów. Odlicza w dół, ogłasza koniec przez
     aria-live i wywołuje przekazane domknięcie. Przy limicie wyłączonym
     pokazuje czas, który upłynął, zamiast czasu, który został — bo liczba
     rosnąca do góry nie wywiera presji, a informację niesie tę samą. */
  function Countdown(box, ms, onTimeout) {
    var self = this;
    this.limit = ms;
    this.start = Date.now();
    this.done = false;
    this.bar = U.el('div', { class: 'num-timer' });
    this.text = U.el('span', { class: 'num-timer-text', role: 'timer',
      'aria-live': 'off' });
    this.fill = U.el('span', { class: 'num-timer-fill' });
    this.bar.appendChild(this.fill);
    this.bar.appendChild(this.text);
    box.appendChild(this.bar);
    this.tick = function () {
      if (self.done) return;
      var passed = Date.now() - self.start;
      if (!self.limit) {
        self.text.textContent = (passed / 1000).toFixed(1).replace('.', ',') + ' s';
      } else {
        var left = Math.max(0, self.limit - passed);
        self.text.textContent = (left / 1000).toFixed(1).replace('.', ',') + ' s';
        self.fill.style.width = Math.round(100 * left / self.limit) + '%';
        if (left <= 0) { self.stop(); onTimeout && onTimeout(); return; }
      }
      self.timer = setTimeout(self.tick, 100);
    };
    this.tick();
  }
  Countdown.prototype.elapsed = function () { return Date.now() - this.start; };
  Countdown.prototype.stop = function () {
    this.done = true;
    clearTimeout(this.timer);
    this.bar.classList.add('stopped');
  };
  Numbers.Countdown = Countdown;

  /* ------------------------------------------------------------ losowanie

     Rozkład jest celowo nierównomierny. Liczby do stu padają w rozmowie
     nieporównanie częściej niż sześciocyfrowe, a nieregularności skupiają się
     w zakresie 11–99 — losowanie równomierne z całego miliona dawałoby
     ćwiczenie prawie wyłącznie na regularnej części systemu, czyli na tej,
     która nikomu nie sprawia kłopotu. */
  function pickNumber(level) {
    var r = Math.random();
    if (level === 'low') return Math.floor(Math.random() * 21);
    if (level === 'mid') {
      if (r < 0.55) return 10 + Math.floor(Math.random() * 90);
      return Math.floor(Math.random() * 1000);
    }
    if (r < 0.35) return 10 + Math.floor(Math.random() * 90);
    if (r < 0.65) return Math.floor(Math.random() * 1000);
    if (r < 0.85) return Math.floor(Math.random() * 100000);
    return Math.floor(Math.random() * (Numbers.MAX + 1));
  }
  Numbers.pickNumber = pickNumber;

  function levelForUser() {
    var done = Progress.numberStats().answers;
    if (done < 20) return 'low';
    if (done < 60) return 'mid';
    return 'high';
  }

  /* --------------------------------------------------------- wspólny szkielet */

  function header(box, def) {
    box.appendChild(U.el('p', { class: 'muted', text: def.lead }));
    box.appendChild(U.el('p', { class: 'muted small', text: Numbers.limitNote(def.limitMs) }));
  }

  function playBtn(label, item, opts) {
    var btn = U.el('button', { class: 'btn gold play-btn', type: 'button',
      'aria-pressed': 'false' });
    btn.appendChild(U.icon('play'));
    btn.appendChild(U.el('span', { text: label }));
    btn.addEventListener('click', function () {
      Player.play(item, Object.assign({ btn: btn }, opts || {}));
    });
    return btn;
  }

  /* Wynik jednego zadania. Czas reakcji jest tu główną miarą, nie dodatkiem:
     liczba odczytana poprawnie po sześciu sekundach w kasie nie zadziałała. */
  function finish(box, ctx, ok, correctText, extra) {
    ctx.clock.stop();
    var ms = ctx.clock.elapsed();
    var timedOut = ctx.timedOut;
    var fb = U.el('p', { class: ok ? 'fb ok' : 'fb bad', role: 'status' });
    fb.appendChild(U.el('strong', { text: timedOut ? 'Czas minął. '
      : (ok ? 'Dobrze. ' : 'Nie. ') }));
    fb.appendChild(document.createTextNode(ok ? '' : ('Było: ' + correctText + '.')));
    box.appendChild(fb);
    if (extra) box.appendChild(extra);

    var verdict = Progress.numberAnswer(ctx.mode, ok, ms, {
      value: ctx.value, timedOut: !!timedOut
    });
    box.appendChild(U.el('p', { class: 'muted', text:
      'Czas reakcji: ' + (ms / 1000).toFixed(1).replace('.', ',') + ' s. '
      + verdict.note }));

    var next = U.el('button', { class: 'btn', type: 'button', text: 'Następne' });
    next.addEventListener('click', ctx.onNext);
    box.appendChild(U.el('div', { class: 'btn-row' }, [next]));
    next.focus();
  }

  /* =================================================== 1. DYKTANDO LICZBOWE */

  Numbers.renderDictation = function (box, onNext) {
    var def = Numbers.drillDef('dictation');
    header(box, def);
    var n = pickNumber(levelForUser());
    var said = Numbers.say(n);
    if (!said) { box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję…' })); return; }

    box.appendChild(U.el('p', { text: 'Posłuchaj i wpisz liczbę cyframi.' }));
    var item = { thaiPhonetic: said.thaiPhonetic, ttsKey: said.ttsKey };
    var play = playBtn('Odtwórz liczbę', item, { tempo: CompTempo.current });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play]));

    var field = U.el('input', { type: 'text', inputmode: 'numeric', id: 'num-dict-in',
      autocomplete: 'off', class: 'num-input' });
    box.appendChild(U.el('label', { class: 'sr-only', for: 'num-dict-in',
      text: 'Wpisz usłyszaną liczbę cyframi' }));
    box.appendChild(field);

    var ctx = { mode: 'dictation', value: n, onNext: onNext, timedOut: false };
    var answered = false;
    function submit(auto) {
      if (answered) return;
      answered = true;
      ctx.timedOut = !!auto;
      var got = parseInt(String(field.value).replace(/\s/g, ''), 10);
      var ok = !auto && got === n;
      field.disabled = true;
      var hint = U.el('p', { class: 'muted' });
      hint.appendChild(U.el('span', { text: 'Zapis: ' }));
      hint.appendChild(U.renderPhonetic(said.thaiPhonetic, {}));
      finish(box, ctx, ok, String(n), hint);
    }
    ctx.clock = new Countdown(box, Numbers.limitMs(def.limitMs), function () { submit(true); });

    var check = U.el('button', { class: 'btn gold', type: 'button', text: 'Sprawdź' });
    check.addEventListener('click', function () { submit(false); });
    field.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); submit(false); }
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [check]));
    box.appendChild(CompTempo.row('numbers', function () { onNext(); }));
    Player.play(item, { btn: play, tempo: CompTempo.current });
    field.focus();
  };

  /* ======================================================= 2. CENA ZE SŁUCHU */

  var NOTES = [20, 50, 100, 500, 1000];

  Numbers.renderPrice = function (box, onNext) {
    var def = Numbers.drillDef('price');
    header(box, def);
    var unit = Numbers.section('prices').filter(function (r) {
      return (r.meta || {}).unit === 'baht';
    })[0];
    var amount = NOTES[Math.floor(Math.random() * NOTES.length)];
    var exact = Math.random() < 0.5;
    var n = exact ? amount : amount + [5, 10, 20, 30, 50][Math.floor(Math.random() * 5)];
    var item = Numbers.item(n, unit ? unit.id : null);
    if (!item) { box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję…' })); return; }

    box.appendChild(U.el('p', { text: 'Posłuchaj kwoty i wskaż, ile masz zapłacić.' }));
    var play = playBtn('Odtwórz kwotę', item, { tempo: CompTempo.current });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play]));

    var options = U.shuffle([n, n + 10, n * 10 <= Numbers.MAX ? n * 10 : n + 100,
      Math.max(1, n - 10)].filter(function (v, i, arr) { return arr.indexOf(v) === i; }));
    var ctx = { mode: 'price', value: n, onNext: onNext, timedOut: false };
    var answered = false;
    var list = U.el('div', { class: 'options' });

    function settle(choice, auto) {
      if (answered) return;
      answered = true;
      ctx.timedOut = !!auto;
      U.$$('.option', list).forEach(function (b) { b.disabled = true; });
      finish(box, ctx, !auto && choice === n, n + ' bahtów');
    }
    ctx.clock = new Countdown(box, Numbers.limitMs(def.limitMs), function () { settle(null, true); });

    options.forEach(function (v) {
      var btn = U.el('button', { class: 'btn option', type: 'button',
        text: v + ' bahtów' });
      btn.addEventListener('click', function () {
        btn.classList.add(v === n ? 'correct' : 'wrong');
        settle(v, false);
      });
      list.appendChild(btn);
    });
    box.appendChild(list);
    box.appendChild(CompTempo.row('numbers', function () { onNext(); }));
    Player.play(item, { btn: play, tempo: CompTempo.current });
  };

  /* ==================================================== 3. GODZINA ZE SŁUCHU */

  Numbers.renderClock = function (box, onNext) {
    var def = Numbers.drillDef('clock');
    header(box, def);
    var pool = Numbers.section('clock').filter(function (r) {
      return (r.meta || {}).kind === 'clock';
    });
    if (!pool.length) { box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję…' })); return; }
    var rec = pool[Math.floor(Math.random() * pool.length)];
    var view = G.view(rec);
    var hour = rec.meta.hour, minute = rec.meta.minute;

    box.appendChild(U.el('p', { text: 'Posłuchaj godziny i ustaw ją na zegarze.' }));
    var play = playBtn('Odtwórz godzinę', view, { tempo: CompTempo.current });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play]));

    var state = { h: 12, m: 0 };
    var face = U.el('div', { class: 'clock-face' });
    var readout = U.el('p', { class: 'clock-readout', role: 'status', 'aria-live': 'polite' });
    function paint() {
      readout.textContent = 'Ustawione: '
        + String(state.h).padStart(2, '0') + ':' + String(state.m).padStart(2, '0');
    }
    function stepper(label, get, set, max, step) {
      var row = U.el('div', { class: 'clock-stepper' });
      var minus = U.el('button', { class: 'btn ghost', type: 'button',
        'aria-label': 'Mniej: ' + label, text: '−' });
      var plus = U.el('button', { class: 'btn ghost', type: 'button',
        'aria-label': 'Więcej: ' + label, text: '+' });
      var val = U.el('span', { class: 'clock-val' });
      function show() { val.textContent = String(get()).padStart(2, '0'); }
      minus.addEventListener('click', function () { set((get() - step + max) % max); show(); paint(); });
      plus.addEventListener('click', function () { set((get() + step) % max); show(); paint(); });
      show();
      row.appendChild(U.el('span', { class: 'clock-label', text: label }));
      row.appendChild(minus); row.appendChild(val); row.appendChild(plus);
      return row;
    }
    face.appendChild(stepper('godzina', function () { return state.h; },
      function (v) { state.h = v; }, 24, 1));
    face.appendChild(stepper('minuty', function () { return state.m; },
      function (v) { state.m = v; }, 60, 15));
    box.appendChild(face);
    box.appendChild(readout);
    paint();

    var ctx = { mode: 'clock', value: hour * 100 + minute, onNext: onNext, timedOut: false };
    var answered = false;
    function settle(auto) {
      if (answered) return;
      answered = true;
      ctx.timedOut = !!auto;
      var ok = !auto && state.h === hour && state.m === minute;
      var why = U.el('p', { class: 'muted', text:
        'Odcinek doby rozstrzyga tu wszystko: ' + partExplain(hour) });
      finish(box, ctx, ok, String(hour).padStart(2, '0') + ':'
        + String(minute).padStart(2, '0'), why);
    }
    ctx.clock = new Countdown(box, Numbers.limitMs(def.limitMs), function () { settle(true); });
    var check = U.el('button', { class: 'btn gold', type: 'button', text: 'Sprawdź' });
    check.addEventListener('click', function () { settle(false); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [check]));
    box.appendChild(CompTempo.row('numbers', function () { onNext(); }));
    Player.play(view, { btn: play, tempo: CompTempo.current });
  };

  function partExplain(hour) {
    var sec = ((data().sections || []).filter(function (s) { return s.id === 'clock'; })[0] || {});
    var parts = sec.dayParts || [];
    for (var i = 0; i < parts.length; i++) {
      if (hour >= parts[i].from && hour <= parts[i].to) {
        return parts[i].range + ' — ' + parts[i].polish + '. ' + parts[i].trap;
      }
    }
    return 'północ ma własne słowo: thîang-khuen.';
  }

  /* ========================================================== 4. PRODUKCJA */

  Numbers.renderProduce = function (box, onNext) {
    var def = Numbers.drillDef('produce');
    header(box, def);
    var n = pickNumber(levelForUser() === 'high' ? 'mid' : levelForUser());
    var said = Numbers.say(n);
    if (!said) { box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję…' })); return; }

    box.appendChild(U.el('p', { class: 'num-big', text: String(n) }));
    box.appendChild(U.el('p', { text: 'Powiedz tę liczbę po tajsku, na głos.' }));

    var ctx = { mode: 'produce', value: n, onNext: onNext, timedOut: false };
    var answered = false;
    var area = U.el('div');
    box.appendChild(area);

    function settle(score, auto) {
      if (answered) return;
      answered = true;
      ctx.timedOut = !!auto;
      var hint = U.el('p', { class: 'muted' });
      hint.appendChild(U.el('span', { text: 'Wzór: ' }));
      hint.appendChild(U.renderPhonetic(said.thaiPhonetic, {}));
      finish(box, ctx, !auto && score >= 60, said.thaiPhonetic, hint);
    }
    ctx.clock = new Countdown(box, Numbers.limitMs(def.limitMs), function () { settle(0, true); });

    /* Ocena tonalna z sesji J. Bez mikrofonu ekran nie udaje, że ocenił —
       PronView.control sam mówi, czego brakuje, a obok stoi droga na piechotę:
       powiedz na głos i porównaj ze wzorem. Odpowiedź „nie wiedziałem” jest
       tam osobno, bo bez niej samoocena byłaby zawsze pozytywna. */
    var rec = { id: 'num:' + n, thaiPhonetic: said.thaiPhonetic, ttsKey: said.ttsKey,
                polish: String(n), syllables: said.thaiPhonetic.split('-') };
    if (global.PronView && PronView.canRecord && PronView.canRecord()) {
      area.appendChild(PronView.control(rec, {
        compact: true,
        label: 'Powiedz i oceń',
        onResult: function (result) { settle(result ? result.score : 0, false); }
      }));
    } else {
      area.appendChild(U.el('p', { class: 'muted', text:
        (global.PronView ? PronView.micMessage() : '')
        + ' Powiedz liczbę na głos i porównaj ze wzorem.' }));
      var reveal = U.el('button', { class: 'btn gold', type: 'button',
        text: 'Powiedziałem — pokaż wzór' });
      reveal.addEventListener('click', function () { settle(100, false); });
      var miss = U.el('button', { class: 'btn ghost', type: 'button',
        text: 'Nie wiedziałem' });
      miss.addEventListener('click', function () { settle(0, false); });
      area.appendChild(U.el('div', { class: 'btn-row' }, [reveal, miss]));
    }
  };

  /* ============================================================= 5. RESZTA */

  Numbers.renderChange = function (box, onNext) {
    var def = Numbers.drillDef('change');
    header(box, def);
    var bill = [100, 200, 500, 1000][Math.floor(Math.random() * 4)];
    var price = 5 * (1 + Math.floor(Math.random() * (bill / 5 - 1)));
    var change = bill - price;
    var unit = Numbers.section('prices').filter(function (r) {
      return (r.meta || {}).unit === 'baht';
    })[0];
    var priceItem = Numbers.item(price, unit ? unit.id : null);
    if (!priceItem) { box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję…' })); return; }

    box.appendChild(U.el('p', { text: 'Do zapłaty jest kwota, którą usłyszysz. '
      + 'Płacisz banknotem ' + bill + ' bahtów. Ile reszty?' }));
    var play = playBtn('Odtwórz kwotę', priceItem, { tempo: CompTempo.current });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play]));

    var field = U.el('input', { type: 'text', inputmode: 'numeric', id: 'num-change-in',
      autocomplete: 'off', class: 'num-input' });
    box.appendChild(U.el('label', { class: 'sr-only', for: 'num-change-in',
      text: 'Wpisz resztę cyframi' }));
    box.appendChild(field);

    var ctx = { mode: 'change', value: change, onNext: onNext, timedOut: false };
    var answered = false;
    function settle(auto) {
      if (answered) return;
      answered = true;
      ctx.timedOut = !!auto;
      field.disabled = true;
      var got = parseInt(String(field.value).replace(/\s/g, ''), 10);
      var said = Numbers.say(change);
      var hint = U.el('p', { class: 'muted' });
      hint.appendChild(U.el('span', { text: bill + ' − ' + price + ' = ' + change + ', czyli ' }));
      if (said) hint.appendChild(U.renderPhonetic(said.thaiPhonetic, {}));
      finish(box, ctx, !auto && got === change, String(change), hint);
    }
    ctx.clock = new Countdown(box, Numbers.limitMs(def.limitMs), function () { settle(true); });
    var check = U.el('button', { class: 'btn gold', type: 'button', text: 'Sprawdź' });
    check.addEventListener('click', function () { settle(false); });
    field.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); settle(false); }
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [check]));
    Player.play(priceItem, { btn: play, tempo: CompTempo.current });
    field.focus();
  };

  /* ============================================================== 6. CIĄG */

  Numbers.renderSequence = function (box, onNext) {
    var def = Numbers.drillDef('sequence');
    header(box, def);
    var len = 4 + Math.floor(Math.random() * 4);       // 4–7 cyfr
    var digits = [];
    for (var i = 0; i < len; i++) digits.push(Math.floor(Math.random() * 10));
    var a = atoms();
    var keys = digits.map(function (d) { return a.digits[d].ttsKey; });
    var item = {
      thaiPhonetic: digits.map(function (d) { return a.digits[d].thaiPhonetic; }).join(' '),
      ttsKey: DB.composeVoice(keys)
    };

    box.appendChild(U.el('p', { text: 'Posłuchaj ciągu ' + len + ' cyfr i odtwórz go. '
      + 'Tak właśnie podaje się numer telefonu — cyfra po cyfrze, nie jako liczba.' }));
    var play = playBtn('Odtwórz ciąg', item, { tempo: CompTempo.current });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play]));

    var field = U.el('input', { type: 'text', inputmode: 'numeric', id: 'num-seq-in',
      autocomplete: 'off', class: 'num-input' });
    box.appendChild(U.el('label', { class: 'sr-only', for: 'num-seq-in',
      text: 'Wpisz usłyszany ciąg cyfr' }));
    box.appendChild(field);

    var want = digits.join('');
    var ctx = { mode: 'sequence', value: len, onNext: onNext, timedOut: false };
    var answered = false;
    function settle(auto) {
      if (answered) return;
      answered = true;
      ctx.timedOut = !!auto;
      field.disabled = true;
      var got = String(field.value).replace(/\D/g, '');
      finish(box, ctx, !auto && got === want, want.split('').join(' '));
    }
    ctx.clock = new Countdown(box, Numbers.limitMs(def.limitMs), function () { settle(true); });
    var check = U.el('button', { class: 'btn gold', type: 'button', text: 'Sprawdź' });
    check.addEventListener('click', function () { settle(false); });
    field.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); settle(false); }
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [check]));
    Player.play(item, { btn: play, tempo: CompTempo.current });
    field.focus();
  };

  Numbers.RENDER = {
    dictation: Numbers.renderDictation,
    price: Numbers.renderPrice,
    clock: Numbers.renderClock,
    produce: Numbers.renderProduce,
    change: Numbers.renderChange,
    sequence: Numbers.renderSequence
  };

  /* ==================================================== SCENY LICZBOWE */

  Numbers.renderScene = function (box, scene, onDone) {
    box.appendChild(U.el('h2', { text: scene.title }));
    box.appendChild(U.el('p', { class: 'muted', text: scene.setting
      + ' · pytania dotyczą KONKRETNEJ WARTOŚCI, nie ogólnego sensu — '
      + 'scenę da się „zrozumieć”, przespawszy całą liczbę, i o to właśnie chodzi.' }));

    var showText = false;
    var lines = U.el('div', { class: 'scene-lines' });
    function paintLines() {
      U.clear(lines);
      scene.lines.forEach(function (line) {
        var view = G.view(line);
        var row = U.el('div', { class: 'scene-line' });
        var b = U.el('button', { class: 'btn ghost play-btn', type: 'button',
          'aria-label': 'Odtwórz kwestię ' + line.index });
        b.appendChild(U.icon('play'));
        b.addEventListener('click', function () {
          Player.play(view, { btn: b, tempo: CompTempo.current,
            role: line.role, gender: line.speakerGender });
        });
        row.appendChild(b);
        row.appendChild(U.el('span', { class: 'scene-role', text: line.role }));
        if (showText) {
          row.appendChild(U.renderPhonetic(view.thaiPhonetic, {}));
          row.appendChild(U.el('span', { class: 'muted', text: view.polish }));
        }
        lines.appendChild(row);
      });
    }
    var toggle = U.el('button', { class: 'chip', type: 'button',
      'aria-pressed': 'false', text: 'Pokaż zapis' });
    toggle.addEventListener('click', function () {
      showText = !showText;
      toggle.setAttribute('aria-pressed', showText ? 'true' : 'false');
      toggle.textContent = showText ? 'Ukryj zapis' : 'Pokaż zapis';
      paintLines();
    });

    var playAll = U.el('button', { class: 'btn gold', type: 'button', text: 'Odtwórz całą scenę' });
    playAll.addEventListener('click', function () {
      var i = 0;
      (function step() {
        if (i >= scene.lines.length) return;
        var line = scene.lines[i++];
        Player.play(G.view(line), { tempo: CompTempo.current, role: line.role,
          gender: line.speakerGender, onend: function () { setTimeout(step, 260); } });
      })();
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [playAll, toggle]));
    box.appendChild(lines);
    paintLines();

    var qbox = U.el('div', { class: 'card' });
    box.appendChild(qbox);
    var at = 0, right = 0;
    function askQuestion() {
      U.clear(qbox);
      if (at >= scene.questions.length) {
        qbox.appendChild(U.el('p', { class: 'fb ok', role: 'status', text:
          'Koniec sceny: ' + right + ' z ' + scene.questions.length + ' wartości trafionych.' }));
        var back = U.el('button', { class: 'btn', type: 'button', text: 'Inna scena' });
        back.addEventListener('click', onDone);
        qbox.appendChild(U.el('div', { class: 'btn-row' }, [back]));
        return;
      }
      var q = scene.questions[at];
      qbox.appendChild(U.el('p', { class: 'q-prompt', text:
        'Pytanie ' + (at + 1) + ' z ' + scene.questions.length + ': ' + q.prompt }));
      var opts = U.el('div', { class: 'options' });
      var done = false;
      q.options.forEach(function (text, i) {
        var btn = U.el('button', { class: 'btn option', type: 'button', text: text });
        btn.addEventListener('click', function () {
          if (done) return;
          done = true;
          var ok = i === q.answer;
          if (ok) right += 1;
          btn.classList.add(ok ? 'correct' : 'wrong');
          U.$$('.option', opts).forEach(function (b, j) {
            b.disabled = true;
            if (j === q.answer) b.classList.add('correct');
          });
          qbox.appendChild(U.el('p', { class: ok ? 'fb ok' : 'fb bad', role: 'status',
            text: q.explain }));
          Progress.numberAnswer('scene', ok, 0, { value: q.value, scene: scene.id });
          var next = U.el('button', { class: 'btn', type: 'button', text: 'Dalej' });
          next.addEventListener('click', function () { at += 1; askQuestion(); });
          qbox.appendChild(U.el('div', { class: 'btn-row' }, [next]));
          next.focus();
        });
        opts.appendChild(btn);
      });
      qbox.appendChild(opts);
    }
    askQuestion();
  };

  global.Numbers = Numbers;
})(window);
