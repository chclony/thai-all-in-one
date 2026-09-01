#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pokrycie rozumienia — korpus kategorii sytuacyjnych rozpisany na wyrazy.

PO CO TO JEST
=============
Do sesji P aplikacja mierzyła postęp liczbą poznanych haseł („poznanych
haseł: 412”). Ta liczba nie odpowiada na jedyne pytanie, które uczący się
naprawdę zadaje: „czy zrozumiem, co się do mnie mówi w restauracji?”.
Czterysta haseł z kategorii „Cechy i opinie” nie pomoże zamówić obiadu,
a czterdzieści właściwych haseł z kategorii „Restauracja” — pomoże.

Ten generator buduje dane, na których aplikacja liczy miarę odpowiadającą
na tamto pytanie: ile procent wyrazów w faktycznym materiale danej kategorii
uczący się zna.

CO DOKŁADNIE LICZYMY
====================
Korpus kategorii to WSZYSTKIE kwestie dialogów przypisanych do tej kategorii —
prawdziwe zdania, które aplikacja odtwarza uczącemu się, a nie wyciąg
z listy haseł. Każdą kwestię rozbijamy na wyrazy (spacja dzieli, dywiz nie:
„sawàt-dii” to jeden wyraz) i każdemu wyrazowi próbujemy przypisać hasło
ze słownika.

Dopasowanie idzie zachłannie od najdłuższego: najpierw trzy wyrazy, potem
dwa, potem jeden — inaczej utrwalony zwrot „khǎw-thôot khráp” rozpadłby się
na części, z których każda znaczy co innego. Porównujemy zapis złożony:
bez tonów, bez dywizów, małymi literami (fold() z comprehension_lib), bo ton
bywa zapisany różnie w haśle i w kwestii, a dywiz jest decyzją redakcyjną.

DWA KLUCZE, NIE JEDEN
---------------------
Klucz ścisły to sam fold(). Klucz luźny dodatkowo skraca podwojone samogłoski
(„taae” → „tae”, „dooen” → „doen”). Jest potrzebny, bo ta sama jednostka bywa
w bazie zapisana raz tak, raz inaczej: kwestia dialogu ma „tàae”, a hasło
słownika „tàe”. To jest niespójność naszego zapisu, nie różnica w tajskim —
i bez klucza luźnego kosztowała 229 wystąpień uznanych za „spoza bazy”.

Klucz luźny działa wyłącznie jako zapas po nietrafionym kluczu ścisłym i tylko
wtedy, gdy prowadzi do DOKŁADNIE JEDNEGO hasła. Długość samogłoski jest
w tajskim znacząca („khǎaw” ryż kontra „khǎw” on), więc gdzie luźny klucz
zbiera kilka haseł, dopasowanie odpada — wolimy policzyć wyraz jako
nieprzypisany niż zaliczyć uczącemu się znajomość innego słowa.

Wynik dla każdej kwestii to lista pozycji o długości równej liczbie wyrazów.
Na pozycji stoi numer hasła w tabeli kategorii albo -1, jeśli wyraz nie ma
odpowiednika w bazie. Hasło wielowyrazowe zajmuje tyle pozycji, ile ma
wyrazów — dzięki temu suma pozycji jest liczbą wystąpień wyrazów i nic się
nie gubi ani nie dubluje.

CZEGO TU NIE MA I DLACZEGO
==========================
1. NIE MA KONTROLI SENSU. Generator luk (comprehension.py) odrzuca
   dopasowanie, którego znaczenia nie widać w polskim tłumaczeniu kwestii —
   tam błąd byłby podaniem uczącemu się nieprawdy jako poprawnej odpowiedzi.
   Tutaj cena jest odwrotna: kontrola sensu jest ostra i odrzuca też trafne
   dopasowania (tłumaczenia bywają swobodne), a każde odrzucone dopasowanie
   zaniżałoby pokrycie o wyraz, który uczący się naprawdę zna. Zamiast tego
   liczymy, ile wystąpień jest niejednoznacznych fonetycznie (kilka haseł
   o różnym znaczeniu i tym samym zapisie złożonym) i podajemy tę liczbę
   w interfejsie jako ograniczenie metody.

2. NIE MA WAG CZĘSTOŚCI. Wystąpienie liczy się raz, niezależnie od tego, czy
   to „khráp”, czy rzadki rzeczownik. Korpus sam waży: wyraz częsty pojawia
   się w nim wiele razy i wiele razy wpada do mianownika.

3. NIE MA MATERIAŁU SPOZA DIALOGÓW. Przykłady przy hasłach są generowane
   szablonowo („Mam grzmota.”) i nie są mową — wciągnięcie ich do korpusu
   zawyżałoby pokrycie, bo w przykładzie hasła X zawsze występuje hasło X.

WYNIK
=====
data/coverage.json — tabela haseł i rozpisane kwestie dla każdej kategorii,
która ma materiał dialogowy. Aplikacja (js/coverage.js) czyta to i liczy
pokrycie względem tego, co uczący się faktycznie opanował.
"""

import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import comprehension_lib as CL  # noqa: E402
from jsonio import dump as write_json  # noqa: E402

ROOT = CL.ROOT
DATA = CL.DATA

# Ile kwestii musi mieć kategoria, żeby liczba miała sens. Poniżej tego progu
# pokrycie liczone z kilku zdań jest przypadkiem, nie pomiarem — kategoria
# trafia do danych ze znacznikiem `thin`, a ekran mówi o tym wprost.
MIN_LINES = 40

# Próg, przy którym uznajemy kwestię za zrozumiałą: uczący się zna co najmniej
# tyle procent jej wyrazów. Wartość wzięta z badań nad pokryciem leksykalnym
# a rozumieniem (Hu i Nation 2000 dla czytania, van Zeeland i Schmitt 2013 dla
# słuchania) — przy 95% pokrycia rozumienie przekazu jest zwykle osiągalne,
# przy 80% zwykle nie. Trzymamy tę wartość w danych, a nie w kodzie ekranu,
# żeby raport i aplikacja liczyły to samo.
LINE_THRESHOLD = 0.95

# Docelowy próg pokrycia dla kategorii — to jest „cel” z mapy drogi.
TARGET = 0.95


def loose_key(key):
    """Klucz luźny: podwojona samogłoska skraca się do jednej."""
    return re.sub(r"([aeiou\u0259])\1+", r"\1", key)


class Matcher(object):
    """Dopasowanie wyrazów kwestii do haseł — wspólne dla każdej długości.

    CL.Lexicon trzyma hasła jednowyrazowe i wielowyrazowe w osobnych mapach,
    co gubi przypadek graniczny: „mûea rài” jest w słowniku dwoma wyrazami,
    a w kwestii dialogu stoi jako jeden wyraz „mûea-rài”. Tutaj klucz jest
    jeden — zapis złożony całego fragmentu — więc liczba wyrazów po obu
    stronach przestaje mieć znaczenie.
    """

    def __init__(self, records):
        self.strict = {}
        self.by_loose = collections.defaultdict(set)
        for r in records:
            key = CL.fold(r["thaiPhonetic"])
            if not key:
                continue
            best = self.strict.get(key)
            if best is None or self._better(r, best):
                self.strict[key] = r
        for key in self.strict:
            self.by_loose[loose_key(key)].add(key)

    @staticmethod
    def _better(a, b):
        if a.get("frequency", 0) != b.get("frequency", 0):
            return a.get("frequency", 0) > b.get("frequency", 0)
        return a.get("difficulty", 9) < b.get("difficulty", 9)

    def span(self, ws, start, length):
        """Zwraca (hasło, 'strict'|'loose') albo (None, None)."""
        key = CL.fold("".join(ws[start:start + length]))
        if not key:
            return None, None
        hit = self.strict.get(key)
        if hit is not None:
            return hit, "strict"
        candidates = self.by_loose.get(loose_key(key))
        if candidates and len(candidates) == 1:
            return self.strict[next(iter(candidates))], "loose"
        return None, None


def build():
    records = CL.load_records()
    dialogues = CL.load_dialogues()
    lex = Matcher(records)

    # Niejednoznaczność fonetyczna: ile haseł o RÓŻNYM znaczeniu ma ten sam
    # zapis złożony. To jest sufit dokładności dopasowania — potrzebny do
    # uczciwego opisu metody, nie do samego liczenia.
    homophones = collections.defaultdict(set)
    for r in records:
        if len(CL.words(r["thaiPhonetic"])) != 1:
            continue
        key = CL.fold(r["thaiPhonetic"])
        if key:
            homophones[key].add(r["polish"].strip().lower())

    by_cat = collections.defaultdict(list)
    for d in dialogues:
        by_cat[d.get("category") or "—"].append(d)

    cats = []
    for name in sorted(by_cat):
        dlgs = by_cat[name]
        ids = []            # tabela haseł tej kategorii
        id_pos = {}
        lines = []
        occurrences = 0
        mapped = 0
        ambiguous = 0
        loose_hits = 0
        unmapped_counter = collections.Counter()

        for dlg in dlgs:
            for line in dlg.get("lines", []):
                ws = CL.words(line.get("thaiPhonetic", ""))
                if not ws:
                    continue
                slots = [-1] * len(ws)
                i = 0
                while i < len(ws):
                    hit = None
                    for length in (3, 2, 1):
                        if i + length > len(ws):
                            continue
                        rec, how = lex.span(ws, i, length)
                        if rec is not None:
                            hit = (rec, length, how)
                            break
                    if hit is None:
                        unmapped_counter[CL.fold(ws[i])] += 1
                        i += 1
                        continue
                    rec, length, how = hit
                    if how == "loose":
                        loose_hits += 1
                    rid = rec["id"]
                    if rid not in id_pos:
                        id_pos[rid] = len(ids)
                        ids.append(rid)
                    for k in range(length):
                        slots[i + k] = id_pos[rid]
                    if length == 1 and len(homophones.get(CL.fold(ws[i]), ())) > 1:
                        ambiguous += 1
                    i += length

                occurrences += len(slots)
                mapped += sum(1 for s in slots if s >= 0)
                lines.append({"d": dlg["id"], "l": line.get("index"), "s": slots})

        # Ile razy każde hasło pada w korpusie kategorii — po tym ekran mapy
        # drogi ustawia kolejność nauki: hasło padające dwadzieścia razy
        # podnosi pokrycie dwadzieścia razy mocniej niż padające raz.
        weight = collections.Counter()
        for ln in lines:
            for s in ln["s"]:
                if s >= 0:
                    weight[s] += 1

        cats.append({
            "name": name,
            "dialogues": len(dlgs),
            "lines": len(lines),
            "occurrences": occurrences,
            "mapped": mapped,
            "unmapped": occurrences - mapped,
            "ambiguous": ambiguous,
            "loose": loose_hits,
            "items": len(ids),
            "thin": len(lines) < MIN_LINES,
            "ids": ids,
            "weights": [weight.get(i, 0) for i in range(len(ids))],
            "l": lines,
            "unmappedTop": [{"w": w, "n": n} for w, n in unmapped_counter.most_common(12)],
        })

    total_occ = sum(c["occurrences"] for c in cats)
    total_mapped = sum(c["mapped"] for c in cats)
    total_amb = sum(c["ambiguous"] for c in cats)
    total_loose = sum(c["loose"] for c in cats)

    out = {
        "file": "coverage.json",
        "generator": "tools/generators/coverage.py",
        "method": {
            "corpus": "kwestie dialogów przypisanych do kategorii",
            "unit": "wystąpienie wyrazu (spacja dzieli, dywiz nie)",
            "match": "zapis złożony bez tonów i dywizów, dopasowanie zachłanne 3→2→1 wyrazy",
            "looseFallback": "przy nietrafieniu klucz ze skróconą podwojoną samogłoską, tylko gdy prowadzi do jednego hasła",
            "known": "hasło z opanowaną kartą rozpoznania w powtórkach",
            "lineThreshold": LINE_THRESHOLD,
            "target": TARGET,
            "minLines": MIN_LINES,
            "senseCheck": False,
        },
        "totals": {
            "categories": len(cats),
            "dialogues": sum(c["dialogues"] for c in cats),
            "lines": sum(c["lines"] for c in cats),
            "occurrences": total_occ,
            "mapped": total_mapped,
            "unmapped": total_occ - total_mapped,
            "ambiguous": total_amb,
            "loose": total_loose,
        },
        "categories": cats,
    }
    return out


def register(out):
    """Wpis w manifeście. Robi to generator, a nie człowiek — inaczej opis
    pliku i sam plik rozjeżdżają się przy pierwszej przebudowie.

    Plik jest oznaczony jako `lazy`: aplikacja dociąga go dopiero przy wejściu
    na ekran, który go potrzebuje. Waży dwieście kilobajtów, a ekran „Dzisiaj”
    otwiera się bez niego."""
    path = os.path.join(DATA, "manifest.json")
    with open(path, encoding="utf-8") as fh:
        man = json.load(fh)
    t = out["totals"]
    entry = {
        "file": "coverage.json",
        "kind": "coverage",
        "count": t["categories"],
        "lines": t["lines"],
        "occurrences": t["occurrences"],
        "mapped": t["mapped"],
        "lazy": True,
    }
    files = man.setdefault("supportFiles", [])
    for i, e in enumerate(files):
        if e.get("file") == "coverage.json":
            files[i] = entry
            break
    else:
        files.append(entry)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(man, fh, ensure_ascii=False, indent=1)


def main():
    out = build()
    path = os.path.join(DATA, "coverage.json")
    write_json(out, path)
    register(out)
    t = out["totals"]
    print("coverage.json — %d kategorii, %d kwestii, %d wystąpień wyrazów"
          % (t["categories"], t["lines"], t["occurrences"]))
    print("  przypisanych do haseł  %6d (%.1f%%)"
          % (t["mapped"], 100.0 * t["mapped"] / max(1, t["occurrences"])))
    print("  nieprzypisanych        %6d (%.1f%%)"
          % (t["unmapped"], 100.0 * t["unmapped"] / max(1, t["occurrences"])))
    print("  niejednoznacznych      %6d (%.1f%%)"
          % (t["ambiguous"], 100.0 * t["ambiguous"] / max(1, t["occurrences"])))
    print("  przez klucz luźny      %6d (%.1f%%)"
          % (t["loose"], 100.0 * t["loose"] / max(1, t["occurrences"])))
    print("-" * 66)
    for c in out["categories"]:
        flag = "  (mało materiału)" if c["thin"] else ""
        print("  %-24s %4d kwestii · %5d wyrazów · sufit %5.1f%%%s"
              % (c["name"][:24], c["lines"], c["occurrences"],
                 100.0 * c["mapped"] / max(1, c["occurrences"]), flag))
    print("Zapisano %s (%.1f KB)" % (path, os.path.getsize(path) / 1024.0))


if __name__ == "__main__":
    main()
