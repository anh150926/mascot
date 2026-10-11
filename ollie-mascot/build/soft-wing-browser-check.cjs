const {chromium}=require('../web-pet/node_modules/@playwright/test');
const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8773/playground/',{waitUntil:'networkidle'});
 await page.waitForFunction(()=>moodProp&&scenes.length===19);
 await page.selectOption('#sceneSelect','wallet');
 for(const size of ['120 px','240 px','400 px']){
  await page.locator('#sizes button').getByText(size,{exact:true}).click();
  await page.waitForTimeout(550);
  await page.locator('.stage').screenshot({path:path.join(__dirname,`soft-wing-wallet-${size.split(' ')[0]}.png`)});
 }
 await page.locator('#useFrames').click();
 await page.waitForFunction(()=>fallback.complete&&fallback.naturalWidth===500);
 const fallback=await page.locator('#fallback').getAttribute('src');
 if(!fallback.includes('wallet.png?v=wing04'))throw Error('Fallback did not use new wallet frame: '+fallback);
 await page.locator('.stage').screenshot({path:path.join(__dirname,'soft-wing-wallet-fallback.png')});
 await page.setViewportSize({width:390,height:844});
 if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Mobile overflow');
 if(errors.length)throw Error(errors.join('\n'));
 await browser.close();console.log('Smooth wallet: live Rive 120/240/400px, fallback and mobile passed');
})().catch(e=>{console.error(e);process.exit(1)});
