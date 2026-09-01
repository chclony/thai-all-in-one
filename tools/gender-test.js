#!/usr/bin/env node
/* Test przełącznika płci mówiącego — Thai All-in-One.

   Sprawdza to, czego walidator danych nie widzi: czy aplikacja faktycznie
   pokazuje i czyta formę zgodną z wyborem użytkownika, na każdym z dziesięciu
   ekranów, w obu ustawieniach.

   Użycie:
     node tools/gender-test.js <url> [etykieta]
*/
const { chromium } = require(process.env.PW_LIB ||
  '/home/claude/.npm-global/lib/node_modules/playwright');

const EXEC = process.env.PW_CHROME ||
  '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const SCREENS = ['today', 'dict', 'phrases', 'listen', 'speak',
                 'dialogues', 'srs', 'pron', 'progress', 'settings'];

/* Formy męskie i żeńskie w zapisie fonetycznym. */
const MALE = /(^|[\s>(])(khráp|phǒm)([\s<).,?!]|$)/;
const FEMALE = /(^|[\s>(])(khâ|khá|chǎn|dì-chǎn)([\s<).,?!]|$)/;
const TH_MALE = '\u0e04\u0e23\u0e31\u0e1a';        // ครับ
const TH_FEM_A = '\u0e04\u0e48\u0e30';             // ค่ะ
const TH_FEM_Q = '\u0e04\u0e30';                   // คะ

let failures = 0;
function log(ok, msg) {
  console.log((ok ? '  OK   ' : '  BLAD ') + msg);
  if (!ok) failures++;
}

const SHIMS = () => {
  window.__spoken = [];
  const voices = [{ lang: 'th-TH', name: 'Thai Female', voiceURI: 'th', localService: true }];
  Object.defineProperty(window, 'speechSynthesis', {
    configurable: true,
    value: {
      speaking: false, paused: false,
      speak(u) { window.__spoken.push(u.text); if (u.onstart) u.onstart(); setTimeout(() => u.onend && u.onend(), 5); },
      cancel() {}, resume() {}, getVoices: () => voices, addEventListener() {},
    },
  });
  window.SpeechSynthesisUtterance = function (t) { this.text = t; };
  window.MediaRecorder = function () {
    this.state = 'inactive';
    this.start = () => { this.state = 'recording'; };
    this.stop = () => { this.state = 'inactive'; if (this.onstop) this.onstop(); };
  };
  window.MediaRecorder.isTypeSupported = () => true;
  if (!navigator.mediaDevices) {
    Object.defineProperty(navigator, 'mediaDevices', { value: {}, configurable: true });
  }
  navigator.mediaDevices.getUserMedia = async () => ({ getTracks: () => [{ stop() {} }] });
};

/* Zbiera tekst widoczny na bieżącym ekranie, bez bloków, które celowo
   pokazują obie formy (szczegóły hasła, sekcja o płci, ćwiczenie rozpoznawania). */
/* Zbiera wyłącznie zapisy fonetyczne widoczne na bieżącym ekranie.
   Prozy nie ruszamy: ekran Wymowa z założenia nazywa obie formy po imieniu,
   a sprawdzamy tutaj to, co uczący się ma powtarzać, nie to, co czyta. */
const collect = () => {
  const node = document.querySelector('#screen-' + window.App.screen);
  if (!node) return '';
  const clone = node.cloneNode(true);
  /* Bloki, które celowo pokazują obie formy naraz. */
  clone.querySelectorAll('.gform, .gender-card, .reveal, .gender-lexicon').forEach((n) => n.remove());
  const parts = [];
  /* U.renderPhonetic rozbija zapis na sylaby w osobnych <span>; bez sklejenia
     ze spacją textContent daje „chǎnphûutthai” i żaden wzorzec by nie trafił. */
  clone.querySelectorAll('.phonetic').forEach((el) => {
    parts.push(Array.from(el.querySelectorAll('.syl')).map((x) => x.textContent).join(' '));
  });
  clone.querySelectorAll('.row-ph, .l-ph, .token').forEach((el) => parts.push(el.textContent));
  return ' ' + parts.join(' | ') + ' ';
};

async function go(page, id) {
  await page.evaluate((s) => window.App.go(s), id);
  await page.waitForTimeout(150);
}

(async () => {
  const url = process.argv[2];
  const label = process.argv[3] || url;
  if (!url) { console.error('podaj adres'); process.exit(2); }

  const browser = await chromium.launch({
    executablePath: EXEC,
    args: ['--allow-file-access-from-files', '--no-sandbox', '--disable-web-security'],
  });
  const ctx = await browser.newContext({
    viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true,
  });
  const page = await ctx.newPage();
  await page.addInitScript(SHIMS);
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message || e)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

  console.log('\n=== PŁEĆ MÓWIĄCEGO — ' + label + ' ===');

  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => window.DB && window.DB.ready, null, { timeout: 60000 });
  await page.waitForFunction(() => window.DB && window.DB.complete, null, { timeout: 90000 });

  /* ------------------------------------------- 1. pytanie przy pierwszym starcie */
  const askVisible = await page.isVisible('#gender-ask');
  log(askVisible, 'przy pierwszym uruchomieniu pojawia się pytanie o płeć');
  const stored0 = await page.evaluate(() => localStorage.getItem('thaiaio.gender'));
  log(stored0 === null, 'przed odpowiedzią nic nie jest zapisane w localStorage');

  await page.click('#gender-ask [data-gender="female"]');
  await page.waitForTimeout(200);
  log(!(await page.isVisible('#gender-ask')), 'po wyborze okno się zamyka');
  const stored1 = await page.evaluate(() => localStorage.getItem('thaiaio.gender'));
  log(JSON.parse(stored1) === 'female', 'wybór zapisany w localStorage: ' + stored1);

  /* Na kilku ekranach treść zależna od płci nie pojawia się sama z siebie —
     zwrot dnia bywa bez cząstki, kolejka powtórek na starcie jest pusta.
     Podstawiamy więc konkretne hasło z wariantem, żeby test faktycznie
     coś sprawdzał, zamiast przechodzić na pustym ekranie. */
  const seed = async () => page.evaluate(() => {
    const gendered = window.DB.records.filter((r) => window.G.hasVariant(r) &&
      /khráp|phǒm/.test(r.thaiPhonetic));
    const rec = gendered[0];
    window.Quiz.mode = 'choice';
    window.SRS.add(rec.id);
    window.__seedId = rec.id;
    window.__seedPolish = rec.polish;
    return rec.id;
  });

  const walk = async (mode) => {
    const report = [];
    for (const id of SCREENS) {
      await go(page, id);
      if (id === 'dict') {
        await page.evaluate(() => {
          document.querySelector('#dict-q').value = window.__seedPolish;
          document.querySelector('#dict-q').dispatchEvent(new Event('input'));
        });
        await page.waitForTimeout(320);
      }
      if (id === 'speak') {
        await page.evaluate(() => window.Quiz.renderSpeak(
          document.querySelector('#speak-area'), window.DB.get(window.__seedId)));
        await page.waitForTimeout(120);
      }
      const txt = await page.evaluate(collect);
      report.push({ id, male: MALE.test(txt), fem: FEMALE.test(txt) });
    }
    return report;
  };

  /* ---------------------------------------------- 2. dziesięć ekranów, kobieta */
  await seed();
  const femaleReport = await walk('female');
  for (const r of femaleReport) {
    if (r.id === 'dialogues') continue;    // dialog ma role o ustalonej płci
    log(!r.male, 'ekran ' + r.id + ': brak form męskich przy ustawieniu „kobieta”');
  }
  const femScreens = femaleReport.filter((r) => r.fem).map((r) => r.id);
  log(femScreens.length >= 6,
      'formy żeńskie faktycznie widoczne na ekranach: ' + femScreens.join(', '));

  /* ------------------------------------------------------ 3. dialog z rolami */
  await go(page, 'dialogues');
  const dlg = await page.evaluate(() => {
    const opts = Array.from(document.querySelectorAll('#dlg-select option'));
    const target = opts.find((o) => /restauracj/i.test(o.textContent)) || opts[0];
    document.querySelector('#dlg-select').value = target.value;
    document.querySelector('#dlg-select').dispatchEvent(new Event('change'));
    const d = window.DB.dialogues.filter((x) => x.id === target.value)[0];
    return { roles: d.roles, roleGender: d.roleGender, caption: document.querySelector('#dlg-view p').textContent };
  });
  log(!!dlg.roleGender, 'dialog ma pole roleGender: ' + JSON.stringify(dlg.roleGender));
  log(/kobieta|mężczyzna/.test(dlg.caption), 'podpis ról zawiera płeć — ' + dlg.caption);

  const fixedLines = await page.evaluate(() => {
    let fixed = 0, any = 0;
    window.DB.dialogues.forEach((d) => d.lines.forEach((l) => {
      if (l.speakerGender && l.speakerGender !== 'any') fixed++; else any++;
    }));
    return { fixed, any };
  });
  log(fixedLines.fixed > 0,
      'kwestii z płcią wynikającą ze scenariusza: ' + fixedLines.fixed +
      ' | podążających za ustawieniem: ' + fixedLines.any);

  /* ------------------------------------------------ 4. syntezator — kobieta */
  const spokenF = await page.evaluate(async () => {
    window.__spoken = [];
    const rec = window.DB.records.filter((r) => {
      if (!window.G.hasVariant(r)) return false;
      const male = window.DB.voiceText(r.ttsKey) || '';
      const fem = window.DB.voiceText((r.genderVariant.female || {}).ttsKey) || '';
      return male.indexOf('\u0e04\u0e23\u0e31\u0e1a') !== -1 && fem;
    })[0];
    window.Player.play(window.G.view(rec));
    await new Promise((r) => setTimeout(r, 120));
    return { text: window.__spoken[0] || '', id: rec.id, male: window.DB.voiceText(rec.ttsKey) };
  });
  log(spokenF.text.indexOf(TH_MALE) === -1 &&
      (spokenF.text.indexOf(TH_FEM_A) !== -1 || spokenF.text.indexOf(TH_FEM_Q) !== -1),
      'syntezator dostaje formę żeńską (rekord ' + spokenF.id + ')');

  /* ------------------------------------------ 5. szczegóły hasła — obie formy */
  const detail = await page.evaluate(async () => {
    const rec = window.DB.records.filter((r) => window.G.hasVariant(r))[0];
    window.App.openRecord(rec.id);
    await new Promise((r) => setTimeout(r, 60));
    const labels = Array.from(document.querySelectorAll('#sheet-body .gform-label'))
      .map((n) => n.textContent);
    const txt = document.querySelector('#sheet-body .gender-card').textContent;
    window.App.closeSheet();
    return { labels, hasMale: /khráp|phǒm/.test(txt), hasFem: /khâ|khá|chǎn/.test(txt) };
  });
  log(detail.labels.indexOf('forma męska') !== -1 && detail.labels.indexOf('forma żeńska') !== -1,
      'szczegóły hasła pokazują etykiety: ' + detail.labels.join(' / '));
  log(detail.hasMale && detail.hasFem, 'w szczegółach widać obie formy naraz');

  /* --------------------------------------------- 6. piąty tryb w Słuchaniu */
  await go(page, 'listen');
  const modeBtn = await page.$('[data-listen="gender"]');
  log(!!modeBtn, 'ekran Słuchanie ma piąty tryb „Forma męska czy żeńska?”');
  await modeBtn.click();
  await page.waitForTimeout(250);
  const listen = await page.evaluate(() => {
    const box = document.querySelector('#listen-area');
    const opts = Array.from(box.querySelectorAll('.opt')).map((b) => b.textContent);
    return { opts, txt: box.textContent, spoken: window.__spoken[window.__spoken.length - 1] || '' };
  });
  log(listen.opts.length === 2 && listen.opts.join('|').indexOf('Mówi kobieta') !== -1,
      'ćwiczenie daje wybór: ' + listen.opts.join(' / '));
  await page.evaluate(() => {
    Array.from(document.querySelectorAll('#listen-area .opt'))[0].click();
  });
  await page.waitForTimeout(150);
  const after = await page.evaluate(() => {
    const box = document.querySelector('#listen-area');
    return {
      graded: /Dobrze|Jeszcze raz/.test(box.textContent),
      both: box.querySelectorAll('.gform').length,
      marker: /sygnał płci/.test(box.textContent),
    };
  });
  log(after.graded, 'odpowiedź jest oceniana');
  log(after.both === 2, 'po odpowiedzi widać obie formy do porównania');
  log(after.marker, 'wskazane jest słowo, po którym słychać płeć');

  /* --------------------------------------- 7. przełączenie na formę męską */
  await page.evaluate(() => window.G.set('male'));
  await page.waitForTimeout(250);
  const chip = await page.textContent('#btn-gender-label');
  log(chip.trim() === 'mężczyzna', 'przełącznik w pasku pokazuje: ' + chip.trim());

  const maleReport = await walk('male');
  for (const r of maleReport) {
    if (r.id === 'dialogues') continue;
    log(!r.fem, 'ekran ' + r.id + ': brak form żeńskich przy ustawieniu „mężczyzna”');
  }
  const maleScreens = maleReport.filter((r) => r.male).map((r) => r.id);
  log(maleScreens.length >= 6, 'formy męskie faktycznie widoczne na ekranach: ' + maleScreens.join(', '));

  const spokenM = await page.evaluate(async () => {
    window.__spoken = [];
    const rec = window.DB.records.filter((r) => {
      if (!window.G.hasVariant(r)) return false;
      const male = window.DB.voiceText(r.ttsKey) || '';
      return male.indexOf('\u0e04\u0e23\u0e31\u0e1a') !== -1;
    })[0];
    window.Player.play(window.G.view(rec));
    await new Promise((r) => setTimeout(r, 120));
    return window.__spoken[0] || '';
  });
  log(spokenM.indexOf(TH_MALE) !== -1, 'syntezator dostaje formę męską po przełączeniu');

  /* ------------------------------------------- 8. trwałość wyboru po odświeżeniu */
  await page.reload({ waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => window.DB && window.DB.ready, null, { timeout: 60000 });
  await page.waitForTimeout(300);
  log(!(await page.isVisible('#gender-ask')), 'po odświeżeniu aplikacja nie pyta ponownie');
  const chip2 = await page.textContent('#btn-gender-label');
  log(chip2.trim() === 'mężczyzna', 'wybór przetrwał odświeżenie: ' + chip2.trim());

  /* --------------------------------------------------- 9. ustawienia */
  await go(page, 'settings');
  const setting = await page.evaluate(() => {
    const labels = Array.from(document.querySelectorAll('#settings-form .field span'))
      .map((n) => n.textContent);
    const sel = Array.from(document.querySelectorAll('#settings-form select'))
      .find((s) => Array.from(s.options).some((o) => o.value === 'female'));
    return { labels, options: sel ? Array.from(sel.options).map((o) => o.text) : [], value: sel && sel.value };
  });
  log(setting.labels[0] === 'Mówię jako',
      'w Ustawieniach pierwsze pole to: ' + setting.labels[0]);
  log(setting.options.join('/') === 'mężczyzna/kobieta',
      'wybór ma opcje: ' + setting.options.join(' / '));
  log(setting.value === 'male', 'pole pokazuje aktualny wybór: ' + setting.value);

  /* -------------------------------------------- 10. sekcja na ekranie Wymowa */
  await go(page, 'pron');
  const lesson = await page.evaluate(() => {
    const heads = Array.from(document.querySelectorAll('#pron-content h2')).map((n) => n.textContent);
    const card = Array.from(document.querySelectorAll('#pron-content .card'))
      .find((c) => /Płeć mówiącego/.test(c.textContent));
    return { heads, has: !!card, forms: card ? card.querySelectorAll('.gform').length : 0 };
  });
  log(lesson.has, 'ekran Wymowa ma sekcję o cząstkach i zaimkach zależnych od płci');
  log(lesson.forms === 2, 'sekcja pokazuje tę samą wypowiedź w obu formach');

  log(errors.length === 0, 'błędy w konsoli: ' + (errors.length ? errors.join(' | ') : 'brak'));

  await browser.close();
  console.log('  ---');
  console.log(failures ? '  WYNIK: ' + failures + ' niepowodzeń' : '  WYNIK: wszystko przeszło');
  process.exit(failures ? 1 : 0);
})();
