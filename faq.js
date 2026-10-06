// Service-page FAQs: answers slide open and shut, one at a time.
// Mouse: hovering a question opens it; moving the cursor off that question closes it again.
// Touch and keyboard: tap / Enter toggles it.
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const EASE = 'cubic-bezier(.2, .8, .2, 1)';

  document.querySelectorAll('.ss-faq-list').forEach((list) => {
    const items = [...list.querySelectorAll('.ss-q')];
    const body = (d) => d.querySelector('.ss-a');

    // Slide the answer between its current height and the target, so a change of mind
    // halfway (hover in, hover out) carries on smoothly from wherever it is
    const slide = (d, opening) => {
      const a = body(d);
      const from = d.open ? a.getBoundingClientRect().height : 0;
      d._anim?.cancel();
      if (opening) d.open = true;
      d.classList.toggle('is-open', opening);
      const to = opening ? a.scrollHeight : 0;
      d._anim = a.animate(
        [{ height: `${from}px`, opacity: from ? 1 : 0 }, { height: `${to}px`, opacity: opening ? 1 : 0 }],
        { duration: reduce ? 0 : opening ? 420 : 340, easing: EASE },
      );
      d._anim.onfinish = () => {
        d._anim = null;
        if (!opening) d.open = false;
      };
    };
    const open = (d) => {
      items.forEach((x) => { if (x !== d && x.classList.contains('is-open')) slide(x, false); });
      if (!d.classList.contains('is-open')) slide(d, true);
    };
    const close = (d) => { if (d.classList.contains('is-open')) slide(d, false); };

    let timer;
    items.forEach((d) => {
      if (d.open) d.classList.add('is-open');
      d.querySelector('summary').addEventListener('click', (e) => {
        e.preventDefault();                       // we open and close it ourselves, animated
        d.classList.contains('is-open') ? close(d) : open(d);
      });
      d.addEventListener('pointerenter', (e) => {
        if (e.pointerType !== 'mouse') return;
        clearTimeout(timer);
        timer = setTimeout(() => open(d), 90);    // short intent delay, so sweeping past doesn't flicker
      });
      d.addEventListener('pointerleave', (e) => {
        if (e.pointerType !== 'mouse') return;
        clearTimeout(timer);
        close(d);
      });
    });
  });
})();
