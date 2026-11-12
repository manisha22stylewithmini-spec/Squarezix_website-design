// Hero scene: builds the stars and the far skyline, and runs the parallax. Moving the pointer slides the layers
// against each other (far layers barely, near ones more); a slow drift keeps it alive at rest. The look-around
// settles to nothing as the push-in starts, so the laptop glass and the static on it stay exactly aligned.
(() => {
  const media = document.querySelector('.hero-media');
  const hero = document.getElementById('hero');
  const stage = document.getElementById('hero-stage');
  if (!media || !hero || !stage) return;
  const NS = 'http://www.w3.org/2000/svg';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  let seed = 7;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
  const mk = (tag, attrs) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); return e; };

  const stars = document.getElementById('hs-stars');
  if (stars) {
    for (let i = 0; i < 260; i++) {
      const y = Math.pow(rnd(), 1.5) * 450;
      const c = mk('circle', { cx: (rnd() * 1280).toFixed(1), cy: y.toFixed(1), r: (0.25 + rnd() * rnd() * 1.1).toFixed(2), fill: rnd() < .2 ? '#cdb8ff' : '#fff', opacity: (0.25 + rnd() * .7).toFixed(2) });
      if (rnd() < .16) { c.classList.add('tw'); c.style.animationDelay = (rnd() * 5).toFixed(2) + 's'; }
      stars.appendChild(c);
    }
  }

  const sky = document.getElementById('hs-skyline');
  if (sky) {
    let x = 36;
    while (x < 470) {
      const w = 6 + rnd() * 16, h = 8 + rnd() * rnd() * 46, base = 486;
      sky.appendChild(mk('rect', { x: x.toFixed(1), y: (base - h).toFixed(1), width: w.toFixed(1), height: h.toFixed(1) }));
      const n = Math.floor(h / 7);
      for (let j = 0; j < n; j++) if (rnd() < .38) sky.appendChild(mk('rect', { x: (x + 1.5 + rnd() * (w - 3.5)).toFixed(1), y: (base - h + 3 + j * 6.4).toFixed(1), width: '1', height: '1.4', fill: '#ffb36a', opacity: (0.5 + rnd() * .5).toFixed(2) }));
      x += w + 1.5 + rnd() * 4;
    }
    sky.appendChild(mk('polygon', { points: '324,486 327.6,430 328.8,402 329.6,382 330.4,402 331.6,430 336,486' }));
    sky.appendChild(mk('rect', { x: '326', y: '440', width: '8', height: '46' }));
    sky.appendChild(mk('rect', { x: '329.2', y: '378', width: '0.8', height: '14', fill: '#ffd7a0', opacity: '.8' }));
  }

  // ---- parallax ----
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  let tx = 0, ty = 0, cx = 0, cy = 0, inView = true, running = false;
  const clamp = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
  const ease = (t) => (t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);

  function frame(now) {
    cx += (tx - cx) * .06; cy += (ty - cy) * .06;
    const r = hero.getBoundingClientRect();
    const total = hero.offsetHeight - stage.offsetHeight;
    const p = total > 0 ? clamp(-r.top / total) : 0;
    const damp = 1 - ease(clamp(p / .06));
    const idle = reduce ? 0 : 1;
    const ax = (cx + Math.sin(now * .00033) * .35 * idle) * damp;
    const ay = (cy + Math.cos(now * .00027) * .3 * idle) * damp;
    media.style.setProperty('--pxm', ax.toFixed(3));
    media.style.setProperty('--pym', ay.toFixed(3));
    if (inView) requestAnimationFrame(frame); else running = false;
  }
  const start = () => { if (!running) { running = true; requestAnimationFrame(frame); } };

  if (fine && !reduce) {
    stage.addEventListener('pointermove', (e) => {
      const b = stage.getBoundingClientRect();
      tx = ((e.clientX - b.left) / b.width) * 2 - 1;
      ty = ((e.clientY - b.top) / b.height) * 2 - 1;
    });
    stage.addEventListener('pointerleave', () => { tx = 0; ty = 0; });
  }
  new IntersectionObserver(([en]) => { inView = en.isIntersecting; if (inView) start(); }).observe(hero);
  start();
})();
