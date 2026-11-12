// 拿錢頁「數到多少元」標註的位值配色模擬圖（勘誤表7 第三輪；使用者覺得綠色不夠清楚）。重產：node make.js
const {chromium}=require('playwright');
const PV={h:{w:84,hh:48,fill:'#f2b5bd',edge:'#b3222f',txt:'100'},t:{w:62,fill:'#E1E4E8',edge:'#222222',txt:'10'},o:{w:48,fill:'#D9A877',edge:'#5A3518',txt:'1'}};
const coin=k=>{const c=PV[k]; return k==='h'?`<svg width="${c.w}" height="${c.hh}" viewBox="0 0 100 57"><rect x="3" y="3" width="94" height="51" rx="7" fill="${c.fill}" stroke="${c.edge}" stroke-width="4"/><rect x="9" y="9" width="82" height="39" rx="4" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="4 3" opacity=".75"/><text x="50" y="37" font-size="27" font-weight="800" text-anchor="middle" fill="${c.edge}" font-family="sans-serif">100</text></svg>`:`<svg width="${c.w}" height="${c.w}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="${c.fill}" stroke="${c.edge}" stroke-width="6"/><circle cx="50" cy="50" r="35" fill="none" stroke="${c.edge}" stroke-width="3" stroke-dasharray="4 5" opacity=".55"/><text x="50" y="63" font-size="${k==='t'?38:46}" font-weight="800" text-anchor="middle" fill="${c.edge}" font-family="sans-serif">${c.txt}</text></svg>`;};
const OPT=[
 ['現在','百 玫瑰紅／十 藍／個 綠','#c2185b','#1d4ed8','#15803d',17,3],
 ['甲','百 紅／十 藍／個 黑（對比最高）','#dc2626','#1d4ed8','#111827',17,3],
 ['乙','百 紅／十 藍／個 深咖啡（接近 1 元的顏色）','#dc2626','#1d4ed8','#6b3410',17,3],
 ['丙','百 紫／十 藍／個 黑','#7e22ce','#0369a1','#111827',17,3],
 ['丁','顏色同甲，字放大、白邊加粗','#dc2626','#1d4ed8','#111827',21,5],
];
const lab=(n,o)=>{const s=String(n),cls=['o','t','h'];return `<span class="tl" style="font-size:${o[5]}px;text-shadow:${Array(o[6]+1).fill('0 0 3px #fff').join(',')}">`+s.split('').map((d,i)=>`<i style="color:${o[2+ (s.length-1-i===2?0:s.length-1-i===1?1:2)]}">${d}</i>`).join('')+'</span>';};
const cell=(k,n,o)=>`<span class="c">${coin(k)}${lab(n,o)}</span>`;
const row=o=>`<div class="row"><div class="nm"><b>${o[0]}</b><small>${o[1]}</small></div><div class="tray">${cell('h',100,o)}${cell('h',200,o)}<span class="gap"></span>${cell('t',210,o)}${cell('t',220,o)}${cell('t',230,o)}<span class="gap"></span>${cell('o',231,o)}${cell('o',232,o)}${cell('o',233,o)}${cell('o',234,o)}</div></div>`;
const html=`<html><body style="margin:0;background:#fff7ed;font-family:'Noto Sans TC','Noto Sans CJK TC',sans-serif"><div id="w" style="padding:18px 22px;width:900px"><h2 style="margin:0 0 4px;color:#9a3412;font-size:22px">金額標註的位值配色（實際大小）</h2><div style="color:#57534e;font-size:15px;margin-bottom:10px">每個錢右上角的數字＝數到這個錢是多少元。百位、十位、個位各一種顏色。</div>
<style>.row{display:flex;align-items:center;gap:14px;margin:10px 0}.nm{width:210px}.nm b{font-size:26px;color:#9a3412;display:block}.nm small{font-size:14px;color:#44403c}.tray{flex:1;display:flex;align-items:center;gap:14px;background:#fef3c7;border:4px solid #a16207;border-radius:16px;padding:16px 14px 12px}.c{position:relative;display:inline-block;line-height:0}.tl{position:absolute;right:-3px;top:-7px;font-weight:900;line-height:1;white-space:nowrap;font-family:sans-serif}.tl i{font-style:normal}.gap{width:14px}</style>
${OPT.map(row).join('')}</div></body></html>`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:960,height:800},deviceScaleFactor:2});await p.setContent(html);await p.locator('#w').screenshot({path:'options.png'});await b.close();})();
