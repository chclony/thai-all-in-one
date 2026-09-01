# -*- coding: utf-8 -*-
"""Wzorce zdaniowe etapu 3 (A2) — czesc D: umiejetnosci, czestotliwosc,
jedzenie i miejsca.

Biale listy jak w pozostalych czesciach: haslo trafia do wzorca tylko wtedy,
gdy polskie zdanie brzmi naturalnie.

Pozycja: (polskie haslo rekordu, polskie haslo bazowe, polski przyklad)
"""

TPL_D = [

# =====================================================================
# … pen — umiejetnosc wyuczona
# =====================================================================
dict(key="PENSKILL", ty="sentence", cat="Cechy i opinie", sub="Umiejętności", reg="n",
     ph="phǒm {ph} pen khráp", th="ผม{th}เป็นครับ",
     lit="… pen = umieć coś, bo się tego nauczyłem",
     note="„pen” to umiejętność wyuczona, „dâai” to fizyczna możliwość. Pływać „pen”, ale dziś nie „dâai”, bo boli noga.",
     ex_ph="{ph} pen mǎi khráp", ex_th="{th}เป็นไหมครับ",
     items=[
       ("Umiem gotować.", "gotować", "Umiesz gotować?"),
       ("Umiem pływać.", "pływać", "Umiesz pływać?"),
       ("Umiem tańczyć.", "tańczyć", "Umiesz tańczyć?"),
       ("Umiem śpiewać.", "śpiewać", "Umiesz śpiewać?"),
       ("Umiem prowadzić samochód.", "prowadzić samochód", "Umiesz prowadzić?"),
       ("Umiem czytać.", "czytać", "Umiesz czytać?"),
       ("Umiem pisać.", "pisać", "Umiesz pisać?"),
       ("Umiem prać ręcznie.", "prać", "Umiesz prać ręcznie?"),
       ("Umiem robić zdjęcia.", "robić zdjęcia", "Umiesz robić zdjęcia?"),
       ("Umiem się targować i pytać o cenę.", "pytać", "Umiesz pytać o cenę?"),
       ("Umiem zamawiać po tajsku.", "zamawiać", "Umiesz zamawiać po tajsku?"),
       ("Umiem to naprawić.", "naprawiać", "Umiesz to naprawić?"),
       ("Umiem sprzątać porządnie.", "sprzątać", "Umiesz sprzątać?"),
       ("Umiem się pakować szybko.", "pakować się", "Umiesz się szybko pakować?"),
       ("Umiem wypełnić formularz.", "wypełnić formularz", "Umiesz wypełnić formularz?"),
       ("Umiem liczyć rachunek.", "policzyć rachunek", "Umiesz policzyć rachunek?"),
       ("Umiem biegać długo.", "biegać", "Umiesz długo biegać?"),
       ("Umiem grać.", "grać / bawić się", "Umiesz grać?"),
     ]),

# =====================================================================
# … mai pen — brak umiejetnosci
# =====================================================================
dict(key="MAIPEN", ty="sentence", cat="Cechy i opinie", sub="Umiejętności", reg="n",
     ph="phǒm {ph} mâi pen khráp", th="ผม{th}ไม่เป็นครับ",
     lit="… mâi pen = nie umiem tego",
     note="Uczciwe przyznanie się do braku umiejętności. Nie brzmi to jak odmowa.",
     ex_ph="{ph} mâi pen jing jing rǔe khráp", ex_th="{th}ไม่เป็นจริงๆ หรือครับ",
     items=[
       ("Nie umiem gotować.", "gotować", "Naprawdę nie umiesz gotować?"),
       ("Nie umiem pływać.", "pływać", "Naprawdę nie umiesz pływać?"),
       ("Nie umiem tańczyć.", "tańczyć", "Naprawdę nie umiesz tańczyć?"),
       ("Nie umiem śpiewać.", "śpiewać", "Naprawdę nie umiesz śpiewać?"),
       ("Nie umiem prowadzić samochodu.", "prowadzić samochód", "Naprawdę nie umiesz prowadzić?"),
       ("Nie umiem czytać po tajsku.", "czytać", "Naprawdę nie umiesz czytać?"),
       ("Nie umiem pisać po tajsku.", "pisać", "Naprawdę nie umiesz pisać?"),
       ("Nie umiem tego naprawić.", "naprawiać", "Naprawdę nie umiesz naprawić?"),
       ("Nie umiem grać.", "grać / bawić się", "Naprawdę nie umiesz grać?"),
       ("Nie umiem się targować.", "pytać", "Naprawdę nie umiesz pytać o cenę?"),
       ("Nie umiem prać ręcznie.", "prać", "Naprawdę nie umiesz prać ręcznie?"),
       ("Nie umiem robić dobrych zdjęć.", "robić zdjęcia", "Naprawdę nie umiesz robić zdjęć?"),
       ("Nie umiem wypełnić formularza.", "wypełnić formularz", "Naprawdę nie umiesz wypełnić?"),
       ("Nie umiem szybko biegać.", "biegać", "Naprawdę nie umiesz biegać?"),
     ]),

# =====================================================================
# … bawi — „czesto"
# =====================================================================
dict(key="BAWI", ty="sentence", cat="Czas i daty", sub="Częstotliwość", reg="n",
     ph="phǒm {ph} bàwi khráp", th="ผม{th}บ่อยครับ",
     lit="bàwi = często",
     note="„bàwi” stoi po czasowniku. Podwojone „bàwi bàwi” znaczy „bardzo często”.",
     ex_ph="{ph} bàwi mǎi khráp", ex_th="{th}บ่อยไหมครับ",
     items=[
       ("Często tu jem.", "jeść", "Często tu jesz?"),
       ("Często to piję.", "pić", "Często to pijesz?"),
       ("Często tu przychodzę.", "przyjść / przyjechać", "Często tu przychodzisz?"),
       ("Często tu kupuję.", "kupować", "Często tu kupujesz?"),
       ("Często gotuję.", "gotować", "Często gotujesz?"),
       ("Często czytam.", "czytać", "Często czytasz?"),
       ("Często oglądam filmy.", "oglądać", "Często oglądasz?"),
       ("Często słucham muzyki.", "słuchać", "Często słuchasz muzyki?"),
       ("Często pływam.", "pływać", "Często pływasz?"),
       ("Często biegam.", "biegać", "Często biegasz?"),
       ("Często podróżuję.", "iść / jechać", "Często podróżujesz?"),
       ("Często zwiedzam.", "zwiedzać", "Często zwiedzasz?"),
       ("Często robię zdjęcia.", "robić zdjęcia", "Często robisz zdjęcia?"),
       ("Często dzwonię do rodziny.", "dzwonić", "Często dzwonisz do rodziny?"),
       ("Często się spotykamy.", "spotykać", "Często się spotykacie?"),
       ("Często się przesiadam.", "przesiadać się", "Często się przesiadasz?"),
       ("Często wynajmuję skuter.", "wynajmować", "Często wynajmujesz skuter?"),
       ("Często zamawiam na wynos.", "zamawiać", "Często zamawiasz na wynos?"),
     ]),

# =====================================================================
# mai khawi … — „rzadko"
# =====================================================================
dict(key="MAIKHAWIV", ty="sentence", cat="Czas i daty", sub="Częstotliwość", reg="n",
     ph="phǒm mâi khâwi {ph} khráp", th="ผมไม่ค่อย{th}ครับ",
     lit="mâi khâwi = rzadko, prawie wcale",
     note="Ta sama konstrukcja co przy przymiotnikach, ale z czasownikiem znaczy „rzadko”.",
     ex_ph="mâi khâwi {ph} rǔe khráp", ex_th="ไม่ค่อย{th}หรือครับ",
     items=[
       ("Rzadko to jem.", "jeść", "Rzadko to jesz?"),
       ("Rzadko to piję.", "pić", "Rzadko to pijesz?"),
       ("Rzadko gotuję.", "gotować", "Rzadko gotujesz?"),
       ("Rzadko oglądam telewizję.", "oglądać", "Rzadko oglądasz?"),
       ("Rzadko czytam.", "czytać", "Rzadko czytasz?"),
       ("Rzadko pływam.", "pływać", "Rzadko pływasz?"),
       ("Rzadko biegam.", "biegać", "Rzadko biegasz?"),
       ("Rzadko tańczę.", "tańczyć", "Rzadko tańczysz?"),
       ("Rzadko tu przychodzę.", "przyjść / przyjechać", "Rzadko tu przychodzisz?"),
       ("Rzadko podróżuję.", "iść / jechać", "Rzadko podróżujesz?"),
       ("Rzadko dzwonię.", "dzwonić", "Rzadko dzwonisz?"),
       ("Rzadko wychodzę wieczorem.", "wychodzić", "Rzadko wychodzisz?"),
       ("Rzadko zamawiam na wynos.", "zamawiać", "Rzadko zamawiasz na wynos?"),
       ("Rzadko robię zdjęcia.", "robić zdjęcia", "Rzadko robisz zdjęcia?"),
       ("Rzadko się spotykamy.", "spotykać", "Rzadko się spotykacie?"),
       ("Rzadko coś wynajmuję.", "wynajmować", "Rzadko wynajmujesz?"),
     ]),

# =====================================================================
# … thuk wan — „codziennie"
# =====================================================================
dict(key="THUKWAN", ty="sentence", cat="Czas i daty", sub="Częstotliwość", reg="n",
     ph="phǒm {ph} thúk wan khráp", th="ผม{th}ทุกวันครับ",
     lit="thúk wan = każdego dnia",
     note="„thúk” znaczy „każdy”: thúk khon — każdy człowiek, thúk aa-thít — co tydzień.",
     ex_ph="{ph} thúk wan loei rǔe khráp", ex_th="{th}ทุกวันเลยหรือครับ",
     items=[
       ("Codziennie tu jem.", "jeść", "Naprawdę codziennie tu jesz?"),
       ("Codziennie to piję.", "pić", "Naprawdę codziennie to pijesz?"),
       ("Codziennie pracuję.", "pracować", "Naprawdę codziennie pracujesz?"),
       ("Codziennie się uczę.", "uczyć się", "Naprawdę codziennie się uczysz?"),
       ("Codziennie biegam.", "biegać", "Naprawdę codziennie biegasz?"),
       ("Codziennie pływam.", "pływać", "Naprawdę codziennie pływasz?"),
       ("Codziennie czytam.", "czytać", "Naprawdę codziennie czytasz?"),
       ("Codziennie gotuję.", "gotować", "Naprawdę codziennie gotujesz?"),
       ("Codziennie sprzątam.", "sprzątać", "Naprawdę codziennie sprzątasz?"),
       ("Codziennie piorę.", "prać", "Naprawdę codziennie pierzesz?"),
       ("Codziennie dzwonię do domu.", "dzwonić", "Naprawdę codziennie dzwonisz?"),
       ("Codziennie wcześnie wstaję.", "wstawać", "Naprawdę codziennie wcześnie wstajesz?"),
       ("Codziennie odpoczywam po pracy.", "odpoczywać", "Naprawdę codziennie odpoczywasz?"),
       ("Codziennie chodzę pieszo.", "iść pieszo", "Naprawdę codziennie chodzisz pieszo?"),
       ("Codziennie myję zęby wieczorem.", "myć zęby", "Naprawdę codziennie wieczorem?"),
       ("Codziennie robię zdjęcia.", "robić zdjęcia", "Naprawdę codziennie robisz zdjęcia?"),
     ]),

# =====================================================================
# khaw lawng … duu — „chce sprobowac"
# =====================================================================
dict(key="KHAWLAWNG", ty="phrase", cat="Gramatyka użytkowa", sub="Chęci", reg="n",
     ph="khǎw lawng {ph} duu nòi khráp", th="ขอลอง{th}ดูหน่อยครับ",
     lit="lawng … duu = spróbować i zobaczyć, co z tego wyjdzie",
     note="Klamra „lawng … duu” zdejmuje z prośby ciężar zobowiązania — świetna w sklepie.",
     ex_ph="lawng {ph} duu sí khráp", ex_th="ลอง{th}ดูสิครับ",
     items=[
       ("Chcę spróbować to zjeść.", "jeść", "Spróbuj zjeść."),
       ("Chcę spróbować to wypić.", "pić", "Spróbuj wypić."),
       ("Chcę to przymierzyć.", "przymierzać / próbować", "Spróbuj przymierzyć."),
       ("Chcę spróbować to ugotować.", "gotować", "Spróbuj ugotować."),
       ("Chcę spróbować poprowadzić.", "prowadzić samochód", "Spróbuj poprowadzić."),
       ("Chcę spróbować to naprawić.", "naprawiać", "Spróbuj naprawić."),
       ("Chcę spróbować zapytać.", "pytać", "Spróbuj zapytać."),
       ("Chcę spróbować zamówić sam.", "zamawiać", "Spróbuj zamówić."),
       ("Chcę spróbować zapłacić kartą.", "płacić", "Spróbuj zapłacić."),
       ("Chcę spróbować to napisać.", "pisać", "Spróbuj napisać."),
       ("Chcę spróbować to przeczytać.", "czytać", "Spróbuj przeczytać."),
       ("Chcę spróbować zatańczyć.", "tańczyć", "Spróbuj zatańczyć."),
       ("Chcę spróbować zaśpiewać.", "śpiewać", "Spróbuj zaśpiewać."),
       ("Chcę spróbować popływać.", "pływać", "Spróbuj popływać."),
       ("Chcę spróbować to wynająć.", "wynajmować", "Spróbuj wynająć."),
       ("Chcę spróbować to wybrać sam.", "wybierać", "Spróbuj wybrać."),
     ]),

# =====================================================================
# chuai yaa — „prosze tego nie robic"
# =====================================================================
dict(key="YAA", ty="phrase", cat="Awarie i pomoc", sub="Prośby", reg="n",
     ph="chûai yàa {ph} khráp", th="ช่วยอย่า{th}ครับ",
     lit="yàa = nie rób tego",
     note="Samo „yàa” brzmi jak rozkaz. Dodanie „chûai” zamienia je w prośbę.",
     ex_ph="yàa {ph} ná khráp", ex_th="อย่า{th}นะครับ",
     items=[
       ("Proszę tu nie palić ani nie jeść.", "jeść", "Proszę tu nie jeść."),
       ("Proszę nie zamykać.", "zamykać", "Proszę nie zamykać."),
       ("Proszę nie otwierać.", "otwierać", "Proszę nie otwierać."),
       ("Proszę nie dzwonić teraz.", "dzwonić", "Proszę teraz nie dzwonić."),
       ("Proszę nie czekać na mnie.", "czekać", "Proszę nie czekać."),
       ("Proszę tego nie zmieniać.", "zmieniać", "Proszę nie zmieniać."),
       ("Proszę tego nie kupować.", "kupować", "Proszę nie kupować."),
       ("Proszę nie zapominać.", "zapominać", "Proszę nie zapomnieć."),
       ("Proszę nie wchodzić.", "wchodzić", "Proszę nie wchodzić."),
       ("Proszę teraz nie wychodzić.", "wychodzić", "Proszę teraz nie wychodzić."),
       ("Proszę się nie spieszyć i nie biec.", "biegać", "Proszę nie biegać."),
       ("Proszę tego nie sprzedawać.", "sprzedawać", "Proszę tego nie sprzedawać."),
       ("Proszę tu nie parkować i się nie zatrzymywać.", "zatrzymać się", "Proszę się tu nie zatrzymywać."),
       ("Proszę nie robić zdjęć.", "robić zdjęcia", "Proszę nie robić zdjęć."),
     ]),

# =====================================================================
# … dai laew — „udalo mi sie"
# =====================================================================
dict(key="DAILAEW", ty="sentence", cat="Gramatyka użytkowa", sub="Przeszłość", reg="n",
     ph="phǒm {ph} dâai láew khráp", th="ผม{th}ได้แล้วครับ",
     lit="… dâai láew = już mi się udało",
     note="Łączy możliwość („dâai”) z dokonaniem („láew”) — czyli sukces po próbach.",
     ex_ph="{ph} dâai láew rǔe khráp", ex_th="{th}ได้แล้วหรือครับ",
     items=[
       ("Udało mi się to znaleźć.", "znaleźć", "Już znalazłeś?"),
       ("Udało mi się zarezerwować.", "rezerwować", "Już zarezerwowałeś?"),
       ("Udało mi się zapłacić.", "płacić", "Już zapłaciłeś?"),
       ("Udało mi się dodzwonić.", "dzwonić", "Już się dodzwoniłeś?"),
       ("Udało mi się zamówić.", "zamawiać", "Już zamówiłeś?"),
       ("Udało mi się to otworzyć.", "otwierać", "Już otworzyłeś?"),
       ("Udało mi się to naprawić.", "naprawiać", "Już naprawiłeś?"),
       ("Udało mi się to zmienić.", "zmieniać", "Już zmieniłeś?"),
       ("Udało mi się wybrać.", "wybierać", "Już wybrałeś?"),
       ("Udało mi się wynająć.", "wynajmować", "Już wynająłeś?"),
       ("Udało mi się to zrozumieć.", "rozumieć", "Już zrozumiałeś?"),
       ("Udało mi się nauczyć.", "uczyć się", "Już się nauczyłeś?"),
       ("Udało mi się spakować.", "pakować się", "Już się spakowałeś?"),
       ("Udało mi się to sprzedać.", "sprzedawać", "Już sprzedałeś?"),
       ("Udało mi się podpisać.", "podpisać", "Już podpisałeś?"),
       ("Udało mi się to wysłać.", "wysyłać", "Już wysłałeś?"),
     ]),

# =====================================================================
# khoei pai — „bylem juz w"
# =====================================================================
dict(key="KHOEIPAI", ty="sentence", cat="Gramatyka użytkowa", sub="Przeszłość", reg="n",
     ph="phǒm khoei pai {ph} láew khráp", th="ผมเคยไป{th}แล้วครับ",
     lit="khoei pai = już tam kiedyś byłem",
     note="Po tajsku „byłem w” to dosłownie „chodziłem do” — stąd „pai”.",
     ex_ph="khoei pai {ph} mǎi khráp", ex_th="เคยไป{th}ไหมครับ",
     items=[
       ("Byłem już na tym targu.", "targ", "Byłeś już na targu?"),
       ("Byłem już na tej plaży.", "plaża", "Byłeś już na plaży?"),
       ("Byłem już w tej świątyni.", "świątynia", "Byłeś już w świątyni?"),
       ("Byłem już w tym parku.", "park", "Byłeś już w parku?"),
       ("Byłem już na tej wyspie.", "wyspa", "Byłeś już na wyspie?"),
       ("Byłem już w tym centrum handlowym.", "centrum handlowe", "Byłeś już w centrum?"),
       ("Byłem już na tym bazarze nocnym.", "bazar nocny", "Byłeś już na bazarze?"),
       ("Byłem już w tej restauracji.", "restauracja", "Byłeś już w tej restauracji?"),
       ("Byłem już w tej kawiarni.", "kawiarnia", "Byłeś już w tej kawiarni?"),
       ("Byłem już w tym salonie masażu.", "salon masażu", "Byłeś już na masażu?"),
       ("Byłem już w tym szpitalu.", "szpital", "Byłeś już w tym szpitalu?"),
       ("Byłem już na tym lotnisku.", "lotnisko", "Byłeś już na tym lotnisku?"),
       ("Byłem już na tym dworcu kolejowym.", "dworzec kolejowy", "Byłeś już na tym dworcu?"),
       ("Byłem już w tym hotelu.", "hotel", "Byłeś już w tym hotelu?"),
       ("Byłem już w tym banku.", "bank", "Byłeś już w tym banku?"),
       ("Byłem już nad tym morzem.", "morze", "Byłeś już nad tym morzem?"),
       ("Byłem już w tych górach.", "góra", "Byłeś już w tych górach?"),
     ]),

# =====================================================================
# yaak pai — „chcialbym pojechac do"
# =====================================================================
dict(key="YAAKPAI", ty="sentence", cat="Gramatyka użytkowa", sub="Plany", reg="n",
     ph="phǒm yàak pai {ph} khráp", th="ผมอยากไป{th}ครับ",
     lit="yàak pai = chcieć się gdzieś wybrać",
     note="Po „yàak” idzie czasownik. „yàak dâai” to chcieć mieć rzecz.",
     ex_ph="yàak pai {ph} mûea-rài khráp", ex_th="อยากไป{th}เมื่อไหร่ครับ",
     items=[
       ("Chciałbym pojechać na plażę.", "plaża", "Kiedy chcesz pojechać na plażę?"),
       ("Chciałbym pojechać na wyspę.", "wyspa", "Kiedy chcesz pojechać na wyspę?"),
       ("Chciałbym pojechać w góry.", "góra", "Kiedy chcesz pojechać w góry?"),
       ("Chciałbym pójść do świątyni.", "świątynia", "Kiedy chcesz iść do świątyni?"),
       ("Chciałbym pójść na targ.", "targ", "Kiedy chcesz iść na targ?"),
       ("Chciałbym pójść na bazar nocny.", "bazar nocny", "Kiedy chcesz iść na bazar?"),
       ("Chciałbym pójść do parku.", "park", "Kiedy chcesz iść do parku?"),
       ("Chciałbym pójść na masaż.", "salon masażu", "Kiedy chcesz iść na masaż?"),
       ("Chciałbym pójść do kawiarni.", "kawiarnia", "Kiedy chcesz iść do kawiarni?"),
       ("Chciałbym pójść do centrum handlowego.", "centrum handlowe", "Kiedy chcesz iść do centrum?"),
       ("Chciałbym pojechać nad morze.", "morze", "Kiedy chcesz pojechać nad morze?"),
       ("Chciałbym pójść na pocztę.", "poczta", "Kiedy chcesz iść na pocztę?"),
       ("Chciałbym pójść do banku.", "bank", "Kiedy chcesz iść do banku?"),
       ("Chciałbym pójść do restauracji.", "restauracja", "Kiedy chcesz iść do restauracji?"),
       ("Chciałbym pojechać na lotnisko wcześniej.", "lotnisko", "Kiedy chcesz jechać na lotnisko?"),
       ("Chciałbym pójść na most.", "most", "Kiedy chcesz iść na most?"),
     ]),

# =====================================================================
# chawp … maak — „bardzo lubie" (rzeczowniki)
# =====================================================================
dict(key="CHAWPMAAK", ty="sentence", cat="Cechy i opinie", sub="Preferencje", reg="i",
     ph="phǒm châwp {ph} mâak khráp", th="ผมชอบ{th}มากครับ",
     lit="châwp … mâak = bardzo coś lubić",
     note="Bez „mâak” zdanie jest neutralne. Z „mâak” brzmi jak szczera pochwała.",
     ex_ph="châwp {ph} mǎi khráp", ex_th="ชอบ{th}ไหมครับ",
     items=[
       ("Bardzo lubię ryż smażony.", "ryż smażony", "Lubisz ryż smażony?"),
       ("Bardzo lubię pad thai.", "pad thai", "Lubisz pad thai?"),
       ("Bardzo lubię zielone curry.", "zielone curry", "Lubisz zielone curry?"),
       ("Bardzo lubię zupę tom yam.", "zupa tom yam z krewetkami", "Lubisz tom yam?"),
       ("Bardzo lubię sałatkę z zielonej papai.", "sałatka z zielonej papai", "Lubisz som tam?"),
       ("Bardzo lubię ryż kleisty z mango.", "ryż kleisty z mango", "Lubisz ryż kleisty z mango?"),
       ("Bardzo lubię mango.", "mango", "Lubisz mango?"),
       ("Bardzo lubię ananas.", "ananas", "Lubisz ananas?"),
       ("Bardzo lubię arbuz.", "arbuz", "Lubisz arbuz?"),
       ("Bardzo lubię papaję.", "papaja", "Lubisz papaję?"),
       ("Bardzo lubię krewetki.", "krewetki", "Lubisz krewetki?"),
       ("Bardzo lubię kraba.", "krab", "Lubisz kraba?"),
       ("Bardzo lubię kalmary.", "kalmary", "Lubisz kalmary?"),
       ("Bardzo lubię kawę mrożoną.", "kawa mrożona", "Lubisz kawę mrożoną?"),
       ("Bardzo lubię herbatę mrożoną.", "herbata mrożona", "Lubisz herbatę mrożoną?"),
       ("Bardzo lubię wodę kokosową.", "woda kokosowa", "Lubisz wodę kokosową?"),
       ("Bardzo lubię lody.", "lody", "Lubisz lody?"),
       ("Bardzo lubię plażę.", "plaża", "Lubisz plażę?"),
       ("Bardzo lubię morze.", "morze", "Lubisz morze?"),
       ("Bardzo lubię góry.", "góra", "Lubisz góry?"),
       ("Bardzo lubię ten park.", "park", "Lubisz ten park?"),
       ("Bardzo lubię ten targ.", "targ", "Lubisz ten targ?"),
     ]),

# =====================================================================
# kin … laew — „jadlem juz"
# =====================================================================
dict(key="KINLAEW", ty="sentence", cat="Jedzenie i napoje", sub="Posiłki", reg="n",
     ph="phǒm kin {ph} láew khráp", th="ผมกิน{th}แล้วครับ",
     lit="kin … láew = już to zjadłem",
     note="„kin” obejmuje jedzenie i picie w mowie potocznej — także lekarstwa.",
     ex_ph="kin {ph} rǔe yang khráp", ex_th="กิน{th}หรือยังครับ",
     items=[
       ("Jadłem już śniadanie.", "śniadanie", "Jadłeś już śniadanie?"),
       ("Jadłem już obiad.", "obiad", "Jadłeś już obiad?"),
       ("Jadłem już kolację.", "kolacja", "Jadłeś już kolację?"),
       ("Jadłem już ryż smażony.", "ryż smażony", "Jadłeś już ryż smażony?"),
       ("Jadłem już pad thai.", "pad thai", "Jadłeś już pad thai?"),
       ("Jadłem już zielone curry.", "zielone curry", "Jadłeś już zielone curry?"),
       ("Jadłem już zupę.", "zupa", "Jadłeś już zupę?"),
       ("Jadłem już sałatkę.", "sałatka", "Jadłeś już sałatkę?"),
       ("Jadłem już owoce.", "owoce", "Jadłeś już owoce?"),
       ("Jadłem już warzywa.", "warzywa", "Jadłeś już warzywa?"),
       ("Jadłem już rybę.", "ryba", "Jadłeś już rybę?"),
       ("Jadłem już kurczaka.", "kurczak", "Jadłeś już kurczaka?"),
       ("Jadłem już wieprzowinę.", "wieprzowina", "Jadłeś już wieprzowinę?"),
       ("Jadłem już wołowinę.", "wołowina", "Jadłeś już wołowinę?"),
       ("Jadłem już lody.", "lody", "Jadłeś już lody?"),
       ("Wziąłem już lekarstwo.", "lek", "Wziąłeś już lekarstwo?"),
       ("Jadłem już makaron w rosole.", "makaron ryżowy w rosole", "Jadłeś już makaron?"),
       ("Jadłem już ryż kleisty.", "ryż kleisty", "Jadłeś już ryż kleisty?"),
     ]),

# =====================================================================
# mai kin — „nie jem"
# =====================================================================
dict(key="MAIKIN", ty="sentence", cat="Jedzenie i napoje", sub="Preferencje", reg="n",
     ph="phǒm mâi kin {ph} khráp", th="ผมไม่กิน{th}ครับ",
     lit="mâi kin = nie jadam czegoś",
     note="Zdanie o stałym nawyku, nie o dzisiejszym wyborze. Do jednorazowej odmowy użyj „mâi ao”.",
     ex_ph="mâi kin {ph} loei rǔe khráp", ex_th="ไม่กิน{th}เลยหรือครับ",
     items=[
       ("Nie jem wieprzowiny.", "wieprzowina", "W ogóle nie jesz wieprzowiny?"),
       ("Nie jem wołowiny.", "wołowina", "W ogóle nie jesz wołowiny?"),
       ("Nie jem ryby.", "ryba", "W ogóle nie jesz ryby?"),
       ("Nie jem krewetek.", "krewetki", "W ogóle nie jesz krewetek?"),
       ("Nie jem kraba.", "krab", "W ogóle nie jesz kraba?"),
       ("Nie jem kalmarów.", "kalmary", "W ogóle nie jesz kalmarów?"),
       ("Nie jem jajek.", "jajko", "W ogóle nie jesz jajek?"),
       ("Nie jem orzeszków ziemnych.", "orzeszki ziemne", "W ogóle nie jesz orzeszków?"),
       ("Nie jem papryczek chili.", "papryczka chili", "W ogóle nie jesz chili?"),
       ("Nie jem słodyczy.", "słodycze / przekąska", "W ogóle nie jesz słodyczy?"),
       ("Nie piję alkoholu.", "alkohol", "W ogóle nie pijesz alkoholu?"),
       ("Nie piję piwa.", "piwo", "W ogóle nie pijesz piwa?"),
       ("Nie piję wina.", "wino", "W ogóle nie pijesz wina?"),
       ("Nie piję kawy.", "kawa", "W ogóle nie pijesz kawy?"),
       ("Nie piję mleka.", "mleko", "W ogóle nie pijesz mleka?"),
       ("Nie jem lodów.", "lody", "W ogóle nie jesz lodów?"),
       ("Nie używam sosu rybnego.", "sos rybny", "W ogóle nie jesz sosu rybnego?"),
       ("Nie jem cukru.", "cukier", "W ogóle nie jesz cukru?"),
     ]),

# =====================================================================
# khaw duu — „czy moge zobaczyc"
# =====================================================================
dict(key="KHAWDUU", ty="question", cat="Zakupy i pieniądze", sub="Oglądanie", reg="n",
     ph="khǎw duu {ph} nòi dâai mǎi khráp", th="ขอดู{th}หน่อยได้ไหมครับ",
     lit="khǎw duu … nòi = poproszę tylko zerknąć",
     note="Grzeczne otwarcie rozmowy w sklepie — nie zobowiązuje do zakupu.",
     ex_ph="duu {ph} dâai loei khráp", ex_th="ดู{th}ได้เลยครับ",
     items=[
       ("Czy mogę zobaczyć pokój?", "pokój", "Proszę obejrzeć pokój."),
       ("Czy mogę zobaczyć kartę dań?", "menu", "Proszę obejrzeć kartę."),
       ("Czy mogę zobaczyć buty?", "buty", "Proszę obejrzeć buty."),
       ("Czy mogę zobaczyć koszulkę?", "koszulka", "Proszę obejrzeć koszulkę."),
       ("Czy mogę zobaczyć spodnie?", "spodnie", "Proszę obejrzeć spodnie."),
       ("Czy mogę zobaczyć kapelusz?", "kapelusz", "Proszę obejrzeć kapelusz."),
       ("Czy mogę zobaczyć okulary przeciwsłoneczne?", "okulary przeciwsłoneczne", "Proszę obejrzeć okulary."),
       ("Czy mogę zobaczyć torbę?", "torba", "Proszę obejrzeć torbę."),
       ("Czy mogę zobaczyć pamiątkę?", "pamiątka", "Proszę obejrzeć pamiątkę."),
       ("Czy mogę zobaczyć mapę?", "mapa", "Proszę obejrzeć mapę."),
       ("Czy mogę zobaczyć rachunek?", "rachunek", "Proszę obejrzeć rachunek."),
       ("Czy mogę zobaczyć paragon?", "paragon", "Proszę obejrzeć paragon."),
       ("Czy mogę zobaczyć rower?", "rower", "Proszę obejrzeć rower."),
       ("Czy mogę zobaczyć motocykl?", "motocykl", "Proszę obejrzeć motocykl."),
       ("Czy mogę zobaczyć kurs wymiany?", "kurs wymiany", "Proszę zobaczyć kurs."),
       ("Czy mogę zobaczyć cenę?", "cena", "Proszę zobaczyć cenę."),
     ]),

# =====================================================================
# mii … kii an — „ile jest"
# =====================================================================
dict(key="MIIKII", ty="question", cat="Liczby i liczenie", sub="Ilość", reg="n",
     ph="mii {ph} kìi an khráp", th="มี{th}กี่อันครับ",
     lit="kìi = ile (przy rzeczach policzalnych)",
     note="„kìi” zawsze wymaga słowa miarowego. „an” pasuje do przedmiotów bez własnego klasyfikatora.",
     ex_ph="mii {ph} yùu kìi an khráp", ex_th="มี{th}อยู่กี่อันครับ",
     items=[
       ("Ile jest ręczników?", "ręcznik", "Ile ręczników zostało?"),
       ("Ile jest koców?", "koc", "Ile koców zostało?"),
       ("Ile jest poduszek?", "poduszka", "Ile poduszek zostało?"),
       ("Ile jest kluczy?", "klucz", "Ile kluczy zostało?"),
       ("Ile jest talerzy?", "talerz", "Ile talerzy zostało?"),
       ("Ile jest szklanek?", "szklanka", "Ile szklanek zostało?"),
       ("Ile jest kubków?", "kubek", "Ile kubków zostało?"),
       ("Ile jest łyżek?", "łyżka", "Ile łyżek zostało?"),
       ("Ile jest widelców?", "widelec", "Ile widelców zostało?"),
       ("Ile jest noży?", "nóż", "Ile noży zostało?"),
       ("Ile jest serwetek?", "serwetka", "Ile serwetek zostało?"),
       ("Ile jest biletów?", "bilet", "Ile biletów zostało?"),
       ("Ile jest kasków?", "kask", "Ile kasków zostało?"),
       ("Ile jest map?", "mapa", "Ile map zostało?"),
       ("Ile jest ładowarek?", "ładowarka", "Ile ładowarek zostało?"),
       ("Ile jest plastrów?", "plaster", "Ile plastrów zostało?"),
     ]),

# =====================================================================
# pai … kan mai — „moze pojdziemy"
# =====================================================================
dict(key="PAIKAN", ty="question", cat="Small talk", sub="Propozycje", reg="i",
     ph="pai {ph} kan mǎi khráp", th="ไป{th}กันไหมครับ",
     lit="… kan = razem, wspólnie",
     note="„kan” zaznacza wspólne działanie. Bez niego propozycja brzmi jak plan tylko dla siebie.",
     ex_ph="pai {ph} kan thòe", ex_th="ไป{th}กันเถอะ",
     items=[
       ("Może pójdziemy na plażę?", "plaża", "Chodźmy na plażę."),
       ("Może pójdziemy na targ?", "targ", "Chodźmy na targ."),
       ("Może pójdziemy na bazar nocny?", "bazar nocny", "Chodźmy na bazar nocny."),
       ("Może pójdziemy do parku?", "park", "Chodźmy do parku."),
       ("Może pójdziemy do świątyni?", "świątynia", "Chodźmy do świątyni."),
       ("Może pójdziemy do kawiarni?", "kawiarnia", "Chodźmy do kawiarni."),
       ("Może pójdziemy do restauracji?", "restauracja", "Chodźmy do restauracji."),
       ("Może pójdziemy na masaż?", "salon masażu", "Chodźmy na masaż."),
       ("Może pójdziemy do centrum handlowego?", "centrum handlowe", "Chodźmy do centrum."),
       ("Może pojedziemy nad morze?", "morze", "Chodźmy nad morze."),
       ("Może pojedziemy na wyspę?", "wyspa", "Chodźmy na wyspę."),
       ("Może pojedziemy w góry?", "góra", "Chodźmy w góry."),
       ("Może pójdziemy na most?", "most", "Chodźmy na most."),
       ("Może pójdziemy do supermarketu?", "supermarket", "Chodźmy do supermarketu."),
     ]),
]
