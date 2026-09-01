/* Thai All-in-One — sceny: rozumienie dłuższej rozmowy.

   Wszystkie wcześniejsze ćwiczenia rozumienia kończyły się na jednym zdaniu.
   Scena pyta o co innego: czy uczący się utrzymał wątek przez kilkadziesiąt
   wymian i wie, o co w tej rozmowie chodziło — nawet jeśli co piątego słowa
   nie zna. Dlatego żadne pytanie w tym ekranie nie da się rozstrzygnąć
   z jednego zdania; wszystkie dotyczą całości.

   Zapis jest domyślnie schowany. To celowe: gdy tekst leży przed oczami,
   ćwiczenie zmienia się w czytanie ze słuchem w tle. */
(function (global) {
  'use strict';

  /* ==================================================== WSPÓLNY WYBÓR TEMPA

     Trzy ekrany rozumienia (Sceny, Słuchanie ekstensywne, Słuchanie) używają
     jednego wyboru tempa, zapamiętanego między sesjami. Postęp jest liczony
     osobno dla każdego tempa — Progress.tempoAnswer — więc uczący się musi
     wiedzieć, w którym tempie właśnie odpowiada. Stąd wybór jest widoczny na
     każdym z tych ekranów, a nie schowany w Ustawieniach. */

  var CompTempo = {
    current: U.store.get('compTempo', 'natural')
  };

  CompTempo.set = function (id) {
    CompTempo.current = id;
    U.store.set('compTempo', id);
  };

  CompTempo.def = function () { return Player.tempoDef(CompTempo.current); };

  /* Pasek wyboru tempa razem ze stanem drabiny dla danego ćwiczenia.
     Uczący się widzi od razu, które tempo ma już zaliczone, a na którym stoi. */
  CompTempo.row = function (exercise, onChange) {
    var wrap = U.el('div', { class: 'tempo-row' });
    wrap.appendChild(U.el('p', { class: 'muted tempo-lead', text:
      'Tempo odsłuchu. Każde liczy się osobno — zaliczenie przy 0,7x nie '
      + 'zalicza 1,0x ani 1,4x.' }));
    var group = U.el('div', { class: 'mode-row', role: 'group',
      'aria-label': 'Tempo odsłuchu' });

    Progress.tempoSteps().forEach(function (step) {
      var cell = Progress.tempoCell(exercise, step.id);
      var chip = U.el('button', {
        class: 'chip tempo-chip' + (cell.passed ? ' done' : ''),
        type: 'button',
        'data-tempo': step.id,
        'aria-pressed': CompTempo.current === step.id ? 'true' : 'false'
      });
      chip.appendChild(U.el('span', { text: step.label }));
      var state = cell.passed ? 'zaliczone'
        : cell.answers ? cell.correct + '/' + cell.answers
        : 'bez podejścia';
      chip.appendChild(U.el('span', { class: 'tempo-state', text: state }));
      chip.setAttribute('aria-label',
        'Tempo ' + step.label + ' — ' + step.hint + ', ' + state);
      chip.addEventListener('click', function () {
        CompTempo.set(step.id);
        if (onChange) onChange(step.id);
      });
      group.appendChild(chip);
    });
    wrap.appendChild(group);

    var stuck = Progress.tempoStuckAt(exercise);
    wrap.appendChild(U.el('p', { class: 'muted', text: stuck
      ? 'W tym ćwiczeniu stoisz na tempie ' + Progress.tempoLabel(stuck) + '.'
      : 'To ćwiczenie masz zaliczone we wszystkich trzech tempach.' }));
    return wrap;
  };

  global.CompTempo = CompTempo;

  /* ============================================================== SCENY */

  var Scenes = { current: null, showText: false };

  Scenes.ready = function () { return !!(DB.scenes && DB.scenes.length); };

  Scenes.ensureData = function () { return DB.ensureScenes(); };

  Scenes.list = function (level) {
    var all = DB.scenes || [];
    if (!level) return all.slice();
    var picked = all.filter(function (s) { return s.level === level; });
    return picked.length ? picked : all.slice();
  };

  /* Scena proponowana na wejściu: z poziomu nauki, najchętniej taka,
     której uczący się jeszcze nie przerabiał. */
  Scenes.suggest = function (level) {
    var pool = Scenes.list(level);
    var fresh = pool.filter(function (s) {
      return !(Progress.data.seen && Progress.data.seen['scene:' + s.id]);
    });
    var from = fresh.length ? fresh : pool;
    return from.length ? from[0] : null;
  };

  Scenes.minutes = function (item, tempo) {
    var sec = (item.estSeconds || {})[tempo || CompTempo.current] || 0;
    var m = Math.floor(sec / 60), s = Math.round(sec % 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
  };

  /* --------------------------------------------------------- silnik pytań */

  /* Jeden renderer pytań dla sceny i dla trybu ekstensywnego — pytania są
     tego samego kształtu, a różni je tylko to, kiedy się pojawiają.

     Po odpowiedzi zawsze pokazujemy uzasadnienie. W ćwiczeniu na sens całości
     samo „dobrze / źle” niczego nie uczy: uczący się musi zobaczyć, co
     w scenie prowadziło do tej odpowiedzi. */
  Scenes.renderQuestion = function (box, question, opts) {
    opts = opts || {};
    var wrap = U.el('div', { class: 'q-card' });
    if (opts.counter) {
      wrap.appendChild(U.el('p', { class: 'muted', text: opts.counter }));
    }
    wrap.appendChild(U.el('p', { class: 'q-prompt', text: question.prompt }));

    var answered = false;
    var list = U.el('div', { class: 'options' });
    question.options.forEach(function (text, i) {
      var btn = U.el('button', { class: 'btn option', type: 'button', text: text });
      btn.addEventListener('click', function () {
        if (answered) return;
        answered = true;
        var ok = i === question.answer;
        btn.classList.add(ok ? 'correct' : 'wrong');
        if (!ok) {
          U.$$('.option', list).forEach(function (b, j) {
            if (j === question.answer) b.classList.add('correct');
          });
        }
        U.$$('.option', list).forEach(function (b) { b.disabled = true; });

        var fb = U.el('div', { class: ok ? 'fb ok' : 'fb bad', role: 'status' });
        fb.appendChild(U.el('strong', { text: ok ? 'Dobrze. ' : 'Nie tym razem. ' }));
        fb.appendChild(document.createTextNode(
          ok ? '' : 'Poprawnie: ' + question.options[question.answer] + '.'));
        wrap.appendChild(fb);
        if (question.explain) {
          wrap.appendChild(U.el('p', { class: 'muted q-explain', text: question.explain }));
        }
        if (opts.onAnswer) opts.onAnswer(ok, wrap);
      });
      list.appendChild(btn);
    });
    wrap.appendChild(list);
    box.appendChild(wrap);
    return wrap;
  };

  /* Zestaw pytań po kolei, z podsumowaniem na końcu. */
  Scenes.runQuestions = function (box, questions, opts) {
    opts = opts || {};
    var at = 0, correct = 0;
    function step() {
      U.clear(box);
      if (at >= questions.length) {
        if (opts.onDone) opts.onDone({ correct: correct, total: questions.length });
        return;
      }
      var q = questions[at];
      Scenes.renderQuestion(box, q, {
        counter: 'Pytanie ' + (at + 1) + ' z ' + questions.length
          + ' · poziom szczegółowości ' + q.tier,
        onAnswer: function (ok, card) {
          if (ok) correct += 1;
          if (opts.onAnswer) opts.onAnswer(ok, q);
          var next = U.el('button', { class: 'btn', type: 'button',
            text: at + 1 >= questions.length ? 'Podsumowanie' : 'Następne pytanie' });
          next.addEventListener('click', function () { at += 1; step(); });
          card.appendChild(U.el('div', { class: 'btn-row' }, [next]));
          next.focus();
        }
      });
    }
    step();
    return { restart: step };
  };

  /* ------------------------------------------------------------- odsłuch */

  /* Odtworzenie ciągu kwestii z podświetleniem bieżącej. Kwestie mają
     zapisaną płeć mówiącego, więc role brzmią dwoma głosami — bez tego
     scena zlewa się w monolog i przestaje być rozmową. */
  Scenes.play = function (lines, opts) {
    opts = opts || {};
    var prepared = G.viewAll(lines).map(function (line, i) {
      var copy = {};
      Object.keys(line).forEach(function (k) { copy[k] = line[k]; });
      copy.__speaker = G.speakerOf(line);
      copy.__key = lines[i].__key;
      copy.role = lines[i].role;
      return copy;
    });
    Player.playSequence(prepared, {
      btn: opts.btn,
      tempo: opts.tempo || CompTempo.current,
      noise: opts.noise,
      onstep: function (line, i) {
        if (opts.onstep) opts.onstep(line, i);
      },
      onend: opts.onend
    });
    return prepared;
  };

  /* ---------------------------------------------------------- ekran sceny */

  Scenes.render = function (root) {
    U.clear(root);
    if (!Scenes.ready()) {
      root.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję sceny…' }));
      return;
    }
    var scene = Scenes.current || Scenes.suggest(
      App.settings.practiceLevel || Progress.entryLevel());
    if (!scene) {
      root.appendChild(U.el('p', { class: 'muted', text: 'Brak scen do pokazania.' }));
      return;
    }
    Scenes.current = scene;

    /* --- nagłówek --- */
    var head = U.el('div', { class: 'card' });
    head.appendChild(U.el('h2', { text: scene.title }));
    head.appendChild(U.el('p', { class: 'muted', text:
      scene.level + ' · ' + scene.lineCount + ' '
      + U.plural(scene.lineCount, 'kwestia', 'kwestie', 'kwestii')
      + ' · ' + scene.beats.length + ' '
      + U.plural(scene.beats.length, 'część', 'części', 'części')
      + ' · około ' + Scenes.minutes(scene) + ' w tempie '
      + Progress.tempoLabel(CompTempo.current) }));
    head.appendChild(U.el('p', { text: scene.situation }));
    root.appendChild(head);

    /* --- tempo --- */
    var tempoCard = U.el('div', { class: 'card' });
    tempoCard.appendChild(CompTempo.row('scene', function () {
      Scenes.render(root);
    }));
    root.appendChild(tempoCard);

    /* --- odsłuch --- */
    var listenCard = U.el('div', { class: 'card' });
    listenCard.appendChild(U.el('h2', { text: 'Posłuchaj całej sceny' }));
    listenCard.appendChild(U.el('p', { class: 'muted', text:
      'Nie zatrzymuj się na słowach, których nie znasz. Zadanie brzmi: '
      + 'zrozumieć, o co chodzi — nie przetłumaczyć każde zdanie.' }));

    var lines = DB.sceneLines(scene);
    var transcript = U.el('div', { class: 'scene-lines' });
    var playAll = U.el('button', { class: 'btn gold play-btn', type: 'button',
      'aria-pressed': 'false' });
    playAll.appendChild(U.icon('play'));
    playAll.appendChild(U.el('span', { text: 'Odtwórz scenę' }));
    playAll.addEventListener('click', function () {
      Progress.data.seen['scene:' + scene.id] = 1;
      Progress.save();
      Scenes.play(lines, {
        btn: playAll,
        onstep: function (line) {
          U.$$('.scene-line', transcript).forEach(function (n) {
            n.classList.remove('current');
          });
          var node = U.$('[data-key="' + line.__key + '"]', transcript);
          if (node) node.classList.add('current');
        },
        onend: function () {
          U.$$('.scene-line', transcript).forEach(function (n) {
            n.classList.remove('current');
          });
        }
      });
    });

    var toggle = U.el('button', { class: 'chip', type: 'button',
      'aria-pressed': Scenes.showText ? 'true' : 'false',
      text: Scenes.showText ? 'Ukryj zapis' : 'Pokaż zapis' });
    toggle.addEventListener('click', function () {
      Scenes.showText = !Scenes.showText;
      Scenes.render(root);
    });
    listenCard.appendChild(U.el('div', { class: 'btn-row' }, [playAll, toggle]));

    /* --- zapis --- */
    if (Scenes.showText) {
      var beatAt = -1;
      lines.forEach(function (line) {
        if (line.__beat !== beatAt) {
          beatAt = line.__beat;
          var beat = scene.beats[beatAt];
          transcript.appendChild(U.el('p', { class: 'scene-beat',
            text: 'Część ' + (beatAt + 1) + ' — ' + beat.label }));
        }
        var view = G.view(line);
        var row = U.el('div', { class: 'scene-line', 'data-key': line.__key });
        row.appendChild(U.el('span', { class: 'role' + (line.role === 'B' ? ' b' : ''),
          text: line.role }));
        var mid = U.el('div');
        mid.appendChild(U.el('div', { class: 'l-ph', text: App.settings.hideTones
          ? U.stripTones(view.thaiPhonetic) : view.thaiPhonetic }));
        mid.appendChild(U.el('div', { class: 'l-pl', text: view.polish }));
        row.appendChild(mid);
        var b = U.el('button', { class: 'icon-btn', type: 'button',
          'aria-label': 'Posłuchaj tej kwestii' });
        b.appendChild(U.icon('play'));
        b.addEventListener('click', function () {
          Player.play(view, { btn: b, role: line.role,
            gender: G.speakerOf(line), tempo: CompTempo.current });
        });
        row.appendChild(b);
        transcript.appendChild(row);
      });
      listenCard.appendChild(transcript);
    } else {
      listenCard.appendChild(transcript);
      listenCard.appendChild(U.el('p', { class: 'muted', text:
        'Zapis jest schowany. Odsłuchaj najpierw bez niego — z tekstem przed '
        + 'oczami ćwiczenie zamienia się w czytanie.' }));
    }
    root.appendChild(listenCard);

    /* --- słowa kluczowe --- */
    if (scene.keywords && scene.keywords.length) {
      var kw = U.el('div', { class: 'card' });
      kw.appendChild(U.el('h2', { text: 'Słowa kluczowe sceny' }));
      kw.appendChild(U.el('p', { class: 'muted', text:
        'Te wracają w scenie najczęściej. Reszty nie musisz znać, żeby '
        + 'zrozumieć, o co chodzi.' }));
      var chips = U.el('div', { class: 'chip-list' });
      scene.keywords.forEach(function (k) {
        var chip = U.el('button', { class: 'kw-chip', type: 'button' });
        chip.appendChild(U.el('span', { text: App.settings.hideTones
          ? U.stripTones(k.thaiPhonetic) : k.thaiPhonetic }));
        chip.appendChild(U.el('span', { class: 'tempo-state', text: k.polish }));
        chip.setAttribute('aria-label', k.thaiPhonetic + ' — ' + k.polish
          + ', pada ' + k.count + ' razy');
        chip.addEventListener('click', function () {
          var rec = DB.any(k.id);
          if (rec) Player.play(G.view(rec), { btn: chip, tempo: CompTempo.current });
        });
        chips.appendChild(chip);
      });
      kw.appendChild(chips);
      root.appendChild(kw);
    }

    /* --- pytania --- */
    var qCard = U.el('div', { class: 'card' });
    qCard.appendChild(U.el('h2', { text: 'Czy wiesz, o co chodziło?' }));
    qCard.appendChild(U.el('p', { class: 'muted', text:
      'Pytania dotyczą całej sceny. Żadnego nie da się rozstrzygnąć '
      + 'z pojedynczego zdania.' }));
    var qArea = U.el('div');
    qCard.appendChild(qArea);

    var start = U.el('button', { class: 'btn', type: 'button', text: 'Zacznij pytania' });
    start.addEventListener('click', function () {
      var qs = (scene.questions || []).slice().sort(function (a, b) {
        return a.tier - b.tier;
      });
      start.hidden = true;
      Scenes.runQuestions(qArea, qs, {
        onAnswer: function (ok) {
          Progress.answer('scene:' + scene.id, ok, { mode: 'scene' });
          Progress.tempoAnswer('scene', CompTempo.current, ok);
        },
        onDone: function (result) {
          U.clear(qArea);
          qArea.appendChild(U.el('p', { class: 'fb ok', text:
            'Scena zaliczona: ' + result.correct + ' z ' + result.total
            + ' odpowiedzi trafnych, w tempie '
            + Progress.tempoLabel(CompTempo.current) + '.' }));
          var again = U.el('button', { class: 'btn ghost', type: 'button',
            text: 'Następna scena' });
          again.addEventListener('click', function () {
            Scenes.current = null;
            Scenes.showText = false;
            Scenes.render(root);
          });
          qArea.appendChild(U.el('div', { class: 'btn-row' }, [again]));
        }
      });
    });
    qCard.appendChild(U.el('div', { class: 'btn-row' }, [start]));
    root.appendChild(qCard);
  };

  global.Scenes = Scenes;
})(window);
