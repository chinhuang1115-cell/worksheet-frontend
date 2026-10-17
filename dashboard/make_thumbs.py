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
    N = 8 if ('calc=1' in item['params'] or 'divtype=' in item['params']) else 3      # 直式計算題多出幾題，才選得到「有進退位」「加法」的示範題
    q = {k: v[0] for k, v in parse_qs(item['params']).items()}
    ep = item['endpoint'].rsplit('/', 1)[1]
    th = '文具店' if ep == 'sub2noreg-app' else '甜點店'
    if ep == 'sub2noreg-app':
        return iw.generate(th, N, 'full', 11, q.get('op', 'sub'), q.get('regroup', 'none'), int(q.get('digits', 2)), q.get('calc') == '1')
    if ep == 'mul-concept': return iw.generate_mul(th, N, 'full', 11, q.get('level', 'normal'))
    if ep == 'mul-wordprob': return iw.generate_mulwp(th, N, 'full', 11, q.get('level', 'normal'))
    if ep == 'mul-vertical': return iw.generate_mulv(th, N, 'full', 11, q.get('regroup', 'none'), q.get('calc') == '1')
    if ep == 'div-vertical': return iw.generate_divv(th, N, 'full', 11, q.get('divtype', 'mix'))
    if ep == 'mul-dial': return iw.generate_dial(th, N, 'full', 11, q.get('level', 'normal'))
    if ep == 'place-value': return iw.generate_pv(th, N, 'full', 11, q.get('level', 'normal'))
    if ep == 'coin-carry': return iw.generate_cy(th, N, 'full', 11, q.get('level', 'normal'), q.get('base', 'one'))
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
.hs{position:relative;align-self:stretch;justify-self:stretch;border-top:6px solid #cbd5e1;margin:-3px 0 -3px 6px}.hs::before{content:'';position:absolute;left:-6px;top:0;width:44px;height:calc(100% + 23px);background:url('data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%2040%20100%27%20preserveAspectRatio%3D%27none%27%3E%3Cpath%20d%3D%27M8%203%20C%2034%2022%2C%2034%2078%2C%208%2097%27%20fill%3D%27none%27%20stroke%3D%27%23cbd5e1%27%20stroke-width%3D%276%27%20stroke-linecap%3D%27round%27%20vector-effect%3D%27non-scaling-stroke%27/%3E%3C/svg%3E') no-repeat;background-size:100% 100%}.ln{grid-column:3/5;width:100%;height:5px;background:#94a3b8}.de{font-size:34px;line-height:1}"""


def div_thumb(b, P0):
    """除法計算格特寫縮圖：房子（除號）、妖怪（被除數）、玩家（除數）、商的虛線格、乘積與餘數的虛線格"""
    a, d = str(P0['a']), P0['b']; big = P0.get('big')
    q1 = '<i class="x">✗</i>' if big else '<i class="q">?</i>'
    html = (f'<style>{DIV_CSS}</style><div class="bd"><span></span><span class="de">👹</span>{q1}<i class="q">?</i>'
            f'<i style="grid-row:2;grid-column:1">{d}</i><span class="hs" style="grid-row:2;grid-column:2/5"></span><i style="grid-row:2;grid-column:3">{a[0]}</i><i style="grid-row:2;grid-column:4">{a[1]}</i>'
            f'<span class="de">🧒</span><span></span><span></span><i class="q">?</i><span></span><span></span><div class="ln"></div></div>')
    pg = b.new_page(viewport={'width': 520, 'height': 390}); pg.set_content(html); pg.wait_for_timeout(250)
    im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); pg.close(); return im


with sync_playwright() as p, tempfile.TemporaryDirectory() as tmp:
    b = p.chromium.launch(executable_path=os.environ.get('PW_CHROMIUM', '/opt/pw-browsers/chromium'))
    for it in cat['items']:
        if only and it['id'] not in only: continue
        f = pathlib.Path(tmp) / (it['id'] + '.html'); f.write_bytes(gen(it))
        pg = b.new_page(viewport={'width': 1100, 'height': 780})
        pg.add_init_script("localStorage.setItem('wp_level','3')")
        pg.goto('file://' + str(f)); pg.wait_for_selector('.card', state='attached'); pg.wait_for_timeout(1800)
        if it['kind'] == 'divvc':      # 除法計算：房子特寫（依卡片類型挑示範題：沒有幫手／找幫手／不能大欺小；混合取第一題）
            want = it['params'].split('divtype=')[1].split('&')[0]
            P0 = pg.evaluate("(w=>{const L=P.filter(p=>w==='mix'||(w==='big'?p.big:w==='help'?p.help:(!p.big&&!p.help))); const p=L[0]||P[0]; return {a:p.a,b:p.b,big:p.big}})", want)
            im = div_thumb(b, P0); im.save(out / (it['id'] + '.webp'), quality=82); pg.close(); print('OK', it['id'], '(房子特寫)'); continue
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
