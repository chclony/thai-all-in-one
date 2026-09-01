# -*- coding: utf-8 -*-
"""Sesja F — PODAWANIE GODZINY. Pelny system, od zera.

DLACZEGO TO JEST TRUDNE DLA POLAKA

Polski dzieli dobe na dwie polowy po dwanascie godzin i liczy je tak samo.
Tajski dzieli dobe na SZESC POR i kazda liczy OD NOWA, wlasnym slowem:

  tii    ตี      01:00-05:00   „tii” + liczba          (tii sǎam = 3 w nocy)
  cháo   เช้า    06:00-11:00   liczba + „mohng cháo”   (jèt mohng cháo = 7 rano)
  thîang เที่ยง   12:00         „thîang wan”            (poludnie)
  bàai   บ่าย    13:00-15:00   „bàai” + liczba + mohng (bàai sǎwng mohng = 14)
  yen    เย็น    16:00-18:00   liczba + „mohng yen”    (hâa mohng yen = 17)
  thûm   ทุ่ม    19:00-23:00   liczba + „thûm”, LICZONA OD 19:00
                               (nùeng thûm = 19, sǎwng thûm = 20)

Pulapka numer jeden: „sǎwng thûm” to NIE druga w nocy, tylko 20:00. Liczba przy
„thûm” liczy godziny od dziewietnastej, nie od polnocy.

Pulapka numer dwa: „sǎai” (สาย) to nie godzina, tylko pora — pozny ranek, mniej
wiecej 09:00-11:00. Uzywa sie go opisowo („przyjde sǎai”), nie do podawania
konkretnej godziny.

Pulapka numer trzy: nie ma tajskiego odpowiednika „wpol do”. Polowa dokladana
jest ZA godzina jako „khrûeng”: „bàai mohng khrûeng” = 13:30, doslownie
„pierwsza popoludniu i pol”. Konstrukcja „wpol do drugiej” nie istnieje.

System 24-godzinny („naa-lí-kaa”) istnieje, ale wylacznie w komunikatach
oficjalnych: dworzec, lotnisko, wojsko, radio. W rozmowie brzmi sztucznie.
"""

CAT = "Czas i daty"
SUB = "Godziny"
SUBP = "Pory dnia"

TIME = [

# ============================================================ pytanie i rdzen
("A1", "Która godzina?", "kìi mohng láew", "กี่โมงแล้ว", "Pytania", SUB, 5, "n",
 "Dosłownie „ile godzin już”. Partykuła „láew” jest tu obowiązkowa — samo „kìi mohng” brzmi jak pytanie o umówioną porę, nie o aktualny czas.",
 "ile godzina już",
 [("Przepraszam, która godzina?", "khǎw thôot khráp kìi mohng láew khráp", "ขอโทษครับกี่โมงแล้วครับ"),
  ("Która godzina teraz?", "tawn níi kìi mohng láew khráp", "ตอนนี้กี่โมงแล้วครับ"),
  ("Nie wiem, która godzina.", "phǒm mâi rúu wâa kìi mohng láew khráp", "ผมไม่รู้ว่ากี่โมงแล้วครับ")],
 ["godzina (jednostka)", "o której godzinie", "zegarek"], []),

("A1", "o której godzinie", "kìi mohng", "กี่โมง", "Pytania", SUB, 5, "n",
 "Bez „láew” pytanie dotyczy pory umówionej lub rozkładowej. To wersja, której użyjesz na dworcu i przy umawianiu spotkania.",
 "ile godzina",
 [("O której odjeżdża autobus?", "rót mee àwk kìi mohng khráp", "รถเมล์ออกกี่โมงครับ"),
  ("O której się spotkamy?", "rao jòoe kan kìi mohng khráp", "เราเจอกันกี่โมงครับ"),
  ("O której otwieracie?", "pòoet kìi mohng khráp", "เปิดกี่โมงครับ")],
 ["Która godzina?", "godzina (jednostka)"], []),

("A1", "godzina (jednostka)", "chûa-mohng", "ชั่วโมง", CAT, SUB, 5, "n",
 "Uwaga na różnicę: „chûa-mohng” to godzina jako odcinek czasu (trwanie), a „mohng” to godzina na zegarze. Po polsku oba to „godzina”.",
 "",
 [("Czekałem godzinę.", "phǒm raw nùeng chûa-mohng khráp", "ผมรอหนึ่งชั่วโมงครับ"),
  ("Ile godzin trwa podróż?", "chái wee-laa kìi chûa-mohng khráp", "ใช้เวลากี่ชั่วโมงครับ"),
  ("Za dwie godziny.", "ìik sǎwng chûa-mohng", "อีกสองชั่วโมง")],
 ["minuta (jednostka)", "Która godzina?", "czas"], []),

("A1", "minuta (jednostka)", "naa-thii", "นาที", CAT, SUB, 5, "n",
 "„th” to „t” z przydechem. Ta sama forma dla liczby pojedynczej i mnogiej — tajski nie odmienia.",
 "",
 [("Poczekaj pięć minut.", "raw hâa naa-thii khráp", "รอห้านาทีครับ"),
  ("To zajmie dziesięć minut.", "chái wee-laa sìp naa-thii khráp", "ใช้เวลาสิบนาทีครับ"),
  ("Zostało jeszcze dwadzieścia minut.", "lǔea ìik yîi-sìp naa-thii khráp", "เหลืออีกยี่สิบนาทีครับ")],
 ["godzina (jednostka)", "sekunda"], []),

("A2", "sekunda", "wí-naa-thii", "วินาที", CAT, SUB, 3, "n",
 "Dosłownie „ułamek minuty”. W mowie codziennej częściej usłyszysz „sák khrûu” (chwileczkę) niż liczbę sekund.",
 "",
 [("Poczekaj sekundę.", "raw sák wí-naa-thii khráp", "รอสักวินาทีครับ"),
  ("Zostało trzydzieści sekund.", "lǔea sǎam-sìp wí-naa-thii khráp", "เหลือสามสิบวินาทีครับ")],
 ["minuta (jednostka)", "chwileczkę"], []),

# ============================================================ pora: tii (noc)
("A2", "pierwsza w nocy", "tii nùeng", "ตีหนึ่ง", CAT, SUB, 3, "n",
 "Pora „tii” obejmuje 01:00–05:00 i liczy się wprost: tii nùeng, tii sǎwng, aż do tii hâa. Słowo „tii” znaczy pierwotnie „uderzać” — od uderzeń gongu odmierzających noc.",
 "uderzenie jeden",
 [("Wróciłem o pierwszej w nocy.", "phǒm klàp maa tii nùeng khráp", "ผมกลับมาตีหนึ่งครับ"),
  ("Jest już pierwsza w nocy.", "tii nùeng láew khráp", "ตีหนึ่งแล้วครับ")],
 ["druga w nocy", "północ", "noc"], []),

("A2", "druga w nocy", "tii sǎwng", "ตีสอง", CAT, SUB, 3, "n",
 "Nie mylić z „sǎwng thûm”, które oznacza 20:00. Liczba przy „tii” to godzina nocna, liczba przy „thûm” to wieczór.",
 "uderzenie dwa",
 [("Pociąg przyjeżdża o drugiej w nocy.", "rót fai thǔeng tii sǎwng khráp", "รถไฟถึงตีสองครับ"),
  ("Spałem dopiero o drugiej.", "phǒm nawn tawn tii sǎwng khráp", "ผมนอนตอนตีสองครับ")],
 ["pierwsza w nocy", "trzecia w nocy", "ósma wieczorem"], []),

("A2", "trzecia w nocy", "tii sǎam", "ตีสาม", CAT, SUB, 3, "n",
 "Dwie sylaby, obie z tonem rosnącym na drugiej. Typowa pora odjazdu nocnych autobusów dalekobieżnych.",
 "uderzenie trzy",
 [("Autobus odjeżdża o trzeciej w nocy.", "rót àwk tii sǎam khráp", "รถออกตีสามครับ"),
  ("Obudziłem się o trzeciej.", "phǒm tùen tawn tii sǎam khráp", "ผมตื่นตอนตีสามครับ")],
 ["druga w nocy", "czwarta nad ranem"], []),

("A2", "czwarta nad ranem", "tii sìi", "ตีสี่", CAT, SUB, 3, "n",
 "Pora, o której zaczyna się ruch na targach hurtowych i przy świątyniach.",
 "uderzenie cztery",
 [("Targ otwiera się o czwartej nad ranem.", "tà-làat pòoet tii sìi khráp", "ตลาดเปิดตีสี่ครับ"),
  ("Muszę wstać o czwartej.", "phǒm tâwng tùen tii sìi khráp", "ผมต้องตื่นตีสี่ครับ")],
 ["trzecia w nocy", "piąta nad ranem", "świt"], []),

("A2", "piąta nad ranem", "tii hâa", "ตีห้า", CAT, SUB, 3, "n",
 "Ostatnia godzina pory „tii”. Szósta to już „hòk mohng cháo” — system się przełącza.",
 "uderzenie pięć",
 [("Wstaję o piątej.", "phǒm tùen tii hâa khráp", "ผมตื่นตีห้าครับ"),
  ("O piątej jest jeszcze ciemno.", "tii hâa yang mûet yùu khráp", "ตีห้ายังมืดอยู่ครับ")],
 ["czwarta nad ranem", "szósta rano", "świt"], []),

# ============================================================ pora: cháo (rano)
("A1", "szósta rano", "hòk mohng cháo", "หกโมงเช้า", CAT, SUB, 4, "n",
 "Tu system się zmienia: od szóstej liczba stoi PRZED „mohng”, a po nim dochodzi nazwa pory „cháo”. Pierwsza godzina, przy której mówi się „mohng”.",
 "sześć godzina rano",
 [("Wstaję o szóstej rano.", "phǒm tùen hòk mohng cháo khráp", "ผมตื่นหกโมงเช้าครับ"),
  ("Śniadanie jest od szóstej.", "aa-hǎan cháo sòet tâng-tàe hòk mohng khráp", "อาหารเช้าเสิร์ฟตั้งแต่หกโมงครับ")],
 ["piąta nad ranem", "siódma rano", "rano"], []),

("A1", "siódma rano", "jèt mohng cháo", "เจ็ดโมงเช้า", CAT, SUB, 4, "n",
 "„j” czytaj jak polskie „dź”. Najczęstsza pora wyjazdu autobusów turystycznych.",
 "siedem godzina rano",
 [("Autobus odjeżdża o siódmej rano.", "rót àwk jèt mohng cháo khráp", "รถออกเจ็ดโมงเช้าครับ"),
  ("Spotkajmy się o siódmej.", "jòoe kan jèt mohng cháo ná khráp", "เจอกันเจ็ดโมงเช้านะครับ")],
 ["szósta rano", "ósma rano"], []),

("A1", "ósma rano", "pàet mohng cháo", "แปดโมงเช้า", CAT, SUB, 4, "n",
 "Standardowa godzina rozpoczęcia pracy w tajskich urzędach — otwierają o ósmej trzydzieści.",
 "osiem godzina rano",
 [("Zaczynam pracę o ósmej.", "phǒm rôoem ngaan pàet mohng cháo khráp", "ผมเริ่มงานแปดโมงเช้าครับ"),
  ("Urząd otwiera o ósmej trzydzieści.", "sǎm-nák-ngaan pòoet pàet mohng khrûeng khráp", "สำนักงานเปิดแปดโมงครึ่งครับ")],
 ["siódma rano", "dziewiąta rano", "praca"], []),

("A1", "dziewiąta rano", "kâo mohng cháo", "เก้าโมงเช้า", CAT, SUB, 4, "n",
 "Ton opadający na „kâo”. Uwaga: „kâo” z innym tonem to „wchodzić” (khâo) — ćwicz różnicę.",
 "dziewięć godzina rano",
 [("Sklep otwiera o dziewiątej.", "ráan pòoet kâo mohng cháo khráp", "ร้านเปิดเก้าโมงเช้าครับ"),
  ("Przyjdę o dziewiątej.", "phǒm jà maa kâo mohng cháo khráp", "ผมจะมาเก้าโมงเช้าครับ")],
 ["ósma rano", "dziesiąta rano"], []),

("A1", "dziesiąta rano", "sìp mohng cháo", "สิบโมงเช้า", CAT, SUB, 4, "n",
 "Od dziesiątej można też powiedzieć opisowo „sǎai” — późny ranek. To pora, nie godzina.",
 "dziesięć godzina rano",
 [("Wymeldowanie jest o dziesiątej.", "chék-aut sìp mohng cháo khráp", "เช็คเอาท์สิบโมงเช้าครับ"),
  ("Spotkajmy się o dziesiątej.", "jòoe kan sìp mohng cháo khráp", "เจอกันสิบโมงเช้าครับ")],
 ["dziewiąta rano", "jedenasta rano", "późny ranek"], []),

("A1", "jedenasta rano", "sìp-èt mohng cháo", "สิบเอ็ดโมงเช้า", CAT, SUB, 4, "n",
 "Liczba 11 to „sìp-èt”, nie „sìp nùeng” — jedynka w liczbach złożonych ma osobną formę „èt”.",
 "jedenaście godzina rano",
 [("Restauracja otwiera o jedenastej.", "ráan aa-hǎan pòoet sìp-èt mohng cháo khráp", "ร้านอาหารเปิดสิบเอ็ดโมงเช้าครับ"),
  ("Zadzwoń o jedenastej.", "thoo maa sìp-èt mohng ná khráp", "โทรมาสิบเอ็ดโมงนะครับ")],
 ["dziesiąta rano", "południe"], []),

# ============================================================ poludnie i bàai
("A1", "południe", "thîang wan", "เที่ยงวัน", CAT, SUBP, 5, "n",
 "Godzina dwunasta w dzień. Samo „thîang” w rozmowie wystarcza; „thîang khuen” to z kolei północ.",
 "południe dzień",
 [("Zjem w południe.", "phǒm jà kin thîang khráp", "ผมจะกินเที่ยงครับ"),
  ("Spotkajmy się w południe.", "jòoe kan thîang wan khráp", "เจอกันเที่ยงวันครับ"),
  ("Przerwa jest w południe.", "phák thîang khráp", "พักเที่ยงครับ")],
 ["północ", "pierwsza po południu", "obiad"], []),

("A1", "pierwsza po południu", "bàai mohng", "บ่ายโมง", CAT, SUB, 4, "n",
 "Wyjątek w systemie: przy pierwszej NIE mówi się liczby. Nie „bàai nùeng mohng”, tylko samo „bàai mohng”.",
 "popołudnie godzina",
 [("Spotkanie jest o pierwszej.", "prà-chum bàai mohng khráp", "ประชุมบ่ายโมงครับ"),
  ("Wracam o pierwszej.", "phǒm klàp bàai mohng khráp", "ผมกลับบ่ายโมงครับ")],
 ["południe", "druga po południu", "popołudnie"], []),

("A1", "druga po południu", "bàai sǎwng mohng", "บ่ายสองโมง", CAT, SUB, 4, "n",
 "Od drugiej wraca liczba, ale stoi między „bàai” a „mohng”. Szyk jest inny niż przy porannym „sǎwng mohng cháo”.",
 "popołudnie dwa godzina",
 [("Przyjdę o drugiej po południu.", "phǒm jà maa bàai sǎwng mohng khráp", "ผมจะมาบ่ายสองโมงครับ"),
  ("Pociąg odjeżdża o drugiej.", "rót fai àwk bàai sǎwng mohng khráp", "รถไฟออกบ่ายสองโมงครับ")],
 ["pierwsza po południu", "trzecia po południu"], []),

("A1", "trzecia po południu", "bàai sǎam mohng", "บ่ายสามโมง", CAT, SUB, 4, "n",
 "Ostatnia godzina pory „bàai”. Czwarta to już „sìi mohng yen”.",
 "popołudnie trzy godzina",
 [("Kończę o trzeciej.", "phǒm lôoek bàai sǎam mohng khráp", "ผมเลิกบ่ายสามโมงครับ"),
  ("Herbata o trzeciej.", "dùuem chaa bàai sǎam mohng khráp", "ดื่มชาบ่ายสามโมงครับ")],
 ["druga po południu", "czwarta po południu"], []),

# ============================================================ pora: yen
("A1", "czwarta po południu", "sìi mohng yen", "สี่โมงเย็น", CAT, SUB, 4, "n",
 "Pora „yen” zaczyna się o szesnastej. Szyk wraca do porannego: liczba, „mohng”, nazwa pory.",
 "cztery godzina wieczór",
 [("Wracam o czwartej.", "phǒm klàp sìi mohng yen khráp", "ผมกลับสี่โมงเย็นครับ"),
  ("Dzieci wychodzą ze szkoły o czwartej.", "dèk lôoek rian sìi mohng yen khráp", "เด็กเลิกเรียนสี่โมงเย็นครับ")],
 ["trzecia po południu", "piąta po południu", "wieczór"], []),

("A1", "piąta po południu", "hâa mohng yen", "ห้าโมงเย็น", CAT, SUB, 4, "n",
 "Godzina, o której kończy się dzień pracy w większości biur.",
 "pięć godzina wieczór",
 [("Kończę pracę o piątej.", "phǒm lôoek ngaan hâa mohng yen khráp", "ผมเลิกงานห้าโมงเย็นครับ"),
  ("Spotkajmy się o piątej.", "jòoe kan hâa mohng yen khráp", "เจอกันห้าโมงเย็นครับ")],
 ["czwarta po południu", "szósta wieczorem"], []),

("A1", "szósta wieczorem", "hòk mohng yen", "หกโมงเย็น", CAT, SUB, 4, "n",
 "Ostatnia godzina liczona przez „mohng”. Od siódmej system przechodzi na „thûm” i liczy od nowa.",
 "sześć godzina wieczór",
 [("Kolacja o szóstej.", "aa-hǎan yen hòk mohng khráp", "อาหารเย็นหกโมงครับ"),
  ("Słońce zachodzi o szóstej.", "phrá aa-thít tòk hòk mohng yen khráp", "พระอาทิตย์ตกหกโมงเย็นครับ")],
 ["piąta po południu", "siódma wieczorem", "zmierzch"], []),

# ============================================================ pora: thûm
("A1", "siódma wieczorem", "nùeng thûm", "หนึ่งทุ่ม", CAT, SUB, 4, "n",
 "TU JEST NAJWIĘKSZA PUŁAPKA CAŁEGO SYSTEMU. „nùeng thûm” to dziewiętnasta, nie pierwsza. Liczba przy „thûm” liczy godziny OD 19:00, więc trzeba do niej dodać osiemnaście.",
 "jeden uderzenie",
 [("Kolacja jest o siódmej wieczorem.", "aa-hǎan yen nùeng thûm khráp", "อาหารเย็นหนึ่งทุ่มครับ"),
  ("Film zaczyna się o siódmej.", "nǎng rôoem nùeng thûm khráp", "หนังเริ่มหนึ่งทุ่มครับ"),
  ("Przyjdę o siódmej wieczorem.", "phǒm jà maa nùeng thûm khráp", "ผมจะมาหนึ่งทุ่มครับ")],
 ["szósta wieczorem", "ósma wieczorem", "wieczór"], []),

("A1", "ósma wieczorem", "sǎwng thûm", "สองทุ่ม", CAT, SUB, 4, "n",
 "Dwadzieścia zero zero. Uczący się notorycznie słyszą tu „druga” — a druga w nocy to „tii sǎwng”.",
 "dwa uderzenie",
 [("Wracam o ósmej wieczorem.", "phǒm klàp sǎwng thûm khráp", "ผมกลับสองทุ่มครับ"),
  ("Sklep zamyka o ósmej.", "ráan pìt sǎwng thûm khráp", "ร้านปิดสองทุ่มครับ")],
 ["siódma wieczorem", "dziewiąta wieczorem", "druga w nocy"], []),

("A1", "dziewiąta wieczorem", "sǎam thûm", "สามทุ่ม", CAT, SUB, 4, "n",
 "Dwadzieścia jeden zero zero. Typowa godzina ostatniego kursu autobusu miejskiego.",
 "trzy uderzenie",
 [("Ostatni autobus jest o dziewiątej.", "rót khan sùt-tháai sǎam thûm khráp", "รถคันสุดท้ายสามทุ่มครับ"),
  ("Idę spać o dziewiątej.", "phǒm nawn sǎam thûm khráp", "ผมนอนสามทุ่มครับ")],
 ["ósma wieczorem", "dziesiąta wieczorem"], []),

("A2", "dziesiąta wieczorem", "sìi thûm", "สี่ทุ่ม", CAT, SUB, 3, "n",
 "Dwadzieścia dwa zero zero. Cisza nocna w wielu kondominiach zaczyna się właśnie o tej porze.",
 "cztery uderzenie",
 [("Cisza nocna od dziesiątej.", "hâam sǐang dang tâng-tàe sìi thûm khráp", "ห้ามเสียงดังตั้งแต่สี่ทุ่มครับ"),
  ("Wróciłem o dziesiątej wieczorem.", "phǒm klàp sìi thûm khráp", "ผมกลับสี่ทุ่มครับ")],
 ["dziewiąta wieczorem", "jedenasta wieczorem"], []),

("A2", "jedenasta wieczorem", "hâa thûm", "ห้าทุ่ม", CAT, SUB, 3, "n",
 "Dwadzieścia trzy zero zero. Ostatnia godzina pory „thûm” — dalej jest już północ.",
 "pięć uderzenie",
 [("Bar zamyka o jedenastej.", "baa pìt hâa thûm khráp", "บาร์ปิดห้าทุ่มครับ"),
  ("Jest już jedenasta wieczorem.", "hâa thûm láew khráp", "ห้าทุ่มแล้วครับ")],
 ["dziesiąta wieczorem", "północ"], []),

("A1", "północ", "thîang khuen", "เที่ยงคืน", CAT, SUBP, 4, "n",
 "Dosłownie „południe nocy”. Ta sama część „thîang” co w południe, tylko z dopiskiem „khuen” (noc).",
 "południe noc",
 [("Wróciłem o północy.", "phǒm klàp thîang khuen khráp", "ผมกลับเที่ยงคืนครับ"),
  ("Pociąg jedzie o północy.", "rót fai àwk thîang khuen khráp", "รถไฟออกเที่ยงคืนครับ")],
 ["południe", "jedenasta wieczorem", "noc"], []),

# ============================================================ minuty i ulamki
("A1", "wpół do (i pół)", "khrûeng", "ครึ่ง", CAT, SUB, 5, "n",
 "PO TAJSKU NIE MA „WPÓŁ DO”. Połowa dokłada się ZA godziną: „bàai mohng khrûeng” to trzynasta trzydzieści, dosłownie „pierwsza po południu i pół”. Polskie „wpół do drugiej” trzeba przeliczyć na „pierwsza i pół”.",
 "połowa",
 [("Spotkajmy się o wpół do drugiej.", "jòoe kan bàai mohng khrûeng khráp", "เจอกันบ่ายโมงครึ่งครับ"),
  ("Jest wpół do dziewiątej rano.", "pàet mohng khrûeng khráp", "แปดโมงครึ่งครับ"),
  ("Wracam o wpół do ósmej wieczorem.", "phǒm klàp nùeng thûm khrûeng khráp", "ผมกลับหนึ่งทุ่มครึ่งครับ")],
 ["godzina (jednostka)", "kwadrans", "punktualnie"], ["i pół"]),

("A2", "kwadrans", "sìp-hâa naa-thii", "สิบห้านาที", CAT, SUB, 4, "n",
 "Tajski nie ma osobnego słowa na kwadrans — mówi się wprost „piętnaście minut”. Godzinę podaje się jako „druga piętnaście”, nie „kwadrans po drugiej”.",
 "piętnaście minut",
 [("Za kwadrans druga.", "ìik sìp-hâa naa-thii jà bàai sǎwng mohng khráp", "อีกสิบห้านาทีจะบ่ายสองโมงครับ"),
  ("Kwadrans po dziesiątej.", "sìp mohng sìp-hâa naa-thii khráp", "สิบโมงสิบห้านาทีครับ"),
  ("Poczekaj kwadrans.", "raw sìp-hâa naa-thii khráp", "รอสิบห้านาทีครับ")],
 ["wpół do (i pół)", "minuta (jednostka)"], []),

("A2", "po (minutach po godzinie)", "mohng ... naa-thii", "โมง...นาที", CAT, SUB, 4, "n",
 "Minuty dokłada się po godzinie bez żadnego przyimka: „kâo mohng sǎam-sìp naa-thii” = dziewiąta trzydzieści. Polskie „po” nie ma odpowiednika.",
 "godzina minut",
 [("Jest dziewiąta dwadzieścia.", "kâo mohng yîi-sìp naa-thii khráp", "เก้าโมงยี่สิบนาทีครับ"),
  ("Autobus jest o siódmej czterdzieści.", "rót àwk jèt mohng sìi-sìp naa-thii khráp", "รถออกเจ็ดโมงสี่สิบนาทีครับ")],
 ["minuta (jednostka)", "za (ile do godziny)"], []),

("A2", "za (ile do godziny)", "ìik ... naa-thii jà", "อีก...นาทีจะ", CAT, SUB, 4, "n",
 "Konstrukcja „ìik X naa-thii jà Y” znaczy „za X minut będzie Y”. Tajski buduje to jako zapowiedź przyszłości, nie jako odejmowanie od godziny.",
 "jeszcze minut będzie",
 [("Za dziesięć minut będzie dziesiąta.", "ìik sìp naa-thii jà sìp mohng khráp", "อีกสิบนาทีจะสิบโมงครับ"),
  ("Za pięć minut wychodzimy.", "ìik hâa naa-thii rao jà pai khráp", "อีกห้านาทีเราจะไปครับ"),
  ("Za dwadzieścia minut będzie druga.", "ìik yîi-sìp naa-thii jà bàai sǎwng mohng khráp", "อีกยี่สิบนาทีจะบ่ายสองโมงครับ")],
 ["po (minutach po godzinie)", "minuta (jednostka)"], []),

("A2", "punktualnie", "trong", "ตรง", CAT, SUB, 4, "n",
 "Dokładany po godzinie: „bàai sǎwng mohng trong” to punkt czternasta. To samo słowo znaczy „prosto” przy wskazywaniu drogi.",
 "prosto, dokładnie",
 [("Spotkanie punktualnie o drugiej.", "prà-chum bàai sǎwng mohng trong khráp", "ประชุมบ่ายสองโมงตรงครับ"),
  ("Przyjdź punktualnie.", "maa hâi trong wee-laa khráp", "มาให้ตรงเวลาครับ")],
 ["około (godziny)", "wpół do (i pół)", "spóźnić się"], []),

("A2", "około (godziny)", "prà-maan", "ประมาณ", CAT, SUB, 5, "n",
 "Stawiany PRZED godziną: „prà-maan sǎam thûm” = koło dwudziestej pierwszej. Tego samego słowa używa się do przybliżania ceny i odległości.",
 "",
 [("Przyjdę około ósmej.", "phǒm jà maa prà-maan sǎwng thûm khráp", "ผมจะมาประมาณสองทุ่มครับ"),
  ("To zajmie około godziny.", "chái wee-laa prà-maan nùeng chûa-mohng khráp", "ใช้เวลาประมาณหนึ่งชั่วโมงครับ"),
  ("Kosztuje około stu batów.", "raa-khaa prà-maan nùeng ráwi bàat khráp", "ราคาประมาณหนึ่งร้อยบาทครับ")],
 ["punktualnie", "godzina (jednostka)"], []),

("A2", "godzina w systemie 24-godzinnym", "naa-lí-kaa", "นาฬิกา", CAT, SUB, 3, "f",
 "System oficjalny: „sìp-hâa naa-lí-kaa” to piętnasta. Usłyszysz go na dworcu, lotnisku i w radiu, ale w rozmowie brzmi sztucznie — tam używa się sześciu pór dnia. To samo słowo znaczy „zegar”.",
 "zegar",
 [("Pociąg odjeżdża o piętnastej trzydzieści.", "rót fai àwk sìp-hâa naa-lí-kaa sǎam-sìp naa-thii", "รถไฟออกสิบห้านาฬิกาสามสิบนาที"),
  ("Odprawa o dziewiętnastej.", "chék-in sìp-kâo naa-lí-kaa", "เช็คอินสิบเก้านาฬิกา")],
 ["zegarek", "godzina (jednostka)"], []),

("A1", "zegarek", "naa-lí-kaa khâw mue", "นาฬิกาข้อมือ", CAT, SUB, 3, "n",
 "Dosłownie „zegar na nadgarstku”. Samo „naa-lí-kaa” to zegar w ogóle.",
 "zegar nadgarstek",
 [("Mój zegarek się spóźnia.", "naa-lí-kaa phǒm doen cháa khráp", "นาฬิกาผมเดินช้าครับ"),
  ("Zapomniałem zegarka.", "phǒm luem naa-lí-kaa khráp", "ผมลืมนาฬิกาครับ")],
 ["godzina w systemie 24-godzinnym", "Która godzina?"], []),

("A2", "spóźnić się (na godzinę)", "maa sǎai", "มาสาย", CAT, SUB, 4, "n",
 "„sǎai” znaczy zarówno „późny ranek”, jak i „spóźniony”. Na spotkanie przychodzi się „sǎai”, a nie „cháa” — „cháa” to powolny.",
 "przyjść późno",
 [("Przepraszam, spóźniłem się.", "khǎw thôot khráp phǒm maa sǎai", "ขอโทษครับผมมาสาย"),
  ("On zawsze się spóźnia.", "kháo maa sǎai sà-mǒoe khráp", "เขามาสายเสมอครับ")],
 ["punktualnie", "późny ranek", "wcześnie"], []),

("A2", "wcześnie", "cháo", "เช้า", CAT, SUB, 4, "n",
 "To samo słowo co „rano”. „maa cháo” znaczy przyjść wcześnie, „tùen cháo” — wstać wcześnie.",
 "rano",
 [("Przyszedłem wcześnie.", "phǒm maa cháo khráp", "ผมมาเช้าครับ"),
  ("Wstaję wcześnie.", "phǒm tùen cháo khráp", "ผมตื่นเช้าครับ")],
 ["spóźnić się (na godzinę)", "rano"], []),
]
