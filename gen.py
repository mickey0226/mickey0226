#!/usr/bin/env python3
"""プロフィール用の動く SVG を全部作る: python3 gen.py"""
import math
import random

random.seed(226)
PINK, YEL, CYAN, LEAF, VIO, INK = '#FF2E88', '#FFE600', '#00E5FF', '#7CFF4F', '#1A0638', '#2E0F5C'
BASE = (
    "text{font-family:'Arial Black','Hiragino Sans','Noto Sans JP','Yu Gothic',sans-serif;font-weight:900}"
    ".c{transform-box:fill-box;transform-origin:center}"
    ".ink{paint-order:stroke;stroke:#1A0638;stroke-linejoin:round}"
    "@keyframes hue{0%,100%{fill:#FF2E88}25%{fill:#FFE600}50%{fill:#00E5FF}75%{fill:#7CFF4F}}"
    "@keyframes spin{to{transform:rotate(360deg)}}"
    "@keyframes blink{50%{opacity:.15}}"
    "@keyframes jump{from{transform:translateY(8px) rotate(-6deg)}to{transform:translateY(-14px) rotate(6deg)}}"
    "@keyframes wig{from{transform:rotate(-3deg) scale(.96)}to{transform:rotate(3deg) scale(1.04)}}"
    "@keyframes pop{0%{transform:translateY(0);opacity:0}15%{opacity:1}100%{transform:translateY(-70px);opacity:0}}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
)


def svg(name, w, h, label, css, body):
    with open(name, 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
                f'role="img" aria-label="{label}"><title>{label}</title><style>{BASE}{css}</style>{body}</svg>\n')


def anim(a):
    return f'style="animation:{a}"'


def popups(n, x0, x1, y0, y1, size=22):
    return ''.join(
        f'<text class="c ink" x="{random.randint(x0, x1)}" y="{random.randint(y0, y1)}" font-size="{size}" '
        f'fill="{LEAF}" stroke-width="4" {anim(f"pop 2.4s ease-out {random.uniform(0, 2.4):.2f}s infinite")}>'
        f'+1🌳</text>' for _ in range(n))


def header():
    R = 800
    rays = ''.join(
        f'<path d="M0 0L{R*math.cos(math.radians(a)):.0f} {R*math.sin(math.radians(a)):.0f}'
        f'L{R*math.cos(math.radians(a+15)):.0f} {R*math.sin(math.radians(a+15)):.0f}Z"/>'
        for a in range(0, 360, 30))
    stars = ''.join(
        f'<text class="c" x="{random.randint(20, 980)}" y="{random.randint(30, 280)}" font-size="{random.randint(14, 30)}" '
        f'fill="{random.choice([YEL, CYAN, PINK, LEAF, "#fff"])}" '
        f'{anim(f"tw {random.uniform(.6, 1.6):.2f}s ease-in-out {random.uniform(0, 1):.2f}s infinite")}>'
        f'{random.choice("★✦●✿")}</text>' for _ in range(26))
    name = 'MICKEY0226'
    letters = ''.join(
        f'<g class="c" {anim(f"jump .7s ease-in-out {i*.07:.2f}s infinite alternate")}>'
        f'<text x="{500+(i-4.5)*72:.0f}" y="150" font-size="80" text-anchor="middle" fill="{CYAN}" opacity=".9" '
        f'{anim("gl .3s steps(1) infinite")}>{ch}</text>'
        f'<text class="ink" x="{500+(i-4.5)*72:.0f}" y="150" font-size="80" text-anchor="middle" stroke-width="10" '
        f'{anim(f"hue 1.2s linear {i*.1:.1f}s infinite")}>{ch}</text></g>'
        for i, ch in enumerate(name))
    msg = 'Tree Planting in Progress🌱🌱 植林、加速中!!!'
    sprouts = ''.join(
        f'<text class="c" x="{60+i*68}" y="290" font-size="34" text-anchor="middle" '
        f'{anim(f"grow 2.2s ease-in-out {random.uniform(0, 2.2):.2f}s infinite")}>{"🌱🌿🌳🌲🌸🍀"[i % 6]}</text>'
        for i in range(14))
    star = ' '.join(
        f'{(42 if k % 2 == 0 else 32)*math.cos(math.pi*k/16):.1f},{(42 if k % 2 == 0 else 32)*math.sin(math.pi*k/16):.1f}'
        for k in range(32))
    css = ("@keyframes tw{0%,100%{transform:scale(.4) rotate(0)}50%{transform:scale(1.4) rotate(180deg)}}"
           "@keyframes gl{0%,100%{transform:translate(5px,5px)}33%{transform:translate(-6px,3px)}66%{transform:translate(4px,-5px)}}"
           "@keyframes type{0%{transform:translateX(0)}70%,100%{transform:translateX(548px)}}"
           "@keyframes grow{0%{transform:scale(0) translateY(10px)}40%{transform:scale(1.4)}60%{transform:scale(1)}100%{transform:scale(0)}}"
           "@keyframes pulse{from{transform:scale(.85)}to{transform:scale(1.2)}}")
    body = (
        f'<clipPath id="h"><rect width="1000" height="300" rx="28"/></clipPath>'
        f'<clipPath id="p"><rect x="210" y="190" width="580" height="46" rx="23"/></clipPath>'
        f'<g clip-path="url(#h)"><rect width="1000" height="300" fill="{VIO}"/>'
        f'<g transform="translate(500 150)"><g class="c" fill="{PINK}" opacity=".22" {anim("spin 14s linear infinite")}>{rays}</g></g>'
        f'{stars}{letters}'
        f'<g class="c" {anim("wig 1.4s ease-in-out infinite alternate")}>'
        f'<rect x="210" y="190" width="580" height="46" rx="23" fill="{YEL}"/>'
        f'<text x="230" y="221" font-size="24" fill="{VIO}" textLength="540" lengthAdjust="spacingAndGlyphs">{msg}</text>'
        f'<g clip-path="url(#p)"><g {anim(f"type 4s steps({len(msg)}) infinite")}>'
        f'<rect x="228" y="190" width="600" height="46" fill="{YEL}"/>'
        f'<rect x="228" y="198" width="5" height="30" fill="{PINK}" {anim("blink .5s steps(1) infinite")}/></g></g></g>'
        f'{sprouts}{popups(6, 60, 940, 60, 200)}'
        f'<g transform="translate(938 52)"><g class="c" {anim("spin 6s linear infinite")}>'
        f'<polygon points="{star}" fill="{YEL}" stroke="{PINK}" stroke-width="4"/></g>'
        f'<text class="c" y="8" font-size="17" text-anchor="middle" fill="{PINK}" '
        f'{anim("pulse .45s ease-in-out infinite alternate")}>LV.∞</text></g>'
        f'<g transform="translate(62 52)"><circle class="c" r="36" fill="{PINK}" {anim("pulse .6s ease-in-out infinite alternate")}/>'
        f'<text y="7" font-size="17" text-anchor="middle" fill="#fff" {anim("blink .8s steps(1) infinite")}>植林中</text></g>'
        f'</g>')
    svg('header.svg', 1000, 300, 'MICKEY0226 — Tree Planting in Progress', css, body)


def ticker():
    a = ' 🌱 植林中 🌳 +1 TREE 🎉 COMBO×99 ☀️ 光合成MAX 🌲 森になる 🍀 '
    b = ' ｷﾀ━━━(ﾟ∀ﾟ)━━━!! 🌱 GROW GROW GROW 🌳 水やり完了 💧 根っこ∞ 🌸 '

    def band(txt, y, deg, bg, fg, extra):
        copies = ''.join(
            f'<text class="ink" x="{x}" y="{y+36}" font-size="28" fill="{fg}" stroke-width="5" textLength="1000" '
            f'lengthAdjust="spacingAndGlyphs">{txt}</text>' for x in (-1000, 0, 1000, 2000))
        return (f'<g transform="rotate({deg} 500 {y+25})"><rect x="-100" y="{y}" width="1200" height="50" fill="{bg}"/>'
                f'<g {anim(f"slide 7s linear infinite{extra}")}>{copies}</g></g>')
    css = "@keyframes slide{to{transform:translateX(-1000px)}}"
    svg('ticker.svg', 1000, 170, '植林中 +1 TREE COMBO', css,
        band(a, 32, -3, PINK, '#fff', '') + band(b, 88, 3, YEL, CYAN, ' reverse'))


def slot():
    pool = list('🌱🌲🍀🌸🍄🌴💎🍒') + ['7️⃣']
    T, stop = 36, (55, 65, 75)
    css = ("@keyframes lever{0%,100%{transform:rotate(-20deg)}50%{transform:rotate(25deg)}}"
           ".lv{transform-box:fill-box;transform-origin:50% 100%}"
           "@keyframes jp{0%,76%{opacity:0}78%,86%,94%{opacity:1;transform:scale(1.15)}82%,90%,98%{opacity:.3;transform:scale(1)}100%{opacity:0}}"
           "@keyframes sp{0%,74%{opacity:1}76%,100%{opacity:0}}"
           "@keyframes burst{0%,76%{transform:translate(0,0) scale(0);opacity:0}80%{opacity:1}100%{transform:translate(var(--x),var(--y)) scale(1.5);opacity:0}}")
    reels = ''
    for r, x in enumerate((245, 420, 595)):
        items = [random.choice(pool) for _ in range(T + 4)]
        items[T] = '🌳'
        css += (f"@keyframes r{r}{{0%{{transform:translateY(0);animation-timing-function:cubic-bezier(.3,0,.25,1)}}"
                f"{stop[r]}%,100%{{transform:translateY({-T*70}px)}}}}")
        col = ''.join(f'<text x="{x+80}" y="{153+i*70}" font-size="56" text-anchor="middle">{e}</text>'
                      for i, e in enumerate(items))
        reels += (f'<clipPath id="w{r}"><rect x="{x}" y="78" width="160" height="110" rx="14"/></clipPath>'
                  f'<rect x="{x}" y="78" width="160" height="110" rx="14" fill="#fff"/>'
                  f'<g clip-path="url(#w{r})"><g {anim(f"r{r} 3.6s infinite")}>{col}</g></g>')
    lights = [(x, y) for x in range(50, 951, 50) for y in (10, 270)] + [(x, y) for x in (10, 990) for y in range(50, 231, 45)]
    bulbs = ''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="{YEL}" {anim(f"blink .5s steps(1) {(i % 2)*.25}s infinite")}/>'
                    for i, (x, y) in enumerate(lights))
    burst = ''.join(
        f'<text class="c" x="500" y="150" font-size="34" text-anchor="middle" '
        f'style="--x:{380*math.cos(t):.0f}px;--y:{150*math.sin(t):.0f}px;animation:burst 3.6s ease-out infinite">'
        f'{random.choice("🌳🪙✨🌲")}</text>' for t in (2*math.pi*k/16 for k in range(16)))
    body = (
        f'<rect width="1000" height="280" rx="30" fill="{PINK}"/><rect x="20" y="20" width="960" height="240" rx="22" fill="{VIO}"/>'
        f'{bulbs}'
        f'<text class="c ink" x="500" y="60" font-size="34" text-anchor="middle" stroke-width="7" '
        f'style="animation:hue 1s linear infinite,wig .5s ease-in-out infinite alternate">GROW-O-MATIC</text>'
        f'{reels}'
        f'<line x1="235" y1="133" x2="765" y2="133" stroke="{PINK}" stroke-width="4" opacity=".8" {anim("blink .3s steps(1) infinite")}/>'
        f'<text class="c" x="130" y="160" font-size="80" text-anchor="middle" {anim("spin 1s linear infinite")}>🌱</text>'
        f'<g class="lv" {anim("lever 1.2s ease-in-out infinite")}><rect x="864" y="90" width="12" height="110" rx="6" fill="#ccc"/>'
        f'<circle cx="870" cy="88" r="20" fill="{PINK}" stroke="#fff" stroke-width="4"/></g>'
        f'<text class="ink" x="500" y="236" font-size="30" text-anchor="middle" fill="{CYAN}" stroke-width="6" '
        f'{anim("sp 3.6s infinite")}><tspan {anim("blink .25s steps(1) infinite")}>SPINNING…</tspan></text>'
        f'<text class="c ink" x="500" y="240" font-size="40" text-anchor="middle" fill="{YEL}" stroke-width="8" '
        f'{anim("jp 3.6s infinite")}>JACKPOT!! 森 森 森</text>'
        f'{burst}')
    svg('slot.svg', 1000, 280, 'GROW-O-MATIC JACKPOT 森森森', css, body)


def stats():
    css = ("@keyframes ants{to{stroke-dashoffset:-60}}"
           ".bar{transform-box:fill-box;transform-origin:0 50%}"
           "@keyframes pump{from{transform:scaleX(.82)}to{transform:scaleX(1.04)}}"
           "@keyframes odo{to{transform:translateY(-440px)}}")
    rows = [('光合成', 490, 'hue 1s linear infinite,pump .35s ease-in-out infinite alternate', None, '9999%'),
            ('水やり', 440, 'pump .7s ease-in-out infinite alternate', CYAN, '120%'),
            ('根っこ', 440, 'pump 1.1s ease-in-out infinite alternate', LEAF, '∞'),
            ('集中力', 14, 'blink .15s steps(1) infinite', PINK, '3%')]
    body = (f'<rect width="1000" height="270" rx="28" fill="{VIO}"/>'
            f'<rect x="6" y="6" width="988" height="258" rx="24" fill="none" stroke="{PINK}" stroke-width="6" '
            f'stroke-dasharray="18 12" {anim("ants .8s linear infinite")}/>')
    for i, (lab, w, a, col, val) in enumerate(rows):
        y = 60 + i*55
        body += (f'<text x="40" y="{y+10}" font-size="26" fill="#fff">{lab}</text>'
                 f'<rect x="150" y="{y-13}" width="440" height="26" rx="13" fill="{INK}"/>'
                 f'<rect class="bar" x="150" y="{y-13}" width="{w}" height="26" rx="13" fill="{col or PINK}" {anim(a)}/>'
                 f'<text class="ink" x="655" y="{y+11}" font-size="30" stroke-width="6" '
                 f'{anim(f"hue .8s linear {i*.2:.1f}s infinite")}>{val}</text>')
    cx, cy = 875, 125
    body += (f'<circle cx="{cx}" cy="{cy}" r="80" fill="none" stroke="{INK}" stroke-width="16"/>'
             f'<circle class="c" cx="{cx}" cy="{cy}" r="80" fill="none" stroke="{PINK}" stroke-width="16" '
             f'stroke-dasharray="120 383" {anim("spin 1.2s linear infinite")}/>'
             f'<circle class="c" cx="{cx}" cy="{cy}" r="80" fill="none" stroke="{YEL}" stroke-width="16" '
             f'stroke-dasharray="60 443" {anim("spin .8s linear infinite reverse")}/>'
             f'<clipPath id="o"><rect x="{cx-56}" y="{cy-22}" width="112" height="44"/></clipPath><g clip-path="url(#o)">')
    for d, dur in enumerate(('300s', '30s', '3s', '.3s')):
        col = ''.join(f'<text x="{cx-41+d*27}" y="{cy+14+k*44}" font-size="40" text-anchor="middle" fill="#fff">{k}</text>'
                      for k in range(10))
        body += f'<g {anim(f"odo {dur} steps(10) infinite")}>{col}</g>'
    body += (f'</g><text x="{cx}" y="{cy+48}" font-size="16" text-anchor="middle" fill="{YEL}">植えた木</text>'
             )
    svg('stats.svg', 1000, 270, '光合成 9999% / 植えた木カウンター', css, body)


def footer():
    css = "@keyframes fall{from{transform:translateY(-40px) rotate(0)}to{transform:translateY(270px) rotate(var(--r))}}"
    bits = ''
    for _ in range(90):
        x, d = random.randint(0, 1000), random.uniform(1.8, 3.6)
        a = f"--r:{random.choice((-1, 1))*random.randint(180, 720)}deg;animation:fall {d:.2f}s linear {-random.uniform(0, d):.2f}s infinite"
        if random.random() < .25:
            bits += f'<text class="c" x="{x}" y="0" font-size="22" style="{a}">{random.choice("🍃🌸🍀")}</text>'
        else:
            bits += (f'<rect class="c" x="{x}" y="-10" width="{random.randint(8, 14)}" height="{random.randint(5, 9)}" '
                     f'fill="{random.choice([PINK, YEL, CYAN, LEAF])}" style="{a}"/>')
    chars = ['ま', 'た', '来', 'て', 'ね', '!!']
    wave = ''.join(
        f'<text class="c ink" x="{500+(i-2.5)*78:.0f}" y="112" font-size="64" text-anchor="middle" stroke-width="10" '
        f'style="animation:jump .6s ease-in-out {i*.08:.2f}s infinite alternate,hue 1.2s linear {i*.15:.2f}s infinite">{ch}</text>'
        for i, ch in enumerate(chars))
    body = (f'{bits}{wave}'
            f'<text class="c ink" x="500" y="178" font-size="30" text-anchor="middle" fill="{YEL}" stroke-width="7" '
            f'{anim("wig .5s ease-in-out infinite alternate")}>see you in the forest 🌳</text>'
            + ''.join(f'<text class="c" x="{x}" y="130" font-size="64" text-anchor="middle" '
                      f'style="animation:wig .3s ease-in-out {k*.15}s infinite alternate">🎉</text>'
                      for k, x in enumerate((110, 890))))
    svg('footer.svg', 1000, 230, 'また来てね!! see you in the forest', css, body)


for f in (header, ticker, slot, stats, footer):
    f()
