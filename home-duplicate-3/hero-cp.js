/* Hero (copilot lab): gentle pointer parallax. The card stack leans a couple of degrees and the tool tiles
   drift a few pixels (front row more than back row, via --px/--py on .cp-tools). */
(function () {
  var hero = document.getElementById('hero');
  var stack = hero && hero.querySelector('.cp-stack');
  var tools = hero && hero.querySelector('.cp-tools');
  if (!stack) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !matchMedia('(hover: hover)').matches) return;
  var base = 'rotateY(-24deg) rotateX(7deg) rotateZ(-2deg)';
  hero.addEventListener('pointermove', function (e) {
    var r = hero.getBoundingClientRect();
    var x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
    stack.style.transform = 'rotateY(' + (-24 + x * 4).toFixed(2) + 'deg) rotateX(' + (7 - y * 3).toFixed(2) + 'deg) rotateZ(-2deg)';
    if (tools) { tools.style.setProperty('--px', (x * 2).toFixed(3)); tools.style.setProperty('--py', (y * 2).toFixed(3)); }
  });
  hero.addEventListener('pointerleave', function () {
    stack.style.transform = base;
    if (tools) { tools.style.setProperty('--px', 0); tools.style.setProperty('--py', 0); }
  });
})();
