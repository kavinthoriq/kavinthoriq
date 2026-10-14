#!/usr/bin/env python3
"""
Generator kartu project bertema Swallowed Star (SVG animasi + screenshot tertanam).

Pakai:
    SHOTS_DIR=/folder/screenshot python3 assets/gen_project_cards.py
Hasil:
    assets/proj-p001.svg ... proj-p006.svg

Edit daftar `projects` di bawah, jalankan ulang, commit SVG barunya.
Screenshot di-embed sebagai base64, jadi tampil di GitHub tanpa file gambar tambahan.
"""
import base64
import html
import io
import os
import random
import textwrap

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.environ.get('SHOTS_DIR', '/mnt/user-data/uploads')

W, H = 420, 462
ACC = {'Web': '#00f5ff', 'Game': '#ffd700', 'Design': '#00ff88'}
REALM = {'Web': 'WEB REALM', 'Game': 'GAME REALM', 'Design': 'DESIGN REALM'}

projects = [
    dict(id='P-001', title='Go To School: Mathemagic Adventure', cat='Game', year='2024', status='COMPLETED',
         desc='Game RPG edukasi bertema matematika. Ikuti perjalanan Vynz ke sekolah, lewati ujian karakter, lalu jelajahi Dunia Bilangan.',
         tags=['RPG Maker MZ', 'JavaScript'], shot='Screenshot_2026-10-14_121306.png'),
    dict(id='P-002', title='PlengerToSmart', cat='Web', year='2025', status='IN PROGRESS',
         desc='Website edukasi: materi video, kuis berwaktu dengan nilai otomatis dan leaderboard, artikel, serta forum diskusi komunitas.',
         tags=['PHP', 'MySQL'], shot='Screenshot_2026-10-14_122049.png'),
    dict(id='P-003', title='Geometry Dash (Fan Game)', cat='Game', year='2024', status='COMPLETED',
         desc='Platformer ritme ala Geometry Dash yang bisa dimainkan langsung di browser. Lompat, hindari rintangan, bertahan sampai akhir level.',
         tags=['Scratch'], shot='Screenshot_2026-10-14_122349.png'),
    dict(id='P-004', title='Vynz News', cat='Web', year='2025', status='COMPLETED',
         desc='Portal berita teknologi: AI, startup, web dev, edukasi digital, dan cybersecurity. Dark mode, responsif, tanpa framework.',
         tags=['HTML', 'CSS', 'JavaScript'], shot='Screenshot_2026-10-14_122628.png'),
    dict(id='P-005', title='StudyNote', cat='Design', year='2025', status='COMPLETED',
         desc='Desain UI aplikasi catatan sekolah dan pengingat tugas untuk siswa SMA/SMK, semua tugas dan ringkasan materi di satu tempat.',
         tags=['Figma', 'UI/UX'], shot='Screenshot_2026-10-14_123129.png'),
    dict(id='P-006', title='SMK TI Dwiguna - Website Design', cat='Design', year='2025', status='COMPLETED',
         desc='Desain UI website resmi SMK TI Dwiguna Depok, "Forging Future Mechanics": halaman Beranda, Galeri, dan Kontak.',
         tags=['Figma', 'UI/UX'], shot='Screenshot_2026-10-14_123421.png'),
]


def thumb_b64(path):
    im = Image.open(path).convert('RGB')
    w, h = im.size
    # buang chrome browser (tab + address bar) dan scrollbar
    box = (min(6, w), min(82, h - 1), max(w - 20, 1), h - 6)
    im = im.crop(box).resize((570, 270), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=78, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def esc(s):
    return html.escape(s, quote=True)


def card(p):
    acc = ACC[p['cat']]
    done = p['status'] == 'COMPLETED'
    sc = '#00ff88' if done else '#ffd700'
    rnd = random.Random(p['id'])
    cut, tcut = 22, 14

    card_path = f'M0 0 H{W - cut} L{W} {cut} V{H} H{cut} L0 {H - cut} Z'
    th_x, th_y, th_w, th_h = 20, 44, 380, 180
    th_path = (f'M{th_x} {th_y} H{th_x + th_w - tcut} L{th_x + th_w} {th_y + tcut} '
               f'V{th_y + th_h} H{th_x + tcut} L{th_x} {th_y + th_h - tcut} Z')

    stars = ''.join(
        f'<circle cx="{rnd.randint(6, W - 6)}" cy="{rnd.randint(6, H - 6)}" r="{rnd.choice([0.8, 1, 1.3])}" '
        f'fill="{rnd.choice(["#ffffff", "#00f5ff"])}">'
        f'<animate attributeName="opacity" values="0.15;1;0.15" dur="{rnd.uniform(2, 4.5):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(26)
    )

    # deskripsi
    lines = textwrap.wrap(p['desc'], width=56)
    assert len(lines) <= 4, f"{p['id']} deskripsi terlalu panjang ({len(lines)} baris)"
    desc = ''.join(
        f'<text x="20" y="{298 + i * 17}" font-family="\'Segoe UI\', Arial, sans-serif" font-size="12" fill="#b6cde6">{esc(l)}</text>'
        for i, l in enumerate(lines)
    )

    # tag chips
    chips, x = [], 20
    for t in p['tags']:
        cw = 7 * len(t) + 18
        chips.append(
            f'<rect x="{x}" y="368" width="{cw}" height="20" fill="{acc}" fill-opacity="0.08" stroke="{acc}" stroke-opacity="0.5"/>'
            f'<text x="{x + cw / 2:.1f}" y="382" text-anchor="middle" font-family="\'Courier New\', monospace" font-size="11" fill="{acc}">{esc(t)}</text>'
        )
        x += cw + 8
    assert x - 8 <= 400, f"{p['id']} tag terlalu panjang"

    # progress bar
    if done:
        bar = (f'<rect x="20" y="424" width="380" height="8" rx="4" fill="url(#bar)"/>')
    else:
        bar = (f'<rect x="20" y="424" width="380" height="8" rx="4" fill="#ffd700" fill-opacity="0.1" stroke="#ffd700" stroke-opacity="0.25"/>'
               f'<rect x="20" y="424" width="250" height="8" rx="4" fill="url(#bar)"><animate attributeName="opacity" values="0.65;1;0.65" dur="1.8s" repeatCount="indefinite"/></rect>')
    shimmer = (f'<g clip-path="url(#trk)"><rect x="-60" y="424" width="60" height="8" fill="url(#shim)">'
               f'<animate attributeName="x" values="-60;{400 if done else 270}" dur="2.4s" repeatCount="indefinite"/></rect></g>')

    status_txt = p['status']
    sx = W - 38
    dot_x = sx - 6.6 * len(status_txt) - 14

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(p['id'] + ' ' + p['title'])}">
<defs>
<clipPath id="card"><path d="{card_path}"/></clipPath>
<clipPath id="thumb"><path d="{th_path}"/></clipPath>
<clipPath id="trk"><rect x="20" y="424" width="{380 if done else 250}" height="8" rx="4"/></clipPath>
<radialGradient id="neb" cx="50%" cy="0%" r="80%"><stop offset="0" stop-color="{acc}" stop-opacity="0.16"/><stop offset="1" stop-color="#020812" stop-opacity="0"/></radialGradient>
<linearGradient id="vig" x1="0" y1="0" x2="0" y2="1"><stop offset="0.55" stop-color="#020812" stop-opacity="0"/><stop offset="1" stop-color="#020812" stop-opacity="0.85"/></linearGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{acc}" stop-opacity="0"/><stop offset="0.5" stop-color="{acc}" stop-opacity="0.28"/><stop offset="1" stop-color="{acc}" stop-opacity="0"/></linearGradient>
<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0099ff"/><stop offset="0.6" stop-color="{acc}"/><stop offset="1" stop-color="#ffd700"/></linearGradient>
<linearGradient id="shim" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.7"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="1.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>

<path d="{card_path}" fill="#020812"/>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#neb)"/>
{stars}
</g>
<path d="{card_path}" fill="none" stroke="{acc}" stroke-width="1.2" stroke-opacity="0.35"><animate attributeName="stroke-opacity" values="0.22;0.7;0.22" dur="3.6s" repeatCount="indefinite"/></path>
<path d="M0 18 V0 H18" fill="none" stroke="#ffd700" stroke-width="2"/>
<path d="M{W - 18} {H} H{W} V{H - 18}" fill="none" stroke="#ffd700" stroke-width="2"/>

<text x="20" y="28" font-family="'Courier New', monospace" font-size="11" fill="{acc}" fill-opacity="0.85" letter-spacing="1.5">MISSION FILE // {esc(p['id'])}</text>
<circle cx="{dot_x:.1f}" cy="24.5" r="3.5" fill="{sc}"><animate attributeName="opacity" values="1;0.35;1" dur="1.8s" repeatCount="indefinite"/></circle>
<text x="{sx}" y="28" text-anchor="end" font-family="'Courier New', monospace" font-size="11" fill="{sc}" letter-spacing="1">{esc(status_txt)}</text>

<image xlink:href="data:image/jpeg;base64,{thumb_b64(os.path.join(SHOTS, p['shot']))}" x="{th_x}" y="{th_y}" width="{th_w}" height="{th_h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#thumb)"/>
<g clip-path="url(#thumb)">
<rect x="{th_x}" y="{th_y}" width="{th_w}" height="{th_h}" fill="url(#vig)"/>
<rect x="{th_x}" y="{th_y}" width="{th_w}" height="34" fill="url(#scan)"><animate attributeName="y" values="{th_y - 34};{th_y + th_h};{th_y - 34}" dur="3.4s" repeatCount="indefinite"/></rect>
</g>
<path d="{th_path}" fill="none" stroke="{acc}" stroke-width="1.4" stroke-opacity="0.8"/>
<rect x="{th_x + 8}" y="{th_y + th_h - 26}" width="{7.2 * len(REALM[p['cat']]) + 18:.1f}" height="18" fill="#020812" fill-opacity="0.88" stroke="{acc}" stroke-opacity="0.7"/>
<text x="{th_x + 17}" y="{th_y + th_h - 13}" font-family="'Courier New', monospace" font-size="11" fill="{acc}" letter-spacing="1">{REALM[p['cat']]}</text>
<rect x="{th_x + th_w - 54}" y="{th_y + 8}" width="46" height="18" fill="#020812" fill-opacity="0.88" stroke="#ffd700" stroke-opacity="0.6"/>
<text x="{th_x + th_w - 31}" y="{th_y + 21}" text-anchor="middle" font-family="'Courier New', monospace" font-size="11" fill="#ffd700">{esc(p['year'])}</text>

<text x="20" y="256" font-family="Orbitron, 'Segoe UI', Arial, sans-serif" font-weight="700" font-size="16" fill="#ffffff" filter="url(#glow)">{esc(p['title'])}</text>
<text x="20" y="274" font-family="'Courier New', monospace" font-size="10" fill="{acc}" fill-opacity="0.7" letter-spacing="1.2">OPERATOR: KAVIN THORIQ  //  CLEARANCE: COSMIC GRADE</text>
{desc}

<line x1="20" y1="358" x2="400" y2="358" stroke="{acc}" stroke-opacity="0.2"/>
{''.join(chips)}

<text x="20" y="416" font-family="'Courier New', monospace" font-size="10" fill="#5b7a99" letter-spacing="1.5">MISSION STATUS</text>
<text x="400" y="416" text-anchor="end" font-family="'Courier New', monospace" font-size="10" fill="{sc}" letter-spacing="1.5">{'100% SYNCED' if done else 'IN PROGRESS'}</text>
{bar}
{shimmer}
<text x="{W / 2}" y="452" text-anchor="middle" font-family="'Courier New', monospace" font-size="9" fill="#00f5ff" fill-opacity="0.35" letter-spacing="2.5">SWALLOWED STAR // HR.ALLIANCE</text>
</svg>
'''
    return svg


for p in projects:
    name = f"proj-{p['id'].lower().replace('-', '')}.svg"
    with open(os.path.join(HERE, name), 'w', encoding='utf-8') as f:
        f.write(card(p))
    print('ok', name, os.path.getsize(os.path.join(HERE, name)) // 1024, 'KB')
