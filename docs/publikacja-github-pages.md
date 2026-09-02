# Checklista publikacji na GitHub Pages

Aplikacja jest zbiorem plików statycznych — nie ma budowania, nie ma zależności,
nie ma kroku kompilacji. Publikacja sprowadza się do wrzucenia katalogu do repozytorium
i włączenia Pages.

Nazwa repozytorium może być dowolna. Wszystkie ścieżki w kodzie są **względne**
(`./index.html`, `data/…`, `css/style.css`), a `manifest.webmanifest` ma
`"start_url": "./index.html"` i `"scope": "./"`, więc aplikacja działa tak samo pod
`https://uzytkownik.github.io/` jak i pod `https://uzytkownik.github.io/dowolna-nazwa/`.

---

## Przed wysłaniem

- [ ] `python3 tools/build-offline-data.py` — odświeżenie kopii `data/*.js` dla trybu `file://`
- [ ] `python3 tools/validate.py` — musi zakończyć się komunikatem **BAZA POPRAWNA** (0 błędów)
- [ ] `python3 tools/audit-quality.py` — sprawdzenie duplikatów i liczników
- [ ] `node tools/browser-test.js "file://$PWD/index.html" "file" 3` — wszystkie testy zaliczone
- [ ] podniesiona wersja w `service-worker.js` (zmienna `VERSION`), jeśli zmieniałeś cokolwiek
      w powłoce aplikacji lub w danych — bez tego użytkownicy zobaczą starą wersję z cache
- [ ] wersja w `data/manifest.json` i `data/metadata.json` zgadza się z tym, co wysyłasz

## Wysłanie

- [ ] wszystkie pliki w repozytorium, **łącznie z katalogiem `data/`** (to około 31 MB —
      mieści się w limitach GitHuba, ale sprawdź, czy `.gitignore` przypadkiem go nie wycina)
- [ ] w katalogu głównym repozytorium leży `index.html` (nie w podkatalogu)
- [ ] plik `.nojekyll` w katalogu głównym — bez niego Jekyll potrafi zignorować
      pliki i katalogi zaczynające się od podkreślenia

```bash
touch .nojekyll
git add -A
git commit -m "Thai All-in-One"
git push
```

## Włączenie Pages

- [ ] **Settings → Pages → Source: Deploy from a branch**
- [ ] gałąź `main`, katalog `/ (root)`
- [ ] po 1–2 minutach adres pojawia się na tej samej stronie ustawień

## Po opublikowaniu

- [ ] adres otwiera się i pokazuje ekran *Dzisiaj* z hasłem dnia
- [ ] w stopce nawigacji widnieje **10200 haseł · 184 dialogów · wersja danych 1.5.0**
      (bez ostrzeżenia „nie wczytano N pliku(ów)”)
- [ ] słownik pokazuje 10 200 haseł po wejściu na ekran *Słownik*
- [ ] w narzędziach deweloperskich (zakładka Application → Service Workers)
      service worker jest **activated and is running**
- [ ] Application → Cache Storage zawiera `thai-aio-v1.5.0-shell` i `thai-aio-v1.5.0-data`
- [ ] tryb samolotowy albo Network → Offline: aplikacja nadal się otwiera i działa
      (po wcześniejszym przejrzeniu materiału przy zasięgu, żeby dane trafiły do pamięci przeglądarki
      albo po prostu po jednej pełnej wizycie — dane cache'ują się same w trakcie dociągania)
- [ ] instalacja na telefonie działa (patrz `docs/instalacja-iphone.md`)

## Aktualizacja po zmianach

GitHub Pages serwuje pliki z własnym cache CDN, a service worker ma jeszcze swój.
Żeby aktualizacja dotarła do użytkowników:

1. podnieś `VERSION` w `service-worker.js` (np. `thai-aio-v1.5.1`),
2. podnieś `version` i `cacheKey` w `data/manifest.json` (robi to automatycznie skrypt etapu),
3. wypchnij zmiany.

Stare cache są kasowane przy aktywacji nowego service workera — użytkownik dostanie
nową wersję przy drugim otwarciu aplikacji.

## Czego NIE trzeba robić

- nie trzeba konfigurować budowania ani GitHub Actions,
- nie trzeba zmieniać żadnych ścieżek pod nazwę repozytorium,
- nie trzeba serwera Node, PHP ani bazy danych,
- nie trzeba certyfikatu — Pages daje HTTPS, a to wystarcza do PWA i mikrofonu.
