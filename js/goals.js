/* Thai All-in-One — cele i przypomnienia.

   CO BYŁO NIE TAK
   ===============
   Cel dzienny był surową liczbą odpowiedzi („20 z 20”). Ta liczba ma trzy wady:

   1. Jest niesterowalna. Uczący się nie decyduje, ile odpowiedzi zdąży —
      decyduje, ile ma czasu. Cel wyrażony w tym, czym uczący się nie
      dysponuje, jest celem cudzym.
   2. Da się ją zrobić najtaniej. Dwadzieścia szybkich rozpoznań w słowniku
      liczy się tak samo jak dwadzieścia prób wymowy. Cel premiuje więc
      ćwiczenie najłatwiejsze, czyli najmniej potrzebne.
   3. Nie ma kierunku. „20 odpowiedzi dziennie” nie przybliża do niczego
      konkretnego — po miesiącu takich dni uczący się ma 600 odpowiedzi
      i nadal nie wie, czy poradzi sobie w restauracji.

   CO JEST TERAZ
   =============
   CEL CZASOWY — ile minut nauki dziennie. Uczący się nim dysponuje i jest
   uczciwy: dziesięć minut wymowy waży tyle samo co dziesięć minut klikania.

   CEL KATEGORIALNY — jedna kategoria sytuacyjna na tydzień, domykana do
   swojego progu pokrycia („w tym tygodniu domykam restaurację”). To jest cel
   z kierunkiem: ma widoczny koniec i widoczny skutek.

   Cel liczby odpowiedzi zostaje w danych, ale wyłącznie jako materiał dla
   sufitu kolejki powtórek (SRS.dailyCap) — nie jest już nikomu pokazywany.

   PRZYPOMNIENIA
   =============
   Powiadomienia są opcjonalne, wyłączone domyślnie i wymagają zgody
   przeglądarki. Aplikacja nie ma serwera ani wysyłki push — przypomnienie
   pojawia się wyłącznie wtedy, gdy karta jest otwarta, i mówi o tym wprost.
   Obietnica „przypomnimy Ci jutro o 19”, której nie da się dotrzymać przy
   zamkniętej przeglądarce, byłaby po prostu nieprawdą.
*/
(function (global) {
  'use strict';

  var Goals = {};

  var DEFAULTS = {
    minutes: 15,          // cel dzienny w minutach
    category: null,       // { name, week, startCoverage }
    notify: false,        // przypomnienia włączone przez użytkownika
    notifyAt: '19:00'     // pora przypomnienia
  };

  Goals.DEFAULTS = DEFAULTS;

  /* Do wyboru w ustawieniach — bez pola liczbowego, żeby nie zachęcać do
     ustawiania celu, którego nikt nie dotrzyma. */
  Goals.MINUTES = [5, 10, 15, 20, 30, 45];

  function read() {
    var g = U.store.get('goals', null);
    if (!g) g = {};
    var out = {};
    Object.keys(DEFAULTS).forEach(function (k) {
      out[k] = (g[k] === undefined || g[k] === null) ? DEFAULTS[k] : g[k];
    });
    /* Kopia sprzed sesji R ma cel jako liczbę odpowiedzi. Przeliczamy go raz,
       przyjmując tempo z pomiarów: około dwóch odpowiedzi na minutę przy
       mieszance ćwiczeń. Wynik zaokrąglamy do najbliższej wartości z listy,
       żeby ustawienia pokazywały wybór, a nie dowolną liczbę. */
    if (!g.minutes && global.Progress && Progress.data && Progress.data.goal) {
      var guess = Math.round(Progress.data.goal / 2);
      out.minutes = Goals.MINUTES.reduce(function (best, m) {
        return Math.abs(m - guess) < Math.abs(best - guess) ? m : best;
      }, Goals.MINUTES[0]);
    }
    return out;
  }

  Goals.get = read;

  Goals.set = function (patch) {
    var g = read();
    Object.keys(patch || {}).forEach(function (k) { g[k] = patch[k]; });
    U.store.set('goals', g);
    /* Sufit kolejki powtórek nadal czyta Progress.data.goal. Utrzymujemy go
       spójnym z celem czasowym, zamiast zostawiać wartość sprzed zmiany. */
    if (global.Progress && Progress.data) {
      Progress.data.goal = Math.max(5, Math.round(g.minutes * 2));
      Progress.save();
    }
    return g;
  };

  /* ------------------------------------------------------- cel czasowy */

  Goals.today = function () {
    var g = read();
    var stats = (global.Progress && Progress.data)
      ? (Progress.data.days[U.today()] || { minutes: 0, answers: 0 })
      : { minutes: 0, answers: 0 };
    var done = Math.round(stats.minutes || 0);
    return {
      minutes: g.minutes,
      done: done,
      left: Math.max(0, g.minutes - done),
      share: g.minutes ? Math.min(1, done / g.minutes) : 0,
      met: done >= g.minutes,
      answers: stats.answers || 0
    };
  };

  /* --------------------------------------------------- cel kategorialny */

  /* Tydzień w formacie ISO (poniedziałek zaczyna). Cel kategorialny jest
     tygodniowy, więc musi mieć jednoznaczny klucz — inaczej „ten tydzień”
     zmienia znaczenie w niedzielę o północy. */
  Goals.weekKey = function (date) {
    var d = new Date((date || U.today()) + 'T00:00:00');
    var day = (d.getDay() + 6) % 7;              // poniedziałek = 0
    d.setDate(d.getDate() - day + 3);            // czwartek tego tygodnia
    var year = d.getFullYear();
    var jan4 = new Date(year, 0, 4);
    var week = 1 + Math.round(((d - jan4) / 86400000 - 3 + ((jan4.getDay() + 6) % 7)) / 7);
    return year + '-W' + String(week).padStart(2, '0');
  };

  Goals.weekStart = function (date) {
    var d = new Date((date || U.today()) + 'T00:00:00');
    var day = (d.getDay() + 6) % 7;
    d.setDate(d.getDate() - day);
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0')
      + '-' + String(d.getDate()).padStart(2, '0');
  };

  /* Propozycja kategorii na ten tydzień: najbliższa domknięcia spośród tych,
     które jeszcze nie są domknięte. Nie najsłabsza — najsłabsza to zwykle
     kategoria o największym materiale, na którą tydzień nie wystarczy,
     a cel nieosiągalny przestaje być celem po pierwszym tygodniu. */
  Goals.suggestCategory = function () {
    if (!global.Coverage || !Coverage.ready()) return null;
    var list = Coverage.solid().filter(function (c) { return c.coverage < c.goal; });
    if (!list.length) return null;
    list.sort(function (a, b) {
      var ga = Coverage.gap(a.name), gb = Coverage.gap(b.name);
      return (ga ? ga.words : 1e9) - (gb ? gb.words : 1e9);
    });
    return list[0].name;
  };

  Goals.setCategory = function (name) {
    if (!name) {
      Goals.set({ category: null });
      return null;
    }
    var cov = (global.Coverage && Coverage.ready()) ? Coverage.category(name) : null;
    var entry = {
      name: name,
      week: Goals.weekKey(),
      start: Goals.weekStart(),
      startCoverage: cov ? cov.coverage : 0
    };
    Goals.set({ category: entry });
    return entry;
  };

  /* Stan celu kategorialnego. Cel z poprzedniego tygodnia jest zwracany
     z flagą `expired` — retrospekcja ma o nim powiedzieć, zanim zniknie. */
  Goals.category = function () {
    var g = read();
    var c = g.category;
    if (!c || !c.name) return null;
    var cov = (global.Coverage && Coverage.ready()) ? Coverage.category(c.name) : null;
    var gap = (global.Coverage && Coverage.ready()) ? Coverage.gap(c.name) : null;
    return {
      name: c.name,
      week: c.week,
      expired: c.week !== Goals.weekKey(),
      startCoverage: c.startCoverage || 0,
      coverage: cov ? cov.coverage : 0,
      goal: cov ? cov.goal : 0,
      gained: cov ? (cov.coverage - (c.startCoverage || 0)) : 0,
      wordsLeft: gap && !gap.done ? gap.words : 0,
      done: !!(cov && cov.coverage >= cov.goal)
    };
  };

  /* ------------------------------------------------------ powiadomienia */

  Goals.notificationsSupported = function () {
    return typeof global.Notification === 'function';
  };

  Goals.permission = function () {
    if (!Goals.notificationsSupported()) return 'unsupported';
    return Notification.permission;
  };

  /* Prośba o zgodę. Wywoływana wyłącznie z kliknięcia — przeglądarki
     odrzucają prośbę bez gestu użytkownika, a poza tym pytanie bez pytania
     jest po prostu nieuprzejme. */
  Goals.requestPermission = function () {
    if (!Goals.notificationsSupported()) return Promise.resolve('unsupported');
    try {
      var r = Notification.requestPermission();
      /* Starsze przeglądarki zwracają wynik przez wywołanie zwrotne. */
      if (r && typeof r.then === 'function') return r;
      return new Promise(function (resolve) {
        Notification.requestPermission(resolve);
      });
    } catch (e) {
      return Promise.resolve('denied');
    }
  };

  Goals.notify = function (title, body) {
    if (Goals.permission() !== 'granted') return false;
    try {
      var n = new Notification(title, {
        body: body,
        icon: 'assets/icons/icon-180.png',
        tag: 'thai-aio-daily'
      });
      n.onclick = function () { try { global.focus(); n.close(); } catch (e) {} };
      return true;
    } catch (e) {
      return false;
    }
  };

  /* Sprawdzenie pory. Uruchamiane z minutowego zegara aplikacji — jedynego
     momentu, w którym cokolwiek możemy zrobić, bo bez serwera nie istnieje
     wysyłka do zamkniętej przeglądarki. Przypomnienie leci raz dziennie
     i tylko wtedy, gdy cel dnia NIE jest zrobiony: gratulowanie komuś, kto
     właśnie skończył sesję, uczy ignorowania powiadomień. */
  Goals.checkReminder = function (now) {
    var g = read();
    if (!g.notify) return false;
    if (Goals.permission() !== 'granted') return false;

    var today = U.today();
    if (U.store.get('goals.lastNotify', null) === today) return false;

    var at = String(g.notifyAt || '19:00').split(':');
    var d = now || new Date();
    var minutesNow = d.getHours() * 60 + d.getMinutes();
    var minutesSet = (parseInt(at[0], 10) || 0) * 60 + (parseInt(at[1], 10) || 0);
    if (minutesNow < minutesSet) return false;

    var t = Goals.today();
    if (t.met) return false;

    U.store.set('goals.lastNotify', today);

    var due = global.SRS ? SRS.plan().today.length : 0;
    var body = t.left + ' ' + U.plural(t.left, 'minuta', 'minuty', 'minut') + ' do celu dnia';
    if (due) body += ' · ' + due + ' ' + U.plural(due, 'karta', 'karty', 'kart') + ' do powtórki';
    return Goals.notify('Thai All-in-One', body + '.');
  };

  global.Goals = Goals;
})(window);
