# -*- coding: utf-8 -*-
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import polish_read, tone_guide, syllables
from lex_dialogues import DIALOGUES

OUT = "/home/claude/thai/data"
VERSION = "1.0.0"

# ------------------------------------------------------------------ DIALOGI
dlgs = []
for i, (title, sit, level, ra, rb, lines, note) in enumerate(DIALOGUES, 1):
    dlgs.append({
        "id": "dlg-%04d" % i,
        "type": "dialogue",
        "title": title,
        "situation": sit,
        "category": sit,
        "level": level,
        "roles": {"A": ra, "B": rb},
        "notes": note,
        "tags": ["dialog", sit.split()[0].lower(), level.lower()],
        "lines": [{
            "index": n,
            "role": r,
            "polish": pl,
            "thaiPhonetic": ph,
            "pronunciationPolish": polish_read(ph),
            "toneGuide": tone_guide(ph),
            "ttsThai": th,
            "audioFile": "",
        } for n, (r, pl, ph, th) in enumerate(lines, 1)],
        "source": "Baza projektu Thai All-in-One",
        "license": "Do weryfikacji przed publiczną publikacją",
    })

with open(os.path.join(OUT, "dialogues-part-01.json"), "w", encoding="utf-8") as f:
    json.dump({"file": "dialogues-part-01.json", "count": len(dlgs),
               "lineCount": sum(len(d["lines"]) for d in dlgs), "records": dlgs},
              f, ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- GRAMATYKA
def P(pl, ph, th):
    return {"polish": pl, "thaiPhonetic": ph, "pronunciationPolish": polish_read(ph), "ttsThai": th}

GRAM = [
 ("Czasownik się nie odmienia", "Survival",
  "Tajski czasownik ma jedną formę. Nie ma odmiany przez osoby, liczby ani czasy. Kto i kiedy — wynika z kontekstu i z dodatkowych słówek.",
  [P("Ja jem.", "phǒm kin", "ผมกิน"), P("On je.", "kháw kin", "เขากิน"), P("Jemy.", "rao kin", "เรากิน")],
  "Nie szukaj końcówek — szukaj słów-wskaźników: jà, láew, yang."),
 ("Szyk zdania: podmiot – czasownik – dopełnienie", "Survival",
  "Podstawowy szyk jest taki jak w polskim zdaniu neutralnym: kto – co robi – co.",
  [P("Ja jem ryż.", "phǒm kin khâaw", "ผมกินข้าว"), P("Ona kupuje owoce.", "kháw súe phǒn-la-máai", "เขาซื้อผลไม้")],
  "Podmiot można pominąć, jeśli jest oczywisty."),
 ("Przeczenie: mâi przed czasownikiem", "Survival",
  "Aby zaprzeczyć, wstaw mâi bezpośrednio przed czasownik lub przymiotnik.",
  [P("Nie jem.", "phǒm mâi kin", "ผมไม่กิน"), P("Nie jest drogie.", "mâi phaeng", "ไม่แพง"), P("Nie mam.", "mâi mii", "ไม่มี")],
  "mâi ma ton opadający — wypowiadaj je zdecydowanie."),
 ("Pytania z mǎi", "Survival",
  "Pytanie o tak/nie tworzysz, dodając mǎi na końcu zdania.",
  [P("Jest woda?", "mii náam mǎi", "มีน้ำไหม"), P("Jest ostre?", "phèt mǎi", "เผ็ดไหม")],
  "Odpowiedź: powtórz czasownik (mii = jest) albo zaprzecz (mâi mii)."),
 ("Pytania potwierdzające: châi mǎi", "A1",
  "châi mǎi to odpowiednik polskiego „prawda?”.",
  [P("Jedziesz do Bangkoku, prawda?", "khun pai krung-thêep châi mǎi", "คุณไปกรุงเทพใช่ไหม")],
  "Odpowiedź: châi (tak) albo mâi châi (nie)."),
 ("Możliwość i zgoda: dâai", "Survival",
  "dâai po czasowniku znaczy „można / da się / potrafię”. W pytaniu: dâai mǎi.",
  [P("Czy mogę zapłacić kartą?", "jàai bàt dâai mǎi", "จ่ายบัตรได้ไหม"),
   P("Nie mogę jeść ostrego.", "kin phèt mâi dâai", "กินเผ็ดไม่ได้")],
  "dâai = można; mâi dâai = nie można."),
 ("Partykuły grzecznościowe khráp i khâ", "Survival",
  "Mężczyzna kończy zdanie khráp, kobieta khâ (w pytaniu khá). To najprostszy sposób, by brzmieć uprzejmie.",
  [P("Dziękuję (mężczyzna).", "khàwp-khun khráp", "ขอบคุณครับ"),
   P("Dziękuję (kobieta).", "khàwp-khun khâ", "ขอบคุณค่ะ")],
  "Bez tych partykuł zdanie brzmi szorstko."),
 ("Zaimki i formy adresatywne", "Survival",
  "phǒm — ja (mężczyzna), chǎn — ja (kobieta), khun — pan/pani/ty. Do osoby starszej mówi się phîi, do młodszej náwng.",
  [P("Jak masz na imię?", "khun chûe à-rai", "คุณชื่ออะไร"),
   P("Przepraszam (do starszej osoby).", "khǎw thôot khráp phîi", "ขอโทษครับพี่")],
  "Tajowie często mówią o sobie po imieniu zamiast „ja”."),
 ("Czas przyszły: jà", "A1",
  "jà przed czasownikiem sygnalizuje przyszłość lub zamiar.",
  [P("Pojadę jutro.", "phrûng níi phǒm jà pai", "พรุ่งนี้ผมจะไป"),
   P("Zapłacę.", "phǒm jà jàai", "ผมจะจ่าย")],
  "Jeśli w zdaniu jest wyraz czasu, jà bywa pomijane."),
 ("Czynność zakończona: láew", "A1",
  "láew na końcu zdania oznacza, że coś się już wydarzyło albo zmienił się stan.",
  [P("Już zjadłem.", "kin láew", "กินแล้ว"), P("Już rozumiem.", "khâo-jai láew", "เข้าใจแล้ว")],
  "To nie jest czas przeszły, tylko sygnał zakończenia."),
 ("Jeszcze nie: yang mâi dâai", "A1",
  "yang = jeszcze; yang mâi dâai + czasownik = jeszcze czegoś nie zrobiłem.",
  [P("Jeszcze nie jadłem.", "yang mâi dâai kin", "ยังไม่ได้กิน"),
   P("Jeszcze nie zapłaciłem.", "yang mâi dâai jàai", "ยังไม่ได้จ่าย")],
  "Na pytanie „… rúe yang” odpowiadasz láew albo yang."),
 ("Klasyfikatory", "A1",
  "Licząc rzeczy, używasz schematu: rzecz + liczba + klasyfikator. Najczęstsze: khon (ludzie), an (rzeczy), bai (sztuki, bilety), tua (zwierzęta, ubrania), khùat (butelki), jaan (talerze), thîi (porcje).",
  [P("Dwie osoby", "sǎwng khon", "สองคน"), P("Trzy butelki wody", "náam sǎam khùat", "น้ำสามขวด"),
   P("Poproszę jedną porcję.", "khǎw nùeng thîi", "ขอหนึ่งที่")],
  "Gdy nie znasz klasyfikatora, an zwykle przejdzie."),
 ("Liczby i ceny", "Survival",
  "Ceny podaje się w bahtach: liczba + bàat. Pytanie o cenę: thâo-rài.",
  [P("Ile to kosztuje?", "níi thâo-rài", "นี่เท่าไหร่"), P("Sto bahtów.", "nùeng ráwi bàat", "หนึ่งร้อยบาท")],
  "„za sztukę/dzień/kilogram” oddaje się słówkiem lá: wan lá, kì-loo lá."),
 ("Grzeczna prośba: khǎw … nòi", "Survival",
  "khǎw = proszę o. nòi łagodzi prośbę i brzmi naturalnie.",
  [P("Poproszę wodę.", "khǎw náam nòi", "ขอน้ำหน่อย"), P("Poproszę menu.", "khǎw mee-nuu nòi", "ขอเมนูหน่อย")],
  "Ten wzorzec działa zawsze, gdy chcesz coś dostać."),
 ("Prośba o przysługę: chûai … nòi dâai mǎi", "Survival",
  "chûai = pomóż. Ten wzorzec to najgrzeczniejsza prośba o czynność.",
  [P("Czy możesz mi pomóc?", "chûai phǒm nòi dâai mǎi", "ช่วยผมหน่อยได้ไหม"),
   P("Czy możesz mówić wolniej?", "chûai phûut cháa cháa nòi dâai mǎi", "ช่วยพูดช้าๆ หน่อยได้ไหม")],
  ""),
 ("Chcieć, musieć, móc", "A1",
  "yàak + czasownik = chcieć coś zrobić; tâwng = musieć; dâai = móc. Chcąc rzecz, użyj ao lub tâwng-kaan.",
  [P("Chcę jechać.", "phǒm yàak pai", "ผมอยากไป"), P("Muszę już iść.", "phǒm tâwng pai láew", "ผมต้องไปแล้ว"),
   P("Poproszę to.", "ao an níi", "เอาอันนี้")],
  "yàak dotyczy czynności, ao — rzeczy."),
 ("Słowa pytające", "Survival",
  "Pytajnik zwykle stoi tam, gdzie w odpowiedzi stanęłaby informacja — najczęściej na końcu.",
  [P("Co to jest?", "nîi à-rai", "นี่อะไร"), P("Gdzie jest toaleta?", "hâwng náam yùu thîi nǎi", "ห้องน้ำอยู่ที่ไหน"),
   P("Kiedy przyjedziesz?", "maa mûea rài", "มาเมื่อไหร่")],
  "Nie zmieniasz szyku zdania jak w angielskim."),
 ("Przymiotnik po rzeczowniku", "A1",
  "Przymiotnik stoi za rzeczownikiem i nie potrzebuje czasownika „być”.",
  [P("gorąca woda", "náam ráwn", "น้ำร้อน"), P("Jedzenie jest smaczne.", "aa-hǎan à-ròi", "อาหารอร่อย")],
  "„jest” dodajesz tylko przy rzeczownikach: khue / pen."),
 ("Stopniowanie: mâak, nít nòi, koen pai", "A1",
  "mâak = bardzo, nít nòi = trochę, … koen pai = za bardzo. Wszystkie stoją po przymiotniku.",
  [P("bardzo ostre", "phèt mâak", "เผ็ดมาก"), P("trochę ostre", "phèt nít nòi", "เผ็ดนิดหน่อย"),
   P("za drogie", "phaeng koen pai", "แพงเกินไป")],
  ""),
 ("Porównania: kwàa i thîi sùt", "A1",
  "kwàa = bardziej niż, thîi sùt = najbardziej.",
  [P("tańsze niż to", "thùuk kwàa níi", "ถูกกว่านี้"), P("najsmaczniejsze", "à-ròi thîi sùt", "อร่อยที่สุด")],
  ""),
 ("Miejsce: yùu, nai, bon, khâang", "A1",
  "yùu = znajdować się; nai = w; bon = na; khâang nâa = przed; khâang lǎng = za.",
  [P("Jestem w hotelu.", "phǒm yùu nai roong raem", "ผมอยู่ในโรงแรม"),
   P("Jest przed sklepem.", "yùu khâang nâa ráan", "อยู่ข้างหน้าร้าน")],
  ""),
 ("Kierunek: pai i maa", "A1",
  "pai = ruch od mówiącego, maa = ruch w stronę mówiącego. Dodaje się je po czasowniku ruchu.",
  [P("Idź prosto.", "trong pai", "ตรงไป"), P("Przynieś to.", "ao maa", "เอามา")],
  ""),
 ("Czynność trwająca: kamlang", "A1",
  "kamlang przed czasownikiem = właśnie coś robię. Na końcu można dodać yùu.",
  [P("Właśnie jem.", "kamlang kin yùu", "กำลังกินอยู่"), P("Czekam na ciebie.", "kamlang raw khun yùu", "กำลังรอคุณอยู่")],
  ""),
 ("Doświadczenie: khoei", "A1",
  "khoei przed czasownikiem = kiedyś, miałem okazję. mâi khoei = nigdy.",
  [P("Byłem już w Tajlandii.", "khoei maa thai láew", "เคยมาไทยแล้ว"),
   P("Nigdy tego nie jadłem.", "mâi khoei kin", "ไม่เคยกิน")],
  ""),
 ("Za jednostkę: lá", "A1",
  "lá po jednostce znaczy „za jeden”: wan lá = za dzień, khuen lá = za noc, kì-loo lá = za kilogram.",
  [P("Ile za noc?", "khuen lá thâo-rài", "คืนละเท่าไหร่"), P("Sto bahtów za dzień.", "wan lá nùeng ráwi bàat", "วันละหนึ่งร้อยบาท")],
  ""),
 ("Czy już? — rúe yang", "A1",
  "Pytanie o wykonanie czynności: zdanie + rúe yang. Odpowiedź: láew (już) albo yang (jeszcze nie).",
  [P("Jadłeś już?", "kin khâaw rúe yang", "กินข้าวหรือยัง"), P("Jeszcze nie.", "yang", "ยัง")],
  "„kin khâaw rúe yang” to popularne powitanie, jak nasze „co słychać”."),
]

grammar = []
for i, (title, level, expl, pats, tip) in enumerate(GRAM, 1):
    grammar.append({"id": "gram-%03d" % i, "title": title, "level": level,
                    "explanation": expl, "patterns": pats, "tip": tip,
                    "tags": ["gramatyka", level.lower()]})
with open(os.path.join(OUT, "grammar.json"), "w", encoding="utf-8") as f:
    json.dump({"file": "grammar.json", "count": len(grammar), "records": grammar},
              f, ensure_ascii=False, indent=1)

# ------------------------------------------------------------------- WYMOWA
tones = [
 {"id": "tone-mid", "symbol": "ā", "name": "ton średni", "description":
  "Głos płaski, na naturalnej wysokości mowy. Nie podnosisz go ani nie opuszczasz.",
  "example": {"polish": "iść", "thaiPhonetic": "pai", "ttsThai": "ไป"}},
 {"id": "tone-low", "symbol": "à", "name": "ton niski", "description":
  "Głos płaski, ale niżej niż zwykle. Wyobraź sobie spokojne, zmęczone „aha”.",
  "example": {"polish": "kurczak", "thaiPhonetic": "kài", "ttsThai": "ไก่"}},
 {"id": "tone-falling", "symbol": "â", "name": "ton opadający", "description":
  "Zaczynasz wysoko i wyraźnie opadasz, jak przy polskim „nie!” wypowiedzianym stanowczo.",
  "example": {"polish": "nie", "thaiPhonetic": "mâi", "ttsThai": "ไม่"}},
 {"id": "tone-high", "symbol": "á", "name": "ton wysoki", "description":
  "Głos wyżej niż normalnie i lekko napięty, utrzymany do końca sylaby.",
  "example": {"polish": "woda", "thaiPhonetic": "náam", "ttsThai": "น้ำ"}},
 {"id": "tone-rising", "symbol": "ǎ", "name": "ton rosnący", "description":
  "Głos schodzi lekko w dół i wznosi się do góry, jak w polskim pytaniu „tak?”.",
  "example": {"polish": "ja (mężczyzna)", "thaiPhonetic": "phǒm", "ttsThai": "ผม"}},
]

minimal_pairs = [
 {"id": "mp-01", "focus": "Tony", "items": [
   {"polish": "nowy", "thaiPhonetic": "mài", "ttsThai": "ใหม่"},
   {"polish": "nie", "thaiPhonetic": "mâi", "ttsThai": "ไม่"},
   {"polish": "drewno", "thaiPhonetic": "mái", "ttsThai": "ไม้"},
   {"polish": "partykuła pytajna", "thaiPhonetic": "mǎi", "ttsThai": "ไหม"}],
  "tip": "Klasyczny tajski łamaniec: cztery tony, jedna sylaba."},
 {"id": "mp-02", "focus": "Tony", "items": [
   {"polish": "biały", "thaiPhonetic": "khǎaw", "ttsThai": "ขาว"},
   {"polish": "wiadomości", "thaiPhonetic": "khàaw", "ttsThai": "ข่าว"},
   {"polish": "ryż", "thaiPhonetic": "khâaw", "ttsThai": "ข้าว"}],
  "tip": "Zamawiając ryż, pilnuj tonu opadającego."},
 {"id": "mp-03", "focus": "Tony", "items": [
   {"polish": "daleko", "thaiPhonetic": "klai", "ttsThai": "ไกล"},
   {"polish": "blisko", "thaiPhonetic": "klâi", "ttsThai": "ใกล้"}],
  "tip": "Te dwa słowa znaczą coś przeciwnego — różni je tylko ton."},
 {"id": "mp-04", "focus": "Tony", "items": [
   {"polish": "tygrys", "thaiPhonetic": "sǔea", "ttsThai": "เสือ"},
   {"polish": "koszula", "thaiPhonetic": "sûea", "ttsThai": "เสื้อ"},
   {"polish": "mata", "thaiPhonetic": "sùea", "ttsThai": "เสื่อ"}],
  "tip": "Ton rosnący kontra opadający — ćwicz wolno."},
 {"id": "mp-05", "focus": "p / ph", "items": [
   {"polish": "ciotka", "thaiPhonetic": "pâa", "ttsThai": "ป้า"},
   {"polish": "materiał, tkanina", "thaiPhonetic": "phâa", "ttsThai": "ผ้า"}],
  "tip": "p jest bez przydechu (jak polskie „p”), ph z mocnym wydechem."},
 {"id": "mp-06", "focus": "t / th", "items": [
   {"polish": "uderzać", "thaiPhonetic": "tii", "ttsThai": "ตี"},
   {"polish": "raz, miejsce", "thaiPhonetic": "thii", "ttsThai": "ที"}],
  "tip": "Trzymaj kartkę przy ustach: przy th ma się poruszyć."},
 {"id": "mp-07", "focus": "k / kh", "items": [
   {"polish": "kurczak", "thaiPhonetic": "kài", "ttsThai": "ไก่"},
   {"polish": "jajko", "thaiPhonetic": "khài", "ttsThai": "ไข่"}],
  "tip": "Zamawiając w barze, ta różnica decyduje o tym, co dostaniesz."},
 {"id": "mp-08", "focus": "Długość samogłoski", "items": [
   {"polish": "usta", "thaiPhonetic": "pàak", "ttsThai": "ปาก"},
   {"polish": "wbijać, wtykać", "thaiPhonetic": "pàk", "ttsThai": "ปัก"}],
  "tip": "Samogłoska długa trwa wyraźnie dłużej — to nie ozdobnik."},
]

exercises = [
 {"id": "ex-01", "title": "Rozpoznawanie tonu", "type": "tone-recognition",
  "instruction": "Posłuchaj słowa i wybierz ton, który słyszysz.",
  "items": [{"thaiPhonetic": t["example"]["thaiPhonetic"], "ttsThai": t["example"]["ttsThai"],
             "answer": t["name"], "polish": t["example"]["polish"]} for t in tones]},
 {"id": "ex-02", "title": "Pary minimalne", "type": "minimal-pairs",
  "instruction": "Posłuchaj i wskaż, które słowo zostało wypowiedziane.",
  "items": [{"pairId": mp["id"], "options": mp["items"], "focus": mp["focus"]} for mp in minimal_pairs]},
 {"id": "ex-03", "title": "Przydech: p / ph, t / th, k / kh", "type": "consonants",
  "instruction": "Powtórz każdą parę, kontrolując wydech dłonią przed ustami.",
  "items": [{"pairId": mp["id"], "options": mp["items"], "focus": mp["focus"]}
            for mp in minimal_pairs if "/" in mp["focus"]]},
]

pron = {
 "file": "pronunciation.json",
 "intro": "Tajski jest językiem tonalnym: ta sama sylaba wypowiedziana na innej wysokości "
          "to inne słowo. W tym kursie nie uczysz się pisma — wszystko zapisujemy fonetycznie, "
          "a znaki nad samogłoską pokazują ton.",
 "toneSystem": {"ā": "ton średni", "à": "ton niski", "â": "ton opadający",
                "á": "ton wysoki", "ǎ": "ton rosnący"},
 "tones": tones,
 "minimalPairs": minimal_pairs,
 "consonantNotes": [
   {"id": "cn-01", "title": "Przydech: p / ph, t / th, k / kh",
    "text": "Litera h po p, t lub k nie tworzy nowego dźwięku — oznacza wydech. ph to „p” z podmuchem, "
            "nigdy „f”. th to „t” z podmuchem, nigdy angielskie „th”. kh to „k” z podmuchem, nigdy „ch”."},
   {"id": "cn-02", "title": "Spółgłoski końcowe",
    "text": "Na końcu sylaby -p, -t, -k są niezwolnione: zatrzymujesz dźwięk w ustach. "
            "Polak zwykle je „wybucha” — to najczęstszy błąd akcentu."},
   {"id": "cn-03", "title": "ng na początku sylaby",
    "text": "ng to jeden dźwięk, taki jak w polskim „bank”, ale postawiony na początku: ngoen (pieniądze)."},
   {"id": "cn-04", "title": "r i l",
    "text": "W mowie potocznej r często brzmi jak lekkie l. Nie warcz polskiego „r”."},
 ],
 "vowelNotes": [
   {"id": "vn-01", "title": "Długość samogłoski",
    "text": "Podwojona litera (aa, ii, uu, ee, oo) oznacza samogłoskę długą. Długość zmienia znaczenie słowa."},
   {"id": "vn-02", "title": "ue oraz oe",
    "text": "ue to dźwięk zbliżony do polskiego „y” wymawianego z cofniętym językiem (súe = kupować). "
            "oe przypomina polskie „e” z zaokrąglonymi wargami (dəən = iść pieszo)."},
   {"id": "vn-03", "title": "aw",
    "text": "aw czytamy jak długie polskie „o” (ráwn = gorący)."},
 ],
 "polishMistakes": [
   {"id": "pm-01", "title": "Ignorowanie tonów",
    "text": "Polak wypowiada zdanie polską intonacją i przypadkiem zmienia znaczenie słów. "
            "Ucz się słowa razem z tonem, nigdy osobno."},
   {"id": "pm-02", "title": "Mylenie mâi (nie) i mǎi (partykuła pytajna)",
    "text": "„phèt mǎi” to pytanie „czy ostre?”, a „mâi phèt” to „nieostre”."},
   {"id": "pm-03", "title": "Czytanie ph jako f",
    "text": "phàt thai to „pat taj”, a nie „fat thaj”."},
   {"id": "pm-04", "title": "Twarde polskie r",
    "text": "à-ròi wypowiadane z polskim „r” brzmi obco; spróbuj lekkiego „l”."},
   {"id": "pm-05", "title": "Zjadanie końcowych samogłosek",
    "text": "khàwp-khun khráp ma trzy pełne sylaby — nie skracaj ich do „khop khun khrap”."},
 ],
 "exercises": exercises,
}
with open(os.path.join(OUT, "pronunciation.json"), "w", encoding="utf-8") as f:
    json.dump(pron, f, ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- KATEGORIE
files = ["survival.json", "a1-part-01.json", "a1-part-02.json"]
cats = collections.Counter()
subs = collections.defaultdict(collections.Counter)
levels = collections.Counter()
total = 0
for fn in files:
    p = os.path.join(OUT, fn)
    if not os.path.exists(p):
        continue
    data = json.load(open(p, encoding="utf-8"))
    for r in data["records"]:
        cats[r["category"]] += 1
        subs[r["category"]][r["subcategory"]] += 1
        levels[r["level"]] += 1
        total += 1

ICON = {"Jedzenie i napoje": "food", "Restauracja": "resto", "Transport": "transport",
        "Hotel": "hotel", "Zakupy i pieniądze": "shop", "Zdrowie": "health",
        "Miejsca i orientacja": "map", "Podstawy i grzeczność": "hello",
        "Ludzie i rodzina": "people", "Czas i daty": "clock", "Liczby i liczenie": "num",
        "Czasowniki": "verb", "Cechy i opinie": "star", "Awarie i pomoc": "alert",
        "Small talk": "chat", "Dom i codzienność": "home", "Praca i nauka": "work",
        "Pytania": "question", "Pogoda i przyroda": "weather"}

categories = [{
    "id": "cat-%02d" % i,
    "name": name,
    "icon": ICON.get(name, "dot"),
    "count": cnt,
    "subcategories": [{"name": s, "count": c} for s, c in sorted(subs[name].items())],
} for i, (name, cnt) in enumerate(sorted(cats.items()), 1)]

with open(os.path.join(OUT, "categories.json"), "w", encoding="utf-8") as f:
    json.dump({"file": "categories.json", "count": len(categories), "records": categories},
              f, ensure_ascii=False, indent=1)

# ----------------------------------------------------------------- METADANE
metadata = {
 "name": "Thai All-in-One",
 "version": VERSION,
 "language": {"interface": "pl", "target": "th"},
 "description": "Baza do nauki tajskiego dla Polaków — bez pisma tajskiego w interfejsie.",
 "phoneticSystem": {
   "name": "Thai All-in-One PL",
   "toneMarks": {"ā": "średni", "à": "niski", "â": "opadający", "á": "wysoki", "ǎ": "rosnący"},
   "notes": "Samogłoski długie zapisujemy podwójnie (aa, ii, uu). ue ≈ polskie y, "
            "oe ≈ e z zaokrąglonymi wargami, aw ≈ długie o.",
 },
 "conventions": {
   "colon": "Dwukropek w polskim tłumaczeniu (np. „Poproszę: woda”) oznacza wstawkę słownikową "
            "w mianowniku — dzięki temu ten sam wzorzec działa z każdym słowem.",
   "gender": "Zdania z „phǒm” są w formie męskiej; kobieta mówi „chǎn” i kończy zdanie „khâ”.",
 },
 "hiddenField": {
   "name": "ttsThai",
   "purpose": "Wejście dla SpeechSynthesis API.",
   "rule": "Nigdy nie renderowane w DOM, nieindeksowane w wyszukiwarce, usuwane z eksportu.",
 },
 "levels": dict(levels),
 "totalRecords": total,
 "dialogues": len(dlgs),
 "dialogueLines": sum(len(d["lines"]) for d in dlgs),
 "grammarTopics": len(grammar),
 "license": "Do weryfikacji przed publiczną publikacją",
 "source": "Baza projektu Thai All-in-One",
 "updated": "2026-08-13",
}
with open(os.path.join(OUT, "metadata.json"), "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=1)

# ----------------------------------------------------------------- MANIFEST
def count_of(fn):
    p = os.path.join(OUT, fn)
    if not os.path.exists(p):
        return 0
    return json.load(open(p, encoding="utf-8")).get("count", 0)

manifest = {
 "version": VERSION,
 "updated": "2026-08-13",
 "cacheKey": "thai-aio-data-v" + VERSION,
 "dataFiles": [
   {"file": "survival.json", "kind": "vocabulary", "level": "Survival", "count": count_of("survival.json")},
   {"file": "a1-part-01.json", "kind": "vocabulary", "level": "A1", "count": count_of("a1-part-01.json")},
   {"file": "a1-part-02.json", "kind": "vocabulary", "level": "A1", "count": count_of("a1-part-02.json")},
   {"file": "dialogues-part-01.json", "kind": "dialogues", "level": "Survival/A1", "count": len(dlgs)},
 ],
 "supportFiles": [
   {"file": "categories.json", "kind": "categories", "count": len(categories)},
   {"file": "grammar.json", "kind": "grammar", "count": len(grammar)},
   {"file": "pronunciation.json", "kind": "pronunciation", "count": len(tones) + len(minimal_pairs)},
   {"file": "metadata.json", "kind": "metadata", "count": 1},
 ],
 "plannedFiles": [
   {"file": "a2-part-01.json", "level": "A2", "stage": 2},
   {"file": "a2-part-02.json", "level": "A2", "stage": 2},
   {"file": "b1-part-01.json", "level": "B1", "stage": 3},
   {"file": "b1-part-02.json", "level": "B1", "stage": 3},
   {"file": "b1-part-03.json", "level": "B1", "stage": 3},
   {"file": "b2-part-01.json", "level": "B2", "stage": 4},
   {"file": "b2-part-02.json", "level": "B2", "stage": 4},
   {"file": "dialogues-part-02.json", "level": "A2/B1", "stage": 3},
   {"file": "dialogues-part-03.json", "level": "B1/B2", "stage": 4},
 ],
 "levels": dict(levels),
 "categories": [c["name"] for c in categories],
 "totalRecords": total,
 "totalDialogues": len(dlgs),
}
with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)

print("dialogi:", len(dlgs), "| linie dialogów:", metadata["dialogueLines"])
print("gramatyka:", len(grammar), "| kategorie:", len(categories), "| rekordy słownika:", total)
