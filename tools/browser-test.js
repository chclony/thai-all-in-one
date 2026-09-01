#!/usr/bin/env node
/* Test aplikacji Thai All-in-One w prawdziwym silniku przeglądarki (Chromium).
   W przeciwieństwie do tools/test-app.js (jsdom) uruchamia pełny układ strony,
   dzięki czemu można sprawdzić widoczność, ognisko, kontrast i wielkość celów
   dotykowych, a także zmierzyć realny czas startu.

   Użycie:
     node tools/browser-test.js <url> [etykieta] [liczba prób]

   Przykłady:
     node tools/browser-test.js "file:///.../index.html" file 3
     node tools/browser-test.js "http://localhost:8123/index.html" http 3
*/
const path = require('path');
const { chromium } = require(process.env.PW_LIB ||
  '/home/claude/.npm-global/lib/node_modules/playwright');

const EXEC = process.env.PW_CHROME ||
  '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const THAI = /[\u0E00-\u0E7F]/;
const SCREENS = ['today', 'dict', 'phrases', 'listen', 'speak',
                 'dialogues', 'srs', 'pron', 'progress', 'settings'];

let failures = 0;
function log(ok, msg) {
  console.log((ok ? '  OK   ' : '  BLAD ') + msg);
  if (!ok) failures++;
}

/* Zastępniki API, których nagłówkowy Chromium nie ma:
   SpeechSynthesis (brak głosów systemowych) i MediaRecorder (brak mikrofonu). */
const SHIMS = () => {
  window.__spoken = [];
  window.__cancelCount = 0;
  const voices = [{ lang: 'th-TH', name: 'Thai Female', voiceURI: 'th', localService: true }];
  /* window.speechSynthesis jest akcesorem tylko do odczytu — samo przypisanie
     nic by nie zmieniło, dlatego podmieniamy właściwość przez defineProperty. */
  Object.defineProperty(window, 'speechSynthesis', {
    configurable: true,
    value: {
      speaking: false,
      paused: false,
      speak(u) { window.__spoken.push(u.text); if (u.onstart) u.onstart(); setTimeout(() => u.onend && u.onend(), 10); },
      cancel() { window.__cancelCount++; },
      resume() {},
      getVoices: () => voices,
      addEventListener() {},
    },
  });
  window.SpeechSynthesisUtterance = function (t) { this.text = t; };
  const chunks = [];
  window.MediaRecorder = function () {
    this.state = 'inactive';
    this.start = () => { this.state = 'recording'; };
    this.stop = () => {
      this.state = 'inactive';
      if (this.ondataavailable) this.ondataavailable({ data: new Blob(['x'], { type: 'audio/webm' }) });
      if (this.onstop) this.onstop();
    };
  };
  window.MediaRecorder.isTypeSupported = () => true;
  if (!navigator.mediaDevices) {
    Object.defineProperty(navigator, 'mediaDevices', { value: {}, configurable: true });
  }
  navigator.mediaDevices.getUserMedia = async () => ({
    getTracks: () => [{ stop() {} }],
  });
  void chunks;
};

(async () => {
  const url = process.argv[2];
  const label = process.argv[3] || url;
  const runs = parseInt(process.argv[4] || '3', 10);
  if (!url) { console.error('podaj adres'); process.exit(2); }

  const browser = await chromium.launch({
    executablePath: EXEC,
    args: ['--allow-file-access-from-files', '--no-sandbox', '--disable-web-security'],
  });

  /* ---------------------------------------------------- pomiar czasu startu */
  const times = [];
  let firstStats = null;
  for (let i = 0; i < runs; i++) {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    await page.addInitScript(SHIMS);
    await page.goto(url, { waitUntil: 'domcontentloaded' });
    const res = await page.evaluate(async () => {
      const t0 = window.__appStart || performance.timeOrigin;
      while (!window.DB) await new Promise((r) => setTimeout(r, 5));
      await new Promise((resolve) => {
        const tick = () => (window.DB.ready ? resolve() : setTimeout(tick, 5));
        tick();
      });
      /* czekamy jeszcze na pierwsze wyrenderowanie ekranu startowego */
      await new Promise((r) => requestAnimationFrame(() => r()));
      return {
        ms: performance.now(),
        records: window.DB.count ? window.DB.count() : window.DB.records.length,
        loaded: window.DB.records.length,
        dialogues: window.DB.dialogueCount ? window.DB.dialogueCount() : window.DB.dialogues.length,
        localMode: window.DB.localMode,
        t0,
      };
    });
    times.push(res.ms);
    firstStats = res;
    await ctx.close();
  }
  const avg = times.reduce((a, b) => a + b, 0) / times.length;

  console.log('\n=== ' + label + ' ===');
  console.log('  czas do gotowości bazy: ' + times.map((t) => Math.round(t) + ' ms').join(', ') +
              '  (średnia ' + Math.round(avg) + ' ms)');
  console.log('  rekordów w bazie: ' + firstStats.records +
              ' | wczytanych do pamięci na starcie: ' + firstStats.loaded +
              ' | dialogów: ' + firstStats.dialogues +
              ' | tryb lokalny: ' + firstStats.localMode);

  /* ------------------------------------------------- pełny przebieg testów */
  const ctx = await browser.newContext({
    viewport: { width: 390, height: 844 },          // iPhone 14/15
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 ' +
               '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  });
  const page = await ctx.newPage();
  await page.addInitScript(SHIMS);
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message || e)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => window.DB && window.DB.ready, null, { timeout: 60000 });

  const mf = await page.evaluate(() => window.DB.manifest);
  log(!!mf, 'manifest.json wczytany (wersja ' + (mf && mf.version) + ')');

  /* wszystkie pliki z manifestu muszą być osiągalne */
  const filesOk = await page.evaluate(async () => {
    const out = [];
    for (const d of window.DB.manifest.dataFiles.concat(window.DB.manifest.supportFiles)) {
      try {
        const j = await window.DB.loadFile(d.file);
        out.push([d.file, !!j, (j.records || []).length]);
      } catch (e) { out.push([d.file, false, String(e.message)]); }
    }
    return out;
  }).catch(() => null);
  if (filesOk) {
    const bad = filesOk.filter((f) => !f[1]);
    log(bad.length === 0, 'wszystkie pliki z manifestu wczytywalne (' +
        filesOk.length + ' plików)' + (bad.length ? ': ' + JSON.stringify(bad) : ''));
  }

  /* liczniki */
  const counts = await page.evaluate(async () => {
    await window.DB.loadAll();
    const lv = {};
    window.DB.records.forEach((r) => { lv[r.level] = (lv[r.level] || 0) + 1; });
    return { records: window.DB.records.length, dialogues: window.DB.dialogues.length, lv };
  });
  log(counts.records === mf.totalRecords,
      'rekordów po pełnym wczytaniu: ' + counts.records + ' (manifest: ' + mf.totalRecords + ')');
  log(counts.dialogues === mf.totalDialogues,
      'dialogów: ' + counts.dialogues + ' (manifest: ' + mf.totalDialogues + ')');
  Object.keys(mf.levels).forEach((lv) => {
    log(counts.lv[lv] === mf.levels[lv], 'poziom ' + lv + ': ' + counts.lv[lv]);
  });

  /* przejście przez ekrany + audyt DOM pod kątem pisma tajskiego */
  const thaiFound = [];
  for (const id of SCREENS) {
    await page.evaluate((s) => window.App.go(s), id);
    await page.waitForTimeout(220);
    const info = await page.evaluate((s) => {
      const sec = document.getElementById('screen-' + s);
      return {
        visible: sec && !sec.hidden && sec.offsetHeight > 0,
        len: sec ? sec.textContent.trim().length : 0,
        text: sec ? sec.textContent : '',
        html: sec ? sec.innerHTML : '',
      };
    }, id);
    log(info.visible && info.len > 20,
        'ekran ' + id + ' (widoczny, treść: ' + info.len + ' znaków)');
    if (THAI.test(info.text) || THAI.test(info.html)) thaiFound.push(id);
  }

  /* audyt DOM: cały dokument, łącznie z atrybutami i pseudo-elementami */
  const domAudit = await page.evaluate(() => {
    const re = /[\u0E00-\u0E7F]/;
    const hits = [];
    const walk = document.createTreeWalker(document.documentElement, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = walk.nextNode())) {
      if (re.test(n.nodeValue)) hits.push('text:' + n.nodeValue.slice(0, 40));
    }
    document.querySelectorAll('*').forEach((el) => {
      for (const a of el.attributes) {
        if (re.test(a.value)) hits.push(el.tagName + '[' + a.name + ']=' + a.value.slice(0, 40));
      }
    });
    return hits;
  });
  log(thaiFound.length === 0 && domAudit.length === 0,
      'brak pisma tajskiego w DOM' +
      (thaiFound.length ? ' — ekrany: ' + thaiFound : '') +
      (domAudit.length ? ' — trafienia: ' + JSON.stringify(domAudit.slice(0, 5)) : ''));

  /* wyszukiwanie po polsku i po fonetyce (także bez tonów) */
  await page.evaluate(() => window.App.go('dict'));
  await page.waitForTimeout(200);
  for (const [q, what] of [['rezerwacj', 'po polsku'], ['náam', 'po fonetyce z tonami'],
                           ['naam', 'po fonetyce bez tonów'], ['sawatdii', 'bez łączników']]) {
    const n = await page.evaluate(async (query) => {
      const inp = document.getElementById('dict-q');
      inp.value = query;
      inp.dispatchEvent(new Event('input', { bubbles: true }));
      await new Promise((r) => setTimeout(r, 450));
      return document.querySelectorAll('#dict-results .row').length;
    }, q);
    log(n > 0, 'wyszukiwanie ' + what + ' („' + q + '”): ' + n + ' wyników');
  }
  await page.evaluate(() => {
    const inp = document.getElementById('dict-q');
    inp.value = '';
    inp.dispatchEvent(new Event('input', { bubbles: true }));
  });
  await page.waitForTimeout(400);

  /* filtry */
  const filt = await page.evaluate(async () => {
    const setSel = async (id, v) => {
      const el = document.getElementById(id);
      el.value = v;
      el.dispatchEvent(new Event('change', { bubbles: true }));
      await new Promise((r) => setTimeout(r, 350));
      return document.getElementById('dict-count').textContent;
    };
    const out = {};
    out.level = await setSel('f-level', 'A2');
    out.cat = await setSel('f-cat', document.getElementById('f-cat').options[1].value);
    await setSel('f-level', '');
    await setSel('f-cat', '');
    out.hard = await setSel('f-sort', 'hard');
    out.firstHard = (document.querySelector('#dict-results .row-meta') || {}).textContent;
    await setSel('f-sort', 'freq');
    /* ulubione */
    const id = window.DB.records[0].id;
    window.Progress.toggleFavourite(id);
    document.getElementById('f-fav').click();
    await new Promise((r) => setTimeout(r, 350));
    out.fav = document.querySelectorAll('#dict-results .row').length;
    document.getElementById('f-fav').click();
    window.Progress.toggleFavourite(id);
    await new Promise((r) => setTimeout(r, 300));
    return out;
  });
  log(/\d/.test(filt.level), 'filtr poziomu: ' + filt.level);
  log(/\d/.test(filt.cat), 'filtr kategorii: ' + filt.cat);
  log(/\d/.test(filt.hard), 'sortowanie po trudności działa');
  log(filt.fav === 1, 'filtr ulubionych: ' + filt.fav + ' wynik');

  /* cztery tryby quizu słuchania */
  for (const mode of ['choice', 'dictation', 'assemble', 'spot']) {
    const ok = await page.evaluate(async (m) => {
      window.App.go('listen');
      const btn = document.querySelector('[data-listen="' + m + '"]');
      btn.click();
      await new Promise((r) => setTimeout(r, 350));
      const area = document.getElementById('listen-area');
      return { len: area.textContent.trim().length,
               controls: area.querySelectorAll('button').length };
    }, mode);
    log(ok.len > 20 && ok.controls > 1,
        'tryb słuchania „' + mode + '” (treść ' + ok.len + ' zn., ' + ok.controls + ' przycisków)');
  }

  /* TTS + zatrzymywanie poprzedniego audio */
  const tts = await page.evaluate(async () => {
    window.__spoken.length = 0; window.__cancelCount = 0;
    window.App.go('today');
    await new Promise((r) => setTimeout(r, 250));
    const b = document.querySelector('#today-word .play-btn');
    b.click();
    await new Promise((r) => setTimeout(r, 60));
    b.click();
    await new Promise((r) => setTimeout(r, 60));
    return { spoken: window.__spoken.slice(), cancels: window.__cancelCount };
  });
  log(tts.spoken.length >= 2 && THAI.test(tts.spoken[0]),
      'TTS dostaje pismo tajskie z ukrytego pola');
  log(tts.cancels >= 2, 'poprzednie audio jest zatrzymywane przed nowym (' + tts.cancels + ' x cancel)');

  /* zachowanie bez tajskiego głosu */
  const noVoice = await page.evaluate(async () => {
    const old = window.speechSynthesis.getVoices;
    window.speechSynthesis.getVoices = () => [{ lang: 'pl-PL', name: 'Polski' }];
    window.Speech.voice = null;
    window.Speech.warned = false;
    window.App.go('today');
    await new Promise((r) => setTimeout(r, 250));
    document.querySelector('#today-word .play-btn').click();
    await new Promise((r) => setTimeout(r, 250));
    const toast = document.getElementById('toast');
    const msg = { hidden: toast.hidden, text: toast.textContent, label: window.Speech.voiceLabel() };
    window.speechSynthesis.getVoices = old;
    window.Speech.voice = null;
    return msg;
  });
  log(!noVoice.hidden && noVoice.text.length > 10,
      'brak tajskiego głosu: aplikacja pokazuje komunikat zamiast milczeć');
  log(!THAI.test(noVoice.label), 'nazwa głosu systemowego oczyszczona z pisma tajskiego');
  await page.evaluate(() => { window.Speech.voice = window.speechSynthesis.getVoices()[0]; });

  /* nagrywanie głosu */
  const rec = await page.evaluate(async () => {
    window.App.go('speak');
    await new Promise((r) => setTimeout(r, 400));
    const btns = () => Array.from(document.querySelectorAll('#speak-area button'));
    const start = btns().find((b) => /nagraj/i.test(b.textContent));
    const playback = btns().find((b) => /odsłuchaj/i.test(b.textContent));
    if (!start || !playback) return { found: false };
    const before = playback.disabled;
    start.click();
    await new Promise((r) => setTimeout(r, 400));
    const recording = /zatrzymaj/i.test(start.textContent);
    start.click();                       // ten sam przycisk kończy nagranie
    await new Promise((r) => setTimeout(r, 400));
    return {
      found: true,
      recording,
      unlocked: before === true && playback.disabled === false,
      relabelled: /ponownie/i.test(start.textContent),
    };
  });
  log(rec.found, 'ekran mówienia ma przyciski nagrywania i odsłuchu');
  log(rec.recording, 'przycisk przechodzi w stan „Zatrzymaj nagrywanie”');
  log(rec.unlocked && rec.relabelled,
      'MediaRecorder oddaje nagranie: odsłuch staje się dostępny');

  /* SRS + zapis postępu */
  const srs = await page.evaluate(async () => {
    const id = window.DB.records[5].id;
    window.SRS.add(id);
    window.SRS.grade(id, 4);
    window.Progress.answer(id, true);
    const raw = localStorage.getItem('thaiaio.srs');
    const p = localStorage.getItem('thaiaio.progress');
    return { srs: !!raw && raw.indexOf(id) !== -1, prog: !!p, stats: window.SRS.stats() };
  });
  log(srs.srs, 'SRS zapisuje kartę w localStorage');
  log(srs.prog, 'postęp zapisywany w localStorage');

  /* eksport / import */
  const io = await page.evaluate(async () => {
    const dump = window.Progress.exportData();
    const json = JSON.stringify(dump);
    const hadThai = /[\u0E00-\u0E7F]/.test(json);
    window.Progress.data.favourites = {};
    window.Progress.importData(JSON.parse(json));
    return { size: json.length, hadThai, restored: Object.keys(window.Progress.data).length > 3 };
  });
  log(io.size > 20 && io.restored, 'eksport i import postępu działają (' + io.size + ' B)');
  log(!io.hadThai, 'eksport nie zawiera pisma tajskiego');

  /* motywy */
  for (const theme of ['light', 'dark']) {
    const bg = await page.evaluate(async (t) => {
      document.body.setAttribute('data-theme', t);
      await new Promise((r) => setTimeout(r, 120));
      const s = getComputedStyle(document.body);
      return { bg: s.backgroundColor, fg: s.color };
    }, theme);
    log(bg.bg !== bg.fg, 'motyw ' + theme + ': tło ' + bg.bg + ', tekst ' + bg.fg);
  }
  await page.evaluate(() => document.body.setAttribute('data-theme', 'auto'));

  /* mobilny układ: brak poziomego przewijania, cele dotykowe, safe-area */
  const layout = await page.evaluate(() => {
    const tab = document.querySelector('.tabbar');
    const cs = tab ? getComputedStyle(tab) : null;
    const small = Array.from(document.querySelectorAll('button, a, select, input'))
      .filter((el) => el.offsetParent !== null)
      .map((el) => el.getBoundingClientRect())
      .filter((r) => r.width > 0 && (r.height < 40 || r.width < 40)).length;
    return {
      overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      tabPadding: cs ? cs.paddingBottom : '',
      smallTargets: small,
    };
  });
  log(layout.overflowX <= 1, 'brak poziomego przewijania na 390 px (nadmiar: ' + layout.overflowX + ' px)');
  log(/px/.test(layout.tabPadding), 'pasek dolny respektuje safe-area (padding-bottom: ' + layout.tabPadding + ')');
  log(layout.smallTargets === 0, 'wszystkie cele dotykowe ≥ 40 px (' + layout.smallTargets + ' za małych)');

  /* dostępność */
  const a11y = await page.evaluate(() => {
    const noLabel = Array.from(document.querySelectorAll('button'))
      .filter((b) => b.offsetParent !== null)
      .filter((b) => !b.getAttribute('aria-label') && !b.textContent.trim()).length;
    const inputs = Array.from(document.querySelectorAll('input, select'))
      .filter((el) => el.offsetParent !== null)
      .filter((el) => !el.getAttribute('aria-label') && !el.labels?.length &&
                      !document.querySelector('label[for="' + el.id + '"]')).length;
    window.App.go('dict');
    document.getElementById('dict-q').focus();
    const focused = document.activeElement && document.activeElement.id;
    const outline = document.activeElement ? getComputedStyle(document.activeElement, ':focus-visible').outlineWidth : '';
    return { noLabel, inputs, focused, outline };
  });
  log(a11y.noLabel === 0, 'każdy przycisk ma etykietę (' + a11y.noLabel + ' bez);');
  log(a11y.inputs === 0, 'każde pole formularza ma etykietę (' + a11y.inputs + ' bez)');
  log(!!a11y.focused, 'ognisko klawiatury działa (aktywny: ' + a11y.focused + ')');

  /* nawigacja klawiaturą */
  await page.evaluate(() => window.App.go('dict'));
  await page.keyboard.press('Tab');
  const tabbed = await page.evaluate(() => document.activeElement.tagName + '#' + document.activeElement.id);
  log(tabbed !== 'BODY#', 'Tab przenosi ognisko na element interaktywny (' + tabbed + ')');

  /* Escape zamyka arkusz */
  const esc = await page.evaluate(async () => {
    window.App.openRecord(window.DB.records[0].id);
    await new Promise((r) => setTimeout(r, 200));
    const open = !document.getElementById('sheet').hidden;
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
    await new Promise((r) => setTimeout(r, 200));
    return { open, closed: document.getElementById('sheet').hidden };
  });
  log(esc.open && esc.closed, 'arkusz szczegółów otwiera się i zamyka klawiszem Escape');

  const real = errors.filter((e) => !/favicon|Not implemented|net::ERR_FILE_NOT_FOUND.*audio/i.test(e));
  log(real.length === 0, 'brak błędów wykonania' + (real.length ? ': ' + real.slice(0, 3).join(' | ') : ''));

  await browser.close();
  console.log('\n  --> ' + (failures ? failures + ' BŁĘDÓW' : 'WSZYSTKIE TESTY ZALICZONE'));
  console.log('  --> czas startu (średnia z ' + runs + '): ' + Math.round(avg) + ' ms');
  process.exit(failures ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });
