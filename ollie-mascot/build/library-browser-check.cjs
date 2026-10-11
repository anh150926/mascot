const { chromium } = require('../web-pet/node_modules/@playwright/test');
const path = require('node:path');
const fs = require('node:fs');
(async () => {
  const browser = await chromium.launch({channel:'msedge',headless:true});
  const page = await browser.newPage({viewport:{width:1440,height:1050}});
  const errors=[];
  page.on('pageerror', e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8773/playground/', {waitUntil:'networkidle'});
  await page.waitForFunction(()=>scenes.length===19 && (moodProp || fallbackMode),null,{timeout:30000});
  console.log(await page.locator('#status').innerText());
  console.log(await page.evaluate(()=>({fallback:fallbackMode, moods:moodProp?.values, sceneCount:scenes.length})));
  await page.selectOption('#sceneSelect','love');
  await page.waitForTimeout(650);
  await page.screenshot({path:path.join(__dirname,'library-browser-love.png')});
  await page.evaluate(()=>{for(const img of document.images) img.loading='eager'});
  await page.waitForFunction(()=>Array.from(document.images).filter(i=>i.getAttribute('src')).every(i=>i.complete));
  const broken=await page.locator('img').evaluateAll(imgs=>imgs.filter(i=>i.getAttribute('src')&&!i.naturalWidth).map(i=>i.src));
  if(broken.length)throw Error('Broken images: '+broken);
  await page.locator('#library').screenshot({path:path.join(__dirname,'library-browser-gallery.png')});
  for(const key of await page.evaluate(()=>scenes.map(s=>s.key))) {
    await page.selectOption('#sceneSelect',key);
    await page.waitForTimeout(320);
    const actual=await page.evaluate(()=>({mood:moodProp?.value||fallbackMood,title:document.querySelector('#sceneTitle').textContent}));
    if(actual.mood!==key)throw Error('Mood mismatch '+key);
  }
  await page.selectOption('#sceneSelect','workout');
  await page.locator('#sleep').click();
  await page.waitForTimeout(1100);
  if((await page.locator('#sceneTitle').innerText())!=='Ollie đang ngủ')throw Error('Sleep description mismatch');
  await page.screenshot({path:path.join(__dirname,'library-browser-sleep.png')});
  await page.locator('#sleep').click();
  await page.waitForTimeout(1500);
  await page.locator('[data-mood="neutral"]').first().click();
  await page.waitForTimeout(700);
  await page.screenshot({path:path.join(__dirname,'library-browser-return.png')});
  await page.selectOption('#sceneSelect','love');
  for(const size of ['120 px','240 px','400 px']) {
    await page.locator('#sizes button').getByText(size,{exact:true}).click();
    for(const theme of ['light','dark']) {
      await page.locator(`button[data-stage="${theme}"]`).click();
      await page.waitForTimeout(300);
      await page.locator('.stage').screenshot({path:path.join(__dirname,`library-size-${size.split(' ')[0]}-${theme}.png`)});
    }
  }
  await page.locator('button[data-stage="light"]').click();
  await page.locator('#useFrames').click();
  if(!(await page.locator('#fallback').getAttribute('src')).includes('love'))throw Error('Fallback did not preserve selection');
  await page.locator('#useFrames').click();
  for(const key of await page.evaluate(()=>scenes.map(s=>s.key))) {
    await page.selectOption('#sceneSelect',key);
    await page.waitForFunction(()=>fallback.complete && fallback.naturalWidth>0);
    if(!(await page.locator('#fallback').getAttribute('src')).includes(key+'.png'))throw Error('Wrong fallback '+key);
  }
  await page.selectOption('#sceneSelect','love');
  await page.setViewportSize({width:390,height:844});
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Mobile overflow');
  await page.screenshot({path:path.join(__dirname,'library-browser-mobile.png')});
  if(errors.length)throw Error(errors.join('\n'));
  fs.writeFileSync(path.join(__dirname,'library-browser-report.json'),JSON.stringify({passed:true,scenes:19,checks:['all selectable','no missing images','sleep and return screenshots','sleep description','120/240/400px light and dark','fallback preserves mood','repeated fallback activation','all fallback images','mobile overflow','no page errors']},null,2));
  await browser.close();
  console.log('Browser checks passed');
})().catch(e=>{console.error(e);process.exit(1)});
