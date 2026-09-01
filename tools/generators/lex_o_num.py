# -*- coding: utf-8 -*-
"""Sesja O, partia 18 — LICZBY: liczebniki złożone, działania, jednostki.

Kategoria Liczby i liczenie miała 101 haseł — najwięcej z nich to same
cyfry. Brakowało tego, co się z liczbami robi: składania ich, porównywania,
podawania cen, dat i numerów.

Tajski system liczebników jest regularny i dlatego opłaca się go domknąć
w jednej partii:

    20      yîi sìp        (nie „sǎwng sìp” — dwudziestka jest nieregularna)
    21      yîi sìp èt     (jedynka na końcu to `èt`, nie `nùeng`)
    100     nùeng ráwi
    1 000   nùeng phan
    10 000  nùeng mùen     (osobne słowo, nie „dziesięć tysięcy”)
    100 000 nùeng sǎen
    milion  nùeng láan

Dwie pułapki, przez które turysta przepłaca: `èt` na końcu i `mùen`/`sǎen`,
których w europejskich językach nie ma. Cena „sǎwng mùen” to 20 000, a nie
dwadzieścia.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

LI = "Liczby i liczenie"
ZP = "Zakupy i pieniądze"
CD = "Czas i daty"
PN = "Praca i nauka"
PY = "Pytania"
GU = "Gramatyka użytkowa"
CO = "Cechy i opinie"
AW = "Awarie i pomoc"
TR = "Transport"

NUM = [

# =========================================================== liczebniki
("A1", "dwadzieścia", "yîi sìp", "ยี่สิบ", "Liczebniki", 5, "n", LI,
 "Nieregularne: nie „sǎwng sìp”. Jedyna taka dziesiątka.", ""),
("A1", "dwadzieścia jeden", "yîi sìp èt", "ยี่สิบเอ็ด", "Liczebniki", 5, "n", LI,
 "Jedynka na końcu liczby to zawsze èt, nigdy nùeng.", ""),
("A1", "trzydzieści", "sǎam sìp", "สามสิบ", "Liczebniki", 5, "n", LI, "", ""),
("A1", "czterdzieści", "sìi sìp", "สี่สิบ", "Liczebniki", 4, "n", LI, "", ""),
("A1", "pięćdziesiąt", "hâa sìp", "ห้าสิบ", "Liczebniki", 5, "n", LI, "", ""),
("A1", "sześćdziesiąt", "hòk sìp", "หกสิบ", "Liczebniki", 4, "n", LI, "", ""),
("A1", "siedemdziesiąt", "jèt sìp", "เจ็ดสิบ", "Liczebniki", 4, "n", LI, "", ""),
("A1", "osiemdziesiąt", "pàet sìp", "แปดสิบ", "Liczebniki", 4, "n", LI, "", ""),
("A1", "dziewięćdziesiąt", "kâo sìp", "เก้าสิบ", "Liczebniki", 4, "n", LI, "", ""),
("A1", "sto", "nùeng ráwi", "หนึ่งร้อย", "Liczebniki", 5, "n", LI, "", ""),
("A1", "dwieście", "sǎwng ráwi", "สองร้อย", "Liczebniki", 5, "n", LI, "", ""),
("A1", "pięćset", "hâa ráwi", "ห้าร้อย", "Liczebniki", 5, "n", LI,
 "Najczęstszy banknot w Tajlandii — fioletowy.", ""),
("A1", "tysiąc", "nùeng phan", "หนึ่งพัน", "Liczebniki", 5, "n", LI, "", ""),
("A1", "dwa tysiące", "sǎwng phan", "สองพัน", "Liczebniki", 4, "n", LI, "", ""),
("A1", "dziesięć tysięcy", "nùeng mùen", "หนึ่งหมื่น", "Liczebniki", 4, "n", LI,
 "Osobne słowo. Cena „sǎwng mùen” to 20 000, nie dwadzieścia.", ""),
("A1", "sto tysięcy", "nùeng sǎen", "หนึ่งแสน", "Liczebniki", 3, "n", LI, "", ""),
("A1", "milion", "nùeng láan", "หนึ่งล้าน", "Liczebniki", 3, "n", LI, "", ""),
("A2", "półtora", "nùeng khrûeng", "หนึ่งครึ่ง", "Liczebniki", 3, "n", LI, "", ""),
("A2", "para (dwa)", "sǎwng an", "สองอัน", "Liczebniki", 4, "n", LI, "", ""),
("A2", "zero", "sǔun", "ศูนย์", "Liczebniki", 4, "n", LI,
 "To samo słowo znaczy „centrum” — sǔun kaan kháa, centrum handlowe.", ""),

# =========================================================== porządkowe
("A1", "pierwszy", "thîi nùeng", "ที่หนึ่ง", "Porządkowe", 5, "adj", LI, "", ""),
("A1", "drugi", "thîi sǎwng", "ที่สอง", "Porządkowe", 5, "adj", LI, "", ""),
("A1", "trzeci", "thîi sǎam", "ที่สาม", "Porządkowe", 4, "adj", LI, "", ""),
("A1", "czwarty", "thîi sìi", "ที่สี่", "Porządkowe", 3, "adj", LI, "", ""),
("A1", "piąty", "thîi hâa", "ที่ห้า", "Porządkowe", 3, "adj", LI, "", ""),
("A2", "ostatni (w kolejności)", "an sùt tháai", "อันสุดท้าย", "Porządkowe", 4, "adj", LI, "", ""),
("A2", "przedostatni", "an kàwn sùt tháai", "อันก่อนสุดท้าย", "Porządkowe", 2, "adj", LI, "", ""),
("A2", "co drugi", "wén nùeng", "เว้นหนึ่ง", "Porządkowe", 2, "adj", LI, "", "omijając jeden"),
("A2", "kolejność", "lam-dàp", "ลำดับ", "Porządkowe", 3, "n", LI, "", ""),

# =========================================================== działania
("A1", "dodawać", "bùak", "บวก", "Działania", 4, "v", LI, "", ""),
("A1", "odejmować", "lóp", "ลบ", "Działania", 4, "v", LI,
 "To samo słowo znaczy „wymazać, usunąć”.", ""),
("A1", "mnożyć", "khuun", "คูณ", "Działania", 3, "v", LI, "", ""),
("A1", "dzielić", "hǎan", "หาร", "Działania", 3, "v", LI, "", ""),
("A1", "równa się", "thâo kàp", "เท่ากับ", "Działania", 4, "v", LI, "", "równy z"),
("A2", "suma", "phǒn bùak", "ผลบวก", "Działania", 2, "n", LI, "", "wynik dodawania"),
("A2", "iloczyn", "phǒn khuun", "ผลคูณ", "Działania", 2, "n", LI, "", ""),
("A2", "reszta z dzielenia", "sèet", "เศษ", "Działania", 2, "n", LI, "", ""),
("A2", "ułamek", "sèet sùan", "เศษส่วน", "Działania", 2, "n", LI, "", "reszta część"),
("A2", "połowa czegoś", "khrûeng nùeng khǎwng", "ครึ่งหนึ่งของ", "Działania", 3, "n", LI, "", ""),
("A2", "jedna trzecia", "nùeng nai sǎam", "หนึ่งในสาม", "Działania", 2, "n", LI, "", "jeden w trzech"),
("A2", "podwójny", "khûu", "คู่", "Działania", 3, "adj", LI, "", ""),
("A2", "pojedynczy", "dìao", "เดี่ยว", "Działania", 3, "adj", LI, "", ""),
("A2", "przybliżona liczba", "tua lêek prà-maan", "ตัวเลขประมาณ", "Działania", 2, "n", LI, "", ""),
("A2", "dokładna liczba", "tua lêek thǽe jing", "ตัวเลขแท้จริง", "Działania", 2, "n", LI, "", ""),

# =========================================================== ceny
("A1", "bat (waluta)", "bàat", "บาท", "Ceny", 5, "n", ZP, "", ""),
("A1", "satang (grosz)", "sà-taang", "สตางค์", "Ceny", 3, "n", ZP,
 "Setna część bata. W praktyce ceny zaokrągla się do bata.", ""),
("A1", "cena za sztukę", "raa-khaa tàw an", "ราคาต่ออัน", "Ceny", 4, "n", ZP, "", ""),
("A1", "cena za kilogram", "raa-khaa tàw kì-loo", "ราคาต่อกิโล", "Ceny", 4, "n", ZP, "", ""),
("A1", "cena stała", "raa-khaa taai tua", "ราคาตายตัว", "Ceny", 3, "n", ZP,
 "Napis, przy którym targowanie się nie ma sensu.", "cena martwa"),
("A1", "zniżka", "sùan lót", "ส่วนลด", "Ceny", 5, "n", ZP, "", "część obniżona"),
("A1", "wyprzedaż", "lót raa-khaa", "ลดราคา", "Ceny", 5, "n", ZP, "", ""),
("A1", "darmowy", "frii", "ฟรี", "Ceny", 5, "adj", ZP, "", ""),
("A2", "dwa w cenie jednego", "súe nùeng thǎem nùeng", "ซื้อหนึ่งแถมหนึ่ง", "Ceny", 3, "n", ZP, "", "kup jeden dodaj jeden"),
("A2", "cena z podatkiem", "raa-khaa ruam phaa-sǐi", "ราคารวมภาษี", "Ceny", 3, "n", ZP, "", ""),
("A2", "cena netto", "raa-khaa mâi ruam phaa-sǐi", "ราคาไม่รวมภาษี", "Ceny", 2, "n", ZP, "", ""),
("A2", "opłata dodatkowa", "khâa chái jàai phôoem", "ค่าใช้จ่ายเพิ่ม", "Ceny", 3, "n", ZP, "", ""),
("A2", "kaucja zwrotna", "ngoen mát-jam khuen dâi", "เงินมัดจำคืนได้", "Ceny", 2, "n", ZP, "", ""),
("A2", "podwyżka ceny", "khûen raa-khaa", "ขึ้นราคา", "Ceny", 3, "n", ZP, "", ""),
("A2", "obniżka ceny", "long raa-khaa", "ลงราคา", "Ceny", 3, "n", ZP, "", ""),
("A2", "cena hurtowa", "raa-khaa sòng", "ราคาส่ง", "Ceny", 3, "n", ZP, "", ""),
("A2", "cena detaliczna", "raa-khaa plìik", "ราคาปลีก", "Ceny", 2, "n", ZP, "", ""),
("A2", "drogo jak na to", "phaeng sǎm-ràp an níi", "แพงสำหรับอันนี้", "Ceny", 3, "adj", CO, "", ""),

# =========================================================== numery
("A1", "numer domu", "bâan lêek thîi", "บ้านเลขที่", "Numery", 4, "n", AW, "", "dom numer"),
("A1", "numer pokoju", "lêek hâwng", "เลขห้อง", "Numery", 4, "n", AW, "", ""),
("A1", "numer miejsca", "lêek thîi nâng", "เลขที่นั่ง", "Numery", 4, "n", TR, "", ""),
("A1", "numer lotu", "thîao bin thîi", "เที่ยวบินที่", "Numery", 3, "n", TR, "", ""),
("A1", "numer peronu", "chaan chaa-laa thîi", "ชานชาลาที่", "Numery", 3, "n", TR, "", ""),
("A1", "numer rejestracyjny", "thá-bian rót", "ทะเบียนรถ", "Numery", 3, "n", TR, "", ""),
("A2", "numer konta", "lêek thîi ban-chii", "เลขที่บัญชี", "Numery", 3, "n", ZP, "", ""),
("A2", "numer dokumentu", "lêek èek-kà-sǎan", "เลขเอกสาร", "Numery", 2, "n", PN, "", ""),
("A2", "kod pocztowy", "rá-hàt prai-sà-nii", "รหัสไปรษณีย์", "Numery", 3, "n", AW, "", ""),
("A2", "numer kierunkowy", "rá-hàt thoo", "รหัสโทร", "Numery", 2, "n", AW, "", ""),
("A2", "numer alarmowy", "boe chùk-chə̌ən", "เบอร์ฉุกเฉิน", "Numery", 4, "n", AW,
 "Policja turystyczna: 1155. Pogotowie: 1669.", ""),

# =========================================================== daty liczbowo
("A1", "rok (jednostka)", "pii", "ปี", "Daty", 5, "n", CD, "", ""),
("A1", "wiek (stulecie)", "sàt-tà-wát", "ศตวรรษ", "Daty", 2, "n", CD, "", ""),
("A1", "dekada", "thót-sà-wát", "ทศวรรษ", "Daty", 2, "n", CD, "", ""),
("A2", "pierwszego stycznia", "wan thîi nùeng mók-kà-raa", "วันที่หนึ่งมกรา", "Daty", 3, "n", CD, "", ""),
("A2", "w tym roku", "pii níi", "ปีนี้", "Daty", 5, "n", CD, "", ""),
("A2", "przez dwa lata", "sǎwng pii", "สองปี", "Daty", 4, "n", CD, "", ""),
("A2", "od dwóch lat", "tâng tàe sǎwng pii kàwn", "ตั้งแต่สองปีก่อน", "Daty", 3, "n", CD, "", ""),
("A2", "co roku", "thúk pii", "ทุกปี", "Daty", 4, "adv", CD, "", ""),
("A2", "co miesiąc", "thúk duean", "ทุกเดือน", "Daty", 5, "adv", CD, "", ""),
("A2", "raz na dwa tygodnie", "sǎwng aa-thít khráng", "สองอาทิตย์ครั้ง", "Daty", 3, "adv", CD, "", ""),

# =========================================================== opis ilościowy
("A1", "podwoić", "phôoem pen sǎwng thâo", "เพิ่มเป็นสองเท่า", "Zmiana", 2, "v", LI, "", ""),
("A1", "zwiększyć", "phôoem", "เพิ่ม", "Zmiana", 5, "v", LI, "", ""),
("A1", "zmniejszyć", "lót", "ลด", "Zmiana", 5, "v", LI, "", ""),
("A1", "policzyć razem", "ruam", "รวม", "Zmiana", 5, "v", LI, "", ""),
("A2", "podzielić po równo", "bàeng thâo kan", "แบ่งเท่ากัน", "Zmiana", 3, "v", LI, "", ""),
("A2", "zaokrąglić w górę", "pàt khûen", "ปัดขึ้น", "Zmiana", 2, "v", LI, "", ""),
("A2", "zaokrąglić w dół", "pàt long", "ปัดลง", "Zmiana", 2, "v", LI, "", ""),
("A2", "przeliczyć na baty", "khít pen bàat", "คิดเป็นบาท", "Zmiana", 3, "v", ZP, "", ""),
("A2", "wzrost o dziesięć procent", "khûen sìp poe-sen", "ขึ้นสิบเปอร์เซ็นต์", "Zmiana", 2, "n", LI, "", ""),
("A2", "spadek o połowę", "lót khrûeng nùeng", "ลดครึ่งหนึ่ง", "Zmiana", 2, "n", LI, "", ""),

# =========================================================== pytania liczbowe
("A1", "Ile to kosztuje razem?", "tháng mòt thâo rài khráp", "ทั้งหมดเท่าไหร่ครับ", "Pytania", 5, "w", PY, "", ""),
("A1", "Ile za sztukę?", "an lá thâo rài khráp", "อันละเท่าไหร่ครับ", "Pytania", 5, "w", PY, "", ""),
("A1", "Ile za kilogram?", "kì-loo lá thâo rài khráp", "กิโลละเท่าไหร่ครับ", "Pytania", 5, "w", PY, "", ""),
("A1", "Jaki jest numer?", "lêek à-rai khráp", "เลขอะไรครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Czy jest zniżka?", "mii sùan lót mǎi khráp", "มีส่วนลดไหมครับ", "Pytania", 5, "w", PY, "", ""),
("A2", "Ile procent zniżki?", "lót kìi poe-sen khráp", "ลดกี่เปอร์เซ็นต์ครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Możesz opuścić?", "lót dâi mǎi khráp", "ลดได้ไหมครับ", "Pytania", 5, "w", ZP,
 "Standardowe otwarcie targowania na straganie. W sklepie sieciowym nie działa.", ""),
("A2", "To za drogo dla mnie.", "phaeng kooen pai sǎm-ràp phǒm khráp", "แพงเกินไปสำหรับผมครับ", "Pytania", 5, "w", ZP, "", ""),
("A2", "Wezmę dwie sztuki.", "ao sǎwng an khráp", "เอาสองอันครับ", "Pytania", 5, "w", ZP, "", ""),
("A2", "Proszę policzyć jeszcze raz.", "chûai khít ìik thii khráp", "ช่วยคิดอีกทีครับ", "Pytania", 4, "w", ZP, "", ""),
("A2", "Reszta się nie zgadza.", "ngoen thawn mâi thùuk khráp", "เงินทอนไม่ถูกครับ", "Pytania", 4, "w", ZP, "", ""),
("A2", "Nie mam drobnych.", "mâi mii ngoen yâwi khráp", "ไม่มีเงินย่อยครับ", "Pytania", 5, "w", ZP,
 "Częsty problem: kierowcy i sprzedawcy nie wydają z tysiąca.", ""),
]
