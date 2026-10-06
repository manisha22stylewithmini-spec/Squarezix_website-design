// Case studies page: sticky filter toolbar + searchable/sortable case grid with a
// "load more" pager, whiteboard theme notes that filter the grid, and the three-way
// "Browse the work" list. Same behaviour as the reference build: cards re-mount on
// every filter change so their staggered fade-up replays, and a dot follows the cursor
// inside a hovered card/row.
(() => {
  const PAGE_SIZE = 6;

  // --- Projects ---
  // The first three are the projects on the home page. The rest are SAMPLE entries
  // (sample: true) so the filters have something to work with — swap them for real
  // projects before launch.
  const projects = [
    { client: 'Digital Stream', title: 'A spec-sheet site rebuilt around one clear outcome',
      service: 'Web Design', industry: 'Technology', outcome: 'Conversion',
      excerpt: 'Rewrote the story, redesigned every page to lead to a demo and rebuilt the front end for speed.',
      tags: 'b2b saas speed load demo', date: '2025-06-10', result: '+212% demo requests', img: 'assets/work/project-1.png' },
    { client: 'Hero Gradients', title: 'A headless store with a two-screen checkout',
      service: 'E-commerce', industry: 'Retail', outcome: 'Conversion',
      excerpt: 'Moved the catalogue to a headless stack and cut checkout from five screens to two.',
      tags: 'digital goods checkout headless speed cro analytics', date: '2025-03-18', result: '+38% conversion rate', img: 'assets/work/project-2.png' },
    { client: 'Lissr.ai', title: 'Onboarding that gets to the first result in four minutes',
      service: 'Web Design', industry: 'Technology', outcome: 'Growth',
      excerpt: 'Mapped the first ten minutes of use and redesigned onboarding around a single task.',
      tags: 'ai saas product dashboard onboarding', date: '2024-11-02', result: '3× trial to paid', img: 'assets/work/project-3.png' },
    { sample: true, client: 'Al Noor Properties', title: 'Off-plan listings buyers can actually compare',
      service: 'Web Design', industry: 'Real Estate', outcome: 'Conversion',
      excerpt: 'Project pages, payment-plan calculators and a viewing request that takes one tap.',
      tags: 'property dubai listings proof', date: '2025-08-21', result: '+164% viewing requests', img: 'assets/services/uxui.png' },
    { sample: true, client: 'Saffron & Salt', title: 'Social feeds turned into a reservations engine',
      service: 'Social & Paid', industry: 'Hospitality', outcome: 'Growth',
      excerpt: 'Short-form video, creator collabs and paid social pointed at one booking link.',
      tags: 'restaurant reels instagram content', date: '2025-05-04', result: '+80% social traffic', img: 'assets/reels/reel-3.jpg' },
    { sample: true, client: 'Meridian Clinics', title: 'From page five to the AI answer box',
      service: 'SEO & AI', industry: 'Healthcare', outcome: 'Visibility',
      excerpt: 'Technical SEO, doctor-reviewed content and structured data for AI search.',
      tags: 'ai seo schema llms content proof', date: '2024-09-12', result: '+142% organic bookings', img: 'assets/services/ai.png' },
    { sample: true, client: 'Oud Atelier', title: 'A heritage fragrance house, rebranded for online',
      service: 'Branding', industry: 'Retail', outcome: 'Transformation',
      excerpt: 'Identity, packaging system and product pages built for gifting and repeat purchase.',
      tags: 'luxury identity packaging', date: '2024-12-01', result: '2.1× online revenue', img: 'assets/services/branding.png' },
    { sample: true, client: 'Gulfline Logistics', title: 'A nine-second site brought under two',
      service: 'Web Design', industry: 'Industrial', outcome: 'Transformation',
      excerpt: 'Replatformed to a fast CMS the team can edit, with an RFQ form sales trusts.',
      tags: 'speed load cms migration', date: '2024-07-15', result: '9s → 1.4s load time', img: 'assets/blog/gcc-growth.jpg' },
    { sample: true, client: 'Vantage Capital', title: 'Paid search that stopped buying bad leads',
      service: 'Social & Paid', industry: 'Finance', outcome: 'Growth',
      excerpt: 'Rebuilt campaigns around qualified intent, with offline conversions fed back to Google.',
      tags: 'ppc google ads tracking analytics', date: '2025-02-09', result: '−34% cost per lead', img: 'assets/services/marketing.png' },
    { sample: true, client: 'Desert Bloom Skincare', title: 'Product pages that sell the routine, not the bottle',
      service: 'E-commerce', industry: 'Retail', outcome: 'Growth',
      excerpt: 'Bundles, subscriptions and a PDP template built around before-and-after proof.',
      tags: 'shopify checkout proof reviews', date: '2024-10-20', result: '+89% repeat orders', img: 'assets/reels/reel-5.jpg' },
    { sample: true, client: 'Atlas Academy', title: 'Cited by ChatGPT before the competition noticed',
      service: 'SEO & AI', industry: 'Education', outcome: 'Visibility',
      excerpt: 'Structured answers, llms.txt and citation-ready course pages for AI discovery.',
      tags: 'ai llms schema geo content', date: '2025-07-01', result: '+312% AI referrals', img: 'assets/blog/ai-search.jpg' },
    { sample: true, client: 'Marina Fit', title: 'A gym brand people screenshot and share',
      service: 'Branding', industry: 'Hospitality', outcome: 'Visibility',
      excerpt: 'New identity, class-launch campaigns and a content system the team runs in-house.',
      tags: 'identity social instagram reels', date: '2024-05-27', result: '3.4× Instagram leads', img: 'assets/reels/reel-1.jpg' },
  ];

  const services = ['Web Design', 'E-commerce', 'Branding', 'SEO & AI', 'Social & Paid'];
  const filters = ['All', ...services];
  const filterHints = {
    All: 'Browse everything',
    'Web Design': 'Sites and web apps',
    'E-commerce': 'Stores and checkouts',
    Branding: 'Identity and rebrands',
    'SEO & AI': 'Search and AI visibility',
    'Social & Paid': 'Social, ads and campaigns',
  };

  // Whiteboard notes, laid out like a real board: four up top, three below, each with a
  // handwritten annotation on one side (tl/tr/l/r/b) and an arrow pointing at the note.
  // Tapping a note searches the grid for its keyword; notes can also be dragged around.
  const notes = [
    { title: 'Speed is\na feature', note: 'Slow sites leak buyers before the first scroll. Under 2s or it doesn’t ship.', keyword: 'speed', side: 'tl', rot: -2.5, row: 1, paper: 'lilac', tag: 'UX' },
    { title: 'Checkout, minus\nthe friction', note: 'Every extra screen at checkout costs sales — so we count them.', keyword: 'checkout', side: 'tr', rot: 1.8, row: 1, paper: 'mist', tag: 'CRO' },
    { title: 'AI &\ndiscovery', note: 'Structured answers + schema, so ChatGPT & Gemini recommend you.', keyword: 'schema', side: 'tr', rot: -1.2, row: 1, paper: 'violet', tag: 'SEO', curl: true },
    { title: 'Proof before\npromise', note: 'Reviews & results placed exactly where decisions happen.', keyword: 'proof', side: 'b', rot: 1.4, row: 1, paper: 'orchid', tag: 'UX' },
    { title: 'Words before\npixels', note: 'Design gets easier once the words exist. When does copy lead?', keyword: 'content', side: 'tl', rot: 2.2, row: 2, paper: 'mist', tag: 'COPY' },
    { title: 'Identity that\ntravels', note: 'Billboard, reel and a 32px favicon — one brand has to work on all three.', keyword: 'identity', side: 'b', rot: -1.6, row: 2, paper: 'lavender', tag: 'BRAND', curl: true },
    { title: 'Measure\nthe gaps', note: 'Blind spots, vanity metrics — the gaps in tracking & reporting.', keyword: 'analytics', side: 'tr', rot: 0.8, row: 2, paper: 'lilac', tag: 'DATA' },
  ];

  // The rough method pinned under the notes: how a case study gets made
  const method = ['Brief & goals', 'Dig into the data', 'Form a hypothesis', 'Design · build · test', 'Measure, then write it up'];

  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const haystack = (p) => `${p.client} ${p.title} ${p.excerpt} ${p.service} ${p.industry} ${p.tags}`.toLowerCase();
  const year = (p) => p.date.slice(0, 4);
  const ARROW = '<svg viewBox="0 0 64 64"><path d="M5 32h49M36 13l19 19-19 19"/></svg>';

  // Shared: a dot that follows the cursor inside cards and rows
  const trackCursor = (el) => el.addEventListener('mousemove', (e) => {
    const r = el.getBoundingClientRect();
    el.style.setProperty('--cursor-x', `${e.clientX - r.left}px`);
    el.style.setProperty('--cursor-y', `${e.clientY - r.top}px`);
  });

  // ================= Listing =================
  // The listing section is hidden on the page for now; everything here only runs when
  // its markup is present. The whiteboard notes then filter "Browse the work" instead.
  let showInListing = null;
  if ($('cx-grid')) {
  const state = { filter: 'All', query: '', sort: 'newest', count: PAGE_SIZE };
  const el = {
    toolbar: $('cx-toolbar'), sentinel: $('cx-sentinel'), filters: $('cx-filters'),
    count: $('cx-count'), q: $('cx-q'), qClear: $('cx-q-clear'), qKbd: $('cx-q-kbd'),
    sort: $('cx-sort'), active: $('cx-active'), grid: $('cx-grid'), pager: $('cx-pager'),
    content: $('cx-list-content'),
  };

  // Toolbar compacts once it sticks under the header
  // (the site header is fixed, so "the top" is the header's bottom edge)
  const headerH = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header-h'), 10) || 80;
  new IntersectionObserver(([entry]) => {
    el.toolbar.classList.toggle('is-stuck', !entry.isIntersecting && entry.boundingClientRect.top < headerH);
  }, { threshold: 0, rootMargin: `-${headerH}px 0px 0px 0px` }).observe(el.sentinel);

  const counts = Object.fromEntries(filters.map((f) => [f, f === 'All' ? projects.length : projects.filter((p) => p.service === f).length]));

  el.filters.innerHTML = filters.map((f, i) => `
    <button type="button" role="tab" id="cx-tab-${i}" aria-controls="cx-grid" title="${esc(filterHints[f])}" data-filter="${esc(f)}">
      <span class="cx-filter-label">${esc(f)}</span>
      <span class="cx-filter-count" aria-label="${counts[f]} projects">${counts[f]}</span>
    </button>`).join('');
  const tabs = [...el.filters.querySelectorAll('button')];
  tabs.forEach((btn, i) => {
    btn.addEventListener('click', () => set({ filter: filters[i] }));
    btn.addEventListener('keydown', (e) => {
      let next = null;
      if (e.key === 'ArrowRight') next = (i + 1) % filters.length;
      if (e.key === 'ArrowLeft') next = (i - 1 + filters.length) % filters.length;
      if (e.key === 'Home') next = 0;
      if (e.key === 'End') next = filters.length - 1;
      if (next === null) return;
      e.preventDefault();
      set({ filter: filters[next] });
      tabs[next].focus();
    });
  });

  el.q.addEventListener('input', () => set({ query: el.q.value }));
  el.qClear.addEventListener('click', () => { set({ query: '' }); el.q.focus(); });
  el.sort.addEventListener('change', () => set({ sort: el.sort.value }));
  // "/" jumps to search (unless the visitor is already typing somewhere)
  window.addEventListener('keydown', (e) => {
    if (e.key !== '/' || e.metaKey || e.ctrlKey || e.altKey) return;
    const a = document.activeElement;
    if (a && (a.tagName === 'INPUT' || a.tagName === 'TEXTAREA' || a.tagName === 'SELECT' || a.isContentEditable)) return;
    e.preventDefault();
    el.q.focus();
  });

  function set(patch) {
    const resetsPage = 'filter' in patch || 'query' in patch || 'sort' in patch;
    Object.assign(state, patch, resetsPage ? { count: PAGE_SIZE } : {});
    renderList();
  }

  function visible() {
    const q = state.query.trim().toLowerCase();
    let list = state.filter === 'All' ? [...projects] : projects.filter((p) => p.service === state.filter);
    if (q) list = list.filter((p) => haystack(p).includes(q));
    list.sort((a, b) => {
      if (state.sort === 'az') return a.client.localeCompare(b.client);
      const d = Date.parse(b.date) - Date.parse(a.date);
      return state.sort === 'newest' ? d : -d;
    });
    return list;
  }

  function renderList() {
    const list = visible();
    const paged = list.slice(0, state.count);
    const q = state.query.trim();

    tabs.forEach((btn, i) => {
      const on = filters[i] === state.filter;
      btn.classList.toggle('active', on);
      btn.setAttribute('aria-selected', on);
      btn.tabIndex = on ? 0 : -1;
    });
    if (el.q.value !== state.query) el.q.value = state.query;
    el.sort.value = state.sort;
    el.qClear.hidden = !state.query;
    el.qKbd.hidden = !!state.query;
    el.grid.setAttribute('aria-labelledby', `cx-tab-${filters.indexOf(state.filter)}`);
    el.count.innerHTML = `Showing <strong>${paged.length}</strong> of ${list.length} ${list.length === 1 ? 'project' : 'projects'}`;

    // Active filters
    const filtered = state.filter !== 'All' || q !== '';
    el.active.hidden = !filtered;
    if (filtered) {
      el.active.innerHTML = `
        <div class="cx-active-pills">
          <span class="cx-active-title">Active:</span>
          ${state.filter !== 'All' ? `<button type="button" class="cx-active-pill" data-clear="filter">${esc(state.filter)} <span aria-hidden="true">×</span></button>` : ''}
          ${q ? `<button type="button" class="cx-active-pill" data-clear="query">“${esc(q)}” <span aria-hidden="true">×</span></button>` : ''}
        </div>
        <button type="button" class="cx-reset" data-clear="all">Reset all</button>`;
    }

    // Grid (re-built each time, so the staggered fade-up replays)
    if (!list.length) {
      el.grid.innerHTML = `
        <div class="cx-empty" role="status">
          <div class="cx-empty-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M11 4a7 7 0 1 0 4.9 12L20 20l1.4-1.4-4.1-4.1A7 7 0 0 0 11 4Zm0 2a5 5 0 1 1 0 10 5 5 0 0 1 0-10Z" fill="currentColor"/></svg></div>
          <h3>No projects found</h3>
          <p>Nothing matches ${state.filter !== 'All' ? `“${esc(state.filter)}”` : 'your filters'}${q ? ` and “${esc(q)}”` : ''}. Try a different keyword or service.</p>
          <button type="button" data-clear="all">Clear filters</button>
        </div>`;
    } else {
      el.grid.innerHTML = paged.map((p, i) => `
        <article class="cx-card" style="animation-delay:${Math.min(i, 8) * 35}ms">
          <p class="cx-card-cat">${esc(p.service)}</p>
          <h2><a href="#ab-contact" title="Start a project like ${esc(p.client)}">${esc(p.title)}</a></h2>
          <p class="cx-card-excerpt">${esc(p.excerpt)}</p>
          <p class="cx-card-result">${esc(p.result)}</p>
          <p class="cx-card-meta">${esc(p.client)} · ${esc(p.industry)} · ${year(p)}</p>
          <span class="cx-card-arrow" aria-hidden="true">${ARROW}</span>
          <span class="cx-cursor" aria-hidden="true"></span>
        </article>`).join('');
      el.grid.querySelectorAll('.cx-card').forEach(trackCursor);
    }

    // Pager
    const showPager = list.length > PAGE_SIZE || state.count > PAGE_SIZE;
    el.pager.hidden = !showPager;
    if (showPager) {
      const pct = Math.round((paged.length / list.length) * 100);
      el.pager.innerHTML = `
        <div class="cx-pager-track" aria-hidden="true"><span class="cx-pager-fill" style="width:${pct}%"></span></div>
        ${state.count < list.length
          ? `<button type="button" class="cx-pager-btn" data-more>Load more projects <span class="cx-pager-left">${list.length - state.count} left</span><span aria-hidden="true">↓</span></button>`
          : (state.count > PAGE_SIZE ? '<button type="button" class="cx-reset cx-pager-less" data-less>Show less</button>' : '')}`;
    }
  }

  // Delegated clicks for the bits that get re-rendered
  document.querySelector('.cx-list').addEventListener('click', (e) => {
    const t = e.target.closest('[data-clear],[data-more],[data-less]');
    if (!t) return;
    if (t.dataset.clear === 'filter') set({ filter: 'All' });
    else if (t.dataset.clear === 'query') set({ query: '' });
    else if (t.dataset.clear === 'all') set({ filter: 'All', query: '', sort: 'newest' });
    else if ('more' in t.dataset) { state.count += PAGE_SIZE; renderList(); }
    else if ('less' in t.dataset) {
      state.count = PAGE_SIZE; renderList();
      el.content.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });

  renderList();
  showInListing = (keyword) => {
    set({ filter: 'All', query: keyword, sort: 'newest' });
    $('cases').scrollIntoView({ behavior: 'smooth', block: 'start' });
  };
  }

  // ================= Whiteboard =================
  const board = $('cx-wall');
  const noteHTML = (n, i) => {
    const matches = projects.filter((p) => haystack(p).includes(n.keyword)).length;
    const count = `${matches} ${matches === 1 ? 'project' : 'projects'}`;
    return `
      <figure class="cx-note cx-note--${n.side} cx-paper--${n.paper}${n.curl ? ' is-curl' : ''}" style="--rot:${n.rot}deg">
        <button type="button" class="cx-postit" data-keyword="${esc(n.keyword)}" aria-label="${esc(n.title.replace('\n', ' '))}: show ${count}">
          <span class="cx-paper-head" aria-hidden="true"><span>R&amp;D log</span><span>No. ${String(i + 1).padStart(2, '0')} · ${esc(n.tag)}</span></span>
          <span class="cx-paper-label" aria-hidden="true">Problem:</span>
          <span class="cx-postit-title">${esc(n.title)}</span>
          <span class="cx-postit-foot">${count} <span aria-hidden="true">→</span></span>
        </button>
        <figcaption class="cx-annot">${esc(n.note)}</figcaption>
        <svg class="cx-curb" viewBox="0 0 130 80" fill="none" aria-hidden="true">
          <defs><marker id="cx-curb-${i}" markerWidth="9" markerHeight="9" refX="6.5" refY="4.5" orient="auto"><path d="M0 .9 8.4 4.5 0 8.1" stroke="currentColor" stroke-width="1.7"/></marker></defs>
          <path d="M8 8 C 58 12, 96 34, 102 69" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" marker-end="url(#cx-curb-${i})"/>
        </svg>
      </figure>`;
  };
  board.innerHTML = [1, 2].map((row) => `
    <div class="cx-notes-row cx-notes-row--${row}">
      ${notes.map((n, i) => (n.row === row ? noteHTML(n, i) : '')).join('')}
    </div>`).join('') + `
    <div class="cx-method">
      <p class="cx-method-title">How every case study gets made <span aria-hidden="true">↴</span></p>
      <ol>${method.map((m, i) => `<li><b>${i + 1}</b>${esc(m)}</li>`).join('')}</ol>
    </div>`;

  // Drag a note around the board (mouse / pen only — touch keeps normal scrolling).
  // A press that doesn't move is a tap, and a tap shows that theme's projects.
  let top = 10;
  board.querySelectorAll('.cx-note').forEach((note) => {
    const btn = note.querySelector('.cx-postit');
    let start = null, moved = false, dx = 0, dy = 0;
    btn.addEventListener('pointerdown', (e) => {
      if (e.pointerType === 'touch' || e.button !== 0 || matchMedia('(max-width: 800px)').matches) return;
      start = { x: e.clientX - dx, y: e.clientY - dy, px: e.clientX, py: e.clientY };
      moved = false;
      btn.setPointerCapture(e.pointerId);
    });
    btn.addEventListener('pointermove', (e) => {
      if (!start) return;
      if (!moved && Math.hypot(e.clientX - start.px, e.clientY - start.py) < 5) return;
      if (!moved) { moved = true; note.classList.add('is-dragging'); note.style.zIndex = ++top; }
      dx = e.clientX - start.x; dy = e.clientY - start.y;
      note.style.setProperty('--dx', `${dx}px`);
      note.style.setProperty('--dy', `${dy}px`);
    });
    const end = () => { start = null; note.classList.remove('is-dragging'); };
    btn.addEventListener('pointerup', end);
    btn.addEventListener('pointercancel', end);
    btn.addEventListener('click', (e) => {
      if (moved) { e.preventDefault(); moved = false; return; }   // that was a drag, not a tap
      if (showInListing) showInListing(btn.dataset.keyword);
      else showTheme(btn.dataset.keyword, btn.querySelector('.cx-postit-title').textContent.replace(/\s+/g, ' '));
    });
  });

  // ================= Browse the work =================
  const opts = {
    cap: ['All Capabilities', ...services],
    ind: ['All Industries', ...[...new Set(projects.map((p) => p.industry))].sort()],
    out: ['All Outcomes', 'Growth', 'Conversion', 'Visibility', 'Transformation'],
  };
  const sel = { cap: $('cx-w-cap'), ind: $('cx-w-ind'), out: $('cx-w-out') };
  Object.entries(sel).forEach(([k, s]) => {
    s.innerHTML = opts[k].map((o) => `<option>${esc(o)}</option>`).join('');
    s.addEventListener('change', () => { shown = workPage(); renderWork(); });
  });
  const workList = $('cx-work-list');
  const wReset = $('cx-w-reset');
  const wPager = $('cx-w-pager');
  // Page size comes from the "Showing" select (6 by default, 4 on phones until the visitor
  // picks one). "Load more" adds another page of that size; "Show less" folds back to one.
  const phone = matchMedia('(max-width: 800px)');
  const perSel = $('cx-w-per');
  const PER = [4, 6, 8, 0];   // 0 = all
  perSel.innerHTML = PER.map((n) => `<option value="${n}">${n ? `${n} projects` : 'All projects'}</option>`).join('');
  let perChosen = false;
  const syncPer = () => { if (!perChosen) perSel.value = phone.matches ? '4' : '6'; };
  syncPer();
  const workPage = () => +perSel.value || projects.length;
  let shown = workPage();
  perSel.addEventListener('change', () => { perChosen = true; shown = workPage(); renderWork(); });
  phone.addEventListener('change', () => { syncPer(); shown = workPage(); renderWork(); });
  // A theme picked on the whiteboard narrows the list too, until it's cleared
  let theme = null;
  const resetWork = () => { Object.values(sel).forEach((s) => { s.selectedIndex = 0; }); theme = null; perChosen = false; syncPer(); shown = workPage(); renderWork(); };
  function showTheme(keyword, label) {
    Object.values(sel).forEach((s) => { s.selectedIndex = 0; });
    theme = { keyword, label };
    shown = workPage();
    renderWork();
    $('work').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  wReset.addEventListener('click', resetWork);
  wPager.addEventListener('click', (e) => {
    if (e.target.closest('[data-wmore]')) { shown += workPage(); renderWork(); }
    else if (e.target.closest('[data-wless]')) {
      shown = workPage(); renderWork();
      $('work').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });

  function renderWork() {
    const [cap, ind, out] = [sel.cap.value, sel.ind.value, sel.out.value];
    const list = projects.filter((p) =>
      (cap === opts.cap[0] || p.service === cap) &&
      (ind === opts.ind[0] || p.industry === ind) &&
      (out === opts.out[0] || p.outcome === out) &&
      (!theme || haystack(p).includes(theme.keyword)));
    const paged = list.slice(0, shown);
    $('cx-w-count').innerHTML = (theme ? `<button type="button" class="cx-active-pill cx-theme-pill" data-clear-theme>${esc(theme.label)} <span aria-hidden="true">×</span></button>` : '');
    $('cx-w-count').hidden = !theme;
    $('cx-w-count').querySelector('[data-clear-theme]')?.addEventListener('click', () => { theme = null; shown = workPage(); renderWork(); });
    wReset.hidden = cap === opts.cap[0] && ind === opts.ind[0] && out === opts.out[0] && !theme;

    if (!list.length) {
      workList.innerHTML = `
        <div class="cx-empty" role="status">
          <h3>No projects match that combination</h3>
          <p>Try loosening one filter — most projects span more than one outcome.</p>
          <button type="button" data-wreset>Reset filters</button>
        </div>`;
      workList.querySelector('[data-wreset]').addEventListener('click', resetWork);
      wPager.hidden = true;
      return;
    }
    workList.innerHTML = paged.map((p, i) => `
      <a class="cx-row" href="#ab-contact" data-p="${projects.indexOf(p)}" style="animation-delay:${Math.min(i, 7) * 45}ms" aria-label="${esc(p.client)} — ${esc(p.result)}">
        <span class="cx-row-index">${String(i + 1).padStart(2, '0')}</span>
        <span class="cx-row-name">
          <span class="cx-row-client">${esc(p.client)}</span>
          <span class="cx-row-tags">${esc(p.service)} <b>·</b> ${esc(p.industry)} <b>·</b> ${esc(p.outcome)}</span>
        </span>
        <span class="cx-row-result"><strong>${esc(p.result)}</strong><span>Outcome</span></span>
        <span class="cx-row-arrow" aria-hidden="true">${ARROW}</span>
        <span class="cx-cursor" aria-hidden="true"></span>
      </a>`).join('');
    workList.querySelectorAll('.cx-row').forEach(trackCursor);

    // Pager: progress bar + "Load more" while there's more; "Show less" once expanded
    const page = workPage();
    wPager.hidden = list.length <= page;
    if (wPager.hidden) return;
    const left = list.length - paged.length;
    wPager.innerHTML = `
      <div class="cx-pager-track" aria-hidden="true"><span class="cx-pager-fill" style="width:${Math.round((paged.length / list.length) * 100)}%"></span></div>
      ${left > 0
        ? `<button type="button" class="cx-pager-btn" data-wmore>Load ${Math.min(page, left)} more ${Math.min(page, left) === 1 ? 'project' : 'projects'} <span class="cx-pager-left">${left} left</span><span aria-hidden="true">↓</span></button>`
        : '<p class="cx-pager-note">You’re all caught up — every project is showing.</p>'}
      ${shown > page ? '<button type="button" class="cx-reset cx-pager-less" data-wless>Show less ↑</button>' : ''}`;
  }
  renderWork();

  // ================= Hover preview =================
  // A device-frame preview (screenshot + client logo) that trails the cursor while it is
  // over a project row, and swaps to that row's project as the cursor moves between rows.
  // Desktop pointers only; the cursor dot is drawn above the card.
  const wrap = $('cx-work-wrap');
  const peek = $('cx-peek');
  const peekImg = $('cx-peek-img');
  const peekLogo = $('cx-peek-logo');
  const peekDot = $('cx-peek-dot');
  const fine = matchMedia('(hover: hover) and (pointer: fine) and (min-width: 801px)');
  const initials = (name) => name.replace(/[^A-Za-z0-9 ]/g, '').split(' ').filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toUpperCase();
  projects.forEach((p) => { const im = new Image(); im.src = p.img; });   // warm the cache so swaps are instant

  let active = -1, raf = 0, on = false;
  const target = { x: 0, y: 0 }, pos = { x: 0, y: 0 };
  let rot = 0;

  function fill(p) {
    peekImg.src = p.img;
    peekLogo.innerHTML = p.logo
      ? `<img src="${esc(p.logo)}" alt="" />`
      : `<span class="cx-peek-mark">${esc(initials(p.client))}</span><span class="cx-peek-name">${esc(p.client)}</span>`;
    peek.classList.remove('is-swap'); void peek.offsetWidth; peek.classList.add('is-swap');
  }
  function frame() {
    // ease toward the cursor; tilt a little in the direction of travel
    const dx = target.x - pos.x;
    pos.x += dx * 0.18; pos.y += (target.y - pos.y) * 0.18;
    rot += (Math.max(-8, Math.min(8, dx * 0.12)) - rot) * 0.15;
    peek.style.transform = `translate3d(${pos.x}px, ${pos.y}px, 0) translate(-50%, -50%) rotate(${rot}deg)`;
    raf = on || Math.abs(dx) > 0.5 ? requestAnimationFrame(frame) : 0;
  }
  function hide() {
    on = false; active = -1;
    wrap.classList.remove('is-peeking');
  }
  wrap.addEventListener('pointermove', (e) => {
    if (!fine.matches) return;
    const row = e.target.closest('.cx-row');
    if (!row) { hide(); return; }
    const r = wrap.getBoundingClientRect();
    target.x = e.clientX - r.left; target.y = e.clientY - r.top;
    peekDot.style.transform = `translate3d(${target.x}px, ${target.y}px, 0) translate(-50%, -50%)`;
    if (!on) { pos.x = target.x; pos.y = target.y; on = true; wrap.classList.add('is-peeking'); }
    const idx = +row.dataset.p;
    if (idx !== active) { active = idx; fill(projects[idx]); }
    if (!raf) raf = requestAnimationFrame(frame);
  });
  wrap.addEventListener('pointerleave', hide);
})();
