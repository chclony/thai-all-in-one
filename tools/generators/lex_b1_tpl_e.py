# -*- coding: utf-8 -*-
"""Wzorce zdaniowe etapu 4 (B1) — czesc E: rzeczowniki, jedzenie, miejsca, pobyt.

Konstrukcje: zaslyszana opinia, prosba o rekomendacje, ciekawosc, niecheс,
przypadkowe odkrycie, cel wizyty, staly ekwipunek, brak doswiadczenia,
plotka, postanowienie, rezerwacja z wyprzedzeniem, prosba o szczegoly,
zaskoczenie, alergia, zamiana.

Pozycja: (polskie haslo rekordu, polskie haslo bazowe, polski przyklad)
"""

JEDZENIE = ["ryż", "kurczak", "wieprzowina", "wołowina", "ryba", "krewetki", "krab",
            "kalmary", "warzywa", "owoce", "mango", "papaja", "ananas", "arbuz",
            "banan", "kokos", "zupa", "sałatka", "pad thai", "ryż smażony",
            "zielone curry", "lody", "jajko", "chleb", "mleko", "sos rybny",
            "papryczka chili", "ryż kleisty", "deser", "przystawka", "danie główne",
            "orzeszki ziemne", "makaron ryżowy w rosole", "sałatka z zielonej papai",
            "zupa tom yam z krewetkami", "ryż kleisty z mango"]

NAPOJE = ["kawa", "herbata", "piwo", "wino", "woda kokosowa", "sok pomarańczowy",
          "herbata mrożona", "kawa mrożona", "woda butelkowana", "woda gazowana"]

MIEJSCA = ["plaża", "park", "świątynia", "wodospad", "wyspa", "morze", "rzeka",
           "góra", "las", "most", "targ", "bazar nocny", "centrum handlowe",
           "supermarket", "kawiarnia", "restauracja", "salon masażu", "poczta",
           "pralnia", "szpital", "apteka", "bank", "kantor", "lotnisko",
           "dworzec kolejowy", "dworzec autobusowy", "przystań / port", "hotel",
           "uliczka boczna", "skrzyżowanie"]

HOTELOWE = ["pokój", "klucz", "ręcznik", "poduszka", "koc", "pościel",
            "klimatyzacja", "wentylator", "basen", "siłownia", "balkon", "sejf",
            "winda", "recepcja", "zameldowanie", "wymeldowanie",
            "śniadanie w hotelu", "sprzątaczka", "przechowalnia bagażu", "widok",
            "gorąca woda", "lodówka w pokoju", "prysznic", "łóżko"]


def _n(nouns, rec_fmt, ex_fmt):
    return [(rec_fmt % n, n, ex_fmt % n) for n in nouns]


TPL_E = [

dict(key="DAIYINMAA", ty="sentence", cat="Small talk", sub="Opinie", reg="n",
     ph="phǒm dâi yin maa wâa {ph} dii khráp", th="ผมได้ยินมาว่า{th}ดีครับ",
     lit="dâi yin maa wâa = słyszałem, że",
     note="„maa” po czasowniku niesie „dotarło do mnie z zewnątrz”. Bez niego zdanie mówiłoby o jednorazowym usłyszeniu.",
     ex_ph="{ph} dii jing mǎi khráp", ex_th="{th}ดีจริงไหมครับ",
     items=_n(JEDZENIE + MIEJSCA,
              "Słyszałem dobre opinie o tym, co dotyczy: %s.",
              "Czy naprawdę jest dobre to, co dotyczy: %s?")),

dict(key="NAENAM", ty="question", cat="Cechy i opinie", sub="Rekomendacje", reg="n",
     ph="náe-nam {ph} mǎi khráp", th="แนะนำ{th}ไหมครับ",
     lit="náe-nam = polecać, doradzać",
     note="Pytanie o rekomendację jest w Tajlandii bardzo naturalne i rzadko odmawia się odpowiedzi.",
     ex_ph="phǒm náe-nam {ph} loei khráp", ex_th="ผมแนะนำ{th}เลยครับ",
     items=_n(JEDZENIE + NAPOJE + MIEJSCA,
              "Poleciłbyś to, co dotyczy: %s?",
              "Zdecydowanie polecam to, co dotyczy: %s.")),

dict(key="YAAKRUUWAA", ty="sentence", cat="Pytania", sub="Ciekawość", reg="n",
     ph="yàak rúu wâa {ph} pen yang-ngai khráp", th="อยากรู้ว่า{th}เป็นยังไงครับ",
     lit="yàak rúu wâa = ciekaw jestem, jak",
     note="„wâa” wprowadza zdanie podrzędne. To jedna z konstrukcji, bez których nie da się mówić dłuższymi zdaniami.",
     ex_ph="{ph} pen yang-ngai bâang khráp", ex_th="{th}เป็นยังไงบ้างครับ",
     items=_n(MIEJSCA + HOTELOWE,
              "Ciekaw jestem, jakie jest to, co dotyczy: %s.",
              "Jakie jest to, co dotyczy: %s?")),

dict(key="MAITHUUKJAI", ty="sentence", cat="Cechy i opinie", sub="Niechęć", reg="n",
     ph="phǒm mâi khâwi thùuk jai {ph} khráp", th="ผมไม่ค่อยถูกใจ{th}ครับ",
     lit="thùuk jai = trafiać w gust",
     note="„thùuk jai” to zgodność z upodobaniem, mocniejsza niż „châwp”. Zaprzeczenie z „mâi khâwi” łagodzi ocenę.",
     ex_ph="{ph} thùuk jai mǎi khráp", ex_th="{th}ถูกใจไหมครับ",
     items=_n(JEDZENIE + HOTELOWE,
              "Nie bardzo przypadło mi do gustu to, co dotyczy: %s.",
              "Przypadło ci do gustu to, co dotyczy: %s?")),

dict(key="BANGOEN", ty="sentence", cat="Miejsca i orientacja", sub="Odkrycia", reg="n",
     ph="phǒm bang-oen jôe {ph} khráp", th="ผมบังเอิญเจอ{th}ครับ",
     lit="bang-oen = przypadkiem, przypadkowo",
     note="„bang-oen” zawsze stoi przed czasownikiem. Po polsku „przypadkiem” może stać wszędzie — po tajsku nie.",
     ex_ph="jôe {ph} thîi nǎi khráp", ex_th="เจอ{th}ที่ไหนครับ",
     items=_n(MIEJSCA + JEDZENIE,
              "Trafiłem przypadkiem na to, co dotyczy: %s.",
              "Gdzie trafiłeś na to, co dotyczy: %s?")),

dict(key="PHUEADOICHAPHAW", ty="sentence", cat="Miejsca i orientacja", sub="Cel", reg="n",
     ph="phǒm pai phûea {ph} doi chà-phǎw khráp", th="ผมไปเพื่อ{th}โดยเฉพาะครับ",
     lit="doi chà-phǎw = specjalnie, wyłącznie w tym celu",
     note="„doi chà-phǎw” podkreśla wyłączność celu. Bez niego zdanie brzmiałoby jak zwykła informacja.",
     ex_ph="pai phûea {ph} loei rǒe khráp", ex_th="ไปเพื่อ{th}เลยหรือครับ",
     items=_n(JEDZENIE + MIEJSCA,
              "Pojechałem tam specjalnie dla tego, co dotyczy: %s.",
              "Pojechałeś tam wyłącznie dla tego, co dotyczy: %s?")),

dict(key="TITTUA", ty="sentence", cat="Gramatyka użytkowa", sub="Zwyczaje", reg="n",
     ph="phǒm ao {ph} tìt tua pai sà-mǒoe khráp", th="ผมเอา{th}ติดตัวไปเสมอครับ",
     lit="tìt tua = przy sobie, na sobie",
     note="„tìt tua” dotyczy rzeczy noszonych stale przy sobie. Rzecz zabrana jednorazowo to „ao … pai dûai”.",
     ex_ph="ao {ph} tìt tua pai dûai mǎi khráp", ex_th="เอา{th}ติดตัวไปด้วยไหมครับ",
     items=_n(HOTELOWE + ["paszport", "prawo jazdy", "karta kredytowa", "gotówka",
                          "ładowarka", "powerbank", "parasol", "krem z filtrem",
                          "okulary przeciwsłoneczne", "kapelusz", "plaster",
                          "lek przeciwbólowy", "mapa", "portfel", "torba"],
              "Zawsze noszę przy sobie to, co dotyczy: %s.",
              "Nosisz przy sobie to, co dotyczy: %s?")),

dict(key="YANGMAIKHOEILAWNG", ty="sentence", cat="Gramatyka użytkowa", sub="Doświadczenie", reg="n",
     ph="phǒm yang mâi khoei lawng {ph} loei khráp", th="ผมยังไม่เคยลอง{th}เลยครับ",
     lit="yang mâi khoei lawng = jeszcze nigdy nie próbowałem",
     note="Trzy elementy naraz: „yang” = jeszcze, „mâi khoei” = nigdy dotąd, „loei” = ani razu. Tajski lubi takie piętrzenie.",
     ex_ph="khoei lawng {ph} mǎi khráp", ex_th="เคยลอง{th}ไหมครับ",
     items=_n(JEDZENIE + NAPOJE,
              "Nigdy jeszcze nie próbowałem tego, co dotyczy: %s.",
              "Próbowałeś kiedyś tego, co dotyczy: %s?")),

dict(key="KHAOWAA", ty="sentence", cat="Small talk", sub="Opinie", reg="p",
     ph="khǎo wâa {ph} nâa pai duu khráp", th="เขาว่า{th}น่าไปดูครับ",
     lit="khǎo wâa = ludzie mówią, podobno",
     note="„khǎo” znaczy tu „ludzie ogólnie”, nie „on”. Potoczne, ale słyszalne wszędzie.",
     ex_ph="khrai wâa {ph} nâa pai duu khráp", ex_th="ใครว่า{th}น่าไปดูครับ",
     items=_n(MIEJSCA,
              "Podobno warto zobaczyć to, co dotyczy: %s.",
              "Kto mówi, że warto zobaczyć: %s?")),

dict(key="TANGJAIPAI", ty="sentence", cat="Miejsca i orientacja", sub="Plany", reg="n",
     ph="phǒm tâng-jai jà pai {ph} hâi dâai khráp", th="ผมตั้งใจจะไป{th}ให้ได้ครับ",
     lit="tâng-jai jà … hâi dâai = postanowiłem i dopnę swego",
     note="Połączenie „tâng-jai” z „hâi dâai” daje najmocniejszą deklarację zamiaru w tajskim.",
     ex_ph="tâng-jai jà pai {ph} mûea-rài khráp", ex_th="ตั้งใจจะไป{th}เมื่อไหร่ครับ",
     items=_n(MIEJSCA,
              "Koniecznie chcę dotrzeć tam, gdzie jest: %s.",
              "Kiedy chcesz dotrzeć tam, gdzie jest: %s?")),

dict(key="JAWNGLUANGNAA", ty="sentence", cat="Hotel", sub="Rezerwacje", reg="f",
     ph="phǒm jawng {ph} lûang nâa khráp", th="ผมจอง{th}ล่วงหน้าครับ",
     lit="lûang nâa = z wyprzedzeniem",
     note="„jawng” obejmuje rezerwację pokoju, stolika, biletu i sprzętu. Jedno słowo na wszystko.",
     ex_ph="tâwng jawng {ph} lûang nâa mǎi khráp", ex_th="ต้องจอง{th}ล่วงหน้าไหมครับ",
     items=_n(HOTELOWE + ["stolik", "bilet", "wycieczka", "taksówka", "rower",
                          "motocykl", "salon masażu", "restauracja"],
              "Zarezerwowałem z wyprzedzeniem to, co dotyczy: %s.",
              "Czy trzeba rezerwować z wyprzedzeniem to, co dotyczy: %s?")),

dict(key="RAILAIAT", ty="sentence", cat="Praca i nauka", sub="Informacje", reg="f",
     ph="phǒm yàak sâap rai-lá-ìat rûeang {ph} khráp", th="ผมอยากทราบรายละเอียดเรื่อง{th}ครับ",
     lit="rai-lá-ìat = szczegóły",
     note="„sâap” to formalne „wiedzieć”. Razem z „rai-lá-ìat” tworzy zwrot urzędowy i biurowy.",
     ex_ph="rai-lá-ìat rûeang {ph} duu dâai thîi nǎi khráp", ex_th="รายละเอียดเรื่อง{th}ดูได้ที่ไหนครับ",
     items=_n(HOTELOWE + ["umowa", "ubezpieczenie", "wiza", "opłata", "zniżka",
                          "kurs wymiany", "przelew", "kaucja", "czynsz",
                          "umowa najmu", "rozkład jazdy", "wycieczka"],
              "Chciałbym poznać szczegóły w sprawie: %s.",
              "Gdzie sprawdzę szczegóły w sprawie: %s?")),

dict(key="MAIKHAATWAA", ty="sentence", cat="Cechy i opinie", sub="Zaskoczenie", reg="n",
     ph="mâi khâat wâa thîi nîi jà mii {ph} khráp", th="ไม่คาดว่าที่นี่จะมี{th}ครับ",
     lit="mâi khâat wâa = nie spodziewałem się, że",
     note="„khâat” to przewidywanie oparte na przesłankach, inaczej niż „nùek”, które jest zwykłym wyobrażeniem.",
     ex_ph="thîi nîi mii {ph} dûai rǒe khráp", ex_th="ที่นี่มี{th}ด้วยหรือครับ",
     items=_n(JEDZENIE + HOTELOWE,
              "Nie spodziewałem się, że będzie tu to, co dotyczy: %s.",
              "Naprawdę jest tu to, co dotyczy: %s?")),

dict(key="PHAE", ty="sentence", cat="Zdrowie", sub="Alergie", reg="f",
     ph="phǒm phǎe {ph} khráp", th="ผมแพ้{th}ครับ",
     lit="phǎe = mieć uczulenie, nie tolerować",
     note="Zdanie ratujące zdrowie. Wypowiedz je przed zamówieniem, nie po. „phǎe” obejmuje uczulenie i nietolerancję.",
     ex_ph="khun phǎe {ph} rǒe plào khráp", ex_th="คุณแพ้{th}หรือเปล่าครับ",
     items=_n(JEDZENIE + ["antybiotyk", "lek", "mleko", "alkohol", "orzeszki ziemne"],
              "Mam uczulenie na to, co dotyczy: %s.",
              "Czy ma pan uczulenie na to, co dotyczy: %s?")),

dict(key="THAEN", ty="question", cat="Restauracja", sub="Zamiana", reg="n",
     ph="phǒm khǎw yàang ùen thǎen {ph} dâai mǎi khráp",
     th="ผมขออย่างอื่นแทน{th}ได้ไหมครับ",
     lit="thǎen = zamiast, w zastępstwie",
     note="„thǎen” wskazuje zamianę jednego na drugie. Nie myl z „plìan”, które znaczy samą zmianę.",
     ex_ph="mii à-rai thǎen {ph} bâang khráp", ex_th="มีอะไรแทน{th}บ้างครับ",
     items=_n(JEDZENIE + NAPOJE,
              "Czy mogę prosić coś innego zamiast tego, co dotyczy: %s?",
              "Co można dostać zamiast tego, co dotyczy: %s?")),
]
