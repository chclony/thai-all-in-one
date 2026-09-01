# -*- coding: utf-8 -*-
"""Sesja O, partia 16 — ŚWIĄTYNIA, OBYCZAJ, ETYKIETA.

Warstwa, bez której cudzoziemiec w Tajlandii regularnie popełnia gafy nie
z braku dobrej woli, tylko z braku słów. Trzy bloki:

1. **Świątynia i buddyzm** — mnich, jałmużna, zasługa, ofiara, medytacja.
   Wat jest w Tajlandii jednocześnie świątynią, szkołą, domem kultury
   i miejscem pogrzebu; rozmowa o kalendarzu i o rodzinie bez tych słów
   się rozjeżdża.
2. **Etykieta** — wai, zdejmowanie butów, zakaz dotykania głowy, zakaz
   wskazywania stopą. Każde z tych haseł jest zarazem informacją, której
   przewodniki nie tłumaczą wystarczająco dosadnie.
3. **Wierzenia codzienne** — domek duchów przed każdym budynkiem,
   amulety, szczęśliwe kolory dni. To nie egzotyka: to tłumaczy, czemu
   przed biurowcem stoi miniaturowy pałacyk z jedzeniem.

Uwaga o rejestrze: mowa o monarchii i o duchownych ma w tajskim osobny
zestaw słów (`phrá`, `thâan`). Hasła tej partii podają rejestr neutralny
i grzeczny, bez form dworskich, które cudzoziemcowi nie są potrzebne, a
łatwo je źle użyć.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

ST = "Small talk"
PG = "Podstawy i grzeczność"
MO = "Miejsca i orientacja"
LR = "Ludzie i rodzina"
CO = "Cechy i opinie"
CZ = "Czasowniki"
CD = "Czas i daty"
PY = "Pytania"
AW = "Awarie i pomoc"
DC = "Dom i codzienność"
ZP = "Zakupy i pieniądze"

TEMPLE = [

# =========================================================== świątynia
("A1", "mnich", "phrá sǒng", "พระสงฆ์", "Świątynia", 4, "n", ST,
 "Kobieta nie podaje mnichowi rzeczy do ręki — kładzie ją na materiale.", ""),
("A1", "nowicjusz", "nêen", "เณร", "Świątynia", 2, "n", ST, "", ""),
("A1", "opat", "jâo aa-wáat", "เจ้าอาวาส", "Świątynia", 2, "n", ST, "", ""),
("A1", "posąg Buddy", "phrá phút-thá rûup", "พระพุทธรูป", "Świątynia", 4, "n", MO, "", ""),
("A1", "kaplica główna", "bòot", "โบสถ์", "Świątynia", 3, "n", MO, "", ""),
("A1", "stupa", "jee-dii", "เจดีย์", "Świątynia", 3, "n", MO, "", ""),
("A1", "dzwon świątynny", "rá-khang", "ระฆัง", "Świątynia", 2, "n", MO, "", ""),
("A1", "kadzidło", "thûup", "ธูป", "Świątynia", 4, "n", ST, "", ""),
("A1", "świeca", "thian", "เทียน", "Świątynia", 4, "n", ST, "", ""),
("A1", "kwiaty ofiarne", "dàwk mái bu-chaa", "ดอกไม้บูชา", "Świątynia", 3, "n", ST, "", ""),
("A2", "jałmużna poranna", "tàk bàat", "ตักบาตร", "Świątynia", 4, "n", ST,
 "O świcie mnisi obchodzą ulice z miskami. Wkładanie ryżu to codzienny obrzęd, nie atrakcja.", "nabierać miska"),
("A2", "zasługa (religijna)", "bun", "บุญ", "Świątynia", 5, "n", ST,
 "Klucz do tajskiej etyki: tham bun — czynić dobro, gromadzić zasługę.", ""),
("A2", "czynić dobro", "tham bun", "ทำบุญ", "Świątynia", 5, "v", CZ, "", "robić zasługę"),
("A2", "grzech, zły uczynek", "bàap", "บาป", "Świątynia", 3, "n", ST, "", ""),
("A2", "medytacja", "nâng sà-maa-thí", "นั่งสมาธิ", "Świątynia", 3, "n", ST, "", "siedzieć skupienie"),
("A2", "modlić się", "sùat mon", "สวดมนต์", "Świątynia", 3, "v", CZ, "", ""),
("A2", "składać ofiarę", "bu-chaa", "บูชา", "Świątynia", 3, "v", CZ, "", ""),
("A2", "wyświęcić się na mnicha", "bùat", "บวช", "Świątynia", 3, "v", CZ,
 "Tradycyjnie każdy Taj spędza w klasztorze przynajmniej kilka tygodni.", ""),
("A2", "wielki post buddyjski", "khâo phan-sǎa", "เข้าพรรษา", "Świątynia", 3, "n", CD,
 "Trzy miesiące pory deszczowej. Część Tajów rezygnuje wtedy z alkoholu.", ""),
("A2", "wróżba, przepowiednia", "duu duang", "ดูดวง", "Świątynia", 3, "n", ST, "", "patrzeć gwiazda"),
("A2", "amulet", "phrá khrûeang", "พระเครื่อง", "Świątynia", 3, "n", ST,
 "Noszony na szyi, kupowany i wymieniany jak kolekcjonerskie monety.", ""),
("A2", "domek duchów", "sǎan phrá phuum", "ศาลพระภูมิ", "Świątynia", 4, "n", DC,
 "Stoi przed każdym domem i biurowcem. Codziennie dostaje jedzenie i napój.", ""),
("A2", "duch", "phǐi", "ผี", "Świątynia", 4, "n", ST, "", ""),
("A2", "szczęście, pomyślność", "chôok", "โชค", "Świątynia", 4, "n", ST, "", ""),
("A2", "pech", "chôok ráai", "โชคร้าย", "Świątynia", 3, "n", ST, "", "szczęście złe"),
("A2", "los, przeznaczenie", "chôok chá-taa", "โชคชะตา", "Świątynia", 2, "n", ST, "", ""),

# =========================================================== etykieta
("A1", "pokłon powitalny", "wâi", "ไหว้", "Etykieta", 5, "n", PG,
 "Złożone dłonie. Niższy kłania się pierwszy, wyższy odpowiada. Do obsługi się nie wai.", ""),
("A1", "zdjąć buty", "thàwt rawng tháo", "ถอดรองเท้า", "Etykieta", 5, "v", CZ,
 "Przed wejściem do domu, świątyni, wielu sklepów i gabinetów. Bezwzględnie.", ""),
("A1", "głowa (jako część święta)", "sǐi-sà", "ศีรษะ", "Etykieta", 3, "n", PG,
 "Najwyższa i najświętsza część ciała — nie dotyka się cudzej głowy, także dziecka.", ""),
("A1", "stopa (jako część nieczysta)", "tháo", "เท้า", "Etykieta", 4, "n", PG,
 "Najniższa część ciała. Nie wskazuje się stopą i nie kładzie jej na stole ani na poduszce.", ""),
("A2", "okazywać szacunek", "hâi khwaam khao-rôp", "ให้ความเคารพ", "Etykieta", 3, "v", CZ, "", ""),
("A2", "zachowywać się grzecznie", "tham tua sù-phâap", "ทำตัวสุภาพ", "Etykieta", 3, "v", CZ, "", ""),
("A2", "podnosić głos", "sǐang dang", "เสียงดัง", "Etykieta", 4, "adj", CO,
 "W Tajlandii poważny nietakt. Głośna kłótnia to utrata twarzy dla obu stron.", "głos głośny"),
("A2", "zachować spokój", "khûap khum aa-rom", "ควบคุมอารมณ์", "Etykieta", 3, "v", CZ, "", ""),
("A2", "kolejka (ustawić się)", "tàw khiu", "ต่อคิว", "Etykieta", 4, "v", CZ, "", ""),
("A2", "wpychać się bez kolejki", "lát khiu", "ลัดคิว", "Etykieta", 3, "v", CZ, "", ""),
("A2", "ubrać się odpowiednio", "tàeng kaai hâi rîap ráwi", "แต่งกายให้เรียบร้อย", "Etykieta", 3, "v", CZ,
 "Do świątyni: zakryte ramiona i kolana. Bez wyjątków dla turystów.", ""),
("A2", "nie wolno", "hâam", "ห้าม", "Etykieta", 5, "v", PG,
 "Na każdej tabliczce zakazu: hâam sùup bù-rìi, hâam jàwt.", ""),
("A2", "wolno, dozwolone", "à-nú-yâat", "อนุญาต", "Etykieta", 4, "v", PG, "", ""),
("A2", "zwyczaj, obyczaj", "prà-phee-nii", "ประเพณี", "Etykieta", 4, "n", ST, "", ""),
("A2", "tradycja", "wát-thá-ná-tham", "วัฒนธรรม", "Etykieta", 4, "n", ST, "", ""),
("A2", "nietakt, coś niestosownego", "mâi mà-sǒm", "ไม่เหมาะสม", "Etykieta", 3, "adj", CO, "", ""),
("A2", "wypada, uchodzi", "mà-sǒm", "เหมาะสม", "Etykieta", 3, "adj", CO, "", ""),

# =========================================================== relacje i hierarchia
("A1", "starszeństwo", "aa-wú-sǒo", "อาวุโส", "Relacje", 2, "n", LR, "", ""),
("A2", "osoba wyżej postawiona", "phûu yài kwàa", "ผู้ใหญ่กว่า", "Relacje", 3, "n", LR, "", ""),
("A2", "podwładny", "lûuk náwng", "ลูกน้อง", "Relacje", 3, "n", LR, "", "dziecko młodsze"),
("A2", "znajomość, kontakty", "sên sǎai", "เส้นสาย", "Relacje", 2, "n", LR,
 "„Mieć plecy”. W wielu sprawach urzędowych działa szybciej niż procedura.", "linia sznur"),
("A2", "przysługa", "bun khun", "บุญคุณ", "Relacje", 3, "n", LR,
 "Dług wdzięczności, którego nie spłaca się pieniędzmi. Filar relacji rodzinnych.", "zasługa dobroć"),
("A2", "odwdzięczyć się", "tàwp thaen", "ตอบแทน", "Relacje", 3, "v", CZ, "", ""),
("A2", "być zobowiązanym", "tìt bun khun", "ติดบุญคุณ", "Relacje", 2, "v", CZ, "", ""),
("A2", "zaufany człowiek", "khon thîi wái jai dâi", "คนที่ไว้ใจได้", "Relacje", 3, "n", LR, "", ""),
("A2", "unikać konfliktu", "lìik lîang khwaam khàt yáeng", "หลีกเลี่ยงความขัดแย้ง", "Relacje", 2, "v", CZ, "", ""),
("A2", "iść na kompromis", "prà-nii prà-nawm", "ประนีประนอม", "Relacje", 2, "v", CZ, "", ""),
("A2", "być w porządku wobec kogoś", "tham dii dûai", "ทำดีด้วย", "Relacje", 3, "v", CZ, "", ""),

# =========================================================== dni i kolory
("A2", "kolor dnia tygodnia", "sǐi prà-jam wan", "สีประจำวัน", "Kolory dni", 2, "n", ST,
 "Każdy dzień ma kolor: poniedziałek żółty, wtorek różowy. Stąd żółte koszule w poniedziałki.", ""),
("A2", "szczęśliwy numer", "lêek mongkhon", "เลขมงคล", "Kolory dni", 3, "n", ST,
 "Dziewiątka jest szczęśliwa (kâo brzmi jak „iść naprzód”), tabliczki z dziewiątkami kosztują więcej.", ""),
("A2", "pechowy numer", "lêek mâi dii", "เลขไม่ดี", "Kolory dni", 2, "n", ST, "", ""),
("A2", "loteria", "lâwt-tá-rîi", "ลอตเตอรี่", "Kolory dni", 4, "n", ZP,
 "Losowanie dwa razy w miesiącu. Numery wybiera się z wróżb i snów.", ""),
("A2", "wróżyć ze snu", "tii khwaam fǎn", "ตีความฝัน", "Kolory dni", 2, "v", CZ, "", ""),
("A2", "przesąd", "khwaam chûea", "ความเชื่อ", "Kolory dni", 3, "n", ST, "", ""),

# =========================================================== życie i śmierć
("A2", "narodziny", "kaan kòoet", "การเกิด", "Życie", 3, "n", LR, "", ""),
("A2", "śmierć", "khwaam taai", "ความตาย", "Życie", 3, "n", LR, "", ""),
("A2", "kremacja", "kaan phǎo sòp", "การเผาศพ", "Życie", 2, "n", LR, "", "palenie ciała"),
("A2", "kondolencje", "sǎ-daeng khwaam sǐa jai", "แสดงความเสียใจ", "Życie", 3, "n", PG, "", ""),
("A2", "reinkarnacja", "kaan kòoet mài", "การเกิดใหม่", "Życie", 2, "n", ST, "", "narodzić się na nowo"),
("A2", "karma, skutek uczynków", "kam", "กรรม", "Życie", 3, "n", ST,
 "W mowie potocznej wykrzyknik rezygnacji: „kam khǎwng phǒm” — taki mój los.", ""),
("A2", "cierpienie", "khwaam thúk", "ความทุกข์", "Życie", 3, "n", ST, "", ""),
("A2", "spokój ducha", "khwaam sà-ngòp jai", "ความสงบใจ", "Życie", 2, "n", ST, "", ""),

# =========================================================== pytania i zwroty
("A1", "Czy mogę tu wejść?", "khâo pai dâi mǎi khráp", "เข้าไปได้ไหมครับ", "Zwroty", 5, "w", PY, "", ""),
("A1", "Czy można robić zdjęcia?", "thàai rûup dâi mǎi khráp", "ถ่ายรูปได้ไหมครับ", "Zwroty", 5, "w", PY, "", ""),
("A1", "Czy trzeba zdjąć buty?", "tâwng thàwt rawng tháo mǎi khráp", "ต้องถอดรองเท้าไหมครับ", "Zwroty", 4, "w", PY, "", ""),
("A2", "Przepraszam, nie wiedziałem.", "khǎw thôot khráp phǒm mâi rúu", "ขอโทษครับผมไม่รู้", "Zwroty", 5, "w", PG, "", ""),
("A2", "Czy tak wypada?", "yàang níi mà-sǒm mǎi khráp", "อย่างนี้เหมาะสมไหมครับ", "Zwroty", 3, "w", PY, "", ""),
("A2", "Jak należy się zachować?", "khuan tham tua yang ngai khráp", "ควรทำตัวยังไงครับ", "Zwroty", 3, "w", PY, "", ""),
("A2", "Czy to jest święte miejsce?", "thîi níi pen thîi sàk-sìt mǎi khráp", "ที่นี่เป็นที่ศักดิ์สิทธิ์ไหมครับ", "Zwroty", 2, "w", PY, "", ""),
("A2", "Z całym szacunkiem.", "dûai khwaam khao-rôp khráp", "ด้วยความเคารพครับ", "Zwroty", 3, "w", PG, "", ""),
("A2", "Niech ci się darzy.", "khǎw hâi chôok dii khráp", "ขอให้โชคดีครับ", "Zwroty", 5, "w", PG, "", ""),
("A2", "Życzę zdrowia.", "khǎw hâi sùk-khà-phâap khǎeng raeng khráp", "ขอให้สุขภาพแข็งแรงครับ", "Zwroty", 4, "w", PG, "", ""),
("A2", "Dziękuję za wszystko.", "khàwp khun sǎm-ràp thúk yàang khráp", "ขอบคุณสำหรับทุกอย่างครับ", "Zwroty", 4, "w", PG, "", ""),
("A2", "To dla mnie zaszczyt.", "pen kìat khráp", "เป็นเกียรติครับ", "Zwroty", 2, "w", PG, "", ""),
]
