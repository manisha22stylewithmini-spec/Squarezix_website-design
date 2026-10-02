#!/usr/bin/env python3
"""Builds the three service hub pages from one template.

    python3 scripts/build_service_pages.py

Header, footer, contact form and script tags are lifted from about-us.html so the
pages can never drift from it; only <main> differs. Copy is taken from the matching
service pages on squarezix.com. Edit PAGES below and re-run to change a page.
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

INDUSTRIES = ['Marketing & Advertising Agencies', 'Real Estate & Property Management', 'Logistics & Supply Chain Companies',
              'Healthcare & Wellness Enterprises', 'SMEs and Growing Startups', 'Retail & E-commerce Businesses']

# One image per sub-category (group id → file). Used as the tile in the statement, the
# dock and the feature row. Swap these for purpose-made visuals when they exist.
GROUP_IMG = {
    'branding': 'assets/blog/ai-workplace.jpg', 'designing': 'assets/work/project-2.png', 'development': 'assets/work/project-3.png',
    'social': 'assets/reels/reel-1.jpg', 'content': 'assets/blog/gcc-growth.jpg',
    'seo': 'assets/blog/ai-search.jpg', 'generative': 'assets/work/project-1.png',
}

PAGES = [
    {
        'file': 'web-and-brand.html', 'menu': 'web', 'badge': 'Web & Brand',
        'title': 'Web & Brand — Branding, Web Design & Development | Squarezix',
        'desc': 'Brand strategy, identity, website design and development from one Dubai team. Websites designed to convert, scale and rank.',
        'h1': ['Professional Web Design', 'That Turns Clicks', 'into Customers.'], 'grad': 1,
        'lead': 'Your website shouldn’t just look good, it should drive measurable growth. We craft brand identities that connect and build websites designed to convert, scale and rank.',
        'screen': 'Rec · CH 03', 'region': 'Brand · Design · Build',
        # Statement after the hero: {group id} marks where that group's image tile sits in the sentence
        'statement': 'One team for the {branding} brand you stand for, the {designing} experience people use and the {development} site that <em>performs.</em>',
        'intro': ('What we do', 'Strategic brand building, <em>designed and built</em> to perform',
                  'Your brand is more than a logo — it’s the reason customers choose you over competitors. From brand strategy and visual identity to the site that carries it, one team does the whole job.'),
        # Groups and items mirror this menu's tabs and services in menu.js — keep the two in step
        'groups': [
            ('branding', 'Branding', 'Identities that connect, convert and create lasting impressions.', [
                ('Brand Strategy & Positioning', 'We define who you are, who you serve, and why you win. Market research, competitor audits and positioning frameworks that carve out your irreplaceable space.'),
                ('Visual Identity Design', 'Logo systems, colour palettes, typography, iconography and brand guidelines — every visual touchpoint crafted to be instantly recognisable. No templates. No generic outputs.'),
                ('Brand Audit & Rebranding', 'We forensically audit every brand asset, identify gaps and lead full or partial rebrands that modernise without losing the equity you’ve spent years building.'),
                ('Brand Experience & Touchpoints', 'Every interaction your customer has with your brand is a chance to build trust or lose it. We map, design and optimise every physical and digital touchpoint.'),
                ('Brand Collateral & Print Design', 'Business cards, brochures, pitch decks, packaging and signage — tangible brand assets designed to the same uncompromising standard as your digital presence.'),
                ('Content Creation Services', 'Photo, video and brand copy that carry the identity into every channel.'),
            ]),
            ('designing', 'Designing', 'Custom, user-friendly, responsive websites tailored to your business goals.', [
                ('Website Design', 'Custom, user-friendly, responsive websites: conversion-first and pixel-perfect.'),
                ('E-commerce Website Design', 'Online stores that are visually appealing and conversion-driven: user-friendly navigation, product-centric layouts and seamless checkout.'),
                ('Email Marketing Testing & Design', 'Email templates designed on brand and tested across clients before they go out.'),
                ('Mobile App Design', 'iOS and Android UX/UI, from flows to finished screens.'),
                ('Rapid Web Design', 'A launch-ready site in two weeks, for when the deadline will not move.'),
                ('Social Media Design', 'Posts, reels and ad creative in one visual system.'),
            ]),
            ('development', 'Development', 'Fast, accessible, SEO-ready builds on the platform that fits you.', [
                ('Website Management', 'Updates, hosting and care plans that keep the site healthy after launch.'),
                ('Website Development', 'Fast, accessible, SEO-ready websites engineered around your content and your editors.'),
                ('Headless CMS Development', 'Sanity, Strapi and Contentful builds that separate content from presentation, so your site stays fast and flexible.'),
                ('E-commerce Website Development', 'Shopify, WooCommerce and custom storefronts built to sell.'),
                ('Headless E-commerce Development', 'Shopify Hydrogen and Next.js storefronts for fast browsing and frictionless checkout.'),
                ('Website Migration Services', 'Move platforms and keep your rankings: redirect planning, URL preservation and content mapping.'),
            ]),
        ],
        'pillars': ('Our approach', 'Our comprehensive branding <em>strategy pillars</em>', [
            ('Plan', ['Brand Launch Strategy', 'Social Media Strategy', 'Brand Messaging Framework', 'Campaign Strategy', 'Launch Event Planning']),
            ('Create', ['Brand Identity', 'Brand Guidelines', 'Brand Logo', 'Brand Marketing Assets', 'Brand Creatives']),
            ('Launch', ['Brand Management', 'Social Media Management', 'Launch Event Management', 'Public Relations', 'Media Relations']),
        ]),
        # Same component as the home page's Why SquareZix (heading lines, intro, six cards)
        'why': ('More than a <em>pretty site.</em>', 'Design and build that earn their keep.', 'Research, strategy, design and engineering under one roof, so the brand and the website are built to perform together.', [
            ('Research-Led Design', 'Stakeholder interviews, user surveys and competitor audits before a single layout.'),
            ('Strategy First', 'Every page and interaction is aligned to a business goal: leads, sign-ups, sales.'),
            ('Conversion Built In', 'CRO is part of the design process: wireframe tests, heatmaps and analytics.'),
            ('Fast by Design', 'Lightweight layouts and optimised imagery, built for Core Web Vitals.'),
            ('Arabic-First Thinking', 'Identities and layouts that work in Arabic and English, RTL included.'),
            ('Accessible UX', 'WCAG best practices: semantic HTML, keyboard navigation and colour contrast.'),
        ]),
        # Six stops round the clock face, clockwise from 12 (see clock_html / clock.js).
        # Each stop: name, when, lead, what happens, what you get.
        'clock': ('How we work', 'From brief to launch, <em>like clockwork</em>', [
            ('Discover', 'Week 1', 'We learn the business before we touch a pixel, so every later decision has a reason behind it.',
             ['Stakeholder workshops', 'Audience and competitor research', 'Site, SEO and analytics audit'],
             ['Discovery report', 'KPI map', 'Project roadmap']),
            ('Position', 'Week 2', 'We define who you are, who you serve and why you win, then put it into words.',
             ['Positioning framework', 'Naming and messaging', 'Tone of voice'],
             ['Brand strategy deck', 'Messaging framework']),
            ('Design', 'Weeks 3–5', 'Identity first, then the experience: every screen designed and signed off before build.',
             ['Visual identity system', 'UX wireframes', 'High-fidelity UI and motion prototype'],
             ['Brand guidelines', 'UI kit', 'Clickable prototype']),
            ('Build', 'Weeks 6–8', 'Engineered for speed, SEO and content-editor happiness on the platform that fits you.',
             ['Front-end and CMS build', 'Performance and SEO setup', 'QA across devices'],
             ['Staging site', 'Editor training', 'Launch checklist']),
            ('Launch', 'Week 9', 'A staged rollout and a brand reveal that makes the market take notice from day one.',
             ['Staged rollout and redirects', 'Tracking and analytics', 'Brand reveal campaign'],
             ['Live site', 'Analytics dashboard', 'Launch assets']),
            ('Grow', 'Ongoing', 'Launch is day one. Then we measure, test and improve in quarterly growth sprints.',
             ['Quarterly growth sprints', 'A/B tests and CRO', 'Content and SEO iteration'],
             ['Monthly reports', 'Test backlog', 'Roadmap updates']),
        ]),
        'steps': [('Discover', 'Deep-dive workshops on brand, audience, competitors and KPIs.'), ('Design', 'UX wireframes → high-fidelity UI → motion prototypes.'),
                  ('Build', 'Engineered for speed, SEO and content-editor happiness.'), ('Grow', 'Launch is day one. Then quarterly growth sprints, forever.')],
    },
    {
        'file': 'growth-marketing.html', 'menu': 'growth', 'badge': 'Growth Marketing',
        'title': 'Growth Marketing — Social Media & Content Marketing | Squarezix',
        'desc': 'Social media and content marketing from a Dubai team: strategy, content, community, paid campaigns and reporting that explains what happened and why.',
        'h1': ['Social Media Marketing', 'That Drives Engagement', 'and Generates Leads.'], 'grad': 1,
        'lead': 'Squarezix helps brands grow online with creative social media posts, data-driven strategies, and results that truly make an impact across all social platforms.',
        'screen': 'Rec · CH 04', 'region': 'Social · Content · Paid',
        # Statement after the hero: {group id} marks where that group's image tile sits in the sentence
        'statement': 'Growth that compounds: {social} social people follow and {content} content worth <em>sharing.</em>',
        'intro': ('What we do', 'Campaigns that build <em>brand loyalty</em> and generate leads',
                  'We specialise in creating impactful campaigns that drive engagement, build brand loyalty and generate leads across all major platforms.'),
        # Groups and items mirror this menu's tabs and services in menu.js — keep the two in step
        'groups': [
            ('social', 'Social Media Marketing', 'A consistent, authentic presence on every platform your audience uses.', [
                ('Community Management', 'We start conversations, respond to feedback, manage reputation and monitor what people say about your brand.'),
                ('Content Creation Services', 'Posts, graphics, videos, stories and reels that reflect your brand identity and resonate with your audience.'),
                ('Advertising & Media Services', 'Paid social that pays back: targeted campaigns on Facebook, Instagram, TikTok, Snapchat, LinkedIn and X.'),
                ('Social Media Event Management', 'Launches, live coverage and activations, planned and run on your channels.'),
            ]),
            ('content', 'Content Marketing', 'Words, coverage and assets built to be found and shared.', [
                ('Website Copywriting', 'Words that convert and rank.'),
                ('Digital PR', 'Coverage and authority links.'),
                ('Multimedia Content Assets', 'Video, graphics and guides built to be shared.'),
            ]),
        ],
        'pillars': ('Our approach', 'Social media marketing <em>services</em>', [
            ('Strategy Development', ['A tailored social media strategy', 'Aligned with your objectives', 'Built to maximise your ROI']),
            ('Content Creation', ['Eye-catching graphics', 'Compelling copy', 'Delivered across all platforms']),
            ('Media Management', ['Scheduling posts', 'Engaging with your followers', 'A consistent, authentic presence']),
            ('Analytics & Reporting', ['Detailed analytics', 'Clear campaign reporting', 'Insights into performance']),
        ]),
        # Same component as the home page's Why SquareZix (heading lines, intro, six cards)
        'why': ('More than <em>posting.</em>', 'Social and content that move the numbers.', 'Organic, paid, community and reporting run as one system, tuned for Dubai and the GCC.', [
            ('Culturally Tuned', 'Content in Arabic and English, adapted for local customs and audiences.'),
            ('Data-First Strategy', 'Analytics and social listening define who your customers are and when they engage.'),
            ('Paid + Organic', 'Organic content that builds trust, blended with paid campaigns that drive action.'),
            ('Platform Mastery', 'Formats that work on Instagram, TikTok, LinkedIn, Facebook, YouTube and Snapchat.'),
            ('Local Moments', 'Dubai events, seasons and festivals built into every content calendar.'),
            ('Transparent Reporting', 'Clear metrics, what happened, why, and what we’ll do next.'),
        ]),
        'steps': [('Listen', 'Audience research, competitor analysis and social listening.'), ('Plan', 'Content calendars built around your goals and local moments.'),
                  ('Create', 'Posts, reels, stories and ad creative, in Arabic and English.'), ('Optimise', 'Real-time monitoring and regular reports that say what’s next.')],
    },
    {
        'file': 'ai-and-intelligence.html', 'menu': 'ai', 'badge': 'AI & Intelligence',
        'title': 'AI & Intelligence — SEO, AI SEO & Generative Search | Squarezix',
        'desc': 'SEO and AI search optimisation from Dubai: get found on Google and cited by ChatGPT, Gemini, Perplexity and AI Overviews.',
        'h1': ['Your Customers Search', 'Smarter. We Make Sure', 'They Find You.'], 'grad': 1,
        'lead': 'If your business isn’t showing up on ChatGPT, Gemini, Perplexity, Google and AI Overviews, you’re already losing customers to competitors who are. We build the visibility, trust and authority that gets you recommended.',
        'screen': 'Rec · CH 05', 'region': 'SEO · AEO · GEO',
        # Statement after the hero: {group id} marks where that group's image tile sits in the sentence
        'statement': 'Be the answer everywhere: {seo} ranked on Google and {generative} cited by <em>AI.</em>',
        'intro': ('What we do', 'Be everywhere your audience <em>is searching</em>',
                  'We don’t just optimise for Google — we optimise your brand for ChatGPT, Gemini, Perplexity and the AI answers your customers now read first.'),
        # Groups and items mirror this menu's tabs and services in menu.js — keep the two in step
        'groups': [
            ('seo', 'Core SEO', 'The technical, on-page and off-page foundation everything else stands on.', [
                ('Enterprise SEO', 'SEO that scales across thousands of pages.'),
                ('E-commerce SEO', 'If you’re running an online store in the UAE, your website needs more than attractive products — it needs visibility.'),
                ('Local SEO', 'Google Business Profile optimisation, citations across trusted UAE directories, reviews and geo-targeted content.'),
                ('AI & LLM SEO', 'Get cited by ChatGPT and Gemini as well as ranked on Google.'),
                ('Search Engine Optimization', 'Technical, on-page and off-page — the full foundation.'),
            ]),
            ('generative', 'Generative Search', 'Structured, citable, conversational content that AI engines quote.', [
                ('Generative AI Research and Analysis', 'How AI answers talk about you today, and where the gaps are.'),
                ('Semantic Keywords Research', 'Topics, entities and intent, not just keywords.'),
                ('AI-Optimised Content', 'Structured, citable, conversational content written to be quoted by AI.'),
                ('Community Engagement Optimization', 'Presence on Reddit, Quora and the forums AI models read.'),
                ('Brand Visibility and Authority', 'Mentions and backlinks from sources that models trust.'),
                ('AI-Friendly Structured Data', 'Schema markup that machines can read.'),
            ]),
        ],
        'pillars': ('Our approach', 'Our comprehensive AI SEO <em>strategy pillars</em>', [
            ('Technical foundation', ['Website architecture optimisation', 'Core Web Vitals', 'Structured data & schema markup', 'Crawlable by GPTBot and search engines']),
            ('Content for generative search', ['Simple, conversational content', 'Q&A sections and TL;DR summaries', 'Logically structured headings', 'English and Arabic']),
            ('AI authority', ['Targeting LLM-cited sources', 'Quality backlinks', 'Authoritative, relevant domains', 'Stronger AI trust signals']),
            ('Multiple formats', ['Blogs and long-form guides', 'Infographics and short-form visuals', 'Videos optimised for AI search', 'Featured in AI Overviews']),
        ]),
        # Same component as the home page's Why SquareZix (heading lines, intro, six cards)
        'why': ('More than <em>rankings.</em>', 'Found on Google, cited by AI.', 'Technical SEO, content and authority working together, so search engines and AI answers both recommend you.', [
            ('Built for Dubai', 'AI SEO strategies aligned with Dubai’s fast-moving digital landscape.'),
            ('Predictive SEO', 'We forecast ranking shifts and search trends, then optimise ahead of time.'),
            ('Intent Targeting', 'Intent-based, high-value keywords tailored to your industry, not generic lists.'),
            ('Competitor Watch', 'Real-time monitoring so we can counter new moves and hold your advantage.'),
            ('Arabic + English', 'Content strategies that are bilingual from the start, multilingual when needed.'),
            ('Data-Rich Reporting', 'Dashboards for rankings, traffic, AI visibility and competitor gaps.'),
        ]),
        'steps': [('Audit', 'Technical gaps, ranking opportunities and LLM citation potential.'), ('Structure', 'Architecture, schema and Core Web Vitals for crawlers and AI bots.'),
                  ('Publish', 'Citable, conversational content in the formats AI engines quote.'), ('Monitor', 'Rankings, AI visibility and citation frequency, tracked continuously.')],
    },
]

e = html.escape


def clock_html(p):
    """Pinned scroll section: a clock whose hand sweeps round six process stops (clock.js)."""
    badge, title, stops = p['clock']
    n = len(stops)
    labels = ''.join(
        f'<li class="svp-stop" style="--i:{i}"><button type="button" data-stop="{i}" aria-label="Step {i + 1}: {e(t)}">'
        f'<span class="svp-stop-no">({i + 1:02d})</span><span class="svp-stop-name">{e(t)}</span><span class="svp-stop-when">{e(w)}</span></button></li>'
        for i, (t, w, *_r) in enumerate(stops))
    details = ''.join(
        f'<li class="svp-clock-detail" data-stop="{i}">'
        f'<div class="svp-cd-top"><span class="svp-clock-no">{i + 1:02d}</span><span class="svp-cd-when">{e(w)}</span></div>'
        f'<h3>{e(t)}</h3><p class="svp-cd-lead">{e(lead)}</p>'
        f'<div class="svp-cd-cols"><div class="svp-cd-does"><h4>What happens</h4><ul>{"".join(f"<li>{e(x)}</li>" for x in does)}</ul></div>'
        f'<div class="svp-cd-gets"><h4>You get</h4><ul>{"".join(f"<li>{e(x)}</li>" for x in gets)}</ul></div></div></li>'
        for i, (t, w, lead, does, gets) in enumerate(stops))
    hour = ' class="is-hour"'
    ticks = ''.join(f'<i style="--t:{i}"{hour if i % 5 == 0 else ""}></i>' for i in range(60))
    marks = ''.join(f'<i style="--i:{i}"></i>' for i in range(n))
    return f'''    <!-- ===== Process clock: pinned while the hand goes once round the dial ===== -->
    <section class="svp-clock" id="process" aria-labelledby="svp-clock-title" style="--n:{n}">
      <div class="svp-clock-pin">
        <div class="svp-clock-copy">
          <span class="svc-badge">{e(badge)}</span>
          <h2 id="svp-clock-title" class="ab-h2">{title}</h2>
          <ol class="svp-clock-details">{details}</ol>
          <p class="svp-clock-count" aria-hidden="true"><b>01</b> / {n:02d}<span><i></i></span></p>
        </div>
        <div class="svp-dial-wrap">
          <div class="svp-orbit" aria-hidden="true"><i class="svp-sat"></i></div>
          <div class="svp-dial" aria-hidden="true">
            <div class="svp-bezel"></div>
            <div class="svp-face"></div>
            <div class="svp-sector"></div>
            <div class="svp-ticks">{ticks}</div>
            <div class="svp-marks">{marks}</div>
            <span class="svp-hand svp-hand--hour"></span>
            <span class="svp-hand svp-hand--min"></span>
            <span class="svp-hand svp-hand--sweep"></span>
            <img class="svp-hub" src="assets/bento/sz-badge.webp" alt="" width="1119" height="1112" loading="lazy" />
          </div>
          <ol class="svp-stops" aria-label="Process steps">{labels}</ol>
        </div>
      </div>
    </section>

'''


def showcase_html(p):
    """Statement with one image tile per sub-category; on scroll the tiles drop out of the
    sentence into a dock (showcase.js), then each sub-category gets its own alternating row.
    Works for any number of groups."""
    groups = p['groups']
    n = len(groups)
    inds = ''.join(f'<li>{e(x)}</li>' for x in INDUSTRIES)
    ib, _it, ip = p['intro']          # eyebrow above the sentence, paragraph once the tiles have landed
    text = p['statement']
    for i, (gid, name, _b, _c) in enumerate(groups):
        text = text.replace('{' + gid + '}', f'<span class="svb-slot" data-i="{i}" aria-hidden="true"></span>')
    tiles = ''.join(f'<div class="svb-tile" data-i="{i}"><img src="{GROUP_IMG[gid]}" alt="" loading="lazy" /></div>' for i, (gid, *_r) in enumerate(groups))
    dock = ''.join(
        f'<li><a href="#svf-{gid}"><span class="svb-dock-slot" data-i="{i}"><img src="{GROUP_IMG[gid]}" alt="" loading="lazy" /></span>'
        f'<span class="svb-dock-label"><b>{i + 1:02d}</b>{e(name)}</span></a></li>' for i, (gid, name, _b, _c) in enumerate(groups))
    ticks = ''.join('<i></i>' for _ in range(24))
    rows = ''
    for i, (gid, name, blurb, cards) in enumerate(groups):
        specs = ''.join(f'<li>{e(t)}</li>' for t, _d in cards)
        rows += f'''
      <article class="svf-row" id="svf-{gid}">
        <div class="svf-panel" data-rise>
          <div class="svf-art"><img src="{GROUP_IMG[gid]}" alt="" loading="lazy" /></div>
          <ul class="svf-specs" aria-label="{e(name)} services">{specs}</ul>
        </div>
        <div class="svf-copy">
          <p class="svf-kicker" data-rise><b>{i + 1:02d}</b> / {n:02d}</p>
          <h3 data-rise>{e(name)}</h3>
          <p class="svf-blurb" data-rise>{e(blurb)}</p>
          <a class="svp-link" href="#ab-contact" data-rise>Talk to us about {e(name.lower())} {ARROW}</a>
        </div>
      </article>'''
    return f'''    <!-- ===== Showcase: the sentence's image tiles drop into a dock as you scroll ===== -->
    <section class="svb" aria-labelledby="svb-title" style="--n:{n}">
      <div class="svb-pin">
        <span class="svc-badge svb-badge">{e(ib)}</span>
        <h2 id="svb-title" class="svb-statement">{text}</h2>
        <div class="svb-dock">
          <div class="svb-dock-bar" aria-hidden="true"><span class="svb-play"></span><span class="svb-time">00:0{n} / 00:0{n}</span><span class="svb-ticks">{ticks}</span></div>
          <ol class="svb-dock-slots">{dock}</ol>
        </div>
        <div class="svb-tiles" aria-hidden="true">{tiles}</div>
      </div>
    </section>
    <p class="svb-after" data-rise>{e(ip)}</p>

    <!-- ===== One row per sub-category, alternating sides ===== -->
    <section class="svf" id="services" aria-label="{e(p['badge'])} sub-categories">{rows}
      <div class="svp-ind-row" data-rise>
        <p class="svp-ind-label">Industries we work with</p>
        <ul class="svp-ind">{inds}</ul>
      </div>
    </section>

'''


SHOW_WHY = False


def why_html(p):
    """The home page's Why SquareZix section (markup, icons, whyus.js) with this page's copy."""
    home = (ROOT / 'index.html').read_text()
    start = home.index('<section class="why-us wu-h"')
    sec = home[start:home.index('</section>', start) + len('</section>')]
    l1, l2, sub, cards = p['why']
    sec = re.sub(r'(<span class="wu-line1">).*?(</span>\s*<span class="wu-line2">)', lambda m: m.group(1) + l1 + m.group(2), sec, count=1, flags=re.S)
    sec = re.sub(r'(<span class="wu-line2">).*?(</span>)', lambda m: m.group(1) + e(l2) + m.group(2), sec, count=1, flags=re.S)
    sec = re.sub(r'(<p class="wu-sub">).*?(</p>)', lambda m: m.group(1) + e(sub) + m.group(2), sec, count=1, flags=re.S)
    it = iter(cards)
    def card(m):
        t, d = next(it)
        return f'<h3>{e(t)}</h3>\n              <p>{e(d)}</p>'
    sec, n = re.subn(r'<h3>.*?</h3>\s*<p>.*?</p>', card, sec, flags=re.S)
    assert n == len(cards), f'home section has {n} cards, page defines {len(cards)}'
    return '    ' + sec.replace('href="#contact"', 'href="#ab-contact"') + '\n\n'


def main_html(p):
    grad = ' class="ab-grad"'
    lines = ''.join(f'<span{grad if i == p["grad"] else ""}>{e(t)}</span>' for i, t in enumerate(p['h1']))
    groups = ''
    for n, (gid, name, blurb, cards) in enumerate(p['groups'], 1):
        items = ''.join(f'<li class="svp-card" id="{gid}-{i}" data-rise><span class="svp-card-no">{n:02d}.{i:02d}</span><h4>{e(t)}</h4><p>{e(d)}</p></li>'
                        for i, (t, d) in enumerate(cards, 1))
        groups += f'''
      <div class="svp-group" id="{gid}">
        <div class="svp-group-head">
          <span class="svp-group-no">{n:02d}</span>
          <h3 data-rise>{e(name)}</h3>
          <p data-rise>{e(blurb)}</p>
          <a class="svp-link" href="#ab-contact" data-rise>Talk to us about {e(name.lower())} {ARROW}</a>
        </div>
        <ul class="svp-cards">{items}</ul>
      </div>'''
    jump = ''.join(f'<a href="#{gid}">{e(name)}<sup>{len(cards):02d}</sup></a>' for gid, name, _, cards in p['groups'])
    pb, pt, pl = p['pillars']
    pillars = ''.join(f'<li class="svp-pillar" data-rise><span class="svp-pillar-no">{i:02d}</span><h3>{e(t)}</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in xs)}</ul></li>'
                      for i, (t, xs) in enumerate(pl, 1))
    # Why SquareZix lives on the home page only. Set SHOW_WHY = True to put it back on these pages.
    why = why_html(p) if SHOW_WHY else ''
    showcase = showcase_html(p)
    steps = ''.join(f'<li class="ab-step" data-rise><span class="ab-step-num">{i:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(p['steps'], 1))
    inds = ''.join(f'<li>{e(x)}</li>' for x in INDUSTRIES)
    ib, it, ip = p['intro']
    process = clock_html(p) if 'clock' in p else f'''    <!-- ===== Process (same track as the About page) ===== -->
    <section class="ab-process" aria-labelledby="svp-process-title">
      <div class="ab-head ab-center">
        <span class="svc-badge" data-rise>How We Work</span>
        <h2 id="svp-process-title" class="ab-h2 ab-reveal" data-reveal>A process that’s <em>boringly reliable</em></h2>
        <p class="ab-sub" data-rise>No surprises. No scope creep. Every engagement follows the same four-phase system.</p>
      </div>
      <ol class="ab-steps" id="ab-steps">{steps}</ol>
    </section>

'''
    return f'''  <main id="service" class="svp">
    <!-- ===== Hero — same universe as the About page ===== -->
    <section class="ab-hero" aria-labelledby="svp-hero-title">
      <canvas class="ab-stars" aria-hidden="true"></canvas>
      <div class="ab-hero-grid" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span></div>
      <div class="ab-hero-inner">
        <div class="ab-hero-copy">
          <span class="svc-badge ab-badge" data-rise>{e(p['badge'])}</span>
          <h1 id="svp-hero-title" class="ab-hero-title svp-hero-title" data-rise>{lines}</h1>
          <p class="svp-lead" data-rise>{e(p['lead'])}</p>
          <div class="ab-hero-cta" data-rise>
            <a href="#ab-contact" class="btn-contact btn-contact--xl">Speak to an Expert {ARROW}</a>
            <a href="#services" class="ab-btn-ghost">See services {ARROW}</a>
          </div>
        </div>
        <figure class="ab-hero-media" data-rise>
          <div class="ab-screen">
            <video src="assets/hero/hero-video.mp4" poster="assets/hero/hero-poster.jpg" autoplay muted loop playsinline preload="metadata"></video>
            <div class="ab-screen-fx" aria-hidden="true"></div>
            <div class="ab-screen-ui" aria-hidden="true"><span><i class="crt-rec"></i>{e(p['screen'])}</span><span>{e(p['region'])}</span></div>
          </div>
          <figcaption class="ab-stat ab-stat--a"><strong data-count="1000" data-suffix="+">1,000+</strong><span>Successful websites</span></figcaption>
          <div class="ab-stat ab-stat--b" aria-hidden="true"><strong data-count="120" data-suffix="+">120+</strong><span>Projects on one process</span></div>
        </figure>
      </div>
    </section>

    <div class="marquee" aria-label="Our services">
      <div class="marquee-track" id="marquee-track">
        <ul class="marquee-group">
          <li>AI Search Visibility</li><li>Web Design &amp; Development</li><li>SEO &amp; Growth</li><li>Branding &amp; Strategy</li><li>Social Media Marketing</li>
        </ul>
      </div>
    </div>

{showcase}    <!-- ===== Approach ===== -->
    <section class="svp-pillars" aria-labelledby="svp-pillars-title">
      <div class="ab-head ab-center">
        <span class="svc-badge" data-rise>{e(pb)}</span>
        <h2 id="svp-pillars-title" class="ab-h2 ab-reveal" data-reveal>{pt}</h2>
      </div>
      <ol class="svp-pillar-list" style="--n:{len(pl)}">{pillars}</ol>
    </section>

{why}{process}'''


def build():
    src = (ROOT / 'about-us.html').read_text()
    head, rest = src.split('<main', 1)
    main, tail = rest.split('</main>', 1)
    contact = main[main.index('<section class="ab-contact"'):]          # reuse the About contact block as is
    for p in PAGES:
        h = re.sub(r'<title>.*?</title>', f'<title>{e(p["title"])}</title>', head, flags=re.S)
        h = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{e(p["desc"])}"', h)
        ver = re.search(r'about\.css(\?v=\w+)', h).group(1)             # same cache-buster as the other assets
        h = re.sub(r'(<link rel="stylesheet" href="about\.css[^>]*>)', rf'\1\n  <link rel="stylesheet" href="service.css{ver}" />', h)
        h = h.replace('class="nav-link is-current" href="about-us.html" aria-current="page"', 'class="nav-link" href="about-us.html"')
        h = h.replace(f'<div class="nav-item" data-menu="{p["menu"]}">', f'<div class="nav-item is-current" data-menu="{p["menu"]}">')
        t = tail.replace('<script src="about.js', f'<script src="showcase.js{ver}"></script>\n  <script src="about.js', 1)
        if SHOW_WHY:
            t = t.replace('<script src="about.js', f'<script src="whyus.js{ver}"></script>\n  <script src="about.js', 1)
        if 'clock' in p:
            t = t.replace('<script src="about.js', f'<script src="clock.js{ver}"></script>\n  <script src="about.js', 1)
        (ROOT / p['file']).write_text(h + main_html(p) + '    ' + contact + '</main>' + t)
        print('wrote', p['file'])


if __name__ == '__main__':
    build()
