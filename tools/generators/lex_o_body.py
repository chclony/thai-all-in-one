# -*- coding: utf-8 -*-
"""Sesja O, partia 5 — CIAŁO I ZDROWIE.

Kategoria Zdrowie miała 119 haseł, co wystarcza na aptekę i nie wystarcza
na wizytę u lekarza. Brakowało trzech rzeczy naraz:

* **nazw części ciała** poza najbardziej oczywistymi — bez nich nie da się
  wskazać, co boli, a wskazanie palcem działa tylko dla rzeczy widocznych;
* **opisu objawu** — tajski rozróżnia rodzaje bólu przyrostkami czasownika
  (`jèp` ból ostry z zewnątrz, `pùat` ból tępy od środka, `khan` swędzenie),
  a Polak domyślnie tłumaczy wszystko jako „boli”;
* **słownictwa apteki i szpitala** — recepta, skierowanie, ubezpieczenie.

Warstwa `jèp`/`pùat` jest tu ważniejsza niż lista chorób. Lekarz w Tajlandii
prawie zawsze zapyta „jèp rǔe pùat” — i od odpowiedzi zależy diagnoza.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

ZD = "Zdrowie"
AW = "Awarie i pomoc"
CO = "Cechy i opinie"
CZ = "Czasowniki"
PY = "Pytania"
DC = "Dom i codzienność"
ZP = "Zakupy i pieniądze"
ST = "Small talk"
LR = "Ludzie i rodzina"

BODY = [

# =========================================================== części ciała
("A1", "czoło", "nâa phàak", "หน้าผาก", "Ciało", 3, "n", ZD, "", ""),
("A1", "policzek", "kâem", "แก้ม", "Ciało", 3, "n", ZD, "", ""),
("A1", "broda (część twarzy)", "khaang", "คาง", "Ciało", 2, "n", ZD, "", ""),
("A1", "warga", "rim fǐi pàak", "ริมฝีปาก", "Ciało", 3, "n", ZD, "", ""),
("A1", "język (w ustach)", "lín", "ลิ้น", "Ciało", 3, "n", ZD,
 "Uwaga: język jako mowa to phaa-sǎa. To dwa różne słowa, inaczej niż po polsku.", ""),
("A1", "gardło", "khaw", "คอ", "Ciało", 4, "n", ZD,
 "To samo słowo znaczy „szyja”. jèp khaw — boli gardło.", ""),
("A1", "kark", "tôn khaw", "ต้นคอ", "Ciało", 2, "n", ZD, "", ""),
("A1", "ramię", "lài", "ไหล่", "Ciało", 3, "n", ZD, "", ""),
("A1", "łokieć", "khâw sàwk", "ข้อศอก", "Ciało", 2, "n", ZD, "", ""),
("A1", "nadgarstek", "khâw mue", "ข้อมือ", "Ciało", 2, "n", ZD, "", "staw ręka"),
("A1", "palec u ręki", "níu mue", "นิ้วมือ", "Ciało", 3, "n", ZD, "", ""),
("A1", "paznokieć", "lép", "เล็บ", "Ciało", 3, "n", ZD, "", ""),
("A1", "klatka piersiowa", "nâa òk", "หน้าอก", "Ciało", 3, "n", ZD, "", ""),
("A1", "plecy", "lǎng", "หลัง", "Ciało", 4, "n", ZD,
 "To samo słowo znaczy „po, za” — lǎng aa-hǎan to po posiłku.", ""),
("A1", "brzuch", "tháwng", "ท้อง", "Ciało", 5, "n", ZD,
 "„mii tháwng” znaczy „być w ciąży” — dosłownie „mieć brzuch”.", ""),
("A1", "biodro", "sà-phôok", "สะโพก", "Ciało", 2, "n", ZD, "", ""),
("A1", "kolano", "hǔa khào", "หัวเข่า", "Ciało", 3, "n", ZD, "", "głowa kolano"),
("A1", "kostka (u nogi)", "khâw tháo", "ข้อเท้า", "Ciało", 3, "n", ZD, "", "staw stopa"),
("A1", "pięta", "sôn tháo", "ส้นเท้า", "Ciało", 2, "n", ZD, "", ""),
("A1", "palec u nogi", "níu tháo", "นิ้วเท้า", "Ciało", 2, "n", ZD, "", ""),
("A2", "skóra (ciała)", "phǐu", "ผิว", "Ciało", 4, "n", ZD, "", ""),
("A2", "kość", "krà-dùuk", "กระดูก", "Ciało", 3, "n", ZD, "", ""),
("A2", "mięsień", "klâam núea", "กล้ามเนื้อ", "Ciało", 3, "n", ZD, "", ""),
("A2", "krew", "lûeat", "เลือด", "Ciało", 4, "n", ZD, "", ""),
("A2", "serce (narząd)", "hǔa jai", "หัวใจ", "Ciało", 4, "n", ZD,
 "Uwaga: jai samo znaczy „serce” w sensie uczuć, hǔa jai to narząd.", "głowa serce"),
("A2", "płuco", "pàwt", "ปอด", "Ciało", 2, "n", ZD, "", ""),
("A2", "żołądek", "krà-pháw aa-hǎan", "กระเพาะอาหาร", "Ciało", 3, "n", ZD, "", ""),
("A2", "nerka", "tai", "ไต", "Ciało", 2, "n", ZD, "", ""),
("A2", "mózg", "sà-mǎwng", "สมอง", "Ciało", 2, "n", ZD, "", ""),
("A2", "nerw", "sên prà-sàat", "เส้นประสาท", "Ciało", 2, "n", ZD, "", ""),
("A2", "oddech", "lom hǎai jai", "ลมหายใจ", "Ciało", 3, "n", ZD, "", "wiatr oddychać"),

# =========================================================== rodzaje bólu
("A1", "boli (ostro, z zewnątrz)", "jèp", "เจ็บ", "Objawy", 5, "v", CZ,
 "Ból od skaleczenia, uderzenia, gardła. Odpowiada na „co cię zabolało”.", ""),
("A1", "boli (tępo, od środka)", "pùat", "ปวด", "Objawy", 5, "v", CZ,
 "Ból głowy, brzucha, mięśni. Lekarz pyta „jèp rǔe pùat” i od tego zaczyna diagnozę.", ""),
("A1", "swędzi", "khan", "คัน", "Objawy", 4, "v", CZ, "", ""),
("A1", "piecze", "sâep", "แสบ", "Objawy", 3, "v", CZ, "", ""),
("A1", "drętwieje", "chaa", "ชา", "Objawy", 3, "v", CZ,
 "Para minimalna z chaa (herbata) — ten sam zapis, inne pismo.", ""),
("A1", "puchnie", "buam", "บวม", "Objawy", 3, "v", CZ, "", ""),
("A2", "kręci się w głowie", "wian hǔa", "เวียนหัว", "Objawy", 4, "v", CZ, "", "kręcić głowa"),
("A2", "mdli mnie", "khlûen sâi", "คลื่นไส้", "Objawy", 3, "v", CZ, "", "fala wnętrzności"),
("A2", "wymiotować", "aa-jian", "อาเจียน", "Objawy", 3, "v", CZ, "", ""),
("A2", "kaszleć", "ai", "ไอ", "Objawy", 4, "v", CZ, "", ""),
("A2", "kichać", "jaam", "จาม", "Objawy", 3, "v", CZ, "", ""),
("A2", "trząść się z zimna", "nǎao sàn", "หนาวสั่น", "Objawy", 3, "v", CZ, "", "zimno drżeć"),
("A2", "krwawić", "lûeat àwk", "เลือดออก", "Objawy", 3, "v", CZ, "", "krew wychodzić"),
("A2", "zemdleć", "pen lom", "เป็นลม", "Objawy", 3, "v", CZ, "", "być wiatrem"),
("A2", "skręcić (nogę)", "phlík", "พลิก", "Objawy", 2, "v", CZ, "", ""),
("A2", "złamać (kość)", "hàk", "หัก", "Objawy", 3, "v", CZ, "", ""),
("A2", "skaleczyć się", "bàat", "บาด", "Objawy", 3, "v", CZ, "", ""),
("A2", "poparzyć się", "lûak", "ลวก", "Objawy", 2, "v", CZ, "", ""),

# =========================================================== dolegliwości
("A1", "gorączka", "khâi", "ไข้", "Choroby", 5, "n", ZD, "", ""),
("A1", "katar", "nám mûuk lǎi", "น้ำมูกไหล", "Choroby", 4, "n", ZD, "", "śluz płynie"),
("A1", "przeziębienie", "wàt", "หวัด", "Choroby", 5, "n", ZD, "", ""),
("A1", "biegunka", "tháwng sǐa", "ท้องเสีย", "Choroby", 5, "n", ZD,
 "Najczęstsza dolegliwość turysty. Dosłownie „zepsuty brzuch”.", "brzuch zepsuty"),
("A1", "zaparcie", "tháwng phùuk", "ท้องผูก", "Choroby", 2, "n", ZD, "", "brzuch związany"),
("A1", "ból głowy", "pùat hǔa", "ปวดหัว", "Choroby", 5, "n", ZD, "", ""),
("A2", "zatrucie pokarmowe", "aa-hǎan pen phít", "อาหารเป็นพิษ", "Choroby", 4, "n", ZD, "", "jedzenie jest trucizną"),
("A2", "alergia", "phúum pháe", "ภูมิแพ้", "Choroby", 4, "n", ZD, "", ""),
("A2", "wysypka", "phùen", "ผื่น", "Choroby", 3, "n", ZD, "", ""),
("A2", "poparzenie słoneczne", "phǐu mâi dàet", "ผิวไหม้แดด", "Choroby", 4, "n", ZD, "", "skóra spalona słońcem"),
("A2", "ukąszenie owada", "malaeng kàt", "แมลงกัด", "Choroby", 4, "n", ZD, "", "owad gryźć"),
("A2", "denga", "khâi lûeat àwk", "ไข้เลือดออก", "Choroby", 3, "n", ZD,
 "W porze deszczowej realne zagrożenie. Objawy: wysoka gorączka i ból za oczami.", "gorączka krwotoczna"),
("A2", "grypa", "khâi wàt yài", "ไข้หวัดใหญ่", "Choroby", 3, "n", ZD, "", "przeziębienie duże"),
("A2", "infekcja", "kaan tìt chúea", "การติดเชื้อ", "Choroby", 3, "n", ZD, "", "przyczepić zarazek"),
("A2", "zapalenie", "kaan àk-sèep", "การอักเสบ", "Choroby", 2, "n", ZD, "", ""),
("A2", "cukrzyca", "bao wǎan", "เบาหวาน", "Choroby", 2, "n", ZD, "", "mocz słodki"),
("A2", "astma", "hòop hùet", "หอบหืด", "Choroby", 2, "n", ZD, "", ""),
("A2", "próchnica", "fan phù", "ฟันผุ", "Choroby", 2, "n", ZD, "", "ząb zepsuty"),
("A2", "bezsenność", "nawn mâi làp", "นอนไม่หลับ", "Choroby", 3, "n", ZD, "", "leżeć nie zasnąć"),
("A2", "choroba lokomocyjna", "mao rót", "เมารถ", "Choroby", 3, "n", ZD, "", "upić się pojazdem"),
("A2", "kac", "mao kháang", "เมาค้าง", "Choroby", 2, "n", ZD, "", "upojenie zaległe"),

# =========================================================== apteka i szpital
("A1", "tabletka", "yaa mét", "ยาเม็ด", "Apteka", 4, "n", ZD, "", "lek ziarno"),
("A1", "syrop (lek)", "yaa nám", "ยาน้ำ", "Apteka", 3, "n", ZD, "", ""),
("A1", "maść", "yaa thaa", "ยาทา", "Apteka", 4, "n", ZD, "", "lek do smarowania"),
("A1", "lek przeciwbólowy", "yaa kâe pùat", "ยาแก้ปวด", "Apteka", 5, "n", ZD,
 "Przedrostek yaa kâe- „lek na coś” jest produktywny: yaa kâe ai, yaa kâe khǎi.", "lek leczyć ból"),
("A1", "lek na kaszel", "yaa kâe ai", "ยาแก้ไอ", "Apteka", 4, "n", ZD, "", ""),
("A1", "lek na gorączkę", "yaa lót khâi", "ยาลดไข้", "Apteka", 4, "n", ZD, "", "lek obniżać gorączkę"),
("A1", "lek na biegunkę", "yaa kâe tháwng sǐa", "ยาแก้ท้องเสีย", "Apteka", 4, "n", ZD, "", ""),
("A2", "antybiotik", "yaa khâa chúea", "ยาฆ่าเชื้อ", "Apteka", 3, "n", ZD, "", "lek zabijać zarazek"),
("A2", "witamina", "wí-taa-min", "วิตามิน", "Apteka", 2, "n", ZD, "", ""),
("A2", "bandaż", "phâa phan phlǎe", "ผ้าพันแผล", "Apteka", 3, "n", ZD, "", "materiał owijać rana"),
("A2", "rana", "phlǎe", "แผล", "Apteka", 4, "n", ZD, "", ""),
("A2", "recepta", "bai sàng yaa", "ใบสั่งยา", "Apteka", 3, "n", ZD, "", "liść zamawiać lek"),
("A2", "dawka", "khà-nàat yaa", "ขนาดยา", "Apteka", 2, "n", ZD, "", "rozmiar lek"),
("A2", "skutek uboczny", "phǒn khâang khiang", "ผลข้างเคียง", "Apteka", 2, "n", ZD, "", "wynik obok"),
("A2", "termin ważności", "wan mòt aa-yú", "วันหมดอายุ", "Apteka", 3, "n", ZP, "", "dzień koniec wiek"),
("A2", "izba przyjęć", "hâwng chùk-chə̌ən", "ห้องฉุกเฉิน", "Szpital", 4, "n", AW, "", ""),
("A2", "przychodnia", "khlii-ník", "คลินิก", "Szpital", 4, "n", ZD, "", ""),
("A2", "gabinet lekarski", "hâwng trùat", "ห้องตรวจ", "Szpital", 2, "n", ZD, "", "pokój badanie"),
("A2", "sala szpitalna", "hâwng phûu pùai", "ห้องผู้ป่วย", "Szpital", 2, "n", ZD, "", "pokój chory"),
("A2", "pacjent", "phûu pùai", "ผู้ป่วย", "Szpital", 4, "n", ZD, "", "osoba chora"),
("A2", "prześwietlenie", "èk-sà-ree", "เอกซเรย์", "Szpital", 2, "n", ZD, "", ""),
("A2", "badanie krwi", "trùat lûeat", "ตรวจเลือด", "Szpital", 3, "n", ZD, "", ""),
("A2", "zastrzyk", "chìit yaa", "ฉีดยา", "Szpital", 3, "n", ZD, "", ""),
("A2", "szwy", "yép phlǎe", "เย็บแผล", "Szpital", 2, "n", ZD, "", "szyć rana"),
("A2", "gips", "fuèak", "เฝือก", "Szpital", 2, "n", ZD, "", ""),
("A2", "wózek inwalidzki", "rót khěn phûu pùai", "รถเข็นผู้ป่วย", "Szpital", 2, "n", ZD, "", ""),
("A2", "karetka", "rót chùk-chə̌ən", "รถฉุกเฉิน", "Szpital", 4, "n", AW, "", "pojazd nagły"),

# =========================================================== zdrowy tryb życia
("A2", "zdrowy (o człowieku)", "sùk-khà-phâap dii", "สุขภาพดี", "Zdrowie", 4, "adj", ZD, "", "zdrowie dobre"),
("A2", "chory", "mâi sà-baai", "ไม่สบาย", "Zdrowie", 5, "adj", ZD,
 "Dosłownie „nie jest wygodnie”. Tajski unika mocnego słowa „chory”.", "nie wygodnie"),
("A2", "wyzdrowieć", "hǎai", "หาย", "Zdrowie", 5, "v", CZ,
 "To samo słowo znaczy „zniknąć” — dolegliwość po prostu znika.", ""),
("A2", "odpoczywać", "phák phàwn", "พักผ่อน", "Zdrowie", 5, "v", CZ, "", ""),
("A2", "ćwiczyć", "àwk kam-lang kaai", "ออกกำลังกาย", "Zdrowie", 4, "v", CZ, "", "wydawać siłę ciała"),
("A2", "schudnąć", "lót nám-nàk", "ลดน้ำหนัก", "Zdrowie", 3, "v", CZ, "", "zmniejszyć wagę"),
("A2", "przytyć", "nám-nàk khûen", "น้ำหนักขึ้น", "Zdrowie", 3, "v", CZ, "", "waga rośnie"),
("A2", "rzucić palenie", "lôek sùup bù-rìi", "เลิกสูบบุหรี่", "Zdrowie", 3, "v", CZ, "", "porzucić palić papieros"),
("A2", "brać leki", "kin yaa", "กินยา", "Zdrowie", 5, "v", CZ,
 "Tajski „je” lekarstwo, nie „bierze” — kin yaa, nie ao yaa.", "jeść lek"),
("A2", "wysypiać się", "nawn làp phaw", "นอนหลับพอ", "Zdrowie", 3, "v", CZ, "", "spać wystarczająco"),

# =========================================================== pytania medyczne
("A1", "Gdzie boli?", "jèp trong nǎi khráp", "เจ็บตรงไหนครับ", "Pytania", 4, "w", PY, "", ""),
("A1", "Od kiedy?", "tâng tàe mûea rài khráp", "ตั้งแต่เมื่อไหร่ครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Czy to poważne?", "raeng mǎi khráp", "แรงไหมครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Ile razy dziennie?", "wan lá kìi khráng khráp", "วันละกี่ครั้งครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Czy mogę to jeść z lekami?", "kin kàp yaa dâi mǎi khráp", "กินกับยาได้ไหมครับ", "Pytania", 2, "w", PY, "", ""),
("A2", "Potrzebuję lekarza.", "phǒm tâwng-kaan mǎw khráp", "ผมต้องการหมอครับ", "Pytania", 5, "w", AW, "", ""),
("A2", "Proszę wezwać karetkę.", "chûai rîak rót chùk-chə̌ən khráp", "ช่วยเรียกรถฉุกเฉินครับ", "Pytania", 5, "w", AW, "", ""),
("A2", "Mam ubezpieczenie.", "phǒm mii prà-kan khráp", "ผมมีประกันครับ", "Pytania", 4, "w", AW, "", ""),
]
