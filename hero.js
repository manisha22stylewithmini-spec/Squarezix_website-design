// Scroll-scrubbed hero: draws pre-extracted video frames onto a canvas
// based on how far the user has scrolled through the .hero section.
(() => {
  const hero = document.getElementById('hero');
  const canvas = document.getElementById('hero-canvas');
  const ctx = canvas.getContext('2d');
  const progressBar = document.getElementById('hero-progress-bar');
  const loader = document.getElementById('hero-loader');
  const loaderPct = document.getElementById('hero-loader-pct');

  const isMobile = window.matchMedia('(max-width: 768px)').matches;
  const FRAME_DIR = isMobile ? 'frames/mobile' : 'frames/desktop';
  const frameUrl = (i) => `${FRAME_DIR}/${String(i + 1).padStart(4, '0')}.${frameExt}`;

  let frameCount = 0;
  let frameExt = 'webp';
  const frames = [];       // HTMLImageElement | undefined
  let targetFrame = 0;     // where scroll says we should be
  let currentFrame = 0;    // smoothed position that eases toward target
  let lastDrawn = -1;

  // --- Canvas sizing (retina-aware) ---
  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(canvas.clientWidth * dpr);
    canvas.height = Math.round(canvas.clientHeight * dpr);
    lastDrawn = -1;
    render();
  }

  // Draw an image like CSS `object-fit: cover`
  function drawCover(img) {
    const cw = canvas.width, ch = canvas.height;
    const scale = Math.max(cw / img.naturalWidth, ch / img.naturalHeight);
    const w = img.naturalWidth * scale, h = img.naturalHeight * scale;
    ctx.drawImage(img, (cw - w) / 2, (ch - h) / 2, w, h);
  }

  // If the exact frame hasn't loaded yet, fall back to the nearest loaded one
  function nearestLoaded(index) {
    for (let d = 0; d < frameCount; d++) {
      if (frames[index - d]?.complete) return frames[index - d];
      if (frames[index + d]?.complete) return frames[index + d];
    }
    return null;
  }

  function render() {
    const index = Math.round(currentFrame);
    if (index === lastDrawn) return;
    const img = nearestLoaded(index);
    if (!img) return;
    drawCover(img);
    if (img === frames[index]) lastDrawn = index;
  }

  // --- Scroll → progress ---
  function getProgress() {
    const rect = hero.getBoundingClientRect();
    const scrollable = hero.offsetHeight - window.innerHeight;
    return Math.min(Math.max(-rect.top / scrollable, 0), 1);
  }

  function onScroll() {
    const p = getProgress();
    targetFrame = p * (frameCount - 1);
    progressBar.style.transform = `scaleX(${p})`;  }

  // --- Animation loop: ease currentFrame toward targetFrame ---
  function tick() {
    const diff = targetFrame - currentFrame;
    currentFrame = Math.abs(diff) < 0.01 ? targetFrame : currentFrame + diff * 0.2;
    render();
    requestAnimationFrame(tick);
  }

  // --- Loading: first frame immediately, then the rest ---
  function loadFrame(i) {
    return new Promise((resolve) => {
      const img = new Image();
      img.decoding = 'async';
      img.onload = img.onerror = () => resolve(img);
      img.src = frameUrl(i);
      frames[i] = img;
    });
  }

  async function init() {
    // frames/manifest.js sets window.HERO_FRAMES; fetch is only a fallback (it fails on file://)
    const res = window.HERO_FRAMES
      ? { json: async () => window.HERO_FRAMES }
      : await fetch('frames/manifest.json');
    ({ count: frameCount, ext: frameExt = 'webp' } = await res.json());

    await loadFrame(0);
    resize();
    onScroll();
    requestAnimationFrame(tick);

    let loaded = 1;
    const queue = Array.from({ length: frameCount - 1 }, (_, i) => i + 1);
    const worker = async () => {
      while (queue.length) {
        await loadFrame(queue.shift());
        loaded++;
        loaderPct.textContent = Math.round((loaded / frameCount) * 100);
        lastDrawn = -1; // redraw in case a better frame just arrived
      }
    };
    await Promise.all(Array.from({ length: 6 }, worker));
    loader.classList.add('done');
  }

  window.addEventListener('resize', resize);
  window.addEventListener('scroll', onScroll, { passive: true });
  init().catch((err) => {
    console.error('Hero frames failed to load. Run scripts/extract-frames.swift first.', err);
    loader.textContent = 'Frames missing — run scripts/extract-frames.swift';
  });
})();
