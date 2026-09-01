/* Thai All-in-One — sesja naprawcza.

   Ekran Postęp od sesji I umiał wskazać najsłabszy obszar: „kategoria Jedzenie,
   34 % pudeł”. I na tym się kończyło. Uczący się wiedział, gdzie jest słabo,
   i nie miał czym tego naprawić — mógł najwyżej włączyć zwykłe ćwiczenia
   i liczyć, że los podrzuci mu akurat te hasła.

   Ten moduł zamyka tę pętlę. Zestaw powstaje z KONKRETNYCH haseł, na których
   uczący się się mylił, wziętych z dziennika pomyłek (Progress.missesIn)
   i z kartoteki powtórek (karty z wpadkami). Nie z losowania po kategorii —
   losowanie dałoby materiał, a nie naprawę.

   Tryb dobieramy do rodzaju błędu, bo to nie jest jedno „nie umiem”:

     mylisz się w rozpoznawaniu   -> wybierz tłumaczenie (odbiór)
     mylisz się w wytwarzaniu     -> ułóż zdanie / napisz po tajsku
     mylisz się w tonach          -> powiedz na głos, z oceną konturu
     mylisz się w gramatyce       -> ułóż zdanie z tym wzorcem
     mylisz się w klasyfikatorach -> ćwiczenie klasyfikatorów

   Jeśli hasło było mylone w kilku trybach, wygrywa ten, w którym pudeł było
   najwięcej — naprawiamy to, co faktycznie nie działa. */
(function (global) {
  'use strict';

  var Repair = { set: null, index: 0, results: [] };

  var MAX_ITEMS = 12;   // ile haseł w jednej sesji naprawczej

  /* Tryb ćwiczenia -> strona kartoteki, której dotyczy. Ta sama mapa mówi
     nam, czym naprawiać: jeśli pudła są receptywne, nie ma sensu kazać
     komuś układać zdań. */
  /* Strona kartoteki bierze się z rejestru trybów (js/utils.js) — ta sama
     wiedza służyła wcześniej w trzech miejscach i w każdym mogła się rozjechać. */
  var MODE_SIDE = {};
  Object.keys(U.EX).forEach(function (id) { MODE_SIDE[id] = U.exSide(id); });

  /* Ćwiczenia, którymi sesja naprawcza umie sterować hasło po haśle.
     Reszta trybów (dialogi, scenki, hałas) potrzebuje własnego materiału
     i nie da się jej nakarmić listą haseł — sprowadzamy je do najbliższego
     ćwiczenia, które to potrafi. */
  /* Ćwiczenia, którymi sesja naprawcza umie sterować hasło po haśle.
     Reszta trybów (dialogi, scenki, hałas) potrzebuje własnego materiału
     i nie da się jej nakarmić listą haseł — sprowadzamy je do najbliższego
     ćwiczenia, które to potrafi.

     Do sesji V stało tu `screen: 'quiz'` — ekran o tym identyfikatorze nigdy
     nie istniał, więc pole wskazywało w pustkę (App.go odesłałoby na „Dzisiaj”).
     Nikt go nie czytał, bo sesja naprawcza prowadzi ćwiczenie u siebie, ale
     martwe pole w danych to zaproszenie do błędu przy następnej rozbudowie.
     Ekran bierzemy teraz z rejestru, gdzie jest prawdziwy. */
  var RUNNABLE = {};
  ['choice', 'build', 'type', 'say', 'classifier'].forEach(function (id) {
    RUNNABLE[id] = { screen: U.exScreen(id), label: U.exLabel(id), side: U.exSide(id) };
  });

  var FALLBACK = {
    dictation: 'choice', assemble: 'choice', spot: 'choice',
    gender: 'choice', noise: 'choice', gap: 'choice', unknown: 'choice',
    tone: 'say', roleplay: 'say'
  };

  Repair.MODE_SIDE = MODE_SIDE;
  Repair.RUNNABLE = RUNNABLE;

  function runnable(mode) {
    if (RUNNABLE[mode]) return mode;
    if (FALLBACK[mode] && RUNNABLE[FALLBACK[mode]]) return FALLBACK[mode];
    return 'choice';
  }

  /* -------------------------------------------------- zbieranie materiału */

  /* Hasła z kartoteki, które w danym obszarze mają wpadki. Dziennik pomyłek
     sięga miesiąc wstecz; karty pamiętają dłużej, więc jedno uzupełnia drugie.
     Karta wie przy okazji, KTÓRA strona zawiodła — to jest informacja,
     której dziennik nie ma. */
  function fromCards(bucket, key) {
    if (!global.SRS || !SRS.cards) return [];
    var out = [];
    Object.keys(SRS.cards).forEach(function (cardId) {
      var card = SRS.cards[cardId];
      if (!card.lapses) return;
      var rid = SRS.recordOf(cardId);
      if (!rid) return;
      var rec = (global.DB && DB.any) ? DB.any(rid) : null;
      if (!rec) return;
      if (bucket === 'category' && rec.category !== key) return;
      if (bucket === 'type' && rec.type !== key) return;
      if (bucket === 'grammar') return;   // gramatyki karta nie zna
      if (bucket === 'mode') return;      // trybu też nie
      out.push({ id: rid, n: card.lapses, last: card.last || '', side: SRS.sideOf(cardId), modes: {} });
    });
    return out;
  }

  function merge(a, b) {
    var byId = {};
    a.concat(b).forEach(function (m) {
      if (!byId[m.id]) {
        byId[m.id] = { id: m.id, n: 0, last: m.last || '', modes: {}, sides: {} };
      }
      var t = byId[m.id];
      t.n += m.n || 1;
      if ((m.last || '') > t.last) t.last = m.last || '';
      Object.keys(m.modes || {}).forEach(function (k) {
        t.modes[k] = (t.modes[k] || 0) + m.modes[k];
      });
      if (m.side) t.sides[m.side] = (t.sides[m.side] || 0) + (m.n || 1);
    });
    return Object.keys(byId).map(function (k) { return byId[k]; });
  }

  /* Który tryb naprawi to zestawienie pomyłek. Patrzymy najpierw na tryby,
     w których hasła faktycznie leciały; dopiero gdy ich nie ma (bo materiał
     przyszedł z kart, nie z dziennika) — na stronę kartoteki. */
  function pickMode(items, bucket, key) {
    if (bucket === 'mode' && key) return runnable(key);

    var tally = {};
    items.forEach(function (it) {
      Object.keys(it.modes || {}).forEach(function (m) {
        tally[m] = (tally[m] || 0) + it.modes[m];
      });
    });
    var best = null;
    Object.keys(tally).forEach(function (m) {
      if (!best || tally[m] > tally[best]) best = m;
    });
    if (best) return runnable(best);

    if (bucket === 'grammar') return 'build';

    var sides = { r: 0, p: 0, w: 0 };
    items.forEach(function (it) {
      Object.keys(it.sides || {}).forEach(function (s) { sides[s] = (sides[s] || 0) + it.sides[s]; });
    });
    if (sides.w > sides.r && sides.w > sides.p) return 'say';
    if (sides.p > sides.r) return 'build';
    return 'choice';
  }

  /* -------------------------------------------------------- budowa zestawu */

  /* area — wynik Progress.worstArea(): { bucket, key, label, rate, ... }
     Zwraca opis zestawu albo null, jeśli nie ma z czego go zbudować. */
  Repair.build = function (area, opts) {
    opts = opts || {};
    if (!area || !area.bucket) return null;

    var fromLog = (global.Progress && Progress.missesIn)
      ? Progress.missesIn(area.bucket, area.key, 0) : [];
    var items = merge(fromLog, fromCards(area.bucket, area.key));
    if (!items.length) return null;

    /* Najpierw hasła mylone najczęściej. Przy remisie decyduje częstość hasła
       w mowie — jeśli mamy naprawić dwanaście z trzydziestu, niech to będą te,
       które uczący się faktycznie usłyszy. */
    items.sort(function (a, b) {
      if (b.n !== a.n) return b.n - a.n;
      var fa = freq(a.id), fb = freq(b.id);
      if (fb !== fa) return fb - fa;
      return a.last < b.last ? 1 : -1;
    });

    var mode = opts.mode || pickMode(items, area.bucket, area.key);
    var picked = items.slice(0, opts.limit || MAX_ITEMS);

    return {
      area: area,
      mode: mode,
      side: (RUNNABLE[mode] || {}).side || 'r',
      label: (RUNNABLE[mode] || {}).label || U.exLabel(mode),
      screen: (RUNNABLE[mode] || {}).screen || U.exScreen(mode) || 'listen',
      ids: picked.map(function (p) { return p.id; }),
      items: picked,
      pool: items.length,
      why: reason(area, mode)
    };
  };

  function freq(id) {
    var rec = (global.DB && DB.any) ? DB.any(id) : null;
    return rec && typeof rec.frequency === 'number' ? rec.frequency : 0;
  }

  function reason(area, mode) {
    var what = {
      category: 'w kategorii', grammar: 'w temacie', mode: 'w ćwiczeniu', type: 'w typie haseł'
    }[area.bucket] || 'w obszarze';
    var how = {
      choice: 'Pudła były w rozpoznawaniu, więc pytamy o znaczenie.',
      build: 'Pudła były w wytwarzaniu, więc każemy ułożyć zdanie.',
      type: 'Pudła były w wytwarzaniu, więc każemy zapisać po tajsku.',
      say: 'Pudła dotyczyły wymowy, więc trzeba to powiedzieć na głos.',
      classifier: 'Pudła dotyczyły klasyfikatorów, więc ćwiczymy właśnie je.'
    }[mode] || '';
    return 'Hasła, na których pomyliłeś się ' + what + ' „' + (area.label || area.key) + '”. ' + how;
  }

  /* Zestaw z jednego konkretnego hasła — wejście z listy „Nad czym popracować”. */
  Repair.buildForIds = function (ids, mode) {
    if (!ids || !ids.length) return null;
    var m = runnable(mode || 'choice');
    return {
      area: { bucket: 'wybrane', key: '', label: 'wybrane hasła' },
      mode: m,
      side: (RUNNABLE[m] || {}).side || 'r',
      label: (RUNNABLE[m] || {}).label || U.exLabel(m),
      screen: (RUNNABLE[m] || {}).screen || U.exScreen(m) || 'listen',
      ids: ids.slice(0, MAX_ITEMS),
      items: ids.slice(0, MAX_ITEMS).map(function (id) { return { id: id, n: 1, modes: {} }; }),
      pool: ids.length,
      why: 'Hasła wybrane ręcznie z listy trudnych.'
    };
  };

  /* --------------------------------------------------------- przebieg sesji */

  Repair.start = function (set) {
    Repair.set = set;
    Repair.index = 0;
    Repair.results = [];
    return set;
  };

  Repair.current = function () {
    if (!Repair.set) return null;
    var id = Repair.set.ids[Repair.index];
    return id ? ((global.DB && DB.any) ? DB.any(id) : null) : null;
  };

  Repair.note = function (id, ok) {
    Repair.results.push({ id: id, ok: !!ok });
  };

  Repair.advance = function () {
    Repair.index += 1;
    return Repair.index < (Repair.set ? Repair.set.ids.length : 0);
  };

  Repair.done = function () {
    return !Repair.set || Repair.index >= Repair.set.ids.length;
  };

  Repair.summary = function () {
    var ok = Repair.results.filter(function (r) { return r.ok; }).length;
    var total = Repair.results.length;
    return {
      ok: ok, total: total,
      rate: total ? Math.round(ok / total * 100) : 0,
      stillWrong: Repair.results.filter(function (r) { return !r.ok; })
        .map(function (r) { return r.id; })
    };
  };

  /* Hasła potrzebne sesji trzeba mieć w pamięci — pochodzą z różnych poziomów,
     więc nie wystarczy poziom bieżący. */
  Repair.ensureData = function (set) {
    if (!set || !set.ids.length) return Promise.resolve();
    if (global.DB && DB.ensureFor) return DB.ensureFor(set.ids);
    return Promise.resolve();
  };

  global.Repair = Repair;
})(window);
