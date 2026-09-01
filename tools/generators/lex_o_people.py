# -*- coding: utf-8 -*-
"""Sesja O, partia 2 — LUDZIE: zawody, role, rodzina, wiek.

Tajski nazywa wykonawcę czterema produktywnymi przedrostkami:

    nák-     ktoś, kto się czymś zajmuje zawodowo lub z pasji (nák rian)
    phûu-    osoba w roli, rejestr wyższy i urzędowy (phûu doi-sǎan)
    châang-  rzemieślnik, fachowiec (châang fai — elektryk)
    khon-    człowiek jakiegoś rodzaju, rejestr potoczny (khon khàp rót)

Wszystkie cztery stoją przed rdzeniem, który uczący się zna już z bazy —
`fai` (prąd), `mái` (drewno), `rót` (pojazd), `khǎai` (sprzedawać). Nowe
hasło nie wnosi nowej sylaby, więc ścieżka bierze je od razu.

Zawody to nie ozdoba kursu. Pierwsze pytanie, jakie Taj zadaje nieznajomemu
po „skąd jesteś”, brzmi „tham ngaan à-rai” — czym się zajmujesz. Baza miała
na to 94 hasła w kategorii Ludzie i rodzina; rozmowa o czyjejś pracy
rozbijała się o brak nazwy zawodu.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

PG = "Podstawy i grzeczność"
LR = "Ludzie i rodzina"
PN = "Praca i nauka"
ST = "Small talk"
ZD = "Zdrowie"
AW = "Awarie i pomoc"
ZP = "Zakupy i pieniądze"
DC = "Dom i codzienność"
TR = "Transport"
HO = "Hotel"
RE = "Restauracja"
MO = "Miejsca i orientacja"
CO = "Cechy i opinie"
PY = "Pytania"

PEOPLE = [

# ============================================================ nák- : zawody
("A2", "sportowiec", "nák kii-laa", "นักกีฬา", "Zawody", 3, "n", ST, "", "człowiek sport"),
("A2", "muzyk", "nák don-trii", "นักดนตรี", "Zawody", 3, "n", ST, "", "człowiek muzyka"),
("A2", "piosenkarz", "nák ráwng", "นักร้อง", "Zawody", 4, "n", ST, "", "człowiek śpiewać"),
("A2", "pisarz", "nák khǐan", "นักเขียน", "Zawody", 3, "n", PN, "", "człowiek pisać"),
("B1", "biznesmen", "nák thú-rá-kìt", "นักธุรกิจ", "Zawody", 3, "n", PN, "", "człowiek interes"),
("B1", "polityk", "nák kaan mueang", "นักการเมือง", "Zawody", 3, "n", PN, "", "człowiek polityka"),
("B1", "naukowiec", "nák wít-thá-yaa-sàat", "นักวิทยาศาสตร์", "Zawody", 2, "n", PN, "", ""),
("B1", "prawnik", "nák kòt mǎai", "นักกฎหมาย", "Zawody", 2, "n", PN, "", "człowiek prawo"),
("B1", "turysta", "nák thâwng thîao", "นักท่องเที่ยว", "Zawody", 4, "n", TR, "", "człowiek podróżować"),
("B1", "pilot", "nák bin", "นักบิน", "Zawody", 3, "n", TR, "", "człowiek latać"),
("B1", "wędkarz", "nák tòk plaa", "นักตกปลา", "Zawody", 2, "n", ST, "", "człowiek łowić ryba"),
("B1", "aktor", "nák sà-daeng", "นักแสดง", "Zawody", 3, "n", ST, "", "człowiek przedstawiać"),
("B1", "tancerz", "nák tên", "นักเต้น", "Zawody", 2, "n", ST, "", ""),
("B1", "inwestor", "nák long thun", "นักลงทุน", "Zawody", 2, "n", ZP, "", ""),
("B1", "badacz", "nák wí-jai", "นักวิจัย", "Zawody", 2, "n", PN, "", ""),

# ============================================================ phûu- : role
("B1", "kierownik", "phûu jàt kaan", "ผู้จัดการ", "Zawody", 4, "n", PN, "", "osoba zarządzać"),
("B1", "dyrektor", "phûu am-nuai kaan", "ผู้อำนวยการ", "Zawody", 2, "n", PN, "", ""),
("B1", "właściciel", "jâo khǎwng", "เจ้าของ", "Zawody", 4, "n", ZP, "", "pan rzeczy"),
("B1", "klient", "lûuk kháa", "ลูกค้า", "Zawody", 4, "n", ZP,
 "Dosłownie „dziecko handlu”. lûuk wchodzi w wiele złożeń o osobach.", "dziecko handel"),
("B1", "pracownik najemny", "phûu ráp jâang", "ผู้รับจ้าง", "Zawody", 2, "n", PN, "", "osoba brać najem"),
("B1", "uczestnik", "phûu khâo rûam", "ผู้เข้าร่วม", "Zawody", 2, "n", PN, "", ""),
("B1", "widz", "phûu chom", "ผู้ชม", "Zawody", 3, "n", ST, "", ""),
("B1", "słuchacz", "phûu fang", "ผู้ฟัง", "Zawody", 2, "n", ST, "", ""),
("B1", "poszkodowany", "phûu sǐa hǎai", "ผู้เสียหาย", "Zawody", 2, "n", AW, "", ""),
("B1", "świadek", "phá-yaan", "พยาน", "Zawody", 2, "n", AW, "", ""),
("B1", "opiekun", "phûu duu lae", "ผู้ดูแล", "Zawody", 3, "n", LR, "", "osoba opiekować się"),
("B1", "przewodniczący", "prà-thaan", "ประธาน", "Zawody", 2, "n", PN, "", ""),
("B1", "przedstawiciel", "tua thaen", "ตัวแทน", "Zawody", 2, "n", PN, "", "ciało zamiast"),
("B1", "wolontariusz", "aa-sǎa sà-màk", "อาสาสมัคร", "Zawody", 2, "n", PN, "", ""),

# ============================================================ châang- : fach
("A2", "elektryk", "châang fai", "ช่างไฟ", "Fachowcy", 3, "n", AW, "", "fachowiec prąd"),
("A2", "hydraulik", "châang prà-pàa", "ช่างประปา", "Fachowcy", 3, "n", AW, "", "fachowiec wodociąg"),
("A2", "mechanik", "châang yon", "ช่างยนต์", "Fachowcy", 3, "n", AW, "", "fachowiec silnik"),
("A2", "stolarz", "châang mái", "ช่างไม้", "Fachowcy", 2, "n", DC, "", "fachowiec drewno"),
("A2", "fryzjer", "châang tàt phǒm", "ช่างตัดผม", "Fachowcy", 3, "n", ZP, "", "fachowiec ciąć włosy"),
("B1", "krawiec", "châang tàt sûea", "ช่างตัดเสื้อ", "Fachowcy", 2, "n", ZP, "", "fachowiec ciąć ubranie"),
("B1", "murarz", "châang pun", "ช่างปูน", "Fachowcy", 2, "n", DC, "", "fachowiec cement"),
("B1", "malarz pokojowy", "châang sǐi", "ช่างสี", "Fachowcy", 2, "n", DC, "", "fachowiec farba"),
("B1", "fotograf", "châang phâap", "ช่างภาพ", "Fachowcy", 3, "n", ST, "", "fachowiec obraz"),
("B1", "technik", "châang thék-nìk", "ช่างเทคนิค", "Fachowcy", 2, "n", AW, "", ""),
("B1", "spawacz", "châang chûeam", "ช่างเชื่อม", "Fachowcy", 2, "n", AW, "", ""),
("B1", "złota rączka", "châang sâwm", "ช่างซ่อม", "Fachowcy", 3, "n", AW, "", "fachowiec naprawiać"),

# ============================================================ khon- : ludzie
("A2", "przechodzień", "khon doen thà-nǒn", "คนเดินถนน", "Ludzie", 2, "n", MO, "", "człowiek iść ulica"),
("A2", "sąsiad", "phûean bâan", "เพื่อนบ้าน", "Ludzie", 4, "n", LR, "", "przyjaciel dom"),
("A2", "gość (w domu)", "khàek", "แขก", "Ludzie", 4, "n", LR,
 "To samo słowo znaczy „gość hotelowy”. Klasyfikator: khon.", ""),
("A2", "tłum", "fǔung chon", "ฝูงชน", "Ludzie", 2, "n", MO, "", ""),
("B1", "obcokrajowiec", "chaao tàang châat", "ชาวต่างชาติ", "Ludzie", 4, "n", ST,
 "Grzeczniejsze niż faràng, którego Tajowie używają swobodnie, ale w ustach cudzoziemca brzmi dziwnie.", "mieszkaniec obcy naród"),
("B1", "mieszkaniec wsi", "chaao bâan", "ชาวบ้าน", "Ludzie", 3, "n", MO, "", "mieszkaniec dom"),
("B1", "rolnik", "chaao naa", "ชาวนา", "Ludzie", 3, "n", PN, "", "mieszkaniec pole ryżowe"),
("B1", "rybak", "chaao prà-mong", "ชาวประมง", "Ludzie", 2, "n", PN, "", ""),
("B1", "cudzoziemiec (urzędowo)", "khon tàang dâao", "คนต่างด้าว", "Ludzie", 2, "n", AW, "", ""),
("B1", "para (dwoje ludzi)", "khûu", "คู่", "Ludzie", 4, "n", LR,
 "Także klasyfikator do rzeczy w parach: butów, pałeczek.", ""),
("B1", "grupa", "klùm", "กลุ่ม", "Ludzie", 4, "n", ST, "", ""),
("B1", "zespół, drużyna", "thiim", "ทีม", "Ludzie", 3, "n", PN, "", ""),
("B1", "społeczeństwo", "sǎng-khom", "สังคม", "Ludzie", 3, "n", PN, "", ""),
("B1", "pokolenie", "rûn", "รุ่น", "Ludzie", 3, "n", LR,
 "Także „model, rocznik” o rzeczach: rót rûn mài — nowy model auta.", ""),

# ============================================================ rodzina
("A1", "krewny", "yâat", "ญาติ", "Rodzina", 3, "n", LR, "", ""),
("A2", "teść (ojciec żony)", "phâw taa", "พ่อตา", "Rodzina", 2, "n", LR,
 "Ojciec męża to phâw phǔa — tajski rozróżnia stronę.", "ojciec dziadek"),
("A2", "zięć", "lûuk khǒei", "ลูกเขย", "Rodzina", 2, "n", LR, "", ""),
("A2", "synowa", "lûuk sà-phái", "ลูกสะใภ้", "Rodzina", 2, "n", LR, "", ""),
("A2", "bliźniak", "fǎa fàet", "ฝาแฝด", "Rodzina", 2, "n", LR, "", ""),
("A2", "wnuk", "lǎan", "หลาน", "Rodzina", 3, "n", LR,
 "To samo słowo znaczy siostrzeniec i bratanek — tajski nie rozróżnia.", ""),
("A2", "przodek", "banphá-bù-rùt", "บรรพบุรุษ", "Rodzina", 2, "n", LR, "", ""),
("A2", "ojciec przybrany", "phâw bun tham", "พ่อบุญธรรม", "Rodzina", 2, "n", LR, "", ""),
("B1", "rodzina wielopokoleniowa", "khrâwp khrua yài", "ครอบครัวใหญ่", "Rodzina", 2, "n", LR, "", ""),
("B1", "narzeczony", "khûu mân", "คู่หมั้น", "Rodzina", 2, "n", LR, "", ""),
("B1", "wdowa", "mâai", "หม้าย", "Rodzina", 2, "n", LR, "", ""),
("B1", "rozwód", "kaan yàa", "การหย่า", "Rodzina", 2, "n", LR, "", ""),
("B1", "wesele", "ngaan tàeng ngaan", "งานแต่งงาน", "Rodzina", 3, "n", LR, "", "impreza ślub"),
("B1", "ciąża", "kaan tâng khan", "การตั้งครรภ์", "Rodzina", 2, "n", ZD, "", ""),
("B1", "niemowlę", "thaa-rók", "ทารก", "Rodzina", 2, "n", LR, "", ""),
("B1", "nastolatek", "wai rûn", "วัยรุ่น", "Rodzina", 3, "n", LR, "", "wiek pokolenie"),
("B1", "emeryt", "khon kà-sǐan", "คนเกษียณ", "Rodzina", 2, "n", LR, "", ""),

# ============================================================ wiek i płeć
("A1", "chłopiec", "dèk chaai", "เด็กชาย", "Wiek", 4, "n", LR, "", "dziecko mężczyzna"),
("A1", "dziewczynka", "dèk yǐng", "เด็กหญิง", "Wiek", 4, "n", LR, "", "dziecko kobieta"),
("A2", "młodzieniec", "khon nùm", "คนหนุ่ม", "Wiek", 3, "n", LR, "", ""),
("A2", "starsza pani", "khun yaai", "คุณยาย", "Wiek", 3, "n", LR,
 "Także zwrot do obcej starszej kobiety — grzeczny i ciepły zarazem.", ""),
("A2", "starszy pan", "khun taa", "คุณตา", "Wiek", 3, "n", LR, "", ""),
("A2", "kolega z pracy", "phûean ruam ngaan", "เพื่อนร่วมงาน", "Wiek", 3, "n", PN, "", "przyjaciel wspólnie praca"),
("A2", "kolega z klasy", "phûean ruam hâwng", "เพื่อนร่วมห้อง", "Wiek", 3, "n", PN, "", "przyjaciel wspólnie pokój"),
("B1", "znajomy", "khon khún khooei", "คนคุ้นเคย", "Wiek", 2, "n", ST, "", ""),
("B1", "człowiek obcy", "khon mâi rúu-jàk", "คนไม่รู้จัก", "Wiek", 3, "n", AW, "", "człowiek nie znać"),

# ============================================================ obsługa, usługi
("A2", "kelner", "phá-nák ngaan sòep", "พนักงานเสิร์ฟ", "Obsługa", 4, "n", RE, "", "pracownik podawać"),
("A2", "kucharz", "phâw khrua", "พ่อครัว", "Obsługa", 3, "n", RE, "", "ojciec kuchnia"),
("A2", "recepcjonista", "phá-nák ngaan tâwn ráp", "พนักงานต้อนรับ", "Obsługa", 3, "n", HO, "", "pracownik witać"),
("A2", "gospodyni, sprzątaczka", "mâe bâan", "แม่บ้าน", "Obsługa", 4, "n", HO,
 "To samo słowo znaczy „gospodyni domowa” — kontekst rozstrzyga.", "matka dom"),
("A2", "ochroniarz", "yaam", "ยาม", "Obsługa", 3, "n", HO,
 "Para minimalna: yaam z tonem średnim to strażnik, yâam to pora dnia.", ""),
("A2", "kasjer", "phá-nák ngaan kèp ngoen", "พนักงานเก็บเงิน", "Obsługa", 3, "n", ZP, "", "pracownik zbierać pieniądze"),
("A2", "kierowca zawodowy", "khon khàp", "คนขับ", "Obsługa", 4, "n", TR, "", ""),
("A2", "konduktor", "khon kèp tǔa", "คนเก็บตั๋ว", "Obsługa", 2, "n", TR, "", "człowiek zbierać bilet"),
("B1", "przewodnik wycieczki", "kái", "ไกด์", "Obsługa", 3, "n", TR, "", ""),
("B1", "masażysta", "mǎw nûat", "หมอนวด", "Obsługa", 3, "n", ZD, "", "specjalista masaż"),
("B1", "pielęgniarka", "phá-yaa-baan", "พยาบาล", "Obsługa", 4, "n", ZD, "", ""),
("B1", "farmaceuta", "phee-sàt chá-kawn", "เภสัชกร", "Obsługa", 2, "n", ZD, "", ""),
("B1", "weterynarz", "sàt-thá-phâet", "สัตวแพทย์", "Obsługa", 2, "n", ZD, "", ""),
("B1", "listonosz", "bù-rùt prai-sà-nii", "บุรุษไปรษณีย์", "Obsługa", 2, "n", MO, "", ""),
("B1", "strażak", "phá-nák ngaan dàp phloeng", "พนักงานดับเพลิง", "Obsługa", 3, "n", AW, "", "pracownik gasić ogień"),
("B1", "ratownik wodny", "jâo nâa thîi chûai chii-wít", "เจ้าหน้าที่ช่วยชีวิต", "Obsługa", 2, "n", AW, "", "urzędnik ratować życie"),
("B1", "urzędnik", "jâo nâa thîi", "เจ้าหน้าที่", "Obsługa", 4, "n", AW,
 "Najczęstsze słowo na każdą osobę „w mundurze albo za biurkiem”.", "pan zadanie"),
("B1", "sprzedawca uliczny", "phâw kháa", "พ่อค้า", "Obsługa", 3, "n", ZP,
 "Sprzedawczyni to mâe kháa — tajski tu rozróżnia płeć.", "ojciec handel"),
("B1", "sprzedawczyni", "mâe kháa", "แม่ค้า", "Obsługa", 3, "n", ZP, "", "matka handel"),
("B1", "ogrodnik", "khon sǔan", "คนสวน", "Obsługa", 2, "n", DC, "", "człowiek ogród"),
("B1", "kierownik zmiany", "hǔa nâa kà", "หัวหน้ากะ", "Obsługa", 2, "n", PN, "", "głowa zmiana"),
("B1", "szef, przełożony", "hǔa nâa", "หัวหน้า", "Obsługa", 4, "n", PN, "", "głowa twarz"),

# ============================================================ cechy ludzi
("A2", "osoba uprzejma", "khon sù-phâap", "คนสุภาพ", "Charakter", 3, "n", CO, "", ""),
("A2", "osoba w dobrym humorze", "khon aa-rom dii", "คนอารมณ์ดี", "Charakter", 3, "n", CO, "", "człowiek nastrój dobry"),
("A2", "osoba nieśmiała", "khon khîi aai", "คนขี้อาย", "Charakter", 3, "n", CO,
 "Przedrostek khîi- tworzy cechy nawykowe: khîi kìat (leniwy), khîi luem (zapominalski).", ""),
("A2", "leń", "khon khîi kìat", "คนขี้เกียจ", "Charakter", 3, "n", CO, "", ""),
("A2", "zapominalski", "khîi luem", "ขี้ลืม", "Charakter", 3, "adj", CO, "", ""),
("A2", "skąpy", "khîi nǐao", "ขี้เหนียว", "Charakter", 3, "adj", CO, "", "lepki"),
("A2", "gadatliwy", "khîi khui", "ขี้คุย", "Charakter", 2, "adj", CO, "", ""),
("A2", "obraźliwy, nadąsany", "khîi ngǒn", "ขี้งอน", "Charakter", 2, "adj", CO, "", ""),
("B1", "pracowity", "khà-yǎn", "ขยัน", "Charakter", 4, "adj", CO,
 "Najczęstsza pochwała w tajskiej szkole i w pracy.", ""),
("B1", "punktualny", "trong wee-laa", "ตรงเวลา", "Charakter", 4, "adj", CO, "", "prosto czas"),
("B1", "niezdecydowany", "lang-lee", "ลังเล", "Charakter", 2, "adj", CO, "", ""),
("B1", "uparty", "dûe", "ดื้อ", "Charakter", 3, "adj", CO,
 "O dzieciach mówi się to codziennie: dèk dûe.", ""),
("B1", "opanowany", "jai yen", "ใจเย็น", "Charakter", 4, "adj", CO,
 "Dosłownie „chłodne serce”. Najczęstsza rada, jaką usłyszysz w Tajlandii.", "serce chłodne"),
("B1", "porywczy", "jai ráwn", "ใจร้อน", "Charakter", 3, "adj", CO, "", "serce gorące"),
("B1", "wielkoduszny", "jai kwâang", "ใจกว้าง", "Charakter", 2, "adj", CO, "", "serce szerokie"),
("B1", "miękkiego serca", "jai àwn", "ใจอ่อน", "Charakter", 2, "adj", CO, "", "serce miękkie"),
("B1", "twardy, nieustępliwy", "jai khǎeng", "ใจแข็ง", "Charakter", 2, "adj", CO, "", "serce twarde"),
("B1", "roztargniony", "jai lawi", "ใจลอย", "Charakter", 2, "adj", CO, "", "serce unosi się"),

# ============================================================ zwroty do ludzi
("A1", "wujku (do starszego mężczyzny)", "lung", "ลุง", "Zwroty", 4, "w", PG,
 "W Tajlandii do obcych mówi się terminami rodzinnymi — to nie poufałość, tylko norma.", "wujek"),
("A1", "ciociu (do starszej kobiety)", "pâa", "ป้า", "Zwroty", 4, "w", PG, "", "ciocia"),
("A1", "myszko (do dziecka)", "nǔu", "หนู", "Zwroty", 3, "w", PG,
 "Tak dorosły zwraca się do dziecka, a dziewczyna do starszych o samej sobie.", "myszka"),
("A2", "starszy bracie, siostro", "phîi", "พี่", "Zwroty", 5, "w", PG,
 "Zwrot obsługujący połowę tajskich rozmów: do kelnera, taksówkarza, sprzedawcy.", ""),
("A2", "młodszy bracie, siostro", "náwng", "น้อง", "Zwroty", 5, "w", PG, "", ""),
("A2", "szanowny panie", "thâan", "ท่าน", "Zwroty", 3, "w", PG,
 "Rejestr urzędowy i świątynny. W barze zabrzmi jak parodia.", ""),

# ============================================================ pytania o ludzi
("A1", "Kim on jest?", "kháo pen khrai khráp", "เขาเป็นใครครับ", "Pytania", 4, "w", PY, "", ""),
("A1", "Czyje to jest?", "khǎwng khrai khráp", "ของใครครับ", "Pytania", 4, "w", PY, "", ""),
("A1", "Z kim?", "kàp khrai khráp", "กับใครครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Dla kogo?", "sǎm-ràp khrai khráp", "สำหรับใครครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Kto to zrobił?", "khrai tham khráp", "ใครทำครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Kogo szukasz?", "hǎa khrai khráp", "หาใครครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Kto następny?", "khrai tàw pai khráp", "ใครต่อไปครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Ile masz lat?", "aa-yú thâo-rài khráp", "อายุเท่าไหร่ครับ", "Pytania", 4, "w", PY,
 "W Tajlandii pytanie neutralne — od wieku zależy dobór zaimków.", ""),
("A2", "Czy jesteś już po ślubie?", "tàeng ngaan rǔe yang khráp", "แต่งงานหรือยังครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Masz dzieci?", "mii lûuk mǎi khráp", "มีลูกไหมครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Kto tu jest szefem?", "khrai pen hǔa nâa khráp", "ใครเป็นหัวหน้าครับ", "Pytania", 2, "w", PY, "", ""),
]
