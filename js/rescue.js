/* Thai All-in-One — strategie ratunkowe i dryl odruchu.

   Aplikacja nie nauczy prowadzenia rozmowy i nie udaje, że nauczy. Ale rozmowa
   nie rozsypuje się na braku swobody — rozsypuje się na jednej sekundzie ciszy
   po zdaniu, którego uczący się nie zrozumiał. Prośba o powtórzenie, o wolniej,
   o prościej, potwierdzenie własnymi słowami: to są gotowe formuły.

   DLACZEGO SAM PRZEGLĄD FORMUŁ NIE WYSTARCZA
   ------------------------------------------
   Formuła znana, ale wypowiedziana po czterech sekundach namysłu, nie
   uratowała już niczego: rozmówca zdążył pójść dalej albo powtórzyć to samo,
   tak samo szybko. Dlatego obok listy stoi dryl, w którym kwestia jest podana
   TAK, ŻEBY SIĘ NIE DAŁO — za szybko, za cicho, w hałasie albo z nieznanym
   słowem — a zadaniem jest zareagować właściwą formułą w oknie kilku sekund.

   Brak reakcji w oknie liczy się jak zła odpowiedź. To nie jest surowość dla
   surowości: w rozmowie brak reakcji też się tak liczy.

   PĘTLA NAPRAWCZA
   ---------------
   Po reakcji aplikacja odtwarza kwestię PONOWNIE — wolniej albo bez hałasu —
   i pyta, co zostało zrozumiane. Bez tego drugiego kroku dryl uczyłby
   wypowiadania formuły, a nie naprawiania rozmowy; a formuła, po której nadal
   się nie rozumie, jest tylko uprzejmym sposobem na utknięcie w tym samym
   miejscu. */
(function (global) {
  'use strict';

  var Rescue = { current: null };

  Rescue.ensureData = function () {
    return Promise.all([DB.ensureRescue(), DB.ensureDialogues()]);
  };
  Rescue.loaded = function () { return !!(DB.rescue && DB.rescue.records); };

  function data() { return DB.rescue || null; }

  Rescue.formulas = function () { return (data() && data().records) || []; };
  Rescue.triggers = function () { return (data() && data().triggers) || []; };
  Rescue.lessons = function () { return (data() && data().lessons) || []; };
  Rescue.items = function () { return (data() && data().items) || []; };
  Rescue.config = function () { return (data() && data().drill) || { windowMs: 4000 }; };

  Rescue.byGroup = function (group) {
    var list = Rescue.formulas();
    for (var i = 0; i < list.length; i++) if (list[i].group === group) return list[i];
    return null;
  };

  /* Rejestr: formalny czy potoczny. Wybór należy do sytuacji, nie do gustu —
     notatka kulturowa przy każdej formule mówi, kiedy który jest właściwy. */
  Rescue.register = function () { return U.store.get('rescueRegister', 'potoczny'); };
  Rescue.setRegister = function (r) { U.store.set('rescueRegister', r); };

  Rescue.form = function (formula, register) {
    var want = register || Rescue.register();
    var forms = formula.forms || [];
    for (var i = 0; i < forms.length; i++) if (forms[i].register === want) return forms[i];
    return forms[0] || null;
  };

  /* ==================================================== PRZEGLĄD FORMUŁ */

  Rescue.renderList = function (box) {
    box.appendChild(U.el('p', { class: 'muted', text:
      'Czternaście formuł, każda w rejestrze formalnym i potocznym, każda '
      + 'z wariantem męskim i żeńskim. Aplikacja pokazuje wariant zgodny '
      + 'z Twoim ustawieniem „Mówię jako”; obie formy widać w szczegółach.' }));

    var row = U.el('div', { class: 'mode-row', role: 'group', 'aria-label': 'Rejestr' });
    [['potoczny', 'potoczny'], ['formalny', 'formalny']].forEach(function (pair) {
      var chip = U.el('button', { class: 'chip', type: 'button',
        'aria-pressed': Rescue.register() === pair[0] ? 'true' : 'false',
        text: 'rejestr ' + pair[1] });
      chip.addEventListener('click', function () {
        Rescue.setRegister(pair[0]);
        U.clear(box);
        Rescue.renderList(box);
      });
      row.appendChild(chip);
    });
    box.appendChild(row);

    Rescue.formulas().forEach(function (f) {
      var card = U.el('div', { class: 'card rescue-card' });
      card.appendChild(U.el('h2', { text: f.title }));
      card.appendChild(U.el('p', { class: 'muted', text: f.why }));

      var form = Rescue.form(f);
      var view = G.view(form);
      var play = U.el('button', { class: 'btn gold play-btn', type: 'button',
        'aria-label': 'Odtwórz: ' + f.title });
      play.appendChild(U.icon('play'));
      play.appendChild(U.el('span', { text: 'Posłuchaj' }));
      play.addEventListener('click', function () { Player.play(view, { btn: play }); });

      card.appendChild(U.renderPhonetic(view.thaiPhonetic, {}));
      card.appendChild(U.el('p', { text: view.polish }));
      card.appendChild(U.el('div', { class: 'btn-row' }, [play]));

      /* Obie formy płci obok siebie. Uczący się używa jednej, ale ze słuchu
         musi rozpoznawać obie — usłyszy je od rozmówców obu płci. */
      var other = form.genderVariant && form.genderVariant.female;
      if (other) {
        var both = U.el('p', { class: 'muted small' });
        both.appendChild(U.el('span', { text: 'mężczyzna: ' + form.thaiPhonetic
          + ' · kobieta: ' + other.thaiPhonetic }));
        card.appendChild(both);
      }
      card.appendChild(U.el('p', { class: 'muted small', text: '⌁ ' + f.culturalNote }));
      box.appendChild(card);
    });
  };

  /* ======================================================= DRYL ODRUCHU */

  function itemsFor(triggerId) {
    return Rescue.items().filter(function (it) {
      return (!triggerId || it.trigger === triggerId) && !!DB.get(it.dialogueId);
    });
  }

  function lineOf(item) {
    var dlg = DB.get(item.dialogueId);
    if (!dlg || !dlg.lines) return null;
    for (var i = 0; i < dlg.lines.length; i++) {
      if (dlg.lines[i].index === item.line) return dlg.lines[i];
    }
    return null;
  }

  function triggerDef(id) {
    var list = Rescue.triggers();
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  }

  /* Zniekształcenie bodźca. Korzystamy z warstwy dźwiękowej sesji L: tempo,
     hałas tła i głośność. Nic nie jest tu nagrane — wszystko liczy się
     w przeglądarce, więc ten sam poziom trudności brzmi zawsze tak samo
     i dwa podejścia da się porównać. */
  function playDegraded(line, def, btn) {
    var d = def.degrade || {};
    var opts = { btn: btn, tempo: d.tempo || 'natural', role: line.role,
                 gender: G.speakerOf(line) };
    if (d.noise && global.DSP && DSP.supported()) {
      var s = U.store.get('settings', {});
      opts.noise = { kind: s.noiseKind || 'restaurant', level: d.noise };
    }
    if (d.rate) opts.rate = d.rate;
    if (d.volume) opts.volume = d.volume;
    Player.play(G.view(line), opts);
  }

  Rescue.renderDrill = function (box, onNext, forcedTrigger) {
    if (!Rescue.loaded()) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję materiał…' }));
      return;
    }
    var cfg = Rescue.config();
    var pool = itemsFor(forcedTrigger);
    if (!pool.length) pool = itemsFor(null);
    if (!pool.length) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Materiał drylu jeszcze się wczytuje. Spróbuj za chwilę.' }));
      return;
    }
    var item = pool[Math.floor(Math.random() * pool.length)];
    var line = lineOf(item);
    var def = triggerDef(item.trigger);
    if (!line || !def) { onNext(); return; }

    box.appendChild(U.el('p', { class: 'muted', text: cfg.lead }));
    var limit = Numbers.limitMs(cfg.windowMs);
    box.appendChild(U.el('p', { class: 'muted small', text: limit
      ? 'Okno reakcji: ' + (limit / 1000).toFixed(1).replace('.', ',') + ' s. '
        + 'Da się je wydłużyć albo wyłączyć w Ustawieniach.'
      : 'Okno reakcji wyłączone w Ustawieniach. Czas nadal jest mierzony '
        + 'i liczy się do statystyk — nie odcina tylko odpowiedzi.' }));

    box.appendChild(U.el('p', { class: 'trigger-label', text: def.label + ' — ' + def.lead }));
    var replay = U.el('button', { class: 'btn ghost play-btn', type: 'button' });
    replay.appendChild(U.icon('play'));
    replay.appendChild(U.el('span', { text: 'Odtwórz jeszcze raz (tak samo)' }));
    replay.addEventListener('click', function () { playDegraded(line, def, replay); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [replay]));

    /* Opcje: cztery formuły, z których część jest trafna dla tego wyzwalacza.
       Dystraktory są formułami PRAWDZIWYMI, tylko nie na tę sytuację —
       ćwiczenie ma rozstrzygać, KTÓRA formuła pasuje, a nie czy uczący się
       rozpoznaje sensowne zdanie tajskie wśród bzdur. */
    var accept = def.accept || [];
    var right = accept[Math.floor(Math.random() * accept.length)];
    var wrong = Rescue.formulas().map(function (f) { return f.group; })
      .filter(function (g) { return accept.indexOf(g) === -1; });
    var options = U.shuffle([right].concat(U.sample(wrong, 3)));

    var ctx = { mode: 'reflex', trigger: item.trigger };
    var answered = false;
    var list = U.el('div', { class: 'options' });

    function settle(group, auto) {
      if (answered) return;
      answered = true;
      clock.stop();
      var ms = clock.elapsed();
      var ok = !auto && accept.indexOf(group) !== -1;
      U.$$('.option', list).forEach(function (b) { b.disabled = true; });

      var fb = U.el('p', { class: ok ? 'fb ok' : 'fb bad', role: 'status' });
      fb.appendChild(U.el('strong', { text: auto
        ? 'Brak reakcji w oknie. ' : (ok ? 'Dobrze. ' : 'Nie ta formuła. ') }));
      fb.appendChild(document.createTextNode(auto
        ? 'W rozmowie cisza jest sygnałem, że skończyłeś — rozmówca pójdzie dalej.'
        : 'Pasowały tu: ' + accept.map(function (g) {
            var f = Rescue.byGroup(g); return f ? f.title.toLowerCase() : g;
          }).join(', ') + '.'));
      box.appendChild(fb);

      var verdict = Progress.reflexAnswer(item.trigger, ok, ms, !!auto);
      box.appendChild(U.el('p', { class: 'muted', text:
        'Czas reakcji: ' + (ms / 1000).toFixed(1).replace('.', ',') + ' s. ' + verdict.note }));

      repairStep();
    }

    var clock = new Numbers.Countdown(box, limit, function () { settle(null, true); });

    options.forEach(function (g) {
      var f = Rescue.byGroup(g);
      if (!f) return;
      var form = Rescue.form(f);
      var view = G.view(form);
      var btn = U.el('button', { class: 'btn option', type: 'button' });
      btn.appendChild(U.el('span', { class: 'opt-thai', text: view.thaiPhonetic }));
      btn.appendChild(U.el('span', { class: 'opt-pl', text: view.polish }));
      btn.setAttribute('aria-label', view.polish + ' — ' + view.thaiPhonetic);
      btn.addEventListener('click', function () {
        btn.classList.add(accept.indexOf(g) !== -1 ? 'correct' : 'wrong');
        Player.play(view, {});
        settle(g, false);
      });
      list.appendChild(btn);
    });
    box.appendChild(list);

    /* ------------------------------------------------ druga próba */

    function repairStep() {
      var step = U.el('div', { class: 'card' });
      box.appendChild(step);
      step.appendChild(U.el('h2', { text: 'Druga próba' }));
      step.appendChild(U.el('p', { class: 'muted', text:
        'Rozmówca powtarza — wolniej i bez hałasu. Teraz pytanie brzmi: '
        + 'czy formuła coś dała, czyli czy TERAZ rozumiesz.' }));

      var again = U.el('button', { class: 'btn gold play-btn', type: 'button' });
      again.appendChild(U.icon('play'));
      again.appendChild(U.el('span', { text: 'Odtwórz wolniej' }));
      again.addEventListener('click', function () {
        Player.play(G.view(line), { btn: again, tempo: def.repeatTempo || 'slow',
          role: line.role, gender: G.speakerOf(line), noAmbience: true });
      });
      step.appendChild(U.el('div', { class: 'btn-row' }, [again]));

      var opts = U.el('div', { class: 'options' });
      var picks = U.shuffle([item.check.answer].concat(item.check.foils || []));
      var done = false;
      picks.forEach(function (text) {
        var b = U.el('button', { class: 'btn option', type: 'button', text: text });
        b.addEventListener('click', function () {
          if (done) return;
          done = true;
          var ok = text === item.check.answer;
          b.classList.add(ok ? 'correct' : 'wrong');
          U.$$('.option', opts).forEach(function (x) { x.disabled = true; });
          step.appendChild(U.el('p', { class: ok ? 'fb ok' : 'fb bad', role: 'status',
            text: ok ? 'Pętla naprawcza zadziałała: po powtórzeniu rozumiesz.'
              : 'Po powtórzeniu nadal nie. Było: ' + item.check.answer
                + '. Czasem trzeba drugiej formuły — o prostsze słowa albo o zapisanie.' }));
          Progress.reflexRepair(item.trigger, ok);
          var next = U.el('button', { class: 'btn', type: 'button', text: 'Następne' });
          next.addEventListener('click', onNext);
          step.appendChild(U.el('div', { class: 'btn-row' }, [next]));
          next.focus();
        });
        opts.appendChild(b);
      });
      step.appendChild(U.el('p', { text: 'Co powiedział rozmówca?' }));
      step.appendChild(opts);
      step.scrollIntoView({ block: 'nearest' });
    }

    playDegraded(line, def, replay);
  };

  global.Rescue = Rescue;
})(window);
