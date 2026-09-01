# -*- coding: utf-8 -*-
"""Sesja F — KOLORY. System zamkniety, domkniety w calosci.

Krotka rekordu:
  (poziom, polski, fonetyka, tajski, kategoria, podkategoria, freq, rejestr,
   notatka, znaczenie doslowne, [przyklady], [powiazania po polskim hasle],
   [warianty polskie])

Przyklad: (polski, fonetyka, tajski). Kazdy rekord ma 2-3 przyklady.
Typ rekordu to zawsze "word" — to ma byc slownik, nie zbior zdan.

Zasada tajska: nazwa koloru to ZAWSZE „sǐi” + rdzen. Samo „daeng” znaczy
„czerwony” tylko w zlozeniach (np. „mǔu daeng”). W zdaniu opisujacym rzecz
mowi sie „X sǐi daeng” bez czasownika „byc”.
"""

CAT = "Cechy i opinie"
SUB = "Kolory"

COLORS = [

# ---------------------------------------------------------------- rdzen systemu
("A1", "czerwony", "sǐi daeng", "สีแดง", CAT, SUB, 5, "n",
 "Nazwa koloru to zawsze „sǐi” plus rdzeń. Samo „daeng” występuje tylko w złożeniach, np. „mǔu daeng” (czerwona wieprzowina).",
 "kolor czerwony",
 [("Ta koszulka jest czerwona.", "sûea tua níi sǐi daeng khráp", "เสื้อตัวนี้สีแดงครับ"),
  ("Poproszę czerwony.", "khǎw sǐi daeng khráp", "ขอสีแดงครับ"),
  ("Nie lubię czerwonego.", "phǒm mâi châwp sǐi daeng khráp", "ผมไม่ชอบสีแดงครับ")],
 ["niebieski", "zielony", "kolor (barwa)"], []),

("A1", "niebieski", "sǐi fáa", "สีฟ้า", CAT, SUB, 5, "n",
 "„sǐi fáa” to niebieski jasny, jak niebo — i to jego Tajowie mają na myśli, mówiąc po prostu „niebieski”. Granat to osobne słowo: „sǐi nám-ngoen”.",
 "kolor nieba",
 [("Lubię niebieski.", "phǒm châwp sǐi fáa khráp", "ผมชอบสีฟ้าครับ"),
  ("Czy jest w niebieskim?", "mii sǐi fáa mǎi khráp", "มีสีฟ้าไหมครับ"),
  ("Niebo dzisiaj jest niebieskie.", "wan-níi tháwng-fáa sǐi fáa", "วันนี้ท้องฟ้าสีฟ้า")],
 ["granatowy", "zielony", "czerwony"], []),

("A2", "granatowy", "sǐi nám-ngoen", "สีน้ำเงิน", CAT, SUB, 4, "n",
 "Ciemny, nasycony niebieski. Polak zwykle powie „niebieski” na jedno i drugie, ale Taj rozróżnia: mundur i garnitur są „nám-ngoen”, niebo jest „fáa”.",
 "kolor wody srebrnej",
 [("Poproszę granatowe spodnie.", "khǎw kaang-keeng sǐi nám-ngoen khráp", "ขอกางเกงสีน้ำเงินครับ"),
  ("Ta koszula jest granatowa, nie czarna.", "sûea tua níi sǐi nám-ngoen mâi châi sǐi dam", "เสื้อตัวนี้สีน้ำเงินไม่ใช่สีดำ")],
 ["niebieski", "czarny"], ["ciemnoniebieski"]),

("A1", "zielony", "sǐi khǐao", "สีเขียว", CAT, SUB, 5, "n",
 "Ton rosnący na „khǐao” — głos idzie w górę. Przy tonie średnim wychodzi inne słowo.",
 "kolor zielony",
 [("Zielone światło.", "fai sǐi khǐao", "ไฟสีเขียว"),
  ("Chciałbym zieloną torbę.", "phǒm yàak dâai krà-pǎo sǐi khǐao khráp", "ผมอยากได้กระเป๋าสีเขียวครับ"),
  ("Te warzywa są zielone.", "phàk níi sǐi khǐao", "ผักนี้สีเขียว")],
 ["żółty", "niebieski", "warzywo"], []),

("A1", "żółty", "sǐi lǔeang", "สีเหลือง", CAT, SUB, 5, "n",
 "„ǔea” to samogłoska, której nie ma po polsku — zaczynasz od „y”, przechodzisz w „a”. Ton rosnący.",
 "kolor żółty",
 [("Żółta taksówka.", "táek-sîi sǐi lǔeang", "แท็กซี่สีเหลือง"),
  ("Poproszę żółty.", "khǎw sǐi lǔeang khráp", "ขอสีเหลืองครับ"),
  ("To mango jest jeszcze żółte.", "má-mûang lûuk níi yang sǐi lǔeang", "มะม่วงลูกนี้ยังสีเหลือง")],
 ["zielony", "pomarańczowy"], []),

("A1", "czarny", "sǐi dam", "สีดำ", CAT, SUB, 5, "n",
 "Jedno z niewielu określeń koloru, którego rdzeń bywa używany bez „sǐi” — „kaafae dam” to czarna kawa.",
 "kolor czarny",
 [("Poproszę czarną kawę.", "khǎw kaa-fae dam khráp", "ขอกาแฟดำครับ"),
  ("Mam czarny telefon.", "thoo-rá-sàp khǎwng phǒm sǐi dam khráp", "โทรศัพท์ของผมสีดำครับ"),
  ("Czy jest w czarnym?", "mii sǐi dam mǎi khráp", "มีสีดำไหมครับ")],
 ["biały", "szary", "granatowy"], []),

("A1", "biały", "sǐi khǎao", "สีขาว", CAT, SUB, 5, "n",
 "Uwaga na parę minimalną: „khǎao” z tonem rosnącym to biały, „khâaw” z opadającym to ryż. Różnica tonu zmienia słowo całkowicie.",
 "kolor biały",
 [("Biała koszula.", "sûea sǐi khǎao", "เสื้อสีขาว"),
  ("Poproszę biały ryż.", "khǎw khâaw sǔai khráp", "ขอข้าวสวยครับ"),
  ("Ściany są białe.", "fǎa sǐi khǎao", "ฝาสีขาว")],
 ["czarny", "szary"], []),

("A1", "różowy", "sǐi chom-phuu", "สีชมพู", CAT, SUB, 4, "n",
 "Od nazwy owocu róży jawajskiej. „ch” czytaj jak polskie „cz”.",
 "kolor jabłka różanego",
 [("Ona lubi różowy.", "kháo châwp sǐi chom-phuu khâ", "เขาชอบสีชมพูค่ะ"),
  ("Poproszę różową.", "khǎw sǐi chom-phuu khráp", "ขอสีชมพูครับ")],
 ["czerwony", "fioletowy"], []),

("A1", "pomarańczowy", "sǐi sôm", "สีส้ม", CAT, SUB, 4, "n",
 "Dokładnie jak po polsku: kolor nazwany od owocu. „sôm” to pomarańcza.",
 "kolor pomarańczy",
 [("Pomarańczowa koszulka.", "sûea sǐi sôm", "เสื้อสีส้ม"),
  ("Poproszę sok pomarańczowy.", "khǎw nám sôm khráp", "ขอน้ำส้มครับ")],
 ["żółty", "czerwony"], []),

("A1", "fioletowy", "sǐi mûang", "สีม่วง", CAT, SUB, 4, "n",
 "Ton opadający. „ûa” to dyftong: zaczynasz od „u”, kończysz na „a”.",
 "kolor fioletowy",
 [("Fioletowy kwiat.", "dàwk-mái sǐi mûang", "ดอกไม้สีม่วง"),
  ("Czy macie to w fiolecie?", "mii sǐi mûang mǎi khráp", "มีสีม่วงไหมครับ")],
 ["różowy", "niebieski"], []),

("A1", "szary", "sǐi thao", "สีเทา", CAT, SUB, 4, "n",
 "„th” to „t” z przydechem, nie angielskie „th”. „ao” czytaj jak polskie „au”.",
 "kolor szary",
 [("Szare niebo.", "tháwng-fáa sǐi thao", "ท้องฟ้าสีเทา"),
  ("Poproszę szare spodnie.", "khǎw kaang-keeng sǐi thao khráp", "ขอกางเกงสีเทาครับ")],
 ["czarny", "biały"], []),

("A1", "brązowy", "sǐi nám-taan", "สีน้ำตาล", CAT, SUB, 4, "n",
 "Dosłownie „kolor cukru palmowego” — „nám-taan” to zarazem cukier. To samo słowo usłyszysz w kawiarni.",
 "kolor cukru",
 [("Brązowe buty.", "rawng-tháo sǐi nám-taan", "รองเท้าสีน้ำตาล"),
  ("Poproszę bez cukru.", "mâi sài nám-taan khráp", "ไม่ใส่น้ำตาลครับ")],
 ["czarny", "złoty"], []),

("A2", "złoty", "sǐi thawng", "สีทอง", CAT, SUB, 4, "n",
 "Kolor obecny wszędzie w świątyniach. „thawng” to też złoto jako materiał.",
 "kolor złota",
 [("Złoty posąg.", "phrá-phút-thá-rûup sǐi thawng", "พระพุทธรูปสีทอง"),
  ("Ten pierścionek jest złoty.", "wǎen wong níi sǐi thawng", "แหวนวงนี้สีทอง")],
 ["srebrny", "żółty"], []),

("A2", "srebrny", "sǐi ngoen", "สีเงิน", CAT, SUB, 3, "n",
 "„ngoen” to zarazem srebro i pieniądze. „ng” na początku sylaby to jeden dźwięk, jak w „bank” bez „k”.",
 "kolor srebra",
 [("Srebrny samochód.", "rót sǐi ngoen", "รถสีเงิน"),
  ("Wolę srebrny niż złoty.", "phǒm châwp sǐi ngoen mâak kwàa sǐi thawng khráp", "ผมชอบสีเงินมากกว่าสีทองครับ")],
 ["złoty", "szary"], []),

# -------------------------------------------------- odcienie i budowa konstrukcji
("A2", "jasny odcień", "sǐi àwn", "สีอ่อน", CAT, SUB, 4, "n",
 "Odcień dokłada się PO nazwie koloru: „sǐi fáa àwn” = jasnoniebieski. Kolejność odwrotna niż po polsku.",
 "kolor miękki",
 [("Poproszę jaśniejszy odcień.", "khǎw sǐi àwn kwàa níi khráp", "ขอสีอ่อนกว่านี้ครับ"),
  ("Jasnoniebieski, proszę.", "sǐi fáa àwn khráp", "สีฟ้าอ่อนครับ")],
 ["ciemny odcień", "kolor (barwa)"], ["jasnyodcień"]),

("A2", "ciemny odcień", "sǐi khêm", "สีเข้ม", CAT, SUB, 4, "n",
 "Para do „sǐi àwn”. „khêm” znaczy też mocny w smaku — o kawie i o kolorze mówi się tak samo.",
 "kolor mocny",
 [("Poproszę ciemniejszy odcień.", "khǎw sǐi khêm kwàa níi khráp", "ขอสีเข้มกว่านี้ครับ"),
  ("Ciemnozielony mi się podoba.", "phǒm châwp sǐi khǐao khêm khráp", "ผมชอบสีเขียวเข้มครับ")],
 ["jasny odcień", "kolor (barwa)"], []),

("A1", "kolor (barwa)", "sǐi", "สี", CAT, SUB, 5, "n",
 "Wyraz bazowy całego systemu. Ton rosnący. To samo słowo znaczy „farba”.",
 "",
 [("Jaki kolor lubisz?", "khun châwp sǐi à-rai khráp", "คุณชอบสีอะไรครับ"),
  ("Ten kolor jest ładny.", "sǐi níi sǔai khráp", "สีนี้สวยครับ"),
  ("Ile jest kolorów?", "mii kìi sǐi khráp", "มีกี่สีครับ")],
 ["czerwony", "jasny odcień", "kolorowy"], ["barwa"]),

("A2", "kolorowy", "lǎai sǐi", "หลายสี", CAT, SUB, 3, "n",
 "Dosłownie „wiele kolorów”. O wzorzystej tkaninie powie się raczej „mii laai” (ma wzór).",
 "wiele kolorów",
 [("Chciałbym coś kolorowego.", "phǒm yàak dâai bàep lǎai sǐi khráp", "ผมอยากได้แบบหลายสีครับ"),
  ("Ten targ jest bardzo kolorowy.", "tà-làat níi lǎai sǐi mâak", "ตลาดนี้หลายสีมาก")],
 ["kolor (barwa)"], []),

("A2", "ten sam kolor", "sǐi diao kan", "สีเดียวกัน", CAT, SUB, 4, "n",
 "„diao kan” znaczy „ten sam” i przykleja się do wielu rzeczowników: „wan diao kan” = tego samego dnia.",
 "kolor jeden razem",
 [("Chcę ten sam kolor.", "phǒm ao sǐi diao kan khráp", "ผมเอาสีเดียวกันครับ"),
  ("Mamy takie same koszulki.", "rao sài sûea sǐi diao kan", "เราใส่เสื้อสีเดียวกัน")],
 ["kolor (barwa)", "inny kolor"], []),

("A2", "inny kolor", "sǐi ùen", "สีอื่น", CAT, SUB, 4, "n",
 "Najczęstsza prośba w sklepie z ubraniami. „ùen” = inny, pozostały.",
 "kolor inny",
 [("Czy jest w innym kolorze?", "mii sǐi ùen mǎi khráp", "มีสีอื่นไหมครับ"),
  ("Poproszę w innym kolorze.", "khǎw sǐi ùen khráp", "ขอสีอื่นครับ")],
 ["ten sam kolor", "kolor (barwa)"], []),

("A1", "jaki kolor", "sǐi à-rai", "สีอะไร", "Pytania", SUB, 5, "n",
 "Pytanie o kolor buduje się bez czasownika „być”: dosłownie „to auto kolor co”.",
 "kolor co",
 [("Jakiego koloru jest twój samochód?", "rót khun sǐi à-rai khráp", "รถคุณสีอะไรครับ"),
  ("Jaki kolor chcesz?", "ao sǐi à-rai khráp", "เอาสีอะไรครับ"),
  ("Jakiego koloru jest ta torba?", "krà-pǎo bai níi sǐi à-rai khráp", "กระเป๋าใบนี้สีอะไรครับ")],
 ["kolor (barwa)", "czerwony"], []),

("A2", "farbować", "yáwm sǐi", "ย้อมสี", "Czasowniki", SUB, 3, "n",
 "O włosach i o tkaninie. Samo „yáwm” wystarczy w rozmowie u fryzjera.",
 "barwić kolor",
 [("Chciałbym pofarbować włosy.", "phǒm yàak yáwm phǒm khráp", "ผมอยากย้อมผมครับ"),
  ("Ta koszulka farbuje.", "sûea tua níi sǐi tòk", "เสื้อตัวนี้สีตก")],
 ["kolor (barwa)", "włosy"], []),

("A2", "kolor wyblakł", "sǐi sìit", "สีซีด", CAT, SUB, 3, "n",
 "Przydaje się przy reklamacji. „sìit” to też blady o cerze.",
 "kolor blady",
 [("Kolor wyblakł po praniu.", "sák láew sǐi sìit khráp", "ซักแล้วสีซีดครับ"),
  ("Jesteś blady, dobrze się czujesz?", "khun nâa sìit sà-baai dii mǎi khráp", "คุณหน้าซีดสบายดีไหมครับ")],
 ["kolor (barwa)", "prać"], []),
]
