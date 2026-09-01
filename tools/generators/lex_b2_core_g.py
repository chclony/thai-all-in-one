# -*- coding: utf-8 -*-
"""Leksyka etapu 5 (B2) — czesc G.

Zakres: sytuacje awaryjne wymagajace precyzyjnej komunikacji. Wezwanie pomocy,
podanie lokalizacji, opis stanu poszkodowanego, wypadek drogowy, pozar, kradziez
i oszustwo, zaginiecie, awaria w mieszkaniu, kontakt z policja i ambasada.

Uwaga dydaktyczna: w sytuacji awaryjnej liczy sie kolejnosc informacji —
CO sie stalo, GDZIE, ILU ludzi, CZY sa ranni. Rekordy sa ulozone tak,
zeby dalo sie je zlozyc w te kolejnosc.

Format jak w lex_b2_core_a.py.
"""

CORE_G = [

# =====================================================================
# WEZWANIE POMOCY
# =====================================================================
("potrzebuję karetki, natychmiast", "khǎw rót phá-yaa-baan dùan khráp", "ขอรถพยาบาลด่วนครับ",
 "Awarie i pomoc", "Alarm", "sentence", 5, "n",
 "„dùan” = pilne. Powiedz je na początku, nie na końcu — skraca rozmowę o połowę.", "",
 ("Potrzebuję karetki, natychmiast, ktoś jest nieprzytomny.", "khǎw rót phá-yaa-baan dùan khráp mii khon mòt sà-tì", "ขอรถพยาบาลด่วนครับ มีคนหมดสติ")),
("proszę wezwać policję", "chûai rîak tam-rùat hâi nòi khráp", "ช่วยเรียกตำรวจให้หน่อยครับ",
 "Awarie i pomoc", "Alarm", "sentence", 5, "n", "", "",
 ("Proszę wezwać policję, doszło do wypadku.", "chûai rîak tam-rùat hâi nòi khráp mii ù-bàt-tì-hèet", "ช่วยเรียกตำรวจให้หน่อยครับ มีอุบัติเหตุ")),
("pali się", "fai mâi khráp", "ไฟไหม้ครับ", "Awarie i pomoc", "Alarm", "sentence", 5, "n",
 "Dwa słowa, które trzeba umieć bez zastanowienia. Krzycz je, nie tłumacz sytuacji.", "",
 ("Pali się na trzecim piętrze, wychodźcie!", "fai mâi chán sǎam khráp rîip àwk maa", "ไฟไหม้ชั้นสามครับ รีบออกมา")),
("jest wypadek", "mii ù-bàt-tì-hèet khráp", "มีอุบัติเหตุครับ", "Awarie i pomoc", "Alarm", "sentence", 5, "n", "", "",
 ("Jest wypadek na drodze przy świątyni.", "mii ù-bàt-tì-hèet bon thà-nǒn nâa wát khráp", "มีอุบัติเหตุบนถนนหน้าวัดครับ")),
("ktoś potrzebuje pomocy", "mii khon tâwng-kaan khwaam chûai lǔea khráp", "มีคนต้องการความช่วยเหลือครับ",
 "Awarie i pomoc", "Alarm", "sentence", 4, "n", "", "",
 ("Ktoś potrzebuje pomocy, leży przy przystanku.", "mii khon tâwng-kaan khwaam chûai lǔea nawn yùu thîi pâai rót khráp", "มีคนต้องการความช่วยเหลือ นอนอยู่ที่ป้ายรถครับ")),
("nie mówię dobrze po tajsku, ale to pilne", "phǒm phûut thai mâi khâwi dâai tàae rûeang dùan mâak khráp", "ผมพูดไทยไม่ค่อยได้ แต่เรื่องด่วนมากครับ",
 "Awarie i pomoc", "Alarm", "sentence", 4, "n",
 "Uprzedzenie o barierze językowej sprawia, że dyspozytor zwolni i będzie pytał krótko.", "",
 ("Nie mówię dobrze po tajsku, ale to pilne — proszę mówić wolno.", "phǒm phûut thai mâi khâwi dâai tàae dùan mâak khráp chûai phûut cháa cháa", "ผมพูดไทยไม่ค่อยได้ แต่ด่วนมากครับ ช่วยพูดช้าๆ")),

# =====================================================================
# PODANIE LOKALIZACJI
# =====================================================================
("jestem na rogu ulicy", "phǒm yùu trong hǔa mum thà-nǒn khráp", "ผมอยู่ตรงหัวมุมถนนครับ",
 "Awarie i pomoc", "Lokalizacja", "sentence", 4, "n", "", "",
 ("Jestem na rogu ulicy naprzeciwko banku.", "phǒm yùu trong hǔa mum thà-nǒn trong khâam thá-naa-khaan khráp", "ผมอยู่ตรงหัวมุมถนนตรงข้ามธนาคารครับ")),
("naprzeciwko jest sklep całodobowy", "trong khâam mii ráan sà-dùak súe khráp", "ตรงข้ามมีร้านสะดวกซื้อครับ",
 "Awarie i pomoc", "Lokalizacja", "sentence", 4, "n",
 "Punkt orientacyjny działa lepiej niż adres — tajskie numery domów bywają nieoczywiste.", "",
 ("Naprzeciwko jest sklep całodobowy z niebieskim szyldem.", "trong khâam mii ráan sà-dùak súe pâai sǐi náam ngoen khráp", "ตรงข้ามมีร้านสะดวกซื้อป้ายสีน้ำเงินครับ")),
("to boczna uliczka numer pięć", "pen sawi hâa khráp", "เป็นซอยห้าครับ", "Awarie i pomoc", "Lokalizacja", "sentence", 4, "n",
 "„sawi” to numerowana boczna uliczka. Bez niej lokalizacja w mieście jest bezużyteczna.", "",
 ("To boczna uliczka numer pięć, wjazd od głównej.", "pen sawi hâa khráp khâo jàak thà-nǒn yài", "เป็นซอยห้าครับ เข้าจากถนนใหญ่")),
("wyślę wam lokalizację z telefonu", "dǐao sòng phíkàt jàak muue-thǔe hâi khráp", "เดี๋ยวส่งพิกัดจากมือถือให้ครับ",
 "Awarie i pomoc", "Lokalizacja", "sentence", 4, "n",
 "„phíkàt” = współrzędne, lokalizacja. Najszybszy sposób, gdy nie znasz nazw ulic.", "",
 ("Wyślę wam lokalizację z telefonu, proszę o numer.", "dǐao sòng phíkàt jàak muue-thǔe hâi khráp khǎw boe thoo", "เดี๋ยวส่งพิกัดจากมือถือให้ครับ ขอเบอร์โทร")),
("jestem przy kilometrze dwudziestym", "phǒm yùu prà-maan kì-loo thîi yîi sìp khráp", "ผมอยู่ประมาณกิโลที่ยี่สิบครับ",
 "Awarie i pomoc", "Lokalizacja", "sentence", 3, "n", "", "",
 ("Jestem przy kilometrze dwudziestym, kierunek północ.", "phǒm yùu prà-maan kì-loo thîi yîi sìp mûng nǔea khráp", "ผมอยู่ประมาณกิโลที่ยี่สิบ มุ่งเหนือครับ")),
("budynek ma pięć pięter", "aa-khaan sǔung hâa chán khráp", "อาคารสูงห้าชั้นครับ", "Awarie i pomoc", "Lokalizacja", "sentence", 3, "n", "", "",
 ("Budynek ma pięć pięter, jestem na ostatnim.", "aa-khaan sǔung hâa chán khráp phǒm yùu chán bon sùt", "อาคารสูงห้าชั้นครับ ผมอยู่ชั้นบนสุด")),
("brama jest zamknięta, przyjdę otworzyć", "prà-tuu lák yùu dǐao pai pòoet hâi khráp", "ประตูล็อกอยู่ เดี๋ยวไปเปิดให้ครับ",
 "Awarie i pomoc", "Lokalizacja", "sentence", 3, "n", "", "",
 ("Brama jest zamknięta, przyjdę otworzyć od razu.", "prà-tuu lák yùu dǐao pai pòoet hâi than-thii khráp", "ประตูล็อกอยู่ เดี๋ยวไปเปิดให้ทันทีครับ")),

# =====================================================================
# STAN POSZKODOWANEGO
# =====================================================================
("jest przytomny, ale słaby", "yang mii sà-tì tàae àwn phliia khráp", "ยังมีสติแต่อ่อนเพลียครับ",
 "Zdrowie", "Ratunek", "sentence", 4, "n",
 "„mii sà-tì” = przytomny. Pierwsza informacja, o którą pyta dyspozytor.", "",
 ("Jest przytomny, ale słaby i blady.", "yang mii sà-tì tàae àwn phliia láe nâa sîit khráp", "ยังมีสติแต่อ่อนเพลียและหน้าซีดครับ")),
("stracił przytomność", "khǎo mòt sà-tì khráp", "เขาหมดสติครับ", "Zdrowie", "Ratunek", "sentence", 4, "n", "", "",
 ("Stracił przytomność jakieś dwie minuty temu.", "khǎo mòt sà-tì prà-maan sǎwng naa-thii thîi láew khráp", "เขาหมดสติประมาณสองนาทีที่แล้วครับ")),
("oddycha samodzielnie", "yang hǎai jai eeng dâai khráp", "ยังหายใจเองได้ครับ", "Zdrowie", "Ratunek", "sentence", 4, "n", "", "",
 ("Oddycha samodzielnie, ale bardzo płytko.", "yang hǎai jai eeng dâai tàae bao mâak khráp", "ยังหายใจเองได้แต่เบามากครับ")),
("mocno krwawi", "lûeat àwk mâak khráp", "เลือดออกมากครับ", "Zdrowie", "Ratunek", "sentence", 4, "n", "", "",
 ("Mocno krwawi z nogi, uciskam ranę.", "lûeat àwk thîi khǎa mâak khráp phǒm kòt phlǎe wái", "เลือดออกที่ขามากครับ ผมกดแผลไว้")),
("chyba ma złamaną nogę", "khǎa khǎo nâa jà hàk khráp", "ขาเขาน่าจะหักครับ", "Zdrowie", "Ratunek", "sentence", 4, "n", "", "",
 ("Chyba ma złamaną nogę, nie może wstać.", "khǎa khǎo nâa jà hàk khráp lúk mâi dâai", "ขาเขาน่าจะหักครับ ลุกไม่ได้")),
("nie ruszałem go", "phǒm mâi dâai yáai tua khǎo khráp", "ผมไม่ได้ย้ายตัวเขาครับ", "Zdrowie", "Ratunek", "sentence", 3, "n",
 "Ważna informacja przy urazach kręgosłupa. Powiedz to dyspozytorowi bez pytania.", "",
 ("Nie ruszałem go, leży tak jak upadł.", "phǒm mâi dâai yáai tua khǎo khráp khǎo nawn yàang thîi lóm", "ผมไม่ได้ย้ายตัวเขาครับ เขานอนอย่างที่ล้ม")),
("jest uczulony na antybiotyk", "khǎo pháe yaa khâa chúea khráp", "เขาแพ้ยาฆ่าเชื้อครับ", "Zdrowie", "Ratunek", "sentence", 3, "f", "", "",
 ("Jest uczulony na antybiotyk, mam to zapisane.", "khǎo pháe yaa khâa chúea khráp phǒm mii jòt wái", "เขาแพ้ยาฆ่าเชื้อครับ ผมมีจดไว้")),
("bierze leki na serce", "khǎo kin yaa rôhk hǔa-jai yùu khráp", "เขากินยาโรคหัวใจอยู่ครับ",
 "Zdrowie", "Ratunek", "sentence", 3, "f", "", "",
 ("Bierze leki na serce, opakowanie mam przy sobie.", "khǎo kin yaa rôhk hǔa-jai yùu khráp klàwng yaa yùu kàp phǒm", "เขากินยาโรคหัวใจอยู่ครับ กล่องยาอยู่กับผม")),
("umiem udzielić pierwszej pomocy", "phǒm pá-thǒm phá-yaa-baan pen khráp", "ผมปฐมพยาบาลเป็นครับ",
 "Zdrowie", "Ratunek", "sentence", 3, "f", "", "",
 ("Umiem udzielić pierwszej pomocy, mówcie co robić.", "phǒm pá-thǒm phá-yaa-baan pen khráp bàwk maa wâa tâwng tham à-rai", "ผมปฐมพยาบาลเป็นครับ บอกมาว่าต้องทำอะไร")),
("proszę mnie prowadzić przez telefon", "chûai bàwk phǒm thaang thoo-rá-sàp khráp", "ช่วยบอกผมทางโทรศัพท์ครับ",
 "Awarie i pomoc", "Ratunek", "sentence", 3, "n", "", "",
 ("Proszę mnie prowadzić przez telefon, zostaję przy nim.", "chûai bàwk phǒm thaang thoo-rá-sàp khráp phǒm yùu kàp khǎo", "ช่วยบอกผมทางโทรศัพท์ครับ ผมอยู่กับเขา")),

# =====================================================================
# WYPADEK DROGOWY
# =====================================================================
("zderzyły się dwa motocykle", "mawtoesai chon kan sǎwng khan khráp", "มอเตอร์ไซค์ชนกันสองคันครับ",
 "Transport", "Wypadek", "sentence", 4, "n", "", "",
 ("Zderzyły się dwa motocykle na skrzyżowaniu.", "mawtoesai chon kan sǎwng khan trong sìi yâek khráp", "มอเตอร์ไซค์ชนกันสองคันตรงสี่แยกครับ")),
("samochód wjechał w barierkę", "rót chon rao kân khráp", "รถชนราวกั้นครับ", "Transport", "Wypadek", "sentence", 3, "n", "", "",
 ("Samochód wjechał w barierkę, kierowca jest w środku.", "rót chon rao kân khráp khon khàp yang yùu nai rót", "รถชนราวกั้นครับ คนขับยังอยู่ในรถ")),
("są ranni, dwie osoby", "mii khon bàat jèp sǎwng khon khráp", "มีคนบาดเจ็บสองคนครับ",
 "Awarie i pomoc", "Wypadek", "sentence", 4, "n",
 "Podaj liczbę rannych zawsze — od niej zależy, ile karetek wyjedzie.", "",
 ("Są ranni, dwie osoby, jedna nie może wstać.", "mii khon bàat jèp sǎwng khon khráp khon nùeng lúk mâi dâai", "มีคนบาดเจ็บสองคนครับ คนหนึ่งลุกไม่ได้")),
("nikomu nic się nie stało", "mâi mii khrai bàat jèp khráp", "ไม่มีใครบาดเจ็บครับ", "Awarie i pomoc", "Wypadek", "sentence", 4, "n", "", "",
 ("Nikomu nic się nie stało, tylko szkody w aucie.", "mâi mii khrai bàat jèp khráp sǐa hǎai chà-phǎw rót", "ไม่มีใครบาดเจ็บครับ เสียหายเฉพาะรถ")),
("droga jest zablokowana", "thà-nǒn thùuk pìt khráp", "ถนนถูกปิดครับ", "Transport", "Wypadek", "sentence", 3, "n", "", "",
 ("Droga jest zablokowana w obu kierunkach.", "thà-nǒn thùuk pìt thóng sǎwng fàng khráp", "ถนนถูกปิดทั้งสองฝั่งครับ")),
("czekam na policję na miejscu", "phǒm raw tam-rùat yùu thîi kòet hèet khráp", "ผมรอตำรวจอยู่ที่เกิดเหตุครับ",
 "Awarie i pomoc", "Wypadek", "sentence", 3, "n",
 "„thîi kòet hèet” = miejsce zdarzenia. Zwrot z języka policyjnego, przydaje się przy zgłoszeniu.", "",
 ("Czekam na policję na miejscu, nikt nie odjechał.", "phǒm raw tam-rùat yùu thîi kòet hèet khráp mâi mii khrai pai nǎi", "ผมรอตำรวจอยู่ที่เกิดเหตุครับ ไม่มีใครไปไหน")),
("mam nagranie z kamery", "phǒm mii khlíp jàak klâwng nâa rót khráp", "ผมมีคลิปจากกล้องหน้ารถครับ",
 "Transport", "Wypadek", "sentence", 3, "n", "", "",
 ("Mam nagranie z kamery samochodowej, mogę pokazać.", "phǒm mii khlíp jàak klâwng nâa rót khǎw hâi duu khráp", "ผมมีคลิปจากกล้องหน้ารถ ขอให้ดูครับ")),
("proszę o dane ubezpieczenia drugiego kierowcy", "khǎw khâw-muun prà-kan khǎwng khon khàp ìik fàai khráp", "ขอข้อมูลประกันของคนขับอีกฝ่ายครับ",
 "Transport", "Wypadek", "sentence", 3, "f", "", "",
 ("Proszę o dane ubezpieczenia drugiego kierowcy do zgłoszenia.", "khǎw khâw-muun prà-kan khǎwng ìik fàai phûea jâeng khleem khráp", "ขอข้อมูลประกันของอีกฝ่ายเพื่อแจ้งเคลมครับ")),
("nie przyznaję się do winy przed policją", "phǒm khǎw yang mâi ráp phìt jon kwàa tam-rùat maa khráp", "ผมขอยังไม่รับผิดจนกว่าตำรวจมาครับ",
 "Transport", "Wypadek", "sentence", 3, "f",
 "W Tajlandii ustne przyznanie się na miejscu bywa traktowane jako rozstrzygające. Poczekaj na policję i ubezpieczyciela.", "",
 ("Nie przyznaję się do winy przed policją, poczekajmy.", "phǒm khǎw yang mâi ráp phìt jon kwàa tam-rùat maa khráp raw kàwn", "ผมขอยังไม่รับผิดจนกว่าตำรวจมาครับ รอก่อน")),

# =====================================================================
# KRADZIEZ, OSZUSTWO, ZAGINIECIE
# =====================================================================
("okradziono mnie", "phǒm thùuk khà-mooi khráp", "ผมถูกขโมยครับ", "Awarie i pomoc", "Kradzież", "sentence", 4, "n", "", "",
 ("Okradziono mnie w autobusie, zginął portfel.", "phǒm thùuk khà-mooi bon rót mee krà-pǎo tang hǎai khráp", "ผมถูกขโมยบนรถเมล์ กระเป๋าตังค์หายครับ")),
("chcę złożyć zawiadomienie", "phǒm yàak jâeng khwaam khráp", "ผมอยากแจ้งความครับ",
 "Awarie i pomoc", "Kradzież", "sentence", 4, "f",
 "„jâeng khwaam” = złożyć doniesienie na policji. Potrzebne również do ubezpieczenia.", "",
 ("Chcę złożyć zawiadomienie o kradzieży telefonu.", "phǒm yàak jâeng khwaam rûeang muue-thǔe thùuk khà-mooi khráp", "ผมอยากแจ้งความเรื่องมือถือถูกขโมยครับ")),
("proszę o kopię protokołu", "khǎw sǎm-nao bai jâeng khwaam khráp", "ขอสำเนาใบแจ้งความครับ",
 "Awarie i pomoc", "Kradzież", "sentence", 3, "f", "", "",
 ("Proszę o kopię protokołu dla ubezpieczyciela.", "khǎw sǎm-nao bai jâeng khwaam hâi bɔɔ-rí-sàt prà-kan khráp", "ขอสำเนาใบแจ้งความให้บริษัทประกันครับ")),
("to było około godziny drugiej", "prà-maan bàai sǎwng moong khráp", "ประมาณบ่ายสองโมงครับ",
 "Czas i daty", "Kradzież", "sentence", 3, "n", "", "",
 ("To było około godziny drugiej po południu.", "hèet kòet prà-maan bàai sǎwng moong khráp", "เหตุเกิดประมาณบ่ายสองโมงครับ")),
("mężczyzna w czerwonej koszulce", "phûu chaai sûea sǐi daaeng khráp", "ผู้ชายเสื้อสีแดงครับ",
 "Ludzie i rodzina", "Kradzież", "sentence", 3, "n",
 "Opisuj ubranie i wzrost, nie twarz — to działa najlepiej przy szybkim poszukiwaniu.", "",
 ("Mężczyzna w czerwonej koszulce, wysoki, na motocyklu.", "phûu chaai sûea sǐi daaeng tua sǔung khìi mawtoesai khráp", "ผู้ชายเสื้อสีแดงตัวสูงขี่มอเตอร์ไซค์ครับ")),
("chyba padłem ofiarą oszustwa", "phǒm nâa jà thùuk lòhk khráp", "ผมน่าจะถูกหลอกครับ",
 "Awarie i pomoc", "Oszustwo", "sentence", 4, "n", "", "",
 ("Chyba padłem ofiarą oszustwa, przelałem zaliczkę.", "phǒm nâa jà thùuk lòhk khráp phǒm oon mát jam pai láew", "ผมน่าจะถูกหลอกครับ ผมโอนมัดจำไปแล้ว")),
("ktoś podszył się pod bank", "mii khon plaawm pen thá-naa-khaan khráp", "มีคนปลอมเป็นธนาคารครับ",
 "Awarie i pomoc", "Oszustwo", "sentence", 3, "n",
 "Telefoniczne oszustwa podszywające się pod urzędy są w Tajlandii bardzo częste. Nikt oficjalny nie prosi o hasło.", "",
 ("Ktoś podszył się pod bank i prosił o hasło.", "mii khon plaawm pen thá-naa-khaan khǎw rá-hàt phàan khráp", "มีคนปลอมเป็นธนาคารขอรหัสผ่านครับ")),
("proszę zablokować moje konto", "chûai à-yàt ban-chii phǒm dûai khráp", "ช่วยอายัดบัญชีผมด้วยครับ",
 "Zakupy i pieniądze", "Oszustwo", "sentence", 3, "f",
 "„à-yàt” = zablokować środki. Jedno słowo, które w kryzysie ratuje pieniądze.", "",
 ("Proszę zablokować moje konto natychmiast.", "chûai à-yàt ban-chii phǒm than-thii dûai khráp", "ช่วยอายัดบัญชีผมทันทีด้วยครับ")),
("zgubiło się dziecko", "dèk hǎai khráp", "เด็กหายครับ", "Awarie i pomoc", "Zaginięcie", "sentence", 3, "n", "", "",
 ("Zgubiło się dziecko, pięć lat, w niebieskiej koszulce.", "dèk hǎai khráp aa-yú hâa khùap sài sûea sǐi fáa", "เด็กหายครับ อายุห้าขวบใส่เสื้อสีฟ้า")),
("ostatni raz widziałem go przy wejściu", "hěn khráng sùt tháai trong thaang khâo khráp", "เห็นครั้งสุดท้ายตรงทางเข้าครับ",
 "Awarie i pomoc", "Zaginięcie", "sentence", 3, "n", "", "",
 ("Ostatni raz widziałem go przy wejściu dziesięć minut temu.", "hěn khráng sùt tháai trong thaang khâo sìp naa-thii thîi láew khráp", "เห็นครั้งสุดท้ายตรงทางเข้าสิบนาทีที่แล้วครับ")),
("proszę ogłosić to przez głośniki", "chûai prà-kàat thaang lam-phoong dûai khráp", "ช่วยประกาศทางลำโพงด้วยครับ",
 "Awarie i pomoc", "Zaginięcie", "sentence", 3, "n", "", "",
 ("Proszę ogłosić to przez głośniki w całym centrum.", "chûai prà-kàat thaang lam-phoong thûa hâang dûai khráp", "ช่วยประกาศทางลำโพงทั่วห้างด้วยครับ")),

# =====================================================================
# AWARIA W MIESZKANIU
# =====================================================================
("czuć gaz", "dâi klìn kâet khráp", "ได้กลิ่นแก๊สครับ", "Awarie i pomoc", "Awaria", "sentence", 4, "n",
 "Przy zapachu gazu nie włączaj światła ani wentylatora. Zgłoś i wyjdź.", "",
 ("Czuć gaz w kuchni, wyłączyłem butlę.", "dâi klìn kâet nai khrua khráp phǒm pìt thǎng láew", "ได้กลิ่นแก๊สในครัวครับ ผมปิดถังแล้ว")),
("zalało mieszkanie", "náam thûam hâwng khráp", "น้ำท่วมห้องครับ", "Awarie i pomoc", "Awaria", "sentence", 4, "n", "", "",
 ("Zalało mieszkanie, woda leci od sąsiada z góry.", "náam thûam hâwng khráp náam maa jàak hâwng chán bon", "น้ำท่วมห้องครับ น้ำมาจากห้องชั้นบน")),
("nie ma prądu w całym budynku", "fai dàp thóng aa-khaan khráp", "ไฟดับทั้งอาคารครับ",
 "Awarie i pomoc", "Awaria", "sentence", 4, "n", "", "",
 ("Nie ma prądu w całym budynku od godziny.", "fai dàp thóng aa-khaan maa nùeng chûa-moong láew khráp", "ไฟดับทั้งอาคารมาหนึ่งชั่วโมงแล้วครับ")),
("gdzie jest główny zawór wody?", "wáan náam làk yùu thîi nǎi khráp", "วาล์วน้ำหลักอยู่ที่ไหนครับ",
 "Dom i codzienność", "Awaria", "sentence", 3, "n", "", "",
 ("Gdzie jest główny zawór wody, muszę zakręcić?", "wáan náam làk yùu thîi nǎi khráp phǒm tâwng pìt", "วาล์วน้ำหลักอยู่ที่ไหนครับ ผมต้องปิด")),
("proszę o technika jeszcze dziś", "khǎw châang maa wan níi loei dâai mǎi khráp", "ขอช่างมาวันนี้เลยได้ไหมครับ",
 "Dom i codzienność", "Awaria", "sentence", 4, "n", "", "",
 ("Proszę o technika jeszcze dziś, to nie może czekać.", "khǎw châang maa wan níi loei dâai mǎi khráp raw mâi dâai", "ขอช่างมาวันนี้เลยได้ไหมครับ รอไม่ได้")),
("utknąłem w windzie", "phǒm tìt yùu nai líf khráp", "ผมติดอยู่ในลิฟต์ครับ", "Awarie i pomoc", "Awaria", "sentence", 3, "n", "", "",
 ("Utknąłem w windzie między drugim a trzecim piętrem.", "phǒm tìt yùu nai líf rá-wàang chán sǎwng kàp sǎam khráp", "ผมติดอยู่ในลิฟต์ระหว่างชั้นสองกับสามครับ")),
("zatrzasnąłem klucze w środku", "phǒm luem kun-jae wái khâang nai khráp", "ผมลืมกุญแจไว้ข้างในครับ",
 "Dom i codzienność", "Awaria", "sentence", 3, "n", "", "",
 ("Zatrzasnąłem klucze w środku, potrzebuję ślusarza.", "phǒm luem kun-jae wái khâang nai khráp tâwng-kaan châang kun-jae", "ผมลืมกุญแจไว้ข้างในครับ ต้องการช่างกุญแจ")),

# =====================================================================
# AMBASADA I POMOC PRAWNA
# =====================================================================
("chcę skontaktować się z ambasadą", "phǒm yàak tìt tàw sà-thǎan thûut khráp", "ผมอยากติดต่อสถานทูตครับ",
 "Awarie i pomoc", "Ambasada", "sentence", 4, "f", "", "",
 ("Chcę skontaktować się z ambasadą mojego kraju.", "phǒm yàak tìt tàw sà-thǎan thûut khǎwng prà-thêet phǒm khráp", "ผมอยากติดต่อสถานทูตของประเทศผมครับ")),
("straciłem paszport", "nǎng-sǔe doen thaang phǒm hǎai khráp", "หนังสือเดินทางผมหายครับ",
 "Awarie i pomoc", "Ambasada", "sentence", 4, "f",
 "„nǎng-sǔe doen thaang” to oficjalna nazwa paszportu. „phàat-sà-pàwt” usłyszysz w mowie potocznej.", "księga podróżna",
 ("Straciłem paszport i potrzebuję dokumentu zastępczego.", "nǎng-sǔe doen thaang phǒm hǎai tâwng-kaan èek-kà-sǎan chûa khraao khráp", "หนังสือเดินทางผมหายต้องการเอกสารชั่วคราวครับ")),
("potrzebuję tłumacza", "phǒm tâwng-kaan lâam khráp", "ผมต้องการล่ามครับ", "Awarie i pomoc", "Ambasada", "sentence", 4, "f",
 "„lâam” = tłumacz ustny. Masz prawo o niego poprosić przy czynnościach urzędowych.", "",
 ("Potrzebuję tłumacza, zanim cokolwiek podpiszę.", "phǒm tâwng-kaan lâam kàwn jà sen à-rai khráp", "ผมต้องการล่ามก่อนจะเซ็นอะไรครับ")),
("nie podpiszę, czego nie rozumiem", "phǒm mâi sen sìng thîi phǒm mâi khâo-jai khráp", "ผมไม่เซ็นสิ่งที่ผมไม่เข้าใจครับ",
 "Awarie i pomoc", "Ambasada", "sentence", 3, "f",
 "Zdanie warte wyuczenia na pamięć. Wypowiedziane spokojnie jest w pełni akceptowane.", "",
 ("Nie podpiszę, czego nie rozumiem — proszę o tłumaczenie.", "phǒm mâi sen sìng thîi phǒm mâi khâo-jai khráp khǎw kham plae", "ผมไม่เซ็นสิ่งที่ผมไม่เข้าใจครับ ขอคำแปล")),
("chcę zadzwonić do rodziny", "khǎw thoo hǎa khrâwp khrua khráp", "ขอโทรหาครอบครัวครับ",
 "Awarie i pomoc", "Ambasada", "sentence", 4, "n", "", "",
 ("Chcę zadzwonić do rodziny, żeby wiedzieli, że żyję.", "khǎw thoo hǎa khrâwp khrua hâi khǎo raw sà-baai jai khráp", "ขอโทรหาครอบครัวให้เขารู้ว่าสบายดีครับ")),
("proszę zapisać mój numer kontaktowy", "jòt boe tìt tàw khǎwng phǒm wái dûai khráp", "จดเบอร์ติดต่อของผมไว้ด้วยครับ",
 "Awarie i pomoc", "Ambasada", "sentence", 3, "n", "", "",
 ("Proszę zapisać mój numer kontaktowy i numer do żony.", "jòt boe tìt tàw khǎwng phǒm kàp boe phan-rá-yaa wái dûai khráp", "จดเบอร์ติดต่อของผมกับเบอร์ภรรยาไว้ด้วยครับ")),
]
