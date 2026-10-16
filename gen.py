#!/usr/bin/env python3
"""プロフィール用の動く SVG を作る: python3 gen.py"""
import math
import random

random.seed(226)
BG, INK, BARK = '#E3E8E2', '#22332C', '#4A3F35'
MOSS, FERN, LICHEN, POLLEN = '#5F8566', '#86A77A', '#B9C79A', '#E2BE5A'
W, H, GROUND, TX = 1000, 320, 268, 760   # TX: 木の根元の x
SERIF = "font-family:Georgia,'Hiragino Mincho ProN','Noto Serif JP',serif"


def tree(x, y, ang, ln, depth, t0, out):
    """枝を根元から順に描き、先端に葉を付ける。t0 はその枝が伸び始める秒。"""
    ex, ey = x + ln * math.cos(ang), y - ln * math.sin(ang)
    bend = random.uniform(-.12, .12) * ln
    cx, cy = (x + ex) / 2 + bend * math.sin(ang), (y + ey) / 2 + bend * math.cos(ang)
    dur = .42
    out['b'].append(f'<path d="M{x:.1f} {y:.1f}Q{cx:.1f} {cy:.1f} {ex:.1f} {ey:.1f}" stroke-width="{.6 + depth * 1.1:.1f}" '
                    f'pathLength="1" style="animation:draw {dur}s ease-out {t0:.2f}s backwards"/>')
    if depth == 0:
        for _ in range(3):
            c = POLLEN if random.random() < .06 else random.choice((MOSS, FERN, FERN, LICHEN))
            lx, ly = ex + random.uniform(-9, 9), ey + random.uniform(-9, 6)
            out['l'].append(f'<ellipse class="c" cx="{lx:.1f}" cy="{ly:.1f}" rx="{random.uniform(5, 8):.1f}" ry="{random.uniform(3, 5):.1f}" '
                            f'fill="{c}" transform="rotate({random.randint(0, 180)})" '
                            f'style="animation:leaf .6s cubic-bezier(.3,1.6,.5,1) {t0 + dur + random.uniform(0, .5):.2f}s backwards"/>')
        return
    for _ in range(3 if depth > 4 and random.random() < .3 else 2):
        tree(ex, ey, ang + random.uniform(-.55, .55), ln * random.uniform(.7, .8), depth - 1, t0 + dur, out)


def header():
    parts = {'b': [], 'l': []}
    tree(TX, GROUND, math.pi / 2, 58, 7, .3, parts)
    # 地面は GitHub の草(contribution graph)。ところどころのマスから芽が出ては引っ込む
    lv = (BG, '#D2DACF', LICHEN, FERN, MOSS)
    cells = ''.join(f'<rect x="{40 + i * 15}" y="{GROUND + 4}" width="12" height="12" rx="2.5" fill="{random.choice(lv)}"/>'
                    for i in range(62))
    sprouts = ''.join(
        f'<g class="s" style="transform-origin:{46 + i * 15}px {GROUND + 4}px;animation:sprout 14s ease-out {d:.1f}s infinite backwards">'
        f'<path d="M{46 + i * 15} {GROUND + 4}v-11" stroke="{MOSS}" stroke-width="1.6"/>'
        f'<ellipse cx="{42 + i * 15}" cy="{GROUND - 7}" rx="4.5" ry="2.4" fill="{FERN}" transform="rotate(-25 {42 + i * 15} {GROUND - 7})"/>'
        f'<ellipse cx="{50 + i * 15}" cy="{GROUND - 9}" rx="4.5" ry="2.4" fill="{MOSS}" transform="rotate(25 {50 + i * 15} {GROUND - 9})"/></g>'
        for i, d in zip(random.sample(range(62), 7), (5, 6.5, 8, 9.5, 11, 12.5, 14)))
    dots = ''.join(f'<tspan style="animation:dot 2.4s ease-in-out {k * .4:.1f}s infinite">.</tspan>' for k in range(3))
    css = (".c{transform-box:fill-box;transform-origin:center}.s{transform-box:view-box}"
           "@keyframes draw{from{stroke-dasharray:1;stroke-dashoffset:1}to{stroke-dasharray:1;stroke-dashoffset:0}}"
           "@keyframes leaf{from{transform:scale(0)}}"
           f"@keyframes sway{{from{{transform:rotate(-.7deg)}}to{{transform:rotate(.7deg)}}}}"
           "@keyframes sprout{0%{transform:scale(0)}6%,80%{transform:scale(1)}88%,100%{transform:scale(0)}}"
           "@keyframes dot{0%,100%{opacity:.2}50%{opacity:1}}"
           "@keyframes fall{0%{transform:translate(0,0) rotate(0);opacity:0}5%{opacity:1}"
           "25%{transform:translate(-30px,40px) rotate(90deg)}50%{transform:translate(10px,80px) rotate(200deg)}"
           "75%{transform:translate(-25px,112px) rotate(300deg);opacity:1}85%,100%{transform:translate(-15px,124px) rotate(340deg);opacity:0}}"
           "@keyframes rise{from{opacity:0;transform:translateY(8px)}}"
           "@media (prefers-reduced-motion:reduce){*{animation:none!important}.f{display:none}}")
    body = (
        f'<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>'
        f'<g style="{SERIF};animation:rise 1.2s ease-out .2s backwards">'
        f'<text x="60" y="140" font-size="54" fill="{INK}" letter-spacing="1">mickey0226</text>'
        f'<text x="62" y="182" font-size="22" font-style="italic" fill="{MOSS}">planting trees{dots}</text>'
        f'<text x="62" y="214" font-size="16" fill="{INK}" opacity=".7">ひとつずつ、ゆっくり育てています</text></g>'
        f'{cells}{sprouts}'
        f'<g style="transform-box:view-box;transform-origin:{TX}px {GROUND}px;animation:sway 7s ease-in-out 5s infinite alternate">'
        f'<g fill="none" stroke="{BARK}" stroke-linecap="round">{"".join(parts["b"])}</g>{"".join(parts["l"])}</g>'
        f'<ellipse class="c f" cx="{TX + 40}" cy="140" rx="6" ry="3.5" fill="{POLLEN}" style="animation:fall 11s ease-in-out 7s infinite backwards"/>')
    label = 'mickey0226 — 木が一本ゆっくり育ち、足もとの草のマスから芽が出る'
    with open('header.svg', 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
                f'aria-label="{label}"><title>{label}</title><style>{css}</style>{body}</svg>\n')


header()
