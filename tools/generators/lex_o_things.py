# -*- coding: utf-8 -*-
"""Sesja O, partia 3 — RZECZY: sprzęty, narzędzia, ubrania, pojemniki.

Przedrostki tej partii są równie produktywne co `kaan-`:

    khrûeang-  urządzenie, maszyna (khrûeang sák phâa — pralka)
    thîi-      przyrząd „do czegoś” (thîi pòet khùat — otwieracz)
    mâi-       przedmiot z drewna lub podłużny (mâi khwǎen sûea — wieszak)
    thǔng-     torba, worek, pojemnik miękki (thǔng khà-yà — worek na śmieci)
    khǎwng-    rzecz jakiegoś rodzaju (khǎwng lên — zabawka)

Cała piątka składa się z sylab, które baza ma od poziomu A1. Rzecz nazwana
złożeniem jest dla ucznia darmowa fonetycznie — płaci tylko za znaczenie.

Uwaga o klasyfikatorach: rzeczy policzalne wymagają w tajskim klasyfikatora
(an, khruêang, tua, lêm, bai). Kurs ma osobny moduł `classifiers.json`;
hasła tej partii świadomie podaje się bez klasyfikatora, żeby nie dublować
tamtego materiału i nie uczyć dwóch rzeczy naraz.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

DC = "Dom i codzienność"
ZP = "Zakupy i pieniądze"
AW = "Awarie i pomoc"
HO = "Hotel"
RE = "Restauracja"
JN = "Jedzenie i napoje"
PN = "Praca i nauka"
TR = "Transport"
ZD = "Zdrowie"
CO = "Cechy i opinie"
MO = "Miejsca i orientacja"
ST = "Small talk"
LI = "Liczby i liczenie"

THINGS = [

# =========================================================== khrûeang- sprzęt
("A2", "lodówka", "tûu yen", "ตู้เย็น", "Sprzęt", 4, "n", DC, "", "szafa zimna"),
("A2", "zamrażarka", "tûu châe khǎeng", "ตู้แช่แข็ง", "Sprzęt", 2, "n", DC, "", "szafa moczyć twardy"),
("A2", "kuchenka", "tao", "เตา", "Sprzęt", 4, "n", DC, "", ""),
("A2", "piekarnik", "tao òp", "เตาอบ", "Sprzęt", 3, "n", DC, "", "kuchenka piec"),
("A2", "mikrofalówka", "mai-khroo-wéef", "ไมโครเวฟ", "Sprzęt", 3, "n", DC, "", ""),
("A2", "czajnik elektryczny", "kaa nám fai fáa", "กาน้ำไฟฟ้า", "Sprzęt", 3, "n", DC, "", "dzbanek woda prąd"),
("A2", "toster", "khrûeang pîng khà-nǒm pang", "เครื่องปิ้งขนมปัง", "Sprzęt", 2, "n", DC, "", "urządzenie opiekać chleb"),
("A2", "blender", "khrûeang pàn", "เครื่องปั่น", "Sprzęt", 3, "n", DC, "", "urządzenie miksować"),
("A2", "wentylator", "phát lom", "พัดลม", "Sprzęt", 5, "n", DC,
 "W tajskim domu ważniejszy niż klimatyzacja — działa cały rok.", "wachlować wiatr"),
("A2", "grzejnik wody", "khrûeang tham nám ráwn", "เครื่องทำน้ำร้อน", "Sprzęt", 3, "n", HO, "", "urządzenie robić woda gorąca"),
("B1", "kserokopiarka", "khrûeang thàai èek-kà-sǎan", "เครื่องถ่ายเอกสาร", "Sprzęt", 2, "n", PN, "", "urządzenie kopiować dokument"),
("B1", "bankomat", "tûu ee-thii-em", "ตู้เอทีเอ็ม", "Sprzęt", 4, "n", ZP, "", ""),
("B1", "automat z napojami", "tûu khǎai khrûeang dùem", "ตู้ขายเครื่องดื่ม", "Sprzęt", 2, "n", ZP, "", ""),
("B1", "waga (przyrząd)", "khrûeang châng", "เครื่องชั่ง", "Sprzęt", 3, "n", ZP, "", "urządzenie ważyć"),
("B1", "kalkulator", "khrûeang khít lêek", "เครื่องคิดเลข", "Sprzęt", 3, "n", LI, "", "urządzenie liczyć"),
("B1", "aparat słuchowy", "khrûeang chûai fang", "เครื่องช่วยฟัง", "Sprzęt", 2, "n", ZD, "", "urządzenie pomagać słuchać"),
("B1", "termometr", "prà-làwt", "ปรอท", "Sprzęt", 3, "n", ZD, "", ""),

# =========================================================== thîi- : przyrządy
("A2", "otwieracz do butelek", "thîi pòet khùat", "ที่เปิดขวด", "Narzędzia", 3, "n", RE, "", "przyrząd otwierać butelka"),
("A2", "otwieracz do puszek", "thîi pòet krà-pǎwng", "ที่เปิดกระป๋อง", "Narzędzia", 2, "n", RE, "", ""),
("A2", "podkładka pod talerz", "thîi rawng jaan", "ที่รองจาน", "Narzędzia", 2, "n", RE, "", "przyrząd podkładać talerz"),
("A2", "popielniczka", "thîi khìa bù-rìi", "ที่เขี่ยบุหรี่", "Narzędzia", 2, "n", RE, "", ""),
("A2", "podstawka na telefon", "thîi wang thoo-rá-sàp", "ที่วางโทรศัพท์", "Narzędzia", 2, "n", DC, "", ""),
("B1", "wieszak na ubrania", "mái khwǎen sûea", "ไม้แขวนเสื้อ", "Narzędzia", 3, "n", HO, "", "drewno wieszać ubranie"),
("B1", "miotła", "mái kwàat", "ไม้กวาด", "Narzędzia", 3, "n", DC, "", "drewno zamiatać"),
("B1", "mop", "mái thǔu phúen", "ไม้ถูพื้น", "Narzędzia", 3, "n", DC, "", "drewno trzeć podłoga"),
("B1", "linijka", "mái ban-thát", "ไม้บรรทัด", "Narzędzia", 2, "n", PN, "", ""),
("B1", "wykałaczka", "mái jîm fan", "ไม้จิ้มฟัน", "Narzędzia", 3, "n", RE, "", "drewno dziabać ząb"),
("B1", "zapałka", "mái khìit", "ไม้ขีด", "Narzędzia", 3, "n", DC, "", "drewno drapać"),
("B1", "patyk do szaszłyków", "mái sîap", "ไม้เสียบ", "Narzędzia", 2, "n", JN, "", ""),

# =========================================================== narzędzia
("A2", "młotek", "kháwn", "ค้อน", "Narzędzia", 3, "n", AW, "", ""),
("A2", "śrubokręt", "khǎi khuang", "ไขควง", "Narzędzia", 3, "n", AW, "", ""),
("A2", "śruba", "sà-krú", "สกรู", "Narzędzia", 2, "n", AW, "", ""),
("A2", "gwóźdź", "tà-puu", "ตะปู", "Narzędzia", 2, "n", AW, "", ""),
("A2", "klucz płaski", "prà-jae", "ประแจ", "Narzędzia", 2, "n", AW, "", ""),
("A2", "szczypce", "khiim", "คีม", "Narzędzia", 2, "n", AW, "", ""),
("A2", "piła", "lûeai", "เลื่อย", "Narzędzia", 2, "n", AW, "", ""),
("A2", "drabina", "ban-dai", "บันได", "Narzędzia", 3, "n", DC,
 "To samo słowo znaczy „schody” — kontekst rozstrzyga.", ""),
("A2", "taśma klejąca", "théep kaao", "เทปกาว", "Narzędzia", 3, "n", DC, "", "taśma klej"),
("A2", "klej", "kaao", "กาว", "Narzędzia", 3, "n", DC, "", ""),
("A2", "sznurek", "chûeak", "เชือก", "Narzędzia", 3, "n", DC, "", ""),
("A2", "drut", "lûat", "ลวด", "Narzędzia", 2, "n", AW, "", ""),
("A2", "łańcuch", "sôo", "โซ่", "Narzędzia", 2, "n", AW, "", ""),
("B1", "wiertarka", "sà-wàan", "สว่าน", "Narzędzia", 2, "n", AW, "", ""),
("B1", "latarka", "fai chǎai", "ไฟฉาย", "Narzędzia", 4, "n", AW, "", "światło świecić"),
("B1", "bateria", "thàan fai chǎai", "ถ่านไฟฉาย", "Narzędzia", 3, "n", AW, "", "węgiel latarka"),
("B1", "przedłużacz", "plák phûang", "ปลั๊กพ่วง", "Narzędzia", 3, "n", AW, "", ""),
("B1", "gniazdko", "plák fai", "ปลั๊กไฟ", "Narzędzia", 4, "n", HO, "", ""),
("B1", "przejściówka", "hǔa plaeng", "หัวแปลง", "Narzędzia", 3, "n", HO, "", "głowa przekształcać"),
("B1", "żarówka", "làwt fai", "หลอดไฟ", "Narzędzia", 3, "n", DC, "", "rurka światło"),

# =========================================================== pojemniki
("A2", "worek na śmieci", "thǔng khà-yà", "ถุงขยะ", "Pojemniki", 4, "n", DC, "", "torba śmieci"),
("A2", "torba papierowa", "thǔng krà-dàat", "ถุงกระดาษ", "Pojemniki", 3, "n", ZP, "", ""),
("A2", "reklamówka", "thǔng phlaat-sà-tìk", "ถุงพลาสติก", "Pojemniki", 4, "n", ZP, "", ""),
("A2", "torba na zakupy", "thǔng phâa", "ถุงผ้า", "Pojemniki", 3, "n", ZP, "", "torba materiał"),
("A2", "pudełko na jedzenie", "klàwng aa-hǎan", "กล่องอาหาร", "Pojemniki", 3, "n", RE, "", ""),
("A2", "słoik", "khùat kâew", "ขวดแก้ว", "Pojemniki", 2, "n", DC, "", "butelka szkło"),
("A2", "puszka", "krà-pǎwng", "กระป๋อง", "Pojemniki", 3, "n", JN, "", ""),
("A2", "wiadro", "thǎng", "ถัง", "Pojemniki", 3, "n", DC, "", ""),
("A2", "kosz na śmieci", "thǎng khà-yà", "ถังขยะ", "Pojemniki", 4, "n", DC, "", ""),
("A2", "koszyk", "tà-krâa", "ตะกร้า", "Pojemniki", 3, "n", ZP, "", ""),
("A2", "taca", "thàat", "ถาด", "Pojemniki", 3, "n", RE, "", ""),
("A2", "plecak", "pêe", "เป้", "Pojemniki", 4, "n", TR, "", ""),
("A2", "walizka", "krà-pǎo doen thaang", "กระเป๋าเดินทาง", "Pojemniki", 4, "n", TR, "", "torba podróż"),
("A2", "portfel", "krà-pǎo tang", "กระเป๋าตังค์", "Pojemniki", 4, "n", ZP, "", "torba pieniądze"),
("B1", "sejf", "tûu sêef", "ตู้เซฟ", "Pojemniki", 3, "n", HO, "", ""),
("B1", "szuflada", "lín chák", "ลิ้นชัก", "Pojemniki", 2, "n", DC, "", ""),
("B1", "półka", "chán waang khǎwng", "ชั้นวางของ", "Pojemniki", 3, "n", DC, "", "poziom kłaść rzeczy"),

# =========================================================== ubrania
("A2", "koszula", "sûea chóoet", "เสื้อเชิ้ต", "Ubrania", 4, "n", ZP, "", ""),
("A2", "bluzka", "sûea phûu yǐng", "เสื้อผู้หญิง", "Ubrania", 2, "n", ZP, "", ""),
("A2", "sweter", "sûea kan nǎao", "เสื้อกันหนาว", "Ubrania", 3, "n", ZP, "", "ubranie chronić zimno"),
("A2", "kurtka przeciwdeszczowa", "sûea kan fǒn", "เสื้อกันฝน", "Ubrania", 3, "n", ZP, "", "ubranie chronić deszcz"),
("A2", "spódnica", "krà-prong", "กระโปรง", "Ubrania", 3, "n", ZP, "", ""),
("A2", "sukienka", "chút drèt", "ชุดเดรส", "Ubrania", 3, "n", ZP, "", ""),
("A2", "garnitur", "chút sùut", "ชุดสูท", "Ubrania", 2, "n", ZP, "", ""),
("A2", "strój kąpielowy", "chút wâai nám", "ชุดว่ายน้ำ", "Ubrania", 3, "n", ZP, "", "strój pływać"),
("A2", "piżama", "chút nawn", "ชุดนอน", "Ubrania", 3, "n", ZP, "", "strój spać"),
("A2", "bielizna", "chút chán nai", "ชุดชั้นใน", "Ubrania", 3, "n", ZP, "", "strój warstwa wewnętrzna"),
("A2", "skarpetki", "thǔng tháo", "ถุงเท้า", "Ubrania", 4, "n", ZP, "", "torba stopa"),
("A2", "rękawiczki", "thǔng mue", "ถุงมือ", "Ubrania", 3, "n", ZP, "", "torba ręka"),
("A2", "klapki", "rawng tháo tàe", "รองเท้าแตะ", "Ubrania", 5, "n", ZP,
 "Obuwie numer jeden w Tajlandii. Przed wejściem do domu i świątyni zdejmuje się je zawsze.", "obuwie dotykać"),
("A2", "buty sportowe", "rawng tháo phâa bai", "รองเท้าผ้าใบ", "Ubrania", 4, "n", ZP, "", "obuwie płótno"),
("A2", "pasek", "khěm khàt", "เข็มขัด", "Ubrania", 3, "n", ZP, "", ""),
("A2", "czapka", "mùak", "หมวก", "Ubrania", 4, "n", ZP, "", ""),
("A2", "okulary przeciwsłoneczne", "wâen kan dàet", "แว่นกันแดด", "Ubrania", 4, "n", ZP, "", "okulary chronić słońce"),
("A2", "szalik", "phâa phan khaw", "ผ้าพันคอ", "Ubrania", 2, "n", ZP, "", "materiał owijać szyja"),
("A2", "krawat", "nék thai", "เนคไท", "Ubrania", 2, "n", ZP, "", ""),
("B1", "biżuteria", "khrûeang prà-dàp kaai", "เครื่องประดับกาย", "Ubrania", 2, "n", ZP, "", ""),
("B1", "pierścionek", "wǎen", "แหวน", "Ubrania", 3, "n", ZP, "", ""),
("B1", "naszyjnik", "sâwi khaw", "สร้อยคอ", "Ubrania", 2, "n", ZP, "", "łańcuszek szyja"),
("B1", "kolczyk", "tûm hǔu", "ตุ้มหู", "Ubrania", 2, "n", ZP, "", ""),
("B1", "zegarek", "naa-lí-kaa khâw mue", "นาฬิกาข้อมือ", "Ubrania", 3, "n", ZP, "", "zegar nadgarstek"),
("B1", "rozmiar (ubrania)", "sái", "ไซส์", "Ubrania", 4, "n", ZP, "", ""),
("B1", "materiał, tkanina", "núea phâa", "เนื้อผ้า", "Ubrania", 2, "n", ZP, "", "mięso materiał"),
("B1", "bawełna", "fâai", "ฝ้าย", "Ubrania", 2, "n", ZP, "", ""),
("B1", "jedwab", "phâa mǎi", "ผ้าไหม", "Ubrania", 3, "n", ZP,
 "Jedwab tajski to towar eksportowy i najczęstsza pamiątka z północy.", ""),
("B1", "skóra (materiał)", "nǎng", "หนัง", "Ubrania", 3, "n", ZP,
 "To samo słowo znaczy „film” — nǎng sanùk to dobry film, nie zabawna skóra.", ""),

# =========================================================== łazienka i higiena
("A2", "ręcznik", "phâa chét tua", "ผ้าเช็ดตัว", "Higiena", 4, "n", HO, "", "materiał wycierać ciało"),
("A2", "mydło", "sà-bùu", "สบู่", "Higiena", 4, "n", HO, "", ""),
("A2", "pasta do zębów", "yaa sǐi fan", "ยาสีฟัน", "Higiena", 4, "n", HO, "", "lek barwić zęby"),
("A2", "szczoteczka do zębów", "praeng sǐi fan", "แปรงสีฟัน", "Higiena", 4, "n", HO, "", ""),
("A2", "grzebień", "wǐi", "หวี", "Higiena", 3, "n", HO, "", ""),
("A2", "papier toaletowy", "krà-dàat cham-rá", "กระดาษชำระ", "Higiena", 4, "n", HO, "", "papier oczyszczać"),
("A2", "chusteczki", "krà-dàat thít-chûu", "กระดาษทิชชู่", "Higiena", 4, "n", RE, "", ""),
("A2", "dezodorant", "yaa ráp klìn", "ยาระงับกลิ่น", "Higiena", 2, "n", ZP, "", "lek tłumić zapach"),
("A2", "krem z filtrem", "khriim kan dàet", "ครีมกันแดด", "Higiena", 4, "n", ZP, "", "krem chronić słońce"),
("A2", "środek na komary", "yaa kan yung", "ยากันยุง", "Higiena", 5, "n", ZD,
 "W porze deszczowej rzecz pierwszej potrzeby, nie luksus.", "lek chronić komar"),
("A2", "maszynka do golenia", "mîit koon", "มีดโกน", "Higiena", 2, "n", HO, "", "nóż golić"),
("A2", "lusterko", "krà-jòk ngao", "กระจกเงา", "Higiena", 3, "n", HO, "", "szkło cień"),
("B1", "suszarka do włosów", "khrûeang pào phǒm", "เครื่องเป่าผม", "Higiena", 3, "n", HO, "", "urządzenie dmuchać włosy"),
("B1", "waciki", "sǎm-lii", "สำลี", "Higiena", 2, "n", ZD, "", ""),
("B1", "plaster", "phlaas-tôe", "พลาสเตอร์", "Higiena", 3, "n", ZD, "", ""),

# =========================================================== biuro i papiery
("A2", "długopis", "pàak-kaa", "ปากกา", "Biuro", 4, "n", PN, "", ""),
("A2", "ołówek", "din-sǎw", "ดินสอ", "Biuro", 3, "n", PN, "", ""),
("A2", "gumka do ścierania", "yaang lóp", "ยางลบ", "Biuro", 2, "n", PN, "", "guma wymazywać"),
("A2", "zeszyt", "sà-mùt", "สมุด", "Biuro", 4, "n", PN, "", ""),
("A2", "koperta", "sawng", "ซอง", "Biuro", 3, "n", PN, "", ""),
("A2", "znaczek pocztowy", "sà-taem", "แสตมป์", "Biuro", 2, "n", MO, "", ""),
("A2", "teczka", "faem", "แฟ้ม", "Biuro", 2, "n", PN, "", ""),
("A2", "nożyczki", "kan-krai", "กรรไกร", "Biuro", 3, "n", PN, "", ""),
("B1", "pieczątka", "traa prà-tháp", "ตราประทับ", "Biuro", 2, "n", PN, "", ""),
("B1", "podpis", "laai sen", "ลายเซ็น", "Biuro", 3, "n", PN, "", "wzór podpisać"),
("B1", "formularz", "bàep fawm", "แบบฟอร์ม", "Biuro", 3, "n", PN, "", ""),
("B1", "paragon", "bai sèt", "ใบเสร็จ", "Biuro", 4, "n", ZP, "", "liść skończony"),
("B1", "faktura", "bai kam-kàp phaa-sǐi", "ใบกำกับภาษี", "Biuro", 2, "n", ZP, "", ""),
("B1", "umowa", "sǎn-yaa", "สัญญา", "Biuro", 3, "n", PN,
 "To samo słowo znaczy „obietnica” — umowa to obietnica na piśmie.", ""),
("B1", "zaświadczenie", "bai ráp-rawng", "ใบรับรอง", "Biuro", 2, "n", PN, "", "liść poświadczać"),
("B1", "wizytówka", "naam bàt", "นามบัตร", "Biuro", 3, "n", PN, "", "imię karta"),
("B1", "kopia", "sǎm-nao", "สำเนา", "Biuro", 3, "n", PN, "", ""),

# =========================================================== jakość rzeczy
("A2", "nowiutki", "mài ìiam", "ใหม่เอี่ยม", "Jakość", 3, "adj", CO, "", ""),
("A2", "używany", "mue sǎwng", "มือสอง", "Jakość", 4, "adj", ZP, "", "ręka druga"),
("A2", "zepsuty", "chamrút", "ชำรุด", "Jakość", 2, "adj", AW, "", ""),
("A2", "pęknięty", "ráao", "ร้าว", "Jakość", 2, "adj", AW, "", ""),
("A2", "podarty", "khàat", "ขาด", "Jakość", 3, "adj", AW,
 "To samo słowo znaczy „brakuje” — khàat nám to brak wody.", ""),
("A2", "wygięty", "ngaw", "งอ", "Jakość", 2, "adj", AW, "", ""),
("A2", "zardzewiały", "pen sà-nǐm", "เป็นสนิม", "Jakość", 2, "adj", AW, "", ""),
("A2", "sztuczny", "thiam", "เทียม", "Jakość", 2, "adj", CO, "", ""),
("A2", "prawdziwy, oryginalny", "thǽe", "แท้", "Jakość", 4, "adj", ZP,
 "Na targu usłyszysz to co pięć minut: khǎwng thǽe — towar oryginalny.", ""),
("A2", "podrobiony", "khǎwng plawm", "ของปลอม", "Jakość", 3, "n", ZP, "", "rzecz fałszywa"),
("B1", "ręcznie robiony", "tham mue", "ทำมือ", "Jakość", 3, "adj", ZP, "", "robić ręka"),
("B1", "jednorazowy", "chái khráng diao", "ใช้ครั้งเดียว", "Jakość", 3, "adj", DC, "", "używać raz jeden"),
("B1", "wielorazowy", "chái sám dâi", "ใช้ซ้ำได้", "Jakość", 2, "adj", DC, "", "używać powtórnie móc"),
("B1", "wodoodporny", "kan nám", "กันน้ำ", "Jakość", 3, "adj", ZP, "", "chronić woda"),
("B1", "przenośny", "phók phaa dâi", "พกพาได้", "Jakość", 2, "adj", ZP, "", ""),
]
