/* Thai All-in-One — dwa ćwiczenia na dziury w rozumieniu.

   LUKI NA SŁUCH
   Uczący się słyszy całe zdanie i uzupełnia jeden brakujący wyraz. Luka nie
   jest losowana ze wszystkich wyrazów: zdanie ma dziurę tam, gdzie uczący się
   ma szansę ją zapełnić. Wyraz, którego nigdy nie widział, daje zgadywanie;
   wyraz funkcyjny wstawia się odruchowo i też niczego nie mierzy. Zostaje to,
   co poznał — i wtedy pytanie brzmi: czy usłyszałeś, nie: czy wiesz.

   TOLERANCJA NIEZNANEGO
   Zdanie z jednym słowem, którego uczący się nie zna. Zadanie: zgadnąć
   znaczenie z kontekstu. To nie jest ćwiczenie pocieszające — przy pokryciu
   słownictwa poniżej 95 procent (a tu jest około 80) domyślanie się jest
   warunkiem rozumienia czegokolwiek dłuższego. Jest przy tym trenowalne,
   dlatego po każdej odpowiedzi pokazujemy, co konkretnie w zdaniu prowadziło
   do rozwiązania — żeby następnym razem uczący się szukał tam sam.

   Trudność w obu ćwiczeniach reguluje tempo i hałas tła z sesji L. */
(function (global) {
  'use strict';

  var Comp = { noiseLevel: 0, current: null };

  Comp.ensureData = function () { return DB.ensureComprehension(); };
  Comp.ready = function () {
    return !!(DB.comprehension && DB.comprehension.gapItems);
  };

  function settings() { return U.store.get('settings', {}); }
  function hideTones() { return !!settings().hideTones; }

  function lineOf(item) {
    var dlg = DB.get(item.d);
    if (!dlg || !dlg.lines) return null;
    for (var i = 0; i < dlg.lines.length; i++) {
      if (dlg.lines[i].index === item.l) return dlg.lines[i];
    }
    return null;
  }

  function wordsOf(phonetic) {
    return (phonetic || '').trim().split(/\s+/).filter(Boolean);
  }

  /* Warunki akustyczne ćwiczenia. Poziom hałasu należy do ćwiczenia, a nie do
     Ustawień — tak samo jak w „Rozumieniu w hałasie” z sesji L. */
  function noiseOpts() {
    if (!Comp.noiseLevel || !global.DSP || !DSP.supported()) return null;
    return { kind: settings().noiseKind || 'restaurant', level: Comp.noiseLevel };
  }

  function noiseRow(onChange) {
    var wrap = U.el('div', { class: 'mode-row', role: 'group',
      'aria-label': 'Hałas tła' });
    [0, 1, 2, 3].forEach(function (lvl) {
      var chip = U.el('button', { class: 'chip', type: 'button',
        'aria-pressed': Comp.noiseLevel === lvl ? 'true' : 'false',
        text: lvl === 0 ? 'cisza' : 'hałas ' + lvl });
      chip.addEventListener('click', function () {
        Comp.noiseLevel = lvl;
        if (onChange) onChange();
      });
      wrap.appendChild(chip);
    });
    return wrap;
  }

  /* ==================================================== LUKI NA SŁUCH */

  /* Ile razy uczący się zetknął się z hasłem. To jedyna miara „czy zna”,
     jaką aplikacja naprawdę ma — i wystarcza, żeby nie robić luki ze słowa
     widzianego pierwszy raz w życiu. */
  function familiarity(recordId) {
    return (Progress.data.seen && Progress.data.seen[recordId]) || 0;
  }

  /* Wybór luki. Kolejność preferencji:
       1. hasło poznane, ale jeszcze nieutrwalone — tu ćwiczenie ma sens,
       2. hasło poznane i częste — łatwiejsze, ale nadal o słuch,
       3. hasło nieznane, za to bardzo częste — wchodzi jako nowe.
     Wewnątrz grupy losowo, żeby to samo zdanie nie dawało zawsze tej samej luki. */
  function chooseSlot(item) {
    var scored = (item.slots || []).map(function (slot) {
      var seen = familiarity(slot.r);
      var rank;
      if (seen > 0 && seen < 4) rank = 3;
      else if (seen >= 4) rank = 2;
      else if ((slot.f || 3) >= 4) rank = 1;
      else rank = 0;
      return { slot: slot, rank: rank };
    });
    if (!scored.length) return null;
    var best = Math.max.apply(null, scored.map(function (s) { return s.rank; }));
    var pool = scored.filter(function (s) { return s.rank === best; });
    return pool[Math.floor(Math.random() * pool.length)].slot;
  }

  function gapPool() {
    var items = (DB.comprehension && DB.comprehension.gapItems) || [];
    return items.filter(function (it) { return DB.get(it.d); });
  }

  /* Dystraktory: wyrazy o tej samej liczbie sylab, najchętniej z tego samego
     poziomu. Równa długość jest tu istotna — inaczej odpowiedź wybiera się po
     kształcie słowa, nie po tym, co się usłyszało. */
  function wordFoils(correct, avoid, level) {
    var target = U.syllables(correct).length;
    var seen = {};
    avoid.forEach(function (w) { seen[U.fold(w)] = true; });
    seen[U.fold(correct)] = true;

    var pool = [];
    var source = DB.index.length ? DB.index : DB.records;
    for (var i = 0; i < source.length; i++) {
      var rec = source[i];
      var ph = rec.thaiPhonetic || '';
      if (ph.indexOf(' ') !== -1) continue;
      if (U.syllables(ph).length !== target) continue;
      var key = U.fold(ph);
      if (!key || seen[key]) continue;
      seen[key] = true;
      pool.push({ text: ph, level: rec.level });
      if (pool.length > 400) break;
    }
    var same = pool.filter(function (p) { return p.level === level; });
    var from = same.length >= 3 ? same : pool;
    return U.sample(from, 3).map(function (p) { return p.text; });
  }

  Comp.renderGap = function (box, onNext) {
    if (!Comp.ready()) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję materiał…' }));
      return;
    }
    var pool = gapPool();
    if (!pool.length) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Ten materiał jeszcze się wczytuje. Spróbuj za chwilę.' }));
      return;
    }
    var item = pool[Math.floor(Math.random() * pool.length)];
    var line = lineOf(item);
    var slot = chooseSlot(item);
    if (!line || !slot) { onNext(); return; }

    var view = G.view(line);
    var ws = wordsOf(view.thaiPhonetic);
    /* Wariant żeński bywa o wyraz dłuższy niż wariant podstawowy, na którym
       liczono pozycje. Gdy się nie zgadza, bierzemy zapis podstawowy —
       inaczej luka wypadłaby na innym słowie niż zaplanowane. */
    if (ws.length !== item.words) {
      ws = wordsOf(line.thaiPhonetic);
      view = line;
    }
    if (slot.w >= ws.length) { onNext(); return; }
    var correct = ws[slot.w];
    Comp.current = { item: item, slot: slot, word: correct };

    box.appendChild(U.el('p', { class: 'muted', text:
      'Posłuchaj całego zdania i uzupełnij brakujący wyraz. Reszty zdania '
      + 'nie musisz rozumieć w całości.' }));

    var play = U.el('button', { class: 'btn gold play-btn', type: 'button',
      'aria-pressed': 'false' });
    play.appendChild(U.icon('play'));
    play.appendChild(U.el('span', { text: 'Odtwórz zdanie' }));
    play.addEventListener('click', function () {
      Player.play(view, { btn: play, tempo: CompTempo.current,
        role: line.role, gender: G.speakerOf(line), noise: noiseOpts() });
    });
    var repeat = U.el('button', { class: 'btn ghost', type: 'button',
      text: 'Jeszcze raz, wolniej' });
    repeat.addEventListener('click', function () {
      Player.play(view, { btn: repeat, tempo: 'slow',
        role: line.role, gender: G.speakerOf(line), noAmbience: true });
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play, repeat]));

    /* Zdanie z dziurą. Pozostałe wyrazy są widoczne — luka ma być jedna. */
    var sentence = U.el('p', { class: 'gap-sentence' });
    ws.forEach(function (w, i) {
      if (i) sentence.appendChild(document.createTextNode(' '));
      if (i === slot.w) {
        sentence.appendChild(U.el('span', { class: 'gap-blank', text: '______',
          'aria-label': 'brakujący wyraz' }));
      } else {
        sentence.appendChild(U.el('span', { text: hideTones() ? U.stripTones(w) : w }));
      }
    });
    box.appendChild(sentence);

    var options = U.shuffle([correct].concat(wordFoils(correct, ws, slot.lvl)));
    var list = U.el('div', { class: 'options' });
    var answered = false;
    options.forEach(function (opt) {
      var btn = U.el('button', { class: 'btn option', type: 'button',
        text: hideTones() ? U.stripTones(opt) : opt });
      btn.addEventListener('click', function () {
        if (answered) return;
        answered = true;
        var ok = U.fold(opt) === U.fold(correct);
        btn.classList.add(ok ? 'correct' : 'wrong');
        U.$$('.option', list).forEach(function (b) {
          b.disabled = true;
          if (U.fold(b.textContent) === U.fold(hideTones() ? U.stripTones(correct) : correct)) {
            b.classList.add('correct');
          }
        });

        U.$('.gap-blank', sentence).textContent = hideTones()
          ? U.stripTones(correct) : correct;
        U.$('.gap-blank', sentence).classList.add(ok ? 'filled-ok' : 'filled-bad');

        var fb = U.el('p', { class: ok ? 'fb ok' : 'fb bad', role: 'status' });
        fb.appendChild(U.el('strong', { text: ok ? 'Dobrze. ' : 'Brakowało: ' }));
        fb.appendChild(document.createTextNode(ok ? '' : correct + '.'));
        box.appendChild(fb);
        box.appendChild(U.el('p', { text: view.polish }));
        if (slot.p) {
          box.appendChild(U.el('p', { class: 'muted', text:
            'Brakujący wyraz znaczy: ' + slot.p + '.' }));
        }
        box.appendChild(U.el('p', { class: 'muted', text:
          'Tempo: ' + Progress.tempoLabel(CompTempo.current)
          + (Comp.noiseLevel ? ', hałas ' + Comp.noiseLevel + ' z 3' : ', bez hałasu')
          + '. Wynik liczy się do tego tempa.' }));

        Progress.answer(slot.r, ok, { mode: 'gap' });
        Progress.tempoAnswer('gap', CompTempo.current, ok);
        SRS.add(slot.r, 'r');
        SRS.grade(slot.r, ok ? 4 : 1, { side: 'r' });

        var next = U.el('button', { class: 'btn', type: 'button', text: 'Następne' });
        next.addEventListener('click', onNext);
        box.appendChild(U.el('div', { class: 'btn-row' }, [next]));
        next.focus();
      });
      list.appendChild(btn);
    });
    box.appendChild(list);

    var tuning = U.el('div', { class: 'tuning' });
    tuning.appendChild(U.el('p', { class: 'muted', text: 'Trudność:' }));
    tuning.appendChild(CompTempo.row('gap', function () { onNext(); }));
    tuning.appendChild(noiseRow(function () { onNext(); }));
    box.appendChild(tuning);

    Player.play(view, { btn: play, tempo: CompTempo.current,
      role: line.role, gender: G.speakerOf(line), noise: noiseOpts() });
  };

  /* ============================================ TOLERANCJA NIEZNANEGO */

  function inferencePool() {
    var items = (DB.comprehension && DB.comprehension.inferenceItems) || [];
    return items.filter(function (it) {
      if (it.src === 'dialogue') return !!DB.get(it.d);
      var rec = DB.get(it.r);
      return !!(rec && rec.examples && rec.examples[it.ex]);
    });
  }

  /* Zdanie i jego źródło. Dwa źródła, bo dwa rodzaje kontekstu: kwestia
     dialogu ma sytuację i rozmówców, przykład użycia ma pewne znaczenie
     hasła. Ekran obsługuje oba tak samo. */
  function inferenceSentence(item) {
    if (item.src === 'dialogue') {
      var line = lineOf(item);
      if (!line) return null;
      var dlg = DB.get(item.d);
      return { text: line, polish: line.polish, role: line.role,
               gender: G.speakerOf(line),
               context: dlg ? dlg.situation : '' };
    }
    var rec = DB.get(item.r);
    if (!rec || !rec.examples || !rec.examples[item.ex]) return null;
    var ex = rec.examples[item.ex];
    return { text: ex, polish: ex.polish, role: null, gender: null,
             context: rec.category };
  }

  Comp.renderUnknown = function (box, onNext) {
    if (!Comp.ready()) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję materiał…' }));
      return;
    }
    var pool = inferencePool();
    if (!pool.length) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Ten materiał jeszcze się wczytuje. Spróbuj za chwilę.' }));
      return;
    }
    /* Najpierw zdania, których słowa docelowego uczący się jeszcze nie widział
       — bo tylko wtedy jest ono naprawdę nieznane. Gdy takich nie ma,
       bierzemy dowolne. */
    var fresh = pool.filter(function (it) { return !familiarity(it.r); });
    var from = fresh.length ? fresh : pool;
    var item = from[Math.floor(Math.random() * from.length)];
    var src = inferenceSentence(item);
    if (!src) { onNext(); return; }

    var view = G.view(src.text);
    var ws = wordsOf(view.thaiPhonetic);
    if (item.w >= ws.length) {
      ws = wordsOf(src.text.thaiPhonetic);
      view = src.text;
    }
    if (item.w >= ws.length) { onNext(); return; }

    box.appendChild(U.el('p', { class: 'muted', text:
      'W tym zdaniu jest jedno słowo, którego prawdopodobnie nie znasz. '
      + 'Nie szukaj go w pamięci — wywnioskuj znaczenie z reszty zdania.' }));

    var play = U.el('button', { class: 'btn gold play-btn', type: 'button',
      'aria-pressed': 'false' });
    play.appendChild(U.icon('play'));
    play.appendChild(U.el('span', { text: 'Odtwórz zdanie' }));
    play.addEventListener('click', function () {
      Player.play(view, { btn: play, tempo: CompTempo.current,
        role: src.role, gender: src.gender, noise: noiseOpts() });
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play]));

    var sentence = U.el('p', { class: 'gap-sentence' });
    ws.forEach(function (w, i) {
      if (i) sentence.appendChild(document.createTextNode(' '));
      var span = U.el('span', {
        class: i === item.w ? 'unknown-word' : '',
        'data-w': String(i),
        text: hideTones() ? U.stripTones(w) : w
      });
      if (i === item.w) span.setAttribute('aria-label', 'nieznane słowo: ' + w);
      sentence.appendChild(span);
    });
    box.appendChild(sentence);
    box.appendChild(U.el('p', { class: 'muted', text:
      'Kontekst: ' + (src.context || 'rozmowa codzienna') }));

    var list = U.el('div', { class: 'options' });
    var answered = false;
    item.opts.forEach(function (text, i) {
      var btn = U.el('button', { class: 'btn option', type: 'button', text: text });
      btn.addEventListener('click', function () {
        if (answered) return;
        answered = true;
        var ok = i === item.a;
        btn.classList.add(ok ? 'correct' : 'wrong');
        U.$$('.option', list).forEach(function (b, j) {
          b.disabled = true;
          if (j === item.a) b.classList.add('correct');
        });

        var fb = U.el('p', { class: ok ? 'fb ok' : 'fb bad', role: 'status' });
        fb.appendChild(U.el('strong', { text: ok ? 'Trafnie. ' : 'Nie tym razem. ' }));
        fb.appendChild(document.createTextNode(
          '„' + ws[item.w] + '” znaczy: ' + item.p + '.'));
        box.appendChild(fb);

        /* Sedno ćwiczenia: pokazujemy, co prowadziło do rozwiązania.
           Bez tego uczący się dowiaduje się tylko, czy zgadł. */
        var cues = U.el('div', { class: 'cues' });
        cues.appendChild(U.el('h3', { text: 'Co prowadziło do tej odpowiedzi' }));
        var ol = U.el('ol');
        item.cues.forEach(function (cue) {
          ol.appendChild(U.el('li', { text: cue.text }));
          if (cue.w >= 0) {
            var mark = U.$('[data-w="' + cue.w + '"]', sentence);
            if (mark) mark.classList.add('cue-word');
          }
        });
        cues.appendChild(ol);
        cues.appendChild(U.el('p', { class: 'muted', text:
          'Podświetlone wyrazy to te wskazówki w zdaniu. Przy następnym '
          + 'nieznanym słowie szukaj dokładnie tam.' }));
        box.appendChild(cues);
        box.appendChild(U.el('p', { text: src.polish }));

        Progress.answer(item.r, ok, { mode: 'unknown' });
        Progress.tempoAnswer('unknown', CompTempo.current, ok);

        var next = U.el('button', { class: 'btn', type: 'button', text: 'Następne' });
        next.addEventListener('click', onNext);
        box.appendChild(U.el('div', { class: 'btn-row' }, [next]));
        next.focus();
      });
      list.appendChild(btn);
    });
    box.appendChild(list);

    var tuning = U.el('div', { class: 'tuning' });
    tuning.appendChild(CompTempo.row('unknown', function () { onNext(); }));
    box.appendChild(tuning);

    Player.play(view, { btn: play, tempo: CompTempo.current,
      role: src.role, gender: src.gender, noise: noiseOpts() });
  };

  global.Comp = Comp;
})(window);
