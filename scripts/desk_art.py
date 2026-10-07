"""Top-down 'portfolio at work' desk scene for the portfolio timeline (inline SVG, brand palette, no text)."""


def desk():
    keys = ''.join(f'<rect x="{262 + c * 18.5}" y="{6 + r * 19}" width="15" height="15" rx="3" fill="#f8f5fd" stroke="#cfc6e6" stroke-width="1"/>'
                   for r in range(4) for c in range(10))
    swatches = ''.join(f'<rect x="292" y="300" width="26" height="96" rx="8" fill="{c}" stroke="rgba(255,255,255,.35)" stroke-width="1" transform="rotate({a} 305 392)"/>'
                       for a, c in ((-36, '#ece2ff'), (-18, '#c98bff'), (0, '#ab24f2'), (18, '#7b2ff0'), (36, '#621dd0')))
    dots = ('<pattern id="dk-dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="rgba(255,255,255,.06)"/></pattern>')
    return f'''<svg class="tl2-desk" viewBox="0 0 400 500" preserveAspectRatio="xMidYMid slice" role="img" aria-label="A designer's desk mid-project: tablet with a wireframe, keyboard, phone, colour swatches, sticky notes and coffee">
<defs>{dots}
<filter id="dk-sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="9" stdDeviation="8" flood-color="#000" flood-opacity=".6"/></filter>
<radialGradient id="dk-glow" cx="50%" cy="55%" r="60%"><stop offset="0" stop-color="#3b1a74" stop-opacity=".55"/><stop offset="1" stop-color="#0d0a1c" stop-opacity="0"/></radialGradient>
<linearGradient id="dk-hero" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c98bff"/><stop offset="1" stop-color="#621dd0"/></linearGradient>
<linearGradient id="dk-screen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c1236"/><stop offset="1" stop-color="#0e0a1e"/></linearGradient>
<linearGradient id="dk-note" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ece2ff"/><stop offset="1" stop-color="#d8c6fb"/></linearGradient>
</defs>
<rect width="400" height="500" fill="#0d0a1c"/><rect width="400" height="500" fill="url(#dk-glow)"/><rect width="400" height="500" fill="url(#dk-dots)"/>
<path d="M352 404 C 360 330, 300 300, 330 250 S 420 190, 380 110" fill="none" stroke="#d9d0ee" stroke-width="4" stroke-linecap="round" opacity=".85"/>
<g filter="url(#dk-sh)" transform="rotate(-9 90 110)">
  <rect x="-44" y="34" width="250" height="172" rx="16" fill="#241a44" stroke="#3b2a6b"/>
  <rect x="-32" y="46" width="226" height="148" rx="8" fill="#f5f1fc"/>
  <rect x="-24" y="54" width="210" height="10" rx="3" fill="#e4dcf5"/><circle cx="-16" cy="59" r="2.5" fill="#ab24f2"/>
  <rect x="-24" y="72" width="128" height="62" rx="6" fill="url(#dk-hero)"/>
  <rect x="112" y="74" width="72" height="7" rx="3" fill="#d3c6ee"/><rect x="112" y="87" width="56" height="7" rx="3" fill="#e4dcf5"/><rect x="112" y="104" width="40" height="14" rx="7" fill="#621dd0"/>
  <rect x="-24" y="142" width="64" height="44" rx="5" fill="#ece2ff"/><rect x="48" y="142" width="64" height="44" rx="5" fill="#ece2ff"/><rect x="120" y="142" width="64" height="44" rx="5" fill="#ece2ff"/>
</g>
<g filter="url(#dk-sh)" transform="rotate(13 350 50)">
  <rect x="252" y="-4" width="200" height="88" rx="11" fill="#e9e3f5" stroke="#d6cdee"/>{keys}
</g>
<g filter="url(#dk-sh)">
  <circle cx="318" cy="196" r="46" fill="#ddd3f0"/><circle cx="318" cy="196" r="35" fill="#f5f1fc"/>
  <rect x="348" y="188" width="24" height="15" rx="7" fill="#f5f1fc"/>
  <circle cx="318" cy="196" r="27" fill="#3a2316"/><circle cx="318" cy="196" r="20" fill="none" stroke="#c9a07a" stroke-width="2.5" opacity=".7"/>
  <path d="M308 192 q10 -8 20 0 q-10 10 -20 0z" fill="#e8cfae" opacity=".75"/>
</g>
<g filter="url(#dk-sh)">{swatches}<circle cx="305" cy="392" r="5" fill="#f5f1fc" stroke="#8e7ab8"/></g>
<g filter="url(#dk-sh)" transform="rotate(-11 80 410)">
  <rect x="8" y="350" width="118" height="118" rx="3" fill="#c6adff"/>
  <rect x="20" y="340" width="118" height="118" rx="3" fill="url(#dk-note)"/>
  <path d="M36 368 h70 M36 386 h56 M36 404 h64 M36 422 h40" stroke="#5b3b9a" stroke-width="2.6" stroke-linecap="round" opacity=".55"/>
  <path d="M110 362 l5 6 l9 -11" fill="none" stroke="#621dd0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</g>
<g filter="url(#dk-sh)" transform="rotate(32 120 262)">
  <rect x="58" y="256" width="124" height="12" rx="2" fill="#ab24f2"/><rect x="58" y="256" width="124" height="4" fill="#c98bff"/>
  <rect x="44" y="256" width="15" height="12" rx="2" fill="#ece2ff"/><path d="M182 256 l20 6 l-20 6z" fill="#efd9b8"/><path d="M196 260.5 l6 1.5 l-6 1.5z" fill="#2a1a40"/>
</g>
<g filter="url(#dk-sh)" transform="rotate(7 196 318)">
  <rect x="140" y="214" width="114" height="212" rx="20" fill="#0b0816" stroke="#3b2a6b" stroke-width="2"/>
  <rect x="148" y="222" width="98" height="196" rx="14" fill="url(#dk-screen)"/>
  <rect x="180" y="228" width="34" height="7" rx="3.5" fill="#0b0816"/>
  <rect x="156" y="244" width="82" height="70" rx="9" fill="url(#dk-hero)"/>
  <rect x="156" y="322" width="62" height="7" rx="3.5" fill="#ece2ff" opacity=".9"/><rect x="156" y="335" width="48" height="6" rx="3" fill="#ece2ff" opacity=".5"/>
  <rect x="156" y="350" width="38" height="38" rx="7" fill="#2b1a55"/><rect x="200" y="350" width="38" height="38" rx="7" fill="#2b1a55"/>
  <rect x="166" y="398" width="62" height="12" rx="6" fill="#ab24f2"/>
</g>
<g filter="url(#dk-sh)" transform="rotate(-14 352 438)">
  <path d="M352 384 c 26 0 38 20 38 50 c 0 34 -16 58 -38 58 c -22 0 -38 -24 -38 -58 c 0 -30 12 -50 38 -50z" fill="#ece7f6" stroke="#d6cdee"/>
  <path d="M352 386 v38" stroke="#cfc6e6" stroke-width="2"/><rect x="348" y="398" width="8" height="16" rx="4" fill="#9a8cc0"/>
</g>
</svg>'''
