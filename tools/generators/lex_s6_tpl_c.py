# -*- coding: utf-8 -*-
"""Wzorce zdaniowe etapu 6 — trzecia seria.

Zakres uzupelniajacy: jedzenie przy stole (uczulenia, dokladka, sklad,
lagodniejsza wersja dania) oraz dzialanie wspolne i pytanie o powod.

Konstrukcje sprawdzone jako nieuzyte w etapach 1-5: „pháe …”, „… phôoem
ìik nòi”, „tham jàak à-rai”, „bàep mâi phèt”, „… dûai kan dâai mǎi”,
„tham mai tâwng …”, „khon ùen kâw … mǔean kan”.

Pozycja: (polskie haslo rekordu, polskie haslo bazowe, polski przyklad)
"""

TPL_C = [

# =====================================================================
# phom phae … khrap — uczulenie
# =====================================================================
dict(key="PHAEALLERG", ty="sentence", cat="Zdrowie", sub="Alergie", reg="n",
     ph="phǒm pháe {ph} khráp", th="ผมแพ้{th}ครับ",
     lit="pháe … = mieć uczulenie na …",
     note="Zdanie o znaczeniu ratunkowym — wypowiedz je, zanim złożysz zamówienie. „pháe” dotyczy też uczulenia na leki.",
     ex_ph="phǒm pháe {ph} khráp mâi sài dâai mǎi", ex_th="ผมแพ้{th}ครับ ไม่ใส่ได้ไหม",
     items=[
       ("Jestem uczulony na krewetki.", "krewetki", "Jestem uczulony na krewetki, można bez nich?"),
       ("Jestem uczulony na kraba.", "krab", "Jestem uczulony na kraba, można bez niego?"),
       ("Jestem uczulony na kalmary.", "kalmary", "Jestem uczulony na kalmary, można bez nich?"),
       ("Jestem uczulony na rybę.", "ryba", "Jestem uczulony na rybę, można bez niej?"),
       ("Jestem uczulony na jajka.", "jajko", "Jestem uczulony na jajka, można bez nich?"),
       ("Jestem uczulony na mleko.", "mleko", "Jestem uczulony na mleko, można bez niego?"),
       ("Jestem uczulony na orzeszki ziemne.", "orzeszki ziemne", "Jestem uczulony na orzeszki, można bez nich?"),
       ("Jestem uczulony na sos rybny.", "sos rybny", "Jestem uczulony na sos rybny, można bez niego?"),
       ("Jestem uczulony na chili.", "papryczka chili", "Jestem uczulony na chili, można bez niego?"),
       ("Jestem uczulony na kokos.", "kokos", "Jestem uczulony na kokos, można bez niego?"),
       ("Jestem uczulony na mango.", "mango", "Jestem uczulony na mango, można bez niego?"),
       ("Jestem uczulony na wieprzowinę.", "wieprzowina", "Jestem uczulony na wieprzowinę, można bez niej?"),
       ("Jestem uczulony na alkohol.", "alkohol", "Jestem uczulony na alkohol, można bez niego?"),
       ("Jestem uczulony na warzywa strączkowe.", "warzywa", "Jestem uczulony na te warzywa, można bez nich?"),
     ]),

# =====================================================================
# khaw … phoem iik noi khrap — dokladka
# =====================================================================
dict(key="PHOEMIIK", ty="sentence", cat="Restauracja", sub="Dokładka", reg="n",
     ph="khǎw {ph} phôoem ìik nòi khráp", th="ขอ{th}เพิ่มอีกหน่อยครับ",
     lit="phôoem ìik nòi = jeszcze trochę więcej",
     note="„phôoem” to dołożyć do tego, co już masz. Prośba o nową porcję to „khǎw … ìik thîi”.",
     ex_ph="khǎw {ph} phôoem ìik nòi khráp khàwp khun khráp", ex_th="ขอ{th}เพิ่มอีกหน่อยครับ ขอบคุณครับ",
     items=[
       ("Poproszę jeszcze trochę ryżu.", "ryż", "Poproszę jeszcze trochę ryżu, dziękuję."),
       ("Poproszę jeszcze trochę wody.", "woda", "Poproszę jeszcze trochę wody, dziękuję."),
       ("Poproszę jeszcze trochę lodu.", "lód", "Poproszę jeszcze trochę lodu, dziękuję."),
       ("Poproszę jeszcze trochę zupy.", "zupa", "Poproszę jeszcze trochę zupy, dziękuję."),
       ("Poproszę jeszcze trochę warzyw.", "warzywa", "Poproszę jeszcze trochę warzyw, dziękuję."),
       ("Poproszę jeszcze trochę sosu rybnego.", "sos rybny", "Poproszę jeszcze trochę sosu rybnego, dziękuję."),
       ("Poproszę jeszcze trochę cukru.", "cukier", "Poproszę jeszcze trochę cukru, dziękuję."),
       ("Poproszę jeszcze trochę soli.", "sól", "Poproszę jeszcze trochę soli, dziękuję."),
       ("Poproszę jeszcze trochę herbaty.", "herbata", "Poproszę jeszcze trochę herbaty, dziękuję."),
       ("Poproszę jeszcze trochę kawy.", "kawa", "Poproszę jeszcze trochę kawy, dziękuję."),
       ("Poproszę jeszcze kilka serwetek.", "serwetka", "Poproszę jeszcze serwetki, dziękuję."),
       ("Poproszę jeszcze jeden talerz.", "talerz", "Poproszę jeszcze talerz, dziękuję."),
       ("Poproszę jeszcze jedną szklankę.", "szklanka", "Poproszę jeszcze szklankę, dziękuję."),
       ("Poproszę jeszcze jedną łyżkę.", "łyżka", "Poproszę jeszcze łyżkę, dziękuję."),
       ("Poproszę jeszcze trochę owoców.", "owoce", "Poproszę jeszcze trochę owoców, dziękuję."),
       ("Poproszę jeszcze trochę makaronu.", "makaron ryżowy w rosole", "Poproszę jeszcze trochę makaronu, dziękuję."),
     ]),

# =====================================================================
# … nii tham jaak arai khrap — sklad dania
# =====================================================================
dict(key="THAMJAAK", ty="question", cat="Restauracja", sub="Skład dania", reg="n",
     ph="{ph} níi tham jàak à-rai khráp", th="{th}นี้ทำจากอะไรครับ",
     lit="tham jàak à-rai = z czego zrobione",
     note="Pytanie warte zadania przy uczuleniach i przy diecie. Kelner wymieni składniki, a nie nazwę dania.",
     ex_ph="{ph} níi tham jàak à-rai khráp mii núea sàt mǎi", ex_th="{th}นี้ทำจากอะไรครับ มีเนื้อสัตว์ไหม",
     items=[
       ("Z czego jest ta zupa?", "zupa", "Z czego jest ta zupa? Czy jest w niej mięso?"),
       ("Z czego jest ta sałatka?", "sałatka", "Z czego jest ta sałatka? Czy jest w niej mięso?"),
       ("Z czego jest ten deser?", "deser", "Z czego jest ten deser? Czy jest w nim mięso?"),
       ("Z czego jest ta przystawka?", "przystawka", "Z czego jest ta przystawka? Czy jest w niej mięso?"),
       ("Z czego jest to danie główne?", "danie główne", "Z czego jest to danie? Czy jest w nim mięso?"),
       ("Z czego jest ten sos?", "sos rybny", "Z czego jest ten sos? Czy jest w nim mięso?"),
       ("Z czego jest ten makaron?", "makaron ryżowy w rosole", "Z czego jest ten makaron? Czy jest w nim mięso?"),
       ("Z czego jest ten napój?", "napoje", "Z czego jest ten napój? Czy jest w nim mięso?"),
       ("Z czego są te lody?", "lody", "Z czego są te lody? Czy jest w nich mięso?"),
       ("Z czego jest to curry?", "zielone curry", "Z czego jest to curry? Czy jest w nim mięso?"),
       ("Z czego jest ten ryż smażony?", "ryż smażony", "Z czego jest ten ryż smażony? Czy jest w nim mięso?"),
       ("Z czego jest ten pad thai?", "pad thai", "Z czego jest ten pad thai? Czy jest w nim mięso?"),
     ]),

# =====================================================================
# mii … baep mai phet mai khrap — lagodniejsza wersja
# =====================================================================
dict(key="BAEPMAIPHET", ty="question", cat="Restauracja", sub="Ostrość", reg="n",
     ph="mii {ph} bàep mâi phèt mǎi khráp", th="มี{th}แบบไม่เผ็ดไหมครับ",
     lit="bàep mâi phèt = wersja nieostra",
     note="„bàep” to wariant, wersja. Konstrukcja działa też z „bàep mâi wǎan” (niesłodka) i „bàep mâi mii núea” (bez mięsa).",
     ex_ph="mii {ph} bàep mâi phèt mǎi khráp phǒm kin phèt mâi dâai", ex_th="มี{th}แบบไม่เผ็ดไหมครับ ผมกินเผ็ดไม่ได้",
     items=[
       ("Czy jest nieostra wersja tej zupy?", "zupa", "Czy jest nieostra zupa? Nie jem ostrych potraw."),
       ("Czy jest nieostra sałatka?", "sałatka", "Czy jest nieostra sałatka? Nie jem ostrych potraw."),
       ("Czy jest nieostry pad thai?", "pad thai", "Czy jest nieostry pad thai? Nie jem ostrych potraw."),
       ("Czy jest nieostre curry?", "zielone curry", "Czy jest nieostre curry? Nie jem ostrych potraw."),
       ("Czy jest nieostry ryż smażony?", "ryż smażony", "Czy jest nieostry ryż smażony? Nie jem ostrych potraw."),
       ("Czy jest nieostry makaron?", "makaron ryżowy w rosole", "Czy jest nieostry makaron? Nie jem ostrych potraw."),
       ("Czy jest nieostra sałatka z papai?", "sałatka z zielonej papai", "Czy jest nieostra sałatka z papai? Nie jem ostrych potraw."),
       ("Czy jest nieostra tom yam?", "zupa tom yam z krewetkami", "Czy jest nieostra tom yam? Nie jem ostrych potraw."),
       ("Czy jest nieostre danie główne?", "danie główne", "Czy jest nieostre danie główne? Nie jem ostrych potraw."),
       ("Czy jest nieostra przystawka?", "przystawka", "Czy jest nieostra przystawka? Nie jem ostrych potraw."),
       ("Czy jest nieostry kurczak?", "kurczak", "Czy jest nieostry kurczak? Nie jem ostrych potraw."),
       ("Czy jest nieostra wieprzowina?", "wieprzowina", "Czy jest nieostra wieprzowina? Nie jem ostrych potraw."),
       ("Czy jest nieostra ryba?", "ryba", "Czy jest nieostra ryba? Nie jem ostrych potraw."),
       ("Czy są nieostre krewetki?", "krewetki", "Czy są nieostre krewetki? Nie jem ostrych potraw."),
     ]),

# =====================================================================
# … duai kan daai mai khrap — dzialanie wspolne
# =====================================================================
dict(key="DUAIKAN", ty="question", cat="Small talk", sub="Propozycje", reg="n",
     ph="{ph} dûai kan dâai mǎi khráp", th="{th}ด้วยกันได้ไหมครับ",
     lit="dûai kan = razem, wspólnie",
     note="Uprzejma propozycja wspólnego działania. W odróżnieniu od „… kan thòe” nie zakłada z góry zgody rozmówcy.",
     ex_ph="thâa mâi rangkìat {ph} dûai kan dâai mǎi khráp", ex_th="ถ้าไม่รังเกียจ {th}ด้วยกันได้ไหมครับ",
     items=[
       ("Czy możemy pójść razem?", "iść / jechać", "Jeśli to nie kłopot, czy możemy pójść razem?"),
       ("Czy możemy zjeść razem?", "jeść", "Jeśli to nie kłopot, czy możemy zjeść razem?"),
       ("Czy możemy poczekać razem?", "czekać", "Jeśli to nie kłopot, czy możemy poczekać razem?"),
       ("Czy możemy uczyć się razem?", "uczyć się", "Jeśli to nie kłopot, czy możemy uczyć się razem?"),
       ("Czy możemy pracować razem?", "pracować", "Jeśli to nie kłopot, czy możemy pracować razem?"),
       ("Czy możemy zwiedzać razem?", "zwiedzać", "Jeśli to nie kłopot, czy możemy zwiedzać razem?"),
       ("Czy możemy wracać razem?", "wracać", "Jeśli to nie kłopot, czy możemy wracać razem?"),
       ("Czy możemy zapłacić wspólnie?", "płacić", "Jeśli to nie kłopot, czy możemy zapłacić wspólnie?"),
       ("Czy możemy zamówić wspólnie?", "zamawiać", "Jeśli to nie kłopot, czy możemy zamówić wspólnie?"),
       ("Czy możemy popływać razem?", "pływać", "Jeśli to nie kłopot, czy możemy popływać razem?"),
       ("Czy możemy poszukać razem?", "szukać", "Jeśli to nie kłopot, czy możemy poszukać razem?"),
       ("Czy możemy zrobić zdjęcie razem?", "robić zdjęcia", "Jeśli to nie kłopot, czy możemy zrobić zdjęcie razem?"),
       ("Czy możemy się razem pouczyć czytania?", "czytać", "Jeśli to nie kłopot, czy możemy poczytać razem?"),
       ("Czy możemy zaśpiewać razem?", "śpiewać", "Jeśli to nie kłopot, czy możemy zaśpiewać razem?"),
     ]),

# =====================================================================
# tham mai tawng … khrap — pytanie o powod obowiazku
# =====================================================================
dict(key="THAMMAITAWNG", ty="question", cat="Pytania", sub="Powody", reg="n",
     ph="tham mai tâwng {ph} khráp", th="ทำไมต้อง{th}ครับ",
     lit="tham mai tâwng … = dlaczego trzeba …?",
     note="Pytanie o powód wymogu, nie zarzut. Ton głosu decyduje o odbiorze — wypowiedziane ostro brzmi jak podważanie autorytetu.",
     ex_ph="khǎw-thôot khráp tham mai tâwng {ph} khráp", ex_th="ขอโทษครับ ทำไมต้อง{th}ครับ",
     items=[
       ("Dlaczego trzeba czekać?", "czekać", "Przepraszam, dlaczego trzeba czekać?"),
       ("Dlaczego trzeba płacić?", "płacić", "Przepraszam, dlaczego trzeba płacić?"),
       ("Dlaczego trzeba się przesiadać?", "przesiadać się", "Przepraszam, dlaczego trzeba się przesiadać?"),
       ("Dlaczego trzeba rezerwować?", "rezerwować", "Przepraszam, dlaczego trzeba rezerwować?"),
       ("Dlaczego trzeba podpisywać?", "podpisać", "Przepraszam, dlaczego trzeba podpisywać?"),
       ("Dlaczego trzeba wracać?", "wracać", "Przepraszam, dlaczego trzeba wracać?"),
       ("Dlaczego trzeba zmieniać?", "zmieniać", "Przepraszam, dlaczego trzeba to zmieniać?"),
       ("Dlaczego trzeba wypełniać formularz?", "wypełnić formularz", "Przepraszam, dlaczego trzeba wypełniać formularz?"),
       ("Dlaczego trzeba dzwonić?", "dzwonić", "Przepraszam, dlaczego trzeba dzwonić?"),
       ("Dlaczego trzeba to pokazywać?", "pokazać", "Przepraszam, dlaczego trzeba to pokazywać?"),
       ("Dlaczego trzeba wysiadać?", "wysiadać", "Przepraszam, dlaczego trzeba wysiadać?"),
       ("Dlaczego trzeba anulować?", "anulować", "Przepraszam, dlaczego trzeba anulować?"),
     ]),

# =====================================================================
# khon uen kaw … muean kan khrap — odwolanie do innych
# =====================================================================
dict(key="KHONUEN", ty="sentence", cat="Small talk", sub="Argumenty", reg="n",
     ph="khon ùen kâw {ph} mǔean kan khráp", th="คนอื่นก็{th}เหมือนกันครับ",
     lit="khon ùen kâw … mǔean kan = inni też …",
     note="Łagodny argument przez odwołanie do zwyczaju. W tajskiej rozmowie działa lepiej niż powoływanie się na własne prawa.",
     ex_ph="khon ùen kâw {ph} mǔean kan khráp mâi châi phǒm khon diao", ex_th="คนอื่นก็{th}เหมือนกันครับ ไม่ใช่ผมคนเดียว",
     items=[
       ("Inni też czekają.", "czekać", "Inni też czekają, nie tylko ja."),
       ("Inni też płacą.", "płacić", "Inni też płacą, nie tylko ja."),
       ("Inni też pytają.", "pytać", "Inni też pytają, nie tylko ja."),
       ("Inni też rezerwują.", "rezerwować", "Inni też rezerwują, nie tylko ja."),
       ("Inni też się uczą.", "uczyć się", "Inni też się uczą, nie tylko ja."),
       ("Inni też tak robią.", "robić", "Inni też tak robią, nie tylko ja."),
       ("Inni też wynajmują.", "wynajmować", "Inni też wynajmują, nie tylko ja."),
       ("Inni też zamawiają.", "zamawiać", "Inni też zamawiają, nie tylko ja."),
       ("Inni też się przesiadają.", "przesiadać się", "Inni też się przesiadają, nie tylko ja."),
       ("Inni też tu pracują.", "pracować", "Inni też tu pracują, nie tylko ja."),
     ]),
]
