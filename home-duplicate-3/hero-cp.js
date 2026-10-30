/* Hero (copilot lab): leans the card stack a few degrees toward the pointer. */
(function () {
  var hero = document.getElementById('hero');
  var stack = hero && hero.querySelector('.cp-stack');
  if (!stack) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !matchMedia('(hover: hover)').matches) return;
  var base = 'rotateY(-24deg) rotateX(7deg) rotateZ(-2deg)';
  hero.addEventListener('pointermove', function (e) {
    var r = hero.getBoundingClientRect();
    var x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
    stack.style.transform = 'rotateY(' + (-24 + x * 8).toFixed(2) + 'deg) rotateX(' + (7 - y * 6).toFixed(2) + 'deg) rotateZ(-2deg)';
  });
  hero.addEventListener('pointerleave', function () { stack.style.transform = base; });
})();
