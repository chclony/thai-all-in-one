# -*- coding: utf-8 -*-
"""Dialogi etapu 4 (B1) — czesc B.

Zakres: wynajem mieszkania i naprawy, technologia, podroze po Tajlandii,
relacje i konflikty, zdrowie i dokladniejszy opis objawow.

Krotka: (tytul, sytuacja, poziom, rola A, rola B, kwestie, notatka)
"""

DIALOGUES_B1_B = [

("Oględziny mieszkania przed wynajmem", "Dom i codzienność", "B1", "Najemca", "Właściciel", [
 ("A", "Szukam mieszkania do wynajęcia.", "phǒm hǎa hâwng châo khráp", "ผมหาห้องเช่าครับ"),
 ("B", "Na ile osób?", "yùu kìi khon khráp", "อยู่กี่คนครับ"),
 ("A", "Sam. Ile wynosi czynsz?", "khon diao khráp khâa châo duean lá thâo-rài", "คนเดียวครับ ค่าเช่าเดือนละเท่าไหร่"),
 ("B", "Dwanaście tysięcy.", "nùeng mùen sǎwng phan khráp", "หนึ่งหมื่นสองพันครับ"),
 ("A", "Czy w cenie są media?", "ruam khâa náam khâa fai mǎi khráp", "รวมค่าน้ำค่าไฟไหมครับ"),
 ("B", "Płatne osobno.", "jàai yâek khráp", "จ่ายแยกครับ"),
 ("A", "Jaka jest kaucja?", "khâa mát-jam thâo-rài khráp", "ค่ามัดจำเท่าไหร่ครับ"),
 ("B", "Za dwa miesiące.", "sǎwng duean khráp", "สองเดือนครับ"),
 ("A", "Czy czynsz można negocjować?", "lót khâa châo dâai mǎi khráp", "ลดค่าเช่าได้ไหมครับ"),
 ("B", "Trochę mogę spuścić.", "lót hâi nít nòi dâai khráp", "ลดให้นิดหน่อยได้ครับ"),
], "„khâa náam khâa fai” to stała para: woda i prąd. Tajowie wymieniają je zawsze razem."),

("Podpisywanie umowy najmu", "Dom i codzienność", "B1", "Najemca", "Właściciel", [
 ("A", "Na jak długo jest umowa?", "sǎn-yaa kìi duean khráp", "สัญญากี่เดือนครับ"),
 ("B", "Na rok.", "nùeng pii khráp", "หนึ่งปีครับ"),
 ("A", "A jeśli wyjadę wcześniej?", "thâa yáai àwk kàwn lâ khráp", "ถ้าย้ายออกก่อนล่ะครับ"),
 ("B", "Trzeba zgłosić miesiąc wcześniej.", "tâwng jâeng lûang nâa nùeng duean khráp", "ต้องแจ้งล่วงหน้าหนึ่งเดือนครับ"),
 ("A", "Kiedy dostanę kaucję z powrotem?", "dâai khâa mát-jam khǒen mûea-rài khráp", "ได้ค่ามัดจำคืนเมื่อไหร่ครับ"),
 ("B", "W ciągu miesiąca po wyprowadzce.", "phaai nai nùeng duean lǎng yáai àwk khráp", "ภายในหนึ่งเดือนหลังย้ายออกครับ"),
 ("A", "Chciałbym poznać szczegóły.", "phǒm yàak sâap rai-lá-ìat khráp", "ผมอยากทราบรายละเอียดครับ"),
 ("B", "Wszystko jest w umowie.", "yùu nai sǎn-yaa tháng mòt khráp", "อยู่ในสัญญาทั้งหมดครับ"),
], "„yáai àwk” = wyprowadzić się, „yáai khâo” = wprowadzić się. Ta para wraca w każdej rozmowie o wynajmie."),

("Awaria klimatyzacji", "Dom i codzienność", "B1", "Najemca", "Właściciel", [
 ("A", "Klimatyzacja nie działa.", "âae sǐa khráp", "แอร์เสียครับ"),
 ("B", "Od kiedy?", "tâng tàae mûea-rài khráp", "ตั้งแต่เมื่อไหร่ครับ"),
 ("A", "Od wczoraj wieczorem.", "tâng tàae mûea waan tawn yen khráp", "ตั้งแต่เมื่อวานตอนเย็นครับ"),
 ("B", "Wyśle pana technika.", "dǐao hâi châang pai duu khráp", "เดี๋ยวให้ช่างไปดูครับ"),
 ("A", "Czy może przyjść dzisiaj?", "maa wan níi dâai mǎi khráp", "มาวันนี้ได้ไหมครับ"),
 ("B", "Po południu.", "tawn bàai khráp", "ตอนบ่ายครับ"),
 ("A", "Proszę uprzedzić przed przyjściem.", "chûai thoo maa kàwn maa ná khráp", "ช่วยโทรมาก่อนมานะครับ"),
 ("B", "Dobrze. Kto pokrywa koszt?", "dâai khráp láew khrai àwk khâa sâwm", "ได้ครับ แล้วใครออกค่าซ่อม"),
 ("A", "To się zepsuło samo.", "man sǐa eeng khráp", "มันเสียเองครับ"),
 ("B", "Rozumiem, pokryję to.", "khâo-jai khráp phǒm àwk hâi", "เข้าใจครับ ผมออกให้"),
], "„sǐa eeng” = zepsuło się samo. To zdanie decyduje o tym, kto zapłaci za naprawę."),

("Zatkany odpływ", "Dom i codzienność", "B1", "Najemca", "Technik", [
 ("A", "Zatkał się odpływ.", "thâw tan khráp", "ท่อตันครับ"),
 ("B", "W łazience czy w kuchni?", "nai hâwng náam rǔe nai khrua khráp", "ในห้องน้ำหรือในครัวครับ"),
 ("A", "W łazience.", "nai hâwng náam khráp", "ในห้องน้ำครับ"),
 ("B", "Woda w ogóle nie schodzi?", "náam mâi long loei rǒe khráp", "น้ำไม่ลงเลยหรือครับ"),
 ("A", "Schodzi bardzo wolno.", "long cháa mâak khráp", "ลงช้ามากครับ"),
 ("B", "Sprawdzę to teraz.", "dǐao duu hâi loei khráp", "เดี๋ยวดูให้เลยครับ"),
 ("A", "Ile będzie kosztować naprawa?", "khâa sâwm thâo-rài khráp", "ค่าซ่อมเท่าไหร่ครับ"),
 ("B", "Najpierw obejrzę.", "khǎw duu kàwn khráp", "ขอดูก่อนครับ"),
], "„châang” to fachowiec każdej specjalności: hydraulik, elektryk, mechanik."),

("Wolny internet", "Dom i codzienność", "B1", "Klient", "Obsługa techniczna", [
 ("A", "Internet jest bardzo wolny.", "nét cháa mâak khráp", "เน็ตช้ามากครับ"),
 ("B", "Restartował pan router?", "lawng rii-sét ráo-tôoe rǔe yang khráp", "ลองรีเซ็ตเราเตอร์หรือยังครับ"),
 ("A", "Próbowałem, ale nie pomogło.", "lawng láew tàae yang mǔean doem khráp", "ลองแล้วแต่ยังเหมือนเดิมครับ"),
 ("B", "Ile urządzeń jest podłączonych?", "tàw kìi khrûeang khráp", "ต่อกี่เครื่องครับ"),
 ("A", "Trzy.", "sǎam khrûeang khráp", "สามเครื่องครับ"),
 ("B", "Sprawdzę sygnał w systemie.", "dǐao chék sǎn-yaan nai rá-bòp khráp", "เดี๋ยวเช็คสัญญาณในระบบครับ"),
 ("A", "Chciałbym zgłosić to oficjalnie.", "phǒm yàak jâeng rûeang níi pen thaang kaan khráp", "ผมอยากแจ้งเรื่องนี้เป็นทางการครับ"),
 ("B", "Otworzę zgłoszenie.", "dǐao pòoet khêet hâi khráp", "เดี๋ยวเปิดเคสให้ครับ"),
], "„mǔean doem” = tak jak było, bez zmiany. Bardzo przydatne przy opisie usterki."),

("Zablokowane konto w aplikacji", "Dom i codzienność", "B1", "Użytkownik", "Obsługa", [
 ("A", "Konto zostało zablokowane.", "ban-chii thùuk láwk khráp", "บัญชีถูกล็อคครับ"),
 ("B", "Pamięta pan hasło?", "jam phàat-wòet dâai mǎi khráp", "จำพาสเวิร์ดได้ไหมครับ"),
 ("A", "Zapomniałem hasła.", "phǒm luem phàat-wòet khráp", "ผมลืมพาสเวิร์ดครับ"),
 ("B", "Wyślemy kod na maila.", "dǐao sòng roo-hàt thaang ii-meew khráp", "เดี๋ยวส่งรหัสทางอีเมลครับ"),
 ("A", "Nie dostałem kodu.", "mâi dâi ráp roo-hàt khráp", "ไม่ได้รับรหัสครับ"),
 ("B", "Proszę sprawdzić folder ze spamem.", "lawng duu nai sà-pam duu khráp", "ลองดูในสแปมดูครับ"),
 ("A", "Już widzę. Dziękuję.", "hěn láew khráp khàwp-khun", "เห็นแล้วครับ ขอบคุณ"),
 ("B", "Cała przyjemność moja.", "yin dii khráp", "ยินดีครับ"),
], "„thùuk” tworzy stronę bierną i niesie odcień czegoś niepożądanego: thùuk láwk, thùuk pràp."),

("Doładowanie telefonu", "Dom i codzienność", "B1", "Klient", "Sprzedawca", [
 ("A", "Chciałbym doładować telefon.", "phǒm yàak toem ngoen mue-thǔe khráp", "ผมอยากเติมเงินมือถือครับ"),
 ("B", "Ile chce pan doładować?", "toem thâo-rài khráp", "เติมเท่าไหร่ครับ"),
 ("A", "Trzysta bahtów.", "sǎam ráwi bàat khráp", "สามร้อยบาทครับ"),
 ("B", "Jaki numer?", "boe à-rai khráp", "เบอร์อะไรครับ"),
 ("A", "Podam za chwilę.", "dǐao bàwk khráp", "เดี๋ยวบอกครับ"),
 ("B", "Chce pan też pakiet internetu?", "ao pháek-kèet nét dûai mǎi khráp", "เอาแพ็คเกจเน็ตด้วยไหมครับ"),
 ("A", "Tak, na trzydzieści dni.", "ao khráp sǎam sìp wan", "เอาครับ สามสิบวัน"),
 ("B", "Gotowe. Można płacić kodem.", "riap ráwi khráp sà-kaen jàai dâai", "เรียบร้อยครับ สแกนจ่ายได้"),
], "Skanowanie kodu QR to w Tajlandii domyślna metoda płatności, częstsza niż karta."),

("Dojazd na wyspę", "Transport", "B1", "Turysta", "Kasjer", [
 ("A", "Jak najlepiej dostać się na wyspę?", "pai kàw yang-ngai dii thîi sùt khráp", "ไปเกาะยังไงดีที่สุดครับ"),
 ("B", "Promem, odpływa rano.", "nâng ruea khráp àwk tawn cháo", "นั่งเรือครับ ออกตอนเช้า"),
 ("A", "O której odpływa?", "ruea àwk kìi moong khráp", "เรือออกกี่โมงครับ"),
 ("B", "O ósmej.", "pàet moong cháo khráp", "แปดโมงเช้าครับ"),
 ("A", "Ile trwa podróż?", "chái wee-laa dòoen thaang kìi chûa moong khráp", "ใช้เวลาเดินทางกี่ชั่วโมงครับ"),
 ("B", "Dwie i pół godziny.", "sǎwng chûa moong khrûeng khráp", "สองชั่วโมงครึ่งครับ"),
 ("A", "Czy bilet trzeba kupić wcześniej?", "tâwng sǔe tǔa lûang nâa mǎi khráp", "ต้องซื้อตั๋วล่วงหน้าไหมครับ"),
 ("B", "Lepiej wcześniej, w weekend jest tłoczno.", "sǔe lûang nâa dii kwàa khráp sǎo aa-thít khon yóe", "ซื้อล่วงหน้าดีกว่าครับ เสาร์อาทิตย์คนเยอะ"),
 ("A", "To poproszę dwa na jutro.", "ngán khǎw sǎwng bai phrûng níi khráp", "งั้นขอสองใบพรุ่งนี้ครับ"),
 ("B", "Proszę bardzo.", "dâai khráp", "ได้ครับ"),
], "„kàw” = wyspa. Nazwy wysp zawsze zaczynają się tym słowem: Kàw Sà-mǔi, Kàw Chaang."),

("Targowanie się o kurs", "Transport", "B1", "Pasażer", "Kierowca", [
 ("A", "Ile kosztuje kurs do centrum?", "khâa rót khâo mueang thâo-rài khráp", "ค่ารถเข้าเมืองเท่าไหร่ครับ"),
 ("B", "Czterysta bahtów.", "sìi ráwi bàat khráp", "สี่ร้อยบาทครับ"),
 ("A", "To za drogo, dziękuję.", "phaeng koen pai khráp khàwp-khun", "แพงเกินไปครับ ขอบคุณ"),
 ("B", "To ile pan da?", "hâi thâo-rài khráp", "ให้เท่าไหร่ครับ"),
 ("A", "Czy może pan włączyć taksometr?", "kòt mí-tôoe dûai dâai mǎi khráp", "กดมิเตอร์ด้วยได้ไหมครับ"),
 ("B", "O tej porze są korki.", "chûang níi rót tìt khráp", "ช่วงนี้รถติดครับ"),
 ("A", "Rozumiem, ale wolę licznik.", "khâo-jai khráp tàae khǎw mí-tôoe dii kwàa", "เข้าใจครับ แต่ขอมิเตอร์ดีกว่า"),
 ("B", "Dobrze, wsiadamy.", "dâai khráp khûen loei", "ได้ครับ ขึ้นเลย"),
], "Odejście z uśmiechem i podziękowaniem działa lepiej niż spór. Zachowanie spokoju to tu realna przewaga."),

("Zgubienie drogi", "Miejsca i orientacja", "B1", "Turysta", "Przechodzień", [
 ("A", "Przepraszam, zgubiłem się.", "khǎw-thôot khráp phǒm lǒng thaang", "ขอโทษครับ ผมหลงทาง"),
 ("B", "Dokąd pan idzie?", "jà pai nǎi khráp", "จะไปไหนครับ"),
 ("A", "Do dworca kolejowego.", "pai sà-thǎa-nii rót fai khráp", "ไปสถานีรถไฟครับ"),
 ("B", "To dość daleko stąd.", "jàak thîi nîi kâw klai mǔean kan khráp", "จากที่นี่ก็ไกลเหมือนกันครับ"),
 ("A", "Jak długo się idzie?", "dòoen pai naan thâo-rài khráp", "เดินไปนานเท่าไหร่ครับ"),
 ("B", "Około pół godziny.", "prà-maan khrûeng chûa moong khráp", "ประมาณครึ่งชั่วโมงครับ"),
 ("A", "Na twoim miejscu wziąłbym motocykl?", "thâa pen khun khun jà nâng win mǎi khráp", "ถ้าเป็นคุณคุณจะนั่งวินไหมครับ"),
 ("B", "Tak, będzie szybciej.", "châi khráp reo kwàa", "ใช่ครับ เร็วกว่า"),
 ("A", "Dziękuję bardzo.", "khàwp-khun mâak khráp", "ขอบคุณมากครับ"),
 ("B", "Uważaj na siebie w drodze.", "dòoen thaang plàwt phai ná khráp", "เดินทางปลอดภัยนะครับ"),
], "„win” to motocyklowa taksówka. Kierowcy noszą kamizelki z numerem i stoją na rogach ulic."),

("Spóźnienie na autobus", "Transport", "B1", "Pasażer", "Kasjer", [
 ("A", "Spóźniłem się na autobus.", "phǒm tòk rót khráp", "ผมตกรถครับ"),
 ("B", "Który to był kurs?", "rót rawp nǎi khráp", "รถรอบไหนครับ"),
 ("A", "Ten o dziesiątej.", "rawp sìp moong khráp", "รอบสิบโมงครับ"),
 ("B", "Następny za godzinę.", "khan tàw pai ìik chûa moong khráp", "คันต่อไปอีกชั่วโมงครับ"),
 ("A", "Czy bilet jest nadal ważny?", "tǔa bai doem yang chái dâai mǎi khráp", "ตั๋วใบเดิมยังใช้ได้ไหมครับ"),
 ("B", "Zmienię go bez opłaty.", "plìan hâi mâi khít ngoen phôoem khráp", "เปลี่ยนให้ไม่คิดเงินเพิ่มครับ"),
 ("A", "Ulżyło mi.", "khôi yang chûa khráp", "ค่อยยังชั่วครับ"),
 ("B", "Proszę czekać na peronie drugim.", "raw thîi chaan-chaa-laa thîi sǎwng khráp", "รอที่ชานชาลาที่สองครับ"),
], "„tòk rót” dosłownie „spaść z pojazdu” — po polsku „nie zdążyć”. Kalka byłaby niezrozumiała."),

("Rozmowa po kłótni", "Ludzie i rodzina", "B1", "Znajomy", "Znajoma", [
 ("A", "Przepraszam za wczoraj.", "khǎw-thôot rûeang mûea waan khráp", "ขอโทษเรื่องเมื่อวานครับ"),
 ("B", "Byłam zdenerwowana.", "tawn nán chǎn aa-rom sǐa khâ", "ตอนนั้นฉันอารมณ์เสียค่ะ"),
 ("A", "Nie chciałem cię urazić.", "phǒm mâi dâi tâng-jai hâi khun sǐa jai khráp", "ผมไม่ได้ตั้งใจให้คุณเสียใจครับ"),
 ("B", "Wiem. Chyba się nie zrozumieliśmy.", "rúu khâ rao khong khâo-jai mâi trong kan", "รู้ค่ะ เราคงเข้าใจไม่ตรงกัน"),
 ("A", "Porozmawiajmy spokojnie.", "khui kan dii dii ná khráp", "คุยกันดีๆ นะครับ"),
 ("B", "Dobrze. Zapomnijmy o tym.", "dâai khâ luem rûeang nán pai thòe", "ได้ค่ะ ลืมเรื่องนั้นไปเถอะ"),
 ("A", "Dziękuję za wyrozumiałość.", "khàwp-khun thîi khâo-jai khráp", "ขอบคุณที่เข้าใจครับ"),
 ("B", "Nie ma o czym mówić.", "rûeang lék náwi khâ", "เรื่องเล็กน้อยค่ะ"),
], "„khâo-jai mâi trong kan” ratuje rozmowę, bo nie obarcza winą żadnej ze stron."),

("Prośba o przestrzeń", "Ludzie i rodzina", "B1", "Znajomy", "Znajomy", [
 ("A", "Potrzebuję trochę przestrzeni.", "phǒm khǎw yùu khon diao sàk phák khráp", "ผมขออยู่คนเดียวสักพักครับ"),
 ("B", "Coś się stało?", "kòet à-rai khûen rǒe plào khráp", "เกิดอะไรขึ้นหรือเปล่าครับ"),
 ("A", "Ostatnio dużo się dzieje.", "chûang níi wûn waai khráp", "ช่วงนี้วุ่นวายครับ"),
 ("B", "Rozumiem, jak się czujesz.", "phǒm khâo-jai wâa khun rúu-sùek yang-ngai khráp", "ผมเข้าใจว่าคุณรู้สึกยังไงครับ"),
 ("A", "Dziękuję, że nie pytasz o szczegóły.", "khàwp-khun thîi mâi thǎam rai-lá-ìat khráp", "ขอบคุณที่ไม่ถามรายละเอียดครับ"),
 ("B", "Odezwij się, jak będziesz gotowy.", "phráwm mûea-rài thák maa dâai loei khráp", "พร้อมเมื่อไหร่ทักมาได้เลยครับ"),
 ("A", "Odezwę się.", "dǐao thák pai ná khráp", "เดี๋ยวทักไปนะครับ"),
 ("B", "Trzymaj się.", "sûu sûu ná khráp", "สู้ๆ นะครับ"),
], "„sûu sûu” to najczęstsze tajskie słowo wsparcia. Znaczy dosłownie „walcz”, ale brzmi ciepło."),

("Nieporozumienie z kolegą", "Ludzie i rodzina", "B1", "Kolega", "Kolega", [
 ("A", "Chyba się pokłóciliśmy wczoraj.", "rao khong thá-ló kan mûea waan khráp", "เราคงทะเลาะกันเมื่อวานครับ"),
 ("B", "Nie miałem tego na myśli.", "phǒm mâi dâi màai khwaam yàang nán khráp", "ผมไม่ได้หมายความอย่างนั้นครับ"),
 ("A", "To o co ci chodziło?", "màai thǔeng à-rai khráp", "หมายถึงอะไรครับ"),
 ("B", "Chodziło mi o termin, nie o ciebie.", "thîi phǒm màai thǔeng khue kam-nòt mâi châi khun", "ที่ผมหมายถึงคือกำหนด ไม่ใช่คุณ"),
 ("A", "Aha, o to chodzi.", "âw yàang níi níi eeng khráp", "อ๋อ อย่างนี้นี่เองครับ"),
 ("B", "Źle się wyraziłem.", "phǒm phûut mâi chát khráp", "ผมพูดไม่ชัดครับ"),
 ("A", "Nic nie szkodzi.", "mâi pen rai khráp", "ไม่เป็นไรครับ"),
 ("B", "Zacznijmy od nowa.", "rôoem mài ná khráp", "เริ่มใหม่นะครับ"),
], "„màai thǔeng” = mieć na myśli. To słowo ratuje najwięcej nieporozumień w rozmowie po tajsku."),

("Wizyta u lekarza z gorączką", "Zdrowie", "B1", "Pacjent", "Lekarz", [
 ("A", "Źle się czuję od wczoraj.", "phǒm mâi sà-baai tâng tàae mûea waan khráp", "ผมไม่สบายตั้งแต่เมื่อวานครับ"),
 ("B", "Jakie ma pan objawy?", "mii aa-kaan yang-ngai bâang khráp", "มีอาการยังไงบ้างครับ"),
 ("A", "Mam gorączkę od dwóch dni.", "mii khâi maa sǎwng wan láew khráp", "มีไข้มาสองวันแล้วครับ"),
 ("B", "Gorączka wraca wieczorem?", "khâi khûen tawn yen mǎi khráp", "ไข้ขึ้นตอนเย็นไหมครับ"),
 ("A", "Tak, i mam dreszcze.", "khráp láew kâw nǎao sàn dûai", "ครับ แล้วก็หนาวสั่นด้วย"),
 ("B", "Boli pana głowa?", "pùat hǔa dûai mǎi khráp", "ปวดหัวด้วยไหมครับ"),
 ("A", "Trochę. Nie mam apetytu.", "nít nòi khráp láew kâw mâi yàak aa-hǎan", "นิดหน่อยครับ แล้วก็ไม่อยากอาหาร"),
 ("B", "Zrobimy badanie krwi.", "tâwng trùat lûeat khráp", "ต้องตรวจเลือดครับ"),
 ("A", "Kiedy będą wyniki?", "phǒn trùat àwk mûea-rài khráp", "ผลตรวจออกเมื่อไหร่ครับ"),
 ("B", "Za dwie godziny.", "ìik sǎwng chûa moong khráp", "อีกสองชั่วโมงครับ"),
], "„aa-kaan” to objawy chorobowe. Lekarz zawsze zacznie od pytania „mii aa-kaan yang-ngai bâang”."),

("Opis bólu u lekarza", "Zdrowie", "B1", "Pacjent", "Lekarz", [
 ("A", "Boli mnie tutaj.", "jèp trong níi khráp", "เจ็บตรงนี้ครับ"),
 ("B", "Ból ostry czy tępy?", "jèp bàep lǽm rǔe pùat tûue khráp", "เจ็บแบบแหลมหรือปวดตื้อครับ"),
 ("A", "To tępy ból.", "man pùat tûue tûue khráp", "มันปวดตื้อๆ ครับ"),
 ("B", "Cały czas czy falami?", "pùat tà-làwt rǔe pen phák pen khraao khráp", "ปวดตลอดหรือเป็นพักเป็นคราวครับ"),
 ("A", "Ból przychodzi falami.", "pùat pen phák pen khraao khráp", "ปวดเป็นพักเป็นคราวครับ"),
 ("B", "Boli, kiedy się pan porusza?", "khà-yàp láew jèp mǎi khráp", "ขยับแล้วเจ็บไหมครับ"),
 ("A", "Tak, wtedy najbardziej.", "khráp tawn nán jèp thîi sùt", "ครับ ตอนนั้นเจ็บที่สุด"),
 ("B", "Zbadam pana.", "khǎw trùat dûai khráp", "ขอตรวจด้วยครับ"),
], "„jèp” to ból ostry i punktowy, „pùat” — tępy i rozlany. Lekarz rozróżnia je zawsze."),

("W aptece po leki", "Zdrowie", "B1", "Klient", "Farmaceuta", [
 ("A", "Mam biegunkę od rana.", "phǒm tháwng sǐa tâng tàae cháo khráp", "ผมท้องเสียตั้งแต่เช้าครับ"),
 ("B", "Ma pan gorączkę?", "mii khâi dûai mǎi khráp", "มีไข้ด้วยไหมครับ"),
 ("A", "Nie, tylko mdłości.", "mâi mii khráp mii tàae khlûen sâi", "ไม่มีครับ มีแต่คลื่นไส้"),
 ("B", "Dam panu lek i elektrolity.", "hâi yaa kàp phǒng klʉa râe khráp", "ให้ยากับผงเกลือแร่ครับ"),
 ("A", "Ile dni mam brać ten lek?", "kin yaa níi kìi wan khráp", "กินยานี้กี่วันครับ"),
 ("B", "Trzy dni, po jedzeniu.", "sǎam wan lǎng aa-hǎan khráp", "สามวัน หลังอาหารครับ"),
 ("A", "Czy ten lek daje senność?", "yaa níi tham hâi ngûang mǎi khráp", "ยานี้ทำให้ง่วงไหมครับ"),
 ("B", "Trochę tak. Proszę pić dużo wody.", "ngûang nít nòi khráp dùem náam yóe yóe ná", "ง่วงนิดหน่อยครับ ดื่มน้ำเยอะๆ นะ"),
 ("A", "Mam uczulenie na antybiotyki.", "phǒm phǎe yaa pà-tì-chii-wá-ná khráp", "ผมแพ้ยาปฏิชีวนะครับ"),
 ("B", "Zanotuję. To nie jest antybiotyk.", "dǐao bantúek wái khráp an níi mâi châi", "เดี๋ยวบันทึกไว้ครับ อันนี้ไม่ใช่"),
], "W tajskim leki się „je” (kin yaa), nie „bierze”. Zdanie o alergii warto umieć bezbłędnie."),

("Umawianie wizyty w klinice", "Zdrowie", "B1", "Pacjent", "Recepcja", [
 ("A", "Chciałbym się umówić do lekarza.", "phǒm yàak nát phóp mǎw khráp", "ผมอยากนัดพบหมอครับ"),
 ("B", "Był pan już u nas?", "khoei maa thîi nîi mǎi khráp", "เคยมาที่นี่ไหมครับ"),
 ("A", "Pierwszy raz.", "khráng râek khráp", "ครั้งแรกครับ"),
 ("B", "Poproszę paszport i ubezpieczenie.", "khǎw phaas-pàwt kàp prà-kan dûai khráp", "ขอพาสปอร์ตกับประกันด้วยครับ"),
 ("A", "Mam ubezpieczenie podróżne.", "phǒm mii prà-kan kaan dòoen thaang khráp", "ผมมีประกันการเดินทางครับ"),
 ("B", "Kiedy panu pasuje?", "sà-dùak wan nǎi khráp", "สะดวกวันไหนครับ"),
 ("A", "Najlepiej dzisiaj.", "wan níi dii thîi sùt khráp", "วันนี้ดีที่สุดครับ"),
 ("B", "Jest wolny termin o trzeciej.", "mii khiw bàai sǎam khráp", "มีคิวบ่ายสามครับ"),
 ("A", "Biorę.", "ao khráp", "เอาครับ"),
 ("B", "Proszę przyjść piętnaście minut wcześniej.", "maa kàwn sìp hâa naa-thii ná khráp", "มาก่อนสิบห้านาทีนะครับ"),
], "„khiw” od angielskiego queue oznacza wolny termin lub miejsce w kolejce."),

("Rozmowa o zdrowieniu", "Zdrowie", "B1", "Znajomy", "Znajomy", [
 ("A", "Jak się czujesz?", "pen yang-ngai bâang khráp", "เป็นยังไงบ้างครับ"),
 ("B", "Trochę mi się poprawiło.", "aa-kaan dii khûen nòi nùeng khráp", "อาการดีขึ้นหน่อยหนึ่งครับ"),
 ("A", "To dobrze. Byłeś u lekarza?", "dii khráp pai hǎa mǎw rǔe yang", "ดีครับ ไปหาหมอหรือยัง"),
 ("B", "Byłem wczoraj.", "pai maa mûea waan khráp", "ไปมาเมื่อวานครับ"),
 ("A", "I co powiedział?", "láew mǎw wâa yang-ngai khráp", "แล้วหมอว่ายังไงครับ"),
 ("B", "Że mam odpoczywać i pić dużo wody.", "mǎw bàwk hâi phák láew dùem náam yóe yóe khráp", "หมอบอกให้พักแล้วดื่มน้ำเยอะๆ ครับ"),
 ("A", "Odpocznij trochę.", "phák phàwn bâang ná khráp", "พักผ่อนบ้างนะครับ"),
 ("B", "Wracam do zdrowia.", "khôi hǎai láew khráp", "ค่อยหายแล้วครับ"),
 ("A", "Zdrowiej szybko.", "hǎai wai wai ná khráp", "หายไวๆ นะครับ"),
 ("B", "Dziękuję.", "khàwp-khun khráp", "ขอบคุณครับ"),
], "„khôi hǎai” = powoli wracać do zdrowia. „khôi” opisuje zmianę stopniową, nie nagłą."),

("Planowanie wyjazdu na północ", "Transport", "B1", "Znajomy", "Znajoma", [
 ("A", "Jeśli się uda, pojadę na północ.", "thâa dâai phǒm jà pai phâak nǔea khráp", "ถ้าได้ผมจะไปภาคเหนือครับ"),
 ("B", "Kiedy planujesz?", "waang phǎen wái mûea-rài khâ", "วางแผนไว้เมื่อไหร่คะ"),
 ("A", "Planuję to na przyszły miesiąc.", "waang phǎen wái duean nâa khráp", "วางแผนไว้เดือนหน้าครับ"),
 ("B", "W porze deszczowej trudno tam dojechać.", "nâa fǒn pai lam-bàak ná khâ", "หน้าฝนไปลำบากนะคะ"),
 ("A", "Nie wiedziałem o tym.", "phǒm mâi rúu maa kàwn khráp", "ผมไม่รู้มาก่อนครับ"),
 ("B", "Na twoim miejscu pojechałabym zimą.", "thâa pen chǎn chǎn jà pai nâa nǎao khâ", "ถ้าเป็นฉัน ฉันจะไปหน้าหนาวค่ะ"),
 ("A", "Może zmienię plany.", "àat jà plìan phǎen khráp", "อาจจะเปลี่ยนแผนครับ"),
 ("B", "Zobaczymy, jak się potoczy.", "duu pai kàwn khâ", "ดูไปก่อนค่ะ"),
], "„phâak nǔea” to północ Tajlandii. „nâa fǒn” i „nâa nǎao” to pory roku, nie miesiące."),
]
