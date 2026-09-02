/* Thai All-in-One — test poziomujący.

   Problem, który rozwiązuje: baza ma ponad 10 000 haseł i 132 lekcje.
   Bez punktu wejścia uczący się albo zaczyna od zera, mimo że zna podstawy,
   albo trafia od razu na materiał, którego nie rozumie, i rezygnuje.

   Test ma 28 pytań o rosnącej trudności: od Survival do B2, po kilka pytań na
   poziom. Kończy się wcześniej, gdy uczący się wyraźnie przestaje nadążać —
   trzy pomyłki z rzędu na jednym poziomie oznaczają, że wyżej nie ma sensu
   pytać. To skraca test tym, którzy zaczynają od zera, a nie odbiera pełnego
   przebiegu tym, którzy coś już umieją.

   Pytania budujemy z lekkiego indeksu, więc test rusza natychmiast po starcie
   aplikacji — bez czekania na pliki poziomów. Dźwięk i przykłady dociągają się
   w tle, w miarę jak są potrzebne.

   Wynik zapisujemy w postępie (Progress.setPlacement) i używamy do:
     - wyznaczenia lekcji, od której otwiera się kurs,
     - doboru materiału w Powtórkach i ćwiczeniach (poziom nauki). */
(function (global) {
  'use strict';

  var Placement = { state: null };

  var LEVELS = ['Survival', 'A1', 'A2', 'B1', 'B2'];

  /* Ile pytań na poziom — razem 28. Niższe poziomy dostają więcej pytań,
     bo to tam rozstrzyga się większość wyników. */
  var PER_LEVEL = { Survival: 6, A1: 6, A2: 6, B1: 5, B2: 5 };

  var STOP_AFTER_WRONG = 3;   // tyle pomyłek z rzędu kończy test

  function hideTones() { return !!U.store.get('settings', {}).hideTones; }

  /* Kandydaci na pytanie: hasła częste i jednoznaczne. Zdania odpadają —
     w teście chodzi o rozpoznanie znaczenia, nie o czytanie ze zrozumieniem. */
  function candidates(level) {
    return DB.index.filter(function (r) {
      return r.level === level && r.frequency >= 3 && r.polish && r.thaiPhonetic
        && U.syllables(r.thaiPhonetic).length <= 6;
    });
  }

  /* Dystraktory z tego samego poziomu i w miarę możliwości tej samej
     kategorii — inaczej odpowiedź da się zgadnąć samym tematem. */
  function distractors(rec, all, n) {
    var same = all.filter(function (r) {
      return r.id !== rec.id && r.category === rec.category && r.polish !== rec.polish;
    });
    var rest = all.filter(function (r) {
      return r.id !== rec.id && r.category !== rec.category && r.polish !== rec.polish;
    });
    var pick = U.sample(same, n);
    if (pick.length < n) pick = pick.concat(U.sample(rest, n - pick.length));
    return pick;
  }

  Placement.build = function () {
    var questions = [];
    LEVELS.forEach(function (level) {
      var all = candidates(level);
      if (all.length < 5) return;
      U.sample(all, PER_LEVEL[level] || 5).forEach(function (rec) {
        var opts = distractors(rec, all, 3);
        if (opts.length < 3) return;
        questions.push({
          level: level,
          id: rec.id,
          prompt: rec.thaiPhonetic,
          answer: rec.polish,
          options: U.shuffle(opts.concat([rec])).map(function (r) { return r.polish; })
        });
      });
    });
    return questions;
  };

  Placement.start = function () {
    Placement.state = {
      questions: Placement.build(),
      at: 0,
      correct: 0,
      byLevel: {},
      streakWrong: 0,
      done: false
    };
    LEVELS.forEach(function (l) { Placement.state.byLevel[l] = { asked: 0, correct: 0 }; });
    return Placement.state;
  };

  /* Poziom wyniku: najwyższy, na którym uczący się utrzymał 60% trafień.
     Próg jest celowo niski — test ma znaleźć punkt startu, a nie certyfikować.
     Lepiej posadzić kogoś odrobinę za nisko (pierwsze lekcje pójdą szybko)
     niż za wysoko (materiał bez podstaw zniechęca). */
  function verdict(state) {
    var reached = 'Survival';
    LEVELS.forEach(function (l) {
      var b = state.byLevel[l];
      if (b.asked >= 3 && b.correct / b.asked >= 0.6) reached = l;
    });
    var total = 0;
    LEVELS.forEach(function (l) { total += state.byLevel[l].asked; });
    return { level: reached, score: state.correct, total: total };
  }

  /* Pierwsza nieukończona lekcja na wyznaczonym poziomie. Lekcje niższych
     poziomów zostają odblokowane jako „zaliczone testem” — uczący się może do
     nich wrócić, ale nie musi ich przechodzić, żeby ruszyć dalej. */
  function entryLesson(level) {
    var lessons = DB.lessons || [];
    var idx = LEVELS.indexOf(level);
    for (var i = 0; i < lessons.length; i++) {
      if (LEVELS.indexOf(lessons[i].level) >= idx) return lessons[i];
    }
    return lessons[0] || null;
  }

  Placement.finish = function () {
    var state = Placement.state;
    state.done = true;
    var v = verdict(state);
    var entry = entryLesson(v.level);

    /* Lekcje poniżej punktu wejścia oznaczamy jako zaliczone testem — inaczej
       blokada trzymałaby uczącego się na materiale, który właśnie zdał. */
    if (entry) {
      (DB.lessons || []).forEach(function (L) {
        if (L.number < entry.number && !Progress.isLessonDone(L.id)) {
          Progress.setLessonResult(L.id, 'skipped', 0, 0);
        }
      });
    }

    Progress.setPlacement({
      level: v.level, score: v.score, total: v.total,
      entryLesson: entry ? entry.id : null
    });

    /* Wynik powyżej A1 zwalnia z obowiązkowego Modułu 0. Kto rozumie zdania
       na poziomie A2, ten kontrasty słyszy — inaczej by ich nie rozumiał.
       Moduł zostaje na mapie jako opcjonalny, bo trening percepcyjny przydaje
       się także wyżej, ale przestaje blokować wejście w lekcję 1. */
    if (['A2', 'B1', 'B2'].indexOf(v.level) !== -1) {
      var perc = Progress.perception();
      perc.optional = true;
      perc.optionalFrom = v.level;
      Progress.save();
    }

    /* Poziom nauki ustawiamy tylko wtedy, gdy użytkownik nie wybrał własnego. */
    var s = U.store.get('settings', {});
    if (!s.practiceLevel) {
      s.practiceLevel = v.level;
      U.store.set('settings', s);
      if (global.App && App.settings) App.settings.practiceLevel = v.level;
    }
    return { verdict: v, entry: entry };
  };

  Placement.answer = function (question, chosen) {
    var state = Placement.state;
    var ok = chosen === question.answer;
    var b = state.byLevel[question.level];
    b.asked += 1;
    if (ok) { b.correct += 1; state.correct += 1; state.streakWrong = 0; }
    else state.streakWrong += 1;
    Progress.answer(question.id, ok, { mode: 'placement' });
    state.at += 1;
    return ok;
  };

  /* Czy kończymy wcześniej: trzy pomyłki z rzędu i mamy już czym ocenić. */
  Placement.shouldStop = function () {
    var state = Placement.state;
    if (state.at >= state.questions.length) return true;
    return state.streakWrong >= STOP_AFTER_WRONG && state.at >= 6;
  };

  Placement.current = function () {
    var state = Placement.state;
    return state && state.at < state.questions.length ? state.questions[state.at] : null;
  };

  Placement.progressText = function () {
    var state = Placement.state;
    return 'Pytanie ' + Math.min(state.at + 1, state.questions.length)
      + ' z ' + state.questions.length;
  };

  Placement.hideTones = hideTones;

  global.Placement = Placement;
})(window);
