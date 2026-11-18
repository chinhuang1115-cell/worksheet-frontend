# 把店放進底圖的「空地」（淡米色圓角方塊）：量空地 → 每區把店分配到空地、決定縮放 f → 輸出 games/index.html 的 LOTS／PLOTS／SITE。
# 用法：python3 docs/mock-town-gemini/place_lots.py [seed]    （從 repo 根目錄；需要 numpy、scipy、PIL）
# 1) 空地：bgA.png 取空地色（249,232,216），形態學開運算＋連通區塊，面積 ≥1500 的 bbox＝空地（目前 36 塊，與 mk.py 的 LOTS 逐一吻合）。
# 2) 店圖：寬＝空地寬×f，底邊＝空地上緣＋空地高×0.9，水平置中（店圖底座約佔圖寬 90%，f 限 0.75～1.15 → 底座 ≤ 空地寬 +15%）。
# 3) 每區用模擬退火排：店圖重疊 ≤5%、不碰區名牌／銀行／城堡、雨棚／直式招牌放得下 ≥8px 的字、上線的店靠近入口、店盡量大；沒用到的空地畫施工中。
import json, math, random, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
im=np.array(Image.open('docs/mock-town-gemini/bgA.png').convert('RGB')).astype(int)
mask=ndi.binary_opening(abs(im-np.array([249,232,216])).sum(2)<45,iterations=2)
lab,_=ndi.label(mask); LOTS=[]
for i,sl in enumerate(ndi.find_objects(lab),1):
    if (lab[sl]==i).sum()>=1500: LOTS.append([sl[1].start,sl[0].start,sl[1].stop-sl[1].start,sl[0].stop-sl[0].start])
LOTS.sort(); print(len(LOTS),'lots')
M=json.load(open('games/town/meta.json'))
CUT=(530,860); GATE=(688,660)
ZN=[['早餐店','麵包店','文具店','糖果餅乾店','玩具店','飲料店','中式餐館','服飾店_100','公車站','動物園'],
    ['服飾店_1000','鞋店','便當店','書店','運動用品店','水果行','電影院','博物館','火車站'],
    ['家電行','腳踏車店','電腦用品店','家具行','樂器行','服飾店_10000','高鐵站','遊樂園','飯店']]
LIVE={'早餐店','麵包店','文具店','糖果餅乾店','玩具店'}
FS=[1.15,1.08,1.0,.92,.85,.78,.7,.62,.55,.5]; CF,VF,TF=13,12.5,11.4   # TF＝最小字級（地圖單位）：1024 寬時地圖約 966px 寬（×0.702）→ 8px
zl=lambda L:0 if L[0]+L[2]/2<CUT[0] else (1 if L[0]+L[2]/2<CUT[1] else 2)
def geom(key,L,f):
    m=M[key]; w=L[2]*f; h=w*m['h']/m['w']; b=L[1]+L[3]*.9; return (L[0]+L[2]/2-w/2,b-h,L[0]+L[2]/2+w/2,b),w,h
def labelf(key,box,w,h):   # 與 games/index.html nameTag 同公式的字級；沒錨點回傳 TF
    m=M[key]; k=len(key.split('_')[0]); x0,y0=box[0],box[1]
    if 'vsign' in m:
        c,a,b=m['vsign']; return min(VF,((b-a)*h-8)/(k*1.06))
    r=m.get('awning') or m.get('name')
    if not r: return TF
    rw=(r[2]-r[0])*w; rh=(r[3]-r[1])*h; return min(CF,(rw-4)/(k*.9),max(rh-3,TF))
FIXI=[(590,590,790,768)]
for bx,by in [(490,600),(905,600)]:
    bh=78*260/242; FIXI.append((bx-39,by-bh/2,bx+39,by+bh/2+16))
for cx,ty in [(260,16),(688,10),(1250,16)]: FIXI.append((cx-120,ty,cx+120,ty+82))
def inter(a,b):
    w=min(a[2],b[2])-max(a[0],b[0]); h=min(a[3],b[3])-max(a[1],b[1]); return w*h if w>0 and h>0 else 0
def ar(a): return (a[2]-a[0])*(a[3]-a[1])
def cost(S):   # S: [(key,lotIdx,fi,site?)]
    c=0; B=[]
    for key,li,fi,site in S:
        box,w,h=geom(key,LOTS[li],FS[fi]); B.append(box); wt=.35 if site else 1
        c-=w*8*wt
        if box[0]<4 or box[1]<4 or box[2]>1372: c+=5000
        for f in FIXI:
            o=inter(box,f)
            if o>0: c+=o*10+3000
        if not site:
            lf=labelf(key,box,w,h)
            if lf<TF-.01: c+=(TF-lf)*5000+300
            if key.split('_')[0] in {n.split('_')[0] for n in LIVE}: c+=.3*math.hypot(LOTS[li][0]+LOTS[li][2]/2-GATE[0],LOTS[li][1]-GATE[1])
    for i in range(len(S)):
        for j in range(i+1,len(S)):
            o=inter(B[i],B[j]); m=min(ar(B[i]),ar(B[j]))
            if o>.04*m: c+=(o-.04*m)*8+3000
    return c
res={}
for zi in range(3):
    lots=[i for i,L in enumerate(LOTS) if zl(L)==zi]; names=ZN[zi]
    items=names+['施工中']*(len(lots)-len(names)); random.shuffle(lots)
    S=[[k,lots[i],2,k=='施工中'] for i,k in enumerate(items)]
    cur=cost(S); best=(cur,[list(s) for s in S])
    N=120000
    for it in range(N):
        T=400*(1-it/N)+1; i=random.randrange(len(S)); r=random.random()
        if r<.5:
            j=random.randrange(len(S)); 
            if i==j: continue
            S[i][1],S[j][1]=S[j][1],S[i][1]; c2=cost(S)
            if c2<cur or random.random()<math.exp((cur-c2)/T): cur=c2
            else: S[i][1],S[j][1]=S[j][1],S[i][1]
        else:
            o=S[i][2]; S[i][2]=max(0,min(len(FS)-1,o+random.choice([-1,1]))); c2=cost(S)
            if c2<cur or random.random()<math.exp((cur-c2)/T): cur=c2
            else: S[i][2]=o
        if cur<best[0]: best=(cur,[list(s) for s in S])
    S=best[1]; print('zone',zi,'cost',round(best[0]))
    # 檢查
    B=[geom(k,LOTS[l],FS[f])[0] for k,l,f,_ in S]
    for i in range(len(S)):
        for j in range(i+1,len(S)):
            o=inter(B[i],B[j])/min(ar(B[i]),ar(B[j]))
            if o>.05: print('  重疊',S[i][0],S[j][0],round(o,2))
    for k,l,f,s in S:
        if not s:
            b,w,h=geom(k,LOTS[l],FS[f]); lf=labelf(k,b,w,h)
            print('  ',k,'空地',l,'f',FS[f],'字級px@1024 %.1f'%(lf*.702))
    res[zi]=S
d100={k:[l,FS[f]] for k,l,f,s in res[0] if not s}; d1000={k:[l,FS[f]] for k,l,f,s in res[1] if not s}; d10000={k:[l,FS[f]] for k,l,f,s in res[2] if not s}
site={l:FS[f] for z in res.values() for k,l,f,s in z if s}
out={'LOTS':LOTS,'PLOTS':{100:d100,1000:d1000,10000:d10000},'SITE':site}
json.dump(out,open('/tmp/claude-0/-home-user/388d1732-fa0e-52bd-8614-752200eca8ee/scratchpad/lots_out.json','w'),ensure_ascii=False)
print(json.dumps(out['PLOTS'],ensure_ascii=False)); print(json.dumps(site)); print(json.dumps(LOTS))
