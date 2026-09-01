# -*- coding: utf-8 -*-
"""Sesja O, partia 15 — DOM: pomieszczenia, meble, ogród, wieś.

Kategoria Dom i codzienność miała 160 haseł, ale rozkładały się one na
czynności (sprzątanie, gotowanie), a nie na rzeczy, o których się mówi.
Wynajmując mieszkanie albo zgłaszając usterkę, uczący się potrzebuje nazwać
przedmiot, nie czynność.

Trzy wzorce trzymają tę partię:

    hâwng-   pomieszczenie (hâwng khrua — kuchnia)
    tûu-     szafa, skrzynia, każdy zamykany mebel (tûu sûea phâa — szafa)
    tó-      stół i wszystko blatowe (tó kin khâao — stół jadalny)

Druga część to **wieś i gospodarstwo** — pole ryżowe, kurnik, studnia,
zbiory. Nie dla folkloru: połowa mieszkańców Bangkoku pochodzi ze wsi
i wraca tam na Songkran, więc to codzienny temat rozmowy o rodzinie.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

DC = "Dom i codzienność"
HO = "Hotel"
AW = "Awarie i pomoc"
ZP = "Zakupy i pieniądze"
PP = "Pogoda i przyroda"
MO = "Miejsca i orientacja"
CZ = "Czasowniki"
PN = "Praca i nauka"
CO = "Cechy i opinie"
PY = "Pytania"
LR = "Ludzie i rodzina"
JN = "Jedzenie i napoje"
ZD = "Zdrowie"

HOME = [

# =========================================================== pomieszczenia
("A1", "kuchnia", "hâwng khrua", "ห้องครัว", "Pomieszczenia", 5, "n", DC, "", "pokój kuchnia"),
("A1", "salon", "hâwng nâng lên", "ห้องนั่งเล่น", "Pomieszczenia", 4, "n", DC, "", "pokój siedzieć bawić się"),
("A1", "jadalnia", "hâwng aa-hǎan", "ห้องอาหาร", "Pomieszczenia", 4, "n", DC, "", ""),
("A1", "sypialnia", "hâwng nawn", "ห้องนอน", "Pomieszczenia", 5, "n", DC, "", "pokój spać"),
("A1", "przedpokój", "thaang khâo bâan", "ทางเข้าบ้าน", "Pomieszczenia", 2, "n", DC, "", ""),
("A1", "garaż", "roong rót", "โรงรถ", "Pomieszczenia", 3, "n", DC, "", "hala pojazd"),
("A1", "taras", "chaan bâan", "ชานบ้าน", "Pomieszczenia", 3, "n", DC, "", ""),
("A1", "podwórko", "sà-nǎam nâa bâan", "สนามหน้าบ้าน", "Pomieszczenia", 3, "n", DC, "", ""),
("A1", "dach", "lǎng khaa", "หลังคา", "Pomieszczenia", 4, "n", DC, "", ""),
("A1", "ściana", "phà-nǎng", "ผนัง", "Pomieszczenia", 4, "n", DC, "", ""),
("A1", "sufit", "phee-daan", "เพดาน", "Pomieszczenia", 3, "n", DC, "", ""),
("A1", "podłoga", "phúen", "พื้น", "Pomieszczenia", 5, "n", DC, "", ""),
("A2", "piwnica", "hâwng tâi din", "ห้องใต้ดิน", "Pomieszczenia", 2, "n", DC, "", "pokój pod ziemią"),
("A2", "strych", "hâwng tâi lǎng khaa", "ห้องใต้หลังคา", "Pomieszczenia", 2, "n", DC, "", ""),
("A2", "pralnia", "hâwng sák phâa", "ห้องซักผ้า", "Pomieszczenia", 3, "n", DC, "", ""),
("A2", "spiżarnia", "hâwng kèp khǎwng", "ห้องเก็บของ", "Pomieszczenia", 3, "n", DC, "", "pokój przechowywać rzeczy"),
("A2", "korytarz", "thaang doen", "ทางเดิน", "Pomieszczenia", 3, "n", HO, "", "droga chodzenie"),
("A2", "brama, furtka", "prà-tuu rúa", "ประตูรั้ว", "Pomieszczenia", 3, "n", DC, "", "drzwi płot"),
("A2", "płot", "rúa", "รั้ว", "Pomieszczenia", 3, "n", DC, "", ""),
("A2", "schody", "khân ban-dai", "ขั้นบันได", "Pomieszczenia", 4, "n", DC, "", "stopień schody"),

# =========================================================== meble
("A1", "szafa na ubrania", "tûu sûea phâa", "ตู้เสื้อผ้า", "Meble", 4, "n", DC, "", "szafa ubranie"),
("A1", "regał na książki", "tûu nǎng-sǔe", "ตู้หนังสือ", "Meble", 3, "n", DC, "", ""),
("A1", "kredens", "tûu thûai chaam", "ตู้ถ้วยชาม", "Meble", 2, "n", DC, "", "szafa miski"),
("A1", "stół jadalny", "tó kin khâao", "โต๊ะกินข้าว", "Meble", 4, "n", DC, "", "stół jeść ryż"),
("A1", "stolik kawowy", "tó klaang", "โต๊ะกลาง", "Meble", 2, "n", DC, "", ""),
("A1", "kanapa", "soo-faa", "โซฟา", "Meble", 4, "n", DC, "", ""),
("A1", "fotel", "kâo-îi nuam", "เก้าอี้นวม", "Meble", 3, "n", DC, "", "krzesło miękkie"),
("A1", "taboret", "kâo-îi mâi mii phá-nák", "เก้าอี้ไม่มีพนัก", "Meble", 2, "n", DC, "", ""),
("A1", "łóżko", "tiang", "เตียง", "Meble", 5, "n", HO, "", ""),
("A1", "materac", "thîi nawn", "ที่นอน", "Meble", 4, "n", HO, "", "przyrząd spać"),
("A1", "poduszka", "mǎwn", "หมอน", "Meble", 5, "n", HO, "", ""),
("A1", "kołdra", "phâa hòm", "ผ้าห่ม", "Meble", 5, "n", HO, "", "materiał okrywać"),
("A1", "prześcieradło", "phâa puu thîi nawn", "ผ้าปูที่นอน", "Meble", 3, "n", HO, "", ""),
("A1", "zasłona", "phâa mâan", "ผ้าม่าน", "Meble", 3, "n", HO, "", ""),
("A1", "dywan", "phrom", "พรม", "Meble", 3, "n", DC, "", ""),
("A2", "mata do siedzenia", "sùea", "เสื่อ", "Meble", 3, "n", DC,
 "Para minimalna: sùea (mata), sûea (ubranie), sǔea (tygrys). Trzy tony, trzy słowa.", ""),
("A2", "lampa", "khoom fai", "โคมไฟ", "Meble", 4, "n", DC, "", ""),
("A2", "obraz na ścianie", "rûup khwǎen phà-nǎng", "รูปแขวนผนัง", "Meble", 2, "n", DC, "", ""),
("A2", "moskitiera", "múng", "มุ้ง", "Meble", 4, "n", ZD,
 "Na wsi i na wyspach rzecz codzienna, nie relikt.", ""),
("A2", "wentylator sufitowy", "phát lom phee-daan", "พัดลมเพดาน", "Meble", 3, "n", DC, "", ""),

# =========================================================== łazienka i kuchnia
("A1", "zlew", "àang láang jaan", "อ่างล้างจาน", "Sprzęty", 4, "n", DC, "", "miska myć talerze"),
("A1", "umywalka", "àang láang nâa", "อ่างล้างหน้า", "Sprzęty", 3, "n", HO, "", "miska myć twarz"),
("A1", "kran", "kók nám", "ก๊อกน้ำ", "Sprzęty", 5, "n", AW, "", ""),
("A1", "prysznic", "fàk bua", "ฝักบัว", "Sprzęty", 5, "n", HO, "", "strąk lotos"),
("A1", "wanna", "àang àap nám", "อ่างอาบน้ำ", "Sprzęty", 3, "n", HO, "", ""),
("A1", "toaleta (muszla)", "chàk khrôok", "ชักโครก", "Sprzęty", 4, "n", HO, "", ""),
("A1", "garnek", "mâw", "หม้อ", "Sprzęty", 4, "n", DC, "", ""),
("A1", "patelnia", "krà-thá", "กระทะ", "Sprzęty", 4, "n", DC, "", ""),
("A1", "pokrywka", "fǎa", "ฝา", "Sprzęty", 3, "n", DC, "", ""),
("A1", "deska do krojenia", "khǐang", "เขียง", "Sprzęty", 3, "n", DC, "", ""),
("A1", "chochla", "thápphii", "ทัพพี", "Sprzęty", 3, "n", DC, "", ""),
("A1", "durszlak", "krà-chǎwn", "กระชอน", "Sprzęty", 2, "n", DC, "", ""),
("A2", "moździerz", "khrók", "ครก", "Sprzęty", 3, "n", DC,
 "Bez niego nie ma sôm tam ani pasty curry. W tajskiej kuchni podstawowy sprzęt.", ""),
("A2", "garnek do ryżu", "mâw hǔng khâao", "หม้อหุงข้าว", "Sprzęty", 4, "n", DC,
 "Elektryczny, stoi w każdej kuchni i chodzi codziennie.", ""),
("A2", "termos", "krà-tìk nám", "กระติกน้ำ", "Sprzęty", 3, "n", DC, "", ""),
("A2", "dzbanek", "yùeak", "เหยือก", "Sprzęty", 2, "n", DC, "", ""),
("A2", "ścierka", "phâa khîi ríu", "ผ้าขี้ริ้ว", "Sprzęty", 2, "n", DC, "", ""),
("A2", "gąbka", "fawng nám", "ฟองน้ำ", "Sprzęty", 3, "n", DC, "", "piana woda"),
("A2", "płyn do naczyń", "nám yaa láang jaan", "น้ำยาล้างจาน", "Sprzęty", 3, "n", DC, "", ""),
("A2", "proszek do prania", "phong sák fâwk", "ผงซักฟอก", "Sprzęty", 3, "n", DC, "", ""),

# =========================================================== usterki
("A1", "przecieka", "rûa", "รั่ว", "Usterki", 4, "v", AW, "", ""),
("A1", "zatkane", "tan", "ตัน", "Usterki", 4, "adj", AW, "", ""),
("A1", "nie działa", "chái mâi dâi", "ใช้ไม่ได้", "Usterki", 5, "adj", AW, "", ""),
("A1", "brak prądu", "fai dàp", "ไฟดับ", "Usterki", 5, "n", AW, "", "światło zgasło"),
("A1", "brak wody", "nám mâi lǎi", "น้ำไม่ไหล", "Usterki", 4, "n", AW, "", "woda nie płynie"),
("A2", "spalona żarówka", "làwt fai khàat", "หลอดไฟขาด", "Usterki", 3, "n", AW, "", ""),
("A2", "wybity bezpiecznik", "fai tàt", "ไฟตัด", "Usterki", 2, "n", AW, "", ""),
("A2", "cieknący kran", "kók nám rûa", "ก๊อกน้ำรั่ว", "Usterki", 3, "n", AW, "", ""),
("A2", "pleśń", "raa", "รา", "Usterki", 3, "n", AW,
 "W porze deszczowej realny problem — na ścianach i na ubraniach.", ""),
("A2", "termity", "pluak", "ปลวก", "Usterki", 3, "n", AW,
 "Główny wróg drewnianych domów w tropikach.", ""),
("A2", "zamek w drzwiach", "kun-jae prà-tuu", "กุญแจประตู", "Usterki", 4, "n", AW, "", ""),
("A2", "zatrzasnąć się (bez klucza)", "luem kun-jae khâang nai", "ลืมกุญแจข้างใน", "Usterki", 3, "v", AW, "", ""),
("A2", "wymienić żarówkę", "plìan làwt fai", "เปลี่ยนหลอดไฟ", "Usterki", 3, "v", CZ, "", ""),
("A2", "wezwać fachowca", "rîak châang", "เรียกช่าง", "Usterki", 4, "v", CZ, "", ""),
("A2", "zgłosić usterkę", "jâeng sâwm", "แจ้งซ่อม", "Usterki", 4, "v", CZ, "", ""),

# =========================================================== ogród i wieś
("A1", "ogród przydomowy", "sǔan nâa bâan", "สวนหน้าบ้าน", "Wieś", 3, "n", PP, "", ""),
("A1", "doniczka", "krà-thǎang tôn mái", "กระถางต้นไม้", "Wieś", 3, "n", DC, "", ""),
("A1", "studnia", "bàw nám", "บ่อน้ำ", "Wieś", 3, "n", PP, "", "dół woda"),
("A1", "kurnik", "lâo kài", "เล้าไก่", "Wieś", 2, "n", PP, "", ""),
("A1", "obora", "khâwk wua", "คอกวัว", "Wieś", 2, "n", PP, "", ""),
("A1", "stodoła", "yúng khâao", "ยุ้งข้าว", "Wieś", 2, "n", PP, "", "spichlerz ryż"),
("A1", "narzędzie rolnicze", "khrûeang mue kà-sèet", "เครื่องมือเกษตร", "Wieś", 2, "n", PP, "", ""),
("A1", "motyka", "jàwp", "จอบ", "Wieś", 2, "n", PP, "", ""),
("A1", "sierp", "khiao", "เคียว", "Wieś", 2, "n", PP, "", ""),
("A2", "nawóz", "pǔi", "ปุ๋ย", "Wieś", 3, "n", PP, "", ""),
("A2", "pestycyd", "yaa khâa má-laeng", "ยาฆ่าแมลง", "Wieś", 2, "n", PP, "", "lek zabijać owady"),
("A2", "traktor", "rót thǎi", "รถไถ", "Wieś", 2, "n", PP, "", "pojazd orać"),
("A2", "zbiory", "phǒn phà-lìt", "ผลผลิต", "Wieś", 3, "n", PP, "", ""),
("A2", "susza na polu", "naa lâeng", "นาแล้ง", "Wieś", 2, "n", PP, "", ""),
("A2", "nawadnianie", "rá-bòp chon-lá-prà-thaan", "ระบบชลประทาน", "Wieś", 2, "n", PP, "", ""),
("A2", "sad owocowy", "sǔan phǒn-lá-mái", "สวนผลไม้", "Wieś", 3, "n", PP, "", ""),
("A2", "plantacja kauczuku", "sǔan yaang", "สวนยาง", "Wieś", 3, "n", PP,
 "Na południu główne źródło utrzymania. Kauczuk nacina się nocą.", ""),
("A2", "hodowla ryb", "bàw plaa", "บ่อปลา", "Wieś", 2, "n", PP, "", ""),

# =========================================================== życie codzienne
("A1", "budzić się", "tùen nawn", "ตื่นนอน", "Codzienność", 5, "v", CZ, "", ""),
("A1", "słać łóżko", "kèp thîi nawn", "เก็บที่นอน", "Codzienność", 3, "v", CZ, "", ""),
("A1", "brać prysznic", "àap nám", "อาบน้ำ", "Codzienność", 5, "v", CZ,
 "W tropikach dwa razy dziennie to norma, nie przesada. Pytanie „àap nám rǔe yang” jest zwykłe.", "kąpać woda"),
("A1", "myć zęby", "praeng fan", "แปรงฟัน", "Codzienność", 5, "v", CZ, "", ""),
("A1", "czesać się", "wǐi phǒm", "หวีผม", "Codzienność", 3, "v", CZ, "", ""),
("A1", "golić się", "koon nùat", "โกนหนวด", "Codzienność", 3, "v", CZ, "", ""),
("A1", "ubierać się", "tàeng tua", "แต่งตัว", "Codzienność", 5, "v", CZ, "", "ozdabiać ciało"),
("A1", "wychodzić z domu", "àwk jàak bâan", "ออกจากบ้าน", "Codzienność", 5, "v", CZ, "", ""),
("A1", "wracać do domu", "klàp bâan", "กลับบ้าน", "Codzienność", 5, "v", CZ, "", ""),
("A2", "robić zakupy spożywcze", "súe khǎwng khâo bâan", "ซื้อของเข้าบ้าน", "Codzienność", 4, "v", CZ, "", ""),
("A2", "wyrzucać śmieci", "thíng khà-yà", "ทิ้งขยะ", "Codzienność", 4, "v", CZ, "", ""),
("A2", "podlewać rośliny", "rót nám tôn mái", "รดน้ำต้นไม้", "Codzienność", 3, "v", CZ, "", ""),
("A2", "karmić psa", "hâi aa-hǎan mǎa", "ให้อาหารหมา", "Codzienność", 3, "v", CZ, "", ""),
("A2", "zamykać na klucz", "lák prà-tuu", "ล็อคประตู", "Codzienność", 4, "v", CZ, "", ""),
("A2", "gasić światło", "pìt fai", "ปิดไฟ", "Codzienność", 5, "v", CZ, "", ""),
("A2", "włączać klimatyzację", "pòet ae", "เปิดแอร์", "Codzienność", 5, "v", CZ, "", ""),

# =========================================================== pytania domowe
("A1", "Ile pokoi?", "kìi hâwng khráp", "กี่ห้องครับ", "Pytania", 4, "w", PY, "", ""),
("A1", "Czy jest umeblowane?", "mii fooe-ní-jôe mǎi khráp", "มีเฟอร์นิเจอร์ไหมครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Kiedy przyjdzie fachowiec?", "châang jà maa mûea rài khráp", "ช่างจะมาเมื่อไหร่ครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Czy prąd jest wliczony?", "ruam khâa fai mǎi khráp", "รวมค่าไฟไหมครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Można trzymać zwierzęta?", "líang sàt dâi mǎi khráp", "เลี้ยงสัตว์ได้ไหมครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Gdzie wyrzuca się śmieci?", "thíng khà-yà thîi nǎi khráp", "ทิ้งขยะที่ไหนครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Klimatyzacja nie działa.", "ae sǐa khráp", "แอร์เสียครับ", "Pytania", 5, "w", AW, "", ""),
("A2", "W łazience nie ma ciepłej wody.", "nám ráwn mâi lǎi khráp", "น้ำร้อนไม่ไหลครับ", "Pytania", 4, "w", AW, "", ""),
]
