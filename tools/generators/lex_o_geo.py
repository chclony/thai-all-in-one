# -*- coding: utf-8 -*-
"""Sesja O, partia 13 — GEOGRAFIA: kraje, narodowości, regiony Tajlandii.

Warstwa nieobecna w bazie prawie w całości, a potrzebna od pierwszej rozmowy:
„maa jàak nǎi khráp” — skąd jesteś — to pytanie numer jeden, a odpowiedź
wymaga nazwy kraju. Tajski tworzy je regularnie:

    prà-thêet + X   kraj (prà-thêet poo-laen — Polska)
    khon + X        obywatel (khon poo-laen — Polak)
    phaa-sǎa + X    język (phaa-sǎa poo-laen — polski)

Trzy wzorce, jedna lista rdzeni — i uczący się nazwie każdy kraj, o który
zapytają. To także najtańsza fonetycznie warstwa w całej sesji: `prà-thêet`,
`khon` i `phaa-sǎa` baza ma od poziomu A1.

Druga część partii to **regiony i miasta Tajlandii**. Rozmowa o kraju,
w którym się jest, bez nazw jego części kończy się po jednym zdaniu.
Isan, Północ, Południe to nie są ciekawostki geograficzne, tylko trzy różne
kuchnie, trzy dialekty i trzy odpowiedzi na pytanie, gdzie się jedzie.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

MO = "Miejsca i orientacja"
ST = "Small talk"
LR = "Ludzie i rodzina"
TR = "Transport"
PY = "Pytania"
PP = "Pogoda i przyroda"
PN = "Praca i nauka"
CD = "Czas i daty"
CO = "Cechy i opinie"
GU = "Gramatyka użytkowa"
AW = "Awarie i pomoc"

GEO = [

# =========================================================== kraje
("A1", "Polska", "prà-thêet poo-laen", "ประเทศโปแลนด์", "Kraje", 5, "n", ST, "", "kraj Polska"),
("A1", "Niemcy", "prà-thêet yoe-rá-man", "ประเทศเยอรมัน", "Kraje", 4, "n", ST, "", ""),
("A1", "Francja", "prà-thêet fà-ràng-sèet", "ประเทศฝรั่งเศส", "Kraje", 4, "n", ST, "", ""),
("A1", "Anglia", "prà-thêet ang-krìt", "ประเทศอังกฤษ", "Kraje", 4, "n", ST, "", ""),
("A1", "Ameryka", "prà-thêet à-mee-rí-kaa", "ประเทศอเมริกา", "Kraje", 4, "n", ST, "", ""),
("A1", "Japonia", "prà-thêet yîi-pùn", "ประเทศญี่ปุ่น", "Kraje", 4, "n", ST, "", ""),
("A1", "Chiny", "prà-thêet jiin", "ประเทศจีน", "Kraje", 5, "n", ST, "", ""),
("A1", "Korea", "prà-thêet kao-lǐi", "ประเทศเกาหลี", "Kraje", 4, "n", ST, "", ""),
("A1", "Indie", "prà-thêet in-dia", "ประเทศอินเดีย", "Kraje", 3, "n", ST, "", ""),
("A1", "Rosja", "prà-thêet rát-sia", "ประเทศรัสเซีย", "Kraje", 3, "n", ST, "", ""),
("A1", "Australia", "prà-thêet áwt-sà-tree-lia", "ประเทศออสเตรเลีย", "Kraje", 3, "n", ST, "", ""),
("A1", "Wietnam", "prà-thêet wîat-naam", "ประเทศเวียดนาม", "Kraje", 3, "n", ST, "", ""),
("A1", "Laos", "prà-thêet laao", "ประเทศลาว", "Kraje", 4, "n", ST,
 "Sąsiad zza Mekongu. Język laotański jest bliski dialektowi Isanu.", ""),
("A1", "Kambodża", "prà-thêet kam-phuu-chaa", "ประเทศกัมพูชา", "Kraje", 3, "n", ST, "", ""),
("A1", "Malezja", "prà-thêet maa-lee-sia", "ประเทศมาเลเซีย", "Kraje", 3, "n", ST, "", ""),
("A1", "Mjanma", "prà-thêet phá-mâa", "ประเทศพม่า", "Kraje", 3, "n", ST, "", ""),
("A1", "Singapur", "prà-thêet sǐng-khá-poo", "ประเทศสิงคโปร์", "Kraje", 3, "n", ST, "", ""),
("A2", "Indonezja", "prà-thêet in-doo-nii-sia", "ประเทศอินโดนีเซีย", "Kraje", 2, "n", ST, "", ""),
("A2", "Filipiny", "prà-thêet fí-líp-pin", "ประเทศฟิลิปปินส์", "Kraje", 2, "n", ST, "", ""),
("A2", "Włochy", "prà-thêet ì-taa-lîi", "ประเทศอิตาลี", "Kraje", 3, "n", ST, "", ""),
("A2", "Hiszpania", "prà-thêet sà-peen", "ประเทศสเปน", "Kraje", 3, "n", ST, "", ""),
("A2", "Holandia", "prà-thêet nee-thoe-laen", "ประเทศเนเธอร์แลนด์", "Kraje", 2, "n", ST, "", ""),
("A2", "Szwecja", "prà-thêet sà-wǐi-den", "ประเทศสวีเดน", "Kraje", 2, "n", ST, "", ""),
("A2", "Kanada", "prà-thêet khae-naa-daa", "ประเทศแคนาดา", "Kraje", 2, "n", ST, "", ""),
("A2", "Brazylia", "prà-thêet braa-sin", "ประเทศบราซิล", "Kraje", 2, "n", ST, "", ""),
("A2", "Ukraina", "prà-thêet yuu-khreen", "ประเทศยูเครน", "Kraje", 2, "n", ST, "", ""),
("A2", "Czechy", "prà-thêet chék-kia", "ประเทศเช็กเกีย", "Kraje", 2, "n", ST, "", ""),

# =========================================================== narodowości
("A1", "Polak", "khon poo-laen", "คนโปแลนด์", "Narodowości", 5, "n", LR, "", "człowiek Polska"),
("A1", "Taj", "khon thai", "คนไทย", "Narodowości", 5, "n", LR, "", ""),
("A1", "Niemiec", "khon yoe-rá-man", "คนเยอรมัน", "Narodowości", 3, "n", LR, "", ""),
("A1", "Anglik", "khon ang-krìt", "คนอังกฤษ", "Narodowości", 3, "n", LR, "", ""),
("A1", "Amerykanin", "khon à-mee-rí-kaa", "คนอเมริกา", "Narodowości", 3, "n", LR, "", ""),
("A1", "Japończyk", "khon yîi-pùn", "คนญี่ปุ่น", "Narodowości", 4, "n", LR, "", ""),
("A1", "Chińczyk", "khon jiin", "คนจีน", "Narodowości", 4, "n", LR,
 "Duża część Tajów ma chińskie korzenie — to temat rozmowy, nie podział.", ""),
("A1", "Koreańczyk", "khon kao-lǐi", "คนเกาหลี", "Narodowości", 3, "n", LR, "", ""),
("A1", "Hindus", "khon in-dia", "คนอินเดีย", "Narodowości", 2, "n", LR, "", ""),
("A1", "Rosjanin", "khon rát-sia", "คนรัสเซีย", "Narodowości", 3, "n", LR, "", ""),
("A2", "Francuz", "khon fà-ràng-sèet", "คนฝรั่งเศส", "Narodowości", 3, "n", LR, "", ""),
("A2", "Włoch", "khon ì-taa-lîi", "คนอิตาลี", "Narodowości", 2, "n", LR, "", ""),
("A2", "Wietnamczyk", "khon wîat-naam", "คนเวียดนาม", "Narodowości", 2, "n", LR, "", ""),
("A2", "Laotańczyk", "khon laao", "คนลาว", "Narodowości", 3, "n", LR, "", ""),
("A2", "Birmańczyk", "khon phá-mâa", "คนพม่า", "Narodowości", 3, "n", LR, "", ""),
("A2", "Kambodżanin", "khon kam-phuu-chaa", "คนกัมพูชา", "Narodowości", 2, "n", LR, "", ""),
("A2", "Malezyjczyk", "khon maa-lee-sia", "คนมาเลเซีย", "Narodowości", 2, "n", LR, "", ""),

# =========================================================== języki
("A1", "język polski", "phaa-sǎa poo-laen", "ภาษาโปแลนด์", "Języki", 5, "n", ST, "", "język Polska"),
("A1", "język japoński", "phaa-sǎa yîi-pùn", "ภาษาญี่ปุ่น", "Języki", 3, "n", ST, "", ""),
("A1", "język chiński", "phaa-sǎa jiin", "ภาษาจีน", "Języki", 4, "n", ST, "", ""),
("A1", "język koreański", "phaa-sǎa kao-lǐi", "ภาษาเกาหลี", "Języki", 3, "n", ST, "", ""),
("A1", "język niemiecki", "phaa-sǎa yoe-rá-man", "ภาษาเยอรมัน", "Języki", 3, "n", ST, "", ""),
("A1", "język francuski", "phaa-sǎa fà-ràng-sèet", "ภาษาฝรั่งเศส", "Języki", 3, "n", ST, "", ""),
("A1", "język rosyjski", "phaa-sǎa rát-sia", "ภาษารัสเซีย", "Języki", 2, "n", ST, "", ""),
("A2", "język mówiony", "phaa-sǎa phûut", "ภาษาพูด", "Języki", 4, "n", PN, "", "język mówić"),
("A2", "język pisany", "phaa-sǎa khǐan", "ภาษาเขียน", "Języki", 3, "n", PN, "", ""),
("A2", "dialekt", "phaa-sǎa thìn", "ภาษาถิ่น", "Języki", 3, "n", PN, "", "język miejscowy"),
("A2", "język potoczny", "phaa-sǎa chaao bâan", "ภาษาชาวบ้าน", "Języki", 3, "n", PN, "", ""),
("A2", "język urzędowy", "phaa-sǎa râat-chá-kaan", "ภาษาราชการ", "Języki", 2, "n", PN, "", ""),
("A2", "akcent, wymowa", "sǎm-niang", "สำเนียง", "Języki", 4, "n", PN,
 "sǎm-niang thai — tajski akcent. Częsty komplement: „phûut mii sǎm-niang thai”.", ""),
("A2", "słowo obce", "kham yuem", "คำยืม", "Języki", 2, "n", PN, "", "słowo pożyczone"),
("A2", "tłumacz (osoba)", "lâam", "ล่าม", "Języki", 3, "n", PN, "", ""),

# =========================================================== regiony Tajlandii
("A1", "północ Tajlandii", "phâak nǔea", "ภาคเหนือ", "Regiony", 4, "n", MO,
 "Chiang Mai, Chiang Rai, Pai. Chłodniej, góry, inna kuchnia i inny dialekt.", "region północ"),
("A1", "północny wschód, Isan", "phâak ì-sǎan", "ภาคอีสาน", "Regiony", 4, "n", MO,
 "Największy i najbiedniejszy region. Stąd pochodzi sôm tam i większość migrantów do Bangkoku.", ""),
("A1", "południe Tajlandii", "phâak tâi", "ภาคใต้", "Regiony", 4, "n", MO,
 "Wyspy, muzułmańska większość w czterech prowincjach, najostrzejsza kuchnia w kraju.", "region południe"),
("A1", "centrum kraju", "phâak klaang", "ภาคกลาง", "Regiony", 3, "n", MO, "", "region środek"),
("A1", "wschód", "phâak tà-wan àwk", "ภาคตะวันออก", "Regiony", 3, "n", MO, "", "region wschód"),
("A1", "zachód", "phâak tà-wan tòk", "ภาคตะวันตก", "Regiony", 3, "n", MO, "", ""),
("A1", "prowincja", "jang-wàt", "จังหวัด", "Regiony", 5, "n", MO,
 "Tajlandia ma 77 prowincji. Adres zawsze kończy się nazwą jang-wàt.", ""),
("A1", "powiat", "am-phoe", "อำเภอ", "Regiony", 4, "n", MO, "", ""),
("A1", "gmina", "tam-bon", "ตำบล", "Regiony", 3, "n", MO, "", ""),
("A1", "wieś", "mùu bâan", "หมู่บ้าน", "Regiony", 4, "n", MO, "", "grupa domów"),
("A2", "stolica", "mueang lǔang", "เมืองหลวง", "Regiony", 4, "n", MO, "", "miasto królewskie"),
("A2", "miasto powiatowe", "mueang", "เมือง", "Regiony", 5, "n", MO, "", ""),
("A2", "przedmieścia", "chaan mueang", "ชานเมือง", "Regiony", 3, "n", MO, "", "skraj miasta"),
("A2", "centrum miasta", "nai mueang", "ในเมือง", "Regiony", 5, "n", MO, "", "w mieście"),
("A2", "prowincja nadmorska", "jang-wàt chaai thá-lee", "จังหวัดชายทะเล", "Regiony", 2, "n", MO, "", ""),
("A2", "wyspa turystyczna", "kàw thâwng thîao", "เกาะท่องเที่ยว", "Regiony", 3, "n", TR, "", ""),

# =========================================================== kierunki świata
("A1", "północ (kierunek)", "thít nǔea", "ทิศเหนือ", "Kierunki", 3, "n", MO, "", ""),
("A1", "południe (kierunek)", "thít tâi", "ทิศใต้", "Kierunki", 3, "n", MO, "", ""),
("A1", "wschód (kierunek)", "thít tà-wan àwk", "ทิศตะวันออก", "Kierunki", 3, "n", MO, "", "kierunek słońce wychodzi"),
("A1", "zachód (kierunek)", "thít tà-wan tòk", "ทิศตะวันตก", "Kierunki", 3, "n", MO, "", "kierunek słońce spada"),
("A2", "w kierunku", "mûng nâa pai", "มุ่งหน้าไป", "Kierunki", 3, "adv", MO, "", ""),
("A2", "na zewnątrz", "khâang nâwk", "ข้างนอก", "Kierunki", 5, "adv", MO, "", ""),
("A2", "wewnątrz", "khâang nai", "ข้างใน", "Kierunki", 5, "adv", MO, "", ""),
("A2", "na górze", "khâang bon", "ข้างบน", "Kierunki", 5, "adv", MO, "", ""),
("A2", "na dole", "khâang lâang", "ข้างล่าง", "Kierunki", 5, "adv", MO, "", ""),
("A2", "z tyłu", "khâang lǎng", "ข้างหลัง", "Kierunki", 4, "adv", MO, "", ""),
("A2", "z przodu", "khâang nâa", "ข้างหน้า", "Kierunki", 4, "adv", MO, "", ""),
("A2", "po prawej stronie", "thaang khwǎa mue", "ทางขวามือ", "Kierunki", 5, "adv", MO, "", "strona prawa ręka"),
("A2", "po lewej stronie", "thaang sáai mue", "ทางซ้ายมือ", "Kierunki", 5, "adv", MO, "", ""),
("A2", "dookoła", "râwp râwp", "รอบๆ", "Kierunki", 3, "adv", MO, "", ""),
("A2", "wzdłuż", "taam nǎew", "ตามแนว", "Kierunki", 2, "adv", MO, "", ""),
("A2", "w poprzek", "khâam", "ข้าม", "Kierunki", 4, "adv", MO, "", ""),

# =========================================================== świat i podróż
("A1", "zagranica", "tàang prà-thêet", "ต่างประเทศ", "Podróż", 4, "n", TR, "", "obcy kraj"),
("A1", "granica państwowa", "dàan", "ด่าน", "Podróż", 3, "n", TR,
 "Także „punkt kontrolny” — dàan trùat na drodze.", ""),
("A1", "wiza", "wii-sâa", "วีซ่า", "Podróż", 5, "n", AW, "", ""),
("A1", "paszport", "nǎng-sǔe doen thaang", "หนังสือเดินทาง", "Podróż", 5, "n", AW, "", "księga podróży"),
("A1", "pieczątka w paszporcie", "traa prà-tháp nai phâat-sà-pòot", "ตราประทับในพาสปอร์ต", "Podróż", 2, "n", AW, "", ""),
("A1", "pobyt", "kaan phá-nák", "การพำนัก", "Podróż", 2, "n", AW, "", ""),
("A2", "przedłużenie pobytu", "kaan tàw wan", "การต่อวัน", "Podróż", 3, "n", AW, "", "przedłużyć dni"),
("A2", "przekroczenie terminu wizy", "yùu kooen", "อยู่เกิน", "Podróż", 3, "n", AW,
 "Kara liczona za każdy dzień. Sprawa poważna, nie formalność.", "zostać ponad"),
("A2", "urząd imigracyjny", "trùat khon khâo mueang", "ตรวจคนเข้าเมือง", "Podróż", 4, "n", AW, "", "kontrola ludzi wjeżdżających"),
("A2", "cło", "sǔn-lá-kaa-kawn", "ศุลกากร", "Podróż", 2, "n", AW, "", ""),
("A2", "deklaracja celna", "bai sǎm-daeng sǐn-kháa", "ใบสำแดงสินค้า", "Podróż", 2, "n", AW, "", ""),
("A2", "ambasada", "sà-thǎan thûut", "สถานทูต", "Podróż", 3, "n", AW,
 "W razie utraty paszportu pierwszy adres po policji.", ""),
("A2", "konsulat", "sà-thǎan kong-sǔn", "สถานกงสุล", "Podróż", 2, "n", AW, "", ""),
("A2", "obywatelstwo", "sǎn-châat", "สัญชาติ", "Podróż", 3, "n", AW, "", ""),
("A2", "zezwolenie na pracę", "bai à-nú-yâat tham ngaan", "ใบอนุญาตทำงาน", "Podróż", 3, "n", PN, "", ""),

# =========================================================== pytania geograficzne
("A1", "Z jakiego kraju?", "prà-thêet à-rai khráp", "ประเทศอะไรครับ", "Pytania", 4, "w", PY, "", ""),
("A1", "Gdzie mieszkasz?", "yùu thîi nǎi khráp", "อยู่ที่ไหนครับ", "Pytania", 5, "w", PY, "", ""),
("A1", "W której prowincji?", "jang-wàt à-rai khráp", "จังหวัดอะไรครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Byłeś już na północy?", "khooei pai phâak nǔea mǎi khráp", "เคยไปภาคเหนือไหมครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Który region najbardziej ci się podoba?", "châwp phâak nǎi thîi sùt khráp", "ชอบภาคไหนที่สุดครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Jak długo lecisz do Polski?", "bin pai poo-laen kìi chûa-moong khráp", "บินไปโปแลนด์กี่ชั่วโมงครับ", "Pytania", 2, "w", PY, "", ""),
("A2", "Czy tam jest zimno?", "thîi nân nǎao mǎi khráp", "ที่นั่นหนาวไหมครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Jestem z Polski.", "phǒm maa jàak poo-laen khráp", "ผมมาจากโปแลนด์ครับ", "Pytania", 5, "w", ST, "", ""),
("A2", "Mieszkam w Bangkoku.", "phǒm yùu krung-thêep khráp", "ผมอยู่กรุงเทพครับ", "Pytania", 5, "w", ST, "", ""),
("A2", "Podróżuję po Tajlandii.", "phǒm thîao nai prà-thêet thai khráp", "ผมเที่ยวในประเทศไทยครับ", "Pytania", 4, "w", ST, "", ""),

# =========================================================== opis miejsca
("A1", "spokojna okolica", "yâan ngîap", "ย่านเงียบ", "Opis", 3, "n", MO, "", "dzielnica cicha"),
("A1", "dzielnica", "yâan", "ย่าน", "Opis", 4, "n", MO, "", ""),
("A1", "hałaśliwe miejsce", "thîi nâa dang", "ที่เสียงดัง", "Opis", 3, "n", MO, "", ""),
("A2", "zatłoczony", "khon yóe", "คนเยอะ", "Opis", 5, "adj", CO, "", "ludzi dużo"),
("A2", "pusty (o miejscu)", "wâang plào", "ว่างเปล่า", "Opis", 3, "adj", CO, "", ""),
("A2", "turystyczny", "pen thîi thâwng thîao", "เป็นที่ท่องเที่ยว", "Opis", 3, "adj", TR, "", ""),
("A2", "lokalny, tutejszy", "thâwng thìn", "ท้องถิ่น", "Opis", 4, "adj", CO, "", ""),
("A2", "odludny", "hàang klai", "ห่างไกล", "Opis", 3, "adj", MO, "", ""),
("A2", "dobrze skomunikowany", "doen thaang sà-dùak", "เดินทางสะดวก", "Opis", 3, "adj", TR, "", "podróż wygodna"),
("A2", "w pobliżu", "yùu klâi klâi", "อยู่ใกล้ๆ", "Opis", 5, "adv", MO, "", ""),
]
