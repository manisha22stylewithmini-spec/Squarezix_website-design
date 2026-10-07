"""Website Management Services page: the live squarezix.com/website-management-services/ wording
(frozen in live_content.py under LIVE['web']) on the locked components."""
from live_content import LIVE
from local_seo_content import node

W = LIVE['web']


def cards(sec, last_wide=True):
    items = W[sec]['items']
    return [(t, d, {'wide': True} if last_wide and i == len(items) - 1 else {}) for i, (t, d, _b) in enumerate(items)]


SERVICES = [node(t, 'Service', d, []) for t, d, _b in W['maintain']['items']]
FAQ = [(q, a) for q, a in W['mfaq']]

WM_LAYOUT = [
    ('statement', 'AI Search', 'Your Customers Search Smarter. <em>We Make Sure They Find You.</em>',
     'Squarezix helps your brand show up in these AI-driven answers—building visibility, trust, and influence where it matters most. Our Generative Engine Optimization (GEO) strategies ensure your business is discovered, recommended, and chosen—across AI platforms and next-generation search experiences.'),
    ('nodes', 'Our Services', 'How do we maintain <em>Your Website</em>', {'intro': W['maintain']['intro'], 'items': SERVICES}, 'services'),
    ('bento', 'Reliable Solutions', 'What Sets Squarezix Apart in <em>Website Maintenance Services</em>',
     {'intro': W['mwhy']['intro'], 'items': cards('mwhy')}),
    ('bento', 'Website Issues', 'Keep Your Business Website <em>Secure and High-Performing</em>',
     {'intro': W['fixes']['intro'], 'items': cards('fixes')}),
    ('bento', 'Why Choose Squarezix', 'Why Choose Squarezix as your <em>website maintenance partner?</em>',
     {'intro': W['mwhy2']['intro'], 'items': cards('mwhy2', last_wide=False), 'grid': 'b6'}),
    ('cta', 'Be Everywhere Your Audience is <em>Searching with Squarezix</em>', 'Connect with our AI experts to drive more leads from SEO in the AI-Era.'),
    ('faq', 'FAQs', 'Have questions about managing <em>your website effectively?</em>', FAQ,
     'Still have questions? Our team is here to help you find the right solution for your business.'),
]

WM_HERO = dict(
    badge='Website Management Services',
    h1=['Website', 'Management'],
    lead='Website Management Company in Dubai',
)
WM_BLOG = ('Blogs', 'What’s going on <em>your Industry</em>', [
    ('Website Development', 'Is DataLife Engine Still a Good CMS for Modern Websites?'),
    ('Website Development', 'Shopify Storefronts Now Support UCP: Is Your Ecommerce Website Ready for AI Shopping Agents?'),
    ('Website Management', 'How to Design Product Filters for Jewellery Ecommerce Stores Without Losing Sales'),
    ('Website Development', 'Why Payload CMS Is Becoming a Powerful Choice for Next.js Websites')])
