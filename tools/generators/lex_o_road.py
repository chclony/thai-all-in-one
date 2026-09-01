# -*- coding: utf-8 -*-
"""Sesja O, partia 19 — POJAZD, DROGA, PRAWO, URZĄD.

Dwie warstwy o wspólnej cesze: obie potrzebne dopiero, gdy coś pójdzie nie
tak — i wtedy potrzebne natychmiast.

1. **Pojazd i jego części.** Wynajęcie skutera to w Tajlandii rzecz
   codzienna. Kiedy przestaje działać, uczący się musi nazwać część, a nie
   pokazać palcem, bo zwykle rozmawia przez telefon. Kategoria Transport
   miała 91 haseł, prawie wyłącznie o jeżdżeniu, nie o pojeździe.

2. **Prawo, policja, urząd.** Mandat, protokół, ubezpieczenie, zeznanie.
   Kategoria Awarie i pomoc miała 43 hasła — najmniej po Pytaniach.

Uwaga praktyczna wpleciona w hasła: kask, prawo jazdy i ubezpieczenie to
trzy rzeczy sprawdzane przy każdej kontroli i przy każdej szkodzie.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

TR = "Transport"
AW = "Awarie i pomoc"
ZP = "Zakupy i pieniądze"
PN = "Praca i nauka"
PY = "Pytania"
CZ = "Czasowniki"
MO = "Miejsca i orientacja"
CO = "Cechy i opinie"
ZD = "Zdrowie"
LR = "Ludzie i rodzina"

ROAD = [

# =========================================================== części pojazdu
("A1", "kierownica", "phuang maa-lai", "พวงมาลัย", "Pojazd", 3, "n", TR, "", ""),
("A1", "hamulec", "brèek", "เบรก", "Pojazd", 4, "n", TR, "", ""),
("A1", "gaz (pedał)", "khan rêng", "คันเร่ง", "Pojazd", 3, "n", TR, "", ""),
("A1", "sprzęgło", "khlát", "คลัตช์", "Pojazd", 2, "n", TR, "", ""),
("A1", "silnik", "khrûeang yon", "เครื่องยนต์", "Pojazd", 4, "n", TR, "", ""),
("A1", "koło", "láw", "ล้อ", "Pojazd", 4, "n", TR, "", ""),
("A1", "opona", "yaang rót", "ยางรถ", "Pojazd", 4, "n", TR, "", "guma pojazd"),
("A1", "lusterko", "krà-jòk mawng lǎng", "กระจกมองหลัง", "Pojazd", 3, "n", TR, "", "szkło patrzeć w tył"),
("A1", "szyba przednia", "krà-jòk nâa", "กระจกหน้า", "Pojazd", 3, "n", TR, "", ""),
("A1", "reflektor", "fai nâa", "ไฟหน้า", "Pojazd", 4, "n", TR, "", "światło przód"),
("A1", "kierunkowskaz", "fai líao", "ไฟเลี้ยว", "Pojazd", 3, "n", TR, "", "światło skręt"),
("A1", "klakson", "trae", "แตร", "Pojazd", 3, "n", TR, "", ""),
("A1", "bagażnik", "krà-prong lǎng", "กระโปรงหลัง", "Pojazd", 3, "n", TR, "", ""),
("A1", "siedzenie", "thîi nâng", "ที่นั่ง", "Pojazd", 5, "n", TR, "", "miejsce siedzieć"),
("A1", "pas bezpieczeństwa", "khěm khàt ní-rá-phai", "เข็มขัดนิรภัย", "Pojazd", 4, "n", TR, "", "pas bezpieczeństwa"),
("A2", "akumulator", "báet-toe-rîi rót", "แบตเตอรี่รถ", "Pojazd", 3, "n", AW, "", ""),
("A2", "bak paliwa", "thǎng nám man", "ถังน้ำมัน", "Pojazd", 3, "n", TR, "", "zbiornik olej"),
("A2", "benzyna", "nám man ben-sin", "น้ำมันเบนซิน", "Pojazd", 4, "n", TR, "", ""),
("A2", "olej silnikowy", "nám man khrûeang", "น้ำมันเครื่อง", "Pojazd", 3, "n", AW, "", ""),
("A2", "skrzynia biegów", "kìa", "เกียร์", "Pojazd", 3, "n", TR, "", ""),
("A2", "automat (skrzynia)", "kìa àw-too", "เกียร์ออโต้", "Pojazd", 3, "n", TR, "", ""),
("A2", "łańcuch (w motocyklu)", "sôo rót", "โซ่รถ", "Pojazd", 2, "n", AW, "", ""),
("A2", "stopka (w skuterze)", "khǎa tâng", "ขาตั้ง", "Pojazd", 2, "n", TR, "", ""),
("A2", "licznik kilometrów", "mí-tôe rá-yá thaang", "มิเตอร์ระยะทาง", "Pojazd", 2, "n", TR, "", ""),
("A2", "kluczyk", "kun-jae rót", "กุญแจรถ", "Pojazd", 4, "n", TR, "", ""),

# =========================================================== awarie drogowe
("A1", "flak w oponie", "yaang bâen", "ยางแบน", "Awarie", 4, "n", AW, "", "opona płaska"),
("A1", "brak paliwa", "nám man mòt", "น้ำมันหมด", "Awarie", 4, "n", AW, "", "paliwo skończone"),
("A1", "silnik nie odpala", "sà-tàat mâi tìt", "สตาร์ทไม่ติด", "Awarie", 4, "n", AW, "", ""),
("A1", "przegrzanie silnika", "khrûeang ráwn kooen", "เครื่องร้อนเกิน", "Awarie", 2, "n", AW, "", ""),
("A1", "stłuczka", "chon lék náwi", "ชนเล็กน้อย", "Awarie", 3, "n", AW, "", "uderzenie małe"),
("A1", "wypadek drogowy", "ù-bàt-tì-hèet bon thà-nǒn", "อุบัติเหตุบนถนน", "Awarie", 4, "n", AW, "", ""),
("A2", "holowanie", "lâak rót", "ลากรถ", "Awarie", 3, "n", AW, "", "ciągnąć pojazd"),
("A2", "pomoc drogowa", "rót yók", "รถยก", "Awarie", 3, "n", AW, "", "pojazd podnoszący"),
("A2", "koszt naprawy", "khâa sâwm", "ค่าซ่อม", "Awarie", 4, "n", AW, "", ""),
("A2", "części zamienne", "à-lài", "อะไหล่", "Awarie", 3, "n", AW, "", ""),
("A2", "gwarancja", "kaan ráp prà-kan", "การรับประกัน", "Awarie", 3, "n", ZP, "", ""),
("A2", "przegląd techniczny", "trùat sà-phâap rót", "ตรวจสภาพรถ", "Awarie", 2, "n", TR, "", ""),
("A2", "wymiana oleju", "plìan thàai nám man", "เปลี่ยนถ่ายน้ำมัน", "Awarie", 2, "n", AW, "", ""),
("A2", "pompować koło", "toem lom yaang", "เติมลมยาง", "Awarie", 3, "v", CZ, "", "napełnić powietrze opona"),
("A2", "zatankować", "toem nám man", "เติมน้ำมัน", "Awarie", 5, "v", CZ, "", ""),
("A2", "uruchomić silnik", "sà-tàat khrûeang", "สตาร์ทเครื่อง", "Awarie", 3, "v", CZ, "", ""),
("A2", "zgasić silnik", "dàp khrûeang", "ดับเครื่อง", "Awarie", 3, "v", CZ, "", ""),

# =========================================================== ruch drogowy
("A1", "znak drogowy", "pâai jà-raa-jawn", "ป้ายจราจร", "Ruch", 3, "n", MO, "", ""),
("A1", "pas ruchu", "chông thaang", "ช่องทาง", "Ruch", 3, "n", TR, "", ""),
("A1", "jednokierunkowa", "thaang diao", "ทางเดียว", "Ruch", 3, "n", TR, "", "droga jedna"),
("A1", "zakaz parkowania", "hâam jàwt", "ห้ามจอด", "Ruch", 4, "n", TR, "", ""),
("A1", "zakaz wjazdu", "hâam khâo", "ห้ามเข้า", "Ruch", 4, "n", TR, "", ""),
("A1", "ograniczenie prędkości", "jam-kàt khwaam reo", "จำกัดความเร็ว", "Ruch", 3, "n", TR, "", ""),
("A2", "kontrola drogowa", "dàan trùat", "ด่านตรวจ", "Ruch", 4, "n", AW,
 "Częste zwłaszcza wieczorami. Sprawdzają kask i prawo jazdy.", ""),
("A2", "badanie alkomatem", "pào lom trùat àen-kaw-hawn", "เป่าลมตรวจแอลกอฮอล์", "Ruch", 2, "n", AW, "", ""),
("A2", "kara pieniężna", "khâa pràp", "ค่าปรับ", "Ruch", 4, "n", AW, "", ""),
("A2", "zabranie prawa jazdy", "yúet bai khàp khìi", "ยึดใบขับขี่", "Ruch", 2, "n", AW, "", ""),
("A2", "jechać za szybko", "khàp reo kooen", "ขับเร็วเกิน", "Ruch", 3, "v", CZ, "", ""),
("A2", "wyprzedzać", "saeng", "แซง", "Ruch", 4, "v", CZ, "", ""),
("A2", "ustąpić pierwszeństwa", "hâi thaang", "ให้ทาง", "Ruch", 3, "v", CZ, "", "dawać drogę"),
("A2", "zatrzymać się na czerwonym", "yùt fai daeng", "หยุดไฟแดง", "Ruch", 4, "v", CZ, "", ""),
("A2", "zapiąć pas", "khàt khěm khàt", "คาดเข็มขัด", "Ruch", 3, "v", CZ, "", ""),
("A2", "założyć kask", "sài mùak kan náwk", "ใส่หมวกกันน็อค", "Ruch", 5, "v", CZ, "", ""),

# =========================================================== policja i prawo
("A1", "policjant", "tam-rùat", "ตำรวจ", "Prawo", 5, "n", AW, "", ""),
("A1", "policja turystyczna", "tam-rùat thâwng thîao", "ตำรวจท่องเที่ยว", "Prawo", 4, "n", AW,
 "Numer 1155, mówią po angielsku. Pierwszy kontakt przy problemie turysty.", ""),
("A1", "protokół, zgłoszenie", "bai jâeng khwaam", "ใบแจ้งความ", "Prawo", 4, "n", AW,
 "Dokument potrzebny do ubezpieczenia. Bez niego szkody nie zgłosisz.", ""),
("A1", "przestępstwo", "à-yàa-kam", "อาชญากรรม", "Prawo", 2, "n", AW, "", ""),
("A1", "kradzież", "kaan khà-mooei", "การขโมย", "Prawo", 4, "n", AW, "", ""),
("A1", "oszustwo", "kaan koong", "การโกง", "Prawo", 4, "n", AW,
 "koong to najczęstsze słowo na naciąganie — także w kontekście ceny.", ""),
("A2", "sąd", "sǎan", "ศาล", "Prawo", 3, "n", AW,
 "To samo słowo co „kapliczka” w sǎan phrá phuum — kontekst rozstrzyga.", ""),
("A2", "adwokat", "thá-naai khwaam", "ทนายความ", "Prawo", 3, "n", AW, "", ""),
("A2", "zeznanie", "kham hâi kaan", "คำให้การ", "Prawo", 2, "n", AW, "", ""),
("A2", "prawo (system)", "kòt mǎai", "กฎหมาย", "Prawo", 4, "n", AW, "", ""),
("A2", "przepis, zasada", "kòt", "กฎ", "Prawo", 4, "n", AW, "", ""),
("A2", "łamać prawo", "phìt kòt mǎai", "ผิดกฎหมาย", "Prawo", 4, "v", CZ, "", ""),
("A2", "zgodny z prawem", "thùuk kòt mǎai", "ถูกกฎหมาย", "Prawo", 4, "adj", CO, "", ""),
("A2", "aresztować", "jàp kum", "จับกุม", "Prawo", 3, "v", CZ, "", ""),
("A2", "zapłacić grzywnę", "jàai khâa pràp", "จ่ายค่าปรับ", "Prawo", 4, "v", CZ, "", ""),
("A2", "złożyć skargę", "yûen ráwng rian", "ยื่นร้องเรียน", "Prawo", 2, "v", CZ, "", ""),
("A2", "podpisać oświadczenie", "sen bai jâeng", "เซ็นใบแจ้ง", "Prawo", 2, "v", CZ, "", ""),

# =========================================================== ubezpieczenie
("A1", "ubezpieczenie podróżne", "prà-kan kaan doen thaang", "ประกันการเดินทาง", "Ubezpieczenie", 4, "n", AW, "", ""),
("A1", "ubezpieczenie zdrowotne", "prà-kan sùk-khà-phâap", "ประกันสุขภาพ", "Ubezpieczenie", 4, "n", ZD, "", ""),
("A1", "polisa", "kram-má-thǎn", "กรมธรรม์", "Ubezpieczenie", 2, "n", AW, "", ""),
("A2", "zgłoszenie szkody", "jâeng khleem", "แจ้งเคลม", "Ubezpieczenie", 3, "n", AW, "", ""),
("A2", "odszkodowanie", "khâa chót chooei", "ค่าชดเชย", "Ubezpieczenie", 3, "n", AW, "", ""),
("A2", "udział własny", "khâa sǐa hǎai sùan râek", "ค่าเสียหายส่วนแรก", "Ubezpieczenie", 2, "n", AW, "", ""),
("A2", "zakres ochrony", "khwaam khúm khrawng", "ความคุ้มครอง", "Ubezpieczenie", 2, "n", AW, "", ""),
("A2", "wyłączenie odpowiedzialności", "khâw yók wén", "ข้อยกเว้น", "Ubezpieczenie", 2, "n", AW, "", ""),
("A2", "termin ważności polisy", "wan mòt aa-yú kram-má-thǎn", "วันหมดอายุกรมธรรม์", "Ubezpieczenie", 2, "n", AW, "", ""),

# =========================================================== urząd
("A1", "urząd", "sǎm-nák ngaan", "สำนักงาน", "Urząd", 4, "n", PN, "", ""),
("A1", "okienko (w urzędzie)", "châwng bàw-rí-kaan", "ช่องบริการ", "Urząd", 3, "n", PN, "", "okienko obsługa"),
("A1", "wniosek (dokument)", "bai khǎw", "ใบคำขอ", "Urząd", 3, "n", PN, "", ""),
("A2", "opłata urzędowa", "khâa tham-niam râat-chá-kaan", "ค่าธรรมเนียมราชการ", "Urząd", 2, "n", PN, "", ""),
("A2", "termin odbioru", "wan ráp", "วันรับ", "Urząd", 3, "n", PN, "", ""),
("A2", "zaświadczenie o adresie", "bai ráp-rawng thîi yùu", "ใบรับรองที่อยู่", "Urząd", 2, "n", PN, "", ""),
("A2", "tłumaczenie przysięgłe", "kaan plae ráp-rawng", "การแปลรับรอง", "Urząd", 2, "n", PN, "", ""),
("A2", "kopia poświadczona", "sǎm-nao ráp-rawng", "สำเนารับรอง", "Urząd", 2, "n", PN, "", ""),
("A2", "złożyć dokumenty", "yûen èek-kà-sǎan", "ยื่นเอกสาร", "Urząd", 3, "v", CZ, "", ""),
("A2", "odebrać dokument", "ráp èek-kà-sǎan", "รับเอกสาร", "Urząd", 3, "v", CZ, "", ""),

# =========================================================== zwroty kryzysowe
("A1", "Miałem wypadek.", "phǒm prà-sòp ù-bàt-tì-hèet khráp", "ผมประสบอุบัติเหตุครับ", "Zwroty", 5, "w", AW, "", ""),
("A1", "Nikt nie jest ranny.", "mâi mii khrai bàat jèp khráp", "ไม่มีใครบาดเจ็บครับ", "Zwroty", 4, "w", AW, "", ""),
("A1", "Ktoś jest ranny.", "mii khon bàat jèp khráp", "มีคนบาดเจ็บครับ", "Zwroty", 5, "w", AW, "", ""),
("A2", "To nie moja wina.", "mâi châi khwaam phìt khǎwng phǒm khráp", "ไม่ใช่ความผิดของผมครับ", "Zwroty", 4, "w", AW, "", ""),
("A2", "Mam ubezpieczenie podróżne.", "phǒm mii prà-kan doen thaang khráp", "ผมมีประกันเดินทางครับ", "Zwroty", 4, "w", AW, "", ""),
("A2", "Proszę o protokół.", "khǎw bai jâeng khwaam khráp", "ขอใบแจ้งความครับ", "Zwroty", 4, "w", AW, "", ""),
("A2", "Chcę zadzwonić do ambasady.", "phǒm yàak thoo hǎa sà-thǎan thûut khráp", "ผมอยากโทรหาสถานทูตครับ", "Zwroty", 4, "w", AW, "", ""),
("A2", "Nie rozumiem tego dokumentu.", "phǒm mâi khâo jai èek-kà-sǎan níi khráp", "ผมไม่เข้าใจเอกสารนี้ครับ", "Zwroty", 4, "w", AW, "", ""),
("A2", "Potrzebuję tłumacza.", "phǒm tâwng-kaan lâam khráp", "ผมต้องการล่ามครับ", "Zwroty", 4, "w", AW, "", ""),
("A2", "Ile wynosi mandat?", "khâa pràp thâo rài khráp", "ค่าปรับเท่าไหร่ครับ", "Zwroty", 4, "w", PY, "", ""),
("A2", "Czy mogę zapłacić na miejscu?", "jàai thîi nîi dâi mǎi khráp", "จ่ายที่นี่ได้ไหมครับ", "Zwroty", 3, "w", PY, "", ""),
("A2", "Proszę o pokwitowanie.", "khǎw bai sèt khráp", "ขอใบเสร็จครับ", "Zwroty", 5, "w", AW,
 "Przy mandacie kluczowe: pokwitowanie odróżnia karę od łapówki.", ""),
]
