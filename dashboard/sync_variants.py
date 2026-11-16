#!/usr/bin/env python3
"""依後端 backend/interactive_variants.py 的 ENTRIES，把 catalog.json 的互動卡縮成「入口卡」（2026-11-15：入口頁＋頁內版型下拉）。
用法：python dashboard/sync_variants.py <後端 repo 路徑>
- items 只留每個入口一張（id＝入口 id＝基礎版型舊卡 id，縮圖沿用 interactive/thumbs/<id>.webp）；遊戲項目原樣保留。
- 每張入口卡的 desc／steps／note／paper／smoke 等沿用基礎版型舊卡，標題改用入口標題；新增 members（全部版型：id、label、og、endpoint、params）。
- 舊 75 個 id 的對照表凍結在 dashboard/legacy_catalog.json（check_catalog.py 用它確認舊網址仍對得上某個選項）。
- 重跑安全：已經是入口卡的 catalog 會照舊 legacy_catalog.json 重新建立。**必須在後端（含 interactive_variants.py）上線之後才推前端**。
"""
import json, sys, pathlib
here = pathlib.Path(__file__).parent
backend = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '../worksheet-backend')
sys.path.insert(0, str(backend / 'backend'))
import interactive_variants as iv
cat = json.loads((here / 'catalog.json').read_text(encoding='utf-8'))
legacy = json.loads((here / 'legacy_catalog.json').read_text(encoding='utf-8'))
old = {i['id']: i for i in cat['items'] if i['kind'] != 'game'}
if not old:      # 已經是入口卡：基礎資料取自 members／item 本身
    old = {i['id']: i for i in cat['items'] if i['kind'] != 'game'}
games = [i for i in cat['items'] if i['kind'] == 'game']
items = []
for e in iv.ENTRIES:
    base = old.get(e['id'])
    if base is None:
        raise SystemExit(f"找不到入口 {e['id']} 的基礎卡（catalog 已經縮過？請先 git checkout dashboard/catalog.json）")
    o0 = e['options'][0]
    it = {k: v for k, v in base.items() if k not in ('title', 'endpoint', 'params')}
    it.update({'title': e['title'], 'endpoint': '/interactive/' + (o0['ep'] or e['ep']), 'params': o0['q'],
               'members': [{'id': o['id'], 'label': o['label'], 'og': o['og'], 'endpoint': '/interactive/' + (o['ep'] or e['ep']), 'params': o['q']} for o in e['options']]})
    items.append(it)
cat['items'] = items + games
(here / 'catalog.json').write_text(json.dumps(cat, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(f'入口卡 {len(items)} 張（版型 {sum(len(i["members"]) for i in items)} 種），遊戲 {len(games)} 個')
