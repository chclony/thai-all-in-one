#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator scen — data/scenes.json.

PO CO TO JEST

Wszystkie dotychczasowe ćwiczenia rozumienia kończą się na jednym zdaniu.
Rozmowa to inna umiejętność: trzeba utrzymać wątek przez kilkanaście wymian,
przejść nad nieznanym słowem do porządku dziennego i wyłapać, o co komu chodzi
— a nie przetłumaczyć każde słowo. Przy pokryciu mowy potocznej rzędu 80 procent
co piąty wyraz i tak będzie nieznany, więc umiejętność „idę dalej mimo dziury”
jest warunkiem rozumienia czegokolwiek dłuższego.

Scena to jedna sytuacja od wejścia do wyjścia: gość wchodzi do restauracji,
zamawia, dopytuje, płaci i wychodzi. Składamy ją z gotowych dialogów, bo one
już są sprawdzone, mają płeć mówiących, warianty potoczne i dane dla
syntezatora. Scena nie kopiuje ich treści — trzyma tylko kolejność i to,
czego w pojedynczym dialogu nie ma: sens całości.

JAK POWSTAJE SCENA

1. Dialogi trafiają do wątków (restauracja + jedzenie to jeden wątek,
   transport + orientacja w terenie to drugi) i dalej dzielą się na poziomy.
2. Grupa krótsza niż 20 kwestii dokleja się do sąsiedniego poziomu w tym samym
   wątku — inaczej powstałaby scena, która kończy się, zanim się zacznie.
3. Grupa dzieli się na sceny programowaniem dynamicznym: każdy kawałek musi
   mieć 20-40 kwestii, a wśród układów spełniających ten warunek wygrywa ten
   najbliższy 28 kwestiom. Podział idzie po granicach dialogów, więc żadna
   scena nie urywa się w połowie rozmowy.

PYTANIA

Wyłącznie o sens całości — żadne nie da się rozstrzygnąć z jednego zdania.
Trzy poziomy szczegółowości, bo tryb słuchania ekstensywnego pyta trzy razy,
za każdym razem drążąc głębiej:

  poziom 1  o co w ogóle chodziło, gdzie to się działo, kto brał udział
  poziom 2  jak scena się zaczęła, czym skończyła, w jakiej kolejności,
            czego w niej NIE było
  poziom 3  gdzie w scenie padło konkretne słowo, ile spraw załatwiono

Dystraktory biorą się z innych scen — najchętniej z tego samego wątku, bo
wtedy odpowiedź wymaga wysłuchania właśnie tej sceny, a nie zgadnięcia po
temacie. Generator pilnuje, żeby dystraktor nie zawierał niczego, co w scenie
faktycznie padło: pytanie z dwiema poprawnymi odpowiedziami jest gorsze niż
brak pytania.

Uruchomienie:  python3 tools/generators/scenes.py
"""

import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comprehension_lib as CL  # noqa: E402

OUT = os.path.join(CL.DATA, "scenes.json")

LEVEL_ORDER = ["Survival", "A1", "A2", "B1", "B2"]

# Sytuacja z dialogu -> wątek. Wątek jest szerszy niż kategoria: „zamawianie
# napojów” i „rachunek w restauracji” to jedno wyjście na miasto, choć
# w bazie siedzą pod różnymi hasłami.
THREAD_OF = {
    "Restauracja": "jedzenie",
    "Jedzenie i napoje": "jedzenie",
    "Transport": "droga",
    "Miejsca i orientacja": "droga",
    "Hotel": "nocleg",
    "Zakupy i pieniądze": "zakupy",
    "Zdrowie": "zdrowie",
    "Praca i nauka": "praca",
    "Dom i codzienność": "dom",
    "Small talk": "ludzie",
    "Ludzie i rodzina": "ludzie",
    "Czas i daty": "ludzie",
    "Pogoda i przyroda": "ludzie",
    "Podstawy i grzeczność": "ludzie",
    "Awarie i pomoc": "klopoty",
}

# Nazwa wątku i opis miejsca. Opis wchodzi wprost do pytania o scenerię,
# więc musi brzmieć jak zdanie, a nie jak etykieta w bazie.
THREADS = {
    "jedzenie": ("Jedzenie na mieście", "w restauracji albo przy jedzeniu"),
    "droga": ("W drodze", "w podróży — transport i szukanie drogi"),
    "nocleg": ("Nocleg", "w hotelu albo na kwaterze"),
    "zakupy": ("Zakupy i pieniądze", "przy kupowaniu, targowaniu się i płaceniu"),
    "zdrowie": ("Zdrowie", "u lekarza, w aptece albo przy dolegliwości"),
    "praca": ("Praca i nauka", "w pracy, na uczelni albo w sprawach zawodowych"),
    "dom": ("Dom i codzienność", "w domu i w sprawach codziennych"),
    "ludzie": ("Ludzie i rozmowa", "w rozmowie towarzyskiej — o sobie, rodzinie i czasie"),
    "klopoty": ("Kłopoty i pomoc", "przy awarii, zgubie albo prośbie o pomoc"),
}

MIN_LINES = 20
MAX_LINES = 40
TARGET_LINES = 28


# --------------------------------------------------------------- etykiety
def beat_label(title):
    """Tytuł dialogu skrócony do nazwy odcinka sceny.

    „W restauracji: zamawianie” -> „zamawianie”. Prefiks przed dwukropkiem
    powtarza sytuację, którą scena i tak podaje raz, u góry.
    """
    label = title.split(":", 1)[1].strip() if ":" in title else title.strip()
    if label and label[0].isupper() and not label.startswith(("Ile", "Kto", "Co", "Gdzie")):
        # Zdanie w środku wyliczenia zaczyna się małą literą.
        label = label[0].lower() + label[1:]
    return label


def join_beats(labels, limit=4):
    take = labels[:limit]
    text = ", ".join(take)
    if len(labels) > limit:
        text += ", …"
    return text


def level_max(levels):
    return max(levels, key=lambda l: LEVEL_ORDER.index(l))


# ------------------------------------------------------------- grupowanie
def partition(counts, lo=MIN_LINES, hi=MAX_LINES, target=TARGET_LINES):
    """Podział listy na kolejne kawałki o sumie w przedziale lo..hi.

    Zwraca listę list indeksów albo None, gdy się nie da. Wśród układów
    spełniających warunek wybieramy ten o najmniejszej sumie kwadratów
    odchyleń od wartości docelowej — kawałki wychodzą wtedy równe, bez
    jednego skrajnie krótkiego i jednego skrajnie długiego obok siebie.

    Podział idzie tylko po granicach elementów (dialogów albo scen), więc
    żaden element nie zostaje przecięty w środku.
    """
    n = len(counts)
    best = [None] * (n + 1)      # best[i] = (koszt, poprzedni indeks)
    best[0] = (0.0, -1)
    for i in range(1, n + 1):
        for j in range(i):
            if best[j] is None:
                continue
            total = sum(counts[j:i])
            if not lo <= total <= hi:
                continue
            cost = best[j][0] + (total - target) ** 2
            if best[i] is None or cost < best[i][0]:
                best[i] = (cost, j)
    if best[n] is None:
        return None
    chunks, at = [], n
    while at > 0:
        prev = best[at][1]
        chunks.append(list(range(prev, at)))
        at = prev
    chunks.reverse()
    return chunks


def group_dialogues(dialogues):
    """Dialogi -> grupy (wątek, poziomy) gotowe do podziału na sceny.

    Grupa nie nadaje się do podziału w dwóch przypadkach: jest za krótka na
    jedną scenę albo długości dialogów nie składają się na kawałki 20-40
    kwestii (41 kwestii w dwóch dialogach po 8 i 33 nie da się podzielić
    inaczej niż źle). Oba przypadki rozwiązuje to samo: doklejenie grupy do
    sąsiedniego poziomu w tym samym wątku. Większa grupa ma więcej granic,
    po których wolno ciąć.
    """
    buckets = {}
    for d in dialogues:
        thread = THREAD_OF[d["situation"]]
        buckets.setdefault((thread, d["level"]), []).append(d)

    def broken(items):
        return partition([len(d["lines"]) for d in items]) is None

    changed = True
    while changed:
        changed = False
        for (thread, level), items in sorted(buckets.items(),
                                             key=lambda kv: sum(len(d["lines"]) for d in kv[1])):
            if not broken(items):
                continue
            here = LEVEL_ORDER.index(level)
            neighbours = [
                (thread, LEVEL_ORDER[i])
                for i in (here - 1, here + 1)
                if 0 <= i < len(LEVEL_ORDER) and (thread, LEVEL_ORDER[i]) in buckets
            ]
            if not neighbours:
                # Wątek nie ma sąsiada — łączymy z najmniejszą grupą wątku.
                neighbours = [k for k in buckets if k[0] == thread and k != (thread, level)]
            if not neighbours:
                continue
            target = min(neighbours, key=lambda k: sum(len(d["lines"]) for d in buckets[k]))
            merged = buckets.pop((thread, level))
            # Kolejność wewnątrz grupy: po poziomie, potem po identyfikatorze —
            # scena ma iść od łatwiejszego do trudniejszego.
            buckets[target] = sorted(
                buckets[target] + merged,
                key=lambda d: (LEVEL_ORDER.index(d["level"]), d["id"]),
            )
            changed = True
            break
    return buckets


# ------------------------------------------------------------------ scena
def build_scene(scene_id, thread, items, lex):
    label, where = THREADS[thread]
    beats = []
    for i, d in enumerate(items):
        beats.append({
            "index": i,
            "dialogueId": d["id"],
            "title": d["title"],
            "label": beat_label(d["title"]),
            "level": d["level"],
            "lineCount": len(d["lines"]),
            "roles": [d["roles"][k] for k in sorted(d["roles"])],
        })

    line_count = sum(b["lineCount"] for b in beats)
    phonetics = []
    translations = []
    for i, d in enumerate(items):
        for ln in d["lines"]:
            phonetics.append((i, ln["thaiPhonetic"]))
            translations.append(ln.get("polish", ""))

    est = {
        t: round(CL.lines_seconds([p for _, p in phonetics], t))
        for t in ("slow", "natural", "fast")
    }

    roles = []
    for b in beats:
        for r in b["roles"]:
            if r not in roles:
                roles.append(r)

    levels = sorted({b["level"] for b in beats}, key=LEVEL_ORDER.index)
    labels = [b["label"] for b in beats]

    # Słowo kluczowe pokazujemy uczącemu się razem ze znaczeniem, więc każde
    # musi przejść kontrolę sensu — inaczej scena uczyłaby homofonu.
    keywords = lex.keywords(phonetics, limit=12, skip=CL.FUNCTION_WORDS,
                            translations=translations)

    return {
        "id": scene_id,
        "type": "scene",
        "thread": thread,
        "threadLabel": label,
        "title": label + " — " + join_beats(labels, 3),
        "level": level_max(levels),
        "levels": levels,
        "situation": (
            "Jedna sytuacja od wejścia do wyjścia, " + where + ". Po kolei: "
            + join_beats(labels, 6) + ". Rozmawiają: " + ", ".join(roles) + "."
        ),
        "summary": join_beats(labels, 4),
        "setting": label + " — " + where,
        "dialogueIds": [b["dialogueId"] for b in beats],
        "beats": beats,
        "lineCount": line_count,
        "estSeconds": est,
        "roles": roles,
        "keywords": keywords,
        "questions": [],
    }


# ---------------------------------------------------------------- pytania
def pick_foils(pool, wanted, exclude, rng):
    """Trzy dystraktory z puli, z pominięciem tego, co w scenie padło."""
    seen = set(exclude)
    out = []
    for item in rng.sample(pool, len(pool)):
        key = item if isinstance(item, str) else item[0]
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
        if len(out) == wanted:
            break
    return out


def question(qid, tier, kind, prompt, correct, foils, explain, note=""):
    options = [correct] + list(foils)
    order = list(range(len(options)))
    random.Random(qid).shuffle(order)
    shuffled = [options[i] for i in order]
    return {
        "id": qid,
        "tier": tier,
        "kind": kind,
        "prompt": prompt,
        "options": shuffled,
        "answer": shuffled.index(correct),
        "explain": explain,
        "note": note,
    }


def build_questions(scene, scenes_by_thread, all_scenes, lex, rng):
    out = []
    sid = scene["id"]
    labels = [b["label"] for b in scene["beats"]]
    own_labels = set(labels)

    # Sceny, z których wolno brać dystraktory: najpierw ten sam wątek,
    # potem reszta. Ten sam wątek jest trudniejszy i o to chodzi.
    siblings = [s for s in scenes_by_thread[scene["thread"]] if s["id"] != sid]
    others = [s for s in all_scenes if s["id"] != sid and s["thread"] != scene["thread"]]
    near = siblings + others

    # --- poziom 1: o co chodziło -------------------------------------------
    settings = []
    for s in near:
        if s["setting"] != scene["setting"] and s["setting"] not in settings:
            settings.append(s["setting"])
    if len(settings) >= 3:
        out.append(question(
            sid + "-q1", 1, "setting",
            "Gdzie i w jakiej sprawie toczyła się cała scena?",
            scene["setting"], settings[:3],
            "Sceneria bierze się z tego, kto się odzywa i o co pyta — nie z "
            "pojedynczego słowa. Tu przez całą scenę wracają role: "
            + ", ".join(scene["roles"]) + ".",
        ))

    gist_foils = []
    for s in near:
        if own_labels & {b["label"] for b in s["beats"]}:
            continue          # dzieli odcinek ze sceną — byłby częściowo prawdziwy
        text = s["summary"]
        if text != scene["summary"] and text not in gist_foils:
            gist_foils.append(text)
    if len(gist_foils) >= 3:
        out.append(question(
            sid + "-q2", 1, "gist",
            "Który opis pasuje do całej sceny, a nie do jej kawałka?",
            scene["summary"], gist_foils[:3],
            "Poprawny opis obejmuje wszystkie " + str(len(labels)) + " części sceny: "
            + join_beats(labels, 6) + ".",
        ))

    foreign_roles = []
    for s in near:
        for r in s["roles"]:
            if r not in scene["roles"] and r not in foreign_roles:
                foreign_roles.append(r)
    if len(scene["roles"]) >= 3 and foreign_roles:
        out.append(question(
            sid + "-q3", 1, "whoAbsent",
            "Kto NIE odzywał się w tej scenie?",
            foreign_roles[0], rng.sample(scene["roles"], 3),
            "W scenie słychać: " + ", ".join(scene["roles"]) + ".",
        ))

    # --- poziom 2: budowa sceny --------------------------------------------
    foreign_labels = []
    for s in near:
        for b in s["beats"]:
            if b["label"] not in own_labels and b["label"] not in foreign_labels:
                foreign_labels.append(b["label"])

    if len(labels) >= 2:
        later = labels[1:]
        foils = later[:3]
        if len(foils) < 3:
            foils += foreign_labels[:3 - len(foils)]
        if len(foils) == 3:
            out.append(question(
                sid + "-q4", 2, "first",
                "Od czego ta scena się zaczęła?",
                labels[0], foils,
                "Pierwsza część sceny to „" + labels[0] + "”. Reszta przyszła później.",
            ))

        earlier = labels[:-1]
        foils = earlier[-3:]
        if len(foils) < 3:
            foils += foreign_labels[:3 - len(foils)]
        if len(foils) == 3:
            out.append(question(
                sid + "-q5", 2, "last",
                "Czym ta scena się skończyła?",
                labels[-1], foils,
                "Ostatnia część sceny to „" + labels[-1] + "”.",
            ))

    if len(labels) >= 3 and foreign_labels:
        out.append(question(
            sid + "-q6", 2, "absent",
            "Której sprawy w tej scenie NIE załatwiano?",
            foreign_labels[0], rng.sample(labels, 3),
            "W scenie było: " + join_beats(labels, 6) + ". Reszta pochodzi z innej rozmowy.",
        ))

    if len(labels) >= 4:
        chosen = sorted(rng.sample(range(len(labels)), 4))
        first = labels[chosen[0]]
        out.append(question(
            sid + "-q7", 2, "order",
            "Które z tych zdarzeń było w scenie najwcześniej?",
            first, [labels[i] for i in chosen[1:]],
            "Kolejność w scenie: " + join_beats(labels, 8) + ".",
        ))

    # --- poziom 3: szczegóły, których nie da się zgadnąć --------------------
    own_words = {k["thaiPhonetic"] for k in scene["keywords"]}
    own_folded = {CL.fold(k["thaiPhonetic"]) for k in scene["keywords"]}

    # Pełny zasób wyrazów sceny — dystraktor nie może przypadkiem w niej paść.
    said = set()
    for _, phon in [(b["index"], b) for b in scene["beats"]]:
        pass
    for b in scene["beats"]:
        pass

    if len(scene["keywords"]) >= 3:
        foreign_words = []
        for s in near:
            for k in s["keywords"]:
                folded = CL.fold(k["thaiPhonetic"])
                if folded in own_folded or folded in scene.get("__allWords", set()):
                    continue
                if k["thaiPhonetic"] in [w[0] for w in foreign_words]:
                    continue
                foreign_words.append((k["thaiPhonetic"], k["polish"]))
        if foreign_words:
            shown = lambda k: k["thaiPhonetic"] + " (" + k["polish"] + ")"
            out.append(question(
                sid + "-q8", 3, "keywordAbsent",
                "Które z tych słów w tej scenie NIE padło?",
                foreign_words[0][0] + " (" + foreign_words[0][1] + ")",
                [shown(k) for k in rng.sample(scene["keywords"][:8], 3)],
                "Pozostałe trzy słychać w scenie — pierwsze z nich nawet "
                + str(scene["keywords"][0]["count"]) + " razy.",
            ))

    single_beat = [k for k in scene["keywords"] if len(k["beats"]) == 1]
    if single_beat and len(labels) >= 2:
        key = single_beat[0]
        correct = labels[key["beats"][0]]
        foils = [l for l in labels if l != correct][:3]
        if len(foils) < 3:
            foils += [l for l in foreign_labels if l not in foils][:3 - len(foils)]
        if len(foils) == 3:
            out.append(question(
                sid + "-q9", 3, "keywordWhere",
                "W której części sceny padło słowo „" + key["thaiPhonetic"]
                + "” (" + key["polish"] + ")?",
                correct, foils,
                "To słowo pada tylko raz, w części „" + correct + "”. "
                "W pozostałych częściach nie ma go wcale.",
            ))

    if len(labels) >= 3:
        n = len(labels)
        foils = [str(x) for x in (n - 1, n + 1, n + 2) if x >= 1][:3]
        out.append(question(
            sid + "-q10", 3, "beatCount",
            "Ile odrębnych spraw załatwiono w tej scenie?",
            str(n), foils,
            "Odrębnych spraw było " + str(n) + ": " + join_beats(labels, 8) + ".",
        ))

    return out


# ------------------------------------------------------------------ bloki
def build_blocks(scenes, rng):
    """Bloki do słuchania ekstensywnego: 3-5 minut ciągłego materiału.

    Pojedyncza scena to około półtorej minuty — za mało, żeby uczący się
    zdążył wpaść w rytm i przestać tłumaczyć w głowie każde zdanie. Blok
    skleja więc kolejne sceny tego samego wątku, aż materiał przekroczy trzy
    minuty, i zamyka go przed piątą. Sceny wewnątrz bloku idą po poziomach,
    więc blok wchodzi w temat od łatwiejszej strony.
    """
    MIN_S, MAX_S = 180, 300
    blocks = []
    by_thread = {}
    for s in scenes:
        by_thread.setdefault(s["thread"], []).append(s)

    leftover = []
    for thread in sorted(by_thread):
        items = sorted(by_thread[thread],
                       key=lambda s: (LEVEL_ORDER.index(s["level"]), s["id"]))
        secs = [s["estSeconds"]["natural"] for s in items]
        chunks = partition(secs, MIN_S, MAX_S, 240)
        if chunks is None:
            # Wątek nie dzieli się na bloki po 3-5 minut przy granicach scen.
            # Bierzemy z niego tyle, ile się da, resztę odkładamy — blok krótszy
            # niż trzy minuty przestałby być słuchaniem ekstensywnym.
            best = None
            for cut in range(len(items), 0, -1):
                trial = partition(secs[:cut], MIN_S, MAX_S, 240)
                if trial is not None:
                    best = (trial, cut)
                    break
            if best is None:
                leftover += items
                continue
            chunks, cut = best
            leftover += items[cut:]
        for chunk in chunks:
            members = [items[i] for i in chunk]
            blocks.append((thread, members, sum(secs[i] for i in chunk)))

    if leftover:
        # Reszta wątku bywa za krótka na własny blok (sześć scen wątku
        # „jedzenie” to 319 sekund — na jeden blok za dużo, na dwa za mało).
        # Zamiast wyrzucać ten materiał z trybu, składamy z resztek blok
        # przeglądowy. Wątek jest wtedy mieszany i blok mówi o tym wprost,
        # bo uczący się musi wiedzieć, że temat zmieni się w trakcie.
        leftover.sort(key=lambda s: (LEVEL_ORDER.index(s["level"]), s["id"]))
        secs = [s["estSeconds"]["natural"] for s in leftover]
        chunks = partition(secs, MIN_S, MAX_S, 240)
        if chunks is None:
            print("  UWAGA: %d scen poza trybem ekstensywnym (za krótkie na blok)"
                  % len(leftover))
        else:
            for chunk in chunks:
                blocks.append((None, [leftover[i] for i in chunk],
                               sum(secs[i] for i in chunk)))

    out = []
    for i, (thread, members, _secs) in enumerate(blocks, 1):
        if thread is None:
            label, where = "Przegląd mieszany", "kilka różnych sytuacji pod rząd"
        else:
            label, where = THREADS[thread]
        levels = sorted({s["level"] for s in members}, key=LEVEL_ORDER.index)
        est = {
            t: sum(s["estSeconds"][t] for s in members)
            for t in ("slow", "natural", "fast")
        }
        bid = "block-%03d" % i
        titles = [s["beats"][0]["label"] for s in members]
        block = {
            "id": bid,
            "type": "block",
            "thread": thread or "mixed",
            "threadLabel": label,
            "mixed": thread is None,
            "title": label + " — blok " + str(i) + ": " + join_beats(titles, 3),
            "level": level_max(levels),
            "levels": levels,
            "setting": label + " — " + where,
            "sceneIds": [s["id"] for s in members],
            "lineCount": sum(s["lineCount"] for s in members),
            "estSeconds": est,
            "estMinutes": round(est["natural"] / 60.0, 1),
            "passes": [],
        }

        # Pytania po każdym przejściu: coraz głębiej. Losujemy z pytań scen
        # składowych, po jednym z każdej sceny, żeby żadna nie została pominięta.
        for tier, title, hint in (
            (1, "bez tekstu", "Pierwsze przejście — słuchasz bez podpórki. "
                              "Pytania są o sens całości."),
            (2, "z tekstem", "Drugie przejście — masz zapis przed oczami. "
                             "Pytania schodzą do budowy sceny."),
            (3, "znów bez tekstu", "Trzecie przejście — tekst znika. "
                                   "Pytania są najbardziej szczegółowe."),
        ):
            picked = []
            for s in members:
                pool = [q for q in s["questions"] if q["tier"] == tier]
                if pool:
                    picked.append(rng.choice(pool)["id"])
            # Uzupełniamy do trzech pytań, jeśli scen w bloku było mniej.
            if len(picked) < 3:
                extra = [q["id"] for s in members for q in s["questions"]
                         if q["tier"] == tier and q["id"] not in picked]
                picked += extra[:3 - len(picked)]
            block["passes"].append({
                "pass": tier,
                "mode": "text" if tier == 2 else "audio",
                "label": title,
                "hint": hint,
                "questionIds": picked,
            })
        out.append(block)
    return out


# ------------------------------------------------------------------- main
def main():
    rng = random.Random(20260823)
    records = CL.load_records()
    dialogues = CL.load_dialogues()
    lex = CL.Lexicon(records)

    buckets = group_dialogues(dialogues)

    scenes = []
    counter = 0
    for (thread, level) in sorted(buckets, key=lambda k: (k[0], LEVEL_ORDER.index(k[1]))):
        items = sorted(buckets[(thread, level)],
                       key=lambda d: (LEVEL_ORDER.index(d["level"]), d["id"]))
        counts = [len(d["lines"]) for d in items]
        chunks = partition(counts)
        if chunks is None:
            print("  UWAGA: nie udało się podzielić grupy %s/%s (%d kwestii)"
                  % (thread, level, sum(counts)))
            continue
        for chunk in chunks:
            counter += 1
            scene = build_scene("scene-%03d" % counter, thread,
                                [items[i] for i in chunk], lex)
            scenes.append(scene)

    # Zbiór wszystkich wyrazów sceny — potrzebny, żeby dystraktor „to słowo
    # nie padło” faktycznie nie padł. Liczymy raz, przed pytaniami.
    by_id = {d["id"]: d for d in dialogues}
    for s in scenes:
        said = set()
        for did in s["dialogueIds"]:
            for ln in by_id[did]["lines"]:
                for w in CL.words(ln["thaiPhonetic"]):
                    said.add(CL.fold(w))
        s["__allWords"] = said

    by_thread = {}
    for s in scenes:
        by_thread.setdefault(s["thread"], []).append(s)

    for s in scenes:
        s["questions"] = build_questions(s, by_thread, scenes, lex, rng)

    for s in scenes:
        del s["__allWords"]

    blocks = build_blocks(scenes, rng)

    payload = {
        "file": "scenes.json",
        "generator": "tools/generators/scenes.py",
        "count": len(scenes),
        "blockCount": len(blocks),
        "lineCount": sum(s["lineCount"] for s in scenes),
        "questionCount": sum(len(s["questions"]) for s in scenes),
        "durationModel": {
            "secPerSyllable": CL.SEC_PER_SYLLABLE,
            "gapBetweenLines": CL.GAP_BETWEEN_LINES,
            "note": "Czas szacowany z liczby sylab i przerwy między kwestiami "
                    "(Player.playSequence). Nagranie lektora może się różnić.",
        },
        "records": scenes,
        "blocks": blocks,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)

    # --- raport ------------------------------------------------------------
    print("=" * 58)
    print("GENEROWANIE SCEN")
    print("=" * 58)
    print("  scen                       %5d" % len(scenes))
    print("  kwestii w scenach          %5d" % payload["lineCount"])
    print("  pytań o sens całości       %5d" % payload["questionCount"])
    print("  bloków ekstensywnych       %5d" % len(blocks))
    total_min = sum(b["estSeconds"]["natural"] for b in blocks) / 60.0
    print("  materiał ekstensywny       %5.1f min" % total_min)
    lens = sorted(s["lineCount"] for s in scenes)
    print("  długość sceny              %d-%d kwestii (mediana %d)"
          % (lens[0], lens[-1], lens[len(lens) // 2]))
    per_level = {}
    for s in scenes:
        per_level[s["level"]] = per_level.get(s["level"], 0) + 1
    for lvl in LEVEL_ORDER:
        if per_level.get(lvl):
            print("      %-10s             %5d scen" % (lvl, per_level[lvl]))
    print("-" * 58)
    print("Zapisano %s (%.1f kB)" % (OUT, os.path.getsize(OUT) / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
