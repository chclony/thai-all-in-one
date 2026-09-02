/* Thai All-in-One — ćwiczenia słuchania i mówienia. */
(function (global) {
  'use strict';

  var Quiz = { mode: 'choice', current: null, answered: false };

  function settings() { return U.store.get('settings', {}); }
  function hideTones() { return !!settings().hideTones; }

  /* Ćwiczenia ze słuchu potrzebują pełnych rekordów — dociągamy poziom nauki,
     a gdyby był pusty, materiał startowy. Nigdy całej bazy. */
  Quiz.ensureData = function () {
    var lvl = settings().practiceLevel || (global.Progress && Progress.entryLevel()) || '';
    var base = DB.ensureLevel(lvl).then(function () {
      if (!DB.records.length) return DB.ensureStarter();
    });
    if (DIALOGUE_MODES[Quiz.mode]) {
      return base.then(function () { return DB.ensureComprehension(); });
    }
    return base;
  };

  function pool() {
    var lvl = settings().practiceLevel;
    var list = DB.records.filter(function (r) {
      if (lvl && r.level !== lvl) return false;
      return r.frequency >= 3;
    });
    return list.length > 12 ? list : DB.records;
  }

  /* Każdy rekord przed pokazaniem i odtworzeniem przechodzi przez wariant
     zgodny z ustawieniem płci — inaczej ćwiczenia uczyłyby formy, której
     uczący się nie użyje. */
  function gv(item) { return global.G ? G.view(item) : item; }

  function feedback(box, ok, text) {
    var node = U.el('p', { class: ok ? 'fb ok' : 'fb bad', role: 'status' }, [
      U.el('strong', { text: ok ? 'Dobrze! ' : 'Jeszcze raz. ' }),
      document.createTextNode(text || '')
    ]);
    box.appendChild(node);
  }

  function nextButton(box, onNext) {
    var btn = U.el('button', { class: 'btn', type: 'button', text: 'Następne' });
    btn.addEventListener('click', onNext);
    box.appendChild(U.el('div', { class: 'btn-row' }, [btn]));
    btn.focus();
  }

  /* ------------------------------------------------- 1. wybierz tłumaczenie */
  function renderChoice(box, onNext, forced) {
    var rec = gv(forced || U.sample(pool(), 1)[0]);
    Quiz.current = rec;
    var options = U.shuffle(Search.similar(rec, 3).concat([rec]));

    box.appendChild(U.el('p', { class: 'muted', text: 'Posłuchaj i wybierz polskie znaczenie.' }));
    var play = Player.button(rec, 'Odtwórz');
    box.appendChild(U.el('div', { class: 'btn-row' }, [play]));

    var reveal = U.el('div', { class: 'reveal', hidden: 'hidden' });
    reveal.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: hideTones() }));
    reveal.appendChild(U.el('p', { class: 'muted', text: 'Czytaj po polsku: ' + rec.pronunciationPolish }));
    box.appendChild(reveal);
    box.appendChild(CompTempo.row('choice', function () { Quiz.renderListen(box); }));

    var list = U.el('div');
    options.forEach(function (opt) {
      var btn = U.el('button', { class: 'opt', type: 'button', text: opt.polish });
      btn.addEventListener('click', function () {
        if (Quiz.answered) return;
        Quiz.answered = true;
        var ok = opt.id === rec.id;
        btn.classList.add(ok ? 'correct' : 'wrong');
        if (!ok) {
          U.$$('.opt', list).forEach(function (b) {
            if (b.textContent === rec.polish) b.classList.add('correct');
          });
        }
        reveal.hidden = false;
        Progress.answer(rec.id, ok, { mode: 'choice' });
        Progress.tempoAnswer('choice', CompTempo.current, ok);
        SRS.add(rec.id, 'r');
        SRS.grade(rec.id, ok ? 4 : 1, { side: 'r' });
        feedback(box, ok, ok ? '' : 'Poprawnie: ' + rec.polish + ' — ' + rec.thaiPhonetic);
        if (Quiz.onAnswer) { Quiz.onAnswer(rec.id, ok); return; }
        nextButton(box, onNext);
      });
      list.appendChild(btn);
    });
    box.appendChild(list);
    Player.play(rec, { btn: play, tempo: CompTempo.current });
  }

  /* --------------------------------------------------- 2. dyktando fonetyczne */
  function renderDictation(box, onNext) {
    var rec = gv(U.sample(pool().filter(function (r) { return U.syllables(r.thaiPhonetic).length <= 4; }), 1)[0]);
    Quiz.current = rec;

    box.appendChild(U.el('p', { class: 'muted', text: 'Posłuchaj i zapisz to, co słyszysz, alfabetem łacińskim. Tony nie są wymagane.' }));
    var play = Player.button(rec, 'Odtwórz');
    var slow = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wolniej (0,5x)' });
    slow.addEventListener('click', function () { Player.play(rec, { btn: slow, rate: 0.5 }); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play, slow]));

    var input = U.el('input', { type: 'text', id: 'dict-input', autocomplete: 'off', autocapitalize: 'off', spellcheck: 'false', placeholder: 'np. sawat-dii' });
    box.appendChild(U.el('label', { class: 'field' }, [U.el('span', { text: 'Twój zapis' }), input]));

    var check = U.el('button', { class: 'btn', type: 'button', text: 'Sprawdź' });
    box.appendChild(U.el('div', { class: 'btn-row' }, [check]));

    function normalize(t) { return U.fold(t).replace(/[^a-z]/g, ''); }

    check.addEventListener('click', function () {
      if (Quiz.answered) return;
      Quiz.answered = true;
      var ok = normalize(input.value) === normalize(rec.thaiPhonetic) ||
               normalize(input.value) === normalize(rec.pronunciationPolish);
      box.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: hideTones() }));
      box.appendChild(U.el('p', { class: 'muted', text: rec.polish + ' — czytaj: ' + rec.pronunciationPolish }));
      Progress.answer(rec.id, ok, { mode: 'dictation' });
      Progress.tempoAnswer('dictation', CompTempo.current, ok);
      SRS.add(rec.id, 'r');
      SRS.grade(rec.id, ok ? 5 : 2, { side: 'r' });
      feedback(box, ok, ok ? '' : 'Poprawny zapis: ' + rec.thaiPhonetic);
      nextButton(box, onNext);
    });
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') check.click(); });
    Player.play(rec, { btn: play });
  }

  /* -------------------------------------------------------- 3. ułóż zdanie */
  function renderAssemble(box, onNext) {
    var candidates = DB.records.filter(function (r) {
      return U.syllables(r.thaiPhonetic).length >= 3 && U.syllables(r.thaiPhonetic).length <= 7;
    });
    var rec = gv(U.sample(candidates.length ? candidates : DB.records, 1)[0]);
    Quiz.current = rec;
    var target = U.syllables(rec.thaiPhonetic);

    box.appendChild(U.el('p', { class: 'muted', text: 'Posłuchaj i ułóż sylaby w odpowiedniej kolejności.' }));
    box.appendChild(U.el('p', { class: 'bc-pl', text: rec.polish }));
    var play = Player.button(rec, 'Odtwórz');
    box.appendChild(U.el('div', { class: 'btn-row' }, [play]));

    var answerRow = U.el('div', { class: 'tokens answer', 'aria-label': 'Twoja odpowiedź' });
    var bank = U.el('div', { class: 'tokens' });
    var picked = [];

    function redraw() {
      U.clear(answerRow);
      picked.forEach(function (syl, i) {
        var t = U.el('button', { class: 'token picked', type: 'button', text: hideTones() ? U.stripTones(syl) : syl });
        t.addEventListener('click', function () {
          if (Quiz.answered) return;
          picked.splice(i, 1);
          redraw();
        });
        answerRow.appendChild(t);
      });
      if (!picked.length) answerRow.appendChild(U.el('span', { class: 'muted', text: 'Dotknij sylab poniżej.' }));
    }

    U.shuffle(target).forEach(function (syl) {
      var t = U.el('button', { class: 'token', type: 'button', text: hideTones() ? U.stripTones(syl) : syl });
      t.addEventListener('click', function () {
        if (Quiz.answered) return;
        picked.push(syl);
        t.disabled = true;
        redraw();
      });
      bank.appendChild(t);
    });

    box.appendChild(answerRow);
    box.appendChild(bank);
    redraw();

    var check = U.el('button', { class: 'btn', type: 'button', text: 'Sprawdź' });
    check.addEventListener('click', function () {
      if (Quiz.answered) return;
      Quiz.answered = true;
      var ok = picked.join(' ') === target.join(' ');
      box.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: hideTones() }));
      Progress.answer(rec.id, ok, { mode: 'assemble' });
      Progress.tempoAnswer('assemble', CompTempo.current, ok);
      SRS.add(rec.id, 'r');
      SRS.grade(rec.id, ok ? 4 : 1, { side: 'r' });
      feedback(box, ok, ok ? '' : 'Poprawna kolejność: ' + rec.thaiPhonetic);
      nextButton(box, onNext);
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [check]));
    Player.play(rec, { btn: play });
  }

  /* ------------------------------------------------------- 4. znajdź słowo */
  function renderSpot(box, onNext) {
    var rec = gv(U.sample(pool(), 1)[0]);
    Quiz.current = rec;
    var options = U.shuffle(Search.similar(rec, 3).concat([rec])).map(gv);

    box.appendChild(U.el('p', { class: 'muted', text: 'Posłuchaj i wskaż właściwy zapis fonetyczny.' }));
    box.appendChild(U.el('p', { class: 'bc-pl', text: 'Znaczenie: ' + rec.polish }));
    var play = Player.button(rec, 'Odtwórz');
    box.appendChild(U.el('div', { class: 'btn-row' }, [play]));

    var list = U.el('div');
    options.forEach(function (opt) {
      var btn = U.el('button', { class: 'opt', type: 'button' });
      btn.appendChild(U.renderPhonetic(opt.thaiPhonetic, { hideTones: false }));
      btn.addEventListener('click', function () {
        if (Quiz.answered) return;
        Quiz.answered = true;
        var ok = opt.id === rec.id;
        btn.classList.add(ok ? 'correct' : 'wrong');
        Progress.answer(rec.id, ok, { mode: 'spot' });
        Progress.tempoAnswer('spot', CompTempo.current, ok);
        SRS.add(rec.id, 'r');
        SRS.grade(rec.id, ok ? 4 : 1, { side: 'r' });
        feedback(box, ok, ok ? '' : 'Poprawnie: ' + rec.thaiPhonetic + ' (' + rec.toneGuide + ')');
        nextButton(box, onNext);
      });
      list.appendChild(btn);
    });
    box.appendChild(list);
    Player.play(rec, { btn: play });
  }

  /* --------------------------------------- 5. forma męska czy żeńska? */
  /* Ćwiczy cechę, której polszczyzna nie zna: płeć słychać w samej wypowiedzi,
     w cząstce końcowej i w zaimku pierwszej osoby. Ucho trzeba tego nauczyć
     osobno, bo w polskim ten sygnał po prostu nie istnieje. */
  function genderPool() {
    var lvl = settings().practiceLevel;
    var list = DB.records.filter(function (r) {
      if (!G.hasVariant(r)) return false;
      if (lvl && r.level !== lvl) return false;
      return r.frequency >= 3;
    });
    if (list.length > 12) return list;
    return DB.records.filter(function (r) { return G.hasVariant(r); });
  }

  /* Wypisuje słowa, po których słychać płeć mówiącego. */
  function marker(phonetic) {
    var out = [];
    ['dì-chǎn', 'chǎn', 'phǒm', 'khráp', 'khâ', 'khá'].forEach(function (w) {
      if (new RegExp('(^|\\s)' + w + '($|\\s)').test(phonetic)) out.push(w);
    });
    return out;
  }

  function renderGenderId(box, onNext) {
    var source = U.sample(genderPool(), 1)[0];
    if (!source) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Baza jeszcze się ładuje…' }));
      return;
    }
    var spoken = Math.random() < 0.5 ? 'female' : 'male';
    var item = G.view(source, spoken);
    Quiz.current = item;

    box.appendChild(U.el('p', { class: 'muted', text:
      'Posłuchaj i wskaż, czy tę wypowiedź mówi kobieta, czy mężczyzna. ' +
      'Słuchaj końcówki zdania i zaimka „ja”.' }));
    box.appendChild(U.el('p', { class: 'bc-pl', text: 'Znaczenie: ' + source.polish }));
    var play = Player.button(item, 'Odtwórz');
    var slow = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wolniej (0,6x)' });
    slow.addEventListener('click', function () { Player.play(item, { btn: slow, rate: 0.6 }); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play, slow]));

    var list = U.el('div');
    [['female', 'Mówi kobieta'], ['male', 'Mówi mężczyzna']].forEach(function (opt) {
      var btn = U.el('button', { class: 'opt', type: 'button', text: opt[1] });
      btn.addEventListener('click', function () {
        if (Quiz.answered) return;
        Quiz.answered = true;
        var ok = opt[0] === spoken;
        btn.classList.add(ok ? 'correct' : 'wrong');
        if (!ok) {
          U.$$('.opt', list).forEach(function (b) {
            if (b.textContent === (spoken === 'female' ? 'Mówi kobieta' : 'Mówi mężczyzna')) {
              b.classList.add('correct');
            }
          });
        }
        Progress.answer(source.id, ok, { mode: 'gender' });
        Progress.tempoAnswer('gender', CompTempo.current, ok);
        SRS.add(source.id, 'r');
        SRS.grade(source.id, ok ? 4 : 1, { side: 'r' });

        var pair = G.pair(source);
        var reveal = U.el('div', { class: 'reveal' });
        reveal.appendChild(U.el('p', { class: 'muted', text:
          'Usłyszałeś formę ' + (spoken === 'female' ? 'żeńską' : 'męską') + '. Porównaj obie:' }));
        [['forma męska', pair.male], ['forma żeńska', pair.female]].forEach(function (row) {
          var line = U.el('div', { class: 'gform' });
          line.appendChild(U.el('div', { class: 'gform-label', text: row[0] }));
          var mid = U.el('div', { class: 'gform-main' });
          mid.appendChild(U.renderPhonetic(row[1].thaiPhonetic, { hideTones: false }));
          var words = marker(row[1].thaiPhonetic);
          if (words.length) {
            mid.appendChild(U.el('div', { class: 'row-meta muted', text: 'sygnał płci: ' + words.join(', ') }));
          }
          line.appendChild(mid);
          var b = U.el('button', { class: 'icon-btn', type: 'button', 'aria-label': 'Posłuchaj — ' + row[0] });
          b.appendChild(U.icon('play'));
          b.addEventListener('click', function () { Player.play(row[1], { btn: b }); });
          line.appendChild(b);
          reveal.appendChild(line);
        });
        box.appendChild(reveal);
        feedback(box, ok, ok ? '' : 'To była forma ' + (spoken === 'female' ? 'żeńska.' : 'męska.'));
        nextButton(box, onNext);
      });
      list.appendChild(btn);
    });
    box.appendChild(list);
    Player.play(item, { btn: play });
  }

  /* ------------------------------------------- 6. rozumienie w hałasie ----

     Rozumienie mowy w ciszy i rozumienie jej w gwarze to dwie różne
     umiejętności. W ciszy wystarczy rozpoznać dźwięki; w hałasie trzeba
     odtworzyć te, które zostały zamaskowane, z reszty wypowiedzi i z sytuacji.
     Nauczony wyłącznie na czystym nagraniu zderza się z tym dopiero
     w restauracji — i zwykle przegrywa.

     Ćwiczenie ma własny, rosnący poziom trudności, niezależny od globalnego
     ustawienia w Ustawieniach: trzy trafne odpowiedzi z rzędu podnoszą hałas
     o stopień, pomyłka go obniża. Dzięki temu każdy siedzi tam, gdzie jest
     na granicy własnej umiejętności, a nie tam, gdzie ustawił suwak. */

  Quiz.noiseLevel = 1;
  Quiz.noiseStreak = 0;

  function renderNoise(box, onNext) {
    var rec = gv(U.sample(pool(), 1)[0]);
    Quiz.current = rec;
    var options = U.shuffle(Search.similar(rec, 3).concat([rec]));

    var kinds = (global.DSP && DSP.supported()) ? DSP.noiseKinds() : [];
    var kind = kinds.length ? kinds[Math.floor(Math.random() * kinds.length)] : null;

    if (!kinds.length) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Ta przeglądarka nie obsługuje Web Audio, więc hałasu nie da się wygenerować. ' +
        'Ćwiczenie działa jak zwykły wybór tłumaczenia.' }));
    } else {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Tło: ' + kind.label + ', poziom ' + Quiz.noiseLevel + ' z 3. ' +
        'Posłuchaj i wybierz polskie znaczenie.' }));
    }

    /* Ustawienia hałasu podajemy przy odtworzeniu, a nie podmieniając stan
       globalny — ćwiczenie ma własny poziom trudności i nie może namieszać
       użytkownikowi w Ustawieniach. */
    /* Poziom trudności zmienia się w trakcie ćwiczenia, więc szum trzeba
       przygotować z wyprzedzeniem — inaczej pierwsze odtworzenie po zmianie
       poziomu czekałoby kilkaset milisekund na wygenerowanie bufora. */
    if (kinds.length && global.DSP && DSP.supported()) {
      var warm = global.requestIdleCallback || function (fn) { return setTimeout(fn, 120); };
      warm(function () {
        /* Wywołanie odłożone „na wolną chwilę” potrafi trafić w moment, gdy
           uczący się jest już na innym ekranie — a generowanie szumu blokuje
           wątek na kilkaset milisekund. Sprawdzamy więc, czy ćwiczenie nadal
           jest tym, na które patrzy. */
        if (Quiz.mode !== 'noise') return;
        try { DSP.noise(kind.id, Quiz.noiseLevel); } catch (e) {}
      });
    }

    function noiseOpts() {
      if (!kinds.length) return { level: 0 };
      return {
        kind: kind.id,
        level: Quiz.noiseLevel,
        room: kind.id === 'station' ? 'hall' : kind.id === 'restaurant' ? 'restaurant' : ''
      };
    }

    var play = U.el('button', { class: 'btn gold play-btn', type: 'button',
      'aria-pressed': 'false', 'aria-label': 'Odtwórz w hałasie' });
    play.appendChild(U.icon('play'));
    play.appendChild(U.el('span', { text: 'Odtwórz' }));
    play.addEventListener('click', function () {
      Player.play(rec, { btn: play, noise: noiseOpts() });
    });

    var clean = U.el('button', { class: 'btn ghost', type: 'button', text: 'Bez hałasu' });
    clean.addEventListener('click', function () {
      Player.play(rec, { btn: clean, noAmbience: true });
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play, clean]));

    var reveal = U.el('div', { class: 'reveal', hidden: 'hidden' });
    reveal.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: hideTones() }));

    var list = U.el('div', { class: 'options' });
    options.forEach(function (opt) {
      var btn = U.el('button', { class: 'btn option', type: 'button', text: opt.polish });
      btn.addEventListener('click', function () {
        if (Quiz.answered) return;
        Quiz.answered = true;
        var ok = opt.id === rec.id;
        Progress.answer(rec.id, ok, { mode: 'noise' });
        Progress.tempoAnswer('noise', CompTempo.current, ok);
        if (ok) {
          Quiz.noiseStreak++;
          if (Quiz.noiseStreak >= 3 && Quiz.noiseLevel < 3) {
            Quiz.noiseLevel++;
            Quiz.noiseStreak = 0;
          }
        } else {
          Quiz.noiseStreak = 0;
          if (Quiz.noiseLevel > 1) Quiz.noiseLevel--;
        }
        reveal.hidden = false;
        box.appendChild(reveal);
        feedback(box, ok, ok ? 'Poziom hałasu: ' + Quiz.noiseLevel + '.'
          : 'To było „' + rec.polish + '”. Posłuchaj jeszcze raz bez hałasu i porównaj.');
        nextButton(box, onNext);
      });
      list.appendChild(btn);
    });
    box.appendChild(list);

    Player.play(rec, { btn: play, noise: noiseOpts() });
  }

  /* Dwa tryby z sesji M mieszkają w osobnym pliku (js/comprehension.js), bo
     działają na innym materiale: nie na hasłach, tylko na kwestiach dialogów
     i adnotacjach z comprehension.json. Wywołujemy je przez globalny obiekt,
     a nie przez referencję zapisaną przy ładowaniu — kolejność skryptów nie
     ma wtedy znaczenia. */
  function renderGap(box, onNext) { Comp.renderGap(box, onNext); }
  function renderUnknown(box, onNext) { Comp.renderUnknown(box, onNext); }

  var RENDERERS = { choice: renderChoice, dictation: renderDictation, assemble: renderAssemble,
                    spot: renderSpot, gender: renderGenderId, noise: renderNoise,
                    gap: renderGap, unknown: renderUnknown };

  /* Tryby oparte na dialogach potrzebują innych plików niż reszta. */
  var DIALOGUE_MODES = { gap: true, unknown: true };

  Quiz.renderListen = function (box) {
    Quiz.renderListenStep(box, function () { Quiz.renderListen(box); });
  };

  /* Jedno ćwiczenie ze słuchu, bez zapętlania.

     Ekran „Słuchanie” po każdej odpowiedzi losuje następne zadanie i robi to
     w nieskończoność — dla ekranu, na którym uczący się siedzi, dopóki chce,
     to jest zachowanie właściwe. Sesja dnia potrzebuje czegoś innego: ma
     policzyć krok, sprawdzić budżet czasu i zdecydować, czy następny krok
     w ogóle należy do tego bloku. Dlatego pętla jest tutaj wyniesiona na
     zewnątrz — `onDone` dostaje sterowanie zamiast rysować kolejne zadanie. */
  Quiz.renderListenStep = function (box, onDone) {
    Quiz.answered = false;
    U.clear(box);
    if (!DB.ready || !DB.records.length) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Baza jeszcze się ładuje…' }));
      return;
    }
    if (DIALOGUE_MODES[Quiz.mode] && !(global.Comp && Comp.ready())) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję materiał do tego trybu…' }));
      DB.ensureComprehension().then(function () {
        if (Quiz.mode && DIALOGUE_MODES[Quiz.mode]) Quiz.renderListenStep(box, onDone);
      });
      return;
    }
    var render = RENDERERS[Quiz.mode] || renderChoice;
    render(box, onDone || function () {});
  };

  /* ============================================================= MÓWIENIE */

  /* Ekran „Wymowa hasła”. Do sesji I kończył się na nagraniu: uczący się
     słyszał wzór, słyszał siebie i musiał sam ocenić, czy trafił w ton — czyli
     musiał już umieć to, czego się dopiero uczy. Teraz po każdym nagraniu
     aplikacja liczy kontur wysokości dźwięku i mówi wprost, która sylaba
     wyszła nie tak i co z nią zrobić. */

  Quiz.stopRecording = function () {
    if (global.PronView) PronView.stopAll();
  };

  /* Jedno ćwiczenie na konkretnym haśle — używa go sesja naprawcza, która
     pyta o hasła z pomyłek, a nie o losowe z puli poziomu. */
  Quiz.renderOne = function (box, rec, onNext) {
    Quiz.answered = false;
    U.clear(box);
    if (Quiz.mode === 'say' || Quiz.mode === 'speak') return Quiz.renderSpeak(box, rec);
    return renderChoice(box, onNext || function () {}, rec);
  };

  Quiz.renderSpeak = function (box, record) {
    U.clear(box);
    if (!DB.ready || !DB.records.length) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Baza jeszcze się ładuje…' }));
      return;
    }
    var source = record || U.sample(pool(), 1)[0];
    var rec = gv(source);
    Quiz.current = rec;

    box.appendChild(U.el('p', { class: 'bc-pl', text: rec.polish }));
    box.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: hideTones() }));
    box.appendChild(U.el('p', { class: 'muted', text: 'Czytaj po polsku: ' + rec.pronunciationPolish }));
    box.appendChild(U.el('p', { class: 'muted', text: rec.toneGuide }));

    var listen = Player.button(rec, 'Wzór');
    var shadow = U.el('button', { class: 'btn ghost', type: 'button', text: 'Powtórz 3× (shadowing)' });
    shadow.addEventListener('click', function () { Player.repeat(rec, 3, { btn: shadow }); });
    var slow = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wolniej (0,75x)' });
    slow.addEventListener('click', function () { Player.play(rec, { btn: slow, rate: 0.75 }); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [listen, shadow, slow]));

    var promptAt = Date.now();
    var control = PronView.control(rec, {
      promptAt: promptAt,
      onResult: function (result, meta) {
        if (!result || !result.ok) return;
        /* Wymowa oceniona trafnie jest mocniejszym dowodem znajomości hasła
           niż rozpoznanie go na liście — podnosi kartę powtórek wyżej. */
        var pace = meta && meta.reactionMs
          ? Progress.recordTime(source.id, meta.reactionMs, 'speak') : null;
        Progress.answer(source.id, result.score >= 60, { mode: 'speak' });
        SRS.add(source.id, 'p');
        SRS.grade(source.id, ToneScore.srsQuality(result), { pace: pace, side: 'p' });
        SRS.notePronunciation(source.id, result);
        if (Quiz.onSpoken) Quiz.onSpoken(source.id, result);
      }
    });
    box.appendChild(control);

    var next = U.el('button', { class: 'btn ghost', type: 'button', text: 'Następne słowo' });
    next.addEventListener('click', function () {
      Quiz.stopRecording();
      Quiz.renderSpeak(box);
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [next]));
  };

  global.Quiz = Quiz;
})(window);
