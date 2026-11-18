from PIL import Image, ImageDraw, ImageFilter
import numpy as np
SHEETS={'巷口1':(['玩具店','飲料店','中式餐館','服飾店_100'],0),'巷口2':(['公車站','動物園','銀行','施工中'],20000),
 '大街1':(['服飾店_1000','鞋店','便當店','書店'],0),'大街2':(['運動用品店','水果行','電影院','博物館'],0),
 '商場1':(['家電行','腳踏車店','電腦用品店','家具行'],0),'商場2':(['樂器行','服飾店_10000','高鐵站','飯店'],0),'其他':(['火車站','遊樂園'],20000)}
def cut(src,minhole):
    r=np.array(Image.open(src).convert('RGB'));h,w=r.shape[:2]
    m=Image.fromarray(((r.min(axis=2)>232)*255).astype(np.uint8)).copy()
    for p in [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]:
        if m.getpixel(p)==255: ImageDraw.floodfill(m,p,128)
    if minhole:
        for y in range(0,h,12):
            for x in range(0,w,12):
                if m.getpixel((x,y))==255:
                    ImageDraw.floodfill(m,(x,y),60); n=m.histogram()[60]
                    to=128 if n>=minhole else 50; m=m.point(lambda v,to=to: to if v==60 else v)
    bg=np.array(m)==128
    a=Image.fromarray(((~bg)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    im=Image.fromarray(r).convert('RGBA');im.putalpha(a);return im,np.array(a)
out=[]
for sh,(names,mh) in SHEETS.items():
    im,a=cut(f'raw_{sh}.png',mh)
    cols=(a>20).any(axis=0);runs=[];s=None
    for x,v in enumerate(list(cols)+[False]):
        if v and s is None:s=x
        if not v and s is not None:
            if x-s>60: runs.append((s,x))
            s=None
    print(sh,len(runs),runs)
    for nm,(x0,x1) in zip(names,runs):
        c=im.crop((x0,0,x1,im.height));c=c.crop(c.getbbox());c.save(f'shop_{nm}.png');out.append((nm,c))
        al=np.array(c)[...,3]; print(' ',nm,c.size,'corners',[al[0,0],al[0,-1],al[-1,0],al[-1,-1]])
# magenta 總表
cs=[c.resize((int(c.width*300/c.height),300)) for _,c in out]
rows=[cs[i:i+7] for i in range(0,len(cs),7)]
W=max(sum(c.width for c in r)+20*(len(r)+1) for r in rows);H=len(rows)*320+20
sh=Image.new('RGBA',(W,H),(200,60,140,255));y=20
for r in rows:
    x=20
    for c in r: sh.alpha_composite(c,(x,y));x+=c.width+20
    y+=320
sh.convert('RGB').resize((W//2,H//2)).save('check_all.png')
