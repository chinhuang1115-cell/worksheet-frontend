# 局部微調幾間店的位置（不重跑整個 place_shops.py，其他店不動）：python3 docs/mock-town-gemini/fix_plots.py
# 使用者 2026-11-18：家具行、家電行的底部壓在馬路上；百貨商場的服飾店往右移一些。
# 規則比 place_shops.py 更嚴：店圖「下面 22%」（灰色底座＋一樓）壓到道路不可超過 2%（place_shops 只看最下面 5 列，斜放的底座前緣會壓到路）；其他店若違反也一起挪到最近的合格位置。
import json, re, math, sys
import numpy as np
from scipy import ndimage as ndi
sys.argv=[sys.argv[0]]
src=open('docs/mock-town-gemini/place_shops.py').read().split('CAP={')[0]
exec(src)                                     # 共用 terrain、alpha、label_box、zone_ok、BLK
html=open('games/index.html').read()
P=json.loads(re.search(r'const PLOTS=(\{.*?\});',html).group(1))
SP=json.loads(re.search(r'const SPARE=(\{.*?\});',html).group(1))
KEY={'100':{'服飾店':'服飾店_100'},'1000':{'服飾店':'服飾店_1000'},'10000':{'服飾店':'服飾店_10000'}}
def key(z,n): return KEY[z].get(n,n)
def box(z,n,v):
    x,y,w=v; m=M[key(z,n)]; h=round(w*m['h']/m['w']); return (x-w/2,y-h,x+w/2,y,h)
def inter(a,b): return max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
def bad_slab(k,x,y,w):
    a,w2,h2,(b0,b1)=alpha(k,w); x0=int(x-w2//2); y0=y-h2; s=min(int(h2*.22),20)   # 只看底座＋一樓（高樓最多 20px）
    if y0<4 or x0<4 or x0+w2>W-4: return True
    part=a[h2-s:]
    if (part&road[y-s:y,x0:x0+w2]).sum()>.02*part.sum(): return True      # 底座＋一樓壓到路 >2%
    if obs_sum(x0+b0,y-5,x0+b1,y)>0: return True                           # 底邊整段在草地（同 place_shops）
    return dist_road[y-3,x0+b0:x0+b1].min()>16
def free(z,n,x,y,w,others):
    k=key(z,n); bx=box(z,n,[x,y,w])
    if bad_slab(k,x,y,w): return False
    m=M[k]; lb=label_box(k,w,bx[4]); L=(bx[0]+lb[0],bx[1]+lb[1],bx[0]+lb[2],bx[1]+lb[3])
    for fx0,fy0,fx1,fy1 in BLK:
        if inter(bx,(fx0,fy0,fx1,fy1))>0: return False
    for ob in others:
        if inter(bx,ob)>.05*(bx[2]-bx[0])*(bx[3]-bx[1]) or inter(L,ob)>0: return False
    return True
STEP=4
# 第二步：附近沒位置的店（家電行、家具行、飲料店）改成整區找，可以用掉「施工中」的位置（被蓋到的施工中刪掉）
WIDE=True
TODO=[(z,n,None) for z in P for n,v in P[z].items() if bad_slab(key(z,n),*v)]
zi={'100':0,'1000':1,'10000':2}
TODO0=[('10000','家電行',None),('10000','家具行',None),('10000','服飾店','right')]+[(z,n,None) for z in P for n,v in P[z].items() if (z,n) not in [('10000','家電行'),('10000','家具行'),('10000','服飾店')] and bad_slab(key(z,n),*v)]
for z,n,mode in TODO:
    others=[box(zz,nn,v)[:4] for zz in P for nn,v in P[zz].items() if not (zz==z and nn==n)]
    if not WIDE: others+=[(x-w/2,y-w*0.8,x+w/2,y) for zz in SP for x,y,w,d in SP[zz] if d]
    x0,y0,w=P[z][n]; best=None
    R=(700 if WIDE else 160)
    for y in range(max(40,y0-R),min(H-26,y0+R+1),STEP if WIDE else 2):
        for x in range(max(10,x0-R),min(W-10,x0+R+1),STEP if WIDE else 2):
            if mode=='right' and x<x0+40: continue
            if not zone_ok(zi[z],x,y): continue
            if not free(z,n,x,y,w,others): continue
            d=math.hypot(x-x0,y-y0) if mode!='right' else abs(y-y0)*2+abs(x-(x0+70))
            if best is None or d<best[0]: best=(d,x,y)
    print(n,'舊',P[z][n],'→',best)
    if best:
        P[z][n]=[best[1],best[2],w]; nb=box(z,n,P[z][n])
        SP[z]=[s for s in SP[z] if inter(nb,(s[0]-s[2]/2,s[1]-s[2]*.8,s[0]+s[2]/2,s[1]))==0]
html=re.sub(r'const PLOTS=\{.*?\};','const PLOTS='+json.dumps(P,ensure_ascii=False,separators=(',',':'))+';',html,count=1)
html=re.sub(r'const SPARE=\{.*?\};','const SPARE='+json.dumps(SP,ensure_ascii=False,separators=(',',':'))+';',html,count=1)
open('games/index.html','w').write(html)
# 其他店也用新規則檢查一次（只回報）
for z in P:
    for n,v in P[z].items():
        if bad_slab(key(z,n),*v): print('  ⚠ 底座／一樓碰到路或障礙：',z,n,v)
