"""Copy for the sub-category pages (one page per dropdown tab).

Keyed by the parent page's menu key, then by that page's group id. The services listed on
each page come from the parent page's group in build_service_pages.py (which mirrors
menu.js); this file only adds what a sub-category page needs on top of that:

  file       output file name
  h1, grad   headline parts and which part is the serif-italic accent
  lead       hero paragraph
  statement  showcase sentence; {s0}, {s1}… mark where each service's image tile sits
  intro      paragraph under the showcase
  services   one entry per service, in the same order as the parent group:
             (short label for the dock, [what's included — three points])
"""

SUB = {
    'web': {
        'branding': {
            'file': 'branding.html',
            'h1': ['A Brand People', 'Recognise, Remember', 'and Choose.'], 'grad': 1,
            'lead': 'Your brand is more than a logo — it’s the reason customers choose you over competitors. We craft identities that connect, convert and create lasting impressions.',
            'statement': 'From {s0} strategy and {s1} identity to {s2} audits, {s3} touchpoints, {s4} print and {s5} content, one brand that holds <em>together.</em>',
            'intro': 'We start with context: market dynamics, competitor moves and consumer behaviour specific to Dubai and the GCC, then build a brand system that scales with you.',
            'services': [
                ('Strategy', ['Market and competitor research', 'Positioning framework', 'Messaging and tone of voice']),
                ('Identity', ['Logo system', 'Colour, type and iconography', 'Brand guidelines']),
                ('Audit', ['Brand asset audit', 'Gap analysis', 'Full or partial rebrand plan']),
                ('Touchpoints', ['Customer journey mapping', 'Physical and digital touchpoints', 'Arabic and English applications']),
                ('Print', ['Business cards and brochures', 'Packaging and signage', 'Pitch decks']),
                ('Content', ['Brand photography', 'Video', 'Brand copy']),
            ],
        },
        'designing': {
            'file': 'designing.html',
            'h1': ['Design That Looks Right', 'and Works', 'Even Better.'], 'grad': 1,
            'lead': 'Custom, user-friendly, responsive design tailored to your business goals: conversion-first and pixel-perfect on every screen.',
            'statement': 'One design team for your {s0} website, {s1} store, {s2} emails, {s3} app, {s4} quick launches and {s5} social, all in one visual <em>system.</em>',
            'intro': 'Design serves a strategy. We start with real research, prototype early and test with real users, so the final product is intuitive before development starts.',
            'services': [
                ('Website', ['UX wireframes', 'High-fidelity UI', 'Responsive layouts']),
                ('Store', ['Product-centric layouts', 'User-friendly navigation', 'Seamless checkout']),
                ('Email', ['On-brand templates', 'Tested across email clients', 'Reusable modules']),
                ('App', ['iOS and Android UX/UI', 'User flows', 'Finished screens']),
                ('Rapid', ['Launch-ready in two weeks', 'Focused scope', 'Built to extend later']),
                ('Social', ['Post and reel templates', 'Ad creative', 'One visual system']),
            ],
        },
        'development': {
            'file': 'development.html',
            'h1': ['Websites Engineered', 'for Speed, Search', 'and Scale.'], 'grad': 1,
            'lead': 'Fast, accessible, SEO-ready builds on the platform that fits you, from first launch to migration and ongoing care.',
            'statement': 'We {s0} look after, {s1} build, go {s2} headless, {s3} sell, {s4} scale and {s5} migrate, without losing a <em>ranking.</em>',
            'intro': 'Whether you want a traditional CMS or a headless setup, the build is engineered around your content and your editors, and kept healthy after launch.',
            'services': [
                ('Care', ['Updates and hosting', 'Monitoring and backups', 'Care plans']),
                ('Build', ['Front-end and CMS build', 'Performance and accessibility', 'SEO-ready structure']),
                ('Headless CMS', ['Sanity, Strapi, Contentful', 'Content separated from presentation', 'Fast and flexible']),
                ('Storefront', ['Shopify and WooCommerce', 'Custom storefronts', 'Built to sell']),
                ('Headless store', ['Shopify Hydrogen and Next.js', 'Fast browsing', 'Frictionless checkout']),
                ('Migration', ['Redirect planning', 'URL preservation', 'Content mapping']),
            ],
        },
    },
    'growth': {
        'social': {
            'file': 'social-media-marketing.html',
            'h1': ['Social Media', 'People Actually', 'Follow.'], 'grad': 1,
            'lead': 'Creative social media posts, data-driven strategies and results that make an impact across every platform your audience uses.',
            'statement': 'A {s0} community that talks back, {s1} content worth saving, {s2} ads that pay back and {s3} events people <em>remember.</em>',
            'intro': 'Every platform has its rules, strengths and audience expectations. We build one strategy and tune it for each, in Arabic and English.',
            'services': [
                ('Community', ['Replies and DMs', 'Reputation management', 'Social listening']),
                ('Content', ['Posts and graphics', 'Reels and stories', 'Brand-aligned copy']),
                ('Ads', ['Audience targeting', 'Campaigns on Facebook, Instagram, TikTok, Snapchat, LinkedIn and X', 'Performance tracking']),
                ('Events', ['Launch planning', 'Live coverage', 'On-channel activations']),
            ],
        },
        'content': {
            'file': 'content-marketing.html',
            'h1': ['Content Built', 'to Be Found', 'and Shared.'], 'grad': 1,
            'lead': 'Words, coverage and assets that educate, persuade and convert, written to rank and built to be passed on.',
            'statement': 'Three ways to earn attention: {s0} copy that converts, {s1} coverage that builds authority and {s2} assets worth <em>sharing.</em>',
            'intro': 'Content must do more than attract visits. We plan it around what your audience is searching for and what moves them to act.',
            'services': [
                ('Copy', ['Website and landing page copy', 'Written to convert and rank', 'Arabic and English']),
                ('PR', ['Press coverage', 'Authority links', 'Media relations']),
                ('Assets', ['Video', 'Graphics and infographics', 'Guides built to be shared']),
            ],
        },
    },
    'ai': {
        'seo': {
            'file': 'core-seo.html',
            'h1': ['The SEO Foundation', 'Everything Else', 'Stands On.'], 'grad': 1,
            'lead': 'Technical, on-page and off-page SEO that drives organic traffic, improves rankings and keeps them, in Dubai, the GCC and beyond.',
            'statement': 'SEO at every scale: {s0} enterprise sites, {s1} online stores, {s2} local search, {s3} AI answers and the {s4} full <em>foundation.</em>',
            'intro': 'SEO is not set and forget. We track algorithm changes, competitor moves and performance shifts, and keep refining so rankings last.',
            'services': [
                ('Enterprise', ['Large-site architecture', 'Templates at scale', 'Crawl budget management']),
                ('E-commerce', ['Product and category pages', 'Structured data for products', 'Faceted navigation']),
                ('Local', ['Google Business Profile', 'Citations in UAE directories', 'Reviews and geo-targeted content']),
                ('AI & LLM', ['Citable content structure', 'AI crawler access', 'Citation tracking']),
                ('Foundation', ['Technical SEO', 'On-page optimisation', 'Off-page authority']),
            ],
        },
        'generative': {
            'file': 'generative-search.html',
            'h1': ['Be the Answer', 'AI Engines', 'Quote.'], 'grad': 1,
            'lead': 'Structured, citable, conversational content, so ChatGPT, Gemini, Perplexity and AI Overviews recommend your brand.',
            'statement': 'Getting cited takes {s0} research, {s1} the right keywords, {s2} quotable content, {s3} community presence, {s4} authority and {s5} clean <em>data.</em>',
            'intro': 'AI search rewards clear structure, credible sources and consistent mentions. We work on all three, in English and Arabic.',
            'services': [
                ('Research', ['How AI answers describe you today', 'Competitor visibility', 'Gap analysis']),
                ('Keywords', ['Topics and entities', 'Search intent mapping', 'Question research']),
                ('Content', ['Q&A sections and summaries', 'Logically structured headings', 'Examples and statistics']),
                ('Community', ['Reddit and Quora presence', 'Forum engagement', 'Authentic participation']),
                ('Authority', ['Brand mentions', 'Backlinks from trusted sources', 'LLM-cited publications']),
                ('Data', ['Schema markup', 'Structured data', 'Machine-readable facts']),
            ],
        },
    },
}
