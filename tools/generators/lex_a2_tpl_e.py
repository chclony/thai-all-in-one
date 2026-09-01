# -*- coding: utf-8 -*-
"""Wzorce zdaniowe etapu 3 (A2) — czesc E: powinnosc, dokonanie, doprecyzowanie.

Pozycja: (polskie haslo rekordu, polskie haslo bazowe, polski przyklad)
"""

TPL_E = [

# =====================================================================
# khuan … mai — „czy powinienem"
# =====================================================================
dict(key="KHUAN", ty="question", cat="Pytania", sub="Rada", reg="n",
     ph="phǒm khuan {ph} mǎi khráp", th="ผมควร{th}ไหมครับ",
     lit="khuan = powinno się",
     note="„khuan” prosi o radę, „tâwng” mówi o przymusie. Mylenie ich brzmi natrętnie.",
     ex_ph="khuan {ph} khráp", ex_th="ควร{th}ครับ",
     items=[
       ("Czy powinienem czekać?", "czekać", "Powinien pan poczekać."),
       ("Czy powinienem zadzwonić?", "dzwonić", "Powinien pan zadzwonić."),
       ("Czy powinienem zarezerwować?", "rezerwować", "Powinien pan zarezerwować."),
       ("Czy powinienem zapłacić teraz?", "płacić", "Powinien pan zapłacić."),
       ("Czy powinienem zapytać?", "pytać", "Powinien pan zapytać."),
       ("Czy powinienem to zmienić?", "zmieniać", "Powinien pan to zmienić."),
       ("Czy powinienem się przesiąść?", "przesiadać się", "Powinien pan się przesiąść."),
       ("Czy powinienem tu wysiąść?", "wysiadać", "Powinien pan tu wysiąść."),
       ("Czy powinienem wracać?", "wracać", "Powinien pan wracać."),
       ("Czy powinienem odpocząć?", "odpoczywać", "Powinien pan odpocząć."),
       ("Czy powinienem to kupić?", "kupować", "Powinien pan to kupić."),
       ("Czy powinienem podpisać?", "podpisać", "Powinien pan podpisać."),
       ("Czy powinienem wypełnić formularz?", "wypełnić formularz", "Powinien pan wypełnić formularz."),
       ("Czy powinienem to pokazać?", "pokazać", "Powinien pan to pokazać."),
       ("Czy powinienem się spakować?", "pakować się", "Powinien pan się spakować."),
       ("Czy powinienem to anulować?", "anulować", "Powinien pan to anulować."),
       ("Czy powinienem tu zaczekać i się zatrzymać?", "zatrzymać się", "Powinien pan się zatrzymać."),
       ("Czy powinienem się uczyć więcej?", "uczyć się", "Powinien pan się uczyć."),
     ]),

# =====================================================================
# … mai than — „nie zdazylem"
# =====================================================================
dict(key="MAITHAN", ty="sentence", cat="Awarie i pomoc", sub="Problemy", reg="n",
     ph="phǒm {ph} mâi than khráp", th="ผม{th}ไม่ทันครับ",
     lit="… mâi than = nie zdążyć na czas",
     note="„than” zawsze idzie po czasowniku i dotyczy wyłącznie czasu, nie umiejętności.",
     ex_ph="{ph} mâi than rǔe khráp", ex_th="{th}ไม่ทันหรือครับ",
     items=[
       ("Nie zdążyłem zjeść.", "jeść", "Nie zdążyłeś zjeść?"),
       ("Nie zdążyłem zapłacić.", "płacić", "Nie zdążyłeś zapłacić?"),
       ("Nie zdążyłem zadzwonić.", "dzwonić", "Nie zdążyłeś zadzwonić?"),
       ("Nie zdążyłem zamówić.", "zamawiać", "Nie zdążyłeś zamówić?"),
       ("Nie zdążyłem zarezerwować.", "rezerwować", "Nie zdążyłeś zarezerwować?"),
       ("Nie zdążyłem wsiąść.", "wsiadać", "Nie zdążyłeś wsiąść?"),
       ("Nie zdążyłem wysiąść.", "wysiadać", "Nie zdążyłeś wysiąść?"),
       ("Nie zdążyłem się przesiąść.", "przesiadać się", "Nie zdążyłeś się przesiąść?"),
       ("Nie zdążyłem się spakować.", "pakować się", "Nie zdążyłeś się spakować?"),
       ("Nie zdążyłem przeczytać.", "czytać", "Nie zdążyłeś przeczytać?"),
       ("Nie zdążyłem obejrzeć.", "oglądać", "Nie zdążyłeś obejrzeć?"),
       ("Nie zdążyłem odpowiedzieć.", "odpowiadać", "Nie zdążyłeś odpowiedzieć?"),
       ("Nie zdążyłem wysłać.", "wysyłać", "Nie zdążyłeś wysłać?"),
       ("Nie zdążyłem zwiedzić.", "zwiedzać", "Nie zdążyłeś zwiedzić?"),
       ("Nie zdążyłem kupić.", "kupować", "Nie zdążyłeś kupić?"),
       ("Nie zdążyłem podpisać.", "podpisać", "Nie zdążyłeś podpisać?"),
     ]),

# =====================================================================
# … yuu trong nai — „gdzie dokladnie"
# =====================================================================
dict(key="TRONGNAI", ty="question", cat="Pytania", sub="Miejsce", reg="n",
     ph="{ph} yùu trong nǎi khráp", th="{th}อยู่ตรงไหนครับ",
     lit="trong nǎi = w którym dokładnie punkcie",
     note="„thîi nǎi” pyta ogólnie o miejscowość, „trong nǎi” o konkretny punkt w zasięgu wzroku.",
     ex_ph="{ph} yùu trong nán khráp", ex_th="{th}อยู่ตรงนั้นครับ",
     items=[
       ("Gdzie dokładnie jest toaleta?", "toaleta", "Toaleta jest tam."),
       ("Gdzie dokładnie jest winda?", "winda", "Winda jest tam."),
       ("Gdzie dokładnie jest wejście?", "wejście", "Wejście jest tam."),
       ("Gdzie dokładnie jest wyjście?", "wyjście", "Wyjście jest tam."),
       ("Gdzie dokładnie jest bankomat?", "bankomat", "Bankomat jest tam."),
       ("Gdzie dokładnie jest przystanek?", "przystanek autobusowy", "Przystanek jest tam."),
       ("Gdzie dokładnie jest apteka?", "apteka", "Apteka jest tam."),
       ("Gdzie dokładnie jest kantor?", "kantor", "Kantor jest tam."),
       ("Gdzie dokładnie jest basen?", "basen", "Basen jest tam."),
       ("Gdzie dokładnie jest kuchnia?", "kuchnia", "Kuchnia jest tam."),
       ("Gdzie dokładnie jest przechowalnia bagażu?", "przechowalnia bagażu", "Przechowalnia jest tam."),
       ("Gdzie dokładnie jest pralnia?", "pralnia", "Pralnia jest tam."),
       ("Gdzie dokładnie jest kawiarnia?", "kawiarnia", "Kawiarnia jest tam."),
       ("Gdzie dokładnie jest most?", "most", "Most jest tam."),
       ("Gdzie dokładnie jest skrzyżowanie?", "skrzyżowanie", "Skrzyżowanie jest tam."),
       ("Gdzie dokładnie jest stacja benzynowa?", "stacja benzynowa", "Stacja jest tam."),
       ("Gdzie dokładnie jest sklep całodobowy?", "sklep całodobowy", "Sklep jest tam."),
       ("Gdzie dokładnie jest mój pokój?", "pokój", "Pokój jest tam."),
       ("Gdzie dokładnie jest moja walizka?", "walizka", "Walizka jest tam."),
       ("Gdzie dokładnie jest ten hotel?", "hotel", "Hotel jest tam."),
     ]),

# =====================================================================
# … kwaa thii khit — „niz myslalem"
# =====================================================================
dict(key="KWAAKHIT", ty="sentence", cat="Cechy i opinie", sub="Porównania", reg="n",
     ph="{ph} kwàa thîi khít wái khráp", th="{th}กว่าที่คิดไว้ครับ",
     lit="kwàa thîi khít wái = bardziej, niż zakładałem",
     note="Bardzo naturalna reakcja na zaskoczenie ceną, odległością albo smakiem.",
     ex_ph="{ph} kwàa thîi khít wái mâak khráp", ex_th="{th}กว่าที่คิดไว้มากครับ",
     items=[
       ("Drożej, niż myślałem.", "drogi", "Dużo drożej, niż myślałem."),
       ("Taniej, niż myślałem.", "tani", "Dużo taniej, niż myślałem."),
       ("Dalej, niż myślałem.", "daleki", "Dużo dalej, niż myślałem."),
       ("Bliżej, niż myślałem.", "bliski", "Dużo bliżej, niż myślałem."),
       ("Większe, niż myślałem.", "duży", "Dużo większe, niż myślałem."),
       ("Mniejsze, niż myślałem.", "mały", "Dużo mniejsze, niż myślałem."),
       ("Szybciej, niż myślałem.", "szybki", "Dużo szybciej, niż myślałem."),
       ("Wolniej, niż myślałem.", "wolny (powolny)", "Dużo wolniej, niż myślałem."),
       ("Ostrzejsze, niż myślałem.", "ostry (pikantny)", "Dużo ostrzejsze, niż myślałem."),
       ("Smaczniejsze, niż myślałem.", "smaczny", "Dużo smaczniejsze, niż myślałem."),
       ("Trudniejsze, niż myślałem.", "trudny", "Dużo trudniejsze, niż myślałem."),
       ("Łatwiejsze, niż myślałem.", "łatwy", "Dużo łatwiejsze, niż myślałem."),
       ("Cieplej, niż myślałem.", "gorący", "Dużo cieplej, niż myślałem."),
       ("Głośniej, niż myślałem.", "głośny", "Dużo głośniej, niż myślałem."),
       ("Ciekawsze, niż myślałem.", "interesujący", "Dużo ciekawsze, niż myślałem."),
       ("Ładniejsze, niż myślałem.", "ładny", "Dużo ładniejsze, niż myślałem."),
       ("Cięższe, niż myślałem.", "ciężki", "Dużo cięższe, niż myślałem."),
       ("Dłuższe, niż myślałem.", "długi", "Dużo dłuższe, niż myślałem."),
     ]),

# =====================================================================
# … phaw dii — „w sam raz"
# =====================================================================
dict(key="PHAWDII", ty="collocation", cat="Cechy i opinie", sub="Ocena", reg="n",
     ph="{ph} phaw dii khráp", th="{th}พอดีครับ",
     lit="phaw dii = akurat tyle, ile trzeba",
     note="Pochwała umiaru — bardzo częsta przy jedzeniu i przy przymierzaniu ubrań.",
     ex_ph="{ph} phaw dii loei khráp", ex_th="{th}พอดีเลยครับ",
     items=[
       ("W sam raz duże.", "duży", "Akurat w sam raz duże."),
       ("W sam raz małe.", "mały", "Akurat w sam raz małe."),
       ("W sam raz długie.", "długi", "Akurat w sam raz długie."),
       ("W sam raz krótkie.", "krótki", "Akurat w sam raz krótkie."),
       ("W sam raz gorące.", "gorący", "Akurat w sam raz gorące."),
       ("W sam raz zimne.", "zimny (o napoju)", "Akurat w sam raz zimne."),
       ("W sam raz ostre.", "ostry (pikantny)", "Akurat w sam raz ostre."),
       ("W sam raz słodkie.", "słodki", "Akurat w sam raz słodkie."),
       ("W sam raz słone.", "słony", "Akurat w sam raz słone."),
       ("W sam raz ciężkie.", "ciężki", "Akurat w sam raz ciężkie."),
       ("W sam raz szybkie.", "szybki", "Akurat w sam raz szybkie."),
       ("W sam raz jasne.", "jasny", "Akurat w sam raz jasne."),
       ("W sam raz drogie.", "drogi", "Akurat w sam raz drogie."),
       ("W sam raz wysokie.", "wysoki", "Akurat w sam raz wysokie."),
     ]),

# =====================================================================
# … set laew — „skonczylem"
# =====================================================================
dict(key="SETLAEW", ty="sentence", cat="Gramatyka użytkowa", sub="Przeszłość", reg="n",
     ph="phǒm {ph} sèt láew khráp", th="ผม{th}เสร็จแล้วครับ",
     lit="sèt láew = zakończone, gotowe",
     note="„sèt” dotyczy zakończenia czynności; „mòt” — wyczerpania zapasu.",
     ex_ph="{ph} sèt rǔe yang khráp", ex_th="{th}เสร็จหรือยังครับ",
     items=[
       ("Skończyłem jeść.", "jeść", "Skończyłeś jeść?"),
       ("Skończyłem pracę.", "pracować", "Skończyłeś pracę?"),
       ("Skończyłem gotować.", "gotować", "Skończyłeś gotować?"),
       ("Skończyłem prać.", "prać", "Skończyłeś prać?"),
       ("Skończyłem sprzątać.", "sprzątać", "Skończyłeś sprzątać?"),
       ("Skończyłem się pakować.", "pakować się", "Skończyłeś się pakować?"),
       ("Skończyłem czytać.", "czytać", "Skończyłeś czytać?"),
       ("Skończyłem pisać.", "pisać", "Skończyłeś pisać?"),
       ("Skończyłem się uczyć.", "uczyć się", "Skończyłeś się uczyć?"),
       ("Skończyłem zamawiać.", "zamawiać", "Skończyłeś zamawiać?"),
       ("Skończyłem wybierać.", "wybierać", "Skończyłeś wybierać?"),
       ("Skończyłem się myć.", "myć", "Skończyłeś się myć?"),
       ("Skończyłem naprawiać.", "naprawiać", "Skończyłeś naprawiać?"),
       ("Skończyłem zwiedzać.", "zwiedzać", "Skończyłeś zwiedzać?"),
       ("Skończyłem oglądać.", "oglądać", "Skończyłeś oglądać?"),
       ("Skończyłem wypełniać formularz.", "wypełnić formularz", "Skończyłeś wypełniać?"),
     ]),

# =====================================================================
# … taw — „bede dalej"
# =====================================================================
dict(key="TAWPAI", ty="sentence", cat="Gramatyka użytkowa", sub="Plany", reg="n",
     ph="phǒm jà {ph} tàw khráp", th="ผมจะ{th}ต่อครับ",
     lit="tàw = dalej, w dalszym ciągu",
     note="„tàw” po czasowniku znaczy kontynuację. To samo słowo tworzy „tàw pai” — dalej, w przyszłość.",
     ex_ph="jà {ph} tàw mǎi khráp", ex_th="จะ{th}ต่อไหมครับ",
     items=[
       ("Będę dalej pracował.", "pracować", "Będziesz dalej pracował?"),
       ("Będę dalej czekał.", "czekać", "Będziesz dalej czekał?"),
       ("Będę dalej czytał.", "czytać", "Będziesz dalej czytał?"),
       ("Będę dalej oglądał.", "oglądać", "Będziesz dalej oglądał?"),
       ("Będę się dalej uczył.", "uczyć się", "Będziesz się dalej uczył?"),
       ("Będę dalej szukał.", "szukać", "Będziesz dalej szukał?"),
       ("Będę dalej zwiedzał.", "zwiedzać", "Będziesz dalej zwiedzał?"),
       ("Będę dalej jechał.", "iść / jechać", "Będziesz dalej jechał?"),
       ("Będę dalej gotował.", "gotować", "Będziesz dalej gotował?"),
       ("Będę dalej pływał.", "pływać", "Będziesz dalej pływał?"),
       ("Będę dalej rozmawiał.", "rozmawiać", "Będziesz dalej rozmawiał?"),
       ("Będę dalej odpoczywał.", "odpoczywać", "Będziesz dalej odpoczywał?"),
       ("Będę dalej wynajmował ten pokój.", "wynajmować", "Będziesz dalej wynajmował?"),
       ("Będę dalej pisał.", "pisać", "Będziesz dalej pisał?"),
     ]),

# =====================================================================
# … duai kan mai — „zrobmy to razem"
# =====================================================================
dict(key="DUAIKAN", ty="question", cat="Small talk", sub="Propozycje", reg="i",
     ph="{ph} dûai kan mǎi khráp", th="{th}ด้วยกันไหมครับ",
     lit="dûai kan = razem, wspólnie",
     note="Cieplejsze niż samo „kan” — podkreśla, że robimy to wspólnie z rozmówcą.",
     ex_ph="{ph} dûai kan thòe", ex_th="{th}ด้วยกันเถอะ",
     items=[
       ("Zjemy razem?", "jeść", "Zjedzmy razem."),
       ("Napijemy się razem?", "pić", "Napijmy się razem."),
       ("Pogotujemy razem?", "gotować", "Pogotujmy razem."),
       ("Pójdziemy razem?", "iść / jechać", "Chodźmy razem."),
       ("Pójdziemy pieszo razem?", "iść pieszo", "Chodźmy pieszo razem."),
       ("Popływamy razem?", "pływać", "Popływajmy razem."),
       ("Pobiegamy razem?", "biegać", "Pobiegajmy razem."),
       ("Pouczymy się razem?", "uczyć się", "Pouczmy się razem."),
       ("Pozwiedzamy razem?", "zwiedzać", "Pozwiedzajmy razem."),
       ("Pooglądamy razem?", "oglądać", "Pooglądajmy razem."),
       ("Zatańczymy razem?", "tańczyć", "Zatańczmy razem."),
       ("Zaśpiewamy razem?", "śpiewać", "Zaśpiewajmy razem."),
       ("Zrobimy razem zdjęcie?", "robić zdjęcia", "Zróbmy razem zdjęcie."),
       ("Poczekamy razem?", "czekać", "Poczekajmy razem."),
       ("Wrócimy razem?", "wracać", "Wróćmy razem."),
       ("Zamówimy razem?", "zamawiać", "Zamówmy razem."),
     ]),

# =====================================================================
# jam … dai — „pamietam"
# =====================================================================
dict(key="JAMDAI", ty="sentence", cat="Gramatyka użytkowa", sub="Pamięć", reg="n",
     ph="phǒm jam {ph} dâai khráp", th="ผมจำ{th}ได้ครับ",
     lit="jam … dâai = udaje mi się to zapamiętać",
     note="Bez „dâai” zdanie znaczy „zapamiętuję”, z „dâai” — „pamiętam”.",
     ex_ph="jam {ph} dâai mǎi khráp", ex_th="จำ{th}ได้ไหมครับ",
     items=[
       ("Pamiętam tę drogę.", "ulica", "Pamiętasz tę ulicę?"),
       ("Pamiętam ten hotel.", "hotel", "Pamiętasz ten hotel?"),
       ("Pamiętam tę restaurację.", "restauracja", "Pamiętasz tę restaurację?"),
       ("Pamiętam ten targ.", "targ", "Pamiętasz ten targ?"),
       ("Pamiętam tę świątynię.", "świątynia", "Pamiętasz tę świątynię?"),
       ("Pamiętam tę plażę.", "plaża", "Pamiętasz tę plażę?"),
       ("Pamiętam ten przystanek.", "przystanek autobusowy", "Pamiętasz ten przystanek?"),
       ("Pamiętam tę cenę.", "cena", "Pamiętasz tę cenę?"),
       ("Pamiętam to hasło.", "hasło", "Pamiętasz to hasło?"),
       ("Pamiętam ten numer telefonu.", "telefon", "Pamiętasz ten numer?"),
       ("Pamiętam ten most.", "most", "Pamiętasz ten most?"),
       ("Pamiętam to skrzyżowanie.", "skrzyżowanie", "Pamiętasz to skrzyżowanie?"),
       ("Pamiętam tę kawiarnię.", "kawiarnia", "Pamiętasz tę kawiarnię?"),
       ("Pamiętam ten park.", "park", "Pamiętasz ten park?"),
     ]),

# =====================================================================
# … an nii dii mai — pytanie o konkretna sztuke
# =====================================================================
dict(key="ANNIIDII", ty="question", cat="Zakupy i pieniądze", sub="Wybór", reg="n",
     ph="{ph} an níi dii mǎi khráp", th="{th}อันนี้ดีไหมครับ",
     lit="an níi = ta konkretna sztuka",
     note="„an níi” wskazuje przedmiot, który trzymamy w ręku albo na który patrzymy.",
     ex_ph="{ph} an níi dii khráp", ex_th="{th}อันนี้ดีครับ",
     items=[
       ("Czy ta koszulka jest dobra?", "koszulka", "Ta koszulka jest dobra."),
       ("Czy te spodnie są dobre?", "spodnie", "Te spodnie są dobre."),
       ("Czy te buty są dobre?", "buty", "Te buty są dobre."),
       ("Czy ten kapelusz jest dobry?", "kapelusz", "Ten kapelusz jest dobry."),
       ("Czy ta torba jest dobra?", "torba", "Ta torba jest dobra."),
       ("Czy ta pamiątka jest dobra?", "pamiątka", "Ta pamiątka jest dobra."),
       ("Czy ta mapa jest dobra?", "mapa", "Ta mapa jest dobra."),
       ("Czy ta ładowarka jest dobra?", "ładowarka", "Ta ładowarka jest dobra."),
       ("Czy ta karta SIM jest dobra?", "karta SIM", "Ta karta SIM jest dobra."),
       ("Czy ten kask jest dobry?", "kask", "Ten kask jest dobry."),
       ("Czy ten rower jest dobry?", "rower", "Ten rower jest dobry."),
       ("Czy ten krem z filtrem jest dobry?", "krem z filtrem", "Ten krem jest dobry."),
       ("Czy ten lek jest dobry?", "lek", "Ten lek jest dobry."),
       ("Czy ten pokój jest dobry?", "pokój", "Ten pokój jest dobry."),
       ("Czy ta restauracja jest dobra?", "restauracja", "Ta restauracja jest dobra."),
       ("Czy ten hotel jest dobry?", "hotel", "Ten hotel jest dobry."),
     ]),
]
