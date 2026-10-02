// Process clock (service pages): the section pins while the sweep hand goes once round the
// dial. Each stop lights as the hand reaches it and the minute hand settles on the current
// stop. The dial is a stack of layers that tilts toward the pointer, like the service cards.
(() => {
  const sec = document.querySelector('.svp-clock');
  if (!sec) return;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canHover = window.matchMedia('(hover: hover)').matches;
  const wrap = sec.querySelector('.svp-dial-wrap');
  const stops = [...sec.querySelectorAll('.svp-stop')];
  const marks = [...sec.querySelectorAll('.svp-marks i')];
  const details = [...sec.querySelectorAll('.svp-clock-detail')];
  const countNow = sec.querySelector('.svp-clock-count b');
  const n = stops.length;
  sec.classList.add('is-live');          // without JS the steps are simply listed

  let target = 0, p = 0, min = 0, active = -1, raf = 0, onScreen = false;
  let tx = 0, ty = 0, gx = 0, gy = 0, hover = false;      // tilt (deg) and its goal

  // Progress 0…1 across the pinned stretch, measured from the untransformed section box
  const span = () => sec.getBoundingClientRect().height - window.innerHeight;
  const measure = () => {
    const s = span();
    target = s > 0 ? Math.min(Math.max(-sec.getBoundingClientRect().top / s, 0), 1) : 0;
  };

  const paint = (now) => {
    raf = 0;
    p += (target - p) * (reduce ? 1 : 0.14);
    if (Math.abs(target - p) < 0.0005) p = target;
    const idx = Math.min(n - 1, Math.floor(p * n + 1e-6));
    const minGoal = idx * 360 / n;
    min += (minGoal - min) * (reduce ? 1 : 0.12);
    if (Math.abs(minGoal - min) < 0.05) min = minGoal;

    // Tilt: toward the pointer while hovered, otherwise a slow idle sway
    const t = (now || 0) / 1000;
    const swayX = hover || reduce ? gx : Math.sin(t * 0.6) * 5;
    const swayY = hover || reduce ? gy : Math.cos(t * 0.45) * 4;
    tx += (swayX - tx) * 0.08; ty += (swayY - ty) * 0.08;

    sec.style.setProperty('--p', p.toFixed(4));
    sec.style.setProperty('--sweep', `${(p * 360).toFixed(2)}deg`);
    sec.style.setProperty('--min', `${min.toFixed(2)}deg`);
    sec.style.setProperty('--hour', `${(300 + p * 60).toFixed(2)}deg`);   // creeps from 10 to 12: "done"
    sec.style.setProperty('--tx', tx.toFixed(2));
    sec.style.setProperty('--ty', ty.toFixed(2));

    if (idx !== active) {
      active = idx;
      const mark = (el, i) => { el.classList.toggle('is-done', i < idx); el.classList.toggle('is-active', i === idx); };
      stops.forEach(mark); marks.forEach(mark);
      details.forEach((d, i) => d.classList.toggle('is-active', i === idx));
      countNow.textContent = String(idx + 1).padStart(2, '0');
    }
    // Keep running while visible so the idle sway and tilt stay alive; stop otherwise
    if (onScreen && !reduce || p !== target || min !== minGoal) raf = requestAnimationFrame(paint);
  };

  const update = () => { measure(); if (!raf) raf = requestAnimationFrame(paint); };
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  new IntersectionObserver((entries) => { onScreen = entries[entries.length - 1].isIntersecting; update(); }).observe(sec);

  if (canHover && !reduce) {
    wrap.addEventListener('pointermove', (e) => {
      const r = wrap.getBoundingClientRect();
      hover = true;
      gx = ((e.clientX - r.left) / r.width - 0.5) * 22;
      gy = -((e.clientY - r.top) / r.height - 0.5) * 22;
    });
    wrap.addEventListener('pointerleave', () => { hover = false; });
  }

  // A stop is also a control: clicking it scrolls to that step
  stops.forEach((s, i) => s.querySelector('button').addEventListener('click', () => {
    const top = sec.getBoundingClientRect().top + window.scrollY;
    window.scrollTo({ top: top + span() * ((i + 0.35) / n), behavior: reduce ? 'auto' : 'smooth' });
  }));

  update();
})();
