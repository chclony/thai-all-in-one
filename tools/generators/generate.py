# -*- coding: utf-8 -*-
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Builder, strip_tones
from lex_core import CORE
from lex_core2 import CORE2
from lex_phrases import PHRASES

OUT = "/home/claude/thai/data"
os.makedirs(OUT, exist_ok=True)
B = Builder()

ENTRIES = []
for row in CORE + CORE2:
    pl, ph, th, cat, sub, pos, flags, extra, srv, freq = row
    cl_ph = cl_th = cl_pl = ""
    if "|" in extra:
        cl_ph, cl_th, cl_pl = extra.split("|")
    ENTRIES.append(dict(pl=pl, ph=ph, th=th, cat=cat, sub=sub, pos=pos,
                        flags=set(flags.split(",")), extra=extra, srv=srv, freq=freq,
                        cl_ph=cl_ph, cl_th=cl_th, cl_pl=cl_pl))

# --------------------------------------------------------------- SZABLONY
# (id, wymagana flaga, polski, fonetyka, tajski, typ, survival, literal, note, przykład)
T = [
 dict(f="order", pl="Poproszę: {pl}.", ph="khǎw {ph} nòi khráp", th="ขอ{th}หน่อยครับ",
      ty="phrase", srv=1, lit="khǎw = proszę o; nòi = trochę (łagodzi prośbę)",
      note="Najważniejsza konstrukcja zamawiania. Kobieta kończy zdanie „khâ”.",
      ex=("Poproszę dwie sztuki: {pl}.", "khǎw {ph} sǎwng {cl_ph} khráp", "ขอ{th}สอง{cl_th}ครับ"), needs_cl=1),
 dict(f="order", pl="Czy jest {pl}?", ph="mii {ph} mǎi khráp", th="มี{th}ไหมครับ",
      ty="question", srv=1, lit="mii = mieć/być; mǎi = partykuła pytajna",
      note="Uniwersalne pytanie o dostępność.",
      ex=("Nie ma, skończyło się.", "mâi mii láew khráp", "ไม่มีแล้วครับ")),
 dict(f="buy", pl="Ile kosztuje {pl}?", ph="{ph} thâo-rài khráp", th="{th}เท่าไหร่ครับ",
      ty="question", srv=1, lit="thâo-rài = ile (o cenie)",
      note="Cenę podadzą w bahtach — „bàat”.",
      ex=("{pl} — pięćdziesiąt bahtów.", "{ph} hâa-sìp bàat khráp", "{th}ห้าสิบบาทครับ")),
 dict(f="food", pl="Chcę zjeść: {pl}.", ph="phǒm yàak kin {ph}", th="ผมอยากกิน{th}",
      ty="sentence", srv=0, lit="yàak = chcieć; kin = jeść",
      note="Kobieta mówi „chǎn yàak kin…”.",
      ex=("Ja też chcę to zjeść.", "phǒm kâw yàak kin mǔean kan", "ผมก็อยากกินเหมือนกัน")),
 dict(f="drink", pl="Chcę wypić: {pl}.", ph="phǒm yàak dùem {ph}", th="ผมอยากดื่ม{th}",
      ty="sentence", srv=0, lit="dùem = pić",
      note="W mowie potocznej Tajowie częściej mówią po prostu „kin”.",
      ex=("Poproszę zimne: {pl}.", "khǎw {ph} yen yen khráp", "ขอ{th}เย็นๆ ครับ")),
 dict(f="food", pl="Bez dodatku: {pl}.", ph="mâi sài {ph} khráp", th="ไม่ใส่{th}ครับ",
      ty="phrase", srv=1, lit="mâi sài = nie wkładać",
      note="Kluczowe przy zamawianiu jedzenia na targu.",
      ex=("Poproszę bez: {pl}.", "khǎw mâi sài {ph} khráp", "ขอไม่ใส่{th}ครับ")),
 dict(f="order", pl="Lubię: {pl}.", ph="phǒm châwp {ph}", th="ผมชอบ{th}",
      ty="sentence", srv=0, lit="châwp = lubić",
      note="",
      ex=("Bardzo lubię: {pl}.", "phǒm châwp {ph} mâak", "ผมชอบ{th}มาก")),
 dict(f="order", pl="Poproszę dokładkę: {pl}.", ph="khǎw {ph} phôem nòi khráp", th="ขอ{th}เพิ่มหน่อยครับ",
      ty="phrase", srv=1, lit="phôem = dodać, dołożyć", note="",
      ex=("Poproszę jeszcze jedną porcję.", "khǎw ìik thîi nùeng khráp", "ขออีกที่หนึ่งครับ")),
 dict(f="buy", pl="Chcę kupić: {pl}.", ph="phǒm yàak súe {ph}", th="ผมอยากซื้อ{th}",
      ty="sentence", srv=1, lit="súe = kupować", note="",
      ex=("Gdzie to kupię?", "súe dâai thîi nǎi khráp", "ซื้อได้ที่ไหนครับ")),
 dict(f="buy", pl="Gdzie mogę kupić: {pl}?", ph="súe {ph} dâai thîi nǎi khráp", th="ซื้อ{th}ได้ที่ไหนครับ",
      ty="question", srv=1, lit="dâai thîi nǎi = gdzie można", note="",
      ex=("Na targu.", "thîi talàat khráp", "ที่ตลาดครับ")),
 dict(f="thing", pl="Nie mam: {pl}.", ph="phǒm mâi mii {ph}", th="ผมไม่มี{th}",
      ty="sentence", srv=1, lit="mâi mii = nie mieć", note="",
      ex=("Czy masz to?", "khun mii mǎi khráp", "คุณมีไหมครับ")),
 dict(f="thing", pl="To jest {pl}.", ph="nîi khue {ph}", th="นี่คือ{th}",
      ty="sentence", srv=0, lit="nîi = to; khue = jest (identyfikacja)", note="",
      ex=("Co to jest?", "nîi à-rai khráp", "นี่อะไรครับ")),
 # --- MIEJSCA
 dict(f="place", pl="Gdzie jest {pl}?", ph="{ph} yùu thîi nǎi khráp", th="{th}อยู่ที่ไหนครับ",
      ty="question", srv=1, lit="yùu = znajdować się; thîi nǎi = gdzie",
      note="Najczęstsze pytanie podróżnika.",
      ex=("To jest tam.", "yùu thîi nân khráp", "อยู่ที่นั่นครับ")),
 dict(f="place", pl="Jak dojechać: {pl}?", ph="pai {ph} yang-ngai khráp", th="ไป{th}ยังไงครับ",
      ty="question", srv=1, lit="pai = jechać; yang-ngai = jak", note="",
      ex=("Weź taksówkę.", "nâng tháek-sîi pai khráp", "นั่งแท็กซี่ไปครับ")),
 dict(f="place", pl="Jadę do: {pl}.", ph="phǒm jà pai {ph}", th="ผมจะไป{th}",
      ty="sentence", srv=1, lit="jà = partykuła czasu przyszłego", note="",
      ex=("Ja też tam jadę.", "phǒm pai mǔean kan", "ผมไปเหมือนกัน")),
 dict(f="place", pl="Czy w pobliżu jest {pl}?", ph="thǎew níi mii {ph} mǎi khráp", th="แถวนี้มี{th}ไหมครับ",
      ty="question", srv=1, lit="thǎew níi = w tej okolicy", note="",
      ex=("Jest, kawałek dalej.", "mii khráp yùu khâang nâa", "มีครับ อยู่ข้างหน้า")),
 dict(f="place", pl="Czy daleko do: {pl}?", ph="pai {ph} klai mǎi khráp", th="ไป{th}ไกลไหมครับ",
      ty="question", srv=1, lit="klai = daleko (ton średni!)",
      note="Uwaga: „klai” (daleko) i „klâi” (blisko) różni tylko ton.",
      ex=("Niedaleko, dziesięć minut.", "mâi klai sìp naa-thii khráp", "ไม่ไกล สิบนาทีครับ")),
 dict(f="place", pl="Spotkajmy się tu: {pl}.", ph="jəə kan thîi {ph} ná khráp", th="เจอกันที่{th}นะครับ",
      ty="sentence", srv=0, lit="jəə kan = spotkać się", note="",
      ex=("O której się spotykamy?", "jəə kan kìi moong khráp", "เจอกันกี่โมงครับ")),
 # --- POJAZDY
 dict(f="vehicle", pl="Pojadę: {pl}.", ph="phǒm jà nâng {ph} pai", th="ผมจะนั่ง{th}ไป",
      ty="sentence", srv=1, lit="nâng = siedzieć, jechać czymś", note="",
      ex=("Ile to kosztuje?", "thâo-rài khráp", "เท่าไหร่ครับ")),
 dict(f="vehicle", pl="Ile kosztuje przejazd: {pl}?", ph="nâng {ph} thâo-rài khráp", th="นั่ง{th}เท่าไหร่ครับ",
      ty="question", srv=1, lit="", note="",
      ex=("Sto bahtów.", "nùeng ráwi bàat khráp", "หนึ่งร้อยบาทครับ")),
 # --- CZASOWNIKI
 dict(f="verb", pl="Chcę: {pl}.", ph="phǒm yàak {ph}", th="ผมอยาก{th}",
      ty="sentence", srv=1, lit="yàak + czasownik = chcieć coś zrobić", note="",
      ex=("Czy mogę tutaj?", "thîi nîi dâai mǎi khráp", "ที่นี่ได้ไหมครับ")),
 dict(f="verb", pl="Muszę: {pl}.", ph="phǒm tâwng {ph}", th="ผมต้อง{th}",
      ty="sentence", srv=1, lit="tâwng = musieć", note="",
      ex=("Muszę już iść.", "phǒm tâwng pai láew", "ผมต้องไปแล้ว")),
 dict(f="verb", pl="Czy mogę tutaj: {pl}?", ph="{ph} thîi nîi dâai mǎi khráp", th="{th}ที่นี่ได้ไหมครับ",
      ty="question", srv=1, lit="dâai mǎi = czy można", note="",
      ex=("Tak, można.", "dâai khráp", "ได้ครับ")),
 dict(f="verb", pl="Nie mogę: {pl}.", ph="phǒm {ph} mâi dâai", th="ผม{th}ไม่ได้",
      ty="sentence", srv=1, lit="czasownik + mâi dâai = nie móc", note="",
      ex=("Dlaczego nie?", "tham-mai lâ khráp", "ทำไมล่ะครับ")),
 dict(f="verb", pl="Czy możesz: {pl}?", ph="chûai {ph} nòi dâai mǎi khráp", th="ช่วย{th}หน่อยได้ไหมครับ",
      ty="question", srv=1, lit="chûai = pomóc; grzeczna prośba", note="",
      ex=("Jasne, mogę.", "dâai khráp", "ได้ครับ")),
 dict(f="verb", pl="Lubię: {pl}.", ph="phǒm châwp {ph}", th="ผมชอบ{th}",
      ty="sentence", srv=0, lit="", note="",
      ex=("Ja też to lubię.", "phǒm kâw châwp mǔean kan", "ผมก็ชอบเหมือนกัน")),
 dict(f="verb", pl="Jeszcze nie: {pl}.", ph="yang mâi dâai {ph}", th="ยังไม่ได้{th}",
      ty="sentence", srv=0, lit="yang mâi dâai = jeszcze nie (zrobiłem)", note="",
      ex=("Zrobię to jutro.", "phrûng níi jà tham khráp", "พรุ่งนี้จะทำครับ")),
 dict(f="verb", pl="Już: {pl}.", ph="{ph} láew khráp", th="{th}แล้วครับ",
      ty="sentence", srv=0, lit="láew = już, sygnał czynności zakończonej", note="",
      ex=("Już? Naprawdę?", "láew rǔe khráp", "แล้วเหรอครับ")),
 # --- PRZYMIOTNIKI
 dict(f="adj", pl="bardzo {n}", ph="{ph} mâak", th="{th}มาก",
      ty="collocation", srv=1, lit="mâak = bardzo (zawsze po przymiotniku)", note="",
      ex=("To jest bardzo {n}.", "nîi {ph} mâak khráp", "นี่{th}มากครับ")),
 dict(f="adj", pl="nie {n}", ph="mâi {ph}", th="ไม่{th}",
      ty="collocation", srv=1, lit="mâi = nie (przed przymiotnikiem)", note="",
      ex=("Wcale nie {n}.", "mâi {ph} loei", "ไม่{th}เลย")),
 dict(f="adj", pl="trochę za {n}", ph="{ph} pai nòi", th="{th}ไปหน่อย",
      ty="collocation", srv=1, lit="… pai = za bardzo; nòi = trochę", note="",
      ex=("Za {n} dla mnie.", "{ph} pai sǎmràp phǒm", "{th}ไปสำหรับผม")),
 dict(f="adj", pl="Czy to jest {n}?", ph="{ph} mǎi khráp", th="{th}ไหมครับ",
      ty="question", srv=1, lit="", note="",
      ex=("Trochę.", "nít nòi khráp", "นิดหน่อยครับ")),
 # --- LICZBY
 dict(f="num", pl="Cena: {extra} bahtów.", ph="{ph} bàat", th="{th}บาท",
      ty="collocation", srv=1, lit="bàat = baht", note="",
      ex=("Poproszę, tu jest zapłata.", "níi khráp", "นี่ครับ")),
 dict(f="num", pl="Liczba osób: {extra}.", ph="{ph} khon", th="{th}คน",
      ty="collocation", srv=1, lit="khon = klasyfikator dla ludzi", note="",
      ex=("Ile osób?", "kìi khon khráp", "กี่คนครับ")),
 dict(f="num", pl="Sztuk: {extra}.", ph="{ph} an", th="{th}อัน",
      ty="collocation", srv=0, lit="an = uniwersalny klasyfikator", note="",
      ex=("Ile sztuk?", "kìi an khráp", "กี่อันครับ")),
 # --- CZAS
 dict(f="time", pl="Wrócę: {pl}.", ph="phǒm jà klàp {ph}", th="ผมจะกลับ{th}",
      ty="sentence", srv=1, lit="klàp = wracać", note="",
      ex=("O której wrócisz?", "klàp kìi moong khráp", "กลับกี่โมงครับ")),
 dict(f="time", pl="Do zobaczenia: {pl}.", ph="jəə kan {ph} ná khráp", th="เจอกัน{th}นะครับ",
      ty="sentence", srv=0, lit="ná = partykuła łagodząca", note="",
      ex=("Dobrze, do zobaczenia.", "dâai khráp jəə kan", "ได้ครับ เจอกัน")),
 dict(f="time", pl="Czy masz czas: {pl}?", ph="{ph} wâang mǎi khráp", th="{th}ว่างไหมครับ",
      ty="question", srv=0, lit="wâang = wolny, dostępny", note="",
      ex=("Mam czas.", "wâang khráp", "ว่างครับ")),
 # --- LUDZIE
 dict(f="person", pl="Czy jest tutaj {pl}?", ph="thîi nîi mii {ph} mǎi khráp", th="ที่นี่มี{th}ไหมครับ",
      ty="question", srv=0, lit="", note="",
      ex=("Nie ma nikogo takiego.", "mâi mii khráp", "ไม่มีครับ")),
 dict(f="person", pl="Idę razem z kimś: {pl}.", ph="phǒm pai kàp {ph}", th="ผมไปกับ{th}",
      ty="sentence", srv=0, lit="kàp = z (razem z)", note="",
      ex=("Z kim idziesz?", "pai kàp khrai khráp", "ไปกับใครครับ")),
]

TYPE_PL = {"word": "słowo", "phrase": "zwrot", "question": "pytanie",
           "sentence": "zdanie", "collocation": "kolokacja", "dialogue": "dialog"}

def fmt(s, e):
    n = e["extra"] if "adj" in e["flags"] else e["pl"]
    return (s.replace("{pl}", e["pl"]).replace("{ph}", e["ph"]).replace("{th}", e["th"])
             .replace("{n}", n).replace("{extra}", e["extra"])
             .replace("{cl_ph}", e["cl_ph"]).replace("{cl_th}", e["cl_th"])
             .replace("{cl_pl}", e["cl_pl"]))

survival, a1 = [], []
base_ids = {}

# 1) rekordy bazowe (slowa)
for e in ENTRIES:
    level = "Survival" if e["srv"] else "A1"
    tags = sorted({e["cat"].split()[0].lower(), e["sub"].split()[0].lower(), "podstawy" if e["freq"] >= 5 else "słownictwo"})
    ex = []
    if "phrase" in e["flags"] or "particle" in e["flags"]:
        ex.append(("Grzecznie: %s (mężczyzna)." % e["pl"], "%s khráp" % e["ph"], "%sครับ" % e["th"]))
    elif "num" in e["flags"]:
        ex.append(("Cena: %s bahtów." % e["extra"], "%s bàat" % e["ph"], "%sบาท" % e["th"]))
    elif "time" in e["flags"]:
        ex.append(("Do zobaczenia: %s." % e["pl"], "jəə kan %s" % e["ph"], "เจอกัน%s" % e["th"]))
    elif "order" in e["flags"]:
        ex.append(("Poproszę: %s." % e["pl"], "khǎw %s nòi khráp" % e["ph"], "ขอ%sหน่อยครับ" % e["th"]))
    elif "place" in e["flags"]:
        ex.append(("Gdzie jest %s?" % e["pl"], "%s yùu thîi nǎi khráp" % e["ph"], "%sอยู่ที่ไหนครับ" % e["th"]))
    elif "verb" in e["flags"]:
        ex.append(("Chcę: %s." % e["pl"], "phǒm yàak %s" % e["ph"], "ผมอยาก%s" % e["th"]))
    elif "adj" in e["flags"]:
        ex.append(("bardzo %s" % e["extra"], "%s mâak" % e["ph"], "%sมาก" % e["th"]))
    elif "person" in e["flags"]:
        ex.append(("To jest %s." % e["pl"], "nîi khue %s" % e["ph"], "นี่คือ%s" % e["th"]))
    else:
        ex.append(("Czy jest %s?" % e["pl"], "mii %s mǎi khráp" % e["ph"], "มี%sไหมครับ" % e["th"]))
    note = "Bardzo częste słowo — warto znać na pamięć." if e["freq"] >= 5 else ""
    if e["cl_ph"]:
        note = (note + " Klasyfikator: %s (%s)." % (e["cl_ph"], e["cl_pl"])).strip()
    alts = [x.strip() for x in e["pl"].split("/")] if "/" in e["pl"] else []
    r = B.make(level, e["pl"], e["ph"], e["th"], e["cat"], e["sub"], "word", tags,
               freq=e["freq"], notes=note, examples=ex, alternatives=alts)
    if r:
        base_ids[e["ph"]] = r["id"]
        (survival if level == "Survival" else a1).append(r)

# 2) zwroty recznie opracowane
for pl, ph, th, cat, sub, srv, freq, note in PHRASES:
    level = "Survival" if srv else "A1"
    r = B.make(level, pl, ph, th, cat, sub, "phrase",
               sorted({"zwroty", cat.split()[0].lower(), sub.split()[0].lower()}),
               freq=freq, register="uprzejmy" if "khráp" in ph or "khâ" in ph else "neutralny",
               notes=note,
               examples=[("Powtórz proszę.", "phûut ìik khráng dâai mǎi khráp", "พูดอีกครั้งได้ไหมครับ")])
    if r:
        (survival if srv else a1).append(r)

# 3) rekordy generowane z szablonow
SRV_CAP = 780
for tpl in T:
    for e in ENTRIES:
        if tpl["f"] not in e["flags"]:
            continue
        if tpl.get("needs_cl") and not e["cl_ph"]:
            continue
        level = "Survival" if (tpl["srv"] and e["srv"] and len(survival) < SRV_CAP) else "A1"
        exs = []
        if tpl.get("ex"):
            exs.append((fmt(tpl["ex"][0], e), fmt(tpl["ex"][1], e), fmt(tpl["ex"][2], e)))
        related = [base_ids[e["ph"]]] if e["ph"] in base_ids else []
        r = B.make(level, fmt(tpl["pl"], e), fmt(tpl["ph"], e), fmt(tpl["th"], e),
                   e["cat"], e["sub"], tpl["ty"],
                   sorted({"zwroty", e["cat"].split()[0].lower(), TYPE_PL[tpl["ty"]]}),
                   freq=max(2, e["freq"] - 1),
                   register="uprzejmy" if "khráp" in tpl["ph"] else "neutralny",
                   notes=tpl["note"], literal=tpl["lit"], examples=exs, related=related)
        if r:
            (survival if level == "Survival" else a1).append(r)

def save(name, records):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump({"file": name, "count": len(records), "records": records},
                  f, ensure_ascii=False, indent=1)
    print("%-22s %5d rekordów" % (name, len(records)))

save("survival.json", survival)
save("a1-part-01.json", a1[:1000])
save("a1-part-02.json", a1[1000:])
print("RAZEM:", len(survival) + len(a1))
