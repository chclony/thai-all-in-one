/* Thai All-in-One — postęp użytkownika.
   Eksport zawiera wyłącznie dane postępu. Nie ma w nim treści bazy ani pola technicznego TTS. */
(function (global) {
  'use strict';

  var Progress = {
    data: null,
    sessionStart: Date.now(),
    lastTick: Date.now()
  };

  function blank() {
    return {
      days: {},          // '2026-08-13': { answers, correct, minutes, newWords }
      streak: 0,
      bestStreak: 0,
      lastDay: null,
      totalAnswers: 0,
      totalCorrect: 0,
      minutes: 0,
      seen: {},          // id -> liczba kontaktów
      favourites: {},    // id -> true
      lists: {},         // nazwa listy -> [id]
      goal: 20,

      /* Wynik testu poziomującego: poziom, punkty i lekcja, od której
         zaczyna się nauka. Dopóki go nie ma, kurs nie wie, co pokazać. */
      placement: null,   // { level, score, total, date, entryLesson }

      /* Stan lekcji: id -> { status: 'passed'|'skipped', score, total, date } */
      lessons: {},

      /* Czas reakcji w ćwiczeniach produkcyjnych: od pokazania polecenia do
         odpowiedzi. Płynność to nie to samo co poprawność — hasło, które
         uczący się zna, ale odtwarza po pięciu sekundach, w rozmowie nie
         zadziała. Trzymamy ostatnie próby na hasło (mediana jest odporna na
         pojedyncze rozproszenie) i wspólny dziennik do mediany ogólnej. */
      times: {},         // id -> [ms, ms, ...] (ostatnie TIME_SAMPLES prób)
      timeLog: [],       // [{d, ms, mode}] — do mediany i statystyk

      /* Moduł 0 — trening percepcyjny. Trzymamy go osobno od lekcji kursu,
         bo mierzy co innego: nie „czy znasz to hasło”, tylko „czy Twoje ucho
         rozróżnia ten kontrast”. Statystyka jest prowadzona per kontrast
         (ton wysoki kontra opadający, p kontra ph i tak dalej), bo tylko na
         tym poziomie da się powiedzieć, czego dokładnie uczący się nie słyszy. */
      perception: {
        lessons: {},     // id lekcji -> { status, score, total, date }
        contrasts: {},   // id kontrastu -> { answers, correct }
        history: [],     // { d, c, ok } — do wykresu w czasie
        diagnostic: null,
        skipped: false
      },

      /* DRABINA TEMPA (sesja M).

         Rozumienie ze słuchu nie jest jedną umiejętnością, tylko trzema.
         Ktoś, kto bez pudła rozbiera zdanie podane wyraz po wyrazie (0,7x),
         potrafi nie zrozumieć ani słowa z tego samego zdania powiedzianego
         normalnie (1,0x) — a mowa potoczna (1,4x) to jeszcze co innego,
         bo dochodzą do niej redukcje. Zaliczenie przy jednym tempie nie
         mówi więc nic o pozostałych i nie może ich zaliczać.

         Stąd osobny licznik dla każdej pary (ćwiczenie, tempo). Mapa postępu
         czyta z tego, na którym stopniu uczący się stanął. */
      tempo: {},         // ćwiczenie -> { slow|natural|fast -> { answers, correct, streak, passed, date } }

      /* Wyniki słuchania ekstensywnego: ile zrozumiane przy pierwszym
         przejściu (bez tekstu), a ile dopiero po zobaczeniu zapisu. */
      extensive: {},     // id bloku -> { runs: [...], best }

      /* Błędy w rozbiciu na obszary. Liczymy odpowiedzi i pomyłki osobno,
         bo sama liczba pomyłek premiuje obszary, których się nie ćwiczy. */
      errors: {
        category: {},    // kategoria -> { answers, wrong }
        grammar: {},     // id tematu gramatycznego -> { answers, wrong }
        type: {},        // typ rekordu -> { answers, wrong }
        mode: {}         // tryb ćwiczenia -> { answers, wrong }
      },

      /* Dziennik pomyłek — konkretne hasła, nie zbiorcze liczniki.

         Statystyka błędów wyżej mówi, GDZIE jest słabo. Ta lista mówi, NA CZYM:
         które hasło, w którym ćwiczeniu i kiedy poszło źle. Bez niej sesja
         naprawcza mogłaby tylko wylosować hasła z najsłabszej kategorii, a to
         jest coś innego niż powtórzenie tego, na czym uczący się poległ.

         Trzymamy ostatnie MISS_LIMIT wpisów. Starsze pomyłki i tak nie opisują
         już dzisiejszego stanu — hasło sprzed pół roku albo zostało nadrobione,
         albo wraca w powtórkach własnym trybem. */
      misses: [],        // [{ d, id, mode, cat, type, gram }]

      /* LICZBY (sesja T).

         Przy liczbach główną miarą opanowania jest CZAS REAKCJI, nie sama
         poprawność. Liczba odczytana bezbłędnie po sześciu sekundach nie
         zadziałała w kasie: kasjer zdążył powtórzyć, pokazać na wyświetlaczu
         albo policzyć za nas. Dlatego trzymamy czasy osobno od `timeLog`
         ćwiczeń produkcyjnych — wymieszane dawałyby medianę, która nie opisuje
         żadnej z tych dwóch rzeczy. */
      numbers: {},       // tryb -> { answers, correct, timeouts, times: [ms], best }

      /* ODRUCH RATUNKOWY (sesja T).

         Mierzymy dwie rzeczy naraz i celowo je rozdzielamy: czy uczący się
         REAGUJE (a nie zamiera) i czy po jego reakcji rozmowa faktycznie się
         naprawia. Pierwsze bez drugiego to uprzejmy sposób na utknięcie w tym
         samym miejscu. */
      reflex: {},        // wyzwalacz -> { answers, correct, frozen, times: [ms], repaired, repairTries }

      /* EGZAMINY POZIOMOWE (sesja U).

         Trzymamy CAŁĄ historię podejść, nie tylko najlepsze. Trzy powody:
         karencja przed powtórką liczy się od ostatniego podejścia (także
         porzuconego); wybór zestawu idzie po tym, który był używany najdawniej;
         a certyfikat ma pokazywać drogę, a nie jeden szczęśliwy wynik.

         Podejście porzucone (wyjście z egzaminu w trakcie) też tu ląduje —
         inaczej dałoby się przejrzeć wszystkie trzy zestawy bez kosztu. */
      exams: {},         // poziom -> { attempts: [...], passedAt, bestAt }

      /* PRÓBKI KONTROLNE (sesja U).

         Krótki test co 20 lekcji z materiału sprzed 20 lekcji. Osobno od
         `days` i od SRS-u, bo jego zadaniem jest właśnie wykrycie tego, czego
         kolejka powtórek jeszcze nie zdążyła pokazać. */
      checkpoints: {}    // id próbki -> { attempts: [...], best, lastDate }
    };
  }

  /* Ile pojedynczych pomyłek pamiętamy. Osiemset to około miesiąca intensywnej
     nauki — dość, by sesja naprawcza miała z czego wybierać, za mało, by
     kopia zapasowa spuchła. */
  var MISS_LIMIT = 800;

  Progress.load = function () {
    /* Kopia z dysku bywa niepełna: zapisała ją starsza wersja aplikacji,
       została ręcznie sklejona albo zapis przerwał się w połowie. Brakujący
       klucz najwyższego poziomu (choćby `days`) wywracał wcześniej CAŁY start
       — z komunikatem o niekompletnym katalogu `data/`, czyli wskazującym
       zupełnie nie tam. Dlatego wczytana kopia jest nakładana na komplet
       domyślnych pól, dokładnie tak samo jak przy imporcie kopii zapasowej
       (Progress.importData). Brak pola oznacza wartość początkową, nigdy
       awarię. */
    var stored = U.store.get('progress', null);
    Progress.data = stored ? Object.assign(blank(), stored) : blank();
    var d = Progress.data;
    /* Scalenie wyżej jest płytkie, więc zagnieżdżone sekcje domykamy osobno. */
    if (!d.lists) d.lists = {};
    if (!d.favourites) d.favourites = {};
    if (!d.lessons) d.lessons = {};
    if (!d.times) d.times = {};
    if (!Array.isArray(d.timeLog)) d.timeLog = [];
    if (!d.errors) d.errors = {};
    ['category', 'grammar', 'type', 'mode'].forEach(function (k) {
      if (!d.errors[k]) d.errors[k] = {};
    });
    /* Kopie sprzed sesji P nie mają dziennika pomyłek. Zakładamy pusty —
       zapełni się przy pierwszych odpowiedziach. */
    if (!Array.isArray(d.misses)) d.misses = [];
    if (d.placement === undefined) d.placement = null;
    /* Kopia zapisana przed sesją K nie ma sekcji percepcyjnej. Dokładamy ją
       przy wczytaniu, żeby import starszego pliku nie wywracał modułu. */
    if (!d.tempo) d.tempo = {};
    if (!d.extensive) d.extensive = {};
    if (!d.perception) d.perception = { lessons: {}, contrasts: {}, history: [], diagnostic: null, skipped: false };
    if (!d.perception.lessons) d.perception.lessons = {};
    if (!d.perception.contrasts) d.perception.contrasts = {};
    if (!Array.isArray(d.perception.history)) d.perception.history = [];
    if (d.perception.diagnostic === undefined) d.perception.diagnostic = null;
    /* Kopie sprzed sesji U nie znają egzaminów ani próbek kontrolnych.
       Puste sekcje są tu poprawnym stanem początkowym: nikt jeszcze nie
       podchodził, więc pierwsze podejście będzie pierwszym. */
    if (!d.exams) d.exams = {};
    if (!d.checkpoints) d.checkpoints = {};
    Progress.touchDay();
    return d;
  };

  Progress.perception = function () { return Progress.data.perception; };

  Progress.save = function () { U.store.set('progress', Progress.data); };

  Progress.day = function (date) {
    var key = date || U.today();
    if (!Progress.data.days[key]) {
      Progress.data.days[key] = { answers: 0, correct: 0, minutes: 0, newWords: 0 };
    }
    return Progress.data.days[key];
  };

  /* Aktualizuje serię dni nauki. */
  Progress.touchDay = function () {
    var d = Progress.data, today = U.today();
    if (d.lastDay === today) return;
    if (!d.lastDay) d.streak = 0;
    else {
      var gap = U.daysBetween(d.lastDay, today);
      if (gap === 1) d.streak = d.streak; /* seria trwa — zwiększymy przy pierwszej odpowiedzi */
      else if (gap > 1) d.streak = 0;
    }
    Progress.save();
  };

  Progress.registerActivity = function () {
    var d = Progress.data, today = U.today();
    if (d.lastDay !== today) {
      var gap = d.lastDay ? U.daysBetween(d.lastDay, today) : 999;
      d.streak = gap === 1 ? d.streak + 1 : 1;
      d.lastDay = today;
      if (d.streak > d.bestStreak) d.bestStreak = d.streak;
    }
    Progress.day(today);
  };

  function bump(bucket, key, correct) {
    if (!key) return;
    var box = bucket[key] || (bucket[key] = { answers: 0, wrong: 0 });
    box.answers += 1;
    if (!correct) box.wrong += 1;
  }

  /* context: { mode: 'tone', grammarId: 'gram-004' } — opcjonalny.
     Kategoria i typ dobierają się same z rekordu, także wtedy, gdy w pamięci
     jest tylko lekki wpis z indeksu. */
  Progress.answer = function (id, correct, context) {
    Progress.registerActivity();
    var day = Progress.day();
    day.answers += 1;
    Progress.data.totalAnswers += 1;
    if (correct) { day.correct += 1; Progress.data.totalCorrect += 1; }
    Progress.data.seen[id] = (Progress.data.seen[id] || 0) + 1;
    if (Progress.data.seen[id] === 1) day.newWords += 1;

    var rec = (global.DB && DB.any) ? DB.any(id) : null;
    var e = Progress.data.errors;
    if (rec) {
      bump(e.category, rec.category, correct);
      bump(e.type, rec.type, correct);
    }
    context = context || {};
    if (context.mode) bump(e.mode, context.mode, correct);
    if (context.grammarId) bump(e.grammar, context.grammarId, correct);

    /* Pomyłkę zapisujemy imiennie. Kolejne pudło na tym samym haśle w tym samym
       trybie tego samego dnia nie zakłada nowego wpisu — podbija licznik
       istniejącego, żeby jedna trudna sesja nie zapchała dziennika jednym
       hasłem i nie wypchnęła z niego reszty. */
    if (!correct) {
      if (!Array.isArray(Progress.data.misses)) Progress.data.misses = [];
      var today = U.today();
      var mode = context.mode || '';
      var prev = null;
      for (var i = Progress.data.misses.length - 1; i >= 0; i--) {
        var m = Progress.data.misses[i];
        if (m.d !== today) break;
        if (m.id === id && m.mode === mode) { prev = m; break; }
      }
      if (prev) {
        prev.n = (prev.n || 1) + 1;
      } else {
        Progress.data.misses.push({
          d: today,
          id: id,
          mode: mode,
          n: 1,
          cat: rec ? rec.category : '',
          type: rec ? rec.type : '',
          gram: context.grammarId || ''
        });
        if (Progress.data.misses.length > MISS_LIMIT) {
          Progress.data.misses = Progress.data.misses.slice(-MISS_LIMIT);
        }
      }
    }

    Progress.save();

    /* Jeden punkt obserwacji dla wszystkich ćwiczeń w aplikacji.

       Sesja dnia musi wiedzieć, czy krok poszedł dobrze, a ćwiczeń jest ponad
       dwadzieścia i każde melduje wynik inaczej. Wpinanie się w każde z osobna
       oznaczałoby dwadzieścia miejsc, w których nowy tryb ćwiczenia zapomni
       się zgłosić. Tędy przechodzi każda odpowiedź w aplikacji — bo każde
       ćwiczenie i tak musi ją tutaj policzyć. */
    if (typeof Progress.onAnswer === 'function') {
      try { Progress.onAnswer(id, correct, context || {}); } catch (err) {}
    }
  };

  /* Ustawiane przez ekran sesji dnia na czas jej trwania i zdejmowane po
     wyjściu. Domyślnie puste — reszta aplikacji działa bez obserwatora. */
  Progress.onAnswer = null;

  /* Pomyłki w jednym obszarze, od najświeższych. `bucket` to ta sama nazwa,
     której używa Progress.weakAreas(): 'category', 'grammar', 'mode', 'type'.
     Zwracamy hasła, nie wpisy — jedno hasło może mieć kilka pudeł i liczy się
     raz, z sumą prób i najświeższą datą. */
  Progress.missesIn = function (bucket, key, limit) {
    var field = { category: 'cat', grammar: 'gram', mode: 'mode', type: 'type' }[bucket];
    if (!field) return [];
    var byId = {};
    var list = Progress.data.misses || [];
    for (var i = list.length - 1; i >= 0; i--) {
      var m = list[i];
      if (key && m[field] !== key) continue;
      if (!byId[m.id]) {
        byId[m.id] = { id: m.id, n: 0, last: m.d, modes: {} };
      }
      byId[m.id].n += (m.n || 1);
      if (m.mode) byId[m.id].modes[m.mode] = (byId[m.id].modes[m.mode] || 0) + (m.n || 1);
    }
    var out = Object.keys(byId).map(function (k) { return byId[k]; });
    /* Najpierw hasła mylone najczęściej, przy remisie — najświeższe. */
    out.sort(function (a, b) { return b.n - a.n || (a.last < b.last ? 1 : -1); });
    return limit ? out.slice(0, limit) : out;
  };

  /* Czas nauki liczymy w minutach aktywności, z przerwą po 2 minutach bezczynności. */
  Progress.tick = function () {
    var now = Date.now();
    var delta = (now - Progress.lastTick) / 60000;
    Progress.lastTick = now;
    if (delta <= 0 || delta > 2) return;
    Progress.registerActivity();
    Progress.day().minutes += delta;
    Progress.data.minutes += delta;
    Progress.save();
  };

  /* ------------------------------------------------------- drabina tempa */

  /* Ćwiczenia rozumienia objęte drabiną. Kolejność jest kolejnością na mapie
     postępu, a etykiety muszą się zgadzać z nazwami trybów na ekranach —
     inaczej mapa mówi o czymś, czego uczący się u siebie nie widzi. */
  var TEMPO_EXERCISES = ['choice', 'dictation', 'assemble', 'spot', 'gender',
    'noise', 'gap', 'unknown', 'scene', 'extensive', 'numbers']
    .map(function (id) { return { id: id, label: U.exLabel(id) }; });

  var TEMPO_STEPS = [
    { id: 'slow', label: '0,7x', hint: 'dydaktyczne' },
    { id: 'natural', label: '1,0x', hint: 'naturalne' },
    { id: 'fast', label: '1,4x', hint: 'potoczne' }
  ];

  /* Próg zaliczenia. Dziesięć odpowiedzi to minimum, przy którym 80 procent
     nie jest jeszcze przypadkiem: przy czterech opcjach ślepe zgadywanie daje
     25 procent, a szansa dobicia do 8/10 losowo jest rzędu jednej na tysiąc. */
  var TEMPO_MIN_ANSWERS = 10;
  var TEMPO_MIN_SHARE = 0.8;

  Progress.tempoExercises = function () { return TEMPO_EXERCISES.slice(); };
  Progress.tempoSteps = function () { return TEMPO_STEPS.slice(); };

  Progress.tempoLabel = function (id) {
    for (var i = 0; i < TEMPO_STEPS.length; i++) {
      if (TEMPO_STEPS[i].id === id) return TEMPO_STEPS[i].label;
    }
    return id;
  };

  Progress.exerciseLabel = function (id) {
    for (var i = 0; i < TEMPO_EXERCISES.length; i++) {
      if (TEMPO_EXERCISES[i].id === id) return TEMPO_EXERCISES[i].label;
    }
    return id;
  };

  function tempoCell(exercise, tempo) {
    var all = Progress.data.tempo || (Progress.data.tempo = {});
    var row = all[exercise] || (all[exercise] = {});
    return row[tempo] || (row[tempo] = { answers: 0, correct: 0, streak: 0, passed: false, date: null });
  }

  Progress.tempoCell = function (exercise, tempo) {
    var cell = tempoCell(exercise, tempo);
    return {
      answers: cell.answers,
      correct: cell.correct,
      streak: cell.streak,
      passed: !!cell.passed,
      date: cell.date,
      share: cell.answers ? cell.correct / cell.answers : 0,
      need: Math.max(0, TEMPO_MIN_ANSWERS - cell.answers)
    };
  };

  /* Odpowiedź w ćwiczeniu rozumienia, z tempem, w którym padła.
     Raz zdobyte zaliczenie nie znika — cofanie go przy jednej pomyłce
     zamieniłoby mapę w licznik dobrego dnia. */
  Progress.tempoAnswer = function (exercise, tempo, correct) {
    if (!exercise || !tempo) return null;
    var cell = tempoCell(exercise, tempo);
    cell.answers += 1;
    if (correct) { cell.correct += 1; cell.streak += 1; } else { cell.streak = 0; }
    if (!cell.passed && cell.answers >= TEMPO_MIN_ANSWERS &&
        cell.correct / cell.answers >= TEMPO_MIN_SHARE) {
      cell.passed = true;
      cell.date = U.today();
    }
    Progress.save();
    return Progress.tempoCell(exercise, tempo);
  };

  /* Na którym tempie uczący się stanął w danym ćwiczeniu.
     Zwraca identyfikator tempa albo null, gdy przeszedł wszystkie trzy. */
  Progress.tempoStuckAt = function (exercise) {
    for (var i = 0; i < TEMPO_STEPS.length; i++) {
      if (!tempoCell(exercise, TEMPO_STEPS[i].id).passed) return TEMPO_STEPS[i].id;
    }
    return null;
  };

  /* Cała mapa: ćwiczenie x tempo. Ćwiczenia nietknięte też są na liście —
     brak wyniku to też informacja. */
  Progress.tempoMap = function () {
    return TEMPO_EXERCISES.map(function (ex) {
      var steps = TEMPO_STEPS.map(function (t) {
        var cell = Progress.tempoCell(ex.id, t.id);
        cell.tempo = t.id;
        cell.tempoLabel = t.label;
        return cell;
      });
      return {
        id: ex.id,
        label: ex.label,
        steps: steps,
        stuckAt: Progress.tempoStuckAt(ex.id),
        touched: steps.some(function (s) { return s.answers > 0; })
      };
    });
  };

  Progress.tempoSummary = function () {
    var passed = 0, total = 0, touched = 0;
    Progress.tempoMap().forEach(function (row) {
      if (row.touched) touched += 1;
      row.steps.forEach(function (s) {
        total += 1;
        if (s.passed) passed += 1;
      });
    });
    return { passed: passed, total: total, touched: touched };
  };

  /* ------------------------------------------- słuchanie ekstensywne */

  /* Zapisujemy oba wyniki osobno, bo różnica między nimi jest tu właściwym
     pomiarem: pierwszy przebieg mówi, ile uczący się wyłapał ze słuchu,
     trzeci — ile z tego zostało po zobaczeniu zapisu. */
  Progress.extensiveResult = function (blockId, run) {
    var box = Progress.data.extensive || (Progress.data.extensive = {});
    var entry = box[blockId] || (box[blockId] = { runs: [] });
    entry.runs.push({
      d: U.today(),
      tempo: run.tempo,
      first: run.first,          // { correct, total } — bez tekstu
      second: run.second,        // { correct, total } — z tekstem
      third: run.third           // { correct, total } — znów bez tekstu
    });
    if (entry.runs.length > 10) entry.runs = entry.runs.slice(-10);
    Progress.save();
    return entry;
  };

  Progress.extensiveOf = function (blockId) {
    return (Progress.data.extensive || {})[blockId] || null;
  };

  /* Podsumowanie po wszystkich blokach: ile rozumiane od razu, ile dopiero
     po tekście. Liczymy na ostatnim podejściu do każdego bloku. */
  Progress.extensiveSummary = function () {
    var first = { correct: 0, total: 0 };
    var third = { correct: 0, total: 0 };
    var blocks = 0;
    var box = Progress.data.extensive || {};
    Object.keys(box).forEach(function (id) {
      var runs = box[id].runs || [];
      if (!runs.length) return;
      var last = runs[runs.length - 1];
      blocks += 1;
      ['first', 'third'].forEach(function (k) {
        var target = k === 'first' ? first : third;
        if (last[k]) {
          target.correct += last[k].correct;
          target.total += last[k].total;
        }
      });
    });
    return {
      blocks: blocks,
      first: first,
      third: third,
      firstShare: first.total ? first.correct / first.total : 0,
      thirdShare: third.total ? third.correct / third.total : 0
    };
  };

  Progress.isFavourite = function (id) { return !!Progress.data.favourites[id]; };

  Progress.toggleFavourite = function (id) {
    if (Progress.data.favourites[id]) delete Progress.data.favourites[id];
    else Progress.data.favourites[id] = true;
    Progress.save();
    return Progress.isFavourite(id);
  };

  Progress.addToList = function (listName, id) {
    var list = Progress.data.lists[listName] || (Progress.data.lists[listName] = []);
    if (list.indexOf(id) === -1) list.push(id);
    Progress.save();
  };

  Progress.removeFromList = function (listName, id) {
    var list = Progress.data.lists[listName];
    if (!list) return;
    Progress.data.lists[listName] = list.filter(function (x) { return x !== id; });
    Progress.save();
  };

  Progress.summary = function () {
    var d = Progress.data;
    var todayStats = d.days[U.today()] || { answers: 0, correct: 0, minutes: 0, newWords: 0 };
    var accuracy = d.totalAnswers ? Math.round(d.totalCorrect / d.totalAnswers * 100) : 0;
    return {
      streak: d.streak,
      bestStreak: d.bestStreak,
      today: todayStats,
      goal: d.goal,
      goalDone: Math.min(100, d.goal ? Math.round(todayStats.answers / d.goal * 100) : 0),
      known: Object.keys(d.seen).length,
      accuracy: accuracy,
      minutes: Math.round(d.minutes),
      favourites: Object.keys(d.favourites).length
    };
  };

  /* Postęp w rozbiciu na poziomy i kategorie. */
  Progress.byLevel = function () {
    var out = {};
    DB.levels.forEach(function (l) { out[l] = { total: DB.countByLevel[l] || 0, seen: 0 }; });
    Object.keys(Progress.data.seen).forEach(function (id) {
      var r = DB.any(id);
      if (r && out[r.level]) out[r.level].seen += 1;
    });
    return out;
  };

  Progress.byCategory = function () {
    var out = {};
    DB.catNames.forEach(function (c) { out[c] = { total: DB.countByCat[c] || 0, seen: 0 }; });
    Object.keys(Progress.data.seen).forEach(function (id) {
      var r = DB.any(id);
      if (r && out[r.category]) out[r.category].seen += 1;
    });
    return out;
  };

  Progress.last14 = function () {
    var out = [];
    var base = new Date();
    for (var i = 13; i >= 0; i--) {
      var d = new Date(base);
      d.setDate(base.getDate() - i);
      var key = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
      out.push({ date: key, stats: Progress.data.days[key] || { answers: 0, correct: 0, minutes: 0, newWords: 0 } });
    }
    return out;
  };

  /* ------------------------------------------------- test poziomujący i kurs */

  Progress.needsPlacement = function () {
    return !Progress.data.placement;
  };

  /* Poziom wyznaczony testem. Używany do doboru materiału w Powtórkach
     i ćwiczeniach, dopóki użytkownik nie ustawi poziomu ręcznie. */
  Progress.entryLevel = function () {
    var p = Progress.data.placement;
    return p ? p.level : '';
  };

  Progress.setPlacement = function (result) {
    Progress.data.placement = {
      level: result.level,
      score: result.score,
      total: result.total,
      date: U.today(),
      entryLesson: result.entryLesson || null
    };
    Progress.save();
    return Progress.data.placement;
  };

  Progress.lessonState = function (id) {
    return Progress.data.lessons[id] || null;
  };

  Progress.isLessonDone = function (id) {
    var st = Progress.data.lessons[id];
    return !!(st && (st.status === 'passed' || st.status === 'skipped'));
  };

  Progress.setLessonResult = function (id, status, score, total) {
    Progress.data.lessons[id] = {
      status: status, score: score || 0, total: total || 0, date: U.today()
    };
    Progress.save();
  };

  /* Odpowiedź przypisana do STRONY tematu gramatycznego. Cienka warstwa nad
     js/grammar-stats.js — moduły ćwiczeń wołają Progress, tak jak wszystkie
     pozostałe, i nie muszą wiedzieć, gdzie ta liczba ostatecznie ląduje. */
  Progress.grammarAnswer = function (recordId, correct, side) {
    if (!global.GStats) return null;
    return GStats.answer(recordId, correct, side);
  };

  Progress.lessonsDone = function () {
    return Object.keys(Progress.data.lessons).filter(function (k) {
      return Progress.isLessonDone(k);
    }).length;
  };

  /* ----------------------------------------------------- czas reakcji */

  var TIME_SAMPLES = 6;      // ile prób pamiętamy na jedno hasło
  var TIME_LOG_LIMIT = 800;  // ile wpisów w dzienniku ogólnym
  var TIME_FLOOR = 400;      // poniżej tego to nie odpowiedź, tylko przypadek
  var TIME_CEILING = 60000;  // dłuższe pomiary to przerwa, nie namysł

  function median(list) {
    if (!list || !list.length) return null;
    var a = list.slice().sort(function (x, y) { return x - y; });
    var m = Math.floor(a.length / 2);
    return a.length % 2 ? a[m] : Math.round((a[m - 1] + a[m]) / 2);
  }
  Progress.median = median;

  /* Zapisuje czas jednej odpowiedzi i mówi, jak wypada na tle reszty.
     Zwraca 'fast' | 'ok' | 'slow' | null. */
  Progress.recordTime = function (id, ms, mode) {
    ms = Math.round(ms);
    if (!id || !(ms > TIME_FLOOR) || ms > TIME_CEILING) return null;
    var d = Progress.data;
    var list = d.times[id] || (d.times[id] = []);
    list.push(ms);
    if (list.length > TIME_SAMPLES) d.times[id] = list.slice(-TIME_SAMPLES);
    d.timeLog.push({ d: U.today(), ms: ms, mode: mode || '' });
    if (d.timeLog.length > TIME_LOG_LIMIT) d.timeLog = d.timeLog.slice(-TIME_LOG_LIMIT);
    Progress.save();
    return Progress.timeVerdict(ms);
  };

  /* Mediana czasu reakcji tego użytkownika. To ona jest punktem odniesienia,
     a nie żadna stała z podręcznika: ktoś, kto zawsze odpowiada w 6 sekund,
     nie ma problemu z płynnością na tym samym poziomie co ktoś, kto zwykle
     odpowiada w 2 sekundy. */
  Progress.medianTime = function (mode) {
    var log = Progress.data.timeLog || [];
    if (mode) log = log.filter(function (e) { return e.mode === mode; });
    return median(log.map(function (e) { return e.ms; }));
  };

  /* Próg powolności: półtora raza mediana, ale nie mniej niż 3,5 sekundy —
     poniżej tego nikt nie „szuka” słowa, tylko normalnie odpowiada. */
  Progress.slowThreshold = function () {
    var m = Progress.medianTime();
    if (!m) return 5000;
    return Math.max(3500, Math.round(m * 1.5));
  };

  Progress.timeVerdict = function (ms) {
    var m = Progress.medianTime();
    if (!m) return 'ok';
    if (ms > Progress.slowThreshold()) return 'slow';
    if (ms < m * 0.7) return 'fast';
    return 'ok';
  };

  Progress.itemTime = function (id) {
    return median(Progress.data.times[id] || []);
  };

  /* Hasła znane, ale odtwarzane wolno. Warunek „znane” bierzemy z kartoteki
     powtórek: hasło z trafnymi odpowiedziami i bez świeżych wpadek. Takie
     hasła nie wracają w powtórkach, bo formalnie są opanowane — a w rozmowie
     nadal się zacinają. */
  Progress.slowItems = function (limit) {
    var threshold = Progress.slowThreshold();
    var cards = (global.SRS && SRS.cards) || {};
    var out = [];
    Object.keys(Progress.data.times).forEach(function (id) {
      var samples = Progress.data.times[id];
      if (!samples || samples.length < 2) return;
      var m = median(samples);
      if (m <= threshold) return;
      /* Czas reakcji mierzymy w ćwiczeniach produkcyjnych, więc „znane”
         sprawdzamy na stronie wytworzenia; gdy jej nie ma (hasło dodane samym
         rozpoznaniem), bierzemy tę, która istnieje. Przed rozdzieleniem kart
         wystarczał tu goły identyfikator — teraz karta ma stronę i wyszukanie
         po samym haśle zawsze zwracałoby pustkę. */
      var c = (global.SRS && SRS.cards)
        ? (SRS.cards[SRS.cardId(id, 'p')] || SRS.cards[SRS.cardId(id, 'r')] || cards[id])
        : cards[id];
      var known = c ? (c.repetitions >= 1 && c.correct >= 1 && c.correct / Math.max(1, c.seen) >= 0.5)
                    : (Progress.data.seen[id] || 0) >= 2;
      if (!known) return;
      out.push({ id: id, ms: m, samples: samples.length, threshold: threshold });
    });
    out.sort(function (a, b) { return b.ms - a.ms; });
    return out.slice(0, limit || 12);
  };

  Progress.timeStats = function () {
    var log = Progress.data.timeLog || [];
    var all = log.map(function (e) { return e.ms; });
    var byMode = {};
    log.forEach(function (e) {
      if (!e.mode) return;
      (byMode[e.mode] || (byMode[e.mode] = [])).push(e.ms);
    });
    Object.keys(byMode).forEach(function (k) {
      byMode[k] = { median: median(byMode[k]), count: byMode[k].length };
    });
    return {
      median: median(all),
      count: all.length,
      threshold: Progress.slowThreshold(),
      byMode: byMode,
      slow: Progress.slowItems(12).length
    };
  };

  /* ------------------------------------------------------- liczby (sesja T) */

  /* Ile ostatnich pomiarów pamiętamy na tryb. Sześćdziesiąt to około trzech
     sesji ćwiczeń — dość, żeby mediana była stabilna, za mało, żeby postęp
     sprzed miesiąca zasłaniał dzisiejszy stan. */
  var NUM_SAMPLES = 60;

  /* Próg opanowania. Nie jest wzięty z podręcznika: bierze się z tego, ile
     czasu ma człowiek w kasie, zanim rozmowa przejdzie dalej — a to jest
     mniej więcej dwie i pół sekundy. Wartość bazowa siedzi w danych
     (`masteryMs` przy każdym ćwiczeniu), tutaj tylko awaryjna. */
  var NUM_MASTERY_FALLBACK = 3000;

  /* Tryby, w których materiał przychodzi UCHEM. Tylko one liczą się do
     drabiny tempa — w produkcji i w liczeniu reszty tempo odsłuchu nie
     opisuje niczego. */
  var LISTENING_NUMBER_MODES = ['dictation', 'price', 'clock', 'sequence'];

  function numCell(mode) {
    var all = Progress.data.numbers || (Progress.data.numbers = {});
    return all[mode] || (all[mode] = { answers: 0, correct: 0, timeouts: 0, times: [] });
  }

  function numMastery(mode) {
    var def = (global.Numbers && Numbers.drillDef) ? Numbers.drillDef(mode) : null;
    return (def && def.masteryMs) || NUM_MASTERY_FALLBACK;
  }

  /* Odpowiedź w ćwiczeniu liczbowym. Zwraca zdanie do pokazania pod wynikiem —
     bo sama liczba milisekund nie mówi uczącemu się, czy to dobrze, czy źle. */
  Progress.numberAnswer = function (mode, correct, ms, context) {
    context = context || {};
    var cell = numCell(mode);
    cell.answers += 1;
    if (correct) cell.correct += 1;
    if (context.timedOut) cell.timeouts += 1;
    /* Do mediany czasu wchodzą wyłącznie odpowiedzi TRAFNE. Czas pomyłki
       mierzy, jak długo ktoś się wahał, zanim wybrał źle — to jest inna
       wielkość i wrzucona do jednego worka zaniża albo zawyża medianę
       zależnie od tego, czy uczący się zgaduje szybko, czy wolno. */
    if (ms > 0 && correct) {
      cell.times.push(Math.round(ms));
      if (cell.times.length > NUM_SAMPLES) cell.times = cell.times.slice(-NUM_SAMPLES);
    }
    /* Liczby ze słuchu wchodzą do drabiny tempa jako jedno pole, nie jako
       sześć. Trzy tryby na sześć są produkcyjne albo rachunkowe i tempo
       odsłuchu nic w nich nie znaczy — osobne kolumny dla nich byłyby na
       mapie miejscem, którego nigdy nie da się zaliczyć. */
    if (LISTENING_NUMBER_MODES.indexOf(mode) !== -1 && global.CompTempo) {
      Progress.tempoAnswer('numbers', CompTempo.current, !!correct);
    }
    Progress.registerActivity();
    Progress.save();

    var note;
    var target = numMastery(mode);
    if (context.timedOut) {
      note = 'Brak odpowiedzi w oknie liczy się jak pomyłka — w sklepie też się tak liczy.';
    } else if (!correct) {
      note = 'Najpierw trafność, potem tempo. Czas liczy się dopiero od trafnych odpowiedzi.';
    } else if (ms <= target) {
      note = 'To jest tempo rozmowy: poniżej ' + (target / 1000).toFixed(1).replace('.', ',') + ' s.';
    } else {
      note = 'Trafnie, ale wolno. Próg opanowania to '
        + (target / 1000).toFixed(1).replace('.', ',') + ' s — powyżej niego rozmówca '
        + 'zdąży powtórzyć albo pokazać na palcach.';
    }
    return { note: note, median: median(cell.times), target: target };
  };

  Progress.numberStats = function () {
    var all = Progress.data.numbers || {};
    var rows = [], answers = 0, correct = 0, timeouts = 0, times = [];
    Object.keys(all).forEach(function (mode) {
      var c = all[mode];
      answers += c.answers; correct += c.correct; timeouts += c.timeouts || 0;
      times = times.concat(c.times || []);
      var target = numMastery(mode);
      var med = median(c.times || []);
      rows.push({
        mode: mode,
        label: (global.Numbers && Numbers.drillDef(mode) && Numbers.drillDef(mode).label) || mode,
        answers: c.answers, correct: c.correct, timeouts: c.timeouts || 0,
        share: c.answers ? c.correct / c.answers : 0,
        median: med, target: target,
        mastered: !!(med && med <= target && c.answers >= 10 && c.correct / c.answers >= 0.8)
      });
    });
    rows.sort(function (a, b) { return b.answers - a.answers; });
    return {
      answers: answers, correct: correct, timeouts: timeouts,
      share: answers ? correct / answers : 0,
      median: median(times), rows: rows,
      mastered: rows.filter(function (r) { return r.mastered; }).length
    };
  };

  /* -------------------------------------------------- odruch ratunkowy */

  function reflexCell(trigger) {
    var all = Progress.data.reflex || (Progress.data.reflex = {});
    return all[trigger] || (all[trigger] = {
      answers: 0, correct: 0, frozen: 0, times: [], repaired: 0, repairTries: 0
    });
  }

  var REFLEX_MASTERY = 1800;

  Progress.reflexAnswer = function (trigger, correct, ms, frozen) {
    var cell = reflexCell(trigger);
    cell.answers += 1;
    if (correct) cell.correct += 1;
    if (frozen) cell.frozen += 1;
    if (ms > 0 && correct) {
      cell.times.push(Math.round(ms));
      if (cell.times.length > NUM_SAMPLES) cell.times = cell.times.slice(-NUM_SAMPLES);
    }
    Progress.registerActivity();
    Progress.save();
    var note;
    if (frozen) note = 'Zamarcie. To jest ta reakcja, którą ten dryl ma zastąpić.';
    else if (!correct) note = 'Formuła nie na tę sytuację — ale reakcja była, i to się liczy.';
    else if (ms <= REFLEX_MASTERY) note = 'Odruch. Poniżej 1,8 s formuła pada, zanim rozmowa zdąży się urwać.';
    else note = 'Trafnie, ale z namysłem. Odruch zaczyna się poniżej 1,8 s.';
    return { note: note, median: median(cell.times) };
  };

  Progress.reflexRepair = function (trigger, ok) {
    var cell = reflexCell(trigger);
    cell.repairTries += 1;
    if (ok) cell.repaired += 1;
    Progress.save();
  };

  /* Czy uczący się REAGUJE, czy ZAMIERA — i czy jego reakcja coś daje.
     To są dwie różne liczby i mieszanie ich w jedną zaciera właśnie tę
     różnicę, o którą w tym module chodzi. */
  Progress.reflexStats = function () {
    var all = Progress.data.reflex || {};
    var rows = [], answers = 0, correct = 0, frozen = 0, times = [];
    var repaired = 0, repairTries = 0;
    Object.keys(all).forEach(function (t) {
      var c = all[t];
      answers += c.answers; correct += c.correct; frozen += c.frozen || 0;
      repaired += c.repaired || 0; repairTries += c.repairTries || 0;
      times = times.concat(c.times || []);
      var def = null;
      if (global.Rescue && Rescue.triggers) {
        Rescue.triggers().forEach(function (d) { if (d.id === t) def = d; });
      }
      rows.push({
        trigger: t, label: (def && def.label) || t,
        answers: c.answers, correct: c.correct, frozen: c.frozen || 0,
        share: c.answers ? c.correct / c.answers : 0,
        frozenShare: c.answers ? (c.frozen || 0) / c.answers : 0,
        median: median(c.times || []),
        repaired: c.repaired || 0, repairTries: c.repairTries || 0
      });
    });
    rows.sort(function (a, b) { return b.frozenShare - a.frozenShare || b.answers - a.answers; });
    return {
      answers: answers, correct: correct, frozen: frozen,
      frozenShare: answers ? frozen / answers : 0,
      share: answers ? correct / answers : 0,
      median: median(times), mastery: REFLEX_MASTERY,
      repaired: repaired, repairTries: repairTries,
      repairShare: repairTries ? repaired / repairTries : 0,
      rows: rows
    };
  };

  /* --------------------------------------------------- statystyka błędów */

  /* Obszary posortowane od najsłabszego. Obszar poniżej progu prób jest
     pomijany — trzy pomyłki z trzech prób to nie jest wiedza o użytkowniku,
     tylko przypadek. */
  Progress.weakAreas = function (bucket, minAnswers) {
    var src = Progress.data.errors[bucket] || {};
    var min = minAnswers || 5;
    return Object.keys(src).map(function (key) {
      var b = src[key];
      return {
        key: key,
        answers: b.answers,
        wrong: b.wrong,
        rate: b.answers ? Math.round(b.wrong / b.answers * 100) : 0
      };
    }).filter(function (x) { return x.answers >= min; })
      .sort(function (a, b) { return b.rate - a.rate || b.wrong - a.wrong; });
  };

  /* Najsłabszy obszar w ogóle — z podpowiedzią, które ćwiczenie go naprawi. */
  var MODE_FOR_CATEGORY = {
    'Liczby i liczenie': { screen: U.exScreen('classifier'), mode: 'classifier', label: U.exShort('classifier') },
    'Podstawy i grzeczność': { screen: U.exScreen('type'), mode: 'type', label: U.exShort('type') },
    'Pytania': { screen: U.exScreen('build'), mode: 'build', label: U.exShort('build') }
  };

  Progress.worstArea = function () {
    var cats = Progress.weakAreas('category', 6);
    var grams = Progress.weakAreas('grammar', 6);
    var modes = Progress.weakAreas('mode', 6);

    var best = null;
    if (cats.length) best = { kind: 'category', item: cats[0] };
    if (grams.length && (!best || grams[0].rate > best.item.rate)) best = { kind: 'grammar', item: grams[0] };
    if (modes.length && (!best || modes[0].rate > best.item.rate)) best = { kind: 'mode', item: modes[0] };
    if (!best) return null;

    var suggestion;
    if (best.kind === 'grammar') {
      suggestion = { screen: U.exScreen('build'), mode: 'build', label: U.exShort('build') };
    } else if (best.kind === 'mode') {
      suggestion = { screen: U.exScreen(best.item.key) || 'produce', mode: best.item.key,
        label: U.exShort(best.item.key) + ' jeszcze raz' };
    } else {
      suggestion = MODE_FOR_CATEGORY[best.item.key]
        || { screen: U.exScreen('build'), mode: 'build', label: U.exShort('build') };
    }
    best.suggestion = suggestion;
    return best;
  };

  /* ------------------------------------------------ percepcja: kontrasty */

  var PERC_LOG_LIMIT = 1500;

  /* Jedna odpowiedź w ćwiczeniu percepcyjnym. Nie przechodzi przez
     Progress.answer, bo tam kluczem jest identyfikator rekordu, a tutaj liczy
     się kontrast — ten sam wyraz raz sprawdza ton, a raz długość samogłoski. */
  Progress.perceptionAnswer = function (contrastId, correct) {
    if (!contrastId) return;
    Progress.registerActivity();
    var p = Progress.data.perception;
    var box = p.contrasts[contrastId] || (p.contrasts[contrastId] = { answers: 0, correct: 0 });
    box.answers += 1;
    if (correct) box.correct += 1;
    p.history.push({ d: U.today(), c: contrastId, ok: correct ? 1 : 0 });
    if (p.history.length > PERC_LOG_LIMIT) p.history = p.history.slice(-PERC_LOG_LIMIT);

    /* Odpowiedzi percepcyjne liczą się też do celu dnia — to jest nauka,
       nie rozgrzewka. */
    var day = Progress.day();
    day.answers += 1;
    Progress.data.totalAnswers += 1;
    if (correct) { day.correct += 1; Progress.data.totalCorrect += 1; }
    bump(Progress.data.errors.mode, 'percepcja', correct);
    Progress.save();
  };

  /* Skuteczność per kontrast, od najsłabszego. Kontrast z małą liczbą prób
     jest oznaczony, ale nie wypada z listy — w module 0 kilka kontrastów ma
     z natury mniej materiału i cisza o nich byłaby myląca. */
  Progress.contrastStats = function (minAnswers) {
    var min = minAnswers || 4;
    var src = Progress.data.perception.contrasts || {};
    return Object.keys(src).map(function (cid) {
      var b = src[cid];
      return {
        id: cid,
        answers: b.answers,
        correct: b.correct,
        rate: b.answers ? Math.round(b.correct / b.answers * 100) : 0,
        reliable: b.answers >= min
      };
    }).sort(function (a, b) {
      if (a.reliable !== b.reliable) return a.reliable ? -1 : 1;
      return a.rate - b.rate || b.answers - a.answers;
    });
  };

  /* Najsłabszy kontrast — ten, od którego warto zacząć następną sesję. */
  Progress.weakestContrast = function (minAnswers) {
    var list = Progress.contrastStats(minAnswers).filter(function (x) { return x.reliable; });
    return list.length ? list[0] : null;
  };

  /* Historia jednego kontrastu w czasie: skuteczność w kolejnych porcjach
     po `chunk` odpowiedzi. Wykres po dniach byłby dziurawy — nikt nie ćwiczy
     każdego kontrastu codziennie. */
  Progress.contrastHistory = function (contrastId, chunk) {
    var size = chunk || 5;
    var log = (Progress.data.perception.history || []).filter(function (e) {
      return !contrastId || e.c === contrastId;
    });
    var out = [];
    for (var i = 0; i < log.length; i += size) {
      var part = log.slice(i, i + size);
      if (part.length < Math.min(size, 3) && out.length) break;
      var ok = part.reduce(function (n, e) { return n + e.ok; }, 0);
      out.push({
        from: part[0].d, to: part[part.length - 1].d,
        answers: part.length,
        rate: Math.round(ok / part.length * 100)
      });
    }
    return out;
  };

  Progress.perceptionSummary = function () {
    var p = Progress.data.perception;
    var answers = 0, correct = 0;
    Object.keys(p.contrasts).forEach(function (k) {
      answers += p.contrasts[k].answers;
      correct += p.contrasts[k].correct;
    });
    return {
      answers: answers,
      correct: correct,
      accuracy: answers ? Math.round(correct / answers * 100) : 0,
      contrasts: Object.keys(p.contrasts).length,
      diagnostic: p.diagnostic || null,
      skipped: !!p.skipped
    };
  };

  /* ----------------------------------------------------- egzaminy poziomowe */

  /* Ile podejść pamiętamy na poziom. Dwanaście to cztery pełne obiegi trzech
     zestawów — dłuższa historia niczego już nie mówi, a puchnie w kopii. */
  var EXAM_LIMIT = 12;

  function examBox(level) {
    var d = Progress.data;
    if (!d.exams[level]) d.exams[level] = { attempts: [], passedAt: null, bestAt: null };
    return d.exams[level];
  }
  Progress.examBox = examBox;

  Progress.examAttempts = function (level) {
    return examBox(level).attempts.slice();
  };

  /* Najlepsze podejście: liczy się liczba ZALICZONYCH SPRAWNOŚCI, a dopiero
     przy remisie najsłabsza z nich. Sortowanie po średniej postawiłoby wyżej
     wynik nierówny (dwie sprawności świetnie, dwie fatalnie) niż równy —
     a to jest dokładnie odwrotnie, niż mówi ten egzamin. */
  function attemptRank(a) {
    if (!a || a.abandoned || !a.sections) return [-1, -1];
    var ids = ['listening', 'detail', 'speaking', 'writing'];
    var passed = 0, worst = 100;
    ids.forEach(function (id) {
      var s = a.sections[id];
      if (!s) return;
      if (s.passed) passed += 1;
      var value = id === 'speaking' ? Math.min(s.tone, s.content) : s.pct;
      if (value < worst) worst = value;
    });
    return [passed, worst];
  }
  Progress.attemptRank = attemptRank;

  Progress.bestExam = function (level) {
    var best = null, bestRank = [-1, -1];
    examBox(level).attempts.forEach(function (a) {
      var r = attemptRank(a);
      if (r[0] > bestRank[0] || (r[0] === bestRank[0] && r[1] > bestRank[1])) {
        best = a; bestRank = r;
      }
    });
    return best;
  };

  Progress.examPassed = function (level) {
    return examBox(level).attempts.some(function (a) { return a.passed; });
  };

  Progress.saveExamAttempt = function (attempt) {
    var box = examBox(attempt.level);
    box.attempts.push(attempt);
    while (box.attempts.length > EXAM_LIMIT) box.attempts.shift();
    if (attempt.passed && !box.passedAt) box.passedAt = attempt.date;
    Progress.registerActivity();
    Progress.save();
    return attempt;
  };

  /* Najwyższy zdany poziom — to, co idzie na certyfikat. Nie „poziom, na
     którym jestem”, tylko „poziom, który udowodniłem”. */
  Progress.certifiedLevel = function () {
    var order = ['Survival', 'A1', 'A2', 'B1', 'B2'];
    var out = null;
    order.forEach(function (l) { if (Progress.examPassed(l)) out = l; });
    return out;
  };

  Progress.examSummary = function () {
    var order = ['Survival', 'A1', 'A2', 'B1', 'B2'];
    return order.map(function (level) {
      var box = Progress.data.exams[level];
      var attempts = box ? box.attempts : [];
      var real = attempts.filter(function (a) { return !a.abandoned; });
      return {
        level: level,
        attempts: attempts.length,
        completed: real.length,
        abandoned: attempts.length - real.length,
        passed: Progress.examPassed(level),
        passedAt: box ? box.passedAt : null,
        best: Progress.bestExam(level)
      };
    });
  };

  /* ------------------------------------------------------ próbki kontrolne */

  function checkpointBox(id) {
    var d = Progress.data;
    if (!d.checkpoints[id]) d.checkpoints[id] = { attempts: [], best: null, lastDate: null };
    return d.checkpoints[id];
  }

  Progress.checkpointOf = function (id) {
    return Progress.data.checkpoints[id] || null;
  };

  Progress.saveCheckpoint = function (result) {
    var box = checkpointBox(result.id);
    box.attempts.push(result);
    while (box.attempts.length > 6) box.attempts.shift();
    if (box.best === null || result.pct > box.best) box.best = result.pct;
    box.lastDate = result.date;
    Progress.registerActivity();
    Progress.save();
    return result;
  };

  Progress.checkpointSummary = function () {
    var out = [];
    Object.keys(Progress.data.checkpoints).forEach(function (id) {
      var box = Progress.data.checkpoints[id];
      var last = box.attempts[box.attempts.length - 1];
      if (last) out.push(last);
    });
    out.sort(function (a, b) { return a.triggerLesson - b.triggerLesson; });
    return out;
  };

  /* ------------------------------------------------------ eksport / import */
  Progress.exportData = function () {
    return {
      app: 'Thai All-in-One',
      formatVersion: 1,
      exportedAt: new Date().toISOString(),
      dataVersion: DB.manifest ? DB.manifest.version : null,
      progress: Progress.data,
      srs: SRS.cards,
      /* Dziennik powtórek i dostrojenie odstępów wychodzą razem z kartoteką.
         Bez nich kopia odtworzyłaby karty, ale pętla zwrotna zaczynałaby od
         zera i przez pierwsze tygodnie po imporcie liczyłaby odstępy tak,
         jakby ten uczący się nie miał żadnej historii. */
      srsLog: SRS.log,
      srsTuning: SRS.tuning,
      settings: U.store.get('settings', {})
    };
  };

  Progress.download = function () {
    var payload = JSON.stringify(Progress.exportData(), null, 2);
    var blob = new Blob([payload], { type: 'application/json;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var a = U.el('a', { href: url, download: 'thai-all-in-one-postep-' + U.today() + '.json' });
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
  };

  Progress.importData = function (json) {
    if (!json || json.app !== 'Thai All-in-One' || !json.progress) {
      throw new Error('To nie jest plik kopii aplikacji Thai All-in-One.');
    }
    Progress.data = Object.assign(blank(), json.progress);
    if (!Array.isArray(Progress.data.misses)) Progress.data.misses = [];
    if (!Progress.data.exams) Progress.data.exams = {};
    if (!Progress.data.checkpoints) Progress.data.checkpoints = {};
    SRS.cards = json.srs || {};
    if (Array.isArray(json.srsLog)) SRS.log = json.srsLog;
    if (json.srsTuning) SRS.tuning = json.srsTuning;
    if (json.settings) U.store.set('settings', json.settings);
    Progress.save();
    SRS.save();
    /* Kopia sprzed rozdzielenia kart niesie karty bez stron — po wczytaniu
       przechodzi tę samą migrację co kartoteka lokalna. */
    SRS.migrateSides();
    return true;
  };

  global.Progress = Progress;
})(window);
