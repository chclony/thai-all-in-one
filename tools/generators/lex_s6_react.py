# -*- coding: utf-8 -*-
"""Leksyka etapu 6 — reakcje rozmowcy i laczenie zdan.

Etap 4 dodal 146 reakcji na poziomie B1. Ten zestaw dokłada reakcje krotsze
i lzejsze — takie, ktore padaja co kilkanascie sekund w zwyklej rozmowie —
oraz spojniki i zwroty organizujace dluzsza wypowiedz.

Krotka: (poziom, polski, fonetyka, tajski, kategoria, podkategoria, typ,
         freq, rejestr, notatka, znaczenie doslowne, przyklad)
"""

REACT = [

# =====================================================================
# POTWIERDZENIE I ZROZUMIENIE
# =====================================================================
("A2", "aha, rozumiem", "âw khrap", "อ๋อครับ", "Small talk", "Reakcje", "phrase", 5, "n",
 "„âw” to dźwięk olśnienia. Bez „khráp” zabrzmi zdawkowo.", "",
 ("Aha, teraz rozumiem.", "âw khráp tawn níi khâo jai láew", "อ๋อครับ ตอนนี้เข้าใจแล้ว")),
("A2", "no tak", "nân sì", "นั่นสิ", "Small talk", "Reakcje", "phrase", 4, "p",
 "Zgoda z odcieniem „sam to zauważyłem”. Bardzo częste między znajomymi.", "",
 ("No tak, masz rację.", "nân sì khun phûut thùuk", "นั่นสิ คุณพูดถูก")),
("A2", "właśnie", "chái loei", "ใช่เลย", "Small talk", "Reakcje", "phrase", 4, "i",
 "Mocne potwierdzenie: rozmówca trafił w sedno.", "tak wcale",
 ("Właśnie o to chodzi!", "chái loei nân lâe khráp", "ใช่เลย นั่นแหละครับ")),
("A2", "no dobrze", "kâw dâai", "ก็ได้", "Small talk", "Reakcje", "phrase", 5, "n",
 "Zgoda bez entuzjazmu — akceptujesz, choć wolałbyś inaczej. Ton głosu decyduje o wydźwięku.", "też móc",
 ("No dobrze, niech będzie.", "kâw dâai khráp taam nán", "ก็ได้ครับ ตามนั้น")),
("A2", "jasne", "dâai loei", "ได้เลย", "Small talk", "Reakcje", "phrase", 5, "n",
 "Zgoda pełna i chętna — przeciwieństwo „kâw dâai”.", "móc wcale",
 ("Jasne, zrobię to.", "dâai loei khráp phǒm jà tham hâi", "ได้เลยครับ ผมจะทำให้")),
("A2", "no proszę", "hǎa", "หา", "Small talk", "Reakcje", "phrase", 3, "p",
 "Krótki wyraz zaskoczenia. W rozmowie formalnej zabrzmi opryskliwie.", "",
 ("No proszę, nie wiedziałem.", "hǎa phǒm mâi rúu maa kàwn loei", "หา ผมไม่รู้มาก่อนเลย")),
("B1", "rzeczywiście tak jest", "kâw jing", "ก็จริง", "Small talk", "Reakcje", "phrase", 3, "n",
 "Przyznanie racji z zastrzeżeniem, że to nie cała prawda. Często poprzedza „tàe …”.", "też prawda",
 ("Rzeczywiście, ale to jeszcze nie wszystko.", "kâw jing khráp tàe yang mâi mòt", "ก็จริงครับ แต่ยังไม่หมด")),
("B1", "tak też myślałem", "khít wái yàang nán lǒoe", "คิดไว้อย่างนั้นเหมือนกัน", "Small talk", "Reakcje", "phrase", 3, "n",
 "Sygnalizuje zgodność bez przechwalania się, że wiedziałeś pierwszy.", "myśleć zostawić tak samo",
 ("Ja też tak myślałem.", "phǒm khít wái yàang nán lǒoe kan khráp", "ผมคิดไว้อย่างนั้นเหมือนกันครับ")),

# =====================================================================
# ZASKOCZENIE I NIEDOWIERZANIE
# =====================================================================
("A2", "naprawdę?", "jing rǒoe", "จริงเหรอ", "Small talk", "Reakcje", "question", 5, "i",
 "Najczęstsza reakcja zaskoczenia. Wersja grzeczna to „jing rǔe khráp”.", "prawda czy",
 ("Naprawdę? Nie wiedziałem.", "jing rǒoe phǒm mâi rúu loei", "จริงเหรอ ผมไม่รู้เลย")),
("A2", "coś takiego!", "yàang níi níi eeng", "อย่างนี้นี่เอง", "Small talk", "Reakcje", "phrase", 3, "n",
 "Reakcja na wyjaśnienie, które właśnie wszystko poukładało.", "tak to samo",
 ("Aha, więc to tak!", "âw yàang níi níi eeng khráp", "อ๋อ อย่างนี้นี่เองครับ")),
("A2", "niemożliwe", "pen pai mâi dâai", "เป็นไปไม่ได้", "Small talk", "Reakcje", "phrase", 3, "n",
 "Mocne zaprzeczenie. Wobec przełożonego lepiej „khong yâak nòi ná khráp”.", "iść nie móc",
 ("To niemożliwe, sprawdzę jeszcze raz.", "pen pai mâi dâai khráp dǐao phǒm chék ìik thii", "เป็นไปไม่ได้ครับ เดี๋ยวผมเช็คอีกที")),
("B1", "nie do wiary", "mâi nâa chûea loei", "ไม่น่าเชื่อเลย", "Small talk", "Reakcje", "phrase", 3, "n",
 "Wyraża podziw albo niedowierzanie — zależnie od intonacji.", "nie warto wierzyć wcale",
 ("Nie do wiary, że tak szybko!", "mâi nâa chûea loei rew khà-nàat níi", "ไม่น่าเชื่อเลย เร็วขนาดนี้")),
("B1", "też mnie to zaskoczyło", "phǒm kâw tòk jai mǔean kan", "ผมก็ตกใจเหมือนกัน", "Small talk", "Reakcje", "phrase", 3, "n",
 "„tòk jai” to nagły przestrach lub zaskoczenie — dosłownie „serce spadło”.", "ja też spaść serce tak samo",
 ("Mnie też to zaskoczyło.", "phǒm kâw tòk jai mǔean kan khráp", "ผมก็ตกใจเหมือนกันครับ")),

# =====================================================================
# WSPOLODCZUWANIE
# =====================================================================
("A2", "współczuję", "sǐa jai dûai", "เสียใจด้วย", "Small talk", "Reakcje", "phrase", 4, "n",
 "Formuła kondolencji i wyrazów współczucia. „dûai” znaczy tu „razem z tobą”.", "smutno razem",
 ("Bardzo mi przykro.", "sǐa jai dûai ná khráp", "เสียใจด้วยนะครับ")),
("A2", "trzymaj się", "sûu sûu", "สู้ๆ", "Small talk", "Reakcje", "phrase", 5, "i",
 "Dosłownie „walcz, walcz”. Najczęstsze tajskie dodanie otuchy — używane wszędzie.", "walczyć walczyć",
 ("Trzymaj się, dasz radę!", "sûu sûu ná tham dâai nâe nawn", "สู้ๆ นะ ทำได้แน่นอน")),
("A2", "to musiało być trudne", "khong nùeai mâak loei", "คงเหนื่อยมากเลย", "Small talk", "Reakcje", "phrase", 3, "n",
 "„khong” to przypuszczenie. Bez niego zdanie brzmi jak stwierdzenie za rozmówcę.", "pewnie zmęczony bardzo",
 ("Musiałeś być bardzo zmęczony.", "khong nùeai mâak loei ná khráp", "คงเหนื่อยมากเลยนะครับ")),
("B1", "rozumiem, co czujesz", "khâo jai khwaam rúu-sùek", "เข้าใจความรู้สึก", "Small talk", "Reakcje", "phrase", 3, "n",
 "Krótka forma bez zaimka jest naturalniejsza niż pełne zdanie z „khun”.", "wejść serce uczucie",
 ("Rozumiem, jak się czujesz.", "phǒm khâo jai khwaam rúu-sùek khráp", "ผมเข้าใจความรู้สึกครับ")),
("B1", "nie martw się tym", "mâi tâwng kang-won", "ไม่ต้องกังวล", "Small talk", "Reakcje", "phrase", 4, "n",
 "„mâi tâwng” = nie musisz. To łagodniejsze niż „yàa” (nie rób).", "nie trzeba martwić się",
 ("Nie martw się, załatwimy to.", "mâi tâwng kang-won ná khráp dǐao jàt kaan hâi", "ไม่ต้องกังวลนะครับ เดี๋ยวจัดการให้")),
("B1", "cieszę się razem z tobą", "dii jai dûai", "ดีใจด้วย", "Small talk", "Reakcje", "phrase", 4, "n",
 "Standardowe gratulacje — krótsze i cieplejsze niż „yin dii dûai”.", "cieszyć się razem",
 ("Gratulacje, cieszę się!", "yin dii dûai ná khráp dii jai dûai jing jing", "ยินดีด้วยนะครับ ดีใจด้วยจริงๆ")),

# =====================================================================
# PODTRZYMYWANIE ROZMOWY
# =====================================================================
("A2", "no i co dalej?", "láew ngai tàw", "แล้วไงต่อ", "Small talk", "Reakcje", "question", 4, "i",
 "Zachęta do kontynuowania opowieści. Między znajomymi, nie w biurze.", "potem jak dalej",
 ("No i co było dalej?", "láew ngai tàw lâ", "แล้วไงต่อล่ะ")),
("A2", "mów dalej", "phûut tàw dâai loei", "พูดต่อได้เลย", "Small talk", "Reakcje", "phrase", 3, "n",
 "Uprzejme oddanie głosu rozmówcy, gdy się zawahał.", "mówić dalej móc wcale",
 ("Proszę mówić dalej.", "chooen phûut tàw dâai loei khráp", "เชิญพูดต่อได้เลยครับ")),
("A2", "słucham cię", "fang yùu khráp", "ฟังอยู่ครับ", "Small talk", "Reakcje", "phrase", 4, "n",
 "„yùu” sygnalizuje czynność trwającą — słucham właśnie teraz.", "słuchać przebywać",
 ("Słucham, proszę mówić.", "fang yùu khráp chooen khráp", "ฟังอยู่ครับ เชิญครับ")),
("B1", "a przy okazji", "wâa tàe", "ว่าแต่", "Small talk", "Prowadzenie rozmowy", "phrase", 4, "n",
 "Zmienia temat bez urażania rozmówcy — sygnalizuje, że robisz to świadomie.", "mówić ale",
 ("A przy okazji, jak tam praca?", "wâa tàe ngaan pen yang-ngai bâang khráp", "ว่าแต่ งานเป็นยังไงบ้างครับ")),
("B1", "wracając do tematu", "klàp maa thîi rûeang dooem", "กลับมาที่เรื่องเดิม", "Small talk", "Prowadzenie rozmowy", "phrase", 3, "n",
 "Przydaje się po dygresji — grzecznie przywraca główny wątek.", "wrócić przyjść do sprawa poprzednia",
 ("Wracając do tematu, co dalej?", "klàp maa thîi rûeang dooem ná khráp tàw pai yang-ngai", "กลับมาที่เรื่องเดิมนะครับ ต่อไปยังไง")),
("B1", "krótko mówiąc", "phûut sân sân", "พูดสั้นๆ", "Small talk", "Prowadzenie rozmowy", "phrase", 3, "n",
 "Zapowiada streszczenie. W biurze bardzo pożądany sygnał.", "mówić krótko krótko",
 ("Krótko mówiąc, nie zdążymy.", "phûut sân sân khue raw jà mâi than khráp", "พูดสั้นๆ คือเราจะไม่ทันครับ")),

# =====================================================================
# SPOJNIKI I LACZENIE ZDAN
# =====================================================================
("A2", "dlatego", "phráw chà-nán", "เพราะฉะนั้น", "Gramatyka użytkowa", "Spójniki", "phrase", 4, "n",
 "Otwiera wniosek. Wersja krótsza to samo „chà-nán”.", "ponieważ tak",
 ("Padało, dlatego się spóźniłem.", "fǒn tòk phráw chà-nán phǒm maa sǎai khráp", "ฝนตก เพราะฉะนั้นผมมาสายครับ")),
("A2", "ponieważ", "phráw wâa", "เพราะว่า", "Gramatyka użytkowa", "Spójniki", "phrase", 5, "n",
 "„phráw wâa” otwiera przyczynę. W mowie często skraca się do „phráw”.", "ponieważ że",
 ("Nie przyjdę, bo jestem chory.", "phǒm mâi pai phráw wâa mâi sà-baai khráp", "ผมไม่ไปเพราะว่าไม่สบายครับ")),
("A2", "poza tym", "nâwk jàak nán", "นอกจากนั้น", "Gramatyka użytkowa", "Spójniki", "phrase", 3, "n",
 "Dokłada argument do już podanego.", "poza od tego",
 ("Poza tym jest za drogo.", "nâwk jàak nán yang phaeng ìik khráp", "นอกจากนั้นยังแพงอีกครับ")),
("A2", "na przykład", "chên", "เช่น", "Gramatyka użytkowa", "Spójniki", "phrase", 4, "n",
 "Wprowadza wyliczenie. Wersja pełna to „yàang chên”.", "",
 ("Na przykład owoce i woda.", "chên phǒn-lá-mái láe náam khráp", "เช่น ผลไม้และน้ำครับ")),
("A2", "albo, lub", "rǔe", "หรือ", "Gramatyka użytkowa", "Spójniki", "phrase", 5, "n",
 "„rǔe” łączy opcje, a na końcu zdania zmienia je w pytanie.", "",
 ("Kawa czy herbata?", "kaa-fae rǔe chaa khráp", "กาแฟหรือชาครับ")),
("B1", "mimo to", "thǔeng yàang nán", "ถึงอย่างนั้น", "Gramatyka użytkowa", "Spójniki", "phrase", 3, "n",
 "Wprowadza kontrast wobec własnego zdania — sygnał dojrzałej wypowiedzi.", "aż tak",
 ("Było drogo, mimo to warto.", "phaeng khráp thǔeng yàang nán kâw khúm", "แพงครับ ถึงอย่างนั้นก็คุ้ม")),
("B1", "z jednej strony", "nai dâan nùeng", "ในด้านหนึ่ง", "Gramatyka użytkowa", "Spójniki", "phrase", 2, "f",
 "Otwiera wyważoną ocenę. Druga część to „ìik dâan nùeng”.", "w stronę jedna",
 ("Z jednej strony jest tanio.", "nai dâan nùeng raa-khaa thùuk khráp", "ในด้านหนึ่งราคาถูกครับ")),
("B1", "po pierwsze", "yàang râek", "อย่างแรก", "Gramatyka użytkowa", "Spójniki", "phrase", 3, "n",
 "Porządkuje argumenty. Dalej idzie „yàang thîi sǎwng”.", "sposób pierwszy",
 ("Po pierwsze, jest za późno.", "yàang râek man sǎai koen pai khráp", "อย่างแรก มันสายเกินไปครับ")),
("B1", "podsumowując", "sà-rùp láew", "สรุปแล้ว", "Gramatyka użytkowa", "Spójniki", "phrase", 3, "n",
 "Sygnał zamykania wypowiedzi — bardzo częsty na zebraniach.", "podsumować już",
 ("Podsumowując, zgadzamy się.", "sà-rùp láew raw tòk long khráp", "สรุปแล้วเราตกลงครับ")),
("B1", "innymi słowy", "phûut ìik yàang", "พูดอีกอย่าง", "Gramatyka użytkowa", "Spójniki", "phrase", 3, "n",
 "Wprowadza parafrazę, gdy pierwsze sformułowanie nie trafiło.", "mówić jeszcze sposób",
 ("Innymi słowy, to za mało.", "phûut ìik yàang khue man nói koen pai khráp", "พูดอีกอย่างคือมันน้อยเกินไปครับ")),
("B1", "chyba że", "nâwk sǐa jàak wâa", "นอกเสียจากว่า", "Gramatyka użytkowa", "Spójniki", "phrase", 2, "f",
 "Wprowadza jedyny wyjątek od reguły. Formalne, dobre przy ustaleniach.", "poza stracić od że",
 ("Nie przyjdę, chyba że przestanie padać.", "phǒm mâi pai nâwk sǐa jàak wâa fǒn yùt khráp", "ผมไม่ไปนอกเสียจากว่าฝนหยุดครับ")),
("B1", "zależy od tego, czy", "khûen yùu kàp wâa", "ขึ้นอยู่กับว่า", "Gramatyka użytkowa", "Spójniki", "phrase", 4, "n",
 "Najuczciwsza odpowiedź, gdy nie chcesz obiecywać. Bardzo częsta w negocjacjach.", "wznieść przebywać z że",
 ("To zależy od pogody.", "khûen yùu kàp aa-kàat khráp", "ขึ้นอยู่กับอากาศครับ")),

# =====================================================================
# LAGODZENIE I ZASTRZEZENIA
# =====================================================================
("B1", "jeśli dobrze rozumiem", "thâa phǒm khâo jai mâi phìt", "ถ้าผมเข้าใจไม่ผิด", "Small talk", "Sprawdzanie", "phrase", 3, "f",
 "Sprawdza zrozumienie bez sugerowania, że rozmówca mówił niejasno.", "jeśli ja rozumieć nie źle",
 ("Jeśli dobrze rozumiem, płacimy jutro.", "thâa phǒm khâo jai mâi phìt raw jàai phrûng-níi khráp", "ถ้าผมเข้าใจไม่ผิด เราจ่ายพรุ่งนี้ครับ")),
("B1", "moim zdaniem", "nai khwaam khít khǎwng phǒm", "ในความคิดของผม", "Cechy i opinie", "Opinie", "phrase", 3, "f",
 "Wersja formalna. Potocznie wystarczy „phǒm wâa”.", "w myśl moja",
 ("Moim zdaniem to za drogo.", "nai khwaam khít khǎwng phǒm man phaeng koen pai khráp", "ในความคิดของผมมันแพงเกินไปครับ")),
("B1", "nie jestem pewien, ale", "mâi nâe jai tàe wâa", "ไม่แน่ใจแต่ว่า", "Cechy i opinie", "Opinie", "phrase", 4, "n",
 "Zabezpiecza przed odpowiedzialnością za nieścisłą informację — bardzo tajski nawyk.", "nie pewny ale że",
 ("Nie jestem pewien, ale chyba zamknięte.", "mâi nâe jai tàe wâa nâa jà pìt láew khráp", "ไม่แน่ใจแต่ว่าน่าจะปิดแล้วครับ")),
("B1", "o ile wiem", "thâo thîi rúu", "เท่าที่รู้", "Cechy i opinie", "Opinie", "phrase", 3, "n",
 "Ogranicza twoją wypowiedź do własnej wiedzy — grzecznie i bezpiecznie.", "tyle co wiedzieć",
 ("O ile wiem, jest otwarte do szóstej.", "thâo thîi rúu pòet thǔeng hòk mohng yen khráp", "เท่าที่รู้เปิดถึงหกโมงเย็นครับ")),
("B1", "z tego, co słyszałem", "thâo thîi dâai yin maa", "เท่าที่ได้ยินมา", "Cechy i opinie", "Opinie", "phrase", 3, "n",
 "Wyraźnie oddziela plotkę od wiedzy własnej.", "tyle co usłyszeć przyjść",
 ("Z tego, co słyszałem, będzie taniej.", "thâo thîi dâai yin maa jà thùuk long khráp", "เท่าที่ได้ยินมาจะถูกลงครับ")),
("B1", "raczej nie", "khong mâi ná", "คงไม่นะ", "Small talk", "Reakcje", "phrase", 4, "n",
 "Miękka odmowa. „khong” zostawia furtkę i chroni twarz obu stron.", "pewnie nie",
 ("Raczej nie dam rady dziś.", "wan níi khong mâi wǎai ná khráp", "วันนี้คงไม่ไหวนะครับ")),
("B1", "być może", "àat jà", "อาจจะ", "Cechy i opinie", "Opinie", "phrase", 4, "n",
 "„àat jà” stoi przed czasownikiem. To najczęstszy tajski sposób na „może”.", "może będzie",
 ("Być może przyjdę później.", "phǒm àat jà maa thii lǎng khráp", "ผมอาจจะมาทีหลังครับ")),
("B1", "szczerze mówiąc", "phûut trong trong", "พูดตรงๆ", "Small talk", "Prowadzenie rozmowy", "phrase", 3, "n",
 "Zapowiada szczerość, która może zaboleć — w tajskiej rozmowie taki sygnał jest ważny.", "mówić prosto prosto",
 ("Szczerze mówiąc, wolałbym inaczej.", "phûut trong trong phǒm yàak dâai bàep ùen mâak kwàa khráp", "พูดตรงๆ ผมอยากได้แบบอื่นมากกว่าครับ")),
]
