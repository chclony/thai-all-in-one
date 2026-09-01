#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wspólne narzędzia dla generatorów rozumienia (sceny, luki, słowa nieznane).

Trzy rzeczy, których potrzebują oba generatory:

1. WCZYTANIE BAZY — hasła słownikowe i dialogi, zawsze z manifestu, nigdy
   z listy plików wpisanej na sztywno.

2. DOPASOWANIE WYRAZÓW — kwestia dialogu to ciąg wyrazów rozdzielonych spacją
   (sylaby wewnątrz wyrazu łączy dywiz: „sawàt-dii” to jeden wyraz, nie dwa).
   Chcemy wiedzieć, które z tych wyrazów mają odpowiednik w słowniku — bo tylko
   o takim wyrazie umiemy powiedzieć uczącemu się cokolwiek sensownego:
   co znaczy, jak częsty jest, do jakiej kategorii należy.

   Dopasowanie idzie po zapisie „złożonym”: bez tonów, bez dywizów, małymi
   literami. Ton bywa zapisany różnie w haśle i w kwestii, a dywiz jest
   decyzją redakcyjną, nie fonetyczną — oba musiałyby psuć trafienia.

3. MODEL CZASU TRWANIA — ile sekund zajmie odsłuchanie danego materiału.
   Nie mamy tu syntezatora, więc czas jest szacowany: liczba sylab razy czas
   sylaby plus przerwa między kwestiami. Wartości poniżej wzięły się z pomiaru
   ścieżki odtwarzania w tools/bench-audio.py i z przerwy 450 ms, którą
   Player.playSequence wstawia między kwestiami. Wynik jest oznaczony w danych
   jako „estSeconds” — szacunek, nie pomiar.
"""

import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")

# --- model czasu ------------------------------------------------------------
# Sylaba tajska w tempie naturalnym syntezatora: ok. 0,30 s.
SEC_PER_SYLLABLE = 0.30
# Przerwa między kwestiami — dokładnie ta, którą wstawia Player.playSequence.
GAP_BETWEEN_LINES = 0.45
# Mnożniki temp z js/audio.js. Trzymamy je tutaj, żeby raport i aplikacja
# liczyły minuty tak samo.
TEMPO_FACTORS = {"slow": 0.7, "natural": 1.0, "fast": 1.4}


def fold(text):
    """Zapis złożony: bez tonów, bez dywizów, bez spacji, małymi literami."""
    d = unicodedata.normalize("NFD", text or "")
    d = "".join(c for c in d if not unicodedata.combining(c))
    return re.sub(r"[^a-z]", "", d.lower())


def words(phonetic):
    """Wyrazy kwestii. Dywiz łączy sylaby w obrębie wyrazu i nie dzieli."""
    return [w for w in re.split(r"\s+", (phonetic or "").strip()) if w]


def syllable_count(phonetic):
    return len([s for s in re.split(r"[\s\-]+", (phonetic or "").strip()) if s])


def line_seconds(phonetic, tempo="natural"):
    factor = TEMPO_FACTORS.get(tempo, 1.0)
    speech = syllable_count(phonetic) * SEC_PER_SYLLABLE / factor
    return speech + GAP_BETWEEN_LINES


def lines_seconds(phonetics, tempo="natural"):
    return sum(line_seconds(p, tempo) for p in phonetics)


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def load_manifest():
    return load("manifest.json")


def load_records():
    """Wszystkie hasła słownikowe, w kolejności z manifestu."""
    mf = load_manifest()
    out = []
    for entry in mf["dataFiles"]:
        if entry["kind"] == "vocabulary":
            out += load(entry["file"])["records"]
    return out


def load_dialogues():
    """Wszystkie dialogi wraz z nazwą pliku źródłowego."""
    mf = load_manifest()
    out = []
    for entry in mf["dataFiles"]:
        if entry["kind"] == "dialogues":
            for d in load(entry["file"])["records"]:
                d = dict(d)
                d["__file"] = entry["file"]
                out.append(d)
    return out


class Lexicon(object):
    """Słownik ułożony pod wyszukiwanie po zapisie złożonym.

    Jedno hasło na klucz — gdy kilka haseł ma ten sam zapis, wygrywa
    najczęstsze, a przy remisie najłatwiejsze. Chodzi o to, żeby wyraz
    „náam” w kwestii dialogu prowadził do hasła „woda”, a nie do rzadkiego
    homofonu, którego uczący się nigdy nie widział.
    """

    def __init__(self, records):
        self.records = records
        self.by_id = {r["id"]: r for r in records}
        self.single = {}
        for r in records:
            if len(words(r["thaiPhonetic"])) != 1:
                continue
            key = fold(r["thaiPhonetic"])
            if not key:
                continue
            best = self.single.get(key)
            if best is None or self._better(r, best):
                self.single[key] = r

        # Hasła wielowyrazowe do dopasowania dłuższych fragmentów — przydają
        # się przy słowach kluczowych sceny („khǎw-thôot khráp” to jedna
        # jednostka znaczeniowa, nie dwie).
        self.multi = {}
        for r in records:
            n = len(words(r["thaiPhonetic"]))
            if not 2 <= n <= 3:
                continue
            key = fold(r["thaiPhonetic"])
            if not key:
                continue
            best = self.multi.get(key)
            if best is None or self._better(r, best):
                self.multi[key] = r

    @staticmethod
    def _better(a, b):
        if a.get("frequency", 0) != b.get("frequency", 0):
            return a.get("frequency", 0) > b.get("frequency", 0)
        return a.get("difficulty", 9) < b.get("difficulty", 9)

    def word(self, w):
        """Hasło dla pojedynczego wyrazu albo None."""
        return self.single.get(fold(w))

    def span(self, ws, start, length):
        """Hasło dla ciągu wyrazów ws[start:start+length] albo None."""
        if length == 1:
            return self.single.get(fold(ws[start]))
        return self.multi.get(fold("".join(ws[start:start + length])))

    def annotate(self, phonetic):
        """Lista pozycji wyrazów z dopasowanym hasłem.

        Zwraca [{'w': indeks, 'word': zapis, 'rec': hasło albo None}].
        """
        ws = words(phonetic)
        return [{"w": i, "word": w, "rec": self.word(w)} for i, w in enumerate(ws)]

    def keywords(self, phonetics, limit=12, skip=(), translations=None):
        """Słowa kluczowe dla zbioru kwestii.

        Najpierw próbujemy dłuższych dopasowań (trzy wyrazy, potem dwa, potem
        jeden) — inaczej utrwalony zwrot rozpadłby się na wyrazy, z których
        każdy z osobna znaczy coś innego. Ranking: ile razy padło, a przy
        remisie — jak rzadkie jest hasło (rzadsze niesie więcej treści).
        """
        counts = {}
        beats = {}
        # translations[i] = polskie tłumaczenie i-tej kwestii. Bez niego nie
        # da się sprawdzić, czy dopasowane hasło znaczy w tym zdaniu to,
        # co twierdzi słownik.
        for pos, (beat_index, phon) in enumerate(phonetics):
            line_pl = translations[pos] if translations else None
            ws = words(phon)
            i = 0
            while i < len(ws):
                hit = None
                for length in (3, 2, 1):
                    if i + length > len(ws):
                        continue
                    rec = self.span(ws, i, length)
                    if rec is not None:
                        hit = (rec, length)
                        break
                if hit is None:
                    i += 1
                    continue
                rec, length = hit
                rid = rec["id"]
                if translations is not None and not sense_matches(rec["polish"], line_pl):
                    i += length
                    continue
                if fold(rec["thaiPhonetic"]) not in skip:
                    counts[rid] = counts.get(rid, 0) + 1
                    beats.setdefault(rid, set()).add(beat_index)
                i += length

        ranked = sorted(
            counts.items(),
            key=lambda kv: (-kv[1], self.by_id[kv[0]].get("frequency", 3), kv[0]),
        )
        out = []
        for rid, n in ranked[:limit]:
            rec = self.by_id[rid]
            out.append({
                "id": rid,
                "polish": rec["polish"],
                "thaiPhonetic": rec["thaiPhonetic"],
                "count": n,
                "beats": sorted(beats[rid]),
            })
        return out


# --- kontrola sensu ---------------------------------------------------------
# Zapis fonetyczny nie wystarcza do ustalenia znaczenia. „kòt” to i „zasada”,
# i „uciskać”; „sài” to i „rozmiar”, i „wkładać”. Dopasowanie po samym zapisie
# wybrałoby jedno z nich na chybił trafił i podałoby uczącemu się błędne
# znaczenie jako poprawną odpowiedź.
#
# Rozstrzygamy to tłumaczeniem kwestii, które w bazie już jest. Jeżeli rdzeń
# polskiego znaczenia hasła pojawia się w polskim tłumaczeniu zdania, sens się
# zgadza. Jeżeli nie — hasło odpada. Kryterium jest ostre i odrzuca też część
# trafnych dopasowań (tłumaczenie bywa swobodne), ale w tę stronę błąd jest
# tani: tracimy ćwiczenie. W drugą stronę byłby to błąd merytoryczny podany
# uczącemu się jako prawda.

POLISH_STOPWORDS = {
    "sie", "nie", "tak", "jest", "byc", "ktos", "cos", "ten", "ta", "to",
    "do", "na", "za", "od", "po", "we", "ze", "przez", "albo", "lub", "i",
}


def pl_fold(text):
    table = str.maketrans("ąćęłńóśźż", "acelnoszz")
    return (text or "").lower().translate(table)


def stems(polish):
    """Rdzenie znaczenia hasła — do szukania w tłumaczeniu zdania.

    Bierzemy wyrazy z pola polish (bez nawiasów, bez wyrazów funkcyjnych)
    i skracamy je o końcówkę fleksyjną: „stacja” -> „stacj”, więc trafi
    zarówno w „stację”, jak i w „stacji”.
    """
    text = re.sub(r"\([^)]*\)", " ", polish or "")
    text = re.sub(r"[/,;]", " ", text)
    out = []
    for word in pl_fold(text).split():
        word = re.sub(r"[^a-z]", "", word)
        if len(word) < 3 or word in POLISH_STOPWORDS:
            continue
        out.append(word[:max(3, min(6, len(word) - 1))])
    return out


def sense_matches(rec_polish, line_polish):
    """Czy znaczenie hasła daje się odnaleźć w tłumaczeniu kwestii."""
    hay = pl_fold(line_polish or "")
    hay = re.sub(r"[^a-z ]", " ", hay)
    found = stems(rec_polish)
    if not found:
        return False
    return any(stem in hay for stem in found)


# Wyrazy funkcyjne i końcówki grzecznościowe. Nie nadają się ani na lukę
# (uczący się wstawi je odruchowo, nie ze zrozumienia), ani na słowo kluczowe
# sceny, ani na słowo „nieznane” — są w każdym zdaniu.
FUNCTION_WORDS = {
    fold(w) for w in [
        "khráp", "khâ", "khá", "khà", "kháp", "ná", "sí", "nà",
        "mǎi", "mái", "châi", "mâi", "mâi-dâi", "dâi", "kôo", "kô",
        "lɛ́ɛo", "yù", "yùu", "wâa", "thîi", "níi", "nîi", "nân", "nán",
        "à", "eh", "ooh", "ə́ə", "kráp", "hâ", "há",
    ]
}
