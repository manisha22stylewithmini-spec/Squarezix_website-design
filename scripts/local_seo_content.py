"""Local SEO page: the live squarezix.com/local-seo-services/ wording, mapped onto the existing components.

Each tuple is a section as build_service_pages.py expects it:
  ('bento',  badge, title, {'intro': str, 'items': [(title, text, extra)]})   extra: {'lead','chips','close','wide'}
  ('nodes',  badge, title, {'intro': str, 'items': [(title, text, {'tag','kw','close'})]}, section_id)
  ('statement', badge, title, text) · ('cta', title, text) · ('faq', badge, title, [(q, a)])
"""


def node(title, tag, text, chips, close=''):
    return (title, text, {'tag': tag, 'kw': chips, **({'close': close} if close else {})})


PROBLEMS = ['Low Google Maps visibility', 'Competitors dominating the Local 3-Pack', 'Poor rankings outside your immediate location',
            'Inconsistent business information online', 'Weak Google Business Profile engagement', 'Limited visibility for “near me” searches',
            'Insufficient customer reviews', 'Poor neighborhood-specific rankings', 'Low phone and WhatsApp enquiries',
            'Missed visibility across AI search platforms']

EXPECT = [
    ('Stronger Google Maps Visibility', 'Build your presence for commercially valuable searches across your priority areas.'),
    ('Optimized Google Business Profile', 'Improve profile relevance, completeness, accuracy, and customer engagement.'),
    ('Geo-Grid Ranking Intelligence', 'See exactly where your business ranks across multiple GPS points—not just from one location.'),
    ('More Qualified Local Leads', 'Create clearer paths from search to phone calls, WhatsApp enquiries, forms, bookings, and visits.'),
    ('Stronger Local Authority', 'Improve citations, reviews, local backlinks, entity signals, and neighborhood relevance.'),
    ('Local 3-Pack Optimization', 'Strengthen the signals that help your business compete for Google’s prominent local results.'),
    ('Location-Based SEO Growth', 'Target relevant Dubai communities with strategically developed location landing pages.'),
    ('AI Search Readiness', 'Build clearer business entities and authoritative signals for modern answer and AI search platforms.'),
]

STEPS = [
    node('Local SEO Audit & Competitor Analysis', 'Step 1',
         'Every campaign begins with a complete assessment of your current local search presence. Our specialists analyze:',
         ['Google Business Profile', 'Existing Maps visibility', 'Local keyword rankings', 'Website SEO', 'NAP consistency', 'Local citations',
          'Reviews and reputation', 'Backlink profile', 'Location landing pages', 'Competitor visibility', 'Conversion paths', 'AI search visibility signals']),
    node('Local Keyword & Neighborhood Strategy', 'Step 2',
         'Local search demand varies significantly across Dubai. We identify the services, keywords, and locations most likely to generate commercially valuable enquiries. Our strategy can cover combinations such as:',
         ['Service + Dubai', 'Service + Business Bay', 'Service + DIFC', 'Service + JLT', 'Service + Dubai Marina', 'Service + Jumeirah',
          'Service + near me', 'Best + service + Dubai']),
    node('Google Business Profile Optimization', 'Step 3',
         'Your Google Business Profile is one of your most important local search assets. We optimize key elements including:',
         ['Primary business category', 'Secondary categories', 'Business information', 'NAP details', 'Services', 'Service areas', 'Business description',
          'Opening hours', 'Website links', 'Appointment links', 'Photos and media', 'Google Posts', 'Business Q&A', 'Review strategy', 'Duplicate profile checks']),
    node('Local Website & Entity Optimization', 'Step 4',
         'Your website must reinforce the same local relevance signals as your Google Business Profile. Our Local SEO specialists optimize:',
         ['Service pages', 'Location pages', 'Page titles', 'Meta descriptions', 'Heading structure', 'Internal links', 'Location signals',
          'Entity relationships', 'Structured data', 'Conversion elements', 'Mobile usability', 'Local content']),
    node('Citations, Reviews & Local Authority', 'Step 5',
         'Prominence plays an important role in local search. We strengthen your wider digital footprint through:',
         ['NAP consistency', 'UAE business citations', 'Relevant directory listings', 'Review acquisition workflows', 'Review monitoring',
          'Professional review responses', 'Local backlinks', 'Industry websites', 'Business partnerships', 'Digital PR opportunities', 'Authoritative brand mentions']),
    node('Geo-Grid Rank Tracking', 'Step 6',
         'A single Maps ranking does not show the full picture. Google Maps visibility can change significantly based on where the customer is searching. SquareZix uses geo-grid tracking across approximately 20–50 GPS coordinates, depending on campaign scope, to identify:',
         ['Areas where you rank in the Top 3', 'Areas with moderate visibility', 'Locations where competitors dominate', 'Geographic ranking improvements',
          'New neighborhood opportunities']),
    node('Lead Tracking, Reporting & Continuous Growth', 'Step 7',
         'Local SEO should ultimately generate business—not just ranking reports. Depending on your analytics setup, we track:',
         ['Phone calls', 'WhatsApp clicks', 'Enquiry forms', 'Booking actions', 'Google Business Profile interactions', 'Direction requests',
          'Website conversions', 'Organic traffic', 'Local rankings', 'Geo-grid visibility']),
]

WHY = [
    ('Dubai-Focused Local Expertise',
     'Dubai is not one uniform search market. Customer behavior varies across Business Bay, Downtown Dubai, DIFC, JLT, Dubai Marina, Jumeirah, Deira, Al Barsha, and other communities. We build strategies around the locations that genuinely matter to your business.', {}),
    ('Google Maps + Organic SEO',
     'Your Google Business Profile and website should reinforce each other. We optimize both as part of one local search ecosystem rather than treating Google Maps and organic SEO as separate services.', {}),
    ('Geo-Grid Visibility Tracking',
     'Instead of reporting one misleading Maps position, we measure your visibility across multiple geographic coordinates. You can see exactly where you are winning and where more work is needed.', {}),
    ('Lead-Focused SEO Strategy', '',
     {'lead': 'Rankings are only valuable when they contribute to business growth. We focus on customer actions including:',
      'chips': ['Calls', 'WhatsApp messages', 'Forms', 'Bookings', 'Direction requests', 'Store visits', 'Qualified enquiries']}),
    ('Local Authority Building',
     'We strengthen the external signals surrounding your business through relevant reviews, citations, backlinks, business listings, brand mentions, and digital PR.', {}),
    ('AI Search Optimization',
     'Local search is evolving beyond traditional results. Our approach also strengthens the entities, structured information, content, authority, and trust signals that help modern AI-powered platforms understand your brand.', {}),
]

SOLUTIONS = [
    node('Google Business Profile Optimization', 'Solution',
         'Your Google Business Profile can become one of your highest-value sources of local customers. Our GBP optimization services include:',
         ['Category selection', 'Complete business information', 'Service optimization', 'Business description', 'Service-area setup', 'Opening hours',
          'Images and media', 'Google Posts', 'Q&A optimization', 'Review monitoring', 'Duplicate listing checks', 'Profile performance analysis'],
         'We optimize your profile around the services and locations your potential customers actually search for.'),
    node('Google Maps & Geo-Grid SEO', 'Solution',
         'Know exactly where your business appears across your target market. Our Google Maps SEO strategy combines:',
         ['Local 3-Pack optimization', 'Geo-grid tracking', 'Competitor visibility analysis', 'Local keyword targeting', 'GBP improvements', 'Review signals',
          'Citation consistency', 'Website relevance', 'Local authority building'],
         'Geo-grid tracking allows us to visualize visibility across multiple GPS coordinates rather than relying on one ranking point.'),
    node('Local Citations & NAP Management', 'Solution',
         'Inconsistent business information can confuse customers and weaken your local digital footprint. We audit and standardize your:',
         ['Business Name', 'Address', 'Phone Number'],
         'Across appropriate maps, directories, business platforms, and industry websites. Our approach prioritizes relevance, accuracy, and authority over citation quantity.'),
    node('Neighborhood & Location Page SEO', 'Solution',
         'Customers frequently search by neighborhood rather than simply searching across the entire city. Depending on genuine service coverage and search demand, we can build strategies targeting locations including:',
         ['Business Bay', 'Downtown Dubai', 'DIFC', 'JLT', 'Dubai Marina', 'Jumeirah', 'Deira', 'Al Barsha', 'Dubai Hills', 'Palm Jumeirah', 'JBR', 'Dubai Silicon Oasis'],
         'Each landing page is developed around unique local intent rather than duplicating the same content and changing the area name.'),
    node('Reviews & Reputation Management', 'Solution',
         'Searchers often compare businesses based on both rankings and reputation. Our reputation-management strategy can include:',
         ['Review acquisition processes', 'Review links', 'QR review journeys', 'Staff review-request guidelines', 'Review monitoring', 'Professional responses',
          'Negative-feedback workflows', 'Reputation analysis'],
         'The goal is to develop a consistent stream of authentic customer feedback while strengthening trust.'),
    node('Local Link Building & Digital PR', 'Solution',
         'Strong third-party signals can improve the authority surrounding your business. Our local link-building strategy can target relevant:',
         ['UAE publications', 'Industry websites', 'Regional blogs', 'Business organizations', 'Partner websites', 'Community resources', 'Business directories',
          'Digital PR opportunities'],
         'We focus on legitimate relevance rather than automated or bulk backlink schemes.'),
    node('Multi-Location Local SEO', 'Solution',
         'Managing several branches requires consistent brand signals without creating location duplication or keyword cannibalization. Our multi-location SEO services can include:',
         ['Individual branch strategies', 'Eligible Google Business Profiles', 'Location landing pages', 'Location-specific schema', 'Branch-level citations',
          'Location-level review management', 'Geo-grid monitoring', 'Centralized reporting', 'Arabic and English SEO'],
         'This allows your Local SEO strategy to scale from Dubai to Abu Dhabi, Sharjah, and other UAE markets as your business grows.'),
    node('AI Search & Answer Engine Optimization', 'Solution',
         'Customers are increasingly discovering businesses through conversational and AI-powered search experiences. SquareZix incorporates Answer Engine Optimization, Generative Engine Optimization, and entity SEO principles into Local SEO campaigns. Our approach focuses on:',
         ['Clear business entities', 'Consistent company information', 'E-E-A-T signals', 'Question-based content', 'Structured information',
          'Service-location relationships', 'Authoritative citations', 'Third-party mentions', 'High-quality backlinks', 'Topical authority'],
         'No SEO agency can guarantee that an AI system will recommend a particular business. Our objective is to create a clearer, more authoritative digital footprint that makes your company easier for search and AI systems to understand.'),
]

FAQ = [
    ('Can Local SEO improve AI search visibility?',
     'Local SEO can strengthen the business information, authority signals, entities, reviews, citations, and content that modern search and AI systems may use to understand companies. No agency can guarantee inclusion in an AI-generated response, but a stronger digital entity can improve your overall discoverability.'),
    ('Do you provide multi-location Local SEO?',
     'Yes. SquareZix can develop Local SEO strategies for individual branches, including Google Business Profile management, location pages, citations, reviews, structured data, geo-grid tracking, and centralized reporting.'),
    ('Do I need separate pages for Business Bay, DIFC, JLT, and Dubai Marina?',
     'Separate location pages can be valuable when your business genuinely serves those areas and there is meaningful local search demand. The pages should provide unique, useful information rather than repeating identical content with only the location name changed.'),
    ('Can Local SEO generate WhatsApp and phone enquiries?',
     'Yes. Local SEO can increase discovery among high-intent customers, while conversion optimization helps turn that visibility into WhatsApp clicks, phone calls, enquiry forms, bookings, and other customer actions.'),
    ('How much does Local SEO cost in Dubai?',
     'Single-location campaigns may typically range from approximately AED 3,000–5,000 per month, while broader or multi-location campaigns can range from approximately AED 5,500 to AED 12,000+ per month, depending on scope and competition.'),
    ('What is geo-grid rank tracking?',
     'Geo-grid tracking measures Google Maps rankings from multiple geographic coordinates. This helps show exactly where your business has strong visibility and where competitors are outperforming you across your target area.'),
    ('Can you guarantee a Top-3 Google Maps ranking?',
     'No responsible SEO agency can guarantee a permanent Top-3 position. Local results vary based on the searcher’s location, query, competitors, Google algorithms, relevance, and prominence. SquareZix instead focuses on measurable improvements across geographic visibility and customer acquisition.'),
    ('What factors influence Google Maps rankings?',
     'Google describes local results primarily through relevance, distance, and prominence. Factors you can strengthen include your Google Business Profile, website relevance, reviews, citations, local authority, links, and business information.'),
    ('How long does Local SEO take to show results in Dubai?',
     'Some improvements may become visible following initial profile and website optimization, but competitive campaigns generally require several months to build momentum. A planning horizon of approximately 3–6 months is common, although actual results depend on competition, location, authority, and starting position.'),
    ('What is the difference between Local SEO and regular SEO?',
     'Traditional SEO can target national, international, or informational searches. Local SEO focuses on geographically relevant intent, including “near me” searches, Google Maps, the Local Pack, and service-plus-location keywords.'),
    ('What are Local SEO services?',
     'Local SEO services help businesses improve visibility for geographically relevant searches across Google Search and Google Maps. This can include Google Business Profile optimization, local keywords, location pages, citations, reviews, backlinks, structured data, and geographic rank tracking.'),
]

LOCAL_LAYOUT = [
    ('bento', 'Local Visibility', 'Why your business needs a strategic <em>Local SEO approach</em>',
     {'intro': 'Local SEO is more than adding “Dubai” to your website or setting up a Google Business Profile. When customers search for nearby products and services, Google considers signals such as relevance, distance, and prominence to determine which businesses appear prominently in local results. In Dubai, that competition becomes even more localized. A customer searching from DIFC may see different results from someone searching for the same service in Dubai Marina, Business Bay, or Jumeirah.',
      'items': [
          ('Without a strong Local SEO strategy, your business may experience:', '', {'chips': PROBLEMS, 'wide': True}),
          ('Our approach',
           'SquareZix builds a coordinated Local SEO strategy across your Google Business Profile, website, location content, reviews, citations, backlinks, structured data, and local authority signals. Our objective is not simply to improve a keyword position. It is to help your business appear more often when high-intent customers are ready to call, message, visit, book, or buy.',
           {'wide': True})]}),
    ('illus', 'Expectations', 'What you can <em>expect</em>',
     {'intro': '', 'items': [(t, d, {'art': a}) for (t, d), a in zip(EXPECT, ['maps', 'profile', 'geogrid', 'leads', 'authority', 'threepack', 'district', 'ai'])]}),
    ('process', 'Our Process', 'Our 7-step Local SEO growth process — <em>building local visibility across Google Maps, Search & AI platforms</em>',
     {'intro': 'Successful Local SEO requires more than occasional Google Business Profile updates. At SquareZix, we follow a structured Local SEO framework combining data, optimization, content, authority building, reputation management, and conversion tracking to grow your visibility across Dubai.',
      'items': STEPS}, 'process'),
    ('bento', 'Why Choose Squarezix', 'Why choose Squarezix for <em>Local SEO services in Dubai?</em>',
     {'intro': 'Choosing the right Local SEO agency can determine whether your business simply appears online or consistently attracts customers from local search. SquareZix combines Google Maps SEO, website optimization, data-driven tracking, content, authority building, and AI search strategy into one coordinated Local SEO campaign.',
      'items': WHY}),
    ('nodes', 'Our Solutions', 'Comprehensive <em>Local SEO solutions</em>',
     {'intro': 'Every business has different geographic targets, competitors, and growth objectives. SquareZix provides customized Local SEO solutions for businesses ranging from a single Dubai location to multi-branch organizations operating across the UAE.',
      'items': SOLUTIONS}, 'services'),
    ('statement', 'Our approach to AI-driven visibility', 'The Squarezix way to <em>AI visibility</em>',
     'Search visibility today goes beyond traditional rankings. At SquareZix, we combine SEO, AI search optimization, structured data, entity development, content, authority, and analytics to send clearer signals across search platforms—helping your business get discovered, trusted, and chosen.'),
    ('cta', 'Be found where your customers are <em>searching</em> with Squarezix',
     'Improve your Google Maps rankings, increase local search visibility, and generate more qualified enquiries with professional Local SEO Services in Dubai.'),
    ('faq', 'FAQs', 'Frequently asked questions about <em>Local SEO in Dubai</em>', FAQ),
]

LOCAL_HERO = dict(
    badge='Local SEO Services in Dubai',
    h1=['Get Found Where', 'Your Customers Are Searching', 'Through Local SEO'],
    lead='Improve your visibility across Google Maps, Google Search, “near me” searches, and AI-powered search platforms with Local SEO strategies built specifically for Dubai businesses. SquareZix helps businesses increase local visibility, attract high-intent customers, and generate more phone calls, WhatsApp enquiries, direction requests, bookings, and qualified leads.',
)
