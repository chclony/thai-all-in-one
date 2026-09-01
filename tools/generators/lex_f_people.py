# -*- coding: utf-8 -*-
"""Sesja F — LUDZIE: rodzina, zawody, narodowosci, opis osoby.

Uwaga systemowa o rodzinie: tajski rozroznia strone matki i ojca oraz
starszenstwo. „phîi” to starsze rodzenstwo, „náwng” — mlodsze; plec
dodaje sie osobno (phîi chaai, phîi sǎao). Nie ma jednego slowa „brat”.
Te same slowa sluza jako grzecznosciowe zwroty do obcych: mlodsza
kelnerke wola sie „náwng”, starszego mezczyzne „phîi”.
"""

LR = "Ludzie i rodzina"
PN = "Praca i nauka"

PEOPLE = [

# ------------------------------------------------------------------ rodzina
("A1", "starszy brat", "phîi chaai", "พี่ชาย", LR, "Rodzina", 4, "n",
 "„phîi” oznacza starsze rodzeństwo niezależnie od płci; „chaai” dodaje męskość. Bez wieku nie da się poprawnie powiedzieć „brat”.",
 "starsze rodzeństwo mężczyzna",
 [("Mam starszego brata.", "phǒm mii phîi chaai khráp", "ผมมีพี่ชายครับ"),
  ("To mój starszy brat.", "níi phîi chaai phǒm khráp", "นี่พี่ชายผมครับ")],
 ["młodszy brat", "starsza siostra", "rodzina"], []),

("A1", "starsza siostra", "phîi sǎao", "พี่สาว", LR, "Rodzina", 4, "n",
 "„sǎao” to młoda kobieta. Uwaga na ton rosnący — „sàao” z innym tonem to zupełnie inne słowo.",
 "starsze rodzeństwo kobieta",
 [("Moja starsza siostra mieszka w Bangkoku.", "phîi sǎao phǒm yùu krung-thêep khráp", "พี่สาวผมอยู่กรุงเทพครับ"),
  ("Mam dwie starsze siostry.", "phǒm mii phîi sǎao sǎwng khon khráp", "ผมมีพี่สาวสองคนครับ")],
 ["starszy brat", "młodsza siostra", "rodzina"], []),

("A1", "młodszy brat", "náwng chaai", "น้องชาย", LR, "Rodzina", 4, "n",
 "Samo „náwng” to uprzejmy zwrot do młodszej osoby obsługującej — kelnera, sprzedawcy.",
 "młodsze rodzeństwo mężczyzna",
 [("To mój młodszy brat.", "níi náwng chaai phǒm khráp", "นี่น้องชายผมครับ"),
  ("Przepraszam, kelnerze.", "náwng khráp", "น้องครับ")],
 ["starszy brat", "młodsza siostra", "kelner"], []),

("A1", "młodsza siostra", "náwng sǎao", "น้องสาว", LR, "Rodzina", 4, "n",
 "Ten sam schemat: náwng plus płeć. Cały system rodzeństwa to cztery słowa z dwóch klocków.",
 "młodsze rodzeństwo kobieta",
 [("Moja młodsza siostra jest studentką.", "náwng sǎao phǒm pen nák sùek-sǎa khráp", "น้องสาวผมเป็นนักศึกษาครับ"),
  ("Mam młodszą siostrę.", "phǒm mii náwng sǎao khráp", "ผมมีน้องสาวครับ")],
 ["młodszy brat", "starsza siostra", "student"], []),

("A2", "dziadek (od strony ojca)", "pùu", "ปู่", LR, "Rodzina", 3, "n",
 "Strona ojca: pùu i yâa. Strona matki: taa i yaai. To rozróżnienie jest obowiązkowe.",
 "",
 [("Mój dziadek ma osiemdziesiąt lat.", "pùu phǒm aa-yú pàet-sìp pii khráp", "ปู่ผมอายุแปดสิบปีครับ"),
  ("Odwiedzam dziadka.", "phǒm pai yîam pùu khráp", "ผมไปเยี่ยมปู่ครับ")],
 ["babcia (od strony ojca)", "dziadek (od strony matki)", "odwiedzać"], []),

("A2", "babcia (od strony ojca)", "yâa", "ย่า", LR, "Rodzina", 3, "n",
 "Uwaga: „yâa” (babcia) i „yaa” (lek) i „yàa” (nie rób) to trzy różne słowa różniące się tonem.",
 "",
 [("Babcia gotuje bardzo dobrze.", "yâa tham aa-hǎan à-ròi mâak khráp", "ย่าทำอาหารอร่อยมากครับ"),
  ("Mieszkam z babcią.", "phǒm yùu kàp yâa khráp", "ผมอยู่กับย่าครับ")],
 ["dziadek (od strony ojca)", "lek", "gotować"], []),

("A2", "dziadek (od strony matki)", "taa", "ตา", LR, "Rodzina", 3, "n",
 "To samo słowo znaczy „oko”. Kontekst rozstrzyga bez trudu.",
 "",
 [("Mój dziadek jest rolnikiem.", "taa phǒm pen chaao naa khráp", "ตาผมเป็นชาวนาครับ"),
  ("Boli mnie oko.", "phǒm jèp taa khráp", "ผมเจ็บตาครับ")],
 ["babcia (od strony matki)", "oko", "rolnik"], []),

("A2", "babcia (od strony matki)", "yaai", "ยาย", LR, "Rodzina", 3, "n",
 "Cztery słowa na dziadków to system domknięty — warto zapamiętać je parami.",
 "",
 [("Babcia mieszka na wsi.", "yaai yùu tàang jang-wàt khráp", "ยายอยู่ต่างจังหวัดครับ"),
  ("Tęsknię za babcią.", "phǒm khít thǔeng yaai khráp", "ผมคิดถึงยายครับ")],
 ["dziadek (od strony matki)", "wieś", "tęsknić"], []),

("A2", "wujek", "lung", "ลุง", LR, "Rodzina", 3, "n",
 "„lung” to starszy brat rodzica, ale też uprzejmy zwrot do starszego mężczyzny — na przykład kierowcy.",
 "",
 [("To mój wujek.", "níi lung phǒm khráp", "นี่ลุงผมครับ"),
  ("Proszę pana, ile do dworca?", "lung khráp pai sà-thǎa-nii thâo-rài khráp", "ลุงครับไปสถานีเท่าไหร่ครับ")],
 ["ciotka", "kierowca"], []),

("A2", "ciotka", "pâa", "ป้า", LR, "Rodzina", 3, "n",
 "Podobnie: „pâa” to zwrot do starszej kobiety, na przykład sprzedawczyni na targu.",
 "",
 [("Ciotka prowadzi sklep.", "pâa khǎai khǎwng khráp", "ป้าขายของครับ"),
  ("Proszę pani, ile to kosztuje?", "pâa khráp an níi thâo-rài khráp", "ป้าครับอันนี้เท่าไหร่ครับ")],
 ["wujek", "targ", "sprzedawać"], []),

("A2", "kuzyn", "lûuk phîi lûuk náwng", "ลูกพี่ลูกน้อง", LR, "Rodzina", 2, "n",
 "Dosłownie „dziecko starszego, dziecko młodszego” — konstrukcja pokazuje logikę całego systemu.",
 "dziecko starszy dziecko młodszy",
 [("To mój kuzyn.", "níi lûuk phîi lûuk náwng phǒm khráp", "นี่ลูกพี่ลูกน้องผมครับ"),
  ("Mam wielu kuzynów.", "phǒm mii lûuk phîi lûuk náwng yóe khráp", "ผมมีลูกพี่ลูกน้องเยอะครับ")],
 ["starszy brat", "młodszy brat", "rodzina"], []),

("A2", "wnuk", "lǎan", "หลาน", LR, "Rodzina", 3, "n",
 "„lǎan” obejmuje wnuka i siostrzeńca — jedno słowo na dwie polskie kategorie.",
 "",
 [("To mój wnuk.", "níi lǎan phǒm khráp", "นี่หลานผมครับ"),
  ("Opiekuję się wnukiem.", "phǒm duu lae lǎan khráp", "ผมดูแลหลานครับ")],
 ["dziecko", "opiekować się", "dziadek (od strony ojca)"], ["siostrzeniec"]),

("A2", "teściowa", "mâe sǎa-mii", "แม่สามี", LR, "Rodzina", 2, "n",
 "Buduje się opisowo: matka męża albo matka żony. Nie ma osobnego słowa.",
 "matka mąż",
 [("To moja teściowa.", "níi mâe sǎa-mii chán khâ", "นี่แม่สามีฉันค่ะ"),
  ("Mieszkamy z teściami.", "rao yùu kàp khrâwp khrua sǎa-mii khâ", "เราอยู่กับครอบครัวสามีค่ะ")],
 ["mąż", "matka", "rodzina"], []),

("A2", "narzeczony", "khûu mân", "คู่หมั้น", LR, "Rodzina", 2, "n",
 "„khûu” to para. „khûu rák” to ukochana osoba, „faen” to potoczne „partner”.",
 "para zaręczony",
 [("To mój narzeczony.", "níi khûu mân chán khâ", "นี่คู่หมั้นฉันค่ะ"),
  ("Zaręczyliśmy się.", "rao mân kan láew khâ", "เราหมั้นกันแล้วค่ะ")],
 ["mąż", "żona", "ślub"], []),

("A2", "ślub", "ngaan tàeng ngaan", "งานแต่งงาน", LR, "Rodzina", 3, "n",
 "„ngaan” to zarazem praca i uroczystość: ngaan wan kòoet (urodziny), ngaan sòp (pogrzeb).",
 "uroczystość ubierać praca",
 [("Idę na ślub.", "phǒm pai ngaan tàeng ngaan khráp", "ผมไปงานแต่งงานครับ"),
  ("Kiedy jest ślub?", "tàeng ngaan mûea-rài khráp", "แต่งงานเมื่อไหร่ครับ")],
 ["mąż", "żona", "przyjęcie"], []),

# ------------------------------------------------------------------ zawody
("A2", "kelner", "phá-nák ngaan sòoep", "พนักงานเสิร์ฟ", PN, "Zawody", 3, "f",
 "„phá-nák ngaan” to ogólnie pracownik obsługi. W praktyce woła się „náwng khráp”.",
 "pracownik serwować",
 [("Kelner zaraz przyjdzie.", "phá-nák ngaan kam-lang maa khráp", "พนักงานกำลังมาครับ"),
  ("Przepraszam.", "náwng khráp", "น้องครับ")],
 ["młodszy brat", "restauracja", "rachunek"], []),

("A2", "kucharz", "phâw khrua", "พ่อครัว", PN, "Zawody", 3, "n",
 "Męski „phâw khrua” i żeński „mâe khrua” — dosłownie „ojciec kuchni”, „matka kuchni”.",
 "ojciec kuchnia",
 [("Kucharz jest bardzo dobry.", "phâw khrua kèng mâak khráp", "พ่อครัวเก่งมากครับ"),
  ("Moja mama świetnie gotuje.", "mâe khrua rúan níi kèng khráp", "แม่ครัวร้านนี้เก่งครับ")],
 ["gotować", "kuchnia", "restauracja"], []),

("A2", "kierowca", "khon khàp rót", "คนขับรถ", PN, "Zawody", 4, "n",
 "„khon” plus czynność tworzy nazwy wykonawców: khon khǎai (sprzedawca), khon tham ngaan (pracownik).",
 "osoba prowadzić pojazd",
 [("Kierowca czeka.", "khon khàp rót raw yùu khráp", "คนขับรถรออยู่ครับ"),
  ("Proszę powiedzieć kierowcy.", "bàwk khon khàp rót dûai khráp", "บอกคนขับรถด้วยครับ")],
 ["prowadzić", "taksówka", "samochód"], []),

("A2", "sprzedawca", "khon khǎai", "คนขาย", PN, "Zawody", 3, "n",
 "Na targu zwraca się do niego „phîi” albo „pâa”, nie nazwą zawodu.",
 "osoba sprzedawać",
 [("Zapytam sprzedawcy.", "phǒm jà thǎam khon khǎai khráp", "ผมจะถามคนขายครับ"),
  ("Sprzedawca powiedział, że nie ma.", "khon khǎai bàwk wâa mòt khráp", "คนขายบอกว่าหมดครับ")],
 ["kupować", "targ", "ciotka"], []),

("A2", "pielęgniarka", "phá-yaa-baan", "พยาบาล", PN, "Zawody", 3, "f",
 "„roong phá-yaa-baan” to szpital — dosłownie „dom pielęgnowania”.",
 "",
 [("Zawołam pielęgniarkę.", "phǒm jà rîak phá-yaa-baan khráp", "ผมจะเรียกพยาบาลครับ"),
  ("Jestem pielęgniarką.", "chán pen phá-yaa-baan khâ", "ฉันเป็นพยาบาลค่ะ")],
 ["szpital", "lekarz", "wołać"], []),

("A2", "inżynier", "wít-sà-wá-kawn", "วิศวกร", PN, "Zawody", 2, "f",
 "Zawód o wysokim statusie. „-kawn” kończy wiele nazw zawodów technicznych.",
 "",
 [("Jestem inżynierem.", "phǒm pen wít-sà-wá-kawn khráp", "ผมเป็นวิศวกรครับ"),
  ("Pracuje jako inżynier.", "kháo tham ngaan pen wít-sà-wá-kawn khráp", "เขาทำงานเป็นวิศวกรครับ")],
 ["praca", "zawód"], []),

("A2", "prawnik", "thá-naai khwaam", "ทนายความ", PN, "Zawody", 2, "f",
 "Potrzebne przy poważniejszych sprawach urzędowych i wypadkach.",
 "",
 [("Potrzebuję prawnika.", "phǒm tâwng kaan thá-naai khwaam khráp", "ผมต้องการทนายความครับ"),
  ("Zapytam prawnika.", "phǒm jà thǎam thá-naai khráp", "ผมจะถามทนายครับ")],
 ["policja", "umowa", "urząd"], []),

("A2", "rolnik", "chaao naa", "ชาวนา", PN, "Zawody", 3, "n",
 "„chaao” tworzy nazwy grup: chaao thai (Tajowie), chaao bâan (mieszkańcy wsi), chaao tàang châat (obcokrajowcy).",
 "mieszkaniec pole ryżowe",
 [("Mój dziadek był rolnikiem.", "taa phǒm pen chaao naa khráp", "ตาผมเป็นชาวนาครับ"),
  ("Rolnicy sadzą ryż.", "chaao naa plùuk khâao khráp", "ชาวนาปลูกข้าวครับ")],
 ["ryż", "wieś", "dziadek (od strony matki)"], []),

("A2", "obcokrajowiec", "chaao tàang châat", "ชาวต่างชาติ", LR, "Ludzie", 4, "n",
 "Formalne określenie. Potocznie o osobach z Zachodu mówi się „fà-ràng” — słowo neutralne, nie obraźliwe.",
 "mieszkaniec inny naród",
 [("Jestem obcokrajowcem.", "phǒm pen chaao tàang châat khráp", "ผมเป็นชาวต่างชาติครับ"),
  ("Cena dla obcokrajowców.", "raa-khaa sǎm-ràp chaao tàang châat khráp", "ราคาสำหรับชาวต่างชาติครับ")],
 ["cudzoziemiec z Zachodu", "kraj", "cena"], []),

("A2", "cudzoziemiec z Zachodu", "fà-ràng", "ฝรั่ง", LR, "Ludzie", 4, "p",
 "To samo słowo oznacza owoc gujawę. Określenie potoczne, ale bez negatywnego zabarwienia.",
 "",
 [("Jestem z Europy.", "phǒm pen fà-ràng khráp", "ผมเป็นฝรั่งครับ"),
  ("Poproszę gujawę.", "khǎw fà-ràng khráp", "ขอฝรั่งครับ")],
 ["obcokrajowiec", "owoc"], []),

# ------------------------------------------------------------- narodowosci
("A2", "Polska", "pra-thêet poo-laen", "ประเทศโปแลนด์", LR, "Narodowości", 4, "n",
 "„pra-thêet” to kraj i poprzedza nazwy państw. Przy narodowości używa się „khon” — khon poo-laen.",
 "kraj Polska",
 [("Jestem z Polski.", "phǒm maa jàak pra-thêet poo-laen khráp", "ผมมาจากประเทศโปแลนด์ครับ"),
  ("Jestem Polakiem.", "phǒm pen khon poo-laen khráp", "ผมเป็นคนโปแลนด์ครับ")],
 ["kraj", "od (miejsce)"], []),

("A2", "Tajlandia", "pra-thêet thai", "ประเทศไทย", LR, "Narodowości", 5, "n",
 "„thai” samo znaczy „wolny”. Tajowie mówią o sobie „khon thai”, o języku „phaa-sǎa thai”.",
 "kraj wolny",
 [("Lubię Tajlandię.", "phǒm châwp mueang thai khráp", "ผมชอบเมืองไทยครับ"),
  ("Uczę się tajskiego.", "phǒm rian phaa-sǎa thai khráp", "ผมเรียนภาษาไทยครับ")],
 ["język", "kraj", "uczyć się"], []),

("A2", "kraj", "pra-thêet", "ประเทศ", LR, "Narodowości", 4, "n",
 "Nieformalnie zamiast „pra-thêet thai” mówi się „mueang thai” — dosłownie „miasto Tajów”.",
 "",
 [("Z jakiego kraju pan jest?", "khun maa jàak pra-thêet à-rai khráp", "คุณมาจากประเทศอะไรครับ"),
  ("W moim kraju jest zimno.", "pra-thêet phǒm nǎao khráp", "ประเทศผมหนาวครับ")],
 ["Polska", "Tajlandia", "zimno"], []),

("A2", "język (mowa)", "phaa-sǎa", "ภาษา", LR, "Narodowości", 5, "n",
 "Nie mylić z „lín” — językiem w ustach. „phaa-sǎa ang-krìt” to angielski.",
 "",
 [("Mówi pan po angielsku?", "phûut phaa-sǎa ang-krìt dâai mǎi khráp", "พูดภาษาอังกฤษได้ไหมครับ"),
  ("Tajski jest trudny.", "phaa-sǎa thai yâak khráp", "ภาษาไทยยากครับ")],
 ["mówić", "język (w ustach)", "trudny"], []),

# ----------------------------------------------------------- opis czlowieka
("A2", "dorosły", "phûu yài", "ผู้ใหญ่", LR, "Ludzie", 3, "n",
 "„phûu yài” znaczy też „osoba wyższa rangą” — do takiej osoby zwraca się z większym szacunkiem.",
 "osoba duży",
 [("To bilet dla dorosłego.", "tǔa phûu yài khráp", "ตั๋วผู้ใหญ่ครับ"),
  ("Trzeba szanować starszych.", "tâwng khao-róp phûu yài khráp", "ต้องเคารพผู้ใหญ่ครับ")],
 ["dziecko", "bilet", "szanować"], []),

("A2", "nastolatek", "wai rûn", "วัยรุ่น", LR, "Ludzie", 3, "n",
 "„wai” to okres życia: wai dèk (dzieciństwo), wai tham ngaan (wiek produkcyjny).",
 "wiek pokolenie",
 [("To miejsce dla nastolatków.", "thîi nîi sǎm-ràp wai rûn khráp", "ที่นี่สำหรับวัยรุ่นครับ"),
  ("Mój syn jest nastolatkiem.", "lûuk chaai phǒm pen wai rûn khráp", "ลูกชายผมเป็นวัยรุ่นครับ")],
 ["dziecko", "dorosły", "syn"], []),

("A2", "starszy człowiek", "khon kàe", "คนแก่", LR, "Ludzie", 3, "n",
 "Uprzejmiej mówi się „phûu sǔung aa-yú”. „khon kàe” bywa odbierane jako zbyt bezpośrednie.",
 "osoba stary",
 [("Ustąp miejsca starszej osobie.", "sà-là thîi nâng hâi phûu sǔung aa-yú khráp", "สละที่นั่งให้ผู้สูงอายุครับ"),
  ("Mieszka tu starszy pan.", "mii khon kàe yùu thîi nîi khráp", "มีคนแก่อยู่ที่นี่ครับ")],
 ["stary (o człowieku)", "dorosły", "miejsce"], []),

("A2", "sąsiad", "phûean bâan", "เพื่อนบ้าน", LR, "Ludzie", 3, "n",
 "Dosłownie „przyjaciel domu”. Relacje sąsiedzkie w Tajlandii bywają bliskie i codzienne.",
 "przyjaciel dom",
 [("Mój sąsiad jest miły.", "phûean bâan jai dii khráp", "เพื่อนบ้านใจดีครับ"),
  ("Zapytam sąsiada.", "phǒm jà thǎam phûean bâan khráp", "ผมจะถามเพื่อนบ้านครับ")],
 ["sąsiedztwo", "przyjaciel", "dom"], []),

("A2", "gość", "khàek", "แขก", LR, "Ludzie", 3, "n",
 "Także „gość hotelowy”. „tâwn ráp khàek” to przyjmować gości.",
 "",
 [("Mam dziś gości.", "wan níi mii khàek khráp", "วันนี้มีแขกครับ"),
  ("Gość hotelowy.", "khàek roong raem khráp", "แขกโรงแรมครับ")],
 ["hotel", "zapraszać", "przyjęcie"], []),

("A2", "grupa ludzi", "klùm", "กลุ่ม", LR, "Ludzie", 3, "n",
 "Przydatne przy rezerwacji: „maa pen klùm” — przychodzimy grupą.",
 "",
 [("Przyszliśmy grupą.", "rao maa pen klùm khráp", "เรามาเป็นกลุ่มครับ"),
  ("Grupa dziesięciu osób.", "klùm sìp khon khráp", "กลุ่มสิบคนครับ")],
 ["rezerwować", "osoba", "razem"], []),

("A2", "tłum", "khon yóe", "คนเยอะ", LR, "Ludzie", 4, "p",
 "Dosłownie „dużo ludzi”. Codzienne wyjaśnienie spóźnienia albo długiej kolejki.",
 "osoba dużo",
 [("Jest dużo ludzi.", "khon yóe khráp", "คนเยอะครับ"),
  ("Rano jest tłoczno.", "tawn cháo khon yóe khráp", "ตอนเช้าคนเยอะครับ")],
 ["kolejka", "spóźnić się", "cicho"], []),
]
