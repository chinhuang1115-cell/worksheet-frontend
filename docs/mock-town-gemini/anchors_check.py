# 把 meta.json 的名字錨點（awning／vsign／name）畫在每張店圖上，輸出 docs/mock-town-gemini/anchors.png 供人工確認。
# 用法：python3 docs/mock-town-gemini/anchors_check.py（從 repo 根目錄）
import json
from PIL import Image, ImageDraw
M=json.load(open('games/town/meta.json')); names=[n for n in M if any(k in M[n] for k in('awning','vsign','name'))]
cols=6; rows=(len(names)+cols-1)//cols; S=Image.new('RGB',(cols*270,rows*285),(200,220,200)); d=ImageDraw.Draw(S)
for i,n in enumerate(names):
    m=M[n]; im=Image.open('games/town/'+m['f']).convert('RGBA'); x=(i%cols)*270+5; y=(i//cols)*285+20
    S.paste(im,(x,y),im); d.text((x,y-16),n,fill=(0,0,0))
    if 'vsign' in m:
        c,a,b=m['vsign']; d.rectangle((x+c*m['w']-12,y+a*m['h'],x+c*m['w']+12,y+b*m['h']),outline=(200,0,0),width=2)
    else:
        a=m.get('awning') or m['name']; d.rectangle((x+a[0]*m['w'],y+a[1]*m['h'],x+a[2]*m['w'],y+a[3]*m['h']),outline=(200,0,0),width=2)
S.save('docs/mock-town-gemini/anchors.png')
