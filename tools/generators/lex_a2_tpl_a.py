# -*- coding: utf-8 -*-
"""Wzorce zdaniowe etapu 3 (A2) — czesc A: konstrukcje czasownikowe.

Kazdy wzorzec ma ZAMKNIETA biala liste hasel bazowych. Nie ma tu iloczynu
kartezjanskiego: pozycja trafia na liste tylko wtedy, gdy polskie zdanie brzmi
naturalnie. Polska strona rekordu i przykladu jest pisana recznie.

Pozycja: (polskie haslo rekordu, polskie haslo bazowe, polski przyklad)
Haslo bazowe musi istniec w bazie (Survival, A1 lub rdzen A2) — stage3.py
sprawdza to i przerywa prace przy literowce.

Konstrukcje sa dobrane tak, zeby NIE powielaly wzorcow poziomu A1
(„Chce: …", „Musze: …", „Juz: …", „Jeszcze nie: …", „Lubie: …").
"""

TPL_A = [

# =====================================================================
# khoei — doswiadczenie: „juz kiedys"
# =====================================================================
dict(key="KHOEI", ty="sentence", cat="Gramatyka użytkowa", sub="Przeszłość", reg="n",
     ph="phǒm khoei {ph} láew khráp", th="ผมเคย{th}แล้วครับ",
     lit="khoei = mieć coś już za sobą",
     note="„khoei” opisuje doświadczenie, nie moment. Nie tłumacz go jako czasu przeszłego.",
     ex_ph="khoei {ph} mǎi khráp", ex_th="เคย{th}ไหมครับ",
     items=[
       ("Już kiedyś to jadłem.", "jeść", "Jadłeś to kiedyś?"),
       ("Już kiedyś to piłem.", "pić", "Piłeś to kiedyś?"),
       ("Już kiedyś tu spałem.", "spać", "Spałeś tu kiedyś?"),
       ("Już kiedyś to czytałem.", "czytać", "Czytałeś to kiedyś?"),
       ("Już kiedyś tu pracowałem.", "pracować", "Pracowałeś tu kiedyś?"),
       ("Już kiedyś tak gotowałem.", "gotować", "Gotowałeś tak kiedyś?"),
       ("Już kiedyś to kupowałem.", "kupować", "Kupowałeś to kiedyś?"),
       ("Już kiedyś tu pływałem.", "pływać", "Pływałeś tu kiedyś?"),
       ("Już kiedyś biegałem rano.", "biegać", "Biegałeś kiedyś rano?"),
       ("Już kiedyś tańczyłem.", "tańczyć", "Tańczyłeś kiedyś?"),
       ("Już kiedyś śpiewałem publicznie.", "śpiewać", "Śpiewałeś kiedyś publicznie?"),
       ("Już kiedyś prowadziłem tutaj samochód.", "prowadzić samochód", "Prowadziłeś tu kiedyś?"),
       ("Już kiedyś wynajmowałem skuter.", "wynajmować", "Wynajmowałeś kiedyś skuter?"),
       ("Już kiedyś rezerwowałem przez internet.", "rezerwować", "Rezerwowałeś kiedyś sam?"),
       ("Już kiedyś zamawiałem po tajsku.", "zamawiać", "Zamawiałeś kiedyś po tajsku?"),
       ("Już kiedyś zwiedzałem to miasto.", "zwiedzać", "Zwiedzałeś to kiedyś?"),
       ("Już kiedyś uczyłem się tajskiego.", "uczyć się", "Uczyłeś się kiedyś tajskiego?"),
       ("Już kiedyś tu byłem i pytałem.", "pytać", "Pytałeś ich kiedyś?"),
       ("Już kiedyś tam mieszkałem i płaciłem czynsz.", "płacić", "Płaciłeś kiedyś sam?"),
       ("Już kiedyś tak się przesiadałem.", "przesiadać się", "Przesiadałeś się tu kiedyś?"),
       ("Już kiedyś robiłem tu zdjęcia.", "robić zdjęcia", "Robiłeś tu kiedyś zdjęcia?"),
       ("Już kiedyś próbowałem tego smaku.", "próbować (smakować)", "Próbowałeś tego kiedyś?"),
       ("Już kiedyś to przymierzałem.", "przymierzać / próbować", "Przymierzałeś to kiedyś?"),
       ("Już kiedyś wypełniałem taki formularz.", "wypełnić formularz", "Wypełniałeś kiedyś taki formularz?"),
       ("Już kiedyś tu jechałem.", "iść / jechać", "Jechałeś tędy kiedyś?"),
     ]),

# =====================================================================
# mai khoei — „nigdy jeszcze"
# =====================================================================
dict(key="MAIKHOEI", ty="sentence", cat="Gramatyka użytkowa", sub="Przeszłość", reg="n",
     ph="phǒm mâi khoei {ph} loei khráp", th="ผมไม่เคย{th}เลยครับ",
     lit="mâi khoei = nigdy dotąd",
     note="„loei” na końcu wzmacnia: ani razu w życiu.",
     ex_ph="mâi khoei {ph} jing jing rǔe khráp", ex_th="ไม่เคย{th}จริงๆ หรือครับ",
     items=[
       ("Nigdy tego nie jadłem.", "jeść", "Naprawdę nigdy tego nie jadłeś?"),
       ("Nigdy tego nie piłem.", "pić", "Naprawdę nigdy tego nie piłeś?"),
       ("Nigdy tego nie czytałem.", "czytać", "Naprawdę nigdy tego nie czytałeś?"),
       ("Nigdy tu nie pracowałem.", "pracować", "Naprawdę nigdy tu nie pracowałeś?"),
       ("Nigdy sam nie gotowałem.", "gotować", "Naprawdę nigdy nie gotowałeś?"),
       ("Nigdy nie pływałem w morzu.", "pływać", "Naprawdę nigdy nie pływałeś?"),
       ("Nigdy nie tańczyłem.", "tańczyć", "Naprawdę nigdy nie tańczyłeś?"),
       ("Nigdy nie śpiewałem przy ludziach.", "śpiewać", "Naprawdę nigdy nie śpiewałeś?"),
       ("Nigdy tu nie prowadziłem samochodu.", "prowadzić samochód", "Naprawdę nigdy tu nie prowadziłeś?"),
       ("Nigdy nie wynajmowałem skutera.", "wynajmować", "Naprawdę nigdy nie wynajmowałeś?"),
       ("Nigdy nie rezerwowałem hotelu sam.", "rezerwować", "Naprawdę nigdy nie rezerwowałeś?"),
       ("Nigdy nie zamawiałem po tajsku.", "zamawiać", "Naprawdę nigdy nie zamawiałeś po tajsku?"),
       ("Nigdy nie zwiedzałem tej okolicy.", "zwiedzać", "Naprawdę nigdy tu nie byłeś?"),
       ("Nigdy nie uczyłem się chińskiego.", "uczyć się", "Naprawdę nigdy się nie uczyłeś?"),
       ("Nigdy tak nie podróżowałem.", "iść / jechać", "Naprawdę nigdy tak nie jechałeś?"),
       ("Nigdy nie wypełniałem takiego formularza.", "wypełnić formularz", "Naprawdę nigdy tego nie wypełniałeś?"),
       ("Nigdy nie robiłem takich zdjęć.", "robić zdjęcia", "Naprawdę nigdy takich nie robiłeś?"),
       ("Nigdy tego nie próbowałem.", "próbować (smakować)", "Naprawdę nigdy nie próbowałeś?"),
       ("Nigdy nie prałem ręcznie.", "prać", "Naprawdę nigdy nie prałeś ręcznie?"),
       ("Nigdy się tak nie przesiadałem.", "przesiadać się", "Naprawdę nigdy się tak nie przesiadałeś?"),
     ]),

# =====================================================================
# kamlang … yuu — czynnosc w toku
# =====================================================================
dict(key="KAMLANG", ty="sentence", cat="Gramatyka użytkowa", sub="Teraźniejszość", reg="n",
     ph="phǒm kamlang {ph} yùu khráp", th="ผมกำลัง{th}อยู่ครับ",
     lit="kamlang … yùu = właśnie w trakcie",
     note="Klamra „kamlang … yùu” otacza czasownik. Sam „kamlang” też wystarczy.",
     ex_ph="kamlang {ph} yùu rǔe khráp", ex_th="กำลัง{th}อยู่หรือครับ",
     items=[
       ("Właśnie jem.", "jeść", "Właśnie jesz?"),
       ("Właśnie piję.", "pić", "Właśnie pijesz?"),
       ("Właśnie czytam.", "czytać", "Właśnie czytasz?"),
       ("Właśnie piszę.", "pisać", "Właśnie piszesz?"),
       ("Właśnie czekam.", "czekać", "Właśnie czekasz?"),
       ("Właśnie pracuję.", "pracować", "Właśnie pracujesz?"),
       ("Właśnie odpoczywam.", "odpoczywać", "Właśnie odpoczywasz?"),
       ("Właśnie gotuję.", "gotować", "Właśnie gotujesz?"),
       ("Właśnie szukam.", "szukać", "Właśnie szukasz?"),
       ("Właśnie słucham.", "słuchać", "Właśnie słuchasz?"),
       ("Właśnie oglądam.", "oglądać", "Właśnie oglądasz?"),
       ("Właśnie się uczę.", "uczyć się", "Właśnie się uczysz?"),
       ("Właśnie prowadzę samochód.", "prowadzić samochód", "Właśnie prowadzisz?"),
       ("Właśnie się pakuję.", "pakować się", "Właśnie się pakujesz?"),
       ("Właśnie piorę.", "prać", "Właśnie pierzesz?"),
       ("Właśnie wracam.", "wracać", "Właśnie wracasz?"),
       ("Właśnie wychodzę.", "wychodzić", "Właśnie wychodzisz?"),
       ("Właśnie zwiedzam.", "zwiedzać", "Właśnie zwiedzasz?"),
       ("Właśnie rozmawiam.", "rozmawiać", "Właśnie rozmawiasz?"),
       ("Właśnie wybieram.", "wybierać", "Właśnie wybierasz?"),
       ("Właśnie płacę.", "płacić", "Właśnie płacisz?"),
       ("Właśnie zamawiam.", "zamawiać", "Właśnie zamawiasz?"),
       ("Właśnie się myję.", "myć", "Właśnie się myjesz?"),
       ("Właśnie robię zdjęcia.", "robić zdjęcia", "Właśnie robisz zdjęcia?"),
       ("Właśnie pływam.", "pływać", "Właśnie pływasz?"),
     ]),

# =====================================================================
# dǐao … jà — „zaraz to zrobie"
# =====================================================================
dict(key="DIAOJA", ty="sentence", cat="Gramatyka użytkowa", sub="Plany", reg="n",
     ph="dǐao phǒm jà {ph} khráp", th="เดี๋ยวผมจะ{th}ครับ",
     lit="dǐao = za chwilę",
     note="„dǐao” obiecuje działanie w najbliższych minutach, nie jutro.",
     ex_ph="dǐao {ph} ná khráp", ex_th="เดี๋ยว{th}นะครับ",
     items=[
       ("Zaraz zapłacę.", "płacić", "Zaraz zapłacę, dobrze?"),
       ("Zaraz zadzwonię.", "dzwonić", "Zaraz zadzwonię, dobrze?"),
       ("Zaraz zamówię.", "zamawiać", "Zaraz zamówię, dobrze?"),
       ("Zaraz to otworzę.", "otwierać", "Zaraz otworzę, dobrze?"),
       ("Zaraz to zamknę.", "zamykać", "Zaraz zamknę, dobrze?"),
       ("Zaraz poszukam.", "szukać", "Zaraz poszukam, dobrze?"),
       ("Zaraz zapytam.", "pytać", "Zaraz zapytam, dobrze?"),
       ("Zaraz odpowiem.", "odpowiadać", "Zaraz odpowiem, dobrze?"),
       ("Zaraz wracam.", "wracać", "Zaraz wracam, dobrze?"),
       ("Zaraz wychodzę.", "wychodzić", "Zaraz wychodzę, dobrze?"),
       ("Zaraz się spakuję.", "pakować się", "Zaraz się spakuję, dobrze?"),
       ("Zaraz to pokażę.", "pokazać", "Zaraz pokażę, dobrze?"),
       ("Zaraz podpiszę.", "podpisać", "Zaraz podpiszę, dobrze?"),
       ("Zaraz zarezerwuję.", "rezerwować", "Zaraz zarezerwuję, dobrze?"),
       ("Zaraz to zmienię.", "zmieniać", "Zaraz zmienię, dobrze?"),
       ("Zaraz wybiorę.", "wybierać", "Zaraz wybiorę, dobrze?"),
       ("Zaraz to ugotuję.", "gotować", "Zaraz ugotuję, dobrze?"),
       ("Zaraz zrobię zdjęcie.", "robić zdjęcia", "Zaraz zrobię zdjęcie, dobrze?"),
       ("Zaraz wsiadam.", "wsiadać", "Zaraz wsiadam, dobrze?"),
       ("Zaraz wysiadam.", "wysiadać", "Zaraz wysiadam, dobrze?"),
       ("Zaraz zacznę.", "zaczynać", "Zaraz zacznę, dobrze?"),
       ("Zaraz to wyślę.", "wysyłać", "Zaraz wyślę, dobrze?"),
     ]),

# =====================================================================
# phôoeng — „dopiero co"
# =====================================================================
dict(key="PHOENG", ty="sentence", cat="Gramatyka użytkowa", sub="Przeszłość", reg="n",
     ph="phǒm phôoeng {ph} khráp", th="ผมเพิ่ง{th}ครับ",
     lit="phôoeng = dopiero co, przed chwilą",
     note="Dotyczy tylko świeżej przeszłości — kilku minut lub godzin.",
     ex_ph="phôoeng {ph} rǔe khráp", ex_th="เพิ่ง{th}หรือครับ",
     items=[
       ("Dopiero co zjadłem.", "jeść", "Dopiero zjadłeś?"),
       ("Dopiero co wypiłem.", "pić", "Dopiero wypiłeś?"),
       ("Dopiero co wstałem.", "wstawać", "Dopiero wstałeś?"),
       ("Dopiero co się obudziłem.", "budzić się", "Dopiero się obudziłeś?"),
       ("Dopiero co zapłaciłem.", "płacić", "Dopiero zapłaciłeś?"),
       ("Dopiero co zadzwoniłem.", "dzwonić", "Dopiero zadzwoniłeś?"),
       ("Dopiero co przyjechałem.", "przyjść / przyjechać", "Dopiero przyjechałeś?"),
       ("Dopiero co wróciłem.", "wracać", "Dopiero wróciłeś?"),
       ("Dopiero co wyszedłem.", "wychodzić", "Dopiero wyszedłeś?"),
       ("Dopiero co zamówiłem.", "zamawiać", "Dopiero zamówiłeś?"),
       ("Dopiero co kupiłem.", "kupować", "Dopiero kupiłeś?"),
       ("Dopiero co skończyłem pracę.", "pracować", "Dopiero skończyłeś pracę?"),
       ("Dopiero co się spakowałem.", "pakować się", "Dopiero się spakowałeś?"),
       ("Dopiero co wysiadłem.", "wysiadać", "Dopiero wysiadłeś?"),
       ("Dopiero co się przesiadłem.", "przesiadać się", "Dopiero się przesiadłeś?"),
       ("Dopiero co to znalazłem.", "znaleźć", "Dopiero znalazłeś?"),
       ("Dopiero co podpisałem.", "podpisać", "Dopiero podpisałeś?"),
       ("Dopiero co się umyłem.", "myć", "Dopiero się umyłeś?"),
       ("Dopiero co zacząłem.", "zaczynać", "Dopiero zacząłeś?"),
       ("Dopiero co wysłałem.", "wysyłać", "Dopiero wysłałeś?"),
     ]),

# =====================================================================
# mai yaak — „nie chce"
# =====================================================================
dict(key="MAIYAAK", ty="sentence", cat="Gramatyka użytkowa", sub="Chęci", reg="n",
     ph="phǒm mâi yàak {ph} khráp", th="ผมไม่อยาก{th}ครับ",
     lit="mâi yàak = nie chcieć",
     note="Łagodniejsze niż odmowa wprost — mówi o chęci, nie o zakazie.",
     ex_ph="mâi yàak {ph} rǔe khráp", ex_th="ไม่อยาก{th}หรือครับ",
     items=[
       ("Nie chcę teraz jeść.", "jeść", "Nie chcesz jeść?"),
       ("Nie chcę teraz pić.", "pić", "Nie chcesz pić?"),
       ("Nie chcę jeszcze spać.", "spać", "Nie chcesz spać?"),
       ("Nie chcę dziś pracować.", "pracować", "Nie chcesz dziś pracować?"),
       ("Nie chcę tego kupować.", "kupować", "Nie chcesz tego kupić?"),
       ("Nie chcę czekać.", "czekać", "Nie chcesz czekać?"),
       ("Nie chcę teraz rozmawiać.", "rozmawiać", "Nie chcesz rozmawiać?"),
       ("Nie chcę o tym mówić.", "mówić", "Nie chcesz o tym mówić?"),
       ("Nie chcę tego oglądać.", "oglądać", "Nie chcesz tego oglądać?"),
       ("Nie chcę dziś gotować.", "gotować", "Nie chcesz dziś gotować?"),
       ("Nie chcę wychodzić.", "wychodzić", "Nie chcesz wychodzić?"),
       ("Nie chcę jeszcze wracać.", "wracać", "Nie chcesz jeszcze wracać?"),
       ("Nie chcę zmieniać planów.", "zmieniać", "Nie chcesz zmieniać planów?"),
       ("Nie chcę tego przymierzać.", "przymierzać / próbować", "Nie chcesz przymierzyć?"),
       ("Nie chcę tego próbować.", "próbować (smakować)", "Nie chcesz spróbować?"),
       ("Nie chcę teraz płacić.", "płacić", "Nie chcesz teraz płacić?"),
       ("Nie chcę nikomu przeszkadzać ani pytać.", "pytać", "Nie chcesz zapytać?"),
       ("Nie chcę tam siedzieć.", "siedzieć", "Nie chcesz tam siedzieć?"),
       ("Nie chcę dziś biegać.", "biegać", "Nie chcesz dziś biegać?"),
       ("Nie chcę tańczyć.", "tańczyć", "Nie chcesz zatańczyć?"),
     ]),

# =====================================================================
# mai tawng … kaw dai — „nie trzeba"
# =====================================================================
dict(key="MAITAWNG", ty="sentence", cat="Gramatyka użytkowa", sub="Konieczność", reg="n",
     ph="mâi tâwng {ph} kâw dâai khráp", th="ไม่ต้อง{th}ก็ได้ครับ",
     lit="mâi tâwng … kâw dâai = spokojnie można tego nie robić",
     note="Bardzo uprzejme zwolnienie z obowiązku — częste w obsłudze klienta.",
     ex_ph="mâi tâwng {ph} ná khráp", ex_th="ไม่ต้อง{th}นะครับ",
     items=[
       ("Nie trzeba czekać.", "czekać", "Nie czekaj na mnie."),
       ("Nie trzeba dzwonić.", "dzwonić", "Nie dzwoń, proszę."),
       ("Nie trzeba płacić.", "płacić", "Nie płać, proszę."),
       ("Nie trzeba rezerwować.", "rezerwować", "Nie rezerwuj, proszę."),
       ("Nie trzeba gotować.", "gotować", "Nie gotuj, proszę."),
       ("Nie trzeba tego zmieniać.", "zmieniać", "Nie zmieniaj tego."),
       ("Nie trzeba pytać.", "pytać", "Nie pytaj, proszę."),
       ("Nie trzeba się pakować.", "pakować się", "Nie pakuj się jeszcze."),
       ("Nie trzeba wracać.", "wracać", "Nie wracaj, proszę."),
       ("Nie trzeba wychodzić.", "wychodzić", "Nie wychodź, proszę."),
       ("Nie trzeba prać.", "prać", "Nie pierz tego."),
       ("Nie trzeba podpisywać.", "podpisać", "Nie podpisuj, proszę."),
       ("Nie trzeba tego pokazywać.", "pokazać", "Nie pokazuj, proszę."),
       ("Nie trzeba wypełniać formularza.", "wypełnić formularz", "Nie wypełniaj formularza."),
       ("Nie trzeba się przesiadać.", "przesiadać się", "Nie przesiadaj się."),
       ("Nie trzeba szukać.", "szukać", "Nie szukaj, proszę."),
       ("Nie trzeba zamawiać.", "zamawiać", "Nie zamawiaj, proszę."),
       ("Nie trzeba się spieszyć i biec.", "biegać", "Nie biegnij, proszę."),
     ]),

# =====================================================================
# tawng … mai — „czy trzeba?"
# =====================================================================
dict(key="TAWNGMAI", ty="question", cat="Pytania", sub="Konieczność", reg="n",
     ph="tâwng {ph} mǎi khráp", th="ต้อง{th}ไหมครับ",
     lit="tâwng … mǎi = czy trzeba…?",
     note="Pytanie o obowiązek. Odpowiedź twierdząca to „tâwng”, przecząca „mâi tâwng”.",
     ex_ph="mâi tâwng {ph} khráp", ex_th="ไม่ต้อง{th}ครับ",
     items=[
       ("Czy trzeba rezerwować?", "rezerwować", "Nie trzeba rezerwować."),
       ("Czy trzeba czekać?", "czekać", "Nie trzeba czekać."),
       ("Czy trzeba płacić z góry?", "płacić", "Nie trzeba płacić."),
       ("Czy trzeba dzwonić?", "dzwonić", "Nie trzeba dzwonić."),
       ("Czy trzeba się przesiadać?", "przesiadać się", "Nie trzeba się przesiadać."),
       ("Czy trzeba podpisać?", "podpisać", "Nie trzeba podpisywać."),
       ("Czy trzeba wypełnić formularz?", "wypełnić formularz", "Nie trzeba wypełniać."),
       ("Czy trzeba pytać?", "pytać", "Nie trzeba pytać."),
       ("Czy trzeba to pokazać?", "pokazać", "Nie trzeba pokazywać."),
       ("Czy trzeba się pakować teraz?", "pakować się", "Nie trzeba się pakować."),
       ("Czy trzeba to zmienić?", "zmieniać", "Nie trzeba zmieniać."),
       ("Czy trzeba wsiadać z przodu?", "wsiadać", "Nie trzeba wsiadać z przodu."),
       ("Czy trzeba zamawiać wcześniej?", "zamawiać", "Nie trzeba zamawiać wcześniej."),
       ("Czy trzeba tu wysiadać?", "wysiadać", "Nie trzeba tu wysiadać."),
       ("Czy trzeba to prać osobno?", "prać", "Nie trzeba prać osobno."),
       ("Czy trzeba tam wchodzić?", "wchodzić", "Nie trzeba tam wchodzić."),
     ]),

# =====================================================================
# luem — „zapomnialem"
# =====================================================================
dict(key="LUEM", ty="sentence", cat="Awarie i pomoc", sub="Problemy", reg="n",
     ph="phǒm luem {ph} khráp", th="ผมลืม{th}ครับ",
     lit="luem = zapomnieć",
     note="Po „luem” idzie czasownik bez żadnej partykuły.",
     ex_ph="luem {ph} rǔe plào khráp", ex_th="ลืม{th}หรือเปล่าครับ",
     items=[
       ("Zapomniałem zapłacić.", "płacić", "Zapomniałeś zapłacić?"),
       ("Zapomniałem zadzwonić.", "dzwonić", "Zapomniałeś zadzwonić?"),
       ("Zapomniałem zamknąć.", "zamykać", "Zapomniałeś zamknąć?"),
       ("Zapomniałem zarezerwować.", "rezerwować", "Zapomniałeś zarezerwować?"),
       ("Zapomniałem zamówić.", "zamawiać", "Zapomniałeś zamówić?"),
       ("Zapomniałem zapytać.", "pytać", "Zapomniałeś zapytać?"),
       ("Zapomniałem odpowiedzieć.", "odpowiadać", "Zapomniałeś odpowiedzieć?"),
       ("Zapomniałem podpisać.", "podpisać", "Zapomniałeś podpisać?"),
       ("Zapomniałem się spakować.", "pakować się", "Zapomniałeś się spakować?"),
       ("Zapomniałem wysłać.", "wysyłać", "Zapomniałeś wysłać?"),
       ("Zapomniałem to kupić.", "kupować", "Zapomniałeś kupić?"),
       ("Zapomniałem wypełnić formularz.", "wypełnić formularz", "Zapomniałeś wypełnić formularz?"),
       ("Zapomniałem to wziąć.", "brać", "Zapomniałeś wziąć?"),
       ("Zapomniałem to pokazać.", "pokazać", "Zapomniałeś pokazać?"),
       ("Zapomniałem prać.", "prać", "Zapomniałeś zrobić pranie?"),
       ("Zapomniałem anulować.", "anulować", "Zapomniałeś anulować?"),
     ]),

# =====================================================================
# chuai … hai noi — uprzejma prosba
# =====================================================================
dict(key="CHUAIHAI", ty="phrase", cat="Awarie i pomoc", sub="Prośby", reg="n",
     ph="chûai {ph} hâi nòi khráp", th="ช่วย{th}ให้หน่อยครับ",
     lit="chûai … hâi nòi = zrób to dla mnie, proszę",
     note="„hâi” dodaje „na moją korzyść”, „nòi” zmiękcza całość. Najuprzejmiejsza prośba w codziennym tajskim.",
     ex_ph="chûai {ph} hâi dûai ná khráp", ex_th="ช่วย{th}ให้ด้วยนะครับ",
     items=[
       ("Proszę mi to otworzyć.", "otwierać", "Proszę, otwórz mi to."),
       ("Proszę mi to zamknąć.", "zamykać", "Proszę, zamknij mi to."),
       ("Proszę do niego zadzwonić.", "dzwonić", "Proszę, zadzwoń dla mnie."),
       ("Proszę mi to zamówić.", "zamawiać", "Proszę, zamów mi to."),
       ("Proszę mi to zarezerwować.", "rezerwować", "Proszę, zarezerwuj mi to."),
       ("Proszę mi to pokazać.", "pokazać", "Proszę, pokaż mi to."),
       ("Proszę mi to policzyć.", "policzyć rachunek", "Proszę, policz mi to."),
       ("Proszę mi to zmienić.", "zmieniać", "Proszę, zmień mi to."),
       ("Proszę tego poszukać.", "szukać", "Proszę, poszukaj tego."),
       ("Proszę o to zapytać.", "pytać", "Proszę, zapytaj o to."),
       ("Proszę mi to wysłać.", "wysyłać", "Proszę, wyślij mi to."),
       ("Proszę mi to wybrać.", "wybierać", "Proszę, wybierz mi coś."),
       ("Proszę mi to spakować.", "pakować się", "Proszę, spakuj mi to."),
       ("Proszę mi to zapisać.", "pisać", "Proszę, zapisz mi to."),
       ("Proszę to anulować.", "anulować", "Proszę, anuluj to."),
       ("Proszę mi to przetłumaczyć na piśmie.", "czytać", "Proszę, przeczytaj mi to."),
       ("Proszę mi to wyprać.", "prać", "Proszę, wypierz mi to."),
       ("Proszę mi to podpisać.", "podpisać", "Proszę, podpisz mi to."),
     ]),

# =====================================================================
# chawp … maak-kwaa — „wole"
# =====================================================================
dict(key="CHAWPKWAA", ty="sentence", cat="Cechy i opinie", sub="Preferencje", reg="n",
     ph="phǒm châwp {ph} mâak-kwàa khráp", th="ผมชอบ{th}มากกว่าครับ",
     lit="châwp … mâak-kwàa = wolę coś od czegoś innego",
     note="Bez drugiego członu zdanie znaczy po prostu „wolę to”.",
     ex_ph="châwp {ph} mâak-kwàa rǔe khráp", ex_th="ชอบ{th}มากกว่าหรือครับ",
     items=[
       ("Wolę gotować sam.", "gotować", "Wolisz gotować sam?"),
       ("Wolę czytać.", "czytać", "Wolisz czytać?"),
       ("Wolę słuchać.", "słuchać", "Wolisz słuchać?"),
       ("Wolę oglądać.", "oglądać", "Wolisz oglądać?"),
       ("Wolę pływać.", "pływać", "Wolisz pływać?"),
       ("Wolę biegać.", "biegać", "Wolisz biegać?"),
       ("Wolę iść pieszo.", "iść pieszo", "Wolisz iść pieszo?"),
       ("Wolę odpoczywać.", "odpoczywać", "Wolisz odpoczywać?"),
       ("Wolę zwiedzać.", "zwiedzać", "Wolisz zwiedzać?"),
       ("Wolę robić zdjęcia.", "robić zdjęcia", "Wolisz robić zdjęcia?"),
       ("Wolę rozmawiać osobiście.", "rozmawiać", "Wolisz rozmawiać osobiście?"),
       ("Wolę uczyć się sam.", "uczyć się", "Wolisz uczyć się sam?"),
       ("Wolę zamawiać sam.", "zamawiać", "Wolisz zamawiać sam?"),
       ("Wolę płacić od razu.", "płacić", "Wolisz zapłacić od razu?"),
       ("Wolę rezerwować wcześniej.", "rezerwować", "Wolisz rezerwować wcześniej?"),
       ("Wolę tańczyć.", "tańczyć", "Wolisz tańczyć?"),
       ("Wolę śpiewać.", "śpiewać", "Wolisz śpiewać?"),
       ("Wolę prowadzić samochód.", "prowadzić samochód", "Wolisz prowadzić?"),
     ]),

# =====================================================================
# mai chawp — „nie lubie"
# =====================================================================
dict(key="MAICHAWP", ty="sentence", cat="Cechy i opinie", sub="Preferencje", reg="i",
     ph="phǒm mâi châwp {ph} khráp", th="ผมไม่ชอบ{th}ครับ",
     lit="mâi châwp = nie lubić",
     note="Neutralne stwierdzenie gustu, nie zarzut wobec rozmówcy.",
     ex_ph="mâi châwp {ph} rǔe khráp", ex_th="ไม่ชอบ{th}หรือครับ",
     items=[
       ("Nie lubię czekać.", "czekać", "Nie lubisz czekać?"),
       ("Nie lubię gotować.", "gotować", "Nie lubisz gotować?"),
       ("Nie lubię prać.", "prać", "Nie lubisz prać?"),
       ("Nie lubię biegać.", "biegać", "Nie lubisz biegać?"),
       ("Nie lubię tańczyć.", "tańczyć", "Nie lubisz tańczyć?"),
       ("Nie lubię śpiewać.", "śpiewać", "Nie lubisz śpiewać?"),
       ("Nie lubię prowadzić samochodu.", "prowadzić samochód", "Nie lubisz prowadzić?"),
       ("Nie lubię wcześnie wstawać.", "wstawać", "Nie lubisz wcześnie wstawać?"),
       ("Nie lubię się pakować.", "pakować się", "Nie lubisz się pakować?"),
       ("Nie lubię się przesiadać.", "przesiadać się", "Nie lubisz się przesiadać?"),
       ("Nie lubię się targować.", "pytać", "Nie lubisz pytać o cenę?"),
       ("Nie lubię pływać.", "pływać", "Nie lubisz pływać?"),
       ("Nie lubię oglądać wiadomości.", "oglądać", "Nie lubisz oglądać?"),
       ("Nie lubię rozmawiać przez telefon.", "rozmawiać", "Nie lubisz rozmawiać przez telefon?"),
       ("Nie lubię zwiedzać w tłumie.", "zwiedzać", "Nie lubisz zwiedzać?"),
       ("Nie lubię robić sobie zdjęć.", "robić zdjęcia", "Nie lubisz zdjęć?"),
     ]),

# =====================================================================
# … hai noi dai mai — prosba pytajaca
# =====================================================================
dict(key="DAIMAIQ", ty="question", cat="Pytania", sub="Prośby", reg="f",
     ph="phǒm khǎw {ph} dâai mǎi khráp", th="ผมขอ{th}ได้ไหมครับ",
     lit="khǎw … dâai mǎi = czy mogę prosić o…",
     note="„khǎw” prosi o pozwolenie dla siebie; „chûai” prosi o przysługę.",
     ex_ph="{ph} dâai loei khráp", ex_th="{th}ได้เลยครับ",
     items=[
       ("Czy mogę zapłacić teraz?", "płacić", "Proszę bardzo, można płacić."),
       ("Czy mogę zamówić?", "zamawiać", "Proszę bardzo, można zamawiać."),
       ("Czy mogę to zmienić?", "zmieniać", "Proszę bardzo, można zmienić."),
       ("Czy mogę tu usiąść?", "siedzieć", "Proszę bardzo, można usiąść."),
       ("Czy mogę wejść?", "wchodzić", "Proszę bardzo, można wejść."),
       ("Czy mogę wyjść?", "wychodzić", "Proszę bardzo, można wyjść."),
       ("Czy mogę tu poczekać?", "czekać", "Proszę bardzo, można poczekać."),
       ("Czy mogę zadzwonić?", "dzwonić", "Proszę bardzo, można zadzwonić."),
       ("Czy mogę zapytać?", "pytać", "Proszę bardzo, można pytać."),
       ("Czy mogę to przymierzyć?", "przymierzać / próbować", "Proszę bardzo, można przymierzyć."),
       ("Czy mogę spróbować?", "próbować (smakować)", "Proszę bardzo, można spróbować."),
       ("Czy mogę zarezerwować?", "rezerwować", "Proszę bardzo, można zarezerwować."),
       ("Czy mogę tu zaparkować i się zatrzymać?", "zatrzymać się", "Proszę bardzo, można się zatrzymać."),
       ("Czy mogę pożyczyć?", "pożyczyć", "Proszę bardzo, można pożyczyć."),
       ("Czy mogę to sfotografować?", "robić zdjęcia", "Proszę bardzo, można fotografować."),
       ("Czy mogę tu odpocząć?", "odpoczywać", "Proszę bardzo, można odpocząć."),
       ("Czy mogę to wypożyczyć?", "wynajmować", "Proszę bardzo, można wynająć."),
       ("Czy mogę anulować?", "anulować", "Proszę bardzo, można anulować."),
     ]),

# =====================================================================
# yang mai dai … loei — mocne „jeszcze wcale nie"
# =====================================================================
dict(key="YANGLOEI", ty="sentence", cat="Gramatyka użytkowa", sub="Przeszłość", reg="n",
     ph="phǒm yang mâi dâi {ph} loei khráp", th="ผมยังไม่ได้{th}เลยครับ",
     lit="yang mâi dâi … loei = jeszcze w ogóle tego nie zrobiłem",
     note="Mocniejsze niż samo „yang mâi dâi”; tłumaczy opóźnienie.",
     ex_ph="yang mâi dâi {ph} loei rǔe khráp", ex_th="ยังไม่ได้{th}เลยหรือครับ",
     items=[
       ("Jeszcze w ogóle nie jadłem.", "jeść", "W ogóle jeszcze nie jadłeś?"),
       ("Jeszcze w ogóle nie spałem.", "spać", "W ogóle jeszcze nie spałeś?"),
       ("Jeszcze w ogóle nie zapłaciłem.", "płacić", "W ogóle jeszcze nie zapłaciłeś?"),
       ("Jeszcze w ogóle nie dzwoniłem.", "dzwonić", "W ogóle jeszcze nie dzwoniłeś?"),
       ("Jeszcze w ogóle się nie spakowałem.", "pakować się", "W ogóle się jeszcze nie spakowałeś?"),
       ("Jeszcze w ogóle nie zamówiłem.", "zamawiać", "W ogóle jeszcze nie zamówiłeś?"),
       ("Jeszcze w ogóle nie zarezerwowałem.", "rezerwować", "W ogóle jeszcze nie zarezerwowałeś?"),
       ("Jeszcze w ogóle nie zacząłem.", "zaczynać", "W ogóle jeszcze nie zacząłeś?"),
       ("Jeszcze w ogóle się nie uczyłem.", "uczyć się", "W ogóle jeszcze się nie uczyłeś?"),
       ("Jeszcze w ogóle nie odpoczywałem.", "odpoczywać", "W ogóle jeszcze nie odpoczywałeś?"),
       ("Jeszcze w ogóle nie prałem.", "prać", "W ogóle jeszcze nie prałeś?"),
       ("Jeszcze w ogóle tego nie widziałem.", "oglądać", "W ogóle jeszcze nie oglądałeś?"),
       ("Jeszcze w ogóle nie odpowiedziałem.", "odpowiadać", "W ogóle jeszcze nie odpowiedziałeś?"),
       ("Jeszcze w ogóle nie wysłałem.", "wysyłać", "W ogóle jeszcze nie wysłałeś?"),
       ("Jeszcze w ogóle nie podpisałem.", "podpisać", "W ogóle jeszcze nie podpisałeś?"),
       ("Jeszcze w ogóle nie szukałem.", "szukać", "W ogóle jeszcze nie szukałeś?"),
     ]),

# =====================================================================
# … dai di — „dobrze mi idzie"
# =====================================================================
dict(key="DAIDII", ty="sentence", cat="Cechy i opinie", sub="Umiejętności", reg="n",
     ph="phǒm {ph} dâai dii khráp", th="ผม{th}ได้ดีครับ",
     lit="… dâai dii = potrafię to robić dobrze",
     note="„dâai” po czasowniku oznacza umiejętność, nie pozwolenie.",
     ex_ph="{ph} dâai dii mǎi khráp", ex_th="{th}ได้ดีไหมครับ",
     items=[
       ("Dobrze gotuję.", "gotować", "Dobrze gotujesz?"),
       ("Dobrze pływam.", "pływać", "Dobrze pływasz?"),
       ("Dobrze tańczę.", "tańczyć", "Dobrze tańczysz?"),
       ("Dobrze śpiewam.", "śpiewać", "Dobrze śpiewasz?"),
       ("Dobrze prowadzę samochód.", "prowadzić samochód", "Dobrze prowadzisz?"),
       ("Dobrze piszę.", "pisać", "Dobrze piszesz?"),
       ("Dobrze czytam.", "czytać", "Dobrze czytasz?"),
       ("Dobrze mówię.", "mówić", "Dobrze mówisz?"),
       ("Dobrze się uczę.", "uczyć się", "Dobrze ci idzie nauka?"),
       ("Dobrze robię zdjęcia.", "robić zdjęcia", "Dobrze robisz zdjęcia?"),
       ("Dobrze biegam.", "biegać", "Dobrze biegasz?"),
       ("Dobrze się targuję i pytam o cenę.", "pytać", "Umiesz pytać o cenę?"),
     ]),

# =====================================================================
# kamlang jà — „wlasnie mialem"
# =====================================================================
dict(key="KAMLANGJA", ty="sentence", cat="Gramatyka użytkowa", sub="Plany", reg="n",
     ph="phǒm kamlang jà {ph} phaw dii khráp", th="ผมกำลังจะ{th}พอดีครับ",
     lit="kamlang jà … phaw dii = właśnie miałem to zrobić",
     note="Idealna odpowiedź, gdy ktoś prosi o coś, co i tak zamierzaliśmy zrobić.",
     ex_ph="kamlang jà {ph} rǔe khráp", ex_th="กำลังจะ{th}หรือครับ",
     items=[
       ("Właśnie miałem zapłacić.", "płacić", "Właśnie miałeś zapłacić?"),
       ("Właśnie miałem zadzwonić.", "dzwonić", "Właśnie miałeś zadzwonić?"),
       ("Właśnie miałem wychodzić.", "wychodzić", "Właśnie miałeś wychodzić?"),
       ("Właśnie miałem zamówić.", "zamawiać", "Właśnie miałeś zamówić?"),
       ("Właśnie miałem to kupić.", "kupować", "Właśnie miałeś to kupić?"),
       ("Właśnie miałem zacząć.", "zaczynać", "Właśnie miałeś zacząć?"),
       ("Właśnie miałem wracać.", "wracać", "Właśnie miałeś wracać?"),
       ("Właśnie miałem to wysłać.", "wysyłać", "Właśnie miałeś to wysłać?"),
       ("Właśnie miałem zapytać.", "pytać", "Właśnie miałeś zapytać?"),
       ("Właśnie miałem to otworzyć.", "otwierać", "Właśnie miałeś otworzyć?"),
       ("Właśnie miałem to zamknąć.", "zamykać", "Właśnie miałeś zamknąć?"),
       ("Właśnie miałem się pakować.", "pakować się", "Właśnie miałeś się pakować?"),
     ]),
]
