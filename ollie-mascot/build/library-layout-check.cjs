const {chromium}=require('../web-pet/node_modules/@playwright/test');
(async()=>{
  const browser=await chromium.launch({channel:'msedge',headless:true});
  const page=await browser.newPage({viewport:{width:1440,height:1050}});
  await page.goto('http://127.0.0.1:8773/playground/');
  await page.waitForFunction(()=>scenes.length===19);
  await page.locator('.scene-card img').evaluateAll(imgs=>imgs.forEach(i=>i.loading='eager'));
  await page.waitForFunction(()=>Array.from(document.querySelectorAll('.scene-card img')).every(i=>i.complete));
  for(const width of [1440,390]) {
    await page.setViewportSize({width,height:1050});
    const r=await page.locator('.scene-card img').first().boundingBox();
    if(Math.abs(r.height-r.width)>1)throw Error('Non-square card image');
    if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Horizontal overflow');
    await page.locator('#library').screenshot({path:`build/library-gallery-${width}.png`});
    console.log({width,imageWidth:r.width,imageHeight:r.height});
  }
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
