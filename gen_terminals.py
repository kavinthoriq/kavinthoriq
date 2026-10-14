#!/usr/bin/env python3
"""
Generator SVG terminal animasi (efek mengetik di Linux) untuk README profil GitHub.

Pakai:   python3 assets/gen_terminals.py
Hasil:   assets/whoami.svg, skills.svg, stack.svg, projects.svg,
         missions.svg, stats.svg, quote.svg, contact.svg

Edit teks di bagian DATA di bawah, jalankan ulang, lalu commit file .svg barunya.
"""
import html
import os
import unicodedata

CW = 7.8      # lebar 1 karakter (px) pada font-size 13
LH = 22       # tinggi baris
FS = 13
X0 = 24
OUT = os.path.dirname(os.path.abspath(__file__))

COL = {
    'g': '#00ff88', 'c': '#00f5ff', 'y': '#ffd700', 'w': '#d0e8ff',
    'b': '#0099ff', 'm': '#5b7a99', 'p': '#ff7ab2',
}


def cols(s):
    return sum(2 if unicodedata.east_asian_width(ch) in 'WF' else 1 for ch in s)


def nb(s):
    return s.replace(' ', '\u00a0')


def kt(*xs):
    return ';'.join(f'{x:.5f}' for x in xs)


# ---------- helper baris ----------
def prompt(cmd, path='~'):
    return dict(cmd=True, segs=[('kavin@hr-alliance', 'g'), (':', 'w'), (path, 'b'), ('$ ', 'w'), (cmd, 'y')])


def o(text, c='w'):
    return dict(segs=[(text, c)])


def multi(*segs):
    return dict(segs=list(segs))


def blank():
    return dict(blank=True, segs=[])


# ---------- builder ----------
def build(fname, title, lines, hold=3.5):
    t = 0.5
    items = []
    for idx, l in enumerate(lines):
        if l.get('blank'):
            items.append(None)
            t += 0.2
            continue
        text = ''.join(s for s, _ in l['segs'])
        n = cols(text)
        cmd = l.get('cmd')
        dur = max(0.2, n * (0.05 if cmd else 0.02))
        s, e = t, t + dur
        t = e + (0.45 if cmd else 0.1)
        items.append(dict(idx=idx, s=s, e=e, n=n, segs=l['segs']))
    T = round(t + hold, 2)
    live = [it for it in items if it]
    H = 40 + 20 + LH * len(lines) + 20
    end_hold = (T - 0.4) / T

    defs, body = [], []
    for k, it in enumerate(live):
        idx = it['idx']
        base = 40 + 28 + idx * LH
        W = it['n'] * CW
        if X0 + W > 780:
            print(f'  [warn] {fname}: baris {idx} terlalu panjang ({it["n"]} kolom)')
        keyT = kt(0, it['s'] / T, it['e'] / T, end_hold, 1)
        defs.append(
            f'<clipPath id="c{idx}"><rect x="{X0}" y="{base - 14}" width="0" height="19">'
            f'<animate attributeName="width" values="0;0;{W:.1f};{W:.1f};0" keyTimes="{keyT}" '
            f'dur="{T}s" repeatCount="indefinite"/></rect></clipPath>'
        )
        tsp = ''.join(
            f'<tspan fill="{COL[c]}">{html.escape(nb(txt))}</tspan>' for txt, c in it['segs']
        )
        body.append(
            f'<g clip-path="url(#c{idx})"><text x="{X0}" y="{base}" textLength="{W:.1f}" '
            f'lengthAdjust="spacing">{tsp}</text></g>'
        )
        nxt = live[k + 1]['s'] if k + 1 < len(live) else T - 0.4
        visT = kt(0, it['s'] / T, nxt / T, 1)
        body.append(
            f'<g><animate attributeName="opacity" values="1;0" calcMode="discrete" dur="0.8s" repeatCount="indefinite"/>'
            f'<rect x="{X0}" y="{base - 12}" width="7" height="15" fill="#00ff88" opacity="0">'
            f'<animate attributeName="x" values="{X0};{X0};{X0 + W:.1f};{X0 + W:.1f};{X0}" keyTimes="{keyT}" '
            f'dur="{T}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;0;0" calcMode="discrete" keyTimes="{visT}" '
            f'dur="{T}s" repeatCount="indefinite"/></rect></g>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {H}" width="800" height="{H}" role="img" aria-label="{html.escape(title)}">
<defs>
{chr(10).join(defs)}
<filter id="tglow" x="-5%" y="-30%" width="110%" height="160%"><feGaussianBlur stdDeviation="1.1" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00f5ff" stop-opacity="0"/><stop offset="0.5" stop-color="#00f5ff" stop-opacity="0.07"/><stop offset="1" stop-color="#00f5ff" stop-opacity="0"/></linearGradient>
</defs>
<rect width="800" height="{H}" rx="12" fill="#020812"/>
<rect x="0.5" y="0.5" width="799" height="{H - 1}" rx="12" fill="none" stroke="#00f5ff" stroke-opacity="0.3"/>
<path d="M0 12 A12 12 0 0 1 12 0 H788 A12 12 0 0 1 800 12 V40 H0 Z" fill="#06142a"/>
<line x1="0" y1="40" x2="800" y2="40" stroke="#00f5ff" stroke-opacity="0.2"/>
<circle cx="24" cy="20" r="6" fill="#ff5f56"/><circle cx="46" cy="20" r="6" fill="#ffbd2e"/><circle cx="68" cy="20" r="6" fill="#27c93f"/>
<text x="400" y="25" text-anchor="middle" font-family="'Courier New', Courier, monospace" font-size="12" fill="#00f5ff" fill-opacity="0.8" letter-spacing="1">{html.escape(title)}</text>
<g font-family="'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, 'Courier New', monospace" font-size="{FS}" filter="url(#tglow)">
{chr(10).join(body)}
</g>
<rect x="0" y="40" width="800" height="40" fill="url(#scan)"><animate attributeName="y" values="40;{H - 60};40" dur="6s" repeatCount="indefinite"/></rect>
</svg>
'''
    with open(os.path.join(OUT, fname), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f'  ok {fname}  ({len(lines)} baris, loop {T}s)')


# =====================================================================
#  DATA
# =====================================================================
def kv(k, v):
    return multi((f'{k:<11}= ', 'c'), (v, 'w'))


def bar(name, pct, color):
    f = round(pct / 5)
    return multi((f'{name:<28}', 'w'), ('[', 'm'), ('█' * f, color), ('░' * (20 - f), 'm'), (']', 'm'), (f' {pct}%', color))


# 1. whoami
build('whoami.svg', 'kavin@hr-alliance: ~/whoami', [
    prompt('cat /etc/operator.conf'),
    blank(),
    kv('NAMA', 'Kavin Thoriq'),
    kv('DOMISILI', 'Bogor, Jawa Barat'),
    kv('SEKOLAH', 'SMK TI Dwiguna Kota Depok'),
    kv('JURUSAN', 'Pengembangan Perangkat Lunak dan Gim (PPLG)'),
    kv('CLASS', 'Cosmic Grade'),
    kv('SPECIALTY', 'Web / Mobile - SQL - UI/UX - Game Dev 2D'),
    kv('MOTTO', '"Adaptif. Terampil. Tangguh."'),
    blank(),
    prompt('echo $MISSION'),
    o('Siap berevolusi dan menembus batas dalam dunia Web & Game Development.', 'g'),
    blank(),
    prompt('cat about.txt'),
    o('Siswa SMK PPLG yang menguasai dasar pemrograman web/mobile, SQL, dan UI/UX design.'),
    o('Adaptif, komunikatif, dan terbiasa bekerja dalam tim untuk menyelesaikan proyek'),
    o('software secara efektif.'),
])

# 2. skills
build('skills.svg', 'kavin@hr-alliance: ~/atribut', [
    prompt('./atribut --hard --soft'),
    blank(),
    o('# HARD SKILLS -- kemampuan teknis terukur', 'y'),
    bar('Pemrograman Web & Mobile', 82, 'c'),
    bar('UI/UX Design', 75, 'c'),
    bar('Game Development 2D', 68, 'c'),
    bar('Pengelolaan Database (SQL)', 72, 'c'),
    bar('Git & GitHub', 78, 'c'),
    bar('Microsoft Office', 88, 'c'),
    blank(),
    o('# SOFT SKILLS -- kemampuan interpersonal', 'y'),
    bar('Problem Solving', 87, 'y'),
    bar('Kerja Sama Tim', 92, 'y'),
    bar('Berpikir Logis & Analitis', 85, 'y'),
    bar('Kemampuan Beradaptasi', 88, 'y'),
    bar('Ketelitian', 83, 'y'),
    bar('Komunikasi', 80, 'y'),
])

# 3. stack
pkgs = ['html5', 'css3', 'javascript', 'php', 'mysql', 'figma', 'git', 'github',
        'vscode', 'game-engine', 'ms-office', 'linux-basics']
stack = [prompt('apt list --installed | grep -E "web|db|design|game"'), o('Listing... Done', 'm')]
for p in pkgs:
    stack.append(multi((p, 'g'), ('/stable', 'm'), (' ' * (30 - len(p) - 7), 'w'), ('[installed]', 'c')))
stack.append(o('12 packages installed, 0 broken.', 'y'))
build('stack.svg', 'kavin@hr-alliance: ~/arsenal', stack)

# 4. projects
def pj(pid, name, cat, year, status):
    sc = 'g' if status == 'COMPLETED' else 'y'
    return multi((pid + '  ', 'c'), (f'{name:<36}', 'w'), (f'{cat:<8}', 'b'), (f'{year:<6}', 'm'), (status, sc))


build('projects.svg', 'kavin@hr-alliance: ~/project-archive', [
    prompt('ls -l ./project-archive', '~'),
    o('total 6', 'm'),
    pj('P-001', 'Go To School: Mathemagic Adventure', 'GAME', '2024', 'COMPLETED'),
    pj('P-002', 'PlengerToSmart', 'WEB', '2025', 'IN PROGRESS'),
    pj('P-003', 'Geometry Dash (Fan Game)', 'GAME', '2024', 'COMPLETED'),
    pj('P-004', 'Vynz News', 'WEB', '2025', 'COMPLETED'),
    pj('P-005', 'StudyNote', 'DESIGN', '2025', 'COMPLETED'),
    pj('P-006', 'SMK TI Dwiguna - Website Design', 'DESIGN', '2025', 'COMPLETED'),
    blank(),
    o('6 projects: 5 completed, 1 in progress', 'y'),
    prompt('cat details.md', '~/project-archive'),
    o('# detail, demo & source code ada di tabel di bawah', 'm'),
])

# 5. missions
def ms(mid, status, text, period):
    sc = 'g' if status == 'ACTIVE' else ('y' if status == 'IN PROGRESS' else 'c')
    return multi((mid + ' ', 'm'), (f'{"[" + status + "]":<14}', sc), (f'{text:<40}', 'w'), (period, 'm'))


build('missions.svg', 'kavin@hr-alliance: ~/mission-log', [
    prompt('cat ./mission-log'),
    blank(),
    ms('M-001', 'ACTIVE', 'SMK TI Dwiguna Kota Depok (PPLG)', '2024 - sekarang'),
    ms('M-002', 'COMPLETED', 'Website & Database System', '2024 - 2025'),
    ms('M-003', 'COMPLETED', 'UI/UX Prototype Design (Figma)', '2024 - 2025'),
    ms('M-004', 'IN PROGRESS', 'Game Development 2D (Indie Project)', '2025 - sekarang'),
    blank(),
    prompt('tail -n 1 ./mission-log'),
    o('> next mission: level up setiap hari.', 'g'),
])

# 6. stats
build('stats.svg', 'kavin@hr-alliance: ~/stats', [
    prompt('./stats --live'),
    o('[ OK ] fetching commits, repos, languages, streak...', 'g'),
    o('[ OK ] rendering widgets', 'g'),
], hold=4)

# 7. quote
build('quote.svg', 'kavin@hr-alliance: ~/quote', [
    prompt('cat ./quote.txt'),
    blank(),
    o('"Dalam alam semesta ini, yang lemah tidak memiliki hak untuk hidup', 'y'),
    o('dengan nyaman. Hanya yang kuat yang bisa melindungi apa yang mereka', 'y'),
    o('cintai."', 'y'),
    blank(),
    o('                              - Luo Feng, Swallowed Star 吞噬星空', 'm'),
])

# 8. contact
def ct(k, v):
    return multi((f'{k:<11}', 'c'), (v, 'w'))


build('contact.svg', 'kavin@hr-alliance: ~/transmit', [
    prompt('ping kavin --transmit'),
    o('> CHANNEL AKTIF - SIAP MENERIMA TRANSMISI', 'g'),
    blank(),
    ct('github', 'github.com/kavinthoriq'),
    ct('email', 'kavinthoriq46@gmail.com'),
    ct('portfolio', 'kavinthoriq.github.io/Portfolio'),
    ct('lokasi', 'Bogor, Jawa Barat'),
    blank(),
    prompt('./collab --open'),
    o('> Terbuka untuk kolaborasi, proyek baru, dan diskusi teknologi.', 'g'),
    prompt(''),
], hold=4)
