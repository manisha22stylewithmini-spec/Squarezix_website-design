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

PAGES = [
    {
        'file': 'web-and-brand.html', 'menu': 'web', 'badge': 'Web & Brand',
        'title': 'Web & Brand — Branding, Web Design & Development | Squarezix',
        'desc': 'Brand strategy, identity, website design and development from one Dubai team. Websites designed to convert, scale and rank.',
        'h1': ['Professional Web Design', 'That Turns Clicks', 'into Customers.'], 'grad': 1,
        'lead': 'Your website shouldn’t just look good, it should drive measurable growth. We craft brand identities that connect and build websites designed to convert, scale and rank.',
        'screen': 'Rec · CH 03', 'region': 'Brand · Design · Build',
        'intro': ('What we do', 'Strategic brand building, <em>designed and built</em> to perform',
                  'Your brand is more than a logo — it’s the reason customers choose you over competitors. From brand strategy and visual identity to the site that carries it, one team does the whole job.'),
        'groups': [
            ('branding', 'Branding', 'Identities that connect, convert and create lasting impressions.', [
                ('Brand Strategy & Positioning', 'We define who you are, who you serve, and why you win. Market research, competitor audits and positioning frameworks that carve out your irreplaceable space.'),
                ('Visual Identity Design', 'Logo systems, colour palettes, typography, iconography and brand guidelines — every visual touchpoint crafted to be instantly recognisable. No templates. No generic outputs.'),
                ('Brand Naming & Messaging', 'Names that stick. Taglines that sell. Messaging frameworks that align every piece of communication — from your homepage headline to your sales deck.'),
                ('Brand Audit & Rebranding', 'We forensically audit every brand asset, identify gaps and lead full or partial rebrands that modernise without losing the equity you’ve spent years building.'),
                ('Brand Experience & Touchpoints', 'Every interaction your customer has with your brand is a chance to build trust or lose it. We map, design and optimise every physical and digital touchpoint.'),
                ('Brand Collateral & Print Design', 'Business cards, brochures, pitch decks, packaging and signage — tangible brand assets designed to the same uncompromising standard as your digital presence.'),
            ]),
            ('designing', 'Designing', 'Custom, user-friendly, responsive websites tailored to your business goals.', [
                ('UI/UX Design', 'User-centric design that enhances usability and engagement: intuitive navigation, visually appealing layouts and interactive elements.'),
                ('Wireframing & Prototyping', 'Low- and high-fidelity prototypes that visualise layouts, page hierarchy and user interactions before a line of code is written.'),
                ('Responsive Web Design', 'Websites that adapt fluidly to desktops, tablets and mobile screens, with usability, fast loading and consistency on every device.'),
                ('E-Commerce Design', 'Online stores that are visually appealing and conversion-driven: user-friendly navigation, product-centric layouts and seamless checkout.'),
                ('Landing Page Design', 'High-impact landing pages for marketing campaigns, product launches and lead generation, with strategic CTAs and clean layouts.'),
                ('SaaS & Dashboard UI Design', 'Clean, organised dashboards with user-friendly layouts, visual data representation and easy navigation.'),
            ]),
            ('development', 'Development', 'Fast, accessible, SEO-ready builds on the platform that fits you.', [
                ('Website Development', 'Fast, accessible, SEO-ready websites engineered around your content and your editors.'),
                ('Headless CMS Development', 'Sanity, Strapi and Contentful builds that separate content from presentation, so your site stays fast and flexible.'),
                ('E-commerce Website Development', 'Shopify, WooCommerce and custom storefronts built to sell.'),
                ('Headless E-commerce Development', 'Shopify Hydrogen and Next.js storefronts for fast browsing and frictionless checkout.'),
                ('Website Migration Services', 'Move platforms and keep your rankings: redirect planning, URL preservation and content mapping.'),
                ('Website Management', 'Updates, hosting and care plans that keep the site healthy after launch.'),
            ]),
        ],
        'pillars': ('Our approach', 'Our comprehensive branding <em>strategy pillars</em>', [
            ('Plan', ['Brand Launch Strategy', 'Social Media Strategy', 'Brand Messaging Framework', 'Campaign Strategy', 'Launch Event Planning']),
            ('Create', ['Brand Identity', 'Brand Guidelines', 'Brand Logo', 'Brand Marketing Assets', 'Brand Creatives']),
            ('Launch', ['Brand Management', 'Social Media Management', 'Launch Event Management', 'Public Relations', 'Media Relations']),
        ]),
        'why': ('Why Squarezix', 'What sets Squarezix <em>apart</em>', [
            ('Research-Led Design (Not Guesswork)', 'We start every project with real research: stakeholder interviews, user surveys, persona creation, competitor audits and user journey mapping.'),
            ('Strategy First — Design Second', 'Design serves a strategy. We align every page and interaction to business goals: lead gen, sign-ups, product sales, brand lift.'),
            ('Conversion & CRO Built-In', 'Conversion Rate Optimization is part of the design process, not an afterthought. We wireframe and A/B test variants, and use heatmaps and analytics insights.'),
            ('Performance & Core Web Vitals Focus', 'Fast sites convert better. We design with performance in mind — lightweight layouts, optimized imagery, sensible animations.'),
            ('Culturally Fluent, Arabic-First Thinking', 'Brands in Dubai must function in Arabic and English. We design identities and messaging with Arabic-first typography, RTL layouts and culturally sensitive storytelling.'),
            ('Accessibility & Inclusive UX', 'Accessibility isn’t a checkbox — it’s good design. We follow WCAG best practices: semantic HTML, ARIA roles, keyboard navigation and colour contrast.'),
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
        'intro': ('What we do', 'Campaigns that build <em>brand loyalty</em> and generate leads',
                  'We specialise in creating impactful campaigns that drive engagement, build brand loyalty and generate leads across all major platforms.'),
        'groups': [
            ('social', 'Social Media Marketing', 'A consistent, authentic presence on every platform your audience uses.', [
                ('Social Media Strategy & Planning', 'Competitor analysis, audience research and content planning to design campaigns that maximise reach, engagement and ROI.'),
                ('Social Media Content Creation', 'Posts, graphics, videos, stories and reels that reflect your brand identity and resonate with your audience.'),
                ('Social Media Account Management', 'Posting schedules, content updates, engagement with followers and performance monitoring, handled for you.'),
                ('Community Management', 'We start conversations, respond to feedback, manage reputation and monitor what people say about your brand.'),
                ('Multi-Platform Campaign Management', 'Cohesive strategy, optimised targeting and synchronised creative across Facebook, Instagram, TikTok, LinkedIn and YouTube.'),
                ('Influencer Marketing', 'We connect you with the right influencers in your industry to promote your brand and drive meaningful engagement.'),
            ]),
            ('paid', 'Advertising & Media', 'Paid campaigns with precise targeting and performance tracking.', [
                ('Facebook Ads', 'Highly targeted campaigns using advanced audience segmentation, retargeting strategies and carousel, video and lead formats.'),
                ('Instagram Ads', 'Visually compelling ads for Instagram Stories, Reels and Feed posts, with precise targeting and performance tracking.'),
                ('TikTok Ads', 'Engaging, trend-driven short-form video campaigns that capture attention and drive conversions.'),
                ('Snapchat Ads', 'Snap Ads, story ads and AR filter campaigns that reach younger demographics through creative storytelling.'),
                ('LinkedIn Ads', 'Sponsored content, InMail and text ads targeting decision-makers and industry professionals for B2B leads.'),
                ('X Ads (Twitter)', 'Promoted posts, video ads and follower campaigns targeting users by interest, keywords and location.'),
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
        'why': ('Why Squarezix', 'A social media agency that <em>delivers</em>', [
            ('Culturally Tuned Content That Resonates', 'We create content in Arabic and English, adapt messaging for local customs, and design visuals that appeal to the region.'),
            ('Data-First Strategy & Audience Segmentation', 'We don’t guess who your audience is. We use analytics, audience insights and social listening tools to define who your customers are, what platforms they use, and when they engage.'),
            ('Integrated Paid + Organic Approach', 'We deliver both — blending organic content that builds trust with paid campaigns that drive action.'),
            ('Platform-Specific Expertise & Format Mastery', 'Every social platform has its rules, strengths and audience expectations. We know how to unlock growth on Instagram, TikTok, LinkedIn, Facebook, YouTube and Snapchat.'),
            ('Local Trends, Events & Seasonal Awareness', 'Dubai is a city of events, seasons and festivals. We integrate relevant local events into content calendars and campaigns.'),
            ('Transparent Insights & Consistent Reporting', 'Regular reports with clear metrics: reach, engagement, follower growth, conversion paths, ad spend ROI. We explain not just what happened but why, and what we’ll do next.'),
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
        'intro': ('What we do', 'Be everywhere your audience <em>is searching</em>',
                  'We don’t just optimise for Google — we optimise your brand for ChatGPT, Gemini, Perplexity and the AI answers your customers now read first.'),
        'groups': [
            ('seo', 'Core SEO', 'The technical, on-page and off-page foundation everything else stands on.', [
                ('SEO Audits', 'A comprehensive audit of on-page, off-page and technical factors, with detailed recommendations to improve visibility, performance and ROI.'),
                ('Technical SEO', 'Site architecture, XML sitemaps, robots.txt, site speed, mobile-friendliness, structured data and indexing issues.'),
                ('On-Page SEO', 'Meta tags, headings, keyword placement, image optimisation, internal linking and content structuring.'),
                ('Local SEO', 'Google Business Profile optimisation, citations across trusted UAE directories, reviews and geo-targeted content.'),
                ('E-Commerce SEO', 'If you’re running an online store in the UAE, your website needs more than attractive products — it needs visibility.'),
                ('Link Building', 'A robust and diverse backlink profile built on relevance, authority and compliance.'),
            ]),
            ('generative', 'Generative Search', 'Structured, citable, conversational content that AI engines quote.', [
                ('AI SEO Audit & Strategy', 'A comprehensive AI-powered audit to identify ranking opportunities, technical gaps and LLM citation potential.'),
                ('Generative Content Optimization (GEO/AEO)', 'Structured, citable and conversational content optimised for AI search engines, chatbots and voice assistants.'),
                ('Technical SEO for AI Crawlers', 'Website architecture, Core Web Vitals, schema markup and site speed, so AI bots and search engines can crawl, index and understand your content.'),
                ('AI-Backed Keyword Research & Targeting', 'High-intent, revenue-driving keywords based on real-time search patterns, LLM citation opportunities and competitor analysis.'),
                ('Link Building & Authority Development', 'High-quality backlinks from authoritative domains, including sources recognised by AI engines.'),
                ('AI Performance Reporting & Analytics', 'Real-time dashboards tracking AI visibility, keyword rankings, citation frequency and ROI.'),
            ]),
        ],
        'pillars': ('Our approach', 'Our comprehensive AI SEO <em>strategy pillars</em>', [
            ('Technical foundation', ['Website architecture optimisation', 'Core Web Vitals', 'Structured data & schema markup', 'Crawlable by GPTBot and search engines']),
            ('Content for generative search', ['Simple, conversational content', 'Q&A sections and TL;DR summaries', 'Logically structured headings', 'English and Arabic']),
            ('AI authority', ['Targeting LLM-cited sources', 'Quality backlinks', 'Authoritative, relevant domains', 'Stronger AI trust signals']),
            ('Multiple formats', ['Blogs and long-form guides', 'Infographics and short-form visuals', 'Videos optimised for AI search', 'Featured in AI Overviews']),
        ]),
        'why': ('Why Squarezix', 'How Squarezix <em>stands out</em>', [
            ('AI-Driven Strategy Tailored for Dubai Markets', 'Real-time AI insights build custom AI SEO strategies aligned with Dubai’s fast-moving digital landscape.'),
            ('Predictive AI SEO for Faster Results', 'Our AI systems forecast ranking shifts, competitor movements and search trend changes, so we optimise ahead of time.'),
            ('Hyper-Personalized Keyword Targeting', 'Instead of generic keyword lists, we use AI to identify intent-based, commercial, high-value keywords tailored to your industry.'),
            ('Real-Time Competitor Monitoring', 'We track your competitors’ AI SEO strategies using AI-powered tools, allowing us to counter new movements and maintain your ranking advantage.'),
            ('Multilingual SEO & Arabic-First Content', 'We build content strategies and implementations that are inherently bilingual (Arabic + English), or multilingual when needed.'),
            ('Transparent, Data-Rich Reporting', 'Dashboards that deliver clear insights — keyword improvements, traffic trends, competitor gaps and opportunities that drive real business growth.'),
        ]),
        'steps': [('Audit', 'Technical gaps, ranking opportunities and LLM citation potential.'), ('Structure', 'Architecture, schema and Core Web Vitals for crawlers and AI bots.'),
                  ('Publish', 'Citable, conversational content in the formats AI engines quote.'), ('Monitor', 'Rankings, AI visibility and citation frequency, tracked continuously.')],
    },
]

e = html.escape


def main_html(p):
    grad = ' class="ab-grad"'
    lines = ''.join(f'<span{grad if i == p["grad"] else ""}>{e(t)}</span>' for i, t in enumerate(p['h1']))
    groups = ''
    for n, (gid, name, blurb, cards) in enumerate(p['groups'], 1):
        items = ''.join(f'<li class="svp-card" data-rise><span class="svp-card-no">{n:02d}.{i:02d}</span><h4>{e(t)}</h4><p>{e(d)}</p></li>'
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
    wb, wt, wl = p['why']
    why = ''.join(f'<li class="svp-why-row" data-rise><span>{i:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(wl, 1))
    steps = ''.join(f'<li class="ab-step" data-rise><span class="ab-step-num">{i:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(p['steps'], 1))
    inds = ''.join(f'<li>{e(x)}</li>' for x in INDUSTRIES)
    ib, it, ip = p['intro']
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

    <!-- ===== Services, grouped the same way as this item's dropdown ===== -->
    <section class="svp-services" id="services" aria-labelledby="svp-services-title">
      <div class="svp-head">
        <div>
          <span class="svc-badge" data-rise>{e(ib)}</span>
          <h2 id="svp-services-title" class="ab-h2 ab-reveal" data-reveal>{it}</h2>
        </div>
        <p class="svp-aside" data-rise>{e(ip)}</p>
      </div>
      <nav class="svp-jump" aria-label="Service groups" data-rise>{jump}</nav>{groups}
    </section>

    <!-- ===== Approach ===== -->
    <section class="svp-pillars" aria-labelledby="svp-pillars-title">
      <div class="ab-head ab-center">
        <span class="svc-badge" data-rise>{e(pb)}</span>
        <h2 id="svp-pillars-title" class="ab-h2 ab-reveal" data-reveal>{pt}</h2>
      </div>
      <ol class="svp-pillar-list" style="--n:{len(pl)}">{pillars}</ol>
    </section>

    <!-- ===== Why Squarezix ===== -->
    <section class="svp-why" aria-labelledby="svp-why-title">
      <div class="svp-why-head">
        <span class="svc-badge" data-rise>{e(wb)}</span>
        <h2 id="svp-why-title" class="ab-h2 ab-reveal" data-reveal>{wt}</h2>
        <p class="svp-ind-label" data-rise>Industries we work with</p>
        <ul class="svp-ind" data-rise>{inds}</ul>
      </div>
      <ol class="svp-why-list">{why}</ol>
    </section>

    <!-- ===== Process (same track as the About page) ===== -->
    <section class="ab-process" aria-labelledby="svp-process-title">
      <div class="ab-head ab-center">
        <span class="svc-badge" data-rise>How We Work</span>
        <h2 id="svp-process-title" class="ab-h2 ab-reveal" data-reveal>A process that’s <em>boringly reliable</em></h2>
        <p class="ab-sub" data-rise>No surprises. No scope creep. Every engagement follows the same four-phase system.</p>
      </div>
      <ol class="ab-steps" id="ab-steps">{steps}</ol>
    </section>

'''


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
        (ROOT / p['file']).write_text(h + main_html(p) + '    ' + contact + '</main>' + tail)
        print('wrote', p['file'])


if __name__ == '__main__':
    build()
