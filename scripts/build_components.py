"""Builds components.html: the Squarezix component library / showcase (a developer reference, not a website page).

Every specimen is rendered by the SAME builder function the real pages use, so the library can never drift from the site.
Foundations (tokens) come from tokens.css, which mirrors the Figma file "Squarezix — Design System" (page "Foundations").

Run:  python3 scripts/build_components.py      (also run by scripts/build_service_pages.py via apply_site_ui? no: run it by hand)
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_service_pages as S  # noqa: E402
import build_company_pages as C  # noqa: E402
from offpage_content import OFFPAGE_LAYOUT  # noqa: E402
from dev3_pages import MIG_PAGE  # noqa: E402
from social_content import SOCIAL_PAGE  # noqa: E402

ROOT = S.ROOT
VER = '20261070b'
esc = html.escape


# ------------------------------------------------------------------ helpers
def sec(layout, kind, nth=0):
    """The nth section of a given kind from a page layout: (kind, *args)."""
    return [s for s in layout if s[0] == kind][nth]


def render(section):
    kind, *args = section
    return S.KINDS[kind](*args)


def page(file):
    return next(p for p in S.PAGES if p['file'] == file)


def slice_html(path, start, end, include_end=True):
    src = (ROOT / path).read_text()
    i = src.index(start)
    j = src.index(end, i) + (len(end) if include_end else 0)
    return src[i:j]


def code(text, summary='Usage'):
    return f'<details class="cl-code"><summary>{esc(summary)}</summary><pre>{esc(text.strip(chr(10)))}</pre></details>'


def markup(htm, limit=2600):
    flat = re.sub(r'\n\s*\n+', '\n', htm).strip()
    flat = re.sub(r' data-(rise|reveal)(="[^"]*")?', '', flat)
    flat = re.sub(r' style="--d: [^"]*"', '', flat)
    if len(flat) > limit:
        flat = flat[:limit].rsplit('>', 1)[0] + '>\n<!-- … -->'
    return code(flat, 'Rendered markup (shortened)')


def props_table(rows):
    body = ''.join(f'<tr><td><code>{esc(n)}</code></td><td>{esc(t)}</td><td>{esc(d)}</td></tr>' for n, t, d in rows)
    return f'<table class="cl-props"><thead><tr><th>Prop</th><th>Type</th><th>Description</th></tr></thead><tbody>{body}</tbody></table>'


def meta(**kw):
    items = ''.join(f'<li><b>{k.replace("_", " ")}</b> {esc(v)}</li>' for k, v in kw.items() if v)
    return f'<ul class="cl-meta">{items}</ul>'


def spec(sid, name, fn, purpose, specimen, props=None, usage='', note='', frame='', **m):
    """One component card: name, purpose, variants/sizes/states/responsive, live specimen, props, usage, markup."""
    return (f'<article class="cl-spec" id="c-{sid}"><div class="cl-spec-head"><h3>{esc(name)}</h3><code>{esc(fn)}</code></div>'
            f'<p class="cl-purpose">{purpose}</p>{meta(**m)}'
            f'<div class="cl-frame {frame}">{specimen}</div>'
            f'{props_table(props) if props else ""}{code(usage) if usage else ""}{f"<p class=cl-note>{note}</p>" if note else ""}</article>')


CATS = []  # (id, title, intro, [specs])


def cat(cid, title, intro, specs):
    CATS.append((cid, title, intro, specs))


# ------------------------------------------------------------------ 1. Foundations (tokens)
def swatch(label, var, extra=''):
    return f'<div class="cl-sw"><i style="background:var({var}){extra}"></i><b>{label}</b><code>{var}</code></div>'


colour = ''.join([
    swatch('brand/purple', '--brand-purple'), swatch('brand/pink', '--brand-pink'), swatch('bg/page', '--bg-dark'),
    swatch('bg/surface', '--header-dark-2'), swatch('bg/surface-deep', '--header-dark'), swatch('bg/band', '--band'),
    swatch('bg/black', '--black'), swatch('bg/inverse · text/primary', '--text-light'), swatch('bg/glass', '--glass'), swatch('bg/tint', '--brand-tint'),
    swatch('text/muted', '--text-muted'), swatch('text/body', '--text-body'), swatch('text/subtle', '--text-subtle'), swatch('text/faint', '--text-faint'),
    swatch('text/on-light', '--ink'), swatch('text/accent', '--accent-soft'), swatch('text/accent-pale', '--accent-pale'),
    swatch('border/subtle', '--border-subtle'), swatch('border/faint', '--border-faint'), swatch('border/brand-soft', '--border-brand-soft'),
    swatch('Gradient/Brand', '--brand-gradient'), swatch('Gradient/Brand hover', '--brand-gradient-hover')])
colour = colour.replace('background:var(--brand-gradient)', 'background:var(--brand-gradient)')

type_rows = [('t-display', 'Title/Display · Sora', 'Squarezix'), ('t-h1', 'Title/H1 · Sora 600', 'More than an agency'), ('t-accent-h1', 'Accent/H1 italic · Instrument Serif', 'agency.'),
             ('t-h2', 'Title/H2 · Sora', 'Proof, not promises'), ('t-accent-h2', 'Accent/H2 italic', 'promises.'), ('t-h3', 'Title/H3 · Sora', 'Digital Stream'),
             ('t-h4', 'Title/H4 · Sora', 'Structured Process'), ('t-stat', 'Accent/Stat italic', '+212%'),
             ('t-body-lg', 'Body/Large · DM Sans', 'One partner, four disciplines.'), ('t-body', 'Body/Default · DM Sans', 'Every project follows: Discover → Design → Build → Grow'),
             ('t-body-sm', 'Body/Small · 13.5px', 'Supporting text and captions'), ('t-button', 'UI/Button · 15px 500', 'Contact us'), ('t-nav', 'UI/Nav · 15px', 'Services'),
             ('t-badge', 'UI/Badge · 12px 500', 'Our approach'), ('t-label', 'UI/Label caps · 11px', 'The challenge'), ('t-meta', 'UI/Meta · 12.5px', 'August 25, 2025')]
type_html = '<div class="cl-type">' + ''.join(f'<div><small>.{c}<br>{esc(n)}</small><span class="{c}">{esc(s)}</span></div>' for c, n, s in type_rows) + '</div>'
space_html = '<div class="cl-space">' + ''.join(
    f'<div><i style="width:var(--space-{k});height:var(--space-{k})"></i>{k} · {v}</div>' for k, v in
    (('2xs', 4), ('xs', 8), ('sm', 12), ('md', 16), ('lg', 24), ('xl', 32), ('2xl', 48), ('3xl', 64), ('4xl', 96))) + '</div>'
radius_html = '<div class="cl-space">' + ''.join(
    f'<div><i style="width:96px;height:64px;border-radius:var(--radius-{k});background:var(--header-dark-2);border:1px solid var(--border-subtle)"></i>{k} · {v}</div>'
    for k, v in (('sm', '8'), ('md', '12'), ('lg', '16'), ('xl', '22'), ('pill', '999'))) + '</div>'
shadow_html = '<div class="cl-shadow">' + ''.join(
    f'<div style="box-shadow:var(--shadow-{k})">--shadow-{k}</div>' for k in ('card', 'lift', 'button', 'panel')) + \
    '<div style="background:var(--glass);color:#16161b;backdrop-filter:blur(var(--glass-blur))">--glass + blur 22</div></div>'
layout_html = '''<table class="cl-props"><thead><tr><th>Token</th><th>Desktop</th><th>Tablet ≤1080px</th><th>Mobile ≤700px</th></tr></thead><tbody>
<tr><td><code>--layout-page-width</code></td><td>1440</td><td>768</td><td>375</td></tr><tr><td><code>--layout-gutter</code></td><td>96</td><td>40</td><td>16</td></tr>
<tr><td><code>--layout-section-gap</code></td><td>150</td><td>110</td><td>72</td></tr><tr><td><code>--layout-card-gap</code></td><td>24</td><td>20</td><td>16</td></tr>
<tr><td><code>--type-display</code></td><td>96</td><td>64</td><td>44</td></tr><tr><td><code>--type-h1</code></td><td>64</td><td>48</td><td>36</td></tr>
<tr><td><code>--type-h2</code></td><td>56</td><td>42</td><td>32</td></tr><tr><td><code>--type-h3</code></td><td>28</td><td>24</td><td>22</td></tr>
<tr><td><code>--type-h4</code></td><td>20</td><td>19</td><td>18</td></tr><tr><td><code>--type-body-lg</code></td><td>18</td><td>17</td><td>16</td></tr>
<tr><td><code>--type-body</code></td><td>16</td><td>16</td><td>15</td></tr><tr><td><code>--type-accent-h1</code></td><td>72</td><td>54</td><td>40</td></tr>
<tr><td><code>--type-accent-h2</code></td><td>63</td><td>47</td><td>36</td></tr><tr><td><code>--type-stat</code></td><td>54</td><td>44</td><td>34</td></tr></tbody></table>'''

cat('foundations', 'Foundations', 'Design tokens from the Figma "Foundations" page. Defined in <code>tokens.css</code> (new) and <code>styles.css</code> (brand colours). Use the variable, never the raw value.', [
    spec('colour', 'Colour', 'var(--…)', 'Semantic colour tokens. Brand colours only; shadows are never brand-coloured.', f'<div class="cl-swatches">{colour}</div>',
         usage='background: var(--bg-dark);\ncolor: var(--text-body);\nborder: 1px solid var(--border-faint);\nbackground: var(--brand-gradient);'),
    spec('typography', 'Typography', '.t-display … .t-meta', 'Three families only: Sora (titles), DM Sans (body and UI), Instrument Serif italic (the accent word inside a title). Sizes switch with the device mode.', type_html,
         usage='<h2 class="t-h2">Proof, not <em class="t-accent-h2">promises.</em></h2>'),
    spec('layout', 'Layout and device scale', '--layout-*, --type-*', 'Values that change per device. Tablet layout at ≤1080px, phone layout at ≤700px (Figma "Device" collection).', layout_html),
    spec('spacing', 'Spacing and radius', '--space-*, --radius-*', 'One spacing scale (4 → 96) and five radii.', space_html + '<div style="height:28px"></div>' + radius_html,
         usage='padding: var(--space-lg);\nborder-radius: var(--radius-xl);'),
    spec('shadows', 'Shadows and glass', '--shadow-*, --glass', 'All shadows are black with opacity. Glass = near-white fill + 22px backdrop blur (the header).', shadow_html,
         usage='box-shadow: var(--shadow-card);\nbackdrop-filter: blur(var(--glass-blur));'),
])

# ------------------------------------------------------------------ 2. Actions and labels
PH = S.PHONE
btn_specs = f'''<div class="cl-row">
<div class="cl-lab"><a href="#" class="zx-btn" onclick="return false">{PH} Contact us</a><small>Default · icon + label</small></div>
<div class="cl-lab"><a href="#" class="zx-btn" onclick="return false">Start a Project</a><small>Label only</small></div>
<div class="cl-lab"><a href="#" class="zx-btn" onclick="return false">View more projects <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a><small>Trailing arrow</small></div>
<div class="cl-lab"><button type="button" class="zx-btn" disabled>Disabled</button><small>Disabled</small></div>
<div class="cl-lab"><button type="button" class="zx-btn" data-contact-open>Open contact form</button><small>Opens the contact popup</small></div>
</div>'''
badge_specs = '''<div class="cl-row"><div class="cl-lab"><span class="svc-badge">Our approach</span><small>Eyebrow badge</small></div>
<div class="cl-lab"><span class="svc-badge ab-badge">Social Media Marketing</span><small>Hero badge</small></div></div>'''
chip_specs = '''<div class="cl-row" style="align-items:flex-start"><div class="cl-lab"><ul class="ec-chips"><li>Next.js</li><li>Vue.js</li><li>Shopify Hydrogen</li></ul><small>Card chips (.ec-chips)</small></div>
<div class="cl-lab"><ul class="px-chips"><li>URL redirect mapping</li><li>Database validation</li></ul><small>Process chips (.px-chips)</small></div></div>'''
head_specs = S.head('Badge', 'Section title with <em>accent words</em>', 'Optional intro paragraph that explains the section in one or two lines.', center=True) + \
    '<div style="height:28px"></div>' + S.head('Badge', 'Left-aligned <em>heading</em>', 'Same component, left aligned.')

cat('actions', 'Actions and labels', 'The smallest building blocks. There is exactly one button style on the whole site.', [
    spec('button', 'Button', '.zx-btn', 'The single primary button (Figma Frame 19: <code>assets/brand/btn-primary.pdf</code>). Used for every action on the site; only the label and optional icon change.',
         btn_specs, props=[('label', 'text / children', 'Button text. Keep it to two or three words.'), ('icon', 'svg (optional)', '16px line icon before or after the label.'),
                           ('data-contact-open', 'attribute', 'Opens the contact popup (set automatically on links to #ab-contact).'), ('disabled', 'attribute', 'Dims to 45% and blocks clicks.')],
         usage='<a href="#ab-contact" class="zx-btn" data-contact-open>Contact us</a>\n<button type="submit" class="zx-btn">Send message</button>',
         note='Hover lifts 1px and brightens. Focus shows a lilac outline. Under 900px the header button drops to 42px; everywhere else it is 48px.',
         sizes='one size: 48px tall', states='default · hover · focus · active · disabled', responsive='fixed size, header version shrinks ≤900px'),
    spec('badge', 'Badge', '.svc-badge', 'Small outlined pill that labels a section ("Our approach", "FAQs").', badge_specs,
         props=[('text', 'text', 'Two to three words, sentence case.')], usage='<span class="svc-badge">Our approach</span>', variants='eyebrow · hero'),
    spec('chips', 'Chip list', '.ec-chips · .cmp-chips · .px-chips', 'Short keyword pills inside cards and panels.', chip_specs,
         props=[('items', 'string[]', 'Keywords, one to four words each.')], usage="{'kw': ['Next.js', 'Vue.js', 'Shopify Hydrogen']}", variants='card · panel · process'),
    spec('section-head', 'Section header', 'head(badge, title, intro, center)', 'Badge + title with one serif-italic accent phrase + optional intro. Opens every section.', head_specs,
         props=[('badge', 'str', 'Eyebrow text.'), ('title', 'html str', 'Title; wrap the accent phrase in <em>.'), ('intro', 'str', 'Optional paragraph.'), ('center', 'bool', 'Centre alignment.')],
         usage="head('Our approach', 'From brief to <em>launch</em>', 'Optional intro.', center=True)", variants='left · centred', responsive='type sizes follow the device scale'),
])

# ------------------------------------------------------------------ 3. Page sections (service pages)
hero_p = dict(badge='Badge', h1=['Headline words', 'accent phrase', 'close'], grad=1, lead='One or two sentences that say what the page offers and who it is for.')
wd = page('website-development.html')
pillars_sec = wd['sections'][0]
dev_list = S.listing(*wd['list'][:2], {**wd['list'][2], 'items': wd['list'][2]['items'][:6]}, sid='cl-list')
nodes_sec = sec(MIG_PAGE['layout'], 'nodes')
nodes_html = S.nodes(nodes_sec[1], nodes_sec[2], {**nodes_sec[3], 'items': nodes_sec[3]['items'][:3]}, 'cl-nodes')
bento_sec = sec(SOCIAL_PAGE['sections'], 'bento')
bento_html = S.bento(bento_sec[1], bento_sec[2], {**bento_sec[3], 'items': bento_sec[3]['items'][:5]})
bento5 = sec(OFFPAGE_LAYOUT, 'bento')
bento5_html = S.bento(bento5[1], bento5[2], bento5[3])
illus_sec = sec(SOCIAL_PAGE['sections'], 'illus')
illus_html = S.illus(illus_sec[1], illus_sec[2], illus_sec[3])
proc_sec = sec(MIG_PAGE['layout'], 'process')
proc_html = S.process_iso(proc_sec[1], proc_sec[2], {**proc_sec[3], 'items': proc_sec[3]['items'][:4]}, 'cl-process')
cmp_sec = sec(MIG_PAGE['layout'], 'compare')
vs_sec = sec(OFFPAGE_LAYOUT, 'vs')
tl_sec = sec(page('headless-ecommerce-development.html')['sections'], 'timeline')
ind_html = S.industries('Industries', 'Websites for businesses <em>across industries</em>', S.L['web']['industries'])
faq_sec = sec(OFFPAGE_LAYOUT, 'faq')
faq_html = S.faq(faq_sec[1], faq_sec[2], faq_sec[3][:4], faq_sec[4])
stmt = sec(OFFPAGE_LAYOUT, 'statement')
blog_html = S.live_blog(('Blogs', 'What’s going on <em>your Industry</em>', [('Social Media Marketing', 'Can You Post Images on TikTok? Here’s Everything You Need to Know'),
                                                                          ('Website Development', 'Why Payload CMS Is Becoming a Powerful Choice for Next.js Websites')]))
about = (ROOT / 'about-us.html').read_text()
contact_html = re.sub(r' data-(rise|reveal)(="[^"]*")?', '', about[about.index('<section class="ab-contact"'):about.index('</main>')])

item_prop = ('items', 'list', '(title, description, meta) tuples; meta carries tag / kw / close / art depending on the component.')
cat('sections', 'Page sections', 'Full-width sections that stack to make a service page. Each is one builder function in <code>scripts/build_service_pages.py</code> that takes plain data.', [
    spec('hero', 'Hero', 'hero(p)', 'Wave-gradient hero: badge, three-part headline (the middle part is the serif-italic accent), lead and one button. Includes the looping services strip.',
         S.hero(hero_p), props=[('badge', 'str', 'Eyebrow text.'), ('h1', 'str[3]', 'Three headline parts.'), ('grad', 'int', 'Index of the part set in serif italic.'), ('lead', 'str', 'One or two sentences.')],
         usage="hero({'badge': 'Social Media Marketing', 'h1': ['Social Media', 'Agency', 'in Dubai'], 'grad': 1, 'lead': '…'})",
         frame='cl-frame--bare', responsive='headline scales with the device scale; button stays one size'),
    spec('statement', 'Statement', 'statement(badge, title, text)', 'One centred paragraph under a section header: the AI-search intro, or any short positioning statement.',
         S.statement(*stmt[1:]), props=[('badge', 'str', 'Eyebrow.'), ('title', 'html str', 'Title with accent.'), ('text', 'str', 'One paragraph.')],
         usage="statement('AI search', 'Your customers search smarter. <em>We make sure they find you.</em>', 'One paragraph.')"),
    spec('listing', 'Service list', 'listing(badge, title, data, sid)', 'Numbered rows in two panels, each with title, one line and an arrow to its page. The parent page of a service family.',
         dev_list, props=[('items', 'list', '(title, description, chips) tuples; links come from the SUBPAGES map.'), ('intro', 'str', 'Paragraph under the title.'), ('panels', '[(bold, rest)]×2', 'Caption under each panel.')],
         usage="listing('Development services', 'Best Website Development <em>Agency in Dubai</em>', {'intro': '…', 'items': SVC['web']['items'], 'panels': [(…), (…)]})",
         responsive='two panels → one column ≤1000px'),
    spec('pillars', 'Approach pillars', 'pillars(badge, title, data)', 'Three infographic cards (Plan / Build / Launch): icon, hairline and a list of points.',
         S.pillars(*pillars_sec[1:3], {**pillars_sec[3]}), props=[('items', '[(name, "", points[])]×3', 'Name picks the icon (Plan, Create, Launch, Discover, Design, Deliver, Grow …).')],
         usage="pillars('Our approach', 'From brief to <em>launch-ready build</em>', pillars_of(('Plan', ['…']), ('Build', ['…']), ('Launch', ['…'])))", responsive='3 across → stacked ≤900px'),
    spec('industries', 'Industries strip', 'industries(badge, title, data)', 'Looping strip of industries (it pauses on hover; outro.js clones the group so the loop has no seam).',
         ind_html, props=[item_prop], usage="industries('Industries', 'Websites for businesses <em>across industries</em>', LIVE['web']['industries'])", responsive='keeps looping at every width'),
    spec('cta', 'Call-to-action band', 'cta(title, text)', 'A single card with a heading, one sentence and the button.',
         S.cta(*sec(OFFPAGE_LAYOUT, 'cta')[1:]), props=[('title', 'html str', 'Heading.'), ('text', 'str', 'One sentence.')],
         usage="cta('Be everywhere your audience is <em>searching</em> with Squarezix', 'Connect with our AI experts …')"),
    spec('faq', 'FAQ', 'faq(badge, title, qa, intro)', 'Accordion on the lighter band. One item open at a time; answers can include a "- " bullet list.',
         faq_html, props=[('qa', '[(question, answer)]', 'Answer text; lines starting "- " become bullets.'), ('intro', 'str', 'Line under the title.')],
         usage="faq('FAQs', 'Questions about <em>our work?</em>', [('Question?', 'Answer.')], 'Intro line.')", states='open · closed · hover', note='Behaviour: faq.js.'),
    spec('blog', 'Blog cards', 'live_blog((badge, title, posts))', 'Latest articles as cards: image, tag, title and a read-more arrow. Sits straight after the FAQ.',
         blog_html, props=[('posts', '[(tag, title)]', 'Two to four posts.')], usage="live_blog(('Blogs', 'What’s going on <em>your Industry</em>', [('Website Development', 'Post title')]))", responsive='grid → one column ≤700px'),
    spec('contact', 'Contact section', 'about-us.html #ab-contact', 'Expansion note + "Ready to Begin?" form. The same block closes every page.',
         contact_html, props=[('form', '#ab-form', 'Name, email, phone, message; validates then opens the visitor’s mail app.')], frame='cl-frame--bare', responsive='two columns → stacked ≤900px',
         note='Lifted from the About page so every page shares one copy of it.'),
])

# ------------------------------------------------------------------ 4. Cards and content blocks
cat('cards', 'Cards and content blocks', 'Reusable blocks that hold a service, benefit, step or comparison. They take the same (title, description, meta) data, so one content set can switch component.', [
    spec('node-cards', 'Feature cards', 'nodes(badge, title, data, sid)', 'Heading pinned left, one column of node cards on the right: tag, mark, title, first sentence, detail box, chips and closing line.',
         nodes_html, props=[('items', '(title, desc, {tag, kw[], close})', 'tag = small label; kw = chips; close = closing sentence.'), ('intro', 'str', 'Paragraph under the title.')],
         usage="nodes('Our Solutions', 'Comprehensive <em>Migration Solutions</em>', {'intro': '…', 'items': [node('Title', 'Tag', 'Description. More detail.', ['chip'], 'Closing line.')]}, 'services')",
         responsive='side heading on top ≤1000px'),
    spec('bento', 'Stand-out cards (bento)', 'bento(badge, title, data)', 'Grid of benefit cards. Optional chip lists and closing lines. The grid variant balances the last row.',
         bento_html, props=[item_prop, ('grid', "'' | 'b5' | 'rem2'", "'b5' = 3+2 cards; 'rem2' = 3n+2 cards with two wide cards last."), ('meta.chips', 'str[]', 'Turns the card into a chip card.')],
         usage="bento('Reliable Solutions', 'How Squarezix <em>stands out</em>', {'intro': '…', 'items': [('Title', 'Text.', {})], 'grid': 'rem2'})", variants='default · b5 · rem2 · chip card', responsive='3 → 2 → 1 columns'),
    spec('bento-b5', 'Bento, five cards', 'bento(…, grid="b5")', 'The same component with five cards: three on top, two wider cards below.', bento5_html, usage="…, {'items': FIVE, 'grid': 'b5'}"),
    spec('illus-cards', 'Illustration cards', 'illus(badge, title, data)', 'Isometric line-light scene above a title and one line. 28 scenes are drawn in <code>scripts/iso_art.py</code>; pick one with <code>art</code>.',
         illus_html, props=[('items', '(title, desc, {art})', 'art: maps, profile, geogrid, leads, authority, threepack, district, ai, server, speed, lock, payment, backup, brokenlink, forms, browsers, firewall, updates.'), ('grid', "'' | 'rem2'", 'Last row layout.')],
         usage="illus('Services', 'Social Media Marketing <em>Services</em>', {'intro': '…', 'items': [('Title', 'Text.', {'art': 'leads'})]})", responsive='two wide + three per row → 2 → 1 columns'),
    spec('process', 'Process plates', 'process_iso(badge, title, data, sid)', 'Steps as tilted glass plates (left) with a glowing progress line; the chosen step opens in a panel beside them. On a phone the plates become a swipe row.',
         proc_html, props=[('items', '(title, desc, {tag, kw[], close})', 'First sentence = lead; the rest = detail; kw = checklist chips.')],
         usage="process_iso('Secure Process', 'Our Secure 7-Step <em>Website Migration Process</em>', {'intro': '…', 'items': STEPS}, 'process')",
         states='plate: default · hover · selected', responsive='vertical plates ≥641px; horizontal swipe ≤640px', note='Behaviour: px-process.js (arrow keys also move between steps).'),
    spec('compare', 'Compare panel', 'compare(badge, title, data)', 'A muted "problem" panel beside a glowing "our approach" panel with a keyword hub diagram.',
         S.compare(*cmp_sec[1:]), props=[('left', '{dim, title, chips[], link}', 'The problem side.'), ('right', '{title, text, hub, keywords[], tag, cta}', 'The approach side; keywords sit around the hub.')],
         usage="compare('Planning', 'Why you need <em>strategic migration</em>', {'left': {…}, 'right': {…}})", responsive='side by side → stacked ≤900px'),
    spec('versus', 'Versus panel', 'vs(badge, title, data)', 'Two panels side by side: the quieter other half on the left, the page’s own topic highlighted on the right.',
         S.vs(*vs_sec[1:]), props=[('left / right', '{title, note, items[]}', 'Check-list panels.')], usage="vs('On-Page vs Off-Page', 'On-Page SEO <em>vs. Off-Page SEO</em>', {'intro': '…', 'left': {…}, 'right': {…}})"),
    spec('timeline', 'Methodology timeline', 'timeline(badge, title, data)', 'The workflow as a node graph on a dotted canvas: six steps in a snake, joined by wires. Hover lights a node and its wire.',
         S.timeline(*tl_sec[1:]), props=[('items', '(title, description, [])×6', 'Six steps, snake order.')], usage="timeline('Methodology', 'Our proven <em>workflow</em>', {'items': [('Step', 'One line.', [])]})", responsive='snake → single column ≤900px'),
])

# ------------------------------------------------------------------ 5. Work and portfolio blocks
pf_cards = '<div class="pf-cards">' + ''.join(re.findall(r'<article class="pf-card pf-fc.*?</article>', (ROOT / 'portfolio.html').read_text(), re.S)[:4]) + '</div>'
pf_stats = re.search(r'<div class="pf-results">.*?</div>\s*<p class="pf-note"', (ROOT / 'portfolio.html').read_text(), re.S).group(0).rsplit('<p class="pf-note"', 1)[0] + '</div>'
pf_stats = (ROOT / 'portfolio.html').read_text()
pf_stats = pf_stats[pf_stats.index('<div class="pf-results">'):]
pf_stats = pf_stats[:pf_stats.index('<p class="pf-note"')].rstrip() + '\n'
filter_html = C.filterbar('Filter projects', [('cap', 'Capability', 'All Capabilities', [('digital', 'Digital Experience'), ('marketing', 'Digital Marketing')]),
                                               ('ind', 'Industry', 'All Industries', [('tech', 'Technology & Innovation'), ('ecom', 'E-commerce & Retail')])], 'cl-filter')
tl2 = C.pk_timeline().replace('class="tl2"', 'class="tl2 is-static"')
tl2 = tl2.replace(' id="timeline"', ' id="cl-timeline"')
cat('work', 'Work and portfolio blocks', 'Blocks that present projects. Their behaviour lives in <code>company.js</code> and is wired by element ids on the Portfolio page; here they are shown in their resting state.', [
    spec('folder-card', 'Project folder card', '.pf-card.pf-fc', 'A project as a frosted folder: peeking photos, a clipped sticky note with the key result, the kind icon, the title below. The description fades in inside the folder on hover.',
         pf_cards, props=[('title', 'str', 'Project name, shown under the folder.'), ('note', '(big, small)', 'Sticky-note result, e.g. ("+212%", "Demo requests").'), ('desc', 'str', 'Shown on hover (always visible on touch screens).'), ('kind', 'icon', 'Website · E-commerce · Product & AI · Social reel.')],
         usage='<article class="pf-card pf-fc" data-cap="digital" data-ind="tech" data-out="leads"> … </article>', states='default · hover · focus', responsive='4 → 2 → 1 columns', note='Filtering reads data-cap / data-ind / data-out.'),
    spec('filter-bar', 'Filter bar', 'filterbar(label, selects, id)', 'One pill with three native selects plus a live "Showing N" count and a reset button.', filter_html,
         props=[('selects', '[(key, label, all_label, options)]', 'Each select filters items by their data-<key> attribute.')], usage="filterbar('Filter projects', [('cap', 'Capability', 'All Capabilities', [('digital', 'Digital Experience')])], 'pf-bar')",
         responsive='4 segments → 2×2 grid ≤700px'),
    spec('pocket', 'Category pocket', 'pk_pocket()', 'One pocket holding a card per category. Hover lifts a card and the pocket front shows its details; click filters the project list.',
         C.pk_pocket(), props=[('cats', 'list', 'name, line, set (the three filter values), paper, image, count.')], states='card: default · hover · focus · active', responsive='four cards → swipe row ≤760px'),
    spec('stats', 'Stat pills', '.pf-results', 'Large pill cards that pair a count-up number with a label.', pf_stats, props=[('value', 'number + suffix', 'Counted up when the pill scrolls into view (about.js).'), ('label', 'str', 'Small caps label.')],
         responsive='3 → 1 columns'),
    spec('timeline-pinned', 'Project timeline', 'pk_timeline()', 'A pinned section: as you scroll the track slides sideways, the line fills and each milestone draws in. Shown here in its static (reduced-motion) form.',
         tl2, props=[('PHASES', '[(when, name, role, initials, quote)]', 'Stages, in order.')], note='Live behaviour (pin + horizontal scroll) is in company.js and can be seen on portfolio.html.', responsive='pinned slide ≥ tablet; same on phones with larger type'),
    spec('note-board', 'Sticky-note board', 'collab()', 'Seven brand-paper sticky notes on a dotted canvas, beside a heading and a five-step row.', C.collab(), props=[('roles', '[(title, line)]', 'One note each, tilted slightly.')], responsive='2-3-2 layout → two per row ≤560px'),
    spec('bookshelf', 'Bookshelf', 'shelf(current, compact, href)', 'A case-study library as book spines. Hover pulls one off the shelf; each links to its project.', C.shelf(href='#bookshelf'),
         props=[('books', 'list', 'width, height %, colours, font style, tilt; the last book is the "your brand, next" slot.')], states='default · hover · current', responsive='row → swipe shelf ≤760px'),
])

# ------------------------------------------------------------------ 6. Forms and feedback
form_html = '''<form class="ab-form" onsubmit="return false" novalidate style="max-width:640px">
<label class="ab-field"><span>Your Name <b>*</b></span><input type="text" placeholder="Enter Your Name"></label>
<label class="ab-field"><span>Your Email <b>*</b></span><input type="email" placeholder="Enter Your Email"></label>
<label class="ab-field is-invalid ab-field--full"><span>Invalid state <b>*</b></span><input type="tel" placeholder="Lilac underline when a required field is empty"></label>
<label class="ab-field ab-field--full"><span>Your Message</span><textarea rows="3" placeholder="Type Here"></textarea></label></form>'''
cat('forms', 'Forms and feedback', 'Inputs and overlays. Behaviour for the popup and the contact dock lives in <code>site-ui.js</code> and is loaded on every page.', [
    spec('field', 'Form field', '.ab-field', 'Label + underlined input or textarea. Required fields carry a purple asterisk; errors use a lilac underline (never red).', form_html,
         props=[('name / email / phone / message', 'input', 'Add "ab-field--full" to span both columns.'), ('is-invalid', 'class', 'Error state.')], usage='<label class="ab-field"><span>Your Name <b>*</b></span><input type="text" required></label>',
         states='default · focus · invalid', responsive='two columns → one ≤520px'),
    spec('modal', 'Contact popup', '#zx-contact (site-ui.js)', 'A modal dialog opened by any button with <code>data-contact-open</code>. Validates, then hands off to the visitor’s mail app. Esc, ×, or a click outside closes it.',
         '<div class="cl-row"><button type="button" class="zx-btn" data-contact-open>Open the contact popup</button></div>', props=[('data-contact-open', 'attribute', 'Add to any link or button to open it.')],
         usage='<button class="zx-btn" data-contact-open>Contact us</button>', states='closed · open · success', note='Injected on every page by site-ui.js, so no markup is needed.'),
    spec('dock', 'Quick-contact dock', '.qc (site-ui.js)', 'A fixed pill on the right edge with WhatsApp, email and LinkedIn: always one tap away. Visible at the right of this page.',
         '<p class="cl-note" style="margin:0">Look at the right edge of this page: the dock is the live component. WhatsApp pulses; each icon shows a label on hover. On phones it moves to the bottom-right corner.</p>',
         props=[('WhatsApp', 'link', 'wa.me/971551318051 with a pre-filled message.'), ('Email', 'link', 'mailto:info@squarezix.com'), ('LinkedIn', 'link', 'company page.')], states='default · hover · focus', responsive='right edge ≥641px; bottom-right ≤640px'),
    spec('header', 'Header and navigation', '.site-header (menu.js)', 'Bright-glass header: logo, four mega-menu groups (Services · Development & Maintenance · Our Work · Insights) and the contact button. The menus are generated from the service data, so the list never drifts from the pages.',
         '<p class="cl-note" style="margin:0">The live header is at the top of this page. Desktop shows the full menu; tablet and phone collapse it into the hamburger sheet.</p>',
         states='default · scrolled · menu open', responsive='full menu ≥1081px; hamburger below'),
    spec('footer', 'Footer', '.szf (footer.css)', 'Pitch band, partner logos, contact details, link groups and the SQUAREZIX letter grid. Identical on every page.',
         '<p class="cl-note" style="margin:0">The live footer is at the bottom of this page.</p>', responsive='four columns → stacked ≤900px'),
])

# ------------------------------------------------------------------ page
nav = ''.join(f'<h2>{esc(t)}</h2>' + ''.join(f'<a href="#{m.group(1)}">{m.group(2)}</a>' for m in re.finditer(r'<article class="cl-spec" id="([^"]+)"><div class="cl-spec-head"><h3>([^<]*)</h3>', ''.join(sp)))
              for cid, t, intro, sp in CATS)
body = ''.join(f'<section class="cl-cat" id="cat-{cid}"><h2>{esc(t)}</h2><p class="cl-intro">{intro}</p>{"".join(sp)}</section>' for cid, t, intro, sp in CATS)
count = sum(len(sp) for *_x, sp in CATS)

src = (ROOT / 'about-us.html').read_text()
head_html, rest = src.split('<main', 1)
main, tail = rest.split('</main>', 1)
head_html = re.sub(r'<title>.*?</title>', '<title>Component Library | Squarezix</title>', head_html, flags=re.S)
head_html = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="Developer reference for the Squarezix design tokens and reusable components."', head_html)
head_html = head_html.replace('<head>', '<head>\n  <meta name="robots" content="noindex, nofollow" />', 1)
head_html = re.sub(r'(<link rel="stylesheet" href="about\.css[^>]*>)', rf'\1\n  <link rel="stylesheet" href="service-static.css?v={VER}" />\n  <link rel="stylesheet" href="company.css?v={VER}" />\n  <link rel="stylesheet" href="tokens.css?v={VER}" />\n  <link rel="stylesheet" href="components.css?v={VER}" />', head_html)
head_html = head_html.replace('<div class="nav-item is-current" data-menu="insights">', '<div class="nav-item" data-menu="insights">')
tail = tail.replace('<script src="about.js', f'<script src="waves-bg.js?v={VER}"></script>\n  <script src="faq.js?v={VER}"></script>\n  <script src="px-process.js?v={VER}"></script>\n  <script src="about.js', 1)

intro = ('<div class="cl-top"><span class="svc-badge">Developer reference</span><h1>Component <em>library</em></h1>'
         f'<p>{count} reusable components and the design tokens behind them, rendered by the same builder functions the real pages use. This is not a website page: '
         'pick components here and combine them with plain data to build any page. Foundations mirror the Figma file <code>Squarezix — Design System</code>; '
         'components are documented from the production code, which is the source of the final design.</p>'
         '<p>How to use: each card shows the live component, its variants and states, its props, and a one-line call. '
         'Builders live in <code>scripts/build_service_pages.py</code> and <code>scripts/build_company_pages.py</code>; styles in <code>service-static.css</code>, <code>company.css</code>, <code>site-ui.css</code>; tokens in <code>tokens.css</code>.</p></div>')
out = f'{head_html}<main id="components" class="ss co-page cl">\n{intro}<div class="cl-layout"><nav class="cl-nav" aria-label="Components">{nav}</nav><div class="cl-main">{body}</div></div>\n</main>{tail}'
(ROOT / 'components.html').write_text(out)
print(f'wrote components.html: {len(CATS)} categories, {count} specimens, {len(out) // 1024} KB')

import apply_site_ui  # noqa: E402
apply_site_ui.main()
