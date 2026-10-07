"""Technical SEO page: the live squarezix.com/technical-seo/ wording on the locked components
(statement, vs, 3D process plates, bento cards, looping strip, solution cards, FAQ)."""
from local_seo_content import node


def deliver(title, text, chips, impact):
    return node(title, 'Included', text, chips, 'Business Impact: ' + impact)


STEPS = [
    node('Technical Discovery & Website Analysis', 'Step 1',
         'Every successful technical SEO strategy begins with understanding your website, business objectives, and current search performance.', [],
         'Outcome: A clear understanding of your website’s technical health, opportunities, and potential growth areas.'),
    node('Comprehensive Technical SEO Audit', 'Step 2',
         'Our specialists conduct a detailed technical audit to identify issues affecting how search engines crawl, render, and index your website.', [],
         'Outcome: A complete technical SEO report highlighting critical issues, opportunities, and recommended solutions.'),
    node('Prioritization & Technical Roadmap', 'Step 3',
         'Not every SEO issue has the same impact. Fixing the wrong things first can waste time and resources.', [],
         'Outcome: A clear action plan showing what needs to be fixed, why it matters, and the expected impact.'),
    node('Technical Implementation & Optimization', 'Step 4',
         'Once the roadmap is approved, our SEO specialists work with developers, designers, and internal teams to implement improvements.', [],
         'Outcome: A technically optimized website that is easier for search engines to understand and users to navigate.'),
    node('Validation, Monitoring & Continuous Improvement', 'Step 5',
         'Technical SEO is an ongoing process. Websites change, content grows, platforms update, and search algorithms evolve.', [],
         'Outcome: A healthy, scalable website that continues supporting long-term organic growth.'),
]

ISSUES = [
    ('Your Website Isn’t Ranking Despite Having Great Content', 'High-quality content cannot perform if search engines struggle to crawl, understand, or index your pages. We identify technical barriers affecting visibility and optimize your website structure to help search engines discover and rank your valuable content.', {}),
    ('Important Pages Are Not Being Indexed by Google', 'Pages that are blocked, poorly structured, or affected by technical errors may remain invisible in search results. We analyze indexation issues, optimize crawl paths, and ensure your important pages are accessible to search engines.', {}),
    ('Your Website Loads Slowly and Provides a Poor User Experience', 'Slow websites can impact rankings, user engagement, and conversions. We optimize Core Web Vitals, page resources, images, scripts, and technical performance factors to create a faster browsing experience across desktop and mobile devices.', {}),
    ('Your Website Has Crawl Errors Affecting Search Visibility', 'Crawl errors can prevent search engines from accessing important sections of your website. We identify issues related to broken links, server responses, redirects, and crawl restrictions to improve search engine accessibility.', {}),
    ('Duplicate Content Is Reducing Your Website Authority', 'Duplicate or similar pages can confuse search engines about which version should rank. We implement solutions such as canonical tags, URL management, and content consolidation to strengthen your website’s ranking signals.', {}),
    ('Search Engines Are Not Understanding Your Website Structure', 'A poorly organized website makes it difficult for search engines to understand your content hierarchy. We improve site architecture, internal linking, breadcrumbs, and URL structures to create a clearer path for both users and search engines.', {}),
    ('Your Website Has Missing or Incorrect Schema Markup', 'Without proper structured data, search engines may struggle to understand your business, services, products, and content. We implement relevant schema markup to improve search visibility and strengthen your website’s understanding across search engines and AI platforms.', {}),
    ('Your Website Performance Drops After a Redesign or Migration', 'Website redesigns, platform changes, and migrations can create unexpected SEO issues such as lost rankings, broken URLs, and indexing problems. We identify migration-related errors and implement technical solutions to protect your organic visibility.', {}),
    ('Your Ecommerce Website Has Technical SEO Challenges', 'Large ecommerce websites often face complex SEO issues including duplicate product pages, crawl budget limitations, filtering problems, and indexation challenges. We optimize ecommerce platforms to improve search visibility for products and category pages.', {}),
    ('Your Website Is Not Optimized for Mobile Search', 'With mobile-first indexing, poor mobile performance can directly impact search visibility and user experience. We analyze mobile usability, responsive design issues, loading performance, and mobile technical factors to ensure your website performs effectively on every device.', {}),
    ('Your Multilingual Website Is Targeting the Wrong Audience', 'Businesses operating in Dubai and the UAE often serve Arabic and English-speaking audiences. Incorrect language targeting can create visibility issues. We implement hreflang, regional targeting, and multilingual SEO best practices to help users find the correct version of your website.', {}),
    ('Your Website Is Not Ready for AI-Powered Search', 'Search is evolving beyond traditional Google results. Websites that lack clear structure, entity signals, and machine-readable information may struggle to appear in AI-generated answers. We optimize your technical foundation to improve visibility across Google AI Overviews, ChatGPT, Gemini, and other AI search experiences.', {}),
]

PLATFORMS = [(t, '', {}) for t in ('WordPress Websites', 'Shopify Websites', 'Magento Websites', 'WooCommerce Websites',
                                  'Laravel & Custom Websites', 'React, Next.js & JavaScript Websites', 'Headless CMS Websites')]

DELIVERABLES = [
    deliver('Technical SEO Audit', 'A successful SEO strategy starts with understanding what’s holding your website back. Our comprehensive technical SEO audit uncovers hidden issues affecting your search performance and provides a prioritized roadmap for improvement. What’s Included:',
            ['Website health assessment', 'Technical issue identification', 'SEO opportunity analysis', 'Prioritized action plan', 'Performance benchmarking'],
            'Gain a clear understanding of your website’s technical health and focus on the improvements that deliver the greatest SEO impact.'),
    deliver('Core Web Vitals & Website Performance Optimization', 'Website speed and user experience play a critical role in search rankings and conversions. We optimize your website to meet Google’s Core Web Vitals standards and improve overall page performance across desktop and mobile devices. What’s Included:',
            ['Largest Contentful Paint (LCP) optimization', 'Interaction to Next Paint (INP) improvements', 'Cumulative Layout Shift (CLS) optimization', 'Image and asset optimization', 'Render-blocking resource optimization', 'Browser caching recommendations'],
            'Deliver a faster, smoother browsing experience that improves user engagement, search visibility, and conversion rates.'),
    deliver('Crawlability & Indexability Optimization', 'If search engines can’t access or understand your website, your pages may never reach their ranking potential. We optimize your website’s crawl paths and indexation to ensure important pages are discovered and indexed efficiently. What’s Included:',
            ['Crawl error analysis', 'Robots.txt review', 'XML sitemap optimization', 'Crawl budget optimization', 'Orphan page identification', 'Index coverage improvements'],
            'Help search engines discover your most valuable pages faster while reducing indexing issues that limit organic visibility.'),
    deliver('Website Architecture & Internal Linking', 'A well-structured website improves navigation for users and helps search engines understand the relationship between your pages. What’s Included:',
            ['Site architecture review', 'URL structure optimization', 'Internal linking strategy', 'Navigation improvements', 'Breadcrumb optimization', 'Topic cluster recommendations'],
            'Strengthen topical authority, improve crawl efficiency, and guide visitors toward your most important services and landing pages.'),
    deliver('Schema Markup & Structured Data Implementation', 'Structured data helps search engines better interpret your content and enhances your eligibility for rich search results. What’s Included:',
            ['Organization Schema', 'LocalBusiness Schema', 'Service Schema', 'FAQ Schema', 'Breadcrumb Schema', 'Article and WebPage Schema (where applicable)'],
            'Improve search visibility, strengthen entity recognition, and prepare your website for AI-powered search experiences.'),
    deliver('Canonicalization & Duplicate Content Management', 'Duplicate content and incorrect canonical implementation can confuse search engines and dilute your website’s authority. What’s Included:',
            ['Canonical tag implementation', 'Duplicate content analysis', 'Parameter handling', 'URL consolidation', 'Pagination recommendations'],
            'Ensure search engines index the correct version of your pages while preserving your website’s ranking potential.'),
    deliver('Mobile Technical SEO', 'With Google’s mobile-first indexing, delivering an exceptional mobile experience is essential. What’s Included:',
            ['Mobile usability review', 'Responsive design assessment', 'Mobile performance optimization', 'Touch interaction improvements', 'Mobile crawlability checks'],
            'Provide a seamless mobile experience that supports higher rankings and better engagement across all devices.'),
    deliver('International & Multilingual SEO', 'For businesses targeting customers across the UAE or multiple countries, proper international SEO ensures users reach the right version of your website. What’s Included:',
            ['Hreflang implementation', 'Language targeting', 'Regional SEO recommendations', 'Multilingual indexation review', 'Cross-language canonicalization'],
            'Improve visibility across multilingual search results while reducing duplicate content and targeting issues.'),
    deliver('AI Search Optimization', 'Search is evolving beyond traditional search engines. We optimize your website’s technical foundation to improve how AI-powered search platforms understand and reference your content. What’s Included:',
            ['Entity optimization', 'Structured data enhancements', 'Semantic HTML improvements', 'AI-friendly content architecture', 'Technical readiness for AI search'],
            'Increase your website’s readiness for Google AI Overviews, ChatGPT, Gemini, Claude, and other AI-powered search experiences.'),
    deliver('Continuous Technical SEO Monitoring', 'Technical SEO requires ongoing attention as websites evolve and search engine algorithms change. We continuously monitor your website to identify new opportunities and maintain optimal performance. What’s Included:',
            ['Technical health monitoring', 'Search Console analysis', 'Core Web Vitals tracking', 'Crawl error monitoring', 'Performance reporting', 'Continuous optimization recommendations'],
            'Maintain a technically healthy website that continues to support long-term organic growth and business performance.'),
]

LOCAL = [
    ('Arabic & English Website Optimization', 'Help your website appear for the correct audience while improving visibility across Arabic and English search results.', {}),
    ('Hreflang Implementation for UAE & International Markets', 'Improve search visibility across different regions while maintaining a clean international SEO structure.', {}),
    ('Local SEO Technical Optimization for Dubai Businesses', 'Improve your website’s ability to appear for location-based searches and attract customers searching for your services in Dubai.', {}),
    ('Website Performance Optimization for UAE Users', 'Provide faster experiences for UAE users while improving engagement, rankings, and conversions.', {}),
    ('Ecommerce Technical SEO for UAE Online Stores', 'Help ecommerce businesses improve product visibility and capture more high-intent organic traffic.', {}),
    ('Technical SEO for UAE Enterprise Websites', 'Create a scalable SEO foundation that supports long-term growth across large digital platforms.', {}),
]

FAQ = [
    ('Can Technical SEO fix a sudden drop in website traffic?', 'Technical SEO can help identify and resolve issues that cause sudden traffic drops, including indexing problems, algorithm-related technical impacts, website migrations, broken redirects, performance issues, and accidental changes to website settings. A technical audit helps determine the root cause before implementing solutions.'),
    ('How much do Technical SEO Services cost in Dubai?', 'The cost of Technical SEO Services in Dubai depends on factors such as website size, platform complexity, technical issues, and required optimization work. Small websites may require focused improvements, while enterprise and ecommerce websites often need ongoing technical SEO support and monitoring.'),
    ('Why choose SquareZix for Technical SEO Services in Dubai?', 'SquareZix combines technical SEO expertise, website development knowledge, and business-focused strategies to solve complex SEO challenges. We help businesses improve website performance, crawlability, rankings, and AI search readiness through customized technical SEO solutions designed for the UAE market.'),
    ('What is Core Web Vitals optimization?', 'Core Web Vitals optimization improves website performance based on Google’s user experience metrics: Largest Contentful Paint (LCP), Interaction to Next Paint (INP), and Cumulative Layout Shift (CLS). Improving these metrics helps create faster, more stable websites that provide better experiences for users.'),
    ('How often should a Technical SEO audit be performed?', 'A Technical SEO audit should typically be performed at least once or twice a year, with additional reviews after major website changes such as redesigns, migrations, platform updates, or significant content expansion. Regular monitoring helps identify issues before they impact rankings.'),
    ('Can you provide Technical SEO for Shopify, WordPress, and Magento websites?', 'Yes. Technical SEO requirements vary depending on the website platform. SquareZix provides technical SEO solutions for platforms including WordPress, Shopify, Magento, WooCommerce, Laravel, React, Next.js, and custom-built websites.'),
    ('Do ecommerce websites need Technical SEO?', 'Yes. Ecommerce websites especially require technical SEO because they often contain thousands of product pages, filters, categories, and dynamic URLs. Technical SEO helps manage crawl efficiency, product indexation, duplicate content, structured data, and website performance to improve organic visibility.'),
    ('Can Technical SEO help my website appear in Google AI Overviews?', 'Yes. Technical SEO helps prepare websites for AI-powered search by improving how search systems understand website information. Structured data, clear website architecture, entity optimization, and machine-readable content can improve your website’s ability to be understood by Google AI Overviews and other AI search platforms.'),
    ('What is the difference between Technical SEO and On-Page SEO?', 'Technical SEO focuses on improving the infrastructure of your website, including speed, crawlability, indexation, security, and structured data. On-page SEO focuses on optimizing website content, keywords, metadata, headings, and internal linking. Both work together to improve organic search performance.'),
    ('Does Technical SEO improve website conversions?', 'Yes. Technical SEO can improve conversions by creating a faster, smoother, and more reliable user experience. Improvements such as faster loading speeds, mobile optimization, better navigation, and reduced technical errors help visitors engage with your website and complete desired actions.'),
    ('How does Technical SEO improve Google rankings?', 'Technical SEO improves rankings by making it easier for search engines to access, understand, and evaluate your website. By improving crawlability, website performance, structured data, mobile experience, and content accessibility, technical SEO helps search engines identify your pages as relevant and valuable for users.'),
    ('What technical SEO issues can prevent my website from ranking?', 'Common technical SEO issues that affect rankings include slow page speed, poor Core Web Vitals, blocked crawling, incorrect indexation, duplicate content, broken links, missing schema markup, poor website architecture, JavaScript rendering problems, and incorrect canonical implementation.'),
    ('How long does it take to see results from Technical SEO?', 'The timeline for Technical SEO results depends on the size of the website, the severity of technical issues, and how quickly recommendations are implemented. Some improvements, such as fixing crawl errors or performance issues, can show impact quickly, while larger architectural improvements may require several months.'),
    ('What does a Technical SEO audit include?', 'A Technical SEO audit analyzes the technical factors affecting your website’s search performance. It typically includes crawlability, indexation, Core Web Vitals, website speed, mobile usability, XML sitemaps, robots.txt, canonical tags, structured data, internal linking, security, and overall website architecture.'),
    ('What are Technical SEO Services?', 'Technical SEO services focus on improving the technical foundation of a website so search engines can crawl, understand, index, and rank pages more effectively. These services include website audits, Core Web Vitals optimization, crawlability improvements, structured data implementation, indexation fixes, mobile optimization, and technical improvements that support better search performance.'),
    ('Why is Technical SEO important for businesses in Dubai?', 'Technical SEO is important for Dubai businesses because competition across industries is highly digital. A technically optimized website helps search engines discover your pages, improves user experience, increases website performance, and creates a stronger foundation for ranking in Google Search and AI-powered search platforms.'),
]

TECH_LAYOUT = [
    ('statement', 'Technical SEO', 'Fix Technical Issues That Hold Your Website Back From <em>Ranking, Converting & Growing</em>',
     'Your website may have great content and a professional design, but technical SEO issues can prevent it from achieving strong search visibility. Slow page speed, poor Core Web Vitals, crawl and indexation errors, broken schema, and weak site architecture can all affect your rankings and user experience. At SquareZix, our Technical SEO Services in Dubai identify and resolve these issues to improve your website’s performance, search engine visibility, and AI search readiness. We build a technically sound foundation that supports sustainable organic growth, better rankings, and higher conversions.'),
    ('vs', 'Audit Comparison', 'Standard SEO Audits <em>vs. SquareZix Technical SEO Audits</em>',
     {'intro': '',
      'left': {'title': 'Standard SEO Audit', 'note': '',
               'items': ['Automated reports', 'Generic recommendations', 'Basic schema checks', 'PageSpeed score', 'Crawl errors', 'Google only']},
      'right': {'title': 'SquareZix Technical Infrastructure Audit', 'note': '',
                'items': ['Manual + automated analysis', 'Business-priority roadmap', 'Entity + AI-ready structured data', 'Core Web Vitals optimization plan', 'Crawl budget optimization', 'Google + AI Search readiness']}}),
    ('statement', 'Business Growth', 'Turn Better On-Page SEO Into <em>Real Business Growth</em>',
     'We build tailored on-page SEO strategies that improve your content, structure, metadata, internal linking, page experience, and visibility across Google search results. AI Search Visibility. More Qualified Leads. Measurable Growth.'),
    ('process', 'Our Framework', 'Our Technical SEO <em>Framework</em>', {'intro': '', 'items': STEPS}, 'process'),
    ('bento', 'Technical SEO Issues', 'Technical SEO <em>Issues We Solve</em>',
     {'intro': 'Technical SEO problems are often hidden behind the surface of your website. A site may look visually perfect but still struggle to rank, generate traffic, or convert visitors due to underlying technical issues. At SquareZix, we identify and resolve the technical barriers preventing your website from reaching its full search potential.',
      'items': ISSUES}),
    ('industries', 'Platforms', 'Platform-Specific <em>Technical SEO Services</em>', {'intro': '', 'items': PLATFORMS}),
    ('nodes', 'Our Solutions', 'What’s Included in Our <em>Technical SEO Services?</em>',
     {'intro': 'Our Technical SEO Services are designed to improve your website’s infrastructure, making it easier for search engines to crawl, index, and understand your content while delivering a faster, more reliable experience for your users.',
      'items': DELIVERABLES}, 'services'),
    ('bento', 'UAE Businesses', 'Technical SEO for UAE Businesses: <em>Optimized for Local, Multilingual & Global Audiences</em>',
     {'intro': 'Our on-page SEO solutions are tailored to businesses of all sizes, from startups building their online presence to established organisations looking to strengthen their organic visibility.',
      'items': LOCAL}),
    ('cta', 'Be Found Where Your Customers Are Searching with <em>Squarezix</em>',
     'Improve your website rankings, attract qualified visitors, and generate more enquiries with professional on-page SEO services in Dubai.'),
    ('statement', 'Our approach to AI-driven visibility', 'The Squarezix Way to <em>AI Visibility</em>',
     'Visibility today is bigger than ever. At Squarezix, we combine AI, data, and strategy to send the right signals across platforms—so your brand gets discovered, trusted, and chosen.'),
    ('faq', 'FAQs', 'Frequently asked questions about <em>Technical SEO</em>', FAQ),
]

TECH_HERO = dict(
    badge='Technical SEO Services',
    h1=['Technical SEO', 'Services', 'in Dubai'],
    lead='Technical SEO Services in Dubai engineered to help your website rank higher, load faster, and convert more visitors into customers.',
)
