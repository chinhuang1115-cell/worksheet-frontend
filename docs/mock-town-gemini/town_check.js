// Gemini 插畫小鎮驗收：量每張店圖、店名牌、區名牌、銀行的 bounding box，檢查重疊／被蓋住／出界／字級／連結／鎖區／手機按鈕列，並截圖。
// 用法：node docs/mock-town-gemini/town_check.js（需要 playwright；會自己起 python http.server 於 8766）
const {chromium}=require('playwright'),{spawn}=require('child_process'),path=require('path');
const ROOT=path.resolve(__dirname,'../..');
(async()=>{
  const srv=spawn('python3',['-m','http.server','8766'],{cwd:ROOT,stdio:'ignore'});await new Promise(r=>setTimeout(r,1000));
  const b=await chromium.launch();let bad=0;
  for(const [w,h,tag] of [[1280,800,'1280'],[1024,768,'1024'],[390,844,'390']]){
    const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:2});
    const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
    await p.goto('http://localhost:8766/games/index.html');await p.waitForSelector('#mapsvg .shop');await p.waitForFunction(()=>[...document.querySelectorAll('#mapsvg image')].every(i=>true));await p.waitForTimeout(900);
    await p.addStyleTag({content:'.shop .lift{transition:none!important}'});
    const r=await p.evaluate(()=>{
      const svg=document.querySelector('#mapsvg'),sb=svg.getBoundingClientRect(),R=e=>{const b=e.getBoundingClientRect();return{x0:b.left,y0:b.top,x1:b.right,y1:b.bottom}};
      const imgs=[...svg.querySelectorAll('image.simg')].map((e,i)=>({kind:e.closest('.shop')?'shop':e.closest('.bank')?'bank':'site',name:e.closest('.shop')?.dataset.n||(e.closest('.bank')?'銀行':'施工中'+i),...R(e)}));
      const plates=[...svg.querySelectorAll('.plt')].map(g=>({name:g.querySelector('text').textContent,...R(g.querySelector('rect')),over:g.querySelector('text').getBoundingClientRect().width-g.querySelector('rect').getBoundingClientRect().width,fs:parseFloat(g.querySelector('text').getAttribute('font-size'))*sb.width/1376}));
      const fixed=[...svg.querySelectorAll('.zone')].map((g,i)=>({name:'區名牌'+i,...R(g)})).concat([...svg.querySelectorAll('.bank .lb')].map((e,i)=>({name:'銀行牌'+i,...R(e)})));
      return{sb:{x0:sb.left,y0:sb.top,x1:sb.right,y1:sb.bottom},imgs,plates,fixed,doc:{sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth},
        live:[...svg.querySelectorAll('.shop.live')].length,lockClick:[...svg.querySelectorAll('.shop.lock,.shop.soon')].filter(e=>e.hasAttribute('data-id')||e.hasAttribute('tabindex')).length,
        lockCount:svg.querySelectorAll('.shop.lock').length}});
    const probs=[],ar=a=>(a.x1-a.x0)*(a.y1-a.y0),ov=(a,c,m=0)=>{const ww=Math.min(a.x1,c.x1+m)-Math.max(a.x0,c.x0-m),hh=Math.min(a.y1,c.y1+m)-Math.max(a.y0,c.y0-m);return ww>0&&hh>0?ww*hh:0};
    const S=r.sb,sc=S.x1-S.x0,tol=sc/1376*3;   // 3 個地圖單位的容許
    // 店名牌：不被任何店圖／其他牌／區名牌／銀行蓋住（自己的店圖除外：牌跟圖同序）
    const shopImgs=r.imgs.filter(i=>i.kind==='shop');
    r.plates.forEach((pl,i)=>{
      r.imgs.forEach(im=>{if(im===shopImgs[i])return;if(ov(pl,im)>0)probs.push(`牌被圖蓋住：${pl.name} × ${im.kind}:${im.name}`)});
      r.plates.forEach((q,j)=>{if(j>i&&ov(pl,q)>0)probs.push(`牌重疊：${pl.name} × ${q.name}`)});
      r.fixed.forEach(f=>{if(ov(pl,f)>0)probs.push(`牌 × ${f.name}：${pl.name}`)});
      if(pl.over>0.5)probs.push(`店名超出名牌：${pl.name}`);
      if(pl.x0<S.x0||pl.x1>S.x1||pl.y0<S.y0||pl.y1>S.y1)probs.push(`牌出地圖：${pl.name}`)});
    // 店圖兩兩重疊 ≤10%（各自面積）；店圖不蓋區名牌／銀行牌
    r.imgs.forEach((a,i)=>{
      if(a.x0<S.x0-.5||a.x1>S.x1+.5||a.y0<S.y0-.5||a.y1>S.y1+.5)probs.push(`圖出地圖：${a.name}`);
      r.imgs.forEach((c,j)=>{if(j>i){const o=ov(a,c);if(o/ar(a)>.10||o/ar(c)>.10)probs.push(`圖重疊 ${(100*Math.max(o/ar(a),o/ar(c))).toFixed(0)}%：${a.name} × ${c.name}`)}});
      r.fixed.forEach(f=>{if(a.kind==='bank'&&/^銀行牌/.test(f.name))return;if(ov(a,f)>0)probs.push(`圖 × ${f.name}：${a.name}`)})});
    const minfs=Math.min(...r.plates.map(q=>q.fs));
    if(w===1024&&minfs<11)probs.push(`1024 寬店名字級 ${minfs.toFixed(1)}px < 11`);
    if(r.lockClick)probs.push('鎖區／即將開幕的店可點');
    if(r.live<5)probs.push('上線店少於 5 間：'+r.live);
    if(r.doc.sw>r.doc.cw)probs.push('頁面橫向捲動');
    // 點店 → 右側欄 + 關卡連結
    if(tag!=='390'){await p.click('#mapsvg .shop[data-id="game-toy-1"]')}else{await p.click('#chips button[data-id="game-toy-1"]')}
    await p.waitForTimeout(900);
    const side=await p.evaluate(()=>({nm:document.querySelector('#side .nm').textContent,links:[...document.querySelectorAll('#side .stage')].map(a=>a.getAttribute('href')),on:document.querySelectorAll('#mapsvg .shop.on').length,
      lay:(()=>{const m=document.querySelector('#mapsvg').getBoundingClientRect(),a=document.querySelector('#side').getBoundingClientRect();return{below:a.top>=m.bottom-1,right:a.left>=m.right-1,vis:a.bottom<=innerHeight+2&&a.bottom>0}})(),
      chips:[...document.querySelectorAll('#chips button')].map(b=>({d:b.disabled}))}));
    const ok=/玩具店/.test(side.nm)&&side.links.length===6&&side.links.every((h,i)=>h.includes('/game/toy-shop?')&&h.includes('stage='+(i+1))&&h.includes('lv=2')&&h.includes('mode=faded'));
    if(!ok)probs.push('點玩具店連結有誤');if(side.on!==1)probs.push('選中店數 '+side.on);
    if(w<=1100&&!(side.lay.below&&side.lay.vis))probs.push('平板／手機關卡欄位置');if(w>1100&&!side.lay.right)probs.push('寬螢幕關卡欄不在右側');
    if(tag==='390'){const dis=side.chips.filter(c=>c.d).length;if(dis<10)probs.push('手機鎖區按鈕 disabled 只有 '+dis)}
    // 選中狀態的重疊（ring／glow 不改 bbox）已含在上面；鍵盤 focus 看得到
    if(tag==='1024'){await p.screenshot({path:path.join(__dirname,'g1_1024_sel.png')})}
    console.log(`${tag}: 店圖 ${r.imgs.length} 張（店 ${shopImgs.length}），牌 ${r.plates.length}，地圖寬 ${sc.toFixed(0)}，店名最小字 ${minfs.toFixed(1)}px，鎖區店 ${r.lockCount}，錯誤 ${errs.length}，問題 ${probs.length}`);
    console.log(`   點玩具店 → ${side.nm}，${side.links.length} 關，連結${ok?'正確':'有誤'}`);
    probs.forEach(x=>console.log('   ',x));errs.forEach(x=>console.log('   JS:',x));bad+=probs.length+errs.length;
    await p.screenshot({path:path.join(__dirname,`g1_${tag}.png`),fullPage:tag==='390'});
    if(tag==='1024'){await p.reload();await p.waitForSelector('#mapsvg .shop');await p.waitForTimeout(700);await p.screenshot({path:path.join(__dirname,'g1_1024_nosel.png')})}
    await p.close()}
  await b.close();srv.kill();console.log(bad?`FAIL ${bad}`:'ALL OK');process.exit(bad?1:0)})();
