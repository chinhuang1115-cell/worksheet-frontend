# 「拿出指定的錢／湊到指定的錢」互動頁模擬圖（2026-11-11）：產生 A～E 五個 HTML，再用 Playwright 轉 PNG。
# 用法：python docs/mock-take-money/make.py <後端路徑>（字型用後端的芫荽體；錢幣畫法、配色照後端 coin.js 的 PV／coinSvg）
import base64, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).parent
BACK = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '../worksheet-backend')
FONT = BACK / 'backend/fonts/Iansui-Regular.ttf'
PV = {'f': dict(w=54, fill='#E1E4E8', edge='#222222', txt='5'), 'q': dict(w=66, fill='#F0D77E', edge='#5E4A12', txt='50'),
      'g': dict(w=96, hh=54, fill='#ecd0a6', edge='#8a4b12', txt='500'), 'h': dict(w=84, hh=48, fill='#f2b5bd', edge='#b3222f', txt='100'),
      't': dict(w=62, fill='#E1E4E8', edge='#222222', txt='10'), 'o': dict(w=48, fill='#D9A877', edge='#5A3518', txt='1')}


def coin(k, cls='', scale=1.0, style=''):
    c = PV[k]; w = c['w'] * scale; h = c.get('hh', c['w']) * scale
    if 'hh' in c:
        svg = (f'<svg viewBox="0 0 100 57"><rect x="3" y="3" width="94" height="51" rx="7" fill="{c["fill"]}" stroke="{c["edge"]}" stroke-width="4"/>'
               f'<rect x="9" y="9" width="82" height="39" rx="4" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="4 3" opacity=".75"/>'
               f'<text x="50" y="37" font-size="27" font-weight="800" text-anchor="middle" fill="{c["edge"]}" font-family="sans-serif">{c["txt"]}</text></svg>')
    else:
        fs = 38 if k in 'qt' else 46
        svg = (f'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="{c["fill"]}" stroke="{c["edge"]}" stroke-width="6"/>'
               f'<circle cx="50" cy="50" r="35" fill="none" stroke="{c["edge"]}" stroke-width="3" stroke-dasharray="4 5" opacity=".55"/>'
               f'<text x="50" y="63" font-size="{fs}" font-weight="800" text-anchor="middle" fill="{c["edge"]}" font-family="sans-serif">{c["txt"]}</text></svg>')
    return f'<span class="coin {cls}" style="width:{w:.0f}px;height:{h:.0f}px;{style}">{svg}</span>'


def ghost(k, scale=1.0):      # 虛線錢幣（強提示：還沒拿的位置）
    c = PV[k]; w = c['w'] * scale; h = c.get('hh', c['w']) * scale
    r = '8px' if 'hh' in c else '50%'
    return f'<span class="gh" style="width:{w:.0f}px;height:{h:.0f}px;border-radius:{r}">{c["txt"]}</span>'


def stack(k, n='', note=''):      # 錢盒裡的一疊（可一直拿；n＝剩幾個的小標）
    b = f'<i class="left">{n}</i>' if n else ''
    return f'<div class="stk">{coin(k, "s3", style="margin-top:6px")}{coin(k, "s2")}{coin(k, "s1")}{b}<em>{note}</em></div>'


def top(title):
    return (f'<div class="top"><span class="qn">第 1 題 / 5</span><span class="th">文具店</span><span class="pill">{title}</span><span class="stars">☆☆☆☆☆</span>'
            '<span class="sp"></span><span class="seg"><b class="on">強提示</b><b>弱提示</b><b>無提示</b></span></div>')


def col(name, k, body, extra=''):
    return f'<div class="pvcol {extra}"><h4>{coin(k, "ic", .42)}{name}</h4><div class="slot">{body}</div></div>'


CSS = f"""
@font-face{{font-family:Iansui;src:url('file://{FONT.resolve()}')}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Iansui,sans-serif;background:#fffaf0;color:#333;width:1180px;height:820px;overflow:hidden;position:relative}}
.top{{display:flex;align-items:center;gap:14px;padding:10px 26px;border-bottom:3px solid #fdba74;background:#fff}}
.qn{{font-size:15px;font-weight:800;color:#555}}.th{{font-size:18px;font-weight:800}}.pill{{padding:4px 16px;border-radius:99px;background:#ffedd5;color:#9a3412;font-size:21px;font-weight:800;border:2px solid #fdba74}}
.stars{{font-size:24px;letter-spacing:2px}}.sp{{flex:1}}.seg{{display:flex;border:3px solid #fdba74;border-radius:10px;overflow:hidden}}.seg b{{padding:6px 14px;font-size:18px;color:#9a3412;border-left:2px solid #fdba74}}.seg b:first-child{{border-left:0}}.seg b.on{{background:#ea580c;color:#fff}}
.main{{display:flex;gap:16px;padding:14px 26px}}
.card{{background:#fff;border:3px solid #fdba74;border-radius:20px;padding:14px}}
.left{{width:640px}}.right{{flex:1}}
.step{{border-color:#ea580c}}
.step h3{{font-size:25px;display:flex;align-items:center;gap:8px;margin-bottom:10px}}.step h3 i{{font-style:normal;background:#ea580c;color:#fff;border-radius:50%;width:34px;height:34px;display:inline-flex;align-items:center;justify-content:center;font-size:20px}}
.step.done{{border-color:#fed7aa;opacity:.6}}.step.done h3{{margin:0;font-size:20px}}.step.todo{{border-color:#e7e5e4;color:#a8a29e}}.step.todo h3{{margin:0;font-size:20px}}.step.todo h3 i{{background:#d6d3d1}}
.step+.step{{margin-top:10px}}
.tip{{font-size:21px;font-weight:700;color:#0369a1;background:#e0f2fe;border-radius:12px;padding:8px 12px;line-height:1.5}}
.goal{{display:flex;align-items:baseline;gap:8px;font-size:26px;font-weight:800;margin:4px 0 10px}}
.goal b{{font-family:sans-serif;font-size:58px;color:#c2410c;background:#fff7ed;border:3px solid #fdba74;border-radius:14px;padding:0 16px;line-height:1.25}}
.now{{display:flex;align-items:baseline;gap:8px;font-size:22px;margin-top:10px;color:#444}}.now b{{font-family:sans-serif;font-size:36px;color:#1d4ed8;border-bottom:3px solid #1d4ed8;padding:0 10px}}
.btn{{display:inline-block;margin-top:12px;background:#16a34a;color:#fff;font-size:24px;font-weight:800;border-radius:14px;padding:8px 26px}}.btn.off{{background:#d6d3d1}}
.coin{{display:inline-block;line-height:0;position:relative;flex:none}}.coin svg{{display:block;width:100%;height:100%}}
.coin.lock{{filter:grayscale(.55);opacity:.75}}
.coin.new{{box-shadow:0 0 0 4px #86efac;border-radius:50%}}.coin.new.bill{{border-radius:8px}}
.gh{{display:inline-flex;align-items:center;justify-content:center;border:3px dashed #9ca3af;color:#9ca3af;font-family:sans-serif;font-weight:800;font-size:20px;flex:none;background:#fafafa}}
.box{{border:3px dashed #fcd34d;border-radius:18px;background:#fffbeb;padding:8px 14px 10px;margin-bottom:12px}}
.box h5{{font-size:19px;color:#92400e;margin-bottom:4px}}
.stks{{display:flex;justify-content:space-around;align-items:flex-end}}
.stk{{position:relative;display:flex;flex-direction:column;align-items:center;padding-top:14px}}.stk .coin+.coin{{margin-top:-999px}}
.stk .s3,.stk .s2,.stk .s1{{display:block}}.stk .s2{{margin-top:-0px}}
.stk em{{font-style:normal;font-size:17px;color:#92400e;margin-top:4px;height:22px}}
.stk .left{{position:absolute;right:-14px;top:0;background:#dc2626;color:#fff;font-style:normal;font-family:sans-serif;font-weight:800;font-size:16px;border-radius:99px;padding:1px 8px;width:auto}}
.cols{{display:flex;gap:10px}}
.pvcol{{flex:1;border:3px solid #fdba74;border-radius:16px;background:#fff;min-height:330px;display:flex;flex-direction:column}}
.pvcol.focus{{border-color:#16a34a;box-shadow:0 0 0 4px #bbf7d0}}
.pvcol h4{{font-size:22px;text-align:center;padding:6px 0;background:#ffedd5;border-radius:12px 12px 0 0;color:#9a3412;display:flex;align-items:center;justify-content:center;gap:8px}}
.pvcol h4 .coin{{filter:grayscale(1) brightness(1.5) contrast(3)}}
.slot{{flex:1;display:flex;flex-wrap:wrap;gap:8px;align-content:flex-start;justify-content:center;padding:10px 6px}}
.chip{{text-align:center;font-size:19px;color:#0369a1;padding:4px 0 8px;font-weight:700}}
.foot{{position:absolute;left:26px;right:26px;bottom:10px;font-size:17px;color:#57534e;background:#f5f5f4;border-radius:10px;padding:6px 12px;line-height:1.45}}
.foot b{{color:#9a3412}}
.hand{{position:absolute;font-size:15px;color:#fff;background:#1d4ed8;border-radius:8px;padding:2px 8px;font-weight:800}}
"""


def stk_css_fix():      # 一疊三枚：往上疊 5px
    return ".stk .coin{margin-top:0}.stk .s2{margin-top:-0px}"


def page(title, body, note):
    return (f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{top(title)}{body}'
            f'<div class="foot">{note}</div></body></html>')


def stacks(items, label='錢盒（要幾個，就拿幾個）'):
    h = ''
    for it in items:
        k, n, note = (it + ('', ''))[:3] if isinstance(it, tuple) else (it, '', '')
        c = PV[k]; hh = c.get('hh', c['w'])
        h += (f'<div class="stk" style="height:{hh + 36}px;width:{c["w"] + 10}px">'
              + ''.join(f'<span style="position:absolute;left:5px;top:{14 + d}px">{coin(k)}</span>' for d in (8, 4, 0))
              + (f'<i class="left">{n}</i>' if n else '') + f'<em style="position:absolute;bottom:-6px;white-space:nowrap">{note}</em></div>')
    return f'<div class="box"><h5>{label}</h5><div class="stks">{h}</div></div>'


def right(steps):
    return '<div class="right">' + ''.join(steps) + '</div>'


def step(n, title, body='', state=''):
    return f'<div class="card step {state}"><h3><i>{n}</i>{title}</h3>{body}</div>'


# ── A：錢盒＋位值板（延續「錢幣位值」頁的板子） ──
A = page('拿出指定的錢', '<div class="main"><div class="card left">' + stacks(['h', 't', 'o']) + '<div class="cols">'
         + col('百元', 'h', coin('h')) + col('十元', 't', coin('t') + coin('t') + ghost('t'), 'focus')
         + col('一元', 'o', ''.join(ghost('o') for _ in range(5))) + '</div></div>'
         + right([step(1, '看一看，要拿多少元？', state='done'),
                  step(2, '拿一拿', '<div class="goal">請拿出 <b>135</b> 元</div><div class="tip">1 個百、3 個十、5 個一<br>十元還要再拿 1 個</div>'
                       '<div class="now">現在有 <b>120</b> 元</div><span class="btn off">✓ 拿好了</span>'),
                  step(3, '數一數，拿對了嗎？', state='todo')]) + '</div>',
         '<b>A 錢盒＋位值板</b>：從上面的錢盒拖錢到百元／十元／一元格（跟「錢幣位值」頁同一張板子，只是方向反過來）。強提示＝虛線錢幣告訴學生還缺幾個、目前格子亮綠框、即時顯示「現在有幾元」；弱提示＝拿掉虛線與即時金額；無提示＝連分格標題的圖都拿掉，按「拿好了」才檢查。')

# ── B：買東西付錢（收銀盤） ──
tray = ('<div style="border:4px solid #a16207;border-radius:22px;background:#fef3c7;min-height:250px;padding:12px 16px;position:relative">'
        '<div style="font-size:19px;color:#92400e;margin-bottom:6px">收銀盤（把錢放在這裡）</div>'
        f'<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">{coin("h")}<span style="width:14px"></span>{coin("t")}{coin("t")}{ghost("t")}'
        f'<span style="width:14px"></span>{"".join(ghost("o") for _ in range(5))}</div>'
        '<div style="position:absolute;right:16px;bottom:10px;font-size:20px;color:#444">盤子裡有 <b style="font-family:sans-serif;font-size:32px;color:#1d4ed8">120</b> 元</div></div>')
shop = ('<div style="display:flex;gap:14px;align-items:center;margin-bottom:12px"><div style="width:150px;height:120px;border-radius:16px;background:#e0f2fe;border:3px solid #7dd3fc;display:flex;align-items:center;justify-content:center;font-size:24px;color:#0369a1;font-weight:800">鉛筆盒<br>（商品圖）</div>'
        '<div style="background:#fff;border:3px solid #ea580c;border-radius:12px;padding:4px 18px;font-size:26px;font-weight:800;white-space:nowrap;transform:rotate(-3deg)">價錢 <span style="font-family:sans-serif;font-size:50px;color:#c2410c">135</span> 元</div>'
        '<div style="font-size:21px;color:#555;line-height:1.5">店員說：<br>「一共 135 元，謝謝！」</div></div>')
B = page('拿出指定的錢', '<div class="main"><div class="card left">' + shop + tray + '<div style="height:12px"></div>' + stacks(['h', 't', 'o'], '我的錢包') + '</div>'
         + right([step(1, '看一看，要付多少元？', state='done'),
                  step(2, '付錢', '<div class="goal">要付 <b>135</b> 元</div><div class="tip">把錢從錢包拿到收銀盤<br>先拿大的，再拿小的</div><span class="btn off">✓ 付好了</span>'),
                  step(3, '數一數，付對了嗎？', state='todo')]) + '</div>',
         '<b>B 買東西付錢</b>：生活情境（商品＋價錢牌，跟早餐店遊戲的付錢畫面同一種感覺）。錢放進收銀盤後自動依大小排成一列，不分百元／十元／一元格。較貼近真實付錢，但位值的結構線索比 A 少；商品圖沿用圖庫（依金額分段換主題）。')

# ── C：一邊拿、一邊往上數（金額條） ──
ticks = [(0, '0'), (100, '100'), (110, '110'), (120, '120'), (130, ''), (135, '135')]
barw = 590
bar = f'<div style="position:relative;height:96px;margin-top:20px"><div style="position:absolute;left:0;top:30px;width:{barw}px;height:26px;border:3px solid #9a3412;border-radius:13px;background:#fff"></div>'
bar += f'<div style="position:absolute;left:0;top:30px;width:{barw * 120 / 135:.0f}px;height:26px;border-radius:13px 0 0 13px;background:#fb923c;border:3px solid #9a3412"></div>'
for v, t in ticks:
    x = barw * v / 135
    bar += f'<div style="position:absolute;left:{x - 1:.0f}px;top:24px;width:3px;height:38px;background:#7c2d12"></div>'
    if t:
        big = 'font-size:26px;color:#c2410c' if v == 135 else ('font-size:24px;color:#1d4ed8' if v == 120 else 'font-size:18px;color:#777')
        bar += f'<div style="position:absolute;left:{x - 30:.0f}px;top:64px;width:60px;text-align:center;font-family:sans-serif;font-weight:800;{big}">{t}</div>'
bar += f'<div style="position:absolute;left:{barw - 90:.0f}px;top:-4px;width:100px;text-align:right;text-align:center;font-size:17px;color:#c2410c;font-weight:800">要拿到這裡</div></div>'
row = ('<div style="border:3px solid #fdba74;border-radius:16px;min-height:150px;padding:10px 14px"><div style="font-size:19px;color:#9a3412;margin-bottom:6px">拿出來的錢（照順序排，一個一個往上數）</div>'
       f'<div style="display:flex;gap:10px;align-items:flex-end">'
       + ''.join(f'<div style="text-align:center">{c}<div style="font-family:sans-serif;font-weight:800;font-size:19px;color:#1d4ed8;margin-top:4px">{n}</div></div>'
                 for c, n in [(coin('h'), '100'), (coin('t'), '110'), (coin('t'), '120')])
       + f'<div style="text-align:center">{ghost("t")}<div style="font-size:19px;color:#9ca3af;margin-top:4px">？</div></div></div></div>')
C = page('拿出指定的錢', '<div class="main"><div class="card left">' + stacks(['h', 't', 'o']) + row + bar + '</div>'
         + right([step(1, '看一看，要拿多少元？', state='done'),
                  step(2, '一邊拿，一邊數', '<div class="goal">請拿出 <b>135</b> 元</div><div class="tip">一百、一百一十、一百二十……<br>再拿 1 個十元，數到一百三十</div><span class="btn off">✓ 拿好了</span>'),
                  step(3, '數一數，拿對了嗎？', state='todo')]) + '</div>',
         '<b>C 一邊拿、一邊往上數</b>：錢排成一列，每放一個就在下面寫出數到多少（強提示會念「一百、一百一十…」），金額條跟著變長，拿超過會衝出終點變紅。重點放在「累數」，最適合第三頁「湊到指定的錢」；缺點是數字很大（例：987）時一列排不下。')

# ── D：第二頁「加入 5／50／500」（畫在 A 版面上） ──
D = page('拿出指定的錢（有 5 元、50 元）', '<div class="main"><div class="card left">'
         + stacks(['h', 'q', ('t', '剩 3', ''), 'f', ('o', '剩 2', '')], '錢盒（10 元只有 4 個、1 元只有 4 個）') + '<div class="cols">'
         + col('百元', 'h', coin('h')) + col('十元', 't', coin('q') + coin('t') + ghost('t') + ghost('t'), 'focus')
         + col('一元', 'o', coin('f') + coin('o') + coin('o') + ghost('o')) + '</div></div>'
         + right([step(1, '看一看，要拿多少元？', state='done'),
                  step(2, '拿一拿', '<div class="goal">請拿出 <b>188</b> 元</div><div class="tip">十元要 8 個，可是錢盒只有 4 個<br>→ 先拿 1 個 50 元，再拿 3 個 10 元</div>'
                       '<div class="now">現在有 <b>167</b> 元</div><span class="btn off">✓ 拿好了</span>'),
                  step(3, '數一數，拿對了嗎？', state='todo')]) + '</div>',
         '<b>第二頁：加入 5 元、50 元、500 元</b>（畫在 A 版面上，實際跟著選定的版面）。50 元放十元格、5 元放一元格。<b>怎麼讓學生一定會用到特殊幣？</b>建議做法＝錢盒裡 10 元、1 元各只有 4 個（紅色小標顯示剩幾個），數字 5 以上就一定要拿 50／5 元；另一種做法＝不限數量，但要求「用最少的錢幣」。')

# ── E：第三頁「湊到指定的錢」（往上加） ──
E = page('湊到指定的錢', '<div class="main"><div class="card left">' + stacks(['h', 't', 'o']) + '<div class="cols">'
         + col('百元', 'h', coin('h', 'lock')) + col('十元', 't', coin('t', 'lock') + coin('t', 'lock') + coin('t', 'new'))
         + col('一元', 'o', ''.join(coin('o', 'new') for _ in range(3)) + ghost('o') + ghost('o'), 'focus') + '</div></div>'
         + right([step(1, '看一看，已經有多少元？', state='done'),
                  step(2, '再拿一些，湊到 135 元', '<div class="goal" style="font-size:21px;white-space:nowrap">已經有 <b style="font-size:38px;color:#57534e;border-color:#d6d3d1;background:#f5f5f4">120</b> 元 ➜ 湊到 <b style="font-size:50px">135</b> 元</div>'
                       '<div class="tip">從 120 往上數：<br>一百三十、一百三十一、一百三十二……</div><div class="now">現在有 <b>133</b> 元</div><span class="btn off">✓ 湊好了</span>'),
                  step(3, '再拿了多少元？', '<div style="font-size:22px">再拿了（　　）元</div>', state='todo')]) + '</div>',
         '<b>第三頁：湊到指定的錢</b>（畫在 A 版面上）。原來就有的錢是灰色、不能動；學生再拿的錢有綠色外圈。①看已經有多少→②從現有的錢往上加到指定金額→③填「再拿了幾元」（要不要有這一步可選）。待決定：要不要出「跨過整十／整百」的題目（例：已經有 80 元，湊到 135 元）。')

for name, html in dict(A=A, B=B, C=C, D=D, E=E).items():
    (HERE / f'mock_{name}.html').write_text(html, encoding='utf-8')
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1180,height:820},deviceScaleFactor:2});"
      "for(const n of 'ABCDE'){await p.goto('file://" + str(HERE.resolve()) + "/mock_'+n+'.html');await p.waitForTimeout(400);await p.screenshot({path:'" + str(HERE.resolve()) + "/mock_'+n+'.png'});}await b.close()})();")
subprocess.run(['node', '-e', js], check=True)
print('done')
