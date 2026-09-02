/* Thai All-in-One — ładowanie danych.

   Zasada nadrzędna: pole ttsThai NIGDY nie trafia do obiektów krążących po
   aplikacji. Przy wczytaniu jest wycinane do prywatnej mapy, a w rekordzie
   zostaje wyłącznie nieczytelny token (ttsKey). Dzięki temu żaden ekran,
   eksport ani wyszukiwarka nie mają fizycznej możliwości pokazać pisma
   tajskiego.

   ŁADOWANIE NA ŻĄDANIE
   --------------------
   Pełne pliki poziomów ważą ponad 21 MB. Wczytywanie ich przy starcie —
   nawet w tle — zajmowało na wolnym telefonie kilka sekund pracy procesora
   i przycinało interfejs w trakcie pierwszych kliknięć.

   Przy starcie wczytujemy więc wyłącznie:
     - manifest,
     - pliki pomocnicze (kategorie, gramatyka, wymowa, metadane, klasyfikatory),
     - ścieżkę nauki (lekcje),
     - lekki indeks wyszukiwania: identyfikator, znaczenie, fonetyka, poziom,
       kategoria, typ, częstotliwość, trudność i nazwa pliku źródłowego.

   Indeks wystarcza, żeby wyszukiwarka, listy, filtry, mapa kursu i statystyki
   postępu działały od pierwszej sekundy. Pełny rekord — z przykładami,
   uwagami i danymi dla syntezatora mowy — dociąga się dopiero wtedy, gdy
   użytkownik naprawdę go potrzebuje: otworzy hasło, wejdzie w lekcję,
   uruchomi ćwiczenie albo powtórkę.

   Działa tak samo przez serwer i po otwarciu index.html z dysku (file://),
   bo w trybie file:// zamiast fetch() używamy bliźniaczych plików data/*.js. */
(function (global) {
  'use strict';

  var voiceMap = new Map();   // token -> tekst dla syntezatora mowy
  var counter = 0;

  function stash(text) {
    if (!text) return null;
    var token = 'v' + (++counter);
    voiceMap.set(token, text);
    return token;
  }

  /* Rekurencyjnie usuwa ttsThai z dowolnie zagnieżdżonej struktury. */
  function sanitize(node) {
    if (Array.isArray(node)) { node.forEach(sanitize); return node; }
    if (!node || typeof node !== 'object') return node;
    if (Object.prototype.hasOwnProperty.call(node, 'ttsThai')) {
      var token = stash(node.ttsThai);
      delete node.ttsThai;
      if (token) node.ttsKey = token;
    }
    Object.keys(node).forEach(function (k) { sanitize(node[k]); });
    return node;
  }

  var SUPPORT = ['categories.json', 'grammar.json', 'pronunciation.json',
                 'metadata.json', 'classifiers.json', 'lessons.json',
                 'module-zero.json',
                 /* Skład lekcji STAREJ ścieżki. Potrzebny wyłącznie przy
                    pierwszym uruchomieniu po przebudowie — ale musi być tutaj,
                    bo w trybie file:// nie ma jak dociągnąć pliku na żądanie. */
                 'progress-migration.json'];

  var DB = {
    ready: false,        // pierwszy ekran ma z czego się wyrenderować
    complete: false,     // wszystkie pliki poziomów są w pamięci
    manifest: null,
    metadata: null,
    records: [],         // pełne rekordy — tylko te z wczytanych plików
    byId: new Map(),
    index: [],           // lekkie wpisy dla WSZYSTKICH haseł
    stubById: new Map(),
    dialogues: [],
    scenes: [],          // sceny — dialogi połączone w jedną sytuację
    blocks: [],          // bloki 3-5 minut do słuchania ekstensywnego
    sceneById: new Map(),
    blockById: new Map(),
    sceneQuestions: new Map(),   // id pytania -> pytanie (bloki odwołują się po id)
    comprehension: null,         // luki na słuch i zdania z nieznanym słowem
    numbers: null,               // moduł liczbowy: atomy, punkty kontrolne, sceny
    rescue: null,                // formuły ratujące rozmowę i zadania drylu odruchu
    exams: null,                 // egzaminy poziomowe: progi, limity czasu, zestawy zadań
    checkpoints: null,           // próbki kontrolne co 20 lekcji
    progressMigration: null,     // mapa starej ścieżki dla migracji postępu
    dialogueIndex: [],   // lekkie wpisy dla wszystkich dialogów
    dialogueStubById: new Map(),
    lessons: [],
    chapters: [],        // rozdziały ścieżki — kilkanaście lekcji z kamieniem milowym
    moduleZero: null,    // Moduł 0 — trening percepcyjny (lekcje, bodźce, diagnoza)
    grammar: [],
    grammarListening: [],
    grammarTransform: [],
    grammarTransformKinds: [],
    grammarAxes: {},
    particles: [],
    particleExercises: [],
    categories: [],
    pronunciation: null,
    classifiers: [],
    levels: [],
    types: [],
    catNames: [],
    countByLevel: {},
    countByCat: {},
    indexTypes: {},
    errors: [],          // pliki, których nie udało się wczytać
    loadedFiles: [],
    indexParts: [],      // pozostałe części indeksu do dociągnięcia w tle
    indexTotal: 0,       // ile haseł ma indeks po sklejeniu wszystkich części
    indexComplete: false,
    indexFiles: [],      // nazwy plików słownikowych w kolejności z indeksu
    dialogueFiles: []
  };

  /* Otwarcie index.html prosto z dysku (file://) blokuje fetch, ale nie blokuje
     znacznika <script>. W tym trybie sięgamy po bliźniacze pliki data/*.js,
     generowane przez tools/build-offline-data.py. */
  DB.localMode = location.protocol === 'file:';

  function loadScript(file) {
    return new Promise(function (resolve, reject) {
      var jsFile = file.replace(/\.json$/, '.js');
      var tag = document.createElement('script');
      tag.src = 'data/' + jsFile;
      tag.onload = function () {
        var store = window.__THAI_DATA__ || {};
        if (!store[file]) {
          reject(new Error('Plik data/' + jsFile + ' nie zawiera danych. Uruchom: python3 tools/build-offline-data.py'));
          return;
        }
        resolve(store[file]);
      };
      tag.onerror = function () {
        reject(new Error('Brak pliku data/' + jsFile + '. Uruchom: python3 tools/build-offline-data.py'));
      };
      document.head.appendChild(tag);
    });
  }

  function fetchJSON(file) {
    if (DB.localMode) return loadScript(file);
    return fetch('data/' + file, { cache: 'no-cache' }).then(function (res) {
      if (!res.ok) throw new Error('Nie udało się wczytać pliku ' + file + ' (' + res.status + ')');
      return res.json();          // uszkodzony JSON rzuci wyjątek tutaj
    }).catch(function (err) {
      /* Zapas na wypadek nietypowych konfiguracji, w których fetch zawodzi
         mimo działającego serwera. */
      return loadScript(file).catch(function () { throw err; });
    });
  }

  /* Pojedynczy plik: pobranie, kopia (tryb file:// współdzieli obiekt globalny),
     wycięcie pisma tajskiego.

     opts.raw = true pomija jedno i drugie. Używamy tego dla indeksu
     wyszukiwania: nie ma w nim pola ttsThai, więc rekurencyjne przejście po
     10 755 wpisach niczego by nie znalazło, a kosztuje na wolnym urządzeniu
     kilkaset milisekund. Kopii też nie potrzebuje — indeksu nie modyfikujemy,
     tylko czytamy z niego wiersze przy budowie wpisów skróconych. */
  DB.loadFile = function (file, opts) {
    return fetchJSON(file).then(function (json) {
      if (opts && opts.raw) return json;
      var source = DB.localMode ? JSON.parse(JSON.stringify(json)) : json;
      return sanitize(source);
    });
  };

  DB.voiceText = function (ttsKey) { return ttsKey ? voiceMap.get(ttsKey) || null : null; };

  /* Pełny rekord — tylko jeśli jego plik jest już wczytany. */
  DB.get = function (id) { return DB.byId.get(id) || null; };

  /* Lekki wpis — dostępny dla każdego hasła od pierwszej sekundy. */
  DB.stub = function (id) { return DB.stubById.get(id) || DB.dialogueStubById.get(id) || null; };

  /* Najlepsze, co mamy pod ręką: pełny rekord, a jeśli go jeszcze nie ma —
     lekki wpis. Ekrany, które tylko wyświetlają znaczenie i fonetykę, nie
     muszą rozróżniać tych dwóch przypadków. */
  DB.any = function (id) { return DB.byId.get(id) || DB.stub(id); };

  DB.count = function () {
    /* Liczymy całą bazę, nie wczytane czoło indeksu — inaczej licznik na
       ekranie skakałby w trakcie dociągania reszty. */
    return DB.indexTotal || DB.index.length ||
      (DB.manifest ? DB.manifest.totalRecords : DB.records.length);
  };
  DB.dialogueCount = function () {
    return DB.dialogueIndex.length || (DB.manifest ? DB.manifest.totalDialogues : DB.dialogues.length);
  };

  function absorb(def, json) {
    var rows = json.records || [];
    switch (def.file) {
      case 'categories.json': DB.categories = rows; break;
      case 'grammar.json': DB.grammar = rows; break;
      case 'pronunciation.json': DB.pronunciation = json; break;
      case 'classifiers.json': DB.classifiers = rows; break;
      case 'lessons.json':
        DB.lessons = rows;
        /* Rozdziały leżą obok listy lekcji, na poziomie pliku. Przy 333
           lekcjach lista bez podziału jest nie do przejrzenia. */
        DB.chapters = json.chapters || [];
        break;
      case 'module-zero.json': DB.moduleZero = json; break;
      case 'grammar-listening.json':
        DB.grammarListening = rows;
        DB.grammarAxes = json.axes || {};
        break;
      case 'grammar-transform.json':
        DB.grammarTransform = rows;
        DB.grammarTransformKinds = json.transforms || [];
        break;
      case 'particles.json':
        DB.particles = rows;
        DB.particleExercises = json.exercises || [];
        break;
      case 'metadata.json': DB.metadata = json; break;
      case 'scenes.json':
        DB.scenes = rows;
        DB.blocks = json.blocks || [];
        rows.forEach(function (s) {
          DB.sceneById.set(s.id, s);
          (s.questions || []).forEach(function (q) { DB.sceneQuestions.set(q.id, q); });
        });
        DB.blocks.forEach(function (b) { DB.blockById.set(b.id, b); });
        break;
      case 'comprehension.json': DB.comprehension = json; break;
      /* Egzaminy i próbki kontrolne (sesja U). Oba pliki trzymamy w całości:
         niosą progi, limity czasu i gotowe zestawy zadań, a ekran egzaminu
         czyta z nich wszystko naraz przy starcie podejścia. */
      case 'exams.json': DB.exams = json; break;
      case 'checkpoints.json': DB.checkpoints = json; break;
      case 'numbers.json': DB.numbers = json; break;
      case 'rescue.json': DB.rescue = json; break;
      /* Korpus pokrycia rozumienia (sesja R). Trzymamy go w całości, bo
         ekrany liczą z niego na żywo — stan powtórek zmienia się w trakcie
         sesji i zapamiętany wynik pokazywałby liczbę sprzed kwadransa. */
      case 'coverage.json': DB.coverage = json; break;
      case 'progress-migration.json':
        DB.progressMigration = json;
        if (global.ProgressMigration) ProgressMigration.setMap(json);
        break;
      default:
        if (def.kind === 'dialogues') {
          DB.dialogues = DB.dialogues.concat(rows);
          rows.forEach(function (d) { DB.byId.set(d.id, d); });
        } else {
          DB.records = DB.records.concat(rows);
          rows.forEach(function (r) { DB.byId.set(r.id, r); });
        }
    }
    if (DB.loadedFiles.indexOf(def.file) === -1) DB.loadedFiles.push(def.file);
  }

  /* ------------------------------------------------------------- indeks */

  /* Wpisy indeksu przychodzą jako tablice — nazwy pól powtórzone 10 755 razy
     ważyłyby więcej niż same dane. Tutaj zamieniamy je na obiekty o polach
     zgodnych z pełnym rekordem, żeby ekrany mogły traktować jedno i drugie
     tak samo. Pole __stub odróżnia wpis skrócony od pełnego rekordu. */
  /* Wspólne puste kolekcje. Osobna tablica dla każdego z 10 755 wpisów to
     ponad trzydzieści tysięcy zbędnych alokacji przy starcie — a te pola
     i tak są w indeksie zawsze puste. Zamrożenie chroni przed przypadkową
     modyfikacją współdzielonego obiektu. */
  var EMPTY_LIST = Object.freeze ? Object.freeze([]) : [];

  /* Indeks jest dzielony: search-index.json niesie czoło (Survival + A1),
     search-index-rest.json resztę. Uzasadnienie podziału — w nagłówku
     tools/build-search-index.py. Liczniki fasetowe muszą być narastające,
     bo czoło i reszta wchodzą w dwóch krokach. */
  var idxLevels = {}, idxCats = {}, idxTypes = {};

  function absorbIndexRows(rows) {
    var files = DB.indexFiles;
    return (rows || []).map(function (row) {
      var fem = row[4];
      var stub = {
        id: row[0],
        polish: row[1],
        thaiPhonetic: row[2],
        pronunciationPolish: row[3],
        level: row[5],
        category: row[6],
        subcategory: '',
        type: row[7],
        frequency: row[8],
        difficulty: row[9],
        polishAlternatives: EMPTY_LIST,
        tags: EMPTY_LIST,
        examples: EMPTY_LIST,
        __stub: true,
        __file: files[row[10]]
      };
      if (fem) stub.genderVariant = { female: { thaiPhonetic: fem } };
      idxLevels[stub.level] = (idxLevels[stub.level] || 0) + 1;
      idxCats[stub.category] = (idxCats[stub.category] || 0) + 1;
      idxTypes[stub.type] = (idxTypes[stub.type] || 0) + 1;
      DB.stubById.set(stub.id, stub);
      return stub;
    });
  }

  function buildIndex(json) {
    DB.indexFiles = json.files || [];
    DB.dialogueFiles = json.dialogueFiles || [];
    DB.indexParts = json.parts || [];
    DB.indexTotal = json.totalRecords || (json.records || []).length;

    DB.index = absorbIndexRows(json.records);

    DB.dialogueIndex = (json.dialogues || []).map(function (row) {
      var stub = {
        id: row[0],
        title: row[1],
        level: row[2],
        category: row[3],
        lineCount: row[4],
        __stub: true,
        __file: DB.dialogueFiles[row[5]]
      };
      DB.dialogueStubById.set(stub.id, stub);
      return stub;
    });

    DB.countByLevel = idxLevels;
    DB.countByCat = idxCats;
    DB.indexTypes = idxTypes;
    DB.indexComplete = !DB.indexParts.length;
  }

  /* Dokleja kolejną część indeksu. Wywoływane w tle po pierwszym renderze. */
  function appendIndexPart(json) {
    var more = absorbIndexRows(json.records);
    DB.index = DB.index.concat(more);
    DB.countByLevel = idxLevels;
    DB.countByCat = idxCats;
    DB.indexTypes = idxTypes;
    refreshFacets();
    return more.length;
  }

  /* Obietnica „indeks jest kompletny”. Ekrany, które przeszukują całą bazę
     (słownik, test poziomujący, dobór nowych haseł do powtórek), wołają to
     przed pracą. W praktyce reszta jest już wtedy wczytana — pobieranie
     rusza zaraz po pierwszym renderze — więc obietnica rozwiązuje się
     natychmiast i nic nie miga. */
  var indexPromise = null;
  DB.ensureIndex = function () {
    if (DB.indexComplete) return Promise.resolve(DB.index);
    if (indexPromise) return indexPromise;
    var parts = DB.indexParts || [];
    indexPromise = parts.reduce(function (chain, f) {
      return chain.then(function () {
        return DB.loadFile(f, { raw: true }).then(function (json) {
          appendIndexPart(json);
        })['catch'](function (err) {
          DB.errors.push({ file: f, message: err.message });
        });
      });
    }, Promise.resolve()).then(function () {
      DB.indexComplete = true;
      if (global.Search && Search.build) Search.build(DB.index);
      return DB.index;
    });
    return indexPromise;
  };

  function refreshFacets() {
    var order = ['Survival', 'A1', 'A2', 'B1', 'B2'];
    var mfLevels = (DB.manifest && DB.manifest.levels) ? Object.keys(DB.manifest.levels) : [];
    DB.levels = (mfLevels.length ? mfLevels : Object.keys(DB.countByLevel))
      .sort(function (a, b) { return order.indexOf(a) - order.indexOf(b); });
    DB.types = Object.keys(DB.indexTypes || {}).sort();
    var mfCats = (DB.manifest && DB.manifest.categories) || [];
    DB.catNames = (mfCats.length ? mfCats.slice() : Object.keys(DB.countByCat))
      .sort(function (a, b) { return a.localeCompare(b, 'pl'); });
  }
  DB.refreshFacets = refreshFacets;

  /* --------------------------------------------------- ładowanie na żądanie */

  var filePromises = {};   // nazwa pliku -> obietnica (jedna na plik)

  function defFor(file) {
    var list = (DB.manifest && DB.manifest.dataFiles) || [];
    for (var i = 0; i < list.length; i++) {
      if (list[i].file === file) return list[i];
    }
    return { file: file, kind: 'vocabulary' };
  }

  /* Wczytuje jeden plik danych. Wywołana wielokrotnie dla tego samego pliku
     zwraca zawsze tę samą obietnicę — równoległe ekrany nie pobiorą go dwa razy. */
  DB.ensureFile = function (file) {
    if (!file) return Promise.resolve();
    if (filePromises[file]) return filePromises[file];
    if (DB.loadedFiles.indexOf(file) !== -1) { filePromises[file] = Promise.resolve(); return filePromises[file]; }
    filePromises[file] = DB.loadFile(file).then(function (json) {
      absorb(defFor(file), json);
      checkComplete();
    })['catch'](function (err) {
      DB.errors.push({ file: file, message: err.message });
    });
    return filePromises[file];
  };

  DB.ensureFiles = function (files) {
    var uniq = [];
    (files || []).forEach(function (f) {
      if (f && uniq.indexOf(f) === -1 && DB.loadedFiles.indexOf(f) === -1) uniq.push(f);
    });
    if (!uniq.length) return Promise.resolve();
    return Promise.all(uniq.map(DB.ensureFile));
  };

  /* Pliki, w których leżą podane hasła. */
  DB.filesFor = function (ids) {
    var files = [];
    (ids || []).forEach(function (id) {
      var stub = DB.stub(id);
      if (stub && stub.__file && files.indexOf(stub.__file) === -1) files.push(stub.__file);
    });
    return files;
  };

  /* Dociąga pełne rekordy dla podanych identyfikatorów.

     Uwaga na kolejność: zamiana identyfikatora na nazwę pliku idzie przez
     stub z indeksu (DB.filesFor). Dopóki wczytane jest samo czoło indeksu
     (Survival + A1), hasła z A2, B1 i B2 stubu nie mają — i bez tego kroku
     ensureFor cicho zwracałby pustą listę plików, a rekord nigdy by nie
     dojechał. Dlatego przy nieznanym identyfikatorze najpierw domykamy
     indeks, a dopiero potem pytamy o pliki. */
  DB.ensureFor = function (ids) {
    if (typeof ids === 'string') ids = [ids];
    var unknown = false;
    for (var i = 0; i < ids.length; i++) {
      if (!DB.stub(ids[i])) { unknown = true; break; }
    }
    if (unknown && !DB.indexComplete) {
      return DB.ensureIndex().then(function () {
        return DB.ensureFiles(DB.filesFor(ids));
      });
    }
    return DB.ensureFiles(DB.filesFor(ids));
  };

  /* Wszystkie pliki słownikowe danego poziomu. Ćwiczenia i powtórki potrzebują
     całego poziomu, ale nie całej bazy — to różnica rzędu 2 MB kontra 21 MB. */
  DB.levelFiles = function (level) {
    if (!level) return [];
    var files = [];
    DB.index.forEach(function (s) {
      if (s.level === level && files.indexOf(s.__file) === -1) files.push(s.__file);
    });
    return files;
  };

  DB.ensureLevel = function (level) {
    if (!level) return DB.ensureStarter();
    /* levelFiles czyta z indeksu — dla poziomów spoza czoła indeks musi być
       kompletny, inaczej lista plików wyszłaby pusta. */
    if (!DB.indexComplete) {
      return DB.ensureIndex().then(function () {
        return DB.ensureFiles(DB.levelFiles(level));
      });
    }
    return DB.ensureFiles(DB.levelFiles(level));
  };

  /* Materiał startowy: najmniejszy plik słownikowy. Wystarcza, żeby ćwiczenia
     miały z czego losować, zanim użytkownik wybierze poziom. */
  DB.ensureStarter = function () {
    var vocab = ((DB.manifest && DB.manifest.dataFiles) || [])
      .filter(function (d) { return d.kind === 'vocabulary'; });
    if (!vocab.length) return Promise.resolve();
    var smallest = vocab.reduce(function (best, d) { return d.count < best.count ? d : best; }, vocab[0]);
    return DB.ensureFile(smallest.file);
  };

  DB.ensureDialogues = function () {
    return DB.ensureFiles(DB.dialogueFiles);
  };

  /* Sceny i ćwiczenia rozumienia trzymamy poza materiałem startowym.

     Oba pliki to razem ponad megabajt, a potrzebne są dopiero wtedy, gdy
     uczący się wejdzie na jeden z trzech ekranów rozumienia. Wciągnięcie ich
     przy starcie opóźniłoby pierwszy ekran o tyle, ile trwa cała reszta
     wczytywania — dla ekranu, którego większość sesji w ogóle nie otwiera.

     Jedno i drugie odwołuje się do kwestii dialogów po identyfikatorze, więc
     dialogi muszą dojechać razem z nimi. */
  DB.ensureScenes = function () {
    return Promise.all([DB.ensureFile('scenes.json'), DB.ensureDialogues()]);
  };

  /* Moduł liczbowy i moduł ratunkowy. Oba poza materiałem startowym: razem
     to kilkaset kilobajtów, potrzebne dopiero po wejściu na ich ekran.
     Dryl odruchu odtwarza kwestie dialogów, więc dialogi jadą z nim. */
  DB.ensureNumbers = function () { return DB.ensureFile('numbers.json'); };
  DB.ensureRescue = function () { return DB.ensureFile('rescue.json'); };

  /* Egzamin poziomowy potrzebuje trzech rzeczy naraz: własnego pliku
     z zestawami, scen (sekcja słuchania odtwarza całe sceny) i pełnych
     rekordów haseł, które padną w produkcji — bez nich nie ma czego odtworzyć
     ani czego porównać z zapisem. Hasła dociągamy dopiero po wczytaniu
     zestawów, bo dopiero wtedy wiadomo, o które chodzi. */
  DB.ensureExams = function () {
    return DB.ensureFile('exams.json').then(function () {
      return DB.ensureScenes();
    });
  };

  DB.ensureExamRecords = function (exam) {
    if (!exam) return Promise.resolve();
    var ids = [];
    ['speaking', 'writing'].forEach(function (key) {
      ((exam.sections[key] || {}).items || []).forEach(function (it) {
        if (it.recordId) ids.push(it.recordId);
      });
    });
    return DB.ensureFor(ids);
  };

  DB.ensureCheckpoints = function () {
    return DB.ensureFile('checkpoints.json');
  };

  DB.ensureCheckpointRecords = function (def) {
    if (!def) return Promise.resolve();
    return DB.ensureFor((def.items || []).map(function (i) { return i.recordId; }));
  };

  /* Sklejenie kilku ukrytych tekstów w jeden.

     Moduł liczbowy składa liczbę z atomów — „sǎam” + „sìp” + „hâa” — i musi
     podać syntezatorowi jeden ciąg. Gdyby robił to u siebie, pismo tajskie
     musiałoby opuścić prywatną mapę i trafić do zwykłej zmiennej w kodzie
     ekranu; stamtąd do DOM-u jest jeden nieuważny appendChild. Sklejenie
     odbywa się więc TUTAJ, a na zewnątrz wychodzi wyłącznie nowy token —
     dokładnie tak samo jak przy każdym innym haśle w bazie.

     Tokeny powtarzają się (liczby składają się z tych samych dziesięciu
     cyfr), więc wynik jest zapamiętywany pod kluczem złożonym z tokenów
     składowych: dwudzieste odtworzenie tej samej liczby nie zakłada nowego
     wpisu w mapie. */
  var composed = new Map();
  DB.composeVoice = function (keys) {
    if (!Array.isArray(keys)) keys = [keys];
    keys = keys.filter(Boolean);
    if (!keys.length) return null;
    if (keys.length === 1) return keys[0];
    var cacheKey = keys.join('+');
    if (composed.has(cacheKey)) return composed.get(cacheKey);
    var text = '';
    for (var i = 0; i < keys.length; i++) {
      var part = voiceMap.get(keys[i]);
      if (!part) return null;
      text += part;
    }
    var token = stash(text);
    composed.set(cacheKey, token);
    return token;
  };

  DB.ensureComprehension = function () {
    return Promise.all([DB.ensureFile('comprehension.json'), DB.ensureDialogues()]);
  };

  /* Korpus pokrycia. Dialogów NIE dociągamy razem z nim: coverage.json ma
     wszystko, czego potrzebuje miara (numery haseł przy każdej kwestii),
     a same treści kwestii są potrzebne dopiero wtedy, gdy uczący się chce je
     usłyszeć. Ekran mapy drogi otwiera się więc po jednym pliku, nie po
     pięciu megabajtach. */
  DB.ensureCoverage = function () {
    return DB.ensureFile('coverage.json');
  };

  /* Trzy tryby gramatyczne trzymamy poza materiałem startowym z tego samego
     powodu co sceny: razem to blisko dwa megabajty, potrzebne dopiero po
     wejściu na ekran Gramatyki, którego większość sesji nie otwiera. */
  DB.ensureGrammarModes = function () {
    return DB.ensureFiles(['grammar-listening.json', 'grammar-transform.json',
                           'particles.json']);
  };

  DB.scene = function (id) { return DB.sceneById.get(id) || null; };
  DB.block = function (id) { return DB.blockById.get(id) || null; };
  DB.sceneQuestion = function (id) { return DB.sceneQuestions.get(id) || null; };

  /* Wszystkie kwestie sceny po kolei, z zapisanym numerem odcinka.
     Odtwarzacz i ekran dostają jedną płaską listę — scena ma brzmieć jak
     jedna rozmowa, a nie jak trzy dialogi puszczone pod rząd. */
  DB.sceneLines = function (scene) {
    var out = [];
    (scene.dialogueIds || []).forEach(function (did, beat) {
      var dlg = DB.get(did);
      if (!dlg || !dlg.lines) return;
      dlg.lines.forEach(function (line) {
        var copy = {};
        Object.keys(line).forEach(function (k) { copy[k] = line[k]; });
        copy.__beat = beat;
        copy.__dialogueId = did;
        copy.__key = did + '-' + line.index;
        out.push(copy);
      });
    });
    return out;
  };

  DB.blockScenes = function (block) {
    return (block.sceneIds || []).map(DB.scene).filter(Boolean);
  };

  DB.blockLines = function (block) {
    var out = [];
    DB.blockScenes(block).forEach(function (s) {
      DB.sceneLines(s).forEach(function (l) { out.push(l); });
    });
    return out;
  };


  /* Cała baza. Używana tylko tam, gdzie naprawdę trzeba: przy eksporcie
     słownictwa i przy ręcznym pobraniu wszystkiego na offline. */
  DB.ensureAll = function () {
    var files = ((DB.manifest && DB.manifest.dataFiles) || []).map(function (d) { return d.file; });
    files = files.concat(['scenes.json', 'comprehension.json', 'coverage.json',
                          'numbers.json', 'rescue.json',
                          'exams.json', 'checkpoints.json']);
    return DB.ensureFiles(files).then(function () { checkComplete(); return DB; });
  };

  /* Zgodność wstecz — starsza nazwa tej samej operacji. */
  DB.loadAll = function () { return DB.ensureAll(); };

  function checkComplete() {
    var files = ((DB.manifest && DB.manifest.dataFiles) || []);
    DB.complete = files.length > 0 && files.every(function (d) {
      return DB.loadedFiles.indexOf(d.file) !== -1;
    });
  }

  DB.isLoaded = function (file) { return DB.loadedFiles.indexOf(file) !== -1; };

  /* Ile procent bazy jest w pamięci — do paska stanu w ustawieniach. */
  DB.loadedShare = function () {
    var files = ((DB.manifest && DB.manifest.dataFiles) || []);
    if (!files.length) return 0;
    var done = files.filter(function (d) { return DB.isLoaded(d.file); }).length;
    return Math.round(done / files.length * 100);
  };

  /* --------------------------------------------------------------- start */

  DB.load = function () {
    return DB.loadFile('manifest.json').then(function (manifest) {
      DB.manifest = manifest;
      var jobs = SUPPORT.map(function (f) {
        return DB.loadFile(f).then(function (json) { absorb({ file: f, kind: 'support' }, json); })
          ['catch'](function (err) { DB.errors.push({ file: f, message: err.message }); });
      });
      jobs.push(DB.loadFile('search-index.json', { raw: true }).then(function (json) {
        buildIndex(json);
      })['catch'](function (err) {
        DB.errors.push({ file: 'search-index.json', message: err.message });
      }));
      return Promise.all(jobs);
    }).then(function () {
      /* Gdyby indeksu zabrakło, aplikacja nie może zostać bez danych —
         wtedy (i tylko wtedy) wracamy do wczytania pełnych plików. */
      if (DB.index.length) return null;
      return DB.ensureAll().then(function () {
        DB.index = DB.records;
        DB.records.forEach(function (r) { DB.stubById.set(r.id, r); });
        DB.dialogueIndex = DB.dialogues;
        DB.dialogues.forEach(function (d) { DB.dialogueStubById.set(d.id, d); });
        var levels = {}, cats = {}, types = {};
        DB.records.forEach(function (r) {
          levels[r.level] = (levels[r.level] || 0) + 1;
          cats[r.category] = (cats[r.category] || 0) + 1;
          types[r.type] = (types[r.type] || 0) + 1;
        });
        DB.countByLevel = levels; DB.countByCat = cats; DB.indexTypes = types;
      });
    }).then(function () {
      refreshFacets();
      checkComplete();
      DB.ready = true;
      return DB;
    });
  };

  global.DB = DB;
})(window);
