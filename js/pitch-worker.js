/* Wątek roboczy oceny wymowy.

   Liczy dokładnie to samo, co Pitch.analyse w wątku głównym — ten sam plik
   pitch.js, wczytany przez importScripts, więc nie ma dwóch implementacji,
   które mogłyby się rozjechać. Powód istnienia: analiza nagrania 3 s zajmuje
   przy dławieniu CPU x4 około 166 ms, a przez ten czas wątek główny nie
   obsługuje ani przewijania, ani kliknięć — w chwili, gdy uczący się czeka
   na ocenę wymowy.

   Gdy wątku roboczego nie da się utworzyć (file://, starsze przeglądarki),
   Pitch.analyseAsync liczy w wątku głównym i zwraca tę samą obietnicę. */

importScripts('pitch.js');

self.onmessage = function (ev) {
  var d = ev.data || {};
  if (d.cmd !== 'analyse') return;
  try {
    var result = Pitch.analyse(d.samples, d.rate, d.opts || undefined);
    self.postMessage({ id: d.id, ok: true, result: result });
  } catch (err) {
    self.postMessage({
      id: d.id, ok: false,
      error: String((err && err.message) || err)
    });
  }
};
