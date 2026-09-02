/* Thai All-in-One — gramatyka w statystyce.

   PYTANIE, NA KTÓRE TEN MODUŁ ODPOWIADA
   =====================================

   Rozkład błędów z sesji I miał już wymiar gramatyczny, ale mierzył jedną
   liczbę na temat: „ile pomyłek w temacie X”. Przy 26 tematach przypisanych
   rotacyjnie ta liczba i tak nic nie znaczyła — mówiła o lekcji, nie
   o konstrukcji.

   Przy progresji i osiemdziesięciu tematach można zapytać o coś ostrzejszego:
   **które konstrukcje uczący się ROZUMIE, ale nie PRODUKUJE.** To nie jest
   ten sam brak i nie naprawia się go tym samym ćwiczeniem.

     rozumienie  — wykrywanie struktury ze słuchu, sprawdzian lekcji
     produkcja   — przekształcenia, układanie zdań z wzorcem

   Ktoś, kto bezbłędnie wskazuje „to było pytanie”, a nie potrafi zamienić
   zdania w pytanie, ma lukę w produkcji, nie w rozumieniu. Wysłanie go na
   kolejne ćwiczenie odsłuchowe jest stratą czasu — a dokładnie to robiłaby
   statystyka mierząca jedną liczbę.

   DLACZEGO PRÓG PRÓB JEST WYSOKI
   ==============================

   Temat oceniamy dopiero od MIN_ANSWERS prób NA STRONĘ. Dwie pomyłki z dwóch
   prób to przypadek, a nie wiedza o uczącym się — a przy osiemdziesięciu
   tematach takich przypadków byłoby na ekranie kilkadziesiąt i zasypałyby
   te trzy, które coś znaczą. */
(function (global) {
  'use strict';

  var GStats = {};

  /* Ile prób musi paść, żeby liczba znaczyła cokolwiek. Osobno dla każdej
     strony, bo temat bywa ćwiczony receptywnie dziesięć razy i produkcyjnie
     ani razu — a wtedy „nie produkuje” jest wnioskiem z braku danych. */
  var MIN_ANSWERS = 6;

  /* Próg, poniżej którego mówimy „nie produkuje”. Osiemdziesiąt procent to
     ten sam próg, którym kurs zalicza lekcję — nie ma powodu, żeby ta sama
     umiejętność miała tu inną poprzeczkę. */
  var GOOD = 0.8;

  /* Różnica między stronami, od której warto o niej mówić. Poniżej
     dwudziestu punktów procentowych to szum dwóch sesji. */
  var GAP = 0.2;

  function bucket() {
    var d = Progress.data;
    if (!d.grammarSides) d.grammarSides = {};
    return d.grammarSides;
  }

  function cell(topicId, side) {
    var all = bucket();
    var row = all[topicId] || (all[topicId] = {});
    return row[side] || (row[side] = { answers: 0, correct: 0 });
  }

  /* Z identyfikatora rekordu na temat gramatyczny.

     Rekord nie wie, jaką konstrukcję ilustruje — wie to lekcja, w której
     stoi. Idziemy więc przez lekcję: rekord należy do lekcji, lekcja ma
     temat. Rekord spoza ścieżki (materiał ćwiczeń dobierany z całej bazy)
     tematu nie dostaje i do statystyki nie wchodzi — zgadywanie tematu po
     samym zapisie dałoby liczby, których nie da się obronić. */
  var recordToTopic = null;

  function topicOf(recordId) {
    if (!recordToTopic) {
      recordToTopic = {};
      (DB.lessons || []).forEach(function (L) {
        (L.recordIds || []).forEach(function (rid) {
          recordToTopic[rid] = L.grammarId;
        });
      });
    }
    return recordToTopic[recordId] || null;
  }

  GStats.reset = function () { recordToTopic = null; };

  /* Odpowiedź w ćwiczeniu, przypisana do strony. Wołane z Gram i z lekcji. */
  GStats.answer = function (recordId, correct, side) {
    var topic = topicOf(recordId);
    if (!topic || (side !== 'receptive' && side !== 'productive')) return null;
    var c = cell(topic, side);
    c.answers += 1;
    if (correct) c.correct += 1;
    Progress.save();
    return c;
  };

  function share(c) {
    return c.answers ? c.correct / c.answers : 0;
  }

  /* Pełna tabela: temat, obie strony, dystans między nimi. */
  GStats.table = function () {
    var all = bucket();
    return (DB.grammar || []).map(function (g) {
      var r = all[g.id] && all[g.id].receptive || { answers: 0, correct: 0 };
      var p = all[g.id] && all[g.id].productive || { answers: 0, correct: 0 };
      return {
        id: g.id,
        title: g.title,
        stage: g.stage,
        stageTitle: g.stageTitle,
        family: g.family,
        introducedAt: g.introducedAt,
        receptive: { answers: r.answers, correct: r.correct, share: share(r) },
        productive: { answers: p.answers, correct: p.correct, share: share(p) },
        gap: share(r) - share(p),
        rated: r.answers >= MIN_ANSWERS && p.answers >= MIN_ANSWERS
      };
    });
  };

  /* Konstrukcje rozumiane, ale nieprodukowane — sedno tego modułu.

     Warunek jest koniunkcją trzech rzeczy i każda z nich odsiewa inny fałszywy
     alarm:
       * obie strony mają dość prób (inaczej to brak danych, nie brak
         umiejętności),
       * strona receptywna jest opanowana (inaczej to nie luka produkcyjna,
         tylko po prostu nieznany temat),
       * dystans przekracza GAP (inaczej to szum). */
  GStats.understoodNotProduced = function (limit) {
    var out = GStats.table().filter(function (t) {
      return t.rated && t.receptive.share >= GOOD
        && t.productive.share < GOOD && t.gap >= GAP;
    });
    out.sort(function (a, b) { return b.gap - a.gap; });
    return limit ? out.slice(0, limit) : out;
  };

  /* Odwrotny przypadek, rzadszy i wart osobnej wzmianki: temat, w którym
     produkcja idzie lepiej niż rozpoznanie. Prawie zawsze znaczy to, że
     uczący się nauczył się wzorca na pamięć i nie słyszy go w mowie. */
  GStats.producedNotUnderstood = function (limit) {
    var out = GStats.table().filter(function (t) {
      return t.rated && t.productive.share >= GOOD
        && t.receptive.share < GOOD && -t.gap >= GAP;
    });
    out.sort(function (a, b) { return a.gap - b.gap; });
    return limit ? out.slice(0, limit) : out;
  };

  /* Podsumowanie po etapach — czy progresja gdzieś się zacięła. */
  GStats.byStage = function () {
    var acc = {};
    GStats.table().forEach(function (t) {
      var s = acc[t.stage] || (acc[t.stage] = {
        stage: t.stage, title: t.stageTitle, topics: 0, rated: 0,
        rAnswers: 0, rCorrect: 0, pAnswers: 0, pCorrect: 0
      });
      s.topics += 1;
      if (t.rated) s.rated += 1;
      s.rAnswers += t.receptive.answers;
      s.rCorrect += t.receptive.correct;
      s.pAnswers += t.productive.answers;
      s.pCorrect += t.productive.correct;
    });
    return Object.keys(acc).sort(function (a, b) { return a - b; })
      .map(function (k) {
        var s = acc[k];
        s.receptiveShare = s.rAnswers ? s.rCorrect / s.rAnswers : 0;
        s.productiveShare = s.pAnswers ? s.pCorrect / s.pAnswers : 0;
        s.touched = s.rAnswers + s.pAnswers > 0;
        return s;
      });
  };

  GStats.summary = function () {
    var t = GStats.table();
    var rated = t.filter(function (x) { return x.rated; });
    var gapList = GStats.understoodNotProduced();
    return {
      topics: t.length,
      rated: rated.length,
      gapCount: gapList.length,
      worst: gapList[0] || null,
      minAnswers: MIN_ANSWERS
    };
  };

  GStats.thresholds = { minAnswers: MIN_ANSWERS, good: GOOD, gap: GAP };

  global.GStats = GStats;
}(this));
