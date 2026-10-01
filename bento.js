// Bento grid: staggered reveal, animated project counter.
(() => {
  const bento = document.querySelector('.bento');
  if (!bento) return;


  // --- Staggered reveal when the grid scrolls into view ---
  const order = ['.b-strategy', '.b-hero', '.b-disc', '.b-tool', '.b-projects', '.b-laptop', '.b-expertise', '.b-grow', '.b-contact'];
  order.forEach((sel, i) => bento.querySelector(sel)?.style.setProperty('--delay', `${i * 0.08}s`));
  bento.classList.add('reveal');
  const io = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) return;
    bento.classList.add('is-in');
    countUp();
    io.disconnect();
  }, { threshold: 0.15 });
  io.observe(bento);

  // --- "120+" counts up once ---
  function countUp() {
    const el = bento.querySelector('.b-bracket');
    const target = 120;
    const start = performance.now();
    const step = (now) => {
      const t = Math.min((now - start) / 1400, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = `${Math.round(target * eased)}+ Projects Delivered`;
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }
})();
