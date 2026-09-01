/* Thai All-in-One — statystyka i eksport.

   Trzy rzeczy, których wcześniej nie było:

   1. Rozkład błędów. Sama skuteczność („78%”) nie mówi, co poprawić.
      Liczymy odpowiedzi i pomyłki osobno w rozbiciu na kategorie, tematy
      gramatyczne, typy rekordu i tryby ćwiczeń, wskazujemy najsłabszy obszar
      i proponujemy konkretne ćwiczenie, które go dotyczy.

   2. Eksport słownictwa do CSV zgodnego z Anki — bez pisma tajskiego,
      z fonetyką i tłumaczeniem.

   3. Krzywa zapamiętywania z danych SRS: po ilu dniach przerwy hasła nadal
      się pamięta. To krzywa tego użytkownika, nie krzywa z podręcznika. */
(function (global) {
  'use strict';

  var Stats = {};

  /* ==================================================== rozkład błędów */

  var BUCKET_LABELS = {
    category: 'Kategoria',
    grammar: 'Temat gramatyczny',
    type: 'Typ materiału',
    mode: 'Tryb ćwiczenia'
  };

  /* Nazwy trybów: jedno źródło, js/utils.js. Wcześniej stała tu druga lista,
     na której „Ułóż zdanie (produkcja)” i „Wybór tłumaczenia” rozjechały się
     z tym, co uczący się widział na ekranie. */
  function modeName(id) { return U.exLabel(id); }

  var TYPE_NAMES = {
    word: 'słowa', phrase: 'zwroty', sentence: 'zdania', question: 'pytania',
    collocation: 'połączenia wyrazowe', verb: 'czasowniki', noun: 'rzeczowniki',
    adjective: 'przymiotniki', adverb: 'przysłówki'
  };

  Stats.bucketLabel = function (bucket) { return BUCKET_LABELS[bucket] || bucket; };

  /* Czytelna nazwa klucza — id tematu gramatycznego zamieniamy na tytuł. */
  Stats.keyLabel = function (bucket, key) {
    if (bucket === 'grammar') {
      var g = (DB.grammar || []).filter(function (x) { return x.id === key; })[0];
      return g ? g.title : key;
    }
    if (bucket === 'mode') return modeName(key);
    if (bucket === 'type') return TYPE_NAMES[key] || key;
    return key;
  };

  Stats.areas = function (bucket, minAnswers) {
    return Progress.weakAreas(bucket, minAnswers).map(function (a) {
      a.label = Stats.keyLabel(bucket, a.key);
      return a;
    });
  };

  Stats.worst = function () {
    var w = Progress.worstArea();
    if (!w) return null;
    w.label = Stats.keyLabel(w.kind, w.item.key);
    w.bucketLabel = Stats.bucketLabel(w.kind);
    return w;
  };

  /* ============================================= eksport CSV do Anki */

  /* Anki importuje zwykły CSV. Kolumny w kolejności: przód, tył, wymowa
     po polsku, tony, poziom, kategoria, tagi. Pole ttsThai (pismo tajskie)
     nie istnieje w obiektach, którymi dysponuje aplikacja — nie ma fizycznej
     możliwości, żeby trafiło do eksportu. */
  var CSV_HEADER = ['Polski', 'Fonetyka', 'CzytajPoPolsku', 'Tony', 'Poziom', 'Kategoria', 'Tagi'];

  function csvCell(value) {
    var text = String(value === null || value === undefined ? '' : value);
    /* Cudzysłów podwajamy, całość w cudzysłowie — tak wymaga RFC 4180
       i tak samo czyta to Anki. */
    if (/[",\n\r]/.test(text)) return '"' + text.replace(/"/g, '""') + '"';
    return text;
  }

  function csvRow(cells) { return cells.map(csvCell).join(','); }

  /* scope: 'srs' | 'favourites' | 'seen' | 'level' | 'all' */
  Stats.collectForExport = function (scope, level) {
    var ids;
    if (scope === 'srs') ids = Object.keys(SRS.cards);
    else if (scope === 'favourites') ids = Object.keys(Progress.data.favourites);
    else if (scope === 'seen') ids = Object.keys(Progress.data.seen);
    else if (scope === 'level') {
      ids = DB.index.filter(function (r) { return r.level === level; })
        .map(function (r) { return r.id; });
    } else {
      ids = DB.index.map(function (r) { return r.id; });
    }
    /* Dialogi mają inną strukturę i nie są hasłami słownikowymi. */
    return ids.filter(function (id) { return !!DB.stub(id); });
  };

  Stats.buildCsv = function (ids) {
    var lines = [csvRow(CSV_HEADER)];
    ids.forEach(function (id) {
      var rec = DB.get(id) || DB.stub(id);
      if (!rec) return;
      var view = global.G ? G.view(rec) : rec;
      lines.push(csvRow([
        view.polish,
        view.thaiPhonetic,
        view.pronunciationPolish || '',
        view.toneGuide || '',
        view.level || '',
        view.category || '',
        (view.tags || []).join(' ')
      ]));
    });
    return lines.join('\r\n');
  };

  /* Pełne dane (wymowa po polsku, opis tonów) leżą w plikach poziomów.
     Przed eksportem dociągamy dokładnie te, które są potrzebne — a nie całą
     bazę, jeśli eksportujemy tylko ulubione. */
  Stats.exportCsv = function (scope, level) {
    var ids = Stats.collectForExport(scope, level);
    if (!ids.length) {
      U.toast('Nie ma czego wyeksportować dla tego wyboru.');
      return Promise.resolve(0);
    }
    return DB.ensureFor(ids).then(function () {
      var csv = Stats.buildCsv(ids);
      /* BOM — bez niego Excel na Windows czyta polskie znaki jako krzaki.
         Anki radzi sobie z BOM-em bez problemu. */
      var blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var a = U.el('a', { href: url, download: 'thai-all-in-one-anki-' + U.today() + '.csv' });
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
      return ids.length;
    });
  };

  /* ============================================ krzywa zapamiętywania */

  /* Wykres rysujemy w SVG, bez bibliotek. Oś X to odstęp między powtórkami,
     oś Y to odsetek trafnych odtworzeń. */
  Stats.retentionChart = function () {
    var data = SRS.retention();
    var withData = data.filter(function (b) { return b.total > 0; });

    var wrap = U.el('figure', { class: 'chart-block' });
    if (withData.length < 2) {
      wrap.appendChild(U.el('p', { class: 'muted', text:
        'Krzywa pojawi się po kilku dniach powtórek — potrzebuje danych z co najmniej '
        + 'dwóch różnych odstępów. Do tej pory zapisano ' + (SRS.log || []).length
        + ' ' + U.plural((SRS.log || []).length, 'powtórkę', 'powtórki', 'powtórek') + '.' }));
      return wrap;
    }

    var W = 320, H = 180, padL = 34, padB = 34, padT = 12, padR = 8;
    var plotW = W - padL - padR, plotH = H - padT - padB;
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.setAttribute('class', 'retention-chart');
    svg.setAttribute('role', 'img');

    function el(name, attrs) {
      var n = document.createElementNS('http://www.w3.org/2000/svg', name);
      Object.keys(attrs).forEach(function (k) { n.setAttribute(k, attrs[k]); });
      return n;
    }

    /* Siatka co 25%. */
    [0, 25, 50, 75, 100].forEach(function (pct) {
      var y = padT + plotH - (pct / 100) * plotH;
      svg.appendChild(el('line', {
        x1: padL, y1: y, x2: W - padR, y2: y, class: 'grid'
      }));
      var t = el('text', { x: padL - 6, y: y + 4, class: 'axis', 'text-anchor': 'end' });
      t.textContent = pct + '%';
      svg.appendChild(t);
    });

    var step = withData.length > 1 ? plotW / (withData.length - 1) : plotW;
    var points = withData.map(function (b, i) {
      return { x: padL + i * step, y: padT + plotH - (b.rate / 100) * plotH, b: b };
    });

    svg.appendChild(el('polyline', {
      points: points.map(function (p) { return p.x + ',' + p.y; }).join(' '),
      class: 'curve'
    }));

    points.forEach(function (p, i) {
      svg.appendChild(el('circle', { cx: p.x, cy: p.y, r: 4, class: 'dot' }));
      var lab = el('text', {
        x: p.x, y: H - padB + 14, class: 'axis',
        'text-anchor': i === 0 ? 'start' : (i === points.length - 1 ? 'end' : 'middle')
      });
      lab.textContent = p.b.label.replace(' dni', '').replace(' dzień', '');
      svg.appendChild(lab);
    });

    var axis = el('text', { x: padL + plotW / 2, y: H - 2, class: 'axis', 'text-anchor': 'middle' });
    axis.textContent = 'odstęp między powtórkami (dni)';
    svg.appendChild(axis);

    /* Opis tekstowy dla czytnika ekranu — wykres bez niego jest niedostępny. */
    var desc = withData.map(function (b) {
      return b.label + ': ' + b.rate + ' procent, ' + b.total + ' powtórek';
    }).join('; ');
    svg.setAttribute('aria-label', 'Krzywa zapamiętywania. ' + desc);

    wrap.appendChild(svg);

    var cap = U.el('figcaption', { class: 'muted' });
    var last = withData[withData.length - 1];
    cap.textContent = 'Po ' + last.label + ' przerwy pamiętasz ' + last.rate + '% haseł. '
      + 'Krzywa liczona z ' + (SRS.log || []).length + ' powtórek. '
      + 'Spadek poniżej 80% oznacza, że odstępy rosną za szybko — częstsze sesje wyrównają go same.';
    wrap.appendChild(cap);

    /* Tabela z tymi samymi liczbami: wykres jest ilustracją, dane muszą być
       dostępne także dla kogoś, kto go nie widzi. */
    var table = U.el('table', { class: 'data-table' });
    var thead = U.el('thead');
    var hr = U.el('tr');
    ['Odstęp', 'Powtórek', 'Trafnych'].forEach(function (h) {
      hr.appendChild(U.el('th', { scope: 'col', text: h }));
    });
    thead.appendChild(hr);
    table.appendChild(thead);
    var tbody = U.el('tbody');
    withData.forEach(function (b) {
      var tr = U.el('tr');
      tr.appendChild(U.el('th', { scope: 'row', text: b.label }));
      tr.appendChild(U.el('td', { text: String(b.total) }));
      tr.appendChild(U.el('td', { text: b.rate + '%' }));
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    wrap.appendChild(table);

    return wrap;
  };

  global.Stats = Stats;
})(window);
