# -*- coding: utf-8 -*-
"""Sesja O, partia 10 — ROZMOWA: spójniki, partykuły, reakcje, uczucia.

To partia, która odróżnia „mówię zdaniami” od „prowadzę rozmowę”. Trzy
warstwy:

1. **Spójniki i wskaźniki toku** — bo, chociaż, dlatego, poza tym, z drugiej
   strony. Kategoria Gramatyka użytkowa miała 89 haseł leksykalnych na
   1 668 rekordów: mnóstwo zdań wzorcowych i prawie żadnych cegiełek do
   budowania własnych.

2. **Partykuły końcowe** — `ná`, `sì`, `lâ`, `lâw`, `ròk`, `mâng`. Tajski
   niesie w nich to, co polski niesie intonacją i trybem: prośbę, naleganie,
   zdziwienie, złagodzenie. Zdanie bez partykuły jest gramatyczne i brzmi
   obcesowo. To najczęstszy powód, dla którego poprawnie mówiący cudzoziemiec
   wypada nieuprzejmie.

3. **Reakcje** — krótkie odpowiedzi, którymi podtrzymuje się rozmowę.
   Bez nich uczący się milczy między swoimi kwestiami i rozmowa umiera.

Uwaga o płci: partykuły grzecznościowe (khráp / khâ) mają wariant żeński
generowany automatycznie przez `gender_forms.py` — tu podaje się formę
męską, jak w całej bazie.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

GU = "Gramatyka użytkowa"
ST = "Small talk"
PG = "Podstawy i grzeczność"
PY = "Pytania"
CO = "Cechy i opinie"
LR = "Ludzie i rodzina"
CD = "Czas i daty"
AW = "Awarie i pomoc"

TALK = [

# =========================================================== spójniki
("A1", "bo, ponieważ", "phráw wâa", "เพราะว่า", "Spójniki", 5, "w", GU, "", ""),
("A1", "dlatego", "dang nán", "ดังนั้น", "Spójniki", 4, "w", GU, "", ""),
("A1", "więc, zatem", "kâw looei", "ก็เลย", "Spójniki", 5, "w", GU,
 "Najczęstszy spójnik tajskiej mowy potocznej — spina przyczynę ze skutkiem.", ""),
("A1", "chociaż", "thǔeng máe wâa", "ถึงแม้ว่า", "Spójniki", 3, "w", GU, "", ""),
("A1", "mimo to", "tàe kâw", "แต่ก็", "Spójniki", 4, "w", GU, "", ""),
("A1", "jeśli", "thâa", "ถ้า", "Spójniki", 5, "w", GU, "", ""),
("A1", "jeśli nie", "thâa mâi", "ถ้าไม่", "Spójniki", 4, "w", GU, "", ""),
("A1", "kiedy (w zdaniu)", "tawn thîi", "ตอนที่", "Spójniki", 5, "w", GU, "", ""),
("A1", "zanim", "kàwn thîi jà", "ก่อนที่จะ", "Spójniki", 4, "w", GU, "", ""),
("A1", "po tym jak", "lǎng jàak", "หลังจาก", "Spójniki", 4, "w", GU, "", ""),
("A1", "dopóki", "jon kwàa", "จนกว่า", "Spójniki", 3, "w", GU, "", ""),
("A1", "aż do", "jon thǔeng", "จนถึง", "Spójniki", 4, "w", GU, "", ""),
("A2", "poza tym", "nâwk jàak níi", "นอกจากนี้", "Spójniki", 4, "w", GU, "", "poza tym"),
("A2", "z drugiej strony", "ìik dâan nùeng", "อีกด้านหนึ่ง", "Spójniki", 3, "w", GU, "", ""),
("A2", "na przykład", "chên", "เช่น", "Spójniki", 5, "w", GU, "", ""),
("A2", "to znaczy", "mǎai khwaam wâa", "หมายความว่า", "Spójniki", 4, "w", GU, "", "znaczyć sens że"),
("A2", "innymi słowy", "phûut ìik yàang", "พูดอีกอย่าง", "Spójniki", 2, "w", GU, "", ""),
("A2", "w rzeczywistości", "thîi jing láew", "ที่จริงแล้ว", "Spójniki", 4, "w", GU, "", ""),
("A2", "przede wszystkim", "yàang râek", "อย่างแรก", "Spójniki", 3, "w", GU, "", "sposób pierwszy"),
("A2", "wreszcie, na koniec", "sùt tháai", "สุดท้าย", "Spójniki", 4, "w", GU, "", ""),
("A2", "zamiast", "thaen thîi jà", "แทนที่จะ", "Spójniki", 3, "w", GU, "", ""),
("A2", "oprócz", "nâwk jàak", "นอกจาก", "Spójniki", 4, "w", GU, "", ""),
("A2", "według (kogoś)", "taam", "ตาม", "Spójniki", 4, "w", GU,
 "To samo słowo znaczy „podążać za” — taam phǒm maa, chodź za mną.", ""),
("A2", "dzięki temu, że", "dûai khwaam thîi", "ด้วยความที่", "Spójniki", 2, "w", GU, "", ""),
("A2", "w takim razie", "thâa yàang nán", "ถ้าอย่างนั้น", "Spójniki", 4, "w", GU, "", ""),
("A2", "niezależnie od tego", "mâi wâa yàang rai", "ไม่ว่าอย่างไร", "Spójniki", 3, "w", GU, "", ""),

# =========================================================== partykuły końcowe
("A1", "…prawda? (łagodzące)", "ná khráp", "นะครับ", "Partykuły", 5, "w", PG,
 "Zmiękcza zdanie i prosi o przyzwolenie. Bez niej prośba brzmi jak rozkaz.", ""),
("A1", "…no dalej (zachęta)", "sì khráp", "สิครับ", "Partykuły", 4, "w", PG, "", ""),
("A1", "…a właściwie? (dopytanie)", "lâ khráp", "ล่ะครับ", "Partykuły", 5, "w", PY,
 "„A ty?” to „láew khun lâ khráp” — najkrótsze podtrzymanie rozmowy.", ""),
("A1", "…już (stan osiągnięty)", "láew khráp", "แล้วครับ", "Partykuły", 5, "w", GU, "", ""),
("A1", "…jeszcze nie", "yang khráp", "ยังครับ", "Partykuły", 5, "w", GU, "", ""),
("A1", "…przecież (zaprzeczenie)", "ròk khráp", "หรอกครับ", "Partykuły", 3, "w", GU,
 "mâi chái ròk — ależ skąd. Partykuła zaprzeczająca łagodnie.", ""),
("A1", "…chyba, może", "mâng khráp", "มั้งครับ", "Partykuły", 4, "w", GU, "", ""),
("A1", "…co? (zdziwienie)", "rǔe khráp", "หรือครับ", "Partykuły", 4, "w", PY, "", ""),
("A2", "…proszę (uprzejma prośba)", "nàwi khráp", "หน่อยครับ", "Partykuły", 5, "w", PG,
 "Dosłownie „troszkę”. Wstawiona do prośby zmniejsza ciężar tego, o co się prosi.", "troszkę"),
("A2", "…też, również", "dûai khráp", "ด้วยครับ", "Partykuły", 5, "w", GU, "", ""),
("A2", "…w ogóle, ani trochę", "looei khráp", "เลยครับ", "Partykuły", 5, "w", GU, "", ""),
("A2", "…dopiero co", "phôeng khráp", "เพิ่งครับ", "Partykuły", 4, "w", CD, "", ""),

# =========================================================== reakcje
("A1", "Aha, rozumiem.", "áa khâo jai láew", "อ๋อเข้าใจแล้ว", "Reakcje", 5, "w", ST, "", ""),
("A1", "Naprawdę?", "jing rǔe", "จริงหรือ", "Reakcje", 5, "w", ST, "", ""),
("A1", "No właśnie.", "nân ná sì", "นั่นนะสิ", "Reakcje", 4, "w", ST, "", ""),
("A1", "Zgadza się.", "thùuk láew", "ถูกแล้ว", "Reakcje", 5, "w", ST,
 "thùuk znaczy też „tanio” — thùuk láew w sklepie może być pochwałą ceny.", ""),
("A1", "Nie sądzę.", "mâi khít yàang nán", "ไม่คิดอย่างนั้น", "Reakcje", 4, "w", ST, "", ""),
("A1", "Możliwe.", "pen pai dâi", "เป็นไปได้", "Reakcje", 4, "w", ST, "", "może się zdarzyć"),
("A1", "Niemożliwe.", "pen pai mâi dâi", "เป็นไปไม่ได้", "Reakcje", 3, "w", ST, "", ""),
("A1", "Nie wiedziałem.", "mâi rúu maa kàwn", "ไม่รู้มาก่อน", "Reakcje", 4, "w", ST, "", ""),
("A1", "To ciekawe.", "nâa sǒn jai ná", "น่าสนใจนะ", "Reakcje", 4, "w", ST, "", ""),
("A1", "Szkoda.", "nâa sǐa daai", "น่าเสียดายจัง", "Reakcje", 4, "w", ST, "", ""),
("A1", "Gratulacje!", "yin dii dûai", "ยินดีด้วย", "Reakcje", 4, "w", PG, "", ""),
("A1", "Powodzenia!", "chôok dii", "โชคดี", "Reakcje", 5, "w", PG, "", "szczęście dobre"),
("A1", "Uważaj na siebie.", "duu lae tua eeng dûai", "ดูแลตัวเองด้วย", "Reakcje", 4, "w", PG, "", ""),
("A1", "Nic się nie stało.", "mâi pen rai", "ไม่เป็นไร", "Reakcje", 5, "w", PG,
 "Najważniejsze zdanie tajskiej kultury. Znaczy naraz: nie ma sprawy, spoko, nieważne, proszę bardzo.", ""),
("A2", "Bez pośpiechu.", "mâi tâwng rîip", "ไม่ต้องรีบ", "Reakcje", 4, "w", ST, "", ""),
("A2", "Zależy.", "láew tàe", "แล้วแต่", "Reakcje", 5, "w", ST,
 "„láew tàe khun” — jak wolisz. Odpowiedź uprzejmie przerzucająca wybór.", ""),
("A2", "Jak wolisz.", "láew tàe khun", "แล้วแต่คุณ", "Reakcje", 5, "w", ST, "", ""),
("A2", "Zgadzam się.", "hěn dûai", "เห็นด้วย", "Reakcje", 5, "w", ST, "", "widzieć razem"),
("A2", "Nie zgadzam się.", "mâi hěn dûai", "ไม่เห็นด้วย", "Reakcje", 4, "w", ST, "", ""),
("A2", "Chwileczkę.", "sàk khrûu", "สักครู่", "Reakcje", 5, "w", PG, "", ""),
("A2", "Już idę.", "maa láew", "มาแล้ว", "Reakcje", 5, "w", ST, "", ""),
("A2", "Nie ma problemu.", "mâi mii pan-hǎa", "ไม่มีปัญหา", "Reakcje", 5, "w", ST, "", ""),
("A2", "Zapomnijmy o tym.", "luem man sá", "ลืมมันซะ", "Reakcje", 2, "w", ST, "", ""),
("A2", "Dobra robota.", "kèng mâak", "เก่งมาก", "Reakcje", 5, "w", ST,
 "kèng to „zdolny, dobry w czymś” — jedna z najczęstszych pochwał.", ""),
("A2", "Trzymaj się.", "sûu sûu", "สู้ๆ", "Reakcje", 5, "w", ST,
 "Dosłownie „walcz, walcz”. Tajskie „dasz radę”, mówione przed egzaminem i w pracy.", "walcz walcz"),
("A2", "Spokojnie.", "jai yen yen", "ใจเย็นๆ", "Reakcje", 5, "w", ST, "", "serce chłodne chłodne"),
("A2", "Nieważne.", "mâi sǎm-khan ròk", "ไม่สำคัญหรอก", "Reakcje", 3, "w", ST, "", ""),
("A2", "Skąd wiesz?", "rúu dâi yang ngai", "รู้ได้ยังไง", "Reakcje", 4, "w", PY, "", ""),
("A2", "Co masz na myśli?", "mǎai khwaam wâa yang ngai", "หมายความว่ายังไง", "Reakcje", 4, "w", PY, "", ""),
("A2", "Możesz powtórzyć?", "phûut ìik thii dâi mǎi", "พูดอีกทีได้ไหม", "Reakcje", 5, "w", PY, "", ""),
("A2", "Nie nadążam.", "taam mâi than", "ตามไม่ทัน", "Reakcje", 4, "w", ST, "", "podążać nie zdążyć"),

# =========================================================== uczucia i opinie
("A1", "być wdzięcznym", "sǔuk sùeng", "ซาบซึ้ง", "Uczucia", 2, "v", ST, "", ""),
("A1", "być rozczarowanym", "phìt wǎng", "ผิดหวัง", "Uczucia", 3, "v", ST, "", "chybić nadzieja"),
("A1", "być zaskoczonym", "plàek jai", "แปลกใจ", "Uczucia", 3, "v", ST, "", ""),
("A1", "być zdenerwowanym", "tùen tên", "ตื่นเต้น", "Uczucia", 4, "v", ST,
 "Uwaga: znaczy zarówno „podekscytowany”, jak i „zestresowany”. Kontekst rozstrzyga.", ""),
("A1", "być zazdrosnym", "ìt-chǎa", "อิจฉา", "Uczucia", 3, "v", ST, "", ""),
("A1", "mieć nadzieję", "wǎng", "หวัง", "Uczucia", 4, "v", ST, "", ""),
("A1", "żałować czegoś", "sǐa daai", "เสียดาย", "Uczucia", 4, "v", ST, "", ""),
("A2", "irytować się", "ram-khaan", "รำคาญ", "Uczucia", 3, "v", ST, "", ""),
("A2", "obrażać się", "ngǒn", "งอน", "Uczucia", 3, "v", LR,
 "Sposób okazywania urazy przez ciche wycofanie, nie przez krzyk. Ważne w relacjach.", ""),
("A2", "wzruszyć się", "prá-tháp jai", "ประทับใจ", "Uczucia", 3, "v", ST, "", "odcisnąć serce"),
("A2", "czuć ulgę", "loong jai", "โล่งใจ", "Uczucia", 3, "v", ST, "", "puste serce"),
("A2", "czuć się nieswojo", "kree-jai", "เกรงใจ", "Uczucia", 4, "v", LR,
 "Pojęcie bez polskiego odpowiednika: skrępowanie kłopotaniem kogoś. Filar tajskiej uprzejmości.", ""),
("A2", "stracić twarz", "sǐa nâa", "เสียหน้า", "Uczucia", 3, "v", LR,
 "W kulturze tajskiej ważniejsze niż racja. Publiczna krytyka to sǐa nâa.", "stracić twarz"),
("A2", "zachować twarz", "ráksǎa nâa", "รักษาหน้า", "Uczucia", 2, "v", LR, "", ""),
("A2", "bawić się dobrze", "sà-nùk", "สนุก", "Uczucia", 5, "v", ST,
 "Kluczowe słowo tajskiego stosunku do świata — sà-nùk mâi? to pytanie o wszystko.", ""),
("A2", "odpuścić, machnąć ręką", "cháang man", "ช่างมัน", "Uczucia", 4, "w", ST, "", ""),

# =========================================================== small talk
("A1", "Skąd jesteś?", "maa jàak nǎi khráp", "มาจากไหนครับ", "Small talk", 5, "w", PY, "", ""),
("A1", "Pierwszy raz w Tajlandii?", "maa thai khráng râek rǔe khráp", "มาไทยครั้งแรกหรือครับ", "Small talk", 4, "w", PY, "", ""),
("A1", "Jak długo tu jesteś?", "yùu thîi nîi naan thâo rài khráp", "อยู่ที่นี่นานเท่าไหร่ครับ", "Small talk", 4, "w", PY, "", ""),
("A1", "Czym się zajmujesz?", "tham ngaan à-rai khráp", "ทำงานอะไรครับ", "Small talk", 5, "w", PY, "", ""),
("A1", "Jadłeś już?", "kin khâao rǔe yang khráp", "กินข้าวหรือยังครับ", "Small talk", 5, "w", ST,
 "Tajskie „co słychać”. Nie jest zaproszeniem na obiad — to grzecznościowe zagajenie.", ""),
("A1", "Dokąd idziesz?", "pai nǎi khráp", "ไปไหนครับ", "Small talk", 5, "w", ST,
 "Też zagajenie, nie przesłuchanie. Odpowiedź „pai thîao” — tak sobie — wystarcza.", ""),
("A2", "Podoba mi się tutaj.", "phǒm châwp thîi nîi khráp", "ผมชอบที่นี่ครับ", "Small talk", 5, "w", ST, "", ""),
("A2", "Uczę się tajskiego.", "phǒm rian phaa-sǎa thai khráp", "ผมเรียนภาษาไทยครับ", "Small talk", 5, "w", ST, "", ""),
("A2", "Mówię tylko trochę.", "phûut dâi nít nàwi khráp", "พูดได้นิดหน่อยครับ", "Small talk", 5, "w", ST, "", ""),
("A2", "Proszę mówić wolniej.", "phûut cháa cháa nàwi khráp", "พูดช้าๆหน่อยครับ", "Small talk", 5, "w", ST, "", ""),
("A2", "Nie rozumiem, przepraszam.", "khǎw thôot phǒm mâi khâo jai khráp", "ขอโทษผมไม่เข้าใจครับ", "Small talk", 5, "w", ST, "", ""),
("A2", "Jak to się mówi po tajsku?", "phaa-sǎa thai phûut wâa à-rai khráp", "ภาษาไทยพูดว่าอะไรครับ", "Small talk", 5, "w", PY, "", ""),
("A2", "Miło było poznać.", "yin dii thîi dâi rúu-jàk khráp", "ยินดีที่ได้รู้จักครับ", "Small talk", 5, "w", PG, "", ""),
("A2", "Do zobaczenia wkrótce.", "láew jooe kan mài khráp", "แล้วเจอกันใหม่ครับ", "Small talk", 5, "w", PG, "", ""),
("A2", "Pozdrów rodzinę.", "fàak sà-wàt-dii khrâwp khrua dûai khráp", "ฝากสวัสดีครอบครัวด้วยครับ", "Small talk", 3, "w", PG, "", ""),

# =========================================================== kłopoty
("A1", "Potrzebuję pomocy.", "phǒm tâwng-kaan khwaam chûai lǔea khráp", "ผมต้องการความช่วยเหลือครับ", "Kłopoty", 5, "w", AW, "", ""),
("A1", "To pilne.", "dùan khráp", "ด่วนครับ", "Kłopoty", 5, "w", AW, "", ""),
("A1", "Coś jest nie tak.", "mii à-rai phìt pòk-kà-tì khráp", "มีอะไรผิดปกติครับ", "Kłopoty", 4, "w", AW, "", ""),
("A2", "Nie mam przy sobie dokumentów.", "phǒm mâi dâi ao èek-kà-sǎan maa khráp", "ผมไม่ได้เอาเอกสารมาครับ", "Kłopoty", 3, "w", AW, "", ""),
("A2", "Chcę zgłosić kradzież.", "phǒm yàak jâeng khwaam khà-mooei khráp", "ผมอยากแจ้งความขโมยครับ", "Kłopoty", 3, "w", AW, "", ""),
("A2", "Proszę zadzwonić na policję.", "chûai thoo hǎa tam-rùat khráp", "ช่วยโทรหาตำรวจครับ", "Kłopoty", 4, "w", AW, "", ""),
("A2", "Nie czuję się bezpiecznie.", "phǒm rúu-sùek mâi plàwt phai khráp", "ผมรู้สึกไม่ปลอดภัยครับ", "Kłopoty", 3, "w", AW, "", ""),
("A2", "Proszę mi pomóc to załatwić.", "chûai jàt kaan hâi nàwi khráp", "ช่วยจัดการให้หน่อยครับ", "Kłopoty", 3, "w", AW, "", ""),
]
