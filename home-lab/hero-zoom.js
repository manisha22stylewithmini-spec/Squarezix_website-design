// Pinned hero push-in. While .hero-stage is stuck, scroll progress (0→1) drives:
//   1. copy lines lifting away at different depths, grid spreading apart
//   2. a parallax push into the TV screen — plate, foreground grass and dust
//      each travel at their own rate
//   3. static that builds on the curved TV glass itself, the closer we get
//   4. one continuous dive: the static fills the view, thins out, and we come out
//      the other side into the Squarezix universe (a starfield that rushes past on
//      arrival and settles to a drift)
// A single rAF loop runs while the hero is on screen; everything is reversible.
(() => {
  const hero = document.getElementById('hero');
  const stage = document.getElementById('hero-stage');
  if (!hero || !stage) return;

  const $ = (sel) => stage.querySelector(sel);
  const header = document.querySelector('.site-header');
  const media = $('.hero-media');
  const video = $('.hero-video');
  const fg = $('.hero-fg');
  const dust = $('.hero-dust');
  const grid = $('.hero-grid');
  const inner = $('.hero-inner');
  const crt = $('.hero-crt');
  const noise = $('.hero-noise');
  const screen = $('.hero-screen');
  const screenCanvas = $('.hero-screen-noise');
  const screenCtx = screenCanvas.getContext('2d');
  const lines = [...stage.querySelectorAll('.crt-line > span')];
  const ui = $('.crt-ui');
  const timecode = document.getElementById('crt-timecode');
  const fgCtx = fg.getContext('2d');
  const dustCtx = dust.getContext('2d');
  const noiseCtx = noise.getContext('2d', { alpha: true });
  const stars = $('.crt-stars');
  const starsCtx = stars.getContext('2d');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  // Copy elements and how "close to camera" each is — closer ones move further
  const depthEls = [
    ['.hero-badge', 0.55], ['.hero-title-main', 1.25], ['.hero-title-sub', 1.0],
    ['.hero-lead', 0.8], ['.hero-text', 0.65], ['.hero-cta', 0.9],
    ['.hero-services a:nth-child(1)', 1.5], ['.hero-services a:nth-child(2)', 1.3],
    ['.hero-services a:nth-child(3)', 1.1], ['.hero-services a:nth-child(4)', 0.9],
  ].map(([sel, depth]) => ({ el: $(sel), depth })).filter((d) => d.el);

  // Glass outline traced from the video, in plate px relative to the .hero-screen box
  // (which starts 6px left / 4px above the glass): bowed edges, rounded corners
  const GLASS = new Path2D('M21 7Q118 6 212 19Q224 21 225 32Q232 106 225 180Q224 192 212 192Q118 199.5 28 185Q16 184 15 172Q1 96 9 20Q10 7 21 7Z');

  // TV screen glass inside the 1920x1080 video frame (x 878–1100, y 338–535)
  const SCREEN = { cx: 989 / 1920, cy: 436.5 / 1080, w: 222 / 1920, h: 197 / 1080 };

  // One tone for every static layer: violet-grey, close to the brand. Returns ABGR.
  const tone = (v, a) => {
    const r = Math.min(255, v * 0.93 + 8) | 0;     // lilac-grey, like the glass static
    const g = (v * 0.86) | 0;                       // over the purple screen
    const b = Math.min(255, v * 0.98 + 20) | 0;
    return (a << 24) | (b << 16) | (g << 8) | r;
  };

  const clamp01 = (v) => Math.min(Math.max(v, 0), 1);
  const seg = (p, a, b) => clamp01((p - a) / (b - a));
  const easeInOut = (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);
  const easeOut = (t) => 1 - Math.pow(1 - t, 3);
  const easeIn = (t) => t * t * t;
  const bell = (p, a, peak, b) => (p < peak ? easeInOut(seg(p, a, peak)) : 1 - easeInOut(seg(p, peak, b)));

  let geo = null;
  let target = 0;
  let current = 0;
  let running = false;
  let inView = true;
  let particles = [];
  let noiseFrames = [];
  let noiseIndex = 0;
  let lastNoise = 0;
  let insideSince = 0;
  let screenImg = null;
  let colTilt = null;          // per-column row offset: the glass sits slightly rotated
  let colBulge = null;         // per-column barrel factor: rows bow like a convex tube
  let glassMask = null;        // the glass shape, feathered, at the canvas's resolution
  let lastScreenNoise = 0;
  let starField = [];
  let lastStarT = 0;

  // ---------- Setup ----------
  function measure() {
    media.style.transform = 'none';
    const s = stage.getBoundingClientRect();
    const m = media.getBoundingClientRect();
    const stickyTop = parseFloat(getComputedStyle(stage).top) || 0;
    const visTop = Math.max(0, header.offsetHeight - stickyTop);
    const visH = stage.offsetHeight - visTop;

    const px = m.left - s.left + SCREEN.cx * m.width;
    const py = m.top - s.top + SCREEN.cy * m.height;
    const origin = `${SCREEN.cx * 100}% ${SCREEN.cy * 100}%`;
    media.style.transformOrigin = origin;
    fg.style.transformOrigin = origin;

    geo = {
      stickyTop, visTop, visH,
      w: s.width, h: stage.offsetHeight,
      px, py,
      distance: Math.max(1, hero.offsetHeight - stage.offsetHeight),
      dx: s.width / 2 - px,
      dy: visTop + visH / 2 - py,
      scaleEnd: Math.max(s.width / (SCREEN.w * m.width), visH / (SCREEN.h * m.height)) * 1.25,
      screenW: SCREEN.w * m.width,              // glass width on screen at zoom 1
    };
    stage.style.setProperty('--vis-top', `${visTop}px`);

    // Foreground copy only needs to be as sharp as it'll ever look (it blurs)
    fg.width = Math.min(1280, Math.round(m.width));
    fg.height = Math.round(fg.width * (m.height / m.width));

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    dust.width = Math.round(s.width * dpr);
    dust.height = Math.round(stage.offsetHeight * dpr);
    dustCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
    seedParticles();

    buildNoise(s.width, visH);

    const sdpr = Math.min(window.devicePixelRatio || 1, 2);
    stars.width = Math.round(s.width * sdpr);
    stars.height = Math.round(visH * sdpr);
    starsCtx.setTransform(sdpr, 0, 0, sdpr, 0, 0);
    starField = Array.from({ length: s.width < 700 ? 140 : 260 }, () => newStar(Math.random()));
    render(current, performance.now());
  }

  function seedParticles() {
    const count = geo.w < 700 ? 40 : 80;
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * geo.w,
      y: geo.visTop + Math.random() * geo.visH,
      depth: 0.3 + Math.random() * 1.4,              // >1 = nearer the lens
      r: 0.4 + Math.random() * 1.1,
      a: 0.15 + Math.random() * 0.45,
      drift: 4 + Math.random() * 10,                 // px/s upward float
      phase: Math.random() * Math.PI * 2,
      tint: Math.random() < 0.3 ? '205,188,255' : '255,255,255',
    }));
  }

  // Pre-render a handful of static frames and cycle them — cheap and convincing
  function buildNoise(w, h) {
    const scale = w < 700 ? 2 : 2.5;
    noise.width = Math.max(1, Math.round(w / scale));
    noise.height = Math.max(1, Math.round(h / scale));
    const { width, height } = noise;
    noiseFrames = Array.from({ length: 6 }, () => {
      const img = noiseCtx.createImageData(width, height);
      const buf = new Uint32Array(img.data.buffer);
      const bandY = Math.random() * height;
      for (let y = 0; y < height; y++) {
        // Horizontal banding like a detuned signal
        const band = Math.abs(y - bandY) < height * 0.06 ? 1.35 : 1;
        const rowBias = 0.85 + Math.random() * 0.3;
        for (let x = 0; x < width; x++) {
          buf[y * width + x] = tone(Math.min(255, Math.random() * 255 * rowBias * band), 255);
        }
      }
      return img;
    });
  }

  // ---------- Frame ----------
  function progress() {
    const top = hero.getBoundingClientRect().top;
    return clamp01((geo.stickyTop - top) / geo.distance);
  }

  function render(p, now) {
    if (!geo) return;
    const still = reduceMotion.matches;

    // 1. Copy peels away in depth; grid columns spread like we're moving through them
    const out = easeInOut(seg(p, 0, 0.22));
    depthEls.forEach(({ el, depth }) => {
      el.style.translate = `0 ${(-out * 170 * depth).toFixed(1)}px`;
      el.style.opacity = (1 - clamp01(out * (0.7 + depth * 0.6))).toFixed(3);
    });
    inner.style.pointerEvents = out > 0.4 ? 'none' : '';
    grid.style.transform = `scaleX(${1 + out * 0.7})`;
    grid.style.opacity = 1 - out;

    // 2. Plate: centre the screen early, then an exponential push (constant-feeling speed)
    const centre = easeInOut(seg(p, 0.02, 0.45));
    const zt = easeInOut(seg(p, 0.02, 0.7));
    const zoom = Math.exp(Math.log(geo.scaleEnd) * zt);
    // Brief signal shake as the glass fills the view
    const shake = still ? 0 : bell(p, 0.54, 0.6, 0.66);
    const shakeX = (Math.random() - 0.5) * shake * 10;
    const shakeY = (Math.random() - 0.5) * shake * 4;
    media.style.transform =
      `translate3d(${(geo.dx * centre + shakeX).toFixed(2)}px, ${(geo.dy * centre + shakeY).toFixed(2)}px, 0) scale(${zoom.toFixed(4)})`;

    // Foreground grass: extra scale + drop so it sweeps past below the lens, defocusing
    const ft = seg(p, 0.005, 0.45);
    const fgOn = ft > 0 && ft < 1;
    fg.style.visibility = fgOn ? 'visible' : 'hidden';
    if (fgOn) {
      const e = easeIn(ft);
      fg.style.transform = `translate3d(0, ${(e * 22).toFixed(2)}%, 0) scale(${(1 + e * 1.6).toFixed(4)})`;
      fg.style.filter = `blur(${(e * 14).toFixed(1)}px)`;
      fg.style.opacity = (1 - seg(p, 0.3, 0.45)).toFixed(3);
      if (video.readyState >= 2) fgCtx.drawImage(video, 0, 0, fg.width, fg.height);
    }

    // Static on the TV glass: none until the screen is ~1.9× (about a fifth of the
    // viewport wide), then it thickens gradually with every step closer, reaching
    // dense snow just as the glass fills the view. The full-screen layer then carries
    // the same static on through, so it reads as one continuous signal.
    const zStart = 1.9;
    const zFull = geo.scaleEnd / 1.25;
    const near = clamp01(Math.log(zoom / zStart) / Math.log(zFull / zStart));
    const level = Math.pow(near, 1.7);
    if (level > 0.002 && p < 0.68) {
      const flicker = still ? 0 : (Math.random() - 0.5) * 0.04 * level;
      // Strength goes into the pixels' alpha, not CSS opacity: an opacity group on a
      // layer scaled this far gets tiled by the compositor and shows seams
      screen.style.visibility = 'visible';
      if (now - lastScreenNoise > 33 || still) {
        lastScreenNoise = now;
        drawScreenNoise(zoom, level, Math.min(0.85, Math.max(0, level * 0.85 + flicker)), now);
      }
    } else {
      screen.style.visibility = 'hidden';
    }

    // Dust: floats at rest, then streams outward from the screen as we push in
    drawDust(p, zt, now);

    // 3. Through the glass — no cut, no power-on. The static fills the view, the
    //    universe fades up underneath it as we keep moving forward, and the static
    //    thins to a low hiss.
    const arrive = easeInOut(seg(p, 0.62, 0.72));
    if (arrive > 0) {
      crt.style.visibility = 'visible';
      crt.style.opacity = arrive.toFixed(3);
      crt.style.transform = `scale(${(0.94 + 0.06 * arrive).toFixed(4)})`;   // still moving forward
      crt.style.filter = arrive < 1 ? `blur(${((1 - arrive) * 10).toFixed(1)}px)` : '';
      drawStars(p, now);
    } else {
      crt.style.visibility = 'hidden';
      crt.style.opacity = 0;
    }

    const cover = 0.8 * easeInOut(seg(p, 0.58, 0.64));
    const thin = easeOut(seg(p, 0.645, 0.74));
    const staticLevel = p < 0.645 ? cover : 0.8 + (0.1 - 0.8) * thin;
    const flick = still || staticLevel < 0.01 ? 0 : (Math.random() - 0.5) * 0.03;
    noise.style.opacity = Math.max(0, staticLevel + flick).toFixed(3);

    // 4. Headline rolls up line by line, then the viewfinder UI
    lines.forEach((el, i) => {
      const t = easeOut(seg(p, 0.72 + i * 0.05, 0.86 + i * 0.05));
      el.style.transform = `translate3d(0, ${((1 - t) * 115).toFixed(2)}%, 0)`;
    });
    ui.style.opacity = easeOut(seg(p, 0.82, 0.92)).toFixed(3);

    // Timecode runs while we're inside
    if (p > 0.74) {
      if (!insideSince) insideSince = now;
      const f = Math.floor((now - insideSince) / 40);
      const pad = (n) => String(n).padStart(2, '0');
      timecode.textContent = `00:${pad(Math.floor(f / 1500) % 60)}:${pad(Math.floor(f / 25) % 60)}:${pad(f % 25)}`;
    } else {
      insideSince = 0;
    }

    // Plate is hidden once the screen is on — stop decoding it
    if (p > 0.75 && !video.paused) video.pause();
    else if (p <= 0.75 && video.paused && !still) video.play().catch(() => {});

    // Swap static frames ~24fps
    if (parseFloat(noise.style.opacity) > 0.005 && (now - lastNoise > 42 || still)) {
      lastNoise = now;
      noiseIndex = (noiseIndex + 1) % noiseFrames.length;
      if (noiseFrames[noiseIndex]) noiseCtx.putImageData(noiseFrames[noiseIndex], 0, 0);
    }
  }

  // Live snow for the TV glass, bent to the tube: every row follows the glass's tilt and
  // barrel curve, and dark scanline gaps are drawn along those same curved rows.
  // Resolution follows the glass's on-screen size — fine grain far away, coarse CRT
  // snow up close.
  function drawScreenNoise(zoom, level, alpha, now) {
    const want = Math.round(Math.min(460, Math.max(90, (geo.screenW * zoom) / 2.2)));
    if (!screenImg || Math.abs(want / screenCanvas.width - 1) > 0.3) {
      screenCanvas.width = want;
      screenCanvas.height = Math.round(want * 200 / 234);         // element box is 234×200 plate px
      screenImg = screenCtx.createImageData(screenCanvas.width, screenCanvas.height);
      colTilt = new Float32Array(want);
      colBulge = new Float32Array(want);
      for (let x = 0; x < want; x++) {
        const xn = (x / (want - 1)) * 2 - 1;
        colTilt[x] = 0.06 * xn;                  // top edge drops ~14px across the glass
        colBulge[x] = 1 + 0.08 * xn * xn;        // rows arch like a convex screen
      }
      glassMask = document.createElement('canvas');
      glassMask.width = screenCanvas.width;
      glassMask.height = screenCanvas.height;
      const m = glassMask.getContext('2d');
      m.setTransform(glassMask.width / 234, 0, 0, glassMask.height / 200, 0, 0);
      m.filter = `blur(${Math.max(1, glassMask.width / 234 * 2.4)}px)`;  // soft rim
      m.fillStyle = '#fff';
      m.fill(GLASS);
    }
    const { width, height } = screenCanvas;
    const buf = new Uint32Array(screenImg.data.buffer);
    const rows = Math.round(Math.min(96, Math.max(28, height / 2.4)));
    const a = Math.round(alpha * 255);
    // Per-row brightness gives the streaky look; a tracking band rolls down the tube
    const bias = new Float32Array(rows + 2);
    const band = ((now * 0.00018) % 1.3 - 0.15) * rows;
    const bandH = rows * (0.05 + level * 0.06);
    for (let i = 0; i < bias.length; i++) {
      bias[i] = (0.8 + Math.random() * 0.35) * (Math.abs(i - band) < bandH ? 1.2 + level * 0.25 : 1);
    }
    for (let y = 0; y < height; y++) {
      const yn = (y / (height - 1)) * 2 - 1;
      const o = y * width;
      for (let x = 0; x < width; x++) {
        const r = ((yn - colTilt[x]) * colBulge[x] + 1) * 0.5 * rows;
        const ri = r < 0 ? 0 : r > rows ? rows : r | 0;
        const gap = r - ri < 0.38 ? 0.5 : 1;     // curved scanline gap
        buf[o + x] = tone(Math.min(255, Math.random() * 255 * bias[ri] * gap), a);
      }
    }
    screenCtx.putImageData(screenImg, 0, 0);
    // Keep only the glass
    screenCtx.globalCompositeOperation = 'destination-in';
    screenCtx.drawImage(glassMask, 0, 0);
    screenCtx.globalCompositeOperation = 'source-over';
  }

  // ---------- The universe: a starfield we fly through ----------
  function newStar(z) {
    return {
      x: (Math.random() * 2 - 1) * 1.2,
      y: (Math.random() * 2 - 1) * 1.2,
      z,                                        // 1 = far, → 0 = passing the lens
      r: 0.5 + Math.random() * 1.1,
      tint: Math.random() < 0.35 ? [205, 180, 255] : [240, 236, 255],
    };
  }

  function drawStars(p, now) {
    const w = geo.w;
    const h = geo.visH;
    const dt = lastStarT ? Math.min((now - lastStarT) / 1000, 1 / 20) : 1 / 60;
    lastStarT = now;
    // Rushing past on arrival, easing to a slow drift once we're inside
    const warp = 1 - easeOut(seg(p, 0.62, 0.9));
    const speed = reduceMotion.matches ? 0 : 0.04 + warp * 1.4;
    const cx = w / 2;
    const cy = h / 2;
    const f = Math.max(w, h) * 0.5;
    starsCtx.clearRect(0, 0, w, h);
    starsCtx.lineCap = 'round';
    for (const s of starField) {
      const pz = s.z;
      s.z -= speed * dt;
      if (s.z <= 0.04) Object.assign(s, newStar(1), { z: 1 });
      const sx = cx + (s.x / s.z) * f;
      const sy = cy + (s.y / s.z) * f;
      if (sx < -50 || sx > w + 50 || sy < -50 || sy > h + 50) { Object.assign(s, newStar(1)); continue; }
      const near = 1 - s.z;
      const alpha = Math.min(1, near * 1.3) * 0.9;
      const [r, g, b] = s.tint;
      starsCtx.strokeStyle = `rgba(${r},${g},${b},${alpha.toFixed(3)})`;
      starsCtx.lineWidth = s.r * (0.6 + near * 1.6);
      // Streak from where it was a moment ago — long at warp, a dot when drifting
      const tail = Math.min(pz, s.z + speed * 0.06);
      starsCtx.beginPath();
      starsCtx.moveTo(cx + (s.x / tail) * f, cy + (s.y / tail) * f);
      starsCtx.lineTo(sx + 0.01, sy);
      starsCtx.stroke();
    }
  }

  function drawDust(p, zt, now) {
    dustCtx.clearRect(0, 0, geo.w, geo.h);
    const alpha = 1 - seg(p, 0.5, 0.64);
    if (alpha <= 0) return;
    const t = now / 1000;
    const cx = geo.w / 2;
    const cy = geo.visTop + geo.visH / 2;
    const push = reduceMotion.matches ? zt * 4 : zt * 9;
    for (const d of particles) {
      const floatY = reduceMotion.matches ? 0 : ((t * d.drift * d.depth) % geo.visH);
      let y = d.y - floatY;
      if (y < geo.visTop) y += geo.visH;
      const x = d.x + Math.sin(t * 0.4 + d.phase) * 6 * d.depth;
      const k = 1 + push * d.depth;                          // nearer specks fly out faster
      const X = cx + (x - cx) * k;
      const Y = cy + (y - cy) * k;
      const r = d.r * (1 + zt * d.depth * 2.2);
      dustCtx.beginPath();
      dustCtx.fillStyle = `rgba(${d.tint},${(d.a * alpha).toFixed(3)})`;
      dustCtx.arc(X, Y, r, 0, Math.PI * 2);
      dustCtx.fill();
    }
  }

  function loop(now) {
    const diff = target - current;
    current = reduceMotion.matches || Math.abs(diff) < 0.0005 ? target : current + diff * 0.12;
    render(current, now);
    if (inView) requestAnimationFrame(loop);
    else running = false;
  }

  function start() {
    if (running || !geo) return;
    running = true;
    requestAnimationFrame(loop);
  }

  // ---------- Wiring ----------
  window.addEventListener('scroll', () => { if (geo) target = progress(); }, { passive: true });

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => { measure(); target = progress(); }, 120);
  });

  new IntersectionObserver(([entry]) => {
    inView = entry.isIntersecting;
    if (inView) start();
  }).observe(hero);

  if (reduceMotion.matches) video.pause();
  measure();
  current = target = progress();
  start();
  document.fonts.ready.then(() => { measure(); target = progress(); });
})();
