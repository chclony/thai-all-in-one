# -*- coding: utf-8 -*-
"""Sesja O, partia 7 — MIASTO: budynki, sklepy, transport, orientacja.

Trzy przedrostki, które trzymają tę partię razem:

    ráan-   sklep albo lokal (ráan yaa — apteka)
    rót-    pojazd (rót tûu — bus)
    thîi-   miejsce do czegoś (thîi jàwt rót — parking)

Kategoria Miejsca i orientacja miała 98 haseł, Transport 91, Hotel 58 —
przy 245 czasownikach i 230 przymiotnikach. Ta dysproporcja miała skutek
praktyczny: uczący się umiał ocenić rzecz („za drogie, za ostre, za daleko”),
ale nie umiał nazwać miejsca, o którym mówi.

Osobna warstwa: **wskazówki drogi**. Nie „skręć w lewo” — to baza ma — tylko
to, co Taj naprawdę mówi: „za mostem”, „naprzeciwko 7-Eleven”, „drugi zaułek”,
„zawróć”. Bez tego zrozumienie odpowiedzi na pytanie o drogę jest loterią.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

MO = "Miejsca i orientacja"
TR = "Transport"
HO = "Hotel"
ZP = "Zakupy i pieniądze"
AW = "Awarie i pomoc"
RE = "Restauracja"
PN = "Praca i nauka"
ZD = "Zdrowie"
ST = "Small talk"
PY = "Pytania"
CZ = "Czasowniki"
DC = "Dom i codzienność"
GU = "Gramatyka użytkowa"

CITY = [

# =========================================================== budynki
("A1", "wieżowiec", "tùek sǔung", "ตึกสูง", "Budynki", 3, "n", MO, "", "budynek wysoki"),
("A1", "blok mieszkalny", "khaawn-doo", "คอนโด", "Budynki", 4, "n", HO,
 "Skrót od „condominium”. Standardowe słowo na mieszkanie w mieście.", ""),
("A1", "dom szeregowy", "thaao háo", "ทาวน์เฮาส์", "Budynki", 2, "n", HO, "", ""),
("A1", "pensjonat", "kées háo", "เกสต์เฮาส์", "Budynki", 4, "n", HO, "", ""),
("A1", "hostel", "hàwt-sà-teew", "โฮสเทล", "Budynki", 3, "n", HO, "", ""),
("A1", "kościół", "bòot khrít", "โบสถ์คริสต์", "Budynki", 2, "n", MO, "", ""),
("A1", "meczet", "mát-sà-yít", "มัสยิด", "Budynki", 2, "n", MO,
 "Na południu Tajlandii element krajobrazu tak samo zwykły jak wat.", ""),
("A1", "ratusz, urząd miasta", "sǎm-nák ngaan thêet-sà-baan", "สำนักงานเทศบาล", "Budynki", 2, "n", MO, "", ""),
("A1", "posterunek policji", "sà-thǎa-nii tam-rùat", "สถานีตำรวจ", "Budynki", 4, "n", AW, "", ""),
("A1", "straż pożarna", "sà-thǎa-nii dàp phloeng", "สถานีดับเพลิง", "Budynki", 2, "n", AW, "", ""),
("A1", "poczta", "prai-sà-nii", "ไปรษณีย์", "Budynki", 3, "n", MO, "", ""),
("A1", "biblioteka", "hâwng sà-mùt", "ห้องสมุด", "Budynki", 3, "n", PN, "", "pokój książka"),
("A1", "muzeum", "phí-phít-thá-phan", "พิพิธภัณฑ์", "Budynki", 3, "n", MO, "", ""),
("A1", "stadion", "sà-nǎam kii-laa", "สนามกีฬา", "Budynki", 2, "n", ST, "", "boisko sport"),
("A1", "kino", "roong nǎng", "โรงหนัง", "Budynki", 4, "n", ST, "", "hala film"),
("A1", "teatr", "roong lá-khaawn", "โรงละคร", "Budynki", 2, "n", ST, "", ""),
("A1", "fabryka", "roong ngaan", "โรงงาน", "Budynki", 3, "n", PN, "", "hala praca"),
("A2", "przedszkole", "roong rian à-nú-baan", "โรงเรียนอนุบาล", "Budynki", 2, "n", PN, "", ""),
("A2", "uniwersytet", "má-hǎa wít-thá-yaa-lai", "มหาวิทยาลัย", "Budynki", 4, "n", PN, "", ""),
("A2", "centrum handlowe", "hâang sàp-phá-sǐn-kháa", "ห้างสรรพสินค้า", "Budynki", 4, "n", ZP,
 "W mowie skracane do samego hâang.", ""),
("A2", "targ nocny", "tà-làat klaang khuen", "ตลาดกลางคืน", "Budynki", 4, "n", ZP, "", "targ środek nocy"),
("A2", "targ pływający", "tà-làat nám", "ตลาดน้ำ", "Budynki", 3, "n", ZP, "", "targ woda"),

# =========================================================== ráan- : lokale
("A1", "piekarnia", "ráan khà-nǒm pang", "ร้านขนมปัง", "Lokale", 3, "n", ZP, "", "sklep chleb"),
("A1", "sklep z owocami", "ráan phǒn-lá-mái", "ร้านผลไม้", "Lokale", 3, "n", ZP, "", ""),
("A1", "sklep mięsny", "ráan núea", "ร้านเนื้อ", "Lokale", 2, "n", ZP, "", ""),
("A1", "kwiaciarnia", "ráan dàwk mái", "ร้านดอกไม้", "Lokale", 2, "n", ZP, "", "sklep kwiaty"),
("A1", "księgarnia", "ráan nǎng-sǔe", "ร้านหนังสือ", "Lokale", 3, "n", ZP, "", ""),
("A1", "sklep z ubraniami", "ráan sûea phâa", "ร้านเสื้อผ้า", "Lokale", 3, "n", ZP, "", ""),
("A1", "sklep z telefonami", "ráan thoo-rá-sàp", "ร้านโทรศัพท์", "Lokale", 3, "n", ZP, "", ""),
("A1", "warsztat samochodowy", "ùu sâwm rót", "อู่ซ่อมรถ", "Lokale", 3, "n", AW, "", ""),
("A1", "myjnia", "ráan láang rót", "ร้านล้างรถ", "Lokale", 2, "n", AW, "", ""),
("A2", "salon kosmetyczny", "ráan sǒe-rǐm sǔai", "ร้านเสริมสวย", "Lokale", 2, "n", ZP, "", ""),
("A2", "bar", "báa", "บาร์", "Lokale", 3, "n", ST, "", ""),
("A2", "herbaciarnia", "ráan chaa", "ร้านชา", "Lokale", 3, "n", RE, "", ""),
("A2", "jadłodajnia przy drodze", "ráan khâao tôm", "ร้านข้าวต้ม", "Lokale", 3, "n", RE, "", ""),
("A2", "stragan", "phǎeng lawi", "แผงลอย", "Lokale", 4, "n", ZP, "", "stragan unoszący się"),
("A2", "wypożyczalnia motocykli", "ráan châo maw-toe-sai", "ร้านเช่ามอเตอร์ไซค์", "Lokale", 4, "n", TR, "", ""),
("A2", "biuro podróży", "bàw-rí-sàt thua", "บริษัททัวร์", "Lokale", 3, "n", TR, "", "firma wycieczka"),
("A2", "kantor", "ráan lâek ngoen", "ร้านแลกเงิน", "Lokale", 4, "n", ZP, "", ""),
("A2", "salon masażu stóp", "ráan nûat tháo", "ร้านนวดเท้า", "Lokale", 3, "n", ZD, "", ""),

# =========================================================== transport
("A1", "przystanek autobusowy", "pâai rót mee", "ป้ายรถเมล์", "Transport", 4, "n", TR, "", "znak autobus"),
("A1", "peron", "chaan chaa-laa", "ชานชาลา", "Transport", 3, "n", TR, "", ""),
("A1", "tor, szyna", "raang rót fai", "รางรถไฟ", "Transport", 2, "n", TR, "", ""),
("A1", "port, przystań", "thâa ruea", "ท่าเรือ", "Transport", 4, "n", TR, "", "przystań łódź"),
("A1", "prom", "ruea khâam fâak", "เรือข้ามฟาก", "Transport", 3, "n", TR, "", "łódź przez brzeg"),
("A1", "łódź długoogonowa", "ruea hǎang yaao", "เรือหางยาว", "Transport", 4, "n", TR,
 "Ikona tajskiego transportu wodnego — silnik samochodowy na długim wale.", "łódź ogon długi"),
("A1", "motorower", "maw-toe-sai", "มอเตอร์ไซค์", "Transport", 5, "n", TR, "", ""),
("A1", "taksówka motocyklowa", "win maw-toe-sai", "วินมอเตอร์ไซค์", "Transport", 5, "n", TR,
 "Kierowcy w kolorowych kamizelkach na rogach ulic. Najszybszy sposób na korek.", ""),
("A1", "tuk-tuk", "túk túk", "ตุ๊กตุ๊ก", "Transport", 4, "n", TR, "", ""),
("A1", "songthaew (bus w formie pikapa)", "sǎwng thǎew", "สองแถว", "Transport", 4, "n", TR, "", "dwa rzędy"),
("A2", "lotnisko krajowe", "sà-nǎam bin nai prà-thêet", "สนามบินในประเทศ", "Transport", 3, "n", TR, "", ""),
("A2", "terminal", "aa-khaan phûu doi-sǎan", "อาคารผู้โดยสาร", "Transport", 3, "n", TR, "", "budynek pasażer"),
("A2", "bagaż podręczny", "krà-pǎo thǔe khûen khrûeang", "กระเป๋าถือขึ้นเครื่อง", "Transport", 3, "n", TR, "", ""),
("A2", "odbiór bagażu", "ráp krà-pǎo", "รับกระเป๋า", "Transport", 3, "n", TR, "", ""),
("A2", "karta pokładowa", "bàt khûen khrûeang", "บัตรขึ้นเครื่อง", "Transport", 3, "n", TR, "", "karta wsiąść samolot"),
("A2", "bilet powrotny", "tǔa pai klàp", "ตั๋วไปกลับ", "Transport", 4, "n", TR, "", "bilet iść wracać"),
("A2", "bilet w jedną stronę", "tǔa thîao diao", "ตั๋วเที่ยวเดียว", "Transport", 3, "n", TR, "", ""),
("A2", "rozkład jazdy", "taa-raang wee-laa", "ตารางเวลา", "Transport", 4, "n", TR, "", "tabela czas"),
("A2", "opłata za przejazd", "khâa doi-sǎan", "ค่าโดยสาร", "Transport", 4, "n", TR, "", ""),
("A2", "korek uliczny", "rót tìt yaao", "รถติดยาว", "Transport", 4, "n", TR, "", ""),
("A2", "objazd", "thaang bìang", "ทางเบี่ยง", "Transport", 2, "n", TR, "", ""),
("A2", "opłata drogowa", "khâa thaang dùan", "ค่าทางด่วน", "Transport", 2, "n", TR, "", "opłata droga szybka"),
("A2", "stacja benzynowa", "pám nám man", "ปั๊มน้ำมัน", "Transport", 4, "n", TR, "", ""),
("A2", "kask", "mùak kan náwk", "หมวกกันน็อค", "Transport", 4, "n", TR,
 "Obowiązkowy i realnie kontrolowany. Brak kasku to najczęstszy mandat turysty.", "czapka chronić uderzenie"),
("A2", "prawo jazdy", "bai khàp khìi", "ใบขับขี่", "Transport", 4, "n", TR, "", "liść prowadzić jechać"),
("A2", "mandat", "bai sàng pràp", "ใบสั่งปรับ", "Transport", 3, "n", AW, "", "liść nakazać grzywna"),

# =========================================================== drogi i orientacja
("A1", "aleja, główna ulica", "thà-nǒn yài", "ถนนใหญ่", "Droga", 4, "n", MO, "", ""),
("A1", "zaułek, boczna uliczka", "sawi", "ซอย", "Droga", 5, "n", MO,
 "Adresy w Bangkoku to numer soi przy głównej ulicy: „Sukhumvit sawi sìp-èt”.", ""),
("A1", "skrzyżowanie", "sìi yâek", "สี่แยก", "Droga", 4, "n", MO, "", "cztery rozejścia"),
("A1", "rondo", "wong wian", "วงเวียน", "Droga", 3, "n", MO, "", "krąg obrót"),
("A1", "most", "sà-phaan", "สะพาน", "Droga", 4, "n", MO, "", ""),
("A1", "kładka dla pieszych", "sà-phaan lawi", "สะพานลอย", "Droga", 4, "n", MO, "", "most unoszący się"),
("A1", "przejście dla pieszych", "thaang máa laai", "ทางม้าลาย", "Droga", 3, "n", MO, "", "droga zebra"),
("A1", "chodnik", "thaang tháo", "ทางเท้า", "Droga", 3, "n", MO, "", "droga stopa"),
("A1", "tunel", "ù-moong", "อุโมงค์", "Droga", 2, "n", MO, "", ""),
("A1", "sygnalizacja świetlna", "fai daeng", "ไฟแดง", "Droga", 4, "n", MO,
 "Dosłownie „czerwone światło”, ale znaczy całą sygnalizację.", ""),
("A2", "róg ulicy", "hǔa mum", "หัวมุม", "Droga", 4, "n", MO, "", "głowa róg"),
("A2", "naprzeciwko", "trong khâam", "ตรงข้าม", "Droga", 5, "adv", MO, "", "prosto naprzeciw"),
("A2", "obok, przy", "khâang khâang", "ข้างๆ", "Droga", 5, "adv", MO, "", ""),
("A2", "za (czymś)", "lǎng", "หลัง", "Droga", 5, "adv", GU, "", ""),
("A2", "przed (czymś)", "nâa", "หน้า", "Droga", 5, "adv", GU, "", ""),
("A2", "pomiędzy", "rá-wàang", "ระหว่าง", "Droga", 4, "adv", GU, "", ""),
("A2", "na końcu (ulicy)", "sùt sawi", "สุดซอย", "Droga", 4, "adv", MO, "", "koniec zaułek"),
("A2", "na wprost", "trong pai", "ตรงไป", "Droga", 5, "adv", MO, "", ""),
("A2", "zawróć", "klàp rót", "กลับรถ", "Droga", 4, "v", CZ, "", "obrócić pojazd"),
("A2", "wysiąść", "long", "ลง", "Droga", 5, "v", CZ,
 "To samo słowo znaczy „schodzić w dół”. long thîi nîi — wysiadam tutaj.", ""),
("A2", "wsiąść", "khûen", "ขึ้น", "Droga", 5, "v", CZ, "", ""),
("A2", "minąć, przejechać za daleko", "loei", "เลย", "Droga", 5, "v", CZ,
 "loei jest też partykułą wzmacniającą — mâi dii loei znaczy „wcale niedobre”.", ""),
("A2", "skręcić w zaułek", "líao khâo sawi", "เลี้ยวเข้าซอย", "Droga", 3, "v", CZ, "", ""),

# =========================================================== hotel i mieszkanie
("A1", "winda", "líf", "ลิฟต์", "Hotel", 4, "n", HO, "", ""),
("A1", "schody ruchome", "ban-dai lûean", "บันไดเลื่อน", "Hotel", 3, "n", HO, "", "schody przesuwne"),
("A1", "recepcja", "kháo-tôe", "เคาน์เตอร์", "Hotel", 4, "n", HO, "", ""),
("A1", "hol", "lóp-bîi", "ล็อบบี้", "Hotel", 3, "n", HO, "", ""),
("A1", "balkon", "rá-biang", "ระเบียง", "Hotel", 3, "n", HO, "", ""),
("A1", "basen", "sà wâai nám", "สระว่ายน้ำ", "Hotel", 4, "n", HO, "", "sadzawka pływać"),
("A1", "siłownia", "hâwng àwk kam-lang kaai", "ห้องออกกำลังกาย", "Hotel", 2, "n", HO, "", ""),
("A2", "klucz do pokoju", "kun-jae hâwng", "กุญแจห้อง", "Hotel", 4, "n", HO, "", ""),
("A2", "karta do drzwi", "khiit khâat", "คีย์การ์ด", "Hotel", 3, "n", HO, "", ""),
("A2", "śniadanie w cenie", "ruam aa-hǎan cháo", "รวมอาหารเช้า", "Hotel", 4, "n", HO, "", "wliczone śniadanie"),
("A2", "kaucja", "ngoen mát-jam", "เงินมัดจำ", "Hotel", 3, "n", HO, "", ""),
("A2", "czynsz", "khâa châo", "ค่าเช่า", "Hotel", 4, "n", HO, "", "opłata najem"),
("A2", "rachunek za prąd", "khâa fai", "ค่าไฟ", "Hotel", 4, "n", DC, "", ""),
("A2", "rachunek za wodę", "khâa nám", "ค่าน้ำ", "Hotel", 4, "n", DC, "", ""),
("A2", "internet w pokoju", "wai-fai nai hâwng", "ไวไฟในห้อง", "Hotel", 4, "n", HO, "", ""),
("A2", "hałas z ulicy", "sǐang jàak thà-nǒn", "เสียงจากถนน", "Hotel", 3, "n", AW, "", ""),
("A2", "widok na morze", "wiu thá-lee", "วิวทะเล", "Hotel", 3, "n", HO, "", ""),
("A2", "pokój dla niepalących", "hâwng plàwt bù-rìi", "ห้องปลอดบุหรี่", "Hotel", 3, "n", HO, "", "pokój wolny papieros"),

# =========================================================== pytania o drogę
("A1", "Jak tam dojechać?", "pai yang ngai khráp", "ไปยังไงครับ", "Pytania", 5, "w", PY, "", ""),
("A1", "Czy to daleko stąd?", "klai jàak thîi nîi mǎi khráp", "ไกลจากที่นี่ไหมครับ", "Pytania", 5, "w", PY,
 "Uwaga na parę minimalną: klai (daleko) kontra klâi (blisko). Różnica jednego tonu.", ""),
("A1", "Który autobus tam jedzie?", "rót mee sǎai nǎi khráp", "รถเมล์สายไหนครับ", "Pytania", 4, "w", PY, "", ""),
("A1", "Gdzie mam wysiąść?", "long thîi nǎi khráp", "ลงที่ไหนครับ", "Pytania", 5, "w", PY, "", ""),
("A2", "Ile przystanków stąd?", "ìik kìi pâai khráp", "อีกกี่ป้ายครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Czy tu jest parking?", "mii thîi jàwt rót mǎi khráp", "มีที่จอดรถไหมครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Proszę zatrzymać tutaj.", "jàwt trong níi khráp", "จอดตรงนี้ครับ", "Pytania", 5, "w", TR, "", ""),
("A2", "Proszę włączyć taksometr.", "chûai pòet mí-tôe khráp", "ช่วยเปิดมิเตอร์ครับ", "Pytania", 5, "w", TR,
 "Zdanie ratujące portfel. Bez taksometru cena jest negocjowana i zwykle wyższa.", ""),
("A2", "Zgubiłem się.", "phǒm lǒng thaang khráp", "ผมหลงทางครับ", "Pytania", 4, "w", AW, "", "zabłądzić droga"),
("A2", "Czy może mnie pan tam zawieźć?", "phaa phǒm pai dâi mǎi khráp", "พาผมไปได้ไหมครับ", "Pytania", 3, "w", PY, "", ""),
]
