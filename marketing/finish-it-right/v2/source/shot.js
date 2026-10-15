const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
(async()=>{const [,,html,out,w,h]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+h}});
await p.goto('file://'+html);await p.waitForLoadState('networkidle');await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:out});await b.close();})();
