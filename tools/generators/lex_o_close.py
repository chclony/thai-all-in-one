# -*- coding: utf-8 -*-
"""Sesja O, partia 20 — DOMKNIĘCIE: złożenia z sylab już w obiegu.

Partia zamykająca, dobrana pod jedno kryterium: **każde hasło ma składać się
wyłącznie z sylab, które baza już zna**. To nie jest ograniczenie stylistyczne,
tylko rachunek.

Ścieżka nasyca się nie na braku haseł, tylko na kolejności, w jakiej sylaby
wchodzą do obiegu. Hasło z jedną nieznaną sylabą czeka, aż ta sylaba wejdzie
skądinąd — a jeśli nie wejdzie nigdy, hasło zostaje w słowniku i kurs go
nie uczy. Hasło zbudowane z sylab znanych wchodzi do najbliższej lekcji
i, co ważniejsze, mieści się w zdaniach parowych z innymi takimi hasłami.
Dzięki temu podnosi nie tylko liczbę wprowadzonych słów, ale i GĘSTOŚĆ
lekcji: więcej haseł na to samo zdanie.

Materiał nie jest przez to sztuczny. Tajski jest językiem izolującym
i buduje słownictwo przez zestawianie morfemów — `hâwng` (pokój) + `nám`
(woda) to łazienka, `khon` (człowiek) + `khàp` (prowadzić) to kierowca.
Poniższe hasła to normalne, częste wyrazy; ich zaleta polega tylko na tym,
że nie wymagają nowej fonetyki.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

DC = "Dom i codzienność"
ZP = "Zakupy i pieniądze"
JN = "Jedzenie i napoje"
RE = "Restauracja"
TR = "Transport"
MO = "Miejsca i orientacja"
HO = "Hotel"
ZD = "Zdrowie"
AW = "Awarie i pomoc"
PN = "Praca i nauka"
LR = "Ludzie i rodzina"
ST = "Small talk"
CO = "Cechy i opinie"
CZ = "Czasowniki"
CD = "Czas i daty"
LI = "Liczby i liczenie"
PY = "Pytania"
GU = "Gramatyka użytkowa"
PP = "Pogoda i przyroda"
PG = "Podstawy i grzeczność"

CLOSE = [

# =========================================================== nám- : płyny
("A1", "woda pitna", "nám dùem", "น้ำดื่ม", "Płyny", 5, "n", JN, "", "woda pić"),
("A1", "woda z kranu", "nám prà-pàa", "น้ำประปา", "Płyny", 4, "n", DC,
 "W Tajlandii nie do picia. Pije się wyłącznie nám khùat albo nám tûu.", ""),
("A1", "woda butelkowana", "nám khùat", "น้ำขวด", "Płyny", 5, "n", JN, "", ""),
("A1", "wrzątek", "nám ráwn jàt", "น้ำร้อนจัด", "Płyny", 3, "n", JN, "", "woda bardzo gorąca"),
("A1", "woda przegotowana", "nám tôm", "น้ำต้ม", "Płyny", 3, "n", JN, "", ""),
("A1", "woda słona", "nám khem", "น้ำเค็ม", "Płyny", 2, "n", PP, "", ""),
("A1", "woda słodka (nie morska)", "nám jùet", "น้ำจืด", "Płyny", 2, "n", PP, "", ""),
("A1", "sok z limonki", "nám má-naao", "น้ำมะนาว", "Płyny", 4, "n", JN, "", ""),
("A1", "syrop cukrowy", "nám chûeam", "น้ำเชื่อม", "Płyny", 2, "n", JN, "", ""),
("A1", "sos, zalewa", "nám jîm", "น้ำจิ้ม", "Płyny", 5, "n", RE,
 "Miseczka sosu do maczania. Do każdego grillowanego dania inny.", "woda maczać"),
("A1", "bulion", "nám súp", "น้ำซุป", "Płyny", 4, "n", RE, "", ""),
("A2", "woda deszczowa", "nám fǒn", "น้ำฝน", "Płyny", 3, "n", PP, "", ""),
("A2", "powódź", "nám thûam", "น้ำท่วม", "Płyny", 4, "n", AW,
 "W porze deszczowej temat codzienny, zwłaszcza w Bangkoku.", "woda zalewa"),
("A2", "para wodna", "ai nám", "ไอน้ำ", "Płyny", 2, "n", PP, "", ""),
("A2", "perfumy", "nám hǎwm", "น้ำหอม", "Płyny", 3, "n", ZP, "", "woda pachnąca"),

# =========================================================== hâwng- : pokoje
("A1", "pokój jednoosobowy", "hâwng dìao", "ห้องเดี่ยว", "Pokoje", 4, "n", HO, "", ""),
("A1", "pokój dwuosobowy", "hâwng khûu", "ห้องคู่", "Pokoje", 4, "n", HO, "", ""),
("A1", "pokój z klimatyzacją", "hâwng ae", "ห้องแอร์", "Pokoje", 5, "n", HO, "", ""),
("A1", "pokój z wentylatorem", "hâwng phát lom", "ห้องพัดลม", "Pokoje", 4, "n", HO,
 "Tańsza opcja w każdym pensjonacie. Warto znać przy pytaniu o cenę.", ""),
("A1", "pokój z oknem", "hâwng mii nâa tàang", "ห้องมีหน้าต่าง", "Pokoje", 3, "n", HO, "", ""),
("A1", "wolny pokój", "hâwng wâang", "ห้องว่าง", "Pokoje", 5, "n", HO, "", ""),
("A1", "pokój na górze", "hâwng chán bon", "ห้องชั้นบน", "Pokoje", 3, "n", HO, "", ""),
("A2", "sala lekcyjna", "hâwng rian", "ห้องเรียน", "Pokoje", 4, "n", PN, "", ""),
("A2", "pokój prób", "hâwng lawng sûea", "ห้องลองเสื้อ", "Pokoje", 3, "n", ZP, "", "pokój przymierzać ubranie"),
("A2", "poczekalnia", "hâwng phák raw", "ห้องพักรอ", "Pokoje", 3, "n", TR, "", ""),

# =========================================================== khon- : ludzie
("A1", "człowiek dorosły", "khon yài", "คนใหญ่", "Ludzie", 3, "n", LR, "", ""),
("A1", "starsza osoba", "khon kàe", "คนแก่", "Ludzie", 4, "n", LR, "", ""),
("A1", "człowiek chory", "khon pùai", "คนป่วย", "Ludzie", 4, "n", ZD, "", ""),
("A1", "człowiek bogaty", "khon ruai", "คนรวย", "Ludzie", 4, "n", LR, "", ""),
("A1", "człowiek biedny", "khon jon", "คนจน", "Ludzie", 4, "n", LR, "", ""),
("A1", "człowiek zajęty", "khon yûng", "คนยุ่ง", "Ludzie", 3, "n", LR, "", ""),
("A1", "człowiek samotny", "khon diao", "คนเดียว", "Ludzie", 4, "n", LR,
 "Także „sam, w pojedynkę”: pai khon diao — idę sam.", ""),
("A1", "człowiek dobry", "khon dii", "คนดี", "Ludzie", 4, "n", CO, "", ""),
("A1", "człowiek zły", "khon mâi dii", "คนไม่ดี", "Ludzie", 3, "n", CO, "", ""),
("A2", "człowiek pracujący", "khon tham ngaan", "คนทำงาน", "Ludzie", 4, "n", PN, "", ""),
("A2", "człowiek z zewnątrz", "khon nâwk", "คนนอก", "Ludzie", 2, "n", LR, "", ""),
("A2", "swój człowiek", "khon kan eeng", "คนกันเอง", "Ludzie", 3, "n", LR, "", ""),
("A2", "człowiek z tej okolicy", "khon thǽew níi", "คนแถวนี้", "Ludzie", 3, "n", MO, "", ""),

# =========================================================== khǎwng- : rzeczy
("A1", "rzecz nowa", "khǎwng mài", "ของใหม่", "Rzeczy", 4, "n", ZP, "", ""),
("A1", "rzecz stara", "khǎwng kào", "ของเก่า", "Rzeczy", 4, "n", ZP, "", ""),
("A1", "prezent", "khǎwng khwǎn", "ของขวัญ", "Rzeczy", 5, "n", ST, "", ""),
("A1", "pamiątka", "khǎwng thîi rá-lúek", "ของที่ระลึก", "Rzeczy", 4, "n", ZP, "", "rzecz do wspominania"),
("A1", "zabawka", "khǎwng lên", "ของเล่น", "Rzeczy", 3, "n", ZP, "", "rzecz do zabawy"),
("A1", "rzecz zgubiona", "khǎwng hǎai", "ของหาย", "Rzeczy", 4, "n", AW, "", ""),
("A1", "rzeczy osobiste", "khǎwng chái sùan tua", "ของใช้ส่วนตัว", "Rzeczy", 3, "n", HO, "", ""),
("A1", "rzeczy do jedzenia", "khǎwng kin", "ของกิน", "Rzeczy", 5, "n", JN, "", ""),
("A1", "napoje (ogólnie)", "khǎwng dùem", "ของดื่ม", "Rzeczy", 4, "n", JN, "", ""),
("A2", "towar", "sǐn-kháa", "สินค้า", "Rzeczy", 4, "n", ZP, "", ""),
("A2", "bagaż (ogółem)", "khǎwng doen thaang", "ของเดินทาง", "Rzeczy", 3, "n", TR, "", ""),
("A2", "rzecz zepsuta", "khǎwng sǐa", "ของเสีย", "Rzeczy", 3, "n", AW, "", ""),

# =========================================================== rót-, thîi-
("A1", "autobus klimatyzowany", "rót ae", "รถแอร์", "Pojazdy", 4, "n", TR, "", ""),
("A1", "autobus zwykły", "rót thammádaa", "รถธรรมดา", "Pojazdy", 3, "n", TR, "", ""),
("A1", "pociąg nocny", "rót fai klaang khuen", "รถไฟกลางคืน", "Pojazdy", 3, "n", TR, "", ""),
("A1", "ciężarówka", "rót ban-thúk", "รถบรรทุก", "Pojazdy", 3, "n", TR, "", ""),
("A1", "wóz z jedzeniem", "rót khěn aa-hǎan", "รถเข็นอาหาร", "Pojazdy", 4, "n", RE, "", "wózek jedzenie"),
("A1", "wózek sklepowy", "rót khěn", "รถเข็น", "Pojazdy", 4, "n", ZP, "", ""),
("A1", "prywatny samochód", "rót sùan tua", "รถส่วนตัว", "Pojazdy", 3, "n", TR, "", ""),
("A1", "wynajęty samochód", "rót châo", "รถเช่า", "Pojazdy", 4, "n", TR, "", ""),
("A1", "miejsce do siedzenia", "thîi nâng wâang", "ที่นั่งว่าง", "Miejsca", 4, "n", TR, "", ""),
("A1", "miejsce na bagaż", "thîi waang krà-pǎo", "ที่วางกระเป๋า", "Miejsca", 3, "n", TR, "", ""),
("A1", "parking", "thîi jàwt rót", "ที่จอดรถ", "Miejsca", 5, "n", TR, "", "miejsce parkować pojazd"),
("A1", "punkt widokowy", "thîi chom wiu", "ที่ชมวิว", "Miejsca", 3, "n", MO, "", ""),
("A2", "adres zamieszkania", "thîi yùu aa-sǎi", "ที่อยู่อาศัย", "Miejsca", 3, "n", AW, "", ""),
("A2", "miejsce pracy", "thîi tham ngaan", "ที่ทำงาน", "Miejsca", 5, "n", PN, "", ""),
("A2", "miejsce spotkania", "thîi nát", "ที่นัด", "Miejsca", 4, "n", ST, "", ""),

# =========================================================== khâa- : opłaty
("A1", "opłata za wstęp", "khâa khâo chom", "ค่าเข้าชม", "Opłaty", 4, "n", ZP, "", "opłata wejść oglądać"),
("A1", "opłata za taksówkę", "khâa tháek-sîi", "ค่าแท็กซี่", "Opłaty", 4, "n", TR, "", ""),
("A1", "opłata za pokój", "khâa hâwng", "ค่าห้อง", "Opłaty", 5, "n", HO, "", ""),
("A1", "opłata za jedzenie", "khâa aa-hǎan", "ค่าอาหาร", "Opłaty", 4, "n", RE, "", ""),
("A1", "opłata za leczenie", "khâa rák-sǎa", "ค่ารักษา", "Opłaty", 4, "n", ZD, "", ""),
("A1", "opłata za naukę", "khâa rian", "ค่าเรียน", "Opłaty", 3, "n", PN, "", ""),
("A1", "opłata za telefon", "khâa thoo", "ค่าโทร", "Opłaty", 3, "n", AW, "", ""),
("A2", "koszty utrzymania", "khâa khrawng chîip", "ค่าครองชีพ", "Opłaty", 3, "n", ZP, "", ""),
("A2", "opłata za wynajem skutera", "khâa châo maw-toe-sai", "ค่าเช่ามอเตอร์ไซค์", "Opłaty", 3, "n", TR, "", ""),
("A2", "napiwek", "khâa thíp", "ค่าทิป", "Opłaty", 3, "n", RE,
 "Nieobowiązkowy. W restauracjach z obsługą zwykle zaokrągla się rachunek.", ""),

# =========================================================== czasowniki złożone
("A1", "iść pieszo do domu", "doen klàp bâan", "เดินกลับบ้าน", "Czynności", 3, "v", CZ, "", ""),
("A1", "iść coś zjeść", "pai kin khâao", "ไปกินข้าว", "Czynności", 5, "v", CZ,
 "Zaproszenie na wspólny posiłek. Dosłownie „iść jeść ryż”.", ""),
("A1", "iść po zakupy", "pai súe khǎwng", "ไปซื้อของ", "Czynności", 5, "v", CZ, "", ""),
("A1", "iść do pracy", "pai tham ngaan", "ไปทำงาน", "Czynności", 5, "v", CZ, "", ""),
("A1", "iść spać", "pai nawn", "ไปนอน", "Czynności", 5, "v", CZ, "", ""),
("A1", "wrócić do pokoju", "klàp hâwng", "กลับห้อง", "Czynności", 4, "v", CZ, "", ""),
("A1", "czekać na kogoś tutaj", "raw thîi nîi", "รอที่นี่", "Czynności", 4, "v", CZ, "", ""),
("A1", "zapytać kogoś o drogę", "thǎam thaang", "ถามทาง", "Czynności", 5, "v", CZ, "", ""),
("A1", "poprosić o rachunek", "khǎw bin", "ขอบิล", "Czynności", 5, "v", CZ, "", ""),
("A1", "zamówić jedzenie", "sàng aa-hǎan", "สั่งอาหาร", "Czynności", 5, "v", CZ, "", ""),
("A2", "sprawdzić cenę", "chék raa-khaa", "เช็คราคา", "Czynności", 4, "v", CZ, "", ""),
("A2", "zarezerwować pokój", "jawng hâwng", "จองห้อง", "Czynności", 5, "v", CZ, "", ""),
("A2", "odwołać rezerwację", "yók lôek kaan jawng", "ยกเลิกการจอง", "Czynności", 4, "v", CZ, "", ""),
("A2", "zmienić pokój", "plìan hâwng", "เปลี่ยนห้อง", "Czynności", 4, "v", CZ, "", ""),
("A2", "wypożyczyć rower", "châo jàk-krà-yaan", "เช่าจักรยาน", "Czynności", 3, "v", CZ, "", ""),
("A2", "zapytać o cenę", "thǎam raa-khaa", "ถามราคา", "Czynności", 5, "v", CZ, "", ""),
("A2", "poprosić o wodę", "khǎw nám", "ขอน้ำ", "Czynności", 5, "v", CZ, "", ""),
("A2", "zapłacić kartą", "jàai dûai bàt", "จ่ายด้วยบัตร", "Czynności", 5, "v", CZ, "", ""),
("A2", "zapłacić gotówką", "jàai ngoen sòt", "จ่ายเงินสด", "Czynności", 5, "v", CZ, "", ""),
("A2", "zostawić bagaż", "fàak krà-pǎo", "ฝากกระเป๋า", "Czynności", 4, "v", CZ, "", ""),
("A2", "odebrać bagaż", "ráp krà-pǎo", "รับกระเป๋า", "Czynności", 4, "v", CZ, "", ""),
("A2", "wezwać taksówkę", "rîak tháek-sîi", "เรียกแท็กซี่", "Czynności", 5, "v", CZ, "", ""),
("A2", "zgubić klucz", "tham kun-jae hǎai", "ทำกุญแจหาย", "Czynności", 4, "v", CZ, "", ""),
("A2", "zapomnieć czegoś w pokoju", "luem khǎwng wái nai hâwng", "ลืมของไว้ในห้อง", "Czynności", 3, "v", CZ, "", ""),

# =========================================================== opisy złożone
("A1", "bardzo dobry", "dii mâak", "ดีมาก", "Opisy", 5, "adj", CO, "", ""),
("A1", "całkiem dobry", "dii phaw chái", "ดีพอใช้", "Opisy", 4, "adj", CO, "", "dobry wystarczająco do użycia"),
("A1", "niezbyt dobry", "mâi khâwi dii", "ไม่ค่อยดี", "Opisy", 5, "adj", CO,
 "mâi khâwi to najuprzejmiejsze zaprzeczenie: „niezbyt”, nie „wcale”.", ""),
("A1", "trochę drogi", "phaeng nít nàwi", "แพงนิดหน่อย", "Opisy", 4, "adj", ZP, "", ""),
("A1", "całkiem tani", "thùuk phaw somkhuan", "ถูกพอสมควร", "Opisy", 3, "adj", ZP, "", ""),
("A1", "bardzo daleko", "klai mâak", "ไกลมาก", "Opisy", 5, "adj", MO, "", ""),
("A1", "całkiem blisko", "klâi phaw somkhuan", "ใกล้พอสมควร", "Opisy", 3, "adj", MO, "", ""),
("A1", "zbyt gorąco", "ráwn kooen pai", "ร้อนเกินไป", "Opisy", 5, "adj", PP, "", ""),
("A1", "za zimno", "yen kooen pai", "เย็นเกินไป", "Opisy", 4, "adj", PP, "", ""),
("A1", "trochę za ostre", "phèt pai nít", "เผ็ดไปนิด", "Opisy", 4, "adj", RE, "", ""),
("A2", "w miarę czysty", "sà-àat phaw chái", "สะอาดพอใช้", "Opisy", 3, "adj", HO, "", ""),
("A2", "nie do przyjęcia", "ráp mâi dâi", "รับไม่ได้", "Opisy", 3, "adj", CO, "", ""),
("A2", "warte swojej ceny", "khúm raa-khaa", "คุ้มราคา", "Opisy", 4, "adj", ZP, "", ""),
("A2", "łatwe do znalezienia", "hǎa ngâai", "หาง่าย", "Opisy", 3, "adj", MO, "", ""),
("A2", "trudne do znalezienia", "hǎa yâak", "หายาก", "Opisy", 3, "adj", MO, "", ""),
("A2", "wygodny do chodzenia", "doen sà-dùak", "เดินสะดวก", "Opisy", 3, "adj", MO, "", ""),

# =========================================================== zwroty złożone
("A1", "Poproszę jeszcze jedno.", "khǎw ìik nùeng khráp", "ขออีกหนึ่งครับ", "Zwroty", 5, "w", RE, "", ""),
("A1", "Poproszę bez tego.", "khǎw mâi sài an níi khráp", "ขอไม่ใส่อันนี้ครับ", "Zwroty", 4, "w", RE, "", ""),
("A1", "Chwileczkę, proszę.", "raw sàk khrûu khráp", "รอสักครู่ครับ", "Zwroty", 5, "w", PG, "", ""),
("A1", "Idę tam pieszo.", "phǒm doen pai khráp", "ผมเดินไปครับ", "Zwroty", 4, "w", MO, "", ""),
("A1", "Jestem tu pierwszy raz.", "maa khráng râek khráp", "มาครั้งแรกครับ", "Zwroty", 5, "w", ST, "", ""),
("A1", "Nie znam tej okolicy.", "phǒm mâi rúu-jàk thǽew níi khráp", "ผมไม่รู้จักแถวนี้ครับ", "Zwroty", 4, "w", MO, "", ""),
("A2", "Czy to jest wliczone?", "ruam láew rǔe yang khráp", "รวมแล้วหรือยังครับ", "Zwroty", 4, "w", PY, "", ""),
("A2", "Zapłacę osobno.", "phǒm jàai yâek khráp", "ผมจ่ายแยกครับ", "Zwroty", 4, "w", ZP, "", ""),
("A2", "Zapłacimy razem.", "jàai ruam kan khráp", "จ่ายรวมกันครับ", "Zwroty", 4, "w", ZP, "", ""),
("A2", "Wolę coś tańszego.", "phǒm châwp an thùuk kwàa khráp", "ผมชอบอันถูกกว่าครับ", "Zwroty", 4, "w", ZP, "", ""),
("A2", "Czy jest coś mniejszego?", "mii an lék kwàa mǎi khráp", "มีอันเล็กกว่าไหมครับ", "Zwroty", 4, "w", PY, "", ""),
("A2", "Czy jest coś większego?", "mii an yài kwàa mǎi khráp", "มีอันใหญ่กว่าไหมครับ", "Zwroty", 4, "w", PY, "", ""),
("A2", "Wezmę to.", "ao an níi khráp", "เอาอันนี้ครับ", "Zwroty", 5, "w", ZP, "", ""),
("A2", "Nie, dziękuję.", "mâi ao khráp khàwp khun", "ไม่เอาครับขอบคุณ", "Zwroty", 5, "w", PG, "", ""),
("A2", "Muszę się zastanowić.", "khǎw khít duu kàwn khráp", "ขอคิดดูก่อนครับ", "Zwroty", 5, "w", ZP,
 "Uprzejme wyjście z targowania bez utraty twarzy po żadnej stronie.", ""),
("A2", "Wrócę później.", "dǐao klàp maa mài khráp", "เดี๋ยวกลับมาใหม่ครับ", "Zwroty", 4, "w", ZP, "", ""),
("A2", "Czy mogę zobaczyć?", "khǎw duu nàwi dâi mǎi khráp", "ขอดูหน่อยได้ไหมครับ", "Zwroty", 5, "w", PY, "", ""),
("A2", "Proszę mi to zapakować.", "chûai hàw hâi nàwi khráp", "ช่วยห่อให้หน่อยครับ", "Zwroty", 4, "w", ZP, "", ""),
("A2", "Gdzie jest najbliższy…?", "thîi klâi thîi sùt yùu nǎi khráp", "ที่ใกล้ที่สุดอยู่ไหนครับ", "Zwroty", 4, "w", PY, "", ""),
("A2", "O której się zamyka?", "pìt kìi moong khráp", "ปิดกี่โมงครับ", "Zwroty", 5, "w", PY, "", ""),

# =========================================================== stany i czas
("A1", "cały dzień", "tháng wan", "ทั้งวัน", "Czas", 4, "n", CD, "", ""),
("A1", "cały tydzień", "tháng aa-thít", "ทั้งอาทิตย์", "Czas", 3, "n", CD, "", ""),
("A1", "pół dnia", "khrûeng wan", "ครึ่งวัน", "Czas", 4, "n", CD, "", ""),
("A1", "kilka dni", "sǎwng sǎam wan", "สองสามวัน", "Czas", 4, "n", CD, "", ""),
("A1", "za tydzień", "ìik nùeng aa-thít", "อีกหนึ่งอาทิตย์", "Czas", 4, "n", CD, "", ""),
("A1", "za miesiąc", "ìik nùeng duean", "อีกหนึ่งเดือน", "Czas", 4, "n", CD, "", ""),
("A2", "przez cały czas", "tà-làwt wee-laa", "ตลอดเวลา", "Czas", 4, "adv", CD, "", ""),
("A2", "przez chwilę", "chûa khrûu", "ชั่วครู่", "Czas", 3, "adv", CD, "", ""),
("A2", "w tym samym dniu", "wan diao kan", "วันเดียวกัน", "Czas", 3, "adv", CD, "", ""),
("A2", "dzień wcześniej", "kàwn nùeng wan", "ก่อนหนึ่งวัน", "Czas", 3, "adv", CD, "", ""),
("A2", "dzień później", "lǎng nùeng wan", "หลังหนึ่งวัน", "Czas", 3, "adv", CD, "", ""),

# =========================================================== ilość złożona
("A1", "dużo ludzi", "khon mâak", "คนมาก", "Ilość", 4, "n", MO, "", ""),
("A1", "mało ludzi", "khon náwi", "คนน้อย", "Ilość", 3, "n", MO, "", ""),
("A1", "za dużo rzeczy", "khǎwng yóe kooen pai", "ของเยอะเกินไป", "Ilość", 3, "n", DC, "", ""),
("A1", "wystarczająco dużo", "mâak phaw", "มากพอ", "Ilość", 4, "adv", LI, "", ""),
("A1", "prawie nic", "kùeap mâi mii", "เกือบไม่มี", "Ilość", 3, "adv", LI, "", ""),
("A2", "coraz więcej ludzi", "khon mâak khûen", "คนมากขึ้น", "Ilość", 3, "n", MO, "", ""),
("A2", "połowa ceny", "khrûeng raa-khaa", "ครึ่งราคา", "Ilość", 3, "n", ZP, "", ""),
("A2", "dwa razy więcej", "mâak kwàa sǎwng thâo", "มากกว่าสองเท่า", "Ilość", 2, "adv", LI, "", ""),
]
