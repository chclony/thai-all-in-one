# -*- coding: utf-8 -*-
"""Wzorce zdaniowe etapu 4 (B1) — czesc B: przymiotniki, ocena i opinia.

Kazdy wzorzec ma zamknieta biala liste. Polska strona jest pisana recznie.

Konstrukcje nowe wobec A1 i A2: przypuszczenie (khong jà, àat jà), zawiedzione
oczekiwanie (mâi … yàang thîi khít wái), porownanie z przeszloscia
(duu … kwàa mûea kàwn), stopniowanie zalezne (yîng … yîng …), przyczyna stanu
(tham hâi phǒm …), przyznanie racji (yawm ráp wâa), uprzejmy kontrargument
(hěn dûai … tàae …), zaprzeczenie zaprzeczenia (mâi châi wâa mâi …).

Pozycja: (polskie haslo rekordu, polskie haslo bazowe, polski przyklad)
"""

TPL_B = [

# =====================================================================
# khong ja — przypuszczenie mocne
# =====================================================================
dict(key="KHONGJA", ty="sentence", cat="Cechy i opinie", sub="Przypuszczenie", reg="n",
     ph="khong jà {ph} khráp", th="คงจะ{th}ครับ",
     lit="khong jà = pewnie, zapewne",
     note="„khong jà” to domysł oparty na przesłankach. Słabsze niż „nâe nawn”, mocniejsze niż „àat jà”.",
     ex_ph="khun khít wâa khong jà {ph} mǎi khráp", ex_th="คุณคิดว่าคงจะ{th}ไหมครับ",
     items=[
       ("Pewnie jest drogo.", "drogi", "Myślisz, że będzie drogo?"),
       ("Pewnie jest tanio.", "tani", "Myślisz, że będzie tanio?"),
       ("Pewnie jest daleko.", "daleki", "Myślisz, że to daleko?"),
       ("Pewnie jest blisko.", "bliski", "Myślisz, że to blisko?"),
       ("Pewnie jest zajęte.", "pełny / zajęty", "Myślisz, że będzie zajęte?"),
       ("Pewnie jest wolne.", "wolny (dostępny)", "Myślisz, że będzie wolne?"),
       ("Pewnie jest ostre.", "ostry (pikantny)", "Myślisz, że będzie ostre?"),
       ("Pewnie jest smaczne.", "smaczny", "Myślisz, że będzie smaczne?"),
       ("Pewnie jest gorąco.", "gorący", "Myślisz, że będzie gorąco?"),
       ("Pewnie jest zimno.", "zimny (o napoju)", "Myślisz, że będzie zimne?"),
       ("Pewnie jest trudne.", "trudny", "Myślisz, że będzie trudne?"),
       ("Pewnie jest łatwe.", "łatwy", "Myślisz, że będzie łatwe?"),
       ("Pewnie jest głośno.", "głośny", "Myślisz, że będzie głośno?"),
       ("Pewnie jest cicho.", "cichy / spokojny", "Myślisz, że będzie cicho?"),
       ("Pewnie jest brudno.", "brudny", "Myślisz, że będzie brudno?"),
       ("Pewnie jest czysto.", "czysty", "Myślisz, że będzie czysto?"),
       ("Pewnie jest bezpiecznie.", "bezpieczny", "Myślisz, że będzie bezpiecznie?"),
       ("Pewnie jest ciężkie.", "ciężki", "Myślisz, że będzie ciężkie?"),
       ("Pewnie jest nowe.", "nowy", "Myślisz, że będzie nowe?"),
       ("Pewnie jest stare.", "stary", "Myślisz, że będzie stare?"),
       ("Pewnie jest wygodne.", "wygodny", "Myślisz, że będzie wygodne?"),
       ("Pewnie jest nudne.", "nudny", "Myślisz, że będzie nudne?"),
       ("Pewnie jest ciekawe.", "interesujący", "Myślisz, że będzie ciekawe?"),
       ("Pewnie jest świeże.", "świeży", "Myślisz, że będzie świeże?"),
       ("Pewnie jest zatłoczone.", "duży", "Myślisz, że będzie duży tłum?"),
     ]),

# =====================================================================
# aat ja … kaw dai — przypuszczenie slabe
# =====================================================================
dict(key="AATJA", ty="sentence", cat="Cechy i opinie", sub="Przypuszczenie", reg="n",
     ph="àat jà {ph} kâw dâai khráp", th="อาจจะ{th}ก็ได้ครับ",
     lit="àat jà … kâw dâai = może i tak, ale nie musi",
     note="Zakończenie „kâw dâai” osłabia domysł jeszcze bardziej. To najostrożniejsza forma opinii.",
     ex_ph="mii thaang {ph} mǎi khráp", ex_th="มีทาง{th}ไหมครับ",
     items=[
       ("Może i jest drogo.", "drogi", "Jest szansa, że będzie drogo?"),
       ("Może i jest za ostre.", "ostry (pikantny)", "Jest szansa, że będzie ostre?"),
       ("Może i jest zajęte.", "pełny / zajęty", "Jest szansa, że będzie zajęte?"),
       ("Może i jest za duże.", "duży", "Jest szansa, że będzie duże?"),
       ("Może i jest za małe.", "mały", "Jest szansa, że będzie małe?"),
       ("Może i jest niebezpiecznie.", "niebezpieczny", "Jest szansa, że będzie niebezpiecznie?"),
       ("Może i jest za daleko.", "daleki", "Jest szansa, że będzie daleko?"),
       ("Może i jest zbyt wolno.", "wolny (powolny)", "Jest szansa, że będzie wolno?"),
       ("Może i jest szybko.", "szybki", "Jest szansa, że będzie szybko?"),
       ("Może i jest twarde.", "twardy", "Jest szansa, że będzie twarde?"),
       ("Może i jest miękkie.", "miękki", "Jest szansa, że będzie miękkie?"),
       ("Może i jest słone.", "słony", "Jest szansa, że będzie słone?"),
       ("Może i jest słodkie.", "słodki", "Jest szansa, że będzie słodkie?"),
       ("Może i jest kwaśne.", "kwaśny", "Jest szansa, że będzie kwaśne?"),
       ("Może i jest gorzkie.", "gorzki", "Jest szansa, że będzie gorzkie?"),
       ("Może i jest ciemno.", "ciemny", "Jest szansa, że będzie ciemno?"),
       ("Może i jest jasno.", "jasny", "Jest szansa, że będzie jasno?"),
       ("Może i jest płytko.", "głęboki", "Jest szansa, że będzie głęboko?"),
       ("Może i jest pusto.", "pusty", "Jest szansa, że będzie pusto?"),
       ("Może i jest lekkie.", "lekki", "Jest szansa, że będzie lekkie?"),
     ]),

# =====================================================================
# mai … yaang thii khit wai — zawiedzione oczekiwanie
# =====================================================================
dict(key="YAANGTHIIKHIT", ty="sentence", cat="Cechy i opinie", sub="Oczekiwania", reg="n",
     ph="mâi {ph} yàang thîi khít wái khráp", th="ไม่{th}อย่างที่คิดไว้ครับ",
     lit="yàang thîi khít wái = tak, jak się to sobie wyobrażało",
     note="„khít wái” to myśl zachowana z przeszłości. Partykuła „wái” niesie tu całe „wcześniej sobie założyłem”.",
     ex_ph="man {ph} yàang thîi khít wái mǎi khráp", ex_th="มัน{th}อย่างที่คิดไว้ไหมครับ",
     items=[
       ("Nie jest tak drogo, jak myślałem.", "drogi", "Jest tak drogo, jak zakładałeś?"),
       ("Nie jest tak tanio, jak myślałem.", "tani", "Jest tak tanio, jak zakładałeś?"),
       ("Nie jest tak ostre, jak myślałem.", "ostry (pikantny)", "Jest tak ostre, jak zakładałeś?"),
       ("Nie jest tak smaczne, jak myślałem.", "smaczny", "Jest tak smaczne, jak zakładałeś?"),
       ("Nie jest tak trudne, jak myślałem.", "trudny", "Jest tak trudne, jak zakładałeś?"),
       ("Nie jest tak łatwe, jak myślałem.", "łatwy", "Jest tak łatwe, jak zakładałeś?"),
       ("Nie jest tak daleko, jak myślałem.", "daleki", "Jest tak daleko, jak zakładałeś?"),
       ("Nie jest tak głośno, jak myślałem.", "głośny", "Jest tak głośno, jak zakładałeś?"),
       ("Nie jest tak duże, jak myślałem.", "duży", "Jest tak duże, jak zakładałeś?"),
       ("Nie jest tak małe, jak myślałem.", "mały", "Jest tak małe, jak zakładałeś?"),
       ("Nie jest tak gorąco, jak myślałem.", "gorący", "Jest tak gorąco, jak zakładałeś?"),
       ("Nie jest tak ciekawe, jak myślałem.", "interesujący", "Jest tak ciekawe, jak zakładałeś?"),
       ("Nie jest tak nudne, jak myślałem.", "nudny", "Jest tak nudne, jak zakładałeś?"),
       ("Nie jest tak wygodne, jak myślałem.", "wygodny", "Jest tak wygodne, jak zakładałeś?"),
       ("Nie jest tak czysto, jak myślałem.", "czysty", "Jest tak czysto, jak zakładałeś?"),
       ("Nie jest tak szybko, jak myślałem.", "szybki", "Jest tak szybko, jak zakładałeś?"),
       ("Nie jest tak bezpiecznie, jak myślałem.", "bezpieczny", "Jest tak bezpiecznie, jak zakładałeś?"),
       ("Nie jest tak świeże, jak myślałem.", "świeży", "Jest tak świeże, jak zakładałeś?"),
       ("Nie jest tak nowe, jak myślałem.", "nowy", "Jest tak nowe, jak zakładałeś?"),
       ("Nie jest tak ciężkie, jak myślałem.", "ciężki", "Jest tak ciężkie, jak zakładałeś?"),
     ]),

# =====================================================================
# duu … kwaa muea kawn — porownanie z przeszloscia
# =====================================================================
dict(key="KWAAMUEAKAWN", ty="sentence", cat="Cechy i opinie", sub="Zmiana", reg="n",
     ph="duu {ph} kwàa mûea kàwn khráp", th="ดู{th}กว่าเมื่อก่อนครับ",
     lit="duu … kwàa mûea kàwn = wygląda na bardziej … niż dawniej",
     note="„duu” przed przymiotnikiem znaczy „sprawia wrażenie”. Bez niego byłoby to twierdzenie, nie obserwacja.",
     ex_ph="rúu-sùek wâa {ph} kwàa mûea kàwn mǎi khráp", ex_th="รู้สึกว่า{th}กว่าเมื่อก่อนไหมครับ",
     items=[
       ("Wygląda drożej niż kiedyś.", "drogi", "Czujesz, że jest drożej niż dawniej?"),
       ("Wygląda taniej niż kiedyś.", "tani", "Czujesz, że jest taniej niż dawniej?"),
       ("Wygląda czyściej niż kiedyś.", "czysty", "Czujesz, że jest czyściej niż dawniej?"),
       ("Wygląda na bardziej zatłoczone niż kiedyś.", "pełny / zajęty", "Czujesz, że jest tłoczniej niż dawniej?"),
       ("Wygląda spokojniej niż kiedyś.", "cichy / spokojny", "Czujesz, że jest spokojniej niż dawniej?"),
       ("Wygląda na nowsze niż kiedyś.", "nowy", "Czujesz, że jest nowsze niż dawniej?"),
       ("Wygląda na starsze niż kiedyś.", "stary", "Czujesz, że jest starsze niż dawniej?"),
       ("Wygląda ładniej niż kiedyś.", "ładny", "Czujesz, że jest ładniej niż dawniej?"),
       ("Wygląda na bardziej zadbane niż kiedyś.", "dobry", "Czujesz, że jest lepiej niż dawniej?"),
       ("Wygląda gorzej niż kiedyś.", "zły / kiepski", "Czujesz, że jest gorzej niż dawniej?"),
       ("Wygląda na cieplejsze niż kiedyś.", "gorący", "Czujesz, że jest cieplej niż dawniej?"),
       ("Wygląda na bardziej ruchliwe niż kiedyś.", "szybki", "Czujesz, że jest szybciej niż dawniej?"),
       ("Wygląda na bezpieczniejsze niż kiedyś.", "bezpieczny", "Czujesz, że jest bezpieczniej niż dawniej?"),
       ("Wygląda na wygodniejsze niż kiedyś.", "wygodny", "Czujesz, że jest wygodniej niż dawniej?"),
       ("Wygląda ciekawiej niż kiedyś.", "interesujący", "Czujesz, że jest ciekawiej niż dawniej?"),
       ("Wygląda na trudniejsze niż kiedyś.", "trudny", "Czujesz, że jest trudniej niż dawniej?"),
     ]),

# =====================================================================
# ying naan ying — stopniowanie zalezne
# =====================================================================
dict(key="YINGNAAN", ty="sentence", cat="Gramatyka użytkowa", sub="Stopniowanie", reg="n",
     ph="yîng naan yîng {ph} khráp", th="ยิ่งนานยิ่ง{th}ครับ",
     lit="yîng … yîng … = im bardziej…, tym bardziej…",
     note="Konstrukcja dwuczłonowa: pierwsze „yîng” zapowiada warunek, drugie skutek. Polskie „im…, tym…” działa tak samo, ale kolejność słów jest inna.",
     ex_ph="yîng naan man yîng {ph} loei rǒe khráp", ex_th="ยิ่งนานมันยิ่ง{th}เลยหรือครับ",
     items=[
       ("Im dłużej, tym drożej.", "drogi", "Im dłużej, tym drożej?"),
       ("Im dłużej, tym trudniej.", "trudny", "Im dłużej, tym trudniej?"),
       ("Im dłużej, tym łatwiej.", "łatwy", "Im dłużej, tym łatwiej?"),
       ("Im dłużej, tym goręcej.", "gorący", "Im dłużej, tym goręcej?"),
       ("Im dłużej, tym głośniej.", "głośny", "Im dłużej, tym głośniej?"),
       ("Im dłużej, tym ciekawiej.", "interesujący", "Im dłużej, tym ciekawiej?"),
       ("Im dłużej, tym nudniej.", "nudny", "Im dłużej, tym nudniej?"),
       ("Im dłużej, tym gorzej.", "zły / kiepski", "Im dłużej, tym gorzej?"),
       ("Im dłużej, tym bardziej zmęczony.", "zmęczony", "Im dłużej, tym bardziej zmęczony?"),
       ("Im dłużej, tym spokojniej.", "cichy / spokojny", "Im dłużej, tym spokojniej?"),
       ("Im dłużej, tym bardziej zestresowany.", "zestresowany", "Im dłużej, tym bardziej zestresowany?"),
       ("Im dłużej, tym bardziej zadowolony.", "zadowolony", "Im dłużej, tym bardziej zadowolony?"),
       ("Im dłużej, tym bardziej znudzony.", "znudzony", "Im dłużej, tym bardziej znudzony?"),
       ("Im dłużej, tym bardziej głodny.", "głodny", "Im dłużej, tym bardziej głodny?"),
       ("Im dłużej, tym większy tłok.", "duży", "Im dłużej, tym większy tłok?"),
     ]),

# =====================================================================
# man tham hai phom — przyczyna stanu
# =====================================================================
dict(key="THAMHAI", ty="sentence", cat="Cechy i opinie", sub="Emocje", reg="n",
     ph="man tham hâi phǒm {ph} khráp", th="มันทำให้ผม{th}ครับ",
     lit="tham hâi = sprawić, że ktoś staje się jakiś",
     note="„tham hâi + osoba + przymiotnik” to tajski sposób mówienia o przyczynie emocji. Polskie „przez to jestem…” nie ma tu odpowiednika słowo w słowo.",
     ex_ph="man tham hâi khun {ph} rǒe khráp", ex_th="มันทำให้คุณ{th}หรือครับ",
     items=[
       ("Przez to czuję się zmęczony.", "zmęczony", "To cię tak męczy?"),
       ("Przez to czuję się zestresowany.", "zestresowany", "To cię tak stresuje?"),
       ("Przez to czuję się zdenerwowany.", "zdenerwowany", "To cię tak denerwuje?"),
       ("Przez to czuję się smutny.", "smutny", "To cię tak zasmuca?"),
       ("Przez to czuję się szczęśliwy.", "szczęśliwy", "To cię tak cieszy?"),
       ("Przez to czuję się zadowolony.", "zadowolony", "To cię tak zadowala?"),
       ("Przez to czuję się rozczarowany.", "rozczarowany", "To cię tak rozczarowuje?"),
       ("Przez to czuję się zaskoczony.", "zaskoczony", "To cię tak zaskakuje?"),
       ("Przez to czuję się samotny.", "samotny", "To cię tak osamotnia?"),
       ("Przez to czuję się spokojny.", "spokojny, opanowany", "To cię tak uspokaja?"),
       ("Przez to czuję się znudzony.", "znudzony", "To cię tak nudzi?"),
       ("Przez to czuję się przestraszony.", "przestraszony", "To cię tak przeraża?"),
       ("Przez to czuję się dumny.", "dumny", "To cię tak napawa dumą?"),
       ("Przez to czuję się głodny.", "głodny", "To cię tak głodzi?"),
       ("Przez to czuję się słaby.", "słaby", "To cię tak osłabia?"),
     ]),

# =====================================================================
# yawm rap waa man … jing — przyznanie racji
# =====================================================================
dict(key="YAWMRAP", ty="sentence", cat="Cechy i opinie", sub="Zgoda", reg="f",
     ph="phǒm yawm ráp wâa man {ph} jing khráp", th="ผมยอมรับว่ามัน{th}จริงครับ",
     lit="yawm ráp = uznać, przyznać",
     note="Przyznanie racji przed kontrargumentem to podstawa uprzejmej dyskusji po tajsku.",
     ex_ph="khun yawm ráp mǎi khráp wâa man {ph}", ex_th="คุณยอมรับไหมครับว่ามัน{th}",
     items=[
       ("Przyznaję, że rzeczywiście jest drogo.", "drogi", "Przyznasz, że jest drogo?"),
       ("Przyznaję, że rzeczywiście jest trudne.", "trudny", "Przyznasz, że jest trudne?"),
       ("Przyznaję, że rzeczywiście jest wolne.", "wolny (powolny)", "Przyznasz, że jest wolne?"),
       ("Przyznaję, że rzeczywiście jest głośno.", "głośny", "Przyznasz, że jest głośno?"),
       ("Przyznaję, że rzeczywiście jest daleko.", "daleki", "Przyznasz, że jest daleko?"),
       ("Przyznaję, że rzeczywiście jest ważne.", "ważny", "Przyznasz, że to ważne?"),
       ("Przyznaję, że rzeczywiście jest smaczne.", "smaczny", "Przyznasz, że jest smaczne?"),
       ("Przyznaję, że rzeczywiście jest ciekawe.", "interesujący", "Przyznasz, że jest ciekawe?"),
       ("Przyznaję, że rzeczywiście jest niewygodne.", "wygodny", "Przyznasz, że jest niewygodne?"),
       ("Przyznaję, że rzeczywiście jest ryzykowne.", "niebezpieczny", "Przyznasz, że jest ryzykowne?"),
       ("Przyznaję, że rzeczywiście jest brudno.", "brudny", "Przyznasz, że jest brudno?"),
       ("Przyznaję, że rzeczywiście jest ciasno.", "mały", "Przyznasz, że jest ciasno?"),
       ("Przyznaję, że rzeczywiście jest nudne.", "nudny", "Przyznasz, że jest nudne?"),
       ("Przyznaję, że rzeczywiście jest gorąco.", "gorący", "Przyznasz, że jest gorąco?"),
     ]),

# =====================================================================
# hen duai … tae … pai noi — uprzejmy kontrargument
# =====================================================================
dict(key="HENDUAITAE", ty="sentence", cat="Cechy i opinie", sub="Kontrargument", reg="n",
     ph="hěn dûai khráp tàae wâa {ph} pai nòi", th="เห็นด้วยครับ แต่ว่า{th}ไปหน่อย",
     lit="hěn dûai … tàae … pai nòi = zgadzam się, ale odrobinę za bardzo…",
     note="Najbezpieczniejszy schemat sporu po tajsku: najpierw zgoda, potem zastrzeżenie z osłabiaczem „pai nòi”. Sam sprzeciw brzmiałby konfrontacyjnie.",
     ex_ph="mâi khít wâa man {ph} pai nòi rǒe khráp", ex_th="ไม่คิดว่ามัน{th}ไปหน่อยหรือครับ",
     items=[
       ("Zgadzam się, ale to trochę za drogie.", "drogi", "Nie sądzisz, że trochę za drogie?"),
       ("Zgadzam się, ale to trochę za ostre.", "ostry (pikantny)", "Nie sądzisz, że trochę za ostre?"),
       ("Zgadzam się, ale to trochę za daleko.", "daleki", "Nie sądzisz, że trochę za daleko?"),
       ("Zgadzam się, ale to trochę za głośne.", "głośny", "Nie sądzisz, że trochę za głośne?"),
       ("Zgadzam się, ale to trochę za wolne.", "wolny (powolny)", "Nie sądzisz, że trochę za wolne?"),
       ("Zgadzam się, ale to trochę za duże.", "duży", "Nie sądzisz, że trochę za duże?"),
       ("Zgadzam się, ale to trochę za małe.", "mały", "Nie sądzisz, że trochę za małe?"),
       ("Zgadzam się, ale to trochę za trudne.", "trudny", "Nie sądzisz, że trochę za trudne?"),
       ("Zgadzam się, ale to trochę za słone.", "słony", "Nie sądzisz, że trochę za słone?"),
       ("Zgadzam się, ale to trochę za słodkie.", "słodki", "Nie sądzisz, że trochę za słodkie?"),
       ("Zgadzam się, ale to trochę za ciężkie.", "ciężki", "Nie sądzisz, że trochę za ciężkie?"),
       ("Zgadzam się, ale to trochę za stare.", "stary", "Nie sądzisz, że trochę za stare?"),
       ("Zgadzam się, ale to trochę za ciemne.", "ciemny", "Nie sądzisz, że trochę za ciemne?"),
       ("Zgadzam się, ale to trochę za ryzykowne.", "niebezpieczny", "Nie sądzisz, że trochę za ryzykowne?"),
       ("Zgadzam się, ale to trochę za szybko.", "szybki", "Nie sądzisz, że trochę za szybko?"),
     ]),

# =====================================================================
# mai chai waa mai … na — zaprzeczenie zaprzeczenia
# =====================================================================
dict(key="MAICHAIWAA", ty="sentence", cat="Cechy i opinie", sub="Sprostowanie", reg="n",
     ph="mâi châi wâa mâi {ph} ná khráp", th="ไม่ใช่ว่าไม่{th}นะครับ",
     lit="mâi châi wâa mâi … = nie chodzi o to, że nie jest…",
     note="Podwójne przeczenie służy do prostowania cudzego wniosku bez sprzeciwiania się wprost.",
     ex_ph="ngán man {ph} rǔe plào khráp", ex_th="งั้นมัน{th}หรือเปล่าครับ",
     items=[
       ("Nie chodzi o to, że nie jest smaczne.", "smaczny", "To jest w końcu smaczne czy nie?"),
       ("Nie chodzi o to, że nie jest dobre.", "dobry", "To jest w końcu dobre czy nie?"),
       ("Nie chodzi o to, że nie jest ładne.", "ładny", "To jest w końcu ładne czy nie?"),
       ("Nie chodzi o to, że nie jest tanie.", "tani", "To jest w końcu tanie czy nie?"),
       ("Nie chodzi o to, że nie jest ciekawe.", "interesujący", "To jest w końcu ciekawe czy nie?"),
       ("Nie chodzi o to, że nie jest wygodne.", "wygodny", "To jest w końcu wygodne czy nie?"),
       ("Nie chodzi o to, że nie jest ważne.", "ważny", "To jest w końcu ważne czy nie?"),
       ("Nie chodzi o to, że nie jest bezpieczne.", "bezpieczny", "To jest w końcu bezpieczne czy nie?"),
       ("Nie chodzi o to, że nie jest czyste.", "czysty", "To jest w końcu czyste czy nie?"),
       ("Nie chodzi o to, że nie jest świeże.", "świeży", "To jest w końcu świeże czy nie?"),
       ("Nie chodzi o to, że nie jest łatwe.", "łatwy", "To jest w końcu łatwe czy nie?"),
       ("Nie chodzi o to, że nie jest szybkie.", "szybki", "To jest w końcu szybkie czy nie?"),
     ]),

# =====================================================================
# nuek waa ja … kwaa nii — spodziewalem sie wiecej
# =====================================================================
dict(key="NUEKWAA", ty="sentence", cat="Cechy i opinie", sub="Oczekiwania", reg="n",
     ph="nùek wâa jà {ph} kwàa níi khráp", th="นึกว่าจะ{th}กว่านี้ครับ",
     lit="nùek wâa = wyobrażałem sobie, że",
     note="„nùek wâa” zawsze wprowadza mylne wyobrażenie. Jeśli oczekiwanie się sprawdziło, mówi się „khâat wái”.",
     ex_ph="nùek wâa jà {ph} kwàa níi mǎi khráp", ex_th="นึกว่าจะ{th}กว่านี้ไหมครับ",
     items=[
       ("Myślałem, że będzie tańsze.", "tani", "Też myślałeś, że będzie tańsze?"),
       ("Myślałem, że będzie większe.", "duży", "Też myślałeś, że będzie większe?"),
       ("Myślałem, że będzie mniejsze.", "mały", "Też myślałeś, że będzie mniejsze?"),
       ("Myślałem, że będzie smaczniejsze.", "smaczny", "Też myślałeś, że będzie smaczniejsze?"),
       ("Myślałem, że będzie szybsze.", "szybki", "Też myślałeś, że będzie szybsze?"),
       ("Myślałem, że będzie ciekawsze.", "interesujący", "Też myślałeś, że będzie ciekawsze?"),
       ("Myślałem, że będzie łatwiejsze.", "łatwy", "Też myślałeś, że będzie łatwiejsze?"),
       ("Myślałem, że będzie nowsze.", "nowy", "Też myślałeś, że będzie nowsze?"),
       ("Myślałem, że będzie czystsze.", "czysty", "Też myślałeś, że będzie czystsze?"),
       ("Myślałem, że będzie cichsze.", "cichy / spokojny", "Też myślałeś, że będzie cichsze?"),
       ("Myślałem, że będzie wygodniejsze.", "wygodny", "Też myślałeś, że będzie wygodniejsze?"),
       ("Myślałem, że będzie ostrzejsze.", "ostry (pikantny)", "Też myślałeś, że będzie ostrzejsze?"),
       ("Myślałem, że będzie świeższe.", "świeży", "Też myślałeś, że będzie świeższe?"),
       ("Myślałem, że będzie lżejsze.", "lekki", "Też myślałeś, że będzie lżejsze?"),
     ]),

# =====================================================================
# kaw … yuu na — ostrozne przyznanie
# =====================================================================
dict(key="KAWYUUNA", ty="sentence", cat="Cechy i opinie", sub="Opinie", reg="p",
     ph="kâw {ph} yùu ná khráp", th="ก็{th}อยู่นะครับ",
     lit="kâw … yùu ná = no, w sumie trochę tak",
     note="Bardzo potoczne złagodzenie oceny. W piśmie służbowym nie występuje — tam użyj „khâwn khâang …”.",
     ex_ph="man {ph} yùu mǎi khráp", ex_th="มัน{th}อยู่ไหมครับ",
     items=[
       ("No, w sumie jest smaczne.", "smaczny", "Jest w sumie smaczne?"),
       ("No, w sumie jest drogo.", "drogi", "Jest w sumie drogo?"),
       ("No, w sumie jest ładne.", "ładny", "Jest w sumie ładne?"),
       ("No, w sumie jest ciekawe.", "interesujący", "Jest w sumie ciekawe?"),
       ("No, w sumie jest trudne.", "trudny", "Jest w sumie trudne?"),
       ("No, w sumie jest daleko.", "daleki", "Jest w sumie daleko?"),
       ("No, w sumie jest głośno.", "głośny", "Jest w sumie głośno?"),
       ("No, w sumie jest wygodne.", "wygodny", "Jest w sumie wygodne?"),
       ("No, w sumie jest nudne.", "nudny", "Jest w sumie nudne?"),
       ("No, w sumie jestem zmęczony.", "zmęczony", "Jesteś w sumie zmęczony?"),
       ("No, w sumie jestem zadowolony.", "zadowolony", "Jesteś w sumie zadowolony?"),
       ("No, w sumie jest bezpiecznie.", "bezpieczny", "Jest w sumie bezpiecznie?"),
     ]),

# =====================================================================
# khaw khang … na — ocena wywazona, rejestr wyzszy
# =====================================================================
dict(key="KHAWNKHANG", ty="sentence", cat="Cechy i opinie", sub="Opinie", reg="f",
     ph="thǔe wâa khâwn khâang {ph} khráp", th="ถือว่าค่อนข้าง{th}ครับ",
     lit="khâwn khâang = dość, stosunkowo",
     note="Wyważona ocena w rejestrze formalnym. Odpowiednik potocznego „kâw … yùu ná”.",
     ex_ph="thǔe wâa khâwn khâang {ph} mǎi khráp", ex_th="ถือว่าค่อนข้าง{th}ไหมครับ",
     items=[
       ("Trzeba uznać, że jest dość drogo.", "drogi", "Uważa pan, że jest dość drogo?"),
       ("Trzeba uznać, że jest dość tanio.", "tani", "Uważa pan, że jest dość tanio?"),
       ("Trzeba uznać, że jest dość trudne.", "trudny", "Uważa pan, że jest dość trudne?"),
       ("Trzeba uznać, że jest dość ważne.", "ważny", "Uważa pan, że jest dość ważne?"),
       ("Trzeba uznać, że jest dość bezpieczne.", "bezpieczny", "Uważa pan, że jest dość bezpieczne?"),
       ("Trzeba uznać, że jest dość ciekawe.", "interesujący", "Uważa pan, że jest dość ciekawe?"),
       ("Trzeba uznać, że jest dość wygodne.", "wygodny", "Uważa pan, że jest dość wygodne?"),
       ("Trzeba uznać, że jest dość szybkie.", "szybki", "Uważa pan, że jest dość szybkie?"),
       ("Trzeba uznać, że jest dość czysto.", "czysty", "Uważa pan, że jest dość czysto?"),
       ("Trzeba uznać, że jest dość głośno.", "głośny", "Uważa pan, że jest dość głośno?"),
       ("Trzeba uznać, że jest dość nowe.", "nowy", "Uważa pan, że jest dość nowe?"),
       ("Trzeba uznać, że jest dość daleko.", "daleki", "Uważa pan, że jest dość daleko?"),
     ]),
]
