// Browser QA: preserves a comfortable paper background across three real lab page types.
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const {chromium}=require('playwright');
const base=process.env.LAB_TEST_ORIGIN || 'http://127.0.0.1:8765';
const routes=[
  {id:'photoelectric',route:'/physics/photoelectric-effect/'},
  {id:'theory',route:'/aerospace-aeronautical-engineering/aeroelastic-torsional-divergence-wing-rigidity/theory/'},
  {id:'report',route:'/aerospace-aeronautical-engineering/aeroelastic-torsional-divergence-wing-rigidity/report/'}
];
const viewports=[{name:'desktop',width:1440,height:900},{name:'mobile',width:390,height:844}];
const out='audit-results/browser';
fs.mkdirSync(out,{recursive:true});
(async()=>{
const browser=await chromium.launch({headless:true});
const results=[];
try{
  for(const route of routes)for(const viewport of viewports){
    const context=await browser.newContext({viewport:{width:viewport.width,height:viewport.height},reducedMotion:'reduce'});
    const page=await context.newPage();
    const response=await page.goto(base+route.route,{waitUntil:'domcontentloaded',timeout:45000});
    assert.equal(response.status(),200,route.route+' must load');
    // Check real rendered CSS, not only DOM readiness.
    await page.waitForFunction(() => getComputedStyle(document.body).backgroundColor === 'rgb(247, 246, 240)', null, {timeout:15000});
    const report=await page.evaluate(()=>{
      const body=getComputedStyle(document.body);
      const p=document.querySelector('.theory-article p,.lab-report p,.page-heading>p');
      return {
        background:body.backgroundColor,
        title:document.title,
        h1:document.querySelector('h1')?.textContent?.trim(),
        fontSize:p?getComputedStyle(p).fontSize:null,
        horizontalOverflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,
        anchors:document.querySelectorAll('a[href]').length
      };
    });
    assert.equal(report.background,'rgb(247, 246, 240)','Keep warm paper background');
    assert.ok(report.h1?.length>3,'Readable heading missing');
    assert.ok(report.anchors>=5,'Missing student navigation');
    assert.ok(report.horizontalOverflow<=24,'Horizontal page overflow: '+JSON.stringify({route,viewport,report}));
    if(route.id!=='photoelectric')
      assert.ok(parseFloat(report.fontSize)>=16,'Long-form reading text must be at least 16px: '+JSON.stringify({route,report}));
    await page.screenshot({path:out+'/'+route.id+'-'+viewport.name+'.png',fullPage:false});
    results.push({route:route.route,viewport:viewport.name,...report});
    await context.close();
  }
  fs.writeFileSync('audit-results/reader-browser.json',JSON.stringify({checks:results.length,results},null,2)+'\n');
  console.log(JSON.stringify({checks:results.length,results},null,2));
}finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1)});
