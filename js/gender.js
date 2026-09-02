/* Thai All-in-One — płeć mówiącego.

   W tajskim cząstka grzecznościowa i zaimek „ja” zależą od płci osoby mówiącej.
   Mężczyzna kończy zdanie khráp i mówi o sobie phǒm, kobieta kończy khâ
   (w pytaniu khá) i mówi chǎn albo — w rejestrze formalnym — dì-chǎn.
   To obowiązek gramatyczny, nie wariant stylistyczny.

   Baza trzyma formę męską jako treść domyślną, a formę żeńską w opcjonalnym
   polu genderVariant.female. Ten moduł jest jedynym miejscem, które o tym wie:
   ekrany wołają G.view(obiekt) i dostają gotową treść do wyświetlenia oraz
   właściwy klucz głosu. Dzięki temu nie ma ryzyka, że jakiś ekran zostanie
   przy formie męskiej — bo żaden ekran nie sięga do genderVariant sam.

   Uwaga na kolejność ładowania: data-loader wycina pola ttsThai (także te
   wewnątrz genderVariant) i zostawia w ich miejsce ttsKey. Tutaj pracujemy
   już na ttsKey. */
(function (global) {
  'use strict';

  var KEY = 'gender';                 // localStorage, przez U.store
  var VALUES = ['female', 'male'];

  var G = {
    value: null,          // 'female' | 'male' | null (jeszcze nie zapytano)
    listeners: []
  };

  G.isSet = function () { return VALUES.indexOf(G.value) !== -1; };

  /* Gdy użytkownik jeszcze nie odpowiedział, pokazujemy formę męską —
     tak wygląda treść domyślna rekordu. Pytanie i tak pojawi się przy starcie. */
  G.current = function () { return G.isSet() ? G.value : 'male'; };

  G.label = function (v) {
    return (v || G.current()) === 'female' ? 'kobieta' : 'mężczyzna';
  };

  G.load = function () {
    var stored = U.store.get(KEY, null);
    G.value = VALUES.indexOf(stored) !== -1 ? stored : null;
    return G.value;
  };

  G.set = function (v) {
    if (VALUES.indexOf(v) === -1) return;
    G.value = v;
    U.store.set(KEY, v);
    G.listeners.forEach(function (fn) { try { fn(v); } catch (e) {} });
  };

  G.onChange = function (fn) { if (typeof fn === 'function') G.listeners.push(fn); };

  /* ------------------------------------------------------------- warianty */

  G.variant = function (item) {
    return (item && item.genderVariant && item.genderVariant.female) || null;
  };

  G.hasVariant = function (item) { return !!G.variant(item); };

  /* Czy dana pozycja w ogóle zależy od płci — także wtedy, gdy jest zapisana
     od razu w formie żeńskiej (kwestia kelnerki) albo męskiej (kwestia kelnera). */
  G.isGendered = function (item) {
    if (!item) return false;
    if (G.hasVariant(item)) return true;
    return !!(item.speakerGender && item.speakerGender !== 'any');
  };

  /* Która płeć obowiązuje dla tej pozycji.
     Kwestia dialogu z rolą o ustalonej płci ma swoją własną, niezależną od
     ustawienia użytkownika — kelnerka mówi po kobiecemu także wtedy, gdy
     uczy się mężczyzna. */
  G.speakerOf = function (item, override) {
    if (item && item.speakerGender && item.speakerGender !== 'any') return item.speakerGender;
    if (override && VALUES.indexOf(override) !== -1) return override;
    return G.current();
  };

  /* Zwraca obiekt gotowy do wyświetlenia i odtworzenia.
     Nigdy nie modyfikuje oryginału — ekrany dostają płytką kopię z podmienioną
     fonetyką, zapisem polskim, opisem tonów i kluczem głosu. */
  G.view = function (item, override) {
    if (!item) return item;
    if (G.speakerOf(item, override) !== 'female') return item;
    var v = G.variant(item);
    if (!v) return item;
    var out = {};
    Object.keys(item).forEach(function (k) { out[k] = item[k]; });
    if (v.thaiPhonetic) out.thaiPhonetic = v.thaiPhonetic;
    if (v.pronunciationPolish) out.pronunciationPolish = v.pronunciationPolish;
    if (v.toneGuide) out.toneGuide = v.toneGuide;
    if (v.ttsKey) out.ttsKey = v.ttsKey;
    /* Granice wyrazów i wariant potoczny należą do konkretnej formy —
       forma żeńska ma inną cząstkę, więc i inny podział, i inną redukcję. */
    out.ttsSplit = v.ttsSplit || null;
    out.colloquial = v.colloquial || null;
    /* Nagranie lektora dla formy męskiej nie pasuje do formy żeńskiej —
       lepiej oddać głos syntezatorowi niż przeczytać nie to zdanie. */
    if (item.audioFile) out.audioFile = '';
    out.__gender = 'female';
    return out;
  };

  G.viewAll = function (items, override) {
    return (items || []).map(function (i) { return G.view(i, override); });
  };

  /* Obie formy naraz — do ekranu szczegółów hasła. Zwraca null, jeżeli hasło
     nie zależy od płci. */
  G.pair = function (item) {
    if (!item) return null;
    var fixed = item.speakerGender && item.speakerGender !== 'any' ? item.speakerGender : null;
    var v = G.variant(item);
    if (!v && !fixed) return null;
    if (fixed === 'female') {
      return { female: item, male: null, fixed: 'female' };
    }
    if (fixed === 'male') {
      return { male: item, female: null, fixed: 'male' };
    }
    return { male: item, female: G.view(item, 'female'), fixed: null };
  };

  global.G = G;
})(window);
