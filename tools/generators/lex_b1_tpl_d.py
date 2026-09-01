# -*- coding: utf-8 -*-
"""Wzorce zdaniowe etapu 4 (B1) — czesc D: czasowniki, duze biale listy.

Konstrukcje: brak czasu, niechec, warto sprobowac, zaniedbany obowiazek,
kolejnosc, zaprzestanie, o malo nie, nabyta umiejetnosc, przyzwyczajenie,
bezcelowosc, sporadycznosc, umawianie sie.

Zadna z nich nie powiela wzorcow A1 ani A2.

Pozycja: (polskie haslo rekordu, polskie haslo bazowe, polski przyklad)
"""

# Czasowniki rdzenne obecne w bazie od poziomu Survival. Kazda lista ponizej
# jest podzbiorem dobranym tak, zeby polskie zdanie brzmialo naturalnie.
CODZIENNE = ["gotować", "prać", "myć", "sprzątać" if False else "odpoczywać",
             "pakować się", "czytać", "pisać", "uczyć się", "biegać", "pływać",
             "tańczyć", "śpiewać", "robić zdjęcia", "rozmawiać", "słuchać"]
ZALATWIANIE = ["dzwonić", "pytać", "płacić", "rezerwować", "zamawiać", "podpisać",
               "wypełnić formularz", "wysyłać", "zmieniać", "anulować", "szukać",
               "wybierać", "kupować", "sprzedawać", "wynajmować", "pożyczyć"]
RUCH = ["iść pieszo", "wracać", "wsiadać", "wysiadać", "przesiadać się",
        "wchodzić", "wychodzić", "zatrzymać się", "zwiedzać", "spotykać",
        "prowadzić samochód"]
CODZ_RANO = ["wstawać", "budzić się", "brać prysznic", "jeść", "pić", "spać",
             "pracować", "odbierać", "oglądać", "czekać"]


def _v(verbs, rec_fmt, ex_fmt):
    return [(rec_fmt % v, v, ex_fmt % v) for v in verbs]


TPL_D = [

dict(key="MAIMIIWEELAA", ty="sentence", cat="Gramatyka użytkowa", sub="Czas", reg="n",
     ph="phǒm mâi mii wee-laa {ph} khráp", th="ผมไม่มีเวลา{th}ครับ",
     lit="mâi mii wee-laa = nie mieć czasu na coś",
     note="Po „mâi mii wee-laa” idzie czasownik bez żadnego łącznika. Polskie „żeby” nie ma tu odpowiednika.",
     ex_ph="mii wee-laa {ph} mǎi khráp", ex_th="มีเวลา{th}ไหมครับ",
     items=_v(CODZIENNE + ZALATWIANIE,
              "Nie mam czasu, żeby: %s.", "Masz czas, żeby: %s?")),

dict(key="KHIIKIAT", ty="sentence", cat="Cechy i opinie", sub="Niechęć", reg="p",
     ph="wan níi khîi kìat {ph} khráp", th="วันนี้ขี้เกียจ{th}ครับ",
     lit="khîi kìat = leniwy, nie chcieć się ruszyć",
     note="Potoczne i bardzo częste między znajomymi. NIE mów tego przełożonemu ani klientowi — zabrzmi jak wymówka.",
     ex_ph="khîi kìat {ph} rǒe khráp", ex_th="ขี้เกียจ{th}หรือครับ",
     items=_v(CODZIENNE + CODZ_RANO,
              "Nie chce mi się dziś: %s.", "Nie chce ci się dziś: %s?")),

dict(key="NAALAWNG", ty="sentence", cat="Cechy i opinie", sub="Zachęta", reg="n",
     ph="nâa lawng {ph} duu ná khráp", th="น่าลอง{th}ดูนะครับ",
     lit="nâa lawng … duu = aż się prosi, żeby spróbować",
     note="„nâa” przed czasownikiem tworzy ocenę: nâa duu = warto zobaczyć, nâa kin = wygląda apetycznie.",
     ex_ph="khoei lawng {ph} duu mǎi khráp", ex_th="เคยลอง{th}ดูไหมครับ",
     items=_v(CODZIENNE + RUCH,
              "Warto by spróbować: %s.", "Próbowałeś już kiedyś: %s?")),

dict(key="KHUANTANGTAERAEK", ty="sentence", cat="Gramatyka użytkowa", sub="Żal", reg="n",
     ph="khuan jà {ph} tâng tàae râek khráp", th="ควรจะ{th}ตั้งแต่แรกครับ",
     lit="tâng tàae râek = od samego początku",
     note="Tajski nie ma osobnego trybu „powinienem był”. Wyraża go „khuan jà” plus wskazanie przeszłego momentu.",
     ex_ph="thammai mâi {ph} tâng tàae râek khráp", ex_th="ทำไมไม่{th}ตั้งแต่แรกครับ",
     items=_v(ZALATWIANIE + RUCH,
              "Powinienem był od razu: %s.", "Czemu nie od razu: %s?")),

dict(key="KHAWKAWNDIIKWAA", ty="sentence", cat="Gramatyka użytkowa", sub="Kolejność", reg="n",
     ph="phǒm khǎw {ph} kàwn dii kwàa khráp", th="ผมขอ{th}ก่อนดีกว่าครับ",
     lit="… kàwn dii kwàa = lepiej najpierw to",
     note="„dii kwàa” na końcu to miękka propozycja, nie porównanie. Bardzo częste przy zmianie planu.",
     ex_ph="{ph} kàwn dii mǎi khráp", ex_th="{th}ก่อนดีไหมครับ",
     items=_v(CODZ_RANO + ZALATWIANIE,
              "Wolałbym najpierw: %s.", "Może najpierw: %s?")),

dict(key="LOEK", ty="sentence", cat="Gramatyka użytkowa", sub="Zaprzestanie", reg="n",
     ph="dǐao phǒm jà lôek {ph} khráp", th="เดี๋ยวผมจะเลิก{th}ครับ",
     lit="lôek = przestać robić coś na stałe",
     note="„lôek” to zerwanie z nawykiem. Chwilowa przerwa to „phák”, a jednorazowe zatrzymanie to „yùt”.",
     ex_ph="jà lôek {ph} mûea-rài khráp", ex_th="จะเลิก{th}เมื่อไหร่ครับ",
     items=_v(CODZIENNE + CODZ_RANO,
              "Zamierzam przestać: %s.", "Kiedy zamierzasz przestać: %s?")),

dict(key="KUEAPLUEM", ty="sentence", cat="Gramatyka użytkowa", sub="Pamięć", reg="n",
     ph="kùeap luem {ph} loei khráp", th="เกือบลืม{th}เลยครับ",
     lit="kùeap luem = o mało nie zapomniałem",
     note="„kùeap” opisuje coś, co prawie się stało, ale się nie stało. Zawsze o zdarzeniu niedokonanym.",
     ex_ph="luem {ph} rǔe plào khráp", ex_th="ลืม{th}หรือเปล่าครับ",
     items=_v(ZALATWIANIE + CODZIENNE,
              "O mało nie zapomniałem: %s.", "Zapomniałeś: %s?")),

dict(key="RIANWITHII", ty="sentence", cat="Praca i nauka", sub="Umiejętności", reg="n",
     ph="phǒm rian rúu wí-thii {ph} láew khráp", th="ผมเรียนรู้วิธี{th}แล้วครับ",
     lit="wí-thii = sposób, metoda",
     note="„wí-thii + czasownik” to „sposób na zrobienie czegoś”. Bez „wí-thii” zdanie mówiłoby o uczeniu się samej czynności.",
     ex_ph="rian wí-thii {ph} jàak khrai khráp", ex_th="เรียนวิธี{th}จากใครครับ",
     items=_v(CODZIENNE + ZALATWIANIE,
              "Nauczyłem się już, jak: %s.", "Od kogo nauczyłeś się, jak: %s?")),

dict(key="KHLAWNGKHUEN", ty="sentence", cat="Praca i nauka", sub="Postęp", reg="n",
     ph="phǒm {ph} dâai khlâwng khûen khráp", th="ผม{th}ได้คล่องขึ้นครับ",
     lit="khlâwng = płynnie, sprawnie",
     note="„khûen” po przymiotniku oznacza zmianę na plus: dii khûen, reo khûen, khlâwng khûen.",
     ex_ph="{ph} dâai khlâwng khûen mǎi khráp", ex_th="{th}ได้คล่องขึ้นไหมครับ",
     items=_v(CODZIENNE + RUCH,
              "Coraz sprawniej mi idzie: %s.", "Idzie ci coraz sprawniej: %s?")),

dict(key="CHINKAP", ty="sentence", cat="Gramatyka użytkowa", sub="Przyzwyczajenie", reg="n",
     ph="phǒm chin kàp kaan {ph} láew khráp", th="ผมชินกับการ{th}แล้วครับ",
     lit="chin kàp = przywyknąć do czegoś",
     note="„kaan” przed czasownikiem zamienia go w rzeczownik odczasownikowy — bez tego zdanie byłoby niegramatyczne.",
     ex_ph="chin kàp kaan {ph} rǔe yang khráp", ex_th="ชินกับการ{th}หรือยังครับ",
     items=_v(CODZ_RANO + RUCH,
              "Przyzwyczaiłem się do tego, żeby: %s.", "Przyzwyczaiłeś się już: %s?")),

dict(key="MAIMIIPRAYOT", ty="sentence", cat="Cechy i opinie", sub="Ocena", reg="n",
     ph="mâi mii prà-yòht thîi jà {ph} khráp", th="ไม่มีประโยชน์ที่จะ{th}ครับ",
     lit="prà-yòht = pożytek, korzyść",
     note="Mocna ocena. Wobec cudzego pomysłu lepiej zmiękczyć: „àat jà mâi khâwi mii prà-yòht”.",
     ex_ph="mii prà-yòht thîi jà {ph} mǎi khráp", ex_th="มีประโยชน์ที่จะ{th}ไหมครับ",
     items=_v(ZALATWIANIE + RUCH,
              "Nie ma sensu: %s.", "Jest sens: %s?")),

dict(key="PENBAANGKHRANG", ty="sentence", cat="Gramatyka użytkowa", sub="Częstotliwość", reg="n",
     ph="phǒm {ph} pen baang khráng khráp", th="ผม{th}เป็นบางครั้งครับ",
     lit="pen baang khráng = czasami, od przypadku do przypadku",
     note="Rzadsze niż „bàwi”, częstsze niż „mâi khâwi”. Ta trójka tworzy pełną skalę częstotliwości.",
     ex_ph="{ph} pen baang khráng rǒe khráp", ex_th="{th}เป็นบางครั้งหรือครับ",
     items=_v(CODZIENNE + CODZ_RANO,
              "Zdarza mi się czasem: %s.", "Zdarza ci się czasem: %s?")),

dict(key="LUEMWITHII", ty="sentence", cat="Gramatyka użytkowa", sub="Pamięć", reg="n",
     ph="phǒm luem wí-thii {ph} khráp", th="ผมลืมวิธี{th}ครับ",
     lit="luem wí-thii = zapomnieć, jak się coś robi",
     note="Inaczej niż „luem + rzecz”, tu chodzi o utraconą umiejętność, nie o zostawiony przedmiot.",
     ex_ph="chûai sǎwn wí-thii {ph} nòi khráp", ex_th="ช่วยสอนวิธี{th}หน่อยครับ",
     items=_v(ZALATWIANIE + CODZIENNE,
              "Zapomniałem, jak: %s.", "Naucz mnie, proszę, jak: %s.")),

dict(key="NATKAN", ty="sentence", cat="Small talk", sub="Umawianie się", reg="i",
     ph="nát kan {ph} ná khráp", th="นัดกัน{th}นะครับ",
     lit="nát kan = umówmy się na wspólne coś",
     note="„kan” oznacza wzajemność i wspólnotę działania. Bez niego zdanie znaczyłoby „umawiam sam siebie”.",
     ex_ph="nát kan {ph} wan nǎi dii khráp", ex_th="นัดกัน{th}วันไหนดีครับ",
     items=_v(RUCH + CODZIENNE,
              "Umówmy się, żeby razem: %s.", "Na kiedy umówimy się, żeby: %s?")),
]
