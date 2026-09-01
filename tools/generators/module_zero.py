#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator Modułu 0 — treningu percepcyjnego przed lekcją 1.

DLACZEGO TEN MODUŁ ISTNIEJE
---------------------------
Do sesji J kurs zaczynał się od słów, a materiał o dźwiękach leżał na ekranie
„Wymowa i tony”, schowanym pod przyciskiem „Więcej”. To zła kolejność.

Polak nie ma w systemie fonologicznym ani tonu leksykalnego, ani kontrastu
długości samogłoski, ani opozycji przydechowej. Dopóki nie usłyszy różnicy
między khǎaw (biały) a khàaw (wiadomości), zapisuje oba słowa w pamięci jako
„khaaw” — czyli błędnie. Każda następna lekcja utrwala ten zapis. Trening
percepcyjny musi więc poprzedzać naukę słownictwa, a nie ją uzupełniać.

SKĄD BIERZE SIĘ MATERIAŁ
------------------------
Wyłącznie z istniejącej bazy (10 755 rekordów) i z pliku pronunciation.json.
Żadnych nowych wyrazów. Każdy bodziec to prawdziwy rekord z własnym polem
ttsThai — inaczej nie dałoby się go odtworzyć.

To nakłada twarde ograniczenie: jednostką odtwarzaną jest CAŁY rekord, bo
syntezator dostaje pismo tajskie całego hasła. Nie da się wyciąć pojedynczej
sylaby z wyrazu wielosylabowego. Dlatego bodźce izolowane pochodzą wyłącznie
z rekordów jednosylabowych (jest ich 506 unikalnych).

PARY MINIMALNE KONTRA IDENTYFIKACJA
-----------------------------------
Zadanie różnicowania („to samo czy inne”, „który z trzech jest inny”) ma sens
tylko na parze minimalnej — dwóch rekordach różniących się WYŁĄCZNIE badaną
cechą. Gdyby różniły się czymś jeszcze, uczący się rozstrzygałby zadanie tą
inną cechą i nie trenowałby niczego.

Prawdziwych par minimalnych w żywym języku jest mało i nierówno:
  tony            55 par w bazie + 8 zestawów z pronunciation.json
  wygłos -p/-t/-k  9 par
  długość          3 pary + 1 z pronunciation.json
  przydech         3 pary + 2 z pronunciation.json
  ng- w nagłosie   0 par (ale 11 par różniących się samym nagłosem)

Dlatego moduł stoi na dwóch nogach. Tam, gdzie par minimalnych wystarcza
(tony, wygłos, ng), idą zadania różnicowania. Tam, gdzie ich brakuje
(długość, przydech), ciężar biorą zadania identyfikacyjne — „długa czy
krótka”, „z przydechem czy bez” — które potrzebują jednego bodźca, a więc
mają do dyspozycji cały zasób jednosylabowców. Każde zadanie, także
identyfikacyjne, dostaje parę do porównania (pole compare), żeby po
odpowiedzi dało się przesłuchać oba warianty jeden po drugim.

Uruchomienie:  python3 tools/generators/module_zero.py
"""
import json, os, re, sys, unicodedata, random, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")

VOCAB = ["survival.json", "a1-part-01.json", "a1-part-02.json",
         "a2-part-01.json", "a2-part-02.json", "b1-part-01.json",
         "b1-part-02.json", "b1-part-03.json", "b2-part-01.json",
         "b2-part-02.json", "supplemental-practical.json",
         "core-lexicon-01.json", "core-lexicon-02.json"]

LEXTYPES = {"word", "verb", "adjective", "noun", "adverb"}

# ---------------------------------------------------------------- fonetyka

MARKS = {"\u0301": "wysoki", "\u0300": "niski", "\u0302": "opadający",
         "\u030c": "rosnący", "\u0304": "średni"}
TONE_ORDER = ["średni", "niski", "opadający", "wysoki", "rosnący"]

ONSETS = ["khw", "khr", "khl", "phr", "phl", "thr", "kw", "kr", "kl", "pr",
          "pl", "tr", "ch", "kh", "ph", "th", "ng",
          "b", "d", "f", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t",
          "w", "y", "c", "g", "v", "z"]
CODAS = ["ng", "p", "t", "k", "m", "n", "w", "y", "i"]
LONG_NUCLEI = ["aaw", "aai", "uea", "iaw", "aa", "ii", "uu", "ee", "oo", "ae",
               "aw", "ai", "ao", "oe", "ua", "ia", "ue", "au", "oi", "ui",
               "eu", "oy"]
SHORT_LONG = {"a": "aa", "i": "ii", "u": "uu", "e": "ee", "o": "oo"}


def strip_tones(text):
    d = unicodedata.normalize("NFD", text or "")
    return unicodedata.normalize("NFC", re.sub("[\u0300\u0301\u0302\u030c\u0304]", "", d))


def tone_of(syl):
    for ch in unicodedata.normalize("NFD", syl or ""):
        if ch in MARKS:
            return MARKS[ch]
    return "średni"


def syllables(ph):
    return [s for s in re.split(r"[\s\-]+", ph or "") if s]


def parse(syl):
    """Rozbiór sylaby: nagłos, jądro, wygłos, ton, długość."""
    tone = tone_of(syl)
    bare = strip_tones(syl).lower()
    onset = ""
    for o in ONSETS:
        if bare.startswith(o):
            onset = o
            break
    rest = bare[len(onset):]
    coda = ""
    for c in CODAS:
        if len(rest) > len(c) and rest.endswith(c):
            coda = c
            break
    nucleus = rest[:len(rest) - len(coda)] if coda else rest
    if not nucleus:
        return None
    long_v = nucleus in LONG_NUCLEI or len(nucleus) >= 2
    return {"onset": onset, "nucleus": nucleus, "coda": coda,
            "tone": tone, "long": long_v}


# ---------------------------------------------------------------- kontrasty

FAMILIES = [
    ("tony-plaskie", "Tony płaskie", "średni, niski i wysoki — trzy poziomy bez ruchu"),
    ("tony-konturowe", "Tony konturowe", "opadający i rosnący — ton, który się zmienia w trakcie sylaby"),
    ("dlugosc", "Długość samogłoski", "aa kontra a — dla Polaka trudniejsze niż tony"),
    ("przydech", "Przydech", "p/ph, t/th, k/kh — obecność podmuchu po spółgłosce"),
    ("wyglos", "Spółgłoski wygłosowe", "-p, -t, -k niezwolnione na końcu sylaby"),
    ("ng", "ng w nagłosie", "jeden dźwięk na początku wyrazu, nie „n” plus „g”"),
    ("wielosylabowe", "Tony w dłuższej wypowiedzi", "ton w wyrazie wielosylabowym i w zdaniu"),
]

CONTRASTS = []


def contrast(cid, family, label, short, note):
    CONTRASTS.append({"id": cid, "family": family, "label": label,
                      "short": short, "note": note})


for t in TONE_ORDER:
    fam = "tony-plaskie" if t in ("średni", "niski", "wysoki") else "tony-konturowe"
    contrast("ton-" + {"średni": "sredni", "niski": "niski", "opadający": "opadajacy",
                       "wysoki": "wysoki", "rosnący": "rosnacy"}[t],
             fam, "rozpoznanie tonu — " + t, "ton " + t,
             "Czy potrafisz nazwać ton %s, słysząc go w izolacji." % t)

TONE_SLUG = {"średni": "sredni", "niski": "niski", "opadający": "opadajacy",
             "wysoki": "wysoki", "rosnący": "rosnacy"}

# Narzędnik nazw tonów — „między tonem niskim a opadającym”, nie „niski a opadający”.
TONE_INSTR = {"średni": "średnim", "niski": "niskim", "opadający": "opadającym",
              "wysoki": "wysokim", "rosnący": "rosnącym"}

TONE_PAIRS = []
for i in range(len(TONE_ORDER)):
    for j in range(i + 1, len(TONE_ORDER)):
        a, b = TONE_ORDER[i], TONE_ORDER[j]
        fam = "tony-konturowe" if ("opadający" in (a, b) or "rosnący" in (a, b)) else "tony-plaskie"
        cid = "ton-%s-vs-%s" % (TONE_SLUG[a], TONE_SLUG[b])
        TONE_PAIRS.append((cid, a, b))
        contrast(cid, fam, "ton %s kontra %s" % (a, b), "%s / %s" % (a, b),
                 "Czy słyszysz różnicę między tonem %s a %s."
                 % (TONE_INSTR[a], TONE_INSTR[b]))

contrast("dlugosc-samogloski", "dlugosc", "samogłoska długa kontra krótka",
         "długa / krótka",
         "Polszczyzna nie odróżnia znaczeń długością samogłoski, więc ucho jej nie mierzy.")
for base in ("p", "t", "k"):
    contrast("przydech-" + base, "przydech",
             "%s kontra %sh" % (base, base), "%s / %sh" % (base, base),
             "Polskie „%s” leży między tajskim %s a %sh — trzeba wybrać stronę." % (base, base, base))
for a, b in (("p", "t"), ("p", "k"), ("t", "k")):
    contrast("wyglos-%s-%s" % (a, b), "wyglos",
             "wygłosowe -%s kontra -%s" % (a, b), "-%s / -%s" % (a, b),
             "Na końcu sylaby dźwięk się zatrzymuje i nie zostaje zwolniony — słychać samo miejsce artykulacji.")
contrast("ng-naglos", "ng", "ng na początku wyrazu", "ng-",
         "Polszczyzna zna „ng” tylko w środku i na końcu (bank), nigdy na początku.")
contrast("liczba-sylab", "wielosylabowe", "granice sylab", "liczba sylab",
         "Zbitki, których polszczyzna nie zna, rozpadają się w uchu na dodatkowe sylaby.")
contrast("ton-w-wyrazie", "wielosylabowe", "ton w wyrazie wielosylabowym", "ton w wyrazie",
         "Ton trzeba usłyszeć na wskazanej sylabie, a nie na całym wyrazie naraz.")
contrast("ton-w-zdaniu", "wielosylabowe", "ton w zdaniu", "ton w zdaniu",
         "W zdaniu intonacja zdaniowa nakłada się na tony leksykalne.")

CONTRAST_IDS = {c["id"] for c in CONTRASTS}


# ------------------------------------------------------------------ dane

def load_records():
    recs = []
    for fn in VOCAB:
        with open(os.path.join(DATA, fn), encoding="utf-8") as f:
            for r in json.load(f)["records"]:
                r["__file"] = fn
                recs.append(r)
    return recs


def load_pron():
    with open(os.path.join(DATA, "pronunciation.json"), encoding="utf-8") as f:
        return json.load(f)


class Pool(object):
    """Zbiór bodźców. Każdy bodziec ma własne ttsThai, więc da się go odtworzyć."""

    def __init__(self):
        self.by_key = {}
        self.order = []

    def add(self, ph, pl, tts, source=None, kind="word"):
        key = ph
        if key in self.by_key:
            return self.by_key[key]["id"]
        sid = "m0s-%04d" % (len(self.order) + 1)
        sy = syllables(ph)
        parts = [parse(s) for s in sy]
        item = {
            "id": sid,
            "phonetic": ph,
            "polish": pl,
            "ttsThai": tts,
            "kind": kind,
            "syllableCount": len(sy),
            "tones": [tone_of(s) for s in sy],
        }
        if len(sy) == 1 and parts[0]:
            p = parts[0]
            item["onset"] = p["onset"]
            item["nucleus"] = p["nucleus"]
            item["coda"] = p["coda"]
            item["long"] = p["long"]
        if source:
            item["sourceId"] = source
        self.by_key[key] = item
        self.order.append(item)
        return sid

    def get(self, sid):
        for it in self.order:
            if it["id"] == sid:
                return it
        return None


def build_inventory(recs, pron):
    """Kandydaci na bodźce: rekordy z ttsThai, bez wariantów zależnych od płci."""
    mono, multi, sent = {}, {}, {}
    for r in recs:
        ph = r.get("thaiPhonetic")
        tts = r.get("ttsThai")
        if not ph or not tts:
            continue
        if r.get("genderLexicon") or r.get("genderVariant"):
            continue          # forma zależna od płci komplikuje odsłuch bez potrzeby
        sy = syllables(ph)
        if any(parse(s) is None for s in sy):
            continue
        typ = r.get("type")
        bucket = None
        if typ in LEXTYPES and len(sy) == 1:
            bucket = mono
        elif typ in LEXTYPES and 2 <= len(sy) <= 3:
            bucket = multi
        elif typ in ("sentence", "question") and 3 <= len(sy) <= 6:
            bucket = sent
        if bucket is None:
            continue
        old = bucket.get(ph)
        if old is None or r.get("frequency", 0) > old.get("frequency", 0):
            bucket[ph] = r

    # zestawy z pronunciation.json — kurowane ręcznie, więc mają pierwszeństwo
    extra = []
    for mp in pron.get("minimalPairs", []):
        items = [i for i in mp["items"] if i.get("ttsThai") and not i.get("genderLexicon")]
        if len(items) >= 2:
            extra.append({"focus": mp["focus"], "items": items, "tip": mp.get("tip", "")})
    return list(mono.values()), list(multi.values()), list(sent.values()), extra


# ------------------------------------------------------- wyszukiwanie par

def minimal_pairs(mono):
    """Pary różniące się dokładnie jedną cechą. Zwraca słownik kontrast -> lista."""
    out = collections.defaultdict(list)
    parsed = [(r, parse(syllables(r["thaiPhonetic"])[0])) for r in mono]
    for i in range(len(parsed)):
        ra, pa = parsed[i]
        for j in range(i + 1, len(parsed)):
            rb, pb = parsed[j]
            diffs = [k for k in ("onset", "nucleus", "coda", "tone") if pa[k] != pb[k]]
            if len(diffs) != 1:
                continue
            d = diffs[0]
            if d == "tone":
                a, b = pa["tone"], pb["tone"]
                key = "ton-%s-vs-%s" % (TONE_SLUG[a], TONE_SLUG[b]) \
                    if TONE_ORDER.index(a) < TONE_ORDER.index(b) \
                    else "ton-%s-vs-%s" % (TONE_SLUG[b], TONE_SLUG[a])
                out[key].append((ra, rb))
            elif d == "onset":
                x, y = pa["onset"], pb["onset"]
                for base in ("p", "t", "k"):
                    if {x, y} == {base, base + "h"}:
                        out["przydech-" + base].append((ra, rb))
                if "ng" in (x, y):
                    out["ng-naglos"].append((ra, rb))
            elif d == "nucleus":
                x, y = pa["nucleus"], pb["nucleus"]
                if SHORT_LONG.get(x) == y or SHORT_LONG.get(y) == x:
                    out["dlugosc-samogloski"].append((ra, rb))
            elif d == "coda":
                x, y = pa["coda"], pb["coda"]
                if x in "ptk" and y in "ptk" and x and y:
                    a, b = sorted([x, y], key=lambda c: "ptk".index(c))
                    out["wyglos-%s-%s" % (a, b)].append((ra, rb))
    return out


def pron_pairs(extra, pool):
    """Zestawy z pronunciation.json rozbite na pary z kontrastem."""
    out = collections.defaultdict(list)
    for grp in extra:
        items = grp["items"]
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, b = items[i], items[j]
                sa, sb = syllables(a["thaiPhonetic"]), syllables(b["thaiPhonetic"])
                if len(sa) != 1 or len(sb) != 1:
                    continue
                pa, pb = parse(sa[0]), parse(sb[0])
                if not pa or not pb:
                    continue
                diffs = [k for k in ("onset", "nucleus", "coda", "tone") if pa[k] != pb[k]]
                if len(diffs) != 1:
                    continue
                d = diffs[0]
                key = None
                if d == "tone":
                    x, y = pa["tone"], pb["tone"]
                    lo, hi = sorted([x, y], key=TONE_ORDER.index)
                    key = "ton-%s-vs-%s" % (TONE_SLUG[lo], TONE_SLUG[hi])
                elif d == "onset":
                    x, y = pa["onset"], pb["onset"]
                    for base in ("p", "t", "k"):
                        if {x, y} == {base, base + "h"}:
                            key = "przydech-" + base
                    if "ng" in (x, y):
                        key = "ng-naglos"
                elif d == "nucleus":
                    x, y = pa["nucleus"], pb["nucleus"]
                    if SHORT_LONG.get(x) == y or SHORT_LONG.get(y) == x:
                        key = "dlugosc-samogloski"
                elif d == "coda":
                    x, y = pa["coda"], pb["coda"]
                    if x in "ptk" and y in "ptk" and x and y:
                        lo, hi = sorted([x, y], key=lambda c: "ptk".index(c))
                        key = "wyglos-%s-%s" % (lo, hi)
                if key:
                    out[key].append((a, b))
    return out


# ------------------------------------------------------------ budowa zadań

TONE_LABELS = ["ton średni", "ton niski", "ton opadający", "ton wysoki", "ton rosnący"]


class Builder(object):
    def __init__(self, pool, rng):
        self.pool = pool
        self.rng = rng
        self.n = 0

    def sid(self, rec):
        return self.pool.add(rec["thaiPhonetic"],
                             rec.get("polish", ""),
                             rec["ttsThai"],
                             rec.get("id"),
                             "sentence" if rec.get("type") in ("sentence", "question") else "word")

    def task(self, lesson, kind, contrast_id, **kw):
        self.n += 1
        t = {"id": "%s-z%02d" % (lesson, self.n),
             "type": kind, "contrastId": contrast_id}
        t.update(kw)
        return t

    # --- 1. to samo czy inne ------------------------------------------------
    def same_diff(self, lesson, cid, a, b, same):
        ia, ib = self.sid(a), self.sid(b)
        play = [ia, ia] if same else self.rng.sample([ia, ib], 2)
        return self.task(
            lesson, "same-diff", cid,
            prompt="Usłyszysz dwa dźwięki. Czy to ten sam wyraz?",
            playIds=play,
            options=["To samo", "Co innego"],
            answer="To samo" if same else "Co innego",
            compare=[ia, ib],
            explain=("Oba nagrania to %s." % a["thaiPhonetic"]) if same
            else ("Pierwszy i drugi różnią się: %s kontra %s."
                  % (a["thaiPhonetic"], b["thaiPhonetic"])))

    # --- 2. który z trzech jest inny ---------------------------------------
    def odd_one(self, lesson, cid, a, b):
        ia, ib = self.sid(a), self.sid(b)
        pos = self.rng.randrange(3)
        play = [ia, ia, ia]
        play[pos] = ib
        return self.task(
            lesson, "odd-one-out", cid,
            prompt="Usłyszysz trzy dźwięki. Który jest inny niż pozostałe dwa?",
            playIds=play,
            options=["Pierwszy", "Drugi", "Trzeci"],
            answer=["Pierwszy", "Drugi", "Trzeci"][pos],
            compare=[ia, ib],
            explain="Dwa razy %s, raz %s — inny był %s."
                    % (a["thaiPhonetic"], b["thaiPhonetic"],
                       ["pierwszy", "drugi", "trzeci"][pos]))

    # --- 3. wskaż ton na skali ---------------------------------------------
    def tone_scale(self, lesson, cid, rec, partner, index=0, label=None):
        ia = self.sid(rec)
        tone = tone_of(syllables(rec["thaiPhonetic"])[index])
        extra = {}
        if label:
            extra["focus"] = label
        return self.task(
            lesson, "tone-scale", cid,
            prompt=("Posłuchaj i wskaż na skali ton, który słyszysz."
                    if not label else
                    "Posłuchaj i wskaż ton sylaby %s." % label),
            playIds=[ia],
            options=TONE_LABELS,
            answer="ton " + tone,
            compare=[ia, self.sid(partner)] if partner else [ia],
            explain="To ton %s." % tone,
            **extra)

    # --- 4. policz sylaby ---------------------------------------------------
    def count_syllables(self, lesson, cid, rec, partner=None):
        ia = self.sid(rec)
        n = len(syllables(rec["thaiPhonetic"]))
        # Zdania mają po pięć i sześć sylab, więc stała lista 1-4 nie
        # obejmowałaby poprawnej odpowiedzi. Okno czterech kolejnych liczb
        # wokół odpowiedzi, z losowym przesunięciem — inaczej poprawna
        # odpowiedź stałaby zawsze w tym samym miejscu i dałoby się ją
        # wyklikać bez słuchania.
        offset = self.rng.randrange(0, min(4, n))
        start = max(1, n - offset)
        opts = [str(x) for x in range(start, start + 4)]
        return self.task(
            lesson, "count-syllables", cid,
            prompt="Ile sylab słyszysz?",
            playIds=[ia],
            options=opts,
            answer=str(n),
            compare=[ia, self.sid(partner)] if partner else [ia],
            explain="%s to %d %s." % (rec["thaiPhonetic"], n,
                                      "sylaba" if n == 1 else
                                      ("sylaby" if n < 5 else "sylab")))

    # --- 5. długa czy krótka ------------------------------------------------
    def vowel_length(self, lesson, rec, partner):
        ia = self.sid(rec)
        p = parse(syllables(rec["thaiPhonetic"])[0])
        return self.task(
            lesson, "vowel-length", "dlugosc-samogloski",
            prompt="Samogłoska w tym wyrazie jest długa czy krótka?",
            playIds=[ia],
            options=["Długa", "Krótka"],
            answer="Długa" if p["long"] else "Krótka",
            compare=[ia, self.sid(partner)] if partner else [ia],
            explain="%s — samogłoska %s (%s)."
                    % (rec["thaiPhonetic"], "długa" if p["long"] else "krótka",
                       p["nucleus"]))

    # --- 6. z przydechem czy bez -------------------------------------------
    def aspiration(self, lesson, rec, partner):
        ia = self.sid(rec)
        p = parse(syllables(rec["thaiPhonetic"])[0])
        base = p["onset"][0]
        asp = p["onset"].endswith("h")
        return self.task(
            lesson, "aspiration", "przydech-" + base,
            prompt="Pierwsza spółgłoska tego wyrazu jest z przydechem czy bez?",
            playIds=[ia],
            options=["Z przydechem", "Bez przydechu"],
            answer="Z przydechem" if asp else "Bez przydechu",
            compare=[ia, self.sid(partner)] if partner else [ia],
            explain="%s zaczyna się od %s — %s."
                    % (rec["thaiPhonetic"], p["onset"],
                       "słychać podmuch" if asp else "bez podmuchu"))


# --------------------------------------------------------------- pomocnicze

def cycle_take(items, n, rng):
    """n elementów z listy, przechodząc ją w kółko, bez powtarzania w serii."""
    if not items:
        return []
    out = []
    pool = []
    while len(out) < n:
        if not pool:
            pool = items[:]
            rng.shuffle(pool)
        out.append(pool.pop())
    return out


def partner_for(rec, mono, feature, rng):
    """Wyraz do porównania: ta sama rama, przeciwna wartość badanej cechy."""
    p = parse(syllables(rec["thaiPhonetic"])[0])
    cands = []
    for r in mono:
        if r["thaiPhonetic"] == rec["thaiPhonetic"]:
            continue
        q = parse(syllables(r["thaiPhonetic"])[0])
        if not q:
            continue
        if feature == "length":
            if q["onset"] != p["onset"] or q["coda"] != p["coda"]:
                continue
            if q["long"] == p["long"]:
                continue
            cands.append((0, r))
        elif feature == "aspiration":
            want = p["onset"][0] if p["onset"].endswith("h") else p["onset"] + "h"
            if q["onset"] != want:
                continue
            score = 0 if (q["nucleus"] == p["nucleus"] and q["coda"] == p["coda"]) else 1
            cands.append((score, r))
        elif feature == "tone":
            if q["nucleus"] != p["nucleus"] or q["coda"] != p["coda"] or q["onset"] != p["onset"]:
                continue
            if q["tone"] == p["tone"]:
                continue
            cands.append((0, r))
    if not cands:
        # zapas: dowolny wyraz o przeciwnej wartości cechy
        for r in mono:
            q = parse(syllables(r["thaiPhonetic"])[0])
            if not q:
                continue
            if feature == "length" and q["long"] != p["long"]:
                cands.append((3, r))
            elif feature == "aspiration":
                want = p["onset"][0] if p["onset"].endswith("h") else p["onset"] + "h"
                if q["onset"] == want:
                    cands.append((3, r))
        if not cands:
            return None
    cands.sort(key=lambda x: x[0])
    best = [r for s, r in cands if s == cands[0][0]]
    return rng.choice(best)


# ------------------------------------------------------------------ lekcje

LESSON_META = [
    (1, "Pięć tonów — każdy z osobna",
     "Uczysz się nazywać ton, który słyszysz. Pięć tonów tajskich w izolacji, "
     "po jednej sylabie naraz, bez znaczeń. Zanim zaczniesz rozróżniać tony między sobą, "
     "musisz umieć każdy z nich rozpoznać osobno.", 25),
    (2, "Tony w parach — to samo czy inne",
     "Słyszysz dwa dźwięki i decydujesz, czy to ten sam wyraz. Tu nie chodzi o nazwanie "
     "tonu, tylko o samo wykrycie różnicy. To najniższy próg percepcji — bez niego "
     "nazywanie tonów jest zgadywaniem.", 20),
    (3, "Tony w trójkach — który jest inny",
     "Trzy dźwięki, dwa takie same i jeden inny. Zadanie obciąża pamięć słuchową "
     "mocniej niż para, więc różnica musi być już naprawdę słyszalna, a nie tylko "
     "przeczuwana.", 20),
    (4, "Długość samogłoski — długa czy krótka",
     "Polszczyzna nie odróżnia znaczeń długością samogłoski, więc Twoje ucho jej "
     "nie mierzy. W tajskim aa i a to dwa różne słowa. Ten kontrast jest dla Polaka "
     "trudniejszy niż tony — tony przynajmniej słychać od razu jako coś obcego.", 25),
    (5, "Długość samogłoski — porównanie i wybór",
     "Ten sam kontrast, ale teraz w parach i trójkach. Musisz usłyszeć różnicę między "
     "dwoma wyrazami, które różni wyłącznie czas trwania samogłoski.", 20),
    (6, "Przydech — p/ph, t/th, k/kh",
     "Litera h nie tworzy nowego dźwięku, tylko oznacza podmuch. Polskie „p” leży "
     "między tajskim p a ph, więc polskie ucho słyszy oba jako to samo. Uczysz się "
     "wybierać stronę.", 24),
    (7, "Przydech — rozróżnianie w parach",
     "Ten sam kontrast w zadaniu różnicowym. Par minimalnych na przydech jest w bazie "
     "mało, więc lekcja łączy pary z zadaniami identyfikacyjnymi.", 20),
    (8, "Spółgłoski wygłosowe — -p, -t, -k",
     "Na końcu sylaby te spółgłoski są niezwolnione: dźwięk zatrzymuje się w ustach "
     "i nie ma słyszalnego wybuchu. Zostaje samo miejsce artykulacji i to je trzeba "
     "usłyszeć.", 20),
    (9, "Spółgłoski wygłosowe — trzy naraz",
     "Rozróżnianie -p, -t i -k między sobą, w parach i trójkach. Polak zwykle "
     "„wybucha” te spółgłoski i przez to ich nie odróżnia.", 20),
    (10, "ng na początku wyrazu",
     "Polszczyzna zna „ng” tylko w środku i na końcu (bank, ręka). Na początku wyrazu "
     "polskie ucho rozkłada go na dwa dźwięki i dokłada sylabę. Uczysz się słyszeć "
     "jeden dźwięk i jedną sylabę.", 16),
    (11, "Tony w wyrazie wielosylabowym",
     "Ton siedzi na sylabie, nie na wyrazie. W wyrazie dwu- i trzysylabowym trzeba "
     "usłyszeć ton wskazanej sylaby, a nie ogólny kształt całości.", 25),
    (12, "Tony w zdaniu",
     "W zdaniu na tony leksykalne nakłada się intonacja zdaniowa. To ostatnia lekcja "
     "modułu i najbliższa temu, co usłyszysz w rozmowie.", 25),
]


def required_for(n):
    """Próg 90 procent, zaokrąglony w górę do pełnej odpowiedzi."""
    import math
    return int(math.ceil(n * 0.9))


def main():
    rng = random.Random(20260822)
    recs = load_records()
    pron = load_pron()
    mono, multi, sent, extra = build_inventory(recs, pron)
    pool = Pool()
    B = Builder(pool, rng)

    mp = minimal_pairs(mono)
    pp = pron_pairs(extra, pool)
    for k, v in pp.items():
        mp[k].extend(v)

    # --- zasoby pomocnicze ---
    by_tone = collections.defaultdict(list)
    for r in mono:
        by_tone[tone_of(syllables(r["thaiPhonetic"])[0])].append(r)
    for t in by_tone:
        by_tone[t].sort(key=lambda r: (-r.get("frequency", 0), r.get("difficulty", 5)))

    asp_words = collections.defaultdict(list)
    for r in mono:
        o = parse(syllables(r["thaiPhonetic"])[0])["onset"]
        if o in ("p", "ph", "t", "th", "k", "kh"):
            asp_words[o].append(r)

    ng_words = [r for r in mono
                if parse(syllables(r["thaiPhonetic"])[0])["onset"] == "ng"]
    ng_multi = [r for r in multi
                if parse(syllables(r["thaiPhonetic"])[0])["onset"] == "ng"]

    lessons = []
    stats = collections.Counter()

    def push(num, tasks):
        meta = LESSON_META[num - 1]
        n = len(tasks)
        req = required_for(n)
        lid = "m0-lesson-%02d" % num
        for t in tasks:
            stats[t["contrastId"]] += 1
        cids = sorted({t["contrastId"] for t in tasks})
        fams = sorted({c["family"] for c in CONTRASTS if c["id"] in cids})
        lessons.append({
            "id": lid, "number": num, "title": meta[1], "goal": meta[2],
            "contrastIds": cids, "families": fams,
            "pass": {"questions": n, "required": req,
                     "accuracy": int(round(req / float(n) * 100)),
                     "text": "Zalicz %d z %d odpowiedzi (%d%%). Próg jest wyższy niż "
                             "w lekcjach słownikowych, bo tu chodzi o samo słyszenie — "
                             "jeżeli słyszysz różnicę, mylisz się rzadko."
                             % (req, n, int(round(req / float(n) * 100)))},
            "tasks": tasks
        })

    # ---------------------------------------------------------- lekcja 1
    B.n = 0
    tasks = []
    per = [5, 5, 5, 5, 5]
    for ti, tone in enumerate(TONE_ORDER):
        words = by_tone[tone][:40]
        chosen = cycle_take(words, per[ti], rng)
        for r in chosen:
            partner = partner_for(r, mono, "tone", rng) or rng.choice(
                by_tone[TONE_ORDER[(ti + 2) % 5]][:20])
            tasks.append(B.tone_scale("m0-lesson-01", "ton-" + TONE_SLUG[tone], r, partner))
    rng.shuffle(tasks)
    for i, t in enumerate(tasks):
        t["id"] = "m0-lesson-01-z%02d" % (i + 1)
    push(1, tasks)

    # ---------------------------------------------------------- lekcja 2
    B.n = 0
    tasks = []
    for cid, a, b in TONE_PAIRS:
        pairs = mp.get(cid, [])
        if not pairs:
            continue
        take = cycle_take(pairs, 2, rng)
        for k, (x, y) in enumerate(take):
            tasks.append(B.same_diff("m0-lesson-02", cid, x, y, same=(k % 2 == 0)))
    # dopełnienie do 20 najbogatszymi kontrastami
    rich = sorted([c for c, _, _ in TONE_PAIRS if mp.get(c)],
                  key=lambda c: -len(mp[c]))
    i = 0
    while len(tasks) < 20:
        cid = rich[i % len(rich)]
        x, y = rng.choice(mp[cid])
        tasks.append(B.same_diff("m0-lesson-02", cid, x, y, same=(len(tasks) % 2 == 1)))
        i += 1
    tasks = tasks[:20]
    rng.shuffle(tasks)
    for i, t in enumerate(tasks):
        t["id"] = "m0-lesson-02-z%02d" % (i + 1)
    push(2, tasks)

    # ---------------------------------------------------------- lekcja 3
    B.n = 0
    tasks = []
    for cid, a, b in TONE_PAIRS:
        pairs = mp.get(cid, [])
        if not pairs:
            continue
        for x, y in cycle_take(pairs, 2, rng):
            tasks.append(B.odd_one("m0-lesson-03", cid, x, y))
    i = 0
    while len(tasks) < 20:
        cid = rich[i % len(rich)]
        x, y = rng.choice(mp[cid])
        tasks.append(B.odd_one("m0-lesson-03", cid, y, x))
        i += 1
    tasks = tasks[:20]
    rng.shuffle(tasks)
    for i, t in enumerate(tasks):
        t["id"] = "m0-lesson-03-z%02d" % (i + 1)
    push(3, tasks)

    # ---------------------------------------------------------- lekcja 4
    B.n = 0
    tasks = []
    longs = [r for r in mono if parse(syllables(r["thaiPhonetic"])[0])["long"]]
    shorts = [r for r in mono if not parse(syllables(r["thaiPhonetic"])[0])["long"]]
    longs.sort(key=lambda r: (-r.get("frequency", 0), r.get("difficulty", 5)))
    shorts.sort(key=lambda r: (-r.get("frequency", 0), r.get("difficulty", 5)))
    picked = []
    for k in range(13):
        picked.append(longs[k % len(longs)])
    for k in range(12):
        picked.append(shorts[k % len(shorts)])
    for r in picked:
        p = partner_for(r, mono, "length", rng)
        tasks.append(B.vowel_length("m0-lesson-04", r, p))
    rng.shuffle(tasks)
    for i, t in enumerate(tasks):
        t["id"] = "m0-lesson-04-z%02d" % (i + 1)
    push(4, tasks)

    # ---------------------------------------------------------- lekcja 5
    B.n = 0
    tasks = []
    lp = mp.get("dlugosc-samogloski", [])
    if lp:
        for k in range(8):
            x, y = lp[k % len(lp)]
            tasks.append(B.same_diff("m0-lesson-05", "dlugosc-samogloski", x, y,
                                     same=(k % 2 == 0)))
        for k in range(4):
            x, y = lp[k % len(lp)]
            tasks.append(B.odd_one("m0-lesson-05", "dlugosc-samogloski", x, y))
    while len(tasks) < 20:
        r = picked[len(tasks) % len(picked)]
        p = partner_for(r, mono, "length", rng)
        tasks.append(B.vowel_length("m0-lesson-05", r, p))
    tasks = tasks[:20]
    rng.shuffle(tasks)
    for i, t in enumerate(tasks):
        t["id"] = "m0-lesson-05-z%02d" % (i + 1)
    push(5, tasks)

    # ---------------------------------------------------------- lekcja 6
    B.n = 0
    tasks = []
    for base in ("p", "t", "k"):
        plain = sorted(asp_words[base], key=lambda r: (-r.get("frequency", 0),))
        aspd = sorted(asp_words[base + "h"], key=lambda r: (-r.get("frequency", 0),))
        for k in range(4):
            r = plain[k % len(plain)]
            tasks.append(B.aspiration("m0-lesson-06", r,
                                      partner_for(r, mono, "aspiration", rng)))
        for k in range(4):
            r = aspd[k % len(aspd)]
            tasks.append(B.aspiration("m0-lesson-06", r,
                                      partner_for(r, mono, "aspiration", rng)))
    rng.shuffle(tasks)
    for i, t in enumerate(tasks):
        t["id"] = "m0-lesson-06-z%02d" % (i + 1)
    push(6, tasks)

    # ---------------------------------------------------------- lekcja 7
    B.n = 0
    tasks = []
    for base in ("p", "t", "k"):
        pairs = mp.get("przydech-" + base, [])
        if not pairs:
            continue
        for k in range(min(4, len(pairs) * 2)):
            x, y = pairs[k % len(pairs)]
            if k % 2 == 0:
                tasks.append(B.same_diff("m0-lesson-07", "przydech-" + base, x, y,
                                         same=(k % 4 == 0)))
            else:
                tasks.append(B.odd_one("m0-lesson-07", "przydech-" + base, x, y))
    idx = 0
    order = ["p", "t", "k"]
    while len(tasks) < 20:
        base = order[idx % 3]
        src = asp_words[base] if idx % 2 else asp_words[base + "h"]
        r = src[(idx // 3) % len(src)]
        tasks.append(B.aspiration("m0-lesson-07", r,
                                  partner_for(r, mono, "aspiration", rng)))
        idx += 1
    tasks = tasks[:20]
    rng.shuffle(tasks)
    for i, t in enumerate(tasks):
        t["id"] = "m0-lesson-07-z%02d" % (i + 1)
    push(7, tasks)

    # ---------------------------------------------------------- lekcja 8
    B.n = 0
    tasks = []
    stop_keys = ["wyglos-p-t", "wyglos-p-k", "wyglos-t-k"]
    avail = [(k, mp.get(k, [])) for k in stop_keys]
    k = 0
    while len(tasks) < 20:
        key, pairs = avail[k % 3]
        if pairs:
            x, y = pairs[(k // 3) % len(pairs)]
            tasks.append(B.same_diff("m0-lesson-08", key, x, y, same=(k % 2 == 0)))
        k += 1
        if k > 200:
            break
    tasks = tasks[:20]
    rng.shuffle(tasks)
    for i, t in enumerate(tasks):
        t["id"] = "m0-lesson-08-z%02d" % (i + 1)
    push(8, tasks)

    # ---------------------------------------------------------- lekcja 9
    B.n = 0
    tasks = []
    k = 0
    while len(tasks) < 20:
        key, pairs = avail[k % 3]
        if pairs:
            x, y = pairs[(k // 3) % len(pairs)]
            if k % 2 == 0:
                tasks.append(B.odd_one("m0-lesson-09", key, x, y))
            else:
                tasks.append(B.odd_one("m0-lesson-09", key, y, x))
        k += 1
        if k > 200:
            break
    tasks = tasks[:20]
    rng.shuffle(tasks)
    for i, t in enumerate(tasks):
        t["id"] = "m0-lesson-09-z%02d" % (i + 1)
    push(9, tasks)

    # ---------------------------------------------------------- lekcja 10
    B.n = 0
    tasks = []
    ngp = mp.get("ng-naglos", [])
    for k in range(8):
        if not ngp:
            break
        x, y = ngp[k % len(ngp)]
        if k % 2 == 0:
            tasks.append(B.same_diff("m0-lesson-10", "ng-naglos", x, y, same=(k % 4 == 0)))
        else:
            tasks.append(B.odd_one("m0-lesson-10", "ng-naglos", x, y))
    # zliczanie sylab na wyrazach z ng — tu Polak słyszy sylabę więcej
    ngc = ng_words + ng_multi
    for k in range(8):
        r = ngc[k % len(ngc)]
        other = ng_multi[k % len(ng_multi)] if ng_multi else None
        tasks.append(B.count_syllables("m0-lesson-10", "liczba-sylab", r, other))
    tasks = tasks[:16]
    rng.shuffle(tasks)
    for i, t in enumerate(tasks):
        t["id"] = "m0-lesson-10-z%02d" % (i + 1)
    push(10, tasks)

    # ---------------------------------------------------------- lekcja 11
    B.n = 0
    tasks = []
    multi2 = [r for r in multi if len(syllables(r["thaiPhonetic"])) == 2]
    multi3 = [r for r in multi if len(syllables(r["thaiPhonetic"])) == 3]
    multi2.sort(key=lambda r: (-r.get("frequency", 0), r.get("difficulty", 5)))
    multi3.sort(key=lambda r: (-r.get("frequency", 0), r.get("difficulty", 5)))
    ordinals = ["pierwszej", "drugiej", "trzeciej"]
    for k in range(15):
        r = multi2[k % len(multi2)]
        idx = k % 2
        tasks.append(B.tone_scale("m0-lesson-11", "ton-w-wyrazie", r, None,
                                  index=idx, label=ordinals[idx]))
    for k in range(5):
        r = multi3[k % len(multi3)]
        idx = k % 3
        tasks.append(B.tone_scale("m0-lesson-11", "ton-w-wyrazie", r, None,
                                  index=idx, label=ordinals[idx]))
    for k in range(5):
        r = (multi2 + multi3)[(k * 7) % len(multi2 + multi3)]
        tasks.append(B.count_syllables("m0-lesson-11", "liczba-sylab", r, None))
    tasks = tasks[:25]
    rng.shuffle(tasks)
    for i, t in enumerate(tasks):
        t["id"] = "m0-lesson-11-z%02d" % (i + 1)
    push(11, tasks)

    # ---------------------------------------------------------- lekcja 12
    B.n = 0
    tasks = []
    sent.sort(key=lambda r: (len(syllables(r["thaiPhonetic"])), -r.get("frequency", 0)))
    ordinals6 = ["pierwszej", "drugiej", "trzeciej", "czwartej", "piątej", "szóstej"]
    for k in range(15):
        r = sent[(k * 13) % len(sent)]
        sy = syllables(r["thaiPhonetic"])
        idx = k % min(3, len(sy))
        tasks.append(B.tone_scale("m0-lesson-12", "ton-w-zdaniu", r, None,
                                  index=idx, label=ordinals6[idx]))
    for k in range(10):
        r = sent[(k * 29 + 5) % len(sent)]
        tasks.append(B.count_syllables("m0-lesson-12", "liczba-sylab", r, None))
    tasks = tasks[:25]
    rng.shuffle(tasks)
    for i, t in enumerate(tasks):
        t["id"] = "m0-lesson-12-z%02d" % (i + 1)
    push(12, tasks)

    # ------------------------------------------------------------ diagnoza
    B.n = 0
    diag = []

    def dtask(t, family):
        t["family"] = family
        diag.append(t)

    # tony płaskie (3)
    flat = [c for c, a, b in TONE_PAIRS
            if "opadający" not in (a, b) and "rosnący" not in (a, b) and mp.get(c)]
    for k in range(3):
        cid = flat[k % len(flat)]
        x, y = mp[cid][k % len(mp[cid])]
        dtask(B.same_diff("m0-diag", cid, x, y, same=(k == 1)), "tony-plaskie")
    # tony konturowe (3)
    cont = [c for c, a, b in TONE_PAIRS
            if ("opadający" in (a, b) or "rosnący" in (a, b)) and mp.get(c)]
    for k in range(2):
        cid = cont[k % len(cont)]
        x, y = mp[cid][k % len(mp[cid])]
        dtask(B.odd_one("m0-diag", cid, x, y), "tony-konturowe")
    r = by_tone["opadający"][0]
    dtask(B.tone_scale("m0-diag", "ton-opadajacy", r,
                       partner_for(r, mono, "tone", rng) or by_tone["rosnący"][0]),
          "tony-konturowe")
    # długość (3)
    for k in range(2):
        if lp:
            x, y = lp[k % len(lp)]
            dtask(B.same_diff("m0-diag", "dlugosc-samogloski", x, y, same=(k == 0)), "dlugosc")
    r = longs[3]
    dtask(B.vowel_length("m0-diag", r, partner_for(r, mono, "length", rng)), "dlugosc")
    # przydech (3)
    for base in ("p", "t", "k"):
        src = asp_words[base + "h"] if base != "t" else asp_words[base]
        r = src[0]
        dtask(B.aspiration("m0-diag", r, partner_for(r, mono, "aspiration", rng)), "przydech")
    # wygłos (3)
    for k, key in enumerate(stop_keys):
        pairs = mp.get(key, [])
        if not pairs:
            continue
        x, y = pairs[0]
        dtask(B.same_diff("m0-diag", key, x, y, same=(k == 2)), "wyglos")
    # ng (2)
    for k in range(2):
        if ngp:
            x, y = ngp[k % len(ngp)]
            dtask(B.same_diff("m0-diag", "ng-naglos", x, y, same=(k == 0)), "ng")
    # wielosylabowe (3)
    r = multi2[2]
    dtask(B.tone_scale("m0-diag", "ton-w-wyrazie", r, None, index=0, label="pierwszej"),
          "wielosylabowe")
    r = sent[7]
    dtask(B.tone_scale("m0-diag", "ton-w-zdaniu", r, None, index=0, label="pierwszej"),
          "wielosylabowe")
    r = multi3[1]
    dtask(B.count_syllables("m0-diag", "liczba-sylab", r, None), "wielosylabowe")

    for i, t in enumerate(diag):
        t["id"] = "m0-diag-z%02d" % (i + 1)

    # ------------------------------------------------------------- zapis
    fam_map = {f[0]: {"id": f[0], "label": f[1], "note": f[2]} for f in FAMILIES}
    lesson_family = {}
    for L in lessons:
        lesson_family[L["id"]] = L["families"]

    payload = {
        "file": "module-zero.json",
        "version": "1.0",
        "title": "Moduł 0 — trening słuchu",
        "intro":
            "Zanim zaczniesz uczyć się słów, ucho musi odróżnić dźwięki, z których te słowa "
            "są zbudowane. Dwanaście lekcji wyłącznie na słuch: bez znaczeń, bez zapisu, "
            "bez tłumaczeń. Odpowiadasz tylko na to, co usłyszałeś.",
        "why":
            "Polak nie usłyszy różnicy między khǎaw (biały) a khàaw (wiadomości), dopóki nie "
            "przejdzie treningu percepcyjnego. A jeśli jej nie słyszy, zapisuje oba wyrazy "
            "w pamięci jako „khaaw” — czyli błędnie. Każda następna lekcja utrwala ten błąd, "
            "więc trening słuchu musi być pierwszy, a nie ostatni.",
        "skipWarning":
            "Możesz pominąć cały moduł, ale warto wiedzieć, co się wtedy stanie. Bez treningu "
            "percepcyjnego zapamiętasz wyrazy bez tonów i bez długości samogłosek — bo tego "
            "właśnie nie usłyszysz. Będziesz je znał w wersji, której Taj nie zrozumie, "
            "a poprawianie utrwalonego zapisu jest znacznie trudniejsze niż nauczenie się "
            "go od razu dobrze. Moduł 0 zostanie na mapie kursu i możesz do niego wrócić "
            "w każdej chwili.",
        "families": [fam_map[f[0]] for f in FAMILIES],
        "contrasts": CONTRASTS,
        "taskTypes": [
            {"id": "same-diff", "label": "To samo czy inne",
             "hint": "Dwa dźwięki. Oceniasz, czy to ten sam wyraz."},
            {"id": "odd-one-out", "label": "Który jest inny",
             "hint": "Trzy dźwięki. Dwa takie same, jeden inny."},
            {"id": "tone-scale", "label": "Wskaż ton na skali",
             "hint": "Jeden dźwięk. Wybierasz kontur tonu, który słyszysz."},
            {"id": "count-syllables", "label": "Policz sylaby",
             "hint": "Jeden dźwięk. Podajesz liczbę sylab."},
            {"id": "vowel-length", "label": "Długa czy krótka",
             "hint": "Jeden dźwięk. Oceniasz długość samogłoski."},
            {"id": "aspiration", "label": "Z przydechem czy bez",
             "hint": "Jeden dźwięk. Oceniasz, czy po spółgłosce słychać podmuch."},
        ],
        "diagnostic": {
            "id": "m0-diagnostic",
            "title": "Diagnoza percepcyjna",
            "description":
                "Dwadzieścia zadań, po kilka na każdą rodzinę kontrastów. Wynik pokazuje, "
                "które kontrasty już słyszysz, a które trzeba dopiero wytrenować. Kontrasty "
                "opanowane zwalniają odpowiadające im lekcje, słabe wracają w powtórkach.",
            "mastery":
                "Rodzina kontrastów liczy się jako opanowana dopiero przy komplecie trafnych "
                "odpowiedzi. Przy dwóch–trzech zadaniach na rodzinę to próg umowny, więc "
                "zwolnione lekcje zostają dostępne — możesz je zrobić mimo wszystko.",
            "tasks": diag
        },
        "lessons": lessons,
        "stimuli": pool.order,
        "counts": {
            "lessons": len(lessons),
            "tasks": sum(len(L["tasks"]) for L in lessons),
            "diagnosticTasks": len(diag),
            "stimuli": len(pool.order),
            "contrasts": len(CONTRASTS)
        }
    }

    out = os.path.join(DATA, "module-zero.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    # ------------------------------------------------------------- raport
    print("=" * 70)
    print("MODUŁ 0 — WYGENEROWANY")
    print("=" * 70)
    print("lekcji: %d · zadań: %d · diagnoza: %d · bodźców: %d · kontrastów: %d"
          % (len(lessons), payload["counts"]["tasks"], len(diag),
             len(pool.order), len(CONTRASTS)))
    print("-" * 70)
    for L in lessons:
        kinds = collections.Counter(t["type"] for t in L["tasks"])
        print("%2d. %-42s %2d zadań (próg %2d = %d%%)"
              % (L["number"], L["title"][:42], L["pass"]["questions"],
                 L["pass"]["required"], L["pass"]["accuracy"]))
        print("      typy: %s" % ", ".join("%s×%d" % (k, v) for k, v in kinds.most_common()))
    print("-" * 70)
    print("ROZKŁAD ZADAŃ PO KONTRASTACH")
    fam_of = {c["id"]: c["family"] for c in CONTRASTS}
    for c in CONTRASTS:
        n = stats.get(c["id"], 0)
        npairs = len(mp.get(c["id"], []))
        print("  %-26s %-16s zadań %3d   par minimalnych %3d"
              % (c["id"], fam_of[c["id"]], n, npairs))
    print("-" * 70)
    byfam = collections.Counter()
    for cid, n in stats.items():
        byfam[fam_of[cid]] += n
    for f in FAMILIES:
        print("  rodzina %-16s zadań %3d" % (f[0], byfam.get(f[0], 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
