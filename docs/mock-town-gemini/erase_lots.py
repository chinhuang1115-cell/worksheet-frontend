# 把底圖 A 的淡米色空地（含外框與陰影）抹成周圍的草地：python3 erase_lots.py → bgA_nolots.png
# 使用者 2026-11-18：空地和店的坐向對不上，看起來亂，請移除。
# 做法：每塊空地＝一個連通區塊，擴張蓋住外框陰影，用「外圍一圈最常見的顏色」（＝草地）平塗，邊緣羽化。
# 試過無效：由外往內鄰居平均（擴散補色）→ 留下菱形紋與深色殘影。
from PIL import Image, ImageFilter
import numpy as np
from collections import deque, Counter
src=Image.open('bgA.png').convert('RGB'); im=np.array(src)
R,G,B=[im[...,i].astype(int) for i in range(3)]
lot=(R>240)&(G>215)&(G<240)&(B>195)&(B<230)&(R-B>15)
h,w=lot.shape; lab=np.zeros((h,w),int); n=0
for y in range(0,h,2):
    for x in range(0,w,2):
        if lot[y,x] and not lab[y,x]:
            n+=1; q=deque([(y,x)]); lab[y,x]=n; cnt=0
            while q:
                cy,cx=q.popleft(); cnt+=1
                for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                    ny,nx=cy+dy,cx+dx
                    if 0<=ny<h and 0<=nx<w and lot[ny,nx] and not lab[ny,nx]: lab[ny,nx]=n; q.append((ny,nx))
            if cnt<600: lab[lab==n]=0
out=src.copy(); kept=0
for k in range(1,n+1):
    comp=lab==k
    if not comp.any(): continue
    kept+=1
    ys,xs=np.nonzero(comp); y0,y1,x0,x1=max(ys.min()-30,0),min(ys.max()+30,h),max(xs.min()-30,0),min(xs.max()+30,w)
    c=Image.fromarray((comp[y0:y1,x0:x1]*255).astype(np.uint8))
    inner=np.array(c.filter(ImageFilter.MaxFilter(23)))>0
    ring=(np.array(c.filter(ImageFilter.MaxFilter(35)))>0)&~inner
    px=im[y0:y1,x0:x1][ring].astype(int); px=px[(px[:,1]>px[:,0]+12)&(px[:,1]>px[:,2]+30)]//8*8   # 只取綠色（草地），路面不算
    col=Counter(map(tuple,px)).most_common(1)[0][0]; col=tuple(int(v)+4 for v in col)
    patch=Image.new('RGB',(x1-x0,y1-y0),col)
    a=Image.fromarray((inner*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5))
    region=out.crop((x0,y0,x1,y1)); region.paste(patch,(0,0),a); out.paste(region,(x0,y0))
out.save('bgA_nolots.png'); print('lots erased',kept)
