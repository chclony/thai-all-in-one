# Thai All-in-One

Aplikacja do nauki mówionego tajskiego dla osób mówiących po polsku.
Działa w przeglądarce, bez konta, bez internetu i bez instalowania czegokolwiek.

**Jedna decyzja odróżnia ten projekt od innych kursów: nie ma tu pisma tajskiego.**
Ani jednego znaku — nie na ekranie, nie w słowniku, nie w eksportach. Wszystko, co
widzisz, jest zapisane alfabetem łacińskim ze znakami tonów (`khráp`, `sǎwng`,
`mâi pen rai`). Powód jest praktyczny: alfabet tajski to 44 spółgłoski, 32 samogłoski
i reguły tonu zależne od klasy znaku. Nauka czytania zajmuje miesiące, w trakcie
których nie powiesz ani jednego zdania. Ten projekt zakłada, że chcesz **mówić
i rozumieć**, a czytanie zostawiasz na później albo nie zostawiasz wcale.

Pismo tajskie istnieje w plikach danych w jednym ukrytym polu technicznym,
`ttsThai`, którego jedynym odbiorcą jest syntezator mowy. Że nie wycieka do
interfejsu, nie jest deklaracją — sprawdza to test, opisany niżej w sekcji
[Testy](#testy).

---

## Spis treści

- [Uruchomienie](#uruchomienie) — dwa tryby
- [Jak się uczyć](#jak-się-uczyć) — od czego zacząć i w jakiej kolejności
- [Co jest w środku](#co-jest-w-środku) — ekrany i tryby ćwiczeń
- [Co zawiera baza](#co-zawiera-baza) — liczby
- [Zapis wymowy](#zapis-wymowy) — jak czytać `khráp` i `sǎwng`
- [Dźwięk](#dźwięk) — skąd bierze się wymowa i kiedy jej nie ma
- [Budowanie danych](#budowanie-danych)
- [Testy](#testy)
- [Struktura katalogów](#struktura-katalogów)
- [Ograniczenia](#ograniczenia) — przeczytaj przed nauką
- [Dokumentacja](#dokumentacja)

---

## Uruchomienie

Aplikacja działa w dwóch trybach. Oba dają ten sam materiał; różnią się tym,
skąd przeglądarka bierze dane.

### Tryb 1: z dysku (`file://`) — nic nie instalujesz

Otwórz plik `index.html` podwójnym kliknięciem albo przeciągnij go na okno
przeglądarki. To wszystko.

Działa, bo obok każdego pliku `data/*.json` leży bliźniak `data/*.js`, ładowany
znacznikiem `<script>`. Przeglądarki blokują `fetch()` dla adresów `file://`,
ale skryptów nie blokują. Pliki `.js` są generowane — patrz
[Budowanie danych](#budowanie-danych).

**Kiedy wybrać:** telefon bez sieci, pendrive, komputer bez Pythona, szybki rzut oka.
**Czego zabraknie:** nie zadziała service worker, więc nie zainstalujesz aplikacji
na ekranie początkowym telefonu.

### Tryb 2: przez serwer — pełna funkcjonalność

```bash
python3 -m http.server 8000
```

Potem otwórz `http://localhost:8000` w przeglądarce.

Dowolny statyczny serwer wystarczy — Python jest tu tylko najkrótszą drogą.
Ten tryb włącza service workera, czyli pracę offline po pierwszym wczytaniu
i instalację jako aplikacja na telefonie (patrz `docs/instalacja-iphone.md`).

**Kiedy wybrać:** codzienna nauka, telefon, publikacja na GitHub Pages.

### Ile to trwa

Pomiar przy **czterokrotnym spowolnieniu procesora** — czyli na telefonie
wyraźnie słabszym niż przeciętny — mediana z pięciu prób, do momentu, w którym
aplikacja jest gotowa do użycia:

| Tryb | Pierwsze uruchomienie | Powrót do nauki |
|---|---|---|
| `file://` | 838 ms | 789 ms |
| serwer | 1107 ms | 1215 ms |
| serwer, z pełnym indeksem w tle | 1579 ms | 1746 ms |

Aplikacja nie czeka na całą bazę. Wczytuje najpierw indeks czołowy (4827 pozycji),
a pozostałe 15 964 dociąga w tle, więc ekran jest gotowy, zanim skończy się
ładowanie. Pomiar powtórzysz poleceniem:

```bash
python3 tools/bench-start.py --dlawienie 4
```

---

## Jak się uczyć

Nie musisz nic ustawiać. Przy pierwszym uruchomieniu aplikacja otwiera **test
poziomujący** i sama proponuje, od czego zacząć. Jeśli chcesz wiedzieć, co
proponuje i dlaczego — poniżej kolejność, na której zbudowany jest kurs.

### 1. Moduł 0 — trening słuchu (zacznij tutaj)

**12 lekcji, 260 zadań, wyłącznie na słuch.** Bez znaczeń, bez zapisu, bez
tłumaczeń. Słyszysz dwa dźwięki i mówisz, czy są takie same.

Lekcja pierwsza — pięć tonów — zaczyna się **odprawą, a nie sprawdzianem**:
każdy ton z widoczną nazwą, rysunkiem konturu na skali Chao, polskim
odpowiednikiem i przyciskiem odsłuchu. Do tego jedna sylaba w czterech tonach
(cztery różne słowa) i trzy pary, które mylą się najczęściej. Dopiero potem
zaczyna się rozpoznawanie. W trakcie ćwiczenia odprawa jest o jeden dotyk —
przycisk *Nie wiem, jak brzmi ten ton* wraca do niej i z powrotem do zadania
bez utraty postępu.

To wygląda na stratę czasu i jest najczęściej pomijanym elementem kursu. Powód,
dla którego jest pierwszy: polszczyzna nie odróżnia tonów ani długości samogłosek,
więc polskie ucho **fizycznie ich nie słyszy** na starcie. `mǎi`, `mài`, `mái`
i `mâi` to cztery różne wyrazy, które nieprzygotowanemu uchu brzmią identycznie.
Jeśli zaczniesz od słówek, będziesz zapamiętywał słowa, których nie odróżnisz
w rozmowie — i dowiesz się o tym dopiero w Tajlandii.

Ćwiczone kontrasty: 26, w 7 rodzinach (tony, długość samogłoski, przydech,
liczba sylab i inne).

### 2. Ścieżka nauki — 333 lekcje w 23 rozdziałach

Główny kurs. Lekcje są ułożone tak, żeby **każde nowe hasło dało się natychmiast
użyć w zdaniu zbudowanym wyłącznie z materiału, który już znasz**. Nie ma zdania
przykładowego, które wprowadza trzy nieznane słowa przy okazji jednego nowego.

Rozkład: Survival 29 lekcji, A1 73, A2 99, B1 70, B2 62. Łącznie ścieżka
wprowadza 3014 haseł.

### 3. Sesja dnia i powtórki

Ekran **Sesja dnia** składa dzienny zestaw z nowego materiału i zaległych
powtórek. Powtórki chodzą w systemie odstępów rosnących, osobno dla trzech
stron hasła: rozpoznawania, produkcji i zapisu. Krzywa zapamiętywania dostraja
odstępy do Twoich wyników, a nie do średniej.

Co 20 lekcji wchodzi **próbka kontrolna** z materiału sprzed 20 lekcji — wykrywa
zapominanie wcześniej, niż zrobi to kolejka powtórek, bo nie czeka na termin karty.

### 4. Materiały i egzaminy

Kiedy masz ochotę na coś innego niż ćwiczenia: 184 dialogi, 61 scen, słuchanie
ekstensywne (66 minut materiału). Na koniec każdego poziomu jest egzamin mierzący
cztery sprawności osobno, każdą z własnym progiem — poziom zaliczasz dopiero
wtedy, gdy przejdziesz wszystkie cztery.

---

## Co jest w środku

**24 ekrany w 6 grupach.**

**Codziennie** — Dzisiaj, Sesja dnia, Kurs, Powtórki

**Ćwiczenia** — Moduł 0 (trening słuchu), Słuchanie, Mówienie po tajsku,
Powtarzaj za wzorem, Gramatyka, Liczby w mowie, Ratowanie rozmowy

**Materiały** — Słownik i zwroty, Dialogi, Sceny, Słuchanie ekstensywne,
Tony i wymowa

**Sprawdziany** — Test poziomujący, Egzamin poziomowy, Próbki kontrolne,
Sesja naprawcza

**Postęp** — Postęp, Tydzień, Droga do celu

**Aplikacja** — Ustawienia

### Tryby ćwiczeń

Trzy ekrany mają po kilka trybów — razem **19 różnych ćwiczeń**:

| Ekran | Tryby |
|---|---|
| Mówienie po tajsku | układanie zdania, wpisywanie, klasyfikatory, ton, wymowa na głos, scenka |
| Gramatyka | mapa, struktura zdania, przekształcenia, partykuły, przewodnik |
| Słuchanie | wybór, dyktando, składanie, wyławianie, płeć mówiącego, w hałasie, luka, nieznane słowo |

Tryb „wymowa na głos” i „ton” korzystają z mikrofonu: aplikacja liczy kontur
tonalny z Twojego nagrania i porównuje go z wzorcem. Dzieje się to w całości
na Twoim urządzeniu — nic nie jest wysyłane.

---

## Co zawiera baza

Wszystkie liczby poniżej pochodzą z pomiaru, który powtórzysz poleceniem
`python3 tools/final-metrics.py`.

### Objętość

| | |
|---|---:|
| rekordy słownika | 20 791 |
| przykłady zdań | 25 196 (17 968 unikalnych) |
| dialogi / kwestie | 184 / 1682 |
| sceny / kwestie / pytania | 61 / 1682 / 529 |
| lekcje ścieżki nauki | 333 w 23 rozdziałach |
| tematy gramatyczne / wzorce | 81 / 483 |
| ćwiczenia gramatyki ze słuchu | 1490 |
| ćwiczenia przekształceń | 1589 |
| klasyfikatory | 139 |
| pozycje liczbowe | 165 |
| zestawy egzaminacyjne / próbki kontrolne | 15 / 15 |

### Poziomy

| Poziom | Rekordy | Udział |
|---|---:|---:|
| Survival | 778 | 3,7% |
| A1 | 4049 | 19,5% |
| A2 | 9561 | 46,0% |
| B1 | 4219 | 20,3% |
| B2 | 2184 | 10,5% |

### Zasób słownictwa

Rekord to nie to samo co hasło. Większość rekordów (67,7%) to zdania — materiał
ćwiczeniowy. **Haseł słownikowych** (rzeczownik, czasownik, przymiotnik,
przysłówek, wyraz) jest **3512**, z czego ścieżka nauki wprowadza **3014**.

Inwentarz sylabiczny: **1977 unikalnych sylab** na 125 232 wystąpienia. Jest
praktycznie domknięty — 1000 najczęstszych sylab pokrywa 96,4% materiału,
1500 pokrywa 99,1%.

Co to oznacza w praktyce, łącznie z tym, czego **nie** będziesz rozumiał, opisuje
`docs/raport-koncowy.md`. Przeczytaj to, zanim zaczniesz — sekcja
[Ograniczenia](#ograniczenia) niżej streszcza najważniejsze.

---

## Zapis wymowy

Tony zapisujemy znakiem nad samogłoską:

| Znak | Ton | Brzmi jak |
|---|---|---|
| `a` | średni | równo, bez zmiany wysokości |
| `à` | niski | równo, ale niżej niż zwykle |
| `â` | opadający | jak polskie „nie!” z naciskiem |
| `á` | wysoki | równo, wyżej niż zwykle |
| `ǎ` | rosnący | jak polskie pytanie: „tak?” |

Samogłoski długie piszemy podwójnie: `aa`, `ii`, `uu`. Różnica długości zmienia
znaczenie, więc `khao` i `khaao` to dwa różne wyrazy.

Trzy samogłoski nie mają polskiego odpowiednika: `ue` ≈ polskie „y”,
`oe` ≈ „e” z zaokrąglonymi wargami, `aw` ≈ długie „o”.

Każdy rekord ma dodatkowo zapis przybliżony polską ortografią
(`pronunciationPolish`) i słowny opis tonów (`toneGuide`). Pełny przewodnik
jest na ekranie **Tony i wymowa**.

---

## Dźwięk

**Aplikacja nie zawiera nagrań lektorskich.** Wymowę wypowiada syntezator mowy
Twojego systemu operacyjnego. Konsekwencja jest jedna i trzeba ją znać:
**jakość wymowy zależy od urządzenia, nie od aplikacji.**

Skrót, gdzie działa:

| System | Tajski głos |
|---|---|
| Android + Chrome | zwykle tak, najlepsza jakość |
| iPhone / iPad | po doinstalowaniu w Ustawieniach systemu |
| Windows + Edge | zwykle tak |
| Windows + Firefox | często nie — spróbuj innej przeglądarki |
| macOS | po doinstalowaniu |

Jeśli głosu nie ma, aplikacja to wykrywa i mówi, jak go zainstalować, zamiast
milczeć. Szczegóły i obejścia: `docs/ograniczenia-tts.md`.

Katalog `audio/` jest przygotowany na nagrania lektorskie — gdy plik istnieje,
ma pierwszeństwo przed syntezatorem. Na dziś jest pusty.

---

## Budowanie danych

Źródłem prawdy są pliki `data/*.json`. Wszystko inne jest z nich generowane
i **nie należy tego edytować ręcznie**.

Po każdej zmianie w `data/` uruchom po kolei:

```bash
python3 tools/update-manifest.py      # przelicza liczniki w manifest.json
python3 tools/build-search-index.py   # indeks wyszukiwarki
python3 tools/build-offline-data.py   # bliźniaki .js dla trybu file://
python3 tools/validate.py             # kontrola poprawności — musi dać 0 błędów
```

Ostatni krok jest obowiązkowy. `validate.py` sprawdza kompletność pól, spójność
odwołań, kolejność wprowadzania sylab w ścieżce nauki i to, czy pismo tajskie
nie wyciekło poza pole `ttsThai`.

Same rekordy powstają z generatorów w `tools/generators/`. Ich opis jest
w `tools/generators/README.md`.

---

## Testy

Jedno polecenie uruchamia całość:

```bash
python3 tools/run-all-tests.py
```

Kończy się kodem niezerowym, jeśli cokolwiek padło. Przebieg jest pocięty na
zadania, a wyniki cząstkowe lądują w `tools/.test-results/`, więc przerwany
przebieg nie zaczyna od zera. Wynik przestaje być ważny, gdy zmieni się to,
co testuje — narzędzie trzyma odcisk wejścia i samo unieważnia nieaktualne etapy.

Przydatne warianty:

```bash
python3 tools/run-all-tests.py --lista          # co się z czego składa
python3 tools/run-all-tests.py --tylko browser  # jeden etap
python3 tools/run-all-tests.py --podsumowanie   # sam raport, bez uruchamiania
python3 tools/run-all-tests.py --budzet 240     # przerwij po 240 s
```

Etapy:

| Etap | Co sprawdza |
|---|---|
| `validate` | poprawność bazy: pola, odwołania, kolejność sylab |
| `function` | logika aplikacji bez przeglądarki |
| `a11y` | dostępność: kontrast, role, nawigacja klawiaturą — 24 ekrany × 2 motywy |
| `zoom` | powiększenie tekstu i tryb redukcji ruchu |
| `browser` | pełne działanie: 2 tryby × 2 motywy × 2 płcie mówiącego |
| `powtorzenia` | powtórzone zdania w opisach lekcji, scen i ćwiczeń |
| `tajski` | **brak pisma tajskiego** w danych, na ekranach i w eksportach |

Interfejs jest pomyślany na telefon i nie pokazuje podpowiedzi o klawiszach.
Obsługa klawiaturą działa nadal — jest potrzebna dla dostępności i sprawdza ją
etap `a11y` — ale nie zajmuje miejsca na ekranie.

Etap `tajski` odpowiada na główną obietnicę projektu i można go uruchomić osobno:

```bash
python3 tools/thai-script-check.py
```

Sprawdza trzy rzeczy niezależnie: czy w plikach danych znak tajski nie pojawia
się poza zamkniętą listą pól zwolnionych, czy nie ma go w widocznym tekście
na 24 ekranach i w 19 trybach ćwiczeń, oraz czy nie ma go w obu eksportach,
które uczący się może wynieść z aplikacji (talia CSV do Anki i kopia postępu
w JSON).

Narzędzia pomiarowe, nieuruchamiane przez `run-all-tests.py`:

```bash
python3 tools/final-metrics.py    # wszystkie liczby raportu
python3 tools/audit.py            # co jest w bazie
python3 tools/audit-quality.py    # kontrola jakości i duplikatów
python3 tools/gap-analysis.py     # luka leksykalna
python3 tools/bench-start.py      # czas startu
```

---

## Struktura katalogów

```
index.html            aplikacja — punkt wejścia
manifest.webmanifest  opis PWA
service-worker.js     praca offline (tylko w trybie serwera)

css/                  jeden arkusz stylów
js/                   kod aplikacji, ~40 modułów bez zależności zewnętrznych
data/                 baza: *.json to źródło, *.js to bliźniaki dla file://
audio/                miejsce na nagrania lektorskie (puste)
assets/icons/         ikony aplikacji
docs/                 dokumentacja
tools/                narzędzia budowania i testy
tools/generators/     generatory materiału
```

Aplikacja nie ma zależności zewnętrznych. Nie ma `npm install`, nie ma kroku
budowania kodu, nie ma frameworka. `js/` to zwykły JavaScript ładowany
znacznikami `<script>`.

---

## Ograniczenia

Trzy rzeczy, które trzeba wiedzieć, zanim zainwestujesz w ten kurs czas.

**1. Materiał nie został zweryfikowany przez rodzimego użytkownika języka.** Jest to materiał wzorcowy: zdania budowane automatycznie z białych list słów według sprawdzonych szablonów. Są gramatycznie poprawne i nie zawierają wykrywalnych
błędów, ale nikt, kto mówi po tajsku od urodzenia, ich nie przeczytał.
Oznacza to, że część zdań może brzmieć sztywno albo książkowo. **To jest
najpoważniejsze ograniczenie projektu i nie da się go usunąć kodem.**

**2. Nie nauczysz się czytać ani pisać.** To była świadoma decyzja, nie brak.
Menu w tajskiej knajpie, tabliczka z nazwą ulicy i wiadomość SMS pozostaną
nieczytelne.

**3. Kurs nie doprowadzi Cię do swobodnego rozumienia mowy potocznej.**
Doprowadzi do około 92%. Brzmi blisko 100, ale 92% oznacza mniej więcej jedno
nieznane słowo na dwanaście — czyli kilka na każde dłuższe zdanie. Co dokładnie
zostaje poza tym progiem i dlaczego nie da się go podnieść obecną metodą,
opisuje uczciwie `docs/raport-koncowy.md`. Przeczytaj tę sekcję, zanim zaczniesz.

---

## Dokumentacja

| Plik | O czym |
|---|---|
| `docs/raport-koncowy.md` | pełny stan projektu, wszystkie liczby, uczciwa ocena, co zostaje poza zasięgiem |
| `docs/instalacja-iphone.md` | instalacja na ekranie początkowym telefonu |
| `docs/ograniczenia-tts.md` | syntezator mowy: gdzie działa, gdzie nie i co z tym zrobić |
| `docs/publikacja-github-pages.md` | publikacja pod własnym adresem |
| `docs/testy-urzadzenia.md` | wyniki testów na realnych urządzeniach |
| `docs/raport-sesja-h-plec.md` | warianty zależne od płci mówiącego |
| `tools/generators/README.md` | jak powstaje materiał |

---

## Licencja i pochodzenie

Materiał powstał w ramach projektu Thai All-in-One. Status licencyjny wymaga
ustalenia przed publiczną publikacją — patrz pole `license` w `data/metadata.json`.
