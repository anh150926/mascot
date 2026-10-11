const {chromium}=require('../web-pet/node_modules/@playwright/test');
const fs=require('node:fs');
(async()=>{
  const browser=await chromium.launch({channel:'msedge',headless:true});
  const page=await browser.newPage({viewport:{width:1440,height:1040}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8773/playground/wing-review.html',{waitUntil:'networkidle'});
  const options=await page.locator('#scene option').evaluateAll(nodes=>nodes.map(n=>n.value));
  if(options.length!==19)throw Error('Expected 19 expression scenes');
  for(const scene of options){
    await page.selectOption('#scene',scene);
    for(let index=0;index<5;index++){
      await page.locator('#frame').fill(String(index));
      await page.waitForFunction(()=>document.querySelector('#full').complete&&document.querySelector('#full').naturalWidth===500);
      const src=await page.locator('#full').getAttribute('src');
      if(!src.includes(`${scene}-${index*25}.webp`))throw Error(`Wrong phase ${scene} ${index}`);
      if((await page.locator('#detail').getAttribute('src'))!==src)throw Error('Detail frame mismatch');
    }
  }
  await page.selectOption('#scene','wallet');
  await page.locator('#frame').fill('2');
  await page.locator('#previous').click();
  if(await page.locator('#frame').inputValue()!=='1')throw Error('Previous button');
  await page.locator('#next').click();
  if(await page.locator('#frame').inputValue()!=='2')throw Error('Next button');
  await page.screenshot({path:'build/wing-review-desktop.png',fullPage:true});
  await page.locator('#theme').click();
  if(!await page.locator('#stage').evaluate(e=>e.classList.contains('dark')))throw Error('Theme toggle');
  await page.setViewportSize({width:390,height:844});
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Mobile overflow');
  await page.screenshot({path:'build/wing-review-mobile.png',fullPage:true});
  if(errors.length)throw Error(errors.join('\n'));
  fs.writeFileSync('build/wing-browser-report.json',JSON.stringify({passed:true,scenes:19,frames:95,checks:['all frames load','detail and main agree','previous and next buttons','theme toggle','mobile width','no page errors']},null,2));
  console.log('Wing review: 19 scenes / 95 frames passed');
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
