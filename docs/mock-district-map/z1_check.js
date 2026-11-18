// 批次 Z1 驗收：開 games/index.html，量每個店牌／區名牌／銀行的 bounding box，檢查互相重疊與出界（扇形、畫面），並截圖。
// 用法：node docs/mock-district-map/z1_check.js（需要 playwright；會自己起 python http.server 於 8765）
const {chromium}=require('playwright'),{spawn}=require('child_process'),path=require('path');
const ROOT=path.resolve(__dirname,'../..');
(async()=>{
  const srv=spawn('python3',['-m','http.server','8765'],{cwd:ROOT,stdio:'ignore'});await new Promise(r=>setTimeout(r,1000));
  const b=await chromium.launch();let bad=0;
  for(const [w,h,tag] of [[1280,800,'1280'],[1024,768,'1024'],[390,844,'390']]){
    const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:2});
    const errs=[];p.on('pageerror',e=>errs.push(e.message));
    await p.goto('http://localhost:8765/games/index.html');await p.waitForSelector('#mapsvg .it');await p.waitForTimeout(600);
    const r=await p.evaluate(()=>{
      const svg=document.querySelector('#mapsvg'),inv=svg.getScreenCTM().inverse(),G=window.__GEO,pt=svg.createSVGPoint();
      const toU=(x,y)=>{pt.x=x;pt.y=y;const q=pt.matrixTransform(inv);return[q.x,q.y]};
      const rects=[];
      const add=(el,kind,name)=>{const bb=el.getBoundingClientRect(),a=toU(bb.left,bb.top),c=toU(bb.right,bb.bottom);rects.push({kind,name,x0:a[0],y0:a[1],x1:c[0],y1:c[1]})};
      svg.querySelectorAll('.shop.it').forEach(el=>{
        // 只量看得見的內容（不含 .ring 對焦框）：臨時隱藏 ring
        const ring=el.querySelector('.ring');ring.style.display='none';add(el,'shop',el.getAttribute('aria-label')||el.querySelector('.lbt').textContent);ring.style.display=''});
      svg.querySelectorAll('.plate').forEach(el=>add(el,'plate',el.querySelector('text').textContent));
      svg.querySelectorAll('g[aria-hidden="true"]:not(.shop)').forEach((el,i)=>{if(!el.classList.contains('shop')&&el.querySelector('polygon')&&el.textContent.includes('銀行'))add(el,'bank','銀行'+i)});
      const gate=svg.querySelector('.gate');add(gate,'gate','入口');
      const lbl=[...svg.querySelectorAll('.lbt')].map(t=>{const pill=t.previousElementSibling.getBoundingClientRect(),tb=t.getBoundingClientRect();return{n:t.textContent,over:tb.width-pill.width,fs:parseFloat(t.getAttribute('font-size'))}});
      return{rects,lbl,G,s:window.__LAYOUT.s,svgW:svg.getBoundingClientRect().width,doc:{sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth}}});
    const R=r.rects,G=r.G,probs=[];
    for(let i=0;i<R.length;i++)for(let j=i+1;j<R.length;j++){const a=R[i],c=R[j];
      if(a.x0<c.x1&&c.x0<a.x1&&a.y0<c.y1&&c.y0<a.y1)probs.push(`重疊：${a.kind}:${a.name} × ${c.kind}:${c.name}`)}
    for(const a of R){if(a.kind==='plate'||a.kind==='shop'||a.kind==='bank'){
      if(a.x0<0||a.y0<0||a.x1>G.W||a.y1>G.H)probs.push(`出畫面：${a.name}`);
      for(const[x,y] of [[a.x0,a.y0],[a.x1,a.y0],[a.x0,a.y1],[a.x1,a.y1]]){const rr=Math.hypot(x-G.cx,y-G.cy);if(rr>G.R1+.5){probs.push(`出扇形外緣：${a.name}`);break}}
      if(a.kind!=='bank'){const nx=Math.min(Math.max(G.cx,a.x0),a.x1),ny=Math.min(Math.max(G.cy,a.y0),a.y1);if(Math.hypot(nx-G.cx,ny-G.cy)<G.R0)probs.push(`蓋到入口：${a.name}`);if(a.y1>G.cy)probs.push(`低於地平線：${a.name}`)}}}
    // 扇形交界：店／區名牌不可跨過 60°／120° 線（銀行本來就跨線，不檢查）
    for(const a of R){if(a.kind==='bank'||a.kind==='gate')continue;
      const cs=[[a.x0,a.y0],[a.x1,a.y0],[a.x0,a.y1],[a.x1,a.y1]].map(([x,y])=>Math.atan2(G.cy-y,x-G.cx)*180/Math.PI);
      const zs=new Set(cs.map(c=>c>=120?0:c>=60?1:2));if(zs.size>1)probs.push(`跨扇區：${a.name}`)}
    for(const l of r.lbl)if(l.over>0.5)probs.push(`店名超出名牌：${l.n}`);
    const minfs=Math.min(...r.lbl.map(l=>l.fs))*r.svgW/G.W;
    console.log(`${tag}: 店/牌 ${R.length} 個，縮放 s=${r.s}，店名最小字約 ${minfs.toFixed(1)}px，svg 寬 ${r.svgW.toFixed(0)}，頁面橫向捲動=${r.doc.sw>r.doc.cw}，錯誤 ${errs.length}，問題 ${probs.length}`);
    probs.forEach(x=>console.log('   ',x));errs.forEach(x=>console.log('   JS:',x));bad+=probs.length+errs.length+(r.doc.sw>r.doc.cw?1:0);
    // 點店 → 右側欄 + 關卡連結
    const first=await p.$('#mapsvg .shop[data-id]');await first.scrollIntoViewIfNeeded();
    if(tag!=='390'){await p.click('#mapsvg .shop[data-id="game-toy-1"]');}else{await p.click('#chips button[data-id="game-toy-1"]')}
    await p.waitForTimeout(200);
    const side=await p.evaluate(()=>({nm:document.querySelector('#side .nm').textContent,links:[...document.querySelectorAll('#side .stage')].map(a=>a.getAttribute('href'))}));
    const ok=/玩具店/.test(side.nm)&&side.links.length===6&&side.links.every((h,i)=>h.includes('/game/toy-shop?')&&h.includes('stage='+(i+1))&&h.includes('lv=2')&&h.includes('mode=faded'));
    console.log(`   點玩具店 → ${side.nm}，${side.links.length} 關，連結${ok?'正確':'有誤'}：${side.links[0]}`);if(!ok)bad++;
    // 點鎖住區的店不應有反應
    const lockedClickable=await p.evaluate(()=>document.querySelectorAll('#mapsvg .shop.soon[data-id]').length);if(lockedClickable)bad++;
    await p.screenshot({path:path.join(__dirname,`z1_${tag}.png`),fullPage:tag==='390'});
    await p.close()}
  await b.close();srv.kill();console.log(bad?`FAIL ${bad}`:'ALL OK');process.exit(bad?1:0)})();
