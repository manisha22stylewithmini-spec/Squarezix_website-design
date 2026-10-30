// Why SquareZix — horizontal scroll.
// Desktop/tablet: the section is made tall enough that scrolling down moves the card
// track sideways by exactly its overflow while .wu-pin stays stuck. A line across the
// card tops fills with progress; each card's dot (and icon) lights when the fill reaches
// it, and the intro's 01 / 06 counter follows. Phones: a native swipe strip drives the
// same line and dots.
(() => {
  const section = document.querySelector('.wu-h');
  if (!section) return;
  const pin = section.querySelector('.wu-pin');
  const rail = section.querySelector('.wu-rail');
  const move = section.querySelector('.wu-move');
  const cards = [...section.querySelectorAll('.wu-card')];
  const countNow = section.querySelector('.wu-count-now');
  const phone = window.matchMedia('(max-width: 700px)');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp01 = (v) => Math.min(Math.max(v, 0), 1);

  let g = null;
  let target = 0, current = 0, running = false;

  function measure() {
    section.style.height = '';
    move.style.transform = 'none';
    const lineW = move.querySelector('.wu-line').offsetWidth;
    // Where each card's dot sits along the line
    const dots = cards.map((c) => c.offsetLeft + parseFloat(getComputedStyle(c, '::before').left) + 6);
    if (phone.matches) {
      g = { phone: true, lineW, dots };
    } else {
      const travel = Math.max(0, move.scrollWidth - rail.clientWidth);
      const pinH = pin.offsetHeight;
      // 1px of scroll per 1px of travel, plus a short hold at each end
      const hold = window.innerHeight * 0.18;
      section.style.height = `${pinH + travel + hold * 2}px`;
      g = {
        phone: false, lineW, dots, travel, hold,
        stickyTop: parseFloat(getComputedStyle(pin).top) || 0,
        distance: Math.max(1, section.offsetHeight - pinH),
      };
    }
    target = progress();
    current = target;
    render(current);
  }

  function progress() {
    if (!g) return 0;
    if (g.phone) {
      const max = rail.scrollWidth - rail.clientWidth;
      return max > 0 ? clamp01(rail.scrollLeft / max) : 1;
    }
    const scrolled = g.stickyTop - section.getBoundingClientRect().top;
    return clamp01((scrolled - g.hold) / Math.max(1, g.distance - g.hold * 2));
  }

  function render(p) {
    if (!g) return;
    if (!g.phone) move.style.transform = `translate3d(${(-g.travel * p).toFixed(2)}px, 0, 0)`;
    // Line fill: starts just past the first dot so card 01 is lit from the outset
    const first = g.dots[0] / g.lineW;
    const fill = first + (1 - first) * p;
    section.style.setProperty('--wu-p', fill.toFixed(4));
    let lit = 0;
    cards.forEach((c, i) => {
      const on = fill * g.lineW >= g.dots[i] - 1;
      c.classList.toggle('is-lit', on);
      if (on) lit = i + 1;
    });
    if (countNow) countNow.textContent = String(Math.max(1, lit)).padStart(2, '0');
  }

  function loop() {
    const d = target - current;
    current = reduce || Math.abs(d) < 0.0005 ? target : current + d * 0.16;
    render(current);
    if (current !== target) requestAnimationFrame(loop);
    else running = false;
  }
  const kick = () => {
    target = progress();
    if (!running) { running = true; requestAnimationFrame(loop); }
  };

  window.addEventListener('scroll', () => { if (g && !g.phone) kick(); }, { passive: true });
  rail.addEventListener('scroll', () => { if (g && g.phone) kick(); }, { passive: true });
  let t;
  window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(measure, 150); });
  phone.addEventListener('change', measure);

  measure();
  document.fonts.ready.then(measure);
  window.addEventListener('load', measure);
})();
