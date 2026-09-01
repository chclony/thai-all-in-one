#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator modułu ratunkowego — data/rescue.json.

Aplikacja nie nauczy prowadzenia rozmowy i nie udaje, że nauczy. Ale rozmowa
nie rozsypuje się na braku swobody — rozsypuje się na jednej sekundzie ciszy
po zdaniu, którego uczący się nie zrozumiał. Prośba o powtórzenie, o wolniejsze
tempo, o prostsze słowo, potwierdzenie własnymi słowami: to są gotowe formuły,
a formuły da się wytrenować drylem do odruchu.

Kryterium jest tu inne niż w słownictwie. Formuła znana, ale wypowiedziana po
czterech sekundach namysłu, nie uratowała już niczego — rozmówca zdążył
przejść dalej albo powtórzyć to samo, tak samo szybko. Dlatego dryl mierzy
czas reakcji i traktuje brak reakcji w oknie jako pomyłkę, nie jako brak
odpowiedzi.

Uruchomienie:
    python3 tools/generators/rescue.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import engine as EN                # noqa: E402
import thai_numbers as TN          # noqa: E402
import colloquial as CO            # noqa: E402
import gender_forms as GF          # noqa: E402
import jsonio                      # noqa: E402

DATA = os.path.join(ROOT, "data")
VERSION = "1.18.0"

# --- słownik ----------------------------------------------------------------

V = {
    "kà-rú-naa": "กรุณา", "phûut": "พูด", "ìik": "อีก", "khráng": "ครั้ง",
    "thii": "ที", "dâai": "ได้", "mǎi": "ไหม", "khráp": "ครับ",
    "cháa": "ช้า", "cháa-cháa": "ช้าๆ", "long": "ลง", "nòi": "หน่อย",
    "ngâai-ngâai": "ง่ายๆ", "khǎw": "ขอ", "kham": "คำ", "khǐan": "เขียน",
    "hâi": "ให้", "chíi": "ชี้", "duu": "ดู", "sà-kòt": "สะกด",
    "khǎw-thôot": "ขอโทษ", "phǒm": "ผม", "mâi": "ไม่", "khâo-jai": "เข้าใจ",
    "láew": "แล้ว", "khàwp-khun": "ขอบคุณ", "ǎw": "อ๋อ",
    "mǎai-khwaam": "หมายความ", "wâa": "ว่า", "châi": "ใช่", "níi": "นี้",
    "plae": "แปล", "à-rai": "อะไร", "wee-laa": "เวลา", "sàk": "สัก",
    "khrûu": "ครู่", "ná": "นะ", "dǐao": "เดี๋ยว", "phôeng": "เพิ่ง",
    "rôem": "เริ่ม", "rian": "เรียน", "phaa-sǎa": "ภาษา", "thai": "ไทย",
    "kèng": "เก่ง", "tâwng": "ต้อง", "pai": "ไป", "kàwn": "ก่อน",
    "an": "อัน", "yàang-níi": "อย่างนี้", "bàep-níi": "แบบนี้",
    "chûai": "ช่วย", "tem": "เต็ม", "dang": "ดัง", "khûen": "ขึ้น",
    "yang": "ยัง", "níit-nàwy": "นิดหน่อย", "rew": "เร็ว", "koen": "เกิน",
}


def words(text):
    """Zapis fonetyczny -> lista par (wyraz, pismo). Klucze muszą być w V."""
    out = []
    for w in text.split(" "):
        if w not in V:
            raise SystemExit("brak wyrazu „%s” w słowniku modułu ratunkowego" % w)
        out.append((w, V[w]))
    return out


def node(polish, phon, register):
    ws = words(phon)
    ph = " ".join(w[0] for w in ws)
    th = "".join(w[1] for w in ws)
    out = {
        "polish": polish,
        "thaiPhonetic": ph,
        "pronunciationPolish": EN.polish_read(ph),
        "toneGuide": EN.tone_guide(ph),
        "ttsThai": th,
        "ttsSplit": [len(w[1]) for w in ws],
        "register": register,
    }
    coll = CO.build(ph, th, EN.polish_read)
    if coll:
        out["colloquial"] = coll
    var = GF.build_variant(out, "formalny" if register == "formalny" else "neutralny")
    if var:
        out["genderVariant"] = {
            "female": {k: v for k, v in var.items() if not k.startswith("_")}
        }
    return out


# --- formuły ----------------------------------------------------------------
#
# (grupa, tytuł, po co to jest, formalna, potoczna, notatka kulturowa)

FORMULAS = [
    ("repeat", "Prośba o powtórzenie",
     "Pierwsza formuła, jakiej użyjesz w życiu. Bez niej rozmowa kończy się na "
     "pierwszym zdaniu, którego nie złapiesz.",
     ("Czy mógłby pan powtórzyć?", "kà-rú-naa phûut ìik khráng dâai mǎi khráp"),
     ("Jeszcze raz?", "phûut ìik thii dâai mǎi khráp"),
     "Prośba o powtórzenie nie jest w Tajlandii przyznaniem się do porażki — jest "
     "normalną częścią rozmowy z obcokrajowcem. Milczenie jest odbierane gorzej: "
     "rozmówca uzna, że go zignorowałeś albo że się obraziłeś."),

    ("slower", "Prośba o wolniejsze tempo",
     "Zwykle skuteczniejsza niż samo powtórzenie: to samo zdanie w tym samym "
     "tempie zrozumiesz tak samo, czyli wcale.",
     ("Czy mógłby pan mówić wolniej?", "kà-rú-naa phûut cháa long nòi dâai mǎi khráp"),
     ("Wolniej, proszę.", "phûut cháa-cháa nòi khráp"),
     "„nòi” łagodzi prośbę i jest tu obowiązkowe. Samo „phûut cháa-cháa” brzmi "
     "jak polecenie wydane komuś na służbie."),

    ("simpler", "Prośba o prostsze słowa",
     "Gdy tempo nie jest problemem, tylko słownictwo. Rozmówca zwykle potrafi "
     "powiedzieć to samo prościej — trzeba go tylko o to poprosić.",
     ("Czy może pan powiedzieć to prostszymi słowami?",
      "khǎw kham ngâai-ngâai dâai mǎi khráp"),
     ("Prościej, proszę.", "phûut ngâai-ngâai nòi khráp"),
     "Ta prośba jest odbierana jako sygnał, że chcesz rozmawiać dalej — częsta "
     "reakcja to przejście na krótsze zdania, a nie na angielski."),

    ("louder", "Prośba o głośniejsze mówienie",
     "W hałasie ulicznym albo przez szybę problem bywa czysto akustyczny, "
     "a nie językowy.",
     ("Czy mógłby pan mówić głośniej?", "kà-rú-naa phûut dang khûen nòi dâai mǎi khráp"),
     ("Głośniej, proszę.", "phûut dang-dang nòi khráp" if False else
      "phûut dang khûen nòi khráp"),
     "Prośba o głośniej jest neutralna, ale zwróconą do osoby starszej albo "
     "wyżej postawionej lepiej otworzyć „kà-rú-naa”."),

    ("write", "Prośba o zapisanie",
     "Ratuje przy nazwach, adresach i kwotach. Zapis nie wymaga tonów ani słuchu.",
     ("Czy mógłby pan to zapisać?", "kà-rú-naa khǐan hâi nòi dâai mǎi khráp"),
     ("Napisz mi to, proszę.", "khǐan hâi nòi khráp"),
     "Uwaga praktyczna: dostaniesz zapis pismem tajskim, którego ta aplikacja "
     "świadomie nie uczy. Do liczby, adresu i godziny to i tak wystarczy — cyfry "
     "arabskie są w Tajlandii w powszechnym użyciu."),

    ("show", "Prośba o pokazanie",
     "Najszybsza droga, gdy chodzi o rzecz albo o kierunek. Palec działa "
     "w każdym tempie.",
     ("Czy mógłby mi pan pokazać?", "chíi hâi duu nòi dâai mǎi khráp"),
     ("Pokaż, proszę.", "chíi hâi duu nòi khráp"),
     "Wskazywanie palcem na osobę jest nieuprzejme, na rzecz i na kierunek — "
     "normalne. Ta prośba dotyczy wyłącznie tego drugiego."),

    ("spell", "Prośba o przeliterowanie",
     "Przy nazwiskach, nazwach miejsc i numerach rezerwacji.",
     ("Czy mógłby pan przeliterować?", "kà-rú-naa sà-kòt hâi nòi dâai mǎi khráp"),
     ("Przeliteruj, proszę.", "sà-kòt hâi nòi khráp"),
     "Ma sens przy zapisie łacińskim i przy cyfrach. Literowanie pisma tajskiego "
     "niewiele Ci da, dopóki go nie czytasz — wtedy lepiej poprosić o zapisanie."),

    ("not-understood", "Sygnalizowanie, że nie rozumiesz",
     "Krótkie, natychmiastowe. Wypowiedziane od razu ratuje rozmowę; "
     "wypowiedziane po pięciu sekundach ciszy już tylko ją tłumaczy.",
     ("Przepraszam, nie rozumiem.", "khǎw-thôot khráp phǒm mâi khâo-jai"),
     ("Nie rozumiem.", "mâi khâo-jai khráp"),
     "Powiedz to WCZEŚNIE. Kiwanie głową na zdanie, którego nie rozumiesz, jest "
     "najkosztowniejszym odruchem początkującego: rozmowa idzie dalej na "
     "fałszywym założeniu i za trzy zdania nie da się już cofnąć."),

    ("understood", "Sygnalizowanie, że rozumiesz",
     "Druga strona tej samej pary. Rozmówca musi wiedzieć, kiedy przestać "
     "tłumaczyć — inaczej powtórzy to samo trzeci raz.",
     ("Już rozumiem, dziękuję.", "khâo-jai láew khráp khàwp-khun khráp"),
     ("Aha, rozumiem.", "ǎw khâo-jai láew khráp"),
     "„khâo-jai láew” znaczy „zrozumiałem właśnie teraz”, nie „rozumiem ogólnie”. "
     "To jest dokładnie ten sygnał, o który chodzi."),

    ("paraphrase", "Parafraza dla potwierdzenia",
     "Powtórzenie własnymi słowami tego, co się zrozumiało. Jedyny sposób, żeby "
     "sprawdzić, czy się zrozumiało dobrze — a nie tylko, że się coś usłyszało.",
     ("Czy to znaczy tak?", "mǎai-khwaam wâa yàang-níi châi mǎi khráp"),
     ("Czyli tak?", "bàep-níi châi mǎi khráp"),
     "W miejsce „yàang-níi” wstawiasz to, co zrozumiałeś — choćby jednym słowem "
     "albo gestem. Formuła jest ramą; treść jest Twoja."),

    ("explain-word", "Pytanie o nieznane słowo po tajsku",
     "Pytanie zadane PO TAJSKU zostawia rozmowę w tajskim. Zapytane po angielsku "
     "zwykle ją do angielskiego przenosi — i tam już zostaje.",
     ("Co znaczy to słowo?", "kham níi plae wâa à-rai khráp"),
     ("A to co znaczy?", "an níi plae wâa à-rai khráp"),
     "Odpowiedzią bywa synonim albo gest, nie definicja. To wystarczy: "
     "chodzi o to, żeby rozmowa nie musiała się zatrzymać."),

    ("time", "Kupowanie czasu na myślenie",
     "Cisza jest w rozmowie sygnałem, że skończyłeś. Ta formuła mówi, że jeszcze "
     "nie — i kupuje kilka sekund, których potrzebujesz.",
     ("Proszę o chwilę.", "khǎw wee-laa sàk khrûu ná khráp"),
     ("Chwileczkę.", "dǐao ná khráp"),
     "„dǐao” jest bardzo częste i całkowicie neutralne. Bez niego pauza dłuższa "
     "niż dwie sekundy jest odbierana jako koniec Twojej tury."),

    ("learner", "Uprzedzenie, że dopiero się uczysz",
     "Wypowiedziane na początku zmienia całą resztę rozmowy: rozmówca sam "
     "zwolni i uprości.",
     ("Dopiero zacząłem uczyć się tajskiego.",
      "phǒm phôeng rôem rian phaa-sǎa thai khráp"),
     ("Słabo mówię po tajsku.", "phǒm phûut thai mâi kèng khráp"),
     "Powiedziane po tajsku działa odwrotnie do treści — jest odbierane jako "
     "wysiłek i zwykle spotyka się z życzliwością, nie z przejściem na angielski. "
     "Ta sama treść po angielsku kończy rozmowę po tajsku."),

    ("exit", "Grzeczne wyjście z rozmowy",
     "Czasem się nie da. Wyjście z rozmowy jest umiejętnością osobną od "
     "prowadzenia jej — i lepszą niż przeczekiwanie w milczeniu.",
     ("Przepraszam, muszę już iść.", "khǎw-thôot khráp phǒm tâwng pai láew khráp"),
     ("Już lecę, na razie.", "pai kàwn ná khráp"),
     "„pai kàwn ná” to standardowe pożegnanie przy wychodzeniu pierwszym — "
     "dosłownie „idę wcześniej”. Nie jest zdawkowe ani niegrzeczne."),
]


# --- wyzwalacze drylu -------------------------------------------------------
#
# Kwestia jest podana tak, żeby NIE dało się jej zrozumieć: za szybko, za cicho,
# w hałasie albo z nieznanym słowem. Zadanie polega na zareagowaniu właściwą
# formułą w oknie kilku sekund. Brak reakcji liczy się jako pomyłka — bo
# w rozmowie właśnie tak się liczy.

TRIGGERS = [
    ("fast", "Za szybko", "Rozmówca mówi w tempie, w którym mówi do swoich.",
     {"tempo": "fast", "rate": 1.25}, ["repeat", "slower", "not-understood"],
     "slow"),
    ("quiet", "Za cicho", "Za szybą, przez maskę albo z drugiego końca lady.",
     {"volume": 0.25}, ["repeat", "louder", "not-understood"], "natural"),
    ("noise", "W hałasie", "Ulica, restauracja albo hala dworca.",
     {"noise": 3, "tempo": "natural"}, ["repeat", "louder", "slower"], "slow"),
    ("unknown", "Nieznane słowo", "Jedno słowo w zdaniu jest spoza Twojego zasobu.",
     {"tempo": "natural"}, ["explain-word", "simpler", "not-understood"], "natural"),
    ("long", "Za długo i za zawile", "Zdanie złożone, wypowiedziane bez pauz.",
     {"tempo": "fast"}, ["simpler", "slower", "repeat"], "slow"),
    ("number", "Liczba w tempie kasjera",
     "Kwota albo godzina rzucona szybko, bez powtórzenia.",
     {"tempo": "fast", "rate": 1.25}, ["repeat", "write", "slower"], "slow"),
]


# --- lekcje -----------------------------------------------------------------
#
# Strategie ratunkowe wchodzą w pierwszych piętnastu lekcjach kursu. To nie jest
# kwestia gustu: są potrzebne od PIERWSZEJ rozmowy, a nie po roku nauki. Kto
# wyjdzie na ulicę bez nich, zawiesi się na pierwszym zdaniu i wróci przekonany,
# że nie umie nic — mimo że zna trzysta słów.

LESSON_PLAN = [
    ("res-lesson-01", "Ratunek pierwszy: powtórz i zwolnij", 2,
     ["repeat", "slower"],
     "Dwie formuły, które ratują największą część rozmów. Uczysz się ich, zanim "
     "poznasz sto słów — bo bez nich sto słów nie wystarczy."),
    ("res-lesson-02", "Nie rozumiem / już rozumiem", 5,
     ["not-understood", "understood"],
     "Para sygnałów. Pierwszy zatrzymuje rozmowę, zanim pójdzie w złą stronę; "
     "drugi ją puszcza dalej."),
    ("res-lesson-03", "Zapisz, pokaż, przeliteruj", 8,
     ["write", "show", "spell", "louder"],
     "Cztery obejścia kanału słuchowego. Gdy ucho nie daje rady, oko daje."),
    ("res-lesson-04", "Sprawdź, czy dobrze rozumiesz", 11,
     ["paraphrase", "explain-word", "simpler"],
     "Parafraza i pytanie o słowo po tajsku. Obie zostawiają rozmowę w tajskim."),
    ("res-lesson-05", "Czas, przyznanie się, wyjście", 14,
     ["time", "learner", "exit"],
     "Trzy formuły o tym, jak nie zawiesić rozmowy, gdy potrzebujesz sekundy, "
     "i jak z niej wyjść, gdy się nie da."),
]


def pick_drill_lines():
    """Kwestie dialogów, na których dryl będzie odtwarzał zniekształcony bodziec.

    Bierzemy z bazy, nie piszemy własnych: kwestia z dialogu ma pismo tajskie
    do syntezy, wariant żeński, zapis potoczny i granice wyrazów — wszystko,
    czego potrzebuje odtwarzacz, i wszystko już zwalidowane.
    """
    files = ["dialogues-part-01.json", "dialogues-part-02.json", "dialogues-part-03.json"]
    pool = []
    for fn in files:
        with open(os.path.join(DATA, fn), encoding="utf-8") as fh:
            for dlg in json.load(fh)["records"]:
                for line in dlg.get("lines", []):
                    ph = line.get("thaiPhonetic", "")
                    n = len(ph.split())
                    if n < 4 or n > 12:
                        continue
                    if not line.get("ttsThai"):
                        continue
                    pool.append({
                        "dialogueId": dlg["id"], "index": line["index"],
                        "words": n, "level": dlg.get("level", "A1"),
                        "category": dlg.get("category", ""),
                        "polish": line.get("polish", ""),
                        "numeric": has_numeral(ph),
                    })
    pool.sort(key=lambda x: (x["dialogueId"], x["index"]))
    return pool


# Dobór materiału per wyzwalacz. „Nieznane słowo” nie może stać na kwestii
# z poziomu Survival — tam uczący się zna wszystko i ćwiczenie mierzyłoby co
# innego, niż deklaruje. „Za długo” wymaga zdania, które faktycznie jest długie.
TRIGGER_PICK = {
    "unknown": {"levels": ("B1", "B2"), "minWords": 4},
    "long": {"levels": None, "minWords": 8},
    "number": {"levels": None, "minWords": 4, "numeric": True},
}

# Liczebniki, po których poznajemy kwestię z liczbą. Lista pochodzi z modułu
# liczbowego, nie jest przepisana ręcznie — inaczej rozjechałaby się przy
# pierwszej zmianie zapisu.
NUMERAL_WORDS = set([ph for ph, _ in TN.DIGITS[1:]]
                    + [ph for _v, ph, _t in TN.POSITIONS]
                    + [TN.ET[0], TN.YII[0], TN.MILLION[0]])


def has_numeral(phonetic):
    for word in (phonetic or "").split():
        for syl in word.split("-"):
            if syl in NUMERAL_WORDS:
                return True
    return False


def build_items(pool):
    """Zadania drylu: kwestia + rodzaj zniekształcenia + dystraktory do sprawdzenia.

    Po reakcji aplikacja odtwarza kwestię ponownie — wolniej albo prościej —
    i pyta, co zostało zrozumiane. Bez tego drugiego kroku dryl uczyłby
    wypowiadania formuły, a nie naprawiania rozmowy.
    """
    items = []
    per = 12
    for tid, _label, _lead, _degrade, _accept, _repeat in TRIGGERS:
        used = set()          # dedup w obrębie wyzwalacza; ta sama kwestia
        pick = TRIGGER_PICK.get(tid, {})   # w innym zniekształceniu to inne zadanie
        levels = pick.get("levels")
        min_words = pick.get("minWords", 4)
        scoped = [p for p in pool
                  if (levels is None or p["level"] in levels)
                  and p["words"] >= min_words
                  and (not pick.get("numeric") or p["numeric"])]
        if not scoped:
            scoped = pool
        local_step = max(1, len(scoped) // (per * 3))
        at = 0
        taken = 0
        while taken < per and at < len(scoped):
            cand = scoped[at]
            at += local_step
            key = (cand["dialogueId"], cand["index"])
            if key in used:
                continue
            used.add(key)
            # Dystraktory do sprawdzenia zrozumienia: polskie znaczenia innych
            # kwestii z tego samego poziomu. Z innego poziomu byłyby rozpoznawalne
            # po samej długości i złożoności zdania.
            foils = [p["polish"] for p in pool
                     if p["level"] == cand["level"] and p["polish"] != cand["polish"]]
            foils = foils[hash(key) % max(1, len(foils) - 3):][:3]
            if len(foils) < 3:
                continue
            items.append({
                "id": "res-item-%03d" % (len(items) + 1),
                "trigger": tid,
                "dialogueId": cand["dialogueId"],
                "line": cand["index"],
                "level": cand["level"],
                "check": {"answer": cand["polish"], "foils": foils},
            })
            taken += 1
    return items


def main():
    records = []
    for gid, title, why, formal, casual, note in FORMULAS:
        records.append({
            "id": "res-%s" % gid,
            "group": gid,
            "title": title,
            "why": why,
            "culturalNote": note,
            "forms": [
                node(formal[0], formal[1], "formalny"),
                node(casual[0], casual[1], "potoczny"),
            ],
        })

    pool = pick_drill_lines()
    items = build_items(pool)

    lessons_path = os.path.join(DATA, "lessons.json")
    with open(lessons_path, encoding="utf-8") as fh:
        by_number = {L["number"]: L for L in json.load(fh)["records"]}

    lessons = []
    for lid, title, after, groups, goal in LESSON_PLAN:
        anchor = by_number.get(after)
        if anchor is None:
            raise SystemExit("brak lekcji o numerze %d w ścieżce" % after)
        lessons.append({
            "id": lid, "title": title, "goal": goal,
            "anchorAfter": anchor["id"], "anchorNumber": after,
            "groups": groups,
            "pass": {"questions": len(groups) * 3,
                     "correct": max(1, int(round(0.8 * len(groups) * 3)))},
        })

    payload = {
        "file": "rescue.json",
        "generator": "tools/generators/rescue.py",
        "version": VERSION,
        "count": len(records),
        "drill": {
            # Okno reakcji. Cztery sekundy to nie jest pomiar z podręcznika,
            # tylko granica, za którą rozmówca w praktyce już mówi dalej.
            "windowMs": 4000,
            "masteryMs": 1800,
            "lead": "Kwestia jest podana tak, żeby nie dało się jej zrozumieć. "
                    "Zareaguj właściwą formułą, zanim minie okno. Brak reakcji "
                    "liczy się jak zła odpowiedź — w rozmowie też się tak liczy.",
        },
        "triggers": [
            {"id": t[0], "label": t[1], "lead": t[2], "degrade": t[3],
             "accept": t[4], "repeatTempo": t[5]} for t in TRIGGERS
        ],
        "lessons": lessons,
        "items": items,
        "records": records,
    }
    jsonio.dump(payload, os.path.join(DATA, "rescue.json"))
    print("rescue.json: %d formuł (%d form), %d wyzwalaczy, %d zadań drylu, %d lekcji"
          % (len(records), sum(len(r["forms"]) for r in records),
             len(TRIGGERS), len(items), len(lessons)))


if __name__ == "__main__":
    main()
