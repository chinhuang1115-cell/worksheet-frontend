const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1100,height:614},deviceScaleFactor:2});
await p.goto('file://'+__dirname+'/prev_A2.html');await p.waitForTimeout(500);await p.screenshot({path:__dirname+'/prev_A2.png'});await b.close()})();
