/* Thai All-in-One — ekran Modułu 0.

   Ćwiczenia w tym module są czysto słuchowe, więc muszą dać się obsłużyć bez
   patrzenia na ekran. Stąd trzy decyzje, które przenikają cały ten plik:

     1. Każde zadanie ma pełną obsługę klawiaturą. Cyfry 1–5 wybierają
        odpowiedź, R powtarza dźwięk, P porównuje oba warianty jeden po drugim,
        Enter i strzałka w prawo przechodzą dalej. Skróty działają na całym
        ekranie, nie tylko na przycisku z focusem.
     2. Wszystko, co dzieje się z dźwiękiem i z odpowiedzią, jest ogłaszane
        przez aria-live. Czytnik ekranu mówi „odtwarzam pierwszy dźwięk”,
        „dobrze”, „to był ton opadający” — bez tego ćwiczenie jest nie do
        przejścia na słuch.
     3. Po odpowiedzi zawsze da się przesłuchać oba warianty kontrastu jeden po
        drugim. Sama informacja „źle” niczego nie uczy; ucho uczy się na
        zestawieniu.

   Zapis fonetyczny bodźca jest domyślnie zasłonięty. To trening percepcyjny —
   gdyby uczący się widział „khàaw”, odpowiadałby z zapisu, nie ze słuchu. */
(function (global) {
  'use strict';

  var View = {};
  var state = {
    mode: 'map',       // 'map' | 'lesson' | 'diagnostic'
    keysBound: false,
    options: [],       // aktywne przyciski odpowiedzi (do skrótów 1–9)
    replay: null,      // funkcja powtarzająca bodziec
    compare: null,     // funkcja porównująca oba warianty
    advance: null,     // funkcja „dalej”
    reveal: false
  };

  var GAP = 620;       // przerwa między bodźcami w jednym zadaniu (ms)

  function say(text) {
    var live = U.$('#m0-live');
    if (!live) return;
    /* Powtórzenie tego samego tekstu nie wywołałoby ogłoszenia, więc
       przełamujemy je pustym cyklem. */
    live.textContent = '';
    setTimeout(function () { live.textContent = text; }, 30);
  }
  View.say = say;

  function stimOf(id) {
    var s = Perception.stimulus(id);
    if (!s) return null;
    return s;
  }

  var ORDINAL = ['pierwszy', 'drugi', 'trzeci', 'czwarty', 'piąty', 'szósty'];

  /* Odtwarza kolejno listę bodźców, ogłaszając, który właśnie leci. */
  function playSeries(ids, opts) {
    opts = opts || {};
    var items = ids.map(stimOf).filter(Boolean);
    if (!items.length) { U.toast('Brak nagrania dla tego zadania.'); return; }
    var i = 0;
    Player.stop();
    (function step() {
      if (i >= items.length) {
        if (opts.onend) opts.onend();
        return;
      }
      var it = items[i];
      if (items.length > 1) say('Odtwarzam ' + (ORDINAL[i] || (i + 1)) + ' dźwięk.');
      i += 1;
      Player.play(it, {
        btn: opts.btn,
        onend: function () { setTimeout(step, opts.gap || GAP); }
      });
    })();
  }

  /* Oba warianty kontrastu, jeden po drugim, z nazwaniem każdego. Po
     odpowiedzi zapis jest już odsłonięty, więc mówimy też fonetykę. */
  function playCompare(ids, named) {
    var items = ids.map(stimOf).filter(Boolean);
    if (items.length < 2) { playSeries(ids); return; }
    var i = 0;
    Player.stop();
    (function step() {
      if (i >= items.length) return;
      var it = items[i];
      say((i === 0 ? 'Pierwszy wariant' : 'Drugi wariant')
        + (named ? ': ' + it.phonetic : '') + '.');
      i += 1;
      Player.play(it, { onend: function () { setTimeout(step, 800); } });
    })();
  }

  /* ------------------------------------------------------------- klawiatura */

  function bindKeys() {
    if (state.keysBound) return;
    state.keysBound = true;
    document.addEventListener('keydown', function (e) {
      if (App.screen !== 'module0' && App.screen !== 'srs') return;
      if (!state.options.length && !state.advance) return;
      if (!U.$('#sheet').hidden) return;
      var tag = (e.target.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
      if (e.ctrlKey || e.metaKey || e.altKey) return;

      var k = e.key;
      if (/^[1-9]$/.test(k)) {
        var idx = parseInt(k, 10) - 1;
        if (state.options[idx]) {
          e.preventDefault();
          state.options[idx].click();
        }
        return;
      }
      if (k === 'r' || k === 'R') {
        if (state.replay) { e.preventDefault(); state.replay(); }
        return;
      }
      if (k === 'p' || k === 'P') {
        if (state.compare) { e.preventDefault(); state.compare(); }
        return;
      }
      if (k === 'Enter' || k === 'ArrowRight') {
        if (state.advance) { e.preventDefault(); state.advance(); }
        return;
      }
      if (k === 'Escape') {
        Player.stop();
        say('Odtwarzanie zatrzymane.');
      }
    });
  }

  function clearHandlers() {
    state.options = [];
    state.replay = null;
    state.compare = null;
    state.advance = null;
  }

  /* ------------------------------------------------------------ mapa modułu */

  function statBox(value, label) {
    return U.el('div', { class: 'stat' },
      [U.el('b', { text: String(value) }), U.el('span', { text: label })]);
  }

  View.render = function () {
    bindKeys();
    clearHandlers();
    var root = U.clear(U.$('#module0-area'));
    if (!Perception.ready()) {
      root.appendChild(U.el('p', { class: 'muted', role: 'status',
        text: 'Moduł 0 jeszcze się wczytuje…' }));
      return;
    }
    if (state.mode === 'lesson' && Perception.run) { renderLessonRun(root); return; }
    if (state.mode === 'diagnostic' && Perception.diag) { renderDiagnosticRun(root); return; }
    renderMap(root);
  };

  function renderMap(root) {
    var info = Perception.info();
    var sum = Perception.summary();

    var stats = U.el('div', { class: 'stat-row' });
    stats.appendChild(statBox(sum.done + ' / ' + sum.total, 'lekcji zrobionych'));
    stats.appendChild(statBox(sum.tasks, 'zadań w module'));
    var ps = Progress.perceptionSummary();
    stats.appendChild(statBox(ps.answers ? ps.accuracy + '%' : '—', 'skuteczność'));
    stats.appendChild(statBox(Perception.isOptional() ? 'opcjonalny' : 'obowiązkowy', 'status'));
    root.appendChild(stats);

    /* --- po co to jest --- */
    var why = U.el('div', { class: 'card' });
    why.appendChild(U.el('h2', { text: info.title }));
    why.appendChild(U.el('p', { text: info.intro }));
    why.appendChild(U.el('p', { class: 'muted', text: info.why }));
    root.appendChild(why);

    /* --- diagnoza --- */
    var dbox = U.el('div', { class: 'card' });
    var diag = Perception.diagnosticResult();
    dbox.appendChild(U.el('h2', { text: info.diagnostic.title }));
    dbox.appendChild(U.el('p', { class: 'muted', text: info.diagnostic.description }));
    if (diag) {
      dbox.appendChild(U.el('p', { class: 'fb ok', text:
        'Ostatni wynik: ' + diag.score + ' z ' + diag.total + ' (' + diag.date + ').' }));
      dbox.appendChild(contrastMapTable(diag));
    }
    var dbtn = U.el('button', { class: 'btn gold', type: 'button',
      text: diag ? 'Powtórz diagnozę' : 'Zrób diagnozę (20 zadań)' });
    dbtn.addEventListener('click', function () {
      Perception.startDiagnostic();
      state.mode = 'diagnostic';
      View.render();
    });
    dbox.appendChild(U.el('div', { class: 'btn-row' }, [dbtn]));
    root.appendChild(dbox);

    /* --- następna lekcja --- */
    var next = Perception.next();
    var nbox = U.el('div', { class: 'card' });
    if (!next) {
      nbox.appendChild(U.el('h2', { text: 'Cały moduł za Tobą' }));
      nbox.appendChild(U.el('p', { class: 'muted', text:
        'Wszystkie ' + sum.total + ' lekcji są zrobione. Kurs jest otwarty — '
        + 'a słabe kontrasty wracają w powtórkach same.' }));
      var toCourse = U.el('button', { class: 'btn gold', type: 'button', text: 'Przejdź do kursu' });
      toCourse.addEventListener('click', function () { App.go('course'); });
      nbox.appendChild(U.el('div', { class: 'btn-row' }, [toCourse]));
    } else {
      nbox.appendChild(U.el('h2', { text: 'Następna lekcja' }));
      nbox.appendChild(U.el('p', { class: 'bc-pl', text: next.number + '. ' + next.title }));
      nbox.appendChild(U.el('p', { class: 'muted', text: next.goal }));
      nbox.appendChild(U.el('p', { class: 'muted', text: next.pass.text }));
      var open = U.el('button', { class: 'btn gold', type: 'button', text: 'Zacznij lekcję' });
      open.addEventListener('click', function () { startLesson(next); });
      nbox.appendChild(U.el('div', { class: 'btn-row' }, [open]));
    }
    root.appendChild(nbox);

    /* --- lista lekcji --- */
    var map = U.el('div', { class: 'card' });
    map.appendChild(U.el('h2', { text: 'Lekcje modułu' }));
    var list = U.el('div', { class: 'course-map' });
    Perception.lessons().forEach(function (L) { list.appendChild(lessonNode(L)); });
    map.appendChild(list);
    root.appendChild(map);

    /* --- pominięcie --- */
    var skip = U.el('div', { class: 'card' });
    skip.appendChild(U.el('h2', { text: 'Chcę pominąć moduł' }));
    skip.appendChild(U.el('p', { text: info.skipWarning }));
    if (Perception.isOptional() && !Perception.isSkipped()) {
      skip.appendChild(U.el('p', { class: 'muted', text:
        'Test poziomujący posadził Cię powyżej A1, więc moduł i tak nie blokuje '
        + 'kursu. Zostaje dostępny, bo trening percepcyjny przydaje się też wyżej.' }));
    }
    if (Perception.isSkipped()) {
      skip.appendChild(U.el('p', { class: 'fb bad', text:
        'Moduł jest pominięty od ' + (Progress.perception().skippedAt || '—')
        + '. Kurs jest otwarty, ale wyrazy zapamiętasz bez tonów.' }));
      var back = U.el('button', { class: 'btn gold', type: 'button',
        text: 'Jednak chcę zrobić Moduł 0' });
      back.addEventListener('click', function () {
        Perception.unskipModule();
        U.toast('Moduł 0 znów jest częścią ścieżki.');
        View.render();
      });
      skip.appendChild(U.el('div', { class: 'btn-row' }, [back]));
    } else {
      var sbtn = U.el('button', { class: 'btn ghost', type: 'button',
        text: 'Rozumiem konsekwencje — pomiń moduł' });
      sbtn.addEventListener('click', confirmSkip);
      skip.appendChild(U.el('div', { class: 'btn-row' }, [sbtn]));
    }
    root.appendChild(skip);
  }

  /* Pominięcie musi być świadome, więc idzie przez osobne okno z wyliczoną
     konsekwencją, a nie przez jedno kliknięcie w przycisk na liście. */
  function confirmSkip() {
    var info = Perception.info();
    var body = U.el('div');
    body.appendChild(U.el('h2', { id: 'sheet-title', text: 'Pominąć trening słuchu?' }));
    body.appendChild(U.el('p', { text: info.skipWarning }));
    body.appendChild(U.el('p', { class: 'muted', text:
      'Konkretnie: khǎaw (biały), khàaw (wiadomości) i khâaw (ryż) zapiszą Ci się '
      + 'w pamięci jako jedno słowo „khaaw”. W restauracji zamówisz wiadomości.' }));
    var yes = U.el('button', { class: 'btn ghost', type: 'button', text: 'Pomijam mimo to' });
    yes.addEventListener('click', function () {
      Perception.skipModule();
      App.closeSheet();
      U.toast('Moduł 0 pominięty. Możesz do niego wrócić w każdej chwili.');
      View.render();
      if (App.renderCourse) App.renderCourse();
    });
    var no = U.el('button', { class: 'btn gold', type: 'button', text: 'Zostaję przy module' });
    no.addEventListener('click', function () { App.closeSheet(); });
    body.appendChild(U.el('div', { class: 'btn-row' }, [no, yes]));
    App.openSheet(body);
  }

  var STATUS_LABEL = {
    passed: 'Zaliczona.', skipped: 'Pominięta.',
    diagnosed: 'Zwolniona diagnozą.', open: 'Dostępna.',
    locked: 'Zamknięta — najpierw zalicz poprzednią lekcję.'
  };

  function lessonNode(L) {
    var status = Perception.status(L);
    var node = U.el('button', {
      class: 'lesson-card is-' + status,
      type: 'button',
      'data-m0-lesson': L.id,
      'aria-label': 'Lekcja ' + L.number + ': ' + L.title + '. ' + STATUS_LABEL[status]
    });
    var badge = U.el('span', { class: 'lesson-badge', 'aria-hidden': 'true' });
    if (status === 'passed' || status === 'diagnosed') badge.appendChild(U.icon('check'));
    else if (status === 'locked') badge.appendChild(U.icon('lock'));
    else badge.appendChild(U.el('span', { text: String(L.number) }));
    node.appendChild(badge);

    var main = U.el('span', { class: 'lesson-main' });
    main.appendChild(U.el('span', { class: 'lesson-title', text: L.title }));
    var kinds = {};
    L.tasks.forEach(function (t) { kinds[t.type] = (kinds[t.type] || 0) + 1; });
    main.appendChild(U.el('span', { class: 'lesson-meta', text:
      L.tasks.length + ' zadań · próg ' + L.pass.required + ' (' + L.pass.accuracy + '%) · '
      + L.contrastIds.length + ' ' + U.plural(L.contrastIds.length, 'kontrast', 'kontrasty', 'kontrastów') }));
    node.appendChild(main);
    node.addEventListener('click', function () { openLesson(L); });
    return node;
  }

  function openLesson(L) {
    var status = Perception.status(L);
    var body = U.el('div');
    body.appendChild(U.el('h2', { id: 'sheet-title', text: L.number + '. ' + L.title }));
    body.appendChild(U.el('p', { text: L.goal }));
    body.appendChild(U.el('p', { class: 'muted', text: L.pass.text }));

    var cl = U.el('p', { class: 'muted', text: 'Kontrasty: '
      + L.contrastIds.map(Perception.contrastLabel).join(' · ') });
    body.appendChild(cl);

    if (status === 'locked') {
      body.appendChild(U.el('p', { class: 'fb bad', text:
        'Ta lekcja jest jeszcze zamknięta. Kolejność w module nie jest przypadkowa: '
        + 'rozróżnianie tonów w trójkach nie ma sensu, dopóki nie słyszysz ich w parach.' }));
      App.openSheet(body);
      return;
    }
    if (status !== 'open') {
      var st = Perception.lessonState(L.id);
      body.appendChild(U.el('p', { class: 'fb ok', text:
        status === 'passed' ? 'Zaliczona ' + st.date + ' — ' + st.score + ' z ' + st.total + '.'
          : (status === 'diagnosed' ? 'Zwolniona diagnozą percepcyjną ' + st.date + '.'
            : 'Pominięta.') }));
    }

    var go = U.el('button', { class: 'btn gold', type: 'button',
      text: status === 'open' ? 'Zacznij lekcję' : 'Powtórz lekcję' });
    go.addEventListener('click', function () { App.closeSheet(); startLesson(L); });
    body.appendChild(U.el('div', { class: 'btn-row' }, [go]));
    App.openSheet(body);
  }

  function startLesson(L) {
    Perception.start(L);
    state.mode = 'lesson';
    View.render();
  }

  /* --------------------------------------------------------- przebieg lekcji */

  function renderLessonRun(root) {
    var run = Perception.run;
    if (Perception.done()) { renderLessonResult(root); return; }
    var task = Perception.current();

    var head = U.el('div', { class: 'card' });
    head.appendChild(U.el('h2', { text: run.lesson.number + '. ' + run.lesson.title }));
    head.appendChild(U.el('p', { class: 'muted', text:
      Perception.progressText() + ' · trafnych: ' + run.correct
      + ' · do zaliczenia trzeba ' + run.lesson.pass.required }));
    var bar = U.el('div', { class: 'progress' });
    bar.appendChild(U.el('i', { style: 'width:'
      + Math.round(run.at / run.tasks.length * 100) + '%' }));
    head.appendChild(bar);
    root.appendChild(head);

    var box = U.el('div', { class: 'card m0-task' });
    root.appendChild(box);
    renderTask(box, task, function (res) {
      Perception.answer(task, res);
    }, function () { View.render(); }, run.lesson.pass);

    var quit = U.el('button', { class: 'btn ghost', type: 'button', text: 'Przerwij lekcję' });
    quit.addEventListener('click', function () {
      Player.stop();
      Perception.run = null;
      state.mode = 'map';
      View.render();
    });
    root.appendChild(U.el('div', { class: 'btn-row' }, [quit]));
  }

  function renderLessonResult(root) {
    var result = Perception.finish();
    var run = Perception.run;
    var box = U.el('div', { class: 'card' });
    box.appendChild(U.el('h2', { text: result.passed ? 'Zaliczone' : 'Jeszcze nie tym razem' }));
    box.appendChild(U.el('p', { class: result.passed ? 'fb ok' : 'fb bad', text:
      result.correct + ' z ' + result.total + ' trafnych odpowiedzi. Próg: '
      + result.required + ' (' + run.lesson.pass.accuracy + '%).' }));
    say((result.passed ? 'Lekcja zaliczona. ' : 'Lekcja niezaliczona. ')
      + result.correct + ' z ' + result.total + ' trafnych odpowiedzi.');

    if (!result.passed) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Próg w tym module jest wyższy niż w lekcjach słownikowych, bo mierzy co innego. '
        + 'Wiedzę można mieć częściową; słyszenie kontrastu albo jest, albo go nie ma. '
        + 'Wynik w okolicy losowania znaczy, że ucho jeszcze nie rozróżnia — powtórz lekcję.' }));
    }
    if (result.weakContrasts.length) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Kontrasty, które sprawiły kłopot, trafiły do powtórek:' }));
      var ul = U.el('ul', { class: 'plain-list' });
      result.weakContrasts.forEach(function (cid) {
        ul.appendChild(U.el('li', { text: Perception.contrastLabel(cid) }));
      });
      box.appendChild(ul);
    }

    var again = U.el('button', { class: 'btn', type: 'button',
      text: result.passed ? 'Powtórz lekcję' : 'Spróbuj jeszcze raz' });
    again.addEventListener('click', function () { startLesson(run.lesson); });
    var back = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wróć do mapy modułu' });
    back.addEventListener('click', function () {
      Perception.run = null;
      state.mode = 'map';
      View.render();
    });
    var buttons = [again, back];
    if (result.passed) {
      var nx = Perception.next();
      if (nx) {
        var go = U.el('button', { class: 'btn gold', type: 'button', text: 'Następna lekcja' });
        go.addEventListener('click', function () { startLesson(nx); });
        buttons = [go, back, again];
      } else {
        var toCourse = U.el('button', { class: 'btn gold', type: 'button',
          text: 'Moduł skończony — przejdź do kursu' });
        toCourse.addEventListener('click', function () {
          Perception.run = null;
          state.mode = 'map';
          App.go('course');
        });
        buttons = [toCourse, back, again];
      }
    }
    box.appendChild(U.el('div', { class: 'btn-row' }, buttons));
    root.appendChild(box);
    buttons[0].focus();
    Perception.run = null;
  }

  /* ------------------------------------------------------- przebieg diagnozy */

  function renderDiagnosticRun(root) {
    var d = Perception.diag;
    if (Perception.diagnosticDone()) { renderDiagnosticResult(root); return; }
    var task = Perception.currentDiagnostic();

    var head = U.el('div', { class: 'card' });
    head.appendChild(U.el('h2', { text: 'Diagnoza percepcyjna' }));
    head.appendChild(U.el('p', { class: 'muted', text:
      'Zadanie ' + (d.at + 1) + ' z ' + d.tasks.length
      + ' · sprawdzamy, które kontrasty już słyszysz' }));
    var bar = U.el('div', { class: 'progress' });
    bar.appendChild(U.el('i', { style: 'width:' + Math.round(d.at / d.tasks.length * 100) + '%' }));
    head.appendChild(bar);
    root.appendChild(head);

    var box = U.el('div', { class: 'card m0-task' });
    root.appendChild(box);
    renderTask(box, task, function (res) {
      Perception.answerDiagnostic(task, res);
    }, function () { View.render(); }, null);
  }

  function renderDiagnosticResult(root) {
    var result = Perception.finishDiagnostic();
    var box = U.el('div', { class: 'card' });
    box.appendChild(U.el('h2', { text: 'Mapa Twojego słuchu' }));
    box.appendChild(U.el('p', { class: 'fb ok', text:
      result.score + ' z ' + result.total + ' trafnych odpowiedzi.' }));
    say('Diagnoza skończona. ' + result.score + ' z ' + result.total + ' trafnych odpowiedzi.');
    box.appendChild(U.el('p', { class: 'muted', text: Perception.info().diagnostic.mastery }));
    box.appendChild(contrastMapTable(result));

    if (result.freed.length) {
      box.appendChild(U.el('p', { class: 'fb ok', text:
        result.freed.length + ' ' + U.plural(result.freed.length, 'lekcja została', 'lekcje zostały', 'lekcji zostało')
        + ' oznaczonych jako zdane — te kontrasty już słyszysz.' }));
    }
    if (result.weakContrasts.length) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Do powtórek trafiło ' + result.weakContrasts.length + ' '
        + U.plural(result.weakContrasts.length, 'kontrast', 'kontrasty', 'kontrastów') + ': '
        + result.weakContrasts.map(Perception.contrastLabel).join(' · ') }));
    }

    var back = U.el('button', { class: 'btn gold', type: 'button', text: 'Wróć do mapy modułu' });
    back.addEventListener('click', function () {
      Perception.diag = null;
      state.mode = 'map';
      View.render();
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [back]));
    root.appendChild(box);
    back.focus();
  }

  /* Mapa mocnych i słabych kontrastów — tabela, nie wykres, bo to jest lista
     nazw z oceną, a nie przebieg w czasie. */
  function contrastMapTable(result) {
    var wrap = U.el('div');
    var table = U.el('table', { class: 'data-table' });
    table.appendChild(U.el('caption', { text: 'Rodziny kontrastów' }));
    var thead = U.el('thead');
    var hr = U.el('tr');
    ['Kontrast', 'Trafnych', 'Ocena'].forEach(function (h) {
      hr.appendChild(U.el('th', { scope: 'col', text: h }));
    });
    thead.appendChild(hr);
    table.appendChild(thead);
    var tbody = U.el('tbody');
    Perception.families().forEach(function (f) {
      var b = (result.byFamily || {})[f.id];
      if (!b || !b.asked) return;
      var tr = U.el('tr');
      tr.appendChild(U.el('th', { scope: 'row', text: f.label }));
      tr.appendChild(U.el('td', { text: b.correct + ' / ' + b.asked }));
      tr.appendChild(U.el('td', { text: b.correct === b.asked ? 'słyszysz' : 'do treningu' }));
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    wrap.appendChild(table);
    return wrap;
  }

  /* ----------------------------------------------------------- jedno zadanie */

  var TYPE_LABEL = {
    'same-diff': 'To samo czy inne',
    'odd-one-out': 'Który jest inny',
    'tone-scale': 'Wskaż ton na skali',
    'count-syllables': 'Policz sylaby',
    'vowel-length': 'Długa czy krótka',
    'aspiration': 'Z przydechem czy bez'
  };

  /* onAnswer(choice) → zapisuje wynik; onNext() → przechodzi dalej.
     Funkcja jest wspólna dla lekcji i diagnozy, bo zadanie wygląda tak samo. */
  function renderTask(box, task, onAnswer, onNext, pass) {
    clearHandlers();
    U.clear(box);
    box.appendChild(U.el('p', { class: 'muted m0-kind', text: TYPE_LABEL[task.type] || task.type }));
    box.appendChild(U.el('p', { class: 'bc-pl', text: task.prompt }));

    /* Sterowanie dźwiękiem. Przycisk odtworzenia dostaje focus od razu, więc
       spacja działa bez szukania po ekranie. */
    var playBtn = U.el('button', { class: 'btn gold play-btn', type: 'button',
      'aria-pressed': 'false',
      'aria-label': 'Odtwórz ponownie (klawisz R)' });
    playBtn.appendChild(U.icon('play'));
    playBtn.appendChild(U.el('span', { text: task.playIds.length > 1
      ? 'Odtwórz ' + task.playIds.length + ' dźwięki' : 'Odtwórz' }));

    var replay = function () { playSeries(task.playIds, { btn: playBtn }); };
    playBtn.addEventListener('click', replay);
    state.replay = replay;

    box.appendChild(U.el('div', { class: 'btn-row' }, [playBtn]));
    box.appendChild(U.el('p', { class: 'muted m0-keys', text:
      'Klawiatura: cyfry wybierają odpowiedź, R powtarza dźwięk, '
      + 'P porównuje oba warianty, Enter przechodzi dalej.' }));

    /* Zapis fonetyczny — zasłonięty do czasu odpowiedzi. */
    var reveal = U.el('div', { class: 'm0-reveal', hidden: 'hidden' });
    box.appendChild(reveal);

    var opts = U.el('div', { class: 'm0-options', role: 'group',
      'aria-label': 'Odpowiedzi' });
    box.appendChild(opts);

    var feedback = U.el('div');
    box.appendChild(feedback);

    var answered = false;
    task.options.forEach(function (label, i) {
      var b = U.el('button', {
        class: 'opt' + (task.type === 'tone-scale' ? ' opt-tone' : ''),
        type: 'button',
        'aria-label': 'Odpowiedź ' + (i + 1) + ': ' + label
      });
      if (task.type === 'tone-scale') {
        b.appendChild(U.toneMark(label.replace(/^ton\s+/, '')));
      }
      b.appendChild(U.el('span', { class: 'opt-num', 'aria-hidden': 'true', text: String(i + 1) }));
      b.appendChild(U.el('span', { text: label }));
      b.addEventListener('click', function () {
        if (answered) return;
        answered = true;
        var ok = label === task.answer;
        onAnswer(label);
        showResult(ok, b);
      });
      opts.appendChild(b);
      state.options.push(b);
    });

    function showResult(ok, chosen) {
      state.options.forEach(function (b) {
        b.disabled = true;
        var txt = b.getAttribute('aria-label').replace(/^Odpowiedź \d+: /, '');
        if (txt === task.answer) b.classList.add('correct');
      });
      if (!ok && chosen) chosen.classList.add('wrong');

      /* Zapis odsłaniamy dopiero teraz — wcześniej byłby ściągą. */
      U.clear(reveal);
      reveal.hidden = false;
      reveal.appendChild(U.el('h3', { text: 'Co usłyszałeś' }));
      var uniq = [];
      task.playIds.forEach(function (id) { if (uniq.indexOf(id) === -1) uniq.push(id); });
      uniq.forEach(function (id) {
        var s = stimOf(id);
        if (!s) return;
        var row = U.el('div', { class: 'm0-stim' });
        row.appendChild(U.renderPhonetic(s.phonetic, { hideTones: false }));
        if (s.polish) row.appendChild(U.el('span', { class: 'muted', text: s.polish }));
        var pb = U.el('button', { class: 'icon-btn', type: 'button',
          'aria-label': 'Posłuchaj: ' + s.phonetic });
        pb.appendChild(U.icon('play'));
        pb.addEventListener('click', function () { Player.play(s, { btn: pb }); });
        row.appendChild(pb);
        reveal.appendChild(row);
      });

      var msg = (ok ? 'Dobrze. ' : 'Źle. Poprawna odpowiedź: ' + task.answer + '. ')
        + (task.explain || '');
      feedback.appendChild(U.el('p', { class: ok ? 'fb ok' : 'fb bad', text: msg }));
      say(msg);

      var row = U.el('div', { class: 'btn-row' });

      /* Porównanie obu wariantów jeden po drugim. To jest sedno treningu:
         różnicy nie słychać w pojedynczym bodźcu, tylko w zestawieniu. */
      if (task.compare && task.compare.length >= 2) {
        var cmp = U.el('button', { class: 'btn', type: 'button',
          'aria-label': 'Porównaj oba warianty jeden po drugim (klawisz P)' });
        cmp.appendChild(U.icon('listen'));
        cmp.appendChild(U.el('span', { text: 'Porównaj oba warianty' }));
        var doCompare = function () { playCompare(task.compare, true); };
        cmp.addEventListener('click', doCompare);
        state.compare = doCompare;
        row.appendChild(cmp);
      }

      var again = U.el('button', { class: 'btn ghost', type: 'button',
        'aria-label': 'Odtwórz zadanie jeszcze raz (klawisz R)', text: 'Jeszcze raz' });
      again.addEventListener('click', replay);
      row.appendChild(again);

      var nb = U.el('button', { class: 'btn gold', type: 'button', text: 'Dalej' });
      var advance = function () { Player.stop(); onNext(); };
      nb.addEventListener('click', advance);
      state.advance = advance;
      row.appendChild(nb);

      feedback.appendChild(row);
      nb.focus();
    }

    /* Bodziec leci sam, od razu — ćwiczenie słuchowe nie powinno wymagać
       kliknięcia, żeby w ogóle się zacząć. */
    setTimeout(replay, 120);
    playBtn.focus();
  }

  /* To samo zadanie, ale wywoływane spoza modułu — z ekranu powtórek.
     Różnica jest jedna: wynik wraca jako `ok`, bo powtórka ocenia kartę
     kontrastu, a nie postęp w lekcji. */
  View.renderDrill = function (box, task, onAnswer, onNext) {
    bindKeys();
    renderTask(box, task, function (choice) {
      onAnswer(choice === task.answer);
    }, onNext, null);
  };

  View.playSeries = playSeries;
  View.playCompare = playCompare;
  View.reset = function () { state.mode = 'map'; Perception.run = null; Perception.diag = null; };
  View.state = state;

  global.M0View = View;
})(window);
