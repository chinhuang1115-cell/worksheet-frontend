#!/usr/bin/env python3
"""比對後端 main.py 的 /interactive/* 端點與 dashboard/catalog.json，找出漏列的端點。
用法：python dashboard/check_catalog.py <後端 repo 路徑>   （有缺漏時結束碼 1）"""
import json, re, sys, pathlib
backend = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '../worksheet-backend')
routes = set(re.findall(r'@app\.get\("(/interactive/[^"]+)"\)', (backend / 'backend/main.py').read_text(encoding='utf-8')))
cat = json.loads((pathlib.Path(__file__).parent / 'catalog.json').read_text(encoding='utf-8'))
listed = {i['endpoint'] for i in cat['items']}
missing, stale = sorted(routes - listed), sorted(listed - routes)
print(f'後端端點 {len(routes)} 個，catalog 涵蓋 {len(routes & listed)} 個')
for m in missing: print('  漏列：', m)
for s in stale: print('  後端已不存在：', s)
sys.exit(1 if missing or stale else 0)
