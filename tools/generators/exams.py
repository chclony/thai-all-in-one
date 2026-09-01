#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Egzaminy poziomowe — generator data/exams.json.

Po co to jest
------------
Test poziomujący (js/placement.js) sprawdza rozpoznanie pojedynczych słów na
WEJŚCIU: ma posadzić uczącego się w odpowiednim miejscu ścieżki, więc jego próg
jest celowo niski (60 %) i mierzy jedną rzecz — rozumienie hasła w izolacji.

Nie było niczego, co sprawdzałoby WYJŚCIE: czy po przejściu materiału poziomu
uczący się faktycznie ten poziom osiągnął. Bez tego „ukończyłem A2” znaczy
tylko „wyklikałem lekcje”.

Egzamin poziomowy jest osobnym narzędziem i ma inną budowę:

  1. mierzy CZTERY SPRAWNOŚCI OSOBNO, bo one nie chodzą razem — można rozumieć
     scenę ze słuchu i nie umieć powiedzieć w niej ani zdania,
  2. każda sprawność ma WŁASNY PRÓG, a poziom jest zaliczony dopiero wtedy,
     gdy wszystkie cztery przekroczą swój próg; średnia jest tu zakazana,
     bo maskuje dokładnie to, co egzamin ma wykryć (98 % ze słuchu i 20 %
     w mówieniu daje „59 % — zdane”, a to nieprawda),
  3. ma trzy niezależne ZESTAWY na poziom, żeby powtórka po nieudanym podejściu
     szła na innym materiale, a nie na zapamiętanym kluczu odpowiedzi.

Skąd bierze się materiał
------------------------
  - rozumienie ze słuchu i rozumienie szczegółowe: sceny (data/scenes.json),
    czyli 20-40 kwestii pod rząd, z zapisanym czasem trwania w trzech tempach;
    pytania budujemy TUTAJ, a nie bierzemy gotowych ze scen, bo egzamin
    potrzebuje ich rozłącznych zestawów, a scena ma ich tylko po kilka,
  - produkcja ustna i pisemna: hasła z lekcji danego poziomu.

Uruchomienie:
    python3 tools/generators/exams.py
"""

import glob
import json
import os
import random
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, HERE)

import jsonio  # noqa: E402

LEVELS = ["Survival", "A1", "A2", "B1", "B2"]
VARIANTS = ["A", "B", "C"]

# --- ile zadań w każdej sprawności ------------------------------------------
#
# Liczby nie są okrągłe dla ozdoby. Przy czterech opcjach zgadywanie daje
# 25 %, więc próg musi leżeć tak wysoko nad przypadkiem, żeby zdanie przez
# przypadek było mało prawdopodobne, a jednocześnie liczba zadań musi być na
# tyle duża, by jedna pomyłka nie przesądzała o wyniku.
#
#   6 pytań / próg 70 %  -> trzeba 5 (83 %); zgadywanie daje 5+ z p = 0,004
#  10 pytań / próg 65 %  -> trzeba 7 (70 %); zgadywanie daje 7+ z p = 0,003
#
# Uzasadnienie progów samo w sobie leży w docs/raport-koncowy.md.
COUNTS = {
    "listening": 6,
    "detail": 10,
    "speaking": 6,
    "writing": 8,
}

# --- limity czasu (sekundy) --------------------------------------------------
#
# Limit jest na SEKCJĘ, nie na cały egzamin. Jeden wspólny limit premiuje tych,
# którzy przelecą przez słuchanie i zostawią sobie kwadrans na pisanie —
# a wtedy przestajemy mierzyć cztery sprawności, tylko jedną umiejętność
# gospodarowania czasem.
#
# Każdy limit to czas potrzebny spokojnie, powiększony o połowę:
#   - słuchanie: 2 sceny po ok. 100 s w tempie naturalnym + jedno powtórzenie
#     każdej + 6 pytań po 25 s = ok. 550 s,
#   - szczegóły: 10 pytań po 30 s = 300 s (sceny są już wysłuchane),
#   - mówienie: 6 zadań po 70 s (nagranie, odsłuch, ocena) = 420 s,
#   - pisanie: 8 zadań po 45 s = 360 s.
TIME = {
    "listening": 840,
    "detail": 450,
    "speaking": 630,
    "writing": 540,
}

# --- progi -------------------------------------------------------------------
THRESHOLDS = {
    "listening": 70,        # procent trafnych odpowiedzi
    "detail": 65,           # procent trafnych odpowiedzi
    "speakingTone": 60,     # średnia punktów oceny wymowy (sesja J)
    "speakingContent": 70,  # procent zadań, w których padła właściwa treść
    "writing": 60,          # procent trafnie zapisanych sylab
}

# --- warunki powtórki --------------------------------------------------------
#
# „Po co najmniej kilku dniach nauki” rozbijamy na dwa warunki naraz, bo każdy
# z osobna da się obejść: sam odstęp dni przeczekać nic nie robiąc, a samą
# liczbę lekcji przeklikać w jeden wieczór. Dopiero oba razem znaczą „wróć,
# kiedy naprawdę coś się zmieniło”.
COOLDOWN = {"days": 5, "lessons": 6}

SECTION_META = [
    {
        "id": "listening",
        "label": "Rozumienie ze słuchu",
        "short": "Słuch",
        "skill": "Rozumiesz sens sceny słuchanej w tempie naturalnym, bez zapisu przed oczami.",
        "how": "Dwie sceny w tempie naturalnym, bez tekstu. Każdą możesz odtworzyć najwyżej dwa razy. Pytania dotyczą sensu całości.",
    },
    {
        "id": "detail",
        "label": "Rozumienie szczegółowe",
        "short": "Szczegóły",
        "skill": "Wyławiasz ze sceny konkrety: kto co powiedział, co padło w odpowiedzi, co było wcześniej.",
        "how": "Pytania o konkretne wypowiedzi z wysłuchanych scen. Bez tekstu i bez ponownego odsłuchu.",
    },
    {
        "id": "speaking",
        "label": "Produkcja ustna",
        "short": "Mówienie",
        "skill": "Mówisz z pamięci to, co trzeba powiedzieć w danej sytuacji, i robisz to zrozumiale.",
        "how": "Sytuacja po polsku, nagrywasz odpowiedź po tajsku. Wymowa oceniana automatycznie (kontur tonalny), treść — po odsłuchaniu wzorca.",
    },
    {
        "id": "writing",
        "label": "Produkcja pisemna",
        "short": "Zapis",
        "skill": "Odtwarzasz z pamięci brzmienie zwrotu w zapisie fonetycznym.",
        "how": "Słyszysz zwrot i zapisujesz go alfabetem łacińskim. Jeden odsłuch dodatkowy, bez podglądu.",
    },
]

TONE_MARKS = "\u0301\u0300\u0302\u030c\u0304"


def fold(text):
    """Zapis bez znaków tonu i bez wielkości liter — do porównań."""
    norm = unicodedata.normalize("NFD", text or "")
    plain = "".join(c for c in norm if c not in TONE_MARKS)
    return unicodedata.normalize("NFC", plain).lower().strip()


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def load_records():
    """Wszystkie hasła i wszystkie dialogi z katalogu data/."""
    records, dialogues = {}, {}
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
            if not isinstance(rec, dict) or not rec.get("id"):
                continue
            if rec.get("type") == "dialogue":
                dialogues[rec["id"]] = rec
            elif rec.get("thaiPhonetic"):
                records.setdefault(rec["id"], rec)
    return records, dialogues


# ---------------------------------------------------------------- pomocnicze

def opts(rng, correct, wrong_pool, count=4):
    """Cztery opcje: jedna prawdziwa i trzy różne od niej i od siebie."""
    pool = [w for w in dict.fromkeys(wrong_pool) if w and w != correct]
    if len(pool) < count - 1:
        return None
    picked = rng.sample(pool, count - 1)
    options = picked + [correct]
    rng.shuffle(options)
    return {"options": options, "answer": options.index(correct)}


def scene_lines(scene, dialogues):
    """Kwestie sceny po kolei, z rolą i numerem części."""
    out = []
    for beat_index, did in enumerate(scene.get("dialogueIds") or []):
        dlg = dialogues.get(did)
        if not dlg:
            continue
        roles = dlg.get("roles") or {}
        for line in dlg.get("lines") or []:
            out.append({
                "polish": line.get("polish") or "",
                "role": roles.get(line.get("role")) or line.get("role") or "",
                "beat": beat_index,
                "pos": len(out),
            })
    return out


# --------------------------------------------------- pytania o sens całości

def listening_pool(scene, scenes, all_scenes, dialogues, rng):
    """Sześć pytań o sens całej sceny — po jednym każdego rodzaju.

    Sześć, bo przy pięciu scenach na poziomie Survival jedna scena wchodzi do
    dwóch zestawów egzaminu, a zestawy nie mogą dzielić ani jednego pytania.

    Dystraktory czerpiemy najpierw z tego samego poziomu, a gdy tam nie ma ich
    dość — z pozostałych. Poziom Survival ma pięć scen z trzech wątków, więc
    samych opisów scenerii jest tam mniej niż cztery i pytanie o scenerię
    w ogóle by nie powstało. Sceneria z innego poziomu nie zdradza odpowiedzi
    (to nazwa miejsca, nie próbka języka), a bez niej zestaw C nie miałby
    z czego powstać.
    """
    others = ([s for s in scenes if s["id"] != scene["id"]]
              + [s for s in all_scenes
                 if s["id"] != scene["id"] and s["level"] != scene["level"]])
    my_roles = set(scene.get("roles") or [])
    my_labels = {b.get("label") or b.get("title") for b in scene.get("beats") or []}
    questions = []

    def add(kind, prompt, built, explain):
        if not built:
            return
        questions.append({
            "id": "%s-%s" % (scene["id"].replace("scene", "ex"), kind),
            "kind": kind,
            "sceneId": scene["id"],
            "prompt": prompt,
            "options": built["options"],
            "answer": built["answer"],
            "explain": explain,
        })

    # 1. sceneria
    add("setting", "Gdzie i w jakiej sprawie toczyła się ta scena?",
        opts(rng, scene["setting"], [s["setting"] for s in others]),
        "Sceneria bierze się z tego, kto się odzywa i o co pyta, a nie z jednego "
        "usłyszanego słowa. W tej scenie rozmawiają: %s."
        % ", ".join(sorted(my_roles)))

    # 2. streszczenie całości
    add("gist", "Który opis pasuje do całej sceny, a nie do jej kawałka?",
        opts(rng, scene["summary"], [s["summary"] for s in others]),
        "Poprawny opis obejmuje wszystkie części sceny: %s."
        % ", ".join(sorted(my_labels)))

    # 3. kto się nie odzywał
    foreign_roles = [r for s in others for r in (s.get("roles") or []) if r not in my_roles]
    if len(my_roles) >= 3 and foreign_roles:
        absent = rng.choice(sorted(set(foreign_roles)))
        present = rng.sample(sorted(my_roles), 3)
        options = present + [absent]
        rng.shuffle(options)
        add("whoAbsent", "Kto NIE odzywał się w tej scenie?",
            {"options": options, "answer": options.index(absent)},
            "W scenie słychać: %s. Pozostałe role pochodzą z innych scen."
            % ", ".join(sorted(my_roles)))

    # 4. o czym nie było mowy
    foreign_labels = [b.get("label") or b.get("title")
                      for s in others for b in (s.get("beats") or [])]
    foreign_labels = [x for x in foreign_labels if x and x not in my_labels]
    if len(my_labels) >= 3 and foreign_labels:
        absent = rng.choice(sorted(set(foreign_labels)))
        present = rng.sample(sorted(my_labels), 3)
        options = present + [absent]
        rng.shuffle(options)
        add("topicAbsent", "O czym w tej scenie NIE było mowy?",
            {"options": options, "answer": options.index(absent)},
            "Scena składa się z części: %s." % ", ".join(sorted(my_labels)))

    # 5. ile osób
    count = len(my_roles)
    numbers = sorted({count, max(2, count - 2), count + 1, count + 3})
    if len(numbers) >= 4:
        numbers = numbers[:4] if count in numbers[:4] else sorted(set(numbers[:3] + [count]))
    if len(numbers) == 4:
        options = [str(n) for n in numbers]
        add("speakerCount", "Ile różnych osób odzywało się w tej scenie?",
            {"options": options, "answer": options.index(str(count))},
            "Odzywa się %d osób: %s." % (count, ", ".join(sorted(my_roles))))

    # 6. z ilu części
    beats = len(scene.get("beats") or [])
    nums = sorted({beats, max(1, beats - 1), beats + 1, beats + 2})
    if len(nums) == 4:
        options = [str(n) for n in nums]
        add("beatCount", "Z ilu części — osobnych rozmów — składała się ta scena?",
            {"options": options, "answer": options.index(str(beats))},
            "Części jest %d: %s." % (beats, ", ".join(
                (b.get("label") or b.get("title") or "") for b in scene.get("beats") or [])))

    return questions


# ------------------------------------------------------- pytania o szczegóły

def detail_pool(scene, lines, foreign_lines, rng):
    """Dwanaście pytań o konkrety z tej sceny.

    Dwanaście, bo scena użyta w dwóch zestawach musi dostarczyć po pięć
    rozłącznych pytań każdemu, a część kandydatów odpada na kontroli
    jednoznaczności (ta sama kwestia w dwóch rolach, powtórzone zdanie).
    """
    said = {ln["polish"] for ln in lines}
    pool = [x for x in foreign_lines if x not in said]
    questions = []
    prefix = scene["id"].replace("scene", "exd")

    def add(kind, seq, prompt, built, explain):
        if not built:
            return
        questions.append({
            "id": "%s-%s%d" % (prefix, kind, seq),
            "kind": kind,
            "sceneId": scene["id"],
            "prompt": prompt,
            "options": built["options"],
            "answer": built["answer"],
            "explain": explain,
        })

    # a) czy to padło (4 pytania)
    usable = [ln for ln in lines if len(ln["polish"]) >= 8]
    rng.shuffle(usable)
    for i, ln in enumerate(usable[:4]):
        add("said", i + 1, "Która z tych wypowiedzi padła w scenie?",
            opts(rng, ln["polish"], pool),
            "To zdanie mówi %s w części %d. Pozostałe pochodzą z innych scen."
            % (ln["role"] or "jedna z osób", ln["beat"] + 1))

    # b) kto to powiedział (3 pytania) — tylko dla kwestii jednoznacznych
    roles_of = {}
    for ln in lines:
        roles_of.setdefault(ln["polish"], set()).add(ln["role"])
    unique = [ln for ln in lines
              if len(roles_of[ln["polish"]]) == 1 and len(ln["polish"]) >= 8]
    all_roles = sorted({ln["role"] for ln in lines if ln["role"]})
    rng.shuffle(unique)
    seq = 0
    for ln in unique:
        if seq >= 3 or len(all_roles) < 4:
            break
        built = opts(rng, ln["role"], [r for r in all_roles if r != ln["role"]])
        if not built:
            break
        seq += 1
        add("who", seq, "Kto powiedział w tej scenie: „%s”?" % ln["polish"], built,
            "Ta kwestia należy do roli „%s” w części %d." % (ln["role"], ln["beat"] + 1))

    # c) co padło w odpowiedzi (3 pytania)
    pairs = [(lines[i], lines[i + 1]) for i in range(len(lines) - 1)
             if lines[i]["beat"] == lines[i + 1]["beat"]
             and len(lines[i]["polish"]) >= 8 and len(lines[i + 1]["polish"]) >= 8]
    rng.shuffle(pairs)
    for i, (before, after) in enumerate(pairs[:3]):
        add("reply", i + 1, "Co padło zaraz po zdaniu „%s”?" % before["polish"],
            opts(rng, after["polish"], pool),
            "Odpowiada %s: „%s”." % (after["role"] or "druga osoba", after["polish"]))

    # d) co padło najwcześniej (2 pytania) — wszystkie opcje są ze sceny
    long_lines = [ln for ln in lines if len(ln["polish"]) >= 8]
    for i in range(2):
        if len(long_lines) < 8:
            break
        picked = rng.sample(long_lines, 4)
        positions = {ln["polish"]: ln["pos"] for ln in picked}
        if len(positions) < 4:
            continue
        first = min(picked, key=lambda x: x["pos"])
        options = [ln["polish"] for ln in picked]
        questions.append({
            "id": "%s-order%d" % (prefix, i + 1),
            "kind": "order",
            "sceneId": scene["id"],
            "prompt": "Która z tych wypowiedzi padła w scenie NAJWCZEŚNIEJ?",
            "options": options,
            "answer": options.index(first["polish"]),
            "explain": "Kolejność w scenie: %s." % " → ".join(
                ln["polish"] for ln in sorted(picked, key=lambda x: x["pos"])),
        })

    return questions


# ----------------------------------------------------- hasła do produkcji

def production_candidates(records, taught_at_level, min_syl, max_syl):
    """Hasła nadające się na zadanie produkcyjne.

    O przynależności do poziomu decyduje LEKCJA, w której hasło zostało
    wprowadzone, a nie pole `level` samego hasła. To nie jest drobiazg:
    lekcje poziomu B2 wprowadzają mnóstwo haseł oznaczonych niżej (bo
    pojedyncze słowo bywa proste, a dopiero jego użycie jest trudne), więc
    filtrowanie po polu `level` zostawiało dla B2 pustą pulę. Egzamin ma
    sprawdzać MATERIAŁ POZIOMU, czyli to, czego uczyły jego lekcje.

    Dalsze warunki: da się to wypowiedzieć jednym tchem, jest częste
    (egzamin nie sprawdza rzadkich ozdobników) i ma tekst dla syntezatora,
    bo bez niego nie ma czego odtworzyć w zadaniu na zapis.
    """
    out = []
    for rid in taught_at_level:
        rec = records.get(rid)
        if not rec:
            continue
        syl = rec.get("syllables") or []
        if not (min_syl <= len(syl) <= max_syl):
            continue
        if (rec.get("frequency") or 0) < 3:
            continue
        if not rec.get("polish") or not rec.get("ttsThai"):
            continue
        out.append(rid)
    out.sort()
    return out


# ------------------------------------------------------------------- główne

def main():
    rng = random.Random(20260830)

    lessons_data = load("lessons.json")
    lessons = lessons_data["records"]
    scenes_data = load("scenes.json")
    scenes = scenes_data["records"]
    records, dialogues = load_records()

    # hasło -> numer lekcji, w której zostało wprowadzone
    lesson_of = {}
    # poziom -> hasła wprowadzone przez lekcje tego poziomu
    taught = {}
    for les in lessons:
        for rid in les.get("newWordIds") or []:
            if rid in lesson_of:
                continue
            lesson_of[rid] = les["number"]
            taught.setdefault(les["level"], []).append(rid)
    # dialog -> lekcje, w których jest omawiany
    lesson_of_dialogue = {}
    for les in lessons:
        did = les.get("dialogueId")
        if did:
            lesson_of_dialogue.setdefault(did, []).append(les["number"])

    level_lessons = {}
    for les in lessons:
        level_lessons.setdefault(les["level"], []).append(les["number"])

    # wszystkie kwestie po poziomach — źródło dystraktorów
    lines_by_level = {}
    for sc in scenes:
        lines_by_level.setdefault(sc["level"], []).extend(
            ln["polish"] for ln in scene_lines(sc, dialogues))

    out_records = []
    problems = []

    for level in LEVELS:
        level_scenes = [s for s in scenes if s["level"] == level]
        level_scenes.sort(key=lambda s: s["id"])
        if len(level_scenes) < 2:
            problems.append("%s: za mało scen (%d)" % (level, len(level_scenes)))
            continue

        # pule pytań budujemy RAZ na scenę, a potem rozdajemy zestawom bez
        # powtórzeń — dzięki temu dwa zestawy nigdy nie dostaną tego samego
        # pytania, nawet jeśli dzielą scenę (Survival ma ich tylko pięć).
        pools = {}
        for sc in level_scenes:
            lines = scene_lines(sc, dialogues)
            foreign = [p for p in lines_by_level.get(level, [])
                       if p not in {ln["polish"] for ln in lines}]
            pools[sc["id"]] = {
                "lines": lines,
                "listening": listening_pool(sc, level_scenes, scenes, dialogues, rng),
                "detail": detail_pool(sc, lines, foreign, rng),
                "taken": {"listening": 0, "detail": 0},
            }

        at_level = taught.get(level) or []
        speak_pool = production_candidates(records, at_level, 2, 8)
        write_pool = production_candidates(records, at_level, 2, 5)
        rng.shuffle(speak_pool)
        rng.shuffle(write_pool)
        # Zapis i mówienie nie mogą sprawdzać tego samego hasła w jednym
        # egzaminie — inaczej druga sprawność mierzyłaby pamięć z pierwszej.
        used_for_speech = set(speak_pool[:COUNTS["speaking"] * len(VARIANTS)])
        write_pool = [r for r in write_pool if r not in used_for_speech]

        need_speak = COUNTS["speaking"] * len(VARIANTS)
        need_write = COUNTS["writing"] * len(VARIANTS)
        if len(speak_pool) < need_speak or len(write_pool) < need_write:
            problems.append("%s: za mało haseł do produkcji (%d/%d ustnych, %d/%d pisemnych)"
                            % (level, len(speak_pool), need_speak,
                               len(write_pool), need_write))
            continue

        numbers = sorted(level_lessons.get(level) or [0])
        for vi, variant in enumerate(VARIANTS):
            pair = [level_scenes[(2 * vi) % len(level_scenes)],
                    level_scenes[(2 * vi + 1) % len(level_scenes)]]
            if pair[0]["id"] == pair[1]["id"]:
                pair[1] = level_scenes[(2 * vi + 2) % len(level_scenes)]

            listening, detail = [], []
            per_scene_listen = COUNTS["listening"] // 2
            per_scene_detail = COUNTS["detail"] // 2
            ok = True
            for sc in pair:
                pool = pools[sc["id"]]
                start = pool["taken"]["listening"]
                chunk = pool["listening"][start:start + per_scene_listen]
                if len(chunk) < per_scene_listen:
                    ok = False
                    break
                pool["taken"]["listening"] = start + per_scene_listen
                listening.extend(chunk)

                start = pool["taken"]["detail"]
                chunk = pool["detail"][start:start + per_scene_detail]
                if len(chunk) < per_scene_detail:
                    ok = False
                    break
                pool["taken"]["detail"] = start + per_scene_detail
                detail.extend(chunk)

            if not ok:
                problems.append("%s %s: pula pytań wyczerpana" % (level, variant))
                continue

            speak_ids = speak_pool[vi * COUNTS["speaking"]:(vi + 1) * COUNTS["speaking"]]
            write_ids = write_pool[vi * COUNTS["writing"]:(vi + 1) * COUNTS["writing"]]

            speak_items = []
            for rid in speak_ids:
                rec = records[rid]
                speak_items.append({
                    "id": "exs-%s-%s-%s" % (level.lower(), variant.lower(), rid),
                    "recordId": rid,
                    "prompt": rec["polish"],
                    "syllables": len(rec.get("syllables") or []),
                    "lesson": lesson_of.get(rid),
                    "category": rec.get("category") or "",
                })
            write_items = []
            for rid in write_ids:
                rec = records[rid]
                write_items.append({
                    "id": "exw-%s-%s-%s" % (level.lower(), variant.lower(), rid),
                    "recordId": rid,
                    "polish": rec["polish"],
                    "syllables": len(rec.get("syllables") or []),
                    "lesson": lesson_of.get(rid),
                    "category": rec.get("category") or "",
                })

            scene_lessons = []
            for sc in pair:
                for did in sc.get("dialogueIds") or []:
                    scene_lessons.extend(lesson_of_dialogue.get(did) or [])
            scene_lessons = sorted(set(scene_lessons))

            out_records.append({
                "id": "exam-%s-%s" % (level.lower(), variant.lower()),
                "level": level,
                "variant": variant,
                "variantLabel": "zestaw " + variant,
                "lessonFrom": numbers[0],
                "lessonTo": numbers[-1],
                "sceneLessons": scene_lessons,
                "taskCount": sum(COUNTS.values()),
                "timeLimitSec": sum(TIME.values()),
                "sections": {
                    "listening": {
                        "timeLimitSec": TIME["listening"],
                        "sceneIds": [sc["id"] for sc in pair],
                        "questions": listening,
                    },
                    "detail": {
                        "timeLimitSec": TIME["detail"],
                        "sceneIds": [sc["id"] for sc in pair],
                        "questions": detail,
                    },
                    "speaking": {
                        "timeLimitSec": TIME["speaking"],
                        "items": speak_items,
                    },
                    "writing": {
                        "timeLimitSec": TIME["writing"],
                        "items": write_items,
                    },
                },
            })

    payload = {
        "file": "exams.json",
        "generator": "tools/generators/exams.py",
        "note": ("Egzamin na koniec poziomu. Cztery sprawności mierzone osobno, "
                 "każda z własnym progiem; poziom zaliczony dopiero wtedy, gdy "
                 "wszystkie cztery przekroczą swój próg. Trzy rozłączne zestawy "
                 "na poziom, żeby powtórka szła na innym materiale."),
        "levels": LEVELS,
        "variants": VARIANTS,
        "count": len(out_records),
        "counts": COUNTS,
        "time": TIME,
        "thresholds": THRESHOLDS,
        "cooldown": COOLDOWN,
        "sections": SECTION_META,
        "records": out_records,
    }

    jsonio.dump(payload, os.path.join(DATA, "exams.json"))

    print("=" * 58)
    print("EGZAMINY POZIOMOWE")
    print("=" * 58)
    for rec in out_records:
        print("  %-14s %-9s zadań %2d · czas %2d min"
              % (rec["level"], rec["variantLabel"], rec["taskCount"],
                 rec["timeLimitSec"] // 60))
    print("-" * 58)
    print("  egzaminów %d (poziomów %d × zestawów %d)"
          % (len(out_records), len(LEVELS), len(VARIANTS)))
    print("  zadań w egzaminie %d: słuch %d, szczegóły %d, mówienie %d, zapis %d"
          % (sum(COUNTS.values()), COUNTS["listening"], COUNTS["detail"],
             COUNTS["speaking"], COUNTS["writing"]))
    for p in problems:
        print("  UWAGA: " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
