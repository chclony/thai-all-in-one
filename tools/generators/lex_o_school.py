# -*- coding: utf-8 -*-
"""Sesja O, partia 11 — NAUKA, BIURO, TECHNIKA, PIENIĄDZE.

Warstwa, w której toczy się rozmowa o sprawach, a nie o rzeczach. Sesja N
otworzyła ją od strony państwa i mediów; tu domykamy stronę codziennej
administracji własnego życia: bank, telefon, internet, szkoła, biuro.

Dlaczego to potrzebne mimo że brzmi urzędowo: cudzoziemiec mieszkający
w Tajlandii spędza nieproporcjonalnie dużo czasu przy okienkach. Konto,
karta SIM, wiza, przelew, hasło, umowa najmu — to nie jest słownictwo
zaawansowane, to słownictwo pierwszego tygodnia.

Druga warstwa: **technika**. Baterie, ładowarki, zasięg, aplikacje, kody QR.
Tajlandia płaci telefonem częściej niż gotówką; bez tych słów uczący się
stoi przy kasie i nie rozumie, o co go proszą.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

PN = "Praca i nauka"
ZP = "Zakupy i pieniądze"
AW = "Awarie i pomoc"
LI = "Liczby i liczenie"
DC = "Dom i codzienność"
MO = "Miejsca i orientacja"
CO = "Cechy i opinie"
PY = "Pytania"
CZ = "Czasowniki"
HO = "Hotel"
ST = "Small talk"

SCHOOL = [

# =========================================================== szkoła
("A1", "lekcja", "bòt rian", "บทเรียน", "Szkoła", 4, "n", PN, "", "rozdział nauka"),
("A1", "zadanie domowe", "kaan bâan", "การบ้าน", "Szkoła", 4, "n", PN, "", "praca dom"),
("A1", "ćwiczenie", "bàep fùek hàt", "แบบฝึกหัด", "Szkoła", 3, "n", PN, "", ""),
("A1", "przykład", "tua yàang", "ตัวอย่าง", "Szkoła", 5, "n", PN, "", "ciało rodzaj"),
("A1", "błąd (w zadaniu)", "khâw phìt", "ข้อผิด", "Szkoła", 4, "n", PN, "", ""),
("A1", "odpowiedź (rozwiązanie)", "kham tàwp", "คำตอบ", "Szkoła", 5, "n", PN, "", "słowo odpowiedzieć"),
("A1", "pytanie (w teście)", "kham thǎam", "คำถาม", "Szkoła", 5, "n", PY, "", "słowo pytać"),
("A1", "ocena, wynik", "khá-naen", "คะแนน", "Szkoła", 4, "n", PN, "", ""),
("A1", "świadectwo", "bai ráp-rawng phǒn", "ใบรับรองผล", "Szkoła", 2, "n", PN, "", ""),
("A1", "przedmiot (w szkole)", "wí-chaa", "วิชา", "Szkoła", 3, "n", PN, "", ""),
("A2", "słownik", "phót-jà-naa-nú-krom", "พจนานุกรม", "Szkoła", 3, "n", PN, "", ""),
("A2", "podręcznik", "nǎng-sǔe rian", "หนังสือเรียน", "Szkoła", 3, "n", PN, "", ""),
("A2", "notatka", "bantúek", "บันทึก", "Szkoła", 3, "n", PN, "", ""),
("A2", "wykład", "kaan ban-yaai sòt", "การบรรยายสด", "Szkoła", 2, "n", PN, "", ""),
("A2", "kurs", "khàwt", "คอร์ส", "Szkoła", 3, "n", PN, "", ""),
("A2", "stypendium", "thun kaan sùek-sǎa", "ทุนการศึกษา", "Szkoła", 2, "n", PN, "", ""),
("A2", "dyplom", "prá-rin-yaa bàt", "ปริญญาบัตร", "Szkoła", 2, "n", PN, "", ""),
("A2", "semestr", "phâak rian", "ภาคเรียน", "Szkoła", 2, "n", PN, "", ""),
("A2", "przerwa (w szkole)", "phák klaang wan", "พักกลางวัน", "Szkoła", 3, "n", PN, "", "przerwa środek dnia"),
("A2", "mundurek szkolny", "chút nák rian", "ชุดนักเรียน", "Szkoła", 3, "n", PN,
 "W Tajlandii obowiązkowy na wszystkich szczeblach, także na studiach.", ""),

# =========================================================== biuro
("A1", "biuro", "áwp-fít", "ออฟฟิศ", "Biuro", 4, "n", PN, "", ""),
("A1", "biurko", "tó tham ngaan", "โต๊ะทำงาน", "Biuro", 3, "n", PN, "", ""),
("A1", "sala konferencyjna", "hâwng prà-chum", "ห้องประชุม", "Biuro", 3, "n", PN, "", ""),
("A1", "termin (deadline)", "kam-nòt sòng", "กำหนดส่ง", "Biuro", 3, "n", PN, "", "ustalony termin oddania"),
("A1", "projekt", "khroong kaan", "โครงการ", "Biuro", 3, "n", PN, "", ""),
("A1", "raport", "raai ngaan", "รายงาน", "Biuro", 4, "n", PN, "", ""),
("A1", "lista", "raai kaan", "รายการ", "Biuro", 4, "n", PN, "", ""),
("A1", "harmonogram", "taa-raang ngaan", "ตารางงาน", "Biuro", 3, "n", PN, "", ""),
("A2", "nadgodziny", "oo-thii", "โอที", "Biuro", 3, "n", PN, "", ""),
("A2", "wypłata", "ngoen duean", "เงินเดือน", "Biuro", 4, "n", PN, "", "pieniądze miesiąc"),
("A2", "premia", "boo-nát", "โบนัส", "Biuro", 3, "n", PN, "", ""),
("A2", "urlop", "wan yùt phák-phàwn", "วันหยุดพักผ่อน", "Biuro", 3, "n", PN, "", ""),
("A2", "zwolnienie lekarskie", "laa pùai", "ลาป่วย", "Biuro", 3, "n", PN, "", "urlop chory"),
("A2", "umowa o pracę", "sǎn-yaa jâang ngaan", "สัญญาจ้างงาน", "Biuro", 2, "n", PN, "", ""),
("A2", "okres próbny", "chûang thót-làwng ngaan", "ช่วงทดลองงาน", "Biuro", 2, "n", PN, "", ""),
("A2", "CV, życiorys", "rêe-sù-mêe", "เรซูเม่", "Biuro", 2, "n", PN, "", ""),
("A2", "kolejka (do okienka)", "khiu", "คิว", "Biuro", 5, "n", MO,
 "ao khiu — wziąć numerek. W tajskich urzędach i bankach rzecz podstawowa.", ""),
("A2", "numerek w kolejce", "bàt khiu", "บัตรคิว", "Biuro", 3, "n", MO, "", ""),

# =========================================================== bank i pieniądze
("A1", "konto bankowe", "ban-chii thá-naa-khaan", "บัญชีธนาคาร", "Bank", 4, "n", ZP, "", ""),
("A1", "karta bankomatowa", "bàt ee-thii-em", "บัตรเอทีเอ็ม", "Bank", 4, "n", ZP, "", ""),
("A1", "karta kredytowa", "bàt khree-dìt", "บัตรเครดิต", "Bank", 4, "n", ZP, "", ""),
("A1", "przelew", "oon ngoen", "โอนเงิน", "Bank", 5, "n", ZP,
 "W Tajlandii płaci się przelewem częściej niż kartą — także w budce z jedzeniem.", "przelać pieniądze"),
("A1", "wpłata", "fàak ngoen", "ฝากเงิน", "Bank", 4, "n", ZP, "", "powierzyć pieniądze"),
("A1", "wypłata z bankomatu", "thǎwn ngoen", "ถอนเงิน", "Bank", 4, "n", ZP, "", "wyjąć pieniądze"),
("A1", "saldo", "yâwt khong lǔea", "ยอดคงเหลือ", "Bank", 3, "n", ZP, "", "kwota pozostała"),
("A1", "prowizja, opłata", "khâa tham-niam", "ค่าธรรมเนียม", "Bank", 4, "n", ZP, "", ""),
("A1", "kurs wymiany", "àt-traa lâek plìan", "อัตราแลกเปลี่ยน", "Bank", 4, "n", ZP, "", ""),
("A2", "kredyt, pożyczka", "sǐn chûea", "สินเชื่อ", "Bank", 3, "n", ZP, "", ""),
("A2", "odsetki", "dàwk bîa", "ดอกเบี้ย", "Bank", 3, "n", ZP, "", ""),
("A2", "rata", "ngôn phàwn", "งวดผ่อน", "Bank", 3, "n", ZP, "", ""),
("A2", "podatek", "phaa-sǐi", "ภาษี", "Bank", 4, "n", ZP, "", ""),
("A2", "rachunek do zapłaty", "bin", "บิล", "Bank", 5, "n", ZP, "", ""),
("A2", "gotówka", "ngoen sòt", "เงินสด", "Bank", 5, "n", ZP, "", "pieniądze świeże"),
("A2", "drobne, reszta", "ngoen thawn", "เงินทอน", "Bank", 5, "n", ZP, "", ""),
("A2", "banknot", "thá-ná-bàt", "ธนบัตร", "Bank", 3, "n", ZP, "", ""),
("A2", "moneta", "rǐan", "เหรียญ", "Bank", 4, "n", ZP, "", ""),
("A2", "budżet", "ngóp prà-maan", "งบประมาณ", "Bank", 2, "n", ZP, "", ""),
("A2", "oszczędności", "ngoen àwm", "เงินออม", "Bank", 3, "n", ZP, "", ""),
("A2", "dług", "nîi", "หนี้", "Bank", 3, "n", ZP, "", ""),
("A2", "faktura elektroniczna", "bai sèt àwn-lai", "ใบเสร็จออนไลน์", "Bank", 2, "n", ZP, "", ""),

# =========================================================== technika
("A1", "ładowarka", "thîi chàat", "ที่ชาร์จ", "Technika", 5, "n", AW, "", "przyrząd ładować"),
("A1", "kabel", "sǎai", "สาย", "Technika", 4, "n", AW,
 "To samo słowo znaczy „linia autobusowa” i „późno” w innym tonie.", ""),
("A1", "powerbank", "phaao-woe báeng", "พาวเวอร์แบงค์", "Technika", 3, "n", AW, "", ""),
("A1", "słuchawki", "hǔu fang", "หูฟัง", "Technika", 4, "n", ZP, "", "ucho słuchać"),
("A1", "głośnik", "lam-phoong", "ลำโพง", "Technika", 3, "n", ZP, "", ""),
("A1", "ekran", "nâa jaw", "หน้าจอ", "Technika", 4, "n", AW, "", "twarz ekran"),
("A1", "klawiatura", "khiibàwt", "คีย์บอร์ด", "Technika", 3, "n", PN, "", ""),
("A1", "komputer", "khawm-phíu-tôe", "คอมพิวเตอร์", "Technika", 4, "n", PN, "", ""),
("A1", "laptop", "nóot búk", "โน้ตบุ๊ก", "Technika", 4, "n", PN, "", ""),
("A2", "karta SIM", "sim", "ซิม", "Technika", 5, "n", AW,
 "Pierwsza rzecz do kupienia na lotnisku. Karty prepaid sprzedają w każdym 7-Eleven.", ""),
("A2", "numer telefonu", "boe thoo", "เบอร์โทร", "Technika", 5, "n", AW, "", ""),
("A2", "doładowanie", "toem ngoen", "เติมเงิน", "Technika", 5, "n", AW, "", "napełnić pieniądze"),
("A2", "pakiet internetu", "phék nét", "แพ็คเน็ต", "Technika", 4, "n", AW, "", ""),
("A2", "zasięg", "sǎn-yaan", "สัญญาณ", "Technika", 4, "n", AW,
 "mâi mii sǎn-yaan — brak zasięgu. Częste na wyspach i w górach.", ""),
("A2", "hasło", "rá-hàt phàan", "รหัสผ่าน", "Technika", 5, "n", AW, "", "kod przejść"),
("A2", "kod QR", "khiu-aa khôot", "คิวอาร์โค้ด", "Technika", 5, "n", ZP,
 "Skanuje się go przy każdej płatności — także u sprzedawcy ulicznego.", ""),
("A2", "aplikacja", "áep", "แอป", "Technika", 5, "n", AW, "", ""),
("A2", "konto (w aplikacji)", "ban-chii phûu chái", "บัญชีผู้ใช้", "Technika", 3, "n", AW, "", ""),
("A2", "zdjęcie", "rûup thàai", "รูปถ่าย", "Technika", 4, "n", ST, "", ""),
("A2", "wideo", "wii-dii-oo", "วิดีโอ", "Technika", 4, "n", ST, "", ""),
("A2", "plik", "fai", "ไฟล์", "Technika", 3, "n", PN, "", ""),
("A2", "link", "lingk", "ลิงก์", "Technika", 3, "n", PN, "", ""),
("A2", "wiadomość (SMS, czat)", "khâw khwaam", "ข้อความ", "Technika", 5, "n", AW, "", ""),
("A2", "powiadomienie", "kaan jâeng tuean", "การแจ้งเตือน", "Technika", 3, "n", AW, "", ""),
("A2", "aktualizacja", "kaan àp-dèet", "การอัปเดต", "Technika", 3, "n", AW, "", ""),
("A2", "kopia zapasowa", "kaan sǎm-rawng khâw muun", "การสำรองข้อมูล", "Technika", 2, "n", AW, "", ""),
("A2", "dane, informacje", "khâw muun", "ข้อมูล", "Technika", 4, "n", PN, "", ""),

# =========================================================== czasowniki tej warstwy
("A1", "ładować (telefon)", "chàat", "ชาร์จ", "Czynności", 5, "v", CZ, "", ""),
("A1", "skanować", "sà-kaen", "สแกน", "Czynności", 4, "v", CZ, "", ""),
("A1", "logować się", "khâo rá-bòp", "เข้าระบบ", "Czynności", 3, "v", CZ, "", "wejść system"),
("A1", "wylogować się", "àwk jàak rá-bòp", "ออกจากระบบ", "Czynności", 2, "v", CZ, "", ""),
("A1", "pobierać (plik)", "dao-lôot", "ดาวน์โหลด", "Czynności", 3, "v", CZ, "", ""),
("A1", "wysyłać (plik)", "àp-lôot", "อัปโหลด", "Czynności", 2, "v", CZ, "", ""),
("A1", "usuwać", "lóp", "ลบ", "Czynności", 4, "v", CZ, "", ""),
("A1", "zapisywać", "sêef", "เซฟ", "Czynności", 4, "v", CZ, "", ""),
("A2", "instalować", "tìt tâng", "ติดตั้ง", "Czynności", 3, "v", CZ, "", ""),
("A2", "restartować", "rîi-sà-tàat", "รีสตาร์ท", "Czynności", 3, "v", CZ, "", ""),
("A2", "podłączyć się do wi-fi", "tàw wai-fai", "ต่อไวไฟ", "Czynności", 4, "v", CZ, "", ""),
("A2", "przelać pieniądze", "oon", "โอน", "Czynności", 5, "v", CZ, "", ""),
("A2", "podzielić rachunek", "yâek bin", "แยกบิล", "Czynności", 3, "v", CZ, "", ""),
("A2", "zaokrąglić", "pàt sèet", "ปัดเศษ", "Czynności", 2, "v", CZ, "", ""),
("A2", "porównać ceny", "prìap thîap raa-khaa", "เปรียบเทียบราคา", "Czynności", 3, "v", CZ, "", ""),
("A2", "obliczyć", "khít lêek", "คิดเลข", "Czynności", 4, "v", CZ, "", ""),
("A2", "sprawdzić stan konta", "chék yâwt", "เช็คยอด", "Czynności", 3, "v", CZ, "", ""),
("A2", "przedłużyć umowę", "tàw sǎn-yaa", "ต่อสัญญา", "Czynności", 3, "v", CZ, "", ""),
("A2", "rozwiązać umowę", "yók lôek sǎn-yaa", "ยกเลิกสัญญา", "Czynności", 2, "v", CZ, "", ""),

# =========================================================== pytania praktyczne
("A1", "Jakie jest hasło do wi-fi?", "rá-hàt wai-fai à-rai khráp", "รหัสไวไฟอะไรครับ", "Pytania", 5, "w", PY, "", ""),
("A1", "Czy mogę tu naładować telefon?", "chàat thoo-rá-sàp thîi nîi dâi mǎi khráp", "ชาร์จโทรศัพท์ที่นี่ได้ไหมครับ", "Pytania", 4, "w", PY, "", ""),
("A1", "Czy przyjmujecie karty?", "ráp bàt mǎi khráp", "รับบัตรไหมครับ", "Pytania", 5, "w", PY, "", ""),
("A2", "Czy mogę zapłacić przelewem?", "oon ngoen dâi mǎi khráp", "โอนเงินได้ไหมครับ", "Pytania", 5, "w", PY, "", ""),
("A2", "Ile wynosi prowizja?", "khâa tham-niam thâo rài khráp", "ค่าธรรมเนียมเท่าไหร่ครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Gdzie mogę kupić kartę SIM?", "súe sim dâi thîi nǎi khráp", "ซื้อซิมได้ที่ไหนครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Czy jest tu zasięg?", "thîi nîi mii sǎn-yaan mǎi khráp", "ที่นี่มีสัญญาณไหมครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Proszę o rachunek na firmę.", "khǎw bai kam-kàp phaa-sǐi khráp", "ขอใบกำกับภาษีครับ", "Pytania", 2, "w", ZP, "", ""),
("A2", "Kiedy jest termin?", "kam-nòt sòng mûea rài khráp", "กำหนดส่งเมื่อไหร่ครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Czy mogę wziąć numerek?", "khǎw bàt khiu dâi mǎi khráp", "ขอบัตรคิวได้ไหมครับ", "Pytania", 3, "w", PY, "", ""),
]
