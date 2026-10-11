const {chromium}=require('../web-pet/node_modules/@playwright/test');
const fs=require('node:fs');
(async()=>{
  const browser=await chromium.launch({channel:'msedge',headless:true});
  const page=await browser.newPage({viewport:{width:1360,height:950}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/dist/ollie.riv?*',route=>route.fulfill({body:fs.readFileSync('build/wing-preview.riv'),contentType:'application/octet-stream'}));
  await page.goto('http://127.0.0.1:8773/playground/',{waitUntil:'networkidle'});
  await page.waitForFunction(()=>moodProp&&scenes.length===19);
  for(const mood of ['wallet','worried','bedtime','workout']){
    await page.selectOption('#sceneSelect',mood);await page.waitForTimeout(900);
    await page.locator('.stage').screenshot({path:`build/wing-live-${mood}.png`});
  }
  if(errors.length)throw Error(errors.join('\n'));
  await browser.close();console.log('Live wing runtime loaded; four representative poses captured.');
})().catch(e=>{console.error(e);process.exit(1)});
