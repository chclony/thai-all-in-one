# -*- coding: utf-8 -*-
"""Wzorce zdaniowe etapu 6 — druga seria.

Konstrukcje uzupelniajace: prosba o instrukcje, pytanie o dokonanie czynnosci,
przyznanie sie do niewiedzy, prosba o odstepstwo, watpliwosc, prosba o lepsza
opcje, wybor sposrod wielu, zgubiona rzecz, liczba powtorzen, dostepne dni.

Pozycja: (polskie haslo rekordu, polskie haslo bazowe, polski przyklad)
"""

TPL_B = [

# =====================================================================
# chuai bawk noi waa … yang-ngai khrap — prosba o instrukcje
# =====================================================================
dict(key="BAWKYANGNGAI", ty="question", cat="Pytania", sub="Instrukcje", reg="n",
     ph="chûai bàwk nòi wâa {ph} yang-ngai khráp", th="ช่วยบอกหน่อยว่า{th}ยังไงครับ",
     lit="chûai bàwk nòi wâa … yang-ngai = proszę powiedzieć, jak …",
     note="Prośba o instrukcję, nie o wykonanie czynności. Rozmówca odpowie opisem kroków, a nie zrobi tego za ciebie.",
     ex_ph="khǎw-thôot khráp chûai bàwk nòi wâa {ph} yang-ngai", ex_th="ขอโทษครับ ช่วยบอกหน่อยว่า{th}ยังไง",
     items=[
       ("Proszę powiedzieć, jak zapłacić.", "płacić", "Przepraszam, proszę powiedzieć, jak zapłacić."),
       ("Proszę powiedzieć, jak zarezerwować.", "rezerwować", "Przepraszam, proszę powiedzieć, jak zarezerwować."),
       ("Proszę powiedzieć, jak wypełnić formularz.", "wypełnić formularz", "Przepraszam, proszę powiedzieć, jak wypełnić formularz."),
       ("Proszę powiedzieć, jak się przesiąść.", "przesiadać się", "Przepraszam, proszę powiedzieć, jak się przesiąść."),
       ("Proszę powiedzieć, jak to otworzyć.", "otwierać", "Przepraszam, proszę powiedzieć, jak to otworzyć."),
       ("Proszę powiedzieć, jak to zamknąć.", "zamykać", "Przepraszam, proszę powiedzieć, jak to zamknąć."),
       ("Proszę powiedzieć, jak tam dojechać.", "iść / jechać", "Przepraszam, proszę powiedzieć, jak tam dojechać."),
       ("Proszę powiedzieć, jak to zamówić.", "zamawiać", "Przepraszam, proszę powiedzieć, jak to zamówić."),
       ("Proszę powiedzieć, jak to wysłać.", "wysyłać", "Przepraszam, proszę powiedzieć, jak to wysłać."),
       ("Proszę powiedzieć, jak to anulować.", "anulować", "Przepraszam, proszę powiedzieć, jak to anulować."),
       ("Proszę powiedzieć, jak to zmienić.", "zmieniać", "Przepraszam, proszę powiedzieć, jak to zmienić."),
       ("Proszę powiedzieć, jak tego używać.", "używać", "Przepraszam, proszę powiedzieć, jak tego używać."),
       ("Proszę powiedzieć, jak się tam dostać pieszo.", "iść pieszo", "Przepraszam, proszę powiedzieć, jak tam dojść."),
       ("Proszę powiedzieć, jak to ugotować.", "gotować", "Przepraszam, proszę powiedzieć, jak to ugotować."),
       ("Proszę powiedzieć, jak to napisać.", "pisać", "Przepraszam, proszę powiedzieć, jak to napisać."),
       ("Proszę powiedzieć, jak to wynająć.", "wynajmować", "Przepraszam, proszę powiedzieć, jak to wynająć."),
     ]),

# =====================================================================
# … laew rue yang khrap — pytanie o dokonanie
# =====================================================================
dict(key="LAEWRUEYANG", ty="question", cat="Pytania", sub="Sprawdzanie", reg="n",
     ph="{ph} láew rǔe yang khráp", th="{th}แล้วหรือยังครับ",
     lit="… láew rǔe yang = czy już …, czy jeszcze nie?",
     note="Pytanie o dokonanie czynności. Odpowiedź brzmi „láew” (już) albo „yang” (jeszcze nie) — nigdy „chái/mâi châi”.",
     ex_ph="khun {ph} láew rǔe yang khráp thâa yang phǒm raw dâai", ex_th="คุณ{th}แล้วหรือยังครับ ถ้ายังผมรอได้",
     items=[
       ("Czy już jadłeś?", "jeść", "Czy już jadłeś? Jeśli nie, mogę poczekać."),
       ("Czy już zapłaciłeś?", "płacić", "Czy już zapłaciłeś? Jeśli nie, mogę poczekać."),
       ("Czy już zarezerwowałeś?", "rezerwować", "Czy już zarezerwowałeś? Jeśli nie, mogę poczekać."),
       ("Czy już zamówiłeś?", "zamawiać", "Czy już zamówiłeś? Jeśli nie, mogę poczekać."),
       ("Czy już wysłałeś?", "wysyłać", "Czy już wysłałeś? Jeśli nie, mogę poczekać."),
       ("Czy już się spakowałeś?", "pakować się", "Czy już się spakowałeś? Jeśli nie, mogę poczekać."),
       ("Czy już wróciłeś?", "wracać", "Czy już wróciłeś? Jeśli nie, mogę poczekać."),
       ("Czy już podpisałeś?", "podpisać", "Czy już podpisałeś? Jeśli nie, mogę poczekać."),
       ("Czy już zadzwoniłeś?", "dzwonić", "Czy już zadzwoniłeś? Jeśli nie, mogę poczekać."),
       ("Czy już odpowiedziałeś?", "odpowiadać", "Czy już odpowiedziałeś? Jeśli nie, mogę poczekać."),
       ("Czy już to znalazłeś?", "znaleźć", "Czy już to znalazłeś? Jeśli nie, mogę poczekać."),
       ("Czy już wybrałeś?", "wybierać", "Czy już wybrałeś? Jeśli nie, mogę poczekać."),
       ("Czy już odebrałeś?", "odbierać", "Czy już odebrałeś? Jeśli nie, mogę poczekać."),
       ("Czy już zacząłeś?", "zaczynać", "Czy już zacząłeś? Jeśli nie, mogę poczekać."),
       ("Czy już wypełniłeś formularz?", "wypełnić formularz", "Czy już wypełniłeś formularz? Jeśli nie, mogę poczekać."),
       ("Czy już kupiłeś bilet?", "kupować", "Czy już kupiłeś? Jeśli nie, mogę poczekać."),
     ]),

# =====================================================================
# phom mai ruu waa … yang-ngai khrap — przyznanie sie do niewiedzy
# =====================================================================
dict(key="MAIRUUYANGNGAI", ty="sentence", cat="Podstawy i grzeczność", sub="Niewiedza", reg="n",
     ph="phǒm mâi rúu wâa {ph} yang-ngai khráp", th="ผมไม่รู้ว่า{th}ยังไงครับ",
     lit="mâi rúu wâa … yang-ngai = nie wiem, jak …",
     note="Przyznanie się do niewiedzy otwiera drogę do pomocy. W Tajlandii jest to całkowicie neutralne i nie odbiera powagi.",
     ex_ph="khǎw-thôot khráp phǒm mâi rúu wâa {ph} yang-ngai chûai nòi dâai mǎi", ex_th="ขอโทษครับ ผมไม่รู้ว่า{th}ยังไง ช่วยหน่อยได้ไหม",
     items=[
       ("Nie wiem, jak to zamówić.", "zamawiać", "Nie wiem, jak to zamówić, czy może pan pomóc?"),
       ("Nie wiem, jak zapłacić.", "płacić", "Nie wiem, jak zapłacić, czy może pan pomóc?"),
       ("Nie wiem, jak tam dojechać.", "iść / jechać", "Nie wiem, jak tam dojechać, czy może pan pomóc?"),
       ("Nie wiem, jak to otworzyć.", "otwierać", "Nie wiem, jak to otworzyć, czy może pan pomóc?"),
       ("Nie wiem, jak tego używać.", "używać", "Nie wiem, jak tego używać, czy może pan pomóc?"),
       ("Nie wiem, jak to wypełnić.", "wypełnić formularz", "Nie wiem, jak to wypełnić, czy może pan pomóc?"),
       ("Nie wiem, jak się przesiąść.", "przesiadać się", "Nie wiem, jak się przesiąść, czy może pan pomóc?"),
       ("Nie wiem, jak to anulować.", "anulować", "Nie wiem, jak to anulować, czy może pan pomóc?"),
       ("Nie wiem, jak to wysłać.", "wysyłać", "Nie wiem, jak to wysłać, czy może pan pomóc?"),
       ("Nie wiem, jak to zmienić.", "zmieniać", "Nie wiem, jak to zmienić, czy może pan pomóc?"),
       ("Nie wiem, jak to napisać.", "pisać", "Nie wiem, jak to napisać, czy może pan pomóc?"),
       ("Nie wiem, jak to ugotować.", "gotować", "Nie wiem, jak to ugotować, czy może pan pomóc?"),
       ("Nie wiem, jak to wynająć.", "wynajmować", "Nie wiem, jak to wynająć, czy może pan pomóc?"),
       ("Nie wiem, jak to zarezerwować.", "rezerwować", "Nie wiem, jak to zarezerwować, czy może pan pomóc?"),
     ]),

# =====================================================================
# khaw … pen phi-seet daai mai khrap — prosba o odstepstwo
# =====================================================================
dict(key="PHISEET", ty="question", cat="Podstawy i grzeczność", sub="Prośby", reg="f",
     ph="khǎw {ph} pen phí-sèet dâai mǎi khráp", th="ขอ{th}เป็นพิเศษได้ไหมครับ",
     lit="pen phí-sèet = wyjątkowo, poza zwykłym trybem",
     note="Prośba o odstępstwo od reguły. Uznajesz, że zasada istnieje, i prosisz o wyjątek — to układ, w którym Tajowi łatwo powiedzieć „tak”.",
     ex_ph="khǎw {ph} pen phí-sèet dâai mǎi khráp phǒm mii thù-rá dùan", ex_th="ขอ{th}เป็นพิเศษได้ไหมครับ ผมมีธุระด่วน",
     items=[
       ("Czy mogę wyjątkowo poczekać dłużej?", "czekać", "Czy mogę wyjątkowo poczekać dłużej? Mam pilną sprawę."),
       ("Czy mogę wyjątkowo zapłacić później?", "płacić", "Czy mogę wyjątkowo zapłacić później? Mam pilną sprawę."),
       ("Czy mogę wyjątkowo to zmienić?", "zmieniać", "Czy mogę wyjątkowo to zmienić? Mam pilną sprawę."),
       ("Czy mogę wyjątkowo anulować?", "anulować", "Czy mogę wyjątkowo anulować? Mam pilną sprawę."),
       ("Czy mogę wyjątkowo zarezerwować?", "rezerwować", "Czy mogę wyjątkowo zarezerwować? Mam pilną sprawę."),
       ("Czy mogę wyjątkowo wejść?", "wchodzić", "Czy mogę wyjątkowo wejść? Mam pilną sprawę."),
       ("Czy mogę wyjątkowo to pożyczyć?", "pożyczyć", "Czy mogę wyjątkowo to pożyczyć? Mam pilną sprawę."),
       ("Czy mogę wyjątkowo przymierzyć?", "przymierzać / próbować", "Czy mogę wyjątkowo przymierzyć? Mam pilną sprawę."),
       ("Czy mogę wyjątkowo zamówić?", "zamawiać", "Czy mogę wyjątkowo zamówić? Mam pilną sprawę."),
       ("Czy mogę wyjątkowo zostać dłużej?", "spać", "Czy mogę wyjątkowo zostać na noc? Mam pilną sprawę."),
       ("Czy mogę wyjątkowo odebrać wcześniej?", "odbierać", "Czy mogę wyjątkowo odebrać wcześniej? Mam pilną sprawę."),
       ("Czy mogę wyjątkowo to wysłać dziś?", "wysyłać", "Czy mogę wyjątkowo wysłać to dziś? Mam pilną sprawę."),
     ]),

# =====================================================================
# phom song-sai waa … rue plao khrap — watpliwosc
# =====================================================================
dict(key="SONGSAI", ty="sentence", cat="Cechy i opinie", sub="Wątpliwości", reg="n",
     ph="phǒm sǒng-sǎi wâa {ph} rǔe plào khráp", th="ผมสงสัยว่า{th}หรือเปล่าครับ",
     lit="sǒng-sǎi wâa … rǔe plào = zastanawiam się, czy …",
     note="Grzeczny sposób zakwestionowania czegoś. Zamiast oskarżać, zgłaszasz własną wątpliwość — rozmówca może sprostować bez utraty twarzy.",
     ex_ph="phǒm sǒng-sǎi wâa {ph} rǔe plào khráp chûai chék hâi nòi", ex_th="ผมสงสัยว่า{th}หรือเปล่าครับ ช่วยเช็คให้หน่อย",
     items=[
       ("Zastanawiam się, czy to zamknięte.", "zamykać", "Zastanawiam się, czy to zamknięte — proszę sprawdzić."),
       ("Zastanawiam się, czy już zapłaciłem.", "płacić", "Zastanawiam się, czy już zapłaciłem — proszę sprawdzić."),
       ("Zastanawiam się, czy dobrze zrozumiałem.", "rozumieć", "Zastanawiam się, czy dobrze zrozumiałem — proszę sprawdzić."),
       ("Zastanawiam się, czy oni czekają.", "czekać", "Zastanawiam się, czy oni czekają — proszę sprawdzić."),
       ("Zastanawiam się, czy to zarezerwowano.", "rezerwować", "Zastanawiam się, czy to zarezerwowano — proszę sprawdzić."),
       ("Zastanawiam się, czy to wysłano.", "wysyłać", "Zastanawiam się, czy to wysłano — proszę sprawdzić."),
       ("Zastanawiam się, czy to anulowano.", "anulować", "Zastanawiam się, czy to anulowano — proszę sprawdzić."),
       ("Zastanawiam się, czy niczego nie zgubiłem.", "zgubić", "Zastanawiam się, czy niczego nie zgubiłem — proszę sprawdzić."),
       ("Zastanawiam się, czy oni to sprzedają.", "sprzedawać", "Zastanawiam się, czy oni to sprzedają — proszę sprawdzić."),
       ("Zastanawiam się, czy to działa.", "używać", "Zastanawiam się, czy tego się używa — proszę sprawdzić."),
       ("Zastanawiam się, czy oni to zmienili.", "zmieniać", "Zastanawiam się, czy oni to zmienili — proszę sprawdzić."),
       ("Zastanawiam się, czy dobrze zapisałem.", "pisać", "Zastanawiam się, czy dobrze zapisałem — proszę sprawdzić."),
     ]),

# =====================================================================
# mii … thii dii kwaa nii mai khrap — prosba o lepsza opcje
# =====================================================================
dict(key="DIIKWAANII", ty="question", cat="Zakupy i pieniądze", sub="Wybór", reg="n",
     ph="mii {ph} thîi dii kwàa níi mǎi khráp", th="มี{th}ที่ดีกว่านี้ไหมครับ",
     lit="… thîi dii kwàa níi = … lepszy niż ten",
     note="Prośba o lepszą opcję bez krytykowania pokazanej. Sprzedawca nie traci twarzy, a ty dostajesz alternatywę.",
     ex_ph="mii {ph} thîi dii kwàa níi mǎi khráp raa-khaa sǔung nòi kâw dâai", ex_th="มี{th}ที่ดีกว่านี้ไหมครับ ราคาสูงหน่อยก็ได้",
     items=[
       ("Czy jest lepszy pokój?", "pokój", "Czy jest lepszy pokój? Może być trochę droższy."),
       ("Czy jest lepszy stolik?", "stolik", "Czy jest lepszy stolik? Może być trochę droższy."),
       ("Czy jest lepszy samochód?", "samochód", "Czy jest lepszy samochód? Może być trochę droższy."),
       ("Czy jest lepszy hotel?", "hotel", "Czy jest lepszy hotel? Może być trochę droższy."),
       ("Czy jest lepsza restauracja?", "restauracja", "Czy jest lepsza restauracja? Może być trochę droższa."),
       ("Czy jest lepszy rower?", "rower", "Czy jest lepszy rower? Może być trochę droższy."),
       ("Czy jest lepszy plecak?", "plecak", "Czy jest lepszy plecak? Może być trochę droższy."),
       ("Czy jest lepszy kask?", "kask", "Czy jest lepszy kask? Może być trochę droższy."),
       ("Czy jest lepsza mapa?", "mapa", "Czy jest lepsza mapa? Może być trochę droższa."),
       ("Czy jest lepszy router?", "router", "Czy jest lepszy router? Może być trochę droższy."),
       ("Czy jest lepszy przewodnik?", "przewodnik (osoba)", "Czy jest lepszy przewodnik? Może być trochę droższy."),
       ("Czy jest lepsze miejsce?", "peron", "Czy jest lepsze miejsce? Może być trochę droższe."),
     ]),

# =====================================================================
# … an nai dii khrap — wybor sposrod wielu
# =====================================================================
dict(key="ANNAIDII", ty="question", cat="Zakupy i pieniądze", sub="Wybór", reg="n",
     ph="{ph} an nǎi dii khráp", th="{th}อันไหนดีครับ",
     lit="an nǎi dii = która sztuka będzie dobra?",
     note="„an” to klasyfikator drobnych przedmiotów. Pytanie prosi o rekomendację, a nie o wskazanie miejsca na półce.",
     ex_ph="{ph} an nǎi dii khráp chûai náe nam nòi", ex_th="{th}อันไหนดีครับ ช่วยแนะนำหน่อย",
     items=[
       ("Który wybrać?", "wybierać", "Który wybrać? Proszę o radę."),
       ("Który kupić?", "kupować", "Który kupić? Proszę o radę."),
       ("Który zamówić?", "zamawiać", "Który zamówić? Proszę o radę."),
       ("Który wynająć?", "wynajmować", "Który wynająć? Proszę o radę."),
       ("Który przymierzyć?", "przymierzać / próbować", "Który przymierzyć? Proszę o radę."),
       ("Który zarezerwować?", "rezerwować", "Który zarezerwować? Proszę o radę."),
       ("Którego spróbować?", "próbować (smakować)", "Którego spróbować? Proszę o radę."),
       ("Którego użyć?", "używać", "Którego użyć? Proszę o radę."),
       ("Który wziąć?", "brać", "Który wziąć? Proszę o radę."),
       ("Który obejrzeć?", "oglądać", "Który obejrzeć? Proszę o radę."),
     ]),

# =====================================================================
# … haai pai nai mai ruu khrap — zguba
# =====================================================================
dict(key="HAAIPAINAI", ty="sentence", cat="Awarie i pomoc", sub="Zguby", reg="n",
     ph="{ph} hǎai pai nǎi mâi rúu khráp", th="{th}หายไปไหนไม่รู้ครับ",
     lit="… hǎai pai nǎi mâi rúu = … gdzieś zniknęło, nie wiem gdzie",
     note="Opis zguby bez wskazywania winnego. W hotelu i w pracy to bezpieczniejsze otwarcie niż „ktoś zabrał”.",
     ex_ph="{ph} hǎai pai nǎi mâi rúu khráp chûai chûai hǎa nòi", ex_th="{th}หายไปไหนไม่รู้ครับ ช่วยหาหน่อย",
     items=[
       ("Gdzieś zniknął mi klucz.", "klucz", "Gdzieś zniknął mi klucz, proszę o pomoc w szukaniu."),
       ("Gdzieś zniknął mi portfel.", "portfel", "Gdzieś zniknął mi portfel, proszę o pomoc w szukaniu."),
       ("Gdzieś zniknął mi paszport.", "paszport", "Gdzieś zniknął mi paszport, proszę o pomoc w szukaniu."),
       ("Gdzieś zniknął mi bilet.", "bilet", "Gdzieś zniknął mi bilet, proszę o pomoc w szukaniu."),
       ("Gdzieś zniknęły mi okulary.", "okulary przeciwsłoneczne", "Gdzieś zniknęły mi okulary, proszę o pomoc w szukaniu."),
       ("Gdzieś zniknął mi plecak.", "plecak", "Gdzieś zniknął mi plecak, proszę o pomoc w szukaniu."),
       ("Gdzieś zniknęła mi karta kredytowa.", "karta kredytowa", "Gdzieś zniknęła mi karta, proszę o pomoc w szukaniu."),
       ("Gdzieś zniknął mi paragon.", "paragon", "Gdzieś zniknął mi paragon, proszę o pomoc w szukaniu."),
       ("Gdzieś zniknął mi kapelusz.", "kapelusz", "Gdzieś zniknął mi kapelusz, proszę o pomoc w szukaniu."),
       ("Gdzieś zniknęła mi karta SIM.", "karta SIM", "Gdzieś zniknęła mi karta SIM, proszę o pomoc w szukaniu."),
       ("Gdzieś zniknął mi powerbank.", "powerbank", "Gdzieś zniknął mi powerbank, proszę o pomoc w szukaniu."),
       ("Gdzieś zniknęło mi prawo jazdy.", "prawo jazdy", "Gdzieś zniknęło mi prawo jazdy, proszę o pomoc w szukaniu."),
     ]),

# =====================================================================
# tawng … kii khrang khrap — liczba powtorzen
# =====================================================================
dict(key="KIIKHRANG", ty="question", cat="Pytania", sub="Liczby", reg="n",
     ph="tâwng {ph} kìi khráng khráp", th="ต้อง{th}กี่ครั้งครับ",
     lit="kìi khráng = ile razy",
     note="„khráng” to klasyfikator powtórzeń. Pytanie przydaje się przy lekach, formalnościach i przesiadkach.",
     ex_ph="tâwng {ph} kìi khráng khráp thǔeng jà sèt", ex_th="ต้อง{th}กี่ครั้งครับ ถึงจะเสร็จ",
     items=[
       ("Ile razy trzeba przyjść?", "przyjść / przyjechać", "Ile razy trzeba przyjść, żeby to załatwić?"),
       ("Ile razy trzeba się przesiąść?", "przesiadać się", "Ile razy trzeba się przesiąść, żeby dojechać?"),
       ("Ile razy trzeba zapłacić?", "płacić", "Ile razy trzeba zapłacić, żeby to załatwić?"),
       ("Ile razy trzeba podpisać?", "podpisać", "Ile razy trzeba podpisać, żeby to załatwić?"),
       ("Ile razy trzeba zadzwonić?", "dzwonić", "Ile razy trzeba zadzwonić, żeby to załatwić?"),
       ("Ile razy trzeba to powtórzyć?", "mówić", "Ile razy trzeba to powiedzieć, żeby zrozumieli?"),
       ("Ile razy trzeba przymierzyć?", "przymierzać / próbować", "Ile razy trzeba przymierzyć, żeby wybrać?"),
       ("Ile razy trzeba to wysłać?", "wysyłać", "Ile razy trzeba to wysłać, żeby dotarło?"),
       ("Ile razy trzeba to sprawdzić?", "szukać", "Ile razy trzeba tego szukać, żeby znaleźć?"),
       ("Ile razy trzeba to zrobić?", "robić", "Ile razy trzeba to zrobić, żeby było gotowe?"),
     ]),

# =====================================================================
# … wan nai daai baang khrap — dostepne dni
# =====================================================================
dict(key="WANNAIBAANG", ty="question", cat="Czas i daty", sub="Terminy", reg="n",
     ph="{ph} dâai wan nǎi bâang khráp", th="{th}ได้วันไหนบ้างครับ",
     lit="wan nǎi bâang = w które dni",
     note="„bâang” otwiera pytanie na kilka odpowiedzi. Bez niego pytasz o jeden konkretny dzień.",
     ex_ph="{ph} dâai wan nǎi bâang khráp phǒm wâang tháng aa-thít", ex_th="{th}ได้วันไหนบ้างครับ ผมว่างทั้งอาทิตย์",
     items=[
       ("W które dni można się spotkać?", "spotykać", "W które dni można się spotkać? Mam wolny cały tydzień."),
       ("W które dni można przyjść?", "przyjść / przyjechać", "W które dni można przyjść? Mam wolny cały tydzień."),
       ("W które dni można zarezerwować?", "rezerwować", "W które dni można zarezerwować? Mam wolny cały tydzień."),
       ("W które dni można wynająć?", "wynajmować", "W które dni można wynająć? Mam wolny cały tydzień."),
       ("W które dni można zwiedzać?", "zwiedzać", "W które dni można zwiedzać? Mam wolny cały tydzień."),
       ("W które dni można odebrać?", "odbierać", "W które dni można odebrać? Mam wolny cały tydzień."),
       ("W które dni można się uczyć?", "uczyć się", "W które dni można się uczyć? Mam wolny cały tydzień."),
       ("W które dni można pracować?", "pracować", "W które dni można pracować? Mam wolny cały tydzień."),
       ("W które dni można zamówić?", "zamawiać", "W które dni można zamówić? Mam wolny cały tydzień."),
       ("W które dni można zapłacić?", "płacić", "W które dni można zapłacić? Mam wolny cały tydzień."),
     ]),
]
