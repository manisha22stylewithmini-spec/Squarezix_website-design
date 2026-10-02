// Header mega-menus.
// UX follows the wireframes: each menu = segmented tabs → grid of services → full-width banner.
// "Insights" uses the split layout: description + banner on the left, image on the right.
// Edit the MENUS data below to change any label, link or copy.
(() => {
  // Content follows the header design (04–06 · Header — Desktop / Tablet / Mobile).
  // `h` = link: items that exist on squarezix.com link there; the rest go to contact.
  const LIVE = 'https://squarezix.com';
  const CONTACT = `${LIVE}/contact-us/`;
  const MENUS = {
    web: {
      page: { href: 'web-and-brand.html', label: 'Explore Web & Brand' },
      tabs: [
        { label: 'Branding', page: 'branding.html', items: [
          { t: 'Brand Strategy & Positioning', d: 'Find the space only you can own', h: CONTACT },
          { t: 'Visual Identity Design', d: 'Logos, type and colour systems', h: CONTACT },
          { t: 'Brand Audit & Rebranding', d: 'Refresh without losing equity', h: CONTACT },
          { t: 'Brand Experience & Touchpoints', d: 'One feel across every channel', h: CONTACT },
          { t: 'Brand Collateral & Print Design', d: 'Stationery, packaging, signage', h: CONTACT },
          { t: 'Content Creation Services', d: 'Photo, video and brand copy', h: CONTACT },
        ] },
        { label: 'Designing', page: 'designing.html', items: [
          { t: 'Website Design', d: 'Conversion-first, pixel-perfect', h: `${LIVE}/website-design-company-dubai/` },
          { t: 'E-commerce Website Design', d: 'Storefronts that sell', h: CONTACT },
          { t: 'Email Marketing Testing & Design', d: 'Templates tested across clients', h: CONTACT },
          { t: 'Mobile App Design', d: 'iOS & Android UX/UI', h: CONTACT },
          { t: 'Rapid Web Design', d: 'Launch-ready in two weeks', h: CONTACT },
          { t: 'Social Media Design', d: 'Posts, reels and ad creative', h: CONTACT },
        ] },
        { label: 'Development', page: 'development.html', items: [
          { t: 'Website Management', d: 'Updates, hosting and care plans', h: `${LIVE}/website-management-services/` },
          { t: 'Website Development', d: 'Fast, accessible, SEO-ready', h: `${LIVE}/website-development-company-in-dubai/` },
          { t: 'Headless CMS Development', d: 'Sanity, Strapi, Contentful', h: `${LIVE}/headless-cms-development/` },
          { t: 'E-commerce Website Development', d: 'Shopify, WooCommerce, custom', h: `${LIVE}/ecommerce-website-development/` },
          { t: 'Headless E-commerce Development', d: 'Shopify Hydrogen & Next.js', h: `${LIVE}/headless-ecommerce-development/` },
          { t: 'Website Migration Services', d: 'Move platforms, keep rankings', h: `${LIVE}/website-migration-services/` },
        ] },
      ],
      banner: { kicker: 'Free audit', title: 'Is your website holding you back?', cta: 'Get a free site & brand audit', href: CONTACT },
    },
    growth: {
      page: { href: 'growth-marketing.html', label: 'Explore Growth Marketing' },
      tabs: [
        { label: 'Social Media Marketing', page: 'social-media-marketing.html', items: [
          { t: 'Community Management', d: 'Replies, DMs and daily presence', h: CONTACT },
          { t: 'Content Creation Services', d: 'Reels, carousels and stories', h: CONTACT },
          { t: 'Advertising & Media Services', d: 'Paid social that pays back', h: CONTACT },
          { t: 'Social Media Event Management', d: 'Launches, live and activations', h: CONTACT },
        ] },
        { label: 'Content Marketing', page: 'content-marketing.html', items: [
          { t: 'Website Copywriting', d: 'Words that convert and rank', h: CONTACT },
          { t: 'Digital PR', d: 'Coverage and authority links', h: CONTACT },
          { t: 'Multimedia Content Assets', d: 'Video, graphics and guides built to be shared', h: CONTACT, wide: true },
        ] },
      ],
      banner: { kicker: 'Playbook', title: 'The GCC social growth playbook', cta: 'Get the free playbook', href: CONTACT },
    },
    ai: {
      page: { href: 'ai-and-intelligence.html', label: 'Explore AI & Intelligence' },
      tabs: [
        { label: 'Core SEO', page: 'core-seo.html', items: [
          { t: 'Enterprise SEO', d: 'Scale across thousands of pages', h: CONTACT },
          { t: 'E-commerce SEO', d: 'Rank products and categories', h: `${LIVE}/ecommerce-seo-services/` },
          { t: 'Local SEO', d: 'Own the map pack in your city', h: `${LIVE}/local-seo-services/` },
          { t: 'AI & LLM SEO', d: 'Get cited by ChatGPT & Gemini', h: `${LIVE}/ai-seo-services/` },
          { t: 'Search Engine Optimization', d: 'Technical, on-page and off-page — the full foundation', h: `${LIVE}/seo-agency-dubai/`, wide: true },
        ] },
        { label: 'Generative Search', page: 'generative-search.html', items: [
          { t: 'Generative AI Research and Analysis', d: 'How AI answers talk about you', h: CONTACT },
          { t: 'Semantic Keywords Research', d: 'Topics, entities and intent', h: CONTACT },
          { t: 'AI-Optimised Content', d: 'Written to be quoted by AI', h: CONTACT },
          { t: 'Community Engagement Optimization', d: 'Reddit, Quora and forums', h: CONTACT },
          { t: 'Brand Visibility and Authority', d: 'Mentions that models trust', h: CONTACT },
          { t: 'AI-Friendly Structured Data', d: 'Schema that machines read', h: CONTACT },
        ] },
      ],
      banner: { kicker: 'AI visibility check', title: 'Does ChatGPT recommend your brand?', cta: 'Run a free AI visibility check', href: CONTACT },
    },
    insights: {
      layout: 'split',
      tabs: [
        { label: 'Blogs', title: 'Blogs', img: 'assets/work/project-3.png',
          d: 'Field notes on design, SEO and AI search from the team shipping it every week — practical, no fluff.',
          banner: { title: 'Read the latest articles', cta: 'Visit the blog', href: `${LIVE}/blogs/` } },
        { label: 'Our Culture', title: 'Our Culture', img: 'assets/footer/sz-stage.jpg',
          d: 'Our story, mission, vision and awards — how a Dubai studio grew into a partner for brands across the GCC and Asia.',
          banner: { title: 'Life at Squarezix', cta: 'Meet the team', href: 'about-us.html' } },
        { label: 'Career', title: 'Career', img: 'assets/work/project-1.png',
          d: 'Designers, developers and strategists who like hard problems. Hybrid in Dubai, remote-friendly across the region.',
          banner: { title: "We're hiring", cta: 'See open roles', href: CONTACT } },
      ],
    },
  };

  const ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>';
  const CHEVRON = '<svg class="nav-chev" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>';
  const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

  const banner = (b) => `
    <a class="mm-banner" href="${b.href}">
      <span class="mm-banner-copy">
        ${b.kicker ? `<span class="mm-banner-kicker">${esc(b.kicker)}</span>` : ''}
        <span class="mm-banner-title">${esc(b.title)}</span>
      </span>
      <span class="mm-banner-cta">${esc(b.cta)} ${ARROW}</span>
    </a>`;

  const gridPane = (tab) => `
    ${tab.page ? `<a class="mm-tab-page" href="${tab.page}">${esc(tab.label)} overview ${ARROW}</a>` : ''}
    <ul class="mm-grid">
      ${tab.items.map((it) => `
        <li${it.wide ? ' class="is-wide"' : ''}><a class="mm-card" href="${it.h || '#'}">
          <span class="mm-card-title">${esc(it.t)}</span>
          <span class="mm-card-desc">${esc(it.d)}</span>
          <span class="mm-card-arrow">${ARROW}</span>
        </a></li>`).join('')}
    </ul>`;

  const splitPane = (tab) => `
    <div class="mm-split">
      <div class="mm-split-copy">
        <h3>${esc(tab.title)}</h3>
        <p>${esc(tab.d)}</p>
        ${banner(tab.banner)}
      </div>
      <div class="mm-split-media"><img src="${tab.img}" alt="" loading="lazy" /></div>
    </div>`;

  const ARROW_R = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  const desktop = matchMedia('(min-width: 1081px)');
  // --- Build a panel for every [data-menu] trigger ---
  const header = document.querySelector('.site-header');
  const items = [...document.querySelectorAll('.nav-item[data-menu]')];
  items.forEach((item) => {
    const key = item.dataset.menu;
    const data = MENUS[key];
    const trigger = item.querySelector('.nav-trigger');
    const panelId = `mm-${key}`;
    trigger.insertAdjacentHTML('beforeend', CHEVRON);
    trigger.setAttribute('aria-expanded', 'false');
    trigger.setAttribute('aria-controls', panelId);

    const panel = document.createElement('div');
    panel.className = `mm-panel${data.layout === 'split' ? ' mm-panel--split' : ''}`;
    panel.id = panelId;
    panel.innerHTML = `
      ${data.page ? `<a class="mm-overview" href="${data.page.href}"><span>${esc(data.page.label)}</span><i>Overview page ${ARROW_R}</i></a>` : ''}
      <div class="mm-tabs" role="tablist" aria-label="${esc(trigger.textContent.trim())}" style="--n:${data.tabs.length}">
        <span class="mm-tab-thumb" aria-hidden="true"></span>
        ${data.tabs.map((t, i) => `<button class="mm-tab" type="button" role="tab" id="${panelId}-t${i}"
            aria-controls="${panelId}-p${i}" aria-selected="${i === 0}" tabindex="${i === 0 ? 0 : -1}">${esc(t.label)}</button>`).join('')}
      </div>
      ${data.tabs.map((t, i) => `<div class="mm-pane" role="tabpanel" id="${panelId}-p${i}" aria-labelledby="${panelId}-t${i}"${i === 0 ? '' : ' hidden'}>
          ${data.layout === 'split' ? splitPane(t) : gridPane(t)}
        </div>`).join('')}
      ${data.banner ? banner(data.banner) : ''}`;
    item.appendChild(panel);

    // --- Tabs: click, hover (short intent delay) and arrow keys ---
    const tabs = [...panel.querySelectorAll('.mm-tab')];
    const panes = [...panel.querySelectorAll('.mm-pane')];
    const tablist = panel.querySelector('.mm-tabs');
    const select = (i, focus) => {
      tabs.forEach((t, j) => {
        t.setAttribute('aria-selected', j === i);
        t.tabIndex = j === i ? 0 : -1;
        panes[j].hidden = j !== i;
      });
      tablist.style.setProperty('--i', i);
      if (focus) tabs[i].focus();
    };
    let hoverTimer;
    tabs.forEach((t, i) => {
      t.addEventListener('click', (e) => {
        // Mouse (any width): hover already shows the tab's services, so a click opens its page.
        // Touch and keyboard: the first press selects the tab, a press on the selected tab opens it.
        const page = data.tabs[i].page;
        const selected = t.getAttribute('aria-selected') === 'true';
        if (page && (selected || e.pointerType === 'mouse')) { location.href = page; return; }
        select(i);
      });
      t.addEventListener('pointerenter', (e) => {
        if (e.pointerType !== 'mouse') return;
        clearTimeout(hoverTimer);
        hoverTimer = setTimeout(() => select(i), 120);
      });
      t.addEventListener('pointerleave', () => clearTimeout(hoverTimer));
      t.addEventListener('keydown', (e) => {
        const n = tabs.length;
        if (e.key === 'ArrowRight') { e.preventDefault(); select((i + 1) % n, true); }
        if (e.key === 'ArrowLeft') { e.preventDefault(); select((i - 1 + n) % n, true); }
      });
    });
  });

  // --- Open / close ---
  let openItem = null;
  let closeTimer;

  const open = (item) => {
    clearTimeout(closeTimer);
    if (openItem === item) return;
    if (openItem) close(openItem, false);
    openItem = item;
    item.classList.add('is-open');
    item.querySelector('.nav-trigger').setAttribute('aria-expanded', 'true');
    header.classList.add('mm-active');
  };
  function close(item, clearHeader = true) {
    if (!item) return;
    item.classList.remove('is-open');
    item.querySelector('.nav-trigger').setAttribute('aria-expanded', 'false');
    if (openItem === item) openItem = null;
    if (clearHeader && !openItem) header.classList.remove('mm-active');
  }

  items.forEach((item) => {
    const trigger = item.querySelector('.nav-trigger');
    const page = MENUS[item.dataset.menu].page;
    trigger.addEventListener('click', (e) => {
      // Desktop mouse: hover already shows the dropdown, so a click on the label opens its hub page.
      // Touch and keyboard still toggle the menu (the hub link is the first row inside it).
      if (page && desktop.matches && e.pointerType === 'mouse') { location.href = page.href; return; }
      item.classList.contains('is-open') ? close(item) : open(item);
    });
    // Desktop hover with a grace period so moving diagonally into the panel doesn't close it
    item.addEventListener('pointerenter', (e) => { if (desktop.matches && e.pointerType === 'mouse') open(item); });
    item.addEventListener('pointerleave', (e) => {
      if (!desktop.matches || e.pointerType !== 'mouse') return;
      closeTimer = setTimeout(() => close(item), 220);
    });
    trigger.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') { e.preventDefault(); open(item); item.querySelector('.mm-tab[aria-selected="true"]').focus(); }
    });
    // Closing when focus leaves the menu (keyboard users tabbing past it)
    item.addEventListener('focusout', (e) => {
      if (desktop.matches && !item.contains(e.relatedTarget)) close(item);
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape' || !openItem) return;
    const trigger = openItem.querySelector('.nav-trigger');
    close(openItem);
    trigger.focus();
  });
  document.addEventListener('click', (e) => {
    if (openItem && desktop.matches && !openItem.contains(e.target)) close(openItem);
  });
  // Following a link inside a panel closes the menu (and the mobile sheet)
  document.getElementById('main-nav').addEventListener('click', (e) => {
    if (!e.target.closest('.mm-panel a, .nav-link')) return;
    close(openItem);
    header.classList.remove('menu-open');
    document.getElementById('menu-toggle').setAttribute('aria-expanded', 'false');
  });
  desktop.addEventListener('change', () => close(openItem));
})();
