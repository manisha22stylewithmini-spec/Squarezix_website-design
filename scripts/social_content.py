"""Social Media Marketing (social-media-marketing.html) rebuilt from the live squarezix.com/social-media-agency-dubai/ page:
live wording (frozen in social_raw.py), existing service-page components only."""
from social_raw import RAW as R
from local_seo_content import node

ART = ['leads', 'profile', 'threepack', 'authority', 'district']


def _answer(lines):
    return lines[0] if len(lines) == 1 else f'{lines[0]} ' + ', '.join(lines[1:]) + '.'


SOCIAL_PAGE = {
    'file': 'social-media-marketing.html', 'badge': 'Social Media Marketing', 'custom': True,
    'title': 'Social Media Agency in Dubai — Social Media Marketing | Squarezix',
    'h1': ['Social Media', 'Agency', 'in Dubai'], 'grad': 1,
    'lead': 'Creative social media posts, data-driven strategies and results that make an impact across every platform your audience uses.',
    'blog': ('Blogs', 'What’s going on <em>your Industry</em>', [(c, t) for c, t in R['posts']]),
    'sections': [
        ('statement', 'AI search', 'Your customers search smarter. <em>We make sure they find you.</em>', R['geo']),
        ('illus', 'Services', 'Social Media Marketing <em>Services</em>',
         {'intro': R['services_intro'], 'items': [(t, d, {'art': a}) for (t, d), a in zip(R['services'], ART)]}),
        ('bento', 'Reliable Solutions', 'Looking for a Social Media Marketing Agency <em>that delivers?</em>',
         {'intro': R['stand_intro'], 'items': [(t, d, {}) for t, d in R['stand']], 'grid': 'rem2'}),
        ('process', 'Reliable Solutions', 'Social Media Marketing <em>Agency in Dubai</em>',
         {'intro': R['agency_intro'], 'items': [node(t, 'Service', d, []) for t, d in R['svc10']]}, 'process'),
        ('cta', 'Be everywhere your audience is <em>searching</em> with Squarezix', R['cta_text']),
        ('faq', 'FAQs', 'Have questions about our <em>Social Media Services?</em>', [(q, _answer(a)) for q, a in R['faq']], R['still'][1]),
    ],
}
