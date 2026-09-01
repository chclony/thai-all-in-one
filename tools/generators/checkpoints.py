#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Próbki kontrolne — generator data/checkpoints.json.

Po co to jest
-------------
Powtórki (SRS) wykrywają zapominanie dopiero wtedy, gdy karta wypadnie do
powtórzenia. Przy odstępach rosnących wykładniczo hasło opanowane w lekcji 12
wraca po miesiącu, potem po trzech — a między jednym a drugim terminem nie ma
żadnego sygnału. Uczący się przechodzi kolejne lekcje w przekonaniu, że
poprzednie zostały w głowie, i dowiaduje się, że nie, dopiero przy powtórce
albo na egzaminie poziomowym.

Próbka kontrolna jest tanim czujnikiem wstawionym POMIĘDZY terminy powtórek:
co 20 lekcji krótki test z materiału sprzed 20 lekcji. Nie zastępuje SRS-u
i niczego nie planuje — ma tylko powiedzieć wcześniej to, co SRS powie później.

Które lekcje sprawdza
---------------------
Próbka po lekcji M obejmuje okno [M-39, M-20], czyli materiał sprzed 20 lekcji.
Pierwsza wypada więc po lekcji 40 i pyta o lekcje 1-20; kolejna po lekcji 60
i pyta o lekcje 21-40. Materiał ma za sobą co najmniej 20 lekcji przerwy —
dość, żeby zdążył wyblaknąć, i mało, żeby dało się go jeszcze odzyskać bez
przerabiania wszystkiego od nowa.

Uruchomienie:
    python3 tools/generators/checkpoints.py
"""

import glob
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, HERE)

import jsonio  # noqa: E402

EVERY = 20          # co ile lekcji wypada próbka
LAG = 20            # o ile lekcji wstecz sięga sprawdzany materiał
LISTEN_COUNT = 7    # rozpoznanie ze słuchu
RECALL_COUNT = 5    # odtworzenie zapisu z pamięci
TIME_LIMIT = 360    # sekundy — sześć minut na dwanaście zadań

# Próg 75 %: dziewięć z dwunastu. Niżej niż na egzaminie (tam najniższy próg to
# 60 %), bo próbka nie decyduje o niczym — nie zalicza poziomu ani nie blokuje
# dalszych lekcji. Ma być czuła, a nie surowa: lepiej raz wysłać do powtórki
# kogoś, kto miał gorszy dzień, niż przegapić realny ubytek.
PASS_PCT = 75


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def load_records():
    records = {}
    skip = {"manifest.json", "metadata.json", "search-index.json",
            "search-index-rest.json", "coverage.json", "comprehension.json",
            "scenes.json", "progress-migration.json", "exams.json",
            "checkpoints.json"}
    for path in sorted(glob.glob(os.path.join(DATA, "*.json"))):
        name = os.path.basename(path)
        if name in skip:
            continue
        try:
            payload = load(name)
        except (ValueError, OSError):
            continue
        if not isinstance(payload, dict):
            continue
        for rec in payload.get("records") or []:
            if isinstance(rec, dict) and rec.get("id") and rec.get("thaiPhonetic") \
                    and rec.get("type") != "dialogue":
                records.setdefault(rec["id"], rec)
    return records


def main():
    rng = random.Random(20260831)
    lessons = load("lessons.json")["records"]
    records = load_records()

    by_number = {les["number"]: les for les in lessons}
    last = max(by_number)

    out = []
    trigger = EVERY + LAG        # pierwsza próbka: po lekcji 40
    while trigger <= last:
        lo, hi = trigger - EVERY - LAG + 1, trigger - LAG
        window = [by_number[n] for n in range(lo, hi + 1) if n in by_number]
        if not window:
            trigger += EVERY
            continue

        # kandydaci: hasła wprowadzone w oknie, dość częste, żeby ich utrata
        # była realną stratą, i dość krótkie, żeby dało się je zapisać
        pool = []
        for les in window:
            for rid in les.get("newWordIds") or []:
                rec = records.get(rid)
                if not rec or not rec.get("polish") or not rec.get("ttsThai"):
                    continue
                syl = rec.get("syllables") or []
                if not (1 <= len(syl) <= 6) or (rec.get("frequency") or 0) < 3:
                    continue
                pool.append((rid, rec, les["number"]))
        # jedno hasło raz
        uniq, seen = [], set()
        for item in pool:
            if item[0] in seen:
                continue
            seen.add(item[0])
            uniq.append(item)

        need = LISTEN_COUNT + RECALL_COUNT
        if len(uniq) < need + 6:
            trigger += EVERY
            continue

        rng.shuffle(uniq)
        chosen = uniq[:need]
        rest = uniq[need:]

        items = []
        for i, (rid, rec, lesson_no) in enumerate(chosen):
            kind = "listen" if i < LISTEN_COUNT else "recall"
            entry = {
                "id": "chk-%03d-%02d" % (trigger, i + 1),
                "kind": kind,
                "recordId": rid,
                "polish": rec["polish"],
                "lesson": lesson_no,
                "level": rec.get("level") or "",
                "category": rec.get("category") or "",
            }
            if kind == "listen":
                # dystraktory z tego samego okna — inaczej odpowiedź wychodzi
                # z samego tematu, a nie z rozpoznania brzmienia
                wrong = [r[1]["polish"] for r in rest
                         if r[1]["polish"] != rec["polish"]]
                wrong = list(dict.fromkeys(wrong))
                if len(wrong) < 3:
                    continue
                options = rng.sample(wrong, 3) + [rec["polish"]]
                rng.shuffle(options)
                entry["options"] = options
                entry["answer"] = options.index(rec["polish"])
            items.append(entry)

        if len(items) < need:
            trigger += EVERY
            continue

        out.append({
            "id": "checkpoint-%03d" % trigger,
            "triggerLesson": trigger,
            "fromLesson": lo,
            "toLesson": hi,
            "level": window[len(window) // 2]["level"],
            "taskCount": len(items),
            "timeLimitSec": TIME_LIMIT,
            "passPct": PASS_PCT,
            "title": "Próbka kontrolna: lekcje %d-%d" % (lo, hi),
            "items": items,
        })
        trigger += EVERY

    payload = {
        "file": "checkpoints.json",
        "generator": "tools/generators/checkpoints.py",
        "note": ("Krótki test co %d lekcji z materiału sprzed %d lekcji. "
                 "Wykrywa zapominanie wcześniej, niż zrobi to kolejka powtórek, "
                 "bo nie czeka na termin karty." % (EVERY, LAG)),
        "every": EVERY,
        "lag": LAG,
        "passPct": PASS_PCT,
        "timeLimitSec": TIME_LIMIT,
        "count": len(out),
        "records": out,
    }
    jsonio.dump(payload, os.path.join(DATA, "checkpoints.json"))

    print("=" * 58)
    print("PRÓBKI KONTROLNE")
    print("=" * 58)
    for c in out:
        print("  %-18s po lekcji %3d · sprawdza %3d-%3d · zadań %d"
              % (c["id"], c["triggerLesson"], c["fromLesson"], c["toLesson"],
                 c["taskCount"]))
    print("-" * 58)
    print("  próbek %d · co %d lekcji · opóźnienie %d lekcji · próg %d%%"
          % (len(out), EVERY, LAG, PASS_PCT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
