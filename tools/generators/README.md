# Generatory bazy — dokumentacja dla kolejnych etapów

Te skrypty wygenerowały bazę etapu 1. **Są potrzebne w każdym następnym etapie**,
bo zapewniają spójność fonetyki, identyfikatorów i transkrypcji. Bez nich kolejne
partie danych rozjadą się z istniejącymi.

## Pliki

| Plik | Rola |
|---|---|
| `engine.py` | **Rdzeń.** Rozpoznawanie tonów, podział na sylaby, transkrypcja `pronunciationPolish`, wyliczanie `difficulty`, generowanie `commonMistakes`, klasa `Builder` (unikalne ID + deduplikacja). |
| `lex_core.py` | Leksyka: podstawy, jedzenie, miejsca, transport. |
| `lex_core2.py` | Leksyka: zakupy, zdrowie, ludzie, dom, czasowniki, przymiotniki, liczby, czas, pytania. |
| `lex_phrases.py` | Około 140 ręcznie opracowanych zwrotów użytkowych. |
| `lex_dialogues.py` | 34 dialogi etapu 1. |
| `generate.py` | Szablony zdaniowe + zapis plików słownikowych. |
| `build_rest.py` | Dialogi, gramatyka, wymowa, kategorie, metadane, manifest. |
| `gender_forms.py` | **Reguły form zależnych od płci mówiącego.** khráp → khâ/khá, phǒm → chǎn/dì-chǎn, rozpoznawanie „phǒm = włosy”, kierunek odwrotny dla ról męskich. Współdzielony z `tools/validate.py`. |
| `build-gender-variants.py` | Dopisuje `genderVariant.female` do rekordów, przykładów, kwestii dialogów i wzorców gramatycznych; oznacza płeć ról. Idempotentny. |

## Jak uruchomić

```bash
cd tools/generators
python3 generate.py      # pliki słownikowe
python3 build_rest.py    # dialogi i pliki pomocnicze
cd ../..
python3 tools/generators/build-gender-variants.py   # warianty żeńskie
python3 tools/build-offline-data.py   # kopie JS dla trybu file://
python3 tools/validate.py             # kontrola jakości
```

**Kolejność ma znaczenie.** `build-gender-variants.py` liczy warianty z treści męskiej,
więc musi iść po generatorach leksyki, a przed `build-offline-data.py` — inaczej kopie
dla trybu `file://` rozjadą się z plikami JSON i walidator to zgłosi.

Skrypty zapisują wynik do katalogu `data/`. Ścieżki są względne wobec katalogu
`tools/generators`, więc uruchamiaj je z tego katalogu.

## Zasady, których nie wolno złamać w kolejnych etapach

1. **Transkrypcja `pronunciationPolish` musi iść przez `engine.py`.** Kolejność
   reguł ma znaczenie (`aw`→`o` przed `ch`→`cz` itd.). Ręczne pisanie tego pola
   da niespójny zapis między partiami danych.
2. **ID nadaje wyłącznie `Builder`** — pilnuje unikalności w obrębie całej bazy.
   Wzorzec: `<prefiks poziomu>-<slug kategorii>-<numer 4-cyfrowy>`.
3. **Deduplikacja działa na parze (polski, fonetyka)** — przed dopisaniem nowej
   partii trzeba wczytać istniejące pliki, żeby nie powielić haseł.
4. **Pole `ttsThai` jest obowiązkowe** w każdym rekordzie i w każdym przykładzie.
   Walidator odrzuci rekord bez niego.
5. **Nie zmieniaj formatu rekordu.** Aplikacja i walidator zakładają obecny zestaw pól.

## Uwaga o jakości danych szablonowych

Rekordy powstają z rdzenia ręcznie opracowanych haseł pomnożonego przez wzorce
zdaniowe. Konstrukcje tajskie są poprawne, ale **polska strona bywa sztuczna**
(np. „trochę za urocze"). Przy rozbudowie bazy warto:

- ograniczać szablony do przymiotników i czasowników, dla których dana konstrukcja
  brzmi naturalnie po polsku (białe listy zamiast iloczynu kartezjańskiego),
- w polu `source` odróżniać rdzeń zweryfikowany od rekordów szablonowych — pole jest
  tekstowe, więc nie wymaga zmiany schematu.

---

## Etap 2 — domknięcie poziomu A1

| Plik | Rola |
|---|---|
| `lex_a1_stage2.py` | Leksyka etapu 2: rdzeń (pogoda, przyroda, rodzina, miesiące, liczby, pieniądze, zdrowie, emocje, dom, hotel, transport, czasowniki, przymiotniki) oraz wzorce zdaniowe z **białymi listami** słów. |
| `lex_dialogues2.py` | 30 nowych dialogów Survival/A1. |
| `stage2.py` | Dopisuje rekordy i dialogi do istniejących plików, przelicza `categories.json`, `metadata.json`, `manifest.json`. |
| `stage2_cleanup.py` | Usuwa artefakty językowe etapu 1 (rodzina „trochę za urocze”) i uzupełnia brakujące miejsca hasłami z rezerwy. |
| `reserve-stage3.json` | Hasła gotowe, ale nieużyte — limit 1000 rekordów w `a1-part-02.json` został wyczerpany. |

```bash
cd tools/generators
python3 stage2.py            # dopisuje dane etapu 2
python3 stage2_cleanup.py    # sprząta artefakty i wyrównuje liczniki
cd ../..
python3 tools/build-offline-data.py
python3 tools/validate.py
```

Oba skrypty są **idempotentne**: nie nadpisują plików od zera, tylko dopisują to,
czego jeszcze nie ma. Powtórne uruchomienie nie zdubluje żadnego hasła.

### Czego nauczył etap 2

1. **Białe listy zamiast iloczynu kartezjańskiego.** Każdy wzorzec zdaniowy ma
   zamkniętą listę słów, dla których wynik brzmi naturalnie po polsku, a polska
   strona rekordu i przykładu jest pisana ręcznie, nie sklejana z fragmentów.
2. **Pole `source` rozróżnia pochodzenie rekordu** — rdzeń zweryfikowany ręcznie
   od materiału wzorcowego. Pole jest tekstowe, więc nie łamie schematu.
3. **Deduplikacja po samym polskim haśle**, nie tylko po parze (polski, tajski).
   Bez tego do bazy trafiały hasła identyczne dla użytkownika, a różne technicznie
   (np. „wolny” = powolny i „wolny” = niezajęty).
4. **Hasła bazowe wzorców są chronione przed odłożeniem do rezerwy** — rekord
   „bardzo miękki” bez rekordu „miękki” zostawiałby dziurę dydaktyczną.

---

## Etap 3 — poziom A2

| Plik | Rola |
|---|---|
| `lex_a2_core_a.py` | Rdzeń A2: restauracja rozszerzona, preferencje i opinie, rezerwacje. |
| `lex_a2_core_b.py` | Rdzeń A2: hotel i problemy z pokojem, transport lokalny, ustalanie spotkań, telefon i internet. |
| `lex_a2_core_c.py` | Rdzeń A2: zdrowie, apteka i lekarz, wygląd i ubrania, dom i mieszkanie. |
| `lex_a2_core_d.py` | Rdzeń A2: praca, hobby, relacje, problemy, prośby, reakcje, uprzejma odmowa, przeszłość i plany. |
| `lex_a2_tpl_a.py` | Wzorce czasownikowe (`khoei`, `kamlang … yùu`, `phôoeng`, `mâi tâwng … kâw dâai` itd.). |
| `lex_a2_tpl_b.py` | Wzorce przymiotnikowe (`kwàa`, `thîi sùt`, `koen pai`, `mâi khâwi`, `rúu-sùek` itd.). |
| `lex_a2_tpl_c.py` | Wzorce rzeczownikowe (`hǎa … yùu`, `tham … hǎai`, `fàak … wái`, `chái … dâai mǎi` itd.). |
| `lex_a2_tpl_d.py` | Umiejętności, częstotliwość, jedzenie, miejsca (`pen`, `bàwi`, `thúk wan`, `khoei pai`). |
| `lex_a2_tpl_e.py` | Powinność i dokonanie (`khuan`, `mâi than`, `sèt láew`, `jam … dâai`). |
| `lex_a2_tpl_f.py` | Uzupełnienie puli do 2000 rekordów. |
| `lex_a2_dialogues_a.py` | 20 dialogów A2: restauracja, hotel, transport, spotkania. |
| `lex_a2_dialogues_b.py` | 20 dialogów A2: zdrowie, zakupy, praca, relacje, mieszkanie. |
| `stage3.py` | Buduje `a2-part-01.json`, `a2-part-02.json`, `dialogues-part-02.json` i przelicza liczniki. |
| `reserve-stage4.json` | Hasła gotowe, nieużyte — limit 2000 rekordów A2 został wyczerpany. |

```bash
cd tools/generators
python3 stage3.py
cd ../..
python3 tools/build-offline-data.py
python3 tools/validate.py
```

`stage3.py` odtwarza pliki A2 od zera z tego samego materiału źródłowego, więc jest
idempotentny. Nie dotyka plików poziomów Survival i A1.

### Czego nauczył etap 3

1. **Deduplikacja musi być trzystopniowa.** Poza polskim hasłem i parą
   (polski, tajski) trzeba sprawdzać samo zdanie tajskie. Bez tego wzorzec
   „Chciałbym odpocząć" tworzył rekord identyczny fonetycznie z istniejącym
   „Chcę: odpoczywać" — dla użytkownika to ta sama karta do nauki.
2. **Nowe wzorce muszą być inną konstrukcją, nie inną partykułą.** Poziom A1
   zużył już `phǒm yàak …`, `phǒm tâwng …`, `… mâi dâai`, `… láew`.
   Dorzucenie samego „khráp" nie tworzy nowej treści dydaktycznej, tylko duplikat.
   Etap 3 sięga po konstrukcje nieużywane wcześniej: `khoei`, `phôoeng`,
   `kamlang … yùu`, `mâi khâwi`, `koen pai`, `pen` w znaczeniu umiejętności.
3. **Hasła bazowe wzorców bierzemy z całej bazy, nie tylko z nowego rdzenia.**
   Dzięki temu 78 wzorców A2 opiera się na zweryfikowanych już czasownikach
   i przymiotnikach z poziomów Survival i A1, a nie na materiale dopisanym obok.
4. **Rejestr wpisujemy przy haśle, nie wyliczamy z fonetyki.** Etap 2 ustawiał
   „uprzejmy" na podstawie obecności `khráp`, przez co wszystko wyglądało tak samo.
   Etap 3 rozróżnia neutralny, formalny, nieformalny i potoczny — to informacja,
   której nie da się odtworzyć z samego zapisu dźwiękowego.
5. **Tytuły dialogów też wymagają deduplikacji.** Cztery dialogi A2 kolidowały
   tytułem z etapem 2 i skrypt je odrzucił, zanim trafiły do pliku.

---

## Etap 4 — poziom B1

| Plik | Rola |
|---|---|
| `lex_b1_core_a.py` | Rdzeń B1: naturalna rozmowa, rozwijanie opinii, zgoda, niezgoda, uprzejme kontrargumenty, łagodzenie wypowiedzi. |
| `lex_b1_core_b.py` | Rdzeń B1: opowiadanie historii, doświadczenia z przeszłości, plany, marzenia, cele. |
| `lex_b1_core_c.py` | Rdzeń B1: problemy w usługach, reklamacje, bank, płatności, formalności codzienne. |
| `lex_b1_core_d.py` | Rdzeń B1: praca, spotkania, zadania, opinia zwrotna, warunki zatrudnienia. |
| `lex_b1_core_e.py` | Rdzeń B1: wynajem mieszkania, umowa i kaucja, naprawy i usterki, technologia. |
| `lex_b1_core_f.py` | Rdzeń B1: podróże po Tajlandii, relacje międzyludzkie, konflikty i godzenie się. |
| `lex_b1_core_g.py` | Rdzeń B1: zdrowie — dokładniejszy opis objawów, wywiad lekarski, apteka. |
| `lex_b1_react.py` | **146 naturalnych reakcji rozmówcy**: wtrącenia, potwierdzenia, zaskoczenie, współodczuwanie, podtrzymywanie rozmowy. |
| `lex_b1_connect.py` | Wyrażenia łączące dłuższą wypowiedź oraz pary rejestrowe formalne/potoczne. |
| `lex_b1_tpl_a.py` | Wzorce czasownikowe: warunek, zamiar, nadzieja, obawa, staranie, ustępstwo, przybliżenie. |
| `lex_b1_tpl_b.py` | Wzorce przymiotnikowe: przypuszczenie, zawiedzione oczekiwanie, stopniowanie zależne, kontrargument. |
| `lex_b1_tpl_c.py` | Wzorce rzeczownikowe: problemy, reklamacje, tematy rozmowy, zależności, odpowiedzialność. |
| `lex_b1_tpl_d.py` | Wzorce czasownikowe z dużymi białymi listami: brak czasu, niechęć, przyzwyczajenie, częstotliwość. |
| `lex_b1_tpl_e.py` | Wzorce rzeczownikowe: jedzenie, miejsca, pobyt, rekomendacje, alergie, zamiana. |
| `lex_b1_dialogues_a.py` | 20 dialogów B1: opinie, opowieści, praca, reklamacje, bank, formalności. |
| `lex_b1_dialogues_b.py` | 20 dialogów B1: wynajem, naprawy, technologia, podróże, konflikty, zdrowie. |
| `stage4.py` | Buduje `b1-part-01/02/03.json`, dopisuje 40 dialogów B1 do `dialogues-part-02.json`, przelicza liczniki. |
| `reserve-stage5.json` | Hasła gotowe, nieużyte — limit 2500 rekordów B1 został wyczerpany. |

```bash
cd tools/generators
python3 stage4.py
cd ../..
python3 tools/build-offline-data.py
python3 tools/validate.py
python3 tools/audit.py
```

`stage4.py` odtwarza pliki B1 od zera z tego samego materiału źródłowego, a dialogi
dopisuje po tytule, więc powtórne uruchomienie niczego nie zdubluje. Nie dotyka
plików poziomów Survival, A1 i A2.

### Nowe narzędzia

| Plik | Rola |
|---|---|
| `tools/audit.py` | Raport zawartości bazy: liczby rekordów, dialogi, duplikaty ID, braki przykładów, poziomów i fonetyki, rozkład rejestru, pochodzenie rekordów. |
| `tools/bench-load.js` | Pomiar czasu wczytania bazy w prawdziwym Chromium, osobno dla `file://` i serwera HTTP. Sprawdza też, czy pole `ttsThai` nie wycieka do obiektów aplikacji. |

### Czego nauczył etap 4

1. **Wzorce muszą być konstrukcją, nie ozdobnikiem.** Poziomy A1 i A2 zużyły już
   `yàak`, `tâwng`, `khoei`, `phôoeng`, `kamlang … yùu`, `mâi khâwi`, `koen pai`.
   Etap 4 sięga po konstrukcje złożone, których nie da się zbudować przez dodanie
   partykuły: `thâa … kâw …`, `kwàa … jà …`, `mâi wâa … kâw …`, `thǔeng máe wâa …`,
   `yîng … yîng …`, `mâi nâe-jai wâa … rǔe plào`, `tham hâi …`, `mâi châi wâa mâi …`.
2. **Reakcje rozmówcy to osobny materiał dydaktyczny.** Bez stu kilkudziesięciu
   drobiazgów w rodzaju „nân ná sì", „âw yàang níi níi eeng", „khôi yang chûa"
   rozmowa brzmi jak przesłuchanie. Te rekordy trzeba pisać ręcznie — żaden wzorzec
   ich nie wygeneruje.
3. **Rejestr trzeba oznaczać przy haśle, a slang dodatkowo ostrzeżeniem.** Siedem
   rekordów B1 ma w polu `notes` wyraźne „SLANG" wraz z informacją, **gdzie tego
   nie używać**. Sama etykieta „potoczny" jest za słaba: uczący się musi wiedzieć,
   że „dàek" obrazi rozmówcę, a „phaeng wôoe" zabrzmi jak zarzut wobec sprzedawcy.
4. **Konstrukcja ma być tajska, nie przetłumaczona.** Kilka miejsc wymagało
   świadomego odejścia od polskiej składni: „tòk rót" (spóźnić się na autobus,
   dosłownie „spaść z pojazdu"), „khít thǔeng" (tęsknić), „jon kwàa jà …" (dopóki
   nie — bez przeczenia po tajsku), „… maa naan láew" (polski czas teraźniejszy,
   tajska konstrukcja dokonana).
5. **Przy 7280 rekordach czas ładowania zaczyna mieć znaczenie.** Aplikacja wczytuje
   całą bazę do pamięci przy starcie: około 0,7 s w obu trybach przy rozgrzanej
   pamięci podręcznej, około 1,6 s przy pierwszym, zimnym wczytaniu przez serwer.
   Przy poziomie B2 warto rozważyć ładowanie plików poziomów na żądanie —
   `manifest.json` już zawiera potrzebne metadane, więc zmiana dotknie wyłącznie
   `js/data-loader.js`.
6. **Deduplikacja odrzuciła 58 rekordów** mimo świadomego doboru konstrukcji:
   39 po polskim haśle i 19 po samym zdaniu tajskim. Bez sprawdzania wobec całej
   bazy, a nie tylko wobec nowej partii, trafiłyby do niej powtórki z poziomu A2.

---

## Etap 5 — poziom B2

| Plik | Rola |
|---|---|
| `lex_b2_core_a.py` | Rdzeń B2: prowadzenie dłuższej rozmowy — wypełniacze, granie na czas, zabieranie i oddawanie głosu, parafraza, sprawdzanie zrozumienia, kłopot ze słowem. |
| `lex_b2_core_b.py` | Rdzeń B2: subtelności grzeczności — prośby, odmowy i sugestie ułożone według stopnia uprzejmości, łagodzenie wypowiedzi. |
| `lex_b2_core_c.py` | Rdzeń B2: negocjowanie i argumentowanie — kontrpropozycja, ustępstwo, zamykanie ustaleń, podważanie cudzego argumentu, wątpliwości. |
| `lex_b2_core_d.py` | Rdzeń B2: konflikty i emocje — zgłaszanie niezadowolenia, przeprosiny o różnej sile, godzenie się, stawianie granic. |
| `lex_b2_core_e.py` | Rdzeń B2: praca i klient — zebrania, delegowanie, opinia zwrotna, obsługa klienta, wyjaśnianie procedur i problemów technicznych. |
| `lex_b2_core_f.py` | Rdzeń B2: życie w Tajlandii — wiza i imigracja, bank i podatki, długoterminowy najem, sąsiedzi, szkoła dziecka, ubezpieczenie. |
| `lex_b2_core_g.py` | Rdzeń B2: sytuacje awaryjne wymagające precyzji — wezwanie pomocy, lokalizacja, stan poszkodowanego, wypadek, kradzież, ambasada. |
| `lex_b2_idioms.py` | **57 idiomów, slangu i kolokacji.** Każdy rekord ma w `notes` etykietę IDIOM / SLANG / KOLOKACJA, a przy slangu — informację, **gdzie tego nie używać**. |
| `lex_b2_register.py` | **38 komunikatów × 3 rejestry = 114 rekordów.** Ten sam komunikat formalnie, neutralnie i potocznie. Notatka każdego rekordu podaje pozostałe dwa warianty fonetycznie oraz sytuację użycia. |
| `lex_b2_tpl_a.py` | Wzorce czasownikowe: prośba o czas, zaprzeczenie możliwości, ciągłość od zawsze, wstrzymanie czynności, gotowość warunkowa, brak konieczności, czynność o włos niedokonana. |
| `lex_b2_tpl_b.py` | Wzorce przymiotnikowe: ostrożne stopniowanie, „jeszcze bardziej”, zawiedzione oczekiwanie, ocena wystarczalności, zaprzeczenie obiegowej opinii, tendencja w czasie, ocena subiektywna. |
| `lex_b2_tpl_c.py` | Wzorce rzeczownikowe: otwarcie tematu, prośba o dane, wskazanie obawy, zależność, negocjowanie punktu, odpowiedzialność, potwierdzanie ustaleń. |
| `lex_b2_tpl_d.py` | Wzorce czasownikowe, druga seria: przymus zewnętrzny, nawyk większościowy, zbieżność zamiaru, ostatnia okazja, gotowość usługowa, elastyczność terminu, żal po niezrealizowanym. |
| `lex_b2_tpl_e.py` | Wzorce rzeczownikowe, druga seria: braki, przygotowanie, związek przyczynowy, weryfikacja, waga sprawy, zakres ubezpieczenia, wzrost kosztów, przekazanie sprawy. |
| `lex_b2_tpl_f.py` | Ramy grzecznościowe na czasownikach: prośba formalna, łagodna odmowa, sugestia zespołowa, przeprosiny za niemożność, akceptacja obu wyjść, pytanie o doskonalenie, propozycja kolejności, uprzejme upomnienie. |
| `lex_b2_dialogues_a.py` | 20 dialogów B2: negocjacje, reklamacje, spory w pracy, obsługa klienta, procedury urzędowe, rozmowa kwalifikacyjna. |
| `lex_b2_dialogues_b.py` | 20 dialogów B1/B2: wiza, awarie, rejestry w praktyce, emocje, idiomy w użyciu, bank, szkoła, zdrowie. |
| `stage5.py` | Buduje `b2-part-01/02.json` oraz `dialogues-part-03.json` i przelicza liczniki. |
| `reserve-stage6.json` | Hasła gotowe, nieużyte — limit 2000 rekordów B2 został wyczerpany. |

```bash
cd tools/generators
python3 stage5.py
cd ../..
python3 tools/build-offline-data.py
python3 tools/validate.py
python3 tools/audit.py
```

`stage5.py` odtwarza pliki B2 i plik dialogów etapu 5 od zera z tego samego
materiału źródłowego, więc jest idempotentny. Nie dotyka plików poziomów
Survival, A1, A2 i B1 ani wcześniejszych plików dialogów.

### Czego nauczył etap 5

1. **Rejestr trzeba pokazywać w trójkach, nie opisywać przymiotnikiem.** Etykieta
   „formalny" nic nie mówi, dopóki uczący się nie widzi obok wersji neutralnej
   i potocznej tego samego komunikatu. Dlatego `lex_b2_register.py` generuje
   rekordy pętlą: notatka każdego z trzech wariantów podaje pozostałe dwa
   fonetycznie oraz sytuację, w której danego wolno użyć. Ręczne pisanie tych
   notatek dałoby 114 różnych sformułowań tej samej informacji.
2. **Przy slangu sama etykieta rejestru jest niebezpieczna.** Dwanaście rekordów
   B2 ma w `notes` wyraźne „SLANG" z informacją, gdzie słowa nie używać:
   „sǔeak" jest wulgarne, „phaeng wôoe" brzmi jak zarzut zdzierstwa wobec
   sprzedawcy, „sǔai wôoe" obraża przy starszych, a „sǐi sáw hâi khwaai fang"
   wolno odnieść do sytuacji, ale nigdy do rozmówcy — nazwanie kogoś bawołem
   to ciężka obelga.
3. **Awaria wymaga kolejności, nie słownictwa.** `lex_b2_core_g.py` jest ułożony
   tak, żeby rekordy dały się złożyć w sekwencję: co się stało, gdzie, ilu ludzi,
   w jakim stanie. Sam zasób słów bez tej kolejności nie skraca rozmowy
   z dyspozytorem.
4. **Wzorce B2 musiały sięgnąć po konstrukcje biurowe i urzędowe.** Poziomy
   niższe zużyły całą prostą gramatykę, więc etap 5 pracuje na `khǎw wee-laa …
   sák khrûu`, `mâi mii thaang thîi jà … dâai`, `… maa tà-làwt`, `yàa phôoeng …`,
   `thâa jam pen tâwng …`, `thùuk bang-kháp hâi …`, `kìao khâwng doi trong`,
   `phà-nàek thîi kìao khâwng`, `trùat sàwp`, `khrâwp khlum`.
5. **Deduplikacja odrzuciła tylko 40 rekordów** (27 po samym zdaniu tajskim,
   13 po polskim haśle) — mniej niż w etapie 4, mimo większej partii danych.
   Powodem jest świadomy dobór konstrukcji nieużywanych wcześniej: im dalej od
   gramatyki poziomów A, tym mniejsze ryzyko kolizji.
6. **Test aplikacji przestał być wiązany z liczbami etapu.** `tools/test-app.js`
   miał wpisane na sztywno liczby z etapu 3 i po etapie 4 zgłaszał fałszywe
   błędy. Teraz czyta oczekiwania z `manifest.json` i sprawdza każdy poziom
   osobno, więc kolejne etapy nie wymagają jego poprawiania.

---

## Etap 6 — uzupełnienie praktyczne do 10 200 rekordów

Etap 6 nie dokłada nowego poziomu. Robi trzy rzeczy: czyści duplikaty wykryte przez
audyt, odzyskuje materiał odłożony w etapie 5 i dokłada nowe słownictwo praktyczne —
tak, żeby baza przekroczyła 10 000 rekordów z zapasem 200.

| Plik | Zawartość |
|---|---|
| `lex_s6_verbs.py` | **87 rekordów.** Częste czasowniki zapisane razem z użyciem: ruch, branie i dawanie, mówienie, myślenie i decyzje, czynności codzienne, próba i powodzenie, pomaganie, stany i odczucia, początek i koniec, szukanie, rodzina wyrażeń z `jai`. |
| `lex_s6_adj.py` | **58 rekordów.** Ocena rzeczy i usług, stopień i miara, częstotliwość, kolejność zdarzeń, pory dnia, punkty na osi czasu, wielkość i przestrzeń, cena i wartość, pogoda i otoczenie. |
| `lex_s6_react.py` | **45 rekordów.** Krótkie reakcje rozmówcy (potwierdzenie, zaskoczenie, współodczuwanie, podtrzymanie rozmowy) oraz spójniki i zwroty organizujące dłuższą wypowiedź. |
| `lex_s6_travel.py` | **51 rekordów.** Lotnisko i dworzec, bilety, taksówka i wynajem, hotel w praktyce, restauracja poza zamawianiem, sklep i targ, fryzjer, pralnia, warsztat, poczta, bank. |
| `lex_s6_safety.py` | **42 rekordy.** Objawy, wywiad lekarski, apteka, sytuacja nagła w układzie sekwencyjnym (co się stało → gdzie → ilu → w jakim stanie), bezpieczeństwo codzienne. |
| `lex_s6_life.py` | **42 rekordy.** Praca na co dzień, sprawy do załatwienia, wyrażenia potoczne **bezpieczne** (każde z etykietą POTOCZNE i notatką, gdzie nie używać) oraz pary i trójki rejestrowe. |
| `lex_s6_tpl.py` | 15 wzorców, 263 pozycje: przypomnienie, przejęcie czynności, brak sił, pytanie o doświadczenie, zapotrzebowanie, zdolność formalna, gotowość, chęci, zapobiegliwość, zachęta, pytanie o osobę i o miejsce, brak zasobu, dostępność w okolicy, sprostowanie. |
| `lex_s6_tpl_b.py` | 10 wzorców, 124 pozycje: prośba o instrukcję, pytanie o dokonanie, przyznanie się do niewiedzy, prośba o odstępstwo, wątpliwość, prośba o lepszą opcję, wybór, zguba, liczba powtórzeń, dostępne dni. |
| `lex_s6_tpl_c.py` | 7 wzorców, 92 pozycje: uczulenia, dokładka, skład dania, łagodniejsza wersja potrawy, działanie wspólne, pytanie o powód obowiązku, odwołanie do zwyczaju. |
| `lex_s6_tpl_d.py` | 8 wzorców, 122 pozycje: przeniesienie terminu, prośba o pośpiech, zakazy, własność, opłaty dodatkowe, wersja dla dzieci, cena konkretnej rzeczy, obowiązek powszechny. |
| `stage6.py` | Czyści duplikaty, odzyskuje rezerwę etapu 5, buduje `supplemental-practical.json` i przelicza liczniki. |
| `reserve-stage7.json` | Nadwyżka ponad cel 10 200 — hasła gotowe, nieużyte. |

```bash
cd tools/generators
python3 stage6.py
cd ../..
python3 tools/build-offline-data.py
python3 tools/validate.py
python3 tools/audit-quality.py
```

`stage6.py` jest idempotentny: czyszczenie działa tylko wtedy, gdy jest co usunąć,
a plik uzupełniający odtwarza od zera z tego samego materiału źródłowego.

### Czego nauczył etap 6

1. **Audyt duplikatów musi patrzeć na fonetykę, nie tylko na hasło polskie.**
   Poprzednie etapy sprawdzały polskie hasło, parę (polski, tajski) i samo zdanie
   tajskie — i wszystkie te testy wychodziły czysto. Dopiero zestawienie po samej
   fonetyce pokazało 17 par, w których to samo tajskie zdanie występowało pod dwoma
   niemal identycznymi polskimi hasłami („odpoczywać" i „odpocząć", „wysiadać"
   i „wysiąść", „torba" i „torba na zakupy"). Dla uczącego się to jedna i ta sama
   karta pokazana dwa razy.
2. **Nie każdy powtórzony zapis fonetyczny jest duplikatem.** Z 17 par jedna została:
   `sâwm` to zarówno widelec (ส้อม), jak i naprawiać (ซ่อม) — dwa różne słowa tajskie
   o identycznej wymowie. Rozstrzygającym testem jest **pole `ttsThai`**, nie fonetyka.
3. **Usunięcie rekordu nie może usunąć hasła z wyszukiwarki.** Polskie warianty
   znaczeniowe kasowanych rekordów trafiły do `polishAlternatives` rekordu
   zachowanego. Dodatkowo `stage6.py` musi zasiać nimi indeks haseł bazowych —
   inaczej wzorce etapu 5, które się na nie powoływały, przestałyby się odtwarzać.
   Idempotentność generatorów oznacza, że kasowanie danych ma skutki uboczne
   w skryptach, nie tylko w plikach.
4. **Przy 9000 rekordów w bazie deduplikacja odrzuca większość nowego materiału.**
   Z puli 3149 kandydatów odpadło 2196 pozycji — 2086 dlatego, że polskie hasło już
   istniało. Rdzeń pisany ręcznie stracił 120 z 323 pozycji: „boli mnie głowa"
   czy „na wynos" po prostu były już w bazie. Wniosek na kolejne etapy: przy tej
   wielkości bazy trzeba planować **trzykrotną nadwyżkę materiału** względem celu.
5. **Odłożona rezerwa okazała się zbyt uboga, żeby ją odtworzyć wprost.**
   `reserve-stage6.json` przechowywał tylko pięć pól, bez przykładów i notatek —
   za mało na pełny rekord. Zamiast odczytywać rezerwę, `stage6.py` uruchamia
   ponownie generatory etapu 5: wszystko, co już jest w bazie, odpada na deduplikacji,
   a zostaje dokładnie 184 odłożone pozycje, tym razem kompletne. `reserve-stage7.json`
   zapisuje dodatkowo poziom, ale ta metoda i tak pozostaje właściwą.
6. **Wzorce trzeba dobierać po zbadaniu, co jest zajęte.** Przed napisaniem
   czterdziestu nowych konstrukcji każda została sprawdzona `grepem` po polu
   `thaiPhonetic` całej bazy. Wybrano wyłącznie te o zerowym lub minimalnym pokryciu:
   `yàa luem`, `hâi phǒm … eeng`, `… mâi wǎai`, `khoei … mǎi`, `tâwng kaan`,
   `sǎa-mâat … dâai`, `phráwm jà`, `tem jai thîi jà`, `… wái kàwn`, `… kan thòe`,
   `mii khrai … bâang mǎi`, `… trong nǎi dii`, `mâi mii … loei`, `thǎew níi mii …`,
   `hâam …`, `khǎwng khrai`, `tâwng jàai khâa …`, `thúk khon tâwng …`.
   Dzięki temu odrzuty po zdaniu tajskim wyniosły tylko 110 na 953 zbudowane rekordy.
7. **Białe listy muszą wskazywać hasła, które naprawdę istnieją.** Dwa razy budowa
   przerwała się na `SystemExit` — raz przez „odpocząć" skasowane w czyszczeniu,
   raz przez „palić papierosy", którego w bazie nigdy nie było. To zachowanie jest
   pożądane: lepszy twardy błąd niż rekord zbudowany z pustego miejsca. Brakujące
   hasło dopisano do rdzenia etapu 6, bo samo w sobie było przydatne.

## Etap 7 (sesja F) — rdzeń leksykalny

### Diagnoza

Baza miała 10 200 rekordów, ale tylko **763 typu `word`** i **1 217 unikalnych
tokenów sylabicznych**. Dziesięć tysięcy rekordów stało na słowniku rzędu tysiąca
jednostek — reszta to warianty zdaniowe tego samego materiału. Systemy zamknięte
były puste albo prawie puste: z trzynastu kolorów podstawowych nie było żadnego,
z piętnastu warzyw żadnego, z dwudziestu części ciała jedna, z liczebników
porządkowych 3–20 żadnego. To blokowało całe klasy wypowiedzi mimo dużej bazy.

### Co robi `stage7.py`

Buduje `data/core-lexicon-01.json` i `data/core-lexicon-02.json` wyłącznie
z rekordów typu `word` — krótkich haseł w mianowniku, każde z dwoma lub trzema
przykładami. Nie generuje zdań: zdań w bazie jest już 6 202. Materiał pochodzi
z 21 modułów `lex_f_*.py`; kolejność w `GROUPS` stawia systemy zamknięte na
początku, żeby w razie jakiegokolwiek limitu to one weszły w całości.

### Wynik

Z 908 kandydatów przyjęto **555** (punkt stały — patrz wniosek 5), odrzucono 353.
Baza urosła do 10 755 rekordów,
`word` z 763 do 1 318, tokeny sylabiczne z 1 217 do 1 408.

### Wnioski dla kolejnych etapów

1. **Przestrzeń częstego słownictwa jest bliska nasycenia.** Rozbiór odrzutów:
   161 kandydatów miało polskie hasło już obecne w bazie jako `word`, kolejne 149
   odpadło na kolizji zapisu tajskiego (synonim już był), a tylko 11 kolidowało
   z typami innymi niż `word`. Odsetek przyjęć spadał wraz z kolejnymi modułami:
   kolory 22/23, warzywa 22/26, ale podróż 9/32 i przymiotniki II 12/48. Przy
   ~1 300 rekordach `word` dalsza rozbudowa oznacza wchodzenie w słownictwo rzadkie.
   Kolejny etap powinien to założyć z góry albo zmienić cel z liczby rekordów
   na jakość powiązań.
2. **Deduplikacja po zapisie tajskim wymaga normalizacji białych znaków.**
   „นานๆ ที" i „นานๆที" to to samo hasło, a różnica jednej spacji przepuściła
   duplikat przez trzy stopnie kontroli. Funkcja `thai_key()` usuwa białe znaki
   przed porównaniem. Cztery pozostałe powtórzenia fonetyki, które zgłasza
   `audit-quality.py`, to prawdziwe homofony o różnym zapisie tajskim
   (`sâwm` widelec/naprawiać, `yâa` trawa/babcia, `tàe` ale/dotykać,
   `lâo` alkohol/opowiadać) — są opisane w polu `notes` i mają zostać.
3. **Relacje zapisywane po polskim haśle wymagają trzech prób rozwiązania.**
   Moduły wskazują powiązania słowem, nie identyfikatorem, bo ID nadaje `Builder`
   dopiero przy budowie. Samo dopasowanie dosłowne dało 857 powiązań. Dodanie
   dopasowania po haśle bez nawiasu (`kolor (barwa)` → `kolor`) podniosło je do
   1 148. Trzeci stopień — pamiętanie zapisu tajskiego haseł odrzuconych przez
   dedup i wskazywanie rekordu bazowego o tym samym brzmieniu — dał 1 364
   powiązań przy 83 nierozwiązanych kluczach. Bez tego stopnia hasło odrzucone
   jako duplikat zabierało ze sobą wszystkie kierujące do niego relacje.
4. **`tools/test-app.js` mierzył stan po `DB.ready`, a porównywał z sumami
   z manifestu.** `DB.ready` oznacza wczytanie jednego pliku startowego, resztę
   dociąga `DB.loadAll()`. Test zgłaszał więc cztery fałszywe błędy — również na
   nietkniętej bazie v1.5.0, co potwierdzono na rozpakowanej kopii wejściowej.
   Dodano oczekiwanie na `DB.complete`. Warto pamiętać, że plikiem startowym jest
   **najmniejszy** plik słownikowy z manifestu, więc dodanie małego pliku zmienia
   to, co widzi ekran „Dzisiaj" przy pierwszym uruchomieniu.
5. **Warianty dopisane do bazy wracają jako klucz deduplikacji — build zbiega się,
   ale nie do tej samej liczby.** Hasła utracone na kolizji zapisu tajskiego
   (np. „świnia" wobec istniejącej „wieprzowiny" — jedno หมู) trafiają przez
   `merge_aliases()` do `polishAlternatives` rekordu bazowego, żeby nie zniknęły
   z wyszukiwarki. Ale `Pool` zasiewa `seen_polish` właśnie z `polishAlternatives`,
   więc przy następnym przebiegu kandydat o takim haśle odpada już na pierwszym
   stopniu. Kolejne uruchomienia dały 558 → 557 → 555 → 555 → 555.

   **To zachowanie jest poprawne, nie jest usterką.** Jeśli „świnia" jest już
   wyszukiwalnym wariantem „wieprzowiny", to osobny rekord „świnia" byłby
   duplikatem — 555 jest odpowiedzią właściwszą niż 558. Trzeba jednak wiedzieć,
   że **pierwszy przebieg na świeżej bazie daje wynik zawyżony o kilka rekordów**,
   a punkt stały pojawia się dopiero przy trzecim. Kolejny etap powinien albo
   uruchamiać `stage7.py` dwukrotnie przed raportowaniem liczb, albo liczyć się
   z tym, że raport z pierwszego przebiegu nie odpowiada zawartości plików po
   ponownym uruchomieniu. Sam `merge_aliases()` jest idempotentny (drugi przebieg
   dopisuje 0 wariantów) — nieidempotentna jest liczba zbudowanych rekordów.

---

## Etap 8 (sesja G) — sesja naprawcza

Etap 8 nie dokłada materiału. Poprawia to, co już jest, w miejscu, z zachowaniem
identyfikatorów. Liczba rekordów przed i po jest ta sama: **10 755**.

### Diagnoza

Audyt zgłosił 2 959 rekordów z dwukropkiem. Przeliczenie pokazało, że problem
jest o dwie trzecie większy, bo audyt patrzył wyłącznie na pole `polish`
rekordu: **4 906 wystąpień** — 2 959 w rekordach, 1 936 w przykładach
i 11 w kwestiach dialogowych. Wzorców było **131**, wstawek **491**.

Trzy inne pozycje audytu wymagały korekty:

| Audyt | Stan faktyczny |
|---|---|
| 41 sztucznych „trochę za X” | 43 rekordy, sztuczne **3**: „trochę za dobre”, „trochę za pełne”, „trochę za bardzo”. „Za drogie”, „za ostre”, „za daleko”, „za głośne” brzmią naturalnie i zostają |
| `an` do wszystkiego | `an níi` / `an nǎi` („ten tutaj”, „który?”) to **poprawny zaimek**, nie błąd. Błędem jest `an` przy rzeczowniku z własnym klasyfikatorem — 30 takich rzeczowników, 90 wystąpień |
| „Cena: 0 bahtów”, „Liczba osób: 0” | Sensowne jako ćwiczenie liczebnika, bezsensowne jako zdanie — przepisane na „Zero bahtów”, „Zero osób” zamiast usuwania |

Znalazły się też rekordy z **błędną stroną tajską**, których nie da się naprawić
samą polszczyzną. Opisane niżej we wniosku 4.

| Plik | Rola |
|---|---|
| `polish_grammar.py` | Odmiana polska na Morfeuszu 2 (SGJP): przypadki, liczba mnoga, uzgodnienie przydawki, liczebniki z odmianą rzeczownika, czas przeszły z bezokolicznika. Cache w `inflect-cache.json`. |
| `fix_polish.py` | Reguły dla wszystkich 131 nagłówków: w jakim przypadku ma stanąć wstawka i jak zbudować zdanie. Lista `KEEP` chroni dwukropki poprawne po polsku. |
| `classifiers.py` | 139 klasyfikatorów z wyjaśnieniem, rzeczownikami i przykładami liczenia. Mapa 190 rzeczowników i 30 poprawek `an` → właściwy klasyfikator. |
| `stage8.py` | Przebieg naprawczy: polszczyzna, klasyfikatory, drugie przykłady, `classifiers.json`, temat gramatyczny, liczniki. |

```bash
cd tools/generators
python3 stage8.py
cd ../..
python3 tools/build-offline-data.py
python3 tools/validate.py
```

`stage8.py` jest idempotentny — powtórne uruchomienie nie zmienia żadnego pliku
JSON (sprawdzone porównaniem zawartości, nie sum kontrolnych).

### Czego nauczył etap 8

1. **Odmiany nie da się zrobić regułami na końcówkach — trzeba słownika
   morfologicznego.** 491 wstawek to za dużo na ręczną tabelę i za mało
   regularności na reguły. Morfeusz 2 jest na PyPI i instaluje się bez
   problemu; `pymorphy2-dicts-pl` nie istnieje, więc to jedyna droga.
   Wynik jest zapisany w `inflect-cache.json`, żeby kolejna sesja nie musiała
   niczego instalować.
2. **Ośrodek frazy trzeba wyznaczać składniowo, nie kolejnościowo.** Pierwsza
   wersja brała pierwszy rzeczownik i psuła „starszy brat” („starszy” jest też
   rzeczownikiem). Wersja druga brała ostatni i psuła „umowa najmu”
   („umową najmem”). Działa dopiero reguła: wyraz jest przydawką tylko wtedy,
   gdy ma czytanie przymiotnikowe **i** dalej stoi rzeczownik, z którym może
   się uzgodnić. Żeńska „umowa” nie może być przydawką męskiego „najmu”,
   więc sama jest ośrodkiem.
3. **Generowanie z lematu wymaga pilnowania ogona tagu.** „smażony” i „smażący”
   dzielą lemat `smażyć`, „dobry” i „lepszy” lemat `dobry`. Bez porównywania
   klasy tagu i kwalifikatorów za rodzajem (`ppas` vs `pact`, `pos` vs `com`)
   „ryż smażony” odmieniał się na „ryżu smażącego”.
4. **Cztery rekordy miały sprzeczne zdanie tajskie i sama polszczyzna ich nie
   ratowała.** `phǒm pai kàp phǒm` znaczy „idę razem ze sobą”, a
   `phǒm jà klàp mûea waan` to czas przyszły z „wczoraj”. Zasada „strona tajska
   bez zmian” zderzyła się z zasadą „przepisz rekordy bezsensowne”. Rozstrzygnięcie:
   minimalna korekta tajskiego w tych czterech (plus jeden bliźniaczy rekord
   w `survival.json`), wypisana w `THAI_REPAIRS` i w polu `notes` każdego z nich.
   Wszystkie pozostałe 10 750 rekordów mają stronę tajską nietkniętą poza
   poprawkami klasyfikatorów.
5. **Kontrola przed nawrotem musi mieć listę wyjątków, nie heurystykę.**
   Dwukropek bywa poprawny — „Neutralnie: poproszę rachunek”, „Popatrzmy na to
   z innej strony: co zyskuje klient?”. Próba odróżnienia dobrych od złych po
   długości albo po obecności czasownika daje fałszywe trafienia w obie strony.
   `KOLON_DOZWOLONE` w `tools/validate.py` wymienia 19 dozwolonych nagłówków;
   każdy nowy daje ostrzeżenie i wymaga świadomej decyzji.
6. **Przy uzupełnianiu przykładów rama zdaniowa musi unikać uzgodnienia rodzaju.**
   Pierwsza wersja ramy przymiotnikowej dawała „To jest bardzo suchy” zamiast
   „suche”. Hasła są w formie słownikowej (męskiej), więc rama „Bardzo {hasło}”
   jest jedyną, która nie wymusza zgodności. Sto jeden rekordów trafiło dodatkowo
   na kolizję z przykładem już obecnym — stąd druga rama zapasowa dla każdego
   rodzaju hasła.
7. **Klasyfikator to nie to samo co zaimek o tym samym brzmieniu.** Ślepe
   zastąpienie `an` popsułoby 30 poprawnych rekordów z `an níi` („ten tutaj”)
   i `an nǎi` („który?”). Poprawka działa tylko wtedy, gdy `an` stoi przy
   rzeczowniku obecnym w tabeli i nie jest zaimkiem.

---

## Sesja N — rozszerzenie leksykalne

### Pliki

| Plik | Zawartość |
|---|---|
| `session_n.py` | generator główny: hasła, zdania aktywujące, kontrole, zapis |
| `lex_n_nature.py` | pogoda, niebo, woda, rośliny, zwierzęta, środowisko |
| `lex_n_move.py` | transport, miejsca i orientacja, hotel |
| `lex_n_people.py` | rodzina, ludzie, small talk, grzeczność, pytania |
| `lex_n_life.py` | dom, zdrowie, awarie, zakupy |
| `lex_n_work.py` | praca, nauka, czas, liczby |
| `lex_n_lang.py` | czasowniki, gramatyka, jedzenie, restauracja, cechy |
| `lex_n_extra.py` | ciało, ubranie, technika, drugi rzut czasowników |
| `lex_n_society.py` | państwo, media, ekonomia, wiara, społeczeństwo |
| `lex_n_mind.py` | rodzina wyrażeń na `jai`, uczucia, charakter, abstrakty |
| `lex_n_act.py` | czasowniki działania, materiały, narzędzia, dziedziny, klasyfikatory |
| `lex_n_balance.py` | partia wyrównująca rozkład |
| `lex_n_close.py` | partia domykająca próg 900 |

Uruchomienie: `python3 session_n.py` z katalogu `tools/generators`, potem kolejno
`build-gender-variants.py`, `build-colloquial.py`, `build-tts-split.py`, `lessons.py`,
`../update-manifest.py`, `../build-search-index.py`, `../build-offline-data.py`,
`../validate.py`.

### Format krotki

```
(poziom, polski, fonetyka, pismo, podkategoria, częstość, typ, kategoria, uwaga, dosłownie)
```

`lex_n_nature.py` jest wyjątkiem — ma jedną kategorię dla całego modułu, więc krotka
jest dziewięcioelementowa. Adapter w `session_n.py` obsługuje obie długości.

### Czego nauczyła ta sesja

1. **Rozkład kategorii nie mówi, czego brakuje.** Pogoda i przyroda miała 61 rekordów
   i wyglądała na największą lukę. Pierwsza partia napisana pod ten wniosek straciła
   512 z 989 kandydatów na duplikaty — burza, chmura i wodospad były w bazie od dawna,
   tylko w innych kategoriach. Lukę trzeba szukać po treści, nie po licznikach:
   najkrótsza droga to zrzucić wszystkie istniejące hasła do jednego pliku i pisać
   przeciwko niemu.

2. **Deduplikacja fonetyczna musi zachowywać tony.** Wersja bez tonów odrzuciła
   `thâm` (jaskinia) jako duplikat `tham` (robić) i `kàw` (wyspa) jako `kâw` (no i).
   W języku tonalnym ton jest częścią wyrazu, nie ozdobą. Pary minimalne są przy tym
   materiałem najcenniejszym — generator wypisuje je teraz osobno zamiast kasować.

3. **Deduplikacja znaczeniowa musi patrzeć na całą bazę, nie na same hasła.**
   Ograniczenie jej do `LEX_TYPES` przepuściło 17 kolizji w rodzaju „jak długo?",
   które w bazie istnieje jako pytanie (`naan thâo-rài khráp`), a nie jako hasło.
   Dwa różne zwroty tajskie pod jednym polskim tłumaczeniem to w słowniku szum:
   uczący się nie ma jak zgadnąć, który wybrać.

4. **Zdania generowane z szablonów kolidują z bazą i trzeba to sprawdzać przed
   zapisem.** Pierwszy przebieg dał 61 duplikatów międzysesyjnych — `mii hâwng wâang
   mǎi khráp` istniało już w materiale hotelowym. Szablonów jest po 5–10 na typ,
   a potrzebne są 3, więc kolizję wystarczy pominąć i wziąć następny szablon.

5. **Zdanie aktywujące musi być osobnym rekordem typu `sentence`.** Wpisanie go
   wyłącznie do `examples` wewnątrz hasła nic nie daje: `lessons.py` liczy jako
   aktywujące tylko rekordy spoza `LEX_TYPES`.

6. **Polską stronę szablonu trzeba odmieniać.** Bez tego wraca konwencja
   „Poproszę: woda", usunięta w sesji G z 2 959 rekordów. `polish_grammar` z Morfeuszem
   radzi sobie z żywotnością (`wąż → węża`) i z nieregularnościami (`klapki → klapek`),
   ale hasła z wielokropkiem (`mâi … looei`) i partykuły trzeba kierować do szablonów
   bezprzypadkowych — stąd `UNINFLECTABLE` i osobny zestaw `T_WORD`.

7. **Wydłużenie ścieżki uruchamia generatory na materiale, którego wcześniej nie
   dotykały.** `build-colloquial.py` obejmuje tylko rekordy w ścieżce, więc po skoku
   ze 132 do 314 lekcji wariant potoczny dostały rekordy, które go nie miały — i test
   tempa zaczął wybierać inny rekord niż dotąd. Po zmianie długości ścieżki należy
   przepuścić cały łańcuch budujący, a nie tylko walidator.

8. **Podział lekcji między poziomy jest ważniejszy niż ich łączna liczba.** Układ
   34/90/130/90/25 daje tyle samo słów (1 185) w 291 lekcjach co 34/78/104/74/25
   w 315, ale zjada ogon: A2 zabiera materiał, z którego wyższe poziomy miałyby
   budować, więc B1 spada do 37 lekcji, a B2 do zera. Liczby w `LESSONS_PER_LEVEL`
   są sufitami, nie kwotami — generator bierze tyle, ile potrafi ułożyć.
