/* Thai All-in-One — service worker.
   Powłoka aplikacji: cache-first (szybki start offline).
   Dane JSON: network-first z zapasem z cache (świeże dane po aktualizacji bazy). */

var VERSION = 'thai-aio-v1.20.0';
var SHELL_CACHE = VERSION + '-shell';
var DATA_CACHE = VERSION + '-data';

var SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './css/style.css',
  './js/utils.js',
  './js/data-loader.js',
  './js/gender.js',
  './js/speech.js',
  './js/dsp.js',
  './js/capture.js',
  './js/audio.js',
  './js/pitch.js',
  './js/pitch-worker.js',
  './js/tone-score.js',
  './js/pron-view.js',
  './js/search.js',
  './js/srs.js',
  './js/quiz.js',
  './js/scenes.js',
  './js/extensive.js',
  './js/comprehension.js',
  './js/numbers.js',
  './js/rescue.js',
  './js/grammar-stats.js',
  './js/grammar.js',
  './js/coverage.js',
  './js/production.js',
  './js/course.js',
  './js/perception.js',
  './js/placement.js',
  './js/exam.js',
  './js/exam-view.js',
  './js/checkpoint.js',
  './js/progress.js',
  './js/progress-migration.js',
  './js/stats.js',
  './js/goals.js',
  './js/session.js',
  './js/retro.js',
  './js/module-zero-view.js',
  './js/app.js',
  './assets/icons/icon.svg',
  './assets/icons/icon-180.png',
  './assets/icons/icon-192.png',
  './assets/icons/icon-512.png',
  './data/manifest.json',
  './data/metadata.json',
  './data/categories.json',
  './data/pronunciation.json',
  './data/grammar.json',
  './data/module-zero.json',
  /* Mapa migracji postępu. Wchodzi do powłoki, a nie do danych, bo bez niej
     pierwsze uruchomienie po aktualizacji nie przeniosłoby postępu — a to jest
     dokładnie ten moment, w którym service worker może jeszcze nie mieć
     świeżych danych. */
  './data/progress-migration.json',
  /* Zestawy egzaminacyjne i próbki kontrolne. Wchodzą do powłoki, a nie do
     danych na żądanie, bo ekran „Dzisiaj” czyta z nich kartę kamienia
     milowego przy każdym starcie — także bez sieci. Razem 230 kB. */
  './data/exams.json',
  './data/checkpoints.json'
];

/* Uwaga: kopie data/*.js służą wyłącznie trybowi file:// (otwarcie z dysku),
   w którym service worker w ogóle nie działa — dlatego nie ma ich w cache. */

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(SHELL_CACHE).then(function (cache) {
      /* Pojedynczy brakujący plik nie może wywrócić instalacji. */
      return Promise.all(SHELL.map(function (url) {
        return cache.add(url).catch(function () { return null; });
      }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) {
        return k.indexOf(VERSION) !== 0;
      }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (event) {
  var request = event.request;
  if (request.method !== 'GET') return;
  var url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  /* Dane: najpierw sieć, potem cache. */
  if (url.pathname.indexOf('/data/') !== -1) {
    event.respondWith(
      fetch(request).then(function (response) {
        var copy = response.clone();
        caches.open(DATA_CACHE).then(function (c) { c.put(request, copy); });
        return response;
      }).catch(function () {
        return caches.match(request).then(function (hit) {
          /* Bez zapisanej kopii oddajemy błąd 503, a nie pustą odpowiedź —
             dzięki temu aplikacja odnotuje brak pliku i powie o tym wprost,
             zamiast pokazywać poziom bez haseł. */
          return hit || new Response('', { status: 503, statusText: 'Brak kopii offline' });
        });
      })
    );
    return;
  }

  /* Nawigacja: offline wracamy do powłoki aplikacji. */
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(function () {
        return caches.match('./index.html').then(function (hit) {
          return hit || new Response('Brak połączenia i brak zapisanej kopii aplikacji.', {
            headers: { 'Content-Type': 'text/plain; charset=utf-8' }
          });
        });
      })
    );
    return;
  }

  /* Reszta: najpierw cache. */
  event.respondWith(
    caches.match(request).then(function (hit) {
      if (hit) return hit;
      return fetch(request).then(function (response) {
        if (response.ok && response.type === 'basic') {
          var copy = response.clone();
          caches.open(SHELL_CACHE).then(function (c) { c.put(request, copy); });
        }
        return response;
      }).catch(function () {
        return new Response('', { status: 504 });
      });
    })
  );
});
