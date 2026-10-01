// Services section: heading word reveal, chip marquees, 3D fold cards.
(() => {
  const section = document.getElementById('services');

  // --- Split [data-reveal] text into words, then light them up with scroll.
  // Runs for every .svc-intro / .reveal-scope on the page. ---
  const intros = [...document.querySelectorAll('.svc-intro, .reveal-scope')].map((intro) => {
    const words = [];
    intro.querySelectorAll('[data-reveal]').forEach((el) => splitWords(el, words));
    return { intro, words };
  });

  function splitWords(el, words) {
    const wrap = (node) => {
      [...node.childNodes].forEach((child) => {
        if (child.nodeType === Node.TEXT_NODE) {
          const frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach((part) => {
            if (!part.trim()) return frag.append(part);
            const span = document.createElement('span');
            span.className = 'word';
            span.textContent = part;
            frag.append(span);
            words.push(span);
          });
          child.replaceWith(frag);
        } else if (child.nodeType === Node.ELEMENT_NODE) {
          // e.g. <em>growth</em>: reveal the element as one word
          child.classList.add('word');
          words.push(child);
        }
      });
    };
    wrap(el);
  }

  function reveal() {
    const vh = window.innerHeight;
    intros.forEach(({ intro, words }) => {
      const r = intro.getBoundingClientRect();
      // 0 when the intro enters the bottom of the screen, 1 when it's ~35% from the top
      const p = Math.min(Math.max((vh - r.top) / (vh * 0.65 + r.height * 0.5), 0), 1);
      const lit = p * words.length;
      words.forEach((w, i) => {
        w.style.setProperty('--o', (0.1 + 0.9 * Math.min(Math.max(lit - i, 0), 1)).toFixed(3));
      });
    });
  }
  window.addEventListener('scroll', reveal, { passive: true });
  window.addEventListener('resize', reveal);
  reveal();

  // --- Chip rows: clone groups so each row loops seamlessly ---
  function buildChips() {
    section.querySelectorAll('.chip-track').forEach((track) => {
      track.querySelectorAll('.chip-group[aria-hidden]').forEach((el) => el.remove());
      const group = track.querySelector('.chip-group');
      const w = group.getBoundingClientRect().width;
      const copies = Math.max(1, Math.ceil((track.parentElement.clientWidth * 2) / w));
      for (let i = 0; i < copies; i++) {
        const clone = group.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true');
        track.appendChild(clone);
      }
      track.style.setProperty('--chip-group-width', `${w}px`);
      track.style.setProperty('--chip-duration', `${w / 45}s`);
    });
  }
  document.fonts.ready.then(buildChips);
  let t;
  window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(buildChips, 150); });

  // --- Service cards: spring-driven 3D fold + cursor twist ---
  // Each card eases --open toward 0/1 with a slightly under-damped spring (a soft
  // settle, never a snap), and --tx/--ty toward the pointer. While hovered the card
  // also sways a little on its own, so it feels alive even with a still cursor.
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canHover = window.matchMedia('(hover: hover)').matches;
  const cards = [...section.querySelectorAll('.svc-card')].map((el) => ({
    el, open: 0, vel: 0, target: 0,
    tx: 0, ty: 0, ptx: 0, pty: 0, hover: false, phase: Math.random() * 6,
  }));
  let raf = 0;
  let last = 0;

  const STIFFNESS = 150;
  const DAMPING = 20;          // critical ≈ 24.5 — just under, for a gentle overshoot

  function frame(now) {
    const dt = Math.min((now - last) / 1000 || 1 / 60, 1 / 30);
    last = now;
    const t = now / 1000;
    let busy = false;

    cards.forEach((c) => {
      if (reduce) {
        c.open = c.target; c.vel = 0;
      } else {
        const acc = STIFFNESS * (c.target - c.open) - DAMPING * c.vel;
        c.vel += acc * dt;
        c.open += c.vel * dt;
      }

      // Pointer twist plus a slow self-sway while open
      const sway = reduce ? 0 : c.open;
      const goalY = c.hover ? c.pty + Math.sin(t * 1.1 + c.phase) * 1.6 * sway : 0;
      const goalX = c.hover ? c.ptx + Math.cos(t * 0.9 + c.phase) * 0.8 * sway : 0;
      const k = 1 - Math.pow(0.001, dt);                  // frame-rate independent ease
      c.ty += (goalY - c.ty) * k * 0.9;
      c.tx += (goalX - c.tx) * k * 0.9;

      const settled = Math.abs(c.target - c.open) < 0.0005 && Math.abs(c.vel) < 0.0005
        && Math.abs(c.tx) + Math.abs(c.ty) < 0.01 && !c.hover;
      if (settled) { c.open = c.target; c.tx = 0; c.ty = 0; }
      else busy = true;

      c.el.style.setProperty('--open', c.open.toFixed(4));
      c.el.style.setProperty('--tx', c.tx.toFixed(3));
      c.el.style.setProperty('--ty', c.ty.toFixed(3));
    });

    raf = busy ? requestAnimationFrame(frame) : 0;
  }
  const kick = () => {
    if (!raf) { last = performance.now(); raf = requestAnimationFrame(frame); }
  };
  const setOpen = (c, open) => {
    c.target = open ? 1 : 0;
    c.el.classList.toggle('is-open', open);
    kick();
  };

  cards.forEach((c) => {
    if (canHover) {
      c.el.addEventListener('pointerenter', () => { c.hover = true; setOpen(c, true); });
      c.el.addEventListener('pointerleave', () => {
        c.hover = false; c.ptx = 0; c.pty = 0;
        setOpen(c, false);
      });
      c.el.addEventListener('pointermove', (e) => {
        const r = c.el.getBoundingClientRect();
        const x = ((e.clientX - r.left) / r.width) * 2 - 1;     // -1…1
        const y = ((e.clientY - r.top) / r.height) * 2 - 1;
        c.pty = x * 5;                                           // twist left/right (deg)
        c.ptx = -y * 3;                                          // tip toward/away (deg)
        kick();
      });
    }
    c.el.addEventListener('focus', () => setOpen(c, true));
    c.el.addEventListener('blur', () => { if (!c.hover) setOpen(c, false); });
  });

  // Touch devices have no hover: open the card nearest the middle of the screen
  if (!canHover) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        const c = cards.find((card) => card.el === e.target);
        if (c) setOpen(c, e.isIntersecting);
      });
    }, { rootMargin: '-45% 0px -45% 0px' });
    cards.forEach((c) => io.observe(c.el));
  }
})();
