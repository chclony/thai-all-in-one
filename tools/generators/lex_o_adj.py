# -*- coding: utf-8 -*-
"""Sesja O, partia 9 — PRZYMIOTNIKI I PRZYSŁÓWKI.

Kategoria Cechy i opinie miała 230 haseł — dużo, ale nierówno. Baza umiała
ocenić rzecz (dobra, zła, droga, ładna) i prawie nie umiała jej **opisać**:
brakowało kształtów, faktur, kolorów pośrednich, natężeń.

Druga luka: **przysłówki**. Baza miała ich 29 na 2 259 haseł leksykalnych,
czyli 1,3%. W mowie potocznej przysłówek jest w co drugim zdaniu — to on
niesie „szybko, powoli, znowu, prawie, w ogóle, akurat”. Bez tej warstwy
uczący się mówi zdaniami poprawnymi i martwymi.

Trzecia warstwa to **reduplikacja**, chwyt gramatyczny bez odpowiednika
w polskim: powtórzenie przymiotnika osłabia go i zmiękcza (`dii dii` —
„porządnie, jak należy”, `cháa cháa` — „powolutku”). Uczący się słyszy to
codziennie i bez wyjaśnienia bierze za jąkanie.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

CO = "Cechy i opinie"
GU = "Gramatyka użytkowa"
LI = "Liczby i liczenie"
CD = "Czas i daty"
ST = "Small talk"
ZP = "Zakupy i pieniądze"
MO = "Miejsca i orientacja"
PP = "Pogoda i przyroda"
DC = "Dom i codzienność"

ADJ = [

# =========================================================== kształt i wymiar
("A1", "okrągły", "klom", "กลม", "Kształt", 3, "adj", CO, "", ""),
("A1", "kwadratowy", "sìi lìam", "สี่เหลี่ยม", "Kształt", 3, "adj", CO, "", "cztery boki"),
("A1", "prosty (nie krzywy)", "trong", "ตรง", "Kształt", 4, "adj", CO,
 "To samo słowo znaczy „dokładnie w” — trong wee-laa, punktualnie.", ""),
("A1", "krzywy", "khót", "คด", "Kształt", 2, "adj", CO, "", ""),
("A1", "płaski", "bâen", "แบน", "Kształt", 3, "adj", CO,
 "yaang bâen — flak w oponie. Zdanie przydatne przy wynajmie skutera.", ""),
("A1", "gruby (o rzeczy)", "nǎa", "หนา", "Kształt", 3, "adj", CO, "", ""),
("A1", "cienki", "baang", "บาง", "Kształt", 3, "adj", CO,
 "To samo słowo znaczy „niektóre” — baang khon, niektórzy ludzie.", ""),
("A1", "wąski", "khâep", "แคบ", "Kształt", 3, "adj", CO, "", ""),
("A1", "głęboki", "lúek", "ลึก", "Kształt", 3, "adj", CO, "", ""),
("A1", "płytki", "tûen", "ตื้น", "Kształt", 2, "adj", CO, "", ""),
("A1", "ostry (o nożu)", "khom", "คม", "Kształt", 3, "adj", CO,
 "Uwaga: ostry o smaku to phèt, ostry o nożu to khom. Dwa różne słowa.", ""),
("A1", "tępy", "thûe", "ทื่อ", "Kształt", 2, "adj", CO, "", ""),
("A1", "spiczasty", "lǎem", "แหลม", "Kształt", 2, "adj", CO, "", ""),

# =========================================================== faktura i stan
("A1", "gładki", "rîap", "เรียบ", "Faktura", 3, "adj", CO,
 "Także „skromny, bez ozdób” — o stroju i o człowieku.", ""),
("A1", "szorstki", "khrù-khrà", "ขรุขระ", "Faktura", 2, "adj", CO, "", ""),
("A1", "śliski", "lûen", "ลื่น", "Faktura", 3, "adj", CO, "", ""),
("A1", "lepki", "nǐao", "เหนียว", "Faktura", 3, "adj", CO,
 "khâo nǐao — ryż kleisty. To samo słowo znaczy „wytrzymały” i „skąpy”.", ""),
("A1", "mokry", "pìak", "เปียก", "Faktura", 4, "adj", CO, "", ""),
("A1", "wilgotny", "chúen", "ชื้น", "Faktura", 3, "adj", PP, "", ""),
("A1", "zakurzony", "mii fùn", "มีฝุ่น", "Faktura", 3, "adj", DC, "", "mieć kurz"),
("A1", "błyszczący", "ngao", "เงา", "Faktura", 2, "adj", CO, "", ""),
("A1", "matowy", "dâan", "ด้าน", "Faktura", 2, "adj", CO, "", ""),
("A1", "przezroczysty", "sǎi", "ใส", "Faktura", 3, "adj", CO,
 "nám sǎi — czysta woda. Także o dźwięku i o człowieku bez ukrytych zamiarów.", ""),
("A1", "mętny", "khùn", "ขุ่น", "Faktura", 2, "adj", CO, "", ""),

# =========================================================== kolory
("A1", "szary", "sǐi thao", "สีเทา", "Kolory", 3, "adj", CO, "", ""),
("A1", "brązowy", "sǐi nám taan", "สีน้ำตาล", "Kolory", 3, "adj", CO, "", "kolor cukru trzcinowego"),
("A1", "różowy", "sǐi chom-phuu", "สีชมพู", "Kolory", 3, "adj", CO, "", ""),
("A1", "fioletowy", "sǐi mûang", "สีม่วง", "Kolory", 3, "adj", CO, "", ""),
("A1", "pomarańczowy", "sǐi sôm", "สีส้ม", "Kolory", 3, "adj", CO, "", "kolor pomarańczy"),
("A1", "złoty (kolor)", "sǐi thawng", "สีทอง", "Kolory", 3, "adj", CO, "", ""),
("A1", "srebrny", "sǐi ngoen", "สีเงิน", "Kolory", 2, "adj", CO, "", ""),
("A1", "beżowy, kremowy", "sǐi khriim", "สีครีม", "Kolory", 2, "adj", CO, "", ""),
("A2", "jasny (o kolorze)", "sǐi àwn", "สีอ่อน", "Kolory", 4, "adj", CO, "", "kolor miękki"),
("A2", "ciemny (o kolorze)", "sǐi khêm", "สีเข้ม", "Kolory", 4, "adj", CO, "", "kolor gęsty"),
("A2", "jednokolorowy", "sǐi diao", "สีเดียว", "Kolory", 2, "adj", ZP, "", ""),
("A2", "w kratę", "laai taa-raang", "ลายตาราง", "Kolory", 2, "adj", ZP, "", "wzór tabela"),
("A2", "w paski", "laai thǎew", "ลายแถว", "Kolory", 2, "adj", ZP, "", ""),
("A2", "w kwiaty", "laai dàwk mái", "ลายดอกไม้", "Kolory", 3, "adj", ZP, "", ""),
("A2", "gładki, bez wzoru", "sǐi phúen", "สีพื้น", "Kolory", 2, "adj", ZP, "", "kolor tło"),

# =========================================================== ocena i natężenie
("A1", "wspaniały", "yîam", "เยี่ยม", "Ocena", 4, "adj", CO, "", ""),
("A1", "okropny", "yâe mâak", "แย่มาก", "Ocena", 4, "adj", CO, "", ""),
("A1", "przeciętny", "thammádaa", "ธรรมดา", "Ocena", 4, "adj", CO,
 "Także „zwykły” — rót thammádaa to autobus bez klimatyzacji.", ""),
("A1", "dziwny", "plàek", "แปลก", "Ocena", 4, "adj", CO, "", ""),
("A1", "śmieszny", "tà-lòk", "ตลก", "Ocena", 4, "adj", CO, "", ""),
("A1", "poważny (o sprawie)", "raeng", "แรง", "Ocena", 4, "adj", CO,
 "Dosłownie „silny”. O wypadku, chorobie, wietrze i o czyichś słowach.", ""),
("A1", "ważny", "sǎm-khan", "สำคัญ", "Ocena", 5, "adj", CO, "", ""),
("A1", "bezużyteczny", "chái mâi dâi", "ใช้ไม่ได้", "Ocena", 4, "adj", CO, "", "używać nie móc"),
("A1", "wygodny", "sà-dùak", "สะดวก", "Ocena", 5, "adj", CO,
 "sà-dùak súe — sklep całodobowy, dosłownie „wygodny zakup”.", ""),
("A1", "niewygodny", "mâi sà-dùak", "ไม่สะดวก", "Ocena", 4, "adj", CO, "", ""),
("A1", "praktyczny", "chái ngaan dâi dii", "ใช้งานได้ดี", "Ocena", 3, "adj", CO, "", ""),
("A2", "opłacalny", "khúm", "คุ้ม", "Ocena", 4, "adj", ZP,
 "khúm khâa — wart swojej ceny. Częsty argument na targu.", ""),
("A2", "nieopłacalny", "mâi khúm", "ไม่คุ้ม", "Ocena", 3, "adj", ZP, "", ""),
("A2", "modny", "than sà-mǎi", "ทันสมัย", "Ocena", 3, "adj", CO, "", "nadążać epoka"),
("A2", "staromodny", "láa sà-mǎi", "ล้าสมัย", "Ocena", 2, "adj", CO, "", ""),
("A2", "popularny", "níyom", "นิยม", "Ocena", 3, "adj", CO, "", ""),
("A2", "słynny", "mii chûe sǐang", "มีชื่อเสียง", "Ocena", 4, "adj", CO, "", "mieć imię głos"),
("A2", "rzadki (nieczęsty)", "hǎa yâak", "หายาก", "Ocena", 3, "adj", CO, "", "szukać trudno"),
("A2", "pospolity", "hǎa ngâai", "หาง่าย", "Ocena", 3, "adj", CO, "", "szukać łatwo"),
("A2", "godny zaufania", "chûea thǔe dâi", "เชื่อถือได้", "Ocena", 3, "adj", CO, "", ""),
("A2", "podejrzany", "nâa sǒng sǎi", "น่าสงสัย", "Ocena", 3, "adj", CO, "", ""),

# =========================================================== nâa- : budzi coś
("A1", "apetyczny", "nâa kin", "น่ากิน", "Wrażenie", 5, "adj", CO,
 "Przedrostek nâa- znaczy „warty tego, budzący to”: nâa duu (wart obejrzenia), nâa klua (straszny).", "warty jedzenia"),
("A1", "wart obejrzenia", "nâa duu", "น่าดู", "Wrażenie", 3, "adj", CO, "", ""),
("A1", "straszny", "nâa klua", "น่ากลัว", "Wrażenie", 4, "adj", CO, "", "budzący strach"),
("A1", "uroczy", "nâa rák", "น่ารัก", "Wrażenie", 5, "adj", CO,
 "Najczęstszy komplement w Tajlandii — o dziecku, zwierzęciu, człowieku i przedmiocie.", "wart miłości"),
("A1", "nudny", "nâa bùea", "น่าเบื่อ", "Wrażenie", 4, "adj", CO, "", ""),
("A1", "interesujący", "nâa sǒn jai", "น่าสนใจ", "Wrażenie", 4, "adj", CO, "", ""),
("A1", "szkoda (że tak)", "nâa sǐa daai", "น่าเสียดาย", "Wrażenie", 4, "adj", CO, "", ""),
("A2", "godny pożałowania", "nâa sǒng sǎan", "น่าสงสาร", "Wrażenie", 3, "adj", CO, "", ""),
("A2", "obrzydliwy", "nâa kliat", "น่าเกลียด", "Wrażenie", 3, "adj", CO,
 "Uwaga: znaczy też „brzydki” o wyglądzie — mocniejsze niż polskie „brzydki”.", ""),
("A2", "godny podziwu", "nâa chûeat chooei", "น่าเชิดชู", "Wrażenie", 2, "adj", CO, "", ""),
("A2", "irytujący", "nâa ram-khaan", "น่ารำคาญ", "Wrażenie", 3, "adj", CO, "", ""),

# =========================================================== przysłówki częstości
("A1", "znowu", "ìik", "อีก", "Przysłówki", 5, "adv", GU,
 "Także „jeszcze, dodatkowo” — ao ìik nùeng, poproszę jeszcze jedno.", ""),
("A1", "jeszcze raz", "ìik khráng", "อีกครั้ง", "Przysłówki", 5, "adv", GU, "", ""),
("A1", "prawie", "kùeap", "เกือบ", "Przysłówki", 5, "adv", GU, "", ""),
("A1", "wcale nie", "mâi looei", "ไม่เลย", "Przysłówki", 5, "adv", GU, "", ""),
("A1", "w ogóle (wzmocnienie)", "looei", "เลย", "Przysłówki", 5, "adv", GU, "", ""),
("A1", "akurat, właśnie", "phaw dii", "พอดี", "Przysłówki", 5, "adv", GU,
 "Przy zakupach: „phaw dii” znaczy też „w sam raz” o rozmiarze.", "wystarczająco dobrze"),
("A1", "jednocześnie", "phráwm kan", "พร้อมกัน", "Przysłówki", 3, "adv", GU, "", ""),
("A1", "osobno", "yâek kan", "แยกกัน", "Przysłówki", 4, "adv", GU,
 "Przy płaceniu w restauracji: jàai yâek kan — płacimy osobno.", ""),
("A1", "razem", "ruam kan", "รวมกัน", "Przysłówki", 4, "adv", GU, "", ""),
("A1", "na przemian", "sàp kan", "สลับกัน", "Przysłówki", 2, "adv", GU, "", ""),
("A2", "zazwyczaj", "pòk-kà-tì", "ปกติ", "Przysłówki", 5, "adv", GU, "", ""),
("A2", "czasami", "baang khráng", "บางครั้ง", "Przysłówki", 5, "adv", CD, "", ""),
("A2", "rzadko", "naan naan thii", "นานๆที", "Przysłówki", 4, "adv", CD, "", "długo długo raz"),
("A2", "od czasu do czasu", "pen khráng khraao", "เป็นครั้งคราว", "Przysłówki", 3, "adv", CD, "", ""),
("A2", "coraz bardziej", "yîng khûen", "ยิ่งขึ้น", "Przysłówki", 3, "adv", GU, "", ""),
("A2", "coraz mniej", "náwi long", "น้อยลง", "Przysłówki", 3, "adv", GU, "", ""),
("A2", "wreszcie", "nai thîi sùt", "ในที่สุด", "Przysłówki", 4, "adv", GU, "", "w miejscu ostatnim"),
("A2", "nagle", "yùu dii dii", "อยู่ดีๆ", "Przysłówki", 3, "adv", GU, "", "będąc sobie dobrze"),
("A2", "stopniowo", "kháwi kháwi", "ค่อยๆ", "Przysłówki", 4, "adv", GU, "", ""),
("A2", "od razu", "than thii", "ทันที", "Przysłówki", 4, "adv", GU, "", ""),
("A2", "na razie", "kàwn", "ก่อน", "Przysłówki", 5, "adv", GU,
 "Na końcu zdania znaczy „na razie, najpierw”: pai kàwn ná — to ja idę.", ""),
("A2", "przynajmniej", "yàang náwi", "อย่างน้อย", "Przysłówki", 4, "adv", LI, "", "sposób mało"),
("A2", "najwyżej", "yàang mâak", "อย่างมาก", "Przysłówki", 3, "adv", LI, "", ""),
("A2", "mniej więcej", "prà-maan", "ประมาณ", "Przysłówki", 5, "adv", LI, "", ""),
("A2", "dokładnie", "phaw dii pé", "พอดีเป๊ะ", "Przysłówki", 3, "adv", LI, "", ""),
("A2", "specjalnie, celowo", "tâng jai", "ตั้งใจ", "Przysłówki", 4, "adv", GU, "", "ustawić serce"),
("A2", "przypadkiem", "bang-oen", "บังเอิญ", "Przysłówki", 3, "adv", GU, "", ""),

# =========================================================== reduplikacja
("A1", "powolutku", "cháa cháa", "ช้าๆ", "Reduplikacja", 5, "adv", GU,
 "Powtórzenie osłabia i zmiękcza. „cháa cháa nàwi” to najuprzejmiejsza prośba o wolniejszą mowę.", ""),
("A1", "porządnie, jak należy", "dii dii", "ดีๆ", "Reduplikacja", 4, "adv", GU, "", ""),
("A1", "po cichutku", "bao bao", "เบาๆ", "Reduplikacja", 4, "adv", GU, "", ""),
("A1", "szybciutko", "reo reo", "เร็วๆ", "Reduplikacja", 4, "adv", GU, "", ""),
("A1", "raz za razem", "bàwi bàwi", "บ่อยๆ", "Reduplikacja", 4, "adv", CD, "", ""),
("A2", "gdzieś tam, byle gdzie", "thîi nǎi kâw dâi", "ที่ไหนก็ได้", "Reduplikacja", 4, "adv", MO, "", "gdziekolwiek może być"),
("A2", "cokolwiek", "à-rai kâw dâi", "อะไรก็ได้", "Reduplikacja", 5, "adv", GU,
 "Najczęstsza tajska odpowiedź na pytanie „co zjemy”.", ""),
("A2", "kiedykolwiek", "mûea rài kâw dâi", "เมื่อไหร่ก็ได้", "Reduplikacja", 3, "adv", CD, "", ""),
("A2", "ktokolwiek", "khrai kâw dâi", "ใครก็ได้", "Reduplikacja", 3, "adv", GU, "", ""),

# =========================================================== sposób
("A1", "po tajsku", "bàep thai", "แบบไทย", "Sposób", 4, "adv", ST, "", "sposób tajski"),
("A1", "po europejsku", "bàep fà-ràng", "แบบฝรั่ง", "Sposób", 3, "adv", ST, "", ""),
("A1", "w ten sposób", "bàep níi", "แบบนี้", "Sposób", 5, "adv", GU, "", ""),
("A1", "inaczej", "bàep ùen", "แบบอื่น", "Sposób", 4, "adv", GU, "", "sposób inny"),
("A1", "samodzielnie", "dûai tua eeng", "ด้วยตัวเอง", "Sposób", 4, "adv", GU, "", "przez siebie samego"),
("A1", "na piechotę", "doen pai", "เดินไป", "Sposób", 4, "adv", MO, "", ""),
("A2", "na głos", "àan àwk sǐang", "อ่านออกเสียง", "Sposób", 2, "adv", GU, "", "czytać wydając głos"),
("A2", "po cichu (bez rozgłosu)", "ngîap ngîap", "เงียบๆ", "Sposób", 3, "adv", GU, "", ""),
("A2", "z grubsza", "khràao khràao", "คร่าวๆ", "Sposób", 2, "adv", GU, "", ""),
("A2", "szczegółowo", "yàang lá-ìat", "อย่างละเอียด", "Sposób", 3, "adv", GU, "", ""),
("A2", "z ręki, na oko", "kà-praa", "กะประมาณ", "Sposób", 2, "adv", LI, "", ""),
]
