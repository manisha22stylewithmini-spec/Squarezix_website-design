// Hero: the video plate stays completely still behind the copy until the scroll animation takes over (no parallax).
// This only fades the veil and glow behind the title out with the copy as the push-in starts.
(() => {
  const hero = document.getElementById('hero');
  const stage = document.getElementById('hero-stage');
  if (!hero || !stage) return;
  const clamp = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
  const ease = (t) => (t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);
  function update() {
    const r = hero.getBoundingClientRect();
    const total = hero.offsetHeight - stage.offsetHeight;
    const p = total > 0 ? clamp(-r.top / total) : 0;
    stage.style.setProperty('--cp', (1 - ease(clamp(p / .22))).toFixed(3));
  }
  addEventListener('scroll', update, { passive: true });
  addEventListener('resize', update);
  update();
})();
