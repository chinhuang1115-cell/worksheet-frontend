const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1100,height:614},deviceScaleFactor:2});
for(const v of ['A','B']){await p.goto('file://'+__dirname+'/prev_'+v+'.html');await p.waitForTimeout(400);await p.screenshot({path:__dirname+'/prev_'+v+'.png'});}await b.close()})();
