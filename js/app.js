/* Thai All-in-One — rdzeń aplikacji. */
(function (global) {
  'use strict';

  /* ================================ UKŁAD EKRANÓW (przebudowa w sesji VI)

     Po trzynastu sesjach rozbudowy lista ekranów urosła do dwudziestu pięciu
     i była PŁASKA: menu boczne wyliczało wszystkie po kolei, a ekran „Więcej”
     powtarzał dwadzieścia z nich w tej samej, niczym nieuzasadnionej
     kolejności. Kolejność powstała historycznie — ekran dopisywano tam, gdzie
     akurat kończyła się lista. Skutek: „Liczby w mowie” sąsiadowały
     z „Ratowaniem rozmowy”, a „Wymowa hasła” stała siedem pozycji od „Wymowy
     i tonów”, choć dotyczą tej samej rzeczy.

     Dwadzieścia pięć pozycji bez podziału to nie jest lista, którą się czyta —
     to lista, którą się przegląda w poszukiwaniu znajomego słowa. Dlatego
     ekrany mają teraz grupy, a grupa odpowiada na pytanie „po co tu wchodzę”,
     nie „z jakiego modułu to pochodzi”:

       codziennie  — to, co się robi każdego dnia,
       ćwiczenia   — pojedyncze ćwiczenie, gdy chcę czegoś konkretnego,
       materiały   — rzeczy do czytania i słuchania, bez oceniania,
       sprawdziany — pomiar: wejściowy, okresowy i naprawa po nim,
       postęp      — liczby o mnie,
       ustawienia.

     `tab` wyznacza pasek dolny. Zakładek jest pięć plus „Więcej”, bo sześć
     pozycji to tyle, ile mieści się na wąskim telefonie bez ścinania nazw. */
  var GROUPS = [
    { id: 'daily',    label: 'Codziennie' },
    { id: 'practice', label: 'Ćwiczenia' },
    { id: 'material', label: 'Materiały' },
    { id: 'tests',    label: 'Sprawdziany' },
    { id: 'stats',    label: 'Postęp' },
    { id: 'app',      label: 'Aplikacja' }
  ];

  var SCREENS = [
    /* --- codziennie --- */
    { id: 'today', label: 'Dzisiaj', icon: 'today', tab: true, group: 'daily' },
    { id: 'session', label: 'Sesja dnia', icon: 'today', tab: true, short: 'Sesja', group: 'daily' },
    { id: 'course', label: 'Kurs', icon: 'course', tab: true, group: 'daily' },
    { id: 'srs', label: 'Powtórki', icon: 'srs', tab: true, group: 'daily' },
    /* --- ćwiczenia --- */
    { id: 'module0', label: 'Moduł 0 — trening słuchu', icon: 'listen', group: 'practice' },
    { id: 'listen', label: 'Słuchanie', icon: 'listen', group: 'practice' },
    { id: 'produce', label: 'Mówienie po tajsku', icon: 'produce', group: 'practice' },
    { id: 'speak', label: 'Powtarzaj za wzorem', icon: 'speak', group: 'practice' },
    { id: 'grammar', label: 'Gramatyka', icon: 'course', group: 'practice' },
    { id: 'numbers', label: 'Liczby w mowie', icon: 'numbers', group: 'practice' },
    { id: 'rescue', label: 'Ratowanie rozmowy', icon: 'rescue', group: 'practice' },
    /* --- materiały --- */
    { id: 'dict', label: 'Słownik i zwroty', icon: 'dict', tab: true, short: 'Słownik', group: 'material' },
    { id: 'dialogues', label: 'Dialogi', icon: 'dialogues', group: 'material' },
    { id: 'scenes', label: 'Sceny', icon: 'dialogues', group: 'material' },
    { id: 'extensive', label: 'Słuchanie ekstensywne', icon: 'listen', group: 'material' },
    { id: 'pron', label: 'Tony i wymowa — przewodnik', icon: 'pron', group: 'material' },
    /* --- sprawdziany --- */
    { id: 'placement', label: 'Test poziomujący', icon: 'placement', group: 'tests' },
    { id: 'exam', label: 'Egzamin poziomowy', icon: 'placement', group: 'tests' },
    { id: 'checkpoint', label: 'Próbki kontrolne', icon: 'srs', group: 'tests' },
    { id: 'repair', label: 'Sesja naprawcza', icon: 'srs', group: 'tests' },
    /* --- postęp --- */
    { id: 'progress', label: 'Postęp', icon: 'progress', group: 'stats' },
    { id: 'week', label: 'Tydzień', icon: 'progress', group: 'stats' },
    { id: 'roadmap', label: 'Droga do celu', icon: 'progress', group: 'stats' },
    /* --- aplikacja --- */
    { id: 'settings', label: 'Ustawienia', icon: 'settings', group: 'app' }
  ];

  var App = { screen: 'today', settings: {} };

  var DEFAULTS = {
    theme: 'auto',
    scale: 1,
    hideTones: false,
    rate: 1,
    goal: 20,
    practiceLevel: '',
    autoplay: true,
    /* --- odsłuch i realizm (sesja L) --- */
    tempo: 'natural',       // 'slow' | 'natural' | 'fast'
    colloquial: false,      // syntezator dostaje wariant zredukowany
    showColloquial: true,   // czy pokazywać zapis potoczny obok słownikowego
    noiseKind: 'restaurant',
    noiseLevel: 0,          // 0 = cisza
    room: '',
    phone: false,
    /* Limit czasu w ćwiczeniach liczbowych i w drylu odruchu. Wydłużenie albo
       wyłączenie jest wymogiem dostępności, nie ustępstwem: ćwiczenie
       z limitem krótszym niż czas potrzebny na samo wpisanie odpowiedzi
       przestaje mierzyć percepcję, a zaczyna mierzyć sprawność motoryczną. */
    timeLimit: 'normal'
  };

  function saveSettings() { U.store.set('settings', App.settings); }

  /* Ile materiału ma wariant potoczny — liczba pochodzi z danych, nie z opisu. */
  var COLLOQUIAL_NOTE = 'materiał 132 lekcji i 184 dialogów';

  function cacheLabel() {
    if (!global.DSP) return 'Web Audio niedostępne.';
    var st = DSP.cache.stats();
    return 'Pamięć dźwięku: ' + st.entries + ' '
      + U.plural(st.entries, 'pozycja', 'pozycje', 'pozycji')
      + ', ' + (st.bytes / 1048576).toFixed(1).replace('.', ',') + ' MB z '
      + Math.round(st.limit / 1048576) + ' MB. Trafień '
      + st.hits + ', chybień ' + st.misses + ', eksmisji ' + st.evictions + '.';
  }

  function applySettings() {
    var s = App.settings;
    document.body.setAttribute('data-theme', s.theme);
    document.documentElement.style.setProperty('--scale', s.scale);
    document.body.classList.toggle('hide-tones', !!s.hideTones);
    Player.rate = parseFloat(s.rate) || 1;
    Player.setTempo(s.tempo);
    Player.colloquial = !!s.colloquial;
    Player.noiseKind = s.noiseKind || 'restaurant';
    Player.noiseLevel = parseInt(s.noiseLevel, 10) || 0;
    Player.room = s.room || '';
    Player.phone = !!s.phone;
    Player.prewarm();
    Progress.data.goal = parseInt(s.goal, 10) || 20;
  }

  /* ------------------------------------------------------------ nawigacja */
  function buildNav() {
    var side = U.$('#sidenav-list');
    var tabs = U.$('#tabbar-list');
    U.clear(side); U.clear(tabs);

    /* Menu boczne idzie grupami. Nagłówek grupy jest zwykłym elementem listy
       z rolą `presentation` — nie przyciskiem, bo nie da się w niego wejść,
       i nie nagłówkiem sekcji, bo `nav` ma już swoją nazwę. Czytnik ekranu
       dostaje go jako etykietę zagnieżdżonej listy, więc „Ćwiczenia: siedem
       pozycji” zapowiada się tak samo dla oka i dla ucha. */
    GROUPS.forEach(function (g) {
      var inGroup = SCREENS.filter(function (s) { return s.group === g.id; });
      if (!inGroup.length) return;
      var head = U.el('li', { class: 'sidenav-group', role: 'presentation' });
      var hid = 'navgrp-' + g.id;
      head.appendChild(U.el('span', { id: hid, text: g.label }));
      side.appendChild(head);
      var sub = U.el('li', { role: 'presentation' });
      var ul = U.el('ul', { 'aria-labelledby': hid });
      inGroup.forEach(function (s) {
        var li = U.el('li');
        var btn = U.el('button', { type: 'button', 'data-screen': s.id });
        btn.appendChild(U.icon(s.icon));
        btn.appendChild(U.el('span', { text: s.label }));
        btn.addEventListener('click', function () { App.go(s.id); });
        li.appendChild(btn);
        ul.appendChild(li);
      });
      sub.appendChild(ul);
      side.appendChild(sub);
    });

    SCREENS.filter(function (s) { return s.tab; }).forEach(function (s) {
      var li = U.el('li');
      var btn = U.el('button', { type: 'button', 'data-tab': s.id, 'aria-label': s.label });
      btn.appendChild(U.icon(s.icon));
      /* Pasek dolny ma sześć pozycji i sześćdziesiąt pikseli na każdą.
         Gdzie pełna nazwa się nie mieści, bierzemy skróconą — ale nazwa
         dostępna (aria-label) zostaje pełna, bo czytnik ekranu nie ma
         problemu z szerokością. */
      btn.appendChild(U.el('span', { text: s.short || s.label }));
      btn.addEventListener('click', function () { App.go(s.id); });
      li.appendChild(btn);
      tabs.appendChild(li);
    });

    var more = U.el('li');
    var moreBtn = U.el('button', { type: 'button', 'aria-label': 'Więcej ekranów' });
    moreBtn.appendChild(U.icon('more'));
    moreBtn.appendChild(U.el('span', { text: 'Więcej' }));
    moreBtn.addEventListener('click', openMore);
    more.appendChild(moreBtn);
    tabs.appendChild(more);
  }

  /* Jednozdaniowy opis ekranu. Sama nazwa nie wystarcza komuś, kto otwiera
     aplikację pierwszy raz: „Sceny” i „Dialogi” brzmią wymiennie, a uczą
     czego innego. Opis stoi w arkuszu „Więcej”, bo to jedyne miejsce, gdzie
     ekran ogląda się PRZED wejściem, a nie po. */
  var BLURB = {
    module0: 'Sam słuch, bez znaczeń — zanim zaczniesz zapamiętywać słowa.',
    listen: 'Osiem ćwiczeń ze słuchu: od wyboru tłumaczenia po hałas w tle.',
    produce: 'Sześć ćwiczeń wytwarzania: układanie, wpisywanie, mówienie, dialog.',
    speak: 'Wzór jest na wierzchu — powtarzasz i sprawdzasz tony.',
    grammar: 'Progresja konstrukcji plus trzy ćwiczenia i przegląd partykuł.',
    numbers: 'Ceny, godziny i reszta — mierzone czasem reakcji, nie trafnością.',
    rescue: 'Formuły na moment, gdy przestajesz nadążać. Z drylem na odruch.',
    dict: 'Cała baza z wyszukiwarką i filtrami. Tu też są gotowe zwroty.',
    dialogues: '184 krótkie rozmowy z podziałem na role.',
    scenes: 'Jedna sytuacja od wejścia do wyjścia — pytania o sens całości.',
    extensive: 'Kilka minut ciągłego materiału w trzech przejściach.',
    pron: 'Do czytania: pięć tonów, pary minimalne, jak czytać zapis.',
    placement: 'Dwadzieścia kilka pytań — ustala, od której lekcji zacząć.',
    exam: 'Cztery sprawności osobno, każda z własnym progiem.',
    checkpoint: 'Co 20 lekcji krótki test z materiału sprzed 20 lekcji.',
    repair: 'Zestaw z haseł, na których faktycznie się pomyliłeś.',
    progress: 'Rozkład błędów, siła pamięci, najsłabsze obszary.',
    week: 'Siedem dni wstecz i jedna rekomendacja na przyszły tydzień.',
    roadmap: 'Ile zostało do progu rozumienia w każdej sytuacji.',
    settings: 'Motyw, wielkość tekstu, tempo, hałas, limity czasu, kopia postępu.'
  };

  function openMore() {
    var body = U.el('div');
    body.appendChild(U.el('h2', { id: 'sheet-title', text: 'Wszystkie ekrany' }));
    body.appendChild(U.el('p', { class: 'muted', text:
      'Pięć ekranów z paska na dole plus wszystko poniżej. Pasek trzyma to, '
      + 'co robi się codziennie — reszta jest tutaj, pogrupowana.' }));
    GROUPS.forEach(function (g) {
      var inGroup = SCREENS.filter(function (s) { return s.group === g.id && !s.tab; });
      if (!inGroup.length) return;
      body.appendChild(U.el('h3', { class: 'sheet-group', text: g.label }));
      var list = U.el('div', { class: 'list' });
      inGroup.forEach(function (s) {
        var row = U.el('button', { class: 'row', type: 'button' });
        row.appendChild(U.icon(s.icon));
        var main = U.el('span', { class: 'row-main' });
        main.appendChild(U.el('strong', { text: s.label }));
        if (BLURB[s.id]) main.appendChild(U.el('span', { class: 'muted small', text: BLURB[s.id] }));
        row.appendChild(main);
        row.addEventListener('click', function () { closeSheet(); App.go(s.id); });
        list.appendChild(row);
      });
      body.appendChild(list);
    });
    openSheet(body);
  }

  function markNav() {
    U.$$('[data-screen]').forEach(function (b) {
      b.setAttribute('aria-current', b.getAttribute('data-screen') === App.screen ? 'page' : 'false');
    });
    U.$$('[data-tab]').forEach(function (b) {
      b.setAttribute('aria-current', b.getAttribute('data-tab') === App.screen ? 'page' : 'false');
    });
  }

  /* Stare adresy mają dalej działać. Ktoś, kto zapisał sobie „#phrases”
     w zakładkach przeglądarki albo dostał ten adres od znajomego, ma trafić
     tam, gdzie ta treść jest TERAZ — czyli do Słownika otwartego na zestawie
     „Zwroty”. Odesłanie na „Dzisiaj” byłoby formalnie poprawne i całkowicie
     bezużyteczne. */
  var ALIAS = { phrases: { screen: 'dict', preset: 'phrase' } };

  App.go = function (id) {
    var alias = ALIAS[id];
    if (alias) {
      id = alias.screen;
      if (alias.preset && App.dictPreset) App.dictPreset(alias.preset);
    }
    if (!SCREENS.some(function (s) { return s.id === id; })) id = 'today';
    Player.stop();
    Quiz.stopRecording();
    if (global.Produce) Produce.stopRecording();
    /* Obserwator odpowiedzi należy do ekranu sesji. Zostawiony po wyjściu
       liczyłby kroki ćwiczeń robionych gdzie indziej. */
    if (App.screen === 'session' && id !== 'session') {
      Progress.onAnswer = null;
      Session.pause();
    }
    /* Wyjście z egzaminu w trakcie kończy podejście. To nie jest złośliwość:
       bez tego dałoby się otworzyć zestaw, wyjść po odpowiedzi do słownika
       i wrócić — a wtedy egzamin przestaje mierzyć cokolwiek. Próbka
       kontrolna zachowuje się odwrotnie i po prostu się porzuca, bo niczego
       nie certyfikuje. */
    if (App.screen === 'exam' && id !== 'exam' && global.ExamView) ExamView.leave();
    if (App.screen === 'checkpoint' && id !== 'checkpoint' && global.Checkpoint) Checkpoint.leave();
    App.screen = id;
    SCREENS.forEach(function (s) {
      var node = document.getElementById('screen-' + s.id);
      if (node) node.hidden = s.id !== id;
    });
    markNav();
    if (location.hash !== '#' + id) history.replaceState(null, '', '#' + id);
    U.$('#main').scrollTop = 0;
    window.scrollTo(0, 0);
    syncIndex();
    RENDER[id] && RENDER[id]();
    wrapWideTables();
    ensureFullData(id);
  };

  /* Tabele powstają w sześciu modułach (tydzień, postęp, egzamin, próbka,
     Moduł 0, ocena wymowy). Zamiast poprawiać każde z tych miejsc osobno —
     i pilnować, żeby następne też pamiętało — opakowanie zakłada się raz,
     po renderze ekranu. Kontener jest osiągalny klawiszem Tab i ma nazwę,
     bo obszar przewijany wyłącznie myszą byłby dla części osób martwy.
     Opakowujemy tylko tabele, które NIE mieszczą się w swoim miejscu —
     przy zwykłej wielkości tekstu nie zmienia się nic. */
  function wrapWideTables() {
    U.$$('#screen-' + App.screen + ' .data-table').forEach(function (tbl) {
      var host = tbl.parentNode;
      var wrapped = host && host.classList && host.classList.contains('table-scroll');
      var room = (wrapped ? host.parentNode : host);
      var fits = !room || tbl.scrollWidth <= room.clientWidth + 1;
      if (fits) {
        /* Zmieściła się — jeśli była opakowana przy węższym ekranie, zdejmujemy
           opakowanie, żeby nie zostawiać pustego przystanku dla klawisza Tab. */
        if (wrapped) { host.parentNode.insertBefore(tbl, host); host.parentNode.removeChild(host); }
        return;
      }
      if (wrapped) return;
      var box = U.el('div', { class: 'table-scroll', tabindex: '0', role: 'region' });
      var cap = tbl.querySelector('caption');
      box.setAttribute('aria-label', (cap ? cap.textContent.trim() : 'Tabela')
        + ' — tabela szersza niż ekran, przewijana w poziomie');
      host.insertBefore(box, tbl);
      box.appendChild(tbl);
    });
  }
  App.wrapWideTables = wrapWideTables;

  /* Część ekranów dosypuje treść PO zakończeniu renderu — tabela tygodnia
     powstaje dopiero, gdy domknie się odczyt postępu. Jednorazowe wywołanie
     po App.go() trafiało wtedy w pustkę. Obserwator domyka te przypadki bez
     zgadywania opóźnień; jest zdławiony ramką animacji, więc nie chodzi przy
     każdym pojedynczym węźle. */
  var wrapQueued = false;
  function watchLateTables() {
    var main = U.$('#main');
    if (!main || !global.MutationObserver) return;
    new MutationObserver(function () {
      if (wrapQueued) return;
      wrapQueued = true;
      requestAnimationFrame(function () {
        wrapQueued = false;
        try { wrapWideTables(); } catch (e) {}
      });
    }).observe(main, { childList: true, subtree: true });
  }

  /* Indeks wyszukiwarki musi odpowiadać temu, co faktycznie jest w pamięci.
     Sprawdzamy to przy każdym przejściu, bo dociąganie plików w tle kończy się
     w nieprzewidywalnym momencie — także w trakcie renderowania ekranu. */
  function syncIndex() {
    if (Search.source.length !== DB.index.length) {
      Search.build(DB.index);
      refreshStatus();
    }
  }
  App.syncIndex = syncIndex;

  /* Zestawienia dla testów i dla arkusza „Więcej”. Trzymamy je tutaj, bo
     SCREENS jest prywatne — a test, który sam powtarza listę ekranów,
     przestaje być testem i staje się drugą kopią tej listy. */
  App.screenIds = function () {
    return SCREENS.map(function (s) { return s.id; });
  };
  App.screenGroups = function () { return GROUPS.slice(); };
  App.screensWithoutGroup = function () {
    var known = {};
    GROUPS.forEach(function (g) { known[g.id] = true; });
    return SCREENS.filter(function (s) { return !known[s.group]; })
      .map(function (s) { return s.id; });
  };

  /* Czego potrzebuje dany ekran. Nie „całej bazy” — tylko tych plików, bez
     których nie da się go pokazać. Słownik, kurs, postęp i test poziomujący
     działają na samym indeksie i nie pobierają nic. */
  function dataNeedFor(id) {
    switch (id) {
      /* Ekrany przeszukujące CAŁĄ bazę potrzebują kompletnego indeksu —
         przy starcie wczytuje się samo czoło (Survival + A1). W praktyce
         reszta jest już wtedy w pamięci, bo dociąganie rusza tuż po
         pierwszym renderze; obietnica tylko domyka wyścig. */
      case 'dict':
      case 'placement':
        return DB.ensureIndex();
      case 'listen':
      case 'speak':
        return Quiz.ensureData();
      case 'grammar':
        return Gram.ensureData();
      case 'produce':
        return Produce.ensureData();
      case 'course':
      case 'module0':
        return null;   /* mapa kursu i Moduł 0 działają na danych startowych */
      case 'dialogues':
        return DB.ensureDialogues();
      case 'numbers':
        return Numbers.ensureData();
      case 'rescue':
        return Rescue.ensureData();
      case 'scenes':
      case 'extensive':
        return DB.ensureScenes();
      /* Egzamin potrzebuje zestawów i scen; hasła produkcyjne dociąga sam po
         wybraniu poziomu, bo dopiero wtedy wiadomo, o które chodzi. */
      case 'exam':
        return Exam.ensureData();
      case 'checkpoint':
        return Checkpoint.ensureData();
      case 'srs':
        return DB.ensureIndex().then(function () {
          return DB.ensureFor(Object.keys(SRS.cards));
        }).then(function () {
          return DB.ensureLevel(App.settings.practiceLevel || Progress.entryLevel());
        });
      case 'today':
        /* Do materiału startowego dokładamy próbki (53 kB) i zestawy
           egzaminacyjne (175 kB). Bez nich karta kamienia milowego nigdy by
           się nie pokazała — a informacja „czeka na ciebie próbka” jest warta
           więcej niż ćwierć megabajta, którego i tak nie widać przy starcie,
           bo ekran renderuje się wcześniej i tylko dorysowuje kartę. */
        return Promise.all([
          DB.ensureStarter(),
          DB.ensureCheckpoints(),
          DB.ensureFile('exams.json')
        ]);
      /* Mapa drogi i podsumowanie tygodnia liczą z korpusu pokrycia. Sam
         korpus wystarcza — treści kwestii nie są potrzebne, dopóki uczący się
         nie zechce ich usłyszeć. */
      case 'roadmap':
      case 'week':
        return DB.ensureCoverage();
      /* Sesja dnia dobiera skład, zanim wie, jaki blok wypadnie pierwszy.
         Potrzebuje więc i haseł z kolejki powtórek, i materiału ćwiczeń,
         i pokrycia (najsłabsza kategoria steruje blokiem słuchania). */
      case 'session':
        return Promise.all([
          DB.ensureCoverage(),
          DB.ensureFor(Object.keys(SRS.cards)),
          DB.ensureLevel(App.settings.practiceLevel || Progress.entryLevel())
        ]);
      default:
        return null;
    }
  }

  /* Wspólna obsługa dociągania: pokazujemy pasek, czekamy, przerysowujemy
     ekran — ale tylko wtedy, gdy użytkownik nadal na nim jest. */
  function ensureFullData(id) {
    /* Sesja naprawcza sama dociąga swoje hasła — lista jest znana dopiero
       po zbudowaniu zestawu, więc nie da się jej obsłużyć mapą ekranów. */
    if (id === 'repair') return;
    var need = dataNeedFor(id);
    if (!need) return;
    var note = U.$('#loading-more');
    var slow = setTimeout(function () { if (note) note.hidden = false; }, 220);
    need.then(function () {
      clearTimeout(slow);
      if (note) note.hidden = true;
      syncIndex();
      refreshStatus();
      if (App.screen === id) RENDER[id] && RENDER[id]();
    });
  }
  App.ensureFullData = ensureFullData;

  function refreshStatus() {
    var node = U.$('#db-status');
    if (!node || !DB.manifest) return;
    var text = DB.count() + ' haseł · ' + DB.dialogueCount() + ' dialogów · '
      + DB.lessons.length + ' lekcji · wersja danych ' + DB.manifest.version;
    if (DB.errors.length) {
      text += ' · nie wczytano ' + DB.errors.length + ' pliku(ów)';
      node.setAttribute('data-warn', 'true');
    } else {
      node.removeAttribute('data-warn');
    }
    node.textContent = text;
  }
  App.refreshStatus = refreshStatus;

  /* --------------------------------------------------------------- arkusz */
  var lastFocus = null;

  function openSheet(content) {
    var sheet = U.$('#sheet');
    lastFocus = document.activeElement;
    U.clear(U.$('#sheet-body')).appendChild(content);
    sheet.hidden = false;
    U.$('#sheet-close').focus();
  }

  function closeSheet() {
    var sheet = U.$('#sheet');
    sheet.hidden = true;
    Player.stop();
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  App.closeSheet = closeSheet;
  App.openSheet = openSheet;

  /* --------------------------------------------------- wiersz i szczegóły */
  function recordRow(source) {
    var rec = G.view(source);
    var row = U.el('button', { class: 'row', type: 'button' });
    var main = U.el('div', { class: 'row-main' }, [
      U.el('div', { class: 'row-pl', text: rec.polish }),
      U.el('div', { class: 'row-ph', text: App.settings.hideTones ? U.stripTones(rec.thaiPhonetic) : rec.thaiPhonetic }),
      U.el('div', { class: 'row-meta', text: rec.level + ' · ' + rec.category })
    ]);
    row.appendChild(main);
    var play = U.el('span', { class: 'icon-btn', 'aria-hidden': 'true' });
    play.appendChild(U.icon('play'));
    row.appendChild(play);
    if (G.hasVariant(source)) row.classList.add('has-gender');
    row.addEventListener('click', function () { App.openRecord(source.id); });
    return row;
  }

  /* Zapis potoczny obok słownikowego.

     Uczący się musi widzieć oba naraz i wiedzieć, że to ten sam zwrot:
     inaczej pierwsze zetknięcie z „wàt-dii kháp” zamiast „sawàt-dii khráp”
     wygląda jak nowe słowo, a nie jak to samo powiedziane normalnie.
     Pod spodem wymieniamy reguły, które ten kształt wytłumaczyły. */
  function colloquialRow(item) {
    if (App.settings.showColloquial === false) return null;
    var coll = item && item.colloquial;
    if (!coll || !coll.thaiPhonetic) return null;
    var wrap = U.el('div', { class: 'coll-row' });
    wrap.appendChild(U.el('div', { class: 'coll-label', text: 'W mowie potocznej' }));
    wrap.appendChild(U.renderPhonetic(coll.thaiPhonetic, { hideTones: App.settings.hideTones }));
    if (coll.pronunciationPolish) {
      wrap.appendChild(U.el('div', { class: 'row-meta muted', text: 'Czytaj: ' + coll.pronunciationPolish }));
    }
    if (coll.rules && coll.rules.length && global.RULE_NAMES) {
      var names = coll.rules.map(function (r) { return RULE_NAMES[r] || r; }).join(', ');
      wrap.appendChild(U.el('div', { class: 'row-meta muted', text: 'Zmiany: ' + names }));
    }
    var b = U.el('button', { class: 'icon-btn', type: 'button',
      'aria-label': 'Posłuchaj formy potocznej' });
    b.appendChild(U.icon('play'));
    b.addEventListener('click', function () {
      var saved = Player.colloquial;
      Player.colloquial = true;
      Player.play(item, { btn: b, tempo: 'fast', onend: function () { Player.colloquial = saved; } });
      setTimeout(function () { Player.colloquial = saved; }, 40);
    });
    wrap.appendChild(b);
    return wrap;
  }
  App.colloquialRow = colloquialRow;

  /* Nazwy reguł redukcji — te same identyfikatory, co w generatorze
     tools/generators/colloquial.py. */
  global.RULE_NAMES = {
    'lex': 'forma utrwalona',
    'cluster-r': 'zbitka bez /r/',
    'cluster-l': 'zbitka bez /l/',
    'r-l': '/r/ jak /l/',
    'coda-drop': 'zgubiony wygłos',
    'vowel-short': 'skrócona samogłoska',
    'tone-lax': 'spłaszczony ton'
  };

  /* Obie formy naraz. Uczący się używa jednej, ale ze słuchu musi rozpoznawać
     obie — rozmówca odezwie się w swojej. */
  function genderFormRow(label, item, hint) {
    var wrap = U.el('div', { class: 'gform' });
    wrap.appendChild(U.el('div', { class: 'gform-label', text: label }));
    var main = U.el('div', { class: 'gform-main' });
    main.appendChild(U.renderPhonetic(item.thaiPhonetic, { hideTones: App.settings.hideTones }));
    main.appendChild(U.el('div', { class: 'row-meta muted', text: 'Czytaj: ' + item.pronunciationPolish }));
    if (hint) main.appendChild(U.el('div', { class: 'row-meta muted', text: hint }));
    wrap.appendChild(main);
    var b = U.el('button', { class: 'icon-btn', type: 'button', 'aria-label': 'Posłuchaj — ' + label });
    b.appendChild(U.icon('play'));
    b.addEventListener('click', function () { Player.play(item, { btn: b }); });
    wrap.appendChild(b);
    return wrap;
  }

  /* Hasło o samej formie („ja (mężczyzna)”) nie przełącza się razem z resztą.
     Oznaczamy je w układzie strony, żeby było widać, że to celowe. */
  function markLexicon(node, item) {
    if (item && item.genderLexicon) node.classList.add('gender-lexicon');
    return node;
  }

  function genderBlock(source) {
    if (source.genderLexicon) {
      var note = U.el('div', { class: 'card gender-card' });
      note.appendChild(U.el('h3', { text: 'Forma zależna od płci mówiącego' }));
      note.appendChild(U.el('p', { class: 'muted', text:
        'To hasło opisuje jedną konkretną formę, więc nie zmienia się razem z ustawieniem. ' +
        'Odpowiednik dla drugiej płci znajdziesz jako osobne hasło w słowniku.' }));
      return note;
    }
    var pair = G.pair(source);
    if (!pair) return document.createDocumentFragment();
    var box = U.el('div', { class: 'card gender-card' });
    box.appendChild(U.el('h3', { text: 'Forma zależna od płci mówiącego' }));
    if (pair.fixed) {
      box.appendChild(U.el('p', { class: 'muted', text: pair.fixed === 'female'
        ? 'Tę kwestię wypowiada kobieta — scenariusz przesądza formę.'
        : 'Tę kwestię wypowiada mężczyzna — scenariusz przesądza formę.' }));
      box.appendChild(genderFormRow(pair.fixed === 'female' ? 'forma żeńska' : 'forma męska',
        pair.fixed === 'female' ? pair.female : pair.male));
      return box;
    }
    var mine = G.current();
    box.appendChild(genderFormRow('forma męska', pair.male,
      mine === 'male' ? 'Tej formy używasz Ty.' : 'Tak powie mężczyzna.'));
    box.appendChild(genderFormRow('forma żeńska', pair.female,
      mine === 'female' ? 'Tej formy używasz Ty.' : 'Tak powie kobieta.'));
    box.appendChild(U.el('p', { class: 'muted', text:
      'Rozpoznawaj obie ze słuchu, nawet jeśli mówisz tylko jedną — rozmówca odezwie się w swojej.' }));
    return box;
  }

  App.openRecord = function (id) {
    var source = DB.get(id);
    if (!source) return;
    var rec = G.view(source);
    var body = U.el('div');
    body.appendChild(U.el('h2', { id: 'sheet-title', text: rec.polish }));
    body.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: App.settings.hideTones }));
    body.appendChild(U.el('p', { class: 'muted', text: 'Czytaj po polsku: ' + rec.pronunciationPolish }));
    body.appendChild(U.el('p', { class: 'muted', text: rec.toneGuide }));

    var badges = U.el('p');
    badges.appendChild(U.el('span', { class: 'badge lvl', text: rec.level }));
    badges.appendChild(document.createTextNode(' '));
    badges.appendChild(U.el('span', { class: 'badge', text: rec.category }));
    badges.appendChild(document.createTextNode(' '));
    badges.appendChild(U.el('span', { class: 'badge', text: 'trudność ' + rec.difficulty + '/5' }));
    badges.appendChild(document.createTextNode(' '));
    badges.appendChild(U.el('span', { class: 'badge', text: rec.register }));
    body.appendChild(badges);

    var favBtn = U.el('button', {
      class: 'btn ghost', type: 'button',
      text: Progress.isFavourite(rec.id) ? 'Usuń z ulubionych' : 'Dodaj do ulubionych'
    });
    favBtn.addEventListener('click', function () {
      var on = Progress.toggleFavourite(rec.id);
      favBtn.textContent = on ? 'Usuń z ulubionych' : 'Dodaj do ulubionych';
      U.toast(on ? 'Dodano do ulubionych.' : 'Usunięto z ulubionych.');
    });
    var srsBtn = U.el('button', {
      class: 'btn ghost', type: 'button',
      text: SRS.hasAny(rec.id) ? 'Jest w powtórkach' : 'Dodaj do powtórek'
    });
    srsBtn.addEventListener('click', function () {
      SRS.addBoth(rec.id);
      srsBtn.textContent = 'Jest w powtórkach';
      U.toast('Dodano do powtórek.');
    });
    var speakBtn = U.el('button', { class: 'btn ghost', type: 'button', text: 'Ćwicz wymowę' });
    speakBtn.addEventListener('click', function () {
      closeSheet();
      App.go('speak');
      Quiz.renderSpeak(U.$('#speak-area'), rec);
    });
    body.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(rec, 'Posłuchaj'), favBtn, srsBtn, speakBtn]));

    var collRow = colloquialRow(rec);
    if (collRow) body.appendChild(collRow);

    body.appendChild(genderBlock(source));

    if (rec.literalMeaning) body.appendChild(U.el('p', {}, [U.el('strong', { text: 'Dosłownie: ' }), document.createTextNode(rec.literalMeaning)]));
    if (rec.notes) body.appendChild(U.el('p', {}, [U.el('strong', { text: 'Uwaga: ' }), document.createTextNode(rec.notes)]));
    if (rec.commonMistakes) body.appendChild(U.el('p', {}, [U.el('strong', { text: 'Częste błędy: ' }), document.createTextNode(rec.commonMistakes)]));

    if (rec.examples && rec.examples.length) {
      body.appendChild(U.el('h3', { text: 'Przykłady' }));
      rec.examples.forEach(function (source_ex) {
        var ex = G.view(source_ex);
        var card = U.el('div', { class: 'bigcard' });
        card.appendChild(U.el('div', { class: 'bc-pl', text: ex.polish }));
        card.appendChild(U.renderPhonetic(ex.thaiPhonetic, { hideTones: App.settings.hideTones }));
        var exColl = colloquialRow(ex);
        if (exColl) card.appendChild(exColl);
        card.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(ex, 'Posłuchaj')]));
        body.appendChild(card);
      });
    }

    var related = (rec.relatedWords || []).map(DB.get).filter(Boolean);
    if (related.length) {
      body.appendChild(U.el('h3', { text: 'Powiązane' }));
      var list = U.el('div', { class: 'list' });
      related.forEach(function (r) { list.appendChild(recordRow(r)); });
      body.appendChild(list);
    }

    Progress.answer(source.id, true);
    openSheet(body);
  };

  /* ========================================================== EKRAN: DZIŚ */
  function statBox(value, label) {
    return U.el('div', { class: 'stat' }, [U.el('b', { text: String(value) }), U.el('span', { text: label })]);
  }

  var RENDER = {};

  /* Pasek postępu z opisem dla czytnika ekranu. Sam pasek jest grafiką —
     bez tekstu obok nie niesie żadnej informacji poza kolorem. */
  function progressBar(share, label) {
    var pct = Math.max(0, Math.min(100, Math.round(share * 100)));
    var bar = U.el('div', {
      class: 'progress', role: 'progressbar',
      'aria-valuenow': String(pct), 'aria-valuemin': '0', 'aria-valuemax': '100',
      'aria-label': label || ('Ukończono ' + pct + '%')
    });
    bar.appendChild(U.el('i', { style: 'width:' + pct + '%' }));
    return bar;
  }
  App.progressBar = progressBar;

  RENDER.today = function () {
    var s = Progress.summary();
    var srs = SRS.stats();
    var goalState = Goals.today();

    var stats = U.clear(U.$('#today-stats'));
    stats.appendChild(statBox(s.streak, U.plural(s.streak, 'dzień z rzędu', 'dni z rzędu', 'dni z rzędu')));
    stats.appendChild(statBox(srs.due, 'do powtórki'));
    stats.appendChild(statBox(goalState.done + '/' + goalState.minutes, 'minut dziś'));
    stats.appendChild(statBox(s.accuracy + '%', 'skuteczność'));

    renderTodaySession();

    var goal = U.clear(U.$('#today-goal'));
    goal.appendChild(U.el('h2', { text: 'Cel dnia' }));
    goal.appendChild(U.el('p', { class: 'muted',
      text: goalState.met
        ? 'Zrobione: ' + goalState.done + ' z ' + goalState.minutes + ' minut.'
        : goalState.done + ' z ' + goalState.minutes + ' minut · zostało '
          + goalState.left + ' ' + U.plural(goalState.left, 'minuta', 'minuty', 'minut') }));
    goal.appendChild(progressBar(goalState.share, 'Cel dnia: ' + goalState.done
      + ' z ' + goalState.minutes + ' minut'));

    var week = Goals.category();
    if (week && !week.expired) {
      goal.appendChild(U.el('p', { class: 'muted',
        text: 'Cel tygodnia: domykam „' + week.name + '” — pokrycie '
          + Math.round(week.coverage * 100) + '% z ' + Math.round(week.goal * 100) + '%'
          + (week.wordsLeft ? ', brakuje ' + week.wordsLeft + ' '
             + U.plural(week.wordsLeft, 'hasła', 'haseł', 'haseł') : '') + '.' }));
    }

    renderTodayMilestone();
    renderTodayCoverage();

    var rec = U.clear(U.$('#today-recommend'));
    rec.appendChild(U.el('h2', { text: 'Albo pojedyncze ćwiczenie' }));
    rec.appendChild(U.el('p', { class: 'muted', text: 'Sesja dnia wystarcza. To jest dla tych dni, gdy chcesz czegoś konkretnego.' }));
    /* Skróty do pojedynczych ćwiczeń. Do sesji V były tu trzy, a „Liczby
       w mowie” i „Ratowanie rozmowy” nie miały w całej aplikacji ANI JEDNEGO
       odnośnika — prowadziło do nich wyłącznie menu boczne i adres. Ekran,
       do którego nic nie kieruje, w praktyce nie istnieje: trafia tam tylko
       ten, kto już wie, że go szuka. Oba uczą czegoś, czego nie uczy nic
       innego (szybkość przy liczbach, odruch przy wychodzeniu z zacięcia),
       więc dostają wejście stąd. */
    var row = U.el('div', { class: 'btn-row' });
    [
      [srs.due ? 'Powtórz ' + srs.due + ' ' + U.plural(srs.due, 'hasło', 'hasła', 'haseł')
        : 'Ucz się nowych słów', 'srs'],
      ['Ćwiczenie ze słuchu', 'listen'],
      ['Dialog dnia', 'dialogues'],
      ['Liczby w mowie', 'numbers'],
      ['Ratowanie rozmowy', 'rescue']
    ].forEach(function (b) {
      var btn = U.el('button', { class: 'btn ghost', type: 'button', text: b[0] });
      btn.addEventListener('click', function () { App.go(b[1]); });
      row.appendChild(btn);
    });
    rec.appendChild(row);

    var word = U.clear(U.$('#today-word'));
    word.appendChild(U.el('h2', { text: 'Zwrot dnia' }));
    if (DB.index.length) {
      var seed = parseInt(U.today().replace(/-/g, ''), 10);
      /* Zwrot dnia ma być czymś, co da się powiedzieć — nie zaimkiem.
         Wybieramy z indeksu, więc działa to zanim cokolwiek się dociągnie. */
      var pick = DB.index.filter(function (r) {
        return r.type !== 'word' && r.frequency === 5 && r.level === 'Survival' && r.difficulty <= 3;
      });
      if (pick.length < 20) pick = DB.index.filter(function (r) { return r.type !== 'word' && r.frequency >= 4; });
      var source = (pick.length ? pick : DB.index)[seed % (pick.length || DB.index.length)];
      source = DB.any(source.id);
      var item = G.view(source);
      word.appendChild(U.el('p', { class: 'bc-pl', text: item.polish }));
      word.appendChild(U.renderPhonetic(item.thaiPhonetic, { hideTones: App.settings.hideTones }));
      word.appendChild(U.el('p', { class: 'muted', text: 'Czytaj: ' + item.pronunciationPolish }));
      var open = U.el('button', { class: 'btn ghost', type: 'button', text: 'Szczegóły' });
      open.addEventListener('click', function () { App.openRecord(source.id); });
      word.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(item, 'Posłuchaj'), open]));
    }
  };


  /* Kamień milowy na ekranie „Dzisiaj”: należna próbka kontrolna albo poziom
     gotowy do egzaminu. Jedno i drugie jest bezużyteczne, jeśli uczący się nie
     wie, że go czeka — a nikt nie zagląda codziennie do ekranu, na którym
     przez trzydzieści lekcji nic się nie dzieje. Pokazujemy najwyżej jedną
     rzecz naraz i tylko wtedy, gdy naprawdę jest do zrobienia. */
  function renderTodayMilestone() {
    var box = U.$('#today-milestone');
    if (!box) return;
    U.clear(box);
    box.hidden = true;

    /* Próbka kontrolna ma pierwszeństwo: jest krótka, a im dłużej czeka,
       tym mniej mówi o tym, co uczący się pamiętał w chwili wyzwolenia. */
    if (global.Checkpoint && Checkpoint.ready()) {
      var due = Checkpoint.due();
      if (due.length) {
        box.hidden = false;
        box.appendChild(U.el('h2', { text: 'Próbka kontrolna czeka' }));
        box.appendChild(U.el('p', {
          text: due[0].title + ' — dwanaście zadań, około sześciu minut. Sprawdza materiał '
            + 'sprzed dwudziestu lekcji, zanim zrobią to powtórki.'
        }));
        var goc = U.el('button', { class: 'btn', type: 'button', text: 'Zrób próbkę' });
        goc.addEventListener('click', function () { App.go('checkpoint'); });
        box.appendChild(U.el('div', { class: 'btn-row' }, [goc]));
        return;
      }
    }

    if (!global.Exam || !Exam.ready()) return;
    /* Egzamin proponujemy dopiero po przerobieniu materiału poziomu —
       wcześniejsze podejście zużywa jeden z trzech zestawów i niewiele mówi. */
    var candidate = null;
    Exam.LEVELS.forEach(function (level) {
      if (candidate || Progress.examPassed(level)) return;
      var ready = Exam.readiness(level);
      if (!ready.total || ready.share < 90) return;
      if (!Exam.eligibility(level).allowed) return;
      candidate = { level: level, ready: ready };
    });
    if (!candidate) return;
    box.hidden = false;
    box.appendChild(U.el('h2', { text: 'Poziom ' + candidate.level + ' gotowy do egzaminu' }));
    box.appendChild(U.el('p', {
      text: 'Lekcje tego poziomu są przerobione (' + candidate.ready.done + ' z '
        + candidate.ready.total + '). Egzamin sprawdzi cztery sprawności osobno i powie, '
        + 'czy „przerobione” znaczy tu „umiem”.'
    }));
    var goe = U.el('button', { class: 'btn', type: 'button', text: 'Przejdź do egzaminu' });
    goe.addEventListener('click', function () { App.go('exam'); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [goe]));
  }

  /* ================================================== EKRAN: SESJA DNIA */

  /* Karta na ekranie „Dzisiaj”: jeden przycisk, który uruchamia zaplanowaną
     sesję, albo wraca do przerwanej. Podgląd składu pokazujemy PRZED startem,
     bo „zaufaj mi” nie jest dobrym interfejsem — uczący się ma widzieć, co
     dostanie i dlaczego. */
  function renderTodaySession() {
    var box = U.clear(U.$('#today-session'));
    Session.load();

    if (Session.resumable()) {
      var prog = Session.progress();
      box.appendChild(U.el('h2', { text: 'Sesja dnia — przerwana' }));
      box.appendChild(U.el('p', { class: 'muted',
        text: 'Zrobione ' + prog.done + ' z ' + prog.steps + ' kroków · '
          + Math.round(prog.spent / 60) + ' z ' + Session.state.minutes + ' minut.' }));
      box.appendChild(progressBar(prog.share, 'Sesja dnia: ' + prog.done + ' z ' + prog.steps + ' kroków'));
      var back = U.el('button', { class: 'btn gold', type: 'button', text: 'Wróć do sesji' });
      back.addEventListener('click', function () { App.go('session'); });
      var drop = U.el('button', { class: 'btn ghost', type: 'button', text: 'Zacznij od nowa' });
      drop.addEventListener('click', function () {
        Session.clear();
        renderTodaySession();
      });
      box.appendChild(U.el('div', { class: 'btn-row' }, [back, drop]));
      return;
    }

    box.appendChild(U.el('h2', { text: 'Sesja dnia' }));
    box.appendChild(U.el('p', { class: 'muted',
      text: 'Powtórki, nowa lekcja, słuchanie i mówienie — wymieszane i odmierzone czasem. '
        + 'Skład dobiera się sam z tego, gdzie jesteś.' }));

    var row = U.el('div', { class: 'btn-row' });
    Session.LENGTHS.forEach(function (m, i) {
      var b = U.el('button', { class: i === 1 ? 'btn gold' : 'btn', type: 'button',
        text: m + ' minut' });
      b.addEventListener('click', function () { startSession(m); });
      row.appendChild(b);
    });
    box.appendChild(row);

    var preview = U.el('button', { class: 'btn ghost', type: 'button', text: 'Co będzie w sesji?' });
    preview.addEventListener('click', function () { openSessionPreview(20); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [preview]));
  }

  function startSession(minutes) {
    Session.start(minutes);
    App.go('session');
  }

  /* Podgląd składu bez uruchamiania. Ta sama funkcja Session.compose, której
     używa start — nie ma tu drugiego, „poglądowego” algorytmu, który mógłby
     pokazać coś innego, niż uczący się faktycznie dostanie. */
  function openSessionPreview(minutes) {
    var body = U.el('div');
    body.appendChild(U.el('h2', { id: 'sheet-title', text: 'Skład sesji' }));

    var pick = U.el('div', { class: 'btn-row' });
    var listBox = U.el('div');

    function draw(m) {
      U.clear(listBox);
      var plan = Session.compose(m);
      listBox.appendChild(U.el('p', { class: 'muted',
        text: plan.steps + ' ' + U.plural(plan.steps, 'krok', 'kroki', 'kroków')
          + ' · szacowany czas ' + Math.round(plan.estimate / 60) + ' min' }));
      var grouped = {};
      plan.blocks.forEach(function (b) {
        var e = grouped[b.kind] || (grouped[b.kind] = { steps: 0, parts: 0, why: b.why, mode: b.mode, label: b.label });
        e.steps += b.steps;
        e.parts += 1;
      });
      var list = U.el('div', { class: 'list' });
      Object.keys(grouped).forEach(function (k) {
        var g = grouped[k];
        var row = U.el('div', { class: 'row static' });
        var main = U.el('div', { class: 'row-main' });
        main.appendChild(U.el('b', { text: g.label + ' — ' + g.steps + ' '
          + U.plural(g.steps, 'krok', 'kroki', 'kroków')
          + (g.parts > 1 ? ' w ' + g.parts + ' częściach' : '') }));
        main.appendChild(U.el('p', { class: 'muted', text: g.why }));
        row.appendChild(main);
        list.appendChild(row);
      });
      listBox.appendChild(list);
      if (!plan.steps) {
        listBox.appendChild(U.el('p', { class: 'muted',
          text: 'Nie ma z czego zbudować sesji — baza jeszcze się wczytuje albo kurs jest ukończony.' }));
      }
    }

    Session.LENGTHS.forEach(function (m) {
      var b = U.el('button', { class: 'chip', type: 'button', text: m + ' min',
        'aria-pressed': m === minutes ? 'true' : 'false' });
      b.addEventListener('click', function () {
        U.$$('.chip', pick).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        draw(m);
      });
      pick.appendChild(b);
    });
    body.appendChild(pick);
    body.appendChild(listBox);
    draw(minutes);
    openSheet(body);
  }

  /* -------------------------------------------------------- bieg sesji */

  /* Wynik bieżącego kroku. Ustawiany przez obserwatora Progress.onAnswer,
     odczytywany, gdy ćwiczenie odda sterowanie. Tylko PIERWSZA odpowiedź
     w kroku się liczy — część ćwiczeń melduje kilka razy (np. rola w dialogu
     kwestia po kwestii), a krok jest jeden. */
  var stepResult = { known: false, ok: null };

  function watchAnswers(on) {
    Progress.onAnswer = on ? function (id, ok) {
      if (stepResult.known) return;
      stepResult.known = true;
      stepResult.ok = !!ok;
    } : null;
  }

  RENDER.session = function () {
    Session.load();

    if (Session.stale()) {
      /* Sesja z poprzedniego dnia. Jej skład opisywał wczorajszą kolejkę
         powtórek, więc wznowienie dałoby plan nieaktualny — mówimy o tym
         wprost, zamiast po cichu podmieniać zawartość. */
      var head0 = U.clear(U.$('#session-head'));
      var area0 = U.clear(U.$('#session-area'));
      head0.appendChild(U.el('h2', { text: 'Nieskończona sesja z ' + U.dateWords(Session.state.date) }));
      head0.appendChild(U.el('p', { class: 'muted',
        text: 'Jej skład był dobrany do stanu z tamtego dnia — dziś kolejka powtórek wygląda inaczej. '
          + 'Nowa sesja weźmie aktualny stan.' }));
      var fresh = U.el('button', { class: 'btn gold', type: 'button', text: 'Zaplanuj dzisiejszą sesję' });
      fresh.addEventListener('click', function () { Session.clear(); RENDER.session(); });
      head0.appendChild(U.el('div', { class: 'btn-row' }, [fresh]));
      area0.appendChild(U.el('p', { class: 'muted', text: 'Postęp z tamtej sesji jest już zapisany w powtórkach i statystykach — nic nie przepadło.' }));
      return;
    }

    if (!Session.state || Session.state.finished) {
      renderSessionStart();
      return;
    }

    Session.resume();
    renderSessionHead();
    renderSessionStep();
  };

  function renderSessionStart() {
    var head = U.clear(U.$('#session-head'));
    var area = U.clear(U.$('#session-area'));

    head.appendChild(U.el('h2', { text: 'Ile masz dziś czasu?' }));
    var row = U.el('div', { class: 'btn-row' });
    Session.LENGTHS.forEach(function (m, i) {
      var b = U.el('button', { class: i === 1 ? 'btn gold' : 'btn', type: 'button', text: m + ' minut' });
      b.addEventListener('click', function () { Session.start(m); RENDER.session(); });
      row.appendChild(b);
    });
    head.appendChild(row);

    /* Ostatnia sesja — jeśli była dziś, mówimy o tym, żeby nikt nie robił
       drugiej w przekonaniu, że pierwsza się nie zapisała. */
    var log = Session.log();
    var last = log.length ? log[log.length - 1] : null;
    if (last && last.d === U.today()) {
      head.appendChild(U.el('p', { class: 'muted',
        text: 'Dzisiejsza sesja jest już zrobiona: ' + Math.round(last.spent / 60)
          + ' min, ' + last.answers + ' ' + U.plural(last.answers, 'odpowiedź', 'odpowiedzi', 'odpowiedzi')
          + '. Kolejna nie zaszkodzi, ale nie jest potrzebna.' }));
    }

    var plan = Session.compose(20);
    area.appendChild(U.el('h2', { text: 'Co jest w planie' }));
    if (!plan.steps) {
      area.appendChild(U.el('p', { class: 'muted', text: 'Materiał jeszcze się wczytuje.' }));
      return;
    }
    area.appendChild(U.el('p', { class: 'muted',
      text: 'Podgląd dla sesji dwudziestominutowej. Przy innych długościach zmieniają się proporcje, nie rodzaje bloków.' }));
    var grouped = {};
    plan.blocks.forEach(function (b) {
      var e = grouped[b.kind] || (grouped[b.kind] = { steps: 0, label: b.label, why: b.why });
      e.steps += b.steps;
    });
    var list = U.el('div', { class: 'list' });
    Object.keys(grouped).forEach(function (k) {
      var g = grouped[k];
      var row2 = U.el('div', { class: 'row static' });
      var main = U.el('div', { class: 'row-main' });
      main.appendChild(U.el('b', { text: g.label + ' · ' + g.steps + ' ' + U.plural(g.steps, 'krok', 'kroki', 'kroków') }));
      main.appendChild(U.el('p', { class: 'muted', text: g.why }));
      row2.appendChild(main);
      list.appendChild(row2);
    });
    area.appendChild(list);
  }

  function renderSessionHead() {
    var head = U.clear(U.$('#session-head'));
    var prog = Session.progress();
    var block = Session.current();

    head.appendChild(U.el('h2', { text: block ? block.label : 'Sesja dnia' }));
    head.appendChild(U.el('p', { class: 'muted', id: 'session-status', role: 'status',
      text: 'Krok ' + Math.min(prog.done + 1, prog.steps) + ' z ' + prog.steps
        + ' · ' + Math.round(prog.spent / 60) + ' z ' + Session.state.minutes + ' min'
        + (prog.overtime ? ' (ponad plan)' : '') }));
    head.appendChild(progressBar(prog.share, 'Sesja: ' + prog.done + ' z ' + prog.steps + ' kroków'));
    if (block && block.why) head.appendChild(U.el('p', { class: 'muted', text: block.why }));

    var pause = U.el('button', { class: 'btn ghost', type: 'button', text: 'Przerwij i wróć później' });
    pause.addEventListener('click', function () {
      Session.pause();
      watchAnswers(false);
      U.toast('Sesja zatrzymana. Wróci w tym samym miejscu.');
      App.go('today');
    });
    var skip = U.el('button', { class: 'btn ghost', type: 'button', text: 'Pomiń ten blok' });
    skip.addEventListener('click', function () {
      Session.skipBlock();
      RENDER.session();
    });
    head.appendChild(U.el('div', { class: 'btn-row' }, [pause, skip]));
  }

  /* Krok sesji. Każdy rodzaj bloku oddaje sterowanie przez `done` — dopiero
     wtedy sesja liczy krok i decyduje, co dalej. */
  function renderSessionStep() {
    var area = U.clear(U.$('#session-area'));
    var block = Session.current();
    if (!block) { renderSessionSummary(); return; }

    stepResult = { known: false, ok: null };
    watchAnswers(true);

    function done() {
      watchAnswers(false);
      Session.step(stepResult.known ? stepResult.ok : null);
      if (!Session.current()) { renderSessionSummary(); return; }
      renderSessionHead();
      renderSessionStep();
    }

    if (block.kind === 'srs') return sessionSrsStep(area, done);
    if (block.kind === 'lesson') return sessionLessonStep(area, done);
    if (block.kind === 'pron') { Produce.mode = 'say'; return sessionProduceStep(area, done, true); }
    if (block.kind === 'produce') { Produce.mode = block.mode || 'build'; return sessionProduceStep(area, done); }
    Quiz.mode = block.mode || 'choice';
    return sessionListenStep(area, done);
  }

  /* Wyjście z pojedynczego kroku.

     Blok wymowy czeka na nagranie i bez mikrofonu — albo w miejscu, gdzie nie
     wypada mówić na głos — nie da się go dokończyć. „Pomiń ten blok” z nagłówka
     wyrzuca wtedy całą wymowę z sesji, co jest karą za brak ciszy. To jest
     wyjście z jednego kroku: krok liczy się jako zrobiony bez wyniku, blok
     idzie dalej. */
  function stepEscape(area, done, label) {
    var b = U.el('button', { class: 'btn ghost', type: 'button', text: label || 'Pomiń to hasło' });
    b.addEventListener('click', done);
    area.appendChild(U.el('div', { class: 'btn-row' }, [b]));
  }

  function sessionListenStep(area, done) {
    Quiz.ensureData().then(function () {
      if (App.screen !== 'session') return;
      Quiz.renderListenStep(area, done);
    });
  }

  function sessionProduceStep(area, done, escapable) {
    area.appendChild(U.el('p', { class: 'muted', role: 'status', text: 'Przygotowuję ćwiczenie…' }));
    Produce.ensureData().then(function () {
      if (App.screen !== 'session') return;
      Produce.renderStep(area, done);
      if (escapable) stepEscape(area, done);
    });
  }

  /* Powtórka w sesji. Ta sama karta co na ekranie „Powtórki”, ale bez
     zapętlania i bez listy zaległości — sesja ma własny licznik postępu
     i drugi w środku bloku byłby hałasem. */
  function sessionSrsStep(area, done) {
    var plan = SRS.plan();
    var card = plan.today[0];
    if (!card) {
      area.appendChild(U.el('p', { class: 'muted', text: 'Kolejka powtórek jest pusta — ten blok jest zrobiony.' }));
      var go = U.el('button', { class: 'btn', type: 'button', text: 'Dalej' });
      go.addEventListener('click', function () { Session.skipBlock(); RENDER.session(); });
      area.appendChild(U.el('div', { class: 'btn-row' }, [go]));
      return;
    }

    if (SRS.isContrastCard(card.id)) {
      /* Karta kontrastu słuchowego ma własny renderer na ekranie powtórek.
         W sesji pokazujemy ją tak samo, a po ocenie wracamy tutaj. */
      renderContrastCard(area, card, 1);
      var next = U.el('button', { class: 'btn', type: 'button', text: 'Dalej' });
      next.addEventListener('click', done);
      area.appendChild(U.el('div', { class: 'btn-row' }, [next]));
      return;
    }

    var side = SRS.sideOf(card.id);
    var source = srsSource(card.id, function () {
      if (App.screen === 'session') sessionSrsStep(U.clear(area), done);
    });
    if (source === null) return sessionSrsStep(U.clear(area), done);   /* sierota — skasowana */
    if (source === undefined) {
      area.appendChild(U.el('p', { class: 'muted', role: 'status', text: 'Wczytuję hasło…' }));
      return;
    }
    var rec = G.view(source);

    if (side === 'w') {
      renderPronCard(area, card, rec, source);
      var nextW = U.el('button', { class: 'btn', type: 'button', text: 'Dalej' });
      nextW.addEventListener('click', done);
      area.appendChild(U.el('div', { class: 'btn-row' }, [nextW]));
      return;
    }

    var receptive = side === 'r';
    area.appendChild(U.el('p', { class: 'm0-kind muted',
      text: SRS.sideName(side) + ' · ' + SRS.SIDE_LONG[side] }));

    var answer = U.el('div', { hidden: 'hidden' });
    if (receptive) {
      area.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: App.settings.hideTones }));
      answer.appendChild(U.el('p', { class: 'bc-pl', text: rec.polish }));
      answer.appendChild(U.el('p', { class: 'muted', text: rec.toneGuide }));
    } else {
      area.appendChild(U.el('p', { class: 'bc-pl', text: rec.polish }));
      answer.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: App.settings.hideTones }));
      answer.appendChild(U.el('p', { class: 'muted', text: 'Czytaj: ' + rec.pronunciationPolish }));
      answer.appendChild(U.el('p', { class: 'muted', text: rec.toneGuide }));
    }
    area.appendChild(answer);

    var show = U.el('button', { class: 'btn', type: 'button',
      text: receptive ? 'Pokaż znaczenie' : 'Pokaż odpowiedź' });
    var grades = U.el('div', { class: 'btn-row', hidden: 'hidden' });
    show.addEventListener('click', function () {
      answer.hidden = false;
      show.hidden = true;
      grades.hidden = false;
      Player.play(rec);
    });
    var head = [show];
    if (receptive) head.push(Player.button(rec, 'Posłuchaj'));
    area.appendChild(U.el('div', { class: 'btn-row' }, head));

    [['Nie pamiętam', 0], ['Trudne', 3], ['Dobrze', 4], ['Łatwe', 5]].forEach(function (g) {
      var b = U.el('button', { class: g[1] >= 4 ? 'btn' : 'btn ghost', type: 'button', text: g[0] });
      b.addEventListener('click', function () {
        SRS.grade(source.id, g[1], { side: side });
        Progress.answer(source.id, g[1] >= 3, { mode: receptive ? 'srs-rec' : 'srs-prod' });
        done();
      });
      grades.appendChild(b);
    });
    area.appendChild(grades);
  }

  /* Nowe hasło z najbliższej lekcji kursu. Blok wprowadza hasła pojedynczo
     i zakłada im karty powtórek — sprawdzian całej lekcji zostaje na ekranie
     kursu, bo jest testem, a nie wprowadzeniem. */
  function sessionLessonStep(area, done) {
    var block = Session.current();
    var lesson = block && block.lessonId ? Course.byId(block.lessonId) : Course.next();
    if (!lesson) {
      area.appendChild(U.el('p', { class: 'muted', text: 'Kurs jest ukończony — nie ma nowych haseł do wprowadzenia.' }));
      var go = U.el('button', { class: 'btn', type: 'button', text: 'Dalej' });
      go.addEventListener('click', function () { Session.skipBlock(); RENDER.session(); });
      area.appendChild(U.el('div', { class: 'btn-row' }, [go]));
      return;
    }

    area.appendChild(U.el('p', { class: 'muted', role: 'status', text: 'Wczytuję lekcję…' }));
    Course.load(lesson).then(function (material) {
      if (App.screen !== 'session') return;
      U.clear(area);
      /* Bierzemy pierwsze hasło, które nie ma jeszcze karty rozpoznania —
         dzięki temu kolejne kroki bloku idą po kolei, a powrót do przerwanej
         sesji nie zaczyna od początku listy. */
      var fresh = material.newWords.filter(function (r) { return !SRS.has(r.id, 'r'); });
      var pick = fresh[0] || material.newWords[0];
      if (!pick) {
        area.appendChild(U.el('p', { class: 'muted', text: 'Ta lekcja nie wprowadza nowych haseł.' }));
        var skip = U.el('button', { class: 'btn', type: 'button', text: 'Dalej' });
        skip.addEventListener('click', function () { Session.skipBlock(); RENDER.session(); });
        area.appendChild(U.el('div', { class: 'btn-row' }, [skip]));
        return;
      }
      var rec = G.view(pick);
      area.appendChild(U.el('p', { class: 'muted', text: lesson.title }));
      area.appendChild(U.el('p', { class: 'bc-pl', text: rec.polish }));
      area.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: App.settings.hideTones }));
      area.appendChild(U.el('p', { class: 'muted', text: 'Czytaj: ' + rec.pronunciationPolish }));
      if (rec.toneGuide) area.appendChild(U.el('p', { class: 'muted', text: rec.toneGuide }));

      var add = U.el('button', { class: 'btn', type: 'button', text: 'Umiem — dodaj do powtórek' });
      add.addEventListener('click', function () {
        SRS.addBoth(pick.id);
        Progress.answer(pick.id, true, { mode: 'lesson-intro' });
        done();
      });
      var details = U.el('button', { class: 'btn ghost', type: 'button', text: 'Szczegóły hasła' });
      details.addEventListener('click', function () { App.openRecord(pick.id); });
      area.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(rec, 'Posłuchaj'), add, details]));
    });
  }

  function renderSessionSummary() {
    var head = U.clear(U.$('#session-head'));
    var area = U.clear(U.$('#session-area'));
    var s = Session.state;
    var log = Session.log();
    var last = log.length ? log[log.length - 1] : null;

    head.appendChild(U.el('h2', { text: 'Sesja skończona' }));
    if (last) {
      head.appendChild(U.el('p', { class: 'muted',
        text: Math.round(last.spent / 60) + ' ' + U.plural(Math.round(last.spent / 60), 'minuta', 'minuty', 'minut')
          + ' · ' + last.answers + ' ' + U.plural(last.answers, 'odpowiedź', 'odpowiedzi', 'odpowiedzi')
          + (last.answers ? ' · skuteczność ' + Math.round(last.correct / last.answers * 100) + '%' : '') }));
      var list = U.el('div', { class: 'list' });
      Object.keys(last.blocks).forEach(function (k) {
        var b = last.blocks[k];
        var row = U.el('div', { class: 'row static' });
        var main = U.el('div', { class: 'row-main' });
        main.appendChild(U.el('b', { text: Session.LABELS[k] || k }));
        main.appendChild(U.el('p', { class: 'muted',
          text: b.done + ' z ' + b.steps + ' ' + U.plural(b.steps, 'kroku', 'kroków', 'kroków')
            + (b.done && b.correct !== undefined && k !== 'lesson'
               ? ' · trafionych ' + b.correct : '') }));
        row.appendChild(main);
        list.appendChild(row);
      });
      area.appendChild(list);
    }

    var goalState = Goals.today();
    area.appendChild(U.el('p', { class: 'muted',
      text: goalState.met
        ? 'Cel dnia zrobiony: ' + goalState.done + ' z ' + goalState.minutes + ' minut.'
        : 'Do celu dnia zostało ' + goalState.left + ' ' + U.plural(goalState.left, 'minuta', 'minuty', 'minut') + '.' }));

    var again = U.el('button', { class: 'btn', type: 'button', text: 'Jeszcze jedna sesja' });
    again.addEventListener('click', function () { Session.clear(); RENDER.session(); });
    var toWeek = U.el('button', { class: 'btn ghost', type: 'button', text: 'Podsumowanie tygodnia' });
    toWeek.addEventListener('click', function () { App.go('week'); });
    var home = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wróć na Dzisiaj' });
    home.addEventListener('click', function () { App.go('today'); });
    area.appendChild(U.el('div', { class: 'btn-row' }, [again, toWeek, home]));
    if (s) Session.clear();
  }

  /* ============================================ POKRYCIE I DROGA DO CELU */

  /* Karta na ekranie „Dzisiaj”: cztery sytuacje, w których ta nauka ma się
     przydać, i uczciwa liczba przy każdej. */
  function renderTodayCoverage() {
    var box = U.clear(U.$('#today-coverage'));
    box.appendChild(U.el('h2', { text: 'Ile już rozumiesz' }));

    if (!Coverage.ready()) {
      box.appendChild(U.el('p', { class: 'muted', role: 'status', text: 'Liczę pokrycie…' }));
      Coverage.ensure().then(function () {
        if (App.screen === 'today') renderTodayCoverage();
      });
      return;
    }

    var list = Coverage.headline();
    if (!list.length) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Brak danych o pokryciu.' }));
      return;
    }

    var wrap = U.el('div', { class: 'list' });
    list.forEach(function (c) {
      var row = U.el('div', { class: 'row static' });
      var main = U.el('div', { class: 'row-main' });
      main.appendChild(U.el('b', { text: c.name + ' — ' + Math.round(c.coverage * 100) + '%' }));
      main.appendChild(progressBar(c.coverage, c.name + ': pokrycie ' + Math.round(c.coverage * 100) + '%'));
      main.appendChild(U.el('p', { class: 'muted',
        text: 'znasz ' + c.known + ' z ' + c.occurrences + ' wyrazów w materiale tej kategorii'
          + ' · zrozumiałych kwestii ' + Math.round(c.linesShare * 100) + '%' }));
      row.appendChild(main);
      wrap.appendChild(row);
    });
    box.appendChild(wrap);

    var how = U.el('button', { class: 'btn ghost', type: 'button', text: 'Jak to liczymy' });
    how.addEventListener('click', openCoverageMethod);
    var map = U.el('button', { class: 'btn', type: 'button', text: 'Droga do celu' });
    map.addEventListener('click', function () { App.go('roadmap'); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [map, how]));
  }

  /* Metoda wyliczenia — w interfejsie, nie tylko w dokumentacji. Liczba, której
     nie da się sprawdzić, jest nie do odróżnienia od wymyślonej. */
  function openCoverageMethod() {
    var t = Coverage.totals();
    var m = Coverage.method();
    var body = U.el('div');
    body.appendChild(U.el('h2', { id: 'sheet-title', text: 'Jak liczymy pokrycie rozumienia' }));

    body.appendChild(U.el('h3', { text: 'Co jest mierzone' }));
    body.appendChild(U.el('p', { text:
      'Dla każdej kategorii bierzemy wszystkie kwestie dialogów, które do niej należą — '
      + 'prawdziwe zdania, które aplikacja Ci odtwarza, a nie listę haseł. '
      + 'Kwestie dzielimy na wyrazy i liczymy, jaki procent WYSTĄPIEŃ wyrazów znasz. '
      + 'Wyraz częsty liczy się tyle razy, ile razy pada.' }));
    body.appendChild(U.el('p', { class: 'muted', text:
      'Korpus: ' + t.lines + ' kwestii z ' + t.dialogues + ' dialogów, '
      + t.occurrences + ' wystąpień wyrazów w ' + t.categories + ' kategoriach.' }));

    body.appendChild(U.el('h3', { text: 'Co znaczy „znasz”' }));
    body.appendChild(U.el('p', { text:
      'Hasło ma w powtórkach opanowaną kartę ROZPOZNANIA: co najmniej '
      + SRS.LEARNED.repetitions + ' udane powtórzenia i odstęp od '
      + SRS.LEARNED.interval + ' dni w górę. Nie liczy się hasło obejrzane raz w słowniku '
      + 'ani hasło dopiero co dodane do kolejki — jedno i drugie podniosłoby liczbę, '
      + 'nie podnosząc rozumienia. Bierzemy stronę rozpoznania, bo rozumienie rozmowy '
      + 'jest umiejętnością bierną: co innego umieć powiedzieć „rachunek”, a co innego '
      + 'zrozumieć je rzucone szybko przez kelnera.' }));

    body.appendChild(U.el('h3', { text: 'Skąd wiadomo, że wyraz to właśnie to hasło' }));
    body.appendChild(U.el('p', { text:
      'Porównujemy zapis bez tonów i bez dywizów, dopasowując najpierw dłuższe zwroty '
      + '(trzy wyrazy, potem dwa, potem jeden) — inaczej utrwalone wyrażenie rozpadłoby się '
      + 'na części znaczące co innego.' }));

    body.appendChild(U.el('h3', { text: 'Ograniczenia — proszę je znać' }));
    var lim = U.el('ul');
    lim.appendChild(U.el('li', { text:
      'SUFIT. ' + t.unmapped + ' z ' + t.occurrences + ' wystąpień ('
      + Math.round(t.unmapped / t.occurrences * 100) + '%) to wyrazy, których w bazie nie ma '
      + 'jako osobnych haseł. Liczymy je jako NIEZNANE i zostawiamy w mianowniku, '
      + 'bo słyszysz je w nagraniu niezależnie od tego, czy aplikacja umie je nazwać. '
      + 'Dlatego 100% jest nieosiągalne, a w części kategorii nieosiągalne jest też 95%.' }));
    lim.appendChild(U.el('li', { text:
      'HOMOFONY. ' + t.ambiguous + ' wystąpień (' + Math.round(t.ambiguous / t.occurrences * 100)
      + '%) ma w bazie więcej niż jedno hasło o tym samym zapisie i różnym znaczeniu. '
      + 'Bierzemy częstsze. Tam, gdzie w zdaniu chodziło o to drugie, pokrycie jest zawyżone.' }));
    lim.appendChild(U.el('li', { text:
      'ZAPIS. ' + t.loose + ' wystąpień dopasowano po skróceniu podwojonej samogłoski '
      + '(„tàae” do „tàe”), bo ta sama jednostka bywa w naszych danych zapisana dwojako. '
      + 'Robimy to tylko wtedy, gdy prowadzi to do dokładnie jednego hasła.' }));
    lim.appendChild(U.el('li', { text:
      'ZNAJOMOŚĆ WYRAZU TO NIE ROZUMIENIE ZDANIA. Można znać wszystkie wyrazy i nie zrozumieć '
      + 'zdania — przez tempo, redukcje albo składnię. Pokrycie leksykalne jest warunkiem '
      + 'koniecznym rozumienia, nie wystarczającym.' }));
    lim.appendChild(U.el('li', { text:
      'KORPUS TO NIE ULICA. Mierzymy pokrycie w materiale aplikacji. Prawdziwa rozmowa ma '
      + 'szerszy zasób słów, więc liczba tutaj jest górnym oszacowaniem tego, co zrozumiesz w Tajlandii.' }));
    body.appendChild(lim);

    body.appendChild(U.el('h3', { text: 'Próg' }));
    body.appendChild(U.el('p', { text:
      'Za „rozumiem tę kategorię” przyjmujemy ' + Math.round((m.target || 0.95) * 100)
      + '% pokrycia. Przy takim udziale znanych wyrazów przekaz zwykle się składa; '
      + 'przy 80% zwykle nie. Kwestię uznajemy za zrozumiałą, gdy znasz co najmniej '
      + Math.round((m.lineThreshold || 0.95) * 100) + '% jej wyrazów.' }));

    openSheet(body);
  }

  /* ------------------------------------------------------ mapa drogi */

  RENDER.roadmap = function () {
    var stats = U.clear(U.$('#roadmap-stats'));
    var method = U.clear(U.$('#roadmap-method'));
    var list = U.clear(U.$('#roadmap-list'));

    if (!Coverage.ready()) {
      method.appendChild(U.el('p', { class: 'muted', role: 'status', text: 'Wczytuję dane pokrycia…' }));
      Coverage.ensure().then(function () {
        if (App.screen === 'roadmap') RENDER.roadmap();
      });
      return;
    }

    Retro.snapshot();

    var all = Coverage.solid();
    var done = all.filter(function (c) { return c.coverage >= c.goal; }).length;
    var pace = Coverage.pace();
    var perLesson = Coverage.wordsPerLesson();

    var totalGap = 0;
    all.forEach(function (c) {
      var g = Coverage.gap(c.name);
      if (g && !g.done) totalGap += g.words;
    });

    stats.appendChild(statBox(done + '/' + all.length, 'kategorii domkniętych'));
    stats.appendChild(statBox(totalGap, 'haseł do celu'));
    stats.appendChild(statBox(Math.ceil(totalGap / perLesson), 'lekcji'));
    stats.appendChild(statBox(pace.known ? Math.round(pace.perWeek) : '—', 'haseł na tydzień'));

    method.appendChild(U.el('h2', { text: 'Jak czytać tę mapę' }));
    method.appendChild(U.el('p', { class: 'muted', text:
      'Cel kategorii to ' + Math.round(Coverage.target() * 100) + '% pokrycia — albo sufit metody, '
      + 'jeśli leży niżej. Liczba haseł to najkrótsza droga: hasła brane od najczęstszego '
      + 'w materiale tej kategorii. Ucząc się w innej kolejności, potrzebujesz ich więcej.' }));
    if (!pace.known) {
      method.appendChild(U.el('p', { class: 'muted', text:
        'Tempa jeszcze nie da się policzyć — potrzeba haseł opanowanych w co najmniej trzech '
        + 'różnych dniach. Do tego czasu mapa pokazuje odległość w hasłach i lekcjach, ale nie w czasie.' }));
    } else {
      method.appendChild(U.el('p', { class: 'muted', text:
        'Tempo liczone z ostatnich czterech tygodni: ' + pace.perWeek.toFixed(1).replace('.', ',')
        + ' opanowanych haseł tygodniowo (' + pace.inWindow + ' w ' + pace.activeDays + ' dniach). '
        + 'Lekcja wprowadza mediana ' + perLesson + ' nowych haseł.' }));
    }
    var how = U.el('button', { class: 'btn ghost', type: 'button', text: 'Metoda wyliczenia pokrycia' });
    how.addEventListener('click', openCoverageMethod);
    method.appendChild(U.el('div', { class: 'btn-row' }, [how]));

    var sorted = Coverage.all().slice().sort(function (a, b) {
      if (a.thin !== b.thin) return a.thin ? 1 : -1;
      return (b.goal - b.coverage) - (a.goal - a.coverage);
    });

    var weekGoal = Goals.category();

    sorted.forEach(function (c) {
      var gap = Coverage.gap(c.name);
      var weeks = Coverage.weeksTo(c.name);
      var row = U.el('div', { class: 'row static' });
      var main = U.el('div', { class: 'row-main' });

      main.appendChild(U.el('b', { text: c.name + ' — ' + Math.round(c.coverage * 100) + '%'
        + (weekGoal && !weekGoal.expired && weekGoal.name === c.name ? ' · cel tygodnia' : '') }));
      main.appendChild(progressBar(c.coverage / Math.max(0.01, c.goal),
        c.name + ': ' + Math.round(c.coverage * 100) + '% z celu ' + Math.round(c.goal * 100) + '%'));

      var line;
      if (gap && gap.done) {
        line = 'Cel osiągnięty (' + Math.round(c.goal * 100) + '%). '
          + 'Zrozumiałych kwestii: ' + Math.round(c.linesShare * 100) + '%.';
      } else if (gap) {
        line = 'Do celu ' + Math.round(c.goal * 100) + '%: ' + gap.words + ' '
          + U.plural(gap.words, 'hasło', 'hasła', 'haseł')
          + ' · ' + Math.max(1, Math.ceil(gap.words / perLesson)) + ' '
          + U.plural(Math.max(1, Math.ceil(gap.words / perLesson)), 'lekcja', 'lekcje', 'lekcji');
        if (weeks === null) line += ' · czasu jeszcze nie da się oszacować';
        else if (weeks <= 1) line += ' · około tygodnia przy obecnym tempie';
        else line += ' · około ' + Math.ceil(weeks) + ' '
          + U.plural(Math.ceil(weeks), 'tygodnia', 'tygodni', 'tygodni') + ' przy obecnym tempie';
      } else {
        line = 'Brak danych.';
      }
      main.appendChild(U.el('p', { class: 'muted', text: line }));

      var notes = [];
      if (c.goalIsCeiling) {
        notes.push('Próg ' + Math.round(Coverage.target() * 100) + '% jest tu nieosiągalny: '
          + c.unmapped + ' z ' + c.occurrences + ' wystąpień to wyrazy spoza bazy. '
          + 'Celem jest sufit metody, czyli ' + Math.round(c.ceiling * 100) + '%.');
      }
      if (c.thin) {
        notes.push('Mało materiału (' + c.lines + ' '
          + U.plural(c.lines, 'kwestia', 'kwestie', 'kwestii') + ') — liczba jest niepewna.');
      }
      if (c.inProgress) {
        notes.push('W nauce, jeszcze nieopanowane: ' + c.inProgress + ' wystąpień. '
          + 'Po ich domknięciu pokrycie sięgnie ' + Math.round(c.reach * 100) + '%.');
      }
      notes.forEach(function (n) { main.appendChild(U.el('p', { class: 'muted small', text: n })); });

      row.appendChild(main);

      var actions = U.el('div', { class: 'btn-row' });
      if (gap && !gap.done) {
        /* To są przyciski akcji, nie przełączniki filtra. Klasa `chip` jest
           w tej aplikacji zarezerwowana dla przełączników i przegląd
           dostępności słusznie wymaga od niej aria-pressed — którego akcja
           nie ma czym wypełnić. */
        var setGoal = U.el('button', { class: 'btn ghost', type: 'button',
          text: (weekGoal && !weekGoal.expired && weekGoal.name === c.name)
            ? 'Cel tygodnia ustawiony' : 'Cel na ten tydzień' });
        setGoal.addEventListener('click', function () {
          Goals.setCategory(c.name);
          U.toast('Cel tygodnia: domykam „' + c.name + '”.');
          RENDER.roadmap();
        });
        actions.appendChild(setGoal);
      }
      var words = U.el('button', { class: 'btn ghost', type: 'button', text: 'Czego się uczyć' });
      words.addEventListener('click', function () { openCoverageWords(c.name); });
      actions.appendChild(words);
      main.appendChild(actions);

      list.appendChild(row);
    });
  };

  /* Hasła, które najmocniej podniosą pokrycie w tej kategorii. Można je stąd
     wrzucić do powtórek — inaczej mapa mówiłaby, co robić, i nie dawała tego
     zrobić. */
  function openCoverageWords(name) {
    var body = U.el('div');
    body.appendChild(U.el('h2', { id: 'sheet-title', text: name + ' — co podniesie pokrycie' }));
    var items = Coverage.nextItems(name, 25);
    if (!items.length) {
      body.appendChild(U.el('p', { class: 'muted', text: 'Wszystkie hasła z materiału tej kategorii masz już opanowane.' }));
      openSheet(body);
      return;
    }
    body.appendChild(U.el('p', { class: 'muted', text:
      'Kolejność wprost z liczby wystąpień w materiale kategorii. Liczba przy haśle mówi, '
      + 'ile razy pada w kwestiach dialogów — tyle wystąpień domkniesz, ucząc się go.' }));

    var note = U.el('p', { class: 'muted', role: 'status', text: 'Wczytuję hasła…' });
    body.appendChild(note);
    var list = U.el('div', { class: 'list' });
    body.appendChild(list);

    var addAll = U.el('button', { class: 'btn', type: 'button', text: 'Dodaj 10 pierwszych do powtórek' });
    addAll.addEventListener('click', function () {
      var n = 0;
      items.slice(0, 10).forEach(function (it) {
        if (!SRS.has(it.id, 'r')) { SRS.addBoth(it.id); n += 1; }
      });
      U.toast(n ? 'Dodano ' + n + ' ' + U.plural(n, 'hasło', 'hasła', 'haseł') + ' do powtórek.'
                : 'Te hasła są już w powtórkach.');
      if (App.screen === 'roadmap') RENDER.roadmap();
    });
    body.appendChild(U.el('div', { class: 'btn-row' }, [addAll]));
    openSheet(body);

    DB.ensureFor(items.map(function (i) { return i.id; })).then(function () {
      note.hidden = true;
      U.clear(list);
      items.forEach(function (it) {
        var src = DB.any(it.id);
        if (!src) return;
        var rec = G.view(src);
        var row = U.el('button', { class: 'row', type: 'button' });
        var main = U.el('div', { class: 'row-main' });
        main.appendChild(U.el('b', { text: rec.polish }));
        main.appendChild(U.el('p', { class: 'muted',
          text: rec.thaiPhonetic + ' · pada ' + it.weight + ' '
            + U.plural(it.weight, 'raz', 'razy', 'razy')
            + (it.started ? ' · w nauce' : '') }));
        row.appendChild(main);
        row.addEventListener('click', function () { App.openRecord(it.id); });
        list.appendChild(row);
      });
    });
  }

  /* ================================================ EKRAN: TYDZIEŃ */

  RENDER.week = function () {
    var statRow = U.clear(U.$('#week-stats'));
    var recBox = U.clear(U.$('#week-recommend'));
    var goalBox = U.clear(U.$('#week-goal'));
    var movedBox = U.clear(U.$('#week-moved'));
    var daysBox = U.clear(U.$('#week-days'));
    var histBox = U.clear(U.$('#week-history'));

    if (Coverage.ready()) Retro.snapshot();

    var sum = Retro.summary();
    var now = sum.now;

    statRow.appendChild(statBox(now.minutes, 'minut w tygodniu'));
    statRow.appendChild(statBox(now.activeDays + '/7', 'dni z nauką'));
    statRow.appendChild(statBox(now.sessions, U.plural(now.sessions, 'sesja dnia', 'sesje dnia', 'sesji dnia')));
    statRow.appendChild(statBox(now.accuracy === null ? '—' : now.accuracy + '%', 'skuteczność'));

    /* --- jedna rekomendacja --- */
    recBox.appendChild(U.el('h2', { text: 'Na przyszły tydzień' }));
    var r = sum.recommendation;
    recBox.appendChild(U.el('p', { text: r.text }));
    if (r.action) {
      var go = U.el('button', { class: 'btn gold', type: 'button', text: r.action.label });
      go.addEventListener('click', function () {
        if (r.action.category) Goals.setCategory(r.action.category);
        App.go(r.action.screen);
      });
      recBox.appendChild(U.el('div', { class: 'btn-row' }, [go]));
    }

    /* --- cel kategorialny --- */
    goalBox.appendChild(U.el('h2', { text: 'Cel tygodnia' }));
    var cat = Goals.category();
    if (!cat) {
      var suggestion = Goals.suggestCategory();
      goalBox.appendChild(U.el('p', { class: 'muted', text:
        'Nie masz celu kategorialnego. Cel wyrażony w jednej sytuacji („domykam restaurację”) '
        + 'ma widoczny koniec — w odróżnieniu od „uczę się dalej”.' }));
      if (suggestion) {
        var set = U.el('button', { class: 'btn', type: 'button', text: 'Domykam „' + suggestion + '”' });
        set.addEventListener('click', function () {
          Goals.setCategory(suggestion);
          RENDER.week();
        });
        goalBox.appendChild(U.el('div', { class: 'btn-row' }, [set]));
        goalBox.appendChild(U.el('p', { class: 'muted small', text:
          'Podpowiadamy kategorię najbliższą domknięcia, nie najsłabszą — najsłabsza zwykle '
          + 'ma tyle materiału, że tydzień nie wystarczy, a cel nieosiągalny przestaje być celem.' }));
      }
    } else {
      goalBox.appendChild(U.el('p', { text: 'Domykam „' + cat.name + '”'
        + (cat.expired ? ' (cel z poprzedniego tygodnia)' : '') }));
      goalBox.appendChild(progressBar(cat.goal ? cat.coverage / cat.goal : 0,
        cat.name + ': ' + Math.round(cat.coverage * 100) + '% z ' + Math.round(cat.goal * 100) + '%'));
      goalBox.appendChild(U.el('p', { class: 'muted', text:
        'Pokrycie ' + Math.round(cat.coverage * 100) + '% z celu ' + Math.round(cat.goal * 100) + '%'
        + (cat.gained > 0 ? ' · w tym tygodniu +' + (cat.gained * 100).toFixed(1).replace('.', ',') + ' punktu' : '')
        + (cat.wordsLeft ? ' · zostało ' + cat.wordsLeft + ' ' + U.plural(cat.wordsLeft, 'hasło', 'hasła', 'haseł') : '') }));
      if (cat.done) goalBox.appendChild(U.el('p', { class: 'fb ok', role: 'status', text: 'Cel osiągnięty.' }));
      var change = U.el('button', { class: 'btn ghost', type: 'button', text: 'Zmień cel' });
      change.addEventListener('click', function () { App.go('roadmap'); });
      var drop = U.el('button', { class: 'btn ghost', type: 'button', text: 'Usuń cel' });
      drop.addEventListener('click', function () { Goals.setCategory(null); RENDER.week(); });
      goalBox.appendChild(U.el('div', { class: 'btn-row' }, [change, drop]));
    }

    /* --- gdzie postęp, gdzie stój --- */
    movedBox.appendChild(U.el('h2', { text: 'Gdzie postęp, gdzie stój' }));
    if (!sum.hasHistory) {
      movedBox.appendChild(U.el('p', { class: 'muted', text:
        'Porównanie pokrycia wymaga migawki z początku tygodnia — pierwsza powstaje przy '
        + 'pierwszym wejściu na ten ekran albo na mapę drogi. Za tydzień będzie co porównywać.' }));
    } else if (!sum.moved.length && !sum.stuck.length) {
      movedBox.appendChild(U.el('p', { class: 'muted', text: 'Pokrycie nie zmieniło się w żadnej kategorii.' }));
    } else {
      if (sum.moved.length) {
        movedBox.appendChild(U.el('h3', { text: 'Urosło' }));
        var up = U.el('div', { class: 'list' });
        sum.moved.slice(0, 4).forEach(function (d) {
          var row = U.el('div', { class: 'row static' });
          row.appendChild(U.el('div', { class: 'row-main' }, [
            U.el('b', { text: d.name }),
            U.el('p', { class: 'muted', text: Math.round(d.was * 100) + '% → '
              + Math.round(d.now * 100) + '% (+' + (Math.abs(d.delta) * 100).toFixed(1).replace('.', ',') + ' punktu)' })
          ]));
          up.appendChild(row);
        });
        movedBox.appendChild(up);
      }
      if (sum.stuck.length) {
        movedBox.appendChild(U.el('h3', { text: 'Stoi' }));
        var down = U.el('div', { class: 'list' });
        sum.stuck.forEach(function (d) {
          var row = U.el('div', { class: 'row static' });
          row.appendChild(U.el('div', { class: 'row-main' }, [
            U.el('b', { text: d.name }),
            U.el('p', { class: 'muted', text: 'bez zmiany, pokrycie ' + Math.round(d.now * 100) + '%' })
          ]));
          down.appendChild(row);
        });
        movedBox.appendChild(down);
      }
    }

    /* --- co zrobione, dzień po dniu --- */
    daysBox.appendChild(U.el('h2', { text: 'Co zrobione' }));
    daysBox.appendChild(U.el('p', { class: 'muted', text:
      now.lessons + ' ' + U.plural(now.lessons, 'lekcja', 'lekcje', 'lekcji') + ' · '
      + now.answers + ' ' + U.plural(now.answers, 'odpowiedź', 'odpowiedzi', 'odpowiedzi') + ' · '
      + now.newWords + ' ' + U.plural(now.newWords, 'nowe hasło', 'nowe hasła', 'nowych haseł') }));

    var cmp = sum.compare;
    daysBox.appendChild(U.el('p', { class: 'muted', text:
      'Wobec poprzedniego tygodnia: ' + signed(cmp.minutes) + ' min, '
      + signed(cmp.activeDays) + ' ' + U.plural(Math.abs(cmp.activeDays), 'dzień', 'dni', 'dni') + ', '
      + signed(cmp.lessons) + ' ' + U.plural(Math.abs(cmp.lessons), 'lekcja', 'lekcje', 'lekcji')
      + (cmp.accuracy === null ? '' : ', skuteczność ' + signed(cmp.accuracy) + ' punktu') + '.' }));

    var table = U.el('table', { class: 'data-table' });
    var thead = U.el('thead');
    thead.appendChild(U.el('tr', {}, [
      U.el('th', { scope: 'col', text: 'Dzień' }),
      U.el('th', { scope: 'col', text: 'Minuty' }),
      U.el('th', { scope: 'col', text: 'Odpowiedzi' }),
      U.el('th', { scope: 'col', text: 'Nowe hasła' })
    ]));
    table.appendChild(thead);
    var tbody = U.el('tbody');
    now.days.forEach(function (d) {
      var tr = U.el('tr');
      tr.appendChild(U.el('th', { scope: 'row', text: U.dateWords(d.date) }));
      if (d.future) {
        tr.appendChild(U.el('td', { text: '—' }));
        tr.appendChild(U.el('td', { text: '—' }));
        tr.appendChild(U.el('td', { text: '—' }));
      } else {
        tr.appendChild(U.el('td', { text: String(Math.round(d.stats.minutes || 0)) }));
        tr.appendChild(U.el('td', { text: String(d.stats.answers || 0) }));
        tr.appendChild(U.el('td', { text: String(d.stats.newWords || 0) }));
      }
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    daysBox.appendChild(table);

    /* --- historia sesji --- */
    histBox.appendChild(U.el('h2', { text: 'Historia sesji dnia' }));
    var log = Session.log().slice(-10).reverse();
    if (!log.length) {
      histBox.appendChild(U.el('p', { class: 'muted', text: 'Nie ma jeszcze żadnej zakończonej sesji.' }));
      var go2 = U.el('button', { class: 'btn', type: 'button', text: 'Uruchom sesję dnia' });
      go2.addEventListener('click', function () { App.go('session'); });
      histBox.appendChild(U.el('div', { class: 'btn-row' }, [go2]));
      return;
    }
    var hist = U.el('div', { class: 'list' });
    log.forEach(function (e) {
      var kinds = Object.keys(e.blocks || {}).map(function (k) {
        return (Session.LABELS[k] || k) + ' ' + e.blocks[k].done + '/' + e.blocks[k].steps;
      }).join(' · ');
      var row = U.el('div', { class: 'row static' });
      row.appendChild(U.el('div', { class: 'row-main' }, [
        U.el('b', { text: U.dateWords(e.d) + ' — ' + Math.round(e.spent / 60) + ' min z ' + e.minutes }),
        U.el('p', { class: 'muted', text: kinds || 'brak bloków' })
      ]));
      hist.appendChild(row);
    });
    histBox.appendChild(hist);
  };

  function signed(n) {
    if (n > 0) return '+' + n;
    return String(n);
  }

  /* =========================================== EKRAN: SŁOWNIK I ZWROTY

     Do sesji V były to DWA ekrany. „Zwroty” nie miały jednak własnych danych
     ani własnego ćwiczenia — był to filtr nad tym samym DB.index, którym żyje
     Słownik: odrzuć `type === 'word'`, zostaw `frequency >= 3`, posortuj po
     częstości, pokaż sześćdziesiąt pozycji jako duże karty. Wszystkie te
     ustawienia Słownik potrafił już ustawić sam, tyle że ręcznie i w czterech
     kontrolkach.

     Dwie nazwy nad jednym zbiorem danych to najgorszy rodzaj duplikatu: nie
     widać go w kodzie (moduły są osobne), a widać w głowie uczącego się, który
     szuka „sà-wàt-dii” raz tu, raz tam i za każdym razem dostaje inny wycinek
     bazy bez wyjaśnienia, dlaczego.

     Dlatego został jeden ekran z rzędem gotowych ustawień. Nic nie znikło:
     „Zwroty” i „Tryb wyjazdowy” są teraz zestawami filtrów, a widok kartowy —
     przełącznikiem prezentacji, nie osobnym adresem. Wyjazdowy nadal zawęża
     do ośmiu kategorii i podnosi próg częstości do 4, bo w podróży liczy się
     to, co padnie na pewno, a nie to, co ładnie wygląda na liście. */

  var TRAVEL = ['Podstawy i grzeczność', 'Lotnisko i podróż', 'Transport', 'Hotel',
    'Restauracja', 'Awarie i pomoc', 'Zdrowie i apteka', 'Liczby i liczenie'];

  var PRESETS = {
    all:    { label: 'Cała baza', view: 'list',
              hint: 'Wszystkie hasła — słowa, zwroty i zdania.' },
    phrase: { label: 'Zwroty', view: 'cards',
              hint: 'Bez pojedynczych słów. Gotowe wypowiedzi, od najczęstszych.' },
    travel: { label: 'Tryb wyjazdowy', view: 'cards',
              hint: 'Osiem kategorii, które padają w podróży, i tylko te najczęstsze.' }
  };

  var dictState = { page: 1, perPage: 40, results: [], preset: 'all' };

  /* Filtr zestawu nakładany PO wyszukiwarce. Zestaw zawęża pulę, wpisany tekst
     nadal działa — inaczej „Zwroty” byłyby ślepą uliczką, z której nie da się
     nic wyszukać. */
  function presetFilter(r) {
    if (dictState.preset === 'all') return true;
    if (r.type === 'word') return false;
    if (dictState.preset === 'travel') {
      return TRAVEL.indexOf(r.category) !== -1 && r.frequency >= 4;
    }
    return r.frequency >= 3;
  }

  function phraseCard(stub) {
    var source = DB.any(stub.id);
    var r = G.view(source);
    var card = U.el('div', { class: 'bigcard' });
    card.appendChild(U.el('div', { class: 'bc-pl', text: r.polish }));
    card.appendChild(U.renderPhonetic(r.thaiPhonetic, { hideTones: App.settings.hideTones }));
    card.appendChild(U.el('p', { class: 'muted', text: 'Czytaj: ' + r.pronunciationPolish }));
    var open = U.el('button', { class: 'btn ghost', type: 'button', text: 'Szczegóły' });
    open.addEventListener('click', function () { App.openRecord(source.id); });
    card.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(r, 'Posłuchaj'), open]));
    return card;
  }

  function runSearch(reset) {
    if (reset) dictState.page = 1;
    var preset = PRESETS[dictState.preset] || PRESETS.all;
    dictState.results = Search.query({
      query: U.$('#dict-q').value,
      level: U.$('#f-level').value,
      category: U.$('#f-cat').value,
      type: U.$('#f-type').value,
      /* W zestawach zwrotowych sortowanie po częstości jest sednem, nie ozdobą:
         zwrot rzadki jest w podróży bezużyteczny, choćby był ciekawy. */
      sort: preset.view === 'cards' ? 'freq' : U.$('#f-sort').value,
      favouritesOnly: U.$('#f-fav').getAttribute('aria-pressed') === 'true',
      favourites: Progress.data.favourites
    }).filter(presetFilter);

    var total = dictState.results.length;
    U.$('#dict-count').textContent = total
      ? 'Znaleziono ' + total + ' ' + U.plural(total, 'hasło', 'hasła', 'haseł')
        + (dictState.preset === 'all' ? '.' : ' w zestawie „' + preset.label + '”.')
      : 'Brak wyników. Spróbuj innego słowa lub zdejmij filtry.';

    var box = U.clear(U.$('#dict-results'));
    box.className = preset.view === 'cards' ? 'bigcards' : 'list';
    var slice = dictState.results.slice(0, dictState.page * dictState.perPage);
    slice.forEach(function (r) {
      box.appendChild(preset.view === 'cards' ? phraseCard(r) : recordRow(r));
    });
    U.$('#dict-more').hidden = slice.length >= total;

    /* Sortowanie ustawione na sztywno musi być widoczne jako wyłączone —
       kontrolka, która nic nie robi, ale wygląda na czynną, jest gorsza
       niż jej brak. */
    U.$('#f-sort').disabled = preset.view === 'cards';
  }

  App.dictPreset = function (id) {
    if (!PRESETS[id]) id = 'all';
    dictState.preset = id;
    U.$$('#dict-presets .chip').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-preset') === id));
    });
    U.$('#dict-preset-hint').textContent = PRESETS[id].hint;
    if (dictState.built) runSearch(true);
  };

  RENDER.dict = function () {
    /* Złożenie indeksu wyszukiwania odkładamy na moment wejścia do Słownika —
       przy starcie nie jest do niczego potrzebne. */
    Search.ensure();
    if (!dictState.built) {
      var lvl = U.$('#f-level'), cat = U.$('#f-cat'), typ = U.$('#f-type');
      DB.levels.forEach(function (l) { lvl.appendChild(U.el('option', { value: l, text: l })); });
      DB.catNames.forEach(function (c) { cat.appendChild(U.el('option', { value: c, text: c })); });
      var typeLabels = { word: 'słowa', phrase: 'zwroty', sentence: 'zdania' };
      DB.types.forEach(function (t) { typ.appendChild(U.el('option', { value: t, text: typeLabels[t] || t })); });
      dictState.built = true;
      runSearch(true);
    }
  };

  /* =================================================== EKRAN: GRAMATYKA */
  var grammarMode = 'map';

  function renderGrammar() {
    var box = U.clear(U.$('#grammar-area'));
    if (grammarMode === 'map') { renderGrammarMap(box); return; }
    if (grammarMode === 'guide') { Gram.renderParticleGuide(box); return; }
    var again = function () { renderGrammar(); };
    if (grammarMode === 'structure') { Gram.renderListening(box, again); return; }
    if (grammarMode === 'transform') { Gram.renderTransform(box, again); return; }
    Gram.renderParticles(box, again);
  }

  /* Mapa progresji. Pokazuje etap, temat, lekcję wejścia i to, czego temat
     dotyczy — a przy każdym temacie zdanie o tym, co robi tu źle Polak.
     Tematy jeszcze nieotwarte są widoczne, ale oznaczone: kolejność sama
     jest komunikatem i chowanie jej niczego nie uczy. */
  function renderGrammarMap(box) {
    var done = Progress.lessonsDone ? Progress.lessonsDone() : 0;
    var stages = {};
    DB.grammar.forEach(function (g) {
      (stages[g.stage] || (stages[g.stage] = [])).push(g);
    });
    var open = DB.grammar.filter(function (g) { return g.introducedAt <= done; });
    box.appendChild(U.el('p', { class: 'muted', text:
      'Otwartych tematów: ' + open.length + ' z ' + DB.grammar.length
      + '. Temat otwiera się w konkretnej lekcji i zostaje tematem kolejnych, '
      + 'aż wejdzie następny.' }));

    Object.keys(stages).sort(function (a, b) { return a - b; }).forEach(function (n) {
      var list = stages[n];
      var sec = U.el('div', { class: 'card sub' });
      sec.appendChild(U.el('h2', { text: 'Etap ' + n + ' — ' + list[0].stageTitle }));
      list.forEach(function (g) {
        var opened = g.introducedAt <= done;
        var row = U.el('div', { class: 'lesson-row' + (opened ? '' : ' locked') });
        var badge = U.el('span', { class: 'badge',
          'aria-label': opened ? 'temat otwarty' : 'temat jeszcze nieotwarty',
          text: opened ? '✓' : String(g.introducedAt) });
        row.appendChild(badge);
        var body = U.el('div');
        body.appendChild(U.el('h3', { text: g.title }));
        body.appendChild(U.el('p', { class: 'muted', text:
          'Lekcja ' + g.introducedAt + ' · ' + g.lessons + ' lekcji · '
          + g.patterns.length + ' przykładów · poziom ' + g.level }));
        if (opened) {
          body.appendChild(U.el('p', { text: g.explanation }));
          body.appendChild(U.el('p', { class: 'muted', text:
            'Pułapka dla Polaka: ' + g.contrast }));
          g.patterns.slice(0, 3).forEach(function (src) {
            var view = G.view(src);
            var line = U.el('div', { class: 'pattern' });
            var play = U.el('button', { class: 'btn ghost play-btn',
              type: 'button', 'aria-pressed': 'false',
              'aria-label': 'Posłuchaj: ' + view.polish });
            play.appendChild(U.icon('play'));
            play.addEventListener('click', function () {
              Player.play(view, { btn: play });
            });
            line.appendChild(U.el('span', { class: 'phonetic', text:
              App.settings.hideTones ? U.stripTones(view.thaiPhonetic)
                : view.thaiPhonetic }));
            line.appendChild(play);
            body.appendChild(line);
            body.appendChild(U.el('p', { class: 'muted', text: view.polish }));
          });
          if (g.tip) {
            body.appendChild(U.el('p', { class: 'muted', text:
              'Wskazówka: ' + g.tip }));
          }
        }
        row.appendChild(body);
        sec.appendChild(row);
      });
      box.appendChild(sec);
    });
  }

  RENDER.grammar = renderGrammar;

  /* ==================================================== EKRAN: SŁUCHANIE */
  RENDER.listen = function () { Quiz.renderListen(U.$('#listen-area')); };

  /* ===================================================== EKRAN: MÓWIENIE */
  RENDER.speak = function () {
    var box = U.$('#speak-area');
    Quiz.renderSpeak(box);
    /* Odnośnik do przewodnika. Do sesji V do ekranu „Tony i wymowa” nie
       prowadziło NIC poza menu — a jedyny moment, w którym człowiek chce
       przeczytać, czym różni się ton opadający od niskiego, to chwila, gdy
       właśnie mu ten ton nie wyszedł. Przewodnik ma być pod ręką tam, gdzie
       powstaje pytanie, a nie tylko na liście ekranów. */
    var help = U.el('button', { class: 'btn ghost', type: 'button',
      text: 'Nie wiem, jak brzmi ten ton — otwórz przewodnik' });
    help.addEventListener('click', function () { App.go('pron'); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [help]));
  };

  /* ====================================================== EKRAN: DIALOGI */
  /* Podpis roli razem z płcią, jeżeli wynika ze scenariusza. Rola opisana
     ogólnie (Turysta, Klient) podąża za ustawieniem użytkownika. */
  function roleCaption(dlg, key) {
    var name = dlg.roles[key];
    var g = (dlg.roleGender && dlg.roleGender[key]) || 'any';
    if (g === 'any') return name + ' (' + key + ', mówi ' + G.label() + ' — jak Ty)';
    return name + ' (' + key + ', ' + G.label(g) + ')';
  }

  function renderDialogue() {
    var sel = U.$('#dlg-select');
    var dlg = DB.get(sel.value) || DB.dialogues[0];
    if (!dlg) return;
    var box = U.clear(U.$('#dlg-view'));
    var hidePl = U.$('#dlg-hide').getAttribute('aria-pressed') === 'true';
    var roleOnly = U.$('#dlg-role').getAttribute('aria-pressed') === 'true';

    box.appendChild(U.el('h2', { text: dlg.title }));
    box.appendChild(U.el('p', { class: 'muted', text: roleCaption(dlg, 'A') + ' · ' + roleCaption(dlg, 'B') + ' · ' + dlg.level }));

    /* Kopie z zapisaną płcią mówiącego — odtwarzacz dobiera po niej głos
       roli, a oryginalnych rekordów nie wolno modyfikować. */
    var lines = G.viewAll(dlg.lines).map(function (line) {
      var copy = {};
      Object.keys(line).forEach(function (k) { copy[k] = line[k]; });
      copy.__speaker = G.speakerOf(line);
      return copy;
    });
    var all = U.el('button', { class: 'btn', type: 'button', text: 'Odtwórz cały dialog' });
    all.addEventListener('click', function () {
      Player.playSequence(lines, {
        btn: all,
        onstep: function (line) {
          U.$$('.line', box).forEach(function (n) { n.classList.remove('current'); });
          var node = U.$('[data-line="' + line.index + '"]', box);
          if (node) node.classList.add('current');
        },
        onend: function () { U.$$('.line', box).forEach(function (n) { n.classList.remove('current'); }); }
      });
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [all]));

    var wrap = U.el('div', { class: hidePl ? 'hide-pl' : '' });
    lines.forEach(function (line) {
      var row = U.el('div', { class: 'line' + (roleOnly && line.role !== 'A' ? ' dim' : ''), 'data-line': line.index });
      var speaker = G.speakerOf(line);
      var tag = U.el('span', { class: 'role' + (line.role === 'B' ? ' b' : ''), text: line.role });
      tag.setAttribute('data-gender', speaker);
      tag.setAttribute('title', 'Rola ' + line.role + ' — mówi ' + G.label(speaker));
      row.appendChild(tag);
      var mid = U.el('div');
      mid.appendChild(U.el('div', { class: 'l-ph', text: App.settings.hideTones ? U.stripTones(line.thaiPhonetic) : line.thaiPhonetic }));
      mid.appendChild(U.el('div', { class: 'l-pl', text: line.polish }));
      mid.appendChild(U.el('div', { class: 'row-meta muted', text: 'Czytaj: ' + line.pronunciationPolish }));
      var lineColl = colloquialRow(line);
      if (lineColl) mid.appendChild(lineColl);
      row.appendChild(mid);
      var b = U.el('button', { class: 'icon-btn', type: 'button', 'aria-label': 'Posłuchaj kwestii ' + line.index });
      b.appendChild(U.icon('play'));
      /* Rola i płeć trafiają do odtwarzacza: obie kwestie tym samym głosem
         zlewają się w monolog i scena przestaje być sceną. */
      b.addEventListener('click', function () {
        Player.play(line, { btn: b, role: line.role, gender: speaker });
      });
      row.appendChild(b);
      wrap.appendChild(row);
    });
    box.appendChild(wrap);
    if (dlg.notes) box.appendChild(U.el('p', { class: 'muted' }, [U.el('strong', { text: 'Wskazówka: ' }), document.createTextNode(dlg.notes)]));
  }

  RENDER.dialogues = function () {
    var sel = U.$('#dlg-select');
    if (!sel.options.length) {
      DB.dialogueIndex.forEach(function (d) {
        sel.appendChild(U.el('option', { value: d.id, text: d.title + ' (' + d.level + ')' }));
      });
    }
    renderDialogue();
  };

  /* ===================================================== EKRAN: POWTÓRKI */
  /* Rekord karty powtórki — z rozróżnieniem, którego brakowało.

     „DB.get(id) zwrócił null” ma dwie zupełnie różne przyczyny:
       a) hasło zniknęło z bazy przy aktualizacji danych — karta jest sierotą
          i trzeba ją skasować,
       b) plik z tym hasłem nie jest JESZCZE wczytany — karta jest w porządku,
          a my po prostu przyszliśmy za wcześnie.

     Do tej pory oba przypadki kończyły się skasowaniem karty. W praktyce
     przypadek (b) zdarza się przy każdym wejściu na ekran powtórek: pierwszy
     render idzie przed dociągnięciem plików, bo App.go woła RENDER, a dopiero
     potem ensureFullData. Na ekranie powtórek to zwykle nie wybuchało, bo
     pliki bywały już w pamięci z wcześniejszych ćwiczeń — ale sesja dnia
     zaczyna od powtórek zaraz po starcie i kasowała wtedy CAŁĄ kartotekę.

     Rozstrzyga o tym indeks: DB.any() zna każde hasło bazy, niezależnie od
     tego, czy jego plik jest wczytany. */
  function srsSource(cardId, onReady) {
    var rid = SRS.recordOf(cardId);
    var full = DB.get(rid);
    if (full) return full;
    if (!DB.any(rid)) { SRS.remove(cardId); return null; }   /* hasła nie ma w bazie */
    DB.ensureFor([rid]).then(function () { onReady && onReady(); });
    return undefined;                                        /* jeszcze się wczytuje */
  }

  function renderSRS() {
    var box = U.clear(U.$('#srs-area'));
    var stats = SRS.stats();

    /* Kolejka pokazywana uczącemu się to PLAN, nie surowa lista zaległych.
       Po dwutygodniowej przerwie przy trzech tysiącach haseł surowa lista ma
       kilkaset pozycji i jedyne, co robi, to zniechęca. Plan ma sufit wzięty
       z tego, ile ten uczący się faktycznie robi dziennie, a resztę rozkłada
       na kolejne dni — od najpilniejszych. */
    var plan = SRS.plan();
    if (plan.backlog > plan.cap) {
      /* Zaległości większe niż jeszcze jeden dzień pracy przepisujemy na
         kolejne dni na stałe, żeby licznik „na dziś” nie kłamał jutro. */
      SRS.spreadBacklog();
      plan = SRS.plan();
    }

    var statRow = U.clear(U.$('#srs-stats'));
    statRow.appendChild(statBox(plan.today.length, 'na dziś'));
    statRow.appendChild(statBox(stats.total, 'kart w nauce'));
    statRow.appendChild(statBox(stats.learned, 'utrwalonych'));
    statRow.appendChild(statBox(stats.tomorrow, 'na jutro'));

    var queue = plan.today;
    if (!queue.length) {
      box.appendChild(U.el('h2', { text: 'Na dziś gotowe' }));
      box.appendChild(U.el('p', { class: 'muted', text: 'Nie masz zaległych powtórek. Możesz dołożyć nowe hasła do nauki.' }));
      var add = U.el('button', { class: 'btn', type: 'button', text: 'Dodaj 10 nowych haseł' });
      add.addEventListener('click', function () {
        var fresh = SRS.suggestNew(10, App.settings.practiceLevel);
        fresh.forEach(function (r) { SRS.addBoth(r.id); });
        U.toast('Dodano ' + fresh.length + ' ' + U.plural(fresh.length, 'hasło', 'hasła', 'haseł')
          + ' — każde jako rozpoznanie i wytworzenie.');
        renderSRS();
      });
      box.appendChild(U.el('div', { class: 'btn-row' }, [add]));
      renderTroubles();
      return;
    }

    var card = queue[0];

    /* Karta kontrastu percepcyjnego wygląda inaczej niż karta hasła, bo pyta
       o co innego: nie „co to znaczy”, tylko „czy słyszysz różnicę”. Materiał
       bierze z Modułu 0 — losowe zadanie dotyczące tego kontrastu. */
    if (SRS.isContrastCard(card.id)) {
      renderContrastCard(box, card, queue.length);
      renderTroubles();
      return;
    }

    var side = SRS.sideOf(card.id);
    var source = srsSource(card.id, function () {
      if (App.screen === 'srs') renderSRS();
    });
    if (source === null) { renderSRS(); return; }
    if (source === undefined) {
      box.appendChild(U.el('p', { class: 'muted', role: 'status', text: 'Wczytuję hasło…' }));
      renderTroubles();
      return;
    }
    var rec = G.view(source);

    box.appendChild(queueLine(plan));

    if (side === 'w') { renderPronCard(box, card, rec, source); renderTroubles(); return; }

    /* Strona karty decyduje, co jest pytaniem, a co odpowiedzią. To jest cały
       sens rozdzielenia: „rozpoznaję ฟ้าร้อง” i „umiem powiedzieć »grzmot«
       po tajsku” to dwie różne umiejętności i nie wolno ich pytać tym samym
       pytaniem. */
    var receptive = side === 'r';
    box.appendChild(U.el('p', { class: 'm0-kind muted',
      text: SRS.sideName(side) + ' · ' + SRS.SIDE_LONG[side] }));

    var answer = U.el('div', { hidden: 'hidden' });
    if (receptive) {
      /* Pytamy tajskim, odpowiedzią jest znaczenie. */
      box.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: App.settings.hideTones }));
      answer.appendChild(U.el('p', { class: 'bc-pl', text: rec.polish }));
      answer.appendChild(U.el('p', { class: 'muted', text: rec.toneGuide }));
    } else {
      /* Pytamy znaczeniem, odpowiedzią jest tajski. */
      box.appendChild(U.el('p', { class: 'bc-pl', text: rec.polish }));
      answer.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: App.settings.hideTones }));
      answer.appendChild(U.el('p', { class: 'muted', text: 'Czytaj: ' + rec.pronunciationPolish }));
      answer.appendChild(U.el('p', { class: 'muted', text: rec.toneGuide }));
    }
    box.appendChild(answer);

    var show = U.el('button', { class: 'btn', type: 'button',
      text: receptive ? 'Pokaż znaczenie' : 'Pokaż odpowiedź' });
    var grades = U.el('div', { class: 'btn-row', hidden: 'hidden' });
    show.addEventListener('click', function () {
      answer.hidden = false;
      show.hidden = true;
      grades.hidden = false;
      Player.play(rec);
    });
    var head = [show];
    /* Przy stronie produktywnej podpowiedź dźwiękowa przed odpowiedzią byłaby
       podaniem rozwiązania — przycisk „Posłuchaj” pojawia się dopiero po niej. */
    if (receptive) head.push(Player.button(rec, 'Posłuchaj'));
    box.appendChild(U.el('div', { class: 'btn-row' }, head));

    [['Nie pamiętam', 0], ['Trudne', 3], ['Dobrze', 4], ['Łatwe', 5]].forEach(function (g) {
      var b = U.el('button', { class: g[1] >= 4 ? 'btn' : 'btn ghost', type: 'button', text: g[0] });
      b.addEventListener('click', function () {
        SRS.grade(source.id, g[1], { side: side });
        Progress.answer(source.id, g[1] >= 3, { mode: receptive ? 'srs-rec' : 'srs-prod' });
        renderSRS();
      });
      grades.appendChild(b);
    });
    box.appendChild(grades);
    renderTroubles();
  }

  /* Wiersz nad kartą: ile zostało dziś i co się stało z resztą. Uczący się ma
     wiedzieć, że zaległości nie zniknęły — tylko że nie musi ich robić dziś. */
  function queueLine(plan) {
    var wrap = U.el('div', { class: 'srs-queue' });
    wrap.appendChild(U.el('p', { class: 'muted', text: 'Pozostało dziś: ' + plan.today.length }));
    if (plan.backlog) {
      wrap.appendChild(U.el('p', { class: 'muted', text:
        'Zaległych kart: ' + plan.dueTotal + '. Rozłożyłem je na ' + plan.days + ' '
        + U.plural(plan.days, 'dzień', 'dni', 'dni')
        + ' po ' + plan.cap + ' — najpierw hasła najczęstsze i najbliższe zapomnienia.' }));
    }
    return wrap;
  }

  /* Karta wymowy. Hasło jest tu rozpoznawane i wytwarzane bez zarzutu —
     problemem jest sam kontur tonalny, więc jedyne sensowne pytanie brzmi
     „powiedz to”, a oceny nie stawia uczący się, tylko analiza nagrania. */
  function renderPronCard(box, card, rec, source) {
    box.appendChild(U.el('p', { class: 'm0-kind muted', text: 'wymowa · powiedz na głos' }));
    box.appendChild(U.el('p', { class: 'bc-pl', text: rec.polish }));
    box.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: false }));

    if (card.tone && card.tone.expected) {
      var hint = U.el('div', { class: 'fb bad' });
      hint.appendChild(U.el('strong', { text: 'Ostatnio: ' }));
      hint.appendChild(document.createTextNode(
        'sylaba „' + card.tone.syllable + '” wyszła tonem ' + card.tone.produced
        + ', a ma być ' + card.tone.expected + '.'
        + (card.tone.fix ? ' ' + card.tone.fix : '')));
      box.appendChild(hint);
    }

    box.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(rec, 'Posłuchaj wzorca')]));

    var area = U.el('div', { class: 'pron-area' });
    box.appendChild(area);

    /* Ocena wymowy potrzebuje mikrofonu. Bez niego nie udajemy, że karta
       została zrobiona — zostawiamy ją na kolejny raz i mówimy dlaczego.
       PronView sam wyświetla powód (brak zgody, brak https, brak obsługi),
       więc tutaj dokładamy tylko wyjście awaryjne. */
    var promptAt = Date.now();
    area.appendChild(PronView.control(source, {
      promptAt: promptAt,
      label: 'Nagraj i oceń ton',
      onResult: function (result) {
        if (!result) return;
        var note = SRS.notePronunciation(source.id, result);
        var clean = !!(result.ok && (result.syllables || []).every(function (s) { return s.ok; }));
        Progress.answer(source.id, clean, { mode: 'srs-pron' });
        if (note && note.action === 'closed') {
          U.toast('Trzy czyste podejścia — karta wymowy zamknięta.');
        }
        var next = U.el('button', { class: 'btn', type: 'button', text: 'Następna karta' });
        next.addEventListener('click', renderSRS);
        area.appendChild(U.el('div', { class: 'btn-row' }, [next]));
        next.focus();
      }
    }));

    if (!PronView.canRecord()) {
      var skip = U.el('button', { class: 'btn ghost', type: 'button', text: 'Odłóż na jutro' });
      skip.addEventListener('click', function () {
        card.due = SRS.addDays(U.today(), 1);
        SRS.save();
        renderSRS();
      });
      box.appendChild(U.el('div', { class: 'btn-row' }, [skip]));
    }
  }

  /* Powtórka kontrastu percepcyjnego. Odpowiedź jest binarna (trafił / nie
     trafił), więc ocena SM-2 wychodzi z samego zadania, a nie z samooceny —
     przy słyszeniu „wydawało mi się, że łatwe” nic nie znaczy. */
  function renderContrastCard(box, card, left) {
    var cid = SRS.contrastOf(card.id);
    if (!global.Perception || !Perception.ready()) {
      SRS.remove(card.id); renderSRS(); return;
    }
    var task = Perception.drillFor(cid);
    if (!task) { SRS.remove(card.id); renderSRS(); return; }

    box.appendChild(U.el('p', { class: 'muted', text: 'Pozostało: ' + left }));
    box.appendChild(U.el('p', { class: 'm0-kind muted', text: 'Powtórka słuchowa' }));
    box.appendChild(U.el('p', { class: 'bc-pl', text: Perception.contrastLabel(cid) }));
    var c = Perception.contrast(cid);
    if (c) box.appendChild(U.el('p', { class: 'muted', text: c.note }));

    var area = U.el('div', { class: 'm0-task' });
    box.appendChild(area);

    M0View.renderDrill(area, task, function (ok) {
      SRS.grade(card.id, ok ? 4 : 0);
      Progress.perceptionAnswer(cid, ok);
    }, function () { renderSRS(); });
  }

  function renderTroubles() {
    var box = U.clear(U.$('#srs-history'));
    box.appendChild(U.el('h2', { text: 'Nad czym popracować' }));
    var trouble = SRS.troubles(8);
    if (!trouble.length) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Nie masz jeszcze powtarzających się błędów.' }));
      return;
    }
    var list = U.el('div', { class: 'list' });
    trouble.forEach(function (c) {
      if (SRS.isContrastCard(c.id)) {
        var cid = SRS.contrastOf(c.id);
        var row = U.el('div', { class: 'row' });
        row.appendChild(U.el('div', { class: 'row-main' }, [
          U.el('div', { class: 'row-pl', text: Perception.ready()
            ? Perception.contrastLabel(cid) : cid }),
          U.el('div', { class: 'row-meta', text:
            'kontrast słuchowy · pomyłki: ' + c.lapses + ' · powtórki: ' + c.seen })
        ]));
        list.appendChild(row);
        return;
      }
      var rec = DB.get(SRS.recordOf(c.id));
      if (!rec) return;
      var row2 = recordRow(rec);
      U.$('.row-meta', row2).textContent = SRS.sideName(SRS.sideOf(c.id))
        + ' · pomyłki: ' + c.lapses + ' · powtórki: ' + c.seen;
      list.appendChild(row2);
    });
    box.appendChild(list);
  }

  /* ============================================ EKRAN: SESJA NAPRAWCZA */

  /* Zestaw budowany na ekranie Postęp trafia tutaj. Sesja prowadzi hasło po
     haśle — nie losuje z puli, bo cała jej wartość polega na tym, że pyta
     dokładnie o to, na czym uczący się poległ. */
  function startRepair(set) {
    Repair.start(set);
    App.go('repair');
  }
  App.startRepair = startRepair;

  RENDER.repair = function () {
    var box = U.clear(U.$('#repair-area'));
    var set = Repair.set;

    if (!set) {
      box.appendChild(U.el('h2', { text: 'Nie ma czego naprawiać' }));
      box.appendChild(U.el('p', { class: 'muted', text:
        'Sesję naprawczą uruchamia się z ekranu Postęp — buduje się ją z haseł, '
        + 'na których faktycznie się pomyliłeś.' }));
      var back = U.el('button', { class: 'btn', type: 'button', text: 'Przejdź do Postępu' });
      back.addEventListener('click', function () { App.go('progress'); });
      box.appendChild(U.el('div', { class: 'btn-row' }, [back]));
      U.clear(U.$('#repair-stats'));
      return;
    }

    var statRow = U.clear(U.$('#repair-stats'));
    statRow.appendChild(statBox(set.ids.length, 'haseł w zestawie'));
    statRow.appendChild(statBox(Math.min(Repair.index + 1, set.ids.length), 'bieżące'));
    statRow.appendChild(statBox(set.pool, 'pomyłek w obszarze'));

    if (Repair.done()) { renderRepairSummary(box); return; }

    /* Hasła zestawu pochodzą z różnych poziomów — dociągamy dokładnie te pliki,
       których trzeba, zanim pokażemy pierwsze pytanie. */
    Repair.ensureData(set).then(function () {
      if (App.screen !== 'repair' || Repair.done()) return;
      var rec = Repair.current();
      if (!rec || rec.__stub) {
        /* Rekordu nie ma w bazie (usunięty przy aktualizacji danych) —
           pomijamy go zamiast przerywać sesję. */
        Repair.advance();
        RENDER.repair();
        return;
      }
      drawRepairItem(box, set, rec);
    });
  };

  function drawRepairItem(box, set, rec) {
    U.clear(box);
    box.appendChild(U.el('p', { class: 'm0-kind muted',
      text: set.label + ' · hasło ' + (Repair.index + 1) + ' z ' + set.ids.length }));
    box.appendChild(U.el('p', { class: 'muted', text: set.why }));

    var area = U.el('div', { class: 'repair-task' });
    box.appendChild(area);

    function done(ok) {
      Repair.note(rec.id, ok);
      var next = U.el('button', { class: 'btn', type: 'button',
        text: Repair.index + 1 < set.ids.length ? 'Następne hasło' : 'Podsumowanie' });
      next.addEventListener('click', function () {
        Repair.advance();
        RENDER.repair();
      });
      box.appendChild(U.el('div', { class: 'btn-row' }, [next]));
      next.focus();
    }

    /* Ćwiczenia produkcyjne i receptywne mają własne renderery przyjmujące
       wymuszony rekord — korzystamy z nich, zamiast pisać trzeci wariant
       tych samych ekranów. */
    if (set.screen === 'produce') {
      Produce.mode = set.mode;
      Produce.onAnswer = function (id, ok) { Produce.onAnswer = null; done(ok); };
      Produce.renderOne(area, rec, function () {});
    } else {
      Quiz.mode = set.mode;
      Quiz.onAnswer = function (id, ok) { Quiz.onAnswer = null; done(ok); };
      Quiz.renderOne(area, rec, function () {});
    }
  }

  function renderRepairSummary(box) {
    var s = Repair.summary();
    box.appendChild(U.el('h2', { text: 'Sesja naprawcza zakończona' }));
    box.appendChild(U.el('p', { class: 'bc-pl', text: s.ok + ' / ' + s.total + ' (' + s.rate + '%)' }));

    if (!s.stillWrong.length) {
      box.appendChild(U.el('p', { text:
        'Wszystkie hasła z zestawu poszły dobrze. Wróciły też do powtórek z nowymi odstępami.' }));
    } else {
      box.appendChild(U.el('p', { text:
        s.stillWrong.length + ' ' + U.plural(s.stillWrong.length, 'hasło nadal sprawia', 'hasła nadal sprawiają',
          'haseł nadal sprawia') + ' kłopot. Zostały w powtórkach z krótkim odstępem — '
        + 'wrócą same w ciągu paru dni.' }));
      var list = U.el('div', { class: 'list' });
      s.stillWrong.forEach(function (id) {
        var rec = DB.any(id);
        if (rec) list.appendChild(recordRow(rec));
      });
      box.appendChild(list);
    }

    var again = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wróć do Postępu' });
    again.addEventListener('click', function () { Repair.set = null; App.go('progress'); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [again]));
  }

  /* ======================================================= EKRAN: SCENY */
  RENDER.scenes = function () { Scenes.render(U.$('#scenes-area')); };

  /* ======================================== EKRAN: SŁUCHANIE EKSTENSYWNE */
  RENDER.extensive = function () { Extensive.render(U.$('#extensive-area')); };

  RENDER.srs = renderSRS;

  /* ======================================================= EKRAN: WYMOWA */
  RENDER.pron = function () {
    var p = DB.pronunciation;
    var box = U.clear(U.$('#pron-content'));
    if (!p) return;

    var intro = U.el('div', { class: 'card' });
    intro.appendChild(U.el('h2', { text: 'Jak czytać ten kurs' }));
    intro.appendChild(U.el('p', { text: p.intro }));
    box.appendChild(intro);
    box.appendChild(genderLesson());

    var tones = U.el('div', { class: 'card' });
    tones.appendChild(U.el('h2', { text: 'Pięć tonów' }));
    p.tones.forEach(function (t) {
      var item = U.el('div', { class: 'bigcard' });
      item.appendChild(U.el('div', { class: 'bc-pl', text: t.symbol + ' — ' + t.name }));
      item.appendChild(U.el('p', { text: t.description }));
      var tex = G.view(t.example);
      markLexicon(item, tex);
      item.appendChild(U.renderPhonetic(tex.thaiPhonetic, {}));
      item.appendChild(U.el('p', { class: 'muted', text: 'przykład: ' + tex.polish }));
      item.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(tex, 'Posłuchaj')]));
      tones.appendChild(item);
    });
    box.appendChild(tones);

    var mp = U.el('div', { class: 'card' });
    mp.appendChild(U.el('h2', { text: 'Pary minimalne' }));
    mp.appendChild(U.el('p', { class: 'muted', text: 'Te słowa różnią się tylko tonem lub długością samogłoski.' }));
    p.minimalPairs.forEach(function (pair) {
      var item = U.el('div', { class: 'bigcard' });
      item.appendChild(U.el('div', { class: 'bc-pl', text: pair.focus }));
      pair.items.forEach(function (raw) {
        var it = G.view(raw);
        var line = markLexicon(U.el('div', { class: 'row' }), it);
        var main = U.el('div', { class: 'row-main' });
        main.appendChild(U.renderPhonetic(it.thaiPhonetic, {}));
        main.appendChild(U.el('div', { class: 'row-meta', text: it.polish }));
        line.appendChild(main);
        var b = U.el('button', { class: 'icon-btn', type: 'button', 'aria-label': 'Posłuchaj: ' + it.polish });
        b.appendChild(U.icon('play'));
        b.addEventListener('click', function () { Player.play(it, { btn: b }); });
        line.appendChild(b);
        item.appendChild(line);
      });
      if (pair.tip) item.appendChild(U.el('p', { class: 'muted', text: pair.tip }));
      mp.appendChild(item);
    });
    box.appendChild(mp);

    var notes = U.el('div', { class: 'card' });
    notes.appendChild(U.el('h2', { text: 'Spółgłoski i samogłoski' }));
    p.consonantNotes.concat(p.vowelNotes).forEach(function (n) {
      notes.appendChild(U.el('h3', { text: n.title }));
      notes.appendChild(U.el('p', { text: n.text }));
    });
    box.appendChild(notes);

    var mistakes = U.el('div', { class: 'card' });
    mistakes.appendChild(U.el('h2', { text: 'Typowe błędy Polaków' }));
    p.polishMistakes.forEach(function (m) {
      mistakes.appendChild(U.el('h3', { text: m.title }));
      mistakes.appendChild(U.el('p', { text: m.text }));
    });
    box.appendChild(mistakes);

    var ex = U.el('div', { class: 'card' });
    ex.appendChild(U.el('h2', { text: 'Ćwiczenia' }));
    p.exercises.forEach(function (e) { ex.appendChild(exerciseBlock(e)); });
    box.appendChild(ex);

    var gram = U.el('div', { class: 'card' });
    gram.appendChild(U.el('h2', { text: 'Gramatyka w pigułce' }));
    DB.grammar.forEach(function (g) {
      var det = U.el('details');
      det.appendChild(U.el('summary', { text: g.title + ' (' + g.level + ')' }));
      det.appendChild(U.el('p', { text: g.explanation }));
      (g.patterns || []).forEach(function (rawPat) {
        var pat = G.view(rawPat);
        var item = markLexicon(U.el('div', { class: 'bigcard' }), pat);
        item.appendChild(U.el('div', { class: 'bc-pl', text: pat.polish }));
        item.appendChild(U.renderPhonetic(pat.thaiPhonetic, { hideTones: App.settings.hideTones }));
        item.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(pat, 'Posłuchaj')]));
        det.appendChild(item);
      });
      if (g.tip) det.appendChild(U.el('p', { class: 'muted', text: g.tip }));
      gram.appendChild(det);
    });
    box.appendChild(gram);
  };

  /* Wyjaśnienie systemu cząstek i zaimków zależnych od płci. W polszczyźnie
     nie ma odpowiednika, więc warto to pokazać osobno, a nie w przypisie. */
  function genderLesson() {
    var card = U.el('div', { class: 'card gender-card' });
    card.appendChild(U.el('h2', { text: 'Płeć mówiącego: cząstki i zaimki' }));
    card.appendChild(U.el('p', { text:
      'W tajskim o formie wypowiedzi decyduje płeć osoby mówiącej, a nie płeć rozmówcy ani rodzaj gramatyczny słowa. ' +
      'Ta sama myśl brzmi inaczej w ustach kobiety i mężczyzny. Nie jest to grzecznościowy wybór ani styl — ' +
      'to obowiązek gramatyczny. Mężczyzna nie może powiedzieć khâ, kobieta nie może powiedzieć khráp.' }));

    var t1 = U.el('div', { class: 'bigcard' });
    t1.appendChild(U.el('div', { class: 'bc-pl', text: 'Cząstka grzecznościowa na końcu zdania' }));
    t1.appendChild(U.el('p', { text:
      'Mężczyzna kończy wypowiedź khráp — tak samo w zdaniu i w pytaniu. ' +
      'Kobieta ma dwie formy: khâ (ton opadający) w zdaniu oznajmującym oraz khá (ton wysoki) w pytaniu ' +
      'i po cząstce ná. Różnica jest tylko w tonie, więc łatwo ją przeoczyć — i łatwo się na niej potknąć.' }));
    card.appendChild(t1);

    var t2 = U.el('div', { class: 'bigcard' });
    t2.appendChild(U.el('div', { class: 'bc-pl', text: 'Zaimek „ja”' }));
    t2.appendChild(U.el('p', { text:
      'Mężczyzna mówi o sobie phǒm. Kobieta mówi chǎn w mowie codziennej, także uprzejmej, ' +
      'a dì-chǎn w rejestrze formalnym — w urzędzie, banku, rozmowie służbowej. ' +
      'dì-chǎn w rozmowie ze znajomym zabrzmi sztywno, chǎn w urzędzie — zbyt swobodnie.' }));
    card.appendChild(t2);

    var t3 = U.el('div', { class: 'bigcard' });
    t3.appendChild(U.el('div', { class: 'bc-pl', text: 'Ta sama wypowiedź w dwóch formach' }));
    var sample = (DB.records.length ? DB.records : DB.index).filter(function (r) {
      return G.hasVariant(r) && r.frequency >= 4 && U.syllables(r.thaiPhonetic).length <= 8;
    })[0];
    if (sample) {
      var pair = G.pair(sample);
      t3.appendChild(U.el('p', { class: 'muted', text: sample.polish }));
      t3.appendChild(genderFormRow('forma męska', pair.male));
      t3.appendChild(genderFormRow('forma żeńska', pair.female));
    }
    t3.appendChild(U.el('p', { class: 'muted', text:
      'Aplikacja pokazuje domyślnie formę zgodną z Twoim ustawieniem (teraz: ' + G.label() + '). ' +
      'Obie formy znajdziesz zawsze w szczegółach hasła, a rozpoznawanie ich ze słuchu ćwiczy tryb ' +
      '„Forma męska czy żeńska?” na ekranie Słuchanie.' }));
    card.appendChild(t3);

    var t4 = U.el('div', { class: 'bigcard' });
    t4.appendChild(U.el('div', { class: 'bc-pl', text: 'Czego nie zmienia płeć' }));
    t4.appendChild(U.el('p', { text:
      'Reszta zdania zostaje bez zmian — tajski nie odmienia czasowników ani rzeczowników przez rodzaj. ' +
      'Zmienia się końcówka grzecznościowa i zaimek pierwszej osoby. Zaimki „ty”, „on”, „ona” (khun, kháw) ' +
      'są wspólne dla obu płci, a kháw znaczy zarówno „on”, jak i „ona”.' }));
    card.appendChild(t4);
    return card;
  }

  function exerciseBlock(exercise) {
    var wrap = U.el('div', { class: 'bigcard' });
    wrap.appendChild(U.el('div', { class: 'bc-pl', text: exercise.title }));
    wrap.appendChild(U.el('p', { class: 'muted', text: exercise.instruction }));
    var area = U.el('div');
    wrap.appendChild(area);
    var i = 0;

    function optionLabel(o) {
      return o.thaiPhonetic + ' — ' + o.polish;
    }

    function step() {
      U.clear(area);
      if (i >= exercise.items.length) {
        area.appendChild(U.el('p', { class: 'muted', text: 'Zestaw ukończony.' }));
        var again = U.el('button', { class: 'btn ghost', type: 'button', text: 'Jeszcze raz' });
        again.addEventListener('click', function () { i = 0; step(); });
        area.appendChild(U.el('div', { class: 'btn-row' }, [again]));
        return;
      }
      /* Zestawy mają dwie postacie. Ćwiczenie tonów podaje gotową odpowiedź
         w polu `answer`, a pary minimalne i spółgłoski — listę `options`,
         z której jedna pozycja jest odtwarzana, a reszta służy za dystraktory.
         Wcześniej obsługiwana była tylko pierwsza postać, więc pary minimalne
         i spółgłoski renderowały przyciski bez treści i nie dało się ich
         zaliczyć. */
      var raw = exercise.items[i];
      var item, opts, answer;

      if (raw.options && raw.options.length) {
        var choices = U.shuffle(raw.options.slice());
        var target = choices[0];
        item = G.view(target);
        answer = optionLabel(target);
        opts = U.shuffle(raw.options.map(optionLabel));
        if (raw.focus) {
          area.appendChild(U.el('p', { class: 'muted', text: 'Różnica: ' + raw.focus }));
        }
      } else {
        item = G.view(raw);
        answer = raw.answer;
        opts = exercise.type === 'tone-recognition'
          ? ['ton średni', 'ton niski', 'ton opadający', 'ton wysoki', 'ton rosnący']
          : U.shuffle([raw.answer].concat(exercise.items
              .filter(function (x) { return x.answer && x.answer !== raw.answer; })
              .slice(0, 3).map(function (x) { return x.answer; })));
      }

      markLexicon(area, item);
      var play = Player.button(item, 'Odtwórz');
      area.appendChild(U.el('div', { class: 'btn-row' }, [play]));

      var done = false;
      opts.forEach(function (o) {
        var b = U.el('button', { class: 'opt', type: 'button', text: o, 'aria-label': 'Odpowiedź: ' + o });
        b.addEventListener('click', function () {
          if (done) return;
          done = true;
          var ok = o === answer;
          b.classList.add(ok ? 'correct' : 'wrong');
          if (!ok) {
            U.$$('.opt', area).forEach(function (n) {
              if (n.textContent === answer) n.classList.add('correct');
            });
          }
          area.appendChild(U.el('p', { class: ok ? 'fb ok' : 'fb bad', text: ok
            ? 'Dobrze!'
            : 'Poprawnie: ' + answer + ' (' + item.thaiPhonetic + ' — ' + item.polish + ')' }));
          var nb = U.el('button', { class: 'btn', type: 'button', text: 'Dalej' });
          nb.addEventListener('click', function () { i += 1; step(); });
          area.appendChild(U.el('div', { class: 'btn-row' }, [nb]));
          nb.focus();
        });
        area.appendChild(b);
      });
      Player.play(item, { btn: play });
    }
    step();
    return wrap;
  }

  /* Mapa drabiny tempa.

     Sedno: zaliczenie ćwiczenia przy 0,7x nie mówi nic o tym, czy uczący się
     zrozumie to samo w tempie rozmowy. Mapa pokazuje trzy kolumny obok siebie
     właśnie po to, żeby widać było, gdzie postęp się zatrzymał — bo prawie
     zawsze zatrzymuje się na 1,4x, a bez rozbicia wyglądałoby to jak ogólny
     sukces. */
  function renderTempoLadder() {
    var box = U.clear(U.$('#prog-tempo'));
    box.appendChild(U.el('h2', { text: 'Drabina tempa' }));
    var sum = Progress.tempoSummary();
    box.appendChild(U.el('p', { class: 'muted', text:
      'Każde ćwiczenie rozumienia liczy się osobno w trzech tempach: 0,7x '
      + '(dydaktyczne), 1,0x (naturalne) i 1,4x (potoczne). Zaliczone '
      + sum.passed + ' z ' + sum.total + ' pól.' }));

    var map = Progress.tempoMap();
    var touched = map.filter(function (r) { return r.touched; });
    if (!touched.length) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Jeszcze żadne ćwiczenie rozumienia nie ma wyniku. Zacznij od ekranu '
        + 'Słuchanie albo Sceny — tempo wybierzesz na miejscu.' }));
      return;
    }

    var table = U.el('table', { class: 'tempo-map' });
    var head = U.el('tr');
    head.appendChild(U.el('th', { scope: 'col', text: 'Ćwiczenie' }));
    Progress.tempoSteps().forEach(function (t) {
      head.appendChild(U.el('th', { scope: 'col', text: t.label }));
    });
    head.appendChild(U.el('th', { scope: 'col', text: 'Stoisz na' }));
    table.appendChild(head);

    map.forEach(function (row) {
      var tr = U.el('tr', { class: row.touched ? '' : 'untouched' });
      tr.appendChild(U.el('th', { scope: 'row', text: row.label }));
      row.steps.forEach(function (cell) {
        var td = U.el('td', { class: cell.passed ? 'pass' : cell.answers ? 'part' : 'none' });
        var text = cell.passed ? 'zaliczone'
          : cell.answers ? cell.correct + '/' + cell.answers
            + ' (' + Math.round(cell.share * 100) + '%)'
          : '—';
        td.appendChild(U.el('span', { text: text }));
        td.setAttribute('aria-label', row.label + ', tempo ' + cell.tempoLabel
          + ': ' + (cell.passed ? 'zaliczone'
            : cell.answers ? cell.correct + ' z ' + cell.answers + ' trafnych'
            : 'brak podejścia'));
        tr.appendChild(td);
      });
      tr.appendChild(U.el('td', { text: row.stuckAt
        ? Progress.tempoLabel(row.stuckAt) : 'nigdzie — komplet' }));
      table.appendChild(tr);
    });
    box.appendChild(table);
    box.appendChild(U.el('p', { class: 'muted', text:
      'Pole zalicza się po dziesięciu odpowiedziach z trafnością co najmniej '
      + '80 procent. Raz zdobyte zaliczenie zostaje.' }));

    /* Słuchanie ekstensywne — różnica między przejściem bez tekstu i po tekście. */
    var ext = Progress.extensiveSummary();
    if (ext.blocks) {
      box.appendChild(U.el('h3', { text: 'Słuchanie ekstensywne' }));
      box.appendChild(U.el('p', { text:
        'Bloki przerobione: ' + ext.blocks + '. Bez tekstu rozumiesz '
        + Math.round(ext.firstShare * 100) + ' procent, po tekście '
        + Math.round(ext.thirdShare * 100) + ' procent.' }));
      var delta = ext.thirdShare - ext.firstShare;
      box.appendChild(U.el('p', { class: 'muted', text: delta >= 0.25
        ? 'Duża różnica: słowa znasz, ale nie rozpoznajesz ich w mowie. '
          + 'To zadanie dla Modułu 0 i wolniejszego tempa, nie dla nowych haseł.'
        : delta <= 0.05
          ? 'Tekst niewiele zmienia — brakuje słownictwa, a nie słuchu.'
          : 'Różnica umiarkowana: słuch i słownictwo idą mniej więcej równo.' }));
    }
  }

  /* ======================================================= EKRAN: POSTĘP */
  RENDER.progress = function () {
    renderTempoLadder();
    renderCourseProgress();
    renderPerception();
    renderSides();
    renderGrammarStats();
    renderWeakArea();
    renderErrorTables();
    renderRetention();
    renderTuning();
    renderFluency();
    renderNumberStats();
    renderReflexStats();
    renderAnkiControls();

    var s = Progress.summary();
    var row = U.clear(U.$('#prog-stats'));
    row.appendChild(statBox(s.known, 'poznanych haseł'));
    row.appendChild(statBox(s.minutes, 'minut nauki'));
    row.appendChild(statBox(s.bestStreak, 'rekord serii'));
    row.appendChild(statBox(s.favourites, 'ulubionych'));

    var lvlBox = U.clear(U.$('#prog-levels'));
    lvlBox.appendChild(U.el('h2', { text: 'Poziomy' }));
    var levels = Progress.byLevel();
    Object.keys(levels).forEach(function (l) {
      var v = levels[l];
      var pct = v.total ? Math.round(v.seen / v.total * 100) : 0;
      lvlBox.appendChild(U.el('p', { class: 'muted', text: l + ': ' + v.seen + ' / ' + v.total + ' (' + pct + '%)' }));
      var bar = U.el('div', { class: 'progress' });
      bar.appendChild(U.el('i', { style: 'width:' + pct + '%' }));
      lvlBox.appendChild(bar);
    });

    var days = Progress.last14();
    var chart = U.el('div', { class: 'chart', 'aria-hidden': 'true' });
    var max = Math.max.apply(null, days.map(function (d) { return d.stats.answers; }).concat([1]));
    days.forEach(function (d) {
      var col = U.el('i', { style: 'height:' + Math.max(3, Math.round(d.stats.answers / max * 100)) + '%', title: d.date + ': ' + d.stats.answers });
      chart.appendChild(col);
    });
    lvlBox.appendChild(U.el('h3', { text: 'Ostatnie 14 dni' }));
    lvlBox.appendChild(chart);

    var catBox = U.clear(U.$('#prog-cats'));
    catBox.appendChild(U.el('h2', { text: 'Kategorie' }));
    var cats = Progress.byCategory();
    Object.keys(cats).sort(function (a, b) { return cats[b].seen - cats[a].seen; }).forEach(function (c) {
      var v = cats[c];
      var pct = v.total ? Math.round(v.seen / v.total * 100) : 0;
      catBox.appendChild(U.el('p', { class: 'muted', text: c + ': ' + v.seen + ' / ' + v.total + ' (' + pct + '%)' }));
      var bar = U.el('div', { class: 'progress' });
      bar.appendChild(U.el('i', { style: 'width:' + pct + '%' }));
      catBox.appendChild(bar);
    });
  };

  /* ============================================ EKRAN: TEST POZIOMUJĄCY */

  /* Test wyznacza poziom i lekcję, od której otwiera się kurs. Pokazujemy go
     raz, przy pierwszym uruchomieniu — potem tylko na życzenie. */
  RENDER.placement = function () {
    var box = U.clear(U.$('#placement-area'));

    if (!Placement.state || Placement.state.done) {
      var done = Progress.data.placement;
      box.appendChild(U.el('h2', { text: done ? 'Test poziomujący — powtórka' : 'Zanim zaczniesz' }));
      if (done) {
        box.appendChild(U.el('p', { class: 'muted', text:
          'Ostatni wynik: poziom ' + done.level + ', ' + done.score + ' z ' + done.total
          + ' trafnych odpowiedzi (' + done.date + ').' }));
      }
      box.appendChild(U.el('p', { text:
        'Test ma 28 pytań o rosnącej trudności. Sprawdza, ile już rozumiesz, i ustawia '
        + 'punkt wejścia w kurs — żebyś nie zaczynał od materiału, który znasz, ani nie '
        + 'trafił od razu na taki, do którego brakuje Ci podstaw.' }));
      box.appendChild(U.el('p', { class: 'muted', text:
        'Jeśli czegoś nie wiesz, wybierz cokolwiek — test skończy się sam, gdy pytania '
        + 'staną się wyraźnie za trudne. Wynik zmienisz w każdej chwili, powtarzając test.' }));

      var startBtn = U.el('button', { class: 'btn gold', type: 'button',
        text: done ? 'Powtórz test' : 'Zacznij test' });
      startBtn.addEventListener('click', function () {
        Placement.start();
        RENDER.placement();
      });
      var skipBtn = U.el('button', { class: 'btn ghost', type: 'button',
        text: done ? 'Wróć do kursu' : 'Pomiń — zacznę od zera' });
      skipBtn.addEventListener('click', function () {
        if (!Progress.data.placement) {
          Progress.setPlacement({ level: 'Survival', score: 0, total: 0,
            entryLesson: (DB.lessons[0] || {}).id || null });
        }
        App.go('course');
      });
      box.appendChild(U.el('div', { class: 'btn-row' }, [startBtn, skipBtn]));
      return;
    }

    var q = Placement.current();
    if (!q || Placement.shouldStop()) { showPlacementResult(box); return; }

    var total = Placement.state.questions.length;
    var at = Placement.state.at;
    box.appendChild(U.el('h2', { text: Placement.progressText() }));
    var bar = U.el('div', { class: 'progress' });
    bar.appendChild(U.el('i', { style: 'width:' + Math.round(at / total * 100) + '%' }));
    box.appendChild(bar);
    box.appendChild(U.el('p', { class: 'muted', text: 'Poziom pytania: ' + q.level }));

    box.appendChild(U.el('p', { class: 'muted', text: 'Co znaczy ta wypowiedź?' }));
    box.appendChild(U.renderPhonetic(q.prompt, { hideTones: App.settings.hideTones }));

    var play = U.el('button', { class: 'btn gold play-btn', type: 'button',
      'aria-pressed': 'false', 'aria-label': 'Posłuchaj wymowy' });
    play.appendChild(U.icon('play'));
    play.appendChild(U.el('span', { text: 'Posłuchaj' }));
    play.addEventListener('click', function () { Player.play(DB.any(q.id), { btn: play }); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [play]));

    var list = U.el('div');
    q.options.forEach(function (opt) {
      var btn = U.el('button', { class: 'opt', type: 'button', text: opt });
      btn.addEventListener('click', function () {
        if (btn.disabled) return;
        U.$$('.opt', list).forEach(function (b) { b.disabled = true; });
        var ok = Placement.answer(q, opt);
        btn.classList.add(ok ? 'correct' : 'wrong');
        if (!ok) {
          U.$$('.opt', list).forEach(function (b) {
            if (b.textContent === q.answer) b.classList.add('correct');
          });
        }
        setTimeout(function () {
          if (Placement.shouldStop()) showPlacementResult(U.clear(U.$('#placement-area')));
          else RENDER.placement();
        }, ok ? 380 : 1100);
      });
      list.appendChild(btn);
    });
    box.appendChild(list);
    U.$$('.opt', list)[0].focus();
  };

  function showPlacementResult(box) {
    var out = Placement.finish();
    box.appendChild(U.el('h2', { text: 'Twój poziom: ' + out.verdict.level }));
    box.appendChild(U.el('p', { class: 'muted', text:
      out.verdict.score + ' z ' + out.verdict.total + ' trafnych odpowiedzi.' }));

    var explain = {
      Survival: 'Zaczynasz od zera albo prawie od zera. Kurs otworzy się na pierwszej lekcji — od grzeczności, liczb i jedzenia.',
      A1: 'Rozumiesz podstawy ratunkowe. Kurs pominie materiał Survival i zacznie od budowania prostych zdań.',
      A2: 'Radzisz sobie z codziennymi sytuacjami. Kurs zacznie od poziomu A2 — dłuższe wypowiedzi i pytania.',
      B1: 'Rozumiesz rozbudowane wypowiedzi. Kurs zacznie od B1 — rejestr, niuanse, mowa zależna.',
      B2: 'Znasz język dobrze. Kurs otworzy się na materiale B2 — idiomy, rejestr formalny, język pracy.'
    }[out.verdict.level];
    box.appendChild(U.el('p', { text: explain }));

    if (out.entry) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Punkt wejścia: ' + out.entry.id.replace('lesson-', 'lekcja ') + ' — ' + out.entry.title }));
    }
    box.appendChild(U.el('p', { class: 'muted', text:
      'Poziom nauki w Powtórkach i ćwiczeniach ustawiliśmy na ' + out.verdict.level
      + '. Zmienisz go w Ustawieniach.' }));

    var go = U.el('button', { class: 'btn gold', type: 'button', text: 'Przejdź do kursu' });
    go.addEventListener('click', function () { App.go('course'); });
    var again = U.el('button', { class: 'btn ghost', type: 'button', text: 'Powtórz test' });
    again.addEventListener('click', function () { Placement.state = null; RENDER.placement(); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [go, again]));
    go.focus();
  }

  /* ========================================================= EKRAN: KURS */

  var courseState = { level: '' };

  /* ================================================= EKRAN: MODUŁ 0 */
  RENDER.module0 = function () { M0View.render(); };

  RENDER.exam = function () { ExamView.render(U.$('#exam-area')); };

  RENDER.checkpoint = function () {
    var box = U.$('#checkpoint-area');
    U.clear(box);
    Checkpoint.render(box);
  };

  /* ========================================================= LICZBY (sesja T)

     Ekran ma jeden wybór trybu i jedno pole zadania — ćwiczenie ma się zaczynać
     od razu po wejściu, bez kliknięcia. Przy pomiarze czasu reakcji każdy
     dodatkowy krok przed startem jest szumem w danych: uczący się, który
     najpierw czyta trzy akapity, a potem klika „zacznij”, ma już wtedy inny
     stan uwagi niż ten, któremu bodziec ruszył sam. */

  var numMode = 'dictation';

  RENDER.numbers = function () {
    var modes = U.clear(U.$('#numbers-modes'));
    var area = U.$('#numbers-area');
    if (!Numbers.loaded()) {
      U.clear(area).appendChild(U.el('p', { class: 'muted', text: 'Wczytuję moduł liczbowy…' }));
      U.clear(U.$('#numbers-map'));
      return;
    }
    Numbers.drills().forEach(function (d) {
      var chip = U.el('button', { class: 'chip', type: 'button',
        'aria-pressed': numMode === d.id ? 'true' : 'false', text: d.label });
      chip.addEventListener('click', function () { numMode = d.id; RENDER.numbers(); });
      modes.appendChild(chip);
    });
    nextNumberTask();
    renderNumberMap();
  };

  function nextNumberTask() {
    var area = U.clear(U.$('#numbers-area'));
    var fn = Numbers.RENDER[numMode];
    if (!fn) { area.appendChild(U.el('p', { class: 'muted', text: 'Nieznany tryb.' })); return; }
    fn(area, nextNumberTask);
  }

  /* Mapa modułu: gdzie liczby wchodzą na ścieżkę i co już opanowane.
     „Opanowane” znaczy tu co innego niż w słownictwie — mediana czasu reakcji
     poniżej progu, a nie sam odsetek trafień. */
  function renderNumberMap() {
    var box = U.clear(U.$('#numbers-map'));
    box.appendChild(U.el('h2', { text: 'Moduł liczbowy na ścieżce' }));
    box.appendChild(U.el('p', { class: 'muted', text:
      'Liczby nie stoją w jednym bloku. Podstawy wchodzą wcześnie, w Survivalu, '
      + 'a rozbudowa idzie stopniowo wzdłuż całego kursu — bo do zrobienia zakupów '
      + 'wystarczą cyfry i baht, a kalendarz buddyjski przyda się dopiero przy '
      + 'wypełnianiu formularza.' }));
    var list = U.el('div', { class: 'list' });
    Numbers.lessons().forEach(function (L) {
      var row = U.el('div', { class: 'row static' });
      var main = U.el('div', { class: 'row-main' });
      main.appendChild(U.el('strong', { text: L.title }));
      main.appendChild(U.el('span', { class: 'muted', text:
        ' — po lekcji ' + L.anchorNumber + ' (' + L.level + ')' }));
      main.appendChild(U.el('p', { class: 'muted small', text: L.goal }));
      row.appendChild(main);
      list.appendChild(row);
    });
    box.appendChild(list);

    var irr = (DB.numbers && DB.numbers.irregularities) || [];
    if (irr.length) {
      box.appendChild(U.el('h3', { text: 'Nieregularności ujęte w danych' }));
      var ul = U.el('ul', { class: 'plain-list' });
      irr.forEach(function (i) {
        ul.appendChild(U.el('li', { text: i.label
          + (i.examples && i.examples.length ? ' (np. ' + i.examples.slice(0, 3).join(', ') + ')' : '') }));
      });
      box.appendChild(ul);
    }

    var scenes = Numbers.scenes();
    if (scenes.length) {
      box.appendChild(U.el('h3', { text: 'Sceny, w których liczba jest sednem' }));
      var sl = U.el('div', { class: 'list' });
      scenes.forEach(function (sc) {
        var btn = U.el('button', { class: 'row', type: 'button' });
        btn.appendChild(U.el('span', { class: 'row-main', text: sc.title + ' — ' + sc.setting }));
        btn.addEventListener('click', function () {
          var area = U.clear(U.$('#numbers-area'));
          Numbers.renderScene(area, sc, function () { RENDER.numbers(); });
          area.scrollIntoView({ block: 'start' });
        });
        sl.appendChild(btn);
      });
      box.appendChild(sl);
    }
  }

  /* ============================================== RATOWANIE ROZMOWY (sesja T) */

  var rescueMode = 'drill';

  RENDER.rescue = function () {
    var modes = U.clear(U.$('#rescue-modes'));
    var area = U.$('#rescue-area');
    if (!Rescue.loaded()) {
      U.clear(area).appendChild(U.el('p', { class: 'muted', text: 'Wczytuję formuły…' }));
      return;
    }
    [['drill', 'Dryl odruchu'], ['list', 'Wszystkie formuły']].forEach(function (m) {
      var chip = U.el('button', { class: 'chip', type: 'button',
        'aria-pressed': rescueMode === m[0] ? 'true' : 'false', text: m[1] });
      chip.addEventListener('click', function () { rescueMode = m[0]; RENDER.rescue(); });
      modes.appendChild(chip);
    });
    if (rescueMode === 'list') {
      Rescue.renderList(U.clear(area));
    } else {
      nextRescueTask();
    }
  };

  function nextRescueTask() {
    var area = U.clear(U.$('#rescue-area'));
    Rescue.renderDrill(area, nextRescueTask);
  }

  /* ------------------------------------------- statystyka liczb i odruchu */

  function renderNumberStats() {
    var box = U.clear(U.$('#prog-numbers'));
    var st = Progress.numberStats();
    box.appendChild(U.el('h2', { text: 'Liczby: skuteczność i czas reakcji' }));
    if (!st.answers) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Jeszcze bez podejścia. Ćwiczenia liczbowe są na ekranie „Liczby w mowie”.' }));
      return;
    }
    box.appendChild(U.el('p', { class: 'muted', text:
      'Przy liczbach czas reakcji jest GŁÓWNĄ miarą opanowania, ważniejszą niż '
      + 'sama poprawność: liczba odczytana bezbłędnie po sześciu sekundach nie '
      + 'zadziałała w kasie. Do mediany wchodzą wyłącznie odpowiedzi trafne — '
      + 'czas pomyłki mierzy wahanie, a nie umiejętność.' }));

    var tbl = U.el('table', { class: 'data-table' });
    var head = U.el('tr');
    ['Ćwiczenie', 'Odpowiedzi', 'Trafność', 'Mediana', 'Próg', 'Stan'].forEach(function (h) {
      head.appendChild(U.el('th', { text: h }));
    });
    tbl.appendChild(head);
    st.rows.forEach(function (r) {
      var tr = U.el('tr');
      tr.appendChild(U.el('td', { text: r.label }));
      tr.appendChild(U.el('td', { text: String(r.answers) }));
      tr.appendChild(U.el('td', { text: Math.round(r.share * 100) + '%' }));
      tr.appendChild(U.el('td', { text: r.median ? (r.median / 1000).toFixed(1).replace('.', ',') + ' s' : '—' }));
      tr.appendChild(U.el('td', { text: (r.target / 1000).toFixed(1).replace('.', ',') + ' s' }));
      tr.appendChild(U.el('td', { text: r.mastered ? 'opanowane'
        : (r.answers < 10 ? 'za mało prób' : 'w trakcie') }));
      tbl.appendChild(tr);
    });
    box.appendChild(tbl);
    box.appendChild(U.el('p', { class: 'muted', text:
      'Opanowane: ' + st.mastered + ' z ' + st.rows.length + ' ćwiczeń. '
      + 'Mediana ogólna: ' + (st.median ? (st.median / 1000).toFixed(1).replace('.', ',') + ' s' : '—')
      + '. Odpowiedzi po czasie: ' + st.timeouts + '.' }));
    if (st.timeouts / Math.max(1, st.answers) > 0.25) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Ponad co czwarte zadanie kończy się upływem limitu. Jeżeli powodem jest '
        + 'samo wpisywanie, a nie rozpoznawanie liczby, wydłuż limit w Ustawieniach '
        + '— pomiar czasu zostaje, znika tylko odcinanie odpowiedzi.' }));
    }
  }

  function renderReflexStats() {
    var box = U.clear(U.$('#prog-reflex'));
    var st = Progress.reflexStats();
    box.appendChild(U.el('h2', { text: 'Odruch ratunkowy: reagujesz czy zamierasz?' }));
    if (!st.answers) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Jeszcze bez podejścia. Dryl jest na ekranie „Ratowanie rozmowy”.' }));
      return;
    }
    box.appendChild(U.el('p', { class: 'muted', text:
      'Mierzone są dwie osobne rzeczy. Pierwsza: czy w ogóle pada reakcja — brak '
      + 'reakcji w oknie liczy się jak zła odpowiedź, bo w rozmowie też się tak '
      + 'liczy. Druga: czy po Twojej formule rozmowa faktycznie się naprawia. '
      + 'Formuła, po której nadal nie rozumiesz, jest tylko uprzejmym sposobem '
      + 'na utknięcie w tym samym miejscu.' }));

    var frozenPct = Math.round(st.frozenShare * 100);
    box.appendChild(U.el('p', { text: 'Zamarcia: ' + frozenPct + '% podejść ('
      + st.frozen + ' z ' + st.answers + '). Trafność formuły: '
      + Math.round(st.share * 100) + '%. Mediana reakcji: '
      + (st.median ? (st.median / 1000).toFixed(1).replace('.', ',') + ' s' : '—')
      + ' przy progu odruchu ' + (st.mastery / 1000).toFixed(1).replace('.', ',') + ' s.' }));
    box.appendChild(U.el('p', { class: 'muted', text:
      'Pętla naprawcza: po Twojej reakcji rozmowa dała się uratować w '
      + Math.round(st.repairShare * 100) + '% przypadków ('
      + st.repaired + ' z ' + st.repairTries + ').' }));

    var tbl = U.el('table', { class: 'data-table' });
    var head = U.el('tr');
    ['Sytuacja', 'Podejść', 'Zamarcia', 'Trafność', 'Mediana'].forEach(function (h) {
      head.appendChild(U.el('th', { text: h }));
    });
    tbl.appendChild(head);
    st.rows.forEach(function (r) {
      var tr = U.el('tr');
      tr.appendChild(U.el('td', { text: r.label }));
      tr.appendChild(U.el('td', { text: String(r.answers) }));
      tr.appendChild(U.el('td', { text: Math.round(r.frozenShare * 100) + '%' }));
      tr.appendChild(U.el('td', { text: Math.round(r.share * 100) + '%' }));
      tr.appendChild(U.el('td', { text: r.median ? (r.median / 1000).toFixed(1).replace('.', ',') + ' s' : '—' }));
      tbl.appendChild(tr);
    });
    box.appendChild(tbl);
  }


  RENDER.course = function () {
    var lessons = Course.lessons();
    var stats = U.clear(U.$('#course-stats'));
    if (!lessons.length) {
      U.clear(U.$('#course-map')).appendChild(U.el('p', { class: 'muted',
        text: 'Ścieżka nauki jeszcze się wczytuje…' }));
      return;
    }

    var sum = Course.summary();
    stats.appendChild(statBox(sum.done + ' / ' + sum.total, 'lekcji zaliczonych'));
    stats.appendChild(statBox(sum.percent + '%', 'ukończenia kursu'));
    stats.appendChild(statBox(Progress.entryLevel() || '—', 'poziom z testu'));
    stats.appendChild(statBox(Progress.summary().accuracy + '%', 'skuteczność'));

    /* --- tempo kursu i kamień milowy bieżącego rozdziału ---
       Przy 333 lekcjach sam pasek procentowy nic nie mówi: różnica między
       31 a 34 procentami jest niewidoczna, a to jest dziesięć lekcji.
       Uczący się potrzebuje dwóch konkretów — gdzie jest (rozdział) i ile
       to jeszcze potrwa przy tempie, które faktycznie utrzymuje. */
    var pace = Course.pace();
    var chapter = Course.currentChapter();
    var paceBox = U.clear(U.$('#course-pace'));
    if (paceBox) {
      if (chapter) {
        var chSt = Course.chapterState(chapter);
        var chList = Course.chapters();
        paceBox.appendChild(U.el('h2', { text:
          'Rozdział ' + chapter.number + ' z ' + chList.length + ': ' + chapter.title }));
        paceBox.appendChild(U.el('p', { class: 'muted', text:
          'Poziom ' + chapter.level + ' · lekcje ' + chapter.fromNumber + '–' + chapter.toNumber +
          ' · zrobione ' + chSt.done + ' z ' + chSt.total + ' (' + chSt.percent + '%).' }));
        paceBox.appendChild(U.el('p', { class: 'muted', text: Course.milestone(chapter) }));
      }
      if (pace.known) {
        var perWeek = Math.round(pace.perWeek * 10) / 10;
        paceBox.appendChild(U.el('p', { class: 'bc-pl', text:
          'Twoje tempo: ' + String(perWeek).replace('.', ',') + ' lekcji na tydzień.' }));
        paceBox.appendChild(U.el('p', { class: 'muted', text:
          'Do końca poziomu ' + pace.level + ' zostało ' + pace.remainingLevel + ' ' +
          U.plural(pace.remainingLevel, 'lekcja', 'lekcje', 'lekcji') +
          ' — przy tym tempie około ' + U.dateWords(pace.dateLevel) + '. ' +
          'Cała ścieżka (' + pace.remainingTotal + ' ' +
          U.plural(pace.remainingTotal, 'lekcja', 'lekcje', 'lekcji') +
          ') — około ' + U.dateWords(pace.dateTotal) + '.' }));
        paceBox.appendChild(U.el('p', { class: 'muted small', text:
          'Liczone z ostatnich czterech tygodni: ' + pace.lessonsInWindow + ' ' +
          U.plural(pace.lessonsInWindow, 'lekcja', 'lekcje', 'lekcji') + ' w ' +
          pace.activeDays + ' ' + U.plural(pace.activeDays, 'dniu', 'dniach', 'dniach') +
          ' nauki. Prognoza zmienia się razem z tempem.' }));
      } else {
        paceBox.appendChild(U.el('p', { class: 'muted', text:
          'Prognozy czasu jeszcze nie ma — policzy się po trzech dniach nauki. ' +
          'Do końca ścieżki zostało ' + pace.remainingTotal + ' z ' + pace.total + ' lekcji.' }));
      }
    }

    /* --- karta „następna lekcja” --- */
    var next = Course.next();
    var nextBox = U.clear(U.$('#course-next'));
    if (Course.moduleZeroBlocks()) {
      /* Dopóki Moduł 0 nie jest zrobiony, to on jest następnym krokiem —
         nie lekcja 1. Karta mówi wprost, dlaczego, bo blokada bez powodu
         wygląda jak awaria. */
      var m0sum = Perception.summary();
      nextBox.appendChild(U.el('h2', { text: 'Najpierw Moduł 0 — trening słuchu' }));
      nextBox.appendChild(U.el('p', { class: 'muted', text:
        'Kurs zaczyna się od słuchu, nie od słów. Dopóki nie usłyszysz różnicy między '
        + 'khǎaw (biały) a khàaw (wiadomości), zapiszesz oba wyrazy w pamięci bez tonu — '
        + 'czyli błędnie, a każda następna lekcja ten zapis utrwali.' }));
      nextBox.appendChild(U.el('p', { class: 'muted', text:
        'Zrobione ' + m0sum.done + ' z ' + m0sum.total + ' lekcji modułu.' }));
      var goM0 = U.el('button', { class: 'btn gold', type: 'button',
        text: m0sum.done ? 'Wróć do Modułu 0' : 'Otwórz Moduł 0' });
      goM0.addEventListener('click', function () { App.go('module0'); });
      nextBox.appendChild(U.el('div', { class: 'btn-row' }, [goM0]));
    } else if (!next) {
      nextBox.appendChild(U.el('h2', { text: 'Cała ścieżka za Tobą' }));
      nextBox.appendChild(U.el('p', { class: 'muted', text:
        'Wszystkie ' + sum.total + ' lekcji są zaliczone. Dalej pracuj na Powtórkach '
        + 'i ćwiczeniach produkcyjnych — one nie mają końca.' }));
      var toSrs = U.el('button', { class: 'btn gold', type: 'button', text: 'Przejdź do powtórek' });
      toSrs.addEventListener('click', function () { App.go('srs'); });
      nextBox.appendChild(U.el('div', { class: 'btn-row' }, [toSrs]));
    } else {
      nextBox.appendChild(U.el('h2', { text: 'Następna lekcja' }));
      nextBox.appendChild(U.el('p', { class: 'bc-pl', text:
        next.number + '. ' + next.title }));
      nextBox.appendChild(U.el('p', { class: 'muted', text: next.goal }));
      var open = U.el('button', { class: 'btn gold', type: 'button', text: 'Otwórz lekcję' });
      open.addEventListener('click', function () { openLesson(next); });
      nextBox.appendChild(U.el('div', { class: 'btn-row' }, [open]));
    }

    /* --- filtr poziomu --- */
    var sel = U.$('#course-level');
    if (sel.options.length <= 1) {
      var byLvl = Course.byLevel();
      Object.keys(byLvl).forEach(function (l) {
        if (!byLvl[l].total) return;
        sel.appendChild(U.el('option', { value: l,
          text: l + ' (' + byLvl[l].done + '/' + byLvl[l].total + ')' }));
      });
    }
    sel.value = courseState.level;

    /* --- mapa --- */
    var map = U.clear(U.$('#course-map'));
    var shown = lessons.filter(function (L) {
      return !courseState.level || L.level === courseState.level;
    });

    if (!courseState.level) map.appendChild(moduleZeroBlock());

    /* Mapa jest łamana rozdziałami, nie poziomami. Poziom nadal jest widoczny
       — stoi w nagłówku rozdziału — ale to rozdział jest jednostką, którą da
       się ogarnąć wzrokiem i skończyć w rozsądnym czasie. */
    var currentLevel = null, currentChapter = null;
    shown.forEach(function (L) {
      if (L.level !== currentLevel) {
        currentLevel = L.level;
        map.appendChild(U.el('h2', { class: 'course-level', text: 'Poziom ' + L.level }));
      }
      if (L.chapterId && L.chapterId !== currentChapter) {
        currentChapter = L.chapterId;
        var ch = Course.chapterOf(L);
        if (ch) map.appendChild(chapterHead(ch));
      }
      map.appendChild(lessonNode(L));
    });
  };

  App.renderCourse = function () { if (RENDER.course) RENDER.course(); };

  /* Moduł 0 stoi na mapie jako osobny blok PRZED poziomem Survival — nie jako
     jedna z lekcji i nie jako dodatek na końcu. Kolejność na mapie jest tu
     komunikatem samym w sobie: trening słuchu poprzedza naukę słów. */
  function moduleZeroBlock() {
    var wrap = U.el('div', { class: 'm0-block' });
    if (!global.Perception || !Perception.ready()) return wrap;
    var sum = Perception.summary();
    var blocking = Course.moduleZeroBlocks();
    var skipped = Perception.isSkipped();
    var optional = Perception.isOptional();

    wrap.appendChild(U.el('h2', { class: 'course-level', text: 'Moduł 0 — trening słuchu' }));

    var card = U.el('button', {
      class: 'lesson-card m0-card is-' + (sum.done >= sum.total ? 'passed'
        : (skipped ? 'skipped' : 'open')),
      type: 'button',
      'aria-label': 'Moduł 0, trening słuchu. ' + sum.done + ' z ' + sum.total
        + ' lekcji zrobionych. ' + (blocking
          ? 'Wymagany przed lekcją 1.'
          : (skipped ? 'Pominięty.' : (optional ? 'Opcjonalny.' : 'Zrobiony.')))
    });
    var badge = U.el('span', { class: 'lesson-badge', 'aria-hidden': 'true' });
    if (sum.done >= sum.total) badge.appendChild(U.icon('check'));
    else badge.appendChild(U.el('span', { text: '0' }));
    card.appendChild(badge);

    var main = U.el('span', { class: 'lesson-main' });
    main.appendChild(U.el('span', { class: 'lesson-title', text:
      '12 lekcji percepcyjnych — tony, długość samogłosek, przydech' }));
    main.appendChild(U.el('span', { class: 'lesson-meta', text:
      sum.done + ' / ' + sum.total + ' lekcji · ' + sum.tasks + ' zadań · '
      + (blocking ? 'wymagany przed lekcją 1'
        : (skipped ? 'pominięty świadomie'
          : (optional ? 'opcjonalny — zwolniony testem poziomującym' : 'zrobiony'))) }));
    card.appendChild(main);
    card.addEventListener('click', function () { App.go('module0'); });
    wrap.appendChild(card);

    if (blocking) {
      wrap.appendChild(U.el('p', { class: 'muted m0-gate-note', text:
        'Poziom Survival otworzy się po Module 0. Możesz go pominąć — świadomie, '
        + 'na ekranie modułu, po przeczytaniu, czym to skutkuje.' }));
    }
    wrap.appendChild(U.el('h2', { class: 'course-level', text: 'Ścieżka słownikowa' }));
    return wrap;
  }

  /* Nagłówek rozdziału na mapie: postęp i to, co daje ukończenie. Zwinięty
     do jednego wiersza, żeby nie przytłoczył listy lekcji — kamień milowy
     rozwija się kliknięciem. */
  function chapterHead(ch) {
    var st = Course.chapterState(ch);
    var wrap = U.el('div', { class: 'chapter-head is-' +
      (st.complete ? 'done' : (st.started ? 'active' : 'ahead')) });

    var line = U.el('button', { class: 'chapter-line', type: 'button',
      'aria-expanded': 'false',
      'aria-label': 'Rozdział ' + ch.number + ': ' + ch.title + '. Zrobione ' +
        st.done + ' z ' + st.total + ' lekcji. Rozwiń kamień milowy.' });
    line.appendChild(U.el('span', { class: 'chapter-num', text: String(ch.number) }));
    var mid = U.el('span', { class: 'chapter-main' });
    mid.appendChild(U.el('span', { class: 'chapter-title', text: ch.title }));
    mid.appendChild(U.el('span', { class: 'chapter-meta', text:
      'lekcje ' + ch.fromNumber + '–' + ch.toNumber + ' · ' + ch.newWords +
      ' nowych haseł · zrobione ' + st.done + '/' + st.total }));
    line.appendChild(mid);
    line.appendChild(U.el('span', { class: 'chapter-pct', text: st.percent + '%' }));
    wrap.appendChild(line);

    var body = U.el('p', { class: 'chapter-milestone muted', text: Course.milestone(ch) });
    body.hidden = true;
    wrap.appendChild(body);

    line.addEventListener('click', function () {
      body.hidden = !body.hidden;
      line.setAttribute('aria-expanded', body.hidden ? 'false' : 'true');
    });
    return wrap;
  }

  function lessonNode(L) {
    var status = Course.status(L);
    var node = U.el('button', {
      class: 'lesson-card is-' + status,
      type: 'button',
      'data-lesson': L.id,
      'aria-label': 'Lekcja ' + L.number + ': ' + L.title + '. '
        + { passed: 'Zaliczona.', skipped: 'Pominięta.', open: 'Dostępna.',
            locked: 'Zablokowana — najpierw zalicz poprzednią lekcję.' }[status]
    });

    var badge = U.el('span', { class: 'lesson-badge', 'aria-hidden': 'true' });
    if (status === 'passed') badge.appendChild(U.icon('check'));
    else if (status === 'locked') badge.appendChild(U.icon('lock'));
    else badge.appendChild(U.el('span', { text: String(L.number) }));
    node.appendChild(badge);

    var main = U.el('span', { class: 'lesson-main' });
    main.appendChild(U.el('span', { class: 'lesson-title', text: L.title }));
    main.appendChild(U.el('span', { class: 'lesson-meta', text:
      L.recordIds.length + ' haseł · ' + L.newWordIds.length + ' nowych · ' + L.grammarTitle }));
    node.appendChild(main);

    node.addEventListener('click', function () { openLesson(L); });
    return node;
  }

  /* --------------------------------------------------------- widok lekcji */

  function openLesson(L) {
    var status = Course.status(L);
    var body = U.el('div');
    body.appendChild(U.el('h2', { id: 'sheet-title', text: L.number + '. ' + L.title }));
    body.appendChild(U.el('p', { class: 'muted', text: L.level + ' · ' + L.category }));

    if (status === 'locked') {
      body.appendChild(U.el('p', { text: L.goal }));
      body.appendChild(U.el('p', { class: 'fb bad', text:
        'Ta lekcja jest jeszcze zamknięta. Ścieżka jest ułożona tak, że każde nowe słowo '
        + 'da się od razu użyć w zdaniu ze słów wcześniejszych — przeskoczenie lekcji '
        + 'oznaczałoby zdania z lukami. Zalicz poprzednią lekcję albo oznacz ją jako znaną.' }));
      var prev = Course.lessons()[Course.lessons().indexOf(L) - 1];
      var goPrev = U.el('button', { class: 'btn gold', type: 'button', text: 'Otwórz poprzednią lekcję' });
      goPrev.addEventListener('click', function () { closeSheet(); openLesson(prev); });
      var skipPrev = U.el('button', { class: 'btn ghost', type: 'button', text: 'Znam poprzednią — pomiń ją' });
      skipPrev.addEventListener('click', function () {
        Course.skip(prev);
        closeSheet();
        RENDER.course();
        openLesson(L);
      });
      body.appendChild(U.el('div', { class: 'btn-row' }, [goPrev, skipPrev]));
      openSheet(body);
      return;
    }

    body.appendChild(U.el('p', { text: L.goal }));
    body.appendChild(U.el('p', { class: 'muted', text: 'Zaliczenie: ' + L.pass.text }));
    var loading = U.el('p', { class: 'muted', role: 'status', text: 'Wczytuję materiał lekcji…' });
    body.appendChild(loading);
    openSheet(body);

    Course.load(L).then(function (material) {
      if (U.$('#sheet').hidden) return;
      loading.remove();
      renderLessonBody(body, L, material, status);
    });
  }

  function renderLessonBody(body, L, material, status) {
    if (status === 'passed' || status === 'skipped') {
      var st = Progress.lessonState(L.id);
      body.appendChild(U.el('p', { class: 'fb ok', text: status === 'passed'
        ? 'Zaliczona ' + st.date + ' — ' + st.score + ' z ' + st.total + ' odpowiedzi.'
        : 'Oznaczona jako znana.' }));
    }

    /* --- nowe hasła --- */
    body.appendChild(U.el('h3', { text: 'Nowe hasła w tej lekcji' }));
    var newList = U.el('div', { class: 'list' });
    material.newWords.forEach(function (r) { newList.appendChild(recordRow(r)); });
    body.appendChild(newList);

    /* --- reszta materiału --- */
    var rest = material.records.filter(function (r) {
      return L.newWordIds.indexOf(r.id) === -1;
    });
    if (rest.length) {
      body.appendChild(U.el('h3', { text: 'Użycie — wszystko z tego, co już znasz' }));
      var restList = U.el('div', { class: 'list' });
      rest.forEach(function (r) { restList.appendChild(recordRow(r)); });
      body.appendChild(restList);
    }

    /* --- gramatyka --- */
    if (material.grammar) {
      body.appendChild(U.el('h3', { text: 'Temat gramatyczny: ' + material.grammar.title }));
      body.appendChild(U.el('p', { class: 'muted', text: material.grammar.explanation }));
      (material.grammar.patterns || []).slice(0, 3).forEach(function (src) {
        var pt = G.view(src);
        var card = U.el('div', { class: 'bigcard' });
        card.appendChild(U.el('div', { class: 'bc-pl', text: pt.polish }));
        card.appendChild(U.renderPhonetic(pt.thaiPhonetic, { hideTones: App.settings.hideTones }));
        card.appendChild(U.el('div', { class: 'btn-row' }, [Player.button(pt, 'Posłuchaj')]));
        body.appendChild(card);
      });
      if (material.grammar.tip) {
        body.appendChild(U.el('p', { class: 'muted', text: 'Wskazówka: ' + material.grammar.tip }));
      }
    }

    /* --- dialog --- */
    if (material.dialogue) {
      body.appendChild(U.el('h3', { text: 'Dialog do tej lekcji: ' + material.dialogue.title }));
      var dlgBtn = U.el('button', { class: 'btn ghost', type: 'button', text: 'Otwórz dialog' });
      dlgBtn.addEventListener('click', function () {
        closeSheet();
        App.openDialogue(material.dialogue.id);
      });
      var rpBtn = U.el('button', { class: 'btn ghost', type: 'button', text: 'Odegraj ten dialog' });
      rpBtn.addEventListener('click', function () {
        closeSheet();
        App.openRolePlay(material.dialogue.id);
      });
      body.appendChild(U.el('div', { class: 'btn-row' }, [dlgBtn, rpBtn]));
    }

    /* --- akcje --- */
    var test = U.el('button', { class: 'btn gold', type: 'button',
      text: status === 'passed' ? 'Powtórz sprawdzian' : 'Zdaj sprawdzian' });
    test.addEventListener('click', function () { startLessonTest(L, material); });

    var srsBtn = U.el('button', { class: 'btn ghost', type: 'button', text: 'Dodaj lekcję do powtórek' });
    srsBtn.addEventListener('click', function () {
      var added = 0;
      L.recordIds.forEach(function (id) { if (SRS.addBoth(id)) added += 1; });
      U.toast(added + ' ' + U.plural(added, 'hasło trafiło', 'hasła trafiły', 'haseł trafiło') + ' do powtórek.');
    });

    var skipBtn = U.el('button', { class: 'btn ghost', type: 'button',
      text: Progress.isLessonDone(L.id) ? 'Cofnij zaliczenie' : 'Znam to — pomiń lekcję' });
    skipBtn.addEventListener('click', function () {
      if (Progress.isLessonDone(L.id)) Course.reset(L);
      else Course.skip(L);
      closeSheet();
      RENDER.course();
    });

    body.appendChild(U.el('div', { class: 'btn-row' }, [test, srsBtn, skipBtn]));
  }

  /* ------------------------------------------------------ sprawdzian lekcji */

  function startLessonTest(L, material) {
    Course.startTest(material);
    var body = U.clear(U.$('#sheet-body'));
    body.appendChild(U.el('h2', { id: 'sheet-title', text: 'Sprawdzian: ' + L.title }));
    var area = U.el('div');
    body.appendChild(area);
    runLessonQuestion(L, area);
  }

  /* Sprawdzian korzysta z tych samych trybów produkcyjnych co ekran ćwiczeń —
     uczący się nie zdaje niczego, czego wcześniej nie ćwiczył. */
  function runLessonQuestion(L, area) {
    var run = Course.run;
    U.clear(area);

    if (Course.testDone()) { showLessonResult(L, area); return; }

    var item = run.items[run.at];
    var head = U.el('p', { class: 'muted', text:
      'Pytanie ' + (run.at + 1) + ' z ' + run.items.length + ' · trafnych: ' + run.correct
      + ' · do zaliczenia trzeba ' + L.pass.required });
    area.appendChild(head);
    var bar = U.el('div', { class: 'progress' });
    bar.appendChild(U.el('i', { style: 'width:' + Math.round(run.at / run.items.length * 100) + '%' }));
    area.appendChild(bar);

    var box = U.el('div');
    area.appendChild(box);

    /* Produce raportuje wynik przez wywołanie zwrotne — dzięki temu sprawdzian
       liczy punkty, a same ćwiczenia nic o lekcjach nie wiedzą. */
    Produce.onAnswer = function (id, ok) {
      Course.recordAnswer(ok, id);
      Progress.answer(id, ok, { mode: 'lesson', grammarId: L.grammarId });
      /* Sprawdzian lekcji pyta o rozpoznanie, więc karmi stronę receptywną
         tematu tej lekcji. Produkcję karmią przekształcenia i układanie
         zdań — mieszanie ich zatarłoby całą różnicę, którą ta statystyka
         ma pokazywać. */
      Progress.grammarAnswer(id, ok, 'receptive');
    };
    Produce.mode = item.kind;
    Produce.lessonPool = [item.rec];
    Produce.renderOne(box, item.rec, function () {
      Produce.lessonPool = null;
      runLessonQuestion(L, area);
    });
  }

  function showLessonResult(L, area) {
    Produce.onAnswer = null;
    var result = Course.finishTest();
    U.clear(area);
    area.appendChild(U.el('h3', { text: result.passed ? 'Zaliczone' : 'Jeszcze nie tym razem' }));
    area.appendChild(U.el('p', { class: result.passed ? 'fb ok' : 'fb bad', text:
      result.correct + ' z ' + result.total + ' trafnych odpowiedzi. Próg zaliczenia: '
      + result.required + '.' }));

    if (result.wrongIds.length) {
      area.appendChild(U.el('p', { class: 'muted', text:
        'Hasła, które sprawiły kłopot, trafiły do powtórek:' }));
      var list = U.el('div', { class: 'list' });
      result.wrongIds.forEach(function (id) {
        var r = DB.any(id);
        if (r) list.appendChild(recordRow(r));
      });
      area.appendChild(list);
    }

    var again = U.el('button', { class: 'btn', type: 'button',
      text: result.passed ? 'Zdaj jeszcze raz' : 'Spróbuj ponownie' });
    again.addEventListener('click', function () {
      Course.load(L).then(function (m) { startLessonTest(L, m); });
    });
    var back = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wróć do kursu' });
    back.addEventListener('click', function () { closeSheet(); RENDER.course(); });
    var buttons = [again, back];

    if (result.passed) {
      var nextL = Course.next();
      if (nextL) {
        var go = U.el('button', { class: 'btn gold', type: 'button', text: 'Następna lekcja' });
        go.addEventListener('click', function () { closeSheet(); RENDER.course(); openLesson(nextL); });
        buttons = [go, back, again];
      }
    }
    area.appendChild(U.el('div', { class: 'btn-row' }, buttons));
    buttons[0].focus();
    RENDER.course();
  }

  /* Skróty używane z widoku lekcji. */
  App.openDialogue = function (id) {
    App.go('dialogues');
    DB.ensureDialogues().then(function () {
      var sel = U.$('#dlg-select');
      if (sel) { sel.value = id; renderDialogue(); }
    });
  };

  App.openRolePlay = function (id) {
    Produce.mode = 'roleplay';
    Produce.setDialogue(id);
    App.go('produce');
  };

  /* ==================================================== EKRAN: PRODUKCJA */

  RENDER.produce = function () {
    var row = U.$('#produce-modes');
    if (!row.children.length) {
      Produce.MODES.forEach(function (m) {
        var chip = U.el('button', {
          class: 'chip', type: 'button', 'data-produce': m.id,
          'aria-pressed': String(m.id === Produce.mode), text: m.label
        });
        chip.addEventListener('click', function () {
          U.$$('[data-produce]').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
          chip.setAttribute('aria-pressed', 'true');
          Produce.mode = m.id;
          U.$('#produce-hint').textContent = m.hint;
          renderProduceArea();
        });
        row.appendChild(chip);
      });
    }
    U.$$('[data-produce]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-produce') === Produce.mode));
    });
    var mode = Produce.MODES.filter(function (m) { return m.id === Produce.mode; })[0];
    if (mode) U.$('#produce-hint').textContent = mode.hint;
    renderProduceArea();
  };

  function renderProduceArea() {
    var area = U.$('#produce-area');
    U.clear(area).appendChild(U.el('p', { class: 'muted', role: 'status', text: 'Przygotowuję ćwiczenie…' }));
    Produce.ensureData().then(function () {
      if (App.screen !== 'produce') return;
      Produce.render(area);
    });
  }


  /* --------------------------------------------- postęp: kurs i błędy */

  function renderCourseProgress() {
    var box = U.clear(U.$('#prog-course'));
    box.appendChild(U.el('h2', { text: 'Kurs' }));
    var sum = Course.summary();
    if (!sum.total) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Ścieżka nauki jeszcze się wczytuje…' }));
      return;
    }
    box.appendChild(U.el('p', { class: 'muted', text:
      sum.passed + ' ' + U.plural(sum.passed, 'lekcja zaliczona', 'lekcje zaliczone', 'lekcji zaliczonych')
      + ', ' + sum.skipped + ' pominiętych, razem ' + sum.done + ' z ' + sum.total + ' (' + sum.percent + '%).' }));
    var bar = U.el('div', { class: 'progress' });
    bar.appendChild(U.el('i', { style: 'width:' + sum.percent + '%' }));
    box.appendChild(bar);

    var byLvl = Course.byLevel();
    Object.keys(byLvl).forEach(function (l) {
      var v = byLvl[l];
      if (!v.total) return;
      box.appendChild(U.el('p', { class: 'muted', text: l + ': ' + v.done + ' / ' + v.total }));
    });

    var p = Progress.data.placement;
    if (p) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Test poziomujący: ' + p.level + ' (' + p.score + '/' + p.total + ', ' + p.date + ').' }));
    }
    var retest = U.el('button', { class: 'btn ghost', type: 'button', text: 'Powtórz test poziomujący' });
    retest.addEventListener('click', function () { Placement.state = null; App.go('placement'); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [retest]));
  }

  /* --------------------------------------------- postęp: słuch (Moduł 0) */

  /* Percepcja dostaje własną sekcję, bo mierzy co innego niż reszta postępu.
     Tam liczy się „ile haseł znasz”, tutaj „które kontrasty Twoje ucho
     rozróżnia”. Uśrednienie jednego z drugim zgubiłoby jedno i drugie. */
  function renderPerception() {
    var box = U.clear(U.$('#prog-perception'));
    box.appendChild(U.el('h2', { text: 'Słuch — kontrasty fonetyczne' }));
    if (!global.Perception || !Perception.ready()) {
      box.appendChild(U.el('p', { class: 'muted', text: 'Moduł 0 jeszcze się wczytuje…' }));
      return;
    }
    var ps = Progress.perceptionSummary();
    var sum = Perception.summary();

    box.appendChild(U.el('p', { class: 'muted', text:
      sum.done + ' z ' + sum.total + ' lekcji Modułu 0'
      + (sum.diagnosed ? ' (w tym ' + sum.diagnosed + ' zwolnionych diagnozą)' : '')
      + ' · ' + ps.answers + ' ' + U.plural(ps.answers, 'odpowiedź', 'odpowiedzi', 'odpowiedzi')
      + ' percepcyjnych' + (ps.answers ? ' · skuteczność ' + ps.accuracy + '%' : '') }));
    var bar = U.el('div', { class: 'progress' });
    bar.appendChild(U.el('i', { style: 'width:' + sum.percent + '%' }));
    box.appendChild(bar);

    if (!ps.answers) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Statystyka per kontrast pojawi się po pierwszym ćwiczeniu słuchowym. '
        + 'Najszybciej zbierze ją diagnoza percepcyjna — 20 zadań, kilka minut.' }));
      var go = U.el('button', { class: 'btn gold', type: 'button', text: 'Otwórz Moduł 0' });
      go.addEventListener('click', function () { App.go('module0'); });
      box.appendChild(U.el('div', { class: 'btn-row' }, [go]));
      return;
    }

    /* --- najsłabszy kontrast --- */
    var worst = Progress.weakestContrast(4);
    if (worst) {
      box.appendChild(U.el('p', { class: 'bc-pl', text:
        'Najsłabszy kontrast: ' + Perception.contrastLabel(worst.id) }));
      var c = Perception.contrast(worst.id);
      box.appendChild(U.el('p', { class: 'muted', text:
        worst.correct + ' z ' + worst.answers + ' trafnych (' + worst.rate + '%).'
        + (c ? ' ' + c.note : '') }));
    } else {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Za mało odpowiedzi, żeby wskazać najsłabszy kontrast — potrzeba co najmniej '
        + 'czterech prób na kontrast, inaczej pokazywalibyśmy przypadek.' }));
    }

    /* --- tabela per kontrast --- */
    var rows = Progress.contrastStats(4);
    var table = U.el('table', { class: 'data-table' });
    table.appendChild(U.el('caption', { text: 'Skuteczność w rozbiciu na kontrasty' }));
    var thead = U.el('thead');
    var hr = U.el('tr');
    ['Kontrast', 'Odpowiedzi', 'Trafnych', 'Skuteczność'].forEach(function (h) {
      hr.appendChild(U.el('th', { scope: 'col', text: h }));
    });
    thead.appendChild(hr);
    table.appendChild(thead);
    var tbody = U.el('tbody');
    rows.forEach(function (r) {
      var tr = U.el('tr');
      tr.appendChild(U.el('th', { scope: 'row', text:
        Perception.contrastLabel(r.id) + (r.reliable ? '' : ' (za mało prób)') }));
      tr.appendChild(U.el('td', { text: String(r.answers) }));
      tr.appendChild(U.el('td', { text: String(r.correct) }));
      tr.appendChild(U.el('td', { text: r.rate + '%' }));
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    box.appendChild(table);

    /* --- historia w czasie --- */
    var hist = Progress.contrastHistory(worst ? worst.id : null, 5);
    if (hist.length >= 2) {
      box.appendChild(U.el('h3', { text: worst
        ? 'Jak zmienia się kontrast „' + Perception.contrastLabel(worst.id) + '”'
        : 'Skuteczność percepcyjna w czasie' }));
      var chart = U.el('div', { class: 'chart', 'aria-hidden': 'true' });
      hist.forEach(function (h) {
        chart.appendChild(U.el('i', { style: 'height:' + Math.max(3, h.rate) + '%',
          title: h.from + '–' + h.to + ': ' + h.rate + '%' }));
      });
      box.appendChild(chart);
      /* Wykres jest ozdobą; liczby muszą być też w tabeli, inaczej czytnik
         ekranu nie dostaje niczego. */
      var t2 = U.el('table', { class: 'data-table' });
      t2.appendChild(U.el('caption', { text: 'Te same liczby w tabeli' }));
      var th2 = U.el('thead');
      var hr2 = U.el('tr');
      ['Okres', 'Odpowiedzi', 'Skuteczność'].forEach(function (h) {
        hr2.appendChild(U.el('th', { scope: 'col', text: h }));
      });
      th2.appendChild(hr2);
      t2.appendChild(th2);
      var tb2 = U.el('tbody');
      hist.forEach(function (h) {
        var tr = U.el('tr');
        tr.appendChild(U.el('th', { scope: 'row', text: h.from + ' – ' + h.to }));
        tr.appendChild(U.el('td', { text: String(h.answers) }));
        tr.appendChild(U.el('td', { text: h.rate + '%' }));
        tb2.appendChild(tr);
      });
      t2.appendChild(tb2);
      box.appendChild(t2);
    }

    var d = ps.diagnostic;
    if (d) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Diagnoza percepcyjna z ' + d.date + ': ' + d.score + ' z ' + d.total
        + '. Opanowane rodziny kontrastów: '
        + (d.mastered.length ? d.mastered.length : 'brak') + ' z '
        + Perception.families().length + '.' }));
    }
    var go2 = U.el('button', { class: 'btn ghost', type: 'button', text: 'Otwórz Moduł 0' });
    go2.addEventListener('click', function () { App.go('module0'); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [go2]));
  }

  /* Najsłabszy obszar z konkretną propozycją ćwiczenia — sama liczba
     procentowa nie mówi, co z tym zrobić. */
  function renderWeakArea() {
    var box = U.clear(U.$('#prog-weak'));
    box.appendChild(U.el('h2', { text: 'Nad czym popracować' }));
    var worst = Stats.worst();
    if (!worst) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Za mało danych. Statystyka błędów potrzebuje kilku odpowiedzi w danym obszarze — '
        + 'inaczej pokazywałaby przypadek, a nie Twoją słabą stronę.' }));
      return;
    }
    box.appendChild(U.el('p', { class: 'bc-pl', text: worst.label }));
    box.appendChild(U.el('p', { class: 'muted', text:
      worst.bucketLabel + ' · ' + worst.item.wrong + ' ' + U.plural(worst.item.wrong, 'pomyłka', 'pomyłki', 'pomyłek')
      + ' na ' + worst.item.answers + ' odpowiedzi (' + worst.item.rate + '% błędów).' }));

    var row = U.el('div', { class: 'btn-row' });

    /* Sesja naprawcza. Różnica wobec przycisku obok jest zasadnicza: „Ćwicz”
       otwiera ćwiczenie z losowym materiałem z tego obszaru, a to buduje zestaw
       z HASEŁ, NA KTÓRYCH SIĘ POMYLIŁEŚ — z dziennika pomyłek i z kart z
       wpadkami. Jeśli dziennik jest jeszcze pusty, przycisku nie pokazujemy,
       zamiast pokazywać go i nie mieć czym wypełnić zestawu. */
    var set = global.Repair ? Repair.build({
      bucket: worst.kind, key: worst.item.key, label: worst.label, rate: worst.item.rate
    }) : null;

    if (set) {
      var fix = U.el('button', { class: 'btn gold', type: 'button',
        text: 'Sesja naprawcza (' + set.ids.length + ' '
          + U.plural(set.ids.length, 'hasło', 'hasła', 'haseł') + ')' });
      fix.addEventListener('click', function () { startRepair(set); });
      row.appendChild(fix);
      box.appendChild(U.el('p', { class: 'muted', text: set.why }));
    }

    var go = U.el('button', { class: set ? 'btn ghost' : 'btn gold', type: 'button',
      text: 'Ćwicz: ' + worst.suggestion.label });
    go.addEventListener('click', function () {
      Produce.mode = worst.suggestion.mode;
      App.go(worst.suggestion.screen);
    });
    row.appendChild(go);
    box.appendChild(row);
  }

  /* ---------------------------------------- postęp: dwie siły pamięci */

  /* GRAMATYKA: co rozumiem, a czego nie produkuję.

     Rozkład błędów miał wymiar gramatyczny od sesji I, ale mierzył jedną
     liczbę na temat. Przy rotacyjnym przypisaniu ta liczba mówiła o lekcji,
     a nie o konstrukcji. Przy progresji i osiemdziesięciu tematach można
     zapytać ostrzej — i to jest pytanie, na które ta karta odpowiada.

     Konstrukcja rozumiana, ale nieprodukowana, nie naprawia się kolejnym
     ćwiczeniem odsłuchowym. Dlatego przy każdej pozycji stoi przycisk
     prowadzący prosto do przekształceń, a nie ogólna zachęta. */
  function renderGrammarStats() {
    var box = U.clear(U.$('#prog-grammar'));
    box.appendChild(U.el('h2', { text: 'Gramatyka: rozumiem czy produkuję' }));

    if (!DB.grammar || !DB.grammar.length) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Materiał gramatyczny jeszcze się wczytuje.' }));
      return;
    }
    var sum = GStats.summary();
    if (!sum.rated) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Za mało prób. Temat trafia tu dopiero po ' + sum.minAnswers
        + ' odpowiedziach po każdej stronie — dwie pomyłki z dwóch prób to '
        + 'przypadek, a nie wiedza o Tobie. Ocenionych tematów: 0 z '
        + sum.topics + '.' }));
      box.appendChild(gramStageTable());
      return;
    }

    box.appendChild(U.el('p', { class: 'muted', text:
      'Ocenionych tematów: ' + sum.rated + ' z ' + sum.topics
      + '. Temat wchodzi do oceny po ' + sum.minAnswers
      + ' odpowiedziach po każdej stronie.' }));

    var gapList = GStats.understoodNotProduced(6);
    if (!gapList.length) {
      box.appendChild(U.el('p', { text:
        'Nie ma konstrukcji, którą rozumiesz wyraźnie lepiej, niż '
        + 'produkujesz. To dobry stan i rzadki.' }));
    } else {
      box.appendChild(U.el('h3', { text: 'Rozumiesz, ale nie produkujesz' }));
      var list = U.el('div', { class: 'gap-list' });
      gapList.forEach(function (t) {
        var row = U.el('div', { class: 'lesson-row' });
        var body = U.el('div');
        body.appendChild(U.el('h3', { text: t.title }));
        body.appendChild(U.el('p', { class: 'muted', text:
          'Etap ' + t.stage + ' · ze słuchu '
          + Math.round(t.receptive.share * 100) + '% ('
          + t.receptive.answers + ' prób), w produkcji '
          + Math.round(t.productive.share * 100) + '% ('
          + t.productive.answers + ' prób) · różnica '
          + Math.round(t.gap * 100) + ' punktów.' }));
        var go = U.el('button', { class: 'btn ghost', type: 'button',
          text: 'Ćwicz przekształcenia' });
        go.addEventListener('click', function () { App.go('grammar'); });
        body.appendChild(go);
        row.appendChild(body);
        list.appendChild(row);
      });
      box.appendChild(list);
    }

    var reverse = GStats.producedNotUnderstood(3);
    if (reverse.length) {
      box.appendChild(U.el('h3', { text: 'Produkujesz, ale nie rozpoznajesz' }));
      box.appendChild(U.el('p', { class: 'muted', text:
        'Rzadszy przypadek i wart uwagi: wzorzec nauczony na pamięć, którego '
        + 'nie słyszysz w mowie. Pomaga tu wykrywanie struktury ze słuchu, '
        + 'nie kolejne układanie zdań.' }));
      reverse.forEach(function (t) {
        box.appendChild(U.el('p', { text: t.title + ' — ze słuchu '
          + Math.round(t.receptive.share * 100) + '%, w produkcji '
          + Math.round(t.productive.share * 100) + '%.' }));
      });
    }

    box.appendChild(gramStageTable());
  }

  /* Etapy obok siebie. Pokazuje, czy progresja gdzieś się zacięła —
     etap nietknięty to co innego niż etap nieudany. */
  function gramStageTable() {
    var wrap = U.el('div');
    wrap.appendChild(U.el('h3', { text: 'Etapy progresji' }));
    var rows = GStats.byStage();
    var table = U.el('table', { class: 'data-table' });
    var head = U.el('tr');
    ['Etap', 'Tematów', 'Ze słuchu', 'W produkcji'].forEach(function (h) {
      head.appendChild(U.el('th', { text: h, scope: 'col' }));
    });
    table.appendChild(U.el('thead', {}, [head]));
    var body = U.el('tbody');
    rows.forEach(function (s) {
      var tr = U.el('tr');
      tr.appendChild(U.el('td', { text: s.stage + '. ' + s.title }));
      tr.appendChild(U.el('td', { text: String(s.topics) }));
      tr.appendChild(U.el('td', { text: s.rAnswers
        ? Math.round(s.receptiveShare * 100) + '%' : '—' }));
      tr.appendChild(U.el('td', { text: s.pAnswers
        ? Math.round(s.productiveShare * 100) + '%' : '—' }));
      body.appendChild(tr);
    });
    table.appendChild(body);
    wrap.appendChild(table);
    wrap.appendChild(U.el('p', { class: 'muted', text:
      'Kreska znaczy „brak prób”, nie „zero procent”. Etap nietknięty to co '
      + 'innego niż etap nieudany.' }));
    return wrap;
  }

  /* Karta, dla której powstało rozdzielenie kart. Wytworzenie zostaje za
     rozpoznaniem o kilka poziomów i tak ma być — ale dopóki obie liczby
     siedziały w jednej średniej, nie było tego widać ani nie było wiadomo,
     czy różnica rośnie, czy maleje. */
  function renderSides() {
    var box = U.clear(U.$('#prog-sides'));
    box.appendChild(U.el('h2', { text: 'Rozpoznanie a wytworzenie' }));

    var gap = SRS.sideGap();
    if (!gap) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Karty pojawią się, gdy dołożysz hasła do powtórek. Każde hasło ma dwie strony: '
        + 'rozpoznanie (tajski → polski) i wytworzenie (polski → tajski).' }));
      return;
    }

    box.appendChild(U.el('p', { class: 'muted', text:
      'Każde hasło ma osobną kartę na rozpoznanie i na wytworzenie, bo to są dwie różne '
      + 'siły pamięci. Wytworzenie prawie zawsze zostaje w tyle — to normalne, nie błąd.' }));

    var stats = SRS.sideStats();
    var table = U.el('table', { class: 'data-table' });
    table.appendChild(U.el('caption', { text: 'Strony kartoteki' }));
    var thead = U.el('thead');
    var hr = U.el('tr');
    ['Strona', 'Kart', 'Utrwalonych', 'Średni odstęp', 'Skuteczność'].forEach(function (h) {
      hr.appendChild(U.el('th', { scope: 'col', text: h }));
    });
    thead.appendChild(hr);
    table.appendChild(thead);
    var tbody = U.el('tbody');
    SRS.SIDES.forEach(function (s) {
      var b = stats[s];
      if (!b.total) return;
      var tr = U.el('tr');
      tr.appendChild(U.el('th', { scope: 'row', text: b.name + ' — ' + b.long }));
      tr.appendChild(U.el('td', { text: String(b.total) }));
      tr.appendChild(U.el('td', { text: String(b.learned) }));
      tr.appendChild(U.el('td', { text: b.avgInterval + ' dni' }));
      tr.appendChild(U.el('td', { text: b.accuracy === null ? '—' : b.accuracy + '%' }));
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    box.appendChild(table);

    var verdict;
    if (gap.behind) {
      verdict = 'Wytworzenie jest za rozpoznaniem o około ' + gap.steps + ' '
        + U.plural(Math.round(gap.steps), 'poziom', 'poziomy', 'poziomów')
        + ' odstępu. Tak wygląda normalna nauka: rozumiesz więcej, niż potrafisz powiedzieć.';
    } else if (gap.steps < 0.3) {
      verdict = 'Obie strony idą równo — rzadkie i dobre.';
    } else {
      verdict = 'Wytworzenie wyprzedza rozpoznanie. Zwykle znaczy to, że ćwiczysz mówienie '
        + 'i pisanie, a mało słuchasz.';
    }
    box.appendChild(U.el('p', { text: verdict }));

    if (stats.w.total) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Kart wymowy: ' + stats.w.total + '. To hasła, które rozpoznajesz i umiesz wytworzyć, '
        + 'ale wymawiasz z błędnym tonem — wracają jako ćwiczenie mówienia.' }));
    }

    var report = SRS.splitReport();
    if (report && report.derived) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Przy rozdzieleniu kart (' + report.date + ') ' + report.moved + ' '
        + U.plural(report.moved, 'karta przeszła', 'karty przeszły', 'kart przeszło')
        + ' na stronę rozpoznania z pełną historią, a ' + report.derived + ' '
        + U.plural(report.derived, 'karta wytworzenia powstała', 'karty wytworzenia powstały',
                   'kart wytworzenia powstało')
        + ' z krótszym odstępem — bo tej strony nikt wcześniej nie ćwiczył.' }));
    }
  }

  /* ------------------------------- postęp: co algorytm zrobił z krzywą */

  /* Krzywa zapamiętywania sama w sobie jest tylko wykresem. Ta karta pokazuje,
     co algorytm z niej wyczytał i jak zmienił odstępy — bez tego pętla byłaby
     zamknięta, ale niewidoczna. */
  function renderTuning() {
    var box = U.clear(U.$('#prog-tuning'));
    box.appendChild(U.el('h2', { text: 'Dostrojenie odstępów' }));
    box.appendChild(U.el('p', { class: 'muted', text:
      'Algorytm czyta Twoją krzywą i sam koryguje odstępy. Poniżej 85% trafień w danym '
      + 'przedziale skraca je, powyżej 90% wydłuża. Liczy osobno dla każdej strony karty '
      + 'i tylko z Twoich danych.' }));

    var any = false;
    SRS.SIDES.forEach(function (s) {
      var r = SRS.tuningReport(s);
      if (!r.samples) return;
      any = true;
      var card = U.el('div', { class: 'bigcard' });
      card.appendChild(U.el('div', { class: 'bc-pl', text: r.name + ' — mnożnik ' + r.factor.toFixed(2) + '×' }));
      card.appendChild(U.el('p', { class: 'muted', text:
        'retencja ' + (r.retention === null ? '—' : r.retention + '%')
        + ' z ' + r.samples + ' ' + U.plural(r.samples, 'powtórki', 'powtórek', 'powtórek')
        + (r.updated ? ' · ostatnio ' + r.updated : '') }));
      card.appendChild(U.el('p', { text: r.verdict }));
      box.appendChild(card);
    });
    if (!any) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Na razie brak danych. Mnożnik rusza z 1,00 i zmienia się dopiero po '
        + SRS.TUNE.minSamples + ' powtórkach danej strony — wcześniej korekta '
        + 'opierałaby się na przypadku.' }));
    }
  }

  function errorTable(bucket) {
    var rows = Stats.areas(bucket, 4).slice(0, 8);
    if (!rows.length) return null;
    var table = U.el('table', { class: 'data-table' });
    var caption = U.el('caption', { text: Stats.bucketLabel(bucket) });
    table.appendChild(caption);
    var thead = U.el('thead');
    var hr = U.el('tr');
    [Stats.bucketLabel(bucket), 'Odpowiedzi', 'Pomyłki', 'Błędów'].forEach(function (h) {
      hr.appendChild(U.el('th', { scope: 'col', text: h }));
    });
    thead.appendChild(hr);
    table.appendChild(thead);
    var tbody = U.el('tbody');
    rows.forEach(function (r) {
      var tr = U.el('tr');
      tr.appendChild(U.el('th', { scope: 'row', text: r.label }));
      tr.appendChild(U.el('td', { text: String(r.answers) }));
      tr.appendChild(U.el('td', { text: String(r.wrong) }));
      tr.appendChild(U.el('td', { text: r.rate + '%' }));
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    return table;
  }

  function renderErrorTables() {
    var box = U.clear(U.$('#prog-errors'));
    box.appendChild(U.el('h2', { text: 'Rozkład błędów' }));
    box.appendChild(U.el('p', { class: 'muted', text:
      'Liczymy odpowiedzi i pomyłki osobno. Sama liczba pomyłek premiowałaby obszary, '
      + 'których nie ćwiczysz — dlatego kolumna „Błędów” pokazuje udział, nie sumę.' }));
    var any = false;
    ['category', 'grammar', 'type', 'mode'].forEach(function (bucket) {
      var t = errorTable(bucket);
      if (t) { box.appendChild(t); any = true; }
    });
    if (!any) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Tabele pojawią się, gdy zbierze się po kilka odpowiedzi w poszczególnych obszarach.' }));
    }
  }

  function renderRetention() {
    var box = U.clear(U.$('#prog-retention'));
    box.appendChild(U.el('h2', { text: 'Krzywa zapamiętywania' }));
    box.appendChild(U.el('p', { class: 'muted', text:
      'Po ilu dniach przerwy nadal pamiętasz hasło. To Twoje dane z powtórek, '
      + 'nie krzywa z podręcznika.' }));
    box.appendChild(Stats.retentionChart());
  }

  /* ------------------------------------------- postęp: płynność mówienia */

  /* Skuteczność mówi, czy uczący się trafia. Ta karta mówi, czy trafia
     w rozmowie: mediana czasu reakcji i lista haseł, które zna, ale odtwarza
     wolno. Te hasła nie wypadają z powtórek — wracają częściej. */
  function renderFluency() {
    var box = U.clear(U.$('#prog-fluency'));
    box.appendChild(U.el('h2', { text: 'Płynność i czas reakcji' }));

    var t = Progress.timeStats();
    if (!t.count) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Czas reakcji mierzymy w ćwiczeniach produkcyjnych — od pokazania polecenia '
        + 'do odpowiedzi. Po kilku ćwiczeniach w zakładce „Mówienie po tajsku” '
        + 'pojawi się tutaj Twoja mediana i lista haseł odtwarzanych wolno.' }));
      return;
    }

    var row = U.el('div', { class: 'stat-row' });
    row.appendChild(statBox((t.median / 1000).toFixed(1).replace('.', ',') + ' s', 'mediana reakcji'));
    row.appendChild(statBox(t.count, 'zmierzonych odpowiedzi'));
    row.appendChild(statBox((t.threshold / 1000).toFixed(1).replace('.', ',') + ' s', 'próg powolności'));
    row.appendChild(statBox(t.slow, 'haseł „znam, ale wolno”'));
    box.appendChild(row);

    var modes = Object.keys(t.byMode).filter(function (k) { return t.byMode[k].count >= 3; });
    if (modes.length) {
      var table = U.el('table', { class: 'data-table' });
      table.appendChild(U.el('caption', { text: 'Mediana czasu reakcji w trybach ćwiczeń' }));
      var thead = U.el('thead'), hr = U.el('tr');
      ['Tryb', 'Odpowiedzi', 'Mediana'].forEach(function (h) {
        hr.appendChild(U.el('th', { scope: 'col', text: h }));
      });
      thead.appendChild(hr);
      table.appendChild(thead);
      var tb = U.el('tbody');
      modes.sort(function (a, b) { return t.byMode[b].median - t.byMode[a].median; })
        .forEach(function (k) {
          var tr = U.el('tr');
          tr.appendChild(U.el('th', { scope: 'row', text: Stats.keyLabel('mode', k) }));
          tr.appendChild(U.el('td', { text: String(t.byMode[k].count) }));
          tr.appendChild(U.el('td', { text: (t.byMode[k].median / 1000).toFixed(1).replace('.', ',') + ' s' }));
          tb.appendChild(tr);
        });
      table.appendChild(tb);
      box.appendChild(table);
    }

    var slow = Progress.slowItems(10);
    if (!slow.length) {
      box.appendChild(U.el('p', { class: 'muted', text:
        'Żadne ze znanych Ci haseł nie wypada wyraźnie wolniej od reszty. '
        + 'Odpowiadasz równo — to dobry znak dla rozmowy.' }));
      return;
    }
    box.appendChild(U.el('h3', { text: 'Znasz, ale odtwarzasz wolno' }));
    box.appendChild(U.el('p', { class: 'muted', text:
      'Te hasła trafiasz poprawnie, ale wolniej niż ' + (slow[0].threshold / 1000).toFixed(1).replace('.', ',')
      + ' s. W powtórkach dostają krótszy odstęp i wracają wcześniej niż wynikałoby to z samej poprawności.' }));
    var list = U.el('ul', { class: 'slow-list' });
    slow.forEach(function (item) {
      var rec = DB.any(item.id);
      var li = U.el('li');
      var label = rec ? (rec.polish + ' — ' + (App.settings.hideTones ? U.stripTones(rec.thaiPhonetic) : rec.thaiPhonetic)) : item.id;
      var btn = U.el('button', { class: 'linkish', type: 'button',
        text: label + ' · ' + (item.ms / 1000).toFixed(1).replace('.', ',') + ' s' });
      btn.addEventListener('click', function () {
        if (DB.stub(item.id)) App.openRecord(item.id);
        else U.toast('To hasło pochodzi z dialogu — znajdziesz je w zakładce Dialogi.');
      });
      li.appendChild(btn);
      list.appendChild(li);
    });
    box.appendChild(list);
  }

  function renderAnkiControls() {
    var scope = U.$('#anki-scope');
    var lvlSel = U.$('#anki-level');
    if (!lvlSel.options.length) {
      DB.levels.forEach(function (l) {
        lvlSel.appendChild(U.el('option', { value: l, text: l }));
      });
    }
    lvlSel.hidden = scope.value !== 'level';
  }

  /* ==================================================== EKRAN: USTAWIENIA */
  RENDER.settings = function () {
    var box = U.clear(U.$('#settings-form'));
    box.appendChild(U.el('h2', { text: 'Wygląd i nauka' }));

    function selectField(label, value, options, onChange) {
      var sel = U.el('select');
      options.forEach(function (o) {
        var opt = U.el('option', { value: o[0], text: o[1] });
        if (String(o[0]) === String(value)) opt.selected = true;
        sel.appendChild(opt);
      });
      sel.addEventListener('change', function () { onChange(sel.value); });
      box.appendChild(U.el('label', { class: 'field' }, [U.el('span', { text: label }), sel]));
    }

    selectField('Mówię jako', G.current(),
      [['male', 'mężczyzna'], ['female', 'kobieta']], function (v) {
        G.set(v);
      });
    box.appendChild(U.el('p', { class: 'muted', text:
      'W tajskim cząstka grzecznościowa i zaimek „ja” zależą od płci osoby mówiącej. ' +
      'Wybór zmienia treść na wszystkich ekranach oraz to, co czyta syntezator. ' +
      'Obie formy zobaczysz zawsze w szczegółach hasła.' }));

    selectField('Motyw', App.settings.theme, [['auto', 'Automatyczny'], ['light', 'Jasny'], ['dark', 'Ciemny']], function (v) {
      App.settings.theme = v; saveSettings(); applySettings();
    });
    selectField('Wielkość tekstu', App.settings.scale, [[0.9, 'Mniejszy'], [1, 'Standardowy'], [1.15, 'Większy'], [1.3, 'Bardzo duży']], function (v) {
      App.settings.scale = parseFloat(v); saveSettings(); applySettings();
    });
    selectField('Prędkość odtwarzania', App.settings.rate, [[0.5, '0,5x'], [0.75, '0,75x'], [1, '1x'], [1.25, '1,25x']], function (v) {
      App.settings.rate = parseFloat(v); saveSettings(); Player.setRate(v);
    });
    selectField('Poziom w ćwiczeniach', App.settings.practiceLevel,
      [['', 'Wszystkie']].concat(DB.levels.map(function (l) { return [l, l]; })), function (v) {
        App.settings.practiceLevel = v; saveSettings();
      });

    /* Limit czasu w ćwiczeniach liczbowych i w drylu odruchu.

       Te ćwiczenia mierzą szybkość, więc limit jest ich treścią, a nie ozdobą.
       To jednak nie znaczy, że ma być nieusuwalny. Ktoś, kto obsługuje telefon
       jedną ręką, korzysta z czytnika ekranu albo ma ograniczenie ruchowe,
       potrzebuje na samo wpisanie odpowiedzi więcej czasu niż wynosi całe okno
       — i wtedy ćwiczenie nie mierzy już percepcji, tylko sprawność motoryczną.
       To jest wymóg dostępności, nie ustępstwo.

       Wyłączenie limitu NIE unieważnia pomiaru: czas nadal jest mierzony
       i nadal liczy się do statystyk, przestaje tylko odcinać odpowiedź.
       Mierzyć da się bez presji; karać bez pomiaru już nie. */
    selectField('Limit czasu w ćwiczeniach liczbowych i drylu',
      App.settings.timeLimit,
      Numbers.limitChoices().map(function (c) { return [c.id, c.label]; }),
      function (v) {
        App.settings.timeLimit = v; saveSettings();
        U.toast(v === 'off' ? 'Limit czasu wyłączony. Czas nadal jest mierzony.'
                            : 'Limit czasu: ' + v + '.');
      });
    box.appendChild(U.el('p', { class: 'muted', text:
      'Dotyczy wszystkich ćwiczeń z odliczaniem: sześciu trybów liczbowych '
      + 'i drylu odruchu. Wyłączenie limitu nie kasuje pomiaru czasu — mediana '
      + 'i próg opanowania liczą się dalej, znika tylko odcinanie odpowiedzi.' }));

    /* Cel dnia w minutach, nie w odpowiedziach.

       Liczba odpowiedzi była celem, którym uczący się nie dysponuje — nie
       decyduje, ile zdąży, tylko ile ma czasu. Była też celem, który najtaniej
       zrobić najłatwiejszym ćwiczeniem, czyli tym najmniej potrzebnym.
       Uzasadnienie w całości w js/goals.js. */
    selectField('Cel dnia', Goals.get().minutes,
      Goals.MINUTES.map(function (m) { return [m, m + ' minut nauki']; }), function (v) {
        Goals.set({ minutes: parseInt(v, 10) });
        U.toast('Cel dnia: ' + v + ' minut.');
      });

    /* Cel kategorialny — jedna sytuacja na tydzień. */
    var catNow = Goals.category();
    var catOptions = [['', 'Brak celu tygodnia']];
    if (Coverage.ready()) {
      Coverage.solid().forEach(function (c) {
        catOptions.push([c.name, c.name + ' — teraz ' + Math.round(c.coverage * 100) + '%']);
      });
    }
    selectField('Cel tygodnia (kategoria)', catNow ? catNow.name : '', catOptions, function (v) {
      Goals.setCategory(v || null);
      U.toast(v ? 'Cel tygodnia: domykam „' + v + '”.' : 'Cel tygodnia usunięty.');
      RENDER.settings();
    });
    if (!Coverage.ready()) {
      box.appendChild(U.el('p', { class: 'muted small', text:
        'Lista kategorii pojawi się po wczytaniu danych pokrycia — wejdź na ekran „Droga do celu”.' }));
    }

    var toneSwitch = U.el('input', { type: 'checkbox' });
    toneSwitch.checked = !!App.settings.hideTones;
    toneSwitch.addEventListener('change', function () {
      App.settings.hideTones = toneSwitch.checked;
      saveSettings(); applySettings();
      U.toast(toneSwitch.checked ? 'Znaki tonów ukryte.' : 'Znaki tonów widoczne.');
    });
    /* Etykieta musi być elementem <label>, żeby pole miało dostępną nazwę
       i żeby dało się je przełączyć kliknięciem w tekst. */
    box.appendChild(U.el('label', { class: 'switch' }, [
      U.el('span', { text: 'Ukryj znaki tonów (dla początkujących)' }), toneSwitch
    ]));

    /* --- odsłuch i realizm --------------------------------------------

       Syntezator mówi formą słownikową: wyraźnie, wolno, w ciszy. Prawdziwa
       rozmowa jest szybsza, zredukowana i prawie zawsze w hałasie. Te trzy
       ustawienia decydują, jak daleko od czystego wzorca chcemy trenować. */
    var lab = U.el('div', { class: 'card' });
    lab.appendChild(U.el('h2', { text: 'Odsłuch i realizm' }));
    lab.appendChild(U.el('p', { class: 'muted', text:
      'Wzorzec słownikowy jest dobry na początek i bezużyteczny w rozmowie. ' +
      'Tutaj ustawiasz, ile realizmu ma dokładać aplikacja.' }));

    /* tempo */
    lab.appendChild(U.el('h3', { text: 'Tempo domyślne' }));
    var tempoRow = U.el('div', { class: 'chip-row', role: 'group',
      'aria-label': 'Tempo odtwarzania' });
    var tempoHint = U.el('p', { class: 'muted', text: Player.tempoDef(App.settings.tempo).hint });
    Player.tempos().forEach(function (t) {
      var chip = U.el('button', {
        class: 'chip', type: 'button',
        'aria-pressed': App.settings.tempo === t.id ? 'true' : 'false',
        text: String(t.factor).replace('.', ',') + 'x ' + t.label
      });
      chip.addEventListener('click', function () {
        App.settings.tempo = t.id;
        saveSettings(); applySettings();
        U.$$('button', tempoRow).forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        chip.setAttribute('aria-pressed', 'true');
        tempoHint.textContent = t.hint;
      });
      tempoRow.appendChild(chip);
    });
    lab.appendChild(tempoRow);
    lab.appendChild(tempoHint);

    /* tryb potoczny */
    var collSwitch = U.el('input', { type: 'checkbox' });
    collSwitch.checked = !!App.settings.colloquial;
    collSwitch.addEventListener('change', function () {
      App.settings.colloquial = collSwitch.checked;
      saveSettings(); applySettings();
      U.toast(collSwitch.checked
        ? 'Tryb potoczny włączony — syntezator dostaje zapis zredukowany.'
        : 'Tryb potoczny wyłączony — forma słownikowa.');
    });
    lab.appendChild(U.el('label', { class: 'switch' }, [
      U.el('span', { text: 'Tryb potoczny (mowa połączona)' }), collSwitch
    ]));

    var showSwitch = U.el('input', { type: 'checkbox' });
    showSwitch.checked = App.settings.showColloquial !== false;
    showSwitch.addEventListener('change', function () {
      App.settings.showColloquial = showSwitch.checked;
      saveSettings(); applySettings();
    });
    lab.appendChild(U.el('label', { class: 'switch' }, [
      U.el('span', { text: 'Pokazuj zapis potoczny obok słownikowego' }), showSwitch
    ]));
    lab.appendChild(U.el('p', { class: 'muted', text:
      'Wariant potoczny ma materiał kursu i wszystkie dialogi (' + COLLOQUIAL_NOTE + '). ' +
      'Poza tym zakresem odtwarzana jest forma słownikowa.' }));

    /* hałas */
    lab.appendChild(U.el('h3', { text: 'Poziom hałasu' }));
    var noiseRow = U.el('div', { class: 'chip-row', role: 'group', 'aria-label': 'Poziom hałasu w tle' });
    [
      { v: 0, t: 'cisza' }, { v: 1, t: 'lekki' }, { v: 2, t: 'średni' }, { v: 3, t: 'trudny' }
    ].forEach(function (opt) {
      var chip = U.el('button', {
        class: 'chip', type: 'button', text: opt.t,
        'aria-pressed': (parseInt(App.settings.noiseLevel, 10) || 0) === opt.v ? 'true' : 'false'
      });
      chip.addEventListener('click', function () {
        App.settings.noiseLevel = opt.v;
        saveSettings(); applySettings();
        U.$$('button', noiseRow).forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        chip.setAttribute('aria-pressed', 'true');
      });
      noiseRow.appendChild(chip);
    });
    lab.appendChild(noiseRow);

    var kindSel = U.el('select');
    var kinds = (global.DSP && DSP.supported()) ? DSP.noiseKinds() : [];
    kinds.forEach(function (k) {
      var o = U.el('option', { value: k.id, text: k.label });
      if (App.settings.noiseKind === k.id) o.selected = true;
      kindSel.appendChild(o);
    });
    kindSel.addEventListener('change', function () {
      App.settings.noiseKind = kindSel.value;
      saveSettings(); applySettings();
    });
    lab.appendChild(U.el('label', { class: 'field' }, [
      U.el('span', { text: 'Rodzaj tła' }), kindSel
    ]));

    var roomSel = U.el('select');
    var rooms = [{ id: '', label: 'bez pogłosu' }].concat(
      (global.DSP && DSP.supported()) ? DSP.roomKinds() : []);
    rooms.forEach(function (r) {
      var o = U.el('option', { value: r.id, text: r.label });
      if ((App.settings.room || '') === r.id) o.selected = true;
      roomSel.appendChild(o);
    });
    roomSel.addEventListener('change', function () {
      App.settings.room = roomSel.value;
      saveSettings(); applySettings();
    });
    lab.appendChild(U.el('label', { class: 'field' }, [
      U.el('span', { text: 'Pogłos pomieszczenia' }), roomSel
    ]));

    var phoneSwitch = U.el('input', { type: 'checkbox' });
    phoneSwitch.checked = !!App.settings.phone;
    phoneSwitch.addEventListener('change', function () {
      App.settings.phone = phoneSwitch.checked;
      saveSettings(); applySettings();
    });
    lab.appendChild(U.el('label', { class: 'switch' }, [
      U.el('span', { text: 'Pasmo telefoniczne (300-3400 Hz)' }), phoneSwitch
    ]));

    var probe = Capture.probe();
    lab.appendChild(U.el('p', { class: 'muted', text:
      probe.synthCapture
        ? 'Ta przeglądarka pozwala przechwycić wyjście syntezatora — pogłos i pasmo ' +
          'telefoniczne działają także na mowie.'
        : 'Wyjścia syntezatora nie da się przechwycić w żadnej przeglądarce, więc pogłos ' +
          'i pasmo telefoniczne działają na tle, a nie na samym głosie. Na nagraniach ' +
          'lektorskich (katalog audio/) działają na wszystkim. Szczegóły: ' +
          'docs/ograniczenia-tts.md.' }));

    var test = U.el('button', { class: 'btn ghost', type: 'button', text: 'Posłuchaj tła' });
    test.addEventListener('click', function () {
      if (!App.settings.noiseLevel) { U.toast('Poziom hałasu jest ustawiony na ciszę.'); return; }
      Player.startAmbience();
      setTimeout(function () { Player.stopAmbience(); }, 3500);
    });
    var cacheBtn = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wyczyść pamięć dźwięku' });
    var cacheInfo = U.el('p', { class: 'muted', text: cacheLabel() });
    cacheBtn.addEventListener('click', function () {
      if (global.DSP) DSP.cache.clear();
      cacheInfo.textContent = cacheLabel();
      U.toast('Pamięć przetworzonych dźwięków wyczyszczona.');
    });
    lab.appendChild(U.el('div', { class: 'btn-row' }, [test, cacheBtn]));
    lab.appendChild(cacheInfo);
    box.appendChild(lab);

    /* --- zakres głosu użytkownika (ocena wymowy) --- */
    var range = ToneScore.voiceRange();
    var vbox = U.el('div');
    vbox.appendChild(U.el('h2', { text: 'Twój zakres głosu' }));
    if (range.personalised) {
      vbox.appendChild(U.el('p', { class: 'muted', text:
        'Ocena wymowy przelicza herce na skalę względną Twojego głosu. Środek zakresu: '
        + Math.round(range.median) + ' Hz, rozpiętość ±'
        + String(Math.round(range.halfSpan * 10) / 10).replace('.', ',') + ' półtonu. '
        + 'Policzone z ' + range.samples + ' '
        + U.plural(range.samples, 'nagrania', 'nagrań', 'nagrań') + '.' }));
    } else {
      vbox.appendChild(U.el('p', { class: 'muted', text:
        'Aplikacja nie zna jeszcze Twojego zakresu głosu — zbiera go z nagrań w ćwiczeniach '
        + 'wymowy. Do trzeciego nagrania skala liczy się z pojedynczego nagrania, więc ocena '
        + 'jest zgrubna. Zapisujemy wyłącznie trzy liczby na nagranie (mediana i granice '
        + 'zakresu), nigdy samego dźwięku.' }));
    }
    var vreset = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wyczyść zakres głosu' });
    vreset.addEventListener('click', function () {
      ToneScore.resetVoice();
      U.toast('Zakres głosu wyczyszczony — policzy się od nowa przy kolejnych nagraniach.');
      RENDER.settings();
    });
    vbox.appendChild(U.el('div', { class: 'btn-row' }, [vreset]));
    box.appendChild(vbox);

    /* --- przypomnienia --- */
    var nbox = U.el('div');
    nbox.appendChild(U.el('h2', { text: 'Przypomnienia' }));
    var perm = Goals.permission();

    if (perm === 'unsupported') {
      nbox.appendChild(U.el('p', { class: 'muted', text:
        'Ta przeglądarka nie obsługuje powiadomień. Wszystko inne działa normalnie.' }));
    } else {
      nbox.appendChild(U.el('p', { class: 'muted', text:
        'Przypomnienia są opcjonalne i domyślnie wyłączone. Aplikacja nie ma serwera, '
        + 'więc powiadomienie pojawi się tylko wtedy, gdy karta z aplikacją jest otwarta — '
        + 'przy zamkniętej przeglądarce nic nie przyjdzie. Wolimy to powiedzieć wprost, '
        + 'niż obiecać coś, czego nie da się dotrzymać.' }));

      var g = Goals.get();
      var notifySwitch = U.el('input', { type: 'checkbox' });
      notifySwitch.checked = !!g.notify && perm === 'granted';
      notifySwitch.addEventListener('change', function () {
        if (!notifySwitch.checked) {
          Goals.set({ notify: false });
          U.toast('Przypomnienia wyłączone.');
          RENDER.settings();
          return;
        }
        Goals.requestPermission().then(function (result) {
          if (result === 'granted') {
            Goals.set({ notify: true });
            U.toast('Przypomnienia włączone.');
          } else {
            Goals.set({ notify: false });
            U.toast('Przeglądarka nie zgodziła się na powiadomienia.');
          }
          RENDER.settings();
        });
      });
      nbox.appendChild(U.el('label', { class: 'switch' }, [
        U.el('span', { text: 'Przypomnij o celu dnia' }), notifySwitch
      ]));

      var timeInput = U.el('input', { type: 'time', value: g.notifyAt });
      timeInput.addEventListener('change', function () {
        Goals.set({ notifyAt: timeInput.value || '19:00' });
      });
      nbox.appendChild(U.el('label', { class: 'field' }, [
        U.el('span', { text: 'Pora przypomnienia' }), timeInput
      ]));

      if (perm === 'denied') {
        nbox.appendChild(U.el('p', { class: 'muted small', text:
          'Powiadomienia są zablokowane w ustawieniach przeglądarki dla tej strony. '
          + 'Aplikacja nie może tego zmienić — trzeba odblokować je po stronie przeglądarki.' }));
      }
      nbox.appendChild(U.el('p', { class: 'muted small', text:
        'Przypomnienie leci raz dziennie i tylko wtedy, gdy cel dnia nie jest jeszcze zrobiony.' }));
    }
    box.appendChild(nbox);

    /* --- migracja postępu po przebudowie ścieżki --- */
    var mig = (global.ProgressMigration && ProgressMigration.report()) || null;
    if (mig) {
      var mbox = U.el('div');
      mbox.appendChild(U.el('h2', { text: 'Postęp a przebudowa kursu' }));
      mbox.appendChild(U.el('p', { class: 'muted', text: ProgressMigration.summary() }));
      var info = ProgressMigration.backupInfo();
      if (info) {
        mbox.appendChild(U.el('p', { class: 'muted', text:
          'Kopia zapasowa sprzed migracji jest zachowana (' +
          info.lessons + ' ' + U.plural(info.lessons, 'lekcja', 'lekcje', 'lekcji') +
          ', zapis z ' + String(info.savedAt).slice(0, 10) + '). ' +
          'Cofnięcie przywraca stan sprzed aktualizacji; migracja wykona się ' +
          'wtedy ponownie przy następnym uruchomieniu.' }));
        var undo = U.el('button', { class: 'btn ghost', type: 'button',
                                    text: 'Cofnij migracj\u0119 postępu' });
        undo.addEventListener('click', function () {
          if (ProgressMigration.restore()) {
            U.toast('Przywrócono postęp sprzed migracji.');
            RENDER.settings();
          } else {
            U.toast('Nie znaleziono kopii zapasowej.');
          }
        });
        mbox.appendChild(U.el('div', { class: 'btn-row' }, [undo]));
      } else {
        mbox.appendChild(U.el('p', { class: 'muted', text:
          'Kopii zapasowej nie ma — nie było czego przenosić.' }));
      }
      box.appendChild(mbox);
    }

    var voice = U.clear(U.$('#voice-info'));
    voice.appendChild(U.el('h2', { text: 'Głos tajski' }));
    voice.appendChild(U.el('p', { class: 'muted', text: Speech.voiceLabel() }));
    if (!Speech.hasThaiVoice()) {
      voice.appendChild(U.el('p', { class: 'muted', text: 'iPhone: Ustawienia → Dostępność → Treść mówiona → Głosy → Tajski. Android: Ustawienia → System → Języki → Zamiana tekstu na mowę.' }));
    }
    var test = U.el('button', { class: 'btn ghost', type: 'button', text: 'Sprawdź głos' });
    test.addEventListener('click', function () {
      var sample = DB.records[0] || DB.index[0];
      if (sample) Player.play(sample, { btn: test });
    });
    voice.appendChild(U.el('div', { class: 'btn-row' }, [test]));
  };

  /* ------------------------------------------------------------ start */
  function refreshGenderChip() {
    var node = U.$('#btn-gender-label');
    if (node) node.textContent = G.label();
    var btn = U.$('#btn-gender');
    if (btn) {
      btn.setAttribute('data-gender', G.current());
      btn.setAttribute('title', 'Mówię jako: ' + G.label() + ' — dotknij, aby zmienić');
      btn.setAttribute('aria-label', 'Mówię jako: ' + G.label() + '. Dotknij, aby zmienić.');
    }
  }
  App.refreshGenderChip = refreshGenderChip;

  /* Przy pierwszym uruchomieniu trzeba zapytać, zanim uczący się zobaczy
     pierwsze zdanie — inaczej przez chwilę uczy się formy, której nie użyje. */
  function askGender() {
    var dlg = U.$('#gender-ask');
    if (!dlg) return;
    dlg.hidden = false;
    U.$$('[data-gender]', dlg).forEach(function (btn) {
      btn.addEventListener('click', function () {
        G.set(btn.getAttribute('data-gender'));
        dlg.hidden = true;
        U.toast('Ustawiono: mówię jako ' + G.label() + '. Zmienisz to w Ustawieniach.');
      });
    });
    var first = U.$('[data-gender]', dlg);
    if (first) first.focus();
  }

  function bindStatic() {
    U.$('#btn-gender').addEventListener('click', function () {
      G.set(G.current() === 'female' ? 'male' : 'female');
      U.toast('Mówię jako: ' + G.label() + '.');
    });
    U.$('#btn-theme').addEventListener('click', function () {
      var order = ['auto', 'light', 'dark'];
      App.settings.theme = order[(order.indexOf(App.settings.theme) + 1) % 3];
      saveSettings(); applySettings();
      U.toast('Motyw: ' + { auto: 'automatyczny', light: 'jasny', dark: 'ciemny' }[App.settings.theme]);
    });
    U.$('#btn-stop-audio').addEventListener('click', function () { Player.stop(); Quiz.stopRecording(); });
    U.$('#sheet-close').addEventListener('click', closeSheet);
    U.$('#sheet').addEventListener('click', function (e) { if (e.target.id === 'sheet') closeSheet(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !U.$('#sheet').hidden) closeSheet();
    });

    U.$('#dict-q').addEventListener('input', U.debounce(function () { runSearch(true); }, 220));
    ['#f-level', '#f-cat', '#f-type', '#f-sort'].forEach(function (sel) {
      U.$(sel).addEventListener('change', function () { runSearch(true); });
    });
    U.$('#f-fav').addEventListener('click', function () {
      var on = this.getAttribute('aria-pressed') === 'true';
      this.setAttribute('aria-pressed', String(!on));
      runSearch(true);
    });
    U.$('#dict-more').addEventListener('click', function () { dictState.page += 1; runSearch(false); });

    U.$$('#dict-presets .chip').forEach(function (btn) {
      btn.addEventListener('click', function () {
        App.dictPreset(btn.getAttribute('data-preset'));
      });
    });

    /* Napisy na przyciskach trybu bierzemy z rejestru (U.EX), a nie z HTML-a.
       Znacznik zostaje w index.html, bo bez JS-a ma się co pokazać, ale to
       rejestr rozstrzyga — dzięki temu nazwa trybu na ekranie NIE MOŻE się
       rozjechać z tą samą nazwą w statystyce ani w planie naprawczym. */
    U.$$('[data-gram]').forEach(function (btn) {
      btn.textContent = U.exLabel(btn.getAttribute('data-gram'));
      btn.addEventListener('click', function () {
        U.$$('[data-gram]').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        btn.setAttribute('aria-pressed', 'true');
        grammarMode = btn.getAttribute('data-gram');
        renderGrammar();
      });
    });

    U.$$('[data-listen]').forEach(function (btn) {
      btn.textContent = U.exLabel(btn.getAttribute('data-listen'));
      btn.addEventListener('click', function () {
        U.$$('[data-listen]').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        btn.setAttribute('aria-pressed', 'true');
        Quiz.mode = btn.getAttribute('data-listen');
        Quiz.renderListen(U.$('#listen-area'));
      });
    });

    U.$('#dlg-select').addEventListener('change', renderDialogue);
    ['#dlg-hide', '#dlg-role'].forEach(function (sel) {
      U.$(sel).addEventListener('click', function () {
        var on = this.getAttribute('aria-pressed') === 'true';
        this.setAttribute('aria-pressed', String(!on));
        renderDialogue();
      });
    });

    U.$('#course-level').addEventListener('change', function () {
      courseState.level = this.value;
      RENDER.course();
    });
    U.$('#course-jump').addEventListener('click', function () {
      var next = Course.next();
      if (!next) { U.toast('Wszystkie lekcje są już zaliczone.'); return; }
      courseState.level = '';
      U.$('#course-level').value = '';
      RENDER.course();
      var node = U.$('[data-lesson="' + next.id + '"]');
      if (node) { node.scrollIntoView({ block: 'center' }); node.focus(); }
    });

    U.$('#anki-scope').addEventListener('change', function () {
      U.$('#anki-level').hidden = this.value !== 'level';
    });
    U.$('#btn-anki').addEventListener('click', function () {
      var btn = this;
      var scope = U.$('#anki-scope').value;
      var level = U.$('#anki-level').value;
      var status = U.$('#anki-status');
      btn.disabled = true;
      status.textContent = 'Przygotowuję plik — dociągam potrzebne hasła…';
      Stats.exportCsv(scope, level).then(function (n) {
        btn.disabled = false;
        status.textContent = n
          ? 'Zapisano plik CSV z ' + n + ' ' + U.plural(n, 'hasłem', 'hasłami', 'hasłami') + '.'
          : 'Nie było czego wyeksportować.';
      })['catch'](function (err) {
        btn.disabled = false;
        status.textContent = 'Nie udało się przygotować pliku: ' + err.message;
      });
    });

    U.$('#btn-export').addEventListener('click', function () {
      Progress.download();
      U.toast('Zapisano plik z kopią postępu.');
    });
    U.$('#import-file').addEventListener('change', function (e) {
      var file = e.target.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function () {
        try {
          Progress.importData(JSON.parse(reader.result));
          applySettings();
          U.toast('Przywrócono postęp z pliku.');
          App.go('progress');
        } catch (err) {
          U.toast('Nie udało się wczytać pliku: ' + err.message);
        }
      };
      reader.readAsText(file);
      e.target.value = '';
    });

    U.$('#btn-clear').addEventListener('click', function () {
      if (!confirm('Usunąć cały postęp i ustawienia?')) return;
      U.store.keys().forEach(U.store.remove);
      U.toast('Wyczyszczono. Aplikacja uruchomi się od nowa.');
      setTimeout(function () { location.reload(); }, 1200);
    });

    window.addEventListener('hashchange', function () {
      var id = location.hash.replace('#', '');
      if (id && id !== App.screen) App.go(id);
    });

    ['click', 'keydown', 'touchstart'].forEach(function (evt) {
      document.addEventListener(evt, function once() {
        Speech.unlock();
        document.removeEventListener(evt, once);
      }, { passive: true });
    });

    ['click', 'keydown', 'input'].forEach(function (evt) {
      document.addEventListener(evt, U.debounce(function () { Progress.tick(); }, 900), { passive: true });
    });

    /* Zegar minutowy. Robi trzy rzeczy i nic poza nimi:
         - sprawdza, czy wypadła pora przypomnienia,
         - dopisuje zużyty czas do trwającej sesji dnia,
         - odświeża licznik na ekranie sesji, żeby „zostało X minut” nie stało
           w miejscu, gdy uczący się właśnie się zastanawia nad odpowiedzią. */
    setInterval(function () {
      try { Goals.checkReminder(); } catch (e) {}
      if (Session.state && !Session.state.finished && Session.state.resumedAt) {
        Session.tick();
        if (App.screen === 'session') {
          var status = U.$('#session-status');
          var prog = Session.progress();
          if (status && prog) {
            status.textContent = 'Krok ' + Math.min(prog.done + 1, prog.steps) + ' z ' + prog.steps
              + ' · ' + Math.round(prog.spent / 60) + ' z ' + Session.state.minutes + ' min'
              + (prog.overtime ? ' (ponad plan)' : '');
          }
        }
      }
    }, 60000);

    /* Wyjście z aplikacji w trakcie sesji: zamykamy licznik czasu, żeby noc
       przy otwartej karcie nie została policzona jako nauka. */
    window.addEventListener('pagehide', function () { Session.pause(); });
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) Session.pause();
      else if (App.screen === 'session' && Session.resumable()) Session.resume();
    });
  }

  function start() {
    if (App.started) return;   /* zabezpieczenie przed podwójną inicjalizacją */
    App.started = true;
    App.settings = Object.assign({}, DEFAULTS, U.store.get('settings', {}));
    G.load();
    G.onChange(function () {
      refreshGenderChip();
      Player.stop();
      /* Ekrany z zapamiętanym stanem trzeba zbudować od nowa, bo trzymają
         gotowe węzły z fonetyką jednej formy. */
      if (dictState.built) runSearch(false);
      RENDER[App.screen] && RENDER[App.screen]();
      if (!U.$('#sheet').hidden) closeSheet();
    });
    Progress.load();
    SRS.load();
    Session.load();
    /* Sufit kolejki powtórek czyta Progress.data.goal. Cel jest teraz czasowy,
       więc przy starcie przeliczamy jedno na drugie — inaczej kartoteka
       pracowałaby na wartości sprzed zmiany celu. */
    Goals.set({});
    applySettings();
    buildNav();
    bindStatic();
    watchLateTables();
    refreshGenderChip();

    U.$('#db-status').textContent = 'Ładowanie bazy…';

    DB.load().then(function () {
      Search.build(DB.index);
      refreshStatus();

      /* Migracja postępu po przebudowie ścieżki. Musi pójść PRZED pierwszym
         renderem, żeby użytkownik od razu zobaczył kurs w miejscu, w którym
         go zostawił, i nie zdążył kliknąć w lekcję, która za chwilę zmieni
         status. Wykonuje się raz, po cichu — szczegóły w progress-migration.js. */
      if (global.ProgressMigration) {
        ProgressMigration.setMap(DB.progressMigration);
        try { ProgressMigration.run(); } catch (e) {}
        /* Druga, niezależna migracja: identyfikatory ekranów po przebudowie
           nawigacji w sesji VI. Musi pójść przed pierwszym renderem z tego
           samego powodu co tamta — zapisany plan sesji wskazuje ekran. */
        try { ProgressMigration.runScreens(); } catch (e) {}
      }

      /* Test poziomujący pokazujemy raz — zanim uczący się w ogóle zobaczy
         kurs. Bez niego nie wiadomo, od której lekcji zacząć. */
      var startScreen = location.hash.replace('#', '') || (Progress.needsPlacement() ? 'placement' : 'today');
      App.go(startScreen);
      if (!G.isSet()) askGender();

      /* Reszta indeksu (A2, B1, B2) rusza natychmiast po pierwszym renderze,
         w tle. Nie blokuje startu, a do czasu, aż użytkownik wejdzie do
         słownika, zwykle już jest. Zdarzenie odświeża licznik i widok. */
      if (!DB.indexComplete) {
        DB.ensureIndex().then(function () {
          refreshStatus();
          if (App.screen === 'dict') RENDER.dict && RENDER.dict();
        });
      }

      /* Nic więcej nie dociągamy z góry. Pliki poziomów pobierają się dopiero
         wtedy, gdy któryś ekran ich potrzebuje — patrz dataNeedFor(). */
      if (DB.errors.length) {
        U.toast('Nie udało się wczytać ' + DB.errors.length + ' pliku(ów) danych. Reszta działa normalnie.');
      }
    })['catch'](function (err) {
      /* Rozdzielamy dwie zupełnie różne awarie. Jeśli baza się wczytała,
         a wywrócił się dopiero pierwszy render, to wina NIE leży po stronie
         katalogu `data/` — wskazywanie go wysyłało szukającego w złe miejsce.
         W tym drugim przypadku aplikacja ma jeszcze szansę stanąć: kasujemy
         zapisany postęp z pamięci przeglądarki i proponujemy start od zera,
         bo najczęstszą przyczyną jest właśnie uszkodzona kopia postępu. */
      var dataLoaded = global.DB && DB.ready;
      U.$('#db-status').textContent = dataLoaded
        ? 'Błąd uruchamiania aplikacji.' : 'Błąd ładowania danych.';
      var box = U.$('#today-recommend');
      if (!dataLoaded) {
        box.textContent = 'Nie udało się wczytać bazy: ' + err.message
          + ' — sprawdź, czy katalog data/ jest kompletny.';
        return;
      }
      U.clear(box);
      box.appendChild(U.el('p', { text: 'Baza wczytała się poprawnie, ale nie udało się '
        + 'zbudować pierwszego ekranu: ' + err.message
        + '. Najczęstsza przyczyna to uszkodzony zapis postępu w tej przeglądarce.' }));
      var reset = U.el('button', { class: 'btn', type: 'button',
        text: 'Zacznij od nowa (kasuje zapisany postęp)' });
      reset.addEventListener('click', function () {
        try { U.store.set('progress', null); } catch (e) {}
        location.reload();
      });
      box.appendChild(reset);
    });

    /* Service worker działa wyłącznie przez http(s). Przy otwarciu z dysku
       pomijamy rejestrację — aplikacja i tak ma wtedy wszystkie dane lokalnie. */
    if ('serviceWorker' in navigator && !DB.localMode) {
      window.addEventListener('load', function () {
        navigator.serviceWorker.register('service-worker.js').catch(function () {});
      });
    }
  }

  document.addEventListener('DOMContentLoaded', start);
  global.App = App;
})(window);
