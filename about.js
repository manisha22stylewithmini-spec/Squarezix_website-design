// About page: hero starfield, scroll reveals, word light-up, accordion, loops,
// process track, stat counters, card spotlight and the contact form.
(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp01 = (v) => Math.min(Math.max(v, 0), 1);

  // --- Hero starfield: the same universe the home page dives into, drifting slowly ---
  const hero = document.querySelector('.ab-hero');
  const canvas = document.querySelector('.ab-stars');
  if (hero && canvas) {
    const ctx = canvas.getContext('2d');
    let stars = [];
    let w = 0, h = 0, raf = 0, visible = true, last = 0;
    const newStar = (z) => ({
      x: (Math.random() * 2 - 1) * 1.2, y: (Math.random() * 2 - 1) * 1.2, z,
      r: 0.4 + Math.random() * 1.1, tint: Math.random() < 0.35 ? '205,180,255' : '240,236,255',
    });
    const size = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = hero.clientWidth; h = hero.clientHeight;
      canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      stars = Array.from({ length: w < 700 ? 110 : 220 }, () => newStar(Math.random()));
    };
    const draw = (now) => {
      const dt = last ? Math.min((now - last) / 1000, 1 / 20) : 1 / 60;
      last = now;
      const speed = reduce ? 0 : 0.035;
      const f = Math.max(w, h) * 0.5;
      ctx.clearRect(0, 0, w, h);
      for (const s of stars) {
        s.z -= speed * dt;
        if (s.z <= 0.05) Object.assign(s, newStar(1));
        const sx = w / 2 + (s.x / s.z) * f;
        const sy = h / 2 + (s.y / s.z) * f;
        if (sx < -20 || sx > w + 20 || sy < -20 || sy > h + 20) { Object.assign(s, newStar(1)); continue; }
        const near = 1 - s.z;
        ctx.fillStyle = `rgba(${s.tint},${(Math.min(1, near * 1.3) * 0.85).toFixed(3)})`;
        ctx.beginPath();
        ctx.arc(sx, sy, s.r * (0.5 + near * 1.3), 0, Math.PI * 2);
        ctx.fill();
      }
      raf = visible && !reduce ? requestAnimationFrame(draw) : 0;
    };
    size();
    requestAnimationFrame(draw);
    new IntersectionObserver(([e]) => {
      visible = e.isIntersecting;
      if (visible && !raf && !reduce) { last = 0; raf = requestAnimationFrame(draw); }
    }).observe(hero);
    let t; window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(() => { size(); if (reduce) draw(performance.now()); }, 150); });
  }

  // --- Rise-in on scroll; siblings stagger ---
  const risers = [...document.querySelectorAll('[data-rise]')];
  risers.forEach((el) => {
    const sibs = [...el.parentElement.children].filter((c) => c.hasAttribute('data-rise'));
    el.style.setProperty('--d', `${Math.min(sibs.indexOf(el), 5) * 0.08}s`);
  });
  const riseIO = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('is-in'); riseIO.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  risers.forEach((el) => riseIO.observe(el));

  // --- Headings light up word by word as they scroll into view ---
  const groups = [...document.querySelectorAll('[data-reveal]')].map((el) => {
    const words = [];
    [...el.childNodes].forEach((node) => {
      if (node.nodeType === Node.TEXT_NODE) {
        const frag = document.createDocumentFragment();
        node.textContent.split(/(\s+)/).forEach((part) => {
          if (!part.trim()) return frag.append(part);
          const span = document.createElement('span');
          span.className = 'word'; span.textContent = part;
          frag.append(span); words.push(span);
        });
        node.replaceWith(frag);
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        node.classList.add('word'); words.push(node);
      }
    });
    return { el, words };
  });

  // --- Process track fills with scroll; steps light as the line reaches them ---
  const steps = document.getElementById('ab-steps');
  const stepEls = steps ? [...steps.querySelectorAll('.ab-step')] : [];

  function onScroll() {
    const vh = window.innerHeight;
    groups.forEach(({ el, words }) => {
      const r = el.getBoundingClientRect();
      const p = clamp01((vh * 0.92 - r.top) / (vh * 0.45));
      const lit = p * words.length;
      words.forEach((w, i) => w.style.setProperty('--o', (0.12 + 0.88 * clamp01(lit - i)).toFixed(3)));
    });
    if (steps) {
      const r = steps.getBoundingClientRect();
      const p = reduce ? 1 : clamp01((vh * 0.85 - r.top) / (vh * 0.5));
      steps.style.setProperty('--fill', p.toFixed(3));
      stepEls.forEach((s, i) => s.classList.toggle('is-lit', p >= (i / stepEls.length) + 0.02));
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  // --- Accordion: one panel open at a time ---
  const acc = document.getElementById('ab-acc');
  if (acc) {
    const items = [...acc.querySelectorAll('.ab-acc-item')];
    items.forEach((item) => {
      item.querySelector('.ab-acc-head').addEventListener('click', () => {
        const open = !item.classList.contains('is-open');
        items.forEach((it) => {
          const on = it === item ? open : false;
          it.classList.toggle('is-open', on);
          it.querySelector('.ab-acc-head').setAttribute('aria-expanded', on);
        });
      });
    });
  }

  // --- Seamless loops (tech chips + partner badges) ---
  function loop(track, group, widthVar, durVar, pxPerSec) {
    const build = () => {
      track.querySelectorAll('[data-clone]').forEach((c) => c.remove());
      const gw = group.getBoundingClientRect().width;
      if (!gw) return;
      const copies = Math.max(1, Math.ceil((track.parentElement.clientWidth * 2) / gw));
      for (let i = 0; i < copies; i++) {
        const c = group.cloneNode(true);
        c.setAttribute('data-clone', ''); c.setAttribute('aria-hidden', 'true');
        track.appendChild(c);
      }
      track.style.setProperty(widthVar, `${gw}px`);
      track.style.setProperty(durVar, `${gw / pxPerSec}s`);
    };
    document.fonts.ready.then(build);
    let t; window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(build, 150); });
  }
  document.querySelectorAll('.ab-tech .chip-track').forEach((track) => {
    loop(track, track.querySelector('.chip-group'), '--chip-group-width', '--chip-duration', 40);
  });
  const partners = document.getElementById('ab-partners-track');
  if (partners) {
    // The shared `ribbon` keyframes read --ribbon-group-width
    loop(partners, partners.querySelector('.ab-partners-group'), '--ribbon-group-width', '--ab-partners-duration', 50);
  }

  // --- Stat counters in the hero ---
  document.querySelectorAll('[data-count]').forEach((el) => {
    const target = +el.dataset.count;
    const suffix = el.dataset.suffix || '';
    const fmt = (n) => n.toLocaleString('en-US') + suffix;
    if (reduce) { el.textContent = fmt(target); return; }
    el.textContent = fmt(0);
    const io = new IntersectionObserver(([e]) => {
      if (!e.isIntersecting) return;
      io.disconnect();
      const start = performance.now();
      const step = (now) => {
        const t = Math.min((now - start) / 1600, 1);
        el.textContent = fmt(Math.round(target * (1 - Math.pow(1 - t, 3))));
        if (t < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    });
    io.observe(el);
  });

  // --- Testimonial cards: soft light follows the cursor ---
  document.querySelectorAll('.ab-quote').forEach((card) => {
    card.addEventListener('pointermove', (e) => {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${e.clientX - r.left}px`);
      card.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  });

  // --- Contact form: validate, then hand off to the visitor's mail app ---
  // (No backend yet — swap the mailto for your form endpoint when one exists.)
  const form = document.getElementById('ab-form');
  if (form) {
    const note = document.getElementById('ab-form-note');
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let ok = true;
      form.querySelectorAll('[required]').forEach((input) => {
        const bad = !input.value.trim() || (input.type === 'email' && !/^\S+@\S+\.\S+$/.test(input.value));
        input.closest('.ab-field').classList.toggle('is-invalid', bad);
        if (bad && ok) { input.focus(); ok = false; }
      });
      if (!ok) { note.textContent = 'Please fill in the required fields.'; return; }
      const d = Object.fromEntries(new FormData(form));
      const body = `Name: ${d.name}\nEmail: ${d.email}\nPhone: ${d.phone}\n\n${d.message || ''}`;
      window.location.href = `mailto:info@squarezix.com?subject=${encodeURIComponent(`New enquiry from ${d.name}`)}&body=${encodeURIComponent(body)}`;
      note.textContent = 'Opening your email app…';
    });
    form.addEventListener('input', (e) => e.target.closest('.ab-field')?.classList.remove('is-invalid'));
  }
})();
