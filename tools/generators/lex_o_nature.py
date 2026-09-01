# -*- coding: utf-8 -*-
"""Sesja O, partia 6 — PRZYRODA: zwierzęta, rośliny, krajobraz, materiały.

Sesja N podniosła Pogodę i przyrodę z 48 do 119 haseł, ale zrobiła to niemal
wyłącznie po stronie pogody. Zwierzęta i rośliny zostały na poziomie
„pies, kot, słoń, drzewo”.

To nie jest luka ozdobna. W Tajlandii zwierzę jest tematem rozmowy
codziennym: gekon na ścianie, małpy przy świątyni, komary o zmierzchu, psy
przy drodze, węże w porze deszczowej. Bez tych słów rozmowa o miejscu, w
którym się jest, urywa się po drugim zdaniu.

Druga warstwa tej partii to **materiały** — drewno, metal, szkło, plastik,
kamień. Potrzebne przy zakupach („czy to prawdziwa skóra?”), przy naprawach
i przy opisie czegokolwiek, co się widzi.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

PP = "Pogoda i przyroda"
DC = "Dom i codzienność"
ZP = "Zakupy i pieniądze"
CO = "Cechy i opinie"
MO = "Miejsca i orientacja"
ZD = "Zdrowie"
AW = "Awarie i pomoc"
CZ = "Czasowniki"
JN = "Jedzenie i napoje"
ST = "Small talk"
LI = "Liczby i liczenie"

NATURE = [

# =========================================================== zwierzęta domowe
("A1", "kurczak (zwierzę)", "kài", "ไก่", "Zwierzęta", 5, "n", PP,
 "To samo słowo na ptaka i na mięso — kài yâang to grillowany kurczak.", ""),
("A1", "krowa", "wua", "วัว", "Zwierzęta", 4, "n", PP, "", ""),
("A1", "bawół wodny", "khwaai", "ควาย", "Zwierzęta", 3, "n", PP,
 "Uwaga: nazwanie kogoś khwaai to poważna obelga („tępy jak bawół”).", ""),
("A1", "koza", "phǽ", "แพะ", "Zwierzęta", 2, "n", PP, "", ""),
("A1", "koń", "máa", "ม้า", "Zwierzęta", 3, "n", PP,
 "Para minimalna: máa (koń), mǎa (pies), mâa (przyjść). Jeden z najtrudniejszych zestawów.", ""),
("A1", "królik", "krà-tàai", "กระต่าย", "Zwierzęta", 2, "n", PP, "", ""),
("A1", "kaczka (zwierzę)", "pèt", "เป็ด", "Zwierzęta", 3, "n", PP, "", ""),
("A2", "szczur", "nǔu", "หนู", "Zwierzęta", 3, "n", PP,
 "To samo słowo służy jako czuły zwrot do dziecka. Kontekst rozstrzyga.", ""),

# =========================================================== zwierzęta dzikie
("A1", "małpa", "ling", "ลิง", "Zwierzęta", 4, "n", PP,
 "Przy świątyniach w Lopburi i na Phra Nang wyrywają torby — to ostrzeżenie, nie ciekawostka.", ""),
("A1", "tygrys", "sǔea", "เสือ", "Zwierzęta", 3, "n", PP,
 "Para minimalna z sûea (ubranie) i sùea (mata).", ""),
("A1", "wąż", "nguu", "งู", "Zwierzęta", 4, "n", PP, "", ""),
("A1", "jaszczurka", "jîng-jòk", "จิ้งจก", "Zwierzęta", 4, "n", PP,
 "Mały gekon domowy. Bywa w każdym pokoju i jest uważany za przynoszącego szczęście.", ""),
("A1", "krokodyl", "jaw-rá-khêe", "จระเข้", "Zwierzęta", 2, "n", PP, "", ""),
("A1", "żaba", "kòp", "กบ", "Zwierzęta", 3, "n", PP, "", ""),
("A1", "żółw", "tào", "เต่า", "Zwierzęta", 3, "n", PP, "", ""),
("A1", "ptak", "nók", "นก", "Zwierzęta", 4, "n", PP, "", ""),
("A2", "nietoperz", "kháang khaao", "ค้างคาว", "Zwierzęta", 2, "n", PP, "", ""),
("A2", "jeleń", "kwaang", "กวาง", "Zwierzęta", 2, "n", PP, "", ""),
("A2", "dzik", "mǔu pàa", "หมูป่า", "Zwierzęta", 2, "n", PP, "", "świnia las"),
("A2", "delfin", "loo-maa", "โลมา", "Zwierzęta", 2, "n", PP, "", ""),
("A2", "rekin", "chà-lǎam", "ฉลาม", "Zwierzęta", 2, "n", PP, "", ""),
("A2", "meduza", "maeng kà-phrun", "แมงกะพรุน", "Zwierzęta", 3, "n", ZD,
 "Na plażach Andamanu realne zagrożenie w porze deszczowej.", ""),

# =========================================================== owady
("A1", "komar", "yung", "ยุง", "Owady", 5, "n", PP, "", ""),
("A1", "mucha", "má-laeng wan", "แมลงวัน", "Owady", 4, "n", PP, "", "owad dzień"),
("A1", "mrówka", "mót", "มด", "Owady", 4, "n", PP,
 "W tropikach codzienny problem kuchenny, nie ciekawostka.", ""),
("A1", "karaluch", "má-laeng sàap", "แมลงสาบ", "Owady", 3, "n", PP, "", ""),
("A1", "pszczoła", "phûeng", "ผึ้ง", "Owady", 3, "n", PP, "", ""),
("A1", "motyl", "phǐi sûea", "ผีเสื้อ", "Owady", 3, "n", PP, "", "duch ubranie"),
("A2", "pająk", "maeng mum", "แมงมุม", "Owady", 3, "n", PP, "", ""),
("A2", "skorpion", "maeng pàwng", "แมงป่อง", "Owady", 2, "n", PP, "", ""),
("A2", "stonoga", "tà-khàap", "ตะขาบ", "Owady", 2, "n", PP, "", ""),
("A2", "pijawka", "thâak", "ทาก", "Owady", 2, "n", PP, "", ""),
("A2", "gąsienica", "nǎwn", "หนอน", "Owady", 2, "n", PP, "", ""),

# =========================================================== rośliny
("A1", "liść", "bai mái", "ใบไม้", "Rośliny", 4, "n", PP, "", "liść drewno"),
("A1", "gałąź", "kìng mái", "กิ่งไม้", "Rośliny", 3, "n", PP, "", ""),
("A1", "korzeń", "râak", "ราก", "Rośliny", 3, "n", PP, "", ""),
("A1", "nasiono", "mét", "เมล็ด", "Rośliny", 3, "n", PP, "", ""),
("A1", "trawa", "yâa", "หญ้า", "Rośliny", 4, "n", PP, "", ""),
("A1", "bambus", "mái phài", "ไม้ไผ่", "Rośliny", 3, "n", PP, "", ""),
("A1", "palma", "tôn maa-phráao", "ต้นมะพร้าว", "Rośliny", 3, "n", PP, "", "drzewo kokos"),
("A2", "orchidea", "klûai mái", "กล้วยไม้", "Rośliny", 3, "n", PP,
 "Dosłownie „drzewny banan”. Symbol tajskiego eksportu kwiatowego.", "banan drewno"),
("A2", "lotos", "bua", "บัว", "Rośliny", 3, "n", PP,
 "Kwiat świątynny — składa się go w ofierze razem z kadzidłem.", ""),
("A2", "jaśmin", "má-lí", "มะลิ", "Rośliny", 3, "n", PP,
 "Symbol Dnia Matki. Girlandy jaśminowe wieszane w taksówkach.", ""),
("A2", "ryż na polu", "tôn khâao", "ต้นข้าว", "Rośliny", 3, "n", PP, "", "roślina ryż"),
("A2", "las deszczowy", "pàa fǒn", "ป่าฝน", "Rośliny", 2, "n", PP, "", "las deszcz"),
("A2", "mangrowiec", "pàa chaai len", "ป่าชายเลน", "Rośliny", 2, "n", PP, "", ""),
("A2", "sadzić, uprawiać", "plùuk", "ปลูก", "Rośliny", 4, "v", CZ,
 "To samo słowo znaczy „budować dom” — plùuk bâan.", ""),
("A2", "podlewać", "rót nám", "รดน้ำ", "Rośliny", 3, "v", CZ, "", ""),
("A2", "zbierać plony", "kèp kìao", "เก็บเกี่ยว", "Rośliny", 2, "v", CZ, "", ""),
("A2", "kwitnąć", "bàan", "บาน", "Rośliny", 3, "v", CZ, "", ""),
("A2", "więdnąć", "hìao", "เหี่ยว", "Rośliny", 2, "v", CZ, "", ""),

# =========================================================== krajobraz
("A1", "wzgórze", "nooen", "เนิน", "Krajobraz", 3, "n", MO, "", ""),
("A1", "dolina", "hùp khǎo", "หุบเขา", "Krajobraz", 2, "n", MO, "", ""),
("A1", "jaskinia", "thâm", "ถ้ำ", "Krajobraz", 3, "n", MO, "", ""),
("A1", "wodospad", "nám tòk", "น้ำตก", "Krajobraz", 4, "n", MO, "", "woda spada"),
("A1", "strumień", "lam-thaan", "ลำธาร", "Krajobraz", 2, "n", MO, "", ""),
("A1", "staw", "bùeng", "บึง", "Krajobraz", 2, "n", MO, "", ""),
("A1", "zatoka", "àao", "อ่าว", "Krajobraz", 3, "n", MO, "", ""),
("A1", "przylądek", "làem", "แหลม", "Krajobraz", 2, "n", MO,
 "To samo słowo znaczy „ostry” — o nożu i o rozumie.", ""),
("A1", "rafa", "nǎew prà-kaa-rang", "แนวปะการัง", "Krajobraz", 2, "n", MO, "", ""),
("A2", "piasek", "sǎai", "ทราย", "Krajobraz", 4, "n", MO,
 "Para minimalna z sàai (w lewo) i sǎai (późno). Trzy różne słowa.", ""),
("A2", "błoto", "khloon", "โคลน", "Krajobraz", 3, "n", MO, "", ""),
("A2", "kurz", "fùn", "ฝุ่น", "Krajobraz", 4, "n", ZD,
 "W porze suchej na północy realny problem zdrowotny — fùn PM 2.5.", ""),
("A2", "skała", "hǐn phǎa", "หินผา", "Krajobraz", 2, "n", MO, "", ""),
("A2", "brzeg (rzeki)", "rim nám", "ริมน้ำ", "Krajobraz", 3, "n", MO, "", "krawędź woda"),
("A2", "pole ryżowe", "thûng naa", "ทุ่งนา", "Krajobraz", 3, "n", MO, "", ""),
("A2", "plantacja", "sǔan", "สวน", "Krajobraz", 4, "n", MO,
 "To samo słowo co „ogród” i „park”. sǔan sà-thǎa-rá-ná to park publiczny.", ""),
("A2", "granica (państwa)", "chaai daen", "ชายแดน", "Krajobraz", 3, "n", MO, "", ""),

# =========================================================== materiały
("A1", "drewno", "mái", "ไม้", "Materiały", 4, "n", ZP, "", ""),
("A1", "metal", "loo-hà", "โลหะ", "Materiały", 3, "n", ZP, "", ""),
("A1", "żelazo", "lèk", "เหล็ก", "Materiały", 3, "n", ZP, "", ""),
("A1", "złoto", "thawng", "ทอง", "Materiały", 4, "n", ZP,
 "Sklepy ze złotem są w Tajlandii także bankiem — złoto kupuje się jako oszczędność.", ""),
("A1", "srebro", "ngoen", "เงิน", "Materiały", 4, "n", ZP,
 "To samo słowo znaczy „pieniądze”. Kontekst rozstrzyga.", ""),
("A1", "szkło", "kâew", "แก้ว", "Materiały", 4, "n", ZP,
 "To samo słowo znaczy „szklanka”.", ""),
("A1", "plastik", "phlaat-sà-tìk", "พลาสติก", "Materiały", 4, "n", ZP, "", ""),
("A1", "papier", "krà-dàat", "กระดาษ", "Materiały", 4, "n", ZP, "", ""),
("A1", "guma", "yaang", "ยาง", "Materiały", 3, "n", ZP,
 "To samo słowo znaczy „opona” i „lateks”. Kauczuk to jeden z głównych towarów Tajlandii.", ""),
("A2", "cement", "pun", "ปูน", "Materiały", 2, "n", ZP, "", ""),
("A2", "kamień", "hǐn", "หิน", "Materiały", 3, "n", ZP, "", ""),
("A2", "glina", "din nǐao", "ดินเหนียว", "Materiały", 2, "n", ZP, "", "ziemia lepka"),
("A2", "wełna", "khǒn sàt", "ขนสัตว์", "Materiały", 2, "n", ZP, "", "sierść zwierzę"),
("A2", "ceramika", "khrûeang pân din phǎo", "เครื่องปั้นดินเผา", "Materiały", 2, "n", ZP, "", ""),

# =========================================================== opis przyrody
("A1", "dziki", "pàa", "ป่า", "Opis", 3, "adj", PP,
 "To samo słowo znaczy „las”. sàt pàa to dzikie zwierzę.", ""),
("A1", "oswojony", "chûeang", "เชื่อง", "Opis", 2, "adj", PP, "", ""),
("A1", "jadowity", "mii phít", "มีพิษ", "Opis", 3, "adj", ZD, "", "mieć truciznę"),
("A2", "gryzie (o zwierzęciu)", "kàt", "กัด", "Opis", 4, "v", CZ, "", ""),
("A2", "żądli", "tàwi", "ต่อย", "Opis", 3, "v", CZ,
 "To samo słowo znaczy „uderzyć pięścią” — o bokserze i o pszczole.", ""),
("A2", "lata (o ptaku)", "bin", "บิน", "Opis", 4, "v", CZ, "", ""),
("A2", "pełza", "khlaan", "คลาน", "Opis", 2, "v", CZ, "", ""),
("A2", "szczeka", "hào", "เห่า", "Opis", 3, "v", CZ, "", ""),
("A2", "karmić (zwierzę)", "hâi aa-hǎan", "ให้อาหาร", "Opis", 3, "v", CZ, "", "dawać jedzenie"),
("A2", "chronić", "khúm khrawng", "คุ้มครอง", "Opis", 2, "v", CZ, "", ""),
("A2", "zanieczyszczać", "tham hâi pen phít", "ทำให้เป็นพิษ", "Opis", 2, "v", CZ, "", "sprawiać być trucizną"),
("A2", "zanieczyszczenie", "mon-lá-phít", "มลพิษ", "Opis", 3, "n", PP, "", ""),
("A2", "śmieci na plaży", "khà-yà chaai hàat", "ขยะชายหาด", "Opis", 2, "n", PP, "", ""),
("A2", "ochrona środowiska", "kaan raksǎa sìng wâet láwm", "การรักษาสิ่งแวดล้อม", "Opis", 2, "n", PP, "", ""),
("A2", "środowisko", "sìng wâet láwm", "สิ่งแวดล้อม", "Opis", 3, "n", PP, "", "rzecz otaczać"),

# =========================================================== pory roku i klimat
("A1", "pora deszczowa", "nâa fǒn", "หน้าฝน", "Klimat", 5, "n", PP,
 "Tajlandia ma trzy pory: nâa fǒn, nâa nǎao, nâa ráwn. Nie cztery.", "sezon deszcz"),
("A1", "pora chłodna", "nâa nǎao", "หน้าหนาว", "Klimat", 4, "n", PP, "", "sezon zimno"),
("A1", "pora gorąca", "nâa ráwn", "หน้าร้อน", "Klimat", 4, "n", PP, "", "sezon gorąco"),
("A2", "wilgotne powietrze", "aa-kàat chúen", "อากาศชื้น", "Klimat", 3, "n", PP, "", ""),
("A2", "susza", "phai lâeng", "ภัยแล้ง", "Klimat", 2, "n", PP, "", ""),
("A2", "monsun", "lom mor-rá-sǔm", "ลมมรสุม", "Klimat", 2, "n", PP, "", "wiatr monsun"),
("A2", "przypływ", "nám khûen", "น้ำขึ้น", "Klimat", 3, "n", PP, "", "woda rośnie"),
("A2", "odpływ", "nám long", "น้ำลง", "Klimat", 3, "n", PP, "", "woda opada"),
("A2", "wschód słońca", "phrá aa-thít khûen", "พระอาทิตย์ขึ้น", "Klimat", 3, "n", PP, "", ""),
("A2", "zachód słońca", "phrá aa-thít tòk", "พระอาทิตย์ตก", "Klimat", 4, "n", PP, "", ""),
("A2", "księżyc w pełni", "phrá jan tem duang", "พระจันทร์เต็มดวง", "Klimat", 3, "n", PP,
 "Data świąt buddyjskich i słynnych imprez na Ko Pha-ngan.", ""),
("A2", "gwiazda", "daao", "ดาว", "Klimat", 3, "n", PP, "", ""),
("A2", "tęcza", "rúng kin nám", "รุ้งกินน้ำ", "Klimat", 2, "n", PP, "", "tęcza pije wodę"),
("A2", "cień", "rôm", "ร่ม", "Klimat", 4, "n", PP,
 "To samo słowo znaczy „parasol” — i jedno, i drugie chroni przed słońcem.", ""),
]
