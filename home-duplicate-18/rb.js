// Hero (dark blueprint + robot loop). Three things live here:
//  1. the giant type band loops sideways (scrolling gives it a push) and the partner strip steps along
//  2. a small three.js jack turns in the black box on the right
//  3. the robot: an 11 s loop on its stand in the middle of the grid —
//       rises out of the stand -> an arm comes down from the top with a glowing SZ chip -> slots it into the head ->
//       the head jolts, the arm lifts away -> the screen boots, the ring lights, the head turns to face you ->
//       it looks around, blinks, shows the Squarezix mark -> powers down, turns away, sinks back into the stand
//     The stand runs on behind the partner strip and shows again below it as a chrome column.
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hero = document.getElementById('hero');
  const track = document.getElementById('hx-track');
  const T = window.THREE;
  if (!hero || !track) return;
  const frame = hero.querySelector('.hx-frame');
  const strip = hero.querySelector('.hx-logos');

  // ---------- 1. type band + partner strip ----------
  let x = 0, vel = 0, lastY = scrollY, tw = 0, inView = true;
  const measure = () => { tw = track.firstElementChild.offsetWidth * 2; };
  addEventListener('resize', measure); (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(measure); measure();
  const lt = document.getElementById('hx-logos');
  let li = 0; const n = lt ? lt.children.length / 2 : 0;
  const step = (d) => { li = (li + d + n) % n; lt.style.transform = `translateX(${-li * lt.children[0].offsetWidth}px)`; };
  const pv = document.getElementById('hx-prev'), nx = document.getElementById('hx-next');
  if (pv) pv.onclick = () => step(-1); if (nx) nx.onclick = () => step(1);
  let hoverStrip = false; if (lt) { lt.addEventListener('pointerenter', () => { hoverStrip = true; }); lt.addEventListener('pointerleave', () => { hoverStrip = false; }); }
  if (lt && !reduce) setInterval(() => inView && !hoverStrip && step(1), 3600);
  new IntersectionObserver(([en]) => { inView = en.isIntersecting; }).observe(hero);
  if (!T) return;

  // shared geometry helpers
  const rr = (w, h, r) => { const s = new T.Shape(), a = -w / 2, b = -h / 2; s.moveTo(a + r, b); s.lineTo(-a - r, b); s.quadraticCurveTo(-a, b, -a, b + r); s.lineTo(-a, -b - r); s.quadraticCurveTo(-a, -b, -a - r, -b); s.lineTo(a + r, -b); s.quadraticCurveTo(a, -b, a, -b - r); s.lineTo(a, b + r); s.quadraticCurveTo(a, b, a + r, b); return s; };
  const ext = (shape, d, bev) => { const g = new T.ExtrudeGeometry(shape, { depth: d, bevelEnabled: true, bevelThickness: bev, bevelSize: bev, bevelSegments: 4, curveSegments: 10 }); g.translate(0, 0, -d / 2); return g; };
  const mat = (color, rough = .5, metal = .1, extra = {}) => new T.MeshStandardMaterial(Object.assign({ color, roughness: rough, metalness: metal }, extra));
  const box = (w, h, d, r, bev, m) => new T.Mesh(ext(rr(w - 2 * bev, h - 2 * bev, Math.max(r - bev, .01)), d - 2 * bev, bev), m);
  const tex = (w, h, draw) => { const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h); const t = new T.CanvasTexture(c); t.anisotropy = 4; return t; };
  const ease = (t) => t * t * (3 - 2 * t);
  const out = (t) => 1 - Math.pow(1 - t, 3);
  const back = (t) => { const c1 = 1.5, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
  const seg = (v, a, b) => Math.min(Math.max((v - a) / (b - a), 0), 1);

  // ---------- 2. the jack in the black box ----------
  const jc = document.getElementById('hx-canvas');
  let jr, js, jcam, jack;
  if (jc) {
    jr = new T.WebGLRenderer({ canvas: jc, antialias: true, alpha: true }); jr.setPixelRatio(Math.min(devicePixelRatio, 2));
    js = new T.Scene(); jcam = new T.PerspectiveCamera(32, 1, .1, 50); jcam.position.set(0, 0, 9);
    js.add(new T.HemisphereLight(0xffffff, 0x2a1d52, .8));
    const k = new T.DirectionalLight(0xffffff, 1.2); k.position.set(3, 4, 5); js.add(k);
    const rim = new T.DirectionalLight(0xab24f2, 1.6); rim.position.set(-4, -2, -3); js.add(rim);
    const R = .42, r = .24, L = 1.35, e = .1, pts = [new T.Vector2(r, L), new T.Vector2(R - e, L)];
    for (let i = 0; i <= 6; i++) { const a = i / 6 * Math.PI / 2; pts.push(new T.Vector2(R - e + Math.sin(a) * e, L - e + Math.cos(a) * e)); }
    pts.push(new T.Vector2(R, -L + e)); for (let i = 0; i <= 6; i++) { const a = i / 6 * Math.PI / 2; pts.push(new T.Vector2(R - e + Math.cos(a) * e, -L + e - Math.sin(a) * e)); }
    pts.push(new T.Vector2(r, -L));
    const g = new T.LatheGeometry(pts, 40), m = mat(0x8a8898, .4, .2, { side: T.DoubleSide });
    jack = new T.Group(); const a = new T.Mesh(g, m), b = a.clone(), c = a.clone(); b.rotation.z = Math.PI / 2; c.rotation.x = Math.PI / 2; jack.add(a, b, c); js.add(jack);
  }

  // ---------- 3. the robot ----------
  const cv = document.getElementById('rb-gl');
  const renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  const scene = new T.Scene();
  const cam = new T.OrthographicCamera(-1, 1, 1, -1, -6000, 6000); cam.position.z = 2000;
  scene.add(new T.HemisphereLight(0xc9c4e8, 0x140b2a, .75));
  const key = new T.DirectionalLight(0xe6e2ff, 1.05); key.position.set(-.6, 1, .9); scene.add(key);
  const fill = new T.DirectionalLight(0xab24f2, .9); fill.position.set(1, -.2, .4); scene.add(fill);
  const rimL = new T.DirectionalLight(0x8c5cff, .7); rimL.position.set(-1, .3, -1); scene.add(rimL);

  const C = { shell: 0x4a4959, body: 0x3c3b4a, dark: 0x22212c, mid: 0x5d5c70, socket: 0x121118 };
  const rig = new T.Group(); scene.add(rig);           // scaled to pixels; origin = top of the stand
  const world = new T.Group(); world.rotation.set(.16, -.16, 0); rig.add(world);

  // stand: a cap block, then a chrome column that runs down out of the hero
  const cap = box(2.7, .85, 2.3, .14, .05, mat(C.body, .55, .15)); cap.position.y = -.425; world.add(cap);
  const capTop = new T.Mesh(new T.BoxGeometry(2.2, .02, 1.8), mat(C.socket, .7)); capTop.position.y = .002; world.add(capTop);
  const chrome = tex(512, 4, (c, w) => { const g = c.createLinearGradient(0, 0, w, 0); [['#15141d', 0], ['#5c5a72', .12], ['#24232f', .22], ['#cfc9ea', .36], ['#3b3a4c', .48], ['#8e89a8', .6], ['#1d1c27', .72], ['#6a6684', .86], ['#15141d', 1]].forEach(([k, o]) => g.addColorStop(o, k)); c.fillStyle = g; c.fillRect(0, 0, w, 4); });
  const column = new T.Mesh(new T.CylinderGeometry(1.25, 1.25, 14, 64, 1, true), new T.MeshBasicMaterial({ map: chrome })); column.position.y = -.85 - 7; world.add(column);
  const collar = new T.Mesh(new T.CylinderGeometry(1.3, 1.3, .06, 64), new T.MeshBasicMaterial({ color: 0xab24f2 })); collar.position.y = -.88; world.add(collar);

  // the robot itself (origin at the stand top)
  const bot = new T.Group(); world.add(bot);
  const body = box(1.9, 1.0, 1.6, .26, .07, mat(C.body, .5, .12)); body.position.y = .5; bot.add(body);
  const seam = new T.Mesh(new T.BoxGeometry(1.92, .02, 1.62), mat(C.dark, .8)); seam.position.y = .62; bot.add(seam);
  const head = new T.Group(); head.position.y = 1.06 + .95; bot.add(head);
  head.add(box(2.1, 1.9, 1.8, .42, .1, mat(C.shell, .45, .12)));
  const ringShape = rr(1.78, 1.6, .36); ringShape.holes.push(new T.Path(rr(1.5, 1.32, .26).getPoints(14).reverse()));
  const ringMat = mat(0x6b2bd6, .35, .1, { emissive: 0xab24f2, emissiveIntensity: .05 });
  const ring = new T.Mesh(ext(ringShape, .08, .04), ringMat); ring.position.z = .93; head.add(ring);
  const gap = box(.3, .5, .16, .1, .04, mat(C.shell, .45, .12)); gap.position.set(.8, -.02, .96); head.add(gap);
  const bezel = box(1.5, 1.32, .16, .26, .04, mat(C.dark, .6)); bezel.position.z = .95; head.add(bezel);
  const SW = 640, SH = 560, sc = document.createElement('canvas'); sc.width = SW; sc.height = SH; const sx = sc.getContext('2d');
  const screenTex = new T.CanvasTexture(sc); screenTex.anisotropy = 4;
  const screen = new T.Mesh(new T.PlaneGeometry(1.26, 1.1), new T.MeshBasicMaterial({ map: screenTex, transparent: true })); screen.position.z = 1.04; head.add(screen);
  [-1, 1].forEach((s) => { const e = new T.Mesh(new T.CylinderGeometry(.22, .22, .3, 28), mat(C.mid, .45, .2)); e.rotation.z = Math.PI / 2; e.position.set(s * 1.12, -.1, 0); head.add(e); });
  // side camera (seen in profile)
  const post = new T.Mesh(new T.CylinderGeometry(.07, .07, .5, 16), mat(C.mid, .4, .4)); post.position.set(-1.25, .3, .35); head.add(post);
  const cambox = box(.32, .3, .62, .07, .03, mat(C.body, .45, .2)); cambox.position.set(-1.25, .62, .35); head.add(cambox);
  const lens = new T.Mesh(new T.CylinderGeometry(.09, .09, .05, 20), new T.MeshBasicMaterial({ color: 0xc58bff })); lens.rotation.x = Math.PI / 2; lens.position.set(-1.25, .62, .67); head.add(lens);
  // back module with a dark circuit panel
  const mod = box(.9, 1.7, .7, .2, .05, mat(C.shell, .45, .12)); mod.position.set(.6, .05, -1.12); head.add(mod);
  const panelTex = tex(128, 256, (c, w, h) => { c.fillStyle = '#100d18'; c.fillRect(0, 0, w, h); c.strokeStyle = 'rgba(190,160,255,.55)'; c.lineWidth = 2; for (let i = 0; i < 14; i++) { const y = 14 + i * 17; c.beginPath(); c.moveTo(12, y); c.lineTo(28 + (i * 37) % 80, y); c.stroke(); } for (let i = 0; i < 5; i++) c.strokeRect(18 + i * 19, 28 + (i * 41) % 120, 13, 44); });
  [1, -1].forEach((s) => { const p = new T.Mesh(new T.PlaneGeometry(.55, 1.36), new T.MeshBasicMaterial({ map: panelTex })); p.rotation.y = s * Math.PI / 2; p.position.set(.6 + s * .46, .05, -1.12); head.add(p); });
  // slot on top of the head (the chip goes in here) and its glow
  const slot = new T.Mesh(new T.BoxGeometry(1.0, .03, .26), mat(C.socket, .8)); slot.position.set(0, .96, .1); head.add(slot);
  const slotGlowMat = new T.MeshBasicMaterial({ color: 0xc76bff, transparent: true, opacity: 0 });
  const slotGlow = new T.Mesh(new T.BoxGeometry(.96, .05, .2), slotGlowMat); slotGlow.position.set(0, .975, .1); head.add(slotGlow);
  const glowLight = new T.PointLight(0xb04cff, 0, 4.5); glowLight.position.set(0, -.1, 1.9); head.add(glowLight);

  // the chip: a little card with the Squarezix mark, glowing
  let logoW = null; const logo = new Image();
  logo.onload = () => { const o = document.createElement('canvas'); o.width = o.height = 241; const c = o.getContext('2d'); c.drawImage(logo, 0, 0); c.globalCompositeOperation = 'source-in'; c.fillStyle = '#fff'; c.fillRect(0, 0, 241, 241); logoW = o; drawChip(); };
  logo.src = 'assets/brand/sz-logo-on-dark.png';
  const chipC = document.createElement('canvas'); chipC.width = 320; chipC.height = 240; const chipTex = new T.CanvasTexture(chipC);
  const drawChip = () => {
    const c = chipC.getContext('2d'), w = 320, h = 240; c.clearRect(0, 0, w, h);
    const g = c.createLinearGradient(0, 0, w, h); g.addColorStop(0, '#3b0f94'); g.addColorStop(1, '#8a1fd8'); c.fillStyle = g; c.beginPath(); c.roundRect(4, 4, w - 8, h - 8, 26); c.fill();
    c.strokeStyle = 'rgba(255,220,255,.75)'; c.lineWidth = 3; c.beginPath(); c.roundRect(26, 26, w - 52, h - 52, 14); c.stroke();
    c.fillStyle = 'rgba(255,230,255,.8)'; for (let i = 0; i < 9; i++) { c.fillRect(46 + i * 26, 8, 8, 14); c.fillRect(46 + i * 26, h - 22, 8, 14); }
    c.shadowColor = '#fff'; c.shadowBlur = 18;
    if (logoW) c.drawImage(logoW, 0, 114, 241, 127, w / 2 - 92, h / 2 - 50, 184, 97);
  };
  drawChip();
  const chip = new T.Group();
  chip.add(box(.92, .7, .12, .1, .03, mat(0x2a0d5c, .4, .3, { emissive: 0x6b1fd0, emissiveIntensity: .7 })));
  const chipFace = new T.Mesh(new T.PlaneGeometry(.86, .64), new T.MeshBasicMaterial({ map: chipTex, transparent: true })); chipFace.position.z = .07; chip.add(chipFace);
  world.add(chip);

  // the arm: a column with a ribbon cable and a yoke whose two prongs hold the chip
  const arm = new T.Group(); world.add(arm);
  const col = box(.78, 12, .78, .18, .05, mat(C.shell, .45, .12)); col.position.y = .95 + 6; arm.add(col);
  const armCap = box(.95, .5, .95, .16, .05, mat(C.body, .5, .2)); armCap.position.y = .75; arm.add(armCap);
  for (let i = 0; i < 8; i++) { const rb = new T.Mesh(new T.CylinderGeometry(.018, .018, 9, 6), mat(0x7d7b92, .5, .2)); rb.position.set(-.24 + i * .068, 5.6, .41); arm.add(rb); }
  const clip = box(.62, .1, .1, .03, .02, mat(C.mid, .5)); clip.position.set(0, 3.2, .45); arm.add(clip);
  const joint = new T.Mesh(new T.CylinderGeometry(.14, .14, 1.26, 20), mat(C.dark, .35, .6)); joint.rotation.z = Math.PI / 2; joint.position.y = .5; arm.add(joint);
  [-1, 1].forEach((s) => { const p = box(.16, .95, .42, .06, .03, mat(C.shell, .45, .12)); p.position.set(s * .58, .08, 0); arm.add(p); });

  // the face: off / booting / eyes / mark
  const drawScreen = (t, power, eyes, mark, ex, ey, blink) => {
    const c = sx; c.clearRect(0, 0, SW, SH); c.save(); c.beginPath(); c.roundRect(0, 0, SW, SH, 96); c.clip();
    const g = c.createLinearGradient(0, 0, 0, SH); g.addColorStop(0, '#170a24'); g.addColorStop(1, '#09060f'); c.fillStyle = g; c.fillRect(0, 0, SW, SH);
    c.globalAlpha = .12 + power * .55; c.strokeStyle = '#c792ff'; c.lineWidth = 2;
    for (let i = 1; i < 6; i++) { const a = i * SW / 6, b = i * SH / 6; c.beginPath(); c.moveTo(a, 0); c.lineTo(a, SH); c.stroke(); c.beginPath(); c.moveTo(0, b); c.lineTo(SW, b); c.stroke(); }
    c.globalAlpha = 1;
    if (power > 0 && power < 1) { for (let i = 0; i < 6; i++) { c.fillStyle = `rgba(210,160,255,${Math.random() * .35})`; c.fillRect(0, Math.random() * SH, SW, 2 + Math.random() * 6); } }
    c.shadowColor = '#e9c8ff'; c.shadowBlur = 26; c.fillStyle = '#fff';
    if (eyes > 0) { c.globalAlpha = eyes; const open = 1 - blink; [-1, 1].forEach((s) => { c.beginPath(); c.ellipse(SW / 2 + s * 92 + ex * 60, SH / 2 + ey * 40, 40, Math.max(3, 44 * open), 0, 0, 7); c.fill(); }); }
    if (mark > 0 && logoW) { c.globalAlpha = mark; const w = 420, h = w * 127 / 241; c.drawImage(logoW, 0, 114, 241, 127, (SW - w) / 2, (SH - h) / 2 + 16, w, h); c.font = '700 40px Sora, sans-serif'; c.textAlign = 'center'; c.fillText('MARKETING AGENCY.', SW / 2, SH / 2 - h / 2 - 12); }
    c.restore(); screenTex.needsUpdate = true;
  };

  // layout: the stand top sits a little above the partner strip, robot sized to the grid
  let k = 100, cw = 1, ch = 1;
  const layout = () => {
    cw = cv.clientWidth; ch = cv.clientHeight; renderer.setSize(cw, ch, false);
    cam.left = -cw / 2; cam.right = cw / 2; cam.top = ch / 2; cam.bottom = -ch / 2; cam.updateProjectionMatrix();
    const fw = frame.clientWidth, small = innerWidth <= 900;
    const headPx = Math.min(Math.max(fw * (small ? .44 : .16), 150), 250);
    k = headPx / 2.1; rig.scale.setScalar(k);
    const top = strip.offsetTop - headPx * .3;
    rig.position.set(0, ch / 2 - top, 0);
    if (jr) { const w = jc.clientWidth, h = jc.clientHeight; jr.setSize(w, h, false); jcam.aspect = w / h; jcam.updateProjectionMatrix(); }
  };
  addEventListener('resize', layout); (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(layout); layout();

  let px = 0, py = 0, cx = 0, cy = 0, last = performance.now();
  hero.addEventListener('pointermove', (ev) => { const r = hero.getBoundingClientRect(); px = (ev.clientX - r.left) / r.width * 2 - 1; py = Math.max(-1, Math.min(1, (ev.clientY - r.top) / r.height * 2 - 1)); });

  const L = 11, PROF = 1.25, t0 = performance.now();
  const ARM_HIGH = 9;
  (function loop(now) {
    const dt = Math.min(now - last, 50); last = now;
    if (inView) {
      const y = scrollY; vel += ((y - lastY) - vel) * .12; lastY = y;
      if (!reduce) x -= dt * (.07 + Math.min(Math.abs(vel), 60) * .012) * (vel < 0 ? -1 : 1);
      if (tw) { x = ((x % tw) - tw) % tw; track.style.transform = `translate3d(${x}px,0,0)`; }
      cx += (px - cx) * .06; cy += (py - cy) * .06;
      const T0 = (now - t0) / 1000;
      if (jack) { jack.rotation.y = .6 + T0 * .5 + cx * .4; jack.rotation.x = .5 + T0 * .3 + cy * .3; jr.render(js, jcam); }

      // robot timeline (reduced motion: stand still, facing front, eyes on)
      const t = reduce ? 6.0 : T0 % L;
      const up = ease(seg(t, .2, 1.4)) * (1 - ease(seg(t, 9.7, 10.85)));
      bot.position.y = -(1 - up) * 3.1;
      bot.visible = up > .002;
      // arm + chip
      const headTop = bot.position.y + head.position.y + .95;
      const d1 = out(seg(t, 1.3, 2.5)), ins = ease(seg(t, 2.6, 3.2)), lift = ease(seg(t, 3.5, 4.6));
      const high = headTop + ARM_HIGH, hover = headTop + 1.0, seated = headTop - .2;
      const chipY = high + (hover - high) * d1 + (seated - hover) * ins;
      const armY = t < 3.35 ? chipY : seated + (high + 2 - seated) * lift;
      arm.position.y = armY; arm.visible = t > 1.2 && t < 4.7;
      chip.position.set(0, chipY, .1); chip.visible = t > 1.2 && t < 3.35;
      // reaction: the head jolts as the chip seats
      const jolt = Math.sin(seg(t, 3.15, 3.75) * Math.PI);
      const powerOn = ease(seg(t, 4.4, 5.0)) * (1 - ease(seg(t, 8.9, 9.5)));
      const turnIn = back(seg(t, 4.8, 5.8)), turnOut = ease(seg(t, 8.9, 9.7));
      head.rotation.y = PROF * (1 - turnIn) + PROF * turnOut + cx * .14 * powerOn;
      head.rotation.x = cy * .06 * powerOn;
      head.rotation.z = jolt * .05;
      head.position.y = 1.06 + .95 - jolt * .1;
      ringMat.emissiveIntensity = .05 + powerOn * 1.6;
      slotGlowMat.opacity = ease(seg(t, 3.2, 3.6)) * (1 - ease(seg(t, 9.5, 10))) * (.7 + .3 * Math.sin(T0 * 6));
      glowLight.intensity = powerOn * 1.6;
      // face
      const eyesOn = ease(seg(t, 5.0, 5.4)) * (1 - ease(seg(t, 6.6, 6.9))) + ease(seg(t, 7.8, 8.1)) * (1 - ease(seg(t, 8.8, 9.1)));
      const mark = ease(seg(t, 6.8, 7.1)) * (1 - ease(seg(t, 7.7, 8.0)));
      const look = t < 6.6 ? Math.sin((t - 5) * 2.2) * .5 : 0;
      const blinkT = [5.9, 8.4].reduce((b, bt) => Math.max(b, Math.sin(seg(t, bt, bt + .22) * Math.PI)), 0);
      drawScreen(T0, powerOn < 1 && powerOn > 0 ? powerOn : powerOn, eyesOn, mark, look + cx * .4, cy * .3, blinkT);
      renderer.render(scene, cam);
    }
    requestAnimationFrame(loop);
  })(last);
})();
