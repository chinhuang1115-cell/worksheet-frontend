# 麵包店第 7 關「哪袋划算」改版模擬圖 C1～C4（2026-11-11）：天平改成「錢幣排一排、一對一比長短」。
# 用法：python make_c.py（需要 playwright；圖片讀前端 images/麵包店）
import base64, pathlib, subprocess
D = pathlib.Path(__file__).parent
img = lambda n: 'data:image/png;base64,' + base64.b64encode((D.parent.parent / 'images' / '麵包店' / f'{n}.png').read_bytes()).decode()
CR = img('可頌'); FONT = (D.parent.parent / 'fonts' / 'Iansui-Regular.ttf').as_uri()
RED, BLUE = '#ef4444', '#2563eb'
CSS = f'''@font-face{{font-family:芫荽;src:url({FONT})}}*{{box-sizing:border-box}}body{{margin:0;width:1280px;height:800px;font-family:芫荽;background:#fdf1f4;color:#333}}
#awn{{height:26px;background:repeating-linear-gradient(90deg,#f472b6 0 40px,#fff7ed 40px 80px);position:relative}}#awn b{{position:absolute;left:50%;top:0;transform:translateX(-50%);background:#5b3a29;color:#fff7ed;border:3px solid #f9a8d4;border-radius:16px;padding:0 20px;font-size:19px}}
.top{{height:50px;background:#fff;border-bottom:3px solid #f9a8d4;display:flex;align-items:center;padding:0 14px;gap:12px;font-size:18px;font-weight:800}}.top .t{{border:2px solid #fdba74;border-radius:20px;padding:2px 14px;color:#9a3412;background:#fff7ed}}
.main{{display:flex;gap:10px;padding:10px;height:714px}}.L{{width:430px;flex:none;border:4px solid #fb923c;border-radius:16px;background:#fff;padding:14px;display:flex;flex-direction:column;gap:12px}}
.C{{flex:1;min-width:0;display:flex;flex-direction:column}}.R{{width:150px;flex:none;border:4px solid #cbd5e1;border-radius:16px;background:#f8fafc;opacity:.6;padding:10px;font-size:18px}}
.sh{{font-size:22px;font-weight:800}}.sh .n{{display:inline-block;width:32px;height:32px;border-radius:50%;background:#ea580c;color:#fff;text-align:center;margin-right:6px}}.sh .s{{font-size:17px;color:#999;font-weight:400}}
.eq{{font-size:28px;font-weight:800;display:flex;align-items:center;gap:6px;flex-wrap:wrap}}.box{{display:inline-block;min-width:64px;height:48px;border:3px dashed #fb923c;border-radius:10px;text-align:center;line-height:42px;color:#c2410c;background:#fff7ed}}.box.ok{{border:3px solid #22c55e;background:#f0fdf4;color:#15803d}}
.btn{{color:#fff;border-radius:12px;padding:10px 18px;font-size:22px;font-weight:800;display:inline-block}}
.counter{{flex:1;background:linear-gradient(#fbe3e8,#f3bfcb);border-top:9px solid #fff;border-radius:16px 16px 0 0;padding:14px 16px;position:relative}}
.bag{{width:200px;background:#fff;border:4px solid var(--c);border-radius:18px 18px 12px 12px;padding:6px;text-align:center}}.bt{{background:var(--c);color:#fff;font-weight:800;border-radius:10px;font-size:19px}}
.bi{{display:flex;justify-content:center;padding:4px 0}}.bp{{font-size:18px;line-height:1.2}}.bp b{{font-size:24px}}
.tag{{font-size:22px;font-weight:800;border:3px dashed #94a3b8;border-radius:10px;padding:2px 8px;background:#fffbeb;margin-top:6px}}
.hint{{font-size:18px;color:#9a3412;background:#fff7ed;border-radius:10px;padding:6px 12px}}
.coin{{width:46px;height:46px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#f8fafc,#cbd5e1 55%,#94a3b8);border:2px solid #64748b;box-shadow:inset 0 0 0 3px rgba(255,255,255,.55),0 2px 0 #475569;color:#334155;font:800 22px/42px 芫荽;text-align:center;flex:none}}
.coin.sm{{width:34px;height:34px;font-size:17px;line-height:30px}}
.coin.ghost{{background:none;border:3px dashed #94a3b8;box-shadow:none;color:transparent}}
.coin.glow{{box-shadow:0 0 0 5px #fde047,0 0 18px 8px #facc15}}
.board{{background:#fff;border:4px solid #e5b4c2;border-radius:16px;padding:14px 16px;margin-top:12px;position:relative}}
.row{{display:flex;align-items:center;gap:0;height:66px}}.row .nm{{width:118px;font-size:20px;font-weight:800;color:#fff;background:var(--c);border-radius:10px;text-align:center;padding:4px 0;margin-right:14px}}
.slot{{width:58px;display:flex;justify-content:center}}.row .tot{{margin-left:14px;font-size:26px;font-weight:800;color:var(--c)}}
.guide{{position:absolute;top:10px;bottom:10px;border-left:2px dashed #cbd5e1}}
.lab{{position:fixed;left:14px;bottom:12px;font-size:22px;background:#5b3a29;color:#fff;border-radius:8px;padding:2px 10px}}
.lv{{position:fixed;right:14px;bottom:12px;font-size:20px;background:#fff;border:3px solid #fb923c;color:#9a3412;border-radius:8px;padding:2px 10px}}
'''
def bag(c, n, price, tag=None):
    ims = ''.join(f'<img src="{CR}" style="width:52px;margin:-4px">' for _ in range(n))
    t = f'<div class="tag">1 個 {tag} 元</div>' if tag else ''
    return f'''<div style="text-align:center"><div class="bag" style="--c:{c}"><div class="bt">{'紅袋' if c==RED else '藍袋'}</div><div class="bi">{ims}</div><div class="bp">一袋 {n} 個　<b>{price} 元</b></div></div>{t}</div>'''
bags = lambda ta, tb: f'<div style="display:flex;gap:50px;justify-content:center">{bag(RED,3,75,ta)}{bag(BLUE,4,80,tb)}</div>'
def coin(cls=''): return f'<div class="slot"><div class="coin {cls}">5</div></div>'
def row(c, nm, k, total, extra=0, glow=False, ghost=0):
    cs = ''.join(coin('glow' if glow and i >= k - extra else '') for i in range(k)) + ''.join(coin('ghost') for _ in range(ghost))
    return f'<div class="row" style="--c:{c}"><div class="nm">{nm} 1 個</div>{cs}<div class="tot">{total}</div></div>'
def board(glow=False, note=''):
    guides = ''.join(f'<div class="guide" style="left:{16+118+14+58*i}px"></div>' for i in range(1, 6))
    return f'<div class="board">{guides}{row(RED,"紅袋",5,"25 元",1,glow)}{row(BLUE,"藍袋",4,"20 元",ghost=1)}{note}</div>'
def page(name, title, lv, left, center):
    return f'''<html><head><meta charset=utf-8><style>{CSS}</style></head><body><div class="top"><span>第 1 位客人 / 3　麵包店</span><span class="t">麵包店購物（第 7 關：哪袋划算）</span><span style="margin-left:auto;color:#c2410c">🙋 現在是：顧客</span></div>
<div id="awn"><b>🥐 香香麵包店</b></div><div class="main"><div class="L">{left}</div><div class="C"><div class="counter">{center}</div></div><div class="R">🧑‍🍳 店員<br><br>等一下輪到店員</div></div>
<div class="lab">模擬圖 {name}：{title}</div><div class="lv">{lv}</div></body></html>'''
task = '<div style="border:3px dashed #eab308;border-radius:12px;padding:10px;font-size:22px;background:#fffbeb">📝 任務卡<br><b>買一袋可頌，哪一袋比較划算？</b></div>'
b3 = f'<div style="display:flex;gap:10px"><span class="btn" style="background:{RED};box-shadow:0 4px 0 #991b1b">紅袋</span><span class="btn" style="background:{BLUE};box-shadow:0 4px 0 #1e3a8a">藍袋</span><span class="btn" style="background:#64748b;box-shadow:0 4px 0 #334155">一樣</span></div>'
step = lambda n, t, s: f'<div class="sh"><span class="n">{n}</span>{t}<span class="s">：{s}</span></div>'
P = {}
# C1 步驟①（強提示才有）：把整袋的錢平分到每個可頌下面，看懂「75 ÷ 3」
def split(c, nm, n, per, done):
    cols = ''.join(f'''<div style="text-align:center;width:112px"><img src="{CR}" style="width:64px"><div style="display:flex;flex-wrap:wrap;justify-content:center;gap:3px;min-height:74px;align-content:flex-start">{''.join('<div class="coin sm">5</div>' if done else '<div class="coin sm ghost">5</div>' for _ in range(per // 5 if done else 3))}</div>
      <div style="font-size:20px;font-weight:800;color:{c}">{str(per) + ' 元' if done else '□ 元'}</div></div>''' for _ in range(n))
    return f'''<div class="board" style="display:flex;align-items:center;gap:10px;padding:8px 12px"><div class="row" style="--c:{c};height:auto;flex-direction:column;gap:4px"><div class="nm" style="margin:0">{nm}</div><div style="font-size:20px;font-weight:800">{n} 個<br>{per*n} 元</div></div>
      <div style="font-size:30px;color:#94a3b8">➜</div>{cols}</div>'''
P['C1'] = page('C1', '① 比一比——把錢平分到每個可頌下面', '強提示才出現', task + step(1, '比一比', '1 個多少元？') +
  f'<div class="eq"><span style="color:{RED}">紅袋</span> 75 ÷ 3 ＝ <span class="box ok">25</span> 元</div><div class="eq"><span style="color:{BLUE}">藍袋</span> 80 ÷ 4 ＝ <span class="box">？</span> 元</div>'
  '<div><span class="btn" style="background:#ea580c;box-shadow:0 4px 0 #9a3412;font-size:20px">📝 用直式算一算</span></div>',
  split(RED, '紅袋', 3, 25, True).replace('margin-top:12px', 'margin-top:0') + split(BLUE, '藍袋', 4, 20, False) +
  '<div class="hint" style="margin-top:12px">一袋的錢平分給每一個可頌：每個可頌下面的錢，就是 1 個的價錢</div>')
# C2 步驟②：兩個單價各排一排錢幣，一對一對齊；短的那排便宜
P['C2'] = page('C2', '② 選划算的——錢幣排一排，一個對一個', '強／弱提示', task + step(2, '選划算的', '哪一袋 1 個比較便宜？') + b3,
  bags(25, 20) + board() + '<div class="hint" style="margin-top:12px">1 個的錢排一排，一個對一個：錢比較少的那一袋比較便宜</div>')
# C3 步驟③：多出來的錢幣發光＝便宜多少
P['C3'] = page('C3', '③ 便宜多少——多出來的錢幣就是答案', '強提示自動發光；弱提示答錯才發光', task + step(3, '便宜多少', '藍袋 1 個便宜多少元？') +
  '<div class="eq">25 － 20 ＝ <span class="box">？</span> 元</div><div><span class="btn" style="background:#ea580c;box-shadow:0 4px 0 #9a3412;font-size:20px">📝 用直式算一算</span></div>',
  bags(25, 20) + board(True, '<div style="position:absolute;left:386px;top:-2px;font-size:19px;font-weight:800;color:#a16207;background:#fef9c3;border-radius:8px;padding:0 8px">多 1 個 5 元</div>') +
  '<div class="hint" style="margin-top:12px">紅袋多出來的錢，就是藍袋便宜的錢</div>')
# C4 無提示：只有價卡上的數字；選錯兩次才出現錢幣排
P['C4'] = page('C4', '② 選划算的——只看數字', '無提示（選錯才出現錢幣）', task + step(2, '選划算的', '哪一袋 1 個比較便宜？') + b3,
  bags(25, 20) + '<div class="hint" style="margin-top:40px;text-align:center;opacity:.75">（無提示：這裡不放錢幣；選錯兩次後才排出錢幣）</div>')
# ───────── D1～D4（使用者 2026-11-11 思路）：算出單價 → 從袋子裡「拉出 1 個」→ 旁邊排出錢幣 → 兩排比多少 ─────────
def rowD(c, nm, n, price, state, glow=False, lit=False):
    # state: 'wait' 還沒算｜'calc' 正在算｜'out' 已拉出 1 個並排好錢幣
    per = price // n; out = state == 'out'
    ims = ''.join(f'<img src="{CR}" style="width:44px;margin:-3px;{"opacity:.22;filter:grayscale(1)" if out and i == n - 1 else ""}">' for i in range(n))
    bagh = f'<div class="bag" style="--c:{c};width:176px;flex:none;{"box-shadow:0 0 0 5px #fde047,0 0 16px 6px #facc15" if lit else ""}"><div class="bt">{nm}</div><div class="bi">{ims}</div><div class="bp" style="white-space:nowrap;font-size:16px">一袋 {n} 個 <b style="font-size:21px">{price} 元</b></div></div>'
    if out:
        k = per // 5; mx = 5
        cs = ''.join(f'<div class="slot" style="width:50px"><div class="coin {"glow" if glow and i >= 4 else ""}" style="width:42px;height:42px;line-height:38px;font-size:20px">5</div></div>' for i in range(k))
        cs += ''.join('<div class="slot" style="width:50px"><div class="coin ghost" style="width:42px;height:42px">5</div></div>' for _ in range(mx - k))
        right = f'<div style="font-size:26px;color:{c};margin:0 4px">➜</div><div style="text-align:center;flex:none;width:72px"><img src="{CR}" style="width:56px;display:block;margin:auto"><div style="white-space:nowrap;font-size:15px;font-weight:800;color:{c};margin-top:-4px">拿出 1 個</div></div>{cs}<div style="margin-left:8px;font-size:24px;font-weight:800;color:{c};white-space:nowrap">{per} 元</div>'
    else:
        right = f'<div style="font-size:26px;color:#cbd5e1;margin:0 4px">➜</div><div style="flex:1;height:70px;border:3px dashed #cbd5e1;border-radius:12px;font-size:19px;color:#94a3b8;display:flex;align-items:center;justify-content:center">{"先算 1 個多少元" if state == "calc" else "等一下再算"}</div>'
    return f'<div style="background:#fff;border:4px solid #e5b4c2;border-radius:16px;padding:10px;display:flex;align-items:center;margin-bottom:12px;height:150px">{bagh}{right}</div>'
def centerD(ra, rb, hint, glow=False, note=''):
    return f'<div style="position:relative">{rowD(RED,"紅袋",3,75,ra,glow,ra=="calc")}{rowD(BLUE,"藍袋",4,80,rb,False,rb=="calc")}{note}</div><div class="hint">{hint}</div>'
eqs = lambda a, b: f'<div class="eq"><span style="color:{RED}">紅袋</span> 75 ÷ 3 ＝ <span class="box {"ok" if a else ""}">{a or "？"}</span> 元</div><div class="eq"><span style="color:{BLUE}">藍袋</span> 80 ÷ 4 ＝ <span class="box {"ok" if b else ""}">{b or "？"}</span> 元</div>'
calcbtn = '<div><span class="btn" style="background:#ea580c;box-shadow:0 4px 0 #9a3412;font-size:20px">📝 用直式算一算</span></div>'
P['D1'] = page('D1', '① 算紅袋 1 個多少元', '袋子原樣：3 個、75 元', task + step(1, '比一比', '1 個多少元？') + eqs('', '') + calcbtn,
  centerD('calc', 'wait', '先算紅袋：75 元買 3 個，1 個多少元？'))
P['D2'] = page('D2', '① 算對了——從紅袋拿出 1 個、排出 25 元', '算對後自動播放', task + step(1, '比一比', '1 個多少元？') + eqs(25, '') + calcbtn,
  centerD('out', 'calc', '紅袋 1 個 25 元：拿出 1 個，旁邊排出 25 元。接著算藍袋'))
P['D3'] = page('D3', '② 選划算的——兩排錢幣比多少', '強／弱提示', task + step(2, '選划算的', '哪一袋 1 個比較便宜？') + b3,
  centerD('out', 'out', '兩袋各拿出 1 個，錢一個對一個：錢比較少的比較便宜'))
P['D4'] = page('D4', '③ 便宜多少——多出來的錢幣就是答案', '強提示自動發光；弱提示答錯才發光', task + step(3, '便宜多少', '藍袋 1 個便宜多少元？') +
  '<div class="eq">25 － 20 ＝ <span class="box">？</span> 元</div>' + calcbtn,
  centerD('out', 'out', '紅袋多出來的錢，就是藍袋便宜的錢', True, '<div style="position:absolute;left:440px;top:8px;font-size:18px;font-weight:800;color:#a16207;background:#fef9c3;border-radius:8px;padding:0 8px">多 5 元</div>'))
NAME = {'C': '錢幣比長短', 'D': '拉出單個比錢幣'}
files = []
for k, h in P.items():
    f = D / f'{k}_{NAME[k[0]]}.html'; f.write_text(h, encoding='utf-8'); files.append(str(f))
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        for f in files:
            pg = b.new_page(viewport={'width': 1280, 'height': 800}); pg.goto(pathlib.Path(f).as_uri()); pg.wait_for_timeout(500); pg.screenshot(path=f[:-5] + '.png'); pg.close()
        b.close()
except ImportError:  # 沒有 Python 版 playwright 就用 Node 版
    JS = "const{chromium}=require('playwright');(async()=>{const b=await chromium.launch();for(const f of process.argv.slice(1)){const p=await b.newPage({viewport:{width:1280,height:800}});await p.goto('file://'+encodeURI(f));await p.waitForTimeout(500);await p.screenshot({path:f.replace(/\\.html$/,'.png')});await p.close()}await b.close()})()"
    subprocess.run(['node', '-e', JS, *files], check=True)
print('ok')
