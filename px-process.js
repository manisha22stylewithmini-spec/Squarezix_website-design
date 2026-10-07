// Process plates: one step open at a time; plates are tabs (click, arrow keys, Home/End).
(() => {
  document.querySelectorAll('[data-px]').forEach((stage) => {
    const tabs = [...stage.querySelectorAll('.px-plate')];
    const panels = [...stage.querySelectorAll('.px-panel')];
    const n = tabs.length;
    let initial = true;
    const set = (i, focus) => {
      tabs.forEach((t, j) => {
        const on = j === i;
        t.classList.toggle('is-active', on);
        t.classList.toggle('is-done', j < i);
        t.setAttribute('aria-selected', on);
        t.tabIndex = on ? 0 : -1;
        panels[j].hidden = !on;
      });
      stage.style.setProperty('--a', i);
      // Phone layout: the plates are a swipe row, so keep the chosen one centred
      const row = tabs[i].parentElement;
      if (row.scrollWidth > row.clientWidth + 2) {
        row.scrollTo({ left: tabs[i].offsetLeft - (row.clientWidth - tabs[i].offsetWidth) / 2, behavior: initial ? 'auto' : 'smooth' });
      }
      if (focus) tabs[i].focus({ preventScroll: true });
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => set(i));
      t.addEventListener('keydown', (e) => {
        const k = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (k) { e.preventDefault(); set((i + k + n) % n, true); }
        if (e.key === 'Home') { e.preventDefault(); set(0, true); }
        if (e.key === 'End') { e.preventDefault(); set(n - 1, true); }
      });
    });
    set(0);
    initial = false;
  });
})();
