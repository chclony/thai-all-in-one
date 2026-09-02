/* Thai All-in-One — kurs.

   Baza jest kompletna, ale zbiór 10 000 rekordów to jeszcze nie kurs.
   Ten moduł zamienia go w ścieżkę: 132 lekcje w kolejności dydaktycznej,
   z mapą postępu i blokadą kolejnych lekcji do czasu zaliczenia poprzedniej.

   Blokada nie jest karą. Ścieżka jest zbudowana tak, że żadna lekcja nie
   wprowadza słowa, którego nie da się użyć w zdaniu z materiału wcześniejszego
   (pilnuje tego generator tools/generators/lessons.py). Przeskoczenie lekcji
   oznaczałoby zdania z lukami. Dlatego lekcja otwiera się dopiero po zaliczeniu
   poprzedniej — ale każdą można świadomie pominąć, jeśli materiał jest już
   znany, i test poziomujący robi to automatycznie dla całych poziomów.

   Zaliczenie: sprawdzian z haseł lekcji, w trybach produkcyjnych, z progiem
   80% trafnych odpowiedzi (kryterium zapisane w samej lekcji). */
(function (global) {
  'use strict';

  var Course = { current: null, run: null };

  var LEVELS = ['Survival', 'A1', 'A2', 'B1', 'B2'];

  Course.lessons = function () { return DB.lessons || []; };

  Course.byId = function (id) {
    var list = Course.lessons();
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === id) return list[i];
    }
    return null;
  };

  /* Przed lekcją 1 stoi Moduł 0 — trening słuchu. Ta kolejność nie jest
     kaprysem: uczący się, który nie słyszy różnicy między khǎaw a khàaw,
     zapisze w pamięci oba wyrazy bez tonu, a każda następna lekcja ten zapis
     utrwali. Moduł da się pominąć świadomie i test poziomujący powyżej A1
     zwalnia z niego automatycznie — ale domyślnie jest obowiązkowy. */
  Course.moduleZeroBlocks = function () {
    if (!global.Perception || !Perception.ready()) return false;
    return !Perception.gateOpen();
  };

  /* Lekcja jest otwarta, gdy jest pierwsza albo gdy poprzednia jest zaliczona
     lub świadomie pominięta. */
  Course.isUnlocked = function (lesson) {
    var list = Course.lessons();
    var idx = list.indexOf(lesson);
    if (idx <= 0) return !Course.moduleZeroBlocks();
    return Progress.isLessonDone(list[idx - 1].id) && !Course.moduleZeroBlocks();
  };

  Course.status = function (lesson) {
    var st = Progress.lessonState(lesson.id);
    if (st && st.status === 'passed') return 'passed';
    if (st && st.status === 'skipped') return 'skipped';
    return Course.isUnlocked(lesson) ? 'open' : 'locked';
  };

  /* Pierwsza lekcja, która czeka na zrobienie. */
  Course.next = function () {
    var list = Course.lessons();
    for (var i = 0; i < list.length; i++) {
      if (!Progress.isLessonDone(list[i].id)) return list[i];
    }
    return null;
  };

  Course.summary = function () {
    var list = Course.lessons();
    var passed = 0, skipped = 0;
    list.forEach(function (L) {
      var st = Progress.lessonState(L.id);
      if (!st) return;
      if (st.status === 'passed') passed += 1;
      else if (st.status === 'skipped') skipped += 1;
    });
    return {
      total: list.length,
      passed: passed,
      skipped: skipped,
      done: passed + skipped,
      percent: list.length ? Math.round((passed + skipped) / list.length * 100) : 0
    };
  };

  Course.byLevel = function () {
    var out = {};
    LEVELS.forEach(function (l) { out[l] = { total: 0, done: 0 }; });
    Course.lessons().forEach(function (L) {
      if (!out[L.level]) out[L.level] = { total: 0, done: 0 };
      out[L.level].total += 1;
      if (Progress.isLessonDone(L.id)) out[L.level].done += 1;
    });
    return out;
  };

  /* Materiał lekcji — pełne rekordy. Wymaga dociągnięcia plików, w których
     leżą hasła tej lekcji (zwykle jeden albo dwa). */
  Course.load = function (lesson) {
    var ids = lesson.recordIds.slice();
    if (lesson.dialogueId) ids.push(lesson.dialogueId);
    return DB.ensureFor(ids).then(function () {
      return {
        lesson: lesson,
        records: lesson.recordIds.map(function (id) { return DB.get(id); }).filter(Boolean),
        newWords: lesson.newWordIds.map(function (id) { return DB.get(id); }).filter(Boolean),
        grammar: (DB.grammar || []).filter(function (g) { return g.id === lesson.grammarId; })[0] || null,
        dialogue: lesson.dialogueId ? DB.get(lesson.dialogueId) : null
      };
    });
  };

  /* ------------------------------------------------------------ sprawdzian */

  /* Sprawdzian sprawdza produkcję, nie rozpoznawanie. Hasła pojedyncze idą
     do wpisywania z pamięci, dłuższe wypowiedzi do układania z rozsypanki. */
  Course.buildTest = function (material) {
    var items = U.shuffle(material.records).map(function (rec) {
      var w = (rec.thaiPhonetic || '').split(/\s+/).filter(Boolean);
      return { rec: rec, kind: w.length >= 2 && w.length <= 7 ? 'build' : 'type' };
    });
    return items;
  };

  Course.startTest = function (material) {
    Course.run = {
      lesson: material.lesson,
      items: Course.buildTest(material),
      at: 0,
      correct: 0,
      wrongIds: []
    };
    return Course.run;
  };

  Course.recordAnswer = function (ok, id) {
    var run = Course.run;
    if (!run) return;
    if (ok) run.correct += 1;
    else run.wrongIds.push(id);
    run.at += 1;
  };

  Course.testDone = function () {
    var run = Course.run;
    return !run || run.at >= run.items.length;
  };

  /* Zaliczenie liczymy według kryterium zapisanego w lekcji. */
  Course.finishTest = function () {
    var run = Course.run;
    var need = run.lesson.pass.required;
    var passed = run.correct >= need;
    if (passed) {
      Progress.setLessonResult(run.lesson.id, 'passed', run.correct, run.items.length);
    }
    /* Pomyłki trafiają do powtórek — to najkrótsza droga od błędu do naprawy. */
    run.wrongIds.forEach(function (id) { SRS.addBoth(id); });
    return {
      passed: passed,
      correct: run.correct,
      total: run.items.length,
      required: need,
      wrongIds: run.wrongIds.slice()
    };
  };

  Course.skip = function (lesson) {
    Progress.setLessonResult(lesson.id, 'skipped', 0, 0);
  };

  Course.reset = function (lesson) {
    delete Progress.data.lessons[lesson.id];
    Progress.save();
  };


  /* ===================================================== ROZDZIAŁY I TEMPO

     Ścieżka ma 333 lekcje. Lista tej długości bez podziału jest ścianą,
     po której nie widać, gdzie się jest ani ile zostało. Trzy rzeczy, które
     to naprawiają, liczy poniższy kod:

       1. ROZDZIAŁY — kilkanaście lekcji o wspólnym temacie, wyznaczone przez
          generator (pole `chapters` w lessons.json) i łamane na granicach
          poziomu. Uczący się widzi „rozdział 7 z 26”, a nie „lekcja 92 z 333”.
       2. KAMIENIE MILOWE — co daje ukończenie rozdziału: ile haseł wchodzi
          do czynnego użycia i co otwiera się dalej.
       3. TEMPO — ile lekcji na tydzień robi się naprawdę i kiedy przy tym
          tempie kończy się bieżący poziom oraz cały kurs.
  */

  Course.chapters = function () { return (global.DB && DB.chapters) || []; };

  Course.chapterOf = function (lesson) {
    var list = Course.chapters();
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === lesson.chapterId) return list[i];
    }
    return null;
  };

  Course.chapterState = function (ch) {
    var ids = ch.lessonIds || [];
    var done = 0;
    for (var i = 0; i < ids.length; i++) {
      if (Progress.isLessonDone(ids[i])) done += 1;
    }
    return {
      done: done,
      total: ids.length,
      percent: ids.length ? Math.round(done / ids.length * 100) : 0,
      complete: ids.length > 0 && done === ids.length,
      started: done > 0
    };
  };

  /* Rozdział, w którym uczący się właśnie jest: pierwszy niedokończony. */
  Course.currentChapter = function () {
    var list = Course.chapters();
    for (var i = 0; i < list.length; i++) {
      if (!Course.chapterState(list[i]).complete) return list[i];
    }
    return list.length ? list[list.length - 1] : null;
  };

  /* Co otwiera ukończenie rozdziału. Sam opis z danych mówi, co się umie;
     tutaj dokładamy, co się pojawia dalej — bo to jest ta część, która
     ciągnie do przodu. */
  Course.milestone = function (ch) {
    var list = Course.chapters();
    var idx = -1;
    for (var i = 0; i < list.length; i++) if (list[i].id === ch.id) idx = i;
    var nextCh = idx >= 0 && idx + 1 < list.length ? list[idx + 1] : null;
    var parts = [ch.milestone];
    if (!nextCh) {
      parts.push('To ostatni rozdział kursu — dalej zostają powtórki i ćwiczenia produkcyjne, które nie mają końca.');
    } else if (nextCh.level !== ch.level) {
      parts.push('Ukończenie zamyka poziom ' + ch.level + ' i otwiera ' + nextCh.level +
                 ' — rozdział „' + nextCh.title + '”.');
    } else {
      parts.push('Ukończenie otwiera rozdział ' + nextCh.number + ': „' + nextCh.title +
                 '” (' + nextCh.lessons + ' ' + U.plural(nextCh.lessons, 'lekcja', 'lekcje', 'lekcji') +
                 ', ' + nextCh.newWords + ' nowych haseł).');
    }
    return parts.join(' ');
  };

  /* ------------------------------------------------------------- tempo */

  var PACE_WINDOW = 28;   // dni wstecz, z których liczymy tempo

  /* Daty zaliczeń lekcji. Wpisy pochodzące z migracji są POMIJANE:
     wszystkie mają jedną datę i policzone jako nauka dałyby tempo rzędu
     stu lekcji dziennie, a po nim prognozę „koniec kursu jutro”. */
  function realDates() {
    var out = [];
    var st = Progress.data.lessons || {};
    Object.keys(st).forEach(function (id) {
      var s = st[id];
      if (!s || !s.date) return;
      if (s.source && s.source.indexOf('migracja') === 0) return;
      out.push(s.date);
    });
    return out;
  }

  Course.pace = function () {
    var list = Course.lessons();
    var sum = Course.summary();
    var remainingTotal = Math.max(0, list.length - sum.done);

    var level = Progress.entryLevel();
    var cur = Course.next();
    if (cur) level = cur.level;
    var remainingLevel = 0;
    list.forEach(function (L) {
      if (L.level === level && !Progress.isLessonDone(L.id)) remainingLevel += 1;
    });

    var dates = realDates();
    var today = U.today();
    var byDay = {}, inWindow = 0;
    dates.forEach(function (d) {
      var age = U.daysBetween(d, today);
      if (age < 0 || age > PACE_WINDOW) return;
      byDay[d] = (byDay[d] || 0) + 1;
      inWindow += 1;
    });
    var activeDays = Object.keys(byDay).length;

    var out = {
      level: level,
      remainingLevel: remainingLevel,
      remainingTotal: remainingTotal,
      done: sum.done,
      total: list.length,
      activeDays: activeDays,
      lessonsInWindow: inWindow,
      known: false
    };

    /* Poniżej trzech dni z aktywnością prognoza byłaby zgadywanką —
       jeden intensywny wieczór dałby „kurs w dwa tygodnie”. Mówimy wprost,
       że jeszcze nie wiadomo, zamiast podawać liczbę bez pokrycia. */
    if (activeDays < 3 || !inWindow) return out;

    var perActiveDay = inWindow / activeDays;
    var daysPerWeek = Math.min(7, activeDays / (PACE_WINDOW / 7));
    var perWeek = perActiveDay * daysPerWeek;
    if (perWeek <= 0) return out;

    out.known = true;
    out.perActiveDay = perActiveDay;
    out.perWeek = perWeek;
    out.weeksLevel = remainingLevel / perWeek;
    out.weeksTotal = remainingTotal / perWeek;
    out.dateLevel = U.addDays(today, Math.ceil(out.weeksLevel * 7));
    out.dateTotal = U.addDays(today, Math.ceil(out.weeksTotal * 7));
    return out;
  };

  global.Course = Course;
})(window);
