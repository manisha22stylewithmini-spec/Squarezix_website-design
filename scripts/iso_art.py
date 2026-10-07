"""Isometric line-light illustrations ("Luminous Stratum") for card sections.

Each scene is plain inline SVG built on a 30° isometric lattice: dark violet glass slabs whose only
brilliance is a neon edge (violet -> blue -> lilac), a pool of light beneath, a few floating satellites
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
<linearGradient id="{k}-top" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2d1b62"/><stop offset="1" stop-color="#170f37"/></linearGradient>
<linearGradient id="{k}-top2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a2483"/><stop offset="1" stop-color="#1d1346"/></linearGradient>
<linearGradient id="{k}-hi" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9b7bff"/><stop offset="1" stop-color="#5a36cf"/></linearGradient>
<linearGradient id="{k}-hi2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c9bff"/><stop offset="1" stop-color="#4b3bd3"/></linearGradient>
<linearGradient id="{k}-l" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c1340"/><stop offset="1" stop-color="#0d0920"/></linearGradient>
<linearGradient id="{k}-r" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#271a58"/><stop offset="1" stop-color="#120c2c"/></linearGradient>
<linearGradient id="{k}-e" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c084fc"/><stop offset=".55" stop-color="#60a5fa"/><stop offset="1" stop-color="#ede9fe"/></linearGradient>
<linearGradient id="{k}-e2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
<linearGradient id="{k}-pin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9d5ff"/><stop offset=".45" stop-color="#a855f7"/><stop offset="1" stop-color="#4f46e5"/></linearGradient>
<linearGradient id="{k}-beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c4b5fd" stop-opacity="0"/><stop offset=".7" stop-color="#a78bfa" stop-opacity=".32"/><stop offset="1" stop-color="#60a5fa" stop-opacity=".5"/></linearGradient>
<radialGradient id="{k}-gP"><stop offset="0" stop-color="#8b5cf6" stop-opacity=".55"/><stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/></radialGradient>
<radialGradient id="{k}-gB"><stop offset="0" stop-color="#3b82f6" stop-opacity=".45"/><stop offset="1" stop-color="#3b82f6" stop-opacity="0"/></radialGradient>
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
    grid_lines = ''.join(f'<line x1="{v}" y1="15" x2="{v}" y2="135" stroke="#8b5cf6" stroke-width=".6" opacity=".25"{NS}/>'
                         f'<line x1="15" y1="{v}" x2="135" y2="{v}" stroke="#8b5cf6" stroke-width=".6" opacity=".25"{NS}/>' for v in range(15, 136, 30))
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


ART = {'maps': maps, 'profile': profile, 'geogrid': geogrid, 'leads': leads,
       'authority': authority, 'threepack': threepack, 'district': district, 'ai': ai}


def art(key):
    return ART[key]()


if __name__ == '__main__':      # preview sheet: python3 scripts/iso_art.py > /tmp/ix.html
    print('<body style="background:#08061a;display:grid;grid-template-columns:repeat(4,1fr);gap:10px">'
          + ''.join(f'<div style="background:#0f0b24">{art(k)}</div>' for k in ART) + '</body>')
