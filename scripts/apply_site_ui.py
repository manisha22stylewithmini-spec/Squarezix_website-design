"""Post-process every page so the whole site shares ONE button (assets/brand/btn-primary.pdf), the contact-us popup and the
quick-contact dock. Idempotent: run it after the page generators (they call it), or by hand: python3 scripts/apply_site_ui.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VER = '20261068a'
OLD_BTN = ('btn-contact', 'cmp-btn', 'hero-cta', 'cx-pager-btn', 'pf-more-btn')
KEEP = ('ss-faq-more', 'wu-cta', 'wf-cta', 'bl-loadmore', 'hero-cta', 'svh-cta')
OPENER_HREFS = ('#ab-contact', '#contact')


def swap_class(m):
    tag, attrs = m.group(1), m.group(0)
    cls = re.search(r'class="([^"]*)"', attrs)
    if not cls:
        return attrs
    tokens = cls.group(1).split()
    if not any(t in OLD_BTN or t == 'zx-btn' for t in tokens):
        return attrs
    new = ['zx-btn'] + [t for t in tokens if t in KEEP]
    out = attrs.replace(f'class="{cls.group(1)}"', f'class="{" ".join(dict.fromkeys(new))}"', 1)
    href = re.search(r'href="([^"]*)"', out)
    if tag == 'a' and href and href.group(1) in OPENER_HREFS and 'data-contact-open' not in out:
        out = out[:-1] + ' data-contact-open>'
    return out


def process(html):
    html = re.sub(r'<(a|button)\b[^>]*>', swap_class, html)
    if 'site-ui.css' not in html:
        html = html.replace('</head>', f'  <link rel="stylesheet" href="site-ui.css?v={VER}" />\n</head>', 1)
    else:
        html = re.sub(r'site-ui\.css\?v=\w+', f'site-ui.css?v={VER}', html)
    if 'site-ui.js' not in html:
        html = html.replace('</body>', f'  <script src="site-ui.js?v={VER}"></script>\n</body>', 1)
    else:
        html = re.sub(r'site-ui\.js\?v=\w+', f'site-ui.js?v={VER}', html)
    return html


def main():
    n = 0
    for f in sorted(ROOT.glob('*.html')):
        src = f.read_text()
        out = process(src)
        if out != src:
            f.write_text(out)
            n += 1
    print(f'apply_site_ui: updated {n} pages')


if __name__ == '__main__':
    main()
