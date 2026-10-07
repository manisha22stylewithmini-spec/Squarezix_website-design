"""Off-Page SEO page: the live squarezix.com/off-page-seo/ wording, laid out like the Local SEO page.

Same tuple shapes as local_seo_content.py, plus ('vs', badge, title, data) for the closing
On-Page vs Off-Page panel (the layout of that last section is a placeholder until the user supplies theirs).
"""
from local_seo_content import node

PROBLEMS = ['Low domain authority compared with competitors', 'Limited high-quality referring domains',
            'Difficulty ranking for competitive commercial keywords', 'Weak local search authority', 'Inconsistent UAE business citations',
            'Limited online brand mentions', 'Poor backlink diversity', 'Lost backlink opportunities', 'Over-optimized anchor text',
            'Limited visibility across authoritative third-party sources', 'A weaker digital footprint for AI-powered discovery']

EXPECT = [
    ('High-Quality Contextual Backlinks', 'Relevant links acquired through legitimate outreach and authority-building opportunities.'),
    ('Manual White-Hat Outreach', 'Human-led publisher prospecting and outreach instead of automated backlink blasts.'),
    ('Relevant Referring Domains', 'Opportunities evaluated for topical relevance, credibility and potential SEO value.'),
    ('Natural Anchor Text Distribution', 'A balanced backlink profile designed to avoid unnatural keyword-heavy linking patterns.'),
    ('UAE Local Citation Building', 'Accurate business information across relevant UAE and industry-specific directories.'),
    ('Digital PR & Brand Mentions', 'Campaigns designed to create credible third-party references to your company and expertise.'),
    ('Transparent Link Reporting', 'Clear reporting covering acquired links, referring domains, landing pages and campaign progress.'),
    ('SEO + GEO Visibility Strategy', 'Authority-building that considers Google search alongside emerging AI-powered discovery environments.'),
]

STEPS = [
    node('Backlink Audit & Competitor Analysis', 'Step 1',
         'Every campaign begins with a detailed assessment of your existing backlink profile. Our SEO specialists evaluate:',
         ['Existing referring domains', 'Backlink relevance', 'Anchor text distribution', 'Follow and nofollow links', 'Newly discovered backlinks', 'Lost backlinks',
          'Suspicious link patterns', 'Competitor referring domains', 'Link gaps', 'High-authority opportunities'],
         'We then compare your backlink profile against competitors already ranking for your priority keywords. This allows us to determine where competitors are earning authority and where your website is being left behind.'),
    node('Link Acquisition & Outreach Strategy', 'Step 2',
         'No two websites need the same backlink strategy. After completing the audit, we develop an outreach roadmap around your industry, competition and commercial objectives. Our strategy can include:',
         ['Contextual backlink opportunities', 'Guest editorial contributions', 'Digital PR campaigns', 'Resource-page outreach', 'Link reclamation', 'Unlinked brand mentions',
          'UAE citations', 'Industry directories', 'Linkable content assets', 'Competitor link-gap opportunities'],
         'Third-party metrics such as Domain Rating (DR) and Domain Authority (DA) can be used during prospect evaluation, but we don’t rely on these numbers alone. Topical relevance, editorial quality, organic visibility and contextual placement are also considered.'),
    node('Manual White-Hat Campaign Activation', 'Step 3',
         'Once the strategy is approved, our outreach team begins identifying and contacting suitable publishers, websites and industry resources. Every opportunity is evaluated individually. Depending on your campaign, this stage can involve:',
         ['Publisher outreach', 'Editorial pitching', 'Guest contributions', 'Journalist outreach', 'Digital PR', 'Resource link outreach', 'Citation submissions',
          'Brand mention reclamation', 'Broken-link opportunities'],
         'Our strategy prioritizes legitimate, relevance-led outreach rather than PBN-dependent link building or automated backlink packages. Publisher decisions remain independent, so placements in specific publications cannot be guaranteed.'),
    node('Reporting & Authority Monitoring', 'Step 4',
         'Off-page SEO shouldn’t disappear into a monthly spreadsheet containing hundreds of unexplained URLs. We monitor the wider impact of your campaign through metrics such as:',
         ['New backlinks', 'New referring domains', 'Link quality and relevance', 'Landing pages receiving links', 'Lost backlinks', 'Authority trends',
          'Keyword visibility', 'Organic traffic', 'Referral traffic', 'Citation progress', 'Brand mentions'],
         'Where relevant, we can also evaluate how your brand appears across AI-powered search environments and identify additional opportunities to strengthen its external digital footprint.'),
]

WHY = [
    ('Quality Over Link Quantity', '',
     {'lead': 'We don’t measure success simply by the number of links created. Every opportunity is assessed according to factors such as:',
      'chips': ['Website relevance', 'Editorial quality', 'Topical alignment', 'Organic visibility', 'Link context', 'Placement quality', 'Referring-domain credibility'],
      'close': 'A relevant editorial backlink can provide considerably more strategic value than dozens of unrelated directory or low-quality links.'}),
    ('White-Hat Authority Building',
     'Shortcuts can create long-term problems. Our campaigns prioritize legitimate outreach, useful content and relevant third-party references rather than relying on manipulative backlink networks. We avoid making PBNs, automated link blasts or mass low-quality directory submissions the foundation of client campaigns.', {}),
    ('Dubai & UAE Market Expertise',
     'Local authority matters when your customers are in the UAE. Our strategies can incorporate relevant UAE publications, local business citations, industry directories and location-specific opportunities appropriate to companies operating in areas such as Business Bay, Dubai Media City and Sheikh Zayed Road, as well as the wider UAE.', {}),
    ('SEO + Digital PR', '',
     {'lead': 'The best backlinks are often earned because a business has something useful to contribute. Our Digital PR strategies can leverage:',
      'chips': ['Original research', 'Industry insights', 'Expert commentary', 'Surveys', 'Data-driven reports', 'Founder expertise', 'Newsworthy campaigns', 'Thought leadership'],
      'close': 'These assets can create legitimate reasons for publishers and journalists to reference your company.'}),
    ('Transparent Reporting',
     'You should know exactly what is happening with your campaign. Our reporting provides visibility into acquired backlinks, referring domains, targeted pages and broader organic performance. No mystery backlink packages.', {}),
]

SOLUTIONS = [
    node('High-Authority White-Hat Link Building', 'Solution',
         'Our link building services in Dubai focus on earning contextual links from relevant and credible websites. Potential strategies include:',
         ['Contextual editorial backlinks', 'Guest contributions', 'Industry publisher outreach', 'Resource-page placements', 'Competitor backlink opportunities',
          'Linkable asset promotion', 'Relevant association opportunities'],
         'Where campaign criteria require DR 30+ prospects, Domain Rating can be used as one qualification threshold alongside relevance, editorial quality and organic visibility. We don’t consider DR alone proof that a backlink is valuable. Relevance comes first.'),
    node('Digital PR & Editorial Authority', 'Solution',
         'Digital PR connects SEO with brand building. Rather than simply asking publishers for links, we develop stories and assets that give journalists and industry publications a reason to reference your company. Campaign opportunities can include:',
         ['Industry research', 'Surveys', 'Data-led stories', 'Expert commentary', 'Newsjacking', 'Executive insights', 'Thought leadership', 'Journalist request platforms'],
         'For UAE businesses, outreach can target appropriate opportunities across regional business and industry media. The objective is not merely a backlink. It is to establish your company as a credible source within its market.'),
    node('Unlinked Brand Mention Reclamation', 'Solution',
         'Your business may already be earning online mentions without receiving a backlink. We identify instances where websites, blogs or publishers reference your:',
         ['Company', 'Products', 'Services', 'Founders', 'Executives', 'Research', 'Campaigns', 'Events'],
         'Where appropriate, we contact the publisher and request that the existing mention be linked to a relevant page on your website. Because the publisher already knows your brand, these can represent particularly natural link opportunities.'),
    node('UAE Citation & Directory Management', 'Solution',
         'Consistent local business information supports a stronger local digital footprint. SquareZix audits and manages citations across relevant UAE and industry-specific sources. We focus particularly on maintaining consistent: Name, Address, Phone Number. Our citation strategy can include:',
         ['UAE business directories', 'Industry-specific directories', 'Mapping platforms', 'Business profiles', 'Professional associations', 'Local discovery platforms'],
         'Rather than submitting your company to hundreds of questionable directories, we prioritize credible sources relevant to your business and market.'),
    node('Backlink Audit & Toxic Link Assessment', 'Solution',
         'Before building new authority, we examine what is already pointing to your website. Our backlink audits analyze:',
         ['Referring domains', 'Anchor text', 'Link relevance', 'Lost links', 'New links', 'Unusual link patterns', 'Spam-heavy domains', 'Competitor link gaps', 'Valuable existing backlinks'],
         'Suspicious links are assessed individually rather than automatically disavowed based solely on third-party toxicity scores. Where further action is warranted, we determine the most appropriate strategy.'),
    node('Broken Link & Resource Page Outreach', 'Solution',
         'Web pages disappear every day, leaving broken links across otherwise valuable resources. We identify relevant broken-link opportunities where your website has a legitimate resource capable of replacing the missing content. We can also investigate backlinks your own website previously earned but later lost.',
         [],
         'Where a valuable link disappeared because of URL changes, deleted content or publisher updates, we assess whether the link can reasonably be reclaimed.'),
]

INDUSTRIES = [
    ('Real Estate & Property', 'Develop authority through relevant property publications, market resources, location-based content, original research and industry coverage.', {}),
    ('Healthcare & Clinics', 'Strengthen credibility through relevant professional, healthcare and local sources while prioritizing trustworthy authority signals.', {}),
    ('E-Commerce & Retail', 'Build category and product authority through editorial outreach, product PR, buying resources, relevant publications and brand mentions.', {}),
    ('Corporate, Technology & Fintech', 'Use research, executive commentary, thought leadership, industry data and business publications to strengthen B2B authority.', {}),
]

FAQ = [
    ('Do you provide off-page SEO throughout the UAE?', 'Yes. SquareZix can develop campaigns for businesses targeting Dubai, the wider UAE and international markets.'),
    ('Can off-page SEO improve AI search visibility?', 'A stronger external digital footprint can make a business easier for search and AI systems to discover and understand. We therefore combine conventional authority building with GEO and AEO considerations. No responsible agency can guarantee that a specific AI platform will cite or recommend a particular company.'),
    ('Can SquareZix provide DR 30+ backlinks?', 'DR 30+ can be used as a prospect qualification criterion where required. However, we also assess topical relevance, editorial quality, organic visibility and contextual value rather than choosing websites purely because they exceed a particular DR score.'),
    ('Does SquareZix use PBNs?', 'Our campaigns prioritize legitimate, relevance-led outreach and do not rely on Private Blog Networks as the foundation of client link-building strategies.'),
    ('What makes a backlink high quality?', 'A strong backlink generally comes from a credible and relevant website and appears naturally within useful content. Topical relevance, editorial quality, organic visibility, placement and surrounding context should all be considered. DR and DA can help evaluate prospects but are third-party metrics, not Google ranking scores.'),
    ('How long does off-page SEO take to work?', 'Results vary according to your starting authority, competition, website quality and campaign scope. Some websites may begin seeing movement within a few months, while highly competitive SEO campaigns can require longer. A 3–6 month period is generally more useful for evaluating meaningful progress than judging individual links immediately.'),
    ('Why is off-page SEO important for Dubai businesses?', 'Many commercially valuable Dubai SERPs are highly competitive. Relevant backlinks, authoritative mentions and local citations can strengthen the external credibility of your website and support your overall organic search strategy.'),
    ('What is off-page SEO?', 'Off-page SEO includes activities outside your own website that help strengthen its online authority, reputation and visibility. Common strategies include backlink acquisition, Digital PR, brand mentions, business citations and link reclamation.'),
]

OFFPAGE_LAYOUT = [
    ('statement', 'Off-Page SEO', 'Ready to Build Powerful <em>Authority & Rankings?</em>',
     'Whether you’re building domain strength across competitive markets in Business Bay, Downtown Dubai, DIFC, JLT, Dubai Marina, Jumeirah, or scaling your authority across the UAE, SquareZix executes strategic Off-Page SEO campaigns that earn high-value backlinks and digital PR. Our strategies strengthen your brand’s trust signals across major search engines while establishing your entity presence across authoritative digital publications, industry directories, and emerging AI citation engines. Book your free Off-Page SEO consultation and discover your biggest authority gaps and backlink opportunities.'),
    ('compare', 'Off-Page Authority', 'Why your business needs a strategic <em>Off-Page SEO approach</em>',
     {'intro': 'Optimizing your website is only one side of SEO. For competitive searches, Google also needs signals that demonstrate your website and business have authority beyond the content published on your own domain. Backlinks, editorial references, local citations, press coverage and other third-party mentions help establish that external digital footprint. This becomes especially important in competitive Dubai industries where multiple businesses may already have well-optimized websites.',
      'left': {'dim': 'Without a strong', 'title': 'Off-Page SEO strategy, your website may struggle with:', 'chips': PROBLEMS,
               'link': ('#process', 'See how we fix it')},
      'right': {'title': 'Our approach',
                'text': 'At SquareZix, our off-page SEO optimization in the UAE focuses on strengthening your website’s reputation through legitimate authority-building strategies rather than artificial link volume. Our goal is straightforward: Make your business more authoritative, discoverable and trustworthy across the wider web.',
                'hub': 'Authority',
                'keywords': ['Backlinks', 'Digital PR', 'Brand mentions', 'Citations', 'Referring domains', 'Outreach', 'Link reclamation', 'AI citations'],
                'tag': 'Authority, not link volume', 'cta': ('#ab-contact', 'Talk to our team')}}),
    ('illus', 'Expectations', 'What you can <em>expect</em>',
     {'intro': '', 'items': [(t, d, {'art': a}) for (t, d), a in zip(EXPECT, ['authority', 'profile', 'district', 'threepack', 'maps', 'leads', 'geogrid', 'ai'])]}),
    ('process', 'Our Process', 'Our 4-Step <em>Off-Page SEO Process</em>',
     {'intro': 'Ready to build your website authority? Discover where your backlink profile stands against your competitors. SquareZix will identify your current referring domains, authority gaps, lost links, competitor backlink opportunities and potential areas for improvement. Key outcomes: stronger domain authority, higher search visibility, more qualified organic traffic.',
      'items': STEPS}, 'process'),
    ('bento', 'Why Choose Squarezix', 'Why Choose SquareZix for <em>Off-Page SEO Services in Dubai?</em>',
     {'intro': 'Building backlinks is easy. Building the right backlinks is considerably harder. SquareZix combines SEO analysis, manual outreach, digital PR and local UAE market knowledge to develop off-page campaigns focused on sustainable authority rather than artificial backlink volume.',
      'items': WHY, 'grid': 'b5'}),
    ('nodes', 'Our Solutions', 'Comprehensive <em>Off-Page Solutions</em>',
     {'intro': 'Every website has a different authority gap. SquareZix develops customized off-page campaigns based on your existing backlink profile, competitors, industry and target market.',
      'items': SOLUTIONS}, 'services'),
    ('statement', 'Beyond Google', 'Build Authority Beyond <em>Traditional Google Search</em>',
     'Search visibility is evolving. Customers increasingly discover and compare businesses through traditional search results alongside platforms and experiences such as Google AI Overviews, ChatGPT, Gemini and Perplexity. That makes your brand’s presence beyond its own website increasingly important. Traditional off-page SEO asks: Who links to your website? Modern authority building also asks: Where is your brand mentioned, referenced and validated across the web? SquareZix incorporates Generative Engine Optimization (GEO) and Answer Engine Optimization (AEO) thinking into our authority strategies. No agency can guarantee a citation from ChatGPT, Gemini or an AI Overview. Instead, we focus on strengthening the credible external signals that make your business easier to discover, understand and verify across the wider web.'),
    ('bento', 'Beyond Google', 'Where your <em>authority is built</em>',
     {'intro': '', 'items': [('This can involve building a stronger presence across:', '', {'chips': ['Authoritative publications', 'Industry websites', 'News sources', 'Expert contributions', 'Relevant communities', 'Business directories', 'Third-party brand mentions', 'Trusted niche resources'], 'wide': True})]}),
    ('bento', 'Industries', 'Off-Page SEO Solutions for <em>Dubai’s Competitive Industries</em>', {'intro': '', 'items': INDUSTRIES}),
    ('vs', 'On-Page vs Off-Page', 'On-Page SEO <em>vs. Off-Page SEO</em>',
     {'intro': 'The strongest SEO strategies combine both. Excellent content needs authority behind it, while backlinks cannot compensate for a website with poor content, weak search intent alignment or major technical problems.',
      'left': {'title': 'On-Page SEO', 'note': 'Establishes relevance and usability',
               'items': ['Website content optimization', 'Keyword targeting', 'Titles and metadata', 'Internal linking', 'Schema markup', 'Technical performance', 'Website architecture']},
      'right': {'title': 'Off-Page SEO', 'note': 'Establishes external authority and prominence',
                'items': ['Backlink acquisition', 'Digital PR', 'Brand mentions', 'Referring domains', 'UAE citations', 'Link reclamation', 'External brand authority']}}),
    ('statement', 'Our approach to AI-driven visibility', 'The Squarezix way to <em>AI visibility</em>',
     'Visibility today extends beyond conventional search rankings. At SquareZix, we combine SEO, Digital PR, data and authority-building strategies to strengthen the signals surrounding your business across search engines and AI-powered discovery platforms. The goal is simple: Get discovered. Build trust. Become the brand customers choose.'),
    ('cta', 'Grow Your Search & AI Visibility with <em>SquareZix</em>',
     'Build stronger authority, improve organic visibility and attract more qualified visitors with professional off-page SEO services in Dubai.'),
    ('faq', 'FAQs', 'Frequently Asked Questions About <em>Off-Page SEO in Dubai</em>', FAQ, 'Still have questions? Our team is here to help you find the right solution for your business.'),
]

OFFPAGE_HERO = dict(
    badge='Off-Page SEO Services in Dubai',
    h1=['Off-Page SEO Services in Dubai', 'That Build Authority', '& Rankings'],
    lead='Build a stronger search presence with strategic off-page SEO services in Dubai designed to increase your website authority, earn high-quality backlinks and strengthen your brand’s reputation across Google and AI-powered search.',
)
