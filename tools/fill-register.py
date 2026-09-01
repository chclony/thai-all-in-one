#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uzupełnienie pola `register` tam, gdzie da się je USTALIĆ, a nie zgadnąć.

Rejestr (neutralny / uprzejmy / formalny / nieformalny / potoczny) jest
w słowniku wypełniony dla wszystkich 20 790 haseł, ale poza słownikiem —
w ćwiczeniach gramatycznych, wzorcach i dialogach — pozostał pusty.

Zasady, w kolejności od najmocniejszego dowodu do najsłabszego:

  1. ŹRÓDŁO. Rekord z `sourceId` jest przekształceniem konkretnego hasła
     słownikowego. Rejestr dziedziczy po źródle — to nie domysł, tylko ta
     sama wypowiedź w innym ćwiczeniu.
  2. JAWNA CECHA. `grammar-listening.json` ma pole `polite`. Gdy jest
     ustawione, ma pierwszeństwo przed dziedziczeniem: opisuje TĘ wypowiedź.
  3. CECHY ZDANIA. Końcowa partykuła grzecznościowa (khráp / khâ / khá)
     to uprzejmość wypowiedziana wprost. Partykuły i zaimki nieformalne
     (wá, wóoi, kuu, mueng) — odwrotnie.
  4. BRAK CECH w pełnym zdaniu = `neutralny`. Tak właśnie opisane jest
     17 656 haseł słownika: neutralny to nie „nie wiem”, tylko zdanie bez
     znaczników grzeczności.

Czego NIE wypełniamy: gołych jednostek leksykalnych — liczebników, słów
kluczowych scen, rzeczowników przy klasyfikatorach, sylab z ćwiczeń wymowy.
Rejestr jest cechą WYPOWIEDZI, nie wyrazu hasłowego; wpisanie im
czegokolwiek byłoby zgadywaniem. Te pozycje zostają puste i są policzone.

Skrypt nie dodaje ani nie usuwa rekordów — wyłącznie uzupełnia opis.
"""
import json
import os
import re
import sys
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')

VALUES = ('neutralny', 'uprzejmy', 'formalny', 'nieformalny', 'potoczny')

# Partykuły grzecznościowe na końcu wypowiedzi.
POLITE = re.compile(r'(^|\s)(khráp|khrap|kháp|khâ|khá|kha|kha)(\s|$)', re.I)
# Znaczniki nieformalne: partykuły i zaimki, których nie używa się do obcych.
INFORMAL = re.compile(r'(^|\s)(wá|wâ|wóoi|wooi|kuu|mueng|mʉng|jà|dì)(\s|$)', re.I)
# Zwroty urzędowe / formalne.
FORMAL = re.compile(r'(^|\s)(krú-naa|krunaa|dì-chǎn|dichǎn|thâan|kràp-phǒm)(\s|$)', re.I)

# Ścieżki, dla których rejestr NIE jest zdefiniowany (gołe jednostki leksykalne).
LEXICAL_ONLY = {
    ('numbers.json', 'records[]'),
    ('numbers.json', 'scenes[].lines[]'),
    ('scenes.json', 'records[].keywords[]'),
    ('classifiers.json', 'records[].nouns[]'),
    ('pronunciation.json', 'exercises[].items[].options[]'),
    ('pronunciation.json', 'minimalPairs[].items[]'),
    ('pronunciation.json', 'tones[].example'),
    ('pronunciation.json', 'exercises[].items[]'),
}


def load(fn):
    with open(os.path.join(DATA, fn), encoding='utf-8') as f:
        return json.load(f)


def save(fn, data):
    with open(os.path.join(DATA, fn), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write('\n')


def source_registers():
    """Rejestr każdego hasła słownikowego — podstawa dziedziczenia."""
    man = load('manifest.json')
    out = {}
    for f in man['dataFiles']:
        if f['kind'] != 'vocabulary':
            continue
        for r in load(f['file'])['records']:
            if r.get('register'):
                out[r['id']] = r['register']
    return out


def sentence_like(node):
    """Czy to WYPOWIEDŹ, czy goły wyraz hasłowy.

    Rejestr opisuje sposób mówienia do kogoś, więc ma sens dopiero tam,
    gdzie jest zdanie. Jednowyrazowe hasło zostaje bez rejestru.
    """
    txt = (node.get('thaiPhonetic') or '').strip()
    pl = (node.get('polish') or node.get('pl') or '').strip()
    if not txt:
        return False
    if len(txt.split()) >= 3:
        return True
    # dwa wyrazy z partykułą grzecznościową to już wypowiedź („khàwp-khun khráp”)
    if POLITE.search(txt) or INFORMAL.search(txt):
        return True
    return bool(re.search(r'[.?!]$', pl))


def decide(node, path, fn, src):
    """Zwraca (wartość, powód) albo (None, powód pozostawienia pustego)."""
    if path.endswith('examples[]'):
        # Zdanie przykładowe należy do swojego hasła i dzieli jego rejestr.
        # Wpisanie mu własnego rejestru nic nie wnosi, a rozjeżdża opis
        # z hasłem przy każdej późniejszej zmianie hasła.
        return None, 'przykład dziedziczy rejestr hasła'
    if (fn, path) in LEXICAL_ONLY:
        return None, 'goła jednostka leksykalna'

    # 2. jawna cecha ma pierwszeństwo — opisuje TĘ wypowiedź
    if 'polite' in node and isinstance(node.get('polite'), bool):
        if node['polite']:
            return 'uprzejmy', 'pole polite'
        # polite=False nie znaczy „nieformalny”; znaczy „bez grzecznościówki”
        if INFORMAL.search(node.get('thaiPhonetic') or ''):
            return 'nieformalny', 'pole polite + partykuła nieformalna'
        return 'neutralny', 'pole polite'

    txt = node.get('thaiPhonetic') or ''

    # 3. cechy zdania wypowiedziane wprost biją dziedziczenie:
    #    przekształcenie mogło DODAĆ grzecznościówkę do neutralnego źródła
    if POLITE.search(txt):
        return 'uprzejmy', 'partykuła grzecznościowa'
    if FORMAL.search(txt):
        return 'formalny', 'zwrot formalny'
    if INFORMAL.search(txt):
        return 'nieformalny', 'partykuła nieformalna'

    # 1. źródło
    sid = node.get('sourceId')
    if sid and sid in src:
        return src[sid], 'dziedziczenie po źródle'

    # 4. pełne zdanie bez znaczników
    if sentence_like(node):
        return 'neutralny', 'zdanie bez znaczników grzeczności'

    return None, 'za mało cech, żeby ustalić'


def main():
    dry = '--proba' in sys.argv or '--próba' in sys.argv
    src = source_registers()
    filled = collections.Counter()
    reasons = collections.Counter()
    left = collections.Counter()
    changed_files = []

    for fn in sorted(os.listdir(DATA)):
        if not fn.endswith('.json') or fn.startswith('search-index'):
            continue
        data = load(fn)
        touched = [0]

        def walk(node, path):
            if isinstance(node, dict):
                if ('thaiPhonetic' in node
                        and ('polish' in node or 'pl' in node)
                        and not node.get('register')):
                    val, why = decide(node, path, fn, src)
                    if val:
                        assert val in VALUES, val
                        node['register'] = val
                        filled[val] += 1
                        reasons[why] += 1
                        touched[0] += 1
                    else:
                        left[(fn, path, why)] += 1
                for k, v in list(node.items()):
                    walk(v, path + '.' + k if path else k)
            elif isinstance(node, list):
                for v in node:
                    walk(v, path + '[]')

        walk(data, '')
        if touched[0] and not dry:
            save(fn, data)
            changed_files.append('%s (%d)' % (fn, touched[0]))

    print('=' * 74)
    print('UZUPEŁNIENIE POLA `register`%s' % (' — PRÓBA, bez zapisu' if dry else ''))
    print('=' * 74)
    print('Uzupełniono: %d' % sum(filled.values()))
    for k, v in filled.most_common():
        print('   %-14s %5d' % (k, v))
    print('\nNa jakiej podstawie:')
    for k, v in reasons.most_common():
        print('   %-38s %5d' % (k, v))
    total_left = sum(left.values())
    print('\nZostawiono puste: %d' % total_left)
    agg = collections.Counter()
    for (fn, path, why), n in left.items():
        agg[why] += n
    for k, v in agg.most_common():
        print('   %-38s %5d' % (k, v))
    print('\nGdzie zostały puste:')
    per = collections.Counter()
    for (fn, path, why), n in left.items():
        per['%s %s' % (fn, path)] += n
    for k, v in per.most_common(12):
        print('   %-52s %5d' % (k, v))
    if changed_files:
        print('\nZmienione pliki: %s' % ', '.join(changed_files))
    return 0


if __name__ == '__main__':
    sys.exit(main())
