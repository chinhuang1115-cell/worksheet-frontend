const OUT=process.env.MOCKOUT, TAG=process.env.MOCKTAG;
const CSS=`
/* 長方形皮革零錢盤（參考使用者提供的皮革托盤：外框斜邊＋縫線＋內凹平台＋四角壓花；不加文字） */
.dish{--lt:#8a3443;--dk:#5b2029;--in1:#5e222b;--in2:#6c2833;--edge:#3d141b;--st:rgba(255,214,200,.5);--orn:#7c3140;
 width:min(440px,88%)!important;height:200px!important;border-radius:18px!important;border:0!important;
 background:linear-gradient(165deg,var(--lt),var(--dk) 75%)!important;
 box-shadow:0 0 0 2px var(--edge),0 14px 0 var(--edge),0 24px 18px rgba(0,0,0,.32),inset 0 3px 0 rgba(255,255,255,.22),inset 0 -4px 0 rgba(0,0,0,.25)!important;
 transform:perspective(900px) rotateX(28deg);transform-origin:50% 100%;transform-style:preserve-3d}
#deal{perspective:900px}
.dish .mat .coin{transform:rotateX(-28deg) translateY(-4px)!important;transform-origin:50% 100%;filter:drop-shadow(0 3px 2px rgba(0,0,0,.45))}
body.shop-bakery .dish{--lt:#7a5038;--dk:#4e3122;--in1:#4f3223;--in2:#5d3b29;--edge:#3a2318;--st:rgba(249,168,212,.85);--orn:#6d4630}
.dish::before{content:'';position:absolute;inset:6px;border-radius:13px;border:2px dashed var(--st);pointer-events:none}
.dish::after{content:'';position:absolute;inset:26px 32px;border-radius:8px;background:linear-gradient(var(--in1),var(--in2));box-shadow:inset 0 9px 10px rgba(0,0,0,.55),inset 0 -2px 0 rgba(255,255,255,.12),0 1px 0 rgba(255,255,255,.2)}
.dish .orn{position:absolute;inset:26px 32px;z-index:1;pointer-events:none}
.dish .orn i{position:absolute;font-style:normal;font-size:30px;line-height:1;color:var(--orn);text-shadow:0 1px 0 rgba(255,255,255,.18),0 -1px 0 rgba(0,0,0,.4)}
.dish .orn i:nth-child(1){left:6px;top:4px}.dish .orn i:nth-child(2){right:6px;top:4px;transform:scaleX(-1)}
.dish .orn i:nth-child(3){left:6px;bottom:4px;transform:scaleY(-1)}.dish .orn i:nth-child(4){right:6px;bottom:4px;transform:scale(-1,-1)}
.dish .mat,.dish .mat .cs{transform-style:preserve-3d}.dish .mat{z-index:2;border-radius:8px!important;inset:26px 32px!important;padding:8px!important;display:flex;align-items:center;justify-content:center}
.dish .mat .cs{justify-content:center}
/* 回商店街 */
.homeb{display:inline-flex;align-items:center;gap:4px;white-space:nowrap;font:inherit;font-weight:800;font-size:17px;color:#9a3412;background:#fff;border:2px solid #fdba74;border-radius:12px;padding:4px 12px;margin-right:10px;cursor:pointer}
.homeI{font-size:20px}
body.hasHome #top .qno+.qno{display:none}body.hasHome #top{gap:8px}.homeb{padding:4px 10px!important;margin-right:2px!important}
.mk{position:fixed;right:20px;top:64px;z-index:99;background:rgba(255,255,255,.9);border-radius:8px;padding:2px 10px;font-size:15px;color:#6b7280}
.confov{position:fixed;inset:0;background:rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center;z-index:80}
.confov .cfbox{display:block!important;background:#fff;border-radius:22px;padding:26px 34px;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,.25);border:4px solid #fdba74;width:440px}
.confov .cfq{font-size:26px;font-weight:800;color:#9a3412;margin:6px 0}.confov .cfs{font-size:18px;color:#57534e;margin-bottom:20px}
.confov .cfrow{display:flex;gap:14px;justify-content:center}
.confov .cfb{white-space:nowrap;font:inherit;font-size:20px;font-weight:800;border-radius:14px;padding:10px 20px;border:0;border-bottom:4px solid}
.confov .cfstay{background:#ea580c;color:#fff;border-color:#9a3412}.confov .cfgo{background:#fff;color:#57534e;border:2px solid #a8a29e;border-bottom-width:4px}
`;
global.HOOK=async(p,lv,n)=>{
 const prep=async(home,mark)=>p.evaluate(([css,home,mark])=>{
  if(!document.getElementById('mockcss')){const s=document.createElement('style');s.id='mockcss';s.textContent=css;document.head.appendChild(s);
   const d=document.querySelector('.dish');const o=document.createElement('div');o.className='orn';o.innerHTML='<i>❦</i><i>❦</i><i>❦</i><i>❦</i>';d.prepend(o);}
  document.querySelectorAll('.homeb,.mk').forEach(e=>e.remove());
  const top=document.getElementById('top'), tools=document.getElementById('tools');
  document.body.classList.toggle('hasHome',home==='L');if(home==='L'){const b=document.createElement('button');b.className='homeb';b.innerHTML='🏠 回商店街';top.prepend(b);}
  if(home==='R'){const b=document.createElement('button');b.className='tbtn homeb homeI';b.style.marginRight='0';b.title='回商店街';b.innerHTML='🏠';tools.appendChild(b);}
  const m=document.createElement('div');m.className='mk';m.textContent=mark;document.body.appendChild(m);
 },[CSS,home,mark]);
 if(n==='3c_paid_center'){
  // 多放 1 元、50 元，看各種錢幣在深色盤上的對比
  await p.evaluate(()=>{const cs=document.querySelector('#pay .cs');const e=cs.querySelector('.coin');const sc=parseFloat(e.style.width)/PV[e.dataset.k].w;for(const k of ['o','q'])cs.prepend(coinEl(k,sc));});
  if(TAG==='bf'){
   await prep('L','模擬圖 甲：左上角「回商店街」＋早餐店酒紅皮革零錢盤'); await p.screenshot({path:`${OUT}/甲_回商店街在左上_早餐店零錢盤.png`});
   await prep('R','模擬圖 乙：右上角工具列 🏠 圖示'); await p.screenshot({path:`${OUT}/乙_回商店街在右上.png`});
   await prep('L','模擬圖 丙：按了之後先問一次（避免學生誤觸）');
   await p.evaluate(()=>{const o=document.createElement('div');o.className='confov';o.innerHTML='<div class="cfbox"><div style="font-size:54px">🏪</div><div class="cfq">要回到商店街嗎？</div><div class="cfs">這一場還沒玩完，離開後要重新開始。</div><div class="cfrow"><button class="cfb cfstay">繼續玩</button><button class="cfb cfgo">🏠 回商店街</button></div></div>';document.body.appendChild(o);});
   await p.screenshot({path:`${OUT}/丙_離開前確認.png`}); await p.evaluate(()=>document.querySelector('.confov').remove());
  } else { await prep('L','模擬圖 戊：麵包店巧克力皮革零錢盤（粉紅縫線）'); await p.screenshot({path:`${OUT}/戊_麵包店零錢盤.png`}); }
 }
 if(n==='all_lv3_finish'&&TAG==='bf'){
  await prep('L','模擬圖 丁：全部完成時多一顆「回商店街」（不再詢問）');
  await p.evaluate(()=>{const b=[...document.querySelectorAll('.ov .btn')].find(x=>x.textContent.includes('再玩'));const g=document.createElement('button');g.className=b.className;g.style.cssText='background:#fff;color:#9a3412;border:2px solid #fdba74;border-bottom:5px solid #fdba74;margin-left:14px';g.textContent='🏠 回商店街';b.after(g);});
  await p.screenshot({path:`${OUT}/丁_完成畫面.png`});
 }
};
require('./test_mock.js');
