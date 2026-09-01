# -*- coding: utf-8 -*-
"""Sesja O, partia 1 — NOMINALIZACJE `kaan-` i `khwaam-`.

Dwa najbardziej produktywne przedrostki tajszczyzny. `kaan-` przed
czasownikiem daje nazwę czynności („kaan doen thaang” — podróżowanie),
`khwaam-` przed przymiotnikiem lub czasownikiem stanu daje rzeczownik
abstrakcyjny („khwaam ngîap” — cisza).

Dlaczego akurat one otwierają tę sesję: obie konstrukcje budują się
**z sylab, które uczący się już zna**. Baza ma `doen thaang` i `ngîap` od
poziomu A1; `kaan` i `khwaam` też. Nowe hasło nie wnosi więc żadnej nowej
sylaby i ścieżka może je wprowadzić w najbliższej lekcji, zamiast czekać,
aż z innego materiału dojdą brakujące cegiełki. To była dokładnie ta blokada,
o którą rozbiła się sesja N (1 821 haseł aktywowalnych, 1 164 wprowadzone).

Warstwa jest przy tym potrzebna sama w sobie: bez rzeczowników
abstrakcyjnych nie da się prowadzić rozmowy o czymkolwiek poza tym, co leży
na stole. „Rozumiem obsługę sytuacji” kontra „rozumiem, o czym mówią”.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

PG = "Podstawy i grzeczność"
LI = "Liczby i liczenie"
JN = "Jedzenie i napoje"
RE = "Restauracja"
TR = "Transport"
MO = "Miejsca i orientacja"
ZP = "Zakupy i pieniądze"
CZ = "Czasowniki"
HO = "Hotel"
PY = "Pytania"
CD = "Czas i daty"
CO = "Cechy i opinie"
ZD = "Zdrowie"
LR = "Ludzie i rodzina"
DC = "Dom i codzienność"
ST = "Small talk"
AW = "Awarie i pomoc"
PP = "Pogoda i przyroda"
PN = "Praca i nauka"
GU = "Gramatyka użytkowa"

KAAN = [

# ======================================================= kaan- : ruch, podróż
("A2", "podróżowanie", "kaan doen thaang", "การเดินทาง", "Czynności", 4, "n", TR,
 "Nazwa czynności, nie wycieczki. Wycieczka to thua albo kaan thâwng thîao.", "czynność iść droga"),
("A2", "przeprowadzka", "kaan yáai bâan", "การย้ายบ้าน", "Czynności", 3, "n", DC,
 "", "czynność przenieść dom"),
("A2", "przyjazd, przylot", "kaan maa thǔeng", "การมาถึง", "Czynności", 3, "n", TR,
 "Na tablicach lotniska obok słowa khǎa khâo.", "czynność przyjść dotrzeć"),
("A2", "wyjazd, odlot", "kaan àwk doen thaang", "การออกเดินทาง", "Czynności", 3, "n", TR, "", ""),
("A2", "prowadzenie samochodu", "kaan khàp rót", "การขับรถ", "Czynności", 3, "n", TR, "", ""),
("B1", "parkowanie", "kaan jàwt rót", "การจอดรถ", "Czynności", 3, "n", TR, "", ""),
("B1", "przesiadka", "kaan plìan rót", "การเปลี่ยนรถ", "Czynności", 3, "n", TR,
 "O pociągu i autobusie. O samolocie mówi się plìan khrûeang.", "czynność zmienić pojazd"),
("A2", "spacer", "kaan doen lên", "การเดินเล่น", "Czynności", 3, "n", ST, "", "czynność iść dla zabawy"),
("B1", "zwiedzanie", "kaan chom", "การชม", "Czynności", 3, "n", TR, "", ""),
("B1", "bieganie", "kaan wîng", "การวิ่ง", "Czynności", 3, "n", ST, "", ""),
("B1", "pływanie", "kaan wâai nám", "การว่ายน้ำ", "Czynności", 3, "n", ST, "", ""),
("B1", "wspinaczka", "kaan piin", "การปีน", "Czynności", 2, "n", PP, "", ""),

# ======================================================= kaan- : jedzenie, dom
("A2", "gotowanie", "kaan tham aa-hǎan", "การทำอาหาร", "Czynności", 4, "n", JN, "", "czynność robić jedzenie"),
("A2", "jedzenie (czynność)", "kaan kin", "การกิน", "Czynności", 4, "n", JN,
 "Uwaga: aa-hǎan to jedzenie jako rzecz, kaan kin to sama czynność.", ""),
("B1", "zamawianie", "kaan sàng", "การสั่ง", "Czynności", 3, "n", RE, "", ""),
("B1", "podawanie do stołu", "kaan sòep", "การเสิร์ฟ", "Czynności", 2, "n", RE, "", ""),
("A2", "sprzątanie", "kaan tham khwaam sà-àat", "การทำความสะอาด", "Czynności", 4, "n", DC,
 "Trzy człony, ale w mowie to jeden blok — warto go ćwiczyć w całości.", "czynność robić czystość"),
("A2", "pranie", "kaan sák phâa", "การซักผ้า", "Czynności", 3, "n", DC, "", ""),
("A2", "zmywanie", "kaan láang jaan", "การล้างจาน", "Czynności", 3, "n", DC, "", ""),
("B1", "naprawa", "kaan sâwm", "การซ่อม", "Czynności", 3, "n", AW, "", ""),
("B1", "remont", "kaan sâwm bâan", "การซ่อมบ้าน", "Czynności", 2, "n", DC, "", ""),
("B1", "budowa", "kaan kàw sâang", "การก่อสร้าง", "Czynności", 3, "n", PN, "", ""),
("B1", "przechowywanie", "kaan kèp", "การเก็บ", "Czynności", 2, "n", DC, "", ""),

# ======================================================= kaan- : pieniądze
("A2", "płacenie", "kaan jàai ngoen", "การจ่ายเงิน", "Pieniądze", 4, "n", ZP, "", ""),
("B1", "oszczędzanie", "kaan àwm", "การออม", "Pieniądze", 3, "n", ZP, "", ""),
("B1", "pożyczanie", "kaan yuem", "การยืม", "Pieniądze", 3, "n", ZP,
 "yuem to pożyczyć od kogoś, hâi yuem to pożyczyć komuś.", ""),
("B1", "sprzedaż", "kaan khǎai", "การขาย", "Pieniądze", 3, "n", ZP, "", ""),
("B1", "zakup", "kaan súe", "การซื้อ", "Pieniądze", 3, "n", ZP, "", ""),
("B1", "wymiana pieniędzy", "kaan lâek ngoen", "การแลกเงิน", "Pieniądze", 3, "n", ZP, "", ""),
("B1", "zwrot pieniędzy", "kaan khuen ngoen", "การคืนเงิน", "Pieniądze", 3, "n", ZP, "", ""),
("B1", "targowanie się", "kaan tàw raa-khaa", "การต่อราคา", "Pieniądze", 3, "n", ZP, "", "czynność ciągnąć cenę"),
("B1", "dostawa", "kaan sòng", "การส่ง", "Pieniądze", 3, "n", ZP, "", ""),
("B1", "zamówienie online", "kaan sàng awn-lai", "การสั่งออนไลน์", "Pieniądze", 3, "n", ZP, "", ""),

# ======================================================= kaan- : praca, nauka
("A2", "praca (czynność)", "kaan tham ngaan", "การทำงาน", "Praca", 4, "n", PN,
 "ngaan to praca jako rzecz albo impreza; kaan tham ngaan to sama czynność.", ""),
("A2", "uczenie się", "kaan rian", "การเรียน", "Nauka", 4, "n", PN, "", ""),
("B1", "nauczanie", "kaan sǎwn", "การสอน", "Nauka", 3, "n", PN, "", ""),
("B1", "czytanie", "kaan àan", "การอ่าน", "Nauka", 3, "n", PN, "", ""),
("B1", "pisanie", "kaan khǐan", "การเขียน", "Nauka", 3, "n", PN, "", ""),
("B1", "liczenie", "kaan náp", "การนับ", "Nauka", 3, "n", LI, "", ""),
("B1", "obliczenie", "kaan khít lêek", "การคิดเลข", "Nauka", 3, "n", LI, "", "czynność myśleć liczba"),
("B1", "spotkanie (zebranie)", "kaan prà-chum", "การประชุม", "Praca", 3, "n", PN, "", ""),
("B1", "rozmowa kwalifikacyjna", "kaan sǎm-phâat", "การสัมภาษณ์", "Praca", 3, "n", PN, "", ""),
("B1", "szkolenie", "kaan òp rom", "การอบรม", "Praca", 3, "n", PN, "", ""),
("B1", "planowanie", "kaan waang phǎen", "การวางแผน", "Praca", 3, "n", PN, "", "czynność kłaść plan"),
("B1", "decyzja (podejmowanie)", "kaan tàt sǐn jai", "การตัดสินใจ", "Praca", 3, "n", PN, "", "czynność ciąć osądzić serce"),

# ======================================================= kaan- : zdrowie
("A2", "leczenie", "kaan rák-sǎa", "การรักษา", "Leczenie", 3, "n", ZD, "", ""),
("B1", "operacja", "kaan phàa tàt", "การผ่าตัด", "Leczenie", 3, "n", ZD, "", "czynność rozciąć uciąć"),
("B1", "badanie (medyczne)", "kaan trùat sùk-khá-phâap", "การตรวจสุขภาพ", "Leczenie", 3, "n", ZD, "", ""),
("B1", "szczepienie", "kaan chìit wák-siin", "การฉีดวัคซีน", "Leczenie", 3, "n", ZD, "", "czynność wstrzyknąć szczepionka"),
("B1", "odpoczynek", "kaan phák phàwn", "การพักผ่อน", "Leczenie", 3, "n", ZD, "", ""),
("B1", "ćwiczenie fizyczne", "kaan àwk kam-lang kaai", "การออกกำลังกาย", "Leczenie", 4, "n", ZD, "", "czynność wydać siła ciało"),
("B1", "dieta", "kaan khûap khum aa-hǎan", "การควบคุมอาหาร", "Leczenie", 2, "n", ZD, "", ""),
("B1", "pierwsza pomoc", "kaan pà-thǒm phá-yaa-baan", "การปฐมพยาบาล", "Leczenie", 3, "n", AW, "", "czynność pierwszy opieka"),

# ======================================================= kaan- : sprawy, urzędy
("B1", "rezerwacja", "kaan jawng", "การจอง", "Formalności", 4, "n", HO, "", ""),
("B1", "zameldowanie", "kaan chék-ín", "การเช็คอิน", "Formalności", 3, "n", HO, "", ""),
("B1", "wymeldowanie", "kaan chék-áo", "การเช็คเอาท์", "Formalności", 3, "n", HO, "", ""),
("B1", "sprzątanie pokoju", "kaan tham hâwng", "การทำห้อง", "Formalności", 2, "n", HO, "", ""),
("B1", "zgłoszenie", "kaan jâeng", "การแจ้ง", "Formalności", 3, "n", AW, "", ""),
("B1", "zgłoszenie na policję", "kaan jâeng khwaam", "การแจ้งความ", "Formalności", 3, "n", AW,
 "Zwrot obowiązkowy przy kradzieży — bez niego ubezpieczenie nie zadziała.", "czynność zgłosić sprawa"),
("B1", "wniosek, podanie", "kaan yûen khǎw", "การยื่นขอ", "Formalności", 3, "n", PN, "", "czynność podać prosić"),
("B1", "przedłużenie wizy", "kaan tàw wii-sâa", "การต่อวีซ่า", "Formalności", 3, "n", AW, "", ""),
("B1", "kontrola dokumentów", "kaan trùat èek-kà-sǎan", "การตรวจเอกสาร", "Formalności", 2, "n", AW, "", ""),
("B1", "ubezpieczenie (wykupienie)", "kaan tham prà-kan", "การทำประกัน", "Formalności", 3, "n", AW, "", ""),

# ======================================================= kaan- : komunikacja
("A2", "rozmowa", "kaan phûut khui", "การพูดคุย", "Rozmowa", 4, "n", ST, "", ""),
("B1", "tłumaczenie (czynność)", "kaan plae phaa-sǎa", "การแปลภาษา", "Rozmowa", 3, "n", ST, "", ""),
("B1", "wyjaśnianie", "kaan à-thí-baai", "การอธิบาย", "Rozmowa", 3, "n", ST, "", ""),
("B1", "pytanie (czynność)", "kaan thǎam", "การถาม", "Rozmowa", 3, "n", PY, "", ""),
("B1", "odpowiadanie", "kaan tàwp", "การตอบ", "Rozmowa", 3, "n", PY, "", ""),
("B1", "słuchanie", "kaan fang", "การฟัง", "Rozmowa", 3, "n", ST, "", ""),
("B1", "narzekanie", "kaan bòn", "การบ่น", "Rozmowa", 3, "n", ST, "", ""),
("B1", "przeprosiny", "kaan khǎw thôot", "การขอโทษ", "Rozmowa", 3, "n", PG, "", ""),
("B1", "podziękowanie", "kaan khàwp khun", "การขอบคุณ", "Rozmowa", 3, "n", PG, "", ""),
("B1", "powitanie", "kaan thák thaai", "การทักทาย", "Rozmowa", 3, "n", PG, "", ""),
("B1", "pożegnanie", "kaan laa", "การลา", "Rozmowa", 3, "n", PG, "", ""),
("B1", "przedstawianie się", "kaan náe-nam tua", "การแนะนำตัว", "Rozmowa", 3, "n", PG, "", "czynność polecić ciało"),
("B1", "zaproszenie", "kaan chuan", "การชวน", "Rozmowa", 3, "n", ST, "", ""),
("B1", "obietnica", "kaan sǎn-yaa", "การสัญญา", "Rozmowa", 3, "n", ST, "", ""),

# ======================================================= kaan- : czas, pogoda
("B1", "czekanie", "kaan raw", "การรอ", "Czas", 3, "n", CD, "", ""),
("B1", "spóźnienie", "kaan maa sǎai", "การมาสาย", "Czas", 3, "n", CD, "", ""),
("B1", "opóźnienie", "kaan lâa cháa", "การล่าช้า", "Czas", 3, "n", TR, "", ""),
("B1", "zmiana pogody", "kaan plìan aa-kàat", "การเปลี่ยนอากาศ", "Pogoda", 2, "n", PP, "", ""),
("B1", "prognoza pogody", "kaan phá-yaa-kawn aa-kàat", "การพยากรณ์อากาศ", "Pogoda", 3, "n", PP, "", ""),
("B1", "ochrona przyrody", "kaan à-nú-rák thammá-châat", "การอนุรักษ์ธรรมชาติ", "Pogoda", 2, "n", PP, "", ""),
("B1", "segregacja śmieci", "kaan yâek khà-yà", "การแยกขยะ", "Pogoda", 2, "n", DC, "", "czynność oddzielić śmieci"),

# ======================================================= khwaam- : cechy
("A2", "cisza", "khwaam ngîap", "ความเงียบ", "Stany", 3, "n", CO, "", ""),
("A2", "czystość", "khwaam sà-àat", "ความสะอาด", "Stany", 3, "n", DC, "", ""),
("A2", "szybkość", "khwaam reo", "ความเร็ว", "Stany", 4, "n", TR,
 "Na znakach drogowych jam-kàt khwaam reo — ograniczenie prędkości.", ""),
("A2", "wolne tempo", "khwaam cháa", "ความช้า", "Stany", 2, "n", CO, "", ""),
("A2", "zimno (rzecz.)", "khwaam nǎao", "ความหนาว", "Stany", 3, "n", PP, "", ""),
("A2", "wilgoć", "khwaam chúen", "ความชื้น", "Stany", 3, "n", PP,
 "Uwaga na parę minimalną: khwaam chúen to wilgoć, khwaam chûen to radość.", ""),
("A2", "suchość", "khwaam hâeng", "ความแห้ง", "Stany", 2, "n", PP, "", ""),
("B1", "ciężar (właściwość)", "khwaam nàk", "ความหนัก", "Stany", 2, "n", CO, "", ""),
("B1", "lekkość", "khwaam bao", "ความเบา", "Stany", 2, "n", CO, "", ""),
("B1", "twardość", "khwaam khǎeng", "ความแข็ง", "Stany", 2, "n", CO, "", ""),
("B1", "miękkość", "khwaam nûm", "ความนุ่ม", "Stany", 2, "n", CO, "", ""),
("B1", "jasność", "khwaam sà-wàang", "ความสว่าง", "Stany", 2, "n", CO, "", ""),
("B1", "ciemność", "khwaam mûet", "ความมืด", "Stany", 2, "n", CO, "", ""),
("B1", "gęstość", "khwaam nǎa", "ความหนา", "Stany", 2, "n", CO, "", ""),
("B1", "świeżość", "khwaam sòt", "ความสด", "Stany", 2, "n", JN, "", ""),

# ======================================================= khwaam- : uczucia
("A2", "spokój", "khwaam sà-ngòp", "ความสงบ", "Uczucia", 3, "n", ST, "", ""),
("A2", "zmęczenie", "khwaam nùeai", "ความเหนื่อย", "Uczucia", 3, "n", ZD, "", ""),
("A2", "głód", "khwaam hǐu", "ความหิว", "Uczucia", 3, "n", JN, "", ""),
("B1", "pragnienie (chęć picia)", "khwaam hǐu nám", "ความหิวน้ำ", "Uczucia", 2, "n", JN, "", ""),
("B1", "senność", "khwaam ngûang", "ความง่วง", "Uczucia", 3, "n", ZD, "", ""),
("B1", "nuda", "khwaam bùea", "ความเบื่อ", "Uczucia", 3, "n", ST, "", ""),
("B1", "samotność", "khwaam ngǎo", "ความเหงา", "Uczucia", 3, "n", ST, "", ""),
("B1", "tęsknota", "khwaam khít thǔeng bâan", "ความคิดถึงบ้าน", "Uczucia", 2, "n", ST, "", "myślenie o domu"),
("B1", "zdziwienie", "khwaam plàek jai", "ความแปลกใจ", "Uczucia", 2, "n", ST, "", "dziwne serce"),
("B1", "ciekawość", "khwaam yàak rúu", "ความอยากรู้", "Uczucia", 3, "n", ST, "", "chcieć wiedzieć"),
("B1", "cierpliwość", "khwaam òt thon dâi", "ความอดทนได้", "Uczucia", 2, "n", CO, "", ""),
("B1", "odwaga", "khwaam klâa", "ความกล้า", "Uczucia", 3, "n", CO, "", ""),
("B1", "wstyd (uczucie)", "khwaam khǎai nâa", "ความขายหน้า", "Uczucia", 2, "n", ST, "", "sprzedać twarz"),
("B1", "zazdrość (o osobę)", "khwaam hǔeng", "ความหึง", "Uczucia", 2, "n", LR, "", ""),
("B1", "ulga", "khwaam bao jai", "ความเบาใจ", "Uczucia", 2, "n", ST, "", "lekkie serce"),
("B1", "zaufanie", "khwaam wái jai", "ความไว้ใจ", "Uczucia", 3, "n", LR, "", "powierzyć serce"),

# ======================================================= khwaam- : życie, ludzie
("B1", "przyjaźń", "khwaam pen phûean", "ความเป็นเพื่อน", "Relacje", 3, "n", LR, "", "bycie przyjacielem"),
("B1", "miłość rodzicielska", "khwaam rák khǎwng phâw mâe", "ความรักของพ่อแม่", "Relacje", 2, "n", LR, "", ""),
("B1", "bliskość", "khwaam klâi chít", "ความใกล้ชิด", "Relacje", 2, "n", LR, "", ""),
("B1", "szacunek", "khwaam khao-rôp", "ความเคารพ", "Relacje", 3, "n", PG, "", ""),
("B1", "grzeczność", "khwaam sù-phâap", "ความสุภาพ", "Relacje", 3, "n", PG, "", ""),
("B1", "uczciwość", "khwaam sûe sàt", "ความซื่อสัตย์", "Relacje", 3, "n", CO, "", ""),
("B1", "życzliwość", "khwaam jai dii", "ความใจดี", "Relacje", 3, "n", CO, "", "dobre serce"),
("B1", "hojność", "khwaam jai kwâang", "ความใจกว้าง", "Relacje", 2, "n", CO, "", "szerokie serce"),
("B1", "zdolność, umiejętność", "khwaam sǎa-mâat", "ความสามารถ", "Relacje", 3, "n", PN, "", ""),
("B1", "doświadczenie", "khwaam chîao chaan", "ความเชี่ยวชาญ", "Relacje", 2, "n", PN, "", ""),
("B1", "gotowość", "khwaam phráwm", "ความพร้อม", "Relacje", 3, "n", PN, "", ""),
("B1", "potrzeba", "khwaam tâwng kaan", "ความต้องการ", "Relacje", 3, "n", ZP, "", ""),

# ======================================================= khwaam- : sprawy trudne
("B1", "trudność", "khwaam yâak", "ความยาก", "Problemy", 3, "n", AW, "", ""),
("B1", "łatwość", "khwaam ngâai", "ความง่าย", "Problemy", 2, "n", CO, "", ""),
("B1", "niebezpieczeństwo", "khwaam an-tà-raai", "ความอันตราย", "Problemy", 4, "n", AW, "", ""),
("B1", "bezpieczeństwo", "khwaam plàwt phai", "ความปลอดภัย", "Problemy", 4, "n", AW, "", "wolny od zagrożenia"),
("B1", "pomyłka, błąd", "khwaam phìt phlâat", "ความผิดพลาด", "Problemy", 3, "n", AW, "", ""),
("B1", "wina", "khwaam phìt", "ความผิด", "Problemy", 3, "n", AW,
 "„To moja wina” to pen khwaam phìt khǎwng phǒm.", ""),
("B1", "szkoda, strata", "khwaam sǐa hǎai", "ความเสียหาย", "Problemy", 3, "n", AW, "", ""),
("B1", "hałas", "khwaam dang", "ความดัง", "Problemy", 3, "n", AW, "", ""),
("B1", "brud", "khwaam sòk-kà-pròk", "ความสกปรก", "Problemy", 2, "n", DC, "", ""),
("B1", "nieporozumienie", "khwaam khâo jai phìt", "ความเข้าใจผิด", "Problemy", 3, "n", ST, "", "zrozumieć źle"),
("B1", "opóźnienie (stan)", "khwaam lâa cháa", "ความล่าช้า", "Problemy", 2, "n", TR, "", ""),
("B1", "zmiana (stan)", "khwaam plìan", "ความเปลี่ยน", "Problemy", 2, "n", GU, "", ""),

# ======================================================= khwaam- : miary
("B1", "długość", "khwaam yaao khǎwng thaang", "ความยาวของทาง", "Miary", 2, "n", LI, "", "długość drogi"),
("B1", "szerokość (wymiar)", "khwaam kwâang khǎwng hâwng", "ความกว้างของห้อง", "Miary", 2, "n", LI, "", ""),
("B1", "wysokość (wymiar)", "khwaam sǔung khǎwng tùek", "ความสูงของตึก", "Miary", 2, "n", LI, "", ""),
("B1", "odległość", "rá-yá thaang", "ระยะทาง", "Miary", 4, "n", LI, "", "odcinek droga"),
("B1", "powierzchnia", "phúen thîi", "พื้นที่", "Miary", 3, "n", LI, "", "podłoga miejsce"),
("B1", "objętość", "prì-mâat", "ปริมาตร", "Miary", 2, "n", LI, "", ""),
("B1", "ilość", "prì-maan", "ปริมาณ", "Miary", 3, "n", LI, "", ""),
("B1", "poziom, stopień", "rá-dàp", "ระดับ", "Miary", 3, "n", LI, "", ""),
("B1", "średnia", "chà-lìa", "เฉลี่ย", "Miary", 3, "n", LI, "", ""),
("B1", "suma, razem", "yâwt ruam", "ยอดรวม", "Miary", 3, "n", ZP, "", "szczyt razem"),
("B1", "różnica (liczbowa)", "phǒn tàang", "ผลต่าง", "Miary", 2, "n", LI, "", "wynik różny"),
("B1", "procent", "poe-sen", "เปอร์เซ็นต์", "Miary", 4, "n", LI, "", ""),

# ======================================================= kaan- : usługi i miasto
("B1", "usługa transportowa", "kaan khǒn sòng", "การขนส่ง", "Usługi", 3, "n", TR, "", ""),
("B1", "wynajem", "kaan châo", "การเช่า", "Usługi", 3, "n", HO, "", ""),
("B1", "sprzątanie ulic", "kaan kwàat thà-nǒn", "การกวาดถนน", "Usługi", 2, "n", MO, "", ""),
("B1", "budowa drogi", "kaan sâang thà-nǒn", "การสร้างถนน", "Usługi", 2, "n", MO, "", ""),
("B1", "naprawa prądu", "kaan sâwm fai", "การซ่อมไฟ", "Usługi", 2, "n", AW, "", ""),
("B1", "przerwa w dostawie wody", "kaan yùt jàai nám", "การหยุดจ่ายน้ำ", "Usługi", 2, "n", AW, "", "zatrzymać wydawanie wody"),
("B1", "wywóz śmieci", "kaan kèp khà-yà", "การเก็บขยะ", "Usługi", 2, "n", DC, "", ""),
("B1", "dostawa jedzenia", "kaan sòng aa-hǎan", "การส่งอาหาร", "Usługi", 3, "n", RE, "", ""),
("B1", "rezerwacja stolika", "kaan jawng tó", "การจองโต๊ะ", "Usługi", 3, "n", RE, "", ""),
("B1", "obsługa gości", "kaan dûu lae khàek", "การดูแลแขก", "Usługi", 2, "n", HO, "", "opiekować się gość"),
]
