# -*- coding: utf-8 -*-
"""Sesja F — GRAMATYKA UZYTKOWA: przyimki, wyrazenia miejsca, spojniki.

Uwaga systemowa o miejscu. Tajski buduje polozenie z dwoch klockow:
„khâang” (strona) albo „dâan” (kierunek) + kierunek. Stad khâang nâa
(przed), khâang lǎng (za), khâang bon (nad), khâang lâang (pod),
khâang nai (wewnatrz), khâang nâwk (na zewnatrz), khâang khâang (obok).
Kto opanuje ten schemat, nie musi uczyc sie kazdego przyimka osobno.

Druga uwaga: w tajskim czesto pomija sie spojnik „i” miedzy zdaniami,
a „kàp” laczy przede wszystkim rzeczowniki (kawa i herbata), nie zdania.
Do laczenia zdan sluzy „láew kâw” — i potem.
"""

GU = "Gramatyka użytkowa"
MO = "Miejsca i orientacja"

GRAM = [

# ============================================================ MIEJSCE
("A1", "wewnątrz", "khâang nai", "ข้างใน", MO, "Położenie", 4, "n",
 "Samo „nai” to przyimek „w”, a „khâang nai” to przysłówek miejsca — „w środku”.",
 "strona wewnątrz",
 [("Jest w środku.", "yùu khâang nai khráp", "อยู่ข้างในครับ"),
  ("Proszę wejść do środka.", "khâo khâang nai khráp", "เข้าข้างในครับ")],
 ["na zewnątrz", "wchodzić"], ["w środku"]),

("A1", "na zewnątrz", "khâang nâwk", "ข้างนอก", MO, "Położenie", 4, "n",
 "„kin khâao khâang nâwk” znaczy zjeść na mieście, poza domem.",
 "strona zewnątrz",
 [("Poczekam na zewnątrz.", "phǒm raw khâang nâwk khráp", "ผมรอข้างนอกครับ"),
  ("Jemy dziś na mieście.", "wan níi kin khâang nâwk khráp", "วันนี้กินข้างนอกครับ")],
 ["wewnątrz", "czekać"], []),

("A1", "przed (z przodu)", "khâang nâa", "ข้างหน้า", MO, "Położenie", 4, "n",
 "Uwaga: to samo wyrażenie w kontekście czasu znaczy „w przyszłości”, a „duean nâa” to przyszły miesiąc.",
 "strona twarz",
 [("Jest przed budynkiem.", "yùu khâang nâa tùek khráp", "อยู่ข้างหน้าตึกครับ"),
  ("Prosto przed siebie.", "trong pai khâang nâa khráp", "ตรงไปข้างหน้าครับ")],
 ["za (z tyłu)", "prosto"], ["z przodu"]),

("A1", "za (z tyłu)", "khâang lǎng", "ข้างหลัง", MO, "Położenie", 4, "n",
 "„lǎng” to plecy. To samo słowo zaczyna „lǎng-khaa” (dach) i „lǎng jàak” (po tym jak).",
 "strona plecy",
 [("Jest z tyłu.", "yùu khâang lǎng khráp", "อยู่ข้างหลังครับ"),
  ("Parking jest za budynkiem.", "thîi jàwt rót yùu khâang lǎng khráp", "ที่จอดรถอยู่ข้างหลังครับ")],
 ["przed (z przodu)", "parking", "plecy"], ["z tyłu"]),

("A1", "nad", "khâang bon", "ข้างบน", MO, "Położenie", 4, "n",
 "Samo „bon” to „na”. „khâang bon” znaczy też „na górze, na piętrze”.",
 "strona góra",
 [("Jest na górze.", "yùu khâang bon khráp", "อยู่ข้างบนครับ"),
  ("Połóż to na stole.", "waang bon tó khráp", "วางบนโต๊ะครับ")],
 ["pod", "piętro", "kłaść"], ["na górze"]),

("A1", "pod", "khâang lâang", "ข้างล่าง", MO, "Położenie", 4, "n",
 "„khâang lâang” znaczy też „na dole, na parterze” — częste w hotelu.",
 "strona dół",
 [("Śniadanie jest na dole.", "aa-hǎan cháo yùu khâang lâang khráp", "อาหารเช้าอยู่ข้างล่างครับ"),
  ("Jest pod stołem.", "yùu tâai tó khráp", "อยู่ใต้โต๊ะครับ")],
 ["nad", "parter", "śniadanie"], ["na dole"]),

("A2", "obok", "khâang khâang", "ข้างๆ", MO, "Położenie", 4, "n",
 "Powtórzenie „khâang khâang” daje sens „tuż obok”. Zapisywane też ze znakiem powtórzenia.",
 "strona strona",
 [("Bank jest obok.", "thá-naa-khaan yùu khâang khâang khráp", "ธนาคารอยู่ข้างๆครับ"),
  ("Usiądź obok mnie.", "nâng khâang khâang phǒm khráp", "นั่งข้างๆผมครับ")],
 ["blisko", "bank", "siedzieć"], []),

("A2", "pomiędzy", "rá-wàang", "ระหว่าง", MO, "Położenie", 3, "f",
 "To samo słowo w znaczeniu czasowym: „rá-wàang thîi” — podczas gdy.",
 "",
 [("Jest między bankiem a apteką.", "yùu rá-wàang thá-naa-khaan kàp ráan yaa khráp", "อยู่ระหว่างธนาคารกับร้านยาครับ"),
  ("Między drugą a trzecią.", "rá-wàang bàai sǎwng thǔeng bàai sǎam khráp", "ระหว่างบ่ายสองถึงบ่ายสามครับ")],
 ["obok", "podczas", "apteka"], ["między"]),

("A2", "naprzeciwko", "trong khâam", "ตรงข้าม", MO, "Położenie", 4, "n",
 "„trong” znaczy prosto, wprost. „khâam” to przechodzić na drugą stronę.",
 "wprost przechodzić",
 [("Jest naprzeciwko hotelu.", "yùu trong khâam roong raem khráp", "อยู่ตรงข้ามโรงแรมครับ"),
  ("Sklep jest po drugiej stronie.", "ráan yùu trong khâam khráp", "ร้านอยู่ตรงข้ามครับ")],
 ["przechodzić", "hotel", "obok"], ["po drugiej stronie"]),

("A2", "wokół", "râwp râwp", "รอบๆ", MO, "Położenie", 3, "n",
 "„râwp” samo znaczy „okrążenie, runda”: „nùeng râwp” to jedno okrążenie.",
 "",
 [("Rozejrzyj się wokół.", "duu râwp râwp khráp", "ดูรอบๆครับ"),
  ("Wokół domu jest ogród.", "râwp râwp bâan mii sǔan khráp", "รอบๆบ้านมีสวนครับ")],
 ["okolica", "ogród", "patrzeć"], ["dookoła"]),

("A2", "na końcu", "sùt", "สุด", MO, "Położenie", 3, "n",
 "„sùt thaang” to koniec drogi, „thîi sùt” tworzy stopień najwyższy: „dii thîi sùt” — najlepszy.",
 "",
 [("Jest na końcu korytarza.", "yùu sùt thaang doen khráp", "อยู่สุดทางเดินครับ"),
  ("To najlepsze.", "an níi dii thîi sùt khráp", "อันนี้ดีที่สุดครับ")],
 ["korytarz", "najlepszy", "koniec"], []),

("A2", "w rogu", "hǔa mum", "หัวมุม", MO, "Położenie", 3, "n",
 "Dosłownie „głowa kąta”. Częste przy wskazywaniu drogi taksówkarzowi.",
 "głowa kąt",
 [("Sklep jest na rogu.", "ráan yùu hǔa mum khráp", "ร้านอยู่หัวมุมครับ"),
  ("Zatrzymaj się na rogu.", "jàwt trong hǔa mum khráp", "จอดตรงหัวมุมครับ")],
 ["skręcać", "ulica", "zatrzymać"], ["na rogu"]),

("A2", "kierunek", "thít thaang", "ทิศทาง", MO, "Położenie", 3, "f",
 "Strony świata: nǔea (północ), tâai (południe), tà-wan àwk (wschód), tà-wan tòk (zachód).",
 "kierunek droga",
 [("W którym kierunku?", "thít thaang nǎi khráp", "ทิศทางไหนครับ"),
  ("Na północ stąd.", "thaang thít nǔea khráp", "ทางทิศเหนือครับ")],
 ["droga", "północ (kierunek)", "skręcać"], []),

# ============================================================ PRZYIMKI
("A1", "z (razem z)", "kàp", "กับ", GU, "Przyimki", 5, "n",
 "Łączy przede wszystkim rzeczowniki: „kaa-fae kàp chaa”. Do łączenia zdań służy „láew kâw”.",
 "",
 [("Idę z przyjacielem.", "phǒm pai kàp phûean khráp", "ผมไปกับเพื่อนครับ"),
  ("Kawa i herbata.", "kaa-fae kàp chaa khráp", "กาแฟกับชาครับ")],
 ["i (potem)", "przyjaciel", "razem"], []),

("A1", "dla", "hâi", "ให้", GU, "Przyimki", 5, "n",
 "„hâi” pełni trzy funkcje: dawać, dla kogoś, oraz „żeby” w prośbie: „chûai … hâi nòi”.",
 "dawać",
 [("To dla pana.", "an níi hâi khun khráp", "อันนี้ให้คุณครับ"),
  ("Zrobię to dla ciebie.", "phǒm tham hâi khráp", "ผมทำให้ครับ")],
 ["dawać", "prosić", "pomagać"], []),

("A2", "za pomocą", "dûai", "ด้วย", GU, "Przyimki", 4, "n",
 "„dûai” znaczy zarazem „też” i „narzędziem”. Na końcu prośby dodaje uprzejmości: „chûai … dûai khráp”.",
 "",
 [("Napisz długopisem.", "khǐan dûai pàak-kaa khráp", "เขียนด้วยปากกาครับ"),
  ("Ja też.", "phǒm dûai khráp", "ผมด้วยครับ")],
 ["także", "pisać", "prosić"], ["czym"]),

("A2", "od (miejsce)", "jàak", "จาก", GU, "Przyimki", 5, "n",
 "„maa jàak” to pochodzić skądś — jedno z pierwszych pytań przy poznaniu.",
 "",
 [("Jestem z Polski.", "phǒm maa jàak pra-thêet poo-laen khráp", "ผมมาจากประเทศโปแลนด์ครับ"),
  ("Skąd pan jest?", "khun maa jàak nǎi khráp", "คุณมาจากไหนครับ")],
 ["do (miejsce)", "przychodzić", "kraj"], []),

("A2", "do (aż do)", "thǔeng", "ถึง", GU, "Przyimki", 5, "n",
 "„thǔeng” to zarazem „dotrzeć” i „aż do”. Godziny otwarcia: „pòoet kâo moong thǔeng hâa moong yen”.",
 "docierać",
 [("Otwarte od dziewiątej do piątej.", "pòoet kâo moong thǔeng hâa moong yen khráp", "เปิดเก้าโมงถึงห้าโมงเย็นครับ"),
  ("Dojechałem na miejsce.", "phǒm thǔeng láew khráp", "ผมถึงแล้วครับ")],
 ["od (miejsce)", "docierać", "otwarty"], []),

("A2", "według", "taam", "ตาม", GU, "Przyimki", 3, "n",
 "„taam” znaczy też „podążać za kimś” i „zgodnie z”: „taam sà-baai” — jak wygodnie.",
 "podążać",
 [("Zrobię według instrukcji.", "phǒm tham taam khaam-ná-nam khráp", "ผมทำตามคำแนะนำครับ"),
  ("Jak pan woli.", "taam sà-baai khráp", "ตามสบายครับ")],
 ["podążać", "polecać"], []),

("A2", "o (na temat)", "kìao kàp", "เกี่ยวกับ", GU, "Przyimki", 4, "n",
 "„kìao” znaczy „dotyczyć, zahaczać”. „mâi kìao” to potoczne „to nie moja sprawa”.",
 "dotyczyć z",
 [("Rozmawiamy o pracy.", "rao khui kìao kàp ngaan khráp", "เราคุยเกี่ยวกับงานครับ"),
  ("To mnie nie dotyczy.", "mâi kìao kàp phǒm khráp", "ไม่เกี่ยวกับผมครับ")],
 ["rozmawiać", "praca"], ["na temat"]),

("A2", "bez", "mâi mii", "ไม่มี", GU, "Przyimki", 4, "n",
 "Tajski nie ma osobnego przyimka „bez” — używa się „mâi mii” (nie mieć) albo „mâi sài” (nie dodawać).",
 "nie mieć",
 [("Kawa bez cukru.", "kaa-fae mâi sài nám-taan khráp", "กาแฟไม่ใส่น้ำตาลครับ"),
  ("Pokój bez okna.", "hâwng mâi mii nâa-tàang khráp", "ห้องไม่มีหน้าต่างครับ")],
 ["mieć", "wkładać", "cukier"], []),

("A2", "oprócz", "nâwk jàak", "นอกจาก", GU, "Przyimki", 3, "f",
 "„nâwk jàak níi” to zwrot spajający wypowiedź — „poza tym”.",
 "poza od",
 [("Oprócz tego wszystko jest dobrze.", "nâwk jàak níi kâw dii khráp", "นอกจากนี้ก็ดีครับ"),
  ("Wszyscy oprócz mnie.", "thúk khon nâwk jàak phǒm khráp", "ทุกคนนอกจากผมครับ")],
 ["na zewnątrz", "wszyscy"], ["poza tym"]),

("A2", "zamiast", "thaen", "แทน", GU, "Przyimki", 3, "n",
 "„thaen” to także „zastępować kogoś”: „pai thaen phǒm” — idź zamiast mnie.",
 "",
 [("Poproszę herbatę zamiast kawy.", "khǎw chaa thaen kaa-fae khráp", "ขอชาแทนกาแฟครับ"),
  ("Pójdę zamiast niego.", "phǒm pai thaen kháo khráp", "ผมไปแทนเขาครับ")],
 ["wymieniać", "herbata", "kawa"], []),

# ============================================================ SPOJNIKI
("A1", "i (potem)", "láew kâw", "แล้วก็", GU, "Spójniki", 5, "p",
 "To spójnik do łączenia zdań i czynności, w odróżnieniu od „kàp”, które łączy rzeczowniki.",
 "już i",
 [("Zjem i pójdę.", "phǒm kin láew kâw pai khráp", "ผมกินแล้วก็ไปครับ"),
  ("Poproszę ryż i zupę.", "khǎw khâao láew kâw súp khráp", "ขอข้าวแล้วก็ซุปครับ")],
 ["z (razem z)", "potem"], []),

("A1", "ale", "tàe", "แต่", GU, "Spójniki", 5, "n",
 "Bardzo częste w mowie także jako samodzielne wtrącenie „tàe wâa” — ale.",
 "",
 [("Chcę, ale nie mam czasu.", "yàak pai tàe mâi mii wee-laa khráp", "อยากไปแต่ไม่มีเวลาครับ"),
  ("Dobre, ale drogie.", "dii tàe phaeng khráp", "ดีแต่แพงครับ")],
 ["chcieć", "czas", "drogi"], []),

("A1", "albo", "rǔe", "หรือ", GU, "Spójniki", 5, "n",
 "To samo słowo na końcu zdania tworzy pytanie: „pai rǔe” — idziesz czy nie?",
 "",
 [("Kawa albo herbata?", "kaa-fae rǔe chaa khráp", "กาแฟหรือชาครับ"),
  ("Dziś czy jutro?", "wan níi rǔe phrûng-níi khráp", "วันนี้หรือพรุ่งนี้ครับ")],
 ["kawa", "herbata", "pytać"], ["czy"]),

("A2", "ponieważ", "phráw wâa", "เพราะว่า", GU, "Spójniki", 5, "n",
 "Skracane w mowie do samego „phráw”. Odpowiada na pytanie „tham-mai” — dlaczego.",
 "ponieważ że",
 [("Nie idę, bo pada.", "phǒm mâi pai phráw fǒn tòk khráp", "ผมไม่ไปเพราะฝนตกครับ"),
  ("Dlaczego? Bo jest drogo.", "tham-mai khráp phráw phaeng khráp", "ทำไมครับ เพราะแพงครับ")],
 ["dlaczego", "deszcz", "drogi"], ["bo"]),

("A2", "dlatego", "loei", "เลย", GU, "Spójniki", 4, "p",
 "„loei” ma wiele funkcji: wzmacnia przeczenie („mâi châwp loei” — wcale nie lubię) i wprowadza skutek.",
 "",
 [("Padało, dlatego zostałem w domu.", "fǒn tòk loei yùu bâan khráp", "ฝนตกเลยอยู่บ้านครับ"),
  ("Wcale mi się nie podoba.", "mâi châwp loei khráp", "ไม่ชอบเลยครับ")],
 ["ponieważ", "deszcz", "dom"], ["więc"]),

("A2", "jeśli", "thâa", "ถ้า", GU, "Spójniki", 5, "n",
 "Zdanie warunkowe: „thâa … kâw …”. Słówko „kâw” w drugiej części jest niemal obowiązkowe.",
 "",
 [("Jeśli będzie padać, nie pójdziemy.", "thâa fǒn tòk kâw mâi pai khráp", "ถ้าฝนตกก็ไม่ไปครับ"),
  ("Jeśli można, poproszę okno.", "thâa dâai khǎw thîi nâng rim nâa-tàang khráp", "ถ้าได้ขอที่นั่งริมหน้าต่างครับ")],
 ["deszcz", "móc", "okno"], []),

("A2", "kiedy (gdy)", "tawn thîi", "ตอนที่", GU, "Spójniki", 4, "n",
 "„tawn” to odcinek czasu: tawn cháo (rano), tawn yen (wieczorem). „tawn thîi” wprowadza zdanie czasowe.",
 "moment który",
 [("Kiedy przyjechałem, padało.", "tawn thîi phǒm maa fǒn tòk khráp", "ตอนที่ผมมาฝนตกครับ"),
  ("Zadzwoń, kiedy dojedziesz.", "thoo maa tawn thǔeng ná khráp", "โทรมาตอนถึงนะครับ")],
 ["rano", "wieczór", "dzwonić"], ["gdy"]),

("A2", "zanim", "kàwn thîi jà", "ก่อนที่จะ", GU, "Spójniki", 3, "f",
 "„kàwn” samo znaczy „przedtem, najpierw”: „khǎw duu kàwn khráp” — najpierw popatrzę.",
 "przed który będzie",
 [("Zapłać, zanim wyjdziesz.", "jàai kàwn thîi jà pai khráp", "จ่ายก่อนที่จะไปครับ"),
  ("Najpierw się zastanowię.", "khǎw khít duu kàwn khráp", "ขอคิดดูก่อนครับ")],
 ["po tym jak", "płacić", "myśleć"], []),

("A2", "po tym jak", "lǎng jàak", "หลังจาก", GU, "Spójniki", 3, "f",
 "„lǎng jàak nán” to „potem, następnie” — przydatne przy opowiadaniu.",
 "po od",
 [("Po pracy idę do domu.", "lǎng jàak lôoek ngaan phǒm klàp bâan khráp", "หลังจากเลิกงานผมกลับบ้านครับ"),
  ("A potem?", "lǎng jàak nán lâ khráp", "หลังจากนั้นล่ะครับ")],
 ["zanim", "praca", "wracać"], ["potem"]),

("A2", "chociaż", "thǔeng mâe wâa", "ถึงแม้ว่า", GU, "Spójniki", 2, "f",
 "Rejestr formalny, typowy dla pisma. W mowie częściej samo „tàe”.",
 "aż nawet że",
 [("Chociaż jest drogo, kupię.", "thǔeng mâe wâa phaeng phǒm kâw jà súe khráp", "ถึงแม้ว่าแพงผมก็จะซื้อครับ"),
  ("Chociaż padało, poszliśmy.", "thǔeng mâe wâa fǒn tòk rao kâw pai khráp", "ถึงแม้ว่าฝนตกเราก็ไปครับ")],
 ["ale", "drogi", "kupować"], ["mimo że"]),

("A2", "więc (w takim razie)", "ngán", "งั้น", GU, "Spójniki", 4, "p",
 "Bardzo częste w mowie potocznej przy podejmowaniu decyzji: „ngán ao an níi” — w takim razie wezmę to.",
 "",
 [("W takim razie wezmę to.", "ngán ao an níi khráp", "งั้นเอาอันนี้ครับ"),
  ("W takim razie jutro.", "ngán phrûng-níi ná khráp", "งั้นพรุ่งนี้นะครับ")],
 ["dlatego", "brać", "jutro"], ["w takim razie"]),

("A2", "poza tym", "ìik yàang", "อีกอย่าง", GU, "Spójniki", 3, "p",
 "Dosłownie „jeszcze jedna rzecz” — wprowadza dodatkowy argument w rozmowie.",
 "jeszcze rodzaj",
 [("Poza tym jest za drogo.", "ìik yàang kâw phaeng koen pai khráp", "อีกอย่างก็แพงเกินไปครับ"),
  ("I jeszcze jedno.", "ìik yàang nùeng khráp", "อีกอย่างหนึ่งครับ")],
 ["oprócz", "drogi", "jeszcze"], []),

("A2", "to znaczy", "mǎai khwaam wâa", "หมายความว่า", GU, "Spójniki", 4, "n",
 "Kluczowe przy nieporozumieniu: „mǎai khwaam wâa à-rai khráp” — co to znaczy?",
 "znaczyć treść że",
 [("Co to znaczy?", "mǎai khwaam wâa à-rai khráp", "หมายความว่าอะไรครับ"),
  ("To znaczy, że jest zamknięte.", "mǎai khwaam wâa pìt khráp", "หมายความว่าปิดครับ")],
 ["rozumieć", "tłumaczyć", "zamknięty"], ["czyli"]),

("A2", "na przykład", "tua yàang chên", "ตัวอย่างเช่น", GU, "Spójniki", 3, "f",
 "„tua yàang” samo znaczy „przykład, próbka”. W mowie wystarcza samo „chên”.",
 "sztuka rodzaj jak",
 [("Na przykład to.", "tua yàang chên an níi khráp", "ตัวอย่างเช่นอันนี้ครับ"),
  ("Czy jest próbka?", "mii tua yàang mǎi khráp", "มีตัวอย่างไหมครับ")],
 ["jak (podobnie)", "pokazywać"], []),
]
