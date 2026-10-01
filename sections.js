// Why us spotlight · Work-flow accordion · Selected-work ribbons · Partners loop
(() => {
  // --- Why us: spotlight follows the cursor inside each cell ---
  document.querySelectorAll('.wu-cell').forEach((cell) => {
    cell.addEventListener('pointermove', (e) => {
      const r = cell.getBoundingClientRect();
      cell.style.setProperty('--mx', `${e.clientX - r.left}px`);
      cell.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  });

  // --- Work flow: accordion that auto-advances; hover pauses, click selects ---
  const list = document.getElementById('wf-steps');
  if (list) {
    const steps = [...list.querySelectorAll('.wf-step')];
    const DURATION = 5000;
    list.style.setProperty('--wf-duration', `${DURATION}ms`);
    let current = 0;
    let timer = null;
    let userPicked = false;

    const open = (i) => {
      steps.forEach((s, j) => {
        const active = j === i;
        s.classList.toggle('is-active', active);
        s.querySelector('.wf-head').setAttribute('aria-expanded', active);
        // restart the progress bar animation
        const bar = s.querySelector('.wf-progress');
        bar.style.animation = 'none'; void bar.offsetWidth; bar.style.animation = '';
      });
      current = i;
    };
    const schedule = () => {
      clearTimeout(timer);
      if (userPicked) return;
      timer = setTimeout(() => { open((current + 1) % steps.length); schedule(); }, DURATION);
    };

    steps.forEach((s, i) => s.querySelector('.wf-head').addEventListener('click', () => {
      userPicked = true;           // once the visitor chooses, stop auto-advancing
      clearTimeout(timer);
      list.classList.add('is-paused');
      open(i);
    }));
    list.addEventListener('pointerenter', () => { list.classList.add('is-paused'); clearTimeout(timer); });
    list.addEventListener('pointerleave', () => {
      if (userPicked) return;
      list.classList.remove('is-paused');
      schedule();
    });

    // Only run the timer while the section is on screen
    new IntersectionObserver((entries) => {
      const e = entries[entries.length - 1];   // latest state if several changes were batched
      if (e.isIntersecting && !userPicked) { list.classList.remove('is-paused'); open(current); schedule(); }
      else { clearTimeout(timer); list.classList.add('is-paused'); }
    }, { threshold: 0.35 }).observe(list);
  }

  // --- Seamless loops: fill a track with enough copies of a group ---
  function loop(track, groupEl, widthVar, durationVar, pxPerSec, onBuild) {
    const build = () => {
      track.querySelectorAll('[data-clone]').forEach((c) => c.remove());
      const w = groupEl.getBoundingClientRect().width;
      if (!w) return;
      const copies = Math.ceil((track.parentElement.clientWidth * 2) / w);
      for (let i = 0; i < copies; i++) {
        const c = groupEl.cloneNode(true);
        c.setAttribute('data-clone', ''); c.setAttribute('aria-hidden', 'true');
        track.appendChild(c);
      }
      track.style.setProperty(widthVar, `${w}px`);
      track.style.setProperty(durationVar, `${w / pxPerSec}s`);
      onBuild?.();
    };
    document.fonts.ready.then(build);
    let t; window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(build, 150); });
  }

  // Ribbons: the crafts behind the Selected Work cards (wording from the design)
  const services = ['Landing page', 'Motion design', 'Logo design', 'Framer development', 'Dashboard design'];
  document.querySelectorAll('.ribbon-track').forEach((track, i) => {
    const ul = document.createElement('ul');
    const items = i === 0 ? services : [...services].reverse();
    items.forEach((s) => { const li = document.createElement('li'); li.textContent = s; ul.appendChild(li); });
    track.appendChild(ul);
    loop(track, ul, '--ribbon-group-width', '--ribbon-duration', 70);
  });

  const partners = document.getElementById('partners-track');
  if (partners) loop(partners, partners.querySelector('.partners-group'), '--ribbon-group-width', '--partners-duration', 60);

  // --- CTA: giant faded words looping behind the heading ---
  const ctaTrack = document.getElementById('cta-loop-track');
  if (ctaTrack) {
    const group = document.createElement('div');
    group.style.display = 'flex';
    ['Found First', 'Built to Grow', 'Seen Everywhere'].forEach((w) => {
      const s = document.createElement('span'); s.textContent = w; group.appendChild(s);
    });
    ctaTrack.appendChild(group);
    loop(ctaTrack, group, '--ribbon-group-width', '--cta-duration', 60);
  }
  const year = document.getElementById('ft-year');
  if (year) year.textContent = new Date().getFullYear();

  // --- Where we show up: cursor parallax ---
  // The pointer position (-1…1) is eased into --mx/--my; CSS moves each depth layer from those.
  const stage = document.getElementById('wwsu-stage');
  if (stage && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    let tx = 0, ty = 0, cx = 0, cy = 0, raf = null, visible = false, hovering = false;
    const t0 = performance.now();
    const tick = (now) => {
      if (!hovering) {
        // Idle drift (also what touch devices see) so the scene never feels frozen
        const t = (now - t0) / 1000;
        tx = Math.sin(t * 0.35) * 0.45;
        ty = Math.cos(t * 0.27) * 0.35;
      }
      cx += (tx - cx) * 0.07;
      cy += (ty - cy) * 0.07;
      stage.style.setProperty('--mx', cx.toFixed(4));
      stage.style.setProperty('--my', cy.toFixed(4));
      raf = visible ? requestAnimationFrame(tick) : null;
    };
    // Track the pointer across the whole section, not just the stage, so the scene reacts early
    const zone = stage.closest('section');
    zone.addEventListener('pointermove', (e) => {
      if (e.pointerType !== 'mouse') return;
      const r = stage.getBoundingClientRect();
      hovering = true;
      tx = Math.max(-1, Math.min(1, ((e.clientX - r.left) / r.width) * 2 - 1));
      ty = Math.max(-1, Math.min(1, ((e.clientY - r.top) / r.height) * 2 - 1));
    });
    zone.addEventListener('pointerleave', () => { hovering = false; });
    // Only animate while on screen
    new IntersectionObserver((entries) => {
      visible = entries[entries.length - 1].isIntersecting;
      if (visible && !raf) raf = requestAnimationFrame(tick);
    }).observe(stage);
  }

  // --- Reels: endless phone row; videos only play while the section is on screen ---
  const reels = document.getElementById('reels-track');
  if (reels) {
    const section = document.getElementById('reels');
    const row = reels.parentElement;
    let onScreen = false;
    const inView = new Set();                   // phones currently inside the visible strip

    // A video plays only when the section is on screen AND its phone is inside the strip —
    // the loop needs many copies of the row, but only ~11 phones are ever visible.
    const syncVideo = (v) => {
      if (onScreen && inView.has(v)) {
        v.preload = 'auto';
        v.muted = true;                         // required for autoplay
        v.play().catch(() => {});               // poster stays if autoplay is blocked
      } else if (!v.paused) {
        v.pause();
      }
    };
    const syncAll = () => reels.querySelectorAll('video').forEach(syncVideo);

    const phoneIO = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        e.isIntersecting ? inView.add(e.target) : inView.delete(e.target);
        syncVideo(e.target);
      });
    }, { root: row, rootMargin: '0px 120px' }); // start a phone just before it slides in

    // Never show a black phone: the poster sits behind each video as the screen's background,
    // and the video only fades in once it is actually rendering frames. If a browser refuses
    // autoplay (Safari Low Power Mode, data saver) or a clip is still loading, the poster stays.
    const paintPosters = () => reels.querySelectorAll('video').forEach((v) => {
      if (!v.previousElementSibling?.classList.contains('reel-poster')) {
        const img = document.createElement('img');
        img.className = 'reel-poster'; img.alt = ''; img.src = v.getAttribute('poster');
        v.before(img);
      }
      if (v.readyState >= 2 && !v.paused) v.classList.add('is-live');
    });
    reels.addEventListener('playing', (e) => e.target.classList.add('is-live'), true);
    reels.addEventListener('error', (e) => e.target.classList?.remove('is-live'), true);

    // Re-observe after each rebuild so freshly cloned phones are tracked too
    loop(reels, reels.querySelector('.reels-group'), '--ribbon-group-width', '--reels-duration', 32, () => {
      paintPosters();
      phoneIO.disconnect();
      inView.clear();
      reels.querySelectorAll('video').forEach((v) => phoneIO.observe(v));
    });
    paintPosters();

    // Several changes can arrive in one batch (e.g. fast scrolling) — the last entry is the current state
    new IntersectionObserver((entries) => {
      onScreen = entries[entries.length - 1].isIntersecting;
      syncAll();
    }, { threshold: 0.15 }).observe(section);
  }
})();
