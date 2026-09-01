#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Walidator bazy Thai All-in-One.

Uruchomienie:  python3 tools/validate.py
Kod wyjścia 0 = baza poprawna, 1 = znaleziono błędy.

Sprawdza:
  1. duplikaty ID,
  2. brakujące pola obowiązkowe,
  3. brak tłumaczenia / fonetyki / ukrytego pola TTS,
  4. błędne odwołania w relatedWords,
  5. wyciek pisma tajskiego do pól widocznych dla użytkownika,
  6. poprawność znaków tonów w fonetyce,
  7. zgodność manifestu z faktyczną liczbą rekordów,
  8. nawrót konwencji „słowo: słowo.” w polu polish (patrz KOLON_DOZWOLONE),
  9. kompletność wariantów żeńskich (patrz KONTROLA PŁCI niżej),
 10. spójność ścieżki nauki (lessons.json) wraz z warunkiem dydaktycznym:
     żadna lekcja nie wprowadza materiału bez podstaw z lekcji wcześniejszych,
 11. zgodność indeksu wyszukiwania (search-index.json wraz z częściami
     wymienionymi w polu parts) z bazą,
 12. spójność Modułu 0 (module-zero.json): kompletność zadań, próg 90 procent,
     odwołania do bodźców, pokrycie kontrastów i zgodność bodźców z bazą,
 13. wariant potoczny (pole colloquial): brak pisma tajskiego w zapisie
     fonetycznym, zgodność z regułami redukcji i zgodność liczby sylab
     z tym, co te reguły mogły zrobić,
 14. granice wyrazów dla syntezatora (pole ttsSplit): suma długości musi się
     zgadzać z długością ukrytego pola ttsThai,
 15. sceny (scenes.json): długość 20-40 kwestii, odwołania do istniejących
     dialogów, brak powtórzeń i pominięć dialogów, poprawność klucza
     odpowiedzi i brak dwóch poprawnych odpowiedzi w jednym pytaniu,
 16. bloki ekstensywne: 3-5 minut materiału, odwołania do istniejących scen
     i pytań, komplet trzech przejść,
 17. ćwiczenia rozumienia (comprehension.json): odwołania do istniejących
     kwestii i haseł, numery wyrazów w zakresie zdania, cztery różne
     odpowiedzi i co najmniej dwie wskazówki na zdanie.
"""
import json, os, re, sys, unicodedata

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "generators"))
import gender_forms as GF
import colloquial as CO
import thai_numbers as TN
import numbers as NUMGEN          # reguła składania godziny — ta sama, którą
                                  # posłużył się generator; walidator nie ma
                                  # własnej kopii, bo dwie kopie tej samej
                                  # reguły rozjeżdżają się przy pierwszej zmianie

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
THAI = re.compile(r"[\u0E00-\u0E7F]")
TONES = set("\u0301\u0300\u0302\u030c\u0304")

REQUIRED = ["id", "type", "polish", "thaiPhonetic", "pronunciationPolish", "ttsThai",
            "syllables", "toneGuide", "category", "subcategory", "level",
            "difficulty", "frequency", "register", "tags", "examples"]
# pola, w ktorych pismo tajskie jest zabronione (widoczne dla uzytkownika)
VISIBLE = ["polish", "thaiPhonetic", "pronunciationPolish", "toneGuide", "category",
           "subcategory", "notes", "literalMeaning", "commonMistakes", "register"]

# --- kontrola dwukropka -----------------------------------------------------
# Do sesji G 2 959 rekordów (29 % bazy) miało w polu `polish` wstawkę
# słownikową w mianowniku: „Poproszę: woda”, „Szukam: apteka”. Konstrukcja
# omijała polską deklinację i uczyła zdań, których nie da się wypowiedzieć.
# Została usunięta; ta kontrola pilnuje, żeby nie wróciła.
#
# Dwukropek bywa poprawny — wprowadza cytat albo wyliczenie („Neutralnie:
# poproszę rachunek”). Dlatego zamiast zgadywać, trzymamy zamkniętą listę
# nagłówków, przy których jest dozwolony. Nowy nagłówek z dwukropkiem daje
# ostrzeżenie: albo jest błędem, albo trzeba go tu świadomie dopisać.
KOLON_DOZWOLONE = {
    "Grzecznie", "Formalnie powiesz", "Neutralnie", "Potocznie",
    "Powiem tak", "Czy dobrze rozumiem", "Proponuję kompromis",
    "I jeszcze jedno", "Zwróć uwagę na jedną rzecz", "Najpierw najważniejsze",
    "A co powiesz na taki układ", "Popatrzmy na to z innej strony",
    "Jedna rzecz do poprawy", "Mamy dwa rozwiązania do wyboru",
    "Mamy dwa rozwiązania", "Upieczemy dwie pieczenie",
    "Spotkajmy się w połowie drogi", "Muszę powiedzieć wprost",
    "Liczby mówią same za siebie",
}
kolon_hits = []

# --- KONTROLA PŁCI ----------------------------------------------------------
# W wersji 1.7.0 baza miała 7 688 rekordów z męskim khráp i dokładnie JEDEN
# zakończony żeńskim khâ. W tajskim cząstka grzecznościowa i zaimek „ja”
# zależą od płci mówiącego — to obowiązek gramatyczny, nie wariant stylu.
# Kobieta ucząca się z takiej bazy przyswaja formy, których nie może użyć.
#
# Reguła: tekst zawierający khráp albo phǒm MUSI mieć wariant żeński
# w polu genderVariant.female. Brak wariantu to błąd walidacji.
#
# Trzy wyjątki, świadome i wyliczone:
#   1. phǒm to także rzeczownik „włosy” (yaa sà phǒm — szampon). Zamiana
#      dałaby „szampon mnie”, więc te rekordy wariantu nie mają.
#   2. Kwestia dialogu wypowiadana przez rolę o płci męskiej wynikającej ze
#      scenariusza (kelner, policjant) — mężczyzna mówi khráp i tak zostaje.
#   3. Hasła, których tematem jest sama forma („ja (mężczyzna)”, „partykuła
#      grzecznościowa (kobieta)”). Generator oznacza je polem genderLexicon.
PLEC_WYJATKI = {
    "a2-home-0081",   # szampon — yaa sà phǒm
    "a2-home-0056",   # czesać się — wǐi phǒm
    "cls-062",        # klasyfikator sên, przykład „jeden włos”
}
plec_braki = []
plec_ok = 0
plec_rekordy = 0


# --- MODUŁ LICZBOWY ---------------------------------------------------------
#
# Walidacja liczebnika nie może polegać na sprawdzeniu, czy pola są wypełnione.
# Rekord „35 = sǎam-sìp-sìi” ma komplet pól i jest po prostu nieprawdziwy.
# Dlatego każdy liczebnik jest tu PRZELICZANY regułą arytmetyczną z
# tools/generators/thai_numbers.py i porównywany znak w znak — a sama reguła
# jest sprawdzana drogą powrotną: rozbiór zapisu z powrotem na liczbę,
# napisany niezależnie od składania. Błąd, który przeżyje obie kontrole,
# musiałby być popełniony dwa razy w przeciwnych kierunkach.

def check_numbers(lessons_by_id, lessons_by_number):
    """Zwraca (liczba rekordów, liczba sprawdzonych liczb, liczba nieregularności)."""
    try:
        data = load("numbers.json")
    except FileNotFoundError:
        err("brak data/numbers.json — uruchom: python3 tools/generators/numbers.py")
        return (0, 0, 0)

    atoms = data.get("atoms") or {}
    digits = atoms.get("digits") or []
    if len(digits) != 10:
        err("numbers.json: atomów cyfr jest %d, powinno być 10" % len(digits))
    for i, d in enumerate(digits):
        if d.get("value") != i:
            err("numbers.json: cyfra na pozycji %d ma value=%r" % (i, d.get("value")))
        if d.get("thaiPhonetic") != TN.DIGITS[i][0] or d.get("ttsThai") != TN.DIGITS[i][1]:
            err("numbers.json: atom cyfry %d rozjechał się z regułą" % i)
    want_pos = [(v, ph, th) for v, ph, th in TN.POSITIONS]
    got_pos = [(p.get("value"), p.get("thaiPhonetic"), p.get("ttsThai"))
               for p in atoms.get("positions") or []]
    if got_pos != want_pos:
        err("numbers.json: lista pozycji rozjechała się z regułą")
    for key, pair in (("et", TN.ET), ("yii", TN.YII), ("million", TN.MILLION)):
        a = atoms.get(key) or {}
        if a.get("thaiPhonetic") != pair[0] or a.get("ttsThai") != pair[1]:
            err("numbers.json: atom „%s” rozjechał się z regułą" % key)

    # Cały zakres, w obie strony. To jest kontrola arytmetyczna, nie próbka:
    # nieregularności skupiają się w miejscach, których próbka losowa
    # regularnie nie trafia (11-19, dziesiątki, jedność po setce).
    checked = 0
    bad_read, bad_parse = [], []
    for n in range(0, TN.MAX + 1):
        ph = TN.phonetic(n)
        if TN.parse(ph) != n:
            bad_parse.append(n)
            if len(bad_parse) > 5:
                break
        checked += 1
    if bad_parse:
        err("numbers.json: rozbiór nie odtwarza wartości dla %d liczb, np. %s"
            % (len(bad_parse), bad_parse[:5]))

    # Twarde punkty, które muszą wyjść dokładnie tak, a nie inaczej. Gdyby
    # reguła i jej rozbiór pomyliły się zgodnie, ta lista i tak by to złapała.
    KNOWN = {0: "sǔun", 1: "nùeng", 10: "sìp", 11: "sìp-èt", 12: "sìp-sǎwng",
             20: "yîi-sìp", 21: "yîi-sìp-èt", 30: "sǎam-sìp", 100: "nùeng-ráwy",
             101: "nùeng-ráwy-èt", 105: "nùeng-ráwy-hâa",
             111: "nùeng-ráwy-sìp-èt", 1000: "nùeng-phan",
             10000: "nùeng-mùen", 100000: "nùeng-sǎen", 1000000: "nùeng-láan"}
    for n, want in KNOWN.items():
        if TN.phonetic(n) != want:
            err("numbers.json: %d czyta się „%s”, reguła daje „%s”"
                % (n, want, TN.phonetic(n)))

    for cp in data.get("checkpoints") or []:
        n = cp.get("n")
        if not isinstance(n, int):
            err("numbers.json: punkt kontrolny bez liczby")
            continue
        if cp.get("thaiPhonetic") != TN.phonetic(n):
            err("numbers.json: punkt kontrolny %d ma „%s”, reguła daje „%s”"
                % (n, cp.get("thaiPhonetic"), TN.phonetic(n)))
        if sorted(cp.get("irregular") or []) != TN.irregular_kinds(n):
            err("numbers.json: punkt kontrolny %d ma źle opisane nieregularności" % n)

    irr_ids = {i.get("id") for i in data.get("irregularities") or []}
    missing = set(TN.IRREGULAR_LABELS) - irr_ids
    if missing:
        err("numbers.json: nieopisane nieregularności: %s" % ", ".join(sorted(missing)))

    section_ids = {s.get("id") for s in data.get("sections") or []}
    drill_ids = {d.get("id") for d in data.get("drills") or []}
    for d in data.get("drills") or []:
        if not isinstance(d.get("limitMs"), int) or d["limitMs"] <= 0:
            err("numbers.json: ćwiczenie %s bez sensownego limitu czasu" % d.get("id"))
        if not isinstance(d.get("masteryMs"), int) or d["masteryMs"] >= d.get("limitMs", 0):
            err("numbers.json: ćwiczenie %s — próg opanowania musi być krótszy "
                "niż limit, inaczej limit odcinałby odpowiedzi uznane za dobre"
                % d.get("id"))

    rec_ids = set()
    for r in data.get("records") or []:
        rid = r.get("id", "<brak id>")
        if rid in rec_ids:
            err("numbers.json: zduplikowane ID %s" % rid)
        rec_ids.add(rid)
        if r.get("section") not in section_ids:
            err("%s: nieznana sekcja %r" % (rid, r.get("section")))
        if not r.get("ttsThai") or not THAI.search(r["ttsThai"]):
            err("%s: pole ttsThai nie zawiera pisma tajskiego" % rid)
        check_visible(rid, r)
        check_plec(rid, r, "moduł liczbowy")
        check_potoczny(rid, r, "moduł liczbowy")
        check_split(rid, r, "moduł liczbowy")
        fem = (r.get("genderVariant") or {}).get("female")
        if fem:
            check_split(rid, fem, "moduł liczbowy, forma żeńska")

        meta = r.get("meta") or {}
        # Liczebnik jako taki: cały zapis musi wyjść z reguły.
        if meta.get("kind") == "cardinal":
            n = meta.get("value")
            if TN.phonetic(n) != r.get("thaiPhonetic"):
                err("%s: liczebnik %s zapisany „%s”, reguła daje „%s”"
                    % (rid, n, r.get("thaiPhonetic"), TN.phonetic(n)))
            if TN.thai(n) != r.get("ttsThai"):
                err("%s: pismo liczebnika %s nie zgadza się z regułą" % (rid, n))
        # Liczba w otoczeniu jednostki: pierwszy wyraz musi się rozebrać
        # na deklarowaną wartość.
        elif isinstance(meta.get("value"), int) and meta.get("kind") in ("price", "quantity"):
            head = (r.get("thaiPhonetic") or "").split(" ")[0]
            got = TN.parse(head)
            if meta.get("unit") == "baht-satang" or meta.get("unit") == "salueng":
                pass          # kwoty złożone mają własną budowę
            elif meta.get("kind") == "quantity" and meta.get("value") == 1:
                got = TN.parse((r.get("thaiPhonetic") or "").split(" ")[-1])
                if got != 1:
                    err("%s: „jeden” po klasyfikatorze nie rozbiera się na 1" % rid)
            elif got != meta["value"]:
                err("%s: zapis „%s” rozbiera się na %r, a deklaruje %r"
                    % (rid, head, got, meta["value"]))
        # Godzina: przeliczana tą samą regułą, którą złożył generator.
        elif meta.get("kind") == "clock":
            formal = meta.get("style") == "formal"
            want = NUMGEN.clock_words(meta["hour"], meta.get("minute", 0), formal=formal)
            want_ph = " ".join(w[0] for w in want)
            if want_ph != r.get("thaiPhonetic"):
                err("%s: godzina %02d:%02d zapisana „%s”, reguła daje „%s”"
                    % (rid, meta["hour"], meta.get("minute", 0),
                       r.get("thaiPhonetic"), want_ph))
        elif meta.get("kind") == "year":
            if meta.get("era") == "BE" and meta.get("be") != meta.get("ce") + 543:
                err("%s: rok buddyjski nie jest gregoriańskim plus 543" % rid)

    # Lekcje: rozłożone wzdłuż ścieżki, nie zwalone w jeden blok.
    prev = 0
    for L in data.get("lessons") or []:
        lid = L.get("id", "<brak id>")
        anchor = L.get("anchorAfter")
        if anchor not in lessons_by_id:
            err("%s: kotwica %r nie wskazuje na żadną lekcję ścieżki" % (lid, anchor))
        elif lessons_by_id[anchor].get("number") != L.get("anchorNumber"):
            err("%s: anchorNumber (%r) nie zgadza się z numerem lekcji %s"
                % (lid, L.get("anchorNumber"), anchor))
        if L.get("anchorNumber", 0) <= prev:
            err("%s: moduł liczbowy cofa się na ścieżce (po lekcji %r, poprzedni po %d)"
                % (lid, L.get("anchorNumber"), prev))
        prev = L.get("anchorNumber", prev)
        for d in L.get("drills") or []:
            if d not in drill_ids:
                err("%s: nieznane ćwiczenie %r" % (lid, d))
        for iid in L.get("itemIds") or []:
            if iid not in rec_ids:
                err("%s: odwołanie do nieistniejącego rekordu %s" % (lid, iid))
        p = L.get("pass") or {}
        if p.get("correct", 0) > p.get("questions", 0):
            err("%s: próg zaliczenia wyższy niż liczba pytań" % lid)
    firsts = [L.get("anchorNumber") for L in data.get("lessons") or []]
    if firsts and firsts[0] > 15:
        err("numbers.json: podstawy liczbowe wchodzą dopiero po lekcji %d — "
            "bez cyfr nie da się zrobić zakupów, więc muszą być wcześnie" % firsts[0])
    if firsts and max(firsts) - min(firsts) < 50:
        err("numbers.json: cały moduł liczbowy mieści się w %d lekcjach — "
            "miał być rozłożony wzdłuż ścieżki" % (max(firsts) - min(firsts)))

    # Sceny: pytanie musi dotyczyć KONKRETNEJ WARTOŚCI.
    for sc in data.get("scenes") or []:
        sid = sc.get("id", "<brak id>")
        lines = sc.get("lines") or []
        if len(lines) < 4:
            err("%s: scena krótsza niż cztery kwestie" % sid)
        for i, ln in enumerate(lines, start=1):
            if ln.get("index") != i:
                err("%s: numeracja kwestii nie jest ciągła (pozycja %d)" % (sid, i))
            if ln.get("role") not in ("A", "B"):
                err("%s: kwestia %d ma rolę %r spoza {A, B}" % (sid, i, ln.get("role")))
            if not ln.get("ttsThai"):
                err("%s: kwestia %d bez danych dla syntezatora" % (sid, i))
            check_visible(sid, ln)
            check_plec(sid, ln, "scena liczbowa, kwestia %d" % i, dialog_line=True)
            check_potoczny(sid, ln, "scena liczbowa, kwestia %d" % i)
            check_split(sid, ln, "scena liczbowa, kwestia %d" % i)
        qs = sc.get("questions") or []
        if not qs:
            err("%s: scena bez pytań kontrolnych" % sid)
        for q in qs:
            opts = q.get("options") or []
            if len(opts) < 3:
                err("%s: pytanie %s ma mniej niż trzy opcje" % (sid, q.get("id")))
            if not isinstance(q.get("answer"), int) or not (0 <= q["answer"] < len(opts)):
                err("%s: pytanie %s ma odpowiedź poza listą opcji" % (sid, q.get("id")))
            if len(set(opts)) != len(opts):
                err("%s: pytanie %s ma powtórzone opcje" % (sid, q.get("id")))
            if "value" not in q:
                err("%s: pytanie %s nie pyta o konkretną wartość — sceny liczbowe "
                    "mają sprawdzać liczbę, nie ogólny sens" % (sid, q.get("id")))
            if not q.get("explain"):
                err("%s: pytanie %s bez wyjaśnienia po odpowiedzi" % (sid, q.get("id")))

    return (len(data.get("records") or []), checked, len(irr_ids))


# --- MODUŁ RATUNKOWY --------------------------------------------------------

def check_rescue(lessons_by_id, dialogues_by_id):
    try:
        data = load("rescue.json")
    except FileNotFoundError:
        err("brak data/rescue.json — uruchom: python3 tools/generators/rescue.py")
        return (0, 0, 0)

    groups = set()
    forms_total = 0
    female_total = 0
    for r in data.get("records") or []:
        rid = r.get("id", "<brak id>")
        gid = r.get("group")
        if gid in groups:
            err("rescue.json: zduplikowana grupa %r" % gid)
        groups.add(gid)
        if not r.get("culturalNote"):
            err("%s: formuła bez notatki kulturowej — bez niej uczący się nie wie, "
                "kiedy który rejestr jest właściwy" % rid)
        regs = [f.get("register") for f in r.get("forms") or []]
        if sorted(regs) != ["formalny", "potoczny"]:
            err("%s: formuła musi mieć dokładnie dwa rejestry (formalny, potoczny), "
                "ma: %s" % (rid, regs))
        for f in r.get("forms") or []:
            forms_total += 1
            where = "formuła %s, rejestr %s" % (gid, f.get("register"))
            if not f.get("ttsThai") or not THAI.search(f["ttsThai"]):
                err("%s: %s bez pisma tajskiego do syntezy" % (rid, where))
            check_visible(rid, f)
            check_plec(rid, f, where)
            check_potoczny(rid, f, where)
            check_split(rid, f, where)
            fem = (f.get("genderVariant") or {}).get("female")
            if fem:
                female_total += 1
                check_split(rid, fem, where + ", forma żeńska")
            else:
                err("%s: %s bez wariantu żeńskiego — formuła ratunkowa musi dać się "
                    "wypowiedzieć obu płciom" % (rid, where))

    trig_ids = set()
    for t in data.get("triggers") or []:
        trig_ids.add(t.get("id"))
        for g in t.get("accept") or []:
            if g not in groups:
                err("rescue.json: wyzwalacz %s przyjmuje nieznaną formułę %r"
                    % (t.get("id"), g))
        if not t.get("accept"):
            err("rescue.json: wyzwalacz %s nie przyjmuje żadnej formuły" % t.get("id"))
        if t.get("repeatTempo") not in ("slow", "natural", "fast"):
            err("rescue.json: wyzwalacz %s ma nieznane tempo powtórzenia %r"
                % (t.get("id"), t.get("repeatTempo")))

    for it in data.get("items") or []:
        iid = it.get("id")
        if it.get("trigger") not in trig_ids:
            err("%s: nieznany wyzwalacz %r" % (iid, it.get("trigger")))
        dlg = dialogues_by_id.get(it.get("dialogueId"))
        if not dlg:
            err("%s: odwołanie do nieistniejącego dialogu %r" % (iid, it.get("dialogueId")))
            continue
        line = None
        for ln in dlg.get("lines") or []:
            if ln.get("index") == it.get("line"):
                line = ln
        if line is None:
            err("%s: dialog %s nie ma kwestii %r" % (iid, dlg["id"], it.get("line")))
            continue
        check = it.get("check") or {}
        if check.get("answer") != line.get("polish"):
            err("%s: klucz odpowiedzi nie zgadza się z treścią kwestii" % iid)
        foils = check.get("foils") or []
        if len(foils) < 3:
            err("%s: mniej niż trzy dystraktory" % iid)
        if check.get("answer") in foils or len(set(foils)) != len(foils):
            err("%s: dystraktor powtarza poprawną odpowiedź albo sam siebie" % iid)

    # Strategie ratunkowe MUSZĄ wejść wcześnie. Są potrzebne od pierwszej
    # rozmowy, a nie po roku — kto wyjdzie na ulicę bez nich, zawiesi się
    # na pierwszym zdaniu i wróci przekonany, że nie umie nic.
    EARLY = 15
    for L in data.get("lessons") or []:
        lid = L.get("id")
        if L.get("anchorAfter") not in lessons_by_id:
            err("%s: kotwica %r nie wskazuje na żadną lekcję ścieżki"
                % (lid, L.get("anchorAfter")))
        elif lessons_by_id[L["anchorAfter"]].get("number") != L.get("anchorNumber"):
            err("%s: anchorNumber nie zgadza się z numerem lekcji" % lid)
        if L.get("anchorNumber", 999) > EARLY:
            err("%s: strategia ratunkowa wchodzi po lekcji %r — miała wejść "
                "w pierwszych %d lekcjach" % (lid, L.get("anchorNumber"), EARLY))
        for g in L.get("groups") or []:
            if g not in groups:
                err("%s: nieznana formuła %r" % (lid, g))

    covered = set()
    for L in data.get("lessons") or []:
        covered.update(L.get("groups") or [])
    orphan = groups - covered
    if orphan:
        err("rescue.json: formuły spoza jakiejkolwiek lekcji: %s"
            % ", ".join(sorted(orphan)))

    return (len(data.get("records") or []), forms_total, female_total)


def check_colon(rid, text, where):
    """Ostrzega przed wzorcem „słowo: słowo.” w tekście widzianym przez uczącego się."""
    if ":" not in text:
        return
    head = text.split(":", 1)[0].strip()
    if head in KOLON_DOZWOLONE:
        return
    kolon_hits.append((rid, where, text))


errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as f:
        return json.load(f)


def check_plec(rid, node, where, dialog_line=False):
    """Pilnuje, żeby każda forma męska miała odpowiednik żeński."""
    global plec_ok
    if rid in PLEC_WYJATKI or node.get("genderLexicon"):
        return
    text = node.get("thaiPhonetic", "")
    if not GF.has_male_form(text):
        return
    # „phǒm” bywa rzeczownikiem „włosy”, nie zaimkiem: „thîi pào phǒm”
    # (suszarka), „ráan tàt phǒm” (fryzjer), „yaa sà phǒm” (szampon).
    # has_male_form widzi sam ciąg znaków, plan() rozstrzyga rolę wyrazu —
    # jeżeli plan nie ma czego zamienić, hasło nie zależy od płci mówiącego
    # i wariantu żeńskiego mieć nie może.
    if GF.plan(text, node.get("polish", ""),
               node.get("register", "neutralny")) is None:
        return
    if dialog_line and node.get("speakerGender") == "male":
        return          # scenariusz przesądza — mówi mężczyzna
    variant = (node.get("genderVariant") or {}).get("female")
    if not variant:
        plec_braki.append((rid, where, text))
        err("%s: forma zależna od płci bez wariantu żeńskiego (%s) — %s"
            % (rid, where, text))
        return
    if not variant.get("thaiPhonetic"):
        err("%s: genderVariant.female bez fonetyki (%s)" % (rid, where))
        return
    # W wariancie żeńskim nie może zostać nic do zamiany. Pytamy o to tym samym
    # kodem, który generuje warianty, więc „phǒm” w znaczeniu „włosy”
    # (chǎn yàak tàt phǒm khâ — chcę obciąć włosy) nie jest tu błędem.
    if GF.plan(variant["thaiPhonetic"], node.get("polish", ""), "neutralny"):
        err("%s: wariant żeński wciąż zawiera formę męską (%s) — %s"
            % (rid, where, variant["thaiPhonetic"]))
        return
    if node.get("ttsThai") and not variant.get("ttsThai"):
        err("%s: wariant żeński bez danych TTS (%s)" % (rid, where))
        return
    plec_ok += 1



# --- KONTROLA WARIANTU POTOCZNEGO -------------------------------------------
# Pole colloquial jest generowane regułami z tools/generators/colloquial.py.
# Walidator NIE sprawdza go „mniej więcej”: przelicza wariant od nowa tym samym
# kodem i porównuje znak w znak. Ręczna poprawka w danych zostanie wykryta —
# tak samo jak rozjazd po zmianie reguł bez ponownego uruchomienia generatora.
colloquial_ok = 0
colloquial_rules = {}


def check_potoczny(rid, node, where):
    global colloquial_ok
    coll = node.get("colloquial")
    if not coll:
        return
    ph = node.get("thaiPhonetic", "")
    got = coll.get("thaiPhonetic", "")
    if not got:
        err("%s: wariant potoczny bez zapisu fonetycznego (%s)" % (rid, where))
        return
    if THAI.search(got):
        err("%s: pismo tajskie w zapisie potocznym (%s)" % (rid, where))
        return

    want, rules = CO.reduce_phonetic(ph)
    if got != want:
        err("%s: wariant potoczny niezgodny z regułami (%s) — jest „%s”, "
            "z reguł wychodzi „%s”" % (rid, where, got, want))
        return
    if list(coll.get("rules") or []) != rules:
        err("%s: lista reguł nie zgadza się z przekształceniem (%s)" % (rid, where))
        return
    for r in rules:
        if r not in CO.RULE_IDS:
            err("%s: nieznana reguła redukcji „%s” (%s)" % (rid, r, where))
            return

    # Liczba sylab może wyłącznie zmaleć, i to tylko wtedy, gdy zadziałała
    # reguła zdejmująca sylabę. Reguły czysto brzmieniowe (skrócenie
    # samogłoski, spłaszczenie tonu, uproszczenie zbitki) sylab nie ruszają —
    # gdyby liczba spadła bez „lex”, znaczyłoby to, że przekształcenie zgubiło
    # kawałek wyrazu.
    before, after = CO.syllable_count(ph), CO.syllable_count(got)
    if after > before:
        err("%s: wariant potoczny ma WIĘCEJ sylab niż słownikowy (%s): %d > %d"
            % (rid, where, after, before))
        return
    if after < before and "lex" not in rules:
        err("%s: ubyło sylab (%d -> %d) bez reguły zdejmującej sylabę (%s)"
            % (rid, before, after, where))
        return
    if node.get("ttsThai") and not coll.get("ttsThai"):
        err("%s: wariant potoczny bez danych TTS (%s)" % (rid, where))
        return

    colloquial_ok += 1
    for r in rules:
        colloquial_rules[r] = colloquial_rules.get(r, 0) + 1


def check_split(rid, node, where):
    """Granice wyrazów: same długości, muszą pokryć ukryty tekst co do znaku."""
    for holder, label in ((node, where),
                          (node.get("colloquial") or {}, where + ", wariant potoczny")):
        split = holder.get("ttsSplit")
        if split is None:
            continue
        thai = holder.get("ttsThai") or ""
        if not thai:
            err("%s: ttsSplit bez pola ttsThai (%s)" % (rid, label))
            continue
        if not isinstance(split, list) or not all(isinstance(n, int) and n > 0 for n in split):
            err("%s: ttsSplit musi być listą liczb dodatnich (%s)" % (rid, label))
            continue
        if sum(split) != len(thai.replace(" ", "")):
            err("%s: suma długości ttsSplit (%d) != długość tekstu TTS (%d) (%s)"
                % (rid, sum(split), len(thai.replace(" ", "")), label))


def check_visible(rid, obj, path=""):
    for k, v in obj.items():
        if k == "ttsThai":
            continue
        if isinstance(v, str) and THAI.search(v):
            err("%s: pismo tajskie w widocznym polu %s%s" % (rid, path, k))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    check_visible(rid, item, "%s%s[%d]." % (path, k, i))
                elif isinstance(item, str) and THAI.search(item):
                    err("%s: pismo tajskie w widocznym polu %s%s[%d]" % (rid, path, k, i))
        elif isinstance(v, dict):
            check_visible(rid, v, "%s%s." % (path, k))


def check_grammar_modes(lessons):
    """Trzy tryby gramatyczne: struktura ze słuchu, transformacje, partykuły.

    Każdy z tych plików ma tę samą własność co korpus pokrycia: rozjechany
    nadal pokazywałby ładne zadania, tylko z błędnym kluczem odpowiedzi.
    Zadanie z dwiema poprawnymi odpowiedziami jest gorsze niż brak zadania,
    bo uczy nieufności do ćwiczenia zamiast języka.
    """
    total = len(lessons) or 1

    # --- wykrywanie struktury ze słuchu
    gl = load("grammar-listening.json")
    axes = gl.get("axes") or {}
    intents = {a["id"] for a in axes.get("intent", [])}
    times = {a["id"] for a in axes.get("time", [])}
    if not intents or not times:
        err("grammar-listening.json: brak opisu osi (intent, time)")
    for a in axes.get("intent", []) + axes.get("time", []):
        if not a.get("why"):
            err("grammar-listening.json: oś %s bez wyjaśnienia" % a.get("id"))

    rows = gl["records"]
    if gl.get("count") != len(rows):
        err("grammar-listening.json: count (%s) != liczba zadań (%d)"
            % (gl.get("count"), len(rows)))
    seen = set()
    for r in rows:
        rid = r.get("id", "<brak id>")
        if rid in seen:
            err("%s: zduplikowane zadanie struktury" % rid)
        seen.add(rid)
        if r.get("intent") not in intents:
            err("%s: nieznana intencja %s" % (rid, r.get("intent")))
        if r.get("time") not in times:
            err("%s: nieznany czas %s" % (rid, r.get("time")))
        if not r.get("ttsThai") or not THAI.search(r.get("ttsThai", "")):
            err("%s: zadanie bez pisma tajskiego — nieodtwarzalne" % rid)
        av = r.get("availableFrom")
        if not isinstance(av, int) or not 1 <= av <= total:
            err("%s: availableFrom=%s poza zakresem 1-%d" % (rid, av, total))
    check_visible("grammar-listening.json", gl)

    # --- transformacje
    gt = load("grammar-transform.json")
    kinds = {t["id"]: t for t in gt.get("transforms", [])}
    if not kinds:
        err("grammar-transform.json: brak opisu przekształceń")
    for t in gt.get("transforms", []):
        for f in ("title", "instruction", "rule", "marker", "position"):
            if not t.get(f):
                err("grammar-transform.json: przekształcenie %s bez pola %s"
                    % (t.get("id"), f))
        if t.get("position") not in ("koniec", "przed czasownikiem"):
            err("grammar-transform.json: %s ma nieznaną pozycję %s"
                % (t.get("id"), t.get("position")))

    rows = gt["records"]
    if gt.get("count") != len(rows):
        err("grammar-transform.json: count (%s) != liczba zadań (%d)"
            % (gt.get("count"), len(rows)))
    seen = set()
    for r in rows:
        rid = r.get("id", "<brak id>")
        if rid in seen:
            err("%s: zduplikowane zadanie transformacji" % rid)
        seen.add(rid)
        kind = kinds.get(r.get("transform"))
        if not kind:
            err("%s: nieznane przekształcenie %s" % (rid, r.get("transform")))
            continue
        check = r.get("check") or {}
        if check.get("marker") != kind["marker"]:
            err("%s: marker w zadaniu (%s) nie zgadza się z opisem "
                "przekształcenia (%s)" % (rid, check.get("marker"),
                                          kind["marker"]))
        if check.get("position") != kind["position"]:
            err("%s: pozycja w zadaniu nie zgadza się z opisem" % rid)

        src = r.get("thaiPhonetic") or ""
        model = r.get("model") or ""
        if not src or not model:
            err("%s: zadanie bez zdania wyjściowego albo wzorca" % rid)
            continue

        # Zdanie wyjściowe NIE MOŻE już zawierać markera — inaczej polecenie
        # każe dołożyć coś, co tam stoi, i każda odpowiedź jest zła.
        marker = check.get("marker")
        if re.search(r"(?:^|[ ])" + re.escape(marker) + r"(?:$|[ ])", src):
            err("%s: zdanie wyjściowe zawiera już `%s` — nie ma czego "
                "przekształcać" % (rid, marker))

        # Wzorzec musi zawierać marker i cały trzon zdania wyjściowego.
        if not re.search(r"(?:^|[ ])" + re.escape(marker) + r"(?:$|[ ])",
                         model):
            err("%s: wzorzec nie zawiera markera `%s`" % (rid, marker))
        keep = check.get("keep") or []
        mwords = model.split()
        for k in keep:
            if k not in mwords:
                err("%s: wzorzec zgubił wyraz trzonu `%s`" % (rid, k))
                break

        # Wzorzec różni się od wyjścia dokładnie o jeden wyraz.
        if len(mwords) != len(src.split()) + 1:
            err("%s: wzorzec różni się od zdania wyjściowego o %d wyrazów, "
                "a przekształcenie dokłada dokładnie jeden"
                % (rid, len(mwords) - len(src.split())))

        av = r.get("availableFrom")
        if not isinstance(av, int) or not 1 <= av <= total:
            err("%s: availableFrom=%s poza zakresem 1-%d" % (rid, av, total))
    check_visible("grammar-transform.json", gt)

    # --- partykuły końcowe
    pa = load("particles.json")
    rows = pa["records"]
    if pa.get("count") != len(rows):
        err("particles.json: count (%s) != liczba partykuł (%d)"
            % (pa.get("count"), len(rows)))
    ids = set()
    for p in rows:
        pid = p.get("id", "<brak id>")
        if pid in ids:
            err("%s: zduplikowana partykuła" % pid)
        ids.add(pid)
        for f in ("particle", "gloss", "meaning", "effect", "missing",
                  "register"):
            if not p.get(f):
                err("%s: partykuła bez pola %s" % (pid, f))
        if not p.get("examples"):
            err("%s: partykuła bez przykładu użycia — to definicja, nie nauka"
                % pid)
        for ex in p.get("examples") or []:
            if not ex.get("ttsThai") or not THAI.search(ex.get("ttsThai", "")):
                err("%s: przykład bez pisma tajskiego" % pid)

    for ex in pa.get("exercises") or []:
        eid = ex.get("id", "<brak id>")
        opts = [o.get("id") for o in ex.get("options") or []]
        if len(opts) < 3:
            err("%s: ćwiczenie ma mniej niż trzy opcje" % eid)
        if len(set(opts)) != len(opts):
            err("%s: powtórzona opcja w ćwiczeniu" % eid)
        for o in opts:
            if o not in ids:
                err("%s: opcja wskazuje na nieznaną partykułę %s" % (eid, o))
        if ex.get("answer") not in opts:
            err("%s: poprawnej odpowiedzi nie ma wśród opcji" % eid)
        if not ex.get("situation") or not ex.get("why"):
            err("%s: ćwiczenie bez sytuacji albo bez uzasadnienia" % eid)
    check_visible("particles.json", pa)


def main():
    manifest = load("manifest.json")
    vocab_files = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "vocabulary"]
    dialog_files = [f["file"] for f in manifest["dataFiles"] if f["kind"] == "dialogues"]

    all_ids, records = set(), []
    counts = {}

    for fn in vocab_files:
        data = load(fn)
        counts[fn] = len(data["records"])
        if data.get("count") != len(data["records"]):
            err("%s: pole count (%s) != liczba rekordów (%d)" % (fn, data.get("count"), len(data["records"])))
        for r in data["records"]:
            rid = r.get("id", "<brak id>")
            if rid in all_ids:
                err("%s: zduplikowane ID w pliku %s" % (rid, fn))
            all_ids.add(rid)
            for field in REQUIRED:
                if field not in r:
                    err("%s: brak pola %s" % (rid, field))
                elif r[field] in ("", [], None):
                    err("%s: puste pole obowiązkowe %s" % (rid, field))
            if not r.get("ttsThai") or not THAI.search(r.get("ttsThai", "")):
                err("%s: pole ttsThai nie zawiera pisma tajskiego" % rid)
            if not r.get("examples"):
                err("%s: brak przykładu użycia" % rid)
            for ex in r.get("examples", []):
                for field in ("polish", "thaiPhonetic", "ttsThai"):
                    if not ex.get(field):
                        err("%s: przykład bez pola %s" % (rid, field))
            d = unicodedata.normalize("NFD", r.get("thaiPhonetic", ""))
            bad = [c for c in d if unicodedata.combining(c) and c not in TONES]
            if bad:
                err("%s: nieznany znak diakrytyczny w fonetyce" % rid)
            if r.get("difficulty") not in range(1, 6):
                err("%s: difficulty poza zakresem 1-5" % rid)
            if r.get("frequency") not in range(1, 6):
                err("%s: frequency poza zakresem 1-5" % rid)
            check_visible(rid, r)
            check_plec(rid, r, "hasło")
            check_potoczny(rid, r, "hasło")
            check_split(rid, r, "hasło")
            fem = (r.get("genderVariant") or {}).get("female")
            if fem:
                check_potoczny(rid, dict(fem, polish=r.get("polish", "")), "hasło, forma żeńska")
                check_split(rid, fem, "hasło, forma żeńska")
            for i, ex in enumerate(r.get("examples", [])):
                check_potoczny(rid, ex, "przykład %d" % (i + 1))
                check_split(rid, ex, "przykład %d" % (i + 1))
                exf = (ex.get("genderVariant") or {}).get("female")
                if exf:
                    check_potoczny(rid, exf, "przykład %d, forma żeńska" % (i + 1))
                    check_split(rid, exf, "przykład %d, forma żeńska" % (i + 1))
            if not r.get("genderLexicon"):
                for i, ex in enumerate(r.get("examples", [])):
                    check_plec(rid, ex, "przykład %d" % (i + 1))
            check_colon(rid, r.get("polish", ""), "polish")
            for alt in r.get("polishAlternatives", []):
                check_colon(rid, alt, "polishAlternatives")
            for ex in r.get("examples", []):
                check_colon(rid, ex.get("polish", ""), "examples")
            records.append(r)

    # --- duplikaty haseł (audyt sesji V, kontrola od sesji VII) -----------
    #
    # Sesja V zgłosiła 13 „duplikatów”. Przegląd rekord po rekordzie pokazał,
    # że kryterium było za grube: cztery z pięciu powtórzonych fonetyk to
    # HOMONIMY o różnym piśmie tajskim (ส้อม widelec / ซ่อม naprawiać,
    # เหล้า alkohol / เล่า opowiadać, แต่ ale / แตะ dotykać, หญ้า trawa /
    # ย่า babcia). Skasowanie ich wycięłoby z bazy prawdziwe słowa.
    #
    # Kontrola pilnuje więc tego, co jest faktycznie błędem, w trzech
    # osobnych regułach:
    #
    #   1. ta sama glosa polska I to samo pismo tajskie — to jeden i ten sam
    #      wpis dwa razy; zawsze błąd,
    #   2. ta sama glosa polska przy różnym piśmie — dopuszczalne tylko wtedy,
    #      gdy rekordy różnią się rejestrem; inaczej w słowniku stoją obok
    #      siebie dwa nierozróżnialne hasła,
    #   3. ta sama fonetyka przy różnym piśmie — homonim, rzecz normalna
    #      w tajskim, ale wymaga różnych glos polskich, żeby uczący się
    #      wiedział, o które słowo chodzi (aplikacja nie pokazuje pisma).
    by_pair, by_polish, by_phon = {}, {}, {}
    for r in records:
        pl = (r.get("polish") or "").strip().lower()
        tts = (r.get("ttsThai") or "").strip()
        ph = (r.get("thaiPhonetic") or "").strip().lower()
        by_pair.setdefault((pl, tts), []).append(r)
        by_polish.setdefault(pl, []).append(r)
        by_phon.setdefault(ph, []).append(r)

    for (pl, tts), group in sorted(by_pair.items()):
        if pl and len(group) > 1:
            err("duplikat hasła — ta sama glosa i to samo pismo tajskie: %s (%s)"
                % (", ".join(x["id"] for x in group), pl[:40]))

    def gender_pair(group):
        """Czy to ta sama wypowiedź w formie męskiej i żeńskiej.

        Kurs uczy zaimków „phǒm" i „chǎn" na osobnych zdaniach, mimo że
        forma żeńska siedzi też w genderVariant.female formy męskiej.
        Taka para ma prawo mieć wspólną glosę — rozróżnia je płeć
        mówiącego, nie rejestr."""
        scripts = set((x.get("ttsThai") or "").strip() for x in group)
        for x in group:
            fem = ((x.get("genderVariant") or {}).get("female") or {})
            fem_tts = (fem.get("ttsThai") or "").strip()
            if fem_tts and fem_tts in scripts - {(x.get("ttsThai") or "").strip()}:
                return True
        return False

    for pl, group in sorted(by_polish.items()):
        if not pl or len(group) < 2:
            continue
        if gender_pair(group):
            continue
        regs = [(x.get("register") or "") for x in group]
        if len(set(regs)) < len(regs) or "" in regs:
            err("nierozróżnialne hasła o tej samej glosie „%s”: %s "
                "— rekordy o wspólnej glosie muszą różnić się rejestrem"
                % (pl[:40], ", ".join("%s (%s)" % (x["id"], x.get("register") or "brak")
                                      for x in group)))

    for ph, group in sorted(by_phon.items()):
        if not ph or len(group) < 2:
            continue
        scripts = set((x.get("ttsThai") or "").strip() for x in group)
        if len(scripts) < len(group):
            err("duplikat fonetyki bez różnicy w piśmie tajskim: %s (%s)"
                % (", ".join(x["id"] for x in group), ph[:40]))
        glosses = [(x.get("polish") or "").strip().lower() for x in group]
        if len(set(glosses)) < len(glosses):
            err("homonim „%s” z powtórzoną glosą polską: %s — aplikacja nie "
                "pokazuje pisma tajskiego, więc glosy muszą się różnić"
                % (ph[:40], ", ".join(x["id"] for x in group)))

    # odwolania
    for r in records:
        for ref in r.get("relatedWords", []):
            if ref not in all_ids:
                err("%s: relatedWords wskazuje na nieistniejące ID %s" % (r["id"], ref))

    # dialogi
    dlg_ids = set()
    for fn in dialog_files:
        data = load(fn)
        counts[fn] = len(data["records"])
        for d in data["records"]:
            did = d.get("id", "<brak id>")
            if did in dlg_ids:
                err("%s: zduplikowane ID dialogu" % did)
            dlg_ids.add(did)
            if not 4 <= len(d.get("lines", [])) <= 16:
                err("%s: dialog ma %d kwestii (dozwolone 4-16)" % (did, len(d.get("lines", []))))
            for ln in d.get("lines", []):
                if not ln.get("polish") or not ln.get("thaiPhonetic"):
                    err("%s: kwestia bez tłumaczenia lub fonetyki" % did)
                if not THAI.search(ln.get("ttsThai", "")):
                    err("%s: kwestia bez danych TTS" % did)
                if ln.get("role") not in ("A", "B"):
                    err("%s: nieznana rola %s" % (did, ln.get("role")))
                if ln.get("speakerGender") not in ("any", "female", "male"):
                    err("%s: kwestia %s bez oznaczenia płci mówiącego"
                        % (did, ln.get("index")))
                check_plec(did, ln, "kwestia %s" % ln.get("index"), dialog_line=True)
                check_potoczny(did, ln, "kwestia %s" % ln.get("index"))
                check_split(did, ln, "kwestia %s" % ln.get("index"))
                lnf = (ln.get("genderVariant") or {}).get("female")
                if lnf:
                    check_potoczny(did, lnf, "kwestia %s, forma żeńska" % ln.get("index"))
                    check_split(did, lnf, "kwestia %s, forma żeńska" % ln.get("index"))
                check_colon(did, ln.get("polish", ""), "lines")
            if not isinstance(d.get("roleGender"), dict):
                err("%s: dialog bez pola roleGender" % did)
            else:
                for k in d.get("roles", {}):
                    if d["roleGender"].get(k) not in ("any", "female", "male"):
                        err("%s: rola %s bez oznaczenia płci" % (did, k))
            check_visible(did, d)

    # pliki pomocnicze
    for f in manifest["supportFiles"]:
        p = os.path.join(DATA, f["file"])
        if not os.path.exists(p):
            err("brak pliku pomocniczego %s" % f["file"])
    for section in ("grammar.json", "pronunciation.json", "categories.json",
                    "module-zero.json"):
        data = load(section)
        check_visible(section, data if isinstance(data, dict) else {"records": data})

    # manifest
    for f in manifest["dataFiles"]:
        if f["file"] in counts and f["count"] != counts[f["file"]]:
            err("manifest: %s deklaruje %d, plik ma %d" % (f["file"], f["count"], counts[f["file"]]))
    if manifest["totalRecords"] != len(records):
        err("manifest: totalRecords=%d, faktycznie %d" % (manifest["totalRecords"], len(records)))

    # kopie JS dla trybu file:// muszą być zgodne z plikami JSON
    for fn in sorted(os.listdir(DATA)):
        if not fn.endswith(".json"):
            continue
        twin = os.path.join(DATA, fn[:-5] + ".js")
        if not os.path.exists(twin):
            warn("brak kopii %s dla trybu file:// — uruchom: python3 tools/build-offline-data.py"
                 % os.path.basename(twin))
            continue
        try:
            raw = open(twin, encoding="utf-8").read()
            start = raw.index("] = ") + 4
            end = raw.rindex(";")
            payload = raw[start:end].strip()
            # Dane są wstawiane jako JSON.parse("...") — szybsza ścieżka
            # parsowania w przeglądarce. Zdejmujemy opakowanie, a potem
            # rozwijamy łańcuch (json.loads) i dopiero z niego czytamy dane.
            if payload.startswith("JSON.parse(") and payload.endswith(")"):
                payload = json.loads(payload[len("JSON.parse("):-1])
            embedded = json.loads(payload)
            original = json.load(open(os.path.join(DATA, fn), encoding="utf-8"))
            if embedded != original:
                err("kopia %s jest nieaktualna — uruchom: python3 tools/build-offline-data.py"
                    % os.path.basename(twin))
        except Exception as exc:
            err("nie udało się sprawdzić kopii %s (%s)" % (os.path.basename(twin), exc))

    # --- sceny -------------------------------------------------------------
    scenes_path = os.path.join(DATA, "scenes.json")
    scenes, blocks, question_ids = [], [], set()
    if not os.path.exists(scenes_path):
        err("brak pliku scenes.json — uruchom: python3 tools/generators/scenes.py")
    else:
        sdata = load("scenes.json")
        scenes = sdata["records"]
        blocks = sdata.get("blocks", [])
        if sdata.get("count") != len(scenes):
            err("scenes.json: pole count (%s) != liczba scen (%d)"
                % (sdata.get("count"), len(scenes)))
        if len(scenes) < 40:
            err("scenes.json: %d scen, wymagane minimum 40" % len(scenes))

        seen_scene_ids = set()
        used_dialogues = []
        for sc in scenes:
            sid = sc.get("id", "<brak id>")
            if sid in seen_scene_ids:
                err("%s: zduplikowane ID sceny" % sid)
            seen_scene_ids.add(sid)
            for field in ("title", "level", "situation", "summary", "setting",
                          "dialogueIds", "beats", "keywords", "questions"):
                if not sc.get(field):
                    err("%s: brak pola %s" % (sid, field))

            lines_total = 0
            for did in sc.get("dialogueIds", []):
                if did not in dlg_ids:
                    err("%s: wskazuje na nieistniejący dialog %s" % (sid, did))
                used_dialogues.append(did)
            for beat in sc.get("beats", []):
                lines_total += beat.get("lineCount", 0)
            if sc.get("lineCount") != lines_total:
                err("%s: lineCount=%s, suma odcinków %d"
                    % (sid, sc.get("lineCount"), lines_total))
            # WARUNEK DYDAKTYCZNY: scena to jedna sytuacja od wejścia do
            # wyjścia. Poniżej 20 kwestii kończy się, zanim zdąży się zacząć;
            # powyżej 40 przestaje być jedną sytuacją.
            if not 20 <= lines_total <= 40:
                err("%s: scena ma %d kwestii (dozwolone 20-40)" % (sid, lines_total))

            if sc.get("level") not in ("Survival", "A1", "A2", "B1", "B2"):
                err("%s: nieznany poziom %s" % (sid, sc.get("level")))

            for kw in sc.get("keywords", []):
                if kw.get("id") not in all_ids:
                    err("%s: słowo kluczowe wskazuje na nieistniejące hasło %s"
                        % (sid, kw.get("id")))
                if not kw.get("polish"):
                    err("%s: słowo kluczowe bez znaczenia po polsku" % sid)

            tiers = set()
            for q in sc.get("questions", []):
                qid = q.get("id", "<brak id>")
                if qid in question_ids:
                    err("%s: zduplikowane ID pytania %s" % (sid, qid))
                question_ids.add(qid)
                opts = q.get("options", [])
                if len(opts) != 4:
                    err("%s: pytanie %s ma %d odpowiedzi (wymagane 4)"
                        % (sid, qid, len(opts)))
                if len(set(opts)) != len(opts):
                    err("%s: pytanie %s ma powtórzone odpowiedzi" % (sid, qid))
                if not isinstance(q.get("answer"), int) or not 0 <= q["answer"] < len(opts):
                    err("%s: pytanie %s ma klucz odpowiedzi poza zakresem" % (sid, qid))
                if q.get("tier") not in (1, 2, 3):
                    err("%s: pytanie %s bez poziomu szczegółowości" % (sid, qid))
                if not q.get("prompt") or not q.get("explain"):
                    err("%s: pytanie %s bez treści albo bez uzasadnienia" % (sid, qid))
                tiers.add(q.get("tier"))
            if tiers != {1, 2, 3}:
                err("%s: brak pytań na poziomach %s"
                    % (sid, ", ".join(str(t) for t in sorted({1, 2, 3} - tiers))))
            check_visible(sid, sc)

        # Każdy dialog dokładnie raz — scena nie może pominąć materiału
        # ani użyć tego samego dialogu dwa razy w różnych scenach.
        if len(used_dialogues) != len(set(used_dialogues)):
            err("scenes.json: dialog użyty w więcej niż jednej scenie")
        missing = dlg_ids - set(used_dialogues)
        if missing:
            err("scenes.json: %d dialogów poza scenami (np. %s)"
                % (len(missing), sorted(missing)[0]))

        # --- bloki ekstensywne ---------------------------------------------
        scene_ids = {sc["id"] for sc in scenes}
        used_scenes = []
        for b in blocks:
            bid = b.get("id", "<brak id>")
            for scid in b.get("sceneIds", []):
                if scid not in scene_ids:
                    err("%s: blok wskazuje na nieistniejącą scenę %s" % (bid, scid))
                used_scenes.append(scid)
            sec = (b.get("estSeconds") or {}).get("natural", 0)
            # WARUNEK TRYBU: słuchanie ekstensywne to 3-5 minut ciągłego
            # materiału. Krótszy blok nie zdąży wymusić słuchania całościowego.
            if not 180 <= sec <= 300:
                err("%s: blok trwa %d s (wymagane 180-300)" % (bid, sec))
            passes = b.get("passes", [])
            if [p.get("pass") for p in passes] != [1, 2, 3]:
                err("%s: blok nie ma kompletu trzech przejść" % bid)
            for pdef in passes:
                if not pdef.get("questionIds"):
                    err("%s: przejście %s bez pytań" % (bid, pdef.get("pass")))
                for qid in pdef.get("questionIds", []):
                    if qid not in question_ids:
                        err("%s: przejście %s wskazuje na nieistniejące pytanie %s"
                            % (bid, pdef.get("pass"), qid))
                if pdef.get("pass") == 2 and pdef.get("mode") != "text":
                    err("%s: drugie przejście musi być z tekstem" % bid)
                if pdef.get("pass") in (1, 3) and pdef.get("mode") != "audio":
                    err("%s: przejście %s musi być bez tekstu" % (bid, pdef.get("pass")))
            check_visible(bid, b)
        outside = scene_ids - set(used_scenes)
        if outside:
            warn("%d scen poza blokami ekstensywnymi" % len(outside))

    # --- ćwiczenia rozumienia ----------------------------------------------
    comp_path = os.path.join(DATA, "comprehension.json")
    if not os.path.exists(comp_path):
        err("brak pliku comprehension.json — uruchom: "
            "python3 tools/generators/comprehension.py")
    else:
        cdata = load("comprehension.json")
        by_dialogue = {}
        for fn in dialog_files:
            for d in load(fn)["records"]:
                by_dialogue[d["id"]] = d
        by_rec = {r["id"]: r for r in records}

        gaps = cdata.get("gapItems", [])
        if cdata.get("gapCount") != len(gaps):
            err("comprehension.json: gapCount (%s) != liczba pozycji (%d)"
                % (cdata.get("gapCount"), len(gaps)))
        for it in gaps:
            gid = it.get("id", "<brak id>")
            dlg = by_dialogue.get(it.get("d"))
            if dlg is None:
                err("%s: wskazuje na nieistniejący dialog %s" % (gid, it.get("d")))
                continue
            line = next((l for l in dlg["lines"] if l["index"] == it.get("l")), None)
            if line is None:
                err("%s: wskazuje na nieistniejącą kwestię %s" % (gid, it.get("l")))
                continue
            words = line["thaiPhonetic"].split()
            if len(words) != it.get("words"):
                err("%s: zapisano %s wyrazów, kwestia ma %d"
                    % (gid, it.get("words"), len(words)))
            if not it.get("slots"):
                err("%s: pozycja bez luk" % gid)
            for slot in it.get("slots", []):
                if not 0 <= slot.get("w", -1) < len(words):
                    err("%s: numer wyrazu %s poza zdaniem" % (gid, slot.get("w")))
                if slot.get("r") not in by_rec:
                    err("%s: luka wskazuje na nieistniejące hasło %s" % (gid, slot.get("r")))

        inf = cdata.get("inferenceItems", [])
        if cdata.get("inferenceCount") != len(inf):
            err("comprehension.json: inferenceCount (%s) != liczba pozycji (%d)"
                % (cdata.get("inferenceCount"), len(inf)))
        for it in inf:
            iid = it.get("id", "<brak id>")
            rec = by_rec.get(it.get("r"))
            if rec is None:
                err("%s: wskazuje na nieistniejące hasło %s" % (iid, it.get("r")))
                continue
            if it.get("src") == "dialogue":
                dlg = by_dialogue.get(it.get("d"))
                line = (next((l for l in dlg["lines"] if l["index"] == it.get("l")), None)
                        if dlg else None)
                phon = line["thaiPhonetic"] if line else None
                if phon is None:
                    err("%s: wskazuje na nieistniejącą kwestię" % iid)
                    continue
            else:
                exs = rec.get("examples", [])
                if not 0 <= it.get("ex", -1) < len(exs):
                    err("%s: wskazuje na nieistniejący przykład" % iid)
                    continue
                phon = exs[it["ex"]]["thaiPhonetic"]
            words = phon.split()
            if not 0 <= it.get("w", -1) < len(words):
                err("%s: numer wyrazu %s poza zdaniem" % (iid, it.get("w")))
                continue
            opts = it.get("opts", [])
            if len(opts) != 4 or len(set(opts)) != 4:
                err("%s: wymagane cztery różne odpowiedzi" % iid)
            if not isinstance(it.get("a"), int) or not 0 <= it["a"] < len(opts):
                err("%s: klucz odpowiedzi poza zakresem" % iid)
            elif opts[it["a"]] != it.get("p"):
                err("%s: klucz odpowiedzi nie wskazuje na znaczenie hasła" % iid)
            # WARUNEK DYDAKTYCZNY: bez wskazówek to nie jest ćwiczenie
            # domyślania się, tylko zgadywanka.
            if len(it.get("cues", [])) < 2:
                err("%s: mniej niż dwie wskazówki kontekstowe" % iid)
            for cue in it.get("cues", []):
                if cue.get("w", -1) >= len(words):
                    err("%s: wskazówka pokazuje wyraz spoza zdania" % iid)
            check_visible(iid, it)

    # --- pokrycie rozumienia -----------------------------------------------
    #
    # Ten plik jest podstawą jedynej liczby w aplikacji, która twierdzi, że
    # mówi coś o rozumieniu. Jeśli się rozjedzie z dialogami albo ze słownikiem,
    # miara nadal będzie pokazywać ładny procent — tylko nieprawdziwy. Dlatego
    # sprawdzamy ją tak samo ostro jak materiał do nauki.
    cov_path = os.path.join(DATA, "coverage.json")
    coverage_cats = []
    if not os.path.exists(cov_path):
        err("brak pliku coverage.json — uruchom: "
            "python3 tools/generators/coverage.py")
    else:
        cov = load("coverage.json")
        coverage_cats = cov.get("categories", [])
        totals = cov.get("totals", {})
        method = cov.get("method", {})

        if not 0 < method.get("target", 0) <= 1:
            err("coverage.json: próg celu poza zakresem (%s)" % method.get("target"))
        if not 0 < method.get("lineThreshold", 0) <= 1:
            err("coverage.json: próg zrozumiałości kwestii poza zakresem")
        # Metoda nie stosuje kontroli sensu i musi to o sobie mówić — opis
        # w interfejsie czyta tę wartość, nie zgaduje jej.
        if method.get("senseCheck") is not False:
            err("coverage.json: metoda musi deklarować brak kontroli sensu")

        # Mapy budujemy tutaj od nowa: te z sekcji rozumienia powstają tylko
        # wtedy, gdy comprehension.json istnieje, a sprawdzenie pokrycia nie
        # może zależeć od obecności innego pliku.
        cov_by_dlg = {}
        for fn in dialog_files:
            for d in load(fn)["records"]:
                cov_by_dlg[d["id"]] = d
        cov_by_rec = {r["id"]: r for r in records}
        sums = {"lines": 0, "occurrences": 0, "mapped": 0}
        for c in coverage_cats:
            name = c.get("name", "<bez nazwy>")
            ids = c.get("ids", [])
            weights = c.get("weights", [])
            lines = c.get("l", [])

            if len(weights) != len(ids):
                err("coverage.json/%s: %d wag przy %d hasłach"
                    % (name, len(weights), len(ids)))
            for rid in ids:
                if rid not in cov_by_rec:
                    err("coverage.json/%s: hasło %s nie istnieje w słowniku"
                        % (name, rid))
                    break

            occ = 0
            mapped = 0
            weight_check = [0] * len(ids)
            for ln in lines:
                dlg = cov_by_dlg.get(ln.get("d"))
                if dlg is None:
                    err("coverage.json/%s: kwestia z nieistniejącego dialogu %s"
                        % (name, ln.get("d")))
                    break
                line = next((x for x in dlg["lines"]
                             if x["index"] == ln.get("l")), None)
                if line is None:
                    err("coverage.json/%s: nieistniejąca kwestia %s/%s"
                        % (name, ln.get("d"), ln.get("l")))
                    break
                if dlg.get("category") != name:
                    err("coverage.json/%s: kwestia z dialogu o kategorii %s"
                        % (name, dlg.get("category")))
                    break
                slots = ln.get("s", [])
                # Liczba pozycji MUSI odpowiadać liczbie wyrazów kwestii —
                # inaczej mianownik miary nie jest tym, co uczący się słyszy.
                words = line["thaiPhonetic"].split()
                if len(slots) != len(words):
                    err("coverage.json/%s: %d pozycji przy %d wyrazach (%s/%s)"
                        % (name, len(slots), len(words), ln.get("d"), ln.get("l")))
                    break
                occ += len(slots)
                for sl in slots:
                    if sl >= len(ids):
                        err("coverage.json/%s: numer hasła %d poza tabelą"
                            % (name, sl))
                        break
                    if sl >= 0:
                        mapped += 1
                        weight_check[sl] += 1

            if occ != c.get("occurrences"):
                err("coverage.json/%s: occurrences %s != policzone %d"
                    % (name, c.get("occurrences"), occ))
            if mapped != c.get("mapped"):
                err("coverage.json/%s: mapped %s != policzone %d"
                    % (name, c.get("mapped"), mapped))
            if len(lines) != c.get("lines"):
                err("coverage.json/%s: lines %s != policzone %d"
                    % (name, c.get("lines"), len(lines)))
            if weights and weight_check != weights:
                err("coverage.json/%s: wagi haseł nie zgadzają się z korpusem" % name)
            if c.get("unmapped") != occ - mapped:
                err("coverage.json/%s: unmapped nie domyka się z occurrences" % name)
            if mapped > occ:
                err("coverage.json/%s: więcej przypisań niż wyrazów" % name)

            sums["lines"] += len(lines)
            sums["occurrences"] += occ
            sums["mapped"] += mapped

        for key in ("lines", "occurrences", "mapped"):
            if totals.get(key) != sums[key]:
                err("coverage.json: totals.%s (%s) != suma kategorii (%d)"
                    % (key, totals.get(key), sums[key]))
        if totals.get("categories") != len(coverage_cats):
            err("coverage.json: totals.categories != liczba kategorii")

        # Kategoria bez materiału dialogowego nie może udawać zmierzonej.
        for c in coverage_cats:
            thin = c.get("lines", 0) < method.get("minLines", 40)
            if bool(c.get("thin")) != thin:
                err("coverage.json/%s: znacznik małego materiału nie zgadza się "
                    "z liczbą kwestii" % c.get("name"))

        # Sufit poniżej progu to nie błąd danych, ale musi być widoczny —
        # aplikacja obniża wtedy cel i mówi o tym wprost.
        below = [c["name"] for c in coverage_cats
                 if c["occurrences"] and
                 c["mapped"] / c["occurrences"] < method.get("target", 0.95)]
        if below:
            warn("coverage.json: w %d kategoriach sufit metody leży poniżej "
                 "progu %d%% (%s) — cel jest tam obniżany do sufitu"
                 % (len(below), round(method.get("target", 0.95) * 100),
                    ", ".join(below[:4]) + ("…" if len(below) > 4 else "")))

    # --- ścieżka nauki -----------------------------------------------------
    lessons_path = os.path.join(DATA, "lessons.json")
    lessons = []
    if not os.path.exists(lessons_path):
        err("brak pliku lessons.json — uruchom: python3 tools/generators/lessons.py")
    else:
        ldata = load("lessons.json")
        lessons = ldata["records"]
        if ldata.get("count") != len(lessons):
            err("lessons.json: pole count (%s) != liczba lekcji (%d)"
                % (ldata.get("count"), len(lessons)))
        if len(lessons) < 120:
            err("lessons.json: %d lekcji, wymagane minimum 120" % len(lessons))

        by_id = {r["id"]: r for r in records}
        seen_lesson_ids, used_records = set(), set()
        gram_ids = {g["id"] for g in load("grammar.json")["records"]}

        # Zasób sylab uczącego się, narastająco.
        known = set()
        for L in lessons:
            lid = L.get("id", "<brak id>")
            if lid in seen_lesson_ids:
                err("%s: zduplikowane ID lekcji" % lid)
            seen_lesson_ids.add(lid)

            for field in ("title", "goal", "level", "recordIds", "newWordIds",
                          "grammarId", "dialogueId", "pass", "category"):
                if not L.get(field):
                    err("%s: brak pola %s" % (lid, field))

            ids = L.get("recordIds", [])
            if not 8 <= len(ids) <= 15:
                err("%s: %d rekordów (dozwolone 8-15)" % (lid, len(ids)))
            if len(set(ids)) != len(ids):
                err("%s: powtórzone ID w obrębie lekcji" % lid)
            for rid in ids:
                if rid not in by_id:
                    err("%s: wskazuje na nieistniejący rekord %s" % (lid, rid))
                if rid in used_records:
                    err("%s: rekord %s użyty już w innej lekcji" % (lid, rid))
                used_records.add(rid)

            if L.get("grammarId") not in gram_ids:
                err("%s: nieznany temat gramatyczny %s" % (lid, L.get("grammarId")))
            if L.get("dialogueId") and L["dialogueId"] not in dlg_ids:
                err("%s: nieznany dialog %s" % (lid, L.get("dialogueId")))

            # KLUCZOWY WARUNEK DYDAKTYCZNY.
            # Nowe hasła lekcji poszerzają zasób sylab. Każdy inny rekord w tej
            # lekcji musi mieścić się w zasobie znanym PO tej lekcji — inaczej
            # uczący się dostaje zdanie ze słowem, którego nie miał skąd poznać.
            new_syl = set()
            for wid in L.get("newWordIds", []):
                if wid not in by_id:
                    err("%s: nowe hasło %s nie istnieje" % (lid, wid))
                    continue
                if wid not in ids:
                    err("%s: nowe hasło %s nie jest na liście rekordów lekcji" % (lid, wid))
                new_syl |= set(by_id[wid].get("syllables") or [])
            after = known | new_syl

            for rid in ids:
                if rid in set(L.get("newWordIds", [])) or rid not in by_id:
                    continue
                missing = set(by_id[rid].get("syllables") or []) - after
                if missing:
                    err("%s: rekord %s wprowadza sylaby bez podstaw: %s"
                        % (lid, rid, ", ".join(sorted(missing))))

            # Każde nowe hasło musi dać się w tej lekcji użyć.
            for wid in L.get("newWordIds", []):
                if wid not in by_id:
                    continue
                wsyl = set(by_id[wid].get("syllables") or [])
                # Pełna wypowiedź jest swoim własnym użyciem. Wymaganie
                # DRUGIEGO rekordu, który zawiera wszystkie jej sylaby, ma
                # sens dla pojedynczego wyrazu, ale dla zdania oznacza, że
                # w bazie musi leżeć jego kopia — i dokładnie tak powstał
                # duplikat srv-time-0004 / a1-time-0040 (sesja V).
                if by_id[wid].get("type") in ("sentence", "question", "phrase"):
                    continue
                usable = any(
                    rid != wid and rid in by_id
                    and wsyl <= set(by_id[rid].get("syllables") or [])
                    for rid in ids)
                if not usable:
                    err("%s: hasła %s nie da się użyć w żadnym zdaniu tej lekcji" % (lid, wid))

            p = L.get("pass") or {}
            if not p.get("required") or not p.get("questions"):
                err("%s: kryterium zaliczenia bez progu" % lid)
            elif p["required"] > p["questions"]:
                err("%s: próg zaliczenia wyższy niż liczba pytań" % lid)

            check_visible(lid, L)
            known = after

    # --- progresja gramatyczna ---------------------------------------------
    #
    # WARUNEK, KTÓREGO PILNUJE TA SEKCJA
    #
    #   Temat gramatyczny nie może pojawić się w lekcji wcześniejszej niż
    #   materiał, który go ilustruje.
    #
    # Reguła jest tym samym warunkiem dydaktycznym, który wyżej obowiązuje
    # hasła, rozszerzonym na gramatykę. Do sesji S gramatyka była od niego
    # wolna, bo była przypisywana rotacyjnie (modulo numeru lekcji) i pełniła
    # rolę ozdobnika. Skutek dało się zmierzyć: dwa tematy miały wzorce
    # z sylabami, które w kursie nie pojawiały się NIGDY.
    #
    # Reguła par form zależnych od płci. Ścieżka wprowadza formy męskie
    # (`khráp`, `phǒm`), bo taka jest treść domyślna rekordu; forma żeńska
    # leży w `genderVariant` i nie ma własnego wpisu w `syllables`. Liczone
    # dosłownie, `khâ` nie weszłoby do obiegu nigdy, a temat „partykuły
    # grzecznościowe khráp i khâ" byłby nie do pokazania — mimo że aplikacja
    # od pierwszej lekcji pokazuje obie formy obok siebie. Para wchodzi więc
    # razem. Zbiór jest zamknięty, bo formy zależne od płci są w tajskim
    # kategorią domkniętą, nie produktywną.
    GENDER_PAIR = {
        "khráp": ("khâ", "khá"),
        "phǒm": ("chǎn", "dì", "dì-chǎn"),
    }

    gdata = load("grammar.json")
    topics = gdata["records"]

    if gdata.get("count") != len(topics):
        err("grammar.json: pole count (%s) != liczba tematów (%d)"
            % (gdata.get("count"), len(topics)))
    if len(topics) < 50:
        err("grammar.json: %d tematów, wymagane minimum 50" % len(topics))

    if lessons:
        by_id = {r["id"]: r for r in records}

        # Oś czasu sylab — liczona dokładnie tak jak w generatorze.
        unlock, pool = {}, set()
        for i, L in enumerate(lessons, 1):
            for wid in L.get("newWordIds") or []:
                rec = by_id.get(wid)
                if not rec:
                    continue
                for s in rec.get("syllables") or []:
                    pool.add(s)
                    for extra in GENDER_PAIR.get(s, ()):
                        pool.add(extra)
            for s in pool:
                unlock.setdefault(s, i)

        # Podział na sylaby: z pola `syllables`, a dla tekstów spoza bazy
        # po spacjach i dywizach — ten sam podział, którego używa coverage.py.
        phon2syl = {}
        for r in records:
            p, s = r.get("thaiPhonetic"), r.get("syllables")
            if p and s:
                phon2syl.setdefault(p, list(s))

        def syls_of(text):
            if text in phon2syl:
                return phon2syl[text]
            return [t for t in re.split(r"[ \-]+", text or "") if t]

        def available_from(text):
            out = 0
            for s in syls_of(text):
                u = unlock.get(s)
                if u is None:
                    return None
                out = max(out, u)
            return out

        seen_topics, seen_order = set(), []
        stage_seq = []
        for g in topics:
            tid = g.get("id", "<brak id>")
            if tid in seen_topics:
                err("%s: zduplikowany temat gramatyczny" % tid)
            seen_topics.add(tid)

            for field in ("order", "stage", "stageTitle", "family", "title",
                          "level", "explanation", "contrast", "patterns",
                          "availableFrom", "introducedAt"):
                if g.get(field) in (None, "", []):
                    err("%s: brak pola %s" % (tid, field))

            pats = g.get("patterns") or []
            if len(pats) < 3:
                err("%s: %d wzorców, temat nie ma czym się wytłumaczyć "
                    "(minimum 3)" % (tid, len(pats)))

            at = g.get("introducedAt")
            if not isinstance(at, int) or not 1 <= at <= len(lessons):
                err("%s: introducedAt=%s poza zakresem 1-%d"
                    % (tid, at, len(lessons)))
                at = None

            # SEDNO KONTROLI: każdy wzorzec musi być wyrażalny w chwili,
            # w której temat wchodzi do kursu.
            worst = 0
            for p in pats:
                ph = p.get("thaiPhonetic") or ""
                if not ph:
                    err("%s: wzorzec bez zapisu fonetycznego" % tid)
                    continue
                if not p.get("polish"):
                    err("%s: wzorzec bez tłumaczenia: %s" % (tid, ph))
                if not p.get("ttsThai") or not THAI.search(p.get("ttsThai", "")):
                    err("%s: wzorzec bez pisma tajskiego do syntezy: %s"
                        % (tid, ph))
                # Rekord szablonowy z wielokropkiem nie jest zdaniem. Pole
                # `syllables` pomija taki znak, więc kontrola dostępności
                # liczyłaby co innego, niż uczący się zobaczy na ekranie.
                if re.search(r"\.\.\.|…|__", ph):
                    err("%s: wzorzec jest szablonem z miejscem do wypełnienia, "
                        "nie zdaniem: %s" % (tid, ph))
                av = available_from(ph)
                if av is None:
                    missing = sorted({s for s in syls_of(ph)
                                      if s not in unlock})
                    err("%s: wzorzec „%s” zawiera sylaby, które nie wchodzą "
                        "do obiegu kursu NIGDY: %s"
                        % (tid, ph, ", ".join(missing)))
                    continue
                worst = max(worst, av)
                if at is not None and av > at:
                    err("%s: temat wchodzi w lekcji %d, ale wzorzec „%s” jest "
                        "wyrażalny dopiero od lekcji %d" % (tid, at, ph, av))

            if worst and g.get("availableFrom") != worst:
                err("%s: availableFrom=%s, a materiał pozwala od lekcji %d"
                    % (tid, g.get("availableFrom"), worst))

            seen_order.append(g.get("order"))
            stage_seq.append((g.get("stage"), at))
            check_visible(tid, g)

        if seen_order != list(range(1, len(topics) + 1)):
            err("grammar.json: pole order nie tworzy ciągu 1..%d" % len(topics))

        # Progresja musi rosnąć. Rotacja poznaje się właśnie po tym, że nie
        # rośnie — a bez tej kontroli nic nie broniłoby powrotu do modulo.
        prev = 0
        for g in topics:
            at = g.get("introducedAt")
            if isinstance(at, int):
                if at < prev:
                    err("%s: temat nr %s wchodzi w lekcji %d, wcześniej niż "
                        "temat poprzedni (%d) — progresja się cofa"
                        % (g.get("id"), g.get("order"), at, prev))
                prev = at

        # Etapy nie mogą się przeplatać.
        prev_stage = 0
        for st, _ in stage_seq:
            if isinstance(st, int):
                if st < prev_stage:
                    err("grammar.json: etap %d wraca po etapie %d — etapy "
                        "mają iść po kolei" % (st, prev_stage))
                prev_stage = st

        # Lekcja nie może nieść tematu, który jeszcze nie wszedł.
        intro = {g["id"]: g.get("introducedAt") for g in topics}
        for i, L in enumerate(lessons, 1):
            gid = L.get("grammarId")
            at = intro.get(gid)
            if at is None:
                continue
            if at > i:
                err("%s (lekcja %d): niesie temat %s, który wchodzi dopiero "
                    "w lekcji %d" % (L.get("id"), i, gid, at))
            rid = L.get("grammarReviewId")
            if rid and intro.get(rid) is not None and intro[rid] > i:
                err("%s (lekcja %d): powtórka tematu %s, który jeszcze nie "
                    "wszedł (lekcja %d)" % (L.get("id"), i, rid, intro[rid]))

        covered = {L.get("grammarId") for L in lessons}
        orphan = [g["id"] for g in topics if g["id"] not in covered]
        if orphan:
            warn("grammar.json: %d tematów nie jest tematem żadnej lekcji (%s)"
                 % (len(orphan), ", ".join(orphan[:5])))

    # --- tryby gramatyczne -------------------------------------------------
    check_grammar_modes(lessons)

    # --- Moduł 0: trening percepcyjny --------------------------------------
    # Moduł stoi PRZED lekcją 1, więc jego niespójność blokowałaby wejście
    # w cały kurs. Sprawdzamy go tak samo ostro jak ścieżkę słownikową.
    mz_path = os.path.join(DATA, "module-zero.json")
    mz_lessons, mz_tasks = [], 0
    if not os.path.exists(mz_path):
        err("brak pliku module-zero.json — uruchom: python3 tools/generators/module_zero.py")
    else:
        mz = load("module-zero.json")
        stim = {s["id"]: s for s in mz.get("stimuli", [])}
        if len(stim) != len(mz.get("stimuli", [])):
            err("module-zero.json: zduplikowane ID bodźca")
        contrast_ids = {c["id"] for c in mz.get("contrasts", [])}
        family_ids = {f["id"] for f in mz.get("families", [])}
        type_ids = {t["id"] for t in mz.get("taskTypes", [])}
        mz_lessons = mz.get("lessons", [])

        # Każdy bodziec musi mieć pismo tajskie do syntezy i czytelną fonetykę.
        # Bez ttsThai nie da się go odtworzyć, a moduł jest wyłącznie słuchowy.
        for sid, s0 in stim.items():
            if not s0.get("ttsThai") or not THAI.search(s0.get("ttsThai", "")):
                err("module-zero.json: bodziec %s bez pisma tajskiego do syntezy" % sid)
            if not s0.get("phonetic"):
                err("module-zero.json: bodziec %s bez fonetyki" % sid)
            d = unicodedata.normalize("NFD", s0.get("phonetic", ""))
            bad = [c for c in d if unicodedata.combining(c) and c not in TONES]
            if bad:
                err("module-zero.json: bodziec %s ma nieznany znak diakrytyczny" % sid)
            src = s0.get("sourceId")
            if src and src not in all_ids:
                err("module-zero.json: bodziec %s wskazuje na nieistniejący rekord %s"
                    % (sid, src))

        seen_task_ids = set()
        used_contrasts = set()

        def check_task(t, where, need_family=False):
            tid = t.get("id", "<brak id>")
            if tid in seen_task_ids:
                err("module-zero.json: zduplikowane ID zadania %s" % tid)
            seen_task_ids.add(tid)
            if t.get("type") not in type_ids:
                err("%s: nieznany typ zadania %s" % (tid, t.get("type")))
            if t.get("contrastId") not in contrast_ids:
                err("%s: nieznany kontrast %s" % (tid, t.get("contrastId")))
            else:
                used_contrasts.add(t["contrastId"])
            if need_family and t.get("family") not in family_ids:
                err("%s: zadanie diagnozy bez rodziny kontrastów" % tid)
            plays = t.get("playIds") or []
            if not plays:
                err("%s: zadanie bez bodźca do odtworzenia" % tid)
            for pid in plays:
                if pid not in stim:
                    err("%s: odwołanie do nieistniejącego bodźca %s" % (tid, pid))
            opts = t.get("options") or []
            if len(opts) < 2:
                err("%s: mniej niż dwie odpowiedzi do wyboru" % tid)
            if len(set(opts)) != len(opts):
                err("%s: powtórzona odpowiedź na liście" % tid)
            if t.get("answer") not in opts:
                err("%s: poprawna odpowiedź spoza listy" % tid)
            # Porównanie obu wariantów jest wymogiem dydaktycznym: bez niego
            # informacja zwrotna mówi „źle”, ale niczego nie pokazuje.
            cmp_ids = t.get("compare") or []
            for pid in cmp_ids:
                if pid not in stim:
                    err("%s: porównanie wskazuje na nieistniejący bodziec %s" % (tid, pid))
            if t.get("type") in ("same-diff", "odd-one-out") and len(set(cmp_ids)) < 2:
                err("%s: zadanie różnicowe bez pary do porównania" % tid)
            if not t.get("explain"):
                err("%s: brak wyjaśnienia po odpowiedzi" % tid)
            # Zadanie różnicowe musi stać na parze minimalnej — inaczej
            # rozstrzyga je inna cecha niż trenowana.
            if t.get("type") == "odd-one-out" and len(set(plays)) != 2:
                err("%s: „który jest inny” musi mieć dokładnie dwa różne bodźce" % tid)
            if t.get("type") == "same-diff" and len(plays) != 2:
                err("%s: „to samo czy inne” musi mieć dokładnie dwa bodźce" % tid)

        if len(mz_lessons) != 12:
            err("module-zero.json: %d lekcji, wymagane 12" % len(mz_lessons))
        numbers = []
        for L in mz_lessons:
            lid = L.get("id", "<brak id>")
            for field in ("id", "number", "title", "goal", "contrastIds",
                          "families", "pass", "tasks"):
                if not L.get(field):
                    err("%s: brak pola %s" % (lid, field))
            numbers.append(L.get("number"))
            tasks = L.get("tasks", [])
            mz_tasks += len(tasks)
            if not 15 <= len(tasks) <= 25:
                err("%s: %d zadań (dozwolone 15-25)" % (lid, len(tasks)))
            p = L.get("pass") or {}
            q, req = p.get("questions"), p.get("required")
            if q != len(tasks):
                err("%s: pass.questions=%s, a zadań jest %d" % (lid, q, len(tasks)))
            if not req or not q:
                err("%s: kryterium zaliczenia bez progu" % lid)
            elif req > q:
                err("%s: próg wyższy niż liczba zadań" % lid)
            elif req / float(q) < 0.9:
                err("%s: próg %d z %d to %.0f%% — wymagane co najmniej 90%%"
                    % (lid, req, q, req / float(q) * 100))
            declared = set(L.get("contrastIds", []))
            actual = {t.get("contrastId") for t in tasks}
            if declared != actual:
                err("%s: lista contrastIds nie zgadza się z zadaniami" % lid)
            for t in tasks:
                check_task(t, lid)
            for f in L.get("families", []):
                if f not in family_ids:
                    err("%s: nieznana rodzina kontrastów %s" % (lid, f))
            check_visible(lid, {k: v for k, v in L.items() if k != "tasks"})

        if sorted(numbers) != list(range(1, len(mz_lessons) + 1)):
            err("module-zero.json: numery lekcji nie tworzą ciągu 1..%d" % len(mz_lessons))

        diag = mz.get("diagnostic") or {}
        dtasks = diag.get("tasks", [])
        if len(dtasks) != 20:
            err("module-zero.json: diagnoza ma %d zadań, wymagane 20" % len(dtasks))
        for t in dtasks:
            check_task(t, "diagnoza", need_family=True)
        dfam = {t.get("family") for t in dtasks}
        missing_fam = family_ids - dfam
        if missing_fam:
            err("module-zero.json: diagnoza nie sprawdza rodzin: %s"
                % ", ".join(sorted(missing_fam)))

        # Kontrast zadeklarowany, ale bez materiału, jest obietnicą bez pokrycia.
        unused = contrast_ids - used_contrasts
        if unused:
            err("module-zero.json: kontrasty bez ani jednego zadania: %s"
                % ", ".join(sorted(unused)))

        # Bodziec, którego nie używa żadne zadanie, tylko powiększa plik.
        used_stim = set()
        for L in mz_lessons:
            for t in L.get("tasks", []):
                used_stim |= set(t.get("playIds") or [])
                used_stim |= set(t.get("compare") or [])
        for t in dtasks:
            used_stim |= set(t.get("playIds") or [])
            used_stim |= set(t.get("compare") or [])
        orphan = set(stim) - used_stim
        if orphan:
            warn("module-zero.json: %d bodźców bez zadania (np. %s)"
                 % (len(orphan), sorted(orphan)[0]))

        mz_counts = mz.get("counts") or {}
        if mz_counts.get("lessons") != len(mz_lessons):
            err("module-zero.json: counts.lessons=%s, faktycznie %d"
                % (mz_counts.get("lessons"), len(mz_lessons)))
        if mz_counts.get("tasks") != mz_tasks:
            err("module-zero.json: counts.tasks=%s, faktycznie %d"
                % (mz_counts.get("tasks"), mz_tasks))
        if mz_counts.get("stimuli") != len(stim):
            err("module-zero.json: counts.stimuli=%s, faktycznie %d"
                % (mz_counts.get("stimuli"), len(stim)))

    # --- indeks wyszukiwania -----------------------------------------------
    idx_path = os.path.join(DATA, "search-index.json")
    if not os.path.exists(idx_path):
        err("brak pliku search-index.json — uruchom: python3 tools/build-search-index.py")
    else:
        idx = load("search-index.json")
        # Od sesji O indeks jest dzielony: search-index.json niesie czoło
        # (Survival + A1), a wymienione w polu `parts` pliki resztę. Sprawdzamy
        # SUMĘ — rozjazd między czołem a resztą jest tak samo groźny jak brak
        # wpisu, bo aplikacja sklei je bez pytania.
        rows = list(idx.get("records", []))
        parts = idx.get("parts") or []
        for part in parts:
            ppath = os.path.join(DATA, part)
            if not os.path.exists(ppath):
                err("brak części indeksu %s — uruchom: "
                    "python3 tools/build-search-index.py" % part)
                continue
            rows.extend(load(part).get("records", []))
        declared = idx.get("totalRecords")
        if declared is not None and declared != len(rows):
            err("search-index.json: totalRecords=%s, a części dają %d wpisów"
                % (declared, len(rows)))
        if len(rows) != len(records):
            err("indeks wyszukiwania: %d wpisów w %d %s, baza ma %d rekordów — "
                "uruchom: python3 tools/build-search-index.py"
                % (len(rows), 1 + len(parts),
                   "pliku" if not parts else "plikach", len(records)))
        idx_ids = {r[0] for r in rows}
        missing = all_ids - idx_ids
        if missing:
            err("search-index.json: brak %d haseł, np. %s"
                % (len(missing), sorted(missing)[0]))
        # Indeks jest wczytywany przy starcie i trafia prosto na ekran —
        # pismo tajskie nie ma prawa się w nim znaleźć.
        for r in rows[:]:
            for cell in r[1:5]:
                if isinstance(cell, str) and THAI.search(cell):
                    err("search-index.json: pismo tajskie we wpisie %s" % r[0])
                    break
        if len(idx.get("dialogues", [])) != len(dlg_ids):
            err("search-index.json: %d dialogów, baza ma %d"
                % (len(idx.get("dialogues", [])), len(dlg_ids)))

    # --- moduł liczbowy i moduł ratunkowy (sesja T) ------------------------
    _lpath = load("lessons.json")
    _les_by_id = {L["id"]: L for L in _lpath["records"]}
    _les_by_no = {L["number"]: L for L in _lpath["records"]}
    _dlg_by_id = {}
    for _fn in dialog_files:
        for _d in load(_fn)["records"]:
            _dlg_by_id[_d["id"]] = _d
    num_recs, num_checked, num_irr = check_numbers(_les_by_id, _les_by_no)
    res_recs, res_forms, res_fem = check_rescue(_les_by_id, _dlg_by_id)

    # --- egzaminy poziomowe (sesja U) --------------------------------------
    #
    # Egzamin ma sprawdzać, czy poziom został osiągnięty — a to znaczy, że sam
    # musi być sprawdzalny. Kontrolujemy pięć rzeczy, z których każda po cichu
    # unieważniłaby wynik:
    #
    #   1. klucz odpowiedzi wskazuje istniejącą opcję i nie ma dwóch takich
    #      samych opcji (inaczej „poprawna” byłaby dwa razy),
    #   2. dystraktor w pytaniu o wypowiedź NIE padł w tej scenie (inaczej
    #      dwie odpowiedzi są prawdziwe), a poprawna w niej padła,
    #   3. zestawy jednego poziomu nie dzielą ani jednego zadania — bez tego
    #      „powtórka z innym zestawem” jest pozorna,
    #   4. hasła produkcyjne istnieją w bazie i mają tekst dla syntezatora,
    #      bo bez niego nie ma czego odtworzyć w zadaniu na zapis,
    #   5. progi są w rozsądnym zakresie i wyraźnie nad progiem zgadywania.
    exams_count, exam_tasks = 0, 0
    # Własna mapa haseł: te wyżej powstają wewnątrz bloków warunkowych i mogą
    # nie istnieć, jeśli któryś plik nie doszedł do sprawdzenia.
    u_by_id = {r["id"]: r for r in records}
    exams_path = os.path.join(DATA, "exams.json")
    if not os.path.exists(exams_path):
        err("brak pliku exams.json — uruchom: python3 tools/generators/exams.py")
    else:
        ex = load("exams.json")
        exam_recs = ex.get("records") or []
        exams_count = len(exam_recs)
        if ex.get("count") != exams_count:
            err("exams.json: pole count (%s) != liczba egzaminów (%d)"
                % (ex.get("count"), exams_count))

        th = ex.get("thresholds") or {}
        for key in ("listening", "detail", "speakingTone", "speakingContent", "writing"):
            if key not in th:
                err("exams.json: brak progu „%s”" % key)
            elif not 50 <= th[key] <= 95:
                err("exams.json: próg „%s” = %s leży poza zakresem 50-95"
                    % (key, th[key]))
        # Zgadywanie przy czterech opcjach daje 25 %. Próg musi leżeć wyraźnie
        # wyżej, inaczej egzamin przepuszcza przypadek.
        for key in ("listening", "detail"):
            if key in th and th[key] < 50:
                err("exams.json: próg „%s” zbyt blisko poziomu zgadywania" % key)

        cd = ex.get("cooldown") or {}
        if not cd.get("days") or not cd.get("lessons"):
            err("exams.json: karencja musi mieć i dni, i lekcje — każdy z tych "
                "warunków osobno da się obejść")

        ex_levels = {}
        ex_by_level_ids = {}
        for e in exam_recs:
            eid = e.get("id", "<bez id>")
            ex_levels.setdefault(e.get("level"), []).append(e)
            secs = e.get("sections") or {}
            for key in ("listening", "detail", "speaking", "writing"):
                if key not in secs:
                    err("%s: brak sekcji „%s”" % (eid, key))
                elif not secs[key].get("timeLimitSec"):
                    err("%s/%s: brak limitu czasu" % (eid, key))

            task_ids = []
            for key in ("listening", "detail"):
                for q in (secs.get(key) or {}).get("questions") or []:
                    exam_tasks += 1
                    task_ids.append(q["id"])
                    options = q.get("options") or []
                    if len(options) != 4:
                        err("%s: pytanie %s ma %d opcji zamiast czterech"
                            % (eid, q["id"], len(options)))
                    if len(set(options)) != len(options):
                        err("%s: pytanie %s ma powtórzone opcje" % (eid, q["id"]))
                    if not isinstance(q.get("answer"), int) or \
                            not 0 <= q["answer"] < len(options):
                        err("%s: pytanie %s ma klucz poza zakresem opcji"
                            % (eid, q["id"]))
                    if not q.get("explain"):
                        err("%s: pytanie %s bez uzasadnienia do diagnozy"
                            % (eid, q["id"]))
                    scid = q.get("sceneId")
                    if scid and scid not in {sc["id"] for sc in scenes}:
                        err("%s: pytanie %s wskazuje nieistniejącą scenę %s"
                            % (eid, q["id"], scid))
                    check_visible(q["id"], q)

            for key in ("speaking", "writing"):
                for it in (secs.get(key) or {}).get("items") or []:
                    exam_tasks += 1
                    task_ids.append(it["id"])
                    rid = it.get("recordId")
                    rec = u_by_id.get(rid)
                    if not rec:
                        err("%s/%s: zadanie %s wskazuje nieistniejące hasło %s"
                            % (eid, key, it["id"], rid))
                        continue
                    if not rec.get("ttsThai"):
                        err("%s/%s: hasło %s nie ma tekstu dla syntezatora"
                            % (eid, key, rid))
                    if not it.get("lesson"):
                        err("%s/%s: zadanie %s bez numeru lekcji — diagnoza nie "
                            "miałaby do czego odesłać" % (eid, key, it["id"]))
                    check_visible(it["id"], it)

            if len(set(task_ids)) != len(task_ids):
                err("%s: powtórzone zadanie w jednym egzaminie" % eid)
            if e.get("taskCount") != len(task_ids):
                err("%s: taskCount (%s) != liczba zadań (%d)"
                    % (eid, e.get("taskCount"), len(task_ids)))
            ex_by_level_ids[eid] = set(task_ids)

        # Rozłączność zestawów w obrębie poziomu.
        for level, group in ex_levels.items():
            if len(group) < 2:
                err("poziom %s ma tylko %d zestaw egzaminacyjny — powtórka "
                    "musiałaby iść na tym samym materiale" % (level, len(group)))
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    a, b = group[i]["id"], group[j]["id"]
                    shared = ex_by_level_ids[a] & ex_by_level_ids[b]
                    if shared:
                        err("%s i %s dzielą %d zadań (np. %s)"
                            % (a, b, len(shared), sorted(shared)[0]))

        # Dystraktor nie może być zdaniem, które w tej scenie padło.
        scene_lines_pl = {}
        for sc in scenes:
            said = set()
            for did in sc.get("dialogueIds") or []:
                for ln in (_dlg_by_id.get(did) or {}).get("lines") or []:
                    if ln.get("polish"):
                        said.add(ln["polish"])
            scene_lines_pl[sc["id"]] = said
        for e in exam_recs:
            for q in ((e.get("sections") or {}).get("detail") or {}).get("questions") or []:
                if q.get("kind") not in ("said", "reply"):
                    continue
                said = scene_lines_pl.get(q.get("sceneId"), set())
                for i, opt in enumerate(q["options"]):
                    if i == q["answer"] and opt not in said:
                        err("%s: klucz pytania %s nie padł w scenie"
                            % (e["id"], q["id"]))
                    if i != q["answer"] and opt in said:
                        err("%s: dystraktor pytania %s padł w scenie — "
                            "dwie odpowiedzi są prawdziwe" % (e["id"], q["id"]))

    # --- próbki kontrolne (sesja U) ----------------------------------------
    #
    # Próbka ma wykrywać zapominanie WCZEŚNIEJ niż powtórki, więc jej sens
    # zależy od jednej liczby: odstępu między lekcją, która ją wyzwala,
    # a materiałem, o który pyta. Zbyt mały odstęp sprawdza pamięć świeżą,
    # zbyt duży — dubluje to, co SRS już pokazał.
    check_count, check_tasks = 0, 0
    chk_path = os.path.join(DATA, "checkpoints.json")
    if not os.path.exists(chk_path):
        err("brak pliku checkpoints.json — uruchom: "
            "python3 tools/generators/checkpoints.py")
    else:
        ch = load("checkpoints.json")
        chk_recs = ch.get("records") or []
        check_count = len(chk_recs)
        if ch.get("count") != check_count:
            err("checkpoints.json: pole count (%s) != liczba próbek (%d)"
                % (ch.get("count"), check_count))
        every, lag = ch.get("every"), ch.get("lag")
        if not every or not lag:
            err("checkpoints.json: brak deklaracji odstępu (every) lub "
                "opóźnienia (lag)")
        last_lesson = max(_les_by_no) if _les_by_no else 0
        seen_ids = set()
        for c in chk_recs:
            cid = c.get("id", "<bez id>")
            if cid in seen_ids:
                err("checkpoints.json: powtórzony identyfikator %s" % cid)
            seen_ids.add(cid)
            if c["triggerLesson"] > last_lesson:
                err("%s: wyzwalana po lekcji %d, a ścieżka ma ich %d"
                    % (cid, c["triggerLesson"], last_lesson))
            span = c["toLesson"] - c["fromLesson"] + 1
            if span != every:
                err("%s: okno obejmuje %d lekcji zamiast %d" % (cid, span, every))
            if c["triggerLesson"] - c["toLesson"] != lag:
                err("%s: materiał sprzed %d lekcji zamiast %d — próbka straciłaby "
                    "sens, bo pytałaby o świeżą pamięć"
                    % (cid, c["triggerLesson"] - c["toLesson"], lag))
            if not 50 <= c.get("passPct", 0) <= 95:
                err("%s: próg %s poza zakresem 50-95" % (cid, c.get("passPct")))
            item_ids = set()
            for it in c.get("items") or []:
                check_tasks += 1
                if it["id"] in item_ids:
                    err("%s: powtórzone zadanie %s" % (cid, it["id"]))
                item_ids.add(it["id"])
                rec = u_by_id.get(it.get("recordId"))
                if not rec:
                    err("%s: zadanie %s wskazuje nieistniejące hasło %s"
                        % (cid, it["id"], it.get("recordId")))
                    continue
                if not rec.get("ttsThai"):
                    err("%s: hasło %s nie ma tekstu dla syntezatora"
                        % (cid, it["recordId"]))
                les = _les_by_no.get(it.get("lesson"))
                if not les:
                    err("%s: zadanie %s wskazuje nieistniejącą lekcję %s"
                        % (cid, it["id"], it.get("lesson")))
                elif not c["fromLesson"] <= it["lesson"] <= c["toLesson"]:
                    err("%s: zadanie %s pochodzi z lekcji %d, spoza okna %d-%d"
                        % (cid, it["id"], it["lesson"], c["fromLesson"], c["toLesson"]))
                if it.get("kind") == "listen":
                    options = it.get("options") or []
                    if len(options) != 4:
                        err("%s: zadanie %s ma %d opcji zamiast czterech"
                            % (cid, it["id"], len(options)))
                    if len(set(options)) != len(options):
                        err("%s: zadanie %s ma powtórzone opcje" % (cid, it["id"]))
                    if not isinstance(it.get("answer"), int) or \
                            not 0 <= it["answer"] < len(options):
                        err("%s: zadanie %s ma klucz poza zakresem" % (cid, it["id"]))
                    elif options[it["answer"]] != rec.get("polish"):
                        err("%s: klucz zadania %s nie wskazuje znaczenia hasła"
                            % (cid, it["id"]))
                check_visible(it["id"], it)

    # nawrót konwencji z dwukropkiem
    if kolon_hits:
        warn("wzorzec „słowo: słowo.” w polu polish — %d wystąpień, np. %s (%s)"
             % (len(kolon_hits), kolon_hits[0][2], kolon_hits[0][0]))
        for rid, where, text in kolon_hits[:10]:
            warn("  %s [%s]: %s" % (rid, where, text))

    # raport
    print("=" * 58)
    print("WALIDACJA BAZY THAI ALL-IN-ONE")
    print("=" * 58)
    for fn, c in counts.items():
        print("  %-26s %5d" % (fn, c))
    print("  %-26s %5d" % ("RAZEM rekordów słownika", len(records)))
    print("  %-26s %5d" % ("dialogów", len(dlg_ids)))
    print("  %-26s %5d" % ("tekstów z wariantem żeńskim", plec_ok))
    print("  %-26s %5d" % ("tekstów z wariantem potocznym", colloquial_ok))
    for rid, _label, _d in CO.RULES:
        if colloquial_rules.get(rid):
            print("      %-22s %5d" % ("reguła " + rid, colloquial_rules[rid]))
    print("  %-26s %5d" % ("lekcji w ścieżce nauki", len(lessons)))
    _g = load("grammar.json")
    print("  %-26s %5d" % ("tematów gramatycznych", len(_g["records"])))
    print("      %-22s %5d" % ("etapów progresji", len(_g.get("stages") or [])))
    print("      %-22s %5d" % ("wzorców", sum(len(t["patterns"])
                                              for t in _g["records"])))
    print("      %-22s %5.1f" % ("wzorców na temat",
                                 sum(len(t["patterns"]) for t in _g["records"])
                                 / float(len(_g["records"]))))
    for _f, _lbl in (("grammar-listening.json", "zadań: struktura"),
                     ("grammar-transform.json", "zadań: transformacje"),
                     ("particles.json", "partykuł końcowych")):
        print("      %-22s %5d" % (_lbl, len(load(_f)["records"])))
    print("  %-26s %5d" % ("lekcji w Module 0", len(mz_lessons)))
    print("  %-26s %5d" % ("zadań percepcyjnych", mz_tasks))
    print("  %-26s %5d" % ("scen", len(scenes)))
    if scenes:
        lens = sorted(sc["lineCount"] for sc in scenes)
        print("      %-22s %5s" % ("kwestii w scenie",
                                   "%d-%d" % (lens[0], lens[-1])))
        print("      %-22s %5d" % ("pytań o sens całości", len(question_ids)))
    print("  %-26s %5d" % ("kategorii z pokryciem", len(coverage_cats)))
    if coverage_cats:
        occ = sum(c["occurrences"] for c in coverage_cats)
        mp = sum(c["mapped"] for c in coverage_cats)
        print("      %-22s %5d" % ("kwestii w korpusie",
                                   sum(c["lines"] for c in coverage_cats)))
        print("      %-22s %5d" % ("wystąpień wyrazów", occ))
        print("      %-22s %5.1f" % ("sufit metody %", 100.0 * mp / max(1, occ)))
    print("  %-26s %5d" % ("rekordów modułu liczbowego", num_recs))
    print("      %-22s %5d" % ("liczb sprawdzonych", num_checked))
    print("      %-22s %5d" % ("nieregularności", num_irr))
    print("  %-26s %5d" % ("formuł ratunkowych", res_recs))
    print("      %-22s %5d" % ("form (rejestr x płeć)", res_forms * 2))
    print("      %-22s %5d" % ("wariantów żeńskich", res_fem))
    print("  %-26s %5d" % ("bloków ekstensywnych", len(blocks)))
    if blocks:
        print("      %-22s %5.1f" % ("minut materiału",
              sum(b["estSeconds"]["natural"] for b in blocks) / 60.0))
    print("  %-26s %5d" % ("egzaminów poziomowych", exams_count))
    print("      %-22s %5d" % ("zadań w egzaminach", exam_tasks))
    print("  %-26s %5d" % ("próbek kontrolnych", check_count))
    print("      %-22s %5d" % ("zadań w próbkach", check_tasks))
    print("-" * 58)
    for w in warnings[:20]:
        print("  OSTRZEŻENIE:", w)
    for e in errors[:40]:
        print("  BŁĄD:", e)
    if len(errors) > 40:
        print("  ... oraz %d dalszych błędów" % (len(errors) - 40))
    print("-" * 58)
    print("Błędy: %d | Ostrzeżenia: %d" % (len(errors), len(warnings)))
    print("WYNIK:", "BAZA POPRAWNA" if not errors else "BAZA ZAWIERA BŁĘDY")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
