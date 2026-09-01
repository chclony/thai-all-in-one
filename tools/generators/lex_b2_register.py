# -*- coding: utf-8 -*-
"""Leksyka etapu 5 (B2) — pary i trojki rejestrowe.

Sedno poziomu B2: ten sam komunikat brzmi inaczej w urzedzie, inaczej w rozmowie
z kolega, inaczej w barze. Kazdy komunikat wystepuje tu TRZY razy — w rejestrze
formalnym, neutralnym i potocznym. Pole `register` niesie te informacje maszynowo,
a `notes` opisuje ja slownie i podaje pozostale dwa warianty fonetycznie, zeby
uczacy sie widzial cala trojke przy kazdej karcie.

Zrodlo danych: MESSAGES. Rekordy w formacie zgodnym z lex_b2_core_a.py buduje
petla na dole pliku — dzieki temu notatka jest zawsze spojna.

Krotka MESSAGES:
  (opis komunikatu, kategoria, podkategoria, gdzie uzywac formalnego,
   formalny, neutralny, potoczny)
Kazdy wariant: (polski, fonetyka, tajski, przyklad_pl, przyklad_ph, przyklad_th)
"""

MESSAGES = [

("prośba o rachunek", "Restauracja", "Rejestr",
 "restauracja hotelowa i lokal z obsługą kelnerską",
 ("Poproszę o rachunek.", "khǎw bin dûai khráp", "ขอบิลด้วยครับ",
  "Poproszę o rachunek, płacę kartą.", "khǎw bin dûai khráp jàai bàt", "ขอบิลด้วยครับ จ่ายบัตร"),
 ("Poproszę rachunek.", "khǎw bin nòi khráp", "ขอบิลหน่อยครับ",
  "Poproszę rachunek, spieszę się.", "khǎw bin nòi khráp phǒm rîip", "ขอบิลหน่อยครับ ผมรีบ"),
 ("Ile płacę?", "khít tang dûai khráp", "คิดตังค์ด้วยครับ",
  "Ile płacę razem?", "khít tang ruam thâo-rài khráp", "คิดตังค์รวมเท่าไหร่ครับ")),

("prośba o powtórzenie", "Podstawy i grzeczność", "Rejestr",
 "rozmowa z urzędnikiem, lekarzem, klientem",
 ("Czy mógłbym prosić o powtórzenie?", "khǎw rop-kuan phûut ìik khráng dâai mǎi khráp", "ขอรบกวนพูดอีกครั้งได้ไหมครับ",
  "Czy mógłbym prosić o powtórzenie nazwiska?", "khǎw rop-kuan phûut naam sà-kun ìik khráng khráp", "ขอรบกวนพูดนามสกุลอีกครั้งครับ"),
 ("Możesz powtórzyć?", "phûut ìik thii dâai mǎi khráp", "พูดอีกทีได้ไหมครับ",
  "Możesz powtórzyć wolniej?", "phûut ìik thii cháa cháa dâai mǎi khráp", "พูดอีกทีช้าๆ ได้ไหมครับ"),
 ("Co? Jeszcze raz.", "à-rai ná ìik thii", "อะไรนะ อีกที",
  "Co? Jeszcze raz, nie słyszałem.", "à-rai ná ìik thii mâi dâai yin", "อะไรนะ อีกที ไม่ได้ยิน")),

("odmowa zaproszenia", "Podstawy i grzeczność", "Rejestr",
 "zaproszenie od przełożonego lub klienta",
 ("Niestety nie będę mógł uczestniczyć.", "khǎw à-phai khráp phǒm khong mâi sà-dùak khâo rûam", "ขออภัยครับ ผมคงไม่สะดวกเข้าร่วม",
  "Niestety nie będę mógł uczestniczyć w piątek.", "khǎw à-phai khráp wan sùk phǒm mâi sà-dùak khâo rûam", "ขออภัยครับ วันศุกร์ผมไม่สะดวกเข้าร่วม"),
 ("Chyba nie dam rady przyjść.", "phǒm khong pai mâi dâai khráp", "ผมคงไปไม่ได้ครับ",
  "Chyba nie dam rady przyjść, mam zajęcia.", "phǒm khong pai mâi dâai khráp tìt thù-rá", "ผมคงไปไม่ได้ครับ ติดธุระ"),
 ("Odpuszczę tym razem.", "khráng níi khǎw phàan náe", "ครั้งนี้ขอผ่านแหน่",
  "Odpuszczę tym razem, następnym razem na pewno.", "khráng níi khǎw phàan náe khráng nâa pai nâe", "ครั้งนี้ขอผ่านแหน่ ครั้งหน้าไปแน่")),

("pytanie o cenę", "Zakupy i pieniądze", "Rejestr",
 "salon, biuro sprzedaży, oferta firmowa",
 ("Jaka jest cena tej usługi?", "khâa brí-kaan níi raa-khaa thâo-rài khráp", "ค่าบริการนี้ราคาเท่าไหร่ครับ",
  "Jaka jest cena tej usługi z podatkiem?", "khâa brí-kaan níi ruam phaa-sǐi raa-khaa thâo-rài khráp", "ค่าบริการนี้รวมภาษีราคาเท่าไหร่ครับ"),
 ("Ile to kosztuje?", "an níi thâo-rài khráp", "อันนี้เท่าไหร่ครับ",
  "Ile to kosztuje za sztukę?", "an níi an lá thâo-rài khráp", "อันนี้อันละเท่าไหร่ครับ"),
 ("Po ile?", "thâo-rài lâ", "เท่าไหร่ล่ะ",
  "Po ile, szefie?", "thâo-rài lâ phîi", "เท่าไหร่ล่ะพี่")),

("zgoda na propozycję", "Praca i nauka", "Rejestr",
 "zebranie, korespondencja służbowa",
 ("Wyrażam zgodę na tę propozycję.", "phǒm hěn châwp kàp khâw sà-nǒoe níi khráp", "ผมเห็นชอบกับข้อเสนอนี้ครับ",
  "Wyrażam zgodę na tę propozycję w całości.", "phǒm hěn châwp kàp khâw sà-nǒoe níi thóng mòt khráp", "ผมเห็นชอบกับข้อเสนอนี้ทั้งหมดครับ"),
 ("Zgadzam się.", "tòk long khráp", "ตกลงครับ",
  "Zgadzam się, róbmy tak.", "tòk long khráp ao yàang nán", "ตกลงครับ เอาอย่างนั้น"),
 ("No dobra, może być.", "ao dì kâw dâai", "เอาดิ ก็ได้",
  "No dobra, może być, lecimy z tym.", "ao dì kâw dâai luǔi loei", "เอาดิ ก็ได้ ลุยเลย")),

("prośba o pomoc", "Podstawy i grzeczność", "Rejestr",
 "obcy człowiek, urząd, osoba starsza",
 ("Czy mógłbym prosić o pomoc?", "khǎw khwaam chûai lǔea nòi dâai mǎi khráp", "ขอความช่วยเหลือหน่อยได้ไหมครับ",
  "Czy mógłbym prosić o pomoc w wypełnieniu?", "khǎw khwaam chûai lǔea rûeang kràwk fawm nòi khráp", "ขอความช่วยเหลือเรื่องกรอกฟอร์มหน่อยครับ"),
 ("Pomożesz mi?", "chûai nòi dâai mǎi khráp", "ช่วยหน่อยได้ไหมครับ",
  "Pomożesz mi to przenieść?", "chûai yók nòi dâai mǎi khráp", "ช่วยยกหน่อยได้ไหมครับ"),
 ("Podasz mi to?", "sòng hâi nòi dì", "ส่งให้หน่อยดิ",
  "Podasz mi to, stary?", "sòng hâi nòi dì phûean", "ส่งให้หน่อยดิ เพื่อน")),

("przeprosiny za spóźnienie", "Podstawy i grzeczność", "Rejestr",
 "spotkanie z klientem, wizyta u lekarza",
 ("Przepraszam za spóźnienie.", "khǎw à-phai thîi maa cháa khráp", "ขออภัยที่มาช้าครับ",
  "Przepraszam za spóźnienie, korek na moście.", "khǎw à-phai thîi maa cháa khráp rót tìt bon sà-phaan", "ขออภัยที่มาช้าครับ รถติดบนสะพาน"),
 ("Sorry, spóźniłem się.", "khǎw-thôot thîi maa cháa khráp", "ขอโทษที่มาช้าครับ",
  "Sorry, spóźniłem się dziesięć minut.", "khǎw-thôot khráp maa cháa sìp naa-thii", "ขอโทษครับ มาช้าสิบนาที"),
 ("Sorki, zakorkowało.", "thôot dì rót tìt", "โทษดิ รถติด",
  "Sorki, zakorkowało totalnie.", "thôot dì rót tìt nàk mâak", "โทษดิ รถติดหนักมาก")),

("pytanie o samopoczucie", "Zdrowie", "Rejestr",
 "rozmowa lekarza z pacjentem, wizyta u chorego przełożonego",
 ("Jak się pan dziś czuje?", "wan níi khun rúu-sùek pen yang-ngai bâang khráp", "วันนี้คุณรู้สึกเป็นยังไงบ้างครับ",
  "Jak się pan dziś czuje po lekach?", "kin yaa láew wan níi rúu-sùek pen yang-ngai bâang khráp", "กินยาแล้ววันนี้รู้สึกเป็นยังไงบ้างครับ"),
 ("Jak się czujesz?", "rúu-sùek dii khûen mǎi khráp", "รู้สึกดีขึ้นไหมครับ",
  "Jak się czujesz, lepiej?", "rúu-sùek dii khûen mǎi khráp wan níi", "รู้สึกดีขึ้นไหมครับวันนี้"),
 ("Lepiej ci już?", "dii khûen rúe yang lâ", "ดีขึ้นหรือยังล่ะ",
  "Lepiej ci już, czy wciąż leżysz?", "dii khûen rúe yang lâ rǔe yang nawn yùu", "ดีขึ้นหรือยังล่ะ หรือยังนอนอยู่")),

("prośba o chwilę czasu", "Praca i nauka", "Rejestr",
 "rozmowa z przełożonym, prośba do klienta",
 ("Czy mógłbym prosić o chwilę pańskiego czasu?", "khǎw rop-kuan wee-laa khǎwng khun sák khrûu dâai mǎi khráp", "ขอรบกวนเวลาของคุณสักครู่ได้ไหมครับ",
  "Czy mógłbym prosić o chwilę pańskiego czasu po zebraniu?", "lǎng prà-chum khǎw rop-kuan wee-laa sák khrûu khráp", "หลังประชุมขอรบกวนเวลาสักครู่ครับ"),
 ("Masz minutę?", "mii wee-laa sák naa-thii mǎi khráp", "มีเวลาสักนาทีไหมครับ",
  "Masz minutę na jedną sprawę?", "mii wee-laa sák naa-thii mǎi khráp rûeang diao", "มีเวลาสักนาทีไหมครับ เรื่องเดียว"),
 ("Chwilkę masz?", "wâang pàp nùeng mǎi", "ว่างแป๊บหนึ่งไหม",
  "Chwilkę masz? Szybka sprawa.", "wâang pàp nùeng mǎi rûeang nít diao", "ว่างแป๊บหนึ่งไหม เรื่องนิดเดียว")),

("informacja o opóźnieniu", "Praca i nauka", "Rejestr",
 "powiadomienie klienta, pismo do kontrahenta",
 ("Uprzejmie informuję o opóźnieniu.", "khǎw riian jâeng wâa mii khwaam lâa cháa khráp", "ขอเรียนแจ้งว่ามีความล่าช้าครับ",
  "Uprzejmie informuję o opóźnieniu o dwa dni.", "khǎw riian jâeng wâa mii khwaam lâa cháa sǎwng wan khráp", "ขอเรียนแจ้งว่ามีความล่าช้าสองวันครับ"),
 ("Będzie później niż planowaliśmy.", "khong cháa kwàa thîi khui wái khráp", "คงช้ากว่าที่คุยไว้ครับ",
  "Będzie później niż planowaliśmy, jakieś dwa dni.", "khong cháa kwàa thîi khui wái sǎwng wan khráp", "คงช้ากว่าที่คุยไว้สองวันครับ"),
 ("Nie wyrobimy się.", "mâi than wâ", "ไม่ทันว่ะ",
  "Nie wyrobimy się na jutro.", "phrûng-níi mâi than wâ", "พรุ่งนี้ไม่ทันว่ะ")),

("prośba o poczekanie", "Praca i nauka", "Rejestr",
 "obsługa klienta, recepcja",
 ("Proszę uprzejmie o chwilę cierpliwości.", "khǎw khwaam kà-rú-naa raw sák khrûu khráp", "ขอความกรุณารอสักครู่ครับ",
  "Proszę uprzejmie o chwilę cierpliwości, sprawdzam.", "khǎw khwaam kà-rú-naa raw sák khrûu khráp kam-lang trùat sàwp", "ขอความกรุณารอสักครู่ครับ กำลังตรวจสอบ"),
 ("Chwileczkę, proszę.", "raw sák khrûu ná khráp", "รอสักครู่นะครับ",
  "Chwileczkę, proszę, zaraz wracam.", "raw sák khrûu ná khráp dǐao maa", "รอสักครู่นะครับ เดี๋ยวมา"),
 ("Sekundka.", "pàp nùeng ná", "แป๊บหนึ่งนะ",
  "Sekundka, zaraz to ogarnę.", "pàp nùeng ná dǐao jàt hâi", "แป๊บหนึ่งนะ เดี๋ยวจัดให้")),

("podziękowanie", "Podstawy i grzeczność", "Rejestr",
 "podziękowanie za realną przysługę, pismo oficjalne",
 ("Serdecznie dziękuję za okazaną pomoc.", "khàwp phrá-khun sǎm-ràp khwaam chûai lǔea khráp", "ขอบพระคุณสำหรับความช่วยเหลือครับ",
  "Serdecznie dziękuję za okazaną pomoc w tej sprawie.", "khàwp phrá-khun sǎm-ràp khwaam chûai lǔea nai rûeang níi khráp", "ขอบพระคุณสำหรับความช่วยเหลือในเรื่องนี้ครับ"),
 ("Dziękuję bardzo.", "khàwp-khun mâak khráp", "ขอบคุณมากครับ",
  "Dziękuję bardzo za dziś.", "khàwp-khun mâak khráp sǎm-ràp wan níi", "ขอบคุณมากครับสำหรับวันนี้"),
 ("Dzięki wielkie.", "thǽngkîu mâak loei", "แต๊งกิ้วมากเลย",
  "Dzięki wielkie, uratowałeś mnie.", "thǽngkîu mâak loei chûai chii-wít wái", "แต๊งกิ้วมากเลย ช่วยชีวิตไว้")),

("wyrażenie niezgody", "Praca i nauka", "Rejestr",
 "dyskusja z przełożonym, oficjalne stanowisko",
 ("Pozwolę sobie mieć odmienne zdanie.", "khǎw à-nú-yâat hěn tàang àwk pai khráp", "ขออนุญาตเห็นต่างออกไปครับ",
  "Pozwolę sobie mieć odmienne zdanie co do terminu.", "rûeang kam-nòt khǎw à-nú-yâat hěn tàang àwk pai khráp", "เรื่องกำหนดขออนุญาตเห็นต่างออกไปครับ"),
 ("Nie do końca się zgadzam.", "phǒm mâi khâwi hěn dûai khráp", "ผมไม่ค่อยเห็นด้วยครับ",
  "Nie do końca się zgadzam z tym punktem.", "khâw níi phǒm mâi khâwi hěn dûai khráp", "ข้อนี้ผมไม่ค่อยเห็นด้วยครับ"),
 ("No nie wiem, mnie to nie leży.", "mâi náe wâ phǒm mâi ao dûai", "ไม่แน่ว่ะ ผมไม่เอาด้วย",
  "No nie wiem, mnie to nie leży w ogóle.", "mâi náe wâ phǒm mâi ao dûai loei", "ไม่แน่ว่ะ ผมไม่เอาด้วยเลย")),

("zaproszenie na posiłek", "Restauracja", "Rejestr",
 "zaproszenie klienta lub przełożonego",
 ("Czy zechciałby pan zjeść z nami obiad?", "khǎw riian chooen thaan aa-hǎan klaang wan dûai kan khráp", "ขอเรียนเชิญทานอาหารกลางวันด้วยกันครับ",
  "Czy zechciałby pan zjeść z nami obiad po spotkaniu?", "lǎng prà-chum khǎw riian chooen thaan aa-hǎan klaang wan dûai kan khráp", "หลังประชุมขอเรียนเชิญทานอาหารกลางวันด้วยกันครับ"),
 ("Zjemy razem?", "pai kin khâao dûai kan mǎi khráp", "ไปกินข้าวด้วยกันไหมครับ",
  "Zjemy razem po pracy?", "lôek ngaan pai kin khâao dûai kan mǎi khráp", "เลิกงานไปกินข้าวด้วยกันไหมครับ"),
 ("Idziemy na żarcie?", "pai sòi kan mǎi", "ไปซอยกันไหม",
  "Idziemy na żarcie? Znam miejsce.", "pai sòi kan mǎi rúu-jàk ráan dèt", "ไปซอยกันไหม รู้จักร้านเด็ด")),

("prośba o dokument", "Praca i nauka", "Rejestr",
 "urząd, bank, dział kadr",
 ("Uprzejmie proszę o wydanie zaświadczenia.", "khǎw khwaam kà-rú-naa àwk nǎng-sǔe rap-rawng khráp", "ขอความกรุณาออกหนังสือรับรองครับ",
  "Uprzejmie proszę o wydanie zaświadczenia o zatrudnieniu.", "khǎw khwaam kà-rú-naa àwk nǎng-sǔe rap-rawng kaan tham-ngaan khráp", "ขอความกรุณาออกหนังสือรับรองการทำงานครับ"),
 ("Poproszę zaświadczenie.", "khǎw bai rap-rawng nòi khráp", "ขอใบรับรองหน่อยครับ",
  "Poproszę zaświadczenie na jutro.", "khǎw bai rap-rawng phrûng-níi dâai mǎi khráp", "ขอใบรับรองพรุ่งนี้ได้ไหมครับ"),
 ("Dasz mi ten papier?", "khǎw krà-dàat bai nán nòi", "ขอกระดาษใบนั้นหน่อย",
  "Dasz mi ten papier? Potrzebny do banku.", "khǎw krà-dàat bai nán nòi chái thîi thá-naa-khaan", "ขอกระดาษใบนั้นหน่อย ใช้ที่ธนาคาร")),

("pytanie o drogę", "Miejsca i orientacja", "Rejestr",
 "pytanie ochroniarza, urzędnika, personelu",
 ("Czy mógłbym zapytać o drogę?", "khǎw rop-kuan thǎam thaang nòi dâai mǎi khráp", "ขอรบกวนถามทางหน่อยได้ไหมครับ",
  "Czy mógłbym zapytać o drogę do biura wizowego?", "khǎw rop-kuan thǎam thaang pai phà-nàek wii-sâa khráp", "ขอรบกวนถามทางไปแผนกวีซ่าครับ"),
 ("Którędy do stacji?", "pai sà-thǎa-nii thaang nǎi khráp", "ไปสถานีทางไหนครับ",
  "Którędy do stacji, prosto czy w lewo?", "pai sà-thǎa-nii thaang nǎi khráp trong rǔe líao sáai", "ไปสถานีทางไหนครับ ตรงหรือเลี้ยวซ้าย"),
 ("Gdzie to jest?", "yùu nǎi wâ", "อยู่ไหนว่ะ",
  "Gdzie to jest, wiesz może?", "yùu nǎi wâ rúu mǎi", "อยู่ไหนว่ะ รู้ไหม")),

("prośba o zniżkę", "Zakupy i pieniądze", "Rejestr",
 "negocjacje z firmą, oferta hurtowa",
 ("Czy istnieje możliwość obniżenia ceny?", "phaw jà mii khwaam pen pai dâai nai kaan lót raa-khaa mǎi khráp", "พอจะมีความเป็นไปได้ในการลดราคาไหมครับ",
  "Czy istnieje możliwość obniżenia ceny przy dużym zamówieniu?", "thâa sàng jam-nuan mâak phaw jà lót raa-khaa dâai mǎi khráp", "ถ้าสั่งจำนวนมากพอจะลดราคาได้ไหมครับ"),
 ("Da się taniej?", "lót nòi dâai mǎi khráp", "ลดหน่อยได้ไหมครับ",
  "Da się taniej, jeśli wezmę dwa?", "ao sǎwng an lót nòi dâai mǎi khráp", "เอาสองอันลดหน่อยได้ไหมครับ"),
 ("Opuść trochę.", "lót nòi dì phîi", "ลดหน่อยดิพี่",
  "Opuść trochę, wezmę od razu.", "lót nòi dì phîi ao loei", "ลดหน่อยดิพี่ เอาเลย")),

("pytanie o zdanie", "Cechy i opinie", "Rejestr",
 "zebranie, ankieta, rozmowa z klientem",
 ("Jakie jest pana zdanie w tej kwestii?", "khun mii khwaam khít hěn tàw rûeang níi yàang rai khráp", "คุณมีความคิดเห็นต่อเรื่องนี้อย่างไรครับ",
  "Jakie jest pana zdanie w kwestii nowych zasad?", "khun mii khwaam khít hěn tàw kót mài yàang rai khráp", "คุณมีความคิดเห็นต่อกฎใหม่อย่างไรครับ"),
 ("Co o tym myślisz?", "khít yang-ngai kàp rûeang níi khráp", "คิดยังไงกับเรื่องนี้ครับ",
  "Co o tym myślisz, warto?", "khít yang-ngai khráp nâa tham mǎi", "คิดยังไงครับ น่าทำไหม"),
 ("No i jak ci się widzi?", "wâa ngai lâ", "ว่าไงล่ะ",
  "No i jak ci się widzi, bierzemy?", "wâa ngai lâ ao mǎi", "ว่าไงล่ะ เอาไหม")),

("prośba o wyjaśnienie", "Praca i nauka", "Rejestr",
 "urząd, bank, obsługa klienta",
 ("Czy mógłbym prosić o wyjaśnienie tej pozycji?", "khǎw rop-kuan à-thí-baai raai kaan níi dâai mǎi khráp", "ขอรบกวนอธิบายรายการนี้ได้ไหมครับ",
  "Czy mógłbym prosić o wyjaśnienie tej pozycji na rachunku?", "khǎw rop-kuan à-thí-baai raai kaan níi nai bin khráp", "ขอรบกวนอธิบายรายการนี้ในบิลครับ"),
 ("Możesz mi to wyjaśnić?", "chûai à-thí-baai hâi nòi dâai mǎi khráp", "ช่วยอธิบายให้หน่อยได้ไหมครับ",
  "Możesz mi to wyjaśnić prościej?", "chûai à-thí-baai hâi ngâai kwàa níi dâai mǎi khráp", "ช่วยอธิบายให้ง่ายกว่านี้ได้ไหมครับ"),
 ("O co tu chodzi?", "man ngai lâ nîi", "มันไงล่ะเนี่ย",
  "O co tu chodzi z tą opłatą?", "khâa níi man ngai lâ nîi", "ค่านี้มันไงล่ะเนี่ย")),

("propozycja spotkania", "Praca i nauka", "Rejestr",
 "korespondencja z klientem, umawianie się z urzędem",
 ("Czy odpowiadałby panu termin w środę?", "wan phút khun sà-dùak mǎi khráp", "วันพุธคุณสะดวกไหมครับ",
  "Czy odpowiadałby panu termin w środę rano?", "wan phút tawn cháo khun sà-dùak mǎi khráp", "วันพุธตอนเช้าคุณสะดวกไหมครับ"),
 ("Pasuje ci środa?", "wan phút dâai mǎi khráp", "วันพุธได้ไหมครับ",
  "Pasuje ci środa po południu?", "wan phút bàai dâai mǎi khráp", "วันพุธบ่ายได้ไหมครับ"),
 ("Środa gra?", "phút wôei", "พุธเวย",
  "Środa gra? Daj znać.", "phút wôei bàwk dûai", "พุธเวย บอกด้วย")),

("informacja o problemie", "Praca i nauka", "Rejestr",
 "zgłoszenie do klienta lub przełożonego",
 ("Chciałbym zgłosić pewną nieprawidłowość.", "khǎw riian jâeng khâw phìt phlâat khráp", "ขอเรียนแจ้งข้อผิดพลาดครับ",
  "Chciałbym zgłosić pewną nieprawidłowość w raporcie.", "khǎw riian jâeng khâw phìt phlâat nai raai-ngaan khráp", "ขอเรียนแจ้งข้อผิดพลาดในรายงานครับ"),
 ("Mamy problem.", "mii pan-hǎa nít nùeng khráp", "มีปัญหานิดหนึ่งครับ",
  "Mamy problem z dostawą.", "mii pan-hǎa rûeang sòng khǎwng khráp", "มีปัญหาเรื่องส่งของครับ"),
 ("Coś się posypało.", "man phang láew wâ", "มันพังแล้วว่ะ",
  "Coś się posypało w systemie.", "rá-bòp man phang láew wâ", "ระบบมันพังแล้วว่ะ")),

("prośba o kontakt", "Praca i nauka", "Rejestr",
 "korespondencja służbowa, kontakt z urzędem",
 ("Uprzejmie proszę o kontakt zwrotny.", "khǎw khwaam kà-rú-naa tìt tàw klàp khráp", "ขอความกรุณาติดต่อกลับครับ",
  "Uprzejmie proszę o kontakt zwrotny w tym tygodniu.", "khǎw khwaam kà-rú-naa tìt tàw klàp phaai-nai aa-thít níi khráp", "ขอความกรุณาติดต่อกลับภายในอาทิตย์นี้ครับ"),
 ("Odezwij się, proszę.", "tìt tàw klàp dûai ná khráp", "ติดต่อกลับด้วยนะครับ",
  "Odezwij się, proszę, jak będziesz wiedział.", "rúu láew tìt tàw klàp dûai ná khráp", "รู้แล้วติดต่อกลับด้วยนะครับ"),
 ("Odpisz mi.", "thák maa dûai ná", "ทักมาด้วยนะ",
  "Odpisz mi, jak wrócisz.", "klàp maa láew thák dûai ná", "กลับมาแล้วทักด้วยนะ")),

("wyrażenie pochwały", "Praca i nauka", "Rejestr",
 "ocena roczna, list referencyjny",
 ("Doceniam pański profesjonalizm.", "phǒm chûen chom khwaam pen mûu aa-chîip khǎwng khun khráp", "ผมชื่นชมความเป็นมืออาชีพของคุณครับ",
  "Doceniam pański profesjonalizm w tej sprawie.", "phǒm chûen chom khwaam pen mûu aa-chîip nai rûeang níi khráp", "ผมชื่นชมความเป็นมืออาชีพในเรื่องนี้ครับ"),
 ("Świetnie to zrobiłeś.", "tham dâai dii mâak loei khráp", "ทำได้ดีมากเลยครับ",
  "Świetnie to zrobiłeś, klient chwalił.", "tham dâai dii mâak loei khráp lûuk-kháa chom", "ทำได้ดีมากเลยครับ ลูกค้าชม"),
 ("Zawodnik, szacun.", "kèng wâ", "เก่งว่ะ",
  "Zawodnik, szacun, sam bym nie dał rady.", "kèng wâ phǒm khong tham mâi dâai", "เก่งว่ะ ผมคงทำไม่ได้")),

("prośba o zgodę", "Praca i nauka", "Rejestr",
 "wniosek do przełożonego, pismo urzędowe",
 ("Zwracam się z prośbą o zgodę.", "khǎw à-nú-yâat khráp", "ขออนุญาตครับ",
  "Zwracam się z prośbą o zgodę na wcześniejsze wyjście.", "khǎw à-nú-yâat klàp kàwn khráp", "ขออนุญาตกลับก่อนครับ"),
 ("Mogę?", "khǎw dâai mǎi khráp", "ขอได้ไหมครับ",
  "Mogę wyjść godzinę wcześniej?", "khǎw klàp kàwn nùeng chûa-moong dâai mǎi khráp", "ขอกลับก่อนหนึ่งชั่วโมงได้ไหมครับ"),
 ("Można?", "dâai pà", "ได้ป่ะ",
  "Można, czy będzie afera?", "dâai pà rǔe jà mii rûeang", "ได้ป่ะ หรือจะมีเรื่อง")),

("wyrażenie współczucia", "Ludzie i rodzina", "Rejestr",
 "kondolencje, oficjalne wyrazy współczucia",
 ("Składam wyrazy współczucia.", "khǎw sà-daeng khwaam sǐa jai dûai khráp", "ขอแสดงความเสียใจด้วยครับ",
  "Składam wyrazy współczucia całej rodzinie.", "khǎw sà-daeng khwaam sǐa jai kàp khrâwp khrua dûai khráp", "ขอแสดงความเสียใจกับครอบครัวด้วยครับ"),
 ("Bardzo mi przykro.", "sǐa jai dûai ná khráp", "เสียใจด้วยนะครับ",
  "Bardzo mi przykro, trzymaj się.", "sǐa jai dûai ná khráp sûu sûu", "เสียใจด้วยนะครับ สู้ๆ"),
 ("Trzymaj się, stary.", "sûu sûu ná wâ", "สู้ๆ นะว่ะ",
  "Trzymaj się, stary, jestem obok.", "sûu sûu ná wâ phǒm yùu trong níi", "สู้ๆ นะว่ะ ผมอยู่ตรงนี้")),

("pytanie o dostępność", "Hotel", "Rejestr",
 "recepcja hotelowa, rezerwacja telefoniczna",
 ("Czy dysponują państwo wolnym pokojem?", "mii hâwng wâang mǎi khráp", "มีห้องว่างไหมครับ",
  "Czy dysponują państwo wolnym pokojem na dwie noce?", "mii hâwng wâang sǎwng khuen mǎi khráp", "มีห้องว่างสองคืนไหมครับ"),
 ("Są wolne pokoje?", "hâwng wâang yang mii mǎi khráp", "ห้องว่างยังมีไหมครับ",
  "Są wolne pokoje na dziś?", "khuen níi hâwng wâang yang mii mǎi khráp", "คืนนี้ห้องว่างยังมีไหมครับ"),
 ("Jest coś wolnego?", "mii wâang pà", "มีว่างป่ะ",
  "Jest coś wolnego na noc?", "khuen níi mii wâang pà", "คืนนี้มีว่างป่ะ")),

("prośba o cierpliwość klienta", "Praca i nauka", "Rejestr",
 "komunikat firmowy, obsługa reklamacji",
 ("Prosimy o wyrozumiałość w tej sprawie.", "khǎw khwaam kà-rú-naa khâo-jai nai rûeang níi khráp", "ขอความกรุณาเข้าใจในเรื่องนี้ครับ",
  "Prosimy o wyrozumiałość, pracujemy nad rozwiązaniem.", "khǎw khwaam kà-rú-naa khâo-jai khráp kam-lang kâe khǎi yùu", "ขอความกรุณาเข้าใจครับ กำลังแก้ไขอยู่"),
 ("Proszę o cierpliwość.", "khǎw hâi jai yen ná khráp", "ขอให้ใจเย็นนะครับ",
  "Proszę o cierpliwość, zaraz to załatwię.", "khǎw hâi jai yen ná khráp dǐao jàt kaan hâi", "ขอให้ใจเย็นนะครับ เดี๋ยวจัดการให้"),
 ("Spoko, ogarniemy.", "chill chill dǐao jàt hâi", "ชิลๆ เดี๋ยวจัดให้",
  "Spoko, ogarniemy to dzisiaj.", "chill chill wan níi jàt hâi", "ชิลๆ วันนี้จัดให้")),

("pożegnanie", "Podstawy i grzeczność", "Rejestr",
 "wyjście ze spotkania, pożegnanie klienta",
 ("Pozwolę sobie się pożegnać.", "khǎw à-nú-yâat laa kàwn khráp", "ขออนุญาตลาก่อนครับ",
  "Pozwolę sobie się pożegnać, dziękuję za spotkanie.", "khǎw à-nú-yâat laa kàwn khráp khàwp-khun sǎm-ràp kaan phóp", "ขออนุญาตลาก่อนครับ ขอบคุณสำหรับการพบ"),
 ("To ja lecę, do zobaczenia.", "phǒm pai kàwn ná khráp", "ผมไปก่อนนะครับ",
  "To ja lecę, do zobaczenia w poniedziałek.", "phǒm pai kàwn ná khráp jôe kan wan jan", "ผมไปก่อนนะครับ เจอกันวันจันทร์"),
 ("Nara.", "pai lá", "ไปละ",
  "Nara, pisz.", "pai lá thák maa dûai", "ไปละ ทักมาด้วย")),

("prośba o powolniejsze mówienie", "Podstawy i grzeczność", "Rejestr",
 "rozmowa z urzędnikiem albo lekarzem",
 ("Czy mógłby pan mówić nieco wolniej?", "khǎw rop-kuan phûut cháa long nòi dâai mǎi khráp", "ขอรบกวนพูดช้าลงหน่อยได้ไหมครับ",
  "Czy mógłby pan mówić nieco wolniej, notuję.", "khǎw rop-kuan phûut cháa long nòi khráp phǒm kam-lang jòt", "ขอรบกวนพูดช้าลงหน่อยครับ ผมกำลังจด"),
 ("Wolniej, proszę.", "cháa cháa nòi khráp", "ช้าๆ หน่อยครับ",
  "Wolniej, proszę, uczę się dopiero.", "cháa cháa nòi khráp phǒm phôoeng rian", "ช้าๆ หน่อยครับ ผมเพิ่งเรียน"),
 ("Wolniej, nie nadążam.", "cháa cháa dì taam mâi than", "ช้าๆ ดิ ตามไม่ทัน",
  "Wolniej, nie nadążam za tobą.", "cháa cháa dì taam khun mâi than", "ช้าๆ ดิ ตามคุณไม่ทัน")),

("potwierdzenie zrozumienia", "Praca i nauka", "Rejestr",
 "odpowiedź przełożonemu, potwierdzenie polecenia",
 ("Przyjąłem do wiadomości.", "ráp sâap láew khráp", "รับทราบแล้วครับ",
  "Przyjąłem do wiadomości i przekażę zespołowi.", "ráp sâap láew khráp jà jâeng thiim tàw", "รับทราบแล้วครับ จะแจ้งทีมต่อ"),
 ("Jasne, rozumiem.", "khâo-jai láew khráp", "เข้าใจแล้วครับ",
  "Jasne, rozumiem, zrobię do jutra.", "khâo-jai láew khráp jà tham hâi kàwn phrûng-níi", "เข้าใจแล้วครับ จะทำให้ก่อนพรุ่งนี้"),
 ("Aha, kumam.", "âw ráw láew", "อ๋อ รู้แล้ว",
  "Aha, kumam, robi się.", "âw ráw láew jàt hâi", "อ๋อ รู้แล้ว จัดให้")),

("prośba o przypomnienie", "Praca i nauka", "Rejestr",
 "prośba do współpracownika lub asystenta",
 ("Uprzejmie proszę o przypomnienie mi o tym.", "khǎw rop-kuan tuean phǒm dûai khráp", "ขอรบกวนเตือนผมด้วยครับ",
  "Uprzejmie proszę o przypomnienie mi o tym w poniedziałek.", "khǎw rop-kuan tuean phǒm wan jan dûai khráp", "ขอรบกวนเตือนผมวันจันทร์ด้วยครับ"),
 ("Przypomnij mi, proszę.", "chûai tuean dûai ná khráp", "ช่วยเตือนด้วยนะครับ",
  "Przypomnij mi, proszę, bo zapomnę.", "chûai tuean dûai ná khráp dǐao luem", "ช่วยเตือนด้วยนะครับ เดี๋ยวลืม"),
 ("Szturchnij mnie potem.", "thák maa thii ná", "ทักมาทีนะ",
  "Szturchnij mnie potem, na pewno zapomnę.", "thák maa thii ná luem nâe nawn", "ทักมาทีนะ ลืมแน่นอน")),

("informacja o nieobecności", "Praca i nauka", "Rejestr",
 "zgłoszenie nieobecności przełożonemu",
 ("Uprzejmie informuję, że będę nieobecny.", "khǎw riian jâeng wâa phǒm jà mâi yùu khráp", "ขอเรียนแจ้งว่าผมจะไม่อยู่ครับ",
  "Uprzejmie informuję, że będę nieobecny od czwartku.", "khǎw riian jâeng wâa phǒm jà mâi yùu tâng tàae wan phá-rúe-hàt khráp", "ขอเรียนแจ้งว่าผมจะไม่อยู่ตั้งแต่วันพฤหัสครับ"),
 ("Nie będzie mnie jutro.", "phrûng-níi phǒm mâi yùu khráp", "พรุ่งนี้ผมไม่อยู่ครับ",
  "Nie będzie mnie jutro, mam sprawy.", "phrûng-níi phǒm mâi yùu khráp tìt thù-rá", "พรุ่งนี้ผมไม่อยู่ครับ ติดธุระ"),
 ("Jutro mnie nie ma.", "phrûng-níi mâi maa ná", "พรุ่งนี้ไม่มานะ",
  "Jutro mnie nie ma, ogarnijcie beze mnie.", "phrûng-níi mâi maa ná jàt kan eeng dûai", "พรุ่งนี้ไม่มานะ จัดกันเองด้วย")),

("upomnienie o płatność", "Zakupy i pieniądze", "Rejestr",
 "przypomnienie klientowi o zaległej fakturze",
 ("Uprzejmie przypominamy o zaległej płatności.", "khǎw riian tuean rûeang yâwt khâang châm-rá khráp", "ขอเรียนเตือนเรื่องยอดค้างชำระครับ",
  "Uprzejmie przypominamy o zaległej płatności z zeszłego miesiąca.", "khǎw riian tuean yâwt khâang châm-rá duean thîi láew khráp", "ขอเรียนเตือนยอดค้างชำระเดือนที่แล้วครับ"),
 ("Przypominam o płatności.", "tuean rûeang jàai ngoen ná khráp", "เตือนเรื่องจ่ายเงินนะครับ",
  "Przypominam o płatności do piątku.", "tuean rûeang jàai ngoen kàwn wan sùk ná khráp", "เตือนเรื่องจ่ายเงินก่อนวันศุกร์นะครับ"),
 ("Kasa jeszcze nie przyszła.", "tang yang mâi khâo loei ná", "ตังค์ยังไม่เข้าเลยนะ",
  "Kasa jeszcze nie przyszła, sprawdzisz?", "tang yang mâi khâo loei ná chék hâi nòi", "ตังค์ยังไม่เข้าเลยนะ เช็คให้หน่อย")),

("przedstawienie się", "Ludzie i rodzina", "Rejestr",
 "spotkanie biznesowe, rozmowa kwalifikacyjna",
 ("Pozwolą państwo, że się przedstawię.", "khǎw à-nú-yâat náe-nam tua khráp", "ขออนุญาตแนะนำตัวครับ",
  "Pozwolą państwo, że się przedstawię — jestem z działu handlowego.", "khǎw à-nú-yâat náe-nam tua khráp phǒm maa jàak fàai khǎai", "ขออนุญาตแนะนำตัวครับ ผมมาจากฝ่ายขาย"),
 ("Nazywam się Marek.", "phǒm chûe maa-rèk khráp", "ผมชื่อมาเร็กครับ",
  "Nazywam się Marek, miło mi.", "phǒm chûe maa-rèk khráp yin dii thîi dâai rúu-jàk", "ผมชื่อมาเร็กครับ ยินดีที่ได้รู้จัก"),
 ("Jestem Marek, cześć.", "phǒm maa-rèk wàt dii", "ผมมาเร็ก หวัดดี",
  "Jestem Marek, cześć, siadaj.", "phǒm maa-rèk wàt dii nâng sí", "ผมมาเร็ก หวัดดี นั่งสิ")),

("prośba o zwrot pieniędzy", "Zakupy i pieniądze", "Rejestr",
 "reklamacja pisemna, rozmowa z kierownikiem sklepu",
 ("Wnoszę o zwrot uiszczonej kwoty.", "khǎw yûen rûeang khǎw ngoen khuen khráp", "ขอยื่นเรื่องขอเงินคืนครับ",
  "Wnoszę o zwrot uiszczonej kwoty wraz z opłatą.", "khǎw yûen rûeang khǎw ngoen khuen phráwm khâa tham-niam khráp", "ขอยื่นเรื่องขอเงินคืนพร้อมค่าธรรมเนียมครับ"),
 ("Chciałbym zwrot pieniędzy.", "khǎw ngoen khuen dâai mǎi khráp", "ขอเงินคืนได้ไหมครับ",
  "Chciałbym zwrot pieniędzy, towar jest wadliwy.", "khǎw ngoen khuen dâai mǎi khráp khǎwng mii tam-nì", "ขอเงินคืนได้ไหมครับ ของมีตำหนิ"),
 ("Oddajcie kasę.", "khuen tang maa thòe", "คืนตังค์มาเถอะ",
  "Oddajcie kasę, nie chcę wymiany.", "khuen tang maa thòe mâi ao khǎwng plìan", "คืนตังค์มาเถอะ ไม่เอาของเปลี่ยน")),

("pytanie o godziny otwarcia", "Miejsca i orientacja", "Rejestr",
 "telefon do urzędu albo kliniki",
 ("O której godzinie państwo otwierają?", "pòoet tham kaan kìi moong khráp", "เปิดทำการกี่โมงครับ",
  "O której godzinie państwo otwierają w soboty?", "wan sǎo pòoet tham kaan kìi moong khráp", "วันเสาร์เปิดทำการกี่โมงครับ"),
 ("O której otwieracie?", "pòoet kìi moong khráp", "เปิดกี่โมงครับ",
  "O której otwieracie w niedzielę?", "wan aa-thít pòoet kìi moong khráp", "วันอาทิตย์เปิดกี่โมงครับ"),
 ("Od której jesteście?", "kìi moong pòoet lâ", "กี่โมงเปิดล่ะ",
  "Od której jesteście dzisiaj?", "wan níi kìi moong pòoet lâ", "วันนี้กี่โมงเปิดล่ะ")),

("odmowa zakupu", "Zakupy i pieniądze", "Rejestr",
 "rozmowa z handlowcem, oferta w biurze",
 ("Dziękuję, ale nie jestem zainteresowany.", "khàwp-khun khráp tàae phǒm mâi sǒn jai", "ขอบคุณครับ แต่ผมไม่สนใจ",
  "Dziękuję, ale nie jestem zainteresowany tą ofertą.", "khàwp-khun khráp tàae phǒm mâi sǒn jai khâw sà-nǒoe níi", "ขอบคุณครับ แต่ผมไม่สนใจข้อเสนอนี้"),
 ("Dziś nie kupuję.", "wan níi mâi ao khráp", "วันนี้ไม่เอาครับ",
  "Dziś nie kupuję, może innym razem.", "wan níi mâi ao khráp wái khraao nâa", "วันนี้ไม่เอาครับ ไว้คราวหน้า"),
 ("Nie, dzięki.", "mâi ao wâ", "ไม่เอาว่ะ",
  "Nie, dzięki, mam już taki.", "mâi ao wâ mii yùu láew", "ไม่เอาว่ะ มีอยู่แล้ว")),

("pytanie o zdrowie bliskiej osoby", "Ludzie i rodzina", "Rejestr",
 "pytanie do przełożonego albo osoby starszej",
 ("Jak zdrowie pańskiej mamy?", "khun mâe khun sà-baai dii mǎi khráp", "คุณแม่คุณสบายดีไหมครับ",
  "Jak zdrowie pańskiej mamy po zabiegu?", "lǎng phàa tàt khun mâe sà-baai dii mǎi khráp", "หลังผ่าตัดคุณแม่สบายดีไหมครับ"),
 ("Jak tam mama?", "mâe pen yang-ngai bâang khráp", "แม่เป็นยังไงบ้างครับ",
  "Jak tam mama, lepiej?", "mâe dii khûen mǎi khráp", "แม่ดีขึ้นไหมครับ"),
 ("Mama zdrowa?", "mâe ok mǎi", "แม่โอเคไหม",
  "Mama zdrowa? Pozdrów ją.", "mâe ok mǎi fàak sà-wàt-dii dûai", "แม่โอเคไหม ฝากสวัสดีด้วย")),

("prośba o przesunięcie terminu", "Praca i nauka", "Rejestr",
 "pismo do klienta, prośba do urzędu",
 ("Zwracam się z prośbą o przesunięcie terminu.", "khǎw khwaam kà-rú-naa lûean kam-nòt àwk pai khráp", "ขอความกรุณาเลื่อนกำหนดออกไปครับ",
  "Zwracam się z prośbą o przesunięcie terminu o tydzień.", "khǎw khwaam kà-rú-naa lûean kam-nòt àwk pai nùeng aa-thít khráp", "ขอความกรุณาเลื่อนกำหนดออกไปหนึ่งอาทิตย์ครับ"),
 ("Możemy to przełożyć?", "lûean dâai mǎi khráp", "เลื่อนได้ไหมครับ",
  "Możemy to przełożyć na przyszły tydzień?", "lûean pen aa-thít nâa dâai mǎi khráp", "เลื่อนเป็นอาทิตย์หน้าได้ไหมครับ"),
 ("Przesuwamy?", "lûean pà", "เลื่อนป่ะ",
  "Przesuwamy? Nie wyrabiam.", "lûean pà tham mâi than", "เลื่อนป่ะ ทำไม่ทัน")),

("prośba o ciszę", "Dom i codzienność", "Rejestr",
 "prośba do sąsiada, którego nie znasz",
 ("Czy mógłbym prosić o ściszenie?", "khǎw rop-kuan bao sǐang long nòi dâai mǎi khráp", "ขอรบกวนเบาเสียงลงหน่อยได้ไหมครับ",
  "Czy mógłbym prosić o ściszenie po dwudziestej drugiej?", "lǎng sìi thûm khǎw rop-kuan bao sǐang long nòi khráp", "หลังสี่ทุ่มขอรบกวนเบาเสียงลงหน่อยครับ"),
 ("Ciszej, proszę.", "bao nòi khráp", "เบาหน่อยครับ",
  "Ciszej, proszę, dzieci śpią.", "bao nòi khráp dèk nawn yùu", "เบาหน่อยครับ เด็กนอนอยู่"),
 ("Przycisz to.", "bao dì", "เบาดิ",
  "Przycisz to, słychać przez ścianę.", "bao dì dâi yin thá-lú fǎa", "เบาดิ ได้ยินทะลุฝา")),

("przyjęcie zaproszenia", "Small talk", "Rejestr",
 "odpowiedź na zaproszenie służbowe",
 ("Z przyjemnością przyjmuję zaproszenie.", "yin dii ráp kham chooen khráp", "ยินดีรับคำเชิญครับ",
  "Z przyjemnością przyjmuję zaproszenie na piątek.", "yin dii ráp kham chooen wan sùk khráp", "ยินดีรับคำเชิญวันศุกร์ครับ"),
 ("Chętnie przyjdę.", "yin dii pai khráp", "ยินดีไปครับ",
  "Chętnie przyjdę, o której zaczynamy?", "yin dii pai khráp rôoem kìi moong", "ยินดีไปครับ เริ่มกี่โมง"),
 ("Wchodzę w to.", "ao dûai", "เอาด้วย",
  "Wchodzę w to, widzimy się tam.", "ao dûai jôe kan thîi nân", "เอาด้วย เจอกันที่นั่น")),

("pytanie o zgodę na zdjęcie", "Small talk", "Rejestr",
 "świątynia, muzeum, cudza posesja",
 ("Czy wolno tu robić zdjęcia?", "thîi nîi à-nú-yâat hâi thàai rûup mǎi khráp", "ที่นี่อนุญาตให้ถ่ายรูปไหมครับ",
  "Czy wolno tu robić zdjęcia bez lampy?", "thàai rûup mâi chái fláet dâai mǎi khráp", "ถ่ายรูปไม่ใช้แฟลชได้ไหมครับ"),
 ("Można tu robić zdjęcia?", "thàai rûup dâai mǎi khráp", "ถ่ายรูปได้ไหมครับ",
  "Można tu robić zdjęcia z tobą?", "thàai rûup kàp khun dâai mǎi khráp", "ถ่ายรูปกับคุณได้ไหมครับ"),
 ("Mogę pstryknąć?", "thàai dâai pà", "ถ่ายได้ป่ะ",
  "Mogę pstryknąć jedno?", "thàai sák rûup dâai pà", "ถ่ายสักรูปได้ป่ะ")),
]

REG_LABEL = {"f": "formalny", "n": "neutralny", "p": "potoczny"}
REG_SLOT = {"f": 4, "n": 5, "p": 6}


def _build():
    out = []
    for msg in MESSAGES:
        opis, cat, sub, gdzie = msg[0], msg[1], msg[2], msg[3]
        variants = {"f": msg[4], "n": msg[5], "p": msg[6]}
        for code in ("f", "n", "p"):
            pl, ph, th, ex_pl, ex_ph, ex_th = variants[code]
            others = [c for c in ("f", "n", "p") if c != code]
            opis_others = "; ".join(
                "%s: „%s”" % (REG_LABEL[c], variants[c][1]) for c in others)
            if code == "f":
                gdzie_txt = "Tej wersji użyj tam, gdzie liczy się dystans: %s." % gdzie
            elif code == "n":
                gdzie_txt = ("Wersja domyślna — bezpieczna wobec obcych, kolegów z pracy "
                             "i obsługi. Od niej zaczynaj, jeśli nie masz pewności.")
            else:
                gdzie_txt = ("Wersja potoczna — tylko wśród bliskich znajomych i rówieśników. "
                             "Wobec urzędnika, klienta i osoby starszej zabrzmi lekceważąco.")
            note = ("REJESTR %s — ten sam komunikat („%s”) w trzech wersjach. "
                    "Pozostałe: %s. %s"
                    % (REG_LABEL[code].upper(), opis, opis_others, gdzie_txt))
            out.append((pl, ph, th, cat, sub, "sentence", 4 if code == "n" else 3,
                        code, note, "", (ex_pl, ex_ph, ex_th)))
    return out


CORE_REGISTER = _build()
