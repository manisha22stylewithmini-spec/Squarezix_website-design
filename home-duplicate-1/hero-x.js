// Hero (lab): pointer parallax on the type and hairlines, and the radiating starburst.
// Runs only while the hero is on screen; with reduced motion it draws one still frame.
(() => {
  const hero = document.querySelector('.hx');
  if (!hero) return;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canHover = window.matchMedia('(hover: hover)').matches;
  const canvas = hero.querySelector('.hx-burst canvas');
  const ctx = canvas && canvas.getContext('2d');

  // ---- starburst: rays of different lengths that breathe and lean toward the pointer ----
  const RAYS = 56;
  const seed = Array.from({ length: RAYS }, (_, i) => {
    const r = Math.sin(i * 91.7) * 43758.5453;
    return { len: .5 + .5 * (r - Math.floor(r)), ph: i * 1.7, w: .6 + .6 * ((r * 7) - Math.floor(r * 7)) };
  });
  let W = 0, H = 0, dpr = 1;
  const size = () => {
    if (!canvas) return;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
  };
  let gx = 0, gy = 0, hover = false;     // pointer across the hero, -1…1 (drives the parallax)
  let rx = 0, ry = 0, qx = 0, qy = 0;    // pointer direction from the burst's centre: target and eased value
  const draw = (ms) => {
    if (!ctx || !W) return;
    const t = ms / 1000, cx = W / 2, cy = H / 2, R = Math.min(W, H) / 2;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    ctx.lineCap = 'round';
    const lean = Math.hypot(qx, qy);
    const pa = Math.atan2(qy, qx);
    for (let i = 0; i < RAYS; i++) {
      const a = (i / RAYS) * Math.PI * 2 + Math.sin(t * .25 + seed[i].ph) * .012;
      const toward = Math.max(0, Math.cos(a - pa)) * Math.min(1, lean * 1.3);
      const len = R * (seed[i].len * (.8 + Math.sin(t * .9 + seed[i].ph) * .12) + toward * .28);
      const inner = R * .04;
      const g = ctx.createLinearGradient(cx + Math.cos(a) * inner, cy + Math.sin(a) * inner, cx + Math.cos(a) * len, cy + Math.sin(a) * len);
      g.addColorStop(0, 'rgba(244, 238, 255, .95)');
      g.addColorStop(1, 'rgba(171, 36, 242, .05)');
      ctx.strokeStyle = g; ctx.lineWidth = seed[i].w;
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(a) * inner, cy + Math.sin(a) * inner);
      ctx.lineTo(cx + Math.cos(a) * len, cy + Math.sin(a) * len);
      ctx.stroke();
    }
    const core = ctx.createRadialGradient(cx, cy, 0, cx, cy, R * .09);
    core.addColorStop(0, 'rgba(255, 255, 255, .95)'); core.addColorStop(1, 'rgba(255, 255, 255, 0)');
    ctx.fillStyle = core; ctx.beginPath(); ctx.arc(cx, cy, R * .09, 0, Math.PI * 2); ctx.fill();
  };

  // ---- loop ----
  let raf = 0, onScreen = true;
  const frame = (ms) => {
    qx += (rx - qx) * .08; qy += (ry - qy) * .08;
    // idle drift when the pointer is away
    const drift = hover || reduce ? 0 : 1;
    const px = hover ? gx : Math.sin(ms / 3600) * .35 * drift;
    const py = hover ? gy : Math.cos(ms / 4300) * .3 * drift;
    hero.style.setProperty('--px', px.toFixed(3));
    hero.style.setProperty('--py', py.toFixed(3));
    draw(ms);
    raf = requestAnimationFrame(frame);
  };
  const sync = () => {
    const run = onScreen && !document.hidden && !reduce;
    if (run && !raf) raf = requestAnimationFrame(frame);
    if (!run && raf) { cancelAnimationFrame(raf); raf = 0; }
  };
  if (canHover && !reduce) {
    hero.addEventListener('pointermove', (e) => {
      if (e.pointerType !== 'mouse') return;
      const r = hero.getBoundingClientRect(), b = canvas.getBoundingClientRect();
      hover = true;
      gx = ((e.clientX - r.left) / r.width - .5) * 2; gy = ((e.clientY - r.top) / r.height - .5) * 2;
      // direction from the burst's centre to the pointer, for the rays
      const bx = e.clientX - (b.left + b.width / 2), by = e.clientY - (b.top + b.height / 2);
      const d = Math.hypot(bx, by) || 1, near = Math.max(0, 1 - d / (r.width * .6));
      rx = bx / d * near; ry = by / d * near;
    });
    hero.addEventListener('pointerleave', () => { hover = false; gx = gy = 0; rx = ry = 0; });
  }
  new IntersectionObserver((e) => { onScreen = e[e.length - 1].isIntersecting; sync(); }).observe(hero);
  document.addEventListener('visibilitychange', sync);
  window.addEventListener('resize', () => { size(); if (!raf) draw(performance.now()); });
  size(); draw(0); sync();
})();
