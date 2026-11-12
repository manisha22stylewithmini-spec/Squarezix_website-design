// Hero hover parallax. The video plate (and the static that sits on the TV glass) drifts a little against the
// pointer while the copy drifts the other way, so the wall of TVs feels deeper. A slow idle drift keeps it alive
// at rest. The look-around settles to nothing as the push-in starts, so the glass and its static stay aligned.
(() => {
  const hero = document.getElementById('hero');
  const stage = document.getElementById('hero-stage');
  if (!hero || !stage) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
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
    stage.style.setProperty('--cp', (1 - ease(clamp(p / .22))).toFixed(3));   // the veil and glow behind the title leave with the copy
    const idle = reduce ? 0 : 1;
    stage.style.setProperty('--pxm', ((cx + Math.sin(now * .00033) * .35 * idle) * damp).toFixed(3));
    stage.style.setProperty('--pym', ((cy + Math.cos(now * .00027) * .3 * idle) * damp).toFixed(3));
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
