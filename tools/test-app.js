/* Test aplikacji Thai All-in-One w dwoch trybach: file:// i przez serwer HTTP.
   Uruchomienie:  node test-app.js file    |    node test-app.js http://localhost:8123 */
const { JSDOM } = require('jsdom');
const path = require('path');
const fs = require('fs');

const APP = path.resolve(__dirname, '..');
const mode = process.argv[2] || 'file';
const THAI = /[\u0E00-\u0E7F]/;

const SCREENS = ['today', 'dict', 'phrases', 'listen', 'speak',
                 'dialogues', 'srs', 'pron', 'progress', 'settings'];

function log(ok, msg) {
  console.log((ok ? '  OK   ' : '  BLAD ') + msg);
  if (!ok) process.exitCode = 1;
}

process.on('unhandledRejection', (e) => {
  console.log('UNHANDLED:', e && (e.stack || e.message || String(e)), JSON.stringify(e));
});

(async () => {
  const url = mode === 'file'
    ? 'file://' + path.join(APP, 'index.html')
    : mode + '/index.html';
  const html = fs.readFileSync(path.join(APP, 'index.html'), 'utf8');

  const dom = new JSDOM(html, {
    url,
    runScripts: 'dangerously',
    resources: 'usable',
    pretendToBeVisual: true,
    /* file:// to w jsdom "opaque origin", w ktorym localStorage jest zablokowany.
       Prawdziwe przegladarki na to pozwalaja, wiec podstawiamy odpowiednik. */
    beforeParse(window) {
      const store = new Map();
      const shim = {
        getItem: (k) => (store.has(String(k)) ? store.get(String(k)) : null),
        setItem: (k, v) => store.set(String(k), String(v)),
        removeItem: (k) => store.delete(String(k)),
        clear: () => store.clear(),
        key: (i) => Array.from(store.keys())[i] ?? null,
        get length() { return store.size; },
      };
      Object.defineProperty(window, 'localStorage', { value: shim, configurable: true });
      Object.defineProperty(window, 'sessionStorage', { value: shim, configurable: true });
    },
  });
  const w = dom.window;

  // jsdom nie ma fetch ani SpeechSynthesis — dokladamy minimalne zamienniki,
  // zeby sciezka sieciowa i przycisk odsluchu byly wykonywane naprawde.
  const spoken = [];
  if (mode !== 'file') {
    w.fetch = (u, opts) => {
      const abs = new URL(u, url).href;
      return fetch(abs, opts);
    };
  }
  w.speechSynthesis = {
    speak: (utt) => spoken.push(utt.text),
    cancel: () => {},
    getVoices: () => [{ lang: 'th-TH', name: 'Thai', voiceURI: 'th' }],
    addEventListener: () => {},
  };
  w.SpeechSynthesisUtterance = function (t) { this.text = t; };
  w.localStorage.clear();

  const errors = [];
  w.addEventListener('error', (e) => errors.push(String(e.message || e.error)));
  w.addEventListener('unhandledrejection', (e) => errors.push(String(e.reason)));

  await new Promise((res) => w.addEventListener('load', res, { once: true }));

  // czekamy, az baza sie wczyta
  for (let i = 0; i < 300; i++) {
    if (w.DB && w.DB.ready) break;
    await new Promise((r) => setTimeout(r, 100));
  }

  console.log('=== TRYB: ' + (mode === 'file' ? 'file://' : mode) + ' ===');
  log(!!(w.DB && w.DB.ready), 'baza wczytana');
  if (!w.DB || !w.DB.ready) {
    console.log('  blad ladowania:', errors.slice(0, 3));
    return;
  }

  /* DB.ready oznacza tylko, ze wczytal sie plik startowy — reszte bazy
     dociaga DB.loadAll(). Asercje ponizej porownuja stan pamieci z sumami
     z manifestu, wiec musimy poczekac na komplet, inaczej test mierzy
     jeden plik i zglasza falszywy blad. */
  await w.DB.loadAll();
  for (let i = 0; i < 300; i++) {
    if (w.DB.complete) break;
    await new Promise((r) => setTimeout(r, 100));
  }
  log(!!w.DB.complete, 'cala baza wczytana (loadAll)');
  if (w.DB.errors && w.DB.errors.length) {
    console.log('  pliki z bledem:', w.DB.errors.slice(0, 5));
  }

  /* Oczekiwania czytamy z manifestu, nie z liczb wpisanych na sztywno.
     Dzieki temu test nie wymaga poprawki po kazdym etapie rozbudowy bazy. */
  const mf = w.DB.manifest;
  const expectRecords = mf.totalRecords;
  const expectDialogues = mf.totalDialogues;
  const expectLevels = Object.keys(mf.levels);

  log(w.DB.records.length === expectRecords,
      'rekordow slownika: ' + w.DB.records.length + ' (manifest: ' + expectRecords + ')');
  log(w.DB.dialogues.length === expectDialogues,
      'dialogow: ' + w.DB.dialogues.length + ' (manifest: ' + expectDialogues + ')');
  log(expectLevels.every((lv) => w.DB.levels.includes(lv)),
      'poziomy: ' + w.DB.levels.join(','));
  expectLevels.forEach((lv) => {
    log(w.DB.countByLevel[lv] === mf.levels[lv],
        'rekordow ' + lv + ': ' + w.DB.countByLevel[lv]);
  });

  // kazdy plik dialogow z manifestu musi trafic do pamieci aplikacji
  const dlgFiles = mf.dataFiles.filter((d) => d.kind === 'dialogues');
  log(dlgFiles.length > 0, 'manifest deklaruje pliki dialogow: ' + dlgFiles.length);
  const dlgSum = dlgFiles.reduce((a, d) => a + d.count, 0);
  log(dlgSum === w.DB.dialogues.length,
      'suma dialogow z manifestu zgadza sie z pamiecia aplikacji');
  log(w.DB.dialogues.some((d) => d.level === 'B2'),
      'dialogi B2 obecne w pamieci aplikacji');

  // ttsThai nie moze istniec w obiektach krazacych po aplikacji
  const leak = JSON.stringify(w.DB.records.slice(0, 500)).includes('ttsThai');
  log(!leak, 'pole ttsThai wyciete z rekordow');

  // przejscie przez wszystkie 10 ekranow
  for (const id of SCREENS) {
    w.location.hash = '#' + id;
    w.dispatchEvent(new w.Event('hashchange'));
    await new Promise((r) => setTimeout(r, 120));
    const sec = w.document.getElementById('screen-' + id);
    const visible = sec && !sec.hidden;
    const filled = sec && sec.textContent.trim().length > 20;
    log(visible && filled, 'ekran ' + id + ' (widoczny, tresc: ' +
        (sec ? sec.textContent.trim().length : 0) + ' znakow)');
  }

  // wyszukiwarka
  w.location.hash = '#dict';
  w.dispatchEvent(new w.Event('hashchange'));
  await new Promise((r) => setTimeout(r, 150));
  const q = w.document.querySelector('#dict-q, #q, input[type=search]');
  if (q) {
    q.value = 'rezerwacj';
    q.dispatchEvent(new w.Event('input', { bubbles: true }));
    await new Promise((r) => setTimeout(r, 400));
    const res = w.document.getElementById('screen-dict').textContent;
    log(/rezerwacj/i.test(res), 'wyszukiwarka znajduje hasla A2');
  } else {
    log(false, 'nie znaleziono pola wyszukiwania');
  }

  // odsluch: przycisk play musi podac syntezatorowi pismo tajskie
  const play = w.document.querySelector('#screen-dict .icon-btn');
  if (play) {
    play.click();
    await new Promise((r) => setTimeout(r, 200));
    log(spoken.length > 0 && THAI.test(spoken[spoken.length - 1] || ''),
        'synteza mowy dostaje pismo tajskie (ukryte wejscie dziala)');
  }

  // pismo tajskie nie moze pojawic sie nigdzie w widocznym DOM
  let thaiScreens = [];
  for (const id of SCREENS) {
    w.location.hash = '#' + id;
    w.dispatchEvent(new w.Event('hashchange'));
    await new Promise((r) => setTimeout(r, 120));
    const sec = w.document.getElementById('screen-' + id);
    if (sec && THAI.test(sec.textContent)) thaiScreens.push(id);
  }
  log(thaiScreens.length === 0,
      'brak pisma tajskiego w interfejsie' + (thaiScreens.length ? ': ' + thaiScreens : ''));

  const real = errors.filter((e) => !/Not implemented|matchMedia|scrollTo/i.test(e));
  log(real.length === 0, 'brak bledow wykonania' + (real.length ? ': ' + real.slice(0, 3) : ''));

  w.close();
})();
