# -*- coding: utf-8 -*-
"""Sesja O, partia 14 — CZAS WOLNY: sport, muzyka, film, gry, media.

Baza umiała zapytać „czym się zajmujesz”, a nie umiała odpowiedzieć na
„co robisz po pracy”. To luka kosztowna: small talk o pracy kończy się po
dwóch zdaniach, small talk o tym, co kto lubi, ciągnie się godzinami.

Struktura partii:

* **sport** — nazwy dyscyplin plus czasowniki `lên` (grać w), `tii` (uderzać),
  `tè` (kopać). Tajski dobiera je do dyscypliny: tè bawn (piłka nożna),
  tii kàwp (golf), lên nám (bawić się w wodzie);
* **muzyka i film** — gatunki, instrumenty, to, co się mówi o obejrzanym;
* **gry i rozrywka** — od karaoke po planszówki, w tym słownictwo, którym
  Tajowie mówią o telefonie;
* **media** — wiadomości, seriale, transmisje, komentarze.

Uwaga kulturowa wpleciona w hasła: `mǔu-ay thai` i karaoke to nie egzotyka
dla turysty, tylko dwie najczęstsze odpowiedzi na pytanie o weekend.

Krotka: (poziom, polski, fonetyka, pismo, podkategoria, częstość, typ,
         kategoria, uwaga, dosłownie)
"""

ST = "Small talk"
CZ = "Czasowniki"
CO = "Cechy i opinie"
PN = "Praca i nauka"
ZP = "Zakupy i pieniądze"
PY = "Pytania"
MO = "Miejsca i orientacja"
LR = "Ludzie i rodzina"
CD = "Czas i daty"
ZD = "Zdrowie"

CULTURE = [

# =========================================================== sport
("A1", "piłka nożna", "fút-bawn", "ฟุตบอล", "Sport", 5, "n", ST, "", ""),
("A1", "koszykówka", "báas-két-bawn", "บาสเกตบอล", "Sport", 3, "n", ST, "", ""),
("A1", "siatkówka", "wawn-lêe-bawn", "วอลเลย์บอล", "Sport", 3, "n", ST,
 "Sport szkolny numer jeden w Tajlandii, zwłaszcza wśród dziewcząt.", ""),
("A1", "badminton", "báet-min-tân", "แบดมินตัน", "Sport", 4, "n", ST, "", ""),
("A1", "tenis", "then-nít", "เทนนิส", "Sport", 3, "n", ST, "", ""),
("A1", "tenis stołowy", "ping-pawng", "ปิงปอง", "Sport", 3, "n", ST, "", ""),
("A1", "golf", "káwp", "กอล์ฟ", "Sport", 3, "n", ST, "", ""),
("A1", "boks tajski", "muai thai", "มวยไทย", "Sport", 5, "n", ST,
 "Sport narodowy. Walki na stadionach Lumpinee i Rajadamnern w Bangkoku.", ""),
("A1", "sepak takraw", "tà-krâw", "ตะกร้อ", "Sport", 3, "n", ST,
 "Siatkówka nogami z rattanową piłką. Gra się w każdym parku.", ""),
("A1", "jazda na rowerze", "khìi jàk-krà-yaan", "ขี่จักรยาน", "Sport", 4, "n", ST, "", ""),
("A2", "joga", "yoo-khá", "โยคะ", "Sport", 3, "n", ZD, "", ""),
("A2", "nurkowanie", "dam nám", "ดำน้ำ", "Sport", 4, "n", ST, "", "zanurzyć woda"),
("A2", "snorkeling", "dam nám tûen", "ดำน้ำตื้น", "Sport", 3, "n", ST, "", "nurkowanie płytkie"),
("A2", "surfing", "tôo khlûen", "โต้คลื่น", "Sport", 2, "n", ST, "", "zmagać się fala"),
("A2", "wspinaczka skałkowa", "piin phǎa", "ปีนผา", "Sport", 3, "n", ST,
 "Krabi i Railay to jeden z lepszych rejonów wspinaczkowych świata.", ""),
("A2", "trekking", "doen pàa", "เดินป่า", "Sport", 3, "n", ST, "", "iść las"),
("A2", "siłownia (ćwiczenia)", "lên fít-nét", "เล่นฟิตเนส", "Sport", 3, "n", ZD, "", ""),
("A2", "mecz", "kaan khàeng", "การแข่ง", "Sport", 4, "n", ST, "", ""),
("A2", "drużyna (sportowa)", "thiim kii-laa", "ทีมกีฬา", "Sport", 3, "n", ST, "", ""),
("A2", "zawodnik", "nák kii-laa aa-chîip", "นักกีฬาอาชีพ", "Sport", 2, "n", ST, "", ""),
("A2", "sędzia (sportowy)", "kam-má-kaan", "กรรมการ", "Sport", 2, "n", ST, "", ""),
("A2", "wynik meczu", "phǒn kaan khàeng", "ผลการแข่ง", "Sport", 3, "n", ST, "", ""),
("A2", "wygrać", "chá-ná", "ชนะ", "Sport", 5, "v", CZ, "", ""),
("A2", "przegrać", "pháe", "แพ้", "Sport", 5, "v", CZ,
 "To samo słowo znaczy „być uczulonym” — pháe thùa, alergia na orzeszki.", ""),
("A2", "remis", "sà-mǒoe", "เสมอ", "Sport", 3, "n", ST, "", ""),
("A2", "grać (w coś)", "lên", "เล่น", "Sport", 5, "v", CZ,
 "Uniwersalne: lên bawn, lên kii-taa, lên nám. Także „żartować” — phûut lên.", ""),
("A2", "kopać (piłkę)", "tè", "เตะ", "Sport", 4, "v", CZ, "", ""),
("A2", "uderzać (rakietą, kijem)", "tii", "ตี", "Sport", 4, "v", CZ, "", ""),
("A2", "rzucać (piłkę)", "yoon", "โยน", "Sport", 3, "v", CZ, "", ""),
("A2", "trenować", "fùek sáwm", "ฝึกซ้อม", "Sport", 3, "v", CZ, "", ""),

# =========================================================== muzyka
("A1", "piosenka", "phleeng", "เพลง", "Muzyka", 5, "n", ST, "", ""),
("A1", "gitara", "kii-taa", "กีตาร์", "Muzyka", 3, "n", ST, "", ""),
("A1", "pianino", "pia-noo", "เปียโน", "Muzyka", 3, "n", ST, "", ""),
("A1", "bęben", "klawng", "กลอง", "Muzyka", 3, "n", ST, "", ""),
("A1", "skrzypce", "sawi", "ซอ", "Muzyka", 2, "n", ST, "", ""),
("A1", "flet", "khlùi", "ขลุ่ย", "Muzyka", 2, "n", ST, "", ""),
("A2", "muzyka ludowa Isanu", "mǎw lam", "หมอลำ", "Muzyka", 3, "n", ST,
 "Gatunek północno-wschodni, wszechobecny na weselach i w autobusach.", ""),
("A2", "muzyka luk thung", "lûuk thûng", "ลูกทุ่ง", "Muzyka", 4, "n", ST,
 "Dosłownie „dziecko pola”. Tajska muzyka wiejska, odpowiednik country.", "dziecko pole"),
("A2", "koncert", "khawn-sòet", "คอนเสิร์ต", "Muzyka", 3, "n", ST, "", ""),
("A2", "zespół muzyczny", "wong don-trii", "วงดนตรี", "Muzyka", 3, "n", ST, "", ""),
("A2", "śpiewać", "ráwng phleeng", "ร้องเพลง", "Muzyka", 5, "v", CZ, "", ""),
("A2", "grać na instrumencie", "lên don-trii", "เล่นดนตรี", "Muzyka", 4, "v", CZ, "", ""),
("A2", "tańczyć", "tên", "เต้น", "Muzyka", 4, "v", CZ, "", ""),
("A2", "karaoke", "khaa-raa-oo-kè", "คาราโอเกะ", "Muzyka", 4, "n", ST,
 "Rozrywka towarzyska numer jeden. Odmowa śpiewania bywa odbierana jako chłód.", ""),
("A2", "melodia", "tham-nawng", "ทำนอง", "Muzyka", 2, "n", ST, "", ""),
("A2", "tekst piosenki", "núea phleeng", "เนื้อเพลง", "Muzyka", 3, "n", ST, "", "treść piosenki"),

# =========================================================== film i media
("A1", "film", "nǎng", "หนัง", "Media", 5, "n", ST, "", ""),
("A1", "serial", "lá-khaawn", "ละคร", "Media", 5, "n", ST,
 "Tajskie seriale wieczorne to temat rozmowy w każdym biurze.", ""),
("A1", "wiadomości (w TV)", "khào", "ข่าว", "Media", 5, "n", ST, "", ""),
("A1", "program (telewizyjny)", "raai kaan", "รายการ", "Media", 4, "n", ST, "", ""),
("A1", "reklama", "khoo-sà-naa", "โฆษณา", "Media", 4, "n", ST, "", ""),
("A2", "komedia", "nǎng tà-lòk", "หนังตลก", "Media", 3, "n", ST, "", "film śmieszny"),
("A2", "film akcji", "nǎng bùu", "หนังบู๊", "Media", 3, "n", ST, "", ""),
("A2", "horror", "nǎng phǐi", "หนังผี", "Media", 4, "n", ST,
 "Tajskie horrory to gatunek eksportowy — phǐi znaczy „duch”.", "film duch"),
("A2", "film romantyczny", "nǎng rák", "หนังรัก", "Media", 3, "n", ST, "", ""),
("A2", "napisy", "kham ban-yaai tâi phâap", "คำบรรยายใต้ภาพ", "Media", 3, "n", ST, "", "słowa opis pod obrazem"),
("A2", "dubbing", "phaak thai", "พากย์ไทย", "Media", 3, "n", ST, "", "dubbing tajski"),
("A2", "aktor główny", "phrá èek", "พระเอก", "Media", 3, "n", ST, "", ""),
("A2", "aktorka główna", "naang èek", "นางเอก", "Media", 3, "n", ST, "", ""),
("A2", "odcinek", "tawn", "ตอน", "Media", 4, "n", ST,
 "To samo słowo znaczy „pora dnia” — tawn cháo, rano.", ""),
("A2", "kanał (TV)", "châwng", "ช่อง", "Media", 4, "n", ST, "", ""),
("A2", "transmisja na żywo", "thàai thâwt sòt", "ถ่ายทอดสด", "Media", 3, "n", ST, "", ""),
("A2", "podcast", "pháwt-khâat", "พอดแคสต์", "Media", 2, "n", ST, "", ""),
("A2", "gazeta", "nǎng-sǔe phim", "หนังสือพิมพ์", "Media", 3, "n", ST, "", "księga drukowana"),
("A2", "czasopismo", "nít-tà-yá-sǎan", "นิตยสาร", "Media", 2, "n", ST, "", ""),

# =========================================================== gry i hobby
("A1", "gra (zabawa)", "keem", "เกม", "Hobby", 4, "n", ST, "", ""),
("A1", "gra na telefonie", "keem mue thǔe", "เกมมือถือ", "Hobby", 4, "n", ST, "", ""),
("A1", "karty (do gry)", "phâi", "ไพ่", "Hobby", 3, "n", ST, "", ""),
("A1", "szachy", "màak rúk", "หมากรุก", "Hobby", 2, "n", ST, "", ""),
("A1", "puzzle", "jík-sáw", "จิ๊กซอว์", "Hobby", 2, "n", ST, "", ""),
("A2", "zbieranie (kolekcjonowanie)", "sà-sǒm", "สะสม", "Hobby", 3, "v", CZ, "", ""),
("A2", "rysować", "wâat rûup", "วาดรูป", "Hobby", 4, "v", CZ, "", ""),
("A2", "malować (obraz)", "rá-baai sǐi", "ระบายสี", "Hobby", 2, "v", CZ, "", ""),
("A2", "robić zdjęcia", "thàai rûup", "ถ่ายรูป", "Hobby", 5, "v", CZ, "", ""),
("A2", "czytać książki", "àan nǎng-sǔe", "อ่านหนังสือ", "Hobby", 5, "v", CZ,
 "Uwaga: to samo wyrażenie znaczy „uczyć się do egzaminu”.", ""),
("A2", "oglądać film", "duu nǎng", "ดูหนัง", "Hobby", 5, "v", CZ, "", ""),
("A2", "słuchać muzyki", "fang phleeng", "ฟังเพลง", "Hobby", 5, "v", CZ, "", ""),
("A2", "gotować dla przyjemności", "tham aa-hǎan lên", "ทำอาหารเล่น", "Hobby", 2, "v", CZ, "", ""),
("A2", "hodować rośliny", "plùuk tôn mái", "ปลูกต้นไม้", "Hobby", 3, "v", CZ, "", ""),
("A2", "łowić ryby", "tòk plaa", "ตกปลา", "Hobby", 3, "v", CZ, "", ""),
("A2", "podróżować dla przyjemności", "pai thîao", "ไปเที่ยว", "Hobby", 5, "v", CZ,
 "Najczęstsza odpowiedź na „co robisz w weekend”.", ""),
("A2", "spotykać się ze znajomymi", "jooe phûean", "เจอเพื่อน", "Hobby", 5, "v", CZ, "", ""),
("A2", "wychodzić wieczorem", "àwk pai klaang khuen", "ออกไปกลางคืน", "Hobby", 3, "v", CZ, "", ""),
("A2", "odpoczywać w domu", "yùu bâan chóei chóei", "อยู่บ้านเฉยๆ", "Hobby", 4, "v", CZ, "", "być w domu tak sobie"),

# =========================================================== opinie o rozrywce
("A1", "zabawny", "sà-nùk dii", "สนุกดี", "Opinie", 5, "adj", CO, "", ""),
("A1", "wciągający", "tìt dâi", "ติดได้", "Opinie", 3, "adj", CO, "", ""),
("A1", "za długi", "yaao kooen pai", "ยาวเกินไป", "Opinie", 4, "adj", CO, "", ""),
("A1", "wzruszający", "sûeng", "ซึ้ง", "Opinie", 3, "adj", CO, "", ""),
("A2", "przereklamowany", "mâi dii yàang thîi khít", "ไม่ดีอย่างที่คิด", "Opinie", 2, "adj", CO, "", ""),
("A2", "wart obejrzenia", "khúm thîi jà duu", "คุ้มที่จะดู", "Opinie", 3, "adj", CO, "", ""),
("A2", "nowy (o filmie, płycie)", "àwk mài", "ออกใหม่", "Opinie", 3, "adj", ST, "", "wyszedł nowy"),
("A2", "popularny wśród młodych", "wai rûn châwp", "วัยรุ่นชอบ", "Opinie", 2, "adj", ST, "", ""),

# =========================================================== pytania o czas wolny
("A1", "Co robisz w wolnym czasie?", "wâang wâang tham à-rai khráp", "ว่างๆทำอะไรครับ", "Pytania", 5, "w", PY, "", ""),
("A1", "Lubisz sport?", "châwp kii-laa mǎi khráp", "ชอบกีฬาไหมครับ", "Pytania", 4, "w", PY, "", ""),
("A1", "Jaką muzykę lubisz?", "châwp phleeng bàep nǎi khráp", "ชอบเพลงแบบไหนครับ", "Pytania", 4, "w", PY, "", ""),
("A1", "Widziałeś ten film?", "duu nǎng rûeang níi rǔe yang khráp", "ดูหนังเรื่องนี้หรือยังครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Idziemy na mecz?", "pai duu kaan khàeng kan mǎi khráp", "ไปดูการแข่งกันไหมครับ", "Pytania", 3, "w", PY, "", ""),
("A2", "Umiesz śpiewać?", "ráwng phleeng dâi mǎi khráp", "ร้องเพลงได้ไหมครับ", "Pytania", 4, "w", PY, "", ""),
("A2", "Co robisz w weekend?", "sǎo aa-thít tham à-rai khráp", "เสาร์อาทิตย์ทำอะไรครับ", "Pytania", 5, "w", PY, "", ""),
("A2", "Chodźmy razem.", "pai dûai kan thòe", "ไปด้วยกันเถอะ", "Pytania", 5, "w", ST,
 "Partykuła thòe zaprasza i zachęca — bez niej zdanie brzmi jak polecenie.", ""),
("A2", "Kiedy masz wolne?", "wâang mûea rài khráp", "ว่างเมื่อไหร่ครับ", "Pytania", 5, "w", PY, "", ""),
("A2", "To brzmi ciekawie.", "fang duu nâa sǒn jai khráp", "ฟังดูน่าสนใจครับ", "Pytania", 4, "w", ST, "", ""),
]
