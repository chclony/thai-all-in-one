#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator ćwiczeń rozumienia — data/comprehension.json.

Dwa ćwiczenia, oba na kwestiach z dialogów. Plik trzyma wyłącznie adnotacje:
identyfikator dialogu, numer kwestii i numer wyrazu. Treść kwestii zostaje
tam, gdzie była — w plikach dialogów. Dzięki temu ten plik waży kilkadziesiąt
kilobajtów zamiast kilku megabajtów i nie może się rozjechać z oryginałem.

LUKI NA SŁUCH (gapItems)

Uczący się słyszy całe zdanie i uzupełnia jeden brakujący wyraz. Luka nie jest
losowana ze wszystkich wyrazów — funkcyjne odpadają (końcówkę „khráp” wstawi
odruchowo, nie ze zrozumienia), a z reszty aplikacja wybiera w czasie
działania, biorąc pod uwagę to, co uczący się zna. Dlatego przy każdej luce
zapisujemy hasło słownikowe i jego częstość: bez tego aplikacja nie wie, czy
pyta o słowo poznane w zeszłym tygodniu, czy o takie, którego uczący się nigdy
nie widział.

TOLERANCJA NIEZNANEGO (inferenceItems)

Zdanie z jednym celowo nieznanym słowem: uczący się ma zgadnąć jego znaczenie
z kontekstu, wybierając z czterech propozycji. Przy pokryciu słownictwa poniżej
95 procent to nie jest ćwiczenie dodatkowe, tylko warunek rozumienia
czegokolwiek — a wbrew intuicji jest trenowalne.

Wybór słowa docelowego: rzadkie albo trudne, przy czym reszta zdania musi być
częsta. Zdanie, w którym nieznane są trzy słowa naraz, niczego nie ćwiczy —
kontekstu po prostu nie ma.

Dystraktory pochodzą z tej samej kategorii co słowo docelowe. To celowe:
gdyby foile były przypadkowe, odpowiedź dałoby się wybrać po samym temacie
rozmowy, bez słuchania zdania. Kiedy wszystkie cztery propozycje są z jednego
pola znaczeniowego, rozstrzyga dopiero kontekst.

Wskazówki (cues) pokazywane po odpowiedzi wyliczamy tu, a nie w aplikacji,
bo wymagają przeszukania słownika i listy klasyfikatorów. Każda wskazuje
konkretne miejsce w zdaniu, nie ogólne „domyśl się z kontekstu”.

Uruchomienie:  python3 tools/generators/comprehension.py
"""

import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comprehension_lib as CL  # noqa: E402

OUT = os.path.join(CL.DATA, "comprehension.json")

# Wyraz na lukę musi być na tyle długi, żeby dało się go usłyszeć jako całość.
MIN_GAP_LETTERS = 2
# Ile luk najwyżej w jednej kwestii — więcej i ćwiczenie zmienia się w dyktando.
MAX_SLOTS = 4

LEVEL_INDEX = {lvl: i for i, lvl in enumerate(
    ["Survival", "A1", "A2", "B1", "B2"])}

NUMBER_WORDS = {
    CL.fold(w) for w in [
        "nɯ̀ng", "sǎwng", "sǎam", "sìi", "hâa", "hòk", "jèt", "pɛ̀ɛt", "kâo",
        "sìp", "rɔ́ɔi", "phan", "mɯ̀ɯn", "lǎai", "kìi",
    ]
}


def classifier_map():
    """Klasyfikator -> co się nim liczy (z listy klasyfikatorów bazy)."""
    out = {}
    for c in CL.load("classifiers.json")["records"]:
        key = CL.fold(c["classifier"])
        if not key:
            continue
        nouns = [n["polish"] for n in c.get("nouns", [])][:3]
        out[key] = {
            "classifier": c["classifier"],
            "explanation": c.get("explanation", ""),
            "nouns": nouns,
        }
    return out


def usable(word, rec):
    """Czy ten wyraz nadaje się na lukę albo na słowo docelowe."""
    if rec is None:
        return False
    folded = CL.fold(word)
    if len(folded) < MIN_GAP_LETTERS:
        return False
    if folded in CL.FUNCTION_WORDS:
        return False
    return True


# ------------------------------------------------------------------- luki
def build_gaps(dialogues, lex):
    items = []
    n = 0
    for d in dialogues:
        for ln in d["lines"]:
            ws = CL.words(ln["thaiPhonetic"])
            if len(ws) < 3:
                continue          # w zdaniu dwuwyrazowym luka to połowa zdania
            slots = []
            for i, w in enumerate(ws):
                rec = lex.word(w)
                if not usable(w, rec):
                    continue
                # Znaczenie hasła pokazujemy tylko wtedy, gdy potwierdza je
                # tłumaczenie kwestii. Odpowiedzią w tym ćwiczeniu jest sam
                # brakujący wyraz, więc luka bez potwierdzonego znaczenia
                # nadal działa — po prostu nie dostaje podpowiedzi „to znaczy”.
                verified = CL.sense_matches(rec["polish"], ln.get("polish", ""))
                slot = {
                    "w": i,
                    "r": rec["id"],
                    "f": rec.get("frequency", 3),
                    "lvl": rec.get("level", ""),
                }
                if verified:
                    slot["p"] = rec["polish"]
                slots.append(slot)
            if not slots:
                continue
            # Zostawiamy najbardziej treściwe pozycje: najrzadsze wyrazy niosą
            # najwięcej znaczenia, więc ich brak najbardziej boli.
            slots.sort(key=lambda s: (s["f"], s["w"]))
            n += 1
            items.append({
                "id": "gap-%04d" % n,
                "d": d["id"],
                "l": ln["index"],
                "words": len(ws),
                "slots": slots[:MAX_SLOTS],
            })
    return items


# ------------------------------------------- zdania z jednym nieznanym słowem
def build_inference(dialogues, lex, rng):
    """Zdania z jednym słowem, którego uczący się na tym etapie jeszcze nie zna.

    „Nieznane” nie znaczy „rzadkie w bazie”. W dialogach praktycznie nie ma
    słów rzadkich — 5551 z 7682 dopasowanych wyrazów to hasła o najwyższej
    częstości, bo dialogi są z założenia zbudowane z tego, co przydatne.
    Rzadkość jest więc złym kryterium: dałaby kilkanaście zdań na całą bazę.

    Nieznane jest natomiast to, co wyprzedza uczącego się na ścieżce nauki.
    Bierzemy więc słowo, którego poziom jest wyższy niż mediana poziomów
    pozostałych słów w zdaniu. Wtedy zdanie faktycznie wygląda tak, jak
    wygląda mowa o jeden stopień za trudna: tło znajome, jedna dziura.
    Aplikacja dobiera potem zdania tak, żeby dziura wypadła poza tym, co
    uczący się już widział.
    """
    clsmap = classifier_map()
    by_category = {}
    for r in lex.single.values():
        by_category.setdefault(r["category"], []).append(r)

    items = []
    n = 0
    used_targets = {}
    for d in dialogues:
        for ln in d["lines"]:
            ws = CL.words(ln["thaiPhonetic"])
            if len(ws) < 4:
                continue      # krótkie zdanie nie daje kontekstu

            annotated = [(i, w, lex.word(w)) for i, w in enumerate(ws)]
            content = [a for a in annotated
                       if a[2] is not None and usable(a[1], a[2])]
            if len(content) < 3:
                continue      # zbyt mało znanego tła, żeby było z czego wnioskować

            levels = sorted(LEVEL_INDEX[a[2]["level"]] for a in content)
            base = levels[len(levels) // 2]

            candidates = [
                a for a in content
                if LEVEL_INDEX[a[2]["level"]] > base
                and len(by_category.get(a[2]["category"], [])) >= 4
            ]
            if not candidates:
                continue

            # Kolejność prób: największy przeskok poziomu, przy remisie
            # trudniejsze hasło. Przechodzimy całą listę, bo kontrola sensu
            # odrzuca sporo kandydatów — rezygnacja po pierwszym odrzuconym
            # kosztowałaby osiem na dziesięć zdań.
            candidates.sort(
                key=lambda a: (-(LEVEL_INDEX[a[2]["level"]] - base),
                               -a[2].get("difficulty", 1), a[0]),
            )
            line_pl = ln.get("polish", "")
            chosen = None
            for cand_idx, cand_word, cand_rec in candidates:
                if used_targets.get(cand_rec["id"], 0) >= 3:
                    continue
                # Klucz odpowiedzi musi się zgadzać z tłumaczeniem kwestii.
                if not CL.sense_matches(cand_rec["polish"], line_pl):
                    continue
                pool = [r for r in by_category[cand_rec["category"]]
                        if r["id"] != cand_rec["id"]
                        and r["polish"] != cand_rec["polish"]
                        and not CL.sense_matches(r["polish"], line_pl)]
                if len(pool) < 3:
                    continue
                trial = [r["polish"] for r in rng.sample(pool, 3)]
                if len(set(trial)) < 3 or cand_rec["polish"] in trial:
                    continue
                chosen = (cand_idx, cand_word, cand_rec, trial)
                break
            if chosen is None:
                continue
            idx, word, target, foils = chosen

            cues = []
            # 1. Sytuacja rozmowy — najszersza wskazówka, zawsze dostępna.
            cues.append({
                "w": -1,
                "text": "Rozmowa toczy się w sytuacji „" + d["situation"]
                        + "”, a rozmawiają: "
                        + " i ".join(d["roles"][k] for k in sorted(d["roles"]))
                        + ". To samo w sobie zawęża pole do kilku znaczeń.",
            })
            # 2. Sąsiad z tej samej kategorii — najmocniejsza wskazówka lokalna.
            for i, w, rec in content:
                if i == idx:
                    continue
                if not CL.sense_matches(rec["polish"], line_pl):
                    continue
                if rec["category"] == target["category"]:
                    cues.append({
                        "w": i,
                        "text": "W tym samym zdaniu pada „" + w + "” ("
                                + rec["polish"] + ") z tej samej kategorii: "
                                + rec["category"] + ". Zdanie krąży wokół jednego tematu.",
                    })
                    break
            # 3. Klasyfikator obok mówi wprost, co się liczy.
            for j in (idx - 1, idx + 1):
                if not 0 <= j < len(ws):
                    continue
                info = clsmap.get(CL.fold(ws[j]))
                # Klasyfikator poznaje się po ramie: liczebnik obok. Bez tego
                # warunku „chûai” (pomagać) trafiałoby na klasyfikator o tym
                # samym zapisie i produkowało wskazówkę prowadzącą donikąd.
                framed = any(
                    0 <= k < len(ws) and CL.fold(ws[k]) in NUMBER_WORDS
                    for k in (j - 1, j + 1)
                )
                if info and info["nouns"] and framed:
                    cues.append({
                        "w": j,
                        "text": "Stoi przy nim klasyfikator „" + info["classifier"]
                                + "”, którym liczy się: " + ", ".join(info["nouns"])
                                + ". Szukane słowo musi być z tego kręgu.",
                    })
                    break
            # 4. Liczebnik przed wyrazem — rzecz policzalna, nie czynność.
            if idx > 0 and CL.fold(ws[idx - 1]) in NUMBER_WORDS:
                cues.append({
                    "w": idx - 1,
                    "text": "Poprzedza go liczebnik „" + ws[idx - 1]
                            + "”, więc chodzi o rzecz policzalną, a nie o czynność.",
                })
            # 5. Rama zdaniowa: co stoi tuż przed i tuż po. Wskazówka dostępna
            #    prawie zawsze i najbliższa temu, co robi się w rozmowie —
            #    znaczenie wyciąga się z sąsiedztwa, nie ze słownika.
            verified_near = [(i, w, r) for i, w, r in content
                             if CL.sense_matches(r["polish"], line_pl)]
            before = next((r for i, w, r in verified_near if i == idx - 1), None)
            after = next((r for i, w, r in verified_near if i == idx + 1), None)
            if before is not None or after is not None:
                parts = []
                if before is not None:
                    parts.append("przed nim „" + ws[idx - 1] + "” (" + before["polish"] + ")")
                if after is not None:
                    parts.append("po nim „" + ws[idx + 1] + "” (" + after["polish"] + ")")
                cues.append({
                    "w": idx - 1 if before is not None else idx + 1,
                    "text": "Miejsce w zdaniu: " + ", ".join(parts)
                            + ". Szukane słowo musi pasować dokładnie w tę szczelinę.",
                })

            if len(cues) < 2:
                continue     # jedna wskazówka to za mało, żeby dało się zgadnąć

            used_targets[target["id"]] = used_targets.get(target["id"], 0) + 1
            options = [target["polish"]] + foils
            order = list(range(4))
            rng.shuffle(order)
            shuffled = [options[i] for i in order]
            items.append({
                "d": d["id"],
                "l": ln["index"],
                "w": idx,
                "r": target["id"],
                "p": target["polish"],
                "level": target.get("level", ""),
                "levelGap": LEVEL_INDEX[target["level"]] - base,
                "freq": target.get("frequency", 3),
                "category": target["category"],
                "opts": shuffled,
                "a": shuffled.index(target["polish"]),
                "cues": cues,
            })
    return items


def build_inference_from_examples(lex, rng, used_targets):
    """Zdania z nieznanym słowem zbudowane na przykładach użycia z haseł.

    Kwestie dialogów są tu słabym materiałem z jednego powodu: żeby ustalić,
    co dane słowo znaczy W TYM zdaniu, trzeba je odnaleźć w polskim
    tłumaczeniu — a tłumaczenia są idiomatyczne. „pai” tłumaczy się raz jako
    „idziemy”, raz jako „jedziesz”, raz znika w polskim zdaniu bezosobowym.
    Kontrola sensu odrzuca wtedy nawet trafne dopasowania i z 1682 kwestii
    zostaje kilkadziesiąt.

    Przykłady użycia nie mają tego problemu. Przykład należy do hasła, więc
    znaczenie słowa docelowego jest znane z definicji — nie trzeba go zgadywać
    ani sprawdzać. Klucz odpowiedzi jest poprawny z konstrukcji, a nie
    z dopasowania tekstów.
    """
    clsmap = classifier_map()
    by_category = {}
    for r in lex.single.values():
        by_category.setdefault(r["category"], []).append(r)

    items = []
    for target in sorted(lex.single.values(), key=lambda r: r["id"]):
        if len(by_category.get(target["category"], [])) < 4:
            continue
        target_level = LEVEL_INDEX[target["level"]]
        key = CL.fold(target["thaiPhonetic"])

        for ex in target.get("examples", []):
            if used_targets.get(target["id"], 0) >= 3:
                break
            ws = CL.words(ex.get("thaiPhonetic", ""))
            if len(ws) < 4:
                continue
            positions = [i for i, w in enumerate(ws) if CL.fold(w) == key]
            if len(positions) != 1:
                continue          # słowo musi w zdaniu wystąpić dokładnie raz
            idx = positions[0]

            annotated = [(i, w, lex.word(w)) for i, w in enumerate(ws)]
            background = [
                a for a in annotated
                if a[0] != idx and a[2] is not None and usable(a[1], a[2])
            ]
            # Tło musi być łatwiejsze od słowa docelowego — inaczej nieznane
            # jest nie jedno słowo, tylko połowa zdania.
            if len(background) < 2:
                continue
            if any(LEVEL_INDEX[a[2]["level"]] > target_level for a in background):
                continue

            line_pl = ex.get("polish", "")
            pool = [r for r in by_category[target["category"]]
                    if r["id"] != target["id"]
                    and r["polish"] != target["polish"]
                    and not CL.sense_matches(r["polish"], line_pl)]
            if len(pool) < 3:
                continue
            foils = [r["polish"] for r in rng.sample(pool, 3)]
            if len(set(foils)) < 3 or target["polish"] in foils:
                continue

            cues = [{
                "w": -1,
                "text": "Zdanie należy do kręgu tematycznego „" + target["category"]
                        + "”" + (" (" + target["subcategory"] + ")"
                                 if target.get("subcategory") else "")
                        + ". Już to odsiewa większość znaczeń.",
            }]
            for i, w, rec in background:
                if rec["category"] == target["category"] and \
                        CL.sense_matches(rec["polish"], line_pl):
                    cues.append({
                        "w": i,
                        "text": "W tym samym zdaniu pada „" + w + "” ("
                                + rec["polish"] + ") z tej samej kategorii. "
                                "Zdanie krąży wokół jednego tematu.",
                    })
                    break
            for j in (idx - 1, idx + 1):
                if not 0 <= j < len(ws):
                    continue
                info = clsmap.get(CL.fold(ws[j]))
                framed = any(
                    0 <= k < len(ws) and CL.fold(ws[k]) in NUMBER_WORDS
                    for k in (j - 1, j + 1)
                )
                if info and info["nouns"] and framed:
                    cues.append({
                        "w": j,
                        "text": "Stoi przy nim klasyfikator „" + info["classifier"]
                                + "”, którym liczy się: " + ", ".join(info["nouns"])
                                + ". Szukane słowo musi być z tego kręgu.",
                    })
                    break
            if idx > 0 and CL.fold(ws[idx - 1]) in NUMBER_WORDS:
                cues.append({
                    "w": idx - 1,
                    "text": "Poprzedza go liczebnik „" + ws[idx - 1]
                            + "”, więc chodzi o rzecz policzalną, a nie o czynność.",
                })
            near = {i: r for i, w, r in background
                    if CL.sense_matches(r["polish"], line_pl)}
            parts = []
            if idx - 1 in near:
                parts.append("przed nim „" + ws[idx - 1] + "” (" + near[idx - 1]["polish"] + ")")
            if idx + 1 in near:
                parts.append("po nim „" + ws[idx + 1] + "” (" + near[idx + 1]["polish"] + ")")
            if parts:
                cues.append({
                    "w": idx - 1 if idx - 1 in near else idx + 1,
                    "text": "Miejsce w zdaniu: " + ", ".join(parts)
                            + ". Szukane słowo musi pasować dokładnie w tę szczelinę.",
                })

            if len(cues) < 2:
                continue

            used_targets[target["id"]] = used_targets.get(target["id"], 0) + 1
            options = [target["polish"]] + foils
            order = list(range(4))
            rng.shuffle(order)
            shuffled = [options[i] for i in order]
            items.append({
                "src": "example",
                "r": target["id"],
                "ex": target["examples"].index(ex),
                "w": idx,
                "p": target["polish"],
                "level": target["level"],
                "levelGap": 0,
                "freq": target.get("frequency", 3),
                "category": target["category"],
                "opts": shuffled,
                "a": shuffled.index(target["polish"]),
                "cues": cues,
            })
    return items


def main():
    rng = random.Random(20260824)
    records = CL.load_records()
    dialogues = CL.load_dialogues()
    lex = CL.Lexicon(records)

    gaps = build_gaps(dialogues, lex)
    used = {}
    inference = build_inference(dialogues, lex, rng)
    for it in inference:
        it["src"] = "dialogue"
        used[it["r"]] = used.get(it["r"], 0) + 1
    inference += build_inference_from_examples(lex, rng, used)
    for i, it in enumerate(inference, 1):
        it["id"] = "inf-%04d" % i

    payload = {
        "file": "comprehension.json",
        "generator": "tools/generators/comprehension.py",
        "gapCount": len(gaps),
        "inferenceCount": len(inference),
        "note": "Adnotacje do kwestii dialogów. Treść kwestii pozostaje "
                "w plikach dialogues-part-*.json — tutaj są tylko numery "
                "wyrazów, odwołania do haseł i wskazówki kontekstowe.",
        "gapItems": gaps,
        "inferenceItems": inference,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)

    print("=" * 58)
    print("GENEROWANIE ĆWICZEŃ ROZUMIENIA")
    print("=" * 58)
    print("  kwestii z lukami           %5d" % len(gaps))
    print("  możliwych luk              %5d" % sum(len(g["slots"]) for g in gaps))
    print("  zdań z nieznanym słowem    %5d" % len(inference))
    src = {}
    for i in inference:
        src[i["src"]] = src.get(i["src"], 0) + 1
    print("      z kwestii dialogów     %5d" % src.get("dialogue", 0))
    print("      z przykładów użycia    %5d" % src.get("example", 0))
    cues = sum(len(i["cues"]) for i in inference)
    print("  wskazówek kontekstowych    %5d (średnio %.1f na zdanie)"
          % (cues, cues / max(1, len(inference))))
    lv = {}
    for i in inference:
        lv[i["level"]] = lv.get(i["level"], 0) + 1
    for k in ["Survival", "A1", "A2", "B1", "B2"]:
        if lv.get(k):
            print("      %-10s             %5d" % (k, lv[k]))
    print("-" * 58)
    print("Zapisano %s (%.1f kB)" % (OUT, os.path.getsize(OUT) / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
