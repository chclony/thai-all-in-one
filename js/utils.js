/* Thai All-in-One — narzędzia wspólne */
(function (global) {
  'use strict';

  var U = {};

  U.$ = function (sel, root) { return (root || document).querySelector(sel); };
  U.$$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  U.el = function (tag, attrs, children) {
    var node = document.createElement(tag);
    attrs = attrs || {};
    Object.keys(attrs).forEach(function (k) {
      if (k === 'class') node.className = attrs[k];
      else if (k === 'text') node.textContent = attrs[k];
      else if (k === 'html') node.innerHTML = attrs[k];
      else if (k.slice(0, 2) === 'on') node.addEventListener(k.slice(2), attrs[k]);
      else if (attrs[k] !== null && attrs[k] !== undefined) node.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) {
      if (typeof c === 'string') node.appendChild(document.createTextNode(c));
      else if (c) node.appendChild(c);
    });
    return node;
  };

  U.clear = function (node) { while (node.firstChild) node.removeChild(node.firstChild); return node; };

  /* --------------------------------------------------------------- pamięć */
  var PREFIX = 'thaiaio.';
  U.store = {
    get: function (key, fallback) {
      try {
        var raw = localStorage.getItem(PREFIX + key);
        return raw === null ? fallback : JSON.parse(raw);
      } catch (e) { return fallback; }
    },
    set: function (key, value) {
      try { localStorage.setItem(PREFIX + key, JSON.stringify(value)); return true; }
      catch (e) { U.toast('Brak miejsca w pamięci przeglądarki. Wyczyść dane w ustawieniach.'); return false; }
    },
    remove: function (key) { try { localStorage.removeItem(PREFIX + key); } catch (e) {} },
    keys: function () {
      var out = [];
      try {
        for (var i = 0; i < localStorage.length; i++) {
          var k = localStorage.key(i);
          if (k.indexOf(PREFIX) === 0) out.push(k.slice(PREFIX.length));
        }
      } catch (e) {}
      return out;
    }
  };

  /* ---------------------------------------------------------------- tony */
  var TONE_MARKS = { '\u0301': 'wysoki', '\u0300': 'niski', '\u0302': 'opadający', '\u030c': 'rosnący', '\u0304': 'średni' };

  U.stripTones = function (text) {
    return (text || '').normalize('NFD').replace(/[\u0300\u0301\u0302\u030c\u0304]/g, '').normalize('NFC');
  };

  U.toneOf = function (syllable) {
    var d = (syllable || '').normalize('NFD');
    for (var i = 0; i < d.length; i++) {
      if (TONE_MARKS[d[i]]) return TONE_MARKS[d[i]];
    }
    return 'średni';
  };

  U.syllables = function (phonetic) {
    return (phonetic || '').split(/[\s\-]+/).filter(Boolean);
  };

  /* Kontury muszą być rozróżnialne na pierwszy rzut oka, także między tonami
     płaskimi — dlatego różnią się wyraźną wysokością w polu 26x14. */
  var CONTOUR = {
    'średni': 'M2 7 H24',
    'niski': 'M2 12 H24',
    'wysoki': 'M2 2 H24',
    'opadający': 'M2 2 C10 2 15 10 24 13',
    'rosnący': 'M2 13 C11 13 16 4 24 2'
  };

  /* Sygnatura interfejsu: nad każdą sylabą rysujemy kształt jej tonu. */
  U.toneMark = function (tone) {
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 26 14');
    svg.setAttribute('class', 'tone-mark');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', CONTOUR[tone] || CONTOUR['średni']);
    svg.appendChild(path);
    return svg;
  };

  /* Renderuje fonetykę z konturami tonów. Nigdy nie renderuje pisma tajskiego. */
  U.renderPhonetic = function (phonetic, options) {
    options = options || {};
    var wrap = U.el('div', { class: 'phonetic' + (options.hideTones ? ' no-tones' : ''), lang: 'th-Latn' });
    U.syllables(phonetic).forEach(function (syl) {
      var tone = U.toneOf(syl);
      var box = U.el('span', { class: 'syl', title: 'ton ' + tone });
      box.appendChild(U.toneMark(tone));
      box.appendChild(U.el('span', { text: options.hideTones ? U.stripTones(syl) : syl }));
      wrap.appendChild(box);
    });
    return wrap;
  };

  /* ------------------------------------------------------------ narzędzia */
  U.shuffle = function (list) {
    var arr = list.slice();
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  };

  U.sample = function (list, n) { return U.shuffle(list).slice(0, n); };

  U.debounce = function (fn, wait) {
    var timer = null;
    return function () {
      var args = arguments, self = this;
      clearTimeout(timer);
      timer = setTimeout(function () { fn.apply(self, args); }, wait);
    };
  };

  U.today = function () {
    var d = new Date();
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  };

  U.daysBetween = function (a, b) {
    return Math.round((new Date(b) - new Date(a)) / 86400000);
  };

  /* Data przesunięta o n dni, w tym samym formacie co U.today(). Używa jej
     prognoza tempa kursu. */
  U.addDays = function (date, n) {
    var d = new Date(date);
    d.setDate(d.getDate() + (n || 0));
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0')
      + '-' + String(d.getDate()).padStart(2, '0');
  };

  /* Data po polsku, do zdań w rodzaju „koniec poziomu około 3 października”. */
  var MONTHS_GEN = ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca',
                    'lipca', 'sierpnia', 'września', 'października',
                    'listopada', 'grudnia'];
  U.dateWords = function (date) {
    var d = new Date(date);
    if (isNaN(d.getTime())) return String(date);
    return d.getDate() + ' ' + MONTHS_GEN[d.getMonth()] + ' ' + d.getFullYear();
  };

  U.fold = function (text) {
    return U.stripTones(text || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/ł/g, 'l');
  };

  U.plural = function (n, one, few, many) {
    var n10 = n % 10, n100 = n % 100;
    if (n === 1) return one;
    if (n10 >= 2 && n10 <= 4 && (n100 < 12 || n100 > 14)) return few;
    return many;
  };

  var toastTimer = null;
  U.toast = function (message) {
    var node = document.getElementById('toast');
    if (!node) return;
    node.textContent = message;
    node.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { node.hidden = true; }, 3600);
  };

  U.icon = function (name) {
    var paths = {
      today: 'M4 5h16v15H4z M4 9h16 M8 3v4 M16 3v4',
      dict: 'M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z M8 4v13',
      phrases: 'M4 5h16v10H9l-5 4z',
      listen: 'M12 3v18 M7 8v8 M17 8v8 M3 11v2 M21 11v2',
      speak: 'M12 4a3 3 0 0 1 3 3v5a3 3 0 0 1-6 0V7a3 3 0 0 1 3-3z M5 11a7 7 0 0 0 14 0 M12 18v3',
      dialogues: 'M3 5h12v8H8l-5 4z M9 15h12v-6',
      srs: 'M4 12a8 8 0 1 1 3 6 M4 12v5 M4 17h5',
      pron: 'M4 15c4-10 12-10 16 0',
      progress: 'M4 20V9 M10 20V4 M16 20v-8 M22 20H2',
      settings: 'M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6z M12 2v3 M12 19v3 M2 12h3 M19 12h3 M5 5l2 2 M17 17l2 2 M19 5l-2 2 M7 17l-2 2',
      more: 'M5 12h.01 M12 12h.01 M19 12h.01',
      course: 'M4 5h7a2 2 0 0 1 2 2v13 M20 5h-7a2 2 0 0 0-2 2 M4 5v13h7 M20 5v13h-7',
      placement: 'M12 3l8 4-8 4-8-4z M4 11l8 4 8-4 M4 15l8 4 8-4',
      produce: 'M4 6h10 M4 12h7 M4 18h12 M17 4l3 3-6 6-3 .6.6-3z',
      lock: 'M6 11h12v9H6z M9 11V8a3 3 0 0 1 6 0v3',
      check: 'M5 13l4 4 10-10',
      play: 'M8 5l11 7-11 7z',
      star: 'M12 3l2.6 6 6.4.6-4.8 4.3 1.4 6.3L12 17l-5.6 3.2 1.4-6.3L3 9.6 9.4 9z',
      numbers: 'M6 4v16 M4 9h4 M4 15h4 M13 20l6-16 M12 9h9 M11 15h9',
      rescue: 'M4 6h11a4 4 0 0 1 0 8H8l-4 4z M17 17h3v3'
    };
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    (paths[name] || paths.more).split(' M').forEach(function (d, i) {
      var p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      p.setAttribute('d', (i ? 'M' : '') + d);
      p.setAttribute('fill', 'none');
      p.setAttribute('stroke', 'currentColor');
      p.setAttribute('stroke-width', '1.9');
      p.setAttribute('stroke-linecap', 'round');
      p.setAttribute('stroke-linejoin', 'round');
      svg.appendChild(p);
    });
    return svg;
  };

  /* ============================ JEDEN REJESTR NAZW ĆWICZEŃ (sesja VI)

     Do sesji V każdy moduł trzymał własną listę etykiet. Osiem trybów miało
     przez to po dwie lub trzy nazwy — „Wpisz z pamięci” na ekranie, „Napisz
     po tajsku” w sesji naprawczej i „wpisywanie fonetyki z pamięci” w planie
     naprawczym. Gorzej: nazwa „Ułóż zdanie” oznaczała DWA różne ćwiczenia —
     układanie ze słuchu (listen/assemble) i układanie z polskiego
     (produce/build). Uczący się, który czytał w statystyce, że najsłabszym
     trybem jest „Ułóż zdanie”, nie miał jak ustalić, na który ekran iść.

     Teraz nazwa jest jedna i mieszka w jednym miejscu. Każdy moduł, który
     wyświetla nazwę trybu, bierze ją stąd. Rozjazd nie jest już kwestią
     dyscypliny przy dopisywaniu — jest niemożliwy, bo nie ma drugiej listy.
     Pilnuje tego osobna asercja w function-test.py.

     `label`  — nazwa widoczna wszędzie: na przycisku wyboru trybu, w rozkładzie
                błędów, w drabinie tempa i w planie naprawczym.
     `short`  — wariant do zdania w środku tekstu („ćwicz ...”), małą literą.
     `screen` — ekran, na którym ten tryb faktycznie mieszka.
     `side`   — strona kartoteki: 'r' rozpoznawanie, 'p' wytwarzanie. */
  var EX = {
    /* --- słuchanie (rozpoznawanie) --- */
    choice:     { label: 'Wybierz tłumaczenie',        short: 'wybieranie tłumaczenia',    screen: 'listen', side: 'r' },
    dictation:  { label: 'Dyktando fonetyczne',        short: 'dyktando fonetyczne',       screen: 'listen', side: 'r' },
    assemble:   { label: 'Ułóż zdanie ze słuchu',      short: 'układanie zdań ze słuchu',  screen: 'listen', side: 'r' },
    spot:       { label: 'Znajdź słowo',               short: 'wyławianie słowa',          screen: 'listen', side: 'r' },
    gender:     { label: 'Forma męska czy żeńska?',    short: 'rozróżnianie form',         screen: 'listen', side: 'r' },
    noise:      { label: 'Rozumienie w hałasie',       short: 'rozumienie w hałasie',      screen: 'listen', side: 'r' },
    gap:        { label: 'Luki na słuch',              short: 'uzupełnianie luk',          screen: 'listen', side: 'r' },
    unknown:    { label: 'Nieznane słowo z kontekstu', short: 'zgadywanie z kontekstu',    screen: 'listen', side: 'r' },
    /* --- mówienie i pisanie (wytwarzanie) --- */
    build:      { label: 'Ułóż zdanie z polskiego',    short: 'układanie zdań z rozsypanki', screen: 'produce', side: 'p' },
    type:       { label: 'Wpisz z pamięci',            short: 'wpisywanie fonetyki z pamięci', screen: 'produce', side: 'p' },
    classifier: { label: 'Klasyfikatory',              short: 'ćwiczenie klasyfikatorów',  screen: 'produce', side: 'p' },
    tone:       { label: 'Tony — pary minimalne',      short: 'pary minimalne',            screen: 'produce', side: 'r' },
    say:        { label: 'Powiedz na głos',            short: 'mówienie na głos',          screen: 'produce', side: 'p' },
    roleplay:   { label: 'Odegraj dialog',             short: 'odgrywanie dialogu',        screen: 'produce', side: 'p' },
    /* --- gramatyka --- */
    map:        { label: 'Progresja',                  short: 'progresja konstrukcji',     screen: 'grammar', side: 'r' },
    structure:  { label: 'Struktura ze słuchu',        short: 'wykrywanie struktury',      screen: 'grammar', side: 'r' },
    transform:  { label: 'Przekształcenia',            short: 'przekształcanie zdań',      screen: 'grammar', side: 'p' },
    particles:  { label: 'Partykuły — ćwiczenie',      short: 'ćwiczenie partykuł',        screen: 'grammar', side: 'p' },
    guide:      { label: 'Partykuły — przegląd',       short: 'przegląd partykuł',         screen: 'grammar', side: 'r' },
    /* --- tryby spoza rejestrów ekranowych, ale widoczne w statystyce --- */
    scene:      { label: 'Sceny — sens całości',       short: 'sceny',                     screen: 'scenes',    side: 'r' },
    extensive:  { label: 'Słuchanie ekstensywne',      short: 'słuchanie ekstensywne',     screen: 'extensive', side: 'r' },
    numbers:    { label: 'Liczby ze słuchu',           short: 'liczby ze słuchu',          screen: 'numbers',   side: 'r' },
    speak:      { label: 'Powtarzaj za wzorem',        short: 'powtarzanie za wzorem',     screen: 'speak',     side: 'p' },
    placement:  { label: 'Test poziomujący',           short: 'test poziomujący',          screen: 'placement', side: 'r' },
    lesson:     { label: 'Sprawdzian lekcji',          short: 'sprawdzian lekcji',         screen: 'course',    side: 'r' }
  };

  U.EX = EX;
  /* Nazwa trybu. Nieznany identyfikator zwracamy w surowej postaci zamiast
     podmieniać na „inne” — bo pusta etykieta w statystyce jest błędem, który
     ma być widoczny, a nie zamaskowany. */
  U.exLabel = function (id) { return (EX[id] && EX[id].label) || id; };
  U.exShort = function (id) { return (EX[id] && EX[id].short) || U.exLabel(id); };
  U.exScreen = function (id) { return (EX[id] && EX[id].screen) || null; };
  U.exSide = function (id) { return (EX[id] && EX[id].side) || 'r'; };

  global.U = U;
})(window);
