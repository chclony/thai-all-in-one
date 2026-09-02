# Checklista testów: Windows, Android, iPhone

Trzy listy do przejścia ręcznie na prawdziwym sprzęcie. Automatyczne testy
(`tools/browser-test.js`) sprawdzają logikę i układ w silniku Chromium, ale nie zastąpią
sprawdzenia syntezy mowy, mikrofonu i instalacji na ekranie początkowym — te zachowują się
na każdym systemie inaczej.

Legenda: **[K]** = krytyczne, blokuje udostępnienie; **[W]** = ważne; **[D]** = dobre mieć.

---

## Windows (Chrome, Edge, Firefox)

### Uruchomienie
- [ ] **[K]** otwarcie `index.html` podwójnym kliknięciem (tryb `file://`) — aplikacja startuje
      i pokazuje hasło dnia
- [ ] **[K]** uruchomienie przez serwer (`python3 -m http.server 8123`) — to samo
- [ ] **[W]** start jest odczuwalnie natychmiastowy; pasek „Wczytuję resztę bazy…”
      znika po chwili
- [ ] **[W]** stopka nawigacji pokazuje 10200 haseł, 184 dialogi, wersję danych 1.16.0

### Dane i wyszukiwanie
- [ ] **[K]** ekran *Słownik* pokazuje 10 200 haseł
- [ ] **[K]** wyszukiwanie po polsku („rezerwacja”) zwraca wyniki
- [ ] **[K]** wyszukiwanie po fonetyce z tonami („náam”) i bez tonów („naam”) zwraca wyniki
- [ ] **[W]** wyszukiwanie bez łączników („sawatdii”) działa
- [ ] **[K]** filtry: poziom, kategoria, ulubione, sortowanie po trudności
- [ ] **[K]** **nigdzie nie widać pisma tajskiego** — przejdź przez wszystkie ekrany
      i otwórz kilka arkuszy szczegółów

### Dźwięk
- [ ] **[K]** przycisk odtwarzania mówi po tajsku (wymaga zainstalowanego głosu — patrz
      `docs/ograniczenia-tts.md`)
- [ ] **[K]** kliknięcie drugiego przycisku przerywa pierwsze odtwarzanie
- [ ] **[W]** przycisk „stop” na górnym pasku zatrzymuje odtwarzanie
- [ ] **[W]** przy braku głosu tajskiego pojawia się komunikat, a nie cisza
- [ ] **[W]** Firefox: sprawdź osobno — jego obsługa `SpeechSynthesis` bywa uboższa

### Nagrywanie
- [ ] **[K]** przez serwer HTTP: ekran *Mówienie* → „Nagraj siebie” → przeglądarka pyta
      o mikrofon → po zatrzymaniu „Odsłuchaj nagranie” działa
- [ ] **[W]** w trybie `file://` przycisk jest wyłączony z czytelnym wyjaśnieniem

### Sesja dnia (sesja R)
- [ ] **[K]** przycisk sesji na ekranie *Dzisiaj* uruchamia sesję na 10, 20 i 40 minut
- [ ] **[K]** „Co będzie w sesji?" pokazuje skład z uzasadnieniem każdego bloku
- [ ] **[K]** sesję da się przerwać („Przerwij i wróć później"), a po **odświeżeniu
      strony** wraca do tego samego kroku z tym samym zużytym czasem
- [ ] **[K]** zamknięcie i ponowne otwarcie karty nie kasuje postępu sesji
- [ ] **[W]** licznik „Krok X z Y · N z M min" odświeża się w trakcie stania na jednym
      zadaniu (co minutę)
- [ ] **[W]** „Pomiń ten blok" przechodzi do następnego, sesja się nie zacina
- [ ] **[W]** w bloku wymowy działa „Pomiń to hasło" — sprawdź **z odłączonym
      mikrofonem**, bo to jest przypadek, dla którego to wyjście powstało
- [ ] **[W]** sesja z poprzedniego dnia nie jest wznawiana: aplikacja proponuje nowy plan
- [ ] **[D]** po ukończeniu sesji podsumowanie pokazuje bloki i skuteczność

### Pokrycie, cele i tydzień (sesja R)
- [ ] **[K]** ekran *Dzisiaj* pokazuje pokrycie dla czterech kategorii
- [ ] **[K]** „Jak to liczymy" otwiera opis metody **wraz z listą ograniczeń**
- [ ] **[K]** ekran *Droga do celu* podaje dla każdej kategorii liczbę haseł i lekcji;
      przy krótkiej historii mówi „tempa jeszcze nie da się policzyć" zamiast zgadywać
- [ ] **[W]** w kategoriach z sufitem poniżej 95% widać zdanie o wyrazach spoza bazy
- [ ] **[W]** „Czego się uczyć" pokazuje hasła od najczęstszego i pozwala dodać je do powtórek
- [ ] **[W]** cel dnia w *Ustawieniach* jest w minutach; zmiana od razu widać na *Dzisiaj*
- [ ] **[W]** cel tygodnia da się ustawić z mapy drogi i z ustawień
- [ ] **[W]** powiadomienia: przełącznik pyta o zgodę przeglądarki, a przy odmowie
      mówi, że blokada jest po stronie przeglądarki
- [ ] **[W]** ekran *Tydzień* pokazuje **jedną** rekomendację z przyciskiem akcji
- [ ] **[D]** przy pustej historii *Tydzień* mówi „za tydzień będzie co porównywać",
      a nie pokazuje zer

### Reszta
- [ ] **[W]** cztery tryby quizu słuchania: wybór, dyktando, układanie, wyłapywanie
- [ ] **[W]** powtórki SRS: karta się pojawia, ocena zapisuje się i przeżywa odświeżenie strony
- [ ] **[W]** eksport postępu pobiera plik, import go przywraca
- [ ] **[W]** przełączanie motywu jasny/ciemny/automatyczny
- [ ] **[D]** nawigacja samą klawiaturą: Tab przechodzi po elementach, Escape zamyka arkusz
- [ ] **[D]** powiększenie strony do 200% nie rozwala układu

---

## Android (Chrome)

### Instalacja i offline
- [ ] **[K]** otwarcie adresu w Chrome → menu ⋮ → **Zainstaluj aplikację** / *Dodaj do ekranu głównego*
- [ ] **[K]** ikona na ekranie głównym, aplikacja otwiera się bez paska adresu
- [ ] **[K]** przejrzenie materiału przy zasięgu → tryb samolotowy → aplikacja działa
      z pełną bazą 10 200 haseł
- [ ] **[W]** po aktualizacji na serwerze druga wizyta pokazuje nową wersję danych

### Układ
- [ ] **[K]** brak poziomego przewijania na żadnym ekranie
- [ ] **[K]** dolny pasek nawigacji nie zasłania treści i nie chowa się pod paskiem systemowym
- [ ] **[W]** wszystkie przyciski da się trafić kciukiem (nic mniejszego niż ~44 px)
- [ ] **[W]** obrót ekranu do poziomu nie psuje układu
- [ ] **[W]** wysuwana klawiatura nie zasłania pola wyszukiwania

### Dźwięk i mikrofon
- [ ] **[K]** synteza mowy działa (Android ma zwykle Google TTS z tajskim w komplecie;
      jeśli nie — *Ustawienia → Ułatwienia dostępu → Zamiana tekstu na mowę*)
- [ ] **[W]** dźwięk działa po zablokowaniu i odblokowaniu ekranu
- [ ] **[W]** nagrywanie głosu — Chrome pyta o mikrofon, nagranie da się odsłuchać
- [ ] **[D]** przy podłączonych słuchawkach Bluetooth dźwięk idzie do nich

---

## iPhone (Safari)

To jest system, na którym najczęściej coś nie działa — przejdź listę uważnie.

### Instalacja
- [ ] **[K]** Safari → przycisk *Udostępnij* → **Dodaj do ekranu początkowego**
      (szczegóły: `docs/instalacja-iphone.md`)
- [ ] **[K]** aplikacja otwiera się na pełnym ekranie, bez paska adresu Safari
- [ ] **[K]** ikona na ekranie początkowym wygląda poprawnie (nie jest zrzutem strony)

### Układ i safe-area
- [ ] **[K]** treść nie chowa się pod wcięciem ekranu (notch / Dynamic Island) u góry
- [ ] **[K]** dolny pasek nawigacji nie chowa się pod paskiem gestu przewijania
- [ ] **[K]** brak poziomego przewijania — sprawdź szczególnie ekrany *Dialogi* i *Wymowa*
- [ ] **[W]** działa bez najeżdżania kursorem — wszystko, co potrzebne, jest dostępne
      po dotknięciu (nie ma funkcji ukrytych pod `:hover`)
- [ ] **[W]** obrót do poziomu i z powrotem
- [ ] **[D]** tryb ciemny systemu przełącza motyw, gdy ustawienie jest na „automatyczny”

### Dźwięk — najważniejsza część
- [ ] **[K]** **pierwsze** dotknięcie ekranu odblokowuje syntezę mowy; sprawdź, czy przycisk
      odtwarzania działa od razu przy pierwszym użyciu, a nie dopiero za drugim razem
- [ ] **[K]** jeśli w systemie nie ma głosu tajskiego, aplikacja pokazuje komunikat
      z instrukcją, a nie milczy
- [ ] **[W]** instalacja głosu: *Ustawienia → Dostępność → Treść mówiona → Głosy → Tajski*,
      potem ponowne uruchomienie aplikacji — wymowa zaczyna działać
- [ ] **[W]** przełącznik dzwonka/ciszy na boku telefonu: sprawdź, czy dźwięk idzie mimo
      trybu cichego (na iOS synteza mowy zwykle idzie, ale warto to zobaczyć)
- [ ] **[W]** przerwanie odtwarzania przez dotknięcie innego przycisku
- [ ] **[D]** odtwarzanie po powrocie z innej aplikacji

### Nagrywanie
- [ ] **[K]** tylko przez `https` (GitHub Pages) — Safari pyta o mikrofon
- [ ] **[W]** po nagraniu przycisk „Odsłuchaj nagranie” odtwarza głos
- [ ] **[W]** odmowa dostępu do mikrofonu daje czytelny komunikat, a nie zawieszenie

### Offline i trwałość
- [ ] **[K]** przejrzenie materiału przy zasięgu → tryb samolotowy → aplikacja działa
- [ ] **[K]** postęp nauki przeżywa zamknięcie i ponowne otwarcie aplikacji
- [ ] **[W]** postęp przeżywa restart telefonu
- [ ] **[D]** iOS potrafi skasować dane stron nieużywanych przez 7 dni — jeśli aplikacja
      jest **zainstalowana na ekranie początkowym**, ten limit jej nie dotyczy; warto
      mimo to raz na jakiś czas zrobić eksport postępu

---

## Co zrobić, gdy coś nie działa

| Objaw | Pierwsze co sprawdzić |
|---|---|
| Pusta lista haseł | konsola przeglądarki; czy stopka pokazuje „nie wczytano N pliku(ów)” |
| Cisza zamiast wymowy | `docs/ograniczenia-tts.md` — najczęściej brak głosu tajskiego w systemie |
| Stara wersja danych po aktualizacji | podniesiona `VERSION` w `service-worker.js`, potem dwa razy odświeżyć |
| Nagrywanie wyłączone | czy adres jest `https` albo `localhost` — `file://` i zwykłe `http` nie wystarczą |
| Aplikacja nie instaluje się | czy `manifest.webmanifest` się wczytuje i czy adres jest `https` |
