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
  const pin = hero.querySelector('.hx-pin');
  const endEl = document.getElementById('hx-end');
  const endNoise = document.getElementById('hx-end-noise');
  const fades = hero.querySelectorAll('.hx-row, .hx-rail');

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
  // services list: one card that slides to whichever row is hovered
  const svc = document.getElementById('hx-svc'), card = document.getElementById('hx-card');
  if (svc && card) {
    const img = card.querySelector('img'), kEl = card.querySelector('.hx-card-k'), tEl = card.querySelector('.hx-card-t'), dEl = card.querySelector('.hx-card-d');
    svc.querySelectorAll('a').forEach((a, i) => {
      a.addEventListener('pointerenter', () => {
        svc.querySelectorAll('a').forEach((b) => b.classList.toggle('on', b === a));
        if (img.getAttribute('src') !== a.dataset.img) img.src = a.dataset.img;
        kEl.textContent = `Service ${a.querySelector('.num').textContent}`; tEl.textContent = a.firstElementChild.textContent; dEl.textContent = a.dataset.desc;
        const top = Math.min(a.offsetTop + a.offsetHeight / 2 - card.offsetHeight / 2, svc.clientHeight - card.offsetHeight);
        card.style.setProperty('--cy', Math.max(0, top) + 'px'); card.classList.add('show');
      });
    });
    svc.addEventListener('pointerleave', () => { card.classList.remove('show'); svc.querySelectorAll('a').forEach((b) => b.classList.remove('on')); });
  }
  if (!T) return;

  // shared geometry helpers
  const rr = (w, h, r) => { const s = new T.Shape(), a = -w / 2, b = -h / 2; s.moveTo(a + r, b); s.lineTo(-a - r, b); s.quadraticCurveTo(-a, b, -a, b + r); s.lineTo(-a, -b - r); s.quadraticCurveTo(-a, -b, -a - r, -b); s.lineTo(a + r, -b); s.quadraticCurveTo(a, -b, a, -b - r); s.lineTo(a, b + r); s.quadraticCurveTo(a, b, a + r, b); return s; };
  const ext = (shape, d, bev) => { const g = new T.ExtrudeGeometry(shape, { depth: d, bevelEnabled: true, bevelThickness: bev, bevelSize: bev, bevelSegments: 4, curveSegments: 10 }); g.translate(0, 0, -d / 2); return g; };
  const mat = (color, rough = .5, metal = .1, extra = {}) => new T.MeshPhysicalMaterial(Object.assign({ color, roughness: rough, metalness: metal, clearcoat: .35, clearcoatRoughness: .3, envMapIntensity: .6 }, extra));
  const box = (w, h, d, r, bev, m) => new T.Mesh(ext(rr(w - 2 * bev, h - 2 * bev, Math.max(r - bev, .01)), d - 2 * bev, bev), m);
  const tex = (w, h, draw) => { const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h); const t = new T.CanvasTexture(c); t.anisotropy = 4; t.encoding = T.sRGBEncoding; return t; };
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
  renderer.localClippingEnabled = true;
  renderer.outputEncoding = T.sRGBEncoding; renderer.toneMapping = T.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  const clipPlane = new T.Plane(new T.Vector3(0, 1, 0), 0);
  const scene = new T.Scene();
  const cam = new T.OrthographicCamera(-1, 1, 1, -1, -6000, 6000); cam.position.z = 2000;
  // studio reflections: a small softbox room baked into an environment map, so the surfaces read as real materials
  {
    const env = new T.Scene(), basic = (c) => new T.MeshBasicMaterial({ color: c, side: T.BackSide });
    env.add(new T.Mesh(new T.BoxGeometry(20, 20, 20), basic(0x07060c)));
    const panel = (w, h, c, x, y, z, ry = 0, rx = 0) => { const m = new T.Mesh(new T.PlaneGeometry(w, h), new T.MeshBasicMaterial({ color: c, side: T.DoubleSide })); m.position.set(x, y, z); m.rotation.set(rx, ry, 0); env.add(m); };
    panel(9, 4, 0x8c87a6, -3, 6, 4, 0, Math.PI / 2.6);          // big soft key, top left
    panel(1.2, 12, 0x7a3cff, 8, 0, 0, -Math.PI / 2);           // tall violet strip, right
    panel(1.2, 12, 0x6b5cff, -8, 0, -2, Math.PI / 2);          // cool strip, left
    panel(10, 1, 0x5c4f8a, 0, -6, 6, 0, -Math.PI / 3);         // low rim
    const pm = new T.PMREMGenerator(renderer); scene.environment = pm.fromScene(env, .035).texture; pm.dispose();
  }
  scene.add(new T.HemisphereLight(0xc9c4e8, 0x0e0818, .35));
  const key = new T.DirectionalLight(0xf2eeff, .75); key.position.set(-.6, 1, .9); scene.add(key);
  const fill = new T.DirectionalLight(0x9a5cff, .45); fill.position.set(1, -.2, .4); scene.add(fill);

  const C = { shell: 0x2e2d36, body: 0x24232b, dark: 0x141319, mid: 0x4a4954, socket: 0x0b0a0f };
  const rig = new T.Group(); scene.add(rig);           // scaled to pixels; origin = top of the stand
  const world = new T.Group(); world.rotation.set(.16, -.16, 0); rig.add(world);

  // stand: a cap block, then a chrome column that runs down out of the hero
  const cap = box(3.0, .85, 2.6, .16, .05, mat(C.body, .55, .15)); cap.position.y = -.425; world.add(cap);
  const capTop = new T.Mesh(new T.BoxGeometry(2.6, .02, 2.25), mat(C.socket, .7)); capTop.position.y = .002; world.add(capTop);
  const chrome = tex(512, 4, (c, w) => { const g = c.createLinearGradient(0, 0, w, 0); [['#15141d', 0], ['#5c5a72', .12], ['#24232f', .22], ['#cfc9ea', .36], ['#3b3a4c', .48], ['#8e89a8', .6], ['#1d1c27', .72], ['#6a6684', .86], ['#15141d', 1]].forEach(([k, o]) => g.addColorStop(o, k)); c.fillStyle = g; c.fillRect(0, 0, w, 4); });
  const column = new T.Mesh(new T.CylinderGeometry(1.35, 1.35, 14, 64, 1, true), new T.MeshBasicMaterial({ map: chrome })); column.position.y = -.85 - 7; world.add(column);
  const collar = new T.Mesh(new T.CylinderGeometry(1.4, 1.4, .06, 64), new T.MeshBasicMaterial({ color: 0xab24f2 })); collar.position.y = -.88; world.add(collar);

  // the robot itself (origin at the stand top)
  const bot = new T.Group(); world.add(bot);
  const body = box(1.9, 1.0, 1.6, .26, .07, mat(C.body, .5, .12)); body.position.y = .5; bot.add(body);
  const seam = new T.Mesh(new T.BoxGeometry(1.92, .02, 1.62), mat(C.dark, .8)); seam.position.y = .62; bot.add(seam);
  const head = new T.Group(); head.position.y = 1.06 + .95; bot.add(head);
  head.add(box(2.1, 1.9, 1.8, .42, .1, mat(C.shell, .45, .12)));
  const ringShape = rr(1.7, 1.52, .34); ringShape.holes.push(new T.Path(rr(1.56, 1.38, .28).getPoints(16).reverse()));
  const ringMat = mat(0x17121f, .3, .1, { emissive: 0x8a3dff, emissiveIntensity: .03, clearcoat: 1, clearcoatRoughness: .1 }); ringMat.toneMapped = false;
  const ring = new T.Mesh(ext(ringShape, .08, .04), ringMat); ring.position.z = .93; head.add(ring);
  const gap = box(.3, .5, .16, .1, .04, mat(C.shell, .45, .12)); gap.position.set(.8, -.02, .96); head.add(gap);
  const bezel = box(1.5, 1.32, .16, .26, .04, mat(C.dark, .6)); bezel.position.z = .95; head.add(bezel);
  const SW = 640, SH = 560, sc = document.createElement('canvas'); sc.width = SW; sc.height = SH; const sx = sc.getContext('2d');
  const screenTex = new T.CanvasTexture(sc); screenTex.anisotropy = 8; screenTex.encoding = T.sRGBEncoding;
  // a curved (convex) display with a glass layer over it
  const bulge = (w, h, d) => { const g = new T.PlaneGeometry(w, h, 40, 36), a = g.attributes.position; for (let i = 0; i < a.count; i++) { const u = a.getX(i) / (w / 2), v = a.getY(i) / (h / 2); a.setZ(i, d * (1 - .55 * u * u - .45 * v * v)); } g.computeVertexNormals(); return g; };
  const screen = new T.Mesh(bulge(1.26, 1.1, .05), new T.MeshBasicMaterial({ map: screenTex, transparent: true, toneMapped: false })); screen.position.z = 1.02; head.add(screen);
  const maskTex = tex(256, 224, (c, w, h) => { c.fillStyle = '#000'; c.fillRect(0, 0, w, h); c.fillStyle = '#fff'; c.beginPath(); c.roundRect(0, 0, w, h, 38); c.fill(); });
  const glass = new T.Mesh(bulge(1.26, 1.1, .05), mat(0x0a0812, .06, 0, { transparent: true, opacity: .28, alphaMap: maskTex, clearcoat: 1, clearcoatRoughness: .04, envMapIntensity: 2.4, depthWrite: false }));
  glass.position.z = 1.034; head.add(glass);
  [-1, 1].forEach((s) => { const e = new T.Mesh(new T.CylinderGeometry(.22, .22, .3, 28), mat(C.mid, .45, .2)); e.rotation.z = Math.PI / 2; e.position.set(s * 1.12, -.1, 0); head.add(e); });
  // side camera (seen in profile)
  const post = new T.Mesh(new T.CylinderGeometry(.07, .07, .5, 16), mat(C.mid, .4, .4)); post.position.set(-1.25, .3, .35); head.add(post);
  const cambox = box(.32, .3, .62, .07, .03, mat(C.body, .45, .2)); cambox.position.set(-1.25, .62, .35); head.add(cambox);
  const lens = new T.Mesh(new T.CylinderGeometry(.09, .09, .05, 24), mat(0x07060b, .05, .2, { emissive: 0x6b4fd0, emissiveIntensity: .35, clearcoat: 1 })); lens.rotation.x = Math.PI / 2; lens.position.set(-1.25, .62, .67); head.add(lens);
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
  logo.onload = () => { const o = document.createElement('canvas'); o.width = o.height = 241; const c = o.getContext('2d'); c.drawImage(logo, 0, 0); c.globalCompositeOperation = 'source-in'; c.fillStyle = '#fff'; c.fillRect(0, 0, 241, 241); c.clearRect(0, 0, 3, 241); c.clearRect(238, 0, 3, 241); logoW = o; drawChip(); };
  logo.src = 'assets/brand/sz-logo-on-dark.png';
  const chipC = document.createElement('canvas'); chipC.width = 320; chipC.height = 240; const chipTex = new T.CanvasTexture(chipC); chipTex.encoding = T.sRGBEncoding;
  const drawChip = () => {
    const c = chipC.getContext('2d'), w = 320, h = 240; c.clearRect(0, 0, w, h);
    const g = c.createLinearGradient(0, 0, w, h); g.addColorStop(0, '#16131f'); g.addColorStop(1, '#0b0a10'); c.fillStyle = g; c.beginPath(); c.roundRect(4, 4, w - 8, h - 8, 18); c.fill();
    c.strokeStyle = 'rgba(190,160,255,.35)'; c.lineWidth = 1.2;
    for (let i = 0; i < 16; i++) { const y = 30 + i * 11.5; c.beginPath(); c.moveTo(16, y); c.lineTo(48 + (i * 23) % 40, y); c.lineTo(58 + (i * 23) % 40, y + 6); c.stroke(); c.beginPath(); c.moveTo(w - 16, y); c.lineTo(w - 48 - (i * 17) % 40, y); c.stroke(); }
    c.fillStyle = '#0f0d16'; c.strokeStyle = 'rgba(200,170,255,.55)'; c.lineWidth = 1.5; c.beginPath(); c.roundRect(w / 2 - 70, h / 2 - 62, 140, 124, 10); c.fill(); c.stroke();
    c.fillStyle = 'rgba(214,196,255,.85)'; for (let i = 0; i < 10; i++) { c.fillRect(70 + i * 19, 6, 6, 10); c.fillRect(70 + i * 19, h - 16, 6, 10); }
    c.shadowColor = 'rgba(180,140,255,.9)'; c.shadowBlur = 10;
    if (logoW) c.drawImage(logoW, 0, 114, 241, 127, w / 2 - 50, h / 2 - 26, 100, 53);
  };
  drawChip();
  const chip = new T.Group();
  chip.add(box(.92, .7, .12, .1, .03, mat(0x121018, .35, .6, { emissive: 0x4a2a9a, emissiveIntensity: .18 })));
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

  // everything that belongs to the robot is cut off at the top of the stand, so it sinks into it cleanly
  bot.traverse((o) => { if (o.material) { o.material = o.material.clone(); o.material.clippingPlanes = [clipPlane]; } });
  const ringM2 = ring.material, slotM2 = slotGlow.material;
  const _q = new T.Quaternion(), _n = new T.Vector3(), _p = new T.Vector3(), _s = new T.Vector3();

  // the face: off / booting / eyes / mark
  // static tiles (reused for the grain on the display, the dive-in static and the end frame)
  const NOISE = Array.from({ length: 5 }, () => { const c = document.createElement('canvas'); c.width = 200; c.height = 176; const x = c.getContext('2d'), d = x.createImageData(200, 176);
    for (let i = 0; i < d.data.length; i += 4) { const v = Math.random() * 255; d.data[i] = v * .92; d.data[i + 1] = v * .86; d.data[i + 2] = v; d.data[i + 3] = 255; } x.putImageData(d, 0, 0); return c; });
  const noiseTile = () => NOISE[(Math.random() * NOISE.length) | 0];
  const drawScreen = (t, power, eyes, mark, ex, ey, blink, stat) => {
    const c = sx; c.clearRect(0, 0, SW, SH); c.save(); c.beginPath(); c.roundRect(0, 0, SW, SH, 92); c.clip();
    const g = c.createRadialGradient(SW / 2, SH * .45, 20, SW / 2, SH / 2, SW * .7); g.addColorStop(0, `rgb(${18 + power * 8},${12 + power * 4},${30 + power * 10})`); g.addColorStop(1, '#040307'); c.fillStyle = g; c.fillRect(0, 0, SW, SH);
    // phosphor content
    c.save(); c.shadowColor = 'rgba(176,140,255,.85)'; c.shadowBlur = 16; c.fillStyle = '#efe7ff';
    if (eyes > 0) { c.globalAlpha = eyes; const open = Math.max(.08, 1 - blink); [-1, 1].forEach((s) => { const w = 92, h = 150 * open; c.beginPath(); c.roundRect(SW / 2 + s * 118 - w / 2 + ex * 46, SH / 2 - h / 2 + ey * 30, w, h, 46 * Math.min(1, open * 1.6)); c.fill(); }); }
    if (mark > 0 && logoW) { c.globalAlpha = mark; const w = 400, h = w * 127 / 241; c.drawImage(logoW, 0, 114, 241, 127, (SW - w) / 2, (SH - h) / 2 + 22, w, h);
      c.shadowBlur = 6; c.font = '400 27px "Space Mono", monospace'; c.textAlign = 'center'; if ('letterSpacing' in c) c.letterSpacing = '7px'; c.fillText('MARKETING AGENCY', SW / 2 + 3, (SH - h) / 2 - 8); if ('letterSpacing' in c) c.letterSpacing = '0px'; }
    c.restore();
    // boot flicker
    if (power > 0 && power < 1) { for (let i = 0; i < 5; i++) { c.fillStyle = `rgba(210,180,255,${Math.random() * .25})`; c.fillRect(0, Math.random() * SH, SW, 1 + Math.random() * 5); } }
    // scanlines, grain, rolling band
    c.fillStyle = 'rgba(0,0,0,.22)'; for (let y = 0; y < SH; y += 3) c.fillRect(0, y, SW, 1);
    c.imageSmoothingEnabled = false;
    c.globalCompositeOperation = 'lighter'; c.globalAlpha = .05 + power * .03; c.drawImage(noiseTile(), 0, 0, SW, SH);
    const by = ((t * 90) % (SH + 160)) - 80; const bg = c.createLinearGradient(0, by - 60, 0, by + 60); bg.addColorStop(0, 'rgba(160,130,255,0)'); bg.addColorStop(.5, `rgba(160,130,255,${.05 + power * .04})`); bg.addColorStop(1, 'rgba(160,130,255,0)'); c.globalAlpha = 1; c.fillStyle = bg; c.fillRect(0, by - 60, SW, 120);
    c.globalCompositeOperation = 'source-over';
    // the dive-in: static takes over the display
    if (stat > 0) { c.globalAlpha = Math.min(1, stat); c.drawImage(noiseTile(), 0, 0, SW, SH); c.globalAlpha = stat * .5; for (let i = 0; i < 6; i++) { c.fillStyle = Math.random() > .5 ? '#000' : '#cbb8ff'; c.fillRect(0, Math.random() * SH, SW, 2 + Math.random() * 10); } c.globalAlpha = 1; }
    // curvature vignette
    const v = c.createRadialGradient(SW / 2, SH / 2, SW * .28, SW / 2, SH / 2, SW * .62); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,.6)'); c.fillStyle = v; c.fillRect(0, 0, SW, SH);
    c.restore(); screenTex.needsUpdate = true;
  };

  // layout: the stand top sits a little above the partner strip, robot sized to the grid
  let k = 100, cw = 1, ch = 1;
  const layout = () => {
    cw = cv.clientWidth; ch = cv.clientHeight; renderer.setSize(cw, ch, false);
    strip.style.setProperty('--cellw', (strip.clientWidth / (innerWidth <= 900 ? 2 : 4)) + 'px');
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
  const FIX = (() => { const v = new URLSearchParams(location.search).get('rbt'); return v == null ? null : +v; })();   // ?rbt=5 freezes the loop at 5 s (for reviewing a pose)
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

      // scroll: the stage is pinned; scrolling first brings the robot to attention (up, facing you, showing the mark),
      // then the camera dives into its screen and the end frame takes over
      const small = innerWidth <= 900;
      const hr = hero.getBoundingClientRect(), total = hero.offsetHeight - pin.offsetHeight;
      const p = small || reduce ? 0 : Math.min(Math.max(-hr.top / Math.max(total, 1), 0), 1);
      const sE = ease(seg(p, 0, .1)), z = ease(seg(p, .1, .62));
      const mix = (a, b) => a + (b - a) * sE;

      // robot timeline (reduced motion: stand still, facing front, eyes on)
      const t = FIX != null ? FIX : reduce ? 6.0 : T0 % L;
      const up = mix(ease(seg(t, .2, 1.4)) * (1 - ease(seg(t, 9.7, 10.85))), 1);
      bot.position.y = -(1 - up) * 3.3;
      bot.visible = up > .002;
      const powerOn = mix(ease(seg(t, 4.4, 5.0)) * (1 - ease(seg(t, 8.9, 9.5))), 1);
      const turnIn = back(seg(t, 4.8, 5.8)), turnOut = ease(seg(t, 8.9, 9.7));
      const rLoop = PROF * (1 - turnIn) + PROF * turnOut;
      const rH = mix(rLoop, 0) + cx * .14 * powerOn * (1 - z);
      const jolt = Math.sin(seg(t, 3.15, 3.75) * Math.PI) * (1 - sE);
      head.rotation.y = rH;
      head.rotation.x = cy * .06 * powerOn * (1 - z);
      head.rotation.z = jolt * .05;
      head.position.y = 1.06 + .95 - jolt * .1;
      world.rotation.set(.16 * (1 - z), -.16 * (1 - z), 0);

      // arm + chip: the chip comes down facing front, then twists to line up with the slot and drops in
      const headTop = bot.position.y + head.position.y + .95;
      const d1 = out(seg(t, 1.3, 2.4)), tw2 = ease(seg(t, 2.25, 2.75)), ins = ease(seg(t, 2.75, 3.25)), lift = ease(seg(t, 3.5, 4.6));
      const high = headTop + ARM_HIGH, hover = headTop + 1.0, seated = headTop - .2;
      let chipY = high + (hover - high) * d1 + (seated - hover) * ins;
      let armY = t < 3.35 ? chipY : seated + (high + 2 - seated) * lift;
      armY += (high + 4 - armY) * sE; if (t < 3.35) chipY = armY;
      const rC = rLoop * tw2;                                  // chip/arm turn to the head's angle before inserting
      const ox = Math.sin(rLoop) * .1 * tw2, oz = Math.cos(rLoop) * .1 * tw2 + .1 * (1 - tw2);
      chip.position.set(ox, chipY, oz); chip.rotation.y = rC; chip.visible = t > 1.2 && t < 3.35;
      arm.position.set(ox, armY, oz); arm.rotation.y = rC; arm.visible = t > 1.2 && t < 4.7 && sE < .99;

      ringM2.emissiveIntensity = .03 + powerOn * 1.05;
      slotM2.opacity = Math.max(ease(seg(t, 3.2, 3.6)) * (1 - ease(seg(t, 9.5, 10))), sE) * (.7 + .3 * Math.sin(T0 * 6));
      glowLight.intensity = powerOn * 1.6;
      // face
      const eyesOn = mix(ease(seg(t, 5.0, 5.4)) * (1 - ease(seg(t, 6.6, 6.9))) + ease(seg(t, 7.8, 8.1)) * (1 - ease(seg(t, 8.8, 9.1))), 0);
      const mark = mix(ease(seg(t, 6.8, 7.1)) * (1 - ease(seg(t, 7.7, 8.0))), 1);
      const look = t < 6.6 ? Math.sin((t - 5) * 2.2) * .5 : 0;
      const blinkT = [5.9, 8.4].reduce((b, bt) => Math.max(b, Math.sin(seg(t, bt, bt + .22) * Math.PI)), 0);
      drawScreen(T0, powerOn, eyesOn, mark, look + cx * .4, cy * .3, blinkT, ease(seg(p, .34, .6)));

      // clip plane = the top of the stand, in camera space
      scene.updateMatrixWorld();
      world.getWorldQuaternion(_q); _n.set(0, 1, 0).applyQuaternion(_q); world.localToWorld(_p.set(0, 0, 0));
      clipPlane.setFromNormalAndCoplanarPoint(_n, _p);

      // camera dive into the screen
      screen.getWorldPosition(_s);
      const zEnd = Math.max(cw / (1.26 * k), ch / (1.1 * k)) * 1.3;
      cam.zoom = Math.pow(zEnd, z); cam.position.set(_s.x * z, _s.y * z, 2000); cam.updateProjectionMatrix();
      hero.classList.toggle('is-zoom', z > .001);
      const fo = (1 - seg(p, .12, .45)).toFixed(3);
      fades.forEach((el) => { el.style.opacity = fo; });
      if (endNoise) { const nv = seg(p, .6, .64) * (1 - seg(p, .68, .84)); endNoise.style.opacity = nv.toFixed(3); if (nv > 0) { const x2 = endNoise.getContext('2d'); x2.imageSmoothingEnabled = false; x2.drawImage(noiseTile(), 0, 0, endNoise.width, endNoise.height); } }
      if (endEl) { const e = ease(seg(p, .6, .66)); endEl.style.opacity = e.toFixed(3); endEl.style.visibility = e > .01 ? 'visible' : 'hidden'; endEl.style.pointerEvents = e > .9 ? 'auto' : 'none'; }
      renderer.render(scene, cam);
    }
    requestAnimationFrame(loop);
  })(last);
})();
