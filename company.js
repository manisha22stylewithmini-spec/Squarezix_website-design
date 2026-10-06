// Company pages (Culture, Careers, Portfolio, Blogs): small page behaviours.
// Reveals, word light-up, counters and the contact form come from about.js; FAQ from faq.js.
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const mk = (tag, cls, text) => { const el = document.createElement(tag); if (cls) el.className = cls; if (text != null) el.textContent = text; return el; };
  const ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';

  // ---- Careers: open positions. Empty list -> "No current openings" state; roles -> filterable list ----
  // Role shape: { title, team, location, type, href }
  const pos = $('#ca-pos');
  if (pos) {
    let roles = [];
    try { roles = JSON.parse($('#ca-positions').textContent) || []; } catch (_) { roles = []; }
    if (roles.length) {
      const list = $('.ca-pos-list', pos), empty = $('.ca-pos-empty', pos), items = $('.ca-pos-items', pos), filters = $('.ca-pos-filters', pos);
      const sub = $('#ca-pos-sub');
      const mail = (r) => r.href || `mailto:info@squarezix.com?subject=${encodeURIComponent('Application — ' + r.title)}`;
      const teams = ['All', ...new Set(roles.map((r) => r.team).filter(Boolean))];
      const render = (team) => {
        items.replaceChildren(...roles.filter((r) => team === 'All' || r.team === team).map((r) => {
          const li = mk('li', 'ca-pos-item'), left = mk('div'), meta = mk('ul', 'ca-pos-meta');
          left.append(mk('h3', '', r.title));
          [r.team, r.location, r.type].filter(Boolean).forEach((t) => meta.append(mk('li', '', t)));
          left.append(meta);
          const a = mk('a', 'ca-pos-apply'); a.href = mail(r); a.innerHTML = `Apply ${ARROW}`;
          li.append(left, a);
          return li;
        }));
      };
      teams.forEach((t, i) => {
        const b = mk('button', `co-chip${i ? '' : ' is-on'}`, t); b.type = 'button'; b.setAttribute('aria-pressed', i === 0);
        b.addEventListener('click', () => {
          $$('.co-chip', filters).forEach((x) => { x.classList.toggle('is-on', x === b); x.setAttribute('aria-pressed', x === b); });
          render(t);
        });
        filters.append(b);
      });
      if (teams.length < 3) filters.hidden = true;
      filters.classList.add('co-chips');
      render('All');
      list.hidden = false; empty.hidden = true; pos.dataset.state = 'list';
      if (sub) sub.textContent = `${roles.length} role${roles.length > 1 ? 's' : ''} open — apply to the one that fits.`;
    }
  }

  // ---- Portfolio: discipline filter + reels play on hover/focus ----
  const grid = $('#pf-grid');
  if (grid) {
    const tiles = $$('.pf-tile', grid), chips = $$('.pf-filters .co-chip'), empty = $('#pf-empty');
    const apply = (k) => {
      let n = 0;
      tiles.forEach((t) => { const show = k === 'all' || t.dataset.cat === k; t.hidden = !show; if (show) n++; });
      grid.classList.toggle('is-filtered', k !== 'all');
      grid.hidden = n === 0; empty.hidden = n !== 0;
      chips.forEach((c) => { const on = c.dataset.filter === k; c.classList.toggle('is-on', on); c.setAttribute('aria-pressed', on); });
    };
    chips.forEach((c) => c.addEventListener('click', () => apply(c.dataset.filter)));
    $('[data-filter-reset]')?.addEventListener('click', () => apply('all'));
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    $$('.pf-tile--reel', grid).forEach((t) => {
      const v = $('video', t);
      const play = () => { if (reduce) return; v.play().then(() => v.classList.add('is-live')).catch(() => {}); };
      const stop = () => { v.pause(); v.classList.remove('is-live'); v.currentTime = 0; };
      t.addEventListener('pointerenter', play); t.addEventListener('pointerleave', stop);
      t.addEventListener('focus', play); t.addEventListener('blur', stop);
    });
  }

  // ---- Blogs: topic filter + load more, industry tabs, newsletter ----
  const bg = $('#bl-grid');
  if (bg) {
    const cards = $$('.bl-card', bg), more = $('#bl-loadmore'), note = $('#bl-filter-note'), topicBtns = $$('.bl-topic');
    const NAMES = { brand: 'Brand', growth: 'Growth', digital: 'Digital', intelligence: 'Intelligence' };
    const STEP = 9;
    let topic = 'all', limit = STEP;
    const render = () => {
      const list = cards.filter((c) => topic === 'all' || c.dataset.topic === topic);
      cards.forEach((c) => { c.hidden = true; c.classList.remove('is-lead'); });
      list.slice(0, limit).forEach((c, i) => { c.hidden = false; c.classList.toggle('is-lead', i === 0 && !!$('img', c)); });
      more.hidden = limit >= list.length;
      note.textContent = topic === 'all' ? '' : `Showing ${NAMES[topic]} — ${list.length} article${list.length === 1 ? '' : 's'}`;
      topicBtns.forEach((b) => b.setAttribute('aria-pressed', b.dataset.topic === topic));
    };
    topicBtns.forEach((b) => b.addEventListener('click', () => {
      topic = topic === b.dataset.topic ? 'all' : b.dataset.topic; limit = STEP; render();
      $('#latest').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
    }));
    more.addEventListener('click', () => { limit += STEP; render(); });
    render();

    const tabs = $$('.bl-ind-tabs [role="tab"]'), panels = tabs.map((t) => document.getElementById(t.getAttribute('aria-controls')));
    const pick = (i, focus) => {
      tabs.forEach((t, j) => { const on = i === j; t.classList.toggle('is-on', on); t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1; panels[j].hidden = !on; });
      if (focus) tabs[i].focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => pick(i));
      t.addEventListener('keydown', (e) => {
        const k = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
        if (k) { e.preventDefault(); pick((i + k + tabs.length) % tabs.length, true); }
      });
    });
  }
})();
