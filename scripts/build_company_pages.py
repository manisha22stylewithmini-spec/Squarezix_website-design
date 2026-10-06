#!/usr/bin/env python3
"""Builds the company pages: culture.html, careers.html, portfolio.html, blogs.html.

The shell (head, header, contact form, footer, scripts) is lifted from about-us.html so the pages
stay in step with it; each page supplies its own sections. Styles live in company.css, behaviour
in company.js (filters, open-positions component, newsletter form, reel hover).

Copy that is NOT taken from squarezix.com is tracked in WRITTEN so it can be cleared later.
Run:  python3 scripts/build_company_pages.py
"""
import json
import re
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ABOUT = (ROOT / 'about-us.html').read_text()
VER = '20261023a'

# Pages / sections whose copy Claude wrote (no live squarezix.com content for them)
WRITTEN = {
    'culture.html': 'all copy except the Life-at-SquareZix line and the learning/recognition facts taken from the live Careers page',
    'careers.html': 'Why SquareZix card text, hiring-process steps, FAQ answers',
    'portfolio.html': 'hero, filter labels, FAQ; project descriptions reuse the home page work cards',
    'blogs.html': 'hero, topic grouping, industry picks, newsletter copy',
}

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'
ARROW_R = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHEV = '<i class="ss-q-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></i>'

# 24x24 stroke icons
IC = {
    'people': '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.4"/><path d="M16 14.2c2.6.2 5 2.3 5 5.3"/>',
    'chat': '<path d="M21 12a8 8 0 0 1-11.7 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/><path d="M8.5 11h7M8.5 14h4"/>',
    'flag': '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
    'flask': '<path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2.2h12.4a1.5 1.5 0 0 0 1.3-2.2L14 9V3"/><path d="M7.5 15h9"/>',
    'book': '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21.5v-16Z"/><path d="M8 7h8"/>',
    'signal': '<path d="M4 14v-4M8 17V7M12 20V4M16 17V7M20 14v-4"/>',
    'spark': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>',
    'rocket': '<path d="M5 15c-1.5 1.5-2 3.5-2 5 1.5 0 3.5-.5 5-2"/><path d="M12 15 9 12c1-3.5 4-7 11-8 0 7-3.5 10-8 11Z"/><circle cx="15" cy="9" r="1.4"/>',
    'heart': '<path d="M12 20s-7.5-4.4-7.5-10A4.3 4.3 0 0 1 12 7.4 4.3 4.3 0 0 1 19.5 10c0 5.6-7.5 10-7.5 10Z"/>',
    'shield': '<path d="M12 3 4 6v6c0 4.4 3.4 8.2 8 9 4.6-.8 8-4.6 8-9V6l-8-3Z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    'cal': '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    'cert': '<circle cx="12" cy="9" r="5"/><path d="m9 13.5-1.5 7 4.5-2.5 4.5 2.5-1.5-7"/>',
    'star': '<path d="m12 3 2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.5 6.6 19.5l1.2-6L3.3 9.3l6.1-.7L12 3Z"/>',
    'cash': '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/><path d="M6.5 9.5v.01M17.5 14.5v.01"/>',
    'gift': '<rect x="3.5" y="8" width="17" height="4" rx="1"/><path d="M5 12v8h14v-8M12 8v12M12 8c-2.5 0-4-1-4-2.5S9.5 3 12 8c2.5-5 4-4.5 4-2.5S14.5 8 12 8Z"/>',
    'compass': '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5 5-2Z"/>',
    'layers': '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/>',
    'bulb': '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.4 1 1.1 1 1.8V16h5v-.3c0-.7.4-1.4 1-1.8A6 6 0 0 0 12 3Z"/>',
    'camera': '<path d="M4 8h3l1.5-2h7L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1Z"/><circle cx="12" cy="13" r="3.5"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    'pin': '<path d="M12 21s-7-6.1-7-11.5a7 7 0 0 1 14 0C19 14.9 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
}


def ic(name, cls='co-ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC[name]}</svg>'


# ---------------------------------------------------------------- shell pieces lifted from about-us.html
def _between(src, start, end, include_end=True):
    a = src.index(start)
    b = src.index(end, a) + (len(end) if include_end else 0)
    return src[a:b]


HEAD_TOP = ABOUT[: ABOUT.index('<main id="about">')]
CONTACT = _between(ABOUT, '<section class="ab-contact"', '</section>')
TAIL = ABOUT[ABOUT.index('  </main>'):]


def shell(slug, title, desc, nav, body):
    head = HEAD_TOP
    head = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', head, flags=re.S)
    head = re.sub(r'<meta name="description" content=".*?" />', f'<meta name="description" content="{e(desc, quote=True)}" />', head, flags=re.S)
    head = re.sub(r'(<link rel="stylesheet" href="about\.css\?v=)\w+', rf'\g<1>{VER}', head)
    head = head.replace('<link rel="stylesheet" href="service-static.css?v=20261009a" />',
                        f'<link rel="stylesheet" href="service-static.css?v=20261009a" />\n  <link rel="stylesheet" href="company.css?v={VER}" />')
    head = head.replace('nav-item is-current', 'nav-item')
    head = head.replace(f'<div class="nav-item" data-menu="{nav}">', f'<div class="nav-item is-current" data-menu="{nav}">')
    tail = TAIL
    tail = re.sub(r'about\.js\?v=\w+', f'about.js?v={VER}', tail)
    tail = tail.replace('  <script src="about.js', f'  <script src="faq.js?v=20261009a"></script>\n  <script src="company.js?v={VER}"></script>\n  <script src="about.js', 1)
    return f'{head}<main id="about" class="ss co-page co-{slug}">\n{body}\n    {CONTACT}\n\n{tail}'


def hero(badge, h1, lead, cta_label, cta_href, aside=''):
    return f'''    <section class="svh" aria-labelledby="svp-hero-title">
      <canvas class="svh-waves" aria-hidden="true"></canvas>
      <div class="svh-inner">
        <span class="svc-badge ab-badge" data-rise>{e(badge)}</span>
        <h1 id="svp-hero-title" class="svh-title" data-rise>{h1}</h1>
        <p class="svh-lead" data-rise>{lead}</p>
        <a href="{cta_href}" class="btn-contact btn-contact--xl svh-cta" data-rise>{cta_label} {ARROW_R}</a>{aside}
      </div>
    </section>
'''


def head_block(badge, title, sub='', center=True, sid=None):
    idattr = f' id="{sid}"' if sid else ''
    s = f'<p class="co-sub" data-rise>{sub}</p>' if sub else ''
    return (f'<div class="co-head{" co-head--center" if center else ""}"><span class="svc-badge" data-rise>{e(badge)}</span>'
            f'<h2{idattr} class="ab-h2 ab-reveal" data-reveal>{title}</h2>{s}</div>')


def cta_panel(title, text, label, href, secondary=''):
    return f'''    <section class="co-sec co-cta-sec">
      <div class="co-cta" data-rise>
        <h2 class="ab-h2">{title}</h2>
        <p>{text}</p>
        <div class="co-cta-actions"><a href="{href}" class="btn-contact btn-contact--xl">{label} {ARROW_R}</a>{secondary}</div>
      </div>
    </section>
'''


def faq_band(title, sub, items):
    qs = ''.join(
        f'<details class="ss-q"{" open" if i == 0 else ""}><summary><span>{q}</span>{CHEV}</summary>'
        f'<div class="ss-a"><div class="ss-a-in"><p>{a}</p></div></div></details>'
        for i, (q, a) in enumerate(items))
    phone = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.18 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.1 9.9a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/><path d="M15 2.5a6 6 0 0 1 6.5 6.5M15 6a2.5 2.5 0 0 1 3 3"/></svg>'
    return f'''
    <div class="ss-faq-band">
      <section class="ss-sec ss-faq">
        <div class="ss-faq-head"><span class="svc-badge">FAQs</span><h2 class="ab-h2">{title}</h2><p class="ss-sub">{sub}</p></div>
        <div class="ss-faq-frame"><div class="ss-faq-list">{qs}</div></div>
        <a href="#ab-contact" class="btn-contact ss-faq-more">{phone} Still have questions? Ask us</a>
      </section>
    </div>
'''


def write(slug, title, desc, nav, body):
    (ROOT / f'{slug}.html').write_text(shell(slug.split('-')[0] if False else slug, title, desc, nav, body))
    print('wrote', f'{slug}.html')


# ================================================================ CULTURE
# Real photography slots: set a path here to swap the designed tile for a photo.
PHOTOS = {k: None for k in ('team', 'workshop', 'celebrate', 'events', 'office', 'behind')}


INIT = {'Strategy': 'St', 'Design': 'De', 'Development': 'Dv', 'Marketing': 'Mk', 'Content': 'Co', 'Client success': 'Cs'}


def culture():
    feel = [('Curious.', 'We keep learning.'), ('Collaborative.', 'We build together.'),
            ('Accountable.', 'We own the outcome.'), ('Ambitious.', 'We don’t settle for good enough.')]
    feel_html = ''.join(
        f'<li class="cu-word" data-rise><span class="cu-no">0{i+1}</span><strong>{w}</strong><span class="cu-line">{l}</span>'
        f'<i class="cu-bar" aria-hidden="true"></i></li>' for i, (w, l) in enumerate(feel))

    practices = [
        ('people', 'Collaboration', 'Strategists, designers, developers and marketers work from one brief — no hand-offs over a wall.'),
        ('chat', 'Feedback', 'Direct, kind and early. We critique the work, never the person, and we do it before it gets expensive.'),
        ('flag', 'Ownership', 'Own campaigns end to end. People are trusted with the outcome, not just the task.'),
        ('flask', 'Experimentation', 'Small bets, fast learning. We test, measure and keep what works — no loyalty to a first idea.'),
        ('book', 'Learning', 'Time and support to keep growing, including Google, Meta and HubSpot certifications.'),
        ('signal', 'Communication', 'Clear briefs, honest updates and no surprises, whether the news is good or not.'),
    ]
    prac_html = ''.join(
        f'<li class="cu-card" data-rise><span class="cu-card-ic">{ic(i)}</span><h3>{t}</h3><p>{d}</p></li>' for i, t, d in practices)

    tiles = [('team', 'Team sessions', 'people', 'a'), ('workshop', 'Workshops', 'layers', 'b'), ('celebrate', 'Celebrations', 'star', 'c'),
             ('events', 'Events', 'compass', 'd'), ('office', 'Office', 'pin', 'e'), ('behind', 'Behind the scenes', 'camera', 'f')]
    tiles_html = ''
    for key, label, icon, area in tiles:
        img = PHOTOS.get(key)
        media = f'<img src="{img}" alt="{label} at SquareZix" loading="lazy" />' if img else f'<span class="cu-art" aria-hidden="true">{ic(icon, "cu-art-ic")}</span>'
        tiles_html += f'<figure class="cu-tile cu-tile--{area}{"" if img else " is-art"}" data-rise>{media}<figcaption><span>{label}</span></figcaption></figure>'

    roles = [('Strategy', 'Research, positioning and the plan every project starts from.'),
             ('Design', 'Brand, UX and UI — from first sketch to finished system.'),
             ('Development', 'Websites and platforms built for speed, structure and search.'),
             ('Marketing', 'Search, social and paid media tied to measurable growth.'),
             ('Content', 'Words, video and assets that earn attention and trust.'),
             ('Client success', 'One point of contact who keeps every project moving.')]
    ppl_html = ''.join(
        f'<li class="cu-person" data-rise><span class="cu-avatar" aria-hidden="true"><b>{INIT[r]}</b></span><h3>{r}</h3><p>{d}</p></li>' for r, d in roles)

    grow = [('compass', 'Long-term career paths', 'We invest in people we want to grow with — from Executive to Strategist to Head of Growth, your next role already has a name here.'),
            ('cert', 'Learning & certification', 'Support for Google, Meta and HubSpot certifications, plus time to practise on real campaigns.'),
            ('rocket', 'Progress on contribution', 'We hire on talent, not titles — and move people up based on results, not tenure.')]
    grow_html = ''.join(
        f'<li class="cu-step" data-rise><span class="cu-step-dot">{ic(i)}</span><h3>{t}</h3><p>{d}</p></li>' for i, t, d in grow)

    faq = [
        ('Do I have to work from the office?', 'We are a Dubai team that meets in person for strategy huddles, workshops and team dinners. Where a role allows it, we are flexible and remote-friendly across the region — the open-role description will say what applies.'),
        ('How do you support learning and development?', 'We support Google, Meta and HubSpot certifications and give people real campaigns to practise on, with feedback from the people doing the work every day.'),
        ('How does career progression work?', 'We back talent over titles. Progression follows contribution and results, with long-term paths such as Executive → Strategist → Head of Growth.'),
        ('What perks and benefits do you offer?', 'Creative and strategic freedom, fast-track growth, certification support, peer recognition, flexible paid time off, performance-based incentives, a bonus programme and healthcare coverage in line with UAE law.'),
        ('How do I join the team?', 'Visit our Careers page for open roles. If nothing matches today, send an application anyway — we read every one and move fast on those that show real performance thinking.'),
    ]

    body = hero('Our Culture', 'Good work starts with <em>good people.</em>',
                'A close-knit Dubai team of strategists, designers, developers and marketers who like hard problems, honest feedback and doing the work properly.',
                'Explore careers', 'careers.html')
    body += f'''
    <section class="co-sec cu-feel" aria-labelledby="cu-feel-title">
      {head_block('What It Feels Like Here', 'Four words that <em>describe us</em>', '', sid='cu-feel-title')}
      <ol class="cu-words">{feel_html}</ol>
    </section>

    <section class="co-sec" aria-labelledby="cu-how-title">
      {head_block('How We Work Together', 'Habits that make the <em>work better</em>', 'The everyday practices behind every project we ship.', sid='cu-how-title')}
      <ul class="cu-cards">{prac_html}</ul>
    </section>

    <section class="co-sec" aria-labelledby="cu-life-title">
      {head_block('Life at SquareZix', 'Strategy huddles, team dinners and <em>everything in between</em>', 'The kind of camaraderie that makes Monday mornings less painful.', sid='cu-life-title')}
      <div class="cu-mosaic">{tiles_html}</div>
    </section>

    <section class="co-sec" aria-labelledby="cu-ppl-title">
      {head_block('People', 'The people behind <em>SquareZix</em>', 'Behind every system is a team of people who care about making it better.', sid='cu-ppl-title')}
      <ul class="cu-people">{ppl_html}</ul>
      <div class="co-more" data-rise><a href="about-us.html" class="co-link">Meet the people behind SquareZix {ARROW_R}</a></div>
    </section>

    <section class="co-sec" aria-labelledby="cu-grow-title">
      {head_block('Growth', 'We invest in people who <em>want to grow</em>', '', sid='cu-grow-title')}
      <ol class="cu-steps">{grow_html}</ol>
    </section>
'''
    body += cta_panel('Think you’d <em>fit in?</em>', 'See open roles, how we hire and what you can expect from us.', 'Explore Careers', 'careers.html')
    body += faq_band('Questions about <em>working here?</em>', 'Everything people ask us before they join the team.', faq)
    write('culture', 'Our Culture — Life at SquareZix | Dubai Digital Agency Team',
          'Good work starts with good people. See what it feels like to work at SquareZix, how we work together and how we help people grow.', 'insights', body)


if __name__ == '__main__':
    culture()
