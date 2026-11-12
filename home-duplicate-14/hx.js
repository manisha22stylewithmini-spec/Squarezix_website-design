// Hero (blueprint grid). Three things move:
//  1. the giant type band loops sideways, and scrolling the page gives it a push (speed follows scroll velocity)
//  2. a three.js jack (three hollow tubes crossing) turns in the black cell; the pointer tilts it, scrolling spins it
//  3. the partner strip steps with the arrows and auto-advances
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const track = document.getElementById('hx-track');
  const hero = document.getElementById('hero');
  if (!track || !hero) return;

  // ---- 1. type band ----
  let x = 0, vel = 0, lastY = scrollY, tw = 0, inView = true;
  const measure = () => { tw = track.firstElementChild.offsetWidth * 2; };
  addEventListener('resize', measure); (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(measure); measure();

  // ---- 2. 3D jack ----
  const cv = document.getElementById('hx-canvas');
  let renderer, scene, cam, jack;
  if (window.THREE && cv) {
    const T = THREE;
    renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    scene = new T.Scene();
    cam = new T.PerspectiveCamera(32, 1, .1, 50); cam.position.set(0, 0, 9);
    scene.add(new T.HemisphereLight(0xffffff, 0x444458, .9));
    const key = new T.DirectionalLight(0xffffff, 1.5); key.position.set(3, 4, 5); scene.add(key);
    const rim = new T.DirectionalLight(0xab24f2, 1.1); rim.position.set(-4, -2, -3); scene.add(rim);
    // a hollow, softly rounded tube along Y, made with a lathe
    const R = .42, r = .24, L = 1.35, e = .1, pts = [];
    pts.push(new T.Vector2(r, L));
    pts.push(new T.Vector2(R - e, L)); for (let i = 0; i <= 6; i++) { const a = i / 6 * Math.PI / 2; pts.push(new T.Vector2(R - e + Math.sin(a) * e, L - e + Math.cos(a) * e)); }
    pts.push(new T.Vector2(R, -L + e)); for (let i = 0; i <= 6; i++) { const a = i / 6 * Math.PI / 2; pts.push(new T.Vector2(R - e + Math.cos(a) * e, -L + e - Math.sin(a) * e)); }
    pts.push(new T.Vector2(r, -L));
    const geo = new T.LatheGeometry(pts, 48);
    const mat = new T.MeshStandardMaterial({ color: 0xf1f1f4, roughness: .42, metalness: .08, side: T.DoubleSide });
    jack = new T.Group();
    const a = new T.Mesh(geo, mat), b = a.clone(), c = a.clone();
    b.rotation.z = Math.PI / 2; c.rotation.x = Math.PI / 2;
    jack.add(a, b, c);
    jack.rotation.set(.5, .6, 0);
    scene.add(jack);
  }
  const fit = () => { if (!renderer) return; const w = cv.clientWidth, h = cv.clientHeight; renderer.setSize(w, h, false); cam.aspect = w / h; cam.updateProjectionMatrix(); };
  addEventListener('resize', fit); fit();
  let px = 0, py = 0, cx = 0, cy = 0, spin = 0;
  hero.addEventListener('pointermove', (ev) => { const r = hero.getBoundingClientRect(); px = (ev.clientX - r.left) / r.width * 2 - 1; py = (ev.clientY - r.top) / r.height * 2 - 1; });

  // ---- 3. partner strip ----
  const lt = document.getElementById('hx-logos');
  let li = 0; const n = lt ? lt.children.length / 2 : 0;
  const step = (d) => { li = (li + d + n) % n; const w = lt.children[0].offsetWidth; lt.style.transform = `translateX(${-li * w}px)`; };
  const pv = document.getElementById('hx-prev'), nx = document.getElementById('hx-next');
  if (pv) pv.onclick = () => step(-1); if (nx) nx.onclick = () => step(1);
  if (lt && !reduce) setInterval(() => inView && step(1), 3200);

  new IntersectionObserver(([en]) => { inView = en.isIntersecting; }).observe(hero);

  let last = performance.now();
  (function loop(now) {
    const dt = Math.min(now - last, 50); last = now;
    if (inView) {
      const y = scrollY; vel += ((y - lastY) - vel) * .12; lastY = y;
      if (!reduce) x -= dt * (.07 + Math.min(Math.abs(vel), 60) * .012) * (vel < 0 ? -1 : 1);
      if (tw) { x = ((x % tw) - tw) % tw; track.style.transform = `translate3d(${x}px,0,0)`; }
      if (jack) {
        cx += (px - cx) * .06; cy += (py - cy) * .06;
        spin += dt * .0005 * (reduce ? 0 : 1) + vel * .004;
        jack.rotation.y = .6 + spin + cx * .5;
        jack.rotation.x = .5 + spin * .6 + cy * .4;
        renderer.render(scene, cam);
      }
    }
    requestAnimationFrame(loop);
  })(last);
})();
