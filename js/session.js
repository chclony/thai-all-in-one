/* Thai All-in-One — sesja dnia.

   PROBLEM
   =======
   Aplikacja ma kilkanaście ekranów i ponad dwadzieścia trybów ćwiczeń. Dopóki
   uczący się musi codziennie sam wybierać, czym się dziś zająć, płaci za to
   dwa razy: raz zmęczeniem decyzją, a drugi raz tym, że wybiera źle. Wybiera
   to, co lubi (rozpoznawanie, bo idzie gładko) zamiast tego, co potrzebne
   (wytwarzanie i wymowa, bo boli). Kolejka powtórek czeka, bo nie jest
   atrakcyjna.

   Ten moduł zdejmuje tę decyzję. Jeden przycisk, jedna zaplanowana sesja,
   skład dobrany z aktualnego stanu nauki.

   ZASADY SKŁADU
   =============
   1. ZALEGŁE POWTÓRKI MAJĄ PIERWSZEŃSTWO. Hasło zapomniane to hasło, którego
      nauka poszła na marne. Im większa zaległość, tym większy udział powtórek
      — aż do połowy sesji. Wyżej nie idziemy: sesja złożona wyłącznie
      z powtórek nie posuwa nauki do przodu i po tygodniu takich sesji uczący
      się przestaje przychodzić.
   2. NAJSŁABSZY OBSZAR DOSTAJE DODATKOWY BLOK. „Najsłabszy” bierzemy z dwóch
      niezależnych źródeł: statystyki błędów (Progress.worstArea — gdzie się
      mylisz) i pokrycia rozumienia (Coverage.weakest — czego nie rozumiesz).
      Pierwsze wskazuje tryb ćwiczenia, drugie kategorię materiału.
   3. WYMOWA WRACA CO KILKA DNI. Ocena wymowy wymaga nagrania i ciszy — nie da
      się jej robić codziennie w autobusie. Co PRON_EVERY dni sesja rezerwuje
      na nią osobny blok; w pozostałe dni nie ma jej wcale.
   4. BLOKI SĄ WYMIESZANE, nie ustawione po kolei. Dwadzieścia powtórek pod
      rząd to dwadzieścia minut jednego rodzaju wysiłku. Blok dłuższy niż
      CHUNK kroków jest dzielony na części i przeplatany innymi.

   BUDŻET CZASU
   ============
   Sesja jest odmierzona czasem, nie liczbą zadań — bo to czasem dysponuje
   uczący się („mam dwadzieścia minut”), a nie liczbą kart. Każdy rodzaj kroku
   ma oszacowany czas trwania (SECONDS), z niego wychodzi liczba kroków
   w bloku. Szacunki są z pomiaru median czasu odpowiedzi w Progress.timeStats,
   zaokrąglone w górę o czas na przeczytanie polecenia i odsłuch.

   PRZERWANIE I POWRÓT
   ===================
   Stan sesji leży w pamięci przeglądarki po każdym kroku, razem z licznikiem
   zużytego czasu. Zamknięcie karty w połowie nie kosztuje nic: przy powrocie
   sesja wraca do tego samego kroku z tym samym budżetem. Zegar liczy czas
   spędzony w sesji, a nie czas od jej rozpoczęcia — przerwa na obiad nie
   zjada sesji.
*/
(function (global) {
  'use strict';

  var Session = { state: null };

  var KEY = 'session';

  /* Do wyboru: kwadrans w kolejce, pół godziny wieczorem, albo solidny blok. */
  Session.LENGTHS = [10, 20, 40];

  /* Szacowany czas jednego kroku w sekundach. */
  var SECONDS = {
    srs: 12,        // odsłonięcie karty i ocena
    lesson: 22,     // nowe hasło: zapis, znaczenie, odsłuch
    listen: 26,     // odsłuch i wybór
    produce: 32,    // ułożenie albo wpisanie odpowiedzi
    pron: 45        // nagranie, ocena, poprawka
  };
  Session.SECONDS = SECONDS;

  /* Co ile dni wraca blok wymowy. */
  var PRON_EVERY = 3;
  Session.PRON_EVERY = PRON_EVERY;

  /* Najdłuższy ciąg kroków jednego rodzaju bez przerwy. */
  var CHUNK = 6;

  /* Górna granica udziału powtórek — uzasadnienie w nagłówku, zasada 1. */
  var SRS_MAX_SHARE = 0.5;

  /* Najwięcej nowych haseł w jednej sesji.

     Bez tego sufitu długa sesja przy pustej kolejce powtórek wprowadzała
     kilkanaście nowych haseł naraz — a każde z nich wraca nazajutrz jako dwie
     karty. Trzy takie dni i kolejka rośnie szybciej, niż uczący się jest
     w stanie ją wyrabiać. Nowe hasła są jedynym wejściem do kartoteki, więc
     to tutaj jest miejsce na hamulec. */
  var NEW_MAX = 8;
  Session.NEW_MAX = NEW_MAX;

  var LABELS = {
    srs: 'Powtórki',
    lesson: 'Nowa lekcja',
    listen: 'Słuchanie',
    produce: 'Mówienie po tajsku',
    /* Blok „pron” uruchamia tryb `say` (patrz compose: b.mode = 'say'), więc
       i nazywa się tak samo jak on. Do sesji V stało tu „Wymowa i tony” —
       nazwa ekranu z materiałem do czytania, na który ten blok nigdy nie
       prowadził. Etykieta idzie z rejestru, żeby nie mogła się rozjechać. */
    pron: U.exLabel('say')
  };
  Session.LABELS = LABELS;

  /* ------------------------------------------------------- stan i zapis */

  Session.load = function () {
    Session.state = U.store.get(KEY, null);
    return Session.state;
  };

  Session.save = function () {
    if (Session.state) U.store.set(KEY, Session.state);
    else U.store.set(KEY, null);
  };

  Session.clear = function () {
    Session.state = null;
    U.store.set(KEY, null);
  };

  /* Czy jest sesja do wznowienia. Sesja z wczoraj nie jest sesją do
     wznowienia — jej skład opisywał wczorajszy stan powtórek. */
  Session.resumable = function () {
    var s = Session.state;
    return !!(s && !s.finished && s.date === U.today());
  };

  Session.stale = function () {
    var s = Session.state;
    return !!(s && !s.finished && s.date !== U.today());
  };

  /* --------------------------------------------------------- diagnoza */

  /* Ile kart czeka i jak bardzo to zaległość. Plan powtórek ma własny sufit
     dzienny — sesja go nie omija, tylko z niego czyta. */
  function reviewLoad() {
    if (!global.SRS) return { due: 0, cap: 0, pressure: 0 };
    var plan = SRS.plan();
    var cap = plan.cap || 1;
    return {
      due: plan.today.length,
      dueTotal: plan.dueTotal,
      cap: cap,
      /* 0 = nic nie czeka, 1 = kolejka wypełnia cały dzienny sufit. */
      pressure: Math.min(1, plan.today.length / cap)
    };
  }

  Session.reviewLoad = reviewLoad;

  /* Czy dziś przypada wymowa. Liczymy od ostatniego bloku wymowy w sesji,
     a nie od ostatniego wejścia na ekran „Wymowa hasła” — chodzi o rytm sesji.
     Brak historii oznacza „tak”: pierwszy raz wypada od razu. */
  Session.pronDue = function (today) {
    var day = today || U.today();
    var last = U.store.get('session.lastPron', null);
    if (!last) return true;
    return U.daysBetween(last, day) >= PRON_EVERY;
  };

  Session.notePron = function (today) {
    U.store.set('session.lastPron', today || U.today());
  };

  /* Najsłabszy obszar — dwa niezależne spojrzenia.

     `mode` mówi, JAKI rodzaj ćwiczenia idzie źle (ze statystyki pomyłek).
     `category` mówi, JAKIEGO materiału uczący się nie rozumie (z pokrycia).
     Nie są tym samym i nie zastępują się nawzajem: można bezbłędnie układać
     zdania z rozsypanki i nie rozumieć ani słowa w restauracji. */
  Session.weakSpot = function () {
    var out = { kind: null, mode: null, category: null, label: null };

    if (global.Progress && Progress.worstArea) {
      var worst = Progress.worstArea();
      if (worst && worst.suggestion) {
        out.kind = worst.kind;
        out.mode = worst.suggestion.mode;
        out.screen = worst.suggestion.screen;
        out.label = worst.item.key;
        out.rate = worst.item.rate;
      }
    }

    if (global.Coverage && Coverage.ready()) {
      var weak = Coverage.weakest();
      if (weak) {
        out.category = weak.name;
        out.categoryCoverage = weak.coverage;
      }
    }
    return out;
  };

  /* ------------------------------------------------------------- skład */

  /* Udziały bloków w budżecie. Suma zawsze 1 — normalizujemy na końcu,
     żeby żadna korekta nie potrafiła po cichu wydłużyć sesji. */
  function shares(load, weak, pron) {
    var s = { srs: 0.30, lesson: 0.22, listen: 0.22, produce: 0.26 };

    /* Zasada 1: nacisk zaległości podnosi udział powtórek do sufitu. */
    s.srs = 0.30 + (SRS_MAX_SHARE - 0.30) * load.pressure;
    if (!load.due) s.srs = 0;

    /* Zasada 3: dzień wymowy zabiera swój kawałek wszystkim po równo. */
    if (pron) s.pron = 0.16;

    /* Zasada 2: najsłabszy obszar dostaje dołożone 0,10 do bloku, który go
       naprawia. Tryby produkcyjne naprawia blok produkcji, resztę — słuchanie. */
    if (weak && weak.mode) {
      var target = (weak.screen === 'produce') ? 'produce' : 'listen';
      s[target] += 0.10;
    }

    var total = 0;
    Object.keys(s).forEach(function (k) { total += s[k]; });
    Object.keys(s).forEach(function (k) { s[k] = s[k] / total; });
    return s;
  }

  Session.shares = shares;

  /* Tryb ćwiczenia dla bloku słuchania i produkcji.

     Jeśli statystyka wskazuje konkretny tryb jako słaby, bierzemy właśnie ten
     — powtarzanie tego, co wychodzi, nie jest nauką. W przeciwnym razie tryb
     jest wybierany rotacyjnie po dacie, żeby sesje z kolejnych dni nie były
     tym samym ćwiczeniem. */
  var LISTEN_ROTATION = ['choice', 'gap', 'dictation', 'unknown', 'assemble', 'spot'];
  var PRODUCE_ROTATION = ['build', 'type', 'classifier', 'tone'];

  function rotate(list, day) {
    var seed = parseInt(String(day).replace(/-/g, ''), 10) || 0;
    return list[seed % list.length];
  }

  Session.pickMode = function (kind, weak, day) {
    if (weak && weak.mode) {
      if (kind === 'produce' && PRODUCE_ROTATION.indexOf(weak.mode) !== -1) return weak.mode;
      if (kind === 'listen' && LISTEN_ROTATION.indexOf(weak.mode) !== -1) return weak.mode;
    }
    return rotate(kind === 'listen' ? LISTEN_ROTATION : PRODUCE_ROTATION, day);
  };

  /* Podział bloku na kawałki po CHUNK kroków i przeplecenie. Powtórki idą
     pierwsze (zasada 1), potem kawałki reszty na przemian. */
  function interleave(blocks) {
    var pieces = [];
    blocks.forEach(function (b) {
      if (b.steps <= 0) return;
      var left = b.steps;
      var part = 0;
      while (left > 0) {
        var take = Math.min(CHUNK, left);
        pieces.push({
          kind: b.kind, mode: b.mode, label: b.label, why: b.why,
          category: b.category,
          steps: take, part: part, done: 0, correct: 0
        });
        left -= take;
        part += 1;
      }
    });

    /* Grupujemy kawałki po rodzaju, potem zbieramy rundami: po jednym
       kawałku każdego rodzaju. Powtórki zawsze otwierają rundę. */
    var order = ['srs', 'lesson', 'listen', 'produce', 'pron'];
    var byKind = {};
    pieces.forEach(function (p) { (byKind[p.kind] = byKind[p.kind] || []).push(p); });

    var out = [];
    var any = true;
    while (any) {
      any = false;
      order.forEach(function (k) {
        var list = byKind[k];
        if (list && list.length) { out.push(list.shift()); any = true; }
      });
    }
    return out;
  }

  Session.interleave = interleave;

  /* Skład sesji dla zadanej długości. Czysta funkcja stanu — nic nie zapisuje,
     więc ekran może pokazać podgląd składu przed startem, a test może ją
     wywołać dla dowolnego stanu użytkownika. */
  Session.compose = function (minutes, opts) {
    opts = opts || {};
    var day = opts.today || U.today();
    var budget = minutes * 60;
    var load = opts.load || reviewLoad();
    var weak = opts.weak || Session.weakSpot();
    var pron = (opts.pron !== undefined) ? opts.pron : Session.pronDue(day);
    var sh = shares(load, weak, pron);

    var blocks = [];
    Object.keys(sh).forEach(function (kind) {
      var seconds = sh[kind] * budget;
      var steps = Math.round(seconds / SECONDS[kind]);
      if (steps < 1) steps = sh[kind] > 0 ? 1 : 0;
      blocks.push({ kind: kind, steps: steps });
    });

    /* Powtórek nie planujemy więcej, niż faktycznie czeka kart — plan
       powtórek ma własny sufit i sesja nie ma prawa go podnosić. */
    blocks.forEach(function (b) {
      if (b.kind === 'srs') b.steps = Math.min(b.steps, load.due);
    });

    /* Nowe hasła: nie więcej, niż ma najbliższa lekcja. Sesja wprowadza
       lekcję, a nie przerabia kursu na wyrywki. */
    var lesson = (global.Course && Course.next) ? Course.next() : null;
    var lessonWords = lesson ? (lesson.newWordIds || []).length : 0;
    blocks.forEach(function (b) {
      if (b.kind !== 'lesson') return;
      if (!lessonWords) { b.steps = 0; return; }
      b.steps = Math.min(b.steps, lessonWords, NEW_MAX);
      /* Przy zaległej kolejce nowe hasła schodzą jeszcze niżej: dokładanie
         materiału do kartoteki, która i tak się nie mieści, pogłębia problem
         zamiast go rozwiązywać. */
      if (load.pressure >= 1) b.steps = Math.min(b.steps, 3);
    });

    /* Czas uwolniony przez powyższe sufity wraca do sesji, a nie przepada —
       inaczej dzień bez zaległości dawałby sesję o połowę krótszą, niż
       uczący się zamówił. Oddajemy go blokom, które nie mają sufitu. */
    var used = 0;
    blocks.forEach(function (b) { used += b.steps * SECONDS[b.kind]; });
    var spare = budget - used;
    if (spare > SECONDS.produce) {
      var open = blocks.filter(function (b) {
        return (b.kind === 'listen' || b.kind === 'produce') && b.steps > 0;
      });
      if (open.length) {
        var each = spare / open.length;
        open.forEach(function (b) { b.steps += Math.floor(each / SECONDS[b.kind]); });
      }
    }

    blocks.forEach(function (b) {
      b.label = LABELS[b.kind];
      if (b.kind === 'listen' || b.kind === 'produce') b.mode = Session.pickMode(b.kind, weak, day);
      if (b.kind === 'pron') b.mode = 'say';
      if (b.kind === 'lesson' && lesson) b.lessonId = lesson.id;
      b.why = whyBlock(b.kind, load, weak, pron);
      if (weak && weak.category && (b.kind === 'listen')) b.category = weak.category;
    });

    var pieces = interleave(blocks.filter(function (b) { return b.steps > 0; }));
    /* Identyfikator lekcji przenosimy na kawałki — po przeplocie kawałek musi
       wiedzieć sam, co ma pokazać. */
    pieces.forEach(function (p) {
      if (p.kind === 'lesson' && lesson) p.lessonId = lesson.id;
    });

    var seconds = 0;
    pieces.forEach(function (p) { seconds += p.steps * SECONDS[p.kind]; });

    return {
      minutes: minutes,
      blocks: pieces,
      steps: pieces.reduce(function (n, p) { return n + p.steps; }, 0),
      estimate: seconds,
      pron: pron,
      weak: weak,
      load: load,
      lessonId: lesson ? lesson.id : null
    };
  };

  /* Jednozdaniowe uzasadnienie bloku. Uczący się ma widzieć, dlaczego dostał
     akurat to — inaczej „zaplanowana sesja” jest nieodróżnialna od losowania. */
  function whyBlock(kind, load, weak, pron) {
    if (kind === 'srs') {
      if (load.dueTotal > load.cap) {
        return 'Masz ' + load.dueTotal + ' zaległych kart. Zaczynamy od nich — hasło zapomniane to nauka od zera.';
      }
      return 'Karty na dziś. Powtórka w terminie kosztuje kilka sekund, powtórka po terminie — całą naukę hasła.';
    }
    if (kind === 'lesson') return 'Nowe hasła z najbliższej lekcji kursu.';
    if (kind === 'pron') return 'Wymowa wraca co ' + PRON_EVERY + ' dni — na tyle rzadko, żeby dało się ją zrobić w ciszy.';
    if (kind === 'listen') {
      if (weak && weak.category) return 'Słuchanie. Najsłabsze pokrycie masz w kategorii „' + weak.category + '”.';
      return 'Słuchanie — jedyne ćwiczenie, które trenuje to, po co uczysz się języka.';
    }
    if (kind === 'produce') {
      if (weak && weak.kind === 'mode') return 'Wytwarzanie. Ten tryb ma u Ciebie najwyższy odsetek pomyłek.';
      return 'Wytwarzanie. Rozpoznać zdanie umie każdy, kto je widział — powiedzieć je umie ktoś inny.';
    }
    return '';
  }

  /* ------------------------------------------------------------- bieg */

  Session.start = function (minutes, opts) {
    var plan = Session.compose(minutes, opts);
    Session.state = {
      date: (opts && opts.today) || U.today(),
      minutes: minutes,
      blocks: plan.blocks,
      at: 0,
      elapsed: 0,          // sekundy faktycznie spędzone w sesji
      answers: 0,
      correct: 0,
      startedAt: Date.now(),
      resumedAt: Date.now(),
      finished: false,
      estimate: plan.estimate,
      lessonId: plan.lessonId,
      weak: plan.weak
    };
    if (plan.pron) Session.notePron(Session.state.date);
    Session.save();
    return Session.state;
  };

  /* Wznowienie: zegar rusza od nowa, ale zużyty czas zostaje. */
  Session.resume = function () {
    if (!Session.state) return null;
    Session.state.resumedAt = Date.now();
    Session.save();
    return Session.state;
  };

  /* Odłożenie sesji. Nie kasuje niczego — dopisuje tylko zużyty czas, żeby
     przerwa między krokami nie liczyła się jako nauka. */
  Session.pause = function () {
    var s = Session.state;
    if (!s || s.finished) return;
    if (s.resumedAt) {
      s.elapsed += Math.round((Date.now() - s.resumedAt) / 1000);
      s.resumedAt = null;
    }
    Session.save();
  };

  Session.tick = function () {
    var s = Session.state;
    if (!s || s.finished || !s.resumedAt) return;
    s.elapsed += Math.round((Date.now() - s.resumedAt) / 1000);
    s.resumedAt = Date.now();
    Session.save();
  };

  Session.current = function () {
    var s = Session.state;
    if (!s || s.finished) return null;
    return s.blocks[s.at] || null;
  };

  Session.progress = function () {
    var s = Session.state;
    if (!s) return null;
    var total = 0, done = 0;
    s.blocks.forEach(function (b) { total += b.steps; done += b.done; });
    var spent = s.elapsed + (s.resumedAt ? Math.round((Date.now() - s.resumedAt) / 1000) : 0);
    return {
      steps: total,
      done: done,
      share: total ? done / total : 0,
      spent: spent,
      budget: s.minutes * 60,
      left: Math.max(0, s.minutes * 60 - spent),
      overtime: spent > s.minutes * 60,
      answers: s.answers,
      correct: s.correct,
      finished: !!s.finished
    };
  };

  /* Jeden krok zaliczony. `ok` bywa null przy krokach, które nie są pytaniem
     (wprowadzenie nowego hasła) — wtedy nie liczą się do skuteczności. */
  Session.step = function (ok) {
    var s = Session.state;
    if (!s || s.finished) return null;
    var block = s.blocks[s.at];
    if (!block) { Session.finish(); return null; }

    block.done += 1;
    if (ok === true) { block.correct += 1; s.answers += 1; s.correct += 1; }
    else if (ok === false) { s.answers += 1; }

    Session.tick();

    if (block.done >= block.steps) {
      s.at += 1;
      if (s.at >= s.blocks.length) Session.finish();
    }
    Session.save();
    return Session.current();
  };

  /* Pominięcie całego bloku — sesja ma być planem, nie przymusem. Kroki
     pominięte zostają policzone jako niezrobione, żeby podsumowanie tygodnia
     widziało prawdę. */
  Session.skipBlock = function () {
    var s = Session.state;
    if (!s || s.finished) return null;
    var block = s.blocks[s.at];
    if (block) block.skipped = true;
    s.at += 1;
    if (s.at >= s.blocks.length) Session.finish();
    Session.save();
    return Session.current();
  };

  Session.finish = function () {
    var s = Session.state;
    if (!s || s.finished) return;
    Session.pause();
    s.finished = true;
    s.finishedAt = Date.now();
    Session.save();
    Session.archive(s);
  };

  /* --------------------------------------------------------- dziennik */

  /* Skrócony zapis zakończonych sesji — materiał dla retrospekcji tygodnia.
     Trzymamy same liczby, bez treści zadań; sześćdziesiąt wpisów to około
     dwóch miesięcy i kilka kilobajtów. */
  var LOG_LIMIT = 60;

  Session.archive = function (s) {
    var log = U.store.get('session.log', []) || [];
    var byKind = {};
    s.blocks.forEach(function (b) {
      var e = byKind[b.kind] || (byKind[b.kind] = { steps: 0, done: 0, correct: 0 });
      e.steps += b.steps;
      e.done += b.done;
      e.correct += b.correct;
    });
    log.push({
      d: s.date,
      minutes: s.minutes,
      spent: s.elapsed,
      answers: s.answers,
      correct: s.correct,
      blocks: byKind
    });
    if (log.length > LOG_LIMIT) log = log.slice(-LOG_LIMIT);
    U.store.set('session.log', log);
  };

  Session.log = function () { return U.store.get('session.log', []) || []; };

  global.Session = Session;
})(window);
