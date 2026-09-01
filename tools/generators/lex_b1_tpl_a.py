# -*- coding: utf-8 -*-
"""Wzorce zdaniowe etapu 4 (B1) — czesc A: konstrukcje czasownikowe.

Kazdy wzorzec ma ZAMKNIETA biala liste hasel bazowych. Pozycja trafia na liste
tylko wtedy, gdy polskie zdanie brzmi naturalnie — nie ma tu iloczynu
kartezjanskiego.

Konstrukcje sa dobrane tak, zeby NIE powielaly wzorcow A1 ani A2. Zuzyte juz
zostaly: „yàak”, „tâwng”, „… mâi dâai”, „… láew”, „khoei”, „phôoeng”,
„kamlang … yùu”, „mâi khâwi”, „mâi than”, „sèt láew”, „jam … dâai”, „pen”,
„bàwi”, „thúk wan”, „khuan”.

Etap 4 siega po konstrukcje zlozone: warunek, zamiar, nadzieja, obawa,
proba, ustepstwo, uporczywosc, przyblizenie.

Pozycja: (polskie haslo rekordu, polskie haslo bazowe, polski przyklad)
"""

TPL_A = [

# =====================================================================
# thaa … dai kaw dii — warunek zyczeniowy
# =====================================================================
dict(key="THAADAI", ty="sentence", cat="Gramatyka użytkowa", sub="Warunek", reg="n",
     ph="thâa phǒm {ph} dâai kâw dii khráp", th="ถ้าผม{th}ได้ก็ดีครับ",
     lit="thâa … dâai kâw dii = gdyby się udało, byłoby dobrze",
     note="Tajski warunek to para „thâa …, kâw …”. Czasownik nie zmienia formy — cały tryb przypuszczający niesie sama konstrukcja.",
     ex_ph="thâa {ph} dâai kâw bàwk ná khráp", ex_th="ถ้า{th}ได้ก็บอกนะครับ",
     items=[
       ("Dobrze by było, gdybym mógł odpocząć.", "odpoczywać", "Daj znać, jeśli się uda odpocząć."),
       ("Dobrze by było, gdybym mógł tu popływać.", "pływać", "Daj znać, jeśli będzie można popływać."),
       ("Dobrze by było, gdybym mógł to wynająć.", "wynajmować", "Daj znać, jeśli da się wynająć."),
       ("Dobrze by było, gdybym mógł zarezerwować.", "rezerwować", "Daj znać, jeśli da się zarezerwować."),
       ("Dobrze by było, gdybym mógł to zmienić.", "zmieniać", "Daj znać, jeśli da się zmienić."),
       ("Dobrze by było, gdybym mógł to zwrócić.", "sprzedawać", "Daj znać, jeśli da się sprzedać."),
       ("Dobrze by było, gdybym zdążył wrócić.", "wracać", "Daj znać, jeśli zdążysz wrócić."),
       ("Dobrze by było, gdybym mógł zapłacić kartą.", "płacić", "Daj znać, jeśli da się zapłacić."),
       ("Dobrze by było, gdybym mógł to pożyczyć.", "pożyczyć", "Daj znać, jeśli da się pożyczyć."),
       ("Dobrze by było, gdybym mógł zapytać osobiście.", "pytać", "Daj znać, jeśli będzie można zapytać."),
       ("Dobrze by było, gdybym mógł to obejrzeć.", "oglądać", "Daj znać, jeśli będzie można obejrzeć."),
       ("Dobrze by było, gdybym mógł się wcześniej spakować.", "pakować się", "Daj znać, jeśli zdążysz się spakować."),
       ("Dobrze by było, gdybym mógł tu zaparkować.", "zatrzymać się", "Daj znać, jeśli da się zatrzymać."),
       ("Dobrze by było, gdybym mógł to podpisać dzisiaj.", "podpisać", "Daj znać, jeśli da się podpisać."),
       ("Dobrze by było, gdybym mógł się jeszcze pouczyć.", "uczyć się", "Daj znać, jeśli będzie czas na naukę."),
       ("Dobrze by było, gdybym mógł to ugotować sam.", "gotować", "Daj znać, jeśli będzie można gotować."),
       ("Dobrze by było, gdybym mógł tu zrobić zdjęcia.", "robić zdjęcia", "Daj znać, jeśli można robić zdjęcia."),
       ("Dobrze by było, gdybym mógł się z nim spotkać.", "spotykać", "Daj znać, jeśli uda się spotkać."),
       ("Dobrze by było, gdybym mógł to wysłać dzisiaj.", "wysyłać", "Daj znać, jeśli da się wysłać."),
       ("Dobrze by było, gdybym mógł to znaleźć.", "znaleźć", "Daj znać, jeśli uda się znaleźć."),
       ("Dobrze by było, gdybym mógł tu jeszcze wrócić i pozwiedzać.", "zwiedzać", "Daj znać, jeśli będzie czas na zwiedzanie."),
       ("Dobrze by było, gdybym mógł się wyspać.", "spać", "Daj znać, jeśli uda ci się wyspać."),
       ("Dobrze by było, gdybym mógł się dodzwonić.", "dzwonić", "Daj znać, jeśli uda się dodzwonić."),
       ("Dobrze by było, gdybym mógł to przymierzyć.", "przymierzać / próbować", "Daj znać, jeśli da się przymierzyć."),
       ("Dobrze by było, gdybym mógł się przesiąść.", "przesiadać się", "Daj znać, jeśli da się przesiąść."),
     ]),

# =====================================================================
# tang-jai waa ja — zamiar
# =====================================================================
dict(key="TANGJAI", ty="sentence", cat="Gramatyka użytkowa", sub="Plany", reg="n",
     ph="phǒm tâng-jai wâa jà {ph} khráp", th="ผมตั้งใจว่าจะ{th}ครับ",
     lit="tâng-jai = ustawić serce, postanowić",
     note="„tâng-jai wâa jà” to postanowienie, nie zwykła przyszłość. Samo „jà” byłoby dużo słabsze.",
     ex_ph="tâng-jai wâa jà {ph} mûea-rài khráp", ex_th="ตั้งใจว่าจะ{th}เมื่อไหร่ครับ",
     items=[
       ("Zamierzam się tego nauczyć.", "uczyć się", "Kiedy zamierzasz się uczyć?"),
       ("Zamierzam wynająć mieszkanie.", "wynajmować", "Kiedy zamierzasz wynająć?"),
       ("Zamierzam to sprzedać.", "sprzedawać", "Kiedy zamierzasz sprzedać?"),
       ("Zamierzam tam pojechać.", "iść / jechać", "Kiedy zamierzasz jechać?"),
       ("Zamierzam wrócić do Polski.", "wracać", "Kiedy zamierzasz wracać?"),
       ("Zamierzam zacząć od jutra.", "zaczynać", "Kiedy zamierzasz zacząć?"),
       ("Zamierzam to zarezerwować.", "rezerwować", "Kiedy zamierzasz rezerwować?"),
       ("Zamierzam zapłacić w tym tygodniu.", "płacić", "Kiedy zamierzasz zapłacić?"),
       ("Zamierzam się spakować wieczorem.", "pakować się", "Kiedy zamierzasz się pakować?"),
       ("Zamierzam to zmienić.", "zmieniać", "Kiedy zamierzasz zmienić?"),
       ("Zamierzam poszukać czegoś tańszego.", "szukać", "Kiedy zamierzasz szukać?"),
       ("Zamierzam z nim porozmawiać.", "rozmawiać", "Kiedy zamierzasz rozmawiać?"),
       ("Zamierzam to napisać dzisiaj.", "pisać", "Kiedy zamierzasz pisać?"),
       ("Zamierzam więcej odpoczywać.", "odpoczywać", "Kiedy zamierzasz odpoczywać?"),
       ("Zamierzam więcej biegać.", "biegać", "Kiedy zamierzasz biegać?"),
       ("Zamierzam nauczyć się gotować.", "gotować", "Kiedy zamierzasz gotować?"),
       ("Zamierzam to anulować.", "anulować", "Kiedy zamierzasz anulować?"),
       ("Zamierzam podpisać w piątek.", "podpisać", "Kiedy zamierzasz podpisać?"),
       ("Zamierzam zwiedzić północ kraju.", "zwiedzać", "Kiedy zamierzasz zwiedzać?"),
       ("Zamierzam zaprosić znajomych.", "zapraszać", "Kiedy zamierzasz zapraszać?"),
       ("Zamierzam wstawać wcześniej.", "wstawać", "Od kiedy zamierzasz wstawać wcześniej?"),
       ("Zamierzam przestać się tym przejmować.", "przestać", "Kiedy zamierzasz przestać?"),
       ("Zamierzam to wysłać jutro.", "wysyłać", "Kiedy zamierzasz wysłać?"),
       ("Zamierzam wypełnić wniosek sam.", "wypełnić formularz", "Kiedy zamierzasz wypełnić wniosek?"),
       ("Zamierzam się z nimi spotkać.", "spotykać", "Kiedy zamierzasz się spotkać?"),
     ]),

# =====================================================================
# wang waa ja dai … iik — nadzieja
# =====================================================================
dict(key="WANGWAA", ty="sentence", cat="Gramatyka użytkowa", sub="Marzenia", reg="n",
     ph="phǒm wǎng wâa jà dâai {ph} ìik khráp", th="ผมหวังว่าจะได้{th}อีกครับ",
     lit="wǎng wâa = mieć nadzieję, że",
     note="„dâai + czasownik” znaczy tu „mieć okazję coś zrobić”, nie „móc”. To ważna różnica.",
     ex_ph="wǎng wâa jà dâai {ph} ìik ná khráp", ex_th="หวังว่าจะได้{th}อีกนะครับ",
     items=[
       ("Mam nadzieję, że jeszcze się spotkamy.", "spotykać", "Oby udało się spotkać jeszcze raz."),
       ("Mam nadzieję, że jeszcze tu przyjadę.", "przyjść / przyjechać", "Oby udało się jeszcze przyjechać."),
       ("Mam nadzieję, że jeszcze tego spróbuję.", "próbować (smakować)", "Oby udało się spróbować jeszcze raz."),
       ("Mam nadzieję, że jeszcze popływam.", "pływać", "Oby udało się jeszcze popływać."),
       ("Mam nadzieję, że jeszcze pozwiedzam.", "zwiedzać", "Oby udało się jeszcze pozwiedzać."),
       ("Mam nadzieję, że jeszcze porozmawiamy.", "rozmawiać", "Oby udało się jeszcze porozmawiać."),
       ("Mam nadzieję, że jeszcze tu popracuję.", "pracować", "Oby udało się jeszcze popracować."),
       ("Mam nadzieję, że jeszcze tu pomieszkam.", "siedzieć", "Oby udało się jeszcze tu posiedzieć."),
       ("Mam nadzieję, że jeszcze się pouczę.", "uczyć się", "Oby udało się jeszcze pouczyć."),
       ("Mam nadzieję, że jeszcze tu odpocznę.", "odpoczywać", "Oby udało się jeszcze odpocząć."),
       ("Mam nadzieję, że jeszcze zrobię tu zdjęcia.", "robić zdjęcia", "Oby udało się jeszcze porobić zdjęcia."),
       ("Mam nadzieję, że jeszcze potańczę.", "tańczyć", "Oby udało się jeszcze potańczyć."),
       ("Mam nadzieję, że jeszcze zaśpiewam.", "śpiewać", "Oby udało się jeszcze zaśpiewać."),
       ("Mam nadzieję, że jeszcze coś tu kupię.", "kupować", "Oby udało się jeszcze coś kupić."),
       ("Mam nadzieję, że jeszcze to zobaczę.", "oglądać", "Oby udało się jeszcze zobaczyć."),
       ("Mam nadzieję, że jeszcze się przejdę.", "iść pieszo", "Oby udało się jeszcze przejść."),
       ("Mam nadzieję, że jeszcze tu zjem.", "jeść", "Oby udało się jeszcze tu zjeść."),
       ("Mam nadzieję, że jeszcze pobiegam.", "biegać", "Oby udało się jeszcze pobiegać."),
       ("Mam nadzieję, że jeszcze poczytam.", "czytać", "Oby udało się jeszcze poczytać."),
       ("Mam nadzieję, że jeszcze pogotuję.", "gotować", "Oby udało się jeszcze pogotować."),
     ]),

# =====================================================================
# klua waa ja … mai dai — obawa
# =====================================================================
dict(key="KLUAWAA", ty="sentence", cat="Gramatyka użytkowa", sub="Obawy", reg="n",
     ph="phǒm klua wâa jà {ph} mâi dâai khráp", th="ผมกลัวว่าจะ{th}ไม่ได้ครับ",
     lit="klua wâa = bać się, że",
     note="„klua wâa” dotyczy obawy o przyszłość. Strach przed rzeczą to samo „klua” bez „wâa”.",
     ex_ph="klua wâa jà {ph} mâi dâai rǔe plào khráp", ex_th="กลัวว่าจะ{th}ไม่ได้หรือเปล่าครับ",
     items=[
       ("Boję się, że nie zdołam zapłacić.", "płacić", "Boisz się, że nie dasz rady zapłacić?"),
       ("Boję się, że nie zdołam wrócić na czas.", "wracać", "Boisz się, że nie zdążysz wrócić?"),
       ("Boję się, że nie zdołam tego znaleźć.", "znaleźć", "Boisz się, że nie znajdziesz?"),
       ("Boję się, że nie zdołam się dodzwonić.", "dzwonić", "Boisz się, że się nie dodzwonisz?"),
       ("Boję się, że nie zdołam zarezerwować.", "rezerwować", "Boisz się, że nie zarezerwujesz?"),
       ("Boję się, że nie zdołam tego zmienić.", "zmieniać", "Boisz się, że nie zmienisz?"),
       ("Boję się, że nie zdołam się spakować.", "pakować się", "Boisz się, że się nie spakujesz?"),
       ("Boję się, że nie zdołam się nauczyć.", "uczyć się", "Boisz się, że się nie nauczysz?"),
       ("Boję się, że nie zdołam się wyspać.", "spać", "Boisz się, że się nie wyśpisz?"),
       ("Boję się, że nie zdołam tego zrozumieć.", "rozumieć", "Boisz się, że nie zrozumiesz?"),
       ("Boję się, że nie zdołam tego kupić.", "kupować", "Boisz się, że nie kupisz?"),
       ("Boję się, że nie zdołam wynająć.", "wynajmować", "Boisz się, że nie wynajmiesz?"),
       ("Boję się, że nie zdołam tego wysłać.", "wysyłać", "Boisz się, że nie wyślesz?"),
       ("Boję się, że nie zdołam wsiąść.", "wsiadać", "Boisz się, że nie wsiądziesz?"),
       ("Boję się, że nie zdołam się przesiąść.", "przesiadać się", "Boisz się, że się nie przesiądziesz?"),
       ("Boję się, że nie zdołam zamówić po tajsku.", "zamawiać", "Boisz się, że nie zamówisz?"),
       ("Boję się, że nie zdołam tego wypełnić.", "wypełnić formularz", "Boisz się, że nie wypełnisz?"),
       ("Boję się, że nie zdołam się z nim spotkać.", "spotykać", "Boisz się, że się nie spotkacie?"),
       ("Boję się, że nie zdołam odpocząć.", "odpoczywać", "Boisz się, że nie odpoczniesz?"),
       ("Boję się, że nie zdołam tego podpisać.", "podpisać", "Boisz się, że nie podpiszesz?"),
     ]),

# =====================================================================
# pha-yaa-yaam ja … hai dai — staranie
# =====================================================================
dict(key="PHAYAAYAAM", ty="sentence", cat="Gramatyka użytkowa", sub="Cele", reg="n",
     ph="phǒm phá-yaa-yaam jà {ph} hâi dâai khráp", th="ผมพยายามจะ{th}ให้ได้ครับ",
     lit="phá-yaa-yaam = starać się, usiłować",
     note="Końcówka „hâi dâai” dodaje upór: „aż mi się uda”. Bez niej zdanie brzmi biernie.",
     ex_ph="phá-yaa-yaam {ph} yùu khráp", ex_th="พยายาม{th}อยู่ครับ",
     items=[
       ("Staram się nauczyć tego na pamięć.", "uczyć się", "Cały czas się uczę."),
       ("Staram się to zrozumieć.", "rozumieć", "Cały czas próbuję zrozumieć."),
       ("Staram się mówić po tajsku.", "mówić", "Cały czas próbuję mówić."),
       ("Staram się to naprawić.", "robić", "Cały czas nad tym pracuję."),
       ("Staram się wstawać wcześniej.", "wstawać", "Cały czas próbuję wstawać wcześniej."),
       ("Staram się to skończyć na czas.", "kończyć się", "Cały czas próbuję to domknąć."),
       ("Staram się więcej biegać.", "biegać", "Cały czas próbuję biegać."),
       ("Staram się gotować w domu.", "gotować", "Cały czas próbuję gotować."),
       ("Staram się mniej wydawać.", "płacić", "Cały czas pilnuję wydatków."),
       ("Staram się więcej czytać.", "czytać", "Cały czas próbuję czytać."),
       ("Staram się to zapamiętać.", "pamiętać", "Cały czas próbuję zapamiętać."),
       ("Staram się nie zapominać.", "zapominać", "Cały czas o tym pamiętam."),
       ("Staram się z nimi spotykać.", "spotykać", "Cały czas próbuję się spotykać."),
       ("Staram się to znaleźć.", "znaleźć", "Cały czas szukam."),
       ("Staram się przyjeżdżać punktualnie.", "przyjść / przyjechać", "Cały czas próbuję zdążyć."),
       ("Staram się odpowiadać od razu.", "odpowiadać", "Cały czas staram się odpowiadać."),
       ("Staram się słuchać uważnie.", "słuchać", "Cały czas próbuję słuchać."),
       ("Staram się pisać codziennie.", "pisać", "Cały czas próbuję pisać."),
       ("Staram się pomagać, kiedy mogę.", "pomagać", "Cały czas staram się pomagać."),
       ("Staram się odpoczywać w weekendy.", "odpoczywać", "Cały czas próbuję odpoczywać."),
     ]),

# =====================================================================
# kwaa … ja … sèt — „zanim skoncze”
# =====================================================================
dict(key="KWAAJA", ty="sentence", cat="Gramatyka użytkowa", sub="Czas", reg="n",
     ph="kwàa phǒm jà {ph} sèt kâw naan khráp", th="กว่าผมจะ{th}เสร็จก็นานครับ",
     lit="kwàa … jà … = zanim zdąży się…",
     note="„kwàa … jà …” zawsze niesie odcień „to trwa zbyt długo”. To nie jest neutralne „zanim”.",
     ex_ph="kwàa jà {ph} sèt tâwng chái wee-laa naan mǎi khráp",
     ex_th="กว่าจะ{th}เสร็จต้องใช้เวลานานไหมครับ",
     items=[
       ("Zanim skończę gotować, minie sporo czasu.", "gotować", "Długo trwa gotowanie?"),
       ("Zanim skończę prać, minie sporo czasu.", "prać", "Długo trwa pranie?"),
       ("Zanim skończę pisać, minie sporo czasu.", "pisać", "Długo trwa pisanie?"),
       ("Zanim skończę czytać, minie sporo czasu.", "czytać", "Długo trwa czytanie?"),
       ("Zanim skończę się pakować, minie sporo czasu.", "pakować się", "Długo trwa pakowanie?"),
       ("Zanim skończę sprzątać, minie sporo czasu.", "myć", "Długo trwa sprzątanie?"),
       ("Zanim skończę wybierać, minie sporo czasu.", "wybierać", "Długo trwa wybieranie?"),
       ("Zanim skończę wypełniać wniosek, minie sporo czasu.", "wypełnić formularz", "Długo trwa wypełnianie?"),
       ("Zanim skończę zamawiać, minie sporo czasu.", "zamawiać", "Długo trwa zamawianie?"),
       ("Zanim skończę pracę, minie sporo czasu.", "pracować", "Długo jeszcze zostaniesz w pracy?"),
       ("Zanim skończę się uczyć, minie sporo czasu.", "uczyć się", "Długo trwa nauka?"),
       ("Zanim skończę zwiedzać, minie sporo czasu.", "zwiedzać", "Długo trwa zwiedzanie?"),
       ("Zanim skończę szukać, minie sporo czasu.", "szukać", "Długo trwa szukanie?"),
       ("Zanim skończę oglądać, minie sporo czasu.", "oglądać", "Długo trwa oglądanie?"),
       ("Zanim skończę płacić, minie sporo czasu.", "płacić", "Długo trwa płacenie?"),
     ]),

# =====================================================================
# thaa pen phom — „na twoim miejscu”
# =====================================================================
dict(key="THAAPENPHOM", ty="sentence", cat="Gramatyka użytkowa", sub="Rada", reg="n",
     ph="thâa pen phǒm phǒm jà {ph} khráp", th="ถ้าเป็นผมผมจะ{th}ครับ",
     lit="thâa pen phǒm = gdybym to był ja",
     note="Uprzejmy sposób doradzania. Tryb rozkazujący jest w tajskim odbierany jako szorstki.",
     ex_ph="thâa pen khun khun jà {ph} mǎi khráp", ex_th="ถ้าเป็นคุณคุณจะ{th}ไหมครับ",
     items=[
       ("Na twoim miejscu bym zapytał.", "pytać", "A ty byś zapytał?"),
       ("Na twoim miejscu bym zaczekał.", "czekać", "A ty byś zaczekał?"),
       ("Na twoim miejscu bym zarezerwował.", "rezerwować", "A ty byś zarezerwował?"),
       ("Na twoim miejscu bym to zmienił.", "zmieniać", "A ty byś zmienił?"),
       ("Na twoim miejscu bym to anulował.", "anulować", "A ty byś anulował?"),
       ("Na twoim miejscu bym zapłacił od razu.", "płacić", "A ty byś zapłacił?"),
       ("Na twoim miejscu bym wrócił.", "wracać", "A ty byś wrócił?"),
       ("Na twoim miejscu bym odpoczął.", "odpoczywać", "A ty byś odpoczął?"),
       ("Na twoim miejscu bym poszukał czegoś innego.", "szukać", "A ty byś poszukał?"),
       ("Na twoim miejscu bym z nim porozmawiał.", "rozmawiać", "A ty byś porozmawiał?"),
       ("Na twoim miejscu bym to sprzedał.", "sprzedawać", "A ty byś sprzedał?"),
       ("Na twoim miejscu bym najpierw przymierzył.", "przymierzać / próbować", "A ty byś przymierzył?"),
       ("Na twoim miejscu bym zadzwonił.", "dzwonić", "A ty byś zadzwonił?"),
       ("Na twoim miejscu bym się przesiadł.", "przesiadać się", "A ty byś się przesiadł?"),
       ("Na twoim miejscu bym poszedł pieszo.", "iść pieszo", "A ty byś poszedł pieszo?"),
       ("Na twoim miejscu bym przestał.", "przestać", "A ty byś przestał?"),
       ("Na twoim miejscu bym to podpisał.", "podpisać", "A ty byś podpisał?"),
       ("Na twoim miejscu bym wynajął coś tańszego.", "wynajmować", "A ty byś wynajął?"),
     ]),

# =====================================================================
# mai nae-jai waa ja … dai rue plao — niepewnosc
# =====================================================================
dict(key="MAINAEJAI", ty="sentence", cat="Gramatyka użytkowa", sub="Niepewność", reg="n",
     ph="phǒm mâi nâe-jai wâa jà {ph} dâai rǔe plào khráp",
     th="ผมไม่แน่ใจว่าจะ{th}ได้หรือเปล่าครับ",
     lit="mâi nâe-jai wâa … rǔe plào = nie wiem, czy … czy nie",
     note="Para „rǔe plào” na końcu tworzy pytanie zależne. To jedna z konstrukcji, które najbardziej podnoszą poziom wypowiedzi.",
     ex_ph="{ph} dâai rǔe plào khráp", ex_th="{th}ได้หรือเปล่าครับ",
     items=[
       ("Nie jestem pewien, czy dam radę przyjechać.", "przyjść / przyjechać", "Da się przyjechać?"),
       ("Nie jestem pewien, czy dam radę zapłacić.", "płacić", "Da się zapłacić?"),
       ("Nie jestem pewien, czy dam radę to zrobić.", "robić", "Da się to zrobić?"),
       ("Nie jestem pewien, czy dam radę zdążyć.", "zaczynać", "Da się zacząć na czas?"),
       ("Nie jestem pewien, czy dam radę wynająć.", "wynajmować", "Da się wynająć?"),
       ("Nie jestem pewien, czy dam radę to zmienić.", "zmieniać", "Da się zmienić?"),
       ("Nie jestem pewien, czy dam radę to znaleźć.", "znaleźć", "Da się znaleźć?"),
       ("Nie jestem pewien, czy dam radę zarezerwować.", "rezerwować", "Da się zarezerwować?"),
       ("Nie jestem pewien, czy dam radę pożyczyć.", "pożyczyć", "Da się pożyczyć?"),
       ("Nie jestem pewien, czy dam radę to wysłać.", "wysyłać", "Da się wysłać?"),
       ("Nie jestem pewien, czy dam radę wrócić dziś.", "wracać", "Da się wrócić dzisiaj?"),
       ("Nie jestem pewien, czy dam radę tam wejść.", "wchodzić", "Da się wejść?"),
       ("Nie jestem pewien, czy dam radę się przesiąść.", "przesiadać się", "Da się przesiąść?"),
       ("Nie jestem pewien, czy dam radę to obejrzeć.", "oglądać", "Da się obejrzeć?"),
       ("Nie jestem pewien, czy dam radę wypełnić wniosek.", "wypełnić formularz", "Da się wypełnić?"),
       ("Nie jestem pewien, czy dam radę zamówić po tajsku.", "zamawiać", "Da się zamówić?"),
     ]),

# =====================================================================
# kueap … sèt laew — przyblizenie
# =====================================================================
dict(key="KUEAP", ty="sentence", cat="Gramatyka użytkowa", sub="Postęp", reg="n",
     ph="phǒm {ph} kùeap sèt láew khráp", th="ผม{th}เกือบเสร็จแล้วครับ",
     lit="kùeap = prawie, o mało co",
     note="„kùeap” dotyczy stanu bliskiego zakończeniu. Nie myl z „phaw dii” = akurat.",
     ex_ph="{ph} kùeap sèt rǔe yang khráp", ex_th="{th}เกือบเสร็จหรือยังครับ",
     items=[
       ("Prawie skończyłem gotować.", "gotować", "Skończyłeś już gotować?"),
       ("Prawie skończyłem prać.", "prać", "Skończyłeś już prać?"),
       ("Prawie skończyłem pisać.", "pisać", "Skończyłeś już pisać?"),
       ("Prawie skończyłem czytać.", "czytać", "Skończyłeś już czytać?"),
       ("Prawie skończyłem się pakować.", "pakować się", "Skończyłeś się pakować?"),
       ("Prawie skończyłem jeść.", "jeść", "Skończyłeś już jeść?"),
       ("Prawie skończyłem pracę.", "pracować", "Skończyłeś już pracę?"),
       ("Prawie skończyłem naukę.", "uczyć się", "Skończyłeś już naukę?"),
       ("Prawie skończyłem wybierać.", "wybierać", "Skończyłeś już wybierać?"),
       ("Prawie skończyłem zamawiać.", "zamawiać", "Skończyłeś już zamawiać?"),
       ("Prawie skończyłem sprzątać.", "myć", "Skończyłeś już sprzątać?"),
       ("Prawie skończyłem oglądać.", "oglądać", "Skończyłeś już oglądać?"),
       ("Prawie skończyłem zwiedzać.", "zwiedzać", "Skończyłeś już zwiedzać?"),
       ("Prawie skończyłem wypełniać wniosek.", "wypełnić formularz", "Skończyłeś już wypełniać?"),
     ]),

# =====================================================================
# … maa naan laew — czynnosc trwajaca do teraz
# =====================================================================
dict(key="MAANAAN", ty="sentence", cat="Gramatyka użytkowa", sub="Przeszłość", reg="n",
     ph="phǒm {ph} maa naan láew khráp", th="ผม{th}มานานแล้วครับ",
     lit="… maa naan láew = robię to już od dawna",
     note="Polski używa tu czasu teraźniejszego („robię od dawna”), tajski — „maa … láew”. Kalka z polskiego zgubiłaby ciągłość.",
     ex_ph="{ph} maa naan thâo-rài láew khráp", ex_th="{th}มานานเท่าไหร่แล้วครับ",
     items=[
       ("Uczę się tego od dawna.", "uczyć się", "Od jak dawna się uczysz?"),
       ("Pracuję tu od dawna.", "pracować", "Od jak dawna tu pracujesz?"),
       ("Czekam już od dawna.", "czekać", "Od jak dawna czekasz?"),
       ("Szukam tego od dawna.", "szukać", "Od jak dawna szukasz?"),
       ("Mieszkam tu od dawna.", "siedzieć", "Od jak dawna tu siedzisz?"),
       ("Biegam od dawna.", "biegać", "Od jak dawna biegasz?"),
       ("Gotuję sam od dawna.", "gotować", "Od jak dawna gotujesz?"),
       ("Pływam od dawna.", "pływać", "Od jak dawna pływasz?"),
       ("Prowadzę samochód od dawna.", "prowadzić samochód", "Od jak dawna prowadzisz?"),
       ("Śpiewam od dawna.", "śpiewać", "Od jak dawna śpiewasz?"),
       ("Tańczę od dawna.", "tańczyć", "Od jak dawna tańczysz?"),
       ("Piszę od dawna.", "pisać", "Od jak dawna piszesz?"),
       ("Znam go od dawna.", "znać", "Od jak dawna go znasz?"),
       ("Wynajmuję to od dawna.", "wynajmować", "Od jak dawna wynajmujesz?"),
       ("Płacę za to od dawna.", "płacić", "Od jak dawna płacisz?"),
       ("Robię zdjęcia od dawna.", "robić zdjęcia", "Od jak dawna robisz zdjęcia?"),
     ]),

# =====================================================================
# mai waa yang-ngai kaw ja — uporczywosc
# =====================================================================
dict(key="MAIWAA", ty="sentence", cat="Gramatyka użytkowa", sub="Postanowienie", reg="n",
     ph="mâi wâa yang-ngai phǒm kâw jà {ph} khráp", th="ไม่ว่ายังไงผมก็จะ{th}ครับ",
     lit="mâi wâa yang-ngai … kâw = tak czy inaczej, mimo wszystko",
     note="Konstrukcja „mâi wâa …, kâw …” działa z każdym pytajnikiem: mâi wâa khrai, mâi wâa thîi nǎi.",
     ex_ph="mâi wâa yang-ngai kâw tâwng {ph} khráp", ex_th="ไม่ว่ายังไงก็ต้อง{th}ครับ",
     items=[
       ("Tak czy inaczej pojadę.", "iść / jechać", "Tak czy inaczej trzeba jechać."),
       ("Tak czy inaczej zapłacę.", "płacić", "Tak czy inaczej trzeba zapłacić."),
       ("Tak czy inaczej zapytam.", "pytać", "Tak czy inaczej trzeba zapytać."),
       ("Tak czy inaczej wrócę.", "wracać", "Tak czy inaczej trzeba wrócić."),
       ("Tak czy inaczej spróbuję.", "próbować (smakować)", "Tak czy inaczej trzeba spróbować."),
       ("Tak czy inaczej się nauczę.", "uczyć się", "Tak czy inaczej trzeba się nauczyć."),
       ("Tak czy inaczej to skończę.", "kończyć się", "Tak czy inaczej trzeba skończyć."),
       ("Tak czy inaczej zarezerwuję.", "rezerwować", "Tak czy inaczej trzeba zarezerwować."),
       ("Tak czy inaczej to wyślę.", "wysyłać", "Tak czy inaczej trzeba wysłać."),
       ("Tak czy inaczej zadzwonię.", "dzwonić", "Tak czy inaczej trzeba zadzwonić."),
       ("Tak czy inaczej poczekam.", "czekać", "Tak czy inaczej trzeba poczekać."),
       ("Tak czy inaczej to podpiszę.", "podpisać", "Tak czy inaczej trzeba podpisać."),
       ("Tak czy inaczej się spakuję.", "pakować się", "Tak czy inaczej trzeba się spakować."),
       ("Tak czy inaczej pójdę pieszo.", "iść pieszo", "Tak czy inaczej trzeba iść pieszo."),
     ]),

# =====================================================================
# thueng mae waa ja yaak kaw ja — ustepstwo
# =====================================================================
dict(key="THUENGMAE", ty="sentence", cat="Gramatyka użytkowa", sub="Ustępstwo", reg="f",
     ph="thǔeng máe wâa jà yâak phǒm kâw jà {ph} khráp",
     th="ถึงแม้ว่าจะยากผมก็จะ{th}ครับ",
     lit="thǔeng máe wâa … kâw … = chociaż…, to jednak…",
     note="Rejestr wyższy niż „tàae”. Dobrze wypada na zebraniu i w piśmie.",
     ex_ph="thǔeng máe wâa jà yâak kâw tâwng {ph} khráp", ex_th="ถึงแม้ว่าจะยากก็ต้อง{th}ครับ",
     items=[
       ("Chociaż to trudne, i tak spróbuję.", "próbować (smakować)", "Chociaż trudne, trzeba spróbować."),
       ("Chociaż to trudne, i tak się nauczę.", "uczyć się", "Chociaż trudne, trzeba się uczyć."),
       ("Chociaż to trudne, i tak to zrobię.", "robić", "Chociaż trudne, trzeba to zrobić."),
       ("Chociaż to trudne, i tak zapłacę.", "płacić", "Chociaż trudne, trzeba zapłacić."),
       ("Chociaż to trudne, i tak pojadę.", "iść / jechać", "Chociaż trudne, trzeba jechać."),
       ("Chociaż to trudne, i tak zapytam.", "pytać", "Chociaż trudne, trzeba zapytać."),
       ("Chociaż to trudne, i tak poczekam.", "czekać", "Chociaż trudne, trzeba poczekać."),
       ("Chociaż to trudne, i tak to wyślę.", "wysyłać", "Chociaż trudne, trzeba wysłać."),
       ("Chociaż to trudne, i tak porozmawiam.", "rozmawiać", "Chociaż trudne, trzeba porozmawiać."),
       ("Chociaż to trudne, i tak to zmienię.", "zmieniać", "Chociaż trudne, trzeba zmienić."),
       ("Chociaż to trudne, i tak wrócę.", "wracać", "Chociaż trudne, trzeba wrócić."),
       ("Chociaż to trudne, i tak poszukam.", "szukać", "Chociaż trudne, trzeba szukać."),
     ]),

# =====================================================================
# lawng … duu laew tae yang mai dai — nieudana proba
# =====================================================================
dict(key="LAWNGTAE", ty="sentence", cat="Gramatyka użytkowa", sub="Problemy", reg="n",
     ph="phǒm lawng {ph} duu láew tàae yang mâi dâai khráp",
     th="ผมลอง{th}ดูแล้วแต่ยังไม่ได้ครับ",
     lit="lawng … duu = spróbować i zobaczyć, co z tego wyjdzie",
     note="„lawng … duu” to próba na spróbowanie. Bez „duu” zdanie brzmi jak deklaracja, nie eksperyment.",
     ex_ph="lawng {ph} duu rǔe yang khráp", ex_th="ลอง{th}ดูหรือยังครับ",
     items=[
       ("Próbowałem zadzwonić, ale nie wyszło.", "dzwonić", "Próbowałeś już dzwonić?"),
       ("Próbowałem zarezerwować, ale nie wyszło.", "rezerwować", "Próbowałeś już rezerwować?"),
       ("Próbowałem to zmienić, ale nie wyszło.", "zmieniać", "Próbowałeś już zmieniać?"),
       ("Próbowałem zapłacić, ale nie wyszło.", "płacić", "Próbowałeś już zapłacić?"),
       ("Próbowałem to znaleźć, ale nie wyszło.", "znaleźć", "Próbowałeś już szukać?"),
       ("Próbowałem to otworzyć, ale nie wyszło.", "otwierać", "Próbowałeś już otwierać?"),
       ("Próbowałem to wysłać, ale nie wyszło.", "wysyłać", "Próbowałeś już wysyłać?"),
       ("Próbowałem to anulować, ale nie wyszło.", "anulować", "Próbowałeś już anulować?"),
       ("Próbowałem wynająć, ale nie wyszło.", "wynajmować", "Próbowałeś już wynajmować?"),
       ("Próbowałem się dodzwonić i zapytać, ale nie wyszło.", "pytać", "Próbowałeś już pytać?"),
       ("Próbowałem to naprawić, ale nie wyszło.", "robić", "Próbowałeś już coś z tym zrobić?"),
       ("Próbowałem to wypełnić, ale nie wyszło.", "wypełnić formularz", "Próbowałeś już wypełniać?"),
       ("Próbowałem to przymierzyć, ale nie wyszło.", "przymierzać / próbować", "Próbowałeś już przymierzać?"),
       ("Próbowałem się przesiąść, ale nie wyszło.", "przesiadać się", "Próbowałeś się przesiadać?"),
     ]),

# =====================================================================
# thaa mii oo-kaat — okazja
# =====================================================================
dict(key="MIIOKAAT", ty="sentence", cat="Gramatyka użytkowa", sub="Plany", reg="n",
     ph="thâa mii oo-kàat phǒm yàak {ph} ìik khráp", th="ถ้ามีโอกาสผมอยาก{th}อีกครับ",
     lit="oo-kàat = okazja, sposobność",
     note="Bardzo częsty sposób mówienia o planach bez zobowiązania.",
     ex_ph="thâa mii oo-kàot yàak {ph} ìik mǎi khráp", ex_th="ถ้ามีโอกาสอยาก{th}อีกไหมครับ",
     items=[
       ("Jeśli będzie okazja, chętnie znów tu przyjadę.", "przyjść / przyjechać", "Przyjechałbyś tu jeszcze?"),
       ("Jeśli będzie okazja, chętnie znów popływam.", "pływać", "Popływałbyś jeszcze?"),
       ("Jeśli będzie okazja, chętnie znów pozwiedzam.", "zwiedzać", "Pozwiedzałbyś jeszcze?"),
       ("Jeśli będzie okazja, chętnie znów spróbuję.", "próbować (smakować)", "Spróbowałbyś jeszcze?"),
       ("Jeśli będzie okazja, chętnie znów tu popracuję.", "pracować", "Popracowałbyś tu jeszcze?"),
       ("Jeśli będzie okazja, chętnie znów się spotkamy.", "spotykać", "Spotkalibyśmy się jeszcze?"),
       ("Jeśli będzie okazja, chętnie znów pobiegam.", "biegać", "Pobiegałbyś jeszcze?"),
       ("Jeśli będzie okazja, chętnie znów pogotuję.", "gotować", "Pogotowałbyś jeszcze?"),
       ("Jeśli będzie okazja, chętnie znów tu zjem.", "jeść", "Zjadłbyś tu jeszcze?"),
       ("Jeśli będzie okazja, chętnie znów potańczę.", "tańczyć", "Potańczyłbyś jeszcze?"),
       ("Jeśli będzie okazja, chętnie znów wynajmę tu pokój.", "wynajmować", "Wynająłbyś tu jeszcze?"),
       ("Jeśli będzie okazja, chętnie znów się pouczę.", "uczyć się", "Pouczyłbyś się jeszcze?"),
     ]),

# =====================================================================
# tawng … hai dai wan nii — koniecznosc terminowa
# =====================================================================
dict(key="TAWNGHAIDAI", ty="sentence", cat="Gramatyka użytkowa", sub="Konieczność", reg="n",
     ph="wan níi phǒm tâwng {ph} hâi dâai khráp", th="วันนี้ผมต้อง{th}ให้ได้ครับ",
     lit="tâwng … hâi dâai = muszę i koniec",
     note="„hâi dâai” po czasowniku podnosi zwykłe „tâwng” do poziomu twardego postanowienia.",
     ex_ph="wan níi tâwng {ph} hâi dâai loei rǒe khráp", ex_th="วันนี้ต้อง{th}ให้ได้เลยหรือครับ",
     items=[
       ("Dziś muszę to koniecznie skończyć.", "kończyć się", "Koniecznie dziś?"),
       ("Dziś muszę koniecznie zapłacić.", "płacić", "Koniecznie dziś płacić?"),
       ("Dziś muszę koniecznie wysłać.", "wysyłać", "Koniecznie dziś wysłać?"),
       ("Dziś muszę koniecznie podpisać.", "podpisać", "Koniecznie dziś podpisać?"),
       ("Dziś muszę koniecznie zarezerwować.", "rezerwować", "Koniecznie dziś rezerwować?"),
       ("Dziś muszę koniecznie zadzwonić.", "dzwonić", "Koniecznie dziś dzwonić?"),
       ("Dziś muszę koniecznie się spakować.", "pakować się", "Koniecznie dziś się pakować?"),
       ("Dziś muszę koniecznie to znaleźć.", "znaleźć", "Koniecznie dziś znaleźć?"),
       ("Dziś muszę koniecznie odpocząć.", "odpoczywać", "Koniecznie dziś odpoczywać?"),
       ("Dziś muszę koniecznie to zmienić.", "zmieniać", "Koniecznie dziś zmieniać?"),
       ("Dziś muszę koniecznie wypełnić wniosek.", "wypełnić formularz", "Koniecznie dziś wypełniać?"),
       ("Dziś muszę koniecznie z nim porozmawiać.", "rozmawiać", "Koniecznie dziś rozmawiać?"),
     ]),

# =====================================================================
# khaw-thoot thii … chaa — przeprosiny za zwloke
# =====================================================================
dict(key="THIICHAA", ty="sentence", cat="Podstawy i grzeczność", sub="Przeprosiny", reg="f",
     ph="khǎw-thôot thîi {ph} cháa khráp", th="ขอโทษที่{th}ช้าครับ",
     lit="khǎw-thôot thîi … = przepraszam, że…",
     note="Po „khǎw-thôot thîi” idzie czasownik, nie rzeczownik. Kalka „przepraszam za opóźnienie” dałaby inną konstrukcję.",
     ex_ph="mâi pen rai khráp {ph} cháa nít diao", ex_th="ไม่เป็นไรครับ {th}ช้านิดเดียว",
     items=[
       ("Przepraszam, że odpowiadam z opóźnieniem.", "odpowiadać", "Nic nie szkodzi, to drobne opóźnienie."),
       ("Przepraszam, że wysyłam z opóźnieniem.", "wysyłać", "Nic nie szkodzi, wysłałeś prawie na czas."),
       ("Przepraszam, że przychodzę z opóźnieniem.", "przyjść / przyjechać", "Nic nie szkodzi, tylko chwilę."),
       ("Przepraszam, że dzwonię tak późno.", "dzwonić", "Nic nie szkodzi, dzwonisz w porę."),
       ("Przepraszam, że płacę z opóźnieniem.", "płacić", "Nic nie szkodzi, to niewielkie opóźnienie."),
       ("Przepraszam, że piszę z opóźnieniem.", "pisać", "Nic nie szkodzi, napisałeś prawie na czas."),
       ("Przepraszam, że odbieram tak późno.", "odbierać", "Nic nie szkodzi, odebrałeś szybko."),
       ("Przepraszam, że zaczynam z opóźnieniem.", "zaczynać", "Nic nie szkodzi, zaczęliśmy prawie punktualnie."),
       ("Przepraszam, że zamawiam tak późno.", "zamawiać", "Nic nie szkodzi, zdążyłeś."),
       ("Przepraszam, że wracam tak późno.", "wracać", "Nic nie szkodzi, wróciłeś prawie na czas."),
     ]),
]
