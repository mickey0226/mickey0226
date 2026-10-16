#!/usr/bin/env python3
"""プロフィール用の動く SVG を全部作る: python3 gen.py"""
import math
import random

random.seed(226)
PINK, YEL, CYAN, LEAF, VIO, INK = '#FF2E88', '#FFE600', '#00E5FF', '#7CFF4F', '#1A0638', '#2E0F5C'
GOLD, RED, PUR = '#FFC400', '#FF1A1A', '#B04DFF'
RB = [PINK, YEL, LEAF, CYAN, PUR]
BASE = (
    "text{font-family:'Arial Black','Hiragino Sans','Noto Sans JP','Yu Gothic',sans-serif;font-weight:900}"
    # ダサさの決め手は Windows の創英角ポップ体と行書体。無い環境では普通の太字に落ちる
    ".pop{font-family:'HGP創英角ﾎﾟｯﾌﾟ体','HG創英角ﾎﾟｯﾌﾟ体','HGP創英角ポップ体','Arial Black','Hiragino Sans',sans-serif}"
    ".brush{font-family:'HGP行書体','HG行書体','HGS行書体','YuMincho','Hiragino Mincho ProN','Noto Serif JP',serif}"
    ".c{transform-box:fill-box;transform-origin:center}"
    ".ink{paint-order:stroke;stroke:#1A0638;stroke-linejoin:round}"
    "@keyframes hue{0%,100%{fill:#FF2E88}25%{fill:#FFE600}50%{fill:#00E5FF}75%{fill:#7CFF4F}}"
    "@keyframes rb{0%,100%{stop-color:#FF2E88}20%{stop-color:#FFE600}40%{stop-color:#7CFF4F}60%{stop-color:#00E5FF}80%{stop-color:#B04DFF}}"
    "@keyframes spin{to{transform:rotate(360deg)}}"
    "@keyframes blink{50%{opacity:.15}}"
    "@keyframes jump{from{transform:translateY(8px) rotate(-6deg)}to{transform:translateY(-14px) rotate(6deg)}}"
    "@keyframes wig{from{transform:rotate(-3deg) scale(.96)}to{transform:rotate(3deg) scale(1.04)}}"
    "@keyframes pulse{from{transform:scale(.85)}to{transform:scale(1.2)}}"
    "@keyframes shake{0%,100%{transform:translate(0,0)}25%{transform:translate(-4px,2px)}50%{transform:translate(3px,-3px)}75%{transform:translate(-2px,-2px)}}"
    "@keyframes pop{0%{transform:translateY(0) scale(.5);opacity:0}15%{transform:translateY(-10px) scale(1.3);opacity:1}100%{transform:translateY(-70px) scale(1);opacity:0}}"
    # 画面全体の点滅は 1 秒に 3 回未満に抑える(光過敏の目安)
    "@keyframes flash{0%,100%{opacity:0}10%{opacity:.25}}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
)


def svg(name, w, h, label, css, body):
    with open(name, 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
                f'role="img" aria-label="{label}"><title>{label}</title><style>{BASE}{css}</style>{body}</svg>\n')


def anim(a):
    return f'style="animation:{a}"'


def rainbow(gid, speed=1):
    """色が流れる虹のグラデーション。動きを止めた環境では静止した虹になる。"""
    return (f'<linearGradient id="{gid}">' + ''.join(
        f'<stop offset="{k/4}" stop-color="{RB[k]}" {anim(f"rb {speed}s linear {-k*speed/5:.2f}s infinite")}/>'
        for k in range(5)) + '</linearGradient>')


def popups(n, x0, x1, y0, y1, texts=('+1🌳',), size=22):
    return ''.join(
        f'<text class="c ink pop" x="{random.randint(x0, x1)}" y="{random.randint(y0, y1)}" font-size="{size}" '
        f'stroke-width="4" style="animation:pop 1.8s ease-out {random.uniform(0, 1.8):.2f}s infinite,hue .6s linear infinite">'
        f'{random.choice(texts)}</text>' for _ in range(n))


def bulbs(w, h, color=GOLD, speed=.3):
    pts = ([(x, y) for x in range(50, w - 49, 50) for y in (10, h - 10)]
           + [(x, y) for x in (10, w - 10) for y in range(50, h - 49, 45)])
    return ''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}" {anim(f"blink {speed}s steps(1) {(i % 3)*speed/3:.2f}s infinite")}/>'
                   for i, (x, y) in enumerate(pts))


def kf(name, pts):
    """(%, 縦の移動量, 次の区間の速度曲線) の列からリールの keyframes を作る。"""
    return f'@keyframes {name}{{' + ''.join(
        f'{p}%{{transform:translateY({y}px)' + (f';animation-timing-function:{e}' if e else '') + '}'
        for p, y, e in pts) + '}'


def header():
    R = 800
    rays = ''.join(
        f'<path d="M0 0L{R*math.cos(math.radians(a)):.0f} {R*math.sin(math.radians(a)):.0f}'
        f'L{R*math.cos(math.radians(a+15)):.0f} {R*math.sin(math.radians(a+15)):.0f}Z" '
        f'{anim(f"hue 1s linear {-a/360:.2f}s infinite")}/>'
        for a in range(0, 360, 30))
    stars = ''.join(
        f'<text class="c" x="{random.randint(20, 980)}" y="{random.randint(30, 280)}" font-size="{random.randint(14, 34)}" '
        f'fill="{random.choice([YEL, CYAN, PINK, LEAF, GOLD, "#fff"])}" '
        f'{anim(f"tw {random.uniform(.4, 1):.2f}s ease-in-out {random.uniform(0, 1):.2f}s infinite")}>'
        f'{random.choice("★✦●✿")}</text>' for _ in range(40))
    letters = ''.join(
        f'<g class="c" {anim(f"jump .45s ease-in-out {i*.05:.2f}s infinite alternate")}>'
        f'<text x="{500+(i-4.5)*72:.0f}" y="150" font-size="80" text-anchor="middle" fill="{CYAN}" opacity=".9" '
        f'{anim("gl .2s steps(1) infinite")}>{ch}</text>'
        f'<text class="ink" x="{500+(i-4.5)*72:.0f}" y="150" font-size="80" text-anchor="middle" stroke-width="10" '
        f'{anim(f"hue .6s linear {i*.06:.2f}s infinite")}>{ch}</text></g>'
        for i, ch in enumerate('MICKEY0226'))
    msg = '確変中!!! Tree Planting in Progress🌱🌱 植林、大当り連チャン中!!!'
    sprouts = ''.join(
        f'<text class="c" x="{60+i*68}" y="290" font-size="34" text-anchor="middle" '
        f'{anim(f"grow 1.4s ease-in-out {random.uniform(0, 1.4):.2f}s infinite")}>{"🌱🌿🌳🌲🌸🍀"[i % 6]}</text>'
        for i in range(14))
    star = ' '.join(
        f'{(42 if k % 2 == 0 else 32)*math.cos(math.pi*k/16):.1f},{(42 if k % 2 == 0 else 32)*math.sin(math.pi*k/16):.1f}'
        for k in range(32))
    css = ("@keyframes tw{0%,100%{transform:scale(.4) rotate(0)}50%{transform:scale(1.5) rotate(180deg)}}"
           "@keyframes gl{0%,100%{transform:translate(5px,5px)}33%{transform:translate(-6px,3px)}66%{transform:translate(4px,-5px)}}"
           "@keyframes type{0%{transform:translateX(0)}70%,100%{transform:translateX(548px)}}"
           "@keyframes grow{0%{transform:scale(0) translateY(10px)}40%{transform:scale(1.4)}60%{transform:scale(1)}100%{transform:scale(0)}}"
           "@keyframes cut{0%,55%{transform:scale(4) rotate(-12deg);opacity:0}62%{transform:scale(.9) rotate(-6deg);opacity:1}"
           "66%{transform:scale(1.12) rotate(-6deg)}70%,88%{transform:scale(1) rotate(-6deg);opacity:1}100%{transform:scale(.2) rotate(10deg);opacity:0}}"
           "@keyframes band{0%,57%{transform:scaleY(0)}62%,90%{transform:scaleY(1)}96%,100%{transform:scaleY(0)}}")
    body = (
        f'<defs>{rainbow("rh", .8)}</defs>'
        f'<clipPath id="h"><rect width="1000" height="300" rx="28"/></clipPath>'
        f'<clipPath id="p"><rect x="210" y="190" width="580" height="46" rx="23"/></clipPath>'
        f'<g clip-path="url(#h)"><rect width="1000" height="300" fill="{VIO}"/>'
        f'<g transform="translate(500 150)"><g class="c" opacity=".3" {anim("spin 4s linear infinite")}>{rays}</g></g>'
        f'{stars}<g {anim("shake .25s linear infinite")}>{letters}</g>'
        f'<g class="c" {anim("wig .7s ease-in-out infinite alternate")}>'
        f'<rect x="210" y="190" width="580" height="46" rx="23" fill="{YEL}" stroke="url(#rh)" stroke-width="5"/>'
        f'<text x="230" y="221" font-size="22" fill="{VIO}" textLength="540" lengthAdjust="spacingAndGlyphs">{msg}</text>'
        f'<g clip-path="url(#p)"><g {anim(f"type 3s steps({len(msg)}) infinite")}>'
        f'<rect x="228" y="190" width="600" height="46" fill="{YEL}"/>'
        f'<rect x="228" y="198" width="5" height="30" fill="{PINK}" {anim("blink .3s steps(1) infinite")}/></g></g></g>'
        f'{sprouts}{popups(8, 60, 940, 60, 200, ("+1🌳", "+3000発", "キュイン!!", "激アツ"))}'
        f'<g transform="translate(938 52)"><g class="c" {anim("spin 2s linear infinite")}>'
        f'<polygon points="{star}" fill="{GOLD}" stroke="{RED}" stroke-width="4"/></g>'
        f'<text class="c brush" y="7" font-size="19" text-anchor="middle" fill="{RED}" '
        f'{anim("pulse .25s ease-in-out infinite alternate")}>激アツ</text></g>'
        f'<g transform="translate(62 52)"><circle class="c" r="36" fill="url(#rh)" {anim("pulse .35s ease-in-out infinite alternate")}/>'
        f'<text y="7" font-size="17" text-anchor="middle" fill="#fff" class="ink" stroke-width="4" {anim("blink .4s steps(1) infinite")}>確変中</text></g>'
        # 4 秒ごとに「確変突入!!」のカットインが叩き込まれる
        f'<rect class="c" x="0" y="95" width="1000" height="110" fill="{VIO}" stroke="url(#rh)" stroke-width="8" opacity=".92" '
        f'{anim("band 4s infinite")}/>'
        f'<text class="c ink brush" x="500" y="186" font-size="104" text-anchor="middle" fill="url(#rh)" stroke-width="14" '
        f'{anim("cut 4s infinite")}>確変突入!!</text>'
        f'<rect width="1000" height="300" fill="{GOLD}" {anim("flash .5s infinite")}/>'
        f'</g>')
    svg('header.svg', 1000, 300, 'MICKEY0226 確変突入!! Tree Planting in Progress', css, body)


def ticker():
    a = ' 🎰 確変突入 ★ 激アツ ★ 大当り 🌳 連チャン継続中 ★ FEVER!! ★ 植林 ∞ ★ '
    b = ' ｷﾀ━━━(ﾟ∀ﾟ)━━━!! 🌱 キュイーン!! 💥 V入賞 🌲 出玉+99999 💰 ST 100回 🍀 '
    c = ' 🌈 虹保留 ★ 金保留 ★ 赤保留 ★ 期待度MAX ★ 🌳🌳🌳 777 🌳🌳🌳 ★ '

    def band(txt, y, deg, bg, fg, a):
        copies = ''.join(
            f'<text class="ink pop" x="{x}" y="{y+36}" font-size="28" fill="{fg}" stroke-width="5" textLength="1000" '
            f'lengthAdjust="spacingAndGlyphs">{txt}</text>' for x in (-1000, 0, 1000, 2000))
        return (f'<g transform="rotate({deg} 500 {y+25})"><rect x="-100" y="{y}" width="1200" height="50" fill="{bg}"/>'
                f'<g {anim(a)}>{copies}</g></g>')
    css = "@keyframes slide{to{transform:translateX(-1000px)}}"
    svg('ticker.svg', 1000, 230, '確変突入 激アツ 大当り 連チャン継続中', css,
        f'<defs>{rainbow("rt", 1.5)}</defs>'
        + band(a, 22, -3, PINK, '#fff', 'slide 4s linear infinite')
        + band(b, 88, 2, 'url(#rt)', '#fff', 'slide 3s linear infinite reverse')
        + band(c, 154, -2, YEL, PINK, 'slide 5s linear infinite'))


def slot():
    """10 秒で 2 回転。1 回目は中リールが 7 を 1 コマ通り過ぎて外れ、2 回目で 777 の大当り。"""
    D, T, W = 90, 30, 10
    E1, E2, E3 = 'cubic-bezier(.3,0,.25,1)', 'cubic-bezier(.3,0,.7,1)', 'cubic-bezier(.1,.6,.3,1)'
    color = dict(zip('12345689', (CYAN, LEAF, PINK, PUR, CYAN, LEAF, PINK, PUR)))
    css = ("@keyframes lever{0%,100%{transform:rotate(-20deg)}50%{transform:rotate(25deg)}}"
           ".lv{transform-box:fill-box;transform-origin:50% 100%}"
           "@keyframes spinning{0%,21%{opacity:1}22.5%,49%{opacity:0}50%,71%{opacity:1}72.5%,100%{opacity:0}}"
           "@keyframes reach{0%,22%{opacity:0}22.5%,39.5%{opacity:1}40%,72%{opacity:0}72.5%,89.5%{opacity:1}90%,100%{opacity:0}}"
           "@keyframes miss{0%,39.5%{opacity:0}40%,49.5%{opacity:1}50%,100%{opacity:0}}"
           "@keyframes jp{0%,89.5%{opacity:0}91%,95%,99%{opacity:1;transform:scale(1.15)}93%,97%{opacity:.4;transform:scale(1)}100%{opacity:0}}"
           "@keyframes win{0%,90%{opacity:0}92%{opacity:.35}94%{opacity:0}96%{opacity:.35}98%,100%{opacity:0}}"
           "@keyframes hold{0%{fill:#2D7BFF}25%{fill:#7CFF4F}50%{fill:#FF1A1A}75%{fill:#FFC400}}"
           "@keyframes burst{0%,90%{transform:translate(0,0) scale(0);opacity:0}92%{opacity:1}100%{transform:translate(var(--x),var(--y)) scale(1.6);opacity:0}}"
           + kf('r0', [(0, 0, E1), (17.5, -T*D, ''), (50, -T*D, ''), (50.01, 0, E1), (67.5, -T*D, ''), (100, -T*D, '')])
           + kf('r2', [(0, 0, E1), (22.5, -T*D, ''), (50, -T*D, ''), (50.01, 0, E1), (72.5, -T*D, ''), (100, -T*D, '')])
           + kf('r1', [(0, 0, E2), (22.5, -(T-4)*D, E3), (40, -(T+1)*D, ''), (50, -(T+1)*D, ''),
                       (50.01, 0, E2), (72.5, -(T-4)*D, E3), (90, -T*D, ''), (100, -T*D, '')]))
    reels = ''
    for r, x in enumerate((245, 420, 595)):
        items = [random.choice('12345689') for _ in range(T + 3)]
        items[T], items[T+1] = '7', '8'
        col = ''.join(
            f'<text x="{x+80}" y="{167+i*D}" font-size="76" text-anchor="middle" '
            + (f'fill="{GOLD}" stroke="{RED}" stroke-width="5" paint-order="stroke">7' if e == '7' else f'fill="{color[e]}">{e}')
            + '</text>' for i, e in enumerate(items))
        reels += (f'<clipPath id="w{r}"><rect x="{x}" y="80" width="160" height="120" rx="14"/></clipPath>'
                  f'<rect x="{x}" y="80" width="160" height="120" rx="14" fill="#000" stroke="{GOLD}" stroke-width="4"/>'
                  f'<g clip-path="url(#w{r})"><g {anim(f"r{r} {W}s infinite")}>{col}</g></g>')
    holds = ''.join(f'<circle cx="130" cy="{110+i*36}" r="14" fill="#2D7BFF" {anim(f"hold 1.6s steps(1) {-i*.4:.1f}s infinite")}/>'
                    for i in range(3))
    burst = ''.join(
        f'<text class="c" x="500" y="155" font-size="36" text-anchor="middle" '
        f'style="--x:{400*math.cos(t):.0f}px;--y:{150*math.sin(t):.0f}px;animation:burst {W}s ease-out infinite">'
        f'{random.choice(["🌳", "🪙", "✨", "7"])}</text>' for t in (2*math.pi*k/20 for k in range(20)))
    body = (
        f'<defs>{rainbow("rs", .7)}</defs>'
        f'<rect width="1000" height="300" rx="30" fill="url(#rs)"/><rect x="20" y="20" width="960" height="260" rx="22" fill="{VIO}"/>'
        f'{bulbs(1000, 300)}'
        f'<text class="c ink brush" x="500" y="62" font-size="34" text-anchor="middle" stroke-width="7" '
        f'style="animation:hue .5s linear infinite,wig .3s ease-in-out infinite alternate">CR植林物語 〜確変の森〜</text>'
        f'{reels}'
        f'<line x1="235" y1="140" x2="765" y2="140" stroke="{RED}" stroke-width="4" opacity=".8" {anim("blink .2s steps(1) infinite")}/>'
        f'<text x="130" y="92" font-size="18" text-anchor="middle" fill="#fff">保留</text>{holds}'
        f'<circle class="c" cx="130" cy="218" r="17" fill="url(#rs)" {anim("pulse .3s ease-in-out infinite alternate")}/>'
        f'<g class="lv" {anim("lever .8s ease-in-out infinite")}><rect x="864" y="100" width="12" height="110" rx="6" fill="#ccc"/>'
        f'<circle cx="870" cy="98" r="20" fill="{RED}" stroke="{GOLD}" stroke-width="4"/></g>'
        f'<text class="ink" x="500" y="258" font-size="30" text-anchor="middle" fill="{CYAN}" stroke-width="6" '
        f'{anim(f"spinning {W}s infinite")}><tspan {anim("blink .25s steps(1) infinite")}>回転中…</tspan></text>'
        f'<text class="c pop" x="500" y="262" font-size="44" text-anchor="middle" fill="{RED}" stroke="{GOLD}" stroke-width="6" '
        f'paint-order="stroke" {anim(f"reach {W}s infinite")}>リーチ!!</text>'
        f'<g {anim(f"miss {W}s infinite")}><text class="c ink pop" x="500" y="262" font-size="40" text-anchor="middle" fill="#9AA0B4" '
        f'stroke-width="7" {anim("shake .15s linear infinite")}>7 が 1 コマ通過…惜しい!!</text></g>'
        f'<text class="c ink brush" x="500" y="266" font-size="46" text-anchor="middle" fill="url(#rs)" stroke-width="9" '
        f'{anim(f"jp {W}s infinite")}>大当り!! 確変突入!!</text>'
        f'<rect x="20" y="20" width="960" height="260" rx="22" fill="{GOLD}" {anim(f"win {W}s infinite")}/>'
        f'{burst}')
    svg('slot.svg', 1000, 300, 'CR植林物語 リーチ!! 外れのあと 777 大当り 確変突入', css, body)


def board():
    """玉が釘に弾かれながら落ち、風車が回り、V が光る盤面。"""
    pins = ''.join(f'<circle cx="{x + (15 if r % 2 else 0)}" cy="{40 + r*26}" r="2.5" fill="#C9C9D9"/>'
                   for r in range(10) for x in range(40, 961, 30) if abs(x - 500) > 70 or r < 2)
    balls = ''
    for _ in range(45):
        d = random.uniform(1.4, 2.6)
        v = ';'.join(f'--{k}:{random.randint(-45, 45)}px' for k in 'abcd')
        balls += (f'<circle cx="{random.randint(60, 940)}" cy="10" r="7" fill="url(#ball)" '
                  f'style="{v};animation:drop {d:.2f}s ease-in {-random.uniform(0, d):.2f}s infinite"/>')

    def windmill(x, y, a):
        blades = ''.join(f'<rect x="-4" y="-34" width="8" height="30" rx="4" fill="{GOLD}" transform="rotate({k*90})"/>' for k in range(4))
        return f'<g transform="translate({x} {y})"><g class="c" {anim(a)}>{blades}<circle r="8" fill="{RED}"/></g></g>'
    css = ("@keyframes drop{0%{transform:translate(0,0)}25%{transform:translate(var(--a),75px)}"
           "50%{transform:translate(var(--b),150px)}75%{transform:translate(var(--c),225px)}100%{transform:translate(var(--d),310px)}}")
    body = (
        f'<defs>{rainbow("rv", .6)}<radialGradient id="ball" cx=".35" cy=".35"><stop offset="0" stop-color="#fff"/>'
        f'<stop offset=".5" stop-color="#B8BCC8"/><stop offset="1" stop-color="#4A4E5A"/></radialGradient></defs>'
        f'<rect width="1000" height="320" rx="30" fill="{GOLD}"/><rect x="20" y="20" width="960" height="280" rx="22" fill="{VIO}"/>'
        f'{bulbs(1000, 320, RED, .2)}{pins}'
        f'{windmill(180, 170, "spin .5s linear infinite")}{windmill(820, 170, "spin .4s linear infinite reverse")}'
        f'<circle class="c" cx="500" cy="130" r="38" fill="url(#rv)" stroke="#fff" stroke-width="4" {anim("pulse .3s ease-in-out infinite alternate")}/>'
        f'<text class="c ink" x="500" y="147" font-size="48" text-anchor="middle" fill="#fff" stroke-width="6" '
        f'{anim("pulse .3s ease-in-out infinite alternate")}>V</text>'
        f'<path d="M455 235h90l-15 40h-60z" fill="{GOLD}" stroke="{RED}" stroke-width="4"/>'
        f'<text x="500" y="262" font-size="16" text-anchor="middle" fill="{RED}">START</text>'
        f'{balls}'
        f'{popups(7, 120, 880, 70, 260, ("キュイーン!!", "V入賞!!", "+15R", "激アツ!!", "保留変化!!"), 26)}')
    svg('board.svg', 1000, 320, 'パチンコ盤面 V入賞!! キュイーン!!', css, body)


def stats():
    css = ("@keyframes ants{to{stroke-dashoffset:-60}}"
           ".bar{transform-box:fill-box;transform-origin:0 50%}"
           "@keyframes pump{from{transform:scaleX(.82)}to{transform:scaleX(1.04)}}"
           "@keyframes odo{to{transform:translateY(-440px)}}")
    rows = [('期待度', 490, 'url(#rd)', 'pump .25s ease-in-out infinite alternate', '9999%'),
            ('確変', 440, GOLD, 'pump .5s ease-in-out infinite alternate', '継続中'),
            ('連チャン', 440, LEAF, 'pump .8s ease-in-out infinite alternate', '∞'),
            ('集中力', 14, PINK, 'blink .15s steps(1) infinite', '3%')]
    body = (f'<defs>{rainbow("rd", .6)}</defs><rect width="1000" height="270" rx="28" fill="{VIO}"/>'
            f'<rect x="6" y="6" width="988" height="258" rx="24" fill="none" stroke="{GOLD}" stroke-width="6" '
            f'stroke-dasharray="18 12" {anim("ants .4s linear infinite")}/>')
    for i, (lab, w, col, a, val) in enumerate(rows):
        y = 60 + i*55
        body += (f'<text x="36" y="{y+9}" font-size="24" fill="#fff">{lab}</text>'
                 f'<rect x="150" y="{y-13}" width="440" height="26" rx="13" fill="{INK}"/>'
                 f'<rect class="bar" x="150" y="{y-13}" width="{w}" height="26" rx="13" fill="{col}" {anim(a)}/>'
                 f'<text class="c ink pop" x="655" y="{y+11}" font-size="30" stroke-width="6" '
                 f'style="animation:hue .4s linear {i*.1:.1f}s infinite,shake .2s linear infinite">{val}</text>')
    cx, cy = 875, 125
    body += (f'<circle cx="{cx}" cy="{cy}" r="80" fill="none" stroke="{INK}" stroke-width="16"/>'
             f'<circle class="c" cx="{cx}" cy="{cy}" r="80" fill="none" stroke="url(#rd)" stroke-width="16" '
             f'stroke-dasharray="160 343" {anim("spin .6s linear infinite")}/>'
             f'<circle class="c" cx="{cx}" cy="{cy}" r="80" fill="none" stroke="{GOLD}" stroke-width="16" '
             f'stroke-dasharray="60 443" {anim("spin .45s linear infinite reverse")}/>'
             f'<clipPath id="o"><rect x="{cx-56}" y="{cy-22}" width="112" height="44"/></clipPath><g clip-path="url(#o)">')
    for d, dur in enumerate(('60s', '6s', '.6s', '.12s')):
        col = ''.join(f'<text x="{cx-41+d*27}" y="{cy+14+k*44}" font-size="40" text-anchor="middle" fill="#fff">{k}</text>'
                      for k in range(10))
        body += f'<g {anim(f"odo {dur} steps(10) infinite")}>{col}</g>'
    body += f'</g><text x="{cx}" y="{cy+48}" font-size="16" text-anchor="middle" fill="{YEL}">植えた木</text>'
    svg('stats.svg', 1000, 270, 'データカウンター 期待度 9999% 確変継続中', css, body)


def footer():
    # 横 3 秒・縦 2 秒で往復させると、6 秒ごとにロゴがちょうど角に当たる(DVD の待機画面の小ネタ)
    css = ("@keyframes fall{from{transform:translateY(-40px) rotate(0)}to{transform:translateY(270px) rotate(var(--r))}}"
           "@keyframes dx{to{transform:translateX(830px)}}@keyframes dy{to{transform:translateY(184px)}}"
           "@keyframes corner{0%,5%{opacity:1;transform:scale(1.3) rotate(-4deg)}12%,100%{opacity:0;transform:scale(.8)}}")
    bits = ''
    for _ in range(120):
        x, d = random.randint(0, 1000), random.uniform(1.2, 2.8)
        a = f"--r:{random.choice((-1, 1))*random.randint(180, 720)}deg;animation:fall {d:.2f}s linear {-random.uniform(0, d):.2f}s infinite"
        k = random.random()
        if k < .2:
            bits += f'<text class="c" x="{x}" y="0" font-size="22" style="{a}">{random.choice(["🍃", "🌸", "🍀", "🪙"])}</text>'
        elif k < .35:
            bits += f'<circle class="c" cx="{x}" cy="-10" r="6" fill="url(#bf)" style="{a}"/>'
        else:
            bits += (f'<rect class="c" x="{x}" y="-10" width="{random.randint(8, 14)}" height="{random.randint(5, 9)}" '
                     f'fill="{random.choice([PINK, YEL, CYAN, LEAF, GOLD])}" style="{a}"/>')
    dvd = (f'<g {anim("dx 3s linear infinite alternate")}><g {anim("dy 2s linear infinite alternate")}>'
           f'<rect width="170" height="46" rx="23" {anim("hue 6s steps(6) infinite")}/>'
           f'<text x="85" y="31" font-size="22" text-anchor="middle" fill="{VIO}">🌳 MICKEY</text></g></g>')
    wave = ''.join(
        f'<text class="c ink pop" x="{500+(i-2.5)*78:.0f}" y="112" font-size="64" text-anchor="middle" stroke-width="10" '
        f'style="animation:jump .4s ease-in-out {i*.06:.2f}s infinite alternate,hue .6s linear {i*.1:.2f}s infinite">{ch}</text>'
        for i, ch in enumerate(['ま', 'た', '来', 'て', 'ね', '!!']))
    body = (f'<defs><radialGradient id="bf" cx=".35" cy=".35"><stop offset="0" stop-color="#fff"/>'
            f'<stop offset="1" stop-color="#6A6E7A"/></radialGradient></defs>{dvd}{bits}{wave}'
            f'<text class="c ink brush" x="500" y="180" font-size="32" text-anchor="middle" fill="{GOLD}" stroke-width="7" '
            f'{anim("wig .3s ease-in-out infinite alternate")}>次回も確変確定!! 🌳</text>'
            + ''.join(f'<text class="c" x="{x}" y="130" font-size="64" text-anchor="middle" '
                      f'style="animation:wig .2s ease-in-out {k*.1}s infinite alternate">🎉</text>'
                      for k, x in enumerate((110, 890)))
            + f'<text class="c ink pop" x="500" y="40" font-size="34" text-anchor="middle" fill="{RED}" stroke-width="7" '
              f'{anim("corner 6s ease-out infinite")}>角ヒット!!</text>')
    svg('footer.svg', 1000, 230, 'また来てね!! 次回も確変確定!!', css, body)


for f in (header, ticker, slot, board, stats, footer):
    f()
