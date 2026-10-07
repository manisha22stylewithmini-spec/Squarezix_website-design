// Company pages (Culture, Careers, Portfolio, Blogs): small page behaviours.
// Reveals, word light-up, counters and the contact form come from about.js; FAQ from faq.js.
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const mk = (tag, cls, text) => { const el = document.createElement(tag); if (cls) el.className = cls; if (text != null) el.textContent = text; return el; };
  const ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Pill filter bar shared by Portfolio and Blogs: every <select data-key="x"> filters items by their data-x.
  // matches() returns the items passing all selects; sync(n) updates the "Showing" count and reset button.
  const filterBar = (bar, items, onChange) => {
    const sels = $$('select', bar), out = $('.co-fb-out', bar), reset = $('.co-fb-reset', bar);
    const noun = bar.dataset.noun || 'items';
    const matches = () => {
      const f = sels.map((s) => [s.dataset.key, s.value]);
      return items.filter((c) => f.every(([k, v]) => v === 'all' || c.dataset[k] === v));
    };
    const sync = (n) => { out.textContent = `${n} ${n === 1 ? noun.replace(/s$/, '') : noun}`; reset.hidden = sels.every((s) => s.value === 'all'); };
    sels.forEach((s) => s.addEventListener('change', onChange));
    const clear = () => { sels.forEach((s) => { s.value = 'all'; }); onChange(); };
    reset.addEventListener('click', clear);
    return { matches, sync, clear };
  };

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

  // ---- Portfolio: Capability / Industry / Outcome filter over the project cards ----
  const pf = $('#pf-cards');
  if (pf) {
    const cards = $$('.pf-card', pf), bar = $('#pf-bar'), nomatch = $('#pf-nomatch');
    bar.dataset.noun = 'projects';
    const render = () => {
      const list = fb.matches();
      cards.forEach((c) => { c.hidden = !list.includes(c); });
      nomatch.hidden = list.length !== 0;
      fb.sync(list.length);
    };
    const fb = filterBar(bar, cards, render);
    $('[data-filter-reset]', nomatch)?.addEventListener('click', fb.clear);
    // Category pockets: each sets the three filters at once; tapping the active pocket clears them again
    const pockets = $$('.pk-pk[data-set]');
    const sels = $$('select', bar);
    const syncPockets = () => pockets.forEach((p) => {
      const set = JSON.parse(p.dataset.set);
      p.setAttribute('aria-pressed', String(sels.every((s) => s.value === set[s.dataset.key])));
    });
    pockets.forEach((p) => p.addEventListener('click', () => {
      const on = p.getAttribute('aria-pressed') === 'true', set = JSON.parse(p.dataset.set);
      sels.forEach((s) => { s.value = on ? 'all' : set[s.dataset.key]; });
      render();
      if (!on) $('#browse')?.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    }));
    sels.forEach((s) => s.addEventListener('change', syncPockets));
    $('.co-fb-reset', bar)?.addEventListener('click', syncPockets);
    $('[data-filter-reset]', nomatch)?.addEventListener('click', syncPockets);
    pockets.forEach((p) => p.addEventListener('click', syncPockets));
    render();
  }


  // ---- Portfolio: story timeline. The section is tall; its inner pin sticks, the track slides sideways with scroll
  // progress, the line fills, and each milestone (--r 0→1) draws its stem, pops its dot and fades its copy in.
  const tl2 = $('.tl2');
  if (tl2) {
    const pin = $('.tl2-pin', tl2), track = $('.tl2-track', tl2), fill = $('.tl2-fill', tl2), items = $$('.tl2-item', tl2);
    const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
    if (reduce) { tl2.classList.add('is-static'); }
    else {
      let dist = 0, raf = 0;
      const measure = () => {
        dist = Math.max(0, track.scrollWidth - innerWidth);
        tl2.style.height = `${Math.round(innerHeight + dist * 1.1)}px`;
      };
      const frame = () => {
        raf = 0;
        const top = tl2.getBoundingClientRect().top;
        const p = clamp(-top / Math.max(1, tl2.offsetHeight - innerHeight));
        track.style.transform = `translate3d(${-p * dist}px, 0, 0)`;
        const rail = $('.tl2-rail', tl2).getBoundingClientRect();
        fill.style.width = `${Math.max(0, rail.width - 24) * clamp(p * 1.04)}px`;
        items.forEach((it) => {
          const x = it.getBoundingClientRect().left;
          it.style.setProperty('--r', clamp((innerWidth * 0.82 - x) / (innerWidth * 0.16)).toFixed(3));
        });
      };
      const queue = () => { if (!raf) raf = requestAnimationFrame(frame); };
      measure(); frame();
      addEventListener('scroll', queue, { passive: true });
      addEventListener('resize', () => { measure(); queue(); });
      addEventListener('load', () => { measure(); queue(); });
    }
  }

  // ---- Portfolio: folder stack, one folder open at a time ----
  const stack = $('.pf-stack');
  if (stack) {
    const folders = $$('.pf-folder', stack);
    const setOpen = (f, open) => {
      f.classList.toggle('is-open', open);
      $('.pf-folder-tab', f).setAttribute('aria-expanded', open);
      $('.pf-folder-more', f).inert = !open;
    };
    folders.forEach((f) => $('.pf-folder-tab', f).addEventListener('click', () => {
      const wasOpen = f.classList.contains('is-open');
      folders.forEach((x) => setOpen(x, false));
      if (!wasOpen) setOpen(f, true);
    }));
    folders.forEach((f, i) => setOpen(f, i === 0));
  }

  // ---- Blogs: Topic / Industry / Category filter, load more, topic cards, industry tabs ----
  const bg = $('#bl-grid');
  if (bg) {
    const cards = $$('.bl-card', bg), more = $('#bl-loadmore'), topicBtns = $$('.bl-topic'), bar = $('#bl-bar'), nomatch = $('#bl-nomatch');
    const STEP = 8;
    let limit = STEP;
    bar.dataset.noun = 'articles';
    const topicSel = $('select[data-key="topic"]', bar);
    const render = () => {
      const list = fb.matches();
      cards.forEach((c) => { c.hidden = true; });
      list.slice(0, limit).forEach((c) => { c.hidden = false; });
      more.hidden = limit >= list.length;
      nomatch.hidden = list.length !== 0;
      topicBtns.forEach((b) => b.setAttribute('aria-pressed', b.dataset.topic === topicSel.value));
      fb.sync(list.length);
    };
    const fb = filterBar(bar, cards, () => { limit = STEP; render(); });
    $('[data-filter-reset]', nomatch)?.addEventListener('click', fb.clear);
    topicBtns.forEach((b) => b.addEventListener('click', () => {
      topicSel.value = topicSel.value === b.dataset.topic ? 'all' : b.dataset.topic; limit = STEP; render();
      $('#latest').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
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
