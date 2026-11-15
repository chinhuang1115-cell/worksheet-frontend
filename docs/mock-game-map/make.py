# 互動遊戲導覽頁「地圖版」模擬圖（2026-11-15，參考使用者給的繪本地圖）：程式畫 SVG，再用 Playwright 轉 PNG。
# 用法：python docs/mock-game-map/make.py && node docs/mock-game-map/shot.js → map_1280.png（桌機）、map_1024.png（平板）
import pathlib

HERE = pathlib.Path(__file__).parent
FONT = (HERE / '../../fonts/Iansui-Regular.ttf').resolve()

# (店名, emoji, 雨棚色1, 雨棚色2, 牆色, x, y, 已開幕)；座標＝地圖 1000×720 上的店門口
SHOPS = [
    ('早餐店', '🍳', '#ef4444', '#fff', '#fff7ed', 150, 690, True),
    ('麵包店', '🥐', '#f472b6', '#fff', '#fdf2f8', 385, 668, True),
    ('文具店', '✏️', '#38bdf8', '#fff', '#eff6ff', 625, 690, True),
    ('糖果餅乾店', '🍭', '#c084fc', '#fff', '#faf5ff', 790, 590, True),
    ('飲料店', '🧋', '#34d399', '#fff', '#ecfdf5', 530, 462, False),
    ('玩具店', '🪀', '#ef4444', '#facc15', '#fefce8', 280, 428, False),
    ('便當店', '🍱', '#f97316', '#fff', '#fff7ed', 110, 300, False),
    ('中式餐館', '🥢', '#dc2626', '#fbbf24', '#fef3c7', 390, 268, False),
    ('服飾店', '🧢', '#fb7185', '#9ca3af', '#fff1f2', 600, 250, False),
]
SEL = '早餐店'

def shop_svg(n, emo, c1, c2, wall, x, y, live):
    on = n == SEL
    g = '' if live else ' filter="url(#gray)" opacity=".55"'
    stripes = ''.join(f'<rect x="{-70+i*20}" y="-96" width="20" height="26" fill="{c1 if i%2==0 else c2}"/>' for i in range(7))
    ring = '<rect x="-84" y="-150" width="168" height="196" rx="22" fill="none" stroke="#ea580c" stroke-width="6" stroke-dasharray="0"/>' if on else ''
    pin = ''
    label_bg = '#ea580c' if on else ('#fff' if live else '#f3f4f6')
    label_fg = '#fff' if on else '#2b3440'
    soon = '' if live else '<text x="0" y="-150" text-anchor="middle" font-size="16" fill="#6b7683">即將開幕</text>'
    return f'''<g transform="translate({x},{y}) scale(.82)" class="shop">
  <ellipse cx="0" cy="8" rx="82" ry="14" fill="#000" opacity=".10"/>
  {ring}
  <g{g}>
    <polygon points="-78,-96 78,-96 64,-136 -64,-136" fill="{c1}" stroke="#3b2f2f" stroke-width="3" stroke-linejoin="round"/>
    <rect x="-64" y="-70" width="128" height="76" rx="4" fill="{wall}" stroke="#3b2f2f" stroke-width="3"/>
    <g clip-path="url(#aw)">{stripes}</g>
    <path d="M-70,-70 q10,10 20,0 q10,10 20,0 q10,10 20,0 q10,10 20,0 q10,10 20,0 q10,10 20,0 q10,10 20,0" fill="none" stroke="#3b2f2f" stroke-width="3"/>
    <rect x="-70" y="-96" width="140" height="26" fill="none" stroke="#3b2f2f" stroke-width="3"/>
    <rect x="-16" y="-40" width="32" height="46" rx="4" fill="#b45309" stroke="#3b2f2f" stroke-width="3"/>
    <rect x="-56" y="-48" width="30" height="26" rx="3" fill="#bae6fd" stroke="#3b2f2f" stroke-width="3"/>
    <rect x="26" y="-48" width="30" height="26" rx="3" fill="#bae6fd" stroke="#3b2f2f" stroke-width="3"/>
    <text x="0" y="-104" text-anchor="middle" font-size="30">{emo}</text>
  </g>
  <rect x="{-12-len(n)*11}" y="20" width="{24+len(n)*22}" height="36" rx="18" fill="{label_bg}" stroke="#3b2f2f" stroke-width="2.5"/>
  <text x="0" y="46" text-anchor="middle" font-size="21" font-weight="800" fill="{label_fg}">{n}</text>
  {soon}{pin}
</g>'''

def tree(x, y, s=1):
    return f'<g transform="translate({x},{y}) scale({s})"><rect x="-5" y="-6" width="10" height="20" fill="#a16207" stroke="#3b2f2f" stroke-width="2"/><circle cx="0" cy="-22" r="22" fill="#4ade80" stroke="#3b2f2f" stroke-width="2.5"/><circle cx="-14" cy="-12" r="14" fill="#22c55e" stroke="#3b2f2f" stroke-width="2.5"/><circle cx="14" cy="-12" r="14" fill="#22c55e" stroke="#3b2f2f" stroke-width="2.5"/></g>'


def smooth(pts):
    d=f"M{pts[0][0]},{pts[0][1]}"
    for i in range(len(pts)-1):
        p0=pts[max(i-1,0)];p1=pts[i];p2=pts[i+1];p3=pts[min(i+2,len(pts)-1)]
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6);c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        d+=f" C{c1[0]:.0f},{c1[1]:.0f} {c2[0]:.0f},{c2[1]:.0f} {p2[0]},{p2[1]}"
    return d
# 主街：入口（左下）→ 往右 → 右側彎上去 → 往左 → 左側彎上去 → 往右到街尾
ROAD=smooth([(0,735),(260,738),(480,705),(720,735),(900,655),(905,540),(720,505),(420,520),(190,480),(105,385),(230,310),(470,310),(700,290),(880,230),(960,210)])
RIVER=smooth([(760,140),(770,210),(770,280),(800,350),(870,385),(930,395)])
TREES=[(40,250),(240,215),(420,420),(660,400),(980,300),(990,480),(30,560),(260,560),(520,600),(980,720),(700,600),(470,215)]



MAP = f'''<svg viewBox="0 0 1000 790" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;display:block" font-family="芫荽, Noto Color Emoji">
<defs>
  <filter id="gray"><feColorMatrix type="saturate" values="0"/></filter>
  <clipPath id="aw"><rect x="-70" y="-96" width="140" height="26"/></clipPath>
</defs>
<!-- 天空與遠山 -->
<rect width="1000" height="790" fill="#e0f2fe"/>
<path d="M0,150 L120,60 L230,130 L360,30 L500,120 L620,50 L760,130 L880,70 L1000,140 L1000,790 L0,790Z" fill="#86efac" stroke="#3b2f2f" stroke-width="3"/>
<ellipse cx="170" cy="70" rx="60" ry="18" fill="#fff" stroke="#3b2f2f" stroke-width="2"/><ellipse cx="820" cy="40" rx="70" ry="18" fill="#fff" stroke="#3b2f2f" stroke-width="2"/>
<!-- 草地 -->
<path d="M0,170 Q500,120 1000,170 L1000,790 L0,790Z" fill="#bbf7d0"/>
<!-- 小河（從山上流下來，流進右邊的小池塘）＋一座橋 -->
<ellipse cx="935" cy="400" rx="70" ry="40" fill="#38bdf8" stroke="#3b2f2f" stroke-width="3"/>
<path d="{RIVER}" fill="none" stroke="#38bdf8" stroke-width="40" stroke-linecap="round"/>
<path d="{RIVER}" fill="none" stroke="#7dd3fc" stroke-width="14" stroke-dasharray="18 28"/>
<!-- 彎彎的主街 -->
<path d="{ROAD}" fill="none" stroke="#fde68a" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>
<path d="{ROAD}" fill="none" stroke="#f59e0b" stroke-width="3" stroke-dasharray="2 14" stroke-linecap="round"/>
<g transform="translate(771,262) rotate(-18)"><rect x="-38" y="-18" width="76" height="36" rx="6" fill="#d97706" stroke="#3b2f2f" stroke-width="3"/><line x1="-38" y1="-6" x2="38" y2="-6" stroke="#3b2f2f" stroke-width="2"/><line x1="-38" y1="6" x2="38" y2="6" stroke="#3b2f2f" stroke-width="2"/></g>
<!-- 入口牌 -->
<g transform="translate(40,680)"><rect x="-4" y="0" width="8" height="60" fill="#a16207"/><rect x="-36" y="-34" width="72" height="38" rx="8" fill="#fff" stroke="#3b2f2f" stroke-width="2.5"/><text x="0" y="-8" text-anchor="middle" font-size="20" font-weight="800">入口</text></g>
{''.join(tree(x,y) for x,y in TREES)}
<g transform="translate(900,190)" opacity=".75"><rect x="-80" y="-60" width="160" height="70" rx="14" fill="#f5f5f4" stroke="#a8a29e" stroke-width="3" stroke-dasharray="10 8"/><text y="-16" text-anchor="middle" font-size="26">🚧</text><text y="40" text-anchor="middle" font-size="20" font-weight="800" fill="#78716c">敬請期待</text></g>
{''.join(shop_svg(*s) for s in sorted(SHOPS, key=lambda s: s[6]))}
</svg>'''

STAGES = [('1','買 1 樣','看價錢'),('2','買 2 樣','加法'),('3','同一樣買好幾個','乘法'),('4','綜合任務','先乘再加'),('5','自由配','錢夠不夠'),('6','折價券','先乘再減')]
side = ''.join(f'<div class="stage"><b>第 {a} 關</b><span>{b}</span><small>{c}</small></div>' for a,b,c in STAGES)

HTML = f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><style>
@font-face{{font-family:芫荽;src:url('file://{FONT}')}}
*{{box-sizing:border-box}}html,body{{margin:0;height:100%}}
body{{font-family:芫荽,sans-serif;background:#f6f5f2;color:#2b3440;display:grid;grid-template-columns:minmax(0,1fr) 320px;height:100vh;overflow:hidden}}
.edgetabs{{position:fixed;left:0;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;gap:10px;z-index:5}}
.edgetab{{writing-mode:vertical-rl;background:#3f8f8a;color:#fff;font-weight:800;letter-spacing:.25em;padding:16px 8px;border-radius:0 12px 12px 0;font-size:16px}}.edgetab.ws{{background:#2f4d6e}}
main{{position:relative;padding:14px 14px 14px 52px;display:flex;flex-direction:column;min-height:0}}
h1{{margin:0;font-size:28px;color:#2f4d6e}}.sub{{color:#6b7683;font-size:16px;margin-bottom:8px}}
.map{{flex:1;min-height:0;border-radius:22px;overflow:hidden;border:4px solid #3b2f2f;box-shadow:0 6px 0 rgba(0,0,0,.12)}}
aside{{border-left:4px solid #ea580c;padding:18px;overflow:hidden}}
aside .nm{{font-size:26px;font-weight:800}}aside .ds{{font-size:15px;color:#6b7683;margin-bottom:10px}}
.stage{{border:3px solid #ea580c;border-bottom-width:6px;border-radius:14px;padding:7px 12px;margin-bottom:8px;background:#fff}}
.stage b{{font-size:18px;color:#c2410c}}.stage span{{font-size:18px;font-weight:800;margin-left:10px}}.stage small{{display:block;font-size:14px;color:#6b7683}}
.lvl{{display:inline-flex;border:2px solid #e8863a;border-radius:12px;overflow:hidden;vertical-align:middle}}.lvl b{{padding:4px 14px;color:#e8863a}}.lvl b.on{{background:#e8863a;color:#fff}}
.mark{{position:fixed;right:330px;bottom:6px;font-size:13px;color:#9ca3af}}
</style></head><body>
<div class="edgetabs"><div class="edgetab">易數教室</div><div class="edgetab ws">互動學習單</div></div>
<main><h1>🗺️ 互動遊戲小鎮</h1><div class="sub">點一間店，右邊選關卡</div><div class="map">{MAP}</div></main>
<aside><div class="nm">🍳 早餐店</div><div class="ds">顧客點餐、算錢、付錢，店員找錢</div>
<div style="margin-bottom:10px">提示：<span class="lvl"><b>強</b><b class="on">弱</b><b>無</b></span></div>{side}</aside>
<div class="mark">模擬圖：地圖版（程式畫；正式版可換 Gemini 插畫）</div>
</body></html>'''

(HERE / 'mock_map.html').write_text(HTML, encoding='utf-8')
print('ok；接著跑 node docs/mock-game-map/shot.js 出 PNG')
