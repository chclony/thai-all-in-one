#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Higiena bazy: usunięcie faktycznych duplikatów i rozróżnienie pozornych.

Audyt sesji V zgłosił 13 duplikatów: 7 powtórzonych glos polskich,
5 powtórzonych fonetyk, 1 powtórzony w obu wymiarach. Przegląd rekord po
rekordzie pokazał, że kryterium audytu było za grube i że SKASOWANIE 13
rekordów wycięłoby z bazy prawdziwe słownictwo. Rozkład jest taki:

  · 1 duplikat prawdziwy — ta sama glosa, ta sama fonetyka, to samo pismo
    tajskie (srv-time-0004 / a1-time-0040). Ten usuwamy; zostaje rekord
    lepiej opisany, czyli ten z dwoma przykładami użycia.

  · 4 powtórzone fonetyki to HOMONIMY o różnym piśmie tajskim:
    ส้อม widelec / ซ่อม naprawiać, เหล้า alkohol / เล่า opowiadać,
    แต่ ale / แตะ dotykać, หญ้า trawa / ย่า babcia. To osobne słowa,
    które zbiegają się dopiero w zapisie fonetycznym. Zostają.

  · 4 pary o wspólnej glosie różnią się końcówką grzecznościową (khráp).
    To ta sama treść w dwóch rejestrach — materiał, nie śmieć. Trzy z nich
    miały OBA warianty opisane jako „neutralny” i to właśnie robiło z nich
    pozorny duplikat. Poprawiamy opis, nie kasujemy zdania.

  · 1 para („Nie mogę spać.") to dwa różne zwroty tajskie: nawn mâi dâai
    (nie ma warunków, żeby spać) i nawn mâi làp (nie udaje się zasnąć).
    Doprecyzowujemy polską glosę.

  · 1 para („Idziesz razem ze mną.") to formy męska i żeńska tego samego
    zdania. Rekord żeński wygląda na zbędny — jego treść siedzi już
    w genderVariant.female rekordu męskiego — ale jest JEDYNYM zdaniem,
    w którym lekcja 043 ćwiczy zaimek „chǎn" (srv-basic-0018, „ja
    (kobieta)"). Usunięcie go zrywa warunek dydaktyczny kursu, co wykrył
    walidator. Zostaje; rozróżnia je płeć mówiącego.

Netto: usuwamy 1 rekord z 20 792, a 12 pozostałych zgłoszeń domykamy
poprawieniem opisu. Baza po tym zabiegu nie ma ani jednej pary
nierozróżnialnej dla uczącego się — pilnuje tego validate.py.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')

# usuwany -> rekord, na który przepinamy odwołania
DROP = {'a1-time-0040': 'srv-time-0004'}

# khráp/khâ na końcu = forma uprzejma; były opisane jako neutralne
POLITE_FIX = ['a2-talk-0008', 'a2-talk-0009', 'a2-talk-0010', 'a2-health-0014']

# doprecyzowanie glosy: nawn mâi làp to „nie udaje się zasnąć"
GLOSS_FIX = {'a2-health-0014': ('Nie mogę spać.', 'Nie mogę zasnąć.')}

# Rekord zachowany z pary bliźniaków miał `type: word`, choć jest pełnym
# zdaniem („Widzieliśmy się wczoraj.", pięć sylab, orzeczenie). Bliźniak,
# którego usuwamy, był otypowany poprawnie jako `sentence`. To ten błąd
# opisu wymusił w swoim czasie istnienie duplikatu: reguła „nowe hasło musi
# dać się użyć w zdaniu lekcji" szuka INNEGO rekordu zawierającego sylaby
# hasła, a dla zdania takiego rekordu z natury nie ma. Bliźniak był tym
# „innym rekordem". Poprawiamy typ i regułę, zamiast hodować duplikat.
TYPE_FIX = {'srv-time-0004': ('word', 'sentence')}


def load(fn):
    with open(os.path.join(DATA, fn), encoding='utf-8') as f:
        return json.load(f)


def save(fn, data):
    with open(os.path.join(DATA, fn), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write('\n')


def main():
    man = load('manifest.json')
    vocab = [f['file'] for f in man['dataFiles'] if f['kind'] == 'vocabulary']

    removed = 0
    for fn in vocab:
        d = load(fn)
        before = len(d['records'])
        d['records'] = [r for r in d['records'] if r['id'] not in DROP]
        gone = before - len(d['records'])
        if gone:
            removed += gone
            d['count'] = len(d['records'])
            # manifest musi zgadzać się z plikiem, inaczej walidator woła
            for entry in man['dataFiles']:
                if entry['file'] == fn:
                    entry['count'] = len(d['records'])
            save(fn, d)
    man['totalRecords'] = man.get('totalRecords', 0) - removed
    save('manifest.json', man)
    print('usunięto duplikatów: %d' % removed)

    # przepięcie odwołań (indeks wyszukiwania generuje się osobno)
    touched = []
    for fn in sorted(os.listdir(DATA)):
        if not fn.endswith('.json') or fn.startswith('search-index'):
            continue
        p = os.path.join(DATA, fn)
        txt = open(p, encoding='utf-8').read()
        orig = txt
        for old, new in DROP.items():
            txt = re.sub(r'"%s"' % re.escape(old), '"%s"' % new, txt)
        if txt != orig:
            open(p, 'w', encoding='utf-8').write(txt)
            touched.append(fn)
    print('przepięto odwołania w: %s' % ', '.join(touched))

    # rejestr form uprzejmych + doprecyzowanie glosy
    fixed_reg = fixed_gloss = 0
    for fn in vocab:
        d = load(fn)
        ch = False
        for r in d['records']:
            if r['id'] in POLITE_FIX and r.get('register') != 'uprzejmy':
                r['register'] = 'uprzejmy'
                fixed_reg += 1
                ch = True
            if r['id'] in TYPE_FIX:
                old, new = TYPE_FIX[r['id']]
                if r.get('type') == old:
                    r['type'] = new
                    ch = True
                    print('typ poprawiony: %s %s -> %s' % (r['id'], old, new))
            if r['id'] in GLOSS_FIX:
                old, new = GLOSS_FIX[r['id']]
                if r.get('polish') == old:
                    r['polish'] = new
                    fixed_gloss += 1
                    ch = True
        if ch:
            save(fn, d)
    print('rejestr poprawiony: %d | glosa doprecyzowana: %d'
          % (fixed_reg, fixed_gloss))

    # Przepięcie mogło wstawić do lekcji identyfikator, który już tam był.
    # Odsiewamy powtórzenia z zachowaniem kolejności i zdejmujemy hasło
    # z listy NOWYCH słów, jeśli kurs wprowadził je wcześniej.
    lessons = load('lessons.json')
    seen_new = {}
    for L in lessons['records']:
        for wid in L.get('newWordIds', []):
            seen_new.setdefault(wid, L['id'])
    fixed_dupes = fixed_new = 0
    for L in lessons['records']:
        for key in ('recordIds', 'newWordIds'):
            if key not in L:
                continue
            out, seen = [], set()
            for rid in L[key]:
                if rid in seen:
                    fixed_dupes += 1
                    continue
                seen.add(rid)
                out.append(rid)
            L[key] = out
        for wid in list(L.get('newWordIds', [])):
            if seen_new.get(wid) and seen_new[wid] != L['id']:
                L['newWordIds'].remove(wid)
                fixed_new += 1

    # Duplikat potrafił PODPIERAĆ warunek dydaktyczny lekcji: reguła „każde
    # nowe hasło musi dać się w tej lekcji użyć" szuka INNEGO rekordu, który
    # zawiera sylaby nowego hasła. Para bliźniaków spełniała ją sama sobą,
    # bo identyfikatory się różniły. Po sklejeniu pary warunek przestaje być
    # spełniony — i słusznie, bo w lekcji nie ma drugiego zdania z tym
    # materiałem. Takie hasło przestaje być „nowym słowem" lekcji, ale
    # zostaje jej materiałem ćwiczeniowym.
    by_id = {}
    for f in man['dataFiles']:
        if f['kind'] == 'vocabulary':
            for r in load(f['file'])['records']:
                by_id[r['id']] = r
    unpropped = 0
    for L in lessons['records']:
        ids = L.get('recordIds', [])
        for wid in list(L.get('newWordIds', [])):
            if wid not in by_id or wid not in DROP.values():
                continue
            wsyl = set(by_id[wid].get('syllables') or [])
            usable = any(rid != wid and rid in by_id
                         and wsyl <= set(by_id[rid].get('syllables') or [])
                         for rid in ids)
            if not usable and (by_id[wid].get('type')
                               not in ('sentence', 'question', 'phrase')):
                L['newWordIds'].remove(wid)
                unpropped += 1
    if unpropped:
        print('haseł zdjętych z „nowych słów" po sklejeniu bliźniaków: %d'
              % unpropped)
    save('lessons.json', lessons)
    print('odsianych powtórzeń w lekcjach: %d, zdjętych z „nowych słów": %d'
          % (fixed_dupes, fixed_new))

    return 0


if __name__ == '__main__':
    sys.exit(main())
