# -*- coding: utf-8 -*-
"""Dialogi etapu 5 (B2) — czesc A.

Zakres: negocjowanie, rozwiazywanie konfliktow, rozmowy zawodowe, obsluga
klienta, wyjasnianie procedur, argumentowanie i wyrazanie watpliwosci.

Krotka: (tytul, sytuacja, poziom, rola A, rola B, kwestie, notatka)
Kwestia: (rola, polski, fonetyka, tajski)
"""

DIALOGUES_B2_A = [

("Negocjacje ceny przy większym zamówieniu", "Zakupy i pieniądze", "B2", "Kupujący", "Sprzedawca", [
 ("A", "Chciałbym omówić warunki przy większym zamówieniu.", "phǒm khǎw khui rûeang ngûean-khǎi thâa sàng jam-nuan mâak khráp", "ผมขอคุยเรื่องเงื่อนไขถ้าสั่งจำนวนมากครับ"),
 ("B", "Proszę bardzo. Ile sztuk pan rozważa?", "chooen khráp khít wái kìi chín khráp", "เชิญครับ คิดไว้กี่ชิ้นครับ"),
 ("A", "Pięćdziesiąt, ale cena musi się ruszyć.", "hâa sìp chín khráp tàae raa-khaa tâwng khà-yàp", "ห้าสิบชิ้นครับ แต่ราคาต้องขยับ"),
 ("B", "Mogę zejść o pięć procent.", "lót hâi dâai hâa poe-sen khráp", "ลดให้ได้ห้าเปอร์เซ็นต์ครับ"),
 ("A", "To wciąż za mało jak na taką ilość.", "sǎm-ràp jam-nuan níi yang mâi phaw khráp", "สำหรับจำนวนนี้ยังไม่พอครับ"),
 ("B", "A co pan proponuje?", "láew khun sà-nǒoe yang-ngai khráp", "แล้วคุณเสนอยังไงครับ"),
 ("A", "Spotkajmy się w połowie drogi: dziesięć procent.", "maa khrûeng thaang kan khráp sìp poe-sen", "มาครึ่งทางกันครับ สิบเปอร์เซ็นต์"),
 ("B", "Osiem, ale transport na mój koszt.", "pàet poe-sen khráp láew phǒm àwk khâa sòng eeng", "แปดเปอร์เซ็นต์ครับ แล้วผมออกค่าส่งเอง"),
 ("A", "Umowa stoi. Poproszę to na piśmie.", "tòk long taam nán khráp khǎw pen èek-kà-sǎan dûai", "ตกลงตามนั้นครับ ขอเป็นเอกสารด้วย"),
], "Tajski schemat targowania: nigdy nie odrzuca się oferty wprost. „yang mâi phaw” („to wciąż za mało”) jest mocne, ale nie obraża."),

("Reklamacja towaru u kierownika", "Zakupy i pieniądze", "B2", "Klient", "Kierownik", [
 ("A", "Chciałbym zgłosić reklamację.", "phǒm yàak yûen rûeang rawng rian khráp", "ผมอยากยื่นเรื่องร้องเรียนครับ"),
 ("B", "Proszę mi opisać problem.", "chûai lâo pan-hǎa hâi fang nòi khráp", "ช่วยเล่าปัญหาให้ฟังหน่อยครับ"),
 ("A", "Sprzęt przestał działać po trzech dniach.", "khrûeng chái mâi dâai lǎng jàak sǎam wan khráp", "เครื่องใช้ไม่ได้หลังจากสามวันครับ"),
 ("B", "Ma pan paragon?", "mii bai-sèt mǎi khráp", "มีใบเสร็จไหมครับ"),
 ("A", "Tak, i zdjęcie z dnia zakupu.", "mii khráp phráwm rûup wan thîi súe", "มีครับ พร้อมรูปวันที่ซื้อ"),
 ("B", "Mamy dwa rozwiązania: wymiana albo zwrot.", "mii sǎwng thaang lûeak khráp plìan an mài rǔe khuen ngoen", "มีสองทางเลือกครับ เปลี่ยนอันใหม่หรือคืนเงิน"),
 ("A", "Wolę zwrot, straciłem zaufanie.", "khǎw ngoen khuen dii kwàa khráp phǒm mâi mân-jai láew", "ขอเงินคืนดีกว่าครับ ผมไม่มั่นใจแล้ว"),
 ("B", "Rozumiem. Zwrot w ciągu tygodnia.", "khâo-jai khráp khuen ngoen phaai-nai nùeng aa-thít", "เข้าใจครับ คืนเงินภายในหนึ่งอาทิตย์"),
 ("A", "Dziękuję za sprawne załatwienie.", "khàwp-khun thîi jàt kaan hâi réw khráp", "ขอบคุณที่จัดการให้เร็วครับ"),
], "„yûen rûeang rawng rian” to reklamacja formalna. Potocznie usłyszysz „khleem”, od angielskiego „claim”."),

("Spór o zakres obowiązków", "Praca i nauka", "B2", "Pracownik", "Kierownik", [
 ("A", "Muszę powiedzieć wprost: to nie leży w moim zakresie.", "khǎw bàwk trong trong khráp an níi mâi yùu nai nâa thîi phǒm", "ขอบอกตรงๆ ครับ อันนี้ไม่อยู่ในหน้าที่ผม"),
 ("B", "Rozumiem, ale nie ma kogo innego.", "khâo-jai khráp tàae mâi mii khrai tham", "เข้าใจครับ แต่ไม่มีใครทำ"),
 ("A", "Mam już pełne ręce roboty do piątku.", "ngaan phǒm nâen thǔeng wan sùk láew khráp", "งานผมแน่นถึงวันศุกร์แล้วครับ"),
 ("B", "Co możemy zrobić, żeby się dogadać?", "tham yang-ngai thǔeng jà tòk long kan dâai khráp", "ทำยังไงถึงจะตกลงกันได้ครับ"),
 ("A", "Wezmę to, jeśli przesuniemy raport.", "phǒm ráp dâai khráp thâa lûean raai-ngaan àwk pai", "ผมรับได้ครับ ถ้าเลื่อนรายงานออกไป"),
 ("B", "Zgoda. Raport w przyszłym tygodniu.", "tòk long khráp raai-ngaan aa-thít nâa", "ตกลงครับ รายงานอาทิตย์หน้า"),
 ("A", "To ustalmy to na piśmie.", "ngán khǎw jòt pen laai lák àk-sǎwn ná khráp", "งั้นขอจดเป็นลายลักษณ์อักษรนะครับ"),
 ("B", "Dobrze, wyślę podsumowanie.", "dâai khráp dǐao sòng sà-rùp hâi", "ได้ครับ เดี๋ยวส่งสรุปให้"),
], "Odmowa wobec przełożonego wymaga propozycji wymiany, nie samego „nie”. Bez „thâa …” zdanie byłoby konfrontacją."),

("Rozmowa o podwyżce", "Praca i nauka", "B2", "Pracownik", "Szef", [
 ("A", "Czy mógłbym prosić o chwilę pańskiego czasu?", "khǎw rop-kuan wee-laa khǎwng khun sák khrûu dâai mǎi khráp", "ขอรบกวนเวลาของคุณสักครู่ได้ไหมครับ"),
 ("B", "Oczywiście, siadaj.", "dâai loei khráp chooen nâng", "ได้เลยครับ เชิญนั่ง"),
 ("A", "Chciałbym porozmawiać o pensji.", "phǒm khǎw khui rûeang ngoen duean khráp", "ผมขอคุยเรื่องเงินเดือนครับ"),
 ("B", "Słucham. Na jakiej podstawie?", "fang yùu khráp ing jàak à-rai khráp", "ฟังอยู่ครับ อิงจากอะไรครับ"),
 ("A", "Po pierwsze, przejąłem dwa projekty.", "yàang râek phǒm ráp chûang tàw sǎwng khroong-kaan khráp", "อย่างแรกผมรับช่วงต่อสองโครงการครับ"),
 ("B", "To prawda, doceniam to.", "jing khráp phǒm hěn khwaam tâng-jai", "จริงครับ ผมเห็นความตั้งใจ"),
 ("A", "Po drugie, klient wrócił dzięki tej pracy.", "yàang thîi sǎwng lûuk kháa klàp maa phráw ngaan níi khráp", "อย่างที่สองลูกค้ากลับมาเพราะงานนี้ครับ"),
 ("B", "Nie mogę tego obiecać dziś.", "wan níi phǒm rap paak mâi dâai khráp", "วันนี้ผมรับปากไม่ได้ครับ"),
 ("A", "Rozumiem. Kiedy dostanę odpowiedź?", "khâo-jai khráp jà dâai kham tàwp mûea rài", "เข้าใจครับ จะได้คำตอบเมื่อไหร่"),
 ("B", "Do końca miesiąca, obiecuję.", "phaai-nai sîn duean khráp sǎn-yaa", "ภายในสิ้นเดือนครับ สัญญา"),
], "Argumentacja „yàang râek … yàang thîi sǎwng …” porządkuje wywód i brzmi profesjonalnie. Nacisk na termin odpowiedzi jest tu kluczowy."),

("Wyjaśnianie opóźnienia klientowi", "Praca i nauka", "B2", "Obsługa", "Klient", [
 ("A", "Dzwonię w sprawie pańskiego zamówienia.", "thoo maa rûeang kaan sàng súe khǎwng khun khráp", "โทรมาเรื่องการสั่งซื้อของคุณครับ"),
 ("B", "Miało być wczoraj.", "tham-mai mâi maa mûea waan khráp", "ทำไมไม่มาเมื่อวานครับ"),
 ("A", "Uprzejmie informuję o opóźnieniu dwóch dni.", "khǎw riian jâeng wâa mii khwaam lâa cháa sǎwng wan khráp", "ขอเรียนแจ้งว่ามีความล่าช้าสองวันครับ"),
 ("B", "To dla mnie problem, mam termin.", "an níi pen pan-hǎa khráp phǒm mii kam-nòt", "อันนี้เป็นปัญหาครับ ผมมีกำหนด"),
 ("A", "Rozumiem pana frustrację.", "phǒm khâo-jai khwaam rúu-sùek khǎwng khun khráp", "ผมเข้าใจความรู้สึกของคุณครับ"),
 ("B", "Co możecie z tym zrobić?", "láew jà tham yang-ngai tàw khráp", "แล้วจะทำยังไงต่อครับ"),
 ("A", "Wyślemy kurierem na nasz koszt.", "jà sòng dûai khoe-ri-ôoe doi raw àwk khâa sòng khráp", "จะส่งด้วยเคอรี่เออร์โดยเราออกค่าส่งครับ"),
 ("B", "Dobrze, ale to ostatni raz.", "dâai khráp tàae khráng níi khráng dìao", "ได้ครับ แต่ครั้งนี้ครั้งเดียว"),
 ("A", "Przepraszam za niedogodności.", "khǎw à-phai nai khwaam mâi sà-dùak khráp", "ขออภัยในความไม่สะดวกครับ"),
], "Kolejność w obsłudze klienta: informacja, uznanie emocji, rozwiązanie, przeprosiny. Odwrócenie jej brzmi jak wykręt."),

("Wyjaśnianie procedury w urzędzie", "Praca i nauka", "B2", "Urzędnik", "Interesant", [
 ("A", "Wyjaśnię krok po kroku.", "phǒm jà à-thí-baai pen khân tawn khráp", "ผมจะอธิบายเป็นขั้นตอนครับ"),
 ("B", "Proszę, notuję.", "chooen khráp phǒm kam-lang jòt", "เชิญครับ ผมกำลังจด"),
 ("A", "Najpierw trzeba złożyć wniosek.", "khân râek tâwng yûen khâm rǎwng kàwn khráp", "ขั้นแรกต้องยื่นคำร้องก่อนครับ"),
 ("B", "Jakich dokumentów potrzeba?", "tâwng chái èek-kà-sǎan à-rai bâang khráp", "ต้องใช้เอกสารอะไรบ้างครับ"),
 ("A", "Paszportu, zaświadczenia i dwóch zdjęć.", "nǎng-sǔe doen thaang bai rap-rawng láe rûup sǎwng bai khráp", "หนังสือเดินทาง ใบรับรอง และรูปสองใบครับ"),
 ("B", "Czy kopia wystarczy?", "chái sǎm-nao dâai mǎi khráp", "ใช้สำเนาได้ไหมครับ"),
 ("A", "Kopia z podpisem na każdej stronie.", "sǎm-nao tâwng sen chûe thúk nâa khráp", "สำเนาต้องเซ็นชื่อทุกหน้าครับ"),
 ("B", "Ile to trwa?", "chái wee-laa naan thâo-rài khráp", "ใช้เวลานานเท่าไหร่ครับ"),
 ("A", "Zwykle trzy dni robocze.", "pòk-kà-tì sǎam wan tham-kaan khráp", "ปกติสามวันทำการครับ"),
 ("B", "Czy dobrze rozumiem: odbiór osobisty?", "phǒm khâo-jai thùuk mǎi khráp maa ráp dûai tua eeng", "ผมเข้าใจถูกไหมครับ มารับด้วยตัวเอง"),
 ("A", "Zgadza się, z tym pokwitowaniem.", "thùuk tâwng khráp ao bai ráp maa dûai", "ถูกต้องครับ เอาใบรับมาด้วย"),
], "„wan tham-kaan” to dzień roboczy — bez tego słowa urzędnik policzy również weekend."),

("Konflikt o hałas z sąsiadem", "Dom i codzienność", "B2", "Lokator", "Sąsiad", [
 ("A", "Przepraszam, że przeszkadzam.", "khǎw-thôot thîi róp-kuan khráp", "ขอโทษที่รบกวนครับ"),
 ("B", "Nie szkodzi, o co chodzi?", "mâi pen rai khráp mii à-rai rǔe plào", "ไม่เป็นไรครับ มีอะไรหรือเปล่า"),
 ("A", "Czuję się niekomfortowo z tym mówić, ale wieczorami jest głośno.", "phǒm rúu-sùek mâi sà-baai jai thîi jà phûut tàae tawn yen sǐang dang khráp", "ผมรู้สึกไม่สบายใจที่จะพูด แต่ตอนเย็นเสียงดังครับ"),
 ("B", "Nie wiedziałem, że słychać.", "phǒm mâi rúu wâa dâi yin khráp", "ผมไม่รู้ว่าได้ยินครับ"),
 ("A", "Ściany są cienkie, słychać przez podłogę.", "fǎa baang khráp dâi yin thá-lú phúen", "ฝาบางครับ ได้ยินทะลุพื้น"),
 ("B", "Przepraszam, ściszę po dziesiątej.", "khǎw-thôot khráp lǎng sìi thûm jà bao sǐang long", "ขอโทษครับ หลังสี่ทุ่มจะเบาเสียงลง"),
 ("A", "Dziękuję, nie robię z tego problemu.", "khàwp-khun khráp phǒm mâi dâai tham hâi pen rûeang yài", "ขอบคุณครับ ผมไม่ได้ทำให้เป็นเรื่องใหญ่"),
 ("B", "Dobrze, że pan powiedział.", "dii láew thîi bàwk khráp", "ดีแล้วที่บอกครับ"),
], "Skarga zaczyna się od przeprosin i mówienia o własnym odczuciu, nie o cudzej winie. To zdejmuje z sąsiada zagrożenie utraty twarzy."),

("Przeprosiny za błąd w raporcie", "Praca i nauka", "B2", "Pracownik", "Kierownik", [
 ("A", "Muszę zgłosić błąd w raporcie.", "phǒm khǎw riian jâeng khâw phìt phlâat nai raai-ngaan khráp", "ผมขอเรียนแจ้งข้อผิดพลาดในรายงานครับ"),
 ("B", "Gdzie dokładnie?", "trong nǎi khráp", "ตรงไหนครับ"),
 ("A", "W tabeli kosztów, pomyliłem liczby.", "nai taa-raang khâa chái jàai phǒm khít tua lêek phìt khráp", "ในตารางค่าใช้จ่าย ผมคิดตัวเลขผิดครับ"),
 ("B", "Klient to widział?", "lûuk kháa hěn láew rǔe yang khráp", "ลูกค้าเห็นแล้วหรือยังครับ"),
 ("A", "Jeszcze nie, zatrzymałem wysyłkę.", "yang khráp phǒm yút kaan sòng wái", "ยังครับ ผมหยุดการส่งไว้"),
 ("B", "Dobrze, że od razu powiedziałeś.", "dii láew thîi bàwk than-thii khráp", "ดีแล้วที่บอกทันทีครับ"),
 ("A", "To moja wina, poprawię do wieczora.", "pen khwaam phìt khǎwng phǒm khráp jà kâe hâi tawn yen", "เป็นความผิดของผมครับ จะแก้ให้ตอนเย็น"),
 ("B", "Wyciągnijmy z tego wnioski na przyszłość.", "thàwt bòt rian wái sǎm-ràp khráng nâa khráp", "ถอดบทเรียนไว้สำหรับครั้งหน้าครับ"),
], "Zgłoszenie błędu zanim wyjdzie na jaw ratuje twarz obu stronom. „thàwt bòt rian” to zwrot z języka zarządzania."),

("Argument za zmianą dostawcy", "Praca i nauka", "B2", "Analityk", "Dyrektor", [
 ("A", "Mogę coś dodać do tego punktu?", "khǎw sòoem rûeang níi nòi dâai mǎi khráp", "ขอเสริมเรื่องนี้หน่อยได้ไหมครับ"),
 ("B", "Proszę.", "chooen khráp", "เชิญครับ"),
 ("A", "Liczby mówią same za siebie: koszt wzrósł o jedną piątą.", "tua lêek fâwng yùu láew khráp tôn thun khûen nùeng nai hâa", "ตัวเลขฟ้องอยู่แล้วครับ ต้นทุนขึ้นหนึ่งในห้า"),
 ("B", "Skąd te dane?", "khâw-muun níi maa jàak nǎi khráp", "ข้อมูลนี้มาจากไหนครับ"),
 ("A", "Z faktur za ostatnie pół roku.", "jàak bai kam-kàp phaa-sǐi khrûeng pii thîi phàan maa khráp", "จากใบกำกับภาษีครึ่งปีที่ผ่านมาครับ"),
 ("B", "Zgadzam się co do zasady, ale zmiana też kosztuje.", "lák kaan phǒm hěn dûai khráp tàae kaan plìan kâw mii tôn thun", "หลักการผมเห็นด้วยครับ แต่การเปลี่ยนก็มีต้นทุน"),
 ("A", "Racja, nie pomyślałem o tym.", "khun phûut thùuk khráp phǒm khít mâi thǔeng", "คุณพูดถูกครับ ผมคิดไม่ถึง"),
 ("B", "Policzmy oba warianty i wróćmy do tego.", "lawng pìap thîap sǎwng bàep láew khui tàw khráp", "ลองเปรียบเทียบสองแบบแล้วคุยต่อครับ"),
], "Przyznanie racji rozmówcy („khun phûut thùuk khráp”) wzmacnia twoją pozycję, zamiast ją osłabiać."),

("Rozmowa o warunkach umowy najmu", "Dom i codzienność", "B2", "Najemca", "Właściciel", [
 ("A", "Chciałbym przeczytać umowę przed podpisaniem.", "khǎw àan sǎn-yaa kàwn sen khráp", "ขออ่านสัญญาก่อนเซ็นครับ"),
 ("B", "Proszę, standardowa umowa roczna.", "chooen khráp sǎn-yaa raai pii bàep mâat-trà-thǎan", "เชิญครับ สัญญารายปีแบบมาตรฐาน"),
 ("A", "Ile wynosi kaucja i kiedy wraca?", "khâa mát jam thâo-rài láe khuen mûea rài khráp", "ค่ามัดจำเท่าไหร่และคืนเมื่อไหร่ครับ"),
 ("B", "Dwa czynsze, zwrot po trzydziestu dniach.", "sǎwng duean khráp khuen phaai-nai sǎam sìp wan", "สองเดือนครับ คืนภายในสามสิบวัน"),
 ("A", "Kto płaci za naprawy klimatyzacji?", "khâa sâwm aae khrai àwk khráp", "ค่าซ่อมแอร์ใครออกครับ"),
 ("B", "Właściciel, jeśli to zwykłe zużycie.", "jâo khǎwng àwk khráp thâa chái ngaan pòk-kà-tì", "เจ้าของออกครับ ถ้าใช้งานปกติ"),
 ("A", "Proszę o protokół stanu ze zdjęciami.", "khǎw bai trùat sà-phâap hâwng phráwm rûup thàai khráp", "ขอใบตรวจสภาพห้องพร้อมรูปถ่ายครับ"),
 ("B", "Zrobimy to razem przy odbiorze kluczy.", "tham dûai kan tawn ráp kun-jae khráp", "ทำด้วยกันตอนรับกุญแจครับ"),
 ("A", "Czy czynsz podlega negocjacji przy dwóch latach?", "sǎn-yaa sǎwng pii khâa châo tàw rawng dâai mǎi khráp", "สัญญาสองปีค่าเช่าต่อรองได้ไหมครับ"),
 ("B", "Mogę zejść o pięćset przy dwuletniej.", "lót hâi hâa ráwi thâa sǎn-yaa sǎwng pii khráp", "ลดให้ห้าร้อยถ้าสัญญาสองปีครับ"),
], "Spisanie stanu mieszkania ze zdjęciami to najskuteczniejsza ochrona kaucji. Poproś o to zawsze przed podpisem."),

("Wątpliwości wobec zbyt dobrej oferty", "Zakupy i pieniądze", "B2", "Klient", "Pośrednik", [
 ("A", "Brzmi to zbyt pięknie.", "man dii koen jing pai nòi khráp", "มันดีเกินจริงไปหน่อยครับ"),
 ("B", "Dlaczego pan tak sądzi?", "tham-mai khít yàang nán khráp", "ทำไมคิดอย่างนั้นครับ"),
 ("A", "Cena jest o połowę niższa niż wszędzie.", "raa-khaa thùuk kwàa thîi ùen khrûeng nùeng khráp", "ราคาถูกกว่าที่อื่นครึ่งหนึ่งครับ"),
 ("B", "Bo to bezpośrednio od właściciela.", "phráw pen khǎwng jâo khǎwng doi trong khráp", "เพราะเป็นของเจ้าของโดยตรงครับ"),
 ("A", "Kto to gwarantuje?", "khrai pen khon káan-tii khráp", "ใครเป็นคนการันตีครับ"),
 ("B", "Firma, mamy licencję.", "bɔɔ-rí-sàt khráp raw mii bai à-nú-yâat", "บริษัทครับ เรามีใบอนุญาต"),
 ("A", "Chcę zobaczyć to na własne oczy przed zapłatą.", "khǎw duu kàp taa kàwn jàai khráp", "ขอดูกับตาก่อนจ่ายครับ"),
 ("B", "Oczywiście, jutro po południu.", "dâai loei khráp phrûng-níi bàai", "ได้เลยครับ พรุ่งนี้บ่าย"),
 ("A", "I proszę o wszystko na piśmie.", "láew khǎw thúk yàang pen èek-kà-sǎan dûai khráp", "แล้วขอทุกอย่างเป็นเอกสารด้วยครับ"),
], "„khǎw duu kàp taa kàwn jàai” to zdanie warte zapamiętania w całości — chroni przed najczęstszym typem oszustwa."),

("Trudna informacja dla zespołu", "Praca i nauka", "B2", "Kierownik", "Pracownik", [
 ("A", "Mam do przekazania trudną wiadomość.", "mii rûeang mâi khâwi dii jà bàwk khráp", "มีเรื่องไม่ค่อยดีจะบอกครับ"),
 ("B", "Słucham uważnie.", "fang yùu khráp", "ฟังอยู่ครับ"),
 ("A", "Projekt zostaje wstrzymany na trzy miesiące.", "khroong-kaan thùuk yút wái sǎam duean khráp", "โครงการถูกหยุดไว้สามเดือนครับ"),
 ("B", "A co z naszą pracą?", "láew ngaan khǎwng raw lâ khráp", "แล้วงานของเราล่ะครับ"),
 ("A", "Nikt nie traci pracy, przechodzimy do innego zadania.", "mâi mii khrai tòk ngaan khráp yáai pai ngaan ùen", "ไม่มีใครตกงานครับ ย้ายไปงานอื่น"),
 ("B", "To ulga. Kiedy zaczynamy?", "khôi yang chûa khráp rôoem mûea rài", "ค่อยยังชั่วครับ เริ่มเมื่อไหร่"),
 ("A", "Od poniedziałku, szczegóły wyślę dziś.", "wan jan khráp rai-lá-ìat jà sòng wan níi", "วันจันทร์ครับ รายละเอียดจะส่งวันนี้"),
 ("B", "Dziękuję, że powiedziałeś wprost.", "khàwp-khun thîi bàwk trong trong khráp", "ขอบคุณที่บอกตรงๆ ครับ"),
], "Złą wiadomość podaje się z zapowiedzią i od razu z tym, co ona oznacza dla słuchacza. Bez tego rozmówca usłyszy tylko zagrożenie."),

("Prośba o przesunięcie terminu płatności", "Zakupy i pieniądze", "B2", "Klient", "Księgowa", [
 ("A", "Zwracam się z prośbą o przesunięcie terminu.", "khǎw khwaam kà-rú-naa lûean kam-nòt àwk pai khráp", "ขอความกรุณาเลื่อนกำหนดออกไปครับ"),
 ("B", "O ile dokładnie?", "lûean kìi wan khráp", "เลื่อนกี่วันครับ"),
 ("A", "O dwa tygodnie, przelew z zagranicy się opóźnia.", "sǎwng aa-thít khráp ngoen oon jàak tàang prà-thêet cháa", "สองอาทิตย์ครับ เงินโอนจากต่างประเทศช้า"),
 ("B", "Czy to się powtórzy?", "man jà pen ìik mǎi khráp", "มันจะเป็นอีกไหมครับ"),
 ("A", "Nie sądzę, zmieniam bank.", "mâi nâa khráp phǒm kam-lang plìan thá-naa-khaan", "ไม่น่าครับ ผมกำลังเปลี่ยนธนาคาร"),
 ("B", "Dobrze, ale proszę o to na piśmie.", "dâai khráp tàae khǎw pen laai lák àk-sǎwn", "ได้ครับ แต่ขอเป็นลายลักษณ์อักษร"),
 ("A", "Wyślę dziś wieczorem.", "jà sòng tawn yen níi khráp", "จะส่งตอนเย็นนี้ครับ"),
 ("B", "Dziękuję za wcześniejsze zgłoszenie.", "khàwp-khun thîi jâeng lûang nâa khráp", "ขอบคุณที่แจ้งล่วงหน้าครับ"),
], "Prośba o odroczenie działa tylko z terminem i powodem. „lûang nâa” — z wyprzedzeniem — jest tu słowem kluczowym."),

("Rozmowa o wynikach badania", "Zdrowie", "B2", "Pacjent", "Lekarz", [
 ("A", "Chciałbym omówić wyniki.", "phǒm khǎw khui rûeang phǒn trùat khráp", "ผมขอคุยเรื่องผลตรวจครับ"),
 ("B", "Proszę, wszystko w normie poza jednym.", "chooen khráp pòk-kà-tì thúk yàang yók wén nùeng khâw", "เชิญครับ ปกติทุกอย่างยกเว้นหนึ่งข้อ"),
 ("A", "Co dokładnie ma pan na myśli?", "mǎai thǔeng à-rai kan nâe khráp", "หมายถึงอะไรกันแน่ครับ"),
 ("B", "Poziom żelaza jest niski.", "rá-dàp thâat lèk tàm khráp", "ระดับธาตุเหล็กต่ำครับ"),
 ("A", "Czy to poważne?", "an níi nàk mǎi khráp", "อันนี้หนักไหมครับ"),
 ("B", "Nie, ale trzeba to kontrolować.", "mâi nàk khráp tàae tâwng taam duu", "ไม่หนักครับ แต่ต้องตามดู"),
 ("A", "Czy ten lek jest refundowany?", "yaa tua níi prà-kan khrâwp khlum mǎi khráp", "ยาตัวนี้ประกันครอบคลุมไหมครับ"),
 ("B", "Nie, ale kosztuje niewiele.", "mâi khrâwp khlum khráp tàae raa-khaa mâi phaeng", "ไม่ครอบคลุมครับ แต่ราคาไม่แพง"),
 ("A", "Proszę o dokumentację do ubezpieczyciela.", "khǎw èek-kà-sǎan sǎm-ràp khleem prà-kan khráp", "ขอเอกสารสำหรับเคลมประกันครับ"),
 ("B", "Wydamy przy kasie.", "ráp dâai thîi châwng châm-rá ngoen khráp", "รับได้ที่ช่องชำระเงินครับ"),
], "Pytanie „mǎai thǔeng à-rai kan nâe” wymusza precyzję. W rozmowie medycznej to ważniejsze niż uprzejmość."),

("Uzgodnienie zakresu prac remontowych", "Dom i codzienność", "B2", "Właściciel mieszkania", "Wykonawca", [
 ("A", "Proszę o wycenę przed rozpoczęciem.", "khǎw prà-mâan raa-khaa kàwn rôoem khráp", "ขอประมาณราคาก่อนเริ่มครับ"),
 ("B", "Około dwudziestu tysięcy, bez materiałów.", "prà-maan sǎwng mùen mâi ruam wát-sà-dù khráp", "ประมาณสองหมื่น ไม่รวมวัสดุครับ"),
 ("A", "Cena zawiera wszystko czy dojdą dopłaty?", "raa-khaa níi ruam thúk yàang rǔe tâwng bùak ìik khráp", "ราคานี้รวมทุกอย่างหรือต้องบวกอีกครับ"),
 ("B", "Wywóz gruzu osobno.", "khâa khǒn khà-yà kàw sâang khít yâek khráp", "ค่าขนขยะก่อสร้างคิดแยกครับ"),
 ("A", "Ile potrwają prace?", "chái wee-laa kìi wan khráp", "ใช้เวลากี่วันครับ"),
 ("B", "Pięć dni, jeśli nie będzie deszczu.", "hâa wan khráp thâa fǒn mâi tòk", "ห้าวันครับ ถ้าฝนไม่ตก"),
 ("A", "Co się stanie, jeśli się nie uda w terminie?", "thâa mâi sèt taam kam-nòt jà tham yang-ngai khráp", "ถ้าไม่เสร็จตามกำหนดจะทำยังไงครับ"),
 ("B", "Dokończymy bez dopłaty za robociznę.", "tham tàw hâi doi mâi khít khâa raeng phôoem khráp", "ทำต่อให้โดยไม่คิดค่าแรงเพิ่มครับ"),
 ("A", "Ustalmy to na piśmie.", "khǎw jòt pen laai lák àk-sǎwn ná khráp", "ขอจดเป็นลายลักษณ์อักษรนะครับ"),
], "Pytanie „co się stanie, jeśli się nie uda” zadaj przed pracami, nie po. To zdanie ratuje najwięcej sporów."),

("Rozmowa kwalifikacyjna po tajsku", "Praca i nauka", "B2", "Kandydat", "Rekruter", [
 ("A", "Pozwolą państwo, że się przedstawię.", "khǎw à-nú-yâat náe-nam tua khráp", "ขออนุญาตแนะนำตัวครับ"),
 ("B", "Proszę bardzo.", "chooen khráp", "เชิญครับ"),
 ("A", "Mam pięć lat doświadczenia w obsłudze klienta.", "phǒm mii prà-sòp-kaan dâan brí-kaan lûuk kháa hâa pii khráp", "ผมมีประสบการณ์ด้านบริการลูกค้าห้าปีครับ"),
 ("B", "Dlaczego chce pan zmienić pracę?", "tham-mai yàak plìan ngaan khráp", "ทำไมอยากเปลี่ยนงานครับ"),
 ("A", "Szukam pracy z większą odpowiedzialnością.", "phǒm hǎa ngaan thîi mii khwaam ráp phìt châwp mâak khûen khráp", "ผมหางานที่มีความรับผิดชอบมากขึ้นครับ"),
 ("B", "Jak radzi pan sobie pod presją?", "thùuk kòt dan láew tham yang-ngai khráp", "ถูกกดดันแล้วทำยังไงครับ"),
 ("A", "Ustalam priorytety i informuję zespół.", "phǒm riang lam-dàp khwaam sǎm-khan láew jâeng thiim khráp", "ผมเรียงลำดับความสำคัญแล้วแจ้งทีมครับ"),
 ("B", "Jakie ma pan oczekiwania finansowe?", "khaat wǎng ngoen duean thâo-rài khráp", "คาดหวังเงินเดือนเท่าไหร่ครับ"),
 ("A", "Otwarty jestem na rozmowę o widełkach.", "rûeang ngoen duean khui kan dâai khráp", "เรื่องเงินเดือนคุยกันได้ครับ"),
 ("B", "Odezwiemy się w tym tygodniu.", "jà tìt tàw klàp phaai-nai aa-thít níi khráp", "จะติดต่อกลับภายในอาทิตย์นี้ครับ"),
], "Na rozmowie kwalifikacyjnej „khǎw à-nú-yâat” otwiera każdą wypowiedź. Deklaracja otwartości na negocjację brzmi lepiej niż podanie kwoty."),

("Zgłoszenie podejrzanej transakcji", "Zakupy i pieniądze", "B2", "Klient", "Pracownik banku", [
 ("A", "Chcę zgłosić podejrzaną transakcję.", "phǒm yàak jâeng raai kaan thîi nâa sǒng-sǎi khráp", "ผมอยากแจ้งรายการที่น่าสงสัยครับ"),
 ("B", "Kiedy się pojawiła?", "kòet khûen mûea rài khráp", "เกิดขึ้นเมื่อไหร่ครับ"),
 ("A", "Wczoraj około drugiej po południu.", "mûea waan prà-maan bàai sǎwng moong khráp", "เมื่อวานประมาณบ่ายสองโมงครับ"),
 ("B", "Czy udostępnił pan komuś hasło?", "khoei hâi rá-hàt phàan kàp khrai mǎi khráp", "เคยให้รหัสผ่านกับใครไหมครับ"),
 ("A", "Nie. Ktoś podszył się pod bank przez telefon.", "mâi khráp mii khon plaawm pen thá-naa-khaan thoo maa", "ไม่ครับ มีคนปลอมเป็นธนาคารโทรมา"),
 ("B", "Proszę zablokować kartę od razu.", "khǎw à-yàt bàt than-thii ná khráp", "ขออายัดบัตรทันทีนะครับ"),
 ("A", "Proszę zablokować też konto.", "chûai à-yàt ban-chii dûai khráp", "ช่วยอายัดบัญชีด้วยครับ"),
 ("B", "Zrobione. Proszę złożyć zawiadomienie na policji.", "riap ráwi khráp chûai pai jâeng khwaam dûai", "เรียบร้อยครับ ช่วยไปแจ้งความด้วย"),
 ("A", "Proszę o kopię zgłoszenia.", "khǎw sǎm-nao bai jâeng dûai khráp", "ขอสำเนาใบแจ้งด้วยครับ"),
], "„à-yàt” to zablokowanie środków — jedno słowo, które w kryzysie ratuje pieniądze. Zapamiętaj je razem z „jâeng khwaam”."),

("Różnica zdań o terminie premiery", "Praca i nauka", "B2", "Kierownik projektu", "Handlowiec", [
 ("A", "Widzę to inaczej niż ty.", "phǒm mawng tàang jàak khun khráp", "ผมมองต่างจากคุณครับ"),
 ("B", "Mów śmiało, nie obrażę się.", "phûut trong trong dâai loei khráp phǒm mâi thǔe", "พูดตรงๆ ได้เลยครับ ผมไม่ถือ"),
 ("A", "Wypuszczenie w tym miesiącu to za duże ryzyko.", "plòi duean níi sìang koen pai khráp", "ปล่อยเดือนนี้เสี่ยงเกินไปครับ"),
 ("B", "Ale klienci czekają od pół roku.", "tàae lûuk kháa raw maa khrûeng pii láew khráp", "แต่ลูกค้ารอมาครึ่งปีแล้วครับ"),
 ("A", "To prawda tylko częściowo — czekają na działającą wersję.", "man jing baang sùan khráp khǎo raw bàep thîi chái dâai", "มันจริงบางส่วนครับ เขารอแบบที่ใช้ได้"),
 ("B", "Masz rację, nie pomyślałem o tym.", "khun phûut thùuk khráp phǒm khít mâi thǔeng", "คุณพูดถูกครับ ผมคิดไม่ถึง"),
 ("A", "Proponuję kompromis: mała grupa testowa.", "khǎw sà-nǒoe thaang saai klaang khráp lawng kàp klùm lék", "ขอเสนอทางสายกลางครับ ลองกับกลุ่มเล็ก"),
 ("B", "To ma sens. Umowa stoi.", "man mii hèet-phǒn khráp tòk long taam nán", "มันมีเหตุผลครับ ตกลงตามนั้น"),
], "„thaang saai klaang” — droga środka — to pojęcie zakorzenione w buddyjskim myśleniu i bardzo dobrze odbierane w sporze."),

("Ustalanie odpowiedzialności po awarii", "Praca i nauka", "B2", "Klient", "Serwisant", [
 ("A", "Kto za to odpowiada?", "khrai ráp phìt châwp rûeang níi khráp", "ใครรับผิดชอบเรื่องนี้ครับ"),
 ("B", "Zależy od przyczyny awarii.", "khûen yùu kàp sǎa-hèet khráp", "ขึ้นอยู่กับสาเหตุครับ"),
 ("A", "Problem polega na tym, że urządzenie było nowe.", "pan-hǎa khue wâa khrûeng phôoeng súe maa khráp", "ปัญหาคือว่าเครื่องเพิ่งซื้อมาครับ"),
 ("B", "Podejrzewam, że przyczyną jest instalacja.", "phǒm sǒng-sǎi wâa sǎa-hèet khue kaan tìt tâng khráp", "ผมสงสัยว่าสาเหตุคือการติดตั้งครับ"),
 ("A", "Instalowaliście państwo, nie ja.", "khun pen khon tìt tâng khráp mâi châi phǒm", "คุณเป็นคนติดตั้งครับ ไม่ใช่ผม"),
 ("B", "Zgadza się. Sprawdzę dokumentację.", "thùuk tâwng khráp dǐao trùat sàwp èek-kà-sǎan", "ถูกต้องครับ เดี๋ยวตรวจสอบเอกสาร"),
 ("A", "Szukam rozwiązania, nie winnego.", "phǒm hǎa thaang àwk mâi dâai hǎa khon phìt khráp", "ผมหาทางออกไม่ได้หาคนผิดครับ"),
 ("B", "Naprawimy na nasz koszt w tym tygodniu.", "raw jà sâwm hâi doi mâi khít khâa chái jàai khráp", "เราจะซ่อมให้โดยไม่คิดค่าใช้จ่ายครับ"),
 ("A", "Proszę o potwierdzenie na piśmie.", "khǎw kaan yuen-yan pen èek-kà-sǎan khráp", "ขอการยืนยันเป็นเอกสารครับ"),
], "Zdanie „szukam rozwiązania, nie winnego” obniża temperaturę rozmowy i zwykle przyspiesza ustępstwo drugiej strony."),

("Odmowa udziału w projekcie", "Praca i nauka", "B2", "Specjalista", "Kolega", [
 ("A", "Chciałem cię zaprosić do projektu.", "yàak chuan khun khâo rûam khroong-kaan khráp", "อยากชวนคุณเข้าร่วมโครงการครับ"),
 ("B", "Dziękuję, ale muszę sprawdzić kalendarz.", "khàwp-khun khráp khǎw duu taa-raang kàwn", "ขอบคุณครับ ขอดูตารางก่อน"),
 ("A", "Zaczynamy w przyszłym miesiącu.", "rôoem duean nâa khráp", "เริ่มเดือนหน้าครับ"),
 ("B", "W tym kwartale raczej nie dam rady.", "khwaa-tôoe níi khong yâak nòi khráp", "ควอเตอร์นี้คงยากหน่อยครับ"),
 ("A", "Szkoda, liczyłem na ciebie.", "sǐa daai khráp phǒm wǎng wái", "เสียดายครับ ผมหวังไว้"),
 ("B", "Nie chcę składać obietnic bez pokrycia.", "phǒm mâi yàak rap paak láew tham mâi dâai khráp", "ผมไม่อยากรับปากแล้วทำไม่ได้ครับ"),
 ("A", "Doceniam szczerość.", "khàwp-khun thîi bàwk trong trong khráp", "ขอบคุณที่บอกตรงๆ ครับ"),
 ("B", "Może innym razem, chętnie doradzę z boku.", "wái oo-kàat nâa khráp tàae chûai náe-nam dâai", "ไว้โอกาสหน้าครับ แต่ช่วยแนะนำได้"),
], "Odmowa z propozycją częściowego wsparcia zachowuje relację. Sam „nie” zamknąłby drogę do przyszłej współpracy."),
]
