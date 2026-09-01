/* Thai All-in-One — próbki kontrolne.

   Problem, który rozwiązują
   -------------------------
   Kolejka powtórek (SRS) mówi o zapominaniu dopiero wtedy, gdy karta wypadnie
   do powtórzenia. Przy odstępach rosnących wykładniczo hasło z lekcji 12 wraca
   po miesiącu, potem po trzech — a pomiędzy jednym a drugim terminem nie ma
   ŻADNEGO sygnału. Uczący się idzie dalej w przekonaniu, że materiał został
   w głowie, i dowiaduje się inaczej dopiero przy powtórce albo na egzaminie.

   Próbka kontrolna jest czujnikiem wstawionym MIĘDZY terminy powtórek: co 20
   lekcji dwanaście zadań z materiału sprzed 20 lekcji. Nie planuje powtórek
   i nie zastępuje SRS-u — mówi wcześniej to, co SRS powie później.

   Najciekawsza rzecz w wyniku nie jest procentem. Jest nią lista haseł, które
   uczący się właśnie pomylił, a które w kolejce powtórek NIE MIAŁY jeszcze
   terminu. Każde takie hasło to jeden konkretny przypadek, w którym odstęp
   powtórki okazał się za długi — i dokładnie po to ta próbka istnieje. */
(function (global) {
  'use strict';

  var Checkpoint = { state: null };

  Checkpoint.ready = function () { return !!(DB.checkpoints && DB.checkpoints.records); };
  Checkpoint.ensureData = function () { return DB.ensureCheckpoints(); };

  function all() { return (DB.checkpoints && DB.checkpoints.records) || []; }
  Checkpoint.all = all;

  Checkpoint.byId = function (id) {
    var list = all();
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  };

  /* Ile lekcji ścieżki jest zaliczonych — próbka odblokowuje się po tej
     liczbie, a nie po numerze ostatnio otwartej lekcji. Ktoś, kto przeskoczył
     połowę kursu testem poziomującym, nie ma czego zapominać z lekcji,
     których nie robił. */
  function doneCount() {
    var lessons = DB.lessons || [];
    var n = 0;
    lessons.forEach(function (L) { if (Progress.isLessonDone(L.id)) n += 1; });
    return n;
  }
  Checkpoint.doneCount = doneCount;

  /* Próbki należne: wyzwolone liczbą zaliczonych lekcji i jeszcze niezrobione.
     Zwracamy WSZYSTKIE zaległe, nie tylko najbliższą — kto zrobił sto lekcji
     jednym ciągiem, ma prawo wiedzieć, że czekają na niego cztery. */
  Checkpoint.due = function () {
    var done = doneCount();
    return all().filter(function (c) {
      if (c.triggerLesson > done) return false;
      var box = Progress.checkpointOf(c.id);
      return !box || !box.attempts.length;
    });
  };

  Checkpoint.next = function () {
    var due = Checkpoint.due();
    if (due.length) return due[0];
    var done = doneCount();
    var upcoming = all().filter(function (c) { return c.triggerLesson > done; });
    return upcoming.length ? upcoming[0] : null;
  };

  /* Ile lekcji dzieli od następnej próbki — do paska „Dzisiaj”. */
  Checkpoint.lessonsToNext = function () {
    var next = Checkpoint.next();
    if (!next) return null;
    var left = next.triggerLesson - doneCount();
    return left > 0 ? left : 0;
  };

  /* --------------------------------------------------------------- przebieg */

  Checkpoint.start = function (id) {
    var def = Checkpoint.byId(id);
    if (!def) return null;
    Checkpoint.state = {
      def: def,
      at: 0,
      startedAt: Date.now(),
      answers: [],
      finished: false
    };
    return Checkpoint.state;
  };

  Checkpoint.current = function () {
    var s = Checkpoint.state;
    return s && s.at < s.def.items.length ? s.def.items[s.at] : null;
  };

  Checkpoint.secondsLeft = function () {
    var s = Checkpoint.state;
    if (!s) return null;
    var used = Math.floor((Date.now() - s.startedAt) / 1000);
    return Math.max(0, s.def.timeLimitSec - used);
  };

  function norm(text) {
    return U.fold(text || '').replace(/[^a-z]/g, '');
  }

  /* Odpowiedź na zadanie ze słuchu (wybór) albo z pamięci (zapis).
     Zapis oceniamy bez tonów: próbka ma wykryć ubytek formy dźwiękowej,
     a nie odpytywać ze znaków diakrytycznych. */
  Checkpoint.answer = function (item, value, expected) {
    var s = Checkpoint.state;
    var ok;
    if (item.kind === 'listen') {
      ok = value === item.answer;
    } else {
      ok = norm(value) === norm(expected);
    }
    /* Czy SRS zdążyłby to wyłapać? Sprawdzamy TERAZ, zanim ocena zmieni
       stan karty — po Progress.answer i SRS.grade termin jest już inny. */
    var card = (global.SRS && SRS.cards)
      ? SRS.cards[SRS.cardId(item.recordId, 'r')] : null;
    var dueLater = false;
    if (!ok && card && card.due) dueLater = card.due > U.today();
    var untracked = !ok && !card;

    s.answers.push({
      id: item.id,
      recordId: item.recordId,
      kind: item.kind,
      lesson: item.lesson,
      polish: item.polish,
      value: value,
      ok: ok,
      dueLater: dueLater,
      untracked: untracked
    });
    Progress.answer(item.recordId, ok, { mode: 'checkpoint' });
    if (global.SRS) {
      SRS.add(item.recordId, 'r');
      SRS.grade(item.recordId, ok ? 4 : 1, { side: 'r' });
    }
    s.at += 1;
    return ok;
  };

  Checkpoint.finish = function (expired) {
    var s = Checkpoint.state;
    if (!s || s.finished) return null;
    s.finished = true;
    /* Zadania nietknięte liczą się jak pomyłki — limit czasu nie może być
       premią za niezrobienie zadania. */
    for (var i = s.answers.length; i < s.def.items.length; i++) {
      var item = s.def.items[i];
      s.answers.push({
        id: item.id, recordId: item.recordId, kind: item.kind,
        lesson: item.lesson, polish: item.polish, value: null,
        ok: false, dueLater: false, untracked: false, skipped: true
      });
    }
    var hit = s.answers.filter(function (a) { return a.ok; }).length;
    var pct = s.answers.length ? Math.round(hit / s.answers.length * 100) : 0;
    var early = s.answers.filter(function (a) { return !a.ok && (a.dueLater || a.untracked); });
    var result = {
      id: s.def.id,
      triggerLesson: s.def.triggerLesson,
      fromLesson: s.def.fromLesson,
      toLesson: s.def.toLesson,
      date: U.today(),
      at: new Date().toISOString(),
      durationSec: Math.round((Date.now() - s.startedAt) / 1000),
      correct: hit,
      total: s.answers.length,
      pct: pct,
      passed: pct >= s.def.passPct,
      expired: !!expired,
      earlyCatch: early.map(function (a) { return a.recordId; }),
      wrong: s.answers.filter(function (a) { return !a.ok; })
        .map(function (a) { return { id: a.recordId, lesson: a.lesson, polish: a.polish }; })
    };
    Progress.saveCheckpoint(result);
    Checkpoint.lastResult = result;
    return result;
  };

  /* Lekcje, do których warto wrócić po słabej próbce — te, z których było
     najwięcej pomyłek, a nie całe okno dwudziestu lekcji. */
  Checkpoint.weakLessons = function (result) {
    var count = {};
    (result.wrong || []).forEach(function (w) {
      if (w.lesson) count[w.lesson] = (count[w.lesson] || 0) + 1;
    });
    return Object.keys(count).map(Number).sort(function (a, b) {
      return count[b] - count[a] || a - b;
    }).slice(0, 5);
  };

  /* ----------------------------------------------------------------- ekran */

  var timer = null;
  function stopTimer() { if (timer) { clearInterval(timer); timer = null; } }

  function root() { return U.$('#checkpoint-area'); }

  function redraw() {
    var box = root();
    if (!box) return;
    U.clear(box);
    Checkpoint.render(box);
  }

  function fmtTime(sec) {
    var m = Math.floor(sec / 60), s = sec % 60;
    return m + ':' + (s < 10 ? '0' : '') + s;
  }

  Checkpoint.render = function (box) {
    stopTimer();
    if (!Checkpoint.ready()) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję próbki kontrolne…' }));
      return;
    }
    if (Checkpoint.state && !Checkpoint.state.finished) { renderTask(box); return; }
    if (Checkpoint.showing === 'result' && Checkpoint.lastResult) {
      renderResult(box, Checkpoint.lastResult);
      return;
    }
    renderHub(box);
  };

  function renderHub(box) {
    var intro = U.el('div', { class: 'card' });
    intro.appendChild(U.el('h2', { text: 'Próbki kontrolne' }));
    intro.appendChild(U.el('p', {
      text: 'Co 20 lekcji dwanaście zadań z materiału sprzed 20 lekcji. Powtórki pokazują '
        + 'ubytek dopiero wtedy, gdy karta wypadnie do powtórzenia — przy odstępach rosnących '
        + 'wykładniczo może to być za miesiąc albo za trzy. Próbka pyta wcześniej.'
    }));
    intro.appendChild(U.el('p', {
      class: 'muted',
      text: 'Zaliczonych lekcji: ' + doneCount() + '. Próg próbki: '
        + (DB.checkpoints.passPct || 75) + '%, limit czasu '
        + Math.round((DB.checkpoints.timeLimitSec || 360) / 60) + ' minut.'
    }));
    box.appendChild(intro);

    var due = Checkpoint.due();
    if (due.length) {
      var card = U.el('div', { class: 'card' });
      card.appendChild(U.el('h3', {
        text: due.length === 1 ? 'Jedna próbka czeka' : (due.length + ' próbki czekają')
      }));
      due.slice(0, 4).forEach(function (c) {
        var row = U.el('div', { class: 'plan-step' });
        row.appendChild(U.el('h4', { text: c.title }));
        row.appendChild(U.el('p', {
          class: 'muted',
          text: 'Wyzwolona po ' + c.triggerLesson + ' zaliczonych lekcjach · zadań '
            + c.taskCount + ' · czas ' + Math.round(c.timeLimitSec / 60) + ' minut.'
        }));
        var go = U.el('button', { class: 'btn', type: 'button', text: 'Zrób próbkę' });
        go.addEventListener('click', function () { start(c.id); });
        row.appendChild(U.el('div', { class: 'btn-row' }, [go]));
        card.appendChild(row);
      });
      box.appendChild(card);
    } else {
      var wait = U.el('div', { class: 'card' });
      var left = Checkpoint.lessonsToNext();
      var next = Checkpoint.next();
      wait.appendChild(U.el('p', {
        text: next
          ? ('Następna próbka za ' + left + ' ' + U.plural(left, 'lekcję', 'lekcje', 'lekcji')
             + ' — sprawdzi lekcje ' + next.fromLesson + '–' + next.toLesson + '.')
          : 'Wszystkie próbki są za tobą.'
      }));
      box.appendChild(wait);
    }

    var history = Progress.checkpointSummary();
    if (history.length) {
      var hist = U.el('div', { class: 'card' });
      hist.appendChild(U.el('h3', { text: 'Historia' }));
      var tbl = U.el('table', { class: 'data-table' });
      var hr = U.el('tr');
      ['Zakres', 'Wynik', 'Wyprzedziło powtórki'].forEach(function (t) {
        hr.appendChild(U.el('th', { text: t }));
      });
      tbl.appendChild(U.el('thead', {}, [hr]));
      var tb = U.el('tbody');
      history.forEach(function (r) {
        var tr = U.el('tr');
        tr.appendChild(U.el('td', { text: 'lekcje ' + r.fromLesson + '–' + r.toLesson }));
        tr.appendChild(U.el('td', { text: r.pct + '%' }));
        tr.appendChild(U.el('td', { text: String((r.earlyCatch || []).length) }));
        tb.appendChild(tr);
      });
      tbl.appendChild(tb);
      hist.appendChild(tbl);
      hist.appendChild(U.el('p', {
        class: 'muted',
        text: 'Ostatnia kolumna to liczba haseł, które wypadły z pamięci, choć kolejka '
          + 'powtórek nie miała ich jeszcze na dziś. To jest dokładnie ten sygnał, po który '
          + 'te próbki istnieją.'
      }));
      box.appendChild(hist);
    }
  }

  function start(id) {
    var def = Checkpoint.byId(id);
    var box = root();
    U.clear(box).appendChild(U.el('p', { class: 'muted', text: 'Przygotowuję zadania…' }));
    DB.ensureCheckpointRecords(def).then(function () {
      Checkpoint.start(id);
      Checkpoint.showing = null;
      redraw();
    });
  }

  function renderTask(box) {
    var s = Checkpoint.state;
    var item = Checkpoint.current();
    if (!item) { finish(false); return; }

    var head = U.el('div', { class: 'card' });
    head.appendChild(U.el('h2', { text: s.def.title }));
    var clock = U.el('p', { class: 'exam-clock', role: 'timer', 'aria-live': 'off' });
    head.appendChild(clock);
    head.appendChild(U.el('p', {
      class: 'muted', text: 'Zadanie ' + (s.at + 1) + ' z ' + s.def.items.length
    }));
    box.appendChild(head);

    function tick() {
      var left = Checkpoint.secondsLeft();
      clock.textContent = 'Pozostały czas: ' + fmtTime(left);
      clock.classList.toggle('low', left <= 45);
      if (left <= 0) { stopTimer(); finish(true); }
    }
    tick();
    stopTimer();
    timer = setInterval(tick, 1000);

    var card = U.el('div', { class: 'card' });
    box.appendChild(card);
    var rec = DB.any(item.recordId);

    if (item.kind === 'listen') {
      card.appendChild(U.el('p', { class: 'muted', text: 'Posłuchaj i wskaż znaczenie.' }));
      if (rec) card.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(rec, 'Odtwórz')]));
      var list = U.el('div', { class: 'options' });
      var locked = false;
      item.options.forEach(function (text, i) {
        var btn = U.el('button', { class: 'btn option', type: 'button', text: text });
        btn.addEventListener('click', function () {
          if (locked) return;
          locked = true;
          Player.stop();
          Checkpoint.answer(item, i);
          redraw();
        });
        list.appendChild(btn);
      });
      card.appendChild(list);
      if (rec) Player.play(rec, {});
    } else {
      card.appendChild(U.el('p', {
        class: 'muted',
        text: 'Zapisz z pamięci, alfabetem łacińskim. Znaki tonu nie są wymagane. '
          + 'Bez odsłuchu — o to właśnie chodzi.'
      }));
      card.appendChild(U.el('p', { class: 'q-prompt', text: item.polish }));
      var input = U.el('input', {
        type: 'text', id: 'chk-input', autocomplete: 'off', autocapitalize: 'off',
        spellcheck: 'false', placeholder: 'np. sawat-dii'
      });
      card.appendChild(U.el('label', { class: 'field' },
        [U.el('span', { text: 'Twój zapis' }), input]));
      var send = U.el('button', { class: 'btn', type: 'button', text: 'Zatwierdź' });
      var used = false;
      send.addEventListener('click', function () {
        if (used) return;
        used = true;
        Checkpoint.answer(item, input.value, rec ? rec.thaiPhonetic : '');
        redraw();
      });
      input.addEventListener('keydown', function (e) { if (e.key === 'Enter') send.click(); });
      card.appendChild(U.el('div', { class: 'btn-row' }, [send]));
      input.focus();
    }
  }

  function finish(expired) {
    stopTimer();
    var result = Checkpoint.finish(expired);
    Checkpoint.showing = 'result';
    redraw();
    return result;
  }

  function renderResult(box, result) {
    var card = U.el('div', { class: 'card' });
    card.appendChild(U.el('h2', {
      text: result.passed ? 'Materiał trzyma się dobrze' : 'Część materiału wypadła z pamięci'
    }));
    card.appendChild(U.el('p', {
      text: 'Lekcje ' + result.fromLesson + '–' + result.toLesson + ': '
        + result.correct + ' z ' + result.total + ' (' + result.pct + '%).'
        + (result.expired ? ' Czas minął przed końcem — nietknięte zadania liczą się jak pomyłki.' : '')
    }));
    box.appendChild(card);

    var early = (result.earlyCatch || []).length;
    var signal = U.el('div', { class: 'card' });
    signal.appendChild(U.el('h3', { text: 'Co to wykryło wcześniej niż powtórki' }));
    signal.appendChild(U.el('p', {
      text: early
        ? (early + ' ' + U.plural(early, 'hasło', 'hasła', 'haseł') + ' wypadło z pamięci, '
           + 'mimo że kolejka powtórek nie miała ich jeszcze na dziś. Odstęp powtórki był '
           + 'dla nich za długi — trafiły już do kolejki na dziś.')
        : 'Wszystkie pomyłki dotyczyły haseł, które kolejka powtórek i tak miała na oku. '
          + 'Tym razem próbka niczego nie wyprzedziła i to jest dobra wiadomość.'
    }));
    box.appendChild(signal);

    var weak = Checkpoint.weakLessons(result);
    if (weak.length) {
      var plan = U.el('div', { class: 'card' });
      plan.appendChild(U.el('h3', { text: 'Do czego wrócić' }));
      plan.appendChild(U.el('p', { text: 'Lekcje z największą liczbą pomyłek: ' + weak.join(', ') + '.' }));
      var go = U.el('button', { class: 'btn', type: 'button', text: 'Otwórz kurs' });
      go.addEventListener('click', function () { App.go('course'); });
      var srs = U.el('button', { class: 'btn ghost', type: 'button', text: 'Przejdź do powtórek' });
      srs.addEventListener('click', function () { App.go('srs'); });
      plan.appendChild(U.el('div', { class: 'btn-row' }, [go, srs]));
      box.appendChild(plan);
    }

    var foot = U.el('div', { class: 'card' });
    var back = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wróć do listy próbek' });
    back.addEventListener('click', function () {
      Checkpoint.showing = null;
      Checkpoint.state = null;
      redraw();
    });
    foot.appendChild(U.el('div', { class: 'btn-row' }, [back]));
    box.appendChild(foot);
  }

  Checkpoint.leave = function () {
    stopTimer();
    /* Próbka nie jest egzaminem — wyjście w trakcie po prostu ją porzuca,
       bez zapisu i bez kary. Ma być tania, więc nie może straszyć. */
    if (Checkpoint.state && !Checkpoint.state.finished) Checkpoint.state = null;
  };

  global.Checkpoint = Checkpoint;
})(window);
