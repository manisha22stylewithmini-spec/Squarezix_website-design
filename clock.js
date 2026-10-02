// Process clock (service pages): the section pins while the sweep hand goes once round the
// dial. Each stop lights as the hand reaches it; the minute hand settles on the current stop.
(() => {
  const sec = document.querySelector('.svp-clock');
  if (!sec) return;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const stops = [...sec.querySelectorAll('.svp-stop')];
  const details = [...sec.querySelectorAll('.svp-clock-detail')];
  const countNow = sec.querySelector('.svp-clock-count b');
  const n = stops.length;
  sec.classList.add('is-live');          // without JS the steps are simply listed

  let target = 0, p = 0, min = 0, active = -1, raf = 0;

  // Progress 0…1 across the pinned stretch, measured from the untransformed section box
  const measure = () => {
    const r = sec.getBoundingClientRect();
    const span = r.height - window.innerHeight;
    target = span > 0 ? Math.min(Math.max(-r.top / span, 0), 1) : 0;
  };

  const paint = () => {
    raf = 0;
    p += (target - p) * (reduce ? 1 : 0.14);
    if (Math.abs(target - p) < 0.0005) p = target;
    const idx = Math.min(n - 1, Math.floor(p * n + 1e-6));
    const minGoal = idx * 360 / n;
    min += (minGoal - min) * (reduce ? 1 : 0.12);
    if (Math.abs(minGoal - min) < 0.05) min = minGoal;

    sec.style.setProperty('--p', p.toFixed(4));
    sec.style.setProperty('--sweep', `${(p * 360).toFixed(2)}deg`);
    sec.style.setProperty('--min', `${min.toFixed(2)}deg`);
    sec.style.setProperty('--hour', `${(300 + p * 60).toFixed(2)}deg`);   // creeps from 10 to 12: "done"

    if (idx !== active) {
      active = idx;
      stops.forEach((s, i) => { s.classList.toggle('is-done', i < idx); s.classList.toggle('is-active', i === idx); });
      details.forEach((d, i) => d.classList.toggle('is-active', i === idx));
      countNow.textContent = String(idx + 1).padStart(2, '0');
    }
    if (p !== target || min !== minGoal) raf = requestAnimationFrame(paint);
  };

  const update = () => { measure(); if (!raf) raf = requestAnimationFrame(paint); };
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
})();
