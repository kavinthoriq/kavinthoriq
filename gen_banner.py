#!/usr/bin/env python3
"""
Generator banner "Swallowed Star" (吞噬星空) — SVG animasi untuk header README.

Pakai:  python3 assets/gen_banner.py
Hasil:  assets/swallowed-star.svg
"""
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
rnd = random.Random(7)

STREAM = ("M 175 140 C 265 52, 430 46, 512 112 C 566 156, 660 130, 652 176 "
          "C 645 214, 560 206, 556 172 C 552 144, 600 140, 600 166")

stars = []
for _ in range(46):
    x, y = rnd.randint(8, 792), rnd.randint(40, 352)
    r = rnd.choice([0.7, 0.9, 1.1, 1.4])
    c = rnd.choice(['#ffffff', '#ffffff', '#00f5ff', '#ffd700'])
    d = rnd.uniform(2, 4.6)
    stars.append(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}">'
        f'<animate attributeName="opacity" values="0.15;1;0.15" dur="{d:.1f}s" begin="-{rnd.uniform(0, 3):.1f}s" repeatCount="indefinite"/></circle>'
    )

particles = []
for i, c in enumerate(['#ffd700', '#ffffff', '#00f5ff', '#ffd700', '#ffffff', '#00f5ff', '#ffd700']):
    b = i * 0.85
    particles.append(
        f'<circle r="{2.2 if i % 2 == 0 else 1.6}" fill="{c}">'
        f'<animateMotion dur="6s" begin="{b:.2f}s" repeatCount="indefinite" calcMode="spline" keyPoints="0;1" keyTimes="0;1" keySplines="0.35 0 0.9 0.65" path="{STREAM}"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="6s" begin="{b:.2f}s" repeatCount="indefinite"/>'
        f'</circle>'
    )

rays = ''.join(
    f'<line x1="140" y1="{150 - 46}" x2="140" y2="{150 - 78 + (i % 3) * 8}" stroke="#ffd700" stroke-width="1.6" stroke-opacity="0.45" '
    f'transform="rotate({i * 30} 140 150)"/>' for i in range(12)
)

svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 360" width="800" height="360" role="img" aria-label="Swallowed Star - bintang ditelan pusaran kosmik">
<defs>
<radialGradient id="neb1" gradientUnits="userSpaceOnUse" cx="620" cy="165" r="330"><stop offset="0" stop-color="#0099ff" stop-opacity="0.28"/><stop offset="0.55" stop-color="#4b1d8f" stop-opacity="0.12"/><stop offset="1" stop-color="#020812" stop-opacity="0"/></radialGradient>
<radialGradient id="neb2" gradientUnits="userSpaceOnUse" cx="130" cy="150" r="240"><stop offset="0" stop-color="#ffb000" stop-opacity="0.2"/><stop offset="1" stop-color="#020812" stop-opacity="0"/></radialGradient>
<radialGradient id="corona" gradientUnits="userSpaceOnUse" cx="140" cy="150" r="78"><stop offset="0.3" stop-color="#ffd700" stop-opacity="0.55"/><stop offset="0.65" stop-color="#ff8c00" stop-opacity="0.18"/><stop offset="1" stop-color="#ff8c00" stop-opacity="0"/></radialGradient>
<radialGradient id="sun" cx="0.45" cy="0.42" r="0.65"><stop offset="0" stop-color="#ffffff"/><stop offset="0.3" stop-color="#fff2a8"/><stop offset="0.7" stop-color="#ffd700"/><stop offset="1" stop-color="#ff7a00"/></radialGradient>
<radialGradient id="hglow" gradientUnits="userSpaceOnUse" cx="600" cy="165" r="150"><stop offset="0.2" stop-color="#00f5ff" stop-opacity="0.4"/><stop offset="0.6" stop-color="#0099ff" stop-opacity="0.12"/><stop offset="1" stop-color="#020812" stop-opacity="0"/></radialGradient>
<linearGradient id="flow" gradientUnits="userSpaceOnUse" x1="175" y1="0" x2="640" y2="0"><stop offset="0" stop-color="#ffd700"/><stop offset="0.45" stop-color="#ffffff"/><stop offset="1" stop-color="#00f5ff"/></linearGradient>
<linearGradient id="tail" gradientUnits="userSpaceOnUse" x1="150" y1="0" x2="420" y2="0"><stop offset="0" stop-color="#ffb000" stop-opacity="0.6"/><stop offset="1" stop-color="#ffd700" stop-opacity="0"/></linearGradient>
<linearGradient id="disk" gradientUnits="userSpaceOnUse" x1="495" y1="0" x2="705" y2="0"><stop offset="0" stop-color="#0099ff"/><stop offset="0.35" stop-color="#00f5ff"/><stop offset="0.5" stop-color="#ffd700"/><stop offset="0.65" stop-color="#00f5ff"/><stop offset="1" stop-color="#0099ff"/></linearGradient>
<linearGradient id="title" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffd700"/><stop offset="0.5" stop-color="#fff6c2"/><stop offset="1" stop-color="#ffd700"/></linearGradient>
<linearGradient id="meteor" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.9"/></linearGradient>
<filter id="blur" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="glow" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>

<rect width="800" height="360" rx="12" fill="#020812"/>
<rect width="800" height="360" rx="12" fill="url(#neb1)"/>
<rect width="800" height="360" rx="12" fill="url(#neb2)"/>
@@STARS@@

<!-- meteors -->
<g>
<line x1="0" y1="0" x2="-46" y2="-13" stroke="url(#meteor)" stroke-width="1.6" transform="translate(790 40)">
<animateTransform attributeName="transform" type="translate" values="790 40;470 132;470 132" keyTimes="0;0.14;1" dur="9s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="0;1;0;0" keyTimes="0;0.04;0.14;1" dur="9s" repeatCount="indefinite"/>
</line>
<line x1="0" y1="0" x2="-40" y2="-11" stroke="url(#meteor)" stroke-width="1.3" transform="translate(420 30)">
<animateTransform attributeName="transform" type="translate" values="420 30;190 96;190 96" keyTimes="0;0.14;1" dur="11s" begin="4s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="0;1;0;0" keyTimes="0;0.04;0.14;1" dur="11s" begin="4s" repeatCount="indefinite"/>
</line>
</g>

<!-- HUD -->
<text x="22" y="28" font-family="'Courier New', Courier, monospace" font-size="11" fill="#00f5ff" fill-opacity="0.7" letter-spacing="2">HR.ALLIANCE // DOJO-OF-LIMITS-SYS v7.4.2</text>
<text x="778" y="28" text-anchor="end" font-family="'Courier New', Courier, monospace" font-size="11" fill="#00ff88" letter-spacing="2">&#9679; SYSTEM_ONLINE<animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/></text>

<!-- ============ THE STAR (left) ============ -->
<circle cx="140" cy="150" r="78" fill="url(#corona)"><animate attributeName="r" values="72;84;72" dur="3.4s" repeatCount="indefinite"/></circle>
<g>@@RAYS@@<animateTransform attributeName="transform" type="rotate" from="0 140 150" to="360 140 150" dur="26s" repeatCount="indefinite"/></g>

<!-- tidal tail: star matter stretched toward the vortex -->
<path d="M 150 112 C 230 70, 330 66, 410 86 C 330 98, 250 126, 176 168 Z" fill="url(#tail)"><animate attributeName="opacity" values="0.55;1;0.55" dur="2.8s" repeatCount="indefinite"/></path>
<ellipse cx="152" cy="146" rx="42" ry="27" transform="rotate(-20 152 146)" fill="#ffd700" fill-opacity="0.35" filter="url(#soft)"/>
<circle cx="140" cy="150" r="30" fill="url(#sun)"><animate attributeName="r" values="29;32;29" dur="3.4s" repeatCount="indefinite"/></circle>

<!-- ============ MATTER STREAM ============ -->
<path d="@@STREAM@@" fill="none" stroke="url(#flow)" stroke-width="9" stroke-opacity="0.22" filter="url(#blur)"/>
<path d="@@STREAM@@" fill="none" stroke="url(#flow)" stroke-width="2.4" stroke-opacity="0.9" stroke-dasharray="26 10"><animate attributeName="stroke-dashoffset" from="0" to="-144" dur="2.2s" repeatCount="indefinite"/></path>
<path d="@@STREAM@@" fill="none" stroke="url(#flow)" stroke-width="1.1" stroke-opacity="0.8" stroke-dasharray="4 14" transform="translate(0 7)"><animate attributeName="stroke-dashoffset" from="0" to="-90" dur="1.6s" repeatCount="indefinite"/></path>
<path d="@@STREAM@@" fill="none" stroke="url(#flow)" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="3 18" transform="translate(0 -7)"><animate attributeName="stroke-dashoffset" from="0" to="-105" dur="2.8s" repeatCount="indefinite"/></path>
@@PARTICLES@@

<!-- ============ THE VORTEX (right) ============ -->
<circle cx="600" cy="165" r="150" fill="url(#hglow)"><animate attributeName="opacity" values="0.7;1;0.7" dur="4s" repeatCount="indefinite"/></circle>
<circle cx="600" cy="165" r="96" fill="none" stroke="#ffd700" stroke-opacity="0.3" stroke-dasharray="3 10"><animateTransform attributeName="transform" type="rotate" from="0 600 165" to="360 600 165" dur="38s" repeatCount="indefinite"/></circle>
<circle cx="600" cy="165" r="124" fill="none" stroke="#00f5ff" stroke-opacity="0.2" stroke-dasharray="1 8"><animateTransform attributeName="transform" type="rotate" from="360 600 165" to="0 600 165" dur="52s" repeatCount="indefinite"/></circle>
<circle cx="600" cy="165" r="34" fill="none" stroke="#00f5ff" stroke-width="1.5"><animate attributeName="r" values="34;130" dur="4.4s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="0.7;0" dur="4.4s" repeatCount="indefinite"/></circle>
<circle cx="600" cy="165" r="34" fill="none" stroke="#ffd700" stroke-width="1.2"><animate attributeName="r" values="34;130" dur="4.4s" begin="2.2s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="0.55;0" dur="4.4s" begin="2.2s" repeatCount="indefinite"/></circle>

<g transform="rotate(-16 600 165)">
<ellipse cx="600" cy="165" rx="105" ry="26" fill="none" stroke="url(#disk)" stroke-width="12" stroke-opacity="0.5" filter="url(#blur)"/>
<ellipse cx="600" cy="165" rx="105" ry="26" fill="none" stroke="url(#disk)" stroke-width="4" stroke-opacity="0.95"/>
<ellipse cx="600" cy="165" rx="90" ry="21" fill="none" stroke="#ffd700" stroke-width="1.5" stroke-opacity="0.9" stroke-dasharray="22 11"><animate attributeName="stroke-dashoffset" from="0" to="-132" dur="2.4s" repeatCount="indefinite"/></ellipse>
<ellipse cx="600" cy="165" rx="120" ry="31" fill="none" stroke="#00f5ff" stroke-width="1.1" stroke-opacity="0.8" stroke-dasharray="12 20"><animate attributeName="stroke-dashoffset" from="0" to="-128" dur="3.6s" repeatCount="indefinite"/></ellipse>
</g>

<circle cx="600" cy="165" r="38" fill="none" stroke="#00f5ff" stroke-width="3" stroke-opacity="0.6" filter="url(#soft)"><animate attributeName="r" values="37;42;37" dur="3s" repeatCount="indefinite"/></circle>
<circle cx="600" cy="165" r="30" fill="#000" stroke="#00f5ff" stroke-width="1.5" stroke-opacity="0.9"/>

<g transform="rotate(-16 600 165)">
<path d="M495 165 A105 26 0 0 0 705 165" fill="none" stroke="url(#disk)" stroke-width="4" stroke-linecap="round"/>
<path d="M510 165 A90 21 0 0 0 690 165" fill="none" stroke="#ffd700" stroke-width="1.5" stroke-opacity="0.9" stroke-dasharray="22 11"><animate attributeName="stroke-dashoffset" from="0" to="-132" dur="2.4s" repeatCount="indefinite"/></path>
</g>
<path d="M573 148 A34 30 0 0 1 627 148" fill="none" stroke="#00f5ff" stroke-width="2" stroke-opacity="0.75" filter="url(#soft)"/>

<!-- ============ TITLE ============ -->
<text x="400" y="288" text-anchor="middle" font-family="'Noto Sans CJK SC','Microsoft YaHei','PingFang SC','Hiragino Sans GB',sans-serif" font-weight="700" font-size="40" letter-spacing="16" fill="url(#title)" filter="url(#glow)">&#21534;&#22124;&#26143;&#31354;<animate attributeName="opacity" values="0.85;1;0.85" dur="3.2s" repeatCount="indefinite"/></text>
<text x="400" y="318" text-anchor="middle" font-family="Orbitron, 'Segoe UI', Arial, sans-serif" font-weight="700" font-size="17" letter-spacing="11" fill="#00f5ff">SWALLOWED STAR</text>
<text x="400" y="342" text-anchor="middle" font-family="'Courier New', Courier, monospace" font-size="10.5" letter-spacing="3" fill="#ffd700" fill-opacity="0.8">OPERATOR: KAVIN THORIQ  //  COSMIC GRADE</text>

<rect x="0.5" y="0.5" width="799" height="359" rx="12" fill="none" stroke="#00f5ff" stroke-opacity="0.28"/>
<path d="M0 20 V0 H20" fill="none" stroke="#ffd700" stroke-width="2"/>
<path d="M780 360 H800 V340" fill="none" stroke="#ffd700" stroke-width="2"/>
</svg>
'''

svg = (svg.replace('@@STARS@@', '\n'.join(stars))
          .replace('@@RAYS@@', rays)
          .replace('@@STREAM@@', STREAM)
          .replace('@@PARTICLES@@', '\n'.join(particles)))

out = os.path.join(HERE, 'swallowed-star.svg')
with open(out, 'w', encoding='utf-8') as f:
    f.write(svg)
print('ok swallowed-star.svg', os.path.getsize(out) // 1024, 'KB')
