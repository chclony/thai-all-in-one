/* Thai All-in-One — ekran egzaminu poziomowego, diagnoza i certyfikat.

   Ekran prowadzi przez cztery sekcje po kolei i pilnuje warunków
   egzaminacyjnych: brak podpowiedzi, najwyżej jeden powtórny odsłuch, limit
   czasu liczony osobno na każdą sekcję. Uzasadnienia odpowiedzi (`explain`)
   pokazujemy dopiero w diagnozie — w trakcie egzaminu byłyby ściągą do
   następnych pytań tej samej sceny.

   Certyfikat powstaje jako osobna strona do wydruku (i do zapisania jako PDF
   przez okno drukowania przeglądarki). Jest po polsku, w UTF-8, z fontami
   systemowymi obsługującymi polskie znaki diakrytyczne — dlatego nie ma tu
   żadnej biblioteki PDF: każda wymagałaby osadzenia własnego fontu, a strona
   do wydruku korzysta z tego, co system już ma, i nie gubi „ą”, „ś” ani „ż”. */
(function (global) {
  'use strict';

  var ExamView = {};

  function th() { return Exam.thresholds(); }
  function hideTones() { return !!U.store.get('settings', {}).hideTones; }

  function fmtTime(sec) {
    var m = Math.floor(sec / 60), s = sec % 60;
    return m + ':' + (s < 10 ? '0' : '') + s;
  }

  function pctText(value) {
    return (Math.round(value * 10) / 10).toString().replace('.', ',') + '%';
  }

  /* ---------------------------------------------------------------- start */

  ExamView.render = function (root) {
    U.clear(root);
    if (!Exam.ready()) {
      root.appendChild(U.el('p', { class: 'muted', text: 'Wczytuję zestawy egzaminacyjne…' }));
      return;
    }
    if (Exam.active()) { renderRun(root); return; }
    if (ExamView.showing === 'result' && Exam.lastAttempt) {
      renderResult(root, Exam.lastAttempt);
      return;
    }
    renderHub(root);
  };

  function renderHub(root) {
    var intro = U.el('div', { class: 'card' });
    intro.appendChild(U.el('h2', { text: 'Egzamin na koniec poziomu' }));
    intro.appendChild(U.el('p', {
      text: 'Test poziomujący sprawdza, od czego zacząć. Egzamin sprawdza, czy poziom '
        + 'naprawdę został osiągnięty. Mierzy cztery sprawności osobno, każda ma własny '
        + 'próg, a poziom jest zaliczony dopiero wtedy, gdy wszystkie cztery ten próg '
        + 'przekroczą. Nie liczymy średniej — wysoki wynik ze słuchu nie zastępuje '
        + 'umiejętności odpowiadania.'
    }));
    var list = U.el('ul', { class: 'plain-list' });
    Exam.ORDER.forEach(function (id) {
      var m = Exam.sectionMeta(id);
      var li = U.el('li');
      li.appendChild(U.el('strong', { text: m.label + ': ' }));
      li.appendChild(document.createTextNode(m.how));
      list.appendChild(li);
    });
    intro.appendChild(list);
    intro.appendChild(U.el('p', {
      class: 'muted',
      text: 'Warunki: bez podpowiedzi, każdy materiał najwyżej dwa razy (pierwszy odsłuch '
        + 'i jedno powtórzenie), limit czasu osobno na każdą sekcję. Wyjście z egzaminu '
        + 'w trakcie kończy podejście.'
    }));
    root.appendChild(intro);

    Exam.LEVELS.forEach(function (level) {
      root.appendChild(levelCard(level));
    });

    var cert = U.el('div', { class: 'card' });
    cert.appendChild(U.el('h2', { text: 'Certyfikat postępu' }));
    var certified = Progress.certifiedLevel();
    cert.appendChild(U.el('p', {
      text: certified
        ? ('Zdany najwyższy poziom: ' + certified + '. Certyfikat opisuje, co z tego wynika '
           + 'w praktyce — i czego nie obejmuje.')
        : ('Żaden poziom nie jest jeszcze zdany. Certyfikat i tak można pobrać: opisze '
           + 'wtedy uczciwie, ile materiału masz za sobą i że sprawności nie zostały '
           + 'jeszcze zmierzone egzaminem.')
    }));
    var certBtn = U.el('button', { class: 'btn', type: 'button', text: 'Otwórz certyfikat do wydruku' });
    certBtn.addEventListener('click', function () { ExamView.openCertificate(); });
    var dlBtn = U.el('button', { class: 'btn ghost', type: 'button', text: 'Pobierz jako plik HTML' });
    dlBtn.addEventListener('click', function () { ExamView.downloadCertificate(); });
    cert.appendChild(U.el('div', { class: 'btn-row' }, [certBtn, dlBtn]));
    root.appendChild(cert);
  }

  function levelCard(level) {
    var card = U.el('div', { class: 'card' });
    var box = Progress.examBox(level);
    var passed = Progress.examPassed(level);
    var ready = Exam.readiness(level);
    var el = Exam.eligibility(level);

    var head = U.el('h3');
    head.appendChild(document.createTextNode('Poziom ' + level + ' '));
    head.appendChild(U.el('span', {
      class: 'badge',
      text: passed ? 'zdany' : (box.attempts.length ? 'niezdany' : 'niepodchodzony')
    }));
    card.appendChild(head);

    card.appendChild(U.el('p', {
      class: 'muted',
      text: 'Lekcje tego poziomu: ' + ready.done + ' z ' + ready.total
        + ' (' + ready.share + '%). Zadań w egzaminie: '
        + (Exam.forLevel(level)[0] || {}).taskCount + ', limit czasu '
        + Math.round(((Exam.forLevel(level)[0] || {}).timeLimitSec || 0) / 60) + ' minut.'
    }));

    if (ready.share < 80 && !passed) {
      card.appendChild(U.el('p', {
        class: 'fb warn',
        text: 'Materiał poziomu nie jest jeszcze przerobiony. Możesz podejść, ale egzamin '
          + 'z lekcji, których się nie widziało, zużyje jeden z trzech zestawów i niewiele powie.'
      }));
    }

    var last = box.attempts[box.attempts.length - 1];
    if (last) {
      card.appendChild(attemptLine(last));
    }

    var row = U.el('div', { class: 'btn-row' });
    if (el.allowed) {
      var go = U.el('button', {
        class: 'btn', type: 'button',
        text: (last ? 'Podejdź ponownie — ' : 'Rozpocznij egzamin — ')
          + (el.variant ? el.variant.variantLabel : '')
      });
      go.addEventListener('click', function () { startExam(level); });
      row.appendChild(go);
    } else {
      var parts = [];
      if (el.waitDays > 0) {
        parts.push(el.waitDays + ' ' + U.plural(el.waitDays, 'dzień', 'dni', 'dni'));
      }
      if (el.waitLessons > 0) {
        parts.push(el.waitLessons + ' ' + U.plural(el.waitLessons, 'lekcja', 'lekcje', 'lekcji'));
      }
      card.appendChild(U.el('p', {
        class: 'fb warn',
        text: 'Powtórne podejście jeszcze nie teraz. Brakuje: ' + parts.join(' i ')
          + '. Egzamin powtarza się po nauce, nie od razu — inaczej mierzyłby pamięć '
          + 'do zestawu, a nie znajomość języka.'
      }));
    }
    var best = Progress.bestExam(level);
    if (best) {
      var see = U.el('button', { class: 'btn ghost', type: 'button', text: 'Zobacz diagnozę' });
      see.addEventListener('click', function () {
        ExamView.showing = 'result';
        Exam.lastAttempt = best;
        RENDERROOT(function (r) { renderResult(r, best); });
      });
      row.appendChild(see);
    }
    card.appendChild(row);
    return card;
  }

  function RENDERROOT(fn) {
    var root = U.$('#exam-area');
    if (!root) return;
    U.clear(root);
    fn(root);
  }

  function attemptLine(a) {
    if (a.abandoned) {
      return U.el('p', {
        class: 'muted',
        text: 'Ostatnie podejście (' + U.dateWords(a.date) + '): przerwane w sekcji „'
          + Exam.sectionMeta(a.reachedSection).label + '”. Przerwane podejście liczy się do karencji.'
      });
    }
    var bits = Exam.ORDER.map(function (id) {
      var s = a.sections[id];
      var value = id === 'speaking'
        ? (Math.round(s.tone) + ' pkt / ' + pctText(s.content))
        : pctText(s.pct);
      return Exam.sectionMeta(id).short + ' ' + value + (s.passed ? ' ✓' : ' ✗');
    });
    return U.el('p', {
      class: 'muted',
      text: 'Ostatnie podejście (' + U.dateWords(a.date) + ', ' + a.variant + '): '
        + bits.join(' · ') + '.'
    });
  }

  function startExam(level) {
    var state = Exam.start(level);
    if (!state) { U.toast('Brak zestawu egzaminacyjnego dla tego poziomu.'); return; }
    ExamView.showing = null;
    var root = U.$('#exam-area');
    U.clear(root).appendChild(U.el('p', { class: 'muted', text: 'Przygotowuję zestaw…' }));
    DB.ensureExamRecords(state.exam).then(function () {
      if (!Exam.active()) return;
      RENDERROOT(function (r) { renderRun(r); });
    });
  }

  /* -------------------------------------------------------------- przebieg */

  var timer = null;

  function stopTimer() {
    if (timer) { clearInterval(timer); timer = null; }
  }

  function renderRun(root) {
    stopTimer();
    var s = Exam.state;
    var box = s.sections[s.section];
    if (!box.startedAt) { renderSectionIntro(root); return; }
    renderTask(root);
  }

  function header(root, extra) {
    var s = Exam.state;
    var m = Exam.sectionMeta(s.section);
    var head = U.el('div', { class: 'card exam-head' });
    head.appendChild(U.el('p', {
      class: 'muted',
      text: 'Egzamin ' + s.level + ' · ' + s.exam.variantLabel + ' · sekcja '
        + (s.sectionAt + 1) + ' z 4'
    }));
    head.appendChild(U.el('h2', { text: m.label }));
    if (extra) head.appendChild(extra);
    root.appendChild(head);
    return head;
  }

  function renderSectionIntro(root) {
    var s = Exam.state;
    var m = Exam.sectionMeta(s.section);
    header(root);
    var card = U.el('div', { class: 'card' });
    card.appendChild(U.el('p', { text: m.how }));
    var tasks = Exam.tasks();
    var limit = s.exam.sections[s.section].timeLimitSec;
    card.appendChild(U.el('p', {
      class: 'muted',
      text: 'Zadań: ' + tasks.length + '. Czas na tę sekcję: ' + Math.round(limit / 60)
        + ' minut. Czas rusza po naciśnięciu przycisku i nie zatrzymuje się.'
    }));
    var thresholdText = s.section === 'speaking'
      ? ('Próg: wymowa ' + th().speakingTone + ' punktów i treść ' + th().speakingContent + '%.')
      : ('Próg: ' + th()[s.section] + '%.');
    card.appendChild(U.el('p', { class: 'muted', text: thresholdText }));

    var go = U.el('button', { class: 'btn', type: 'button', text: 'Zaczynam' });
    go.addEventListener('click', function () {
      Exam.beginSection();
      RENDERROOT(renderTask);
    });
    var quit = U.el('button', { class: 'btn ghost', type: 'button', text: 'Przerwij egzamin' });
    quit.addEventListener('click', confirmQuit);
    card.appendChild(U.el('div', { class: 'btn-row' }, [go, quit]));
    root.appendChild(card);
  }

  function confirmQuit() {
    var wrap = U.el('div');
    wrap.appendChild(U.el('h2', { text: 'Przerwać egzamin?' }));
    wrap.appendChild(U.el('p', {
      text: 'Przerwane podejście zostanie zapisane jako niezaliczone i policzy się do '
        + 'karencji przed następnym. Zestaw, który właśnie widzisz, wróci dopiero po '
        + 'dwóch pozostałych.'
    }));
    var yes = U.el('button', { class: 'btn', type: 'button', text: 'Tak, przerywam' });
    yes.addEventListener('click', function () {
      stopTimer();
      Exam.abandon();
      App.closeSheet();
      RENDERROOT(renderHub);
    });
    var no = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wracam do egzaminu' });
    no.addEventListener('click', function () { App.closeSheet(); });
    wrap.appendChild(U.el('div', { class: 'btn-row' }, [yes, no]));
    App.openSheet(wrap);
  }

  /* Zegar sekcji. Odliczanie jest widoczne, bo ukryty limit czasu jest
     nieuczciwy — uczący się ma prawo wiedzieć, ile mu zostało, i rozłożyć
     siły. Ostatnia minuta zmienia kolor, ale nie miga: migotanie na ekranie
     w trakcie zadania na słuch szkodzi bardziej niż pomaga. */
  function clock(root) {
    var node = U.el('p', { class: 'exam-clock', role: 'timer', 'aria-live': 'off' });
    root.appendChild(node);
    function tick() {
      var left = Exam.secondsLeft();
      node.textContent = 'Pozostały czas sekcji: ' + fmtTime(left);
      node.classList.toggle('low', left <= 60);
      if (left <= 0) {
        stopTimer();
        Exam.closeSection(true);
        U.toast('Czas tej sekcji minął.');
        afterSection();
      }
    }
    tick();
    stopTimer();
    timer = setInterval(tick, 1000);
    return node;
  }

  function afterSection() {
    stopTimer();
    var next = Exam.nextSection();
    if (!next) {
      var attempt = Exam.finish();
      Exam.pushToSRS(attempt);
      ExamView.showing = 'result';
      RENDERROOT(function (r) { renderResult(r, attempt); });
      return;
    }
    RENDERROOT(renderSectionIntro);
  }

  function renderTask(root) {
    var s = Exam.state;
    var tasks = Exam.tasks();
    if (s.at >= tasks.length) {
      Exam.closeSection(false);
      afterSection();
      return;
    }
    var head = header(root);
    clock(head);
    head.appendChild(U.el('p', {
      class: 'muted', text: 'Zadanie ' + (s.at + 1) + ' z ' + tasks.length
    }));

    var card = U.el('div', { class: 'card' });
    root.appendChild(card);
    var task = tasks[s.at];

    if (s.section === 'listening') renderListening(card, task);
    else if (s.section === 'detail') renderDetail(card, task);
    else if (s.section === 'speaking') renderSpeaking(card, task);
    else renderWriting(card, task);
  }

  /* --- 1. rozumienie ze słuchu ------------------------------------------ */

  function sceneOf(id) { return DB.sceneById.get(id) || null; }

  function playScene(scene, btn, onend) {
    var lines = DB.sceneLines(scene);
    if (!lines.length) { U.toast('Nie udało się wczytać sceny.'); return; }
    Scenes.play(lines, { btn: btn, tempo: 'natural', onend: onend });
  }

  function listeningSource(box, sceneId, label) {
    var scene = sceneOf(sceneId);
    if (!scene) {
      box.appendChild(U.el('p', { class: 'fb bad', text: 'Nie udało się wczytać sceny.' }));
      return;
    }
    var info = U.el('p', { class: 'muted' });
    var play = U.el('button', { class: 'btn gold', type: 'button', text: label || 'Odtwórz scenę' });
    function refresh() {
      var left = Exam.playsLeft(sceneId);
      info.textContent = 'Tempo naturalne, bez tekstu. Pozostałe odtworzenia: ' + left
        + ' z ' + Exam.MAX_PLAYS + '.';
      play.disabled = left <= 0;
    }
    play.addEventListener('click', function () {
      if (!Exam.canPlay(sceneId)) return;
      Exam.notePlay(sceneId);
      refresh();
      playScene(scene, play);
    });
    refresh();
    box.appendChild(U.el('div', { class: 'btn-row' }, [play]));
    box.appendChild(info);
  }

  function renderListening(box, q) {
    listeningSource(box, q.sceneId);
    box.appendChild(U.el('hr'));
    question(box, q);
  }

  /* --- 2. rozumienie szczegółowe ---------------------------------------- */

  function renderDetail(box, q) {
    box.appendChild(U.el('p', {
      class: 'muted',
      text: 'Pytanie o scenę, której już słuchałeś. Bez ponownego odsłuchu i bez zapisu.'
    }));
    question(box, q);
  }

  /* Wspólny renderer pytania zamkniętego. Świadomie NIE pokazuje, czy
     odpowiedź była trafna: informacja zwrotna po każdym pytaniu zmieniłaby
     egzamin w ćwiczenie, a w scenie z kilkoma pytaniami podpowiadałaby
     następne. Wszystko wraca w diagnozie. */
  function question(box, q) {
    box.appendChild(U.el('p', { class: 'q-prompt', text: q.prompt }));
    var list = U.el('div', { class: 'options' });
    var locked = false;
    q.options.forEach(function (text, i) {
      var btn = U.el('button', { class: 'btn option', type: 'button', text: text });
      btn.addEventListener('click', function () {
        if (locked) return;
        locked = true;
        Exam.answerQuestion(q, i);
        RENDERROOT(renderTask);
      });
      list.appendChild(btn);
    });
    box.appendChild(list);
    var skip = U.el('button', { class: 'btn ghost', type: 'button', text: 'Nie wiem — pomijam' });
    skip.addEventListener('click', function () {
      if (locked) return;
      locked = true;
      Exam.answerQuestion(q, -1);
      RENDERROOT(renderTask);
    });
    box.appendChild(U.el('div', { class: 'btn-row' }, [skip]));
  }

  /* --- 3. produkcja ustna ----------------------------------------------- */

  function renderSpeaking(box, item) {
    var rec = DB.any(item.recordId);
    if (!rec) {
      box.appendChild(U.el('p', { class: 'fb bad', text: 'Nie udało się wczytać hasła.' }));
      return;
    }
    box.appendChild(U.el('p', {
      class: 'muted',
      text: 'Powiedz to po tajsku, z pamięci. Wzorzec zobaczysz dopiero po nagraniu.'
    }));
    box.appendChild(U.el('p', { class: 'q-prompt', text: item.prompt }));

    var stage = U.el('div');
    box.appendChild(stage);

    var result = { tone: 0, plausible: false, empty: true };

    if (!PronView.canRecord() || !Pitch.supported) {
      /* Bez mikrofonu sprawność ustna nie jest mierzalna. Zamiast udawać
         ocenę, mówimy to wprost i przepuszczamy zadanie jako niezaliczone —
         certyfikat odnotuje, że tej sprawności nie zmierzono na tym urządzeniu. */
      stage.appendChild(U.el('p', { class: 'fb warn', text: PronView.micMessage() }));
      var skip = U.el('button', { class: 'btn', type: 'button', text: 'Dalej' });
      skip.addEventListener('click', function () {
        Exam.answerSpeaking(item, { tone: 0, claim: 'miss', plausible: false, empty: true });
        RENDERROOT(renderTask);
      });
      stage.appendChild(U.el('div', { class: 'btn-row' }, [skip]));
      return;
    }

    var control = PronView.control(rec, {
      compact: true,
      label: 'Nagraj odpowiedź',
      onResult: function (res) {
        if (!res || !res.ok) {
          result = { tone: 0, plausible: false, empty: true };
        } else {
          result = {
            tone: res.score,
            plausible: Exam.checkPlausible(res.analysis, (rec.syllables || []).length),
            empty: false
          };
        }
        showClaim();
      }
    });
    stage.appendChild(control);

    function showClaim() {
      var wrap = U.el('div', { class: 'exam-claim' });
      wrap.appendChild(U.el('hr'));
      wrap.appendChild(U.el('h3', { text: 'Wzorzec' }));
      wrap.appendChild(U.renderPhonetic(rec.thaiPhonetic, { hideTones: hideTones() }));
      wrap.appendChild(Player.button(rec, 'Posłuchaj wzorca'));
      wrap.appendChild(U.el('p', {
        class: 'muted',
        text: 'Wymowę ocenił automat (kontur tonalny). Treść musisz ocenić sam — '
          + 'aplikacja nie rozpoznaje mowy. Odpowiedz uczciwie: to jest jedyna część '
          + 'egzaminu, w której możesz oszukać wyłącznie siebie.'
      }));
      if (!result.plausible && !result.empty) {
        wrap.appendChild(U.el('p', {
          class: 'fb warn',
          text: 'Nagranie ma inną długość niż wzorzec, więc deklaracja „powiedziałem '
            + 'dokładnie to” nie zostanie przyjęta.'
        }));
      }
      var row = U.el('div', { class: 'btn-row' });
      Exam.CLAIMS.forEach(function (c) {
        var btn = U.el('button', { class: 'btn' + (c.value ? '' : ' ghost'), type: 'button', text: c.label });
        btn.addEventListener('click', function () {
          if (control.stopRecording) control.stopRecording();
          Player.stop();
          Exam.answerSpeaking(item, {
            tone: result.tone, claim: c.id,
            plausible: result.plausible, empty: result.empty
          });
          RENDERROOT(renderTask);
        });
        row.appendChild(btn);
      });
      wrap.appendChild(row);
      stage.appendChild(wrap);
      wrap.scrollIntoView({ block: 'nearest' });
    }
  }

  /* --- 4. produkcja pisemna --------------------------------------------- */

  function renderWriting(box, item) {
    var rec = DB.any(item.recordId);
    if (!rec) {
      box.appendChild(U.el('p', { class: 'fb bad', text: 'Nie udało się wczytać hasła.' }));
      return;
    }
    box.appendChild(U.el('p', {
      class: 'muted',
      text: 'Posłuchaj i zapisz to, co słyszysz, alfabetem łacińskim. Znaki tonu nie są '
        + 'wymagane — liczymy je osobno i nie wpływają na próg.'
    }));
    box.appendChild(U.el('p', { class: 'q-prompt', text: item.polish }));

    var info = U.el('p', { class: 'muted' });
    var play = U.el('button', { class: 'btn gold', type: 'button', text: 'Odtwórz' });
    function refresh() {
      var left = Exam.playsLeft(item.id);
      info.textContent = 'Pozostałe odtworzenia: ' + left + ' z ' + Exam.MAX_PLAYS + '.';
      play.disabled = left <= 0;
    }
    play.addEventListener('click', function () {
      if (!Exam.canPlay(item.id)) return;
      Exam.notePlay(item.id);
      refresh();
      Player.play(rec, { btn: play, tempo: 'natural' });
    });
    refresh();
    box.appendChild(U.el('div', { class: 'btn-row' }, [play]));
    box.appendChild(info);

    var input = U.el('input', {
      type: 'text', id: 'exam-write', autocomplete: 'off', autocapitalize: 'off',
      spellcheck: 'false', placeholder: 'np. sawat-dii'
    });
    box.appendChild(U.el('label', { class: 'field' },
      [U.el('span', { text: 'Twój zapis' }), input]));

    var send = U.el('button', { class: 'btn', type: 'button', text: 'Zatwierdź i dalej' });
    var locked = false;
    send.addEventListener('click', function () {
      if (locked) return;
      locked = true;
      Player.stop();
      Exam.answerWriting(item, input.value, rec.thaiPhonetic);
      RENDERROOT(renderTask);
    });
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') send.click(); });
    box.appendChild(U.el('div', { class: 'btn-row' }, [send]));
    input.focus();
  }

  /* --------------------------------------------------- wynik i diagnoza */

  function renderResult(root, attempt) {
    stopTimer();
    var diag = Exam.diagnose(attempt);
    if (!diag) {
      root.appendChild(U.el('p', { class: 'muted', text: 'To podejście zostało przerwane.' }));
      var back0 = U.el('button', { class: 'btn', type: 'button', text: 'Wróć do listy poziomów' });
      back0.addEventListener('click', function () { ExamView.showing = null; RENDERROOT(renderHub); });
      root.appendChild(U.el('div', { class: 'btn-row' }, [back0]));
      return;
    }

    var head = U.el('div', { class: 'card' });
    head.appendChild(U.el('h2', {
      text: attempt.passed
        ? ('Poziom ' + attempt.level + ' zaliczony')
        : ('Poziom ' + attempt.level + ' jeszcze niezaliczony')
    }));
    head.appendChild(U.el('p', {
      text: attempt.passed
        ? ('Wszystkie cztery sprawności przekroczyły swój próg. To znaczy, że materiał '
           + 'poziomu ' + attempt.level + ' działa i w rozumieniu, i w mówieniu.')
        : ('Zaliczone sprawności: ' + diag.sections.filter(function (s) { return s.passed; }).length
           + ' z 4. Poziom zalicza się dopiero przy komplecie — nie przy średniej, bo '
           + 'jedna mocna sprawność nie zastępuje słabej.')
    }));
    head.appendChild(U.el('p', {
      class: 'muted',
      text: 'Podejście z ' + U.dateWords(attempt.date) + ', ' + attempt.variant
        + ', czas ' + fmtTime(attempt.durationSec) + '.'
    }));
    root.appendChild(head);

    /* Rozbicie na sprawności — po to, żeby wynik nie kończył się procentem. */
    var table = U.el('div', { class: 'card' });
    table.appendChild(U.el('h3', { text: 'Rozbicie na sprawności' }));
    var tbl = U.el('table', { class: 'data-table' });
    var thead = U.el('tr');
    ['Sprawność', 'Wynik', 'Próg', 'Ocena'].forEach(function (t) {
      thead.appendChild(U.el('th', { text: t }));
    });
    tbl.appendChild(U.el('thead', {}, [thead]));
    var tbody = U.el('tbody');
    diag.sections.forEach(function (s) {
      var tr = U.el('tr');
      tr.appendChild(U.el('td', { text: s.meta.label }));
      if (s.id === 'speaking') {
        tr.appendChild(U.el('td', {
          text: 'wymowa ' + Math.round(s.box.tone) + ' pkt · treść ' + pctText(s.box.content)
        }));
        tr.appendChild(U.el('td', {
          text: s.box.toneThreshold + ' pkt · ' + s.box.contentThreshold + '%'
        }));
      } else {
        tr.appendChild(U.el('td', { text: pctText(s.box.pct) }));
        tr.appendChild(U.el('td', { text: s.box.threshold + '%' }));
      }
      tr.appendChild(U.el('td', {}, [U.el('span', {
        class: 'badge', text: s.passed ? 'zaliczone' : 'poniżej progu'
      })]));
      tbody.appendChild(tr);
    });
    tbl.appendChild(tbody);
    table.appendChild(tbl);
    if (attempt.sections.writing.tonePct !== null && attempt.sections.writing.tonePct !== undefined) {
      table.appendChild(U.el('p', {
        class: 'muted',
        text: 'Znaki tonu w zapisie: ' + pctText(attempt.sections.writing.tonePct)
          + ' trafnych. Nie wchodzą do progu — liczymy je, żeby było wiadomo, czy tony '
          + 'są słyszane, czy tylko zgadywane.'
      }));
    }
    root.appendChild(table);

    /* Najsłabsza sprawność — jedna, wskazana wprost. */
    var weak = U.el('div', { class: 'card' });
    weak.appendChild(U.el('h3', { text: 'Najsłabsza sprawność: ' + diag.weakest.meta.label }));
    weak.appendChild(U.el('p', {
      text: diag.weakest.margin >= 0
        ? ('Przeszła próg, ale z najmniejszym zapasem (' + diag.weakest.margin
           + ' punktu procentowego). To ona pierwsza polegnie na wyższym poziomie.')
        : ('Brakuje ' + Math.abs(diag.weakest.margin) + ' punktu procentowego do progu.')
    }));
    weak.appendChild(U.el('p', { class: 'muted', text: diag.weakest.meta.skill }));
    root.appendChild(weak);

    /* Plan naprawczy — konkretne ekrany, sceny i lekcje. */
    var plan = U.el('div', { class: 'card' });
    plan.appendChild(U.el('h3', { text: 'Plan naprawczy' }));
    if (!diag.plan.length) {
      plan.appendChild(U.el('p', { text: 'Nic do naprawy — wszystkie sprawności z zapasem.' }));
    }
    diag.plan.forEach(function (step) {
      var item = U.el('div', { class: 'plan-step' });
      item.appendChild(U.el('h4', { text: step.title }));
      item.appendChild(U.el('p', { class: 'muted', text: step.why }));
      var row = U.el('div', { class: 'btn-row' });
      var go = U.el('button', { class: 'btn', type: 'button', text: 'Otwórz: ' + step.screenLabel });
      go.addEventListener('click', function () { App.go(step.screen); });
      row.appendChild(go);
      if (step.lessons && step.lessons.length) {
        item.appendChild(U.el('p', {
          text: 'Lekcje: ' + step.lessons.join(', ') + '.'
        }));
      }
      if (step.sceneIds && step.sceneIds.length) {
        var titles = step.sceneIds.map(function (id) {
          var sc = sceneOf(id);
          return sc ? sc.title : id;
        });
        item.appendChild(U.el('p', { text: 'Sceny: ' + titles.join(' · ') + '.' }));
      }
      if (step.kind === 'srs') {
        item.appendChild(U.el('p', {
          class: 'muted',
          text: step.records.length + ' ' + U.plural(step.records.length, 'hasło', 'hasła', 'haseł')
            + ' już trafiło do kolejki powtórek.'
        }));
      }
      item.appendChild(row);
      plan.appendChild(item);
    });
    root.appendChild(plan);

    var foot = U.el('div', { class: 'card' });
    var again = U.el('button', { class: 'btn ghost', type: 'button', text: 'Wróć do listy poziomów' });
    again.addEventListener('click', function () { ExamView.showing = null; RENDERROOT(renderHub); });
    var cert = U.el('button', { class: 'btn', type: 'button', text: 'Certyfikat postępu' });
    cert.addEventListener('click', function () { ExamView.openCertificate(); });
    foot.appendChild(U.el('div', { class: 'btn-row' }, [cert, again]));
    root.appendChild(foot);
  }

  /* ------------------------------------------------------------ certyfikat */

  /* Co uczący się umie — po sytuacjach, nie po liczbie haseł. „Poradzisz
     sobie przy zamawianiu jedzenia” jest informacją; „opanowałeś 1240 haseł”
     nie jest, bo nikt nie wie, ile trzeba. */
  function situationsFor(level) {
    var order = ['Survival', 'A1', 'A2', 'B1', 'B2'];
    var upto = order.indexOf(level);
    var cats = {};
    (DB.lessons || []).forEach(function (L) {
      if (order.indexOf(L.level) <= upto && L.category) cats[L.category] = true;
    });
    return Object.keys(cats).sort();
  }

  ExamView.certificateData = function () {
    var summary = Progress.examSummary();
    var certified = Progress.certifiedLevel();
    var lessons = DB.lessons || [];
    var done = lessons.filter(function (L) { return Progress.isLessonDone(L.id); }).length;
    var stats = Progress.summary ? Progress.summary() : {};
    var checkpoints = Progress.checkpointSummary();
    return {
      date: U.today(),
      certified: certified,
      levels: summary,
      lessonsDone: done,
      lessonsTotal: lessons.length,
      words: stats.seen || 0,
      accuracy: stats.accuracy || 0,
      streak: (Progress.data && Progress.data.bestStreak) || 0,
      situations: certified ? situationsFor(certified) : [],
      checkpoints: checkpoints,
      dataVersion: DB.manifest ? DB.manifest.version : ''
    };
  };

  function esc(text) {
    return String(text === null || text === undefined ? '' : text)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  /* Czego certyfikat NIE obejmuje. Ta lista jest dłuższa niż lista osiągnięć
     i tak ma zostać. Dokument, który mówi tylko, co ktoś umie, jest reklamą;
     dokument, który mówi także, czego nie sprawdzono, jest oceną. */
  var LIMITS = [
    ['Pismo tajskie', 'Kurs w ogóle go nie uczy. Cały materiał jest w zapisie fonetycznym łacińskim. Znak drogowy, menu bez obrazków ani wiadomość SMS po tajsku pozostają nieczytelne.'],
    ['Akcenty regionalne', 'Materiał jest w tajskim centralnym (bangkockim). Isan, tajski północny i południowy brzmią inaczej i nie były sprawdzane.'],
    ['Mowa w hałasie', 'Egzamin odbywa się w ciszy. Bar, targ, ulica i telefon to warunki, w których rozumienie spada — i te warunki nie były na egzaminie.'],
    ['Treść wypowiedzi ustnej', 'Aplikacja nie rozpoznaje mowy. Automat ocenia wymowę (kontur tonalny), ale to, czy padło właściwe zdanie, deklaruje sam zdający. Ta część wyniku jest samooceną wspartą kontrolą długości nagrania.'],
    ['Głos syntetyczny', 'Nagrania pochodzą z syntezatora mowy systemu. Żywy mówca mówi szybciej, mniej wyraźnie i z redukcjami, których syntezator nie odtwarza.'],
    ['Rozmowa na żywo', 'Egzamin sprawdza reakcję na materiał przygotowany. Nie sprawdza rozmowy z człowiekiem, który przerywa, zmienia temat i nie czeka.'],
    ['Pisanie po tajsku', 'Sprawdzany jest zapis fonetyczny z pamięci, a nie pisanie tekstów. To narzędzie kontroli pamięci dźwiękowej, nie umiejętność praktyczna.']
  ];

  ExamView.certificateHTML = function () {
    var d = ExamView.certificateData();
    var rows = d.levels.map(function (l) {
      var best = l.best;
      var detail = '—';
      if (best && best.sections) {
        detail = Exam.ORDER.map(function (id) {
          var s = best.sections[id];
          var value = id === 'speaking'
            ? (Math.round(s.tone) + ' pkt / ' + Math.round(s.content) + '%')
            : (Math.round(s.pct) + '%');
          return esc(Exam.sectionMeta(id).short) + ' ' + value + (s.passed ? ' ✓' : ' ✗');
        }).join('<br>');
      }
      return '<tr><td>' + esc(l.level) + '</td><td>'
        + (l.passed ? 'zdany' + (l.passedAt ? ' (' + esc(U.dateWords(l.passedAt)) + ')' : '') : 'niezdany')
        + '</td><td>' + l.completed + '</td><td>' + detail + '</td></tr>';
    }).join('');

    var limits = LIMITS.map(function (pair) {
      return '<li><strong>' + esc(pair[0]) + '.</strong> ' + esc(pair[1]) + '</li>';
    }).join('');

    var situations = d.situations.length
      ? ('<ul class="cols">' + d.situations.map(function (s) {
          return '<li>' + esc(s) + '</li>';
        }).join('') + '</ul>')
      : '<p class="muted">Żaden poziom nie został jeszcze zdany egzaminem, więc nie ma podstaw, żeby wypisać sytuacje. Lista pojawi się po pierwszym zdanym poziomie.</p>';

    var checkRows = d.checkpoints.length
      ? d.checkpoints.map(function (c) {
          return '<tr><td>lekcje ' + c.fromLesson + '–' + c.toLesson + '</td><td>'
            + c.pct + '%</td><td>' + (c.passed ? 'w normie' : 'ubytek') + '</td></tr>';
        }).join('')
      : '<tr><td colspan="3">Nie było jeszcze żadnej próbki kontrolnej.</td></tr>';

    var verdict = d.certified
      ? ('Poziom potwierdzony egzaminem: <strong>' + esc(d.certified) + '</strong>. '
         + 'Oznacza to, że na tym poziomie wszystkie cztery sprawności — rozumienie ze słuchu, '
         + 'rozumienie szczegółowe, produkcja ustna i produkcja pisemna — przekroczyły swój '
         + 'osobny próg w jednym podejściu.')
      : ('Żaden poziom nie został jeszcze potwierdzony egzaminem. Ten dokument opisuje '
         + 'przerobiony materiał, a nie zmierzone umiejętności — i tej różnicy nie da się '
         + 'zatrzeć.');

    /* Deklaracja kodowania i fonty systemowe: dokument jest po polsku i musi
       zachować „ą”, „ć”, „ę”, „ł”, „ń”, „ó”, „ś”, „ź”, „ż” zarówno na ekranie,
       jak i po wydrukowaniu do PDF-u. */
    return '<!DOCTYPE html>\n<html lang="pl">\n<head>\n'
      + '<meta charset="utf-8">\n'
      + '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
      + '<title>Thai All-in-One — certyfikat postępu</title>\n'
      + '<style>\n'
      + '  :root { color-scheme: light; }\n'
      + '  body { font-family: "Segoe UI", "Helvetica Neue", "DejaVu Sans", "Liberation Sans", Arial, sans-serif;\n'
      + '         color: #16202e; background: #fff; margin: 0; padding: 32px 28px 48px;\n'
      + '         line-height: 1.55; max-width: 820px; }\n'
      + '  h1 { font-size: 26px; margin: 0 0 4px; }\n'
      + '  h2 { font-size: 18px; margin: 28px 0 8px; border-bottom: 2px solid #d7cfc2; padding-bottom: 4px; }\n'
      + '  .lead { font-size: 15px; margin: 0 0 18px; color: #4a5666; }\n'
      + '  table { border-collapse: collapse; width: 100%; font-size: 14px; }\n'
      + '  th, td { border: 1px solid #d7cfc2; padding: 6px 8px; text-align: left; vertical-align: top; }\n'
      + '  th { background: #f4f0ea; }\n'
      + '  ul { margin: 8px 0; padding-left: 20px; }\n'
      + '  ul.cols { columns: 2; }\n'
      + '  li { margin-bottom: 4px; }\n'
      + '  .muted { color: #5b6675; font-size: 14px; }\n'
      + '  .box { border: 1px solid #d7cfc2; background: #faf8f5; padding: 12px 14px; margin: 12px 0; }\n'
      + '  .no-print { margin: 20px 0; }\n'
      + '  button { font: inherit; padding: 8px 14px; border: 1px solid #16202e; background: #16202e;\n'
      + '           color: #fff; border-radius: 4px; cursor: pointer; }\n'
      + '  footer { margin-top: 28px; font-size: 12px; color: #5b6675; }\n'
      + '  @media print { .no-print { display: none; } body { padding: 0; } }\n'
      + '</style>\n</head>\n<body>\n'
      + '<h1>Certyfikat postępu — język tajski</h1>\n'
      + '<p class="lead">Thai All-in-One · dokument wystawiony ' + esc(U.dateWords(d.date))
      + (d.dataVersion ? ' · wersja bazy ' + esc(d.dataVersion) : '') + '</p>\n'
      + '<div class="no-print"><button onclick="window.print()">Drukuj / zapisz jako PDF</button></div>\n'
      + '<div class="box">' + verdict + '</div>\n'
      + '<h2>Co zostało zmierzone</h2>\n'
      + '<table><thead><tr><th>Poziom</th><th>Status</th><th>Podejść</th><th>Najlepszy wynik po sprawnościach</th></tr></thead>\n'
      + '<tbody>' + rows + '</tbody></table>\n'
      + '<p class="muted">Poziom uznaje się za zdany dopiero wtedy, gdy w jednym podejściu '
      + 'wszystkie cztery sprawności przekroczą swoje progi. Średnia nie zalicza niczego.</p>\n'
      + '<h2>W jakich sytuacjach to wystarcza</h2>\n'
      + situations + '\n'
      + '<h2>Przerobiony materiał</h2>\n'
      + '<p>Lekcje ścieżki: <strong>' + d.lessonsDone + ' z ' + d.lessonsTotal + '</strong>. '
      + 'Hasła widziane co najmniej raz: <strong>' + d.words + '</strong>. '
      + 'Trafność wszystkich odpowiedzi: <strong>' + d.accuracy + '%</strong>. '
      + 'Najdłuższa seria dni nauki: <strong>' + d.streak + '</strong>.</p>\n'
      + '<p class="muted">Przerobiony materiał to nie to samo co umiejętność. Ta sekcja mówi, '
      + 'ile pracy zostało włożone, a nie co z niej zostało w głowie — o tym mówi tabela wyżej.</p>\n'
      + '<h2>Próbki kontrolne</h2>\n'
      + '<table><thead><tr><th>Zakres</th><th>Wynik</th><th>Ocena</th></tr></thead>\n'
      + '<tbody>' + checkRows + '</tbody></table>\n'
      + '<h2>Czego ten dokument NIE obejmuje</h2>\n'
      + '<ul>' + limits + '</ul>\n'
      + '<footer>Dokument wystawiony przez aplikację na podstawie danych zapisanych w tej '
      + 'przeglądarce. Nie jest certyfikatem państwowym ani uznawanym urzędowo — jest '
      + 'uczciwym podsumowaniem tego, co aplikacja zmierzyła, i tego, czego nie mierzyła.</footer>\n'
      + '</body>\n</html>\n';
  };

  ExamView.openCertificate = function () {
    var html = ExamView.certificateHTML();
    var win = global.open('', '_blank');
    if (!win) {
      U.toast('Przeglądarka zablokowała nowe okno — pobieram plik zamiast otwierać.');
      ExamView.downloadCertificate();
      return;
    }
    win.document.open();
    win.document.write(html);
    win.document.close();
  };

  ExamView.downloadCertificate = function () {
    var html = ExamView.certificateHTML();
    /* charset=utf-8 w typie MIME i w samym dokumencie: bez tego plik otwarty
       z dysku traci polskie znaki. */
    var blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    var url = URL.createObjectURL(blob);
    var a = U.el('a', { href: url, download: 'thai-all-in-one-certyfikat-' + U.today() + '.html' });
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
    U.toast('Certyfikat pobrany. Otwórz go w przeglądarce i wydrukuj do PDF-u.');
  };

  ExamView.leave = function () {
    stopTimer();
    if (Exam.active()) Exam.abandon();
  };

  global.ExamView = ExamView;
})(window);
