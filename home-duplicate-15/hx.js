// Hero (blueprint grid, dark). One robot, built in three.js, scrubbed by scroll through the pinned stage:
//   rest: small, in the right-hand cell  ->  forward and front-on  ->  big and turned side-on  ->  filling the stage from above/behind
// The giant type loops behind it (speed follows scroll velocity). The robot's eyes follow the pointer and blink.
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hero = document.getElementById('hero');
  const track = document.getElementById('hx-track');
  const cv = document.getElementById('hx-canvas');
  if (!hero || !track) return;
  const T = window.THREE;
  const small = () => matchMedia('(max-width: 900px)').matches;

  // ---------- type band ----------
  let x = 0, vel = 0, lastY = scrollY, tw = 0, inView = true;
  const measure = () => { tw = track.firstElementChild.offsetWidth * 2; };
  addEventListener('resize', measure); (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(measure); measure();

  // ---------- partner strip ----------
  const lt = document.getElementById('hx-logos');
  let li = 0; const n = lt ? lt.children.length / 2 : 0;
  const step = (d) => { li = (li + d + n) % n; lt.style.transform = `translateX(${-li * lt.children[0].offsetWidth}px)`; };
  const pv = document.getElementById('hx-prev'), nx = document.getElementById('hx-next');
  if (pv) pv.onclick = () => step(-1); if (nx) nx.onclick = () => step(1);
  if (lt && !reduce) setInterval(() => inView && step(1), 3200);
  new IntersectionObserver(([en]) => { inView = en.isIntersecting; }).observe(hero);

  // ---------- robot ----------
  let renderer, scene, cam, rig, bot, screenCtx, screenTex, eyeX = 0, eyeY = 0, blink = 0;
  if (T && cv) {
    renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    scene = new T.Scene();
    cam = new T.PerspectiveCamera(32, 1, .1, 60); cam.position.set(0, 0, 9);
    scene.add(new T.HemisphereLight(0xffffff, 0x3a2a66, .85));
    const key = new T.DirectionalLight(0xffffff, 1.6); key.position.set(3, 4, 6); scene.add(key);
    const rim = new T.DirectionalLight(0xab24f2, 1.4); rim.position.set(-5, 1, -4); scene.add(rim);
    const glow = new T.PointLight(0xc061ff, 1.8, 7); glow.position.set(0, -.2, 2.4); scene.add(glow);

    const rr = (w, h, r) => { const s = new T.Shape(), a = -w / 2, b = -h / 2; s.moveTo(a + r, b); s.lineTo(-a - r, b); s.quadraticCurveTo(-a, b, -a, b + r); s.lineTo(-a, -b - r); s.quadraticCurveTo(-a, -b, -a - r, -b); s.lineTo(a + r, -b); s.quadraticCurveTo(a, -b, a, -b - r); s.lineTo(a, b + r); s.quadraticCurveTo(a, b, a + r, b); return s; };
    const ext = (shape, d, bev) => { const g = new T.ExtrudeGeometry(shape, { depth: d, bevelEnabled: true, bevelThickness: bev, bevelSize: bev, bevelSegments: 4, curveSegments: 10 }); g.translate(0, 0, -d / 2); return g; };
    const box = (w, h, d, r, bev, color, rough = .45) => new T.Mesh(ext(rr(w - 2 * bev, h - 2 * bev, Math.max(r - bev, .01)), d - 2 * bev, bev), new T.MeshStandardMaterial({ color, roughness: rough, metalness: .05 }));
    const white = 0xf3f2f7, grey = 0xd6d4de;

    bot = new T.Group();
    const head = box(2.2, 2.0, 1.7, .4, .1, white); bot.add(head);
    // glowing C ring
    const ringShape = rr(2.0 - .2, 1.8 - .2, .36); const hole = rr(1.74, 1.52, .26); ringShape.holes.push(new T.Path(hole.getPoints(14).reverse()));
    const ringMat = new T.MeshStandardMaterial({ color: 0xab24f2, emissive: 0x9a2cf0, emissiveIntensity: 1.4, roughness: .35 });
    const ring = new T.Mesh(ext(ringShape, .08, .04), ringMat); ring.position.z = .9; bot.add(ring);
    const gap = box(.34, .56, .16, .1, .04, white); gap.position.set(.9, -.02, .93); bot.add(gap);
    const bezel = box(1.72, 1.52, .16, .3, .04, 0xe9e7f0); bezel.position.z = .93; bot.add(bezel);
    // screen: a canvas texture (dark grid + two eyes)
    const sc = document.createElement('canvas'); sc.width = sc.height = 256; screenCtx = sc.getContext('2d');
    screenTex = new T.CanvasTexture(sc); screenTex.anisotropy = 4;
    const screen = new T.Mesh(new T.PlaneGeometry(1.44, 1.3), new T.MeshBasicMaterial({ map: screenTex, transparent: true }));
    screen.position.z = 1.03; bot.add(screen);
    // ears
    [-1, 1].forEach((sx) => { const e = new T.Mesh(new T.CylinderGeometry(.22, .22, .4, 28), new T.MeshStandardMaterial({ color: grey, roughness: .4 })); e.rotation.z = Math.PI / 2; e.position.set(sx * 1.3, -.1, 0); bot.add(e); });
    // back module with a dark blueprint panel
    const mod = box(.95, 1.75, .75, .22, .06, white); mod.position.set(.75, .05, -1.2); bot.add(mod);
    const pc = document.createElement('canvas'); pc.width = 128; pc.height = 256; const px = pc.getContext('2d');
    px.fillStyle = '#16121f'; px.fillRect(0, 0, 128, 256); px.strokeStyle = 'rgba(200,190,230,.55)'; px.lineWidth = 2;
    for (let i = 0; i < 14; i++) { const yy = 14 + i * 17; px.beginPath(); px.moveTo(14, yy); px.lineTo(14 + 20 + (i * 37) % 80, yy); px.stroke(); }
    for (let i = 0; i < 5; i++) { px.strokeRect(20 + i * 18, 30 + (i * 41) % 120, 14, 40); }
    const panel = new T.Mesh(new T.PlaneGeometry(.62, 1.4), new T.MeshBasicMaterial({ map: new T.CanvasTexture(pc) })); panel.rotation.y = Math.PI / 2; panel.position.set(.75 + .5, .05, -1.2); bot.add(panel);
    const panelL = panel.clone(); panelL.rotation.y = -Math.PI / 2; panelL.position.x = .75 - .5; bot.add(panelL);
    // neck / body / base / cable
    const body = box(1.9, 1.3, 1.55, .32, .08, 0xe2e0ea); body.position.y = -1.65; bot.add(body);
    const base = box(2.8, .38, 2.1, .16, .05, 0xcdcad8); base.position.y = -2.5; bot.add(base);
    const cable = new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3([new T.Vector3(.3, 1.0, -1.1), new T.Vector3(-.2, .5, -1.55), new T.Vector3(-.3, -.6, -1.5), new T.Vector3(0, -1.5, -1.1)]), 40, .055, 8), new T.MeshStandardMaterial({ color: 0xdedce6, roughness: .5 }));
    bot.add(cable);
    bot.position.y = .75;
    rig = new T.Group(); rig.add(bot); scene.add(rig);
  }

  const drawScreen = (t) => {
    const c = screenCtx; if (!c) return; const W = 256;
    c.clearRect(0, 0, W, W);
    c.save(); c.beginPath(); c.roundRect(0, 0, W, W, 44); c.clip();
    const g = c.createLinearGradient(0, 0, 0, W); g.addColorStop(0, '#1d0a22'); g.addColorStop(1, '#0d0615'); c.fillStyle = g; c.fillRect(0, 0, W, W);
    c.strokeStyle = 'rgba(255,140,220,.32)'; c.lineWidth = 1.4;
    for (let i = 1; i < 8; i++) { const p = i * W / 8; c.beginPath(); c.moveTo(p, 0); c.lineTo(p, W); c.stroke(); c.beginPath(); c.moveTo(0, p); c.lineTo(W, p); c.stroke(); }
    const open = blink > 0 ? Math.max(.08, 1 - Math.sin(blink * Math.PI)) : 1;
    c.fillStyle = '#fff'; c.shadowColor = '#ffd6ff'; c.shadowBlur = 18;
    [-1, 1].forEach((s) => { c.beginPath(); c.ellipse(W / 2 + s * 36 + eyeX * 20, W / 2 + eyeY * 14, 15, 17 * open, 0, 0, 7); c.fill(); });
    c.restore(); screenTex.needsUpdate = true;
  };

  // scroll keyframes: [progress, ndcX, ndcY, scale, rotY, rotX]
  const KF = [[0, .74, -.34, .42, -.45, .08], [.22, .0, -.1, .85, 0, .05], [.5, 0, -.02, 1.4, -1.25, .2], [.76, 0, .12, 1.9, -1.55, -.35], [1, 0, .02, 2.5, -3.1, -.1]];
  const ease = (t) => t * t * (3 - 2 * t);
  const sample = (p) => { let i = 0; while (i < KF.length - 2 && p > KF[i + 1][0]) i++; const a = KF[i], b = KF[i + 1], t = ease(Math.min(Math.max((p - a[0]) / (b[0] - a[0]), 0), 1)); return a.map((v, k) => v + (b[k] - v) * t); };
  const fit = () => { if (!renderer) return; const w = cv.clientWidth, h = cv.clientHeight; renderer.setSize(w, h, false); cam.aspect = w / h; cam.updateProjectionMatrix(); };
  addEventListener('resize', fit); fit();
  let px = 0, py = 0, cx = 0, cy = 0, tnext = 2000, last = performance.now();
  hero.addEventListener('pointermove', (ev) => { const r = hero.getBoundingClientRect(); px = (ev.clientX - r.left) / r.width * 2 - 1; py = Math.max(-1, Math.min(1, (ev.clientY - r.top) / Math.min(r.height, innerHeight) * 2 - 1)); });

  (function loop(now) {
    const dt = Math.min(now - last, 50); last = now;
    if (inView) {
      const y = scrollY; vel += ((y - lastY) - vel) * .12; lastY = y;
      if (!reduce) x -= dt * (.07 + Math.min(Math.abs(vel), 60) * .012) * (vel < 0 ? -1 : 1);
      if (tw) { x = ((x % tw) - tw) % tw; track.style.transform = `translate3d(${x}px,0,0)`; }
      if (rig) {
        const r = hero.getBoundingClientRect(), total = hero.offsetHeight - (hero.firstElementChild.offsetHeight || 0);
        const p = small() || reduce ? 0 : Math.min(Math.max(-r.top / Math.max(total, 1), 0), 1);
        const k = small() ? [0, 0, .02, .62, -.3, .08] : sample(p);
        const hh = Math.tan(16 * Math.PI / 180) * 9, hw = hh * cam.aspect;
        cx += (px - cx) * .06; cy += (py - cy) * .06;
        const t = now * .001;
        rig.position.set(k[1] * hw, k[2] * hh + Math.sin(t * 1.3) * .05, 0);
        rig.scale.setScalar(k[3] * (small() ? 1 : 1));
        rig.rotation.y = k[4] + cx * .18 + Math.sin(t * .6) * .06;
        rig.rotation.x = k[5] + cy * .1;
        eyeX += (px - eyeX) * .1; eyeY += (py - eyeY) * .1;
        tnext -= dt; if (tnext < 0 && blink <= 0) { blink = .001; tnext = 2200 + Math.random() * 2600; }
        if (blink > 0) { blink += dt / 180; if (blink >= 1) blink = 0; }
        drawScreen(now); renderer.render(scene, cam);
      }
    }
    requestAnimationFrame(loop);
  })(last);
})();
