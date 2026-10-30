#!/usr/bin/env python3
"""為統整頁（interactive/index.html）產生每個互動頁的縮圖：依 catalog.json 的端點與參數，用後端產生器產出 HTML，
以 Chromium 截圖題目卡（只呈現題目，不含提示版本切換），存成 interactive/thumbs/<id>.webp（寬 520）。
用法：python dashboard/make_thumbs.py <後端 repo 路徑> [id ...]      需要 playwright、Pillow；chromium 位置用 PW_CHROMIUM 指定。
新增／改版互動頁後重跑（只重做指定的 id，沒指定就全部）。"""
import io, json, os, pathlib, sys, tempfile
from urllib.parse import parse_qs
backend = pathlib.Path(sys.argv[1]).resolve()
only = set(sys.argv[2:])
sys.path.insert(0, str(backend / 'backend'))
import interactive_wordprob as iw
from PIL import Image
from playwright.sync_api import sync_playwright
here = pathlib.Path(__file__).resolve().parent
cat = json.loads((here / 'catalog.json').read_text(encoding='utf-8'))
out = here.parent / 'interactive' / 'thumbs'; out.mkdir(parents=True, exist_ok=True)


def gen(item):
    N = 8 if ('calc=1' in item['params'] or 'divtype=' in item['params'] or item['kind'] == 'divdec') else 3      # 直式計算題多出幾題，才選得到「有進退位」「加法」的示範題
    q = {k: v[0] for k, v in parse_qs(item['params']).items()}
    ep = item['endpoint'].rsplit('/', 1)[1]
    th = '文具店' if ep == 'sub2noreg-app' else '甜點店'
    if ep == 'sub2noreg-app':
        return iw.generate(th, N, 'full', 11, q.get('op', 'sub'), q.get('regroup', 'none'), int(q.get('digits', 2)), q.get('calc') == '1')
    if ep == 'mul-concept': return iw.generate_mul(th, N, 'full', 11, q.get('level', 'normal'))
    if ep == 'mul-wordprob': return iw.generate_mulwp(th, N, 'full', 11, q.get('level', 'normal'))
    if ep == 'mul-vertical': return iw.generate_mulv(th, N, 'full', 11, q.get('regroup', 'none'), q.get('calc') == '1', int(q.get('mdig', 1)))
    if ep == 'div-vertical': return iw.generate_divv(th, N, 'full', 11, q.get('divtype', 'mix'), int(q.get('digits', 2)), int(q.get('rem', 0)), int(q.get('ddig', 1)), q.get('dstage'), int(q.get('qdig', 1)))
    if ep in ('div-int-dec', 'div-dec-int'): return iw.generate_divdec('int' if ep == 'div-int-dec' else 'dec', th, N, 'full', 11)
    if ep == 'mul-dial': return iw.generate_dial(th, N, 'full', 11, q.get('level', 'normal'))
    if ep == 'place-value': return iw.generate_pv(th, N, 'full', 11, q.get('level', 'normal'))
    if ep == 'coin-carry': return iw.generate_cy(th, N, 'full', 11, q.get('level', 'normal'), q.get('base', 'one'))
    if ep == 'fenfen': return iw.generate_ff('水果', N, 'full', 11, q.get('level', 'normal'), q.get('ftype', 'share'))
    if ep == 'chufa': return iw.generate_cf('水果', N, 'full', 11, q.get('level', 'normal'), q.get('stage', 'plate'), q.get('div', 'small'))
    raise SystemExit('未知端點：' + ep)


CALC_CSS = """*{box-sizing:border-box}body{margin:0;width:520px;height:390px;background:#fdf0e3;display:flex;align-items:flex-end;justify-content:center;padding-bottom:22px;font-family:"芫荽","Noto Sans CJK TC",sans-serif}
.bd{background:#1f2937;border-radius:18px;padding:20px 28px;color:#fff;font-size:52px;font-weight:700}.r{display:flex;gap:8px;align-items:center}
.r i{font-style:normal;width:58px;height:64px;text-align:center;line-height:64px}.r i.op{color:#93c5fd}.q{border:3px dashed #94a3b8;border-radius:12px;color:#94a3b8;margin:4px 0;height:58px;line-height:54px}.ln{height:5px;background:#94a3b8;margin:7px 0}"""      # 下方對齊、板子縮小：右上角留給進退位標籤（標籤在總覽頁用 CSS 疊上去）


def calc_thumb(b, P0):
    """計算格特寫縮圖：依第一題的數字畫深色計算板（符號在最左欄、數字靠右對齊、答案虛線格依答案位數）"""
    a, bb, ans = str(P0['a']), str(P0['b']), str(P0['ans'])
    n = max(len(a), len(bb), len(ans))
    row = lambda t: ''.join(f'<i>{t[i - (n - len(t))] if i >= n - len(t) else ""}</i>' for i in range(n))
    sym = {'-': '－', '+': '＋', '×': '×'}.get(P0['op'], P0['op'])
    row2 = f'<i class="op">{sym}</i>' + row(bb)      # 符號固定在最左欄（與互動頁計算格相同），不是貼著第二列數字（使用者 2026-10-17）
    qs = ''.join('<i class="q">?</i>' for _ in range(len(ans)))
    pad = '<i></i>' * (n - len(ans))
    html = (f'<style>{CALC_CSS}</style><div class="bd"><div class="r"><i></i>{row(a)}</div><div class="r">{row2}</div>'
            f'<div class="ln"></div><div class="r"><i></i>{pad}{qs}</div></div>')
    pg = b.new_page(viewport={'width': 520, 'height': 390}); pg.set_content(html); pg.wait_for_timeout(200)
    im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); pg.close(); return im


DIV_CSS = """*{box-sizing:border-box}body{margin:0;width:520px;height:390px;background:#fdf0e3;display:flex;align-items:flex-end;justify-content:center;padding-bottom:22px;font-family:"芫荽","Noto Sans CJK TC",sans-serif}
.bd{background:#1f2937;border-radius:18px;padding:18px 26px;color:#fff;font-size:52px;font-weight:700;display:grid;grid-template-columns:70px 44px 66px 66px;gap:6px 8px;align-items:center;justify-items:center}
.bd i{font-style:normal;width:60px;height:62px;text-align:center;line-height:62px}.q{border:3px dashed #94a3b8;border-radius:12px;color:#94a3b8;height:56px;line-height:50px}.x{border:3px dashed #f87171;border-radius:12px;color:#f87171;height:56px;line-height:50px}
.hs{position:relative;align-self:stretch;justify-self:stretch;border-top:6px solid #cbd5e1;margin:-3px -10px -3px 6px}.hs::before{content:'';position:absolute;left:-6px;top:0;width:44px;height:calc(100% + 11px);background:url('data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%2040%20100%27%20preserveAspectRatio%3D%27none%27%3E%3Cpath%20d%3D%27M8%203%20C%2034%2022%2C%2034%2078%2C%208%2097%27%20fill%3D%27none%27%20stroke%3D%27%23cbd5e1%27%20stroke-width%3D%276%27%20stroke-linecap%3D%27round%27%20vector-effect%3D%27non-scaling-stroke%27/%3E%3C/svg%3E') no-repeat;background-size:100% 100%}.ln{grid-column:3/5;width:100%;height:5px;background:#94a3b8}.de{font-size:34px;line-height:1}"""


def div_thumb(b, P0):
    """除法計算格特寫縮圖：房子（除號）、妖怪（被除數）、玩家（除數）、商的虛線格、乘積與餘數的虛線格"""
    a, d = str(P0['a']), P0['b']; big = P0.get('big')
    q1 = '<i class="x">✗</i>' if big else '<i class="q">?</i>'
    html = (f'<style>{DIV_CSS}</style><div class="bd"><span></span><span class="de"></span>{q1}<i class="q">?</i>'
            f'<i style="grid-row:2;grid-column:1">{d}</i><span class="hs" style="grid-row:2;grid-column:2/5"></span><i style="grid-row:2;grid-column:3">{a[0]}</i><i style="grid-row:2;grid-column:4">{a[1]}</i>'
            f'<span class="de"></span><span></span><span></span><i class="q">?</i><span></span><span></span><div class="ln"></div></div>')
    pg = b.new_page(viewport={'width': 520, 'height': 390}); pg.set_content(html); pg.wait_for_timeout(250)
    im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); pg.close(); return im


def div_thumb2(b, P0):
    """除法計算格特寫（泛用版：三位數被除數、二位數除數、餘數格；2026-10-22 新增，舊的 div_thumb 保留給二位數÷一位數）。
    商的每一格對齊被除數的每一位（最高位比除數小的那一輪畫 ✗），第一個打得到的位置畫乘積虛線格（併大格時橫跨兩位），有餘數再多一格「……？」。整塊太寬就縮放到 460px 內。"""
    a, d, steps = str(P0['a']), str(P0['b']), P0['steps']; n = len(a)
    dw = 70 if len(d) == 1 else 112
    cols = f'{dw}px 44px ' + ' '.join(['66px'] * n) + (' 40px 66px' if P0.get('rem') else '')
    qs = ''.join(f'<i class="{"x" if st["kind"] == "x" else "q"}" style="grid-row:1;grid-column:{3 + k}">{"✗" if st["kind"] == "x" else "?"}</i>' for k, st in enumerate(steps))
    rem = '<i class="de" style="grid-row:1;grid-column:%d">……</i><i class="q" style="grid-row:1;grid-column:%d">?</i>' % (3 + n, 4 + n) if P0.get('rem') else ''
    digs = ''.join(f'<i style="grid-row:2;grid-column:{3 + k}">{c}</i>' for k, c in enumerate(a))
    h = next(st for st in steps if st['kind'] != 'x'); k0 = h['i']; c1 = 3 + max(k0 - (1 if h.get('merge') else 0), 0); c2 = 3 + k0
    prod = f'<i class="q" style="grid-row:3;grid-column:{c1}/{c2 + 1};width:calc(100% - 6px)">?</i><div class="ln" style="grid-row:4;grid-column:{c1}/{c2 + 1}"></div>'
    html = (f'<style>{DIV_CSS}.bd{{grid-template-columns:{cols};zoom:1}}.bd .ln{{grid-column:auto}}</style><div class="bd" id="bd">{qs}{rem}'
            f'<i style="grid-row:2;grid-column:1">{d}</i><span class="hs" style="grid-row:2;grid-column:2/{3 + n}"></span>{digs}{prod}</div>')
    pg = b.new_page(viewport={'width': 520, 'height': 390}); pg.set_content(html); pg.wait_for_timeout(250)
    pg.evaluate("(()=>{const e=document.getElementById('bd');const w=e.getBoundingClientRect().width;if(w>460)e.style.zoom=460/w})()")
    pg.wait_for_timeout(100)
    im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); pg.close(); return im



def div_thumb_dec(b, P0):
    """除法「商是小數」（小數關）的房子特寫（2026-10-30）：被除數照原貌、後面補到百分位的隱藏版妖怪畫成灰色虛線 0，
    小數點畫成黃色發光點（被除數與商各一個，商的小數點對齊被除數），小數點右邊鋪深藍的「小數關」；商的個位打 ✗ 的題目畫 ✗。"""
    d, dc, steps = str(P0['b']), P0['dec'], P0['steps']; dp, nd, hid = dc['dp'], dc['ND'], dc['hid']
    hid = min(hid, nd)
    cols = f'{70 if len(d) == 1 else 112}px 44px ' + ' '.join(['66px'] * nd)
    qs = ''.join(f'<i class="{"x" if k < len(steps) and steps[k]["kind"] == "x" else "q"}{" dp" if k == dp - 1 else ""}" style="grid-row:1;grid-column:{3 + k}">{"✗" if k < len(steps) and steps[k]["kind"] == "x" else "?"}</i>' for k in range(nd))
    digs = ''.join(f'<i class="{"hd" if k >= hid else ""}{" dp" if k == dp - 1 else ""}" style="grid-row:2;grid-column:{3 + k}">{c}</i>' for k, c in enumerate(str(x) for x in dc['digits']))
    css = (f'{DIV_CSS}.bd{{grid-template-columns:{cols};zoom:1;position:relative;overflow:hidden;padding-bottom:40px}}.bd>*{{position:relative;z-index:1}}'
           '.bd i.hd{border:3px dashed #9ca3af;border-radius:12px;color:#9ca3af;height:56px;line-height:50px;opacity:.75}'
           '.bd i.dp::after{content:"";position:absolute;right:-11px;bottom:6px;width:12px;height:12px;border-radius:50%;background:#fde047;box-shadow:0 0 6px 3px rgba(253,224,71,.85),0 0 16px 6px rgba(253,224,71,.4)}'
           '.zone{position:absolute!important;z-index:0!important;top:0;bottom:0;right:0;background:#183d55;border-left:4px solid rgba(253,224,71,.75)}')
    html = (f'<style>{css}</style><div class="bd" id="bd"><div class="zone" id="zn"></div>{qs}'
            f'<i style="grid-row:2;grid-column:1">{d}</i><span class="hs" style="grid-row:2;grid-column:2/{3 + nd}"></span>{digs}</div>')
    pg = b.new_page(viewport={'width': 520, 'height': 390}); pg.set_content(html); pg.wait_for_timeout(250)
    pg.evaluate("(dp=>{const e=document.getElementById('bd'),c=e.querySelectorAll('i[style*=\"grid-row:2\"]')[dp+1];const z=document.getElementById('zn');z.style.left=(c.offsetLeft-6)+'px';const w=e.getBoundingClientRect().width;if(w>460)e.style.zoom=460/w})", dp)
    pg.wait_for_timeout(100)
    im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); pg.close(); return im


with sync_playwright() as p, tempfile.TemporaryDirectory() as tmp:
    b = p.chromium.launch(executable_path=os.environ.get('PW_CHROMIUM', '/opt/pw-browsers/chromium'))
    for it in cat['items']:
        if only and it['id'] not in only: continue
        f = pathlib.Path(tmp) / (it['id'] + '.html'); f.write_bytes(gen(it))
        pg = b.new_page(viewport={'width': 1100, 'height': 780})
        pg.add_init_script("localStorage.setItem('wp_level','3')")
        pg.goto('file://' + str(f)); pg.wait_for_selector('.card', state='attached'); pg.wait_for_timeout(1800)
        if it['kind'] == 'divdec':      # 商是小數：示範題挑「商比 1 小」（有 ✗ 變身、看得到隱藏版妖怪）
            P0 = pg.evaluate("(()=>{const L=P.filter(p=>p.dec&&p.dec.lt1); const p=L[0]||P[0]; return {b:p.b,dec:p.dec,steps:p.steps}})()")
            im = div_thumb_dec(b, P0); im.save(out / (it['id'] + '.webp'), quality=82); pg.close(); print('OK', it['id'], '(房子特寫・小數關)'); continue
        if it['kind'].startswith('divvc'):      # 除法計算：房子特寫（依卡片類型挑示範題：沒有幫手／找幫手／不能大欺小；混合取第一題）
            prm = {k: v[0] for k, v in parse_qs(it['params']).items()}; want = prm.get('divtype', 'mix')
            if it['kind'] == 'divvc' and 'rem' not in prm:      # 舊的四張（二位數÷一位數、整除）：維持原縮圖
                P0 = pg.evaluate("(w=>{const L=P.filter(p=>w==='mix'||(w==='big'?p.big:w==='help'?p.help:(!p.big&&!p.help))); const p=L[0]||P[0]; return {a:p.a,b:p.b,big:p.big}})", want)
                im = div_thumb(b, P0)
            else:      # 新的六張（有餘數、三位數、補 0、除數二位數）：泛用版，直接用題目的逐位模擬結果
                P0 = pg.evaluate("(w=>{const L=P.filter(p=>w==='zero'?p.steps.some(s=>s.kind==='zero'):true); const p=L[0]||P[0]; return {a:p.a,b:p.b,steps:p.steps}})", want)
                P0['rem'] = prm.get('rem') == '1'; im = div_thumb2(b, P0)
            im.save(out / (it['id'] + '.webp'), quality=82); pg.close(); print('OK', it['id'], '(房子特寫)'); continue
        if 'calc=1' in it['params']:      # 直式計算題：縮圖只畫「計算格特寫」（深色板、直式算式、答案虛線格；使用者 2026-10-17 選方案 A），不拍題目卡
            want_rg = 'regroup=none' not in it['params']; want_op = '+' if 'op=mix' in it['params'] else None      # 示範題：不進退位的卡要選沒進退位的題，其餘選有進退位的；加減交錯的卡選加法，才和減法卡的縮圖不同
            P0 = pg.evaluate("(w=>{const L=P.filter(p=>!!p.regroup===w[0]&&(!w[1]||p.op===w[1])); const p=L[0]||P[0]; return {a:p.a,b:p.b,op:p.op,ans:p.ans}})", [want_rg, want_op])
            im = calc_thumb(b, P0); im.save(out / (it['id'] + '.webp'), quality=82); pg.close(); print('OK', it['id'], '(計算格特寫)'); continue
        pg.evaluate("document.querySelectorAll('body *').forEach(e=>{if(getComputedStyle(e).position==='fixed')e.style.visibility='hidden'})")      # 凍結的頂端列會蓋到截圖
        el = pg.query_selector('main .lcol')      # 縮圖只呈現題目（左欄題目卡）；圓盤沒有題目卡，改取作答區
        if not el or el.bounding_box()['height'] < 60: el = pg.query_selector('main #steps')
        im = Image.open(io.BytesIO(el.screenshot())).convert('RGB'); im.thumbnail((520, 520))
        im.save(out / (it['id'] + '.webp'), quality=82); pg.close(); print('OK', it['id'])
    b.close()
    cat['thumbsV'] = int(__import__('time').time())      # 縮圖網址帶版本號，重產後瀏覽器／CDN 才不會沿用舊圖（使用者 2026-10-17 看到舊縮圖）
    (here / 'catalog.json').write_text(json.dumps(cat, ensure_ascii=False, indent=1), encoding='utf-8')
