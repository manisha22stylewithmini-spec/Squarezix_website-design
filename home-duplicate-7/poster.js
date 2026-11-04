// Hero (campaign poster). While .pz-stage is stuck, scroll steps through four parts of a campaign:
//   Brand -> Content -> Campaign -> Growth. Each part swaps the giant word (letters drop in), the TV screen,
//   the stamp and the handwritten note, and pulls the puppet's arms to a new pose. Strings follow the hands.
// Idle motion (arm sway, head bob, flowers) runs while the hero is on screen.
(() => {
  const hero = document.getElementById('hero');
  const stage = hero && hero.querySelector('.pz-stage');
  if (!stage) return;
  const $ = (id) => document.getElementById(id);
  const fig = $('pz-fig'), tv = $('pz-tv'), headEl = stage.querySelector('.pz-head');
  const tagEl = $('pz-tag'), wordEl = $('pz-word'), stampEl = $('pz-stamp'), stampT = $('pz-stamp-t');
  const noteEl = $('pz-note'), noteT = $('pz-note-t'), countEl = $('pz-count');
  const slides = [...stage.querySelectorAll('.pz-slide')];
  const lines = [...$('pz-strings').querySelectorAll('line')];
  const arms = { L: { arm: $('pz-armL'), fore: $('pz-foreL'), s: [190, 322] }, R: { arm: $('pz-armR'), fore: $('pz-foreR'), s: [410, 322] } };
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const STAGES = [
    { tag: 'Start with a', word: 'Brand', stamp: '01 · Brief', note: 'your name, your look,\nbuilt once and used everywhere' },
    { tag: 'Feed it with', word: 'Content', stamp: '02 · Create', note: 'one idea, cut into posts,\nreels and stories' },
    { tag: 'Launch it as a', word: 'Campaign', stamp: '03 · Launch', note: 'live where your audience\nalready scrolls' },
    { tag: 'Watch it turn into', word: 'Growth', stamp: '04 · Scale', note: 'every click measured,\nevery dirham counted' },
  ];
  // arm poses: upper-arm angle, forearm bend (deg, svg rotate) for [left, right]
  const POSES = [[-34, -8, 34, 8], [-64, -18, 22, 10], [-24, 8, 66, 18], [-52, -26, 52, 26]];

  const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v);
  const lerp = (a, b, t) => a + (b - a) * t;
  const rot = (x, y, d) => { const r = d * Math.PI / 180, c = Math.cos(r), s = Math.sin(r); return [x * c - y * s, x * s + y * c]; };

  let W, H, fx, fy, fw, fh, idx = -1, pose = POSES[0].slice(), target = POSES[0], p = 0;

  // ---------- flowers & ground ----------
  function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; };
  const PURPLES = ['#8a3dea', '#a35cf2', '#6a2cc4', '#c490ff', '#b36cf7'];
  function leaf(x, y, a, s) { return `<ellipse cx="${x}" cy="${y}" rx="${5 * s}" ry="${15 * s}" transform="rotate(${a} ${x} ${y})" fill="${a % 2 ? '#2f4b34' : '#46664a'}"/>`; }
  function cluster(x, base, len, r) {
    const top = base - len; let g = `<path d="M${x} ${base} Q${x + (r() - .5) * 26} ${base - len / 2} ${x} ${top}" stroke="#35523b" stroke-width="3" fill="none" stroke-linecap="round"/>`;
    g += leaf(x - 8, base - len * .4, -50, 1) + leaf(x + 8, base - len * .55, 50, .9);
    const n = 6 + (r() * 4 | 0);
    for (let i = 0; i < n; i++) g += `<circle cx="${(x + (r() - .5) * 30).toFixed(1)}" cy="${(top + (r() - .5) * 26).toFixed(1)}" r="${(6 + r() * 5).toFixed(1)}" fill="${PURPLES[r() * PURPLES.length | 0]}"/>`;
    return g;
  }
  function daisy(x, base, len, r) {
    const top = base - len; let g = `<path d="M${x} ${base} Q${x + (r() - .5) * 20} ${base - len / 2} ${x} ${top}" stroke="#35523b" stroke-width="3" fill="none" stroke-linecap="round"/>`;
    g += leaf(x + 7, base - len * .45, 55, .9);
    for (let i = 0; i < 9; i++) g += `<ellipse cx="${x}" cy="${top - 14}" rx="6" ry="15" transform="rotate(${i * 40} ${x} ${top})" fill="#fff" stroke="#e7def7" stroke-width=".8"/>`;
    return g + `<circle cx="${x}" cy="${top}" r="8" fill="#f6c445"/>`;
  }
  function grass(x, base, len, r) {
    const l = len * (.6 + r() * .6), b = (r() - .5) * 40;
    return `<path d="M${x - 5} ${base} Q${x + b / 2} ${base - l / 2} ${x + b} ${base - l} Q${x + b / 2 + 4} ${base - l / 2} ${x + 5} ${base} Z" fill="${r() > .5 ? '#2f4b34' : '#3d6143'}"/>`;
  }
  function build(elId, vbH, seed, count, ground) {
    const el = $(elId), r = rng(seed), VW = 1600;
    let s = `<svg viewBox="0 0 ${VW} ${vbH}" preserveAspectRatio="xMidYMax slice" aria-hidden="true">`;
    if (ground) {
      let pts = `0,${vbH} `; const top = vbH * .5;
      for (let x = 0; x <= VW; x += 80) pts += `${x},${(top + Math.sin(x / 210) * 14 + (r() - .5) * 22).toFixed(1)} `;
      pts += `${VW},${vbH}`;
      s += `<defs><linearGradient id="g-ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#241638"/><stop offset=".5" stop-color="#120c20"/><stop offset="1" stop-color="#0a0a15"/></linearGradient></defs><polygon points="${pts}" fill="url(#g-ground)"/>`;
    }
    for (let i = 0; i < count; i++) {
      const x = (i + .5) / count * VW + (r() - .5) * (VW / count), base = vbH - 8 - r() * (ground ? 50 : 14), len = (ground ? 60 : 30) + r() * (ground ? 110 : 80);
      const k = r(), body = k < .42 ? cluster(x, base, len, r) : k < .72 ? daisy(x, base, len, r) : grass(x, base, len * 1.2, r);
      s += `<g class="pz-fw" style="animation-duration:${(3.6 + r() * 2.6).toFixed(2)}s;animation-delay:-${(r() * 5).toFixed(2)}s">${body}</g>`;
    }
    el.innerHTML = s + '</svg>';
  }
  build('pz-fl-back', 240, 11, 42, true);
  build('pz-fl-front', 170, 29, 30, false);

  // ---------- word ----------
  function setWord(text) {
    const n = text.length;
    wordEl.innerHTML = '<span class="pz-wi">' + [...text].map((c, i) => `<span class="pz-l" style="--i:${i};--n:${n}">${c}</span>`).join('') + '</span>';
    fitWord();
  }
  function fitWord() {
    wordEl.style.fontSize = '100px';
    const wi = wordEl.firstElementChild, w = (wi && wi.getBoundingClientRect().width) || 1;
    const size = Math.min(100 * (W * .86) / w, H * .26);
    wordEl.style.fontSize = size.toFixed(1) + 'px';
  }

  // ---------- stage switching ----------
  function retrigger(el, cls) { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); }
  function setStage(i) {
    if (i === idx) return;
    idx = i;
    const s = STAGES[i];
    tagEl.textContent = s.tag; retrigger(tagEl, 'in');
    setWord(s.word);
    stampT.textContent = s.stamp; retrigger(stampEl, 'slam');
    noteT.textContent = s.note; retrigger(noteEl, 'in');
    slides.forEach((el) => el.classList.toggle('is-on', +el.dataset.s === i));
    countEl.textContent = String(i + 1).padStart(2, '0');
    target = POSES[i];
  }

  // ---------- puppet ----------
  function toStage(x, y) { return [fx + x / 600 * fw, fy + y / 830 * fh]; }
  function drawFigure(t) {
    const idle = reduce ? 0 : 1;
    const sway = (ph, a) => Math.sin(t * 1.15 + ph) * a * idle;
    for (let i = 0; i < 4; i++) pose[i] += (target[i] - pose[i]) * (reduce ? 1 : .07);
    const hands = [];
    ['L', 'R'].forEach((k, j) => {
      const a = arms[k], a1 = pose[j * 2] + sway(j * 2.1, 3), a2 = pose[j * 2 + 1] + sway(j * 2.1 + 1, 4);
      a.arm.setAttribute('transform', `translate(${a.s[0]} ${a.s[1]}) rotate(${a1.toFixed(2)})`);
      a.fore.setAttribute('transform', `translate(0 -110) rotate(${a2.toFixed(2)})`);
      const e = rot(0, -110, a1), h = rot(0, -162, a1 + a2);
      hands.push([a.s[0] + e[0] + h[0], a.s[1] + e[1] + h[1]]);
    });
    const bob = Math.sin(t * 1.6) * (reduce ? 0 : 1);
    tv.style.transform = `translateY(${(bob * -.4).toFixed(2)}%) rotate(${(Math.sin(t * .9) * 1.3 * (reduce ? 0 : 1)).toFixed(2)}deg)`;

    // strings: stage top -> hands, antenna tips, knees
    const ends = [hands[0], hands[1], [246, 27], [346, 30], [225, 640]].map(([x, y]) => toStage(x, y));
    const tops = [.22, .22, .5, .5, .3].map((m, i) => [lerp(ends[i][0], W / 2, m) + Math.sin(t * .8 + i) * 5 * idle, -12]);
    lines.forEach((ln, i) => { ln.setAttribute('x1', tops[i][0].toFixed(1)); ln.setAttribute('y1', tops[i][1]); ln.setAttribute('x2', ends[i][0].toFixed(1)); ln.setAttribute('y2', ends[i][1].toFixed(1)); });
  }

  function measure() {
    W = stage.clientWidth; H = stage.clientHeight;
    const sr = stage.getBoundingClientRect(), r = fig.getBoundingClientRect();
    fx = r.left - sr.left; fy = r.top - sr.top; fw = r.width; fh = r.height;
    fitWord();
  }
  function progress() {
    const r = hero.getBoundingClientRect(), total = hero.offsetHeight - stage.offsetHeight;
    return total > 0 ? clamp(-r.top / total) : 0;
  }
  function onScroll() {
    p = progress();
    setStage(reduce ? 0 : Math.min(3, Math.floor(p * 4)));
    headEl.style.transform = `translate3d(0,${(-p * 50).toFixed(1)}px,0)`;
  }

  let inView = true, running = false;
  function loop(now) {
    drawFigure(now / 1000);
    if (inView) requestAnimationFrame(loop); else running = false;
  }
  function start() { if (!running) { running = true; requestAnimationFrame(loop); } }
  new IntersectionObserver(([e]) => { inView = e.isIntersecting; if (inView) start(); }).observe(hero);

  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', () => { measure(); });
  measure(); onScroll(); setStage(Math.min(3, Math.floor(p * 4)));
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { measure(); fitWord(); });
  start();
})();
