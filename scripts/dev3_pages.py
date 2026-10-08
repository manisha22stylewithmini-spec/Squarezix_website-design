"""ERP Customization, Website Migration Services and Headless Ecommerce Development: sub-inner pages built from the live
squarezix.com wording (frozen in dev3_raw.py) on the existing service-page components only (no new sections).

Wording is the live page's. Only the small section labels (badges) the live page does not have are ours, marked LABEL."""
from dev3_raw import RAW
from local_seo_content import node

ERP, HEC, MIG = RAW['ERP'], RAW['HEC'], RAW['MIG']
CTA_TITLE = 'Be everywhere your audience is <em>searching</em> with Squarezix'


def _blog(cat, posts):
    return ('Blogs', 'What’s going on <em>your Industry</em>', [(cat, t) for t in posts])


# ---------------------------------------------------------------- ERP Customization
ERP_PAGE = dict(
    name='ERP Customization', parent='web', source='live',
    h1=['ERP', 'Customization', 'Dubai'], badge='ERP',
    lead=ERP['intro_title'],
    intro=ERP['intro'][0], nodes=[], feats=[], faq=ERP['faq'],
    live=dict(blog=_blog(ERP['blog_cat'], ERP['posts'])),
    layout=[
        ('statement', 'Why Choose Squarezix', 'ERP Customization and <em>Implementation for Businesses in Dubai</em>', ' '.join(ERP['intro'])),
        ('nodes', 'ERP Modules', 'Our <em>ERP Modules</em>',
         {'intro': ERP['modules_intro'], 'items': [node(t, 'Module', d, []) for t, d in ERP['modules']]}, 'services'),
        ('process', 'Process', 'Our <em>ERP Customization Process</em>',
         {'intro': '', 'items': [node(t, f'Step {i}', d, []) for i, (t, d) in enumerate(ERP['steps'], 1)]}, 'process'),
        ('industries', 'Industries', 'Industries We Serve with <em>Tailored ERP Systems in the UAE</em>',
         {'intro': '', 'items': [(t, '', []) for t in ERP['industries']]}),
        ('cta', CTA_TITLE, ERP['cta_text']),
        ('faq', 'FAQs', 'Personalizing <em>Your ERP</em>', ERP['faq'], ERP['still'][1]),
    ])

# ---------------------------------------------------------------- Headless Ecommerce Development
HEC_PAGE = dict(
    name='Headless Ecommerce Development', parent='web', source='live',
    h1=['Headless Ecommerce', 'Development', 'Services'], badge='Ecommerce Development',
    lead='Your customers search smarter. We make sure they find you. Squarezix helps your brand show up in these AI-driven answers—building visibility, trust, and influence where it matters most.',
    intro=HEC['best_intro'],
    nodes=[(t, 'Platform', d, []) for t, d in HEC['platforms']],
    trust={'intro': HEC['trust_intro'], 'items': [(t, d, []) for t, d in HEC['trust']]},
    stand={'intro': HEC['stand_intro'], 'items': [(t, d, []) for t, d in HEC['stand']]},
    live=dict(
        nostatement=True,
        ind=('Industries we serve', 'SquareZix Proudly Develops <em>Headless CMS Websites for Businesses Across Multiple Industries</em>'),
        nodes_title='Best Headless Ecommerce <em>Development Company in Dubai</em>',
        flow=('Methodology', 'Our Proven <em>Headless Ecommerce Development Workflow</em>'),
        cta_text=HEC['cta_text'],
        faq_title='Have Questions about <em>Headless Ecommerce Development?</em>',
        faq_intro=HEC['faq_intro'],
        blog=('Blogs', 'What’s going on <em>your Industry</em>', [
            ('Website Development', 'Is DataLife Engine Still a Good CMS for Modern Websites?'),
            ('Website Development', 'Shopify Storefronts Now Support UCP: Is Your Ecommerce Website Ready for AI Shopping Agents?'),
            ('Website Development', 'Why Payload CMS Is Becoming a Powerful Choice for Next.js Websites'),
            ('Website Development', 'Can GPT-6 Astra Build Websites? What Businesses Need to Know')])),
    flow=HEC['flow'],
    industries={'intro': '', 'items': [(t, '', []) for t in HEC['industries']]},
    faq=HEC['faq'])


# ---------------------------------------------------------------- Website Migration Services
def _split(block):
    """Block paragraphs before its first list (+ the list's label) / the list items / the paragraphs after it."""
    before = [p for p, n in block['paras'] if n == 0]
    after = [p for p, n in block['paras'] if n > 0]
    labels = [a for a, _ in block['lists']]
    items = [x for _, c in block['lists'] for x in c]
    return before, labels, items, after


def _card(block, tag):
    before, labels, items, after = _split(block)
    desc = ' '.join(before + labels[:1])
    return node(block['title'], tag, desc, items, ' '.join(after))


def _stand(block):
    before, labels, items, after = _split(block)
    meta = {'lead': ' '.join(before + labels[:1]), 'close': ' '.join(after)}
    if items:
        meta['chips'] = items
        return (block['title'], '', meta)
    return (block['title'], ' '.join(before + after), {})


MIG_ART = ['server', 'backup', 'authority', 'lock', 'brokenlink', 'speed', 'browsers', 'geogrid']
MIG_PAGE = dict(
    name='Website Migration Services', parent='web', source='live',
    h1=['Migrate Your Website Without', 'Downtime, Data Loss,', 'or SEO Rankings'], badge='Website Migration Services',
    lead=MIG['lead'].strip(), intro=MIG['sol_intro'], nodes=[], feats=[], faq=[], noblog=True,
    live=dict(blog=None),
    layout=[
        # LABEL: 'Website Migration' and 'Free consultation' badges are ours (the live page has no label there)
        ('statement', 'Website Migration', 'Ready for Your <em>Next Website Move?</em>', MIG['ready'].strip()),
        ('compare', 'Planning', 'Why Your Business Needs Strategic <em>Website Migration</em>',
         {'intro': '',
          'left': {'dim': 'Without proper', 'title': 'planning, a migration can result in:', 'chips': MIG['without'][1], 'link': ('#process', 'See how we fix it')},
          'right': {'title': 'Strategic Website Migration', 'text': MIG['plan'][0], 'hub': 'Migration',
                    'keywords': ['Detailed planning', 'URL redirect mapping', 'Database validation', 'Technical SEO implementation', 'Continuous monitoring'],
                    'tag': 'Structured migration methodology', 'cta': ('#ab-contact', 'Talk to our team')}}),
        ('illus', 'Expectations', 'What You <em>Can Expect</em>',
         {'intro': '', 'items': [(t, '', {'art': a}) for t, a in zip(MIG['expect'], MIG_ART)]}),
        ('statement', 'Free consultation', 'Ready to migrate your website <em>with confidence?</em>', 'Speak with our migration experts today for a free consultation.'),
        ('process', 'Secure Process', 'Our Secure 7-Step <em>Website Migration Process</em>',
         {'intro': MIG['proc_intro'], 'items': [_card(b, f'Step {i}') for i, b in enumerate(MIG['proc'], 1)]}, 'process'),
        ('bento', 'Why Choose Squarezix', 'Why Choose SquareZix for <em>Website Migration Services?</em>',
         {'intro': MIG['why_intro'], 'items': [_stand(b) for b in MIG['why']]}),
        ('nodes', 'Our Solutions', 'Comprehensive <em>Website Migration Solutions</em>',
         {'intro': MIG['sol_intro'], 'items': [_card(b, 'Migration') for b in MIG['sol']]}, 'services'),
        ('cta', MIG['be_title'].replace('Be Found Where Your Customers Are Searching with Squarezix',
                                        'Be Found Where Your Customers Are <em>Searching</em> with Squarezix'), MIG['be']),
        ('statement', 'Our approach to AI-driven visibility', 'The Squarezix Way to <em>AI Visibility</em>', MIG['way']),
    ])

PAGES = [ERP_PAGE, HEC_PAGE, MIG_PAGE]
