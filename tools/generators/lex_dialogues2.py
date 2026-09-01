# -*- coding: utf-8 -*-
"""Dialogi etapu 2 (nr 35 i dalsze).

Format identyczny jak w lex_dialogues.py:
    (tytul, sytuacja, poziom, rolaA, rolaB, linie, notatka)
Linia: (rola, polski, fonetyka, tajski)
"""

DIALOGUES2 = [

("Poznajemy się na plaży", "Small talk", "A1", "Turysta", "Tajka", [
 ("B", "Dzień dobry. Skąd pan jest?", "sawàt-dii khâ maa jàak thîi nǎi khá", "สวัสดีค่ะ มาจากที่ไหนคะ"),
 ("A", "Jestem z Polski.", "phǒm maa jàak poo-laen khráp", "ผมมาจากโปแลนด์ครับ"),
 ("B", "Pierwszy raz w Tajlandii?", "maa mueang thai khráng râek rǔe plào khá", "มาเมืองไทยครั้งแรกหรือเปล่าคะ"),
 ("A", "Tak, pierwszy raz.", "châi khráp khráng râek", "ใช่ครับ ครั้งแรก"),
 ("B", "I jak się panu podoba?", "châwp mǎi khá", "ชอบไหมคะ"),
 ("A", "Bardzo. Ludzie są mili.", "châwp mâak khráp khon jai dii", "ชอบมากครับ คนใจดี"),
 ("B", "Jak długo pan zostaje?", "yùu naan thâo-rài khá", "อยู่นานเท่าไหร่คะ"),
 ("A", "Dwa tygodnie.", "sǎwng aa-thít khráp", "สองอาทิตย์ครับ"),
 ("B", "Miłego pobytu.", "khǎw hâi sà-nùk ná khá", "ขอให้สนุกนะคะ"),
 ("A", "Dziękuję bardzo.", "khàwp-khun mâak khráp", "ขอบคุณมากครับ"),
], "„maa jàak” = pochodzić skądś. „khráng râek” = pierwszy raz."),

("Pytanie o drogę do świątyni", "Miejsca i orientacja", "Survival", "Turysta", "Przechodzień", [
 ("A", "Przepraszam, mogę o coś zapytać?", "khǎw thôot khráp thǎam nòi dâai mǎi khráp", "ขอโทษครับ ถามหน่อยได้ไหมครับ"),
 ("B", "Proszę bardzo.", "dâai khráp", "ได้ครับ"),
 ("A", "Gdzie jest ta świątynia?", "wát níi yùu thîi nǎi khráp", "วัดนี้อยู่ที่ไหนครับ"),
 ("B", "Prosto, potem w lewo.", "trong pai láew líao sáai khráp", "ตรงไปแล้วเลี้ยวซ้ายครับ"),
 ("A", "Czy to daleko?", "klai mǎi khráp", "ไกลไหมครับ"),
 ("B", "Niedaleko, pięć minut pieszo.", "mâi klai dəən hâa naa-thii khráp", "ไม่ไกล เดินห้านาทีครับ"),
 ("A", "Dziękuję bardzo.", "khàwp-khun mâak khráp", "ขอบคุณมากครับ"),
 ("B", "Nie ma sprawy.", "mâi pen rai khráp", "ไม่เป็นไรครับ"),
], "„thǎam nòi dâai mǎi” — uprzejme wprowadzenie do każdego pytania na ulicy."),

("Kupno karty SIM", "Zakupy i pieniądze", "A1", "Turysta", "Sprzedawca", [
 ("A", "Dzień dobry, chcę kupić kartę SIM.", "sawàt-dii khráp phǒm yàak súe sim khráp", "สวัสดีครับ ผมอยากซื้อซิมครับ"),
 ("B", "Na ile dni?", "chái kìi wan khráp", "ใช้กี่วันครับ"),
 ("A", "Na dwa tygodnie.", "sǎwng aa-thít khráp", "สองอาทิตย์ครับ"),
 ("B", "Ta jest za trzysta bahtów.", "an níi sǎam ráwi bàat khráp", "อันนี้สามร้อยบาทครับ"),
 ("A", "Czy internet jest bez limitu?", "net mâi jam-kàt chái mǎi khráp", "เน็ตไม่จำกัดใช่ไหมครับ"),
 ("B", "Tak, bez limitu.", "châi khráp mâi jam-kàt", "ใช่ครับ ไม่จำกัด"),
 ("A", "Poproszę paszport?", "tâwng chái pháat-sà-pàwt mǎi khráp", "ต้องใช้พาสปอร์ตไหมครับ"),
 ("B", "Tak, poproszę.", "khǎw dûai khráp", "ขอด้วยครับ"),
 ("A", "Proszę bardzo.", "nîi khráp", "นี่ครับ"),
 ("B", "Chwileczkę, zaraz włożę kartę.", "sàk khrûu ná khráp dǐao sài hâi", "สักครู่นะครับ เดี๋ยวใส่ให้"),
], "Do zakupu karty SIM paszport jest wymagany przepisami."),

("Na targu: targowanie o cenę", "Zakupy i pieniądze", "Survival", "Turysta", "Sprzedawczyni", [
 ("A", "Ile kosztuje ta koszulka?", "sûea tua níi thâo-rài khráp", "เสื้อตัวนี้เท่าไหร่ครับ"),
 ("B", "Czterysta bahtów.", "sìi ráwi bàat khâ", "สี่ร้อยบาทค่ะ"),
 ("A", "To dla mnie za drogo.", "phaeng pai sǎmràp phǒm khráp", "แพงไปสำหรับผมครับ"),
 ("B", "To ile pan da?", "hâi thâo-rài khá", "ให้เท่าไหร่คะ"),
 ("A", "Dwieście pięćdziesiąt?", "sǎwng ráwi hâa-sìp dâai mǎi khráp", "สองร้อยห้าสิบได้ไหมครับ"),
 ("B", "Trzysta, ostatnie słowo.", "sǎam ráwi ná khá lót mâi dâai láew", "สามร้อยนะคะ ลดไม่ได้แล้ว"),
 ("A", "Dobrze, wezmę dwie.", "dâai khráp ao sǎwng tua", "ได้ครับ เอาสองตัว"),
 ("B", "Dziękuję bardzo.", "khàwp-khun mâak khâ", "ขอบคุณมากค่ะ"),
], "Targuj się z uśmiechem. Kupno dwóch sztuk to naturalny argument za zniżką."),

("W kawiarni: mrożona kawa", "Restauracja", "Survival", "Klient", "Barista", [
 ("B", "Dzień dobry, co podać?", "sawàt-dii khâ ráp à-rai dii khá", "สวัสดีค่ะ รับอะไรดีคะ"),
 ("A", "Poproszę mrożoną kawę.", "khǎw kaa-fae yen nòi khráp", "ขอกาแฟเย็นหน่อยครับ"),
 ("B", "Słodką?", "wǎan mǎi khá", "หวานไหมคะ"),
 ("A", "Poproszę bez cukru.", "khǎw mâi sài náam-taan khráp", "ขอไม่ใส่น้ำตาลครับ"),
 ("B", "Na miejscu czy na wynos?", "thaan thîi nîi rǔe klàp bâan khá", "ทานที่นี่หรือกลับบ้านคะ"),
 ("A", "Na miejscu.", "thaan thîi nîi khráp", "ทานที่นี่ครับ"),
 ("B", "Sześćdziesiąt bahtów.", "hòk-sìp bàat khâ", "หกสิบบาทค่ะ"),
 ("A", "Proszę. Czy jest wi-fi?", "nîi khráp mii wai-fai mǎi khráp", "นี่ครับ มีไวไฟไหมครับ"),
 ("B", "Jest, hasło na paragonie.", "mii khâ rá-hàt yùu nai bai sèt", "มีค่ะ รหัสอยู่ในใบเสร็จ"),
], "„wǎan mǎi” — pytanie o słodkość zadaje się przy niemal każdym napoju."),

("Zamawianie jedzenia na wynos", "Restauracja", "Survival", "Klient", "Sprzedawca", [
 ("A", "Poproszę smażony ryż z kurczakiem.", "khǎw khâao phàt kài nòi khráp", "ขอข้าวผัดไก่หน่อยครับ"),
 ("B", "Ostro?", "phèt mǎi khráp", "เผ็ดไหมครับ"),
 ("A", "Poproszę mniej ostro.", "khǎw phèt náwi náwi khráp", "ขอเผ็ดน้อยๆ ครับ"),
 ("B", "Na wynos?", "klàp bâan mǎi khráp", "กลับบ้านไหมครับ"),
 ("A", "Tak, na wynos.", "châi khráp sài thǔng khráp", "ใช่ครับ ใส่ถุงครับ"),
 ("B", "Pięćdziesiąt bahtów.", "hâa-sìp bàat khráp", "ห้าสิบบาทครับ"),
 ("A", "Proszę. Ile to potrwa?", "nîi khráp chái weelaa naan mǎi khráp", "นี่ครับ ใช้เวลานานไหมครับ"),
 ("B", "Pięć minut.", "hâa naa-thii khráp", "ห้านาทีครับ"),
], "„sài thǔng” dosłownie: włożyć do torby — tak zamawia się na wynos na ulicy."),

("U lekarza: przeziębienie", "Zdrowie", "A1", "Pacjent", "Lekarz", [
 ("B", "Dzień dobry, co dolega?", "sawàt-dii khráp pen à-rai maa khráp", "สวัสดีครับ เป็นอะไรมาครับ"),
 ("A", "Źle się czuję.", "phǒm mâi sà-baai khráp", "ผมไม่สบายครับ"),
 ("B", "Jakie objawy?", "mii aa-kaan yang-ngai khráp", "มีอาการยังไงครับ"),
 ("A", "Kaszlę i mam katar.", "phǒm ai láew kâw náam mûuk lǎi khráp", "ผมไอ แล้วก็น้ำมูกไหลครับ"),
 ("B", "Od kiedy?", "tâng tàe mûea-rài khráp", "ตั้งแต่เมื่อไหร่ครับ"),
 ("A", "Od wczoraj.", "tâng tàe mûea waan khráp", "ตั้งแต่เมื่อวานครับ"),
 ("B", "Ma pan gorączkę?", "mii khâi mǎi khráp", "มีไข้ไหมครับ"),
 ("A", "Trochę.", "nít nòi khráp", "นิดหน่อยครับ"),
 ("B", "To przeziębienie. Dam leki.", "pen wàt khráp jà hâi yaa", "เป็นหวัดครับ จะให้ยา"),
 ("A", "Dziękuję.", "khàwp-khun khráp", "ขอบคุณครับ"),
], "„aa-kaan” = objaw. „khâi” = gorączka."),

("W aptece: lek na ból głowy", "Zdrowie", "Survival", "Klient", "Farmaceutka", [
 ("A", "Dzień dobry, boli mnie głowa.", "sawàt-dii khráp phǒm pùat hǔa khráp", "สวัสดีครับ ผมปวดหัวครับ"),
 ("B", "Ma pan gorączkę?", "mii khâi mǎi khá", "มีไข้ไหมคะ"),
 ("A", "Nie, tylko głowa.", "mâi mii khráp pùat hǔa yàang diao", "ไม่มีครับ ปวดหัวอย่างเดียว"),
 ("B", "To lek przeciwbólowy.", "an níi yaa kâe pùat khâ", "อันนี้ยาแก้ปวดค่ะ"),
 ("A", "Jak to brać?", "kin yang-ngai khráp", "กินยังไงครับ"),
 ("B", "Jedna tabletka po jedzeniu.", "kin nùeng mét lǎng aa-hǎan khâ", "กินหนึ่งเม็ดหลังอาหารค่ะ"),
 ("A", "Ile kosztuje?", "thâo-rài khráp", "เท่าไหร่ครับ"),
 ("B", "Czterdzieści bahtów.", "sìi-sìp bàat khâ", "สี่สิบบาทค่ะ"),
], "„yaa kâe pùat” = lek przeciwbólowy; „mét” = klasyfikator tabletek."),

("Wynajem skutera: kaucja i kask", "Transport", "A1", "Turysta", "Wypożyczalnia", [
 ("A", "Chcę wynająć skuter.", "phǒm yàak châo maw-tə\u0304ə-sai khráp", "ผมอยากเช่ามอเตอร์ไซค์ครับ"),
 ("B", "Na ile dni?", "kìi wan khráp", "กี่วันครับ"),
 ("A", "Na trzy dni.", "sǎam wan khráp", "สามวันครับ"),
 ("B", "Dwieście bahtów za dzień.", "wan lá sǎwng ráwi bàat khráp", "วันละสองร้อยบาทครับ"),
 ("A", "Ile wynosi kaucja?", "ngoen mát-jam thâo-rài khráp", "เงินมัดจำเท่าไหร่ครับ"),
 ("B", "Dwa tysiące bahtów.", "sǎwng phan bàat khráp", "สองพันบาทครับ"),
 ("A", "Czy jest kask?", "mii mùak kan náwk mǎi khráp", "มีหมวกกันน็อคไหมครับ"),
 ("B", "Jest, proszę.", "mii khráp nîi khráp", "มีครับ นี่ครับ"),
 ("A", "Mam prawo jazdy.", "phǒm mii bai khàp khìi khráp", "ผมมีใบขับขี่ครับ"),
 ("B", "Świetnie, proszę podpisać.", "dii khráp sen chûe trong níi", "ดีครับ เซ็นชื่อตรงนี้"),
], "Kask jest obowiązkowy. Zostaw kaucję pieniężną, nie paszport."),

("Autobus: zakup biletu", "Transport", "Survival", "Pasażer", "Kasjerka", [
 ("A", "Poproszę bilet do Chiang Mai.", "khǎw tǔa pai chiang mài khráp", "ขอตั๋วไปเชียงใหม่ครับ"),
 ("B", "Na kiedy?", "wan nǎi khá", "วันไหนคะ"),
 ("A", "Na jutro rano.", "phrûng níi cháo khráp", "พรุ่งนี้เช้าครับ"),
 ("B", "Jest o ósmej i o dziesiątej.", "mii pàet moong kàp sìp moong khâ", "มีแปดโมงกับสิบโมงค่ะ"),
 ("A", "Poproszę o ósmej.", "khǎw pàet moong khráp", "ขอแปดโมงครับ"),
 ("B", "Sześćset bahtów.", "hòk ráwi bàat khâ", "หกร้อยบาทค่ะ"),
 ("A", "Ile trwa podróż?", "chái weelaa naan thâo-rài khráp", "ใช้เวลานานเท่าไหร่ครับ"),
 ("B", "Około dziesięciu godzin.", "pramaan sìp chûa-moong khâ", "ประมาณสิบชั่วโมงค่ะ"),
], "„tǔa” = bilet. Zawsze potwierdź godzinę odjazdu przy kasie."),

("Pociąg: peron i opóźnienie", "Transport", "A1", "Pasażer", "Obsługa", [
 ("A", "Przepraszam, z którego peronu?", "khǎw thôot khráp chaan chaa-laa nǎi khráp", "ขอโทษครับ ชานชาลาไหนครับ"),
 ("B", "Z drugiego.", "chaan chaa-laa thîi sǎwng khráp", "ชานชาลาที่สองครับ"),
 ("A", "O której odjeżdża?", "rót fai àwk kìi moong khráp", "รถไฟออกกี่โมงครับ"),
 ("B", "Ma opóźnienie, o wpół do trzeciej.", "cháa kwàa kam-nòt khráp bàai sǎwng khrûeng", "ช้ากว่ากำหนดครับ บ่ายสองครึ่ง"),
 ("A", "Ile to opóźnienia?", "cháa kìi naa-thii khráp", "ช้ากี่นาทีครับ"),
 ("B", "Trzydzieści minut.", "sǎam-sìp naa-thii khráp", "สามสิบนาทีครับ"),
 ("A", "Rozumiem, dziękuję.", "khâo jai láew khráp khàwp-khun", "เข้าใจแล้วครับ ขอบคุณ"),
 ("B", "Proszę bardzo.", "yin dii khráp", "ยินดีครับ"),
], "„chaan chaa-laa” = peron; „bàai sǎwng khrûeng” = wpół do trzeciej po południu."),

("Hotel: wymeldowanie i bagaż", "Hotel", "A1", "Gość", "Recepcja", [
 ("A", "Dzień dobry, chcę się wymeldować.", "sawàt-dii khráp khǎw chék áo khráp", "สวัสดีครับ ขอเช็คเอาท์ครับ"),
 ("B", "Numer pokoju?", "hâwng bəə à-rai khá", "ห้องเบอร์อะไรคะ"),
 ("A", "Pokój dwieście dwa.", "hâwng sǎwng sǔun sǎwng khráp", "ห้องสองศูนย์สองครับ"),
 ("B", "Chwileczkę, sprawdzę.", "sàk khrûu ná khá dǐao trùat duu", "สักครู่นะคะ เดี๋ยวตรวจดู"),
 ("A", "Czy mogę zostawić bagaż do wieczora?", "fàak krà-pǎo thǔeng yen dâai mǎi khráp", "ฝากกระเป๋าถึงเย็นได้ไหมครับ"),
 ("B", "Oczywiście, bez opłat.", "dâai khâ mâi mii khâa tham-niam", "ได้ค่ะ ไม่มีค่าธรรมเนียม"),
 ("A", "Świetnie, dziękuję.", "dii mâak khráp khàwp-khun", "ดีมากครับ ขอบคุณ"),
 ("B", "Zapraszamy ponownie.", "maa mài ná khá", "มาใหม่นะคะ"),
], "„fàak” = zostawić na przechowanie."),

("Hotel: prośba o koc", "Hotel", "Survival", "Gość", "Recepcja", [
 ("A", "Dzień dobry, mam prośbę.", "sawàt-dii khráp róp-kuan nòi khráp", "สวัสดีครับ รบกวนหน่อยครับ"),
 ("B", "Słucham.", "wâa yang-ngai khá", "ว่ายังไงคะ"),
 ("A", "Poproszę jeszcze jeden koc.", "khǎw phâa hòm ìik phǔen khráp", "ขอผ้าห่มอีกผืนครับ"),
 ("B", "Oczywiście. Coś jeszcze?", "dâai khâ ao à-rai ìik mǎi khá", "ได้ค่ะ เอาอะไรอีกไหมคะ"),
 ("A", "Poproszę jeszcze jedną poduszkę.", "khǎw mǎwn ìik bai khráp", "ขอหมอนอีกใบครับ"),
 ("B", "Zaraz przyniosę.", "dǐao ao pai hâi khâ", "เดี๋ยวเอาไปให้ค่ะ"),
 ("A", "Dziękuję bardzo.", "khàwp-khun mâak khráp", "ขอบคุณมากครับ"),
 ("B", "Nie ma sprawy.", "mâi pen rai khâ", "ไม่เป็นไรค่ะ"),
], "Klasyfikatory: koc liczy się na „phǔen”, poduszkę na „bai”."),

("W pralni", "Dom i codzienność", "A1", "Klient", "Obsługa", [
 ("A", "Dzień dobry, chcę oddać pranie.", "sawàt-dii khráp khǎw sák phâa khráp", "สวัสดีครับ ขอซักผ้าครับ"),
 ("B", "Ile kilogramów?", "kìi kì-loo khá", "กี่กิโลคะ"),
 ("A", "Chyba trzy.", "nâa jà sǎam kì-loo khráp", "น่าจะสามกิโลครับ"),
 ("B", "Czterdzieści bahtów za kilogram.", "kì-loo lá sìi-sìp bàat khâ", "กิโลละสี่สิบบาทค่ะ"),
 ("A", "Kiedy będzie gotowe?", "sèt mûea-rài khráp", "เสร็จเมื่อไหร่ครับ"),
 ("B", "Jutro po południu.", "phrûng níi bàai khâ", "พรุ่งนี้บ่ายค่ะ"),
 ("A", "Dobrze, dziękuję.", "dâai khráp khàwp-khun", "ได้ครับ ขอบคุณ"),
], "Pralnie na wagę są w Tajlandii tanie i wszechobecne."),

("Rozmowa o pogodzie", "Pogoda i przyroda", "A1", "Turysta", "Sąsiad", [
 ("B", "Ale dziś gorąco, prawda?", "wan níi ráwn mâak nə\u0301 khráp", "วันนี้ร้อนมากเนอะครับ"),
 ("A", "Bardzo gorąco.", "ráwn mâak jing jing khráp", "ร้อนมากจริงๆ ครับ"),
 ("B", "Po południu będzie padać.", "tawn bàai fǒn jà tòk khráp", "ตอนบ่ายฝนจะตกครับ"),
 ("A", "Naprawdę? Nie mam parasola.", "jing rǔe khráp phǒm mâi mii rôm", "จริงเหรอครับ ผมไม่มีร่ม"),
 ("B", "Teraz jest pora deszczowa.", "tawn níi pen nâa fǒn khráp", "ตอนนี้เป็นหน้าฝนครับ"),
 ("A", "Jak długo pada?", "fǒn tòk naan mǎi khráp", "ฝนตกนานไหมครับ"),
 ("B", "Zwykle około godziny.", "pramaan chûa-moong nùeng khráp", "ประมาณชั่วโมงหนึ่งครับ"),
 ("A", "To poczekam, aż przestanie.", "ngán phǒm raw hâi fǒn yùt kàwn khráp", "งั้นผมรอให้ฝนหยุดก่อนครับ"),
], "„nə\u0301” to partykuła szukająca zgody rozmówcy — jak polskie „prawda?”."),

("Umawianie się na spotkanie", "Czas i daty", "A1", "Znajomy A", "Znajomy B", [
 ("A", "Masz jutro czas?", "phrûng níi wâang mǎi khráp", "พรุ่งนี้ว่างไหมครับ"),
 ("B", "Rano mam pracę.", "tawn cháo tâwng tham ngaan khráp", "ตอนเช้าต้องทำงานครับ"),
 ("A", "To może wieczorem?", "ngán tawn yen dâai mǎi khráp", "งั้นตอนเย็นได้ไหมครับ"),
 ("B", "Może być. O której?", "dâai khráp kìi moong dii", "ได้ครับ กี่โมงดี"),
 ("A", "O szóstej?", "hòk moong yen dii mǎi khráp", "หกโมงเย็นดีไหมครับ"),
 ("B", "Dobrze. Gdzie się spotkamy?", "dâai khráp jəə kan thîi nǎi", "ได้ครับ เจอกันที่ไหน"),
 ("A", "Przed hotelem.", "nâa roong raem khráp", "หน้าโรงแรมครับ"),
 ("B", "Umowa stoi, do zobaczenia.", "tòk long khráp jəə kan", "ตกลงครับ เจอกัน"),
], "„dii mǎi” na końcu propozycji = „może być?”."),

("Rozmowa o rodzinie", "Ludzie i rodzina", "A1", "Turysta", "Znajoma", [
 ("B", "Ma pan rodzeństwo?", "mii phîi náwng mǎi khá", "มีพี่น้องไหมคะ"),
 ("A", "Mam starszego brata.", "mii phîi chaai khon nùeng khráp", "มีพี่ชายคนหนึ่งครับ"),
 ("B", "A dzieci?", "láew mii lûuk mǎi khá", "แล้วมีลูกไหมคะ"),
 ("A", "Mam dwoje dzieci.", "mii lûuk sǎwng khon khráp", "มีลูกสองคนครับ"),
 ("B", "Ile mają lat?", "aa-yú thâo-rài khá", "อายุเท่าไหร่คะ"),
 ("A", "Pięć i osiem lat.", "hâa khùap kàp pàet khùap khráp", "ห้าขวบกับแปดขวบครับ"),
 ("B", "Słodkie. Są tutaj z panem?", "nâa rák jang maa dûai mǎi khá", "น่ารักจัง มาด้วยไหมคะ"),
 ("A", "Nie, zostały w domu z żoną.", "mâi khráp yùu bâan kàp phan-rá-yaa", "ไม่ครับ อยู่บ้านกับภรรยา"),
], "Wiek dzieci liczy się na „khùap”, dorosłych na „pii”."),

("Owoce na straganie", "Jedzenie i napoje", "Survival", "Klient", "Sprzedawczyni", [
 ("A", "Ile kosztuje mango?", "má-mûang thâo-rài khráp", "มะม่วงเท่าไหร่ครับ"),
 ("B", "Sześćdziesiąt bahtów za kilogram.", "kì-loo lá hòk-sìp bàat khâ", "กิโลละหกสิบบาทค่ะ"),
 ("A", "Czy są dojrzałe?", "sùk mǎi khráp", "สุกไหมครับ"),
 ("B", "Dojrzałe i słodkie.", "sùk khâ wǎan mâak", "สุกค่ะ หวานมาก"),
 ("A", "Poproszę kilogram.", "khǎw nùeng kì-loo khráp", "ขอหนึ่งกิโลครับ"),
 ("B", "Coś jeszcze?", "ao à-rai ìik mǎi khá", "เอาอะไรอีกไหมคะ"),
 ("A", "Poproszę jeszcze dwa banany.", "khǎw klûai sǎwng lûuk dûai khráp", "ขอกล้วยสองลูกด้วยครับ"),
 ("B", "Razem osiemdziesiąt bahtów.", "tháng mòt pàet-sìp bàat khâ", "ทั้งหมดแปดสิบบาทค่ะ"),
], "Owoce liczy się na „lûuk”; ceny podaje się zwykle za kilogram."),

("Sklep całodobowy: szukam wody", "Zakupy i pieniądze", "Survival", "Klient", "Kasjer", [
 ("A", "Przepraszam, gdzie jest woda?", "khǎw thôot khráp náam yùu thîi nǎi khráp", "ขอโทษครับ น้ำอยู่ที่ไหนครับ"),
 ("B", "Z tyłu, przy lodówce.", "yùu khâang lǎng thîi tûu yen khráp", "อยู่ข้างหลังที่ตู้เย็นครับ"),
 ("A", "Dziękuję.", "khàwp-khun khráp", "ขอบคุณครับ"),
 ("B", "Coś jeszcze?", "ao à-rai ìik mǎi khráp", "เอาอะไรอีกไหมครับ"),
 ("A", "To wszystko. Ile razem?", "thâo níi khráp tháng mòt thâo-rài", "เท่านี้ครับ ทั้งหมดเท่าไหร่"),
 ("B", "Osiemdziesiąt pięć bahtów.", "pàet-sìp hâa bàat khráp", "แปดสิบห้าบาทครับ"),
 ("A", "Czy mogę zapłacić kartą?", "jàai bàt dâai mǎi khráp", "จ่ายบัตรได้ไหมครับ"),
 ("B", "Można, proszę tutaj.", "dâai khráp trong níi khráp", "ได้ครับ ตรงนี้ครับ"),
], "„thâo níi” = tyle wystarczy, to wszystko."),

("Zgubiony telefon: prośba o pomoc", "Awarie i pomoc", "A1", "Turysta", "Obsługa", [
 ("A", "Przepraszam, potrzebuję pomocy.", "khǎw thôot khráp phǒm tâwng kaan khwaam chûai lǔea", "ขอโทษครับ ผมต้องการความช่วยเหลือ"),
 ("B", "Co się stało?", "pen à-rai khá", "เป็นอะไรคะ"),
 ("A", "Zgubiłem telefon.", "phǒm tham mue-thǔe hǎai khráp", "ผมทำมือถือหายครับ"),
 ("B", "Gdzie ostatnio pan go widział?", "hěn khráng sùt tháai thîi nǎi khá", "เห็นครั้งสุดท้ายที่ไหนคะ"),
 ("A", "Chyba w restauracji.", "nâa jà yùu thîi ráan aa-hǎan khráp", "น่าจะอยู่ที่ร้านอาหารครับ"),
 ("B", "Zadzwonię tam i zapytam.", "dǐao thoo pai thǎam hâi khâ", "เดี๋ยวโทรไปถามให้ค่ะ"),
 ("A", "Bardzo dziękuję.", "khàwp-khun mâak khráp", "ขอบคุณมากครับ"),
 ("B", "Proszę chwilę poczekać.", "raw sàk khrûu ná khá", "รอสักครู่นะคะ"),
], "„khwaam chûai lǔea” = pomoc (rzeczownik)."),
]

DIALOGUES2 += [

("Kantor: wymiana euro na bahty", "Zakupy i pieniądze", "A1", "Turysta", "Kasjerka", [
 ("A", "Dzień dobry, chcę wymienić pieniądze.", "sawàt-dii khráp phǒm yàak lâek ngoen khráp", "สวัสดีครับ ผมอยากแลกเงินครับ"),
 ("B", "Jaka waluta?", "ngoen sà-kun nǎi khá", "เงินสกุลไหนคะ"),
 ("A", "Euro na bahty.", "yuu-roo pen ngoen bàat khráp", "ยูโรเป็นเงินบาทครับ"),
 ("B", "Ile chce pan wymienić?", "lâek thâo-rài khá", "แลกเท่าไหร่คะ"),
 ("A", "Dwieście euro.", "sǎwng ráwi yuu-roo khráp", "สองร้อยยูโรครับ"),
 ("B", "Poproszę paszport.", "khǎw pháat-sà-pàwt dûai khâ", "ขอพาสปอร์ตด้วยค่ะ"),
 ("A", "Proszę. Jaki jest dziś kurs?", "nîi khráp wan níi àt-traa thâo-rài khráp", "นี่ครับ วันนี้อัตราเท่าไหร่ครับ"),
 ("B", "Trzydzieści osiem bahtów.", "sǎam-sìp pàet bàat khâ", "สามสิบแปดบาทค่ะ"),
 ("A", "Dobrze, wymieniam.", "dâai khráp lâek loei khráp", "ได้ครับ แลกเลยครับ"),
 ("B", "Proszę policzyć.", "chûai náp duu ná khá", "ช่วยนับดูนะคะ"),
], "Kantory dają lepszy kurs niż lotnisko. Zawsze przelicz gotówkę na miejscu."),

("Negocjacja z kierowcą tuk-tuka", "Transport", "Survival", "Pasażer", "Kierowca", [
 ("A", "Ile do dworca kolejowego?", "pai sà-thǎa-nii rót fai thâo-rài khráp", "ไปสถานีรถไฟเท่าไหร่ครับ"),
 ("B", "Trzysta bahtów.", "sǎam ráwi bàat khráp", "สามร้อยบาทครับ"),
 ("A", "To za drogo.", "phaeng pai khráp", "แพงไปครับ"),
 ("B", "To ile pan da?", "hâi thâo-rài khráp", "ให้เท่าไหร่ครับ"),
 ("A", "Sto pięćdziesiąt.", "nùeng ráwi hâa-sìp khráp", "หนึ่งร้อยห้าสิบครับ"),
 ("B", "Dwieście, dobrze?", "sǎwng ráwi ná khráp", "สองร้อยนะครับ"),
 ("A", "Dobrze, jedziemy.", "tòk long khráp pai loei", "ตกลงครับ ไปเลย"),
], "Cenę ustalaj ZAWSZE przed wsiadaniem. Taksówka z licznikiem bywa tańsza."),

("W świątyni: zasady", "Miejsca i orientacja", "A1", "Turysta", "Opiekun", [
 ("A", "Przepraszam, czy mogę tu wejść?", "khǎw thôot khráp khâo dâai mǎi khráp", "ขอโทษครับ เข้าได้ไหมครับ"),
 ("B", "Można, ale proszę zdjąć buty.", "dâai khráp tàe thàwt rawng tháo dûai", "ได้ครับ แต่ถอดรองเท้าด้วย"),
 ("A", "Rozumiem. A zdjęcia?", "khâo jai khráp láew thàai rûup dâai mǎi", "เข้าใจครับ แล้วถ่ายรูปได้ไหม"),
 ("B", "Zdjęcia można, bez lampy.", "thàai dâai khráp tàe mâi chái flaet", "ถ่ายได้ครับ แต่ไม่ใช้แฟลช"),
 ("A", "Czy ubranie jest odpowiednie?", "sài chút níi dâai mǎi khráp", "ใส่ชุดนี้ได้ไหมครับ"),
 ("B", "Trzeba zakryć ramiona.", "tâwng pìt lài dûai khráp", "ต้องปิดไหล่ด้วยครับ"),
 ("A", "Mam koszulę w torbie.", "phǒm mii sûea nai krà-pǎo khráp", "ผมมีเสื้อในกระเป๋าครับ"),
 ("B", "Świetnie, proszę bardzo.", "dii khráp chəən loei", "ดีครับ เชิญเลย"),
], "W świątyni: zakryte ramiona i kolana, buty zdejmowane przed wejściem."),

("Rezerwacja masażu", "Zdrowie", "A1", "Klient", "Recepcja", [
 ("A", "Dzień dobry, chcę zarezerwować masaż.", "sawàt-dii khráp khǎw jawng nûat khráp", "สวัสดีครับ ขอจองนวดครับ"),
 ("B", "Masaż tajski czy olejkowy?", "nûat thai rǔe nûat náam man khá", "นวดไทยหรือนวดน้ำมันคะ"),
 ("A", "Tajski, proszę.", "nûat thai khráp", "นวดไทยครับ"),
 ("B", "Godzina czy dwie?", "chûa-moong nùeng rǔe sǎwng chûa-moong khá", "ชั่วโมงหนึ่งหรือสองชั่วโมงคะ"),
 ("A", "Godzina wystarczy.", "chûa-moong nùeng phaw khráp", "ชั่วโมงหนึ่งพอครับ"),
 ("B", "Na którą godzinę?", "kìi moong dii khá", "กี่โมงดีคะ"),
 ("A", "Na siedemnastą.", "hâa moong yen khráp", "ห้าโมงเย็นครับ"),
 ("B", "Zapisane. Proszę być pięć minut wcześniej.", "jawng hâi láew khâ maa kàwn hâa naa-thii ná khá", "จองให้แล้วค่ะ มาก่อนห้านาทีนะคะ"),
], "„nûat” = masaż. Powiedz „bao bao” (delikatnie), jeśli boli."),

("Restauracja: alergia", "Restauracja", "A1", "Gość", "Kelner", [
 ("A", "Przepraszam, mam alergię na orzeszki.", "khǎw thôot khráp phǒm pháe thùa khráp", "ขอโทษครับ ผมแพ้ถั่วครับ"),
 ("B", "Rozumiem, powiem w kuchni.", "khâo jai khráp dǐao bàwk khrua hâi", "เข้าใจครับ เดี๋ยวบอกครัวให้"),
 ("A", "Czy w tym daniu są orzeszki?", "meen-nuu níi mii thùa mǎi khráp", "เมนูนี้มีถั่วไหมครับ"),
 ("B", "Są, ale można bez nich.", "mii khráp tàe sàng mâi sài dâai", "มีครับ แต่สั่งไม่ใส่ได้"),
 ("A", "To poproszę bez orzeszków.", "ngán khǎw mâi sài thùa khráp", "งั้นขอไม่ใส่ถั่วครับ"),
 ("B", "Dobrze. Coś do picia?", "dâai khráp ráp náam à-rai dii khráp", "ได้ครับ รับน้ำอะไรดีครับ"),
 ("A", "Poproszę wodę bez lodu.", "khǎw náam plào mâi sài nám khǎeng khráp", "ขอน้ำเปล่าไม่ใส่น้ำแข็งครับ"),
 ("B", "Już przynoszę.", "sàk khrûu ná khráp", "สักครู่นะครับ"),
], "Alergie zgłaszaj przy zamówieniu — orzeszki są w wielu sosach."),

("Telefon: rezerwacja stolika", "Restauracja", "A1", "Klient", "Restauracja", [
 ("B", "Dzień dobry, słucham.", "sawàt-dii khâ ráan aa-hǎan khâ", "สวัสดีค่ะ ร้านอาหารค่ะ"),
 ("A", "Chcę zarezerwować stolik.", "phǒm yàak jawng tó khráp", "ผมอยากจองโต๊ะครับ"),
 ("B", "Na kiedy?", "wan nǎi weelaa nǎi khá", "วันไหน เวลาไหนคะ"),
 ("A", "Na dziś wieczór, na siódmą.", "khuen níi nùeng thûm khráp", "คืนนี้หนึ่งทุ่มครับ"),
 ("B", "Ile osób?", "kìi khon khá", "กี่คนคะ"),
 ("A", "Cztery osoby.", "sìi khon khráp", "สี่คนครับ"),
 ("B", "Poproszę imię i numer.", "khǎw chûe kàp bəə thoo dûai khâ", "ขอชื่อกับเบอร์โทรด้วยค่ะ"),
 ("A", "Marek, numer podam teraz.", "chûe maa-rèek khráp dǐao bàwk bəə", "ชื่อมาเร็คครับ เดี๋ยวบอกเบอร์"),
 ("B", "Rezerwacja przyjęta.", "jawng hâi láew khâ", "จองให้แล้วค่ะ"),
], "„nùeng thûm” = dziewiętnasta. Godziny wieczorne liczy się od „thûm”."),

("Small talk o pracy", "Praca i nauka", "A1", "Sąsiad", "Turysta", [
 ("A", "Czym się pan zajmuje?", "tham ngaan à-rai khráp", "ทำงานอะไรครับ"),
 ("B", "Jestem nauczycielem.", "phǒm pen khruu khráp", "ผมเป็นครูครับ"),
 ("A", "Ciekawa praca.", "nâa sǒn jai mâak khráp", "น่าสนใจมากครับ"),
 ("B", "A pan?", "láew khun lâ khráp", "แล้วคุณล่ะครับ"),
 ("A", "Pracuję w biurze.", "phǒm tham ngaan thîi áwf-fít khráp", "ผมทำงานที่ออฟฟิศครับ"),
 ("B", "Daleko stąd?", "klai jàak thîi nîi mǎi khráp", "ไกลจากที่นี่ไหมครับ"),
 ("A", "Pół godziny autobusem.", "nâng rót mee khrûeng chûa-moong khráp", "นั่งรถเมล์ครึ่งชั่วโมงครับ"),
 ("B", "To niedaleko.", "kâw mâi klai ná khráp", "ก็ไม่ไกลนะครับ"),
], "„pen” + zawód = być kimś z zawodu."),

("Zaproszenie na jedzenie", "Small talk", "A1", "Znajomy", "Turysta", [
 ("A", "Jadł pan już?", "kin khâao rǔe yang khráp", "กินข้าวหรือยังครับ"),
 ("B", "Jeszcze nie.", "yang khráp", "ยังครับ"),
 ("A", "To chodźmy razem.", "ngán pai kin dûai kan khráp", "งั้นไปกินด้วยกันครับ"),
 ("B", "Chętnie. Gdzie?", "dii loei khráp pai thîi nǎi", "ดีเลยครับ ไปที่ไหน"),
 ("A", "Znam dobrą knajpkę niedaleko.", "phǒm rúu-jàk ráan à-ròi thǎew níi khráp", "ผมรู้จักร้านอร่อยแถวนี้ครับ"),
 ("B", "Ostre jedzenie?", "aa-hǎan phèt mǎi khráp", "อาหารเผ็ดไหมครับ"),
 ("A", "Może być łagodne.", "sàng mâi phèt dâai khráp", "สั่งไม่เผ็ดได้ครับ"),
 ("B", "Świetnie, idziemy.", "yîam khráp pai loei", "เยี่ยมครับ ไปเลย"),
], "„kin khâao rǔe yang” to codzienne powitanie, nie tylko pytanie o posiłek."),

("Na poczcie", "Miejsca i orientacja", "A1", "Klient", "Urzędniczka", [
 ("A", "Dzień dobry, chcę wysłać paczkę.", "sawàt-dii khráp phǒm yàak sòng phát-sà-dù khráp", "สวัสดีครับ ผมอยากส่งพัสดุครับ"),
 ("B", "Dokąd?", "sòng pai thîi nǎi khá", "ส่งไปที่ไหนคะ"),
 ("A", "Do Polski.", "pai poo-laen khráp", "ไปโปแลนด์ครับ"),
 ("B", "Poproszę na wagę.", "khǎw châng nám-nàk dûai khâ", "ขอชั่งน้ำหนักด้วยค่ะ"),
 ("A", "Ile to kosztuje?", "thâo-rài khráp", "เท่าไหร่ครับ"),
 ("B", "Osiemset bahtów.", "pàet ráwi bàat khâ", "แปดร้อยบาทค่ะ"),
 ("A", "Jak długo idzie?", "chái weelaa kìi wan khráp", "ใช้เวลากี่วันครับ"),
 ("B", "Około dwóch tygodni.", "pramaan sǎwng aa-thít khâ", "ประมาณสองอาทิตย์ค่ะ"),
 ("A", "Dobrze, wysyłam.", "dâai khráp sòng loei khráp", "ได้ครับ ส่งเลยครับ"),
], "„phát-sà-dù” = paczka; „châng” = ważyć."),

("Godziny otwarcia", "Czas i daty", "Survival", "Turysta", "Obsługa", [
 ("A", "Przepraszam, o której otwieracie?", "khǎw thôot khráp pə\u0300ət kìi moong khráp", "ขอโทษครับ เปิดกี่โมงครับ"),
 ("B", "O dziewiątej rano.", "kâo moong cháo khráp", "เก้าโมงเช้าครับ"),
 ("A", "A o której zamykacie?", "láew pìt kìi moong khráp", "แล้วปิดกี่โมงครับ"),
 ("B", "O dwudziestej.", "sǎwng thûm khráp", "สองทุ่มครับ"),
 ("A", "Czy jesteście otwarci w niedzielę?", "wan aa-thít pə\u0300ət mǎi khráp", "วันอาทิตย์เปิดไหมครับ"),
 ("B", "Tak, codziennie.", "pə\u0300ət thúk wan khráp", "เปิดทุกวันครับ"),
 ("A", "Dziękuję, wrócę jutro.", "khàwp-khun khráp phrûng níi maa mài", "ขอบคุณครับ พรุ่งนี้มาใหม่"),
 ("B", "Zapraszamy.", "yin dii khráp", "ยินดีครับ"),
], "„sǎwng thûm” = 20:00. Wieczorne godziny liczy się od 19:00 jako „nùeng thûm”."),
]
