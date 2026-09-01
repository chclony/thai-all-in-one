# -*- coding: utf-8 -*-
"""Wzorce zdaniowe etapu 6 — czwarta seria.

Konstrukcje sprawdzone jako nieuzyte w etapach 1-5: „… wan ùen”, „… hâi rew
nòi”, „hâam …”, „… khǎwng khrai”, „tâwng jàai khâa …”, „… sǎm-ràp dèk”,
„raa-khaa … thâo rài”, „thúk khon tâwng …”.

Pozycja: (polskie haslo rekordu, polskie haslo bazowe, polski przyklad)
"""

TPL_D = [

# =====================================================================
# … wan uen daai mai khrap — przeniesienie na inny dzien
# =====================================================================
dict(key="WANUEN", ty="question", cat="Czas i daty", sub="Terminy", reg="n",
     ph="{ph} wan ùen dâai mǎi khráp", th="{th}วันอื่นได้ไหมครับ",
     lit="wan ùen = inny dzień",
     note="Prośba o zmianę terminu bez podawania powodu. W Tajlandii powód nie jest wymagany — liczy się uprzedzenie z wyprzedzeniem.",
     ex_ph="khǎw-thôot khráp {ph} wan ùen dâai mǎi khráp", ex_th="ขอโทษครับ {th}วันอื่นได้ไหมครับ",
     items=[
       ("Czy można przyjść innego dnia?", "przyjść / przyjechać", "Przepraszam, czy można przyjść innego dnia?"),
       ("Czy można się spotkać innego dnia?", "spotykać", "Przepraszam, czy można się spotkać innego dnia?"),
       ("Czy można zapłacić innego dnia?", "płacić", "Przepraszam, czy można zapłacić innego dnia?"),
       ("Czy można odebrać innego dnia?", "odbierać", "Przepraszam, czy można odebrać innego dnia?"),
       ("Czy można zarezerwować na inny dzień?", "rezerwować", "Przepraszam, czy można zarezerwować na inny dzień?"),
       ("Czy można wynająć innego dnia?", "wynajmować", "Przepraszam, czy można wynająć innego dnia?"),
       ("Czy można pracować innego dnia?", "pracować", "Przepraszam, czy można pracować innego dnia?"),
       ("Czy można zwiedzać innego dnia?", "zwiedzać", "Przepraszam, czy można zwiedzać innego dnia?"),
       ("Czy można wysłać innego dnia?", "wysyłać", "Przepraszam, czy można wysłać innego dnia?"),
       ("Czy można podpisać innego dnia?", "podpisać", "Przepraszam, czy można podpisać innego dnia?"),
       ("Czy można zacząć innego dnia?", "zaczynać", "Przepraszam, czy można zacząć innego dnia?"),
       ("Czy można wracać innego dnia?", "wracać", "Przepraszam, czy można wracać innego dnia?"),
     ]),

# =====================================================================
# chuai … hai rew noi daai mai khrap — prosba o przyspieszenie
# =====================================================================
dict(key="HAIREWNOI", ty="question", cat="Podstawy i grzeczność", sub="Prośby", reg="n",
     ph="chûai {ph} hâi rew nòi dâai mǎi khráp", th="ช่วย{th}ให้เร็วหน่อยได้ไหมครับ",
     lit="hâi rew nòi = trochę szybciej",
     note="„nòi” łagodzi prośbę o pośpiech. Bez niego zabrzmi jak ponaglanie, co w tajskiej obsłudze odbiera się źle.",
     ex_ph="khǎw-thôot khráp phǒm rîip chûai {ph} hâi rew nòi dâai mǎi", ex_th="ขอโทษครับ ผมรีบ ช่วย{th}ให้เร็วหน่อยได้ไหม",
     items=[
       ("Czy można szybciej to przygotować?", "robić", "Przepraszam, śpieszę się — czy można szybciej?"),
       ("Czy można szybciej podać?", "dawać", "Przepraszam, śpieszę się — czy można szybciej?"),
       ("Czy można szybciej to naprawić?", "naprawiać", "Przepraszam, śpieszę się — czy można szybciej?"),
       ("Czy można szybciej wysłać?", "wysyłać", "Przepraszam, śpieszę się — czy można szybciej?"),
       ("Czy można szybciej to sprawdzić?", "szukać", "Przepraszam, śpieszę się — czy można szybciej?"),
       ("Czy można szybciej ugotować?", "gotować", "Przepraszam, śpieszę się — czy można szybciej?"),
       ("Czy można szybciej odpowiedzieć?", "odpowiadać", "Przepraszam, śpieszę się — czy można szybciej?"),
       ("Czy można szybciej zarezerwować?", "rezerwować", "Przepraszam, śpieszę się — czy można szybciej?"),
       ("Czy można szybciej to zmienić?", "zmieniać", "Przepraszam, śpieszę się — czy można szybciej?"),
       ("Czy można szybciej jechać?", "iść / jechać", "Przepraszam, śpieszę się — czy można szybciej?"),
       ("Czy można szybciej otworzyć?", "otwierać", "Przepraszam, śpieszę się — czy można szybciej?"),
       ("Czy można szybciej to policzyć?", "płacić", "Przepraszam, śpieszę się — czy można szybciej?"),
     ]),

# =====================================================================
# thii nii haam … mai khrap — zakazy
# =====================================================================
dict(key="HAAM", ty="question", cat="Pytania", sub="Zasady", reg="n",
     ph="thîi nîi hâam {ph} mǎi khráp", th="ที่นี่ห้าม{th}ไหมครับ",
     lit="hâam … = zakazane jest …",
     note="„hâam” widnieje na wszystkich tabliczkach zakazu. Pytanie zadane wprost oszczędza kłopotów w świątyniach i parkach narodowych.",
     ex_ph="khǎw-thôot khráp thîi nîi hâam {ph} mǎi khráp", ex_th="ขอโทษครับ ที่นี่ห้าม{th}ไหมครับ",
     items=[
       ("Czy tu nie wolno robić zdjęć?", "robić zdjęcia", "Przepraszam, czy tu nie wolno robić zdjęć?"),
       ("Czy tu nie wolno palić?", "palić papierosy", "Przepraszam, czy tu nie wolno palić?"),
       ("Czy tu nie wolno jeść?", "jeść", "Przepraszam, czy tu nie wolno jeść?"),
       ("Czy tu nie wolno pić?", "pić", "Przepraszam, czy tu nie wolno pić?"),
       ("Czy tu nie wolno pływać?", "pływać", "Przepraszam, czy tu nie wolno pływać?"),
       ("Czy tu nie wolno wchodzić?", "wchodzić", "Przepraszam, czy tu nie wolno wchodzić?"),
       ("Czy tu nie wolno siedzieć?", "siedzieć", "Przepraszam, czy tu nie wolno siedzieć?"),
       ("Czy tu nie wolno spać?", "spać", "Przepraszam, czy tu nie wolno spać?"),
       ("Czy tu nie wolno biegać?", "biegać", "Przepraszam, czy tu nie wolno biegać?"),
       ("Czy tu nie wolno śpiewać?", "śpiewać", "Przepraszam, czy tu nie wolno śpiewać?"),
       ("Czy tu nie wolno się zatrzymywać?", "zatrzymać się", "Przepraszam, czy tu nie wolno się zatrzymywać?"),
       ("Czy tu nie wolno sprzedawać?", "sprzedawać", "Przepraszam, czy tu nie wolno sprzedawać?"),
     ]),

# =====================================================================
# … an nii khawng khrai khrap — wlasnosc
# =====================================================================
dict(key="KHAWNGKHRAI", ty="question", cat="Pytania", sub="Własność", reg="n",
     ph="{ph} níi khǎwng khrai khráp", th="{th}นี้ของใครครับ", lit="khǎwng khrai = czyje",
     note="„khǎwng” tworzy dopełniacz: „khǎwng phǒm” = mój. Pytanie przydaje się w hostelu i w biurze.",
     ex_ph="{ph} níi khǎwng khrai khráp mii khon luem wái", ex_th="{th}นี้ของใครครับ มีคนลืมไว้",
     items=[
       ("Czyj to portfel?", "portfel", "Czyj to portfel? Ktoś go tu zostawił."),
       ("Czyj to plecak?", "plecak", "Czyj to plecak? Ktoś go tu zostawił."),
       ("Czyja to walizka?", "walizka", "Czyja to walizka? Ktoś ją tu zostawił."),
       ("Czyj to klucz?", "klucz", "Czyj to klucz? Ktoś go tu zostawił."),
       ("Czyj to telefon?", "telefon", "Czyj to telefon? Ktoś go tu zostawił."),
       ("Czyja to ładowarka?", "ładowarka", "Czyja to ładowarka? Ktoś ją tu zostawił."),
       ("Czyje to okulary?", "okulary przeciwsłoneczne", "Czyje to okulary? Ktoś je tu zostawił."),
       ("Czyj to kapelusz?", "kapelusz", "Czyj to kapelusz? Ktoś go tu zostawił."),
       ("Czyj to bilet?", "bilet", "Czyj to bilet? Ktoś go tu zostawił."),
       ("Czyj to paszport?", "paszport", "Czyj to paszport? Ktoś go tu zostawił."),
       ("Czyj to rower?", "rower", "Czyj to rower? Ktoś go tu zostawił."),
       ("Czyja to torba?", "torba", "Czyja to torba? Ktoś ją tu zostawił."),
       ("Czyj to kask?", "kask", "Czyj to kask? Ktoś go tu zostawił."),
       ("Czyj to dokument?", "dokument", "Czyj to dokument? Ktoś go tu zostawił."),
       ("Czyja to koszula?", "koszula", "Czyja to koszula? Ktoś ją tu zostawił."),
       ("Czyje to skarpetki?", "skarpetki", "Czyje to skarpetki? Ktoś je tu zostawił."),
       ("Czyja to wizytówka?", "wizytówka", "Czyja to wizytówka? Ktoś ją tu zostawił."),
       ("Czyja to kurtka?", "kurtka", "Czyja to kurtka? Ktoś ją tu zostawił."),
       ("Czyj to czajnik?", "czajnik", "Czyj to czajnik? Ktoś go tu zostawił."),
       ("Czyja to karta kredytowa?", "karta kredytowa", "Czyja to karta? Ktoś ją tu zostawił."),
     ]),

# =====================================================================
# tawng jaai khaa … duai mai khrap — oplaty dodatkowe
# =====================================================================
dict(key="JAAIKHAA", ty="question", cat="Zakupy i pieniądze", sub="Opłaty", reg="n",
     ph="tâwng jàai khâa {ph} dûai mǎi khráp", th="ต้องจ่ายค่า{th}ด้วยไหมครับ",
     lit="khâa … = opłata za …",
     note="Przedrostek „khâa” tworzy nazwy wszystkich opłat: „khâa hâwng”, „khâa fai”, „khâa rót”. Pytanie warto zadać przed, a nie po.",
     ex_ph="tâwng jàai khâa {ph} dûai mǎi khráp rǔe ruam yùu láew", ex_th="ต้องจ่ายค่า{th}ด้วยไหมครับ หรือรวมอยู่แล้ว",
     items=[
       ("Czy trzeba płacić za pokój osobno?", "pokój", "Czy trzeba płacić za pokój osobno, czy to wliczone?"),
       ("Czy trzeba płacić za śniadanie?", "śniadanie", "Czy trzeba płacić za śniadanie, czy to wliczone?"),
       ("Czy trzeba płacić za wodę?", "woda", "Czy trzeba płacić za wodę, czy to wliczone?"),
       ("Czy trzeba płacić za internet?", "internet", "Czy trzeba płacić za internet, czy to wliczone?"),
       ("Czy trzeba płacić za basen?", "basen", "Czy trzeba płacić za basen, czy to wliczone?"),
       ("Czy trzeba płacić za siłownię?", "siłownia", "Czy trzeba płacić za siłownię, czy to wliczone?"),
       ("Czy trzeba płacić za sejf?", "sejf", "Czy trzeba płacić za sejf, czy to wliczone?"),
       ("Czy trzeba płacić za ręcznik?", "ręcznik", "Czy trzeba płacić za ręcznik, czy to wliczone?"),
       ("Czy trzeba płacić za przechowalnię bagażu?", "przechowalnia bagażu", "Czy trzeba płacić za przechowalnię, czy to wliczone?"),
       ("Czy trzeba płacić za benzynę osobno?", "benzyna", "Czy trzeba płacić za benzynę osobno, czy to wliczone?"),
       ("Czy trzeba płacić za kask?", "kask", "Czy trzeba płacić za kask, czy to wliczone?"),
       ("Czy trzeba płacić za ubezpieczenie?", "ubezpieczenie", "Czy trzeba płacić za ubezpieczenie, czy to wliczone?"),
       ("Czy trzeba płacić za wycieczkę?", "wycieczka", "Czy trzeba płacić za wycieczkę, czy to wliczone?"),
       ("Czy trzeba płacić za przewodnika?", "przewodnik (osoba)", "Czy trzeba płacić za przewodnika, czy to wliczone?"),
       ("Czy trzeba płacić za wejście?", "wejście", "Czy trzeba płacić za wejście, czy to wliczone?"),
       ("Czy trzeba płacić za klimatyzację?", "klimatyzacja", "Czy trzeba płacić za klimatyzację, czy to wliczone?"),
       ("Czy trzeba płacić za pranie?", "pralnia", "Czy trzeba płacić za pralnię, czy to wliczone?"),
       ("Czy trzeba płacić za dokładkę?", "dokładka", "Czy trzeba płacić za dokładkę, czy to wliczone?"),
       ("Czy trzeba płacić za balkon?", "balkon", "Czy trzeba płacić za balkon, czy to wliczone?"),
       ("Czy trzeba płacić za widok?", "widok", "Czy trzeba płacić za widok, czy to wliczone?"),
       ("Czy trzeba płacić za napiwek?", "napiwek", "Czy trzeba doliczyć napiwek, czy to wliczone?"),
       ("Czy trzeba płacić za toaletę?", "toaleta", "Czy trzeba płacić za toaletę, czy to wliczone?"),
       ("Czy trzeba płacić za bagaż?", "walizka", "Czy trzeba płacić za walizkę, czy to wliczone?"),
       ("Czy trzeba płacić za lodówkę w pokoju?", "lodówka w pokoju", "Czy trzeba płacić za lodówkę, czy to wliczone?"),
     ]),

# =====================================================================
# mii … sam-rap dek mai khrap — wersja dla dzieci
# =====================================================================
dict(key="SAMRAPDEK", ty="question", cat="Pytania", sub="Rodzina", reg="n",
     ph="mii {ph} sǎm-ràp dèk mǎi khráp", th="มี{th}สำหรับเด็กไหมครับ",
     lit="sǎm-ràp dèk = dla dziecka",
     note="„sǎm-ràp” to „przeznaczony dla”. Konstrukcja działa też z „sǎm-ràp phûu yài” i „sǎm-ràp khon tàang châat”.",
     ex_ph="mii {ph} sǎm-ràp dèk mǎi khráp lûuk phǒm aa-yú hâa khùap", ex_th="มี{th}สำหรับเด็กไหมครับ ลูกผมอายุห้าขวบ",
     items=[
       ("Czy jest menu dla dzieci?", "menu", "Czy jest menu dla dzieci? Moje ma pięć lat."),
       ("Czy jest bilet dla dzieci?", "bilet", "Czy jest bilet dla dzieci? Moje ma pięć lat."),
       ("Czy jest krzesełko dla dzieci?", "krzesło", "Czy jest krzesełko dla dzieci? Moje ma pięć lat."),
       ("Czy jest łóżko dla dziecka?", "łóżko", "Czy jest łóżko dla dziecka? Moje ma pięć lat."),
       ("Czy jest basen dla dzieci?", "basen", "Czy jest basen dla dzieci? Moje ma pięć lat."),
       ("Czy jest zniżka dla dzieci?", "zniżka", "Czy jest zniżka dla dzieci? Moje ma pięć lat."),
       ("Czy jest porcja dla dzieci?", "porcja", "Czy jest porcja dla dzieci? Moje ma pięć lat."),
       ("Czy jest lek dla dzieci?", "lek", "Czy jest lek dla dzieci? Moje ma pięć lat."),
       ("Czy jest kask dla dzieci?", "kask", "Czy jest kask dla dzieci? Moje ma pięć lat."),
       ("Czy jest wycieczka dla dzieci?", "wycieczka", "Czy jest wycieczka dla dzieci? Moje ma pięć lat."),
       ("Czy jest rower dla dzieci?", "rower", "Czy jest rower dla dzieci? Moje ma pięć lat."),
       ("Czy jest pokój dla rodziny z dzieckiem?", "pokój", "Czy jest pokój dla dzieci? Moje ma pięć lat."),
     ]),

# =====================================================================
# … raa-khaa thao rai khrap — cena konkretnej rzeczy
# =====================================================================
dict(key="RAAKHAATHAORAI", ty="question", cat="Zakupy i pieniądze", sub="Cena", reg="n",
     ph="{ph} raa-khaa thâo rài khráp", th="{th}ราคาเท่าไหร่ครับ",
     lit="raa-khaa thâo rài = jaka cena",
     note="Pełniejsze niż samo „thâo rài khráp” — wskazujesz konkretny przedmiot, więc sprzedawca nie pomyli się co do pytania.",
     ex_ph="{ph} raa-khaa thâo rài khráp lót dâai mǎi", ex_th="{th}ราคาเท่าไหร่ครับ ลดได้ไหม",
     items=[
       ("Ile kosztuje ten plecak?", "plecak", "Ile kosztuje ten plecak? Da się taniej?"),
       ("Ile kosztuje ta koszulka?", "koszulka", "Ile kosztuje ta koszulka? Da się taniej?"),
       ("Ile kosztują te sandały?", "sandały", "Ile kosztują te sandały? Da się taniej?"),
       ("Ile kosztuje ten kapelusz?", "kapelusz", "Ile kosztuje ten kapelusz? Da się taniej?"),
       ("Ile kosztuje ta pamiątka?", "pamiątka", "Ile kosztuje ta pamiątka? Da się taniej?"),
       ("Ile kosztuje ta sukienka?", "sukienka", "Ile kosztuje ta sukienka? Da się taniej?"),
       ("Ile kosztują te spodnie?", "spodnie", "Ile kosztują te spodnie? Da się taniej?"),
       ("Ile kosztują te buty?", "buty", "Ile kosztują te buty? Da się taniej?"),
       ("Ile kosztuje ta kurtka?", "kurtka", "Ile kosztuje ta kurtka? Da się taniej?"),
       ("Ile kosztuje ta torba?", "torba", "Ile kosztuje ta torba? Da się taniej?"),
       ("Ile kosztuje ten pasek?", "pasek", "Ile kosztuje ten pasek? Da się taniej?"),
       ("Ile kosztuje ten krem z filtrem?", "krem z filtrem", "Ile kosztuje ten krem? Da się taniej?"),
       ("Ile kosztuje ta karta SIM?", "karta SIM", "Ile kosztuje ta karta SIM? Da się taniej?"),
       ("Ile kosztuje ten powerbank?", "powerbank", "Ile kosztuje ten powerbank? Da się taniej?"),
       ("Ile kosztuje ta ładowarka?", "ładowarka", "Ile kosztuje ta ładowarka? Da się taniej?"),
       ("Ile kosztuje ten prom?", "prom", "Ile kosztuje ten prom? Da się taniej?"),
       ("Ile kosztuje ten tuk-tuk?", "tuk-tuk", "Ile kosztuje ten tuk-tuk? Da się taniej?"),
       ("Ile kosztuje ten masaż?", "salon masażu", "Ile kosztuje ten masaż? Da się taniej?"),
       ("Ile kosztuje ta koszula?", "koszula", "Ile kosztuje ta koszula? Da się taniej?"),
       ("Ile kosztują te krótkie spodenki?", "krótkie spodenki", "Ile kosztują te spodenki? Da się taniej?"),
       ("Ile kosztują te skarpetki?", "skarpetki", "Ile kosztują te skarpetki? Da się taniej?"),
       ("Ile kosztuje ta łódź?", "łódź", "Ile kosztuje ta łódź? Da się taniej?"),
       ("Ile kosztuje ten minibus?", "minibus", "Ile kosztuje ten minibus? Da się taniej?"),
       ("Ile kosztuje ta przejściówka?", "przejściówka", "Ile kosztuje ta przejściówka? Da się taniej?"),
       ("Ile kosztuje ten router?", "router", "Ile kosztuje ten router? Da się taniej?"),
       ("Ile kosztuje ta mapa?", "mapa", "Ile kosztuje ta mapa? Da się taniej?"),
     ]),

# =====================================================================
# thuk khon tawng … mai khrap — obowiazek powszechny
# =====================================================================
dict(key="THUKKHON", ty="question", cat="Pytania", sub="Zasady", reg="n",
     ph="thúk khon tâwng {ph} mǎi khráp", th="ทุกคนต้อง{th}ไหมครับ",
     lit="thúk khon = każdy, wszyscy",
     note="Pytanie o regułę powszechną, nie o wyjątek dla ciebie. Bezpieczniejsze niż „phǒm tâwng … mǎi”, bo nie brzmi jak próba wymigania się.",
     ex_ph="thúk khon tâwng {ph} mǎi khráp rǔe wâa baang khon kâw phaw", ex_th="ทุกคนต้อง{th}ไหมครับ หรือว่าบางคนก็พอ",
     items=[
       ("Czy wszyscy muszą się rejestrować?", "podpisać", "Czy wszyscy muszą podpisać, czy tylko niektórzy?"),
       ("Czy wszyscy muszą płacić?", "płacić", "Czy wszyscy muszą płacić, czy tylko niektórzy?"),
       ("Czy wszyscy muszą czekać?", "czekać", "Czy wszyscy muszą czekać, czy tylko niektórzy?"),
       ("Czy wszyscy muszą rezerwować?", "rezerwować", "Czy wszyscy muszą rezerwować, czy tylko niektórzy?"),
       ("Czy wszyscy muszą wysiadać?", "wysiadać", "Czy wszyscy muszą wysiadać, czy tylko niektórzy?"),
       ("Czy wszyscy muszą się przesiadać?", "przesiadać się", "Czy wszyscy muszą się przesiadać, czy tylko niektórzy?"),
       ("Czy wszyscy muszą pokazać dokument?", "pokazać", "Czy wszyscy muszą pokazać, czy tylko niektórzy?"),
       ("Czy wszyscy muszą wypełnić formularz?", "wypełnić formularz", "Czy wszyscy muszą wypełnić formularz, czy tylko niektórzy?"),
       ("Czy wszyscy muszą wracać?", "wracać", "Czy wszyscy muszą wracać, czy tylko niektórzy?"),
       ("Czy wszyscy muszą wejść?", "wchodzić", "Czy wszyscy muszą wejść, czy tylko niektórzy?"),
     ]),
]
