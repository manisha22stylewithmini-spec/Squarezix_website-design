"""Isometric line-light illustrations in the Squarezix palette (brand purple #621DD0 -> pink #AB24F2 -> lilac) ("Luminous Stratum") for card sections.

Each scene is plain inline SVG built on a 30° isometric lattice: dark violet glass slabs whose only
brilliance is a neon edge (brand pink -> lilac -> white), a pool of light beneath, a few floating satellites
and a scatter of stars. Ids are prefixed per scene so many can live on one page.
art(key) -> '<svg ...>'.  Motion classes (ix-float, ix-tw, ix-spin, ix-pulse) are animated in CSS.
"""
import random

C = 0.8660254
W, H = 480, 300


class Scene:
    def __init__(self, key, ox=240, oy=158):
        self.k, self.ox, self.oy, self.out = key, ox, oy, []

    # --- projection -------------------------------------------------------------------------
    def p(self, x, y, z=0):
        return self.ox + (x - y) * C, self.oy + (x + y) * 0.5 - z

    def pts(self, seq):
        return ' '.join(f'{X:.1f},{Y:.1f}' for X, Y in (self.p(*q) for q in seq))

    def add(self, *s):
        self.out.extend(s)
        return self

    # --- primitives -------------------------------------------------------------------------
    def box(self, x, y, z, w, d, h, top='top', edge=True, glow=False, inner=''):
        k = self.k
        T = [(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)]
        L = [(x, y + d, z + h), (x + w, y + d, z + h), (x + w, y + d, z), (x, y + d, z)]
        R = [(x + w, y, z + h), (x + w, y + d, z + h), (x + w, y + d, z), (x + w, y, z)]
        g = [f'<polygon points="{self.pts(L)}" fill="url(#{k}-l)"/>',
             f'<polygon points="{self.pts(R)}" fill="url(#{k}-r)"/>',
             f'<polygon points="{self.pts(T)}" fill="url(#{k}-{top})"/>']
        if edge:
            if glow:
                g.append(f'<polygon class="ix-pulse" points="{self.pts(T)}" fill="none" stroke="url(#{k}-e)" stroke-width="4" filter="url(#{k}-blur)"/>')
            g.append(f'<polygon points="{self.pts(T)}" fill="none" stroke="url(#{k}-e)" stroke-width="1.3" stroke-linejoin="round"/>')
            g.append(f'<polyline points="{self.pts([(x, y + d, z), (x + w, y + d, z), (x + w, y, z)])}" fill="none" stroke="url(#{k}-e2)" stroke-width="1" opacity=".6"/>')
            g.append(f'<polyline points="{self.pts([(x + w, y + d, z + h), (x + w, y + d, z)])}" fill="none" stroke="#c4b5fd" stroke-width=".8" opacity=".45"/>')
        if inner:
            g.append(self.plane(x, y, z + h, inner))
        return ''.join(g)

    def plane(self, x, y, z, inner):
        X, Y = self.p(x, y, z)
        return f'<g transform="matrix({C:.4f},0.5,{-C:.4f},0.5,{X:.1f},{Y:.1f})">{inner}</g>'

    def pool(self, x=0, y=0, rx=170, ry=70, kind='P', z=0):
        X, Y = self.p(x, y, z)
        return f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="{rx}" ry="{ry}" fill="url(#{self.k}-g{kind})"/>'

    def line(self, a, b, dash=True, op=.55):
        (X1, Y1), (X2, Y2) = self.p(*a), self.p(*b)
        da = ' stroke-dasharray="2 4"' if dash else ''
        return (f'<line x1="{X1:.1f}" y1="{Y1:.1f}" x2="{X2:.1f}" y2="{Y2:.1f}" stroke="url(#{self.k}-e2)" stroke-width="1.1"'
                f'{da} stroke-linecap="round" opacity="{op}"/>')

    def beam(self, x, y, z, height=110, width=26):
        X, Y = self.p(x, y, z)
        return f'<rect x="{X - width / 2:.1f}" y="{Y - height:.1f}" width="{width}" height="{height}" fill="url(#{self.k}-beam)" filter="url(#{self.k}-blur)"/>'

    def at(self, x, y, z, inner, cls='', delay=0):
        """2D artwork placed at an iso point (origin of `inner` sits on the point)."""
        X, Y = self.p(x, y, z)
        c = f' class="{cls}" style="animation-delay:{delay}s"' if cls else ''
        return f'<g{c}><g transform="translate({X:.1f},{Y:.1f})">{inner}</g></g>'

    def stars(self, n=26, seed=1):
        r = random.Random(seed)
        s = []
        for i in range(n):
            x, y = r.uniform(16, W - 16), r.uniform(10, H * 0.72)
            rad = r.choice([.7, .9, 1.1, 1.4, 1.9])
            op = r.uniform(.25, .9)
            tw = ' class="ix-tw" style="animation-delay:%.1fs"' % r.uniform(0, 4) if i % 3 == 0 else ''
            s.append(f'<circle{tw} cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="#fff" opacity="{op:.2f}"/>')
        return ''.join(s)

    # --- output -----------------------------------------------------------------------------
    def svg(self):
        k = self.k
        defs = f'''<defs>
<linearGradient id="{k}-top" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a1452"/><stop offset="1" stop-color="#140a2a"/></linearGradient>
<linearGradient id="{k}-top2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b1a74"/><stop offset="1" stop-color="#1c0e3c"/></linearGradient>
<linearGradient id="{k}-hi" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c47bff"/><stop offset="1" stop-color="#621dd0"/></linearGradient>
<linearGradient id="{k}-hi2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e2b8ff"/><stop offset="1" stop-color="#ab24f2"/></linearGradient>
<linearGradient id="{k}-l" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#190e33"/><stop offset="1" stop-color="#0a0716"/></linearGradient>
<linearGradient id="{k}-r" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#24124b"/><stop offset="1" stop-color="#100a24"/></linearGradient>
<linearGradient id="{k}-e" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ab24f2"/><stop offset=".55" stop-color="#c98bff"/><stop offset="1" stop-color="#f3e8ff"/></linearGradient>
<linearGradient id="{k}-e2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#621dd0"/><stop offset="1" stop-color="#ab24f2"/></linearGradient>
<linearGradient id="{k}-pin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3e8ff"/><stop offset=".45" stop-color="#ab24f2"/><stop offset="1" stop-color="#621dd0"/></linearGradient>
<linearGradient id="{k}-beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c4b5fd" stop-opacity="0"/><stop offset=".7" stop-color="#c98bff" stop-opacity=".3"/><stop offset="1" stop-color="#ab24f2" stop-opacity=".5"/></linearGradient>
<radialGradient id="{k}-gP"><stop offset="0" stop-color="#ab24f2" stop-opacity=".42"/><stop offset="1" stop-color="#ab24f2" stop-opacity="0"/></radialGradient>
<radialGradient id="{k}-gB"><stop offset="0" stop-color="#621dd0" stop-opacity=".5"/><stop offset="1" stop-color="#621dd0" stop-opacity="0"/></radialGradient>
<filter id="{k}-blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.2"/></filter>
<filter id="{k}-soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="9"/></filter>
</defs>'''
        return (f'<svg class="ix-svg" viewBox="32 18 416 260" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">'
                f'{defs}{"".join(self.out)}</svg>')


# --- small glyphs (drawn in unit space on a plane, or 2D at a point) ---------------------------
NS = ' vector-effect="non-scaling-stroke"'
WHITE = f'fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"{NS}'


def tile_icon(kind, w):
    c = w / 2
    if kind == 'star':
        r1, r2, pts = w * .3, w * .13, []
        import math
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            r = r1 if i % 2 == 0 else r2
            pts.append(f'{c + r * math.cos(a):.1f},{c + r * math.sin(a):.1f}')
        return f'<polygon points="{" ".join(pts)}" fill="#fff" opacity=".95"/>'
    if kind == 'route':
        return f'<path d="M{w*.22},{w*.75} C{w*.3},{w*.35} {w*.7},{w*.65} {w*.78},{w*.25}" {WHITE} stroke-dasharray="1.5 3"/><circle cx="{w*.78}" cy="{w*.25}" r="{w*.07}" fill="#fff"/>'
    if kind == 'phone':
        return f'<rect x="{w*.32}" y="{w*.2}" width="{w*.36}" height="{w*.6}" rx="{w*.08}" {WHITE}/><line x1="{w*.45}" y1="{w*.7}" x2="{w*.55}" y2="{w*.7}" {WHITE}/>'
    if kind == 'chat':
        return f'<path d="M{w*.22},{w*.3} h{w*.56} v{w*.34} h-{w*.3} l-{w*.14},{w*.12} v-{w*.12} h-{w*.12} z" {WHITE}/>'
    if kind == 'cal':
        return f'<rect x="{w*.22}" y="{w*.26}" width="{w*.56}" height="{w*.5}" rx="{w*.06}" {WHITE}/><line x1="{w*.22}" y1="{w*.42}" x2="{w*.78}" y2="{w*.42}" {WHITE}/><circle cx="{w*.4}" cy="{w*.58}" r="{w*.05}" fill="#fff"/>'
    if kind == 'camera':
        return f'<rect x="{w*.2}" y="{w*.32}" width="{w*.6}" height="{w*.42}" rx="{w*.07}" {WHITE}/><circle cx="{c}" cy="{w*.53}" r="{w*.12}" {WHITE}/>'
    if kind == 'check':
        return f'<path d="M{w*.26},{w*.5} L{w*.43},{w*.67} L{w*.75},{w*.33}" {WHITE}/>'
    if kind == 'power':
        return f'<path d="M{w*.34},{w*.3} A{w*.22},{w*.22} 0 1 0 {w*.66},{w*.3}" {WHITE}/><line x1="{c}" y1="{w*.2}" x2="{c}" y2="{w*.48}" {WHITE}/>'
    if kind == 'bolt':
        return f'<path d="M{w*.55},{w*.18} L{w*.3},{w*.55} H{w*.5} L{w*.44},{w*.82} L{w*.7},{w*.44} H{w*.5} Z" fill="#fff" opacity=".95"/>'
    if kind == 'cart':
        return f'<path d="M{w*.2},{w*.28} h{w*.12} l{w*.08},{w*.34} h{w*.3} l{w*.08},{w*.24}" {WHITE}/><circle cx="{w*.42}" cy="{w*.72}" r="{w*.04}" fill="#fff"/><circle cx="{w*.64}" cy="{w*.72}" r="{w*.04}" fill="#fff"/>'
    if kind == 'cloud':
        return f'<path d="M{w*.28},{w*.66} h{w*.4} a{w*.12},{w*.12} 0 0 0 {w*.02},-{w*.24} a{w*.17},{w*.17} 0 0 0 -{w*.32},{w*.04} a{w*.1},{w*.1} 0 0 0 -{w*.1},{w*.2} z" {WHITE}/>'
    if kind == 'bug':
        return f'<ellipse cx="{c}" cy="{w*.55}" rx="{w*.14}" ry="{w*.2}" {WHITE}/><path d="M{w*.36},{w*.45} h-{w*.12} M{w*.64},{w*.45} h{w*.12} M{w*.36},{w*.6} h-{w*.12} M{w*.64},{w*.6} h{w*.12} M{w*.42},{w*.3} l-{w*.06},-{w*.08} M{w*.58},{w*.3} l{w*.06},-{w*.08}" {WHITE}/>'
    if kind == 'x':
        return f'<path d="M{w*.3},{w*.3} L{w*.7},{w*.7} M{w*.7},{w*.3} L{w*.3},{w*.7}" {WHITE}/>'
    if kind == 'refresh':
        return f'<path d="M{w*.72},{w*.4} A{w*.22},{w*.22} 0 1 0 {w*.7},{w*.62}" {WHITE}/><path d="M{w*.74},{w*.22} V{w*.42} H{w*.54}" {WHITE}/>'
    if kind == 'link':
        return f'<rect x="{w*.18}" y="{w*.38}" width="{w*.36}" height="{w*.24}" rx="{w*.12}" {WHITE}/><rect x="{w*.46}" y="{w*.38}" width="{w*.36}" height="{w*.24}" rx="{w*.12}" {WHITE}/>'
    return ''


def label(text, x, y, size, op=1, weight=600):
    return (f'<text x="{x}" y="{y}" font-family="Sora, sans-serif" font-weight="{weight}" font-size="{size}" fill="#fff" '
            f'opacity="{op}" text-anchor="middle" dominant-baseline="central">{text}</text>')


def pin2d(k, s=1.0):
    return (f'<g transform="scale({s})"><path d="M0,-50 a19,19 0 0 1 19,19 c0,15 -19,33 -19,33 c0,0 -19,-18 -19,-33 a19,19 0 0 1 19,-19z" '
            f'fill="url(#{k}-pin)" filter="url(#{k}-blur)" opacity=".8"/>'
            f'<path d="M0,-50 a19,19 0 0 1 19,19 c0,15 -19,33 -19,33 c0,0 -19,-18 -19,-33 a19,19 0 0 1 19,-19z" fill="url(#{k}-pin)" stroke="#ede9fe" stroke-width="1"/>'
            f'<circle cx="0" cy="-31" r="7" fill="#170f37"/><circle cx="0" cy="-31" r="2.6" fill="#fff"/></g>')


def sparkle(k, r=16):
    d = f'M0,-{r} C{r*.18},-{r*.18} {r*.18},-{r*.18} {r},0 C{r*.18},{r*.18} {r*.18},{r*.18} 0,{r} C-{r*.18},{r*.18} -{r*.18},{r*.18} -{r},0 C-{r*.18},-{r*.18} -{r*.18},-{r*.18} 0,-{r}z'
    return f'<path d="{d}" fill="url(#{k}-pin)" filter="url(#{k}-blur)"/><path d="{d}" fill="#f5f3ff"/>'


# --- scenes ---------------------------------------------------------------------------------
def maps():
    s = Scene('ixa')
    s.add(s.stars(28, 11), s.pool(0, 0, 190, 78, 'B'), s.pool(0, 0, 130, 55, 'P'))
    DASH = ' stroke-dasharray="2 5"'
    rings = ''.join(f'<circle cx="0" cy="0" r="{r}" fill="none" stroke="url(#ixa-e)" stroke-width="1.2" opacity="{o}"{NS}{DASH if da else ""}/>'
                    for r, o, da in ((18, .9, 0), (30, .55, 0), (42, .35, 1)))
    s.add(s.box(-72, -72, 0, 144, 144, 10, glow=True),
          s.box(-48, -48, 10, 96, 96, 6, top='top2', inner=f'<g transform="translate(48,48)">{rings}</g>'),
          s.beam(0, 0, 16, 104, 22),
          s.at(0, 0, 58, pin2d('ixa'), 'ix-float'),
          f'<g class="ix-float" style="animation-delay:-2s">{s.box(52, -100, 44, 28, 28, 6, top="hi", inner=tile_icon("star", 28))}</g>',
          f'<g class="ix-float" style="animation-delay:-4s">{s.box(-104, 44, 30, 26, 26, 5, top="hi2", inner=tile_icon("route", 26))}</g>')
    return s.svg()


def profile():
    s = Scene('ixb', oy=172)
    s.add(s.stars(26, 21), s.pool(0, 0, 190, 70, 'B'), s.pool(0, -10, 120, 50, 'P'))
    for i in range(4):
        top = i == 3
        inner = ''
        if top:
            stars_row = ''.join(f'<g transform="translate({52 + j * 11},20) scale(.34)">{tile_icon("star", 28)}</g>' for j in range(5))
            inner = (f'<circle cx="18" cy="20" r="9" fill="#c4b5fd"/><rect x="34" y="12" width="44" height="5" rx="2.5" fill="#ede9fe" opacity=".9"/>'
                     f'<rect x="34" y="22" width="0" height="0"/>{stars_row}'
                     f'<rect x="12" y="40" width="96" height="4" rx="2" fill="#a78bfa" opacity=".55"/><rect x="12" y="50" width="70" height="4" rx="2" fill="#a78bfa" opacity=".4"/>'
                     f'<rect x="12" y="60" width="84" height="4" rx="2" fill="#a78bfa" opacity=".3"/>')
        s.add(s.box(-60 + i * 4, -40 - i * 4, i * 15, 120, 80, 3, top='top2' if top else 'top', glow=top, inner=inner))
    s.add(f'<g class="ix-float" style="animation-delay:-1.5s">{s.box(70, -84, 58, 24, 24, 5, top="hi2", inner=tile_icon("camera", 24))}</g>',
          f'<g class="ix-float" style="animation-delay:-3.5s">{s.box(-108, 30, 36, 22, 22, 5, top="hi", inner=tile_icon("check", 22))}</g>')
    return s.svg()


def geogrid():
    s = Scene('ixc', oy=150)
    s.add(s.stars(26, 31), s.pool(0, 0, 200, 80, 'B'), s.pool(0, 0, 130, 55, 'P'))
    dots = []
    ranks = {(0, 0): ('1', 11, 1), (30, -30): ('2', 8.5, .88), (-30, 30): ('3', 8.5, .88), (30, 30): ('5', 7, .62), (-60, -30): ('9', 6, .45), (60, 0): ('4', 7, .72)}
    for gx in range(-60, 61, 30):
        for gy in range(-60, 61, 30):
            if (gx, gy) in ranks:
                t, r, o = ranks[(gx, gy)]
                dots.append(f'<circle cx="{gx + 75}" cy="{gy + 75}" r="{r}" fill="url(#ixc-hi)" opacity="{o}"/>'
                            f'<circle cx="{gx + 75}" cy="{gy + 75}" r="{r}" fill="none" stroke="#ede9fe" stroke-width=".8" opacity="{o}"{NS}/>'
                            + label(t, gx + 75, gy + 75, r * 1.05, o))
            else:
                dots.append(f'<circle cx="{gx + 75}" cy="{gy + 75}" r="2.4" fill="#c4b5fd" opacity=".35"/>')
    grid_lines = ''.join(f'<line x1="{v}" y1="15" x2="{v}" y2="135" stroke="#ab24f2" stroke-width=".6" opacity=".22"{NS}/>'
                         f'<line x1="15" y1="{v}" x2="135" y2="{v}" stroke="#ab24f2" stroke-width=".6" opacity=".22"{NS}/>' for v in range(15, 136, 30))
    scan = f'<g transform="translate(75,75)"><g class="ix-spin"><circle r="44" fill="none" stroke="url(#ixc-e)" stroke-width="1.4" stroke-dasharray="40 236"{NS}/></g></g>'
    s.add(s.box(-75, -75, 0, 150, 150, 8, glow=True, inner=grid_lines + ''.join(dots) + scan),
          s.at(0, 0, 66, pin2d('ixc', .62), 'ix-float', -1))
    return s.svg()


def leads():
    s = Scene('ixd', oy=165)
    s.add(s.stars(26, 41), s.pool(0, 0, 200, 78, 'B'), s.pool(0, 0, 120, 52, 'P'))
    hub = (0, 0, 14)
    s.add(s.box(-55, -55, 0, 110, 110, 8, glow=True),
          s.box(-30, -30, 8, 60, 60, 6, top='top2'))
    for (x, y, z, ic, top, dl) in ((-120, -20, 46, 'phone', 'hi', -1), (40, -122, 54, 'chat', 'hi2', -3), (82, 40, 30, 'cal', 'hi', -5)):
        s.add(s.line((x + 14, y + 14, z), hub))
        s.add(f'<g class="ix-float" style="animation-delay:{dl}s">{s.box(x, y, z, 28, 28, 6, top=top, inner=tile_icon(ic, 28))}</g>')
    arrow = ('<path d="M-26,10 L-8,-6 L4,4 L24,-18" fill="none" stroke="url(#ixd-e)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" filter="url(#ixd-blur)" opacity=".8"/>'
             '<path d="M-26,10 L-8,-6 L4,4 L24,-18" fill="none" stroke="#f5f3ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
             '<path d="M12,-19 L25,-19 L25,-6" fill="none" stroke="#f5f3ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    s.add(s.beam(0, 0, 14, 70, 18), s.at(0, 0, 50, arrow, 'ix-float', -2))
    return s.svg()


def authority():
    s = Scene('ixe', oy=150)
    s.add(s.stars(26, 51), s.pool(0, 0, 200, 80, 'B'), s.pool(0, 0, 120, 52, 'P'))
    nodes = [(-100, 0), (0, -100), (100, 0), (0, 100)]
    for nx, ny in nodes[:2]:
        s.add(s.line((nx, ny, 0), (0, 0, 0)), s.box(nx - 9, ny - 9, 0, 18, 18, 4, top='hi2', inner=tile_icon('link', 18)))
    s.add(s.box(-58, -58, 0, 116, 116, 8, glow=True))
    for nx, ny in nodes[2:]:
        s.add(s.line((nx, ny, 0), (0, 0, 8)), s.box(nx - 9, ny - 9, 0, 18, 18, 4, top='hi', inner=tile_icon('link', 18)))
    shield = ('<path d="M0,-44 L30,-33 V-8 C30,12 15,24 0,32 C-15,24 -30,12 -30,-8 V-33 Z" fill="url(#ixe-pin)" filter="url(#ixe-blur)" opacity=".75"/>'
              '<path d="M0,-44 L30,-33 V-8 C30,12 15,24 0,32 C-15,24 -30,12 -30,-8 V-33 Z" fill="url(#ixe-pin)" stroke="#ede9fe" stroke-width="1"/>'
              '<path d="M-11,-6 L-2,3 L13,-14" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>')
    s.add(s.beam(0, 0, 8, 80, 22), s.at(0, 0, 56, shield, 'ix-float', -1.5))
    return s.svg()


def threepack():
    s = Scene('ixf', oy=170)
    s.add(s.stars(26, 61), s.pool(0, 0, 210, 78, 'B'), s.pool(30, -20, 120, 52, 'P'))
    s.add(s.box(-100, -32, 0, 210, 64, 6))
    for i, (h, n, top) in enumerate(((18, '3', 'top'), (34, '2', 'top2'), (52, '1', 'hi'))):
        x = -92 + i * 66
        s.add(s.box(x, -24, 6, 58, 48, h, top=top, glow=(n == '1'), inner=label(n, 29, 24, 20 if n == '1' else 16, 1 if n == '1' else .75)))
    s.add(s.at(-92 + 2 * 66 + 29, 0, 6 + 52 + 34, sparkle('ixf', 13), 'ix-float', -2))
    return s.svg()


def district():
    s = Scene('ixg', oy=172)
    s.add(s.stars(26, 71), s.pool(0, 0, 200, 78, 'B'), s.pool(0, 0, 130, 55, 'P'))
    s.add(s.box(-60, -60, 0, 120, 120, 6, glow=True))
    heights = [[18, 40, 26], [30, 64, 22], [14, 34, 48]]
    order = sorted(((i, j) for i in range(3) for j in range(3)), key=lambda t: t[0] + t[1])
    for i, j in order:
        h = heights[i][j]
        tall = h == 64
        s.add(s.box(-51 + i * 36, -51 + j * 36, 6, 30, 30, h, top='hi' if tall else ('top2' if h > 30 else 'top'), glow=tall))
    s.add(s.at(-51 + 36 + 15, -51 + 36 + 15, 6 + 64 + 22, pin2d('ixg', .52), 'ix-float', -1),
          s.at(-51 + 72 + 15, -51 + 72 + 15, 6 + 48 + 26, pin2d('ixg', .42), 'ix-float', -3.2))
    return s.svg()


def ai():
    s = Scene('ixh', oy=160)
    s.add(s.stars(28, 81), s.pool(0, 0, 200, 80, 'B'), s.pool(0, 0, 130, 55, 'P'))
    pins = []
    for k in range(5):
        o = 28 + k * 14
        pins.append(f'<rect x="{o}" y="8" width="6" height="12" rx="1" fill="#a78bfa" opacity=".7"/>'
                    f'<rect x="{o}" y="100" width="6" height="12" rx="1" fill="#a78bfa" opacity=".7"/>'
                    f'<rect x="8" y="{o}" width="12" height="6" rx="1" fill="#a78bfa" opacity=".7"/>'
                    f'<rect x="100" y="{o}" width="12" height="6" rx="1" fill="#a78bfa" opacity=".7"/>')
    orbit = f'<circle cx="60" cy="60" r="56" fill="none" stroke="url(#ixh-e)" stroke-width="1" stroke-dasharray="2 5" opacity=".6"{NS}/>'
    s.add(s.box(-60, -60, 0, 120, 120, 8, glow=True, inner=orbit + ''.join(pins)),
          s.box(-38, -38, 8, 76, 76, 12, top='hi', glow=True,
                inner=f'<rect x="10" y="10" width="56" height="56" rx="6" fill="none" stroke="#ede9fe" stroke-width="1" opacity=".7"{NS}/>' + label('AI', 38, 38, 22)),
          s.beam(0, 0, 20, 70, 20),
          s.at(0, 0, 66, sparkle('ixh', 15), 'ix-float', -2))
    return s.svg()


def base(key, seed, oy=165, pools=(200, 78)):
    s = Scene(key, oy=oy)
    s.add(s.stars(26, seed), s.pool(0, 0, pools[0], pools[1], 'B'), s.pool(0, 0, 120, 52, 'P'))
    return s


def server():
    s = base('ixi', 91)
    s.add(s.box(-100, -36, 0, 200, 72, 5))
    for i, (h, top) in enumerate(((34, 'top'), (50, 'top2'), (34, 'top'))):
        x = -92 + i * 64
        dots = ''.join(f'<circle cx="{12 + j * 10}" cy="48" r="2.4" fill="#c4b5fd" opacity="{.9 if j < 2 else .35}"/>' for j in range(4))
        bars = '<rect x="10" y="12" width="36" height="5" rx="2.5" fill="#a78bfa" opacity=".5"/><rect x="10" y="24" width="36" height="5" rx="2.5" fill="#a78bfa" opacity=".35"/>'
        inner = dots + bars + (label('!', 28, 28, 22) if i == 1 else '')
        s.add(s.box(x, -28, 5, 56, 56, h, top=top if i != 1 else 'hi', glow=(i == 1), inner=inner))
    s.add(s.beam(0, 0, 55, 60, 18),
          f'<g class="ix-float" style="animation-delay:-1.5s">{s.box(-14, -14, 78, 28, 28, 6, top="hi2", inner=tile_icon("power", 28))}</g>')
    return s.svg()


def speed():
    s = base('ixj', 92)
    gauge = ('<path d="M18,84 A52,52 0 0 1 122,84" fill="none" stroke="#3b1a74" stroke-width="10" stroke-linecap="round"/>'
             '<path d="M18,84 A52,52 0 0 1 100,41" fill="none" stroke="url(#ixj-e)" stroke-width="10" stroke-linecap="round"/>'
             '<line x1="70" y1="84" x2="100" y2="54" stroke="#fff" stroke-width="3" stroke-linecap="round"/><circle cx="70" cy="84" r="6" fill="#fff"/>')
    s.add(s.box(-70, -60, 0, 140, 120, 8, glow=True, inner=gauge),
          f'<g class="ix-float" style="animation-delay:-2s">{s.box(70, -96, 40, 28, 28, 6, top="hi", inner=tile_icon("bolt", 28))}</g>',
          f'<g class="ix-float" style="animation-delay:-4s">{s.box(-112, 34, 28, 24, 24, 5, top="hi2", inner=tile_icon("check", 24))}</g>')
    return s.svg()


def lock():
    s = base('ixk', 93, oy=152)
    s.add(s.box(-60, -60, 0, 120, 120, 8, glow=True))
    for nx, ny in ((-100, 0), (100, 0)):
        s.add(s.line((nx, ny, 0), (0, 0, 8)), s.box(nx - 9, ny - 9, 0, 18, 18, 4, top='hi2', inner=tile_icon('check', 18)))
    padlock = ('<path d="M-17,-8 V-22 a17,17 0 0 1 34,0 V-8" fill="none" stroke="#ede9fe" stroke-width="5" stroke-linecap="round"/>'
               '<rect x="-27" y="-10" width="54" height="42" rx="9" fill="url(#ixk-pin)" stroke="#ede9fe" stroke-width="1"/>'
               '<circle cx="0" cy="8" r="5.5" fill="#170f37"/><rect x="-1.8" y="10" width="3.6" height="9" rx="1.8" fill="#170f37"/>')
    s.add(s.beam(0, 0, 8, 80, 22), s.at(0, 0, 50, padlock, 'ix-float', -1.5))
    return s.svg()


def payment():
    s = base('ixl', 94)
    card = ('<rect x="8" y="10" width="104" height="14" fill="#140a2a" opacity=".85"/><rect x="12" y="44" width="40" height="8" rx="2" fill="#ede9fe" opacity=".85"/>'
            '<rect x="12" y="58" width="64" height="5" rx="2.5" fill="#a78bfa" opacity=".5"/><circle cx="92" cy="58" r="9" fill="#ab24f2" opacity=".9"/><circle cx="102" cy="58" r="9" fill="#c98bff" opacity=".8"/>')
    s.add(s.box(-80, -55, 0, 160, 110, 6),
          s.box(-60, -40, 6, 120, 80, 4, top='top2', glow=True, inner=card),
          f'<g class="ix-float" style="animation-delay:-1s">{s.box(58, -96, 44, 28, 28, 6, top="hi", inner=tile_icon("cart", 28))}</g>',
          f'<g class="ix-float" style="animation-delay:-3.5s">{s.box(-112, 40, 30, 24, 24, 5, top="hi2", inner=tile_icon("check", 24))}</g>')
    return s.svg()


def backup():
    s = base('ixm', 95)
    s.add(s.box(-62, -62, 0, 124, 124, 6))
    for i in range(3):
        top = 'hi' if i == 2 else 'top2'
        inner = '<rect x="14" y="40" width="40" height="5" rx="2.5" fill="#a78bfa" opacity=".6"/><circle cx="92" cy="43" r="3.2" fill="#e2b8ff"/>' if i == 2 else ''
        s.add(s.box(-48, -48, 6 + i * 20, 96, 96, 14, top=top, glow=(i == 2), inner=inner))
    s.add(s.beam(0, 0, 70, 60, 18),
          f'<g class="ix-float" style="animation-delay:-2s">{s.box(-14, -14, 100, 28, 28, 6, top="hi2", inner=tile_icon("cloud", 28))}</g>',
          f'<g class="ix-float" style="animation-delay:-4s">{s.box(70, 44, 28, 24, 24, 5, top="hi", inner=tile_icon("refresh", 24))}</g>')
    return s.svg()


def brokenlink():
    s = base('ixn', 96)
    s.add(s.box(-100, -48, 0, 200, 96, 6, glow=True))
    s.add(s.box(-88, -14, 6, 70, 28, 12, top='hi', inner=tile_icon('link', 28) if False else ''),
          s.box(18, -14, 6, 70, 28, 12, top='hi2'))
    s.add(s.at(-53, 0, 26, '<rect x="-24" y="-9" width="34" height="18" rx="9" fill="none" stroke="#fff" stroke-width="2.4"/>', 'ix-float', -1),
          s.at(53, 0, 26, '<rect x="-10" y="-9" width="34" height="18" rx="9" fill="none" stroke="#fff" stroke-width="2.4"/>', 'ix-float', -3))
    s.add(s.at(0, 0, 34, '<path d="M-7,-7 L7,7 M7,-7 L-7,7" stroke="#e2b8ff" stroke-width="3" stroke-linecap="round"/>', 'ix-pulse'),
          s.beam(0, 0, 8, 52, 16))
    return s.svg()


def forms():
    s = base('ixo', 97)
    ui = ('<rect x="12" y="12" width="50" height="6" rx="3" fill="#ede9fe" opacity=".9"/>'
          '<rect x="12" y="26" width="96" height="14" rx="4" fill="#140a2a" stroke="#a78bfa" stroke-width="1" opacity=".95"/>'
          '<rect x="12" y="48" width="96" height="14" rx="4" fill="#140a2a" stroke="#a78bfa" stroke-width="1" opacity=".95"/>'
          '<rect x="12" y="70" width="42" height="14" rx="7" fill="url(#ixo-pin)"/>')
    s.add(s.box(-72, -52, 0, 144, 104, 6),
          s.box(-60, -42, 6, 120, 96, 5, top='top2', glow=True, inner=ui),
          f'<g class="ix-float" style="animation-delay:-1.5s">{s.box(64, -92, 46, 26, 26, 6, top="hi", inner=tile_icon("check", 26))}</g>')
    return s.svg()


def browsers():
    s = base('ixp', 98, oy=170)
    s.add(s.box(-96, -40, 0, 192, 80, 5))
    for i, top in enumerate(('top', 'top2', 'hi')):
        x = -88 + i * 62
        bar = f'<rect x="0" y="0" width="52" height="9" fill="#140a2a" opacity=".9"/><circle cx="7" cy="4.5" r="2" fill="#c98bff"/><circle cx="14" cy="4.5" r="2" fill="#a78bfa"/>'
        body = '<rect x="8" y="18" width="36" height="5" rx="2.5" fill="#a78bfa" opacity=".55"/><rect x="8" y="30" width="26" height="5" rx="2.5" fill="#a78bfa" opacity=".4"/>'
        s.add(s.box(x, -30, 5, 54, 60, 8 + i * 10, top=top, glow=(i == 2), inner=bar + body))
    s.add(f'<g class="ix-float" style="animation-delay:-2s">{s.box(-14, -14, 70, 28, 28, 6, top="hi2", inner=tile_icon("check", 28))}</g>')
    return s.svg()


def firewall():
    s = base('ixq', 99, oy=165)
    s.add(s.box(-90, -40, 0, 180, 80, 6))
    for i in range(4):
        s.add(s.box(-84 + i * 42, -22, 6, 38, 44, 26 + (i % 2) * 14, top='hi' if i == 1 else 'top2', glow=(i == 1)))
    shield = ('<path d="M0,-34 L24,-26 V-6 C24,10 12,19 0,25 C-12,19 -24,10 -24,-6 V-26 Z" fill="url(#ixq-pin)" filter="url(#ixq-blur)" opacity=".75"/>'
              '<path d="M0,-34 L24,-26 V-6 C24,10 12,19 0,25 C-12,19 -24,10 -24,-6 V-26 Z" fill="url(#ixq-pin)" stroke="#ede9fe" stroke-width="1"/>'
              '<path d="M-9,-4 L-2,3 L11,-11" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    s.add(s.at(0, 0, 80, shield, 'ix-float', -1.5),
          f'<g class="ix-float" style="animation-delay:-3s">{s.box(88, -70, 40, 24, 24, 5, top="hi2", inner=tile_icon("bug", 24))}</g>')
    return s.svg()


def updates():
    s = base('ixr', 100)
    s.add(s.box(-62, -62, 0, 124, 124, 6, glow=True))
    for i, top in enumerate(('top', 'top2')):
        s.add(s.box(-44, -44, 6 + i * 12, 88, 88, 8, top=top))
    ring = ('<circle cx="0" cy="0" r="24" fill="none" stroke="url(#ixr-e)" stroke-width="5" stroke-dasharray="110 40" stroke-linecap="round"/>'
            '<path d="M18,-24 L30,-14 L14,-10 Z" fill="#f5f3ff"/>')
    s.add(s.beam(0, 0, 26, 60, 18), s.at(0, 0, 50, ring, 'ix-float', -1),
          f'<g class="ix-float" style="animation-delay:-2.5s">{s.box(64, 40, 30, 24, 24, 5, top="hi", inner=tile_icon("check", 24))}</g>')
    return s.svg()


ART = {'maps': maps, 'profile': profile, 'geogrid': geogrid, 'leads': leads,
       'authority': authority, 'threepack': threepack, 'district': district, 'ai': ai,
       'server': server, 'speed': speed, 'lock': lock, 'payment': payment, 'backup': backup, 'brokenlink': brokenlink,
       'forms': forms, 'browsers': browsers, 'firewall': firewall, 'updates': updates}


def art(key):
    return ART[key]()


if __name__ == '__main__':      # preview sheet: python3 scripts/iso_art.py > /tmp/ix.html
    print('<body style="background:#08061a;display:grid;grid-template-columns:repeat(4,1fr);gap:10px">'
          + ''.join(f'<div style="background:#0f0b24">{art(k)}</div>' for k in ART) + '</body>')
