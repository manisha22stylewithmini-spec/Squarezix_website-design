// Hero (desk scene). One scroll value p (0 -> 1) while .ds-stage is stuck:
//   copy steps aside -> the camera pushes into the phone (photo zoom + pan, centred on the screen)
//   -> the screen turns flat to the camera and fills the view -> the page inside it keeps scrolling.
// The phone screen is a real 390x844 page, mapped onto the photo's screen quad with a CSS matrix3d,
// so it stays sharp at any zoom. Nothing fades or blurs; everything is reversible.
(() => {
  const hero = document.getElementById('hero');
  const stage = hero && hero.querySelector('.ds-stage');
  const media = stage && stage.querySelector('.ds-media');
  const screen = stage && stage.querySelector('.ds-screen');
  const feed = stage && stage.querySelector('.ds-feed');
  const copy = stage && stage.querySelector('.ds-copy');
  const shade = stage && stage.querySelector('.ds-shade');
  const dim = stage && stage.querySelector('.ds-dim');
  if (!media || !screen || !feed) return;

  // Where the phone's screen sits in the photo, as fractions of the image (TL, TR, BR, BL).
  // Retune these four points when the final shot replaces assets/hero/bench-shot.jpg.
  const QUAD = [[.5250, .4559], [.5340, .4576], [.5260, .4783], [.5177, .4764]];
  // The thumb covers the lower part of the real screen, so QUAD is only the part you can see. VIS says how much of
  // the page (top to bottom) that part shows; the rest of the page is clipped away and comes back as the screen flattens.
  const VIS = 585 / 844;
  const SW = 390, SH = 844;                       // the page inside the phone, in its own px
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const clamp = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
  const seg = (p, a, b) => clamp((p - a) / (b - a));
  const ease = (t) => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const lerp = (a, b, t) => a + (b - a) * t;
  const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);

  let W, H, mw, mh, ml, mt, corners, sc, wq, zEnd, feedMax, N;

  function measure() {
    W = stage.clientWidth; H = stage.clientHeight;
    stage.style.setProperty('--stage-h', H + 'px');
    mw = media.offsetWidth; mh = media.offsetHeight;
    ml = (W - mw) / 2; mt = (H - mh) / 2;
    corners = QUAD.map(([x, y]) => [x * mw, y * mh]);
    sc = [corners.reduce((s, c) => s + c[0], 0) / 4, corners.reduce((s, c) => s + c[1], 0) / 4];
    wq = (dist(corners[0], corners[1]) + dist(corners[3], corners[2])) / 2;
    zEnd = W * 1.04 / wq;                         // flat screen ends up a touch wider than the stage
    feedMax = Math.max(0, feed.offsetHeight - SH * .66);   // runs far enough that the closing line reaches the middle band
    N = W < 700 ? [W * .56, H * .4] : [ml + sc[0] + W * .09, mt + sc[1]];   // on desktop the shot sits a little right, clear of the copy   // where the screen rests before scrolling
    render(progress());
  }

  function progress() {
    const r = hero.getBoundingClientRect();
    const total = hero.offsetHeight - stage.offsetHeight;
    return total > 0 ? clamp(-r.top / total) : 0;
  }

  // 4-point homography: unit page rect -> quad, as a CSS matrix3d
  function matrixFor(q) {
    const s = [[0, 0], [SW, 0], [SW, SH], [0, SH]];
    const A = [], b = [];
    for (let i = 0; i < 4; i++) {
      const [x, y] = s[i], [u, v] = q[i];
      A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.push(u);
      A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); b.push(v);
    }
    for (let i = 0; i < 8; i++) {                  // gaussian elimination
      let m = i;
      for (let r = i + 1; r < 8; r++) if (Math.abs(A[r][i]) > Math.abs(A[m][i])) m = r;
      [A[i], A[m]] = [A[m], A[i]]; [b[i], b[m]] = [b[m], b[i]];
      for (let r = i + 1; r < 8; r++) {
        const f = A[r][i] / A[i][i];
        for (let c = i; c < 8; c++) A[r][c] -= f * A[i][c];
        b[r] -= f * b[i];
      }
    }
    const h = new Array(8);
    for (let i = 7; i >= 0; i--) {
      let v = b[i];
      for (let c = i + 1; c < 8; c++) v -= A[i][c] * h[c];
      h[i] = v / A[i][i];
    }
    const [a, bb, c, d, e, f, g, hh] = h;
    return `matrix3d(${a},${d},0,${g},${bb},${e},0,${hh},0,0,1,0,${c},${f},0,1)`;
  }

  function render(p) {
    if (!W) return;
    const pp = reduce ? 0 : p;

    // copy steps aside first
    const out = ease(seg(pp, 0, .16));
    if (copy) { copy.style.opacity = (1 - out).toFixed(3); copy.style.transform = `translate3d(${(-out * 48).toFixed(1)}px,0,0)`; copy.style.pointerEvents = out > .5 ? 'none' : ''; }
    if (shade) shade.style.opacity = (1 - ease(seg(pp, .04, .4))).toFixed(3);

    // camera: pan the screen to the middle of the stage while zooming in on it
    const pan = ease(seg(pp, .03, .5));
    const z = Math.exp(Math.log(zEnd) * ease(seg(pp, .03, .62)));
    const tx = lerp(N[0], W / 2, pan) - ml - z * sc[0];
    const ty = lerp(N[1], H / 2, pan) - mt - z * sc[1];
    media.style.transform = `translate3d(${tx.toFixed(2)}px,${ty.toFixed(2)}px,0) scale(${z.toFixed(4)})`;

    // screen quad on stage: the visible part, extended down to the full page, then eased toward a flat upright rectangle
    const Pv = corners.map(([x, y]) => [ml + tx + z * x, mt + ty + z * y]);
    const k = 1 / VIS;
    const P = [Pv[0], Pv[1],
      [Pv[1][0] + k * (Pv[2][0] - Pv[1][0]), Pv[1][1] + k * (Pv[2][1] - Pv[1][1])],
      [Pv[0][0] + k * (Pv[3][0] - Pv[0][0]), Pv[0][1] + k * (Pv[3][1] - Pv[0][1])]];
    const wp = (dist(P[0], P[1]) + dist(P[3], P[2])) / 2;
    const flat = ease(seg(pp, .26, .68));
    const cx = lerp(P.reduce((s, c) => s + c[0], 0) / 4, W / 2, flat), cy = lerp(P.reduce((s, c) => s + c[1], 0) / 4, H / 2, flat);
    const fw = wp, fh = wp * SH / SW;
    const F = [[cx - fw / 2, cy - fh / 2], [cx + fw / 2, cy - fh / 2], [cx + fw / 2, cy + fh / 2], [cx - fw / 2, cy + fh / 2]];
    const Q = P.map((c, i) => [lerp(c[0], F[i][0], flat), lerp(c[1], F[i][1], flat)]);
    screen.style.transform = matrixFor(Q);
    screen.style.clipPath = `inset(-120px -120px ${((1 - lerp(VIS, 1, flat)) * 100).toFixed(2)}% -120px)`;
    screen.style.borderRadius = lerp(16, 0, ease(seg(pp, .5, .72))).toFixed(1) + 'px';
    if (dim) dim.style.opacity = (.92 * ease(seg(pp, .1, .5))).toFixed(3);
    screen.style.visibility = 'visible';

    // the page inside keeps scrolling the whole way
    feed.style.transform = `translate3d(0,${(-feedMax * ease(seg(pp, .1, .94))).toFixed(1)}px,0)`;
  }

  let ticking = false;
  addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { ticking = false; render(progress()); });
  }, { passive: true });
  addEventListener('resize', measure);
  const img = media.querySelector('img');
  if (img && !img.complete) img.addEventListener('load', measure);
  measure();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
})();
