// Hero (card wall). The cards sit on the inside of a sphere, every one facing the viewer. Two things move it:
//   pointer  -> the wall looks around (parallax), the card under the pointer lifts, the images slide against it
//   scroll   -> the camera pushes straight into the middle (hero) card; once it fills the view, the page inside
//               it keeps scrolling, slide by slide
// One rAF loop runs while the hero is on screen; everything is reversible.
(() => {
  const hero = document.getElementById('hero');
  const stage = hero && hero.querySelector('.wl-stage');
  const zoom = stage && stage.querySelector('.wl-zoom');
  const world = stage && stage.querySelector('.wl-world');
  const page = stage && stage.querySelector('.wl-page');
  const hint = stage && stage.querySelector('.wl-hint');
  if (!world || !page) return;

  const R = 1250, D = 2400;                    // sphere radius and camera distance (px)
  const CW = 520, CH = 325, GAP = 34;          // card size and the gap between cards
  const COLS = 4, ROWS = 3;                    // cards each way from the middle one
  const DTH = (CW + GAP) / R, DPH = (CH + GAP) / R;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;

  const WORK = [
    ['Digital Stream', 'A B2B SaaS site rebuilt to turn visitors into demos.', 'assets/work/project-1.png', '50% 40%'],
    ['Hero Gradients', 'A digital-goods storefront built to sell.', 'assets/work/project-2.png', '50% 50%'],
    ['Product Launch', 'AI software story, site and launch, end to end.', 'assets/work/project-3.png', '50% 50%'],
    ['Digital Marketing', 'Reels that make brands stop the scroll.', 'assets/reels/reel-1.jpg', '50% 38%'],
    ['Brand Voice', 'Say it once, so it sticks.', 'assets/reels/reel-2.jpg', '50% 50%'],
    ['Strategy', 'Without content, a brand is invisible.', 'assets/reels/reel-3.jpg', '50% 30%'],
    ['Content that pays', 'Reels, ads and social that earn their budget.', 'assets/reels/reel-4.jpg', '50% 22%'],
    ['GCC Growth', 'A playbook for scaling brands across the Gulf.', 'assets/blog/gcc-growth.jpg', '50% 36%'],
    ['AI Search', 'Be the answer when people ask AI.', 'assets/blog/ai-search.jpg', '50% 50%'],
    ['AI at Work', 'Where teams and AI actually meet.', 'assets/blog/ai-workplace.jpg', '50% 40%'],
    ['Dubai after dark', 'Campaigns for the city that never sleeps.', 'assets/hero/bench-shot.jpg', '55% 50%'],
  ];

  // ---------- build the wall ----------
  const place = (el, i, j) => {
    el.style.transform = `rotateY(${(-i * DTH).toFixed(4)}rad) rotateX(${(j * DPH).toFixed(4)}rad) translateZ(${-R}px)`;
  };
  const hero0 = world.querySelector('.wl-hero');
  place(hero0, 0, 0);
  for (let j = -ROWS; j <= ROWS; j++) {
    for (let i = -COLS; i <= COLS; i++) {
      if (!i && !j) continue;
      const w = WORK[(((i + COLS) * 3 + (j + ROWS) * 5) % WORK.length)];
      const card = document.createElement('article');
      card.className = 'wl-card';
      card.innerHTML = `<div class="wl-face"><img src="${w[2]}" alt="" style="object-position:${w[3]}" decoding="async" draggable="false" /><div class="wl-scrim"></div><div class="wl-cap"><h3>${w[0]}</h3><p>${w[1]}</p></div></div>`;
      place(card, i, j);
      world.appendChild(card);
    }
  }

  // ---------- state ----------
  const clamp = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
  const seg = (p, a, b) => clamp((p - a) / (b - a));
  const ease = (t) => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  let W, H, k, sEnd, pageMax;
  let tx = 0, ty = 0, cx = 0, cy = 0;          // pointer target / smoothed, each -1..1
  let running = false, inView = true;

  function measure() {
    W = stage.clientWidth; H = stage.clientHeight;
    const tw = Math.min(Math.max(W * (W < 700 ? .8 : .34), 290), 560);   // middle card width on screen at rest
    k = tw / (CW * (D / (D + R)));
    sEnd = (W * 1.04) / tw;                                              // card ends a touch wider than the stage
    pageMax = page.offsetHeight - CH;
  }

  function progress() {
    const r = hero.getBoundingClientRect();
    const total = hero.offsetHeight - stage.offsetHeight;
    return total > 0 ? clamp(-r.top / total) : 0;
  }

  function render(now) {
    const p = reduce ? 0 : progress();
    const drift = reduce ? 0 : 1;
    const ax = cx + Math.sin(now * .00042) * .3 * drift;
    const ay = cy + Math.cos(now * .00031) * .22 * drift;
    const damp = 1 - ease(seg(p, 0, .22));                                // look-around settles as we commit to the card

    world.style.transform = `rotateX(${(-ay * 2.6 * damp).toFixed(3)}deg) rotateY(${(ax * 3.4 * damp).toFixed(3)}deg)`;
    world.style.setProperty('--px', (ax * damp).toFixed(3));
    world.style.setProperty('--py', (ay * damp).toFixed(3));

    const z = Math.exp(Math.log(sEnd) * ease(seg(p, .03, .6)));
    zoom.style.transform = `scale(${(k * z).toFixed(4)})`;
    page.style.transform = `translate3d(0,${(-pageMax * ease(seg(p, .12, .94))).toFixed(1)}px,0)`;
    stage.style.setProperty('--vig', (1 - ease(seg(p, .1, .5))).toFixed(3));
    if (hint) hint.style.opacity = (1 - seg(p, 0, .07)).toFixed(3);
  }

  function loop(now) {
    cx += (tx - cx) * .07; cy += (ty - cy) * .07;
    render(now);
    if (inView) requestAnimationFrame(loop); else running = false;
  }
  function start() { if (!running) { running = true; requestAnimationFrame(loop); } }

  if (fine && !reduce) {
    stage.addEventListener('pointermove', (e) => {
      const r = stage.getBoundingClientRect();
      tx = ((e.clientX - r.left) / r.width) * 2 - 1;
      ty = ((e.clientY - r.top) / r.height) * 2 - 1;
      const face = e.target.closest && e.target.closest('.wl-face');
      if (face) {
        const f = face.getBoundingClientRect();
        face.style.setProperty('--mx', ((e.clientX - f.left) / f.width * 100).toFixed(1) + '%');
        face.style.setProperty('--my', ((e.clientY - f.top) / f.height * 100).toFixed(1) + '%');
      }
    });
    stage.addEventListener('pointerleave', () => { tx = 0; ty = 0; });
  }
  addEventListener('resize', measure);
  new IntersectionObserver(([en]) => { inView = en.isIntersecting; if (inView) start(); }).observe(hero);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
  measure();
  start();
})();
