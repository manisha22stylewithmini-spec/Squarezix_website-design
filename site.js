// Header (mobile menu) + infinite services marquee.
(() => {
  // --- Mobile menu toggle ---
  const toggle = document.getElementById('menu-toggle');
  const header = document.querySelector('.site-header');
  toggle.addEventListener('click', () => {
    const open = header.classList.toggle('menu-open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });

  // --- Glass header after the first scroll ---
  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // --- Marquee: clone the group until it overfills the screen twice,
  // so translating by exactly one group width loops with no visible seam ---
  const track = document.getElementById('marquee-track');
  if (!track) return;                    // pages without the marquee strip
  const group = track.querySelector('.marquee-group');

  function build() {
    track.querySelectorAll('.marquee-group[aria-hidden]').forEach((el) => el.remove());
    const groupWidth = group.getBoundingClientRect().width;
    const copies = Math.max(1, Math.ceil((window.innerWidth * 2) / groupWidth));
    for (let i = 0; i < copies; i++) {
      const clone = group.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      track.appendChild(clone);
    }
    track.style.setProperty('--group-width', `${groupWidth}px`);
    // Constant speed (px/sec) regardless of how long the text is
    track.style.setProperty('--marquee-duration', `${groupWidth / 90}s`);
  }

  document.fonts.ready.then(build);
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(build, 150);
  });
})();
