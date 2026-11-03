// Script-writing line on the portal sign: each message is typed out, held, rubbed out, then the
// next one is written. Sits inside .hero-media so it zooms with the plate.
(() => {
  const el = document.querySelector('.sign-type');
  if (!el) return;
  const lines = ['And you still looked.', 'An ad in the middle\nof nowhere.'];
  const TYPE = 58, ERASE = 22, HOLD = 1900, GAP = 320;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { el.textContent = lines[0]; return; }
  let i = 0;
  const text = el.firstChild || el.appendChild(document.createTextNode(''));
  const type = (n) => {
    const s = lines[i];
    text.nodeValue = s.slice(0, n);
    if (n < s.length) setTimeout(() => type(n + 1), TYPE + (s[n] === ' ' ? 30 : 0));
    else setTimeout(() => erase(n), HOLD);
  };
  const erase = (n) => {
    const s = lines[i];
    text.nodeValue = s.slice(0, n);
    if (n > 0) setTimeout(() => erase(n - 1), ERASE);
    else { i = (i + 1) % lines.length; setTimeout(() => type(1), GAP); }
  };
  setTimeout(() => type(1), 700);
})();
