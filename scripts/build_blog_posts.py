#!/usr/bin/env python3
"""Blog detail pages: one blog-<live slug>.html per article in blog_raw.py (live squarezix.com article text, frozen).

Layout: article header (breadcrumb, category, title, byline), featured image, article body + sticky side rail
(contents, share, speak-to-an-expert), related articles on the existing listing cards, then the shared contact section.
Run via build_company_pages.py (it calls main()) or directly: python3 scripts/build_blog_posts.py
"""
import re
import sys
from html import escape as e
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_company_pages as B
from blog_raw import RAW

ROOT = B.ROOT
LOCAL_SLUGS = {v['slug'] for v in RAW.values()}


def _local_links(html):
    """Point links to squarezix.com pages we have built (or blog articles we ported) at the local file."""
    def rep(m):
        slug_ = m.group(1)
        if slug_ in LOCAL_SLUGS:
            return f'href="blog-{slug_}.html"'
        if (ROOT / f'{slug_}.html').exists():
            return f'href="{slug_}.html"'
        return m.group(0)
    return re.sub(r'href="https?://(?:www\.)?squarezix\.com/([a-z0-9-]+)/?"', rep, html)


def _prepare(body):
    body = re.sub(r'(?:<p>)?\s*CONTENT END\s*\d*\s*(?:</p>)?', '', body)
    body = _local_links(body)
    # id + toc from h2s
    toc, n = [], 0

    def h2(m):
        nonlocal n
        n += 1
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        toc.append((f'sec-{n}', text))
        return f'<h2 id="sec-{n}">{m.group(1)}</h2>'
    body = re.sub(r'<h2[^>]*>(.*?)</h2>', h2, body, flags=re.S)
    # external links open in a new tab
    body = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', body)
    body = body.replace('<table', '<div class="bp-table"><table').replace('</table>', '</table></div>')
    return body, toc


def page(title, r):
    meta = next((p for p in B.POSTS if p['t'] == title), {})
    cat = meta.get('c', 'Blog')
    body, toc = _prepare(r['body'])
    fname = f"blog-{r['slug']}"
    toc_html = ''.join(f'<li><a href="#{i}">{e(t)}</a></li>' for i, t in toc[:14])
    toc_block = (f'<nav class="bp-toc" aria-label="On this page"><h2>On this page</h2><ol>{toc_html}</ol></nav>' if toc else '')
    rel_pool = [p for p in B.POSTS if p['t'] != title and p['t'] in RAW]
    rel = [p for p in rel_pool if p['topic'] == meta.get('topic')][:3]
    rel += [p for p in rel_pool if p not in rel][: 3 - len(rel)]
    rel_html = '\n          '.join(B.blog_card({**p, 'img': RAW[p['t']]['img'], 'alt': ''}, i) for i, p in enumerate(rel))
    img = (f'<figure class="bp-hero-img" data-rise><img src="{r["img"]}" alt="{e(r["h1"], quote=True)}" /></figure>' if r.get('img') else '')
    url = f'https://squarezix-website.vercel.app/{fname}.html'
    share = (f'<div class="bp-share"><h2>Share</h2><div class="bp-share-row">'
             f'<a href="https://www.linkedin.com/sharing/share-offsite/?url={url}" target="_blank" rel="noopener" aria-label="Share on LinkedIn">{B.ic("people")}</a>'
             f'<a href="https://wa.me/?text={e(r["h1"], quote=True)}%20{url}" target="_blank" rel="noopener" aria-label="Share on WhatsApp">{B.ic("chat")}</a>'
             f'<a href="mailto:?subject={e(r["h1"], quote=True)}&amp;body={url}" aria-label="Share by email">{B.ic("mail")}</a>'
             f'<button type="button" data-copy-link aria-label="Copy link">{B.ic("layers")}</button></div></div>')
    out = f'''    <div class="bp-progress" aria-hidden="true"><i></i></div>
    <header class="bp-head">
      <nav class="bp-crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i><a href="blogs.html">Blogs</a><i>/</i><span>{e(cat)}</span></nav>
      <span class="svc-badge" data-rise>{e(cat)}</span>
      <h1 class="bp-title" data-rise>{e(r['h1'])}</h1>
      <div class="bl-byline bp-byline" data-rise><span>By Squarezix Team</span><i></i><time datetime="{r['iso']}">{e(r['date'])}</time><i></i><span class="bl-read">{B.CLOCK}{e(r['read'])}</span></div>
    </header>
    {img}
    <div class="bp-layout">
      <article class="bp-article" id="bp-article">
{body}
      </article>
      <aside class="bp-rail">
        {toc_block}
        <div class="bp-cta"><h2>Speak to an <em>expert</em></h2><p>Talk to the team behind these articles about your website, brand or search visibility.</p>
          <a href="#ab-contact" class="zx-btn" data-contact-open>Contact us</a></div>
        {share}
      </aside>
    </div>
    <section class="co-sec bp-related" aria-labelledby="bp-rel-title">
      {B.head_block('Keep reading', 'More from <em>our insights</em>', '', sid='bp-rel-title')}
      <div class="bl-grid bp-rel-grid">
          {rel_html}
      </div>
      <div class="co-more"><a href="blogs.html" class="btn-contact btn-contact--xl">All articles {B.ARROW_R}</a></div>
    </section>
'''
    desc = r['desc'] or r['h1']
    B.write(fname, f"{r['h1']} | SquareZix", desc, 'insights', out)


def main():
    for title, r in RAW.items():
        page(title, r)


if __name__ == '__main__':
    main()
