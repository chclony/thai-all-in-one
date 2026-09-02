/* Thai All-in-One — wyszukiwarka.
   Indeksujemy wyłącznie pola widoczne dla użytkownika: polski, warianty polskie,
   fonetykę (z tonami i bez), zapis pod polskiego czytelnika, tagi i kategorię.

   Wyszukiwarka pracuje na lekkim indeksie (DB.index), a nie na pełnych
   rekordach. Dzięki temu działa od pierwszej sekundy, zanim którykolwiek plik
   poziomu zostanie pobrany. Wynikiem są wpisy skrócone — ekran, który
   potrzebuje przykładów albo dźwięku, dociąga pełny rekord przez DB.ensureFor. */
(function (global) {
  'use strict';

  var Search = { index: [], source: [], built: false };

  /* Budowa indeksu to złożenie i znormalizowanie sześciu pól dla każdego
     z 10 755 haseł. Przy starcie kosztowałaby kilkaset milisekund pracy
     procesora, a jest potrzebna dopiero przy pierwszym wyszukiwaniu.
     Dlatego Search.build tylko zapamiętuje materiał, a właściwą pracę
     wykonuje Search.ensure() — wołane przez zapytanie albo przez ekran
     Słownika, gdy przeglądarka ma wolną chwilę. */
  Search.build = function (records) {
    Search.source = records || [];
    Search.index = [];
    Search.built = false;
    return Search.source;
  };

  Search.ensure = function () {
    if (Search.built) return Search.index;
    Search.built = true;
    Search.index = Search.source.map(function (r) {
      /* Formę żeńską też indeksujemy — inaczej hasło „chǎn” albo „khâ”
         nie dałoby się znaleźć, mimo że jest w bazie. */
      var fem = (r.genderVariant && r.genderVariant.female) || {};
      var haystack = [
        fem.thaiPhonetic || '',
        U.stripTones(fem.thaiPhonetic || ''),
        fem.pronunciationPolish || '',
        r.polish,
        (r.polishAlternatives || []).join(' '),
        r.thaiPhonetic,
        U.stripTones(r.thaiPhonetic),
        r.pronunciationPolish,
        (r.tags || []).join(' '),
        r.category,
        r.subcategory
      ].join(' | ');
      return {
        id: r.id,
        rec: r,
        pl: U.fold(r.polish),
        text: U.fold(haystack),
        plain: U.fold(U.stripTones(r.thaiPhonetic || '')).replace(/[\s-]/g, ''),
        plainF: U.fold(U.stripTones(fem.thaiPhonetic || '')).replace(/[\s-]/g, '')
      };
    });
    return Search.index;
  };

  /* Ile haseł czeka na zindeksowanie — ekran może pokazać pasek zamiast
     zamierać na czas budowy. */
  Search.pending = function () { return Search.built ? 0 : Search.source.length; };

  function score(entry, q, qplain) {
    if (entry.pl === q) return 100;
    if (entry.plain === qplain) return 96;
    if (entry.plainF && entry.plainF === qplain) return 94;
    if (entry.pl.indexOf(q) === 0) return 80;
    if (entry.plain.indexOf(qplain) === 0) return 76;
    if (entry.plainF && entry.plainF.indexOf(qplain) === 0) return 74;
    var at = entry.text.indexOf(q);
    if (at === 0) return 60;
    if (at > 0) return 40;
    if (qplain && entry.plain.indexOf(qplain) > 0) return 30;
    return -1;
  }

  /* filters: { query, level, category, type, favouritesOnly, favourites, sort } */
  Search.query = function (filters) {
    Search.ensure();
    filters = filters || {};
    var q = U.fold(filters.query || '').trim();
    var qplain = q.replace(/[\s-]/g, '');
    var fav = filters.favourites || {};
    var out = [];

    for (var i = 0; i < Search.index.length; i++) {
      var e = Search.index[i], r = e.rec;
      if (filters.level && r.level !== filters.level) continue;
      if (filters.category && r.category !== filters.category) continue;
      if (filters.type && r.type !== filters.type) continue;
      if (filters.favouritesOnly && !fav[r.id]) continue;
      var s = 0;
      if (q) {
        s = score(e, q, qplain);
        if (s < 0) continue;
      }
      out.push({ rec: r, score: s });
    }

    var sort = filters.sort || 'freq';
    out.sort(function (a, b) {
      if (q && b.score !== a.score) return b.score - a.score;
      switch (sort) {
        case 'az': return a.rec.polish.localeCompare(b.rec.polish, 'pl');
        case 'easy': return a.rec.difficulty - b.rec.difficulty || b.rec.frequency - a.rec.frequency;
        case 'hard': return b.rec.difficulty - a.rec.difficulty || b.rec.frequency - a.rec.frequency;
        default: return b.rec.frequency - a.rec.frequency || a.rec.polish.localeCompare(b.rec.polish, 'pl');
      }
    });

    return out.map(function (o) { return o.rec; });
  };

  /* Dobiera dystraktory podobne do wzorca — sensowniejsze niż losowe. */
  Search.similar = function (record, count) {
    Search.ensure();
    var pool = Search.index.filter(function (e) {
      return e.rec.id !== record.id && e.rec.category === record.category;
    });
    if (pool.length < count) {
      pool = pool.concat(Search.index.filter(function (e) {
        return e.rec.id !== record.id && e.rec.level === record.level && e.rec.category !== record.category;
      }));
    }
    if (pool.length < count) pool = Search.index.filter(function (e) { return e.rec.id !== record.id; });
    return U.sample(pool, count).map(function (e) { return e.rec; });
  };

  global.Search = Search;
})(window);
