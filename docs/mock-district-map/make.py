# 價位街區地圖「換頁」模擬圖 A～D：python make.py → *.html，再 node shot.js 截圖
# 規劃稿 docs/價位街區_規劃.md（使用者 2026-11-18）
import pathlib
D = pathlib.Path(__file__).parent

ZONES = [
    dict(key='z1', name='巷口小街', sub='100 元以內', c='#f97316', bg='#fff7ed', ground='#fde68a', money='1・5・10・50 元',
         shops=[('🍳', '早餐店', '#ef4444'), ('🥐', '麵包店', '#f472b6'), ('✏️', '文具店', '#38bdf8'), ('🍭', '糖果餅乾店', '#c084fc'),
                ('🪀', '玩具店', '#facc15'), ('🧋', '飲料店', '#34d399'), ('🥢', '中式餐館', '#dc2626'), ('🧦', '服飾店', '#fb7185')],
         venues=[('🚌', '公車站', '#0ea5e9'), ('🦁', '動物園', '#65a30d')]),
    dict(key='z2', name='熱鬧大街', sub='1000 元以內', c='#2563eb', bg='#eff6ff', ground='#bfdbfe', money='＋100・500 元鈔',
         shops=[('👕', '服飾店', '#fb7185'), ('👟', '鞋店', '#a78bfa'), ('🍱', '便當店', '#f97316'), ('📚', '書店', '#0d9488'),
                ('⚽', '運動用品店', '#22c55e'), ('🍎', '水果行', '#ef4444')],
         venues=[('🎬', '電影院', '#7c3aed'), ('🏛️', '博物館', '#78716c'), ('🚆', '火車站', '#0284c7')]),
    dict(key='z3', name='百貨商場', sub='10000 元以內', c='#9333ea', bg='#faf5ff', ground='#e9d5ff', money='＋1000 元鈔',
         shops=[('📺', '家電行', '#64748b'), ('🚲', '腳踏車店', '#16a34a'), ('💻', '電腦用品店', '#0ea5e9'), ('🛋️', '家具行', '#b45309'),
                ('🎹', '樂器行', '#e11d48'), ('🧥', '服飾店', '#fb7185')],
         venues=[('🚄', '高鐵站', '#f97316'), ('🎢', '遊樂園', '#db2777'), ('🏨', '飯店', '#0f766e')]),
]

CSS = """
*{box-sizing:border-box}body{margin:0;font-family:'Noto Sans TC',sans-serif;background:#f8fafc;width:1100px;height:660px;overflow:hidden;color:#1f2937}
.tag{position:absolute;left:12px;top:10px;background:#111827;color:#fff;font-weight:800;padding:4px 12px;border-radius:8px;font-size:16px;z-index:9}
.shop{width:118px;text-align:center;position:relative}
.shop .roof{height:22px;border:3px solid #3b2f2f;border-bottom:0;border-radius:10px 10px 0 0;background:repeating-linear-gradient(90deg,var(--c) 0 14px,#fff 14px 28px)}
.shop .wall{height:62px;border:3px solid #3b2f2f;background:#fff;display:flex;align-items:center;justify-content:center;font-size:36px}
.shop .nm{margin-top:4px;font-weight:800;font-size:15px;background:#fff;border:2px solid #3b2f2f;border-radius:14px;padding:2px 4px}
.venue .roof{background:var(--c);border-radius:40px 40px 0 0;height:26px}
.venue .wall{background:#f1f5f9}
.venue .nm{background:#fef9c3}
.lock{filter:grayscale(1);opacity:.45}
.street{position:absolute;left:0;right:0;bottom:0;height:150px;background:#9ca3af}
.street:after{content:'';position:absolute;left:0;right:0;top:72px;border-top:6px dashed #fff}
.hdr{position:absolute;left:0;right:0;top:0;height:64px;display:flex;align-items:center;justify-content:center;gap:14px;color:#fff;font-weight:900;font-size:28px}
.hdr small{font-size:16px;font-weight:700;background:#fff3;border-radius:12px;padding:3px 10px}
.money{position:absolute;right:16px;top:74px;background:#fff;border:2px solid #3b2f2f;border-radius:12px;padding:4px 10px;font-weight:800;font-size:14px}
.arrow{position:absolute;top:290px;width:74px;height:120px;border-radius:16px;background:#f97316;color:#fff;font-size:44px;display:flex;align-items:center;justify-content:center;border:3px solid #3b2f2f;font-weight:900}
.arrow small{position:absolute;bottom:-44px;width:150px;text-align:center;color:#1f2937;font-size:14px;font-weight:800;line-height:1.2}
.arrow.off{background:#d1d5db}
.bank{width:130px;text-align:center}
.bank .wall{height:84px;background:#fef3c7;border:3px solid #3b2f2f;font-size:40px;display:flex;align-items:center;justify-content:center;border-top:0}
.bank .roof{height:30px;background:#ca8a04;border:3px solid #3b2f2f;clip-path:polygon(0 100%,50% 0,100% 100%);border:0}
.bank .nm{margin-top:4px;font-weight:900;font-size:16px;background:#facc15;border:2px solid #3b2f2f;border-radius:14px;padding:2px 4px}
.fence{position:absolute;background:repeating-linear-gradient(90deg,#fff 0 18px,#ef4444 18px 36px);border:3px solid #3b2f2f;border-radius:8px;height:34px;font-weight:900;text-align:center;line-height:28px;font-size:15px;color:#7f1d1d}
.dots{position:absolute;bottom:14px;left:0;right:0;display:flex;justify-content:center;gap:10px;z-index:3}
.dots span{background:#fff;border:2px solid #3b2f2f;border-radius:14px;padding:2px 12px;font-weight:800;font-size:14px}
.dots span.on{background:#f97316;color:#fff}
.dots span.lk{background:#e5e7eb;color:#6b7280}
.note{position:absolute;left:12px;bottom:-1px;font-size:13px;color:#374151}
"""


def shop(e, n, c, venue=False, lock=False):
    return f'<div class="shop{" venue" if venue else ""}{" lock" if lock else ""}" style="--c:{c}"><div class="roof"></div><div class="wall">{e}</div><div class="nm">{n}</div></div>'


def bank(label='銀行'):
    return f'<div class="bank"><div class="roof"></div><div class="wall">🏦</div><div class="nm">{label}</div></div>'


def page(title, body):
    return f'<!doctype html><meta charset="utf-8"><title>{title}</title><style>{CSS}</style><body>{body}</body>'


def zone_page(z, lock=False, left=None, right=None, extra=''):
    items = [shop(*s, lock=lock) for s in z['shops']] + [shop(*v, venue=True, lock=lock) for v in z['venues']]
    half = (len(items) + 1) // 2
    row = lambda xs, top: f'<div style="position:absolute;left:100px;right:100px;top:{top}px;display:flex;justify-content:space-around">{"".join(xs)}</div>'
    b = f'<div style="position:absolute;inset:0;background:{z["bg"]}"></div>'
    b += f'<div class="hdr" style="background:{z["c"]}">{z["name"]}<small>{z["sub"]}</small></div>'
    b += f'<div class="money">💰 用到的錢：{z["money"]}</div>'
    b += row(items[:half], 112) + row(items[half:], 262)
    b += '<div class="street"></div>'
    if left: b += left
    if right: b += right
    return b + extra


def arrow(side, txt, sub, off=False):
    pos = 'left:12px' if side == 'L' else 'right:12px'
    return f'<div class="arrow{" off" if off else ""}" style="{pos}">{txt}<small>{sub}</small></div>'


z1, z2, z3 = ZONES

# A 左右翻頁：一頁一區，街尾有銀行，右箭頭＝去銀行／下一區
A = zone_page(z1, left=arrow('L', '◀', '', off=True),
              right=arrow('R', '▶', '下一區<br>熱鬧大街'),
              extra='<div style="position:absolute;right:110px;bottom:150px">' + bank('銀行（換錢）') + '</div>'
                    '<div class="dots"><span class="on">① 巷口小街</span><span>🏦</span><span class="lk">🔒 ② 熱鬧大街</span><span>🏦</span><span class="lk">🔒 ③ 百貨商場</span></div>')
A = A.replace('right:100px;top:112px', 'right:260px;top:112px').replace('right:100px;top:262px', 'right:260px;top:262px')
(D / 'A_左右翻頁.html').write_text(page('A', '<div class="tag">A 左右翻頁（一頁一區，銀行在街尾）</div>' + A), encoding='utf-8')

# B 上方頁籤：銀行是獨立一頁；這張顯示「熱鬧大街」還鎖著的樣子
tabs = ('<div style="position:absolute;left:0;right:0;top:0;height:58px;background:#334155;display:flex;align-items:flex-end;gap:6px;padding:0 20px">'
        + ''.join(f'<div style="padding:8px 18px;border-radius:12px 12px 0 0;font-weight:900;font-size:18px;{s}">{t}</div>' for t, s in [
            ('巷口小街', 'background:#fff7ed;color:#c2410c'), ('🏦 銀行', 'background:#fef3c7'), ('熱鬧大街 🔒', 'background:#eff6ff;color:#1d4ed8;outline:4px solid #f97316'),
            ('🏦 銀行', 'background:#e5e7eb;color:#6b7280'), ('百貨商場 🔒', 'background:#e5e7eb;color:#6b7280')]) + '</div>')
B = zone_page(z2, lock=True).replace('class="hdr" style="', 'class="hdr" style="top:58px;height:56px;').replace('top:112px', 'top:150px').replace('top:262px', 'top:300px').replace('top:74px', 'top:124px')
B += ('<div class="fence" style="left:250px;right:250px;top:470px">🚧 到銀行換好錢就能去 🚧</div>'
      '<div style="position:absolute;left:390px;top:520px;background:#facc15;border:3px solid #3b2f2f;border-radius:14px;padding:6px 18px;font-weight:900;font-size:18px">🏦 去銀行換錢</div>')
(D / 'B_上方頁籤.html').write_text(page('B', B + tabs + '<div class="tag" style="top:64px">B 上方頁籤（銀行獨立一頁，這張是還鎖著）</div>'), encoding='utf-8')

# C 先看小鎮總圖 → 點一區進去（總圖只有三區＋銀行）
def card(z, lock, x, y):
    ic = ''.join(s[0] for s in z['shops'][:4]) + ''.join(v[0] for v in z['venues'][:2])
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:270px;height:250px;border-radius:26px;background:{z["bg"]};border:5px solid {z["c"]};'
            f'text-align:center;padding-top:16px{";filter:grayscale(1);opacity:.5" if lock else ""}">'
            f'<div style="font-size:28px;font-weight:900;color:{z["c"]}">{z["name"]}</div><div style="font-weight:800">{z["sub"]}</div>'
            f'<div style="font-size:34px;margin:14px 0;letter-spacing:4px">{ic}</div>'
            f'<div style="font-weight:800;font-size:14px">💰 {z["money"]}</div>'
            f'{"<div style=font-size:40px>🔒</div>" if lock else "<div style=margin-top:8px;background:#f97316;color:#fff;border-radius:14px;display:inline-block;padding:4px 18px;font-weight:900>走進去 ▶</div>"}</div>')
C = ('<div style="position:absolute;inset:0;background:#dcfce7"></div>'
     '<div class="hdr" style="background:#16a34a">互動遊戲小鎮</div>'
     '<svg style="position:absolute;inset:0" width="1100" height="660"><path d="M60,470 C250,560 330,380 550,430 S850,560 1060,420" stroke="#9ca3af" stroke-width="46" fill="none"/>'
     '<path d="M60,470 C250,560 330,380 550,430 S850,560 1060,420" stroke="#fff" stroke-width="4" stroke-dasharray="16 14" fill="none"/></svg>'
     + card(z1, False, 40, 110) + card(z2, True, 415, 110) + card(z3, True, 790, 110)
     + '<div style="position:absolute;left:315px;top:410px;transform:scale(.8)">' + bank() + '</div>'
     + '<div style="position:absolute;left:690px;top:430px;transform:scale(.8)">' + bank() + '</div>'
     + '<div style="position:absolute;left:40px;bottom:16px;font-weight:800;font-size:15px">點一個街區 → 進到那一區的街道（像現在的小鎮地圖）</div>')
(D / 'C_小鎮總圖.html').write_text(page('C', C + '<div class="tag" style="top:72px">C 先看小鎮總圖，點一區再進去</div>'), encoding='utf-8')

# D 搭公車換區：街尾公車站旁就是銀行，換好錢上公車，公車開走＝換頁
D_ = zone_page(z1, left=arrow('L', '◀', '', off=True))
D_ = D_.replace('right:100px;top:112px', 'right:290px;top:112px').replace('right:100px;top:262px', 'right:290px;top:262px')
D_ += ('<div style="position:absolute;right:150px;bottom:150px">' + bank('① 先換錢') + '</div>'
       '<div style="position:absolute;right:20px;bottom:150px;text-align:center"><div style="font-size:16px;font-weight:900;background:#0ea5e9;color:#fff;border-radius:8px;padding:2px 6px">🚏 公車站</div><div style="height:90px;width:6px;background:#3b2f2f;margin:0 auto"></div></div>'
       '<div style="position:absolute;right:70px;bottom:30px;font-size:96px;transform:scaleX(-1)">🚌</div>'
       '<div style="position:absolute;right:220px;bottom:58px;background:#fff;border:3px solid #3b2f2f;border-radius:14px;padding:4px 14px;font-weight:900;font-size:17px">② 搭公車去「熱鬧大街」▶</div>'
       '<div class="dots" style="justify-content:flex-start;left:20px"><span class="on">巷口小街</span><span class="lk">熱鬧大街</span><span class="lk">百貨商場</span></div>')
(D / 'D_搭公車換區.html').write_text(page('D', '<div class="tag">D 搭公車換區（街尾銀行＋公車站，公車開走＝換頁）</div>' + D_), encoding='utf-8')
print('ok')
