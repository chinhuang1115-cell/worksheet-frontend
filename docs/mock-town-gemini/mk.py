import json, math
LOTS={'A':[(80,314,50,66),(86,402,68,82),(94,234,72,62),(166,180,76,56),(178,362,70,72),(196,540,70,62),(236,446,96,72),(244,268,78,74),(256,148,74,50),(274,574,90,60),(314,220,62,62),(348,134,72,42),(364,326,76,80),(394,436,88,92),(422,230,52,68),(578,106,68,42),(582,390,62,74),(584,284,60,72),(586,180,60,70),(596,500,50,52),(726,106,70,42),(728,180,60,70),(728,284,62,72),(728,500,50,52),(730,390,62,74),(896,446,76,74),(930,384,78,64),(940,250,88,66),(954,326,88,66),(978,140,64,54),(1008,530,82,66),(1048,466,88,70),(1056,138,84,52),(1090,400,96,74),(1170,354,92,74),(1218,198,88,64)],
'B':[(82,274,70,80),(92,388,72,78),(136,198,76,76),(176,308,70,86),(182,478,78,74),(208,150,76,68),(248,240,74,70),(248,406,74,70),(282,540,80,70),(294,122,72,64),(354,204,72,70),(384,564,74,58),(392,286,64,74),(414,380,64,76),(588,78,66,54),(588,160,68,54),(588,238,68,54),(588,322,68,58),(588,404,66,54),(720,78,66,54),(720,164,66,54),(720,244,66,54),(720,330,66,54),(720,410,66,54),(874,372,92,84),(934,274,72,66),(974,210,72,68),(992,462,94,90),(1022,108,78,74),(1096,150,78,78),(1110,452,78,76),(1204,228,86,80),(1204,360,78,72)]}
CUT={'A':(530,860),'B':(560,830)}
GATE={'A':(688,660),'B':(690,690)}
BANK={'A':[(490,600),(905,600)],'B':[(600,560),(860,590)]}
ZLAB={'A':[(260,70),(688,40),(1150,90)],'B':[(260,90),(688,30),(1150,60)]}
Z=[('巷口小街','100 元以內','#f97316',['早餐店','麵包店','文具店','糖果餅乾店','玩具店','飲料店','中式餐館','服飾店','公車站','動物園']),
   ('熱鬧大街','1000 元以內','#2563eb',['服飾店','鞋店','便當店','書店','運動用品店','水果行','電影院','博物館','火車站']),
   ('百貨商場','10000 元以內','#9333ea',['家電行','腳踏車店','電腦用品店','家具行','樂器行','服飾店','高鐵站','遊樂園','飯店'])]
LIVE={'早餐店','麵包店','文具店','糖果餅乾店'}
IMG=['早餐店','麵包店','文具店','糖果餅乾店']
K=1100/1376
for v in 'AB':
    gx,gy=GATE[v]; zones=[[],[],[]]
    for L in LOTS[v]:
        cx=L[0]+L[2]/2; zi=0 if cx<CUT[v][0] else (1 if cx<CUT[v][1] else 2); zones[zi].append(L)
    h=''
    for zi,(nm,sub,col,places) in enumerate(Z):
        lots=sorted(zones[zi],key=lambda L:math.hypot(L[0]+L[2]/2-gx,L[1]+L[3]-gy))
        lots=lots[:len(places)]
        # 畫的順序：上面的先畫
        items=list(zip(places,lots)); items.sort(key=lambda t:t[1][1])
        for i,(p,L) in enumerate(items):
            live=p in LIVE
            if live:
                w=L[2]*1.05*K; x=(L[0]+L[2]/2)*K-w/2; yb=(L[1]+L[3]*0.92)*K
                h+=f'<div class="s" style="left:{x:.0f}px;top:{yb:.0f}px;width:{w:.0f}px"><img src="shop_{p}.png"><b>{p}</b></div>'
            else:
                h+=(f'<div class="lot{" lk" if zi else ""}" style="left:{L[0]*K:.0f}px;top:{L[1]*K:.0f}px;width:{L[2]*K:.0f}px;height:{L[3]*K:.0f}px">'
                    f'<span>{p}</span>{"" if zi else "<i>即將開幕</i>"}</div>')
        lx,ly=ZLAB[v][zi]
        h+=f'<div class="z{" lk" if zi else ""}" style="left:{lx*K:.0f}px;top:{ly*K:.0f}px"><b>{nm}{" 🔒" if zi else ""}</b><span>{sub}</span></div>'
    for bx,by in BANK[v]:
        h+=f'<div class="bank" style="left:{bx*K:.0f}px;top:{by*K:.0f}px">🏦<b>銀行</b></div>'
    bg='bgA.png' if v=='A' else 'bgB_clean.png'
    html=f'''<!doctype html><meta charset="utf-8"><style>
body{{margin:0;width:1100px;height:614px;position:relative;font-family:"Noto Sans TC",sans-serif;overflow:hidden}}
.bg{{position:absolute;inset:0;width:1100px;height:614px}}
.s{{position:absolute;transform:translateY(-100%);text-align:center}}
.s img{{width:100%;display:block}}
.s b{{position:absolute;left:50%;bottom:-16px;transform:translateX(-50%);white-space:nowrap;background:#fff;border:2px solid #3b2f2f;border-radius:10px;padding:0 6px;font-size:12px;line-height:17px}}
.s i{{position:absolute;left:50%;top:38%;transform:translate(-50%,-50%) rotate(-8deg);white-space:nowrap;background:#fff;border:1.5px solid #6b7280;color:#6b7280;font-style:normal;font-weight:800;font-size:10px;padding:0 4px;border-radius:4px}}
/*x*/.lot{{position:absolute;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;border:2px dashed #b45309;border-radius:9px;background:#fff8}} .lot span{{font-size:11px;font-weight:800;color:#78350f;white-space:nowrap}} .lot i{{font-style:normal;font-size:9px;font-weight:800;color:#fff;background:#f59e0b;border-radius:4px;padding:0 3px}} .lot.lk{{border-color:#9ca3af;background:#e5e7eb99}} .lot.lk span{{color:#6b7280}}
.s.off img{{filter:grayscale(1) brightness(1.08);opacity:.75}}
.s.off b{{color:#6b7280;border-color:#9ca3af}}
.z{{position:absolute;transform:translate(-50%,0);text-align:center}}
.z b{{display:block;background:#f97316;color:#fff;font-size:20px;padding:2px 16px;border-radius:18px;border:3px solid #3b2f2f}}
.z.lk b{{background:#9ca3af}} .z span{{display:inline-block;margin-top:2px;background:#fffd;border-radius:8px;padding:0 8px;font-weight:800;font-size:13px}}
.bank{{position:absolute;transform:translate(-50%,-50%);font-size:34px;text-align:center;line-height:1}}
.bank b{{display:block;font-size:12px;background:#facc15;border:2px solid #3b2f2f;border-radius:10px;padding:0 6px;margin-top:-2px}}
.tag{{position:absolute;left:10px;bottom:10px;background:#111827;color:#fff;font-weight:800;padding:3px 10px;border-radius:8px;font-size:14px}}
</style><img class="bg" src="{bg}">{h}<div class="tag">{v}：{"小河＋木橋、樹林＋山丘" if v=="A" else "花田＋矮樹叢、山丘＋池塘"}（Gemini 底圖＋程式放店）</div>'''
    open(f'prev_{v}.html','w').write(html)
