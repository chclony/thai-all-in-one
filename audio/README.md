# Nagrania lektorskie

Ten katalog jest miejscem na nagrania audio. Aplikacja **działa bez nich** — gdy pliku
nie ma, wymowę odtwarza syntezator mowy systemu (SpeechSynthesis) na podstawie ukrytego
pola technicznego `ttsThai`.

## Jak działa odtwarzanie

Każde naciśnięcie „Posłuchaj” przechodzi przez trzy etapy:

1. **Nagranie lektora** — jeśli rekord ma wypełnione pole `audioFile`, aplikacja odtwarza
   plik z tego katalogu (`audio/<nazwa pliku>`).
2. **Synteza mowy** — gdy pola `audioFile` nie ma lub plik się nie wczyta, tekst trafia do
   systemowego głosu tajskiego.
3. **Komunikat** — gdy w systemie nie ma głosu tajskiego, użytkownik dostaje informację,
   jak go zainstalować.

## Co nagranie odblokowuje (sesja L)

Nagranie to jedyny materiał, który przechodzi przez **pełny tor przetwarzania**
Web Audio. Syntezator swojego wyjścia nie udostępnia (powód:
`docs/ograniczenia-tts.md`), więc dopiero plik w tym katalogu włącza:

| Funkcja | Bez nagrania (syntezator) | Z nagraniem |
|---|---|---|
| tempo 0,7× / 1,4× | pauzy między wyrazami, ograniczony `rate` | **WSOLA** — rozciąganie w czasie bez zmiany wysokości |
| pogłos pomieszczenia | tylko na tle | **na głosie** |
| pasmo telefoniczne 300–3400 Hz | niedostępne | **działa** |
| szum tła | działa | działa |

Kod tego toru jest napisany i przetestowany — czeka wyłącznie na pliki.

**Uwaga o trybie `file://`:** przeglądarka blokuje tam `fetch()` na plikach z dysku,
więc nagranie zagra, ale **bez przetwarzania** (zwykły element `<audio>`).
Pełny tor wymaga serwera — choćby `python3 -m http.server`.

## Jak dodać własne nagrania

1. Wgraj plik do tego katalogu, np. `srv-basic-0001.mp3`.
2. W odpowiednim rekordzie w `data/*.json` wpisz nazwę pliku w polu `audioFile`:
   `"audioFile": "srv-basic-0001.mp3"`.
3. Przykłady zdaniowe mają własne pole `audioFile` wewnątrz tablicy `examples`,
   a kwestie dialogów — wewnątrz tablicy `lines`.
4. Uruchom walidator: `python3 tools/validate.py`.

## Zalecenia techniczne

- Format: MP3 (128 kbit/s) lub M4A — oba działają w Safari, Chrome i Firefox.
- Jeden plik = jedno hasło lub jedna kwestia dialogu.
- Nazwa pliku = identyfikator rekordu (`id`), dzięki temu łatwo je masowo podpiąć.
- Cisza na początku i końcu: maksymalnie 0,2 s.
- Głośność znormalizowana do ok. −16 LUFS, żeby nagrania nie różniły się poziomem.

## Uwaga o prawach

Nie wgrywaj tu nagrań pobranych z serwisów słownikowych ani kursów komercyjnych.
Używaj wyłącznie nagrań własnych lub takich, do których masz wyraźną licencję.
