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
    q = {k: v[0] for k, v in parse_qs(item['params']).items()}
    ep = item['endpoint'].rsplit('/', 1)[1]
    th = '文具店' if ep == 'sub2noreg-app' else '甜點店'
    if ep == 'sub2noreg-app':
        return iw.generate(th, 3, 'full', 11, q.get('op', 'sub'), q.get('regroup', 'none'), int(q.get('digits', 2)))
    if ep == 'mul-concept': return iw.generate_mul(th, 3, 'full', 11, q.get('level', 'normal'))
    if ep == 'mul-wordprob': return iw.generate_mulwp(th, 3, 'full', 11, q.get('level', 'normal'))
    if ep == 'mul-vertical': return iw.generate_mulv(th, 3, 'full', 11, q.get('regroup', 'none'), q.get('calc') == '1')
    if ep == 'mul-dial': return iw.generate_dial(th, 3, 'full', 11, q.get('level', 'normal'))
    if ep == 'place-value': return iw.generate_pv(th, 3, 'full', 11, q.get('level', 'normal'))
    if ep == 'coin-carry': return iw.generate_cy(th, 3, 'full', 11, q.get('level', 'normal'), q.get('base', 'one'))
    raise SystemExit('未知端點：' + ep)


with sync_playwright() as p, tempfile.TemporaryDirectory() as tmp:
    b = p.chromium.launch(executable_path=os.environ.get('PW_CHROMIUM', '/opt/pw-browsers/chromium'))
    for it in cat['items']:
        if only and it['id'] not in only: continue
        f = pathlib.Path(tmp) / (it['id'] + '.html'); f.write_bytes(gen(it))
        pg = b.new_page(viewport={'width': 1100, 'height': 780})
        pg.add_init_script("localStorage.setItem('wp_level','3')")
        pg.goto('file://' + str(f)); pg.wait_for_selector('.card', state='attached'); pg.wait_for_timeout(1800)
        pg.evaluate("document.querySelectorAll('body *').forEach(e=>{if(getComputedStyle(e).position==='fixed')e.style.visibility='hidden'})")      # 凍結的頂端列會蓋到截圖
        el = pg.query_selector('main .lcol')      # 縮圖只呈現題目（左欄題目卡）；圓盤沒有題目卡，改取作答區
        if not el or el.bounding_box()['height'] < 60: el = pg.query_selector('main #steps')
        im = Image.open(io.BytesIO(el.screenshot())).convert('RGB'); im.thumbnail((520, 520))
        im.save(out / (it['id'] + '.webp'), quality=82); pg.close(); print('OK', it['id'])
    b.close()
