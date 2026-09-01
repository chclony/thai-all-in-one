# -*- coding: utf-8 -*-
"""Sesja O, partia 17 — CZASOWNIKI ZŁOŻONE I KONSTRUKCJE KIERUNKOWE.

Partia domykająca, celowo najbardziej „gramatyczna”. Tajski buduje ogromną
część czasowników seryjnie: rdzeń plus kierunek albo rdzeń plus wynik.

    + pai / maa     kierunek od mówiącego / do mówiącego
                    (àwk pai wyjść tam, àwk maa wyjść tutaj)
    + khûen / long  w górę / w dół, także wzrost i spadek
                    (raa-khaa khûen cena rośnie)
    + khâo / àwk    do środka / na zewnątrz
    + wái           „na później”, czynność z zapasem (kèp wái odłożyć)
    + dâi           potrafić, zdołać
    + lǒoe / mòt    do końca, całkowicie

Dla uczącego się to zamiana jednego problemu na dwa gotowe: zamiast uczyć
się osobno „wnieść”, „wynieść”, „znieść”, „wnieść na górę”, uczy się jednego
rdzenia i pięciu kierunków. Fonetycznie każdy taki czasownik składa się
z sylab, które baza ma od poziomu A1 — dokładnie ta własność, na której
opiera się cała sesja O.

Druga część partii to **czasowniki z `hâi`** (dawać / sprawiać, że), czyli
tajski sposób na stronę sprawczą: `tham hâi` (sprawić), `chûai hâi` (pomóc,
żeby), `bàwk hâi` (kazać). Bez nich nie da się powiedzieć „to sprawiło, że…”.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

CZ = "Czasowniki"
GU = "Gramatyka użytkowa"
ST = "Small talk"
ZP = "Zakupy i pieniądze"
AW = "Awarie i pomoc"
DC = "Dom i codzienność"
MO = "Miejsca i orientacja"
PN = "Praca i nauka"
CO = "Cechy i opinie"
PY = "Pytania"
CD = "Czas i daty"
LI = "Liczby i liczenie"

MORE = [

# =========================================================== kierunek pai/maa
("A1", "wyjść (stąd tam)", "àwk pai", "ออกไป", "Kierunek", 5, "v", CZ, "", "wyjść iść"),
("A1", "wyjść (do mnie)", "àwk maa", "ออกมา", "Kierunek", 5, "v", CZ, "", "wyjść przyjść"),
("A1", "wejść (tam)", "khâo pai", "เข้าไป", "Kierunek", 5, "v", CZ, "", ""),
("A1", "wejść (tutaj)", "khâo maa", "เข้ามา", "Kierunek", 5, "v", CZ,
 "„chooen khâo maa” — proszę wejść. Najczęstsze zaproszenie do środka.", ""),
("A1", "zanieść (tam)", "ao pai", "เอาไป", "Kierunek", 5, "v", CZ, "", "wziąć iść"),
("A1", "przynieść (tutaj)", "ao maa", "เอามา", "Kierunek", 5, "v", CZ, "", ""),
("A1", "odwieźć", "sòng pai", "ส่งไป", "Kierunek", 4, "v", CZ, "", ""),
("A1", "przywieźć", "sòng maa", "ส่งมา", "Kierunek", 4, "v", CZ, "", ""),
("A1", "pobiec tam", "wîng pai", "วิ่งไป", "Kierunek", 3, "v", CZ, "", ""),
("A1", "przybiec tutaj", "wîng maa", "วิ่งมา", "Kierunek", 3, "v", CZ, "", ""),
("A2", "odsunąć się", "lǒp pai", "หลบไป", "Kierunek", 3, "v", CZ, "", ""),
("A2", "podejść bliżej", "khâo maa klâi klâi", "เข้ามาใกล้ๆ", "Kierunek", 3, "v", CZ, "", ""),

# =========================================================== kierunek khûen/long
("A1", "podnieść się, wzrosnąć", "khûen", "ขึ้น", "Kierunek", 5, "v", CZ, "", ""),
("A1", "opaść, zmniejszyć się", "long", "ลง", "Kierunek", 5, "v", CZ, "", ""),
("A1", "cena rośnie", "raa-khaa khûen", "ราคาขึ้น", "Kierunek", 4, "n", ZP, "", ""),
("A1", "cena spada", "raa-khaa long", "ราคาลง", "Kierunek", 4, "n", ZP, "", ""),
("A1", "wnieść na górę", "yók khûen", "ยกขึ้น", "Kierunek", 3, "v", CZ, "", ""),
("A1", "znieść na dół", "yók long", "ยกลง", "Kierunek", 2, "v", CZ, "", ""),
("A1", "wsiąść (do pojazdu)", "khûen rót", "ขึ้นรถ", "Kierunek", 5, "v", CZ, "", ""),
("A1", "wysiąść (z pojazdu)", "long rót", "ลงรถ", "Kierunek", 5, "v", CZ, "", ""),
("A2", "zapisać się na coś", "long chûe", "ลงชื่อ", "Kierunek", 3, "v", CZ, "", "opuścić imię"),
("A2", "wrzucić do wody", "yoon long nám", "โยนลงน้ำ", "Kierunek", 2, "v", CZ, "", ""),
("A2", "przybrać na wadze", "nám-nàk khûen", "น้ำหนักขึ้น", "Kierunek", 3, "v", CZ, "", ""),
("A2", "zejść ze schodów", "long ban-dai", "ลงบันได", "Kierunek", 3, "v", CZ, "", ""),

# =========================================================== + wái (na później)
("A1", "odłożyć, zachować", "kèp wái", "เก็บไว้", "Zapas", 5, "v", CZ,
 "Przyrostek wái znaczy „na potem”. kèp wái to schować z myślą o przyszłości.", "zbierać zostawić"),
("A1", "zapisać sobie", "jòt wái", "จดไว้", "Zapas", 4, "v", CZ, "", ""),
("A1", "zamówić z wyprzedzeniem", "jawng wái", "จองไว้", "Zapas", 4, "v", CZ, "", ""),
("A1", "przygotować wcześniej", "triam wái", "เตรียมไว้", "Zapas", 4, "v", CZ, "", ""),
("A2", "położyć (i zostawić)", "waang wái", "วางไว้", "Zapas", 4, "v", CZ, "", ""),
("A2", "trzymać dla kogoś", "kèp wái hâi", "เก็บไว้ให้", "Zapas", 3, "v", CZ, "", ""),
("A2", "zapamiętać", "jam wái", "จำไว้", "Zapas", 4, "v", CZ, "", ""),
("A2", "obiecać na przyszłość", "sǎn-yaa wái", "สัญญาไว้", "Zapas", 2, "v", CZ, "", ""),

# =========================================================== + dâi (móc, zdołać)
("A1", "umieć mówić", "phûut dâi", "พูดได้", "Możliwość", 5, "v", CZ, "", ""),
("A1", "umieć czytać", "àan dâi", "อ่านได้", "Możliwość", 4, "v", CZ, "", ""),
("A1", "dać się zjeść, jadalne", "kin dâi", "กินได้", "Możliwość", 5, "v", CZ, "", ""),
("A1", "da się użyć", "chái dâi", "ใช้ได้", "Możliwość", 5, "v", CZ,
 "Także „w porządku, ujdzie” jako ocena.", ""),
("A1", "nie da rady", "mâi wǎi", "ไม่ไหว", "Możliwość", 5, "v", CZ,
 "Różnica wobec mâi dâi: mâi dâi to „nie wolno / nie umiem”, mâi wǎi to „nie mam siły”.", ""),
("A2", "dać radę, wytrzymać", "wǎi", "ไหว", "Możliwość", 4, "v", CZ, "", ""),
("A2", "zdążyć na coś", "than wee-laa", "ทันเวลา", "Możliwość", 4, "v", CZ, "", ""),
("A2", "umieć na pamięć", "jam dâi", "จำได้", "Możliwość", 5, "v", CZ, "", ""),
("A2", "rozpoznać kogoś", "jam nâa dâi", "จำหน้าได้", "Możliwość", 3, "v", CZ, "", "pamiętać twarz móc"),
("A2", "usłyszeć wyraźnie", "dâi yin chát", "ได้ยินชัด", "Możliwość", 3, "v", CZ, "", ""),

# =========================================================== hâi (sprawić, że)
("A1", "sprawić, że", "tham hâi", "ทำให้", "Sprawczość", 5, "v", GU,
 "Konstrukcja przyczynowa: tham hâi phǒm khâo jai — sprawiło, że zrozumiałem.", "robić dawać"),
("A1", "kazać komuś", "bàwk hâi", "บอกให้", "Sprawczość", 4, "v", GU, "", "powiedzieć dawać"),
("A1", "pozwolić komuś", "hâi ... dâi", "ให้…ได้", "Sprawczość", 4, "w", GU, "", ""),
("A1", "pomóc, żeby", "chûai hâi", "ช่วยให้", "Sprawczość", 4, "v", GU, "", ""),
("A1", "zrobić dla kogoś", "tham hâi khon ùen", "ทำให้คนอื่น", "Sprawczość", 3, "v", GU, "", ""),
("A2", "poprosić kogoś, żeby", "khǎw hâi", "ขอให้", "Sprawczość", 4, "v", GU, "", ""),
("A2", "wysłać kogoś, żeby", "chái hâi", "ใช้ให้", "Sprawczość", 2, "v", GU, "", ""),
("A2", "przekazać komuś", "fàak hâi", "ฝากให้", "Sprawczość", 3, "v", GU, "", ""),
("A2", "kupić komuś", "súe hâi", "ซื้อให้", "Sprawczość", 4, "v", GU, "", ""),
("A2", "zrobić za kogoś", "tham thaen hâi", "ทำแทนให้", "Sprawczość", 2, "v", GU, "", ""),

# =========================================================== + mòt, lǒoe (do końca)
("A1", "zjeść do końca", "kin mòt", "กินหมด", "Zakończenie", 4, "v", CZ, "", "jeść wyczerpać"),
("A1", "skończyć się (zapas)", "mòt", "หมด", "Zakończenie", 5, "v", CZ,
 "W sklepie: „mòt láew khráp” — skończyło się.", ""),
("A1", "wydać wszystko", "chái mòt", "ใช้หมด", "Zakończenie", 4, "v", CZ, "", ""),
("A1", "sprzedać wszystko", "khǎai mòt", "ขายหมด", "Zakończenie", 4, "v", CZ, "", ""),
("A2", "zapomnieć zupełnie", "luem mòt", "ลืมหมด", "Zakończenie", 3, "v", CZ, "", ""),
("A2", "przesadzić, przekroczyć miarę", "kooen pai", "เกินไป", "Zakończenie", 5, "adv", GU, "", ""),
("A2", "wystarczająco", "phaw", "พอ", "Zakończenie", 5, "adv", GU, "", ""),
("A2", "niemal skończone", "kùeap sèt", "เกือบเสร็จ", "Zakończenie", 4, "adj", CO, "", ""),

# =========================================================== próba i powtórzenie
("A1", "spróbować", "lawng", "ลอง", "Próba", 5, "v", CZ,
 "lawng chim — spróbować smaku, lawng sài — przymierzyć.", ""),
("A1", "przymierzyć", "lawng sài", "ลองใส่", "Próba", 5, "v", CZ, "", "spróbować włożyć"),
("A1", "spróbować smaku", "lawng chim", "ลองชิม", "Próba", 5, "v", CZ, "", ""),
("A1", "spróbować jeszcze raz", "lawng ìik thii", "ลองอีกที", "Próba", 4, "v", CZ, "", ""),
("A2", "ćwiczyć, wprawiać się", "fùek", "ฝึก", "Próba", 4, "v", CZ, "", ""),
("A2", "powtarzać (ćwiczenie)", "tham sám", "ทำซ้ำ", "Próba", 3, "v", CZ, "", ""),
("A2", "przyzwyczaić się do", "chin kàp", "ชินกับ", "Próba", 3, "v", CZ, "", ""),
("A2", "zdarzyło mi się (kiedyś)", "khooei", "เคย", "Próba", 5, "v", GU,
 "Wskaźnik doświadczenia: khooei pai mǎi — byłeś tam kiedyś?", ""),
("A2", "nigdy nie (doświadczenie)", "mâi khooei", "ไม่เคย", "Próba", 5, "v", GU, "", ""),

# =========================================================== czas czynności
("A1", "właśnie robię", "kam-lang ... yùu", "กำลัง…อยู่", "Aspekt", 5, "w", GU,
 "Otoczka kam-lang … yùu opisuje czynność trwającą teraz.", ""),
("A1", "dopiero co zrobiłem", "phôeng ... pai", "เพิ่ง…ไป", "Aspekt", 4, "w", GU, "", ""),
("A1", "zaraz zrobię", "kam-lang jà", "กำลังจะ", "Aspekt", 4, "w", GU, "", ""),
("A1", "jeszcze nie zrobiłem", "yang mâi dâi", "ยังไม่ได้", "Aspekt", 5, "w", GU, "", ""),
("A1", "już zrobiłem", "tham láew", "ทำแล้ว", "Aspekt", 5, "w", GU, "", ""),
("A2", "zwykle robię", "pòk-kà-tì jà", "ปกติจะ", "Aspekt", 4, "w", GU, "", ""),
("A2", "kiedyś robiłem", "mûea kàwn khooei", "เมื่อก่อนเคย", "Aspekt", 3, "w", GU, "", ""),
("A2", "będę robić dalej", "jà tham tàw", "จะทำต่อ", "Aspekt", 3, "w", GU, "", ""),
("A2", "przestać robić", "lôek tham", "เลิกทำ", "Aspekt", 4, "v", CZ, "", ""),
("A2", "zacząć od nowa", "rôoem mài", "เริ่มใหม่", "Aspekt", 4, "v", CZ, "", ""),

# =========================================================== porównania
("A1", "taki sam jak", "mǔean kan kàp", "เหมือนกันกับ", "Porównania", 5, "w", GU, "", ""),
("A1", "inny niż", "tàang jàak", "ต่างจาก", "Porównania", 4, "w", GU, "", ""),
("A1", "podobny do", "khláai kàp", "คล้ายกับ", "Porównania", 4, "w", GU, "", ""),
("A1", "lepszy niż", "dii kwàa", "ดีกว่า", "Porównania", 5, "w", GU, "", ""),
("A1", "najlepszy", "dii thîi sùt", "ดีที่สุด", "Porównania", 5, "w", GU, "", ""),
("A1", "gorszy niż", "yâe kwàa", "แย่กว่า", "Porównania", 4, "w", GU, "", ""),
("A2", "równie ... jak", "phaw phaw kàp", "พอๆกับ", "Porównania", 3, "w", GU, "", ""),
("A2", "im więcej, tym lepiej", "yîng mâak yîng dii", "ยิ่งมากยิ่งดี", "Porównania", 3, "w", GU, "", ""),
("A2", "w porównaniu z", "mûea thîap kàp", "เมื่อเทียบกับ", "Porównania", 3, "w", GU, "", ""),
("A2", "raczej (wolę)", "châwp ... mâak kwàa", "ชอบ…มากกว่า", "Porównania", 4, "w", GU, "", ""),

# =========================================================== pytania i tryb
("A1", "Czy mógłbyś…?", "chûai ... nàwi dâi mǎi khráp", "ช่วย…หน่อยได้ไหมครับ", "Prośby", 5, "w", PY, "", ""),
("A1", "Czy wolno mi…?", "phǒm ... dâi mǎi khráp", "ผม…ได้ไหมครับ", "Prośby", 5, "w", PY, "", ""),
("A1", "Lepiej nie.", "mâi dii kwàa khráp", "ไม่ดีกว่าครับ", "Prośby", 4, "w", ST, "", ""),
("A1", "Może lepiej…", "sùu ... dii kwàa", "สู้…ดีกว่า", "Prośby", 2, "w", ST, "", ""),
("A2", "Nie musisz.", "mâi tâwng khráp", "ไม่ต้องครับ", "Prośby", 5, "w", ST,
 "Odmowa oferty: „mâi tâwng, khàwp khun khráp” — nie trzeba, dziękuję.", ""),
("A2", "Trzeba było wcześniej.", "khuan tham tâng tàe raek khráp", "ควรทำตั้งแต่แรกครับ", "Prośby", 2, "w", ST, "", ""),
("A2", "Powinieneś…", "khuan jà", "ควรจะ", "Prośby", 4, "w", GU, "", ""),
("A2", "Nie powinieneś…", "mâi khuan jà", "ไม่ควรจะ", "Prośby", 4, "w", GU, "", ""),
("A2", "Wolno mi?", "dâi mǎi khráp", "ได้ไหมครับ", "Prośby", 5, "w", PY, "", ""),
("A2", "A gdyby…?", "thâa ... lâ khráp", "ถ้า…ล่ะครับ", "Prośby", 3, "w", PY, "", ""),
]
