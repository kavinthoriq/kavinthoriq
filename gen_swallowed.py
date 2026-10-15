#!/usr/bin/env python3
"""
SWALLOWED STAR 100% (吞噬星空): panel antarmuka kosmik untuk README profil GitHub.
Tanpa terminal, tanpa efek mengetik. Isi muncul seperti hologram (fade + geser) di atas
nebula, bintang, pusaran, dan adegan yang mewakili isi tiap bab.

Pakai:  python3 assets/gen_swallowed.py
Hasil:  assets/ssr-origin.svg ssr-power.svg ssr-arsenal.svg ssr-starmap.svg
        ssr-journey.svg ssr-radar.svg ssr-legend.svg ssr-signal.svg
Edit teks di bagian DATA paling bawah, jalankan ulang, commit SVG barunya.
"""
import html
import math
import os
import random
import textwrap
import unicodedata

OUT = os.path.dirname(os.path.abspath(__file__))
CW, FS, LH, X0 = 7.2, 12, 20, 20      # lebar karakter, font, tinggi baris, margin kiri
TW, SW, TB = 456, 344, 34             # lebar terminal, lebar adegan, tinggi title bar
W = TW + SW
MINH = 300

COL = {'g': '#00ff88', 'c': '#00f5ff', 'y': '#ffd700', 'w': '#d0e8ff',
       'b': '#0099ff', 'm': '#5b7a99', 'p': '#ff7ab2', 'o': '#ff8c00'}
STREAM = ("M 175 140 C 265 52, 430 46, 512 112 C 566 156, 660 130, 652 176 "
          "C 645 214, 560 206, 556 172 C 552 144, 600 140, 600 166")


def cols(s):
    return sum(2 if unicodedata.east_asian_width(ch) in 'WF' else 1 for ch in s)


def nb(s):
    return s.replace(' ', ' ')


def kt(*xs):
    return ';'.join(f'{x:.5f}' for x in xs)


def esc(s):
    return html.escape(s, quote=True)


# ------------------------------------------------------------------ baris terminal
def prompt(cmd, path='~'):
    return dict(cmd=True, segs=[('kavin@swallowed-os', 'g'), (':', 'w'), (path, 'b'), ('$ ', 'w'), (cmd, 'y')])


def o(text, c='w'):
    return dict(segs=[(text, c)])


def multi(*segs):
    return dict(segs=list(segs))


def blank():
    return dict(blank=True, segs=[])


def wrap(text, c='w', width=55):
    return [o(l, c) for l in textwrap.wrap(text, width)]


# ------------------------------------------------------------------ potongan adegan bersama
def defs_common(sw, sh):
    return f'''<clipPath id="win"><rect width="{W}" height="{sh + TB}" rx="12"/></clipPath>
<clipPath id="pane"><rect width="{sw}" height="{sh}"/></clipPath>
<radialGradient id="bgp1" gradientUnits="userSpaceOnUse" cx="{sw * 0.65:.0f}" cy="{sh * 0.4:.0f}" r="{sw * 0.95:.0f}"><stop offset="0" stop-color="#0099ff" stop-opacity="0.26"/><stop offset="0.55" stop-color="#4b1d8f" stop-opacity="0.11"/><stop offset="1" stop-color="#020812" stop-opacity="0"/></radialGradient>
<radialGradient id="bgp2" gradientUnits="userSpaceOnUse" cx="{sw * 0.15:.0f}" cy="{sh * 0.85:.0f}" r="{sw * 0.8:.0f}"><stop offset="0" stop-color="#ffb000" stop-opacity="0.16"/><stop offset="1" stop-color="#020812" stop-opacity="0"/></radialGradient>
<radialGradient id="core" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffffff"/><stop offset="0.3" stop-color="#ffe98a" stop-opacity="0.9"/><stop offset="1" stop-color="#ff8c00" stop-opacity="0"/></radialGradient>
<radialGradient id="goldglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0.25" stop-color="#ffd700" stop-opacity="0.6"/><stop offset="1" stop-color="#ff8c00" stop-opacity="0"/></radialGradient>
<radialGradient id="sun" cx="0.45" cy="0.42" r="0.65"><stop offset="0" stop-color="#ffffff"/><stop offset="0.3" stop-color="#fff2a8"/><stop offset="0.7" stop-color="#ffd700"/><stop offset="1" stop-color="#ff7a00"/></radialGradient>
<radialGradient id="corona" gradientUnits="userSpaceOnUse" cx="140" cy="150" r="78"><stop offset="0.3" stop-color="#ffd700" stop-opacity="0.55"/><stop offset="0.65" stop-color="#ff8c00" stop-opacity="0.18"/><stop offset="1" stop-color="#ff8c00" stop-opacity="0"/></radialGradient>
<radialGradient id="hglow" gradientUnits="userSpaceOnUse" cx="600" cy="165" r="150"><stop offset="0.2" stop-color="#00f5ff" stop-opacity="0.4"/><stop offset="0.6" stop-color="#0099ff" stop-opacity="0.12"/><stop offset="1" stop-color="#020812" stop-opacity="0"/></radialGradient>
<radialGradient id="planet" cx="0.35" cy="0.35" r="0.75"><stop offset="0" stop-color="#9fe8ff"/><stop offset="0.5" stop-color="#1e7fd6"/><stop offset="1" stop-color="#06204a"/></radialGradient>
<linearGradient id="flow" gradientUnits="userSpaceOnUse" x1="175" y1="0" x2="640" y2="0"><stop offset="0" stop-color="#ffd700"/><stop offset="0.45" stop-color="#ffffff"/><stop offset="1" stop-color="#00f5ff"/></linearGradient>
<linearGradient id="tail" gradientUnits="userSpaceOnUse" x1="150" y1="0" x2="420" y2="0"><stop offset="0" stop-color="#ffb000" stop-opacity="0.6"/><stop offset="1" stop-color="#ffd700" stop-opacity="0"/></linearGradient>
<linearGradient id="disk" gradientUnits="userSpaceOnUse" x1="495" y1="0" x2="705" y2="0"><stop offset="0" stop-color="#0099ff"/><stop offset="0.35" stop-color="#00f5ff"/><stop offset="0.5" stop-color="#ffd700"/><stop offset="0.65" stop-color="#00f5ff"/><stop offset="1" stop-color="#0099ff"/></linearGradient>
<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0099ff"/><stop offset="0.6" stop-color="#00f5ff"/><stop offset="1" stop-color="#ffd700"/></linearGradient>
<linearGradient id="sweep" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#00f5ff" stop-opacity="0.55"/><stop offset="1" stop-color="#00f5ff" stop-opacity="0"/></linearGradient>
<linearGradient id="goldtxt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6c2"/><stop offset="1" stop-color="#ffd700"/></linearGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00f5ff" stop-opacity="0"/><stop offset="0.5" stop-color="#00f5ff" stop-opacity="0.07"/><stop offset="1" stop-color="#00f5ff" stop-opacity="0"/></linearGradient>
<filter id="blur" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="glow" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'''


def star_markup():
    rays = ''.join(
        f'<line x1="140" y1="104" x2="140" y2="{72 + (i % 3) * 8}" stroke="#ffd700" stroke-width="1.6" '
        f'stroke-opacity="0.45" transform="rotate({i * 30} 140 150)"/>' for i in range(12))
    return f'''<circle cx="140" cy="150" r="78" fill="url(#corona)"><animate attributeName="r" values="72;84;72" dur="3.4s" repeatCount="indefinite"/></circle>
<g>{rays}<animateTransform attributeName="transform" type="rotate" from="0 140 150" to="360 140 150" dur="26s" repeatCount="indefinite"/></g>
<path d="M 150 112 C 230 70, 330 66, 410 86 C 330 98, 250 126, 176 168 Z" fill="url(#tail)"><animate attributeName="opacity" values="0.55;1;0.55" dur="2.8s" repeatCount="indefinite"/></path>
<ellipse cx="152" cy="146" rx="42" ry="27" transform="rotate(-20 152 146)" fill="#ffd700" fill-opacity="0.35" filter="url(#soft)"/>
<circle cx="140" cy="150" r="30" fill="url(#sun)"><animate attributeName="r" values="29;32;29" dur="3.4s" repeatCount="indefinite"/></circle>'''


def stream_markup():
    parts = [
        f'<path d="{STREAM}" fill="none" stroke="url(#flow)" stroke-width="9" stroke-opacity="0.22" filter="url(#blur)"/>',
        f'<path d="{STREAM}" fill="none" stroke="url(#flow)" stroke-width="2.4" stroke-opacity="0.9" stroke-dasharray="26 10"><animate attributeName="stroke-dashoffset" from="0" to="-144" dur="2.2s" repeatCount="indefinite"/></path>',
        f'<path d="{STREAM}" fill="none" stroke="url(#flow)" stroke-width="1.1" stroke-opacity="0.8" stroke-dasharray="4 14" transform="translate(0 7)"><animate attributeName="stroke-dashoffset" from="0" to="-90" dur="1.6s" repeatCount="indefinite"/></path>',
    ]
    for i, c in enumerate(['#ffd700', '#ffffff', '#00f5ff', '#ffd700', '#ffffff', '#00f5ff', '#ffd700']):
        b = i * 0.85
        parts.append(
            f'<circle r="{2.2 if i % 2 == 0 else 1.6}" fill="{c}">'
            f'<animateMotion dur="6s" begin="{b:.2f}s" repeatCount="indefinite" calcMode="spline" keyPoints="0;1" keyTimes="0;1" keySplines="0.35 0 0.9 0.65" path="{STREAM}"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="6s" begin="{b:.2f}s" repeatCount="indefinite"/></circle>')
    return '\n'.join(parts)


def vortex_markup():
    return '''<circle cx="600" cy="165" r="150" fill="url(#hglow)"><animate attributeName="opacity" values="0.7;1;0.7" dur="4s" repeatCount="indefinite"/></circle>
<circle cx="600" cy="165" r="96" fill="none" stroke="#ffd700" stroke-opacity="0.3" stroke-dasharray="3 10"><animateTransform attributeName="transform" type="rotate" from="0 600 165" to="360 600 165" dur="38s" repeatCount="indefinite"/></circle>
<circle cx="600" cy="165" r="124" fill="none" stroke="#00f5ff" stroke-opacity="0.2" stroke-dasharray="1 8"><animateTransform attributeName="transform" type="rotate" from="360 600 165" to="0 600 165" dur="52s" repeatCount="indefinite"/></circle>
<circle cx="600" cy="165" r="34" fill="none" stroke="#00f5ff" stroke-width="1.5"><animate attributeName="r" values="34;130" dur="4.4s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="0.7;0" dur="4.4s" repeatCount="indefinite"/></circle>
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
<path d="M573 148 A34 30 0 0 1 627 148" fill="none" stroke="#00f5ff" stroke-width="2" stroke-opacity="0.75" filter="url(#soft)"/>'''


def txt(x, y, s, fill='#00f5ff', size=9, anchor='start', op=1, ls=1):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="\'Courier New\', monospace" '
            f'font-size="{size}" fill="{fill}" fill-opacity="{op}" letter-spacing="{ls}">{esc(s)}</text>')


# ------------------------------------------------------------------ ADEGAN (kanan)
def sc_boot(sw, sh):
    rnd = random.Random(3)
    cx, cy, R = sw / 2, sh / 2, min(sw, sh) * 0.47
    dots = []
    for arm in range(3):
        for i in range(90):
            t = i / 90
            r, th = 6 + t * R, arm * 2 * math.pi / 3 + t * 3.4 * math.pi + rnd.uniform(-.15, .15)
            col = '#ffd700' if t < .35 else ('#ffffff' if t < .6 else '#00f5ff')
            dots.append(f'<circle cx="{r * math.cos(th):.1f}" cy="{r * math.sin(th):.1f}" r="{rnd.uniform(.6, 1.5):.1f}" '
                        f'fill="{col}" fill-opacity="{0.95 - t * 0.6:.2f}"/>')
    return (f'<g transform="translate({cx:.0f} {cy:.0f}) scale(1 0.62) rotate(-20)"><g>{"".join(dots)}'
            f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="70s" repeatCount="indefinite"/></g></g>'
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="34" fill="url(#core)"><animate attributeName="r" values="30;38;30" dur="4s" repeatCount="indefinite"/></circle>')


def sc_whoami(sw, sh):
    s = (sw - 24) / 620
    tx, ty = sw / 2 - 410 * s, sh * 0.40 - 165 * s
    rd = ''.join(txt(18, sh - 62 + i * 14, f'{k:<9} {v}', c, 10, op=0.9)
                 for i, (k, v, c) in enumerate([('OPERATOR', 'KAVIN THORIQ', '#00f5ff'),
                                                ('CLASS', 'COSMIC GRADE', '#ffd700'),
                                                ('POWER', 'INFINITY', '#00ff88')]))
    return f'<g transform="translate({tx:.1f} {ty:.1f}) scale({s:.3f})">{star_markup()}{stream_markup()}{vortex_markup()}</g>{rd}'


def sc_code(sw, sh):
    s, hx, hy = 0.6, sw * 0.7, sh * 0.42
    tx, ty = hx - 600 * s, hy - 165 * s
    bw = sw - 36
    return f'''<g transform="translate({tx:.1f} {ty:.1f}) scale({s})">{vortex_markup()}</g>
<path d="M 82 {hy:.0f} C 122 {hy - 46:.0f}, 172 {hy - 40:.0f}, {hx - 40:.0f} {hy:.0f}" fill="none" stroke="#ffd700" stroke-width="2" stroke-dasharray="14 8" stroke-opacity="0.9"><animate attributeName="stroke-dashoffset" from="0" to="-88" dur="1.4s" repeatCount="indefinite"/></path>
<circle cx="64" cy="{hy:.0f}" r="40" fill="url(#goldglow)"><animate attributeName="r" values="44;44;4;44" keyTimes="0;0.05;0.9;1" dur="7s" repeatCount="indefinite"/></circle>
<circle cx="64" cy="{hy:.0f}" r="22" fill="url(#sun)"><animate attributeName="r" values="24;24;2;24" keyTimes="0;0.05;0.9;1" dur="7s" repeatCount="indefinite"/></circle>
{txt(18, sh - 60, 'star.mass', '#ffd700', 10)}
<rect x="18" y="{sh - 52}" width="{bw}" height="8" rx="4" fill="#ffd700" fill-opacity="0.1" stroke="#ffd700" stroke-opacity="0.3"/>
<rect x="18" y="{sh - 52}" width="{bw}" height="8" rx="4" fill="url(#bar)"><animate attributeName="width" values="{bw};{bw};0;{bw}" keyTimes="0;0.05;0.9;1" dur="7s" repeatCount="indefinite"/></rect>'''


def sc_skills(sw, sh):
    cx, cy = sw / 2, sh / 2 - 6
    items = [('WEB', 82, '#00f5ff'), ('UI', 75, '#ffd700'), ('GAME', 68, '#00ff88'),
             ('SQL', 72, '#0099ff'), ('GIT', 78, '#ff7ab2'), ('OFC', 88, '#ffffff')]
    out = [f'<circle cx="{cx}" cy="{cy}" r="26" fill="url(#hglow)" transform="translate({cx * -1.0 + cx} 0)"/>',
           f'<circle cx="{cx}" cy="{cy}" r="11" fill="#000" stroke="#00f5ff" stroke-width="1.5"/>',
           f'<circle cx="{cx}" cy="{cy}" r="16" fill="none" stroke="#00f5ff" stroke-opacity="0.5" filter="url(#soft)"/>']
    for i, (n, p, c) in enumerate(items):
        r, dur, phase = 36 + i * 21, 12 + i * 5, i * 61
        path = f'M {cx + r} {cy} A {r} {r} 0 1 1 {cx - r} {cy} A {r} {r} 0 1 1 {cx + r} {cy}'
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-opacity="0.22" stroke-dasharray="2 5"/>')
        out.append(f'<g><animateMotion dur="{dur}s" begin="-{dur * phase / 360:.1f}s" repeatCount="indefinite" path="{path}"/>'
                   f'<circle r="{3 + p / 25:.1f}" fill="{c}" filter="url(#glow)"/>{txt(0, -9, f"{n} {p}", c, 8.5, "middle")}</g>')
    return '\n'.join(out)


def sc_stack(sw, sh):
    nodes = [('html5', .14, .18), ('css3', .38, .10), ('js', .62, .20), ('php', .80, .10), ('mysql', .76, .36),
             ('git', .54, .40), ('github', .28, .34), ('figma', .12, .52), ('vscode', .34, .60),
             ('linux', .60, .64), ('rpgmz', .78, .72), ('scratch', .30, .82)]
    pts = [(n, sw * x, (sh - 40) * y + 14) for n, x, y in nodes]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (2, 5), (6, 8), (1, 6), (5, 9)]
    out = [f'<line x1="{pts[a][1]:.0f}" y1="{pts[a][2]:.0f}" x2="{pts[b][1]:.0f}" y2="{pts[b][2]:.0f}" stroke="#00f5ff" '
           f'stroke-opacity="0.45" stroke-dasharray="3 5"><animate attributeName="stroke-dashoffset" from="0" to="-32" dur="{2 + (i % 3)}s" repeatCount="indefinite"/></line>'
           for i, (a, b) in enumerate(edges)]
    for i, (n, x, y) in enumerate(pts):
        c = '#ffd700' if i % 4 == 0 else '#ffffff'
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="8" fill="#00f5ff" fill-opacity="0.25"><animate attributeName="r" values="5;10;5" dur="{2.4 + i * 0.3:.1f}s" repeatCount="indefinite"/></circle>'
                   f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="{c}"/>{txt(x + 7, y - 6, n, "#d0e8ff", 8.5)}')
    return '\n'.join(out)


def sc_projects(sw, sh):
    ps = [('P-001', '#ffd700', .18, .22), ('P-002', '#00f5ff', .52, .14), ('P-003', '#ffd700', .80, .28),
          ('P-004', '#00f5ff', .70, .54), ('P-005', '#00ff88', .30, .60), ('P-006', '#00ff88', .56, .78)]
    pts = [(n, c, sw * x, (sh - 48) * y + 20) for n, c, x, y in ps]
    edges = [(0, 1), (1, 2), (2, 3), (3, 5), (5, 4), (4, 0), (1, 3)]
    out = [f'<line x1="{pts[a][2]:.0f}" y1="{pts[a][3]:.0f}" x2="{pts[b][2]:.0f}" y2="{pts[b][3]:.0f}" stroke="#d0e8ff" stroke-opacity="0.22" stroke-dasharray="2 5"/>'
           for a, b in edges]
    for i, (n, c, x, y) in enumerate(pts):
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="12" fill="{c}" fill-opacity="0.2" filter="url(#soft)"><animate attributeName="r" values="9;15;9" dur="{2.6 + i * 0.4:.1f}s" repeatCount="indefinite"/></circle>'
                   f'<line x1="{x - 9:.0f}" y1="{y:.0f}" x2="{x + 9:.0f}" y2="{y:.0f}" stroke="{c}" stroke-width="1.2"/>'
                   f'<line x1="{x:.0f}" y1="{y - 9:.0f}" x2="{x:.0f}" y2="{y + 9:.0f}" stroke="{c}" stroke-width="1.2"/>'
                   f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.5" fill="#fff"/>{txt(x + 11, y + 3, n, c, 9)}')
    px, py = pts[1][2], pts[1][3]
    out.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="8" fill="none" stroke="#ffd700" stroke-width="1.5"><animate attributeName="r" values="8;26" dur="2s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="0.9;0" dur="2s" repeatCount="indefinite"/></circle>')
    for i, (lab, c) in enumerate([('GAME', '#ffd700'), ('WEB', '#00f5ff'), ('DESIGN', '#00ff88')]):
        out.append(f'<circle cx="{22 + i * 70}" cy="{sh - 34}" r="3" fill="{c}"/>{txt(30 + i * 70, sh - 31, lab, c, 8.5)}')
    return '\n'.join(out)


def sc_missions(sw, sh):
    p = [(40, sh - 56), (138, sh * 0.62), (226, sh * 0.40), (306, sh * 0.2)]
    d = (f'M {p[0][0]} {p[0][1]} C {p[0][0] + 50} {p[0][1]}, {p[1][0] - 40} {p[1][1] + 30}, {p[1][0]} {p[1][1]} '
         f'S {p[2][0] - 40} {p[2][1] + 30}, {p[2][0]} {p[2][1]} S {p[3][0] - 40} {p[3][1] + 30}, {p[3][0]} {p[3][1]}')
    labs = [('M-001', '2024', '#00ff88', 12, -8, 'start'), ('M-002', '2024', '#00f5ff', 12, -8, 'start'),
            ('M-003', '2025', '#00f5ff', 12, -8, 'start'), ('M-004', 'NOW', '#ffd700', -10, 20, 'end')]
    out = [f'<path d="{d}" fill="none" stroke="#00f5ff" stroke-opacity="0.35" stroke-dasharray="3 6"/>']
    for i, ((x, y), (m, yr, c, dx, dy, an)) in enumerate(zip(p, labs)):
        out.append(f'<circle cx="{x}" cy="{y:.0f}" r="9" fill="{c}" fill-opacity="0.22" filter="url(#soft)"/>'
                   f'<circle cx="{x}" cy="{y:.0f}" r="4" fill="{c}"/>{txt(x + dx, y + dy, m, c, 9, an)}{txt(x + dx, y + dy + 11, yr, "#5b7a99", 8.5, an)}')
    out.append(f'<circle cx="{p[3][0]}" cy="{p[3][1]:.0f}" r="6" fill="none" stroke="#ffd700"><animate attributeName="r" values="6;22" dur="2s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="0.9;0" dur="2s" repeatCount="indefinite"/></circle>')
    for k, (r, op) in enumerate([(3.2, 1), (2.4, 0.6), (1.6, 0.35)]):
        out.append(f'<circle r="{r}" fill="#fff" fill-opacity="{op}"><animateMotion dur="8s" begin="{-k * 0.18:.2f}s" repeatCount="indefinite" path="{d}"/></circle>')
    return '\n'.join(out)


def sc_stats(sw, sh):
    cx, cy, R = sw / 2, sh / 2 - 6, min(sw, sh) * 0.38
    a = math.radians(-42)
    out = [f'<circle cx="{cx}" cy="{cy}" r="{R * k:.0f}" fill="none" stroke="#00f5ff" stroke-opacity="0.3"/>' for k in (1, .66, .33)]
    out.append(f'<line x1="{cx - R}" y1="{cy}" x2="{cx + R}" y2="{cy}" stroke="#00f5ff" stroke-opacity="0.25"/>'
               f'<line x1="{cx}" y1="{cy - R}" x2="{cx}" y2="{cy + R}" stroke="#00f5ff" stroke-opacity="0.25"/>')
    out.append(f'<g transform="translate({cx} {cy})"><g><path d="M0 0 L {R} 0 A {R} {R} 0 0 0 {R * math.cos(a):.1f} {R * math.sin(a):.1f} Z" fill="url(#sweep)"/>'
               f'<line x1="0" y1="0" x2="{R}" y2="0" stroke="#00f5ff" stroke-width="1.5"/>'
               f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="5s" repeatCount="indefinite"/></g></g>')
    for name, ang, rr, c in [('commits', 25, .8, '#00ff88'), ('repos', 110, .55, '#ffd700'), ('stars', 190, .85, '#ffffff'),
                             ('pr', 250, .45, '#00f5ff'), ('streak', 320, .7, '#ffd700')]:
        x, y = cx + R * rr * math.cos(math.radians(ang)), cy + R * rr * math.sin(math.radians(ang))
        out.append(f'<g><circle cx="{x:.0f}" cy="{y:.0f}" r="3.2" fill="{c}" filter="url(#glow)"/>{txt(x + 6, y - 5, name, c, 8.5)}'
                   f'<animate attributeName="opacity" from="1" to="0.12" dur="5s" begin="{ang / 360 * 5:.2f}s" repeatCount="indefinite"/></g>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="#00f5ff"/>')
    return '\n'.join(out)


def sc_quote(sw, sh):
    s, hx, hy = 0.62, 112, sh * 0.46
    tx, ty = hx - 600 * s, hy - 165 * s
    y0 = (sh - 4 * 46) / 2 + 34
    kanji = ''.join(
        f'<text x="{sw - 46}" y="{y0 + i * 46:.0f}" text-anchor="middle" font-family="\'Noto Sans CJK SC\',\'Microsoft YaHei\',\'PingFang SC\',sans-serif" '
        f'font-size="34" font-weight="700" fill="url(#goldtxt)" filter="url(#glow)">{ch}'
        f'<animate attributeName="opacity" values="0.6;1;0.6" dur="{3 + i * 0.5:.1f}s" repeatCount="indefinite"/></text>'
        for i, ch in enumerate('吞噬星空'))
    return (f'<g transform="translate({tx:.1f} {ty:.1f}) scale({s})">{vortex_markup()}</g>'
            f'<line x1="{sw - 82}" y1="{y0 - 34:.0f}" x2="{sw - 82}" y2="{y0 + 4 * 46 - 34:.0f}" stroke="#ffd700" stroke-opacity="0.35"/>{kanji}')


def sc_contact(sw, sh):
    ax, ay, bx, by = 66, sh - 74, sw - 64, 66
    qx, qy = sw * 0.3, 40
    def at(t):
        return ((1 - t) ** 2 * ax + 2 * (1 - t) * t * qx + t * t * bx, (1 - t) ** 2 * ay + 2 * (1 - t) * t * qy + t * t * by)
    d = f'M {ax} {ay} Q {qx:.0f} {qy} {bx} {by}'
    out = [f'<circle cx="{ax}" cy="{ay}" r="22" fill="none" stroke="#00f5ff" stroke-width="1.4"><animate attributeName="r" values="22;120" dur="3.6s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="0.7;0" dur="3.6s" repeatCount="indefinite"/></circle>',
           f'<circle cx="{ax}" cy="{ay}" r="22" fill="none" stroke="#ffd700" stroke-width="1.2"><animate attributeName="r" values="22;120" dur="3.6s" begin="1.8s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="0.55;0" dur="3.6s" begin="1.8s" repeatCount="indefinite"/></circle>',
           f'<path d="{d}" fill="none" stroke="#00f5ff" stroke-opacity="0.5" stroke-dasharray="4 6"><animate attributeName="stroke-dashoffset" from="0" to="-40" dur="1.6s" repeatCount="indefinite"/></path>',
           f'<circle cx="{ax}" cy="{ay}" r="22" fill="url(#planet)"/>',
           f'<ellipse cx="{ax}" cy="{ay}" rx="36" ry="9" fill="none" stroke="#ffd700" stroke-opacity="0.8" transform="rotate(-18 {ax} {ay})"/>',
           txt(ax, ay + 40, 'BOGOR, ID', '#00f5ff', 9, 'middle'),
           f'<rect x="{bx - 8}" y="{by - 8}" width="16" height="16" fill="#ffd700" fill-opacity="0.25" stroke="#ffd700" transform="rotate(45 {bx} {by})"><animate attributeName="fill-opacity" values="0.2;0.7;0.2" dur="2s" repeatCount="indefinite"/></rect>',
           txt(bx, by - 18, 'HR.ALLIANCE', '#ffd700', 9, 'middle')]
    for t, lab, c in [(0.36, 'GITHUB', '#00f5ff'), (0.68, 'EMAIL', '#00ff88')]:
        x, y = at(t)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="{c}" filter="url(#glow)"/>{txt(x + 9, y + 3, lab, c, 8.5)}')
    for k, c in enumerate(['#ffffff', '#ffd700', '#00f5ff']):
        out.append(f'<circle r="2.4" fill="{c}"><animateMotion dur="3.6s" begin="{k * 1.2}s" repeatCount="indefinite" path="{d}"/>'
                   f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" dur="3.6s" begin="{k * 1.2}s" repeatCount="indefinite"/></circle>')
    return '\n'.join(out)



# =====================================================================
#  PANEL 100% SWALLOWED STAR
# =====================================================================
import re

PW, TWL, SWR = 800, 456, 344          # lebar panel, kolom kiri (kartu hologram), kolom kanan (adegan)
HDR = 78                              # tinggi header bab
FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
CJK = "'Noto Sans CJK SC','Microsoft YaHei','PingFang SC','Hiragino Sans GB',sans-serif"
CUT = 14


def T(x, y, s, fill, size=13, weight='400', anchor='start', ls=0, op=1, fam=FONT, cls='L', extra=''):
    return (f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" fill-opacity="{op}" letter-spacing="{ls}" {extra}>{esc(s)}</text>')


# ---- tipe baris (data) ----
def kv(label, value, c='#ffffff'):
    return dict(t='kv', label=label, value=value, c=c, h=28)


def bar(name, pct, c='c'):
    return dict(t='bar', name=name, pct=pct, c=c, h=26)


def head(text):
    return dict(t='head', text=text, h=36)


def para(text, c='#b6cde6', width=54, size=13):
    return [dict(t='line', text=l, c=c, size=size, h=size + 8) for l in textwrap.wrap(text, width)]


def item(code, title, sub, tag, tagc, codec='#ffd700'):
    return dict(t='item', code=code, title=title, sub=sub, tag=tag, tagc=tagc, codec=codec, h=42)


def gap(h=10):
    return dict(t='gap', h=h)


def reveal(inner, s, total, dx=-14, d=0.4):
    k = kt(0, s / total, (s + d) / total, (total - 0.5) / total, 1)
    return (f'<g opacity="1"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{k}" dur="{total}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="{dx} 0;{dx} 0;0 0;0 0;{dx} 0" keyTimes="{k}" dur="{total}s" repeatCount="indefinite"/>'
            f'{inner}</g>')


BARC = {'c': ('url(#bar)', '#00f5ff'), 'y': ('url(#barGold)', '#ffd700')}


def row_markup(r, y, s, total):
    x0, vx, right = 28, 140, TWL - 28
    sep = f'<line x1="{x0}" y1="{y + r["h"] - 4}" x2="{right}" y2="{y + r["h"] - 4}" stroke="#00f5ff" stroke-opacity="0.09"/>'
    t = r['t']
    if t == 'kv':
        m = (T(x0, y + 18, r['label'].upper(), '#00f5ff', 10.5, '600', ls=1.6, op=0.85)
             + T(vx, y + 18, r['value'], r['c'], 13.5, '500') + sep)
    elif t == 'bar':
        fill, col = BARC[r['c']]
        w = 196 * r['pct'] / 100
        k = kt(0, (s + 0.1) / total, (s + 1.0) / total, (total - 0.5) / total, 1)
        m = (T(x0, y + 16, r['name'], '#d0e8ff', 13)
             + f'<rect x="190" y="{y + 9}" width="196" height="7" rx="3.5" fill="#00f5ff" fill-opacity="0.08" stroke="#00f5ff" stroke-opacity="0.2"/>'
             + f'<rect x="190" y="{y + 9}" width="{w:.1f}" height="7" rx="3.5" fill="{fill}">'
               f'<animate attributeName="width" values="0;0;{w:.1f};{w:.1f};0" keyTimes="{k}" dur="{total}s" repeatCount="indefinite"/></rect>'
             + T(right, y + 16, f'{r["pct"]}%', col, 12.5, '700', 'end'))
    elif t == 'head':
        m = (f'<rect x="{x0}" y="{y + 13}" width="6" height="6" fill="#ffd700" transform="rotate(45 {x0 + 3} {y + 16})"/>'
             + T(x0 + 14, y + 20, r['text'].upper(), '#ffd700', 11, '700', ls=2.4)
             + f'<line x1="{x0}" y1="{y + 30}" x2="{right}" y2="{y + 30}" stroke="#ffd700" stroke-opacity="0.22"/>')
    elif t == 'line':
        m = T(x0, y + r['size'] + 1, r['text'], r['c'], r['size'])
    elif t == 'item':
        m = (T(x0, y + 17, r['code'], r['codec'], 12, '700', ls=1)
             + T(84, y + 17, r['title'], '#ffffff', 13.5, '600')
             + T(84, y + 33, r['sub'], '#7f9bb8', 11)
             + T(right, y + 17, r['tag'], r['tagc'], 10, '700', 'end', ls=1.4) + sep)
    else:
        return ''
    return reveal(m, s, total)


def panel(fname, num, title, cn, sector, scene_fn, rows, seed=1, min_h=300, hold=6):
    flat = []
    for r in rows:
        flat.extend(r if isinstance(r, list) else [r])
    n_vis = sum(1 for r in flat if r['t'] != 'gap')
    total = round(0.6 + 0.2 * n_vis + hold, 2)
    H = int(math.ceil(max(min_h, HDR + sum(r["h"] for r in flat) + 26)))

    y, i, body = HDR, 0, []
    for r in flat:
        if r['t'] != 'gap':
            body.append(row_markup(r, y, 0.6 + 0.2 * i, total))
            i += 1
        y += r['h']

    rnd = random.Random(seed)
    stars = ''.join(
        f'<circle cx="{rnd.randint(4, PW - 4)}" cy="{rnd.randint(4, H - 4)}" r="{rnd.choice([0.7, 0.9, 1.2, 1.4])}" '
        f'fill="{rnd.choice(["#fff", "#fff", "#00f5ff", "#ffd700"])}"><animate attributeName="opacity" values="0.15;1;0.15" '
        f'dur="{rnd.uniform(2, 4.5):.1f}s" begin="-{rnd.uniform(0, 3):.1f}s" repeatCount="indefinite"/></circle>' for _ in range(70))
    coord = f'RA {rnd.randint(1, 23):02d}h{rnd.randint(0, 59):02d}  DEC {rnd.choice("+-")}{rnd.randint(5, 80):02d}'

    frame = f'M0 0 H{PW - 20} L{PW} 20 V{H} H20 L0 {H - 20} Z'
    cx0, cx1 = 12, TWL - 6
    card = (f'M{cx0} {12} H{cx1 - CUT} L{cx1} {12 + CUT} V{H - 12} H{cx0 + CUT} L{cx0} {H - 12 - CUT} Z')
    defs = re.sub(r'<clipPath id="(win|pane)">.*?</clipPath>', '', defs_common(SWR, H), flags=re.S)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {H}" width="{PW}" height="{H}" role="img" aria-label="{esc(title)}">
<defs>
{defs}
<clipPath id="frame"><path d="{frame}"/></clipPath>
<clipPath id="pane2"><rect x="{TWL}" y="0" width="{SWR}" height="{H}"/></clipPath>
<radialGradient id="bgA" gradientUnits="userSpaceOnUse" cx="{PW * 0.78:.0f}" cy="{H * 0.4:.0f}" r="{PW * 0.55:.0f}"><stop offset="0" stop-color="#0099ff" stop-opacity="0.28"/><stop offset="0.55" stop-color="#4b1d8f" stop-opacity="0.12"/><stop offset="1" stop-color="#020812" stop-opacity="0"/></radialGradient>
<radialGradient id="bgB" gradientUnits="userSpaceOnUse" cx="{PW * 0.08:.0f}" cy="{H * 0.95:.0f}" r="{PW * 0.5:.0f}"><stop offset="0" stop-color="#ffb000" stop-opacity="0.2"/><stop offset="1" stop-color="#020812" stop-opacity="0"/></radialGradient>
<linearGradient id="barGold" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ff8c00"/><stop offset="1" stop-color="#ffd700"/></linearGradient>
<linearGradient id="hl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffd700" stop-opacity="0"/><stop offset="0.5" stop-color="#ffd700"/><stop offset="1" stop-color="#ffd700" stop-opacity="0"/></linearGradient>
</defs>
<g clip-path="url(#frame)">
<rect width="{PW}" height="{H}" fill="#020812"/>
<rect width="{PW}" height="{H}" fill="url(#bgA)"/>
<rect width="{PW}" height="{H}" fill="url(#bgB)"/>
{stars}
<g transform="translate(40 {H})" fill="none" stroke-dasharray="3 9">
<circle r="150" stroke="#ffd700" stroke-opacity="0.16"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="60s" repeatCount="indefinite"/></circle>
<circle r="210" stroke="#00f5ff" stroke-opacity="0.12"><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="80s" repeatCount="indefinite"/></circle>
</g>

<path d="{card}" fill="#030d1c" fill-opacity="0.74" stroke="#00f5ff" stroke-opacity="0.28"/>
<path d="M{cx0} {12 + 22} V12 H{cx0 + 22} M{cx1 - 22} {H - 12} H{cx1} V{H - 12 - 22}" fill="none" stroke="#ffd700" stroke-width="2"/>
{T(28, 34, f'BAB {num:02d}', '#ffd700', 10.5, '700', ls=3.5, op=0.9)}
{T(28, 60, title, 'url(#goldtxt)', 20, '700', ls=2.6, extra='filter="url(#glow)"')}
{T(TWL - 26, 60, cn, '#00f5ff', 20, '700', 'end', ls=4, op=0.75, fam=CJK)}
<line x1="28" y1="68" x2="{TWL - 26}" y2="68" stroke="#00f5ff" stroke-opacity="0.22"/>
<rect x="28" y="67" width="70" height="2" fill="url(#hl)"><animate attributeName="x" values="28;{TWL - 96};28" dur="4.6s" repeatCount="indefinite"/></rect>
{chr(10).join(body)}

<g clip-path="url(#pane2)">
<rect x="{TWL}" y="0" width="{SWR}" height="{H}" fill="#020812" fill-opacity="0.35"/>
<g transform="translate({TWL} 0)">
{scene_fn(SWR, H)}
{txt(14, 22, coord, '#5b7a99', 9)}
{txt(SWR - 14, 22, sector, '#ffd700', 10, 'end', 0.9, 2)}
{txt(SWR / 2, H - 12, 'SWALLOWED STAR // 吞噬星空', '#00f5ff', 8.5, 'middle', 0.45, 2.5)}
</g>
<rect x="{TWL}" y="0" width="{SWR}" height="40" fill="url(#scan)"><animate attributeName="y" values="0;{H - 40};0" dur="6s" repeatCount="indefinite"/></rect>
</g>
</g>
<rect x="0.5" y="0.5" width="{PW - 1}" height="{H - 1}" fill="none" stroke="#00f5ff" stroke-opacity="0.3" clip-path="url(#frame)"/>
<path d="M0 {H - 20} V{H} H20" fill="none" stroke="#ffd700" stroke-width="2" opacity="0"/>
<path d="M0 22 V2 H22" fill="none" stroke="#ffd700" stroke-width="2"/>
<path d="M{PW - 22} {H - 2} H{PW - 2} V{H - 22}" fill="none" stroke="#ffd700" stroke-width="2"/>
</svg>
"""
    with open(os.path.join(OUT, fname), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f'  ok {fname:<18} {PW}x{H}  {n_vis} baris  loop {total}s')


# =====================================================================
#  DATA (edit di sini)
# =====================================================================
GOLD, CYAN, GREEN = '#ffd700', '#00f5ff', '#00ff88'

panel('ssr-origin.svg', 1, 'PROFIL PRAJURIT', '起源', 'SECTOR 01 // ORIGIN', sc_whoami, [
    kv('Nama', 'Kavin Thoriq'),
    kv('Domisili', 'Bogor, Jawa Barat'),
    kv('Akademi', 'SMK TI Dwiguna Kota Depok'),
    kv('Jurusan', 'PPLG - Perangkat Lunak & Gim'),
    kv('Peringkat', 'Cosmic Grade', GOLD),
    kv('Spesialisasi', 'Web/Mobile · SQL · UI/UX · Game 2D'),
    kv('Motto', '"Adaptif. Terampil. Tangguh."', CYAN),
    gap(8),
    head('Misi'),
    *para('Siap berevolusi dan menembus batas dalam dunia Web & Game Development.', GREEN, 54),
    gap(4),
    *para('Siswa SMK PPLG yang menguasai dasar pemrograman web/mobile, SQL, dan UI/UX design. '
          'Adaptif, komunikatif, dan terbiasa bekerja dalam tim untuk menyelesaikan proyek software secara efektif.', '#b6cde6', 56, 12.5),
], seed=11, min_h=420)

panel('ssr-power.svg', 2, 'ATRIBUT KEKUATAN', '力量', 'SECTOR 02 // ORBITS', sc_skills, [
    head('Kekuatan teknis'),
    bar('Web & Mobile Dev', 82), bar('UI/UX Design', 75), bar('Game Dev 2D', 68),
    bar('SQL / Database', 72), bar('Git & GitHub', 78), bar('MS Office', 88),
    gap(6),
    head('Kekuatan jiwa'),
    bar('Problem Solving', 87, 'y'), bar('Kerja Sama Tim', 92, 'y'), bar('Logis & Analitis', 85, 'y'),
    bar('Adaptasi', 88, 'y'), bar('Ketelitian', 83, 'y'), bar('Komunikasi', 80, 'y'),
], seed=12)

panel('ssr-arsenal.svg', 3, 'ARSENAL BINTANG', '兵器', 'SECTOR 03 // ARSENAL', sc_stack, [
    kv('Web', 'HTML5 · CSS3 · JavaScript · PHP', CYAN),
    kv('Database', 'MySQL', CYAN),
    kv('Desain', 'Figma · UI/UX Prototype', GOLD),
    kv('Versi', 'Git · GitHub', GOLD),
    kv('Editor', 'VS Code · Microsoft Office'),
    kv('Sistem', 'Linux (dasar)'),
    kv('Game', 'RPG Maker MZ · Scratch', GREEN),
    gap(8),
    *para('12 senjata terpasang. Setiap alat adalah bintang yang siap dihubungkan menjadi rasi.', '#7f9bb8', 54, 12),
], seed=13)

panel('ssr-starmap.svg', 4, 'PETA BINTANG PROJECT', '星图', 'SECTOR 04 // STAR MAP', sc_projects, [
    item('P-001', 'Go To School: Mathemagic Adventure', 'GAME REALM · 2024', 'COMPLETED', GREEN),
    item('P-002', 'PlengerToSmart', 'WEB REALM · 2025', 'IN PROGRESS', GOLD, CYAN),
    item('P-003', 'Geometry Dash (Fan Game)', 'GAME REALM · 2024', 'COMPLETED', GREEN),
    item('P-004', 'Vynz News', 'WEB REALM · 2025', 'COMPLETED', GREEN, CYAN),
    item('P-005', 'StudyNote', 'DESIGN REALM · 2025', 'COMPLETED', GREEN, GREEN),
    item('P-006', 'SMK TI Dwiguna - Website Design', 'DESIGN REALM · 2025', 'COMPLETED', GREEN, GREEN),
], seed=14)

panel('ssr-journey.svg', 5, 'JALUR KULTIVASI', '征途', 'SECTOR 05 // TRAJECTORY', sc_missions, [
    item('M-001', 'SMK TI Dwiguna Kota Depok (PPLG)', '2024 - sekarang', 'ACTIVE', GREEN, GREEN),
    item('M-002', 'Website & Database System', '2024 - 2025', 'COMPLETED', CYAN, CYAN),
    item('M-003', 'UI/UX Prototype Design (Figma)', '2024 - 2025', 'COMPLETED', CYAN, CYAN),
    item('M-004', 'Game Development 2D', '2025 - sekarang', 'IN PROGRESS', GOLD),
    gap(8),
    *para('Misi berikutnya: naik level setiap hari.', GREEN, 54, 12.5),
], seed=15)

panel('ssr-radar.svg', 6, 'RADAR KEKUATAN', '探测', 'SECTOR 06 // RADAR', sc_stats, [
    kv('Status', 'Radar aktif', GREEN),
    kv('Memindai', 'commits · repos · stars · PR · streak'),
    kv('Siklus', 'Satu sapuan setiap 5 detik'),
    gap(8),
    *para('Data energi GitHub ditampilkan langsung di bawah panel ini.', '#7f9bb8', 54, 12),
], seed=16, min_h=300)

panel('ssr-legend.svg', 7, 'KATA-KATA LEGENDA', '传说', 'SECTOR 07 // 吞噬星空', sc_quote, [
    gap(6),
    *para('"Dalam alam semesta ini, yang lemah tidak memiliki hak untuk hidup dengan nyaman. '
          'Hanya yang kuat yang bisa melindungi apa yang mereka cintai."', GOLD, 36, 16),
    gap(8),
    dict(t='line', text='- Luo Feng, Swallowed Star 吞噬星空', c='#7f9bb8', size=12, h=20),
], seed=17, min_h=300)

panel('ssr-signal.svg', 8, 'TRANSMISI SINYAL', '讯号', 'SECTOR 08 // UPLINK', sc_contact, [
    kv('GitHub', 'github.com/kavinthoriq', CYAN),
    kv('Email', 'kavinthoriq46@gmail.com', GOLD),
    kv('Portfolio', 'kavinthoriq.github.io/Portfolio', GREEN),
    kv('Lokasi', 'Bogor, Jawa Barat'),
    gap(8),
    head('Saluran aktif'),
    *para('Siap menerima transmisi. Terbuka untuk kolaborasi, proyek baru, dan diskusi teknologi.', '#b6cde6', 54, 12.5),
], seed=18)
