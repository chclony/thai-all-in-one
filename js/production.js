/* Thai All-in-One — ćwiczenia produkcji.

   Dotychczasowe quizy sprawdzały wyłącznie rozumienie: aplikacja podawała
   tajski, uczący się wybierał polskie znaczenie. Rozpoznanie słowa na liście
   czterech opcji to jednak zupełnie inna umiejętność niż powiedzenie go
   samemu — i tylko ta druga przydaje się w rozmowie.

   Ten moduł odwraca kierunek. Punktem wyjścia jest polski, a uczący się musi
   wyprodukować tajski: ułożyć zdanie, przypomnieć sobie zapis fonetyczny,
   dobrać klasyfikator, rozstrzygnąć ton albo odegrać swoją rolę w dialogu.

   Tryby:
     build      — polski -> tajski, układanie zdania z rozsypanych słów
     type       — polski -> tajski, wpisywanie fonetyki z pamięci
     classifier — dobór klasyfikatora do rzeczownika
     tone       — pary minimalne, wybór właściwego tonu, z oceną wyboru
     say        — polski -> wypowiedź na głos, z oceną konturu tonalnego
     roleplay   — dialog: aplikacja gra partnera, uczący się nagrywa swoją rolę

   Czas reakcji
   ------------
   Każdy tryb mierzy czas od pokazania polecenia do odpowiedzi. Poprawność to
   nie wszystko: hasło odtwarzane po pięciu sekundach jest w rozmowie
   bezużyteczne, a SM-2 tego nie widzi, bo zna wyłącznie „dobrze / źle”.
   Wynik pomiaru trafia do SRS jako tempo i skraca odstęp powtórki. */
(function (global) {
  'use strict';

  var Produce = { mode: 'build', answered: false, current: null };

  /* Etykiety pochodzą z jednego rejestru (U.EX) — patrz js/utils.js. Zostaje
     tu tylko podpowiedź, bo ona jest specyficzna dla tego ekranu. */
  var MODES = [
    { id: 'build',      hint: 'Polski → tajski. Ułóż wypowiedź z rozsypanych słów.' },
    { id: 'type',       hint: 'Polski → tajski. Wpisz fonetykę bez podpowiedzi.' },
    { id: 'classifier', hint: 'Dobierz klasyfikator, którym policzysz ten rzeczownik.' },
    { id: 'tone',       hint: 'Te same głoski, inny ton, inne znaczenie.' },
    { id: 'say',        hint: 'Polski → wypowiedź na głos, bez wzoru przed oczami. Aplikacja ocenia tony i mówi, co poprawić.' },
    { id: 'roleplay',   hint: 'Aplikacja gra partnera, Ty nagrywasz swoje kwestie.' }
  ].map(function (m) { m.label = U.exLabel(m.id); return m; });
  Produce.MODES = MODES;

  function settings() { return U.store.get('settings', {}); }
  function hideTones() { return !!settings().hideTones; }
  function gv(item) { return global.G ? G.view(item) : item; }

  function activeLevel() {
    return settings().practiceLevel || Progress.entryLevel() || '';
  }

  /* Materiał: pełne rekordy z wczytanych plików. Ekran dba o to, żeby
     odpowiedni poziom był w pamięci, zanim tu zajrzymy. */
  function pool(filter) {
    var lvl = activeLevel();
    var list = DB.records.filter(function (r) {
      if (r.type === 'dialogue') return false;
      if (lvl && r.level !== lvl) return false;
      return filter ? filter(r) : true;
    });
    if (list.length < 12) {
      list = DB.records.filter(function (r) {
        return r.type !== 'dialogue' && (filter ? filter(r) : true);
      });
    }
    return list;
  }

  /* Ćwiczenia produkcyjne potrzebują pełnych rekordów — samego indeksu nie da
     się wypowiedzieć. Dociągamy poziom użytkownika, a gdyby był pusty,
     materiał startowy. */
  Produce.ensureData = function () {
    var jobs = [DB.ensureLevel(activeLevel())];
    if (Produce.mode === 'roleplay') jobs.push(DB.ensureDialogues());
    return Promise.all(jobs).then(function () {
      if (!DB.records.length) return DB.ensureStarter();
    });
  };

  /* ------------------------------------------------------------ pomocnicze */

  function feedback(box, ok, text) {
    box.appendChild(U.el('p', { class: ok ? 'fb ok' : 'fb bad', role: 'status' }, [
      U.el('strong', { text: ok ? 'Dobrze! ' : 'Jeszcze raz. ' }),
      document.createTextNode(text || '')
    ]));
  }

  function nextButton(box, onNext, label) {
    var btn = U.el('button', { class: 'btn', type: 'button', text: label || 'Następne' });
    btn.addEventListener('click', onNext);
    box.appendChild(U.el('div', { class: 'btn-row' }, [btn]));
    btn.focus();
  }

  /* Wynik trafia i do postępu, i do powtórek — ćwiczenie produkcyjne jest
     mocniejszym dowodem znajomości hasła niż rozpoznanie go na liście,
     więc trafna odpowiedź dostaje wyższą ocenę SM-2. */
  function score(id, ok, mode) {
    var pace = Produce.promptAt
      ? Progress.recordTime(id, Date.now() - Produce.promptAt, mode) : null;
    Progress.answer(id, ok, { mode: mode });
    /* Wszystkie tryby przechodzące przez tę funkcję są produkcyjne z
       definicji — punktem wyjścia jest polski, a uczący się ma wytworzyć
       tajski. To jest dokładnie ta strona, której brak wykrywa statystyka
       gramatyczna. */
    Progress.grammarAnswer(id, ok, 'productive');
    SRS.add(id, 'p');
    SRS.grade(id, ok ? 5 : 1, { pace: pace, side: 'p' });
    if (Produce.onAnswer) Produce.onAnswer(id, ok);
  }

  function words(phonetic) {
    return (phonetic || '').split(/\s+/).filter(Boolean);
  }

  function normalise(text) {
    return U.fold(U.stripTones(text || '')).replace(/[^a-z]/g, '');
  }

  /* ==================================================== 1. UŁÓŻ ZDANIE */

  function renderBuild(box, onNext, forced) {
    var candidates = pool(function (r) {
      var w = words(r.thaiPhonetic);
      return r.type !== 'word' && w.length >= 2 && w.length <= 7;
    });
    if (!forced && !candidates.length) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Brak materiału do tego ćwiczenia na wybranym poziomie.' }));
      return;
    }
    var source = forced || U.sample(candidates, 1)[0];
    if (!candidates.length) candidates = [source];
    var rec = gv(source);
    Produce.current = rec;

    var target = words(rec.thaiPhonetic);

    box.appendChild(U.el('p', { class: 'muted', text: 'Powiedz to po tajsku. Ułóż wypowiedź, dotykając słów po kolei.' }));
    box.appendChild(U.el('p', { class: 'bc-pl', text: rec.polish }));

    /* Dystraktory: słowa z innych wypowiedzi tego samego poziomu. Bez nich
       ćwiczenie sprowadza się do porządkowania i nie sprawdza doboru słów. */
    var noise = [];
    U.sample(candidates, 6).forEach(function (other) {
      words(other.thaiPhonetic).forEach(function (w) {
        if (target.indexOf(w) === -1 && noise.indexOf(w) === -1) noise.push(w);
      });
    });
    var extras = U.sample(noise, Math.min(3, Math.max(1, Math.floor(target.length / 2))));
    var tiles = U.shuffle(target.concat(extras));

    var picked = [];
    var answer = U.el('div', { class: 'tokens answer', 'aria-live': 'polite' });
    var bank = U.el('div', { class: 'tokens' });
    box.appendChild(U.el('p', { class: 'muted sr-only', id: 'build-help', text: 'Wybrane słowa pojawiają się w linii odpowiedzi. Dotknij słowa w odpowiedzi, żeby je cofnąć.' }));
    box.appendChild(answer);
    box.appendChild(bank);

    function redraw() {
      U.clear(answer);
      if (!picked.length) {
        answer.appendChild(U.el('span', { class: 'muted', text: 'Tutaj pojawi się Twoje zdanie.' }));
      }
      picked.forEach(function (w, i) {
        var t = U.el('button', {
          class: 'token picked', type: 'button', text: hideTones() ? U.stripTones(w) : w,
          'aria-label': 'Cofnij słowo ' + w
        });
        t.addEventListener('click', function () {
          if (Produce.answered) return;
          picked.splice(i, 1);
          redraw();
        });
        answer.appendChild(t);
      });
    }

    U.clear(bank);
    tiles.forEach(function (w) {
      var t = U.el('button', {
        class: 'token', type: 'button', text: hideTones() ? U.stripTones(w) : w,
        'aria-label': 'Dodaj słowo ' + w, 'aria-describedby': 'build-help'
      });
      t.addEventListener('click', function () {
        if (Produce.answered) return;
        picked.push(w);
        t.disabled = true;
        redraw();
      });
      bank.appendChild(t);
    });
    redraw();

    var check = U.el('button', { class: 'btn', type: 'button', text: 'Sprawdź' });
    var clear = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wyczyść' });
    clear.addEventListener('click', function () {
      if (Produce.answered) return;
      picked = [];
      U.$$('.token', bank).forEach(function (t) { t.disabled = false; });
      redraw();
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [check, clear]));

    check.addEventListener('click', function () {
      if (Produce.answered) return;
      if (!picked.length) { U.toast('Ułóż najpierw zdanie.'); return; }
      Produce.answered = true;
      var ok = normalise(picked.join(' ')) === normalise(target.join(' '));

      var reveal = U.el('div', { class: 'reveal' });
      reveal.appendChild(U.el('p', { class: 'muted', text: 'Poprawnie:' }));
      reveal.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: hideTones() }));
      if (rec.pronunciationPolish) {
        reveal.appendChild(U.el('p', { class: 'muted', text: 'Czytaj po polsku: ' + rec.pronunciationPolish }));
      }
      reveal.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(rec, 'Posłuchaj wzoru')]));
      box.appendChild(reveal);

      score(source.id, ok, 'build');
      feedback(box, ok, ok ? 'Kolejność słów się zgadza.'
        : 'W tajskim szyk jest stały: podmiot, czasownik, dopełnienie, a określenia idą po rzeczowniku.');
      nextButton(box, onNext);
    });
  }

  /* =============================================== 2. WPISZ Z PAMIĘCI */

  function renderType(box, onNext, forced) {
    var candidates = pool(function (r) {
      var w = words(r.thaiPhonetic);
      return w.length >= 1 && w.length <= 5;
    });
    if (!forced && !candidates.length) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Brak materiału do tego ćwiczenia na wybranym poziomie.' }));
      return;
    }
    var source = forced || U.sample(candidates, 1)[0];
    var rec = gv(source);
    Produce.current = rec;

    box.appendChild(U.el('p', { class: 'muted', text: 'Wpisz fonetykę z pamięci. Znaki tonów możesz pominąć — sprawdzamy same głoski.' }));
    box.appendChild(U.el('p', { class: 'bc-pl', text: rec.polish }));

    var label = U.el('label', { class: 'sr-only', for: 'produce-type-input', text: 'Zapis fonetyczny po tajsku' });
    var input = U.el('input', {
      id: 'produce-type-input', type: 'text', autocomplete: 'off',
      autocapitalize: 'none', spellcheck: 'false',
      placeholder: 'np. khǎw chûai phǒm nòi'
    });
    box.appendChild(label);
    box.appendChild(input);

    var hintBtn = U.el('button', { class: 'btn ghost', type: 'button', text: 'Podpowiedz pierwszą sylabę' });
    var check = U.el('button', { class: 'btn', type: 'button', text: 'Sprawdź' });
    box.appendChild(U.el('div', { class: 'btn-row' }, [check, hintBtn]));
    var hintOut = U.el('p', { class: 'muted', role: 'status' });
    box.appendChild(hintOut);

    var usedHint = false;
    hintBtn.addEventListener('click', function () {
      usedHint = true;
      var syl = U.syllables(rec.thaiPhonetic);
      hintOut.textContent = 'Zaczyna się od: ' + (hideTones() ? U.stripTones(syl[0]) : syl[0])
        + ' · liczba sylab: ' + syl.length;
    });

    check.addEventListener('click', function () {
      if (Produce.answered) return;
      Produce.answered = true;
      var given = normalise(input.value);
      var want = normalise(rec.thaiPhonetic);
      var ok = given === want;
      /* Bliska próba to nie to samo co strzał w ciemno — mówimy o tym wprost,
         ale do powtórek liczy się tylko odpowiedź trafna. */
      var close = !ok && given.length > 2 && (want.indexOf(given) === 0 || given.indexOf(want) === 0);
      input.classList.add(ok ? 'correct' : 'wrong');
      input.disabled = true;

      var reveal = U.el('div', { class: 'reveal' });
      reveal.appendChild(U.el('p', { class: 'muted', text: 'Poprawnie:' }));
      reveal.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: false }));
      if (rec.toneGuide) reveal.appendChild(U.el('p', { class: 'muted', text: rec.toneGuide }));
      reveal.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(rec, 'Posłuchaj')]));
      box.appendChild(reveal);

      score(source.id, ok && !usedHint, 'type');
      feedback(box, ok, ok
        ? (usedHint ? 'Zgadza się — następnym razem spróbuj bez podpowiedzi.' : 'Zapis się zgadza.')
        : (close ? 'Blisko — brakuje końcówki. Porównaj z wzorem.'
                 : 'Porównaj swój zapis z wzorem i posłuchaj wymowy.'));
      nextButton(box, onNext);
    });

    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') check.click(); });
    input.focus();
  }

  /* ================================================= 3. KLASYFIKATORY */

  function renderClassifier(box, onNext) {
    var list = (DB.classifiers || []).filter(function (c) { return (c.nouns || []).length; });
    if (list.length < 4) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Wykaz klasyfikatorów jeszcze się wczytuje…' }));
      return;
    }
    var right = U.sample(list, 1)[0];
    var noun = U.sample(right.nouns, 1)[0];
    Produce.current = right;

    var wrong = U.sample(list.filter(function (c) { return c.id !== right.id; }), 3);
    var options = U.shuffle(wrong.concat([right]));

    box.appendChild(U.el('p', { class: 'muted', text: 'Chcesz policzyć ten rzeczownik. Którym klasyfikatorem?' }));
    var card = U.el('div', { class: 'bigcard' });
    card.appendChild(U.el('div', { class: 'bc-pl', text: noun.polish }));
    card.appendChild(U.renderPhonetic(noun.thaiPhonetic, { hideTones: hideTones() }));
    box.appendChild(card);
    box.appendChild(U.el('p', { class: 'muted', text: 'Szyk w tajskim: rzeczownik + liczba + klasyfikator.' }));

    var wrap = U.el('div');
    options.forEach(function (opt) {
      var btn = U.el('button', {
        class: 'opt', type: 'button',
        'aria-label': 'Klasyfikator ' + opt.classifier
      });
      btn.appendChild(U.el('span', { class: 'opt-main', text: hideTones() ? U.stripTones(opt.classifier) : opt.classifier }));
      btn.addEventListener('click', function () {
        if (Produce.answered) return;
        Produce.answered = true;
        var ok = opt.id === right.id;
        btn.classList.add(ok ? 'correct' : 'wrong');
        if (!ok) {
          U.$$('.opt', wrap).forEach(function (b) {
            if (b.getAttribute('aria-label') === 'Klasyfikator ' + right.classifier) b.classList.add('correct');
          });
        }

        var reveal = U.el('div', { class: 'reveal' });
        reveal.appendChild(U.el('p', {}, [
          U.el('strong', { text: right.classifier + ' — ' }),
          document.createTextNode(right.explanation || '')
        ]));
        var ex = (right.examples || [])[0];
        if (ex) {
          var exCard = U.el('div', { class: 'bigcard' });
          exCard.appendChild(U.el('div', { class: 'bc-pl', text: ex.polish }));
          exCard.appendChild(U.renderPhonetic(ex.thaiPhonetic, { hideTones: hideTones() }));
          exCard.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(ex, 'Posłuchaj')]));
          reveal.appendChild(exCard);
        }
        box.appendChild(reveal);

        var pace = Produce.promptAt
          ? Progress.recordTime(right.id, Date.now() - Produce.promptAt, 'classifier') : null;
        Progress.answer(right.id, ok, { mode: 'classifier', grammarId: 'gram-012' });
        Progress.grammarAnswer(right.id, ok, 'productive');
        SRS.add(right.id, 'p');
        SRS.grade(right.id, ok ? 4 : 1, { pace: pace, side: 'p' });
        if (Produce.onAnswer) Produce.onAnswer(right.id, ok);
        feedback(box, ok, ok ? '' : 'Właściwy klasyfikator to ' + right.classifier + '.');
        nextButton(box, onNext);
      });
      wrap.appendChild(btn);
    });
    box.appendChild(wrap);
  }

  /* ============================================ 4. TONY — PARY MINIMALNE */

  var pairsCache = null;

  /* Para minimalna: te same głoski, inny ton, inne znaczenie. Budujemy je
     z indeksu, grupując jednosylabowe hasła po zapisie bez znaków tonu. */
  function minimalPairs() {
    if (pairsCache) return pairsCache;
    var groups = {};
    (DB.index.length ? DB.index : DB.records).forEach(function (r) {
      var syl = U.syllables(r.thaiPhonetic);
      if (syl.length !== 1) return;
      if (r.type !== 'word' && r.type !== 'noun' && r.type !== 'verb'
        && r.type !== 'adjective' && r.type !== 'adverb') return;
      var base = U.fold(U.stripTones(r.thaiPhonetic));
      if (!base || base.length < 2) return;
      var tone = U.toneOf(r.thaiPhonetic);
      var g = groups[base] || (groups[base] = {});
      /* Jeden reprezentant na ton — inaczej „para” bywałaby dwoma zapisami
         tego samego słowa. */
      if (!g[tone]) g[tone] = r;
    });
    pairsCache = Object.keys(groups).map(function (base) {
      var tones = Object.keys(groups[base]);
      return { base: base, tones: tones, items: tones.map(function (t) { return groups[base][t]; }) };
    }).filter(function (g) { return g.items.length >= 2; });
    return pairsCache;
  }

  function renderTone(box, onNext) {
    /* Ten sam powód co na ekranie „Powtarzaj za wzorem”: pary minimalne to
       jedyne ćwiczenie, w którym uczący się regularnie potrzebuje OPISU tonu,
       a nie kolejnej próby. Przewodnik dostaje wejście stąd. */
    var guide = U.el('button', { class: 'btn ghost', type: 'button',
      text: 'Przewodnik po tonach' });
    guide.addEventListener('click', function () { if (global.App) App.go('pron'); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [guide]));
    var pairs = minimalPairs();
    if (!pairs.length) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Nie znaleziono par minimalnych w tym materiale.' }));
      return;
    }
    var group = U.sample(pairs, 1)[0];
    var target = U.sample(group.items, 1)[0];
    Produce.current = target;

    box.appendChild(U.el('p', { class: 'muted', text:
      'Te słowa różnią się wyłącznie tonem. Posłuchaj i wskaż, które usłyszałeś.' }));

    var play = Player.button(target, 'Odtwórz');
    var slow = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wolniej (0,6x)' });
    slow.addEventListener('click', function () { Player.play(DB.any(target.id), { btn: slow, rate: 0.6 }); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play, slow]));

    var wrap = U.el('div');
    U.shuffle(group.items).forEach(function (opt) {
      var tone = U.toneOf(opt.thaiPhonetic);
      var btn = U.el('button', {
        class: 'opt tone-opt', type: 'button',
        'aria-label': opt.polish + ', ton ' + tone + ', zapis ' + opt.thaiPhonetic
      });
      var main = U.el('span', { class: 'opt-main' });
      main.appendChild(U.toneMark(tone));
      main.appendChild(U.el('span', { text: opt.thaiPhonetic }));
      btn.appendChild(main);
      btn.appendChild(U.el('span', { class: 'opt-sub', text: opt.polish + ' · ton ' + tone }));

      btn.addEventListener('click', function () {
        if (Produce.answered) return;
        Produce.answered = true;
        var ok = opt.id === target.id;
        btn.classList.add(ok ? 'correct' : 'wrong');
        if (!ok) {
          U.$$('.opt', wrap).forEach(function (b) {
            if (b.getAttribute('aria-label').indexOf(target.polish + ', ton') === 0) b.classList.add('correct');
          });
        }

        /* Ocena wyboru: nie wystarczy „źle”. Mówimy, jaki ton uczący się
           wybrał, jaki był naprawdę i czym te dwa kontury się różnią. */
        var chosen = U.toneOf(opt.thaiPhonetic);
        var real = U.toneOf(target.thaiPhonetic);
        var reveal = U.el('div', { class: 'reveal' });
        var row = U.el('div', { class: 'tone-compare' });
        [['Wybrałeś', chosen, opt], ['Usłyszałeś', real, target]].forEach(function (entry) {
          var cell = U.el('div', { class: 'tone-cell' });
          cell.appendChild(U.el('div', { class: 'row-meta muted', text: entry[0] }));
          var line = U.el('div', { class: 'tone-line' });
          line.appendChild(U.toneMark(entry[1]));
          line.appendChild(U.el('span', { text: entry[2].thaiPhonetic }));
          cell.appendChild(line);
          cell.appendChild(U.el('div', { class: 'row-meta', text: 'ton ' + entry[1] + ' · ' + entry[2].polish }));
          var b = U.el('button', { class: 'icon-btn', type: 'button', 'aria-label': 'Posłuchaj: ' + entry[2].polish });
          b.appendChild(U.icon('play'));
          b.addEventListener('click', function () { Player.play(DB.any(entry[2].id), { btn: b }); });
          cell.appendChild(b);
          row.appendChild(cell);
        });
        reveal.appendChild(row);
        if (!ok) {
          reveal.appendChild(U.el('p', { class: 'muted', text: toneAdvice(chosen, real) }));
        }
        box.appendChild(reveal);

        var pace = Produce.promptAt
          ? Progress.recordTime(target.id, Date.now() - Produce.promptAt, 'tone') : null;
        Progress.answer(target.id, ok, { mode: 'tone' });
        SRS.add(target.id, 'r');
        SRS.grade(target.id, ok ? 4 : 1, { pace: pace, side: 'r' });
        if (Produce.onAnswer) Produce.onAnswer(target.id, ok);
        feedback(box, ok, ok ? 'Ton rozpoznany prawidłowo.' : '');
        nextButton(box, onNext);
      });
      wrap.appendChild(btn);
    });
    box.appendChild(wrap);
    Player.play(DB.any(target.id), { btn: play });
  }

  /* Podpowiedź dopasowana do konkretnej pomyłki. Polak myli przede wszystkim
     ton opadający ze zwykłym zdaniem oznajmującym i ton wysoki ze średnim. */
  function toneAdvice(chosen, real) {
    var key = chosen + '>' + real;
    var map = {
      'opadający>wysoki': 'Ton wysoki trzyma się równo u góry. Ton opadający startuje wysoko i wyraźnie spada — to różnica, którą słychać na końcu sylaby.',
      'wysoki>opadający': 'Ton opadający ma wyraźny spadek. Jeśli słyszysz płaskie, równe brzmienie — to ton wysoki.',
      'średni>wysoki': 'Ton wysoki leży zauważalnie wyżej niż średni i lekko się podnosi. Ton średni jest płaski, na poziomie zwykłej mowy.',
      'wysoki>średni': 'Ton średni jest płaski i neutralny. Jeśli sylaba nie wyróżnia się wysokością — to ton średni.',
      'rosnący>niski': 'Ton rosnący najpierw opada, a potem idzie w górę. Ton niski leży płasko, poniżej poziomu mowy.',
      'niski>rosnący': 'Ton rosnący kończy się wyraźnie wyżej, niż zaczyna. Ton niski nie zmienia wysokości.',
      'opadający>rosnący': 'To kontury lustrzane. Opadający zaczyna wysoko i spada, rosnący zaczyna nisko i idzie w górę.',
      'rosnący>opadający': 'To kontury lustrzane. Zwróć uwagę na sam początek sylaby: wysoko czy nisko?'
    };
    return map[key] || ('Ton ' + chosen + ' i ton ' + real
      + ' różnią się przebiegiem wysokości. Odsłuchaj oba nagrania jedno po drugim i porównaj kontury nad zapisem.');
  }

  /* ============================================ 5. WYMÓW POPRAWNIE */

  /* Tryb produkcyjny w najczystszej postaci: na wejściu polski, na wyjściu
     wypowiedź na głos. Nie ma tu przycisków do wyboru ani pola tekstowego —
     jedynym sposobem odpowiedzi jest powiedzenie czegoś, a jedynym sędzią
     kontur wysokości dźwięku. Hasło wraca, dopóki tony się nie zgodzą. */

  var sayState = { id: null, attempts: 0, hinted: false, best: 0 };

  function renderSay(box, onNext, forced) {
    /* Materiał krótki: przy siedmiu sylabach ocena konturu robi się
       orientacyjna, a ćwiczenie zamienia się w test pamięci. */
    var candidates = pool(function (r) {
      var w = U.syllables(r.thaiPhonetic);
      return w.length >= 1 && w.length <= 4;
    });
    if (!forced && !candidates.length) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Brak materiału do tego ćwiczenia na wybranym poziomie.' }));
      return;
    }
    var source = forced
      || (sayState.id && DB.get(sayState.id)) || U.sample(candidates, 1)[0];
    if (source.id !== sayState.id) {
      sayState = { id: source.id, attempts: 0, hinted: false, best: 0 };
    }
    var rec = gv(source);
    Produce.current = rec;
    Produce.promptAt = Date.now();

    box.appendChild(U.el('p', { class: 'muted', text:
      'Powiedz to po tajsku na głos. Aplikacja policzy przebieg wysokości Twojego głosu '
      + 'i porówna go z wzorcem — sylaba po sylabie.' }));
    box.appendChild(U.el('p', { class: 'bc-pl', text: rec.polish }));

    if (sayState.attempts) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Próba ' + (sayState.attempts + 1) + '. Najlepszy dotąd wynik: ' + sayState.best + '/100.' }));
    }

    /* Podpowiedź jest dostępna, ale kosztuje: hasło z podpowiedzią nie
       zalicza się jako samodzielna produkcja. */
    var reveal = U.el('div', { class: 'reveal', hidden: 'hidden' });
    reveal.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: false }));
    reveal.appendChild(U.el('p', { class: 'muted', text: 'Czytaj po polsku: ' + rec.pronunciationPolish }));
    if (rec.toneGuide) reveal.appendChild(U.el('p', { class: 'muted', text: rec.toneGuide }));
    reveal.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(rec, 'Posłuchaj wzoru')]));

    var hint = U.el('button', {
      class: 'btn ghost', type: 'button',
      text: 'Nie wiem — pokaż zapis i wzór', 'aria-expanded': 'false', 'aria-controls': 'say-reveal'
    });
    reveal.id = 'say-reveal';
    hint.addEventListener('click', function () {
      sayState.hinted = true;
      reveal.hidden = false;
      hint.setAttribute('aria-expanded', 'true');
      hint.disabled = true;
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [hint]));
    box.appendChild(reveal);

    var after = U.el('div');
    var control = PronView.control(rec, {
      promptAt: Produce.promptAt,
      label: 'Nagraj i oceń wymowę',
      onResult: function (result, meta) {
        if (!result || !result.ok) return;
        sayState.attempts += 1;
        sayState.best = Math.max(sayState.best, result.score);

        var pace = meta && meta.reactionMs
          ? Progress.recordTime(source.id, meta.reactionMs, 'say') : null;
        var passed = result.score >= 70 && !sayState.hinted;
        Progress.answer(source.id, result.score >= 70, { mode: 'say' });
        SRS.add(source.id, 'p');
        var q = ToneScore.srsQuality(result);
        SRS.grade(source.id, sayState.hinted ? Math.min(3, q) : q,
          { pace: pace, side: 'p' });
        SRS.notePronunciation(source.id, result);
        if (Produce.onAnswer) Produce.onAnswer(source.id, result.score >= 70);

        U.clear(after);
        if (result.score >= 70) {
          feedback(after, true, sayState.hinted
            ? 'Tony się zgadzają — następnym razem spróbuj bez podpowiedzi.'
            : 'Tony się zgadzają. To już umiesz powiedzieć.');
          var nb = U.el('button', { class: 'btn', type: 'button', text: 'Następne hasło' });
          nb.addEventListener('click', function () {
            sayState = { id: null, attempts: 0, hinted: false, best: 0 };
            onNext();
          });
          var again = U.el('button', { class: 'btn ghost', type: 'button', text: 'Powtórz to samo' });
          /* Ponowienie musi wrócić do renderSay z TYM SAMYM onNext. Wołanie
             Produce.render zaczynało pętlę ekranu „Mówienie po tajsku” i w sesji
             dnia odbierało sterowanie blokowi, który ten krok zamawiał. */
          again.addEventListener('click', function () { U.clear(box); renderSay(box, onNext); });
          after.appendChild(U.el('div', { class: 'btn-row' }, [nb, again]));
          nb.focus();
        } else {
          after.appendChild(U.el('p', { class: 'muted', text:
            'Posłuchaj wzoru, popraw wskazane sylaby i nagraj jeszcze raz. '
            + 'Możesz też przejść dalej i wrócić do tego hasła później.' }));
          var retry = U.el('button', { class: 'btn', type: 'button', text: 'Spróbuj jeszcze raz' });
          retry.addEventListener('click', function () { U.clear(box); renderSay(box, onNext); });
          var skip = U.el('button', { class: 'btn ghost', type: 'button', text: 'Inne hasło' });
          skip.addEventListener('click', function () {
            sayState = { id: null, attempts: 0, hinted: false, best: 0 };
            onNext();
          });
          after.appendChild(U.el('div', { class: 'btn-row' }, [retry, skip]));
          retry.focus();
        }
        if (passed) SRS.add(source.id, 'p');
      }
    });
    box.appendChild(control);
    box.appendChild(after);

    if (!PronView.canRecord() || !Pitch.supported) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Bez mikrofonu ten tryb nie oceni wymowy. Pozostałe ćwiczenia produkcyjne '
        + 'działają normalnie — wybierz „Ułóż zdanie” albo „Wpisz z pamięci”.' }));
      var alt = U.el('button', { class: 'btn ghost', type: 'button', text: 'Inne hasło' });
      alt.addEventListener('click', function () {
        sayState = { id: null, attempts: 0, hinted: false, best: 0 };
        onNext();
      });
      box.appendChild(U.el('div', { class: 'btn-row' }, [alt]));
    }
  }

  /* ================================================= 6. ODEGRAJ DIALOG */

  /* Nagrania kwestii żyją tylko w tej karcie przeglądarki. Trzymamy adres
     obiektowy do złożenia całej rozmowy oraz ocenę wymowy każdej kwestii. */
  var Rec = { takes: {}, scores: {} };

  Produce.stopRecording = function () {
    if (global.PronView) PronView.stopAll();
  };

  /* Nagranie kwestii żyje jako adres blob:. Samo wyrzucenie go z mapy NIE
     zwalnia pamięci — przeglądarka trzyma bufor tak długo, aż adres zostanie
     jawnie unieważniony. Przy role-play, gdzie jedną kwestię nagrywa się po
     kilka razy, a dialog ma kilkanaście kwestii, dawało to kilkadziesiąt
     porzuconych nagrań na godzinę ćwiczeń i rosło do końca życia karty.
     Dlatego każde odejście od nagrania przechodzi przez to jedno miejsce. */
  function releaseTake(index) {
    var url = Rec.takes[index];
    if (url) { try { URL.revokeObjectURL(url); } catch (e) {} }
    delete Rec.takes[index];
  }

  /* Jedyna droga, którą nagranie trafia do mapy. Poprzednie podejście na tej
     samej kwestii jest zwalniane, zanim straci ostatnią referencję. */
  Produce.noteTake = function (index, url) {
    if (!url) return;
    releaseTake(index);
    Rec.takes[index] = url;
  };

  /* Dostęp do stanu nagrań dla testów — kod ekranu korzysta z Rec wprost. */
  Produce.rec = function () { return Rec; };

  Produce.resetTakes = function () {
    Object.keys(Rec.takes).forEach(releaseTake);
    Rec.takes = {};
    Rec.scores = {};
  };

  var rolePlay = { dialogueId: null, role: 'A' };

  function renderRolePlay(box, onNext) {
    var list = DB.dialogues;
    if (!list.length) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Dialogi jeszcze się wczytują…' }));
      return;
    }
    var dlg = DB.get(rolePlay.dialogueId) || U.sample(list, 1)[0];
    rolePlay.dialogueId = dlg.id;
    Produce.current = dlg;

    /* --- wybór dialogu i roli --- */
    var head = U.el('div', { class: 'filters' });
    var selLabel = U.el('label', { class: 'sr-only', for: 'rp-dlg', text: 'Wybierz dialog' });
    var sel = U.el('select', { id: 'rp-dlg' });
    list.slice().sort(function (a, b) { return a.id < b.id ? -1 : 1; }).forEach(function (d) {
      var o = U.el('option', { value: d.id, text: d.level + ' · ' + d.title });
      if (d.id === dlg.id) o.setAttribute('selected', 'selected');
      sel.appendChild(o);
    });
    sel.addEventListener('change', function () {
      rolePlay.dialogueId = sel.value;
      Produce.resetTakes();
      Produce.render(box);
    });
    head.appendChild(selLabel);
    head.appendChild(sel);

    ['A', 'B'].forEach(function (role) {
      var chip = U.el('button', {
        class: 'chip', type: 'button',
        'aria-pressed': rolePlay.role === role ? 'true' : 'false',
        text: 'Gram rolę ' + role + ': ' + (dlg.roles ? dlg.roles[role] : role)
      });
      chip.addEventListener('click', function () {
        rolePlay.role = role;
        Produce.resetTakes();
        Produce.render(box);
      });
      head.appendChild(chip);
    });
    box.appendChild(head);

    var mine = rolePlay.role;
    var lines = G.viewAll(dlg.lines);
    var myLines = lines.filter(function (l) { return l.role === mine; });

    box.appendChild(U.el('p', { class: 'muted', text:
      'Aplikacja odtwarza kwestie partnera. Twoje kwestie nagrywasz sam, a na końcu '
      + 'odsłuchujesz całość jako jedną rozmowę. Nagrania zostają tylko w tej karcie '
      + 'przeglądarki — nigdzie ich nie wysyłamy.' }));

    if (!PronView.canRecord() || !Pitch.supported) {
      box.appendChild(U.el('p', { class: 'fb bad', text: PronView.micMessage()
        + ' Kwestie partnera odtworzysz normalnie, więc dialog da się odegrać na głos.' }));
    }

    /* --- lista kwestii --- */
    var wrap = U.el('div', { class: 'roleplay' });
    lines.forEach(function (line) {
      var isMine = line.role === mine;
      var row = U.el('div', { class: 'line rp-line' + (isMine ? ' rp-mine' : ''), 'data-line': line.index });
      var speaker = G.speakerOf(line);
      var tag = U.el('span', { class: 'role' + (line.role === 'B' ? ' b' : ''), text: line.role });
      tag.setAttribute('data-gender', speaker);
      tag.setAttribute('title', 'Rola ' + line.role + ' — mówi ' + G.label(speaker));
      row.appendChild(tag);

      var mid = U.el('div');
      mid.appendChild(U.el('div', { class: 'l-pl', text: line.polish }));
      if (isMine) {
        mid.appendChild(U.renderPhonetic(line.thaiPhonetic, { hideTones: hideTones() }));
        mid.appendChild(U.el('div', { class: 'row-meta muted', text: 'Czytaj: ' + line.pronunciationPolish }));
      } else {
        mid.appendChild(U.el('div', { class: 'l-ph', text: hideTones() ? U.stripTones(line.thaiPhonetic) : line.thaiPhonetic }));
      }
      row.appendChild(mid);

      var actions = U.el('div', { class: 'rp-actions' });
      var listen = U.el('button', { class: 'icon-btn', type: 'button',
        'aria-label': 'Posłuchaj kwestii ' + line.index });
      listen.appendChild(U.icon('play'));
      listen.addEventListener('click', function () { Player.play(line, { btn: listen }); });
      actions.appendChild(listen);

      if (isMine) {
        /* Ocena wymowy tej kwestii pojawia się pod wierszem, więc lista
           kwestii zostaje czytelna, dopóki uczący się nie nagra. */
        var state = U.el('span', { class: 'row-meta muted rp-score', role: 'status' });
        if (Rec.scores[line.index]) {
          state.textContent = 'nagrane · ' + Rec.scores[line.index] + '/100';
        }
        actions.appendChild(state);
      }
      row.appendChild(actions);
      wrap.appendChild(row);

      if (isMine) {
        var promptAt = Date.now();
        var control = PronView.control(line, {
          promptAt: promptAt,
          compact: true,
          label: 'Nagraj kwestię ' + line.index,
          onResult: function (result, meta) {
            /* Powtórne nagranie tej samej kwestii zastępuje poprzednie —
               poprzednie musi zostać zwolnione, inaczej zostaje w pamięci
               bez żadnego sposobu, by się do niego dostać. */
            if (meta && meta.url) Produce.noteTake(line.index, meta.url);
            if (result && result.ok) {
              Rec.scores[line.index] = result.score;
              var st = U.$('[data-line="' + line.index + '"] .rp-score', wrap);
              if (st) st.textContent = 'nagrane · ' + result.score + '/100';
              /* Kwestia dialogu też jest hasłem — trafna wymowa podnosi kartę
                 powtórek tak samo jak w ćwiczeniu pojedynczego zwrotu. */
              var pace = meta.reactionMs
                ? Progress.recordTime(dlg.id, meta.reactionMs, 'roleplay') : null;
              Progress.answer(dlg.id, result.score >= 60, { mode: 'roleplay' });
              SRS.add(dlg.id, 'p');
              SRS.grade(dlg.id, ToneScore.srsQuality(result), { pace: pace, side: 'p' });
              SRS.notePronunciation(dlg.id, result);
            }
            updateWhole();
          }
        });
        wrap.appendChild(U.el('div', { class: 'rp-control' }, [control]));
      }
    });
    box.appendChild(wrap);

    /* --- odtworzenie całości --- */
    var whole = U.el('button', { class: 'btn gold', type: 'button', text: 'Odsłuchaj całą rozmowę' });
    var partner = U.el('button', { class: 'btn ghost', type: 'button', text: 'Odtwórz tylko partnera' });
    var again = U.el('button', { class: 'btn ghost', type: 'button', text: 'Inny dialog' });
    var status = U.el('p', { class: 'muted', role: 'status' });

    function recordedCount() {
      return myLines.filter(function (l) { return Rec.takes[l.index]; }).length;
    }
    function updateWhole() {
      var n = recordedCount();
      status.textContent = n + ' z ' + myLines.length + ' '
        + U.plural(myLines.length, 'Twojej kwestii nagrana', 'Twoich kwestii nagrane', 'Twoich kwestii nagranych') + '.';
      whole.disabled = n === 0;
    }

    /* Rozmowa złożona: kwestie partnera idą z syntezatora, Twoje z nagrania.
       Nienagrane kwestie zastępujemy wzorem, żeby dało się odsłuchać całość
       nawet w trakcie pracy. */
    function playWhole() {
      Player.stop();
      var i = 0;
      U.$$('.rp-line', wrap).forEach(function (n) { n.classList.remove('current'); });
      (function step() {
        if (i >= lines.length) {
          U.$$('.rp-line', wrap).forEach(function (n) { n.classList.remove('current'); });
          whole.classList.remove('playing');
          return;
        }
        var line = lines[i++];
        U.$$('.rp-line', wrap).forEach(function (n) { n.classList.remove('current'); });
        var node = U.$('[data-line="' + line.index + '"]', wrap);
        if (node) node.classList.add('current');

        var take = line.role === mine ? Rec.takes[line.index] : null;
        if (take) {
          var el = new Audio(take);
          el.onended = function () { setTimeout(step, 350); };
          el.onerror = function () { setTimeout(step, 350); };
          el.play()['catch'](function () { setTimeout(step, 350); });
        } else {
          Player.play(line, { onend: function () { setTimeout(step, 350); }, silentWarning: true });
        }
      })();
      whole.classList.add('playing');
    }

    whole.addEventListener('click', playWhole);
    partner.addEventListener('click', function () {
      Player.playSequence(lines.filter(function (l) { return l.role !== mine; }), { btn: partner });
    });
    again.addEventListener('click', function () {
      Produce.stopRecording();
      Produce.resetTakes();
      rolePlay.dialogueId = U.sample(list, 1)[0].id;
      Produce.render(box);
    });

    box.appendChild(U.el('div', { class: 'btn-row' }, [whole, partner, again]));
    box.appendChild(status);
    updateWhole();

    /* Odegranie dialogu liczymy jako kontakt z materiałem, nie jako test. */
    Progress.answer(dlg.id, true, { mode: 'roleplay' });
  }

  /* ==================================================== render i przełącznik */

  var RENDERERS = {
    build: renderBuild, type: renderType, classifier: renderClassifier,
    tone: renderTone, say: renderSay, roleplay: renderRolePlay
  };

  /* Ustawia dialog do odegrania — używane, gdy uczący się wchodzi w role-play
     prosto z lekcji, a nie z listy. */
  Produce.setDialogue = function (id) {
    rolePlay.dialogueId = id;
    Produce.resetTakes();
  };

  /* Jedno ćwiczenie na konkretnym haśle. Sprawdzian lekcji pyta o dokładnie
     te hasła, które lekcja wprowadziła — nie o losowe z poziomu. */
  Produce.renderOne = function (box, rec, onNext) {
    Produce.answered = false;
    Produce.promptAt = Date.now();
    U.clear(box);
    /* Trybom, które umieją przyjąć wymuszone hasło, podajemy je wprost.
       „Klasyfikatory” dobierają materiał same z reguł gramatycznych i nie da
       się ich wskazać hasłem — sprowadzamy je wtedy do układania zdania,
       żeby sesja naprawcza nie zatrzymała się na pustym ekranie. */
    var run;
    if (Produce.mode === 'type') run = renderType;
    else if (Produce.mode === 'say') run = renderSay;
    else run = renderBuild;
    run(box, onNext, rec);
  };

  Produce.render = function (box) {
    Produce.renderStep(box, function () { Produce.render(box); });
  };

  /* Jedno ćwiczenie produkcyjne, bez zapętlania — uzasadnienie przy
     Quiz.renderListenStep. Sesja dnia sama decyduje, co dalej. */
  Produce.renderStep = function (box, onDone) {
    Produce.answered = false;
    Produce.stopRecording();
    /* Zegar czasu reakcji startuje w chwili, gdy polecenie trafia na ekran. */
    Produce.promptAt = Date.now();
    U.clear(box);
    if (!DB.ready) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Baza jeszcze się ładuje…' }));
      return;
    }
    if (Produce.mode !== 'classifier' && Produce.mode !== 'roleplay' && !DB.records.length) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję materiał do ćwiczeń…' }));
      Produce.ensureData().then(function () { Produce.renderStep(box, onDone); });
      return;
    }
    var run = RENDERERS[Produce.mode] || renderBuild;
    run(box, onDone || function () {});
  };

  global.Produce = Produce;
})(window);
