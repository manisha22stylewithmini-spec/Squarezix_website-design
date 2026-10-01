// Lens scroll (after andagain.uk): each [data-lens] section behaves like a panel on a
// curved glass sphere. Arriving from below it tilts back around the centre of the
// screen, shrinks a little and rounds its leading corners; it flattens to full size
// while it fills the view, then curves away over the top as it leaves. A small elastic
// stretch follows scroll speed. Pure transforms — text stays crisp, links and videos
// keep working. Positions come from cached layout (never from transformed rects), so
// there's no feedback loop.
(() => {
  const panels = [...document.querySelectorAll('[data-lens]')];
  if (!panels.length) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const clamp01 = (v) => Math.min(Math.max(v, 0), 1);
  const smooth = (t) => t * t * (3 - 2 * t);

  let layout = [];
  let vh = window.innerHeight, vw = window.innerWidth;
  let lastY = window.scrollY, velocity = 0, raf = 0;

  function docTop(el) {
    let y = 0;
    for (let n = el; n; n = n.offsetParent) y += n.offsetTop;
    return y;
  }

  function measure() {
    vh = window.innerHeight;
    vw = window.innerWidth;
    panels.forEach((el) => { el.style.transform = ''; el.style.clipPath = ''; });
    layout = panels.map((el) => ({ el, top: docTop(el), h: el.offsetHeight }));
    render();
  }

  function render() {
    const y = window.scrollY;
    const small = vw < 700;
    const ANGLE = small ? 10 : 16;           // max tilt (deg)
    const SHRINK = small ? 0.06 : 0.1;       // max scale loss
    const R = Math.min(vw * 0.09, 150);      // max corner radius (px)
    const skew = Math.max(-2.5, Math.min(2.5, velocity * 0.03));

    for (const p of layout) {
      const top = p.top - y;
      const bottom = top + p.h;
      if (bottom < -vh * 0.5 || top > vh * 1.5) continue;   // far off screen

      // k: 0 while the panel fills / sits centred in the view, → 1 as it leaves it
      let k, entering;
      if (p.h <= vh) {
        const c = top + p.h / 2;
        k = clamp01(Math.abs(c - vh / 2) / ((vh + p.h) / 2));
        entering = c > vh / 2;
      } else if (top > 0) {
        k = clamp01(top / vh); entering = true;
      } else if (bottom < vh) {
        k = clamp01((vh - bottom) / vh); entering = false;
      } else {
        k = 0; entering = true;
      }
      k = smooth(k);

      if (k < 0.001 && Math.abs(skew) < 0.02) {
        p.el.style.transform = '';
        p.el.style.clipPath = '';
        continue;
      }
      // Pivot on the centre line of the screen so the visible part curves like a sphere
      const originY = vh / 2 - top;
      const angle = (entering ? 1 : -1) * ANGLE * k;
      p.el.style.transformOrigin = `50% ${originY.toFixed(1)}px`;
      p.el.style.transform =
        `perspective(${(vh * 1.3).toFixed(0)}px) rotateX(${angle.toFixed(3)}deg) scale(${(1 - SHRINK * k).toFixed(4)}) skewY(${skew.toFixed(3)}deg)`;
      const r = R * k;
      p.el.style.clipPath = r > 0.5 ? `inset(0 round ${r.toFixed(1)}px)` : '';
    }
  }

  // Scroll speed eases back to zero, so the stretch settles when scrolling stops
  function tick() {
    const y = window.scrollY;
    const v = y - lastY;
    lastY = y;
    velocity += (v - velocity) * 0.2;
    render();
    if (Math.abs(velocity) > 0.05 || Math.abs(v) > 0) raf = requestAnimationFrame(tick);
    else { velocity = 0; render(); raf = 0; }
  }

  window.addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(tick); }, { passive: true });
  let t;
  window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(measure, 150); });
  // Sections above can change height as fonts, images and pinned sections settle
  window.addEventListener('load', measure);
  document.fonts.ready.then(measure);
  new ResizeObserver(() => { clearTimeout(t); t = setTimeout(measure, 150); }).observe(document.body);
  measure();
})();
