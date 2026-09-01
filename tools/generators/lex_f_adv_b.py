# -*- coding: utf-8 -*-
"""Sesja F — PRZYSLOWKI II: czas, pewnosc, kolejnosc, ilosc.

Uwaga systemowa: tajski przysłówek stopnia stoi PO czasowniku lub
przymiotniku („phûut cháa cháa” — mów wolno), a przyslowek czasu
zwykle na poczatku zdania („phrûng-níi phǒm pai”). Ta kolejnosc jest
sztywniejsza niz w polskim.
"""

GU = "Gramatyka użytkowa"
CD = "Czas i daty"

ADV_B = [

# ------------------------------------------------------------------ czas
("A2", "właśnie teraz", "tawn níi", "ตอนนี้", CD, "Czas", 5, "n",
 "„tawn” to odcinek czasu. „tawn níi” różni się od „diǎo níi”, które znaczy „za chwilę”.",
 "moment ten",
 [("Teraz jestem zajęty.", "tawn níi phǒm mâi wâang khráp", "ตอนนี้ผมไม่ว่างครับ"),
  ("Gdzie pan teraz jest?", "tawn níi yùu nǎi khráp", "ตอนนี้อยู่ไหนครับ")],
 ["zaraz", "zajęty (o osobie)"], ["teraz"]),

("A2", "zaraz", "diǎo", "เดี๋ยว", CD, "Czas", 5, "p",
 "„diǎo” samo znaczy „chwilę”. Powtórzone „diǎo diǎo” to „momencik”. Bywa elastyczne czasowo.",
 "",
 [("Zaraz przyjdę.", "diǎo maa khráp", "เดี๋ยวมาครับ"),
  ("Chwileczkę.", "diǎo ná khráp", "เดี๋ยวนะครับ")],
 ["właśnie teraz", "czekać"], ["chwilę"]),

("A2", "dopiero co", "phôoeng", "เพิ่ง", CD, "Czas", 4, "n",
 "Stoi przed czasownikiem: „phôoeng maa” — dopiero przyszedłem. Nie mylić z „phôoem” (dodać).",
 "",
 [("Dopiero przyjechałem.", "phǒm phôoeng maa thǔeng khráp", "ผมเพิ่งมาถึงครับ"),
  ("Dopiero co jadłem.", "phǒm phôoeng kin khâao khráp", "ผมเพิ่งกินข้าวครับ")],
 ["niedawno", "przychodzić", "dodatkowy"], []),

("A2", "wkrótce", "reo reo níi", "เร็วๆนี้", CD, "Czas", 3, "n",
 "Powtórzenie „reo reo” łagodzi i uogólnia — nie oznacza konkretnego terminu.",
 "szybko szybko ten",
 [("Wkrótce się spotkamy.", "jooe kan reo reo níi khráp", "เจอกันเร็วๆนี้ครับ"),
  ("Wkrótce wyjeżdżam.", "phǒm jà pai reo reo níi khráp", "ผมจะไปเร็วๆนี้ครับ")],
 ["szybko", "spotykać się"], []),

("A2", "wcześniej", "kàwn nâa níi", "ก่อนหน้านี้", CD, "Czas", 3, "n",
 "Formalniejsze od samego „kàwn”. Przydatne przy opowiadaniu kolejności zdarzeń.",
 "przed twarz ten",
 [("Wcześniej tu mieszkałem.", "kàwn nâa níi phǒm yùu thîi nîi khráp", "ก่อนหน้านี้ผมอยู่ที่นี่ครับ"),
  ("Wcześniej było taniej.", "kàwn nâa níi thùuk kwàa khráp", "ก่อนหน้านี้ถูกกว่าครับ")],
 ["zanim", "potem", "tani"], []),

("A2", "od tamtej pory", "tâng tàe nán", "ตั้งแต่นั้น", CD, "Czas", 2, "f",
 "„tâng tàe” to „począwszy od” — także o godzinie: „tâng tàe cháo”.",
 "ustawiać od tamten",
 [("Od tamtej pory go nie widziałem.", "tâng tàe nán phǒm mâi jooe kháo loei khráp", "ตั้งแต่นั้นผมไม่เจอเขาเลยครับ"),
  ("Czekam od rana.", "phǒm raw tâng tàe cháo khráp", "ผมรอตั้งแต่เช้าครับ")],
 ["potem", "czekać", "rano"], []),

("A2", "nagle", "yùu dii dii kâw", "อยู่ดีๆก็", CD, "Czas", 2, "p",
 "Dosłownie „będąc sobie dobrze, nagle”. Wyrażenie mocno potoczne, częste w opowieściach.",
 "być dobrze i",
 [("Nagle zaczęło padać.", "yùu dii dii kâw fǒn tòk khráp", "อยู่ดีๆก็ฝนตกครับ"),
  ("Nagle zniknął.", "yùu dii dii kâw hǎai pai khráp", "อยู่ดีๆก็หายไปครับ")],
 ["deszcz", "gubić"], []),

("A2", "wreszcie", "nai thîi sùt", "ในที่สุด", CD, "Czas", 3, "f",
 "„thîi sùt” to ten sam element co w stopniu najwyższym: „dii thîi sùt”.",
 "w miejsce koniec",
 [("Wreszcie dojechałem.", "nai thîi sùt phǒm kâw thǔeng khráp", "ในที่สุดผมก็ถึงครับ"),
  ("Wreszcie skończone.", "nai thîi sùt kâw sèt khráp", "ในที่สุดก็เสร็จครับ")],
 ["na końcu", "gotowy", "docierać"], []),

("A2", "na razie", "pai kàwn", "ไปก่อน", CD, "Czas", 4, "p",
 "„… pai kàwn” na końcu zdania znaczy „na razie, tymczasem”. Także w pożegnaniu: „pai kàwn ná”.",
 "iść przed",
 [("Na razie wystarczy.", "phaw kâwn khráp", "พอก่อนครับ"),
  ("To ja się już zbieram.", "pai kàwn ná khráp", "ไปก่อนนะครับ")],
 ["zanim", "wystarczy", "żegnać się"], []),

("A2", "za każdym razem", "thúk khráng", "ทุกครั้ง", CD, "Częstotliwość", 3, "n",
 "„khráng” to raz, przypadek. „khráng nâa” to następnym razem.",
 "każdy raz",
 [("Za każdym razem jest korek.", "rót tìt thúk khráng khráp", "รถติดทุกครั้งครับ"),
  ("Następnym razem przyjdę wcześniej.", "khráng nâa jà maa reo khûen khráp", "ครั้งหน้าจะมาเร็วขึ้นครับ")],
 ["korek uliczny", "zawsze", "raz"], []),

("A2", "rzadko", "nâan nâan thii", "นานๆที", CD, "Częstotliwość", 3, "p",
 "Dosłownie „raz na długo”. Wyrażenie potoczne i bardzo częste w mowie.",
 "długo długo raz",
 [("Rzadko tu przychodzę.", "phǒm maa nâan nâan thii khráp", "ผมมานานๆทีครับ"),
  ("Rzadko piję alkohol.", "phǒm dùem lâo nâan nâan thii khráp", "ผมดื่มเหล้านานๆทีครับ")],
 ["często", "alkohol"], []),

("A2", "prawie nigdy", "mâi khâwi … loei", "ไม่ค่อย…เลย", CD, "Częstotliwość", 3, "n",
 "Konstrukcja rozdzielna: „mâi khâwi” przed czasownikiem, „loei” na końcu zdania.",
 "nie bardzo wcale",
 [("Prawie nigdy nie gotuję.", "phǒm mâi khâwi tham aa-hǎan loei khráp", "ผมไม่ค่อยทำอาหารเลยครับ"),
  ("Prawie tam nie bywam.", "phǒm mâi khâwi pai loei khráp", "ผมไม่ค่อยไปเลยครับ")],
 ["rzadko", "nigdy", "gotować"], []),

# --------------------------------------------------------------- pewnosc
("A2", "chyba", "khong jà", "คงจะ", GU, "Pewność", 4, "n",
 "Wyraża przypuszczenie z dużym prawdopodobieństwem. Słabsze niż „nâe nawn” (na pewno).",
 "prawdopodobnie będzie",
 [("Chyba będzie padać.", "khong jà fǒn tòk khráp", "คงจะฝนตกครับ"),
  ("Chyba jest zamknięte.", "khong jà pìt láew khráp", "คงจะปิดแล้วครับ")],
 ["na pewno", "może", "deszcz"], ["prawdopodobnie"]),

("A2", "może", "àat jà", "อาจจะ", GU, "Pewność", 4, "n",
 "Słabsza pewność niż „khong jà”. Przydatne przy uprzejmym niezobowiązywaniu się.",
 "może będzie",
 [("Może przyjdę.", "phǒm àat jà maa khráp", "ผมอาจจะมาครับ"),
  ("Może być drogo.", "àat jà phaeng khráp", "อาจจะแพงครับ")],
 ["chyba", "na pewno"], []),

("A2", "na pewno", "nâe nawn", "แน่นอน", GU, "Pewność", 4, "n",
 "Także samodzielna odpowiedź: „nâe nawn khráp” — oczywiście.",
 "",
 [("Na pewno przyjdę.", "phǒm maa nâe nawn khráp", "ผมมาแน่นอนครับ"),
  ("Oczywiście.", "nâe nawn khráp", "แน่นอนครับ")],
 ["chyba", "może", "obiecywać"], ["oczywiście"]),

("A2", "podobno", "dâi yin wâa", "ได้ยินว่า", GU, "Pewność", 3, "n",
 "Dosłownie „słyszałem, że”. Sposób na przekazanie informacji bez brania za nią odpowiedzialności.",
 "słyszeć że",
 [("Podobno jest tam tanio.", "dâi yin wâa thîi nân thùuk khráp", "ได้ยินว่าที่นั่นถูกครับ"),
  ("Podobno zamknęli.", "dâi yin wâa pìt láew khráp", "ได้ยินว่าปิดแล้วครับ")],
 ["słyszeć", "tani", "zamknięty"], []),

("A2", "moim zdaniem", "khít wâa", "คิดว่า", GU, "Pewność", 5, "n",
 "Dosłownie „myślę, że”. Łagodzi opinię — bezpośrednie sądy bywają odbierane jako zbyt stanowcze.",
 "myśleć że",
 [("Moim zdaniem to za drogo.", "phǒm khít wâa phaeng koen pai khráp", "ผมคิดว่าแพงเกินไปครับ"),
  ("Myślę, że tak.", "khít wâa châi khráp", "คิดว่าใช่ครับ")],
 ["myśleć", "drogi (kosztowny)"], ["myślę, że"]),

("A2", "wcale nie", "mâi … loei", "ไม่…เลย", GU, "Pewność", 4, "n",
 "„loei” na końcu wzmacnia przeczenie do zera: „mâi phèt loei” — wcale nie ostre.",
 "nie wcale",
 [("Wcale nie jest ostre.", "mâi phèt loei khráp", "ไม่เผ็ดเลยครับ"),
  ("Wcale nie rozumiem.", "mâi khâo jai loei khráp", "ไม่เข้าใจเลยครับ")],
 ["ostry", "rozumieć", "prawie nigdy"], []),

("A2", "raczej nie", "khong mâi", "คงไม่", GU, "Pewność", 3, "n",
 "Uprzejma odmowa bez kategorycznego „nie” — forma bardzo tajska.",
 "prawdopodobnie nie",
 [("Raczej nie dam rady.", "khong mâi wǎang khráp", "คงไม่ว่างครับ"),
  ("Raczej nie będzie padać.", "khong mâi tòk khráp", "คงไม่ตกครับ")],
 ["chyba", "zajęty (o osobie)"], []),

# --------------------------------------------------------------- kolejnosc
("A2", "najpierw", "an dàp râek", "อันดับแรก", GU, "Kolejność", 3, "f",
 "Formalne wyliczenie. W mowie codziennej wystarczy samo „kàwn”.",
 "pozycja pierwszy",
 [("Najpierw zapłacę.", "an dàp râek jàai kàwn khráp", "อันดับแรกจ่ายก่อนครับ"),
  ("Najpierw to.", "an níi kàwn khráp", "อันนี้ก่อนครับ")],
 ["zanim", "pierwszy", "płacić"], []),

("A2", "następnie", "tàw maa", "ต่อมา", GU, "Kolejność", 3, "n",
 "„tàw” to ten sam czasownik co „kontynuować, podłączyć”.",
 "kontynuować przychodzić",
 [("Następnie poszliśmy na targ.", "tàw maa rao pai tà-làat khráp", "ต่อมาเราไปตลาดครับ"),
  ("A co potem?", "tàw maa lâ khráp", "ต่อมาล่ะครับ")],
 ["po tym jak", "podłączać", "targ"], []),

("A2", "jednocześnie", "phráwm kan", "พร้อมกัน", GU, "Kolejność", 3, "n",
 "„phráwm” samo znaczy „gotowy”. „phráwm kan” to „razem, w tym samym momencie”.",
 "gotowy razem",
 [("Wyszliśmy jednocześnie.", "rao àwk phráwm kan khráp", "เราออกพร้อมกันครับ"),
  ("Jesteśmy gotowi.", "rao phráwm láew khráp", "เราพร้อมแล้วครับ")],
 ["gotowy", "razem"], []),

("A2", "osobno", "yâek kan", "แยกกัน", GU, "Kolejność", 3, "n",
 "„yâek” to rozdzielić. Kluczowe przy płaceniu: „jàai yâek kan”.",
 "rozdzielać razem",
 [("Płacimy osobno.", "jàai yâek kan khráp", "จ่ายแยกกันครับ"),
  ("Proszę zapakować osobno.", "yâek thǔng hâi nòi khráp", "แยกถุงให้หน่อยครับ")],
 ["rachunek", "razem", "reklamówka"], []),

# ------------------------------------------------------------------ ilosc
("A2", "mniej więcej", "prà-maan", "ประมาณ", GU, "Ilość", 4, "n",
 "Także „około” przy godzinie i cenie: „prà-maan hâa moong”.",
 "",
 [("Mniej więcej sto batów.", "prà-maan nùeng ráwi bàat khráp", "ประมาณหนึ่งร้อยบาทครับ"),
  ("Około godziny.", "prà-maan nùeng chûa-moong khráp", "ประมาณหนึ่งชั่วโมงครับ")],
 ["około", "cena", "godzina"], ["około"]),

("A2", "co najmniej", "yàang nói", "อย่างน้อย", GU, "Ilość", 3, "n",
 "Para z „yàang mâak” — co najwyżej. Oba przydatne przy negocjacji terminu.",
 "rodzaj mało",
 [("Co najmniej dwa dni.", "yàang nói sǎwng wan khráp", "อย่างน้อยสองวันครับ"),
  ("Co najwyżej tydzień.", "yàang mâak nùeng aa-thít khráp", "อย่างมากหนึ่งอาทิตย์ครับ")],
 ["dzień", "tydzień", "mało"], []),

("A2", "coraz bardziej", "… khûen rûeai rûeai", "ขึ้นเรื่อยๆ", GU, "Ilość", 3, "n",
 "„khûen” to „w górę”. Dodane po przymiotniku daje wzrost natężenia.",
 "w górę stopniowo",
 [("Jest coraz drożej.", "phaeng khûen rûeai rûeai khráp", "แพงขึ้นเรื่อยๆครับ"),
  ("Coraz lepiej mówisz.", "phûut dii khûen rûeai rûeai khráp", "พูดดีขึ้นเรื่อยๆครับ")],
 ["wchodzić na górę", "drogi (kosztowny)", "lepszy"], []),

("A2", "trochę za bardzo", "… pai nòi", "ไปหน่อย", GU, "Ilość", 4, "p",
 "Łagodniejsze niż „koen pai” (za bardzo). Uprzejmy sposób na zgłoszenie zastrzeżenia.",
 "iść trochę",
 [("Trochę za ostre.", "phèt pai nòi khráp", "เผ็ดไปหน่อยครับ"),
  ("Trochę za drogo.", "phaeng pai nòi khráp", "แพงไปหน่อยครับ")],
 ["za bardzo", "ostry", "drogi (kosztowny)"], []),

("A2", "równo", "phaw dii", "พอดี", GU, "Ilość", 4, "n",
 "„phaw dii” to „w sam raz” — o rozmiarze, ilości, cenie i czasie.",
 "wystarczy dobrze",
 [("W sam raz.", "phaw dii khráp", "พอดีครับ"),
  ("Mam odliczone.", "phǒm mii ngoen phaw dii khráp", "ผมมีเงินพอดีครับ")],
 ["wystarczy", "rozmiar", "reszta"], ["w sam raz"]),

("A2", "tylko trochę", "nít diao", "นิดเดียว", GU, "Ilość", 4, "p",
 "Mocniejsze niż „nít nòi” — podkreśla, że naprawdę niewiele.",
 "trochę jeden",
 [("Tylko troszkę.", "nít diao khráp", "นิดเดียวครับ"),
  ("Mówię tylko trochę po tajsku.", "phǒm phûut thai dâai nít diao khráp", "ผมพูดไทยได้นิดเดียวครับ")],
 ["mało", "mówić", "język (mowa)"], []),

("A2", "w ogóle", "tháng mòt", "ทั้งหมด", GU, "Ilość", 4, "n",
 "„tháng mòt thâo-rài” to „ile w sumie” — najważniejsze pytanie przy rachunku.",
 "cały wyczerpany",
 [("Ile w sumie?", "tháng mòt thâo-rài khráp", "ทั้งหมดเท่าไหร่ครับ"),
  ("To wszystko.", "tháng mòt khráp", "ทั้งหมดครับ")],
 ["rachunek", "razem", "cena"], ["w sumie"]),
]
