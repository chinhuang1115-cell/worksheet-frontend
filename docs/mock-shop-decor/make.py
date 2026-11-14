#!/usr/bin/env python3
"""商店街新增店家：第 0 批「裝潢模擬圖」。重產：
    python docs/mock-shop-decor/make.py <後端 backend 資料夾> [暫存資料夾]
需要：pip install 'fonttools[woff]' brotli pillow；node 與 playwright（NODE_PATH 要找得到）。
做法：用後端產生早餐店 HTML，注入 body.shop-<id> 的覆寫 CSS（寫法同 game_shop.html 的 body.shop-bakery）＋菜單與雨棚，截 1280×800（2x）。
覆寫 CSS 另存 decor.css，第 1 批以後實作時直接搬進後端 game_shop.html。商品圖＝Fluent Emoji 3D（MIT），模擬圖只是示意。"""
import sys, os, io, json, base64, pathlib, subprocess, tarfile, shutil
from PIL import Image

HERE = pathlib.Path(__file__).parent.resolve()
BACKEND = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/user/worksheet-backend/backend').resolve()
TMP = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else '/tmp/shop-decor-work').resolve()
TMP.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(BACKEND))

# ── 1. 取圖（npm 套件 @lobehub/fluent-emoji-3d@1.1.0，MIT） ──
PKG = TMP / 'emoji' / 'package' / 'assets'
if not PKG.exists():
    (TMP / 'emoji').mkdir(exist_ok=True)
    subprocess.run(['npm', 'pack', '@lobehub/fluent-emoji-3d@1.1.0'], cwd=TMP / 'emoji', check=True, capture_output=True)
    tg = next((TMP / 'emoji').glob('*.tgz'))
    tarfile.open(tg).extractall(TMP / 'emoji')

def emoji(code, tint=None):
    f = PKG / f'{code}.webp'
    if not f.exists(): f = PKG / f'{code}-fe0f.webp'
    im = Image.open(f).convert('RGBA')
    if tint:                                   # 紅茶／奶茶：同一張 🥤，程式改顏色（只改偏紅的像素）
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if a and r > g + 50 and r > b + 50:
                    k = (r - g) / 255
                    if tint == 'black': px[x, y] = (int(r * .55), int(g * .3 + 10), int(b * .2 + 5), a)
                    if tint == 'milk': px[x, y] = (int(215 + 20 * (1 - k)), int(178 + 30 * (1 - k)), int(130 + 40 * (1 - k)), a)
    im.thumbnail((132, 132), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

# ── 2. 雨棚（SVG，取代 Gemini 生的 awning.png；實作時仍用 Gemini 生圖，這裡只示意條紋與配色） ──
def awning(c1, c2, band=None, edge='rgba(0,0,0,.25)'):
    p = []
    for i in range(20):
        x = i * 64; c = c1 if i % 2 == 0 else c2
        p.append(f'<path d="M{x},0H{x+64}V20A32,32 0 0 1 {x},20Z" fill="{c}" stroke="{edge}" stroke-width="1.5"/>')
    if band:
        p.append(f'<rect x="0" y="12" width="1280" height="6" fill="{band}"/>')
        for i in range(40): p.append(f'<circle cx="{16+i*32}" cy="15" r="2.4" fill="#92400e"/>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 52" preserveAspectRatio="none">{"".join(p)}</svg>'
    return 'url(data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode() + ')'

# ── 3. 七家店（菜單取自 docs/商店街新增店家_規劃.md，每場擺 8 樣） ──
SHOPS = [
 dict(id='drink', name='清涼飲料店', sign='🧋 清涼飲料店', short='飲料店', tint='薄荷綠', note='薄荷綠＋白條紋雨棚、深綠招牌、白綠磁磚牆與櫃台、青綠色零錢盤',
      awn=('#6ee7b7', '#ffffff'),
      menu=[('珍珠奶茶', 50, '1f9cb'), ('奶茶', 40, '1f964', 'milk'), ('紅茶', 25, '1f964', 'black'), ('綠茶', 25, '1f375'), ('鮮奶', 35, '1f95b'), ('咖啡', 45, '2615'), ('果汁', 20, '1f9c3'), ('水果茶', 55, '1f379')],
      css='''
body.shop-drink{background:#ecfdf5;--hole:#b9e5d3}
body.shop-drink #top{border-bottom-color:#6ee7b7}
body.shop-drink #awn .sign{background:#14532d;color:#d1fae5;border-color:#34d399;border-radius:22px}
body.shop-drink #C{background:repeating-linear-gradient(0deg,rgba(20,120,90,.13) 0 2px,transparent 2px 36px),repeating-linear-gradient(90deg,rgba(20,120,90,.10) 0 2px,transparent 2px 72px),linear-gradient(#e6f8ef,#d2f0e3)}
body.shop-drink #board{background:#bfe9d6;border:3px solid #2f8f6b;border-radius:18px}
body.shop-drink .counter::before{background:linear-gradient(rgba(10,90,70,.28),rgba(0,0,0,0) 28%),repeating-conic-gradient(#d3f1e3 0 25%,#aee0cb 0 50%) 0 0/54px 54px}
body.shop-drink #slip{background:#f0fdf4}
body.shop-drink .dish{--lt:#1f8a8a;--dk:#146065;--in1:#134f52;--in2:#17595c;--edge:#0c3a3d;--st:rgba(255,255,255,.75);--orn:#1b7476}
'''),
 dict(id='stationery', name='小學堂文具店', sign='✏️ 小學堂文具店', short='文具店', note='天空藍＋白條紋雨棚、海軍藍招牌、方格紙牆與藍色切割墊桌面、寶藍色零錢盤',
      awn=('#7dd3fc', '#ffffff'),
      menu=[('鉛筆', 10, '270f'), ('原子筆', 15, '1f58a'), ('蠟筆', 10, '1f58d'), ('水彩筆', 25, '1f58c'), ('尺', 15, '1f4cf'), ('剪刀', 45, '2702'), ('筆記本', 30, '1f4d2'), ('三角板', 20, '1f4d0')],
      css='''
body.shop-stationery{background:#eef6ff;--hole:#c5dcf2}
body.shop-stationery #top{border-bottom-color:#93c5fd}
body.shop-stationery #awn .sign{background:#1e3a8a;color:#fef9c3;border-color:#93c5fd;border-radius:4px}
body.shop-stationery #C{background:linear-gradient(rgba(59,130,246,.2) 1px,transparent 1px) 0 0/26px 26px,linear-gradient(90deg,rgba(59,130,246,.2) 1px,transparent 1px) 0 0/26px 26px,#f6faff}
body.shop-stationery #board{background:#dbeafe;border:3px solid #1e40af;border-radius:4px}
body.shop-stationery .counter::before{background:linear-gradient(rgba(20,40,120,.28),rgba(0,0,0,0) 28%),linear-gradient(rgba(30,64,175,.28) 1px,transparent 1px) 0 0/34px 34px,linear-gradient(90deg,rgba(30,64,175,.28) 1px,transparent 1px) 0 0/34px 34px,linear-gradient(#cfe3f8,#b3d0f0)}
body.shop-stationery #slip{background:#fefce8}
body.shop-stationery .dish{--lt:#2f56b8;--dk:#1c2f78;--in1:#1a2a6b;--in2:#203479;--edge:#101c4d;--st:rgba(254,240,138,.85);--orn:#2a46a0}
'''),
 dict(id='toy', name='童趣玩具店', sign='🪀 童趣玩具店', short='玩具店', note='紅黃相間雨棚、木頭招牌、彩色點點牆、藍黃積木墊桌面、紫色零錢盤',
      awn=('#ef4444', '#fde047'),
      menu=[('氣球', 10, '1f388'), ('骰子', 15, '1f3b2'), ('撲克牌', 40, '1f0cf'), ('溜溜球', 50, '1fa80'), ('迴力車', 50, '1f697'), ('水槍', 60, '1f52b'), ('飛鏢靶', 90, '1f3af'), ('小熊娃娃', 99, '1f9f8')],
      css='''
body.shop-toy{background:#fffbe6;--hole:#8cc8f4}
body.shop-toy #top{border-bottom-color:#fbbf24}
body.shop-toy #awn .sign{background:linear-gradient(#c28a45,#9a6a2c);color:#fff7ed;border-color:#fde047;border-radius:12px;text-shadow:0 2px 0 rgba(0,0,0,.35)}
body.shop-toy #C{background:radial-gradient(circle,#f87171 6px,transparent 7px) 0 0/66px 66px,radial-gradient(circle,#60a5fa 6px,transparent 7px) 33px 33px/66px 66px,radial-gradient(circle,#34d399 5px,transparent 6px) 33px 0/66px 66px,#fff6cf}
body.shop-toy #board{background:#fde68a;border:4px solid #ef4444;border-radius:22px}
body.shop-toy .counter::before{background:linear-gradient(rgba(20,60,120,.28),rgba(0,0,0,0) 28%),repeating-conic-gradient(#6db8f2 0 25%,#ffe08a 0 50%) 0 0/72px 72px}
body.shop-toy #slip{background:#fff7d6}
body.shop-toy .dish{--lt:#7c4fd0;--dk:#4a2a96;--in1:#3f2383;--in2:#4a2a96;--edge:#2a1561;--st:rgba(253,224,71,.85);--orn:#6a40bd}
'''),
 dict(id='bento', name='飯香便當店', sign='🍱 飯香便當店', short='便當店', note='橘紅雨棚、黑底金字招牌、直條木板牆、黑漆金邊菜單框、深木桌面、黑漆金線零錢盤',
      awn=('#f97316', '#c2410c'),
      menu=[('便當', 85, '1f371'), ('咖哩飯', 80, '1f35b'), ('炸雞腿', 50, '1f357'), ('飯糰', 30, '1f359'), ('炸蝦', 40, '1f364'), ('關東煮', 30, '1f362'), ('玉米', 25, '1f33d'), ('滷蛋', 10, '1f95a')],
      css='''
body.shop-bento{background:#f3e5d0;--hole:#62401f}
body.shop-bento #top{border-bottom-color:#f97316}
body.shop-bento #awn .sign{background:#111;color:#facc15;border-color:#facc15;border-radius:6px;letter-spacing:2px}
body.shop-bento #C{background:repeating-linear-gradient(90deg,#d8b685 0 46px,#c9a46e 46px 48px)}
body.shop-bento #board{background:#2a1f16;border:3px solid #e0b252;border-radius:6px}
body.shop-bento .counter::before{background:linear-gradient(rgba(0,0,0,.4),rgba(0,0,0,0) 28%),repeating-linear-gradient(90deg,#74492a 0 38px,#5e3a1e 38px 40px)}
body.shop-bento #slip{background:#fffbeb}
body.shop-bento .dish{--lt:#3a3a3a;--dk:#161616;--in1:#101010;--in2:#1c1c1c;--edge:#000;--st:rgba(250,204,21,.85);--orn:#a8841c}
'''),
 dict(id='chinese', name='好味小館', sign='🥢 好味小館', short='中式餐館', lantern=True, note='中國紅雨棚＋金色回紋帶、紅底金字招牌、兩盞燈籠、米色格窗牆、紅漆金線桌面、墨綠色零錢盤',
      awn=('#dc2626', '#b91c1c', '#fbbf24'),
      menu=[('湯麵', 60, '1f35c'), ('炒麵', 70, '1f961'), ('白飯', 10, '1f35a'), ('水餃', 60, '1f95f'), ('蔥油餅', 35, '1fad3'), ('排骨', 50, '1f356'), ('魚板', 15, '1f365'), ('酸辣湯', 40, '1f372')],
      css='''
body.shop-chinese{background:#fbf0dc;--hole:#a31a1a}
body.shop-chinese #top{border-bottom-color:#dc2626}
body.shop-chinese #awn .sign{background:#991b1b;color:#fcd34d;border-color:#fcd34d;border-radius:4px;letter-spacing:3px}
body.shop-chinese #awn::before,body.shop-chinese #awn::after{content:'🏮';position:absolute;top:34px;font-size:46px;line-height:1;z-index:3;filter:drop-shadow(0 4px 3px rgba(0,0,0,.3))}
body.shop-chinese #awn::before{left:calc(37% + 14px)}body.shop-chinese #awn::after{right:calc(18% + 14px)}
body.shop-chinese #C{background:linear-gradient(45deg,transparent 48%,rgba(185,28,28,.16) 49% 51%,transparent 52%) 0 0/34px 34px,linear-gradient(-45deg,transparent 48%,rgba(185,28,28,.16) 49% 51%,transparent 52%) 0 0/34px 34px,#f7e7c6}
body.shop-chinese #board{background:#fff3d6;border:3px solid #b91c1c;border-radius:6px;box-shadow:0 0 0 3px #fbbf24,0 14px 10px -6px rgba(90,50,10,.35)}
body.shop-chinese .counter::before{background:linear-gradient(rgba(60,0,0,.38),rgba(0,0,0,0) 28%),repeating-linear-gradient(90deg,transparent 0 78px,rgba(252,211,77,.38) 78px 80px),linear-gradient(#bd2020,#8f1414)}
body.shop-chinese #slip{background:#fff7dd}
body.shop-chinese .dish{--lt:#2f7a52;--dk:#16452e;--in1:#123b27;--in2:#184a32;--edge:#0a2a1b;--st:rgba(252,211,77,.85);--orn:#2a6a47}
'''),
 dict(id='candy', name='甜甜糖果屋', sign='🍭 甜甜糖果屋', short='糖果餅乾店', note='粉紫＋白條紋雨棚、桃紅招牌、粉紫圓點牆、薄荷綠配粉紅斜紋桌面、莓果紅紫色零錢盤',
      awn=('#d8a7f0', '#ffffff'),
      menu=[('棒棒糖', 10, '1f36d'), ('大顆糖果', 10, '1f36c'), ('仙貝', 10, '1f358'), ('蝴蝶餅', 25, '1f968'), ('巧克力', 35, '1f36b'), ('爆米花', 40, '1f37f'), ('冰淇淋', 25, '1f366'), ('杯子蛋糕', 40, '1f9c1')],
      css='''
body.shop-candy{background:#fbf0ff;--hole:#dfd9d6}
body.shop-candy #top{border-bottom-color:#e9a8f5}
body.shop-candy #awn .sign{background:#be185d;color:#fff;border-color:#f9a8d4;border-radius:22px}
body.shop-candy #C{background:radial-gradient(circle,#f9a8d4 5px,transparent 6px) 0 0/48px 48px,radial-gradient(circle,#c4b5fd 5px,transparent 6px) 24px 24px/48px 48px,#f6eaff}
body.shop-candy #board{background:#e9d5ff;border:3px solid #a855f7;border-radius:22px}
body.shop-candy .counter::before{background:linear-gradient(rgba(120,30,100,.25),rgba(0,0,0,0) 28%),repeating-linear-gradient(135deg,#c4efdd 0 24px,#f9c9de 24px 48px)}
body.shop-candy #slip{background:#fff1f8}
body.shop-candy .dish{--lt:#c0307c;--dk:#7a1d4e;--in1:#6a1744;--in2:#7a1d4e;--edge:#4a0e30;--st:rgba(255,255,255,.8);--orn:#a02a6a}
'''),
 dict(id='clothes', name='小可愛服飾店', sign='🧢 小可愛服飾店', short='服飾店', hanger=True, note='玫瑰粉＋灰條紋雨棚、白底黑字招牌、粉色牆面掛衣桿（菜單像掛在衣架上）、灰色地毯桌面、炭灰色玫瑰縫線零錢盤',
      awn=('#fda4af', '#9ca3af'),
      menu=[('髮夾', 20, '1f380'), ('襪子', 30, '1f9e6'), ('零錢包', 60, '1f45b'), ('手套', 80, '1f9e4'), ('圍巾', 99, '1f9e3'), ('帽子', 99, '1f9e2'), ('太陽眼鏡', 99, '1f576'), ('T 恤', 99, '1f455')],
      css='''
body.shop-clothes{background:#fff1f3;--hole:#cdd1d8}
body.shop-clothes #top{border-bottom-color:#fda4af}
body.shop-clothes #awn .sign{background:#fff;color:#111;border-color:#111;border-radius:3px;letter-spacing:2px}
body.shop-clothes #C{background:repeating-linear-gradient(90deg,rgba(244,114,182,.14) 0 2px,transparent 2px 40px),linear-gradient(#ffe6ea,#ffd6de)}
body.shop-clothes #board{background:transparent;border:0;box-shadow:none;padding:14px 3px 3px;position:relative;gap:6px;margin-top:6px}
body.shop-clothes #board::before{content:'';position:absolute;top:2px;left:1%;right:1%;height:7px;background:linear-gradient(#e5e7eb,#6b7280);border-radius:4px;box-shadow:0 3px 3px rgba(0,0,0,.25)}
body.shop-clothes .item{position:relative;border-radius:8px;border:2px solid #fda4af}
body.shop-clothes .item::before{content:'';position:absolute;top:-13px;left:50%;margin-left:-12px;width:24px;height:11px;border:3px solid #6b7280;border-bottom:0;border-radius:14px 14px 0 0}
body.shop-clothes .counter::before{background:linear-gradient(rgba(40,40,50,.3),rgba(0,0,0,0) 28%),repeating-linear-gradient(45deg,rgba(255,255,255,.28) 0 2px,transparent 2px 6px),linear-gradient(#d3d7de,#b6bbc4)}
body.shop-clothes #slip{background:#fff}
body.shop-clothes .dish{--lt:#555a66;--dk:#2a2d34;--in1:#22252b;--in2:#2d3037;--edge:#14161a;--st:rgba(253,164,175,.9);--orn:#8a5f67}
'''),
]
# 對照用的現有兩家（直接截後端原版，不注入）
REF = [dict(id='breakfast', name='美而好早餐店', short='早餐店', note='紅白雨棚、木頭菜單牆與櫃台、酒紅零錢盤（現有）'),
       dict(id='bakery', name='香香麵包店', short='麵包店', note='粉紅奶油色、巧克力招牌、巧克力＋粉紅縫線零錢盤（現有）')]

# ── 4. 後端產生早餐店／麵包店 HTML ──
import game_shop
H = TMP / 'html'; H.mkdir(exist_ok=True)
for s in ('breakfast', 'bakery'):
    (H / f'{s}.html').write_bytes(game_shop.generate(1, 3, 'faded', seed=3, shop=s))

cfg = {'out': str(HERE), 'html': str(H), 'shops': []}
css_all = []
for s in SHOPS:
    css_all.append(f'/* {s["short"]}：{s["note"]} */' + s['css'])
    cfg['shops'].append(dict(id=s['id'], name=s['name'], short=s['short'], note=s['note'], sign=s['sign'], css=s['css'], lantern=s.get('lantern', False),
        awn=awning(*s['awn']), menu=[dict(id=i, name=m[0], price=m[1], img=emoji(m[2], m[3] if len(m) > 3 else None)) for i, m in enumerate(s['menu'])]))
for r in REF: cfg['shops'].append(dict(id=r['id'], name=r['name'], short=r['short'], note=r['note'], ref=True))
(HERE / 'decor.css').write_text('/* 第 0 批裝潢覆寫 CSS（模擬圖用）；第 1 批以後實作時搬進後端 game_shop.html，格式同 body.shop-bakery。雨棚在實作時改用 Gemini 生的 awning.png。 */\n' + '\n'.join(css_all), encoding='utf8')
(TMP / 'cfg.json').write_text(json.dumps(cfg, ensure_ascii=False), encoding='utf8')
env = dict(os.environ)
subprocess.run(['node', str(HERE / 'shot.js'), str(TMP / 'cfg.json')], check=True, env=env)
