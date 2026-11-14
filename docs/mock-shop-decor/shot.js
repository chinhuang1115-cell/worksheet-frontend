// make.py 呼叫：依 cfg.json 截每家店的場景圖（1280×800、2x）與 總覽.png（9 格）
const {chromium}=require('playwright'); const fs=require('fs');
const cfg=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
(async()=>{const b=await chromium.launch();
 for(const s of cfg.shops){
  const ctx=await b.newContext({viewport:{width:1280,height:800},deviceScaleFactor:2}); const p=await ctx.newPage();
  await p.goto(`file://${cfg.html}/${s.ref?s.id:'breakfast'}.html?lv=2&noanim=1`); await p.waitForTimeout(900);
  await p.evaluate(()=>document.querySelectorAll('.ov').forEach(o=>o.remove()));
  if(!s.ref){
   await p.addStyleTag({content:s.css});
   await p.evaluate(s=>{
     document.body.classList.remove('shop-breakfast'); document.body.classList.add('shop-'+s.id);
     document.body.style.setProperty('--awn',s.awn); document.body.style.setProperty('--ctr','none');
     document.querySelector('#sign').textContent=s.sign; const sn=document.querySelector('#top .ttl'); if(sn) sn.textContent=s.short+'購物（第 1 關：買 1 樣）';
     MENU.length=0; s.menu.forEach(m=>MENU.push(m)); drawBoard();
     const t=document.querySelector('#tray'); t.innerHTML=[s.menu[0],s.menu[3]].map(m=>`<img src="${m.img}" style="height:84px;transform:rotateX(-26deg)">`).join('');
     document.querySelector('#slip').innerHTML='<b>點餐單</b><div class="ln">'+s.menu[0].name+' 1</div><div class="ln">'+s.menu[3].name+' 1</div>';
   },s);
  } else {
   await p.evaluate(()=>{const t=document.querySelector('#tray');t.innerHTML=[MENU[0],MENU[3]].map(m=>`<img src="${m.img}" style="height:84px;transform:rotateX(-26deg)">`).join('');document.querySelector('#slip').innerHTML='<b>點餐單</b><div class="ln">'+MENU[0].name+' 1</div><div class="ln">'+MENU[3].name+' 1</div>';});
  }
  await p.evaluate(()=>document.querySelector('#deal').classList.add('show')); await p.waitForTimeout(1300);
  await p.screenshot({path:`${cfg.out}/${s.id}.png`}); console.log('shot',s.id);
  const bad=await p.evaluate(()=>[...document.querySelectorAll('#board .item .nm')].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.textContent));
  if(bad.length) console.log('  text overflow',bad);
  await ctx.close();
 }
 // 總覽
 const html=`<body style="margin:0;background:#f1f5f9;font-family:'WenQuanYi Zen Hei','Noto Sans CJK TC',sans-serif"><div style="display:grid;grid-template-columns:repeat(3,640px);gap:14px;padding:14px;width:1992px">`+
  cfg.shops.map(s=>`<div style="background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.2)"><img src="file://${cfg.out}/${s.id}.png" style="width:640px;display:block"><div style="padding:6px 12px 8px"><b style="font-size:20px">${s.short}${s.ref?'（現有）':'（新）'}</b><div style="font-size:14px;color:#475569">${s.note}</div></div></div>`).join('')+`</div></body>`;
 const ctx=await b.newContext({viewport:{width:1992,height:1000},deviceScaleFactor:1}); const p=await ctx.newPage();
 fs.writeFileSync(cfg.html+'/ov.html',html); await p.goto('file://'+cfg.html+'/ov.html'); await p.waitForTimeout(800);
 await p.screenshot({path:`${cfg.out}/總覽.png`,fullPage:true}); await b.close();})();
