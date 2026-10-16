#!/usr/bin/env python3
"""プロフィール用の動く SVG を作る: python3 gen.py
ぼやけた世界から畳み込み(ぼかし)が一段ずつ外れ、視界が中心から広がっていく。月・灯籠・蛍・流れ星が動き続ける。"""
import random

random.seed(226)
W, H, T = 1000, 320, 16                 # T: 1 周の秒数
BLUR = (24, 14, 8, 4, 1.8)              # 外れていくぼかしの強さ(上の層ほど強い)
OFF = [1.4 + k * 1.5 for k in range(5)]  # 各層が消え始める秒
BACK = [13 + (4 - k) * .35 for k in range(5)]  # 周の終わりに戻ってくる秒
APER = (.1, .2, .34, .52, .74, 1)       # 各段の視界の広さ


def pct(t):
    return f'{t / T * 100:.2f}%'


def ridge(y0, amp, color):
    pts, y = [], y0
    for x in range(-20, W + 41, 20):
        y = y0 + (y - y0) * .7 + random.uniform(-amp, amp)
        pts.append(f'{x},{y:.0f}')
    return f'<polygon points="-20,{H} {" ".join(pts)} {W + 40},{H}" fill="{color}"/>'


def scene():
    """夕暮れの湖畔。月が水面に揺れ、灯籠が昇り、蛍が漂い、ときどき流れ星が走る。"""
    rnd = random.uniform
    stars = ''.join(f'<circle cx="{rnd(0, W):.0f}" cy="{rnd(0, 170):.0f}" r="{rnd(.6, 1.5):.1f}" '
                    f'fill="#F3EEF7" opacity="{rnd(.4, .9):.2f}" '
                    f'style="animation:tw {rnd(3, 6):.1f}s ease-in-out {rnd(-6, 0):.1f}s infinite alternate"/>'
                    for _ in range(70))
    meteors = ''.join(f'<path d="M{x} {y}l-90 36" stroke="url(#tail)" stroke-width="1.4" stroke-linecap="round" '
                      f'style="animation:meteor {p}s ease-in {d}s infinite"/>' for x, y, p, d in ((420, 20, 7, 2), (900, 40, 11, 6)))
    moon = ('<circle class="c" cx="760" cy="72" r="70" fill="url(#halo)" style="animation:breathe 6s ease-in-out infinite alternate"/>'
            '<circle cx="760" cy="72" r="15" fill="#FBEFD9"/>')
    glint = ''.join(f'<rect class="c" x="{760 - w / 2 + rnd(-5, 5):.0f}" y="{y + rnd(-1.5, 1.5):.1f}" width="{w:.0f}" height="1.2" rx=".6" fill="#FBEFD9" opacity="{.55 - (y - 212) / 200:.2f}" '
                    f'style="animation:glint {rnd(1.6, 3):.1f}s ease-in-out {rnd(-3, 0):.1f}s infinite alternate"/>'
                    for y in range(212, 300, 4) for w in [rnd(8, 18) + (y - 212) * .5])
    lights = ''
    for _ in range(26):
        x, y, r = rnd(40, W - 40), rnd(204, 212), rnd(1, 2.2)
        lights += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#F2C879"/>'
                   f'<rect x="{x - r / 2:.1f}" y="{y + 6:.0f}" width="{r:.1f}" height="{rnd(10, 26):.0f}" fill="#F2C879" opacity=".25"/>')
    ripples = ''.join(f'<rect x="{rnd(0, W):.0f}" y="{rnd(222, 315):.0f}" width="{rnd(20, 90):.0f}" height="1" '
                      f'fill="#D8CBE0" opacity=".18" style="animation:drift {rnd(6, 12):.0f}s ease-in-out {rnd(-12, 0):.1f}s infinite alternate"/>'
                      for _ in range(36))
    lanterns = ''.join(
        f'<g style="animation:up {p:.0f}s linear {-rnd(0, p):.1f}s infinite"><g style="animation:sway {rnd(3, 5):.1f}s ease-in-out {rnd(-5, 0):.1f}s infinite alternate">'
        f'<circle cx="{x:.0f}" cy="250" r="{9 * k:.1f}" fill="url(#glow)"/><rect x="{x - 2.5 * k:.1f}" y="{250 - 3.5 * k:.1f}" width="{5 * k:.1f}" height="{7 * k:.1f}" rx="{1.5 * k:.1f}" fill="#F7B867"/></g></g>'
        for x, k, p in ((rnd(60, W - 60), rnd(.6, 1.2), rnd(16, 26)) for _ in range(16)))
    flies = ''.join(f'<circle cx="{rnd(30, W - 30):.0f}" cy="{rnd(190, 300):.0f}" r="1.3" fill="#FFF3B0" '
                    f'style="animation:fly {rnd(5, 9):.1f}s ease-in-out {rnd(-9, 0):.1f}s infinite alternate,tw {rnd(1.2, 2.5):.1f}s ease-in-out {rnd(-2, 0):.1f}s infinite alternate"/>'
                    for _ in range(24))
    return ('<linearGradient id="sky" x2="0" y2="1"><stop offset="0" stop-color="#1C1A33"/><stop offset=".38" stop-color="#4A4570"/>'
            '<stop offset=".56" stop-color="#E0A9A2"/></linearGradient>'
            '<linearGradient id="lake" x2="0" y2="1"><stop offset="0" stop-color="#3B3658"/><stop offset="1" stop-color="#17152A"/></linearGradient>'
            '<radialGradient id="halo"><stop offset="0" stop-color="#FBEFD9" stop-opacity=".45"/><stop offset="1" stop-color="#FBEFD9" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="glow"><stop offset="0" stop-color="#FFC978" stop-opacity=".6"/><stop offset="1" stop-color="#FFC978" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="tail" x1="1" x2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>'
            f'<g id="scene"><rect width="{W}" height="{H}" fill="url(#sky)"/>{stars}{meteors}{moon}'
            + ridge(165, 14, '#6A5F86') + ridge(185, 10, '#4A4368') + ridge(200, 6, '#332E4F')
            + f'<rect y="208" width="{W}" height="{H - 208}" fill="url(#lake)"/>{glint}{ripples}{lights}{lanterns}{flies}</g>')


def grid(k):
    s = 48 >> k   # 畳み込みの窓を思わせる格子。段が進むほど細かくなる
    return (f'<pattern id="g{k}" width="{s}" height="{s}" patternUnits="userSpaceOnUse">'
            f'<path d="M{s} 0V{s}H0" fill="none" stroke="#E8EEF0" stroke-width=".6"/></pattern>')


def header():
    css = ".c{transform-box:fill-box;transform-origin:center}.v{transform-box:view-box;transform-origin:500px 160px}.b,.g{opacity:0}"
    css += ("@keyframes tw{to{opacity:.15}}@keyframes drift{to{transform:translateX(24px)}}"
            "@keyframes breathe{to{transform:scale(1.15)}}@keyframes glint{to{transform:scaleX(.55);opacity:.15}}"
            "@keyframes up{0%{transform:translateY(0);opacity:0}8%{opacity:1}80%{opacity:.9}100%{transform:translateY(-300px);opacity:0}}"
            "@keyframes sway{from{transform:translateX(-7px)}to{transform:translateX(7px)}}"
            "@keyframes fly{to{transform:translate(18px,-14px)}}"
            "@keyframes meteor{0%,88%{transform:translate(0,0);opacity:0}90%{opacity:1}100%{transform:translate(-160px,64px);opacity:0}}")
    for k in range(5):
        css += (f'@keyframes b{k}{{0%,{pct(OFF[k])}{{opacity:1}}{pct(OFF[k] + .7)},{pct(BACK[k])}{{opacity:0}}{pct(BACK[k] + .6)},100%{{opacity:1}}}}'
                f'.b{k}{{animation:b{k} {T}s ease-in-out infinite}}')
        on = OFF[k - 1] + .7 if k else .3
        css += (f'@keyframes g{k}{{0%,{pct(on - .3)}{{opacity:0}}{pct(on)},{pct(OFF[k])}{{opacity:1}}{pct(OFF[k] + .5)},100%{{opacity:0}}}}'
                f'.g{k}{{animation:g{k} {T}s ease-in-out infinite}}')
    steps = ''.join(f'{pct(OFF[k] - .01 if k else 0)}{{transform:scale({APER[k]})}}{pct(OFF[k] + .7)}{{transform:scale({APER[k + 1]})}}'
                    for k in range(5))
    css += (f'@keyframes ap{{{steps}{pct(BACK[4])}{{transform:scale(1)}}{pct(BACK[0] + .6)},100%{{transform:scale({APER[0]})}}}}'
            f'.ap{{animation:ap {T}s ease-in-out infinite}}'
            '@media (prefers-reduced-motion:reduce){*{animation:none!important}}')
    filters = ''.join(f'<filter id="f{k}" x="0" y="0" width="1" height="1"><feGaussianBlur stdDeviation="{b}" edgeMode="duplicate"/></filter>'
                      for k, b in enumerate(BLUR))
    defs = (f'<defs>{scene()}{filters}{"".join(grid(k) for k in range(5))}'
            '<radialGradient id="eye"><stop offset=".62" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>'
            f'<mask id="m" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}"/>'
            '<circle class="v ap" cx="500" cy="160" r="760" fill="url(#eye)"/></mask>'
            f'<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>')
    body = ('<g clip-path="url(#card)"><rect width="1000" height="320" fill="#15131F"/>'
            '<use href="#scene" filter="url(#f0)" opacity=".55"/><g mask="url(#m)"><use href="#scene"/>'
            + ''.join(f'<use class="b b{k}" href="#scene" filter="url(#f{k})"/>' for k in reversed(range(5)))
            + ''.join(f'<rect class="g g{k}" width="{W}" height="{H}" fill="url(#g{k})" style="mix-blend-mode:soft-light"/>' for k in range(5))
            + '</g></g>')
    label = 'ぼやけた夕暮れの湖畔が、畳み込みが一段ずつ外れるように中心から澄んで広がっていく'
    with open('header.svg', 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" '
                f'width="{W}" height="{H}" role="img" aria-label="{label}"><title>{label}</title><style>{css}</style>{defs}{body}</svg>\n')


def welcome():
    """来た人を迎える: 障子が左右に開いて灯りがこぼれ、道の灯籠が戸口から外へ順に灯り、光の粒が舞い出る。"""
    w, h, rnd = 1000, 180, random.uniform
    lattice = lambda x0: ''.join(f'<path d="M{x0 + 20 * i} 30v120" />' for i in (1, 2)) + ''.join(
        f'<path d="M{x0} {30 + 30 * j}h60" />' for j in (1, 2, 3))
    door = lambda x0, d: (f'<g style="animation:{d} 1.4s cubic-bezier(.23,1,.32,1) .6s backwards" class="{d}">'
                          f'<rect x="{x0}" y="30" width="60" height="120" fill="#F6E3C4" fill-opacity=".92"/>'
                          f'<g stroke="#5A4036" stroke-width="2">{lattice(x0)}</g>'
                          f'<rect x="{x0}" y="30" width="60" height="120" fill="none" stroke="#5A4036" stroke-width="4"/></g>')
    lamps = ''
    for i in range(6):
        for sgn in (-1, 1):
            x = 500 + sgn * (150 + i * 66)
            lamps += (f'<g style="animation:lit .8s ease-out {1.6 + i * .22:.2f}s backwards">'
                      f'<circle cx="{x}" cy="146" r="18" fill="url(#lg)" style="animation:flick {rnd(2, 3.5):.1f}s ease-in-out {rnd(-3, 0):.1f}s infinite alternate"/>'
                      f'<rect x="{x - 3}" y="140" width="6" height="10" rx="1.5" fill="#FFD9A0"/></g>'
                      f'<rect x="{x - 4}" y="150" width="8" height="12" fill="#2A2540"/>')
    sparks = ''.join(f'<circle cx="500" cy="95" r="{rnd(1.4, 3):.1f}" fill="#FFE2B0" '
                     f'style="--x:{rnd(-420, 420):.0f}px;--y:{rnd(-80, 70):.0f}px;animation:spark {rnd(4, 7):.1f}s ease-out {1.4 + rnd(0, 5):.1f}s infinite backwards"/>'
                     for _ in range(32))
    css = ("@keyframes dl{from{transform:translateX(60px)}}@keyframes dr{from{transform:translateX(-60px)}}"
           ".dl{transform:translateX(0)}.dr{transform:translateX(0)}"
           "@keyframes glow{from{opacity:0;transform:scaleX(.1)}}@keyframes breathe{to{opacity:.75}}"
           "@keyframes lit{from{opacity:.15}}@keyframes flick{to{opacity:.6}}"
           "@keyframes spark{0%{transform:translate(0,0) scale(.5);opacity:0}15%{opacity:1}100%{transform:translate(var(--x),var(--y)) scale(1.4);opacity:0}}"
           ".c{transform-box:fill-box;transform-origin:center}"
           "@media (prefers-reduced-motion:reduce){*{animation:none!important}}")
    body = ('<defs><radialGradient id="room"><stop offset="0" stop-color="#FFE7BD"/><stop offset="1" stop-color="#E8955A"/></radialGradient>'
            '<radialGradient id="aura"><stop offset="0" stop-color="#FFC978" stop-opacity=".5"/><stop offset="1" stop-color="#FFC978" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="lg"><stop offset="0" stop-color="#FFC978" stop-opacity=".7"/><stop offset="1" stop-color="#FFC978" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="spill" x2="0" y2="1"><stop offset="0" stop-color="#FFC978" stop-opacity=".45"/><stop offset="1" stop-color="#FFC978" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="dusk" x2="0" y2="1"><stop offset="0" stop-color="#1C1A33"/><stop offset="1" stop-color="#2E2A4C"/></linearGradient>'
            f'<clipPath id="wc"><rect width="{w}" height="{h}" rx="18"/></clipPath></defs>'
            f'<g clip-path="url(#wc)"><rect width="{w}" height="{h}" fill="url(#dusk)"/><rect y="150" width="{w}" height="30" fill="#211E37"/>'
            '<g class="c" style="animation:glow 1.6s ease-out .8s backwards"><ellipse cx="500" cy="95" rx="260" ry="90" fill="url(#aura)" class="c" style="animation:breathe 4s ease-in-out 2.4s infinite alternate"/>'
            '<polygon points="440,150 560,150 720,180 280,180" fill="url(#spill)"/></g>'
            '<rect x="440" y="30" width="120" height="120" fill="url(#room)"/>'
            f'{door(380, "dl")}{door(560, "dr")}'
            '<path d="M372 26h256" stroke="#5A4036" stroke-width="6" stroke-linecap="round"/>'
            f'{lamps}{sparks}</g>')
    label = '障子が開いて温かい灯りがこぼれ、道の灯籠が順に灯って迎え入れる'
    with open('welcome.svg', 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
                f'aria-label="{label}"><title>{label}</title><style>{css}</style>{body}</svg>\n')


header()
welcome()
