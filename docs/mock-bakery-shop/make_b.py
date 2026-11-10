# 麵包店第 5 關「兩個牌子比單價」模擬圖 B1～B4（2026-11-10）。用法：python make_b.py（需要 playwright；圖片讀前端 images/麵包店）
import base64, pathlib
from playwright.sync_api import sync_playwright
D = pathlib.Path(__file__).parent
img = lambda n: 'data:image/png;base64,' + base64.b64encode((D.parent.parent / 'images' / '麵包店' / f'{n}.png').read_bytes()).decode()
CR = img('可頌'); FONT = (D.parent.parent / 'fonts' / 'Iansui-Regular.ttf').as_uri()
def bag(color, n, price, w=150, label=True):
    ims = ''.join(f'<img src="{CR}" style="width:{w*0.42}px;margin:-6px">' for _ in range(n))
    return f'''<div class="bag" style="--c:{color}"><div class="bt">{'紅袋' if color=='#ef4444' else '藍袋'}</div><div class="bi">{ims}</div>
      {'<div class="bp">一袋 '+str(n)+' 個<br><b>'+str(price)+' 元</b></div>' if label else ''}</div>'''
CSS = f'''@font-face{{font-family:芫荽;src:url({FONT})}}*{{box-sizing:border-box}}body{{margin:0;width:1280px;height:800px;font-family:芫荽;background:#fdf1f4;color:#333}}
#awn{{height:26px;background:repeating-linear-gradient(90deg,#f472b6 0 40px,#fff7ed 40px 80px);position:relative}}#awn b{{position:absolute;left:50%;top:0;transform:translateX(-50%);background:#5b3a29;color:#fff7ed;border:3px solid #f9a8d4;border-radius:16px;padding:0 20px;font-size:19px}}
.top{{height:50px;background:#fff;border-bottom:3px solid #f9a8d4;display:flex;align-items:center;padding:0 14px;gap:12px;font-size:18px;font-weight:800}}.top .t{{border:2px solid #fdba74;border-radius:20px;padding:2px 14px;color:#9a3412;background:#fff7ed}}
.main{{display:flex;gap:10px;padding:10px;height:714px}}.L{{width:470px;border:4px solid #fb923c;border-radius:16px;background:#fff;padding:14px;display:flex;flex-direction:column;gap:10px}}
.C{{flex:1;display:flex;flex-direction:column;gap:10px}}.R{{width:170px;border:4px solid #cbd5e1;border-radius:16px;background:#f8fafc;opacity:.6;padding:10px;font-size:18px}}
.sh{{font-size:22px;font-weight:800}}.sh .n{{display:inline-block;width:32px;height:32px;border-radius:50%;background:#ea580c;color:#fff;text-align:center;margin-right:6px}}.sh .s{{font-size:17px;color:#999;font-weight:400}}
.eq{{font-size:28px;font-weight:800;display:flex;align-items:center;gap:6px;flex-wrap:wrap}}.box{{display:inline-block;min-width:64px;height:48px;border:3px dashed #fb923c;border-radius:10px;text-align:center;line-height:42px;color:#c2410c;background:#fff7ed}}.box.ok{{border:3px solid #22c55e;background:#f0fdf4;color:#15803d}}
.btn{{background:#ea580c;color:#fff;border-radius:12px;padding:10px 16px;font-size:20px;font-weight:800;display:inline-block;box-shadow:0 4px 0 #9a3412}}
.counter{{flex:1;background:linear-gradient(#fbe3e8,#f3bfcb);border-top:9px solid #fff;border-radius:16px 16px 0 0;padding:16px;position:relative}}
.bag{{width:230px;background:#fff;border:4px solid var(--c);border-radius:18px 18px 12px 12px;padding:8px;text-align:center;position:relative}}.bt{{background:var(--c);color:#fff;font-weight:800;border-radius:10px;font-size:20px}}
.bi{{display:flex;justify-content:center;flex-wrap:wrap;padding:6px 0}}.bp{{font-size:20px}}.bp b{{font-size:26px}}
.tag{{font-size:22px;font-weight:800;border:3px dashed #94a3b8;border-radius:10px;padding:4px 8px;background:#fffbeb;margin-top:6px}}
.hint{{font-size:17px;color:#9a3412;background:#fff7ed;border-radius:10px;padding:6px 10px}}.lab{{position:absolute;right:14px;top:10px;font-size:16px;color:#9d174d;background:#fff;border-radius:8px;padding:2px 8px}}
table{{border-collapse:collapse;font-size:22px}}td,th{{border:3px solid #e5b4c2;padding:8px 14px;text-align:center;background:#fff}}th{{background:#fdf2f8}}
'''
def page(name, title, left, center):
    return f'''<html><head><meta charset=utf-8><style>{CSS}</style></head><body><div class="top"><span>第 1 位客人 / 3　麵包店</span><span class="t">麵包店購物（第 5 關：比比看哪袋划算）</span><span style="margin-left:auto;color:#c2410c">🙋 現在是：顧客</span></div>
<div id="awn"><b>🥐 香香麵包店</b></div><div class="main"><div class="L">{left}</div><div class="C">{center}</div><div class="R">🧑‍🍳 店員<br><br>等一下輪到店員</div></div>
<div class="lab" style="position:fixed;left:14px;bottom:12px;top:auto;right:auto;font-size:22px;background:#5b3a29;color:#fff">模擬圖 {name}：{title}</div></body></html>'''
task = '<div style="border:3px dashed #eab308;border-radius:12px;padding:10px;font-size:22px;background:#fffbeb">📝 任務卡<br><b>買一袋可頌，哪一袋比較划算？</b></div>'
calc = '<span class="btn">📝 用直式算一算</span>'
P = {}
# B1：兩袋擺在櫃台上，袋子下方各一張空白的「1 個 □ 元」價卡；算完填上、便宜的蓋「划算」章
P['B1'] = page('B1', '櫃台上兩袋＋空白價卡', task + '''<div class="sh"><span class="n">1</span>比一比<span class="s">：1 個多少元？</span></div>
 <div class="eq"><span style="color:#ef4444">紅袋</span> 75 ÷ 3 ＝ <span class="box ok">25</span> 元</div><div class="eq"><span style="color:#2563eb">藍袋</span> 80 ÷ 4 ＝ <span class="box">？</span> 元</div>''' + calc,
 '<div class="counter"><div style="display:flex;gap:60px;justify-content:center;margin-top:30px">' +
 f'<div style="text-align:center">{bag("#ef4444",3,75)}<div class="tag">1 個 <span style="color:#15803d">25</span> 元</div></div>' +
 f'<div style="text-align:center">{bag("#2563eb",4,80)}<div class="tag">1 個 □ 元</div></div></div>' +
 '<div class="hint" style="position:absolute;left:16px;bottom:16px">算出 1 個多少元，寫在袋子下面的價卡</div></div>')
# B2：比價單（表格）：一袋幾個、一袋多少元、1 個多少元；最後一列圈便宜的
P['B2'] = page('B2', '比價單（表格）', task + '''<div class="sh"><span class="n">2</span>選划算的<span class="s">：哪一袋 1 個比較便宜？</span></div>
 <div style="display:flex;gap:10px"><span class="btn" style="background:#ef4444;box-shadow:0 4px 0 #991b1b">紅袋</span><span class="btn" style="background:#2563eb;box-shadow:0 4px 0 #1e3a8a">藍袋</span><span class="btn" style="background:#64748b;box-shadow:0 4px 0 #334155">一樣</span></div>''',
 '<div class="counter"><div style="display:flex;gap:30px;align-items:flex-start;justify-content:center;margin-top:10px">' + bag('#ef4444',3,75,120,False) + bag('#2563eb',4,80,120,False) + '</div>' +
 '<table style="margin:18px auto"><tr><th></th><th style="color:#ef4444">紅袋</th><th style="color:#2563eb">藍袋</th></tr><tr><th>一袋幾個</th><td>3 個</td><td>4 個</td></tr><tr><th>一袋多少元</th><td>75 元</td><td>80 元</td></tr><tr><th>1 個多少元</th><td><span class="box ok">25</span></td><td><span class="box ok">20</span></td></tr></table></div>')
# B3：天平：兩個單價放上秤，便宜的那邊翹高、亮起來
P['B3'] = page('B3', '價錢天平', task + '''<div class="sh"><span class="n">2</span>選划算的<span class="s">：天平哪邊比較輕＝比較便宜</span></div><div class="eq">25 元 ＞ 20 元</div>
 <div style="display:flex;gap:10px"><span class="btn" style="background:#ef4444;box-shadow:0 4px 0 #991b1b">紅袋</span><span class="btn" style="background:#2563eb;box-shadow:0 4px 0 #1e3a8a">藍袋</span><span class="btn" style="background:#64748b;box-shadow:0 4px 0 #334155">一樣</span></div>''',
 '<div class="counter"><div style="display:flex;gap:40px;justify-content:center">' + bag('#ef4444',3,75,110) + bag('#2563eb',4,80,110) + '</div>' +
 '''<svg width="520" height="240" style="display:block;margin:10px auto" viewBox="0 0 520 240"><rect x="250" y="70" width="20" height="150" fill="#a16207"/><rect x="190" y="215" width="140" height="18" rx="6" fill="#78350f"/>
 <g transform="rotate(-12 260 70)"><rect x="60" y="64" width="400" height="12" rx="6" fill="#92400e"/><line x1="90" y1="76" x2="90" y2="120" stroke="#92400e" stroke-width="4"/><line x1="430" y1="76" x2="430" y2="120" stroke="#92400e" stroke-width="4"/>
 <rect x="30" y="120" width="120" height="50" rx="12" fill="#fee2e2" stroke="#ef4444" stroke-width="4"/><text x="90" y="155" font-size="28" text-anchor="middle" fill="#b91c1c" font-weight="800">25 元</text>
 <rect x="370" y="120" width="120" height="50" rx="12" fill="#dbeafe" stroke="#2563eb" stroke-width="4"/><text x="430" y="155" font-size="28" text-anchor="middle" fill="#1d4ed8" font-weight="800">20 元</text></g></svg>
 <div class="hint" style="text-align:center">1 個的價錢放上天平：比較便宜的那邊比較輕、翹起來</div></div>''')
# B4：一個一個排出來：每袋拆成一排可頌，每個可頌下面寫單價，兩排上下對齊比
P['B4'] = page('B4', '拆開排一排（看得到每個的價錢）', task + '''<div class="sh"><span class="n">3</span>便宜多少<span class="s">：1 個便宜多少元？</span></div><div class="eq">25 － 20 ＝ <span class="box">？</span> 元</div>''' + calc,
 '<div class="counter">' + ''.join(f'''<div style="display:flex;align-items:center;gap:10px;margin:14px 0"><div class="bag" style="--c:{c};width:120px"><div class="bt">{nm}</div><div class="bp">一袋 {n} 個<br><b>{p} 元</b></div></div>
   <div style="display:flex;gap:10px">{''.join(f'<div style="text-align:center"><img src="{CR}" style="width:70px"><div style="font-size:20px;font-weight:800;color:{c}">{p//n} 元</div></div>' for _ in range(n))}</div></div>''' for c,nm,n,p in (('#ef4444','紅袋',3,75),('#2563eb','藍袋',4,80))) +
 '<div class="hint">每一個可頌下面寫 1 個的價錢：紅袋 25 元、藍袋 20 元，藍袋 1 個便宜 5 元</div></div>')
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium') if pathlib.Path('/opt/pw-browsers/chromium').exists() else p.chromium.launch()
    for k, h in P.items():
        f = D / f'{k}_比單價.html'; f.write_text(h, encoding='utf-8')
        pg = b.new_page(viewport={'width': 1280, 'height': 800}); pg.goto(f.as_uri()); pg.wait_for_timeout(500); pg.screenshot(path=str(D / f'{k}_比單價.png')); pg.close()
    b.close()
print('ok')
