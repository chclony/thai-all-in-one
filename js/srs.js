/* Thai All-in-One — powtórki w odstępach (SM-2 z pętlą zwrotną).

   Trzy rzeczy, których nie było do sesji O:

   1. KARTA MA STRONY. Jedno hasło to nie jedna siła pamięci, tylko trzy:
      rozpoznanie (tajski -> polski), wytworzenie (polski -> tajski) i wymowa
      (czy przy mówieniu trafiasz w ton). Rozpoznanie zwykle wyprzedza
      wytworzenie o kilka poziomów, a wymowa potrafi zostać w tyle za obiema.
      Jedna karta na hasło uśredniała te trzy rzeczy w jedną liczbę i przez to
      kłamała w obie strony: pytała o rozpoznanie hasła, które dawno
      rozpoznajesz, i nie pytała o wytworzenie, którego nie umiesz.

      Stąd identyfikator karty ma postać `rekord#strona`:
        rekord#r — receptywna  (słyszysz / widzisz tajski, podajesz polski)
        rekord#p — produktywna (widzisz polski, wytwarzasz tajski)
        rekord#w — wymowa      (mówisz na głos, liczy się kontur tonalny)
      Karty kontrastów słuchowych z Modułu 0 zachowują dawny prefiks `perc:`
      i stoją obok tego podziału — kontrast nie jest hasłem.

   2. KRZYWA ZAPAMIĘTYWANIA STERUJE ODSTĘPAMI. Do sesji O krzywa była
      rysowana i na tym się kończyło: `grade()` jej nie czytał. Teraz z tego
      samego dziennika liczony jest mnożnik odstępów — osobno dla każdej
      strony karty, wyłącznie z danych tego użytkownika. Reguła siedzi
      w sekcji „pętla zwrotna” niżej i jest opisana tam, gdzie działa.

   3. KOLEJKA MA SUFIT. Przy trzech tysiącach haseł dwutygodniowa przerwa
      robi kolejkę na kilkaset pozycji. Kolejka, której nie da się zrobić,
      nie jest kolejką, tylko wyrzutem sumienia — więc zaległości rozkładają
      się na dni, a na wierzch idzie to, co najczęstsze i najbliższe
      zapomnienia. */
(function (global) {
  'use strict';

  var SRS = { cards: {}, log: [], tuning: null };

  var LOG_LIMIT = 3000;   // ile pojedynczych powtórek pamiętamy do krzywej

  /* ==================================================== strony kartoteki */

  var SEP = '#';

  SRS.SIDES = ['r', 'p', 'w'];

  SRS.SIDE_NAMES = {
    r: 'rozpoznanie',
    p: 'wytworzenie',
    w: 'wymowa',
    c: 'kontrast słuchowy'
  };

  SRS.SIDE_LONG = {
    r: 'tajski → polski',
    p: 'polski → tajski',
    w: 'wypowiedz na głos',
    c: 'słyszysz różnicę?'
  };

  SRS.CONTRAST_PREFIX = 'perc:';

  SRS.isContrastCard = function (id) {
    return typeof id === 'string' && id.indexOf(SRS.CONTRAST_PREFIX) === 0;
  };

  SRS.contrastOf = function (id) {
    return SRS.isContrastCard(id) ? id.slice(SRS.CONTRAST_PREFIX.length) : null;
  };

  /* Identyfikator karty z identyfikatora rekordu i strony. Wywołanie bez
     strony daje stronę receptywną — tak zachowują się stare ścieżki kodu,
     które o stronach nie wiedzą. */
  SRS.cardId = function (recordId, side) {
    if (typeof recordId !== 'string') return recordId;
    if (SRS.isContrastCard(recordId)) return recordId;
    if (recordId.indexOf(SEP) !== -1) return recordId;   // już ma stronę
    return recordId + SEP + (side || 'r');
  };

  SRS.recordOf = function (cardId) {
    if (typeof cardId !== 'string') return cardId;
    if (SRS.isContrastCard(cardId)) return null;
    var i = cardId.indexOf(SEP);
    return i === -1 ? cardId : cardId.slice(0, i);
  };

  SRS.sideOf = function (cardId) {
    if (SRS.isContrastCard(cardId)) return 'c';
    var i = String(cardId).indexOf(SEP);
    return i === -1 ? 'r' : cardId.slice(i + 1);
  };

  SRS.sideName = function (side) { return SRS.SIDE_NAMES[side] || side; };

  /* ============================================== wczytanie i zapisanie */

  SRS.load = function () {
    SRS.cards = U.store.get('srs', {}) || {};
    SRS.log = U.store.get('srslog', []) || [];
    SRS.tuning = U.store.get('srstune', null) || blankTuning();
    SRS.migrateSides();
    return SRS.cards;
  };

  SRS.save = function () {
    U.store.set('srs', SRS.cards);
    U.store.set('srslog', SRS.log);
    U.store.set('srstune', SRS.tuning);
  };

  function blankCard(id) {
    return {
      id: id, ease: 2.5, interval: 0, repetitions: 0,
      due: U.today(), lapses: 0, seen: 0, correct: 0, last: null
    };
  }

  /* Karta danej strony. Bez drugiego argumentu — strona receptywna. */
  SRS.card = function (recordId, side) {
    var id = SRS.cardId(recordId, side);
    if (!SRS.cards[id]) SRS.cards[id] = blankCard(id);
    return SRS.cards[id];
  };

  SRS.add = function (recordId, side) {
    var id = SRS.cardId(recordId, side);
    var isNew = !SRS.cards[id];
    SRS.card(id);
    if (isNew) SRS.save();
    return isNew;
  };

  /* Obie strony hasła naraz — tak wchodzą hasła z lekcji. Wytworzenie startuje
     z tego samego miejsca co rozpoznanie, ale w praktyce zostaje w tyle po
     kilku powtórkach, bo trudniej je zaliczyć. */
  SRS.addBoth = function (recordId) {
    var a = SRS.add(recordId, 'r');
    var b = SRS.add(recordId, 'p');
    return a || b;
  };

  SRS.has = function (recordId, side) {
    return !!SRS.cards[SRS.cardId(recordId, side)];
  };

  /* Hasło jest „w powtórkach”, jeśli ma choć jedną stronę. */
  SRS.hasAny = function (recordId) {
    return SRS.SIDES.some(function (s) { return SRS.has(recordId, s); });
  };

  SRS.addContrast = function (contrastId) {
    if (!contrastId) return false;
    return SRS.add(SRS.CONTRAST_PREFIX + contrastId);
  };

  SRS.contrastCards = function () {
    return Object.keys(SRS.cards).filter(SRS.isContrastCard);
  };

  SRS.remove = function (recordId, side) {
    delete SRS.cards[SRS.cardId(recordId, side)];
    SRS.save();
  };

  /* Usuwa wszystkie strony hasła — używane, gdy rekord zniknął z bazy. */
  SRS.removeAll = function (recordId) {
    SRS.SIDES.forEach(function (s) { delete SRS.cards[SRS.cardId(recordId, s)]; });
    delete SRS.cards[recordId];
    SRS.save();
  };

  function addDays(dateStr, days) {
    var d = new Date(dateStr + 'T00:00:00');
    d.setDate(d.getDate() + days);
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-'
      + String(d.getDate()).padStart(2, '0');
  }
  SRS.addDays = addDays;

  function daysBetween(a, b) {
    return Math.round((new Date(b + 'T00:00:00') - new Date(a + 'T00:00:00')) / 86400000);
  }

  /* ==================================================== migracja stron

     Kartoteka sprzed sesji P ma jedną kartę na hasło. Tamta karta powstawała
     głównie z ćwiczeń rozpoznawania, więc jej stan przechodzi na stronę
     receptywną jeden do jednego — bez zaokrągleń i bez utraty historii.

     Strona produktywna nie może dostać tego samego stanu, bo nikt jej nie
     ćwiczył: hasło rozpoznawane od pół roku wcale nie jest hasłem, które
     umiesz powiedzieć. Dostaje więc stan pochodny — krótszy odstęp i niższy
     licznik powtórek — i znacznik `derived`, żeby statystyka mogła uczciwie
     powiedzieć, skąd się wzięła. Liczniki `seen`, `correct` i `lapses`
     przechodzą w całości: to jest historia kontaktu z hasłem, wspólna dla
     obu stron, i jej kasowanie byłoby utratą danych.

     Przed zmianą powstaje kopia zapasowa, a `SRS.undoSplit()` przywraca stan
     sprzed migracji. */

  var SPLIT_MARK = 'srs.split.v1';
  var SPLIT_BACKUP = 'srs.split.backup';

  /* O ile skracamy odstęp, przenosząc go na stronę produktywną. 0,4 bierze się
     z tego, o ile wytworzenie zostaje w tyle za rozpoznaniem u kogoś, kto
     ćwiczył tylko rozpoznanie: mniej więcej dwa–trzy kroki SM-2. */
  var DERIVE_RATIO = 0.4;
  var DERIVE_CAP = 21;      // dni — pochodna strona nie startuje dalej niż tu

  SRS.deriveProductive = function (source, recordId) {
    var c = blankCard(SRS.cardId(recordId, 'p'));
    c.ease = source.ease || 2.5;
    c.interval = Math.min(DERIVE_CAP, Math.max(0, Math.round((source.interval || 0) * DERIVE_RATIO)));
    c.repetitions = Math.max(0, Math.floor((source.repetitions || 0) / 2));
    c.lapses = source.lapses || 0;
    c.seen = source.seen || 0;
    c.correct = source.correct || 0;
    c.last = source.last || null;
    c.due = c.interval > 0 ? addDays(U.today(), c.interval) : U.today();
    c.derived = true;
    if (source.slow) c.slow = true;
    return c;
  };

  SRS.needsSplit = function () {
    return Object.keys(SRS.cards).some(function (id) {
      return !SRS.isContrastCard(id) && id.indexOf(SEP) === -1;
    });
  };

  SRS.migrateSides = function () {
    if (!SRS.needsSplit()) return null;

    U.store.set(SPLIT_BACKUP, { cards: SRS.cards, log: SRS.log, date: U.today() });

    var legacy = Object.keys(SRS.cards).filter(function (id) {
      return !SRS.isContrastCard(id) && id.indexOf(SEP) === -1;
    });

    var report = { moved: 0, derived: 0, kept: 0, date: U.today() };
    legacy.forEach(function (id) {
      var old = SRS.cards[id];
      delete SRS.cards[id];

      var rec = old;
      rec.id = SRS.cardId(id, 'r');
      SRS.cards[rec.id] = rec;
      report.moved += 1;

      var prodId = SRS.cardId(id, 'p');
      if (!SRS.cards[prodId]) {
        SRS.cards[prodId] = SRS.deriveProductive(old, id);
        report.derived += 1;
      }
    });
    report.kept = SRS.contrastCards().length;

    /* Dziennik sprzed rozdzielenia opisuje powtórki rozpoznawania — dopisujemy
       mu stronę, żeby pętla zwrotna nie liczyła go jako „nieznanej strony”. */
    SRS.log = (SRS.log || []).map(function (e) {
      if (!e.s) e.s = 'r';
      return e;
    });

    U.store.set(SPLIT_MARK, report);
    SRS.save();
    return report;
  };

  SRS.splitReport = function () { return U.store.get(SPLIT_MARK, null); };

  SRS.undoSplit = function () {
    var backup = U.store.get(SPLIT_BACKUP, null);
    if (!backup) return false;
    SRS.cards = backup.cards || {};
    SRS.log = backup.log || [];
    U.store.set(SPLIT_MARK, null);
    SRS.save();
    return true;
  };

  /* ================================================ pętla zwrotna z krzywej

     REGUŁA. Po każdej dziesiątej ocenie przeliczamy retencję tego użytkownika
     w rozbiciu na przedziały odstępu — dokładnie te same przedziały, które
     rysuje krzywa zapamiętywania na ekranie Postęp. Dla każdego przedziału
     z dostateczną liczbą prób liczymy, jak bardzo wypada poza okno docelowe
     85–90 %, i z tych odchyleń — ważonych liczbą prób — składamy jedną korektę:

         retencja < 85 %  ->  przemnóż mnożnik przez 1 - (0,85 - r) * 2,0
         retencja > 90 %  ->  przemnóż mnożnik przez 1 + (r - 0,90) * 2,0
         pomiędzy         ->  zostaw (odstępy są dobrze dobrane)

     Uwaga, na której ta reguła stoi, a którą łatwo przeoczyć: korekta jest
     MNOŻONA przez dotychczasowy mnożnik, a nie ustawiana jako jego nowa
     wartość. Pierwsza wersja liczyła mnożnik wprost z retencji i miała wadę
     każdego regulatora proporcjonalnego — trwały uchyb. Mnożnik zbiegał do
     punktu, w którym korekta zerowała się przy retencji 65 %, i tam zostawał:
     algorytm „godził się” z tym, że co trzecie hasło wypada z pamięci, bo
     przy tej retencji jego własna formuła nie kazała już nic zmieniać.
     Wersja mnożąca zachowuje się jak regulator całkujący: dopóki retencja
     jest poza oknem, mnożnik dalej się przesuwa. Zatrzymuje się dopiero
     wtedy, gdy uczący się faktycznie trafia w okno.

     Pojedynczą korektę ograniczamy do ±10 % (`maxStep`), żeby jeden zły
     tydzień nie przestawił całej kartoteki, a całość tłumimy pewnością
     (`próby / 2 × minimum`) — na starcie nauki mnożnik stoi na 1,0 i rusza
     dopiero, gdy jest z czego liczyć.

     Liczymy osobno dla każdej strony karty, bo to są osobne siły pamięci —
     ktoś może rozpoznawać z retencją 94 % i wytwarzać z retencją 71 %,
     i wtedy jego odstępy receptywne mają rosnąć, a produktywne maleć. */

  var TUNE = {
    low: 0.85,          // próg, poniżej którego skracamy
    high: 0.90,         // próg, powyżej którego wydłużamy
    downGain: 2.0,
    upGain: 2.0,
    /* Ile najwyżej wolno przesunąć mnożnik przy jednym przeliczeniu. Regulator
       całkujący dochodzi do celu sumą małych kroków, więc krok ma być mały:
       przy 10 % co dziesiątą ocenę mnożnik zjeżdżał do granicy zakresu
       w ciągu pierwszych dni nauki — czyli w chwili, gdy dane były jeszcze
       przypadkowe — i potem długo wracał. Sześć procent co dwadzieścia pięć
       ocen daje pętli czas na zebranie dowodów, zanim zmieni odstępy. */
    maxStep: 0.06,
    minSamples: 30,     // ile powtórek strony, zanim mnożnik ruszy z 1,0
    bucketMin: 8,       // ile powtórek w przedziale, żeby go liczyć
    /* Od ilu dni odstępu przedział w ogóle bierzemy pod uwagę.

       Przedziały najkrótsze — jeden dzień, dwa–trzy dni — są zapełnione
       kartami, które właśnie wypadły i wróciły od zera. Ich trafność jest
       z natury kiepska i ALGORYTM NIE MA NA NIĄ WPŁYWU: krócej niż jeden
       dzień i tak nie zaplanuje. Wliczanie ich do dostrajania to pogoń za
       celem, którego nie da się osiągnąć — mnożnik zjeżdżałby do podłogi
       i tam został, bez względu na to, jak dobrze idzie reszta kartoteki.
       Dostrajamy więc na kartach dojrzałych, tam gdzie skrócenie albo
       wydłużenie odstępu naprawdę coś zmienia. */
    matureFrom: 4,      // dni
    window: 400,        // ile ostatnich powtórek strony bierzemy pod uwagę
    step: 1.0,          // ile z wyliczonej korekty przyjmujemy (1 = całą)
    /* Podłoga musi leżeć niżej, niż podpowiada intuicja. Mnożnik skaluje TEMPO
       WZROSTU odstępów, a nie ich punkt wyjścia: przy mnożniku 0,60 odstęp
       rośnie 2,5 × 0,60 = 1,5 raza na powtórkę. Jeśli pamięć uczącego się
       umacnia się dokładnie w tym tempie, odstępy i pamięć rosną równolegle —
       i retencja zostaje na tyle, ile wyszło na starcie, choćby była fatalna.
       Żeby ją podnieść, algorytm musi móc na jakiś czas rosnąć WOLNIEJ niż
       pamięć, a do tego potrzebuje zejść wyraźnie poniżej tej równowagi.
       Stąd 0,40: przy nim odstępy praktycznie przestają rosnąć, hasła nadganiają,
       retencja wraca do okna i mnożnik sam się podnosi. */
    min: 0.40,
    max: 1.60,
    every: 25           // co ile ocen przeliczamy
  };
  SRS.TUNE = TUNE;

  function blankTuning() {
    var t = { since: 0 };
    SRS.SIDES.forEach(function (s) {
      t[s] = { factor: 1, retention: null, samples: 0, updated: null };
    });
    return t;
  }

  function tuningFor(side) {
    if (!SRS.tuning) SRS.tuning = blankTuning();
    if (!SRS.tuning[side]) SRS.tuning[side] = { factor: 1, retention: null, samples: 0, updated: null };
    return SRS.tuning[side];
  }

  SRS.factor = function (side) {
    var t = tuningFor(side || 'r');
    var f = typeof t.factor === 'number' ? t.factor : 1;
    return Math.max(TUNE.min, Math.min(TUNE.max, f));
  };

  /* Korekta dla jednej zmierzonej retencji — o ile PRZEMNOŻYĆ dotychczasowy
     mnożnik. Zwraca 1, gdy nie ma czego poprawiać. Wydzielona, bo test
     sprawdza ją osobno: reguła musi dać się przeczytać i sprawdzić bez
     uruchamiania całej pętli. */
  SRS.tuneProposal = function (retention) {
    if (retention === null || retention === undefined) return 1;
    var raw = 1;
    if (retention < TUNE.low) raw = 1 - (TUNE.low - retention) * TUNE.downGain;
    else if (retention > TUNE.high) raw = 1 + (retention - TUNE.high) * TUNE.upGain;
    return Math.max(1 - TUNE.maxStep, Math.min(1 + TUNE.maxStep, raw));
  };

  SRS.retune = function (side) {
    var t = tuningFor(side);
    var entries = (SRS.log || []).filter(function (e) {
      return (e.s || 'r') === side && e.iv >= 1;
    });
    if (entries.length > TUNE.window) entries = entries.slice(-TUNE.window);

    var buckets = SRS.retention(side, entries);

    /* Zbieramy korekty z przedziałów dojrzałych. Gdyby żaden się nie
       kwalifikował, powtarzamy zbieranie z progiem obniżonym do dwóch dni —
       i to nie jest kosmetyka, tylko wyjście z zakleszczenia. Bez tego pętla
       mogła się zapętlić na trwałe: mnożnik spada, odstępy przestają
       przekraczać cztery dni, więc znika materiał, z którego liczy się
       korekta, więc mnożnik już nigdy nie ruszy — nawet gdy uczący się
       zacznie trafiać bezbłędnie. Algorytm musi widzieć swoje własne skutki,
       także wtedy, gdy sam zepchnął się w krótkie odstępy. */
    function gather(floorDays) {
      var w = 0, ps = 0;
      buckets.forEach(function (b) {
        if (b.total < TUNE.bucketMin) return;
        if (b.min < floorDays) return;
        var p = SRS.tuneProposal(b.ok / b.total);
        ps += p * b.total;
        w += b.total;
      });
      return { weight: w, sum: ps };
    }

    var ok = 0, total = 0;
    buckets.forEach(function (b) { total += b.total; ok += b.ok; });

    var g = gather(TUNE.matureFrom);
    if (!g.weight) g = gather(2);
    var wSum = g.weight, pSum = g.sum;

    t.samples = total;
    t.retention = total ? ok / total : null;

    var correction = wSum ? pSum / wSum : 1;
    /* Dopóki prób jest mało, tłumimy korektę — inaczej pięć wpadek na starcie
       ustawiałoby odstępy na pół roku nauki do przodu. */
    var confidence = Math.min(1, total / (TUNE.minSamples * 2));
    if (total < TUNE.minSamples) confidence = 0;
    var applied = 1 + (correction - 1) * confidence * TUNE.step;

    /* Mnożenie, nie podstawienie — powód w komentarzu do reguły wyżej. */
    var next = t.factor * applied;
    t.factor = Math.max(TUNE.min, Math.min(TUNE.max, Math.round(next * 1000) / 1000));
    t.updated = U.today();
    return t;
  };

  SRS.retuneAll = function () {
    SRS.SIDES.forEach(function (s) { SRS.retune(s); });
    SRS.tuning.since = 0;
    return SRS.tuning;
  };

  /* Sprawozdanie dla ekranu Postęp i dla dokumentacji: co pętla widzi
     i co z tym zrobiła. */
  SRS.tuningReport = function (side) {
    var t = tuningFor(side);
    var buckets = SRS.retention(side).filter(function (b) { return b.total > 0; });
    return {
      side: side,
      name: SRS.sideName(side),
      factor: t.factor,
      retention: t.retention === null ? null : Math.round(t.retention * 100),
      samples: t.samples,
      updated: t.updated,
      active: t.samples >= TUNE.minSamples,
      buckets: buckets.map(function (b) {
        return { label: b.label, total: b.total, rate: b.rate,
                 mature: b.min >= TUNE.matureFrom,
                 proposal: (b.total >= TUNE.bucketMin && b.min >= TUNE.matureFrom)
                   ? Math.round(SRS.tuneProposal(b.ok / b.total) * 100) / 100 : null };
      }),
      verdict: t.samples < TUNE.minSamples
        ? 'Za mało powtórek — odstępy liczą się na razie bez korekty.'
        : (t.factor < 0.97 ? 'Odstępy skrócone: hasła wypadały z pamięci szybciej, niż zakładał algorytm.'
          : (t.factor > 1.03 ? 'Odstępy wydłużone: pamiętasz lepiej, niż zakładał algorytm.'
            : 'Odstępy bez zmian — trafiają w Twoją krzywą.'))
    };
  };

  /* ======================================================== ocenianie

     quality: 0 = nie pamiętam, 3 = trudne, 4 = dobrze, 5 = łatwe

     opts.side: 'r' | 'p' | 'w' — której siły pamięci dotyczy odpowiedź.
     opts.pace: 'slow' | 'ok' | 'fast' — jak szybko padła odpowiedź.
     Hasło odtworzone poprawnie, ale wolno, jest opanowane biernie: w rozmowie
     nie zdąży się go użyć. SM-2 samo tego nie widzi, bo zna wyłącznie
     poprawność, więc skracamy takiej karcie odstęp o 40 % i zostawiamy na niej
     znacznik. Odpowiedź szybka znacznik zdejmuje. */
  SRS.grade = function (recordId, quality, opts) {
    opts = opts || {};
    if (quality === null || quality === undefined) return null;
    var id = SRS.cardId(recordId, opts.side);
    var side = SRS.sideOf(id);
    var c = SRS.card(id);

    /* Zapis do krzywej zapamiętywania robimy PRZED zmianą karty: interesuje
       nas, po ilu dniach przerwy hasło zostało odtworzone i czy się udało.
       Po aktualizacji ta informacja jest już nie do odzyskania. */
    if (c.repetitions > 0 || c.interval > 0) {
      /* Zapisujemy FAKTYCZNĄ przerwę, nie zaplanowany odstęp. Różnica bywa
         duża: karta przesunięta przez rozkładanie zaległości albo zastana po
         urlopie wraca po dziesięciu dniach, choć algorytm planował trzy.
         Gdyby do krzywej trafiała trójka, pętla zwrotna czytałaby wpadkę jako
         „mój trzydniowy odstęp jest za długi” i skracała odstępy za cudzy
         błąd — a przy większych zaległościach nakręcałaby się sama: krótsze
         odstępy to większa kolejka, większa kolejka to więcej przesunięć,
         więcej przesunięć to więcej wpadek. Krzywa ma zresztą odpowiadać na
         pytanie „po ilu dniach przerwy nadal pamiętasz”, więc liczy się
         przerwa rzeczywista. */
      var elapsed = c.last ? daysBetween(c.last, U.today()) : c.interval;
      if (!(elapsed > 0)) elapsed = c.interval;
      SRS.log.push({
        d: U.today(),
        iv: elapsed,                          // rzeczywista przerwa w dniach
        ok: quality >= 3 ? 1 : 0,
        s: side                               // której strony dotyczy
      });
      if (SRS.log.length > LOG_LIMIT) SRS.log = SRS.log.slice(-LOG_LIMIT);
    }

    c.seen += 1;
    c.last = U.today();

    var factor = SRS.factor(side);

    if (quality < 3) {
      c.repetitions = 0;
      c.interval = 1;
      c.lapses += 1;
    } else {
      c.correct += 1;
      c.repetitions += 1;
      if (c.repetitions === 1) c.interval = 1;
      else if (c.repetitions === 2) c.interval = Math.max(1, Math.round(6 * factor));
      else c.interval = Math.max(1, Math.round(c.interval * c.ease * factor));
      c.ease = c.ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
      if (c.ease < 1.3) c.ease = 1.3;
      if (c.ease > 2.8) c.ease = 2.8;
    }
    if (opts.pace === 'slow' && quality >= 3) {
      c.slow = true;
      c.interval = Math.max(1, Math.round(c.interval * 0.6));
    } else if (opts.pace === 'fast' || quality < 3) {
      delete c.slow;
    }

    if (c.interval > 365) c.interval = 365;
    c.due = addDays(U.today(), c.interval);
    delete c.postponed;

    /* Pętla zwrotna: co dziesiątą ocenę przeliczamy mnożniki z dziennika. */
    if (!SRS.tuning) SRS.tuning = blankTuning();
    SRS.tuning.since = (SRS.tuning.since || 0) + 1;
    if (SRS.tuning.since >= TUNE.every) SRS.retuneAll();

    SRS.save();
    return c;
  };

  /* Wygodne skróty, żeby wywołania z ekranów czytały się jak zdanie. */
  SRS.gradeReceptive = function (id, q, opts) {
    opts = opts || {}; opts.side = 'r'; return SRS.grade(id, q, opts);
  };
  SRS.gradeProductive = function (id, q, opts) {
    opts = opts || {}; opts.side = 'p'; return SRS.grade(id, q, opts);
  };

  /* ============================================ trzeci wymiar: wymowa

     Hasło zaliczone receptywnie i produktywnie, ale wymawiane z błędnym tonem,
     nie jest hasłem opanowanym — jest hasłem, którego rozmówca nie zrozumie.
     Taki przypadek nie ma jak wrócić w zwykłych powtórkach: obie strony są
     „na zielono”, więc kolejka o nie nie zapyta. Dlatego dostaje własną kartę.

     Kartę zakładamy dopiero wtedy, gdy obie pozostałe strony są opanowane —
     wcześniej błędny ton jest zwyczajną częścią uczenia się hasła i nie ma
     sensu robić z niego osobnego ćwiczenia. */

  var LEARNED = { repetitions: 2, interval: 6 };
  SRS.LEARNED = LEARNED;

  SRS.isLearned = function (recordId, side) {
    var c = SRS.cards[SRS.cardId(recordId, side)];
    return !!c && c.repetitions >= LEARNED.repetitions && c.interval >= LEARNED.interval;
  };

  /* Wynik oceny wymowy (ToneScore) trafia tutaj. Zwraca opis tego, co się
     stało — ekran może z tego zrobić komunikat. */
  SRS.notePronunciation = function (recordId, result) {
    if (!result || !result.ok) return null;
    var wrong = (result.syllables || []).filter(function (s) { return !s.ok; });
    var id = SRS.cardId(recordId, 'w');
    var exists = !!SRS.cards[id];

    if (!wrong.length) {
      /* Trafione tony. Jeśli karta wymowy istnieje, podnosimy ją; jeśli nie —
         nie zakładamy jej, bo nie ma czego ćwiczyć. */
      if (!exists) return null;
      var q = result.score >= 85 ? 5 : (result.score >= 70 ? 4 : 3);
      var up = SRS.grade(recordId, q, { side: 'w' });
      delete up.tone;
      if (up.repetitions >= 3 && result.score >= 85) {
        /* Trzy czyste podejścia z rzędu — hasło wraca do zwykłego obiegu. */
        SRS.remove(recordId, 'w');
        return { action: 'closed', record: recordId };
      }
      SRS.save();
      return { action: 'up', record: recordId, card: up };
    }

    if (!exists && !(SRS.isLearned(recordId, 'r') && SRS.isLearned(recordId, 'p'))) {
      /* Hasła jeszcze się uczysz — błędny ton obsłuży karta produktywna. */
      return null;
    }

    var card = SRS.card(recordId, 'w');
    card.tone = {
      syllable: wrong[0].label || wrong[0].plain || '',
      expected: wrong[0].expectedTone,
      produced: wrong[0].producedTone,
      fix: wrong[0].fix || '',
      score: result.score,
      date: U.today()
    };
    var quality = result.score >= 55 ? 3 : 0;
    SRS.grade(recordId, quality, { side: 'w' });
    return { action: exists ? 'again' : 'opened', record: recordId, tone: card.tone };
  };

  SRS.pronunciationCards = function () {
    return Object.keys(SRS.cards)
      .filter(function (id) { return SRS.sideOf(id) === 'w'; })
      .map(function (id) { return SRS.cards[id]; });
  };

  /* ============================================== kolejka i jej rozłożenie

     Sufit dzienny bierze się z tego, ile ten uczący się faktycznie robi:
     mediana odpowiedzi z ostatnich dwóch tygodni, ograniczona z dołu i z góry.
     Ktoś, kto robi po 25 odpowiedzi dziennie, nie dostanie kolejki na 300 —
     dostanie kolejkę na tyle, ile robi, i informację, że reszta czeka. */

  var CAP = { min: 20, max: 120, fallback: 40 };
  SRS.CAP = CAP;

  /* Zapas ponad zmierzone tempo. Bez niego sufit byłby pułapką: liczylibyśmy
     go z liczby odpowiedzi, która sama jest przez ten sufit ograniczona, więc
     raz ustawiony na 20 nie mógłby już nigdy urosnąć — nawet gdyby uczący się
     chciał robić więcej. Ćwierć zapasu pozwala tempu rosnąć stopniowo, jeśli
     uczący się faktycznie wyrabia całą kolejkę. */
  var HEADROOM = 1.25;

  SRS.dailyCap = function () {
    var goal = 0;
    if (global.Progress && Progress.data) {
      var days = Progress.data.days || {};
      var keys = Object.keys(days).sort().slice(-14);
      var counts = keys.map(function (k) { return days[k].answers || 0; })
        .filter(function (n) { return n > 0; });
      if (counts.length >= 3) {
        counts.sort(function (a, b) { return a - b; });
        var mid = Math.floor(counts.length / 2);
        goal = counts.length % 2 ? counts[mid] : Math.round((counts[mid - 1] + counts[mid]) / 2);
      } else if (Progress.data.goal) {
        goal = Progress.data.goal * 2;
      }
    }
    if (!goal) goal = CAP.fallback;
    return Math.max(CAP.min, Math.min(CAP.max, Math.round(goal * HEADROOM)));
  };

  /* Jak bardzo hasło jest „na krawędzi zapomnienia”: ile czasu minęło ponad
     zaplanowany odstęp, w stosunku do samego odstępu. Karta z odstępem
     jednodniowym, przetrzymana trzy dni, jest w gorszym stanie niż karta
     z odstępem sześćdziesięciodniowym przetrzymana trzy dni. */
  SRS.urgency = function (card, today) {
    var over = daysBetween(card.due, today || U.today());
    if (over < 0) over = 0;
    var base = Math.max(1, card.interval || 1);
    return Math.min(4, over / base);
  };

  function frequencyOf(recordId) {
    if (!recordId || !global.DB || !DB.any) return 0;
    var rec = DB.any(recordId);
    return rec && typeof rec.frequency === 'number' ? rec.frequency : 0;
  }

  /* Wynik priorytetu. Kolejność składników jest kolejnością wagi:
     najpierw bliskość zapomnienia, potem częstość hasła w mowie, potem
     historia wpadek i znacznik „umiem, ale wolno”. */
  SRS.priority = function (card, today) {
    var rid = SRS.recordOf(card.id);
    var freq = frequencyOf(rid) / 5;          // frequency w bazie: 0–5
    var score = SRS.urgency(card, today) * 1.0
      + Math.min(1.2, freq) * 0.6
      + Math.min(1, (card.lapses || 0) / 4) * 0.4
      + (card.slow ? 0.2 : 0);
    /* Kontrast słuchowy jest fundamentem — jeśli ucho nie słyszy różnicy,
       reszta powtórek pracuje na darmo. */
    if (SRS.isContrastCard(card.id)) score += 0.5;
    /* Karta wymowy dotyczy hasła już opanowanego — może poczekać dzień. */
    if (SRS.sideOf(card.id) === 'w') score -= 0.15;
    return score;
  };

  /* Pełna lista zaległych, posortowana priorytetem. To jest surowa prawda
     o kartotece — ekran jej nie pokazuje, korzysta z SRS.plan(). */
  SRS.dueList = function (today) {
    var day = today || U.today();
    return Object.keys(SRS.cards)
      .map(function (id) { return SRS.cards[id]; })
      .filter(function (c) { return c.due <= day; })
      .sort(function (a, b) {
        var d = SRS.priority(b, day) - SRS.priority(a, day);
        if (Math.abs(d) > 0.0001) return d;
        if (a.due !== b.due) return a.due < b.due ? -1 : 1;
        return (b.lapses || 0) - (a.lapses || 0);
      });
  };

  /* Plan na dziś: co pokazujemy, ile zostaje i na ile dni to rozłożone. */
  SRS.plan = function (opts) {
    opts = opts || {};
    var today = opts.today || U.today();
    var cap = opts.cap || SRS.dailyCap();
    var all = SRS.dueList(today);
    var todayList = all.slice(0, cap);
    var rest = all.slice(cap);
    return {
      today: todayList,
      cap: cap,
      dueTotal: all.length,
      backlog: rest.length,
      days: rest.length ? Math.ceil(rest.length / cap) + 1 : 1,
      rest: rest
    };
  };

  /* Rozłożenie zaległości. Nadmiar dostaje nowe terminy w kolejnych dniach,
     po `cap` na dzień, ale nie dalej niż `HORIZON` dni w przód — dłuższe
     odkładanie przestaje być planem, a zaczyna być udawaniem, że kartoteka
     jest mniejsza. Karta przesunięta dostaje znacznik `postponed`; jej odstęp
     się od tego nie wydłuża, bo SM-2 liczy od zapisanego `interval`, a nie od
     tego, ile faktycznie minęło. */
  var HORIZON = 14;
  SRS.HORIZON = HORIZON;

  SRS.spreadBacklog = function (opts) {
    opts = opts || {};
    var today = opts.today || U.today();
    var cap = opts.cap || SRS.dailyCap();
    var plan = SRS.plan({ today: today, cap: cap });
    if (!plan.backlog) return { moved: 0, days: 1, cap: cap };

    var moved = 0, day = 1, inDay = 0, maxDay = 1;
    plan.rest.forEach(function (card) {
      if (inDay >= cap) { day += 1; inDay = 0; }
      if (day > HORIZON) day = HORIZON;

      /* Ile wolno przesunąć TĘ kartę. Nie wszystkie znoszą odkładanie tak
         samo: karta z odstępem sześćdziesięciodniowym poczeka tydzień i nic
         się nie stanie, a karta z odstępem trzydniowym po tygodniu jest
         zapomniana. Limit ustawiamy na połowę własnego odstępu karty, bo
         to jest miara jej kruchości, jaką mamy pod ręką.

         Bez tego ograniczenia rozkładanie zaległości samo psuło naukę: świeże
         hasła (krótkie odstępy) lądowały na końcu kolejki, wracały po dwóch
         tygodniach i wypadały z pamięci — a pętla zwrotna czytała to jako
         „odstępy są za długie” i skracała je jeszcze bardziej, przez co
         kolejka rosła. Nauka potrafi się w ten sposób rozkręcić w dół. */
      var limit = Math.max(1, Math.min(HORIZON, Math.ceil((card.interval || 1) * 0.5)));
      var shift = Math.min(day, limit);

      card.due = addDays(today, shift);
      card.postponed = today;
      inDay += 1;
      moved += 1;
      if (shift > maxDay) maxDay = shift;
    });
    SRS.save();
    return { moved: moved, days: maxDay + 1, cap: cap };
  };

  /* ====================================================== statystyka */

  SRS.stats = function (today) {
    var day = today || U.today();
    var next = addDays(day, 1);
    var ids = Object.keys(SRS.cards);
    var out = { total: ids.length, records: 0, due: 0, learned: 0, hard: 0,
                tomorrow: 0, slow: 0, pronunciation: 0 };
    var records = {};
    ids.forEach(function (id) {
      var c = SRS.cards[id];
      var rid = SRS.recordOf(id);
      if (rid) records[rid] = true;
      if (c.due <= day) out.due += 1;
      else if (c.due === next) out.tomorrow += 1;
      if (c.repetitions >= 3 && c.interval >= 6) out.learned += 1;
      if (c.lapses >= 2) out.hard += 1;
      if (c.slow) out.slow += 1;
      if (SRS.sideOf(id) === 'w') out.pronunciation += 1;
    });
    out.records = Object.keys(records).length;
    return out;
  };

  /* Statystyka w rozbiciu na strony — to jest liczba, dla której powstało
     rozdzielenie kart. Różnica między rozpoznaniem a wytworzeniem ma być
     widoczna, nie zamiecona pod średnią. */
  SRS.sideStats = function (today) {
    var day = today || U.today();
    var out = {};
    SRS.SIDES.forEach(function (s) {
      out[s] = { side: s, name: SRS.sideName(s), long: SRS.SIDE_LONG[s],
                 total: 0, learned: 0, due: 0, lapses: 0,
                 intervalSum: 0, seen: 0, correct: 0,
                 factor: SRS.factor(s), retention: null };
    });
    Object.keys(SRS.cards).forEach(function (id) {
      var side = SRS.sideOf(id);
      if (!out[side]) return;
      var c = SRS.cards[id];
      var b = out[side];
      b.total += 1;
      b.intervalSum += c.interval || 0;
      b.lapses += c.lapses || 0;
      b.seen += c.seen || 0;
      b.correct += c.correct || 0;
      if (c.due <= day) b.due += 1;
      if (c.repetitions >= 3 && c.interval >= 6) b.learned += 1;
    });
    SRS.SIDES.forEach(function (s) {
      var b = out[s];
      b.avgInterval = b.total ? Math.round(b.intervalSum / b.total * 10) / 10 : 0;
      b.accuracy = b.seen ? Math.round(b.correct / b.seen * 100) : null;
      var t = tuningFor(s);
      b.retention = t.retention === null ? null : Math.round(t.retention * 100);
      b.samples = t.samples;
    });
    return out;
  };

  /* Ile poziomów wytworzenie zostaje za rozpoznaniem. „Poziom” to krok SM-2 —
     liczymy go z ilorazu średnich odstępów, bo odstęp rośnie mniej więcej
     geometrycznie z każdą trafną powtórką. */
  SRS.sideGap = function () {
    var s = SRS.sideStats();
    var r = s.r, p = s.p;
    if (!r.total || !p.total) return null;
    var ratio = (p.avgInterval + 1) / (r.avgInterval + 1);
    var steps = Math.log(ratio) / Math.log(2.5);
    return {
      receptive: r, productive: p,
      steps: Math.round(Math.abs(steps) * 10) / 10,
      behind: steps < 0,
      learnedGap: r.learned - p.learned
    };
  };

  /* Najczęściej mylone hasła — do sekcji „Nad czym popracować”. */
  SRS.troubles = function (limit) {
    return Object.keys(SRS.cards)
      .map(function (id) { return SRS.cards[id]; })
      .filter(function (c) { return c.lapses > 0; })
      .sort(function (a, b) { return b.lapses - a.lapses || a.ease - b.ease; })
      .slice(0, limit || 10);
  };

  /* Krzywa zapamiętywania: dla każdego przedziału odstępu liczymy, jaki
     odsetek powtórek się udał. To realna krzywa tego użytkownika, a nie
     teoretyczna krzywa Ebbinghausa.

     side — opcjonalnie ogranicza krzywą do jednej strony karty.
     entries — opcjonalnie gotowa lista wpisów (używa jej pętla zwrotna,
     żeby nie filtrować dziennika dwa razy). */
  SRS.retention = function (side, entries) {
    var buckets = [
      { label: '1 dzień', min: 1, max: 1 },
      { label: '2–3 dni', min: 2, max: 3 },
      { label: '4–7 dni', min: 4, max: 7 },
      { label: '8–15 dni', min: 8, max: 15 },
      { label: '16–30 dni', min: 16, max: 30 },
      { label: '31–60 dni', min: 31, max: 60 },
      { label: '61+ dni', min: 61, max: 100000 }
    ];
    buckets.forEach(function (b) { b.total = 0; b.ok = 0; });
    var src = entries || (SRS.log || []);
    src.forEach(function (e) {
      if (side && (e.s || 'r') !== side) return;
      for (var i = 0; i < buckets.length; i++) {
        if (e.iv >= buckets[i].min && e.iv <= buckets[i].max) {
          buckets[i].total += 1;
          buckets[i].ok += e.ok;
          return;
        }
      }
    });
    buckets.forEach(function (b) {
      b.rate = b.total ? Math.round(b.ok / b.total * 100) : null;
    });
    return buckets;
  };

  /* Jeśli kolejka pusta, dokładamy nowe hasła wg częstotliwości i poziomu.
     Losujemy z indeksu, nie z wczytanych plików — inaczej propozycje
     ograniczałyby się do tego, co akurat leży w pamięci. */
  SRS.suggestNew = function (count, level) {
    var source = DB.index && DB.index.length ? DB.index : DB.records;
    var pool = source.filter(function (r) {
      if (SRS.hasAny(r.id)) return false;
      if (level && r.level !== level) return false;
      return true;
    });
    pool.sort(function (a, b) { return b.frequency - a.frequency || a.difficulty - b.difficulty; });
    return pool.slice(0, count || 10);
  };

  global.SRS = SRS;
})(window);
