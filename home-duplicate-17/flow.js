// Hero (brief -> collaboration -> output). The centre tile is a real 3D object (three.js): a dark plate with a glossy purple slab on
// top, a white Squarezix mark and a ring of words turning on its face, a light sweep, a soft halo. It floats and tilts toward the pointer.
// The stage is pinned: scrolling pushes the camera straight into the tile until its face fills the stage, then the
// "Welcome to the inside of Squarezix" frame takes over and the page carries on.
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hero = document.getElementById('hero');
  const cv = document.getElementById('fp-gl');
  const plate = document.getElementById('fp-plate');
  const endEl = document.getElementById('fp-end');
  const T = window.THREE;
  if (!hero || !cv || !plate || !T) return;
  const stage = hero.querySelector('.fp-stage');
  const fade = hero.querySelectorAll('.fp-head, .fp-lane, .fp-cap-core');
  const small = () => matchMedia('(max-width: 700px)').matches;

  const renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  const scene = new T.Scene();
  const cam = new T.PerspectiveCamera(32, 1, .05, 80); const CZ = 10; cam.position.set(0, 0, CZ);
  scene.add(new T.HemisphereLight(0xffffff, 0x4a2a9a, .8));
  const key = new T.DirectionalLight(0xffffff, 1.5); key.position.set(-3, 5, 6); scene.add(key);
  const rim = new T.DirectionalLight(0xd070ff, 1.6); rim.position.set(5, -2, -3); scene.add(rim);
  const pt = new T.PointLight(0xb040ff, 1.6, 9); pt.position.set(0, -1.2, 2); scene.add(pt);

  const rr = (w, h, r) => { const s = new T.Shape(), a = -w / 2, b = -h / 2; s.moveTo(a + r, b); s.lineTo(-a - r, b); s.quadraticCurveTo(-a, b, -a, b + r); s.lineTo(-a, -b - r); s.quadraticCurveTo(-a, -b, -a - r, -b); s.lineTo(a + r, -b); s.quadraticCurveTo(a, -b, a, -b - r); s.lineTo(a, b + r); s.quadraticCurveTo(a, b, a + r, b); return s; };
  const slab = (w, h, d, r, bev, mat) => { const g = new T.ExtrudeGeometry(rr(w - 2 * bev, h - 2 * bev, r - bev), { depth: d - 2 * bev, bevelEnabled: true, bevelThickness: bev, bevelSize: bev, bevelSegments: 6, curveSegments: 14 }); g.translate(0, 0, -(d - 2 * bev) / 2); return new T.Mesh(g, mat); };

  const g = new T.Group(); scene.add(g);
  // halo behind everything
  const hc = document.createElement('canvas'); hc.width = hc.height = 256; const hx = hc.getContext('2d');
  const hg = hx.createRadialGradient(128, 128, 0, 128, 128, 128); hg.addColorStop(0, 'rgba(171,36,242,.75)'); hg.addColorStop(.45, 'rgba(98,29,208,.28)'); hg.addColorStop(1, 'rgba(98,29,208,0)'); hx.fillStyle = hg; hx.fillRect(0, 0, 256, 256);
  const halo = new T.Mesh(new T.PlaneGeometry(2.7, 2.7), new T.MeshBasicMaterial({ map: new T.CanvasTexture(hc), transparent: true, depthWrite: false, blending: T.AdditiveBlending })); halo.position.z = -.45; g.add(halo);
  // dark plate (1.34 wide) and the tile slab standing proud of it
  const plateM = slab(1.34, 1.34, .26, .3, .06, new T.MeshStandardMaterial({ color: 0x0b0814, roughness: .55, metalness: .3 })); plateM.position.z = -.08; g.add(plateM);
  const tileM = slab(1, 1, .3, .26, .06, new T.MeshStandardMaterial({ color: 0x6a24d8, roughness: .28, metalness: .35, emissive: 0x2a0a70, emissiveIntensity: .8 })); tileM.position.z = .22; g.add(tileM);

  // the face texture
  const FS = 1024, fc = document.createElement('canvas'); fc.width = fc.height = FS; const f = fc.getContext('2d');
  const faceTex = new T.CanvasTexture(fc); faceTex.anisotropy = 8;
  const face = new T.Mesh(new T.PlaneGeometry(.96, .96), new T.MeshBasicMaterial({ map: faceTex, transparent: true })); face.position.z = .22 + .15 + .065 + .001; g.add(face);
  let logoW = null;
  const li = new Image(); li.onload = () => { const o = document.createElement('canvas'); o.width = o.height = 241; const c = o.getContext('2d'); c.drawImage(li, 0, 0); c.globalCompositeOperation = 'source-in'; c.fillStyle = '#fff'; c.fillRect(0, 0, 241, 241); logoW = o; }; li.src = 'assets/brand/sz-logo-on-dark.png';
  const WORDS = 'WEBSITES  ✦  CONTENT  ✦  ADS  ✦  SEO  ✦  BRAND  ✦  REELS  ✦  ';
  const drawFace = (t) => {
    f.clearRect(0, 0, FS, FS);
    f.save(); f.beginPath(); f.roundRect(0, 0, FS, FS, 250); f.clip();
    const gr = f.createLinearGradient(0, 0, FS, FS); gr.addColorStop(0, '#5a18c8'); gr.addColorStop(.55, '#8a24ee'); gr.addColorStop(1, '#c23ff7'); f.fillStyle = gr; f.fillRect(0, 0, FS, FS);
    const hl = f.createRadialGradient(FS * .3, FS * .12, 0, FS * .3, FS * .12, FS * .8); hl.addColorStop(0, 'rgba(255,255,255,.42)'); hl.addColorStop(1, 'rgba(255,255,255,0)'); f.fillStyle = hl; f.fillRect(0, 0, FS, FS);
    // moving light sweep
    const sx = ((t * .18) % 1.8 - .4) * FS * 1.6 - FS * .3; f.save(); f.translate(sx, 0); f.rotate(.5); const sw = f.createLinearGradient(0, 0, 200, 0); sw.addColorStop(0, 'rgba(255,255,255,0)'); sw.addColorStop(.5, 'rgba(255,255,255,.2)'); sw.addColorStop(1, 'rgba(255,255,255,0)'); f.fillStyle = sw; f.fillRect(0, -FS, 200, FS * 3); f.restore();
    // inner edge
    f.lineWidth = 10; f.strokeStyle = 'rgba(255,255,255,.28)'; f.beginPath(); f.roundRect(8, 8, FS - 16, FS - 16, 242); f.stroke();
    // ring of words
    f.save(); f.translate(FS / 2, FS / 2); f.rotate(t * .12); f.fillStyle = '#fff'; f.shadowColor = 'rgba(40,0,110,.55)'; f.shadowBlur = 10; f.font = '700 52px Sora, sans-serif'; f.textAlign = 'center'; f.textBaseline = 'middle';
    const R = FS * .385, n = WORDS.length; for (let i = 0; i < n; i++) { f.save(); f.rotate(i / n * Math.PI * 2); f.translate(0, -R); f.fillText(WORDS[i], 0, 0); f.restore(); }
    f.restore();
    // the mark, in white
    if (logoW) { const w = FS * .5, sh = 127 / 241; f.save(); f.shadowColor = 'rgba(255,255,255,.55)'; f.shadowBlur = 30; f.drawImage(logoW, 0, 114, 241, 127, (FS - w) / 2, FS / 2 - w * sh / 2 + FS * .015, w, w * sh); f.restore(); }
    f.restore(); faceTex.needsUpdate = true;
  };

  const ease = (t) => t * t * (3 - 2 * t);
  const seg = (v, a, b) => Math.min(Math.max((v - a) / (b - a), 0), 1);
  let baseS = 1, tx = 0, ty = 0, cw = 1, ch = 1;
  const UPP = () => (2 * CZ * Math.tan(16 * Math.PI / 180)) / ch;
  const layout = () => {
    cw = cv.clientWidth; ch = cv.clientHeight; renderer.setSize(cw, ch, false); cam.aspect = cw / ch; cam.updateProjectionMatrix();
    const a = plate.getBoundingClientRect(), b = cv.getBoundingClientRect(), u = UPP();
    baseS = a.width * u / 1.34; tx = (a.left + a.width / 2 - b.left - cw / 2) * u; ty = -((a.top + a.height / 2 - b.top) - ch / 2) * u;
  };
  addEventListener('resize', layout); (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(layout);
  let px = 0, py = 0, cx = 0, cy = 0, inView = true, last = performance.now();
  hero.addEventListener('pointermove', (ev) => { const r = hero.getBoundingClientRect(); px = (ev.clientX - r.left) / r.width * 2 - 1; py = Math.max(-1, Math.min(1, (ev.clientY - r.top) / Math.min(r.height, innerHeight) * 2 - 1)); });
  new IntersectionObserver(([en]) => { inView = en.isIntersecting; }).observe(hero);

  (function loop(now) {
    if (inView) {
      layout();
      const r = hero.getBoundingClientRect(), total = hero.offsetHeight - stage.offsetHeight;
      const p = small() || reduce ? 0 : Math.min(Math.max(-r.top / Math.max(total, 1), 0), 1);
      const z = ease(seg(p, .04, .6)), t = now / 1000;
      cx += (px - cx) * .07; cy += (py - cy) * .07;
      g.scale.setScalar(baseS); g.position.set(tx, ty + Math.sin(t * 1.2) * .035 * baseS * (1 - z), 0);
      const k = 1 - z;
      g.rotation.y = (cx * .38 + Math.sin(t * .7) * .1) * k;
      g.rotation.x = (cy * .26 + Math.cos(t * .6) * .06) * k;
      // camera dives to just in front of the face, which then overfills the stage
      const faceZ = (.22 + .15 + .065) * baseS, dEnd = .72 * baseS * .96;
      const dz = CZ + (faceZ + dEnd - CZ) * Math.pow(z, .85);
      cam.position.set(tx * z, ty * z, dz);
      pt.position.set(tx, ty - 1.2 * baseS, 2 * baseS);
      drawFace(t);
      fade.forEach((el) => { el.style.opacity = (1 - seg(p, .08, .42)).toFixed(3); });
      if (endEl) { const e = ease(seg(p, .6, .72)); endEl.style.opacity = e.toFixed(3); endEl.style.visibility = e > .01 ? 'visible' : 'hidden'; endEl.style.pointerEvents = e > .9 ? 'auto' : 'none'; }
      renderer.render(scene, cam);
    }
    requestAnimationFrame(loop);
  })(last);
})();
