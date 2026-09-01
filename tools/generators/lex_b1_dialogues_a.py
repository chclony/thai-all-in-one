# -*- coding: utf-8 -*-
"""Dialogi etapu 4 (B1) — czesc A.

Zakres: rozwijanie opinii i uprzejma niezgoda, opowiadanie historii, praca
i spotkania, reklamacje i uslugi, bank oraz formalnosci.

Krotka: (tytul, sytuacja, poziom, rola A, rola B, kwestie, notatka)
Kwestia: (rola, polski, fonetyka, tajski)
"""

DIALOGUES_B1_A = [

("Rozmowa o planach na wieczór", "Small talk", "B1", "Znajomy", "Znajoma", [
 ("A", "Masz jakieś plany na wieczór?", "yen níi mii phǎen à-rai mǎi khráp", "เย็นนี้มีแผนอะไรไหมครับ"),
 ("B", "Jeszcze się zastanawiam.", "yang khít yùu khâ", "ยังคิดอยู่ค่ะ"),
 ("A", "Może pójdziemy coś zjeść?", "pai kin khâao kan mǎi khráp", "ไปกินข้าวกันไหมครับ"),
 ("B", "Chętnie, ale nie chcę wracać późno.", "dii khâ tàae mâi yàak klàp dùek", "ดีค่ะ แต่ไม่อยากกลับดึก"),
 ("A", "Rozumiem. To wybierzmy coś blisko.", "khâo-jai khráp ngán lûeak thîi klâi klâi", "เข้าใจครับ งั้นเลือกที่ใกล้ๆ"),
 ("B", "Świetnie. O której?", "dii loei khâ kìi moong khâ", "ดีเลยค่ะ กี่โมงคะ"),
 ("A", "Powiedzmy o siódmej.", "kâw prà-maan nùeng thûm khráp", "ก็ประมาณหนึ่งทุ่มครับ"),
 ("B", "Pasuje. Dam znać, jak wyjdę.", "dâai khâ dǐao bàwk tawn àwk", "ได้ค่ะ เดี๋ยวบอกตอนออก"),
], "Kobieta kończy zdania na „khâ”, mężczyzna na „khráp”. „nùeng thûm” to 19:00 — tajski liczy wieczorne godziny osobno."),

("Różnica zdań o cenie", "Zakupy i pieniądze", "B1", "Kupujący", "Znajomy", [
 ("A", "Moim zdaniem to za drogo.", "nai khwaam-khít phǒm man phaeng koen pai khráp", "ในความคิดผมมันแพงเกินไปครับ"),
 ("B", "Zgadzam się, ale jakość jest dobra.", "hěn dûai khráp tàae khun-ná-phâap dii", "เห็นด้วยครับ แต่คุณภาพดี"),
 ("A", "Może i tak, ale spójrz na to inaczej.", "kâw àat jà châi khráp tàae lawng mawng ìik mum", "ก็อาจจะใช่ครับ แต่ลองมองอีกมุม"),
 ("B", "Mów śmiało.", "wâa maa loei khráp", "ว่ามาเลยครับ"),
 ("A", "Obok jest to samo o połowę taniej.", "khâang khâang khǎwng mǔean kan tàae thùuk kwàa khrûeng nùeng", "ข้างๆ ของเหมือนกันแต่ถูกกว่าครึ่งหนึ่ง"),
 ("B", "Nie wiedziałem o tym.", "phǒm mâi rúu maa kàwn khráp", "ผมไม่รู้มาก่อนครับ"),
 ("A", "Sprawdźmy najpierw tam.", "lawng pai duu thîi nân kàwn khráp", "ลองไปดูที่นั่นก่อนครับ"),
 ("B", "Przekonałeś mnie.", "khun tham hâi phǒm khâo-jai láew khráp", "คุณทำให้ผมเข้าใจแล้วครับ"),
], "Tajski schemat sporu: najpierw „hěn dûai”, dopiero potem „tàae”. Otwarcie od „mâi” brzmiałoby konfrontacyjnie."),

("Opowieść o zgubionym bagażu", "Transport", "B1", "Podróżny", "Znajomy", [
 ("A", "Opowiem ci, co się stało wczoraj.", "jà lâo hâi fang wâa mûea waan kòet à-rai khûen", "จะเล่าให้ฟังว่าเมื่อวานเกิดอะไรขึ้น"),
 ("B", "Słucham.", "fang yùu khráp", "ฟังอยู่ครับ"),
 ("A", "Na początku wszystko było w porządku.", "tawn râek thúk yàang kâw pòk-kà-tì dii", "ตอนแรกทุกอย่างก็ปกติดี"),
 ("B", "A potem?", "láew ngai tàw khráp", "แล้วไงต่อครับ"),
 ("A", "Na lotnisku nie było mojej walizki.", "thîi sà-nǎam bin krà-pǎo phǒm mâi maa", "ที่สนามบินกระเป๋าผมไม่มา"),
 ("B", "O rany. I co zrobiłeś?", "óo hǒo láew tham yang-ngai khráp", "โอ้โห แล้วทำยังไงครับ"),
 ("A", "Zgłosiłem to od razu przy stanowisku.", "phǒm jâeng thîi kaao-nôoe loei khráp", "ผมแจ้งที่เคาน์เตอร์เลยครับ"),
 ("B", "Dobrze, że od razu.", "dii thîi jâeng thán-thii khráp", "ดีที่แจ้งทันทีครับ"),
 ("A", "W końcu przywieźli ją wieczorem.", "sùt-tháai kâw ao maa sòng tawn yen", "สุดท้ายก็เอามาส่งตอนเย็น"),
 ("B", "Ulżyło mi.", "khôi yang chûa khráp", "ค่อยยังชั่วครับ"),
], "„tawn râek … lǎng jàak nán … sùt-tháai” to szkielet każdej dłuższej opowieści po tajsku."),

("Spóźnienie na spotkanie", "Praca i nauka", "B1", "Pracownik", "Kolega", [
 ("A", "Spóźnię się dziesięć minut.", "phǒm jà thǔeng cháa sìp naa-thii khráp", "ผมจะถึงช้าสิบนาทีครับ"),
 ("B", "Nie ma sprawy, poczekamy.", "mâi pen rai khráp raw dâai", "ไม่เป็นไรครับ รอได้"),
 ("A", "Utknąłem w korku.", "rót tìt khráp", "รถติดครับ"),
 ("B", "Zaczniemy od pierwszego punktu.", "rao jà rôoem khâw râek kàwn khráp", "เราจะเริ่มข้อแรกก่อนครับ"),
 ("A", "Dobrze. Prześlij mi potem notatkę.", "dâai khráp dǐao sòng sà-rùp hâi dûai", "ได้ครับ เดี๋ยวส่งสรุปให้ด้วย"),
 ("B", "Zapiszę wszystko.", "dǐao jòt wái hâi khráp", "เดี๋ยวจดไว้ให้ครับ"),
 ("A", "Dziękuję, liczę na ciebie.", "khàwp-khun khráp fàak dûai ná", "ขอบคุณครับ ฝากด้วยนะ"),
 ("B", "Zrobi się.", "dâai loei khráp", "ได้เลยครับ"),
], "„fàak dûai ná” to jedno z najczęstszych zdań w tajskim biurze — nie ma dokładnego polskiego odpowiednika."),

("Ustalanie terminu zebrania", "Praca i nauka", "B1", "Kierownik", "Pracownik", [
 ("A", "Kiedy panu pasuje?", "khun sà-dùak wan nǎi khráp", "คุณสะดวกวันไหนครับ"),
 ("B", "W czwartek rano.", "wan phá-rúe-hàt cháo khráp", "วันพฤหัสเช้าครับ"),
 ("A", "Mam wtedy inne spotkanie.", "wan nán phǒm mii prà-chum ùen khráp", "วันนั้นผมมีประชุมอื่นครับ"),
 ("B", "To może piątek po południu?", "ngán wan sùk bàai dâai mǎi khráp", "งั้นวันศุกร์บ่ายได้ไหมครับ"),
 ("A", "Pasuje. O drugiej.", "dâai khráp bàai sǎwng moong", "ได้ครับ บ่ายสองโมง"),
 ("B", "Ile potrwa?", "chái wee-laa naan thâo-rài khráp", "ใช้เวลานานเท่าไหร่ครับ"),
 ("A", "Około godziny.", "prà-maan nùeng chûa moong khráp", "ประมาณหนึ่งชั่วโมงครับ"),
 ("B", "Zanotowałem.", "jòt wái láew khráp", "จดไว้แล้วครับ"),
], "„sà-dùak” dosłownie „być wygodnym”. Tajowie pytają o wygodę rozmówcy, nie o wolny termin w kalendarzu."),

("Uwagi do projektu", "Praca i nauka", "B1", "Kierownik", "Pracownik", [
 ("A", "Mam kilka uwag.", "phǒm mii khwaam-hěn baang khâw khráp", "ผมมีความเห็นบางข้อครับ"),
 ("B", "Słucham.", "wâa maa loei khráp", "ว่ามาเลยครับ"),
 ("A", "Zrobiłeś to dobrze, ale można jeszcze poprawić.", "tham dâai dii khráp tàae yang phát-thá-naa dâai ìik", "ทำได้ดีครับ แต่ยังพัฒนาได้อีก"),
 ("B", "Powiedz, gdzie dokładnie.", "bàwk nòi khráp wâa trong nǎi", "บอกหน่อยครับว่าตรงไหน"),
 ("A", "Druga część jest za długa.", "sùan thîi sǎwng yaao koen pai khráp", "ส่วนที่สองยาวเกินไปครับ"),
 ("B", "Rozumiem. Skrócę ją.", "khâo-jai khráp dǐao tàt hâi sân long", "เข้าใจครับ เดี๋ยวตัดให้สั้นลง"),
 ("A", "Do kiedy zdążysz?", "sèt phaai nai mûea-rài khráp", "เสร็จภายในเมื่อไหร่ครับ"),
 ("B", "Do jutra wieczorem.", "phrûng níi tawn yen khráp", "พรุ่งนี้ตอนเย็นครับ"),
 ("A", "Dobrze, liczę na ciebie.", "dii khráp fàak dûai ná", "ดีครับ ฝากด้วยนะ"),
], "Krytyka zaczyna się od pochwały. „phát-thá-naa dâai ìik” brzmi łagodniej niż wprost „mâi dii”."),

("Rozmowa o zmianie pracy", "Praca i nauka", "B1", "Znajomy", "Znajomy", [
 ("A", "Zmieniam pracę.", "phǒm plìan ngaan khráp", "ผมเปลี่ยนงานครับ"),
 ("B", "Serio, naprawdę?", "jing jing rǒe khráp", "จริงๆ หรือครับ"),
 ("A", "Tak. Długo się zastanawiałem.", "khráp khít yùu naan mǔean kan", "ครับ คิดอยู่นานเหมือนกัน"),
 ("B", "Co cię przekonało?", "à-rai tham hâi tàt-sǐn jai khráp", "อะไรทำให้ตัดสินใจครับ"),
 ("A", "Chcę żyć spokojniej.", "phǒm yàak chai chii-wít hâi ngîap long khráp", "ผมอยากใช้ชีวิตให้เงียบลงครับ"),
 ("B", "Rozumiem cię.", "khâo-jai khráp", "เข้าใจครับ"),
 ("A", "Nowa firma jest bliżej domu.", "bà-rí-sàt mài yùu klâi bâan kwàa", "บริษัทใหม่อยู่ใกล้บ้านกว่า"),
 ("B", "To dobra wiadomość. Powodzenia.", "pen khàao dii khráp chôok dii ná", "เป็นข่าวดีครับ โชคดีนะ"),
], "„chái chii-wít” dosłownie „używać życia” — tajski idiom na prowadzenie życia w jakimś stylu."),

("Reklamacja zamówienia online", "Zakupy i pieniądze", "B1", "Klient", "Obsługa", [
 ("A", "Chciałbym zgłosić problem.", "phǒm yàak jâeng pan-hǎa khráp", "ผมอยากแจ้งปัญหาครับ"),
 ("B", "Proszę powiedzieć, co się stało.", "lâo maa dâai loei khráp", "เล่ามาได้เลยครับ"),
 ("A", "Towar przyszedł uszkodzony.", "khǎwng thîi sòng maa chamrút khráp", "ของที่ส่งมาชำรุดครับ"),
 ("B", "Bardzo przepraszamy. Ma pan zdjęcie?", "khǎw-thôot mâak khráp mii rûup mǎi khráp", "ขอโทษมากครับ มีรูปไหมครับ"),
 ("A", "Wyślę na czacie.", "dǐao sòng thaang sáet khráp", "เดี๋ยวส่งทางแชทครับ"),
 ("B", "Wymienimy na nowy.", "dǐao plìan an mài hâi khráp", "เดี๋ยวเปลี่ยนอันใหม่ให้ครับ"),
 ("A", "Ile to potrwa?", "tâwng chái wee-laa naan thâo-rài khráp", "ต้องใช้เวลานานเท่าไหร่ครับ"),
 ("B", "Około trzech dni.", "prà-maan sǎam wan khráp", "ประมาณสามวันครับ"),
 ("A", "Rozumiem, że to nie pana wina.", "phǒm khâo-jai wâa mâi châi khwaam phìt khǎwng khun", "ผมเข้าใจว่าไม่ใช่ความผิดของคุณ"),
 ("B", "Dziękuję za wyrozumiałość.", "khàwp-khun thîi khâo-jai khráp", "ขอบคุณที่เข้าใจครับ"),
], "Zdanie o braku winy rozmówcy pozwala mu zachować twarz i realnie przyspiesza załatwienie sprawy."),

("Zwrot towaru w sklepie", "Zakupy i pieniądze", "B1", "Klient", "Sprzedawca", [
 ("A", "Czy mogę to zwrócić?", "khǒen khǎwng dâai mǎi khráp", "คืนของได้ไหมครับ"),
 ("B", "Ma pan paragon?", "mii bai sèt mǎi khráp", "มีใบเสร็จไหมครับ"),
 ("A", "Tak, proszę.", "mii khráp nîi khráp", "มีครับ นี่ครับ"),
 ("B", "Co było nie tak?", "man mii pan-hǎa à-rai khráp", "มันมีปัญหาอะไรครับ"),
 ("A", "Rozmiar nie pasuje.", "sái mâi phaw dii khráp", "ไซส์ไม่พอดีครับ"),
 ("B", "Może wymiana na inny rozmiar?", "plìan sái dii mǎi khráp", "เปลี่ยนไซส์ดีไหมครับ"),
 ("A", "Wolałbym zwrot pieniędzy.", "phǒm khǎw khǒen ngoen dii kwàa khráp", "ผมขอคืนเงินดีกว่าครับ"),
 ("B", "Zwrot w ciągu trzech dni.", "khǒen ngoen phaai nai sǎam wan khráp", "คืนเงินภายในสามวันครับ"),
], "„phaw dii” znaczy „w sam raz”. „mâi phaw dii” to nie „za małe”, tylko „nie leży”."),

("Rachunek się nie zgadza", "Restauracja", "B1", "Gość", "Kelner", [
 ("A", "Przepraszam, rachunek się nie zgadza.", "khǎw-thôot khráp bin mâi trong", "ขอโทษครับ บิลไม่ตรง"),
 ("B", "Sprawdzę jeszcze raz.", "dǐao chék mài khráp", "เดี๋ยวเช็คใหม่ครับ"),
 ("A", "Policzyliście napój dwa razy.", "khít khâa khrûeang dùem sáwn kan khráp", "คิดค่าเครื่องดื่มซ้อนกันครับ"),
 ("B", "Rzeczywiście, przepraszam.", "jing dûai khráp khǎw-thôot", "จริงด้วยครับ ขอโทษ"),
 ("A", "Nic nie szkodzi.", "mâi pen rai khráp", "ไม่เป็นไรครับ"),
 ("B", "Poprawię i przyniosę nowy.", "dǐao kâe láew ao maa mài khráp", "เดี๋ยวแก้แล้วเอามาใหม่ครับ"),
 ("A", "Dziękuję.", "khàwp-khun khráp", "ขอบคุณครับ"),
 ("B", "Przepraszam za kłopot.", "khǎw-thôot nai khwaam mâi sà-dùak khráp", "ขอโทษในความไม่สะดวกครับ"),
], "„khǎw-thôot nai khwaam mâi sà-dùak” to formuła oficjalna — usłyszysz ją też w komunikatach na dworcu."),

("Zakładanie konta w banku", "Zakupy i pieniądze", "B1", "Klient", "Pracownik banku", [
 ("A", "Chciałbym założyć konto.", "phǒm yàak pòoet ban-chii khráp", "ผมอยากเปิดบัญชีครับ"),
 ("B", "Poproszę paszport.", "khǎw phaas-pàwt dûai khráp", "ขอพาสปอร์ตด้วยครับ"),
 ("A", "Proszę. Czy potrzeba czegoś jeszcze?", "nîi khráp tâwng chái à-rai ìik mǎi khráp", "นี่ครับ ต้องใช้อะไรอีกไหมครับ"),
 ("B", "Potrzebny jest adres zamieszkania.", "tâwng chái thîi yùu dûai khráp", "ต้องใช้ที่อยู่ด้วยครับ"),
 ("A", "Mam umowę najmu.", "phǒm mii sǎn-yaa châo khráp", "ผมมีสัญญาเช่าครับ"),
 ("B", "To wystarczy. Proszę wypełnić formularz.", "khâe níi phaw khráp krù-naa kràwk bàep fawm", "แค่นี้พอครับ กรุณากรอกแบบฟอร์ม"),
 ("A", "Gdzie mam podpisać?", "sen trong nǎi khráp", "เซ็นตรงไหนครับ"),
 ("B", "Tu na dole.", "trong dâan lâang khráp", "ตรงด้านล่างครับ"),
 ("A", "Jakie są opłaty?", "khâa tham-niam thâo-rài khráp", "ค่าธรรมเนียมเท่าไหร่ครับ"),
 ("B", "Dwieście bahtów rocznie.", "pii lá sǎwng ráwi bàat khráp", "ปีละสองร้อยบาทครับ"),
], "„krù-naa” to formalne „proszę” z tabliczek i formularzy. W rozmowie brzmiałoby sztywno."),

("Problem z przelewem", "Zakupy i pieniądze", "B1", "Klient", "Pracownik banku", [
 ("A", "Przelew nie doszedł.", "ngoen thîi oon yang mâi khâo khráp", "เงินที่โอนยังไม่เข้าครับ"),
 ("B", "Kiedy pan przelewał?", "oon mûea-rài khráp", "โอนเมื่อไหร่ครับ"),
 ("A", "Wczoraj rano.", "mûea waan tawn cháo khráp", "เมื่อวานตอนเช้าครับ"),
 ("B", "Ma pan potwierdzenie?", "mii sà-lìp mǎi khráp", "มีสลิปไหมครับ"),
 ("A", "Tak, w telefonie.", "mii khráp yùu nai mue-thǔe", "มีครับ อยู่ในมือถือ"),
 ("B", "Sprawdzę w systemem.", "dǐao chék nai rá-bòp hâi khráp", "เดี๋ยวเช็คในระบบให้ครับ"),
 ("A", "Kto odpowiada za taką sprawę?", "khrai ráp phìt châwp rûeang níi khráp", "ใครรับผิดชอบเรื่องนี้ครับ"),
 ("B", "Nasz dział rozliczeń. Zgłoszę to.", "fàai kaan ngoen khráp dǐao jâeng hâi", "ฝ่ายการเงินครับ เดี๋ยวแจ้งให้"),
], "„sà-lìp” to zapożyczone slip — potwierdzenie transakcji. Tajowie prawie zawsze proszą o zrzut ekranu."),

("Przedłużanie wizy", "Praca i nauka", "B1", "Obcokrajowiec", "Urzędnik", [
 ("A", "Muszę przedłużyć wizę.", "phǒm tâwng tàw wii-sâa khráp", "ผมต้องต่อวีซ่าครับ"),
 ("B", "Kiedy wygasa?", "mòt aa-yú mûea-rài khráp", "หมดอายุเมื่อไหร่ครับ"),
 ("A", "Za dwa tygodnie.", "ìik sǎwng aa-thít khráp", "อีกสองอาทิตย์ครับ"),
 ("B", "Jakie dokumenty pan przyniósł?", "ao èek-kà-sǎan à-rai maa bâang khráp", "เอาเอกสารอะไรมาบ้างครับ"),
 ("A", "Paszport, zdjęcie i umowę najmu.", "phaas-pàwt rûup thàai láe sǎn-yaa châo khráp", "พาสปอร์ต รูปถ่าย และสัญญาเช่าครับ"),
 ("B", "Potrzebna też kopia.", "tâwng chái sǎm-nao dûai khráp", "ต้องใช้สำเนาด้วยครับ"),
 ("A", "Ile trwa rozpatrzenie?", "phíi-jaa-rá-naa naan thâo-rài khráp", "พิจารณานานเท่าไหร่ครับ"),
 ("B", "Około dwóch tygodni.", "prà-maan sǎwng aa-thít khráp", "ประมาณสองอาทิตย์ครับ"),
 ("A", "Czy mogę to śledzić online?", "tìt taam awn-lai dâai mǎi khráp", "ติดตามออนไลน์ได้ไหมครับ"),
 ("B", "Tak, przez aplikację.", "dâai khráp phàan áep", "ได้ครับ ผ่านแอป"),
], "„phíi-jaa-rá-naa” to słowo wyłącznie urzędowe. W rozmowie prywatnej nikt go nie używa."),

("Rozmowa o pensji", "Praca i nauka", "B1", "Kandydat", "Rekruter", [
 ("A", "Chciałbym omówić wynagrodzenie.", "phǒm yàak khui rûeang ngoen duean khráp", "ผมอยากคุยเรื่องเงินเดือนครับ"),
 ("B", "Proszę podać oczekiwania.", "khǎw sâap thîi khâat wái khráp", "ขอทราบที่คาดไว้ครับ"),
 ("A", "Mam pięcioletnie doświadczenie.", "phǒm mii prà-sòp-kaan hâa pii khráp", "ผมมีประสบการณ์ห้าปีครับ"),
 ("B", "Rozumiem. A godziny pracy panu odpowiadają?", "khâo-jai khráp wee-laa tham ngaan sà-dùak mǎi khráp", "เข้าใจครับ เวลาทำงานสะดวกไหมครับ"),
 ("A", "Tak, ale wolałbym dwa dni zdalnie.", "sà-dùak khráp tàae khǎw tham thîi bâan sǎwng wan", "สะดวกครับ แต่ขอทำที่บ้านสองวัน"),
 ("B", "To jest do ustalenia.", "rûeang níi khui kan dâai khráp", "เรื่องนี้คุยกันได้ครับ"),
 ("A", "Czy jest możliwość podwyżki?", "mii oo-kàat khûen ngoen duean mǎi khráp", "มีโอกาสขึ้นเงินเดือนไหมครับ"),
 ("B", "Raz w roku, po ocenie.", "pii lá khráng lǎng prà-mòoen phǒn khráp", "ปีละครั้ง หลังประเมินผลครับ"),
], "Rozmowa o pieniądzach jest w Tajlandii możliwa, ale prowadzi się ją spokojnie i pośrednio."),

("Prośba o urlop", "Praca i nauka", "B1", "Pracownik", "Kierownik", [
 ("A", "Chciałbym wziąć urlop.", "phǒm yàak lǎa phák ráwn khráp", "ผมอยากลาพักร้อนครับ"),
 ("B", "Od kiedy?", "tâng tàae wan nǎi khráp", "ตั้งแต่วันไหนครับ"),
 ("A", "Od poniedziałku, na pięć dni.", "tâng tàae wan jan hâa wan khráp", "ตั้งแต่วันจันทร์ห้าวันครับ"),
 ("B", "Kto przejmie twoje zadania?", "khrai jà duu ngaan thǎen khráp", "ใครจะดูงานแทนครับ"),
 ("A", "Przekażę to koledze.", "dǐao sòng tàw hâi phûean khráp", "เดี๋ยวส่งต่อให้เพื่อนครับ"),
 ("B", "Dobrze. Prześlij wniosek.", "dâai khráp sòng bai lǎa maa dûai", "ได้ครับ ส่งใบลามาด้วย"),
 ("A", "Zrobię to dzisiaj.", "wan níi tham hâi loei khráp", "วันนี้ทำให้เลยครับ"),
 ("B", "Odpocznij dobrze.", "phák phàwn hâi tem thîi khráp", "พักผ่อนให้เต็มที่ครับ"),
], "„thǎen” znaczy „w zastępstwie”. Bez tego słowa pytanie brzmiałoby jak podważanie kompetencji."),

("Niezgoda na zebraniu", "Praca i nauka", "B1", "Pracownik", "Kolega", [
 ("A", "Z całym szacunkiem, nie zgadzam się.", "dûai khwaam khaw-róp phǒm mâi hěn dûai khráp", "ด้วยความเคารพผมไม่เห็นด้วยครับ"),
 ("B", "Proszę powiedzieć dlaczego.", "chûai bàwk hèet-phǒn nòi khráp", "ช่วยบอกเหตุผลหน่อยครับ"),
 ("A", "Termin jest zbyt krótki.", "wee-laa sân koen pai khráp", "เวลาสั้นเกินไปครับ"),
 ("B", "Przyznaję, że rzeczywiście jest krótki.", "phǒm yawm ráp wâa man sân jing khráp", "ผมยอมรับว่ามันสั้นจริงครับ"),
 ("A", "Proponuję przesunąć o tydzień.", "phǒm khǎw sà-nǒoe lûean ìik nùeng aa-thít khráp", "ผมขอเสนอเลื่อนอีกหนึ่งอาทิตย์ครับ"),
 ("B", "To brzmi rozsądnie.", "fang duu mii hèet-phǒn khráp", "ฟังดูมีเหตุผลครับ"),
 ("A", "Dziękuję za wysłuchanie.", "khàwp-khun thîi fang khráp", "ขอบคุณที่ฟังครับ"),
 ("B", "Zapiszę to w ustaleniach.", "dǐao jòt long nai sà-rùp khráp", "เดี๋ยวจดลงในสรุปครับ"),
], "„dûai khwaam khaw-róp” otwiera sprzeciw wobec osoby wyższej rangą. Bez tej ramy uwaga brzmiałaby zuchwale."),

("Opowieść o pierwszym dniu w pracy", "Praca i nauka", "B1", "Znajomy", "Znajoma", [
 ("A", "Pamiętasz swój pierwszy dzień w pracy?", "jam wan râek thîi tham ngaan dâai mǎi khráp", "จำวันแรกที่ทำงานได้ไหมครับ"),
 ("B", "Do dziś to pamiętam.", "jon thǔeng wan níi yang jam dâai khâ", "จนถึงวันนี้ยังจำได้ค่ะ"),
 ("A", "Było ciężko?", "nàk mǎi khráp", "หนักไหมครับ"),
 ("B", "Wtedy jeszcze nic nie wiedziałam.", "tawn nán yang mâi rúu à-rai loei khâ", "ตอนนั้นยังไม่รู้อะไรเลยค่ะ"),
 ("A", "Każdemu się zdarza.", "khrai kâw pen khráp", "ใครก็เป็นครับ"),
 ("B", "Dopiero później to zrozumiałam.", "phôoeng maa khâo-jai thii lǎng khâ", "เพิ่งมาเข้าใจทีหลังค่ะ"),
 ("A", "Dużo się nauczyłaś.", "rian rúu yóe loei ná khráp", "เรียนรู้เยอะเลยนะครับ"),
 ("B", "Uczyłam się na własnych błędach.", "rian jàak khwaam phìt phlâat khǎwng tua eeng khâ", "เรียนจากความผิดพลาดของตัวเองค่ะ"),
], "„tawn nán” = wtedy, „thii lǎng” = później. Ta para porządkuje całą opowieść w czasie."),

("Rozmowa o marzeniach", "Small talk", "B1", "Znajomy", "Znajomy", [
 ("A", "Marzy mi się własny mały lokal.", "phǒm fǎn yàak mii ráan lék lék khǎwng tua eeng khráp", "ผมฝันอยากมีร้านเล็กๆ ของตัวเองครับ"),
 ("B", "Fajny pomysł. Jaki?", "khwaam-khít dii khráp bàep nǎi khráp", "ความคิดดีครับ แบบไหนครับ"),
 ("A", "Kawiarnia przy plaży.", "ráan kaa-fae rim thá-lee khráp", "ร้านกาแฟริมทะเลครับ"),
 ("B", "Kiedy chcesz to zrobić?", "jà tham mûea-rài khráp", "จะทำเมื่อไหร่ครับ"),
 ("A", "Chcę to osiągnąć w ciągu dwóch lat.", "yàak tham hâi dâai phaai nai sǎwng pii khráp", "อยากทำให้ได้ภายในสองปีครับ"),
 ("B", "Ambitnie. Nie poddawaj się.", "tâng jai dii khráp yàa yawm pháe ná", "ตั้งใจดีครับ อย่ายอมแพ้นะ"),
 ("A", "Powoli do tego dążę.", "khôi khôi tham pai khráp", "ค่อยๆ ทำไปครับ"),
 ("B", "Trzymam kciuki.", "pen kamlang jai hâi khráp", "เป็นกำลังใจให้ครับ"),
], "„pen kamlang jai hâi” dosłownie „być czyjąś siłą ducha” — tajski odpowiednik trzymania kciuków."),

("Skarga na hałas u sąsiadów", "Dom i codzienność", "B1", "Najemca", "Właściciel", [
 ("A", "Sąsiedzi są bardzo głośni.", "phûean bâan sǐang dang mâak khráp", "เพื่อนบ้านเสียงดังมากครับ"),
 ("B", "Od kiedy tak jest?", "pen maa naan rǔe yang khráp", "เป็นมานานหรือยังครับ"),
 ("A", "Od tygodnia, każdej nocy.", "nùeng aa-thít láew thúk khuen khráp", "หนึ่งอาทิตย์แล้ว ทุกคืนครับ"),
 ("B", "Rozmawiał pan z nimi?", "khoei khui kàp khǎo mǎi khráp", "เคยคุยกับเขาไหมครับ"),
 ("A", "Nie chcę się kłócić.", "phǒm mâi yàak thá-ló khráp", "ผมไม่อยากทะเลาะครับ"),
 ("B", "Rozumiem. Porozmawiam z nimi.", "khâo-jai khráp dǐao khui hâi", "เข้าใจครับ เดี๋ยวคุยให้"),
 ("A", "Dziękuję bardzo.", "khàwp-khun mâak khráp", "ขอบคุณมากครับ"),
 ("B", "Dam znać, jak się uda.", "dǐao bàwk phǒn ìik thii khráp", "เดี๋ยวบอกผลอีกทีครับ"),
], "Unikanie bezpośredniej konfrontacji i proszenie o pośrednictwo to w Tajlandii norma, nie unik."),

("Zgłoszenie zgubionego dokumentu", "Awarie i pomoc", "B1", "Obcokrajowiec", "Policjant", [
 ("A", "Zgubiłem dokument.", "phǒm tham èek-kà-sǎan hǎai khráp", "ผมทำเอกสารหายครับ"),
 ("B", "Jaki dokument?", "èek-kà-sǎan à-rai khráp", "เอกสารอะไรครับ"),
 ("A", "Prawo jazdy.", "bai khàp khìi khráp", "ใบขับขี่ครับ"),
 ("B", "Gdzie i kiedy?", "hǎai thîi nǎi mûea-rài khráp", "หายที่ไหนเมื่อไหร่ครับ"),
 ("A", "Chyba wczoraj na targu.", "khong mûea waan thîi tà-làat khráp", "คงเมื่อวานที่ตลาดครับ"),
 ("B", "Wystawię zaświadczenie.", "dǐao àwk bai jâeng khwaam hâi khráp", "เดี๋ยวออกใบแจ้งความให้ครับ"),
 ("A", "Ile to kosztuje?", "mii khâa chái jàai mǎi khráp", "มีค่าใช้จ่ายไหมครับ"),
 ("B", "Bez opłat.", "mâi mii khráp", "ไม่มีครับ"),
 ("A", "Dziękuję za pomoc.", "khàwp-khun thîi chûai khráp", "ขอบคุณที่ช่วยครับ"),
 ("B", "Proszę uważać na siebie.", "duu-lae tua eeng dûai ná khráp", "ดูแลตัวเองด้วยนะครับ"),
], "„bai jâeng khwaam” to policyjne zaświadczenie o zgłoszeniu. Bywa wymagane przez ubezpieczyciela."),
]
