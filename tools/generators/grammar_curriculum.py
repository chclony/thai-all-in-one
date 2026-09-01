# -*- coding: utf-8 -*-
"""Ciąg dydaktyczny gramatyki tajskiej dla polskiego ucha.

CO TU JEST UPORZĄDKOWANE I DLACZEGO TAK
=======================================

Kolejność nie jest kolejnością podręcznika ani kolejnością trudności. Jest
kolejnością, w jakiej konstrukcja zaczyna być POTRZEBNA do rozumienia — bo
temu ma służyć cały ten moduł.

Osiem etapów:

  1. **Szkielet zdania.** Co niesie znaczenie, skoro nie niesie go końcówka.
     Bez tego uczący się szuka w tajskim rzeczy, których tam nie ma.
  2. **Pytanie i przeczenie.** Pierwszy podział, który trzeba usłyszeć:
     czy rozmówca coś stwierdza, czy o coś pyta. Pomyłka tutaj kosztuje
     najwięcej, bo zmienia rolę słuchacza.
  3. **Czas i aspekt.** Tajski nie odmienia czasownika, więc czas leży
     w cząstkach i okolicznikach. To najczęstsze miejsce, w którym Polak
     rozumie słowa i gubi sens.
  4. **Prośba, rozkaz, modalność.** Ta sama treść w trzech różnych
     intencjach. Rozróżnienie jest gramatyczne, nie tonalne.
  5. **Rozbudowa frazy.** Klasyfikatory, określenia, porównania — wszystko,
     co stoi wokół rzeczownika i decyduje, o którym egzemplarzu mowa.
  6. **Łączenie zdań.** Spójniki, warunek, przyczyna, ustępstwo. Tu zaczyna
     się rozumienie wypowiedzi dłuższej niż jedno zdanie.
  7. **Mowa zależna i strona bierna.** Kto mówi, kto działa, kto obrywa.
  8. **Partykuły końcowe.** Ostatni, bo najtrudniejszy: niosą znaczenie,
     którego polszczyzna nie koduje w ogóle.

CZEGO BRAKOWAŁO W 26 TEMATACH
=============================

Stare 26 tematów pokrywało etapy 1, 2 i część 4 i 5. Nie było w nich ANI
JEDNEGO tematu z etapów 6, 7 i 8: żadnego spójnika złożonego, żadnej mowy
zależnej, żadnego trybu warunkowego, żadnej strony biernej i żadnej partykuły
końcowej poza `khráp`/`khâ`. Aspekt był reprezentowany przez trzy tematy
(`jà`, `láew`, `kamlang`) bez powiedzenia, że to JEDEN system.

POLE `select`
=============

Każdy nowy temat opisuje, po czym poznać materiał, który go ilustruje.
Wzorce NIE są pisane ręcznie — są wybierane z bazy. Powód jest praktyczny
i wart wypowiedzenia: ręcznie napisane zdanie tajskie nie ma pisma tajskiego
do syntezy, nie ma wariantu żeńskiego, nie ma zapisu potocznego i nie ma
gwarancji, że jego sylaby w ogóle wchodzą do obiegu kursu. Zdanie wzięte
z bazy ma to wszystko z definicji i przeszło już walidację.
"""

# Etapy: (numer, tytuł, opis)
STAGES = [
    (1, 'Szkielet zdania',
     'Co niesie znaczenie w języku, który nie odmienia wyrazów.'),
    (2, 'Pytanie i przeczenie',
     'Pierwszy podział, który trzeba usłyszeć: pytanie czy stwierdzenie.'),
    (3, 'Czas i aspekt',
     'Czas leży w cząstkach i okolicznikach, nigdy w czasowniku.'),
    (4, 'Prośba, rozkaz, modalność',
     'Ta sama treść w trzech intencjach — różnicę robi konstrukcja.'),
    (5, 'Rozbudowa frazy',
     'Wszystko, co stoi wokół rzeczownika i wskazuje, o co dokładnie chodzi.'),
    (6, 'Łączenie zdań',
     'Spójniki, warunek, przyczyna, ustępstwo — wypowiedź dłuższa niż zdanie.'),
    (7, 'Mowa zależna i strona bierna',
     'Kto mówi, kto działa, a kto tylko obrywa.'),
    (8, 'Partykuły końcowe',
     'Znaczenie, którego polszczyzna nie koduje w ogóle.'),
]

# Wspólne skróty do selektorów.
_W = r'(^|[ ])'          # granica wyrazu w zapisie fonetycznym
_E = r'($|[ ])'


def w(x):
    return _W + x + _E


# ---------------------------------------------------------------------------
# CIĄG DYDAKTYCZNY
#
# keep  — temat istniejący; zachowujemy tytuł, wyjaśnienie i wskazówkę,
#         wzorce filtrujemy przez warunek dostępności i uzupełniamy z bazy.
# select— selektor materiału ilustrującego.
# ---------------------------------------------------------------------------

CURRICULUM = [

    # ================= ETAP 1 — SZKIELET ZDANIA =================
    # Selektor jest tu celowo szeroki. Temat otwiera cały kurs, więc musi
    # dać się pokazać materiałem lekcji pierwszej — a po lekcji pierwszej
    # w obiegu jest trzynaście haseł. Zawężanie po polskiej stronie
    # („Ja …”, „On …”) przesuwałoby go na lekcję dziewiątą.
    dict(id='gram-001', stage=1, family='szyk', keep=True,
         select=dict(include=w(r'(phǒm|khun|kháw|rao)'), min_syl=2),
         contrast='Polak szuka końcówki osoby i czasu. Nie ma jej i nie będzie '
                  '— osobę niesie zaimek albo sam kontekst.'),

    dict(id='gram-002', stage=1, family='szyk', keep=True,
         select=dict(include=w('phǒm') + r'.+ .+',
                     pl_exclude=r'\?'),
         contrast='Polski szyk jest swobodny, bo trzyma go przypadek. Tajski '
                  'przypadka nie ma, więc szyk jest jedyną informacją o tym, '
                  'kto komu co robi. Przestawienie zmienia sens.'),

    dict(id='gram-030', stage=1, family='szyk', level='Survival',
         title='Zdanie bez podmiotu',
         explanation='Jeżeli wiadomo, o kim mowa, zaimek znika. Tajskie zdanie '
                     'zaczyna się wtedy od czasownika i to jest wypowiedź '
                     'pełna, nie skrót ani nie forma niedbała.',
         tip='Brak zaimka nie znaczy „bezosobowo”. Znaczy „o tym, o kim '
             'przed chwilą była mowa”.',
         contrast='Polak słyszy zdanie bez podmiotu i szuka podmiotu '
                  'domyślnego w końcówce czasownika. Tajski końcówki nie ma '
                  '— podmiot trzeba wziąć z poprzedniego zdania.',
         select=dict(include=r'^(mii|pai|maa|ao|kin|sèt|dâai|khâo|klàp|yàak)' + _E,
                     exclude=w(r'(phǒm|chǎn|khun|kháw|rao)'),
                     min_syl=3)),

    dict(id='gram-031', stage=1, family='istnienie', level='Survival',
         title='mii — jest, są, mam',
         explanation='Jedno słowo obsługuje istnienie i posiadanie. '
                     '`mii náam` to zależnie od sytuacji „jest woda” albo '
                     '„mam wodę”; rozstrzyga kontekst, nie forma.',
         tip='Pytanie o dostępność czegokolwiek zaczyna się od `mii`, '
             'a kończy na `mǎi`. To najczęstsze pytanie turysty.',
         contrast='Polski rozdziela „jest” i „mam” na dwa czasowniki. Tajski '
                  'nie rozdziela, więc tłumaczenie trzeba wybrać z sytuacji.',
         select=dict(include=w('mii'), min_syl=3)),

    dict(id='gram-032', stage=1, family='istnienie', level='A1',
         title='pen — to jest, jestem kimś',
         explanation='`pen` łączy podmiot z rzeczownikiem: zawód, narodowość, '
                     'rola, choroba. Stoi wyłącznie przed rzeczownikiem.',
         tip='Przed przymiotnikiem `pen` NIE stoi. „Jestem zmęczony” to sam '
             'przymiotnik, bez łącznika.',
         contrast='Polak wstawia „być” wszędzie, gdzie polszczyzna go używa, '
                  'i mówi `pen nùeai` zamiast `nùeai`. To brzmi jak '
                  '„jestem zmęczeniem”.',
         select=dict(include=w('pen'), min_syl=3)),

    dict(id='gram-033', stage=1, family='istnienie', level='Survival',
         title='Przymiotnik jest czasownikiem',
         explanation='`à-ròi` znaczy nie „smaczny”, tylko „być smacznym”. '
                     'Przymiotnik sam tworzy orzeczenie, więc między nim '
                     'a podmiotem nie ma żadnego łącznika.',
         tip='Przeczenie stawiamy tak samo jak przy czasowniku: `mâi à-ròi`.',
         contrast='Najczęstszy błąd Polaka na poziomie Survival: dokładanie '
                  '`pen` albo `yùu` przed przymiotnikiem. Tajski tego nie ma '
                  'i brzmi to obco od pierwszej sylaby.',
         select=dict(include=w(r'(à-ròi|phaeng|thùuk|yài|lék|dii|rórn|yen|sǔai|nùeai|ngîap)'),
                     exclude=w(r'(pen|yùu)'), min_syl=2)),

    dict(id='gram-034', stage=1, family='szyk', level='A1',
         title='Dwa czasowniki pod rząd',
         explanation='Tajski zestawia czasowniki bez żadnego łącznika: '
                     '`pai kin` — „iść jeść”, czyli „idę coś zjeść”. '
                     'Pierwszy czasownik mówi o ruchu albo o zamiarze, drugi '
                     'o właściwej czynności.',
         tip='Nie szukaj tu bezokolicznika ani spójnika „żeby”. Kolejność '
             'czasowników sama nadaje sens.',
         contrast='Polak wstawia „żeby” (`phûea`), co jest poprawne, ale '
                  'w mowie codziennej brzmi ciężko. Tajowie zestawiają.',
         select=dict(include=w(r'(pai|maa|klàp|khâo|àwk)') + r' *(kin|duu|ao|séu|súe|hǎa|tham|rian|nawn|sòng)' + _E,
                     min_syl=3)),

    dict(id='gram-007', stage=1, family='rejestr', keep=True,
         select=dict(include=w('khráp')),
         contrast='Polszczyzna grzeczność koduje w formie „pan/pani” i trybie '
                  'przypuszczającym. Tajski dokłada cząstkę na końcu i jej '
                  'brak jest słyszalny natychmiast.'),

    dict(id='gram-008', stage=1, family='rejestr', keep=True,
         select=dict(include=w(r'(phǒm|khun|kháw|rao)')),
         contrast='Tajski zaimek pierwszej osoby zależy od płci MÓWIĄCEGO. '
                  'W polszczyźnie „ja” jest jedno.'),

    # ================= ETAP 2 — PYTANIE I PRZECZENIE =================
    dict(id='gram-003', stage=2, family='przeczenie', keep=True,
         select=dict(include=w('mâi'), min_syl=2),
         contrast='Polskie „nie” bywa daleko od czasownika. Tajskie `mâi` '
                  'stoi zawsze bezpośrednio przed nim — i tylko tam.'),

    dict(id='gram-035', stage=2, family='przeczenie', level='A1',
         title='mâi châi — przeczenie tożsamości',
         explanation='Rzeczownika nie przeczy się przez `mâi`, tylko przez '
                     '`mâi châi`: „to nie jest X”. `mâi` zaprzecza '
                     'czynnościom i cechom, `mâi châi` — tożsamości.',
         tip='Jeśli po przeczeniu stoi rzeczownik, potrzebujesz `mâi châi`.',
         contrast='Polskie „nie” obsługuje oba przypadki jednym słowem. '
                  'Tajski dzieli je i pomyłka jest słyszalna.',
         select=dict(include=w(r'mâi châi'), min_syl=2)),

    dict(id='gram-036', stage=2, family='przeczenie', level='A1',
         title='mâi dâai — nie zrobiłem, nie udało się',
         explanation='`mâi dâai` przed czasownikiem przeczy faktowi '
                     'dokonanemu: „nie zrobiłem tego”. To nie to samo co '
                     '`mâi` — tamto przeczy w ogóle, to przeczy wykonaniu.',
         tip='`mâi dâai pai` — nie pojechałem (choć mogłem). `mâi pai` — '
             'nie jadę, nie pojadę.',
         contrast='Polszczyzna rozróżnia to aspektem („nie jechałem” kontra '
                  '„nie pojechałem”). Tajski robi to osobnym słowem.',
         select=dict(include=w(r'mâi dâ?ai'), min_syl=3)),

    dict(id='gram-017', stage=2, family='pytanie', keep=True,
         select=dict(include=w(r'(à-rai|thîi nǎi|mûea[- ]rài|khrai|yang[- ]ngai)')),
         contrast='Tajskie słowo pytające zostaje na miejscu wyrazu, o który '
                  'pyta. Polski przesuwa je na początek zdania.'),

    dict(id='gram-037', stage=2, family='pytanie', level='A1',
         title='Pytanie o ilość: thâo-rài i kìi',
         explanation='`thâo-rài` pyta o wielkość niepoliczalną — cenę, wagę, '
                     'odległość. `kìi` pyta o liczbę i wymaga po sobie '
                     'klasyfikatora: `kìi khon`, `kìi wan`.',
         tip='Pytanie o cenę to zawsze `thâo-rài`, nigdy `kìi`.',
         contrast='Polskie „ile” obsługuje jedno i drugie. Tajski wymaga '
                  'wyboru, a po `kìi` jeszcze klasyfikatora.',
         select=dict(include=w(r'(thâo[- ]rài|kìi)'), min_syl=2)),

    dict(id='gram-004', stage=2, family='pytanie', keep=True,
         select=dict(include=w('mǎi'), min_syl=2),
         contrast='Polskie „czy” stoi na początku. Tajskie `mǎi` na końcu — '
                  'więc do ostatniej sylaby nie wiadomo, że to pytanie. '
                  'To główny powód, dla którego początkujący nie wyłapuje '
                  'pytań ze słuchu.'),

    dict(id='gram-005', stage=2, family='pytanie', keep=True,
         select=dict(include=w(r'châi mǎi')),
         contrast='Odpowiednik polskiego „prawda?” na końcu zdania — ale '
                  'obowiązkowo z `châi`, nie samo `mǎi`.'),

    dict(id='gram-026', stage=2, family='pytanie', keep=True,
         select=dict(include=w(r'r[úǔ]e yang')),
         contrast='Pytanie o to, czy coś się już wydarzyło. Odpowiedź brzmi '
                  '`láew` (już) albo `yang` (jeszcze nie) — nie „tak/nie”.'),

    dict(id='gram-038', stage=2, family='pytanie', level='A2',
         title='rǔe plào — czy tak, czy nie',
         explanation='`rǔe plào` na końcu zdania żąda rozstrzygnięcia: '
                     '„…czy nie?”. Jest ostrzejsze od `mǎi` i pyta '
                     'o fakt, nie o zgodę.',
         tip='`mǎi` zaprasza. `rǔe plào` domaga się odpowiedzi.',
         contrast='Polskie „czy nie?” brzmi neutralnie. Tajskie `rǔe plào` '
                  'wobec obcej osoby bywa odebrane jako naciskanie.',
         select=dict(include=w(r'r[úǔ]e (plào|yang)'))),

    # ================= ETAP 3 — CZAS I ASPEKT =================
    dict(id='gram-039', stage=3, family='czas', level='A1',
         title='Czas siedzi w okoliczniku, nie w czasowniku',
         explanation='`phǒm pai` znaczy „idę”, „szedłem” i „pójdę”. '
                     'Rozstrzyga wyraz czasu: `mûea waan` (wczoraj), '
                     '`tawn níi` (teraz), `phrûng-níi` (jutro). Postawiony '
                     'raz na początku wypowiedzi obowiązuje do końca.',
         tip='Słuchając, łap okolicznik czasu w pierwszych sekundach. Potem '
             'już nie wróci, a cała reszta wypowiedzi od niego zależy.',
         contrast='Polak czeka na końcówkę czasownika, która nigdy nie '
                  'przyjdzie, i gubi jedyną informację o czasie, która padła '
                  'na samym początku.',
         select=dict(include=w(r'(mûea waan|tawn níi|phrûng[- ]níi|mûea kîi|wan níi|mûea[- ]cháo)'))),

    dict(id='gram-010', stage=3, family='czas', keep=True,
         select=dict(include=w('láew'), min_syl=2),
         contrast='`láew` nie jest czasem przeszłym, tylko zmianą stanu: '
                  '„już”. Dlatego `ìm láew` to „już jestem najedzony”, '
                  'a nie „byłem najedzony”.'),

    dict(id='gram-009', stage=3, family='czas', keep=True,
         select=dict(include=w('jà'), min_syl=3),
         contrast='`jà` niesie zamiar, nie samą przyszłość. Prognoza pogody '
                  'obejdzie się bez niego, decyzja mówiącego — nie.'),

    dict(id='gram-011', stage=3, family='czas', keep=True,
         select=dict(include=w(r'yang mâi')),
         contrast='„Jeszcze nie” zakłada, że to się wydarzy. `mâi` zwykłe '
                  'tego nie zakłada. Różnica jest w oczekiwaniu, nie w czasie.'),

    dict(id='gram-040', stage=3, family='czas', level='A1',
         title='yang — jeszcze, wciąż',
         explanation='`yang` mówi, że stan trwa wbrew oczekiwaniu, że się '
                     'skończył: `yang mâi sèt` (jeszcze nie gotowe), '
                     '`yang yùu` (wciąż tu jest).',
         tip='Sama odpowiedź `yang` znaczy „jeszcze nie” i jest wypowiedzią '
             'pełną.',
         contrast='Polskie „jeszcze” bywa też wzmocnieniem („jeszcze jak”). '
                  'Tajskie `yang` jest wyłącznie aspektowe.',
         select=dict(include=w('yang'), exclude=w(r'yang[- ]ngai'), min_syl=2)),

    dict(id='gram-023', stage=3, family='czas', keep=True,
         select=dict(include=w('kamlang')),
         contrast='`kamlang` odpowiada polskiemu „właśnie”, nie samemu '
                  'aspektowi niedokonanemu. Zdanie o nawyku go nie bierze.'),

    dict(id='gram-041', stage=3, family='czas', level='A2',
         title='yùu — stan, który trwa',
         explanation='`yùu` po czasowniku mówi, że czynność albo stan trwa '
                     'w danym momencie. Razem z `kamlang` tworzy ramę '
                     '`kamlang … yùu` — najczystszy odpowiednik polskiego '
                     '„właśnie coś robię”.',
         tip='Samo `yùu` znaczy też „znajdować się”. Jeden wyraz, dwie role: '
             'czasownik i wskaźnik trwania.',
         contrast='Polak używa `yùu` wyłącznie w znaczeniu „być gdzieś” '
                  'i przez to nie rozpoznaje go w roli aspektowej.',
         select=dict(include=w('yùu'), min_syl=3)),

    dict(id='gram-024', stage=3, family='czas', keep=True,
         select=dict(include=w('khoei')),
         contrast='`khoei` to doświadczenie kiedykolwiek w życiu, nie czas '
                  'przeszły. Polskie „byłem w Tajlandii” może znaczyć jedno '
                  'i drugie; tajski to rozdziela.'),

    dict(id='gram-042', stage=3, family='czas', level='A2',
         title='dâai przed czasownikiem — udało się, faktycznie',
         explanation='`dâai` przed czasownikiem potwierdza, że czynność '
                     'doszła do skutku. Po czasowniku znaczy co innego — '
                     '„móc, dać radę”. Ta sama sylaba, dwa różne miejsca, '
                     'dwa różne znaczenia.',
         tip='`dâai pai` — udało mi się pojechać. `pai dâai` — mogę pojechać.',
         contrast='To jedna z najkosztowniejszych pomyłek pozycyjnych '
                  'w tajskim, bo obie wersje są poprawne i obie częste.',
         select=dict(include=w('dâai'), min_syl=3)),

    dict(id='gram-043', stage=3, family='czas', level='B1',
         title='phôeng — dopiero co',
         explanation='`phôeng` przed czasownikiem znaczy, że coś stało się '
                     'przed chwilą. Wskazuje na świeżość zdarzenia, nie na '
                     'jego zakończenie.',
         tip='`phôeng` i `láew` bywają w jednym zdaniu i nie kłócą się: '
             'jedno mówi „niedawno”, drugie „już”.',
         contrast='Polskie „dopiero co” brzmi potocznie i bywa pomijane. '
                  'W tajskim to normalny środek, nie kolokwializm.',
         select=dict(include=w(r'ph[ôû]eng'))),

    # ================= ETAP 4 — PROŚBA, ROZKAZ, MODALNOŚĆ =================
    dict(id='gram-016', stage=4, family='modalność', keep=True,
         select=dict(include=w(r'(yàak|tâwng)'), min_syl=3),
         contrast='Tajski nie ma trybu przypuszczającego. Uprzejmość robi '
                  'konstrukcja i partykuła, nie forma czasownika.'),

    dict(id='gram-006', stage=4, family='modalność', keep=True,
         select=dict(include=w(r'dâai mǎi')),
         contrast='`dâai` po czasowniku pyta o możliwość i o pozwolenie '
                  'jednocześnie. Polski te dwie rzeczy rozdziela.'),

    dict(id='gram-044', stage=4, family='modalność', level='A1',
         title='tâwng i mâi tâwng — pułapka przeczenia',
         explanation='`tâwng` to „musieć”. Ale `mâi tâwng` NIE znaczy „nie '
                     'wolno” — znaczy „nie trzeba, nie ma potrzeby”. '
                     'Przeczenie zdejmuje konieczność, nie nadaje zakazu.',
         tip='Zakaz to `hâam` albo `yàa`, nigdy `mâi tâwng`.',
         contrast='Polskie „nie musisz” i „nie możesz” różnią się jednym '
                  'słowem, a znaczą coś przeciwnego. W tajskim ta sama '
                  'pułapka stoi w tym samym miejscu — i Polacy wpadają w nią '
                  'dokładnie tak samo.',
         select=dict(include=w(r'tâwng'), min_syl=2)),

    dict(id='gram-045', stage=4, family='modalność', level='B1',
         title='khuan — powinno się',
         explanation='`khuan (jà)` mówi o powinności wynikającej z sensu '
                     'sytuacji, nie z przymusu. Słabsze od `tâwng`, '
                     'mocniejsze od zwykłej propozycji.',
         tip='W pytaniu `khuan … mǎi` prosi o radę: „czy powinienem…?”.',
         contrast='Polskie „powinienem” to tryb przypuszczający czasownika. '
                  'Tajskie `khuan` to osobne słowo przed czasownikiem.',
         select=dict(include=w('khuan'))),

    dict(id='gram-046', stage=4, family='modalność', level='B1',
         title='àat jà i khong jà — stopnie pewności',
         explanation='`àat jà` to „może, być może” — pewność niska. '
                     '`khong jà` to „pewnie, chyba” — pewność wysoka, ale '
                     'wciąż nie fakt. Oba stoją przed czasownikiem.',
         tip='Bez żadnego z nich zdanie jest twierdzeniem o fakcie. '
             'W rozmowie o planach to często za mocno.',
         contrast='Polszczyzna stopniuje pewność przysłówkiem („chyba”, '
                  '„pewnie”), który może stanąć gdziekolwiek. Tajskie '
                  'wskaźniki mają stałe miejsce.',
         select=dict(include=w(r'(àat|khong)'), exclude=r'sà-àat')),

    dict(id='gram-014', stage=4, family='prośba', keep=True,
         select=dict(include=w(r'kh[ǎa]w') + r'.*' + w('nòi')),
         contrast='`khǎw … nòi` to prośba o rzecz. `nòi` nie znaczy tu '
                  '„trochę” — zmiękcza żądanie.'),

    dict(id='gram-015', stage=4, family='prośba', keep=True,
         select=dict(include=w('chûai')),
         contrast='`chûai` to prośba o czynność. Bez niego zdanie jest '
                  'poleceniem, choćby miało `khráp` na końcu.'),

    dict(id='gram-047', stage=4, family='prośba', level='A2',
         title='Rozkaz to goły czasownik',
         explanation='Tryb rozkazujący nie ma w tajskim własnej formy: '
                     'zostaje sam czasownik. Cała różnica między poleceniem '
                     'a prośbą leży w tym, co do niego dołożysz — `chûai`, '
                     '`nòi`, `ná`, `khráp`.',
         tip='Goły czasownik do obcej osoby brzmi jak komenda do psa. '
             'Zawsze coś dołóż.',
         contrast='Polak, który zna słowa i nie zna partykuł, mówi samymi '
                  'rozkazami i nie wie, dlaczego rozmówcy sztywnieją.',
         select=dict(include=r'^(nâng|raw|duu|fang|maa|pai|kin|ao|dùem|phûut|yùt)' + _E,
                     min_syl=2)),

    dict(id='gram-048', stage=4, family='prośba', level='B1',
         title='yàa — zakaz',
         explanation='`yàa` przed czasownikiem tworzy zakaz: „nie rób tego”. '
                     'Sam jest dość mocny, więc w rozmowie zwykle idzie '
                     'z `ná` albo z `khráp`.',
         tip='Nie myl `yàa` (nie rób) z `yaa` (lek). Różni je ton, nie '
             'głoski.',
         contrast='Polski zakaz to „nie” plus tryb rozkazujący — czyli ta '
                  'sama partykuła co przeczenie. Tajski ma na zakaz osobne '
                  'słowo i użycie `mâi` w tej roli jest po prostu błędem.',
         select=dict(include=w('yàa'), exclude=w('yaa'))),

    dict(id='gram-049', stage=4, family='prośba', level='A2',
         title='lawng … duu — spróbuj',
         explanation='`lawng` przed czasownikiem i `duu` po nim tworzą ramę '
                     '„spróbuj, zobacz co będzie”. Najłagodniejszy sposób '
                     'zaproponowania czegokolwiek.',
         tip='`duu` nie znaczy tu „patrz” — domyka ramę i znaczy „na próbę”.',
         contrast='Polskie „spróbuj” to jeden czasownik. Tajska rama ma dwa '
                  'człony i uczący się gubi drugi.',
         select=dict(include=w('lawng'))),

    dict(id='gram-050', stage=4, family='prośba', level='A2',
         title='hâi — dla kogo, żeby, niech',
         explanation='`hâi` to „dawać”, ale przede wszystkim wskaźnik '
                     'odbiorcy i celu: `tham hâi phǒm` (zrób dla mnie), '
                     '`bàwk hâi maa` (powiedz, żeby przyszedł).',
         tip='Po `hâi` stoi osoba albo całe zdanie. Jeśli zdanie — to '
             'konstrukcja celu lub polecenia.',
         contrast='Polszczyzna rozdziela „dla” (przyimek) i „żeby” '
                  '(spójnik). Tajski obsługuje oba jednym wyrazem.',
         select=dict(include=w('hâi'), min_syl=3)),

    # ================= ETAP 5 — ROZBUDOWA FRAZY =================
    dict(id='gram-013', stage=5, family='liczenie', keep=True,
         select=dict(include=w(r'(bàat|sìp|rói|phan)')),
         contrast='Tajskie liczebniki są regularne, ale `sìp-èt` zamiast '
                  '`sìp-nùeng` (11) łamie regułę — i to jedyny wyjątek.'),

    dict(id='gram-012', stage=5, family='liczenie', keep=True,
         select=dict(include=w(r'(khon|tua|an|bai|khùat|jaan|lûuk|khan)'),
                     min_syl=3),
         contrast='Polszczyzna klasyfikatorów nie ma prawie wcale („dwie '
                  'sztuki”, „trzy pary”). W tajskim są obowiązkowe przy '
                  'każdym liczeniu i pominięcie ich słychać.'),

    dict(id='gram-051', stage=5, family='liczenie', level='A2',
         title='Liczba, klasyfikator, wskazanie',
         explanation='Pełna fraza to rzeczownik + liczba + klasyfikator, '
                     'a wskazanie („ten”, „tamten”) idzie NA KONIEC: '
                     '`nǎngsǔe sǎwng lêm níi` — te dwie książki.',
         tip='Przy liczbie „jeden” szyk się odwraca: klasyfikator staje '
             'przed liczbą albo liczba znika zupełnie.',
         contrast='Polski stawia wskazanie na początku („te dwie książki”). '
                  'Tajski na końcu — i uczący się słucha wtedy pierwszego '
                  'wyrazu zamiast ostatniego.',
         select=dict(include=w(r'(khon|tua|an|bai|khùat|jaan|khan|lêm)') + r' *(níi|nán)' + _E)),

    dict(id='gram-018', stage=5, family='fraza', keep=True,
         select=dict(include=w(r'(yài|lék|mài|kào|rórn|yen|phaeng)'), min_syl=3),
         contrast='Polski stawia przymiotnik przed rzeczownikiem. Tajski po. '
                  'Przy słuchaniu znaczy to, że najpierw wiesz O CZYM mowa, '
                  'a dopiero potem JAKIE ono jest.'),

    dict(id='gram-052', stage=5, family='fraza', level='A2',
         title='khǎwng — czyje to jest',
         explanation='`khǎwng` łączy rzecz z właścicielem w kolejności '
                     'rzecz–właściciel: `nǎngsǔe khǎwng phǒm` (moja '
                     'książka, dosłownie „książka moja”).',
         tip='Przy bliskich relacjach `khǎwng` zwykle znika: '
             '`mâe phǒm` — moja mama.',
         contrast='Polski ma zaimek dzierżawczy przed rzeczownikiem. Tajski '
                  'wyrażenie przyimkowe po nim — dokładnie odwrotnie.',
         select=dict(include=w(r'kh[ǎa]wng'), min_syl=3)),

    dict(id='gram-053', stage=5, family='fraza', level='B1',
         title='thîi — ten, który',
         explanation='`thîi` wprowadza zdanie określające rzeczownik: '
                     '`ráan thîi yùu tìt talàat` — sklep, który stoi przy '
                     'targu. To ten sam wyraz co „miejsce” i co wskaźnik '
                     'miejsca — rolę rozstrzyga pozycja.',
         tip='Po `thîi` stoi całe zdanie, nie pojedyncze słowo. Jeśli po nim '
             'idzie rzeczownik miejsca, to nie jest ta konstrukcja.',
         contrast='Polskie „który” się odmienia i tym zdradza swoją funkcję. '
                  'Tajskie `thîi` jest niezmienne, więc trzeba je rozpoznać '
                  'po tym, co za nim stoi.',
         select=dict(include=w('thîi'), min_syl=4)),

    dict(id='gram-019', stage=5, family='stopniowanie', keep=True,
         select=dict(include=w(r'(mâak|nít nòi|koen pai)')),
         contrast='Tajski nie stopniuje przymiotnika formą. Wszystkie stopnie '
                  'to osobne wyrazy dostawiane po nim.'),

    dict(id='gram-020', stage=5, family='stopniowanie', keep=True,
         select=dict(include=w(r'(kwàa|thîi sùt)')),
         contrast='`kwàa` po przymiotniku to stopień wyższy; `thîi sùt` '
                  'najwyższy. Oba stoją PO wyrazie, który stopniują.'),

    dict(id='gram-054', stage=5, family='stopniowanie', level='A2',
         title='Powtórzenie przymiotnika',
         explanation='Podwojony przymiotnik lub przysłówek zmiękcza '
                     'i uprzejmia: `cháa cháa` to nie „bardzo wolno”, tylko '
                     '„wolniutko, spokojnie”. Ton pierwszego członu bywa '
                     'przy tym podniesiony.',
         tip='Podwojenie plus `nòi` to najuprzejmiejsza prośba, jaką da się '
             'zbudować z jednego przymiotnika.',
         contrast='Polak słyszy powtórzenie jako jąkanie albo wzmocnienie. '
                  'W tajskim to osłabienie i uprzejmość.',
         select=dict(include=r'(^|[ ])(\w+) \2($|[ ])', min_syl=2)),

    dict(id='gram-021', stage=5, family='przestrzeń', keep=True,
         select=dict(include=w(r'(yùu|nai|bon|khâang)'), min_syl=3),
         contrast='Tajskie wskaźniki miejsca to rzeczowniki, nie przyimki. '
                  'Dlatego stoją w innym miejscu, niż podpowiada polski.'),

    dict(id='gram-022', stage=5, family='przestrzeń', keep=True,
         select=dict(include=w(r'(pai|maa)'), min_syl=3),
         contrast='`pai` i `maa` po czasowniku nie znaczą już „iść” '
                  'i „przyjść”, tylko kierunek: od mówiącego i do mówiącego.'),

    dict(id='gram-025', stage=5, family='liczenie', keep=True,
         select=dict(include=w('lá')),
         contrast='`lá` to „za sztukę, na jednostkę”. Bez niego cena dotyczy '
                  'całości, nie egzemplarza — a to różnica w rachunku.'),

    dict(id='gram-055', stage=5, family='fraza', level='B1',
         title='Wyrażenia z jai — serce jako gramatyka',
         explanation='`jai` (serce) tworzy dziesiątki złożeń o stanach '
                     'i reakcjach: `khâo-jai` (rozumieć), `dii-jai` '
                     '(cieszyć się), `sǐa-jai` (żałować), `jai yen` '
                     '(spokojny). To produktywny wzorzec, nie lista.',
         tip='Widząc nieznane słowo z `jai`, szukaj emocji albo postawy — '
             'trafisz w większości przypadków.',
         contrast='Polszczyzna ma „serce” w idiomach, ale nie buduje na nim '
                  'systemu. W tajskim to jeden z głównych wzorców '
                  'słowotwórczych.',
         select=dict(include=w(r'\w*[- ]?jai'), min_syl=2)),

    # ================= ETAP 6 — ŁĄCZENIE ZDAŃ =================
    dict(id='gram-056', stage=6, family='spójniki', level='A1',
         title='kàp — i, razem z',
         explanation='`kàp` łączy rzeczowniki i osoby: `phǒm kàp khun` '
                     '(ja i ty). Zdań nim się nie łączy — te stoją obok '
                     'siebie albo spina je `láew kâw`.',
         tip='Do łączenia zdań `kàp` nie służy. To najczęstsze nadużycie '
             'tego wyrazu przez uczących się.',
         contrast='Polskie „i” łączy wszystko: wyrazy, zdania, listy. Tajski '
                  'ma na to osobne środki i mieszanie ich słychać.',
         select=dict(include=w('kàp'), min_syl=3)),

    dict(id='gram-057', stage=6, family='spójniki', level='A2',
         title='tàe — ale',
         explanation='`tàe` przeciwstawia dwa zdania. Stoi na początku '
                     'drugiego, tak jak polskie „ale”.',
         tip='W mowie `tàe` bywa wydłużone i wzmocnione — sygnalizuje, że '
             'zaraz padnie zastrzeżenie. To dobry moment, żeby nastawić uszu.',
         contrast='Jeden z niewielu spójników, które działają jak w polskim. '
                  'Warto to powiedzieć wprost, bo obniża czujność w dobrym '
                  'miejscu.',
         select=dict(include=w(r't[àa]ae?'), min_syl=3)),

    dict(id='gram-058', stage=6, family='spójniki', level='A2',
         title='rǔe — albo',
         explanation='`rǔe` między dwiema możliwościami znaczy „albo”. '
                     'To ten sam wyraz, który na końcu zdania robi z niego '
                     'pytanie — a to nie przypadek: pytanie o wybór '
                     'i alternatywa to jedna konstrukcja.',
         tip='Jeśli `rǔe` stoi w środku, oferuje wybór. Jeśli na końcu — '
             'pyta.',
         contrast='Polski ma „albo” i „czy” jako dwa różne wyrazy. Tajski '
                  'jeden, więc pozycja niesie całą różnicę.',
         select=dict(include=w(r'r[úǔ]e'), exclude=w(r'r[úǔ]e (yang|plào)'),
                     min_syl=3)),

    dict(id='gram-059', stage=6, family='spójniki', level='A2',
         title='kâw — spinacz zdania',
         explanation='`kâw` to najczęstszy tajski łącznik i najtrudniejszy '
                     'do przetłumaczenia. Znaczy mniej więcej „to, więc, no '
                     'i” — sygnalizuje, że to, co idzie, wynika z tego, co '
                     'padło.',
         tip='`kâw` prawie nigdy nie tłumaczy się osobnym słowem. Jego rolą '
             'jest spójność, nie treść.',
         contrast='Polak próbuje mu przypisać stałe znaczenie i nie znajduje '
                  'żadnego. Lepiej traktować go jak znak „ciąg dalszy '
                  'wynika z poprzedniego”.',
         select=dict(include=w('kâw'), min_syl=3)),

    dict(id='gram-060', stage=6, family='warunek', level='B1',
         title='thâa … kâw — jeśli, to',
         explanation='Warunek buduje `thâa` na początku pierwszego zdania '
                     'i zwykle `kâw` na początku drugiego. Tajski nie ma '
                     'trybu przypuszczającego — warunek jest wyłącznie '
                     'w spójniku.',
         tip='O tym, czy warunek jest realny czy nierealny, decyduje '
             'kontekst i `jà`, nigdy forma czasownika.',
         contrast='Polszczyzna odmienia czasownik („gdybym miał”). Tajski nie '
                  'zmienia ani jednej sylaby, więc Polak nie słyszy warunku '
                  'i bierze zdanie za twierdzenie.',
         select=dict(include=w('thâa'), exclude=w('thâa ruea'), min_syl=3)),

    dict(id='gram-061', stage=6, family='czas w zdaniu', level='B1',
         title='kàwn, lǎng, tawn — kiedy względem czego',
         explanation='`kàwn` (przed), `lǎng (jàak)` (po), `tawn thîi` '
                     '(kiedy, w chwili) porządkują zdarzenia w czasie. '
                     'Stoją na początku członu, którego dotyczą.',
         tip='`kàwn` po czasowniku znaczy „najpierw”: `kin kàwn` — zjedz '
             'najpierw. Ta sama sylaba, inna pozycja, inna rola.',
         contrast='Polskie „zanim” wymaga określonego trybu i szyku. Tajskie '
                  '`kàwn thîi jà` jest sztywną ramą, którą trzeba rozpoznać '
                  'w całości.',
         select=dict(include=w(r'(kàwn|l[ǎa]ng|tawn)'), min_syl=3)),

    dict(id='gram-062', stage=6, family='przyczyna', level='B1',
         title='phûea i hâi — po co',
         explanation='`phûea` wprowadza cel: „po to, żeby”. `hâi` robi to '
                     'samo w rejestrze codziennym i dodatkowo wskazuje, '
                     'komu ten cel służy.',
         tip='`phûea` brzmi formalnie i pisemnie. W rozmowie usłyszysz '
             'częściej `hâi` albo dwa czasowniki pod rząd.',
         contrast='Polskie „żeby” jest jedno i neutralne. Tajski wybiera '
                  'między rejestrami, więc wybór sam niesie informację '
                  'o sytuacji.',
         select=dict(include=w('phûea'), min_syl=3)),

    dict(id='gram-063', stage=6, family='przyczyna', level='B1',
         title='phráw (wâa) — bo, ponieważ',
         explanation='`phráw wâa` wprowadza przyczynę i stoi przed nią, tak '
                     'jak polskie „ponieważ”. W mowie skraca się do samego '
                     '`phráw`, a bywa wzmocnione przez `kâw`: '
                     '`kâw phráw wâa` — „no bo przecież”.',
         tip='Przyczyna w tajskim idzie zwykle PO skutku, odwrotnie niż '
             'w polskim wykładzie. Najpierw fakt, potem dlaczego.',
         contrast='Polak buduje „ponieważ X, to Y”. Tajski woli „Y, bo X”. '
                  'Słuchając, nie czekaj na przyczynę na początku.',
         select=dict(include=w('phráw'), min_syl=2, need_space=False)),

    dict(id='gram-064', stage=6, family='przyczyna', level='B1',
         title='loei i phráw chà-nán — a więc, dlatego',
         explanation='Skutek wprowadza `loei` („no to, dlatego”) albo '
                     'formalne `phráw chà-nán`. `loei` po czasowniku znaczy '
                     'też „od razu, bez namysłu”.',
         tip='`kâw … loei` to najczęstsza para spinająca skutek w mowie '
             'potocznej.',
         contrast='Polskie „więc” jest jedno. Tajskie środki różnią się '
                  'rejestrem tak mocno, że pomyłka brzmi jak wykład '
                  'w rozmowie o obiedzie.',
         select=dict(include=w('loei'), min_syl=2)),

    dict(id='gram-065', stage=6, family='ustępstwo', level='B2',
         title='thǔeng máe wâa … kâw — chociaż',
         explanation='Rama `thǔeng máe wâa` … `kâw` odpowiada polskiemu '
                     '„chociaż …, to i tak …”. Drugi człon prawie zawsze ma '
                     '`kâw`, bo bez niego zdanie zawisa.',
         tip='Rozpoznawaj tę ramę po `kâw` w drugim członie — pierwszy człon '
             'bywa długi i łatwo zgubić jego początek.',
         contrast='Polskie „chociaż” wystarcza samo. Tajski wymaga domknięcia '
                  'i uczący się je pomija.',
         select=dict(include=w(r'm[áa]e'), min_syl=2, need_space=False)),

    dict(id='gram-066', stage=6, family='ustępstwo', level='B2',
         title='mâi wâa … kâw — obojętnie, cokolwiek',
         explanation='`mâi wâa` plus słowo pytające znaczy „obojętnie '
                     'kto/co/gdzie”: `mâi wâa à-rai` — cokolwiek. Drugi '
                     'człon domyka `kâw`.',
         tip='To ta sama rama co przy ustępstwie, tylko z pytajnikiem '
             'w środku.',
         contrast='Polszczyzna używa tu zaimków „-kolwiek”. Tajski zestawia '
                  'przeczenie ze słowem pytającym, co dla polskiego ucha '
                  'brzmi jak pytanie w środku zdania.',
         select=dict(include=w(r'mâi wâa'))),

    dict(id='gram-067', stage=6, family='ustępstwo', level='B2',
         title='yîng … yîng — im, tym',
         explanation='Powtórzone `yîng` w dwóch członach daje polskie '
                     '„im więcej …, tym …”. Konstrukcja jest sztywna: oba '
                     'człony muszą mieć `yîng`.',
         tip='`yîng khûen` samo w sobie znaczy „coraz bardziej”.',
         contrast='Polska rama „im … tym” ma dwa różne wyrazy. Tajska '
                  'powtarza jeden i przez to bywa niesłyszalna.',
         select=dict(include=w('yîng'), min_syl=2)),

    # ================= ETAP 7 — MOWA ZALEŻNA I STRONA BIERNA =================
    dict(id='gram-068', stage=7, family='mowa zależna', level='B1',
         title='wâa — łącznik zdania podrzędnego',
         explanation='`wâa` odpowiada polskiemu „że” i wprowadza całe zdanie '
                     'po czasownikach mówienia, myślenia i wiedzy. Bez niego '
                     'zdanie podrzędne się nie zaczyna.',
         tip='`wâa` to sygnał: dalej idzie CUDZA treść albo treść myśli, '
             'nie fakt.',
         contrast='Polskie „że” bywa opuszczane. Tajskie `wâa` jest '
                  'obowiązkowe i właśnie dlatego jest dobrym punktem '
                  'zaczepienia przy słuchaniu.',
         select=dict(include=w('wâa'), min_syl=3)),

    dict(id='gram-069', stage=7, family='mowa zależna', level='B1',
         title='khít wâa i rúu wâa — sądzę, że',
         explanation='`khít wâa` (myślę, że) i `rúu wâa` (wiem, że) to '
                     'najczęstsze ramy opinii. Przeczenie stawia się '
                     'w członie GŁÓWNYM: `mâi khít wâa` — nie sądzę, żeby.',
         tip='`khít wâa` zmiękcza każdą opinię i jest w tajskim niemal '
             'obowiązkowe przy niezgodzie.',
         contrast='Polak przeczy w członie podrzędnym („myślę, że nie”). '
                  'Tajski przenosi przeczenie do przodu i sens jest ten sam '
                  '— ale słyszy się go w innym miejscu zdania.',
         select=dict(include=w(r'(khít|rúu) wâa'))),

    dict(id='gram-070', stage=7, family='mowa zależna', level='B1',
         title='bàwk wâa — powiedział, że',
         explanation='`bàwk wâa` relacjonuje cudzą wypowiedź. Treść po `wâa` '
                     'zostaje BEZ ZMIAN — dokładnie taka, jaka padła.',
         tip='`bàwk hâi` to co innego: nie relacja, tylko przekazane '
             'polecenie („kazał, żeby”).',
         contrast='Polszczyzna przy mowie zależnej przestawia osobę i czas. '
                  'Tajski nie przestawia niczego, więc zdanie brzmi jak '
                  'cytat i uczący się bierze je za wypowiedź mówiącego.',
         select=dict(include=w('bàwk'), min_syl=2)),

    dict(id='gram-071', stage=7, family='mowa zależna', level='B1',
         title='thǎam wâa — pytał, czy',
         explanation='Pytanie zależne buduje `thǎam wâa` plus zdanie '
                     'pytajne w niezmienionej postaci — z `mǎi` albo ze '
                     'słowem pytającym na swoim miejscu.',
         tip='Partykuła pytajna ZOSTAJE w zdaniu zależnym. To najpewniejszy '
             'sygnał, że słuchasz pytania relacjonowanego.',
         contrast='Polski zamienia pytanie na „czy” i przestawia szyk. '
                  'Tajski zostawia pytanie takim, jakie było.',
         select=dict(include=w('thǎam'), min_syl=2)),

    dict(id="gram-072", stage=7, family="mowa zależna", level="B2",
         title='Brak następstwa czasów',
         explanation='Skoro czasownik się nie odmienia, mowa zależna nie ma '
                     'czego cofać. `kháw bàwk wâa jà maa` znaczy '
                     '„powiedział, że przyjdzie” — `jà` zostaje takie, '
                     'jakie padło w oryginale.',
         tip='Czas zdania podrzędnego liczy się względem chwili, w której '
             'PADŁA wypowiedź, nie względem teraz.',
         contrast='To jedna z rzeczy, które w tajskim są łatwiejsze niż '
                  'w polskim — pod warunkiem, że uczący się przestanie '
                  'szukać przesunięcia, którego nie ma.',
         select=dict(include=r'w[âa]a .*' + w('jà'), min_syl=4)),

    dict(id='gram-073', stage=7, family='strona bierna', level='B1',
         title='thùuk — strona bierna niepomyślna',
         explanation='`thùuk` przed czasownikiem tworzy stronę bierną '
                     'o wydźwięku negatywnym: coś złego spotkało podmiot. '
                     '`thùuk khà-mooi` — zostać okradzionym.',
         tip='`thùuk` znaczy też „tani” i „trafny”. Rolę rozstrzyga to, co '
             'stoi po nim: czasownik czy nic.',
         contrast='Polska strona bierna jest neutralna. Tajska z `thùuk` '
                  'niesie ocenę, więc użycie jej do zdarzenia miłego brzmi '
                  'sarkastycznie.',
         select=dict(include=w('thùuk'), min_syl=2)),

    dict(id='gram-074', stage=7, family='strona bierna', level='B2',
         title='Kiedy tajski obywa się bez strony biernej',
         explanation='Większość zdań, które polszczyzna oddaje stroną bierną, '
                     'tajski mówi w stronie czynnej albo bez podmiotu w ogóle. '
                     'Strona bierna z `thùuk` jest zarezerwowana dla rzeczy '
                     'przykrych, więc pozostałe przypadki muszą pójść inaczej.',
         tip='„Rachunek został zapłacony” powiesz najczęściej jako '
             '„zapłaciłem” albo bezpodmiotowo. Sięganie po `thùuk` byłoby tu '
             'błędem stylistycznym, nie gramatycznym.',
         contrast='Polak, który zna `thùuk`, zaczyna go używać wszędzie tam, '
                  'gdzie polszczyzna ma stronę bierną — i mówi zdania '
                  'poprawne gramatycznie, a niemożliwe w rozmowie.',
         select=dict(include=r'^(sèt|jàai|tham|sòng|riap-rói)' + _E,
                     min_syl=2)),

    # ================= ETAP 8 — PARTYKUŁY KOŃCOWE =================
    dict(id='gram-075', stage=8, family='partykuły', level='A2',
         title='Po co są partykuły końcowe',
         explanation='Partykuła na końcu zdania nie zmienia treści — zmienia '
                     'to, CZYM ta wypowiedź jest: prośbą, propozycją, '
                     'zapewnieniem, zniecierpliwieniem. Polszczyzna robi to '
                     'intonacją i doborem słów; tajski osobnym wyrazem.',
         tip='W tajskim intonacja jest zajęta — niesie ton leksykalny. '
             'Dlatego to, co polski robi melodią, tajski musi robić słowem.',
         contrast='To jest powód, dla którego Polak brzmi w tajskim '
                  'szorstko, mówiąc rzeczy poprawne: opuszcza całą warstwę, '
                  'której w swoim języku nie musi wypowiadać.',
         select=dict(include=w(r'(khráp|khâ|ná|nòi|dûai)') + r'$', min_syl=3)),

    dict(id='gram-076', stage=8, family='partykuły', level='A2',
         title='ná — szukanie zgody',
         explanation='`ná` zmiękcza wypowiedź i prosi rozmówcę o '
                     'przyzwolenie: „dobrze?”, „zgoda?”. Zamienia polecenie '
                     'w propozycję, a stwierdzenie w zaproszenie do '
                     'potwierdzenia.',
         tip='`ná khráp` to najbezpieczniejsze zakończenie prośby, jakie '
             'możesz mieć w zapasie.',
         contrast='Polszczyzna dokleja „dobra?” tylko w mowie potocznej. '
                  'Tajskie `ná` jest neutralne i pasuje też do rozmowy '
                  'z obcą osobą.',
         select=dict(include=w('ná'), min_syl=3)),

    dict(id='gram-077', stage=8, family='partykuły', level='Survival',
         title='nòi — zmiękczenie prośby',
         explanation='`nòi` dosłownie znaczy „trochę”, ale na końcu prośby '
                     'nie mówi o ilości. Zmniejsza CIĘŻAR prośby: '
                     '„zrób to, to drobiazg”.',
         tip='`nòi` plus `khráp` zamienia niemal każde polecenie w prośbę do '
             'przyjęcia.',
         contrast='Polak tłumaczy `nòi` jako „trochę” i nie używa go tam, '
                  'gdzie o ilość nie chodzi — czyli w większości przypadków, '
                  'w których jest potrzebne.',
         select=dict(include=w('nòi'), min_syl=2)),

    dict(id='gram-078', stage=8, family='partykuły', level='A2',
         title='dûai — też, proszę też',
         explanation='`dûai` znaczy „również” i „razem”, a w prośbie dokłada '
                     'nutę „proszę, przy okazji”. `chûai … dûai` to prośba '
                     'o pomoc w czymś dodatkowym.',
         tip='Samo `chûai dûai` to wołanie o pomoc. Kontekst decyduje, czy '
             'to uprzejmość, czy alarm.',
         contrast='Polskie „też” stoi zwykle w środku zdania. Tajskie `dûai` '
                  'na końcu, razem z innymi partykułami.',
         select=dict(include=w('dûai'), min_syl=2)),

    dict(id='gram-079', stage=8, family='partykuły', level='B1',
         title='loei jako wzmocnienie',
         explanation='Na końcu wypowiedzi `loei` wzmacnia: „w ogóle”, '
                     '„zupełnie”, „od razu”. `mâi châwp loei` — wcale mi się '
                     'nie podoba.',
         tip='Ten sam wyraz spina skutek w środku zdania. Na końcu wzmacnia. '
             'Pozycja rozstrzyga.',
         contrast='Polak zna `loei` jako „więc” i nie rozpoznaje go '
                  'w funkcji wzmacniającej, przez co słyszy zdanie słabsze, '
                  'niż jest.',
         select=dict(include=w('loei') + r'|loei$', min_syl=2)),

    dict(id='gram-080', stage=8, family='partykuły', level='B2',
         title='sì — nacisk i zachęta',
         explanation='`sì` popycha rozmówcę do działania: „no dawaj”, '
                     '„śmiało”. Wobec kogoś bliskiego brzmi serdecznie, '
                     'wobec obcego — jak popędzanie.',
         tip='`sì` z `khráp` łagodnieje, ale nie znika. Do urzędnika lepiej '
             'go nie używać.',
         contrast='Polszczyzna robi to trybem rozkazującym plus „no”. '
                  'W tajskim tryb rozkazujący jest goły, więc cały nacisk '
                  'niesie właśnie ta partykuła.',
         select=dict(include=w(r's[íì]'), min_syl=2)),

    dict(id='gram-081', stage=8, family='partykuły', level='B2',
         title='lâ i là — domaganie się',
         explanation='`lâ` po słowie pytającym domaga się odpowiedzi: '
                     '`à-rai lâ` — „no co?”. Sygnalizuje, że rozmówca '
                     'czegoś oczekiwał i tego nie dostał.',
         tip='Ta partykuła niesie emocję. Użyta wobec obcej osoby brzmi '
             'niecierpliwie i tak zostanie odebrana.',
         contrast='Polskie „no” przed pytaniem robi to samo, ale jest '
                  'wyraźnie potoczne. Tajskie `lâ` bywa neutralne w gronie '
                  'znajomych.',
         select=dict(include=w(r'l[âà]'), min_syl=2)),

    dict(id='gram-082', stage=8, family='partykuły', level='B2',
         title='ròk i ngai — sprostowanie i oczywistość',
         explanation='`ròk` prostuje cudze założenie: „ależ nie, przecież”. '
                     '`ngai` mówi, że rzecz jest oczywista: „no przecież”. '
                     'Obie zakładają, że rozmówca coś źle przyjął.',
         tip='`mâi … ròk` to najuprzejmiejszy sposób zaprzeczenia komuś '
             'w tajskim.',
         contrast='Polszczyzna sprostowanie robi intonacją i „przecież”. '
                  'W tajskim intonacja jest zajęta przez tony, więc rolę '
                  'przejmuje partykuła.',
         select=dict(include=w(r'(ròk|ngai)'), exclude=w(r'yang[- ]ngai'),
                     min_syl=2)),

    dict(id='gram-083', stage=8, family='partykuły', level='Survival',
         title='Kiedy brak partykuły jest niegrzeczny',
         explanation='Wypowiedź bez `khráp`/`khâ` do obcej osoby, do kogoś '
                     'starszego albo w każdej sytuacji usługowej brzmi '
                     'szorstko — nawet jeśli treść jest uprzejma. Brak '
                     'partykuły jest w tajskim informacją, nie jej brakiem.',
         tip='Zasada praktyczna: partykuła należy się każdemu, kogo nie '
             'znasz, i każdemu, kto cię obsługuje. Nadmiar nikogo nie razi.',
         contrast='Polak wychodzi z założenia, że skoro nie powiedział nic '
                  'niegrzecznego, jest w porządku. W tajskim milczenie '
                  'w tym miejscu SAMO jest wypowiedzią.',
         select=dict(include=w('khráp') + r'$', min_syl=3)),

    dict(id='gram-084', stage=8, family='partykuły', level='B1',
         title='Łączenie partykuł',
         explanation='Partykuły ustawiają się w stałej kolejności: najpierw '
                     'te, które modyfikują treść (`nòi`, `dûai`, `ná`), '
                     'a grzecznościowa `khráp`/`khâ` zawsze na samym końcu.',
         tip='`… nòi ná khráp` to najbardziej miękka prośba, jaką da się '
             'zbudować. Kolejności nie da się zamienić.',
         contrast='Polszczyzna nie piętrzy takich cząstek, więc uczący się '
                  'nie ma nawyku ich układania — a kolejność jest tu sztywna '
                  'jak szyk zdania.',
         select=dict(include=w(r'(nòi|dûai|ná)') + r' *khráp' + r'$', min_syl=3)),
]
