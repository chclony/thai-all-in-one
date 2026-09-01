# -*- coding: utf-8 -*-
"""Wspólna mechanika progresji gramatycznej.

Moduł odpowiada na jedno pytanie: **od której lekcji wolno pokazać dany temat
gramatyczny**. Odpowiedź nie jest kwestią gustu — wynika z materiału.

ZASADA
======

Temat gramatyczny jest wart tyle, ile zdania, którymi go pokazujemy. Reguła
„czas przyszły tworzy się przez jà" nie uczy niczego, dopóki nie stoi obok
zdania, które uczący się rozumie w całości. Jeżeli w przykładzie pada choćby
jedna sylaba, której kurs jeszcze nie wprowadził, przykład przestaje być
przykładem, a staje się drugą rzeczą do odgadnięcia.

Stąd warunek, którego pilnuje ten moduł i `tools/validate.py`:

    Temat gramatyczny może być przypisany do lekcji L tylko wtedy, gdy
    WSZYSTKIE sylaby WSZYSTKICH jego wzorców należą do zasobu znanego
    po lekcji L.

To ten sam warunek, który od sesji I obowiązuje hasła w ścieżce — rozszerzony
na gramatykę, która do tej pory była od niego wolna, bo była ozdobnikiem.

SKĄD BIERZE SIĘ ZASÓB SYLAB
===========================

Z `lessons.json`, dokładnie tak samo jak w generatorze ścieżki: zasób poszerzają
wyłącznie hasła leksykalne wprowadzane przez lekcję (`newWordIds`).

Jest jeden dopisek i trzeba go wypowiedzieć wprost, bo bez niego rachunek
kłamie. Ścieżka wprowadza formy MĘSKIE — `khráp`, `phǒm` — bo taka jest treść
domyślna rekordu. Forma żeńska (`khâ`, `khá`, `chǎn`) leży w `genderVariant`
i nie ma własnego wpisu w `syllables`. Gdyby liczyć dosłownie, sylaba `khâ`
nie weszłaby do obiegu NIGDY, a temat „partykuły grzecznościowe khráp i khâ"
byłby nie do pokazania — mimo że aplikacja od pierwszej lekcji pokazuje obie
formy obok siebie i kobieta widzi wyłącznie `khâ`.

Dlatego para form idzie do obiegu razem: w chwili, gdy ścieżka wprowadza
`khráp`, wchodzą też `khâ` i `khá`; razem z `phǒm` wchodzi `chǎn` i `dì-chǎn`.
Lista jest zamknięta i krótka, bo formy zależne od płci to w tajskim domknięty
zbiór, a nie kategoria produktywna.
"""

import json
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
DATA = os.path.join(ROOT, 'data')

# Formy zależne od płci wchodzą do obiegu parami — uzasadnienie w nagłówku.
GENDER_PAIR = {
    'khráp': ('khâ', 'khá'),
    'phǒm': ('chǎn', 'dì', 'dì-chǎn'),
}

LEX_TYPES = {'word', 'noun', 'verb', 'adjective', 'adverb'}


def load(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as f:
        return json.load(f)


def load_records(name):
    return load(name)['records']


class Corpus(object):
    """Baza haseł, kwestii dialogów i osi czasu ścieżki nauki."""

    def __init__(self):
        man = load('manifest.json')
        self.vocab_files = [f['file'] for f in man['dataFiles']
                            if f['kind'] == 'vocabulary']
        self.dialog_files = [f['file'] for f in man['dataFiles']
                             if f['kind'] == 'dialogues']

        self.records = {}
        for fn in self.vocab_files:
            for r in load_records(fn):
                self.records[r['id']] = r

        self.dialogues = []
        for fn in self.dialog_files:
            self.dialogues.extend(load_records(fn))

        self.lessons = load('lessons.json')['records']
        self._build_timeline()
        self._build_syllable_map()

    # ------------------------------------------------------------ oś czasu
    def _build_timeline(self):
        """unlock[sylaba] = numer lekcji, po której sylaba jest w obiegu."""
        known = set()
        self.unlock = {}
        for i, les in enumerate(self.lessons, 1):
            for wid in les.get('newWordIds') or []:
                rec = self.records.get(wid)
                if not rec:
                    continue
                for s in rec.get('syllables') or []:
                    known.add(s)
                    for extra in GENDER_PAIR.get(s, ()):
                        known.add(extra)
            for s in known:
                self.unlock.setdefault(s, i)
        self.known = known
        self.total_lessons = len(self.lessons)

    def _build_syllable_map(self):
        """Zapis fonetyczny -> podział na sylaby.

        Bierzemy go z pola `syllables` rekordów, bo tam jest wyliczony raz
        i zgodny z resztą bazy. Dla tekstów spoza bazy (kwestie dialogów mają
        własny zapis) wracamy do podziału po spacjach i dywizach — ten sam,
        którym posługuje się `coverage.py`.
        """
        self.phon2syl = {}
        for r in self.records.values():
            p, s = r.get('thaiPhonetic'), r.get('syllables')
            if p and s:
                self.phon2syl.setdefault(p, list(s))

    def syllables(self, text):
        if text in self.phon2syl:
            return list(self.phon2syl[text])
        return [t for t in re.split(r'[ \-]+', text or '') if t]

    # -------------------------------------------------------- dostępność
    def available_from(self, text):
        """Numer lekcji, po której cały tekst mieści się w zasobie.

        None, jeżeli któraś sylaba nie wchodzi do obiegu nigdy — taki tekst
        nie nadaje się na wzorzec, bo dla uczącego się zawsze zostanie
        częściowo nieczytelny.
        """
        syls = self.syllables(text)
        if not syls:
            return None
        worst = 0
        for s in syls:
            u = self.unlock.get(s)
            if u is None:
                return None
            worst = max(worst, u)
        return worst

    def missing_syllables(self, text):
        return sorted({s for s in self.syllables(text)
                       if s not in self.unlock})

    def topic_available_from(self, patterns):
        """Dostępność tematu = najpóźniejszy z jego wzorców."""
        worst = 0
        for p in patterns:
            a = self.available_from(p['thaiPhonetic'])
            if a is None:
                return None
            worst = max(worst, a)
        return worst

    # ------------------------------------------------------------- pule
    def sentence_pool(self):
        """Materiał, z którego wolno brać wzorce.

        Hasła leksykalne odpadają: „musieć" nie ilustruje niczego poza sobą.
        Wzorzec ma być wypowiedzią, więc bierzemy zdania, pytania, zwroty
        i kolokacje z bazy oraz kwestie dialogów.
        """
        out = []
        for r in self.records.values():
            if r['type'] in LEX_TYPES:
                continue
            out.append({
                'polish': r.get('polish', ''),
                'thaiPhonetic': r.get('thaiPhonetic', ''),
                'pronunciationPolish': r.get('pronunciationPolish', ''),
                'ttsThai': r.get('ttsThai', ''),
                'ttsSplit': r.get('ttsSplit'),
                'genderVariant': r.get('genderVariant'),
                'colloquial': r.get('colloquial'),
                '_src': r['id'],
                '_type': r['type'],
                '_level': r.get('level', ''),
                '_freq': int(r.get('frequency') or 0),
            })
        for d in self.dialogues:
            for ln in d.get('lines') or []:
                out.append({
                    'polish': ln.get('polish', ''),
                    'thaiPhonetic': ln.get('thaiPhonetic', ''),
                    'pronunciationPolish': ln.get('pronunciationPolish', ''),
                    'ttsThai': ln.get('ttsThai', ''),
                    'ttsSplit': ln.get('ttsSplit'),
                    'genderVariant': ln.get('genderVariant'),
                    'colloquial': ln.get('colloquial'),
                    '_src': '%s#%s' % (d['id'], ln.get('index')),
                    '_type': 'dialogue',
                    '_level': d.get('level', ''),
                    '_freq': 3,
                })
        return out


# ------------------------------------------------------------------ wybór
def clean_pattern(p):
    """Wzorzec do zapisu: same pola treściowe, bez śladów po doborze."""
    out = {
        'polish': p['polish'],
        'thaiPhonetic': p['thaiPhonetic'],
        'pronunciationPolish': p.get('pronunciationPolish', ''),
        'ttsThai': p.get('ttsThai', ''),
    }
    for k in ('ttsSplit', 'genderVariant', 'colloquial'):
        if p.get(k):
            out[k] = p[k]
    out['sourceId'] = p.get('_src', '')
    return out


def select_patterns(corpus, pool, include, exclude=None, want=6, min_syl=2,
                    max_syl=12, need_space=True, pl_include=None,
                    pl_exclude=None):
    """Wzorce dla tematu: pasujące, wyrażalne, jak najwcześniej dostępne.

    Kolejność doboru jest celowa. Sortujemy po dostępności rosnąco, bo temat
    ma się otworzyć najwcześniej, jak pozwala materiał — wzorzec dostępny
    dopiero w lekcji 280 przesunąłby cały temat na koniec kursu, choć obok
    leży zdanie o tej samej konstrukcji dostępne w lekcji 40.
    """
    # Rekordy szablonowe („phûut wâa … yùu") mają w zapisie wielokropek albo
    # podkreślenie w miejscu, które użytkownik ma wypełnić sam. Jako wzorzec
    # gramatyczny się nie nadają: syntezator nie ma czego z nich powiedzieć,
    # a pole `syllables` po cichu pomija taki znak, więc kontrola dostępności
    # liczyłaby coś innego, niż uczący się zobaczy na ekranie.
    PLACEHOLDER = re.compile(r'[.…_]{2,}|\.\.\.|…')

    inc = re.compile(include)
    exc = re.compile(exclude) if exclude else None
    pinc = re.compile(pl_include, re.I) if pl_include else None
    pexc = re.compile(pl_exclude, re.I) if pl_exclude else None
    cand = []
    seen_pl, seen_ph = set(), set()
    for p in pool:
        ph = p['thaiPhonetic']
        pl = p['polish']
        if not ph or not pl:
            continue
        if PLACEHOLDER.search(ph):
            continue
        if not inc.search(ph):
            continue
        if exc and exc.search(ph):
            continue
        if pinc and not pinc.search(pl):
            continue
        if pexc and pexc.search(pl):
            continue
        if need_space and ' ' not in ph:
            continue
        syls = corpus.syllables(ph)
        if not (min_syl <= len(syls) <= max_syl):
            continue
        av = corpus.available_from(ph)
        if av is None:
            continue
        cand.append((av, len(syls), -p['_freq'], p['_src'], p))
    cand.sort(key=lambda x: (x[0], x[1], x[2], x[3]))

    out = []
    for av, nsyl, negf, src, p in cand:
        key_pl = p['polish'].strip().lower()
        key_ph = p['thaiPhonetic'].strip()
        if key_pl in seen_pl or key_ph in seen_ph:
            continue
        seen_pl.add(key_pl)
        seen_ph.add(key_ph)
        out.append(p)
        if len(out) >= want:
            break
    return out


# -------------------------------------------------------------- przydział
MAX_GAP_TRY = 4


def _forward(topics, gap):
    fwd, prev = [], None
    for t in topics:
        at = t['availableFrom'] if prev is None else max(t['availableFrom'],
                                                         prev + gap)
        fwd.append(at)
        prev = at
    return fwd


def assign_to_lessons(topics, total_lessons):
    """Rozstawia tematy na ścieżce: kolejność dydaktyczna, ale nie wcześniej,
       niż pozwala materiał, i możliwie równomiernie.

    Trzy kroki:

      1. **odstęp minimalny.** Temat, po którym w następnej lekcji wchodzi
         kolejny, nie ma kiedy się osadzić — uczący się dostaje regułę
         i natychmiast następną. Szukamy więc największego odstępu z zakresu
         1..4, przy którym cały ciąg jeszcze mieści się na ścieżce, i to on
         wyznacza minimum między wprowadzeniami.
      2. **w przód** — najwcześniejszy dopuszczalny układ monotoniczny:
         `at[i] = max(dostępność[i], at[i-1] + odstęp)`. To jedyny układ,
         który nigdy nie łamie warunku; wszystko inne jest jego przesunięciem
         w prawo.
      3. **wstecz** — rozsunięcie. Sam przebieg 2 upycha tematy jeden przy
         drugim za każdą „ścianą" dostępności i zostawia pustkę dalej.
         Przebieg 3 przesuwa każdy temat tak blisko pozycji idealnej, jak
         pozwala temat następny — nigdy przed pozycję z przebiegu 2.

    Czego to NIE naprawia i trzeba powiedzieć wprost: jeżeli sześć tematów
    wchodzi do obiegu w tej samej lekcji, bo ich materiał pojawia się razem,
    to będą stały obok siebie mimo odstępu minimalnego — odstęp ustępuje
    dostępności, bo dostępność jest warunkiem, a odstęp tylko wygodą.
    """
    n = len(topics)
    if not n:
        return []

    gap = 1
    for g in range(MAX_GAP_TRY, 0, -1):
        if _forward(topics, g)[-1] <= total_lessons:
            gap = g
            break
    fwd = _forward(topics, gap)
    if fwd[-1] > total_lessons:
        raise ValueError('nie mieści się na ścieżce: ostatni temat w lekcji %d '
                         'przy %d lekcjach' % (fwd[-1], total_lessons))

    step = total_lessons / float(n)
    out = list(fwd)
    nxt = total_lessons + 1
    for i in range(n - 1, -1, -1):
        ideal = int(round(i * step)) + 1
        out[i] = max(fwd[i], min(ideal, nxt - gap))
        nxt = out[i]
    return out
