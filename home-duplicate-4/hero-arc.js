/* Hero (card arc): places the cards on an arc and turns the ring with the scroll position.
   Cards wrap around a full circle; the lower half is hidden off the bottom of the stage. */
(function () {
  var hero = document.getElementById('hero');
  var stage = hero && hero.querySelector('.ar-stage');
  var cards = hero ? Array.prototype.slice.call(hero.querySelectorAll('.ar-card')) : [];
  if (!stage || !cards.length) return;

  var N = cards.length, STEP = 360 / N;
  var TURN = STEP * 6;                          // how far the ring turns over the whole scroll
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var w = 0, h = 0, cx = 0, cy = 0, R = 0;

  function measure() {
    w = stage.clientWidth; h = stage.clientHeight;
    cx = w / 2; cy = h * (w < 700 ? .47 : .68);
    R = Math.min(w * (w < 700 ? .5 : .43), h * .5);
  }

  function progress() {
    var r = hero.getBoundingClientRect();
    var total = hero.offsetHeight - stage.offsetHeight;
    return total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
  }

  function render() {
    var p = reduce ? 0 : progress();
    for (var i = 0; i < N; i++) {
      // angle in degrees measured from the right, counter-clockwise; scrolling moves cards left to right
      var a = 196 - i * STEP - p * TURN;
      a = ((a + 60) % 360 + 360) % 360 - 60;      // wrap to [-60, 300)
      var rad = a * Math.PI / 180;
      var x = cx + R * Math.cos(rad), y = cy - R * Math.sin(rad);
      var rot = 90 - a;                           // tangent to the arc, like cards on a wheel
      var edge = Math.max(0, Math.min(1, (a + 12) / 28, (192 - a) / 28));   // fade out below the horizon
      var k = 0.86 + 0.14 * Math.sin(Math.max(0, Math.min(Math.PI, rad)));  // slightly larger at the top
      var c = cards[i];
      c.style.setProperty('--x', x.toFixed(1) + 'px');
      c.style.setProperty('--y', y.toFixed(1) + 'px');
      c.style.setProperty('--r', rot.toFixed(1) + 'deg');
      c.style.setProperty('--k', k.toFixed(3));
      c.style.setProperty('--o', edge.toFixed(3));
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
