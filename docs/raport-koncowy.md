# Raport końcowy — Thai All-in-One

**Data pomiaru: 1 września 2026. Sesja zamykająca projekt.**

Wszystkie liczby w tym dokumencie pochodzą z pomiaru wykonanego w tej sesji,
nie z wcześniejszych raportów. Tam, gdzie wynik różni się od wcześniej
publikowanego, różnica jest pokazana i wyjaśniona. Pomiar powtórzysz poleceniem:

```bash
python3 tools/final-metrics.py
```

Raport jest podzielony na dwie części. Pierwsza (rozdziały 1–8) opisuje, co
w projekcie jest, i jest chwaleniem się. Druga (rozdziały 9–11) opisuje, czego
nie ma, i jest jedyną częścią, którą naprawdę trzeba przeczytać przed podjęciem
decyzji, czy uczyć się z tego materiału.

---

## Spis treści

1. [Objętość](#1-objętość)
2. [Inwentarz sylabiczny](#2-inwentarz-sylabiczny)
3. [Rozkłady](#3-rozkłady)
4. [Ekrany i tryby ćwiczeń](#4-ekrany-i-tryby-ćwiczeń)
5. [Czas startu na przestrzeni sesji](#5-czas-startu-na-przestrzeni-sesji)
6. [Brak pisma tajskiego — weryfikacja testem](#6-brak-pisma-tajskiego--weryfikacja-testem)
7. [Stan testów](#7-stan-testów)
8. [Różnice wobec sesji V](#8-różnice-wobec-sesji-v)
9. [Pokrycie mowy potocznej](#9-pokrycie-mowy-potocznej)
10. [Stan weryfikacji językowej](#10-stan-weryfikacji-językowej)
11. [Uczciwa ocena: co uczący się będzie rozumiał, a czego nie](#11-uczciwa-ocena-co-uczący-się-będzie-rozumiał-a-czego-nie)
12. [Co zostało naprawione w tej sesji](#12-co-zostało-naprawione-w-tej-sesji)

---

## 1. Objętość

| Miara | Wartość |
|---|---:|
| rekordy słownika | **20 791** |
| hasła leksykalne (word / noun / verb / adjective / adverb) | **3512** |
| przykłady zdań | **25 196** |
| w tym unikalnych | 17 968 |
| dialogi | **184** |
| kwestie w dialogach | 1682 |
| sceny | **61** |
| kwestie w scenach | 1682 |
| pytania do scen | 529 |
| lekcje ścieżki nauki | **333** |
| rozdziały | 23 |
| hasła wprowadzane przez ścieżkę | 3014 |
| tematy gramatyczne | 81 |
| wzorce gramatyczne | 483 |
| ćwiczenia gramatyki ze słuchu | 1490 |
| ćwiczenia przekształceń | 1589 |
| luki do uzupełnienia w dialogach | 1631 |
| zadania wnioskowania | 169 |
| klasyfikatory | 139 |
| pozycje liczbowe | 165 |
| zestawy egzaminacyjne | 15 |
| próbki kontrolne | 15 |
| scenariusze ratowania rozmowy | 14 |
| lekcje Modułu 0 (trening słuchu) | 12 |
| zadania Modułu 0 | 260 |
| kontrasty fonetyczne | 26 w 7 rodzinach |
| pozycje w indeksie czołowym | 4827 |

### Dlaczego to nie jest jedna suma

Powyższe liczby są celowo rozdzielone i nie sumują się do „ilu jest rekordów”.
Rekord słownikowy, dialog, lekcja i ćwiczenie gramatyczne to cztery różne
jednostki mieszkające w różnych plikach. Zsumowanie ich dałoby liczbę większą
i bardziej efektowną, ale nie znaczącą nic — bo nie wiadomo, czego byłaby miarą.

Podobnie **rekord to nie hasło**. 67,7% rekordów to zdania: materiał ćwiczeniowy
zbudowany wokół haseł, nie same hasła. Zasób słownictwa tej bazy to 3512 haseł,
a nie 20 791 rekordów, i tylko ta pierwsza liczba mówi cokolwiek o tym, ile
uczący się będzie umiał.

---

## 2. Inwentarz sylabiczny

**1977 unikalnych tokenów sylabicznych na 125 232 wystąpienia.**

Krzywa pokrycia — jaki odsetek wszystkich wystąpień pokrywa N najczęstszych sylab:

| Sylab | Pokrycie |
|---:|---:|
| 50 | 54,88% |
| 100 | 64,83% |
| 200 | **75,25%** |
| 300 | 81,41% |
| 500 | 88,89% |
| 750 | 93,74% |
| 1000 | **96,40%** |
| 1250 | 97,99% |
| 1500 | **99,12%** |
| 1750 | 99,82% |
| 1977 | 100,00% |

### Inwentarz sylabiczny jest praktycznie domknięty

To najmocniejszy wynik całego projektu i warto rozumieć dlaczego.

Tajski jest językiem o zamkniętym zasobie sylab — liczba dopuszczalnych
kombinacji spółgłoska–samogłoska–ton–wygłos jest skończona i niewielka.
Kształt krzywej powyżej pokazuje, że baza ten zasób w praktyce wyczerpała:
1500 sylab pokrywa 99,1% materiału, a ostatnie 477 sylab wnosi mniej niż
jeden procent.

Konsekwencja dla uczącego się jest konkretna: **po przejściu kursu nie będzie
napotykał dźwięków, których nigdy nie słyszał.** Nowe słowo będzie dla niego
nieznane znaczeniowo, ale nie fonetycznie — usłyszy je poprawnie, powtórzy
poprawnie i zapisze poprawnie w zapisie fonetycznym, nawet nie wiedząc, co
znaczy. To jest różnica między „nie rozumiem tego słowa” a „nie usłyszałem
tego słowa”, i tylko ta druga sytuacja blokuje naukę w kontakcie z językiem.

Domknięcie inwentarza jest też powodem, dla którego rozszerzanie bazy przestało
mieć sens fonetyczny. Każde kolejne tysiąc rekordów wnosi statystycznie zero
nowych sylab. To, czego brakuje, to nie dźwięki — to słowa, co jest tematem
rozdziału 9.

---

## 3. Rozkłady

### Według poziomu

| Poziom | Rekordy | Udział | Hasła leksykalne | Dialogi | Lekcje |
|---|---:|---:|---:|---:|---:|
| Survival | 778 | 3,7% | 273 | 26 | 29 |
| A1 | 4049 | 19,5% | 851 | 38 | 73 |
| A2 | 9561 | 46,0% | 2051 | 40 | 99 |
| B1 | 4219 | 20,3% | 337 | 40 | 70 |
| B2 | 2184 | 10,5% | 0 | 40 | 62 |
| **razem** | **20 791** | 100% | **3512** | **184** | **333** |

Rozkład jest wyraźnie skrzywiony w stronę A2 — 46% materiału. To nie przypadek
ani błąd: A2 jest poziomem, na którym leży rdzeń mowy codziennej, i to tam
kierowano trzy kolejne sesje rozbudowy. Skrzywienie ma jednak drugą stronę,
widoczną w kolumnie haseł leksykalnych: **B2 nie wnosi ani jednego nowego
hasła słownikowego.** Materiał B2 to w całości zdania, rejestry i idiomy
zbudowane ze słownictwa wprowadzonego wcześniej. Poziom B2 uczy więc używać
znanych słów w trudniejszy sposób, a nie nowych słów.

### Według typu rekordu

| Typ | Liczba | Udział |
|---|---:|---:|
| sentence | 14 079 | 67,7% |
| question | 1671 | 8,0% |
| word | 1529 | 7,4% |
| noun | 1367 | 6,6% |
| phrase | 1124 | 5,4% |
| collocation | 405 | 1,9% |
| verb | 387 | 1,9% |
| adjective | 141 | 0,7% |
| adverb | 88 | 0,4% |

### Według rejestru

| Rejestr | Liczba | Udział |
|---|---:|---:|
| neutralny | 17 657 | 84,9% |
| formalny | 1593 | 7,7% |
| uprzejmy | 1025 | 4,9% |
| nieformalny | 269 | 1,3% |
| potoczny | 247 | 1,2% |

Rejestr potoczny i nieformalny to razem 2,5% materiału. Przy projekcie, którego
celem jest rozumienie **mowy potocznej**, to jest dysproporcja, którą trzeba
nazwać. Wracam do niej w rozdziale 11.

### Według kategorii

| Kategoria | Rekordy | Udział | Hasła leksykalne |
|---|---:|---:|---:|
| Praca i nauka | 2146 | 10,3% | 233 |
| Cechy i opinie | 2092 | 10,1% | 281 |
| Czasowniki | 1975 | 9,5% | 441 |
| Gramatyka użytkowa | 1908 | 9,2% | 145 |
| Small talk | 1503 | 7,2% | 244 |
| Awarie i pomoc | 1187 | 5,7% | 138 |
| Zakupy i pieniądze | 1180 | 5,7% | 209 |
| Jedzenie i napoje | 1022 | 4,9% | 195 |
| Miejsca i orientacja | 848 | 4,1% | 148 |
| Pytania | 837 | 4,0% | 101 |
| Dom i codzienność | 778 | 3,7% | 217 |
| Podstawy i grzeczność | 692 | 3,3% | 65 |
| Zdrowie | 672 | 3,2% | 163 |
| Transport | 671 | 3,2% | 143 |
| Pogoda i przyroda | 613 | 2,9% | 164 |
| Ludzie i rodzina | 593 | 2,9% | 138 |
| Czas i daty | 587 | 2,8% | 174 |
| Liczby i liczenie | 525 | 2,5% | 140 |
| Restauracja | 509 | 2,4% | 91 |
| Hotel | 453 | 2,2% | 82 |

---

## 4. Ekrany i tryby ćwiczeń

**24 ekrany w 6 grupach.**

| Grupa | Ekrany |
|---|---|
| Codziennie | Dzisiaj, Sesja dnia, Kurs, Powtórki |
| Ćwiczenia | Moduł 0 — trening słuchu, Słuchanie, Mówienie po tajsku, Powtarzaj za wzorem, Gramatyka, Liczby w mowie, Ratowanie rozmowy |
| Materiały | Słownik i zwroty, Dialogi, Sceny, Słuchanie ekstensywne, Tony i wymowa — przewodnik |
| Sprawdziany | Test poziomujący, Egzamin poziomowy, Próbki kontrolne, Sesja naprawcza |
| Postęp | Postęp, Tydzień, Droga do celu |
| Aplikacja | Ustawienia |

**19 trybów ćwiczeń** rozłożonych na trzy ekrany:

| Ekran | Tryby | Liczba |
|---|---|---:|
| Mówienie po tajsku | układanie zdania, wpisywanie, klasyfikatory, ton, wymowa na głos, scenka | 6 |
| Gramatyka | mapa, struktura zdania, przekształcenia, partykuły, przewodnik | 5 |
| Słuchanie | wybór, dyktando, składanie, wyławianie, płeć mówiącego, w hałasie, luka, nieznane słowo | 8 |

Do tego sześć typów zadań Modułu 0 (`same-diff`, `odd-one-out`, `tone-scale`,
`count-syllables`, `vowel-length`, `aspiration`) i sześć rodzajów drylu
liczbowego (dyktando, cena, godzina, produkcja, reszta, ciąg cyfr).

Egzamin poziomowy mierzy cztery sprawności osobno, każdą z własnym progiem:
rozumienie ze słuchu (próg 70%), rozumienie szczegółowe (65%), produkcja ustna
(60% kontur tonalny / 70% treść), produkcja pisemna (60%). Poziom jest zaliczony
dopiero wtedy, gdy wszystkie cztery przekroczą swój próg — średnia nie zalicza.

---

## 5. Czas startu na przestrzeni sesji

Wszystkie pomiary: Chromium przez Playwright, **dławienie CPU ×4**, mediana
z pięciu prób, do momentu gotowości do użycia.

| Sesja / stan | `file://` | serwer HTTP |
|---|---:|---:|
| etap 6, przed dwuetapowym ładowaniem | 403 ms | 644 ms |
| etap 6, po dwuetapowym ładowaniu | 618 ms | 822 ms |
| sesja N (15 285 rekordów) | 1001 ms | 1656 ms |
| sesja O, indeks w całości (20 791 rekordów) | 1202 ms | 1916 ms |
| sesja O, po podziale indeksu | 832 ms | 1178 ms |
| sesja V (odniesienie) | 766 ms | 1097 ms |
| **ta sesja, pierwsze uruchomienie** | **838 ms** | **1107 ms** |
| **ta sesja, powrót uczącego się** | **789 ms** | **1215 ms** |

Z pełnym indeksem dociąganym w tle:

| Stan | serwer, pierwsze uruchomienie | serwer, powrót |
|---|---:|---:|
| sesja V (odniesienie) | 1360 ms | 1887 ms |
| **ta sesja** | **1579 ms** | **1746 ms** |

Pomiar powtórzysz poleceniem `python3 tools/bench-start.py --dlawienie 4`.

### Interpretacja

**Start jest w normie i nie cofnął się w żadnym istotnym wymiarze.** Największe
odchylenie wobec sesji V to +16% (serwer z pełnym indeksem, pierwsze
uruchomienie: 1579 ms wobec 1360 ms), największa poprawa to −7% (serwer z pełnym
indeksem, powrót: 1746 ms wobec 1887 ms). Pozostałe cztery scenariusze mieszczą
się w przedziale −0% do +9%. Przy medianie z pięciu prób i rozrzucie
pojedynczych przebiegów rzędu 200 ms te różnice są w większości szumem pomiaru,
a nie regresją — narzędzie kwalifikuje wszystkie sześć scenariuszy jako
mieszczące się w normie.

Historia w tabeli pokazuje jednak coś ważniejszego niż bieżący wynik: **dwa razy
projekt zbliżył się do progu 2 s i dwa razy trzeba było zmienić architekturę
ładowania, żeby się cofnąć.** Raz w etapie 6 (dwuetapowe ładowanie zamiast
wczytywania całej bazy), raz w sesji O (podział indeksu na czołowy i resztę,
gdy mediana przez serwer podeszła pod 1,9 s). Wąskim gardłem za każdym razem
był transfer, nie procesor: pobranie 3,6 MB indeksu kosztowało 865 ms, podczas
gdy sparsowanie go — 77 ms, a zbudowanie z niego obiektów — 33 ms.

Wniosek na przyszłość, gdyby ktoś projekt kiedyś wznowił: przy obecnej
architekturze każde kolejne ~5000 rekordów doda ok. 200 ms do startu przez
serwer, a zapas do progu 2 s wynosi dziś ok. 250 ms w najgorszym mierzonym
scenariuszu. **Baza nie może już urosnąć znacząco bez trzeciej zmiany sposobu
ładowania.**

---

## 6. Brak pisma tajskiego — weryfikacja testem

Główna obietnica projektu brzmi: uczący się nigdy nie widzi znaku tajskiego.
Przez trzynaście sesji ta obietnica była w raportach zdaniem oznajmującym.
Zdanie oznajmujące nie jest dowodem. W tej sesji powstało narzędzie
`tools/thai-script-check.py`, które ją sprawdza, i zostało wpięte do zestawu
testów jako etap `tajski`.

```bash
python3 tools/thai-script-check.py
```

Test sprawdza trzy rzeczy niezależnie, bo każda może pęknąć osobno.

### Etap 1 — dane

Rekurencyjny obchód **wszystkich pól wszystkich rekordów w 50 plikach danych**.
W bazie jest **2 058 041 znaków tajskich** — muszą tam być, bo bez nich
syntezator mowy nie ma czego powiedzieć. Umowa brzmi: wolno im leżeć wyłącznie
w polach `ttsThai` i `thaiScript`. Lista zwolnień jest zamknięta i wpisana
w kod testu, więc nowe pole z tajskim obleje test, dopóki ktoś świadomie go
tam nie dopisze.

**Wynik: 0 wycieków poza pola zwolnione.**

### Etap 2 — interfejs

Aplikacja ładowana w przeglądarce, obchód **24 ekranów i 19 trybów ćwiczeń**,
czytanie `innerText` (a nie `innerHTML` — liczy się to, co widzi oko), plus
osobne sprawdzenie obudowy aplikacji: nawigacji, nagłówka i stopki.

**Wynik: 0 wycieków.**

### Etap 3 — eksporty dla uczącego się

Uczący się może wynieść z aplikacji dwie rzeczy, i obie ogląda się poza
aplikacją, gdzie filtr widoku już nie działa.

| Eksport | Zakres testu | Wycieki |
|---|---|---:|
| talia CSV do Anki | 1200 rekordów, 209 933 znaki | **0** |
| kopia postępu JSON | 800 kart, 120 wpisów dziennika, 128 509 znaków | **0** |
| indeks wyszukiwarki (to, co widać w słowniku) | 20 791 pozycji, 8 619 139 znaków | **0** |

Kartoteka i dziennik powtórek są przed pomiarem sztucznie zapełniane, a każda
karta oceniana dwukrotnie. Bez tego test przechodziłby dlatego, że nie ma czego
eksportować, a nie dlatego, że eksport jest czysty — dziennik powtórek dostaje
wpis dopiero przy drugim podejściu do karty.

### Wynik zbiorczy

**96 sprawdzeń, 0 wycieków. Obietnica dotrzymana i od tej sesji pilnowana
automatycznie** — zmiana w `data/`, `js/` lub `index.html` unieważnia zapamiętany
wynik tego etapu i każe go przeliczyć.

---

## 7. Stan testów

Pełny przebieg: `python3 tools/run-all-tests.py`

| Etap | Wynik | Zadań | Asercji | Czas |
|---|---|---:|---:|---:|
| `validate` — walidacja bazy | przeszedł | 1/1 | 68 | 14,1 s |
| `function` — test działania | przeszedł | 1/1 | 334 | 37,0 s |
| `a11y` — dostępność | przeszedł | 8/8 | 384 | 1 min 08 s |
| `zoom` — powiększenie i redukcja ruchu | przeszedł | 1/1 | 216 | 17,0 s |
| `browser` — test w przeglądarce | przeszedł | 8/8 | 1048 | 6 min 28 s |
| `tajski` — brak pisma tajskiego | przeszedł | 1/1 | 96 | 23,5 s |
| **RAZEM** | **przeszedł** | **20/20** | **2146** | **9 min 08 s** |

Walidacja bazy: **0 błędów, 1 ostrzeżenie.** Ostrzeżenie dotyczy sufitu metody
pokrycia w 12 kategoriach i jest tematem rozdziału 9 — nie jest usterką, tylko
zmierzonym ograniczeniem, o którym walidator ma przypominać.

Audyt jakości (`python3 tools/audit-quality.py`): **bez zastrzeżeń.**
Duplikatów identyfikatorów: 0. Rekordów o identycznym tłumaczeniu **i** fonetyce: 0.
Martwych odwołań w `relatedWords`: 0 na 23 567 odwołań. Braków w polach
wymaganych przez schemat: 0.

Zakres testu przeglądarkowego: 2 tryby ładowania (`file://` i serwer) × 2 motywy
(jasny, ciemny) × 2 płcie mówiącego (męska, żeńska) = 8 kombinacji. Zakres testu
dostępności: 24 ekrany × 2 motywy.

---

## 8. Różnice wobec sesji V

Polecenie było jasne: liczby mają pochodzić z pomiaru w tej sesji, a rozbieżności
mają być pokazane. Oto one.

| Miara | Sesja V | Ta sesja | Różnica |
|---|---:|---:|---:|
| rekordy słownika | 20 792 | **20 791** | −1 |
| hasła leksykalne | 3513 | **3512** | −1 |
| unikalne tokeny sylabiczne | 1977 | **1977** | 0 |
| wystąpienia sylab | 125 237 | **125 232** | −5 |
| rekordy zweryfikowane | 2460 | **2460** | 0 |

### Skąd biorą się różnice

**Rekordy: −1.** To nie jest utrata rekordu. `manifest.json` deklarował dla
poziomu A1 wartość 4050 przy faktycznych 4049 — pojedynczy błąd w ręcznie
utrzymywanym liczniku, przenoszony przez kolejne raporty jako suma 20 792.
Faktyczna liczba rekordów w plikach nie zmieniła się. Licznik został w tej
sesji przeliczony z plików i poprawiony; od teraz `audit-quality.py` raportuje
zgodność manifestu, metadanych i stanu faktycznego jako `OK` we wszystkich
dziesięciu pozycjach.

**Hasła leksykalne: −1.** Konsekwencja powyższego — rekord, którego nie było,
był liczony jako hasło.

**Wystąpienia sylab: −5.** Różnica metody, nie danych. Ten raport liczy sylaby
z pola `syllables`, zapisywanego przy rekordzie przez generator. Sesja V liczyła
je, dzieląc fonetykę ponownie własną regułą, która inaczej traktowała
interpunkcję na końcu zdania. Liczba unikalnych sylab jest w obu metodach
identyczna (1977), różnica dotyczy wyłącznie zliczania wystąpień i wynosi
0,004%. Przyjęto pole `syllables`, bo podział na sylaby jest decyzją generatora
i liczenie go drugi raz inną regułą dawałoby liczbę, o której nie wiadomo,
która jest prawdziwa.

**Krzywa pokrycia sylabicznego potwierdzona co do dziesiątej części procenta:**
200 sylab → 75,25% (sesja V: 75,3%), 1000 → 96,40% (96,4%), 1500 → 99,12% (99,1%).

---

## 9. Pokrycie mowy potocznej

### Model

Pokrycie tekstu przez N najczęstszych haseł opisuje rozkład Zipfa-Mandelbrota
`f(r) = C / (r + b)^a`. Parametry dopasowano metodą najmniejszych kwadratów do
czterech punktów zaczepienia zmierzonych na korpusach **mówionych**, nie pisanych:
1000 haseł → 85%, 2000 → 90%, 3000 → 93%, 5000 → 95%. Dopasowane parametry:
`a = 1,39`, `b = 10`.

Mowa potoczna ma pokrycie wyższe niż pismo przy tej samej liczbie haseł, bo
powtarza się w niej wąski rdzeń czasowników, zaimków i partykuł. Liczenie na
frekwencji pisanej zaniżyłoby wymaganie i dałoby fałszywy komfort.

**Ograniczenie modelu, które trzeba powiedzieć wprost:** to jest interpolacja
między czterema punktami, a nie pomiar na korpusie tajskim. Liczby są rzędem
wielkości, nie wynikiem pomiaru. Druga niepewność: „hasło” to jednostka
słownikowa, a tajski składa gęsto — `nám khǎeng` (lód) to dwa hasła albo jedno,
zależnie od decyzji. Liczby wahają się od tego o kilkanaście procent.

### Stan

| | Haseł | Pokrycie |
|---|---:|---:|
| zasób bazy | **3512** | **92,8%** |
| wprowadza ścieżka nauki (333 lekcje) | **3014** | **92,2%** |
| próg 90% wymaga | 1923 | — |
| **próg 95% wymaga** | **6286** | — |

**Do progu 95% brakuje 3272 haseł** licząc od stanu ścieżki nauki, albo 2774
licząc od zasobu bazy. To nie jest doszlifowanie — to podwojenie słownika.

### Dlaczego próg 95% jest nieosiągalny obecną metodą

Pytanie nie brzmi „ile brakuje”, tylko „czy jest z czego to dobrać”. Metoda
budowania bazy jest jedna: hasła pochodzą z białych list słów, a to, co z tych
list zostało niewykorzystane, leży w plikach `tools/generators/reserve-stage*.json`.
Rezerwa jest więc **górnym ograniczeniem na to, o ile kategoria może jeszcze
urosnąć bez nowego materiału źródłowego.**

Rezerwa łączna: **365 haseł w 5 plikach.** Potrzeba: 3272.

| Kategoria | Hasła | Potrzeba | Luka | Rezerwa | Osiągalne? |
|---|---:|---:|---:|---:|---|
| Praca i nauka | 233 | 649 | 416 | 78 | NIE |
| Cechy i opinie | 281 | 633 | 352 | 60 | NIE |
| Czasowniki | 441 | 597 | 156 | 0 | NIE |
| Gramatyka użytkowa | 145 | 577 | 432 | 11 | NIE |
| Small talk | 244 | 454 | 210 | 0 | NIE |
| Awarie i pomoc | 138 | 359 | 221 | 6 | NIE |
| Zakupy i pieniądze | 209 | 357 | 148 | 7 | NIE |
| Jedzenie i napoje | 195 | 309 | 114 | 0 | NIE |
| Miejsca i orientacja | 148 | 256 | 108 | 0 | NIE |
| Pytania | 101 | 253 | 152 | 10 | NIE |
| Dom i codzienność | 217 | 235 | 18 | 0 | NIE |
| Podstawy i grzeczność | 65 | 209 | 144 | 108 | NIE |
| Zdrowie | 163 | 203 | 40 | 39 | NIE |
| Transport | 143 | 203 | 60 | 0 | NIE |
| Pogoda i przyroda | 164 | 185 | 21 | 0 | NIE |
| Ludzie i rodzina | 138 | 179 | 41 | 0 | NIE |
| Czas i daty | 174 | 177 | 3 | 0 | NIE |
| Liczby i liczenie | 140 | 159 | 19 | 0 | NIE |
| Restauracja | 91 | 154 | 63 | 46 | NIE |
| Hotel | 82 | 137 | 55 | 0 | NIE |

**Nieosiągalnych obecną metodą: 20 z 20 kategorii. W tym 11 kategorii nie ma
ani jednego hasła w rezerwie.** Trzy kategorie (Czas i daty — brakuje 3,
Dom i codzienność — 18, Liczby i liczenie — 19) są blisko, ale nie mają z czego
dobrać nawet tych kilkunastu haseł.

### Rozbieżność z sesją V — i dlaczego nie na korzyść projektu

Sesja V podawała, że próg 95% jest nieosiągalny **w 12 kategoriach**. Ta liczba
jest poprawna, ale mierzy co innego, i obie warto mieć obok siebie.

**Miara sesji V — sufit metody pokrycia.** `data/coverage.json` liczy, jaki
odsetek wystąpień wyrazów w kwestiach dialogów daje się w ogóle odwzorować na
hasła bazy. Kategorii w tym modelu jest 15 (nie 20 — pięć kategorii nie ma
dość materiału dialogowego, żeby je zmierzyć). Poniżej progu 95% leży
**dokładnie 12 z 15**:

| Kategoria | Sufit | | Kategoria | Sufit |
|---|---:|---|---|---:|
| Podstawy i grzeczność | 85,0% | | Zakupy i pieniądze | 92,0% |
| Ludzie i rodzina | 90,5% | | Czas i daty | 93,0% |
| Small talk | 91,1% | | Transport | 94,1% |
| Awarie i pomoc | 91,8% | | Restauracja | 94,4% |
| Praca i nauka | 91,8% | | Miejsca i orientacja | 94,7% |
| Zdrowie | 92,0% | | *(powyżej progu: Hotel 95,4%,* |
| Dom i codzienność | 92,8% | | *Pogoda 95,7%, Jedzenie 98,9%)* |

Sufit globalny: **92,6%** — 9011 z 9728 wystąpień daje się odwzorować.

**Miara tej sesji — test rezerwy źródłowej.** Pyta nie „jak wysoko sięga metoda”,
tylko „czy zostało z czego budować”. Odpowiedź: nie, w żadnej z 20 kategorii.

Obie miary mówią to samo z dwóch stron, ale **miara tej sesji jest surowsza:
20 z 20 zamiast 12 z 15.** Nie zaokrąglam tego w górę i nie zastępuję nowej
liczby starszą, korzystniejszą.

---

## 10. Stan weryfikacji językowej

### To jest najpoważniejsze ograniczenie projektu

**Materiał zweryfikowany językowo: 2460 rekordów z 20 791, czyli 11,8%.
Pozostałe 88,2% to materiał wzorcowy generowany z białych list słów.**

| Rodzaj materiału | Rekordy | Udział |
|---|---:|---:|
| rdzeń zweryfikowany (źródło z adnotacją „zweryfikowany”) | **2460** | **11,8%** |
| ręcznie opracowany, bez adnotacji weryfikacji | 114 | 0,5% |
| materiał wzorcowy z białych list | 18 217 | 87,6% |

Pochodzenie rekordów według pola `source`:

| Źródło | Rekordy |
|---|---:|
| Sesja O — domknięcie leksykonu (ścieżka 3000 słów) | 5507 |
| Sesja N — rozszerzenie leksykalne | 4530 |
| Baza projektu Thai All-in-One | 2427 |
| Wzorzec zdaniowy z białej listy — etap 4 B1 | 1999 |
| Wzorzec zdaniowy z białej listy — etap 3 A2 | 1518 |
| Wzorzec zdaniowy z białej listy — etap 5 B2 | 1398 |
| Rdzeń leksykalny — sesja F (zweryfikowany) | 555 |
| Wzorzec zdaniowy z białej listy — etap 6 | 551 |
| Rdzeń ręczny — etap 4 B1 (zweryfikowany) | 500 |
| Rdzeń ręczny — etap 3 A2 (zweryfikowany) | 482 |
| Rdzeń ręczny — etap 5 B2 (zweryfikowany) | 431 |
| Rdzeń ręczny — etap 2 (zweryfikowany) | 291 |
| Rdzeń ręczny — etap 6 (zweryfikowany) | 201 |
| pozostałe | 401 |

### Uwaga do liczby 2460

Narzędzie `tools/audit-quality.py` raportuje 2574 rekordy (12,4%) jako „rdzeń
zweryfikowany”, bo dolicza 114 ręcznie opracowanych trójek rejestrowych z etapu 5.
Ten raport ich **nie** dolicza: zostały napisane ręcznie, ale nie mają adnotacji
weryfikacji, więc nie ma dowodu, że ktoś je sprawdził pod kątem naturalności.
Przy dwóch dostępnych liczbach raport zamykający podaje niższą.

### Co to znaczy w praktyce

Materiał wzorcowy nie jest błędny. Zdania są gramatycznie poprawne, zbudowane
z haseł, które przeszły przez białą listę, według szablonów sprawdzonych na
rdzeniu. Walidator nie znajduje w nich usterek, bo formalnie ich nie ma.

Problem jest inny i formalna kontrola go nie wykryje: **poprawne zdanie może
brzmieć nienaturalnie.** Rodzimy użytkownik języka powiedziałby to inaczej —
krócej, innym szykiem, z inną partykułą, albo w ogóle by tego nie powiedział
w tej sytuacji. Automat nie ma jak tego wiedzieć, bo nie ma dostępu do tego,
co ludzie faktycznie mówią; ma dostęp tylko do tego, co jest gramatycznie
dopuszczalne. Różnica między tymi dwoma zbiorami jest dokładnie tym, co
odróżnia mówienie płynne od mówienia poprawnego.

Ryzyko rośnie tam, gdzie materiał jest najbardziej wzorcowy: w kategoriach
o największym udziale zdań generowanych i na poziomach A2 i B1, czyli w 66%
bazy. Rośnie też szczególnie w rejestrze — a przypominam z rozdziału 3, że
rejestr potoczny i nieformalny to razem 2,5% materiału. Kurs, który obiecuje
rozumienie mowy potocznej, ma tej mowy potocznej w materiale bardzo niewiele,
a to, co ma, w większości nie zostało przez nikogo sprawdzone.

### Usunięcie tego ograniczenia wymaga rodzimego użytkownika języka, nie kodu

To jest sedno i nie ma tu obejścia. Żadne narzędzie w `tools/` — istniejące ani
możliwe do napisania — nie odpowie na pytanie „czy Tajowie tak mówią”. Walidator
sprawdzi kompletność pól, spójność odwołań i kolejność sylab; audyt policzy
duplikaty; analiza luki oszacuje pokrycie. **Żadne z nich nie odróżni zdania
naturalnego od poprawnego.**

Praca, która została do wykonania, to przeczytanie 18 331 rekordów przez osobę
mówiącą po tajsku od urodzenia i oznaczenie tych, które brzmią sztucznie.
Przy tempie 200 rekordów na godzinę to około 92 godziny czytania. Nie da się
tego przyspieszyć kodem, zlecić modelowi ani ominąć lepszym szablonem.
**To jest jedyne zadanie, którego ten projekt nie może wykonać sam.**

---

## 11. Uczciwa ocena: co uczący się będzie rozumiał, a czego nie

Ta sekcja jest po to, żeby ktoś, kto rozważa zainwestowanie kilkuset godzin
w ten materiał, wiedział, co dostanie, zanim zacznie.

### Co będzie umiał

**Usłyszy wszystko.** Po Module 0 i ścieżce nauki odróżni pięć tonów, długość
samogłoski i przydech. Inwentarz sylabiczny bazy jest domknięty (1977 sylab,
1500 najczęstszych pokrywa 99,1%), więc **nie napotka dźwięku, którego nigdy
nie słyszał.** Nieznane słowo usłyszy poprawnie i powtórzy poprawnie, nawet nie
znając jego znaczenia. To jest realny, sprawdzalny wynik i najmocniejsza rzecz,
jaką ten projekt daje.

**Zrozumie około 92% mowy potocznej.** Ścieżka nauki wprowadza 3014 haseł, co
w przyjętym modelu daje 92,2% pokrycia. Poradzi sobie w sytuacjach, na których
kurs jest zbudowany: restauracja, targ, transport, hotel, lekarz, awaria,
small talk.

**Powie, co ma do powiedzenia.** 333 lekcje ułożone tak, żeby każde nowe hasło
dało się natychmiast użyć w zdaniu ze znanego materiału. 81 tematów gramatycznych
w 483 wzorcach. Sześć trybów produkcji, w tym ocena konturu tonalnego z mikrofonu.
Klasyfikatory (139) i liczby (165 pozycji, sześć rodzajów drylu) — dwie rzeczy,
na których polskojęzyczni uczący się przewracają się najczęściej.

**Zda egzamin na własnym poziomie.** Cztery sprawności mierzone osobno, każda
z progiem, bez uśredniania.

### Czego nie będzie umiał

**Nie przeczyta nic po tajsku.** Decyzja projektowa, nie brak. Menu, tabliczka,
SMS, formularz — nieczytelne. Konsekwencja jest większa, niż się wydaje: odcina
to najtańsze źródło kontaktu z żywym językiem, jakim jest czytanie. Uczący się
zostaje zależny od słuchu i od rozmówcy.

**Nie zrozumie tych 8%.** To brzmi jak drobiazg i nie jest. **8% to mniej więcej
jedno nieznane słowo na dwanaście, czyli kilka w każdym dłuższym zdaniu.**
W praktyce oznacza to rozmowę, którą się nadąża, ale w której co chwilę wypada
element — zwykle ten, który niesie konkret. Różnica między 92% a 95% nie jest
różnicą trzech punktów, tylko różnicą między „rozumiem, o czym mowa” a „rozumiem,
co zostało powiedziane”. Domknięcie tej luki wymagałoby 3272 haseł, których nie
ma z czego dobrać w żadnej z 20 kategorii (rozdział 9).

**Nie będzie brzmiał naturalnie i nie ma jak tego sprawdzić.** 88,2% materiału,
z którego się uczy, nie zostało przeczytane przez nikogo, kto mówi po tajsku od
urodzenia. Zdania są poprawne. Czy są naturalne — nie wiadomo, i to jest uczciwa
odpowiedź, a nie ostrożnościowa. **Uczący się może przez cały kurs utrwalać
sformułowania, których Tajowie nie używają, i dowie się o tym dopiero od
rozmówcy.** Ryzyko jest największe dokładnie tam, gdzie najbardziej boli: w mowie
potocznej, która stanowi 2,5% materiału i której weryfikacja jest najtrudniejsza.

**Nie będzie swobodny w rejestrze.** Baza jest w 84,9% neutralna. Uczący się
będzie mówił uprzejmie i bezpiecznie w każdej sytuacji, co jest dobrą strategią
dla obcokrajowca, ale nie da mu ani wyczucia, kiedy `khráp` można opuścić, ani
zrozumienia, gdy ktoś mówi do niego swobodnie. 23 idiomy i 18 rekordów
z ostrzeżeniem o slangu to za mało, żeby cokolwiek z tego wynikało.

**B2 nie doda mu słów.** Poziom B2 to 2184 rekordy i **zero nowych haseł
leksykalnych** — same zdania, rejestry i idiomy ze znanego słownictwa. Kto
przechodzi B2 licząc na poszerzenie zasobu słów, nie dostanie tego.

### Podsumowanie liczbowe

| Pytanie | Odpowiedź | Podstawa |
|---|---|---|
| Czy usłyszy poprawnie? | tak, praktycznie zawsze | 1977 sylab, 1500 pokrywa 99,1% |
| Ile zrozumie z rozmowy? | **~92%** | 3014 haseł, model Zipfa-Mandelbrota |
| Czy dojdzie do 95%? | **nie, obecną metodą** | brakuje 3272 haseł, rezerwa 365 |
| Czy zabrzmi naturalnie? | **nie wiadomo** | 88,2% materiału niezweryfikowane |
| Czy przeczyta cokolwiek? | nie | decyzja projektowa |
| Czy poradzi sobie w Tajlandii? | w sytuacjach z kursu — tak | 184 dialogi, 61 scen, 20 kategorii |

### Zdanie, którym warto zamknąć

Ten projekt doprowadza uczącego się do progu, za którym dalsza nauka wymaga
**kontaktu z żywym językiem, a nie z większą bazą.** Ucho jest przygotowane,
słownictwo wystarcza do funkcjonowania, gramatyka jest opanowana. Brakuje
trzech tysięcy słów, których nie ma skąd wziąć bez korpusu, i weryfikacji
naturalności, której nie da się wykonać bez człowieka. Jedno i drugie leży
poza tym, co da się zrobić kodem — i to jest właściwy moment, żeby projekt
zamknąć, zamiast dokładać do niego kolejne dziesięć tysięcy rekordów,
które nie zmienią żadnej z powyższych liczb.

---

## 12. Co zostało naprawione w tej sesji

Sesja zamykająca nie powinna zostawiać otwartych spraw. Poza napisaniem od nowa
`README.md` i tego raportu, naprawiono cztery rzeczy.

**1. Obietnica braku pisma tajskiego przestała być deklaracją.** Powstało
narzędzie `tools/thai-script-check.py` (96 sprawdzeń: dane, 24 ekrany, 19 trybów,
3 eksporty) i zostało wpięte do `run-all-tests.py` jako etap `tajski`. Od teraz
zmiana w `data/`, `js/` lub `index.html` unieważnia jego wynik i wymusza
ponowne sprawdzenie.

**2. `data/metadata.json` był nieaktualny o kilka sesji.** Deklarował 10 755
rekordów przy faktycznych 20 791, 12 094 przykłady przy 25 196 i błędne liczby
dla A1, A2 i B1. Wszystkie liczniki przeliczono z plików.

**3. `data/manifest.json` miał błąd w liczniku poziomu A1** — 4050 zamiast 4049.
To jest źródło rozbieżności „20 792 kontra 20 791” ciągnącej się przez kolejne
raporty. Poprawione; `audit-quality.py` raportuje teraz zgodność we wszystkich
dziesięciu pozycjach.

**4. `tools/audit-quality.py` zgłaszał 9 nieistniejących problemów.** Pięć
„duplikatów polskiego tłumaczenia” to pary grzecznościowe (`súe tǔa dâai thîi nǎi`
i wariant z `khráp`) albo pary męsko-żeńskie (`kàp phǒm` / `kàp chǎn`) — polskie
tłumaczenie jest jedno, bo polszczyzna tej różnicy nie koduje, i to jest właśnie
powód istnienia obu rekordów. Cztery „duplikaty fonetyki” to prawdziwe tajskie
homofony: ส้อม „widelec” i ซ่อม „naprawiać” brzmią identycznie (`sâwm`),
tak samo เหล้า „alkohol” i เล่า „opowiadać” (`lâo`). To materiał, nie usterka.
Audyt rozróżnia je teraz od prawdziwych duplikatów (zgodność tłumaczenia
**i** fonetyki, których jest 0) i raportuje osobną linią jako zamierzone.
Wynik audytu: **bez zastrzeżeń.**

---

## Jak odtworzyć każdą liczbę z tego raportu

```bash
python3 tools/final-metrics.py       # rozdziały 1, 2, 3, 4, 8, 9, 10
python3 tools/bench-start.py --dlawienie 4   # rozdział 5
python3 tools/thai-script-check.py   # rozdział 6
python3 tools/run-all-tests.py       # rozdział 7
python3 tools/audit-quality.py       # rozdziały 7, 10, 12
python3 tools/gap-analysis.py        # rozdział 9
```
