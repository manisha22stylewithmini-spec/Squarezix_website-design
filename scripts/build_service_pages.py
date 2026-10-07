#!/usr/bin/env python3
"""Builds the service pages and the Services / Development & Maintenance menus.

    python3 scripts/build_service_pages.py

Pages: branding, design, social-media-marketing, content-marketing, paid-marketing,
seo-ai-visibility, geo, website-development, its sub-inner page
ecommerce-website-development, and website-maintenance. Copy comes from the live squarezix.com
service pages (scripts/live_content.py); PAGES below picks which live sections each page
shows. Only the hero moves (wave shader + rise-in); the content below is static.

Header, footer and contact form are lifted from about-us.html so the pages never drift
from it. The menu's Services and Development & Maintenance lists are written into
menu.js between the `<services:auto>` / `<dev:auto>` markers, so the dropdowns and the
pages always list the same services.
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from live_content import LIVE  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
e = html.escape
PHONE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.18 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.1 9.9a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z" />'
         '<path d="M15 2.5a6 6 0 0 1 6.5 6.5M15 6a2.5 2.5 0 0 1 3 3" /></svg>')
ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def slug(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower().replace('&', 'and')).strip('-')


L = LIVE

# Content Marketing has no page on the live site yet, so its copy below is written for the
# redesign — placeholders to replace when the real copy exists.
CONTENT = {
    'intro': 'Words, coverage and assets that get your brand found, quoted and shared — written for your audience in Dubai and across the GCC, in English and Arabic.',
    'items': [
        ('Website Copywriting', 'Homepages, service pages and landing pages written to rank and to convert: clear structure, search intent built in and a tone of voice that sounds like you.', []),
        ('Multimedia Content Assets', 'Video, graphics, guides and reports built to be shared — reusable assets that feed your website, social channels and sales conversations.', []),
        ('Digital PR', 'Stories and expert commentary placed in the publications your customers read, earning coverage and authority links that lift both reputation and search visibility.', []),
    ],
}
CONTENT_WHY = {'items': [
    ('Search-Led Topics', 'Every piece starts from what your customers actually search for, in English and Arabic.', []),
    ('Built to Convert', 'Clear structure, strong calls to action and copy aligned to each stage of your funnel.', []),
    ('Authority That Compounds', 'Digital PR and quality links that lift both your reputation and your rankings over time.', []),
    ('One Voice Everywhere', 'A tone of voice that stays consistent across your website, social channels and email.', []),
    ('Formats That Travel', 'Video, graphics and guides planned so one idea can be reused across every channel.', []),
    ('Measured, Not Guessed', 'Monthly reporting on traffic, rankings, engagement and leads, with next steps.', []),
]}
CONTENT_FAQ = [
    ('What is content marketing?', 'Planning, creating and distributing useful content — website copy, articles, video, graphics and PR — that attracts the right audience and turns them into customers.'),
    ('How does content marketing help SEO?', 'Search engines and AI assistants rank and quote pages that answer real questions well. Search-led content, clear structure and earned links all improve visibility.'),
    ('Do you write in Arabic and English?', 'Yes. We plan and write content in both languages, adapted for local audiences rather than translated word for word.'),
    ('How long before content shows results?', 'Most brands see engagement early, while organic traffic and leads build over three to six months as content and authority compound.'),
    ('Can you work alongside our in-house team?', 'Yes. We can own the full content plan or support your team with strategy, writing, design or PR where you need it.'),
]


def live(sec, title):
    """A service's description as written on the live page."""
    return next(d for t, d, _b in sec['items'] if t == title)


def find_live(title):
    """First live-content description for a service title, searched anywhere in the frozen live copy."""
    def walk(o):
        if isinstance(o, (list, tuple)):
            if len(o) >= 2 and o[0] == title and isinstance(o[1], str) and len(o[1]) > 40:
                return o[1]
            for x in o:
                r = walk(x)
                if r:
                    return r
        elif isinstance(o, dict):
            for x in o.values():
                r = walk(x)
                if r:
                    return r
    out = walk(L)
    assert out, title
    return out


def services(intro, *rows):
    """A page's service list — the same services, in the same order, as its header menu column."""
    return {'intro': intro, 'items': [(t, d, []) for t, d in rows]}


S, DS, SO, SE, GE, WB = L['branding']['services'], L['design']['services'], L['social'], L['seo']['services'], L['geo']['services'], L['web']
SVC = {
    'branding': services(S['intro'], *[(t, live(S, t)) for t in (
        'Brand Strategy & Positioning', 'Visual Identity Design', 'Brand Audit & Rebranding', 'Brand Experience & Touchpoints', 'Brand Collateral & Print Design')]),
    'design': services(DS['intro'],
        ('Web & App Design', 'Websites and mobile apps designed around your users. Our designers focus on intuitive navigation, visually appealing layouts and interactive elements, so every screen looks great and is effortless to use.'),
        ('Revamp Website', live(DS, 'Website Redesign & Revamp')),
        ('Ecommerce Website Design', live(DS, 'E-Commerce Design')),
        ('Social Media Design', live(SO['why'], 'Visual Excellence & Design Local Flavor')),
        ('Email Marketing Testing & Design', 'On-brand email templates designed to be read and clicked, then tested across inboxes, devices and dark mode before they go out.')),
    'social': services(SO['services']['intro'],
        ('Community Management', live(SO['why'], 'Engaged Community Building & Social Listening')),
        ('Content Creation Services', live(SO['services'], 'Social Media Content Creation')),
        ('Advertising & Media Services', 'Paid campaigns on Facebook, Instagram, TikTok, Snapchat, X and LinkedIn: targeting, creatives, budgets and reporting managed end to end, so every ad reinforces your brand and drives action.'),
        ('Social Media Event Management', live(SO['why'], 'Local Trends, Events & Seasonal Awareness'))),
    'paid': services(L['paid']['core']['intro'],   # keywords per row come from PAID_SUB
        ('PPC Agency', 'A Dubai PPC agency managing Google, Bing, Amazon and social campaigns end to end, with every dirham tied to leads and sales.'),
        ('Search & Display Advertising', 'Reach people the moment they search on Google and Bing, and stay visible across the Display Network.'),
        ('Shopping & Marketplace Advertising', 'Put your products in front of ready-to-buy shoppers on Google Shopping and Amazon.'),
        ('Social & App Advertising', 'Reach your audience where they scroll, and bring high-intent users to your app.'),
        ('Retargeting & Remarketing', live(L['paid']['services'], 'Remarketing & Retargeting Ads'))),
    'seo': services(SE['intro'],
        ('Search Engine Optimization', 'Our expert team drives organic traffic, improves search rankings and boosts online visibility, with technical, on-page and off-page SEO tailored to the competitive Dubai market.'),
        ('Technical SEO', live(SE, 'Technical SEO')),
        ('On-Page SEO', live(SE, 'On-Page SEO')),
        ('Off-Page SEO', live(SE, 'Off-Page SEO')),
        ('Local SEO', live(SE, 'Local SEO')),
        ('Enterprise SEO', 'SEO at scale for large and multi-location websites: site architecture, technical health and content programmes across thousands of pages, with reporting your stakeholders can act on.'),
        ('Ecommerce SEO', live(SE, 'E-Commerce SEO')),
        ('AI SEO Services', live(SE, 'AI SEO'))),
    'geo': services(GE['intro'],
        ('Generative AI Research and Analysis', live(GE, 'AI SEO Audit & Strategy')),
        ('Semantic Keywords Research', live(GE, 'AI-Backed Keyword Research & Targeting')),
        ('AI-Optimized Content', live(GE, 'Generative Content Optimization (GEO/AEO)')),
        ('Community Engagement Optimization', 'A helpful, genuine presence in the communities AI models learn from — Reddit, Quora and industry forums — so your brand is part of the conversations behind AI answers.'),
        ('Brand Visibility and Authority', live(GE, 'Link Building & Authority Development')),
        ('AI-Friendly Structured Data', live(GE, 'Technical SEO for AI Crawlers'))),
    # App Development has no live-site page: every description here except Ecommerce App Development is Claude-written (flag it)
    'app': services('Mobile apps people keep using: designed, built and supported for iOS, Android and the web, with the same care we put into every website.',
        ('iOS App Development', 'Native iPhone and iPad apps built in Swift and SwiftUI, designed to Apple’s guidelines and prepared for App Store review and release.'),
        ('Android App Development', 'Fast, reliable Android apps built in Kotlin, tested across the devices your customers use and published on Google Play.'),
        ('Cross-Platform App Development', 'One codebase for iOS and Android using Flutter or React Native, so you launch on both platforms sooner and maintain them together.'),
        ('Ecommerce App Development', find_live('Ecommerce App Development')),
        ('Progressive Web Apps (PWA)', 'App-like websites that load fast, work with weak connections and can be added to the home screen, without an app store.'),
        ('App Maintenance & Support', 'Updates for new iOS and Android releases, bug fixes, performance monitoring and store compliance, so your app stays stable after launch.')),
    'web': services(WB['services']['intro'], *[(t, d) for t, d, _b in WB['services']['items'][:9]],
                    ('Headless Ecommerce Development', find_live('Headless E-Commerce Development')),
                    ('Squarespace Website Development', find_live('Squarespace Development')),
                    ('Website Migration Services', find_live('Website Migration Services'))),
    # Website Management Services has no live-site copy: the description is Claude-written (flag it)
    'maintain': services(WB['maintain']['intro'], *[(t, d) for t, d, _b in WB['maintain']['items']],
                         ('Website Management Services', 'We run your website day to day, so you do not have to. Content updates, plugin and platform upgrades, performance, security and monthly reporting are handled by one team, with a single point of contact for every change.')),
}
SVC['content'] = CONTENT
# Paid Marketing's menu entries also say what each kind of advertising covers
PAID_SUB = {
    'PPC Agency': 'Google Ads · Bing Ads · Amazon PPC · Social Ads',
    'Search & Display Advertising': 'Google Search · Google Display · Bing Ads',
    'Shopping & Marketplace Advertising': 'Google Shopping · Shopping Feed Optimization · Amazon PPC',
    'Social & App Advertising': 'Social Ads · App Install Ads',
    'Retargeting & Remarketing': 'Retargeting · Remarketing Campaigns',
}


def panels(data, first, second):
    """Attach the two panel captions (bold lead, muted rest) to a service list."""
    return {**data, 'panels': [first, second]}


def pillars_of(*cols):
    """Approach pillars: (name, [points]) → the item shape the cards use."""
    return {'items': [(t, '', pts) for t, pts in cols]}


def items_only(data):
    """A live section without its intro paragraph (when the hero already says it)."""
    return {'items': data['items']}


# Every service page has the Branding page's structure: wave hero → services list (two
# panels) → approach pillars → why Squarezix → industries strip → FAQs → contact form.
# Copy comes from the matching live page; approach pillars on pages that have none live
# are grouped from that page's own services.
PAGES = [
    {
        'file': 'branding.html', 'badge': 'Branding',
        'title': 'Branding Agency in Dubai — Brand Strategy & Identity | Squarezix',
        'h1': ['A Brand People', 'Recognise, Remember', 'and Choose.'], 'grad': 1,
        'lead': 'Your brand is more than a logo — it’s the reason customers choose you over competitors. We craft identities that connect, convert and create lasting impressions.',
        'list': ('Branding services', 'Strategic brand building that drives <em>revenue &amp; recognition</em>', panels(SVC['branding'],
                 ('Strategy & identity.', 'Positioning, visual identity and audits that sharpen your brand.'),
                 ('Experience & collateral.', 'Every touchpoint and printed piece, designed to the same standard.'))),
        'sections': [
            ('pillars', 'Our approach', 'Our comprehensive branding <em>strategy pillars</em>', L['branding']['pillars']),
            ('why', 'Why Squarezix', 'How we stand out as the best <em>branding company</em> in Dubai', L['branding']['why']),
            ('industries', 'Industries', 'Brands we build <em>across industries</em>', L['branding']['industries']),
            ('faq', 'FAQs', 'Got questions about <em>branding services?</em>', L['branding']['faq'], 'We know branding services comes with a lot of questions. So we’ve unpacked them here, with answers straight from the experts at Squarezix.'),
        ],
    },
    {
        'file': 'design.html', 'badge': 'Design',
        'title': 'Website Design Company in Dubai — UI/UX & Web Design | Squarezix',
        'h1': ['Design That Looks Right', 'and Works', 'Even Better.'], 'grad': 1,
        'lead': 'Custom, user-friendly, responsive design tailored to your business goals: conversion-first and pixel-perfect on every screen.',
        'list': ('Design services', 'Web design company <em>in Dubai</em>', panels(SVC['design'],
                 ('Websites & apps.', 'Web, app, redesign and e-commerce design that converts.'),
                 ('Campaign design.', 'Social media creatives and tested email templates.'))),
        'sections': [
            ('pillars', 'Our approach', 'From research to <em>pixel-perfect launch</em>', pillars_of(
                ('Discover', ['Stakeholder interviews', 'User surveys & personas', 'Competitor audits', 'User journey mapping', 'Content strategy']),
                ('Design', ['Wireframing & prototyping', 'UI/UX design', 'Responsive web design', 'Interactive & animation design', 'Style guides & UI kits']),
                ('Deliver', ['Usability testing', 'Accessibility (WCAG)', 'Core Web Vitals focus', 'Conversion & CRO', 'Developer handover']))),
            ('why', 'Why Squarezix', 'What sets Squarezix apart in <em>website design</em>', items_only(L['design']['why'])),
            ('industries', 'Industries', 'Websites we design <em>across industries</em>', L['design']['industries']),
            ('faq', 'FAQs', 'Got questions about our <em>website design services?</em>', L['design']['faq'][:10], 'Everything you need to know before you start a website design project, answered by the designers who build them.'),
        ],
    },
    {
        'file': 'social-media-marketing.html', 'badge': 'Social Media Marketing',
        'title': 'Social Media Agency in Dubai — Social Media Marketing | Squarezix',
        'h1': ['Social Media', 'People Actually', 'Follow.'], 'grad': 1,
        'lead': 'Creative social media posts, data-driven strategies and results that make an impact across every platform your audience uses.',
        'list': ('Social media services', 'Social media marketing agency <em>in Dubai</em>', panels(SVC['social'],
                 ('Community & content.', 'A daily presence and content your audience wants to share.'),
                 ('Ads & events.', 'Paid media and event campaigns that drive action.'))),
        'sections': [
            ('pillars', 'Our approach', 'How we grow your <em>social presence</em>', pillars_of(
                ('Plan', ['Strategy development', 'Audience research & segmentation', 'Competitor analysis', 'Content calendars', 'Local events & seasons']),
                ('Create', ['Posts, reels & stories', 'Ad creatives', 'Influencer marketing', 'Arabic & English content', 'Platform-specific formats']),
                ('Grow', ['Account management', 'Community building', 'Paid + organic campaigns', 'Real-time monitoring', 'Analytics & reporting']))),
            ('why', 'Why Squarezix', 'Looking for a social media agency <em>that delivers?</em>', items_only(L['social']['why'])),
            ('industries', 'Industries', 'Brands we grow <em>across industries</em>', L['branding']['industries']),
            ('faq', 'FAQs', 'Have questions about our <em>social media services?</em>', L['social']['faq'], 'Platforms, timelines, costs and results — the questions brands ask us most about social media marketing in Dubai.'),
        ],
    },
    {
        'file': 'content-marketing.html', 'badge': 'Content Marketing',
        'title': 'Content Marketing in Dubai — Copywriting, Digital PR & Content | Squarezix',
        'h1': ['Content Built', 'to Be Found', 'and Shared.'], 'grad': 1,
        'lead': 'Words, coverage and assets that educate, persuade and convert, written to rank and built to be passed on.',
        'list': ('Content marketing services', 'Content built to be <em>found and shared</em>', panels(SVC['content'],
                 ('Content that converts.', 'Website copy and multimedia assets built to rank and be shared.'),
                 ('Coverage that builds authority.', 'Digital PR that earns mentions and links.'))),
        'sections': [
            ('pillars', 'Our approach', 'How we plan, create and <em>amplify content</em>', pillars_of(
                ('Plan', ['Audience & keyword research', 'Content strategy', 'Topic clusters', 'Editorial calendar', 'Tone of voice']),
                ('Create', ['Website copywriting', 'Blogs & long-form guides', 'Video & graphics', 'Reports & downloadables', 'Arabic & English copy']),
                ('Amplify', ['Digital PR', 'Media outreach', 'Authority links', 'Social distribution', 'Performance reporting']))),
            ('why', 'Why Squarezix', 'Why brands choose us for <em>content</em>', CONTENT_WHY),
            ('industries', 'Industries', 'Content for brands <em>across industries</em>', L['branding']['industries']),
            ('faq', 'FAQs', 'Questions about <em>content marketing?</em>', CONTENT_FAQ, 'How content marketing works, what it does for search and how we fit alongside your team — answered in one place.'),
        ],
    },
    {
        'file': 'paid-marketing.html', 'badge': 'Paid Marketing',
        'title': 'PPC Agency in Dubai — Google Ads & Paid Marketing | Squarezix',
        'h1': ['Paid Ads That', 'Pay for', 'Themselves.'], 'grad': 1,
        'lead': 'Google, Bing, Amazon and social campaigns planned around ROI: the right audience, the right message and every dirham tracked.',
        'list': ('Paid marketing services', 'Google Ads and paid search <em>that pays back</em>', panels(SVC['paid'],
                 ('Search & shopping.', 'Be there when people search, and when they are ready to buy.'),
                 ('Social & retargeting.', 'Reach new audiences on social and win back your visitors.'))),
        'sections': [
            ('pillars', 'Our approach', 'How we run <em>paid campaigns</em>', pillars_of(
                ('Plan', ['Keyword research & optimization', 'Audience targeting', 'Budget & bid strategy', 'Competitor ad analysis', 'Tracking & analytics setup']),
                ('Launch', ['Ad creation', 'Landing page optimization', 'Search & display campaigns', 'Shopping & Amazon ads', 'Remarketing campaigns']),
                ('Optimise', ['Quality Score', 'Bid management', 'A/B testing', 'Continuous optimization', 'Transparent ROI reporting']))),
            ('why', 'Why Squarezix', 'What makes Squarezix the best <em>pay-per-click agency</em> in Dubai', L['paid']['why']),
            ('industries', 'Industries', 'Campaigns for brands <em>across industries</em>', L['branding']['industries']),
            ('faq', 'FAQs', 'Have questions about <em>PPC campaigns?</em>', L['paid']['faq'][:10], 'Budgets, platforms and results — clear answers to the questions businesses ask us most about pay-per-click advertising.'),
        ],
    },
    {
        'file': 'seo-ai-visibility.html', 'badge': 'SEO & AI Visibility',
        'title': 'SEO Agency in Dubai — SEO & AI Search Visibility | Squarezix',
        'h1': ['The SEO Foundation', 'Everything Else', 'Stands On.'], 'grad': 1,
        'lead': 'Technical, on-page and off-page SEO that drives organic traffic, improves rankings and keeps them, in Dubai, the GCC and beyond.',
        'list': ('SEO services', 'SEO company <em>in Dubai</em>', panels(SVC['seo'],
                 ('Rank everywhere.', 'Core, local and enterprise SEO on solid technical foundations.'),
                 ('Sell & get cited.', 'E-commerce SEO and visibility in AI and LLM answers.'))),
        'sections': [
            ('pillars', 'Our approach', 'How we build <em>search visibility</em>', pillars_of(
                ('Audit', ['SEO audits', 'Competitor analysis', 'Technical SEO review', 'Keyword research', 'Local search review']),
                ('Optimise', ['On-page SEO', 'SEO content & blogging', 'E-commerce SEO', 'International SEO', 'Voice search SEO']),
                ('Grow', ['Off-page SEO', 'Ethical link building', 'AI SEO', 'Ongoing monitoring', 'Transparent reporting']))),
            ('why', 'Why Squarezix', 'Why businesses trust Squarezix as the best <em>SEO company</em> in Dubai', L['seo']['why']),
            ('industries', 'Industries', 'SEO for businesses <em>across industries</em>', L['seo']['industries']),
            ('faq', 'FAQs', 'Have questions about getting your site to <em>rank higher?</em>', L['seo']['faq'], 'Rankings, timelines and what SEO involves — straight answers from the team that does it every day.'),
        ],
    },
    {
        'file': 'geo.html', 'badge': 'GEO',
        'title': 'Generative Engine Optimization (GEO) & AI SEO in Dubai | Squarezix',
        'h1': ['Be the Answer', 'AI Engines', 'Quote.'], 'grad': 1,
        'lead': 'Structured, citable, conversational content, so ChatGPT, Gemini, Perplexity and AI Overviews recommend your brand.',
        'list': ('GEO services', 'Leading AI SEO <em>agency in Dubai</em>', panels(SVC['geo'],
                 ('Research & content.', 'How AI answers see you, the topics they need and content they quote.'),
                 ('Authority & structure.', 'Community presence, trusted mentions and machine-readable data.'))),
        'sections': [
            ('pillars', 'Our approach', 'Our comprehensive AI SEO <em>strategy pillars</em>', pillars_of(
                ('Technical', ['Website architecture optimization', 'Core Web Vitals', 'Structured data & schema markup', 'Crawlable by AI agents like GPTBot']),
                ('Content', ['Simple, conversational answers', 'Q&As, TL;DRs and bullet points', 'Logical heading structure', 'Arabic & English content']),
                ('Authority', ['Targeting LLM-cited sources', 'Quality backlinks', 'Domain authority', 'AI trust signals']),
                ('Formats', ['Blogs & long-form guides', 'Infographics & short visuals', 'Videos for AI search', 'YouTube, Instagram & TikTok']))),
            ('why', 'Why Squarezix', 'How Squarezix <em>stands out</em>', L['geo']['why']),
            ('industries', 'Industries', 'AI visibility <em>across industries</em>', L['geo']['industries']),
            ('faq', 'FAQs', 'Questions about <em>AI SEO in Dubai?</em>', L['geo']['faq'], 'Find the top questions and clear answers about our AI SEO services in Dubai, all in one place. If something’s missing, our team is just a message away.'),
        ],
    },
    {
        'file': 'website-development.html', 'menu': 'dev', 'badge': 'Website Development',
        'title': 'Web Development Company in Dubai | Squarezix',
        'h1': ['Websites Engineered', 'for Speed, Search', 'and Scale.'], 'grad': 1,
        'lead': 'Fast, accessible, SEO-ready builds on the platform that fits you, from first launch to migration.',
        'list': ('Development services', 'Best website development <em>agency in Dubai</em>', panels(SVC['web'],
                 ('Platforms & frameworks.', 'WordPress, e-commerce, React, Next.js and full-stack builds.'),
                 ('CMS & front-end.', 'Custom, headless and Concrete CMS, plus Vue.js interfaces.'))),
        'sections': [
            ('pillars', 'Our approach', 'From brief to <em>launch-ready build</em>', pillars_of(
                ('Plan', ['Requirements & discovery', 'Platform & stack selection', 'Information architecture', 'SEO-ready structure', 'Project roadmap']),
                ('Build', ['Front-end & CMS development', 'API development & integration', 'Payment gateway integration', 'Multi-language & localization', 'Security & pentesting']),
                ('Launch', ['Quality assurance & testing', 'Performance optimization', 'Website migration', 'Cloud & hosting setup', 'Maintenance & support']))),
            ('why', 'Why Squarezix', 'Why businesses trust us for <em>web development</em>', items_only(L['web']['why'])),
            ('industries', 'Industries', 'Websites for businesses <em>across industries</em>', L['web']['industries']),
            ('faq', 'FAQs', 'Ask. Click. <em>Done.</em>', L['web']['faq'][:10], 'Find the top questions and clear answers, all in one place. If something’s missing, our team is just a message away.'),
        ],
    },
    # App Development: no live page exists, so the copy below is Claude-written (flag it)
    {
        'file': 'app-development.html', 'menu': 'dev', 'badge': 'App Development',
        'title': 'Mobile App Development Company in Dubai | Squarezix',
        'h1': ['Apps Built to', 'Be Opened', 'Every Day.'], 'grad': 1,
        'lead': 'iOS, Android and cross-platform apps designed, built and supported by the same team behind your website.',
        'list': ('App development services', 'Mobile app <em>development in Dubai</em>', panels(SVC['app'],
                 ('Native & cross-platform.', 'iOS, Android, Flutter and React Native builds.'),
                 ('Commerce & web apps.', 'Ecommerce apps and progressive web apps, kept up to date after launch.'))),
        'sections': [
            ('pillars', 'Our approach', 'From idea to <em>app store launch</em>', pillars_of(
                ('Plan', ['Goals & user research', 'Platform choice', 'Feature roadmap', 'Wireframes & prototype', 'Technical architecture']),
                ('Build', ['UI design', 'iOS & Android development', 'API & backend integration', 'Payments & notifications', 'Security & testing']),
                ('Launch', ['App Store & Google Play release', 'Analytics setup', 'Performance monitoring', 'Updates & new OS support', 'Ongoing support']))),
            ('why', 'Why Squarezix', 'Why businesses choose us for <em>app development</em>', {'items': [
                ('Web and app, one team', 'Your website, app and marketing are planned together, so design, data and messaging stay consistent.', []),
                ('Built for the UAE market', 'Arabic and English interfaces, local payment methods and the habits of UAE users are designed in from the start.', []),
                ('Clear process and communication', 'Prototypes, milestones and regular demos keep you informed from the first sketch to release.', []),
                ('Support after launch', 'We keep your app updated for new devices and operating systems, and fix issues quickly.', [])]}),
            ('industries', 'Industries', 'Apps for businesses <em>across industries</em>', L['web']['industries']),
            ('faq', 'FAQs', 'Questions about <em>app development?</em>', [
                ('Which platforms do you build apps for?', 'iOS, Android and cross-platform apps using Flutter or React Native, plus progressive web apps.'),
                ('Should I build native or cross-platform?', 'Native apps suit performance-heavy or platform-specific products. Cross-platform apps suit most business apps and launch faster. We recommend one after reviewing your goals.'),
                ('Can you build an app for my online store?', 'Yes. We build ecommerce apps connected to Shopify, WooCommerce, Magento and custom stores.'),
                ('Will you publish the app on the App Store and Google Play?', 'Yes. We prepare your listings, handle review requirements and manage the release.'),
                ('Do you support the app after launch?', 'Yes. Maintenance plans cover updates, bug fixes, monitoring and compatibility with new OS versions.')],
             'Platforms, timelines and support: clear answers before you start building an app.'),
        ],
    },
    # Sub-inner page under Website Development. Its own design, section by section from the live
    # page; only the sections the inner pages also have (hero, strip, industries, FAQ, contact)
    # reuse their components. 'custom' = the sections below are the whole page.
    {
        'file': 'ecommerce-website-development.html', 'menu': 'dev', 'badge': 'Ecommerce Website Development', 'custom': True,
        'title': 'Ecommerce Website Development Company in Dubai | Squarezix',
        'h1': ['Online Stores', 'Built to Sell', 'and Scale.'], 'grad': 1,
        'lead': 'Shopify, WooCommerce, Magento and custom stores built for the UAE: Arabic and English, local payments and a fast, frictionless checkout.',
        'sections': [
            ('statement', 'AI search', 'Your customers search smarter. <em>We make sure they find you.</em>', L['ecom']['geo']),
            # Same layout as the inner pages' Why Squarezix: heading left, every platform with its live copy right
            ('nodes', 'Ecommerce platforms', 'Best ecommerce web development <em>company in Dubai</em>', L['ecom']['services'], 'services'),
            ('bento', 'Reliable Solutions', 'How Squarezix <em>stands out</em>', L['ecom']['why']),
            ('timeline', 'Development methodology', 'Our proven ecommerce <em>development workflow</em>', L['ecom']['workflow']),
            ('industries', 'Industries', 'Online stores <em>across industries</em>', L['ecom']['industries']),
            ('cta', 'Be everywhere your audience is <em>searching</em> with Squarezix', 'Connect with our AI experts to drive more leads from SEO in the AI era.'),
            ('faq', 'FAQs', 'Have questions about getting your ecommerce website to <em>rank higher?</em>', L['ecom']['faq'], 'Platforms, timelines, costs and payments — everything businesses ask us before building an ecommerce website in Dubai.'),
        ],
    },
    {
        'file': 'website-maintenance.html', 'menu': 'dev', 'badge': 'Website Maintenance',
        'title': 'Website Maintenance & Management Company in Dubai | Squarezix',
        'h1': ['A Website That', 'Stays Fast, Safe', 'and Up to Date.'], 'grad': 1,
        'lead': 'Monitoring, hosting, backups, security and on-demand edits, so your website keeps working while you run the business.',
        'list': ('Maintenance services', 'How we <em>maintain</em> your website', panels(SVC['maintain'],
                 ('Watched & backed up.', 'Uptime, hosting, backups and analytics, handled for you.'),
                 ('Secure & up to date.', 'SSL, content edits and speed tuning on demand.'))),
        'sections': [
            ('pillars', 'Our approach', 'How we keep your website <em>healthy</em>', pillars_of(
                ('Monitor', ['24/7 uptime monitoring', 'Website & traffic analytics', 'Broken links & forms checks', 'Backup monitoring', 'Transparent reporting']),
                ('Protect', ['Site security & SSL', 'Malware & vulnerability scans', 'CMS, plugin & theme updates', 'Weekly & monthly backups', 'Firewall setup']),
                ('Improve', ['Speed & performance optimization', 'Content updates & edits', 'Browser compatibility fixes', 'Payment & e-commerce fixes', 'Premium hosting performance']))),
            ('why', 'Why Squarezix', 'What sets Squarezix apart in <em>website maintenance</em>', items_only(L['web']['mwhy'])),
            ('industries', 'Industries', 'Websites we look after <em>across industries</em>', L['web']['industries']),
            ('faq', 'FAQs', 'Have questions about managing your <em>website effectively?</em>', L['web']['mfaq'], 'Care plans, security, backups and support — clear answers on keeping your website fast, safe and up to date.'),
        ],
    },
]

# Services with a sub-inner page of their own: their rows and menu entries open that page
SUBPAGES = {'Ecommerce Website Development': 'ecommerce-website-development.html'}

# Every other menu service gets a sub-inner page in the locked structure (subpages_content.py)
from subpages_content import SUBS, FAMILIES, WRITTEN  # noqa: E402
from iso_art import art as iso_art  # noqa: E402


def sub_page(sp):
    name, fam = sp['name'], FAMILIES[sp['parent']]
    file = slug(name) + '.html'
    nodes_data = {'intro': sp['intro'], 'items': [(t, d, {'tag': tag, 'kw': kw}) for t, tag, d, kw in sp['nodes']]}
    live = sp.get('live')
    if 'trust' in sp:
        # Pages with both live sections: the trust cards, then the stand-outs, each in full wording
        why_secs = [('bento', 'Why Choose Squarezix', f'Why businesses trust Squarezix for <em>{e(name)} services?</em>', sp['trust']),
                    ('bento', 'Why Squarezix', 'How Squarezix <em>stands out</em>', sp['stand'])]
    else:
        bento_data = {'feats': [(t, lead, chips, False) for t, lead, chips in sp['feats']], 'points': sp.get('points') or fam['why']}
        why_secs = [('bento', 'Why Squarezix', f'Why choose Squarezix for <em>{e(name)}</em>', bento_data)]
    flow = {'items': [(t, d, []) for t, d in (sp.get('flow') or fam['flow'])]}
    if sp.get('layout'):
        sections = sp['layout']
    elif live:
        sections = [
            ('bento', 'Why Choose Squarezix', f'Why businesses trust Squarezix for <em>{e(name)} services?</em>', sp['trust']),
            ('industries', live['ind'][0], live['ind'][1], sp.get('industries') or L['branding']['industries']),
            ('bento', 'Reliable Solutions', 'How Squarezix <em>stands out</em>', sp['stand']),
            ('nodes', 'Reliable Solutions', live['nodes_title'], nodes_data, 'services'),
            ('timeline', live['flow'][0], live['flow'][1], flow),
            ('cta', 'Be everywhere your audience is <em>searching</em> with Squarezix', live['cta_text']),
            ('faq', 'FAQs', live['faq_title'], sp['faq'], live['faq_intro']),
        ]
    else:
        sections = None
    return {
        'file': file, 'menu': fam['menu'], 'badge': sp.get('badge', name), 'custom': True, 'blog': live and live.get('blog'),
        'title': f'{name} in Dubai | Squarezix', 'h1': sp['h1'], 'grad': 1, 'lead': sp['lead'],
        'sections': sections or [
            ('statement', 'AI search', 'Your customers search smarter. <em>We make sure they find you.</em>', L['ecom']['geo']),
            ('nodes', 'What we deliver', f'What’s included in <em>{e(name)}</em>', nodes_data, 'services'),
            *why_secs,
            ('timeline', fam['flow_badge'], fam['flow_title'], flow),
            ('industries', 'Industries', 'Brands we work with <em>across industries</em>', sp.get('industries') or L['branding']['industries']),
            ('cta', 'Be everywhere your audience is <em>searching</em> with Squarezix', 'Connect with our AI experts to drive more leads from SEO in the AI era.'),
            ('faq', 'FAQs', f'Questions about <em>{e(name)}?</em>', sp['faq'],
             f'Clear answers to the questions businesses ask us most about {name}.'),
        ],
    }


for _sp in SUBS:
    _pg = sub_page(_sp)
    PAGES.append(_pg)
    SUBPAGES[_sp['name']] = _pg['file']


# Header menus: each column lists exactly its page's services (SVC), linking to each one.
def menu_items(page, key, subs=None):
    return [(t, SUBPAGES.get(t, f'{page}#{slug(t)}'), *([subs[t]] if subs else [])) for t, _d, _b in SVC[key]['items']]


MENU_TABS = [
    ('Digital Marketing', None, [
        ('Social Media', 'social-media-marketing.html', menu_items('social-media-marketing.html', 'social')),
        ('Content Marketing', 'content-marketing.html', menu_items('content-marketing.html', 'content')),
        ('Paid Marketing', 'paid-marketing.html', menu_items('paid-marketing.html', 'paid', PAID_SUB)),
    ]),
    # One column: the SEO and GEO services together; each item still opens its own page
    ('AI Search & SEO', None, [
        ('AI & Search Visibility', 'seo-ai-visibility.html',
         menu_items('seo-ai-visibility.html', 'seo') + menu_items('geo.html', 'geo')),
    ]),
    ('Branding & Design', 'branding.html', [
        ('Branding', 'branding.html', menu_items('branding.html', 'branding')),
        ('Design', 'design.html', menu_items('design.html', 'design')),
    ]),
]
# Its own header item after Services: one tab each for development and maintenance
DEV_TABS = [
    ('Website Development', 'website-development.html', [('Website Development', 'website-development.html', menu_items('website-development.html', 'web'))]),
    ('App Development', 'app-development.html', [('App Development', 'app-development.html', menu_items('app-development.html', 'app'))]),
    ('Website Maintenance', 'website-maintenance.html', [('Website Maintenance', 'website-maintenance.html', menu_items('website-maintenance.html', 'maintain'))]),
]


def hero(p):
    """The wave hero from the earlier service pages: badge, one-sentence headline with a
    serif-italic accent phrase, lead and one button, over the animated waves (waves-bg.js)."""
    headline = ' '.join(f'<em>{e(t)}</em>' if i == p['grad'] else e(t) for i, t in enumerate(p['h1']))
    return f'''    <!-- ===== Hero: animated wave gradient (waves-bg.js) behind badge, headline, lead and one button ===== -->
    <section class="svh" aria-labelledby="svp-hero-title">
      <canvas class="svh-waves" aria-hidden="true"></canvas>
      <div class="svh-inner">
        <span class="svc-badge ab-badge" data-rise>{e(p['badge'])}</span>
        <h1 id="svp-hero-title" class="svh-title" data-rise>{headline}</h1>
        <p class="svh-lead" data-rise>{e(p['lead'])}</p>
        <a href="#ab-contact" class="btn-contact btn-contact--xl svh-cta" data-rise>{PHONE} Contact us</a>
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


def head(badge, title, intro='', center=False):
    sub = f'<p class="ss-sub">{e(intro)}</p>' if intro else ''
    cls = 'ss-head ss-head--center' if center else 'ss-head'
    return f'<div class="{cls}"><span class="svc-badge">{e(badge)}</span><h2 class="ab-h2">{title}</h2>{sub}</div>'


def short(d, limit=110):
    """One line under a service's title: the first sentence of its live description."""
    first = re.split(r'(?<=[.!?])\s|(?<=[a-z][.])(?=[A-Z])', d, maxsplit=1)[0]
    if len(first) > limit:
        cut = first.split(' — ')[0].split('—')[0]
        first = cut if len(cut) <= limit else first[:limit].rsplit(' ', 1)[0].rstrip(',;:') + '…'
    return first


NE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'


def tags(t):
    """Keywords under a service (Paid Marketing's groups), the same ones its menu entry shows."""
    kw = PAID_SUB.get(t)
    return f'<span class="ss-row-tags">{"".join(f"<i>{e(k)}</i>" for k in kw.split(" · "))}</span>' if kw else ''


def listing(badge, title, data, sid='services'):
    """The long service list as two panels of rows (number, title, one line, arrow), each
    panel closed by a short caption — the structure of the reference design."""
    items = list(enumerate(data['items'], 1))
    half = (len(items) + 1) // 2
    caps = data.get('panels') or [('', ''), ('', '')]
    panels = ''
    for (bold, rest), chunk in zip(caps, (items[:half], items[half:])):
        rows = ''.join(
            f'<li id="{slug(t)}"><a class="ss-row" href="{SUBPAGES.get(t, "#ab-contact")}"><span class="ss-row-no">{i:02d}</span>'
            f'<span class="ss-row-txt"><b>{e(t)}</b>{f"<span>{e(short(d))}</span>" if d else ""}{tags(t)}</span>'
            f'<span class="ss-row-go">{NE}</span></a></li>'
            for i, (t, d, _b) in chunk)
        cap = f'<p class="ss-panel-cap"><b>{e(bold)}</b> {e(rest)}</p>' if bold else ''
        panels += f'<div class="ss-panel"><ol class="ss-rows">{rows}</ol>{cap}</div>'
    sub = f'<p class="ss-sub">{e(data["intro"])}</p>' if data.get('intro') else ''
    return f'''    <section class="ss-sec ss-list" id="{sid}">
      <div class="ss-list-head"><span class="svc-badge">{e(badge)}</span><h2 class="ab-h2">{title}</h2>{sub}</div>
      <div class="ss-panels">{panels}</div>
    </section>

'''


# Line icons for the approach cards (24px grid, stroked in CSS)
PILLAR_ICONS = {
    'Plan': '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2.2 5-4.8 2.2 2.2-5z"/>',
    'Create': '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13 7 4 4"/>',
    'Launch': '<path d="M9 15 6 12c1-4.5 4.5-8.5 12-9-.5 7.5-4.5 11-9 12z"/><path d="M6 15c-1.5 1.5-2 3.5-2 5 1.5 0 3.5-.5 5-2"/><circle cx="14.5" cy="9.5" r="1.5"/>',
    'Discover': '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.4-4.4"/>',
    'Design': '<path d="M12 3a9 9 0 1 0 0 18c1.2 0 1.8-.9 1.4-1.9-.5-1.2.3-2.1 1.5-2.1H17a4 4 0 0 0 4-4c0-5.5-4-10-9-10z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="15" cy="7.5" r="1"/>',
    'Deliver': '<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="m3 7.5 9 4.5 9-4.5M12 12v9"/>',
    'Grow': '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    'Amplify': '<path d="M4 10v4h3l6 4V6L7 10z"/><path d="M17 9a4 4 0 0 1 0 6M19.5 6.5a7.5 7.5 0 0 1 0 11"/>',
    'Optimise': '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
    'Audit': '<path d="M9 4h6v3H9z"/><path d="M15 5h3v16H6V5h3"/><path d="m9 13 2 2 4-4"/>',
    'Build': '<path d="m8 8-5 4 5 4M16 8l5 4-5 4M14 5l-4 14"/>',
    'Technical': '<path d="m8 8-5 4 5 4M16 8l5 4-5 4M14 5l-4 14"/>',
    'Content': '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 12h7M9 16h7"/>',
    'Authority': '<circle cx="12" cy="9" r="5.5"/><path d="m8.5 13.5-1.5 7.5 5-3 5 3-1.5-7.5"/>',
    'Formats': '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
    'Monitor': '<path d="M3 12h4l3-7 4 14 3-7h4"/>',
    'Protect': '<path d="M12 3 5 6v6c0 4.5 3 7.5 7 9 4-1.5 7-4.5 7-9V6z"/><path d="m9 12 2 2 4-4"/>',
    'Improve': '<path d="M12 21a9 9 0 1 1 9-9"/><path d="m12 12 5-5M17 7h-4M17 7v4"/>',
}


def pillars(badge, title, data):
    """Approach as infographic cards: a gradient tab with a pointer on top, then the card —
    icon on the left, a hairline, and the pillar's points on the right."""
    def card(t, b):
        ic = PILLAR_ICONS.get(t, '<circle cx="12" cy="12" r="9"/>')
        return (f'<li class="ss-pillar"><h3 class="ss-pillar-tab">{e(t)}</h3>'
                f'<div class="ss-pillar-body"><span class="ss-pillar-ic"><svg viewBox="0 0 24 24" aria-hidden="true">{ic}</svg></span>'
                f'<ul>{"".join(f"<li>{e(x)}</li>" for x in b)}</ul></div></li>')
    ps = ''.join(card(t, b) for t, _d, b in data['items'])
    return f'''    <section class="ss-sec">
      {head(badge, title, center=True)}
      <ol class="ss-pillars" style="--cols:{2 if len(data['items']) == 4 else 3}">{ps}</ol>
    </section>

'''


def why(badge, title, data, sid=None):
    rows = ''.join(f'<li><h3>{e(t)}</h3>{f"<p>{e(d)}</p>" if d else ""}</li>' for t, d, _b in data['items'])
    return f'''    <section class="ss-sec ss-why"{f' id="{sid}"' if sid else ''}>
      <div class="ss-why-side">{head(badge, title, data.get('intro', ''))}
        <a href="#ab-contact" class="btn-contact">{PHONE} Talk to our team</a>
      </div>
      <ul class="ss-why-list">{rows}</ul>
    </section>

'''


# Short name + descriptor for each live industry, shown in the looping strip
IND_SHORT = {
    'Marketing & Advertising Agencies': ('Marketing', 'Advertising agencies'),
    'Real Estate & Property Management': ('Real Estate', 'Property management'),
    'Logistics & Supply Chain Companies': ('Logistics', 'Supply chain companies'),
    'Healthcare & Wellness Enterprises': ('Healthcare', 'Wellness enterprises'),
    'SMEs and Growing Startups': ('Startups', 'SMEs and growing teams'),
    'Retail & E-commerce Businesses': ('Retail', 'E-commerce businesses'),
    'Fashion & Lifestyle Brands': ('Fashion', 'Lifestyle brands'),
    'Electronics & Technology Retailers': ('Electronics', 'Technology retailers'),
    'Luxury & Jewellery Brands': ('Luxury', 'Jewellery brands'),
    'Health, Beauty & Wellness': ('Beauty', 'Health & wellness'),
    'Automotive & Spare Parts': ('Automotive', 'Spare parts'),
    'Home Décor & Furniture': ('Home Décor', 'Furniture'),
}


def industries(badge, title, data):
    """Looping strip of industries, the same build as the footer's partner strip and the
    earlier service pages (outro.js clones the group and loops it)."""
    cells = ''.join(f'<li><strong>{e(IND_SHORT.get(t, (t, ""))[0])}</strong><span>{e(IND_SHORT.get(t, (t, ""))[1])}</span></li>'
                    for t, *_r in data['items'])
    return f'''    <section class="ss-sec">
      {head(badge, title, center=True)}
      <div class="szf-partners-row ss-ind-loop">
        <div class="szf-partners-track"><ul class="szf-partners-group">{cells}</ul></div>
      </div>
    </section>

'''


def faq(badge, title, qa, intro='', sid=None):
    def answer(a):
        out, bullets = [], []
        for line in a.split('\n'):
            if line.startswith('- '):
                bullets.append(f'<li>{e(line[2:])}</li>')
            elif line:
                out.append(f'<p>{e(line)}</p>')
        return ''.join(out) + (f'<ul>{"".join(bullets)}</ul>' if bullets else '')
    chev = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
    items = ''.join(f'<details class="ss-q"{" open" if i == 0 else ""}><summary><span>{e(q)}</span><i class="ss-q-icon">{chev}</i></summary>'
                    f'<div class="ss-a"><div class="ss-a-in">{answer(a)}</div></div></details>'
                    for i, (q, a) in enumerate(qa))
    # A full-width band in its own colour; one compact column of questions (faq.js animates them)
    return f'''    <div class="ss-faq-band"{f' id="{sid}"' if sid else ''}>
    <section class="ss-sec ss-faq">
      <div class="ss-faq-head"><span class="svc-badge">{e(badge)}</span><h2 class="ab-h2">{title}</h2>{f'<p class="ss-sub">{e(intro)}</p>' if intro else ''}</div>
      <div class="ss-faq-frame">
        <div class="ss-faq-list">{items}</div>
      </div>
      <a href="#ab-contact" class="btn-contact ss-faq-more">{PHONE} Still have questions? Ask us</a>
    </section>
    </div>

'''


def statement(badge, title, text):
    """One centred statement (the live page's AI-search intro)."""
    return f'''    <section class="ss-sec ec-statement">
      {head(badge, title, text, center=True)}
    </section>

'''


# Platform node cards: (mark, tag, keywords). Keywords are phrases from each platform's live copy.
PLATFORM_NODES = {
    'Shopify Development': ('Sh', 'Platform', ['Custom themes', 'Secure payments', 'Mobile-optimized']),
    'WooCommerce Development': ('Wc', 'Platform', ['WordPress', 'SEO-friendly', 'Plugin integrations']),
    'Custom Ecommerce Development': ('Cu', 'Custom build', ['UI/UX design', 'Backend architecture', 'Scalability']),
    'Magento Development': ('Mg', 'Enterprise', ['Multi-store', 'Advanced customization', 'Global growth']),
    'Laravel E-commerce Development (Custom-Built Solutions)': ('Lv', 'Custom build', ['Bespoke platform', 'Complex integrations', 'Long-term scalability']),
    'BigCommerce Development': ('Bc', 'Platform', ['Custom design', 'API integrations', 'High-volume sales']),
    'OpenCart Development': ('Oc', 'Platform', ['Multi-store', 'Payment integrations', 'Admin panels']),
    'Sitecore E-commerce Development': ('Sc', 'Enterprise', ['Personalization', 'Customer data insights', 'Targeted marketing']),
    'Ecommerce App Development': ('Ap', 'Mobile', ['Native iOS', 'Android', 'Hybrid', 'PWA']),
    'Headless E-Commerce Development': ('Hl', 'Headless', ['Next.js', 'Vue.js', 'Shopify Hydrogen']),
}


def auto_mark(t):
    """Two-letter mark for a card: initials of the first two main words, or a word's first two letters."""
    words = [w for w in re.findall(r'[A-Za-z0-9]+', t) if w.lower() not in {'and', 'of', 'for', 'the', 'to', 'in', 'a'}]
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper() if not words[0].isdigit() else words[0][:2]
    return (words[0][:2] if words else t[:2]).capitalize()


def nodes(badge, title, data, sid=None):
    """Why Squarezix layout (heading pinned left, one column scrolling right) with each item as a
    node card: tag on top, mark + title + menu, first sentence, the rest in a field box, keywords."""
    def card(t, d, meta):
        if isinstance(meta, dict):
            mark, tag, kws = auto_mark(t), meta.get('tag', 'Service'), meta.get('kw', [])
        else:
            mark, tag, kws = PLATFORM_NODES.get(t, (auto_mark(t), 'Service', []))
        lead, _, rest = d.partition('. ')
        lead = lead + ('.' if rest else '')
        box = f'<p class="ec-card-field">{e(rest)}</p>' if rest else ''
        chips = f'<ul class="ec-card-meta">{"".join(f"<li>{e(k)}</li>" for k in kws)}</ul>' if kws else ''
        close = f'<p class="ec-card-close">{e(meta["close"])}</p>' if isinstance(meta, dict) and meta.get('close') else ''
        return (f'<li class="ec-card" id="{idp}{slug(t)}"><span class="ec-card-tag"><i></i>{e(tag)}</span>'
                f'<div class="ec-card-body"><div class="ec-card-head"><span class="ec-card-mark">{e(mark)}</span><h3>{e(t)}</h3>'
                f'<i class="ec-card-menu" aria-hidden="true"></i></div><p class="ec-card-lead">{e(lead)}</p>{box}'
                f'{chips}{close}</div></li>')
    idp = f'{sid}-' if sid and sid != 'services' else ''
    cards = ''.join(card(t, d, b) for t, d, b in data['items'])
    return f'''    <section class="ss-sec ss-why"{f' id="{sid}"' if sid else ''}>
      <div class="ss-why-side">{head(badge, title, data.get('intro', ''))}
        <a href="#ab-contact" class="btn-contact">{PHONE} Talk to our team</a>
      </div>
      <ul class="ec-cards">{cards}</ul>
    </section>

'''


# Stand-out points that are really lists on the live page: shown as chips in larger cards
BENTO_FEATURES = [
    ('Secure Payment Gateway Integration in Dubai', 'Frictionless checkout with the payment options UAE shoppers use.',
     ['Apple Pay', 'Google Pay', 'Network International', 'CC Avenue', 'Tabby', 'Tamara'], 'wide'),
    ('Third-Party Integrations', 'A centralized, automated ecommerce ecosystem.',
     ['ERP systems', 'CRM platforms', 'POS systems', 'Shipping APIs', 'Inventory automation'], 'wide'),
    ('Multilingual & Multi-Currency Support', 'Fully localized for the region.', ['Arabic interface', 'English interface', 'Multi-currency'], ''),
    ('AI-Driven Search & Personalization', 'Help shoppers find the right product faster.',
     ['Smart filtering', 'Predictive search', 'Product recommendations', 'Behavior tracking'], ''),
    ('Mobile-First Architecture', 'Optimized layouts on every screen.', ['Smartphones', 'Tablets', 'Desktop'], ''),
]


# Ecommerce stand-outs: the live page's own wording, in the live order. Paragraph items keep their full text;
# list items show a lead line, the chips, then the closing sentence (as on the live page).
STAND_LISTS = {
    'Secure Payment Gateway Integration in Dubai': ('We integrate:', ['Apple Pay', 'Google Pay', 'Network International', 'CC Avenue', 'Tabby', 'Tamara'],
                                                    'Our payment gateway integration Dubai solutions ensure frictionless checkout experiences.'),
    'Third-Party Integrations': ('We connect your store with:', ['ERP systems', 'CRM platforms', 'POS systems', 'Shipping APIs', 'Inventory automation tools'],
                                 'This creates a centralized, automated ecommerce ecosystem.'),
    'Multilingual & Multi-Currency Support': ('UAE customers expect:', ['Arabic interface', 'English interface', 'Multi-currency support'],
                                              'We build fully localized ecommerce platforms tailored for the region.'),
    'AI-Driven Search & Personalization': ('', ['Smart filtering', 'Predictive search', 'Product recommendations', 'Customer behavior tracking'], ''),
    'Mobile-First Architecture': ('Optimized layouts across:', ['Smartphones', 'Tablets', 'Desktop'], ''),
}
STAND_LINKS = {'AI SEO Services': 'ai-seo-services.html', 'Ecommerce SEO': 'ecommerce-seo.html'}


def stand_card(title, text, extra=None):
    if isinstance(extra, dict) and extra.get('chips'):
        lead, chips, close = extra.get('lead', ''), extra['chips'], extra.get('close', '')
        body = (f'<p>{e(lead)}</p>' if lead else '') + f'<ul class="ec-chips">{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul>' + (f'<p class="ec-close">{e(close)}</p>' if close else '')
        return f'<li class="ec-feat ec-feat--chips{" ec-feat--full" if extra.get("wide") else ""}"><h3>{e(title)}</h3>{body}</li>'
    if isinstance(extra, dict) and extra.get('wide'):
        return f'<li class="ec-feat ec-feat--full"><h3>{e(title)}</h3><p>{e(text)}</p></li>'
    if title in STAND_LISTS:
        lead, chips, close = STAND_LISTS[title]
        body = (f'<p>{e(lead)}</p>' if lead else '') + f'<ul class="ec-chips">{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul>' + (f'<p class="ec-close">{e(close)}</p>' if close else '')
    else:
        para = e(text)
        for phrase, href in STAND_LINKS.items():
            para = para.replace(e(phrase), f'<a href="{href}">{e(phrase)}</a>', 1) if phrase in text else para
        body = f'<p>{para}</p>'
    return f'<li class="ec-feat"><h3>{e(title)}</h3>{body}</li>'


def bento(badge, title, data):
    """Stand-outs as a bento: feature cards with chips, then compact cards. Pages pass
    {'feats': [(title, lead, chips, wide)], 'points': [(title, text)]}; the ecommerce page builds
    them from its live stand-out list (BENTO_FEATURES + the remaining points)."""
    if 'items' in data and 'feats' not in data:
        cards = ''.join(stand_card(t, d, b) for t, d, b in data['items'])
        return f'''    <section class="ss-sec">
      {head(badge, title, data.get('intro', ''), center=True)}
      <ul class="ec-stand{' ec-stand--b5' if data.get('grid') == 'b5' else ''}">{cards}</ul>
    </section>

'''
    if 'feats' in data:
        feats_src, points = data['feats'], data['points']
    else:
        feats_src = BENTO_FEATURES
        taken = {t for t, *_r in BENTO_FEATURES}
        points = [(t, d) for t, d, _b in data['items'] if t not in taken]
    even = len(feats_src) % 2 == 0 and not any(w for *_r, w in feats_src)
    feats = ''.join(
        f'<li class="ec-feat{" ec-feat--wide" if (w or even) else ""}"><h3>{e(t)}</h3><p>{e(lead)}</p>'
        + (f'<ul class="ec-chips">{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul>' if chips else '') + '</li>'
        for t, lead, chips, w in feats_src)
    rest = ''.join(f'<li class="ec-point"><h3>{e(t)}</h3>{f"<p>{e(short(d, 150))}</p>" if d else ""}</li>' for t, d in points)
    return f'''    <section class="ss-sec">
      {head(badge, title, data.get('intro', ''), center=True)}
      <ul class="ec-bento">{feats}</ul>
      <ul class="ec-points">{rest}</ul>
    </section>

'''


def process_iso(badge, title, data, sid=None):
    """Steps as tilted isometric glass plates (left) with a glowing progress line; the chosen step's
    full content opens in a panel beside them. Panels are all in the HTML; px-process.js shows one."""
    items = data['items']
    tabs = ''.join(
        f'<button type="button" class="px-plate" role="tab" id="px-t-{i}" aria-controls="px-p-{i}" style="--i:{i}">'
        f'<b>{i + 1:02d}</b><span>{e(t)}</span><i class="px-stub" aria-hidden="true"></i></button>'
        for i, (t, _d, _m) in enumerate(items))
    panels = ''
    for i, (t, d, meta) in enumerate(items):
        lead, _, rest = d.partition('. ')
        lead = lead + ('.' if rest else '')
        field = f'<p class="px-field">{e(rest)}</p>' if rest else ''
        chips = f'<ul class="px-chips">{"".join(f"<li>{e(k)}</li>" for k in meta.get("kw", []))}</ul>' if meta.get('kw') else ''
        close = f'<p class="px-close">{e(meta["close"])}</p>' if meta.get('close') else ''
        panels += (f'<article class="px-panel" role="tabpanel" id="px-p-{i}" aria-labelledby="px-t-{i}">'
                   f'<span class="px-step">{e(meta.get("tag", "Step"))} <i>/ {len(items)}</i></span>'
                   f'<h3>{e(t)}</h3><p class="px-lead">{e(lead)}</p>{field}{chips}{close}</article>')
    return f'''    <section class="ss-sec px-sec"{f' id="{sid}"' if sid else ''}>
      {head(badge, title, data.get('intro', ''), center=True)}
      <div class="ss-head--center px-cta"><a href="#ab-contact" class="btn-contact">{PHONE} Talk to our team</a></div>
      <div class="px-stage" data-px style="--n:{len(items)}">
        <div class="px-iso">
          <div class="px-plane">
            <div class="px-tabs" role="tablist" aria-orientation="vertical" aria-label="{e(badge)} steps">{tabs}</div>
            <i class="px-trunk" aria-hidden="true"><i class="px-trunk-fill"></i><i class="px-node"></i></i>
          </div>
        </div>
        <div class="px-panels">{panels}</div>
      </div>
    </section>

'''


def compare(badge, title, data):
    """Muted 'problem' panel beside a dark, glowing 'our approach' panel with a keyword hub diagram.
    data: intro, left {dim, title, chips, link}, right {title, text, hub, keywords, tag, cta}"""
    import math
    L_, R_ = data['left'], data['right']
    x_icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>'
    chips = ''.join(f'<li>{x_icon}{e(c)}</li>' for c in L_['chips'])
    kws, parts = R_['keywords'], ''
    cx, cy, r = 340, 170, 74
    for i, k in enumerate(kws):
        a = -math.pi / 2 + i * 2 * math.pi / len(kws)
        c, sn = math.cos(a), math.sin(a)
        dx, dy = cx + r * c, cy + r * sn
        lx, ly = cx + 214 * c, cy + 138 * sn
        gx, gy = lx - 12 * c, ly - 12 * sn
        anc = 'middle' if abs(c) < .2 else ('start' if c > 0 else 'end')
        tx = lx + (10 if anc == 'start' else -10 if anc == 'end' else 0)
        ty = ly + (4 if abs(c) >= .2 else (-6 if sn < 0 else 16))
        parts += (f'<line x1="{dx:.1f}" y1="{dy:.1f}" x2="{gx:.1f}" y2="{gy:.1f}"/><circle class="d" cx="{dx:.1f}" cy="{dy:.1f}" r="2.6"/>'
                  f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anc}">{e(k)}</text>')
    check = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>'
    arrow_dn = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>'
    arrow_r = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
    return f'''    <section class="ss-sec cmp-sec">
      {head(badge, title, data.get('intro', ''), center=True)}
      <div class="cmp">
        <article class="cmp-panel cmp-panel--dim">
          <h3><span>{e(L_['dim'])}</span> {e(L_['title'])}</h3>
          <ul class="cmp-chips">{chips}</ul>
          <a href="{L_['link'][0]}" class="cmp-btn cmp-btn--dark">{arrow_dn}{e(L_['link'][1])}</a>
        </article>
        <article class="cmp-panel cmp-panel--hi">
          <h3>{e(R_['title'])}</h3>
          <p>{e(R_['text'])}</p>
          <svg class="cmp-orbit" viewBox="0 0 680 340" role="img" aria-label="{e(R_['hub'])}: {e(', '.join(kws))}"><circle class="r" cx="340" cy="170" r="74"/>{parts}<text class="ht" x="340" y="177" text-anchor="middle">{e(R_['hub'])}</text></svg>
          <div class="cmp-foot"><span class="cmp-tag">{check}{e(R_['tag'])}</span><a href="{R_['cta'][0]}" class="cmp-btn cmp-btn--light">{e(R_['cta'][1])} {arrow_r}</a></div>
        </article>
      </div>
    </section>

'''


def illus(badge, title, data):
    """Bento of illustration cards: an isometric line-light scene (scripts/iso_art.py) above each
    title and line. The first two cards are wide, the rest sit three to a row."""
    cards = ''.join(
        f'<li class="ix-card"><div class="ix-art">{iso_art(b["art"])}</div>'
        f'<div class="ix-copy"><h3>{e(t)}</h3><p>{e(d)}</p></div></li>'
        for t, d, b in data['items'])
    return f'''    <section class="ss-sec ix-sec">
      {head(badge, title, data.get('intro', ''), center=True)}
      <ul class="ix-grid">{cards}</ul>
    </section>

'''


FLOW_ICONS = [   # one line icon per workflow node, in step order
    '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.4-4.4"/>',
    '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
    '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 9v11"/>',
    '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13 7 4 4"/>',
    '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    '<path d="M9 15 6 12c1-4.5 4.5-8.5 12-9-.5 7.5-4.5 11-9 12z"/><path d="M6 15c-1.5 1.5-2 3.5-2 5 1.5 0 3.5-.5 5-2"/><circle cx="14.5" cy="9.5" r="1.5"/>',
]
# Wires between nodes (120 x 40 px boxes): right/left = direction of travel, down/up = to a lower/higher node
WIRES = {
    'rd': 'M0 0C60 0 60 40 120 40', 'ru': 'M0 40C60 40 60 0 120 0',
    'ld': 'M120 0C60 0 60 40 0 40', 'lu': 'M120 40C60 40 60 0 0 0',
}
FLOW_PATH = ['rd', 'ru', 'turn', 'ld', 'lu', None]   # 1→2→3 left to right, down to 4, then 4→5→6 back


def timeline(badge, title, data):
    """The workflow as a node graph on a dotted canvas: six step nodes in a snake (three across,
    then back), joined by wires with ports at both ends. Static; hover lights a node and its wire."""
    items = data['items']
    n = len(items)
    nodes = ''
    for i, (t, d, _b) in enumerate(items):
        w = FLOW_PATH[i] if i < len(FLOW_PATH) else None
        if w == 'turn':
            wire = '<svg class="ec-wire ec-wire--turn" viewBox="0 0 12 96" aria-hidden="true"><path d="M6 0V96"/><circle cx="6" cy="0" r="4"/><circle cx="6" cy="96" r="4"/></svg>'
        elif w:
            d_ = WIRES[w]
            nums = [float(x) for x in re.findall(r'[\d.]+', d_)]
            wire = (f'<svg class="ec-wire ec-wire--{w}" viewBox="0 0 120 40" aria-hidden="true"><path d="{d_}"/>'
                    f'<circle cx="{nums[0]:g}" cy="{nums[1]:g}" r="4"/><circle cx="{nums[-2]:g}" cy="{nums[-1]:g}" r="4"/></svg>')
        else:
            wire = ''
        nxt = (f'<span>Next</span><b>{e(items[i + 1][0])}</b>' if i + 1 < n else '<span>Output</span><b>Live store</b>')
        tag = '<span class="ec-node-tag">Start</span>' if i == 0 else ('<span class="ec-node-tag ec-node-tag--end">Launch</span>' if i == n - 1 else '')
        nodes += (f'<li class="ec-node">{tag}<div class="ec-node-head"><span class="ec-node-ic"><svg viewBox="0 0 24 24" aria-hidden="true">{FLOW_ICONS[i % len(FLOW_ICONS)]}</svg></span>'
                  f'<h3>{e(t)}</h3><i class="ec-node-dots" aria-hidden="true"></i></div>'
                  f'<div class="ec-node-box"><p class="ec-node-row"><span>Step</span><b>{i + 1:02d} / {n:02d}</b></p><p class="ec-node-desc">{e(d)}</p></div>'
                  f'<p class="ec-node-row ec-node-box ec-node-next">{nxt}</p>{wire}</li>')
    return f'''    <section class="ss-sec">
      {head(badge, title, center=True)}
      <div class="ec-canvas"><ol class="ec-flow">{nodes}</ol></div>
    </section>

'''


def cta(title, text):
    return f'''    <section class="ss-sec">
      <div class="ec-cta">
        <div><h2 class="ab-h2">{title}</h2><p>{e(text)}</p></div>
        <a href="#ab-contact" class="btn-contact btn-contact--xl">{PHONE} Speak to an expert</a>
      </div>
    </section>

'''


DIVIDER = '    <div class="ss-divider" aria-hidden="true"><i></i></div>\n\n'


def vs(badge, title, data):
    """Two panels side by side: the quieter 'other half' on the left, the page's own topic highlighted on the right."""
    dot = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>'

    def panel(cls, d):
        rows = ''.join(f'<li>{dot}{e(i)}</li>' for i in d['items'])
        note = f'<p class="cmp-note">{e(d["note"])}</p>' if d.get('note') else ''
        return f'<article class="cmp-panel {cls}"><h3>{e(d["title"])}</h3><ul class="cmp-chips">{rows}</ul>{note}</article>'
    return f'''    <section class="ss-sec cmp-sec">
      {head(badge, title, data.get('intro', ''), center=True)}
      <div class="cmp cmp--vs">{panel('cmp-panel--dim', data['left'])}{panel('cmp-panel--hi', data['right'])}</div>
    </section>

'''


KINDS = {'vs': vs, 'compare': compare, 'process': process_iso, 'illus': illus, 'nodes': nodes, 'statement': statement, 'bento': bento, 'timeline': timeline, 'cta': cta, 'pillars': pillars, 'why': why, 'industries': industries, 'faq': faq}


def main_html(p):
    secs = [] if p.get('custom') else [('main', listing(*p['list']))]
    for kind, *args in p['sections']:
        secs.append((kind, KINDS[kind](*args)))
    # The gradient divider between content sections
    out = hero(p)
    for i, (kind, html_) in enumerate(secs):
        if i and not {'faq', 'cta'} & {kind, secs[i - 1][0]}:   # FAQ band and CTA card separate themselves
            out += DIVIDER
        out += html_
    return f'  <main id="service" class="ss">\n{out}'


def menu_js(tabs_src):
    """Menu data for menu.js: tabs → columns → [{t, h}]."""
    tabs = [{'label': lab, 'page': page,
             'cols': [{'title': ct, 'page': cp, 'items': [{'t': it[0], 'h': it[1], **({'d': it[2]} if len(it) > 2 else {})} for it in items]}
                      for ct, cp, items in cols]}
            for lab, page, cols in tabs_src]
    return json.dumps(tabs, ensure_ascii=False, indent=2)


def live_blog(spec):
    """Blog block with the home page component's markup, used where the live page has its own post list (title and tag only)."""
    badge, title, posts = spec
    cards = ''.join(
        f'''<li>
        <a class="blog-card" href="https://squarezix.com/blogs/">
          <div class="blog-media"><img src="assets/blog/placeholder.webp" alt="" loading="lazy" /></div>
          <div class="blog-body">
            <div class="blog-meta"><span class="blog-tag">{e(tag)}</span></div>
            <h3>{e(t)}</h3>
            <span class="blog-more">Read more <i class="blog-arrow"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></i></span>
          </div>
        </a>
      </li>''' for tag, t in posts)
    return f'''    <section class="blog blog--live" id="blog" aria-labelledby="blog-title">
      <div class="blog-head">
        <span class="blog-badge">{e(badge)}</span>
        <h2 id="blog-title">{title}</h2>
      </div>
      <ul class="blog-list blog-list--4">
      {cards}
      </ul>
    </section>
'''


def body_probe(p):
    """True-ish text of the page's sections, used to decide which page scripts are needed."""
    return ' '.join('px-stage' for sec in p['sections'] if sec[0] == 'process')


def build():
    src = (ROOT / 'about-us.html').read_text()
    head_html, rest = src.split('<main', 1)
    main, tail = rest.split('</main>', 1)
    # Reuse the About contact block, without its scroll-in effects (these pages are static)
    contact = main[main.index('<section class="ab-contact"'):]
    contact = re.sub(r' data-(rise|reveal)(="[^"]*")?', '', contact)
    ver = re.search(r'about\.css(\?v=\w+)', head_html).group(1)
    home = (ROOT / 'index.html').read_text()
    blog = home[home.index('<section class="blog" id="blog"'):]
    blog = '    ' + blog[:blog.index('</section>') + len('</section>')] + '\n'
    for p in PAGES:
        h = re.sub(r'<title>.*?</title>', f'<title>{e(p["title"])}</title>', head_html, flags=re.S)
        h = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{e(p["lead"])}"', h)
        h = re.sub(r'(<link rel="stylesheet" href="about\.css[^>]*>)', rf'\1\n  <link rel="stylesheet" href="service-static.css{ver}" />', h)
        h = h.replace('<div class="nav-item is-current" data-menu="insights">', '<div class="nav-item" data-menu="insights">')
        cur = p.get('menu', 'services')
        h = h.replace(f'<div class="nav-item" data-menu="{cur}">', f'<div class="nav-item is-current" data-menu="{cur}">')
        extra = f'\n  <script src="px-process.js{ver}"></script>' if 'px-stage' in body_probe(p) else ''
        t = tail.replace('<script src="about.js', f'<script src="waves-bg.js{ver}"></script>\n  <script src="faq.js{ver}"></script>{extra}\n  <script src="about.js', 1)
        body = main_html(p)
        # "Our Blogs" from the home page, straight after the FAQ band
        faq_end = '</section>\n    </div>\n'
        i = body.index('ss-faq-band')
        j = body.index(faq_end, i) + len(faq_end)
        page_blog = live_blog(p['blog']) if p.get('blog') else blog
        body = body[:j] + '\n' + page_blog + '\n' + body[j:]
        (ROOT / p['file']).write_text(h + body + '    ' + contact + '</main>' + t)
        print('wrote', p['file'])
    # Menus: replace the generated blocks in menu.js
    mp = ROOT / 'menu.js'
    js = mp.read_text()
    for key, src in (('services', MENU_TABS), ('dev', DEV_TABS)):
        js, n = re.subn(rf'(// <{key}:auto>\n).*?(\n\s*// </{key}:auto>)', lambda m: m.group(1) + '      tabs: ' + menu_js(src).replace('\n', '\n      ') + ',' + m.group(2), js, flags=re.S)
        assert n == 1, f'menu.js is missing the <{key}:auto> markers'
    mp.write_text(js)
    print('updated menu.js menus')
    print(f'sub-inner pages: {len(SUBS) + 1}; Claude-written copy (no live page) on {len(WRITTEN)}:', ', '.join(WRITTEN))


if __name__ == '__main__':
    build()
