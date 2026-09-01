# -*- coding: utf-8 -*-
"""Sesja O, partia 8 — CZASOWNIKI codzienne.

Kategoria Czasowniki miała 245 haseł i była największa w bazie, więc sesja N
miała na nią twardy zakaz dokładania. Tu zakaz zdejmujemy, ale w wąskim
zakresie: dokładamy **czasowniki wielosylabowe złożone z sylab już znanych**
oraz kilkadziesiąt rdzeni, których brak blokował całe pola tematyczne.

Powód jest arytmetyczny. Zdanie parowe „Chcę {czasownik} {rzeczownik}”
wymaga czasownika. Partie rzeczownikowe tej sesji dokładają ponad
sześćset rzeczowników; bez odpowiedniej podaży czasowników generator
ścieżki nie ma czym ich aktywować i gęstość lekcji spada z powrotem do
jednego hasła na zdanie.

Grupa druga to **czasowniki z `jai` (serce)**. Tajski buduje na nich całą
warstwę mówienia o stanach umysłu: `khâo jai` (rozumieć), `sǒn jai`
(interesować się), `tòk jai` (przestraszyć się). Wszystkie składają się
z dwóch znanych sylab, a otwierają rozmowę o tym, co ktoś czuje.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

CZ = "Czasowniki"
DC = "Dom i codzienność"
PN = "Praca i nauka"
ST = "Small talk"
ZP = "Zakupy i pieniądze"
AW = "Awarie i pomoc"
MO = "Miejsca i orientacja"
GU = "Gramatyka użytkowa"
LR = "Ludzie i rodzina"
TR = "Transport"

VERBS = [

# =========================================================== ruch i ciało
("A1", "wstawać", "lúk khûen", "ลุกขึ้น", "Ruch", 4, "v", CZ, "", "podnieść się w górę"),
("A1", "siadać", "nâng long", "นั่งลง", "Ruch", 4, "v", CZ, "", "siedzieć w dół"),
("A1", "kłaść się", "nawn long", "นอนลง", "Ruch", 3, "v", CZ, "", ""),
("A1", "schylać się", "kôm", "ก้ม", "Ruch", 2, "v", CZ, "", ""),
("A1", "odwracać się", "hǎn", "หัน", "Ruch", 3, "v", CZ, "", ""),
("A1", "skakać", "krà-dòot", "กระโดด", "Ruch", 3, "v", CZ, "", ""),
("A1", "ciągnąć", "dueng", "ดึง", "Ruch", 4, "v", CZ,
 "Na drzwiach napisane obok phlàk (pchać) — warto rozpoznać oba.", ""),
("A1", "pchać", "phlàk", "ผลัก", "Ruch", 3, "v", CZ, "", ""),
("A1", "podnosić", "yók", "ยก", "Ruch", 4, "v", CZ, "", ""),
("A1", "rzucać", "khwâang", "ขว้าง", "Ruch", 3, "v", CZ, "", ""),
("A1", "łapać", "jàp", "จับ", "Ruch", 4, "v", CZ,
 "To samo słowo znaczy „dotknąć” i „aresztować”.", ""),
("A1", "puszczać, wypuszczać", "plàwi", "ปล่อย", "Ruch", 4, "v", CZ, "", ""),
("A1", "nieść", "thǔe", "ถือ", "Ruch", 4, "v", CZ, "", ""),
("A1", "wieźć, zabierać ze sobą", "phaa", "พา", "Ruch", 4, "v", CZ, "", ""),
("A1", "wkładać", "sài", "ใส่", "Ruch", 5, "v", CZ,
 "Jedno z najczęstszych słów: wkładać ubranie, dodawać do potrawy, wsypywać cukier.", ""),
("A1", "wyjmować", "ao àwk", "เอาออก", "Ruch", 4, "v", CZ, "", "brać na zewnątrz"),
("A2", "przewracać się", "lóm", "ล้ม", "Ruch", 3, "v", CZ, "", ""),
("A2", "poślizgnąć się", "lûen", "ลื่น", "Ruch", 3, "v", CZ, "", ""),
("A2", "ślizgać się, unikać", "lìik lîang", "หลีกเลี่ยง", "Ruch", 2, "v", CZ, "", ""),
("A2", "wspinać się na coś", "piin khûen", "ปีนขึ้น", "Ruch", 2, "v", CZ, "", ""),
("A2", "schodzić w dół", "doen long", "เดินลง", "Ruch", 3, "v", CZ, "", ""),

# =========================================================== dom
("A1", "zamiatać", "kwàat", "กวาด", "Dom", 3, "v", CZ, "", ""),
("A1", "wycierać", "chét", "เช็ด", "Dom", 4, "v", CZ, "", ""),
("A1", "szorować", "khàt", "ขัด", "Dom", 2, "v", CZ, "", ""),
("A1", "prasować", "rîit", "รีด", "Dom", 3, "v", CZ, "", ""),
("A1", "wieszać", "khwǎen", "แขวน", "Dom", 3, "v", CZ, "", ""),
("A1", "składać (ubrania)", "pháp", "พับ", "Dom", 3, "v", CZ, "", ""),
("A1", "wyrzucać", "thíng", "ทิ้ง", "Dom", 5, "v", CZ,
 "To samo słowo znaczy „porzucić kogoś” — thíng faen.", ""),
("A1", "zbierać, chować", "kèp", "เก็บ", "Dom", 5, "v", CZ, "", ""),
("A1", "porządkować", "jàt", "จัด", "Dom", 4, "v", CZ, "", ""),
("A1", "wypełniać, napełniać", "toem", "เติม", "Dom", 4, "v", CZ,
 "toem nám man — zatankować, toem ngoen — doładować telefon.", ""),
("A1", "wylewać", "thee", "เท", "Dom", 3, "v", CZ, "", ""),
("A1", "rozlewać (przypadkiem)", "tham lôn", "ทำหล่น", "Dom", 2, "v", CZ, "", ""),
("A2", "przykrywać", "pìt", "ปิด", "Dom", 4, "v", CZ,
 "To samo słowo znaczy „zamykać” i „wyłączać” — pìt fai to zgasić światło.", ""),
("A2", "wietrzyć", "tàak lom", "ตากลม", "Dom", 2, "v", CZ, "", "wystawiać wiatr"),
("A2", "suszyć na słońcu", "tàak dàet", "ตากแดด", "Dom", 3, "v", CZ, "", "wystawiać słońce"),
("A2", "podłączyć", "sìap", "เสียบ", "Dom", 3, "v", CZ, "", ""),
("A2", "odłączyć", "thǎwt plák", "ถอดปลั๊ก", "Dom", 2, "v", CZ, "", "wyjąć wtyczka"),
("A2", "zakręcić (kran)", "pìt kók", "ปิดก๊อก", "Dom", 3, "v", CZ, "", ""),
("A2", "zdejmować (ubranie, buty)", "thǎwt", "ถอด", "Dom", 4, "v", CZ,
 "thǎwt rawng tháo — zdjąć buty. Przed wejściem do domu i świątyni obowiązkowo.", ""),

# =========================================================== praca i sprawy
("A1", "kończyć", "sèt", "เสร็จ", "Praca", 5, "v", CZ, "", ""),
("A1", "przerywać", "yùt phák", "หยุดพัก", "Praca", 3, "v", CZ, "", "zatrzymać odpocząć"),
("A1", "przygotować", "triam", "เตรียม", "Praca", 4, "v", CZ, "", ""),
("A1", "sprawdzać", "chék", "เช็ค", "Praca", 5, "v", CZ, "", ""),
("A1", "poprawiać", "kâe khǎi", "แก้ไข", "Praca", 4, "v", CZ, "", ""),
("A1", "podpisywać", "sen chûe", "เซ็นชื่อ", "Praca", 3, "v", CZ, "", "podpisać imię"),
("A1", "wypełniać formularz", "kràwk", "กรอก", "Praca", 3, "v", CZ, "", ""),
("A1", "drukować", "phim", "พิมพ์", "Praca", 4, "v", CZ,
 "To samo słowo znaczy „pisać na klawiaturze”.", ""),
("A1", "kopiować", "thàai èek-kà-sǎan", "ถ่ายเอกสาร", "Praca", 3, "v", CZ, "", ""),
("A2", "zatrudniać", "jâang", "จ้าง", "Praca", 3, "v", CZ, "", ""),
("A2", "zwalniać (z pracy)", "lâi àwk", "ไล่ออก", "Praca", 2, "v", CZ, "", ""),
("A2", "rezygnować", "laa àwk", "ลาออก", "Praca", 3, "v", CZ, "", "prosić wyjść"),
("A2", "brać wolne", "laa", "ลา", "Praca", 4, "v", CZ, "", ""),
("A2", "awansować", "lûean tam-nàeng", "เลื่อนตำแหน่ง", "Praca", 2, "v", CZ, "", ""),
("A2", "przekładać (termin)", "lûean", "เลื่อน", "Praca", 4, "v", CZ,
 "Także „przesuwać” — lûean nát to przełożyć spotkanie.", ""),
("A2", "odwoływać", "yók lôek", "ยกเลิก", "Praca", 4, "v", CZ, "", "podnieść porzucić"),
("A2", "potwierdzać", "yuen yan", "ยืนยัน", "Praca", 4, "v", CZ, "", ""),
("A2", "zgłaszać", "jâeng", "แจ้ง", "Praca", 4, "v", CZ, "", ""),
("A2", "składać wniosek", "yûen khǎw", "ยื่นขอ", "Praca", 2, "v", CZ, "", ""),
("A2", "zarządzać", "jàt kaan", "จัดการ", "Praca", 3, "v", CZ, "", ""),
("A2", "dzielić się, rozdzielać", "bàeng", "แบ่ง", "Praca", 4, "v", CZ, "", ""),
("A2", "zamieniać", "lâek", "แลก", "Praca", 4, "v", CZ, "", ""),
("A2", "zwracać (rzecz)", "khuen", "คืน", "Praca", 4, "v", CZ, "", ""),
("A2", "pożyczać od kogoś", "yuem", "ยืม", "Praca", 4, "v", CZ, "", ""),
("A2", "wynajmować", "châo", "เช่า", "Praca", 4, "v", CZ, "", ""),
("A2", "oszczędzać (pieniądze)", "kèp ngoen", "เก็บเงิน", "Praca", 4, "v", CZ, "", ""),
("A2", "wydawać (pieniądze)", "chái ngoen", "ใช้เงิน", "Praca", 4, "v", CZ, "", ""),
("A2", "zarabiać", "hǎa ngoen", "หาเงิน", "Praca", 4, "v", CZ, "", "szukać pieniędzy"),
("A2", "być winnym pieniądze", "tìt ngoen", "ติดเงิน", "Praca", 2, "v", CZ, "", ""),

# =========================================================== jai — stany umysłu
("A1", "interesować się", "sǒn jai", "สนใจ", "Umysł", 5, "v", CZ, "", "wchodzić serce"),
("A1", "przestraszyć się", "tòk jai", "ตกใจ", "Umysł", 4, "v", CZ, "", "spaść serce"),
("A1", "być zadowolonym", "phaw jai", "พอใจ", "Umysł", 4, "v", CZ, "", "wystarczy serce"),
("A1", "ufać", "wái jai", "ไว้ใจ", "Umysł", 3, "v", CZ, "", "powierzyć serce"),
("A1", "martwić się", "pen hùang", "เป็นห่วง", "Umysł", 4, "v", CZ, "", ""),
("A1", "uważać, być ostrożnym", "rá-wang", "ระวัง", "Umysł", 5, "v", CZ,
 "Na każdym znaku ostrzegawczym w Tajlandii.", ""),
("A2", "zwracać uwagę", "sǒn jai jing jing", "สนใจจริงๆ", "Umysł", 2, "v", CZ, "", ""),
("A2", "zdecydować", "tàt sǐn jai", "ตัดสินใจ", "Umysł", 4, "v", CZ, "", "ciąć osądzić serce"),
("A2", "zmienić zdanie", "plìan jai", "เปลี่ยนใจ", "Umysł", 3, "v", CZ, "", "zmienić serce"),
("A2", "poddać się", "yawm pháe", "ยอมแพ้", "Umysł", 3, "v", CZ, "", "zgodzić się przegrać"),
("A2", "zgodzić się", "yawm", "ยอม", "Umysł", 4, "v", CZ, "", ""),
("A2", "wybaczyć", "yók thôot", "ยกโทษ", "Umysł", 3, "v", CZ, "", "podnieść winę"),
("A2", "żałować", "sǐa jai", "เสียใจ", "Umysł", 4, "v", CZ,
 "To samo wyrażenie znaczy „przykro mi” przy kondolencjach.", "stracić serce"),
("A2", "cieszyć się", "dii jai", "ดีใจ", "Umysł", 5, "v", CZ, "", "dobre serce"),
("A2", "nudzić się", "bùea", "เบื่อ", "Umysł", 4, "v", CZ, "", ""),
("A2", "tęsknić", "khít thǔeng", "คิดถึง", "Umysł", 5, "v", CZ,
 "Najcieplejsze tajskie wyrażenie — mówi się je znajomym po tygodniu niewidzenia.", "myśleć dosięgać"),
("A2", "być dumnym", "phuum jai", "ภูมิใจ", "Umysł", 3, "v", CZ, "", ""),
("A2", "wstydzić się", "aai", "อาย", "Umysł", 4, "v", CZ, "", ""),
("A2", "wątpić", "sǒng sǎi", "สงสัย", "Umysł", 4, "v", CZ,
 "To samo słowo znaczy „zastanawiać się” i „podejrzewać”.", ""),
("A2", "przypominać sobie", "nûek àwk", "นึกออก", "Umysł", 3, "v", CZ, "", "pomyśleć wyjść"),
("A2", "zapominać", "luem", "ลืม", "Umysł", 5, "v", CZ, "", ""),
("A2", "przyzwyczaić się", "chin", "ชิน", "Umysł", 3, "v", CZ, "", ""),
("A2", "domyślać się", "dao", "เดา", "Umysł", 3, "v", CZ, "", ""),
("A2", "planować", "waang phǎen", "วางแผน", "Umysł", 4, "v", CZ, "", ""),

# =========================================================== mowa i kontakt
("A1", "krzyczeć", "tà-kon", "ตะโกน", "Mowa", 3, "v", CZ, "", ""),
("A1", "szeptać", "krà-síp", "กระซิบ", "Mowa", 2, "v", CZ, "", ""),
("A1", "powtarzać", "phûut sám", "พูดซ้ำ", "Mowa", 4, "v", CZ, "", "mówić powtórnie"),
("A1", "opowiadać", "lâo", "เล่า", "Mowa", 4, "v", CZ, "", ""),
("A1", "wyjaśniać", "à-thí-baai", "อธิบาย", "Mowa", 4, "v", CZ, "", ""),
("A1", "obiecywać", "sǎn-yaa", "สัญญา", "Mowa", 3, "v", CZ, "", ""),
("A1", "kłamać", "koo-hòk", "โกหก", "Mowa", 3, "v", CZ, "", ""),
("A1", "żartować", "phûut lên", "พูดเล่น", "Mowa", 4, "v", CZ, "", "mówić dla zabawy"),
("A2", "kłócić się", "thá-lǎw", "ทะเลาะ", "Mowa", 3, "v", CZ, "", ""),
("A2", "przekonywać", "chák chuan", "ชักชวน", "Mowa", 2, "v", CZ, "", ""),
("A2", "prosić o pozwolenie", "khǎw à-nú-yâat", "ขออนุญาต", "Mowa", 3, "v", CZ, "", ""),
("A2", "odmawiać", "pà-tì-sèet", "ปฏิเสธ", "Mowa", 3, "v", CZ, "", ""),
("A2", "zapraszać", "chuan", "ชวน", "Mowa", 4, "v", CZ, "", ""),
("A2", "przedstawiać kogoś", "náe-nam hâi rúu-jàk", "แนะนำให้รู้จัก", "Mowa", 3, "v", CZ, "", ""),
("A2", "dzwonić do kogoś", "thoo hǎa", "โทรหา", "Mowa", 5, "v", CZ, "", "dzwonić szukać"),
("A2", "oddzwonić", "thoo klàp", "โทรกลับ", "Mowa", 4, "v", CZ, "", ""),
("A2", "wysłać wiadomość", "sòng khâw khwaam", "ส่งข้อความ", "Mowa", 5, "v", CZ, "", ""),
("A2", "odpisać", "tàwp klàp", "ตอบกลับ", "Mowa", 4, "v", CZ, "", ""),
("A2", "przetłumaczyć", "plae", "แปล", "Mowa", 5, "v", CZ, "", ""),
("A2", "przeliterować", "sà-kòt", "สะกด", "Mowa", 2, "v", CZ, "", ""),

# =========================================================== zdarzenia i pomoc
("A1", "zgubić", "tham hǎai", "ทำหาย", "Zdarzenia", 4, "v", CZ, "", "sprawić zniknięcie"),
("A1", "znaleźć", "jooe", "เจอ", "Zdarzenia", 5, "v", CZ,
 "To samo słowo znaczy „spotkać kogoś” — jooe kan phrûng níi.", ""),
("A1", "ukraść", "khà-mooei", "ขโมย", "Zdarzenia", 4, "v", CZ, "", ""),
("A1", "zepsuć", "tham phang", "ทำพัง", "Zdarzenia", 3, "v", CZ, "", ""),
("A1", "naprawić", "sâwm", "ซ่อม", "Zdarzenia", 5, "v", CZ, "", ""),
("A1", "wymienić na nowe", "plìan mài", "เปลี่ยนใหม่", "Zdarzenia", 4, "v", CZ, "", ""),
("A1", "uderzyć w coś", "chon", "ชน", "Zdarzenia", 4, "v", CZ, "", ""),
("A1", "wybuchnąć, eksplodować", "rá-bòet", "ระเบิด", "Zdarzenia", 2, "v", CZ, "", ""),
("A2", "gasić (pożar)", "dàp", "ดับ", "Zdarzenia", 3, "v", CZ,
 "To samo słowo znaczy „zgasnąć” — fai dàp, prąd padł.", ""),
("A2", "ratować", "chûai chii-wít", "ช่วยชีวิต", "Zdarzenia", 3, "v", CZ, "", "pomóc życie"),
("A2", "uciekać", "nǐi", "หนี", "Zdarzenia", 3, "v", CZ, "", ""),
("A2", "chować się", "làwp", "หลบ", "Zdarzenia", 2, "v", CZ, "", ""),
("A2", "ostrzegać", "tuean", "เตือน", "Zdarzenia", 4, "v", CZ,
 "Także „przypominać komuś” — tuean phǒm dûai khráp.", ""),
("A2", "pilnować", "fâo", "เฝ้า", "Zdarzenia", 2, "v", CZ, "", ""),
("A2", "przeszkadzać", "róp-kuan", "รบกวน", "Zdarzenia", 4, "v", CZ,
 "Grzeczne wejście w rozmowę: khǎw róp-kuan nàwi khráp.", ""),
("A2", "czekać na kogoś", "raw", "รอ", "Zdarzenia", 5, "v", CZ, "", ""),
("A2", "spóźnić się", "maa sǎai", "มาสาย", "Zdarzenia", 4, "v", CZ, "", ""),
("A2", "zdążyć", "than", "ทัน", "Zdarzenia", 4, "v", CZ, "", ""),
("A2", "przegapić, nie zdążyć", "phlâat", "พลาด", "Zdarzenia", 3, "v", CZ, "", ""),
]
