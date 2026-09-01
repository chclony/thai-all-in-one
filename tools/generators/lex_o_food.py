# -*- coding: utf-8 -*-
"""Sesja O, partia 4 — JEDZENIE: produkty, dania, smaki, sposoby przyrządzania.

Baza miała 155 haseł na jedzenie — dużo jak na rozmówki, mało jak na kraj,
w którym jedzenie jest głównym tematem small talku. „Kin khâao rǔe yang?”
(jadłeś już?) jest w Tajlandii tym, czym u nas „co słychać”.

Ta partia dokłada trzy warstwy, których brakowało:

1. **Produkty surowe** — warzywa, owoce, mięsa, przyprawy. Bez nich nie da
   się ani zrobić zakupów, ani powiedzieć, czego się nie je.
2. **Sposoby przyrządzenia** — `phàt` (smażone na patelni), `thâwt`
   (w głębokim tłuszczu), `nûeng` (na parze), `yâang` (z grilla), `tôm`
   (gotowane w wodzie). To one tworzą nazwy dań: khâo phàt, kài thâwt.
   Znając pięć czasowników i dwadzieścia produktów, uczący się odczytuje
   setki pozycji z karty.
3. **Zastrzeżenia** — bez orzeszków, bez cukru, mniej ostro. Warstwa
   praktyczna, przy alergii ratująca zdrowie.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

JN = "Jedzenie i napoje"
RE = "Restauracja"
ZP = "Zakupy i pieniądze"
ZD = "Zdrowie"
DC = "Dom i codzienność"
CO = "Cechy i opinie"
CZ = "Czasowniki"
PY = "Pytania"

FOOD = [

# =========================================================== warzywa
("A1", "marchewka", "kae-ràwt", "แครอท", "Warzywa", 3, "n", JN, "", ""),
("A1", "kapusta", "kà-làm plii", "กะหล่ำปลี", "Warzywa", 3, "n", JN, "", ""),
("A1", "sałata", "phàk kàat", "ผักกาด", "Warzywa", 3, "n", JN, "", ""),
("A1", "szpinak wodny", "phàk bûng", "ผักบุ้ง", "Warzywa", 4, "n", JN,
 "Najpospolitsze tajskie warzywo: phàk bûng fai daeng to danie z każdej ulicy.", ""),
("A1", "bakłażan", "má-khǔea", "มะเขือ", "Warzywa", 3, "n", JN, "", ""),
("A1", "papryka", "phrík yùak", "พริกหยวก", "Warzywa", 3, "n", JN, "", ""),
("A1", "dynia", "fák thawng", "ฟักทอง", "Warzywa", 3, "n", JN, "", "dynia złota"),
("A1", "ziemniak", "man fà-ràng", "มันฝรั่ง", "Warzywa", 4, "n", JN, "", "bulwa zachodnia"),
("A1", "batat", "man thêet", "มันเทศ", "Warzywa", 3, "n", JN, "", ""),
("A1", "kukurydza", "khâo phôot", "ข้าวโพด", "Warzywa", 4, "n", JN, "", ""),
("A1", "fasolka szparagowa", "thùa fàk yaao", "ถั่วฝักยาว", "Warzywa", 3, "n", JN, "", "fasola strąk długi"),
("A1", "kiełki fasoli", "thùa ngâwk", "ถั่วงอก", "Warzywa", 3, "n", JN, "", "fasola kiełkować"),
("A1", "grzyb", "hèt", "เห็ด", "Warzywa", 3, "n", JN, "", ""),
("A2", "por", "tôn kràt", "ต้นกระเทียม", "Warzywa", 2, "n", JN, "", ""),
("A2", "seler naciowy", "khûen châai", "ขึ้นฉ่าย", "Warzywa", 2, "n", JN, "", ""),
("A2", "brokuł", "bràwk-khoo-lîi", "บรอกโคลี", "Warzywa", 2, "n", JN, "", ""),
("A2", "rzodkiew", "hǔa châi tháo", "หัวไชเท้า", "Warzywa", 2, "n", JN, "", ""),
("A2", "pęd bambusa", "nàw mái", "หน่อไม้", "Warzywa", 3, "n", JN, "", "pęd drewno"),

# =========================================================== owoce
("A1", "arbuz", "taeng moo", "แตงโม", "Owoce", 4, "n", JN, "", ""),
("A1", "ananas", "sàp-pà-rót", "สับปะรด", "Owoce", 4, "n", JN, "", ""),
("A1", "mango", "má-mûang", "มะม่วง", "Owoce", 5, "n", JN,
 "khâo nǐao má-mûang — ryż kleisty z mango — to najsłynniejszy tajski deser.", ""),
("A1", "papaja", "má-lá-kaw", "มะละกอ", "Owoce", 4, "n", JN, "", ""),
("A1", "guawa", "fà-ràng", "ฝรั่ง", "Owoce", 3, "n", JN,
 "To samo słowo znaczy „człowiek Zachodu”. Homonim, nie żart.", ""),
("A1", "kokos", "má-phráao", "มะพร้าว", "Owoce", 4, "n", JN, "", ""),
("A1", "rambutan", "ngáw", "เงาะ", "Owoce", 3, "n", JN, "", ""),
("A1", "mangostan", "mang-khút", "มังคุด", "Owoce", 3, "n", JN, "", ""),
("A1", "durian", "thú-rian", "ทุเรียน", "Owoce", 3, "n", JN,
 "Zakazany w hotelach i metrze. Zapach czuć przez zamknięte drzwi.", ""),
("A1", "liczi", "lín-jìi", "ลิ้นจี่", "Owoce", 2, "n", JN, "", ""),
("A1", "smoczy owoc", "kâeo mang-kawn", "แก้วมังกร", "Owoce", 3, "n", JN, "", "klejnot smok"),
("A1", "melon", "taeng thai", "แตงไทย", "Owoce", 2, "n", JN, "", ""),
("A1", "winogrono", "à-ngùn", "องุ่น", "Owoce", 3, "n", JN, "", ""),
("A1", "gruszka", "sǎa-lîi", "สาลี่", "Owoce", 2, "n", JN, "", ""),
("A1", "brzoskwinia", "lûuk phîich", "ลูกพีช", "Owoce", 2, "n", JN, "", ""),
("A2", "limonka", "má-naao", "มะนาว", "Owoce", 5, "n", JN,
 "Podstawa tajskiej kuchni. „Sok z cytryny” w tajskim przepisie to zwykle limonka.", ""),
("A2", "tamaryndowiec", "má-khǎam", "มะขาม", "Owoce", 3, "n", JN, "", ""),
("A2", "owoc sezonowy", "phǒn-lá-mái taam rúe-duu", "ผลไม้ตามฤดู", "Owoce", 2, "n", JN, "", ""),

# =========================================================== mięso i ryby
("A1", "wołowina", "núea wua", "เนื้อวัว", "Mięso", 4, "n", JN, "", "mięso krowa"),
("A1", "wieprzowina", "mǔu", "หมู", "Mięso", 5, "n", JN,
 "To samo słowo znaczy „świnia”. Na karcie zawsze chodzi o mięso.", ""),
("A1", "kaczka", "pèt", "เป็ด", "Mięso", 3, "n", JN, "", ""),
("A1", "krewetka", "kûng", "กุ้ง", "Mięso", 5, "n", JN, "", ""),
("A1", "kalmar", "plaa mùek", "ปลาหมึก", "Mięso", 4, "n", JN, "", "ryba atrament"),
("A1", "krab", "puu", "ปู", "Mięso", 4, "n", JN, "", ""),
("A1", "małż", "hǎwi", "หอย", "Mięso", 3, "n", JN, "", ""),
("A2", "kiełbasa", "sâi kràwk", "ไส้กรอก", "Mięso", 3, "n", JN, "", ""),
("A2", "szynka", "haem", "แฮม", "Mięso", 2, "n", JN, "", ""),
("A2", "boczek", "mǔu sǎam chán", "หมูสามชั้น", "Mięso", 3, "n", JN, "", "wieprzowina trzy warstwy"),
("A2", "mielone mięso", "mǔu sàp", "หมูสับ", "Mięso", 4, "n", JN, "", "wieprzowina siekana"),
("A2", "żeberka", "sîi khrong", "ซี่โครง", "Mięso", 2, "n", JN, "", ""),
("A2", "wątróbka", "tàp", "ตับ", "Mięso", 2, "n", JN, "", ""),
("A2", "owoce morza", "aa-hǎan thá-lee", "อาหารทะเล", "Mięso", 4, "n", RE, "", "jedzenie morze"),

# =========================================================== podstawy kuchni
("A1", "mąka", "pâeng", "แป้ง", "Produkty", 3, "n", JN, "", ""),
("A1", "olej", "nám man phûet", "น้ำมันพืช", "Produkty", 3, "n", JN, "", "olej roślinny"),
("A1", "ocet", "nám sôm sǎai chuu", "น้ำส้มสายชู", "Produkty", 3, "n", JN, "", ""),
("A1", "sos sojowy", "sii-íu", "ซีอิ๊ว", "Produkty", 4, "n", JN, "", ""),
("A1", "sos rybny", "nám plaa", "น้ำปลา", "Produkty", 5, "n", JN,
 "Sól tajskiej kuchni. Stoi na stole obok cukru, chili i octu — to „czwórka przypraw”.", "woda ryba"),
("A1", "sos ostrygowy", "nám man hǎwi", "น้ำมันหอย", "Produkty", 3, "n", JN, "", ""),
("A1", "mleko kokosowe", "kà-thí", "กะทิ", "Produkty", 4, "n", JN, "", ""),
("A1", "masło", "noei", "เนย", "Produkty", 3, "n", JN, "", ""),
("A1", "ser", "noei khǎeng", "เนยแข็ง", "Produkty", 3, "n", JN, "", "masło twarde"),
("A1", "jogurt", "yoo-kôet", "โยเกิร์ต", "Produkty", 3, "n", JN, "", ""),
("A1", "miód", "nám phûeng", "น้ำผึ้ง", "Produkty", 3, "n", JN, "", "woda pszczoła"),
("A1", "dżem", "yaem", "แยม", "Produkty", 2, "n", JN, "", ""),
("A2", "pasta curry", "phrík kaeng", "พริกแกง", "Produkty", 3, "n", JN, "", "chili curry"),
("A2", "kolendra", "phàk chii", "ผักชี", "Produkty", 4, "n", JN,
 "„mâi sài phàk chii” — bez kolendry — to zdanie, które warto umieć, bo dodaje się ją do wszystkiego.", ""),
("A2", "bazylia tajska", "hoo-rá-phaa", "โหระพา", "Produkty", 3, "n", JN, "", ""),
("A2", "trawa cytrynowa", "tà-khrái", "ตะไคร้", "Produkty", 3, "n", JN, "", ""),
("A2", "galangal", "khàa", "ข่า", "Produkty", 2, "n", JN, "", ""),
("A2", "liść limonki kaffir", "bai má-krùut", "ใบมะกรูด", "Produkty", 2, "n", JN, "", "liść limonka kaffir"),
("A2", "orzeszki ziemne", "thùa lí-sǒng", "ถั่วลิสง", "Produkty", 4, "n", JN,
 "Alergeny są w Tajlandii wszędzie — to hasło warto znać zdrowotnie, nie kulinarnie.", ""),
("A2", "sezam", "ngaa", "งา", "Produkty", 2, "n", JN, "", ""),
("A2", "przyprawa", "khrûeang thêet", "เครื่องเทศ", "Produkty", 3, "n", JN, "", ""),

# =========================================================== sposoby gotowania
("A1", "smażyć na patelni", "phàt", "ผัด", "Gotowanie", 5, "v", CZ,
 "Najczęstszy czasownik tajskiej karty: khâo phàt, phàt thai, phàt phàk.", ""),
("A1", "smażyć w głębokim tłuszczu", "thâwt", "ทอด", "Gotowanie", 5, "v", CZ, "", ""),
("A1", "gotować na parze", "nûeng", "นึ่ง", "Gotowanie", 4, "v", CZ, "", ""),
("A1", "grillować", "yâang", "ย่าง", "Gotowanie", 4, "v", CZ, "", ""),
("A1", "gotować w wodzie", "tôm", "ต้ม", "Gotowanie", 5, "v", CZ,
 "Stąd tôm yam — zupa gotowana z mieszanką przypraw.", ""),
("A2", "piec (w piekarniku)", "òp", "อบ", "Gotowanie", 3, "v", CZ, "", ""),
("A2", "dusić", "tǔn", "ตุ๋น", "Gotowanie", 2, "v", CZ, "", ""),
("A2", "siekać", "sàp", "สับ", "Gotowanie", 3, "v", CZ, "", ""),
("A2", "kroić w plastry", "hàn", "หั่น", "Gotowanie", 3, "v", CZ, "", ""),
("A2", "mieszać (łyżką)", "khon", "คน", "Gotowanie", 3, "v", CZ,
 "Para minimalna z khon (człowiek) — ten sam zapis, inne znaczenie i inne pismo.", ""),
("A2", "obierać", "pàwk", "ปอก", "Gotowanie", 3, "v", CZ, "", ""),
("A2", "ucierać w moździerzu", "tam", "ตำ", "Gotowanie", 3, "v", CZ,
 "Stąd sôm tam — sałatka z zielonej papai ucierana w moździerzu.", ""),
("A2", "wyciskać (sok)", "khán", "คั้น", "Gotowanie", 2, "v", CZ, "", ""),
("A2", "podgrzać", "ùn", "อุ่น", "Gotowanie", 4, "v", CZ, "", ""),
("A2", "schłodzić", "châe yen", "แช่เย็น", "Gotowanie", 3, "v", CZ, "", "moczyć zimno"),
("A2", "marynować", "màk", "หมัก", "Gotowanie", 2, "v", CZ, "", ""),
("A2", "posypać", "roi", "โรย", "Gotowanie", 2, "v", CZ, "", ""),
("A2", "polać sosem", "râat", "ราด", "Gotowanie", 3, "v", CZ,
 "Stąd khâo râat kaeng — ryż polany curry, najtańszy obiad w Tajlandii.", ""),

# =========================================================== dania
("A1", "smażony ryż", "khâo phàt", "ข้าวผัด", "Dania", 5, "n", RE, "", "ryż smażony"),
("A1", "ryż kleisty", "khâo nǐao", "ข้าวเหนียว", "Dania", 4, "n", RE, "", "ryż lepki"),
("A1", "makaron ryżowy", "kǔai tǐao", "ก๋วยเตี๋ยว", "Dania", 5, "n", RE, "", ""),
("A1", "zupa z makaronem", "kǔai tǐao nám", "ก๋วยเตี๋ยวน้ำ", "Dania", 4, "n", RE, "", "makaron woda"),
("A1", "makaron bez zupy", "kǔai tǐao hâeng", "ก๋วยเตี๋ยวแห้ง", "Dania", 3, "n", RE, "", "makaron suchy"),
("A1", "omlet", "khài jiao", "ไข่เจียว", "Dania", 4, "n", RE, "", ""),
("A1", "jajko sadzone", "khài daao", "ไข่ดาว", "Dania", 4, "n", RE, "", "jajko gwiazda"),
("A1", "sałatka z papai", "sôm tam", "ส้มตำ", "Dania", 5, "n", RE, "", ""),
("A2", "zupa tom yam", "tôm yam", "ต้มยำ", "Dania", 5, "n", RE, "", ""),
("A2", "curry zielone", "kaeng khǐao wǎan", "แกงเขียวหวาน", "Dania", 4, "n", RE, "", "curry zielone słodkie"),
("A2", "curry czerwone", "kaeng phèt", "แกงเผ็ด", "Dania", 3, "n", RE, "", "curry ostre"),
("A2", "kurczak z bazylią", "kà-phrao kài", "กะเพราไก่", "Dania", 5, "n", RE,
 "Domyślne danie Taja, gdy nie wie, co zamówić. Zwykle z jajkiem sadzonym na wierzchu.", ""),
("A2", "szaszłyk wieprzowy", "mǔu pîng", "หมูปิ้ง", "Dania", 4, "n", RE, "", ""),
("A2", "sajgonki", "pàw-pía thâwt", "ปอเปี๊ยะทอด", "Dania", 3, "n", RE, "", "sajgonka smażona"),
("A2", "owsianka ryżowa", "jóok", "โจ๊ก", "Dania", 3, "n", RE,
 "Standardowe tajskie śniadanie, także jedzenie dla chorych.", ""),
("A2", "przekąska", "khǎwng waang", "ของว่าง", "Dania", 4, "n", RE, "", "rzecz wolna"),
("A2", "deser", "khǎwng wǎan", "ของหวาน", "Dania", 4, "n", RE, "", "rzecz słodka"),
("A2", "lody", "ai-sà-khriim", "ไอศกรีม", "Dania", 4, "n", RE, "", ""),
("A2", "ciasto", "khéek", "เค้ก", "Dania", 3, "n", RE, "", ""),

# =========================================================== napoje
("A1", "woda gazowana", "nám sôo-daa", "น้ำโซดา", "Napoje", 3, "n", JN, "", ""),
("A1", "herbata mrożona", "chaa yen", "ชาเย็น", "Napoje", 5, "n", JN, "", "herbata zimna"),
("A1", "kawa mrożona", "kaa-fae yen", "กาแฟเย็น", "Napoje", 5, "n", JN, "", ""),
("A1", "kawa czarna", "kaa-fae dam", "กาแฟดำ", "Napoje", 4, "n", JN, "", ""),
("A1", "sok ze świeżych owoców", "nám phǒn-lá-mái khán sòt", "น้ำผลไม้คั้นสด", "Napoje", 3, "n", JN, "", ""),
("A1", "koktajl owocowy", "nám pàn", "น้ำปั่น", "Napoje", 4, "n", JN, "", "woda miksowana"),
("A2", "piwo", "bia", "เบียร์", "Napoje", 4, "n", JN, "", ""),
("A2", "wino", "wai", "ไวน์", "Napoje", 3, "n", JN, "", ""),
("A2", "lód (kostki)", "nám khǎeng", "น้ำแข็ง", "Napoje", 5, "n", JN, "", "woda twarda"),
("A2", "słomka", "làwt", "หลอด", "Napoje", 4, "n", RE, "", "rurka"),

# =========================================================== smaki i zastrzeżenia
("A1", "kwaśny", "prîao", "เปรี้ยว", "Smaki", 4, "adj", CO, "", ""),
("A1", "gorzki", "khǒm", "ขม", "Smaki", 3, "adj", CO, "", ""),
("A1", "słony", "khem", "เค็ม", "Smaki", 4, "adj", CO, "", ""),
("A1", "mdły, bez smaku", "jùet", "จืด", "Smaki", 4, "adj", CO,
 "Ważne przy zamawianiu: kaeng jùet to zupa łagodna, nie „zepsuta”.", ""),
("A2", "tłusty", "man", "มัน", "Smaki", 3, "adj", CO, "", ""),
("A2", "chrupiący", "kràwp", "กรอบ", "Smaki", 4, "adj", CO, "", ""),
("A2", "miękki (o jedzeniu)", "nîm", "นิ่ม", "Smaki", 3, "adj", CO, "", ""),
("A2", "aromatyczny", "hǎwm", "หอม", "Smaki", 4, "adj", CO,
 "To samo słowo znaczy „pachnący” i jest komplementem także o człowieku.", ""),
("A2", "nieświeży, zepsuty", "bùut", "บูด", "Smaki", 3, "adj", CO, "", ""),
("A2", "Bez ostrego, proszę.", "mâi phèt ná khráp", "ไม่เผ็ดนะครับ", "Zastrzeżenia", 5, "w", RE,
 "Uwaga: „mâi phèt” po tajsku i tak bywa ostre. Bezpieczniej dodać „mâi sài phrík” — bez chili.", ""),
("A2", "Bez chili.", "mâi sài phrík khráp", "ไม่ใส่พริกครับ", "Zastrzeżenia", 5, "w", RE, "", ""),
("A2", "Bez cukru.", "mâi sài nám taan khráp", "ไม่ใส่น้ำตาลครับ", "Zastrzeżenia", 4, "w", RE, "", ""),
("A2", "Bez lodu.", "mâi sài nám khǎeng khráp", "ไม่ใส่น้ำแข็งครับ", "Zastrzeżenia", 4, "w", RE, "", ""),
("A2", "Bez orzeszków.", "mâi sài thùa khráp", "ไม่ใส่ถั่วครับ", "Zastrzeżenia", 4, "w", RE, "", ""),
("A2", "Jestem uczulony.", "phǒm pháe khráp", "ผมแพ้ครับ", "Zastrzeżenia", 4, "w", ZD, "", ""),
("A2", "Nie jem mięsa.", "phǒm mâi kin núea sàt khráp", "ผมไม่กินเนื้อสัตว์ครับ", "Zastrzeżenia", 4, "w", RE, "", ""),
("A2", "Trochę mniej ostre.", "phèt náwi khráp", "เผ็ดน้อยครับ", "Zastrzeżenia", 4, "w", RE, "", ""),
("A2", "Na wynos.", "sài thǔng khráp", "ใส่ถุงครับ", "Zastrzeżenia", 5, "w", RE,
 "Dosłownie „do torebki”. Tajskie jedzenie na wynos jedzie w woreczku, nie w pudełku.", "włożyć torba"),
("A2", "Na miejscu.", "kin thîi nîi khráp", "กินที่นี่ครับ", "Zastrzeżenia", 4, "w", RE, "", ""),

# =========================================================== pytania o jedzenie
("A1", "Co polecacie?", "náe-nam à-rai dii khráp", "แนะนำอะไรดีครับ", "Pytania", 4, "w", PY, "", ""),
("A1", "Czy to jest ostre?", "an níi phèt mǎi khráp", "อันนี้เผ็ดไหมครับ", "Pytania", 5, "w", PY, "", ""),
("A1", "Co to za mięso?", "núea à-rai khráp", "เนื้ออะไรครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Czy jest coś bez mięsa?", "mii aa-hǎan mâi mii núea mǎi khráp", "มีอาหารไม่มีเนื้อไหมครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Ile to zajmie?", "chái wee-laa naan mǎi khráp", "ใช้เวลานานไหมครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Czy mogę prosić rachunek?", "khǎw chék bin dûai khráp", "ขอเช็คบิลด้วยครับ", "Pytania", 5, "w", RE, "", ""),
]
