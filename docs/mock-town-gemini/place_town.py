# 自動找「店名牌不被蓋、店圖重疊 ≤10%」的店位置（起點＝mk.py 的空地 LOTS 與 mk2.py 的分配），結果手抄進 games/index.html 的 PLOTS。
# 用法：python3 docs/mock-town-gemini/place_town.py [seed]   輸出 JSON 的 PLOTS 表與違規統計
import json, math, random, sys
exec(open('docs/mock-town-gemini/mk.py').read().split("Z=[")[0])
LOTS=LOTS['A']; CUT=CUT['A']; BANKP=BANK['A']
M=json.load(open('games/town/meta.json'))
Z=[('巷口小街',['早餐店','麵包店','文具店','糖果餅乾店','玩具店','飲料店','中式餐館','服飾店_100','公車站','動物園']),
   ('熱鬧大街',['服飾店_1000','鞋店','便當店','書店','運動用品店','水果行','電影院','博物館','火車站']),
   ('百貨商場',['家電行','腳踏車店','電腦用品店','家具行','樂器行','服飾店_10000','高鐵站','遊樂園','飯店'])]
ZB=[(0,CUT[0]),(CUT[0],CUT[1]),(CUT[1],1376)]
FS=17
ZPLATE=[(260,16),(688,10),(1150,16)]  # 區名牌 中心x, 上緣y；大小 ZW×ZH
ZW=[250,250,250]; ZH=82
def lab(n): return len(n.split('_')[0])*FS+16
def zone_of(cx): return 0 if cx<CUT[0] else (1 if cx<CUT[1] else 2)
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
zl=[[],[],[]]
for L in LOTS: zl[zone_of(L[0]+L[2]/2)].append(L)
GX,GY=688,660
for z in zl: z.sort(key=lambda L:math.hypot(L[0]+L[2]/2-GX,L[1]+L[3]-GY))
shops=[]
for zi,(nm,names) in enumerate(Z):
    for i,n in enumerate(names):
        L=zl[zi][i]; m=M[n]; w=L[2]*1.0
        shops.append(dict(n=n,z=zi,x=L[0]+L[2]/2,y=L[1]+L[3]*.95,w=max(60,min(120,w*1.1))))
def img(s):
    m=M[s['n']]; h=s['w']*m['h']/m['w']; return (s['x']-s['w']/2,s['y']-h,s['x']+s['w']/2,s['y'])
def plate(s):
    w=lab(s['n']); return (s['x']-w/2,s['y']-3,s['x']+w/2,s['y']+19)
FIX_IMG=[]; FIX_PLATE=[]
for (bx,by) in BANKP:
    bw=78; bh=bw*260/242; FIX_IMG.append((bx-bw/2,by-bh/2,bx+bw/2,by+bh/2)); FIX_PLATE.append((bx-62,by+bh/2-3,bx+62,by+bh/2+19))
for zi,(cx,ty) in enumerate(ZPLATE):
    FIX_PLATE.append((cx-ZW[zi]/2,ty,cx+ZW[zi]/2,ty+ZH)); FIX_IMG.append((cx-ZW[zi]/2,ty,cx+ZW[zi]/2,ty+ZH))
FIX_IMG.append((590,590,790,768))  # 城堡入口
def inter(a,b,m=0):
    w=min(a[2],b[2]+m)-max(a[0],b[0]-m); h=min(a[3],b[3]+m)-max(a[1],b[1]-m); return w*h if w>0 and h>0 else 0
def area(a): return (a[2]-a[0])*(a[3]-a[1])
def cost(S):
    c=0; I=[img(s) for s in S]; P=[plate(s) for s in S]
    for i,s in enumerate(S):
        a=I[i]
        if a[0]<6 or a[1]<6 or a[2]>1370 or a[3]>762 or P[i][3]>764: c+=5000
        lo,hi=ZB[s['z']]
        if s['x']<lo+25 or s['x']>hi-25: c+=3000
        for j in range(i+1,len(S)):
            o=inter(a,I[j])
            ex=o-0.05*min(area(a),area(I[j]))
            if ex>0: c+=ex*3+800
            c+=inter(P[i],I[j],2)*10+inter(P[j],a,2)*10+inter(P[i],P[j],3)*10
            if inter(P[i],I[j],2)>0 or inter(P[j],a,2)>0 or inter(P[i],P[j],3)>0: c+=800
        for f in FIX_IMG:
            o=inter(a,f); 
            if o>0: c+=o*10+800
            if inter(P[i],f,2)>0: c+=inter(P[i],f,2)*10+800
        for f in FIX_PLATE:
            if inter(a,f,2)>0: c+=inter(a,f,2)*10+800
            if inter(P[i],f,3)>0: c+=inter(P[i],f,3)*10+800
        c-=s['w']*6
        # 離空地中心不要太遠
        d=min(math.hypot(s['x']-(L[0]+L[2]/2),s['y']-(L[1]+L[3]*.95)) for L in zl[s['z']])
        c+=max(0,d-45)*20+d*0.3
    return c
S=shops; cur=cost(S); T=3000.0
best=None
for it in range(60000):
    T=3000*(1-it/60000)+5
    i=random.randrange(len(S)); s=S[i]; old=dict(s); r=random.random()
    if r<.35: s['x']+=random.gauss(0,12); s['y']+=random.gauss(0,12)
    elif r<.6: s['w']=max(56,min(130,s['w']+random.choice([-6,-3,3,6])))
    elif r<.8:
        L=random.choice(zl[s['z']]); s['x']=L[0]+L[2]/2+random.gauss(0,15); s['y']=L[1]+L[3]*.95+random.gauss(0,15)
    else:
        j=random.randrange(len(S))
        if S[j]['z']==s['z'] and j!=i:
            o=dict(S[j]); S[j]['x'],S[j]['y']=s['x'],s['y']; s['x'],s['y']=o['x'],o['y']
            c2=cost(S)
            if c2<cur or random.random()<math.exp((cur-c2)/T): cur=c2
            else: s['x'],s['y']=S[j]['x'],S[j]['y']; S[j]['x'],S[j]['y']=o['x'],o['y']
            continue
    c2=cost(S)
    if c2<cur or random.random()<math.exp((cur-c2)/T): cur=c2
    else: s.update(old)
    if best is None or cur<best[0]: best=(cur,[dict(x) for x in S])
S=best[1]; print('cost',best[0])
# 統計違規
I=[img(s) for s in S]; P=[plate(s) for s in S]; bad=0
for i in range(len(S)):
    for j in range(i+1,len(S)):
        o=inter(I[i],I[j])/min(area(I[i]),area(I[j]))
        if o>.10: bad+=1; print('img',S[i]['n'],S[j]['n'],round(o,2))
        if inter(P[i],I[j],2) or inter(P[j],I[i],2) or inter(P[i],P[j],3): bad+=1; print('plate',S[i]['n'],S[j]['n'])
print('bad',bad)
json.dump({'S':S,'ZPLATE':ZPLATE},open('/tmp/place_out.json','w'),ensure_ascii=False)
# 沒用到的空地放「施工中」：寬度從空地寬往下試，直到不碰任何店圖／名牌／固定物（重疊 ≤5%）
spare=[[],[],[]]
CM=M['施工中']
placed=[(img(s),plate(s)) for s in S]
for zi in range(3):
    for L in sorted(zl[zi],key=lambda L:(L[1],L[0])):
        x=L[0]+L[2]/2; y=L[1]+L[3]*.95
        for w in range(int(max(L[2]*1.15,70)),40,-4):
            h=w*CM['h']/CM['w']; r=(x-w/2,y-h,x+w/2,y)
            if r[0]<6 or r[1]<6 or r[2]>1370: continue
            ok=all(inter(r,a)<=.05*min(area(r),area(a)) and inter(r,p,2)==0 for a,p in placed)
            ok=ok and all(inter(r,f)==0 for f in FIX_IMG) and all(inter(r,f,2)==0 for f in FIX_PLATE)
            ok=ok and all(inter(r,q)<=.05*area(r) for q in [c for c,_ in [((sx-sw/2,sy-sw*CM['h']/CM['w'],sx+sw/2,sy),0) for sx,sy,sw in [tuple(v) for z in spare for v in z]]])
            if ok: spare[zi].append([round(x),round(y),w]); break
for zi in range(3): print('spare',zi,len(spare[zi]),spare[zi])
out={}
for s in S: out.setdefault(s['z'],{})[s['n']]=[round(s['x']),round(s['y']),round(s['w'])]
for zi in range(3): print(zi,json.dumps(out[zi],ensure_ascii=False),'\n spare',json.dumps(spare[zi]))
json.dump({'plots':out,'spare':spare,'zplate':ZPLATE},open('/tmp/place_out.json','w'),ensure_ascii=False)
