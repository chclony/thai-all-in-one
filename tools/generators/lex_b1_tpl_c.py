# -*- coding: utf-8 -*-
"""Wzorce zdaniowe etapu 4 (B1) — czesc C: konstrukcje rzeczownikowe.

Zakres: zglaszanie problemow, reklamacje, tematy rozmowy, zaleznosci,
odpowiedzialnosc, braki, decyzje.

Dwukropek w polskim hasle oznacza wstawke slownikowa w mianowniku — konwencja
opisana w data/metadata.json. Dzieki niej ten sam wzorzec dziala z kazdym
rzeczownikiem bez lamania polskiej odmiany.

Pozycja: (polskie haslo rekordu, polskie haslo bazowe, polski przyklad)
"""

# wspolne biale listy rzeczownikow
USLUGI = ["internet", "wi-fi", "klimatyzacja", "gorąca woda", "pralka", "lodówka",
          "router", "hasło", "telefon", "ładowarka", "karta SIM", "zasięg",
          "winda", "gniazdko", "okno", "drzwi", "klucz"]
PODROZ = ["bilet", "paszport", "wiza", "prawo jazdy", "walizka", "taksówka",
          "autobus", "pociąg", "lotnisko", "opóźnienie", "korek uliczny", "mapa",
          "wycieczka", "przystanek", "rozkład jazdy"]
PIENIADZE = ["rachunek", "czynsz", "kaucja", "paragon", "karta kredytowa",
             "bankomat", "przelew", "ubezpieczenie", "cena", "zniżka", "opłata",
             "gotówka", "kurs wymiany", "pieniądze"]
PRACA = ["umowa", "dokument", "projekt", "zebranie", "pensja", "urlop",
         "nadgodziny", "klient", "biuro", "firma", "wizytówka", "praca"]
DOM = ["mieszkanie do wynajęcia", "umowa najmu", "właściciel", "sąsiad z góry",
       "śmieci", "kuchnia", "sypialnia", "salon", "mebel", "piętro", "czajnik",
       "kuchenka", "mikrofalówka", "odkurzacz", "ochroniarz"]
ZDROWIE = ["apteka", "lekarz", "badanie", "wynik badania", "gorączka", "alergia",
           "ubezpieczenie", "szpital", "klinika", "recepta" if False else "lek"]


def _items(nouns, rec_fmt, ex_fmt):
    """Buduje liste pozycji z jednej bialej listy rzeczownikow."""
    return [(rec_fmt % n, n, ex_fmt % n) for n in nouns]


TPL_C = [

# =====================================================================
# mii pan-haa rueang — zglaszanie problemu
# =====================================================================
dict(key="MIIPANHAA", ty="sentence", cat="Awarie i pomoc", sub="Problemy", reg="n",
     ph="phǒm mii pan-hǎa rûeang {ph} khráp", th="ผมมีปัญหาเรื่อง{th}ครับ",
     lit="rûeang = sprawa, kwestia, temat",
     note="„rûeang” wprowadza temat i jest obowiązkowe. Samo „pan-hǎa + rzeczownik” brzmi urwanie.",
     ex_ph="pan-hǎa rûeang {ph} kâe yang-ngai khráp", ex_th="ปัญหาเรื่อง{th}แก้ยังไงครับ",
     items=_items(USLUGI + PIENIADZE + DOM,
                  "Mam problem z tym, co dotyczy: %s.",
                  "Jak rozwiązać sprawę: %s?")),

# =====================================================================
# yaak jaeng rueang — reklamacja
# =====================================================================
dict(key="JAENG", ty="sentence", cat="Awarie i pomoc", sub="Reklamacje", reg="f",
     ph="phǒm yàak jâeng rûeang {ph} khráp", th="ผมอยากแจ้งเรื่อง{th}ครับ",
     lit="jâeng = zgłaszać oficjalnie",
     note="„jâeng” to zgłoszenie do instytucji: hotelu, banku, policji. Do kolegi powiesz „bàwk”.",
     ex_ph="jâeng rûeang {ph} dâai thîi nǎi khráp", ex_th="แจ้งเรื่อง{th}ได้ที่ไหนครับ",
     items=_items(USLUGI + PIENIADZE + PODROZ,
                  "Chcę zgłosić sprawę: %s.",
                  "Gdzie mogę zgłosić sprawę: %s?")),

# =====================================================================
# yaak khui rueang — otwieranie tematu
# =====================================================================
dict(key="KHUIRUEANG", ty="sentence", cat="Small talk", sub="Rozmowa", reg="n",
     ph="phǒm yàak khui rûeang {ph} khráp", th="ผมอยากคุยเรื่อง{th}ครับ",
     lit="khui = rozmawiać swobodnie",
     note="„khui” to rozmowa nieformalna. Na zebraniu użyj „phûut khui” albo „nam sà-nǒoe”.",
     ex_ph="khui rûeang {ph} dǐao níi dâai mǎi khráp", ex_th="คุยเรื่อง{th}เดี๋ยวนี้ได้ไหมครับ",
     items=_items(PRACA + DOM + PIENIADZE,
                  "Chciałbym porozmawiać o tym, co dotyczy: %s.",
                  "Możemy teraz porozmawiać o tym, co dotyczy: %s?")),

# =====================================================================
# pen huang rueang — troska
# =====================================================================
dict(key="PENHUANG", ty="sentence", cat="Ludzie i rodzina", sub="Troska", reg="n",
     ph="phǒm pen hùang rûeang {ph} khráp", th="ผมเป็นห่วงเรื่อง{th}ครับ",
     lit="pen hùang = martwić się o kogoś lub o coś",
     note="„pen hùang” dotyczy troski o dobro kogoś. Zwykły niepokój to „kang-won”.",
     ex_ph="mâi tâwng pen hùang rûeang {ph} khráp", ex_th="ไม่ต้องเป็นห่วงเรื่อง{th}ครับ",
     items=_items(ZDROWIE + PRACA + PIENIADZE,
                  "Martwię się o to, co dotyczy: %s.",
                  "Nie musisz się martwić o to, co dotyczy: %s.")),

# =====================================================================
# sia daai thii mai mii — zal z powodu braku
# =====================================================================
dict(key="SIADAAI", ty="sentence", cat="Cechy i opinie", sub="Braki", reg="n",
     ph="sǐa daai thîi mâi mii {ph} khráp", th="เสียดายที่ไม่มี{th}ครับ",
     lit="sǐa daai thîi = szkoda, że",
     note="„sǐa daai” to żal za czymś utraconym albo niedostępnym. Nie znaczy „przepraszam”.",
     ex_ph="thîi nîi mâi mii {ph} loei rǒe khráp", ex_th="ที่นี่ไม่มี{th}เลยหรือครับ",
     items=_items(USLUGI + DOM + ZDROWIE,
                  "Szkoda, że nie ma tego, co dotyczy: %s.",
                  "Naprawdę nie ma tu tego, co dotyczy: %s?")),

# =====================================================================
# khrai rap phit chawp rueang — odpowiedzialnosc
# =====================================================================
dict(key="RAPPHIT", ty="question", cat="Awarie i pomoc", sub="Odpowiedzialność", reg="f",
     ph="khrai ráp phìt châwp rûeang {ph} khráp", th="ใครรับผิดชอบเรื่อง{th}ครับ",
     lit="ráp phìt châwp = brać odpowiedzialność",
     note="Mocne pytanie. W tajskiej kulturze pracy zadaje się je dopiero, gdy sprawa jest poważna — wcześniej pyta się „khrai duu rûeang níi”.",
     ex_ph="phǒm mâi dâi ráp phìt châwp rûeang {ph} khráp", ex_th="ผมไม่ได้รับผิดชอบเรื่อง{th}ครับ",
     items=_items(PRACA + DOM + PIENIADZE,
                  "Kto odpowiada za to, co dotyczy: %s?",
                  "Nie odpowiadam za to, co dotyczy: %s.")),

# =====================================================================
# khaat — brak czegos
# =====================================================================
dict(key="KHAAT", ty="sentence", cat="Awarie i pomoc", sub="Braki", reg="n",
     ph="phǒm khàat {ph} khráp", th="ผมขาด{th}ครับ",
     lit="khàat = brakować, nie mieć czegoś potrzebnego",
     note="„khàat” mówi o braku czegoś, co powinno być. Zwykłe „mâi mii” to tylko stwierdzenie faktu.",
     ex_ph="khàat {ph} rǒe plào khráp", ex_th="ขาด{th}หรือเปล่าครับ",
     items=_items(PODROZ + PRACA + ZDROWIE,
                  "Brakuje mi tego, co dotyczy: %s.",
                  "Brakuje ci tego, co dotyczy: %s?")),

# =====================================================================
# yang mai dai tat-sin jai rueang — brak decyzji
# =====================================================================
dict(key="TATSINJAI", ty="sentence", cat="Gramatyka użytkowa", sub="Decyzje", reg="n",
     ph="phǒm yang mâi dâi tàt-sǐn jai rûeang {ph} khráp",
     th="ผมยังไม่ได้ตัดสินใจเรื่อง{th}ครับ",
     lit="tàt-sǐn jai = zdecydować, dosłownie: przeciąć serce",
     note="„yang mâi dâi …” to czynność jeszcze niewykonana. Nie myl z „mâi …”, które znaczy odmowę.",
     ex_ph="tàt-sǐn jai rûeang {ph} rǔe yang khráp", ex_th="ตัดสินใจเรื่อง{th}หรือยังครับ",
     items=_items(DOM + PRACA + PODROZ,
                  "Jeszcze nie zdecydowałem w sprawie: %s.",
                  "Zdecydowałeś już w sprawie: %s?")),

# =====================================================================
# khuen yuu kap — zaleznosc
# =====================================================================
dict(key="KHUENYUU", ty="sentence", cat="Gramatyka użytkowa", sub="Zależności", reg="n",
     ph="man khûen yùu kàp {ph} khráp", th="มันขึ้นอยู่กับ{th}ครับ",
     lit="khûen yùu kàp = zależeć od",
     note="Jedno z najczęstszych zdań w tajskiej dyskusji. Pozwala uniknąć twardej deklaracji.",
     ex_ph="man khûen yùu kàp {ph} rǒe khráp", ex_th="มันขึ้นอยู่กับ{th}หรือครับ",
     items=_items(PIENIADZE + PRACA + ["pogoda", "deszcz", "pora deszczowa", "czas",
                                       "właściciel", "klient", "opóźnienie"],
                  "To zależy od tego, co dotyczy: %s.",
                  "To zależy od tego, co dotyczy: %s?")),

# =====================================================================
# khaw thaam rueang … noi — pytanie o temat
# =====================================================================
dict(key="THAAMRUEANG", ty="question", cat="Pytania", sub="Rozmowa", reg="f",
     ph="khǎw thǎam rûeang {ph} nòi khráp", th="ขอถามเรื่อง{th}หน่อยครับ",
     lit="khǎw thǎam … nòi = poproszę o możliwość zapytania",
     note="„khǎw … nòi” zmiękcza każdą prośbę. Samo „thǎam” bez tej ramy brzmi jak przesłuchanie.",
     ex_ph="rûeang {ph} thǎam khrai dii khráp", ex_th="เรื่อง{th}ถามใครดีครับ",
     items=_items(PIENIADZE + DOM + PODROZ,
                  "Chciałbym zapytać o to, co dotyczy: %s.",
                  "Kogo najlepiej zapytać o to, co dotyczy: %s?")),

# =====================================================================
# tawng triam — przygotowanie
# =====================================================================
dict(key="TRIAM", ty="sentence", cat="Praca i nauka", sub="Przygotowanie", reg="n",
     ph="phǒm tâwng triam {ph} khráp", th="ผมต้องเตรียม{th}ครับ",
     lit="triam = przygotować z wyprzedzeniem",
     note="„triam” dotyczy przygotowania rzeczy i dokumentów. Przygotowanie się psychicznie to „tham jai”.",
     ex_ph="tâwng triam {ph} dûai mǎi khráp", ex_th="ต้องเตรียม{th}ด้วยไหมครับ",
     items=_items(PRACA + PODROZ + ZDROWIE,
                  "Muszę przygotować to, co dotyczy: %s.",
                  "Czy trzeba przygotować też to, co dotyczy: %s?")),

# =====================================================================
# … mai pen pai taam thii khaat wai — zawiedzione zalozenie
# =====================================================================
dict(key="MAIPENPAITAAM", ty="sentence", cat="Cechy i opinie", sub="Oczekiwania", reg="f",
     ph="{ph} mâi pen pai taam thîi khâat wái khráp", th="{th}ไม่เป็นไปตามที่คาดไว้ครับ",
     lit="pen pai taam = przebiegać zgodnie z czymś",
     note="Rejestr wyższy, dobry w raporcie i w rozmowie z instytucją.",
     ex_ph="{ph} pen pai taam thîi khâat wái mǎi khráp", ex_th="{th}เป็นไปตามที่คาดไว้ไหมครับ",
     items=_items(PRACA + PIENIADZE + PODROZ,
                  "Nie wyszło zgodnie z założeniem to, co dotyczy: %s.",
                  "Czy wyszło zgodnie z założeniem to, co dotyczy: %s?")),

# =====================================================================
# khaw hai chuai duu rueang — prosba o zajecie sie sprawa
# =====================================================================
dict(key="CHUAIDUURUEANG", ty="sentence", cat="Awarie i pomoc", sub="Prośby", reg="f",
     ph="chûai duu rûeang {ph} hâi nòi dâai mǎi khráp",
     th="ช่วยดูเรื่อง{th}ให้หน่อยได้ไหมครับ",
     lit="duu rûeang = zająć się sprawą, zerknąć na temat",
     note="„duu rûeang” to zajęcie się czymś, nie samo patrzenie. To bardzo częsty zwrot w obsłudze klienta.",
     ex_ph="rûeang {ph} chûai duu hâi dûai ná khráp", ex_th="เรื่อง{th}ช่วยดูให้ด้วยนะครับ",
     items=_items(USLUGI + DOM + PIENIADZE,
                  "Czy mógłby pan zająć się sprawą: %s?",
                  "Proszę zająć się sprawą: %s.")),

# =====================================================================
# rueang … tok long kan yang-ngai — ustalenia
# =====================================================================
dict(key="TOKLONG", ty="question", cat="Praca i nauka", sub="Ustalenia", reg="f",
     ph="rûeang {ph} tòk long kan yang-ngai khráp", th="เรื่อง{th}ตกลงกันยังไงครับ",
     lit="tòk long = uzgodnić, dojść do porozumienia",
     note="„tòk long” to zarówno „zgoda!”, jak i „ustalenie”. Bardzo produktywne słowo w pracy.",
     ex_ph="rûeang {ph} tòk long taam nán ná khráp", ex_th="เรื่อง{th}ตกลงตามนั้นนะครับ",
     items=_items(PRACA + DOM + PIENIADZE,
                  "Jak ustaliliśmy sprawę: %s?",
                  "Zostajemy przy ustaleniu w sprawie: %s.")),
]
