/* Thai All-in-One — słuchanie ekstensywne.

   Trzy do pięciu minut ciągłego materiału, trzy przejścia:

     1. bez tekstu          — ile wyłapiesz z samego słuchu
     2. z tekstem           — to samo nagranie, zapis przed oczami
     3. znów bez tekstu     — ile z tego zostało, gdy tekst znika

   Po każdym przejściu pytania, za każdym razem bardziej szczegółowe.

   Pomiar jest w różnicy między przejściem pierwszym a trzecim. To ona mówi,
   czego uczący się nie usłyszał, a nie: czego nie wiedział. Jeśli po tekście
   wynik skacze, słowa są znane, a zawodzi rozpoznanie ich w mowie — wtedy
   pomaga Moduł 0 i wolniejsze tempo. Jeśli wynik nie drgnie, brakuje samego
   słownictwa i tekst niczego nie odblokował.

   Blok trwa tyle, ile trwa: nie da się go przewinąć ani zatrzymać w połowie
   i zapytać o szczegół. O to chodzi — słuchanie ekstensywne polega na
   wytrzymaniu dłuższego kawałka bez zatrzymywania się na każdym słowie. */
(function (global) {
  'use strict';

  var Extensive = {
    block: null,
    state: null      // { pass, results: [], playedPass }
  };

  Extensive.ready = function () { return !!(DB.blocks && DB.blocks.length); };
  Extensive.ensureData = function () { return DB.ensureScenes(); };

  Extensive.list = function (level) {
    var all = DB.blocks || [];
    if (!level) return all.slice();
    var picked = all.filter(function (b) { return b.level === level; });
    return picked.length ? picked : all.slice();
  };

  Extensive.suggest = function (level) {
    var pool = Extensive.list(level);
    var fresh = pool.filter(function (b) { return !Progress.extensiveOf(b.id); });
    var from = fresh.length ? fresh : pool;
    return from.length ? from[0] : null;
  };

  function minutes(block) {
    var sec = block.estSeconds[CompTempo.current] || block.estSeconds.natural;
    var m = Math.floor(sec / 60), s = Math.round(sec % 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
  }

  function questionsFor(block, pass) {
    var def = (block.passes || []).filter(function (p) { return p.pass === pass; })[0];
    if (!def) return [];
    return (def.questionIds || []).map(DB.sceneQuestion).filter(Boolean);
  }

  function passDef(block, pass) {
    return (block.passes || []).filter(function (p) { return p.pass === pass; })[0] || {};
  }

  Extensive.reset = function () {
    Extensive.state = { pass: 1, results: [], played: {} };
  };

  /* ------------------------------------------------------------- render */

  Extensive.render = function (root) {
    U.clear(root);
    if (!Extensive.ready()) {
      root.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję bloki…' }));
      return;
    }
    var block = Extensive.block || Extensive.suggest(
      App.settings.practiceLevel || Progress.entryLevel());
    if (!block) {
      root.appendChild(U.el('p', { class: 'muted', text: 'Brak bloków do odsłuchu.' }));
      return;
    }
    Extensive.block = block;
    if (!Extensive.state) Extensive.reset();

    /* --- nagłówek bloku --- */
    var head = U.el('div', { class: 'card' });
    head.appendChild(U.el('h2', { text: block.title }));
    var scenes = DB.blockScenes(block);
    head.appendChild(U.el('p', { class: 'muted', text:
      block.level + ' · ' + minutes(block) + ' ciągłego materiału · '
      + block.lineCount + ' ' + U.plural(block.lineCount, 'kwestia', 'kwestie', 'kwestii')
      + ' · ' + scenes.length + ' ' + U.plural(scenes.length, 'scena', 'sceny', 'scen') }));
    if (block.mixed) {
      head.appendChild(U.el('p', { class: 'muted', text:
        'Blok przeglądowy — temat zmienia się w trakcie. Nie zdziw się, gdy '
        + 'po restauracji zacznie się rozmowa o czym innym.' }));
    }
    var arc = U.el('ol', { class: 'block-arc' });
    scenes.forEach(function (s) {
      arc.appendChild(U.el('li', { text: s.title }));
    });
    head.appendChild(arc);

    var swap = U.el('button', { class: 'btn ghost', type: 'button', text: 'Inny blok' });
    swap.addEventListener('click', function () { openPicker(root); });
    head.appendChild(U.el('div', { class: 'btn-row' }, [swap]));
    root.appendChild(head);

    /* --- tempo --- */
    var tempoCard = U.el('div', { class: 'card' });
    tempoCard.appendChild(CompTempo.row('extensive', function () {
      Extensive.render(root);
    }));
    root.appendChild(tempoCard);

    /* --- przejścia --- */
    var st = Extensive.state;
    [1, 2, 3].forEach(function (pass) {
      var def = passDef(block, pass);
      var card = U.el('div', { class: 'card pass-card'
        + (st.pass === pass ? ' current' : '') + (st.pass > pass ? ' done' : '') });
      card.appendChild(U.el('h2', { text:
        'Przejście ' + pass + ' — ' + (def.label || '') }));
      card.appendChild(U.el('p', { class: 'muted', text: def.hint || '' }));

      if (st.pass < pass) {
        card.appendChild(U.el('p', { class: 'muted', text:
          'Odblokuje się po zakończeniu poprzedniego przejścia.' }));
        root.appendChild(card);
        return;
      }
      if (st.pass > pass) {
        var r = st.results[pass - 1];
        card.appendChild(U.el('p', { class: 'fb ok', text:
          'Zrobione: ' + r.correct + ' z ' + r.total + ' odpowiedzi trafnych.' }));
        root.appendChild(card);
        return;
      }

      renderPass(card, root, block, pass);
      root.appendChild(card);
    });

    if (st.pass > 3) renderSummary(root, block);
  };

  function renderPass(card, root, block, pass) {
    var st = Extensive.state;
    var lines = DB.blockLines(block);
    var showText = pass === 2;

    var transcript = U.el('div', { class: 'scene-lines' });
    var play = U.el('button', { class: 'btn gold play-btn', type: 'button',
      'aria-pressed': 'false' });
    play.appendChild(U.icon('play'));
    play.appendChild(U.el('span', { text: 'Odtwórz blok (' + minutes(block) + ')' }));

    var qArea = U.el('div');
    var startQ = U.el('button', { class: 'btn', type: 'button',
      text: 'Przejdź do pytań', disabled: 'disabled' });

    play.addEventListener('click', function () {
      Scenes.play(lines, {
        btn: play,
        onstep: function (line) {
          if (!showText) return;
          U.$$('.scene-line', transcript).forEach(function (n) {
            n.classList.remove('current');
          });
          var node = U.$('[data-key="' + line.__key + '"]', transcript);
          if (node) {
            node.classList.add('current');
            if (node.scrollIntoView) {
              node.scrollIntoView({ block: 'nearest' });
            }
          }
        },
        onend: function () {
          U.$$('.scene-line', transcript).forEach(function (n) {
            n.classList.remove('current');
          });
          st.played[pass] = true;
          startQ.disabled = false;
          startQ.focus();
        }
      });
      /* Przejście do pytań odblokowuje się także wtedy, gdy uczący się
         zatrzyma odtwarzanie — blokada ma przypominać o kolejności,
         a nie więzić na ekranie. */
      st.played[pass] = true;
      startQ.disabled = false;
    });
    if (st.played[pass]) startQ.disabled = false;

    card.appendChild(U.el('div', { class: 'btn-row' }, [play]));

    if (showText) {
      var beatKey = null;
      lines.forEach(function (line) {
        var key = line.__dialogueId;
        if (key !== beatKey) {
          beatKey = key;
          var dlg = DB.get(key);
          if (dlg) {
            transcript.appendChild(U.el('p', { class: 'scene-beat', text: dlg.title }));
          }
        }
        var view = G.view(line);
        var row = U.el('div', { class: 'scene-line', 'data-key': line.__key });
        row.appendChild(U.el('span', { class: 'role' + (line.role === 'B' ? ' b' : ''),
          text: line.role }));
        var mid = U.el('div');
        mid.appendChild(U.el('div', { class: 'l-ph', text: App.settings.hideTones
          ? U.stripTones(view.thaiPhonetic) : view.thaiPhonetic }));
        mid.appendChild(U.el('div', { class: 'l-pl', text: view.polish }));
        row.appendChild(mid);
        transcript.appendChild(row);
      });
      card.appendChild(transcript);
    } else {
      card.appendChild(U.el('p', { class: 'muted', text:
        'Bez zapisu. Nieznane słowa przepuść — wracaj do wątku, zamiast '
        + 'zatrzymywać się na każdym z nich.' }));
    }

    card.appendChild(U.el('div', { class: 'btn-row' }, [startQ]));
    card.appendChild(qArea);

    startQ.addEventListener('click', function () {
      startQ.hidden = true;
      play.disabled = true;
      var qs = questionsFor(block, pass);
      if (!qs.length) {
        qArea.appendChild(U.el('p', { class: 'muted', text:
          'Ten blok nie ma pytań na tym przejściu.' }));
        return;
      }
      Scenes.runQuestions(qArea, qs, {
        onAnswer: function (ok) {
          Progress.answer('block:' + block.id, ok, { mode: 'extensive' });
          Progress.tempoAnswer('extensive', CompTempo.current, ok);
        },
        onDone: function (result) {
          Extensive.state.results[pass - 1] = result;
          Extensive.state.pass = pass + 1;
          if (pass === 3) {
            Progress.extensiveResult(block.id, {
              tempo: CompTempo.current,
              first: Extensive.state.results[0],
              second: Extensive.state.results[1],
              third: Extensive.state.results[2]
            });
          }
          Extensive.render(root);
        }
      });
    });
  }

  /* Podsumowanie — sedno trybu. Pokazujemy nie tylko wynik, ale i to, co
     z niego wynika dla dalszej nauki. */
  function renderSummary(root, block) {
    var st = Extensive.state;
    var first = st.results[0] || { correct: 0, total: 0 };
    var third = st.results[2] || { correct: 0, total: 0 };
    var card = U.el('div', { class: 'card' });
    card.appendChild(U.el('h2', { text: 'Ile zrozumiałeś od razu, a ile po tekście' }));

    var row = U.el('div', { class: 'stat-row' });
    [['Bez tekstu', first], ['Z tekstem', st.results[1] || { correct: 0, total: 0 }],
     ['Znów bez tekstu', third]].forEach(function (pair) {
      var box = U.el('div', { class: 'stat' });
      box.appendChild(U.el('div', { class: 'stat-num',
        text: pair[1].correct + '/' + pair[1].total }));
      box.appendChild(U.el('div', { class: 'stat-label', text: pair[0] }));
      row.appendChild(box);
    });
    card.appendChild(row);

    var fs = first.total ? first.correct / first.total : 0;
    var ts = third.total ? third.correct / third.total : 0;
    var verdict;
    if (fs >= 0.75) {
      verdict = 'Wyłapałeś sens od pierwszego przejścia. Ten blok jest dla '
        + 'Ciebie za łatwy — weź tempo ' + (CompTempo.current === 'fast'
        ? '1,4x z hałasem tła' : 'o stopień szybsze') + ' albo blok z wyższego poziomu.';
    } else if (ts - fs >= 0.25) {
      verdict = 'Po zobaczeniu zapisu wynik wyraźnie skoczył. To znaczy, że '
        + 'słowa znasz, ale nie rozpoznajesz ich w mowie. Pomoże Moduł 0 '
        + 'i ten sam blok w tempie 0,7x — nie dokładanie nowego słownictwa.';
    } else if (ts <= fs + 0.05 && fs < 0.5) {
      verdict = 'Tekst niewiele zmienił, a wynik jest niski. Tu brakuje samego '
        + 'słownictwa — wróć do kursu i powtórek, zanim weźmiesz następny blok.';
    } else {
      verdict = 'Wynik rośnie po tekście, ale bez skoku. Powtórz ten blok za '
        + 'kilka dni w tym samym tempie i porównaj pierwsze przejście.';
    }
    card.appendChild(U.el('p', { text: verdict }));
    card.appendChild(U.el('p', { class: 'muted', text:
      'Tempo tego podejścia: ' + Progress.tempoLabel(CompTempo.current)
      + '. Wynik liczy się tylko do tego tempa.' }));

    var again = U.el('button', { class: 'btn', type: 'button', text: 'Ten sam blok od nowa' });
    again.addEventListener('click', function () {
      Extensive.reset();
      Extensive.render(root);
    });
    var next = U.el('button', { class: 'btn ghost', type: 'button', text: 'Następny blok' });
    next.addEventListener('click', function () {
      Extensive.block = null;
      Extensive.reset();
      Extensive.render(root);
    });
    card.appendChild(U.el('div', { class: 'btn-row' }, [again, next]));
    root.appendChild(card);
  }

  function openPicker(root) {
    var body = U.el('div');
    body.appendChild(U.el('h2', { id: 'sheet-title', text: 'Wybierz blok' }));
    var list = U.el('div', { class: 'list' });
    Extensive.list('').forEach(function (b) {
      var done = Progress.extensiveOf(b.id);
      var row = U.el('button', { class: 'row', type: 'button' });
      row.appendChild(U.el('div', { class: 'row-main' }, [
        U.el('div', { class: 'row-pl', text: b.title }),
        U.el('div', { class: 'row-meta', text: b.level + ' · ' + b.estMinutes
          + ' min · ' + b.lineCount + ' kwestii'
          + (done ? ' · przerobiony' : '') })
      ]));
      row.addEventListener('click', function () {
        App.closeSheet();
        Extensive.block = b;
        Extensive.reset();
        Extensive.render(root);
      });
      list.appendChild(row);
    });
    body.appendChild(list);
    App.openSheet(body);
  }

  global.Extensive = Extensive;
})(window);
