# 把 docs/mock-town-gemini 的底圖與去背店家圖整理成 games/town/：底圖 bg.webp、店家依 alpha 外框裁邊、縮到最長邊 260px 的 WebP，並寫 meta.json（名稱 → 檔名與寬高）。
# 用法：python3 docs/mock-town-gemini/build_town.py（從 repo 根目錄）
import json, glob, os
from PIL import Image
src='docs/mock-town-gemini/'; out='games/town/'; os.makedirs(out,exist_ok=True)
bg=Image.open(src+'bgA_nolots.png').convert('RGB'); bg.save(out+'bg.webp',quality=80,method=6)

# 名字錨點（店圖內的比例座標，0～1）。awning＝雨棚（條紋）正面範圍，店名寫在裡面；vsign＝[中心x,上緣y,下緣y] 直式招牌（三層樓以上）；
# name＝沒有雨棚的場所（公車站、動物園…）寫名字的範圍。新店圖要補一筆，否則 games/index.html 退回名牌貼底邊。
# 數值是看圖（docs/mock-town-gemini/anchors_check.py 會畫疊圖）人工量的。
ANCH={
 '中式餐館':{'awning':[.05,.43,.66,.62]},'便當店':{'awning':[.04,.55,.62,.69]},'文具店':{'awning':[.04,.38,.47,.54]},
 '早餐店':{'awning':[.03,.40,.66,.59]},'書店':{'awning':[.04,.55,.60,.70]},'服飾店_100':{'awning':[.04,.37,.58,.51]},
 '服飾店_1000':{'awning':[.05,.54,.60,.70]},'水果行':{'awning':[.12,.62,.88,.73]},'玩具店':{'awning':[.04,.40,.60,.57]},
 '糖果餅乾店':{'awning':[.04,.34,.64,.55]},'運動用品店':{'awning':[.10,.61,.88,.73]},'電影院':{'awning':[.12,.52,.88,.64]},
 '鞋店':{'awning':[.05,.53,.64,.70]},'飲料店':{'awning':[.06,.47,.62,.65]},'麵包店':{'awning':[.05,.31,.58,.56]},
 '家具行':{'vsign':[.72,.22,.70]},'家電行':{'vsign':[.66,.24,.64]},'腳踏車店':{'vsign':[.68,.22,.66]},'電腦用品店':{'vsign':[.68,.27,.74]},
 '樂器行':{'vsign':[.70,.27,.72]},'服飾店_10000':{'vsign':[.82,.27,.72]},'飯店':{'vsign':[.66,.12,.62]},
 '高鐵站':{'name':[.22,.50,.72,.78]},'公車站':{'name':[.15,.04,.72,.20]},'動物園':{'name':[.26,.25,.66,.41]},
 '博物館':{'name':[.15,.48,.85,.60]},'火車站':{'name':[.10,.56,.90,.76]},'遊樂園':{'name':[.30,.47,.78,.64]},'銀行':{'name':[.25,.42,.78,.60]},
}
meta={}
for f in sorted(glob.glob(src+'shop_*.png')):
    name=os.path.basename(f)[5:-4]; im=Image.open(f).convert('RGBA')
    a=im.getchannel('A').point(lambda v:255 if v>40 else 0); bb=a.getbbox(); im=im.crop(bb)
    k=260/max(im.size); im=im.resize((max(1,round(im.width*k)),max(1,round(im.height*k))),Image.LANCZOS)
    fn=f'shop_{name}.webp'; im.save(out+fn,quality=82,method=6)
    meta[name]={'f':fn,'w':im.width,'h':im.height}
    if name in ANCH: meta[name].update(ANCH[name])
json.dump(meta,open(out+'meta.json','w'),ensure_ascii=False,indent=0)
print(len(meta),'shops',sum(os.path.getsize(out+x) for x in os.listdir(out))//1024,'KB')
