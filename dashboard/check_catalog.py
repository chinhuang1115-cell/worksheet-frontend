#!/usr/bin/env python3
"""檢查 dashboard/catalog.json（2026-11-15 起為「入口卡」＋members）與後端：
 ① 後端 main.py 的 /interactive/* 端點都被某張卡或某個 member 涵蓋，且沒有多餘端點；
 ② id 全域唯一；入口卡的 members[0] 就是卡片本身（endpoint／params 相同）；
 ③ 舊 75 個 id（dashboard/legacy_catalog.json）仍對得上：每個舊網址丟給後端 interactive_variants.lookup，cur 必須是同一個 id；
 ④ 每張入口卡都有縮圖 interactive/thumbs/<id>.webp；
 ⑤ 和後端 interactive_variants.ENTRIES 逐項一致（入口 id、選項 id／標籤／分組／端點／參數）。
用法：python dashboard/check_catalog.py <後端 repo 路徑>   （有問題時結束碼 1）"""
import json, re, sys, pathlib
from urllib.parse import parse_qsl
here = pathlib.Path(__file__).parent
backend = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '../worksheet-backend')
sys.path.insert(0, str(backend / 'backend'))
import interactive_variants as iv
routes = set(re.findall(r'@app\.get\("(/(?:interactive|game)/[^"]+)"\)', (backend / 'backend/main.py').read_text(encoding='utf-8')))
cat = json.loads((here / 'catalog.json').read_text(encoding='utf-8'))
legacy = json.loads((here / 'legacy_catalog.json').read_text(encoding='utf-8'))
errs = []
listed = set()
for i in cat['items']:
    listed.add(i['endpoint']); [listed.add(m['endpoint']) for m in i.get('members', [])]
for m in sorted(routes - listed): errs.append(f'漏列端點：{m}')
for s in sorted(listed - routes): errs.append(f'後端已不存在：{s}')
ids = [i['id'] for i in cat['items']] + [m['id'] for i in cat['items'] for m in i.get('members', []) if m['id'] != i['id']]
for d in {x for x in ids if ids.count(x) > 1}: errs.append(f'id 重複：{d}')
for i in cat['items']:
    if i['kind'] == 'game': continue
    ms = i.get('members')
    if not ms: errs.append(f"{i['id']}：沒有 members"); continue
    if ms[0]['id'] != i['id'] or ms[0]['endpoint'] != i['endpoint'] or ms[0]['params'] != i['params']: errs.append(f"{i['id']}：members[0] 與卡片不一致")
    if not (here.parent / 'interactive/thumbs' / f"{i['id']}.webp").exists(): errs.append(f"{i['id']}：缺縮圖 interactive/thumbs/{i['id']}.webp")
mem = {m['id'] for i in cat['items'] for m in i.get('members', [])}
for lid, v in legacy.items():
    if lid not in mem: errs.append(f'舊 id {lid} 不在任何 members'); continue
    ep = v['endpoint'].rsplit('/', 1)[-1]
    r = iv.lookup(ep, **dict(parse_qsl(v['params'], keep_blank_values=True)))
    if not r or r['cur'] != lid: errs.append(f"舊網址 {lid} 查回 {r and r['cur']}")
byid = {i['id']: i for i in cat['items']}
for e in iv.ENTRIES:
    i = byid.get(e['id'])
    if not i: errs.append(f"後端入口 {e['id']} 不在 catalog"); continue
    want = [(o['id'], o['label'], o['og'], '/interactive/' + (o['ep'] or e['ep']), o['q']) for o in e['options']]
    got = [(m['id'], m['label'], m['og'], m['endpoint'], m['params']) for m in i['members']]
    if want != got: errs.append(f"{e['id']}：members 與後端不一致（請跑 sync_variants.py）")
extra = set(byid) - {e['id'] for e in iv.ENTRIES} - {i['id'] for i in cat['items'] if i['kind'] == 'game'}
for x in sorted(extra): errs.append(f'catalog 有後端沒有的入口：{x}')
n = sum(len(i.get('members', [])) for i in cat['items'])
print(f'後端端點 {len(routes)} 個；入口卡 {len([i for i in cat["items"] if i["kind"] != "game"])} 張、版型 {n} 種；舊 id {len(legacy)} 個')
for e in errs: print('  ✗', e)
print('OK' if not errs else f'{len(errs)} 項問題')
sys.exit(1 if errs else 0)
