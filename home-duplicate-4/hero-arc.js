/* Hero (card arc): one connected scroll scene while the stage sticks.
   First frame: title block on top, a fan of 4 cards, CTA at the bottom; the other cards sit stacked exactly
   behind the fan cards. Scrolling slides every card out from behind the fan onto a curve (arc lines draw in)
   while the title block travels down and the CTA travels up to meet in the middle of the arc. Then the ring
   keeps turning. Nothing fades: the ring is a full circle whose lower half runs off the bottom of the screen. */
(function () {
  var hero = document.getElementById('hero');
  var stage = hero && hero.querySelector('.ar-stage');
  var head = document.getElementById('ar-head');
  var cta = document.getElementById('ar-cta');
  var cards = hero ? Array.prototype.slice.call(hero.querySelectorAll('.ar-card')) : [];
  if (!stage || !head || !cta || !cards.length) return;
  var lines = Array.prototype.slice.call(stage.querySelectorAll('.ar-line'));
  var LINE_SCALE = [1, .74, 1.2];               // line through the cards, an inner and an outer echo

  var N = cards.length, STEP = 360 / N;
  var TURN = STEP * 4;                          // how far the ring turns after it has formed
  var FAN = [2, 3, 7, 8];                       // the cards on show in the first frame, left to right
  var FAN_K = .92;                              // fan card scale
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var w, h, phone, cx, cy, R, s, lift, headH, ctaH, headY0, ctaY0, rowY, hsF;

  cards.forEach(function (el, i) { el.style.zIndex = FAN.indexOf(i) > -1 ? 2 : 1; });

  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function lerp(a, b, t) { return a + (b - a) * t; }

  function measure() {
    w = stage.clientWidth; h = stage.clientHeight; phone = w < 700;
    s = cards[0].offsetWidth || 130;
    headH = head.offsetHeight; ctaH = cta.offsetHeight;
    var pad = h * (phone ? .06 : .07);
    headY0 = pad;                                 // first frame: title block at the top ...
    ctaY0 = h - pad - ctaH;                       // ... CTA at the bottom ...
    rowY = (headY0 + headH + ctaY0) / 2;          // ... and the fan centred between them
    cx = w / 2;
    cy = h * (phone ? .56 : .74);
    R = phone ? w * .66 : Math.min(w * .42, h * .6);
    lift = h * .05;
    hsF = phone ? .86 : .72;                       // title block scale once it sits inside the arc
  }

  function progress() {
    var r = hero.getBoundingClientRect();
    var total = hero.offsetHeight - stage.offsetHeight;
    return total > 0 ? clamp(-r.top / total) : 0;
  }

  // one half of an arc: from an end angle up to the top (90deg); left half sweeps clockwise, right half counter-clockwise
  function halfPath(c, radius, fromDeg, left) {
    var a0 = fromDeg * Math.PI / 180, a1 = Math.PI / 2;
    var x0 = cx + radius * Math.cos(a0), y0 = c - radius * Math.sin(a0);
    var x1 = cx, y1 = c - radius;
    return 'M' + x0.toFixed(1) + ' ' + y0.toFixed(1) + ' A' + radius.toFixed(1) + ' ' + radius.toFixed(1) + ' 0 0 ' + (left ? 1 : 0) + ' ' + x1.toFixed(1) + ' ' + y1.toFixed(1);
  }

  function render() {
    var p = reduce ? .42 : progress();
    var t1 = ease(clamp((p - .03) / .37));      // fan -> arc, content -> middle (one motion)
    var t2 = clamp((p - .42) / .58);            // ring turns and rises a little
    var c = cy - t2 * lift;

    // content: both halves travel to meet inside the arc
    var gap = phone ? 18 : 22;
    var total = headH * hsF + gap + ctaH;
    var topF = phone ? c - R * .55 : c - R * .64;
    stage.style.setProperty('--hy', lerp(headY0, topF, t1).toFixed(1) + 'px');
    stage.style.setProperty('--hs', lerp(1, hsF, t1).toFixed(3));
    stage.style.setProperty('--ctay', lerp(ctaY0, topF + total - ctaH, t1).toFixed(1) + 'px');

    for (var i = 0; i < N; i++) {
      // arc pose: angle from the right, counter-clockwise; scrolling moves cards left to right
      var a = 196 - i * STEP - t2 * TURN;
      var rad = a * Math.PI / 180;
      var ax = cx + R * Math.cos(rad), ay = c - R * Math.sin(rad);
      var ar = 90 - a;

      // fan pose: the 4 fan cards in a tilted row; every other card waits exactly behind one of them
      var j = FAN.indexOf(i), slot = j > -1 ? j : i % 4, off = slot - 1.5;
      var fx = cx + off * s * .84, fy = rowY + Math.abs(off) * s * .06, fr = off * 6;
      var fk = j > -1 ? FAN_K : FAN_K * .96;

      var el = cards[i];
      el.style.setProperty('--x', lerp(fx, ax, t1).toFixed(1) + 'px');
      el.style.setProperty('--y', lerp(fy, ay, t1).toFixed(1) + 'px');
      el.style.setProperty('--r', lerp(fr, ar, t1).toFixed(1) + 'deg');
      el.style.setProperty('--k', lerp(fk, 1, t1).toFixed(3));
    }

    // outlines grow from both ends at once and meet at the top
    var d = (1 - t1).toFixed(3), hide = t1 < .005 ? 'hidden' : 'visible';
    for (var k = 0; k < lines.length; k++) {
      var left = lines[k].classList.contains('side-l');
      var radius = R * LINE_SCALE[Math.floor(k / 2)];
      lines[k].setAttribute('d', halfPath(c, radius, left ? 200 : -20, left));
      lines[k].style.setProperty('--draw', d);
      lines[k].style.visibility = hide;
    }
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { ticking = false; render(); });
  }

  measure(); render();
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', function () { measure(); render(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { measure(); render(); });
})();
