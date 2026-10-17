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
 if(cfg.slug==='hydrate-stoichiometric-composition'){
  $('liveState').textContent='Ready to calcine crucible containing '+p.input.toFixed(1)+' g hydrate.';
  message('Adjust initial hydrate mass, then calcine to constant mass.');
 }else if(cfg.slug==='limiting-reactant-precipitation'){
  $('liveState').textContent='Ready to deliver '+p.input.toFixed(1)+' mL of 0.1000 M Na₂SO₄ into excess BaCl₂.';
  message('Adjust sulfate volume V, then precipitate, digest, filter & weigh.');
 }else if(cfg.slug==='molar-volume-ideal-gas'){
  $('liveState').textContent='Ready to react '+p.input.toFixed(1)+' mg magnesium ribbon in eudiometer.';
  message('Set magnesium mass m_Mg, then react, equilibrate meniscus & convert to STP.');
 }else if(cfg.slug==='volatile-liquid-molar-mass'){
  $('liveState').textContent='Ready to vaporize liquid in calibrated '+p.input.toFixed(1)+' mL Dumas bulb.';
  message('Set Dumas bulb volume V_flask, then vaporize, flush air, condense & weigh.');
 }else if(cfg.slug==='chemical-reactions-copper-cycle'){
  $('liveState').textContent='Ready to cycle '+p.input.toFixed(2)+' g copper wire through 5 reactions.';
  message('Set initial copper mass m_initial, then run cyclic reactions, isolate, wash & dry.');
 }else if(cfg.slug==='empirical-formula-magnesium-oxide'){
  $('liveState').textContent='Ready to burn '+p.input.toFixed(2)+' g burnished magnesium ribbon in porcelain crucible.';
  message('Set initial magnesium mass m_Mg, then oxidize, digest nitride with steam, calcine & weigh.');
 }else if(cfg.slug==='liquid-viscosity-poiseuille'){
  $('liveState').textContent='Ready to establish '+p.input.toFixed(1)+' cm hydrostatic head across capillary.';
  message('Set hydrostatic head Δh, equilibrate at 20.0 °C, purge bubbles & record flow rate.');
 }else{
  $('liveState').textContent='Ready to dispense '+p.input.toFixed(cfg.inputDecimals)+' '+cfg.inputUnit+' of liquid.';
  message('Adjust '+cfg.shortInput+' V, then weigh the dispensed aliquot.');
 }
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
 let msgStart='Dispensing '+p.input.toFixed(cfg.inputDecimals)+' '+cfg.inputUnit+' into tared beaker…';
 if(cfg.slug==='hydrate-stoichiometric-composition') msgStart='Heating crucible at 250 °C and evolving steam…';
 if(cfg.slug==='limiting-reactant-precipitation') msgStart='Adding Na₂SO₄ dropwise at 85 °C, digesting, filtering through Gooch crucible, drying to constant mass…';
 if(cfg.slug==='molar-volume-ideal-gas') msgStart='Inverting eudiometer, diffusing 6 M HCl, evolving H₂ gas, leveling menisci…';
 if(cfg.slug==='volatile-liquid-molar-mass') msgStart='Immersing Dumas bulb at 100 °C, flushing air through pinhole, condensing & weighing…';
 if(cfg.slug==='chemical-reactions-copper-cycle') msgStart='Dissolving in HNO₃, precipitating Cu(OH)₂, dehydrating to CuO, dissolving in H₂SO₄, reducing with Zn, washing & desiccation…';
 if(cfg.slug==='empirical-formula-magnesium-oxide') msgStart='Igniting magnesium ribbon, throttling aerosol smoke, digesting nitride with hot water, calcining at 850 °C…';
 if(cfg.slug==='liquid-viscosity-poiseuille') msgStart='Equilibrating jacket at 20.0 °C, establishing constant overflow head, timing effluent discharge…';
 message(msgStart);
 await new Promise(resolve=>setTimeout(resolve,400));
 const raw=prediction.raw;
 measurement=model.reading(cfg.slug,p.input,raw);
 busy=false;$('independent').disabled=false;$('independentNumber').disabled=false;$('measure').disabled=false;$('recordReading').disabled=false;
 $('readingValue').textContent=raw.toFixed(cfg.rawDecimals)+' '+cfg.rawUnit;
 if(cfg.slug==='hydrate-stoichiometric-composition'){
  $('liveState').textContent='Crucible cooled in desiccator: '+raw.toFixed(4)+' g water evolved.';
  message('Calcination complete: evolved '+raw.toFixed(4)+' g H₂O from '+p.input.toFixed(1)+' g hydrate. Record in notebook.');
 }else if(cfg.slug==='limiting-reactant-precipitation'){
  $('liveState').textContent='Isolated dry BaSO₄ precipitate: '+raw.toFixed(4)+' g.';
  message('Gravimetric precipitation complete: isolated '+raw.toFixed(4)+' g BaSO₄ from '+p.input.toFixed(1)+' mL sulfate. Record in notebook.');
 }else if(cfg.slug==='molar-volume-ideal-gas'){
  $('liveState').textContent='Eudiometric gas volume at STP: '+raw.toFixed(3)+' mL H₂.';
  message('Reaction complete: generated '+raw.toFixed(3)+' mL H₂ at STP from '+p.input.toFixed(1)+' mg Mg. Record in notebook.');
 }else if(cfg.slug==='volatile-liquid-molar-mass'){
  $('liveState').textContent='Condensed vapor mass: '+raw.toFixed(4)+' g in '+p.input.toFixed(1)+' mL bulb.';
  message('Vapor density determination complete: condensed '+raw.toFixed(4)+' g vapor in '+p.input.toFixed(1)+' mL flask. Record in notebook.');
 }else if(cfg.slug==='chemical-reactions-copper-cycle'){
  $('liveState').textContent='Desiccated recovered metallic copper: '+raw.toFixed(4)+' g.';
  message('Copper cycle complete: recovered '+raw.toFixed(4)+' g pure Cu from '+p.input.toFixed(2)+' g wire (100.00% yield). Record in notebook.');
 }else if(cfg.slug==='empirical-formula-magnesium-oxide'){
  $('liveState').textContent='Calcined magnesium oxide: incorporated '+raw.toFixed(4)+' g bound oxygen.';
  message('Crucible thermal oxidation complete: incorporated '+raw.toFixed(4)+' g O into '+p.input.toFixed(2)+' g Mg (formula MgO). Record in notebook.');
 }else if(cfg.slug==='liquid-viscosity-poiseuille'){
  $('liveState').textContent='Volumetric capillary discharge: '+raw.toFixed(3)+' mL/min at Δh = '+p.input.toFixed(1)+' cm.';
  message('Poiseuille flow stabilized: discharge rate '+raw.toFixed(3)+' mL/min under '+p.input.toFixed(1)+' cm head (Re < 90, laminar). Record in notebook.');
 }else{
  $('liveState').textContent='Analytical balance stabilized: '+raw.toFixed(cfg.rawDecimals)+' g net mass.';
  message('Gravimetric measurement complete: '+raw.toFixed(cfg.rawDecimals)+' '+cfg.rawUnit+' for '+p.input.toFixed(cfg.inputDecimals)+' '+cfg.inputUnit+'. Record in notebook.');
 }
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
 if(cfg.slug==='hydrate-stoichiometric-composition'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawHydrateCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawHydrateSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawHydrateBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='limiting-reactant-precipitation'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawLimitingCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawLimitingSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawLimitingBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='molar-volume-ideal-gas'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawGasCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawGasSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawGasBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='volatile-liquid-molar-mass'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawDumasCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawDumasSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawDumasBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='chemical-reactions-copper-cycle'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawCopperCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawCopperSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawCopperBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='empirical-formula-magnesium-oxide'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawMgCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawMgSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawMgBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='liquid-viscosity-poiseuille'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawPoiseuilleCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawPoiseuilleSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawPoiseuilleBenchView(p,rawVal);
  return;
 }
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

function drawHydrateBenchView(p,rawVal){
 const m_hyd=p.input;
 const m_wat=measurement?measurement.raw:(busy?rawVal*0.8:rawVal);
 const m_salt=measurement?m_hyd-m_wat:(busy?m_hyd-m_wat:m_hyd*0.63924);
 const isDehydrated=Boolean(measurement);

 let svg='<defs><pattern id="chemGrid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" stroke="#ffffff" stroke-opacity=".03" fill="none"/></pattern>';
 svg+='<linearGradient id="flameInner" x1="0%" y1="100%" x2="0%" y2="0%"><stop offset="0%" stop-color="#93c5fd"/><stop offset="60%" stop-color="#60a5fa"/><stop offset="100%" stop-color="#3b82f6" stop-opacity=".2"/></linearGradient>';
 svg+='<linearGradient id="flameOuter" x1="0%" y1="100%" x2="0%" y2="0%"><stop offset="0%" stop-color="#2563eb" stop-opacity=".7"/><stop offset="100%" stop-color="#1d4ed8" stop-opacity="0"/></linearGradient>';
 svg+='<linearGradient id="crucibleGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#e2e8f0"/><stop offset="30%" stop-color="#ffffff"/><stop offset="80%" stop-color="#f1f5f9"/><stop offset="100%" stop-color="#cbd5e1"/></linearGradient>';
 svg+='<linearGradient id="blueCrystals" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0284c7"/><stop offset="50%" stop-color="#0369a1"/><stop offset="100%" stop-color="#075985"/></linearGradient>';
 svg+='<linearGradient id="whiteSalt" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#f8fafc"/><stop offset="50%" stop-color="#e2e8f0"/><stop offset="100%" stop-color="#cbd5e1"/></linearGradient>';
 svg+='</defs><rect width="720" height="320" fill="#0b140e"/><rect width="720" height="320" fill="url(#chemGrid)"/>';

 // Workbench surface
 svg+='<rect x="0" y="270" width="720" height="50" fill="#132419" stroke="#1f3b28" stroke-width="1"/>';
 svg+='<line x1="0" y1="270" x2="720" y2="270" stroke="#2d523b" stroke-width="2"/>';

 // 1. LEFT STATION: Tirrill Gas Burner & Porcelain Crucible on Ring Stand
 const rBaseX=40,rBaseY=258,rBaseW=120,rBaseH=12;
 svg+='<rect x="'+rBaseX+'" y="'+rBaseY+'" width="'+rBaseW+'" height="'+rBaseH+'" rx="2" fill="#1e293b" stroke="#334155"/>';
 svg+='<rect x="'+(rBaseX+20)+'" y="35" width="8" height="223" fill="#334155" stroke="#475569"/>';
 // Iron Ring
 const ringY=145;
 svg+='<rect x="'+(rBaseX+15)+'" y="'+ringY+'" width="85" height="7" rx="2" fill="#475569"/>';
 svg+='<ellipse cx="'+(rBaseX+85)+'" cy="'+(ringY+3)+'" rx="26" ry="7" fill="none" stroke="#64748b" stroke-width="3"/>';
 // Pipe Clay Triangle
 const cX=rBaseX+85;
 svg+='<polygon points="'+(cX-22)+','+(ringY+2)+' '+(cX+22)+','+(ringY+2)+' '+cX+','+(ringY-14)+'" fill="none" stroke="#e2e8f0" stroke-width="4"/>';

 // Tirrill Burner under Crucible
 const bX=cX-12,bY=205;
 svg+='<rect x="'+(bX-12)+'" y="260" width="48" height="10" rx="3" fill="#334155" stroke="#475569"/>'; // burner base
 svg+='<rect x="'+(bX+7)+'" y="215" width="10" height="45" fill="#64748b" stroke="#475569"/>'; // barrel
 svg+='<circle cx="'+(bX+12)+'" cy="250" r="4" fill="#94a3b8"/>'; // air collar
 // Gas flame
 svg+='<path d="M'+(bX+4)+' 215 Q'+(bX+12)+' '+(ringY+25)+' '+(bX+20)+' 215 Z" fill="url(#flameOuter)"/>';
 svg+='<path d="M'+(bX+7)+' 215 Q'+(bX+12)+' '+(ringY+38)+' '+(bX+17)+' 215 Z" fill="url(#flameInner)"/>';

 // Porcelain Crucible sitting in triangle
 const crucY=ringY-22;
 svg+='<path d="M'+(cX-18)+' '+crucY+' L'+(cX-12)+' '+(crucY+28)+' Q'+cX+' '+(crucY+34)+' '+(cX+12)+' '+(crucY+28)+' L'+(cX+18)+' '+crucY+' Z" fill="url(#crucibleGrad)" stroke="#94a3b8" stroke-width="1.2"/>';
 // Salt inside crucible
 const saltGrad=isDehydrated?'url(#whiteSalt)':'url(#blueCrystals)';
 svg+='<ellipse cx="'+cX+'" cy="'+(crucY+18)+'" rx="12" ry="4" fill="'+saltGrad+'"/>';

 // Crucible Lid (slightly ajar 3 mm to vent steam)
 const lidY=crucY-5;
 svg+='<path d="M'+(cX-20)+' '+(lidY+3)+' L'+(cX+18)+' '+(lidY-4)+' L'+(cX+19)+' '+(lidY-7)+' L'+(cX-19)+' '+(lidY)+' Z" fill="url(#crucibleGrad)" stroke="#94a3b8" stroke-width="1"/>';
 svg+='<circle cx="'+cX+'" cy="'+(lidY-3)+'" r="2.5" fill="#cbd5e1"/>'; // lid handle

 // Steam vapor wisps when busy heating
 if(busy){
  svg+='<path d="M'+(cX+14)+' '+(lidY-8)+' Q'+(cX+20)+' '+(lidY-25)+' '+(cX+10)+' '+(lidY-45)+' T'+(cX+18)+' '+(lidY-75)+'" fill="none" stroke="#e2e8f0" stroke-width="2" stroke-opacity=".6" stroke-dasharray="4,3"/>';
  svg+='<path d="M'+(cX+8)+' '+(lidY-10)+' Q'+(cX+4)+' '+(lidY-30)+' '+(cX+16)+' '+(lidY-55)+' T'+(cX+8)+' '+(lidY-85)+'" fill="none" stroke="#e2e8f0" stroke-width="1.5" stroke-opacity=".4" stroke-dasharray="3,3"/>';
 }
 svg+='<text x="'+cX+'" y="295" text-anchor="middle" fill="#94a3b8" font-size="9" font-weight="bold">CALCINATION (250 °C)</text>';

 // 2. MIDDLE STATION: Vacuum Desiccator
 const dX=250,dY=145,dW=130,dH=125;
 // Desiccator Base
 svg+='<path d="M'+dX+' '+(dY+dH)+' L'+(dX+10)+' '+(dY+dH-30)+' L'+(dX+dW-10)+' '+(dY+dH-30)+' L'+(dX+dW)+' '+(dY+dH)+' Z" fill="#1e293b" stroke="#334155" stroke-width="1.2"/>';
 // Cobalt-blue Drierite Crystals in bottom
 for(let bx=dX+20;bx<dX+dW-20;bx+=10){
  svg+='<circle cx="'+bx+'" cy="'+(dY+dH-12)+'" r="3.5" fill="#1d4ed8"/>';
  svg+='<circle cx="'+(bx+5)+'" cy="'+(dY+dH-7)+'" r="3" fill="#2563eb"/>';
 }
 // Perforated porcelain plate
 svg+='<rect x="'+(dX+10)+'" y="'+(dY+dH-34)+'" width="'+(dW-20)+'" height="5" fill="#e2e8f0" stroke="#94a3b8"/>';
 // Desiccator Glass Dome
 svg+='<path d="M'+(dX+8)+' '+(dY+dH-34)+' Q'+(dX+8)+' '+(dY+20)+' '+(dX+dW/2)+' '+(dY+10)+' Q'+(dX+dW-8)+' '+(dY+20)+' '+(dX+dW-8)+' '+(dY+dH-34)+' Z" fill="#ffffff" fill-opacity=".06" stroke="#475569" stroke-width="1.5"/>';
 // Stopcock valve on top
 svg+='<rect x="'+(dX+dW/2-4)+'" y="'+(dY-2)+'" width="8" height="12" fill="#94a3b8" stroke="#64748b"/>';
 svg+='<circle cx="'+(dX+dW/2)+'" cy="'+(dY-6)+'" r="4.5" fill="#3b82f6"/>';
 // Cooled crucible inside desiccator
 svg+='<path d="M'+(dX+dW/2-12)+' '+(dY+dH-34)+' L'+(dX+dW/2-8)+' '+(dY+dH-52)+' L'+(dX+dW/2+8)+' '+(dY+dH-52)+' L'+(dX+dW/2+12)+' '+(dY+dH-34)+' Z" fill="url(#crucibleGrad)" stroke="#94a3b8"/>';
 svg+='<text x="'+(dX+dW/2)+'" y="295" text-anchor="middle" fill="#60a5fa" font-size="9" font-weight="bold">DESICCATOR COOLING</text>';

 // 3. RIGHT STATION: Electronic Analytical Balance & Live Stoichiometric Telemetry
 const balX=420,balY=115,balW=270,balH=155;
 svg+='<rect x="'+balX+'" y="'+balY+'" width="'+balW+'" height="'+balH+'" rx="6" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<rect x="'+balX+'" y="'+balY+'" width="'+balW+'" height="26" rx="5" fill="#14331e"/>';
 svg+='<text x="'+(balX+balW/2)+'" y="'+(balY+17)+'" text-anchor="middle" fill="#86efac" font-size="10.5" font-weight="bold">ANALYTICAL GRAVIMETRIC TELEMETRY</text>';

 const rows_meta=[
  {lbl:'INITIAL HYDRATE MASS (m_hyd):',val:m_hyd.toFixed(4)+' g',col:'#60a5fa'},
  {lbl:'RECOVERED ANHYDROUS SALT (m_salt):',val:(isDehydrated?m_salt.toFixed(4):'—')+' g',col:'#f8fafc'},
  {lbl:'EVOLVED WATER OF CRYSTALLIZATION:',val:(isDehydrated?m_wat.toFixed(4):'—')+' g',col:'#4ade80'},
  {lbl:'ANHYDROUS MOLES n(CuSO₄):',val:(isDehydrated?(m_salt/159.609).toFixed(5):'—')+' mol',col:'#cbd5e1'},
  {lbl:'WATER MOLES n(H₂O):',val:(isDehydrated?(m_wat/18.0154).toFixed(5):'—')+' mol',col:'#cbd5e1'},
  {lbl:'EMPIRICAL HYDRATION RATIO x:',val:isDehydrated?((m_wat/18.0154)/(m_salt/159.609)).toFixed(4):'5.0000',col:'#fde047'}
 ];

 rows_meta.forEach((item,idx)=>{
  const ry=balY+38+idx*19;
  svg+='<text x="'+(balX+12)+'" y="'+ry+'" fill="#789c80" font-size="8">'+item.lbl+'</text>';
  svg+='<text x="'+(balX+balW-12)+'" y="'+ry+'" text-anchor="end" fill="'+item.col+'" font-size="9" font-family="monospace" font-weight="bold">'+item.val+'</text>';
 });

 svg+='<rect x="'+(balX+10)+'" y="'+(balY+balH-24)+'" width="'+(balW-20)+'" height="18" rx="3" fill="#061209" stroke="#1a3d24"/>';
 svg+='<text x="'+(balX+balW/2)+'" y="'+(balY+balH-12)+'" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="monospace">CuSO₄ · 5 H₂O ⟶ CuSO₄ (s) + 5 H₂O (g)</text>';

 svg+=text(360,22,'GRAVIMETRIC HYDRATE STOICHIOMETRY: THERMAL DESICCATION OF COPPER(II) SULFATE','#86efac',11.5);
 return svg;
}

function drawHydrateCompareView(p,rawVal){
 let svg='<rect width="720" height="320" fill="#0b140e"/>';
 const text=(x,y,str,color='#789c80',size=11)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';
 svg+=text(360,26,'WATER OF CRYSTALLIZATION DETERMINATION: THREE ANALYTICAL TECHNIQUES','#86efac',12);

 const methods=[
  {
   name:'1. Crucible Calcination',
   type:'Classical Thermal Gravimetry',
   prec:'±0.02 mol H₂O',
   sample:'2.0–5.0 g',
   dur:'45–60 min',
   adv:'Simple classical student bench method; requires repeated heating to constant mass to prevent moisture reabsorption.',
   col:'#38a169',
   score:75
  },
  {
   name:'2. Thermogravimetric (TGA)',
   type:'Continuous Microbalance Heating',
   prec:'±0.002 mol H₂O',
   sample:'10–20 mg',
   dur:'30 min',
   adv:'Resolves stepwise intermediate hydrates (trihydrate, monohydrate) via derivative DTG peaks under inert N₂ purge.',
   col:'#3b82f6',
   score:96
  },
  {
   name:'3. Karl Fischer Titration',
   type:'Coulometric Iodine Redox Reaction',
   prec:'±0.0005 mol H₂O',
   sample:'100 mg',
   dur:'5 min',
   adv:'Direct chemical reaction with H₂O: I₂ + SO₂ + CH₃OH + H₂O; operates at room temperature without risk of overheating.',
   col:'#eab308',
   score:98
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

  svg+='<text x="'+(cx+15)+'" y="'+(cy+92)+'" fill="#789c80" font-size="8.5">SAMPLE REQUIREMENT:</text>';
  svg+='<text x="'+(cx+cw-15)+'" y="'+(cy+92)+'" text-anchor="end" fill="#e2e8f0" font-size="9" font-family="monospace">'+m.sample+'</text>';

  svg+='<text x="'+(cx+15)+'" y="'+(cy+114)+'" fill="#789c80" font-size="8.5">TOTAL RUN DURATION:</text>';
  svg+='<text x="'+(cx+cw-15)+'" y="'+(cy+114)+'" text-anchor="end" fill="#e2e8f0" font-size="9" font-family="monospace">'+m.dur+'</text>';

  svg+='<line x1="'+(cx+12)+'" y1="'+(cy+126)+'" x2="'+(cx+cw-12)+'" y2="'+(cy+126)+'" stroke="#1f3b28"/>';
  svg+='<text x="'+(cx+15)+'" y="'+(cy+144)+'" fill="#789c80" font-size="8">ANALYTICAL RESOLUTION SCORE</text>';
  svg+='<rect x="'+(cx+15)+'" y="'+(cy+152)+'" width="'+(cw-30)+'" height="8" rx="2" fill="#08140c"/>';
  svg+='<rect x="'+(cx+15)+'" y="'+(cy+152)+'" width="'+((cw-30)*m.score/100)+'" height="8" rx="2" fill="'+m.col+'"/>';

  svg+='<foreignObject x="'+(cx+12)+'" y="'+(cy+170)+'" width="'+(cw-24)+'" height="68"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:8.5px;color:#a0aec0;line-height:1.4;margin:0">'+m.adv+'</p></foreignObject>';
 });

 svg+=text(360,306,'Safety Rule: Never exceed 600 °C during calcination to prevent decomposition of CuSO₄ into black CuO and SO₃ gas.','#86efac',9.5);
 return svg;
}

function drawHydrateSandboxView(p,rawVal){
 let svg='<rect width="720" height="320" fill="#0b140e"/>';
 const text=(x,y,str,color='#789c80',size=11)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';
 svg+=text(360,24,'THERMOGRAVIMETRIC (TGA) STEPWISE DEHYDRATION PROFILE: CuSO₄ · 5 H₂O','#86efac',12);

 // TGA Curve Plot (X: Temp 0 to 750 C; Y: Mass % remaining 100% to 20%)
 const pX=60,pY=50,pW=400,pH=220;
 svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" fill="#061009" stroke="#1f3b28" rx="4"/>';
 const mapX=t=>pX+(t/750)*pW;
 const mapY=pct=>pY+pH-((pct-20)/85)*pH;

 // TGA step curve coordinates
 const tgaSteps=[
  [25,100],[60,100],[95,85.6],[105,85.6],[130,71.2],[200,71.2],[245,63.9],[600,63.9],[680,31.8],[750,31.8]
 ];
 const pts=tgaSteps.map(pair=>mapX(pair[0]).toFixed(1)+','+mapY(pair[1]).toFixed(1));
 svg+='<polyline points="'+pts.join(' ')+'" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';

 // Grid labels
 [100,200,300,400,500,600,700].forEach(deg=>{
  svg+='<line x1="'+mapX(deg)+'" y1="'+pY+'" x2="'+mapX(deg)+'" y2="'+(pY+pH)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+mapX(deg)+'" y="'+(pY+pH+14)+'" text-anchor="middle" fill="#789c80" font-size="8.5">'+deg+' °C</text>';
 });
 [40,60,80,100].forEach(pct=>{
  svg+='<line x1="'+pX+'" y1="'+mapY(pct)+'" x2="'+(pX+pW)+'" y2="'+mapY(pct)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+(pX-6)+'" y="'+(mapY(pct)+3)+'" text-anchor="end" fill="#789c80" font-size="8.5">'+pct+'%</text>';
 });

 // Labels on Plateaus
 svg+='<text x="'+(mapX(75))+'" y="'+(mapY(85.6)-6)+'" text-anchor="middle" fill="#fde047" font-size="7.5">−2 H₂O (Trihydrate)</text>';
 svg+='<text x="'+(mapX(160))+'" y="'+(mapY(71.2)-6)+'" text-anchor="middle" fill="#fde047" font-size="7.5">−2 H₂O (Monohydrate)</text>';
 svg+='<text x="'+(mapX(400))+'" y="'+(mapY(63.9)-7)+'" text-anchor="middle" fill="#86efac" font-size="8.5" font-weight="bold">ANHYDROUS CuSO₄ (63.9%)</text>';
 svg+='<text x="'+(mapX(700))+'" y="'+(mapY(31.8)-6)+'" text-anchor="middle" fill="#ef4444" font-size="7.5">CuO residue (31.8%)</text>';

 // Right Sidebar: Crystal Field & Structural Coordination
 const sX=480,sY=50,sW=200,sH=220;
 svg+='<rect x="'+sX+'" y="'+sY+'" width="'+sW+'" height="'+sH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+20)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">COORDINATION SPHERE</text>';
 svg+='<line x1="'+(sX+15)+'" y1="'+(sY+28)+'" x2="'+(sX+sW-15)+'" y2="'+(sY+28)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+46)+'" fill="#60a5fa" font-size="9" font-weight="bold">Equatorial Ligands (4 H₂O)</text>';
 svg+='<foreignObject x="'+(sX+12)+'" y="'+(sY+50)+'" width="'+(sW-24)+'" height="45"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#a0aec0;line-height:1.35;margin:0">4 water molecules coordinate equatorially to Cu²⁺ with short bonds (1.97 Å); split d-orbitals produce azure blue color.</p></foreignObject>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+108)+'" fill="#fde047" font-size="9" font-weight="bold">Bridging Water (5th H₂O)</text>';
 svg+='<foreignObject x="'+(sX+12)+'" y="'+(sY+112)+'" width="'+(sW-24)+'" height="45"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#a0aec0;line-height:1.35;margin:0">Held by 4 hydrogen bonds between sulfate anions and coordinated waters; released only above 200 °C.</p></foreignObject>';

 svg+='<rect x="'+(sX+12)+'" y="'+(sY+170)+'" width="'+(sW-24)+'" height="38" rx="3" fill="#061209" stroke="#1f3b28"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+185)+'" text-anchor="middle" fill="#86efac" font-size="8">Hydration Exothermicity:</text>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+198)+'" text-anchor="middle" fill="#f8fafc" font-size="8.5" font-family="monospace">ΔH_hyd = −78.2 kJ/mol</text>';

 svg+=text(360,305,'TGA Thermogravimetry: Stepwise mass plateaus isolate discrete stoichiometric intermediate hydrate phases.','#789c80',9);
 return svg;
}

update();
renderResults();

// ======================================================================
// CHEMISTRY LAB 03: LIMITING REACTANTS & GRAVIMETRIC PRECIPITATION
// ======================================================================
function drawLimitingBenchView(p,rawVal){
 const v=p.input;
 const m_ppt=rawVal;
 let svg='<defs>';
 svg+='<linearGradient id="flaskGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ffffff" stop-opacity=".15"/><stop offset="30%" stop-color="#ffffff" stop-opacity=".05"/><stop offset="80%" stop-color="#38bdf8" stop-opacity=".08"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".2"/></linearGradient>';
 svg+='<linearGradient id="buretteGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#bae6fd" stop-opacity=".3"/><stop offset="50%" stop-color="#e0f2fe" stop-opacity=".1"/><stop offset="100%" stop-color="#bae6fd" stop-opacity=".35"/></linearGradient>';
 svg+='<linearGradient id="pptCake" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#f8fafc"/><stop offset="50%" stop-color="#e2e8f0"/><stop offset="100%" stop-color="#cbd5e1"/></linearGradient>';
 svg+='<linearGradient id="heatPlate" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#334155"/><stop offset="100%" stop-color="#0f172a"/></linearGradient>';
 svg+='<filter id="glow"><feGaussianBlur stdDeviation="2" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';
 svg+='</defs>';

 // Background bench layout
 svg+='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+='<line x1="20" y1="280" x2="700" y2="280" stroke="#1f3b28" stroke-width="2"/>';

 // Header banner
 svg+=text(360,20,'GRAVIMETRIC PRECIPITATION & VACUUM FILTRATION: Ba²⁺(aq) + SO₄²⁻(aq) ⟶ BaSO₄(s)↓','#86efac',11);

 // 1. LEFT STATION: Precision Burette & Heated Digestion Reaction
 const bX=110,bY=32;
 svg+='<rect x="'+(bX-45)+'" y="30" width="5" height="250" fill="#64748b"/>';
 svg+='<rect x="'+(bX-65)+'" y="276" width="45" height="6" rx="2" fill="#475569"/>';
 svg+='<rect x="'+(bX-45)+'" y="80" width="40" height="6" fill="#94a3b8"/>';
 svg+='<circle cx="'+(bX-5)+'" cy="83" r="5" fill="#cbd5e1"/>';

 // Glass Burette
 svg+='<rect x="'+(bX-7)+'" y="'+bY+'" width="14" height="130" fill="url(#buretteGrad)" stroke="#7dd3fc" stroke-width="1.2"/>';
 const menY=bY+15+(v/24.0)*85;
 svg+='<rect x="'+(bX-6)+'" y="'+menY+'" width="12" height="'+(bY+130-menY)+'" fill="#0284c7" fill-opacity=".35"/>';
 svg+='<path d="M'+(bX-6)+' '+menY+' Q'+bX+' '+(menY+3)+' '+(bX+6)+' '+menY+'" fill="none" stroke="#38bdf8" stroke-width="1.2"/>';
 for(let gy=bY+15;gy<=bY+120;gy+=10){
  svg+='<line x1="'+(bX+1)+'" y1="'+gy+'" x2="'+(bX+6)+'" y2="'+gy+'" stroke="#bae6fd" stroke-width="0.8"/>';
 }
 svg+='<polygon points="'+(bX-7)+','+(bY+130)+' '+(bX+7)+','+(bY+130)+' '+(bX+3)+','+(bY+144)+' '+(bX-3)+','+(bY+144)+'" fill="#cbd5e1"/>';
 svg+='<rect x="'+(bX-8)+'" y="'+(bY+134)+'" width="16" height="5" rx="1.5" fill="#ef4444"/>';
 svg+='<line x1="'+bX+'" y1="'+(bY+144)+'" x2="'+bX+'" y2="'+(bY+154)+'" stroke="#7dd3fc" stroke-width="1.5"/>';

 if(busy){
  svg+='<circle cx="'+bX+'" cy="'+(bY+162)+'" r="2" fill="#38bdf8" filter="url(#glow)"/>';
  svg+='<circle cx="'+bX+'" cy="'+(bY+172)+'" r="1.5" fill="#38bdf8"/>';
 }

 // Hotplate Magnetic Stirrer
 const hpX=bX-50,hpY=240,hpW=100,hpH=38;
 svg+='<rect x="'+hpX+'" y="'+hpY+'" width="'+hpW+'" height="'+hpH+'" rx="4" fill="url(#heatPlate)" stroke="#475569" stroke-width="1.2"/>';
 svg+='<rect x="'+(hpX+6)+'" y="'+(hpY+8)+'" width="36" height="20" rx="2" fill="#020617" stroke="#1e293b"/>';
 svg+='<text x="'+(hpX+24)+'" y="'+(hpY+22)+'" text-anchor="middle" fill="#ef4444" font-size="8" font-family="monospace">85.0°C</text>';
 svg+='<circle cx="'+(hpX+60)+'" cy="'+(hpY+18)+'" r="7" fill="#64748b"/>';
 svg+='<text x="'+(hpX+80)+'" y="'+(hpY+22)+'" text-anchor="middle" fill="#86efac" font-size="7">300 rpm</text>';

 // Reaction Beaker
 const bkX=bX-35,bkY=175,bkW=70,bkH=65;
 svg+='<rect x="'+bkX+'" y="'+bkY+'" width="'+bkW+'" height="'+bkH+'" rx="2" fill="url(#flaskGrad)" stroke="#94a3b8" stroke-width="1.2"/>';
 const liqH=42;
 svg+='<rect x="'+(bkX+1)+'" y="'+(bkY+bkH-liqH)+'" width="'+(bkW-2)+'" height="'+liqH+'" fill="#0284c7" fill-opacity=".15"/>';
 for(let i=0;i<18;i++){
  const px=bkX+8+(i*13)%(bkW-16);
  const py=bkY+bkH-8-((i*17)%(liqH-12));
  svg+='<circle cx="'+px+'" cy="'+py+'" r="1.8" fill="#f8fafc" fill-opacity=".85"/>';
 }
 svg+='<rect x="'+(bX-10)+'" y="'+(bkY+bkH-7)+'" width="20" height="5" rx="2.5" fill="#f1f5f9" stroke="#94a3b8"/>';
 svg+='<text x="'+bX+'" y="295" text-anchor="middle" fill="#94a3b8" font-size="9" font-weight="bold">1. DIGESTION BEAKER (85 °C)</text>';

 // 2. MIDDLE STATION: Vacuum Buchner / Gooch Filtration Manifold
 const fX=330,fY=150;
 svg+='<path d="M'+(fX-14)+' '+(fY+24)+' L'+(fX-12)+' '+(fY+45)+' L'+(fX-42)+' '+(fY+120)+' Q'+fX+' '+(fY+126)+' '+(fX+42)+' '+(fY+120)+' L'+(fX+12)+' '+(fY+45)+' L'+(fX+14)+' '+(fY+24)+' Z" fill="url(#flaskGrad)" stroke="#64748b" stroke-width="1.2"/>';
 svg+='<line x1="'+(fX+12)+'" y1="'+(fY+42)+'" x2="'+(fX+28)+'" y2="'+(fY+38)+'" stroke="#64748b" stroke-width="4"/>';
 svg+='<path d="M'+(fX+28)+' '+(fY+38)+' Q'+(fX+50)+' '+(fY+32)+' '+(fX+65)+' '+(fY+70)+'" fill="none" stroke="#d97706" stroke-width="3.5" stroke-linecap="round"/>';
 svg+='<text x="'+(fX+75)+'" y="'+(fY+65)+'" fill="#fbbf24" font-size="7.5">VACUUM (−20 kPa)</text>';

 svg+='<polygon points="'+(fX-15)+','+(fY+22)+' '+(fX+15)+','+(fY+22)+' '+(fX+12)+','+(fY+32)+' '+(fX-12)+','+(fY+32)+'" fill="#020617" stroke="#334155"/>';

 const crX=fX-18,crY=fY-14,crW=36,crH=36;
 svg+='<path d="M'+crX+' '+crY+' L'+(crX+4)+' '+(crY+crH)+' L'+(crX+crW-4)+' '+(crY+crH)+' L'+(crX+crW)+' '+crY+' Z" fill="#1e293b" stroke="#94a3b8" stroke-width="1.2"/>';
 svg+='<line x1="'+(crX+5)+'" y1="'+(crY+crH-8)+'" x2="'+(crX+crW-5)+'" y2="'+(crY+crH-8)+'" stroke="#64748b" stroke-dasharray="2,1.5" stroke-width="2"/>';
 const cakeH=3+(v/24.0)*8;
 svg+='<rect x="'+(crX+6)+'" y="'+(crY+crH-8-cakeH)+'" width="'+(crW-12)+'" height="'+cakeH+'" fill="url(#pptCake)" rx="1.5"/>';
 svg+='<rect x="'+(fX-3.5)+'" y="'+(crY+crH)+'" width="7" height="35" fill="url(#buretteGrad)" stroke="#7dd3fc" stroke-width="0.8"/>';

 svg+='<path d="M'+(fX-34)+' '+(fY+105)+' Q'+fX+' '+(fY+110)+' '+(fX+34)+' '+(fY+105)+' L'+(fX+40)+' '+(fY+118)+' Q'+fX+' '+(fY+125)+' '+(fX-40)+' '+(fY+118)+' Z" fill="#38bdf8" fill-opacity=".25"/>';

 const ttX=fX+75,ttY=fY+110;
 svg+='<rect x="'+ttX+'" y="'+ttY+'" width="14" height="45" rx="7" fill="url(#flaskGrad)" stroke="#94a3b8"/>';
 svg+='<rect x="'+(ttX+1.5)+'" y="'+(ttY+18)+'" width="11" height="24" rx="5" fill="#38bdf8" fill-opacity=".2"/>';
 svg+='<text x="'+(ttX+7)+'" y="'+(ttY+32)+'" text-anchor="middle" fill="#4ade80" font-size="6.5" font-weight="bold">AgNO₃ ✓</text>';
 svg+='<text x="'+(ttX+7)+'" y="'+(ttY+62)+'" text-anchor="middle" fill="#86efac" font-size="7">0.0 ppm Cl⁻</text>';

 svg+='<text x="'+fX+'" y="295" text-anchor="middle" fill="#60a5fa" font-size="9" font-weight="bold">2. GOOCH VACUUM FILTRATION</text>';

 // 3. RIGHT STATION: 4-Decimal Analytical Balance
 const abX=540,abY=120,abW=145,abH=150;
 svg+='<rect x="'+abX+'" y="'+abY+'" width="'+abW+'" height="'+abH+'" rx="4" fill="#0f172a" fill-opacity=".7" stroke="#334155" stroke-width="1.5"/>';
 svg+='<rect x="'+(abX+5)+'" y="'+(abY+5)+'" width="'+(abW-10)+'" height="85" fill="#ffffff" fill-opacity=".04" stroke="#475569" stroke-width="1"/>';
 const panX=abX+abW/2;
 svg+='<rect x="'+(panX-25)+'" y="'+(abY+70)+'" width="50" height="4" fill="#e2e8f0" stroke="#94a3b8"/>';
 svg+='<rect x="'+(panX-3)+'" y="'+(abY+74)+'" width="6" height="16" fill="#64748b"/>';

 const cbX=panX-14,cbY=abY+45;
 svg+='<path d="M'+cbX+' '+cbY+' L'+(cbX+3)+' '+(cbY+25)+' L'+(cbX+25)+' '+(cbY+25)+' L'+(cbX+28)+' '+cbY+' Z" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>';
 svg+='<rect x="'+(cbX+5)+' " y="'+(cbY+16)+'" width="18" height="7" fill="url(#pptCake)" rx="1"/>';

 const conY=abY+95;
 svg+='<rect x="'+(abX+10)+'" y="'+conY+'" width="'+(abW-20)+'" height="'+(abH-105)+'" rx="3" fill="#020617" stroke="#1e293b"/>';
 svg+='<rect x="'+(abX+16)+'" y="'+(conY+6)+'" width="'+(abW-32)+'" height="24" rx="2" fill="#061c10" stroke="#14532d"/>';
 const dispText=m_ppt>0?m_ppt.toFixed(4)+' g':'0.0000 g';
 svg+='<text x="'+(abX+abW-22)+'" y="'+(conY+23)+'" text-anchor="end" fill="#4ade80" font-size="12" font-family="monospace" font-weight="bold">'+dispText+'</text>';
 svg+='<text x="'+(abX+20)+'" y="'+(conY+14)+'" fill="#15803d" font-size="6">TARE NET</text>';

 svg+='<text x="'+(abX+20)+'" y="'+(conY+38)+'" fill="#94a3b8" font-size="7">Product: BaSO₄ (dry)</text>';
 svg+='<text x="'+(abX+abW-20)+'" y="'+(conY+38)+'" text-anchor="end" fill="#86efac" font-size="7">Yield: 100.0%</text>';

 svg+='<text x="'+panX+'" y="295" text-anchor="middle" fill="#4ade80" font-size="9" font-weight="bold">3. ANALYTICAL BALANCE (±0.1 mg)</text>';

 svg+=text(360,312,'Quantitative Metathesis: Limiting SO₄²⁻ governs isolated dry BaSO₄ mass. All excess Ba²⁺ remains dissolved.','#789c80',8.5);
 return svg;
}

function drawLimitingCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'ANALYTICAL METROLOGY COMPARISON: QUANTITATIVE SULFATE DETERMINATION','#86efac',12);

 const cards=[
  {
   title:'1. Gravimetric Precipitation',
   sub:'Classical Absolute Primary Method',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Principle: Ba²⁺ + SO₄²⁻ ⟶ BaSO₄(s)↓',
    'Mass isolated via sintered glass Gooch crucible',
    'Primary method: No calibration standards needed',
    'Analytical Precision: ±0.0001 g (±0.1 mg)',
    'Dynamic Range: 10 mg to 5.0 g sulfate',
    'Analysis Time: 90–120 minutes (digestion/drying)',
    'Systematic Biases: Coprecipitation, slight K_sp loss'
   ]
  },
  {
   title:'2. Turbidimetric Titration',
   sub:'Optical Rayleigh-Gans Scattering',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Principle: 90° light scattering by micro-crystallites',
    'Optical scatter intensity: I_scatter ∝ [SO₄²⁻]',
    'Secondary method: Requires matrix-matched calibration',
    'Analytical Precision: ±1.5% to ±3.0% RSD',
    'Dynamic Range: 1.0 mg/L to 40 mg/L (ppm)',
    'Analysis Time: 1 to 3 minutes per sample',
    'Systematic Biases: Particle ripening, stirring speed'
   ]
  },
  {
   title:'3. ICP-OES Emission',
   sub:'Inductively Coupled Argon Plasma',
   color:'#fde047',
   border:'#5a4814',
   items:[
    'Principle: Atomic emission lines (S: 180.7 nm, Ba: 455.4 nm)',
    'Thermal atomization & ionization at 7000–8000 K',
    'Instrumental method: Multi-element calibration curve',
    'Analytical Precision: ±0.5% to ±1.0% RSD',
    'Dynamic Range: 5 μg/L to 100 mg/L (ppb to ppm)',
    'Analysis Time: 30 seconds per injection',
    'Systematic Biases: Plasma drift, spectral interferences'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Classical gravimetry provides absolute primary SI traceability without calibration curve drift.','#789c80',9);
 return svg;
}

function drawLimitingSandboxView(p,rawVal){
 const v=p.input;
 const m_ppt=rawVal;
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'STOICHIOMETRIC RESPONSE & EQUIVALENCE PLATEAU: Ba²⁺ + SO₄²⁻ ⟶ BaSO₄↓','#86efac',12);

 // Left Plot: Precipitate mass vs added Na2SO4 volume (0 to 40 mL)
 const pX=55,pY=48,pW=420,pH=225;
 svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" fill="#061209" stroke="#1f3b28" rx="4"/>';

 const mapX=vol=>pX+(vol/40.0)*pW;
 const mapY=mass=>pY+pH-(mass/0.85)*pH;

 // Draw Equivalence zone line at V = 30.0 mL (3.00 mmol)
 const eqX=mapX(30.0);
 svg+='<line x1="'+eqX+'" y1="'+pY+'" x2="'+eqX+'" y2="'+(pY+pH)+'" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,3"/>';
 svg+='<text x="'+eqX+'" y="'+(pY+15)+'" text-anchor="middle" fill="#ef4444" font-size="8" font-weight="bold">EQUIVALENCE POINT (V = 30.0 mL)</text>';

 // Linear stoichiometric line (0 to 30 mL) and plateau line (30 to 40 mL)
 const p0=[mapX(0),mapY(0)];
 const pEq=[mapX(30.0),mapY(0.7002)];
 const pEnd=[mapX(40.0),mapY(0.7002)];
 svg+='<polyline points="'+p0[0]+','+p0[1]+' '+pEq[0]+','+pEq[1]+' '+pEnd[0]+','+pEnd[1]+'" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';

 // Grid lines & labels
 [10,20,30,40].forEach(vol=>{
  svg+='<line x1="'+mapX(vol)+'" y1="'+pY+'" x2="'+mapX(vol)+'" y2="'+(pY+pH)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+mapX(vol)+'" y="'+(pY+pH+14)+'" text-anchor="middle" fill="#789c80" font-size="8.5">'+vol+' mL</text>';
 });
 [0.2,0.4,0.6,0.8].forEach(mass=>{
  svg+='<line x1="'+pX+'" y1="'+mapY(mass)+'" x2="'+(pX+pW)+'" y2="'+mapY(mass)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+(pX-6)+'" y="'+(mapY(mass)+3)+'" text-anchor="end" fill="#789c80" font-size="8.5">'+mass.toFixed(1)+' g</text>';
 });

 // Shaded regimes
 svg+='<text x="'+(pX+110)+'" y="'+(pY+pH-40)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">SULFATE LIMITING (Linear)</text>';
 svg+='<text x="'+(pX+110)+'" y="'+(pY+pH-28)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">m = 0.02334 · V_SO₄</text>';
 svg+='<text x="'+(eqX+45)+'" y="'+(mapY(0.7002)-10)+'" text-anchor="middle" fill="#fde047" font-size="8.5" font-weight="bold">BARIUM LIMITING (Plateau)</text>';
 svg+='<text x="'+(eqX+45)+'" y="'+(mapY(0.7002)+14)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">m_max = 0.7002 g</text>';

 // Active current operating point
 const curX=mapX(v);
 const curY=mapY(m_ppt);
 svg+='<circle cx="'+curX+'" cy="'+curY+'" r="6" fill="#4ade80" stroke="#08140c" stroke-width="2"/>';
 svg+='<circle cx="'+curX+'" cy="'+curY+'" r="9" fill="none" stroke="#4ade80" stroke-width="1.2" stroke-opacity=".6"/>';
 svg+='<line x1="'+curX+'" y1="'+curY+'" x2="'+curX+'" y2="'+(pY+pH)+'" stroke="#4ade80" stroke-dasharray="2,2"/>';

 // Right Sidebar: Stoichiometric Balance & Baryte Crystallography
 const sX=490,sY=48,sW=205,sH=225;
 svg+='<rect x="'+sX+'" y="'+sY+'" width="'+sW+'" height="'+sH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">STOICHIOMETRIC STATUS</text>';
 svg+='<line x1="'+(sX+15)+'" y1="'+(sY+25)+'" x2="'+(sX+sW-15)+'" y2="'+(sY+25)+'" stroke="#1f3b28"/>';

 const n_SO4=(0.1000*v);
 const n_Ba_init=3.000;
 const n_Ba_rem=Math.max(0,n_Ba_init-n_SO4);
 svg+='<text x="'+(sX+12)+'" y="'+(sY+42)+'" fill="#94a3b8" font-size="8">Initial Ba²⁺ Aliquot: 3.000 mmol</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+57)+'" fill="#38bdf8" font-size="8">Delivered SO₄²⁻: '+n_SO4.toFixed(3)+' mmol</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+72)+'" fill="#fde047" font-size="8">Excess Ba²⁺ in soln: '+n_Ba_rem.toFixed(3)+' mmol</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+87)+'" fill="#4ade80" font-size="8">Precipitated BaSO₄: '+n_SO4.toFixed(3)+' mmol</text>';

 svg+='<rect x="'+(sX+10)+'" y="'+(sY+98)+'" width="'+(sW-20)+'" height="32" rx="3" fill="#061209" stroke="#1f3b28"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+112)+'" text-anchor="middle" fill="#86efac" font-size="7.5">Limiting Reagent Condition:</text>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+124)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-family="monospace">SO₄²⁻ IS LIMITING (100% Yield)</text>';

 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+148)+'" text-anchor="middle" fill="#86efac" font-size="9" font-weight="bold">BARYTE LATTICE (Pnma)</text>';
 svg+='<foreignObject x="'+(sX+10)+'" y="'+(sY+154)+'" width="'+(sW-20)+'" height="60"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7px;color:#a0aec0;line-height:1.3;margin:0">BaSO₄ crystallizes in the orthorhombic baryte structure where each Ba²⁺ cation is coordinated by 12 oxygen atoms from neighboring tetrahedral SO₄²⁻ anions, providing immense thermodynamic lattice enthalpy (ΔH_lat = −2469 kJ/mol) and insoluble stability.</p></foreignObject>';

 svg+=text(360,305,'Sandbox: Beyond 30.0 mL, Ba²⁺ becomes limiting and precipitate mass plateaus at 0.7002 g.','#789c80',9);
 return svg;
}

// ======================================================================
// CHEMISTRY LAB 04: MOLAR VOLUME OF AN IDEAL GAS (EUDIOMETRY)
// ======================================================================
function drawGasBenchView(p,rawVal){
 const m_mg=p.input;
 const v_stp=rawVal;
 // Raw experimental volume at 20 C and P_H2 = 742.46 mmHg
 const v_exp=(v_stp * (760.0 / 742.46) * (293.15 / 273.15));

 let svg='<defs>';
 svg+='<linearGradient id="eudioGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#bae6fd" stop-opacity=".35"/><stop offset="30%" stop-color="#ffffff" stop-opacity=".1"/><stop offset="70%" stop-color="#38bdf8" stop-opacity=".15"/><stop offset="100%" stop-color="#bae6fd" stop-opacity=".4"/></linearGradient>';
 svg+='<linearGradient id="waterCyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#0284c7" stop-opacity=".25"/><stop offset="50%" stop-color="#38bdf8" stop-opacity=".12"/><stop offset="100%" stop-color="#0284c7" stop-opacity=".3"/></linearGradient>';
 svg+='<linearGradient id="gasZone" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#f8fafc" stop-opacity=".25"/><stop offset="100%" stop-color="#38bdf8" stop-opacity=".08"/></linearGradient>';
 svg+='<linearGradient id="copperCage" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#f59e0b"/><stop offset="50%" stop-color="#b45309"/><stop offset="100%" stop-color="#78350f"/></linearGradient>';
 svg+='</defs>';

 // Background bench layout
 svg+='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+='<line x1="20" y1="280" x2="700" y2="280" stroke="#1f3b28" stroke-width="2"/>';

 // Header banner
 svg+=text(360,20,'EUDIOMETRIC GAS DISPLACEMENT: Mg(s) + 2 HCl(aq) ⟶ MgCl₂(aq) + H₂(g)↑','#86efac',11);

 // -------------------------------------------------------------
 // 1. LEFT STATION: Microbalance & Magnesium Ribbon Preparation
 // -------------------------------------------------------------
 const mbX=40,mbY=135,mbW=140,mbH=140;
 svg+='<rect x="'+mbX+'" y="'+mbY+'" width="'+mbW+'" height="'+mbH+'" rx="4" fill="#0f172a" fill-opacity=".7" stroke="#334155" stroke-width="1.2"/>';
 svg+='<rect x="'+(mbX+5)+'" y="'+(mbY+5)+'" width="'+(mbW-10)+'" height="75" fill="#ffffff" fill-opacity=".04" stroke="#475569" stroke-width="1"/>';

 // Weighing pan & boat
 const panX=mbX+mbW/2;
 svg+='<rect x="'+(panX-22)+'" y="'+(mbY+62)+'" width="44" height="3.5" fill="#e2e8f0" stroke="#94a3b8"/>';
 svg+='<rect x="'+(panX-2.5)+'" y="'+(mbY+65)+'" width="5" height="15" fill="#64748b"/>';
 // Polished Magnesium Ribbon in Copper Cage
 svg+='<path d="M'+(panX-12)+' '+(mbY+52)+' Q'+(panX-6)+' '+(mbY+44)+' '+panX+' '+(mbY+52)+' Q'+(panX+6)+' '+(mbY+60)+' '+(panX+12)+' '+(mbY+52)+'" fill="none" stroke="#f59e0b" stroke-width="2"/>';
 svg+='<rect x="'+(panX-6)+'" y="'+(mbY+48)+'" width="12" height="6" rx="1.5" fill="#e2e8f0" stroke="#94a3b8"/>'; // Mg strip

 // Balance console
 const cY=mbY+86;
 svg+='<rect x="'+(mbX+8)+'" y="'+cY+'" width="'+(mbW-16)+'" height="46" rx="3" fill="#020617" stroke="#1e293b"/>';
 svg+='<rect x="'+(mbX+14)+'" y="'+(cY+6)+'" width="'+(mbW-28)+'" height="20" rx="2" fill="#061c10" stroke="#14532d"/>';
 svg+='<text x="'+(mbX+mbW-18)+'" y="'+(cY+20)+'" text-anchor="end" fill="#4ade80" font-size="11" font-family="monospace" font-weight="bold">'+(m_mg/1000.0).toFixed(5)+' g</text>';
 svg+='<text x="'+(mbX+18)+'" y="'+(cY+13)+'" fill="#15803d" font-size="6">Mg TARE</text>';
 svg+='<text x="'+panX+'" y="'+(cY+38)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">m_Mg = '+m_mg.toFixed(1)+' mg</text>';

 svg+='<text x="'+panX+'" y="295" text-anchor="middle" fill="#94a3b8" font-size="9" font-weight="bold">1. MICROBALANCE (±0.01 mg)</text>';

 // -------------------------------------------------------------
 // 2. CENTER STATION: Tall-Form Leveling Cylinder & Eudiometer
 // -------------------------------------------------------------
 const eX=340,eY=35;
 // Tall-Form Water Leveling Cylinder (1000 mL)
 const cylX=eX-60,cylY=70,cylW=120,cylH=205;
 svg+='<rect x="'+cylX+'" y="'+cylY+'" width="'+cylW+'" height="'+cylH+'" rx="4" fill="url(#waterCyl)" stroke="#38bdf8" stroke-width="1.5"/>';
 svg+='<rect x="'+(cylX-8)+'" y="'+(cylY+cylH-6)+'" width="'+(cylW+16)+'" height="10" rx="3" fill="#1e293b" stroke="#475569"/>'; // base
 // Water in leveling jar
 const waterLevelY=cylY+45;
 svg+='<rect x="'+(cylX+2)+'" y="'+waterLevelY+'" width="'+(cylW-4)+'" height="'+(cylH-47)+'" fill="#0284c7" fill-opacity=".2"/>';
 svg+='<line x1="'+cylX+'" y1="'+waterLevelY+'" x2="'+(cylX+cylW)+'" y2="'+waterLevelY+'" stroke="#38bdf8" stroke-width="1.5"/>';

 // Eudiometer Tube (Inverted 50 mL burette)
 const eudW=26,eudH=220;
 const eudTop=eY+10;
 // Outer glass wall
 svg+='<rect x="'+(eX-eudW/2)+'" y="'+eudTop+'" width="'+eudW+'" height="'+eudH+'" rx="6" fill="url(#eudioGrad)" stroke="#7dd3fc" stroke-width="1.2"/>';

 // Gas space at top of inverted tube (proportional to v_exp)
 const gasH=20+(v_exp/50.0)*135;
 const gasBottom=eudTop+gasH;
 svg+='<rect x="'+(eX-eudW/2+1)+'" y="'+eudTop+'" width="'+(eudW-2)+'" height="'+gasH+'" fill="url(#gasZone)" rx="5"/>';
 // Inverted meniscus (concave downward)
 svg+='<path d="M'+(eX-eudW/2+1)+' '+gasBottom+' Q'+eX+' '+(gasBottom-4)+' '+(eX+eudW/2-1)+' '+gasBottom+'" fill="#0284c7" fill-opacity=".3" stroke="#38bdf8" stroke-width="1.5"/>';

 // Leveling indicator line showing Δh = 0 (Internal Meniscus == External Meniscus)
 svg+='<line x1="'+(cylX-25)+'" y1="'+gasBottom+'" x2="'+(cylX+cylW+25)+'" y2="'+gasBottom+'" stroke="#4ade80" stroke-width="1.2" stroke-dasharray="3,2"/>';
 svg+='<text x="'+(cylX+cylW+28)+'" y="'+(gasBottom+3)+'" fill="#4ade80" font-size="7.5" font-weight="bold">MENISCUS LEVEL (Δh = 0)</text>';

 // Eudiometer graduations
 for(let gy=eudTop+15;gy<eudTop+eudH-30;gy+=8){
  svg+='<line x1="'+(eX+eudW/2-6)+'" y1="'+gy+'" x2="'+(eX+eudW/2-1)+'" y2="'+gy+'" stroke="#ffffff" stroke-opacity=".7" stroke-width="0.8"/>';
 }
 svg+='<text x="'+(eX+eudW/2-8)+'" y="'+(gasBottom-6)+'" text-anchor="end" fill="#f8fafc" font-size="8" font-family="monospace">'+v_exp.toFixed(1)+' mL</text>';

 // Effervescent bubbles ascending if busy
 if(busy){
  for(let bi=0;bi<12;bi++){
   const bx=eX-6+(bi*7)%12;
   const by=gasBottom+10+(bi*15);
   svg+='<circle cx="'+bx+'" cy="'+by+'" r="1.8" fill="#f8fafc" fill-opacity=".9"/>';
  }
 }

 // Copper wire cage at bottom orifice of eudiometer
 const cageY=eudTop+eudH-25;
 svg+='<path d="M'+(eX-8)+' '+cageY+' Q'+eX+' '+(cageY-6)+' '+(eX+8)+' '+cageY+' Q'+eX+' '+(cageY+6)+' '+(eX-8)+' '+cageY+'" fill="none" stroke="url(#copperCage)" stroke-width="2"/>';
 svg+='<rect x="'+(eX-4)+'" y="'+(cageY-3)+'" width="8" height="6" rx="1" fill="#cbd5e1"/>'; // dissolving Mg strip
 svg+='<line x1="'+eX+'" y1="'+(cageY+6)+'" x2="'+eX+'" y2="'+(eudTop+eudH+5)+'" stroke="#b45309" stroke-width="1.5"/>'; // copper tail

 // One-hole rubber stopper at tube mouth
 svg+='<polygon points="'+(eX-eudW/2-2)+','+(eudTop+eudH)+' '+(eX+eudW/2+2)+','+(eudTop+eudH)+' '+(eX+eudW/2-1)+','+(eudTop+eudH+15)+' '+(eX-eudW/2+1)+','+(eudTop+eudH+15)+'" fill="#020617" stroke="#334155"/>';

 svg+='<text x="'+eX+'" y="295" text-anchor="middle" fill="#60a5fa" font-size="9" font-weight="bold">2. LEVELING CYLINDER (Δh = 0)</text>';

 // -------------------------------------------------------------
 // 3. RIGHT STATION: Fortin Barometer & NIST Thermometer Station
 // -------------------------------------------------------------
 const barX=520,barY=60,barW=175,barH=215;
 svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barW+'" height="'+barH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(barX+barW/2)+'" y="'+(barY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">GAS METROLOGY TELEMETRY</text>';
 svg+='<line x1="'+(barX+12)+'" y1="'+(barY+25)+'" x2="'+(barX+barW-12)+'" y2="'+(barY+25)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+44)+'" fill="#94a3b8" font-size="8">Barometer P_atm:</text>';
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+44)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">760.00 mmHg</text>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+60)+'" fill="#94a3b8" font-size="8">Bath Temp T_water:</text>';
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+60)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">20.00 °C (293.15 K)</text>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+76)+'" fill="#38bdf8" font-size="8">P_H₂O* (Antoine):</text>';
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+76)+'" text-anchor="end" fill="#38bdf8" font-size="8.5" font-family="monospace">17.54 mmHg</text>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+92)+'" fill="#4ade80" font-size="8">P_dry (H₂):</text>';
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+92)+'" text-anchor="end" fill="#4ade80" font-size="8.5" font-family="monospace">742.46 mmHg</text>';

 svg+='<line x1="'+(barX+12)+'" y1="'+(barY+102)+'" x2="'+(barX+barW-12)+'" y2="'+(barY+102)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+118)+'" fill="#94a3b8" font-size="8">Raw Volume V_exp:</text>';
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+118)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">'+v_exp.toFixed(2)+' mL</text>';

 svg+='<rect x="'+(barX+10)+'" y="'+(barY+128)+'" width="'+(barW-20)+'" height="32" rx="3" fill="#061209" stroke="#1f3b28"/>';
 svg+='<text x="'+(barX+barW/2)+'" y="'+(barY+142)+'" text-anchor="middle" fill="#86efac" font-size="7.5">Standardized Volume at STP:</text>';
 svg+='<text x="'+(barX+barW/2)+'" y="'+(barY+154)+'" text-anchor="middle" fill="#4ade80" font-size="9" font-family="monospace" font-weight="bold">'+v_stp.toFixed(3)+' mL H₂</text>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+176)+'" fill="#94a3b8" font-size="7.5">Moles Generated n(H₂):</text>';
 const n_moles=(m_mg/1000.0/24.305);
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+176)+'" text-anchor="end" fill="#86efac" font-size="8" font-family="monospace">'+(n_moles*1000).toFixed(3)+' mmol</text>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+192)+'" fill="#94a3b8" font-size="7.5">Instantaneous V_m:</text>';
 const inst_vm=v_stp/1000.0/n_moles;
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+192)+'" text-anchor="end" fill="#fde047" font-size="8" font-family="monospace">'+inst_vm.toFixed(3)+' L/mol</text>';

 svg+='<text x="'+(barX+barW/2)+'" y="295" text-anchor="middle" fill="#4ade80" font-size="9" font-weight="bold">3. STP REDUCTION TELEMETRY</text>';

 svg+=text(360,312,'Dalton Gas Law: P_dry = P_atm − P_H₂O*(T). Internal and external water surfaces leveled to eliminate Δh head.','#789c80',8.5);
 return svg;
}

function drawGasCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'COMPARATIVE ANALYTICAL METROLOGY: GAS VOLUME & MOLAR MASS DETERMINATION','#86efac',12);

 const cards=[
  {
   title:'1. Eudiometry Displacement',
   sub:'Acid-Metal Gas Evolution over Water',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Principle: Stoichiometric metal dissolution (Mg + 2HCl ⟶ H₂)',
    'Measurement: Gas volume collected in Class A eudiometer',
    'Corrections: Dalton vapor pressure + hydrostatic head',
    'Precision: ±0.05 mL (±0.2% relative volumetric error)',
    'Dynamic Range: 5 to 50 mL gas evolution',
    'Primary advantage: Simple direct absolute stoichiometry',
    'Limitation: Saturated water vapor, trace gas solubility'
   ]
  },
  {
   title:'2. Dumas Vapor Density',
   sub:'Condensation of Vaporized Volatiles',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Principle: Volatilization in boiling water bath (100 °C)',
    'Measurement: Mass of condensed vapor filling bulb of volume V',
    'Formula: M = (m · R · T) / (P · V)',
    'Precision: ±0.5% to ±1.5% molar mass accuracy',
    'Applicability: Volatile liquids (bp 40 °C to 90 °C)',
    'Primary advantage: Determines unknown molecular weight',
    'Limitation: Premature condensation, vapor non-ideality'
   ]
  },
  {
   title:'3. Gas Chromatography (TCD)',
   sub:'Thermal Conductivity Gas Analysis',
   color:'#fde047',
   border:'#5a4814',
   items:[
    'Principle: Differential thermal conductivity detector (TCD)',
    'Helium/Argon carrier gas across heated tungsten filament',
    'Calibration: Multi-point certified calibration gas mixtures',
    'Precision: ±0.1% to ±0.5% RSD',
    'Detection Limits: 10 ppm to 100% composition',
    'Primary advantage: Simultaneous multi-gas separation',
    'Limitation: Expensive capital equipment, carrier gases'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Eudiometry directly connects macroscopic reactant mass to microscopic Avogadro mole volume.','#789c80',9);
 return svg;
}

function drawGasSandboxView(p,rawVal){
 const m_mg=p.input;
 const v_stp=rawVal;
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'GAS THERMODYNAMICS & REAL-GAS INTERMOLECULAR FORCES','#86efac',12);

 // Left Plot: STP Volume vs Magnesium Mass (0 to 40 mg)
 const pX=55,pY=48,pW=400,pH=225;
 svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" fill="#061209" stroke="#1f3b28" rx="4"/>';

 const mapX=m=>pX+(m/40.0)*pW;
 const mapY=v=>pY+pH-(v/40.0)*pH;

 // Linear ideal gas response line
 const x0=mapX(0),y0=mapY(0);
 const xEnd=mapX(40.0),yEnd=mapY(40.0*0.922197);
 svg+='<line x1="'+x0+'" y1="'+y0+'" x2="'+xEnd+'" y2="'+yEnd+'" stroke="#38bdf8" stroke-width="2.5"/>';

 // Grid lines & labels
 [10,20,30,40].forEach(m=>{
  svg+='<line x1="'+mapX(m)+'" y1="'+pY+'" x2="'+mapX(m)+'" y2="'+(pY+pH)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+mapX(m)+'" y="'+(pY+pH+14)+'" text-anchor="middle" fill="#789c80" font-size="8.5">'+m+' mg</text>';
 });
 [10,20,30,40].forEach(v=>{
  svg+='<line x1="'+pX+'" y1="'+mapY(v)+'" x2="'+(pX+pW)+'" y2="'+mapY(v)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+(pX-6)+'" y="'+(mapY(v)+3)+'" text-anchor="end" fill="#789c80" font-size="8.5">'+v+' mL</text>';
 });

 // Current operating point
 const curX=mapX(m_mg);
 const curY=mapY(v_stp);
 svg+='<circle cx="'+curX+'" cy="'+curY+'" r="6" fill="#4ade80" stroke="#08140c" stroke-width="2"/>';
 svg+='<circle cx="'+curX+'" cy="'+curY+'" r="9" fill="none" stroke="#4ade80" stroke-width="1.2" stroke-opacity=".6"/>';
 svg+='<line x1="'+curX+'" y1="'+curY+'" x2="'+curX+'" y2="'+(pY+pH)+'" stroke="#4ade80" stroke-dasharray="2,2"/>';
 svg+='<text x="'+(curX+10)+'" y="'+(curY-8)+'" fill="#86efac" font-size="8.5" font-family="monospace">V_STP = '+v_stp.toFixed(3)+' mL</text>';

 // Right Sidebar: Real Gas Virial / van der Waals Comparison
 const sX=475,sY=48,sW=220,sH=225;
 svg+='<rect x="'+sX+'" y="'+sY+'" width="'+sW+'" height="'+sH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">REAL GAS NON-IDEALITY</text>';
 svg+='<line x1="'+(sX+15)+'" y1="'+(sY+25)+'" x2="'+(sX+sW-15)+'" y2="'+(sY+25)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+42)+'" fill="#38bdf8" font-size="8.5" font-weight="bold">Hydrogen (H₂): Z = 1.0006</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+55)+'" fill="#94a3b8" font-size="7.5">a = 0.248 L²·bar/mol², b = 0.0266 L/mol</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+67)+'" fill="#94a3b8" font-size="7.5">Real V_m = 22.428 L/mol (+0.06% offset)</text>';

 svg+='<line x1="'+(sX+12)+'" y1="'+(sY+76)+'" x2="'+(sX+sW-12)+'" y2="'+(sY+76)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+92)+'" fill="#fde047" font-size="8.5" font-weight="bold">Carbon Dioxide (CO₂): Z = 0.9950</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+105)+'" fill="#94a3b8" font-size="7.5">a = 3.640 L²·bar/mol², b = 0.0427 L/mol</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+117)+'" fill="#94a3b8" font-size="7.5">Real V_m = 22.302 L/mol (−0.50% offset)</text>';

 svg+='<line x1="'+(sX+12)+'" y1="'+(sY+126)+'" x2="'+(sX+sW-12)+'" y2="'+(sY+126)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+142)+'" fill="#ef4444" font-size="8.5" font-weight="bold">Ammonia (NH₃): Z = 0.9880</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+155)+'" fill="#94a3b8" font-size="7.5">a = 4.225 L²·bar/mol², b = 0.0371 L/mol</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+167)+'" fill="#94a3b8" font-size="7.5">Real V_m = 22.145 L/mol (−1.20% offset)</text>';

 svg+='<rect x="'+(sX+10)+'" y="'+(sY+178)+'" width="'+(sW-20)+'" height="36" rx="3" fill="#061209" stroke="#1f3b28"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+192)+'" text-anchor="middle" fill="#86efac" font-size="7.5">Conclusion: H₂ is the closest of all</text>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+205)+'" text-anchor="middle" fill="#38bdf8" font-size="8" font-family="monospace">gases to ideal Avogadro behavior.</text>';

 svg+=text(360,305,'Thermodynamics: Repulsive excluded volume slightly exceeds attractive dispersion for H₂ at STP.','#789c80',9);
 return svg;
}

// ======================================================================
// CHEMISTRY LAB 05: DUMAS VAPOR DENSITY METHOD (MOLAR MASS)
// ======================================================================
function drawDumasBenchView(p,rawVal){
 const v_flask=p.input;
 const m_vap=rawVal;
 const rho_vap=(m_vap/v_flask);

 let svg='<defs>';
 svg+='<linearGradient id="boilWater" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#0284c7" stop-opacity=".3"/><stop offset="50%" stop-color="#38bdf8" stop-opacity=".15"/><stop offset="100%" stop-color="#0284c7" stop-opacity=".35"/></linearGradient>';
 svg+='<linearGradient id="flaskGlass" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ffffff" stop-opacity=".2"/><stop offset="25%" stop-color="#ffffff" stop-opacity=".06"/><stop offset="75%" stop-color="#38bdf8" stop-opacity=".1"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".25"/></linearGradient>';
 svg+='<linearGradient id="alumFoil" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#f1f5f9"/><stop offset="50%" stop-color="#94a3b8"/><stop offset="100%" stop-color="#64748b"/></linearGradient>';
 svg+='<linearGradient id="heatPlateDumas" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#334155"/><stop offset="100%" stop-color="#0f172a"/></linearGradient>';
 svg+='<filter id="plumeGlow"><feGaussianBlur stdDeviation="2.5" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';
 svg+='</defs>';

 // Background bench layout
 svg+='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+='<line x1="20" y1="280" x2="700" y2="280" stroke="#1f3b28" stroke-width="2"/>';

 // Header banner
 svg+=text(360,20,'DUMAS VAPOR DENSITY: PV = (m/M)RT ⟹ M = (m·R·T) / (P·V) [CYCLOHEXANE]','#86efac',11);

 // -------------------------------------------------------------
 // 1. LEFT STATION: Boiling Water Bath & Submerged Dumas Bulb
 // -------------------------------------------------------------
 const bX=145,bY=80;
 // Retort Stand & Clamp
 svg+='<rect x="'+(bX-85)+'" y="30" width="5" height="250" fill="#64748b"/>';
 svg+='<rect x="'+(bX-105)+'" y="276" width="45" height="6" rx="2" fill="#475569"/>';
 svg+='<rect x="'+(bX-85)+'" y="75" width="80" height="6" fill="#94a3b8"/>'; // clamp rod
 svg+='<circle cx="'+(bX-5)+'" cy="78" r="5" fill="#cbd5e1"/>'; // boss head
 // Clamp jaws grasping flask neck
 svg+='<path d="M'+(bX-14)+' 90 Q'+(bX-5)+' 84 '+bX+' 90" fill="none" stroke="#ef4444" stroke-width="4"/>';
 svg+='<path d="M'+bX+' 90 Q'+(bX+5)+' 84 '+(bX+14)+' 90" fill="none" stroke="#ef4444" stroke-width="4"/>';

 // Hotplate
 const hpX=bX-65,hpY=245,hpW=130,hpH=35;
 svg+='<rect x="'+hpX+'" y="'+hpY+'" width="'+hpW+'" height="'+hpH+'" rx="4" fill="url(#heatPlateDumas)" stroke="#475569" stroke-width="1.2"/>';
 svg+='<rect x="'+(hpX+8)+'" y="'+(hpY+8)+'" width="42" height="18" rx="2" fill="#020617" stroke="#1e293b"/>';
 svg+='<text x="'+(hpX+29)+'" y="'+(hpY+21)+'" text-anchor="middle" fill="#ef4444" font-size="8.5" font-family="monospace">100.0°C</text>';
 svg+='<circle cx="'+(hpX+75)+'" cy="'+(hpY+17)+'" r="6" fill="#64748b"/>';
 svg+='<text x="'+(hpX+102)+'" y="'+(hpY+21)+'" text-anchor="middle" fill="#86efac" font-size="7.5">BOIL</text>';

 // 2000 mL Tall Pyrex Beaker Water Bath
 const bkX=bX-55,bkY=115,bkW=110,bkH=130;
 svg+='<rect x="'+bkX+'" y="'+bkY+'" width="'+bkW+'" height="'+bkH+'" rx="3" fill="url(#boilWater)" stroke="#94a3b8" stroke-width="1.5"/>';
 // Boiling water level (near top)
 const boilTop=bkY+20;
 svg+='<rect x="'+(bkX+2)+'" y="'+boilTop+'" width="'+(bkW-4)+'" height="'+(bkH-22)+'" fill="#0284c7" fill-opacity=".2"/>';
 svg+='<line x1="'+bkX+'" y1="'+boilTop+'" x2="'+(bkX+bkW)+'" y2="'+boilTop+'" stroke="#38bdf8" stroke-width="1.2"/>';
 // Boiling bubbles
 for(let bi=0;bi<14;bi++){
  const bx=bkX+12+(bi*13)%(bkW-24);
  const by=bkY+bkH-10-((bi*19)%(bkH-35));
  svg+='<circle cx="'+bx+'" cy="'+by+'" r="2" fill="#ffffff" fill-opacity=".7"/>';
 }

 // Submerged Dumas Bulb (Erlenmeyer / bulb form)
 const flW=46,flH=95;
 const flTop=bkY+5;
 svg+='<path d="M'+(bX-8)+' '+flTop+' L'+(bX-8)+' '+(flTop+35)+' L'+(bX-flW/2)+' '+(flTop+flH)+' Q'+bX+' '+(flTop+flH+6)+' '+(bX+flW/2)+' '+(flTop+flH)+' L'+(bX+8)+' '+(flTop+35)+' L'+(bX+8)+' '+flTop+' Z" fill="url(#flaskGlass)" stroke="#e0f2fe" stroke-width="1.2"/>';

 // Aluminum foil cap with pinhole
 svg+='<polygon points="'+(bX-12)+','+(flTop-4)+' '+(bX+12)+','+(flTop-4)+' '+(bX+10)+','+(flTop+8)+' '+(bX-10)+','+(flTop+8)+'" fill="url(#alumFoil)" stroke="#475569"/>';
 svg+='<circle cx="'+bX+'" cy="'+(flTop-4)+'" r="1.2" fill="#020617"/>'; // pinhole

 // Vapor venting jet / plume from pinhole if busy
 if(busy){
  svg+='<path d="M'+bX+' '+(flTop-6)+' Q'+(bX-6)+' '+(flTop-25)+' '+(bX+4)+' '+(flTop-45)+' T'+(bX-2)+' '+(flTop-65)+'" fill="none" stroke="#f8fafc" stroke-width="2" stroke-opacity=".8" filter="url(#plumeGlow)"/>';
  svg+='<path d="M'+(bX+2)+' '+(flTop-6)+' Q'+(bX+8)+' '+(flTop-20)+' '+(bX-4)+' '+(flTop-40)+'" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-opacity=".6"/>';
 }
 svg+='<text x="'+(bX+18)+'" y="'+(flTop-15)+'" fill="#38bdf8" font-size="7.5">0.5 mm Pinhole</text>';

 svg+='<text x="'+bX+'" y="295" text-anchor="middle" fill="#94a3b8" font-size="9" font-weight="bold">1. BOILING WATER BATH (100.0 °C)</text>';

 // -------------------------------------------------------------
 // 2. CENTER STATION: Water Pycnometry Calibration
 // -------------------------------------------------------------
 const pycX=350,pycY=125;
 svg+='<rect x="'+(pycX-40)+'" y="'+pycY+'" width="80" height="120" rx="4" fill="#0f172a" fill-opacity=".6" stroke="#334155" stroke-width="1.2"/>';
 // Calibrated flask filled with water to brim
 svg+='<path d="M'+(pycX-7)+' '+(pycY+20)+' L'+(pycX-7)+' '+(pycY+40)+' L'+(pycX-25)+' '+(pycY+105)+' Q'+pycX+' '+(pycY+110)+' '+(pycX+25)+' '+(pycY+105)+' L'+(pycX+7)+' '+(pycY+40)+' L'+(pycX+7)+' '+(pycY+20)+' Z" fill="url(#boilWater)" stroke="#7dd3fc" stroke-width="1.2"/>';
 // Flat ground glass optical plate shearing meniscus
 svg+='<rect x="'+(pycX-15)+'" y="'+(pycY+17)+'" width="30" height="3" fill="#cbd5e1" stroke="#94a3b8"/>';
 svg+='<text x="'+pycX+'" y="'+(pycY+12)+'" text-anchor="middle" fill="#38bdf8" font-size="7">Optical Flat Plate</text>';
 svg+='<text x="'+pycX+'" y="'+(pycY+70)+'" text-anchor="middle" fill="#f8fafc" font-size="8.5" font-family="monospace">'+v_flask.toFixed(1)+' mL</text>';
 svg+='<text x="'+pycX+'" y="'+(pycY+82)+'" text-anchor="middle" fill="#94a3b8" font-size="7">±0.02 mL (Pycnometry)</text>';

 svg+='<text x="'+pycX+'" y="295" text-anchor="middle" fill="#60a5fa" font-size="9" font-weight="bold">2. VOLUME PYCNOMETRY</text>';

 // -------------------------------------------------------------
 // 3. RIGHT STATION: Analytical Balance & Condensed Vapor Telemetry
 // -------------------------------------------------------------
 const abX=490,abY=95,abW=205,abH=175;
 svg+='<rect x="'+abX+'" y="'+abY+'" width="'+abW+'" height="'+abH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(abX+abW/2)+'" y="'+(abY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">VAPOR DENSITY TELEMETRY</text>';
 svg+='<line x1="'+(abX+12)+'" y1="'+(abY+25)+'" x2="'+(abX+abW-12)+'" y2="'+(abY+25)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(abX+14)+'" y="'+(abY+42)+'" fill="#94a3b8" font-size="8">Bulb Volume V_flask:</text>';
 svg+='<text x="'+(abX+abW-14)+'" y="'+(abY+42)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">'+v_flask.toFixed(1)+' mL</text>';

 svg+='<text x="'+(abX+14)+'" y="'+(abY+57)+'" fill="#94a3b8" font-size="8">Bath Temp T_bath:</text>';
 svg+='<text x="'+(abX+abW-14)+'" y="'+(abY+57)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">100.00 °C (373.15 K)</text>';

 svg+='<text x="'+(abX+14)+'" y="'+(abY+72)+'" fill="#94a3b8" font-size="8">Barometric Pressure P:</text>';
 svg+='<text x="'+(abX+abW-14)+'" y="'+(abY+72)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">1.0000 atm (760.0 mmHg)</text>';

 svg+='<line x1="'+(abX+12)+'" y1="'+(abY+80)+'" x2="'+(abX+abW-12)+'" y2="'+(abY+80)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(abX+14)+'" y="'+(abY+96)+'" fill="#38bdf8" font-size="8">Condensed Vapor m:</text>';
 svg+='<text x="'+(abX+abW-14)+'" y="'+(abY+96)+'" text-anchor="end" fill="#4ade80" font-size="8.5" font-family="monospace">'+m_vap.toFixed(4)+' g</text>';

 svg+='<text x="'+(abX+14)+'" y="'+(abY+111)+'" fill="#94a3b8" font-size="8">Vapor Density ρ_vap:</text>';
 svg+='<text x="'+(abX+abW-14)+'" y="'+(abY+111)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">'+rho_vap.toFixed(6)+' g/mL</text>';

 svg+='<rect x="'+(abX+10)+'" y="'+(abY+120)+'" width="'+(abW-20)+'" height="30" rx="3" fill="#061209" stroke="#1f3b28"/>';
 svg+='<text x="'+(abX+abW/2)+'" y="'+(abY+133)+'" text-anchor="middle" fill="#86efac" font-size="7.5">Calculated Molar Mass M:</text>';
 const m_calc=(m_vap*82.0574*373.15)/(1.000*v_flask);
 svg+='<text x="'+(abX+abW/2)+'" y="'+(abY+145)+'" text-anchor="middle" fill="#38bdf8" font-size="9" font-family="monospace" font-weight="bold">'+m_calc.toFixed(2)+' g/mol</text>';

 svg+='<text x="'+(abX+14)+'" y="'+(abY+164)+'" fill="#94a3b8" font-size="7.5">Substance Identification:</text>';
 svg+='<text x="'+(abX+abW-14)+'" y="'+(abY+164)+'" text-anchor="end" fill="#fde047" font-size="8" font-weight="bold">Cyclohexane (C₆H₁₂)</text>';

 svg+='<text x="'+(abX+abW/2)+'" y="295" text-anchor="middle" fill="#4ade80" font-size="9" font-weight="bold">3. ANALYTICAL BALANCE (±0.1 mg)</text>';

 svg+=text(360,312,'Dumas Metrology: Pure vapor fills bulb at T_bath and P_atm. Condensation isolates exact mole mass.','#789c80',8.5);
 return svg;
}

function drawDumasCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'COMPARATIVE ANALYTICAL METROLOGY: MOLECULAR WEIGHT DETERMINATION TECHNIQUES','#86efac',12);

 const cards=[
  {
   title:'1. Dumas Vapor Method',
   sub:'Open Bulb Boiling Bath Gravimetry',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Principle: Vapor sweeps air; bulb filled at T_bath & P_atm',
    'Measurement: Mass of condensed vapor filling bulb of volume V',
    'Formula: M = (m_vapor · R · T) / (P · V)',
    'Precision: ±0.5% to ±1.0% molar mass accuracy',
    'Applicability: Volatile liquids with bp 40 °C to 95 °C',
    'Primary advantage: Classical direct physical gravimetry',
    'Limitation: Saturated vapor near bp exhibits non-ideality'
   ]
  },
  {
   title:'2. Victor Meyer Method',
   sub:'Closed Chamber Air Displacement',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Principle: Fragile sample ampoule dropped into heated tube',
    'Measurement: Displaced air volume collected over water',
    'Formula: M = (m_sample · R · T_room) / (P_dry · V_air)',
    'Precision: ±1.0% to ±2.0% accuracy',
    'Applicability: High-boiling volatiles up to 300 °C (vapor jackets)',
    'Primary advantage: Requires only tiny sample aliquot (~0.1 g)',
    'Limitation: Thermal convection currents, rubber stopper leakage'
   ]
  },
  {
   title:'3. Cryoscopic Osmometry',
   sub:'Freezing-Point Depression Colligative',
   color:'#fde047',
   border:'#5a4814',
   items:[
    'Principle: Colligative freezing point shift: ΔT_f = K_f · m_solute',
    'Measurement: Differential temperature drop via Beckmann sensor',
    'Formula: M = (K_f · w_solute · 1000) / (ΔT_f · W_solvent)',
    'Precision: ±0.2% to ±0.8% with large K_f solvents (camphor)',
    'Applicability: Non-volatile and volatile solutes in solution',
    'Primary advantage: Operates at low temperature, zero vapor loss',
    'Limitation: Solute association/dissociation shifts van\'t Hoff i'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Dumas measures vapor mass directly; Victor Meyer measures displaced air volume.','#789c80',9);
 return svg;
}

function drawDumasSandboxView(p,rawVal){
 const v_flask=p.input;
 const m_vap=rawVal;
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'VAPOR DENSITY LINEARITY & VAN DER WAALS NON-IDEALITY: CYCLOHEXANE (C₆H₁₂)','#86efac',12);

 // Left Plot: Condensed vapor mass vs Flask volume (0 to 420 mL)
 const pX=55,pY=48,pW=390,pH=225;
 svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" fill="#061209" stroke="#1f3b28" rx="4"/>';

 const mapX=vol=>pX+(vol/420.0)*pW;
 const mapY=mass=>pY+pH-(mass/1.20)*pH;

 const x0=mapX(0),y0=mapY(0);
 const xEnd=mapX(420.0),yEnd=mapY(420.0*0.00274859);
 svg+='<line x1="'+x0+'" y1="'+y0+'" x2="'+xEnd+'" y2="'+yEnd+'" stroke="#38bdf8" stroke-width="2.5"/>';

 [100,200,300,400].forEach(vol=>{
  svg+='<line x1="'+mapX(vol)+'" y1="'+pY+'" x2="'+mapX(vol)+'" y2="'+(pY+pH)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+mapX(vol)+'" y="'+(pY+pH+14)+'" text-anchor="middle" fill="#789c80" font-size="8.5">'+vol+' mL</text>';
 });
 [0.3,0.6,0.9,1.2].forEach(mass=>{
  svg+='<line x1="'+pX+'" y1="'+mapY(mass)+'" x2="'+(pX+pW)+'" y2="'+mapY(mass)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+(pX-6)+'" y="'+(mapY(mass)+3)+'" text-anchor="end" fill="#789c80" font-size="8.5">'+mass.toFixed(1)+' g</text>';
 });

 const curX=mapX(v_flask);
 const curY=mapY(m_vap);
 svg+='<circle cx="'+curX+'" cy="'+curY+'" r="6" fill="#4ade80" stroke="#08140c" stroke-width="2"/>';
 svg+='<circle cx="'+curX+'" cy="'+curY+'" r="9" fill="none" stroke="#4ade80" stroke-width="1.2" stroke-opacity=".6"/>';
 svg+='<line x1="'+curX+'" y1="'+curY+'" x2="'+curX+'" y2="'+(pY+pH)+'" stroke="#4ade80" stroke-dasharray="2,2"/>';
 svg+='<text x="'+(curX+10)+'" y="'+(curY-8)+'" fill="#86efac" font-size="8.5" font-family="monospace">m_vap = '+m_vap.toFixed(4)+' g</text>';

 // Right Sidebar: Molecular Chair Conformation & Non-Ideality
 const sX=465,sY=48,sW=235,sH=225;
 svg+='<rect x="'+sX+'" y="'+sY+'" width="'+sW+'" height="'+sH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">MOLECULAR THERMODYNAMICS</text>';
 svg+='<line x1="'+(sX+15)+'" y1="'+(sY+25)+'" x2="'+(sX+sW-15)+'" y2="'+(sY+25)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+42)+'" fill="#38bdf8" font-size="8.5" font-weight="bold">Cyclohexane (C₆H₁₂, Chair Form):</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+55)+'" fill="#94a3b8" font-size="7.5">Molar Mass M = 84.161 g/mol, bp = 80.7 °C</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+67)+'" fill="#94a3b8" font-size="7.5">van der Waals a = 23.3 L²·bar/mol², b = 0.144 L/mol</text>';

 svg+='<line x1="'+(sX+12)+'" y1="'+(sY+76)+'" x2="'+(sX+sW-12)+'" y2="'+(sY+76)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+92)+'" fill="#fde047" font-size="8.5" font-weight="bold">Compressibility Factors (Z = PV/nRT):</text>';
 svg+='<text x="'+(sX+14)+'" y="'+(sY+106)+'" fill="#86efac" font-size="7.5">Ideal Gas: Z = 1.0000 ⟹ M = 84.16 g/mol</text>';
 svg+='<text x="'+(sX+14)+'" y="'+(sY+118)+'" fill="#38bdf8" font-size="7.5">Real Cyclohexane at 100 °C: Z = 0.985</text>';
 svg+='<text x="'+(sX+14)+'" y="'+(sY+130)+'" fill="#94a3b8" font-size="7.5">Uncorrected M_apparent = M_true / Z ≈ 85.4 g/mol</text>';

 svg+='<line x1="'+(sX+12)+'" y1="'+(sY+138)+'" x2="'+(sX+sW-12)+'" y2="'+(sY+138)+'" stroke="#1f3b28"/>';

 svg+='<rect x="'+(sX+10)+'" y="'+(sY+146)+'" width="'+(sW-20)+'" height="68" rx="3" fill="#061209" stroke="#1f3b28"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+160)+'" text-anchor="middle" fill="#86efac" font-size="7.5" font-weight="bold">Multi-Point Regression Benefit:</text>';
 svg+='<foreignObject x="'+(sX+14)+'" y="'+(sY+165)+'" width="'+(sW-28)+'" height="46"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7px;color:#a0aec0;line-height:1.25;margin:0">Plotting m_vapor vs V_flask across 6 calibrated bulbs absorbs constant aluminum foil tare errors into the intercept m₀ = 0.0000 g, isolating true vapor density with R² = 1.00000.</p></foreignObject>';

 svg+=text(360,305,'Thermodynamics: Dense organic vapors near condensation exhibit attractive London dispersion (Z < 1).','#789c80',9);
 return svg;
}



// ======================================================================
// CHEMISTRY LAB 06: THE COPPER CYCLE (MASS CONSERVATION)
// ======================================================================
function drawCopperBenchView(p,rawVal){
 const m_init=p.input;
 const m_rec=rawVal;
 const n_moles=m_init/63.546;

 let svg='<defs>';
 svg+='<linearGradient id="cuNitrateGrad" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#10b981" stop-opacity=".7"/><stop offset="100%" stop-color="#059669" stop-opacity=".9"/></linearGradient>';
 svg+='<linearGradient id="cuHydroxideGrad" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#38bdf8" stop-opacity=".8"/><stop offset="100%" stop-color="#0284c7" stop-opacity=".95"/></linearGradient>';
 svg+='<linearGradient id="cuOxideGrad" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#27272a" stop-opacity=".95"/><stop offset="100%" stop-color="#09090b" stop-opacity=".98"/></linearGradient>';
 svg+='<linearGradient id="cuSulfateGrad" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#3b82f6" stop-opacity=".8"/><stop offset="100%" stop-color="#1d4ed8" stop-opacity=".95"/></linearGradient>';
 svg+='<linearGradient id="cuMetalGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#f97316"/><stop offset="50%" stop-color="#ea580c"/><stop offset="100%" stop-color="#9a3412"/></linearGradient>';
 svg+='<linearGradient id="glassWall" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#ffffff" stop-opacity=".2"/><stop offset="10%" stop-color="#ffffff" stop-opacity=".04"/><stop offset="90%" stop-color="#ffffff" stop-opacity=".06"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".25"/></linearGradient>';
 svg+='</defs><rect width="720" height="320" fill="#08140c"/>';

 svg+=text(360,20,'QUANTITATIVE FIVE-STEP CHEMICAL TRANSFORMATION CYCLE: COPPER CONSERVATION','#86efac',12);

 // Table surface
 svg+='<rect x="0" y="275" width="720" height="45" fill="#132419" stroke="#1f3b2a" stroke-width="1"/>';
 svg+='<line x1="0" y1="275" x2="720" y2="275" stroke="#2d523b" stroke-width="2"/>';

 // Draw 5 Reaction Stations
 const stations=[
  {num:'1',label:'HNO₃ Oxidation',formula:'Cu ⟶ Cu(NO₃)₂',color:'#10b981',grad:'url(#cuNitrateGrad)',sub:'Brown NO₂↑ gas'},
  {num:'2',label:'NaOH Metathesis',formula:'Cu²⁺ ⟶ Cu(OH)₂↓',color:'#38bdf8',grad:'url(#cuHydroxideGrad)',sub:'Gelatinous sky blue'},
  {num:'3',label:'Thermal Dehyd.',formula:'Cu(OH)₂ ⟶ CuO↓',color:'#a1a1aa',grad:'url(#cuOxideGrad)',sub:'Granular black at 90°C'},
  {num:'4',label:'H₂SO₄ Leaching',formula:'CuO ⟶ CuSO₄',color:'#60a5fa',grad:'url(#cuSulfateGrad)',sub:'Royal blue solution'},
  {num:'5',label:'Zn Reduction',formula:'Cu²⁺ ⟶ Cu(s)↓',color:'#fb923c',grad:'url(#cuMetalGrad)',sub:'Spongy copper isolated'}
 ];

 stations.forEach((st,idx)=>{
  const bx=20+idx*104,bw=92,by=42,bh=158;
  // Card container
  svg+='<rect x="'+bx+'" y="'+by+'" width="'+bw+'" height="'+bh+'" rx="5" fill="#0b1a10" stroke="#1f3b2a" stroke-width="1.2"/>';
  // Step badge
  svg+='<rect x="'+(bx+6)+'" y="'+(by+6)+'" width="20" height="14" rx="3" fill="#162e1e"/>';
  svg+='<text x="'+(bx+16)+'" y="'+(by+17)+'" text-anchor="middle" fill="#86efac" font-size="9" font-weight="bold">'+st.num+'</text>';
  svg+='<text x="'+(bx+30)+'" y="'+(by+17)+'" fill="#cbd5e1" font-size="8" font-weight="bold">'+st.label+'</text>';
  svg+='<text x="'+(bx+bw/2)+'" y="'+(by+30)+'" text-anchor="middle" fill="'+st.color+'" font-size="7.5" font-family="monospace">'+st.formula+'</text>';

  // Miniature Beaker
  const bkX=bx+18,bkY=by+38,bkW=56,bkH=68;
  svg+='<rect x="'+bkX+'" y="'+bkY+'" width="'+bkW+'" height="'+bkH+'" rx="3" fill="url(#glassWall)" stroke="#4b7055" stroke-width="1"/>';
  // Beaker lip
  svg+='<ellipse cx="'+(bkX+bkW/2)+'" cy="'+bkY+'" rx="'+(bkW/2)+'" ry="3" fill="none" stroke="#789c80" stroke-width="1"/>';
  // Solution / Precipitate inside beaker
  const fillH=idx===2?42:(idx===4?38:46);
  svg+='<rect x="'+(bkX+2)+'" y="'+(bkY+bkH-fillH)+'" width="'+(bkW-4)+'" height="'+fillH+'" rx="2" fill="'+st.grad+'"/>';

  if(idx===0){
   // NO2 gas bubbles / fumes rising
   svg+='<circle cx="'+(bkX+20)+'" cy="'+(bkY+28)+'" r="3.5" fill="#ca8a04" fill-opacity=".8"/>';
   svg+='<circle cx="'+(bkX+36)+'" cy="'+(bkY+18)+'" r="4.5" fill="#b45309" fill-opacity=".7"/>';
   svg+='<circle cx="'+(bkX+28)+'" cy="'+(bkY+8)+'" r="5.5" fill="#9a3412" fill-opacity=".6"/>';
  }else if(idx===1){
   // Gelatinous precipitate flakes
   for(let f=0;f<5;f++){
    svg+='<ellipse cx="'+(bkX+12+f*8)+'" cy="'+(bkY+bkH-12-((f*7)%20))+'" rx="4" ry="2" fill="#7dd3fc" fill-opacity=".9"/>';
   }
  }else if(idx===2){
   // Dense black particles settled + heat waves underneath
   for(let p=0;p<8;p++){
    svg+='<circle cx="'+(bkX+10+p*5)+'" cy="'+(bkY+bkH-6-((p*3)%10))+'" r="2.5" fill="#000000"/>';
   }
   svg+='<path d="M'+(bkX+10)+' '+(bkY+bkH+6)+' Q'+(bkX+18)+' '+(bkY+bkH+2)+' '+(bkX+26)+' '+(bkY+bkH+6)+' Q'+(bkX+34)+' '+(bkY+bkH+10)+' '+(bkX+42)+' '+(bkY+bkH+6)+'" fill="none" stroke="#ef4444" stroke-width="1.5"/>';
  }else if(idx===3){
   // Clear royal blue solution
   svg+='<rect x="'+(bkX+6)+'" y="'+(bkY+bkH-fillH+4)+'" width="6" height="30" fill="#93c5fd" fill-opacity=".4" rx="2"/>';
  }else if(idx===4){
   // Spongy reddish copper cake at bottom + bubbles
   svg+='<rect x="'+(bkX+6)+'" y="'+(bkY+bkH-16)+'" width="'+(bkW-12)+'" height="14" rx="2" fill="url(#cuMetalGrad)"/>';
   svg+='<circle cx="'+(bkX+22)+'" cy="'+(bkY+bkH-22)+'" r="2" fill="#ffffff" fill-opacity=".7"/>';
   svg+='<circle cx="'+(bkX+34)+'" cy="'+(bkY+bkH-30)+'" r="1.8" fill="#ffffff" fill-opacity=".7"/>';
  }

  // Description footer
  svg+='<text x="'+(bx+bw/2)+'" y="'+(by+122)+'" text-anchor="middle" fill="#94a3b8" font-size="7">'+st.sub+'</text>';

  // Status pill
  svg+='<rect x="'+(bx+8)+'" y="'+(by+132)+'" width="'+(bw-16)+'" height="18" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg+='<text x="'+(bx+bw/2)+'" y="'+(by+144)+'" text-anchor="middle" fill="#86efac" font-size="7.5" font-family="monospace">Cu: '+(idx<4?'100% In System':'100% Isolated')+'</text>';

  // Reaction arrow connecting to next station
  if(idx<4){
   svg+='<path d="M'+(bx+bw)+' '+(by+bh/2)+' L'+(bx+bw+12)+' '+(by+bh/2)+'" stroke="#38a169" stroke-width="2" stroke-dasharray="2,2"/>';
   svg+='<polygon points="'+(bx+bw+12)+','+(by+bh/2-3)+' '+(bx+bw+16)+','+(by+bh/2)+' '+(bx+bw+12)+','+(by+bh/2+3)+'" fill="#38a169"/>';
  }
 });

 // Analytical Pan & Quantitative Readout Banner (Bottom)
 const panX=20,panY=210,panW=680,panH=58;
 svg+='<rect x="'+panX+'" y="'+panY+'" width="'+panW+'" height="'+panH+'" rx="6" fill="#0a190e" stroke="#22422c" stroke-width="1.5"/>';

 // Initial mass badge
 svg+='<rect x="'+(panX+15)+'" y="'+(panY+10)+'" width="145" height="38" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(panX+25)+'" y="'+(panY+24)+'" fill="#789c80" font-size="8" font-weight="bold">INITIAL COPPER WIRE</text>';
 svg+='<text x="'+(panX+25)+'" y="'+(panY+40)+'" fill="#f97316" font-size="13" font-family="monospace" font-weight="bold">m₀ = '+m_init.toFixed(4)+' g</text>';

 // Stoichiometric mole conservation
 svg+='<rect x="'+(panX+175)+'" y="'+(panY+10)+'" width="165" height="38" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(panX+185)+'" y="'+(panY+24)+'" fill="#789c80" font-size="8" font-weight="bold">MOLAR QUANTITY [M=63.546]</text>';
 svg+='<text x="'+(panX+185)+'" y="'+(panY+40)+'" fill="#38bdf8" font-size="12" font-family="monospace" font-weight="bold">n(Cu) = '+n_moles.toFixed(5)+' mol</text>';

 // Final recovered mass badge
 svg+='<rect x="'+(panX+355)+'" y="'+(panY+10)+'" width="155" height="38" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(panX+365)+'" y="'+(panY+24)+'" fill="#789c80" font-size="8" font-weight="bold">RECOVERED PURE COPPER</text>';
 svg+='<text x="'+(panX+365)+'" y="'+(panY+40)+'" fill="#86efac" font-size="13" font-family="monospace" font-weight="bold">m_rec = '+m_rec.toFixed(4)+' g</text>';

 // Recovery % & Conservation status
 svg+='<rect x="'+(panX+525)+'" y="'+(panY+10)+'" width="140" height="38" rx="4" fill="#051009" stroke="#22543d"/>';
 svg+='<text x="'+(panX+535)+'" y="'+(panY+24)+'" fill="#86efac" font-size="8" font-weight="bold">STOICHIOMETRIC YIELD</text>';
 svg+='<text x="'+(panX+535)+'" y="'+(panY+40)+'" fill="#48bb78" font-size="13" font-family="monospace" font-weight="bold">Yield = 100.00%</text>';

 svg+=text(360,305,'Conservation Metrology: Cu ⟶ Cu(NO₃)₂ ⟶ Cu(OH)₂ ⟶ CuO ⟶ CuSO₄ ⟶ Cu (100.00% Recovery).','#789c80',8.5);
 return svg;
}

function drawCopperCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'COMPARATIVE EXTRACTIVE & REFINING METALLURGY: COPPER PROCESSING ROUTES','#86efac',12);

 const cards=[
  {
   title:'1. Cyclic Hydrometallurgy',
   sub:'Aqueous Closed Cycle (Our Protocol)',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Principle: Sequential aqueous redox, metathesis & dehydration',
    'Reactions: HNO₃ oxid. ⟶ NaOH ppt ⟶ Dehyd. ⟶ H₂SO₄ ⟶ Zn red.',
    'Energy & Temp: Ambient to 90 °C (low carbon/energy demand)',
    'Theoretical Yield: 100.00% closed-loop stoichiometric conservation',
    'Selectivity: Eliminates iron & zinc via acidic extraction',
    'Primary advantage: Rigorous quantitative proof of mass conservation',
    'Limitation: Multi-step transfers require meticulous wall rinsing'
   ]
  },
  {
   title:'2. Pyrometallurgical Smelting',
   sub:'Flash Furnace Carbothermal Smelting',
   color:'#fb923c',
   border:'#5a3014',
   items:[
    'Principle: High-temperature oxidation of chalcopyrite (CuFeS₂)',
    'Reactions: 2CuFeS₂ + 2.5O₂ ⟶ Cu₂S·FeS (matte) + FeO + 2SO₂',
    'Energy & Temp: 1250 °C to 1350 °C in oxygen-enriched blast furnace',
    'Theoretical Yield: 95% to 98% copper recovered into blister cake',
    'Selectivity: Produces 98.5% crude blister copper (requires refining)',
    'Primary advantage: Massive industrial capacity (millions of tons/yr)',
    'Limitation: Massive SO₂ emissions, slag disposal, huge energy demand'
   ]
  },
  {
   title:'3. Electrolytic Refining',
   sub:'Acidic CuSO₄ Electrorefining (Cathode)',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Principle: Anodic dissolution & cathodic deposition of Cu²⁺ ions',
    'Reactions: Cu(blister anode) ⟶ Cu²⁺ + 2e⁻ ⟶ Cu(pure cathode)',
    'Energy & Temp: 55 °C to 65 °C; electrical power ~300 kWh/ton',
    'Theoretical Yield: >99.5% cathode current efficiency (Faraday's law)',
    'Selectivity: Produces 99.99% Grade A electrolytic copper cathode',
    'Primary advantage: Precious metals (Au, Ag, Pt) drop as anode slime',
    'Limitation: Requires pre-smelted copper anodes and high DC power'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Hydrometallurgy conserves atom mass in closed cycles; Pyrometallurgy processes high-volume ore.','#789c80',9);
 return svg;
}

function drawCopperSandboxView(p,rawVal){
 const m_init=p.input;
 const m_rec=rawVal;
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'MASS CONSERVATION BUDGET & MULTI-STEP REACTION EFFICIENCY: COPPER CYCLE','#86efac',12);

 // Left Plot: Stage-by-Stage Copper Mass Conservation (0 to 5)
 const pX=50,pY=48,pW=395,pH=225;
 svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" fill="#061209" stroke="#1f3b28" rx="4"/>';

 const stages=['Start (Cu)','Step 1 (NO₃)','Step 2 (OH)','Step 3 (CuO)','Step 4 (SO₄)','Step 5 (Cu)'];
 const barW=36;

 stages.forEach((stg,idx)=>{
  const cx=pX+35+idx*60;
  const h=(m_init/0.80)*170;
  const by=pY+pH-h-25;

  // Background guide line
  svg+='<line x1="'+cx+'" y1="'+pY+'" x2="'+cx+'" y2="'+(pY+pH)+'" stroke="#132418" stroke-width="1"/>';
  // Mass bar
  const col=idx===0?'#f97316':(idx===5?'#48bb78':'#38bdf8');
  svg+='<rect x="'+(cx-barW/2)+'" y="'+by+'" width="'+barW+'" height="'+h+'" rx="3" fill="'+col+'" fill-opacity=".85" stroke="'+col+'" stroke-width="1"/>';
  // Mass label on bar
  svg+='<text x="'+cx+'" y="'+(by-6)+'" text-anchor="middle" fill="#f8fafc" font-size="8" font-family="monospace">'+m_init.toFixed(3)+'g</text>';
  // X axis label
  svg+='<text x="'+cx+'" y="'+(pY+pH-8)+'" text-anchor="middle" fill="#789c80" font-size="7.5">'+stg+'</text>';
 });

 // Conservation boundary line across all bars
 const idealY=pY+pH-((m_init/0.80)*170)-25;
 svg+='<line x1="'+(pX+15)+'" y1="'+idealY+'" x2="'+(pX+pW-15)+'" y2="'+idealY+'" stroke="#facc15" stroke-width="1.8" stroke-dasharray="3,3"/>';
 svg+='<text x="'+(pX+pW-18)+'" y="'+(idealY-4)+'" text-anchor="end" fill="#facc15" font-size="8">100.00% Theoretical Invariant</text>';

 // Right Panel: Systematic Error Sensitivity & Yield Perturbations
 const rX=460,rY=48,rW=235,rH=225;
 svg+='<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="5" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">ANALYTICAL SENSITIVITY AUDIT</text>';

 const errItems=[
  {label:'Residual Zinc Metal (+)',desc:'Unreacted Zn in spongy Cu falsely inflates yield',val:'+2.0% per 10 mg Zn',col:'#f87171'},
  {label:'Transfer Decantation (-)',desc:'Loss of CuO/Cu during decant or beaker wall rinse',val:'-1.0% per 5 mg Cu',col:'#fbbf24'},
  {label:'Surface Oxidation (+)',desc:'Hot drying in air oxidizes Cu ⟶ CuO (+25.2% O)',val:'Prevented by ethanol/desicc.',col:'#38bdf8'},
  {label:'Colloidal Passing (-)',desc:'Cu(OH)₂ bypassing filter paper without dehydration',val:'Prevented by 90°C heating',col:'#a78bfa'},
  {label:'OLS Slope Insulation (★)',desc:'Constant transfer losses absorbed into intercept m₀',val:'Slope = 1.0000 g/g Unbiased',col:'#48bb78'}
 ];

 errItems.forEach((ei,idx)=>{
  const ey=rY+32+idx*38;
  svg+='<rect x="'+(rX+8)+'" y="'+ey+'" width="'+(rW-16)+'" height="32" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+12)+'" fill="'+ei.col+'" font-size="7.5" font-weight="bold">'+ei.label+'</text>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+24)+'" fill="#94a3b8" font-size="6.8">'+ei.desc+'</text>';
  svg+='<text x="'+(rX+rW-14)+'" y="'+(ey+12)+'" text-anchor="end" fill="'+ei.col+'" font-size="7.5" font-family="monospace">'+ei.val+'</text>';
 });

 svg+=text(360,305,'Mass Budget: OLS regression slope m_slope = 1.0000 g/g insulates true stoichiometry against transfer offsets.','#789c80',9);
 return svg;
}


// ======================================================================
// CHEMISTRY LAB 07: EMPIRICAL FORMULA OF MAGNESIUM OXIDE (MgO)
// ======================================================================
function drawMgBenchView(p,rawVal){
 const m_mg=p.input;
 const m_ox=rawVal;
 const m_tot=m_mg+m_ox;
 const n_mg=m_mg/24.305;
 const n_ox=m_ox/15.9994;
 const ratio=n_ox/n_mg;

 let svg='<defs>';
 svg+='<linearGradient id="flameGrad" x1="0%" y1="100%" x2="0%" y2="0%"><stop offset="0%" stop-color="#1e3a8a"/><stop offset="30%" stop-color="#3b82f6"/><stop offset="70%" stop-color="#38bdf8"/><stop offset="100%" stop-color="#fef08a"/></linearGradient>';
 svg+='<linearGradient id="innerCone" x1="0%" y1="100%" x2="0%" y2="0%"><stop offset="0%" stop-color="#0284c7"/><stop offset="100%" stop-color="#a7f3d0"/></linearGradient>';
 svg+='<linearGradient id="porcelainGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#e2e8f0"/><stop offset="25%" stop-color="#ffffff"/><stop offset="75%" stop-color="#cbd5e1"/><stop offset="100%" stop-color="#94a3b8"/></linearGradient>';
 svg+='<linearGradient id="incandescentGlow" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#ffffff"/><stop offset="40%" stop-color="#fef08a"/><stop offset="80%" stop-color="#f97316"/><stop offset="100%" stop-color="#dc2626"/></linearGradient>';
 svg+='<linearGradient id="burnerMetal" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#334155"/><stop offset="50%" stop-color="#64748b"/><stop offset="100%" stop-color="#1e293b"/></linearGradient>';
 svg+='</defs><rect width="720" height="320" fill="#08140c"/>';

 svg+=text(360,20,'CRUCIBLE THERMAL OXIDATION & EMPIRICAL FORMULA DETERMINATION: MAGNESIUM OXIDE (MgO)','#86efac',12);

 // Table surface
 svg+='<rect x="0" y="275" width="720" height="45" fill="#132419" stroke="#1f3b2a" stroke-width="1"/>';
 svg+='<line x1="0" y1="275" x2="720" y2="275" stroke="#2d523b" stroke-width="2"/>';

 // --- LEFT SYSTEM: Meker Burner & High-Form Porcelain Crucible (x = 30 to 340) ---
 // Burner base & barrel
 const bX=175;
 svg+='<rect x="'+(bX-45)+'" y="260" width="90" height="15" rx="3" fill="url(#burnerMetal)" stroke="#0f172a"/>';
 svg+='<rect x="'+(bX-12)+'" y="180" width="24" height="80" fill="url(#burnerMetal)" stroke="#0f172a"/>';
 // Meker burner expanded grid head
 svg+='<path d="M'+(bX-18)+' 180 L'+(bX-26)+' 162 L'+(bX+26)+' 162 L'+(bX+18)+' 180 Z" fill="url(#burnerMetal)" stroke="#0f172a"/>';
 // Grid lines on Meker head
 for(let g=-20;g<=20;g+=8){
  svg+='<line x1="'+(bX+g)+'" y1="162" x2="'+(bX+g)+'" y2="168" stroke="#94a3b8" stroke-width="1"/>';
 }

 // Iron Ring & Clay Pipe Triangle
 svg+='<line x1="'+(bX-75)+'" y1="125" x2="'+(bX+75)+'" y2="125" stroke="#475569" stroke-width="5"/>'; // Iron ring
 // Ceramic clay pipes of triangle
 svg+='<line x1="'+(bX-38)+'" y1="125" x2="'+(bX+38)+'" y2="125" stroke="#e2e8f0" stroke-width="7" stroke-linecap="round"/>';
 svg+='<line x1="'+(bX-38)+'" y1="125" x2="'+bX+'" y2="92" stroke="#e2e8f0" stroke-width="7" stroke-linecap="round"/>';
 svg+='<line x1="'+(bX+38)+'" y1="125" x2="'+bX+'" y2="92" stroke="#e2e8f0" stroke-width="7" stroke-linecap="round"/>';

 // High-temperature Meker flame
 svg+='<path d="M'+(bX-24)+' 162 Q'+(bX-12)+' 120 '+bX+' 95 Q'+(bX+12)+' 120 '+(bX+24)+' 162 Z" fill="url(#flameGrad)" fill-opacity=".85"/>';
 svg+='<path d="M'+(bX-14)+' 162 Q'+(bX-6)+' 136 '+bX+' 118 Q'+(bX+6)+' 136 '+(bX+14)+' 162 Z" fill="url(#innerCone)" fill-opacity=".95"/>';

 // High-Form Porcelain Crucible (seated in clay triangle)
 const cX=bX,cY=68,cW=52,cH=54;
 // Glowing bottom when heating
 svg+='<ellipse cx="'+cX+'" cy="'+(cY+cH)+'" rx="'+(cW/3.2)+'" ry="4" fill="#ef4444" fill-opacity=".9"/>';
 // Crucible body (tapered)
 svg+='<path d="M'+(cX-cW/2)+' '+cY+' L'+(cX-cW/3.2)+' '+(cY+cH)+' Q'+cX+' '+(cY+cH+5)+' '+(cX+cW/3.2)+' '+(cY+cH)+' L'+(cX+cW/2)+' '+cY+' Z" fill="url(#porcelainGrad)" stroke="#64748b" stroke-width="1"/>';
 // Crucible rim lip
 svg+='<ellipse cx="'+cX+'" cy="'+cY+'" rx="'+(cW/2)+'" ry="5" fill="#f8fafc" stroke="#64748b" stroke-width="1"/>';

 // Incandescent magnesium flare / ash inside crucible
 svg+='<ellipse cx="'+cX+'" cy="'+(cY+12)+'" rx="'+(cW/2.4)+'" ry="4" fill="url(#incandescentGlow)"/>';
 if(busy){
  // Active combustion sparks & light rays
  svg+='<circle cx="'+cX+'" cy="'+(cY+8)+'" r="12" fill="#ffffff" fill-opacity=".7"/>';
  svg+='<line x1="'+(cX-18)+'" y1="'+(cY-6)+'" x2="'+(cX+18)+'" y2="'+(cY+22)+'" stroke="#ffffff" stroke-width="1.5"/>';
  svg+='<line x1="'+(cX+18)+'" y1="'+(cY-6)+'" x2="'+(cX-18)+'" y2="'+(cY+22)+'" stroke="#ffffff" stroke-width="1.5"/>';
 }

 // Crucible Lid (tilted / cracked open 1.5 mm to admit O2)
 svg+='<path d="M'+(cX-cW/2-2)+' '+(cY-4)+' L'+(cX+cW/2+4)+' '+(cY-8)+' L'+(cX+cW/2+2)+' '+(cY-12)+' L'+(cX-cW/2-4)+' '+(cY-8)+' Z" fill="url(#porcelainGrad)" stroke="#64748b" stroke-width="1"/>';
 // Lid handle loop
 svg+='<rect x="'+(cX-4)+'" y="'+(cY-15)+'" width="8" height="5" rx="2" fill="url(#porcelainGrad)" stroke="#64748b"/>';
 // Tiny arrow indicating air O2 diffusing into crucible
 svg+='<path d="M'+(cX+cW/2+18)+' '+(cY-18)+' Q'+(cX+cW/2+10)+' '+(cY-8)+' '+(cX+cW/2-2)+' '+(cY-5)+'" fill="none" stroke="#38bdf8" stroke-width="1.5"/>';
 svg+='<text x="'+(cX+cW/2+24)+'" y="'+(cY-16)+'" fill="#38bdf8" font-size="7.5" font-weight="bold">O₂ influx</text>';

 svg+='<rect x="'+(bX-95)+'" y="38" width="190" height="20" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+bX+'" y="52" text-anchor="middle" fill="#86efac" font-size="8.5" font-weight="bold">Meker Flame Calcination: 850 °C</text>';


 // --- RIGHT SYSTEM: Analytical Force Restoration Balance (x = 370 to 690) ---
 const balX=390,balY=95,balW=300,balH=175;
 // Granite anti-vibration base
 svg+='<rect x="'+(balX-10)+'" y="260" width="'+(balW+20)+'" height="15" rx="3" fill="#1e293b" stroke="#0f172a"/>';
 // Main balance enclosure
 svg+='<rect x="'+balX+'" y="'+balY+'" width="'+balW+'" height="'+balH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';

 // Glass Draft Chamber (upper half of balance)
 const dX=balX+15,dY=balY+12,dW=balW-30,dH=98;
 svg+='<rect x="'+dX+'" y="'+dY+'" width="'+dW+'" height="'+dH+'" rx="4" fill="#061209" stroke="#334155" stroke-width="1.2"/>';
 // Stainless steel balance pan
 svg+='<rect x="'+(dX+dW/2-35)+'" y="'+(dY+dH-8)+'" width="70" height="6" rx="2" fill="#94a3b8" stroke="#475569"/>';
 svg+='<rect x="'+(dX+dW/2-5)+'" y="'+(dY+dH-2)+'" width="10" height="8" fill="#64748b"/>';

 // Cooled porcelain crucible on balance pan with snow-white MgO product
 const pX=dX+dW/2,pY=dY+dH-42,pW=36,pH=34;
 svg+='<path d="M'+(pX-pW/2)+' '+pY+' L'+(pX-pW/3.2)+' '+(pY+pH)+' L'+(pX+pW/3.2)+' '+(pY+pH)+' L'+(pX+pW/2)+' '+pY+' Z" fill="url(#porcelainGrad)" stroke="#475569" stroke-width="1"/>';
 svg+='<ellipse cx="'+pX+'" cy="'+pY+'" rx="'+(pW/2)+'" ry="3.5" fill="#f8fafc" stroke="#64748b"/>';
 // White MgO powder cake inside crucible
 svg+='<ellipse cx="'+pX+'" cy="'+(pY+8)+'" rx="'+(pW/2.5)+'" ry="2.8" fill="#ffffff"/>';

 // Balance LCD Display
 const lcdX=balX+25,lcdY=balY+120,lcdW=balW-50,lcdH=42;
 svg+='<rect x="'+lcdX+'" y="'+lcdY+'" width="'+lcdW+'" height="'+lcdH+'" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.5"/>';
 svg+='<circle cx="'+(lcdX+16)+'" cy="'+(lcdY+21)+'" r="4" fill="'+(busy?'#eab308':'#48bb78')+'"/>';
 svg+='<text x="'+(lcdX+26)+'" y="'+(lcdY+17)+'" fill="#789c80" font-size="7.5">STABLE</text>';
 svg+='<text x="'+(lcdX+26)+'" y="'+(lcdY+28)+'" fill="#789c80" font-size="7.5">NET MASS</text>';

 const dispVal=measurement?m_ox.toFixed(4):(busy?(rawVal*0.75).toFixed(4):'0.0000');
 svg+='<text x="'+(lcdX+lcdW-16)+'" y="'+(lcdY+28)+'" text-anchor="end" fill="#86efac" font-size="19" font-family="monospace" font-weight="bold">'+dispVal+' g O</text>';

 // Summary Data Card (Bottom Banner)
 const bannerX=20,bannerY=215,bannerW=340,bannerH=52;
 svg+='<rect x="'+bannerX+'" y="'+bannerY+'" width="'+bannerW+'" height="'+bannerH+'" rx="5" fill="#0a190e" stroke="#22422c"/>';
 svg+='<text x="'+(bannerX+12)+'" y="'+(bannerY+16)+'" fill="#f97316" font-size="8.5" font-weight="bold">m(Mg) = '+m_mg.toFixed(4)+' g  [n = '+n_mg.toFixed(5)+' mol]</text>';
 svg+='<text x="'+(bannerX+12)+'" y="'+(bannerY+31)+'" fill="#38bdf8" font-size="8.5" font-weight="bold">m(O)  = '+m_ox.toFixed(4)+' g  [n = '+n_ox.toFixed(5)+' mol]</text>';
 svg+='<text x="'+(bannerX+12)+'" y="'+(bannerY+45)+'" fill="#86efac" font-size="8.5" font-family="monospace" font-weight="bold">n(O)/n(Mg) = '+ratio.toFixed(4)+' ⟹ Empirical Formula MgO</text>';

 svg+=text(360,305,'Metrology: 2Mg(s) + O₂(g) ⟶ 2MgO(s); Steam hydrolyzes intermediate Mg₃N₂ ⟶ MgO.','#789c80',8.5);
 return svg;
}

function drawMgCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'COMPARATIVE ANALYTICAL STOICHIOMETRY: FORMULA & EQUIVALENT DETERMINATIONS','#86efac',12);

 const cards=[
  {
   title:'1. Crucible Thermal Oxidation',
   sub:'Direct High-Temp Binary Synthesis (Our Lab)',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Analyte: Electropositive metals (Mg ribbon, Cu, Sn)',
    'Principle: Direct combustion with atmospheric oxygen',
    'Reagents: 99.9% Mg ribbon, porcelain crucible, Meker burner',
    'Digestion: Hot steam destroys intermediate Mg₃N₂ ⟶ NH₃↑',
    'Temperature: 850 °C (cherry red calcination to constant mass)',
    'Measurement: Mass gain of bound lattice oxygen (m_oxygen)',
    'Invariant: Slope directly isolates stoichiometric ratio M(O)/M(Mg)'
   ]
  },
  {
   title:'2. Solution Metathesis Ppt.',
   sub:'Aqueous Ionic Double Displacement',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Analyte: Insoluble inorganic salts (BaSO₄, AgCl, PbCrO₄)',
    'Principle: Metathesis precipitation under low supersaturation',
    'Reagents: Standard aqueous salt solutions (e.g., BaCl₂ + Na₂SO₄)',
    'Digestion: 85 °C Ostwald ripening converts colloid to granular',
    'Temperature: 80 °C to 90 °C water bath; Gooch filtration',
    'Measurement: Isolated anhydrous precipitate cake mass',
    'Invariant: Slope isolates formula weight via limiting reactant'
   ]
  },
  {
   title:'3. Dumas Vapor Density',
   sub:'Gas-Phase Molecular Weight Metrology',
   color:'#fde047',
   border:'#5a4814',
   items:[
    'Analyte: Volatile organic liquids (cyclohexane, CCl₄, ethanol)',
    'Principle: Vapor sweeps air; bulb filled at T_bath and P_atm',
    'Reagents: Volatile organic analyte, boiling water bath, barometer',
    'Digestion: Rapid air quenching condenses vapor inside bulb',
    'Temperature: 100.0 °C (boiling water bath immersion)',
    'Measurement: Mass of condensed vapor filling flask volume V',
    'Invariant: Slope isolates ideal gas equation of state molar mass'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Thermal oxidation synthesizes binary solid; Precipitation filters ions; Dumas weighs vapor.','#789c80',9);
 return svg;
}

function drawMgSandboxView(p,rawVal){
 const m_mg=p.input;
 const m_ox=rawVal;
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'STOICHIOMETRIC MECHANISM, NITRIDE HYDROLYSIS & DEFECT AUDIT: MgO','#86efac',12);

 // Left Panel: Rocksalt FCC Lattice & Thermochemical Cycle
 const lX=25,lY=46,lW=340,lH=230;
 svg+='<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">ROCKSALT FCC LATTICE (SPACE GROUP Fm3̄m)</text>';

 // 3D perspective wireframe cube of MgO unit cell
 const ox=lX+80,oy=lY+95,s=70;
 // Back square
 svg+='<rect x="'+(ox+25)+'" y="'+(oy-25)+'" width="'+s+'" height="'+s+'" fill="none" stroke="#1e3a29" stroke-width="1.2"/>';
 // Connecting lines
 svg+='<line x1="'+ox+'" y1="'+oy+'" x2="'+(ox+25)+'" y2="'+(oy-25)+'" stroke="#1e3a29" stroke-width="1.2"/>';
 svg+='<line x1="'+(ox+s)+'" y1="'+oy+'" x2="'+(ox+s+25)+'" y2="'+(oy-25)+'" stroke="#1e3a29" stroke-width="1.2"/>';
 svg+='<line x1="'+ox+'" y1="'+(oy+s)+'" x2="'+(ox+25)+'" y2="'+(oy+s-25)+'" stroke="#1e3a29" stroke-width="1.2"/>';
 svg+='<line x1="'+(ox+s)+'" y1="'+(oy+s)+'" x2="'+(ox+s+25)+'" y2="'+(oy+s-25)+'" stroke="#1e3a29" stroke-width="1.2"/>';
 // Front square
 svg+='<rect x="'+ox+'" y="'+oy+'" width="'+s+'" height="'+s+'" fill="none" stroke="#2d523b" stroke-width="1.5"/>';

 // Corner & edge ions (alternating Mg2+ green, O2- red)
 const ions=[
  {x:ox,y:oy,col:'#48bb78',r:6,label:'Mg²⁺'},
  {x:ox+s/2,y:oy,col:'#ef4444',r:8,label:'O²⁻'},
  {x:ox+s,y:oy,col:'#48bb78',r:6,label:'Mg²⁺'},
  {x:ox,y:oy+s/2,col:'#ef4444',r:8,label:'O²⁻'},
  {x:ox+s/2,y:oy+s/2,col:'#48bb78',r:6,label:'Mg²⁺'},
  {x:ox+s,y:oy+s/2,col:'#ef4444',r:8,label:'O²⁻'},
  {x:ox,y:oy+s,col:'#48bb78',r:6,label:'Mg²⁺'},
  {x:ox+s/2,y:oy+s,col:'#ef4444',r:8,label:'O²⁻'},
  {x:ox+s,y:oy+s,col:'#48bb78',r:6,label:'Mg²⁺'}
 ];
 ions.forEach(i=>{
  svg+='<circle cx="'+i.x+'" cy="'+i.y+'" r="'+i.r+'" fill="'+i.col+'" stroke="#051009" stroke-width="1"/>';
 });

 // Lattice thermochemistry legend
 svg+='<rect x="'+(lX+190)+'" y="'+(lY+38)+'" width="138" height="120" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+52)+'" fill="#789c80" font-size="7.5" font-weight="bold">BORN-HABER THERMODYNAMICS</text>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+67)+'" fill="#cbd5e1" font-size="7">ΔH_sub(Mg) = +148 kJ/mol</text>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+80)+'" fill="#cbd5e1" font-size="7">IE₁ + IE₂  = +2188 kJ/mol</text>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+93)+'" fill="#cbd5e1" font-size="7">½ D(O₂)    = +249 kJ/mol</text>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+106)+'" fill="#cbd5e1" font-size="7">EA₁ + EA₂  = +603 kJ/mol</text>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+120)+'" fill="#38bdf8" font-size="7.5" font-weight="bold">U_lattice  = -3791 kJ/mol</text>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+134)+'" fill="#86efac" font-size="8" font-weight="bold">ΔH°_f(MgO) = -601.7 kJ/mol</text>';

 svg+='<text x="'+(lX+lW/2)+'" y="'+(lY+215)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">Stoichiometric charge neutrality: 1 Mg²⁺ cation per 1 O²⁻ anion (Coordination Number 6:6)</text>';


 // Right Panel: Systematic Error & Nitride Audit
 const rX=380,rY=46,rW=315,rH=230;
 svg+='<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">NITRIDE DIGESTION & ERROR SENSITIVITY AUDIT</text>';

 const errItems=[
  {label:'Unhydrolyzed Mg₃N₂ (-)',desc:'Omitting water leaves N instead of O (M_N=14 vs M_O=16)',val:'-0.274 g O / g Mg error',col:'#f87171'},
  {label:'Aerosol Smoke Loss (-)',desc:'Escaping white MgO nanoparticles if lid kept open',val:'-2% to -8% mass deficit',col:'#fbbf24'},
  {label:'Glaze Silica Attack (+)',desc:'Basic MgO reacts with porcelain SiO₂ at >900 °C',val:'Minor tare alteration',col:'#38bdf8'},
  {label:'Atmospheric Moisture (+)',desc:'Cooled MgO powder chemisorbs H₂O and CO₂ from air',val:'Prevented by desiccator',col:'#a78bfa'},
  {label:'OLS Slope Insulation (★)',desc:'Constant crucible glaze tare absorbed into intercept m₀',val:'Slope = 0.6582 g/g Unbiased',col:'#48bb78'}
 ];

 errItems.forEach((ei,idx)=>{
  const ey=rY+30+idx*39;
  svg+='<rect x="'+(rX+8)+'" y="'+ey+'" width="'+(rW-16)+'" height="33" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+12)+'" fill="'+ei.col+'" font-size="7.5" font-weight="bold">'+ei.label+'</text>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+25)+'" fill="#94a3b8" font-size="6.8">'+ei.desc+'</text>';
  svg+='<text x="'+(rX+rW-14)+'" y="'+(ey+12)+'" text-anchor="end" fill="'+ei.col+'" font-size="7.5" font-family="monospace">'+ei.val+'</text>';
 });

 svg+=text(360,305,'Formula Verification: Ordinary least-squares regression slope m_slope = 0.65823 g O / g Mg isolations ratio n(O)/n(Mg) = 1.0000.','#789c80',9);
 return svg;
}


// ======================================================================
// CHEMISTRY LAB 08: LIQUID VISCOSITY & POISEUILLE FLOW
// ======================================================================
function drawPoiseuilleBenchView(p,rawVal){
 const h_cm=p.input;
 const q_val=rawVal;
 const dP_pa=998.2*9.80665*(h_cm/100.0);
 const v_mean=(q_val/60.0/1e6)/(Math.PI*Math.pow(0.00025,2));
 const reynolds=(2.0*0.00025*v_mean*998.2)/0.0010020;

 let svg='<defs>';
 svg+='<linearGradient id="waterFlow" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#0284c7" stop-opacity=".7"/><stop offset="50%" stop-color="#38bdf8" stop-opacity=".9"/><stop offset="100%" stop-color="#0284c7" stop-opacity=".7"/></linearGradient>';
 svg+='<linearGradient id="jacketGlass" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#ffffff" stop-opacity=".2"/><stop offset="15%" stop-color="#38bdf8" stop-opacity=".08"/><stop offset="85%" stop-color="#38bdf8" stop-opacity=".12"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".3"/></linearGradient>';
 svg+='<linearGradient id="reservoirGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#ffffff" stop-opacity=".25"/><stop offset="20%" stop-color="#ffffff" stop-opacity=".05"/><stop offset="80%" stop-color="#ffffff" stop-opacity=".08"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".3"/></linearGradient>';
 svg+='</defs><rect width="720" height="320" fill="#08140c"/>';

 svg+=text(360,20,'HAGEN-POISEUILLE CONSTANT-HEAD CAPILLARY VISCOMETER (20.0 °C THERMOSTATED)','#86efac',12);

 // Table surface
 svg+='<rect x="0" y="275" width="720" height="45" fill="#132419" stroke="#1f3b2a" stroke-width="1"/>';
 svg+='<line x1="0" y1="275" x2="720" y2="275" stroke="#2d523b" stroke-width="2"/>';

 // --- 1. Constant-Head Reservoir (Left: x = 30 to 140) ---
 const resX=45,resW=65,resH=180,resY=45;
 svg+='<rect x="'+resX+'" y="'+resY+'" width="'+resW+'" height="'+resH+'" rx="4" fill="url(#reservoirGrad)" stroke="#475569" stroke-width="1.2"/>';

 // Liquid column height in reservoir corresponding to Delta h (cm)
 const hPixels=(h_cm/40.0)*130;
 const liquidY=resY+resH-30-hPixels;
 svg+='<rect x="'+(resX+2)+'" y="'+liquidY+'" width="'+(resW-4)+'" height="'+(resY+resH-liquidY)+'" rx="2" fill="url(#waterFlow)" fill-opacity=".65"/>';
 svg+='<ellipse cx="'+(resX+resW/2)+'" cy="'+liquidY+'" rx="'+(resW/2-2)+'" ry="4" fill="#7dd3fc" fill-opacity=".8"/>';

 // Overflow weir tube on left of reservoir
 svg+='<path d="M'+resX+' '+(liquidY+5)+' L'+(resX-18)+' '+(liquidY+5)+' L'+(resX-18)+' '+(resY+resH)+' L'+(resX-24)+' '+(resY+resH)+'" fill="none" stroke="#64748b" stroke-width="3"/>';
 svg+='<text x="'+(resX-20)+'" y="'+(liquidY)+'" text-anchor="end" fill="#94a3b8" font-size="7">Overflow Weir</text>';

 // Cathetometer height indicator scale
 svg+='<line x1="'+(resX+resW+8)+'" y1="'+(resY+resH-30)+'" x2="'+(resX+resW+8)+'" y2="'+liquidY+'" stroke="#facc15" stroke-width="2"/>';
 svg+='<line x1="'+(resX+resW+4)+'" y1="'+liquidY+'" x2="'+(resX+resW+12)+'" y2="'+liquidY+'" stroke="#facc15" stroke-width="2"/>';
 svg+='<line x1="'+(resX+resW+4)+'" y1="'+(resY+resH-30)+'" x2="'+(resX+resW+12)+'" y2="'+(resY+resH-30)+'" stroke="#facc15" stroke-width="2"/>';
 svg+='<text x="'+(resX+resW+16)+'" y="'+(liquidY+hPixels/2+4)+'" fill="#facc15" font-size="9" font-weight="bold">Δh = '+h_cm.toFixed(1)+' cm</text>';

 // Feed line connecting reservoir bottom to capillary
 svg+='<path d="M'+(resX+resW/2)+' '+(resY+resH)+' L'+(resX+resW/2)+' '+(resY+resH+15)+' L160 '+(resY+resH+15)+' L160 170" fill="none" stroke="#38bdf8" stroke-width="5" stroke-opacity=".8"/>';


 // --- 2. Jacketed Precision Capillary Tube (Center: x = 160 to 490) ---
 const capX=170,capY=162,capW=310,capH=16;
 // Thermostatic Water Jacket (outer cylinder)
 const jX=155,jY=146,jW=340,jH=48;
 svg+='<rect x="'+jX+'" y="'+jY+'" width="'+jW+'" height="'+jH+'" rx="8" fill="url(#jacketGlass)" stroke="#38bdf8" stroke-width="1.5"/>';
 svg+='<text x="'+(jX+jW/2)+'" y="'+(jY-6)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">Water Jacket: 20.0 ± 0.05 °C (Length L = 15.00 cm)</text>';

 // Precision Capillary Tube inside (inner tube)
 svg+='<rect x="'+capX+'" y="'+capY+'" width="'+capW+'" height="'+capH+'" rx="2" fill="url(#reservoirGrad)" stroke="#64748b" stroke-width="1"/>';
 // Flowing liquid stream inside capillary
 svg+='<rect x="'+(capX+1)+'" y="'+(capY+4)+'" width="'+(capW-2)+'" height="'+(capH-8)+'" fill="url(#waterFlow)"/>';

 // Laminar streamline dashes
 if(busy){
  for(let l=0;l<5;l++){
   svg+='<line x1="'+(capX+20+l*55)+'" y1="'+(capY+capH/2)+'" x2="'+(capX+45+l*55)+'" y2="'+(capY+capH/2)+'" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,2"/>';
  }
 }
 svg+='<text x="'+(capX+capW/2)+'" y="'+(capY+capH/2+3)+'" text-anchor="middle" fill="#ffffff" font-size="7.5" font-weight="bold">Radius r = 0.250 mm (Poiseuille Laminar Streamlines)</text>';

 // Jacket circulating coolant ports
 svg+='<rect x="'+(jX+30)+'" y="'+(jY+jH)+'" width="12" height="15" fill="#38bdf8" stroke="#0284c7"/>';
 svg+='<text x="'+(jX+36)+'" y="'+(jY+jH+24)+'" text-anchor="middle" fill="#38bdf8" font-size="7">Bath In (20°C)</text>';
 svg+='<rect x="'+(jX+jW-42)+'" y="'+(jY-15)+'" width="12" height="15" fill="#38bdf8" stroke="#0284c7"/>';
 svg+='<text x="'+(jX+jW-36)+'" y="'+(jY-18)+'" text-anchor="middle" fill="#38bdf8" font-size="7">Bath Out</text>';


 // --- 3. Receiving Vessel / Effluent Burette (Right: x = 520 to 690) ---
 const bX=540,bY=120,bW=34,bH=150;
 svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="3" fill="url(#reservoirGrad)" stroke="#64748b" stroke-width="1.2"/>';
 // Capillary exit nozzle into receiving burette
 svg+='<path d="M'+(capX+capW)+' '+(capY+capH/2)+' L'+(bX+bW/2)+' '+(capY+capH/2)+' L'+(bX+bW/2)+' '+(bY+15)+'" fill="none" stroke="#38bdf8" stroke-width="3"/>';
 // Dripping effluent
 svg+='<line x1="'+(bX+bW/2)+'" y1="'+(bY+15)+'" x2="'+(bX+bW/2)+'" y2="'+(bY+35)+'" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3,3"/>';
 svg+='<circle cx="'+(bX+bW/2)+'" cy="'+(bY+38)+'" r="2" fill="#7dd3fc"/>';

 // Collected liquid in receiving burette
 const collH=Math.min(90, Math.max(10, (q_val/2.2)*80));
 svg+='<rect x="'+(bX+2)+'" y="'+(bY+bH-collH)+'" width="'+(bW-4)+'" height="'+collH+'" rx="2" fill="url(#waterFlow)" fill-opacity=".75"/>';
 // Burette graduation lines
 for(let gy=bY+20;gy<bY+bH-10;gy+=12){
  svg+='<line x1="'+bX+'" y1="'+gy+'" x2="'+(bX+6)+'" y2="'+gy+'" stroke="#94a3b8" stroke-width="0.8"/>';
 }

 // Analytical Digital Readout Screen (Right Panel)
 const panX=590,panY=85,panW=115,panH=150;
 svg+='<rect x="'+panX+'" y="'+panY+'" width="'+panW+'" height="'+panH+'" rx="5" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(panX+panW/2)+'" y="'+(panY+18)+'" text-anchor="middle" fill="#86efac" font-size="9" font-weight="bold">DISCHARGE RATE</text>';

 svg+='<rect x="'+(panX+8)+'" y="'+(panY+26)+'" width="'+(panW-16)+'" height="32" rx="3" fill="#051009" stroke="#162e1e"/>';
 const dispQ=measurement?q_val.toFixed(3):(busy?(rawVal*0.75).toFixed(3):'0.000');
 svg+='<text x="'+(panX+panW/2)+'" y="'+(panY+48)+'" text-anchor="middle" fill="#38bdf8" font-size="14" font-family="monospace" font-weight="bold">'+dispQ+'</text>';
 svg+='<text x="'+(panX+panW/2)+'" y="'+(panY+70)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">mL / min</text>';

 svg+='<rect x="'+(panX+8)+'" y="'+(panY+78)+'" width="'+(panW-16)+'" height="58" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(panX+12)+'" y="'+(panY+92)+'" fill="#789c80" font-size="7">ΔP = '+dP_pa.toFixed(0)+' Pa</text>';
 svg+='<text x="'+(panX+12)+'" y="'+(panY+105)+'" fill="#789c80" font-size="7">v = '+v_mean.toFixed(3)+' m/s</text>';
 svg+='<text x="'+(panX+12)+'" y="'+(panY+118)+'" fill="#86efac" font-size="7" font-weight="bold">Re = '+reynolds.toFixed(1)+' (Laminar)</text>';
 svg+='<text x="'+(panX+12)+'" y="'+(panY+130)+'" fill="#facc15" font-size="7">η = 1.0020 mPa·s</text>';

 svg+=text(360,305,'Poiseuille Metrology: Q = (π·r⁴·ΔP) / (8·η·L); High aspect ratio (L/r = 600) eliminates Couette end-effects.','#789c80',8.5);
 return svg;
}

function drawPoiseuilleCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'COMPARATIVE VISCOMETRY METROLOGY: PRIMARY VS SECONDARY FLUID TRANSPORT METHODS','#86efac',12);

 const cards=[
  {
   title:'1. Absolute Poiseuille Capillary',
   sub:'Primary Hydrostatic Capillary Flow (Our Lab)',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Principle: Steady laminar flow under constant hydrostatic head Δh',
    'Equation: Q = (π · r⁴ · ρ · g · Δh) / (8 · η · L)',
    'Classification: Fundamental primary method (no calibration fluid needed)',
    'Fluid range: Low-viscosity fluids (0.3 to 20 mPa·s, water/solvents)',
    'Temperature control: Thermostated water jacket stable to ±0.05 °C',
    'Primary advantage: Extracts true absolute dynamic viscosity directly',
    'Limitation: Highly sensitive to capillary radius bore uniformity (r⁴)'
   ]
  },
  {
   title:'2. Relative Ostwald / Ubbelohde',
   sub:'Gravity Efflux Timing in U-Tube',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Principle: Efflux time t of fixed volume draining between etched marks',
    'Equation: η_unk / η_ref = (ρ_unk · t_unk) / (ρ_ref · t_ref)',
    'Classification: Secondary relative method (requires pure water reference)',
    'Fluid range: Polymer solutions, intrinsic viscosity [η], biological serums',
    'Temperature control: Immersion in large optical thermostatic bath',
    'Primary advantage: Simple glassware, fast execution, small sample volume',
    'Limitation: Relative only; variable driving head requires meniscus alignment'
   ]
  },
  {
   title:'3. Falling Sphere / Rotational',
   sub:'Stokes Terminal Drag & Concentric Cylinder Shear',
   color:'#fde047',
   border:'#5a4814',
   items:[
    'Principle: Stokes settling sphere (Höppler) or Couette drag torque',
    'Equation: Höppler: η = K · (ρ_s - ρ) · t; Couette: τ = η · (du/dy)',
    'Classification: Direct mechanical shear rate rheometry',
    'Fluid range: Medium to ultra-high viscosity (1 to 10⁶ mPa·s, oils/polymers)',
    'Temperature control: Jacketed cell with Peltier heating/cooling',
    'Primary advantage: Sweeps shear rates to detect shear-thinning (non-Newtonian)',
    'Limitation: High-viscosity requirement; wall effects alter settling speed'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Poiseuille measures absolute viscosity standard-free; Ostwald requires water calibration.','#789c80',9);
 return svg;
}

function drawPoiseuilleSandboxView(p,rawVal){
 const h_cm=p.input;
 const q_val=rawVal;
 const dP_pa=998.2*9.80665*(h_cm/100.0);
 const v_mean=(q_val/60.0/1e6)/(Math.PI*Math.pow(0.00025,2));
 const reynolds=(2.0*0.00025*v_mean*998.2)/0.0010020;

 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'PARABOLIC SHEAR VELOCITY PROFILE & LAMINAR FLOW STABILITY: POISEUILLE','#86efac',12);

 // Left Panel: Parabolic Velocity Profile across Capillary Bore (r = -R to +R)
 const lX=25,lY=46,lW=340,lH=230;
 svg+='<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">PARABOLIC SHEAR VELOCITY PROFILE v(r)</text>';

 // Upper & lower capillary walls
 const wY1=lY+45,wY2=lY+165;
 svg+='<line x1="'+(lX+20)+'" y1="'+wY1+'" x2="'+(lX+lW-20)+'" y2="'+wY1+'" stroke="#94a3b8" stroke-width="3"/>';
 svg+='<text x="'+(lX+25)+'" y="'+(wY1-6)+'" fill="#94a3b8" font-size="7.5">Upper Capillary Wall (r = +R, v = 0 No-Slip)</text>';
 svg+='<line x1="'+(lX+20)+'" y1="'+wY2+'" x2="'+(lX+lW-20)+'" y2="'+wY2+'" stroke="#94a3b8" stroke-width="3"/>';
 svg+='<text x="'+(lX+25)+'" y="'+(wY2+12)+'" fill="#94a3b8" font-size="7.5">Lower Capillary Wall (r = -R, v = 0 No-Slip)</text>';

 // Centerline dashed line
 const cY=(wY1+wY2)/2;
 svg+='<line x1="'+(lX+20)+'" y1="'+cY+'" x2="'+(lX+lW-20)+'" y2="'+cY+'" stroke="#334155" stroke-width="1" stroke-dasharray="3,3"/>';

 // Velocity profile arrows (parabolic curve)
 const vMaxPix=(v_mean/0.20)*130;
 for(let step=-5;step<=5;step++){
  const rFrac=step/5.0;
  const py=cY+rFrac*((wY2-wY1)/2 - 5);
  const vxLen=vMaxPix*(1 - rFrac*rFrac);
  if(vxLen>2){
   svg+='<line x1="'+(lX+50)+'" y1="'+py+'" x2="'+(lX+50+vxLen)+'" y2="'+py+'" stroke="#38bdf8" stroke-width="1.5"/>';
   svg+='<polygon points="'+(lX+50+vxLen)+','+(py-2.5)+' '+(lX+54+vxLen)+','+py+' '+(lX+50+vxLen)+','+(py+2.5)+'" fill="#38bdf8"/>';
  }
 }
 // Curve connecting arrow heads
 const pts=[];
 for(let s=-20;s<=20;s++){
  const rf=s/20.0;
  const y=cY+rf*((wY2-wY1)/2 - 5);
  const x=lX+54+vMaxPix*(1 - rf*rf);
  pts.push(x.toFixed(1)+','+y.toFixed(1));
 }
 svg+='<polyline points="'+pts.join(' ')+'" fill="none" stroke="#facc15" stroke-width="1.8"/>';

 // Data summary below velocity profile
 svg+='<rect x="'+(lX+15)+'" y="'+(lY+180)+'" width="'+(lW-30)+'" height="38" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(lX+25)+'" y="'+(lY+194)+'" fill="#789c80" font-size="7.5">Mean Velocity: v_mean = '+v_mean.toFixed(3)+' m/s  |  Max Velocity: v_max = '+(2*v_mean).toFixed(3)+' m/s</text>';
 svg+='<text x="'+(lX+25)+'" y="'+(lY+208)+'" fill="#86efac" font-size="7.5" font-family="monospace">v(r) = [ΔP/(4ηL)] · (R² - r²)  ⟹  Shear Rate at Wall γ̇_w = '+((4*v_mean)/0.00025).toFixed(0)+' s⁻¹</text>';


 // Right Panel: Reynolds Number & End-Correction Analysis
 const rX=380,rY=46,rW=315,rH=230;
 svg+='<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">REYNOLDS CRITERION & HYDRODYNAMIC AUDIT</text>';

 const errItems=[
  {label:'Reynolds Number',desc:'Re = (2·r·v·ρ)/η = '+reynolds.toFixed(1)+' ≪ 2000',val:'Strictly Laminar Flow',col:'#48bb78'},
  {label:'Couette End-Losses',desc:'Entrance length L_e ≈ 0.22 cm ≪ 15 cm (L/r = 600)',val:'< 0.2% Dissipation',col:'#38bdf8'},
  {label:'Radius Sensitivity (r⁴)',desc:'δr/r = 0.4% propagates as 4·(δr/r) = 1.6%',val:'Calibrated to ±0.001 mm',col:'#f87171'},
  {label:'Thermal Gradient (T)',desc:'∂η/∂T ≈ -2.5%/°C near 20.0 °C',val:'Thermostated ±0.05 °C',col:'#fbbf24'},
  {label:'OLS Slope Insulation (★)',desc:'Residual meniscus pressure absorbed into Q₀',val:'Slope = 0.05995 Unbiased',col:'#86efac'}
 ];

 errItems.forEach((ei,idx)=>{
  const ey=rY+30+idx*39;
  svg+='<rect x="'+(rX+8)+'" y="'+ey+'" width="'+(rW-16)+'" height="33" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+12)+'" fill="'+ei.col+'" font-size="7.5" font-weight="bold">'+ei.label+'</text>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+25)+'" fill="#94a3b8" font-size="6.8">'+ei.desc+'</text>';
  svg+='<text x="'+(rX+rW-14)+'" y="'+(ey+12)+'" text-anchor="end" fill="'+ei.col+'" font-size="7.5" font-family="monospace">'+ei.val+'</text>';
 });

 svg+=text(360,305,'Laminar Invariant: Reynolds number Re = '+reynolds.toFixed(1)+' guarantees pure Poiseuille streamline shear.','#789c80',9);
 return svg;
}
