#!/usr/bin/env python3
"""Case-study detail pages: case-<slug>.html for the three website cases and five social reels in build_company_pages.CASES / REEL_CASES.

Copy is the home-page case-study section (challenge, what we did, services, results); no new claims are added.
Layout mirrors the blog detail page: header, hero media, story column, sticky facts rail, previous / next, shelf, CTA.
Run via build_company_pages.py (it calls main()).
"""
import sys
from html import escape as e
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_company_pages as B


# ---- Case-study narrative (SquareZix 12-section framework: context -> diagnosis -> direction -> execution -> impact -> continuation).
# Only sections that have real material are rendered. Everything below is either the home-page case copy already in
# build_company_pages.CASES or a split of it; add a key here when verified material exists and the section appears:
#   pain=[(point, implication)]   research=text   insights=[text]   approach=text   blueprint=[(title, text)]
#   final=text   before_after=[(metric, before, after)]   quote=(text, who)   next=text   timeline=text   market=text
# Never add invented figures, research or testimonials.
DETAIL = {
    'digital-stream': dict(
        work=['Rewrote the story around one outcome.', 'Redesigned every page to lead to a demo.', 'Rebuilt the front end for speed.'],
        groups=[('Business', 0), ('Performance', 1), ('Experience & operations', 2)], duration='9 weeks, brief to launch'),
    'hero-gradients': dict(
        work=['Moved the store to a headless stack.', 'Cut checkout from five screens to two.', 'Rebuilt product pages around the photography.'],
        groups=[('Business', 0), ('Business', 1), ('Business', 2)]),
    'lissr-ai': dict(
        work=['Mapped the first ten minutes of use.', 'Redesigned onboarding around a single task.', 'Rebuilt the dashboard to match.'],
        groups=[('Business', 0), ('Experience & operations', 1), ('Experience & operations', 2)]),
}


def _site_sections(c, order):
    """Return [(id, title, html)] for the sections that have material, in framework order."""
    d = DETAIL.get(c['slug'], {})
    secs = []
    facts = [('Client', c['client']), ('Industry', c['industry']), ('Project', c['kind']), ('Year', c['year']),
             ('Services', ', '.join(c['services']))]
    if d.get('duration'):
        facts.append(('Duration', d['duration']))
    if d.get('market'):
        facts.append(('Market', d['market']))
    intro = (f'<p>{e(c["client"])} is a {e(c["industry"])} business. SquareZix worked on its {e(c["kind"].lower())} project: '
             f'{e(", ".join(c["services"]))}.</p>')
    secs.append(('intro', 'Project introduction', intro))
    secs.append(('challenge', 'The challenge', f'<p>{e(c["challenge"])}</p>'))
    if d.get('pain'):
        rows = ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in d['pain'])
        secs.append(('pain', 'Pain points', f'<div class="bp-table"><table><thead><tr><th>Pain point</th><th>Business implication</th></tr></thead><tbody>{rows}</tbody></table></div>'))
    if d.get('research') or d.get('insights'):
        h = f'<p>{e(d["research"])}</p>' if d.get('research') else ''
        h += ''.join(f'<blockquote><p>{e(t)}</p></blockquote>' for t in d.get('insights', []))
        secs.append(('research', 'Research & key insights', h))
    if d.get('approach'):
        secs.append(('approach', 'Strategic approach', f'<p>{e(d["approach"])}</p>'))
    if d.get('blueprint'):
        cards = ''.join(f'<li><b>{e(t)}</b><span>{e(x)}</span></li>' for t, x in d['blueprint'])
        secs.append(('blueprint', 'Solution blueprint', f'<ul class="cd-cards">{cards}</ul>'))
    work = d.get('work') or [c['did']]
    steps = ''.join(f'<li><i>{n:02d}</i><span>{e(t)}</span></li>' for n, t in enumerate(work, 1))
    chips = ''.join(f'<li>{e(x)}</li>' for x in c['services'])
    secs.append(('work', 'The work', f'<ol class="cd-steps">{steps}</ol><ul class="cd-chips" aria-label="Services">{chips}</ul>'))
    if d.get('final'):
        secs.append(('final', 'The final experience', f'<p>{e(d["final"])}</p>'))
    groups = d.get('groups') or [('Results', i) for i in range(len(c['results']))]
    stats = ''.join(f'<li><small>{e(g)}</small><b>{e(c["results"][i][0])}</b><span>{e(c["results"][i][1])}</span></li>' for g, i in groups)
    res = f'<ul class="cd-stats">{stats}</ul>'
    if d.get('before_after'):
        rows = ''.join(f'<tr><td>{e(m)}</td><td>{e(b)}</td><td>{e(a)}</td></tr>' for m, b, a in d['before_after'])
        res += f'<div class="bp-table"><table><thead><tr><th>Metric</th><th>Before</th><th>After</th></tr></thead><tbody>{rows}</tbody></table></div>'
    secs.append(('results', 'Results & business impact', res))
    if d.get('quote'):
        q, who = d['quote']
        secs.append(('client', 'Client perspective', f'<blockquote><p>{e(q)}</p></blockquote><p class="cd-who">{e(who)}</p>'))
    if d.get('next'):
        secs.append(('next', 'What’s next?', f'<p>{e(d["next"])}</p>'))
    return facts, secs


def _related(c, order):
    pool = [x for x in order if 'client' in x and x['slug'] != c['slug']]
    pool.sort(key=lambda x: (x['industry'] != c['industry'], x['kind'] != c['kind']))
    cards = ''.join(
        f'<a class="cd-rel" href="case-{x["slug"]}.html"><span class="cd-rel-img"><img src="{x["img"]}" alt="{e(x["alt"])}" loading="lazy" /></span>'
        f'<span class="cd-rel-body"><small>{e(x["kind"])} · {e(x["industry"])}</small><b>{e(x["client"])}</b>'
        f'<em>{e(x["results"][0][0])} {e(x["results"][0][1].lower())}</em></span></a>' for x in pool[:3])
    return (f'    <section class="co-sec cd-related" aria-labelledby="cd-rel-title">\n'
            f'      {B.head_block("Related work", "More <em>case studies</em>", "", sid="cd-rel-title")}\n'
            f'      <div class="cd-rel-grid">{cards}</div>\n    </section>\n')


def page(i, order):
    c = order[i]
    prev_c, next_c = order[i - 1], order[(i + 1) % len(order)]
    site = 'client' in c
    name = c['client'] if site else c['title']
    if site:
        badge = f'Case Study {c["no"]} / 03'
        sub = f'{c["kind"]} · {c["industry"]} · {c["year"]}'
        media = f'<img src="{c["img"]}" alt="{e(c["alt"])}" />'
        facts, secs = _site_sections(c, order)
        article = ''.join(
            f'<section class="cd-sec" id="{sid}"><p class="cd-no">{n:02d}</p><h2>{e(t)}</h2>{h}</section>\n        '
            for n, (sid, t, h) in enumerate(secs, 1))
        toc = [(sid, f'{n:02d} · {t}') for n, (sid, t, _) in enumerate(secs, 1)]
        lead = c['did']
    else:
        badge, sub = 'Social Reel', 'Short-form social video · Motion'
        media = (f'<video src="assets/reels/reel-{c["n"]}.mp4" poster="assets/reels/reel-{c["n"]}.jpg" controls playsinline muted loop '
                 f'preload="none" aria-label="{e(c["title"])} reel"></video>')
        article = f'<h2 id="about">About this reel</h2>\n        <p>{e(c["desc"])}</p>'
        toc = [('about', 'About this reel')]
        facts = [('Format', 'Short-form social video'), ('Craft', 'Motion · Social video'), ('Made for', 'Instagram · TikTok · Reels')]
        lead = c['desc']
    toc_html = ''.join(f'<li><a href="#{a}">{e(t)}</a></li>' for a, t in toc)
    facts_html = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in facts)
    out = f'''    <div class="bp-progress" aria-hidden="true"><i></i></div>
    <header class="bp-head">
      <span class="svc-badge" data-rise>{e(badge)}</span>
      <h1 class="bp-title" data-rise>{e(name)}</h1>
      <p class="cd-sub" data-rise>{e(sub)}</p>
      <p class="cd-lead" data-rise>{e(lead)}</p>
    </header>
    <figure class="bp-hero-img cd-media{"" if site else " cd-media--reel"}" data-rise>{media}</figure>
    <div class="bp-layout">
      <article class="bp-article" id="bp-article">
        {article}
      </article>
      <aside class="bp-rail">
        <dl class="cd-facts">{facts_html}</dl>
        <nav class="bp-toc" aria-label="On this page"><h2>On this page</h2><ol>{toc_html}</ol></nav>
        <div class="bp-cta"><h2>Want a result like <em>this?</em></h2><p>Tell us what you want to launch, fix or grow.</p>
          <a href="#ab-contact" class="zx-btn" data-contact-open>Start a project</a></div>
      </aside>
    </div>
    <nav class="co-sec cd-pager" aria-label="More case studies">
      <a href="case-{prev_c['slug']}.html"><span>Previous</span><b>{e(prev_c.get('client') or prev_c['title'])}</b></a>
      <a href="case-study.html#shelf" class="cd-pager-all">All case studies</a>
      <a href="case-{next_c['slug']}.html"><span>Next</span><b>{e(next_c.get('client') or next_c['title'])}</b></a>
    </nav>
'''
    if site:
        out += _related(c, order)
    out += B.shelf(c['slug'], compact=True)
    out += B.cta_panel('Have a similar challenge? <em>Let’s talk.</em>', 'Tell us what you want to launch, fix or grow — we’ll come back with a plan within five days.', 'Start a Project', '#ab-contact')
    B.write(f'case-{c["slug"]}', f'{name} — Case Study | SquareZix', f'{name}: {lead}', 'work', out)


def main():
    order = [B._case_by(s) for s in B.SHELF_ORDER]
    for i in range(len(order)):
        page(i, order)


if __name__ == '__main__':
    main()
