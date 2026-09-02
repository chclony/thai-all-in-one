# Ograniczenia syntezy mowy (TTS)

Aplikacja nie zawiera nagrań lektorskich. Wymowę wypowiada **syntezator mowy systemu
operacyjnego**, do którego przeglądarka daje dostęp przez `SpeechSynthesis`.
Konsekwencja jest jedna i trzeba ją znać: **jakość i dostępność wymowy zależą od
urządzenia, nie od aplikacji.** Jeśli w systemie nie ma głosu tajskiego, żadna
przeglądarka go nie wyczaruje.

Aplikacja wykrywa to sama: sprawdza listę głosów, szuka `th-TH`, a gdy nie znajdzie —
pokazuje komunikat z instrukcją zamiast milczeć. Ekran *Ustawienia* pokazuje nazwę
wykrytego głosu.

---

## Skrót: co gdzie działa

| System / przeglądarka | Tajski głos | Uwagi |
|---|---|---|
| Android, Chrome | zwykle tak | Google TTS ma tajski w standardzie; najlepsza jakość |
| iPhone / iPad, Safari | po doinstalowaniu | głos trzeba pobrać w ustawieniach systemu |
| iPhone / iPad, Chrome i Firefox | jak w Safari | na iOS każda przeglądarka używa silnika Safari |
| Windows, Edge | zwykle tak | Edge ma własne głosy sieciowe, w tym tajskie |
| Windows, Chrome | zależy | korzysta z głosów systemowych; tajski trzeba dodać |
| Windows, Firefox | często nie | najuboższa obsługa — jeśli cisza, sprawdź inną przeglądarkę |
| macOS, Safari i Chrome | po doinstalowaniu | głos pobiera się w Ustawieniach systemowych |
| Linux | rzadko | zależy od zainstalowanego `speech-dispatcher` i głosów |

---

## Jak dodać głos tajski

### iPhone / iPad
1. *Ustawienia* → **Dostępność** → **Treść mówiona** → **Głosy**
2. wybierz **Tajski**, pobierz głos
3. zamknij i otwórz aplikację ponownie

Sam wybór języka klawiatury albo języka systemu **nie wystarczy** — głos to osobne pobranie.

### Android
1. *Ustawienia* → **Ułatwienia dostępu** → **Zamiana tekstu na mowę**
2. silnik: **Google Text-to-Speech** (jeśli jest wybór)
3. **Zainstaluj dane głosowe** → **ไทย / Thai**

### Windows
1. *Ustawienia* → **Czas i język** → **Język i region** → **Dodaj język** → **ไทย (Thai)**
2. przy dodawaniu zaznacz opcję **Zamiana tekstu na mowę**
3. uruchom ponownie przeglądarkę

W Edge część głosów jest sieciowa — działają tylko przy połączeniu z internetem.

### macOS
*Ustawienia systemowe* → **Dostępność** → **Treść mówiona** → **Głos systemowy** →
**Zarządzaj głosami** → **Tajski**.

---

## Ograniczenia, których nie da się obejść

### iOS wymaga gestu użytkownika
Safari na iPhonie nie odtworzy mowy, dopóki użytkownik czegoś nie dotknie.
Aplikacja radzi sobie z tym, wypuszczając przy pierwszym dotknięciu ekranu pustą,
bezgłośną wypowiedź, która odblokowuje kanał audio. W praktyce znaczy to tyle, że
**pierwsze dotknięcie ekranu jest potrzebne, zanim cokolwiek zabrzmi** — samo wejście
na stronę nie wystarczy.

### Głosy pojawiają się z opóźnieniem
Część przeglądarek wypełnia listę głosów asynchronicznie, już po wczytaniu strony.
Aplikacja nasłuchuje zdarzenia `voiceschanged` i dodatkowo sprawdza listę po 0,4 s
i po 1,5 s. Jeśli mimo to przy pierwszym uruchomieniu widzisz komunikat o braku głosu,
odśwież stronę.

### Głosy sieciowe wymagają internetu
Niektóre głosy (zwłaszcza w Edge i na części Androidów) są syntezowane w chmurze.
Aplikacja preferuje głosy lokalne (`localService`), bo działają offline i szybciej
reagują — ale jeśli lokalnego nie ma, użyje sieciowego. Ekran *Ustawienia* pokazuje,
który typ został wykryty.

### Chrome potrafi się zaciąć
Chrome bywa wstrzymany po powrocie do zakładki i milknie w połowie zdania.
Aplikacja wywołuje `resume()` po każdym `speak()`, co rozwiązuje większość takich sytuacji.

### Jakość wymowy tonów
Syntezatory czytają tony poprawnie **na poziomie sylaby**, ale intonacja całych zdań
bywa płaska i nienaturalna. Do nauki poszczególnych słów nadaje się to dobrze,
do naśladowania melodii dłuższej wypowiedzi — tylko orientacyjnie. Ekran *Wymowa*
i kontury tonów przy każdym haśle są tu ważniejsze niż sam dźwięk.

---

## Wyjścia syntezatora NIE DA SIĘ przechwycić

To jest najważniejsze ograniczenie całej warstwy dźwiękowej i z niego wynika kształt
wszystkiego, co opisano niżej.

Żeby rozciągnąć mowę w czasie, nałożyć na nią pogłos albo przepuścić ją przez filtr
telefoniczny, trzeba mieć jej **próbki**. Web Audio API potrafi to wszystko — ale
tylko na sygnale, który dostanie na wejściu. `SpeechSynthesis` takiego wejścia nie daje:
wypowiedź trafia prosto na wyjście systemowe i nie przechodzi przez graf Web Audio.

Nie jest to błąd konkretnej przeglądarki ani rzecz do obejścia sprytniejszym kodem.
W specyfikacji Web Speech API **nie istnieje** żaden węzeł, strumień ani zdarzenie,
które wypuszczałoby sygnał mowy. Na iOS i Androidzie mowa powstaje w ogóle poza
procesem karty przeglądarki.

Aplikacja tego nie zakłada — sprawdza. Moduł `js/capture.js` przy starcie bada trzy
drogi i zapisuje wynik każdej z nich; widać go w *Ustawieniach → Odsłuch i realizm*.

| Droga | Stan | Dlaczego |
|---|---|---|
| Bezpośrednie wyjście syntezatora | niedostępna wszędzie | Web Speech API nie przewiduje dostępu do sygnału |
| Przechwycenie dźwięku karty (`getDisplayMedia`) | tylko komputery, Chromium, https | wymaga zgody przy **każdym** uruchomieniu, a mowa systemowa i tak zwykle omija strumień karty |
| Nagranie w katalogu `audio/` | działa zawsze | pełne przetwarzanie na buforze; nagrań w projekcie nie ma |

Drugą drogę można uruchomić ręcznie jako eksperyment (przycisk w *Ustawieniach*).
Aplikacja mierzy wtedy, czy w strumieniu w czasie wypowiedzi cokolwiek słychać,
i mówi wprost, co z tego wyszło. Domyślnie jest wyłączona: okno wyboru przy każdym
odtworzeniu to nie jest interfejs do nauki języka.

---

## Wariant zapasowy — co robimy, skoro przechwycić się nie da

### Tempo wolne (0,7×): pauzy zamiast zwalniania silnika

Oczywiste rozwiązanie — `utterance.rate = 0.7` — jest **złe**, i to w sposób, który
psuje sens całej aplikacji. `rate` rozciąga kontur tonalny razem z czasem, a w języku
tonalnym kontur **jest** znaczeniem. Uczący się trenowałby na materiale, którego nikt
nigdy nie powiedział.

Zamiast tego wypowiedź jest cięta na wyrazy i mówiona wyraz po wyrazie, każdy przy
`rate 1,0`, z wydłużonymi pauzami między nimi. Wolniejsza robi się **cała wypowiedź**,
a nie pojedynczy ton. Kontur każdego wyrazu zostaje dokładnie taki, jaki wypuszcza silnik.

Wymaga to znajomości granic wyrazów w piśmie tajskim, które spacji nie stawia —
91% haseł to jeden ciąg bez separatorów. Granice wyznacza generator
`tools/generators/build-tts-split.py` i zapisuje jako same długości członów
(`ttsSplit: [6, 4]`), więc pismo tajskie nie opuszcza prywatnej mapy w pamięci.
Pokrycie: **98,5% wypowiedzi wielowyrazowych** (51 160 z 51 937).

Pozostałe 1,5% oraz hasła jednowyrazowe nie mają czego rozsuwać. Tam tempo wolne
schodzi na `rate` — i aplikacja mówi o tym wprost w opisie odtworzenia, zamiast
udawać, że nic się nie stało.

### Tempo szybkie (1,4×): krótszy zapis plus ograniczone przyspieszenie

Przyspieszyć syntezator bez `rate` się nie da — nie ma innego pokrętła. Można za to
**dać mu mniej do powiedzenia**: w trybie potocznym silnik dostaje zredukowany zapis
(pole `colloquial`), który jest krótszy sam z siebie. Reszta idzie przez `rate`
ograniczony do **1,25**; powyżej tej wartości deformacja konturu robi się słyszalna.

Część przyspieszenia bierze się więc z faktycznej fonetyki, a nie z silnika.

### Warunki akustyczne: równolegle, nie na głosie

Szum tła i pogłos są generowane w Web Audio i mieszane na wyjściu **równolegle**
z mową syntezatora. Działa to bez dostępu do jej próbek: szum, który maskuje mowę,
maskuje ją tak samo skutecznie niezależnie od tego, czy siedzi w tym samym buforze.
Ćwiczenie rozumienia w hałasie jest więc pełnoprawne — stosunek sygnału do szumu
jest tu jedyną wielkością, która naprawdę coś znaczy.

**Czego to nie odtwarza:** pogłosu NA GŁOSIE i pasma telefonicznego NA GŁOSIE.
Jedno i drugie wymaga próbek mowy. Na nagraniach lektorskich (katalog `audio/`)
oba działają na wszystkim; przy syntezatorze pogłos słychać wyłącznie na tle,
a filtr telefoniczny w ogóle się nie włącza. Aplikacja pisze o tym w *Ustawieniach*.

### Tryb potoczny widać częściej, niż słychać

Zapis potoczny zmienia się dla **wszystkich 6 858** tekstów z wariantem. Ale tekst
podawany syntezatorowi zmienia się tylko dla **4 463 z nich (65%)** — bo potocznych
pisowni tajskich, które silniki czytają poprawnie, jest ledwie osiem
(ครับ → คับ, สวัสดี → หวัดดี, อะไร → ไร, ไหม → มั้ย, อย่างไร → ยังไง,
ดิฉัน / ฉัน → ชั้น, เท่าไร → เท่าไหร่).

Dla pozostałych 35% uczący się **widzi** redukcję w zapisie, ale jej nie **usłyszy**:
syntezator nie ma jak wymówić skróconej samogłoski nieakcentowanej ani uproszczonej
zbitki, jeżeli pisownia tajska tego nie zapisuje. Zmuszanie go do tego przez
przekręcanie pisowni dawałoby wymowę gorszą, nie bardziej potoczną.

To jest realna granica tej warstwy i nie da się jej przesunąć bez nagrań człowieka.

---

## Dwa głosy w scenie z dwoma rozmówcami

Obie kwestie wypowiedziane tym samym głosem zlewają się w monolog. Ucho rozdziela
mówiących zanim zrozumie słowa — bez tego sygnału ćwiczenie jest trudniejsze niż
rzeczywistość, ale w niewłaściwy sposób.

* **Dwa głosy tajskie w systemie** — każda rola dostaje własny. Jeśli scenariusz
  określa płeć roli, aplikacja próbuje dobrać głos po nazwie.
* **Jeden głos** (przypadek najczęstszy) — role różnicowane są wysokością
  (`pitch` 0,82 wobec 1,06) i minimalnie tempem. Zakres jest celowo wąski: poza nim
  silniki zaczynają brzmieć jak nagranie puszczone z inną prędkością i psują kontur.

**Na iOS dzieje się dokładnie to:** system udostępnia zwykle **jeden** głos tajski
(Kanya), i to dopiero po ręcznym pobraniu. Scena z dwoma rozmówcami jest więc na
iPhonie odtwarzana jednym głosem o dwóch wysokościach. To namiastka — dwie osoby
różnią się barwą, nie samą wysokością — ale wystarcza, żeby słuchacz wiedział,
kto właśnie mówi. Gdy głosu tajskiego nie ma wcale, nie działa żadna wymowa
i aplikacja pokazuje instrukcję pobrania zamiast milczeć.

Dodatkowo `pitch` bywa na iOS traktowany zgrubnie, a przy wartościach skrajnych
ignorowany. Dlatego rozstaw jest niewielki i nie zależy od niego poprawność
ćwiczenia, tylko jego czytelność.

---

### Prędkość odtwarzania
Ustawienie „tempo domyślne” (0,7× / 1,0× / 1,4×) opisano wyżej. Niezależnie od niego
część silników ignoruje `rate` albo obniża przy nim jakość — jeśli wolniejsze
odtwarzanie brzmi gorzej, korzystaj z naturalnego.

---

## Co zrobić, gdy nie ma żadnego tajskiego głosu

Wymowa jest wtedy jedyną funkcją, która nie działa — słownik, zwroty, dialogi, quizy
tekstowe, powtórki i cały zapis fonetyczny działają normalnie. Możliwości:

1. **Doinstaluj głos** według instrukcji wyżej (najlepsze rozwiązanie).
2. **Zmień przeglądarkę** — na Windowsie Edge ma tajskie głosy najczęściej.
3. **Dodaj własne nagrania.** Format danych to przewiduje: pole `audioFile` w każdym
   rekordzie i przykładzie. Szczegóły w `audio/README.md`. Aplikacja odtworzy plik
   z nagraniem zamiast syntezy, jeśli go znajdzie.
4. **Ucz się z zapisu fonetycznego** — cały projekt jest tak zaprojektowany, żeby
   dało się z niego korzystać wzrokowo: zapis z tonami, zapis „czytaj po polsku”,
   kontury tonów, opis typowych błędów Polaków przy każdym haśle.
