#!/usr/bin/env python3
"""プロフィール用の動く SVG を作る: python3 gen.py
ぼやけた世界から畳み込み(ぼかし)が一段ずつ外れ、視界が中心から広がっていく。"""
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
    stars = ''.join(f'<circle cx="{random.uniform(0, W):.0f}" cy="{random.uniform(0, 170):.0f}" r="{random.uniform(.6, 1.5):.1f}" '
                    f'fill="#E8EEF0" opacity="{random.uniform(.4, .9):.2f}" '
                    f'style="animation:tw {random.uniform(3, 6):.1f}s ease-in-out {random.uniform(-6, 0):.1f}s infinite alternate"/>'
                    for _ in range(70))
    lights = ''
    for _ in range(26):
        x, y, r = random.uniform(40, W - 40), random.uniform(204, 212), random.uniform(1, 2.2)
        lights += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#F2C879"/>'
                   f'<rect x="{x - r / 2:.1f}" y="{y + 6:.0f}" width="{r:.1f}" height="{random.uniform(10, 26):.0f}" fill="#F2C879" opacity=".25"/>')
    ripples = ''.join(f'<rect x="{random.uniform(0, W):.0f}" y="{random.uniform(222, 315):.0f}" width="{random.uniform(20, 90):.0f}" height="1" '
                      f'fill="#B9C8CF" opacity=".18" style="animation:drift {random.uniform(6, 12):.0f}s ease-in-out {random.uniform(-12, 0):.1f}s infinite alternate"/>'
                      for _ in range(36))
    return ('<linearGradient id="sky" x2="0" y2="1"><stop offset="0" stop-color="#1F2A36"/><stop offset=".42" stop-color="#5E7686"/>'
            '<stop offset=".56" stop-color="#C9B596"/></linearGradient>'
            '<linearGradient id="lake" x2="0" y2="1"><stop offset="0" stop-color="#34475A"/><stop offset="1" stop-color="#18222D"/></linearGradient>'
            f'<g id="scene"><rect width="{W}" height="{H}" fill="url(#sky)"/>{stars}'
            + ridge(165, 14, '#566C7A') + ridge(185, 10, '#3E5263') + ridge(200, 6, '#2C3D4E')
            + f'<rect y="208" width="{W}" height="{H - 208}" fill="url(#lake)"/>{ripples}{lights}</g>')


def grid(k):
    s = 48 >> k   # 畳み込みの窓を思わせる格子。段が進むほど細かくなる
    return (f'<pattern id="g{k}" width="{s}" height="{s}" patternUnits="userSpaceOnUse">'
            f'<path d="M{s} 0V{s}H0" fill="none" stroke="#E8EEF0" stroke-width=".6"/></pattern>')


def header():
    css = ".v{transform-box:view-box;transform-origin:500px 160px}.b,.g{opacity:0}"
    css += "@keyframes tw{to{opacity:.15}}@keyframes drift{to{transform:translateX(24px)}}"
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
    body = ('<g clip-path="url(#card)"><rect width="1000" height="320" fill="#141B22"/>'
            '<use href="#scene" filter="url(#f0)" opacity=".55"/><g mask="url(#m)"><use href="#scene"/>'
            + ''.join(f'<use class="b b{k}" href="#scene" filter="url(#f{k})"/>' for k in reversed(range(5)))
            + ''.join(f'<rect class="g g{k}" width="{W}" height="{H}" fill="url(#g{k})" style="mix-blend-mode:soft-light"/>' for k in range(5))
            + '</g></g>')
    label = 'ぼやけた夜の湖畔が、畳み込みが一段ずつ外れるように中心から澄んで広がっていく'
    with open('header.svg', 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" '
                f'width="{W}" height="{H}" role="img" aria-label="{label}"><title>{label}</title><style>{css}</style>{defs}{body}</svg>\n')


header()
