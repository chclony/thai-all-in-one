# -*- coding: utf-8 -*-
"""Dialogi praktyczne. Krotka: (tytul, sytuacja, poziom, rolaA, rolaB, linie, notatka)
Linia: (rola, polski, fonetyka, tajski)
"""

DIALOGUES = [
("W restauracji: zamawianie", "Restauracja", "Survival", "Turysta", "Kelnerka", [
 ("B", "Dzień dobry. Ile osób?", "sawàt-dii khâ kìi khon khá", "สวัสดีค่ะ กี่คนคะ"),
 ("A", "Dwie osoby.", "sǎwng khon khráp", "สองคนครับ"),
 ("B", "Proszę, oto menu.", "chəən khâ nîi mee-nuu khâ", "เชิญค่ะ นี่เมนูค่ะ"),
 ("A", "Poproszę dwa pad thai.", "khǎw phàt thai sǎwng jaan khráp", "ขอผัดไทยสองจานครับ"),
 ("B", "Ostre?", "ao phèt mǎi khá", "เอาเผ็ดไหมคะ"),
 ("A", "Nieostre, proszę.", "mâi phèt khráp", "ไม่เผ็ดครับ"),
 ("A", "I poproszę dwie wody.", "láew kâw khǎw náam plào sǎwng khùat khráp", "แล้วก็ขอน้ำเปล่าสองขวดครับ"),
 ("B", "Dobrze, chwileczkę.", "dâai khâ raw sàk khrûu ná khá", "ได้ค่ะ รอสักครู่นะคะ"),
], "Zapamiętaj schemat: khǎw + danie + liczba + klasyfikator + khráp."),

("W restauracji: rachunek", "Restauracja", "Survival", "Turysta", "Kelnerka", [
 ("A", "Poproszę rachunek.", "khít ngoen dûai khráp", "คิดเงินด้วยครับ"),
 ("B", "Razem trzysta bahtów.", "tháng mòt sǎam ráwi bàat khâ", "ทั้งหมดสามร้อยบาทค่ะ"),
 ("A", "Czy mogę zapłacić kartą?", "jàai bàt dâai mǎi khráp", "จ่ายบัตรได้ไหมครับ"),
 ("B", "Przepraszam, tylko gotówka.", "khǎw thôot khâ ráp tàe ngoen sòt khâ", "ขอโทษค่ะ รับแต่เงินสดค่ะ"),
 ("A", "Dobrze, proszę.", "dâai khráp nîi khráp", "ได้ครับ นี่ครับ"),
 ("B", "Dziękuję, oto reszta.", "khàwp-khun khâ nîi ngoen thawn khâ", "ขอบคุณค่ะ นี่เงินทอนค่ะ"),
 ("A", "Jedzenie było bardzo smaczne.", "aa-hǎan à-ròi mâak khráp", "อาหารอร่อยมากครับ"),
 ("B", "Dziękuję bardzo.", "khàwp-khun mâak khâ", "ขอบคุณมากค่ะ"),
], "„tháng mòt” = razem, w sumie."),

("Taksówka do hotelu", "Transport", "Survival", "Pasażer", "Kierowca", [
 ("A", "Do tego hotelu, proszę.", "pai roong raem níi khráp", "ไปโรงแรมนี้ครับ"),
 ("B", "Dobrze.", "dâai khráp", "ได้ครับ"),
 ("A", "Proszę włączyć taksometr.", "kòt mí-təə dûai khráp", "กดมิเตอร์ด้วยครับ"),
 ("B", "Już włączony.", "kòt láew khráp", "กดแล้วครับ"),
 ("A", "Długo tam jedziemy?", "chái weelaa naan mǎi khráp", "ใช้เวลานานไหมครับ"),
 ("B", "Około dwudziestu minut.", "pramaan yîi-sìp naa-thii khráp", "ประมาณยี่สิบนาทีครับ"),
 ("A", "Proszę tutaj się zatrzymać.", "jàwt trong níi dâai mǎi khráp", "จอดตรงนี้ได้ไหมครับ"),
 ("B", "Proszę, sto pięćdziesiąt bahtów.", "dâai khráp nùeng ráwi hâa-sìp bàat khráp", "ได้ครับ หนึ่งร้อยห้าสิบบาทครับ"),
], "Bez taksometru kierowca poda cenę z góry — wtedy negocjuj."),

("Hotel: meldunek", "Hotel", "Survival", "Gość", "Recepcjonistka", [
 ("A", "Dzień dobry, mam rezerwację.", "sawàt-dii khráp phǒm jawng wái láew khráp", "สวัสดีครับ ผมจองไว้แล้วครับ"),
 ("B", "Poproszę paszport.", "khǎw nǎng-sǔe dəən thaang khâ", "ขอหนังสือเดินทางค่ะ"),
 ("A", "Proszę bardzo.", "nîi khráp", "นี่ครับ"),
 ("B", "Dwie noce, prawda?", "phák sǎwng khuen châi mǎi khá", "พักสองคืนใช่ไหมคะ"),
 ("A", "Tak. Czy śniadanie jest w cenie?", "châi khráp ruam aa-hǎan cháo mǎi khráp", "ใช่ครับ รวมอาหารเช้าไหมครับ"),
 ("B", "Tak, od siódmej do dziesiątej.", "ruam khâ jèt moong thǔeng sìp moong khâ", "รวมค่ะ เจ็ดโมงถึงสิบโมงค่ะ"),
 ("A", "Jakie jest hasło do wi-fi?", "rahàt wai-fai à-rai khráp", "รหัสไวไฟอะไรครับ"),
 ("B", "Jest na karcie pokoju.", "yùu nai bàt hâwng khâ", "อยู่ในบัตรห้องค่ะ"),
], "„phák” = zatrzymać się, nocować."),

("Hotel: problem w pokoju", "Hotel", "A1", "Gość", "Recepcja", [
 ("A", "Przepraszam, mam problem.", "khǎw thôot khráp mii panhǎa nít nòi", "ขอโทษครับ มีปัญหานิดหน่อย"),
 ("B", "Co się stało?", "mii à-rai khá", "มีอะไรคะ"),
 ("A", "Klimatyzacja nie działa.", "ae sǐa khráp", "แอร์เสียครับ"),
 ("B", "Który pokój?", "hâwng bəə à-rai khá", "ห้องเบอร์อะไรคะ"),
 ("A", "Pokój trzysta pięć.", "hâwng sǎam sǔun hâa khráp", "ห้องสามศูนย์ห้าครับ"),
 ("B", "Wyślę kogoś, kto sprawdzi.", "jà sòng khon pai duu khâ", "จะส่งคนไปดูค่ะ"),
 ("A", "Nie ma też gorącej wody.", "láew kâw mâi mii náam ráwn khráp", "แล้วก็ไม่มีน้ำร้อนครับ"),
 ("B", "Przepraszam. Zmienimy pokój.", "khǎw thôot khâ jà plìan hâwng hâi khâ", "ขอโทษค่ะ จะเปลี่ยนห้องให้ค่ะ"),
], "„sǐa” = zepsuty. „plìan hâi” = zmienić dla kogoś."),

("Na targu: targowanie", "Zakupy i pieniądze", "Survival", "Turysta", "Sprzedawczyni", [
 ("B", "Proszę spojrzeć, bardzo ładne.", "chəən duu khâ sǔai mâak khâ", "เชิญดูค่ะ สวยมากค่ะ"),
 ("A", "Ile to kosztuje?", "an níi thâo-rài khráp", "อันนี้เท่าไหร่ครับ"),
 ("B", "Czterysta bahtów.", "sìi ráwi bàat khâ", "สี่ร้อยบาทค่ะ"),
 ("A", "Za drogo. Może taniej?", "phaeng pai lót dâai mǎi khráp", "แพงไป ลดได้ไหมครับ"),
 ("B", "Trzysta pięćdziesiąt.", "sǎam ráwi hâa-sìp khâ", "สามร้อยห้าสิบค่ะ"),
 ("A", "Trzysta, dobrze?", "sǎam ráwi dâai mǎi khráp", "สามร้อยได้ไหมครับ"),
 ("B", "Dobrze, biorę.", "dâai khâ ao loei khâ", "ได้ค่ะ เอาเลยค่ะ"),
 ("A", "Wezmę dwie sztuki.", "ao sǎwng an khráp", "เอาสองอันครับ"),
], "Targuj się z uśmiechem — to część kultury, nie konflikt."),

("W sklepie całodobowym", "Zakupy i pieniądze", "Survival", "Klient", "Kasjer", [
 ("A", "Przepraszam, gdzie jest woda?", "khǎw thôot khráp náam yùu thîi nǎi khráp", "ขอโทษครับ น้ำอยู่ที่ไหนครับ"),
 ("B", "Z tyłu, po lewej.", "yùu khâang lǎng dâan sáai khráp", "อยู่ข้างหลังด้านซ้ายครับ"),
 ("A", "Dziękuję.", "khàwp-khun khráp", "ขอบคุณครับ"),
 ("B", "Razem osiemdziesiąt bahtów.", "tháng mòt pàet-sìp bàat khráp", "ทั้งหมดแปดสิบบาทครับ"),
 ("A", "Poproszę torbę.", "khǎw thǔng dûai khráp", "ขอถุงด้วยครับ"),
 ("B", "Torba kosztuje dwa bahty.", "thǔng sǎwng bàat khráp", "ถุงสองบาทครับ"),
 ("A", "W porządku.", "mâi pen rai khráp", "ไม่เป็นไรครับ"),
], "W Tajlandii torby foliowe bywają płatne."),

("Pytanie o drogę", "Miejsca i orientacja", "Survival", "Turysta", "Przechodzień", [
 ("A", "Przepraszam, gdzie jest dworzec kolejowy?", "khǎw thôot khráp sathǎanii rót fai yùu thîi nǎi khráp", "ขอโทษครับ สถานีรถไฟอยู่ที่ไหนครับ"),
 ("B", "Prosto, potem w prawo.", "trong pai láew líaw khwǎa khráp", "ตรงไปแล้วเลี้ยวขวาครับ"),
 ("A", "Czy to daleko?", "klai mǎi khráp", "ไกลไหมครับ"),
 ("B", "Niedaleko, dziesięć minut pieszo.", "mâi klai dəən sìp naa-thii khráp", "ไม่ไกล เดินสิบนาทีครับ"),
 ("A", "Czy mogę tam dojść pieszo?", "dəən pai dâai mǎi khráp", "เดินไปได้ไหมครับ"),
 ("B", "Tak, można.", "dâai khráp", "ได้ครับ"),
 ("A", "Dziękuję bardzo.", "khàwp-khun mâak khráp", "ขอบคุณมากครับ"),
], "„trong pai” = prosto, „líaw” = skręć."),

("W aptece", "Zdrowie", "Survival", "Klient", "Farmaceutka", [
 ("A", "Dzień dobry, źle się czuję.", "sawàt-dii khráp phǒm mâi sabaai khráp", "สวัสดีครับ ผมไม่สบายครับ"),
 ("B", "Co panu dolega?", "pen à-rai khá", "เป็นอะไรคะ"),
 ("A", "Boli mnie głowa i mam gorączkę.", "pùat hǔa láew kâw mii khâi khráp", "ปวดหัวแล้วก็มีไข้ครับ"),
 ("B", "Od kiedy?", "pen maa kìi wan láew khá", "เป็นมากี่วันแล้วคะ"),
 ("A", "Od dwóch dni.", "sǎwng wan láew khráp", "สองวันแล้วครับ"),
 ("B", "Proszę, lek na gorączkę.", "nîi yaa lót khâi khâ", "นี่ยาลดไข้ค่ะ"),
 ("A", "Ile razy dziennie?", "kin wan lá kìi khráng khráp", "กินวันละกี่ครั้งครับ"),
 ("B", "Trzy razy, po jedzeniu.", "wan lá sǎam khráng lǎng aa-hǎan khâ", "วันละสามครั้ง หลังอาหารค่ะ"),
], "„pen à-rai” = co ci jest? „lǎng aa-hǎan” = po jedzeniu."),

("U lekarza", "Zdrowie", "A1", "Pacjent", "Lekarz", [
 ("B", "Dzień dobry, proszę usiąść.", "sawàt-dii khráp chəən nâng khráp", "สวัสดีครับ เชิญนั่งครับ"),
 ("A", "Boli mnie brzuch.", "phǒm pùat tháwng khráp", "ผมปวดท้องครับ"),
 ("B", "Ma pan biegunkę?", "tháwng sǐa dûai mǎi khráp", "ท้องเสียด้วยไหมครับ"),
 ("A", "Tak, od wczoraj.", "châi khráp tâng tàe mûea waan", "ใช่ครับ ตั้งแต่เมื่อวาน"),
 ("B", "Co pan jadł?", "kin à-rai maa khráp", "กินอะไรมาครับ"),
 ("A", "Jedzenie z ulicy.", "aa-hǎan khâang thanǒn khráp", "อาหารข้างถนนครับ"),
 ("B", "Proszę dużo pić wody.", "dùem náam yóe yóe ná khráp", "ดื่มน้ำเยอะๆ นะครับ"),
 ("A", "Czy mam ubezpieczenie? Mam papiery.", "phǒm mii prakan khráp mii èek-kasǎan", "ผมมีประกันครับ มีเอกสาร"),
], "„tâng tàe” = od (jakiegoś momentu)."),

("Na lotnisku", "Transport", "A1", "Pasażer", "Obsługa", [
 ("B", "Poproszę paszport i bilet.", "khǎw nǎng-sǔe dəən thaang kàp tǔa khâ", "ขอหนังสือเดินทางกับตั๋วค่ะ"),
 ("A", "Proszę bardzo.", "nîi khráp", "นี่ครับ"),
 ("B", "Ile ma pan bagażu?", "mii krapǎo kìi bai khá", "มีกระเป๋ากี่ใบคะ"),
 ("A", "Jedną walizkę.", "nùeng bai khráp", "หนึ่งใบครับ"),
 ("B", "Bramka numer dwanaście.", "prátuu bəə sìp-sǎwng khâ", "ประตูเบอร์สิบสองค่ะ"),
 ("A", "O której zaczyna się boarding?", "khûen khrûeang kìi moong khráp", "ขึ้นเครื่องกี่โมงครับ"),
 ("B", "O ósmej rano.", "pàet moong cháo khâ", "แปดโมงเช้าค่ะ"),
 ("A", "Dziękuję.", "khàwp-khun khráp", "ขอบคุณครับ"),
], "„khûen khrûeang” = wejść na pokład."),

("Wynajem skutera", "Transport", "Survival", "Turysta", "Wypożyczalnia", [
 ("A", "Chcę wynająć skuter.", "yàak châo maw-tôe-sai khráp", "อยากเช่ามอเตอร์ไซค์ครับ"),
 ("B", "Na ile dni?", "châo kìi wan khá", "เช่ากี่วันคะ"),
 ("A", "Na trzy dni. Ile za dzień?", "sǎam wan khráp wan lá thâo-rài khráp", "สามวันครับ วันละเท่าไหร่ครับ"),
 ("B", "Dwieście pięćdziesiąt bahtów dziennie.", "wan lá sǎwng ráwi hâa-sìp bàat khâ", "วันละสองร้อยห้าสิบบาทค่ะ"),
 ("A", "Czy jest kask?", "mii mùak kan nók mǎi khráp", "มีหมวกกันน็อคไหมครับ"),
 ("B", "Jest, dwa.", "mii khâ sǎwng bai khâ", "มีค่ะ สองใบค่ะ"),
 ("A", "Czy benzyna jest pełna?", "náam man tem mǎi khráp", "น้ำมันเต็มไหมครับ"),
 ("B", "Pełna. Proszę oddać jutro wieczorem.", "tem khâ khuen phrûng níi tawn yen ná khá", "เต็มค่ะ คืนพรุ่งนี้ตอนเย็นนะคะ"),
], "Nigdy nie zostawiaj paszportu jako kaucji."),

("W kawiarni", "Jedzenie i napoje", "Survival", "Klient", "Barista", [
 ("B", "Dzień dobry, co podać?", "sawàt-dii khâ ráp à-rai dii khá", "สวัสดีค่ะ รับอะไรดีคะ"),
 ("A", "Poproszę kawę mrożoną.", "khǎw kaa-fae yen nòi khráp", "ขอกาแฟเย็นหน่อยครับ"),
 ("B", "Słodką?", "wǎan mǎi khá", "หวานไหมคะ"),
 ("A", "Bez cukru.", "mâi sài náam-taan khráp", "ไม่ใส่น้ำตาลครับ"),
 ("B", "Na miejscu czy na wynos?", "kin thîi nîi rǔe klàp bâan khá", "กินที่นี่หรือกลับบ้านคะ"),
 ("A", "Na wynos, proszę.", "klàp bâan khráp", "กลับบ้านครับ"),
 ("B", "Sześćdziesiąt bahtów.", "hòk-sìp bàat khâ", "หกสิบบาทค่ะ"),
], "„klàp bâan” dosłownie: wracam do domu = na wynos."),

("Masaż tajski", "Miejsca i orientacja", "A1", "Klient", "Masażystka", [
 ("A", "Ile kosztuje godzina masażu?", "nûat chûa moong lá thâo-rài khráp", "นวดชั่วโมงละเท่าไหร่ครับ"),
 ("B", "Trzysta bahtów za godzinę.", "chûa moong lá sǎam ráwi bàat khâ", "ชั่วโมงละสามร้อยบาทค่ะ"),
 ("A", "Poproszę dwie godziny.", "khǎw sǎwng chûa moong khráp", "ขอสองชั่วโมงครับ"),
 ("B", "Mocno czy delikatnie?", "nàk rǔe bao khá", "หนักหรือเบาคะ"),
 ("A", "Delikatnie, proszę.", "bao bao khráp", "เบาๆ ครับ"),
 ("B", "Boli?", "jèp mǎi khá", "เจ็บไหมคะ"),
 ("A", "Trochę. Proszę lżej.", "jèp nít nòi khráp bao long nòi", "เจ็บนิดหน่อยครับ เบาลงหน่อย"),
], "„nàk” = mocno, „bao” = delikatnie."),

("Poznawanie ludzi", "Small talk", "Survival", "Turysta", "Nowa znajoma", [
 ("B", "Cześć, jak masz na imię?", "sawàt-dii khâ khun chûe à-rai khá", "สวัสดีค่ะ คุณชื่ออะไรคะ"),
 ("A", "Mam na imię Marek. A ty?", "phǒm chûe maa-rèk khráp láew khun lâ khráp", "ผมชื่อมาเร็คครับ แล้วคุณล่ะครับ"),
 ("B", "Mam na imię Nok. Skąd jesteś?", "chǎn chûe nók khâ khun maa jàak thîi nǎi khá", "ฉันชื่อนกค่ะ คุณมาจากที่ไหนคะ"),
 ("A", "Jestem z Polski.", "phǒm maa jàak poo-laen khráp", "ผมมาจากโปแลนด์ครับ"),
 ("B", "Mówisz po tajsku?", "khun phûut thai dâai mǎi khá", "คุณพูดไทยได้ไหมคะ"),
 ("A", "Trochę mówię.", "phûut dâai nít nòi khráp", "พูดได้นิดหน่อยครับ"),
 ("B", "Mówisz bardzo dobrze!", "phûut dii mâak khâ", "พูดดีมากค่ะ"),
 ("A", "Dziękuję, miło mi.", "khàwp-khun khráp yin-dii thîi dâai rúu-jàk khráp", "ขอบคุณครับ ยินดีที่ได้รู้จักครับ"),
], "„láew khun lâ” = a ty?"),

("Rozmowa o Polsce", "Small talk", "A1", "Turysta", "Znajoma", [
 ("B", "Polska jest daleko, prawda?", "poo-laen klai mǎi khá", "โปแลนด์ไกลไหมคะ"),
 ("A", "Bardzo daleko, dwanaście godzin samolotem.", "klai mâak khráp bin sìp-sǎwng chûa moong", "ไกลมากครับ บินสิบสองชั่วโมง"),
 ("B", "Czy w Polsce jest zimno?", "thîi poo-laen nǎaw mǎi khá", "ที่โปแลนด์หนาวไหมคะ"),
 ("A", "Zimą bardzo zimno.", "nâa nǎaw nǎaw mâak khráp", "หน้าหนาวหนาวมากครับ"),
 ("B", "Lubisz tajskie jedzenie?", "châwp aa-hǎan thai mǎi khá", "ชอบอาหารไทยไหมคะ"),
 ("A", "Bardzo lubię, ale jest ostre.", "châwp mâak khráp tàe phèt", "ชอบมากครับ แต่เผ็ด"),
 ("B", "Co lubisz najbardziej?", "châwp à-rai mâak thîi sùt khá", "ชอบอะไรมากที่สุดคะ"),
 ("A", "Najbardziej lubię tom yam.", "châwp tôm yam mâak thîi sùt khráp", "ชอบต้มยำมากที่สุดครับ"),
], "„mâak thîi sùt” = najbardziej."),

("Wymiana pieniędzy", "Zakupy i pieniądze", "A1", "Turysta", "Kantor", [
 ("A", "Chcę wymienić pieniądze.", "yàak lâek ngoen khráp", "อยากแลกเงินครับ"),
 ("B", "Jaka waluta?", "ngoen à-rai khá", "เงินอะไรคะ"),
 ("A", "Euro na bahty.", "yuu-roo pen bàat khráp", "ยูโรเป็นบาทครับ"),
 ("B", "Ile chce pan wymienić?", "lâek thâo-rài khá", "แลกเท่าไหร่คะ"),
 ("A", "Dwieście euro.", "sǎwng ráwi yuu-roo khráp", "สองร้อยยูโรครับ"),
 ("B", "Poproszę paszport.", "khǎw nǎng-sǔe dəən thaang khâ", "ขอหนังสือเดินทางค่ะ"),
 ("A", "Proszę. Poproszę drobne banknoty.", "nîi khráp khǎw bae yôi dûai khráp", "นี่ครับ ขอแบงค์ย่อยด้วยครับ"),
], "„lâek ngoen” = wymienić pieniądze, „bae yôi” = drobne banknoty."),

("Problem z płatnością", "Zakupy i pieniądze", "A1", "Klient", "Kasjer", [
 ("A", "Czy przyjmujecie karty?", "ráp bàt mǎi khráp", "รับบัตรไหมครับ"),
 ("B", "Przyjmujemy, proszę wsunąć kartę.", "ráp khâ sòt bàt dâai loei khâ", "รับค่ะ สอดบัตรได้เลยค่ะ"),
 ("A", "Nie działa.", "chái mâi dâai khráp", "ใช้ไม่ได้ครับ"),
 ("B", "Proszę spróbować jeszcze raz.", "lawng ìik khráng dâai mǎi khá", "ลองอีกครั้งได้ไหมคะ"),
 ("A", "Nadal nie działa.", "yang chái mâi dâai khráp", "ยังใช้ไม่ได้ครับ"),
 ("B", "W takim razie gotówką?", "thâa yang-ngán jàai ngoen sòt dâai mǎi khá", "ถ้ายังงั้นจ่ายเงินสดได้ไหมคะ"),
 ("A", "Gdzie jest bankomat?", "tûu ee-thii-em yùu thîi nǎi khráp", "ตู้เอทีเอ็มอยู่ที่ไหนครับ"),
 ("B", "Przed sklepem.", "yùu nâa ráan khâ", "อยู่หน้าร้านค่ะ"),
], "„chái mâi dâai” = nie działa, nie da się użyć."),

("Bilet autobusowy", "Transport", "Survival", "Podróżny", "Kasa", [
 ("A", "Poproszę dwa bilety do Chiang Mai.", "khǎw tǔa pai chiang mài sǎwng bai khráp", "ขอตั๋วไปเชียงใหม่สองใบครับ"),
 ("B", "Na kiedy?", "wan nǎi khá", "วันไหนคะ"),
 ("A", "Na jutro rano.", "phrûng níi tawn cháo khráp", "พรุ่งนี้ตอนเช้าครับ"),
 ("B", "O której odjeżdża autobus?", "rót àwk kìi moong khá", "รถออกกี่โมงคะ"),
 ("A", "O której są autobusy?", "mii rót kìi moong bâang khráp", "มีรถกี่โมงบ้างครับ"),
 ("B", "O ósmej i o dziesiątej.", "pàet moong kàp sìp moong khâ", "แปดโมงกับสิบโมงค่ะ"),
 ("A", "Poproszę na ósmą.", "ao pàet moong khráp", "เอาแปดโมงครับ"),
 ("B", "Razem osiemset bahtów.", "tháng mòt pàet ráwi bàat khâ", "ทั้งหมดแปดร้อยบาทค่ะ"),
], "„kìi moong bâang” = o których godzinach (lista)."),

("W pociągu", "Transport", "A1", "Pasażer", "Konduktor", [
 ("A", "Przepraszam, to moje miejsce?", "khǎw thôot khráp thîi nâng phǒm châi mǎi khráp", "ขอโทษครับ ที่นั่งผมใช่ไหมครับ"),
 ("B", "Poproszę bilet.", "khǎw duu tǔa nòi khráp", "ขอดูตั๋วหน่อยครับ"),
 ("A", "Proszę.", "nîi khráp", "นี่ครับ"),
 ("B", "Pana miejsce jest tam.", "thîi nâng khun yùu thîi nân khráp", "ที่นั่งคุณอยู่ที่นั่นครับ"),
 ("A", "O której dojedziemy?", "thǔeng kìi moong khráp", "ถึงกี่โมงครับ"),
 ("B", "Około szóstej wieczorem.", "pramaan hòk moong yen khráp", "ประมาณหกโมงเย็นครับ"),
 ("A", "Czy jest tu jedzenie?", "bon rót mii aa-hǎan mǎi khráp", "บนรถมีอาหารไหมครับ"),
 ("B", "Jest, w wagonie obok.", "mii khráp yùu tûu tìt kan", "มีครับ อยู่ตู้ติดกัน"),
], "„thǔeng” = dotrzeć, przyjechać."),

("Łódź na wyspę", "Transport", "A1", "Turysta", "Kasa", [
 ("A", "O której odpływa łódź?", "ruea àwk kìi moong khráp", "เรือออกกี่โมงครับ"),
 ("B", "Za pół godziny.", "ìik khrûeng chûa moong khâ", "อีกครึ่งชั่วโมงค่ะ"),
 ("A", "Jak długo płyniemy?", "chái weelaa kìi chûa moong khráp", "ใช้เวลากี่ชั่วโมงครับ"),
 ("B", "Około dwóch godzin.", "pramaan sǎwng chûa moong khâ", "ประมาณสองชั่วโมงค่ะ"),
 ("A", "Poproszę jeden bilet.", "khǎw tǔa nùeng bai khráp", "ขอตั๋วหนึ่งใบครับ"),
 ("B", "Czterysta bahtów.", "sìi ráwi bàat khâ", "สี่ร้อยบาทค่ะ"),
 ("A", "Czy dziś jest spokojne morze?", "wan níi thalee ngîap mǎi khráp", "วันนี้ทะเลเงียบไหมครับ"),
 ("B", "Dziś spokojne.", "wan níi ngîap khâ", "วันนี้เงียบค่ะ"),
], "„ìik khrûeng chûa moong” = za pół godziny."),

("Jedzenie z ulicy", "Jedzenie i napoje", "Survival", "Klient", "Sprzedawca", [
 ("A", "Co to jest?", "nîi à-rai khráp", "นี่อะไรครับ"),
 ("B", "Kurczak z ryżem.", "khâaw man kài khráp", "ข้าวมันไก่ครับ"),
 ("A", "Poproszę jedną porcję.", "khǎw nùeng thîi khráp", "ขอหนึ่งที่ครับ"),
 ("B", "Ostre?", "sài phrík mǎi khráp", "ใส่พริกไหมครับ"),
 ("A", "Bez chili.", "mâi sài phrík khráp", "ไม่ใส่พริกครับ"),
 ("B", "Pięćdziesiąt bahtów.", "hâa-sìp bàat khráp", "ห้าสิบบาทครับ"),
 ("A", "Na wynos, proszę.", "sài thǔng khráp", "ใส่ถุงครับ"),
], "„nùeng thîi” = jedna porcja."),

("Pralnia", "Dom i codzienność", "A1", "Klient", "Pralnia", [
 ("A", "Chcę oddać rzeczy do prania.", "yàak sák phâa khráp", "อยากซักผ้าครับ"),
 ("B", "Ile kilogramów?", "kìi kì-loo khá", "กี่กิโลคะ"),
 ("A", "Około trzech kilogramów.", "pramaan sǎam kì-loo khráp", "ประมาณสามกิโลครับ"),
 ("B", "Czterdzieści bahtów za kilogram.", "kì-loo lá sìi-sìp bàat khâ", "กิโลละสี่สิบบาทค่ะ"),
 ("A", "Kiedy będzie gotowe?", "sèt mûea rài khráp", "เสร็จเมื่อไหร่ครับ"),
 ("B", "Jutro po południu.", "phrûng níi tawn bàai khâ", "พรุ่งนี้ตอนบ่ายค่ะ"),
 ("A", "Dobrze, przyjdę jutro.", "dâai khráp phrûng níi maa ráp", "ได้ครับ พรุ่งนี้มารับ"),
], "„sèt” = gotowe, skończone."),

("Karta SIM", "Dom i codzienność", "A1", "Klient", "Sprzedawca", [
 ("A", "Chcę kupić kartę SIM.", "yàak súe sim kâat khráp", "อยากซื้อซิมการ์ดครับ"),
 ("B", "Na ile dni?", "chái kìi wan khá", "ใช้กี่วันคะ"),
 ("A", "Na dwa tygodnie.", "sǎwng aa-thít khráp", "สองอาทิตย์ครับ"),
 ("B", "Ten pakiet, dwieście dziewięćdziesiąt bahtów.", "phaek-kèt níi sǎwng ráwi kâo-sìp bàat khâ", "แพ็กเกจนี้สองร้อยเก้าสิบบาทค่ะ"),
 ("A", "Czy internet jest szybki?", "in-təə-nét rew mǎi khráp", "อินเทอร์เน็ตเร็วไหมครับ"),
 ("B", "Bardzo szybki.", "rew mâak khâ", "เร็วมากค่ะ"),
 ("A", "Poproszę paszport? Proszę.", "tâwng chái nǎng-sǔe dəən thaang mǎi khráp", "ต้องใช้หนังสือเดินทางไหมครับ"),
 ("B", "Tak, poproszę.", "tâwng chái khâ khǎw dûai khâ", "ต้องใช้ค่ะ ขอด้วยค่ะ"),
], "Rejestracja karty SIM wymaga paszportu."),

("Zgubiony telefon", "Awarie i pomoc", "Survival", "Turysta", "Obsługa", [
 ("A", "Przepraszam, zgubiłem telefon.", "khǎw thôot khráp phǒm tham thoo-rasàp hǎai", "ขอโทษครับ ผมทำโทรศัพท์หาย"),
 ("B", "Gdzie go pan zostawił?", "wái thîi nǎi khá", "ไว้ที่ไหนคะ"),
 ("A", "Chyba w taksówce.", "khít wâa yùu nai tháek-sîi khráp", "คิดว่าอยู่ในแท็กซี่ครับ"),
 ("B", "Ma pan numer taksówki?", "mii bəə rót mǎi khá", "มีเบอร์รถไหมคะ"),
 ("A", "Nie mam.", "mâi mii khráp", "ไม่มีครับ"),
 ("B", "Proszę zgłosić na policję.", "jâeng tamrùat dii kwàa khâ", "แจ้งตำรวจดีกว่าค่ะ"),
 ("A", "Gdzie jest komisariat?", "sathǎanii tamrùat yùu thîi nǎi khráp", "สถานีตำรวจอยู่ที่ไหนครับ"),
 ("B", "Niedaleko stąd, pięć minut.", "mâi klai jàak thîi nîi hâa naa-thii khâ", "ไม่ไกลจากที่นี่ ห้านาทีค่ะ"),
], "„tham … hǎai” = zgubić coś."),

("Na policji", "Awarie i pomoc", "A1", "Turysta", "Policjant", [
 ("A", "Chcę zgłosić kradzież.", "yàak jâeng khwaam khráp", "อยากแจ้งความครับ"),
 ("B", "Co się stało?", "kə̀ət à-rai khûen khráp", "เกิดอะไรขึ้นครับ"),
 ("A", "Skradziono mi torbę.", "krapǎo phǒm thùuk khamooi khráp", "กระเป๋าผมถูกขโมยครับ"),
 ("B", "Gdzie i kiedy?", "thîi nǎi láew mûea rài khráp", "ที่ไหนแล้วเมื่อไหร่ครับ"),
 ("A", "Na targu, godzinę temu.", "thîi talàat mûea chûa moong thîi láew khráp", "ที่ตลาด เมื่อชั่วโมงที่แล้วครับ"),
 ("B", "Co było w torbie?", "nai krapǎo mii à-rai bâang khráp", "ในกระเป๋ามีอะไรบ้างครับ"),
 ("A", "Paszport i pieniądze.", "nǎng-sǔe dəən thaang kàp ngoen khráp", "หนังสือเดินทางกับเงินครับ"),
 ("B", "Proszę wypełnić ten formularz.", "krúnaa kràwk èek-kasǎan níi khráp", "กรุณากรอกเอกสารนี้ครับ"),
], "„jâeng khwaam” = złożyć zawiadomienie."),

("Umawianie spotkania", "Small talk", "A1", "Znajomy", "Znajoma", [
 ("A", "Masz czas jutro?", "phrûng níi wâang mǎi khráp", "พรุ่งนี้ว่างไหมครับ"),
 ("B", "Jutro wieczorem mam czas.", "phrûng níi tawn yen wâang khâ", "พรุ่งนี้ตอนเย็นว่างค่ะ"),
 ("A", "Zjemy razem kolację?", "pai kin khâaw dûai kan mǎi khráp", "ไปกินข้าวด้วยกันไหมครับ"),
 ("B", "Chętnie. O której?", "dâai khâ kìi moong khá", "ได้ค่ะ กี่โมงคะ"),
 ("A", "O szóstej wieczorem.", "hòk moong yen khráp", "หกโมงเย็นครับ"),
 ("B", "Gdzie się spotkamy?", "jəə kan thîi nǎi khá", "เจอกันที่ไหนคะ"),
 ("A", "Przed centrum handlowym.", "nâa hâang khráp", "หน้าห้างครับ"),
 ("B", "Dobrze, do zobaczenia jutro.", "dâai khâ jəə kan phrûng níi khâ", "ได้ค่ะ เจอกันพรุ่งนี้ค่ะ"),
], "„pai … dûai kan” = pójść razem."),

("W pracy: spóźnienie", "Praca i nauka", "A1", "Pracownik", "Szef", [
 ("A", "Przepraszam za spóźnienie.", "khǎw thôot thîi maa sǎai khráp", "ขอโทษที่มาสายครับ"),
 ("B", "Co się stało?", "pen à-rai khráp", "เป็นอะไรครับ"),
 ("A", "Był korek.", "rót tìt khráp", "รถติดครับ"),
 ("B", "Rozumiem, nie ma sprawy.", "khâo-jai khráp mâi pen rai", "เข้าใจครับ ไม่เป็นไร"),
 ("A", "Jutro przyjdę wcześniej.", "phrûng níi jà maa réw khûen khráp", "พรุ่งนี้จะมาเร็วขึ้นครับ"),
 ("B", "Mamy dziś spotkanie o dziesiątej.", "wan níi mii prachum sìp moong khráp", "วันนี้มีประชุมสิบโมงครับ"),
 ("A", "Będę gotowy.", "phǒm phráwm khráp", "ผมพร้อมครับ"),
], "„rót tìt” = korek uliczny."),

("Wynajem mieszkania", "Dom i codzienność", "A1", "Najemca", "Właściciel", [
 ("A", "Czy jest wolny pokój?", "mii hâwng wâang mǎi khráp", "มีห้องว่างไหมครับ"),
 ("B", "Jest. Miesięcznie osiem tysięcy.", "mii khâ duean lá pàet phan khâ", "มีค่ะ เดือนละแปดพันค่ะ"),
 ("A", "Czy prąd i woda są wliczone?", "ruam khâa fai kàp khâa náam mǎi khráp", "รวมค่าไฟกับค่าน้ำไหมครับ"),
 ("B", "Nie, płaci się osobno.", "mâi ruam khâ jàai tàang hàak khâ", "ไม่รวมค่ะ จ่ายต่างหากค่ะ"),
 ("A", "Czy mogę zobaczyć pokój?", "khǎw duu hâwng dâai mǎi khráp", "ขอดูห้องได้ไหมครับ"),
 ("B", "Proszę bardzo.", "chəən khâ", "เชิญค่ะ"),
 ("A", "Jest klimatyzacja?", "mii ae mǎi khráp", "มีแอร์ไหมครับ"),
 ("B", "Jest, i lodówka.", "mii khâ láew kâw mii tûu yen khâ", "มีค่ะ แล้วก็มีตู้เย็นค่ะ"),
], "„khâa fai” = rachunek za prąd, „khâa náam” = za wodę."),

("Zakupy spożywcze", "Zakupy i pieniądze", "A1", "Klient", "Sprzedawczyni", [
 ("A", "Ile kosztują mango?", "mamûang thâo-rài khráp", "มะม่วงเท่าไหร่ครับ"),
 ("B", "Kilogram sto bahtów.", "kì-loo lá nùeng ráwi bàat khâ", "กิโลละหนึ่งร้อยบาทค่ะ"),
 ("A", "Poproszę dwa kilogramy.", "khǎw sǎwng kì-loo khráp", "ขอสองกิโลครับ"),
 ("B", "Coś jeszcze?", "ao à-rai ìik mǎi khá", "เอาอะไรอีกไหมคะ"),
 ("A", "Poproszę jeszcze banany.", "khǎw klûai dûai khráp", "ขอกล้วยด้วยครับ"),
 ("B", "Razem dwieście pięćdziesiąt bahtów.", "tháng mòt sǎwng ráwi hâa-sìp bàat khâ", "ทั้งหมดสองร้อยห้าสิบบาทค่ะ"),
 ("A", "Proszę, tu jest pięćset.", "nîi khráp hâa ráwi", "นี่ครับ ห้าร้อย"),
 ("B", "Reszta dwieście pięćdziesiąt.", "thawn sǎwng ráwi hâa-sìp khâ", "ทอนสองร้อยห้าสิบค่ะ"),
], "„kì-loo lá” = za kilogram."),

("W świątyni", "Miejsca i orientacja", "A1", "Turysta", "Przewodniczka", [
 ("A", "Czy mogę tu wejść?", "khâo pai dâai mǎi khráp", "เข้าไปได้ไหมครับ"),
 ("B", "Można, ale proszę zdjąć buty.", "dâai khâ tàe tâwng thàwt rawng tháo khâ", "ได้ค่ะ แต่ต้องถอดรองเท้าค่ะ"),
 ("A", "Czy mogę robić zdjęcia?", "thàai rûup dâai mǎi khráp", "ถ่ายรูปได้ไหมครับ"),
 ("B", "Można na zewnątrz, w środku nie.", "khâang nâwk dâai khâang nai mâi dâai khâ", "ข้างนอกได้ ข้างในไม่ได้ค่ะ"),
 ("A", "Rozumiem, dziękuję.", "khâo-jai láew khráp khàwp-khun khráp", "เข้าใจแล้วครับ ขอบคุณครับ"),
 ("B", "Świątynia ma trzysta lat.", "wát níi aayú sǎam ráwi pii khâ", "วัดนี้อายุสามร้อยปีค่ะ"),
 ("A", "Bardzo piękna.", "sǔai mâak khráp", "สวยมากครับ"),
], "W świątyni zakrywaj ramiona i kolana."),

("Na plaży", "Miejsca i orientacja", "A1", "Turysta", "Wypożyczalnia", [
 ("A", "Ile kosztuje leżak?", "tiang chaai hàat thâo-rài khráp", "เตียงชายหาดเท่าไหร่ครับ"),
 ("B", "Sto bahtów na cały dzień.", "wan lá nùeng ráwi bàat khâ", "วันละหนึ่งร้อยบาทค่ะ"),
 ("A", "Poproszę dwa.", "khǎw sǎwng an khráp", "ขอสองอันครับ"),
 ("B", "Proszę tutaj.", "chəən trong níi khâ", "เชิญตรงนี้ค่ะ"),
 ("A", "Czy tu można pływać?", "wâai náam thîi nîi dâai mǎi khráp", "ว่ายน้ำที่นี่ได้ไหมครับ"),
 ("B", "Można, ale dziś są fale.", "dâai khâ tàe wan níi khlûen yóe khâ", "ได้ค่ะ แต่วันนี้คลื่นเยอะค่ะ"),
 ("A", "Będę uważał.", "jà rawang khráp", "จะระวังครับ"),
], "„khlûen” = fale."),

("Codzienny poranek", "Dom i codzienność", "A1", "Współlokator", "Współlokatorka", [
 ("A", "Dzień dobry, jak spałaś?", "sawàt-dii khráp nawn làp dii mǎi khráp", "สวัสดีครับ นอนหลับดีไหมครับ"),
 ("B", "Dobrze, dziękuję.", "làp dii khâ khàwp-khun khâ", "หลับดีค่ะ ขอบคุณค่ะ"),
 ("A", "Jadłaś już śniadanie?", "kin khâaw cháo rúe yang khá", "กินข้าวเช้าหรือยังคะ"),
 ("B", "Jeszcze nie.", "yang mâi dâai kin khâ", "ยังไม่ได้กินค่ะ"),
 ("A", "Chodźmy coś zjeść.", "pai kin khâaw kan thòe", "ไปกินข้าวกันเถอะ"),
 ("B", "Dobrze, chodźmy.", "dâai khâ pai kan", "ได้ค่ะ ไปกัน"),
], "„… rúe yang” = czy już? Odpowiedź: „láew” (już) lub „yang” (jeszcze nie)."),

("Prośba o pomoc na ulicy", "Awarie i pomoc", "Survival", "Turysta", "Przechodzień", [
 ("A", "Przepraszam, czy może mi pan pomóc?", "khǎw thôot khráp chûai nòi dâai mǎi khráp", "ขอโทษครับ ช่วยหน่อยได้ไหมครับ"),
 ("B", "Co się stało?", "mii à-rai khráp", "มีอะไรครับ"),
 ("A", "Zgubiłem się.", "phǒm lǒng thaang khráp", "ผมหลงทางครับ"),
 ("A", "Chcę wrócić do hotelu.", "yàak klàp roong raem khráp", "อยากกลับโรงแรมครับ"),
 ("B", "Który hotel?", "roong raem à-rai khráp", "โรงแรมอะไรครับ"),
 ("A", "Nie pamiętam nazwy, mam adres.", "jam chûe mâi dâai tàe mii thîi yùu khráp", "จำชื่อไม่ได้ แต่มีที่อยู่ครับ"),
 ("B", "Proszę pokazać. Wezwę taksówkę.", "khǎw duu nòi khráp dǐaw rîak tháek-sîi hâi", "ขอดูหน่อยครับ เดี๋ยวเรียกแท็กซี่ให้"),
 ("A", "Dziękuję bardzo!", "khàwp-khun mâak khráp", "ขอบคุณมากครับ"),
], "„rîak … hâi” = zawołać coś dla kogoś."),
]
