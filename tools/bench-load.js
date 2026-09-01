#!/usr/bin/env node
/* Pomiar czasu ladowania bazy Thai All-in-One w przegladarce.
   Uruchamia prawdziwy silnik Chromium, laduje index.html w dwoch trybach
   i mierzy czas od startu DB.load() do gotowosci bazy.

   Uzycie:  node tools/bench-load.js <url> <etykieta> [liczba prob]
*/
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');

(async () => {
  const url = process.argv[2];
  const label = process.argv[3] || url;
  const runs = parseInt(process.argv[4] || '3', 10);
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--allow-file-access-from-files', '--no-sandbox'],
  });
  const times = [];
  let stats = null;
  const errors = [];

  for (let i = 0; i < runs; i++) {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    page.on('pageerror', (e) => errors.push(String(e)));
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

    await page.goto(url, { waitUntil: 'domcontentloaded' });
    const res = await page.evaluate(async () => {
      const t0 = performance.now();
      // aplikacja moze juz ladowac dane sama — czekamy na gotowosc
      while (!window.DB) await new Promise((r) => setTimeout(r, 5));
      if (!window.DB.ready) {
        await new Promise((resolve) => {
          const tick = () => (window.DB.ready ? resolve() : setTimeout(tick, 5));
          tick();
        });
      }
      const t1 = performance.now();
      return {
        ms: t1 - t0,
        records: window.DB.records.length,
        dialogues: window.DB.dialogues.length,
        levels: window.DB.countByLevel,
        localMode: window.DB.localMode,
        // kontrola szczelnosci: czy ttsThai wyciekl do obiektow aplikacji?
        leaks: window.DB.records.filter((r) => 'ttsThai' in r).length,
      };
    });
    times.push(res.ms);
    stats = res;
    await ctx.close();
  }

  await browser.close();
  const avg = times.reduce((a, b) => a + b, 0) / times.length;
  console.log(JSON.stringify({
    label,
    url,
    runs,
    timesMs: times.map((t) => Math.round(t)),
    avgMs: Math.round(avg),
    minMs: Math.round(Math.min(...times)),
    maxMs: Math.round(Math.max(...times)),
    records: stats.records,
    dialogues: stats.dialogues,
    levels: stats.levels,
    localMode: stats.localMode,
    thaiLeaks: stats.leaks,
    errors: errors.slice(0, 5),
  }, null, 1));
})();
