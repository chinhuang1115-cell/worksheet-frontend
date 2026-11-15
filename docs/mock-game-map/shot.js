// mock_map.html → map_1280.png、map_1024.png
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();for(const [w,h] of [[1280,800],[1024,768]]){const p=await b.newPage({viewport:{width:w,height:h}});await p.goto('file://'+path.join(__dirname,'mock_map.html'));await p.waitForTimeout(500);await p.screenshot({path:path.join(__dirname,`map_${w}.png`)});}await b.close()})();
