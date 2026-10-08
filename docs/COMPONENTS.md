# Squarezix component library

Open **`/components.html`** (noindex, not linked from the site). Every specimen on it is rendered by the same builder function the real pages use, so it cannot drift from the site.

## Where things live
| What | Where |
|---|---|
| Design tokens (colour, type scale per device, spacing, radius, shadows, glass) | `tokens.css` (brand colours stay in `styles.css`). Mirrors the Figma file **Squarezix — Design System → Foundations** |
| The one button, contact popup, quick-contact dock | `site-ui.css` / `site-ui.js` (added to every page by `scripts/apply_site_ui.py`) |
| Service-page sections (hero, list, pillars, cards, process, compare, timeline, FAQ, CTA …) | builders in `scripts/build_service_pages.py`, styles in `service-static.css` |
| Company / portfolio blocks (folder card, pocket, bookshelf, note board, filter bar, project timeline …) | builders in `scripts/build_company_pages.py`, styles in `company.css`, behaviour in `company.js` |
| The library page itself | `scripts/build_components.py` → `components.html` (styles: `components.css`) |

## Build a page from components
Pages are lists of `(kind, *args)` sections; each kind is one component and takes plain data:

```python
('statement', 'AI search', 'Your customers search smarter. <em>We make sure they find you.</em>', 'One paragraph.')
('nodes',     'Our Solutions', 'Comprehensive <em>Solutions</em>', {'intro': '…', 'items': [('Title', 'Description.', {'tag': 'Service', 'kw': ['chip']})]}, 'services')
('bento',     'Reliable Solutions', 'How we <em>stand out</em>', {'items': [('Title', 'Text.', {})], 'grid': 'rem2'})
('faq',       'FAQs', 'Questions about <em>our work?</em>', [('Question?', 'Answer.')], 'Intro line.')
```

Register the list in `PAGES` (or a `layout=` on a sub-page) in `scripts/build_service_pages.py`, then run `python3 scripts/build_service_pages.py`. Never hand-edit generated pages.

## Rules that keep it consistent
- One button only (`.zx-btn`); add `data-contact-open` to open the popup.
- Colours, spacing, radii and shadows come from tokens; shadows are always black.
- Three fonts only: Sora, DM Sans, Instrument Serif italic (accent word).
- Keep content out of components: pass it as data.
- After changing components, run `python3 scripts/build_components.py` to refresh the library.
