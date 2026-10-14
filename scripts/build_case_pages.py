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


def page(i, order):
    c = order[i]
    prev_c, next_c = order[i - 1], order[(i + 1) % len(order)]
    site = 'client' in c
    name = c['client'] if site else c['title']
    if site:
        badge = f'Case Study {c["no"]} / 03'
        sub = f'{c["kind"]} · {c["industry"]} · {c["year"]}'
        media = f'<img src="{c["img"]}" alt="{e(c["alt"])}" />'
        stats = ''.join(f'<li><b>{e(v)}</b><span>{e(l)}</span></li>' for v, l in c['results'])
        chips = ''.join(f'<li>{e(x)}</li>' for x in c['services'])
        article = f'''<ul class="cd-stats" data-rise>{stats}</ul>
        <h2 id="challenge">The challenge</h2>
        <p>{e(c["challenge"])}</p>
        <h2 id="approach">What we did</h2>
        <p>{e(c["did"])}</p>
        <ul class="cmp-chips cd-chips">{chips}</ul>
        <h2 id="results">Results</h2>
        <p>{" · ".join(f"<strong>{e(v)}</strong> {e(l.lower())}" for v, l in c["results"])}</p>'''
        toc = [('challenge', 'The challenge'), ('approach', 'What we did'), ('results', 'Results')]
        facts = [('Client', c['client']), ('Project', c['kind']), ('Industry', c['industry']), ('Year', c['year']), ('Services', ', '.join(c['services']))]
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
    out += B.shelf(c['slug'], compact=True)
    out += B.cta_panel('Let’s write <em>your chapter next.</em>', 'Tell us what you want to launch, fix or grow — we’ll come back with a plan within five days.', 'Start a Project', '#ab-contact')
    B.write(f'case-{c["slug"]}', f'{name} — Case Study | SquareZix', f'{name}: {lead}', 'work', out)


def main():
    order = [B._case_by(s) for s in B.SHELF_ORDER]
    for i in range(len(order)):
        page(i, order)


if __name__ == '__main__':
    main()
