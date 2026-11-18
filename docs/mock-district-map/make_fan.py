# 價位街區「扇形總覽地圖」模擬圖 E～G（使用者 2026-11-18 選 C 總圖、問能否做成扇形、一頁看全部）
# python make_fan.py → E/F/G *.html，再 node shot.js 截圖
import math, pathlib
from make import ZONES
D = pathlib.Path(__file__).parent
W, H = 1100, 660
GRAY = '<filter id="g"><feColorMatrix type="saturate" values="0"/></filter>'


def P(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def sector(cx, cy, r0, r1, a0, a1, fill, stroke='#3b2f2f'):
    # a0→a1 逆時針（度，數學座標，往上為正）
    x0, y0 = P(cx, cy, r1, a0); x1, y1 = P(cx, cy, r1, a1)
    x2, y2 = P(cx, cy, r0, a1); x3, y3 = P(cx, cy, r0, a0)
    big = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'<path d="M{x0:.1f},{y0:.1f} A{r1},{r1} 0 {big} 0 {x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} '
            f'A{r0},{r0} 0 {big} 1 {x3:.1f},{y3:.1f} Z" fill="{fill}" stroke="{stroke}" stroke-width="4"/>')


def icon(x, y, e, n, lock, s=1.0):
    r = 27 * s
    return (f'<g transform="translate({x:.1f},{y:.1f})"{" filter=url(#g) opacity=.5" if lock else ""}>'
            f'<circle r="{r}" fill="#fff" stroke="#3b2f2f" stroke-width="3"/>'
            f'<text y="{10*s:.1f}" text-anchor="middle" font-size="{28*s:.0f}">{e}</text>'
            f'<rect x="{-len(n)*8.5*s-6:.1f}" y="{r+3:.1f}" width="{len(n)*17*s+12:.1f}" height="{22*s:.1f}" rx="{11*s:.1f}" fill="#fff" stroke="#3b2f2f" stroke-width="2"/>'
            f'<text y="{r+19*s:.1f}" text-anchor="middle" font-size="{15*s:.0f}" font-weight="800">{n}</text></g>')


def bank(x, y, s=1.0):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s})"><circle r="30" fill="#facc15" stroke="#3b2f2f" stroke-width="3"/>'
            f'<text y="11" text-anchor="middle" font-size="30">🏦</text>'
            f'<rect x="-26" y="32" width="52" height="22" rx="11" fill="#facc15" stroke="#3b2f2f" stroke-width="2"/>'
            f'<text y="48" text-anchor="middle" font-size="15" font-weight="900">銀行</text></g>')


def label(x, y, z, lock):
    t = z['name'] + ('  🔒' if lock else '')
    w = len(t) * 22 + 30
    return (f'<g transform="translate({x:.1f},{y:.1f})"><rect x="{-w/2}" y="-24" width="{w}" height="40" rx="20" fill="{"#9ca3af" if lock else z["c"]}" stroke="#3b2f2f" stroke-width="3"/>'
            f'<text y="5" text-anchor="middle" font-size="22" font-weight="900" fill="#fff">{t}</text>'
            f'<text y="36" text-anchor="middle" font-size="14" font-weight="800" fill="#1f2937">{z["sub"]}・{z["money"]}</text></g>')


def items(z):
    return z['shops'] + z['venues']


def page(tag, svg, foot):
    return (f'<!doctype html><meta charset="utf-8"><style>body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;font-family:"Noto Sans TC",sans-serif;background:#dcfce7}}'
            f'.tag{{position:absolute;left:12px;top:10px;background:#111827;color:#fff;font-weight:800;padding:4px 12px;border-radius:8px;font-size:16px}}'
            f'.foot{{position:absolute;right:12px;bottom:8px;max-width:520px;font-weight:800;font-size:14px;color:#1f2937;background:#fffc;border-radius:8px;padding:2px 8px}}</style>'
            f'<svg width="{W}" height="{H}"><defs>{GRAY}</defs>{svg}</svg><div class="tag">{tag}</div><div class="foot">{foot}</div>')


LOCK = [False, True, True]

# E 半圓三扇：入口在下方中央，三個扇形左→右＝巷口小街→熱鬧大街→百貨商場，扇形交界有銀行
cx, cy, r0, r1 = 550, 650, 95, 625
svg = ''
for i, z in enumerate(ZONES):
    a1, a0 = 180 - i * 60, 120 - i * 60
    svg += sector(cx, cy, r0, r1, a0, a1, z['bg'] if not LOCK[i] else '#e5e7eb')
for i, z in enumerate(ZONES):
    a1, a0 = 180 - i * 60, 120 - i * 60
    it = items(z); rows = [it[:2], it[2:5], it[5:]]
    for k, (row, r) in enumerate(zip(rows, (255, 385, 505))):
        for j, s in enumerate(row):
            a = a0 + (a1 - a0) * (j + 1) / (len(row) + 1)
            x, y = P(cx, cy, r, a); svg += icon(x, y - 10, s[0], s[1], LOCK[i], .8)
    lx, ly = P(cx, cy, 585, (a0 + a1) / 2); svg += label(min(max(lx, 150), 950), max(ly, 70), z, LOCK[i])
for a in (120, 60):
    x, y = P(cx, cy, 170, a); svg += bank(x, y - 10, .9)
svg += f'<path d="M{cx-r0},{cy} A{r0},{r0} 0 0 1 {cx+r0},{cy}" fill="#9ca3af" stroke="#3b2f2f" stroke-width="4"/><text x="{cx}" y="{cy-30}" text-anchor="middle" font-size="22" font-weight="900" fill="#fff">🚶 入口</text>'
(D / 'E_半圓三扇.html').write_text(page('E 半圓三扇（入口在下方，左→右三區）', svg, '三區都在同一頁；點店直接開右側欄（和現在一樣）。鎖住的區是灰色。'), encoding='utf-8')

# F 同心扇：入口在下方中央，越往外圈越貴（巷口小街→熱鬧大街→百貨商場），每一圈的門口有銀行
cx, cy = 550, 655
bands = [(90, 300), (300, 470), (470, 645)]
svg = ''
for i, z in list(enumerate(ZONES))[::-1]:
    svg += sector(cx, cy, bands[i][0], bands[i][1], 0.01, 179.99, z['bg'] if not LOCK[i] else '#e5e7eb')
for i, z in enumerate(ZONES):
    it = items(z); lo, hi = bands[i]; rA, rB = lo + (hi - lo) * .32, lo + (hi - lo) * .76
    L, R = it[::2], it[1::2]                                 # 左半、右半各一半，中間留給區名與銀行
    for side, grp in ((0, L), (1, R)):
        for j, s in enumerate(grp):
            rr = rA if j % 2 == 0 else rB
            k = len(grp)
            a = 12 + 60 * j / max(k - 1, 1) if side == 0 else 168 - 60 * j / max(k - 1, 1)
            if i == 0: a = 18 + 52 * j / max(k - 1, 1) if side == 0 else 162 - 52 * j / max(k - 1, 1)
            x, y = P(cx, cy, rr, a); svg += icon(x, y - 8, s[0], s[1], LOCK[i], .74)
for i, z in enumerate(ZONES):
    x, y = P(cx, cy, (bands[i][0] + bands[i][1]) / 2 + 10, 90); svg += label(x, y - 6, z, LOCK[i])
for i in (1, 2):
    x, y = P(cx, cy, bands[i][0], 90); svg += bank(x - 0, y - 8, .7)
svg += f'<path d="M{cx-95},{cy} A95,95 0 0 1 {cx+95},{cy}" fill="#9ca3af" stroke="#3b2f2f" stroke-width="4"/><text x="{cx}" y="{cy-30}" text-anchor="middle" font-size="22" font-weight="900" fill="#fff">🚶 入口</text>'
(D / 'F_同心扇.html').write_text(page('F 同心扇（一圈一圈往外，越外越貴）', svg, '從入口往外走：巷口小街 → 銀行 → 熱鬧大街 → 銀行 → 百貨商場，像一層一層升級。'), encoding='utf-8')

# G 整圓三扇：中間是小鎮廣場，三區各佔 120 度，順時針一區一區走，銀行在交界
cx, cy, r0, r1 = 550, 335, 75, 312
starts = [210, 90, -30]          # 左下、上、右下
svg = ''
for i, z in enumerate(ZONES):
    a0 = starts[i] - 120 + 120; a1 = a0 + 120
    svg += sector(cx, cy, r0, r1, starts[i] - 0, starts[i] + 120, z['bg'] if not LOCK[i] else '#e5e7eb')
for i, z in enumerate(ZONES):
    a0, a1 = starts[i], starts[i] + 120
    it = items(z); rows = [it[:4], it[4:]]
    for row, r in zip(rows, (160, 255)):
        for j, s in enumerate(row):
            a = a0 + (a1 - a0) * (j + 1) / (len(row) + 1)
            x, y = P(cx, cy, r, a); svg += icon(x, y - 8, s[0], s[1], LOCK[i], .78)
lab = [(170, 560), (170, 70), (930, 70)]
for i, z in enumerate(ZONES):
    svg += label(lab[i][0], lab[i][1] + 26, z, LOCK[i])
for a in (210, 90):     # 1↔2、2↔3 的交界
    x, y = P(cx, cy, 200, a % 360); svg += bank(x, y - 8, .8)
x, y = P(cx, cy, 200, 330); svg += f'<text x="{x:.0f}" y="{y:.0f}" font-size="30" text-anchor="middle">🌳🌳</text>'
svg += f'<circle cx="{cx}" cy="{cy}" r="{r0}" fill="#9ca3af" stroke="#3b2f2f" stroke-width="4"/><text x="{cx}" y="{cy+8}" text-anchor="middle" font-size="22" font-weight="900" fill="#fff">⛲ 廣場</text>'
(D / 'G_整圓三扇.html').write_text(page('G 整圓三扇（中間廣場，三區圍一圈）', svg, '中間是廣場（入口）；巷口小街 → 銀行 → 熱鬧大街 → 銀行 → 百貨商場，順時針繞一圈。'), encoding='utf-8')
print('ok')
