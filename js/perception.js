/* Thai All-in-One — Moduł 0: trening percepcyjny.

   Do sesji J kurs zaczynał się od słów, a materiał o dźwiękach leżał na ekranie
   „Wymowa i tony”, schowanym pod przyciskiem „Więcej”. To była zła kolejność.

   Polak nie ma w systemie fonologicznym ani tonu leksykalnego, ani kontrastu
   długości samogłoski, ani opozycji przydechowej. Dopóki nie usłyszy różnicy
   między khǎaw a khàaw, zapisuje oba wyrazy w pamięci jako „khaaw” — czyli
   błędnie. Każda następna lekcja utrwala ten zapis, a poprawianie utrwalonego
   błędu jest droższe niż nauczenie się od razu dobrze. Dlatego trening słuchu
   idzie PRZED lekcją 1, a nie obok niej.

   Moduł jest domyślnie obowiązkowy: lekcja 1 kursu otwiera się dopiero, gdy
   Moduł 0 jest zaliczony, pominięty świadomie albo zwolniony testem
   poziomującym powyżej A1.

   Ten plik trzyma wyłącznie logikę. Rysowaniem zajmuje się app.js. */
(function (global) {
  'use strict';

  var P = { run: null, diag: null };

  function data() { return DB.moduleZero || null; }

  P.ready = function () { return !!data(); };
  P.info = function () { return data(); };

  P.lessons = function () { return (data() && data().lessons) || []; };
  P.contrasts = function () { return (data() && data().contrasts) || []; };
  P.families = function () { return (data() && data().families) || []; };
  P.taskTypes = function () { return (data() && data().taskTypes) || []; };
  P.diagnostic = function () { return data() && data().diagnostic; };

  P.byId = function (id) {
    var list = P.lessons();
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  };

  P.contrast = function (cid) {
    var list = P.contrasts();
    for (var i = 0; i < list.length; i++) if (list[i].id === cid) return list[i];
    return null;
  };

  P.contrastLabel = function (cid) {
    var c = P.contrast(cid);
    return c ? c.label : cid;
  };

  /* Bodźce trzymamy w mapie — zadania odwołują się do nich po identyfikatorze,
     żeby ten sam wyraz nie powtarzał się w pliku kilkadziesiąt razy. */
  var stimMap = null;
  function stims() {
    if (!stimMap) {
      stimMap = {};
      ((data() && data().stimuli) || []).forEach(function (s) { stimMap[s.id] = s; });
    }
    return stimMap;
  }
  P.stimulus = function (id) { return stims()[id] || null; };
  P.resetCache = function () { stimMap = null; };

  /* ------------------------------------------------------------- stan modułu */

  function store() { return Progress.perception(); }

  P.lessonState = function (id) { return store().lessons[id] || null; };

  P.isLessonDone = function (id) {
    var st = store().lessons[id];
    return !!(st && (st.status === 'passed' || st.status === 'skipped'
      || st.status === 'diagnosed'));
  };

  /* Lekcja otwiera się po zaliczeniu poprzedniej. Pierwsza jest otwarta zawsze —
     bez niej moduł nie miałby od czego zacząć. */
  P.isUnlocked = function (lesson) {
    var list = P.lessons();
    var idx = list.indexOf(lesson);
    if (idx <= 0) return true;
    return P.isLessonDone(list[idx - 1].id);
  };

  P.status = function (lesson) {
    var st = P.lessonState(lesson.id);
    if (st && st.status === 'passed') return 'passed';
    if (st && st.status === 'diagnosed') return 'diagnosed';
    if (st && st.status === 'skipped') return 'skipped';
    return P.isUnlocked(lesson) ? 'open' : 'locked';
  };

  P.next = function () {
    var list = P.lessons();
    for (var i = 0; i < list.length; i++) {
      if (!P.isLessonDone(list[i].id)) return list[i];
    }
    return null;
  };

  P.summary = function () {
    var list = P.lessons();
    var passed = 0, skipped = 0, diagnosed = 0;
    list.forEach(function (L) {
      var st = store().lessons[L.id];
      if (!st) return;
      if (st.status === 'passed') passed += 1;
      else if (st.status === 'diagnosed') diagnosed += 1;
      else if (st.status === 'skipped') skipped += 1;
    });
    var done = passed + skipped + diagnosed;
    return {
      total: list.length, passed: passed, skipped: skipped,
      diagnosed: diagnosed, done: done,
      percent: list.length ? Math.round(done / list.length * 100) : 0,
      tasks: list.reduce(function (n, L) { return n + L.tasks.length; }, 0)
    };
  };

  /* ------------------------------------------- obowiązkowość i furtka do kursu */

  /* Moduł jest opcjonalny, gdy test poziomujący posadził uczącego się powyżej
     A1. Ktoś, kto rozumie zdania na poziomie A2, kontrasty słyszy — inaczej by
     ich nie rozumiał. Nie ma powodu trzymać go na ćwiczeniach z pięciu tonów. */
  P.isOptional = function () {
    if (store().optional) return true;
    var p = Progress.data.placement;
    if (!p) return false;
    return ['A2', 'B1', 'B2'].indexOf(p.level) !== -1;
  };

  P.isSkipped = function () { return !!store().skipped; };

  P.allDone = function () {
    var list = P.lessons();
    if (!list.length) return true;
    return list.every(function (L) { return P.isLessonDone(L.id); });
  };

  /* Warunek otwarcia lekcji 1 kursu. */
  P.gateOpen = function () {
    if (!P.ready()) return true;          // brak danych modułu nie może blokować kursu
    if (P.isSkipped()) return true;
    if (P.isOptional()) return true;
    return P.allDone();
  };

  P.skipModule = function () {
    var s = store();
    s.skipped = true;
    s.skippedAt = U.today();
    Progress.save();
  };

  P.unskipModule = function () {
    var s = store();
    delete s.skipped;
    delete s.skippedAt;
    Progress.save();
  };

  P.setLessonResult = function (id, status, score, total) {
    store().lessons[id] = {
      status: status, score: score || 0, total: total || 0, date: U.today()
    };
    Progress.save();
  };

  P.resetLesson = function (id) {
    delete store().lessons[id];
    Progress.save();
  };

  /* ------------------------------------------------------------------ lekcja */

  P.start = function (lesson) {
    P.run = {
      lesson: lesson,
      tasks: U.shuffle(lesson.tasks),
      at: 0,
      correct: 0,
      wrong: []
    };
    return P.run;
  };

  P.current = function () {
    var r = P.run;
    return r && r.at < r.tasks.length ? r.tasks[r.at] : null;
  };

  P.done = function () {
    var r = P.run;
    return !r || r.at >= r.tasks.length;
  };

  /* Zwraca { ok, answer, explain } — bez efektów ubocznych na interfejsie. */
  P.answer = function (task, choice) {
    var ok = choice === task.answer;
    var r = P.run;
    if (r) {
      if (ok) r.correct += 1;
      else r.wrong.push(task);
      r.at += 1;
    }
    Progress.perceptionAnswer(task.contrastId, ok);
    return { ok: ok, answer: task.answer, explain: task.explain || '' };
  };

  P.finish = function () {
    var r = P.run;
    var need = r.lesson.pass.required;
    var passed = r.correct >= need;
    if (passed) {
      P.setLessonResult(r.lesson.id, 'passed', r.correct, r.tasks.length);
    }
    /* Kontrasty, na których poszło źle, wracają w powtórkach jako osobny typ
       karty — inaczej pomyłka zostaje bez konsekwencji i nic jej nie naprawi. */
    var weak = {};
    r.wrong.forEach(function (t) { weak[t.contrastId] = true; });
    var added = Object.keys(weak);
    added.forEach(function (cid) { SRS.addContrast(cid); });
    return {
      passed: passed, correct: r.correct, total: r.tasks.length,
      required: need, weakContrasts: added
    };
  };

  /* ---------------------------------------------------------------- diagnoza */

  P.startDiagnostic = function () {
    var d = P.diagnostic();
    P.diag = {
      tasks: d ? U.shuffle(d.tasks) : [],
      at: 0, correct: 0,
      byFamily: {},
      byContrast: {},
      done: false
    };
    P.families().forEach(function (f) {
      P.diag.byFamily[f.id] = { asked: 0, correct: 0 };
    });
    return P.diag;
  };

  P.currentDiagnostic = function () {
    var d = P.diag;
    return d && d.at < d.tasks.length ? d.tasks[d.at] : null;
  };

  P.answerDiagnostic = function (task, choice) {
    var d = P.diag;
    var ok = choice === task.answer;
    var fam = d.byFamily[task.family] || (d.byFamily[task.family] = { asked: 0, correct: 0 });
    fam.asked += 1;
    if (ok) { fam.correct += 1; d.correct += 1; }
    var c = d.byContrast[task.contrastId]
      || (d.byContrast[task.contrastId] = { asked: 0, correct: 0 });
    c.asked += 1;
    if (ok) c.correct += 1;
    Progress.perceptionAnswer(task.contrastId, ok);
    d.at += 1;
    return { ok: ok, answer: task.answer, explain: task.explain || '' };
  };

  P.diagnosticDone = function () {
    var d = P.diag;
    return !d || d.at >= d.tasks.length;
  };

  /* Rodzina liczy się jako opanowana przy komplecie trafnych odpowiedzi.
     Przy dwóch–trzech zadaniach na rodzinę to próg umowny, więc lekcje
     zwolnione diagnozą zostają dostępne — można je zrobić mimo wszystko. */
  P.finishDiagnostic = function () {
    var d = P.diag;
    d.done = true;
    var mastered = [], weak = [];
    Object.keys(d.byFamily).forEach(function (f) {
      var b = d.byFamily[f];
      if (!b.asked) return;
      if (b.correct === b.asked) mastered.push(f);
      else weak.push(f);
    });

    /* Lekcje, których wszystkie rodziny kontrastów są opanowane, oznaczamy jako
       zdane diagnozą. Uczący się nie musi przechodzić treningu czegoś, co już
       słyszy — to najszybszy sposób na stratę zaufania do kursu. */
    var freed = [];
    P.lessons().forEach(function (L) {
      var fams = L.families || [];
      if (!fams.length) return;
      var all = fams.every(function (f) { return mastered.indexOf(f) !== -1; });
      if (all && !P.isLessonDone(L.id)) {
        P.setLessonResult(L.id, 'diagnosed', 0, 0);
        freed.push(L);
      }
    });

    /* Słabe kontrasty trafiają do powtórek. */
    var weakContrasts = [];
    Object.keys(d.byContrast).forEach(function (cid) {
      var b = d.byContrast[cid];
      if (b.correct < b.asked) { weakContrasts.push(cid); SRS.addContrast(cid); }
    });

    var result = {
      date: U.today(),
      score: d.correct,
      total: d.tasks.length,
      mastered: mastered,
      weak: weak,
      weakContrasts: weakContrasts,
      freed: freed.map(function (L) { return L.id; }),
      byFamily: d.byFamily,
      byContrast: d.byContrast
    };
    var s = store();
    s.diagnostic = {
      date: result.date, score: result.score, total: result.total,
      mastered: mastered, weak: weak, weakContrasts: weakContrasts,
      byFamily: d.byFamily, byContrast: d.byContrast
    };
    Progress.save();
    return result;
  };

  P.diagnosticResult = function () { return store().diagnostic || null; };

  P.progressText = function () {
    var r = P.run;
    return 'Zadanie ' + Math.min(r.at + 1, r.tasks.length) + ' z ' + r.tasks.length;
  };

  /* ------------------------------------------------- powtórki kontrastów */

  /* Karta powtórkowa kontrastu nie ma rekordu w bazie, więc losujemy dla niej
     zadanie z materiału modułu — dowolne, byle dotyczyło tego kontrastu. */
  P.drillFor = function (cid) {
    var pool = [];
    P.lessons().forEach(function (L) {
      L.tasks.forEach(function (t) { if (t.contrastId === cid) pool.push(t); });
    });
    var d = P.diagnostic();
    if (d) d.tasks.forEach(function (t) { if (t.contrastId === cid) pool.push(t); });
    if (!pool.length) return null;
    return pool[Math.floor(Math.random() * pool.length)];
  };

  global.Perception = P;
})(window);
