/* Thai All-in-One — trzy tryby gramatyczne.

   WYKRYWANIE STRUKTURY ZE SŁUCHU
   Uczący się słyszy zdanie i mówi, CZYM ono jest: pytaniem czy stwierdzeniem,
   przeszłością czy przyszłością, prośbą czy poleceniem. Nie co znaczy — czym
   jest. To umiejętność osobna od słownikowej i przy niepełnym słownictwie
   ważniejsza: kto usłyszy `mǎi` na końcu, wie, że ma odpowiedzieć, choćby nie
   zrozumiał ani jednego wyrazu przed nim. Kto nie usłyszy — będzie milczał.

   Zapis fonetyczny jest ZASŁONIĘTY do czasu odpowiedzi. Gdyby był widoczny,
   uczący się odczytywałby cząstkę z tekstu zamiast wyłapywać ją ze słuchu,
   a ćwiczenie mierzyłoby czytanie.

   TRANSFORMACJE
   Dane zdanie plus polecenie. Ocena idzie PO STRUKTURZE, nie po zgodności
   znak w znak: liczy się, czy wymagany marker stanął we właściwym miejscu
   i czy trzon zdania ocalał. Odpowiedź inaczej sformułowana, ale zbudowana
   poprawnie, jest zaliczana — inaczej uczący się szybko przestałby ufać
   ocenie i zaczął zgadywać brzmienie wzorca zamiast budować zdanie.

   PARTYKUŁY KOŃCOWE
   Niosą znaczenie, którego polszczyzna nie koduje w ogóle: to samo zdanie
   z inną partykułą jest inną wypowiedzią. Ćwiczenie jest sytuacyjne, bo
   partykuły nie mają odpowiedników słownikowych — mają warunki użycia. */
(function (global) {
  'use strict';

  var Gram = { current: null, axis: 'intent', transform: 'question' };

  Gram.ensureData = function () { return DB.ensureGrammarModes(); };
  Gram.ready = function () {
    return !!(DB.grammarListening && DB.grammarListening.length);
  };

  function settings() { return U.store.get('settings', {}); }
  function hideTones() { return !!settings().hideTones; }

  /* Materiał ograniczony do tego, co kurs zdążył wprowadzić.
     Zadanie zbudowane ze zdania, którego uczący się nie ma prawa rozumieć,
     nie mierzy wykrywania struktury — mierzy szczęście. */
  function reach() {
    var n = Progress.lessonsDone ? Progress.lessonsDone() : 0;
    return Math.max(12, n);
  }

  function withinReach(list) {
    var limit = reach();
    var ok = list.filter(function (x) { return x.availableFrom <= limit; });
    /* Zapas: gdy uczący się jest na samym początku, a nic się nie kwalifikuje,
       lepiej dać materiał odrobinę za trudny niż pusty ekran. */
    return ok.length >= 8 ? ok : list.slice(0, 40);
  }

  function pick(list) {
    return list[Math.floor(Math.random() * list.length)];
  }

  function axisMeta(axis) {
    var axes = (DB.grammarAxes || {});
    return axes[axis] || [];
  }

  /* ============================================ WYKRYWANIE STRUKTURY */

  var AXES = [
    { id: 'intent', label: 'Pytanie czy stwierdzenie?' },
    { id: 'time', label: 'Przeszłość czy przyszłość?' }
  ];

  Gram.axes = function () { return AXES.slice(); };

  Gram.renderListening = function (box, onNext) {
    if (!Gram.ready()) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję materiał…' }));
      return;
    }
    var pool = withinReach(DB.grammarListening);
    if (!pool.length) { onNext(); return; }
    var item = pick(pool);
    var axis = Gram.axis;
    var meta = axisMeta(axis);
    var correct = item[axis];
    Gram.current = { item: item, axis: axis };

    box.appendChild(U.el('p', { class: 'muted', text:
      'Posłuchaj i powiedz, jaka to konstrukcja. Nie musisz rozumieć '
      + 'wszystkich słów — wystarczy usłyszeć, gdzie stoi cząstka.' }));

    var play = U.el('button', { class: 'btn gold play-btn', type: 'button',
      'aria-pressed': 'false' });
    play.appendChild(U.icon('play'));
    play.appendChild(U.el('span', { text: 'Odtwórz zdanie' }));
    play.addEventListener('click', function () {
      Player.play(item, { btn: play, tempo: CompTempo.current });
    });
    var again = U.el('button', { class: 'btn ghost', type: 'button',
      text: 'Jeszcze raz, wolniej' });
    again.addEventListener('click', function () {
      Player.play(item, { btn: again, tempo: 'slow' });
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play, again]));

    /* Zasłonięty zapis — odsłania się dopiero po odpowiedzi. */
    var veil = U.el('p', { class: 'muted veil', text:
      'Zapis pojawi się po odpowiedzi.' });
    box.appendChild(veil);

    var options = meta.filter(function (o) {
      return axis !== 'time' || o.id !== 'nieokreslony' ||
        correct === 'nieokreslony';
    });
    var list = U.el('div', { class: 'options' });
    var answered = false;
    options.forEach(function (opt, i) {
      var btn = U.el('button', { class: 'btn option', type: 'button',
        'aria-label': 'Odpowiedź ' + (i + 1) + ': ' + opt.label,
        text: opt.label });
      btn.addEventListener('click', function () {
        if (answered) return;
        answered = true;
        var ok = opt.id === correct;
        U.$$('.option', list).forEach(function (b) { b.disabled = true; });
        btn.classList.add(ok ? 'correct' : 'wrong');
        U.$$('.option', list).forEach(function (b) {
          var m = options[Array.prototype.indexOf.call(list.children, b)];
          if (m && m.id === correct) b.classList.add('correct');
        });

        var right = options.filter(function (o) { return o.id === correct; })[0];
        veil.classList.remove('veil');
        veil.textContent = hideTones()
          ? U.stripTones(item.thaiPhonetic) : item.thaiPhonetic;

        var fb = U.el('p', { class: ok ? 'fb ok' : 'fb bad', role: 'status',
          text: ok ? 'Dobrze.' : 'To była konstrukcja: '
            + (right ? right.label : correct) + '.' });
        box.appendChild(fb);
        box.appendChild(U.el('p', { text: item.polish }));
        if (right && right.why) {
          box.appendChild(U.el('p', { class: 'muted', text: right.why }));
        }
        if (item.polite) {
          box.appendChild(U.el('p', { class: 'muted', text:
            'Wypowiedź jest w formie grzecznej — cząstka na samym końcu.' }));
        }

        Progress.answer(item.sourceId, ok, { mode: 'structure' });
        Progress.tempoAnswer('structure', CompTempo.current, ok);
        Progress.grammarAnswer(item.sourceId, ok, 'receptive');

        var next = U.el('button', { class: 'btn', type: 'button',
          text: 'Następne' });
        next.addEventListener('click', onNext);
        box.appendChild(U.el('div', { class: 'btn-row' }, [next]));
        next.focus();
      });
      list.appendChild(btn);
    });
    box.appendChild(list);

    var tuning = U.el('div', { class: 'tuning' });
    tuning.appendChild(U.el('p', { class: 'muted', text: 'O co pytamy:' }));
    var axisRow = U.el('div', { class: 'mode-row', role: 'group',
      'aria-label': 'Oś pytania' });
    AXES.forEach(function (a) {
      var chip = U.el('button', { class: 'chip', type: 'button', text: a.label,
        'aria-pressed': Gram.axis === a.id ? 'true' : 'false' });
      chip.addEventListener('click', function () {
        Gram.axis = a.id;
        onNext();
      });
      axisRow.appendChild(chip);
    });
    tuning.appendChild(axisRow);
    tuning.appendChild(U.el('p', { class: 'muted', text: 'Tempo:' }));
    tuning.appendChild(CompTempo.row('structure', function () { onNext(); }));
    box.appendChild(tuning);

    Player.play(item, { btn: play, tempo: CompTempo.current });
  };

  /* =================================================== TRANSFORMACJE */

  /* Ocena po strukturze.

     Sprawdzamy trzy rzeczy i tylko te trzy:
       1. czy wymagany marker w ogóle padł,
       2. czy stoi we właściwym miejscu — na końcu albo przed czasownikiem,
       3. czy trzon zdania ocalał (nie wolno wyrzucić połowy wyrazów).

     Czego świadomie NIE sprawdzamy: cząstki grzecznościowej, znaków tonów
     i dokładnej kolejności wyrazów trzonu. Uczący się ma zbudować
     konstrukcję, a nie odtworzyć wzorzec z pamięci — to drugie jest osobnym
     ćwiczeniem i mierzy co innego. */
  Gram.grade = function (answer, item) {
    var check = item.check || {};
    var words = U.fold(answer || '').split(/\s+/).filter(Boolean);
    if (!words.length) {
      return { ok: false, reason: 'Nie ma odpowiedzi.' };
    }
    var accepted = [check.marker].concat(check.alternatives || []);
    var foldAcc = accepted.map(U.fold);
    var at = -1;
    for (var i = 0; i < words.length; i++) {
      if (foldAcc.indexOf(words[i]) !== -1) { at = i; break; }
    }
    if (at === -1) {
      return { ok: false, reason: 'Brakuje cząstki `' + check.marker
        + '`. Bez niej konstrukcja się nie zmienia.' };
    }

    /* Trzon: ile wyrazów oryginału przetrwało. Próg 70 procent, bo część
       wyrazów uczący się może pominąć albo zapisać inaczej, ale zdanie
       zbudowane od zera nie jest przekształceniem tego zdania. */
    var keep = (check.keep || []).map(U.fold);
    var kept = keep.filter(function (k) { return words.indexOf(k) !== -1; });
    if (keep.length && kept.length / keep.length < 0.7) {
      return { ok: false, reason: 'To już inne zdanie. Przekształcenie ma '
        + 'zmienić konstrukcję, a zostawić treść.' };
    }

    if (check.position === 'koniec') {
      /* „Na końcu” znaczy: za trzonem, ale cząstka grzecznościowa i tak
         zawsze zamyka wypowiedź, więc wolno jej stać za markerem. */
      var tail = words.slice(at + 1).filter(function (x) {
        return ['khrap', 'kha', 'khá', 'khâ'].indexOf(x) === -1
          && U.fold(x) !== U.fold('khráp');
      });
      if (tail.length) {
        return { ok: false, reason: 'Cząstka `' + check.marker + '` musi stać '
          + 'na końcu — za nią może być już tylko forma grzecznościowa.' };
      }
      return { ok: true };
    }

    var before = U.fold(check.before || '');
    if (before && words[at + 1] !== before) {
      return { ok: false, reason: 'Cząstka `' + check.marker + '` musi stać '
        + 'bezpośrednio przed czasownikiem `' + check.before + '`.' };
    }
    return { ok: true };
  };

  Gram.renderTransform = function (box, onNext) {
    if (!DB.grammarTransform || !DB.grammarTransform.length) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję materiał…' }));
      return;
    }
    var kinds = DB.grammarTransformKinds || [];
    var pool = withinReach(DB.grammarTransform.filter(function (x) {
      return x.transform === Gram.transform;
    }));
    if (!pool.length) { onNext(); return; }
    var item = pick(pool);
    var spec = kinds.filter(function (k) { return k.id === item.transform; })[0]
      || { title: 'Przekształć zdanie', instruction: '', rule: '' };
    Gram.current = { item: item };

    box.appendChild(U.el('h3', { text: spec.title }));
    box.appendChild(U.el('p', { class: 'muted', text: spec.instruction }));

    var src = U.el('p', { class: 'phonetic', text: hideTones()
      ? U.stripTones(item.thaiPhonetic) : item.thaiPhonetic });
    box.appendChild(src);
    box.appendChild(U.el('p', { text: item.polish }));

    var play = U.el('button', { class: 'btn ghost play-btn', type: 'button',
      'aria-pressed': 'false' });
    play.appendChild(U.icon('play'));
    play.appendChild(U.el('span', { text: 'Posłuchaj zdania wyjściowego' }));
    play.addEventListener('click', function () {
      Player.play(item, { btn: play });
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play]));

    var label = U.el('label', { class: 'field-label', for: 'gram-answer',
      text: 'Twoja wersja' });
    var input = U.el('input', { id: 'gram-answer', type: 'text',
      autocomplete: 'off', autocapitalize: 'off', spellcheck: 'false',
      placeholder: 'wpisz przekształcone zdanie' });
    box.appendChild(U.el('div', { class: 'field' }, [label, input]));

    var answered = false;
    var send = U.el('button', { class: 'btn gold', type: 'button',
      text: 'Sprawdź' });
    var hint = U.el('button', { class: 'btn ghost', type: 'button',
      text: 'Podpowiedz regułę' });
    hint.addEventListener('click', function () {
      hint.disabled = true;
      box.insertBefore(U.el('p', { class: 'muted', role: 'status',
        text: spec.rule }), send.parentNode);
    });

    function submit() {
      if (answered) return;
      answered = true;
      var verdict = Gram.grade(input.value, item);
      input.disabled = true;
      send.disabled = true;
      hint.disabled = true;

      var fb = U.el('p', { class: verdict.ok ? 'fb ok' : 'fb bad',
        role: 'status' });
      fb.appendChild(U.el('strong', { text: verdict.ok
        ? 'Struktura poprawna. ' : 'Jeszcze nie. ' }));
      if (!verdict.ok) fb.appendChild(document.createTextNode(verdict.reason));
      box.appendChild(fb);

      box.appendChild(U.el('p', { class: 'muted', text:
        'Wzorzec: ' + (hideTones() ? U.stripTones(item.model) : item.model) }));
      box.appendChild(U.el('p', { class: 'muted', text:
        'Oceniamy konstrukcję, nie dosłowną zgodność z wzorcem — inne '
        + 'poprawnie zbudowane zdanie też jest zaliczone.' }));

      Progress.answer(item.sourceId, verdict.ok, { mode: 'transform' });
      Progress.grammarAnswer(item.sourceId, verdict.ok, 'productive');

      var next = U.el('button', { class: 'btn', type: 'button',
        text: 'Następne' });
      next.addEventListener('click', onNext);
      box.appendChild(U.el('div', { class: 'btn-row' }, [next]));
      next.focus();
    }

    send.addEventListener('click', submit);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); submit(); }
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [send, hint]));

    var tuning = U.el('div', { class: 'tuning' });
    tuning.appendChild(U.el('p', { class: 'muted', text: 'Rodzaj zmiany:' }));
    var row = U.el('div', { class: 'mode-row', role: 'group',
      'aria-label': 'Rodzaj przekształcenia' });
    kinds.forEach(function (k) {
      var chip = U.el('button', { class: 'chip', type: 'button', text: k.title,
        'aria-pressed': Gram.transform === k.id ? 'true' : 'false' });
      chip.addEventListener('click', function () {
        Gram.transform = k.id;
        onNext();
      });
      row.appendChild(chip);
    });
    tuning.appendChild(row);
    box.appendChild(tuning);
    input.focus();
  };

  /* ================================================ PARTYKUŁY KOŃCOWE */

  Gram.renderParticles = function (box, onNext) {
    var data = DB.particles;
    if (!data || !data.length) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję materiał…' }));
      return;
    }
    var ex = pick(DB.particleExercises || []);
    if (!ex) { return; }
    var byId = {};
    data.forEach(function (p) { byId[p.id] = p; });

    box.appendChild(U.el('p', { class: 'muted', text:
      'Ta sama treść, różne partykuły. Wybierz tę, która pasuje do sytuacji '
      + '— partykuły nie mają odpowiedników w słowniku, mają warunki użycia.' }));
    box.appendChild(U.el('p', { class: 'situation', text: ex.situation }));

    var list = U.el('div', { class: 'options' });
    var answered = false;
    U.shuffle(ex.options.slice()).forEach(function (opt, i) {
      var btn = U.el('button', { class: 'btn option', type: 'button',
        'aria-label': 'Odpowiedź ' + (i + 1) + ': ' + opt.particle
          + ' — ' + opt.gloss });
      btn.appendChild(U.el('strong', { text: opt.particle }));
      btn.appendChild(U.el('span', { class: 'muted', text: ' — ' + opt.gloss }));
      btn.addEventListener('click', function () {
        if (answered) return;
        answered = true;
        var ok = opt.id === ex.answer;
        U.$$('.option', list).forEach(function (b) { b.disabled = true; });
        btn.classList.add(ok ? 'correct' : 'wrong');

        var right = byId[ex.answer];
        var fb = U.el('p', { class: ok ? 'fb ok' : 'fb bad', role: 'status',
          text: ok ? 'Dobrze.' : 'Pasuje: ' + right.particle + '.' });
        box.appendChild(fb);
        box.appendChild(U.el('p', { class: 'muted', text: ex.why }));

        var card = U.el('div', { class: 'card sub' });
        card.appendChild(U.el('h3', { text: right.particle + ' — '
          + right.gloss }));
        card.appendChild(U.el('p', { text: right.meaning }));
        card.appendChild(U.el('p', { class: 'muted', text:
          'Wydźwięk: ' + right.effect }));
        card.appendChild(U.el('p', { class: 'muted', text:
          'Gdy jej brak: ' + right.missing }));
        (right.examples || []).slice(0, 2).forEach(function (p) {
          var line = U.el('p', { class: 'phonetic' });
          line.appendChild(U.el('span', { text: hideTones()
            ? U.stripTones(p.thaiPhonetic) : p.thaiPhonetic }));
          card.appendChild(line);
          card.appendChild(U.el('p', { class: 'muted', text: p.polish }));
        });
        box.appendChild(card);

        Progress.answer('particle:' + ex.answer, ok, { mode: 'particle' });

        var next = U.el('button', { class: 'btn', type: 'button',
          text: 'Następne' });
        next.addEventListener('click', onNext);
        box.appendChild(U.el('div', { class: 'btn-row' }, [next]));
        next.focus();
      });
      list.appendChild(btn);
    });
    box.appendChild(list);
  };

  /* Przegląd partykuł — do czytania, nie do ćwiczenia. */
  Gram.renderParticleGuide = function (box) {
    var data = DB.particles || [];
    if (!data.length) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję materiał…' }));
      return;
    }
    data.forEach(function (p) {
      var card = U.el('div', { class: 'card sub' });
      var head = U.el('h3', { text: p.particle + ' — ' + p.gloss });
      card.appendChild(head);
      if (p.rude_without) {
        card.appendChild(U.el('p', { class: 'warn', text:
          'Brak tej cząstki wobec obcej osoby jest odbierany jako '
          + 'opryskliwość.' }));
      }
      card.appendChild(U.el('p', { text: p.meaning }));
      card.appendChild(U.el('p', { class: 'muted', text:
        'Wydźwięk: ' + p.effect }));
      card.appendChild(U.el('p', { class: 'muted', text:
        'Gdy jej brak: ' + p.missing }));
      card.appendChild(U.el('p', { class: 'muted', text:
        'Rejestr: ' + p.register }));
      (p.examples || []).slice(0, 3).forEach(function (ex) {
        var row = U.el('div', { class: 'pattern' });
        var play = U.el('button', { class: 'btn ghost play-btn', type: 'button',
          'aria-label': 'Posłuchaj: ' + ex.polish, 'aria-pressed': 'false' });
        play.appendChild(U.icon('play'));
        play.addEventListener('click', function () {
          Player.play(ex, { btn: play });
        });
        row.appendChild(U.el('span', { class: 'phonetic', text: hideTones()
          ? U.stripTones(ex.thaiPhonetic) : ex.thaiPhonetic }));
        row.appendChild(play);
        card.appendChild(row);
        card.appendChild(U.el('p', { class: 'muted', text: ex.polish }));
      });
      box.appendChild(card);
    });
  };

  global.Gram = Gram;
}(this));
