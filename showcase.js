// Service page showcase: a pinned statement whose image tiles leave the sentence and land
// in the dock below as you scroll. One tile per sub-category, any number of them.
(() => {
  const sec = document.querySelector('.svb');
  if (!sec) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;   // static: images sit in the dock

  const pin = sec.querySelector('.svb-pin');
  const tiles = [...sec.querySelectorAll('.svb-tile')];
  const from = tiles.map((t) => sec.querySelector(`.svb-slot[data-i="${t.dataset.i}"]`));
  const to = tiles.map((t) => sec.querySelector(`.svb-dock-slot[data-i="${t.dataset.i}"]`));
  const labels = to.map((s) => s.parentElement.querySelector('.svb-dock-label'));
  const n = tiles.length;
  sec.classList.add('is-live');

  const clamp01 = (v) => Math.min(Math.max(v, 0), 1);
  const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  let target = 0, p = -1, raf = 0;

  const measure = () => {
    const r = sec.getBoundingClientRect();
    const span = r.height - window.innerHeight;
    target = span > 0 ? clamp01(-r.top / span) : 0;
  };

  const paint = () => {
    raf = 0;
    p = p < 0 ? target : p + (target - p) * 0.16;
    if (Math.abs(target - p) < 0.0005) p = target;

    // 0 → .25 the dock rises; .18 → .84 the tiles travel, each a beat after the last; then the paragraph
    sec.style.setProperty('--dock', ease(clamp01(p / 0.25)).toFixed(3));
    const pr = pin.getBoundingClientRect();
    const stagger = n > 1 ? 0.22 / (n - 1) : 0;
    tiles.forEach((tile, i) => {
      const t = ease(clamp01((p - 0.18 - i * stagger) / 0.44));
      const a = from[i].getBoundingClientRect(), b = to[i].getBoundingClientRect();
      const size = a.width + (b.width - a.width) * t;
      const x = a.left + (b.left - a.left) * t - pr.left;
      // a small arc: lift first, then drop into the dock
      const y = a.top + (b.top - a.top) * t - pr.top - Math.sin(t * Math.PI) * 26;
      tile.style.width = tile.style.height = `${size.toFixed(1)}px`;
      tile.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) rotate(${(Math.sin(t * Math.PI) * (i % 2 ? 6 : -6)).toFixed(2)}deg)`;
      labels[i].style.setProperty('--land', t > 0.96 ? 1 : 0);
    });
    if (p !== target) raf = requestAnimationFrame(paint);
  };

  const update = () => { measure(); if (!raf) raf = requestAnimationFrame(paint); };
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  window.addEventListener('load', update);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(update);   // the sentence reflows when fonts arrive
  update();
})();
