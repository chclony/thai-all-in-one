# Sesja H — płeć mówiącego

Wersja danych: **1.8.0** (poprzednia: 1.7.0)

## Problem

W tajskim cząstka grzecznościowa kończąca wypowiedź i zaimek pierwszej osoby
zależą od **płci osoby mówiącej** — nie od płci rozmówcy i nie od rodzaju
gramatycznego słowa. Mężczyzna kończy zdanie `khráp` i mówi o sobie `phǒm`.
Kobieta kończy `khâ` (w pytaniu `khá`) i mówi `chǎn` albo — w rejestrze
formalnym — `dì-chǎn`. To obowiązek gramatyczny, nie wariant stylistyczny:
mężczyzna nie może powiedzieć `khâ`, kobieta nie może powiedzieć `khráp`.

Stan zastany w wersji 1.7.0:

| forma | w całym rekordzie | w głównym polu `thaiPhonetic` |
|---|---|---|
| khráp | 10 524 | 7 688 |
| khâ | 111 | **1** |
| phǒm | 4 794 | 3 788 |
| chǎn | 55 | 3 |
| dì-chǎn | 0 | **0** |

Rekordów kończących się na `khráp` — 7 501. Na `khâ` — jeden.
Formy `dì-chǎn` nie było w bazie ani razu, więc kobieta nie miała nawet skąd
wziąć zaimka do rozmowy w urzędzie. Kobieta ucząca się z takiej bazy
przyswajała formy, których nie może użyć.

## Rozwiązanie w danych

Rozszerzenie schematu, nie zmiana. Treść domyślna rekordu pozostaje formą
męską; forma żeńska trafia do nowego, **opcjonalnego** pola:

```json
"genderVariant": {
  "female": {
    "thaiPhonetic": "khàwp-khun khâ",
    "pronunciationPolish": "khop-khun kha",
    "ttsThai": "…",
    "toneGuide": "khàwp — ton niski; khun — ton średni; khâ — ton opadający"
  }
}
```

Rekordy bez form zależnych od płci pola nie mają. Żadne istniejące pole nie
zostało zmienione ani usunięte, więc starsza wersja aplikacji czyta bazę
dokładnie tak jak dotąd — po prostu ignoruje nieznany klucz.

**Odstępstwo od specyfikacji, świadome:** wariant zawiera czwarte pole
`toneGuide`. Bez niego ekran przy formie `khâ` wyświetlałby opis
„khráp — ton wysoki”, czyli wprost nieprawdę.

### Reguły przekształcenia

Kod: `tools/generators/gender_forms.py` (reguły) i `build-gender-variants.py`
(przebieg po bazie). Skrypt jest idempotentny — liczy warianty od nowa
z treści męskiej.

1. **Cząstka.** `khráp` → `khâ` w zdaniu oznajmującym, `khá` w pytaniu oraz po
   cząstce `ná`. Rozstrzygane po słowie poprzedzającym (`mǎi`, `nǎi`,
   `thâo-rài`, `yang-ngai`…) i po polskim znaku zapytania. W bazie wypadło to
   5 186 razy `khâ` i 2 502 razy `khá`.
2. **Zaimek.** `phǒm` → `chǎn` albo `dì-chǎn` zależnie od pola `register`:
   `formalny` → `dì-chǎn` (510 rekordów), pozostałe → `chǎn` (3 276).
   Różnica opisana w polu `notes` każdego rekordu, którego dotyczy.
3. **Pismo tajskie.** `ครับ` → `ค่ะ` / `คะ`, `ผม` → `ฉัน` / `ดิฉัน`,
   pozycyjnie, w kolejności wystąpień.

### Pułapki, które trzeba było obsłużyć osobno

- **`phǒm` to także rzeczownik „włosy”.** `yaa sà phǒm` (szampon),
  `wǐi phǒm` (czesać się), `phǒm nùeng sên` (jeden włos). Ślepa zamiana dałaby
  „szampon mnie”. Rozpoznawane po słowie poprzedzającym i po polskim
  tłumaczeniu; te rekordy wariantu nie dostają. W zdaniu
  `phǒm yàak tàt phǒm khráp` pierwsze `phǒm` się zmienia, drugie nie.
- **Znak powtórzenia `ๆ`.** Zapis `ครับๆ` to dwa `khráp` w fonetyce i jedno
  `ครับ` w piśmie. Osobna ścieżka.
- **Hasła o samej formie.** `ja (mężczyzna)`, `partykuła grzecznościowa
  (kobieta)`, wzorzec `Dziękuję (mężczyzna).` w lekcji o cząstkach — tutaj
  nawias jest znaczeniem hasła, nie etykietą. Cztery takie wpisy dostały
  znacznik `genderLexicon: true` i **nie** przełączają się razem z resztą;
  inaczej ekran pokazałby „ja (mężczyzna) — chǎn”.
- **Etykiety `(mężczyzna)` doklejone do zdań przykładowych** — 43 sztuki,
  w rodzaju „Grzecznie: dziękuję (mężczyzna).”. Były obejściem dla bazy, która
  nie znała płci mówiącego. Teraz płeć niesie struktura rekordu, więc etykieta
  stała się zbędna i sprzeczna z treścią w formie żeńskiej. Usunięte.

### Dialogi

Każdy dialog ma pole `roleGender`, każda kwestia — `speakerGender`:

| oznaczenie | ról | znaczenie |
|---|---|---|
| `female` | 33 | płeć wynika ze scenariusza (Kelnerka, Recepcjonistka, Farmaceutka…) |
| `male` | 70 | j.w. (Kelner, Policjant, Konduktor…) |
| `any` | 265 | rola opisana bezosobowo (Turysta, Klient, Pasażer) — podąża za ustawieniem |

Role oznaczone rzeczownikiem rodzaju męskiego, ale w praktyce bezosobowym
(Turysta, Klient, Lekarz, Pracownik), zostały świadomie przy `any`.

451 kwestii ma płeć przesądzoną przez scenariusz i brzmi poprawnie od razu,
niezależnie od ustawienia. Przy okazji poprawiono **24 kwestie**, w których
kelnerka mówiła `khráp`, i **11**, w których mężczyzna mówił `khâ`.

## Rozwiązanie w aplikacji

Nowy moduł `js/gender.js` jest jedynym miejscem, które wie o istnieniu
`genderVariant`. Ekrany wołają `G.view(obiekt)` i dostają gotową treść razem
z właściwym kluczem głosu. Żaden ekran nie sięga do wariantu sam, więc nie da
się przypadkiem zostawić któregoś przy formie męskiej.

- **Pytanie przy pierwszym uruchomieniu**, przed pierwszym zdaniem. Wybór
  w `localStorage` pod kluczem `thaiaio.gender`.
- **Wybór w Ustawieniach** jako pierwsze pole, oraz szybki przełącznik
  w pasku górnym (♀/♂ z etykietą).
- **Szczegóły hasła** pokazują obie formy z etykietami „forma męska” i
  „forma żeńska”, każdą z osobnym przyciskiem odsłuchu.
- **Ekran Wymowa i tony** ma sekcję „Płeć mówiącego: cząstki i zaimki”
  z wyjaśnieniem systemu i tą samą wypowiedzią w obu formach.
- **Wyszukiwarka** indeksuje także formę żeńską — bez tego hasła `chǎn` czy
  `khâ` nie dałoby się znaleźć.
- **Syntezator** dostaje `ttsThai` z właściwego wariantu.

### Nowy tryb ćwiczenia

Ekran Słuchanie ma piąty tryb: **„Forma męska czy żeńska?”**. Użytkownik
słyszy wypowiedź w losowo wybranej formie i wskazuje płeć mówiącego.
Po odpowiedzi widzi obie formy obok siebie z zaznaczeniem słowa, po którym
płeć słychać. Ćwiczy to cechę, której w polszczyźnie nie ma — sygnał płci
niesiony przez samą wypowiedź, a nie przez końcówkę fleksyjną.

## Kontrola w walidatorze

`tools/validate.py` ma nową regułę: tekst zawierający `khráp` albo `phǒm`
**musi** mieć `genderVariant.female`; brak = błąd walidacji. Sprawdzane jest
też, czy wariant nie zawiera resztek formy męskiej i czy ma dane TTS.

Wyjątki, wyliczone i uzasadnione: trzy rekordy z `phǒm` w znaczeniu „włosy”,
wpisy oznaczone `genderLexicon`, oraz kwestie dialogów o `speakerGender: male`.

Test negatywny: po usunięciu wariantu z dwóch rekordów walidator zgłasza
dokładnie te dwa.

## Wyniki

```
python3 tools/validate.py
  RAZEM rekordów słownika      10755
  dialogów                       184
  tekstów z wariantem żeńskim  21255
  Błędy: 0 | Ostrzeżenia: 0
  WYNIK: BAZA POPRAWNA
```

| miara | przed | po |
|---|---|---|
| rekordów z wariantem żeńskim | 1 | **8 407** |
| przykładów z wariantem | 0 | **11 697** |
| kwestii dialogu z wariantem | 0 | **1 155** |
| dialogów z oznaczoną płcią ról | 0 | **85** ze 184 |
| wystąpień `dì-chǎn` | 0 | **510** |

## Testy

- `tools/gender-test.js` — nowy, 44 kontrole, przechodzi w obu trybach
  (`file://` i serwer http): pytanie przy starcie, zapis wyboru, dziesięć
  ekranów w obu ustawieniach, treść syntezatora, obie formy w szczegółach,
  nowy tryb ćwiczenia, trwałość po odświeżeniu.
- `tools/browser-test.js` — istniejący zestaw regresyjny, bez zmian
  w wyniku: wszystkie testy zaliczone, `file://` i http.
- `tools/audit.py` — bez zastrzeżeń.
- `tools/audit-quality.py` — 13 uwag, dokładnie tyle samo co przed sesją
  (duplikaty polskich haseł sprzed sesji H, nietknięte).

## Znane ograniczenia

- Rozpoznawanie „`phǒm` = włosy” opiera się na słowie poprzedzającym i polskim
  tłumaczeniu. Przy dopisywaniu nowych haseł o fryzjerstwie warto sprawdzić
  wynik walidacji.
- Zaimek dobierany jest z pola `register`. Rekordy oznaczone `uprzejmy`
  dostają `chǎn` — to poprawne w rozmowie, ale w piśmie urzędowym kobieta
  napisałaby `dì-chǎn`. Różnica opisana w `notes`.
- Cztery hasła `genderLexicon` nie pokazują drugiej formy w bloku porównania,
  bo jej nie mają — odpowiednik jest osobnym hasłem w słowniku.
- Nagranie lektora (`audioFile`) dla formy męskiej nie pasuje do żeńskiej,
  więc w wariancie żeńskim oddajemy głos syntezatorowi. Obecnie baza nie ma
  jeszcze nagrań, więc nie ma to skutku praktycznego.
