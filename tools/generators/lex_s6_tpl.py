# -*- coding: utf-8 -*-
"""Wzorce zdaniowe etapu 6.

Kazdy wzorzec ma ZAMKNIETA biala liste hasel bazowych, a polska strona rekordu
i przykladu jest pisana recznie, nie sklejana z fragmentow.

Konstrukcje sa dobrane tak, zeby nie powielaly etapow 1-5. Zuzyte juz zostaly
miedzy innymi: „yàak”, „tâwng”, „khoei … láew”, „phôoeng”, „kamlang … yùu”,
„mâi khâwi”, „koen pai”, „thâa … kâw …”, „kwàa … jà …”, „yîng … yîng …”,
„tham hâi …”, „khǎw wee-laa … sák khrûu”, „thùuk bang-kháp hâi …”.

Etap 6 siega po konstrukcje codzienne, ktorych wczesniejsze etapy nie ruszaly:
przypomnienie („yàa luem”), przejecie czynnosci („hâi phǒm … eeng”), brak sil
(„… mâi wǎai”), pytanie o doswiadczenie („khoei … mǎi”), zapotrzebowanie
(„tâwng kaan”), zdolnosc formalna („sǎa-mâat … dâai”), gotowosc („phráwm jà”),
checi („tem jai thîi jà”), zapobiegliwosc („… wái kàwn”), zacheta („… kan thòe”),
pytanie o osobe („mii khrai … bâang mǎi”), pytanie o miejsce („… trong nǎi dii”),
brak zasobu („mâi mii … loei”), dostepnosc w okolicy („… yùu thǎew níi mǎi”).

Pozycja: (polskie haslo rekordu, polskie haslo bazowe, polski przyklad)
"""

TPL = [

# =====================================================================
# yàa luem … na khrap — przypomnienie
# =====================================================================
dict(key="YAALUEM", ty="sentence", cat="Podstawy i grzeczność", sub="Przypomnienia", reg="n",
     ph="yàa luem {ph} ná khráp", th="อย่าลืม{th}นะครับ",
     lit="yàa luem … = nie zapomnij …",
     note="„yàa” to zakaz, ale w tej konstrukcji brzmi jak przyjacielskie przypomnienie, nie rozkaz. Bez „ná khráp” staje się szorstkie.",
     ex_ph="yàa luem {ph} ná khráp dǐao jà mâi than", ex_th="อย่าลืม{th}นะครับ เดี๋ยวจะไม่ทัน",
     items=[
       ("Nie zapomnij zapłacić.", "płacić", "Nie zapomnij zapłacić, bo potem nie zdążymy."),
       ("Nie zapomnij zarezerwować.", "rezerwować", "Nie zapomnij zarezerwować, bo potem nie będzie miejsc."),
       ("Nie zapomnij zamówić.", "zamawiać", "Nie zapomnij zamówić, bo kuchnia zaraz zamyka."),
       ("Nie zapomnij zamknąć.", "zamykać", "Nie zapomnij zamknąć, zanim wyjdziesz."),
       ("Nie zapomnij podpisać.", "podpisać", "Nie zapomnij podpisać, inaczej nie przyjmą."),
       ("Nie zapomnij wysłać.", "wysyłać", "Nie zapomnij wysłać, termin jest dziś."),
       ("Nie zapomnij zadzwonić.", "dzwonić", "Nie zapomnij zadzwonić, oni czekają."),
       ("Nie zapomnij odpowiedzieć.", "odpowiadać", "Nie zapomnij odpowiedzieć, to pilne."),
       ("Nie zapomnij zapytać.", "pytać", "Nie zapomnij zapytać, zanim podpiszesz."),
       ("Nie zapomnij poczekać na mnie.", "czekać", "Nie zapomnij na mnie poczekać przy wyjściu."),
       ("Nie zapomnij wypełnić formularza.", "wypełnić formularz", "Nie zapomnij wypełnić formularza przed wejściem."),
       ("Nie zapomnij się spakować.", "pakować się", "Nie zapomnij się spakować, wyjeżdżamy rano."),
       ("Nie zapomnij pokazać biletu.", "pokazać", "Nie zapomnij pokazać biletu przy wejściu."),
       ("Nie zapomnij odebrać reszty.", "odbierać", "Nie zapomnij odebrać reszty przy kasie."),
       ("Nie zapomnij wziąć kluczy.", "brać", "Nie zapomnij wziąć kluczy ze sobą."),
       ("Nie zapomnij kupić wody.", "kupować", "Nie zapomnij kupić wody na drogę."),
       ("Nie zapomnij zmienić rezerwacji.", "zmieniać", "Nie zapomnij zmienić rezerwacji na późniejszą godzinę."),
       ("Nie zapomnij anulować.", "anulować", "Nie zapomnij anulować, inaczej naliczą opłatę."),
       ("Nie zapomnij się wyspać.", "spać", "Nie zapomnij się wyspać, jutro długi dzień."),
       ("Nie zapomnij odpocząć.", "odpoczywać", "Nie zapomnij odpocząć między spotkaniami."),
       ("Nie zapomnij zjeść.", "jeść", "Nie zapomnij zjeść, minęło południe."),
       ("Nie zapomnij napić się wody.", "pić", "Nie zapomnij napić się wody, jest gorąco."),
       ("Nie zapomnij poprosić o rachunek.", "policzyć rachunek", "Nie zapomnij poprosić o rachunek przed wyjściem."),
       ("Nie zapomnij zapisać adresu.", "pisać", "Nie zapomnij zapisać adresu, żeby wrócić."),
     ]),

# =====================================================================
# hai phom … eeng khrap — przejecie czynnosci na siebie
# =====================================================================
dict(key="HAIPHOMEENG", ty="sentence", cat="Podstawy i grzeczność", sub="Uprzejmości", reg="n",
     ph="hâi phǒm {ph} eeng khráp", th="ให้ผม{th}เองครับ",
     lit="hâi phǒm … eeng = pozwól, że ja sam …",
     note="Uprzejme przejęcie czynności od rozmówcy. „eeng” podkreśla, że robisz to osobiście i nie oczekujesz pomocy.",
     ex_ph="mâi pen rai khráp hâi phǒm {ph} eeng", ex_th="ไม่เป็นไรครับ ให้ผม{th}เอง",
     items=[
       ("Ja zapłacę.", "płacić", "Nie trzeba, ja zapłacę."),
       ("Ja to zrobię.", "robić", "Nie trzeba, ja to zrobię."),
       ("Ja poprowadzę.", "prowadzić samochód", "Nie trzeba, ja poprowadzę."),
       ("Ja zamówię.", "zamawiać", "Nie trzeba, ja zamówię."),
       ("Ja zadzwonię.", "dzwonić", "Nie trzeba, ja zadzwonię."),
       ("Ja poszukam.", "szukać", "Nie trzeba, ja poszukam."),
       ("Ja zaniosę.", "dawać", "Nie trzeba, ja zaniosę."),
       ("Ja wypełnię formularz.", "wypełnić formularz", "Nie trzeba, ja wypełnię formularz."),
       ("Ja się spakuję.", "pakować się", "Nie trzeba, ja się spakuję."),
       ("Ja pozmywam.", "myć", "Nie trzeba, ja pozmywam."),
       ("Ja zarezerwuję.", "rezerwować", "Nie trzeba, ja zarezerwuję."),
       ("Ja odbiorę.", "odbierać", "Nie trzeba, ja odbiorę."),
       ("Ja wyślę.", "wysyłać", "Nie trzeba, ja wyślę."),
       ("Ja zapytam.", "pytać", "Nie trzeba, ja zapytam."),
       ("Ja poczekam.", "czekać", "Nie trzeba, ja poczekam."),
       ("Ja wybiorę.", "wybierać", "Nie trzeba, ja wybiorę."),
       ("Ja pomogę.", "pomagać", "Nie trzeba nikogo wołać, ja pomogę."),
       ("Ja to napiszę.", "pisać", "Nie trzeba, ja to napiszę."),
       ("Ja zamknę.", "zamykać", "Nie trzeba, ja zamknę."),
       ("Ja otworzę.", "otwierać", "Nie trzeba, ja otworzę."),
     ]),

# =====================================================================
# … mai wai khrap — brak sil, nie daje rady
# =====================================================================
dict(key="MAIWAI", ty="sentence", cat="Zdrowie", sub="Samopoczucie", reg="n",
     ph="phǒm {ph} mâi wǎai khráp", th="ผม{th}ไม่ไหวครับ",
     lit="… mâi wǎai = nie mam siły …",
     note="„mâi wǎai” dotyczy braku sił, a „mâi dâai” braku możliwości lub pozwolenia. Ta różnica sprawia Polakom najwięcej kłopotu.",
     ex_ph="wan níi phǒm {ph} mâi wǎai jing jing khráp", ex_th="วันนี้ผม{th}ไม่ไหวจริงๆ ครับ",
     items=[
       ("Nie dam rady dziś pracować.", "pracować", "Dziś naprawdę nie dam rady pracować."),
       ("Nie dam rady iść dalej.", "iść / jechać", "Dziś naprawdę nie dam rady iść dalej."),
       ("Nie dam rady jeść więcej.", "jeść", "Dziś naprawdę nie dam rady jeść więcej."),
       ("Nie dam rady czekać dłużej.", "czekać", "Dziś naprawdę nie dam rady czekać dłużej."),
       ("Nie dam rady biegać.", "biegać", "Dziś naprawdę nie dam rady biegać."),
       ("Nie dam rady pływać.", "pływać", "Dziś naprawdę nie dam rady pływać."),
       ("Nie dam rady prowadzić.", "prowadzić samochód", "Dziś naprawdę nie dam rady prowadzić."),
       ("Nie dam rady się uczyć.", "uczyć się", "Dziś naprawdę nie dam rady się uczyć."),
       ("Nie dam rady dłużej siedzieć.", "siedzieć", "Dziś naprawdę nie dam rady dłużej siedzieć."),
       ("Nie dam rady tańczyć.", "tańczyć", "Dziś naprawdę nie dam rady tańczyć."),
       ("Nie dam rady dziś zwiedzać.", "zwiedzać", "Dziś naprawdę nie dam rady zwiedzać."),
       ("Nie dam rady tyle nieść.", "brać", "Dziś naprawdę nie dam rady tyle nieść."),
       ("Nie dam rady dziś gotować.", "gotować", "Dziś naprawdę nie dam rady gotować."),
       ("Nie dam rady dziś sprzątać.", "sprzątać", "Dziś naprawdę nie dam rady sprzątać."),
       ("Nie dam rady dziś prać.", "prać", "Dziś naprawdę nie dam rady prać."),
       ("Nie dam rady dziś rozmawiać.", "rozmawiać", "Dziś naprawdę nie dam rady rozmawiać."),
     ]),

# =====================================================================
# khoei … mai khrap — pytanie o doswiadczenie
# =====================================================================
dict(key="KHOEIMAI", ty="question", cat="Pytania", sub="Doświadczenie", reg="n",
     ph="khoei {ph} mǎi khráp", th="เคย{th}ไหมครับ",
     lit="khoei … mǎi = czy zdarzyło ci się kiedyś …?",
     note="„khoei” pyta o doświadczenie kiedykolwiek w życiu, nie o niedawną czynność. Odpowiedź brzmi „khoei” albo „mâi khoei”.",
     ex_ph="khun khoei {ph} thîi mueang thai mǎi khráp", ex_th="คุณเคย{th}ที่เมืองไทยไหมครับ",
     items=[
       ("Czy próbowałeś kiedyś tego?", "próbować (smakować)", "Czy próbowałeś tego kiedyś w Tajlandii?"),
       ("Czy jeździłeś kiedyś sam?", "prowadzić samochód", "Czy prowadziłeś kiedyś samochód w Tajlandii?"),
       ("Czy pływałeś tu kiedyś?", "pływać", "Czy pływałeś kiedyś w Tajlandii?"),
       ("Czy pracowałeś kiedyś tutaj?", "pracować", "Czy pracowałeś kiedyś w Tajlandii?"),
       ("Czy uczyłeś się tego kiedyś?", "uczyć się", "Czy uczyłeś się tego kiedyś w Tajlandii?"),
       ("Czy wynajmowałeś kiedyś?", "wynajmować", "Czy wynajmowałeś kiedyś coś w Tajlandii?"),
       ("Czy rezerwowałeś kiedyś sam?", "rezerwować", "Czy rezerwowałeś kiedyś sam w Tajlandii?"),
       ("Czy gotowałeś to kiedyś?", "gotować", "Czy gotowałeś to kiedyś w Tajlandii?"),
       ("Czy zwiedzałeś to kiedyś?", "zwiedzać", "Czy zwiedzałeś to kiedyś w Tajlandii?"),
       ("Czy śpiewałeś kiedyś publicznie?", "śpiewać", "Czy śpiewałeś kiedyś publicznie w Tajlandii?"),
       ("Czy tańczyłeś to kiedyś?", "tańczyć", "Czy tańczyłeś to kiedyś w Tajlandii?"),
       ("Czy przesiadałeś się tu kiedyś?", "przesiadać się", "Czy przesiadałeś się kiedyś w Tajlandii?"),
       ("Czy robiłeś tu kiedyś zdjęcia?", "robić zdjęcia", "Czy robiłeś kiedyś zdjęcia w Tajlandii?"),
       ("Czy zgubiłeś się tu kiedyś?", "zgubić", "Czy zgubiłeś coś kiedyś w Tajlandii?"),
       ("Czy pożyczałeś komuś kiedyś?", "pożyczyć", "Czy pożyczałeś komuś kiedyś w Tajlandii?"),
       ("Czy anulowałeś kiedyś rezerwację?", "anulować", "Czy anulowałeś kiedyś rezerwację w Tajlandii?"),
       ("Czy płaciłeś tu kiedyś kartą?", "płacić", "Czy płaciłeś kiedyś kartą w Tajlandii?"),
       ("Czy mieszkałeś tu kiedyś?", "spać", "Czy nocowałeś kiedyś w Tajlandii?"),
     ]),

# =====================================================================
# phom tawng kaan … khrap — zapotrzebowanie formalne
# =====================================================================
dict(key="TAWNGKAAN", ty="sentence", cat="Praca i nauka", sub="Prośby", reg="f",
     ph="phǒm tâwng kaan {ph} khráp", th="ผมต้องการ{th}ครับ",
     lit="tâwng kaan … = potrzebuję …",
     note="„tâwng kaan” to formalne „potrzebuję”, używane w urzędzie i w piśmie. W rozmowie ze znajomym zabrzmi sztywno — tam lepsze jest „yàak dâai”.",
     ex_ph="phǒm tâwng kaan {ph} khráp chûai náe nam nòi", ex_th="ผมต้องการ{th}ครับ ช่วยแนะนำหน่อย",
     items=[
       ("Potrzebuję pokoju.", "pokój", "Potrzebuję pokoju, proszę o poradę."),
       ("Potrzebuję lekarstwa.", "lek", "Potrzebuję lekarstwa, proszę o poradę."),
       ("Potrzebuję mapy.", "mapa", "Potrzebuję mapy, proszę o poradę."),
       ("Potrzebuję karty SIM.", "karta SIM", "Potrzebuję karty SIM, proszę o poradę."),
       ("Potrzebuję paragonu.", "paragon", "Potrzebuję paragonu, proszę o poradę."),
       ("Potrzebuję taksówki.", "samochód", "Potrzebuję samochodu, proszę o poradę."),
       ("Potrzebuję przejściówki.", "przejściówka", "Potrzebuję przejściówki, proszę o poradę."),
       ("Potrzebuję ręcznika.", "ręcznik", "Potrzebuję ręcznika, proszę o poradę."),
       ("Potrzebuję koca.", "koc", "Potrzebuję koca, proszę o poradę."),
       ("Potrzebuję gotówki.", "gotówka", "Potrzebuję gotówki, proszę o poradę."),
       ("Potrzebuję prawa jazdy.", "prawo jazdy", "Potrzebuję prawa jazdy, proszę o poradę."),
       ("Potrzebuję kasku.", "kask", "Potrzebuję kasku, proszę o poradę."),
       ("Potrzebuję plastra.", "plaster", "Potrzebuję plastra, proszę o poradę."),
       ("Potrzebuję leku przeciwbólowego.", "lek przeciwbólowy", "Potrzebuję leku przeciwbólowego, proszę o poradę."),
       ("Potrzebuję bandaża.", "bandaż", "Potrzebuję bandaża, proszę o poradę."),
       ("Potrzebuję przewodnika.", "przewodnik (osoba)", "Potrzebuję przewodnika, proszę o poradę."),
       ("Potrzebuję rozkładu jazdy.", "rozkład jazdy", "Potrzebuję rozkładu jazdy, proszę o poradę."),
       ("Potrzebuję powerbanku.", "powerbank", "Potrzebuję powerbanku, proszę o poradę."),
       ("Potrzebuję kremu z filtrem.", "krem z filtrem", "Potrzebuję kremu z filtrem, proszę o poradę."),
       ("Potrzebuję sejfu.", "sejf", "Potrzebuję sejfu, proszę o poradę."),
     ]),

# =====================================================================
# phom saa-maat … daai khrap — zdolnosc, wersja formalna
# =====================================================================
dict(key="SAAMAAT", ty="sentence", cat="Praca i nauka", sub="Możliwości", reg="f",
     ph="phǒm sǎa-mâat {ph} dâai khráp", th="ผมสามารถ{th}ได้ครับ",
     lit="sǎa-mâat … dâai = jestem w stanie …",
     note="Wersja formalna, właściwa dla rozmowy o pracę i pism urzędowych. W barze zabrzmi pretensjonalnie — tam wystarczy samo „… dâai”.",
     ex_ph="phǒm sǎa-mâat {ph} dâai khráp mâi mii pan-hǎa", ex_th="ผมสามารถ{th}ได้ครับ ไม่มีปัญหา",
     items=[
       ("Jestem w stanie to zrobić.", "robić", "Jestem w stanie to zrobić, nie ma problemu."),
       ("Jestem w stanie prowadzić samochód.", "prowadzić samochód", "Jestem w stanie prowadzić, nie ma problemu."),
       ("Jestem w stanie pomóc.", "pomagać", "Jestem w stanie pomóc, nie ma problemu."),
       ("Jestem w stanie pracować w weekendy.", "pracować", "Jestem w stanie pracować w weekendy, nie ma problemu."),
       ("Jestem w stanie się tego nauczyć.", "uczyć się", "Jestem w stanie się tego nauczyć, nie ma problemu."),
       ("Jestem w stanie to napisać.", "pisać", "Jestem w stanie to napisać, nie ma problemu."),
       ("Jestem w stanie to przetłumaczyć ustnie.", "mówić", "Jestem w stanie to powiedzieć, nie ma problemu."),
       ("Jestem w stanie zapłacić od razu.", "płacić", "Jestem w stanie zapłacić od razu, nie ma problemu."),
       ("Jestem w stanie przyjść wcześniej.", "przyjść / przyjechać", "Jestem w stanie przyjść wcześniej, nie ma problemu."),
       ("Jestem w stanie poczekać.", "czekać", "Jestem w stanie poczekać, nie ma problemu."),
       ("Jestem w stanie to zorganizować.", "rezerwować", "Jestem w stanie to zarezerwować, nie ma problemu."),
       ("Jestem w stanie gotować.", "gotować", "Jestem w stanie gotować, nie ma problemu."),
       ("Jestem w stanie wypełnić formularz.", "wypełnić formularz", "Jestem w stanie wypełnić formularz, nie ma problemu."),
       ("Jestem w stanie to wysłać dzisiaj.", "wysyłać", "Jestem w stanie to wysłać dzisiaj, nie ma problemu."),
       ("Jestem w stanie odebrać przesyłkę.", "odbierać", "Jestem w stanie odebrać przesyłkę, nie ma problemu."),
       ("Jestem w stanie to sprawdzić.", "szukać", "Jestem w stanie to sprawdzić, nie ma problemu."),
     ]),

# =====================================================================
# phom phraawm ja … khrap — gotowosc
# =====================================================================
dict(key="PHRAWMJA", ty="sentence", cat="Praca i nauka", sub="Ustalenia", reg="f",
     ph="phǒm phráwm jà {ph} khráp", th="ผมพร้อมจะ{th}ครับ",
     lit="phráwm jà … = jestem gotów …",
     note="„phráwm” znaczy „gotowy” i „w komplecie”. Zdanie sygnalizuje, że czekasz tylko na sygnał drugiej strony.",
     ex_ph="phǒm phráwm jà {ph} mûea rài kâw dâai khráp", ex_th="ผมพร้อมจะ{th}เมื่อไหร่ก็ได้ครับ",
     items=[
       ("Jestem gotów zacząć.", "zaczynać", "Jestem gotów zacząć w każdej chwili."),
       ("Jestem gotów zapłacić.", "płacić", "Jestem gotów zapłacić w każdej chwili."),
       ("Jestem gotów wyjechać.", "iść / jechać", "Jestem gotów wyjechać w każdej chwili."),
       ("Jestem gotów pomóc.", "pomagać", "Jestem gotów pomóc w każdej chwili."),
       ("Jestem gotów się spotkać.", "spotykać", "Jestem gotów się spotkać w każdej chwili."),
       ("Jestem gotów podpisać.", "podpisać", "Jestem gotów podpisać w każdej chwili."),
       ("Jestem gotów się przeprowadzić.", "wracać", "Jestem gotów wrócić w każdej chwili."),
       ("Jestem gotów porozmawiać.", "rozmawiać", "Jestem gotów porozmawiać w każdej chwili."),
       ("Jestem gotów to zmienić.", "zmieniać", "Jestem gotów to zmienić w każdej chwili."),
       ("Jestem gotów poczekać.", "czekać", "Jestem gotów poczekać w każdej chwili."),
       ("Jestem gotów zarezerwować.", "rezerwować", "Jestem gotów zarezerwować w każdej chwili."),
       ("Jestem gotów to wysłać.", "wysyłać", "Jestem gotów to wysłać w każdej chwili."),
       ("Jestem gotów wynająć.", "wynajmować", "Jestem gotów wynająć w każdej chwili."),
       ("Jestem gotów odpowiedzieć.", "odpowiadać", "Jestem gotów odpowiedzieć w każdej chwili."),
     ]),

# =====================================================================
# tem jai thii ja … khrap — checi, uprzejma zgoda
# =====================================================================
dict(key="TEMJAI", ty="sentence", cat="Podstawy i grzeczność", sub="Uprzejmości", reg="f",
     ph="tem jai thîi jà {ph} khráp", th="เต็มใจที่จะ{th}ครับ",
     lit="tem jai = pełne serce, czyli z własnej chęci",
     note="Mocniejsze i cieplejsze niż „dâai khráp”. Sygnalizuje, że robisz coś chętnie, a nie z obowiązku.",
     ex_ph="phǒm tem jai thîi jà {ph} khráp mâi tâwng kreeng jai", ex_th="ผมเต็มใจที่จะ{th}ครับ ไม่ต้องเกรงใจ",
     items=[
       ("Chętnie pomogę.", "pomagać", "Chętnie pomogę, proszę się nie krępować."),
       ("Chętnie poczekam.", "czekać", "Chętnie poczekam, proszę się nie krępować."),
       ("Chętnie wytłumaczę.", "mówić", "Chętnie o tym opowiem, proszę się nie krępować."),
       ("Chętnie pokażę.", "pokazać", "Chętnie pokażę, proszę się nie krępować."),
       ("Chętnie oprowadzę.", "zwiedzać", "Chętnie oprowadzę, proszę się nie krępować."),
       ("Chętnie ugotuję.", "gotować", "Chętnie ugotuję, proszę się nie krępować."),
       ("Chętnie zapłacę.", "płacić", "Chętnie zapłacę, proszę się nie krępować."),
       ("Chętnie zarezerwuję.", "rezerwować", "Chętnie zarezerwuję, proszę się nie krępować."),
       ("Chętnie odbiorę cię z lotniska.", "odbierać", "Chętnie odbiorę, proszę się nie krępować."),
       ("Chętnie posłucham.", "słuchać", "Chętnie posłucham, proszę się nie krępować."),
       ("Chętnie zaproszę.", "zapraszać", "Chętnie zaproszę, proszę się nie krępować."),
       ("Chętnie poszukam.", "szukać", "Chętnie poszukam, proszę się nie krępować."),
     ]),

# =====================================================================
# … wai kawn dii kwaa khrap — zapobiegliwosc
# =====================================================================
dict(key="WAIKAWN", ty="sentence", cat="Gramatyka użytkowa", sub="Rady", reg="n",
     ph="{ph} wái kàwn dii kwàa khráp", th="{th}ไว้ก่อนดีกว่าครับ",
     lit="… wái kàwn = zrobić coś zawczasu i zostawić gotowe",
     note="„wái” oznacza czynność wykonaną na zapas, z myślą o przyszłości. To jeden z najbardziej tajskich odcieni czasownika — polski nie ma dla niego jednego słowa.",
     ex_ph="{ph} wái kàwn dii kwàa khráp dǐao khon yóe", ex_th="{th}ไว้ก่อนดีกว่าครับ เดี๋ยวคนเยอะ",
     items=[
       ("Lepiej zarezerwować z wyprzedzeniem.", "rezerwować", "Lepiej zarezerwować wcześniej, bo potem będzie tłok."),
       ("Lepiej kupić zawczasu.", "kupować", "Lepiej kupić wcześniej, bo potem będzie tłok."),
       ("Lepiej zapłacić od razu.", "płacić", "Lepiej zapłacić wcześniej, bo potem będzie tłok."),
       ("Lepiej zapytać wcześniej.", "pytać", "Lepiej zapytać wcześniej, bo potem będzie tłok."),
       ("Lepiej spakować się wcześniej.", "pakować się", "Lepiej spakować się wcześniej, bo potem będzie tłok."),
       ("Lepiej zamówić wcześniej.", "zamawiać", "Lepiej zamówić wcześniej, bo potem będzie tłok."),
       ("Lepiej się wyspać.", "spać", "Lepiej się wyspać wcześniej, bo potem będzie tłok."),
       ("Lepiej wcześniej zjeść.", "jeść", "Lepiej zjeść wcześniej, bo potem będzie tłok."),
       ("Lepiej wcześniej się dowiedzieć.", "pokazać", "Lepiej wcześniej to pokazać, bo potem będzie tłok."),
       ("Lepiej wcześniej wypełnić formularz.", "wypełnić formularz", "Lepiej wypełnić formularz wcześniej, bo potem będzie tłok."),
       ("Lepiej wcześniej wysłać.", "wysyłać", "Lepiej wysłać wcześniej, bo potem będzie tłok."),
       ("Lepiej wcześniej wybrać.", "wybierać", "Lepiej wybrać wcześniej, bo potem będzie tłok."),
       ("Lepiej wcześniej wynająć.", "wynajmować", "Lepiej wynająć wcześniej, bo potem będzie tłok."),
       ("Lepiej wcześniej odpocząć.", "odpoczywać", "Lepiej odpocząć wcześniej, bo potem będzie tłok."),
     ]),

# =====================================================================
# … kan thoe — zacheta do wspolnego dzialania
# =====================================================================
dict(key="KANTHOE", ty="sentence", cat="Small talk", sub="Propozycje", reg="i",
     ph="{ph} kan thòe", th="{th}กันเถอะ",
     lit="… kan thòe = chodźmy / zróbmy to razem",
     note="„kan” oznacza wspólnie, „thòe” to zachęta. Zwrot nieformalny — wobec przełożonego użyj „… kan mǎi khráp”.",
     ex_ph="{ph} kan thòe dǐao kâw yen láew", ex_th="{th}กันเถอะ เดี๋ยวก็เย็นแล้ว",
     items=[
       ("Chodźmy coś zjeść.", "jeść", "Chodźmy coś zjeść, robi się późno."),
       ("Chodźmy już.", "iść / jechać", "Chodźmy już, robi się późno."),
       ("Odpocznijmy chwilę.", "odpoczywać", "Odpocznijmy chwilę, robi się późno."),
       ("Zacznijmy.", "zaczynać", "Zacznijmy, robi się późno."),
       ("Wracajmy.", "wracać", "Wracajmy, robi się późno."),
       ("Zamówmy coś.", "zamawiać", "Zamówmy coś, robi się późno."),
       ("Porozmawiajmy o tym.", "rozmawiać", "Porozmawiajmy o tym, robi się późno."),
       ("Poczekajmy jeszcze chwilę.", "czekać", "Poczekajmy jeszcze chwilę, robi się późno."),
       ("Zwiedzajmy dalej.", "zwiedzać", "Zwiedzajmy dalej, robi się późno."),
       ("Popływajmy.", "pływać", "Popływajmy, robi się późno."),
       ("Zróbmy zdjęcie.", "robić zdjęcia", "Zróbmy zdjęcie, robi się późno."),
       ("Poszukajmy razem.", "szukać", "Poszukajmy razem, robi się późno."),
       ("Podzielmy się rachunkiem.", "płacić", "Zapłaćmy razem, robi się późno."),
       ("Spotkajmy się.", "spotykać", "Spotkajmy się, robi się późno."),
       ("Pouczmy się razem.", "uczyć się", "Pouczmy się razem, robi się późno."),
       ("Zaśpiewajmy.", "śpiewać", "Zaśpiewajmy, robi się późno."),
     ]),

# =====================================================================
# mii khrai … baang mai khrap — pytanie o osobe
# =====================================================================
dict(key="MIIKHRAI", ty="question", cat="Pytania", sub="Osoby", reg="n",
     ph="mii khrai {ph} bâang mǎi khráp", th="มีใคร{th}บ้างไหมครับ",
     lit="mii khrai … bâang mǎi = czy ktoś …?",
     note="„bâang” sygnalizuje, że spodziewasz się więcej niż jednej odpowiedzi. Bez niego pytanie brzmi jak sprawdzanie listy obecności.",
     ex_ph="mii khrai {ph} bâang mǎi khráp phǒm tâwng kaan khon chûai", ex_th="มีใคร{th}บ้างไหมครับ ผมต้องการคนช่วย",
     items=[
       ("Czy ktoś mówi po angielsku?", "mówić", "Czy ktoś tu mówi? Potrzebuję pomocy."),
       ("Czy ktoś umie prowadzić?", "prowadzić samochód", "Czy ktoś umie prowadzić? Potrzebuję pomocy."),
       ("Czy ktoś może pomóc?", "pomagać", "Czy ktoś może pomóc? Potrzebuję pomocy."),
       ("Czy ktoś tu czeka?", "czekać", "Czy ktoś tu czeka? Potrzebuję pomocy."),
       ("Czy ktoś to widział?", "oglądać", "Czy ktoś to widział? Potrzebuję pomocy."),
       ("Czy ktoś tego szuka?", "szukać", "Czy ktoś tego szuka? Potrzebuję pomocy."),
       ("Czy ktoś to zamawiał?", "zamawiać", "Czy ktoś to zamawiał? Potrzebuję pomocy."),
       ("Czy ktoś już zapłacił?", "płacić", "Czy ktoś już zapłacił? Potrzebuję pomocy."),
       ("Czy ktoś umie pływać?", "pływać", "Czy ktoś umie pływać? Potrzebuję pomocy."),
       ("Czy ktoś to zna?", "znać", "Czy ktoś to zna? Potrzebuję pomocy."),
       ("Czy ktoś tu pracuje?", "pracować", "Czy ktoś tu pracuje? Potrzebuję pomocy."),
       ("Czy ktoś umie gotować?", "gotować", "Czy ktoś umie gotować? Potrzebuję pomocy."),
       ("Czy ktoś tu mieszka?", "spać", "Czy ktoś tu nocuje? Potrzebuję pomocy."),
       ("Czy ktoś się na tym zna?", "rozumieć", "Czy ktoś to rozumie? Potrzebuję pomocy."),
     ]),

# =====================================================================
# … trong nai dii khrap — pytanie o najlepsze miejsce
# =====================================================================
dict(key="TRONGNAIDII", ty="question", cat="Miejsca i orientacja", sub="Orientacja", reg="n",
     ph="{ph} trong nǎi dii khráp", th="{th}ตรงไหนดีครับ",
     lit="… trong nǎi dii = gdzie najlepiej …?",
     note="„dii” na końcu pytania prosi o radę, nie o suchą informację. Rozmówca odpowie wtedy rekomendacją, a nie samym adresem.",
     ex_ph="{ph} trong nǎi dii khráp phǒm mâi khún khooei", ex_th="{th}ตรงไหนดีครับ ผมไม่คุ้นเคย",
     items=[
       ("Gdzie najlepiej zaparkować?", "zatrzymać się", "Gdzie najlepiej się zatrzymać? Nie znam okolicy."),
       ("Gdzie najlepiej wysiąść?", "wysiadać", "Gdzie najlepiej wysiąść? Nie znam okolicy."),
       ("Gdzie najlepiej wsiąść?", "wsiadać", "Gdzie najlepiej wsiąść? Nie znam okolicy."),
       ("Gdzie najlepiej się przesiąść?", "przesiadać się", "Gdzie najlepiej się przesiąść? Nie znam okolicy."),
       ("Gdzie najlepiej zjeść?", "jeść", "Gdzie najlepiej zjeść? Nie znam okolicy."),
       ("Gdzie najlepiej kupić pamiątki?", "kupować", "Gdzie najlepiej kupić? Nie znam okolicy."),
       ("Gdzie najlepiej poczekać?", "czekać", "Gdzie najlepiej poczekać? Nie znam okolicy."),
       ("Gdzie najlepiej usiąść?", "siedzieć", "Gdzie najlepiej usiąść? Nie znam okolicy."),
       ("Gdzie najlepiej popływać?", "pływać", "Gdzie najlepiej popływać? Nie znam okolicy."),
       ("Gdzie najlepiej robić zdjęcia?", "robić zdjęcia", "Gdzie najlepiej robić zdjęcia? Nie znam okolicy."),
       ("Gdzie najlepiej wymienić pieniądze?", "zmieniać", "Gdzie najlepiej to zmienić? Nie znam okolicy."),
       ("Gdzie najlepiej wynająć skuter?", "wynajmować", "Gdzie najlepiej wynająć? Nie znam okolicy."),
       ("Gdzie najlepiej zapłacić?", "płacić", "Gdzie najlepiej zapłacić? Nie znam okolicy."),
       ("Gdzie najlepiej skręcić?", "skręcać", "Gdzie najlepiej skręcić? Nie znam okolicy."),
     ]),

# =====================================================================
# mai mii … loei khrap — kategoryczny brak
# =====================================================================
dict(key="MAIMIILOEI", ty="sentence", cat="Awarie i pomoc", sub="Braki", reg="n",
     ph="mâi mii {ph} loei khráp", th="ไม่มี{th}เลยครับ",
     lit="mâi mii … loei = w ogóle nie ma …",
     note="„loei” domyka przeczenie do zera. Bez niego zdanie znaczy tylko „nie ma”, co brzmi jak chwilowy brak, a nie całkowity.",
     ex_ph="nai hâwng mâi mii {ph} loei khráp chûai duu hâi nòi", ex_th="ในห้องไม่มี{th}เลยครับ ช่วยดูให้หน่อย",
     items=[
       ("W ogóle nie ma ręcznika.", "ręcznik", "W pokoju w ogóle nie ma ręcznika, proszę to sprawdzić."),
       ("W ogóle nie ma gorącej wody.", "gorąca woda", "W pokoju w ogóle nie ma gorącej wody, proszę to sprawdzić."),
       ("W ogóle nie ma papieru toaletowego.", "papier toaletowy", "W pokoju w ogóle nie ma papieru, proszę to sprawdzić."),
       ("W ogóle nie ma mydła.", "mydło", "W pokoju w ogóle nie ma mydła, proszę to sprawdzić."),
       ("W ogóle nie ma koca.", "koc", "W pokoju w ogóle nie ma koca, proszę to sprawdzić."),
       ("W ogóle nie ma poduszki.", "poduszka", "W pokoju w ogóle nie ma poduszki, proszę to sprawdzić."),
       ("W ogóle nie ma internetu.", "internet", "W pokoju w ogóle nie ma internetu, proszę to sprawdzić."),
       ("W ogóle nie ma gniazdka.", "gniazdko", "W pokoju w ogóle nie ma gniazdka, proszę to sprawdzić."),
       ("W ogóle nie ma klucza.", "klucz", "W pokoju w ogóle nie ma klucza, proszę to sprawdzić."),
       ("W ogóle nie ma menu.", "menu", "Tutaj w ogóle nie ma menu, proszę to sprawdzić."),
       ("W ogóle nie ma serwetek.", "serwetka", "Tutaj w ogóle nie ma serwetek, proszę to sprawdzić."),
       ("W ogóle nie ma reszty.", "reszta", "Tutaj w ogóle nie ma reszty, proszę to sprawdzić."),
       ("W ogóle nie ma lodu.", "lód", "Tutaj w ogóle nie ma lodu, proszę to sprawdzić."),
       ("W ogóle nie ma paragonu.", "paragon", "Tutaj w ogóle nie ma paragonu, proszę to sprawdzić."),
       ("W ogóle nie ma pościeli.", "pościel", "W pokoju w ogóle nie ma pościeli, proszę to sprawdzić."),
       ("W ogóle nie ma lodówki.", "lodówka w pokoju", "W pokoju w ogóle nie ma lodówki, proszę to sprawdzić."),
       ("W ogóle nie ma hasła do wi-fi.", "hasło", "W pokoju w ogóle nie ma hasła, proszę to sprawdzić."),
       ("W ogóle nie ma wentylatora.", "wentylator", "W pokoju w ogóle nie ma wentylatora, proszę to sprawdzić."),
       ("W ogóle nie ma światła.", "światło", "W pokoju w ogóle nie ma światła, proszę to sprawdzić."),
       ("W ogóle nie ma ładowarki.", "ładowarka", "W pokoju w ogóle nie ma ładowarki, proszę to sprawdzić."),
       ("W ogóle nie ma czajnika.", "czajnik", "W pokoju w ogóle nie ma czajnika, proszę to sprawdzić."),
     ]),

# =====================================================================
# … yuu thaew nii mai khrap — dostepnosc w okolicy
# =====================================================================
dict(key="THAEWNII", ty="question", cat="Miejsca i orientacja", sub="W okolicy", reg="n",
     ph="thǎew níi mii {ph} mǎi khráp", th="แถวนี้มี{th}ไหมครับ",
     lit="thǎew níi = w tej okolicy",
     note="„thǎew” to okolica w promieniu spaceru. Pytanie brzmi naturalniej niż „klâi klâi níi mii …”, którego uczą podręczniki.",
     ex_ph="thǎew níi mii {ph} mǎi khráp klâi thîi sùt yùu thîi nǎi", ex_th="แถวนี้มี{th}ไหมครับ ใกล้ที่สุดอยู่ที่ไหน",
     items=[
       ("Czy w okolicy jest apteka?", "apteka", "Czy w okolicy jest apteka? Gdzie najbliższa?"),
       ("Czy w okolicy jest bankomat?", "bankomat", "Czy w okolicy jest bankomat? Gdzie najbliższy?"),
       ("Czy w okolicy jest szpital?", "szpital", "Czy w okolicy jest szpital? Gdzie najbliższy?"),
       ("Czy w okolicy jest przystanek?", "przystanek", "Czy w okolicy jest przystanek? Gdzie najbliższy?"),
       ("Czy w okolicy jest sklep całodobowy?", "sklep całodobowy", "Czy w okolicy jest sklep całodobowy? Gdzie najbliższy?"),
       ("Czy w okolicy jest kantor?", "kantor", "Czy w okolicy jest kantor? Gdzie najbliższy?"),
       ("Czy w okolicy jest pralnia?", "pralnia", "Czy w okolicy jest pralnia? Gdzie najbliższa?"),
       ("Czy w okolicy jest stacja benzynowa?", "stacja benzynowa", "Czy w okolicy jest stacja benzynowa? Gdzie najbliższa?"),
       ("Czy w okolicy jest kawiarnia?", "kawiarnia", "Czy w okolicy jest kawiarnia? Gdzie najbliższa?"),
       ("Czy w okolicy jest restauracja?", "restauracja", "Czy w okolicy jest restauracja? Gdzie najbliższa?"),
       ("Czy w okolicy jest klinika?", "klinika", "Czy w okolicy jest klinika? Gdzie najbliższa?"),
       ("Czy w okolicy jest dentysta?", "dentysta", "Czy w okolicy jest dentysta? Gdzie najbliższy?"),
       ("Czy w okolicy jest supermarket?", "supermarket", "Czy w okolicy jest supermarket? Gdzie najbliższy?"),
       ("Czy w okolicy jest poczta?", "poczta", "Czy w okolicy jest poczta? Gdzie najbliższa?"),
       ("Czy w okolicy jest park?", "park", "Czy w okolicy jest park? Gdzie najbliższy?"),
       ("Czy w okolicy jest siłownia?", "siłownia", "Czy w okolicy jest siłownia? Gdzie najbliższa?"),
       ("Czy w okolicy jest salon masażu?", "salon masażu", "Czy w okolicy jest salon masażu? Gdzie najbliższy?"),
       ("Czy w okolicy jest centrum handlowe?", "centrum handlowe", "Czy w okolicy jest centrum handlowe? Gdzie najbliższe?"),
       ("Czy w okolicy jest dworzec autobusowy?", "dworzec autobusowy", "Czy w okolicy jest dworzec autobusowy? Gdzie najbliższy?"),
       ("Czy w okolicy jest przechowalnia bagażu?", "przechowalnia bagażu", "Czy w okolicy jest przechowalnia bagażu? Gdzie najbliższa?"),
       ("Czy w okolicy jest bank?", "bank", "Czy w okolicy jest bank? Gdzie najbliższy?"),
       ("Czy w okolicy jest targ?", "targ", "Czy w okolicy jest targ? Gdzie najbliższy?"),
       ("Czy w okolicy jest bazar nocny?", "bazar nocny", "Czy w okolicy jest bazar nocny? Gdzie najbliższy?"),
       ("Czy w okolicy jest świątynia?", "świątynia", "Czy w okolicy jest świątynia? Gdzie najbliższa?"),
       ("Czy w okolicy jest toaleta?", "toaleta", "Czy w okolicy jest toaleta? Gdzie najbliższa?"),
       ("Czy w okolicy jest przystanek autobusowy?", "przystanek autobusowy", "Czy w okolicy jest przystanek autobusowy? Gdzie najbliższy?"),
     ]),

# =====================================================================
# … na khrap, mai chai … — sprostowanie przymiotnikowe
# =====================================================================
dict(key="MAICHAIADJ", ty="sentence", cat="Cechy i opinie", sub="Sprostowania", reg="n",
     ph="man mâi châi {ph} ná khráp", th="มันไม่ใช่{th}นะครับ",
     lit="mâi châi … = to nie jest …",
     note="„mâi châi” zaprzecza tożsamości rzeczy, a samo „mâi” zaprzecza cesze. „mâi phaeng” = nie jest drogie; „mâi châi phaeng” = kwestia nie polega na cenie.",
     ex_ph="man mâi châi {ph} ná khráp pan-hǎa yùu thîi ùen", ex_th="มันไม่ใช่{th}นะครับ ปัญหาอยู่ที่อื่น",
     items=[
       ("Nie chodzi o to, że jest drogo.", "drogi", "Nie chodzi o cenę, problem leży gdzie indziej."),
       ("Nie chodzi o to, że jest daleko.", "daleki", "Nie chodzi o odległość, problem leży gdzie indziej."),
       ("Nie chodzi o to, że jest trudno.", "trudny", "Nie chodzi o trudność, problem leży gdzie indziej."),
       ("Nie chodzi o to, że jest wolno.", "wolny (powolny)", "Nie chodzi o tempo, problem leży gdzie indziej."),
       ("Nie chodzi o to, że jest brudno.", "brudny", "Nie chodzi o czystość, problem leży gdzie indziej."),
       ("Nie chodzi o to, że jest głośno.", "głośny", "Nie chodzi o hałas, problem leży gdzie indziej."),
       ("Nie chodzi o to, że jest małe.", "mały", "Nie chodzi o rozmiar, problem leży gdzie indziej."),
       ("Nie chodzi o to, że jest stare.", "stary", "Nie chodzi o wiek, problem leży gdzie indziej."),
       ("Nie chodzi o to, że jest niebezpiecznie.", "niebezpieczny", "Nie chodzi o bezpieczeństwo, problem leży gdzie indziej."),
       ("Nie chodzi o to, że jest nudno.", "nudny", "Nie chodzi o nudę, problem leży gdzie indziej."),
       ("Nie chodzi o to, że jest ostre.", "ostry (pikantny)", "Nie chodzi o ostrość, problem leży gdzie indziej."),
       ("Nie chodzi o to, że jest ciężkie.", "ciężki", "Nie chodzi o ciężar, problem leży gdzie indziej."),
     ]),
]
