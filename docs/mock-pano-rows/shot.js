// 把 make.py 產生的模擬圖 *.html 截成 PNG（deviceScaleFactor 2）：node shot.js
const {chromium} = require('playwright'), fs = require('fs'), path = require('path');
(async () => { const b = await chromium.launch(), p = await b.newPage({viewport: {width: 1100, height: 660}, deviceScaleFactor: 2});
  for (const f of fs.readdirSync(__dirname).filter(f => f.endsWith('.html'))) {
    await p.goto('file://' + path.join(__dirname, f)); await p.waitForTimeout(300);
    await p.screenshot({path: path.join(__dirname, f.replace('.html', '.png'))}); }
  await b.close(); })();
