import math
exec(open('mk.py').read().split("Z=[")[0])   # 取 LOTS 等常數
Z=[('巷口小街','100 元以內','#f97316',[('早餐店','早餐店'),('麵包店','麵包店'),('文具店','文具店'),('糖果餅乾店','糖果餅乾店'),('玩具店','玩具店'),('飲料店','飲料店'),('中式餐館','中式餐館'),('服飾店','服飾店_100'),('公車站','公車站'),('動物園','動物園')]),
   ('熱鬧大街','1000 元以內','#2563eb',[('服飾店','服飾店_1000'),('鞋店','鞋店'),('便當店','便當店'),('書店','書店'),('運動用品店','運動用品店'),('水果行','水果行'),('電影院','電影院'),('博物館','博物館'),('火車站','火車站')]),
   ('百貨商場','10000 元以內','#9333ea',[('家電行','家電行'),('腳踏車店','腳踏車店'),('電腦用品店','電腦用品店'),('家具行','家具行'),('樂器行','樂器行'),('服飾店','服飾店_10000'),('高鐵站','高鐵站'),('遊樂園','遊樂園'),('飯店','飯店')])]
LIVE={'早餐店','麵包店','文具店','糖果餅乾店','玩具店'}
WIDE={'公車站':1.15,'動物園':1.2,'高鐵站':1.35,'火車站':1.35,'遊樂園':1.35,'施工中':1.05}
K=1100/1376; v='A'; gx,gy=GATE[v]; zones=[[],[],[]]
for L in LOTS[v]:
    cx=L[0]+L[2]/2; zones[0 if cx<CUT[v][0] else (1 if cx<CUT[v][1] else 2)].append(L)
items=[]
for zi,(nm,sub,col,places) in enumerate(Z):
    lots=sorted(zones[zi],key=lambda L:math.hypot(L[0]+L[2]/2-gx,L[1]+L[3]-gy))
    for i,L in enumerate(lots):
        if i<len(places): items.append((zi,places[i][0],places[i][1],L))
        else: items.append((zi,None,'施工中',L))
items.sort(key=lambda t:t[3][1]+t[3][3])
h=''
for zi,label,img,L in items:
    live=label in LIVE and zi==0
    w=L[2]*[1.0,0.95,0.78][zi]*WIDE.get(img,1)*K; x=(L[0]+L[2]/2)*K-w/2; yb=(L[1]+L[3]*0.95)*K
    cls='s'+('' if live else (' soon' if zi==0 else ' lk'))
    lab='' if label is None else f'<b>{label}</b>'
    rib='<i>即將開幕</i>' if (zi==0 and not live and label) else ''
    h+=f'<div class="{cls}" style="left:{x:.0f}px;top:{yb:.0f}px;width:{w:.0f}px"><img src="shop_{img}.png">{lab}{rib}</div>'
for zi,(nm,sub,col,_) in enumerate(Z):
    lx,ly=ZLAB[v][zi]
    h+=f'<div class="z{" lk" if zi else ""}" style="left:{lx*K:.0f}px;top:{ly*K:.0f}px"><b style="background:{col if not zi else "#9ca3af"}">{nm}{" 🔒" if zi else ""}</b><span>{sub}</span></div>'
for bx,by in BANK[v]:
    h+=f'<div class="bank" style="left:{bx*K:.0f}px;top:{by*K:.0f}px"><img src="shop_銀行.png"><b>銀行</b></div>'
css=open('prev_A.html').read().split('<style>')[1].split('</style>')[0]
css+='''.s.soon img{filter:saturate(.55) brightness(1.05)} .s.lk img{filter:grayscale(.85) brightness(1.08)} .s b{z-index:5} .s.lk b{color:#6b7280;border-color:#9ca3af}
.s i{top:auto;bottom:6px} .bank{width:58px} .bank img{width:100%;display:block} .bank b{font-size:12px}'''
open('prev_A2.html','w').write(f'<!doctype html><meta charset="utf-8"><style>{css}</style><img class="bg" src="bgA.png">{h}<div class="tag">底圖 A＋26 間 Gemini 店（彩色＝能玩、淡色＝即將開幕、灰色＝鎖住）</div>')
