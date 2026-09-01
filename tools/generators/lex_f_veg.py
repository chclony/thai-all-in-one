# -*- coding: utf-8 -*-
"""Sesja F — WARZYWA. System zamkniety.

Dobor: warzywa faktycznie obecne na tajskim targu i w karcie dan. Kazde haslo
powiazane z daniem, w ktorym uczacy sie je spotka — powiazania maja dzialac
w aplikacji, a nie byc ozdoba.
"""

CAT = "Jedzenie i napoje"
SUB = "Warzywa"

VEG = [

("A1", "warzywo", "phàk", "ผัก", CAT, SUB, 5, "n",
 "Wyraz nadrzędny całej grupy. „phàk” zaczyna też nazwy wielu konkretnych warzyw, np. „phàk bûng”, „phàk kàat”.",
 "",
 [("Lubię warzywa.", "phǒm châwp phàk khráp", "ผมชอบผักครับ"),
  ("Poproszę więcej warzyw.", "khǎw phàk phôoem khráp", "ขอผักเพิ่มครับ"),
  ("Jem tylko warzywa.", "phǒm kin tàe phàk khráp", "ผมกินแต่ผักครับ")],
 ["ogórek", "kapusta", "jarski"], []),

("A2", "ogórek", "taeng-kwaa", "แตงกวา", CAT, SUB, 4, "n",
 "Podawany na surowo obok ostrych dań — Tajowie traktują go jak chłodzący dodatek, nie jak sałatkę.",
 "",
 [("Poproszę bez ogórka.", "mâi sài taeng-kwaa khráp", "ไม่ใส่แตงกวาครับ"),
  ("Ogórek jest chłodzący.", "taeng-kwaa yen khráp", "แตงกวาเย็นครับ")],
 ["warzywo", "pomidor", "sałatka"], []),

("A2", "pomidor", "má-khǔea thêet", "มะเขือเทศ", CAT, SUB, 4, "n",
 "Dosłownie „zagraniczny bakłażan” — Tajowie zaliczyli pomidora do rodziny bakłażanów.",
 "bakłażan zagraniczny",
 [("Poproszę bez pomidorów.", "mâi sài má-khǔea thêet khráp", "ไม่ใส่มะเขือเทศครับ"),
  ("Sok pomidorowy poproszę.", "khǎw nám má-khǔea thêet khráp", "ขอน้ำมะเขือเทศครับ")],
 ["bakłażan", "ogórek", "warzywo"], []),

("A2", "marchewka", "kae-ràwt", "แครอท", CAT, SUB, 3, "n",
 "Zapożyczenie z angielskiego. Końcowe „t” jest niezwolnione — zatrzymujesz dźwięk, nie wybuchasz nim.",
 "",
 [("Poproszę z marchewką.", "sài kae-ràwt dûai khráp", "ใส่แครอทด้วยครับ"),
  ("Dzieci lubią marchewkę.", "dèk châwp kae-ràwt khráp", "เด็กชอบแครอทครับ")],
 ["warzywo", "ziemniak"], []),

("A2", "cebula", "hǔa hǎwm", "หัวหอม", CAT, SUB, 4, "n",
 "Dosłownie „pachnąca głowa”. Dwa tony rosnące z rzędu — trudne, ćwicz powoli.",
 "głowa pachnąca",
 [("Poproszę bez cebuli.", "mâi sài hǔa hǎwm khráp", "ไม่ใส่หัวหอมครับ"),
  ("Muszę kupić cebulę.", "phǒm tâwng súe hǔa hǎwm khráp", "ผมต้องซื้อหัวหอมครับ")],
 ["czosnek", "warzywo", "dymka"], []),

("A2", "dymka", "tôn hǎwm", "ต้นหอม", CAT, SUB, 4, "n",
 "Zielona część, którą posypuje się zupę. „tôn” to łodyga, „hǎwm” to zapach.",
 "łodyga pachnąca",
 [("Poproszę bez dymki.", "mâi sài tôn hǎwm khráp", "ไม่ใส่ต้นหอมครับ"),
  ("Zupa z dymką jest lepsza.", "sài tôn hǎwm à-ròi kwàa khráp", "ใส่ต้นหอมอร่อยกว่าครับ")],
 ["cebula", "kolendra", "zupa"], ["szczypiorek"]),

("A2", "kolendra", "phàk chii", "ผักชี", CAT, SUB, 4, "n",
 "Warto znać, żeby móc odmówić — dla części Europejczyków smakuje jak mydło. „mâi sài phàk chii” to zdanie ratunkowe.",
 "",
 [("Poproszę bez kolendry.", "mâi sài phàk chii khráp", "ไม่ใส่ผักชีครับ"),
  ("Nie lubię kolendry.", "phǒm mâi châwp phàk chii khráp", "ผมไม่ชอบผักชีครับ")],
 ["dymka", "warzywo"], []),

("A2", "czosnek", "krà-thiam", "กระเทียม", CAT, SUB, 4, "n",
 "„kh” po „t” to przydech — „thiam”, nie „tiam”. Podstawa większości dań smażonych.",
 "",
 [("Poproszę bez czosnku.", "mâi sài krà-thiam khráp", "ไม่ใส่กระเทียมครับ"),
  ("Wieprzowina z czosnkiem i pieprzem.", "mǔu thâwt krà-thiam phrík-thai", "หมูทอดกระเทียมพริกไทย")],
 ["cebula", "chili", "warzywo"], []),

("A2", "kapusta", "kà-làm-plii", "กะหล่ำปลี", CAT, SUB, 3, "n",
 "Trzy sylaby, ostatnia długa. Podawana surowa do sałatki som tam.",
 "",
 [("Poproszę smażoną kapustę.", "khǎw kà-làm-plii phàt khráp", "ขอกะหล่ำปลีผัดครับ"),
  ("Kapusta jest tania.", "kà-làm-plii thùuk khráp", "กะหล่ำปลีถูกครับ")],
 ["warzywo", "sałata"], []),

("A2", "sałata", "phàk kàat", "ผักกาด", CAT, SUB, 3, "n",
 "Ogólne określenie liściastych. W restauracji zachodniej usłyszysz też „sà-làt”.",
 "",
 [("Poproszę sałatę do tego.", "khǎw phàk kàat dûai khráp", "ขอผักกาดด้วยครับ"),
  ("Ta sałata jest świeża.", "phàk kàat níi sòt khráp", "ผักกาดนี้สดครับ")],
 ["kapusta", "warzywo", "świeży"], []),

("A2", "ziemniak", "man fà-ràng", "มันฝรั่ง", CAT, SUB, 4, "n",
 "Dosłownie „zagraniczny korzeń”. „fà-ràng” to również określenie białego cudzoziemca — to samo słowo.",
 "korzeń zagraniczny",
 [("Poproszę frytki.", "khǎw man fà-ràng thâwt khráp", "ขอมันฝรั่งทอดครับ"),
  ("Nie mamy ziemniaków.", "mâi mii man fà-ràng khráp", "ไม่มีมันฝรั่งครับ")],
 ["marchewka", "warzywo", "smażyć na głębokim"], []),

("A2", "papryka", "phrík yùak", "พริกหยวก", CAT, SUB, 3, "n",
 "Papryka słodka, duża. Nie mylić z „phrík” samym w sobie, które znaczy chili i będzie ostre.",
 "chili łagodne",
 [("Poproszę z papryką.", "sài phrík yùak dûai khráp", "ใส่พริกหยวกด้วยครับ"),
  ("Papryka nie jest ostra.", "phrík yùak mâi phèt khráp", "พริกหยวกไม่เผ็ดครับ")],
 ["chili", "warzywo"], []),

("A1", "chili", "phrík", "พริก", CAT, SUB, 5, "n",
 "Najważniejsze słowo tej grupy dla obcokrajowca. „mâi sài phrík” oznacza „bez chili” i bywa jedyną obroną przed daniem nie do zjedzenia.",
 "",
 [("Poproszę bez chili.", "mâi sài phrík khráp", "ไม่ใส่พริกครับ"),
  ("Ile chili?", "phrík kìi mét khráp", "พริกกี่เม็ดครับ"),
  ("To ma dużo chili.", "an níi phrík yóe khráp", "อันนี้พริกเยอะครับ")],
 ["papryka", "ostry", "czosnek"], ["papryczka"]),

("A2", "bakłażan", "má-khǔea yaao", "มะเขือยาว", CAT, SUB, 3, "n",
 "Tajski bakłażan bywa okrągły i zielony. „yaao” (długi) wskazuje odmianę podłużną, znaną z Europy.",
 "bakłażan długi",
 [("Poproszę smażony bakłażan.", "khǎw má-khǔea yaao phàt khráp", "ขอมะเขือยาวผัดครับ"),
  ("Bakłażan jest miękki.", "má-khǔea yaao nûm khráp", "มะเขือยาวนุ่มครับ")],
 ["pomidor", "warzywo"], []),

("A2", "kukurydza", "khâao phôot", "ข้าวโพด", CAT, SUB, 4, "n",
 "Dosłownie „ryż kukurydziany” — „khâao” to nazwa nadrzędna zbóż, nie tylko ryżu.",
 "ryż kukurydziany",
 [("Poproszę gotowaną kukurydzę.", "khǎw khâao phôot tôm khráp", "ขอข้าวโพดต้มครับ"),
  ("Sałatka z kukurydzą.", "sà-làt sài khâao phôot", "สลัดใส่ข้าวโพด")],
 ["warzywo", "gotować w wodzie"], []),

("A2", "fasolka szparagowa", "thùa fàk yaao", "ถั่วฝักยาว", CAT, SUB, 3, "n",
 "Tajska odmiana jest bardzo długa, jada się ją także na surowo do som tam.",
 "fasola strąk długi",
 [("Poproszę smażoną fasolkę.", "khǎw thùa fàk yaao phàt khráp", "ขอถั่วฝักยาวผัดครับ"),
  ("Fasolka jest chrupiąca.", "thùa fàk yaao kràwp khráp", "ถั่วฝักยาวกรอบครับ")],
 ["kiełki fasoli", "warzywo"], ["fasolka"]),

("A2", "kiełki fasoli", "thùa ngâwk", "ถั่วงอก", CAT, SUB, 4, "n",
 "Nieodłączny dodatek do pad thai i zup z makaronem. Podawane surowe obok talerza.",
 "fasola kiełkująca",
 [("Poproszę bez kiełków.", "mâi sài thùa ngâwk khráp", "ไม่ใส่ถั่วงอกครับ"),
  ("Poproszę więcej kiełków.", "khǎw thùa ngâwk phôoem khráp", "ขอถั่วงอกเพิ่มครับ")],
 ["fasolka szparagowa", "pad thai", "warzywo"], ["kiełki"]),

("A2", "dynia", "fák thawng", "ฟักทอง", CAT, SUB, 3, "n",
 "Dosłownie „złota tykwa”. Bywa w curry i w deserach z mlekiem kokosowym.",
 "tykwa złota",
 [("Curry z dynią jest słodkie.", "kaeng fák thawng wǎan khráp", "แกงฟักทองหวานครับ"),
  ("Poproszę gotowaną dynię.", "khǎw fák thawng nûeng khráp", "ขอฟักทองนึ่งครับ")],
 ["warzywo", "gotować na parze", "złoty"], []),

("A2", "szpinak wodny", "phàk bûng", "ผักบุ้ง", CAT, SUB, 4, "n",
 "Najczęstsze warzywo w tajskim menu. Danie „phàk bûng fai daeng” to jedna z pierwszych rzeczy, jakie warto umieć zamówić.",
 "",
 [("Poproszę smażony szpinak wodny.", "khǎw phàk bûng fai daeng khráp", "ขอผักบุ้งไฟแดงครับ"),
  ("Szpinak wodny jest tani i dobry.", "phàk bûng thùuk láe à-ròi khráp", "ผักบุ้งถูกและอร่อยครับ")],
 ["warzywo", "smażyć na patelni", "czerwony"], []),

("A2", "grzyb", "hèt", "เห็ด", CAT, SUB, 4, "n",
 "Krótka samogłoska, końcowe „t” niezwolnione. Częsty składnik zupy tom yum.",
 "",
 [("Poproszę z grzybami.", "sài hèt dûai khráp", "ใส่เห็ดด้วยครับ"),
  ("Nie jem grzybów.", "phǒm mâi kin hèt khráp", "ผมไม่กินเห็ดครับ")],
 ["warzywo", "zupa"], []),

("A2", "imbir", "khǐng", "ขิง", CAT, SUB, 3, "n",
 "Ton rosnący. W herbacie i w rosole z kurczaka.",
 "",
 [("Herbata z imbirem, proszę.", "khǎw chaa khǐng khráp", "ขอชาขิงครับ"),
  ("Poproszę bez imbiru.", "mâi sài khǐng khráp", "ไม่ใส่ขิงครับ")],
 ["czosnek", "warzywo", "herbata"], []),

("A2", "rzodkiew", "hǔa chái-tháo", "หัวไชเท้า", CAT, SUB, 2, "n",
 "Biała, długa. W zupach z wieprzowiną.",
 "głowa rzodkwi",
 [("W zupie jest rzodkiew.", "nai súp mii hǔa chái-tháo khráp", "ในซุปมีหัวไชเท้าครับ"),
  ("Rzodkiew jest miękka.", "hǔa chái-tháo nûm khráp", "หัวไชเท้านุ่มครับ")],
 ["warzywo", "zupa"], []),

("A2", "jarski", "je", "เจ", CAT, SUB, 4, "n",
 "Kluczowe słowo dla wegetarianina. „aa-hǎan je” wyklucza mięso, ale też czosnek i cebulę. Łagodniejsza wersja to „mang-sà-wí-rát”.",
 "",
 [("Jestem wegetarianinem.", "phǒm kin je khráp", "ผมกินเจครับ"),
  ("Czy macie dania jarskie?", "mii aa-hǎan je mǎi khráp", "มีอาหารเจไหมครับ"),
  ("Poproszę bez mięsa.", "mâi sài núea sàt khráp", "ไม่ใส่เนื้อสัตว์ครับ")],
 ["warzywo", "wegetariański"], ["wegański"]),

("A2", "wegetariański", "mang-sà-wí-rát", "มังสวิรัติ", CAT, SUB, 3, "f",
 "Słowo formalne, z sanskrytu. W przeciwieństwie do „je” dopuszcza czosnek i cebulę, więc dla większości Europejczyków jest trafniejsze.",
 "",
 [("Jestem wegetarianinem.", "phǒm pen mang-sà-wí-rát khráp", "ผมเป็นมังสวิรัติครับ"),
  ("Poproszę danie wegetariańskie.", "khǎw aa-hǎan mang-sà-wí-rát khráp", "ขออาหารมังสวิรัติครับ")],
 ["jarski", "warzywo"], []),

("A2", "świeży", "sòt", "สด", CAT, SUB, 4, "n",
 "O warzywach, rybie i soku. „nám phǒn-lá-mái sòt” to sok świeżo wyciskany.",
 "",
 [("Te warzywa są świeże.", "phàk níi sòt khráp", "ผักนี้สดครับ"),
  ("Poproszę świeży sok.", "khǎw nám phǒn-lá-mái sòt khráp", "ขอน้ำผลไม้สดครับ")],
 ["warzywo", "sałata"], []),

("A2", "surowy", "dìp", "ดิบ", CAT, SUB, 3, "n",
 "Ważne przy zamawianiu — „núea dìp” to mięso surowe. Krótka samogłoska, końcowe „p” niezwolnione.",
 "",
 [("Nie jem surowego mięsa.", "phǒm mâi kin núea dìp khráp", "ผมไม่กินเนื้อดิบครับ"),
  ("Te warzywa są surowe.", "phàk níi dìp khráp", "ผักนี้ดิบครับ")],
 ["świeży", "warzywo"], []),
]
