// Hero (work wall), after baked.design's World script, dark theme.
// Cards sit in masonry columns on the inside of a cylinder around the viewer. The cylinder turns slowly on its own and
// every column drifts upward. The cursor looks around (yaw + pitch) and pushes the turn when it nears an edge; a card under
// the cursor lifts toward you and a chip names it. Scrolling scatters the cards outward from the middle of the screen
// (nearest cards go first), revealing the centre copy; the CTA slides down under it and a curved strip of case studies
// rises along the bottom and orbits. Past the hero, the CTA hands over to a fixed floating pill.
(() => {
  const hero = document.getElementById('hero');
  if (!hero) return;
  const stage = hero.querySelector('.bk-stage');
  const world = hero.querySelector('.bk-world');
  const center = hero.querySelector('.bk-center');
  const intro = hero.querySelector('.bk-intro');
  const book = hero.querySelector('.bk-book');
  const casesNav = hero.querySelector('.bk-cases');
  const cases = Array.from(casesNav.querySelectorAll('.bk-case'));
  const hint = hero.querySelector('.bk-hint');
  const pauseBtn = hero.querySelector('.bk-pause');
  const float = document.querySelector('.bk-float');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let paused = false;
  const still = () => reduce || paused;

  // ---------- wall content (swap the images later; keep name + url per entry) ----------
  const W8 = (n) => `assets/blog/posts/${n}`;
  const POSTS = ['0ac3ae8ddf.webp', '0cfa8cbc44.webp', '0d6fb47f45.webp', '113a0cb3d5.webp', '128eff985c.webp', '1be0bf6f38.webp', '2daaa7838c.webp', '32cdfdbeed.webp', '37c3149de8.webp', '38550ea2a6.webp', '48d08df74e.webp', '4ace1a0699.webp', '4c617f93ef.webp', '5ce7301097.webp', '603a59739f.webp', '61c021fd0c.webp', '63fa5c985e.webp', '6862b6ed81.jpg', '6b764bf0f1.webp', '6cbaa434d3.webp', '6df44a0513.webp', '7affde9b7d.webp', '90aa2ce390.webp', '9488a83dc7.webp', '95753594c6.webp', 'a7b59523bd.webp', 'aa75df667c.webp', 'b3216b6dac.webp', 'b863f0289c.webp', 'b9eda33355.webp', 'bb49a7610e.webp', 'bdb7ee856d.webp', 'c38820820d.webp', 'cb0a0350b7.webp', 'cbbf8f0229.webp', 'cc7e1237a9.webp', 'd5304ce6ca.webp', 'd559e300c6.webp', 'e59d202eab.webp', 'f3d5298c2a.webp'];
  const WALL = [
    { name: 'Digital Stream', src: 'assets/work/project-1.png', url: 'case-digital-stream.html', cs: 1 },
    { name: 'Hero Gradients', src: 'assets/work/project-2.png', url: 'case-hero-gradients.html', cs: 1 },
    { name: 'Lissr AI', src: 'assets/work/project-3.png', url: 'case-lissr-ai.html', cs: 1 },
    { name: 'United Advocates', src: 'assets/work/united-advocates.jpg', url: 'case-united-advocates.html', cs: 1 },
    { name: 'Digital Marketing', src: 'assets/reels/reel-1.mp4', poster: 'assets/reels/reel-1.jpg', video: 1, url: 'case-reel-digital-marketing.html', cs: 1 },
    { name: 'Justify Your Rates', src: 'assets/reels/reel-2.mp4', poster: 'assets/reels/reel-2.jpg', video: 1, url: 'case-reel-justify-your-rates.html', cs: 1 },
    { name: 'Strategy Without Content', src: 'assets/reels/reel-3.mp4', poster: 'assets/reels/reel-3.jpg', video: 1, url: 'case-reel-strategy-without-content.html', cs: 1 },
    { name: 'Kinetic Type', src: 'assets/reels/reel-4.mp4', poster: 'assets/reels/reel-4.jpg', video: 1, url: 'case-reel-kinetic-type.html', cs: 1 },
    { name: 'Solution Wagon', src: 'assets/reels/reel-5.mp4', poster: 'assets/reels/reel-5.jpg', video: 1, url: 'case-reel-solution-wagon.html', cs: 1 },
    { name: 'Showreel', src: 'assets/hero/laptop-meadow.mp4', poster: 'assets/hero/laptop-meadow-poster.jpg', video: 1, url: 'portfolio.html' },
    { name: 'Portal', src: 'assets/hero/portal-video.mp4', poster: 'assets/hero/portal-poster.jpg', video: 1, url: 'portfolio.html' },
    { name: 'Studio', src: 'assets/hero/mountain-desk.mp4', poster: 'assets/hero/mountain-desk-poster.jpg', video: 1, url: 'portfolio.html' },
    { name: 'Studio', src: 'assets/hero/mountain-desk-2-poster.jpg', url: 'portfolio.html' },
    { name: 'Brand film', src: 'assets/hero/hero-poster.jpg', url: 'portfolio.html' },
    { name: 'TV wall', src: 'assets/hero/tv-wall-poster.jpg', url: 'portfolio.html' },
    { name: 'Studio set', src: 'assets/hero/studio-stage.jpg', url: 'portfolio.html' },
    { name: 'Dubai after dark', src: 'assets/hero/bench-shot.jpg', url: 'portfolio.html' },
    { name: 'Workspace', src: 'assets/hero/desk-shot.jpg', url: 'portfolio.html' },
    { name: 'Timeline', src: 'assets/portfolio/timeline-laptop.jpg', url: 'portfolio.html' },
    { name: 'Squarezix', src: 'assets/footer/sz-stage.jpg', url: 'about-us.html' },
    { name: 'Social', src: 'assets/social/stage-bg.jpg', url: 'social-media-marketing.html' },
    { name: 'UX/UI Design', src: 'assets/services/uxui.png', url: 'website-design.html' },
    { name: 'Branding', src: 'assets/services/branding.png', url: 'branding.html' },
    { name: 'Marketing', src: 'assets/services/marketing.png', url: 'paid-marketing.html' },
    { name: 'Social Media', src: 'assets/services/social.png', url: 'social-media-marketing.html' },
    { name: 'AI Search', src: 'assets/services/ai.png', url: 'seo-ai-visibility.html' },
    { name: 'GCC Growth', src: 'assets/blog/gcc-growth.jpg', url: 'blogs.html' },
    { name: 'AI Search', src: 'assets/blog/ai-search.jpg', url: 'blogs.html' },
    { name: 'AI at Work', src: 'assets/blog/ai-workplace.jpg', url: 'blogs.html' },
    ...POSTS.map((p) => ({ name: 'Insights', src: W8(p), url: 'blogs.html' })),
  ];

  // ---------- build the cylinder ----------
  const RATIOS = [1.33, 1, .8, 1.6, 1.25, .75];   // card width / height, cycled down each column
  let cards = [], cols = [], E = { W: 250, R: 900, Z: 540, P: 1100, GAP: 34 };
  let hovered = null, overCard = false;

  function build() {
    world.textContent = ''; cards = []; cols = [];
    const mobile = innerWidth < 760, s = Math.max(1, innerWidth / 1440);
    E = mobile ? { W: 150, R: 560, Z: 330, P: 760, GAP: 22 }
      : { W: Math.round(250 * Math.min(s, 1.35)), R: Math.round(900 * s), Z: Math.round(540 * s), P: Math.round(1100 * s), GAP: Math.round(34 * Math.min(s, 1.35)) };
    world.style.perspective = E.P + 'px';
    const nCols = Math.round(360 / ((E.W + E.GAP + 14) / E.R * 180 / Math.PI));
    const colH = mobile ? Math.max(1100, innerHeight * 2.4) : 2300 * s;
    const slots = [];
    for (let c = 0; c < nCols; c++) {
      let y = 0, k = c * 2, row = 0;
      while (y < colH) { const h = Math.round(E.W / RATIOS[k % RATIOS.length]); k++; slots.push({ c, y, h, row: row++ }); y += h + E.GAP; }
      cols.push({ phi: 360 / nCols * c, L: y, off: (c * 173) % 400 });
    }
    // hand out images nearest-first, never repeating one among close neighbours
    const key = (w) => w.src;
    const used = new Map(), pick = new Array(slots.length);
    const near = (a, b) => {
      const A = slots[a], B = slots[b], dc = Math.abs(A.c - B.c);
      if (Math.min(dc, nCols - dc) > 2) return false;
      const L = cols[A.c].L || 1, dy = Math.abs(A.y + A.h / 2 - (B.y + B.h / 2));
      return Math.min(dy, Math.abs(L - dy)) < E.W * 2.6;
    };
    const dist = (i) => {
      const t = slots[i], col = cols[t.c], x = Math.min(t.c, nCols - t.c) * (E.W + E.GAP);
      const y = ((t.y + col.off) % col.L + col.L) % col.L - col.L / 2 + t.h / 2;
      return x * x + y * y;
    };
    const order = slots.map((_, i) => i).sort((a, b) => dist(a) - dist(b));
    const done = []; let cur = 0;
    for (const i of order) {
      const block = new Set(done.filter((j) => near(i, j)).map((j) => key(pick[j])));
      let best = -1, bestN = Infinity;
      for (let n = 0; n < WALL.length; n++) {
        const idx = (cur + n) % WALL.length, w = WALL[idx];
        if (block.has(key(w))) continue;
        const u = used.get(key(w)) || 0;
        if (u < bestN) { best = idx; bestN = u; }
      }
      if (best < 0) best = cur % WALL.length;
      pick[i] = WALL[best]; used.set(key(WALL[best]), (used.get(key(WALL[best])) || 0) + 1); done.push(i); cur = best + 1;
    }
    slots.forEach((t, i) => {
      const w = pick[i];
      const a = document.createElement('a');
      a.className = 'bk-card'; a.href = w.url; a.tabIndex = -1; a.draggable = false;
      a.style.width = E.W + 'px'; a.style.height = t.h + 'px';
      let video = null;
      if (w.video && !mobile) {
        video = document.createElement('video');
        video.src = w.src; video.poster = w.poster; video.muted = true; video.loop = true; video.playsInline = true; video.preload = 'none';
        a.append(video);
      } else {
        const img = document.createElement('img');
        img.src = w.video ? w.poster : w.src; img.alt = ''; img.decoding = 'async'; img.loading = 'lazy'; img.draggable = false;
        a.append(img);
      }
      a.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') { overCard = true; hovered = a; showChip(w, e); } });
      a.addEventListener('pointerleave', () => { overCard = false; if (hovered === a) hovered = null; hideChip(); });
      a.addEventListener('click', (e) => { if (dragDist > 6) e.preventDefault(); });
      world.append(a);
      cards.push({ el: a, video, col: t.c, y: t.y, h: t.h, shown: false, lift: 0 });
    });
  }

  // ---------- chip that follows the cursor over a card ----------
  const chip = document.createElement('span');
  chip.className = 'bk-chip'; chip.setAttribute('aria-hidden', 'true'); stage.append(chip);
  function showChip(w, e) { chip.textContent = w.cs ? `${w.name} · case study` : w.name; chip.classList.add('on'); moveChip(e); }
  function moveChip(e) { chip.style.transform = `translate(${e.clientX + 14}px, ${e.clientY + 14}px)`; }
  function hideChip() { chip.classList.remove('on'); }

  // ---------- input ----------
  let yaw = 0, kick = 0, auto = 1, spin = reduce ? 0 : 7, drift = 0, lastMove = -1e9;
  let tx = 0, ty = 0, sx = 0, sy = 0, px = 0, inside = false, edge = 0;
  let dragging = false, dragDist = 0, lastX = 0, startX = 0, startY = 0, axis = 0, touch = false;

  world.addEventListener('pointerdown', (e) => {
    dragging = true; dragDist = 0; lastX = startX = e.clientX; startY = e.clientY; kick = 0;
    touch = e.pointerType !== 'mouse'; axis = touch ? 0 : 1;
  });
  stage.addEventListener('pointermove', (e) => {
    if (e.pointerType !== 'mouse' || reduce) return;
    px = e.clientX / innerWidth * 2 - 1;
    const py = e.clientY / innerHeight * 2 - 1;
    if (!dragging) { tx = px * 24; ty = py; }
    inside = true; lastMove = performance.now();
    if (hovered) moveChip(e);
  });
  const out = () => { inside = false; tx = 0; ty = 0; edge = 0; hideChip(); };
  stage.addEventListener('pointerleave', out);
  document.addEventListener('mouseleave', out);
  addEventListener('blur', out);
  stage.addEventListener('wheel', (e) => {
    if (Math.abs(e.deltaX) > Math.abs(e.deltaY) && !reduce) { kick -= e.deltaX * .9; e.preventDefault(); }
  }, { passive: false });
  world.addEventListener('pointermove', (e) => {
    if (!dragging) return;
    if (!axis) {
      const dx = Math.abs(e.clientX - startX), dy = Math.abs(e.clientY - startY);
      if (dx + dy < 8) return;
      axis = dx > dy * 1.2 ? 1 : -1; lastX = e.clientX;
    }
    if (axis < 0) return;
    const d = e.clientX - lastX; lastX = e.clientX; dragDist += Math.abs(d);
    if (dragDist > 6 && !world.hasPointerCapture(e.pointerId)) { try { world.setPointerCapture(e.pointerId); } catch (_) {} world.classList.add('grab'); }
    yaw += d * .09; kick += (d * 6 - kick) * (touch ? .35 : 1);
  });
  const up = () => { dragging = false; world.classList.remove('grab'); };
  world.addEventListener('pointerup', up); world.addEventListener('pointercancel', up);

  // case strip: drag to spin, slows on hover
  let caseHover = false, caseDrag = false, caseDist = 0, caseX = 0, caseOff = 0, caseVel = 0, caseInit = false, caseSlow = 1, caseW = 0;
  casesNav.addEventListener('pointerenter', () => { caseHover = true; });
  casesNav.addEventListener('pointerleave', () => { caseHover = false; caseDrag = false; });
  casesNav.addEventListener('pointerdown', (e) => { caseDrag = true; caseDist = 0; caseX = e.clientX; });
  casesNav.addEventListener('pointermove', (e) => {
    if (!caseDrag) return;
    const d = e.clientX - caseX; caseX = e.clientX; caseDist += Math.abs(d);
    if (caseDist > 6 && !casesNav.hasPointerCapture(e.pointerId)) { try { casesNav.setPointerCapture(e.pointerId); } catch (_) {} }
    caseOff += d; caseVel = d * 60;
  });
  const caseUp = () => { caseDrag = false; };
  casesNav.addEventListener('pointerup', caseUp); casesNav.addEventListener('pointercancel', caseUp);
  cases.forEach((c) => c.addEventListener('click', (e) => { if (caseDist > 6) e.preventDefault(); }));

  pauseBtn && pauseBtn.addEventListener('click', () => {
    paused = !paused;
    pauseBtn.dataset.paused = paused ? '1' : '';
    pauseBtn.querySelector('.bk-pause-t').textContent = paused ? 'Play motion' : 'Pause motion';
    spin = still() ? 0 : 7;
    cards.forEach((c) => { if (c.video) { if (paused || !c.shown) c.video.pause(); else c.video.play().catch(() => {}); } });
  });

  // ---------- layout numbers ----------
  let X = innerWidth, Y = innerHeight, introH = 0, centerH = 0, bookH = 56, bookW = 180, stageH = innerHeight, headH = 0;
  function measure() {
    X = innerWidth; Y = innerHeight;
    centerH = center.offsetHeight; introH = intro ? intro.offsetHeight : 0; bookH = book.offsetHeight || 56; bookW = book.offsetWidth || 180;
    stageH = stage.offsetHeight || innerHeight;
    headH = parseFloat(getComputedStyle(hero).marginTop) || 0;
    if (float) { float.style.width = bookW + 'px'; float.style.height = bookH + 'px'; }
    caseW = 0;
  }
  let rT = 0;
  addEventListener('resize', () => {
    clearTimeout(rT);
    rT = setTimeout(() => { const flip = (innerWidth < 760) !== (X < 760); measure(); if (flip) build(); }, 120);
  });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure).catch(() => {});

  // ---------- floating CTA hand-off ----------
  let floatOn = false, floatAnim = null;
  function setFloat(on) {
    if (!float) return;
    if (floatAnim) floatAnim.cancel(); floatAnim = null;
    const b = book.getBoundingClientRect();
    if (on) {
      book.style.visibility = 'hidden'; float.classList.add('on');
      if (reduce) return;
      const f = float.getBoundingClientRect();
      floatAnim = float.animate([
        { transform: `translate(${b.left - f.left}px, ${b.top - f.top}px)`, easing: 'cubic-bezier(.55,0,.9,.45)' },
        { transform: 'translate(0, 0) scale(.94, 1.1)', offset: .62, easing: 'cubic-bezier(.2,.8,.2,1)' },
        { transform: 'translate(0, 3px) scale(1.16, .8)', offset: .74, easing: 'cubic-bezier(.3,0,.3,1)' },
        { transform: 'translate(0, -4px) scale(.95, 1.06)', offset: .87, easing: 'cubic-bezier(.3,0,.3,1)' },
        { transform: 'none' },
      ], { duration: 720 });
    } else {
      const f = float.getBoundingClientRect();
      const done = () => { float.classList.remove('on'); book.style.visibility = ''; floatAnim = null; };
      if (reduce) return done();
      floatAnim = float.animate([{ transform: 'none' }, { transform: `translate(${b.left - f.left}px, ${b.top - f.top}px)` }], { duration: 320, easing: 'cubic-bezier(.4,0,.2,1)' });
      floatAnim.onfinish = done;
    }
  }
  const foot = document.querySelector('footer');
  if (foot && float && 'IntersectionObserver' in window) {
    new IntersectionObserver(([en]) => float.classList.toggle('foot', en.isIntersecting)).observe(foot);
  }

  // ---------- frame ----------
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const smooth = (t) => t * t * (3 - 2 * t);
  const rnd = (i) => { const t = Math.sin(i * 78.233) * 43758.5453; return t - Math.floor(t); };
  const t0 = performance.now();
  let last = t0, G = 0;

  function frame(now) {
    const dt = Math.min(.05, (now - last) / 1000); last = now;
    const n = (now - t0) / 1000;                                    // seconds since load (intro)
    const hr = hero.getBoundingClientRect();
    const v = clamp((headH - hr.top) / (Y * .9));                   // scroll progress through the hero
    G = reduce || Math.abs(v - G) < 5e-4 ? v : G + (v - G) * (1 - Math.exp(-dt / .1));

    if (hr.bottom > 0) {
      if (!dragging) {
        kick *= Math.pow(.04, dt);
        const moving = now - lastMove < 900;
        auto += ((overCard ? 0 : moving ? .35 : 1) - auto) * (1 - Math.pow(.05, dt));
        const atEdge = inside && now - lastMove > 450 && Math.abs(px) > .78 && !overCard;
        edge += ((atEdge ? Math.sign(px) * 14 * Math.min(1, (Math.abs(px) - .78) / .2) : 0) - edge) * (1 - Math.pow(.02, dt));
        yaw += (spin * auto + kick + edge) * dt;
      }
      if (!still()) drift += 22 * auto * dt;
      const ease = 1 - Math.pow(4e-4, dt);
      sx += (tx - sx) * ease; sy += (ty - sy) * ease;
      world.style.perspectiveOrigin = `50% ${(50 + sy * 9).toFixed(2)}%`;

      const look = yaw - sx, lift = -sy * 70, { R, Z, P } = E;
      for (let i = 0; i < cards.length; i++) {
        const c = cards[i], col = cols[c.col];
        const s = ((col.phi + look) % 360 + 540) % 360 - 180;     // card's angle off straight ahead
        let show = Math.abs(s) <= 82 && G < 1, x = 0, y = 0, z = 0, op = 1;
        if (show) {
          const rad = s * Math.PI / 180;
          x = R * Math.sin(rad);
          const zb = Z - R * Math.cos(rad);
          y = ((c.y + col.off - drift) % col.L + col.L) % col.L - col.L / 2 + c.h / 2 + lift;
          if (Math.abs(y) > (E.W === 150 ? col.L / 2 + 200 : 1000 * R / 900)) show = false;
          else {
            const sc = P / (P - zb), ox = x * sc, oy = y * sc, m = Math.hypot(ox, oy);
            const dir = m < 40 ? rnd(i + 13) * Math.PI * 2 : Math.atan2(oy, ox);
            const sp = smooth(clamp((G - Math.min(1, m / 900) * .3) / .7));   // nearer the middle scatters first
            if (sp > .995) show = false;
            else {
              const push = (Math.max(0, Math.hypot(X, Y) / 1.7 - m) + 250) / sc * sp;
              const delay = Math.abs(s) / 82 + Math.abs(y) / 1400;
              const intro = reduce ? 1 : 1 - Math.pow(1 - clamp((n - .1 - delay * .9) / .9), 3);
              x += Math.cos(dir) * push; y += Math.sin(dir) * push;
              c.lift += (+(c.el === hovered && G < .2) - c.lift) * (1 - Math.pow(.001, dt));
              z = zb - (1 - intro) * 500 + 160 * sp + c.lift * 70;
              if (z > P * .7) show = false;
              op = intro * Math.min(1, (P * .7 - z) / 250);
              if (show) c.el.style.transform = `translate3d(${(x - E.W / 2).toFixed(1)}px,${(y - c.h / 2).toFixed(1)}px,${z.toFixed(1)}px) rotateY(${(-s).toFixed(2)}deg)`;
            }
          }
        }
        if (show !== c.shown) {
          c.shown = show; c.el.style.visibility = show ? 'visible' : 'hidden';
          if (c.video) { if (show && !still()) c.video.play().catch(() => {}); else c.video.pause(); }
        }
        if (show) c.el.style.opacity = op.toFixed(3);
      }

      // centre copy, CTA, case strip
      const reveal = 1 - Math.pow(1 - clamp((G - .45) / .4), 3);
      center.style.opacity = reveal.toFixed(3);
      center.style.transform = `translate(-50%, calc(-50% + ${((1 - reveal) * 14).toFixed(1)}px))`;
      // at rest the opening copy + CTA sit as one centred block; the copy lifts away as the wall scatters
      const gap = introH ? 30 : 0, top0 = Math.max(16, (stageH - (introH + gap + bookH)) / 2);
      if (intro) {
        const io = clamp(G / .32), ie = io * io;
        intro.style.opacity = (clamp((n - .5) / .7) * (1 - io)).toFixed(3);
        intro.style.transform = `translate(-50%, ${(top0 - ie * 60 + (1 - clamp((n - .5) / .7)) * 14).toFixed(1)}px) scale(${(1 - ie * .06).toFixed(4)})`;
        intro.style.visibility = io >= 1 ? 'hidden' : 'visible';
      }
      const b0 = top0 + introH + gap, b1 = stageH / 2 - 90 + centerH / 2 + 36, bs = smooth(G);
      book.style.opacity = clamp((n - 1.2) / .5).toFixed(3);
      book.style.transform = `translate(-50%, ${(b0 + (b1 - b0) * bs).toFixed(1)}px)`;
      casesNav.style.opacity = reveal.toFixed(3);
      casesNav.style.transform = `translateY(${((1 - reveal) * 16).toFixed(1)}px)`;
      casesNav.style.pointerEvents = reveal > .5 ? 'auto' : 'none';
      if ((reveal > .5) === casesNav.inert) casesNav.inert = reveal <= .5;
      hint.style.opacity = n > 1.8 && G < .04 ? '1' : '0';

      if (reveal > 0) {
        caseSlow += ((caseHover ? .1 : 1) - caseSlow) * (1 - Math.pow(.001, dt));
        if (!caseDrag) { caseVel *= Math.pow(.03, dt); caseOff += ((still() ? 0 : -45) * caseSlow + caseVel) * dt; }
        const w = (caseW ||= cases[0] ? cases[0].offsetWidth : 219) || 219;
        const rad = X < 760 ? 900 : 1600, step = (w + 8) / rad, span = cases.length * step;
        if (!caseInit) { caseInit = true; caseOff = rad * (span / 2 - Math.asin(Math.min(.99, (X / 2 - w / 2 - 16) / rad))); }
        for (let k = 0; k < cases.length; k++) {
          const a = ((k * step + caseOff / rad) % span + span) % span - span / 2;
          const vis = Math.abs(rad * Math.sin(a)) < X / 2 + w && Math.abs(a) < 1.2;
          cases[k].style.visibility = vis ? 'visible' : 'hidden';
          if (vis) cases[k].style.transform = `translate3d(${(X / 2 - w / 2 + rad * Math.sin(a)).toFixed(1)}px,0,${(rad * (1 - Math.cos(a))).toFixed(1)}px) rotateY(${(-a * 180 / Math.PI).toFixed(2)}deg)`;
        }
      }
    }

    // scrolling away from a hovered card never fires pointerleave: drop the chip once the wall has scattered
    if ((hovered || chip.classList.contains('on')) && (G > .2 || hr.bottom < 0)) { hovered = null; overCard = false; hideChip(); }
    document.body.classList.toggle('qc-hide', hr.bottom > Y * .5);   // contact dock waits until the hero is done
    if (float && n > 1.7) {
      const on = floatOn ? hr.bottom < Y + 8 : hr.bottom < Y - 8;
      if (on !== floatOn) { floatOn = on; setFloat(on); pauseBtn && pauseBtn.classList.toggle('gone', on); }
    }
    requestAnimationFrame(frame);
  }

  build();
  measure();
  requestAnimationFrame(frame);
})();
