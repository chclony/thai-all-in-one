/* Thai All-in-One — historia i retrospekcja tygodnia.

   PO CO
   =====
   Ekran „Postęp” pokazuje kilkanaście wykresów i tabel. To jest dobre, gdy
   ktoś chce coś sprawdzić, i bezużyteczne, gdy ktoś chce wiedzieć, jak mu
   idzie. Retrospekcja odpowiada na cztery pytania i nie zadaje piątego:

     co zrobione   — ile czasu, ile odpowiedzi, ile sesji, ile lekcji
     gdzie postęp  — co urosło względem poprzedniego tygodnia
     gdzie stój    — co nie drgnęło albo się cofnęło
     co dalej      — JEDNA rekomendacja, nie lista

   Jedna rekomendacja jest tu zasadą, nie skrótem. Lista pięciu rzeczy do
   poprawy to znowu decyzja do podjęcia — czyli dokładnie to, czego ten
   tydzień ma nie wymagać.

   SKĄD DANE
   =========
   Wyłącznie z tego, co aplikacja i tak zapisuje: dziennika dni
   (Progress.data.days), dziennika sesji (Session.log), stanu lekcji, kartoteki
   powtórek i pokrycia rozumienia. Retrospekcja nic nie mierzy sama — gdyby
   miała własny licznik, mogłaby pokazać coś innego niż reszta aplikacji.
*/
(function (global) {
  'use strict';

  var Retro = {};

  function dayList(start, days) {
    var out = [];
    for (var i = 0; i < days; i++) out.push(U.addDays(start, i));
    return out;
  }

  /* Surowe liczby tygodnia zaczynającego się danego dnia. */
  function weekStats(start) {
    var days = dayList(start, 7);
    var today = U.today();
    var out = { start: start, end: days[6], minutes: 0, answers: 0, correct: 0,
                activeDays: 0, newWords: 0, days: [] };
    var store = (global.Progress && Progress.data && Progress.data.days) || {};
    days.forEach(function (d) {
      var s = store[d] || { answers: 0, correct: 0, minutes: 0, newWords: 0 };
      if (d > today) { out.days.push({ date: d, future: true, stats: s }); return; }
      out.minutes += s.minutes || 0;
      out.answers += s.answers || 0;
      out.correct += s.correct || 0;
      out.newWords += s.newWords || 0;
      if ((s.answers || 0) > 0 || (s.minutes || 0) >= 1) out.activeDays += 1;
      out.days.push({ date: d, stats: s });
    });
    out.minutes = Math.round(out.minutes);
    out.accuracy = out.answers ? Math.round(out.correct / out.answers * 100) : null;

    /* Lekcje zaliczone w tym tygodniu. Wpisy z migracji pomijamy — mają
       jedną wspólną datę i policzone dałyby „trzysta lekcji w tydzień”. */
    var lessons = (global.Progress && Progress.data && Progress.data.lessons) || {};
    out.lessons = 0;
    Object.keys(lessons).forEach(function (id) {
      var st = lessons[id];
      if (!st || !st.date) return;
      if (st.source && String(st.source).indexOf('migracja') === 0) return;
      if (st.date >= start && st.date <= out.end) out.lessons += 1;
    });

    /* Sesje dnia: ile uruchomionych, ile domkniętych. */
    var log = (global.Session && Session.log) ? Session.log() : [];
    out.sessions = 0;
    out.sessionMinutes = 0;
    out.byKind = {};
    log.forEach(function (e) {
      if (e.d < start || e.d > out.end) return;
      out.sessions += 1;
      out.sessionMinutes += Math.round((e.spent || 0) / 60);
      Object.keys(e.blocks || {}).forEach(function (k) {
        var b = out.byKind[k] || (out.byKind[k] = { steps: 0, done: 0, correct: 0 });
        b.steps += e.blocks[k].steps;
        b.done += e.blocks[k].done;
        b.correct += e.blocks[k].correct;
      });
    });
    return out;
  }

  Retro.weekStats = weekStats;

  /* Bieżący tydzień i poprzedni — porównanie potrzebuje obu. */
  Retro.week = function (offset) {
    var start = Goals.weekStart(U.today());
    if (offset) start = U.addDays(start, offset * 7);
    return weekStats(start);
  };

  /* --------------------------------------------------- pokrycie w czasie */

  /* Migawka pokrycia zapisywana raz dziennie. Bez niej nie da się powiedzieć,
     czy pokrycie w tym tygodniu urosło — miara liczy się z bieżącego stanu
     powtórek i nie pamięta, jak było w poniedziałek.

     Zapisujemy liczby, nie stany kart: kilkanaście wartości na dzień, sześć
     tygodni wstecz. */
  var SNAP_LIMIT = 45;

  Retro.snapshot = function (force) {
    if (!global.Coverage || !Coverage.ready()) return null;
    var today = U.today();
    var snaps = U.store.get('coverage.snaps', []) || [];
    var last = snaps.length ? snaps[snaps.length - 1] : null;
    if (last && last.d === today && !force) return last;

    var entry = { d: today, c: {} };
    Coverage.all().forEach(function (c) {
      entry.c[c.name] = Math.round(c.coverage * 1000) / 1000;
    });
    if (last && last.d === today) snaps[snaps.length - 1] = entry;
    else snaps.push(entry);
    if (snaps.length > SNAP_LIMIT) snaps = snaps.slice(-SNAP_LIMIT);
    U.store.set('coverage.snaps', snaps);
    return entry;
  };

  Retro.snapshots = function () { return U.store.get('coverage.snaps', []) || []; };

  /* Migawka z dnia nie późniejszego niż podany. Zwraca null, gdy historii
     jeszcze nie ma — ekran musi wtedy powiedzieć „za wcześnie”, a nie
     udawać zerowy punkt startowy. */
  Retro.snapshotAt = function (date) {
    var snaps = Retro.snapshots();
    var best = null;
    snaps.forEach(function (s) { if (s.d <= date) best = s; });
    return best;
  };

  /* Zmiana pokrycia w kategoriach od początku tygodnia. */
  Retro.coverageDelta = function (start) {
    if (!global.Coverage || !Coverage.ready()) return null;
    var base = Retro.snapshotAt(start || Goals.weekStart());
    if (!base) return null;
    var out = [];
    Coverage.all().forEach(function (c) {
      var was = base.c[c.name];
      if (was === undefined) return;
      out.push({ name: c.name, was: was, now: c.coverage, delta: c.coverage - was, thin: c.thin });
    });
    out.sort(function (a, b) { return b.delta - a.delta; });
    return out;
  };

  /* ------------------------------------------------------ podsumowanie */

  /* Co urosło i co stoi. Progi są celowo tępe: różnica poniżej nich nie jest
     postępem, tylko szumem jednej dobrej sesji. */
  var GROWTH = 0.005;      // pół punktu procentowego pokrycia

  Retro.summary = function () {
    var now = Retro.week(0);
    var prev = Retro.week(-1);
    var delta = Retro.coverageDelta(now.start);

    var moved = [], stuck = [];
    if (delta) {
      delta.forEach(function (d) {
        if (d.delta >= GROWTH) moved.push(d);
        else if (!d.thin) stuck.push(d);
      });
      stuck.sort(function (a, b) { return a.now - b.now; });
    }

    return {
      now: now,
      prev: prev,
      compare: {
        minutes: now.minutes - prev.minutes,
        answers: now.answers - prev.answers,
        activeDays: now.activeDays - prev.activeDays,
        lessons: now.lessons - prev.lessons,
        accuracy: (now.accuracy !== null && prev.accuracy !== null)
          ? now.accuracy - prev.accuracy : null
      },
      moved: moved,
      stuck: stuck.slice(0, 3),
      hasHistory: !!delta,
      recommendation: Retro.recommend(now, prev, moved, stuck)
    };
  };

  /* JEDNA rekomendacja. Kolejność sprawdzania jest kolejnością szkody:
     najpierw to, co psuje naukę, potem to, co ją hamuje, na końcu to, co ją
     przyspiesza. Pierwsza reguła, która zaskoczy, wygrywa — i nic więcej nie
     jest pokazywane. */
  Retro.recommend = function (now, prev, moved, stuck) {
    var due = global.SRS ? SRS.plan() : null;

    /* 1. Zaległa kolejka. Nic innego nie ma znaczenia, dopóki hasła
          wypadają z pamięci szybciej, niż wchodzą. */
    if (due && due.dueTotal > due.cap * 2) {
      return {
        kind: 'backlog',
        text: 'Masz ' + due.dueTotal + ' zaległych kart — ponad dwa dni pracy. '
          + 'W przyszłym tygodniu rób wyłącznie sesje dnia i nie dokładaj nowych lekcji, '
          + 'aż kolejka zejdzie poniżej ' + due.cap + ' kart.',
        action: { screen: 'session', label: 'Uruchom sesję dnia' }
      };
    }

    /* 2. Brak regularności. Trzy dni po godzinie są warte więcej niż jedna
          trzygodzinna niedziela — odstępy powtórek liczą się w dniach. */
    if (now.activeDays > 0 && now.activeDays <= 2 && now.minutes >= 30) {
      return {
        kind: 'rhythm',
        text: 'Uczyłeś się ' + now.minutes + ' minut, ale tylko przez '
          + now.activeDays + ' ' + U.plural(now.activeDays, 'dzień', 'dni', 'dni')
          + '. Powtórki są planowane w dniach, więc ten sam czas rozłożony na cztery dni '
          + 'da wyraźnie więcej. Ustaw krótszy cel dzienny i przypomnienie.',
        action: { screen: 'settings', label: 'Ustaw cel dzienny' }
      };
    }

    /* 3. Wypadnięcie z rytmu w ogóle. */
    if (now.activeDays === 0) {
      return {
        kind: 'restart',
        text: 'W tym tygodniu nie było ani jednego dnia nauki. '
          + 'Wróć najkrótszą sesją, jaka jest — dziesięć minut. Chodzi o to, żeby '
          + 'znowu zacząć, a nie żeby nadrobić.',
        action: { screen: 'session', label: 'Sesja na 10 minut' }
      };
    }

    /* 4. Wytwarzanie zostaje w tyle za rozpoznawaniem. */
    if (global.SRS && SRS.sideGap) {
      var gap = SRS.sideGap();
      if (gap && gap.behind && gap.steps >= 1.5) {
        return {
          kind: 'sides',
          text: 'Rozpoznajesz znacznie więcej, niż potrafisz powiedzieć — różnica '
            + 'urosła do ' + String(gap.steps).replace('.', ',') + ' poziomu odstępu. '
            + 'W przyszłym tygodniu daj więcej miejsca ćwiczeniom produkcyjnym; sesja dnia '
            + 'sama je dołoży, jeśli będziesz ją uruchamiać.',
          action: { screen: 'produce', label: 'Mówienie po tajsku' }
        };
      }
    }

    /* 5. Kategoria stojąca w miejscu — konkretna, z nazwy. */
    if (stuck && stuck.length) {
      var s = stuck[0];
      var g = global.Coverage ? Coverage.gap(s.name) : null;
      return {
        kind: 'category',
        text: 'Pokrycie w kategorii „' + s.name + '” nie drgnęło i jest najniższe ze wszystkich ('
          + Math.round(s.now * 100) + '%). '
          + (g && !g.done ? 'Do celu brakuje ' + g.words + ' ' + U.plural(g.words, 'hasła', 'haseł', 'haseł') + '. ' : '')
          + 'Ustaw ją jako cel tygodnia — sesja dnia zacznie dobierać z niej materiał.',
        action: { screen: 'roadmap', label: 'Mapa drogi do celu', category: s.name }
      };
    }

    /* 6. Wszystko idzie. Wtedy rekomendacja mówi, co przyspieszyć. */
    if (moved && moved.length) {
      var m = moved[0];
      return {
        kind: 'keep',
        text: 'Najwięcej urosło pokrycie w kategorii „' + m.name + '” (+'
          + Math.round(m.delta * 100) + ' punktu). Trzymaj ten rytm — '
          + 'i dołóż jeden dzień z blokiem wymowy, bo to jedyna część, której '
          + 'nie da się nadrobić samym czytaniem.',
        action: { screen: 'session', label: 'Sesja dnia' }
      };
    }

    return {
      kind: 'start',
      text: 'Za mało danych na wnioski — potrzebny jest tydzień z kilkoma sesjami. '
        + 'Zacznij od sesji dnia; ona sama dobierze skład.',
      action: { screen: 'session', label: 'Sesja dnia' }
    };
  };

  global.Retro = Retro;
})(window);
