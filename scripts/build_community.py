#!/usr/bin/env python3
"""Community Hub page (community-hub.html): live squarezix.com/community-hub/ wording and all 181 FAQs (community_raw.py),
laid out on the existing hero, chip filter and FAQ components, with a search box and load-more.
Run via build_company_pages.py (it calls main())."""
import sys
from html import escape as e
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_company_pages as B
from community_raw import CATS, ITEMS

SHOW = 12  # items shown before "Load more"


def main():
    counts = {k: sum(1 for i in ITEMS if i['cat'] == k) for k, _ in CATS}
    chips = ''.join(
        f'<button type="button" class="co-chip{" is-on" if k == "all" else ""}" data-cat="{k}" aria-pressed="{str(k == "all").lower()}">'
        f'{e(label)}<sup>{len(ITEMS) if k == "all" else counts[k]}</sup></button>' for k, label in CATS if k == 'all' or counts.get(k))
    labels = dict(CATS)
    qs = ''.join(
        f'<details class="ss-q" data-cat="{i["cat"]}" data-n="{n}"><summary><span>{e(i["q"])}</span>{B.CHEV}</summary>'
        f'<div class="ss-a"><div class="ss-a-in">{i["a"]}</div></div></details>' for n, i in enumerate(ITEMS))
    body = B.hero('Community Hub', 'The <em>Squarezix Community Hub</em> for AI, SEO &amp; Business Growth',
                  'Explore expert articles, practical guides, frequently asked questions, industry updates, and digital marketing insights designed to help businesses grow in the AI era. Learn everything from SEO and GEO to web development, branding, and online marketing—all in one place.',
                  'Speak to an Expert', '#ab-contact')
    body += f'''
    <section class="co-sec ch-sec" id="hub" aria-label="Community Hub questions and answers">
      <div class="ch-tools" data-rise>
        <label class="ch-search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
          <input type="search" id="ch-search" placeholder="Search {len(ITEMS)} questions" aria-label="Search questions" /></label>
        <div class="co-chips ch-chips" id="ch-chips" role="group" aria-label="Filter by topic">{chips}</div>
        <p class="ch-count" id="ch-count" aria-live="polite"></p>
      </div>
      <div class="ss-faq-band ch-band"><section class="ss-sec ss-faq">
        <div class="ss-faq-frame"><div class="ss-faq-list" id="ch-list" data-show="{SHOW}">{qs}</div></div>
        <p class="bl-nomatch" id="ch-none" hidden>No questions match. <button type="button" class="co-link" id="ch-reset">Reset filters</button></p>
        <div class="co-more"><button type="button" class="btn-contact btn-contact--xl" id="ch-more">Load more questions {B.ARROW_R}</button></div>
      </section></div>
    </section>
'''
    body += B.cta_panel('Still have <em>a question?</em>', 'Our team is here to help you find the right solution for your business.', 'Speak to an Expert', '#ab-contact')
    B.write('community-hub', 'Community Hub — SquareZix for AI, SEO & Business Growth',
            'Explore expert articles, practical guides, frequently asked questions, industry updates, and digital marketing insights designed to help businesses grow in the AI era.',
            'insights', body)


if __name__ == '__main__':
    main()
