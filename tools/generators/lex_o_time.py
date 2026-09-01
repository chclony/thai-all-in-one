# -*- coding: utf-8 -*-
"""Sesja O, partia 12 — CZAS, LICZBY, MIARY, ŚWIĘTA.

Cztery warstwy, wszystkie oparte na sylabach, które baza już ma:

1. **Czas względny** — przedwczoraj, za trzy dni, w przyszłym tygodniu,
   pod koniec miesiąca. Baza miała 141 haseł na czas, ale prawie wyłącznie
   punktowych (godziny, dni tygodnia, miesiące). Relacja między punktami
   była luką: uczący się umiał powiedzieć „wtorek”, a nie umiał „za dwa dni”.

2. **Miary i pojemniki liczące** — kilogram, metr, butelka, porcja, kawałek.
   W tajskim liczy się przez klasyfikator, a te są w osobnym module
   `classifiers.json`; tu dokładamy jednostki, które klasyfikatorami nie są.

3. **Święta i kalendarz** — Songkran, Loy Krathong, dzień buddyjski, rok
   buddyjski. Bez tego rozmowa o dacie się rozjeżdża: w Tajlandii rok 2026
   to rok 2569, a daty urzędowe podaje się w kalendarzu buddyjskim.

4. **Pytania o czas i ilość** — bo połowa rozmowy praktycznej to „kiedy”
   i „ile”.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

CD = "Czas i daty"
LI = "Liczby i liczenie"
PY = "Pytania"
ST = "Small talk"
GU = "Gramatyka użytkowa"
ZP = "Zakupy i pieniądze"
JN = "Jedzenie i napoje"
RE = "Restauracja"
MO = "Miejsca i orientacja"
PG = "Podstawy i grzeczność"
TR = "Transport"
HO = "Hotel"

TIME = [

# =========================================================== czas względny
("A1", "przedwczoraj", "mûea waan suen", "เมื่อวานซืน", "Czas względny", 3, "adv", CD, "", ""),
("A1", "pojutrze", "má-ruen níi", "มะรืนนี้", "Czas względny", 3, "adv", CD, "", ""),
("A1", "za trzy dni", "ìik sǎam wan", "อีกสามวัน", "Czas względny", 4, "adv", CD, "", "jeszcze trzy dni"),
("A1", "trzy dni temu", "sǎam wan thîi láew", "สามวันที่แล้ว", "Czas względny", 4, "adv", CD, "", ""),
("A1", "w przyszłym tygodniu", "aa-thít nâa", "อาทิตย์หน้า", "Czas względny", 5, "adv", CD, "", "tydzień przedni"),
("A1", "w zeszłym tygodniu", "aa-thít thîi láew", "อาทิตย์ที่แล้ว", "Czas względny", 5, "adv", CD, "", ""),
("A1", "w przyszłym miesiącu", "duean nâa", "เดือนหน้า", "Czas względny", 4, "adv", CD, "", ""),
("A1", "w zeszłym miesiącu", "duean thîi láew", "เดือนที่แล้ว", "Czas względny", 4, "adv", CD, "", ""),
("A1", "w przyszłym roku", "pii nâa", "ปีหน้า", "Czas względny", 4, "adv", CD, "", ""),
("A1", "w zeszłym roku", "pii thîi láew", "ปีที่แล้ว", "Czas względny", 4, "adv", CD, "", ""),
("A2", "na początku miesiąca", "tôn duean", "ต้นเดือน", "Czas względny", 4, "adv", CD, "", "początek miesiąca"),
("A2", "w środku miesiąca", "klaang duean", "กลางเดือน", "Czas względny", 3, "adv", CD, "", ""),
("A2", "pod koniec miesiąca", "sîn duean", "สิ้นเดือน", "Czas względny", 4, "adv", CD,
 "Dzień wypłaty w Tajlandii — stąd tłok w centrach handlowych na sîn duean.", ""),
("A2", "na początku roku", "tôn pii", "ต้นปี", "Czas względny", 3, "adv", CD, "", ""),
("A2", "pod koniec roku", "plaai pii", "ปลายปี", "Czas względny", 3, "adv", CD, "", ""),
("A2", "od (jakiegoś czasu)", "tâng tàe", "ตั้งแต่", "Czas względny", 5, "adv", GU, "", ""),
("A2", "do (jakiegoś czasu)", "jon thǔeng wee-laa", "จนถึงเวลา", "Czas względny", 3, "adv", GU, "", ""),
("A2", "przez cały dzień", "tháng wan", "ทั้งวัน", "Czas względny", 4, "adv", CD, "", ""),
("A2", "przez całą noc", "tháng khuen", "ทั้งคืน", "Czas względny", 3, "adv", CD, "", ""),
("A2", "co drugi dzień", "wan wén wan", "วันเว้นวัน", "Czas względny", 3, "adv", CD, "", "dzień omijać dzień"),
("A2", "codziennie rano", "thúk cháo", "ทุกเช้า", "Czas względny", 4, "adv", CD, "", ""),
("A2", "raz w tygodniu", "aa-thít lá khráng", "อาทิตย์ละครั้ง", "Czas względny", 4, "adv", CD, "", ""),
("A2", "dwa razy dziennie", "wan lá sǎwng khráng", "วันละสองครั้ง", "Czas względny", 4, "adv", CD,
 "Wzorzec „X lá Y” — na dawkach leków i cenach za sztukę.", ""),
("A2", "przed chwilą", "mûea sàk khrûu", "เมื่อสักครู่", "Czas względny", 4, "adv", CD, "", ""),
("A2", "za chwilę", "ìik sàk khrûu", "อีกสักครู่", "Czas względny", 5, "adv", CD, "", ""),
("A2", "w tym samym czasie", "wee-laa diao kan", "เวลาเดียวกัน", "Czas względny", 3, "adv", CD, "", ""),
("A2", "wcześniej niż", "kàwn kwàa", "ก่อนกว่า", "Czas względny", 3, "adv", GU, "", ""),
("A2", "później niż", "chái kwàa", "ช้ากว่า", "Czas względny", 3, "adv", GU, "", ""),

# =========================================================== pory i etapy
("A1", "świt", "rûng cháo", "รุ่งเช้า", "Pory", 3, "n", CD, "", ""),
("A1", "przedpołudnie", "cháo sǎai", "เช้าสาย", "Pory", 3, "n", CD, "", ""),
("A1", "zmierzch", "phlóp khâm", "พลบค่ำ", "Pory", 2, "n", CD, "", ""),
("A1", "północ (godzina)", "thîang khuen", "เที่ยงคืน", "Pory", 4, "n", CD, "", "południe nocy"),
("A1", "kwadrans", "sìp-hâa naa-thii", "สิบห้านาที", "Pory", 4, "n", CD, "", ""),
("A1", "pół godziny", "khrûeng chûa-moong", "ครึ่งชั่วโมง", "Pory", 5, "n", CD, "", ""),
("A2", "chwila, moment", "khrûu nùeng", "ครู่หนึ่ง", "Pory", 4, "n", CD, "", ""),
("A2", "okres, etap", "chûang", "ช่วง", "Pory", 5, "n", CD,
 "chûang níi — w tym okresie, ostatnio. Bardzo częste w mowie.", ""),
("A2", "termin, wyznaczony czas", "kam-nòt", "กำหนด", "Pory", 3, "n", CD, "", ""),
("A2", "godziny otwarcia", "wee-laa tham kaan", "เวลาทำการ", "Pory", 4, "n", ZP, "", "czas pracy"),
("A2", "godzina szczytu", "chûang rêng dùan", "ช่วงเร่งด่วน", "Pory", 4, "n", TR, "", ""),
("A2", "poza sezonem", "nâwk rúe-duu", "นอกฤดู", "Pory", 3, "n", TR, "", ""),
("A2", "w sezonie", "nai rúe-duu", "ในฤดู", "Pory", 3, "n", TR, "", ""),
("A2", "dzień powszedni", "wan tham ngaan", "วันทำงาน", "Pory", 4, "n", CD, "", ""),
("A2", "dzień wolny", "wan yùt", "วันหยุด", "Pory", 5, "n", CD, "", ""),
("A2", "długi weekend", "wan yùt yaao", "วันหยุดยาว", "Pory", 3, "n", CD, "", ""),

# =========================================================== święta i kalendarz
("A1", "Songkran (tajski Nowy Rok)", "sǒng-kraan", "สงกรานต์", "Święta", 5, "n", ST,
 "13–15 kwietnia. Trzy dni oblewania wodą — pory roku i kalendarza turystycznego nie da się bez tego zrozumieć.", ""),
("A1", "Loy Krathong (święto świateł)", "loi krà-thong", "ลอยกระทง", "Święta", 4, "n", ST,
 "Listopadowa pełnia. Puszcza się na wodę wianki ze świecą.", "puścić koszyczek"),
("A1", "dzień buddyjski", "wan phrá", "วันพระ", "Święta", 3, "n", ST,
 "Cztery razy w miesiącu księżycowym. W te dni część barów nie sprzedaje alkoholu.", "dzień mnich"),
("A1", "Nowy Rok", "pii mài", "ปีใหม่", "Święta", 5, "n", ST, "", "rok nowy"),
("A1", "urodziny", "wan kòoet", "วันเกิด", "Święta", 5, "n", ST, "", "dzień urodzić się"),
("A2", "rocznica", "wan khróp râwp", "วันครบรอบ", "Święta", 3, "n", ST, "", ""),
("A2", "święto państwowe", "wan yùt râat-chá-kaan", "วันหยุดราชการ", "Święta", 3, "n", CD, "", ""),
("A2", "rok buddyjski", "phút-thá sàk-kà-ràat", "พุทธศักราช", "Święta", 3, "n", CD,
 "Na dokumentach urzędowych rok podaje się buddyjski: rok 2026 to 2569. Różnica wynosi 543 lata.", ""),
("A2", "kalendarz", "pà-tì-thin", "ปฏิทิน", "Święta", 3, "n", CD, "", ""),
("A2", "data", "wan thîi", "วันที่", "Święta", 5, "n", CD, "", ""),
("A2", "wesele (uroczystość)", "ngaan mong-khon", "งานมงคล", "Święta", 2, "n", ST, "", ""),
("A2", "pogrzeb", "ngaan sòp", "งานศพ", "Święta", 2, "n", ST, "", ""),
("A2", "impreza, przyjęcie", "ngaan líang", "งานเลี้ยง", "Święta", 4, "n", ST, "", "impreza karmić"),
("A2", "festiwal", "thêet-sà-kaan", "เทศกาล", "Święta", 4, "n", ST, "", ""),
("A2", "procesja świątynna", "ngaan wát", "งานวัด", "Święta", 3, "n", ST, "", "impreza świątynia"),

# =========================================================== miary
("A1", "kilogram", "kì-loo", "กิโล", "Miary", 5, "n", ZP,
 "W mowie skraca się i do wagi, i do odległości: „sìp kì-loo” może znaczyć jedno i drugie.", ""),
("A1", "gram", "kram", "กรัม", "Miary", 3, "n", ZP, "", ""),
("A1", "litr", "lít", "ลิตร", "Miary", 4, "n", ZP, "", ""),
("A1", "metr", "méet", "เมตร", "Miary", 4, "n", LI, "", ""),
("A1", "centymetr", "sen", "เซนต์", "Miary", 3, "n", LI, "", ""),
("A1", "kilometr", "kì-loo méet", "กิโลเมตร", "Miary", 4, "n", LI, "", ""),
("A1", "połowa", "khrûeng", "ครึ่ง", "Miary", 5, "n", LI, "", ""),
("A1", "ćwierć", "sèet nùeng sùan sìi", "เศษหนึ่งส่วนสี่", "Miary", 2, "n", LI, "", "reszta jedna część cztery"),
("A2", "para (sztuk)", "khûu nùeng", "คู่หนึ่ง", "Miary", 3, "n", LI, "", ""),
("A2", "tuzin", "lǒo", "โหล", "Miary", 3, "n", ZP, "", ""),
("A2", "porcja", "thîi", "ที่", "Miary", 5, "n", RE,
 "„sǎwng thîi” — dwie porcje. To samo słowo co „miejsce”.", ""),
("A2", "talerz (jako porcja)", "jaan", "จาน", "Miary", 5, "n", RE, "", ""),
("A2", "miska (jako porcja)", "chaam", "ชาม", "Miary", 5, "n", RE, "", ""),
("A2", "kawałek", "chín", "ชิ้น", "Miary", 5, "n", RE, "", ""),
("A2", "plaster, kromka", "phàen", "แผ่น", "Miary", 4, "n", JN, "", ""),
("A2", "łyżka (jako miara)", "cháwn", "ช้อน", "Miary", 4, "n", JN, "", ""),
("A2", "szklanka (jako miara)", "kâew nùeng", "แก้วหนึ่ง", "Miary", 4, "n", JN, "", ""),
("A2", "worek, torba (jako miara)", "thǔng nùeng", "ถุงหนึ่ง", "Miary", 4, "n", ZP, "", ""),
("A2", "pudełko (jako miara)", "klàwng nùeng", "กล่องหนึ่ง", "Miary", 4, "n", ZP, "", ""),
("A2", "zestaw, komplet", "chút", "ชุด", "Miary", 4, "n", ZP, "", ""),

# =========================================================== ilość i porównanie
("A1", "kilka", "sǎwng sǎam", "สองสาม", "Ilość", 5, "adv", LI, "", "dwa trzy"),
("A1", "wiele", "lǎai", "หลาย", "Ilość", 5, "adv", LI, "", ""),
("A1", "trochę, odrobinę", "nít nàwi", "นิดหน่อย", "Ilość", 5, "adv", LI, "", ""),
("A1", "wszystko", "tháng mòt", "ทั้งหมด", "Ilość", 5, "adv", LI, "", "całe skończone"),
("A1", "nic", "mâi mii à-rai", "ไม่มีอะไร", "Ilość", 5, "adv", LI, "", "nie ma czegokolwiek"),
("A1", "reszta, pozostałe", "thîi lǔea", "ที่เหลือ", "Ilość", 4, "adv", LI, "", ""),
("A1", "każdy", "thúk", "ทุก", "Ilość", 5, "adv", GU, "", ""),
("A1", "żaden", "mâi mii", "ไม่มี", "Ilość", 5, "adv", GU, "", ""),
("A2", "więcej niż", "mâak kwàa", "มากกว่า", "Ilość", 5, "adv", LI, "", ""),
("A2", "mniej niż", "náwi kwàa", "น้อยกว่า", "Ilość", 5, "adv", LI, "", ""),
("A2", "tyle samo", "thâo kan", "เท่ากัน", "Ilość", 5, "adv", LI, "", "równo razem"),
("A2", "dwa razy tyle", "sǎwng thâo", "สองเท่า", "Ilość", 3, "adv", LI, "", ""),
("A2", "połowa tego", "khrûeng nùeng", "ครึ่งหนึ่ง", "Ilość", 4, "adv", LI, "", ""),
("A2", "wystarczy", "phaw láew", "พอแล้ว", "Ilość", 5, "adv", RE,
 "Zdanie kończące dolewanie i dokładanie. Bez niego kelner nie przestanie.", ""),
("A2", "za mało", "mâi phaw", "ไม่พอ", "Ilość", 4, "adv", LI, "", ""),
("A2", "za dużo", "mâak kooen pai", "มากเกินไป", "Ilość", 5, "adv", LI, "", ""),
("A2", "w sam raz", "phaw dii láew", "พอดีแล้ว", "Ilość", 4, "adv", ZP, "", ""),
("A2", "prawie wszystko", "kùeap tháng mòt", "เกือบทั้งหมด", "Ilość", 3, "adv", LI, "", ""),
("A2", "co najmniej", "yàang náwi thîi sùt", "อย่างน้อยที่สุด", "Ilość", 3, "adv", LI, "", ""),
("A2", "łącznie, w sumie", "ruam tháng mòt", "รวมทั้งหมด", "Ilość", 5, "adv", ZP, "", ""),

# =========================================================== kolejność
("A1", "najpierw", "râek sùt", "แรกสุด", "Kolejność", 4, "adv", GU, "", ""),
("A1", "potem", "lǎng jàak nán", "หลังจากนั้น", "Kolejność", 5, "adv", GU, "", ""),
("A1", "na końcu", "tawn sùt tháai", "ตอนสุดท้าย", "Kolejność", 4, "adv", GU, "", ""),
("A1", "następny", "tàw pai", "ต่อไป", "Kolejność", 5, "adj", GU, "", ""),
("A1", "poprzedni", "kàwn nâa níi", "ก่อนหน้านี้", "Kolejność", 4, "adj", GU, "", ""),
("A1", "ostatni (w kolejce)", "khon sùt tháai", "คนสุดท้าย", "Kolejność", 3, "n", MO, "", ""),
("A2", "po kolei", "taam lam-dàp", "ตามลำดับ", "Kolejność", 3, "adv", GU, "", ""),
("A2", "jednocześnie z", "phráwm kàp", "พร้อมกับ", "Kolejność", 3, "adv", GU, "", ""),
("A2", "od razu potem", "than thii lǎng", "ทันทีหลัง", "Kolejność", 2, "adv", GU, "", ""),

# =========================================================== pytania o czas i ilość
("A1", "O której godzinie?", "kìi moong khráp", "กี่โมงครับ", "Pytania", 5, "w", PY, "", ""),
("A1", "Jak długo to trwa?", "naan thâo rài khráp", "นานเท่าไหร่ครับ", "Pytania", 5, "w", PY, "", ""),
("A1", "Od której jest otwarte?", "pòet kìi moong khráp", "เปิดกี่โมงครับ", "Pytania", 5, "w", PY, "", ""),
("A1", "Do której jest otwarte?", "pìt kìi moong khráp", "ปิดกี่โมงครับ", "Pytania", 5, "w", PY, "", ""),
("A1", "Który dzisiaj?", "wan níi wan thîi thâo rài khráp", "วันนี้วันที่เท่าไหร่ครับ", "Pytania", 4, "w", PY, "", ""),
("A1", "Ile sztuk?", "kìi an khráp", "กี่อันครับ", "Pytania", 5, "w", PY, "", ""),
("A1", "Ile osób?", "kìi khon khráp", "กี่คนครับ", "Pytania", 5, "w", PY, "", ""),
("A2", "Ile razy?", "kìi khráng khráp", "กี่ครั้งครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Kiedy będzie gotowe?", "sèt mûea rài khráp", "เสร็จเมื่อไหร่ครับ", "Pytania", 5, "w", PY, "", ""),
("A2", "Czy zdążę?", "than mǎi khráp", "ทันไหมครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Jak daleko stąd?", "klai thâo rài khráp", "ไกลเท่าไหร่ครับ", "Pytania", 5, "w", PY, "", ""),
("A2", "Ile to waży?", "nàk thâo rài khráp", "หนักเท่าไหร่ครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Na jak długo?", "sǎm-ràp kìi wan khráp", "สำหรับกี่วันครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Czy można później?", "chái wee-laa lǎng dâi mǎi khráp", "ใช้เวลาหลังได้ไหมครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "O której się spotkamy?", "jooe kan kìi moong khráp", "เจอกันกี่โมงครับ", "Pytania", 5, "w", PY, "", ""),
("A2", "Czy jest wolne miejsce dziś wieczorem?", "khuen níi mii thîi wâang mǎi khráp", "คืนนี้มีที่ว่างไหมครับ", "Pytania", 4, "w", HO, "", ""),
("A2", "Do kiedy trzeba oddać?", "tâwng khuen mûea rài khráp", "ต้องคืนเมื่อไหร่ครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Czy to potrwa długo?", "jà naan mǎi khráp", "จะนานไหมครับ", "Pytania", 5, "w", PY, "", ""),

# =========================================================== zwroty czasowe
("A1", "Nie mam czasu.", "phǒm mâi mii wee-laa khráp", "ผมไม่มีเวลาครับ", "Zwroty", 5, "w", ST, "", ""),
("A1", "Mam czas.", "phǒm mii wee-laa khráp", "ผมมีเวลาครับ", "Zwroty", 4, "w", ST, "", ""),
("A1", "Spieszę się.", "phǒm rîip khráp", "ผมรีบครับ", "Zwroty", 5, "w", ST, "", ""),
("A2", "Jestem wolny jutro.", "phrûng níi phǒm wâang khráp", "พรุ่งนี้ผมว่างครับ", "Zwroty", 4, "w", ST, "", ""),
("A2", "Może innym razem.", "wái khraao nâa khráp", "ไว้คราวหน้าครับ", "Zwroty", 5, "w", PG,
 "Uprzejma odmowa. Rzadko oznacza konkretną obietnicę.", ""),
("A2", "Zdążyłem na czas.", "phǒm maa than wee-laa khráp", "ผมมาทันเวลาครับ", "Zwroty", 3, "w", ST, "", ""),
("A2", "Przepraszam za spóźnienie.", "khǎw thôot thîi maa sǎai khráp", "ขอโทษที่มาสายครับ", "Zwroty", 5, "w", PG, "", ""),
]
