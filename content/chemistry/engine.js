'use strict';
const cfg=JSON.parse(document.getElementById('labConfig').textContent),model=window.ChemistryModels,$=id=>document.getElementById(id);
const fmt=(v,n=4)=>Math.abs(v)>0&&(Math.abs(v)<.001||Math.abs(v)>=1e6)?v.toExponential(3):v.toFixed(n);
let rows=[],measurement=null,busy=false,clearPending=false;
try{const saved=JSON.parse(localStorage.getItem('openstemlab-'+cfg.slug+'-v1')||'[]');if(Array.isArray(saved))rows=saved.filter(r=>r&&Number.isFinite(r.input)&&r.input>=cfg.min&&r.input<=cfg.max&&Number.isFinite(r.raw)&&r.raw>0).slice(0,100).map(r=>model.reading(cfg.slug,r.input,r.raw));}catch{}

function params(){return{input:+$('independent').value};}
function message(text,error=false){$('trialStatus').textContent=text;$('trialStatus').classList.toggle('error',error);}

function update(){
 const p=params();
 measurement=null;
 $('independentOut').textContent=p.input.toFixed(cfg.inputDecimals)+' '+cfg.inputUnit;
 $('readingValue').textContent='—';
 $('recordReading').disabled=true;
 $('measure').disabled=busy;
 $('liveState').textContent='Ready to dispense '+p.input.toFixed(cfg.inputDecimals)+' '+cfg.inputUnit+' of liquid.';
 message('Adjust '+cfg.shortInput+' V, then weigh the dispensed aliquot.');
 draw(performance.now());
}

$('independent').addEventListener('input',()=>{$('independentNumber').value=$('independent').value;update();});
$('independentNumber').addEventListener('input',()=>{const v=+$('independentNumber').value;if($('independentNumber').value!==''&&Number.isFinite(v)&&v>=cfg.min&&v<=cfg.max){$('independent').value=v;update();}});
$('independentNumber').addEventListener('change',()=>{const v=+$('independentNumber').value;if(!Number.isFinite(v)||v<cfg.min||v>cfg.max){$('independentNumber').value=$('independent').value;message('Use a value between '+cfg.min+' and '+cfg.max+' '+cfg.inputUnit+'.',true);return;}$('independent').value=v;$('independentNumber').value=$('independent').value;update();});

$('pauseMotion').hidden=true;
$('resetApparatus').onclick=()=>{if(busy)return;$('independent').value=cfg.initial;$('independentNumber').value=cfg.initial;update();message('Apparatus reset to standard tare baseline. Your notebook is kept.');};

$('measure').onclick=async()=>{
 if(busy)return;
 const p=params(),prediction=model.predict(cfg.slug,p.input);
 if(!prediction.valid){message('Select a valid '+cfg.shortInput+' between '+cfg.min+' and '+cfg.max+' '+cfg.inputUnit+'.',true);return;}
 busy=true;$('measure').disabled=true;$('recordReading').disabled=true;$('independent').disabled=true;$('independentNumber').disabled=true;
 message('Dispensing '+p.input.toFixed(cfg.inputDecimals)+' '+cfg.inputUnit+' into tared beaker…');
 await new Promise(resolve=>setTimeout(resolve,400));
 const raw=prediction.raw;
 measurement=model.reading(cfg.slug,p.input,raw);
 busy=false;$('independent').disabled=false;$('independentNumber').disabled=false;$('measure').disabled=false;$('recordReading').disabled=false;
 $('readingValue').textContent=raw.toFixed(cfg.rawDecimals)+' '+cfg.rawUnit;
 $('liveState').textContent='Analytical balance stabilized: '+raw.toFixed(cfg.rawDecimals)+' g net mass.';
 message('Gravimetric measurement complete: '+raw.toFixed(cfg.rawDecimals)+' '+cfg.rawUnit+' for '+p.input.toFixed(cfg.inputDecimals)+' '+cfg.inputUnit+'. Record in notebook.');
 draw(performance.now());
};

$('recordReading').onclick=()=>{
 if(!measurement)return;
 if(rows.length>=100){message('Notebook full. Export readings or clear the notebook.',true);return;}
 rows.push({...measurement});
 measurement=null;
 $('recordReading').disabled=true;
 persist();
 message('Observation '+rows.length+' recorded. Change '+cfg.shortInput+' for the next trial.');
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
  const result=model.estimate(cfg.slug,f),pct=Math.abs(result.value-result.reference)/result.reference*100;
  $('fitSummary').innerHTML='<strong>'+fmt(result.value*cfg.resultScale,cfg.resultDecimals)+' '+cfg.resultUnit+'</strong><p>Estimated '+cfg.target+'<br>Gradient: '+fmt(f.m)+'<br>Intercept: '+fmt(f.b)+' g<br>R²: '+f.r2.toFixed(5)+'<br>Difference from CIPM reference: '+pct.toFixed(3)+'%<br>Fit standard error: '+fmt(result.se*cfg.resultScale)+' '+cfg.resultUnit+'</p><p>Linear regression eliminates constant tare and meniscus biases.</p>';
 } else {
  $('fitSummary').innerHTML='<p>Record at least three distinct '+cfg.shortInput+' values to fit a regression line and calculate '+cfg.target+'.</p>';
 }
 drawPlot(f);
}

function drawPlot(f){
 const left=68,right=610,top=28,bottom=280;
 let xs=rows.map(r=>r.x*cfg.xScale),ys=rows.map(r=>r.y*cfg.yScale);
 let xmin=xs.length?Math.min(...xs):cfg.emptyX[0],xmax=xs.length?Math.max(...xs):cfg.emptyX[1],ymin=ys.length?Math.min(...ys):cfg.emptyY[0],ymax=ys.length?Math.max(...ys):cfg.emptyY[1];
 const dx=(xmax-xmin)||Math.max(Math.abs(xmax)*.2,1),dy=(ymax-ymin)||Math.max(Math.abs(ymax)*.2,1);
 xmin-=dx*.12;xmax+=dx*.12;ymin-=dy*.15;ymax+=dy*.15;
 const px=x=>left+(x-xmin)/(xmax-xmin)*(right-left),py=y=>bottom-(y-ymin)/(ymax-ymin)*(bottom-top);
 let svg='';
 for(let i=0;i<5;i++){
  const x=xmin+i*(xmax-xmin)/4,y=ymin+i*(ymax-ymin)/4;
  svg+='<line x1="'+left+'" y1="'+py(y)+'" x2="'+right+'" y2="'+py(y)+'" stroke="#223b28" stroke-width="1"/>';
  svg+='<text x="'+(left-8)+'" y="'+(py(y)+4)+'" text-anchor="end" font-size="10" fill="#789c80">'+fmt(y,1)+'</text>';
  svg+='<text x="'+px(x)+'" y="300" text-anchor="middle" font-size="10" fill="#789c80">'+fmt(x,1)+'</text>';
 }
 svg+='<path d="M'+left+' '+top+'V'+bottom+'H'+right+'" stroke="#466e4e" fill="none"/>';
 svg+='<text x="335" y="332" text-anchor="middle" fill="#9ec4a6" font-size="12">'+cfg.xAxis+'</text>';
 svg+='<text transform="translate(18 160) rotate(-90)" text-anchor="middle" fill="#9ec4a6" font-size="12">'+cfg.yAxis+'</text>';
 if(f){
  const pts=[];
  for(let i=0;i<=100;i++){
   const x=xmin+i*(xmax-xmin)/100,y=(f.m*(x/cfg.xScale)+f.b)*cfg.yScale;
   pts.push(px(x).toFixed(1)+','+py(y).toFixed(1));
  }
  svg+='<polyline points="'+pts.join(' ')+'" stroke="#38a169" stroke-width="2" fill="none"/>';
 }
 rows.forEach((r,i)=>{
  svg+='<circle cx="'+px(r.x*cfg.xScale)+'" cy="'+py(r.y*cfg.yScale)+'" r="4.5" fill="#48bb78" stroke="#142b1a" stroke-width="1.5"><title>Aliquot '+(i+1)+': V = '+r.input.toFixed(cfg.inputDecimals)+' mL, m = '+r.raw.toFixed(cfg.rawDecimals)+' g</title></circle>';
 });
 $('labPlot').innerHTML=svg;
}

$('downloadReadings').onclick=()=>{
 if(!rows.length)return;
 let csv='aliquot,volume_mL,mass_g,x_metric,y_metric\n';
 rows.forEach((r,i)=>{csv+=(i+1)+','+r.input.toFixed(cfg.inputDecimals)+','+r.raw.toFixed(cfg.rawDecimals)+','+(r.x*cfg.xScale).toFixed(4)+','+(r.y*cfg.yScale).toFixed(4)+'\n';});
 const a=document.createElement('a');
 a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));
 a.download=cfg.slug+'-observations.csv';
 a.click();
};

$('clearReadings').onclick=()=>{
 if(!clearPending){clearPending=true;$('clearReadings').textContent='Confirm clear?';setTimeout(()=>{clearPending=false;$('clearReadings').textContent='Clear notebook';},3000);return;}
 rows=[];clearPending=false;$('clearReadings').textContent='Clear notebook';persist();message('Notebook cleared. Apparatus remains ready.');
};

$('checkEstimate').onclick=()=>{
 const val=+$('studentEstimate').value,f=model.fit(rows);
 if(!Number.isFinite(val)||val<=0){$('estimateFeedback').textContent='Enter a positive calculated density value.';return;}
 if(!f){$('estimateFeedback').textContent='Record at least three observations first to compare with regression.';return;}
 const result=model.estimate(cfg.slug,f),pct=Math.abs(val-result.value*cfg.resultScale)/(result.value*cfg.resultScale)*100;
 $('estimateFeedback').textContent=pct<1.0?'Excellent! Within '+pct.toFixed(2)+'% of regression slope ('+fmt(result.value*cfg.resultScale,cfg.resultDecimals)+' '+cfg.resultUnit+').':'Off by '+pct.toFixed(1)+'%. Fitted slope is '+fmt(result.value*cfg.resultScale,cfg.resultDecimals)+' '+cfg.resultUnit+'. Check S_xy / S_xx.';
};

document.querySelectorAll('[data-quiz]').forEach(b=>b.onclick=()=>{
 const q=cfg.quiz[+b.dataset.quiz],j=+b.dataset.choice;
 document.querySelectorAll('[data-quiz="'+b.dataset.quiz+'"]').forEach(x=>x.classList.remove('correct','wrong'));
 b.classList.add(j===q.correct?'correct':'wrong');
 $('quizFeedback'+b.dataset.quiz).textContent=(j===q.correct?'Correct. ':'Think it through. ')+q.explanation;
});

let currentSimMode='bench';
document.querySelectorAll('.sim-mode-btn').forEach(btn=>{
 btn.onclick=()=>{
  document.querySelectorAll('.sim-mode-btn').forEach(b=>{b.classList.remove('active');b.setAttribute('aria-selected','false');});
  btn.classList.add('active');
  btn.setAttribute('aria-selected','true');
  currentSimMode=btn.dataset.sim;
  draw(performance.now());
 };
});

function draw(t){
 const p=params();
 const rawVal=measurement?measurement.raw:model.predict(cfg.slug,p.input).raw;
 if(currentSimMode==='compare'){
  $('apparatusDiagram').innerHTML=drawCompareView(p,rawVal);
  return;
 }
 if(currentSimMode==='sandbox'){
  $('apparatusDiagram').innerHTML=drawSandboxView(p,rawVal);
  return;
 }
 $('apparatusDiagram').innerHTML=drawBenchView(p,rawVal);
}

function drawBenchView(p,rawVal){
 const v=p.input;
 const m_disp=measurement?measurement.raw:(busy?rawVal*0.75:0.0000);
 const v_pct=v/35.0;
 const liquidHeight=Math.min(48, Math.max(6, v_pct*45));
 
 let svg='<defs><pattern id="chemGrid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" stroke="#ffffff" stroke-opacity=".03" fill="none"/></pattern>';
 svg+='<linearGradient id="glassGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#ffffff" stop-opacity=".15"/><stop offset="30%" stop-color="#ffffff" stop-opacity=".05"/><stop offset="80%" stop-color="#ffffff" stop-opacity=".12"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".25"/></linearGradient>';
 svg+='<linearGradient id="waterGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#38a169" stop-opacity=".4"/><stop offset="50%" stop-color="#48bb78" stop-opacity=".55"/><stop offset="100%" stop-color="#2f855a" stop-opacity=".45"/></linearGradient>';
 svg+='<linearGradient id="metalGrad" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#2d3748"/><stop offset="100%" stop-color="#1a202c"/></linearGradient>';
 svg+='</defs><rect width="720" height="320" fill="#0b140e"/><rect width="720" height="320" fill="url(#chemGrid)"/>';

 // Lab Table surface
 svg+='<rect x="0" y="270" width="720" height="50" fill="#132419" stroke="#1f3b2a" stroke-width="1"/>';
 svg+='<line x1="0" y1="270" x2="720" y2="270" stroke="#2d523b" stroke-width="2"/>';

 // Retort Stand (holding burette on left)
 svg+='<rect x="60" y="260" width="100" height="10" rx="2" fill="url(#metalGrad)" stroke="#4a5568" stroke-width="1"/>';
 svg+='<rect x="105" y="25" width="8" height="235" fill="url(#metalGrad)" stroke="#4a5568" stroke-width="1"/>';
 // Clamps
 svg+='<rect x="95" y="70" width="55" height="8" rx="2" fill="#718096"/>';
 svg+='<circle cx="109" cy="74" r="5" fill="#4a5568"/>';
 svg+='<rect x="95" y="160" width="55" height="8" rx="2" fill="#718096"/>';
 svg+='<circle cx="109" cy="164" r="5" fill="#4a5568"/>';

 // Burette body (x = 135 to 155)
 const bX=140,bW=14,bTop=35,bBottom=210;
 svg+='<rect x="'+bX+'" y="'+bTop+'" width="'+bW+'" height="'+(bBottom-bTop)+'" fill="url(#glassGrad)" stroke="#789c80" stroke-width="1.2" rx="1"/>';
 // Schellbach blue line in burette
 svg+='<line x1="'+(bX+bW/2)+'" y1="'+bTop+'" x2="'+(bX+bW/2)+'" y2="'+bBottom+'" stroke="#3182ce" stroke-width="1.2" stroke-opacity=".7"/>';
 // Liquid inside burette (draining as volume increases)
 const bLiquidTop=bTop + v_pct*110;
 svg+='<rect x="'+(bX+1)+'" y="'+bLiquidTop+'" width="'+(bW-2)+'" height="'+(bBottom-bLiquidTop)+'" fill="url(#waterGrad)"/>';
 svg+='<ellipse cx="'+(bX+bW/2)+'" cy="'+bLiquidTop+'" rx="'+(bW/2-1)+'" ry="2.5" fill="#68d391" fill-opacity=".7"/>';
 // Burette graduation lines
 for(let gy=bTop+10;gy<bBottom-10;gy+=8){
  const isMajor=(gy-bTop-10)%32===0;
  svg+='<line x1="'+bX+'" y1="'+gy+'" x2="'+(bX+(isMajor?6:3))+'" y2="'+gy+'" stroke="#a0aec0" stroke-width="'+(isMajor?1:0.7)+'"/>';
 }
 // Burette stopcock and tip
 svg+='<path d="M'+(bX+2)+' '+bBottom+' L'+(bX+5)+' '+(bBottom+14)+' L'+(bX+9)+' '+(bBottom+14)+' L'+(bX+12)+' '+bBottom+' Z" fill="url(#glassGrad)" stroke="#789c80"/>';
 svg+='<rect x="'+(bX-3)+'" y="'+(bBottom+8)+'" width="20" height="6" rx="2" fill="#e2e8f0" stroke="#a0aec0"/>'; // stopcock
 svg+='<path d="M'+(bX+5)+' '+(bBottom+14)+' L'+(bX+6)+' '+(bBottom+30)+' L'+(bX+8)+' '+(bBottom+30)+' L'+(bX+9)+' '+(bBottom+14)+' Z" fill="url(#glassGrad)" stroke="#789c80"/>';
 // Droplet stream when dispensing
 if(busy){
  svg+='<line x1="'+(bX+7)+'" y1="'+(bBottom+30)+'" x2="'+(bX+7)+'" y2="240" stroke="#48bb78" stroke-width="1.5" stroke-dasharray="4,3"/>';
  svg+='<circle cx="'+(bX+7)+'" cy="236" r="2.2" fill="#68d391"/>';
 }

 // Analytical Balance (centered at x = 360)
 const balX=240,balW=240,balBaseY=220,balH=50;
 // Granite slab
 svg+='<rect x="'+(balX-15)+'" y="262" width="'+(balW+30)+'" height="8" rx="2" fill="#2d3748" stroke="#1a202c"/>';
 // Balance housing
 svg+='<rect x="'+balX+'" y="'+balBaseY+'" width="'+balW+'" height="'+balH+'" rx="4" fill="#1a271f" stroke="#2d523b" stroke-width="1.5"/>';
 // Digital Display Screen
 svg+='<rect x="'+(balX+45)+'" y="'+(balBaseY+18)+'" width="150" height="24" rx="3" fill="#061009" stroke="#1e3b27" stroke-width="1"/>';
 svg+='<text x="'+(balX+185)+'" y="'+(balBaseY+35)+'" text-anchor="end" fill="#48bb78" font-size="15" font-family="monospace" font-weight="bold">'+(measurement?m_disp.toFixed(4):(busy?(rawVal*0.75).toFixed(4):'0.0000'))+' g</text>';
 svg+='<circle cx="'+(balX+55)+'" cy="'+(balBaseY+30)+'" r="2.5" fill="'+(busy?'#ecc94b':'#48bb78')+'"/>';
 svg+='<text x="'+(balX+62)+'" y="'+(balBaseY+33)+'" fill="#718096" font-size="7">STABLE</text>';
 // Tare and Cal buttons
 svg+='<rect x="'+(balX+18)+'" y="'+(balBaseY+22)+'" width="20" height="14" rx="2" fill="#274632" stroke="#3b6b4c"/><text x="'+(balX+28)+'" y="'+(balBaseY+32)+'" text-anchor="middle" fill="#a0aec0" font-size="6">TARE</text>';
 svg+='<rect x="'+(balX+202)+'" y="'+(balBaseY+22)+'" width="20" height="14" rx="2" fill="#274632" stroke="#3b6b4c"/><text x="'+(balX+212)+'" y="'+(balBaseY+32)+'" text-anchor="middle" fill="#a0aec0" font-size="6">CAL</text>';

 // Glass Draft Shield Enclosure
 const dsX=balX+25,dsW=balW-50,dsTop=75,dsH=balBaseY-dsTop;
 svg+='<rect x="'+dsX+'" y="'+dsTop+'" width="'+dsW+'" height="'+dsH+'" fill="url(#glassGrad)" stroke="#386b48" stroke-width="1.2" rx="2"/>';
 svg+='<line x1="'+(dsX+dsW/2)+'" y1="'+dsTop+'" x2="'+(dsX+dsW/2)+'" y2="'+balBaseY+'" stroke="#ffffff" stroke-opacity=".08" stroke-width="1"/>';
 // Weighing Pan inside draft shield
 svg+='<rect x="'+(dsX+dsW/2-35)+'" y="'+(balBaseY-8)+'" width="70" height="5" rx="1.5" fill="#cbd5e0" stroke="#718096"/>';
 svg+='<rect x="'+(dsX+dsW/2-4)+'" y="'+(balBaseY-3)+'" width="8" height="3" fill="#a0aec0"/>';

 // Receiving Beaker (100 mL) on Pan (x centered at dsX + dsW/2 = 360)
 const bkX=330,bkW=60,bkH=70,bkY=balBaseY-8-bkH;
 svg+='<rect x="'+bkX+'" y="'+bkY+'" width="'+bkW+'" height="'+bkH+'" rx="2" fill="url(#glassGrad)" stroke="#789c80" stroke-width="1.2"/>';
 svg+='<path d="M'+(bkX+bkW)+' '+bkY+' L'+(bkX+bkW+6)+' '+(bkY-4)+' L'+(bkX+bkW)+' '+(bkY+4)+' Z" fill="url(#glassGrad)" stroke="#789c80"/>'; // spout
 // Water inside beaker
 const wY=bkY+bkH-liquidHeight;
 svg+='<rect x="'+(bkX+1.5)+'" y="'+wY+'" width="'+(bkW-3)+'" height="'+(liquidHeight-1)+'" rx="1" fill="url(#waterGrad)"/>';
 svg+='<ellipse cx="'+(bkX+bkW/2)+'" cy="'+wY+'" rx="'+(bkW/2-2)+'" ry="3" fill="#68d391" fill-opacity=".65"/>';
 // Beaker graduation markings
 for(let gy=bkY+15;gy<bkY+bkH-10;gy+=12){
  svg+='<line x1="'+bkX+'" y1="'+gy+'" x2="'+(bkX+8)+'" y2="'+gy+'" stroke="#e2e8f0" stroke-opacity=".4" stroke-width="1"/>';
 }
 svg+='<text x="'+(bkX+12)+'" y="'+(bkY+28)+'" fill="#cbd5e0" fill-opacity=".5" font-size="7">100 mL</text>';

 // Right Side: Thermostat Water Bath & Thermometer
 const bathX=530,bathY=175,bathW=150,bathH=95;
 svg+='<rect x="'+bathX+'" y="'+bathY+'" width="'+bathW+'" height="'+bathH+'" rx="5" fill="#12251a" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<rect x="'+(bathX+10)+'" y="'+(bathY+12)+'" width="'+(bathW-20)+'" height="'+(bathH-22)+'" rx="3" fill="#09140e" stroke="#1a3825"/>';
 svg+='<text x="'+(bathX+bathW/2)+'" y="'+(bathY+28)+'" text-anchor="middle" fill="#789c80" font-size="9" font-weight="bold">THERMOSTATIC CONTROLLER</text>';
 // LED display of temperature
 svg+='<rect x="'+(bathX+25)+'" y="'+(bathY+36)+'" width="100" height="26" rx="3" fill="#040d07" stroke="#163820"/>';
 svg+='<text x="'+(bathX+75)+'" y="'+(bathY+54)+'" text-anchor="middle" fill="#48bb78" font-size="15" font-family="monospace" font-weight="bold">20.00 °C</text>';
 svg+='<text x="'+(bathX+bathW/2)+'" y="'+(bathY+76)+'" text-anchor="middle" fill="#81e6d9" font-size="8">±0.01 °C PELTIER REGULATED</text>';

 // Status overlay on top bar
 svg+='<text x="360" y="24" text-anchor="middle" fill="#81e6d9" font-size="11" font-weight="bold">CLASS A VOLUMETRIC GRAVIMETRY · ρ = m / V = 0.9982 g/mL</text>';
 return svg;
}

function drawCompareView(p,rawVal){
 let svg='<rect width="720" height="320" fill="#0b140e"/>';
 const text=(x,y,str,color='#789c80',size=11)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';
 svg+=text(360,26,'ANALYTICAL METROLOGY COMPARISON: THREE DENSITY METHODOLOGIES','#a7f3d0',12);

 const methods=[
  {
   name:'1. Capillary Pycnometer',
   type:'Hydrostatic Confinement (Gay-Lussac)',
   prec:'±0.0001 g/mL',
   vol:'25.000 mL',
   time:'30–45 min',
   adv:'Eliminates optical meniscus reading; exact volume calibration via CIPM water standard.',
   col:'#38a169',
   bar:88
  },
  {
   name:'2. Class A Volumetric Burette',
   type:'Gravimetric Aliquot Titration',
   prec:'±0.0020 g/mL',
   vol:'5.0–50.0 mL',
   time:'5–10 min',
   adv:'Rapid sequential aliquots; linear regression slope eliminates constant tare/meniscus offsets.',
   col:'#3182ce',
   bar:62
  },
  {
   name:'3. Digital Oscillating U-Tube',
   type:'Harmonic Resonance (Anton Paar)',
   prec:'±0.00005 g/mL',
   vol:'1.5 mL',
   time:'1–2 min',
   adv:'Frequency period T² = A + B·ρ; minimal sample volume; automated Peltier control.',
   col:'#d69e2e',
   bar:98
  }
 ];

 methods.forEach((m,idx)=>{
  const cx=50+idx*215,cy=45,cw=195,ch=245;
  svg+='<rect x="'+cx+'" y="'+cy+'" width="'+cw+'" height="'+ch+'" rx="6" fill="#101e14" stroke="'+m.col+'" stroke-width="1.5"/>';
  svg+='<rect x="'+cx+'" y="'+cy+'" width="'+cw+'" height="28" rx="5" fill="'+m.col+'" fill-opacity=".2"/>';
  svg+='<text x="'+(cx+cw/2)+'" y="'+(cy+18)+'" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="bold">'+m.name+'</text>';
  svg+='<text x="'+(cx+cw/2)+'" y="'+(cy+42)+'" text-anchor="middle" fill="#a0aec0" font-size="8.5">'+m.type+'</text>';
  svg+='<line x1="'+(cx+12)+'" y1="'+(cy+52)+'" x2="'+(cx+cw-12)+'" y2="'+(cy+52)+'" stroke="#1f3b28"/>';

  svg+='<text x="'+(cx+15)+'" y="'+(cy+70)+'" fill="#789c80" font-size="8.5">PRECISION LIMIT:</text>';
  svg+='<text x="'+(cx+cw-15)+'" y="'+(cy+70)+'" text-anchor="end" fill="'+m.col+'" font-size="10" font-family="monospace" font-weight="bold">'+m.prec+'</text>';

  svg+='<text x="'+(cx+15)+'" y="'+(cy+92)+'" fill="#789c80" font-size="8.5">SAMPLE VOLUME:</text>';
  svg+='<text x="'+(cx+cw-15)+'" y="'+(cy+92)+'" text-anchor="end" fill="#e2e8f0" font-size="9" font-family="monospace">'+m.vol+'</text>';

  svg+='<text x="'+(cx+15)+'" y="'+(cy+114)+'" fill="#789c80" font-size="8.5">EQUILIBRATION TIME:</text>';
  svg+='<text x="'+(cx+cw-15)+'" y="'+(cy+114)+'" text-anchor="end" fill="#e2e8f0" font-size="9" font-family="monospace">'+m.time+'</text>';

  svg+='<line x1="'+(cx+12)+'" y1="'+(cy+126)+'" x2="'+(cx+cw-12)+'" y2="'+(cy+126)+'" stroke="#1f3b28"/>';
  svg+='<text x="'+(cx+15)+'" y="'+(cy+144)+'" fill="#789c80" font-size="8">ANALYTICAL RESOLUTION SCORE</text>';
  svg+='<rect x="'+(cx+15)+'" y="'+(cy+152)+'" width="'+(cw-30)+'" height="8" rx="2" fill="#08140c"/>';
  svg+='<rect x="'+(cx+15)+'" y="'+(cy+152)+'" width="'+((cw-30)*m.bar/100)+'" height="8" rx="2" fill="'+m.col+'"/>';

  svg+='<foreignObject x="'+(cx+12)+'" y="'+(cy+170)+'" width="'+(cw-24)+'" height="68"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:8.5px;color:#a0aec0;line-height:1.4;margin:0">'+m.adv+'</p></foreignObject>';
 });

 svg+=text(360,306,'CIPM Recommendation: Buoyancy correction Δm = m_app · ρ_air · (1/ρ_sample - 1/ρ_weights) is mandatory for 4-decimal precision.','#68d391',9.5);
 return svg;
}

function drawSandboxView(p,rawVal){
 let svg='<rect width="720" height="320" fill="#0b140e"/>';
 const text=(x,y,str,color='#789c80',size=11)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';
 svg+=text(360,24,'THERMODYNAMIC EQUATION OF STATE: WATER DENSITY ANOMALY (0 °C TO 100 °C)','#68d391',12);

 // Density vs Temperature Plot (0 to 100 C)
 const pX=60,pY=50,pW=400,pH=220;
 svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" fill="#061009" stroke="#1f3b28" rx="4"/>';
 // Axes
 const tMin=0,tMax=100,rhoMin=0.95,rhoMax=1.005;
 const mapX=t=>pX+(t-tMin)/(tMax-tMin)*pW;
 const mapY=r=>pY+pH-(r-rhoMin)/(rhoMax-rhoMin)*pH;

 // Grid lines
 [0,20,40,60,80,100].forEach(deg=>{
  svg+='<line x1="'+mapX(deg)+'" y1="'+pY+'" x2="'+mapX(deg)+'" y2="'+(pY+pH)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+mapX(deg)+'" y="'+(pY+pH+14)+'" text-anchor="middle" fill="#789c80" font-size="8.5">'+deg+' °C</text>';
 });
 [0.96,0.98,1.00].forEach(r=>{
  svg+='<line x1="'+pX+'" y1="'+mapY(r)+'" x2="'+(pX+pW)+'" y2="'+mapY(r)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+(pX-6)+'" y="'+(mapY(r)+3)+'" text-anchor="end" fill="#789c80" font-size="8.5">'+r.toFixed(2)+'</text>';
 });

 // Water density curve using Tilton-Taylor formula approximation
 const pts=[];
 for(let deg=0;deg<=100;deg+=1){
  // Polynomial approximation of water density: ρ(T) ≈ 0.99984 + 6.79e-5·T - 9.10e-6·T² + 1.00e-7·T³ - 1.12e-9·T⁴ + 6.53e-12·T⁵
  const t_val=deg;
  const r_val=0.9998395 + 6.79829998e-5*t_val - 9.106025e-6*t_val**2 + 1.0052729e-7*t_val**3 - 1.1267135e-9*t_val**4 + 6.536332e-12*t_val**5;
  pts.push(mapX(t_val).toFixed(1)+','+mapY(r_val).toFixed(1));
 }
 svg+='<polyline points="'+pts.join(' ')+'" fill="none" stroke="#48bb78" stroke-width="2.5"/>';

 // Highlight Density Peak at 3.98 °C
 const xPeak=mapX(3.98),yPeak=mapY(0.99997);
 svg+='<circle cx="'+xPeak+'" cy="'+yPeak+'" r="4.5" fill="#f6e05e" stroke="#142b1a" stroke-width="1.5"/>';
 svg+='<line x1="'+xPeak+'" y1="'+yPeak+'" x2="'+xPeak+'" y2="'+(pY+20)+'" stroke="#f6e05e" stroke-dasharray="3,2"/>';
 svg+='<text x="'+(xPeak+8)+'" y="'+(pY+28)+'" fill="#f6e05e" font-size="8.5" font-weight="bold">MAX DENSITY: 3.98 °C (0.99997 g/mL)</text>';

 // Current Laboratory Operating Point (20.0 °C)
 const xLab=mapX(20.0),yLab=mapY(0.99820);
 svg+='<circle cx="'+xLab+'" cy="'+yLab+'" r="5" fill="#63b3ed" stroke="#142b1a" stroke-width="1.5"/>';
 svg+='<text x="'+(xLab+10)+'" y="'+(yLab-6)+'" fill="#63b3ed" font-size="8.5" font-weight="bold">BENCH TARGET: 20.00 °C (0.99820 g/mL)</text>';

 // Sidebar Explanations (Right Side)
 const sX=480,sY=50,sW=200,sH=220;
 svg+='<rect x="'+sX+'" y="'+sY+'" width="'+sW+'" height="'+sH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+22)+'" text-anchor="middle" fill="#81e6d9" font-size="10" font-weight="bold">STRUCTURAL ANOMALY</text>';
 svg+='<line x1="'+(sX+15)+'" y1="'+(sY+32)+'" x2="'+(sX+sW-15)+'" y2="'+(sY+32)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+50)+'" fill="#f6e05e" font-size="9" font-weight="bold">1. Hydrogen Bond Collapse</text>';
 svg+='<foreignObject x="'+(sX+12)+'" y="'+(sY+56)+'" width="'+(sW-24)+'" height="48"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#a0aec0;line-height:1.35;margin:0">Below 3.98 °C, melting collapses open tetrahedral Ice Ih cages into dense interstitial monomers, increasing ρ.</p></foreignObject>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+115)+'" fill="#68d391" font-size="9" font-weight="bold">2. Thermal Expansion</text>';
 svg+='<foreignObject x="'+(sX+12)+'" y="'+(sY+121)+'" width="'+(sW-24)+'" height="48"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#a0aec0;line-height:1.35;margin:0">Above 3.98 °C, kinetic thermal expansion overwhelms network collapse, causing monotonic density reduction.</p></foreignObject>';

 svg+='<rect x="'+(sX+12)+'" y="'+(sY+176)+'" width="'+(sW-24)+'" height="32" rx="3" fill="#061009" stroke="#1f3b28"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+190)+'" text-anchor="middle" fill="#9ae6b4" font-size="8">Thermal Coefficient β at 20 °C:</text>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+202)+'" text-anchor="middle" fill="#e2e8f0" font-size="9" font-family="monospace">2.07 × 10⁻⁴ K⁻¹</text>';

 svg+=text(360,305,'Tilton-Taylor Thermodynamic Formulation: Pure water density is an international primary measurement standard.','#789c80',9);
 return svg;
}

update();
renderResults();
