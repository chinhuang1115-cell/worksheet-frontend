# 互動遊戲導覽頁的模擬圖（2026-11-10）：產生 A～D 四個 HTML，再用 Playwright 轉 PNG。
# 用法：python docs/mock-game-hub/make.py <後端路徑>（字型用後端的芫荽體）
import pathlib, sys
HERE = pathlib.Path(__file__).parent
FONT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '../worksheet-backend') / 'backend/fonts/Iansui-Regular.ttf'
THUMB = '../../interactive/thumbs/game-breakfast-1.webp'

BASE = f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
@font-face{{font-family:Iansui;src:url('file://{FONT.resolve()}')}}
:root{{--L0:#3f8f8a;--L1:#2f4d6e;--L2:#5a86ad;--L3:#e9f1f9;--bg:#f6f5f2;--card:#fff;--ink:#2b3440;--mute:#6b7683;--line:#e3e0d9;--ac:#e8863a;--ac-soft:#fdf0e3;--game:#ea580c}}
*{{box-sizing:border-box}}html,body{{margin:0}}body{{font-family:Iansui,sans-serif;background:var(--bg);color:var(--ink);width:1280px;height:800px;overflow:hidden;position:relative}}
.edgetabs{{position:absolute;left:0;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;gap:10px}}
.edgetab{{writing-mode:vertical-rl;background:var(--L0);color:#fff;font-weight:800;letter-spacing:.25em;padding:16px 8px;border-radius:0 12px 12px 0;font-size:17px}}
.edgetab.alt{{background:var(--L1)}}
.wrap{{margin-left:56px;padding:22px 28px}}
h1{{margin:0 0 4px;font-size:30px;color:var(--L1)}}.sub{{color:var(--mute);font-size:17px;margin-bottom:14px}}
.tag{{display:inline-block;background:var(--L3);color:var(--L1);border-radius:999px;padding:2px 12px;font-size:15px;font-weight:800}}
.soon{{filter:grayscale(1);opacity:.55}}
.lvl{{display:inline-flex;border:2px solid var(--ac);border-radius:12px;overflow:hidden}}.lvl b{{padding:6px 14px;font-size:17px;color:var(--ac)}}.lvl b.on{{background:var(--ac);color:#fff}}
.mark{{position:absolute;right:14px;bottom:10px;font-size:14px;color:#9ca3af}}
</style>"""

GAMES = [('早餐店', '顧客點餐、算錢、付錢，店員找錢', '錢幣＋四則', True),
         ('文具店', '（示意：即將推出）', '錢幣＋加減', False),
         ('水果攤', '（示意：即將推出）', '重量＋乘法', False)]
STAGES = [('第 1 關', '買 1 樣', '看價錢'), ('第 2 關', '買 2 樣', '加法'), ('第 3 關', '同一樣買好幾個', '乘法'), ('第 4 關', '綜合任務', '先乘再加')]

def thumb(real, h):
    return f'<img src="{THUMB}" style="height:{h}px;border-radius:12px;display:block">' if real else f'<div style="height:{h}px;aspect-ratio:1.6;border-radius:12px;background:#e5e7eb;display:flex;align-items:center;justify-content:center;font-size:{h//4}px">🏪</div>'

def edge(): return '<div class="edgetabs"><div class="edgetab">易數教室</div><div class="edgetab alt">互動學習單</div></div>'

# A：每個遊戲一條大卡，關卡按鈕直接排在卡片上
def mock_a():
    cards = ''
    for i, (n, d, t, real) in enumerate(GAMES[:2]):
        st = ''.join(f'<div style="flex:1;border:3px solid {"var(--game)" if real else "#d1d5db"};border-radius:16px;padding:10px 12px;background:#fff"><div style="font-size:20px;font-weight:800;color:{"var(--game)" if real else "#9ca3af"}">{a}</div><div style="font-size:18px;font-weight:800">{b}</div><div style="font-size:15px;color:var(--mute)">{c}</div></div>' for a, b, c in STAGES) if real else '<div style="font-size:20px;color:#9ca3af;align-self:center">即將推出</div>'
        cards += f'<div class="{"" if real else "soon"}" style="display:flex;gap:22px;background:var(--card);border:1px solid var(--line);border-radius:22px;padding:18px;margin-bottom:18px;box-shadow:0 4px 0 var(--line)">{thumb(real, 190)}<div style="flex:1;display:flex;flex-direction:column;gap:10px"><div style="display:flex;align-items:center;gap:12px"><span style="font-size:28px;font-weight:800">{n}</span><span class="tag">{t}</span></div><div style="font-size:18px;color:var(--mute)">{d}</div><div style="display:flex;gap:10px">{st}</div></div></div>'
    return BASE + f'<body>{edge()}<div class="wrap"><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><h1>🎮 互動遊戲</h1><div class="sub">點一個關卡就開始玩</div></div><div>提示：<span class="lvl"><b>強</b><b class="on">弱</b><b>無</b></span></div></div>{cards}</div><div class="mark">模擬圖 A：大卡片＋關卡按鈕</div></body></html>'

# B：遊戲卡片排成格子，點卡片跳出選關面板
def mock_b():
    cards = ''.join(f'<div class="{"" if r else "soon"}" style="background:var(--card);border:1px solid var(--line);border-radius:18px;padding:12px;box-shadow:0 4px 0 var(--line){";outline:4px solid var(--game)" if r else ""}">{thumb(r, 170)}<div style="font-size:24px;font-weight:800;margin-top:8px">{n}</div><span class="tag">{t}</span></div>' for n, d, t, r in GAMES)
    stages = ''.join(f'<div style="display:flex;align-items:center;gap:12px;border:3px solid var(--game);border-radius:14px;padding:10px 14px;margin-bottom:10px;background:#fff"><b style="font-size:20px;color:var(--game);white-space:nowrap">{a}</b><span style="font-size:19px;font-weight:800">{b}</span><span style="font-size:15px;color:var(--mute);margin-left:auto">{c}</span></div>' for a, b, c in STAGES)
    panel = f'<div style="position:absolute;inset:0;background:rgba(15,23,42,.35)"></div><div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:520px;background:var(--bg);border-radius:24px;padding:22px;box-shadow:0 20px 50px rgba(0,0,0,.3)"><div style="display:flex;gap:14px;align-items:center;margin-bottom:12px">{thumb(True, 80)}<div><div style="font-size:26px;font-weight:800">早餐店</div><div style="font-size:16px;color:var(--mute)">顧客點餐、算錢、付錢，店員找錢</div></div></div>{stages}<div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px"><span>提示：<span class="lvl"><b>強</b><b class="on">弱</b><b>無</b></span></span><span style="font-size:16px;color:var(--mute)">✕ 關閉</span></div></div>'
    return BASE + f'<body>{edge()}<div class="wrap"><h1>🎮 互動遊戲</h1><div class="sub">選一個遊戲</div><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px">{cards}</div></div>{panel}<div class="mark">模擬圖 B：小卡片格子＋選關面板</div></body></html>'

# C：商店街，每個遊戲是一間店；選中的店右側抽屜選關
def mock_c():
    shops = ''
    for n, d, t, r in GAMES:
        roof = 'repeating-linear-gradient(90deg,#ef4444 0 30px,#fff 30px 60px)' if r else 'repeating-linear-gradient(90deg,#9ca3af 0 30px,#f3f4f6 30px 60px)'
        shops += f'<div class="{"" if r else "soon"}" style="width:240px"><div style="height:34px;background:{roof};border-radius:12px 12px 0 0"></div><div style="background:#fff;border:3px solid {"#b45309" if r else "#d1d5db"};border-top:0;border-radius:0 0 14px 14px;padding:12px;text-align:center">{thumb(r, 120).replace("display:block", "display:block;margin:0 auto")}<div style="font-size:24px;font-weight:800;margin-top:6px">{n}</div><span class="tag">{t}</span></div></div>'
    stages = ''.join(f'<div style="border:3px solid var(--game);border-radius:14px;padding:10px 14px;margin-bottom:10px;background:#fff"><b style="font-size:19px;color:var(--game)">{a}</b>　<span style="font-size:19px;font-weight:800">{b}</span><div style="font-size:15px;color:var(--mute)">{c}</div></div>' for a, b, c in STAGES)
    return BASE + f'<body style="background:linear-gradient(#e0f2fe 0 62%,#d6d3d1 62%)">{edge()}<div class="wrap" style="width:860px"><h1>🎮 互動遊戲街</h1><div class="sub">走進一間店開始玩</div><div style="display:flex;gap:26px;margin-top:70px;align-items:flex-end">{shops}</div></div><div style="position:absolute;right:0;top:0;bottom:0;width:340px;background:var(--bg);border-left:4px solid var(--game);padding:22px"><div style="font-size:26px;font-weight:800;margin-bottom:4px">早餐店</div><div style="font-size:16px;color:var(--mute);margin-bottom:12px">顧客點餐、算錢、付錢，店員找錢</div>{stages}<div>提示：<span class="lvl"><b>強</b><b class="on">弱</b><b>無</b></span></div></div><div class="mark" style="right:356px">模擬圖 C：商店街＋右側選關</div></body></html>'

# D：和互動學習單總覽一致（左側導覽、縮圖格子），關卡用小標籤列在縮圖下
def mock_d():
    nav = ''.join(f'<div style="padding:8px 12px;border-radius:10px;font-size:18px;{"background:var(--L1);color:#fff;font-weight:800" if i == 0 else "color:var(--L1)"}">{x}</div>' for i, x in enumerate(['全部遊戲', '錢幣與購物', '四則運算', '時間（示意）', '幾何（示意）']))
    cards = ''
    for n, d, t, r in GAMES:
        chips = ''.join(f'<span style="border:2px solid var(--game);color:var(--game);border-radius:10px;padding:2px 8px;font-size:15px;font-weight:800;background:#fff">{a.replace("第 ", "").replace(" 關", "")}｜{c}</span>' for a, b, c in STAGES) if r else '<span style="color:#9ca3af">即將推出</span>'
        cards += f'<div class="{"" if r else "soon"}" style="background:var(--card);border:1px solid var(--line);border-radius:16px;padding:12px">{thumb(r, 160)}<div style="font-size:22px;font-weight:800;margin:8px 0 2px">{n}</div><div style="font-size:15px;color:var(--mute);margin-bottom:8px">{d}</div><div style="display:flex;flex-wrap:wrap;gap:6px">{chips}</div></div>'
    return BASE + f'<body>{edge()}<div class="wrap" style="display:flex;gap:24px"><div style="width:200px"><h1 style="font-size:24px">🎮 互動遊戲</h1><div style="margin-top:14px;border-left:4px solid var(--rail,#a9c4de);padding-left:8px">{nav}</div></div><div style="flex:1"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px"><input placeholder="🔍 搜尋遊戲" style="font:inherit;font-size:18px;padding:8px 14px;border:2px solid var(--line);border-radius:12px;width:320px"><span>提示：<span class="lvl"><b>強</b><b class="on">弱</b><b>無</b></span></span></div><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px">{cards}</div></div></div><div class="mark">模擬圖 D：比照互動學習單總覽</div></body></html>'

for k, f in (('A', mock_a), ('B', mock_b), ('C', mock_c), ('D', mock_d)):
    (HERE / f'mock_{k}.html').write_text(f(), encoding='utf-8')
print('ok')
