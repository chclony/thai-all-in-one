/* Thai All-in-One — migracja postępu po przebudowie ścieżki (sesja O).

   PROBLEM
   -------
   Ścieżka została przeliczona od nowa: 314 lekcji po niecałe cztery hasła
   zamieniło się w 333 lekcje po dziewięć. Dziewięćdziesiąt pięć lekcji
   zachowało identyfikator, bo większość ich materiału trafiła w całości do
   jednej nowej lekcji. Pozostałe 238 nowych lekcji nie ma jednego
   poprzednika — każda jest spadkobierczynią mniej więcej dwóch starych.

   Bez migracji zapisany stan nie znika, tylko przestaje na cokolwiek
   wskazywać: użytkownik po stu lekcjach widzi kurs otwarty na pierwszej.

   ROZWIĄZANIE — DWA TORY
   ----------------------
   1. TOR PROSTY. Lekcja, która zachowała identyfikator, przejmuje stan
      jeden do jednego: status, wynik i datę. Nic nie liczymy.

   2. TOR PRZELICZENIA. Dla reszty pytamy o rzecz, która naprawdę ma
      znaczenie: ile haseł nowej lekcji uczący się już przerobił. Sumujemy
      hasła (`newWordIds`) wszystkich starych lekcji zaliczonych albo
      świadomie pominiętych — to jest jego ZNANY ZASÓB. Nowa lekcja, której
      zasób pokrywa co najmniej 80 procent haseł, jest uznana za przerobioną.

      Status ustawiamy na 'skipped', nie 'passed'. To nie jest drobiazg:
      'passed' niesie wynik sprawdzianu, którego nikt nie pisał, i zafałszowałby
      statystyki trafności. 'skipped' istnieje w aplikacji dokładnie po to,
      żeby powiedzieć „ten materiał jest już znany” — odblokowuje ścieżkę
      i nie udaje egzaminu.

   3. REGUŁA PREFIKSU. Zaliczamy tylko nieprzerwany początek nowej ścieżki.
      Stara ścieżka była zamknięta na klucz — lekcja otwierała się po
      zaliczeniu poprzedniej — więc zaliczone lekcje zawsze tworzyły prefiks.
      Obie ścieżki wprowadzają hasła w tej samej kolejności (poziom,
      częstość, trudność), więc pokrycie też układa się w prefiks. Gdyby
      gdzieś w środku wypadła dziura, oznacza to realną lukę w materiale
      i lepiej, żeby użytkownik tę lekcję przerobił, niż żeby dostał ją
      za darmo. Lekcje z toru prostego przechodzą niezależnie od prefiksu —
      tam mamy twarde dopasowanie, nie oszacowanie.

   JEDNORAZOWOŚĆ I ODWRACALNOŚĆ
   ----------------------------
   Migracja zostawia w postępie znacznik `migration` z wersją. Przy każdym
   starcie sprawdzamy znacznik i nie ruszamy stanu drugi raz. Przed
   zmianą całość postępu ląduje w osobnym kluczu kopii zapasowej —
   `ProgressMigration.restore()` przywraca stan sprzed migracji i kasuje
   znacznik. Ustawienia mają na to przycisk.

   CISZA
   -----
   Migracja nie pyta i nie przerywa. Użytkownik ma po aktualizacji zobaczyć
   swój kurs w miejscu, w którym go zostawił — to jest cały oczekiwany
   efekt. Raport z tego, co się stało, leży w Ustawieniach dla tych, którzy
   chcą sprawdzić. */
(function (global) {
  'use strict';

  var M = {};

  /* Wersja migracji, nie wersja aplikacji. Rośnie tylko wtedy, gdy ścieżka
     jest przebudowywana na nowo i stary przelicznik przestaje pasować. */
  var MIGRATION_VERSION = 'o-2026-08';
  var BACKUP_KEY = 'progress-backup-' + MIGRATION_VERSION;
  var COVERAGE = 0.8;

  M.map = null;          // zawartość data/progress-migration.json
  M.lastReport = null;

  M.setMap = function (json) { M.map = json || null; };

  M.needed = function () {
    if (!M.map || !global.Progress || !Progress.data) return false;
    var d = Progress.data;
    if (d.migration && d.migration.version === MIGRATION_VERSION) return false;
    /* Nowy użytkownik nie ma czego migrować. Zapisujemy mu tylko znacznik,
       żeby przy kolejnym starcie nie liczyć tego od nowa. */
    return true;
  };

  function doneOldLessons(d) {
    var out = [];
    Object.keys(d.lessons || {}).forEach(function (id) {
      var st = d.lessons[id];
      if (st && (st.status === 'passed' || st.status === 'skipped')) out.push(id);
    });
    return out;
  }

  /* Zbiór haseł, które uczący się przerobił w starej ścieżce. */
  function knownWords(d) {
    var known = Object.create(null), n = 0;
    var legacy = M.map.legacy || {};
    doneOldLessons(d).forEach(function (id) {
      var words = legacy[id];
      if (!words) return;
      for (var i = 0; i < words.length; i++) {
        if (!known[words[i]]) { known[words[i]] = true; n += 1; }
      }
    });
    return { set: known, count: n };
  }

  function coverage(lesson, known) {
    var ids = lesson.newWordIds || [];
    if (!ids.length) return 0;
    var hit = 0;
    for (var i = 0; i < ids.length; i++) if (known[ids[i]]) hit += 1;
    return hit / ids.length;
  }

  /* Właściwa migracja. Zwraca raport; nie rysuje niczego na ekranie. */
  M.run = function () {
    if (!M.needed()) return null;

    var d = Progress.data;
    var lessons = (global.DB && DB.lessons) || [];
    var oldDone = doneOldLessons(d);

    var report = {
      version: MIGRATION_VERSION,
      date: (global.U && U.today) ? U.today() : new Date().toISOString().slice(0, 10),
      oldDone: oldDone.length,
      direct: 0,
      derived: 0,
      knownWords: 0,
      newTotal: lessons.length,
      backup: false
    };

    /* Nic do przeniesienia — zostawiamy sam znacznik i wychodzimy.
       Bez kopii zapasowej, bo nie ma czego zapisywać. */
    if (!oldDone.length || !lessons.length) {
      d.migration = report;
      Progress.save();
      M.lastReport = report;
      return report;
    }

    /* KOPIA ZAPASOWA — przed jakąkolwiek zmianą stanu. */
    try {
      U.store.set(BACKUP_KEY, {
        savedAt: new Date().toISOString(),
        version: MIGRATION_VERSION,
        progress: JSON.parse(JSON.stringify(d))
      });
      report.backup = true;
    } catch (e) {
      /* Brak miejsca w pamięci lokalnej. Migracja bez możliwości cofnięcia
         byłaby złym interesem — odpuszczamy i spróbujemy przy następnym
         starcie, gdy użytkownik zwolni miejsce. */
      return null;
    }

    var known = knownWords(d);
    report.knownWords = known.count;

    var oldState = d.lessons || {};
    var next = {};

    /* --- tor 1: identyfikatory zachowane ------------------------------- */
    var direct = M.map.direct || {};
    Object.keys(direct).forEach(function (oldId) {
      var st = oldState[oldId];
      if (!st) return;
      var newId = direct[oldId];
      next[newId] = {
        status: st.status,
        score: st.score || 0,
        total: st.total || 0,
        date: st.date || report.date,
        source: 'migracja-bezpośrednia'
      };
      report.direct += 1;
    });

    /* --- tor 2: przeliczenie po hasłach, regułą prefiksu ---------------- */
    for (var i = 0; i < lessons.length; i++) {
      var L = lessons[i];
      if (next[L.id]) continue;                    // już przeniesiona torem 1
      if (coverage(L, known.set) < COVERAGE) break; // koniec prefiksu
      next[L.id] = {
        status: 'skipped',
        score: 0,
        total: (L.recordIds || []).length,
        date: report.date,
        source: 'migracja-przeliczenie'
      };
      report.derived += 1;
    }

    d.lessons = next;
    d.migration = report;
    Progress.save();
    M.lastReport = report;
    return report;
  };

  /* --------------------------------------------------------- odwracanie */

  M.hasBackup = function () {
    return !!U.store.get(BACKUP_KEY, null);
  };

  M.backupInfo = function () {
    var b = U.store.get(BACKUP_KEY, null);
    if (!b) return null;
    return {
      savedAt: b.savedAt,
      lessons: Object.keys((b.progress && b.progress.lessons) || {}).length
    };
  };

  /* Przywraca postęp sprzed migracji. Znacznik znika razem ze stanem, więc
     przy kolejnym starcie migracja wykona się ponownie — to jest zamierzone:
     cofnięcie ma wrócić do punktu wyjścia, a nie zamrozić stary układ na
     nowej ścieżce, w której te identyfikatory już nic nie znaczą. Kto chce
     zostać przy starym stanie, cofa i eksportuje plik. */
  M.restore = function () {
    var b = U.store.get(BACKUP_KEY, null);
    if (!b || !b.progress) return false;
    Progress.data = b.progress;
    delete Progress.data.migration;
    Progress.save();
    U.store.remove(BACKUP_KEY);
    M.lastReport = null;
    return true;
  };

  /* ================= MIGRACJA UKŁADU EKRANÓW (sesja VI) ==================

     PROBLEM
     -------
     Porządkowanie nawigacji zlikwidowało ekran `phrases`: nie miał własnych
     danych ani własnego ćwiczenia, był filtrem nad tym samym indeksem, którym
     żyje Słownik. Jego treść wróciła do `dict` jako gotowy zestaw („Zwroty”,
     „Tryb wyjazdowy”), więc nic nie ubyło — ale identyfikator zniknął.

     Zapisany stan trzyma identyfikatory ekranów w trzech miejscach: w planie
     przerwanej sesji dnia (`session`), w zapamiętanej rekomendacji tygodnia
     (`goals`) i w podpowiedzi najsłabszego obszaru wewnątrz postępu. Zostawiony
     tam `phrases` nie wywala aplikacji — App.go odsyła nieznany ekran na
     „Dzisiaj” — ale to jest właśnie najgorszy wariant: przycisk „Ćwicz zwroty”
     działa i wyrzuca gdzie indziej, bez śladu, że coś poszło nie tak.

     Identyfikatory TRYBÓW nie zmieniły się ani razu. Zmieniły się wyłącznie
     ich nazwy, a nazwy nigdy nie były zapisywane — w postępie leżą klucze
     (`build`, `assemble`, `say`), nie etykiety. Dzięki temu cała statystyka
     błędów, drabina tempa i kartoteka SRS przechodzą bez tknięcia. Gdyby było
     odwrotnie, ta migracja musiałaby przepisywać `errors.mode`, a każde takie
     przepisanie miesza dane sprzed zmiany z danymi po niej.

     Migracja jest osobna od tej ze ścieżki (sesja O) i ma własny znacznik:
     obie muszą móc wykonać się niezależnie, w dowolnej kolejności i tylko raz.
     Kopii zapasowej tu nie robimy — podmiana jednego identyfikatora ekranu
     jest odwracalna wprost, a druga kopia całego postępu przy każdym starcie
     kosztowałaby więcej miejsca, niż jest warta. */

  var SCREEN_VERSION = 'vi-2026-08';
  var SCREEN_MAP = { phrases: 'dict' };

  M.SCREEN_MAP = SCREEN_MAP;
  M.SCREEN_VERSION = SCREEN_VERSION;

  /* Podmiana w miejscu, rekurencyjnie po zapisanym obiekcie. Szukamy pola
     `screen`, bo tylko ono niesie identyfikator ekranu — nie przeglądamy
     wszystkich napisów, żeby nie podmienić przypadkiem kategorii ani tytułu
     lekcji, w którym słowo „phrases” mogłoby wystąpić jako zwykły tekst. */
  function rewriteScreens(node, stats) {
    if (!node || typeof node !== 'object') return;
    if (Object.prototype.toString.call(node) === '[object Array]') {
      for (var i = 0; i < node.length; i++) rewriteScreens(node[i], stats);
      return;
    }
    Object.keys(node).forEach(function (k) {
      var v = node[k];
      if (k === 'screen' && typeof v === 'string' && SCREEN_MAP[v]) {
        node[k] = SCREEN_MAP[v];
        stats.changed += 1;
      } else if (v && typeof v === 'object') {
        rewriteScreens(v, stats);
      }
    });
  }

  M.screensNeeded = function () {
    if (!global.Progress || !Progress.data) return false;
    var m = Progress.data.screenMigration;
    return !(m && m.version === SCREEN_VERSION);
  };

  /* Uruchamiana przy starcie, obok M.run(). Zwraca raport albo null. */
  M.runScreens = function () {
    if (!M.screensNeeded()) return null;
    var stats = { changed: 0 };

    /* 1. postęp — podpowiedzi najsłabszego obszaru i cokolwiek jeszcze
          zdążyło tam wpaść z polem `screen`. */
    rewriteScreens(Progress.data, stats);

    /* 2. przerwana sesja dnia — plan zawiera bloki z ekranem docelowym. */
    var sess = U.store.get('session', null);
    if (sess) { rewriteScreens(sess, stats); U.store.set('session', sess); }

    /* 3. cel i rekomendacja tygodnia. */
    var goals = U.store.get('goals', null);
    if (goals) { rewriteScreens(goals, stats); U.store.set('goals', goals); }

    var report = {
      version: SCREEN_VERSION,
      date: (global.U && U.today) ? U.today() : new Date().toISOString().slice(0, 10),
      changed: stats.changed
    };
    Progress.data.screenMigration = report;
    Progress.save();
    return report;
  };

  M.screenSummary = function () {
    var r = (global.Progress && Progress.data && Progress.data.screenMigration) || null;
    if (!r) return 'Migracja układu ekranów jeszcze nie przebiegła.';
    if (!r.changed) return 'Migracja układu ekranów z ' + r.date + ': nie było czego poprawiać.';
    return 'Migracja układu ekranów z ' + r.date + ': poprawiono ' + r.changed + ' '
      + U.plural(r.changed, 'odwołanie', 'odwołania', 'odwołań') + ' do usuniętego ekranu.';
  };

  M.report = function () {
    return (global.Progress && Progress.data && Progress.data.migration) || null;
  };

  M.summary = function () {
    var r = M.report();
    if (!r) return 'Migracja postępu nie była potrzebna.';
    if (!r.oldDone) return 'Migracja postępu: nie było czego przenosić.';
    return 'Migracja postępu z ' + r.date + ': przeniesiono ' + r.oldDone +
      ' zaliczonych lekcji starej ścieżki na ' + (r.direct + r.derived) +
      ' lekcji nowej (' + r.direct + ' po identyfikatorze, ' + r.derived +
      ' przeliczonych przez ' + r.knownWords + ' znanych haseł).';
  };

  global.ProgressMigration = M;
})(window);
