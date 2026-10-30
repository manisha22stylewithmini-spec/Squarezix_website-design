/* Hero (3D lab): builds the scrolling statement on the three walls, mirrors the room for the floor
   reflection, scales the 1000x562 stage to fit, and leans the room a few degrees toward the pointer. */
(function () {
  var hero = document.getElementById('hero');
  var room = document.getElementById('h3-room');
  var reflect = document.getElementById('h3-reflect');
  if (!hero || !room) return;

  var W = 520;            // wall width (room depth and width are equal so one line wraps the corner)
  var SPEED = 70;         // px per second
  var UNIT = '<span class="h3-unit"><span>We design </span><em>brands</em><span>&nbsp;people remember, build </span><em>websites</em><span>&nbsp;that perform, and </span><em>grow</em><span>&nbsp;your business with search, social and AI</span></span><span class="h3-dot"></span>';

  var lines = room.querySelectorAll('.h3-line');
  var wallIndex = { right: 0, back: 1, left: 2 };   // order the text visits the walls

  // Measure one unit so the loop period P is exact
  var probe = document.createElement('div');
  probe.className = 'h3-line';
  probe.style.visibility = 'hidden';
  probe.innerHTML = '<div class="h3-run">' + UNIT + '</div>';
  room.querySelector('.h3-face').appendChild(probe);
  var P = probe.querySelector('.h3-run').offsetWidth;
  probe.remove();
  if (!P || P < 200) P = 1800;

  var copies = Math.ceil((W + 2 * P) / P) + 1;
  var unitsHtml = new Array(copies + 1).join(UNIT);
  var dur = (P / SPEED).toFixed(2) + 's';
  room.style.setProperty('--P', P + 'px');
  room.style.setProperty('--dur', dur);

  for (var i = 0; i < lines.length; i++) {
    var k = wallIndex[lines[i].getAttribute('data-wall')] || 0;
    var shift = ((k * W) % P) - P;                  // phase of this wall within the repeating line
    lines[i].style.marginLeft = shift + 'px';
    lines[i].innerHTML = '<div class="h3-run">' + unitsHtml + '</div>';
  }

  // Mirrored copy for the floor reflection (same markup, same animations, starts in the same frame)
  if (reflect) {
    reflect.innerHTML = '';
    var clone = room.cloneNode(true);
    clone.removeAttribute('id');
    clone.style.transition = 'none';
    reflect.appendChild(clone);
    reflect._room = clone;
  }

  // Scale the 1000x562 stage into the space above the foot
  var fit = hero.querySelector('.h3-fit');
  function resize() {
    var vw = fit.clientWidth, vh = fit.clientHeight;
    var s = Math.min(vw / 1000, vh / 562);
    if (vw < 700) s = Math.min(vh / 562, (vw / 1000) * 1.9);   // phones: crop the sides, keep the text legible
    s = Math.max(.3, Math.min(s, 1.35));
    hero.style.setProperty('--s', s.toFixed(3));
  }
  resize();
  addEventListener('resize', resize);
  if (window.ResizeObserver) new ResizeObserver(resize).observe(fit);

  // Pointer lean
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches && matchMedia('(hover: hover)').matches) {
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      var rx = (x * 8).toFixed(2), ry = (y * 5).toFixed(2);
      room.style.setProperty('--rx', rx); room.style.setProperty('--ry', ry);
      if (reflect && reflect._room) { reflect._room.style.setProperty('--rx', rx); reflect._room.style.setProperty('--ry', ry); }
    });
    hero.addEventListener('pointerleave', function () {
      room.style.setProperty('--rx', 0); room.style.setProperty('--ry', 0);
      if (reflect && reflect._room) { reflect._room.style.setProperty('--rx', 0); reflect._room.style.setProperty('--ry', 0); }
    });
  }
})();
