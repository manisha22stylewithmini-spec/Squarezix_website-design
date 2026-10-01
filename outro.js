// Outro sequence (home) + footer bits (every page).
//
// Outro — scroll progress p (0→1) while the stage is pinned (animation flow frames):
//   0.00–0.06  [1]  the Amethyst Wash "That's What Inside." card sits in the page
//   0.06–0.30  [2]  it shrinks to a rounded square, the words shrinking with it
//   0.30–0.42  [3]  → a small, sharp square; the wash hands over to solid violet
//   0.42–0.50  [4]  the square slides left to where the headline starts
//   0.50–0.72  [5–6] it types "Now Let's Build Yours" — the text appears behind it
//   0.72–0.76        it blinks at the end of the line, like a cursor
//   0.76–0.88  [7]  the screen folds into an outlined card, the talk row rises below,
//                   the square hops to "Let's Talk" and the headline gets its full stop
//   0.91–0.99  [8–9] "Let's Talk" gets its full stop; the square tumbles down and
//                   becomes the newsletter button
// One clipped element (.outro-panel) is the card and the square the whole way, so the
// motion never cuts. Everything is scrubbed by scroll and reverses on the way back up.
(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp01 = (v) => Math.min(Math.max(v, 0), 1);
  const seg = (p, a, b) => clamp01((p - a) / (b - a));
  const lerp = (a, b, t) => a + (b - a) * t;
  const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const easeOut = (t) => 1 - Math.pow(1 - t, 3);
  const smooth = (t) => t * t * (3 - 2 * t);

  // ---------- Outro ----------
  const stage = document.getElementById('outro-stage');
  if (stage) {
    const section = stage.parentElement;
    const frame = stage.querySelector('.outro-frame');
    const panel = stage.querySelector('.outro-panel');
    const inside = stage.querySelector('.outro-inside');
    const build = stage.querySelector('.outro-build');
    const typed = build.querySelector('.outro-typed');
    const buildDot = build.querySelector('.outro-dot');
    const cta = stage.querySelector('.szf-cta');
    const slot = cta.querySelector('.szf-square');
    const talkDot = cta.querySelector('.szf-talk-dot');
    const send = cta.querySelector('.szf-send');
    const cue = stage.querySelector('.outro-cue');

    // Animated Amethyst Wash fill for the card (falls back to the CSS gradient)
    const washCanvas = stage.querySelector('.outro-wash');
    const wash = washCanvas && window.AmethystWash ? window.AmethystWash.mount(washCanvas) : null;
    if (!wash && washCanvas) washCanvas.remove();

    // Card from Section.pdf: 1676×531, 61px radius; type size as a share of card width
    const CARD_RATIO = 531 / 1676;
    const CARD_RADIUS = 61 / 531;
    const TEXT_RATIO = 113 / 1676;
    const VIOLET = '176, 77, 255';            // #b04dff — the square from frame 4 on

    let g = null;
    let lastWash = null;
    let target = 0, current = 0, running = false, inView = false;

    function measure() {
      build.style.transform = 'none';
      cta.style.transform = 'none';
      inside.style.transform = 'none';
      frame.style.height = '';
      const s = stage.getBoundingClientRect();
      const W = s.width, H = s.height;

      const gutter = Math.min(Math.max(W * 0.04, 16), 64);
      const Wc = W - gutter * 2;
      const Hc = Math.min(Wc * CARD_RATIO, H * 0.8);
      inside.style.fontSize = `${(Wc * TEXT_RATIO).toFixed(2)}px`;
      lastWash = null;

      // Where the dark screen folds to, and where the talk row sits under it
      // The talk row gets generous room above it; the folded card takes whatever height
      // is left, so the row always fits with space below it on short screens too
      const gap = Math.min(Math.max(H * 0.11, 44), 130);
      const ctaH = cta.offsetHeight;
      const room = Math.min(Math.max(H * 0.06, 28), 64);
      const cardH = Math.max(H * 0.34, Math.min(H * (W < 700 ? 0.46 : 0.52), H - gap - ctaH - room));
      stage.style.setProperty('--cta-top', `${(cardH + gap).toFixed(1)}px`);

      const hb = build.getBoundingClientRect();
      const tb = typed.getBoundingClientRect();
      const sl = slot.getBoundingClientRect();
      const sb = send.getBoundingClientRect();
      g = {
        W, H, Wc, Hc, cardH,
        R: Math.min(Math.max(W * 0.022, 20), 44),
        S1: Math.min(W, H) * 0.62,
        S2: tb.height * 0.62,                    // about a capital letter tall
        hH: hb.height,
        x0: tb.left - s.left,                    // where "Now" starts
        x1: tb.right - s.left,                   // just after "Yours"
        yT: tb.top - hb.top + tb.height / 2,     // text centre inside the headline box
        lx: sl.left - s.left + sl.width / 2, ly: sl.top - s.top + sl.height / 2, ls: sl.width,
        bx: sb.left - s.left + sb.width / 2, by: sb.top - s.top + sb.height / 2, bs: sb.width,
        stickyTop: parseFloat(getComputedStyle(stage).top) || 0,
        distance: Math.max(1, section.offsetHeight - stage.offsetHeight),
        insideW: 0, insideH: 0,
      };
      g.insideW = inside.offsetWidth;
      g.insideH = inside.offsetHeight;
      render(current, performance.now());
    }

    function progress() {
      return clamp01((g.stickyTop - section.getBoundingClientRect().top) / g.distance);
    }

    function render(p, now) {
      if (!g) return;
      const { W, H, S1, S2 } = g;

      const e1 = easeInOut(seg(p, 0.06, 0.3));
      const e2 = easeInOut(seg(p, 0.3, 0.42));
      const slide = easeInOut(seg(p, 0.42, 0.5));
      const type = smooth(seg(p, 0.5, 0.72));
      const fold = easeInOut(seg(p, 0.76, 0.88));
      const hop = easeInOut(seg(p, 0.79, 0.89));
      const tumble = easeInOut(seg(p, 0.91, 0.99));
      const rise = easeOut(seg(p, 0.78, 0.87));

      // --- The dark screen folds into an outlined card ---
      const frameH = lerp(H, g.cardH, fold);
      frame.style.height = `${frameH.toFixed(2)}px`;
      frame.style.borderRadius = `${(g.R * fold).toFixed(2)}px`;
      frame.style.borderColor = `rgba(157, 90, 255, ${(0.75 * fold).toFixed(3)})`;
      cue.style.visibility = fold > 0 ? 'hidden' : '';   // (its blink animation owns opacity)

      // --- Headline stays centred in the screen/card; revealed behind the square ---
      const ty = frameH / 2 - g.hH / 2;
      build.style.transform = `translate3d(0, ${ty.toFixed(2)}px, 0)`;
      const typedEdge = g.x0 + (g.x1 - g.x0) * type;          // the square's left edge
      build.style.clipPath = hop > 0 ? 'none' : `inset(0 ${(W - typedEdge).toFixed(2)}px 0 0)`;
      buildDot.style.opacity = hop > 0.05 ? 1 : 0;

      // --- Talk row rises in below the card ---
      cta.style.opacity = rise.toFixed(3);
      cta.style.transform = `translate3d(0, ${((1 - rise) * 40).toFixed(2)}px, 0)`;
      cta.classList.toggle('is-live', rise > 0.6);
      talkDot.style.opacity = tumble > 0.05 ? 1 : 0;

      // --- The one shape: card → square → cursor → hop → button ---
      let cx = W / 2, cy = H / 2, w, h;
      if (e1 < 1) {
        w = lerp(g.Wc, S1, e1);
        h = lerp(g.Hc, S1, e1);
      } else {
        w = h = lerp(S1, S2, e2);
      }
      // Slide to the start of the line, then type along it
      const textCy = ty + g.yT;
      cx = lerp(cx, typedEdge + S2 / 2, slide);
      cy = lerp(cy, textCy, slide);
      // Hop to "Let's Talk"
      cx = lerp(cx, g.lx, hop); cy = lerp(cy, g.ly, hop);
      if (e1 >= 1) w = h = lerp(w, g.ls, hop);
      // Tumble down into the newsletter button: a small arc and a tilt on the way
      const arc = Math.sin(Math.PI * tumble);
      cx = lerp(cx, g.bx, tumble);
      cy = lerp(cy, g.by, tumble) - arc * Math.min(60, H * 0.07);
      if (e1 >= 1) w = h = lerp(w, g.bs, tumble);
      const rot = reduce ? 0 : -32 * arc;

      const landed = tumble >= 1;
      panel.style.visibility = landed ? 'hidden' : 'visible';
      send.style.opacity = landed ? 1 : 0;

      const t = cy - h / 2, l = cx - w / 2;
      if (e2 < 1) {
        // Card and rounded square: corners stay proportional, then sharpen
        const r = Math.min(w, h) * CARD_RADIUS * (1 - e2);
        panel.style.clipPath = `inset(${t.toFixed(2)}px ${(W - l - w).toFixed(2)}px ${(H - t - h).toFixed(2)}px ${l.toFixed(2)}px round ${r.toFixed(2)}px)`;
      } else {
        // Sharp square that can tilt: four rotated corners
        const a = (rot * Math.PI) / 180, c = Math.cos(a), sn = Math.sin(a), k = w / 2;
        const pt = (dx, dy) => `${(cx + dx * c - dy * sn).toFixed(2)}px ${(cy + dx * sn + dy * c).toFixed(2)}px`;
        panel.style.clipPath = `polygon(${pt(-k, -k)}, ${pt(k, -k)}, ${pt(k, k)}, ${pt(-k, k)})`;
      }

      // Colour: the wash (or the design's gradient) → solid violet as it becomes the square
      const base = wash ? 'linear-gradient(#0a0720, #0a0720)' : 'linear-gradient(180deg, #7340b6, #ab5fdc 50%, #dd7aff)';
      panel.style.backgroundImage = `linear-gradient(rgba(${VIOLET}, ${e2.toFixed(3)}), rgba(${VIOLET}, ${e2.toFixed(3)})), ${base}`;
      panel.style.backgroundSize = `${w.toFixed(2)}px ${h.toFixed(2)}px`;
      panel.style.backgroundPosition = `${l.toFixed(2)}px ${t.toFixed(2)}px`;

      // Cursor blink at the end of the typed line
      const blinking = !reduce && p > 0.72 && p < 0.76;
      panel.style.opacity = blinking && Math.floor(now / 420) % 2 ? 0.25 : 1;

      // The wash is sized to the live shape (never stretched); its buffer only
      // reallocates when the size changes by >12%
      if (wash) {
        const on = e2 < 1;
        washCanvas.style.opacity = (1 - e2).toFixed(3);
        if (on) {
          washCanvas.style.transform = `translate3d(${l.toFixed(2)}px, ${t.toFixed(2)}px, 0)`;
          washCanvas.style.width = `${w.toFixed(2)}px`;
          washCanvas.style.height = `${h.toFixed(2)}px`;
          if (!lastWash || Math.abs(w / lastWash.w - 1) > 0.12 || Math.abs(h / lastWash.h - 1) > 0.12) {
            lastWash = { w, h };
            wash.resize();
          }
        }
        wash.setActive(inView && on);
      }

      // "That's What Inside." rides the card, shrinking with it, then fades
      const ts = (w / g.Wc) * (1 - 0.1 * e1);
      inside.style.transform = `translate3d(${(cx - g.insideW / 2).toFixed(2)}px, ${(cy - g.insideH / 2).toFixed(2)}px, 0) scale(${ts.toFixed(4)})`;
      inside.style.opacity = (1 - seg(p, 0.3, 0.4)).toFixed(3);
    }

    // Ease toward the scroll position; keep ticking while visible (cursor blink, wash)
    function loop(now) {
      const d = target - current;
      current = reduce || Math.abs(d) < 0.0004 ? target : current + d * 0.14;
      render(current, now);
      if (inView || current !== target) requestAnimationFrame(loop);
      else running = false;
    }
    const kick = () => { if (!running && g) { running = true; requestAnimationFrame(loop); } };

    window.addEventListener('scroll', () => { if (g) { target = progress(); kick(); } }, { passive: true });
    let rt; window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { measure(); target = progress(); kick(); }, 150); });
    new IntersectionObserver(([e]) => {
      inView = e.isIntersecting;
      if (inView) kick();
      else if (wash) wash.setActive(false);   // no shader work while off screen
    }).observe(section);

    measure();
    current = target = progress();
    render(current, performance.now());
    document.fonts.ready.then(() => { measure(); target = progress(); kick(); });
  }

  // ---------- Footer: partner strip loop ----------
  document.querySelectorAll('.szf-partners-track').forEach((track) => {
    const group = track.querySelector('.szf-partners-group');
    const build = () => {
      track.querySelectorAll('[data-clone]').forEach((c) => c.remove());
      const gw = group.getBoundingClientRect().width;
      if (!gw) return;
      const copies = Math.max(1, Math.ceil((track.parentElement.clientWidth * 2) / gw));
      for (let i = 0; i < copies; i++) {
        const c = group.cloneNode(true);
        c.setAttribute('data-clone', ''); c.setAttribute('aria-hidden', 'true');
        track.appendChild(c);
      }
      // The shared `ribbon` keyframes (sections.css) read --ribbon-group-width
      track.style.setProperty('--ribbon-group-width', `${gw}px`);
      track.style.setProperty('--szf-partners-duration', `${gw / 50}s`);
    };
    document.fonts.ready.then(build);
    let t; window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(build, 150); });
  });

  // ---------- Footer: Dubai clock ----------
  const hh = document.querySelectorAll('.szf-hh');
  const mm = document.querySelectorAll('.szf-mm');
  if (hh.length) {
    const fmt = new Intl.DateTimeFormat('en-GB', { timeZone: 'Asia/Dubai', hour: '2-digit', minute: '2-digit', hour12: false });
    const tick = () => {
      const [h, m] = fmt.format(new Date()).split(':');
      hh.forEach((el) => { el.textContent = h; });
      mm.forEach((el) => { el.textContent = m; });
    };
    tick();
    setInterval(tick, 15000);
  }

  // ---------- Footer: SQUAREZIX tiles light up in turn while idle ----------
  document.querySelectorAll('.szf-tiles').forEach((grid) => {
    if (reduce) return;
    const tiles = [...grid.children];
    let i = 0, timer = null, hovering = false;
    const step = () => {
      tiles.forEach((t) => t.classList.remove('is-ping'));
      if (!hovering) tiles[i % tiles.length].classList.add('is-ping');
      i++;
    };
    grid.addEventListener('pointerenter', () => { hovering = true; tiles.forEach((t) => t.classList.remove('is-ping')); });
    grid.addEventListener('pointerleave', () => { hovering = false; });
    new IntersectionObserver(([e]) => {
      clearInterval(timer);
      if (e.isIntersecting) timer = setInterval(step, 900);
      else tiles.forEach((t) => t.classList.remove('is-ping'));
    }).observe(grid);
  });

  // ---------- Footer: newsletter (no list provider yet — hands off to email) ----------
  document.querySelectorAll('[data-newsletter]').forEach((form) => {
    const note = form.querySelector('.szf-news-note');
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = form.querySelector('input[type="email"]');
      if (!/^\S+@\S+\.\S+$/.test(input.value.trim())) {
        note.textContent = 'Please enter a valid email.';
        input.focus();
        return;
      }
      window.location.href = `mailto:info@squarezix.com?subject=${encodeURIComponent('Weekly AI insights — subscribe')}&body=${encodeURIComponent(`Please add ${input.value.trim()} to the weekly AI insights list.`)}`;
      note.textContent = 'Opening your email app…';
    });
  });
})();
