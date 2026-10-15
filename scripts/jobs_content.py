"""Job openings: one dict per role, mirroring the Career fields in the WordPress admin
(Title, Country, City, Job Type, Workplace Type, Overview, Qualifications, Key Responsibilities, Benefits).

SAMPLE: every role and every line below is placeholder copy written so the job detail page can be reviewed. Replace with the
real openings (or set JOBS = [] to show the "No current openings" state on the careers page). Never publish samples as live roles."""

IS_SAMPLE = True

BENEFITS = ['Creative and strategic freedom: own campaigns end to end.',
            'Fast-track career growth based on results.',
            'Learning and certification support.',
            'Flexible paid time off.',
            'Performance-based incentives.',
            'Healthcare coverage in line with UAE law.']


def job(slug, team, title, workplace, job_type, overview, qualifications, responsibilities, city='Dubai', country='United Arab Emirates'):
    return dict(slug=slug, team=team, title=title, country=country, city=city, workplace=workplace, job_type=job_type,
                overview=overview, qualifications=qualifications, responsibilities=responsibilities, benefits=BENEFITS)


JOBS = [
    job('senior-ui-ux-designer', 'Design', 'Senior UI/UX Designer', 'On-site', 'Full-time',
        'Lead the design of websites and digital products for brands across the GCC, from first sketch to a launch-ready interface.',
        ['5+ years designing web or product interfaces', 'A portfolio that shows process as well as polish', 'Strong command of Figma and design systems', 'Clear communication with developers and clients'],
        ['Turn briefs into user journeys, wireframes and high-fidelity designs', 'Build and maintain reusable components and design tokens', 'Present and defend design decisions to clients', 'Work with developers so the build matches the design']),
    job('brand-designer', 'Design', 'Brand Designer', 'Hybrid', 'Full-time',
        'Create identity systems, campaign visuals and brand collateral that look consistent across digital and print.',
        ['3+ years in brand or graphic design', 'Strong typography and layout skills', 'Experience building brand guidelines'],
        ['Design logos, identity systems and brand collateral', 'Adapt the brand across social, web and print', 'Keep every deliverable consistent with the brand guidelines']),
    job('front-end-developer', 'Development', 'Front-end Developer', 'Hybrid', 'Full-time',
        'Build fast, accessible and responsive websites from approved designs.',
        ['3+ years of HTML, CSS and JavaScript', 'Comfort with responsive and accessible layouts', 'Experience with performance optimisation'],
        ['Implement pixel-accurate, responsive pages', 'Keep Core Web Vitals healthy', 'Review work with designers and other developers']),
    job('wordpress-developer', 'Development', 'WordPress Developer', 'On-site', 'Full-time',
        'Develop and maintain custom WordPress themes and plugins for client websites.',
        ['3+ years of WordPress theme and plugin development', 'PHP, MySQL and REST API experience', 'Understanding of security and caching'],
        ['Build custom themes, post types and fields', 'Maintain, update and secure client sites', 'Troubleshoot performance and plugin conflicts']),
    job('shopify-developer', 'Development', 'Shopify Developer', 'Remote', 'Full-time',
        'Build and customise Shopify storefronts that convert.',
        ['2+ years of Shopify theme development (Liquid)', 'Experience with apps and checkout customisation', 'An eye for conversion detail'],
        ['Build and customise Shopify themes', 'Integrate apps and third-party tools', 'Improve store speed and conversion paths']),
    job('performance-marketing-manager', 'Marketing', 'Performance Marketing Manager', 'On-site', 'Full-time',
        'Plan, run and optimise paid campaigns that turn spend into measurable growth.',
        ['4+ years running Google Ads and Meta Ads', 'Strong analytics and reporting skills', 'A record of improving cost per lead or ROAS'],
        ['Plan campaign structure, audiences and budgets', 'Optimise creative, bidding and landing pages', 'Report results clearly to clients and the team']),
    job('social-media-executive', 'Marketing', 'Social Media Executive', 'On-site', 'Full-time',
        'Manage day-to-day social channels for client brands: planning, publishing and community.',
        ['1–3 years in social media management', 'Strong writing in English; Arabic is a plus', 'Comfort with Canva and short-form video tools'],
        ['Plan content calendars and publish posts', 'Respond to the community and track engagement', 'Prepare monthly performance summaries']),
    job('seo-specialist', 'SEO', 'SEO Specialist', 'Hybrid', 'Full-time',
        'Grow organic visibility for clients across classic search and AI search surfaces.',
        ['3+ years in technical and on-page SEO', 'Experience with Search Console, GA4 and crawling tools', 'Interest in GEO and AI search visibility'],
        ['Audit sites and prioritise technical fixes', 'Plan keyword and content strategy', 'Track rankings, traffic and leads']),
    job('content-writer', 'Content', 'Content Writer', 'Remote', 'Full-time',
        'Write clear, search-aware content that explains complex services simply.',
        ['2+ years of professional writing', 'Excellent English; SEO awareness', 'Ability to research unfamiliar topics quickly'],
        ['Write website copy, articles and case studies', 'Research topics and interview subject experts', 'Edit for clarity, accuracy and tone']),
]
