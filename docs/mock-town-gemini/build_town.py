# 把 docs/mock-town-gemini 的底圖與去背店家圖整理成 games/town/：底圖 bg.webp、店家依 alpha 外框裁邊、縮到最長邊 260px 的 WebP，並寫 meta.json（名稱 → 檔名與寬高）。
# 用法：python3 docs/mock-town-gemini/build_town.py（從 repo 根目錄）
import json, glob, os
from PIL import Image
src='docs/mock-town-gemini/'; out='games/town/'; os.makedirs(out,exist_ok=True)
bg=Image.open(src+'bgA.png').convert('RGB'); bg.save(out+'bg.webp',quality=80,method=6)
meta={}
for f in sorted(glob.glob(src+'shop_*.png')):
    name=os.path.basename(f)[5:-4]; im=Image.open(f).convert('RGBA')
    a=im.getchannel('A').point(lambda v:255 if v>40 else 0); bb=a.getbbox(); im=im.crop(bb)
    k=260/max(im.size); im=im.resize((max(1,round(im.width*k)),max(1,round(im.height*k))),Image.LANCZOS)
    fn=f'shop_{name}.webp'; im.save(out+fn,quality=82,method=6)
    meta[name]={'f':fn,'w':im.width,'h':im.height}
json.dump(meta,open(out+'meta.json','w'),ensure_ascii=False,indent=0)
print(len(meta),'shops',sum(os.path.getsize(out+x) for x in os.listdir(out))//1024,'KB')
