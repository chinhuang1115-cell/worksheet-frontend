#!/usr/bin/env python3
"""自助選購型店家模擬圖：python docs/mock-selfserve/make.py  （需 playwright）"""
import os, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
GAME = '/home/user/worksheet-backend/backend/assets/game'
ST = f'file://{REPO}/images/遊戲_文具店/'
CD = f'file://{REPO}/images/遊戲_糖果餅乾店/'
G = f'file://{GAME}/'
FONT = "'WenQuanYi Zen Hei','Noto Sans CJK TC',sans-serif"

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#f1f5f9;font-family:%s;color:#1f2937}
.page{padding:22px 26px 26px}
.hd{display:flex;align-items:baseline;gap:18px;margin-bottom:14px}
.hd b{font-size:40px;color:#c2410c}.hd span{font-size:24px;color:#475569}
.row{display:flex;align-items:flex-start;gap:0}
.col{display:flex;flex-direction:column}
.cap{display:flex;align-items:center;gap:10px;font-size:26px;font-weight:bold;margin:0 0 8px 4px}
.cap i{font-style:normal;background:#ea580c;color:#fff;border-radius:50%%;width:36px;height:36px;display:flex;align-items:center;justify-content:center;font-size:22px}
.sub{font-size:19px;color:#475569;margin:8px 4px 0;min-height:52px;line-height:1.35}
.pn{position:relative;width:760px;height:570px;border-radius:16px;overflow:hidden;border:4px solid #334155;background:#fff7ea;box-shadow:0 4px 14px rgba(0,0,0,.25)}
.chev{width:70px;align-self:center;text-align:center;font-size:56px;color:#ea580c;margin-top:30px}
.a{position:absolute}
.tag{display:inline-block;background:#f3e8ff;border:2px solid #7c3aed;color:#6d28d9;border-radius:12px;padding:0 8px;font-size:15px;font-weight:bold;line-height:21px;white-space:nowrap}
.nm{font-size:16px;font-weight:bold;text-align:center;line-height:18px}
.it{position:absolute;width:96px;text-align:center}
.it img{width:68px;height:68px;display:block;margin:0 auto}
.it.hl img{filter:drop-shadow(0 0 8px #f59e0b)}
.it.hl:before{content:'';position:absolute;inset:-4px 2px -3px;border:4px solid #f59e0b;border-radius:12px;background:rgba(251,191,36,.18)}
.it.dim{opacity:.38}
.board{position:absolute;height:14px;border-radius:4px;background:linear-gradient(#d9a066,#b5773a);box-shadow:0 3px 3px rgba(0,0,0,.25)}
.shelfback{position:absolute;background:#f8ecd2;border:5px solid #9a6330;border-radius:6px}
.bk{position:absolute}
.bkb{position:absolute;left:0;right:0;bottom:0;height:62%%;clip-path:polygon(0 0,100%% 0,88%% 100%%,12%% 100%%);
 background:repeating-linear-gradient(90deg,#c58a4b 0 7px,#a8702f 7px 9px),#c58a4b;border-radius:0 0 8px 8px}
.bkb:after{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.14) 0 3px,transparent 3px 14px)}
.bkh{position:absolute;left:18%%;right:18%%;top:0;height:60%%;border:6px solid #8a5a2b;border-bottom:none;border-radius:60px 60px 0 0}
.bkrim{position:absolute;left:-4px;right:-4px;top:38%%;height:9px;background:#8a5a2b;border-radius:5px;z-index:3}
.bki{position:absolute;z-index:2}
.task{position:absolute;background:#fffbe6;border:3px dashed #f59e0b;border-radius:14px;padding:6px 12px;font-size:22px;font-weight:bold;display:flex;align-items:center;gap:6px;white-space:nowrap}
.task img{height:36px}
.task .ck{color:#16a34a;font-size:24px}
.task .tt{font-size:15px;color:#92400e;position:absolute;top:-14px;left:10px;background:#fffbe6;padding:0 6px;border-radius:6px}
.btn{position:absolute;background:#ea580c;color:#fff;border-radius:16px;font-size:26px;font-weight:bold;padding:8px 22px;box-shadow:0 4px 0 #9a3412;white-space:nowrap}
.btn.g{background:#e2e8f0;color:#94a3b8;box-shadow:0 4px 0 #cbd5e1}
.bubble{position:absolute;background:#fff;border:3px solid #334155;border-radius:16px;padding:6px 14px;font-size:21px;font-weight:bold;white-space:nowrap}
.floor{position:absolute;left:0;right:0;bottom:0;background:repeating-linear-gradient(90deg,#f1dcb8 0 60px,#ead2a8 60px 62px)}
.wall{position:absolute;left:0;right:0;top:0;background:#cfe8fb}
.sign{position:absolute;background:#1e3a8a;color:#fff;font-size:22px;font-weight:bold;padding:4px 16px;border-radius:8px;border:3px solid #93c5fd;white-space:nowrap}
.desk{position:absolute;background:linear-gradient(#e5edff,#b9c8ee);border:3px solid #6477b0;border-radius:10px}
.desktop{position:absolute;background:#dbe5ff;border:3px solid #6477b0;clip-path:polygon(8%% 0,92%% 0,100%% 100%%,0 100%%)}
.arrowlbl{position:absolute;font-size:20px;font-weight:bold;color:#fff;background:#2563eb;border-radius:12px;padding:2px 12px;white-space:nowrap}
.dot{position:absolute;border-radius:50%%;background:#ea580c;color:#fff;font-weight:bold;display:flex;align-items:center;justify-content:center}
.note{position:absolute;font-size:17px;color:#475569}
""" % FONT

def img(src, style='', cls=''):
    return f'<img class="a {cls}" style="{style}" src="{src}">'

def person(x, y, h, n=1, flip=False, walk=True):
    f = f'customer_walk_{n}.png' if walk else f'customer_{n}.png'
    t = 'transform:scaleX(-1);' if flip else ''
    return img(G + f, f'left:{x}px;top:{y}px;height:{h}px;{t}')

def clerk(x, y, h=150):
    return img(G + 'clerk_1.png', f'left:{x}px;top:{y}px;height:{h}px')

def hand(x, y, s=46):
    return img(G + 'cursor_tap@3x.png', f'left:{x}px;top:{y}px;width:{s}px;z-index:20;filter:drop-shadow(0 2px 2px rgba(0,0,0,.4))')

def item(base, name, price, x, y, state='', size=68, show_tag=True):
    st = f' {state}' if state else ''
    sz = f'style="width:{size}px;height:{size}px"'
    tag = f'<div style="margin-top:2px"><span class="tag">{price} 元</span></div>' if show_tag else ''
    return (f'<div class="it{st}" style="left:{x}px;top:{y}px"><img {sz} src="{base}{name}.png">'
            f'<div class="nm">{name}</div>{tag}</div>')

def shelf(base, x, y, rows, prices, states=None, rowh=132, cols=4, title=None, size=68, iw=96):
    """rows: list of list of names"""
    states = states or {}
    w = cols * iw + 16
    h = len(rows) * rowh + 20
    out = [f'<div class="shelfback" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>']
    for r, names in enumerate(rows):
        ry = y + 8 + r * rowh
        for c, n in enumerate(names):
            out.append(item(base, n, prices[n], x + 8 + c * iw, ry, states.get(n, ''), size))
        out.append(f'<div class="board" style="left:{x+2}px;top:{ry+rowh-14}px;width:{w-4}px"></div>')
    return ''.join(out)

def basket(x, y, w, items=(), base=ST, isz=36, label=None):
    h = int(w * 0.8)
    s = [f'<div class="bk" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><div class="bkh"></div><div class="bkb"></div><div class="bkrim"></div>']
    n = len(items)
    for i, nm in enumerate(items):
        cx = (w - isz * n * 0.7) / 2 + i * isz * 0.7
        s.append(f'<img class="bki" style="left:{cx:.0f}px;top:{int(h*0.38-isz*0.8)}px;width:{isz}px" src="{base}{nm}.png">')
    s.append('</div>')
    if label:
        s.append(f'<div class="a" style="left:{x-6}px;top:{y+h+4}px;width:{w+12}px;text-align:center;font-size:17px;font-weight:bold;color:#7c2d12">{label}</div>')
    return ''.join(s)

def task(x, y, parts, title='任務卡', w=None):
    """parts: list of (text, imgname|None, done)"""
    h = ''.join((f'<span>{t}</span>' + (f'<img src="{ST}{im}.png">' if im else '') + ('<span class="ck">✔</span>' if d else '')) for t, im, d in parts)
    ws = f';white-space:normal;flex-wrap:wrap;width:{w}px;font-size:20px' if w else ''
    return f'<div class="task" style="left:{x}px;top:{y}px{ws}"><span class="tt">📝 {title}</span>{h}</div>'

def route(d, color='#2563eb', w=7, dash='4 12', extra=''):
    return (f'<svg class="a" style="left:0;top:0;z-index:15" width="760" height="570"><defs><marker id="ar{abs(hash(d))%9999}" markerUnits="userSpaceOnUse" markerWidth="24" markerHeight="24" refX="12" refY="12" orient="auto"><path d="M2,3 L22,12 L2,21 z" fill="{color}"/></marker></defs>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-dasharray="{dash}" marker-end="url(#ar{abs(hash(d))%9999})" {extra}/></svg>')

def lbl(x, y, t, cls='arrowlbl', extra=''):
    return f'<div class="{cls}" style="left:{x}px;top:{y}px;{extra}">{t}</div>'

def door(x, y, w=80, h=130):
    return (f'<div class="a" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#a16207;border:4px solid #713f12;border-radius:8px 8px 0 0"></div>'
            f'<div class="a" style="left:{x+10}px;top:{y+12}px;width:{w-20}px;height:{h-60}px;background:#bfe3f7;border:3px solid #713f12"></div>'
            f'<div class="a" style="left:{x}px;top:{y-30}px;width:{w}px;text-align:center;font-size:18px;font-weight:bold;color:#713f12">入口</div>')

def counter(x, y, w=300, h=100, items=(), beeps=False, prices=None, base=ST):
    """櫃台：桌面梯形＋前板。items 放在桌面上（名稱列表）"""
    s = [f'<div class="desktop" style="left:{x}px;top:{y}px;width:{w}px;height:{int(h*0.5)}px"></div>',
         f'<div class="desk" style="left:{x+8}px;top:{y+int(h*0.5)-2}px;width:{w-16}px;height:{int(h*0.6)}px"></div>']
    n = len(items)
    for i, nm in enumerate(items):
        cx = x + (w - n * 70) / 2 + i * 70
        s.append(f'<img class="a" style="left:{cx:.0f}px;top:{y-52}px;width:62px;z-index:4" src="{base}{nm}.png">')
        if prices:
            s.append(f'<div class="a" style="left:{cx-6:.0f}px;top:{y+10}px;width:74px;text-align:center;z-index:5"><span class="tag" style="font-size:13px;line-height:18px">{prices[i]} 元</span></div>')
    return ''.join(s)

def register(x, y):
    return (f'<div class="a" style="left:{x}px;top:{y}px;width:70px;height:46px;background:#475569;border-radius:6px;border:3px solid #1e293b"></div>'
            f'<div class="a" style="left:{x+6}px;top:{y+5}px;width:58px;height:18px;background:#86efac;border-radius:3px;font-size:13px;text-align:center;font-weight:bold;line-height:18px">$ 0</div>')

def panel(inner, bg=None):
    s = f' style="background:{bg}"' if bg else ''
    return f'<div class="pn"{s}>{inner}</div>'

def step(n, title, sub, inner, bg=None):
    return (f'<div class="col"><div class="cap"><i>{n}</i>{title}</div>{panel(inner,bg)}<div class="sub">{sub}</div></div>')

def page(title, desc, steps_html, width=None):
    chev = '<div class="chev">➜</div>'
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="page"'
            f'{" style=width:%dpx"%width if width else ""}><div class="hd"><b>{title}</b><span>{desc}</span></div>'
            f'<div class="row">{chev.join(steps_html)}</div></div></body></html>')

PRICE = {'鉛筆':10,'原子筆':15,'蠟筆':10,'水彩筆':25,'尺':15,'剪刀':30,'筆記本':30,'作業簿':25,'便條紙':20,'三角板':20,'鋼筆':40}
ROW1 = ['鉛筆','原子筆','蠟筆','水彩筆']
ROW2 = ['尺','筆記本','作業簿','便條紙']
T_START = [('買 2 枝', '鉛筆', False), ('＋ 1 本', '筆記本', False)]
T_HALF = [('買 2 枝', '鉛筆', True), ('＋ 1 本', '筆記本', False)]
T_DONE = [('買 2 枝', '鉛筆', True), ('＋ 1 本', '筆記本', True)]

# ---------------------------------------------------------------- A
def scene_a(cust_x, cust_y, bk_items, st1, st2, extra='', counter_items=(), basket_on_counter=False, flip=False):
    s = ['<div class="wall" style="height:150px"></div><div class="floor" style="top:150px"></div>',
         '<div class="sign" style="left:500px;top:14px">✏️ 小學堂文具店</div>']
    s.append(shelf(ST, 16, 100, [ROW1, ROW2], PRICE, {**st1, **st2}, rowh=128, title=None))
    s.append(door(24, 408))
    s.append(clerk(560, 118, 150))
    s.append(register(650, 262))
    s.append(counter(470, 290, 280, 100, counter_items, prices=[PRICE[i] for i in counter_items] if counter_items else None))
    s.append(person(cust_x, cust_y, 160, 1, flip=flip))
    if not basket_on_counter:
        s.append(basket(cust_x + 62, cust_y + 78, 64, bk_items, isz=30))
    s.append(extra)
    return ''.join(s)

def make_A():
    p1 = scene_a(100, 400, [], {}, {}, extra=
        route('M150 530 C 200 470, 140 440, 150 420') .replace('M150 530', 'M170 545') +
        task(250, 468, T_START) +
        lbl(250, 420, '① 先到架子找東西', extra='background:#16a34a'))
    # A1 route: from door through shelf to counter
    p1 = scene_a(70, 410, [], {}, {}, extra=
        route('M120 560 C 200 520, 260 470, 330 440 S 430 440, 520 400') +
        task(16, 14, T_START) +
        lbl(20, 372, '走進店裡', extra='background:#16a34a'))
    p2 = scene_a(250, 410, ['鉛筆', '鉛筆'], {'鉛筆': 'hl'}, {'筆記本': ''}, extra=
        hand(318, 82) +
        route('M300 150 C 330 250, 340 340, 330 470', color='#ea580c', w=6, dash='3 10') +
        lbl(350, 392, '放進籃子', extra='background:#ea580c') +
        task(16, 14, T_HALF) +
        f'<div class="btn" style="left:560px;top:470px">去結帳 ➜</div>')
    p3 = scene_a(540, 405, [], {}, {}, basket_on_counter=True, counter_items=['鉛筆', '鉛筆', '筆記本'], flip=False, extra=
        '<div class="bubble" style="left:16px;top:14px">籃子交給店員 ➜</div>' +
        '<div class="bubble" style="left:300px;top:60px">一樣一樣嗶～ ♪</div>' + f'<div class="bubble" style="left:560px;top:60px;border-color:#2563eb;color:#1d4ed8">一共 ？元</div>')
    # cust at counter should be left of counter
    return page('A　一個畫面：貨架＋櫃台', '顧客提著籃子，在同一個畫面裡走：進門 → 架子 → 櫃台',
        [step(1, '進門', '左邊是架子、右邊是櫃台；藍色虛線告訴學生「接下來要走哪」。', p1),
         step(2, '挑選，放進籃子', '點架子上的東西，會飛進籃子。任務卡打勾；都放好才出現「去結帳」。', p2),
         step(3, '走到櫃台結帳', '顧客走到櫃台，籃子的東西一樣一樣放上桌，店員嗶一聲。接下來沿用現在的算錢→付錢。', p3)])

# ---------------------------------------------------------------- B
def make_B():
    # 場景 1：大貨架
    sh = shelf(ST, 24, 70, [ROW1, ROW2], PRICE, {'鉛筆': 'hl'}, rowh=150, cols=4, size=84, iw=112)
    sh = sh.replace('width:68px', 'width:84px')
    p1 = ('<div class="wall" style="height:70px"></div><div class="sign" style="left:240px;top:16px">✏️ 小學堂文具店 · 貨架區</div>'
          + sh +
          task(500, 90, T_START, title='任務卡', w=240) +
          hand(122, 160) +
          '<div class="a" style="left:0;right:0;bottom:0;height:150px;background:#fde7c7;border-top:5px solid #9a6330"></div>' +
          basket(40, 436, 150, [], isz=44, label='我的籃子（空的）') +
          '<div class="a" style="left:230px;top:450px;font-size:22px;font-weight:bold;color:#7c2d12;width:260px;line-height:1.4">點東西，放進籃子<br>每點一下 ＋1 個</div>' +
          '<div class="btn g" style="left:520px;top:470px">去結帳 ➜</div>')
    p1b = p1.replace(basket(40, 436, 150, [], isz=44, label='我的籃子（空的）'), basket(40, 436, 150, ['鉛筆', '鉛筆'], isz=44, label='籃子：鉛筆 × 2'))
    p1b = p1b.replace(task(500, 90, T_START, title='任務卡', w=240), task(500, 90, T_HALF, title='任務卡', w=240))
    p1b = p1b.replace(item(ST, '筆記本', 30, 24 + 8 + 1 * 112, 70 + 8 + 150, '', 84), item(ST, '筆記本', 30, 24 + 8 + 1 * 112, 70 + 8 + 150, '', 84))
    # 過場
    p2 = ('<div class="wall" style="height:230px;background:linear-gradient(#cfe8fb,#e8f3fc)"></div><div class="floor" style="top:230px;background:repeating-linear-gradient(90deg,#f1dcb8 0 60px,#ead2a8 60px 62px)"></div>'
          '<div class="a" style="left:20px;top:30px;width:240px;height:200px;background:#f8ecd2;border:5px solid #9a6330;border-radius:6px;opacity:.55;text-align:center;font-size:26px;font-weight:bold;color:#7c2d12;padding-top:70px">貨架區<br>（離開了）</div>'
          '<div class="sign" style="left:450px;top:20px">結帳櫃台</div>' +
          counter(470, 160, 260, 90) + clerk(560, 20, 140) +
          person(60, 330, 200, 1) + basket(150, 410, 90, ['鉛筆', '鉛筆', '筆記本'], isz=34) +
          route('M270 450 C 330 450, 380 430, 460 420', w=8, color='#2563eb') +
          '<div class="bubble" style="left:230px;top:300px;font-size:28px">走去櫃台 ➜</div>' +
          '<div class="a" style="left:0;right:0;bottom:12px;text-align:center;font-size:19px;color:#475569">（短短 1 秒的過場動畫，不用操作）</div>')
    # 場景 2：櫃台
    p3 = ('<div class="wall" style="height:175px"></div><div class="floor" style="top:175px;background:repeating-linear-gradient(90deg,#c7d6f4 0 56px,#b9c9ee 56px 58px)"></div>'
          '<div class="sign" style="left:270px;top:14px">✏️ 小學堂文具店</div>' +
          clerk(300, 50, 150) + register(450, 168) +
          '<div class="a" style="left:60px;top:200px;width:640px;height:150px;background:#dbe5ff;border:3px solid #6477b0;clip-path:polygon(6% 0,94% 0,100% 100%,0 100%)"></div>' +
          ''.join(f'<img class="a" style="left:{150+i*130}px;top:215px;width:96px;z-index:4" src="{ST}{n}.png"><div class="a" style="left:{150+i*130-4}px;top:300px;width:104px;text-align:center"><span class="tag">{pr} 元</span></div>' for i, (n, pr) in enumerate([('鉛筆', 10), ('鉛筆', 10)])) +
          f'<div class="a" style="left:410px;top:215px;width:96px;z-index:4;opacity:.25;filter:grayscale(1)"><img src="{ST}筆記本.png" style="width:96px"></div>' +
          '<div class="bubble" style="left:520px;top:225px;border-color:#2563eb;color:#1d4ed8">嗶！</div>' +
          basket(20, 380, 140, ['筆記本'], isz=44, label='籃子裡還有 1 樣') +
          '<div class="a" style="left:180px;top:390px;font-size:21px;font-weight:bold;line-height:1.45;color:#334155;width:300px">店員一樣一樣拿出來<br>嗶一聲、放上櫃台<br>再用現在的方式：算錢 → 付錢</div>' +
          '<div class="a" style="left:520px;top:400px;width:210px;height:140px;background:#fffbe6;border:3px solid #f59e0b;border-radius:12px;padding:10px;font-size:20px;font-weight:bold;line-height:1.5">收據<br>鉛筆 10 元<br>鉛筆 10 元<br><span style="color:#94a3b8">筆記本 ？元</span></div>')
    return page('B　兩個場景：貨架區 → 櫃台', '先專心挑東西（貨架大畫面），按「去結帳」過場，再到櫃台（沿用現在的櫃台）',
        [step(1, '場景 1：貨架區', '全畫面是貨架，沒有櫃台。底部籃子＋任務卡；沒放好時「去結帳」是灰的。', p1b),
         step(2, '過場：走去櫃台', '按「去結帳」後，顧客提著籃子走到櫃台（約 1 秒），告訴學生「換地方了」。', p2),
         step(3, '場景 2：櫃台', '沿用現有櫃台版面，托盤換成籃子；店員一樣一樣嗶，之後算錢、付錢、找錢不變。', p3)])

# ---------------------------------------------------------------- C
def minimap(cust, route_d, hot=None, basket_n=0, entrycap=True):
    s = ['<div class="a" style="left:0;top:0;width:760px;height:570px;background:repeating-linear-gradient(90deg,#f1dcb8 0 50px,#ead2a8 50px 52px)"></div>',
         '<div class="a" style="left:18px;top:14px;right:18px;height:30px;background:#1e3a8a;color:#fff;font-size:20px;font-weight:bold;text-align:center;line-height:30px;border-radius:6px">✏️ 小學堂文具店（俯視）</div>']
    # shelves rows
    rows = [('寫的筆', ['鉛筆', '原子筆', '蠟筆'], 70), ('本子紙張', ['筆記本', '作業簿', '便條紙'], 215), ('小工具', ['尺', '剪刀', '三角板'], 360)]
    for name, its, y in rows:
        c = '#f59e0b' if hot == name else '#9a6330'
        glow = 'box-shadow:0 0 0 6px rgba(245,158,11,.45);' if hot == name else ''
        s.append(f'<div class="a" style="left:40px;top:{y}px;width:420px;height:110px;background:#f8ecd2;border:5px solid {c};border-radius:8px;{glow}"></div>')
        for i, it in enumerate(its):
            s.append(f'<img class="a" style="left:{58+i*132}px;top:{y+8}px;width:62px" src="{ST}{it}.png">')
        s.append(f'<div class="a" style="left:48px;top:{y+86}px;width:404px;text-align:center;font-size:19px;font-weight:bold;color:#7c2d12">{name}</div>')
    # counter
    s.append('<div class="a" style="left:520px;top:70px;width:200px;height:300px;background:#dbe5ff;border:4px solid #6477b0;border-radius:10px"></div>')
    s.append(clerk(560, 100, 120))
    s.append('<div class="a" style="left:520px;top:300px;width:200px;text-align:center;font-size:24px;font-weight:bold;color:#1e3a8a">結帳櫃台</div>')
    s.append(register(590, 250))
    s.append(f'<div class="a" style="left:20px;top:495px;width:100px;height:70px;background:#a16207;border:4px solid #713f12;border-radius:8px 8px 0 0;color:#fff;font-weight:bold;text-align:center;font-size:20px;padding-top:20px">入口</div>')
    s.append(route(route_d, w=7))
    # customer dot
    cx, cy = cust
    s.append(person(cx - 30, cy - 78, 120, 1))
    if basket_n:
        s.append(f'<div class="dot" style="left:{cx+14}px;top:{cy-30}px;width:44px;height:44px;font-size:22px;z-index:25;border:3px solid #fff">🧺{basket_n}</div>')
    return ''.join(s)

def make_C():
    p1 = minimap((80, 460), 'M110 470 C 250 480, 470 460, 480 330 S 480 190, 470 175', hot=None) + \
         task(480, 452, T_START, w=260) + \
         lbl(130, 440, '點要去的那一排', extra='background:#16a34a;font-size:22px') + hand(250, 85)
    # p2 zoom into 寫的筆
    sh = shelf(ST, 24, 90, [['鉛筆', '原子筆', '蠟筆']], PRICE, {'鉛筆': 'hl'}, rowh=160, cols=3, size=100, iw=140)
    sh = sh.replace('width:68px', 'width:100px')
    sh = sh.replace('class="it', 'class="it" ').replace('width:96px', 'width:140px')
    p2 = ('<div class="wall" style="height:70px"></div>'
          '<div class="a" style="left:0;right:0;top:70px;bottom:0;background:#fff7ea"></div>'
          '<div class="sign" style="left:200px;top:14px">貨架：寫的筆</div>'
          '<div class="btn" style="left:560px;top:12px;font-size:20px;background:#64748b;box-shadow:0 4px 0 #334155;padding:4px 14px">◀ 回走道</div>' +
          sh +
          task(480, 110, T_START, w=250) +
          hand(98, 190) +
          '<div class="a" style="left:0;right:0;bottom:0;height:170px;background:#fde7c7;border-top:5px solid #9a6330"></div>' +
          basket(30, 395, 150, ['鉛筆', '鉛筆'], isz=44, label='籃子：鉛筆 × 2') +
          '<div class="a" style="left:230px;top:440px;font-size:22px;font-weight:bold;color:#7c2d12;line-height:1.5">這一排挑好了，<br>按「回走道」</div>')
    p3 = minimap((330, 240), 'M360 250 C 440 250, 470 220, 500 200', hot=None, basket_n=3) + \
         task(480, 452, T_DONE, w=260) + \
         '<div class="btn" style="left:520px;top:385px;font-size:24px">去結帳 ➜</div>'
    return page('C　店內俯視小地圖', '像看地圖：點走道上的某一排 → 放大挑東西 → 回走道 → 去櫃台',
        [step(1, '走進店，看地圖', '從上面往下看整間店。三排架子各寫一個類別；點哪排，人就走過去。', p1),
         step(2, '點進去，放大挑選', '放大成一排貨架，底部籃子。挑完按「回走道」，地圖上籃子角標會變成 3。', p2),
         step(3, '走去櫃台', '兩排都挑完，按「去結帳」，人在地圖上走到櫃台，之後接現有的結帳流程。', p3)])

# ---------------------------------------------------------------- D
def aisle(seg, items, hl, basket_items, extra='', pos='1 / 3', segname=''):
    n = len(items)
    iw = 150
    sh = shelf(ST, 70, 85, [items], PRICE, {x: 'hl' for x in hl}, rowh=170, cols=n, size=104, iw=iw)
    sh = sh.replace('width:68px', 'width:104px').replace('width:96px', f'width:{iw}px')
    sh = sh.replace('<div class="board"', '<div class="board"')
    # 第二層（背面小貨架）
    return ('<div class="wall" style="height:70px;background:#cfe8fb"></div>'
            '<div class="a" style="left:0;right:0;top:70px;height:330px;background:#fff7ea"></div>'
            f'<div class="sign" style="left:250px;top:14px">✏️ 走道 {pos}　{segname}</div>' +
            sh +
            '<div class="a" style="left:6px;top:200px;width:56px;height:90px;background:#fb923c;border-radius:14px;color:#fff;font-size:42px;text-align:center;line-height:84px;box-shadow:0 4px 0 #9a3412">◀</div>'
            '<div class="a" style="right:6px;top:200px;width:56px;height:90px;background:#fb923c;border-radius:14px;color:#fff;font-size:42px;text-align:center;line-height:84px;box-shadow:0 4px 0 #9a3412">▶</div>' +
            '<div class="a" style="left:0;right:0;top:330px;height:60px;display:flex;justify-content:center;gap:12px;align-items:center">' +
            ''.join(f'<div style="width:{26 if i+1==int(pos[0]) else 16}px;height:16px;border-radius:8px;background:{"#ea580c" if i+1==int(pos[0]) else "#cbd5e1"}"></div>' for i in range(3)) + '</div>' +
            '<div class="a" style="left:0;right:0;bottom:0;height:170px;background:#fde7c7;border-top:5px solid #9a6330"></div>' +
            basket(24, 400, 150, basket_items, isz=44, label='我的籃子') + extra)

def make_D():
    t = lambda parts: task(220, 428, parts, w=300)
    p1 = aisle(1, ROW1[:4][:3] + ['橡皮擦'] if False else ['鉛筆', '原子筆', '蠟筆'], ['鉛筆'], [], pos='1 / 3', segname='寫的筆',
               extra=t(T_START) + hand(130, 150) +
               '<div class="a" style="left:230px;top:500px;font-size:19px;color:#7c2d12;font-weight:bold">點東西放進籃子；往右滑看下一段 ▶</div>' +
               '<div class="btn g" style="left:570px;top:430px;font-size:22px">去結帳 ➜</div>')
    p2 = aisle(2, ['筆記本', '作業簿', '便條紙'], ['筆記本'], ['鉛筆', '鉛筆', '筆記本'], pos='2 / 3', segname='本子紙張',
               extra=t(T_DONE) + hand(130, 150) +
               '<div class="a" style="left:230px;top:500px;font-size:19px;color:#7c2d12;font-weight:bold">任務都好了，往右走到最後去結帳 ▶</div>' +
               '<div class="btn g" style="left:570px;top:430px;font-size:22px">去結帳 ➜</div>')
    # 第 3 段：走道盡頭＝櫃台
    p3 = ('<div class="wall" style="height:70px"></div>'
          '<div class="a" style="left:0;right:0;top:70px;height:330px;background:#fff7ea"></div>'
          '<div class="sign" style="left:250px;top:14px">走道 3 / 3　結帳櫃台</div>' +
          shelf(ST, 40, 100, [['尺', '剪刀', '三角板']], PRICE, {}, rowh=170, cols=3, size=70, iw=96).replace('width:68px', 'width:70px').replace('class="it', 'class="it dim ') +
          '<div class="a" style="left:400px;top:90px;width:340px;height:310px;background:#cfe8fb;border-left:4px solid #6477b0"></div>' +
          clerk(520, 70, 150) + register(640, 190) + counter(420, 220, 320, 120, ['鉛筆', '鉛筆', '筆記本'], prices=[10, 10, 30]) +
          '<div class="a" style="left:6px;top:200px;width:56px;height:90px;background:#fb923c;border-radius:14px;color:#fff;font-size:42px;text-align:center;line-height:84px;box-shadow:0 4px 0 #9a3412">◀</div>' +
          person(250, 215, 170, 1, flip=False) +
          '<div class="a" style="left:0;right:0;bottom:0;height:170px;background:#fde7c7;border-top:5px solid #9a6330"></div>' +
          basket(24, 400, 150, [], isz=44, label='籃子已經交給店員') +
          '<div class="bubble" style="left:540px;top:70px;border-color:#2563eb;color:#1d4ed8;font-size:24px">一樣一樣嗶～ ♪</div>' +
          '<div class="a" style="left:230px;top:440px;font-size:22px;font-weight:bold;color:#7c2d12;line-height:1.5">走到走道最後面，<br>就是櫃台，接著算錢、付錢</div>')
    return page('D　走道橫向捲動', '像走在走道上：左右按 ◀ ▶（或滑動）看下一段架子，底部籃子固定，最後一段是櫃台',
        [step(1, '第 1 段：寫的筆', '一次只看 3 樣東西，東西放大；底部籃子與任務卡固定不動。', p1),
         step(2, '往右走：第 2 段', '籃子累積東西。圓點告訴學生「走到第幾段」。「去結帳」要等任務完成才亮。', p2),
         step(3, '最後一段：櫃台', '走道盡頭自然接到櫃台，店員嗶東西；之後沿用現有算錢→付錢。', p3)])

# ---------------------------------------------------------------- 糖果店
def jar(x, y, name, price, n=7, w=170, h=190):
    import random
    rnd = random.Random(hash(name) % 1000)
    inner = ''
    for i in range(n):
        ix = rnd.randint(8, w - 66); iy = rnd.randint(int(h * 0.30), h - 66)
        inner += f'<img class="a" style="left:{ix}px;top:{iy}px;width:56px;transform:rotate({rnd.randint(-30,30)}deg)" src="{CD}{name}.png">'
    return (f'<div class="a" style="left:{x}px;top:{y}px;width:{w}px;height:{h+78}px">'
            f'<div class="a" style="left:22px;top:0;width:{w-44}px;height:18px;background:#e11d48;border-radius:8px"></div>'
            f'<div class="a" style="left:0;top:14px;width:{w}px;height:{h}px;border:5px solid rgba(100,116,139,.55);border-radius:18px 18px 28px 28px;background:rgba(226,240,255,.55);overflow:hidden">{inner}</div>'
            f'<div class="a" style="left:0;top:{h+22}px;width:{w}px;text-align:center"><div class="nm" style="font-size:20px">{name}</div><span class="tag" style="font-size:18px;line-height:26px">1 個 {price} 元</span></div></div>')

def make_candy():
    P = {'棒棒糖': 5, '大顆糖果': 10, '巧克力': 20, '餅乾': 15, '仙貝': 10, '蝴蝶餅': 15, '爆米花': 25, '冰淇淋': 30, '杯子蛋糕': 35}
    s = ['<div class="a" style="left:0;top:0;right:0;height:120px;background:#fde7f3"></div>',
         '<div class="a" style="left:0;right:0;top:120px;bottom:0;background:#fff7ea"></div>',
         '<div class="a" style="left:420px;top:18px;width:440px;text-align:center;background:#be185d;color:#fff;font-size:34px;font-weight:bold;padding:6px;border-radius:12px;border:4px solid #fbcfe8">🍬 糖果餅乾小舖</div>']
    # 上層：糖果罐
    s.append('<div class="a" style="left:40px;top:140px;width:1200px;height:316px;background:#fbe2c4;border:6px solid #9a6330;border-radius:10px"></div>')
    for i, (n, pr) in enumerate([('棒棒糖', 5), ('大顆糖果', 10), ('巧克力', 20), ('蝴蝶餅', 15), ('仙貝', 10)]):
        s.append(jar(68 + i * 236, 150, n, pr, n=7))
    s.append('<div class="board" style="left:40px;top:450px;width:1200px;height:18px"></div>')
    # 下層：包裝零食架
    s.append('<div class="a" style="left:40px;top:500px;width:760px;height:260px;background:#fbe2c4;border:6px solid #9a6330;border-radius:10px"></div>')
    for i, n in enumerate(['餅乾', '爆米花', '冰淇淋', '杯子蛋糕']):
        x = 70 + i * 185
        s.append(f'<div class="it" style="left:{x}px;top:520px;width:170px"><img src="{CD}{n}.png" style="width:116px;height:116px;margin-bottom:10px"><div class="nm" style="font-size:20px">{n}</div><span class="tag" style="font-size:18px;line-height:26px">{P[n]} 元</span></div>')
    s.append('<div class="board" style="left:40px;top:748px;width:760px;height:16px"></div>')
    # 右下：籃子與任務
    s.append('<div class="a" style="left:830px;top:500px;width:410px;height:260px;background:#fde7c7;border:5px solid #9a6330;border-radius:14px"></div>')
    s.append(basket(860, 580, 150, ['棒棒糖', '棒棒糖', '巧克力'], base=CD, isz=44, label='棒棒糖 ×2、巧克力 ×1'))
    s.append(task(850, 530, [('買 2 支', '棒棒糖', True), ('＋ 1 條', '巧克力', True)], title='任務卡').replace(f'{ST}', CD).replace('white-space:nowrap', 'white-space:normal;font-size:20px'))
    s.append('<div class="btn" style="left:1040px;top:640px;font-size:28px">去結帳 ➜</div>')
    s.append(hand(150, 235))
    s.append('<div class="bubble" style="left:60px;top:430px;font-size:18px;z-index:30;border-color:#ea580c;color:#c2410c">點一下罐子 ＝ 拿 1 個，放進籃子</div>')
    s.append('<div class="a" style="left:60px;top:772px;font-size:18px;color:#475569">糖果用「罐子」、餅乾零食用「架子」；一罐裡的東西同價，標價牌寫「1 個幾元」</div>')
    inner = ''.join(s)
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}body{{background:#fff7ea}}</style></head><body>'
            f'<div style="position:relative;width:1280px;height:800px;overflow:hidden">{inner}</div></body></html>')
    return html

def main():
    pages = {'A_同一畫面': make_A(), 'B_兩個場景': make_B(), 'C_店內地圖': make_C(), 'D_走道捲動': make_D()}
    for k, h in pages.items():
        open(f'{HERE}/{k}.html', 'w', encoding='utf-8').write(h)
    open(f'{HERE}/糖果店貨架.html', 'w', encoding='utf-8').write(make_candy())
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get('CHROME_PATH') or None)
        for k in list(pages) + ['糖果店貨架']:
            w = 1280 if k == '糖果店貨架' else 2420
            h = 800 if k == '糖果店貨架' else 820
            pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2 if k == '糖果店貨架' else 1.3)
            pg.goto(f'file://{HERE}/{k}.html'); pg.wait_for_timeout(500)
            pg.screenshot(path=f'{HERE}/{k}.png', full_page=True)
            print('shot', k)
        b.close()

if __name__ == '__main__':
    main()
