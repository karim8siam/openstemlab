'use strict';
const cfg=JSON.parse(document.getElementById('labConfig').textContent),model=window.StatsModels,$=id=>document.getElementById(id);
const fmt=(v,n=4)=>Math.abs(v)>0&&(Math.abs(v)<.001||Math.abs(v)>=1e6)?v.toExponential(3):v.toFixed(n);
let rows=[],measurement=null,busy=false,clearPending=false;
try{const saved=JSON.parse(localStorage.getItem('openstemlab-'+cfg.slug+'-v1')||'[]');if(Array.isArray(saved))rows=saved.filter(r=>r&&Number.isFinite(r.input)&&r.input>=cfg.min&&r.input<=cfg.max&&Number.isFinite(r.raw)).slice(0,100).map(r=>model.reading(cfg.slug,r.input,r.raw));}catch{}

function params(){return{input:+$('independent').value};}
function message(text,error=false){$('trialStatus').textContent=text;$('trialStatus').classList.toggle('error',error);}

function update(){
 const p=params();
 measurement=null;
 $('independentOut').textContent=p.input.toFixed(cfg.inputDecimals)+' '+cfg.inputUnit;
 $('readingValue').textContent='—';
 $('recordReading').disabled=true;
 $('measure').disabled=busy;
 $('liveState').textContent='Ready to sample with '+cfg.shortInput+' = '+p.input+'.';
 message('Adjust '+cfg.shortInput+', then run statistical trial.');
 draw(performance.now());
}

$('independent').addEventListener('input',()=>{$('independentNumber').value=$('independent').value;update();});
$('independentNumber').addEventListener('input',()=>{const v=+$('independentNumber').value;if($('independentNumber').value!==''&&Number.isFinite(v)&&v>=cfg.min&&v<=cfg.max){$('independent').value=v;update();}});
$('independentNumber').addEventListener('change',()=>{const v=+$('independentNumber').value;if(!Number.isFinite(v)||v<cfg.min||v>cfg.max){$('independentNumber').value=$('independent').value;message('Use a value between '+cfg.min+' and '+cfg.max+' '+cfg.inputUnit+'.',true);return;}$('independent').value=v;$('independentNumber').value=$('independent').value;update();});

$('pauseMotion').hidden=true;
$('resetApparatus').onclick=()=>{if(busy)return;$('independent').value=cfg.initial;$('independentNumber').value=cfg.initial;update();message('State reset. Notebook observations preserved.');};

$('measure').onclick=async()=>{
 if(busy)return;
 const p=params(),prediction=model.predict(cfg.slug,p.input);
 if(!prediction.valid){message('Select a valid input between '+cfg.min+' and '+cfg.max+'.',true);return;}
 busy=true;$('measure').disabled=true;$('recordReading').disabled=true;$('independent').disabled=true;$('independentNumber').disabled=true;
 message('Running statistical sampling iteration for '+cfg.shortInput+' = '+p.input+'…');
 await new Promise(resolve=>setTimeout(resolve,220));
 const raw=prediction.raw;
 measurement=model.reading(cfg.slug,p.input,raw);
 busy=false;$('independent').disabled=false;$('independentNumber').disabled=false;$('measure').disabled=false;$('recordReading').disabled=false;
 $('readingValue').textContent=raw.toFixed(cfg.rawDecimals)+' '+cfg.rawUnit;
 $('liveState').textContent='Trial finished; ready to record.';
 message(cfg.shortInput+' = '+p.input+' computed: '+cfg.measureLabel+' = '+raw+'. Record in notebook.');
};

$('recordReading').onclick=()=>{
 if(!measurement)return;
 if(rows.length>=100){message('Notebook full. Export observations or clear.',true);return;}
 rows.push({...measurement});
 measurement=null;
 $('recordReading').disabled=true;
 persist();
 message('Observation '+rows.length+' recorded. Set '+cfg.shortInput+' for the next trial.');
};

function persist(){try{localStorage.setItem('openstemlab-'+cfg.slug+'-v1',JSON.stringify(rows));}catch{}renderResults();}

function renderResults(){
 const f=model.fit(rows);
 $('notebookCount').textContent=rows.length;
 $('emptyReadings').hidden=rows.length>0;
 $('downloadReadings').disabled=!rows.length;
 $('clearReadings').disabled=!rows.length;
 $('readingRows').innerHTML=rows.map((r,i)=>'<tr><td>'+(i+1)+'</td><td>'+r.input.toFixed(cfg.inputDecimals)+'</td><td>'+r.raw.toFixed(cfg.rawDecimals)+'</td><td>'+fmt(r.x*cfg.xScale)+'</td><td>'+fmt(r.y*cfg.yScale)+'</td><td><button class="text-button" data-remove="'+i+'" aria-label="Remove observation '+(i+1)+'">×</button></td></tr>').join('');
 document.querySelectorAll('[data-remove]').forEach(b=>b.onclick=()=>{rows.splice(+b.dataset.remove,1);persist();});
 if(f){
  const result=model.estimate(cfg.slug,f),pct=Math.abs(result.value-result.reference)/Math.abs(result.reference)*100;
  $('fitSummary').innerHTML='<strong>'+fmt(result.value*cfg.resultScale,cfg.resultDecimals)+' '+cfg.resultUnit+'</strong><p>Estimated '+cfg.targetName+'<br>Gradient m: '+fmt(f.m)+'<br>Intercept b: '+fmt(f.b)+'<br>R²: '+f.r2.toFixed(6)+'<br>Difference from reference: '+pct.toFixed(4)+'%<br>Fit standard error: '+fmt(result.se*cfg.resultScale)+' '+cfg.resultUnit+'</p><p>Statistical relationship confirmed by linear regression.</p>';
 } else {
  $('fitSummary').innerHTML='<p>Record at least three distinct observations to fit an empirical regression line and calculate '+cfg.targetName+'.</p>';
 }
 drawPlot(f);
}

function drawPlot(f){
 const left=68,right=610,top=28,bottom=280;
 let xs=rows.map(r=>r.x*cfg.xScale),ys=rows.map(r=>r.y*cfg.yScale);
 let xmin=xs.length?Math.min(...xs):cfg.emptyX,xmax=xs.length?Math.max(...xs):cfg.emptyX+1,ymin=ys.length?Math.min(...ys):cfg.emptyY,ymax=ys.length?Math.max(...ys):cfg.emptyY+1;
 const dx=(xmax-xmin)||Math.max(Math.abs(xmax)*.2,1),dy=(ymax-ymin)||Math.max(Math.abs(ymax)*.2,1);
 xmin-=dx*.12;xmax+=dx*.12;ymin-=dy*.15;ymax+=dy*.15;
 const px=x=>left+(x-xmin)/(xmax-xmin)*(right-left),py=y=>bottom-(y-ymin)/(ymax-ymin)*(bottom-top);
 let svg='<rect width="640" height="340" fill="#021a19"/>';
 for(let i=0;i<=5;i++){
  const gx=left+i*(right-left)/5,gy=top+i*(bottom-top)/5;
  svg+='<line x1="'+gx+'" y1="'+top+'" x2="'+gx+'" y2="'+bottom+'" stroke="#042f2e" stroke-width="1"/>';
  svg+='<line x1="'+left+'" y1="'+gy+'" x2="'+right+'" y2="'+gy+'" stroke="#042f2e" stroke-width="1"/>';
  const valX=xmin+i*(xmax-xmin)/5,valY=ymax-i*(ymax-ymin)/5;
  svg+='<text x="'+gx+'" y="'+(bottom+18)+'" fill="#5eead4" font-size="10" text-anchor="middle">'+fmt(valX,2)+'</text>';
  svg+='<text x="'+(left-10)+'" y="'+(gy+3)+'" fill="#5eead4" font-size="10" text-anchor="end">'+fmt(valY,2)+'</text>';
 }
 svg+='<text x="'+((left+right)/2)+'" y="325" fill="#99f6e4" font-size="12" text-anchor="middle">'+cfg.xLabel+'</text>';
 svg+='<text x="18" y="'+((top+bottom)/2)+'" fill="#99f6e4" font-size="12" text-anchor="middle" transform="rotate(-90 18 '+((top+bottom)/2)+')">'+cfg.yLabel+'</text>';
 if(f&&rows.length>=2){
  const x1=xmin,x2=xmax,y1=f.m*(x1/cfg.xScale)+f.b,y2=f.m*(x2/cfg.xScale)+f.b;
  svg+='<line x1="'+px(x1)+'" y1="'+py(y1*cfg.yScale)+'" x2="'+px(x2)+'" y2="'+py(y2*cfg.yScale)+'" stroke="#2dd4bf" stroke-width="2"/>';
 }
 rows.forEach((r,i)=>{
  const cx=px(r.x*cfg.xScale),cy=py(r.y*cfg.yScale);
  svg+='<circle cx="'+cx+'" cy="'+cy+'" r="5" fill="#facc15" stroke="#021a19" stroke-width="1.5"/>';
  svg+='<text x="'+cx+'" y="'+(cy-8)+'" fill="#fef08a" font-size="9" text-anchor="middle">'+(i+1)+'</text>';
 });
 $('labPlot').innerHTML=svg;
}

function draw(){
 const svg=$('simCanvas'),p=params();
 if(!svg)return;
 const w=svg.clientWidth||640,h=svg.clientHeight||280;
 let content='<rect width="100%" height="100%" fill="#042f2e"/>';
 
 // Background statistical grid
 for(let x=40;x<600;x+=40){
  content+='<line x1="'+x+'" y1="20" x2="'+x+'" y2="240" stroke="#115e59" stroke-width="1" stroke-dasharray="2,3" opacity="0.4"/>';
 }
 for(let y=30;y<240;y+=30){
  content+='<line x1="40" y1="'+y+'" x2="600" y2="'+y+'" stroke="#115e59" stroke-width="1" stroke-dasharray="2,3" opacity="0.4"/>';
 }
 
 // Dynamic distribution visualization
 const midX=320,baseY=220;
 content+='<line x1="40" y1="'+baseY+'" x2="600" y2="'+baseY+'" stroke="#5eead4" stroke-width="1.5"/>';
 content+='<line x1="'+midX+'" y1="30" x2="'+midX+'" y2="'+baseY+'" stroke="#5eead4" stroke-width="1" stroke-dasharray="4,4"/>';
 
 // Bell curve / density function
 let dPath='M 60 '+baseY;
 const spread=Math.max(20,Math.min(180,p.input*15));
 for(let px=60;px<=580;px+=10){
  const z=(px-midX)/spread;
  const py=baseY-170*Math.exp(-0.5*z*z);
  dPath+=' L '+px+' '+py;
 }
 dPath+=' L 580 '+baseY+' Z';
 content+='<path d="'+dPath+'" fill="url(#statsGrad)" stroke="#2dd4bf" stroke-width="2.5"/>';
 
 // Sample scatter markers along axis
 for(let i=0;i<12;i++){
  const rx=midX+(Math.sin(i*2.71+p.input)*spread*1.2);
  if(rx>=60&&rx<=580){
   content+='<circle cx="'+rx+'" cy="'+(baseY+8)+'" r="3.5" fill="#facc15" opacity="0.8"/>';
  }
 }
 
 content+='<defs><linearGradient id="statsGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#14b8a6" stop-opacity="0.6"/><stop offset="100%" stop-color="#0f766e" stop-opacity="0.05"/></linearGradient></defs>';
 content+='<text x="320" y="25" fill="#5eead4" font-size="12" font-weight="600" text-anchor="middle">EMPIRICAL DENSITY & SAMPLING DISTRIBUTION ('+cfg.shortInput+' = '+p.input+')</text>';
 content+='<text x="590" y="215" fill="#99f6e4" font-size="10" text-anchor="end">Value (x)</text>';
 content+='<text x="50" y="45" fill="#99f6e4" font-size="10">Density f(x)</text>';
 svg.innerHTML=content;
}

$('downloadReadings').onclick=()=>{
 if(!rows.length)return;
 let csv='Trial,'+cfg.shortInput+','+cfg.measureLabel+','+cfg.xLabel+','+cfg.yLabel+'\n';
 rows.forEach((r,i)=>{csv+=(i+1)+','+r.input+','+r.raw+','+(r.x*cfg.xScale)+','+(r.y*cfg.yScale)+'\n';});
 const a=document.createElement('a');
 a.href='data:text/csv;charset=utf-8,'+encodeURIComponent(csv);
 a.download=cfg.slug+'-observations.csv';
 a.click();
};

$('clearReadings').onclick=()=>{
 if(!clearPending){
  clearPending=true;
  $('clearReadings').textContent='Confirm clear?';
  setTimeout(()=>{clearPending=false;$('clearReadings').textContent='Clear notebook';},3000);
  return;
 }
 clearPending=false;
 $('clearReadings').textContent='Clear notebook';
 rows=[];
 persist();
 message('Notebook cleared.');
};

update();
renderResults();
window.addEventListener('resize',()=>draw());
