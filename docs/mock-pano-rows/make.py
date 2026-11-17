"""自助選購店第六輪模擬圖（使用者 2026-11-17）：
① 進門全景改成多排並列、有角度與前後（A～D 四種）
② 架上加放其他價位的商品、全部縮小，呈現琳瑯滿目（走道 E、F 兩種）
③ 賣吃的店（糖果餅乾店）改用托盤，進門時空手（G）
用法：python make.py <後端路徑>  → 產生 *.html，再 node shot.js 截圖
"""
import sys, json, pathlib, html as H

BE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/user/worksheet-backend')
IMG = BE / 'backend/assets/images'
GAME = BE / 'backend/assets/game'
OUT = pathlib.Path(__file__).parent
LIB = json.load(open(BE / 'backend/library.json'))['themes']


def items(theme):
    out = []
    for i in LIB[theme]['items']:
        p = i.get('default_price') or i.get('worksheet_price') or i.get('price_min') or 0
        out.append((i['name'], (IMG / i['file']).as_uri(), p))
    return out


MAIN = items('遊戲_玩具店')                                   # 這家店本來的商品（99 元以內）
EXTRA = items('玩具店') + items('懷舊玩具') + items('玩具車')   # 加放的其他價位（三位數）
CANDY = items('遊戲_糖果餅乾店')
CANDY_X = items('甜點店')
g = lambda n: (GAME / n).as_uri()

CSS = """
@font-face{font-family:x;src:local('Noto Sans CJK TC')}
*{box-sizing:border-box}body{margin:0;font-family:'Noto Sans CJK TC',sans-serif;background:#fff7ed}
.stage{position:relative;width:1100px;height:660px;margin:0;overflow:hidden;border:6px solid #7c4a1e;border-radius:18px;background:linear-gradient(#fde68a 0 38%,#bfdbfe 38% 100%)}
.cap{position:absolute;left:16px;top:12px;z-index:50;background:#1e3a8a;color:#fff;font-weight:900;font-size:24px;padding:4px 16px;border-radius:12px}
.note{position:absolute;right:16px;top:12px;z-index:50;background:#fff;border:3px solid #f97316;color:#9a3412;font-weight:800;font-size:17px;padding:4px 12px;border-radius:12px;max-width:520px}
.it{display:inline-flex;flex-direction:column;align-items:center;margin:0 1px}
.it img{width:var(--s,34px);height:var(--s,34px);object-fit:contain}
.it b{font-size:calc(var(--s,34px)*.30);color:#4c1d95;background:#fff;border:1.5px solid #a78bfa;border-radius:8px;padding:0 4px;line-height:1.25;white-space:nowrap}
.tier{display:flex;justify-content:center;align-items:flex-end;padding:2px 4px 0;border-bottom:7px solid #ef4444;min-height:calc(var(--s,34px) + 18px)}
.shelf{position:absolute;background:#fffbeb;border:5px solid #2563eb;border-radius:8px 8px 0 0;box-shadow:0 10px 0 #1e40af}
.shelf .lab{position:absolute;left:50%;top:-24px;transform:translateX(-50%);background:#7c3aed;color:#fff;font-weight:900;font-size:16px;padding:1px 12px;border-radius:10px;white-space:nowrap;z-index:2}
.cus{position:absolute;z-index:40}
.clerk{position:absolute;z-index:20}
.counter{position:absolute;background:repeating-conic-gradient(#fde047 0 25%,#60a5fa 0 50%) 0 0/28px 28px;border:4px solid #1e40af;border-radius:8px;color:#fff;font-weight:900;text-align:center;text-shadow:0 2px 3px #000;font-size:18px}
.door{position:absolute;width:62px;height:112px;background:#92400e;border:5px solid #78350f;border-radius:6px 6px 0 0}
.door::after{content:'';position:absolute;left:12px;top:12px;width:28px;height:36px;background:#bae6fd}
.plant{position:absolute;z-index:30}
"""


def tier(lst, s):
    return f'<div class="tier" style="--s:{s}px">' + ''.join(
        f'<span class="it"><img src="{u}"><b>{p} 元</b></span>' for n, u, p in lst) + '</div>'


def shelf(lab, rows, s, style):
    return f'<div class="shelf" style="{style}"><div class="lab">{H.escape(lab)}</div>' + ''.join(tier(r, s) for r in rows) + '</div>'


def mix(a, b, k):      # 主商品與加放商品交錯
    out, ia, ib = [], iter(a), iter(b)
    for i in range(k):
        src = ib if i % 3 == 2 else ia
        try:
            out.append(next(src))
        except StopIteration:
            out.append(next(ia if src is ib else ib))
    return out


def page(name, body, cap, note):
    doc = f'<!doctype html><meta charset=utf-8><style>{CSS}</style><div class="stage">{body}<div class="cap">{cap}</div><div class="note">{note}</div></div>'
    (OUT / f'{name}.html').write_text(doc, encoding='utf-8')


def people(cx=150, hand=None):
    h = f'<img class="cus" src="{g("customer_walk_1.png")}" style="left:{cx}px;bottom:-30px;height:230px">'
    h += f'<div class="door" style="left:24px;bottom:0"></div>'
    for i, x in enumerate((520, 980)):
        h += f'<img class="plant" src="{g(f"plant_{i + 1}.png")}" style="left:{x}px;bottom:4px;height:96px">'
    return h


R1 = mix(MAIN[:4], EXTRA[:6], 7); R2 = mix(MAIN[4:8], EXTRA[6:12], 7); R3 = mix(MAIN[8:], EXTRA[12:], 7)

# A：斜角多排（3/4 視角，三排架子斜斜往後排）
b = '<div style="position:absolute;inset:0;perspective:900px;perspective-origin:20% 30%">'
for k, (lab, rows, x, y, z) in enumerate((('走道 3　大玩具', [R3, R1], 470, 60, -260), ('走道 2　動動玩具', [R2, R3], 300, 190, -130), ('走道 1　小玩具', [R1, R2], 130, 330, 0))):
    b += shelf(lab, rows, 30, f'left:{x}px;top:{y}px;width:520px;transform:rotateY(30deg) translateZ({z}px);transform-origin:0 0;z-index:{10 + k}')
b += '</div>'
b += f'<img class="clerk" src="{g("clerk_1.png")}" style="right:70px;top:150px;height:150px"><div class="counter" style="right:40px;top:290px;width:210px;height:44px;line-height:36px;z-index:21">櫃台</div>'
page('A_斜角多排', b + people(), 'A　斜角多排', '從門口斜斜看進去，三排架子一排比一排遠；最遠的櫃台在右後方')

# B：正面前後排（後排小、前排大，中間是走道）
b = ''
for k, (lab, rows, s, w, top, left) in enumerate((('走道 3　大玩具', [R3, R1], 22, 560, 60, 270), ('走道 2　動動玩具', [R2, R3], 27, 700, 175, 200), ('走道 1　小玩具', [R1, R2], 33, 860, 315, 120))):
    b += shelf(lab, rows, s, f'left:{left}px;top:{top}px;width:{w}px;z-index:{10 + k}')
b += f'<img class="clerk" src="{g("clerk_1.png")}" style="right:40px;top:40px;height:110px"><div class="counter" style="right:20px;top:140px;width:170px;height:36px;line-height:28px">櫃台</div>'
page('B_前後排', b + people(), 'B　前後排', '正面看，三排架子由後往前一排比一排大，排和排中間就是走道')

# C：走廊兩側（一點透視，左右兩面牆是架子，櫃台在盡頭）
b = '<div style="position:absolute;inset:0;perspective:700px;perspective-origin:50% 40%">'
b += shelf('走道 1　小玩具', [R1, R2, R3], 30, 'left:60px;top:90px;width:520px;transform:rotateY(62deg);transform-origin:0 50%;z-index:10')
b += shelf('走道 2　動動玩具', [R2, R3, R1], 30, 'right:60px;top:90px;width:520px;transform:rotateY(-62deg);transform-origin:100% 50%;z-index:10')
b += '</div>'
b += f'<img class="clerk" src="{g("clerk_1.png")}" style="left:500px;top:120px;height:120px"><div class="counter" style="left:470px;top:230px;width:170px;height:36px;line-height:28px;z-index:25">櫃台</div>'
page('C_走廊兩側', b + people(cx=380), 'C　走廊兩側', '站在走廊口看，左右兩面都是架子，往盡頭變小；正前方盡頭是櫃台')

# D：俯看島型架（從斜上方看，2×2 座架子，看得到架頂與走道地板）
b = '<div style="position:absolute;left:0;right:0;top:40px;bottom:0;background:repeating-linear-gradient(90deg,#dbeafe 0 60px,#bfdbfe 60px 120px)"></div>'
pos = ((150, 70, '走道 1　小玩具', [R1, R2]), (560, 70, '走道 2　動動玩具', [R2, R3]), (110, 300, '走道 3　大玩具', [R3, R1]), (520, 300, '走道 4　玩具車', [R2, R1]))
for k, (x, y, lab, rows) in enumerate(pos):
    b += f'<div style="position:absolute;left:{x}px;top:{y}px;width:400px;height:28px;background:#93c5fd;border:4px solid #1e40af;border-bottom:none;transform:skewX(-35deg);transform-origin:0 100%;z-index:{10 + k}"></div>'
    b += shelf(lab, rows, 28, f'left:{x}px;top:{y + 28}px;width:400px;z-index:{10 + k}')
b += f'<img class="clerk" src="{g("clerk_1.png")}" style="right:30px;top:60px;height:110px"><div class="counter" style="right:16px;top:160px;width:140px;height:36px;line-height:28px;z-index:30">櫃台</div>'
page('D_俯看島型', b + people(cx=760), 'D　俯看島型架', '從斜上方看，架子一座一座像小島，看得到架頂和中間的走道地板')

# E：走道內，全部縮小、三層、主商品和三位數商品混放
AIS = '.stage{background:#dbeafe}.big{position:absolute;left:90px;right:90px;top:70px;bottom:120px;background:#fffbeb;border:7px solid #2563eb;border-radius:10px;padding:26px 14px 0}.big .tier{border-bottom-width:9px;justify-content:space-around}.foot{position:absolute;left:0;right:0;bottom:0;height:110px;background:#fde68a;border-top:5px solid #f59e0b}'
def aisle(name, cap, note, body, extra=''):
    (OUT / f'{name}.html').write_text(f'<!doctype html><meta charset=utf-8><style>{CSS}{AIS}{extra}</style><div class="stage">{body}<div class="cap">{cap}</div><div class="note">{note}</div></div>', encoding='utf-8')
rows = [mix(MAIN[0:4], EXTRA[0:4], 7), mix(MAIN[4:8], EXTRA[4:8], 7), mix(MAIN[8:12], EXTRA[8:12], 7)]
e = '<div class="big">' + ''.join(tier(r, 62) for r in rows) + '</div>'
e += f'<div class="foot"><img src="{g("plant_1.png")}" style="display:none"></div>'
aisle('E_走道全部縮小', 'E　全部縮小、三層', '每層 7 樣、一段 21 樣；三位數的玩具（積木 250 元…）和原本的混在一起，大小一樣', e)

# F：主商品照原大小在中間兩層，最上層與兩側塞滿小一號的三位數商品
f = '<div class="big" style="padding-top:20px">' + tier(EXTRA[:11], 40) + tier(MAIN[0:4] + EXTRA[11:13], 70) + tier(MAIN[4:8] + EXTRA[13:15], 70) + '</div>'
f += '<div class="foot"></div>'
aisle('F_加放的較小', 'F　加放的小一號', '最上層一排小小的三位數玩具；下面兩層是原本的商品，旁邊也塞一兩樣較貴的', f)

# G：糖果餅乾店走道，底部改托盤；全景顧客空手
TR = '.tray{position:absolute;left:40px;bottom:18px;width:300px;height:74px;border-radius:20px;background:#f8fafc;border:6px solid #e2e8f0;box-shadow:inset 0 6px 10px rgba(0,0,0,.1),0 10px 0 #cbd5e1;transform:rotateX(26deg);display:flex;align-items:center;justify-content:center;gap:4px}.tray img{height:54px}'
crow = [CANDY[0], CANDY[1], CANDY[4], CANDY_X[4], CANDY[8], CANDY[2], CANDY_X[3]]
crow2 = [CANDY[3], CANDY[5], CANDY_X[0], CANDY[6], CANDY[7], CANDY_X[1], CANDY_X[5]]
gg = '<div class="big" style="border-color:#db2777">' + tier(crow, 62).replace('#ef4444', '#f472b6') + tier(crow2, 62).replace('#ef4444', '#f472b6') + '</div>'
gg += f'<div class="foot" style="background:#fbcfe8;border-top-color:#db2777"><div class="tray"><img src="{CANDY[0][1]}"><img src="{CANDY[8][1]}"></div><div style="position:absolute;left:380px;top:28px;background:#cbd5e1;color:#fff;font-weight:900;font-size:26px;padding:8px 22px;border-radius:14px">去結帳 ➜</div></div>'
aisle('G_吃的店用托盤', 'G　糖果餅乾店：托盤', '賣吃的店底部改成托盤（同早餐店的托盤）；進門全景時顧客兩手空空', gg, TR)
print('ok', sorted(p.name for p in OUT.glob('*.html')))
