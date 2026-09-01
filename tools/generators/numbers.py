#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator modułu liczbowego — data/numbers.json.

Liczby w mowie nie są podzbiorem słownictwa. Uczący się może znać wszystkie
dziesięć cyfr i mimo to nie wyłapać ceny powiedzianej w tempie kasjera. To jest
umiejętność percepcyjna — mierzy się ją czasem reakcji, nie liczbą znanych
haseł — i dlatego stoi w osobnym pliku, z osobnymi ćwiczeniami i osobną
statystyką.

Plik NIE jest listą liczb. Trzyma atomy (cyfry, pozycje, nieregularności),
jednostki (baht, moong, wan…) i punkty kontrolne; każdą konkretną liczbę składa
reguła z `thai_numbers.py` — po stronie generatora, walidatora i aplikacji ta
sama. Gdyby liczby były wypisane, plik miałby milion pozycji, a ćwiczenie i tak
musiałoby umieć wygenerować tę jedną, której akurat brakuje.

Uruchomienie:
    python3 tools/generators/numbers.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import thai_numbers as TN          # noqa: E402
import engine as EN                # noqa: E402
import colloquial as CO            # noqa: E402
import gender_forms as GF          # noqa: E402
import jsonio                      # noqa: E402

DATA = os.path.join(ROOT, "data")
VERSION = "1.18.0"


# --- budowa węzła -----------------------------------------------------------

def node(polish, words, *, register="neutralny", gender=True, colloq=True, extra=None):
    """Jeden tekst modułu: fonetyka, pismo dla syntezatora, warianty.

    `words` to lista par (fonetyka wyrazu, pismo wyrazu). Dzięki temu granice
    wyrazów dla syntezatora (`ttsSplit`) wychodzą z budowy, a nie z zgadywania
    po fakcie — pismo tajskie nie stawia spacji, więc bez tych długości nie da
    się pociąć wypowiedzi na wyrazy w tempie dydaktycznym.
    """
    ph = " ".join(w[0] for w in words)
    th = "".join(w[1] for w in words)
    out = {
        "polish": polish,
        "thaiPhonetic": ph,
        "pronunciationPolish": EN.polish_read(ph),
        "toneGuide": EN.tone_guide(ph),
        "ttsThai": th,
        "ttsSplit": [len(w[1]) for w in words],
    }
    if extra:
        out.update(extra)
    if colloq:
        coll = CO.build(ph, th, EN.polish_read)
        if coll:
            out["colloquial"] = coll
    if gender:
        var = GF.build_variant(out, register)
        if var:
            var = {k: v for k, v in var.items() if not k.startswith("_")}
            out["genderVariant"] = {"female": var}
    return out


def num_words(n):
    """Liczba jako jeden wyraz — para (fonetyka, pismo)."""
    return TN.read(n)


# --- słownik jednostek ------------------------------------------------------

W = {
    "bàat": ("bàat", "บาท"),
    "sà-taang": ("sà-taang", "สตางค์"),
    "sà-lueng": ("sà-lueng", "สลึง"),
    "raa-khaa": ("raa-khaa", "ราคา"),
    "thâo-rài": ("thâo-rài", "เท่าไหร่"),
    "kìi": ("kìi", "กี่"),
    "lót": ("lót", "ลด"),
    "nòi": ("nòi", "หน่อย"),
    "dâai": ("dâai", "ได้"),
    "mǎi": ("mǎi", "ไหม"),
    "khráp": ("khráp", "ครับ"),
    "khǎw": ("khǎw", "ขอ"),
    "thawn": ("thawn", "ทอน"),
    "ngoen": ("ngoen", "เงิน"),
    "phaeng": ("phaeng", "แพง"),
    "thùuk": ("thùuk", "ถูก"),
    "moong": ("moong", "โมง"),
    "tii": ("tii", "ตี"),
    "thûm": ("thûm", "ทุ่ม"),
    "cháo": ("cháo", "เช้า"),
    "bàai": ("bàai", "บ่าย"),
    "yen": ("yen", "เย็น"),
    "thîang": ("thîang", "เที่ยง"),
    "thîang-khuen": ("thîang-khuen", "เที่ยงคืน"),
    "klaang-wan": ("klaang-wan", "กลางวัน"),
    "klaang-khuen": ("klaang-khuen", "กลางคืน"),
    "naa-lí-kaa": ("naa-lí-kaa", "นาฬิกา"),
    "naa-thii": ("naa-thii", "นาที"),
    "wí-naa-thii": ("wí-naa-thii", "วินาที"),
    "chûa-moong": ("chûa-moong", "ชั่วโมง"),
    "khrûeng": ("khrûeng", "ครึ่ง"),
    "wan": ("wan", "วัน"),
    "duean": ("duean", "เดือน"),
    "pii": ("pii", "ปี"),
    "sàp-daa": ("sàp-daa", "สัปดาห์"),
    "aa-thít": ("aa-thít", "อาทิตย์"),
    "thîi": ("thîi", "ที่"),
    "phaw-sǎw": ("phaw-sǎw", "พ.ศ."),
    "khaw-sǎw": ("khaw-sǎw", "ค.ศ."),
    "boe": ("boe", "เบอร์"),
    "thoo": ("thoo", "โทร"),
    "hâwng": ("hâwng", "ห้อง"),
    "rót-mee": ("rót-mee", "รถเมล์"),
    "sǎai": ("sǎai", "สาย"),
    "chaan-chaa-laa": ("chaan-chaa-laa", "ชานชาลา"),
    "thîi-nâng": ("thîi-nâng", "ที่นั่ง"),
    "prà-maan": ("prà-maan", "ประมาณ"),
    "kwàa": ("kwàa", "กว่า"),
    "kùeap": ("kùeap", "เกือบ"),
    "raao-raao": ("raao-raao", "ราวๆ"),
    "mâak": ("mâak", "มาก"),
    "náwy": ("náwy", "น้อย"),
    "sèet": ("sèet", "เศษ"),
    "sùan": ("sùan", "ส่วน"),
    "nai": ("nai", "ใน"),
    "thúk": ("thúk", "ทุก"),
    "khráng": ("khráng", "ครั้ง"),
    "tâng-tàe": ("tâng-tàe", "ตั้งแต่"),
    "thǔeng": ("thǔeng", "ถึง"),
    "pen": ("pen", "เป็น"),
    "wee-laa": ("wee-laa", "เวลา"),
    "tàw": ("tàw", "ต่อ"),
    "khon": ("khon", "คน"),
    "an": ("an", "อัน"),
    "bai": ("bai", "ใบ"),
    "tua": ("tua", "ตัว"),
    "khùat": ("khùat", "ขวด"),
    "jaan": ("jaan", "จาน"),
    "mii": ("mii", "มี"),
    "ao": ("ao", "เอา"),
    "yùu": ("yùu", "อยู่"),
    "mûea-rài": ("mûea-rài", "เมื่อไหร่"),
    "wan-níi": ("wan-níi", "วันนี้"),
    "phrûng-níi": ("phrûng-níi", "พรุ่งนี้"),
    "mûea-waan-níi": ("mûea-waan-níi", "เมื่อวานนี้"),
    "níi": ("níi", "นี้"),
    "nǎi": ("nǎi", "ไหน"),
    "dii": ("dii", "ดี"),
    "khâ": ("khâ", "ค่ะ"),
    "khá": ("khá", "คะ"),
}

WEEKDAYS = [
    ("jan", "จันทร์", "poniedziałek"),
    ("ang-khaan", "อังคาร", "wtorek"),
    ("phút", "พุธ", "środa"),
    ("phá-rúe-hàt", "พฤหัส", "czwartek"),
    ("sùk", "ศุกร์", "piątek"),
    ("sǎo", "เสาร์", "sobota"),
    ("aa-thít", "อาทิตย์", "niedziela"),
]

MONTHS = [
    ("má-ka-raa-khom", "มกราคม", "styczeń"),
    ("kum-phaa-phan", "กุมภาพันธ์", "luty"),
    ("mii-naa-khom", "มีนาคม", "marzec"),
    ("mee-sǎa-yon", "เมษายน", "kwiecień"),
    ("phrúet-sà-phaa-khom", "พฤษภาคม", "maj"),
    ("mí-thù-naa-yon", "มิถุนายน", "czerwiec"),
    ("ka-rá-ka-daa-khom", "กรกฎาคม", "lipiec"),
    ("sǐng-hǎa-khom", "สิงหาคม", "sierpień"),
    ("kan-yaa-yon", "กันยายน", "wrzesień"),
    ("tù-laa-khom", "ตุลาคม", "październik"),
    ("phrúet-sà-jì-kaa-yon", "พฤศจิกายน", "listopad"),
    ("than-waa-khom", "ธันวาคม", "grudzień"),
]

# Miesiące „-khom” mają 31 dni, „-yon” 30, luty (-phan) 28/29. Ta końcówka jest
# regułą, nie zbiegiem okoliczności — warto ją uczącemu się powiedzieć wprost.
MONTH_HINT = ("Końcówka mówi, ile dni ma miesiąc: -khom to 31 dni, -yon to 30, "
              "a luty -phan jest jedynym wyjątkiem.")


# --- pora dnia w systemie sześciogodzinnym ----------------------------------

def clock_words(hour, minute=0, formal=False):
    """Godzina jako lista par (fonetyka, pismo).

    Tajski system potoczny dzieli dobę na cztery odcinki i w każdym liczy od
    nowa. `sìi moong` znaczy 10 rano albo 16, zależnie od tego, co stoi obok —
    i to jest ta pułapka, przez którą uczący się z formalnie opanowanym A2
    spóźnia się o sześć godzin.
    """
    if formal:
        out = [num_words(hour), W["naa-lí-kaa"]]
    elif hour == 0:
        out = [W["thîang-khuen"]]
    elif 1 <= hour <= 5:
        out = [W["tii"], num_words(hour)]
    elif 6 <= hour <= 11:
        out = [num_words(hour), W["moong"], W["cháo"]]
    elif hour == 12:
        out = [W["thîang"], W["wan"]]
    elif 13 <= hour <= 15:
        out = [W["bàai"], num_words(hour - 12), W["moong"]]
    elif 16 <= hour <= 18:
        out = [num_words(hour - 12), W["moong"], W["yen"]]
    elif 19 <= hour <= 23:
        out = [num_words(hour - 18), W["thûm"]]
    else:
        raise ValueError("godzina poza dobą: %r" % (hour,))

    if minute == 30:
        out.append(W["khrûeng"])
    elif minute:
        out.append(num_words(minute))
        out.append(W["naa-thii"])
    return out


def clock_polish(hour, minute):
    return "%02d:%02d" % (hour, minute)


DAY_PARTS = [
    ("tii", "tii 1 – tii 5", 1, 5, "od pierwszej do piątej nad ranem",
     "Odcinek liczony od północy. `tii hâa` to piąta rano, nie siedemnasta."),
    ("cháo", "hòk – sìp-èt moong cháo", 6, 11, "od szóstej do jedenastej rano",
     "Tu numer godziny zgadza się z zegarem, ale `cháo` na końcu jest obowiązkowe."),
    ("thîang", "thîang wan", 12, 12, "południe",
     "Południe ma własne słowo i nie jest liczone jako dwunasta."),
    ("bàai", "bàai nùeng – bàai sǎam moong", 13, 15, "od trzynastej do piętnastej",
     "Licznik startuje od nowa: `bàai sǎwng moong` to czternasta, nie druga w nocy."),
    ("yen", "sìi – hòk moong yen", 16, 18, "od szesnastej do osiemnastej",
     "`sìi moong yen` i `sìi moong cháo` różnią się jednym słowem i sześcioma godzinami."),
    ("thûm", "nùeng – hâa thûm", 19, 23, "od dziewiętnastej do dwudziestej trzeciej",
     "Wieczór liczy się od dziewiętnastej: `sǎwng thûm` to dwudziesta."),
]


# --- składanie rekordów -----------------------------------------------------

class Builder(object):
    def __init__(self):
        self.records = []
        self.seq = 0

    def add(self, section, polish, words, **kw):
        self.seq += 1
        rec = {"id": "num-%04d" % self.seq, "section": section}
        meta = kw.pop("meta", None)
        rec.update(node(polish, words, **kw))
        if meta:
            rec["meta"] = meta
        self.records.append(rec)
        return rec


def build_records():
    B = Builder()

    # --- 1. liczebniki ------------------------------------------------------
    for n in range(0, 11):
        B.add("numerals", str(n), [num_words(n)], gender=False,
              meta={"value": n, "kind": "cardinal"})
    for n in range(11, 20):
        B.add("numerals", str(n), [num_words(n)], gender=False,
              meta={"value": n, "kind": "cardinal",
                    "irregular": TN.irregular_kinds(n)})
    for n in [20, 21, 22, 30, 31, 40, 50, 60, 70, 80, 90]:
        B.add("numerals", str(n), [num_words(n)], gender=False,
              meta={"value": n, "kind": "cardinal",
                    "irregular": TN.irregular_kinds(n)})
    for n in [100, 101, 105, 110, 111, 120, 121, 200, 555, 999,
              1000, 1001, 1100, 2500, 10000, 12345, 100000, 123456,
              999999, 1000000]:
        B.add("numerals", str(n), [num_words(n)], gender=False,
              meta={"value": n, "kind": "cardinal",
                    "irregular": TN.irregular_kinds(n)})

    # --- 2. ceny ------------------------------------------------------------
    for n in [5, 10, 20, 25, 35, 50, 60, 100, 120, 250, 500, 1000, 1500]:
        B.add("prices", "%d bahtów" % n if n > 1 else "1 baht",
              [num_words(n), W["bàat"]], gender=False,
              meta={"value": n, "kind": "price", "unit": "baht"})
    for n in [25, 50, 75]:
        B.add("prices", "%d satangów" % n, [num_words(n), W["sà-taang"]],
              gender=False, meta={"value": n, "kind": "price", "unit": "satang"})
    B.add("prices", "35,50 bahta",
          [num_words(35), W["bàat"], num_words(50), W["sà-taang"]], gender=False,
          meta={"value": 3550, "kind": "price", "unit": "baht-satang"})
    B.add("prices", "jeden salueng (25 satangów) — forma z targu",
          [num_words(1), W["sà-lueng"]], gender=False,
          meta={"value": 25, "kind": "price", "unit": "salueng",
                "note": "Salueng to ćwierć bahta. Na targu i w rozmowie o drobnych "
                        "słychać go częściej niż „yîi-sìp-hâa sà-taang”."})
    B.add("prices", "Ile to kosztuje?", [W["raa-khaa"], W["thâo-rài"], W["khráp"]],
          meta={"kind": "ask-price"})
    B.add("prices", "Ile bahtów?", [W["kìi"], W["bàat"], W["khráp"]],
          meta={"kind": "ask-price"})
    B.add("prices", "Może pan trochę opuścić?",
          [W["lót"], W["nòi"], W["dâai"], W["mǎi"], W["khráp"]],
          meta={"kind": "haggle"})
    B.add("prices", "To bardzo drogo.", [W["phaeng"], W["mâak"], W["khráp"]],
          meta={"kind": "haggle"})
    B.add("prices", "Poproszę resztę.", [W["khǎw"], W["ngoen"], W["thawn"], W["khráp"]],
          meta={"kind": "change"})

    # --- 3. godziny ---------------------------------------------------------
    for hour in [1, 3, 5, 6, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 0]:
        B.add("clock", clock_polish(hour, 0), clock_words(hour, 0), gender=False,
              meta={"hour": hour, "minute": 0, "kind": "clock", "style": "spoken"})
    for hour, minute in [(7, 30), (9, 15), (14, 30), (18, 45), (20, 30)]:
        B.add("clock", clock_polish(hour, minute), clock_words(hour, minute),
              gender=False,
              meta={"hour": hour, "minute": minute, "kind": "clock", "style": "spoken"})
    for hour, minute in [(13, 0), (18, 30), (21, 0)]:
        B.add("clock", clock_polish(hour, minute) + " (forma urzędowa)",
              clock_words(hour, minute, formal=True), gender=False,
              meta={"hour": hour, "minute": minute, "kind": "clock", "style": "formal"})
    B.add("clock", "O której?", [W["kìi"], W["moong"], W["khráp"]], meta={"kind": "ask-clock"})
    B.add("clock", "w dzień", [W["klaang-wan"]], gender=False, meta={"kind": "daypart"})
    B.add("clock", "w nocy", [W["klaang-khuen"]], gender=False, meta={"kind": "daypart"})

    # --- 4. daty ------------------------------------------------------------
    for ph, th, pl in WEEKDAYS:
        B.add("dates", pl, [W["wan"], (ph, th)], gender=False,
              meta={"kind": "weekday", "index": [w[0] for w in WEEKDAYS].index(ph) + 1})
    for i, (ph, th, pl) in enumerate(MONTHS, start=1):
        B.add("dates", pl, [(ph, th)], gender=False,
              meta={"kind": "month", "index": i, "days": (28 if i == 2 else
                    (31 if ph.endswith("khom") else 30))})
    for day, month in [(1, 1), (13, 4), (15, 6), (31, 12)]:
        mph, mth, mpl = MONTHS[month - 1]
        B.add("dates", "%d %s" % (day, mpl),
              [W["wan"], W["thîi"], num_words(day), (mph, mth)], gender=False,
              meta={"kind": "date", "day": day, "month": month})
    for ce in [2024, 2025, 2026]:
        be = ce + 543
        B.add("dates", "rok %d (kalendarz buddyjski: %d)" % (ce, be),
              [W["pii"], W["phaw-sǎw"], num_words(be)], gender=False,
              meta={"kind": "year", "ce": ce, "be": be, "era": "BE"})
    B.add("dates", "rok 2026 w kalendarzu gregoriańskim",
          [W["pii"], W["khaw-sǎw"], num_words(2026)], gender=False,
          meta={"kind": "year", "ce": 2026, "be": 2569, "era": "CE"})
    B.add("dates", "Którego dziś jest?", [W["wan"], W["thîi"], W["thâo-rài"], W["khráp"]],
          meta={"kind": "ask-date"})

    # --- 5. czas trwania i częstotliwość ------------------------------------
    B.add("duration", "dwie godziny", [num_words(2), W["chûa-moong"]], gender=False,
          meta={"kind": "duration", "value": 2, "unit": "hour"})
    B.add("duration", "czterdzieści minut", [num_words(40), W["naa-thii"]], gender=False,
          meta={"kind": "duration", "value": 40, "unit": "minute"})
    B.add("duration", "trzy dni", [num_words(3), W["wan"]], gender=False,
          meta={"kind": "duration", "value": 3, "unit": "day"})
    B.add("duration", "dwa tygodnie", [num_words(2), W["aa-thít"]], gender=False,
          meta={"kind": "duration", "value": 2, "unit": "week"})
    B.add("duration", "przez pięć dni", [W["pen"], W["wee-laa"], num_words(5), W["wan"]],
          gender=False, meta={"kind": "duration", "value": 5, "unit": "day"})
    B.add("duration", "od dziewiątej do siedemnastej",
          [W["tâng-tàe"]] + clock_words(9) + [W["thǔeng"]] + clock_words(17),
          gender=False, meta={"kind": "range", "from": 9, "to": 17})
    B.add("duration", "codziennie", [W["thúk"], W["wan"]], gender=False,
          meta={"kind": "frequency"})
    B.add("duration", "co tydzień", [W["thúk"], W["aa-thít"]], gender=False,
          meta={"kind": "frequency"})
    B.add("duration", "trzy razy w tygodniu",
          [num_words(3), W["khráng"], W["tàw"], W["aa-thít"]], gender=False,
          meta={"kind": "frequency", "value": 3})
    B.add("duration", "Jak długo?", [W["kìi"], W["chûa-moong"], W["khráp"]],
          meta={"kind": "ask-duration"})

    # --- 6. numery ----------------------------------------------------------
    B.add("serials", "Mój numer telefonu to 08 1234 5678.",
          [W["boe"], W["thoo"], (TN.phonetic(0), TN.thai(0)),
           (TN.phonetic(8), TN.thai(8)), (TN.phonetic(1), TN.thai(1)),
           (TN.phonetic(2), TN.thai(2)), (TN.phonetic(3), TN.thai(3)),
           (TN.phonetic(4), TN.thai(4)), (TN.phonetic(5), TN.thai(5)),
           (TN.phonetic(6), TN.thai(6)), (TN.phonetic(7), TN.thai(7)),
           (TN.phonetic(8), TN.thai(8)), W["khráp"]],
          meta={"kind": "phone", "digits": "0812345678",
                "note": "Numer telefonu czyta się cyfra po cyfrze. Złożenie go "
                        "w liczbę („osiemset dwanaście…”) jest niezrozumiałe."})
    B.add("serials", "pokój 512", [W["hâwng"], W["boe"], num_words(512)], gender=False,
          meta={"kind": "room", "value": 512})
    B.add("serials", "autobus linii 25", [W["rót-mee"], W["sǎai"], num_words(25)],
          gender=False, meta={"kind": "bus", "value": 25})
    B.add("serials", "peron 3", [W["chaan-chaa-laa"], W["thîi"], num_words(3)],
          gender=False, meta={"kind": "platform", "value": 3})
    B.add("serials", "miejsce 14", [W["thîi-nâng"], W["boe"], num_words(14)],
          gender=False, meta={"kind": "seat", "value": 14})
    B.add("serials", "Jaki jest pana numer telefonu?",
          [W["boe"], W["thoo"], W["thâo-rài"], W["khráp"]], meta={"kind": "ask-phone"})

    # --- 7. ilości z klasyfikatorami ----------------------------------------
    quantities = [
        (2, "khon", "คน", "dwie osoby", "cls-001"),
        (3, "khùat", "ขวด", "trzy butelki", "cls-023"),
        (1, "jaan", "จาน", "jeden talerz", "cls-024"),
        (4, "bai", "ใบ", "cztery sztuki (rzeczy okrągłe i pojemniki)", "cls-006"),
        (5, "an", "อัน", "pięć sztuk (rzeczy drobne)", "cls-007"),
        (2, "tua", "ตัว", "dwa zwierzęta albo sztuki odzieży", "cls-005"),
    ]
    for n, cph, cth, pl, cid in quantities:
        if n == 1:
            # „Jeden” staje PO klasyfikatorze — to jedyna liczba, która tak robi.
            words = [(cph, cth), num_words(1)]
            irr = "one-after-classifier"
        else:
            words = [num_words(n), (cph, cth)]
            irr = None
        B.add("quantities", pl, words, gender=False,
              meta={"kind": "quantity", "value": n, "classifier": cph,
                    "classifierId": cid, "irregular": [irr] if irr else []})
    B.add("quantities", "Ile sztuk?", [W["kìi"], W["an"], W["khráp"]],
          meta={"kind": "ask-quantity"})

    # --- 8. ułamki i wartości przybliżone -----------------------------------
    B.add("fractions", "połowa", [W["khrûeng"]], gender=False, meta={"kind": "fraction"})
    B.add("fractions", "jedna czwarta", [num_words(1), W["nai"], num_words(4)],
          gender=False, meta={"kind": "fraction"})
    B.add("fractions", "dwie trzecie", [num_words(2), W["nai"], num_words(3)],
          gender=False, meta={"kind": "fraction"})
    B.add("fractions", "jedna trzecia (zapis formalny)",
          [W["sèet"], num_words(1), W["sùan"], num_words(3)], gender=False,
          meta={"kind": "fraction", "style": "formal"})
    B.add("fractions", "około stu bahtów",
          [W["prà-maan"], num_words(100), W["bàat"]], gender=False,
          meta={"kind": "approx", "word": "prà-maan"})
    B.add("fractions", "ponad sto bahtów",
          [num_words(100), W["bàat"], W["kwàa"]], gender=False,
          meta={"kind": "approx", "word": "kwàa",
                "note": "kwàa stoi PO liczbie, nie przed nią."})
    B.add("fractions", "prawie sto bahtów",
          [W["kùeap"], num_words(100), W["bàat"]], gender=False,
          meta={"kind": "approx", "word": "kùeap"})
    B.add("fractions", "mniej więcej sto bahtów",
          [num_words(100), W["bàat"], W["raao-raao"]], gender=False,
          meta={"kind": "approx", "word": "raao-raao"})
    B.add("fractions", "więcej niż pięćdziesiąt",
          [W["mâak"], W["kwàa"], num_words(50)], gender=False,
          meta={"kind": "approx", "word": "mâak kwàa"})
    B.add("fractions", "mniej niż pięćdziesiąt",
          [W["náwy"], W["kwàa"], num_words(50)], gender=False,
          meta={"kind": "approx", "word": "náwy kwàa"})

    return B.records


# --- sceny liczbowe ---------------------------------------------------------

def scene_line(index, role, polish, words, speaker="any"):
    n = node(polish, words, gender=(speaker == "any"))
    n["index"] = index
    n["role"] = role
    n["speakerGender"] = speaker
    return n


def build_scenes():
    """Sceny, w których liczba jest sednem, nie tłem.

    Pytania kontrolne pytają o KONKRETNĄ WARTOŚĆ — ile kosztowało, o której,
    który peron. Pytanie o ogólny sens („o czym była ta rozmowa”) da się
    rozstrzygnąć, przespawszy całą liczbę; to jest dokładnie ten błąd, który
    ten moduł ma naprawiać.
    """
    scenes = []

    def scene(sid, title, setting, lines, questions, level="A1"):
        scenes.append({
            "id": sid, "type": "number-scene", "title": title, "setting": setting,
            "level": level, "lines": lines, "questions": questions,
        })

    # --- targowanie się -----------------------------------------------------
    lines = [
        scene_line(1, "A", "Ile kosztuje ta koszulka?",
                   [W["an"], W["níi"], W["raa-khaa"], W["thâo-rài"], W["khráp"]]),
        scene_line(2, "B", "Trzysta pięćdziesiąt bahtów.",
                   [num_words(350), W["bàat"], W["khâ"]], speaker="female"),
        scene_line(3, "A", "Drogo. Może pani opuścić?",
                   [W["phaeng"], W["lót"], W["nòi"], W["dâai"], W["mǎi"], W["khráp"]]),
        scene_line(4, "B", "Trzysta. Taniej się nie da.",
                   [num_words(300), W["bàat"], W["khâ"]], speaker="female"),
        scene_line(5, "A", "Dwieście pięćdziesiąt?",
                   [num_words(250), W["bàat"], W["dâai"], W["mǎi"], W["khráp"]]),
        scene_line(6, "B", "Dwieście osiemdziesiąt. Zgoda.",
                   [num_words(280), W["bàat"], W["khâ"]], speaker="female"),
        scene_line(7, "A", "Dobrze, biorę.", [W["ao"], W["khráp"]]),
    ]
    scene("nscene-001", "Targowanie się o koszulkę", "Na targu",
          lines, [
              {"id": "nscene-001-q1", "prompt": "Ile sprzedawczyni zażądała na początku?",
               "options": ["250 bahtów", "280 bahtów", "300 bahtów", "350 bahtów"],
               "answer": 3, "value": 350,
               "explain": "Pierwsza cena padła w drugiej kwestii: sǎam-ráwy-hâa-sìp bàat."},
              {"id": "nscene-001-q2", "prompt": "Na jakiej cenie stanęło?",
               "options": ["250 bahtów", "280 bahtów", "300 bahtów", "350 bahtów"],
               "answer": 1, "value": 280,
               "explain": "Ostatnia liczba w scenie: sǎwng-ráwy-pàet-sìp bàat."},
              {"id": "nscene-001-q3", "prompt": "O ile udało się zbić cenę?",
               "options": ["o 50 bahtów", "o 70 bahtów", "o 80 bahtów", "wcale"],
               "answer": 1, "value": 70,
               "explain": "350 minus 280. Odjęcie trzeba zrobić samemu — żadna kwestia "
                          "nie podaje różnicy."},
          ])

    # --- rachunek w restauracji --------------------------------------------
    lines = [
        scene_line(1, "A", "Poproszę rachunek.",
                   [W["khǎw"], ("chék-bin", "เช็คบิล"), W["khráp"]]),
        scene_line(2, "B", "Razem czterysta dwadzieścia bahtów.",
                   [("tháng-mòt", "ทั้งหมด"), num_words(420), W["bàat"], W["khâ"]],
                   speaker="female"),
        scene_line(3, "A", "Daję pięćset.",
                   [W["khǎw"], num_words(500), W["khráp"]]),
        scene_line(4, "B", "Reszta osiemdziesiąt bahtów.",
                   [W["thawn"], num_words(80), W["bàat"], W["khâ"]], speaker="female"),
        scene_line(5, "A", "Dziękuję.", [("khàwp-khun", "ขอบคุณ"), W["khráp"]]),
    ]
    scene("nscene-002", "Rachunek i reszta", "W restauracji",
          lines, [
              {"id": "nscene-002-q1", "prompt": "Ile wyniósł rachunek?",
               "options": ["80 bahtów", "420 bahtów", "480 bahtów", "500 bahtów"],
               "answer": 1, "value": 420,
               "explain": "sìi-ráwy-yîi-sìp bàat — druga kwestia."},
              {"id": "nscene-002-q2", "prompt": "Ile powinna wynosić reszta?",
               "options": ["20 bahtów", "80 bahtów", "100 bahtów", "180 bahtów"],
               "answer": 1, "value": 80,
               "explain": "500 minus 420. Kelnerka podała pàet-sìp bàat i się zgadza."},
          ])

    # --- bilet na konkretną godzinę ----------------------------------------
    lines = [
        scene_line(1, "A", "Poproszę bilet do Chiang Mai.",
                   [W["khǎw"], ("tǔa", "ตั๋ว"), ("pai", "ไป"),
                    ("chiang-mài", "เชียงใหม่"), W["khráp"]]),
        scene_line(2, "B", "O której?", [W["kìi"], W["moong"], W["khá"]],
                   speaker="female"),
        scene_line(3, "A", "O ósmej rano.", clock_words(8) + [W["khráp"]]),
        scene_line(4, "B", "O ósmej nie ma. Jest o dziewiątej trzydzieści.",
                   clock_words(9, 30) + [("mii", "มี"), W["khâ"]], speaker="female"),
        scene_line(5, "A", "Dobrze. Peron który?",
                   [W["chaan-chaa-laa"], W["thîi"], W["thâo-rài"], W["khráp"]]),
        scene_line(6, "B", "Peron czwarty. Miejsce dwudzieste drugie.",
                   [W["chaan-chaa-laa"], W["thîi"], num_words(4), W["thîi-nâng"],
                    W["boe"], num_words(22), W["khâ"]], speaker="female"),
    ]
    scene("nscene-003", "Bilet na konkretną godzinę", "Na dworcu",
          lines, [
              {"id": "nscene-003-q1", "prompt": "O której faktycznie odjeżdża autobus?",
               "options": ["08:00", "09:00", "09:30", "10:30"],
               "answer": 2, "value": 930,
               "explain": "kâo moong cháo khrûeng — „khrûeng” to pół godziny, "
                          "nie osobna godzina."},
              {"id": "nscene-003-q2", "prompt": "Z którego peronu?",
               "options": ["z drugiego", "z trzeciego", "z czwartego", "z dwudziestego drugiego"],
               "answer": 2, "value": 4,
               "explain": "chaan-chaa-laa thîi sìi. Liczba 22 padła zaraz potem, "
                          "ale dotyczyła miejsca, nie peronu."},
              {"id": "nscene-003-q3", "prompt": "Który numer ma miejsce?",
               "options": ["4", "9", "22", "30"],
               "answer": 2, "value": 22,
               "explain": "thîi-nâng boe yîi-sìp-sǎwng."},
          ])

    # --- umawianie wizyty ---------------------------------------------------
    lines = [
        scene_line(1, "A", "Chciałbym umówić wizytę.",
                   [("yàak", "อยาก"), ("nát", "นัด"), W["khráp"]]),
        scene_line(2, "B", "Kiedy panu pasuje?",
                   [W["wan"], W["nǎi"], W["dii"], W["khá"]], speaker="female"),
        scene_line(3, "A", "W piątek po południu.",
                   [W["wan"], ("sùk", "ศุกร์"), W["bàai"], W["khráp"]]),
        scene_line(4, "B", "Piątek czternastego, o czternastej trzydzieści?",
                   [W["wan"], ("sùk", "ศุกร์"), W["thîi"], num_words(14)]
                   + clock_words(14, 30) + [W["khá"]], speaker="female"),
        scene_line(5, "A", "Pasuje.", [("dâai", "ได้"), W["khráp"]]),
    ]
    scene("nscene-004", "Umawianie wizyty", "W przychodni",
          lines, [
              {"id": "nscene-004-q1", "prompt": "Na który dzień miesiąca umówiona jest wizyta?",
               "options": ["na 4", "na 14", "na 30", "na 40"],
               "answer": 1, "value": 14,
               "explain": "wan thîi sìp-sìi — czternasty."},
              {"id": "nscene-004-q2", "prompt": "O której godzinie?",
               "options": ["02:30", "14:00", "14:30", "16:30"],
               "answer": 2, "value": 1430,
               "explain": "bàai sǎwng moong khrûeng. `bàai sǎwng` to czternasta — "
                          "licznik po południu startuje od nowa."},
          ])

    # --- podawanie własnego numeru -----------------------------------------
    lines = [
        scene_line(1, "B", "Jaki jest pana numer telefonu?",
                   [W["boe"], W["thoo"], W["thâo-rài"], W["khá"]], speaker="female"),
        scene_line(2, "A", "Zero osiem, dziewięć jeden, dwa trzy, cztery pięć, sześć siedem.",
                   [W["boe"], W["thoo"]] + [(TN.phonetic(d), TN.thai(d))
                                            for d in [0, 8, 9, 1, 2, 3, 4, 5, 6, 7]]
                   + [W["khráp"]]),
        scene_line(3, "B", "Powtórzę: zero osiem, dziewięć jeden, dwa trzy…",
                   [("thúan", "ทวน")] + [(TN.phonetic(d), TN.thai(d))
                                         for d in [0, 8, 9, 1, 2, 3]] + [W["khá"]],
                   speaker="female"),
        scene_line(4, "A", "Zgadza się.", [("thùuk", "ถูก"), ("láew", "แล้ว"), W["khráp"]]),
    ]
    scene("nscene-005", "Podawanie własnego numeru", "Przy rejestracji",
          lines, [
              {"id": "nscene-005-q1", "prompt": "Jakie są trzy pierwsze cyfry numeru?",
               "options": ["0 8 1", "0 8 9", "0 9 8", "8 9 1"],
               "answer": 1, "value": 89,
               "explain": "sǔun pàet kâo. Numer telefonu czyta się cyfra po cyfrze — "
                          "nikt nie mówi „osiemdziesiąt dziewięć”."},
              {"id": "nscene-005-q2", "prompt": "Ile cyfr powtórzyła rozmówczyni?",
               "options": ["cztery", "pięć", "sześć", "wszystkie dziesięć"],
               "answer": 2, "value": 6,
               "explain": "Powtórzyła sześć: sǔun pàet kâo nùeng sǎwng sǎam."},
          ])

    # --- sprawdzanie reszty -------------------------------------------------
    lines = [
        scene_line(1, "A", "Poproszę dwie wody.",
                   [W["khǎw"], ("náam", "น้ำ"), num_words(2), W["khùat"], W["khráp"]]),
        scene_line(2, "B", "Trzydzieści bahtów.",
                   [num_words(30), W["bàat"], W["khâ"]], speaker="female"),
        scene_line(3, "A", "Mam tylko setkę.",
                   [W["mii"], ("tàe", "แต่"), num_words(100), W["khráp"]]),
        scene_line(4, "B", "Reszta sześćdziesiąt bahtów.",
                   [W["thawn"], num_words(60), W["bàat"], W["khâ"]], speaker="female"),
        scene_line(5, "A", "Chyba za mało.",
                   [("mâi", "ไม่"), W["thùuk"], ("ná", "นะ"), W["khráp"]]),
    ]
    scene("nscene-006", "Sprawdzanie reszty", "W sklepie",
          lines, [
              {"id": "nscene-006-q1", "prompt": "Ile powinna wynosić reszta?",
               "options": ["30 bahtów", "60 bahtów", "70 bahtów", "100 bahtów"],
               "answer": 2, "value": 70,
               "explain": "100 minus 30. Sprzedawczyni podała hòk-sìp — o dziesięć za mało."},
              {"id": "nscene-006-q2", "prompt": "Ile reszty faktycznie podała sprzedawczyni?",
               "options": ["30 bahtów", "60 bahtów", "70 bahtów", "100 bahtów"],
               "answer": 1, "value": 60,
               "explain": "thawn hòk-sìp bàat. Różnica między tym a rachunkiem jest "
                          "właśnie powodem, dla którego ostatnia kwestia brzmi jak brzmi."},
          ])

    return scenes


# --- lekcje i ćwiczenia -----------------------------------------------------

LESSON_PLAN = [
    ("num-lesson-01", "Liczby 0–10 ze słuchu", "Survival", 3,
     "Dziesięć cyfr rozpoznawanych ze słuchu, bez zapisu przed oczami. "
     "To jest warunek wszystkiego dalej: bez cyfr nie ma ani ceny, ani godziny.",
     ["numerals"], (0, 10), ["dictation"]),
    ("num-lesson-02", "Jedenaście–dziewiętnaście i dziesiątki", "Survival", 6,
     "Trzy nieregularności naraz: niema dziesiątka w sìp, èt zamiast nùeng "
     "w jedności i yîi-sìp zamiast sǎwng-sìp. Tu przepada najwięcej ludzi.",
     ["numerals"], (11, 99), ["dictation", "produce"]),
    ("num-lesson-03", "Setki, tysiące i cały system do miliona", "A1", 10,
     "Reszta systemu jest już regularna — pozycja razy cyfra. Ćwiczymy tempo, "
     "nie regułę.", ["numerals"], (100, 1000000), ["dictation", "sequence"]),
    ("num-lesson-04", "Ceny: baht i satang", "Survival", 14,
     "Kwota ze słuchu i wybór właściwego banknotu. Cena pada raz i szybko — "
     "drugie podejście w sklepie kosztuje.", ["prices"], None, ["price", "change"]),
    ("num-lesson-05", "Godziny w systemie sześciogodzinnym", "A1", 22,
     "Doba dzielona na cztery odcinki, w każdym licznik od nowa. "
     "`sìi moong cháo` i `sìi moong yen` różnią się jednym słowem i sześcioma godzinami.",
     ["clock"], None, ["clock"]),
    ("num-lesson-06", "Dni tygodnia i miesiące", "A1", 40,
     "Nazwy miesięcy niosą liczbę dni w samej końcówce: -khom to 31, -yon to 30.",
     ["dates"], None, ["dictation"]),
    ("num-lesson-07", "Lata: kalendarz buddyjski i gregoriański", "A2", 60,
     "Rok buddyjski to gregoriański plus 543. Data urodzenia w dokumencie "
     "będzie w tym pierwszym.", ["dates"], None, ["produce"]),
    ("num-lesson-08", "Czas trwania i częstotliwość", "A2", 85,
     "Od–do, co ile, przez ile. Konstrukcje, bez których nie da się umówić "
     "niczego powtarzalnego.", ["duration"], None, ["dictation", "produce"]),
    ("num-lesson-09", "Numery: telefon, pokój, autobus, peron, miejsce", "A2", 110,
     "Numer nie jest liczbą — czyta się go cyfra po cyfrze. Ćwiczenie ciągu "
     "sprawdza pamięć słuchową, nie arytmetykę.", ["serials"], None, ["sequence"]),
    ("num-lesson-10", "Ilości z klasyfikatorami", "A2", 140,
     "Liczba bez klasyfikatora jest w tajskim niegramatyczna. „Jeden” to "
     "jedyna liczba, która staje PO klasyfikatorze.", ["quantities"], None,
     ["produce"]),
    ("num-lesson-11", "Ułamki i wartości przybliżone", "B1", 175,
     "Około, ponad, prawie, mniej więcej — i to, że kwàa stoi po liczbie, "
     "a prà-maan przed nią.", ["fractions"], None, ["dictation", "produce"]),
]

DRILLS = [
    ("dictation", "Dyktando liczbowe",
     "Słuchasz liczby, wpisujesz ją cyframi. Nie tłumaczysz — zapisujesz.",
     8000, 2500),
    ("price", "Cena ze słuchu",
     "Słuchasz kwoty i wybierasz właściwy banknot albo właściwą sumę.",
     7000, 2200),
    ("clock", "Godzina ze słuchu",
     "Słuchasz godziny i ustawiasz ją na tarczy zegara.",
     9000, 3000),
    ("produce", "Produkcja: powiedz liczbę",
     "Widzisz liczbę cyframi, mówisz ją po tajsku. Ocena konturu tonalnego "
     "z sesji J rozstrzyga, czy trafiłeś.", 10000, 3500),
    ("change", "Reszta",
     "Ile wydać z podanej kwoty. Liczenie po tajsku pod presją czasu.",
     12000, 4000),
    ("sequence", "Ciąg cyfr",
     "Kilka liczb pod rząd — zapamiętaj i odtwórz. Tak podaje się numer telefonu.",
     12000, 4500),
]


def build_lessons(records, lessons_path):
    with open(lessons_path, encoding="utf-8") as fh:
        path = json.load(fh)
    by_number = {L["number"]: L for L in path["records"]}
    total = len(path["records"])

    by_section = {}
    for r in records:
        by_section.setdefault(r["section"], []).append(r)

    out = []
    for lid, title, level, after, goal, sections, rng, drills in LESSON_PLAN:
        anchor = by_number.get(after)
        if anchor is None:
            raise SystemExit("brak lekcji o numerze %d w ścieżce (%d lekcji)"
                             % (after, total))
        ids = []
        for s in sections:
            for r in by_section.get(s, []):
                v = (r.get("meta") or {}).get("value")
                if rng and isinstance(v, int) and not (rng[0] <= v <= rng[1]):
                    continue
                if rng and not isinstance(v, int):
                    continue
                ids.append(r["id"])
        out.append({
            "id": lid, "title": title, "level": level, "goal": goal,
            "anchorAfter": anchor["id"], "anchorNumber": after,
            "sections": sections, "itemIds": ids, "drills": drills,
            "pass": {"questions": max(8, min(14, len(ids))),
                     "correct": max(7, int(round(0.8 * max(8, min(14, len(ids))))))},
        })
    return out


# --- główna -----------------------------------------------------------------

def main():
    records = build_records()
    scenes = build_scenes()
    lessons = build_lessons(records, os.path.join(DATA, "lessons.json"))

    digits = []
    for i, (ph, th) in enumerate(TN.DIGITS):
        digits.append({"value": i, "thaiPhonetic": ph, "ttsThai": th,
                       "pronunciationPolish": EN.polish_read(ph),
                       "toneGuide": EN.tone_guide(ph)})
    positions = []
    for value, ph, th in TN.POSITIONS:
        positions.append({"value": value, "thaiPhonetic": ph, "ttsThai": th,
                          "pronunciationPolish": EN.polish_read(ph)})

    def atom(pair):
        return {"thaiPhonetic": pair[0], "ttsThai": pair[1],
                "pronunciationPolish": EN.polish_read(pair[0])}

    # Punkty kontrolne: liczby, na których reguła najczęściej się łamie, plus
    # rozrzut po całym zakresie. Walidator i tak sprawdza CAŁY zakres regułą —
    # te wpisy są po to, żeby rozjazd między plikiem a regułą był widoczny
    # od razu, także dla kogoś, kto czyta sam plik.
    checkpoint_values = ([n for n in range(0, 31)]
                         + [40, 50, 90, 99, 100, 101, 105, 110, 111, 120, 121,
                            200, 555, 999, 1000, 1001, 1010, 1100, 2568,
                            10000, 10001, 12345, 100000, 123456, 999999, 1000000])
    checkpoints = []
    for n in checkpoint_values:
        ph = TN.phonetic(n)
        checkpoints.append({"n": n, "thaiPhonetic": ph,
                            "irregular": TN.irregular_kinds(n)})

    payload = {
        "file": "numbers.json",
        "generator": "tools/generators/numbers.py",
        "version": VERSION,
        "count": len(records),
        "range": {"min": 0, "max": TN.MAX},
        "atoms": {
            "digits": digits,
            "positions": positions,
            "et": atom(TN.ET),
            "yii": atom(TN.YII),
            "million": atom(TN.MILLION),
        },
        "irregularities": [
            {"id": k, "label": v,
             "examples": [n for n in checkpoint_values if k in TN.irregular_kinds(n)][:6]}
            for k, v in sorted(TN.IRREGULAR_LABELS.items())
        ],
        "checkpoints": checkpoints,
        "sections": [
            {"id": "numerals", "title": "Liczebniki 0–1 000 000",
             "lead": "System pozycyjny z pięcioma nieregularnościami. Reszta jest "
                     "regularna — cyfra razy pozycja."},
            {"id": "prices", "title": "Ceny: baht i satang",
             "lead": "Kwota pada raz i szybko. Na targu usłyszysz też salueng — "
                     "ćwierć bahta."},
            {"id": "clock", "title": "Godziny — system sześciogodzinny",
             "lead": "Doba w czterech odcinkach, w każdym licznik od nowa.",
             "dayParts": [
                 {"id": p[0], "range": p[1], "from": p[2], "to": p[3],
                  "polish": p[4], "trap": p[5]} for p in DAY_PARTS]},
            {"id": "dates", "title": "Daty: dni, miesiące, lata",
             "lead": MONTH_HINT + " Rok w dokumentach jest buddyjski: gregoriański plus 543."},
            {"id": "duration", "title": "Czas trwania i częstotliwość",
             "lead": "Od–do, co ile, przez ile."},
            {"id": "serials", "title": "Numery",
             "lead": "Numer to nie liczba. Czyta się go cyfra po cyfrze."},
            {"id": "quantities", "title": "Ilości z klasyfikatorami",
             "lead": "Liczba bez klasyfikatora jest niegramatyczna. Pełny wykaz "
                     "klasyfikatorów leży w data/classifiers.json."},
            {"id": "fractions", "title": "Ułamki i wartości przybliżone",
             "lead": "prà-maan stoi przed liczbą, kwàa po niej."},
        ],
        "drills": [
            {"id": d[0], "label": d[1], "lead": d[2],
             "limitMs": d[3], "masteryMs": d[4]} for d in DRILLS
        ],
        "lessons": lessons,
        "scenes": scenes,
        "records": records,
    }

    jsonio.dump(payload, os.path.join(DATA, "numbers.json"))
    print("numbers.json: %d rekordów, %d lekcji, %d scen, %d punktów kontrolnych"
          % (len(records), len(lessons), len(scenes), len(checkpoints)))


if __name__ == "__main__":
    main()
