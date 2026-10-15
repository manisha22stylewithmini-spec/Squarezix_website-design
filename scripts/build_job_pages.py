#!/usr/bin/env python3
"""Job opening detail pages: job-<slug>.html per role in jobs_content.JOBS.
Fields follow the Career entry in the WordPress admin: Title, Country, City, Job Type, Workplace Type, Overview,
Qualifications, Key Responsibilities, Benefits. Layout reuses the blog/case detail styles (.bp-*)."""
import sys
from html import escape as e
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_company_pages as B
from jobs_content import JOBS


def _list(items):
    return '<ul>' + ''.join(f'<li>{e(x)}</li>' for x in items) + '</ul>'


def page(j):
    mail = f"mailto:info@squarezix.com?subject=Application%20%E2%80%94%20{e(j['title']).replace(' ', '%20')}"
    secs = [('overview', 'Overview', f'<p>{e(j["overview"])}</p>'),
            ('qualifications', 'Qualifications', _list(j['qualifications'])),
            ('responsibilities', 'Key responsibilities', _list(j['responsibilities'])),
            ('benefits', 'Benefits', _list(j['benefits']))]
    article = ''.join(f'<section class="cd-sec" id="{i}"><h2>{t}</h2>{h}</section>\n        ' for i, t, h in secs)
    toc = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t, _ in secs)
    facts = [('Team', j['team']), ('Job type', j['job_type']), ('Workplace', j['workplace']),
             ('Location', f"{j['city']}, {j['country']}")]
    facts_html = ''.join(f'<div><dt>{k}</dt><dd>{e(v)}</dd></div>' for k, v in facts)
    chips = ''.join(f'<li>{e(v)}</li>' for v in (j['job_type'], j['workplace'], f"{j['city']}, {j['country']}"))
    others = [x for x in JOBS if x['slug'] != j['slug']]
    others.sort(key=lambda x: x['team'] != j['team'])
    more = ''.join(
        f'<li><a class="ca-role" href="job-{x["slug"]}.html"><i>{n:02d}</i><span class="ca-role-t">{e(x["title"])}</span>'
        f'<span class="ca-role-l">{e(x["city"])} · {e(x["workplace"])}</span><span class="ca-role-a">{B.ARROW_R}</span></a></li>'
        for n, x in enumerate(others[:4], 1))
    apply_attrs = f'data-apply-open data-role="{e(j["title"], quote=True)}" data-team="{e(j["team"], quote=True)}"'
    out = f'''    <header class="bp-head">
      <span class="svc-badge" data-rise>{e(j['team'])}</span>
      <h1 class="bp-title" data-rise>{e(j['title'])}</h1>
      <ul class="cd-chips jb-chips" data-rise>{chips}</ul>
      <a href="{mail}" class="zx-btn" {apply_attrs}>Apply now</a>
    </header>
    <div class="bp-layout">
      <article class="bp-article" id="bp-article">
        {article}
      </article>
      <aside class="bp-rail">
        <dl class="cd-facts">{facts_html}</dl>
        <nav class="bp-toc" aria-label="On this page"><h2>On this page</h2><ol>{toc}</ol></nav>
        <div class="bp-cta"><h2>Ready to <em>apply?</em></h2><p>Attach your CV and tell us what you would bring to the team.</p>
          <a href="{mail}" class="zx-btn" {apply_attrs}>Apply now</a></div>
      </aside>
    </div>
    <section class="co-sec jb-more" aria-labelledby="jb-more-title">
      {B.head_block('More openings', 'Other <em>open roles</em>', '', sid='jb-more-title')}
      <div class="ca-pos"><div class="ca-dept is-open"><div class="ca-dept-panel"><ul>{more}</ul></div></div></div>
      <div class="co-more"><a href="careers.html#open-roles" class="btn-contact btn-contact--xl">All open positions {B.ARROW_R}</a></div>
    </section>
'''
    B.write(f"job-{j['slug']}", f"{j['title']} — Careers at SquareZix", f"{j['title']} at SquareZix in {j['city']}: {j['overview']}", 'insights', out)


def main():
    for j in JOBS:
        page(j)


if __name__ == '__main__':
    main()
