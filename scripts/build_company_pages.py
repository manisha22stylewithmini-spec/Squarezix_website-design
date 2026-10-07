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
VER = '20261054b'

# Pages / sections whose copy Claude wrote (no live squarezix.com content for them)
WRITTEN = {
    'culture.html': 'all copy except the Life-at-SquareZix line and the learning/recognition facts taken from the live Careers page',
    'careers.html': 'Why SquareZix card text, hiring-process steps, FAQ answers',
    'portfolio.html': 'hero, FAQ, the four folder titles/descriptions/stickers in What We Make, the five reel descriptions, and the Capability/Industry/Outcome classification of each project (outcomes are goals taken from the home-page case-study challenges, no figures); website blurbs reuse the home page work cards',
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
    # about-us.html's service-static.css version changes with every style edit, so match any version
    head, n = re.subn(r'(<link rel="stylesheet" href="service-static\.css\?v=\w+" />)', rf'\1\n  <link rel="stylesheet" href="company.css?v={VER}" />', head)
    assert n == 1, 'service-static.css link not found in the about-us.html shell; company.css would be missing'
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

    <!-- Looping services strip, same as the home page (site.js clones the group and loops it) -->
    <div class="marquee" aria-label="Our services">
      <div class="marquee-track" id="marquee-track">
        <ul class="marquee-group">
          <li>AI Search Visibility</li><li>Web Design &amp; Development</li><li>SEO &amp; Growth</li><li>Branding &amp; Strategy</li><li>Social Media Marketing</li>
        </ul>
      </div>
    </div>
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


FB_CHEV = '<svg class="co-fb-chev" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
FB_X = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>'


def filterbar(label, selects, bar_id=''):
    """Pill filter bar: one native <select> per segment plus a live 'Showing N' segment with a reset button.
    selects = [(data_key, label, all_label, [(value, text), ...])]"""
    segs = ''
    for key, lab, all_label, opts in selects:
        o = f'<option value="all">{e(all_label)}</option>' + ''.join(f'<option value="{v}">{e(t)}</option>' for v, t in opts)
        segs += f'<label class="co-fb-seg"><span class="co-fb-label">{lab}</span><select data-key="{key}" aria-label="{lab}">{o}</select>{FB_CHEV}</label>'
    idattr = f' id="{bar_id}"' if bar_id else ''
    return (f'<div class="co-filterbar"{idattr} role="group" aria-label="{e(label)}" data-rise>{segs}'
            f'<div class="co-fb-seg co-fb-count"><span class="co-fb-label">Showing</span><output class="co-fb-out" aria-live="polite"></output>'
            f'<button type="button" class="co-fb-reset" hidden aria-label="Reset filters">{FB_X}</button></div></div>')


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


# ================================================================ CAREERS
def careers():
    why = [('Work', 'Work across B2B, ecommerce and regional brands, on campaigns that move real numbers.'),
           ('Growth', 'Build skills on meaningful projects, with a team that treats performance data as a craft, not a checkbox.'),
           ('Ownership', 'Own campaigns end to end instead of waiting for permission.'),
           ('Progression', 'Move up on contribution and capability — we back talent, not titles.')]
    why_html = ''.join(
        f'<li class="ca-why-card" data-rise><span class="ca-why-no">0{i+1}</span><h3><em>Real</em> {w}</h3><p>{d}</p><i class="ca-why-glow" aria-hidden="true"></i></li>'
        for i, (w, d) in enumerate(why))

    tiles_html = ''.join(
        f'<figure class="cu-tile is-art" data-rise><span class="cu-art" aria-hidden="true">{ic(icn, "cu-art-ic")}</span><figcaption><span>{lab}</span></figcaption></figure>'
        for lab, icn in (('Team sessions', 'people'), ('Workshops', 'layers'), ('Celebrations', 'star')))

    benefits = [('compass', 'Creative & strategic freedom', 'Own campaigns end to end.'),
                ('rocket', 'Fast-track career growth', 'Move up based on results.'),
                ('cert', 'Learning & certification support', 'Google, Meta and HubSpot certifications.'),
                ('star', 'Peer recognition', 'Be celebrated for your wins.'),
                ('cal', 'Flexible time off', 'Paid time off that respects your time.'),
                ('cash', 'Performance incentives', 'Uncapped bonuses tied to results.'),
                ('gift', 'Bonus programme', 'Bring talent in and get rewarded.'),
                ('shield', 'Healthcare coverage', 'Comprehensive medical insurance in line with UAE law.')]
    ben_html = ''.join(
        f'<li class="ca-ben" data-rise><span class="ca-ben-ic">{ic(i)}</span><div><h3>{e(t)}</h3><p>{d}</p></div></li>' for i, t, d in benefits)

    steps = [('Apply', 'Send your CV and, where you can, work you’re proud of. We read every application.'),
             ('Meet', 'A relaxed first conversation about you, your work and what you want to do next.'),
             ('Discuss', 'Go deeper with the people you’d work with — craft, ownership and how we run projects.'),
             ('Build together', 'An offer, an onboarding plan and a first real project to get your hands on.')]
    steps_html = ''.join(
        f'<li class="ca-step" data-rise><span class="ca-step-no">0{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(steps))

    mail = 'mailto:info@squarezix.com?subject=Application%20%E2%80%94%20SquareZix'
    faq = [
        ('Which teams are you hiring for?', 'We hire across performance marketing, creative and strategy. Open roles are listed above whenever they are available.'),
        ('Do you only hire people based in the UAE?', 'No. We hire UAE-based talent and people open to relocating. We back people who show up with real results, not just a polished résumé.'),
        ('What does the hiring process look like?', 'Four simple steps: apply, meet, discuss and build together. We read every application and move quickly on the ones that show real performance thinking.'),
        ('Can I apply if there is no open position for me?', 'Yes. Send us an application with your CV and a few lines on what you would bring. We are always interested in meeting people who can add something meaningful.'),
        ('What benefits do you offer?', 'Creative and strategic freedom, fast-track career growth, certification support, peer recognition, flexible paid time off, performance-based incentives, a bonus programme and healthcare coverage in line with UAE law.'),
        ('Do you support certifications and learning?', 'Yes — we support Google, Meta and HubSpot certifications and give you real campaigns to practise on.'),
    ]

    body = hero('Careers', 'Build what’s next. <em>With us.</em>',
                'Join a team where strategy, creativity, technology and growth come together.',
                'View open roles', '#open-roles')
    body += f'''
    <section class="co-sec" aria-labelledby="ca-why-title">
      {head_block('Why SquareZix?', 'Four reasons people <em>stay and grow</em>', 'We hire on talent, not titles — and give people the room to prove it.', sid='ca-why-title')}
      <ul class="ca-why">{why_html}</ul>
    </section>

    <section class="co-sec ca-life" aria-labelledby="ca-life-title">
      <div class="ca-life-copy">
        {head_block('Life at SquareZix', 'Culture is <em>who we are.</em> Careers is why you should join.', 'Strategy huddles, team dinners and the kind of camaraderie that makes Monday mornings less painful.', center=False, sid='ca-life-title')}
        <div class="ca-life-link" data-rise><a href="culture.html" class="co-link">Explore our culture {ARROW_R}</a></div>
      </div>
      <div class="ca-tiles">{tiles_html}</div>
    </section>

    <section class="co-sec" aria-labelledby="ca-ben-title">
      {head_block('Perks &amp; Benefits', 'Looked after, <em>properly</em>', '', sid='ca-ben-title')}
      <ul class="ca-bens">{ben_html}</ul>
    </section>

    <section class="co-sec" id="open-roles" aria-labelledby="ca-pos-title">
      {head_block('Open Positions', 'Open <em>positions</em>', '<span id="ca-pos-sub">We’re not hiring for a specific role right now.</span>', sid='ca-pos-title')}
      <div class="ca-pos" id="ca-pos" data-state="empty">
        <div class="ca-pos-list" hidden>
          <div class="ca-pos-filters" role="group" aria-label="Filter roles by team"></div>
          <ul class="ca-pos-items"></ul>
        </div>
        <div class="ca-pos-empty" data-rise>
          <span class="ca-pos-ic">{ic('mail')}</span>
          <h3>No current openings.</h3>
          <p>Don’t see your role? We’re always interested in meeting people who can add something meaningful.</p>
          <a href="{mail}" class="btn-contact btn-contact--xl">Send an Application {ARROW_R}</a>
        </div>
      </div>
      <!-- Add roles as JSON and the list replaces the empty state: [{{"title":"","team":"","location":"","type":"","href":""}}] -->
      <script type="application/json" id="ca-positions">[]</script>
    </section>

    <section class="co-sec" aria-labelledby="ca-proc-title">
      {head_block('Hiring Process', 'Simple on <em>purpose</em>', 'Four steps, no maze.', sid='ca-proc-title')}
      <ol class="ca-steps">{steps_html}</ol>
    </section>
'''
    body += cta_panel('Your next chapter <em>could start here.</em>', 'See which roles are open, or send us an application and tell us what you would build.', 'View Open Roles', '#open-roles')
    body += faq_band('Questions before you <em>apply?</em>', 'What people ask us about working at SquareZix.', faq)
    write('careers', 'Careers at SquareZix — Build What’s Next | Dubai Digital Agency',
          'Join a team where strategy, creativity, technology and growth come together. Real work, real growth, real ownership and real progression at SquareZix in Dubai.', 'insights', body)


# ================================================================ PORTFOLIO
def portfolio():
    # Real projects (home page case studies) and the five social reels already in assets/
    sites = [
        dict(key='ds', client='Digital Stream', industry='B2B SaaS', cap='Positioning · UX/UI · Development · SEO', cat='digital',
             img='assets/work/project-1.png', alt='Digital Stream website', year='2025',
             blurb='A product story rewritten around one outcome, with every page leading to a demo.'),
        dict(key='hg', client='Hero Gradients', industry='Digital goods e-commerce', cap='UX/UI · Headless build · CRO', cat='digital',
             img='assets/work/project-2.png', alt='Hero Gradients storefront', year='2025',
             blurb='A headless storefront with checkout cut from five screens to two.'),
        dict(key='ls', client='Lissr.ai', industry='AI SaaS', cap='Product design · Design system · AI integration', cat='digital',
             img='assets/work/project-3.png', alt='Lissr.ai product site and dashboard', year='2024',
             blurb='Onboarding and a dashboard redesigned around a single first task.'),
    ]
    reels = [
        dict(n=1, title='Digital Marketing', cap='Social video · Motion'),
        dict(n=3, title='Strategy without content is invisible', cap='Social video · Motion'),
        dict(n=4, title='Struggling to justify your rates?', cap='Social video · Motion'),
        dict(n=2, title='Kinetic type reel', cap='Social video · Motion'),
        dict(n=5, title='Solution Wagon', cap='Social video · Motion'),
    ]
    CAT = {'digital': 'Digital Experience', 'marketing': 'Digital Marketing'}

    def feat(s, i, wide):
        return f'''<a class="pf-feat{" pf-feat--wide" if wide else ""}" href="case-study.html" data-rise>
          <div class="pf-feat-media"><img src="{s['img']}" alt="{s['alt']}" loading="lazy" /></div>
          <div class="pf-feat-body">
            <span class="pf-no">0{i+1}</span>
            <h3>{s['client']}</h3>
            <p class="pf-feat-blurb">{s['blurb']}</p>
            <ul class="pf-chain"><li>{s['client']}</li><li>{s['industry']}</li><li>{s['cap']}</li></ul>
          </div>
          <span class="pf-arrow" aria-hidden="true">{ARROW}</span>
        </a>'''
    feat_html = feat(sites[0], 0, True) + feat(sites[1], 1, False) + feat(sites[2], 2, False)

    def web_tile(s, size):
        return f'''<a class="pf-tile pf-tile--{size}" href="case-study.html" data-cat="{s['cat']}" data-rise>
          <div class="pf-tile-media"><img src="{s['img']}" alt="{s['alt']}" loading="lazy" /></div>
          <div class="pf-tile-body"><span class="pf-tag">{CAT[s['cat']]}</span><h3>{s['client']}</h3>
            <p class="pf-tile-chain"><span>{s['industry']}</span><span>{s['cap'].split(' · ')[0]}</span></p></div>
          <span class="pf-arrow" aria-hidden="true">{ARROW}</span>
        </a>'''

    def reel_tile(r, size):
        n = r['n']
        return f'''<a class="pf-tile pf-tile--{size} pf-tile--reel" href="index.html#reels" data-cat="marketing" aria-label="{r['title']} — social reel" data-rise>
          <div class="pf-tile-media"><img src="assets/reels/reel-{n}.jpg" alt="" loading="lazy" /><video src="assets/reels/reel-{n}.mp4" poster="assets/reels/reel-{n}.jpg" muted loop playsinline preload="none"></video></div>
          <div class="pf-tile-body"><span class="pf-tag">{CAT['marketing']}</span><h3>{r['title']}</h3>
            <p class="pf-tile-chain"><span>Social reel</span><span>Motion</span></p></div>
          <span class="pf-play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5.5v13l11-6.5-11-6.5Z"/></svg></span>
        </a>'''

    grid = [web_tile(sites[0], 'l'), reel_tile(reels[0], 's'), reel_tile(reels[1], 's'), web_tile(sites[1], 'l'),
            web_tile(sites[2], 'full'), reel_tile(reels[2], 'xs'), reel_tile(reels[3], 'xs'), reel_tile(reels[4], 'xs')]
    grid_html = '\n          '.join(grid)

    counts = {'all': 8, 'branding': 0, 'digital': 3, 'marketing': 5, 'ai': 0}
    chips = [('all', 'All'), ('branding', 'Branding'), ('digital', 'Digital Experience'), ('marketing', 'Digital Marketing'), ('ai', 'AI / Search')]
    chips_html = ''.join(
        f'<button type="button" class="co-chip{" is-on" if k == "all" else ""}" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{lab}<sup>{counts[k]:02d}</sup></button>'
        for k, lab in chips)

    results = [(1000, '+', 'Websites delivered'), (80, '%', 'Social traffic growth for a lifestyle brand'), (7, '', 'Official platform partnerships')]
    res_html = ''.join(
        f'<div class="ab-stat-card" data-rise><div class="ab-stat-value"><strong data-count="{n}" data-suffix="{suf}">{n}{suf}</strong></div><p class="ab-stat-label">{lab}</p></div>'
        for n, suf, lab in results)

    faq = [
        ('Can I see full case studies?', 'Yes. Our case studies walk through the brief, what we did and what changed. Every project here that has a case study links straight to it.'),
        ('Do you only build websites?', 'No. Alongside websites and platforms we work on branding, UX and product design, search and AI visibility, paid media, social and content — one team, one process.'),
        ('What kind of businesses do you work with?', 'A diverse mix of B2B, e-commerce and regional brands across the UAE, the wider GCC and Asia.'),
        ('Can you work on something similar for my business?', 'Almost certainly. Book a free 30-minute strategy call and we will send a custom proposal within five days — no obligation, no hard sell.'),
        ('Why isn’t every project shown here?', 'This page is a curated selection. Some work is under NDA, and we only show results we can stand behind. Ask us for relevant examples for your industry.'),
    ]

    # "Selected portfolios" card listing, straight after the hero (design: image, title, line, Contact us)
    reel_desc = {1: 'A short-form social reel built around 3D motion graphics.',
                 3: 'Kinetic-typography reel making the case for content-led strategy.',
                 4: 'Short-form reel built around a single, direct client question.',
                 2: 'Kinetic-typography social reel with bold, minimal type.',
                 5: 'Branded social reel for Solution Wagon.'}
    PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.18 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.1 9.9a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/><path d="M15 2.5a6 6 0 0 1 6.5 6.5M15 6a2.5 2.5 0 0 1 3 3"/></svg>'

    # Project cards as folders: photos peek out of a frosted folder, a paper-clipped tag carries the key result
    # (or the reel poster), small bubbles name the disciplines, title and line sit underneath.
    ICON_WEB = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01"/></svg>'
    ICON_REEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="m10.5 9.5 4 2.5-4 2.5z" fill="currentColor"/></svg>'
    SHORT = {'Positioning': 'Po', 'UX/UI': 'UX', 'Development': 'Dev', 'SEO': 'SEO', 'Headless build': 'HL', 'CRO': 'CRO',
             'Product design': 'PD', 'Design system': 'DS', 'AI integration': 'AI'}

    def sel_card(title, desc, img, href, pics, note, cap='', ind='none', out=''):
        pic_html = ''.join(f'<img class="pf-fc-p{i + 1}" src="{src}" alt="" loading="lazy" />' for i, src in enumerate(pics + [img]))
        big, small = note
        return (f'<article class="pf-card pf-fc" data-cap="{cap}" data-ind="{ind}" data-out="{out}" data-rise><div class="pf-fc-wrap">'
                f'<a class="pf-fc-folder" href="{href}" tabindex="-1" aria-hidden="true"><span class="pf-fc-back"></span>'
                f'<span class="pf-fc-pics">{pic_html}</span><span class="pf-fc-front"></span>'
                f'<span class="pf-fc-note"><i class="pf-fc-clip"></i><b>{e(big)}</b><small>{e(small)}</small></span></a>'
                f'<p class="pf-fc-desc">{e(desc)}</p></div>'
                f'<h3><a href="{href}">{e(title)}</a></h3></article>')

    SITE_META = [('digital', 'tech', 'leads'), ('digital', 'ecom', 'conversion'), ('digital', 'tech', 'adoption')]
    site_imgs = [s['img'] for s in sites]
    REEL_NOTE = {1: ('3D motion', 'Social reel'), 3: ('Kinetic type', 'Social reel'), 4: ('One question', 'Social reel'),
                 2: ('Bold & minimal', 'Social reel'), 5: ('Branded', 'Social reel')}

    def sel_site(i):
        x = sites[i]
        c = next(k for k in CASES if k['client'] == x['client'])
        cap, ind, out = SITE_META[i]
        others = [im for im in site_imgs if im != x['img']]
        return sel_card(x['client'], x['blurb'], x['img'], 'case-study.html', others, c['results'][0], cap=cap, ind=ind, out=out)

    def sel_reel(i):
        r = reels[i]
        poster = f"assets/reels/reel-{r['n']}.jpg"
        others = [f"assets/reels/reel-{reels[(i + k) % len(reels)]['n']}.jpg" for k in (1, 2)]
        return sel_card(r['title'], reel_desc[r['n']], poster, 'index.html#reels', others, REEL_NOTE[r['n']],
                        cap='marketing', ind='none', out='engagement')

    sel_cards = ''.join([sel_site(0), sel_reel(0), sel_site(1), sel_reel(1), sel_site(2), sel_reel(2), sel_reel(3), sel_reel(4)])

    # Folder stack: disciplines filed top to bottom, each folder peeks a slice of work and opens to the full piece
    folders = [
        dict(name='Websites & platforms', title='Sites that earn demos, not just visits.',
             desc='Marketing sites and platforms designed around one outcome, built for speed, structure and search.',
             tags=['b2b saas', 'ux/ui', 'development', 'seo'], media=['assets/work/project-1.png'], alt='Digital Stream website',
             link=('case-study.html', 'See the case study')),
        dict(name='E-commerce & storefronts', title='Storefronts with a checkout that keeps shoppers.',
             desc='Headless builds, product pages around the photography and checkouts with less friction.',
             tags=['digital goods', 'headless build', 'cro'], media=['assets/work/project-2.png'], alt='Hero Gradients storefront',
             link=('case-study.html', 'See the case study')),
        dict(name='Product & AI', title='Products people finish setting up.',
             desc='Onboarding, dashboards and design systems for AI products, designed around a single first task.',
             tags=['ai saas', 'product design', 'design system'], media=['assets/work/project-3.png'], alt='Lissr.ai product site and dashboard',
             link=('case-study.html', 'See the case study')),
        dict(name='Social & motion', title='Short-form reels that stop the scroll.',
             desc='Kinetic-typography and 3D motion reels made for social feeds.',
             tags=['social reels', 'motion', 'kinetic type'], media=['assets/reels/reel-1.jpg', 'assets/reels/reel-3.jpg', 'assets/reels/reel-4.jpg'],
             alt='Social reel posters', link=('index.html#reels', 'Watch the reels')),
    ]
    fold_html = ''
    for i, f in enumerate(folders):
        trio = len(f['media']) > 1
        imgs = ''.join(f'<img src="{m}" alt="{e(f["alt"]) if j == 0 else ""}" loading="lazy" />' for j, m in enumerate(f['media']))
        stickers = ''.join(f'<li>{t}</li>' for t in f['tags'])
        open_cls = ' is-open' if i == 0 else ''
        fold_html += (
            f'<article class="pf-folder{open_cls}" style="--i:{i}" data-rise>'
            f'<button type="button" class="pf-folder-tab" id="pf-fold-tab-{i}" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="pf-fold-{i}">'
            f'<span class="pf-tab-no">0{i+1}</span><span class="pf-tab-name">{e(f["name"])}</span><i class="pf-tab-plus" aria-hidden="true"></i></button>'
            f'<div class="pf-folder-body" id="pf-fold-{i}" role="region" aria-labelledby="pf-fold-tab-{i}"><div class="pf-folder-inner">'
            f'<div class="pf-folder-info"><h3>{e(f["title"])}</h3><p>{e(f["desc"])}</p><ul class="pf-stickers">{stickers}</ul>'
            f'<div class="pf-folder-more"><a href="{f["link"][0]}" class="co-link">{f["link"][1]} {ARROW_R}</a></div></div>'
            f'<div class="pf-folder-media{" pf-folder-media--trio" if trio else ""}">{imgs}</div>'
            f'</div></div></article>')

    body = hero('Portfolio', 'A selection of brands, experiences and <em>digital systems</em> we’ve built.',
                'Websites, products and campaigns — designed, built and grown by one team.',
                'Start a project', '#ab-contact')
    body += pk_pocket()
    body += f'''
    <section class="co-sec pf-sel" id="browse" aria-labelledby="pf-sel-title">
      {head_block('Browse Work', 'Find a project <em>like yours</em>', 'Filter by what we did, who it was for and what changed — three ways in, not fifteen.', sid='pf-sel-title')}
      <div class="pf-bar-wrap">{filterbar('Filter projects', [('cap', 'Capability', 'All Capabilities', [('digital', 'Digital Experience'), ('marketing', 'Digital Marketing')]), ('ind', 'Industry', 'All Industries', [('tech', 'Technology & Innovation'), ('ecom', 'E-commerce & Retail')]), ('out', 'Outcome', 'All Outcomes', [('leads', 'Lead generation'), ('conversion', 'Conversion'), ('adoption', 'Product adoption'), ('engagement', 'Audience engagement')])], 'pf-bar')}</div>
      <div class="pf-cards" id="pf-cards">{sel_cards}</div>
      <div class="pf-nomatch" id="pf-nomatch" hidden>
        <h3>No projects match those filters.</h3>
        <p>Try a different combination, or tell us what you need and we’ll share relevant examples.</p>
        <div class="pf-empty-actions"><button type="button" class="co-link" data-filter-reset>Reset filters</button><a href="#ab-contact" class="btn-contact btn-contact--xl">Talk to us {ARROW_R}</a></div>
      </div>
      <div class="pf-more"><a href="case-study.html#work" class="pf-more-btn">View more projects <span class="pf-more-left">Case studies</span><span aria-hidden="true">→</span></a></div>
    </section>

    <section class="co-sec" aria-labelledby="pf-res-title">
      {head_block('Selected Results', 'Real work. <em>Real outcomes.</em>', '', sid='pf-res-title')}
      <div class="pf-results">{res_html}</div>
      <p class="pf-note" data-rise>Figures come from our published company and client information. Case-study metrics are added once verified.</p>
    </section>
'''
    body += cta_panel('Let’s build something <em>worth showing.</em>', 'Tell us what you want to launch, fix or grow — we’ll come back with a plan within five days.', 'Start a Project', '#ab-contact')
    body += faq_band('Questions about <em>our work?</em>', 'What people ask before we start a project together.', faq)
    write('portfolio', 'Our Work — Portfolio of Brands, Websites & Digital Systems | SquareZix',
          'A selection of brands, experiences and digital systems built by SquareZix — websites, products and campaigns designed, built and grown by one Dubai team.', 'work', body)


# ================================================================ CASE STUDIES (bookshelf; every book opens case-study.html)
# Copy comes from the home page case-study section (challenge, what we did, services, results) and the
# five social reels already in assets/reels. Shelf colours stay inside the brand palette.
CASES = [
    dict(slug='digital-stream', client='Digital Stream', kind='Website', industry='B2B SaaS', year='2025', img='assets/work/project-1.png',
         alt='Digital Stream website', no='01',
         challenge='A strong product hidden behind a site that read like a spec sheet. Visitors left before they understood what it did.',
         did='Rewrote the story around one outcome, redesigned every page to lead to a demo, and rebuilt the front end for speed.',
         services=['Positioning', 'UX/UI', 'Development', 'SEO'],
         results=[('+212%', 'Demo requests'), ('1.1s', 'Mobile load (LCP)'), ('9 wks', 'Brief to launch')],
         book=dict(font='sora', w=78, h=94, bg='#f3e8ff', fg='#1a0b36', band='#621dd0', bh=20, title='Digital Stream')),
    dict(slug='hero-gradients', client='Hero Gradients', kind='E-commerce', industry='Digital goods', year='2025', img='assets/work/project-2.png',
         alt='Hero Gradients storefront', no='02',
         challenge='Plenty of traffic, a slow catalogue and a checkout that lost shoppers at the shipping step.',
         did='Moved the store to a headless stack, cut checkout from five screens to two and rebuilt product pages around the photography.',
         services=['UX/UI', 'Headless build', 'CRO'],
         results=[('+38%', 'Conversion rate'), ('−41%', 'Cart abandonment'), ('2.4×', 'Returning buyers')],
         book=dict(font='sora', w=96, h=93, bg='#0f0a22', fg='#e2b8ff', band='linear-gradient(90deg,#621dd0,#ab24f2)', bh=12, top=True, title='Hero Gradients')),
    dict(slug='lissr-ai', client='Lissr.ai', kind='Product & AI', industry='AI SaaS', year='2024', img='assets/work/project-3.png',
         alt='Lissr.ai product site and dashboard', no='03',
         challenge='An AI tool people signed up for and then abandoned, because the first screen asked for too much too soon.',
         did='Mapped the first ten minutes of use, redesigned onboarding around a single task and rebuilt the dashboard to match.',
         services=['Product design', 'Design system', 'AI integration'],
         results=[('3×', 'Trial to paid'), ('−57%', 'Support tickets'), ('4 min', 'To first result')],
         book=dict(font='sora', w=104, h=95, bg='linear-gradient(160deg,#7b2ff0,#ab24f2)', fg='#ffffff', tilt=-6, big=True, title='Lissr.ai')),
]
REEL_CASES = [
    dict(slug='reel-digital-marketing', n=1, title='Digital Marketing', desc='A short-form social reel built around 3D motion graphics.',
         book=dict(font='serif', w=58, h=74, bg='#ab24f2', fg='#ffffff', title='Digital Marketing')),
    dict(slug='reel-strategy-without-content', n=3, title='Strategy without content is invisible', desc='Kinetic-typography reel making the case for content-led strategy.',
         book=dict(font='mono', w=60, h=91, bg='#f7f5fb', fg='#621dd0', band='#e9d5ff', bh=9, title='Strategy without content is invisible')),
    dict(slug='reel-justify-your-rates', n=4, title='Struggling to justify your rates?', desc='Short-form reel built around a single, direct client question.',
         book=dict(font='serif', w=70, h=80, bg='#1c1233', fg='#f5f3ff', band='#ab24f2', bh=8, top=True, title='Justify your rates?')),
    dict(slug='reel-kinetic-type', n=2, title='Kinetic type reel', desc='Kinetic-typography social reel with bold, minimal type.',
         book=dict(font='sora', w=82, h=88, bg='#e9d5ff', fg='#2a0f5c', band='#3b1a74', bh=16, title='Kinetic Type')),
    dict(slug='reel-solution-wagon', n=5, title='Solution Wagon', desc='Branded social reel for Solution Wagon.',
         book=dict(font='sora', w=64, h=88, bg='#6d28d9', fg='#ffffff', title='Solution Wagon')),
]
SHELF_ORDER = ['digital-stream', 'reel-digital-marketing', 'hero-gradients', 'reel-strategy-without-content', 'lissr-ai',
               'reel-justify-your-rates', 'reel-kinetic-type', 'reel-solution-wagon']


def _case_by(slug_):
    return next(c for c in CASES + REEL_CASES if c['slug'] == slug_)


def book_html(c, current=False, href='case-study.html', i=0):
    b = c['book']
    is_site = 'client' in c
    sub = f"{c['kind']} · {c['year']}" if is_site else 'Social reel'
    if is_site:
        tip = f"<b>{e(c['client'])}</b><span>{e(c['kind'])} · {e(c['industry'])}</span><i>{e(c['results'][0][0])} {e(c['results'][0][1].lower())}</i>"
    else:
        tip = f"<b>{e(c['title'])}</b><span>Social video · Motion</span><i>Watch the reel</i>"
    style = f"--i:{i};--w:{b['w']}px;--h:{b['h']}%;--bg:{b['bg']};--fg:{b['fg']};"
    if b.get('band'):
        style += f"--band:{b['band']};--bh:{b['bh']}%;"
    if b.get('tilt'):
        style += f"--tilt:{b['tilt']}deg;"
    cls = f"bk bk--{b['font']}" + (' bk--top' if b.get('top') else '') + (' bk--big' if b.get('big') else '') + (' is-current' if current else '')
    label = f"{c['client']}: {c['kind']} case study" if is_site else f"{c['title']}: social reel"
    num = c['no'] if is_site else 'R' + str(c['n'])
    cur = ' aria-current="page"' if current else ''
    return (f'<a class="{cls}" style="{style}" href="{href}" aria-label="{e(label)}"{cur}>'
            f'<span class="bk-top" aria-hidden="true">{num}</span><span class="bk-title" aria-hidden="true">{e(b["title"])}</span>'
            f'<span class="bk-sub" aria-hidden="true">{e(sub)}</span><span class="bk-mark" aria-hidden="true">SZ</span>'
            f'<span class="bk-tip" aria-hidden="true">{tip}</span></a>')


def shelf(current=None, compact=False, href='case-study.html'):
    books = ''.join(book_html(_case_by(s), s == current, href, n) for n, s in enumerate(SHELF_ORDER))
    books += ('<a class="bk bk--mono bk--next" style="--i:8;--w:66px;--h:82%;" href="#ab-contact" aria-label="Your brand: start the next case study">'
              '<span class="bk-top" aria-hidden="true">+</span><span class="bk-title" aria-hidden="true">Your brand, next</span>'
              '<span class="bk-sub" aria-hidden="true">Vol. 09</span><span class="bk-mark" aria-hidden="true">SZ</span>'
              '<span class="bk-tip" aria-hidden="true"><b>Your brand</b><span>The next chapter on this shelf</span><i>Start a project</i></span></a>')
    sid = '' if compact else ' id="shelf"'
    return (f'    <section class="co-sec bk-sec{" bk-sec--compact" if compact else ""}"{sid} aria-label="Case study library">\n'
            f'      {head_block("Case Library", "Squarezix <em>Case Studies.</em>", "Every spine is a project. Hover to pull one off the shelf, click to open it.")}\n'
            f'      <div class="bk-shelf" data-rise>{books}</div>\n'
            f'    </section>\n')


def collab():
    """How the team builds a case study: specialists around one brief (Claude-written copy, flag it)."""
    roles = [('Brand Strategist', 'Finds the one outcome that matters'), ('UX/UI Designer', 'Shapes how it looks and flows'),
             ('Developer', 'Builds it fast and solid'), ('SEO & AI Specialist', 'Makes it findable in search and AI'),
             ('Content & Social Lead', 'Gives it a voice people share'), ('Performance Analyst', 'Measures what changed')]
    notes = roles + [('Project Lead', 'Keeps one brief, one timeline, one team')]
    papers = ['lilac', 'violet', 'mist', 'lavender', 'orchid', 'lilac', 'violet']
    tilts = [-2.2, 1.6, -1.2, 2, -1.8, 1.4, -1]
    note_html = ''.join(f'<li class="cb-note cb-note--{papers[i]}" style="--r:{tilts[i]}deg"><b>{e(r)}</b><span>{e(d)}</span></li>'
                        for i, (r, d) in enumerate(notes))
    svg = (f'<div class="cb-board" role="img" aria-label="Seven specialists on one brief: {e(", ".join(r for r, _ in notes))}">'
           f'<p class="cb-board-title">One brief <i>→ one case study</i></p><ul class="cb-notes" aria-hidden="true">{note_html}</ul></div>')
    cards = ''.join(f'<li><b>{e(r)}</b><span>{e(d)}</span></li>' for r, d in roles)
    steps = ''.join(f'<li><i>{i + 1:02d}</i>{e(t)}</li>' for i, t in enumerate(
        ['Brief & goals', 'Dig into the data', 'Form a hypothesis', 'Design · build · test', 'Measure, then write it up']))
    head = head_block('How We Work', 'Not an ordinary case study. <em>A room full of market experts.</em>',
                      'Every SquareZix case study starts with the people around the table. Strategists, designers, developers, '
                      'SEO and AI specialists and marketers who know the GCC market work on one brief together, so the result is '
                      'something people remember, not a template with a new logo.', center=False, sid='cb-title')
    return (f'    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;600;700&display=swap" />\n'
            f'    <section class="co-sec cb-sec" aria-labelledby="cb-title">\n'
            f'      <div class="cb-grid">\n        <div class="cb-copy">{head}</div>\n'
            f'        <div class="cb-visual" data-rise>{svg}</div>\n      </div>\n'
            f'      <ol class="cb-steps" data-rise aria-label="How every case study gets made">{steps}</ol>\n'
            f'    </section>\n')


# ================================================================ PORTFOLIO SHOWCASE (pocket · bento · featured work)
# Structure follows the "Wall of Portfolios" reference; colours, fonts and content are Squarezix's own.
def pk_pocket():
    """Category shelf: one pocket per kind of work. Clicking a pocket sets the Browse filters below
    (company.js) and scrolls to the matching projects; the active pocket follows the filters."""
    cats = [
        dict(name='Websites & platforms', line='Sites that earn demos, not just visits.', set='{"cap":"digital","ind":"tech","out":"leads"}',
             tone='a', pics=['assets/work/project-1.png'], note=('+212%', 'demo requests'), n=1),
        dict(name='E-commerce & storefronts', line='Storefronts with a checkout that keeps shoppers.', set='{"cap":"all","ind":"ecom","out":"all"}',
             tone='b', pics=['assets/work/project-2.png'], note=('+38%', 'conversion rate'), n=1),
        dict(name='Product & AI', line='Products people finish setting up.', set='{"cap":"all","ind":"all","out":"adoption"}',
             tone='c', pics=['assets/work/project-3.png'], note=('3×', 'trial to paid'), n=1),
        dict(name='Social & motion', line='Short-form reels that stop the scroll.', set='{"cap":"marketing","ind":"all","out":"all"}',
             tone='d', pics=['assets/reels/reel-3.jpg', 'assets/reels/reel-1.jpg'], note=('5', 'social reels'), n=5),
    ]
    head = head_block('Browse by Category', 'Pick a <em>pocket</em>',
                      'Every kind of work we do, filed in its own pocket. Open one to see the projects inside.', sid='pk-title')
    pockets = ''
    for c in cats:
        pics = ''.join(f'<img class="pk-pic pk-pic--{i + 1}{" pk-pic--tall" if "reels" in src else ""}" src="{src}" alt="" loading="lazy" />'
                       for i, src in enumerate(c['pics']))
        big, small = c['note']
        count = f'{c["n"]} project{"s" if c["n"] > 1 else ""}'
        pockets += (f"<button type=\"button\" class=\"pk-pk pk-pk--{c['tone']}\" data-set='{c['set']}' aria-pressed=\"false\" aria-controls=\"pf-cards\">"
                    f'<span class="pk-inside" aria-hidden="true"></span>'
                    f'<span class="pk-peek" aria-hidden="true">{pics}<span class="pk-note"><b>{e(big)}</b><small>{e(small)}</small></span></span>'
                    f'<span class="pk-front"><span class="pk-count">{count}</span><b class="pk-name">{e(c["name"])}</b>'
                    f'<span class="pk-line">{e(c["line"])}</span><span class="pk-go">View work {ARROW_R}</span></span></button>')
    return f'''    <section class="co-sec pk-sec" aria-labelledby="pk-title">
      {head}
      <div class="pk-shelf" data-rise>{pockets}</div>
    </section>
'''


def pk_bento():
    chips = ['Visual Design', 'UX Research', 'Development', 'SEO', 'AI Search', 'Paid Media', 'Social Media', 'Branding']
    chip_html = ''.join(f'<li style="--r:{r}deg">{e(c)}</li>' for c, r in zip(chips, (-12, 9, -4, 14, -8, 5, -14, 7)))
    head = head_block('What We Do', 'Beyond the <em>screenshots</em>', 'The disciplines behind the work, and where to read and watch more of it.', sid='pk-bento-title')
    blogs = ''.join(f'<li>{e(t)}</li>' for t in ('How AI Is Changing Search Visibility', 'Guide to Effective SEO Strategy in 2026'))
    return f'''    <section class="co-sec pk-sec" aria-labelledby="pk-bento-title">
      {head}
      <div class="pk-bento" data-rise>
        <a class="pk-tile pk-tile--sites" href="case-study.html">
          <div class="pk-polas"><figure style="--r:-7deg"><img src="assets/work/project-1.png" alt="" loading="lazy" /><figcaption>Websites</figcaption></figure><figure style="--r:5deg"><img src="assets/work/project-2.png" alt="" loading="lazy" /><figcaption>E-commerce</figcaption></figure></div>
          <h3>Websites &amp; platforms</h3><p>Marketing sites and platforms designed around one outcome, built for speed, structure and search.</p>
        </a>
        <div class="pk-tile pk-tile--skills"><h3>Capabilities</h3><p>One team across strategy, design, build and growth.</p><ul class="pk-chips">{chip_html}</ul></div>
        <a class="pk-tile pk-tile--read" href="blogs.html"><h3>Insights</h3><ul class="pk-reads">{blogs}</ul><span class="pk-more">Read the blog {ARROW_R}</span></a>
        <a class="pk-tile pk-tile--reels" href="index.html#reels"><h3>Social reels</h3><div class="pk-posters"><img src="assets/reels/reel-3.jpg" alt="" loading="lazy" /><img src="assets/reels/reel-4.jpg" alt="" loading="lazy" /></div><p>Short-form reels that stop the scroll.</p></a>
      </div>
    </section>
'''


def pk_featured():
    c = CASES[0]
    head = head_block('Featured Work', 'A closer look, <em>one project</em>', 'What the brief was, and what changed once it shipped.', sid='pk-feat-title')
    stats = ''.join(f'<div><b>{e(v)}</b><span>{e(l)}</span></div>' for v, l in c['results'][:2])
    return f'''    <section class="co-sec pk-sec" aria-labelledby="pk-feat-title">
      {head}
      <div class="pk-feat" data-rise>
        <div class="pk-feat-info"><p class="pk-year">{c["year"]}</p><h3>A spec-sheet site rebuilt around one clear outcome</h3><div class="pk-stats">{stats}</div></div>
        <div class="pk-feat-show">
          <div class="pk-devices">
            <figure class="pk-d pk-d--main"><img src="{c["img"]}" alt="{e(c["alt"])}" loading="lazy" /></figure>
            <figure class="pk-d pk-d--phone pk-d--l"><img src="assets/reels/reel-2.jpg" alt="" loading="lazy" /></figure>
            <figure class="pk-d pk-d--phone pk-d--r"><img src="assets/reels/reel-5.jpg" alt="" loading="lazy" /></figure>
          </div>
        </div>
        <a class="pk-view" href="case-study.html">View Project {ARROW_R}</a>
      </div>
    </section>
'''


# ================================================================ BLOGS
BLOG_LIVE = 'https://squarezix.com/blogs/'

# Titles and categories are the live squarezix.com/blogs listing. The live listing shows no dates,
# descriptions or read times, so only the three posts already on the home page carry them.
# topic: brand | growth | digital | intelligence   (our new architecture over the live categories)
# ind:   industry-perspective picks (our classification, not a live category)
POSTS = [
    dict(t='Digital Growth in the GCC', c='Reports', topic='growth', date='August 25, 2025', iso='2025-08-25', read='7 min read',
         d='What’s actually driving results for brands scaling across Dubai, the wider GCC, and beyond.'),
    dict(t='WhatsApp Business API Pricing Changes in UAE: What Will Businesses Pay From October 2026?', c='Blog', topic='growth'),
    dict(t='Is DataLife Engine Still a Good CMS for Modern Websites?', c='Website Development', topic='digital'),
    dict(t='Shopify Storefronts Now Support UCP: Is Your Ecommerce Website Ready for AI Shopping Agents?', c='Website Development', topic='digital', ind='tech'),
    dict(t='How to Design Product Filters for Jewellery Ecommerce Stores Without Losing Sales', c='Website Management', topic='digital'),
    dict(t='Can SEO Work for a New Website? A 6-Month Growth Roadmap', c='Search Engine Optimization', topic='growth'),
    dict(t='Why Payload CMS Is Becoming a Powerful Choice for Next.js Websites', c='Website Development', topic='digital', ind='tech'),
    dict(t='WordPress 7.1.1 Fixes 11 Security Vulnerabilities: Is Your Website Updated?', c='Website Management', topic='digital'),
    dict(t='Can GPT-6 Astra Build Websites? What Businesses Need to Know', c='Website Development', topic='intelligence', ind='tech'),
    dict(t='Is Your Website Ready for iPhone 18 Pro? Mobile SEO & UX Checklist', c='Emerging Tech', topic='intelligence'),
    dict(t='Can You Post Images on TikTok? Here’s Everything You Need to Know', c='Social Media Marketing', topic='growth'),
    dict(t='Google Goto URL Redirects: Everything You Need to Know', c='Emerging Tech', topic='intelligence'),
    dict(t='Should My Business Website Be in Both Arabic and English in UAE?', c='Website Development', topic='digital'),
    dict(t='WhatsApp Web Calling Is Here: What the Latest Update Means for Businesses', c='Emerging Tech', topic='intelligence'),
    dict(t='Why Luxury Hotels Need Better Websites Than Booking Platforms', c='Website Development', topic='digital', ind='luxury'),
    dict(t='How AI Is Changing the Jewellery Buying Journey', c='Artificial Intelligence', topic='intelligence', ind='luxury'),
    dict(t='When Is the Right Time to Rebrand Your Business?', c='Branding', topic='brand'),
    dict(t='Is Your Brand Ready for Bigger Clients? Here’s How to Tell', c='Branding', topic='brand'),
    dict(t='Why Brands Are Replacing Hashtags with Bracketed Keywords on Social Media', c='Social Media Marketing', topic='growth'),
    dict(t='AI-First Content Architecture: How to Structure Your Website for Machine Understanding', c='Artificial Intelligence', topic='intelligence'),
    dict(t='The Real Reason Your Website Isn’t Appearing in AI Overviews (And the Fix Is Faster Than You Think)', c='Artificial Intelligence', topic='intelligence'),
    dict(t='Your Brand’s First Impression Happens in 0.3 Seconds, Before Anyone Reads Your Ad Copy', c='Branding', topic='brand'),
    dict(t='What Is a Brand Audit in Dubai and Why It’s So Important', c='Branding', topic='brand'),
    dict(t='Guide to Effective SEO Strategy in 2026', c='Search Engine Optimization', topic='growth'),
    dict(t='10 Mistakes You Need to Avoid in Paid Ads in 2026 (And How to Fix Them)', c='Search Engine Marketing', topic='growth'),
    dict(t='How Google AI Overviews Choose Which Brands to Trust', c='Search Engine Optimization', topic='intelligence'),
    dict(t='Micro-Moments That Build Macro-Brands', c='Branding', topic='brand'),
    dict(t='Zero-Click Marketing: How Brands Can Win Without the Click', c='Artificial Intelligence', topic='intelligence'),
    dict(t='Why Luxury Brands Need Premium Ecommerce Websites', c='Website Development', topic='digital', ind='luxury'),
    dict(t='How SEO Helps Luxury Wellness Clinics Increase Qualified Leads', c='Search Engine Optimization', topic='growth', ind='luxury'),
    dict(t='Dubai’s High-Competition Industries That MUST Use PPC in 2026', c='Search Engine Marketing', topic='growth'),
    dict(t='How Headless Architecture Improves Checkout Speed & Reduces Cart Abandonment', c='Website Development', topic='digital', ind='tech'),
    dict(t='ERP for E-Commerce in Dubai: Customization Tips to Boost Online Sales', c='ERP', topic='digital', ind='b2b'),
    dict(t='The Hidden Costs of Ignoring ERP Customization in Your Business Strategy', c='ERP', topic='digital', ind='b2b'),
    dict(t='How to Build a Scalable Website Architecture for Multi-Location Businesses in the UAE', c='Website Development', topic='digital', ind='b2b'),
    dict(t='Planning for 1000+ Pages Website? Choose Your CMS Carefully', c='Website Development', topic='digital', ind='b2b'),
    dict(t='Why Aesthetic Clinics in Dubai Need Beautifully Designed Websites to Attract Patients', c='Website Development', topic='digital', ind='pro'),
    dict(t='Preparing to Sell Your Business? Start with Your Website', c='Website Development', topic='digital', ind='pro'),
    dict(t='Your Trade License Is Approved—Now What? A Digital Setup Checklist for Dubai Startups', c='Website Development', topic='digital', ind='pro'),
    dict(t='Freelancer vs SEO Agency: Which Is Right for Your Business?', c='Search Engine Optimization', topic='growth', ind='pro'),
]
FEATURED = dict(t='How AI Is Changing Search Visibility', c='AI & Search', img='assets/blog/ai-search.jpg',
                alt='Isometric 3D kiosk with a striped awning and shelves of products', date='August 25, 2025', iso='2025-08-25', read='5 min read',
                d='Why ranking on Google isn’t enough anymore, and what showing up in AI answers actually takes.')
TOPICS = [('brand', 'Brand', 'Branding · Strategy · Identity', 'spark'),
          ('growth', 'Growth', 'SEO · Paid Media · Social · Content', 'signal'),
          ('digital', 'Digital', 'UX · Web · Development · Management', 'layers'),
          ('intelligence', 'Intelligence', 'AI · Emerging Technology · Search', 'bulb')]
INDUSTRIES = [('luxury', 'Luxury & Lifestyle'), ('pro', 'Professional Services'), ('tech', 'Technology & Innovation'), ('b2b', 'Industrial & B2B')]
TOPIC_ICON = {t[0]: t[3] for t in TOPICS}
CLOCK = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'


FEATURED_LIST = [
    dict(t='AI in the Modern Workplace: A Guide for Businesses', c='Artificial Intelligence', img='assets/blog/ai-workplace.jpg',
         alt='Illustrated team of three posing in front of a pink city skyline', date='August 25, 2025', iso='2025-08-25', read='6 min read',
         d='Explore how artificial intelligence is transforming business operations'),
    dict(t='How AI Is Changing Search Visibility', c='AI & Search', img='assets/blog/ai-search.jpg',
         alt='Isometric 3D kiosk with a striped awning and shelves of products', date='August 25, 2025', iso='2025-08-25', read='5 min read',
         d='Why ranking on Google isn’t enough anymore, and what showing up in AI answers actually takes.'),
]


def home_blog_card(p):
    """Same markup as the home page blog cards (sections.css .blog-card)."""
    return f'''<li>
        <a class="blog-card" href="{BLOG_LIVE}">
          <div class="blog-media"><img src="{p['img']}" alt="{e(p['alt'])}" loading="lazy" /></div>
          <div class="blog-body">
            <div class="blog-meta"><time datetime="{p['iso']}">{p['date']}</time><span class="blog-tag">{e(p['c'])}</span></div>
            <h3>{e(p['t'])}</h3>
            <p>{e(p['d'])}</p>
            <div class="blog-foot"><span class="blog-author">By Squarezix Team</span><span class="blog-read">{CLOCK}{p['read']}</span></div>
            <span class="blog-more">Read more <i class="blog-arrow">{ARROW_R}</i></span>
          </div>
        </a>
      </li>'''


def slug(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


def blog_card(p, i):
    if p.get('img'):
        vis = f'<img src="{p["img"]}" alt="{e(p.get("alt", ""))}" loading="lazy" />'
    else:
        vis = '<img class="bl-demo" src="assets/blog/placeholder.webp" alt="" loading="lazy" />'
    meta = ''
    if p.get('date'):
        meta = f'<span class="bl-when"><time datetime="{p["iso"]}">{p["date"]}</time><i></i>{CLOCK}{p["read"]}</span>'
    desc = f'<p class="bl-desc">{e(p["d"])}</p>' if p.get('d') else ''
    return (f'<article class="bl-card" data-topic="{p["topic"]}" data-ind="{p.get("ind", "none")}" data-cat="{slug(p["c"])}" data-n="{i}"><a class="bl-card-link" href="{BLOG_LIVE}">'
            f'<div class="bl-visual">{vis}<span class="bl-cat">{e(p["c"])}</span></div>'
            f'<div class="bl-card-body"><h3>{e(p["t"])}</h3>{desc}{meta}'
            f'<span class="bl-more">Read article <i>{ARROW_R}</i></span></div></a></article>')


def blogs():
    topic_counts = {k: sum(1 for p in POSTS if p['topic'] == k) for k, *_ in TOPICS}
    topics_html = ''.join(
        f'<li data-rise><button type="button" class="bl-topic" data-topic="{k}" aria-pressed="false">'
        f'<span class="bl-topic-ic">{ic(icn)}</span><span class="bl-topic-name">{name}</span>'
        f'<span class="bl-topic-sub">{sub}</span><span class="bl-topic-count">{topic_counts[k]:02d} articles</span></button></li>'
        for k, name, sub, icn in TOPICS)

    cards = '\n          '.join(blog_card(p, i) for i, p in enumerate(POSTS))

    tabs, panels = '', ''
    for j, (k, name) in enumerate(INDUSTRIES):
        sel = j == 0
        on = ' is-on' if sel else ''
        tabidx = '' if sel else ' tabindex="-1"'
        tabs += f'<button type="button" class="co-chip{on}" role="tab" id="bl-ind-tab-{k}" aria-controls="bl-ind-{k}" aria-selected="{str(sel).lower()}"{tabidx}>{name}</button>'
        links = ''.join(
            f'<li><a href="{BLOG_LIVE}"><span class="bl-ind-cat">{e(p["c"])}</span><span class="bl-ind-title">{e(p["t"])}</span>{ARROW_R}</a></li>'
            for p in POSTS if p.get('ind') == k)
        panels += (f'<div class="bl-ind-panel" role="tabpanel" id="bl-ind-{k}" aria-labelledby="bl-ind-tab-{k}"{"" if sel else " hidden"}>'
                   f'<h3 class="bl-ind-q">What’s changing in <em>{name}?</em></h3><ul class="bl-ind-list">{links}</ul></div>')

    faq = [
        ('Who writes the articles?', 'Our team of strategists, designers, developers and marketers — the same people who do the work. Articles are published under the Squarezix Team.'),
        ('Can I suggest a topic?', 'Please do. Send us the question you would like answered through the contact form below and we will consider it for a future article.'),
        ('Do you offer SEO and content services too?', 'Yes. SEO and AI visibility, content, social, paid media, branding and web development are all part of what we do — one team, one process.'),
        ('How do I stay updated?', 'Browse the latest insights here, or follow us on social for new articles on AI, growth and the platforms shaping how brands get discovered.'),
    ]

    cats = sorted({p['c'] for p in POSTS})
    blog_bar = filterbar('Filter articles', [
        ('topic', 'Topic', 'All Topics', [(k, name) for k, name, *_ in TOPICS]),
        ('ind', 'Industry', 'All Industries', INDUSTRIES),
        ('cat', 'Category', 'All Categories', [(slug(c), c) for c in cats]),
    ], 'bl-bar')

    featured_cards = '\n      '.join(home_blog_card(x) for x in FEATURED_LIST)
    f = FEATURED
    feature = f'''<article class="bl-feature" data-rise>
        <a class="bl-feature-media" href="{BLOG_LIVE}" tabindex="-1" aria-hidden="true"><img src="{f['img']}" alt="" loading="lazy" /></a>
        <div class="bl-feature-body">
          <span class="bl-cat bl-cat--solid">{e(f['c'])}</span>
          <h3><a href="{BLOG_LIVE}">{e(f['t'])}</a></h3>
          <p>{e(f['d'])}</p>
          <div class="bl-byline"><span>By Squarezix Team</span><i></i><time datetime="{f['iso']}">{f['date']}</time><i></i><span class="bl-read">{CLOCK}{f['read']}</span></div>
          <a href="{BLOG_LIVE}" class="btn-contact btn-contact--xl">Read Article {ARROW_R}</a>
        </div>
      </article>'''

    body = hero('Blogs', 'Ideas shaping the future of <em>digital growth.</em>',
                'Perspectives, strategies and practical thinking across branding, technology, search, marketing and digital experiences.',
                'Explore the latest', '#latest')
    body += f'''
    <section class="co-sec" id="latest" aria-labelledby="bl-latest-title">
      {head_block('Browse Blogs', 'Find an article <em>worth reading</em>', 'Filter by topic, industry and category to get straight to what matters.', sid='bl-latest-title')}
      <div class="bl-bar-wrap">{blog_bar}</div>
      <div class="bl-grid" id="bl-grid">
          {cards}
      </div>
      <p class="bl-nomatch" id="bl-nomatch" hidden>No articles match those filters. <button type="button" class="co-link" data-filter-reset>Reset filters</button></p>
      <div class="co-more"><button type="button" class="btn-contact btn-contact--xl bl-loadmore" id="bl-loadmore">Load more articles {ARROW_R}</button></div>
    </section>

    <section class="co-sec" aria-labelledby="bl-topics-title">
      {head_block('Explore by Topic', 'Four ways into <em>what we think</em>', 'Choose a topic to filter the articles above.', sid='bl-topics-title')}
      <ul class="bl-topics">{topics_html}</ul>
    </section>

    <section class="co-sec" aria-labelledby="bl-ind-title">
      {head_block('Industry Perspectives', 'What’s changing in <em>your industry?</em>', 'Pick your sector for the articles most relevant to it.', sid='bl-ind-title')}
      <div class="bl-ind">
        <div class="co-chips bl-ind-tabs" role="tablist" aria-label="Industry" data-rise>{tabs}</div>
        <div class="bl-ind-panels" data-rise>{panels}</div>
      </div>
    </section>

    <section class="blog bl-featured" id="featured" aria-labelledby="blog-title">
      <div class="blog-head">
        <span class="blog-badge">Featured Insights</span>
        <h2 id="blog-title">Start with our <em>featured</em> insights.</h2>
        <p>Perspectives on AI, growth, and the platforms shaping how brands get discovered.</p>
      </div>
      <ul class="blog-list">
      {featured_cards}
      </ul>
    </section>
'''
    body += faq_band('Questions about <em>our insights?</em>', 'Quick answers about where the articles come from.', faq)
    write('blogs', 'Insights — Ideas Shaping the Future of Digital Growth | SquareZix',
          'Perspectives, strategies and practical thinking across branding, technology, search, marketing and digital experiences from the SquareZix team in Dubai.', 'insights', body)


if __name__ == '__main__':
    culture()
    careers()
    portfolio()
    blogs()
