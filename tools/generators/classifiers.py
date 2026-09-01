# -*- coding: utf-8 -*-
"""Klasyfikatory tajskie (ลักษณนาม) — tabela i dane dla `data/classifiers.json`.

Powód powstania: baza używała `an` jako klasyfikatora dla wszystkiego —
ręczników, koców, kluczy, talerzy, łyżek, biletów i map. `an` jest workiem
na drobne przedmioty bez własnego klasyfikatora i zaimkiem („ten tutaj”),
ale postawione przy rzeczowniku, który ma swój klasyfikator, jest błędem
gramatycznym równie wyraźnym jak polskie „dwa krzesłów”.

Szyk jest stały i odwrotny do polskiego:

    rzeczownik + liczba + klasyfikator
    bia        + sǎwng  + khùat        („piwo dwie butelki” = dwa piwa)

Wyjątek: przy `nùeng` (jeden) mowa potoczna zwykle przestawia szyk na
rzeczownik + klasyfikator + nùeng — i tę wersję słychać częściej.

Struktura:

* `CLASSIFIERS` — pełny wykaz. Każda pozycja: zapis fonetyczny, pismo tajskie
  (wyłącznie do TTS), wyjaśnienie po polsku, lista rzeczowników i przykłady
  liczenia.
* `NOUN_TO_CLASSIFIER` — odwzorowanie zapisu tajskiego rzeczownika na właściwy
  klasyfikator, budowane automatycznie z `CLASSIFIERS`. Używa go `stage8.py`
  do poprawiania istniejących rekordów.
"""

# Format pozycji:
#   (fonetyka, pismo, poziom, wyjaśnienie,
#    [(polski, fonetyka rzeczownika, pismo rzeczownika), ...],
#    [(polski przykład, fonetyka, pismo), ...])

CLASSIFIERS = [
    # ---------------------------------------------------------------- ludzie
    ("khon", "คน", "Survival",
     "Ludzie w mowie codziennej — niezależnie od wieku, płci i zawodu. "
     "Nie używa się go do mnichów ani do rodziny królewskiej.",
     [("człowiek / osoba", "khon", "คน"), ("przyjaciel", "phûean", "เพื่อน"),
      ("student", "nák rian", "นักเรียน"), ("kierowca", "khon khàp rót", "คนขับรถ"),
      ("lekarz", "mǎw", "หมอ"), ("dziecko", "dèk", "เด็ก")],
     [("Dwie osoby.", "sǎwng khon", "สองคน"),
      ("Jesteśmy w pięć osób.", "rao hâa khon", "เราห้าคน")]),

    ("thân", "ท่าน", "B1",
     "Osoby, którym należy się szacunek: przełożeni, goście oficjalni, "
     "urzędnicy wysokiego szczebla. Grzeczniejszy odpowiednik `khon`.",
     [("gość", "khàek", "แขก"), ("dyrektor", "phûu am-nuai kaan", "ผู้อำนวยการ"),
      ("prelegent", "phûu banyaai", "ผู้บรรยาย")],
     [("Trzej goście.", "khàek sǎam thân", "แขกสามท่าน"),
      ("Zapraszam dwie osoby.", "chəən sǎwng thân", "เชิญสองท่าน")]),

    ("rûup", "รูป", "B1",
     "Mnisi buddyjscy. Tego samego słowa używa się do zdjęć i obrazów.",
     [("mnich", "phrá", "พระ"), ("zdjęcie", "rûup", "รูป")],
     [("Pięciu mnichów.", "phrá hâa rûup", "พระห้ารูป"),
      ("Dwa zdjęcia.", "rûup sǎwng rûup", "รูปสองรูป")]),

    ("ong", "องค์", "B2",
     "Rodzina królewska, posągi Buddy, obiekty sakralne. Rejestr wysoki.",
     [("posąg Buddy", "phrá phút-thá rûup", "พระพุทธรูป"), ("pagoda", "chee-dii", "เจดีย์")],
     [("Jeden posąg Buddy.", "phrá phút-thá rûup nùeng ong", "พระพุทธรูปหนึ่งองค์"),
      ("Dwie pagody.", "chee-dii sǎwng ong", "เจดีย์สององค์")]),

    # -------------------------------------------------- zwierzęta i ubrania
    ("tua", "ตัว", "Survival",
     "Zwierzęta, a także ubrania zakładane na tułów i przedmioty o „ciele”: "
     "stoły, krzesła, litery. Jeden z najczęstszych klasyfikatorów.",
     [("pies", "mǎa", "หมา"), ("kot", "maew", "แมว"), ("ryba", "plaa", "ปลา"),
      ("koszulka", "sûea yúet", "เสื้อยืด"), ("spodnie", "kaang keeng", "กางเกง"),
      ("krzesło", "kâo îi", "เก้าอี้"), ("stół", "tó", "โต๊ะ"),
      ("sukienka", "krà-proong", "กระโปรง")],
     [("Dwa psy.", "mǎa sǎwng tua", "หมาสองตัว"),
      ("Poproszę dwie koszulki.", "khǎw sûea yúet sǎwng tua", "ขอเสื้อยืดสองตัว")]),

    # ------------------------------------------------------ przedmioty ogólne
    ("bai", "ใบ", "Survival",
     "Rzeczy puste w środku i rzeczy cienkie jak liść: torby, kapelusze, "
     "talerze, szklanki, poduszki, bilety, dokumenty, owoce o twardej skórce.",
     [("torba", "thǔng", "ถุง"), ("kapelusz", "mùak", "หมวก"),
      ("talerz", "jaan", "จาน"), ("szklanka", "kâew", "แก้ว"),
      ("poduszka", "mǎwn", "หมอน"), ("bilet", "tǔa", "ตั๋ว"),
      ("kask", "mùak kan nók", "หมวกกันน็อค"), ("mapa", "phǎen thîi", "แผนที่"),
      ("walizka", "krà-pǎo dəən thaang", "กระเป๋าเดินทาง"),
      ("paszport", "nǎng-sǔe dəən thaang", "หนังสือเดินทาง")],
     [("Poproszę dwa bilety.", "khǎw tǔa sǎwng bai", "ขอตั๋วสองใบ"),
      ("Ile jest talerzy?", "mii jaan kìi bai", "มีจานกี่ใบ")]),

    ("an", "อัน", "Survival",
     "Drobne przedmioty, które nie mają własnego klasyfikatora. "
     "UWAGA: to nie jest klasyfikator uniwersalny. Jeśli rzeczownik ma swój "
     "klasyfikator (ręcznik — phǔen, klucz — dàwk, talerz — bai), użycie `an` "
     "jest błędem. `an` służy też jako zaimek: `an níi` = ten tutaj.",
     [("rzecz", "khǎwng", "ของ"), ("ładowarka", "thîi chàat", "ที่ชาร์จ"),
      ("otwieracz", "thîi pòət", "ที่เปิด"), ("pilot", "rii-mòot", "รีโมท")],
     [("Ten tutaj.", "an níi", "อันนี้"),
      ("Poproszę dwie sztuki.", "khǎw sǎwng an", "ขอสองอัน")]),

    ("chín", "ชิ้น", "A1",
     "Kawałki i sztuki wykrojone z całości: mięso, ciasto, tkanina, "
     "a także meble i elementy garderoby liczone jako sztuki towaru.",
     [("kawałek", "chín", "ชิ้น"), ("ciasto", "khá-nǒm kháek", "ขนมเค้ก"),
      ("mięso", "núea", "เนื้อ"), ("mebel", "fəə-ní-jəə", "เฟอร์นิเจอร์")],
     [("Poproszę jeszcze jeden kawałek.", "khǎw ìik chín nùeng", "ขออีกชิ้นหนึ่ง"),
      ("Trzy kawałki kurczaka.", "kài sǎam chín", "ไก่สามชิ้น")]),

    ("phàen", "แผ่น", "A1",
     "Rzeczy płaskie i cienkie: kartka papieru, plaster, płyta, deska, "
     "serwetka papierowa.",
     [("kartka", "kràdàat", "กระดาษ"), ("plaster", "phlaastəə", "พลาสเตอร์"),
      ("serwetka", "kràdàat chét paak", "กระดาษเช็ดปาก"), ("płyta", "phàen sǐang", "แผ่นเสียง")],
     [("Poproszę dwa plastry.", "khǎw phlaastəə sǎwng phàen", "ขอพลาสเตอร์สองแผ่น"),
      ("Trzy kartki.", "kràdàat sǎam phàen", "กระดาษสามแผ่น")]),

    ("kâwn", "ก้อน", "A1",
     "Bryły i grudki: mydło, kamień, kostka lodu, kostka cukru, chmura.",
     [("mydło", "sabùu", "สบู่"), ("kamień", "hǐn", "หิน"),
      ("lód w kostkach", "náam khǎeng", "น้ำแข็ง"), ("chmura", "mêek", "เมฆ")],
     [("Poproszę jedno mydło.", "khǎw sabùu nùeng kâwn", "ขอสบู่หนึ่งก้อน"),
      ("Dwie kostki lodu.", "náam khǎeng sǎwng kâwn", "น้ำแข็งสองก้อน")]),

    ("mét", "เม็ด", "A1",
     "Drobinki i ziarna: tabletki, nasiona, koraliki, krople deszczu.",
     [("tabletka", "yaa", "ยา"), ("nasiono", "má-lét", "เมล็ด"),
      ("ziarnko ryżu", "khâo", "ข้าว")],
     [("Dwie tabletki.", "yaa sǎwng mét", "ยาสองเม็ด"),
      ("Bierz jedną tabletkę.", "kin yaa nùeng mét", "กินยาหนึ่งเม็ด")]),

    # ------------------------------------------------------------- tekstylia
    ("phǔen", "ผืน", "A1",
     "Płaskie tkaniny rozkładane na powierzchni: ręcznik, koc, mata, dywan, "
     "prześcieradło, chusta.",
     [("ręcznik", "phâa chét tua", "ผ้าเช็ดตัว"), ("koc", "phâa hòm", "ผ้าห่ม"),
      ("mata", "sùea", "เสื่อ"), ("dywan", "phrom", "พรม"),
      ("prześcieradło", "phâa puu thîi nawn", "ผ้าปูที่นอน")],
     [("Poproszę jeszcze jeden ręcznik.", "khǎw phâa chét tua ìik phǔen nùeng",
       "ขอผ้าเช็ดตัวอีกผืนหนึ่ง"),
      ("Ile jest koców?", "mii phâa hòm kìi phǔen", "มีผ้าห่มกี่ผืน")]),

    ("chút", "ชุด", "A1",
     "Komplety i zestawy: garnitur, strój, zestaw naczyń, zestaw obiadowy.",
     [("strój", "chút", "ชุด"), ("garnitur", "chút sùut", "ชุดสูท"),
      ("zestaw", "chút", "ชุด")],
     [("Poproszę jeden zestaw.", "khǎw nùeng chút", "ขอหนึ่งชุด"),
      ("Dwa komplety.", "sǎwng chút", "สองชุด")]),

    ("khûu", "คู่", "A1",
     "Rzeczy chodzące w parach: buty, skarpetki, pałeczki, kolczyki, rękawiczki.",
     [("buty", "rawng tháo", "รองเท้า"), ("skarpetki", "thǔng tháo", "ถุงเท้า"),
      ("pałeczki", "tà-kìap", "ตะเกียบ"), ("rękawiczki", "thǔng mue", "ถุงมือ")],
     [("Poproszę jedną parę pałeczek.", "khǎw tà-kìap nùeng khûu", "ขอตะเกียบหนึ่งคู่"),
      ("Dwie pary butów.", "rawng tháo sǎwng khûu", "รองเท้าสองคู่")]),

    # --------------------------------------------------- naczynia i porcje
    ("kâew", "แก้ว", "Survival",
     "Napoje podawane w szklance. Uwaga: samo naczynie liczy się przez `bai`, "
     "a napój w naczyniu — przez `kâew`.",
     [("woda", "náam", "น้ำ"), ("piwo", "bia", "เบียร์"), ("sok", "náam phǒn-lá-mái", "น้ำผลไม้")],
     [("Poproszę dwie szklanki wody.", "khǎw náam sǎwng kâew", "ขอน้ำสองแก้ว"),
      ("Jedno piwo.", "bia nùeng kâew", "เบียร์หนึ่งแก้ว")]),

    ("khùat", "ขวด", "Survival",
     "Butelki: woda, piwo, sos, lekarstwo w płynie.",
     [("woda butelkowana", "náam plào", "น้ำเปล่า"), ("piwo", "bia", "เบียร์"),
      ("sos rybny", "náam plaa", "น้ำปลา")],
     [("Poproszę dwie butelki wody.", "khǎw náam plào sǎwng khùat", "ขอน้ำเปล่าสองขวด"),
      ("Ile kosztuje butelka?", "khùat lá thâo-rài", "ขวดละเท่าไหร่")]),

    ("thûai", "ถ้วย", "A1",
     "Filiżanki i czarki: kawa, herbata, deser w miseczce.",
     [("kawa", "kaa-fae", "กาแฟ"), ("herbata", "chaa", "ชา")],
     [("Poproszę dwie kawy.", "khǎw kaa-fae sǎwng thûai", "ขอกาแฟสองถ้วย"),
      ("Jedna herbata.", "chaa nùeng thûai", "ชาหนึ่งถ้วย")]),

    ("chaam", "ชาม", "A1",
     "Miski: zupa, makaron w rosole, ryż w misce.",
     [("makaron w rosole", "kǔai-tǐao", "ก๋วยเตี๋ยว"), ("zupa", "súp", "ซุป")],
     [("Poproszę jedną miskę makaronu.", "khǎw kǔai-tǐao nùeng chaam", "ขอก๋วยเตี๋ยวหนึ่งชาม"),
      ("Dwie miski.", "sǎwng chaam", "สองชาม")]),

    ("jaan", "จาน", "Survival",
     "Dania podawane na talerzu. Sam talerz jako przedmiot liczy się przez `bai`.",
     [("ryż smażony", "khâo phàt", "ข้าวผัด"), ("pad thai", "phàt thai", "ผัดไทย"),
      ("danie", "aa-hǎan", "อาหาร")],
     [("Poproszę dwa ryże smażone.", "khǎw khâo phàt sǎwng jaan", "ขอข้าวผัดสองจาน"),
      ("Jedno danie.", "nùeng jaan", "หนึ่งจาน")]),

    ("múue", "มื้อ", "A2",
     "Posiłki jako pory jedzenia: śniadanie, obiad, kolacja.",
     [("posiłek", "aa-hǎan", "อาหาร")],
     [("Trzy posiłki dziennie.", "wan lá sǎam múue", "วันละสามมื้อ"),
      ("Jeden posiłek.", "nùeng múue", "หนึ่งมื้อ")]),

    ("thîi", "ที่", "A1",
     "Porcje i miejsca siedzące: porcja dania, miejsce w restauracji lub w kinie.",
     [("porcja", "thîi", "ที่"), ("miejsce", "thîi nâng", "ที่นั่ง")],
     [("Poproszę dwie porcje.", "khǎw sǎwng thîi", "ขอสองที่"),
      ("Stolik dla czterech osób.", "tó sǎm-ràp sìi thîi", "โต๊ะสำหรับสี่ที่")]),

    ("lǒot", "หลอด", "A2",
     "Rzeczy w tubkach i rurkach: pasta do zębów, słomka, świetlówka.",
     [("pasta do zębów", "yaa sǐi fan", "ยาสีฟัน"), ("słomka", "làwt", "หลอด")],
     [("Poproszę jedną słomkę.", "khǎw làwt nùeng lǒot", "ขอหลอดหนึ่งหลอด"),
      ("Dwie tubki pasty.", "yaa sǐi fan sǎwng lǒot", "ยาสีฟันสองหลอด")]),

    ("krà-pǎwng", "กระป๋อง", "A2",
     "Puszki: napój w puszce, konserwa.",
     [("napój gazowany", "náam àt lom", "น้ำอัดลม"), ("konserwa", "aa-hǎan krà-pǎwng", "อาหารกระป๋อง")],
     [("Dwie puszki.", "sǎwng krà-pǎwng", "สองกระป๋อง"),
      ("Poproszę puszkę coli.", "khǎw khóok nùeng krà-pǎwng", "ขอโค้กหนึ่งกระป๋อง")]),

    ("hàw", "ห่อ", "A2",
     "Rzeczy zawinięte w papier lub liść: jedzenie na wynos, paczuszka.",
     [("jedzenie na wynos", "aa-hǎan klàp bâan", "อาหารกลับบ้าน")],
     [("Poproszę dwie paczki.", "khǎw sǎwng hàw", "ขอสองห่อ"),
      ("Jedno na wynos.", "nùeng hàw", "หนึ่งห่อ")]),

    ("thǔng", "ถุง", "A1",
     "Zawartość torebki: ryż w torebce, lód w woreczku, zakupy w reklamówce.",
     [("torebka", "thǔng", "ถุง"), ("lód", "náam khǎeng", "น้ำแข็ง")],
     [("Poproszę dwie torebki.", "khǎw sǎwng thǔng", "ขอสองถุง"),
      ("Jedna torebka lodu.", "náam khǎeng nùeng thǔng", "น้ำแข็งหนึ่งถุง")]),

    ("klàwng", "กล่อง", "A1",
     "Pudełka i kartony: pudełko, karton mleka, opakowanie zbiorcze.",
     [("pudełko", "klàwng", "กล่อง"), ("mleko", "nom", "นม")],
     [("Dwa pudełka.", "sǎwng klàwng", "สองกล่อง"),
      ("Poproszę karton mleka.", "khǎw nom nùeng klàwng", "ขอนมหนึ่งกล่อง")]),

    ("sàwng", "ซอง", "A2",
     "Koperty i saszetki: list, saszetka kawy, opakowanie proszku.",
     [("koperta", "sawng", "ซอง"), ("saszetka", "sawng", "ซอง")],
     [("Dwie koperty.", "sǎwng sàwng", "สองซอง"),
      ("Poproszę jedną saszetkę.", "khǎw nùeng sàwng", "ขอหนึ่งซอง")]),

    ("lang", "ลัง", "B1",
     "Skrzynki i kartony zbiorcze: skrzynka piwa, karton towaru.",
     [("skrzynka", "lang", "ลัง")],
     [("Dwie skrzynki.", "sǎwng lang", "สองลัง"),
      ("Skrzynka piwa.", "bia nùeng lang", "เบียร์หนึ่งลัง")]),

    ("thǎng", "ถัง", "B1",
     "Wiadra, beczki, zbiorniki: wiadro wody, butla gazu.",
     [("wiadro", "thǎng", "ถัง"), ("butla gazu", "thǎng kháet", "ถังแก๊ส")],
     [("Dwa wiadra.", "sǎwng thǎng", "สองถัง"),
      ("Jedna butla gazu.", "kháet nùeng thǎng", "แก๊สหนึ่งถัง")]),

    ("mûan", "ม้วน", "B1",
     "Rzeczy zwinięte w rolkę: papier toaletowy, taśma, film.",
     [("papier toaletowy", "kràdàat cham-rá", "กระดาษชำระ"), ("taśma", "théep", "เทป")],
     [("Dwie rolki.", "sǎwng mûan", "สองม้วน"),
      ("Poproszę rolkę papieru.", "khǎw kràdàat cham-rá nùeng mûan", "ขอกระดาษชำระหนึ่งม้วน")]),

    ("thâeng", "แท่ง", "B1",
     "Sztabki i pałeczki: czekolada, ołówek, kreda.",
     [("czekolada", "cháwk-koo-lét", "ช็อกโกแลต"), ("ołówek", "din-sǎw", "ดินสอ")],
     [("Dwie tabliczki czekolady.", "cháwk-koo-lét sǎwng thâeng", "ช็อกโกแลตสองแท่ง"),
      ("Jeden ołówek.", "din-sǎw nùeng thâeng", "ดินสอหนึ่งแท่ง")]),

    ("dâam", "ด้าม", "B1",
     "Przedmioty z rączką: długopis, młotek, parasol składany.",
     [("długopis", "pàak-kaa", "ปากกา")],
     [("Dwa długopisy.", "pàak-kaa sǎwng dâam", "ปากกาสองด้าม"),
      ("Poproszę jeden długopis.", "khǎw pàak-kaa nùeng dâam", "ขอปากกาหนึ่งด้าม")]),

    ("muan", "มวน", "B1",
     "Papierosy i skręty.",
     [("papieros", "bù-rìi", "บุหรี่")],
     [("Dwa papierosy.", "bù-rìi sǎwng muan", "บุหรี่สองมวน"),
      ("Jeden papieros.", "bù-rìi nùeng muan", "บุหรี่หนึ่งมวน")]),

    ("krà-bàwk", "กระบอก", "B1",
     "Przedmioty w kształcie rury: bambusowy pojemnik, strzykawka, lufa.",
     [("strzykawka", "khěm chìit", "เข็มฉีด")],
     [("Dwie sztuki.", "sǎwng krà-bàwk", "สองกระบอก"),
      ("Jedna strzykawka.", "khěm chìit nùeng krà-bàwk", "เข็มฉีดหนึ่งกระบอก")]),

    # ------------------------------------------------------ książki i ostrza
    ("lêm", "เล่ม", "A1",
     "Książki, zeszyty, karta dań w formie książeczki — a także noże i inne "
     "przedmioty z ostrzem oraz świece i igły.",
     [("książka", "nǎng-sǔe", "หนังสือ"), ("zeszyt", "sà-mùt", "สมุด"),
      ("nóż", "mîit", "มีด"), ("karta dań", "mee-nuu", "เมนู"),
      ("świeca", "thian", "เทียน"), ("igła", "khěm", "เข็ม")],
     [("Poproszę jeszcze jedną kartę dań.", "khǎw mee-nuu ìik lêm nùeng", "ขอเมนูอีกเล่มหนึ่ง"),
      ("Dwie książki.", "nǎng-sǔe sǎwng lêm", "หนังสือสองเล่ม")]),

    ("chà-bàp", "ฉบับ", "B1",
     "Egzemplarze pism: list, gazeta, dokument urzędowy, wydanie.",
     [("list", "jòt mǎai", "จดหมาย"), ("gazeta", "nǎng-sǔe phim", "หนังสือพิมพ์"),
      ("dokument", "èek-kà-sǎan", "เอกสาร")],
     [("Dwa listy.", "jòt mǎai sǎwng chà-bàp", "จดหมายสองฉบับ"),
      ("Jeden dokument.", "èek-kà-sǎan nùeng chà-bàp", "เอกสารหนึ่งฉบับ")]),

    ("nâa", "หน้า", "A2",
     "Strony w książce lub dokumencie.",
     [("strona", "nâa", "หน้า")],
     [("Dwie strony.", "sǎwng nâa", "สองหน้า"),
      ("Strona dziesiąta.", "nâa thîi sìp", "หน้าที่สิบ")]),

    ("bòt", "บท", "B1",
     "Rozdziały, lekcje, akty w sztuce.",
     [("rozdział", "bòt", "บท"), ("lekcja", "bòt rian", "บทเรียน")],
     [("Dwa rozdziały.", "sǎwng bòt", "สองบท"),
      ("Lekcja piąta.", "bòt thîi hâa", "บทที่ห้า")]),

    ("rûeang", "เรื่อง", "A2",
     "Sprawy, historie, filmy — wszystko, co ma treść i przebieg.",
     [("film", "nǎng", "หนัง"), ("sprawa", "rûeang", "เรื่อง")],
     [("Dwa filmy.", "nǎng sǎwng rûeang", "หนังสองเรื่อง"),
      ("Mam jedną sprawę.", "mii rûeang nùeng rûeang", "มีเรื่องหนึ่งเรื่อง")]),

    ("kham", "คำ", "A2",
     "Słowa, a także kęsy jedzenia.",
     [("słowo", "kham", "คำ")],
     [("Dwa słowa.", "sǎwng kham", "สองคำ"),
      ("Jeden kęs.", "nùeng kham", "หนึ่งคำ")]),

    ("prà-yòok", "ประโยค", "B1",
     "Zdania.",
     [("zdanie", "prà-yòok", "ประโยค")],
     [("Dwa zdania.", "sǎwng prà-yòok", "สองประโยค"),
      ("Powtórz jedno zdanie.", "phûut ìik nùeng prà-yòok", "พูดอีกหนึ่งประโยค")]),

    # ------------------------------------------------------------- pojazdy
    ("khan", "คัน", "A1",
     "Pojazdy kołowe i przedmioty z trzonkiem: samochód, motocykl, rower, "
     "a także parasol, łyżka, widelec i wędka.",
     [("samochód", "rót yon", "รถยนต์"), ("motocykl", "maw-təə-sai", "มอเตอร์ไซค์"),
      ("rower", "jàk-krà-yaan", "จักรยาน"), ("parasol", "rôm", "ร่ม"),
      ("łyżka", "cháwn", "ช้อน"), ("widelec", "sâwm", "ส้อม")],
     [("Poproszę jeszcze jedną łyżkę.", "khǎw cháwn ìik khan nùeng", "ขอช้อนอีกคันหนึ่ง"),
      ("Zderzyły się dwa motocykle.", "maw-təə-sai chon kan sǎwng khan", "มอเตอร์ไซค์ชนกันสองคัน")]),

    ("lam", "ลำ", "B1",
     "Łodzie i samoloty.",
     [("łódź", "ruea", "เรือ"), ("samolot", "khrûeang bin", "เครื่องบิน")],
     [("Dwie łodzie.", "ruea sǎwng lam", "เรือสองลำ"),
      ("Jeden samolot.", "khrûeang bin nùeng lam", "เครื่องบินหนึ่งลำ")]),

    ("khà-buan", "ขบวน", "B1",
     "Pociągi i pochody — wszystko, co jedzie albo idzie w składzie.",
     [("pociąg", "rót fai", "รถไฟ")],
     [("Dwa pociągi.", "rót fai sǎwng khà-buan", "รถไฟสองขบวน"),
      ("Następny pociąg.", "khà-buan tàw pai", "ขบวนต่อไป")]),

    ("sǎai", "สาย", "A2",
     "Linie i rzeczy długie jak sznur: linia autobusowa, droga, rzeka, kabel, pasek.",
     [("linia autobusowa", "rót mee", "รถเมล์"), ("droga", "thà-nǒn", "ถนน"),
      ("rzeka", "mâe náam", "แม่น้ำ"), ("kabel", "sǎai fai", "สายไฟ")],
     [("Która linia?", "sǎai nǎi", "สายไหน"),
      ("Dwie linie autobusowe.", "rót mee sǎwng sǎai", "รถเมล์สองสาย")]),

    ("khrûeang", "เครื่อง", "A2",
     "Maszyny i urządzenia: pralka, lodówka, klimatyzator, komputer.",
     [("pralka", "khrûeang sák phâa", "เครื่องซักผ้า"),
      ("klimatyzacja", "aae", "แอร์"), ("lodówka", "tûu yen", "ตู้เย็น"),
      ("komputer", "khawm-phíu-tôe", "คอมพิวเตอร์")],
     [("Dwie pralki.", "khrûeang sák phâa sǎwng khrûeang", "เครื่องซักผ้าสองเครื่อง"),
      ("Jeden klimatyzator.", "aae nùeng khrûeang", "แอร์หนึ่งเครื่อง")]),

    # ------------------------------------------------------ budynki i miejsca
    ("lǎng", "หลัง", "A1",
     "Budynki i to, co ma dach: dom, hotel, moskitiera.",
     [("dom", "bâan", "บ้าน"), ("hotel", "roong raem", "โรงแรม"),
      ("moskitiera", "múng", "มุ้ง")],
     [("Dwa domy.", "bâan sǎwng lǎng", "บ้านสองหลัง"),
      ("Jeden hotel.", "roong raem nùeng lǎng", "โรงแรมหนึ่งหลัง")]),

    ("hâwng", "ห้อง", "Survival",
     "Pokoje i pomieszczenia.",
     [("pokój", "hâwng", "ห้อง"), ("łazienka", "hâwng náam", "ห้องน้ำ")],
     [("Poproszę dwa pokoje.", "khǎw hâwng sǎwng hâwng", "ขอห้องสองห้อง"),
      ("Jeden pokój na dwie noce.", "hâwng nùeng hâwng sǎwng khuen", "ห้องหนึ่งห้องสองคืน")]),

    ("chán", "ชั้น", "A1",
     "Piętra, warstwy, klasy w szkole.",
     [("piętro", "chán", "ชั้น")],
     [("Drugie piętro.", "chán sǎwng", "ชั้นสอง"),
      ("Dwa piętra.", "sǎwng chán", "สองชั้น")]),

    ("hàeng", "แห่ง", "B1",
     "Miejsca i placówki w rejestrze oficjalnym: oddział banku, urząd, szpital.",
     [("oddział", "sǎa-khǎa", "สาขา"), ("urząd", "nùai ngaan", "หน่วยงาน")],
     [("Dwa oddziały.", "sǎa-khǎa sǎwng hàeng", "สาขาสองแห่ง"),
      ("Jedno miejsce.", "nùeng hàeng", "หนึ่งแห่ง")]),

    ("jùt", "จุด", "B1",
     "Punkty na mapie i w tekście: punkt kontrolny, punkt programu.",
     [("punkt", "jùt", "จุด")],
     [("Dwa punkty.", "sǎwng jùt", "สองจุด"),
      ("Punkt spotkania.", "jùt nát phóp", "จุดนัดพบ")]),

    ("thǎew", "แถว", "A2",
     "Rzędy i szeregi: rząd krzeseł, rząd domów, kolejka.",
     [("rząd", "thǎew", "แถว")],
     [("Drugi rząd.", "thǎew thîi sǎwng", "แถวที่สอง"),
      ("Dwa rzędy.", "sǎwng thǎew", "สองแถว")]),

    # -------------------------------------------------------- rośliny i owoce
    ("tôn", "ต้น", "A1",
     "Rośliny stojące pionowo: drzewo, krzew, roślina doniczkowa, słup.",
     [("drzewo", "tôn mái", "ต้นไม้"), ("roślina", "tôn mái", "ต้นไม้")],
     [("Dwa drzewa.", "tôn mái sǎwng tôn", "ต้นไม้สองต้น"),
      ("Jedno drzewo.", "tôn mái nùeng tôn", "ต้นไม้หนึ่งต้น")]),

    ("lûuk", "ลูก", "A1",
     "Rzeczy okrągłe: owoce, piłki, góry, a potocznie także dzieci.",
     [("mango", "má-mûang", "มะม่วง"), ("pomarańcza", "sôm", "ส้ม"),
      ("piłka", "lûuk bawn", "ลูกบอล"), ("jajko", "khài", "ไข่")],
     [("Dwa mango.", "má-mûang sǎwng lûuk", "มะม่วงสองลูก"),
      ("Poproszę trzy pomarańcze.", "khǎw sôm sǎam lûuk", "ขอส้มสามลูก")]),

    ("phǒn", "ผล", "B2",
     "Owoce w rejestrze pisanym i urzędowym. W mowie codziennej używa się `lûuk`.",
     [("owoc", "phǒn-lá-mái", "ผลไม้")],
     [("Dwa owoce.", "phǒn-lá-mái sǎwng phǒn", "ผลไม้สองผล"),
      ("Jeden owoc.", "nùeng phǒn", "หนึ่งผล")]),

    ("fawng", "ฟอง", "A1",
     "Jajka i bańki.",
     [("jajko", "khài", "ไข่")],
     [("Dwa jajka.", "khài sǎwng fawng", "ไข่สองฟอง"),
      ("Poproszę pięć jajek.", "khǎw khài hâa fawng", "ขอไข่ห้าฟอง")]),

    ("dàwk", "ดอก", "A1",
     "Kwiaty, klucze, kadzidełka i strzały — rzeczy o wąskim trzonie.",
     [("kwiat", "dàwk mái", "ดอกไม้"), ("klucz", "kunjae", "กุญแจ"),
      ("kadzidełko", "thûup", "ธูป")],
     [("Poproszę jeszcze jeden klucz.", "khǎw kunjae ìik dàwk nùeng", "ขอกุญแจอีกดอกหนึ่ง"),
      ("Ile jest kluczy?", "mii kunjae kìi dàwk", "มีกุญแจกี่ดอก")]),

    ("kìng", "กิ่ง", "B1",
     "Gałęzie.",
     [("gałąź", "kìng mái", "กิ่งไม้")],
     [("Dwie gałęzie.", "kìng mái sǎwng kìng", "กิ่งไม้สองกิ่ง"),
      ("Jedna gałąź.", "nùeng kìng", "หนึ่งกิ่ง")]),

    ("phuang", "พวง", "B1",
     "Grona i pęki: winogrona, pęk kluczy, girlanda kwiatów.",
     [("winogrona", "à-ngùn", "องุ่น"), ("girlanda", "phuang maa-lai", "พวงมาลัย")],
     [("Dwie kiście winogron.", "à-ngùn sǎwng phuang", "องุ่นสองพวง"),
      ("Jedna girlanda.", "phuang maa-lai nùeng phuang", "พวงมาลัยหนึ่งพวง")]),

    ("châw", "ช่อ", "B1",
     "Bukiety i kiście kwiatów.",
     [("bukiet", "châw dàwk mái", "ช่อดอกไม้")],
     [("Dwa bukiety.", "sǎwng châw", "สองช่อ"),
      ("Poproszę jeden bukiet.", "khǎw nùeng châw", "ขอหนึ่งช่อ")]),

    ("hǔa", "หัว", "A2",
     "Bulwy i główki: czosnek, cebula, kapusta.",
     [("czosnek", "krà-thiam", "กระเทียม"), ("cebula", "hǔa hǎwm", "หัวหอม")],
     [("Dwie główki czosnku.", "krà-thiam sǎwng hǔa", "กระเทียมสองหัว"),
      ("Jedna cebula.", "hǔa hǎwm nùeng hǔa", "หัวหอมหนึ่งหัว")]),

    ("sên", "เส้น", "A1",
     "Rzeczy długie i cienkie: makaron, włos, sznurek, naszyjnik.",
     [("makaron", "sên", "เส้น"), ("włos", "phǒm", "ผม"),
      ("naszyjnik", "sɔ̂i khaw", "สร้อยคอ")],
     [("Dwie porcje makaronu.", "sên sǎwng sên", "เส้นสองเส้น"),
      ("Jeden włos.", "phǒm nùeng sên", "ผมหนึ่งเส้น")]),

    ("mát", "มัด", "B1",
     "Wiązki i pęczki: pęczek warzyw, wiązka drewna.",
     [("pęczek", "mát", "มัด")],
     [("Dwa pęczki.", "sǎwng mát", "สองมัด"),
      ("Poproszę jeden pęczek.", "khǎw nùeng mát", "ขอหนึ่งมัด")]),

    ("kam", "กำ", "B1",
     "Garście: garść ziół, garść ryżu.",
     [("garść", "kam", "กำ")],
     [("Dwie garście.", "sǎwng kam", "สองกำ"),
      ("Jedna garść.", "nùeng kam", "หนึ่งกำ")]),

    ("kawng", "กอง", "B1",
     "Sterty i stosy: sterta ubrań, stos papierów.",
     [("sterta", "kawng", "กอง")],
     [("Dwie sterty.", "sǎwng kawng", "สองกอง"),
      ("Jeden stos.", "nùeng kawng", "หนึ่งกอง")]),

    # ---------------------------------------------------- zwierzęta w grupach
    ("fǔung", "ฝูง", "B1",
     "Stada i ławice: stado ptaków, ławica ryb.",
     [("stado", "fǔung", "ฝูง")],
     [("Dwa stada.", "sǎwng fǔung", "สองฝูง"),
      ("Stado ptaków.", "fǔung nók", "ฝูงนก")]),

    ("klùm", "กลุ่ม", "A2",
     "Grupy ludzi i rzeczy.",
     [("grupa", "klùm", "กลุ่ม")],
     [("Dwie grupy.", "sǎwng klùm", "สองกลุ่ม"),
      ("Grupa turystów.", "klùm nák thâwng thîao", "กลุ่มนักท่องเที่ยว")]),

    ("wong", "วง", "B1",
     "Kręgi i zespoły: zespół muzyczny, pierścionek, koło.",
     [("zespół", "wong don-trii", "วงดนตรี"), ("pierścionek", "wǎaen", "แหวน")],
     [("Dwa zespoły.", "wong don-trii sǎwng wong", "วงดนตรีสองวง"),
      ("Jeden pierścionek.", "wǎaen nùeng wong", "แหวนหนึ่งวง")]),

    # ------------------------------------------------------------ zdarzenia
    ("khráng", "ครั้ง", "A1",
     "Razy i okazje: ile razy coś się wydarzyło.",
     [("raz", "khráng", "ครั้ง")],
     [("Dwa razy.", "sǎwng khráng", "สองครั้ง"),
      ("Pierwszy raz.", "khráng râek", "ครั้งแรก")]),

    ("thîao", "เที่ยว", "A2",
     "Kursy i rejsy: kurs autobusu, lot, wyjazd.",
     [("kurs", "thîao", "เที่ยว"), ("lot", "thîao bin", "เที่ยวบิน")],
     [("Dwa kursy dziennie.", "wan lá sǎwng thîao", "วันละสองเที่ยว"),
      ("Następny kurs.", "thîao tàw pai", "เที่ยวต่อไป")]),

    ("rawp", "รอบ", "A2",
     "Seanse, okrążenia, tury: seans w kinie, runda.",
     [("seans", "rawp", "รอบ")],
     [("Dwa seanse.", "sǎwng rawp", "สองรอบ"),
      ("Seans o siódmej.", "rawp jèt moong", "รอบเจ็ดโมง")]),

    ("nát", "นัด", "B1",
     "Spotkania umówione oraz mecze.",
     [("spotkanie", "nát", "นัด"), ("mecz", "kaan khàeng khǎn", "การแข่งขัน")],
     [("Dwa spotkania.", "sǎwng nát", "สองนัด"),
      ("Mam jedno spotkanie.", "mii nát nùeng nát", "มีนัดหนึ่งนัด")]),

    # ----------------------------------------------------------- rodzaje
    ("yàang", "อย่าง", "A1",
     "Rodzaje i sposoby: ile rodzajów, na ile sposobów.",
     [("rodzaj", "yàang", "อย่าง")],
     [("Dwa rodzaje.", "sǎwng yàang", "สองอย่าง"),
      ("Poproszę trzy rodzaje.", "khǎw sǎam yàang", "ขอสามอย่าง")]),

    ("chá-nít", "ชนิด", "B1",
     "Gatunki i odmiany w opisie technicznym.",
     [("gatunek", "chá-nít", "ชนิด")],
     [("Dwa gatunki.", "sǎwng chá-nít", "สองชนิด"),
      ("Jeden gatunek.", "nùeng chá-nít", "หนึ่งชนิด")]),

    ("prà-phêet", "ประเภท", "B1",
     "Kategorie i typy w klasyfikacji.",
     [("kategoria", "prà-phêet", "ประเภท")],
     [("Dwie kategorie.", "sǎwng prà-phêet", "สองประเภท"),
      ("Jaka kategoria?", "prà-phêet nǎi", "ประเภทไหน")]),

    # ------------------------------------------------------------ jednostki
    ("bàat", "บาท", "Survival",
     "Baht — waluta tajska. W liczeniu zachowuje się jak klasyfikator.",
     [("baht", "bàat", "บาท")],
     [("Sto bahtów.", "nùeng ráwi bàat", "หนึ่งร้อยบาท"),
      ("Ile to kosztuje?", "thâo-rài", "เท่าไหร่")]),

    ("sà-taang", "สตางค์", "A2",
     "Satang — jedna setna bahta. W obiegu rzadka, ale pojawia się w cenach.",
     [("satang", "sà-taang", "สตางค์")],
     [("Pięćdziesiąt satangów.", "hâa-sìp sà-taang", "ห้าสิบสตางค์"),
      ("Dwadzieścia pięć satangów.", "yîi-sìp hâa sà-taang", "ยี่สิบห้าสตางค์")]),

    ("chûa-moong", "ชั่วโมง", "Survival",
     "Godziny jako czas trwania.",
     [("godzina", "chûa-moong", "ชั่วโมง")],
     [("Dwie godziny.", "sǎwng chûa-moong", "สองชั่วโมง"),
      ("Za godzinę.", "ìik nùeng chûa-moong", "อีกหนึ่งชั่วโมง")]),

    ("naa-thii", "นาที", "Survival",
     "Minuty.",
     [("minuta", "naa-thii", "นาที")],
     [("Pięć minut.", "hâa naa-thii", "ห้านาที"),
      ("Za dziesięć minut.", "ìik sìp naa-thii", "อีกสิบนาที")]),

    ("wan", "วัน", "Survival",
     "Dni.",
     [("dzień", "wan", "วัน")],
     [("Trzy dni.", "sǎam wan", "สามวัน"),
      ("Za dwa dni.", "ìik sǎwng wan", "อีกสองวัน")]),

    ("khuen", "คืน", "Survival",
     "Noce — jednostka rozliczeniowa w hotelu.",
     [("noc", "khuen", "คืน")],
     [("Dwie noce.", "sǎwng khuen", "สองคืน"),
      ("Poproszę pokój na trzy noce.", "khǎw hâwng sǎam khuen", "ขอห้องสามคืน")]),

    ("aa-thít", "อาทิตย์", "A1",
     "Tygodnie.",
     [("tydzień", "aa-thít", "อาทิตย์")],
     [("Dwa tygodnie.", "sǎwng aa-thít", "สองอาทิตย์"),
      ("Za tydzień.", "ìik nùeng aa-thít", "อีกหนึ่งอาทิตย์")]),

    ("duean", "เดือน", "A1",
     "Miesiące.",
     [("miesiąc", "duean", "เดือน")],
     [("Trzy miesiące.", "sǎam duean", "สามเดือน"),
      ("Za miesiąc.", "ìik nùeng duean", "อีกหนึ่งเดือน")]),

    ("pii", "ปี", "A1",
     "Lata.",
     [("rok", "pii", "ปี")],
     [("Dwa lata.", "sǎwng pii", "สองปี"),
      ("Mam trzydzieści lat.", "aa-yú sǎam-sìp pii", "อายุสามสิบปี")]),

    ("kì-loo", "กิโล", "A1",
     "Kilogramy — skrót od `kì-loo-kram`, w mowie codziennej używany zawsze.",
     [("kilogram", "kì-loo", "กิโล")],
     [("Dwa kilo.", "sǎwng kì-loo", "สองกิโล"),
      ("Ile za kilo?", "kì-loo lá thâo-rài", "กิโลละเท่าไหร่")]),

    ("khìit", "ขีด", "A2",
     "Sto gramów — jednostka używana na targu.",
     [("sto gramów", "khìit", "ขีด")],
     [("Dwie sztuki po sto gramów.", "sǎwng khìit", "สองขีด"),
      ("Poproszę trzysta gramów.", "khǎw sǎam khìit", "ขอสามขีด")]),

    ("lít", "ลิตร", "A2",
     "Litry.",
     [("litr", "lít", "ลิตร")],
     [("Dwa litry.", "sǎwng lít", "สองลิตร"),
      ("Jeden litr.", "nùeng lít", "หนึ่งลิตร")]),

    ("méet", "เมตร", "A2",
     "Metry.",
     [("metr", "méet", "เมตร")],
     [("Dwa metry.", "sǎwng méet", "สองเมตร"),
      ("Sto metrów.", "nùeng ráwi méet", "หนึ่งร้อยเมตร")]),

    ("kì-loo-méet", "กิโลเมตร", "A2",
     "Kilometry.",
     [("kilometr", "kì-loo-méet", "กิโลเมตร")],
     [("Dwa kilometry.", "sǎwng kì-loo-méet", "สองกิโลเมตร"),
      ("Ile kilometrów?", "kìi kì-loo-méet", "กี่กิโลเมตร")]),

    ("níu", "นิ้ว", "B1",
     "Cale — używane przy rozmiarach ekranów i rur.",
     [("cal", "níu", "นิ้ว")],
     [("Dwa cale.", "sǎwng níu", "สองนิ้ว"),
      ("Ekran trzydziestocalowy.", "jaw sǎam-sìp níu", "จอสามสิบนิ้ว")]),

    ("rái", "ไร่", "B2",
     "Rai — tajska miara powierzchni gruntu, 1 600 metrów kwadratowych.",
     [("rai", "rái", "ไร่")],
     [("Dwa rai.", "sǎwng rái", "สองไร่"),
      ("Działka o powierzchni jednego rai.", "thîi din nùeng rái", "ที่ดินหนึ่งไร่")]),

    ("taa-raang-méet", "ตารางเมตร", "B1",
     "Metry kwadratowe — przy wynajmie mieszkania.",
     [("metr kwadratowy", "taa-raang-méet", "ตารางเมตร")],
     [("Trzydzieści metrów kwadratowych.", "sǎam-sìp taa-raang-méet", "สามสิบตารางเมตร"),
      ("Ile metrów kwadratowych?", "kìi taa-raang-méet", "กี่ตารางเมตร")]),

    ("duang", "ดวง", "B1",
     "Ciała niebieskie, światła, znaczki pocztowe, pieczęcie, serce.",
     [("gwiazda", "daaw", "ดาว"), ("znaczek", "sà-taem", "แสตมป์"),
      ("słońce", "phrá aa-thít", "พระอาทิตย์")],
     [("Dwa znaczki.", "sà-taem sǎwng duang", "แสตมป์สองดวง"),
      ("Jedna gwiazda.", "daaw nùeng duang", "ดาวหนึ่งดวง")]),
]

# ---------------------------------------------------------------------------
# Klasyfikatory pomocnicze — bez własnej listy rzeczowników, ale spotykane
# w mowie. Wchodzą do `data/classifiers.json` jako pełnoprawne rekordy.
# ---------------------------------------------------------------------------
EXTRA = [
    ("khaan", "ขัน", "B2", "Czerpaki i miski do wody w łazience.", "czerpak", "khǎn", "ขัน"),
    ("bai lá", "ใบละ", "A2", "Cena za sztukę liczona przez `bai`.", "sztuka", "bai", "ใบ"),
    ("pàek", "แพ็ก", "A2", "Zgrzewki i wielopaki towaru.", "zgrzewka", "pàek", "แพ็ก"),
    ("khûu lá", "คู่ละ", "A2", "Cena za parę.", "para", "khûu", "คู่"),
    ("hìip", "หีบ", "B2", "Kufry i skrzynie zamykane wiekiem.", "kufer", "hìip", "หีบ"),
    ("ohng", "โอ่ง", "B2", "Gliniane zbiorniki na wodę deszczową.", "zbiornik", "ohng", "โอ่ง"),
    ("krà-thǎwm", "กระท่อม", "B2", "Chaty i szałasy liczone jako budowle.", "chata", "krà-thǎwm", "กระท่อม"),
    ("phǎen", "แผน", "B2", "Plany i projekty jako dokumenty.", "plan", "phǎen", "แผน"),
    ("chút khâo", "ชุดข้าว", "B2", "Zestawy obiadowe w restauracji.", "zestaw obiadowy", "chút khâo", "ชุดข้าว"),
    ("sà-lâak", "สลาก", "B2", "Losy loteryjne.", "los", "sà-lâak", "สลาก"),
    ("bai sèt", "ใบเสร็จ", "A2", "Paragony i rachunki liczone przez `bai`.", "paragon", "bai sèt", "ใบเสร็จ"),
    ("pàak", "ปาก", "B2", "Sieci rybackie i studnie.", "sieć", "hàae", "แห"),
    ("lam tân", "ลำต้น", "B2", "Pnie roślin w opisie botanicznym.", "pień", "lam tân", "ลำต้น"),
    ("khà-nàat", "ขนาด", "B1", "Rozmiary jako pozycje w tabeli.", "rozmiar", "khà-nàat", "ขนาด"),
    ("rûun", "รุ่น", "B1", "Modele i roczniki sprzętu.", "model", "rûun", "รุ่น"),
    ("sǐi", "สี", "A2", "Kolory jako pozycje wyboru.", "kolor", "sǐi", "สี"),
    ("bàep", "แบบ", "A2", "Wzory i fasony.", "wzór", "bàep", "แบบ"),
    ("chán rian", "ชั้นเรียน", "B1", "Klasy szkolne jako grupy uczniów.", "klasa", "chán rian", "ชั้นเรียน"),
    ("khá-naen", "คะแนน", "B1", "Punkty w ocenianiu i w grze.", "punkt", "khá-naen", "คะแนน"),
    ("khâw", "ข้อ", "B1", "Punkty umowy, pytania w teście, stawy w ciele.", "punkt umowy", "khâw", "ข้อ"),
    ("mǔat", "หมวด", "B2", "Działy i sekcje w spisie.", "dział", "mǔat", "หมวด"),
    ("tawn", "ตอน", "A2", "Odcinki serialu i części opowieści.", "odcinek", "tawn", "ตอน"),
    ("phâak", "ภาค", "B2", "Części dzieła i regiony kraju.", "część", "phâak", "ภาค"),
    ("chút khâw sǎwp", "ชุดข้อสอบ", "B2", "Zestawy egzaminacyjne.", "zestaw zadań", "chút khâw sǎwp", "ชุดข้อสอบ"),
    ("thǎew thǎew", "แถวแถว", "B2", "Szeregi w układzie wojskowym.", "szereg", "thǎew", "แถว"),
    ("sǎai phan", "สายพันธุ์", "B2", "Odmiany i rasy.", "odmiana", "sǎai phan", "สายพันธุ์"),
    ("kàp khâo", "กับข้าว", "B1", "Dodatki do ryżu liczone jako pozycje menu.", "dodatek do ryżu", "kàp khâo", "กับข้าว"),
    ("jaan lék", "จานเล็ก", "B2", "Małe talerze jako porcje.", "mała porcja", "jaan lék", "จานเล็ก"),
    ("khem", "เข็ม", "B1", "Igły i wskazówki zegara.", "igła", "khěm", "เข็ม"),
    ("bai à-nú-yâat", "ใบอนุญาต", "B1", "Zezwolenia i licencje liczone przez `bai`.", "zezwolenie", "bai à-nú-yâat", "ใบอนุญาต"),
    ("khan rôm", "คันร่ม", "B2", "Parasole liczone przez `khan`.", "parasol", "rôm", "ร่ม"),
    ("tua nǎng-sǔe", "ตัวหนังสือ", "B1", "Litery i znaki pisma.", "litera", "tua nǎng-sǔe", "ตัวหนังสือ"),
    ("khon ngaan", "คนงาน", "B1", "Pracownicy fizyczni liczeni przez `khon`.", "pracownik", "khon ngaan", "คนงาน"),
    ("thîi nâng", "ที่นั่ง", "A2", "Miejsca siedzące w pojeździe i w sali.", "miejsce siedzące", "thîi nâng", "ที่นั่ง"),
    ("chûai", "ช่วง", "B1", "Odcinki czasu i przedziały.", "przedział", "chûang", "ช่วง"),
    ("rá-yá", "ระยะ", "B1", "Etapy i odległości.", "etap", "rá-yá", "ระยะ"),
    ("khrâwp khrua", "ครอบครัว", "B1", "Rodziny jako jednostki spisu.", "rodzina", "khrâwp khrua", "ครอบครัว"),
    ("khon khàp", "คนขับ", "B1", "Kierowcy liczeni przez `khon`.", "kierowca", "khon khàp", "คนขับ"),
    ("tua yàang", "ตัวอย่าง", "A2", "Przykłady i próbki.", "przykład", "tua yàang", "ตัวอย่าง"),
    ("khà-nǒm", "ขนม", "B2", "Ciastka i słodycze liczone jako sztuki.", "ciastko", "khà-nǒm", "ขนม"),
    ("sà-thǎa-nii", "สถานี", "B1", "Stacje i przystanki.", "stacja", "sà-thǎa-nii", "สถานี"),
    ("pâai", "ป้าย", "A2", "Przystanki i tablice.", "przystanek", "pâai", "ป้าย"),
    ("dàan", "ด่าน", "B2", "Punkty kontrolne i przejścia graniczne.", "przejście graniczne", "dàan", "ด่าน"),
    ("chút pathǒm", "ชุดปฐมพยาบาล", "B2", "Zestawy pierwszej pomocy.", "apteczka", "chút pathǒm phá-yaa-baan", "ชุดปฐมพยาบาล"),
    ("bai sàng yaa", "ใบสั่งยา", "B1", "Recepty liczone przez `bai`.", "recepta", "bai sàng yaa", "ใบสั่งยา"),
    ("khráng khraaw", "ครั้งคราว", "B2", "Pojedyncze okazje.", "okazja", "khráng khraaw", "ครั้งคราว"),
]


# ---------------------------------------------------------------------------
# Odwzorowanie: pismo tajskie rzeczownika -> właściwy klasyfikator
# ---------------------------------------------------------------------------
def _build_noun_map():
    out = {}
    for entry in CLASSIFIERS:
        cls_ph, cls_th = entry[0], entry[1]
        for _pl, _ph, th in entry[4]:
            out.setdefault(th, (cls_ph, cls_th))
    return out


NOUN_TO_CLASSIFIER = _build_noun_map()

# Rzeczowniki, przy których baza używała `an`, a które mają własny klasyfikator.
# Klucz: pismo tajskie rzeczownika. Wartość: (fonetyka, pismo) klasyfikatora.
CORRECTIONS = {
    "ผ้าเช็ดตัว": ("phǔen", "ผืน"),          # ręcznik
    "ผ้าห่ม": ("phǔen", "ผืน"),               # koc
    "หมอน": ("bai", "ใบ"),                    # poduszka
    "กุญแจ": ("dàwk", "ดอก"),                 # klucz
    "จาน": ("bai", "ใบ"),                     # talerz
    "แก้ว": ("bai", "ใบ"),                    # szklanka
    "ช้อน": ("khan", "คัน"),                  # łyżka
    "ส้อม": ("khan", "คัน"),                  # widelec
    "มีด": ("lêm", "เล่ม"),                   # nóż
    "กระดาษเช็ดปาก": ("phàen", "แผ่น"),      # serwetka
    "เมนู": ("lêm", "เล่ม"),                  # karta dań
    "ตั๋ว": ("bai", "ใบ"),                    # bilet
    "หมวกกันน็อค": ("bai", "ใบ"),            # kask
    "แผนที่": ("bai", "ใบ"),                  # mapa
    "พลาสเตอร์": ("phàen", "แผ่น"),          # plaster
    "สบู่": ("kâwn", "ก้อน"),                 # mydło
    "ถุง": ("bai", "ใบ"),                     # torba
    "เสื้อยืด": ("tua", "ตัว"),                # koszulka
    "กางเกง": ("tua", "ตัว"),                  # spodnie
    "รองเท้า": ("khûu", "คู่"),                # buty
    "หมวก": ("bai", "ใบ"),                    # kapelusz
    "กระเป๋า": ("bai", "ใบ"),                 # torebka
    "ผ้าปูที่นอน": ("phǔen", "ผืน"),          # prześcieradło
    "หนังสือ": ("lêm", "เล่ม"),               # książka
    "ร่ม": ("khan", "คัน"),                   # parasol
    "ไข่": ("fawng", "ฟอง"),                  # jajko
    "ยา": ("mét", "เม็ด"),                    # tabletka
    "ดอกไม้": ("dàwk", "ดอก"),                # kwiat
    "เก้าอี้": ("tua", "ตัว"),                 # krzesło
    "โต๊ะ": ("tua", "ตัว"),                    # stół
}
