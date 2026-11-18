# 店沿路自由擺放（取代舊的 place_lots.py 空地表）。用法：python3 docs/mock-town-gemini/place_shops.py [seed]（從 repo 根目錄；先跑 terrain.py）
# 規則（座標＝1376×768 底圖像素）：
#  1) 底座（店圖 alpha 最下面幾列的實際範圍）整段落在草地上：不碰道路／河與天空／樹／城堡／銀行／區名牌／畫面外框（障礙物外擴 2px）。
#  2) 店要沿著路：底座離最近道路邊 ≤ NEAR（14px；底座中心約 ≤ 寬/2＋14）。
#  3) 依街區分區（河左＝巷口小街、河與樹林之間＝熱鬧大街、樹林右＝百貨商場）；上線的店優先靠近入口。
#  4) 同一區、同一類（雨棚／直式招牌／其他場所）的店寬度一律相同（寬度由「店名放得下 ≥11.4 地圖單位＝1024 寬 8px」決定，取該類所需最大值）。
#  5) 模擬退火：店圖 alpha 重疊 ≤5%、店名牌不被別間店蓋住、店名牌彼此不重疊、店身壓到道路／河／樹的比例盡量小。
#  6) 每區留 2 個「施工中」（要畫出來）＋1 個隱形候選；新增店沒指定位置時 games/index.html 依序取用。
# 輸出：把 games/index.html 裡 /*PLOTS-START*/ … /*PLOTS-END*/ 之間的 PLOTS／SPARE 換掉；同時印出檢查。
import json, math, random, sys, re
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
D='docs/mock-town-gemini/'; T=np.load(D+'terrain.npz'); W,H=1376,768
blue,road,tree,fixed=T['blue'],T['road'],T['tree'],T['fixed']
obs=blue|road|tree|fixed; obsd=ndi.binary_dilation(obs,iterations=2)
dist_road=ndi.distance_transform_edt(~road)
ci=np.pad(obsd.astype(np.int32).cumsum(0).cumsum(1),((1,0),(1,0)))
def obs_sum(x0,y0,x1,y1): return ci[y1,x1]-ci[y0,x1]-ci[y1,x0]+ci[y0,x0]
M=json.load(open('games/town/meta.json'))
CF,VF,TF=13,12.5,11.4
ZN=[['早餐店','麵包店','文具店','糖果餅乾店','玩具店','飲料店','中式餐館','服飾店_100','公車站','動物園'],
    ['服飾店_1000','鞋店','便當店','書店','運動用品店','水果行','電影院','博物館','火車站'],
    ['家電行','腳踏車店','電腦用品店','家具行','樂器行','服飾店_10000','高鐵站','遊樂園','飯店']]
LIVE={'早餐店','麵包店','文具店','糖果餅乾店','玩具店'}; GATE=(688,650); NEAR=14
# 河中心線（依 y）：用來分左／中區
rc=np.full(H,np.nan)
for y in range(110,H):
    xs=np.nonzero(blue[y,300:620])[0]
    if len(xs): rc[y]=300+xs.mean()
ys=np.arange(H); ok=~np.isnan(rc); rc=np.interp(ys,ys[ok],rc[ok])
def zone_ok(z,x,y):
    if z==0: return x<rc[y]-30
    if z==1: return rc[y]+30<x<(815 if y<540 else 860)
    return x>(940 if y<300 else 905)
def klass(key):
    m=M[key]; return 'v' if 'vsign' in m else ('a' if 'awning' in m else 'n')
def need_w(key):
    m=M[key]; k=len(key.split('_')[0])
    if 'vsign' in m:
        c,a,b=m['vsign']; hneed=(TF*k*1.06+8)/(b-a); return hneed*m['w']/m['h']
    r=m.get('awning') or m['name']; return (TF*k*.9+4)/(r[2]-r[0])
def alpha(key,w):
    m=M[key]; h=round(w*m['h']/m['w']); w=round(w)
    a=np.array(Image.open('games/town/'+m['f']).convert('RGBA').getchannel('A').resize((w,h),Image.BILINEAR))>40
    rows=a[-6:]; cols=np.nonzero(rows.any(0))[0]; return a,w,h,(cols.min(),cols.max()+1)
def label_box(key,w,h):   # 店名牌範圍（相對店圖左上，同 games/index.html nameTag 的錨點）
    m=M[key]
    if key=='施工中': return (0,0,0,0)
    if 'vsign' in m:
        c,a,b=m['vsign']; k=len(key.split('_')[0]); f=min(VF,((b-a)*h-8)/(k*1.06)); sw=f*1.35; return (c*w-sw/2,a*h-4,c*w+sw/2,a*h+k*f*1.06+8)
    r=m.get('awning') or m['name']; return (r[0]*w,r[1]*h,r[2]*w,r[3]*h)
BLK=[(cx-122,ty-2,cx+122,ty+86) for cx,ty in [(260,16),(688,10),(1250,16)]]+[(bx-42,by-int(78*260/242)//2-4,bx+42,by+int(78*260/242)//2+18) for bx,by in [(490,600),(905,600)]]
CAP={'a':104,'v':92,'n':104}; MINW={'a':76,'v':58,'n':70}
res={}
for z in range(3):
    names=ZN[z]; cw={}
    for c in 'avn':
        ks=[n for n in names if klass(n)==c]
        if ks: cw[c]=int(min(CAP[c],max(MINW[c],max(need_w(n) for n in ks)))+.99)
    print('zone',z,'class widths',cw,{n:round(need_w(n)) for n in names})
    items=[(n,cw[klass(n)],'shop') for n in names]
    sw=cw.get('a',80); items+=[('施工中',sw,'site'),('施工中',sw,'site'),('施工中',sw,'spare')]
    # 候選位置
    cand=[]
    for key,w,kind in items:
        a,w2,h2,(b0,b1)=alpha(key,w); L=[]
        for y in range(40,H-26,4):
            for x in range(10,W-10,4):
                if not zone_ok(z,x,y): continue
                x0=x-w2//2; bx0,bx1=x0+b0,x0+b1; y0=y-h2
                if y0<4 or x0<4 or x0+w2>W-4: continue
                if obs_sum(bx0,y-5,bx1,y)>0: continue
                if dist_road[y-3,bx0:bx1].min()>NEAR: continue
                body=a; ob=obs[y0:y,x0:x0+w2]
                bo=(body&ob).sum()/max(1,body.sum())          # 店身壓到障礙物的比例
                rd=(body&road[y0:y,x0:x0+w2]).sum()/max(1,body.sum())
                u=bo*900+rd*1200
                for fx0,fy0,fx1,fy1 in BLK:      # 店圖外框不可蓋住區名牌、銀行（含「即將開放」小標）
                    if min(x0+w2,fx1)>max(x0,fx0) and min(y,fy1)>max(y0,fy0): u+=6000
                if key in LIVE: u+=.22*math.hypot(x-GATE[0],y-GATE[1])
                lb=label_box(key,w2,h2)
                L.append((x,y,x0,y0,u,lb))
        cand.append((a,w2,h2,L)); print('  ',key,kind,'w',w2,'候選',len(L))
        if not L: raise SystemExit('沒有候選：'+key)
    def pair(i,s,j,t):
        a,w,h,Li=cand[i]; b,w2,h2,Lj=cand[j]; p=Li[s]; q=Lj[t]
        X0=max(p[2],q[2]); X1=min(p[2]+w,q[2]+w2); Y0=max(p[3],q[3]); Y1=min(p[3]+h,q[3]+h2)
        if X1<=X0 or Y1<=Y0: ov=0;cov=0
        else:
            ai=a[Y0-p[3]:Y1-p[3],X0-p[2]:X1-p[2]]; bi=b[Y0-q[3]:Y1-q[3],X0-q[2]:X1-q[2]]; both=(ai&bi).sum()
            ov=both/min(a.sum(),b.sum())
        c=0
        if X1>X0 and Y1>Y0:
            bf=(X1-X0)*(Y1-Y0)/min(w*h,w2*h2); c+=500*bf   # 店圖外框重疊也扣分：讓店散開、不擠成一團
            if bf>.07: c+=3000+bf*3000
        if ov>.03: c+=(ov-.03)*6000+2500
        # 店名牌被蓋：標示在 (p) 店，若 q 底邊較大（畫在上面）且 q 的 alpha 蓋到 p 的名牌
        def covered(pp,qq,aa_label_key,bb_alpha,w_b,h_b):
            lb=aa_label_key; x0=int(pp[2]+lb[0]);x1=int(pp[2]+lb[2]);y0=int(pp[3]+lb[1]);y1=int(pp[3]+lb[3])
            X0=max(x0,qq[2]);X1=min(x1,qq[2]+w_b);Y0=max(y0,qq[3]);Y1=min(y1,qq[3]+h_b)
            if X1<=X0 or Y1<=Y0: return 0
            return bb_alpha[Y0-qq[3]:Y1-qq[3],X0-qq[2]:X1-qq[2]].sum()
        if q[1]>p[1] and covered(p,q,p[5],b,w2,h2)>0: c+=4000
        if p[1]>q[1] and covered(q,p,q[5],a,w,h)>0: c+=4000
        lp=p[5];lq=q[5]
        if min(p[2]+lp[2],q[2]+lq[2])>max(p[2]+lp[0],q[2]+lq[0])-2 and min(p[3]+lp[3],q[3]+lq[3])>max(p[3]+lp[1],q[3]+lq[1])-2: c+=4000
        # 太靠近（店圖 bbox 間距 <3px）略扣分，避免擠成一團
        return c
    n=len(items); st=[random.randrange(len(cand[i][3])) for i in range(n)]
    PC={}
    def pc(i,s,j,t):
        k=(i,s,j,t) if i<j else (j,t,i,s)
        if k not in PC: PC[k]=pair(k[0],k[1],k[2],k[3])
        return PC[k]
    def cost_i(i,s): return cand[i][3][s][4]+sum(pc(i,s,j,st[j]) for j in range(n) if j!=i)
    cur=sum(cand[i][3][st[i]][4] for i in range(n))+sum(pc(i,st[i],j,st[j]) for i in range(n) for j in range(i+1,n))
    best=(cur,st[:]); N=30000
    for it in range(N):
        Tm=300*(1-it/N)+2; i=random.randrange(n); old=st[i]
        if random.random()<.6:   # 在目前位置附近走
            ox,oy=cand[i][3][old][:2]; nb=[s for s,c in enumerate(cand[i][3]) if abs(c[0]-ox)<60 and abs(c[1]-oy)<60]; new=random.choice(nb)
        else: new=random.randrange(len(cand[i][3]))
        d=cost_i(i,new)-cost_i(i,old)
        if d<0 or random.random()<math.exp(-d/Tm):
            st[i]=new; cur+=d
            if cur<best[0]-1e-9: best=(cur,st[:])
    st=best[1]; print('  cost',round(best[0],1))
    out=[]
    for i,(key,w,kind) in enumerate(items):
        c=cand[i][3][st[i]]; out.append((key,kind,c[0],c[1],cand[i][1]))
        for j in range(i+1,n):
            if pc(i,st[i],j,st[j])>=2000: print('  衝突',key,items[j][0])
        if c[4]>150: print('  店身壓到障礙物 cost',round(c[4]),key)
    res[z]=out
D100={};PL={}
for z,d in enumerate([100,1000,10000]):
    PL[d]={}
    for key,kind,x,y,w in res[z]:
        if kind=='shop': PL[d][key.split('_')[0] if key.startswith('服飾店') else key]=[x,y,w]
SP={d:[[x,y,w,1 if kind=='site' else 0] for key,kind,x,y,w in res[z] if kind!='shop'] for z,d in enumerate([100,1000,10000])}
js='/*PLOTS-START*/\nconst PLOTS='+json.dumps(PL,ensure_ascii=False,separators=(',',':'))+';\nconst SPARE='+json.dumps(SP,separators=(',',':'))+';\n/*PLOTS-END*/'
pass
h=open('games/index.html').read()
if '/*PLOTS-START*/' in h:
    h=re.sub(r'/\*PLOTS-START\*/.*?/\*PLOTS-END\*/',lambda m:js,h,flags=re.S); open('games/index.html','w').write(h); print('index.html 已更新')
else: print('index.html 還沒有 PLOTS 標記')
