/* Thai All-in-One — egzaminy poziomowe.

   Czym to się różni od testu poziomującego
   ----------------------------------------
   Test poziomujący (js/placement.js) pyta o WEJŚCIE: gdzie posadzić uczącego
   się na ścieżce. Sprawdza rozpoznanie pojedynczych słów, ma niski próg (60 %)
   i jedną wspólną punktację, bo pomyłka o jedną lekcję w dół nic nie kosztuje.

   Egzamin pyta o WYJŚCIE: czy po przejściu materiału poziom naprawdę jest
   osiągnięty. Dlatego:

     - mierzy cztery sprawności OSOBNO (słuch, szczegóły, mówienie, zapis),
     - każda ma własny próg,
     - poziom jest zaliczony dopiero, gdy WSZYSTKIE cztery przekroczą próg.

   Zakaz średniej jest tu najważniejszą decyzją. Średnia z czterech sprawności
   pozwala nadrobić mówienie słuchem — a to są różne umiejętności i jedna nie
   zastępuje drugiej. „98 % ze słuchu i 20 % w mówieniu” to nie jest 59 %
   znajomości języka, to jest ktoś, kto rozumie i nie umie odpowiedzieć.

   Warunki egzaminacyjne
   ---------------------
   Bez podpowiedzi (żadnych `explain`, `cues` ani podglądu zapisu w trakcie),
   z limitem czasu liczonym osobno na każdą sekcję, z najwyżej jednym
   dodatkowym odsłuchem. Wyjście z egzaminu przerywa podejście — próba zostaje
   zapisana jako porzucona i liczy się do karencji, żeby nie dało się
   podejrzeć zestawu i wyjść. */
(function (global) {
  'use strict';

  var Exam = { state: null };

  var LEVELS = ['Survival', 'A1', 'A2', 'B1', 'B2'];
  var ORDER = ['listening', 'detail', 'speaking', 'writing'];

  /* Ile razy wolno odtworzyć jeden materiał. Jeden odsłuch to za mało nawet
     w prawdziwym egzaminie językowym — przy pierwszym przejściu uwaga idzie
     na wejście w scenę, a nie na treść. Dwa to standard egzaminów
     certyfikatowych i tyle dajemy: pierwszy i JEDEN powtórny. */
  var MAX_PLAYS = 2;

  Exam.LEVELS = LEVELS;
  Exam.ORDER = ORDER;
  Exam.MAX_PLAYS = MAX_PLAYS;

  Exam.ready = function () { return !!(DB.exams && DB.exams.records); };
  Exam.ensureData = function () { return DB.ensureExams(); };

  function meta() { return DB.exams || {}; }
  Exam.meta = meta;

  Exam.thresholds = function () {
    return (meta().thresholds) || {
      listening: 70, detail: 65, speakingTone: 60, speakingContent: 70, writing: 60
    };
  };

  Exam.cooldown = function () {
    return (meta().cooldown) || { days: 5, lessons: 6 };
  };

  Exam.sectionMeta = function (id) {
    var list = meta().sections || [];
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return { id: id, label: id, short: id, skill: '', how: '' };
  };

  Exam.forLevel = function (level) {
    return (meta().records || []).filter(function (e) { return e.level === level; });
  };

  Exam.byId = function (id) {
    var all = meta().records || [];
    for (var i = 0; i < all.length; i++) if (all[i].id === id) return all[i];
    return null;
  };

  /* Ile lekcji poziomu jest już za uczącym się — pokazujemy to przed
     podejściem, bo egzamin z materiału, którego się nie widziało, nie jest
     diagnozą, tylko stratą jednego zestawu. */
  Exam.readiness = function (level) {
    var lessons = (DB.lessons || []).filter(function (L) { return L.level === level; });
    var done = lessons.filter(function (L) { return Progress.isLessonDone(L.id); }).length;
    return {
      total: lessons.length,
      done: done,
      share: lessons.length ? Math.round(done / lessons.length * 100) : 0
    };
  };

  /* ------------------------------------------------------------ karencja */

  /* Który zestaw wypada teraz: ten, którego użyto najdawniej. Po nieudanym
     podejściu uczący się dostaje inny materiał, a nie ten sam klucz. */
  function nextVariant(level) {
    var all = Exam.forLevel(level);
    if (!all.length) return null;
    var used = Progress.examAttempts(level).map(function (a) { return a.examId; });
    var best = null, bestAt = Infinity;
    all.forEach(function (e) {
      var at = used.lastIndexOf(e.id);
      var rank = at === -1 ? -1 : at;
      if (rank < bestAt) { bestAt = rank; best = e; }
    });
    return best;
  }
  Exam.nextVariant = nextVariant;

  /* Czy wolno podejść. Pierwsze podejście zawsze; kolejne dopiero, gdy minęły
     dni ORAZ przybyło lekcji. Każdy z tych warunków osobno da się obejść —
     odstęp przeczekać nic nie robiąc, lekcje przeklikać w jeden wieczór.
     Dopiero oba naraz znaczą „wróć, kiedy coś się zmieniło”. */
  Exam.eligibility = function (level) {
    var cd = Exam.cooldown();
    var attempts = Progress.examAttempts(level);
    var variant = nextVariant(level);
    if (!attempts.length) {
      return { allowed: true, first: true, variant: variant, waitDays: 0, waitLessons: 0 };
    }
    var last = attempts[attempts.length - 1];
    var days = U.daysBetween(last.date, U.today());
    var lessonsNow = Progress.lessonsDone();
    var grown = lessonsNow - (last.lessonsDone || 0);
    var waitDays = Math.max(0, cd.days - days);
    var waitLessons = Math.max(0, cd.lessons - grown);
    return {
      allowed: waitDays === 0 && waitLessons === 0,
      first: false,
      variant: variant,
      waitDays: waitDays,
      waitLessons: waitLessons,
      last: last,
      days: days,
      grown: grown
    };
  };

  /* ------------------------------------------------------------- przebieg */

  Exam.start = function (level) {
    var exam = nextVariant(level);
    if (!exam) return null;
    Exam.state = {
      exam: exam,
      level: level,
      startedAt: Date.now(),
      sectionAt: 0,
      section: ORDER[0],
      at: 0,
      plays: {},                 /* klucz materiału -> ile razy odtworzony */
      sections: {
        listening: { answers: [], startedAt: null, endedAt: null, expired: false },
        detail: { answers: [], startedAt: null, endedAt: null, expired: false },
        speaking: { answers: [], startedAt: null, endedAt: null, expired: false },
        writing: { answers: [], startedAt: null, endedAt: null, expired: false }
      },
      finished: false,
      abandoned: false
    };
    return Exam.state;
  };

  Exam.active = function () {
    return !!(Exam.state && !Exam.state.finished && !Exam.state.abandoned);
  };

  Exam.section = function () {
    var s = Exam.state;
    return s ? s.exam.sections[s.section] : null;
  };

  Exam.tasks = function (sectionId) {
    var sec = Exam.state.exam.sections[sectionId || Exam.state.section];
    return sec.questions || sec.items || [];
  };

  /* Ile sekund zostało w bieżącej sekcji. Zwraca null, zanim sekcja ruszy. */
  Exam.secondsLeft = function () {
    var s = Exam.state;
    if (!s) return null;
    var box = s.sections[s.section];
    if (!box.startedAt) return s.exam.sections[s.section].timeLimitSec;
    var used = Math.floor((Date.now() - box.startedAt) / 1000);
    return Math.max(0, s.exam.sections[s.section].timeLimitSec - used);
  };

  Exam.beginSection = function () {
    var s = Exam.state;
    var box = s.sections[s.section];
    if (!box.startedAt) box.startedAt = Date.now();
    s.at = 0;
    return box;
  };

  /* Odsłuch: zwraca false, gdy limit odtworzeń wyczerpany. */
  Exam.canPlay = function (key) {
    return (Exam.state.plays[key] || 0) < MAX_PLAYS;
  };
  Exam.notePlay = function (key) {
    var s = Exam.state;
    s.plays[key] = (s.plays[key] || 0) + 1;
    return s.plays[key];
  };
  Exam.playsLeft = function (key) {
    return Math.max(0, MAX_PLAYS - (Exam.state.plays[key] || 0));
  };

  /* ----------------------------------------------------------- odpowiedzi */

  Exam.answerQuestion = function (question, chosen) {
    var s = Exam.state;
    var box = s.sections[s.section];
    var ok = chosen === question.answer;
    box.answers.push({
      id: question.id,
      kind: question.kind,
      sceneId: question.sceneId,
      chosen: chosen,
      ok: ok
    });
    s.at += 1;
    return ok;
  };

  /* --- produkcja ustna ---
     Wymowę ocenia ToneScore z sesji J: to jest pomiar, nie deklaracja.
     Treść jest deklarowana przez uczącego się PO odsłuchaniu wzorca, ale nie
     na słowo honoru: deklarację „powiedziałem to samo” przyjmujemy tylko
     wtedy, gdy nagranie w ogóle mogło nią być. Kontrolą jest liczba sylab
     wykrytych w nagraniu — jeśli od oczekiwanej odbiega o więcej niż połowę,
     to nie było to zdanie i deklaracja zostaje odrzucona. To nie jest
     rozpoznawanie mowy i nie udaje nim być; to zabezpieczenie przed
     przypadkiem „nacisnąłem, chrząknąłem, zaznaczyłem zaliczone”. */
  Exam.checkPlausible = function (analysis, expectedSyllables) {
    if (!analysis || !expectedSyllables) return false;
    var got = (analysis.syllables || []).length;
    if (!got) return false;
    var slack = Math.max(1, Math.round(expectedSyllables * 0.5));
    return Math.abs(got - expectedSyllables) <= slack;
  };

  Exam.CLAIMS = [
    { id: 'same', label: 'Powiedziałem dokładnie to', value: 1 },
    { id: 'close', label: 'Powiedziałem inaczej, ale o to samo', value: 0.5 },
    { id: 'miss', label: 'Nie powiedziałem tego', value: 0 }
  ];

  Exam.answerSpeaking = function (item, data) {
    var s = Exam.state;
    var box = s.sections[s.section];
    var claim = data.claim || 'miss';
    var value = 0;
    Exam.CLAIMS.forEach(function (c) { if (c.id === claim) value = c.value; });
    /* Deklaracja bez wiarygodnego nagrania nie liczy się wcale. */
    if (!data.plausible) value = 0;
    box.answers.push({
      id: item.id,
      recordId: item.recordId,
      lesson: item.lesson,
      tone: data.tone === null || data.tone === undefined ? 0 : data.tone,
      claim: claim,
      plausible: !!data.plausible,
      content: value,
      empty: !!data.empty
    });
    s.at += 1;
    return value;
  };

  /* --- produkcja pisemna ---
     Punktujemy sylabami, nie zerojedynkowo. Zapis „sawàt-dee” zamiast
     „sawàt-dii” to jedna pomyłka w dwóch sylabach, a nie całkowity brak
     wiedzy — a przy ocenie „wszystko albo nic” obie sytuacje dają zero
     i egzamin przestaje odróżniać „prawie umiem” od „nie mam pojęcia”.

     Znaki tonu liczymy OSOBNO i nie wchodzą do progu. Uczący się może mieć
     włączone ukrywanie tonów przez cały kurs; wymaganie ich na egzaminie
     sprawdzałoby wtedy ustawienie, a nie umiejętność. Trafność tonów trafia
     do diagnozy, bo jest cenną informacją — tylko nie decyduje o zaliczeniu. */
  function norm(text) {
    return U.fold(text || '').replace(/[^a-z]/g, '');
  }

  function levenshtein(a, b) {
    var m = a.length, n = b.length;
    if (!m) return n;
    if (!n) return m;
    var prev = [], cur = [], i, j;
    for (j = 0; j <= n; j++) prev[j] = j;
    for (i = 1; i <= m; i++) {
      cur[0] = i;
      for (j = 1; j <= n; j++) {
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1,
                          prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
      }
      for (j = 0; j <= n; j++) prev[j] = cur[j];
    }
    return prev[n];
  }
  Exam.levenshtein = levenshtein;

  Exam.scoreWriting = function (typed, expected) {
    var exp = U.syllables(expected).map(function (x) { return norm(x); }).filter(Boolean);
    var got = U.syllables(typed).map(function (x) { return norm(x); }).filter(Boolean);
    /* Zapis bez spacji i myślników („sawatdii”) też ma być uczciwie oceniony —
       porównujemy wtedy ciągi liter, bo sam podział na sylaby nie jest
       przedmiotem tego zadania. */
    if (got.length === 1 && exp.length > 1) {
      var flat = got[0], joined = exp.join('');
      var d = levenshtein(flat.split(''), joined.split(''));
      var share = joined.length ? Math.max(0, 1 - d / joined.length) : 0;
      return { base: share, syllables: exp.length, tones: null, flat: true };
    }
    var dist = levenshtein(exp, got);
    var span = Math.max(exp.length, got.length) || 1;
    var base = Math.max(0, 1 - dist / span);

    /* Tony: porównujemy tylko tam, gdzie sylaba trafiła w swoje miejsce. */
    var toneHits = 0, toneSeen = 0;
    var typedSyl = U.syllables(typed);
    var expSyl = U.syllables(expected);
    for (var i = 0; i < Math.min(typedSyl.length, expSyl.length); i++) {
      if (norm(typedSyl[i]) !== norm(expSyl[i])) continue;
      toneSeen += 1;
      if (U.toneOf(typedSyl[i]) === U.toneOf(expSyl[i])) toneHits += 1;
    }
    return {
      base: base,
      syllables: exp.length,
      tones: toneSeen ? toneHits / toneSeen : null,
      toneSeen: toneSeen,
      flat: false
    };
  };

  Exam.answerWriting = function (item, typed, expected) {
    var s = Exam.state;
    var box = s.sections[s.section];
    var score = Exam.scoreWriting(typed, expected);
    box.answers.push({
      id: item.id,
      recordId: item.recordId,
      lesson: item.lesson,
      typed: typed,
      base: score.base,
      tones: score.tones,
      ok: score.base >= 0.999
    });
    s.at += 1;
    return score;
  };

  /* --------------------------------------------------------- zamykanie */

  /* Sekcja kończy się z upływem czasu albo po ostatnim zadaniu. Zadania
     nietknięte liczą się jak pomyłki — inaczej limit czasu byłby premią
     („nie zdążę, więc mi nie policzą”). */
  Exam.closeSection = function (expired) {
    var s = Exam.state;
    var box = s.sections[s.section];
    box.endedAt = Date.now();
    if (expired) box.expired = true;
    var tasks = Exam.tasks(s.section);
    var answered = box.answers.length;
    for (var i = answered; i < tasks.length; i++) {
      var t = tasks[i];
      if (s.section === 'speaking') {
        box.answers.push({ id: t.id, recordId: t.recordId, lesson: t.lesson,
                           tone: 0, claim: 'miss', plausible: false, content: 0,
                           empty: true, skipped: true });
      } else if (s.section === 'writing') {
        box.answers.push({ id: t.id, recordId: t.recordId, lesson: t.lesson,
                           typed: '', base: 0, tones: null, ok: false, skipped: true });
      } else {
        box.answers.push({ id: t.id, kind: t.kind, sceneId: t.sceneId,
                           chosen: -1, ok: false, skipped: true });
      }
    }
    return box;
  };

  Exam.nextSection = function () {
    var s = Exam.state;
    s.sectionAt += 1;
    if (s.sectionAt >= ORDER.length) return null;
    s.section = ORDER[s.sectionAt];
    s.at = 0;
    return s.section;
  };

  /* ------------------------------------------------------------ punktacja */

  function pct(part, whole) {
    return whole ? Math.round(part / whole * 1000) / 10 : 0;
  }

  Exam.score = function (state) {
    var th = Exam.thresholds();
    var out = {};

    ['listening', 'detail'].forEach(function (id) {
      var ans = state.sections[id].answers;
      var hit = ans.filter(function (a) { return a.ok; }).length;
      var value = pct(hit, ans.length);
      out[id] = {
        id: id, correct: hit, total: ans.length, pct: value,
        threshold: th[id], passed: value >= th[id],
        expired: state.sections[id].expired
      };
    });

    var sp = state.sections.speaking.answers;
    var toneSum = 0, contentSum = 0;
    sp.forEach(function (a) { toneSum += a.tone || 0; contentSum += a.content || 0; });
    var tone = sp.length ? Math.round(toneSum / sp.length * 10) / 10 : 0;
    var content = pct(contentSum, sp.length);
    out.speaking = {
      id: 'speaking', tone: tone, content: content, total: sp.length,
      pct: Math.min(tone, content),
      toneThreshold: th.speakingTone, contentThreshold: th.speakingContent,
      tonePassed: tone >= th.speakingTone,
      contentPassed: content >= th.speakingContent,
      passed: tone >= th.speakingTone && content >= th.speakingContent,
      threshold: th.speakingTone,
      expired: state.sections.speaking.expired
    };

    var wr = state.sections.writing.answers;
    var baseSum = 0, toneHit = 0, toneSeen = 0;
    wr.forEach(function (a) {
      baseSum += a.base || 0;
      if (a.tones !== null && a.tones !== undefined) { toneHit += a.tones; toneSeen += 1; }
    });
    var wpct = wr.length ? Math.round(baseSum / wr.length * 1000) / 10 : 0;
    out.writing = {
      id: 'writing', pct: wpct, total: wr.length,
      tonePct: toneSeen ? Math.round(toneHit / toneSeen * 1000) / 10 : null,
      threshold: th.writing, passed: wpct >= th.writing,
      expired: state.sections.writing.expired
    };

    /* Zaliczenie: KONIUNKCJA, nie średnia. Jedna sprawność poniżej progu
       przesądza o wyniku całego egzaminu. */
    out.passed = ORDER.every(function (id) { return out[id].passed; });
    out.passedCount = ORDER.filter(function (id) { return out[id].passed; }).length;
    return out;
  };

  /* --------------------------------------------------------------- koniec */

  Exam.finish = function () {
    var s = Exam.state;
    if (!s || s.finished) return null;
    s.finished = true;
    var scored = Exam.score(s);
    var attempt = {
      examId: s.exam.id,
      level: s.level,
      variant: s.exam.variant,
      date: U.today(),
      at: new Date().toISOString(),
      durationSec: Math.round((Date.now() - s.startedAt) / 1000),
      lessonsDone: Progress.lessonsDone(),
      abandoned: false,
      passed: scored.passed,
      sections: {
        listening: scored.listening,
        detail: scored.detail,
        speaking: scored.speaking,
        writing: scored.writing
      },
      answers: {
        listening: s.sections.listening.answers,
        detail: s.sections.detail.answers,
        speaking: s.sections.speaking.answers,
        writing: s.sections.writing.answers
      }
    };
    Progress.saveExamAttempt(attempt);
    Exam.lastAttempt = attempt;
    return attempt;
  };

  /* Wyjście w trakcie. Zapisujemy próbę jako porzuconą i wliczamy ją do
     karencji — inaczej dałoby się przejrzeć wszystkie trzy zestawy bez
     żadnego kosztu i wrócić do nich z gotowymi odpowiedziami. */
  Exam.abandon = function () {
    var s = Exam.state;
    if (!s || s.finished || s.abandoned) return null;
    s.abandoned = true;
    var attempt = {
      examId: s.exam.id,
      level: s.level,
      variant: s.exam.variant,
      date: U.today(),
      at: new Date().toISOString(),
      durationSec: Math.round((Date.now() - s.startedAt) / 1000),
      lessonsDone: Progress.lessonsDone(),
      abandoned: true,
      passed: false,
      reachedSection: s.section,
      sections: null,
      answers: null
    };
    Progress.saveExamAttempt(attempt);
    Exam.state = null;
    return attempt;
  };

  /* ------------------------------------------------------------- diagnoza */

  var SECTION_ADVICE = {
    listening: {
      why: 'Sens całej sceny umyka, choć pojedyncze słowa mogą być znane. To zwykle nie brak słownictwa, tylko brak wprawy w słuchaniu dłuższych całości bez zatrzymywania.',
      screen: 'extensive',
      screenLabel: 'Słuchanie ekstensywne'
    },
    detail: {
      why: 'Ogólny sens dociera, ale konkrety gubią się po drodze — kto co powiedział, co padło w odpowiedzi. Trzeba słuchać tych samych scen drugi raz, tym razem po szczegóły.',
      screen: 'scenes',
      screenLabel: 'Sceny'
    },
    speaking: {
      why: 'Rozumienie jest wyżej niż mówienie. To najczęstszy rozjazd w nauce ze słuchu i nie znika sam — trzeba osobno ćwiczyć produkcję, a nie kolejne odsłuchy.',
      screen: 'produce',
      screenLabel: 'Mówienie po tajsku'
    },
    writing: {
      why: 'Brzmienie zwrotów jest rozpoznawane, ale nie odtwarzane z pamięci. Zapis fonetyczny jest najprostszym sprawdzianem tego, czy forma dźwiękowa naprawdę siedzi w głowie.',
      screen: 'listen',
      screenLabel: 'Słuchanie — dyktando'
    }
  };

  /* Wynik to nie procent. Rozbicie na sprawności, wskazanie najsłabszej
     i plan z konkretnych lekcji oraz ćwiczeń — bo „62 %” nie mówi, co robić
     jutro rano. */
  Exam.diagnose = function (attempt) {
    if (!attempt || attempt.abandoned || !attempt.sections) return null;
    var sections = ORDER.map(function (id) {
      var box = attempt.sections[id];
      var margin = (id === 'speaking')
        ? Math.min(box.tone - box.toneThreshold, box.content - box.contentThreshold)
        : box.pct - box.threshold;
      return {
        id: id,
        meta: Exam.sectionMeta(id),
        box: box,
        margin: Math.round(margin * 10) / 10,
        passed: box.passed
      };
    });

    var sorted = sections.slice().sort(function (a, b) { return a.margin - b.margin; });
    var weakest = sorted[0];
    var failed = sections.filter(function (s) { return !s.passed; });

    /* Lekcje do powtórzenia bierzemy z zadań, które poszły źle — nie
       z całego poziomu. Powtórka „całego A2” jest radą bezużyteczną. */
    var lessons = {};
    var wrongRecords = [];
    (attempt.answers.speaking || []).forEach(function (a) {
      if (a.content < 1 && a.lesson) lessons[a.lesson] = (lessons[a.lesson] || 0) + 1;
      if (a.content < 1 && a.recordId) wrongRecords.push(a.recordId);
    });
    (attempt.answers.writing || []).forEach(function (a) {
      if (a.base < 0.75 && a.lesson) lessons[a.lesson] = (lessons[a.lesson] || 0) + 1;
      if (a.base < 0.75 && a.recordId) wrongRecords.push(a.recordId);
    });
    var scenes = {};
    ['listening', 'detail'].forEach(function (id) {
      (attempt.answers[id] || []).forEach(function (a) {
        if (!a.ok && a.sceneId) scenes[a.sceneId] = (scenes[a.sceneId] || 0) + 1;
      });
    });

    var lessonList = Object.keys(lessons).map(Number).sort(function (a, b) {
      return lessons[b] - lessons[a] || a - b;
    }).slice(0, 6);
    var sceneList = Object.keys(scenes).sort(function (a, b) {
      return scenes[b] - scenes[a];
    }).slice(0, 4);

    var plan = [];
    failed.forEach(function (s) {
      var advice = SECTION_ADVICE[s.id];
      plan.push({
        kind: 'section',
        section: s.id,
        title: s.meta.label + ' — poniżej progu',
        why: advice.why,
        screen: advice.screen,
        screenLabel: advice.screenLabel
      });
    });
    if (sceneList.length) {
      plan.push({
        kind: 'scenes',
        title: 'Przesłuchaj ponownie sceny, w których zgubiłeś odpowiedzi',
        why: 'Te same sceny, ale tym razem z zapisem i bez limitu czasu. Różnica między tym, co usłyszałeś na egzaminie, a tym, co widzisz w zapisie, jest listą rzeczy do douczenia.',
        screen: 'scenes',
        screenLabel: 'Sceny',
        sceneIds: sceneList
      });
    }
    if (lessonList.length) {
      plan.push({
        kind: 'lessons',
        title: 'Wróć do lekcji, z których pochodziły nietrafione zwroty',
        why: 'To są konkretne lekcje, nie „powtórz poziom”. Każda z nich dała na egzaminie co najmniej jedną pomyłkę.',
        screen: 'course',
        screenLabel: 'Kurs',
        lessons: lessonList
      });
    }
    if (wrongRecords.length) {
      plan.push({
        kind: 'srs',
        title: 'Dorzuć nietrafione hasła do powtórek',
        why: 'Hasła z pomyłek trafiają do kolejki od razu, zamiast czekać na swój termin.',
        screen: 'srs',
        screenLabel: 'Powtórki',
        records: wrongRecords.slice(0, 40)
      });
    }

    return {
      sections: sections,
      weakest: weakest,
      failed: failed,
      passed: attempt.passed,
      lessons: lessonList,
      scenes: sceneList,
      records: wrongRecords,
      plan: plan
    };
  };

  /* Nietrafione hasła wracają do kolejki powtórek. Robimy to raz, przy
     zamknięciu egzaminu — diagnoza ma prowadzić do działania, a nie do
     kolejnej listy rzeczy do zrobienia ręcznie. */
  Exam.pushToSRS = function (attempt) {
    if (!attempt || !attempt.answers) return 0;
    var ids = [];
    (attempt.answers.speaking || []).forEach(function (a) {
      if (a.content < 1 && a.recordId) ids.push(a.recordId);
    });
    (attempt.answers.writing || []).forEach(function (a) {
      if (a.base < 0.75 && a.recordId) ids.push(a.recordId);
    });
    var added = 0;
    ids.forEach(function (id) {
      if (!global.SRS) return;
      SRS.add(id, 'r');
      SRS.grade(id, 2, { side: 'r' });
      added += 1;
    });
    return added;
  };

  global.Exam = Exam;
})(window);
