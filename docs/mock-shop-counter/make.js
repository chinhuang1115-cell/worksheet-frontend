const {chromium}=require('playwright');
const S=process.argv[2], OUT=process.argv[3];
const V={
 CA:`/* C 牆面＋菜單陰影，桌面用 A（梯形、後緣深） */
 #C{gap:0;background:linear-gradient(#f7e9cf,#efd9b1);border-radius:12px}
 #board{box-shadow:0 14px 10px -6px rgba(90,50,10,.35)}
 .counter{margin-top:52px;border-top:none;border-radius:0;clip-path:polygon(7% 0,93% 0,100% 100%,0 100%);
   background:linear-gradient(rgba(70,35,0,.35),rgba(0,0,0,0) 28%),var(--ctr) 0 0/360px,linear-gradient(#d6a76c,#c08a4c)}
 body.shop-bakery .counter{background:linear-gradient(rgba(150,40,80,.22),rgba(0,0,0,0) 28%),var(--ctr) 0 0/360px,linear-gradient(#fbe3e8,#f3bfcb);box-shadow:none}`};
(async()=>{const b=await chromium.launch();
 for(const shop of ['breakfast','bakery']) for(const [vw,vh] of [[1366,768],[1024,768]]) for(const k of Object.keys(V)){
  if(shop==='bakery'&&k!=='now'&&false) continue;
  const p=await b.newPage({viewport:{width:vw,height:vh}});
  await p.goto(`file://${S}/${shop}.html?lv=2&noanim=1`); await p.waitForTimeout(600); await p.evaluate(()=>document.querySelectorAll('.ov').forEach(o=>o.remove()));
  if(V[k]) await p.addStyleTag({content:V[k]}); await p.waitForTimeout(200);
  const info=await p.evaluate(()=>{const ct=document.querySelector('.counter').getBoundingClientRect(),cc=document.querySelector('#C').getBoundingClientRect(),bd=document.querySelector('#board').getBoundingClientRect();
   const CH=Math.min(160,Math.round((innerHeight-110)*.23)),CW=Math.round(CH*152/200);
   const d=document.createElement('div');d.style.cssText=`position:fixed;overflow:hidden;width:${CW}px;height:${CH}px;left:${cc.right-20-CW}px;top:${ct.top-CH+ (getComputedStyle(document.querySelector('.counter')).borderTopWidth==='0px'?0:0)}px;z-index:50`;
   const i=document.createElement('img');i.src=SPEC.faces.clerk;i.style.cssText='width:100%;height:100%';d.appendChild(i);document.body.appendChild(d);
   const bub=document.createElement('div');bub.className='bub';bub.textContent=SHOP.greet;bub.style.cssText=`position:fixed;z-index:51;display:block;background:#fff;border:3px solid #2563eb;color:#1d4ed8;border-radius:16px;padding:4px 12px;font-size:19px;font-weight:800;white-space:nowrap;right:${innerWidth-(cc.right-20)}px;bottom:${innerHeight-(ct.top-CH)+6}px`;document.body.appendChild(bub);
   return {scroll:document.documentElement.scrollHeight-innerHeight,counterH:Math.round(ct.height),boardBottom:Math.round(bd.bottom),counterTop:Math.round(ct.top),overlapMenu:Math.max(0,Math.round(bd.bottom-(ct.top-CH)))};});
  await p.waitForTimeout(150);
  await p.screenshot({path:`${OUT}/${shop}_${vw}_${k}.png`});
  console.log(shop,vw,k,JSON.stringify(info)); await p.close(); }
 await b.close();})();
