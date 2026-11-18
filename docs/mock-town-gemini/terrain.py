# 從底圖 bgA_nolots.png 做「地形遮罩」：道路／河與天空／樹與樹叢／城堡／銀行／區名牌，其餘＝草地。輸出 terrain.npz（供 place_shops.py）與 terrain.png（疊圖，自己看）。
# 用法：python3 docs/mock-town-gemini/terrain.py（從 repo 根目錄）。顏色分類＋形態學處理，座標＝1376×768。
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
D='docs/mock-town-gemini/'
im=np.array(Image.open(D+'bgA_nolots.png').convert('RGB')).astype(int); R,G,B=im[...,0],im[...,1],im[...,2]
H,W=R.shape
blue=(B>R+25)&(B>G-35)                                   # 天空、河
road=(R>=G-8)&(R>B+18)&~blue                             # 米色小路、石板大道、灰粉大馬路與圓環（草地 g>r）
tree=(G<196)&(R<152)&~blue&~road                         # 樹與樹叢（深綠）
road=ndi.binary_opening(road,iterations=1)
blue=ndi.binary_opening(blue,iterations=1); tree=ndi.binary_opening(tree,iterations=1)
# 城堡（含兩旁灌木）、銀行（河上木橋旁、山丘小路旁）、區名牌、畫面外框：固定矩形
fixed=np.zeros((H,W),bool)
def rect(x0,y0,x1,y1): fixed[max(0,y0):y1,max(0,x0):x1]=True
rect(610,610,770,768)
for bx,by in [(490,600),(905,600)]:
    bh=int(78*260/242); rect(bx-42,by-bh//2-4,bx+42,by+bh//2+18)
for cx,ty in [(260,16),(688,10),(1250,16)]: rect(cx-120,ty,cx+120,ty+82)
rect(0,0,W,4); rect(0,H-4,W,H); rect(0,0,4,H); rect(W-4,0,W,H)
# 草地連通區：只留面積夠大的草地（被道路切成的小角落若放不下店就沒用，由排位置腳本用距離圖判斷）
np.savez_compressed(D+'terrain.npz',blue=blue,road=road,tree=tree,fixed=fixed)
Image.fromarray(np.stack([blue,road,tree|fixed],2).astype(np.uint8)*255).save(D+'terrain_mask.png')   # 給 town_check.js 用：R＝河與天空、G＝道路、B＝樹／固定物
ov=im.copy().astype(float)
for m,c in [(blue,(0,90,255)),(road,(255,60,60)),(tree,(0,0,0)),(fixed,(255,0,255))]:
    ov[m]=ov[m]*.45+np.array(c)*.55
Image.fromarray(ov.astype(np.uint8)).save(D+'terrain.png'); print('ok',[int(m.sum()) for m in (blue,road,tree,fixed)])
