// Hero (blueprint grid, dark). The robot stands in the middle of the stage.
//   on load : the robot starts with its back to us, a mechanical arm drops in from the top, turns its head to face us (the Squarezix
//             screen boots up) and lifts away again
//   scroll  : the stage is pinned and the camera pushes into the robot's screen until it fills the view; that lands on the
//             "Welcome to the inside of Squarezix" frame, then the page carries on
// The giant type loops behind it (speed follows scroll velocity). The partner strip steps on its own.
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hero = document.getElementById('hero');
  const track = document.getElementById('hx-track');
  const cv = document.getElementById('hx-canvas');
  const endEl = document.getElementById('hx-end');
  const frame = hero && hero.querySelector('.hx-frame');
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

  // ---------- robot + arm ----------
  let renderer, scene, cam, rig, bot, arm, screenCtx, screenTex, logoImg = null;
  const SW = 1152, SH = 1040;
  if (T && cv) {
    renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    scene = new T.Scene();
    cam = new T.PerspectiveCamera(32, 1, .05, 60); cam.position.set(0, 0, 10.5);
    scene.add(new T.HemisphereLight(0xb8b4d8, 0x1a1030, .7));
    const key = new T.DirectionalLight(0xdcd8f2, 1.1); key.position.set(3, 4, 6); scene.add(key);
    const rim = new T.DirectionalLight(0xab24f2, 1.4); rim.position.set(-5, 1, -4); scene.add(rim);
    const glow = new T.PointLight(0xc061ff, 1.5, 7); glow.position.set(0, -.2, 2.4); scene.add(glow);

    const rr = (w, h, r) => { const s = new T.Shape(), a = -w / 2, b = -h / 2; s.moveTo(a + r, b); s.lineTo(-a - r, b); s.quadraticCurveTo(-a, b, -a, b + r); s.lineTo(-a, -b - r); s.quadraticCurveTo(-a, -b, -a - r, -b); s.lineTo(a + r, -b); s.quadraticCurveTo(a, -b, a, -b - r); s.lineTo(a, b + r); s.quadraticCurveTo(a, b, a + r, b); return s; };
    const ext = (shape, d, bev) => { const g = new T.ExtrudeGeometry(shape, { depth: d, bevelEnabled: true, bevelThickness: bev, bevelSize: bev, bevelSegments: 4, curveSegments: 10 }); g.translate(0, 0, -d / 2); return g; };
    const box = (w, h, d, r, bev, color, rough = .45) => new T.Mesh(ext(rr(w - 2 * bev, h - 2 * bev, Math.max(r - bev, .01)), d - 2 * bev, bev), new T.MeshStandardMaterial({ color, roughness: rough, metalness: .05 }));
    const white = 0x3b3a48, grey = 0x55546a;

    bot = new T.Group();
    bot.add(box(2.2, 2.0, 1.7, .4, .1, white));
    const ringShape = rr(1.8, 1.6, .36); ringShape.holes.push(new T.Path(rr(1.74, 1.52, .26).getPoints(14).reverse()));
    const ring = new T.Mesh(ext(ringShape, .08, .04), new T.MeshStandardMaterial({ color: 0xab24f2, emissive: 0x9a2cf0, emissiveIntensity: 1.3, roughness: .35 }));
    ring.position.z = .9; bot.add(ring);
    const gap = box(.34, .56, .16, .1, .04, white); gap.position.set(.9, -.02, .94); bot.add(gap);
    const bezel = box(1.72, 1.52, .16, .3, .04, 0x2a2935); bezel.position.z = .93; bot.add(bezel);
    const sc = document.createElement('canvas'); sc.width = SW; sc.height = SH; screenCtx = sc.getContext('2d');
    screenTex = new T.CanvasTexture(sc); screenTex.anisotropy = 8;
    const screen = new T.Mesh(new T.PlaneGeometry(1.44, 1.3), new T.MeshBasicMaterial({ map: screenTex, transparent: true }));
    screen.position.z = 1.03; bot.add(screen);
    [-1, 1].forEach((sx) => { const e = new T.Mesh(new T.CylinderGeometry(.22, .22, .4, 28), new T.MeshStandardMaterial({ color: grey, roughness: .4 })); e.rotation.z = Math.PI / 2; e.position.set(sx * 1.3, -.1, 0); bot.add(e); });
    const mod = box(.95, 1.75, .75, .22, .06, white); mod.position.set(.75, .05, -1.2); bot.add(mod);
    const pc = document.createElement('canvas'); pc.width = 128; pc.height = 256; const px = pc.getContext('2d');
    px.fillStyle = '#16121f'; px.fillRect(0, 0, 128, 256); px.strokeStyle = 'rgba(200,190,230,.55)'; px.lineWidth = 2;
    for (let i = 0; i < 14; i++) { const yy = 14 + i * 17; px.beginPath(); px.moveTo(14, yy); px.lineTo(14 + 20 + (i * 37) % 80, yy); px.stroke(); }
    for (let i = 0; i < 5; i++) px.strokeRect(20 + i * 18, 30 + (i * 41) % 120, 14, 40);
    const ptex = new T.CanvasTexture(pc);
    const panel = new T.Mesh(new T.PlaneGeometry(.62, 1.4), new T.MeshBasicMaterial({ map: ptex })); panel.rotation.y = Math.PI / 2; panel.position.set(1.25, .05, -1.2); bot.add(panel);
    const panelL = panel.clone(); panelL.rotation.y = -Math.PI / 2; panelL.position.x = .25; bot.add(panelL);
    const body = box(1.9, 1.3, 1.55, .32, .08, 0x302f3d); body.position.y = -1.65; bot.add(body);
    const base = box(2.8, .38, 2.1, .16, .05, 0x24232e); base.position.y = -2.5; bot.add(base);
    const cable = new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3([new T.Vector3(.3, 1.0, -1.1), new T.Vector3(-.2, .5, -1.55), new T.Vector3(-.3, -.6, -1.5), new T.Vector3(0, -1.5, -1.1)]), 40, .055, 8), new T.MeshStandardMaterial({ color: 0x6a6980, roughness: .5 }));
    bot.add(cable);
    bot.position.y = .75;
    rig = new T.Group(); rig.add(bot); scene.add(rig);

    // the arm: a tall column with a ribbon cable, ending in a yoke that grips the top of the head
    arm = new T.Group();
    const col = box(.78, 7, .78, .2, .06, white); col.position.y = 3.9; arm.add(col);
    const cap = box(.9, .5, .9, .18, .05, 0x2a2935); cap.position.y = .35; arm.add(cap);
    for (let i = 0; i < 7; i++) { const rb = new T.Mesh(new T.CylinderGeometry(.018, .018, 5.6, 6), new T.MeshStandardMaterial({ color: 0x6a6980, roughness: .6 })); rb.position.set(-.27 + i * .09, 4.4, .4); arm.add(rb); }
    const yokeL = box(.2, .55, .9, .08, .03, white), yokeR = yokeL.clone(); yokeL.position.set(-.55, .0, 0); yokeR.position.set(.55, .0, 0); arm.add(yokeL, yokeR);
    const pin = new T.Mesh(new T.CylinderGeometry(.16, .16, 1.3, 20), new T.MeshStandardMaterial({ color: 0x4a4658, roughness: .4, metalness: .4 })); pin.rotation.z = Math.PI / 2; arm.add(pin);
    scene.add(arm);
  }

  // the face: dark grid, the Squarezix mark, a soft scanline. `on` = 0..1 boot-up level
  const logo = new Image(); logo.onload = () => { logoImg = logo; }; logo.src = 'assets/brand/sz-logo-on-dark.png';
  const drawScreen = (t, on) => {
    const c = screenCtx; if (!c) return;
    c.clearRect(0, 0, SW, SH);
    c.save(); c.beginPath(); c.roundRect(0, 0, SW, SH, 200); c.clip();
    const g = c.createLinearGradient(0, 0, 0, SH); g.addColorStop(0, '#1d0a22'); g.addColorStop(1, '#0d0615'); c.fillStyle = g; c.fillRect(0, 0, SW, SH);
    c.strokeStyle = 'rgba(255,140,220,.3)'; c.lineWidth = 3;
    for (let i = 1; i < 8; i++) { const a = i * SW / 8, b = i * SH / 8; c.beginPath(); c.moveTo(a, 0); c.lineTo(a, SH); c.stroke(); c.beginPath(); c.moveTo(0, b); c.lineTo(SW, b); c.stroke(); }
    const flick = on < 1 ? (Math.sin(t * 40) > 0 ? 1 : .35) : 1, a = Math.min(on, 1) * flick;
    c.globalAlpha = a;
    c.shadowColor = 'rgba(171,36,242,.9)'; c.shadowBlur = 50;
    c.fillStyle = '#fff'; c.font = '700 74px Sora, sans-serif'; c.textAlign = 'center';
    c.fillText('MARKETING', SW / 2, 270); c.fillText('AGENCY.', SW / 2, 352);
    if (logoImg) { const sw = 237, sh = 124, w = 760, h = w * sh / sw; c.drawImage(logoImg, 2, 106, sw, sh, (SW - w) / 2, 440, w, h); }
    c.globalAlpha = 1; c.shadowBlur = 0;
    const sy = ((t * 120) % (SH + 200)) - 100; const sg = c.createLinearGradient(0, sy - 90, 0, sy + 90); sg.addColorStop(0, 'rgba(255,255,255,0)'); sg.addColorStop(.5, 'rgba(255,255,255,.07)'); sg.addColorStop(1, 'rgba(255,255,255,0)'); c.fillStyle = sg; c.fillRect(0, sy - 90, SW, 180);
    c.restore(); screenTex.needsUpdate = true;
  };

  const ease = (t) => t * t * (3 - 2 * t);
  const out = (t) => 1 - Math.pow(1 - t, 3);
  const seg = (v, a, b) => Math.min(Math.max((v - a) / (b - a), 0), 1);
  const fit = () => { if (!renderer) return; const w = cv.clientWidth, h = cv.clientHeight; renderer.setSize(w, h, false); cam.aspect = w / h; cam.updateProjectionMatrix(); };
  addEventListener('resize', fit); fit();
  let px = 0, py = 0, cx = 0, cy = 0, last = performance.now();
  const t0 = performance.now();
  hero.addEventListener('pointermove', (ev) => { const r = hero.getBoundingClientRect(); px = (ev.clientX - r.left) / r.width * 2 - 1; py = Math.max(-1, Math.min(1, (ev.clientY - r.top) / Math.min(r.height, innerHeight) * 2 - 1)); });

  (function loop(now) {
    const dt = Math.min(now - last, 50); last = now;
    if (inView) {
      const y = scrollY; vel += ((y - lastY) - vel) * .12; lastY = y;
      if (!reduce) x -= dt * (.07 + Math.min(Math.abs(vel), 60) * .012) * (vel < 0 ? -1 : 1);
      if (tw) { x = ((x % tw) - tw) % tw; track.style.transform = `translate3d(${x}px,0,0)`; }
      if (rig) {
        const sm = small() || reduce;
        const r = hero.getBoundingClientRect(), total = hero.offsetHeight - (hero.firstElementChild.offsetHeight || 0);
        const p = sm ? 0 : Math.min(Math.max(-r.top / Math.max(total, 1), 0), 1);
        const ts = (now - t0) / 1000, ti = sm ? 99 : ts;       // intro clock (seconds)
        // intro: back to us -> arm drops -> head turns to the front -> arm lifts away
        const drop = out(seg(ti, .5, 1.6)), turn = ease(seg(ti, 1.8, 3.2)), lift = ease(seg(ti, 3.4, 4.4));
        const armY = 8 - (1 - drop) * 0 - drop * 0 + (1 - drop) * 6 + lift * 8;
        arm.position.set(0, 1.78 + (1 - drop) * 7 + lift * 8, 0);
        arm.visible = drop > 0 && lift < 1;
        bot.rotation.y = Math.PI * (1 - turn) + Math.sin(ts * .6) * .04 + cx * .16;
        bot.rotation.x = cy * .08;
        const on = ease(seg(ti, 3.0, 3.8));
        drawScreen(ts, on);
        // scroll: push the camera into the screen
        const z = ease(seg(p, .04, .62));
        const D = 10.5 + (2.1 - 10.5) * Math.pow(z, .8);
        const hh = Math.tan(16 * Math.PI / 180);
        cam.position.set(0, .75 * z, D);
        rig.position.y = 0;
        cx += (px - cx) * .06; cy += (py - cy) * .06;
        if (frame) frame.style.opacity = (1 - seg(p, .18, .5)).toFixed(3);
        if (endEl) { const e = ease(seg(p, .6, .72)); endEl.style.opacity = e.toFixed(3); endEl.style.visibility = e > .01 ? 'visible' : 'hidden'; endEl.style.pointerEvents = e > .9 ? 'auto' : 'none'; }
        renderer.render(scene, cam);
      }
    }
    requestAnimationFrame(loop);
  })(last);
})();
