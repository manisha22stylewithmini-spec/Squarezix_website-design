/* Hero (card arc), scroll-driven in three stages while the stage sticks:
   1. opening screen: highlighted title + a fan of 4 cards + CTA (all other cards hidden behind the fan)
   2. first scroll: the intro fades, every card travels from the fan onto a curved arc and the arc lines draw in
   3. further scroll: the ring turns and rises, and the main copy + three points fade in mid-screen
   Cards wrap round a full circle; the lower half fades out below the horizon. */
(function () {
  var hero = document.getElementById('hero');
  var stage = hero && hero.querySelector('.ar-stage');
  var cards = hero ? Array.prototype.slice.call(hero.querySelectorAll('.ar-card')) : [];
  if (!stage || !cards.length) return;
  var lines = Array.prototype.slice.call(stage.querySelectorAll('.ar-line'));
  var LINE_SCALE = [1, .72, 1.22];             // main line through the cards, an inner and an outer echo

  var N = cards.length, STEP = 360 / N;
  var TURN = STEP * 5;                          // how far the ring turns during stage 3
  var FAN = [2, 3, 7, 8];                       // cards shown in the opening fan, left to right
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var w = 0, h = 0, cx = 0, cy = 0, R = 0, s = 160, rowY = 0, lift = 0, phone = false;

  FAN.forEach(function (i) { if (cards[i]) cards[i].style.zIndex = 2; });

  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function lerp(a, b, t) { return a + (b - a) * t; }

  function measure() {
    w = stage.clientWidth; h = stage.clientHeight; phone = w < 700;
    cx = w / 2; cy = h * (phone ? .47 : .68);
    R = Math.min(w * (phone ? .5 : .43), h * .5);
    s = cards[0].offsetWidth || 160;
    rowY = h * (phone ? .52 : .64);
    lift = h * (phone ? .1 : .14);
    stage.style.setProperty('--s-fan', s + 'px');
    stage.style.setProperty('--row', rowY + 'px');
  }

  function progress() {
    var r = hero.getBoundingClientRect();
    var total = hero.offsetHeight - stage.offsetHeight;
    return total > 0 ? clamp(-r.top / total) : 0;
  }

  function arcPath(c, radius) {
    var a0 = 200 * Math.PI / 180, a1 = -20 * Math.PI / 180;
    var x0 = cx + radius * Math.cos(a0), y0 = c - radius * Math.sin(a0);
    var x1 = cx + radius * Math.cos(a1), y1 = c - radius * Math.sin(a1);
    return 'M' + x0.toFixed(1) + ' ' + y0.toFixed(1) + ' A' + radius.toFixed(1) + ' ' + radius.toFixed(1) + ' 0 1 1 ' + x1.toFixed(1) + ' ' + y1.toFixed(1);
  }

  function render() {
    var p = reduce ? .62 : progress();
    var intro = 1 - clamp((p - .02) / .16);           // opening screen fades out first
    var t1 = ease(clamp((p - .04) / .30));            // fan -> arc
    var t2 = clamp((p - .34) / .66);                  // ring turns and rises
    var main = clamp((p - .38) / .2);                 // main copy fades in
    var c = cy - t2 * lift;

    stage.style.setProperty('--intro', intro.toFixed(3));
    stage.style.setProperty('--main', main.toFixed(3));
    stage.style.setProperty('--main-pe', main > .6 ? 'auto' : 'none');

    for (var i = 0; i < N; i++) {
      // arc pose: angle from the right, counter-clockwise; scrolling moves cards left to right
      var a = 196 - i * STEP - t2 * TURN;
      a = ((a + 60) % 360 + 360) % 360 - 60;
      var rad = a * Math.PI / 180;
      var ax = cx + R * Math.cos(rad), ay = c - R * Math.sin(rad);
      var ar = 90 - a;
      var ao = clamp(Math.min((a + 12) / 28, (192 - a) / 28));
      var ak = .86 + .14 * Math.sin(Math.max(0, Math.min(Math.PI, rad)));

      // fan pose: 4 tilted cards in a row; the rest wait, hidden, behind the middle of the fan
      var j = FAN.indexOf(i), fx, fy, fr, fk, fo;
      if (j > -1) {
        var off = j - 1.5;
        fx = cx + off * s * .8; fy = rowY + Math.abs(off) * s * .06;
        fr = off * 6; fk = .86; fo = 1;
      } else {
        fx = cx; fy = rowY; fr = 0; fk = .7; fo = 0;
      }

      var el = cards[i];
      el.style.setProperty('--x', lerp(fx, ax, t1).toFixed(1) + 'px');
      el.style.setProperty('--y', lerp(fy, ay, t1).toFixed(1) + 'px');
      el.style.setProperty('--r', lerp(fr, ar, t1).toFixed(1) + 'deg');
      el.style.setProperty('--k', lerp(fk, ak, t1).toFixed(3));
      el.style.setProperty('--o', lerp(fo, ao, t1).toFixed(3));
    }

    for (var k = 0; k < lines.length; k++) {
      lines[k].setAttribute('d', arcPath(c, R * LINE_SCALE[k]));
      lines[k].style.setProperty('--draw', (1 - t1).toFixed(3));
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
})();
