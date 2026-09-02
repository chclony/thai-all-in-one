/* Thai All-in-One — pokrycie rozumienia.

   PO CO TO JEST
   =============
   Do sesji P jedyną miarą postępu była liczba poznanych haseł. Ta liczba
   rośnie zawsze i nie mówi nic o celu, którym jest zrozumienie rozmowy:
   czterysta haseł z „Cech i opinii” nie pomoże zamówić obiadu, a czterdzieści
   właściwych z „Restauracji” — pomoże.

   Ten moduł liczy co innego: jaki procent wyrazów w FAKTYCZNYM materiale danej
   kategorii uczący się zna. Korpus i przypisanie wyrazów do haseł przygotowuje
   tools/generators/coverage.py; tutaj dokłada się jedyne, czego generator nie
   mógł wiedzieć — stan wiedzy konkretnego człowieka.

   CO ZNACZY „ZNA”
   ===============
   Znane hasło to takie, którego karta ROZPOZNANIA jest w powtórkach opanowana:
   co najmniej dwa udane powtórzenia i odstęp od sześciu dni w górę
   (SRS.LEARNED). Nie „widziane raz”, nie „jest w kartotece”.

   Wybór jest celowy i idzie wbrew temu, co daje wyższą liczbę:
     - Progress.seen liczy każdy kontakt z hasłem, także przelotny. Hasło
       obejrzane raz w słowniku nie jest hasłem rozumianym ze słuchu.
     - Sama obecność karty w kartotece też nie wystarcza — karta założona
       wczoraj oznacza dopiero początek nauki.
     - Strona ROZPOZNANIA, nie wytworzenia, bo rozumienie rozmowy jest
       umiejętnością receptywną. Umieć powiedzieć „rachunek” to co innego niż
       zrozumieć „rachunek” rzucone szybko przez kelnera.

   DWIE LICZBY, NIE JEDNA
   ======================
   pokrycie  — znane wystąpienia / WSZYSTKIE wystąpienia w korpusie
   sufit     — wystąpienia z hasłem w bazie / wszystkie wystąpienia

   Mianownik jest w obu ten sam i obejmuje też wyrazy, których w bazie nie ma.
   Można było je z mianownika wyrzucić i pokazywać ładniejszą liczbę — ale
   uczący się słyszy te wyrazy w nagraniu niezależnie od tego, czy aplikacja
   umie je nazwać. Pokrycie musi to widzieć, a sufit mówi wprost, gdzie leży
   granica tego, czego ta baza jest w stanie nauczyć.
*/
(function (global) {
  'use strict';

  var Coverage = { data: null };

  /* Cztery kategorie, o które pyta się najczęściej i które ekran „Dzisiaj”
     pokazuje bez rozwijania. Reszta jest na mapie drogi do celu. */
  Coverage.HEADLINE = ['Restauracja', 'Transport', 'Zdrowie', 'Small talk'];

  Coverage.ready = function () {
    return !!(global.DB && DB.coverage && DB.coverage.categories);
  };

  Coverage.ensure = function () {
    return DB.ensureCoverage();
  };

  Coverage.method = function () {
    return (DB.coverage && DB.coverage.method) || {};
  };

  Coverage.totals = function () {
    return (DB.coverage && DB.coverage.totals) || {};
  };

  /* Próg pokrycia uznany za „rozumiem tę kategorię”. Liczba pochodzi z danych,
     nie z kodu ekranu — raport i aplikacja mają liczyć tak samo. */
  Coverage.target = function () {
    var m = Coverage.method();
    return typeof m.target === 'number' ? m.target : 0.95;
  };

  /* Ile wyrazów kwestii trzeba znać, żeby uznać ją za zrozumiałą. */
  Coverage.lineThreshold = function () {
    var m = Coverage.method();
    return typeof m.lineThreshold === 'number' ? m.lineThreshold : 0.95;
  };

  /* --------------------------------------------------------------- stan */

  function learned(recordId) {
    return !!(global.SRS && SRS.isLearned(recordId, 'r'));
  }

  /* Hasło w kartotece, ale jeszcze nieopanowane. Nie wchodzi do pokrycia —
     wchodzi do osobnej liczby „w drodze”, żeby ekran mógł pokazać, ile
     pokrycia przybędzie, gdy bieżąca nauka dojdzie do końca. */
  function started(recordId) {
    return !!(global.SRS && SRS.has(recordId, 'r') && !SRS.isLearned(recordId, 'r'));
  }

  /* --------------------------------------------------- liczenie kategorii */

  /* Wynik dla jednej kategorii. Liczone od zera przy każdym wywołaniu:
     stan powtórek zmienia się w trakcie sesji, a pamiętany wynik
     pokazywałby liczbę sprzed dziesięciu minut. Koszt to jedno przejście po
     korpusie kategorii — przy największej z nich (1637 wyrazów) rzecz
     nieodczuwalna. */
  Coverage.category = function (name) {
    if (!Coverage.ready()) return null;
    var cat = null;
    DB.coverage.categories.forEach(function (c) { if (c.name === name) cat = c; });
    if (!cat) return null;

    /* Stan każdego hasła z tabeli kategorii liczymy raz, a nie przy każdym
       jego wystąpieniu — hasła wracają w korpusie po kilkanaście razy. */
    var state = cat.ids.map(function (id) {
      if (learned(id)) return 2;
      if (started(id)) return 1;
      return 0;
    });

    var known = 0, inProgress = 0;
    var linesKnown = 0;
    var threshold = Coverage.lineThreshold();

    cat.l.forEach(function (line) {
      var slots = line.s;
      var hit = 0;
      for (var i = 0; i < slots.length; i++) {
        var s = slots[i];
        if (s < 0) continue;
        if (state[s] === 2) { known += 1; hit += 1; }
        else if (state[s] === 1) inProgress += 1;
      }
      if (slots.length && hit / slots.length >= threshold) linesKnown += 1;
    });

    var occ = cat.occurrences || 1;
    return {
      name: cat.name,
      dialogues: cat.dialogues,
      lines: cat.lines,
      occurrences: cat.occurrences,
      items: cat.items,
      thin: !!cat.thin,

      known: known,
      inProgress: inProgress,
      coverage: known / occ,
      reach: (known + inProgress) / occ,          // pokrycie po domknięciu nauki
      ceiling: cat.mapped / occ,                   // sufit metody
      unmapped: cat.unmapped,
      ambiguous: cat.ambiguous,
      loose: cat.loose || 0,

      linesKnown: linesKnown,
      linesShare: cat.lines ? linesKnown / cat.lines : 0,

      /* Cel osiągalny: próg z badań albo sufit metody, jeśli jest niżej.
         Obiecywanie 95% tam, gdzie baza nie zna 8% wyrazów materiału, byłoby
         dokładnie tą motywacyjną fikcją, której ta miara ma nie być. */
      goal: Math.min(Coverage.target(), cat.mapped / occ),
      goalIsCeiling: (cat.mapped / occ) < Coverage.target()
    };
  };

  Coverage.all = function () {
    if (!Coverage.ready()) return [];
    return DB.coverage.categories.map(function (c) { return Coverage.category(c.name); })
      .filter(Boolean);
  };

  /* Kategorie warte pokazania: te z materiałem wystarczającym, żeby liczba
     coś znaczyła. Cienkie zostają dostępne, ale nie ustawiają się na czele
     żadnej listy i nie sterują niczym automatycznie. */
  Coverage.solid = function () {
    return Coverage.all().filter(function (c) { return !c.thin; });
  };

  Coverage.headline = function () {
    var out = [];
    Coverage.HEADLINE.forEach(function (name) {
      var c = Coverage.category(name);
      if (c) out.push(c);
    });
    return out;
  };

  /* Najsłabsza kategoria z sensownym materiałem — używa jej sesja dnia przy
     doborze bloku wzmacniającego i retrospekcja tygodnia. */
  Coverage.weakest = function () {
    var list = Coverage.solid();
    if (!list.length) return null;
    /* Na starcie wszystkie kategorie mają pokrycie zero i „najsłabsza” byłaby
       wynikiem kolejności w pliku, nie stanu nauki. Wskazywanie wtedy
       czegokolwiek jako słabego punktu jest podawaniem szumu za diagnozę —
       więc mówimy, że sygnału nie ma. */
    var any = list.some(function (c) { return c.coverage > 0; });
    if (!any) return null;
    return list.slice().sort(function (a, b) { return a.coverage - b.coverage; })[0];
  };

  /* --------------------------------------------------- droga do celu */

  /* Które hasła kategorii dołożą najwięcej pokrycia. Kolejność jest wprost
     liczbą wystąpień w korpusie: hasło padające dwadzieścia razy podnosi
     pokrycie dwadzieścia razy mocniej niż padające raz. To jest cała
     tajemnica „skąd wiadomo, czego się uczyć najpierw”. */
  Coverage.nextItems = function (name, limit) {
    if (!Coverage.ready()) return [];
    var cat = null;
    DB.coverage.categories.forEach(function (c) { if (c.name === name) cat = c; });
    if (!cat) return [];
    var out = [];
    cat.ids.forEach(function (id, i) {
      if (learned(id)) return;
      out.push({ id: id, weight: cat.weights[i] || 0, started: started(id) });
    });
    out.sort(function (a, b) { return b.weight - a.weight; });
    return out.slice(0, limit || 20);
  };

  /* Ile haseł dzieli uczącego się od celu w tej kategorii — i ile to lekcji.
     Liczymy zachłannie: bierzemy hasła od najczęstszego, aż pokrycie sięgnie
     celu. To jest dolna granica (uczący się mógłby uczyć się w gorszej
     kolejności), więc liczba jest optymistyczna i tak jest opisana. */
  Coverage.gap = function (name) {
    var c = Coverage.category(name);
    if (!c) return null;
    var cat = null;
    DB.coverage.categories.forEach(function (x) { if (x.name === name) cat = x; });

    var needShare = c.goal - c.coverage;
    if (needShare <= 0) {
      return { name: name, done: true, words: 0, occurrences: 0,
               goal: c.goal, coverage: c.coverage, goalIsCeiling: c.goalIsCeiling };
    }
    var needOcc = Math.ceil(needShare * cat.occurrences);

    var pool = Coverage.nextItems(name, cat.ids.length);
    var got = 0, words = 0;
    for (var i = 0; i < pool.length && got < needOcc; i++) {
      got += pool[i].weight;
      words += 1;
    }
    return {
      name: name,
      done: false,
      words: words,                 // ile haseł trzeba opanować
      occurrences: needOcc,         // ile wystąpień trzeba domknąć
      goal: c.goal,
      coverage: c.coverage,
      goalIsCeiling: c.goalIsCeiling
    };
  };

  /* ----------------------------------------------------------- tempo */

  /* Ile haseł uczący się opanowuje tygodniowo. Bierzemy to z kartoteki:
     karty, które PRZEKROCZYŁY próg opanowania, mają odstęp co najmniej
     sześciodniowy, więc daty ich ostatniej powtórki rozłożone w czasie są
     najlepszym, co mamy. Poniżej progu wiarygodności mówimy „jeszcze nie
     wiadomo” zamiast podawać liczbę bez pokrycia — tak samo jak Course.pace. */
  var PACE_WINDOW = 28;

  Coverage.pace = function () {
    if (!global.SRS || !SRS.cards) return { known: false };
    var today = U.today();
    var count = 0, days = {};
    Object.keys(SRS.cards).forEach(function (cid) {
      if (SRS.sideOf(cid) !== 'r') return;
      var card = SRS.cards[cid];
      if (!card || !card.last) return;
      if (!(card.repetitions >= SRS.LEARNED.repetitions && card.interval >= SRS.LEARNED.interval)) return;
      var age = U.daysBetween(card.last, today);
      if (age < 0 || age > PACE_WINDOW) return;
      count += 1;
      days[card.last] = true;
    });
    var activeDays = Object.keys(days).length;
    if (activeDays < 3 || !count) return { known: false, perWeek: 0 };
    var perActiveDay = count / activeDays;
    var daysPerWeek = Math.min(7, activeDays / (PACE_WINDOW / 7));
    return {
      known: true,
      perWeek: perActiveDay * daysPerWeek,
      inWindow: count,
      activeDays: activeDays
    };
  };

  /* Ile tygodni do celu w kategorii przy obecnym tempie. Zwraca null, gdy
     tempa jeszcze nie da się policzyć — ekran ma wtedy powiedzieć, czego
     brakuje, a nie zgadywać. */
  Coverage.weeksTo = function (name) {
    var gap = Coverage.gap(name);
    var pace = Coverage.pace();
    if (!gap || gap.done) return 0;
    if (!pace.known || pace.perWeek <= 0) return null;
    return gap.words / pace.perWeek;
  };

  /* Ile lekcji kursu to odpowiada. Lekcja wprowadza tyle nowych haseł, ile
     wynika z danych ścieżki — liczymy medianę zamiast zakładać stałą. */
  Coverage.wordsPerLesson = function () {
    var list = (global.DB && DB.lessons) || [];
    if (!list.length) return 8;
    var counts = list.map(function (L) { return (L.newWordIds || []).length; })
      .filter(function (n) { return n > 0; });
    if (!counts.length) return 8;
    counts.sort(function (a, b) { return a - b; });
    var mid = Math.floor(counts.length / 2);
    return counts.length % 2 ? counts[mid] : Math.round((counts[mid - 1] + counts[mid]) / 2);
  };

  global.Coverage = Coverage;
})(window);
