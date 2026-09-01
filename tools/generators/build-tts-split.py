#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wyznacza granice wyrazów w ukrytym polu ttsThai i zapisuje je jako DŁUGOŚCI.

    python3 tools/generators/build-tts-split.py

PO CO
-----
Tempo dydaktyczne 0,7x nie może działać przez utterance.rate — rate rozciąga
kontur tonalny, a w języku tonalnym kontur JEST znaczeniem. Zamiast tego
tniemy wypowiedź na wyrazy i mówimy je osobno, każdy przy rate 1,0,
z pauzą pomiędzy. Kontur każdego wyrazu zostaje dokładnie taki, jaki
wypuszcza silnik; wydłuża się wyłącznie odstęp.

Żeby tak zrobić, trzeba wiedzieć, gdzie w łańcuchu tajskim kończy się wyraz.
Pismo tajskie nie stawia spacji między wyrazami — 91% haseł to jeden ciąg
bez żadnego separatora.

JAK
---
Bazy nie trzeba zgadywać, wystarczy ją przeczytać. Rekordy jednowyrazowe
dają gotowy słownik „fonetyka -> pisownia tajska”. Mając go, próbujemy
zjeść łańcuch tajski wyraz po wyrazie w kolejności wyznaczonej przez zapis
fonetyczny. Podział przyjmujemy TYLKO wtedy, gdy człony zjadły łańcuch
co do znaku — inaczej odrzucamy go w całości. Żadnego dopasowania „na oko”.

Słownik rośnie w kolejnych przebiegach: każdy rozłożony tekst uczy nas
pisowni wyrazów, których wcześniej nie znaliśmy, a te pozwalają rozłożyć
następne teksty. Pętla kręci się do nasycenia.

CO TRAFIA DO DANYCH
-------------------
Wyłącznie tablica liczb, np. "ttsSplit": [9, 6, 4] — tyle znaków ma kolejny
wyraz. Pisma tajskiego nie dokładamy nigdzie: zasada „użytkownik nigdy nie
widzi pisma tajskiego” obowiązuje też generatory, a liczby niczego nie zdradzają.
Walidator sprawdza, że suma długości zgadza się z długością pola ttsThai.
"""

import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jsonio  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")

FILES = ("survival", "a1-part", "a2-part", "b1-part", "b2-part",
         "core-lexicon", "supplemental", "dialogues-part", "grammar")

PUNCT = ".,?!\u2026:;\u201e\u201d\u2018\u2019\"'()"

stats = collections.Counter()


def nodes_of(rec):
    """Wszystkie węzły rekordu, które mają fonetykę i pismo tajskie."""
    out = []

    def walk(node):
        if isinstance(node, list):
            for item in node:
                walk(item)
            return
        if not isinstance(node, dict):
            return
        if node.get("thaiPhonetic"):
            out.append(node)
        for key in ("examples", "lines", "patterns", "genderVariant", "female", "colloquial"):
            if key in node:
                walk(node[key])

    walk(rec)
    return out


def words_of(phonetic):
    return [w.strip(PUNCT) for w in (phonetic or "").split() if w.strip(PUNCT)]


def learn(words, thai, lex):
    """Uczy się napisania JEDNEGO nieznanego wyrazu z częściowego dopasowania.

    Zjadamy łańcuch od lewej, dopóki wyrazy są znane, i od prawej tak samo.
    Jeżeli w środku zostanie dokładnie jeden nieznany wyraz, a łańcuch nie jest
    pusty, to reszta łańcucha jest jego napisaniem — bo nic innego nią być
    nie może. Zwraca (wyraz, napisanie) albo None.

    Warunek „dokładnie jeden” jest tu istotny: przy dwóch nieznanych wyrazach
    nie wiadomo, gdzie przebiega granica między nimi, a zgadywanie zatruwałoby
    słownik i psuło wszystkie następne przebiegi.
    """
    rest = thai.replace(" ", "")
    left, right = 0, len(words) - 1
    while left <= right:
        cand = _match(words[left], rest, lex)
        if cand is None:
            break
        rest = rest[len(cand):]
        left += 1
    while right >= left:
        cand = _match_end(words[right], rest, lex)
        if cand is None:
            break
        rest = rest[:len(rest) - len(cand)]
        right -= 1
    if left == right and rest:
        return words[left], rest
    return None


def _match(word, rest, lex):
    hit = None
    for cand in lex.get(word, ()):
        if rest.startswith(cand) and (hit is None or len(cand) > len(hit)):
            hit = cand
    return hit


def _match_end(word, rest, lex):
    hit = None
    for cand in lex.get(word, ()):
        if rest.endswith(cand) and (hit is None or len(cand) > len(hit)):
            hit = cand
    return hit


def segment(words, thai, lex):
    """Zwraca listę członów tajskich albo None, gdy podział się nie zamyka."""
    rest = thai.replace(" ", "")
    parts = []
    for w in words:
        spellings = lex.get(w)
        if not spellings:
            return None
        # Najdłuższe pasujące napisanie — krótsze bywa przedrostkiem dłuższego.
        hit = None
        for cand in spellings:
            if rest.startswith(cand) and (hit is None or len(cand) > len(hit)):
                hit = cand
        if hit is None:
            return None
        parts.append(hit)
        rest = rest[len(hit):]
    return parts if not rest else None


def main():
    dry = "--dry-run" in sys.argv

    payloads = {}
    for name in sorted(os.listdir(DATA)):
        if not name.endswith(".json"):
            continue
        if not any(name[:-5].startswith(p) for p in FILES):
            continue
        with open(os.path.join(DATA, name), encoding="utf-8") as fh:
            payloads[name] = json.load(fh)

    items = []          # (węzeł, wyrazy fonetyczne, tekst tajski)
    for payload in payloads.values():
        for rec in payload.get("records", []):
            for node in nodes_of(rec):
                thai = (node.get("ttsThai") or "").strip()
                if thai:
                    items.append((node, words_of(node.get("thaiPhonetic")), thai))

    # --- słownik startowy: hasła jednowyrazowe --------------------------------
    counts = collections.defaultdict(collections.Counter)
    for _node, words, thai in items:
        if len(words) == 1 and " " not in thai:
            counts[words[0]][thai] += 1
    lex = {w: sorted(c, key=lambda t: -c[t]) for w, c in counts.items()}
    print("słownik startowy: %d wyrazów" % len(lex))

    # --- pętla nasycenia -----------------------------------------------------
    for round_no in range(1, 13):
        learned = 0
        solved = 0
        for _node, words, thai in items:
            if len(words) < 2:
                continue
            parts = segment(words, thai, lex)
            if parts:
                solved += 1
                continue
            found = learn(words, thai, lex)
            if found:
                word, spelling = found
                bucket = lex.setdefault(word, [])
                if spelling not in bucket:
                    bucket.append(spelling)
                    learned += 1
        print("  przebieg %d: rozłożonych %d, nowych napisań %d" % (round_no, solved, learned))
        if not learned:
            break

    # --- zapis ---------------------------------------------------------------
    total = ok = 0
    for _node, words, thai in items:
        if len(words) < 2:
            continue
        total += 1
    for node, words, thai in items:
        node.pop("ttsSplit", None)
        if len(words) < 2:
            continue
        parts = segment(words, thai, lex)
        if not parts:
            continue
        node["ttsSplit"] = [len(p) for p in parts]
        ok += 1

    if not dry:
        for name, payload in payloads.items():
            jsonio.dump(payload, os.path.join(DATA, name))

    print("=" * 70)
    print("GRANICE WYRAZÓW DLA SYNTEZATORA" + ("  (próba, bez zapisu)" if dry else ""))
    print("=" * 70)
    print("słownik końcowy:            %d wyrazów" % len(lex))
    print("tekstów wielowyrazowych:    %d" % total)
    print("z wyznaczonymi granicami:   %d  (%.1f%%)" % (ok, 100.0 * ok / max(1, total)))
    print("Pamiętaj o: python3 tools/build-offline-data.py && python3 tools/validate.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
