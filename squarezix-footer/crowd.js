// SquareZix footer crowd — a dependency-free port of minima's crowd.js
// (originally GSAP-driven). Peeps from the CC0 "Open Peeps" set walk across
// the footer, re-inked in Mist so they sit on the dark SquareZix field.
(() => {
  const canvas = document.querySelector("[data-sz-crowd]");
  if (!canvas) return;

  const config = {
    src: canvas.dataset.src || "open-peeps-sheet.avif",
    rows: 15,
    cols: 7,
    ink: "#c9bfe0", // Mist — line colour
    fill: "#1b0f33", // Mid Field — body colour
  };

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const ctx = canvas.getContext("2d");
  const stage = { width: 0, height: 0 };
  const rand = (min, max) => min + Math.random() * (max - min);
  const easeIn = (t) => t * t; // skews offsets low so peeps' missing legs stay hidden

  let sheet; // recoloured sprite sheet
  let peeps = [];
  let crowd = [];
  let last = 0;
  let running = false;

  const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));

  // The sprites are black ink on white fill. Re-ink them for the dark field:
  // ink -> Mist, fill -> Mid Field, alpha preserved.
  function recolour(img) {
    const c = document.createElement("canvas");
    c.width = img.naturalWidth;
    c.height = img.naturalHeight;
    const g = c.getContext("2d");
    g.drawImage(img, 0, 0);
    try {
      const data = g.getImageData(0, 0, c.width, c.height);
      const px = data.data;
      const ink = hex(config.ink);
      const fill = hex(config.fill);
      for (let i = 0; i < px.length; i += 4) {
        const t = px[i] / 255; // 0 = ink, 1 = fill
        px[i] = ink[0] + (fill[0] - ink[0]) * t;
        px[i + 1] = ink[1] + (fill[1] - ink[1]) * t;
        px[i + 2] = ink[2] + (fill[2] - ink[2]) * t;
      }
      g.putImageData(data, 0, 0);
      return c;
    } catch {
      // Cross-origin sheet without CORS: fall back to compositing (fill goes black).
    }
    g.globalCompositeOperation = "difference";
    g.fillStyle = "#fff";
    g.fillRect(0, 0, c.width, c.height);
    g.globalCompositeOperation = "multiply";
    g.fillStyle = config.ink;
    g.fillRect(0, 0, c.width, c.height);
    g.globalCompositeOperation = "destination-in";
    g.drawImage(img, 0, 0);
    return c;
  }

  function createPeeps() {
    const w = sheet.width / config.rows;
    const h = sheet.height / config.cols;
    const total = config.rows * config.cols;
    peeps = Array.from({ length: total }, (_, i) => ({
      sx: (i % config.rows) * w,
      sy: ((i / config.rows) | 0) * h,
      w,
      h,
    }));
  }

  function scaleFor() {
    // Peep height relative to the strip height; smaller screens get smaller peeps.
    const base = stage.height / peeps[0].h;
    return window.innerWidth < 480 ? base * 0.8 : base * 0.95;
  }

  // Place a walker at the edge (or anywhere, when `spread`), heading across.
  function launch(peep, spread) {
    const s = scaleFor();
    const w = peep.w * s;
    const h = peep.h * s;
    const dir = Math.random() > 0.5 ? 1 : -1;
    const startX = dir === 1 ? -w : stage.width + w;
    const endX = dir === 1 ? stage.width + w : -w;
    const offsetY = stage.height * (0.45 - 0.55 * easeIn(Math.random()));
    const y = stage.height - h + offsetY;
    const duration = 10 / rand(0.5, 1.5); // seconds, as in minima
    const walker = {
      peep,
      s,
      dir,
      startX,
      endX,
      y,
      duration,
      t: spread ? Math.random() : 0,
    };
    return walker;
  }

  function populate() {
    const pool = peeps.slice().sort(() => Math.random() - 0.5);
    // Density scales with width so narrow screens aren't a wall of people.
    const count = Math.min(pool.length, Math.round(stage.width / 22));
    crowd = pool.slice(0, count).map((p) => launch(p, true));
    crowd.sort((a, b) => a.y - b.y);
  }

  function resize() {
    stage.width = canvas.clientWidth;
    stage.height = canvas.clientHeight;
    canvas.width = stage.width * devicePixelRatio;
    canvas.height = stage.height * devicePixelRatio;
    if (peeps.length) {
      populate();
      draw();
    }
  }

  function step(dt) {
    for (let i = 0; i < crowd.length; i++) {
      const wk = crowd[i];
      wk.t += dt / wk.duration;
      if (wk.t >= 1) crowd[i] = launch(wk.peep, false);
    }
    crowd.sort((a, b) => a.y - b.y);
  }

  function draw() {
    ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
    ctx.clearRect(0, 0, stage.width, stage.height);
    for (const wk of crowd) {
      const { peep, s, dir } = wk;
      const x = wk.startX + (wk.endX - wk.startX) * wk.t;
      // Bob: 0.25s up/down cycles, 10px, like minima's yoyo tween.
      const bob = reduceMotion.matches
        ? 0
        : Math.abs(Math.sin((wk.t * wk.duration * Math.PI) / 0.25)) * 10 * s;
      ctx.save();
      ctx.translate(x, wk.y - bob);
      ctx.scale(dir * s, s);
      ctx.drawImage(sheet, peep.sx, peep.sy, peep.w, peep.h, dir === 1 ? 0 : -peep.w, 0, peep.w, peep.h);
      ctx.restore();
    }
    // Fade the crowd's top edge into the field.
    const fade = ctx.createLinearGradient(0, 0, 0, stage.height * 0.35);
    fade.addColorStop(0, "rgba(10,7,20,1)");
    fade.addColorStop(1, "rgba(10,7,20,0)");
    ctx.fillStyle = fade;
    ctx.fillRect(0, 0, stage.width, stage.height * 0.35);
  }

  function tick(now) {
    if (!running) return;
    const dt = Math.min((now - last) / 1000, 0.1);
    last = now;
    step(dt);
    draw();
    requestAnimationFrame(tick);
  }

  function start() {
    if (running || reduceMotion.matches) return;
    running = true;
    last = performance.now();
    requestAnimationFrame(tick);
  }

  function stop() {
    running = false;
  }

  function init(img) {
    sheet = recolour(img);
    createPeeps();
    resize();

    // Only animate while the footer is on screen.
    new IntersectionObserver(([entry]) =>
      entry.isIntersecting ? start() : stop()
    ).observe(canvas);

    window.addEventListener("resize", resize);
    reduceMotion.addEventListener("change", () =>
      reduceMotion.matches ? (stop(), draw()) : start()
    );
  }

  const img = new Image();
  img.decoding = "async";
  img.onload = () => init(img);
  img.src = config.src;
})();
