# -*- coding: utf-8 -*-
"""Wzorce zdaniowe etapu 3 (A2) — czesc F: uzupelnienie puli.

Pozycja: (polskie haslo rekordu, polskie haslo bazowe, polski przyklad)
"""

TPL_F = [

# =====================================================================
# chuai bawk noi wa … yuu thii nai — uprzejme pytanie o droge
# =====================================================================
dict(key="BAWKTHAANG", ty="question", cat="Awarie i pomoc", sub="Prośby", reg="f",
     ph="chûai bàwk nòi khráp wâa {ph} yùu thîi nǎi", th="ช่วยบอกหน่อยครับว่า{th}อยู่ที่ไหน",
     lit="chûai bàwk nòi wâa … = proszę mi powiedzieć, że…",
     note="Dłuższa, uprzejmiejsza forma pytania o drogę niż samo „… yùu thîi nǎi”.",
     ex_ph="{ph} yùu thaang nǎi khráp", ex_th="{th}อยู่ทางไหนครับ",
     items=[
       ("Proszę mi powiedzieć, gdzie jest toaleta.", "toaleta", "W którą stronę jest toaleta?"),
       ("Proszę mi powiedzieć, gdzie jest apteka.", "apteka", "W którą stronę jest apteka?"),
       ("Proszę mi powiedzieć, gdzie jest szpital.", "szpital", "W którą stronę jest szpital?"),
       ("Proszę mi powiedzieć, gdzie jest bankomat.", "bankomat", "W którą stronę jest bankomat?"),
       ("Proszę mi powiedzieć, gdzie jest kantor.", "kantor", "W którą stronę jest kantor?"),
       ("Proszę mi powiedzieć, gdzie jest przystanek.", "przystanek autobusowy", "W którą stronę jest przystanek?"),
       ("Proszę mi powiedzieć, gdzie jest dworzec kolejowy.", "dworzec kolejowy", "W którą stronę jest dworzec?"),
       ("Proszę mi powiedzieć, gdzie jest targ.", "targ", "W którą stronę jest targ?"),
       ("Proszę mi powiedzieć, gdzie jest świątynia.", "świątynia", "W którą stronę jest świątynia?"),
       ("Proszę mi powiedzieć, gdzie jest plaża.", "plaża", "W którą stronę jest plaża?"),
       ("Proszę mi powiedzieć, gdzie jest poczta.", "poczta", "W którą stronę jest poczta?"),
       ("Proszę mi powiedzieć, gdzie jest pralnia.", "pralnia", "W którą stronę jest pralnia?"),
       ("Proszę mi powiedzieć, gdzie jest supermarket.", "supermarket", "W którą stronę jest supermarket?"),
       ("Proszę mi powiedzieć, gdzie jest park.", "park", "W którą stronę jest park?"),
       ("Proszę mi powiedzieć, gdzie jest most.", "most", "W którą stronę jest most?"),
       ("Proszę mi powiedzieć, gdzie jest kawiarnia.", "kawiarnia", "W którą stronę jest kawiarnia?"),
       ("Proszę mi powiedzieć, gdzie jest sklep całodobowy.", "sklep całodobowy", "W którą stronę jest sklep?"),
       ("Proszę mi powiedzieć, gdzie jest stacja benzynowa.", "stacja benzynowa", "W którą stronę jest stacja?"),
     ]),

# =====================================================================
# phoeng pai … maa — „bylem wlasnie w"
# =====================================================================
dict(key="PHOENGPAI", ty="sentence", cat="Gramatyka użytkowa", sub="Przeszłość", reg="n",
     ph="phǒm phôoeng pai {ph} maa khráp", th="ผมเพิ่งไป{th}มาครับ",
     lit="phôoeng pai … maa = dopiero co stamtąd wróciłem",
     note="Klamra „pai … maa” opisuje wyprawę zakończoną powrotem. Bez „maa” zdanie mówi tylko o wyjściu.",
     ex_ph="phôoeng pai {ph} maa rǔe khráp", ex_th="เพิ่งไป{th}มาหรือครับ",
     items=[
       ("Byłem właśnie na targu.", "targ", "Byłeś właśnie na targu?"),
       ("Byłem właśnie w aptece.", "apteka", "Byłeś właśnie w aptece?"),
       ("Byłem właśnie w banku.", "bank", "Byłeś właśnie w banku?"),
       ("Byłem właśnie na poczcie.", "poczta", "Byłeś właśnie na poczcie?"),
       ("Byłem właśnie w pralni.", "pralnia", "Byłeś właśnie w pralni?"),
       ("Byłem właśnie na plaży.", "plaża", "Byłeś właśnie na plaży?"),
       ("Byłem właśnie w parku.", "park", "Byłeś właśnie w parku?"),
       ("Byłem właśnie w świątyni.", "świątynia", "Byłeś właśnie w świątyni?"),
       ("Byłem właśnie w szpitalu.", "szpital", "Byłeś właśnie w szpitalu?"),
       ("Byłem właśnie w supermarkecie.", "supermarket", "Byłeś właśnie w supermarkecie?"),
       ("Byłem właśnie w centrum handlowym.", "centrum handlowe", "Byłeś właśnie w centrum?"),
       ("Byłem właśnie na masażu.", "salon masażu", "Byłeś właśnie na masażu?"),
       ("Byłem właśnie w kawiarni.", "kawiarnia", "Byłeś właśnie w kawiarni?"),
       ("Byłem właśnie na bazarze nocnym.", "bazar nocny", "Byłeś właśnie na bazarze?"),
       ("Byłem właśnie na lotnisku.", "lotnisko", "Byłeś właśnie na lotnisku?"),
       ("Byłem właśnie w hotelu.", "hotel", "Byłeś właśnie w hotelu?"),
     ]),

# =====================================================================
# raa-khaa … thao-rai — pytanie o cene
# =====================================================================
dict(key="RAAKHAA", ty="question", cat="Zakupy i pieniądze", sub="Ceny", reg="f",
     ph="raa-khaa {ph} thâo-rài khráp", th="ราคา{th}เท่าไหร่ครับ",
     lit="raa-khaa = cena",
     note="Bardziej formalne niż samo „… thâo-rài”. Dobrze brzmi w sklepie z metkami.",
     ex_ph="raa-khaa {ph} lót dâai mǎi khráp", ex_th="ราคา{th}ลดได้ไหมครับ",
     items=[
       ("Jaka jest cena tej koszulki?", "koszulka", "Czy cena koszulki podlega negocjacji?"),
       ("Jaka jest cena tych spodni?", "spodnie", "Czy cena spodni podlega negocjacji?"),
       ("Jaka jest cena tych butów?", "buty", "Czy cena butów podlega negocjacji?"),
       ("Jaka jest cena tego kapelusza?", "kapelusz", "Czy cena kapelusza podlega negocjacji?"),
       ("Jaka jest cena tej torby?", "torba", "Czy cena torby podlega negocjacji?"),
       ("Jaka jest cena tej pamiątki?", "pamiątka", "Czy cena pamiątki podlega negocjacji?"),
       ("Jaka jest cena tej mapy?", "mapa", "Czy cena mapy podlega negocjacji?"),
       ("Jaka jest cena tej ładowarki?", "ładowarka", "Czy cena ładowarki podlega negocjacji?"),
       ("Jaka jest cena karty SIM?", "karta SIM", "Czy cena karty podlega negocjacji?"),
       ("Jaka jest cena tego kasku?", "kask", "Czy cena kasku podlega negocjacji?"),
       ("Jaka jest cena tego roweru?", "rower", "Czy cena roweru podlega negocjacji?"),
       ("Jaka jest cena kremu z filtrem?", "krem z filtrem", "Czy cena kremu podlega negocjacji?"),
       ("Jaka jest cena okularów przeciwsłonecznych.", "okulary przeciwsłoneczne", "Czy cena okularów podlega negocjacji?"),
       ("Jaka jest cena tego leku?", "lek", "Czy cena leku podlega negocjacji?"),
       ("Jaka jest cena tego pokoju?", "pokój", "Czy cena pokoju podlega negocjacji?"),
       ("Jaka jest cena tego biletu?", "bilet", "Czy cena biletu podlega negocjacji?"),
       ("Jaka jest cena tego motocykla?", "motocykl", "Czy cena motocykla podlega negocjacji?"),
       ("Jaka jest cena tego telefonu?", "telefon", "Czy cena telefonu podlega negocjacji?"),
     ]),

# =====================================================================
# … kawn — „najpierw"
# =====================================================================
dict(key="KAWN", ty="phrase", cat="Gramatyka użytkowa", sub="Kolejność", reg="n",
     ph="{ph} kàwn khráp", th="{th}ก่อนครับ",
     lit="kàwn = najpierw, przed innymi rzeczami",
     note="„kàwn” na końcu zdania porządkuje kolejność. Na początku znaczy „zanim”.",
     ex_ph="{ph} kàwn dii mǎi khráp", ex_th="{th}ก่อนดีไหมครับ",
     items=[
       ("Najpierw zjem.", "jeść", "Może najpierw zjemy?"),
       ("Najpierw się napiję.", "pić", "Może najpierw się napijemy?"),
       ("Najpierw zapłacę.", "płacić", "Może najpierw zapłacimy?"),
       ("Najpierw zadzwonię.", "dzwonić", "Może najpierw zadzwonimy?"),
       ("Najpierw zapytam.", "pytać", "Może najpierw zapytamy?"),
       ("Najpierw poczekam.", "czekać", "Może najpierw poczekamy?"),
       ("Najpierw odpocznę.", "odpoczywać", "Może najpierw odpoczniemy?"),
       ("Najpierw poszukam.", "szukać", "Może najpierw poszukamy?"),
       ("Najpierw wybiorę.", "wybierać", "Może najpierw wybierzemy?"),
       ("Najpierw się spakuję.", "pakować się", "Może najpierw się spakujemy?"),
       ("Najpierw obejrzę.", "oglądać", "Może najpierw obejrzymy?"),
       ("Najpierw przeczytam.", "czytać", "Może najpierw przeczytamy?"),
       ("Najpierw się umyję.", "myć", "Może najpierw się umyjemy?"),
       ("Najpierw zarezerwuję.", "rezerwować", "Może najpierw zarezerwujemy?"),
       ("Najpierw zamówię.", "zamawiać", "Może najpierw zamówimy?"),
       ("Najpierw pójdę pieszo.", "iść pieszo", "Może najpierw pójdziemy pieszo?"),
     ]),

# =====================================================================
# khoei kin — „jadlem juz kiedys"
# =====================================================================
dict(key="KHOEIKIN", ty="sentence", cat="Jedzenie i napoje", sub="Doświadczenia", reg="n",
     ph="phǒm khoei kin {ph} khráp", th="ผมเคยกิน{th}ครับ",
     lit="khoei kin = miałem już okazję to jeść",
     note="Bardzo częste pytanie w rozmowie o kuchni tajskiej: „khoei kin … mǎi khráp”.",
     ex_ph="khoei kin {ph} mǎi khráp", ex_th="เคยกิน{th}ไหมครับ",
     items=[
       ("Jadłem już kiedyś pad thai.", "pad thai", "Jadłeś kiedyś pad thai?"),
       ("Jadłem już kiedyś zielone curry.", "zielone curry", "Jadłeś kiedyś zielone curry?"),
       ("Jadłem już kiedyś tom yam.", "zupa tom yam z krewetkami", "Jadłeś kiedyś tom yam?"),
       ("Jadłem już kiedyś som tam.", "sałatka z zielonej papai", "Jadłeś kiedyś som tam?"),
       ("Jadłem już kiedyś ryż kleisty z mango.", "ryż kleisty z mango", "Jadłeś kiedyś ryż z mango?"),
       ("Jadłem już kiedyś kalmary.", "kalmary", "Jadłeś kiedyś kalmary?"),
       ("Jadłem już kiedyś kraba.", "krab", "Jadłeś kiedyś kraba?"),
       ("Jadłem już kiedyś papaję.", "papaja", "Jadłeś kiedyś papaję?"),
       ("Jadłem już kiedyś durian.", "owoce", "Jadłeś kiedyś takie owoce?"),
       ("Piłem już kiedyś wodę kokosową.", "woda kokosowa", "Piłeś kiedyś wodę kokosową?"),
       ("Piłem już kiedyś kawę mrożoną.", "kawa mrożona", "Piłeś kiedyś kawę mrożoną?"),
       ("Piłem już kiedyś herbatę mrożoną.", "herbata mrożona", "Piłeś kiedyś herbatę mrożoną?"),
       ("Jadłem już kiedyś ryż smażony.", "ryż smażony", "Jadłeś kiedyś ryż smażony?"),
       ("Jadłem już kiedyś makaron w rosole.", "makaron ryżowy w rosole", "Jadłeś kiedyś ten makaron?"),
       ("Jadłem już kiedyś sałatkę tajską.", "sałatka", "Jadłeś kiedyś tajską sałatkę?"),
     ]),

# =====================================================================
# ao … pai duai — „wezme ze soba"
# =====================================================================
dict(key="AOPAIDUAI", ty="sentence", cat="Gramatyka użytkowa", sub="Plany", reg="n",
     ph="phǒm jà ao {ph} pai dûai khráp", th="ผมจะเอา{th}ไปด้วยครับ",
     lit="ao … pai dûai = zabiorę to ze sobą",
     note="„pai dûai” znaczy „razem ze mną, w tamtą stronę”. Odwrotnie: „maa dûai”.",
     ex_ph="ao {ph} pai dûai mǎi khráp", ex_th="เอา{th}ไปด้วยไหมครับ",
     items=[
       ("Wezmę ze sobą parasol.", "parasol", "Weźmiesz parasol?"),
       ("Wezmę ze sobą kapelusz.", "kapelusz", "Weźmiesz kapelusz?"),
       ("Wezmę ze sobą krem z filtrem.", "krem z filtrem", "Weźmiesz krem z filtrem?"),
       ("Wezmę ze sobą ładowarkę.", "ładowarka", "Weźmiesz ładowarkę?"),
       ("Wezmę ze sobą mapę.", "mapa", "Weźmiesz mapę?"),
       ("Wezmę ze sobą paszport.", "paszport", "Weźmiesz paszport?"),
       ("Wezmę ze sobą lekarstwo.", "lek", "Weźmiesz lekarstwo?"),
       ("Wezmę ze sobą torbę na zakupy.", "torba na zakupy", "Weźmiesz torbę na zakupy?"),
       ("Wezmę ze sobą okulary przeciwsłoneczne.", "okulary przeciwsłoneczne", "Weźmiesz okulary?"),
       ("Wezmę ze sobą kask.", "kask", "Weźmiesz kask?"),
       ("Wezmę ze sobą ręcznik.", "ręcznik", "Weźmiesz ręcznik?"),
       ("Wezmę ze sobą wodę butelkowaną.", "woda butelkowana", "Weźmiesz wodę?"),
       ("Wezmę ze sobą plaster.", "plaster", "Weźmiesz plaster?"),
       ("Wezmę ze sobą prawo jazdy.", "prawo jazdy", "Weźmiesz prawo jazdy?"),
     ]),

# =====================================================================
# mii … yoe — „jest duzo"
# =====================================================================
dict(key="MIIYOE", ty="sentence", cat="Liczby i liczenie", sub="Ilość", reg="p",
     ph="mii {ph} yóe khráp", th="มี{th}เยอะครับ",
     lit="yóe = dużo (potocznie)",
     note="„yóe” jest swobodniejsze niż „mâak”. W piśmie urzędowym lepiej „mâak”.",
     ex_ph="mii {ph} yóe mǎi khráp", ex_th="มี{th}เยอะไหมครับ",
     items=[
       ("Jest dużo ludzi.", "człowiek / osoba", "Czy jest dużo ludzi?"),
       ("Jest dużo turystów.", "obcokrajowiec", "Czy jest dużo obcokrajowców?"),
       ("Jest dużo jedzenia.", "jedzenie", "Czy jest dużo jedzenia?"),
       ("Jest dużo owoców.", "owoce", "Czy jest dużo owoców?"),
       ("Jest dużo warzyw.", "warzywa", "Czy jest dużo warzyw?"),
       ("Jest dużo pamiątek.", "pamiątka", "Czy jest dużo pamiątek?"),
       ("Jest dużo sklepów.", "sklep całodobowy", "Czy jest dużo sklepów?"),
       ("Jest dużo taksówek.", "taksówka", "Czy jest dużo taksówek?"),
       ("Jest dużo motocykli.", "motocykl", "Czy jest dużo motocykli?"),
       ("Jest dużo komarów.", "ukąszenie owada", "Czy jest dużo owadów?"),
       ("Jest dużo pracy.", "praca", "Czy jest dużo pracy?"),
       ("Jest dużo pokoi.", "pokój", "Czy jest dużo pokoi?"),
       ("Jest dużo świątyń.", "świątynia", "Czy jest dużo świątyń?"),
       ("Jest dużo wysp.", "wyspa", "Czy jest dużo wysp?"),
     ]),

# =====================================================================
# chuai … hai noi dai mai — prosba pytajaca o przysluge
# =====================================================================
dict(key="CHUAIDAIMAI", ty="question", cat="Awarie i pomoc", sub="Prośby", reg="f",
     ph="chûai {ph} hâi nòi dâai mǎi khráp", th="ช่วย{th}ให้หน่อยได้ไหมครับ",
     lit="chûai … hâi nòi dâai mǎi = czy mógłbyś to dla mnie zrobić",
     note="Najuprzejmiejsza wersja prośby: pytanie zamiast polecenia.",
     ex_ph="chûai {ph} hâi dûai ná khráp", ex_th="ช่วย{th}ให้ด้วยนะครับ",
     items=[
       ("Czy mógłbyś mi to napisać?", "pisać", "Napisz mi to, proszę."),
       ("Czy mógłbyś mi to przeczytać?", "czytać", "Przeczytaj mi to, proszę."),
       ("Czy mógłbyś to naprawić?", "naprawiać", "Napraw to, proszę."),
       ("Czy mógłbyś to sprawdzić i policzyć?", "policzyć rachunek", "Policz to, proszę."),
       ("Czy mógłbyś mi to kupić?", "kupować", "Kup mi to, proszę."),
       ("Czy mógłbyś zadzwonić?", "dzwonić", "Zadzwoń, proszę."),
       ("Czy mógłbyś mi to zamówić?", "zamawiać", "Zamów mi to, proszę."),
       ("Czy mógłbyś mi to zarezerwować?", "rezerwować", "Zarezerwuj mi to, proszę."),
       ("Czy mógłbyś to otworzyć?", "otwierać", "Otwórz to, proszę."),
       ("Czy mógłbyś to zamknąć?", "zamykać", "Zamknij to, proszę."),
       ("Czy mógłbyś mi to pokazać?", "pokazać", "Pokaż mi to, proszę."),
       ("Czy mógłbyś tego poszukać?", "szukać", "Poszukaj tego, proszę."),
       ("Czy mógłbyś to wysłać?", "wysyłać", "Wyślij to, proszę."),
       ("Czy mógłbyś to wyprać?", "prać", "Wypierz to, proszę."),
       ("Czy mógłbyś to zmienić?", "zmieniać", "Zmień to, proszę."),
       ("Czy mógłbyś to anulować?", "anulować", "Anuluj to, proszę."),
     ]),

# =====================================================================
# … long — „coraz mniej"
# =====================================================================
dict(key="LONGDOWN", ty="collocation", cat="Gramatyka użytkowa", sub="Zmiana", reg="n",
     ph="{ph} long", th="{th}ลง",
     lit="… long = spadek cechy, „coraz mniej”",
     note="Przeciwieństwo „khûen”. Uwaga: „long” samo w sobie znaczy też „schodzić, wysiadać”.",
     ex_ph="chûang níi {ph} long khráp", ex_th="ช่วงนี้{th}ลงครับ",
     items=[
       ("robi się coraz taniej", "tani", "Ostatnio taniej."),
       ("robi się coraz mniej gorąco", "gorący", "Ostatnio mniej gorąco."),
       ("robi się coraz ciszej", "głośny", "Ostatnio ciszej."),
       ("robi się coraz wolniej", "szybki", "Ostatnio wolniej."),
       ("robi się coraz ciemniej", "jasny", "Ostatnio ciemniej."),
       ("robi się coraz mniej zatłoczone", "pełny / zajęty", "Ostatnio mniej tłoczno."),
       ("jestem coraz mniej zmęczony", "zmęczony", "Ostatnio mniej zmęczony."),
       ("jestem coraz mniej zdenerwowany", "zdenerwowany", "Ostatnio mniej zdenerwowany."),
       ("jestem coraz mniej zestresowany", "zestresowany", "Ostatnio mniej zestresowany."),
       ("robi się coraz mniej ostro", "ostry (pikantny)", "Ostatnio mniej ostro."),
       ("robi się coraz mniej trudno", "trudny", "Ostatnio mniej trudno."),
       ("robi się coraz mniej brudno", "brudny", "Ostatnio mniej brudno."),
     ]),
]
