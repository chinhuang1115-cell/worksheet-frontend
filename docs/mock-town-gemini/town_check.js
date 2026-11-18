// Gemini 插畫小鎮驗收（2026-11-18 第二版：店放在空地上、店名寫在雨棚／直式招牌）。
// 量每張店圖、店名標示的 bounding box（地圖座標），檢查：
//  - 店位置：每間店底座中心落在某塊空地內、一塊空地最多一間、空地屬於正確街區、底座 ≤ 空地寬 +15%
//  - 店名：落在 meta.json 的錨點內（雨棚／直式招牌／沒雨棚的位置）、不蓋住其他店圖（逐像素 alpha 取樣）、彼此不重疊、1024 寬字級 ≥ 8px
//  - 店圖：重疊 ≤10%、不出地圖、不蓋區名牌／銀行；點店連結、鎖區不可點、手機按鈕列、橫向捲動、JS 錯誤
// 並截圖 g2_*.png（含 g2_lots.png：底圖＋空地框＋店底座點）。用法：node docs/mock-town-gemini/town_check.js（需要 playwright；自己起 python http.server 於 8766）
const {chromium}=require('playwright'),{spawn}=require('child_process'),path=require('path');
const ROOT=path.resolve(__dirname,'../..');
(async()=>{
  const srv=spawn('python3',['-m','http.server','8766'],{cwd:ROOT,stdio:'ignore'});await new Promise(r=>setTimeout(r,1000));
  const b=await chromium.launch();let bad=0;
  for(const [w,h,tag] of [[1280,800,'1280'],[1024,768,'1024'],[390,844,'390']]){
    const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:2});
    const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
    await p.goto('http://localhost:8766/games/index.html');await p.waitForSelector('#mapsvg .shop');await p.waitForTimeout(900);
    await p.addStyleTag({content:'.shop .lift,.plt{transition:none!important}'});
    const r=await p.evaluate(async()=>{
      const svg=document.querySelector('#mapsvg'),sb=svg.getBoundingClientRect(),META=await fetch('town/meta.json').then(r=>r.json());
      const num=(e,a)=>parseFloat(e.getAttribute(a)),box=e=>({x0:num(e,'x'),y0:num(e,'y'),x1:num(e,'x')+num(e,'width'),y1:num(e,'y')+num(e,'height')});
      // 店圖（地圖座標）＋ alpha 取樣用的像素
      const imgs=[];
      for(const e of svg.querySelectorAll('image.simg')){
        const g=e.closest('.shop'),isBank=!!e.closest('.bank'),name=g?.dataset.n||(isBank?'銀行':'施工中'),bx=box(e);
        const key=g?(g.dataset.n==='服飾店'?'服飾店_'+g.dataset.d:g.dataset.n):(isBank?'銀行':'施工中');
        const im=new Image();im.src=e.getAttribute('href');await im.decode();const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const cx=c.getContext('2d');cx.drawImage(im,0,0);
        imgs.push({kind:g?'shop':isBank?'bank':'site',name,key,lot:g?+g.dataset.lot:(e.dataset.lot!==undefined?+e.dataset.lot:-1),d:g?+g.dataset.d:(e.dataset.d?+e.dataset.d:0),...bx,alpha:cx.getImageData(0,0,c.width,c.height),meta:META[key]});}
      const hit=(im,x,y)=>{if(x<im.x0||x>=im.x1||y<im.y0||y>=im.y1)return false;const px=Math.floor((x-im.x0)/(im.x1-im.x0)*im.alpha.width),py=Math.floor((y-im.y0)/(im.y1-im.y0)*im.alpha.height);return im.alpha.data[(py*im.alpha.width+px)*4+3]>40};
      const labels=[...svg.querySelectorAll('.plt')].map(g=>{const rc=g.querySelector('rect.lb'),bb=rc.getBBox(),t=g.querySelector('text');
        const tbs=[...g.querySelectorAll('text')].map(x=>x.getBBox());
        return{name:g.dataset.n,vs:g.classList.contains('vs'),x0:bb.x,y0:bb.y,x1:bb.x+bb.width,y1:bb.y+bb.height,
          tx0:Math.min(...tbs.map(q=>q.x)),tx1:Math.max(...tbs.map(q=>q.x+q.width)),ty0:Math.min(...tbs.map(q=>q.y)),ty1:Math.max(...tbs.map(q=>q.y+q.height)),
          fs:parseFloat(t.getAttribute('font-size'))*sb.width/1376,hasAnc:g.hasAttribute('data-anc')}});
      const bankImgs=imgs.filter(i=>i.kind==='bank'),shopI=imgs.filter(i=>i.kind==='shop');
      const covered=labels.map((L,li)=>{let n=0,tot=0;const own=li<2?bankImgs[li]:shopI[li-2];
        for(let a=0;a<=8;a++)for(let c=0;c<=3;c++){const x=L.x0+(L.x1-L.x0)*a/8,y=L.y0+(L.y1-L.y0)*c/3;tot++;if(imgs.some(i=>i!==own&&i.kind!=='bank'&&hit(i,x,y)))n++}return n});
      const fixed=[...svg.querySelectorAll('.zone')].map((g,i)=>{const q=g.getBBox();return{name:'區名牌'+i,x0:q.x,y0:q.y,x1:q.x+q.width,y1:q.y+q.height}}).concat([...svg.querySelectorAll('.bank .tag')].map((g,i)=>{const q=g.getBBox();return{name:'銀行小標'+i,x0:q.x,y0:q.y,x1:q.x+q.width,y1:q.y+q.height}}));
      return{sc:sb.width/1376,sbw:sb.width,imgs:imgs.map(({alpha,...r})=>r),labels,covered,fixed,LOTS,lotz:LOTS.map((_,i)=>LOTZ(i)),
        doc:{sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth},live:svg.querySelectorAll('.shop.live').length,
        lockClick:[...svg.querySelectorAll('.shop.lock,.shop.soon')].filter(e=>e.hasAttribute('data-id')||e.hasAttribute('tabindex')).length,lockCount:svg.querySelectorAll('.shop.lock').length}});
    const probs=[],ar=a=>(a.x1-a.x0)*(a.y1-a.y0),ov=(a,c,m=0)=>{const ww=Math.min(a.x1,c.x1+m)-Math.max(a.x0,c.x0-m),hh=Math.min(a.y1,c.y1+m)-Math.max(a.y0,c.y0-m);return ww>0&&hh>0?ww*hh:0};
    const shopImgs=r.imgs.filter(i=>i.kind==='shop');
    // 空地：底座中心落在空地內、一塊空地最多一間、街區正確、底座寬 ≤ 空地寬 +15%
    const seen={};
    r.imgs.filter(i=>i.kind!=='bank').forEach(i=>{const L=r.LOTS[i.lot];if(!L){probs.push(`沒有空地：${i.name}`);return}
      const bx=(i.x0+i.x1)/2,by=i.y1-6;
      if(bx<L[0]||bx>L[0]+L[2]||by<L[1]||by>L[1]+L[3])probs.push(`底座中心不在空地內：${i.kind}:${i.name} 空地${i.lot}`);
      if(seen[i.lot])probs.push(`空地 ${i.lot} 放了兩間：${seen[i.lot]}、${i.name}`);seen[i.lot]=i.name;
      if(r.lotz[i.lot]!==i.d)probs.push(`空地街區不符：${i.name} 空地${i.lot}（${r.lotz[i.lot]}）≠ ${i.d}`);
      if((i.x1-i.x0)*0.92>L[2]*1.15+0.5)probs.push(`底座比空地寬超過 15%：${i.name}`)});
    // 店名：錨點、被其他店圖蓋住、互相重疊、字級
    r.labels.forEach((L,i)=>{const im=i<2?r.imgs.filter(s=>s.kind==='bank')[i]:shopImgs[i-2];   // 標示順序＝先 2 間銀行、再依 y 排序的店（同圖順序）
      if(!im||im.name!==L.name){probs.push('標示與店圖對不上：'+L.name);return}if(!im){probs.push('找不到店圖：'+L.name);return}
      const m=im.meta||{},iw=im.x1-im.x0,ih=im.y1-im.y0;
      if(!L.hasAnc)probs.push('沒有錨點（退回底邊小牌）：'+L.name);
      if(m.vsign){const[c,a,bb]=m.vsign,cx=im.x0+c*iw,cx2=(L.x0+L.x1)/2;
        if(Math.abs(cx-cx2)>1||L.y0<im.y0+a*ih-1||L.y1>im.y0+bb*ih+1)probs.push(`直式招牌不在錨點：${L.name}`)}
      else{const q=m.awning||m.name;if(q){const A={x0:im.x0+q[0]*iw,y0:im.y0+q[1]*ih,x1:im.x0+q[2]*iw,y1:im.y0+q[3]*ih};
        if(L.x0<A.x0-1||L.x1>A.x1+1||L.y0<A.y0-2.5||L.y1>A.y1+2.5)probs.push(`店名超出${m.awning?'雨棚':'錨點'}：${L.name}`);}}
      if(tag!=='390'&&(L.tx1>L.x1+.5||L.tx0<L.x0-.5))probs.push(`字超出牌：${L.name}`);
      if(r.covered[i]>0)probs.push(`店名被其他店圖蓋住（${r.covered[i]} 個取樣點）：${L.name}`);
      r.labels.forEach((q,j)=>{if(j>i&&ov(L,q)>0)probs.push(`店名重疊：${L.name} × ${q.name}`)});
      r.fixed.forEach(f=>{if(ov(L,f)>0)probs.push(`店名 × ${f.name}：${L.name}`)})});
    // 店圖：兩兩重疊 ≤10%、不出地圖、不蓋區名牌／銀行小標
    r.imgs.forEach((a,i)=>{
      if(a.x0<-.5||a.x1>1376.5||a.y0<-.5||a.y1>768.5)probs.push(`圖出地圖：${a.name}`);
      r.imgs.forEach((c,j)=>{if(j>i){const o=ov(a,c);if(o/ar(a)>.10||o/ar(c)>.10)probs.push(`圖重疊 ${(100*Math.max(o/ar(a),o/ar(c))).toFixed(0)}%：${a.name} × ${c.name}`)}});
      r.fixed.forEach(f=>{if(ov(a,f)>0&&!(a.kind==='bank'&&/^銀行/.test(f.name)))probs.push(`圖 × ${f.name}：${a.name}`)})});
    const minfs=Math.min(...r.labels.map(q=>q.fs));
    if(w===1024&&minfs<7.99)probs.push(`1024 寬店名字級 ${minfs.toFixed(2)}px < 8`);
    if(r.lockClick)probs.push('鎖區／即將開幕的店可點');
    if(r.live<5)probs.push('上線店少於 5 間：'+r.live);
    if(r.doc.sw>r.doc.cw)probs.push('頁面橫向捲動');
    if(tag!=='390'){await p.click('#mapsvg .shop[data-id="game-toy-1"]')}else{await p.click('#chips button[data-id="game-toy-1"]')}
    await p.waitForTimeout(900);
    const side=await p.evaluate(()=>({nm:document.querySelector('#side .nm').textContent,links:[...document.querySelectorAll('#side .stage')].map(a=>a.getAttribute('href')),on:document.querySelectorAll('#mapsvg .shop.on').length,
      lay:(()=>{const m=document.querySelector('#mapsvg').getBoundingClientRect(),a=document.querySelector('#side').getBoundingClientRect();return{below:a.top>=m.bottom-1,right:a.left>=m.right-1,vis:a.bottom<=innerHeight+2&&a.bottom>0}})(),
      chips:[...document.querySelectorAll('#chips button')].map(b=>({d:b.disabled}))}));
    const ok=/玩具店/.test(side.nm)&&side.links.length===6&&side.links.every((h,i)=>h.includes('/game/toy-shop?')&&h.includes('stage='+(i+1))&&h.includes('lv=2')&&h.includes('mode=faded'));
    if(!ok)probs.push('點玩具店連結有誤');if(side.on!==1)probs.push('選中店數 '+side.on);
    if(w<=1100&&!(side.lay.below&&side.lay.vis))probs.push('平板／手機關卡欄位置');if(w>1100&&!side.lay.right)probs.push('寬螢幕關卡欄不在右側');
    if(tag==='390'){const dis=side.chips.filter(c=>c.d).length;if(dis<10)probs.push('手機鎖區按鈕 disabled 只有 '+dis)}
    if(tag==='1024')await p.screenshot({path:path.join(__dirname,'g2_1024_sel.png')});
    console.log(`${tag}: 店圖 ${r.imgs.length} 張（店 ${shopImgs.length}），店名 ${r.labels.length}，地圖寬 ${r.sbw.toFixed(0)}，店名最小字 ${minfs.toFixed(2)}px，鎖區店 ${r.lockCount}，錯誤 ${errs.length}，問題 ${probs.length}`);
    console.log(`   點玩具店 → ${side.nm}，${side.links.length} 關，連結${ok?'正確':'有誤'}`);
    probs.forEach(x=>console.log('   ',x));errs.forEach(x=>console.log('   JS:',x));bad+=probs.length+errs.length;
    if(tag!=='1024')await p.screenshot({path:path.join(__dirname,`g2_${tag}.png`),fullPage:tag==='390'});
    if(tag==='1280'){ // 空地對照圖：底圖＋空地框＋編號＋店底座點；局部放大
      await p.evaluate(()=>{const svg=document.querySelector('#mapsvg'),ns='http://www.w3.org/2000/svg',g=document.createElementNS(ns,'g');g.id='dbg';
        LOTS.forEach((L,i)=>{g.insertAdjacentHTML('beforeend',`<rect x="${L[0]}" y="${L[1]}" width="${L[2]}" height="${L[3]}" fill="none" stroke="#dc2626" stroke-width="1.5"/><text x="${L[0]+2}" y="${L[1]+9}" font-size="9" fill="#dc2626" font-weight="800">${i}</text>`)});
        svg.querySelectorAll('image.simg').forEach(e=>{const x=+e.getAttribute('x')+e.getAttribute('width')/2,y=+e.getAttribute('y')+ +e.getAttribute('height')-6;g.insertAdjacentHTML('beforeend',`<circle cx="${x}" cy="${y}" r="3.2" fill="#2563eb" stroke="#fff" stroke-width="1"/>`)});svg.appendChild(g)});
      await p.locator('#mapsvg').screenshot({path:path.join(__dirname,'g2_lots.png')});
      await p.evaluate(()=>document.querySelector('#dbg').remove());
      const clip=async(name,x0,y0,x1,y1)=>{const q=await p.evaluate(()=>{const s=document.querySelector('#mapsvg').getBoundingClientRect();return{x:s.left,y:s.top,w:s.width}});const k=q.w/1376;
        const p3=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:3});await p3.goto('http://localhost:8766/games/index.html');await p3.waitForSelector('#mapsvg .shop');await p3.waitForTimeout(900);await p3.addStyleTag({content:'.shop .lift,.plt{transition:none!important}'});
        const s=await p3.evaluate(()=>{const r=document.querySelector('#mapsvg').getBoundingClientRect();return{x:r.left,y:r.top}});
        await p3.screenshot({path:path.join(__dirname,name),clip:{x:s.x+x0*k,y:s.y+y0*k,width:(x1-x0)*k,height:(y1-y0)*k}});await p3.close()};
      await clip('g2_zoom_巷口.png',60,300,420,620);await clip('g2_zoom_商場.png',880,330,1280,620)}
    await p.close()}
  await b.close();srv.kill();console.log(bad?`FAIL ${bad}`:'ALL OK');process.exit(bad?1:0)})();
