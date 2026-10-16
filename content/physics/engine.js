'use strict';
const cfg=JSON.parse(document.getElementById('labConfig').textContent),model=window.PhysicsModels,$=id=>document.getElementById(id);
const fmt=(v,n=4)=>Math.abs(v)>0&&(Math.abs(v)<.001||Math.abs(v)>=1e6)?v.toExponential(3):v.toFixed(n);
let rows=[],measurement=null,busy=false,paused=matchMedia('(prefers-reduced-motion: reduce)').matches,clearPending=false;
try{const saved=JSON.parse(localStorage.getItem('openstemlab-'+cfg.slug+'-v1')||'[]');if(Array.isArray(saved))rows=saved.filter(r=>r&&Number.isFinite(r.input)&&r.input>=cfg.min&&r.input<=cfg.max&&Number.isFinite(r.raw)&&r.raw>0&&Number.isFinite(r.angle)&&r.angle<=5).slice(0,100).map(r=>model.reading(cfg.slug,r.input,r.raw,r.angle));}catch{}
function params(){return{input:+$('independent').value,angle:$('angle')?+$('angle').value:3,screen:$('screen')?+$('screen').value:0,balance:$('balance')?+$('balance').value:50};}
function message(text,error=false){$('trialStatus').textContent=text;$('trialStatus').classList.toggle('error',error);}
function update(){const p=params();measurement=null;$('independentOut').textContent=p.input.toFixed(cfg.inputDecimals)+' '+cfg.inputUnit;if($('angleOut'))$('angleOut').textContent=p.angle+'°';if($('balanceOut'))$('balanceOut').textContent=p.balance.toFixed(1)+' cm';if($('screenOut'))$('screenOut').textContent=p.screen.toFixed(1)+' cm';$('readingValue').textContent='—';$('recordReading').disabled=true;$('measure').disabled=busy;$('liveState').textContent=(cfg.slug==='convex-lens'?'Move the screen to form a sharp image.':p.angle>5&&cfg.angle?'Large amplitude: outside the measurement range.':'Ready for a virtual observation.');message('Adjust the apparatus, then take a reading.');draw(performance.now());}
$('independent').addEventListener('input',()=>{$('independentNumber').value=$('independent').value;update();});
$('independentNumber').addEventListener('input',()=>{const v=+$('independentNumber').value;if($('independentNumber').value!==''&&Number.isFinite(v)&&v>=cfg.min&&v<=cfg.max){$('independent').value=v;update();}});
$('independentNumber').addEventListener('change',()=>{const v=+$('independentNumber').value;if(!Number.isFinite(v)||v<cfg.min||v>cfg.max){$('independentNumber').value=$('independent').value;message('Use a value between '+cfg.min+' and '+cfg.max+' '+cfg.inputUnit+'.',true);return;}$('independent').value=v;$('independentNumber').value=$('independent').value;update();});
['angle','screen','balance'].forEach(id=>{if($(id))$(id).addEventListener('input',update);});
$('pauseMotion').hidden=!['simple-pendulum','bifilar-suspension','stokes-viscosity','ohms-law'].includes(cfg.slug);
$('pauseMotion').onclick=()=>{paused=!paused;$('pauseMotion').textContent=paused?'Resume motion':'Pause motion';};$('pauseMotion').textContent=paused?'Resume motion':'Pause motion';
$('resetApparatus').onclick=()=>{if(busy)return;$('independent').value=cfg.initial;$('independentNumber').value=cfg.initial;if($('angle'))$('angle').value=3;if($('screen'))$('screen').value=30;if($('balance'))$('balance').value=50;update();message('Apparatus reset. Your notebook is kept.');};
$('measure').onclick=async()=>{if(busy)return;const p=params(),prediction=model.predict(cfg.slug,p.input,p.angle);if(!prediction.valid){message(cfg.angle?'Use an angle of 5° or less for the measurement series.':'Choose a valid whole-number order.',true);return;}if(rows.length&&cfg.angle&&rows[0].angle!==p.angle){message('Keep amplitude fixed throughout this notebook. Restore '+rows[0].angle+'° or start a new series.',true);return;}
 if(cfg.slug==='convex-lens'&&Math.abs(p.screen-prediction.ideal)>.050001){message('The screen is out of focus. Adjust its position until the inverted image is sharp, then check again.',true);return;}
 if(cfg.slug==='metre-bridge'&&Math.abs(p.balance-prediction.ideal)>.050001){message('The bridge is not balanced. Move the jockey until the galvanometer is at null, then check again.',true);return;}
 busy=true;$('measure').disabled=true;$('recordReading').disabled=true;['independent','independentNumber','angle','screen','balance'].forEach(id=>{if($(id))$(id).disabled=true;});
 if(cfg.timed){message('Virtual trial running… physical time is accelerated for this teaching model.');await new Promise(resolve=>setTimeout(resolve,1400));}
 const raw=cfg.slug==='convex-lens'?p.screen:cfg.slug==='metre-bridge'?p.balance:prediction.raw;measurement=model.reading(cfg.slug,p.input,raw,p.angle);busy=false;['independent','independentNumber','angle','screen','balance'].forEach(id=>{if($(id))$(id).disabled=false;});$('measure').disabled=false;$('recordReading').disabled=false;$('readingValue').textContent=raw.toFixed(cfg.rawDecimals)+' '+cfg.rawUnit;$('liveState').textContent='Virtual observation ready to record.';message(cfg.timed?'Virtual '+cfg.observationLabel+' complete. Record the reading, then change '+cfg.shortInput+'.':'Reading obtained. Record it in your notebook.');};
$('recordReading').onclick=()=>{if(!measurement)return;if(rows.length>=100){message('Notebook full. Export readings or clear the notebook.',true);return;}rows.push({...measurement});measurement=null;$('recordReading').disabled=true;persist();message('Reading '+rows.length+' recorded. Change '+cfg.shortInput+' for the next observation.');};
function persist(){try{localStorage.setItem('openstemlab-'+cfg.slug+'-v1',JSON.stringify(rows));}catch{}renderResults();}
function renderResults(){const f=model.fit(rows);$('notebookCount').textContent=rows.length;$('emptyReadings').hidden=rows.length>0;$('downloadReadings').disabled=!rows.length;$('clearReadings').disabled=!rows.length;$('readingRows').innerHTML=rows.map((r,i)=>'<tr><td>'+(i+1)+'</td><td>'+r.input.toFixed(cfg.inputDecimals)+'</td><td>'+r.raw.toFixed(cfg.rawDecimals)+'</td><td>'+fmt(r.x*cfg.xScale)+'</td><td>'+fmt(r.y*cfg.yScale)+'</td><td><button class="text-button" data-remove="'+i+'" aria-label="Remove observation '+(i+1)+'">×</button></td></tr>').join('');document.querySelectorAll('[data-remove]').forEach(b=>b.onclick=()=>{rows.splice(+b.dataset.remove,1);persist();});
 if(f){const result=model.estimate(cfg.slug,f),pct=Math.abs(result.value-result.reference)/result.reference*100;$('fitSummary').innerHTML='<strong>'+fmt(result.value*cfg.resultScale,cfg.resultDecimals)+' '+cfg.resultUnit+'</strong><p>Estimated '+cfg.target+'<br>Gradient (SI): '+fmt(f.m)+'<br>Intercept (SI): '+fmt(f.b)+'<br>R²: '+f.r2.toFixed(5)+'<br>Difference from model value: '+pct.toFixed(3)+'%<br>Fit-only standard error: '+fmt(result.se*cfg.resultScale)+' '+cfg.resultUnit+'</p><p>Fit error is not a complete experimental uncertainty.</p>';}else $('fitSummary').innerHTML='<p>Record at least three distinct '+cfg.shortInput+' values to fit a line and calculate '+cfg.target+'.</p>';
 drawPlot(f);}
function drawPlot(f){const left=68,right=610,top=28,bottom=280;let xs=rows.map(r=>r.x*cfg.xScale),ys=rows.map(r=>r.y*cfg.yScale);let xmin=xs.length?Math.min(...xs):cfg.emptyX[0],xmax=xs.length?Math.max(...xs):cfg.emptyX[1],ymin=ys.length?Math.min(...ys):cfg.emptyY[0],ymax=ys.length?Math.max(...ys):cfg.emptyY[1];const dx=(xmax-xmin)||Math.max(Math.abs(xmax)*.2,1),dy=(ymax-ymin)||Math.max(Math.abs(ymax)*.2,1);xmin-=dx*.12;xmax+=dx*.12;ymin-=dy*.15;ymax+=dy*.15;const px=x=>left+(x-xmin)/(xmax-xmin)*(right-left),py=y=>bottom-(y-ymin)/(ymax-ymin)*(bottom-top);let svg='';for(let i=0;i<=4;i++){const x=xmin+i*(xmax-xmin)/4,y=ymin+i*(ymax-ymin)/4;svg+='<line x1="'+left+'" y1="'+py(y)+'" x2="'+right+'" y2="'+py(y)+'" stroke="#e2e7d8"/><text x="'+(left-9)+'" y="'+(py(y)+4)+'" text-anchor="end" font-size="10" fill="#768d68">'+fmt(y,2)+'</text><text x="'+px(x)+'" y="300" text-anchor="middle" font-size="10" fill="#768d68">'+fmt(x,2)+'</text>';}
 svg+='<path d="M'+left+' '+top+'V'+bottom+'H'+right+'" stroke="#9caf8c" fill="none"/><text x="335" y="332" text-anchor="middle" fill="#47683d" font-size="12">'+cfg.xAxis+'</text><text transform="translate(15 160) rotate(-90)" text-anchor="middle" fill="#47683d" font-size="12">'+cfg.yAxis+'</text>';
 if(f){const points=[];for(let i=0;i<=100;i++){const x=xmin+i*(xmax-xmin)/100,y=(f.m*x/cfg.xScale+f.b)*cfg.yScale;if(y>=ymin&&y<=ymax)points.push(px(x)+','+py(y));}svg+='<polyline points="'+points.join(' ')+'" stroke="#517b4c" stroke-width="2" fill="none"/>';}
 rows.forEach(r=>svg+='<circle cx="'+px(r.x*cfg.xScale)+'" cy="'+py(r.y*cfg.yScale)+'" r="4.8" fill="#b75632"><title>'+r.input.toFixed(cfg.inputDecimals)+' '+cfg.inputUnit+'</title></circle>');if(!rows.length)svg+='<text x="330" y="155" text-anchor="middle" fill="#8b9c7c" font-size="13">Your observations will appear here.</text>';$('labPlot').innerHTML=svg;}
$('downloadReadings').onclick=()=>{if(!rows.length)return;const csv=[['experiment','input_'+cfg.inputUnit,'observed_'+cfg.rawUnit,'x_SI','y_SI','amplitude_degrees'],...rows.map(r=>[cfg.slug,r.input,r.raw,r.x,r.y,cfg.angle?r.angle:''])].map(row=>row.join(',')).join('\r\n');const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download=cfg.slug+'-observations.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
$('clearReadings').onclick=()=>{if(!clearPending){clearPending=true;$('clearReadings').textContent='Confirm clear';setTimeout(()=>{clearPending=false;$('clearReadings').textContent='Clear notebook';},4000);return;}rows=[];clearPending=false;$('clearReadings').textContent='Clear notebook';persist();message('Notebook cleared.');};
$('checkEstimate').onclick=()=>{const f=model.fit(rows),answer=+$('studentEstimate').value;if(!f){$('estimateFeedback').textContent='Collect at least three distinct settings first.';return;}if(!$('studentEstimate').value||!Number.isFinite(answer)||answer<=0){$('estimateFeedback').textContent='Enter a positive numerical estimate in '+cfg.resultUnit+'.';return;}const expected=model.estimate(cfg.slug,f).value*cfg.resultScale;$('estimateFeedback').textContent=Math.abs(answer-expected)/expected<.02?'Your calculation agrees with the notebook fit within 2%. Explain your uncertainty separately.':'Recheck units and the gradient/intercept conversion. The fit gives '+fmt(expected,cfg.resultDecimals)+' '+cfg.resultUnit+'.';};
document.querySelectorAll('[data-quiz]').forEach(b=>b.onclick=()=>{const q=cfg.quiz[+b.dataset.quiz],j=+b.dataset.choice;document.querySelectorAll('[data-quiz="'+b.dataset.quiz+'"]').forEach(x=>x.classList.remove('correct','wrong'));b.classList.add(j===q.correct?'correct':'wrong');$('quizFeedback'+b.dataset.quiz).textContent=(j===q.correct?'Correct. ':'Think it through. ')+q.explanation;});
let currentSimMode='bench';
document.querySelectorAll('.sim-mode-btn').forEach(btn=>{
  btn.onclick=()=>{
    document.querySelectorAll('.sim-mode-btn').forEach(b=>{
      b.classList.remove('active');
      b.setAttribute('aria-selected','false');
    });
    btn.classList.add('active');
    btn.setAttribute('aria-selected','true');
    currentSimMode=btn.dataset.sim;
    draw(performance.now());
  };
});

function drawComparativeSim(t,p,v,phase,ink,soft,orange){
  const isGas=['boyles-law','charles-law-volume','charles-law-pressure','vapor-pressure','air-humidity'].includes(cfg.slug);
  const isHeat=['specific-heat-capacity','newtons-cooling','solidification-cooling','latent-heat-vaporization','latent-heat-fusion','thermal-expansion','mechanical-equivalent-heat'].includes(cfg.slug);
  const isOptics=['convex-lens','glass-slab','diffraction-grating'].includes(cfg.slug);
  const isElec=['ohms-law','metre-bridge','rc-charging'].includes(cfg.slug);
  const isSound=['resonance-air-column','modes-air-column','vibration-strings-sonometer','interference-sound-waves'].includes(cfg.slug);
  const isElectrostatic=['electrostatics'].includes(cfg.slug);
  const isMagnetic=['magnetic-fields'].includes(cfg.slug);
  const isFieldMapping=['electric-fields'].includes(cfg.slug);
  const isMagMoments=['magnetic-moments'].includes(cfg.slug);
  const isInternalR=['internal-resistance'].includes(cfg.slug);
  const isTempR=['temperature-resistance'].includes(cfg.slug);
  const isFaraday=['faradays-law-electrolysis'].includes(cfg.slug);
  const isElecHeat=['electrical-equivalent-heat'].includes(cfg.slug);
  const isPotentiometer=['potentiometer-emf-comparison'].includes(cfg.slug);
  const isSpectra=['emission-spectra-spectroscopy'].includes(cfg.slug);
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#9fb498',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  if(isGas){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'MULTI-GAS EQUATION OF STATE COMPARISON','#e2ecd7',11);
    svg+='<line x1="'+(gX+40)+'" y1="'+(gY+gH-30)+'" x2="'+(gX+gW-20)+'" y2="'+(gY+gH-30)+'" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<line x1="'+(gX+40)+'" y1="'+(gY+25)+'" x2="'+(gX+40)+'" y2="'+(gY+gH-30)+'" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+=text(gX+gW/2,gY+gH-10,'Specific Volume v (m³ / kg)',soft,9);
    svg+='<text transform="translate('+(gX+16)+','+(gY+gH/2)+') rotate(-90)" text-anchor="middle" fill="'+soft+'" font-size="9">Pressure P (kPa)</text>';

    let pAir=[],pCO2=[],pHe=[];
    for(let i=0;i<=60;i++){
      const vol=0.05+i*(0.45/60);
      const px=gX+45+(i/60)*(gW-75);
      const yAir=gY+gH-35-Math.min(gH-55,(2.8/vol)*2.2);
      const yCO2=gY+gH-35-Math.min(gH-55,((2.8/vol)*0.95-(0.364/(vol*vol))*0.04)*2.2);
      const yHe=gY+gH-35-Math.min(gH-55,(2.8/vol)*1.08*2.2);
      pAir.push(px.toFixed(1)+','+yAir.toFixed(1));
      pCO2.push(px.toFixed(1)+','+yCO2.toFixed(1));
      pHe.push(px.toFixed(1)+','+yHe.toFixed(1));
    }
    svg+='<polyline points="'+pAir.join(' ')+'" fill="none" stroke="'+ink+'" stroke-width="2"/>';
    svg+='<polyline points="'+pCO2.join(' ')+'" fill="none" stroke="'+orange+'" stroke-width="2"/>';
    svg+='<polyline points="'+pHe.join(' ')+'" fill="none" stroke="#38bdf8" stroke-width="2"/>';

    const currVolNorm=(p.input-cfg.min)/(cfg.max-cfg.min);
    const curX=gX+45+Math.max(0,Math.min(1,currVolNorm))*(gW-75);
    svg+='<line x1="'+curX+'" y1="'+(gY+25)+'" x2="'+curX+'" y2="'+(gY+gH-30)+'" stroke="#fde68a" stroke-dasharray="3 3"/>';

    svg+='<rect x="'+(gX+gW-125)+'" y="'+(gY+32)+'" width="115" height="55" rx="3" fill="#182824" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<line x1="'+(gX+gW-115)+'" y1="'+(gY+44)+'" x2="'+(gX+gW-95)+'" y2="'+(gY+44)+'" stroke="'+ink+'" stroke-width="2"/>';
    svg+=text(gX+gW-55,gY+47,'Air (Diatomic)',ink,8.5);
    svg+='<line x1="'+(gX+gW-115)+'" y1="'+(gY+58)+'" x2="'+(gX+gW-95)+'" y2="'+(gY+58)+'" stroke="'+orange+'" stroke-width="2"/>';
    svg+=text(gX+gW-55,gY+61,'CO₂ (van der Waals)',orange,8.5);
    svg+='<line x1="'+(gX+gW-115)+'" y1="'+(gY+72)+'" x2="'+(gX+gW-95)+'" y2="'+(gY+72)+'" stroke="#38bdf8" stroke-width="2"/>';
    svg+=text(gX+gW-55,gY+75,'He (Monatomic)','#38bdf8',8.5);

    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'GAS PROPERTY MATRIX','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';

    const gases=[
      {name:'Air (N₂/O₂)',m:'28.97 g/mol',gamma:'1.400',z:'0.999',col:ink},
      {name:'Carbon Dioxide (CO₂)',m:'44.01 g/mol',gamma:'1.289',z:'0.992',col:orange},
      {name:'Helium (He)',m:'4.003 g/mol',gamma:'1.667',z:'1.001',col:'#38bdf8'}
    ];
    gases.forEach((g,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+g.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+g.col+'" font-size="11" font-weight="bold">'+g.name+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">M = '+g.m+' · γ = '+g.gamma+' · Z(P) = '+g.z+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,'Comparative Real vs Ideal Gas Thermodynamics · Isothermal Compression & Expansion',soft,10);
  }
  else if(isHeat){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'THERMAL RESPONSE CURVES BY MATERIAL','#e2ecd7',11);
    svg+='<line x1="'+(gX+40)+'" y1="'+(gY+gH-30)+'" x2="'+(gX+gW-20)+'" y2="'+(gY+gH-30)+'" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<line x1="'+(gX+40)+'" y1="'+(gY+25)+'" x2="'+(gX+40)+'" y2="'+(gY+gH-30)+'" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+=text(gX+gW/2,gY+gH-10,'Elapsed Time / Input Energy',soft,9);
    svg+='<text transform="translate('+(gX+16)+','+(gY+gH/2)+') rotate(-90)" text-anchor="middle" fill="'+soft+'" font-size="9">Temperature Rise ΔT (°C)</text>';

    let pCu=[],pAl=[],pFe=[];
    for(let i=0;i<=60;i++){
      const frac=i/60;
      const px=gX+45+frac*(gW-75);
      const yCu=gY+gH-35-Math.min(gH-55,frac*145);
      const yFe=gY+gH-35-Math.min(gH-55,frac*115);
      const yAl=gY+gH-35-Math.min(gH-55,frac*75);
      pCu.push(px.toFixed(1)+','+yCu.toFixed(1));
      pFe.push(px.toFixed(1)+','+yFe.toFixed(1));
      pAl.push(px.toFixed(1)+','+yAl.toFixed(1));
    }
    svg+='<polyline points="'+pCu.join(' ')+'" fill="none" stroke="'+orange+'" stroke-width="2"/>';
    svg+='<polyline points="'+pFe.join(' ')+'" fill="none" stroke="'+ink+'" stroke-width="2"/>';
    svg+='<polyline points="'+pAl.join(' ')+'" fill="none" stroke="#38bdf8" stroke-width="2"/>';

    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'THERMAL SPECIMEN PROPERTIES','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';

    const metals=[
      {name:'Copper (Cu)',c:'385 J kg⁻¹ K⁻¹',alpha:'16.8 × 10⁻⁶ K⁻¹',col:orange},
      {name:'Iron / Steel (Fe)',c:'450 J kg⁻¹ K⁻¹',alpha:'11.8 × 10⁻⁶ K⁻¹',col:ink},
      {name:'Aluminum (Al)',c:'900 J kg⁻¹ K⁻¹',alpha:'23.1 × 10⁻⁶ K⁻¹',col:'#38bdf8'}
    ];
    metals.forEach((m,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+m.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+m.col+'" font-size="11" font-weight="bold">'+m.name+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">c = '+m.c+' · α = '+m.alpha+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,'Thermal Properties: Calorimetry, Heat Transfer, and Phase Transition Dynamics',soft,10);
  }
  else if(isOptics){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'SNELL\'S REFRACTION & DISPERSION RAYS','#e2ecd7',11);

    const midX=gX+170;
    svg+='<line x1="'+midX+'" y1="'+gY+'" x2="'+midX+'" y2="'+(gY+gH)+'" stroke="'+soft+'" stroke-width="2"/>';
    svg+=text(midX-60,gY+25,'Air (n = 1.00)',soft,9);
    svg+=text(midX+60,gY+25,'Medium',soft,9);
    svg+='<line x1="'+(gX+20)+'" y1="'+(gY+gH/2)+'" x2="'+(gX+gW-20)+'" y2="'+(gY+gH/2)+'" stroke="'+soft+'" stroke-dasharray="3 3"/>';

    const incY=gY+gH/2-70;
    svg+='<line x1="'+(midX-70)+'" y1="'+incY+'" x2="'+midX+'" y2="'+(gY+gH/2)+'" stroke="#fde68a" stroke-width="2.5"/>';
    svg+=text(midX-45,incY+30,'θ₁ = 45°','#fde68a',9);

    const rCrown=27.7*Math.PI/180,rFlint=25.2*Math.PI/180,rDia=17.0*Math.PI/180;
    const len=120;
    svg+='<line x1="'+midX+'" y1="'+(gY+gH/2)+'" x2="'+(midX+len*Math.cos(rCrown))+'" y2="'+(gY+gH/2+len*Math.sin(rCrown))+'" stroke="'+ink+'" stroke-width="2"/>';
    svg+='<line x1="'+midX+'" y1="'+(gY+gH/2)+'" x2="'+(midX+len*Math.cos(rFlint))+'" y2="'+(gY+gH/2+len*Math.sin(rFlint))+'" stroke="'+orange+'" stroke-width="2"/>';
    svg+='<line x1="'+midX+'" y1="'+(gY+gH/2)+'" x2="'+(midX+len*Math.cos(rDia))+'" y2="'+(gY+gH/2+len*Math.sin(rDia))+'" stroke="#38bdf8" stroke-width="2"/>';

    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'OPTICAL MEDIA CHARACTERISTICS','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';

    const media=[
      {name:'Crown Glass (BK7)',n:'1.5168',cA:'41.2°',col:ink},
      {name:'Dense Flint (SF11)',n:'1.6644',cA:'36.9°',col:orange},
      {name:'Natural Diamond',n:'2.4175',cA:'24.4°',col:'#38bdf8'}
    ];
    media.forEach((m,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+m.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+m.col+'" font-size="11" font-weight="bold">'+m.name+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">n = '+m.n+' · Critical θ_c = '+m.cA+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,'Snell\'s Law of Refraction: n₁ sin(θ₁) = n₂ sin(θ₂) · Total Internal Reflection',soft,10);
  }
  else if(isElec){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'V-I CHARACTERISTIC CURVES (OHMIC VS NON-OHMIC)','#e2ecd7',11);
    svg+='<line x1="'+(gX+40)+'" y1="'+(gY+gH-30)+'" x2="'+(gX+gW-20)+'" y2="'+(gY+gH-30)+'" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<line x1="'+(gX+40)+'" y1="'+(gY+25)+'" x2="'+(gX+40)+'" y2="'+(gY+gH-30)+'" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+=text(gX+gW/2,gY+gH-10,'Voltage V (Volts)',soft,9);
    svg+='<text transform="translate('+(gX+16)+','+(gY+gH/2)+') rotate(-90)" text-anchor="middle" fill="'+soft+'" font-size="9">Current I (mA)</text>';

    let pRes=[],pLamp=[],pDiode=[];
    for(let i=0;i<=60;i++){
      const vVal=(i/60)*10;
      const px=gX+45+(i/60)*(gW-75);
      const yRes=gY+gH-35-Math.min(gH-55,(vVal/10)*120);
      const yLamp=gY+gH-35-Math.min(gH-55,Math.pow(vVal/10,0.65)*140);
      const iDiode=vVal<6?0:Math.exp((vVal-6)*0.7)*4;
      const yDiode=gY+gH-35-Math.min(gH-55,iDiode);
      pRes.push(px.toFixed(1)+','+yRes.toFixed(1));
      pLamp.push(px.toFixed(1)+','+yLamp.toFixed(1));
      pDiode.push(px.toFixed(1)+','+yDiode.toFixed(1));
    }
    svg+='<polyline points="'+pRes.join(' ')+'" fill="none" stroke="'+ink+'" stroke-width="2"/>';
    svg+='<polyline points="'+pLamp.join(' ')+'" fill="none" stroke="'+orange+'" stroke-width="2"/>';
    svg+='<polyline points="'+pDiode.join(' ')+'" fill="none" stroke="#38bdf8" stroke-width="2"/>';

    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'CONDUCTION BEHAVIOR','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';

    const elecs=[
      {name:'Ohmic Resistor',r:'Constant R = 100 Ω',col:ink},
      {name:'Tungsten Lamp',r:'R(T) increases with heat',col:orange},
      {name:'Silicon PN Diode',r:'Forward threshold V_th ≈ 0.7V',col:'#38bdf8'}
    ];
    elecs.forEach((m,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+m.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+m.col+'" font-size="11" font-weight="bold">'+m.name+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">'+m.r+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,'Electrical Transport: Constant vs Temperature-Dependent Dynamic Resistance',soft,10);
  }
  else if(isSound){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'ACOUSTIC WAVE PROPAGATION ACROSS GASES & MEDIA','#e2ecd7',11);
    const media=[
      {name:'Helium Gas (He)',v:965,col:'#38bdf8',type:'Gas · γ=1.67, M=4.0 g/mol'},
      {name:'Dry Air (20°C)',v:343,col:ink,type:'Gas · γ=1.40, M=29.0 g/mol'},
      {name:'Carbon Dioxide (CO₂)',v:267,col:orange,type:'Gas · γ=1.30, M=44.0 g/mol'}
    ];
    media.forEach((m,idx)=>{
      const rowY=gY+35+idx*55;
      svg+='<text x="'+(gX+18)+'" y="'+(rowY-8)+'" fill="'+m.col+'" font-size="10" font-weight="bold">'+m.name+'</text>';
      svg+='<text x="'+(gX+gW-18)+'" y="'+(rowY-8)+'" text-anchor="end" fill="'+m.col+'" font-size="10" font-family="monospace">'+m.v+' m/s</text>';
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+(gW-36)+'" height="14" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
      const barW=((m.v/1000)*(gW-36)).toFixed(1);
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+barW+'" height="14" rx="3" fill="'+m.col+'"/>';
      const pulseX=gX+18+((phase*(m.v/300))%1)*(gW-36);
      svg+='<circle cx="'+pulseX.toFixed(1)+'" cy="'+(rowY+7)+'" r="4.5" fill="#fde68a" stroke="#fff" stroke-width="1"/>';
      svg+='<text x="'+(gX+22)+'" y="'+(rowY+26)+'" fill="#9fb498" font-size="8">'+m.type+'</text>';
    });
    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'ACOUSTIC IMPEDANCE & MODULUS','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    const acStats=[
      {mat:'Air (20°C, 1 atm)',z:'415 Pa·s/m',k:'142 kPa',col:ink},
      {mat:'Water (Fresh, 20°C)',z:'1.48 × 10⁶ Pa·s/m',k:'2.20 GPa',col:'#38bdf8'},
      {mat:'Steel (Structural)',z:'4.05 × 10⁷ Pa·s/m',k:'160 GPa',col:orange}
    ];
    acStats.forEach((s,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+s.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+s.col+'" font-size="11" font-weight="bold">'+s.mat+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">Z = '+s.z+' · K = '+s.k+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,'Laplace Sound Speed: v = √(γRT/M) = √(K/ρ) · Radiation Mismatch Z_water >> Z_air',soft,10);
  }
  else if(isElectrostatic){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'DIELECTRIC SCREENING & COULOMB FORCE ATTENUATION (F = F₀ / κ)','#e2ecd7',11);
    const media=[
      {name:'Vacuum / Dry Air (κ = 1.00)',factor:1.0,fVal:'1438.0 μN',col:ink,desc:'ε = ε₀ = 8.85 pF/m · Zero Screening'},
      {name:'Mica / Glass (κ = 6.00)',factor:6.0,fVal:'239.7 μN',col:orange,desc:'ε = 6.0 ε₀ = 53.1 pF/m · Strong Polarization'},
      {name:'Pure Water (20°C, κ = 80.1)',factor:80.1,fVal:'18.0 μN',col:'#38bdf8',desc:'ε = 80.1 ε₀ = 709 pF/m · Massive Dipole Shield'}
    ];
    media.forEach((m,idx)=>{
      const rowY=gY+35+idx*55;
      svg+='<text x="'+(gX+18)+'" y="'+(rowY-8)+'" fill="'+m.col+'" font-size="10" font-weight="bold">'+m.name+'</text>';
      svg+='<text x="'+(gX+gW-18)+'" y="'+(rowY-8)+'" text-anchor="end" fill="'+m.col+'" font-size="10" font-family="monospace">F = '+m.fVal+'</text>';
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+(gW-36)+'" height="14" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
      const barW=((1.0/m.factor)*(gW-36)).toFixed(1);
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+barW+'" height="14" rx="3" fill="'+m.col+'"/>';
      const pulseX=gX+18+((phase*(3.0/m.factor))%1)*(gW-36);
      svg+='<circle cx="'+pulseX.toFixed(1)+'" cy="'+(rowY+7)+'" r="4.5" fill="#fde68a" stroke="#fff" stroke-width="1"/>';
      svg+='<text x="'+(gX+22)+'" y="'+(rowY+26)+'" fill="#9fb498" font-size="8">'+m.desc+'</text>';
    });
    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'DIELECTRIC CONSTANT & BREAKDOWN FIELD','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    const dStats=[
      {mat:'Dry Air (1 atm, 20°C)',k:'κ = 1.0006',bd:'E_b = 3.0 MV/m',col:ink},
      {mat:'Pyrex Glass (Plate)',k:'κ = 5.60',bd:'E_b = 14.0 MV/m',col:orange},
      {mat:'Distilled Water (Pure)',k:'κ = 80.1',bd:'E_b = 65.0 MV/m',col:'#38bdf8'}
    ];
    dStats.forEach((s,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+s.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+s.col+'" font-size="11" font-weight="bold">'+s.mat+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">'+s.k+' · '+s.bd+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,'Coulomb Law in Matter: F = (1 / 4πε₀κ) (q₁q₂ / r²) · Polarization P⃗ = ε₀(κ − 1)E⃗',soft,10);
  }
  else if(isMagnetic){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'GEOMAGNETIC LATITUDE & COMPONENT DECOMPOSITION (B_H, B_V, I_d)','#e2ecd7',11);
    const stations=[
      {loc:'Magnetic Equator (0° Lat)',bh:'39.0 μT',bv:'0.0 μT',dip:'0.0°',kVal:'124.1 mA',col:ink,desc:'Pure horizontal field · Maximal galvanometer torque'},
      {loc:'Mid-Latitude Lab (45° Lat)',bh:'35.0 μT',bv:'42.0 μT',dip:'50.2°',kVal:'111.4 mA',col:orange,desc:'Standard reference station · Moderate dip angle'},
      {loc:'High Sub-Polar (70° Lat)',bh:'14.0 μT',bv:'52.0 μT',dip:'74.9°',kVal:'44.6 mA',col:'#38bdf8',desc:'Steep vertical dip · Compressed reduction factor'}
    ];
    stations.forEach((st,idx)=>{
      const rowY=gY+35+idx*55;
      svg+='<text x="'+(gX+18)+'" y="'+(rowY-8)+'" fill="'+st.col+'" font-size="10" font-weight="bold">'+st.loc+'</text>';
      svg+='<text x="'+(gX+gW-18)+'" y="'+(rowY-8)+'" text-anchor="end" fill="'+st.col+'" font-size="10" font-family="monospace">B_H = '+st.bh+' (Dip '+st.dip+')</text>';
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+(gW-36)+'" height="14" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
      const bhNum=parseFloat(st.bh);
      const barW=((bhNum/45.0)*(gW-36)).toFixed(1);
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+barW+'" height="14" rx="3" fill="'+st.col+'"/>';
      const pulseX=gX+18+((phase*(bhNum/20.0))%1)*(gW-36);
      svg+='<circle cx="'+pulseX.toFixed(1)+'" cy="'+(rowY+7)+'" r="4.5" fill="#fde68a" stroke="#fff" stroke-width="1"/>';
      svg+='<text x="'+(gX+22)+'" y="'+(rowY+26)+'" fill="#9fb498" font-size="8">'+st.desc+' · K = '+st.kVal+'</text>';
    });
    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'MAGNETIC INCLINATION & TOTAL FIELD B','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    const geoStats=[
      {zone:'Equatorial Zone',tot:'B = 39.0 μT',tanDip:'tan I_d = 0.00',col:ink},
      {zone:'Mid-Latitude Zone',tot:'B = 54.7 μT',tanDip:'tan I_d = 1.20',col:orange},
      {zone:'Polar Circle Zone',tot:'B = 53.8 μT',tanDip:'tan I_d = 3.71',col:'#38bdf8'}
    ];
    geoStats.forEach((s,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+s.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+s.col+'" font-size="11" font-weight="bold">'+s.zone+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">'+s.tot+' · '+s.tanDip+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,'Tangent Law: B_coil = B_H tan θ ⇔ I = K tan θ · Reduction Factor K = 2 R B_H / (μ₀ N)',soft,10);
  }
  else if(isFieldMapping){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'ELECTRODE GEOMETRY & POTENTIAL GRADIENT PROFILES (V vs x)','#e2ecd7',11);
    const geos=[
      {name:'Parallel Planar Plates',law:'Linear V(x) = E · x',eField:'E = 100.0 V/m (Uniform)',col:ink,desc:'Equidistant parallel planar equipotentials · Zero curvature'},
      {name:'Coaxial Cylindrical Rings',law:'Logarithmic V(r) ∝ ln(r)',eField:'E(r) ∝ 1/r (Cylindrical)',col:orange,desc:'Concentric circular equipotentials · Crowding near center pin'},
      {name:'Point Charge Dipole (+ / −)',law:'Dipole V ∝ cos θ / r²',eField:'E ∝ 1/r³ (Dipole axis)',col:'#38bdf8',desc:'Apollonian orthogonal curves · Strong polar field concentration'}
    ];
    geos.forEach((g,idx)=>{
      const rowY=gY+35+idx*55;
      svg+='<text x="'+(gX+18)+'" y="'+(rowY-8)+'" fill="'+g.col+'" font-size="10" font-weight="bold">'+g.name+'</text>';
      svg+='<text x="'+(gX+gW-18)+'" y="'+(rowY-8)+'" text-anchor="end" fill="'+g.col+'" font-size="10" font-family="monospace">'+g.eField+'</text>';
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+(gW-36)+'" height="14" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
      const barW=(idx===0?(gW-36):idx===1?(gW-36)*0.75:(gW-36)*0.55).toFixed(1);
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+barW+'" height="14" rx="3" fill="'+g.col+'"/>';
      const pulseX=gX+18+((phase*(2.0+idx*0.8))%1)*(gW-36);
      svg+='<circle cx="'+pulseX.toFixed(1)+'" cy="'+(rowY+7)+'" r="4.5" fill="#fde68a" stroke="#fff" stroke-width="1"/>';
      svg+='<text x="'+(gX+22)+'" y="'+(rowY+26)+'" fill="#9fb498" font-size="8">'+g.desc+' · '+g.law+'</text>';
    });
    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'SPATIAL LAPLACE POTENTIAL LAWS','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    const topStats=[
      {geo:'Parallel Plates (1D)',lap:'d²V/dx² = 0',grad:'E = −dV/dx = const',col:ink},
      {geo:'Cylinders (2D Polar)',lap:'(1/r) d/dr(r dV/dr) = 0',grad:'E = −(V₀/ln(r₂/r₁)) (1/r)',col:orange},
      {geo:'Point Dipole (3D Spherical)',lap:'∇²V = 0 (r > 0)',grad:'E_axial = 2k_e p / r³',col:'#38bdf8'}
    ];
    topStats.forEach((s,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+s.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+s.col+'" font-size="11" font-weight="bold">'+s.geo+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">'+s.lap+' · '+s.grad+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,'Orthogonality Law: E⃗ ⊥ Equipotential Surfaces (E⃗ · dℓ⃗ ≡ 0) · Field Density |E| ∝ 1 / Δs',soft,10);
  }
  else if(isMagMoments){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'MAGNET MATERIAL & ORIENTATION DEFLECTION PROFILES','#e2ecd7',11);
    const mags=[
      {mat:'Alnico V (Tan-A End-On)',moment:'M = 0.875 A m²',def:'θ = 40.6° (at d=18cm)',col:ink,desc:'High coercivity cast alloy · Tan-A axial dipole field'},
      {mat:'Cobalt Steel (Tan-A End-On)',moment:'M = 0.525 A m²',def:'θ = 27.2° (at d=18cm)',col:orange,desc:'Classic quench-hardened magnet · 60% dipole moment'},
      {mat:'Alnico V (Tan-B Broadside)',moment:'M = 0.875 A m²',def:'θ = 23.3° (at d=18cm)',col:'#38bdf8',desc:'Equatorial broadside orientation · Exactly half field B_B = ½ B_A'}
    ];
    mags.forEach((m,idx)=>{
      const rowY=gY+35+idx*55;
      svg+='<text x="'+(gX+18)+'" y="'+(rowY-8)+'" fill="'+m.col+'" font-size="10" font-weight="bold">'+m.mat+'</text>';
      svg+='<text x="'+(gX+gW-18)+'" y="'+(rowY-8)+'" text-anchor="end" fill="'+m.col+'" font-size="10" font-family="monospace">'+m.moment+'</text>';
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+(gW-36)+'" height="14" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
      const barW=(idx===0?(gW-36):idx===1?(gW-36)*0.60:(gW-36)*0.50).toFixed(1);
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+barW+'" height="14" rx="3" fill="'+m.col+'"/>';
      const pulseX=gX+18+((phase*(2.0+idx*0.7))%1)*(gW-36);
      svg+='<circle cx="'+pulseX.toFixed(1)+'" cy="'+(rowY+7)+'" r="4.5" fill="#fde68a" stroke="#fff" stroke-width="1"/>';
      svg+='<text x="'+(gX+22)+'" y="'+(rowY+26)+'" fill="#9fb498" font-size="8">'+m.desc+' · '+m.def+'</text>';
    });
    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'GAUSS TAN-A VS TAN-B DIPOLES','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    const topStats=[
      {pos:'Tan-A (End-On Position)',ratio:'B_A = (μ₀/4π) (2M/d³)',tan:'tan θ_A = 2(μ₀/4π) M / (B_H d³)',col:ink},
      {pos:'Tan-B (Broadside Position)',ratio:'B_B = (μ₀/4π) (M/d³)',tan:'tan θ_B = (μ₀/4π) M / (B_H d³)',col:orange},
      {pos:'Gauss Axial Ratio',ratio:'B_A / B_B ≡ 2.000',tan:'tan θ_A / tan θ_B ≡ 2.000',col:'#38bdf8'}
    ];
    topStats.forEach((s,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+s.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+s.col+'" font-size="11" font-weight="bold">'+s.pos+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">'+s.ratio+' · '+s.tan+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,'Gauss Tan-A Dipole Law: B_A = (μ₀/4π) [2Md / (d² − ℓ²)²] ≈ (μ₀/4π) (2M / d³) = B_H tan θ',soft,10);
  }
  else if(isInternalR){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'CELL ELECTROCHEMICAL CHEMISTRY & IMPEDANCE PROFILES','#e2ecd7',11);
    const cells=[
      {type:'Fresh Alkaline AA (Zn/MnO₂)',emf:'ℰ = 1.50V',rVal:'r = 0.15 Ω',iSc:'I_sc = 10.0 A',col:ink,desc:'High ionic mobility KOH electrolyte · Negligible voltage drop'},
      {type:'Leclanché Primary (NH₄Cl)',emf:'ℰ = 1.50V',rVal:'r = 2.50 Ω',iSc:'I_sc = 0.60 A',col:orange,desc:'Standard laboratory cell · Linear ohmic internal loss'},
      {type:'Aged Carbon-Zinc Cell',emf:'ℰ = 1.30V',rVal:'r = 8.50 Ω',iSc:'I_sc = 0.15 A',col:'#38bdf8',desc:'Depleted electrolyte paste · Severe voltage collapse under load'}
    ];
    cells.forEach((c,idx)=>{
      const rowY=gY+35+idx*55;
      svg+='<text x="'+(gX+18)+'" y="'+(rowY-8)+'" fill="'+c.col+'" font-size="10" font-weight="bold">'+c.type+'</text>';
      svg+='<text x="'+(gX+gW-18)+'" y="'+(rowY-8)+'" text-anchor="end" fill="'+c.col+'" font-size="10" font-family="monospace">'+c.rVal+' ('+c.emf+')</text>';
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+(gW-36)+'" height="14" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
      const barW=(idx===0?(gW-36)*0.15:idx===1?(gW-36)*0.55:(gW-36)*0.95).toFixed(1);
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+barW+'" height="14" rx="3" fill="'+c.col+'"/>';
      const pulseX=gX+18+((phase*(2.0+idx*0.7))%1)*(gW-36);
      svg+='<circle cx="'+pulseX.toFixed(1)+'" cy="'+(rowY+7)+'" r="4.5" fill="#fde68a" stroke="#fff" stroke-width="1"/>';
      svg+='<text x="'+(gX+22)+'" y="'+(rowY+26)+'" fill="#9fb498" font-size="8">'+c.desc+' · '+c.iSc+'</text>';
    });
    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'MAXIMUM POWER & SHORT CIRCUIT','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    const cellStats=[
      {name:'Fresh Alkaline AA',pMax:'P_max = 3.75 W',iShort:'I_sc = 10.0 A',col:ink},
      {name:'Leclanché Cell (r = 2.50Ω)',pMax:'P_max = 225.0 mW',iShort:'I_sc = 0.60 A',col:orange},
      {name:'Aged Carbon-Zinc',pMax:'P_max = 49.7 mW',iShort:'I_sc = 0.15 A',col:'#38bdf8'}
    ];
    cellStats.forEach((s,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+s.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+s.col+'" font-size="11" font-weight="bold">'+s.name+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">'+s.pMax+' · '+s.iShort+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,'Terminal Voltage: V = ℰ − I · r · Short-Circuit Current I_sc = ℰ / r · Max Power P_max = ℰ² / (4r)',soft,10);
  }
  else if(isTempR){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'CONDUCTIVE MATERIAL TEMPERATURE SENSITIVITY (α PROFILES)','#e2ecd7',11);
    const mats=[
      {mat:'Pure Annealed Copper (PTC)',alpha:'α = +3.93 × 10⁻³ °C⁻¹',r100:'R_100 = 139.3 Ω',col:ink,desc:'Standard metallic conductor · Linear electron-phonon scattering'},
      {mat:'Manganin Alloy (Zero-TC)',alpha:'α = +0.01 × 10⁻³ °C⁻¹',r100:'R_100 = 100.1 Ω',col:orange,desc:'Solid-solution impurity alloy · Temperature-invariant standard resistor'},
      {mat:'NTC Semiconductor Thermistor',alpha:'α = −40.0 × 10⁻³ °C⁻¹',r100:'R_100 = 12.5 Ω',col:'#38bdf8',desc:'Exponential thermal carrier generation · Massive negative sensitivity'}
    ];
    mats.forEach((m,idx)=>{
      const rowY=gY+35+idx*55;
      svg+='<text x="'+(gX+18)+'" y="'+(rowY-8)+'" fill="'+m.col+'" font-size="10" font-weight="bold">'+m.mat+'</text>';
      svg+='<text x="'+(gX+gW-18)+'" y="'+(rowY-8)+'" text-anchor="end" fill="'+m.col+'" font-size="10" font-family="monospace">'+m.alpha+'</text>';
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+(gW-36)+'" height="14" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
      const barW=(idx===0?(gW-36)*0.75:idx===1?(gW-36)*0.10:(gW-36)*0.95).toFixed(1);
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+barW+'" height="14" rx="3" fill="'+m.col+'"/>';
      const pulseX=gX+18+((phase*(2.0+idx*0.7))%1)*(gW-36);
      svg+='<circle cx="'+pulseX.toFixed(1)+'" cy="'+(rowY+7)+'" r="4.5" fill="#fde68a" stroke="#fff" stroke-width="1"/>';
      svg+='<text x="'+(gX+22)+'" y="'+(rowY+26)+'" fill="#9fb498" font-size="8">'+m.desc+' · '+m.r100+'</text>';
    });
    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'INFERRED ABSOLUTE ZERO & DRIFT','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    const matStats=[
      {name:'Pure Copper (R₀ = 100Ω)',tZero:'T_abs = −254.5 °C',drift:'+0.393 Ω/°C',col:ink},
      {name:'Platinum PT100 Sensor',tZero:'T_abs = −259.7 °C',drift:'+0.385 Ω/°C',col:orange},
      {name:'Manganin Standard Resistor',tZero:'T_abs = N/A (Stable)',drift:'±0.001 Ω/°C',col:'#38bdf8'}
    ];
    matStats.forEach((s,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+s.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+s.col+'" font-size="11" font-weight="bold">'+s.name+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">'+s.tZero+' · '+s.drift+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,'Resistance Law: R(T) = R₀(1 + α T) ⇔ α = (1/R₀)(dR/dT) · Inferred Absolute Zero: T_abs = −1 / α',soft,10);
  }
  else if(isFaraday){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'FARADAY 2ND LAW: MASS PER 1000 C CHARGE (M / n F)','#e2ecd7',11);
    const ions=[
      {ion:'Silver (Ag⁺, n = 1)',ece:'Z = 1.1180 mg/C',m1k:'m_1000 = 1118.0 mg',col:ink,desc:'Monovalent noble cation · Historical international standard ampere'},
      {ion:'Copper (Cu²⁺, n = 2)',ece:'Z = 0.3293 mg/C',m1k:'m_1000 = 329.3 mg',col:orange,desc:'Divalent transition cation · University laboratory reference standard'},
      {ion:'Aluminum (Al³⁺, n = 3)',ece:'Z = 0.0932 mg/C',m1k:'m_1000 = 93.2 mg',col:'#38bdf8',desc:'Trivalent light metal cation · 12× lower mass per Coulomb than silver'}
    ];
    ions.forEach((item,idx)=>{
      const rowY=gY+35+idx*55;
      svg+='<text x="'+(gX+18)+'" y="'+(rowY-8)+'" fill="'+item.col+'" font-size="10" font-weight="bold">'+item.ion+'</text>';
      svg+='<text x="'+(gX+gW-18)+'" y="'+(rowY-8)+'" text-anchor="end" fill="'+item.col+'" font-size="10" font-family="monospace">'+item.ece+'</text>';
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+(gW-36)+'" height="14" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
      const barW=(idx===0?(gW-36)*0.95:idx===1?(gW-36)*0.295:(gW-36)*0.083).toFixed(1);
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+barW+'" height="14" rx="3" fill="'+item.col+'"/>';
      const pulseX=gX+18+((phase*(2.0+idx*0.7))%1)*(gW-36);
      svg+='<circle cx="'+pulseX.toFixed(1)+'" cy="'+(rowY+7)+'" r="4.5" fill="#fde68a" stroke="#fff" stroke-width="1"/>';
      svg+='<text x="'+(gX+22)+'" y="'+(rowY+26)+'" fill="#9fb498" font-size="8">'+item.desc+' · '+item.m1k+'</text>';
    });
    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'CHEMICAL EQUIVALENT WEIGHT RATIOS','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    const equivStats=[
      {name:'Silver Ag (M = 107.87, n = 1)',eq:'Eq = 107.87 g/eq',ratio:'Ratio = 3.395 × Cu',col:ink},
      {name:'Copper Cu (M = 63.55, n = 2)',eq:'Eq = 31.77 g/eq',ratio:'Reference Baseline (1.000)',col:orange},
      {name:'Aluminum Al (M = 26.98, n = 3)',eq:'Eq = 8.99 g/eq',ratio:'Ratio = 0.283 × Cu',col:'#38bdf8'}
    ];
    equivStats.forEach((s,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+s.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+s.col+'" font-size="11" font-weight="bold">'+s.name+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">'+s.eq+' · '+s.ratio+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,"Faraday's 2nd Law: m₁ / m₂ = (M₁ / n₁) / (M₂ / n₂) · Faraday Constant F = e N_A = 96485.3 C mol⁻¹",soft,10);
  }
  else if(isElecHeat){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'CALORIMETRIC HEATING CURVES (25.0 W CONTINUOUS)', '#e2ecd7',11);
    const fluids=[
      {name:'Distilled Water (c = 4.186 J g⁻¹ K⁻¹)',col:ink,rate:'dT/dt = 0.0964 °C/s',barW:0.45,desc:'High specific heat capacity reference · Strong hydrogen bond network'},
      {name:'Pure Ethanol (c = 2.440 J g⁻¹ K⁻¹)',col:orange,rate:'dT/dt = 0.1654 °C/s',barW:0.75,desc:'Medium specific heat organic alcohol · 1.7× faster heating than water'},
      {name:'Mineral Oil (c = 1.900 J g⁻¹ K⁻¹)',col:'#38bdf8',rate:'dT/dt = 0.2124 °C/s',barW:0.95,desc:'Low specific heat hydrocarbon fluid · 2.2× rapid temperature rise'}
    ];
    fluids.forEach((item,idx)=>{
      const rowY=gY+35+idx*55;
      svg+='<text x="'+(gX+18)+'" y="'+(rowY-8)+'" fill="'+item.col+'" font-size="10" font-weight="bold">'+item.name+'</text>';
      svg+='<text x="'+(gX+gW-18)+'" y="'+(rowY-8)+'" text-anchor="end" fill="'+item.col+'" font-size="10" font-family="monospace">'+item.rate+'</text>';
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+(gW-36)+'" height="14" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
      const bW=(gW-36)*item.barW;
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+bW.toFixed(1)+'" height="14" rx="3" fill="'+item.col+'"/>';
      const pulseX=gX+18+((phase*(1.8+idx*0.6))%1)*(gW-36);
      svg+='<circle cx="'+pulseX.toFixed(1)+'" cy="'+(rowY+7)+'" r="4.5" fill="#fde68a" stroke="#fff" stroke-width="1"/>';
      svg+='<text x="'+(gX+22)+'" y="'+(rowY+26)+'" fill="#9fb498" font-size="8">'+item.desc+'</text>';
    });
    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'MECHANICAL EQUIVALENCE THEOREM','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    const heatStats=[
      {name:'Electrical Work: W = V · I · t',val:'dW/dt = 25.00 J s⁻¹',col:ink},
      {name:'Thermal Absorption: Q = C_sys · ΔT',val:'dQ/dt = 5.972 cal s⁻¹',col:orange},
      {name:'Mechanical Equivalent J = W / Q',val:'J = 4.1860 J cal⁻¹',col:'#38bdf8'}
    ];
    heatStats.forEach((s,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+s.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+s.col+'" font-size="10.5" font-weight="bold">'+s.name+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">'+s.val+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,"First Law of Thermodynamics: ∮ dW = J ∮ dQ · J = 4.1860 J cal⁻¹ (Absolute Equivalence)",soft,10);
  }
  else if(isPotentiometer){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'ELECTROCHEMICAL CELL EMF BENCHMARK (k = 0.02000 V/cm)','#e2ecd7',11);
    const cells=[
      {name:'Weston Cadmium Standard (ℰ = 1.0183 V)',col:ink,ell:'ℓ = 50.92 cm',barW:0.509,desc:'Saturated cadmium sulfate primary metrology standard · Low temp drift'},
      {name:'Daniell Porous Pot Cell (ℰ = 1.0800 V)',col:orange,ell:'ℓ = 54.00 cm',barW:0.540,desc:'Copper-Zinc redox equilibrium: Zn + Cu²⁺ ⟶ Zn²⁺ + Cu (Classic 1836)'},
      {name:'Leclanché Carbon-Zinc Dry Cell (ℰ = 1.4500 V)',col:'#38bdf8',ell:'ℓ = 72.50 cm',barW:0.725,desc:'Manganese dioxide depolarizer · University laboratory workhorse cell'}
    ];
    cells.forEach((item,idx)=>{
      const rowY=gY+35+idx*55;
      svg+='<text x="'+(gX+18)+'" y="'+(rowY-8)+'" fill="'+item.col+'" font-size="10" font-weight="bold">'+item.name+'</text>';
      svg+='<text x="'+(gX+gW-18)+'" y="'+(rowY-8)+'" text-anchor="end" fill="'+item.col+'" font-size="10" font-family="monospace">'+item.ell+'</text>';
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+(gW-36)+'" height="14" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
      const bW=(gW-36)*item.barW;
      svg+='<rect x="'+(gX+18)+'" y="'+rowY+'" width="'+bW.toFixed(1)+'" height="14" rx="3" fill="'+item.col+'"/>';
      const pulseX=gX+18+((phase*(1.5+idx*0.5))%1)*(gW-36);
      svg+='<circle cx="'+pulseX.toFixed(1)+'" cy="'+(rowY+7)+'" r="4.5" fill="#fde68a" stroke="#fff" stroke-width="1"/>';
      svg+='<text x="'+(gX+22)+'" y="'+(rowY+26)+'" fill="#9fb498" font-size="8">'+item.desc+'</text>';
    });
    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'POTENTIOMETER NULL COMPARISON','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    const potStats=[
      {name:'Driver Cell Potential: ℰ_driver = 2.000 V',val:'Wire length L = 100.0 cm',col:ink},
      {name:'Linear Gradient: k = ℰ / L',val:'k = 0.02000 V cm⁻¹ (2.000 V m⁻¹)',col:orange},
      {name:'EMF Ratio: ℰ₁ / ℰ₂ = ℓ₁ / ℓ₂',val:'Independent of wire diameter & internal r',col:'#38bdf8'}
    ];
    potStats.forEach((s,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+s.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+s.col+'" font-size="10.5" font-weight="bold">'+s.name+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">'+s.val+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,"Poggendorff Null Method: ℰ_x = k · ℓ_x ⟹ Infinite effective input resistance eliminates internal drop I·r",soft,10);
  }
  else if(isSpectra){
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#091014" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'MULTI-ELEMENT DISCHARGE EMISSION SPECTRA','#e2ecd7',11);
    const spectra=[
      {name:'Hydrogen (Balmer Series)',lines:[{wl:656.3,col:'#ef4444'},{wl:486.1,col:'#06b6d4'},{wl:434.0,col:'#6366f1'},{wl:410.2,col:'#8b5cf6'}],desc:'Pure Coulomb single-electron atom · Rydberg fit diff < 0.02%'},
      {name:'Helium (Neutral He I Arc)',lines:[{wl:706.5,col:'#dc2626'},{wl:667.8,col:'#ea580c'},{wl:587.6,col:'#eab308'},{wl:501.6,col:'#22c55e'},{wl:447.1,col:'#3b82f6'},{wl:388.9,col:'#a855f7'}],desc:'Two electrons · Orthohelium & parahelium singlet/triplet states'},
      {name:'Sodium (Alkali Metal Vapor)',lines:[{wl:589.0,col:'#facc15'},{wl:589.6,col:'#fde047'},{wl:568.8,col:'#84cc16'},{wl:615.4,col:'#f97316'}],desc:'Single valence electron · Spin-orbit doublet splitting (0.597 nm gap)'},
      {name:'Mercury (Low-Pressure Arc)',lines:[{wl:579.1,col:'#facc15'},{wl:577.0,col:'#fde047'},{wl:546.1,col:'#10b981'},{wl:435.8,col:'#38bdf8'},{wl:404.7,col:'#818cf8'}],desc:'Heavy Z=80 atom · Relativistic j-j coupling & prominent UV lines'}
    ];
    const wlMin=380,wlMax=750;
    spectra.forEach((s,idx)=>{
      const rowY=gY+25+idx*46;
      svg+='<text x="'+(gX+14)+'" y="'+(rowY-4)+'" fill="#e2ecd7" font-size="9" font-weight="bold">'+s.name+'</text>';
      svg+='<rect x="'+(gX+14)+'" y="'+rowY+'" width="'+(gW-28)+'" height="16" rx="2" fill="#04080c" stroke="#1f2937" stroke-width="1"/>';
      s.lines.forEach(l=>{
        const lx=gX+14+((l.wl-wlMin)/(wlMax-wlMin))*(gW-28);
        svg+='<line x1="'+lx.toFixed(1)+'" y1="'+rowY+'" x2="'+lx.toFixed(1)+'" y2="'+(rowY+16)+'" stroke="'+l.col+'" stroke-width="2.5"/>';
        svg+='<line x1="'+lx.toFixed(1)+'" y1="'+(rowY-1)+'" x2="'+lx.toFixed(1)+'" y2="'+(rowY+17)+'" stroke="#ffffff" stroke-width="0.8" opacity="0.6"/>';
      });
      svg+='<text x="'+(gX+16)+'" y="'+(rowY+25)+'" fill="#9fb498" font-size="7.5">'+s.desc+'</text>';
    });
    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'QUANTUM EMISSION FINGERPRINTS','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    const qStats=[
      {name:'Hydrogen H (Z = 1)',term:'1s¹ (Pure Coulomb)',scale:'R_H = 10967758 m⁻¹',col:'#ef4444'},
      {name:'Helium He (Z = 2)',term:'1s² (Screened e⁻-e⁻)',scale:'R_He = 10972227 m⁻¹',col:'#ea580c'},
      {name:'Sodium Na (Z = 11)',term:'[Ne] 3s¹ (Core Defect δ_s=1.37)',scale:'Doublet Δλ = 0.597 nm',col:'#facc15'},
      {name:'Mercury Hg (Z = 80)',term:'[Xe] 4f¹⁴ 5d¹⁰ 6s² (Relativistic)',scale:'Ultraviolet λ = 253.7 nm',col:'#38bdf8'}
    ];
    qStats.forEach((s,idx)=>{
      const rowY=bY+48+idx*39;
      svg+='<circle cx="'+(bX+20)+'" cy="'+(rowY-4)+'" r="4" fill="'+s.col+'"/>';
      svg+='<text x="'+(bX+30)+'" y="'+rowY+'" fill="'+s.col+'" font-size="10" font-weight="bold">'+s.name+'</text>';
      svg+='<text x="'+(bX+30)+'" y="'+(rowY+13)+'" fill="#9fb498" font-size="8">'+s.term+' · '+s.scale+'</text>';
      if(idx<3)svg+='<line x1="'+(bX+18)+'" y1="'+(rowY+20)+'" x2="'+(bX+bW-18)+'" y2="'+(rowY+20)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,"Kirchhoff's Laws: Every gas radiates bright spectral lines identical to its absorption wavelengths",soft,10);
  }
  else{
    const gX=60,gY=55,gW=340,gH=210;
    svg+='<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#14221e" stroke="'+soft+'" stroke-width="1.5" rx="4"/>';
    svg+=text(gX+gW/2,gY-15,'DYNAMIC OSCILLATIONS ACROSS CELESTIAL BODIES','#e2ecd7',11);

    const worlds=[
      {name:'Earth',g:9.807,col:ink,x:gX+65},
      {name:'Moon',g:1.625,col:orange,x:gX+170},
      {name:'Mars',g:3.721,col:'#38bdf8',x:gX+275}
    ];

    worlds.forEach(w=>{
      const period=2*Math.PI*Math.sqrt(1.0/w.g);
      const angle=0.35*Math.cos(phase*(2*Math.PI/period));
      const len=90;
      const bXPos=w.x+len*Math.sin(angle);
      const bYPos=gY+45+len*Math.cos(angle);

      svg+='<line x1="'+(w.x-25)+'" y1="'+(gY+45)+'" x2="'+(w.x+25)+'" y2="'+(gY+45)+'" stroke="'+soft+'" stroke-width="2"/>';
      svg+='<circle cx="'+w.x+'" cy="'+(gY+45)+'" r="3" fill="'+soft+'"/>';
      svg+='<line x1="'+w.x+'" y1="'+(gY+45)+'" x2="'+bXPos+'" y2="'+bYPos+'" stroke="'+w.col+'" stroke-width="1.5"/>';
      svg+='<circle cx="'+bXPos+'" cy="'+bYPos+'" r="10" fill="'+w.col+'"/>';
      svg+=text(w.x,gY+175,w.name,w.col,10);
      svg+=text(w.x,gY+190,'g = '+w.g.toFixed(2)+' m/s²','#9fb498',8.5);
      svg+=text(w.x,gY+202,'T = '+period.toFixed(2)+' s','#9fb498',8.5);
    });

    const bX=425,bY=55,bW=265,bH=210;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'GRAVITATIONAL FIELD DYNAMICS','#718e79',9.5);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';

    const stats=[
      {name:'Earth Surface',g:'9.807 m s⁻²',tRatio:'1.000 × T₀',col:ink},
      {name:'Lunar Surface',g:'1.625 m s⁻²',tRatio:'2.456 × T₀',col:orange},
      {name:'Martian Surface',g:'3.721 m s⁻²',tRatio:'1.623 × T₀',col:'#38bdf8'}
    ];
    stats.forEach((s,idx)=>{
      const rowY=bY+52+idx*46;
      svg+='<circle cx="'+(bX+22)+'" cy="'+(rowY-4)+'" r="4.5" fill="'+s.col+'"/>';
      svg+='<text x="'+(bX+34)+'" y="'+rowY+'" fill="'+s.col+'" font-size="11" font-weight="bold">'+s.name+'</text>';
      svg+='<text x="'+(bX+34)+'" y="'+(rowY+15)+'" fill="#9fb498" font-size="8.5">g = '+s.g+' · T = '+s.tRatio+'</text>';
      if(idx<2)svg+='<line x1="'+(bX+20)+'" y1="'+(rowY+24)+'" x2="'+(bX+bW-20)+'" y2="'+(rowY+24)+'" stroke="#253a34" stroke-dasharray="2 2"/>';
    });
    svg+=text(360,305,'Gravitational Scaling Law: Period T ∝ 1 / √g · Frequency f ∝ √g',soft,10);
  }

  $('apparatusDiagram').innerHTML=svg;
}

function drawDynamicSandbox(t,p,v,phase,ink,soft,orange){
  const isGas=['boyles-law','charles-law-volume','charles-law-pressure','vapor-pressure','air-humidity'].includes(cfg.slug);
  const isHeat=['specific-heat-capacity','newtons-cooling','solidification-cooling','latent-heat-vaporization','latent-heat-fusion','thermal-expansion','mechanical-equivalent-heat'].includes(cfg.slug);
  const isOptics=['convex-lens','glass-slab','diffraction-grating'].includes(cfg.slug);
  const isElec=['ohms-law','metre-bridge','rc-charging'].includes(cfg.slug);
  const isSound=['resonance-air-column','modes-air-column','vibration-strings-sonometer','interference-sound-waves'].includes(cfg.slug);
  const isElectrostatic=['electrostatics'].includes(cfg.slug);
  const isMagnetic=['magnetic-fields'].includes(cfg.slug);
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#9fb498',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  if(isGas){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'2D KINETIC GAS MOLECULAR SIMULATION (N = 36 MOLECULES)','#e2ecd7',11);

    const tempK=p.input>100?p.input:p.input+273.15;
    const vScale=Math.sqrt(Math.max(200,Math.min(600,tempK)))*0.08;

    for(let i=0;i<36;i++){
      const seedX=(i*37)%cW;
      const seedY=(i*73)%cH;
      const angle=(i*1.618)*2*Math.PI;
      const speed=vScale*(0.6+((i*19)%10)*0.08);
      const curX=cX+15+Math.abs((seedX+Math.cos(angle)*phase*speed*40)%(cW-30));
      const curY=cY+15+Math.abs((seedY+Math.sin(angle)*phase*speed*40)%(cH-30));
      const col=(i%3===0)?orange:(i%3===1)?ink:'#38bdf8';
      svg+='<circle cx="'+curX.toFixed(1)+'" cy="'+curY.toFixed(1)+'" r="4.5" fill="'+col+'"/>';
      svg+='<line x1="'+curX.toFixed(1)+'" y1="'+curY.toFixed(1)+'" x2="'+(curX+Math.cos(angle)*speed*12).toFixed(1)+'" y2="'+(curY+Math.sin(angle)*speed*12).toFixed(1)+'" stroke="'+col+'" stroke-width="1.2" opacity="0.6"/>';
    }

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'MAXWELL-BOLTZMANN VELOCITY SPECTRUM','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';

    const mX=bX+25,mY=bY+115,mW=bW-50,mH=65;
    svg+='<line x1="'+mX+'" y1="'+mY+'" x2="'+(mX+mW)+'" y2="'+mY+'" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<line x1="'+mX+'" y1="'+(mY-mH)+'" x2="'+mX+'" y2="'+mY+'" stroke="'+soft+'" stroke-width="1"/>';
    let mbPoints=[];
    const peakPos=mW*0.35*(vScale/1.8);
    for(let j=0;j<=40;j++){
      const u=j/40;
      const xPt=mX+u*mW;
      const yVal=(u/0.35)*Math.exp(1-u/0.35);
      const yPt=mY-Math.min(mH,yVal*(mH*0.85));
      mbPoints.push(xPt.toFixed(1)+','+yPt.toFixed(1));
    }
    svg+='<polyline points="'+mbPoints.join(' ')+'" fill="none" stroke="'+orange+'" stroke-width="2"/>';
    svg+='<circle cx="'+(mX+peakPos).toFixed(1)+'" cy="'+(mY-mH*0.85).toFixed(1)+'" r="4" fill="#fde68a"/>';
    svg+=text(mX+peakPos,mY-mH*0.85-8,'v_rms','#fde68a',8);

    const vRmsEst=Math.round(vScale*240);
    svg+='<text x="'+(bX+25)+'" y="'+(bY+142)+'" fill="'+soft+'" font-size="8.5">RMS MOLECULAR SPEED (v_rms):</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+162)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">'+vRmsEst+' m s⁻¹</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+184)+'" fill="'+soft+'" font-size="8.5">MEAN KINETIC ENERGY ⟨E_k⟩:</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+202)+'" fill="'+ink+'" font-size="14" font-family="monospace">'+(3/2*1.38e-23*tempK*1e21).toFixed(2)+' × 10⁻²¹ J</text>';

    svg+=text(360,305,'Microscopic Kinetic Theory: P = (1/3) ρ ⟨v²⟩ · Thermal Equipartition ⟨E_k⟩ = (3/2) k_B T',soft,10);
  }
  else if(isHeat){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'ATOMIC LATTICE THERMAL PHONON VIBRATIONS','#e2ecd7',11);

    const tempK=p.input>100?p.input:p.input+273.15;
    const vibAmp=Math.min(12,Math.sqrt(tempK/50.0)*1.8);

    for(let r=0;r<4;r++){
      for(let c=0;c<6;c++){
        const baseX=cX+45+c*50;
        const baseY=cY+40+r*45;
        const vibX=vibAmp*Math.sin(phase*12+r*1.2+c*0.9);
        const vibY=vibAmp*Math.cos(phase*10+r*0.8+c*1.4);
        const ax=baseX+vibX;
        const ay=baseY+vibY;

        if(c<5){
          const nextAx=cX+45+(c+1)*50+vibAmp*Math.sin(phase*12+r*1.2+(c+1)*0.9);
          const nextAy=baseY+vibAmp*Math.cos(phase*10+r*0.8+(c+1)*1.4);
          svg+='<line x1="'+ax.toFixed(1)+'" y1="'+ay.toFixed(1)+'" x2="'+nextAx.toFixed(1)+'" y2="'+nextAy.toFixed(1)+'" stroke="'+soft+'" stroke-width="1.2" stroke-dasharray="2 2"/>';
        }
        if(r<3){
          const downAx=baseX+vibAmp*Math.sin(phase*12+(r+1)*1.2+c*0.9);
          const downAy=cY+40+(r+1)*45+vibAmp*Math.cos(phase*10+(r+1)*0.8+c*1.4);
          svg+='<line x1="'+ax.toFixed(1)+'" y1="'+ay.toFixed(1)+'" x2="'+downAx.toFixed(1)+'" y2="'+downAy.toFixed(1)+'" stroke="'+soft+'" stroke-width="1.2" stroke-dasharray="2 2"/>';
        }
        svg+='<circle cx="'+ax.toFixed(1)+'" cy="'+ay.toFixed(1)+'" r="7" fill="'+orange+'" stroke="#fde68a" stroke-width="1.5"/>';
      }
    }

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'PHONON DENSITY & LATTICE ENTHALPY','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';

    svg+='<text x="'+(bX+25)+'" y="'+(bY+60)+'" fill="'+soft+'" font-size="8.5">LATTICE TEMPERATURE:</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+80)+'" fill="'+orange+'" font-size="17" font-family="monospace" font-weight="bold">'+tempK.toFixed(1)+' K</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+108)+'" fill="'+soft+'" font-size="8.5">MEAN ROOT DISPLACEMENT ⟨u²⟩¹/²:</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+128)+'" fill="'+ink+'" font-size="14" font-family="monospace">'+(vibAmp*0.08).toFixed(3)+' Å (Angstroms)</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+156)+'" fill="'+soft+'" font-size="8.5">DEBYE PHONON CUTOFF FREQUENCY:</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+176)+'" fill="#38bdf8" font-size="14" font-family="monospace">ω_D ≈ 4.82 × 10¹³ rad s⁻¹</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+202)+'" fill="#9fb498" font-size="8.5">Dulong-Petit Limit: C_v → 3 R ≈ 24.9 J mol⁻¹ K⁻¹</text>';

    svg+=text(360,305,'Solid-State Thermodynamics: Harmonic Interatomic Potentials & Phonon Scattering',soft,10);
  }
  else if(isOptics){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'HUYGENS-FRESNEL WAVEFRONT PROPAGATION','#e2ecd7',11);

    const slitX=cX+70,slitY=cY+cH/2;
    svg+='<line x1="'+slitX+'" y1="'+cY+'" x2="'+slitX+'" y2="'+(slitY-20)+'" stroke="'+soft+'" stroke-width="4"/>';
    svg+='<line x1="'+slitX+'" y1="'+(slitY+20)+'" x2="'+slitX+'" y2="'+(cY+cH)+'" stroke="'+soft+'" stroke-width="4"/>';
    svg+=text(slitX-30,slitY+4,'Aperture',soft,8.5);

    for(let w=0;w<7;w++){
      const radius=((phase*40+w*32)%220)+10;
      svg+='<circle cx="'+slitX+'" cy="'+slitY+'" r="'+radius.toFixed(1)+'" fill="none" stroke="#38bdf8" stroke-width="1.8" opacity="'+(1.0-radius/230).toFixed(2)+'"/>';
    }

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'DIFFRACTION INTENSITY PATTERN I(θ)','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';

    const mX=bX+25,mY=bY+130,mW=bW-50,mH=75;
    svg+='<line x1="'+mX+'" y1="'+mY+'" x2="'+(mX+mW)+'" y2="'+mY+'" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<line x1="'+(mX+mW/2)+'" y1="'+(mY-mH)+'" x2="'+(mX+mW/2)+'" y2="'+mY+'" stroke="'+soft+'" stroke-width="1" stroke-dasharray="2 2"/>';

    let diffPoints=[];
    for(let k=0;k<=60;k++){
      const theta=(k-30)/10.0;
      const xPt=mX+(k/60)*mW;
      const sinc=theta===0?1:Math.sin(theta)/theta;
      const intensity=sinc*sinc;
      const yPt=mY-intensity*(mH*0.9);
      diffPoints.push(xPt.toFixed(1)+','+yPt.toFixed(1));
    }
    svg+='<polyline points="'+diffPoints.join(' ')+'" fill="none" stroke="'+orange+'" stroke-width="2"/>';

    svg+='<text x="'+(bX+25)+'" y="'+(bY+165)+'" fill="'+soft+'" font-size="8.5">CENTRAL MAXIMUM (m = 0):</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+185)+'" fill="'+orange+'" font-size="14" font-family="monospace">I₀ = 100% Relative Intensity</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+205)+'" fill="#9fb498" font-size="8.5">First Minimum: a sin(θ) = λ ⇔ θ₁ = ±1.22 λ/D</text>';

    svg+=text(360,305,'Physical Wave Optics: Phase Coherence, Secondary Wavelets, and Diffraction Envelopes',soft,10);
  }
  else if(isElec){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'MICROSCOPIC ELECTRON DRIFT IN COPPER LATTICE','#e2ecd7',11);

    for(let r=0;r<4;r++){
      for(let c=0;c<7;c++){
        const ix=cX+30+c*48;
        const iy=cY+35+r*50;
        svg+='<circle cx="'+ix+'" cy="'+iy+'" r="10" fill="#20362f" stroke="'+soft+'" stroke-width="1.5"/>';
        svg+=text(ix,iy+3,'+Cu',soft,7.5);
      }
    }

    const driftSpeed=(p.input/(cfg.max||10))*25+10;
    for(let e=0;e<20;e++){
      const eSeedX=(e*53)%cW;
      const eSeedY=(e*47)%(cH-40);
      const curX=cX+((eSeedX+phase*driftSpeed*2)%(cW-20));
      const curY=cY+20+eSeedY+Math.sin(phase*8+e)*6;
      svg+='<circle cx="'+curX.toFixed(1)+'" cy="'+curY.toFixed(1)+'" r="3" fill="#38bdf8"/>';
    }

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'DRUDE MODEL ELECTRON TRANSPORT','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';

    const driftVel_um=(driftSpeed*1.5).toFixed(1);
    svg+='<text x="'+(bX+25)+'" y="'+(bY+60)+'" fill="'+soft+'" font-size="8.5">ELECTRON DRIFT SPEED (v_d):</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+80)+'" fill="'+orange+'" font-size="17" font-family="monospace" font-weight="bold">'+driftVel_um+' μm s⁻¹</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+108)+'" fill="'+soft+'" font-size="8.5">CONDUCTION ELECTRON DENSITY (n):</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+128)+'" fill="'+ink+'" font-size="14" font-family="monospace">8.49 × 10²⁸ m⁻³ (Copper)</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+156)+'" fill="'+soft+'" font-size="8.5">MEAN FREE COLLISION TIME (τ):</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+176)+'" fill="#38bdf8" font-size="14" font-family="monospace">τ ≈ 2.47 × 10⁻¹⁴ s</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+202)+'" fill="#9fb498" font-size="8.5">Microscopic Ohm\'s Law: J = σ E = n e v_d</text>';

    svg+=text(360,305,'Solid-State Conduction: Electronic Scattering, Mobility μ = eτ/m, and Joule Dissipation',soft,10);
  }
  else if(isSound){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'LONGITUDINAL MOLECULAR STANDING WAVE (N = 48 MOLECULES)','#e2ecd7',11);
    const fVal=p.input||384.0;
    const omega=2*Math.PI*(fVal/200);
    for(let row=0;row<6;row++){
      const yRow=cY+35+row*28;
      svg+='<line x1="'+(cX+15)+'" y1="'+yRow+'" x2="'+(cX+cW-15)+'" y2="'+yRow+'" stroke="#1f332c" stroke-width="1" stroke-dasharray="2 4"/>';
      for(let col=0;col<8;col++){
        const xEq=cX+25+col*((cW-50)/7);
        const normX=col/7;
        const disp=Math.sin((Math.PI/2)*normX)*Math.cos(omega*phase)*14;
        const curX=xEq+disp;
        const colParticle=(disp>2)?orange:(disp<-2)?'#38bdf8':ink;
        svg+='<circle cx="'+curX.toFixed(1)+'" cy="'+yRow+'" r="3.5" fill="'+colParticle+'"/>';
      }
    }
    let prPoints=[];
    for(let i=0;i<=40;i++){
      const nx=i/40;
      const px=cX+20+nx*(cW-40);
      const prVal=Math.cos((Math.PI/2)*nx)*Math.sin(omega*phase);
      const py=cY+cH-30-prVal*22;
      prPoints.push(px.toFixed(1)+','+py.toFixed(1));
    }
    svg+='<polyline points="'+prPoints.join(' ')+'" fill="none" stroke="#fde68a" stroke-width="2"/>';
    svg+='<line x1="'+(cX+20)+'" y1="'+(cY+cH-30)+'" x2="'+(cX+cW-20)+'" y2="'+(cY+cH-30)+'" stroke="'+soft+'" stroke-dasharray="2 2"/>';
    svg+=text(cX+35,cY+cH-8,'Node (Water)',soft,8);
    svg+=text(cX+cW-45,cY+cH-8,'Antinode (Open)',orange,8);
    svg+=text(cX+cW/2,cY+cH-8,'Acoustic Pressure ΔP(x,t)',soft,8);

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'ACOUSTIC ENERGY & HARMONIC DENSITY','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    const sinT=Math.sin(omega*phase),cosT=Math.cos(omega*phase);
    const Ek=sinT*sinT,Ep=cosT*cosT;
    svg+='<text x="'+(bX+25)+'" y="'+(bY+58)+'" fill="'+ink+'" font-size="9">Acoustic Kinetic Energy (Particle Velocity ~ u²)</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="'+(Ek*220).toFixed(1)+'" height="12" rx="3" fill="'+ink+'"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+100)+'" fill="'+orange+'" font-size="9">Acoustic Potential Energy (Compression ~ ΔP²)</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+107)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+107)+'" width="'+(Ep*220).toFixed(1)+'" height="12" rx="3" fill="'+orange+'"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+142)+'" fill="#fde68a" font-size="9">Total Acoustic Energy Density ε = E_k + E_p</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+149)+'" width="220" height="14" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+149)+'" width="220" height="14" rx="3" fill="#fde68a"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+185)+'" fill="#9fb498" font-size="8.5">Quarter-Wave Condition: L + c = (2n − 1) λ / 4</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+202)+'" fill="'+soft+'" font-size="8">Orthogonal Modes: Odd Harmonics f₁ (1f), f₂ (3f), f₃ (5f)</text>';
    svg+=text(360,305,'Longitudinal Waves: Molecular Compressions & Rarefactions · Rayleigh Boundary Dissipation',soft,10);
  }
  else if(isElectrostatic){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'2D ELECTROSTATIC FIELD & VECTOR TRACERS (COULOMB REPULSION)','#e2ecd7',11);
    const q1X=cX+90,q2X=cX+cW-90,qY=cY+cH/2;
    // Charge spheres
    svg+='<circle cx="'+q1X+'" cy="'+qY+'" r="14" fill="#d97706" stroke="#f59e0b" stroke-width="2"/>';
    svg+='<text x="'+q1X+'" y="'+(qY+4)+'" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold">+q₁</text>';
    svg+='<circle cx="'+q2X+'" cy="'+qY+'" r="14" fill="#d97706" stroke="#f59e0b" stroke-width="2"/>';
    svg+='<text x="'+q2X+'" y="'+(qY+4)+'" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold">+q₂</text>';
    // Central neutral point
    const midX=(q1X+q2X)/2;
    svg+='<circle cx="'+midX+'" cy="'+qY+'" r="4" fill="none" stroke="#ef4444" stroke-width="1.5"/>';
    svg+='<line x1="'+(midX-6)+'" y1="'+qY+'" x2="'+(midX+6)+'" y2="'+qY+'" stroke="#ef4444" stroke-width="1"/>';
    svg+='<line x1="'+midX+'" y1="'+(qY-6)+'" x2="'+midX+'" y2="'+(qY+6)+'" stroke="#ef4444" stroke-width="1"/>';
    svg+=text(midX,qY-10,'E⃗ = 0 (Neutral Point)','#ef4444',7.5);
    // Field lines radiating and bending away
    for(let a=0;a<8;a++){
      const ang=(a/8)*2*Math.PI;
      const c1x=q1X+Math.cos(ang)*18,c1y=qY+Math.sin(ang)*18;
      const bend1X=c1x+Math.cos(ang)*60-(Math.cos(ang)>0?25:0);
      const bend1Y=c1y+Math.sin(ang)*70;
      svg+='<path d="M '+c1x.toFixed(1)+' '+c1y.toFixed(1)+' Q '+bend1X.toFixed(1)+' '+bend1Y.toFixed(1)+' '+(bend1X+Math.cos(ang)*30).toFixed(1)+' '+(bend1Y+Math.sin(ang)*30).toFixed(1)+'" fill="none" stroke="'+ink+'" stroke-width="1.2" opacity="0.65"/>';
      const c2x=q2X+Math.cos(ang)*18,c2y=qY+Math.sin(ang)*18;
      const bend2X=c2x+Math.cos(ang)*60+(Math.cos(ang)<0?25:0);
      const bend2Y=c2y+Math.sin(ang)*70;
      svg+='<path d="M '+c2x.toFixed(1)+' '+c2y.toFixed(1)+' Q '+bend2X.toFixed(1)+' '+bend2Y.toFixed(1)+' '+(bend2X+Math.cos(ang)*30).toFixed(1)+' '+(bend2Y+Math.sin(ang)*30).toFixed(1)+'" fill="none" stroke="'+ink+'" stroke-width="1.2" opacity="0.65"/>';
    }
    // Dynamic tracer particles flowing outward
    for(let tr=0;tr<12;tr++){
      const tNorm=((phase*1.8+tr/12)%1);
      const tAng=(tr/12)*2*Math.PI;
      const tX=q1X+Math.cos(tAng)*(18+tNorm*75);
      const tY=qY+Math.sin(tAng)*(18+tNorm*75);
      svg+='<circle cx="'+tX.toFixed(1)+'" cy="'+tY.toFixed(1)+'" r="2.5" fill="#fde68a" opacity="'+(1.0-tNorm*0.6)+'"/>';
    }
    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'ENERGY DENSITY & FARADAY SHIELDING','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+58)+'" fill="'+ink+'" font-size="9">Electrostatic Energy Density u_E = ½ ε₀ E²</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    const uE_bar=(160+Math.sin(phase*4)*40).toFixed(1);
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="'+uE_bar+'" height="12" rx="3" fill="'+ink+'"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+100)+'" fill="'+orange+'" font-size="9">Electric Potential V(r) = k_e q / r</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+107)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    const v_bar=(180+Math.cos(phase*3)*30).toFixed(1);
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+107)+'" width="'+v_bar+'" height="12" rx="3" fill="'+orange+'"/>';
    // Faraday Ice Pail Cavity Icon
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+135)+'" width="220" height="58" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+152)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">FARADAY CAGE / CONDUCTING SHELL</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+168)+'" text-anchor="middle" fill="#fde68a" font-size="8">Internal Cavity: E⃗_inside ≡ 0 (Gauss Law)</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+182)+'" text-anchor="middle" fill="#9fb498" font-size="7.5">100% Net Charge Resides on Outer Surface: σ = ε₀ E_⊥</text>';
    svg+=text(360,305,'Coulomb Vector Superposition: E⃗_net = Σ E⃗_i · Electrostatic Energy Density u_E = ½ ε₀ E²',soft,10);
  }
  else if(isMagnetic){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'2D BIOT-SAVART MAGNETIC FLUX & CIRCULATING VECTOR TRACERS','#e2ecd7',11);
    const midX=cX+cW/2,midY=cY+cH/2;
    // Circular coil cross-section: Top conductor (current out of page ⊙) and Bottom conductor (current into page ⊗)
    const topWireY=cY+35,botWireY=cY+cH-35;
    // Top wire element
    svg+='<circle cx="'+midX+'" cy="'+topWireY+'" r="10" fill="#b45309" stroke="#d97706" stroke-width="2"/>';
    svg+='<circle cx="'+midX+'" cy="'+topWireY+'" r="3" fill="#fff"/>';
    svg+='<text x="'+(midX+16)+'" y="'+(topWireY+4)+'" fill="#fde68a" font-size="8.5" font-weight="bold">I ⊙ (Out of page)</text>';
    // Bottom wire element
    svg+='<circle cx="'+midX+'" cy="'+botWireY+'" r="10" fill="#b45309" stroke="#d97706" stroke-width="2"/>';
    svg+='<line x1="'+(midX-4)+'" y1="'+(botWireY-4)+'" x2="'+(midX+4)+'" y2="'+(botWireY+4)+'" stroke="#fff" stroke-width="1.8"/>';
    svg+='<line x1="'+(midX-4)+'" y1="'+(botWireY+4)+'" x2="'+(midX+4)+'" y2="'+(botWireY-4)+'" stroke="#fff" stroke-width="1.8"/>';
    svg+='<text x="'+(midX+16)+'" y="'+(botWireY+4)+'" fill="#fde68a" font-size="8.5" font-weight="bold">I ⊗ (Into page)</text>';
    // Concentric and joined magnetic flux contours (ellipses passing through coil center)
    for(let r=1;r<=4;r++){
      const rx=25*r+15,ry=18*r+10;
      svg+='<ellipse cx="'+midX+'" cy="'+midY+'" rx="'+rx+'" ry="'+ry+'" fill="none" stroke="'+ink+'" stroke-width="1.2" opacity="'+(0.8-r*0.12)+'"/>';
    }
    // Dynamic circulating tracers along flux loops
    for(let tr=0;tr<10;tr++){
      const tNorm=((phase*1.5+tr/10)%1);
      const tAng=tNorm*2*Math.PI;
      const tX=midX+Math.cos(tAng)*65;
      const tY=midY+Math.sin(tAng)*45;
      svg+='<circle cx="'+tX.toFixed(1)+'" cy="'+tY.toFixed(1)+'" r="2.8" fill="#fde68a" opacity="0.9"/>';
    }
    // Center point with axial field vector B_coil pointing right
    svg+='<circle cx="'+midX+'" cy="'+midY+'" r="4" fill="#ef4444"/>';
    svg+='<line x1="'+(midX-35)+'" y1="'+midY+'" x2="'+(midX+35)+'" y2="'+midY+'" stroke="#ef4444" stroke-width="2.5"/>';
    svg+='<path d="M '+(midX+35)+' '+midY+' L '+(midX+27)+' '+(midY-4)+' L '+(midX+27)+' '+(midY+4)+' Z" fill="#ef4444"/>';
    svg+='<text x="'+(midX+42)+'" y="'+(midY+4)+'" fill="#ef4444" font-size="9" font-weight="bold">B⃗_coil</text>';
    // Earth field vector B_H pointing up (North)
    svg+='<line x1="'+midX+'" y1="'+(midY+30)+'" x2="'+midX+'" y2="'+(midY-30)+'" stroke="#22c55e" stroke-width="2.2"/>';
    svg+='<path d="M '+midX+' '+(midY-30)+' L '+(midX-4)+' '+(midY-22)+' L '+(midX+4)+' '+(midY-22)+' Z" fill="#22c55e"/>';
    svg+='<text x="'+(midX+8)+'" y="'+(midY-26)+'" fill="#22c55e" font-size="9" font-weight="bold">B⃗_H (North)</text>';
    // Resultant vector B_res
    svg+='<line x1="'+midX+'" y1="'+midY+'" x2="'+(midX+32)+'" y2="'+(midY-28)+'" stroke="'+orange+'" stroke-width="2" stroke-dasharray="3 2"/>';
    svg+='<text x="'+(midX+36)+'" y="'+(midY-30)+'" fill="'+orange+'" font-size="8.5" font-weight="bold">B⃗_res (θ)</text>';

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'AXIAL FIELD GRADIENT & HELMHOLTZ CONDITION','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+58)+'" fill="'+ink+'" font-size="9">Central Uniformity Zone (Needle 2ℓ ≪ 2R)</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="216" height="12" rx="3" fill="'+ink+'"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+92)+'" fill="#9fb498" font-size="7.5">Field variation &lt; 0.2% within central r ≤ 0.15 R</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+115)+'" fill="'+orange+'" font-size="9">Magnetic Energy Density u_B = B² / (2μ₀)</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    const uB_bar=(150+Math.sin(phase*3)*45).toFixed(1);
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="'+uB_bar+'" height="12" rx="3" fill="'+orange+'"/>';
    // Helmholtz uniform pairing box
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+145)+'" width="220" height="52" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+162)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">HELMHOLTZ COIL UNIFORMITY PAIR</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+176)+'" text-anchor="middle" fill="#fde68a" font-size="8">Coil Spacing d = R ⟹ d²B_z / dz² ≡ 0</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+190)+'" text-anchor="middle" fill="#9fb498" font-size="7.5">B_Helmholtz = (4/5)^(3/2) · (μ₀ N I / R) ≈ 0.7155 (μ₀ N I / R)</text>';
    svg+=text(360,305,'Biot-Savart Law: dB⃗ = (μ₀/4π) [I (dℓ⃗ × r̂) / r²] · Central Field B_coil = μ₀ N I / (2R)',soft,10);
  }
  else if(isFieldMapping){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'2D VECTOR FIELD GRID & EQUIPOTENTIAL FLOW TRACERS','#e2ecd7',11);
    // Boundary electrodes: Left ground (0 V), Right positive (+10 V)
    svg+='<rect x="'+(cX+10)+'" y="'+(cY+15)+'" width="8" height="'+(cH-30)+'" rx="2" fill="#3b82f6"/>';
    svg+='<text x="'+(cX+14)+'" y="'+(cY+cH-8)+'" text-anchor="middle" fill="#93c5fd" font-size="7.5" font-weight="bold">0V</text>';
    svg+='<rect x="'+(cX+cW-18)+'" y="'+(cY+15)+'" width="8" height="'+(cH-30)+'" rx="2" fill="#ef4444"/>';
    svg+='<text x="'+(cX+cW-14)+'" y="'+(cY+cH-8)+'" text-anchor="middle" fill="#fca5a5" font-size="7.5" font-weight="bold">+10V</text>';
    // Equipotential vertical lines at 2V, 4V, 6V, 8V
    for(let eq=1;eq<=4;eq++){
      const eqX=cX+14+eq*((cW-28)/5);
      svg+='<line x1="'+eqX.toFixed(1)+'" y1="'+(cY+15)+'" x2="'+eqX.toFixed(1)+'" y2="'+(cY+cH-15)+'" stroke="#06b6d4" stroke-width="1.2" stroke-dasharray="3 3" opacity="0.75"/>';
      svg+='<text x="'+eqX.toFixed(1)+'" y="'+(cY+26)+'" text-anchor="middle" fill="#06b6d4" font-size="7">'+(eq*2)+'V</text>';
    }
    // 2D Vector field arrows E pointing from right (+10V) to left (0V)
    for(let gx=0;gx<5;gx++){
      for(let gy=0;gy<4;gy++){
        const vx=cX+45+gx*58;
        const vy=cY+45+gy*42;
        svg+='<line x1="'+(vx+12)+'" y1="'+vy+'" x2="'+(vx-12)+'" y2="'+vy+'" stroke="'+ink+'" stroke-width="1.5" opacity="0.6"/>';
        svg+='<path d="M '+(vx-12)+' '+vy+' L '+(vx-6)+' '+(vy-3)+' L '+(vx-6)+' '+(vy+3)+' Z" fill="'+ink+'" opacity="0.7"/>';
      }
    }
    // Dynamic charge tracers moving along field lines
    for(let tr=0;tr<8;tr++){
      const tNorm=((phase*1.2+tr/8)%1);
      const trX=cX+cW-22-tNorm*(cW-40);
      const trY=cY+35+((tr*37)%150);
      svg+='<circle cx="'+trX.toFixed(1)+'" cy="'+trY.toFixed(1)+'" r="2.8" fill="#fde68a" opacity="0.9"/>';
    }
    // Orthogonal intersection marker at center
    const midX=cX+cW/2,midY=cY+cH/2;
    svg+='<rect x="'+(midX-8)+'" y="'+(midY-8)+'" width="8" height="8" fill="none" stroke="#f59e0b" stroke-width="1.2"/>';
    svg+='<text x="'+(midX+12)+'" y="'+(midY+4)+'" fill="#f59e0b" font-size="8" font-weight="bold">θ = 90.0° (E⃗ ⊥ Equipotential)</text>';

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'POTENTIAL GRADIENT & ENERGY DENSITY','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+58)+'" fill="'+ink+'" font-size="9">Uniform Field Gradient E = −dV/dx</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="'+ink+'"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+92)+'" fill="#9fb498" font-size="7.5">Constant 100.0 V/m across 10.0 cm gap</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+115)+'" fill="'+orange+'" font-size="9">Electrostatic Energy Density u_E = ½ ε₀ E²</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    const uE_bar=(140+Math.sin(phase*3)*40).toFixed(1);
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="'+uE_bar+'" height="12" rx="3" fill="'+orange+'"/>';
    // Laplace equation card
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+145)+'" width="220" height="52" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+162)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">LAPLACE EQUATION IN CONDUCTOR</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+176)+'" text-anchor="middle" fill="#fde68a" font-size="8">∇²V = ∂²V/∂x² + ∂²V/∂y² ≡ 0 (∇ · J⃗ = 0)</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+190)+'" text-anchor="middle" fill="#9fb498" font-size="7.5">Unique Solution: Conducting Paper ≡ Vacuum Electrostatics</text>';
    svg+=text(360,305,'Electrostatic Field: E⃗ = −∇V · Field Strength: E = V₀ / d = 100.00 V m⁻¹',soft,10);
  }
  else if(isMagMoments){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'2D MAGNETIC DIPOLE FIELD LINES & ROTATING NEEDLE','#e2ecd7',11);
    
    // Bar magnet on East axis at right
    const magX=cX+240,magY=cY+cH/2,magW=70,magH=22;
    // South half (blue)
    svg+='<rect x="'+(magX-magW/2)+'" y="'+(magY-magH/2)+'" width="'+(magW/2)+'" height="'+magH+'" rx="2" fill="#3b82f6"/>';
    svg+='<text x="'+(magX-magW/4)+'" y="'+(magY+5)+'" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">S</text>';
    // North half (red)
    svg+='<rect x="'+magX+'" y="'+(magY-magH/2)+'" width="'+(magW/2)+'" height="'+magH+'" rx="2" fill="#ef4444"/>';
    svg+='<text x="'+(magX+magW/4)+'" y="'+(magY+5)+'" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">N</text>';
    svg+='<rect x="'+(magX-magW/2)+'" y="'+(magY-magH/2)+'" width="'+magW+'" height="'+magH+'" rx="2" fill="none" stroke="#e2e8f0" stroke-width="1"/>';
    
    // Compass needle pivot at center (cX + 80, cY + cH/2)
    const pivX=cX+80,pivY=cY+cH/2;
    svg+='<circle cx="'+pivX+'" cy="'+pivY+'" r="38" fill="#090d16" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<circle cx="'+pivX+'" cy="'+pivY+'" r="28" fill="none" stroke="#253a34" stroke-width="1" stroke-dasharray="2 3"/>';
    // Needle at angle theta deflected by dipole field
    const simTheta=0.68;
    const nLen=26;
    const nx1=pivX+nLen*Math.sin(simTheta),ny1=pivY-nLen*Math.cos(simTheta);
    const nx2=pivX-nLen*Math.sin(simTheta),ny2=pivY+nLen*Math.cos(simTheta);
    svg+='<line x1="'+pivX+'" y1="'+pivY+'" x2="'+nx1.toFixed(1)+'" y2="'+ny1.toFixed(1)+'" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>';
    svg+='<line x1="'+pivX+'" y1="'+pivY+'" x2="'+nx2.toFixed(1)+'" y2="'+ny2.toFixed(1)+'" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>';
    svg+='<circle cx="'+pivX+'" cy="'+pivY+'" r="3.5" fill="#fde68a" stroke="#fff" stroke-width="1"/>';
    svg+='<text x="'+(pivX+18)+'" y="'+(pivY-16)+'" fill="#fde68a" font-size="8" font-weight="bold">θ = 39.0°</text>';
    
    // Magnetic dipole field loop curves radiating from North to South
    for(let r=1;r<=3;r++){
      const rx=r*24,ry=r*16;
      svg+='<path d="M '+(magX+magW/4)+' '+(magY-magH/2)+' C '+(magX+magW/4+rx)+' '+(magY-magH/2-ry)+', '+(magX-magW/4+rx)+' '+(magY-magH/2-ry)+', '+(magX-magW/4)+' '+(magY-magH/2)+'" fill="none" stroke="'+ink+'" stroke-width="1" opacity="0.5"/>';
      svg+='<path d="M '+(magX+magW/4)+' '+(magY+magH/2)+' C '+(magX+magW/4+rx)+' '+(magY+magH/2+ry)+', '+(magX-magW/4+rx)+' '+(magY+magH/2+ry)+', '+(magX-magW/4)+' '+(magY+magH/2)+'" fill="none" stroke="'+ink+'" stroke-width="1" opacity="0.5"/>';
    }
    // Axial field lines passing through the compass needle pivot
    svg+='<line x1="'+(cX+20)+'" y1="'+magY+'" x2="'+(magX-magW/2)+'" y2="'+magY+'" stroke="'+orange+'" stroke-width="1.5" stroke-dasharray="3 3"/>';
    // Dynamic flux particle tracers streaming towards South pole
    for(let tr=0;tr<6;tr++){
      const tNorm=((phase*1.2+tr/6)%1);
      const trX=magX-magW/2-tNorm*120;
      svg+='<circle cx="'+trX.toFixed(1)+'" cy="'+magY+'" r="2.5" fill="#fde68a" opacity="0.85"/>';
    }

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'INVERSE-CUBE DIPOLE FIELD ATTENUATION','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+58)+'" fill="'+ink+'" font-size="9">Dipole Field Decay B_axial ∝ 1/d³</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="205" height="12" rx="3" fill="'+ink+'"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+92)+'" fill="#9fb498" font-size="7.5">Field drops 8× when separation distance doubles (d ⟶ 2d)</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+115)+'" fill="'+orange+'" font-size="9">Magnetic Energy Density u_B = B² / (2μ₀)</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    const uB_bar=(145+Math.sin(phase*3)*42).toFixed(1);
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="'+uB_bar+'" height="12" rx="3" fill="'+orange+'"/>';
    // Finite length correction card
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+145)+'" width="220" height="52" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+162)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">FINITE BAR MAGNET LENGTH CORRECTION</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+176)+'" text-anchor="middle" fill="#fde68a" font-size="8">B_exact / B_dipole = [1 − (ℓ/d)²]⁻² ≈ 1 + 2(ℓ/d)²</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+190)+'" text-anchor="middle" fill="#9fb498" font-size="7.5">Correction = +1.4% at d = 14 cm (2ℓ = 8.4 cm) · &lt; 0.5% for d &gt; 22 cm</text>';
    svg+=text(360,305,'Gauss End-On Axial Law: B_A = (μ₀/4π) [2Md / (d² − ℓ²)²] = B_H tan θ ⇔ tan θ ∝ 1/d³',soft,10);
  }
  else if(isInternalR){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'CLOSED-LOOP POTENTIAL PROFILE & ION DRIFT DYNAMICS','#e2ecd7',11);
    
    // Battery Box at left
    const batX=cX+20,batY=cY+25,batW=120,batH=165;
    svg+='<rect x="'+batX+'" y="'+batY+'" width="'+batW+'" height="'+batH+'" rx="5" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>';
    svg+='<text x="'+(batX+batW/2)+'" y="'+(batY+16)+'" text-anchor="middle" fill="#94a3b8" font-size="8" font-weight="bold">PRIMARY CELL (ℰ = 1.50 V)</text>';
    
    // Anode (Zn - negative) and Cathode (MnO₂ / Carbon - positive)
    svg+='<rect x="'+(batX+12)+'" y="'+(batY+30)+'" width="14" height="100" fill="#64748b"/>';
    svg+='<text x="'+(batX+19)+'" y="'+(batY+142)+'" text-anchor="middle" fill="#93c5fd" font-size="8" font-weight="bold">− (Zn)</text>';
    svg+='<rect x="'+(batX+batW-26)+'" y="'+(batY+30)+'" width="14" height="100" fill="#d97706"/>';
    svg+='<text x="'+(batX+batW-19)+'" y="'+(batY+142)+'" text-anchor="middle" fill="#fca5a5" font-size="8" font-weight="bold">+ (C)</text>';
    
    // Electrolyte paste & ion drift particles
    svg+='<rect x="'+(batX+30)+'" y="'+(batY+30)+'" width="'+(batW-60)+'" height="100" fill="#1e293b" opacity="0.6"/>';
    svg+='<text x="'+(batX+batW/2)+'" y="'+(batY+42)+'" text-anchor="middle" fill="#718e79" font-size="7">Electrolyte Paste</text>';
    for(let tr=0;tr<8;tr++){
      const tNorm=((phase*1.2+tr/8)%1);
      const ionX=batX+32+tNorm*(batW-64);
      const ionY=batY+55+((tr*23)%65);
      const isCat=tr%2===0;
      svg+='<circle cx="'+ionX.toFixed(1)+'" cy="'+ionY.toFixed(1)+'" r="3.5" fill="'+(isCat?'#38bdf8':'#f59e0b')+'"/>';
      svg+='<text x="'+ionX.toFixed(1)+'" y="'+(ionY+2.5)+'" text-anchor="middle" fill="#000" font-size="5" font-weight="bold">'+(isCat?'+':'−')+'</text>';
    }

    // Potential step graph inside the loop
    const pX=cX+165,pY=cY+35,pW=155,pH=145;
    svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" fill="#090d16" stroke="'+soft+'" stroke-width="1" rx="4"/>';
    svg+=text(pX+pW/2,pY+14,'Closed Circuit Potential V(s)','#fde68a',7.5);
    // Axis lines
    svg+='<line x1="'+(pX+15)+'" y1="'+(pY+pH-20)+'" x2="'+(pX+pW-10)+'" y2="'+(pY+pH-20)+'" stroke="#334155"/>';
    svg+='<line x1="'+(pX+15)+'" y1="'+(pY+25)+'" x2="'+(pX+15)+'" y2="'+(pY+pH-20)+'" stroke="#334155"/>';
    svg+='<text x="'+(pX+12)+'" y="'+(pY+30)+'" text-anchor="end" fill="#cbd5e1" font-size="7">ℰ</text>';
    svg+='<text x="'+(pX+12)+'" y="'+(pY+55)+'" text-anchor="end" fill="'+orange+'" font-size="7">V</text>';
    svg+='<text x="'+(pX+12)+'" y="'+(pY+pH-18)+'" text-anchor="end" fill="#cbd5e1" font-size="7">0</text>';
    
    // Stepped potential polyline
    const y0=pY+pH-20, yE=pY+30, yV=pY+55;
    const x0=pX+15, x1=pX+35, x2=pX+65, x3=pX+120, x4=pX+pW-15;
    svg+='<polyline points="'+x0+','+y0+' '+x1+','+yE+' '+x2+','+yV+' '+x3+','+yV+' '+x4+','+y0+'" fill="none" stroke="'+ink+'" stroke-width="2"/>';
    svg+='<text x="'+((x1+x2)/2)+'" y="'+(yE-4)+'" text-anchor="middle" fill="#ef4444" font-size="6.5">−I·r drop</text>';
    svg+='<text x="'+((x2+x3)/2)+'" y="'+(yV-4)+'" text-anchor="middle" fill="'+orange+'" font-size="6.5">V = ℰ − Ir</text>';
    svg+='<text x="'+((x3+x4)/2)+'" y="'+(yV+20)+'" text-anchor="middle" fill="#38bdf8" font-size="6.5">−I·R_load</text>';

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'MAXIMUM POWER TRANSFER DYNAMICS','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+58)+'" fill="'+ink+'" font-size="9">Matched Condition: R_load = r = 2.50 Ω</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="'+ink+'"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+92)+'" fill="#9fb498" font-size="7.5">Maximum extractable power P_max = 225.0 mW</text>';
    svg+='<text x="'+(bX+25)+'"; y="'+(bY+115)+'" fill="'+orange+'" font-size="9">Electrical Transmission Efficiency η = 50.0%</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    const uE_bar=(110+Math.sin(phase*3)*20).toFixed(1);
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="'+uE_bar+'" height="12" rx="3" fill="'+orange+'"/>';
    // Circuit matching card
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+145)+'" width="220" height="52" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+162)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">KIRCHHOFF VOLTAGE LAW LOOP</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+176)+'" text-anchor="middle" fill="#fde68a" font-size="8">∮ E⃗ · dℓ⃗ = ℰ − I · r − I · R_load ≡ 0</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+190)+'" text-anchor="middle" fill="#9fb498" font-size="7.5">Terminal Voltage V = I · R_load = ℰ − I · r</text>';
    svg+=text(360,305,"Ohm's Law in Closed Circuit: I = ℰ / (R_load + r) · Terminal Voltage: V = ℰ − I · r",soft,10);
  }
  else if(isTempR){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'MICROSCOPIC ELECTRON-PHONON LATTICE SCATTERING','#e2ecd7',11);
    
    // 2D Copper crystal lattice grid with vibrating nuclei
    const gridCols=6, gridRows=4;
    const startX=cX+35, startY=cY+35;
    const stepX=(cW-70)/(gridCols-1), stepY=(cH-70)/(gridRows-1);
    const vibAmp=2.5+Math.sin(phase*6)*1.5;

    for(let r=0;r<gridRows;r++){
      for(let c=0;c<gridCols;c++){
        const baseGx=startX+c*stepX;
        const baseGy=startY+r*stepY;
        const offX=Math.sin(phase*8+r*1.7+c*2.3)*vibAmp;
        const offY=Math.cos(phase*8+r*2.1+c*1.5)*vibAmp;
        // Thermal vibrational envelope circle
        svg+='<circle cx="'+baseGx+'" cy="'+baseGy+'" r="'+(vibAmp+4).toFixed(1)+'" fill="#3b82f6" opacity="0.15"/>';
        // Copper Cu2+ ion core
        svg+='<circle cx="'+(baseGx+offX).toFixed(1)+'" cy="'+(baseGy+offY).toFixed(1)+'" r="4.5" fill="#f59e0b" stroke="#fff" stroke-width="0.8"/>';
        svg+='<text x="'+(baseGx+offX).toFixed(1)+'" y="'+(baseGy+offY+2).toFixed(1)+'" text-anchor="middle" fill="#000" font-size="4" font-weight="bold">Cu</text>';
      }
    }
    // Drifting conduction electrons colliding with vibrating ions
    for(let e=0;e<10;e++){
      const tNorm=((phase*1.5+e/10)%1);
      const eX=cX+25+tNorm*(cW-50);
      const eY=cY+40+Math.sin(tNorm*14+e*3)*22+((e*31)%120);
      svg+='<circle cx="'+eX.toFixed(1)+'" cy="'+eY.toFixed(1)+'" r="2.5" fill="#38bdf8"/>';
    }
    svg+='<text x="'+(cX+cW/2)+'" y="'+(cY+cH-8)+'" text-anchor="middle" fill="#93c5fd" font-size="7.5">Conduction Electron Mean Free Path: λ ∝ 1 / ⟨u²⟩ ∝ 1 / T</text>';

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'DRUDE-LORENTZ RESISTIVITY DYNAMICS','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+58)+'" fill="'+ink+'" font-size="9">Lattice Phonon Energy ⟨u²⟩ ∝ k_B T</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="'+ink+'"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+92)+'" fill="#9fb498" font-size="7.5">Scattering cross-section σ_phonon increases linearly with T</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+115)+'" fill="'+orange+'" font-size="9">Mean Collision Time τ = m_e / (n e² ρ)</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    const tau_bar=(130+Math.sin(phase*3)*35).toFixed(1);
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="'+tau_bar+'" height="12" rx="3" fill="'+orange+'"/>';
    // Matthiessen law card
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+145)+'" width="220" height="52" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+162)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">MATTHIESSEN\'S SUPERPOSITION RULE</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+176)+'" text-anchor="middle" fill="#fde68a" font-size="8">ρ_total(T) = ρ_impurity + ρ_phonon(T) ∝ T</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+190)+'" text-anchor="middle" fill="#9fb498" font-size="7.5">Debye Temperature Θ_D = 343 K (70 °C) for pure copper</text>';
    svg+=text(360,305,'Drude Conductivity: σ = n e² τ / m_e · Scattering Rate: 1/τ ∝ ⟨u²⟩ ∝ T ⟹ R(T) = R₀(1 + α T)',soft,10);
  }
  else if(isFaraday){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'HELMHOLTZ DOUBLE-LAYER & CATHODIC REDUCTION','#e2ecd7',11);

    // Cathode boundary at left (negative electrode)
    const catX=cX+25, catY=cY+25, catW=18, catH=170;
    svg+='<rect x="'+catX+'" y="'+catY+'" width="'+catW+'" height="'+catH+'" fill="#64748b" stroke="#94a3b8" stroke-width="1.5"/>';
    svg+='<text x="'+(catX+catW/2)+'" y="'+(catY+catH-10)+'" text-anchor="middle" fill="#fca5a5" font-size="8" font-weight="bold">− (Cathode)</text>';
    // Growing salmon-pink copper microcrystalline deposit layer
    const depW=6+Math.min(12,(phase*2)%14);
    svg+='<rect x="'+(catX+catW)+'" y="'+catY+'" width="'+depW+'" height="'+catH+'" fill="#b45309" stroke="#d97706" stroke-width="1"/>';
    
    // Anode boundary at right (positive electrode)
    const anoX=cX+cW-40, anoY=cY+25, anoW=18, anoH=170;
    svg+='<rect x="'+anoX+'" y="'+anoY+'" width="'+anoW+'" height="'+anoH+'" fill="#b45309" stroke="#d97706" stroke-width="1.5"/>';
    svg+='<text x="'+(anoX+anoW/2)+'" y="'+(anoY+anoH-10)+'" text-anchor="middle" fill="#93c5fd" font-size="8" font-weight="bold">+ (Anode)</text>';

    // Electrolyte solution space between electrodes
    svg+='<rect x="'+(catX+catW+depW)+'" y="'+catY+'" width="'+(anoX-catX-catW-depW)+'" height="'+catH+'" fill="#0284c7" opacity="0.15"/>';
    
    // Hydrated Cu2+ cations drifting from anode toward cathode
    for(let i=0;i<8;i++){
      const tNorm=((phase*1.2+i/8)%1);
      const cuX=anoX-tNorm*(anoX-catX-catW-depW);
      const cuY=catY+25+((i*29)%120);
      svg+='<circle cx="'+cuX.toFixed(1)+'" cy="'+cuY.toFixed(1)+'" r="4.5" fill="#38bdf8" stroke="#fff" stroke-width="0.8"/>';
      svg+='<text x="'+cuX.toFixed(1)+'" y="'+(cuY+2.5)+'" text-anchor="middle" fill="#000" font-size="5" font-weight="bold">Cu²⁺</text>';
    }
    // Sulfate SO4^2- anions migrating toward anode
    for(let j=0;j<5;j++){
      const tNorm=((phase*0.8+j/5)%1);
      const soX=catX+catW+depW+tNorm*(anoX-catX-catW-depW);
      const soY=catY+35+((j*37)%110);
      svg+='<circle cx="'+soX.toFixed(1)+'" cy="'+soY.toFixed(1)+'" r="4" fill="#f59e0b" opacity="0.75"/>';
      svg+='<text x="'+soX.toFixed(1)+'" y="'+(soY+2)+'" text-anchor="middle" fill="#000" font-size="4" font-weight="bold">SO₄²⁻</text>';
    }
    // 2e- electron capture animation at cathode interface
    const eY=catY+70+Math.sin(phase*5)*30;
    svg+='<circle cx="'+(catX+catW+depW-2)+'" cy="'+eY.toFixed(1)+'" r="3" fill="#ef4444"/>';
    svg+='<text x="'+(catX+catW+depW+18)+'" y="'+eY.toFixed(1)+'" fill="#fde68a" font-size="7" font-weight="bold">Cu²⁺ + 2e⁻ ⟶ Cu⁰</text>';

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'QUANTIZED ATOMIC DEPOSITION RATE','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+58)+'" fill="'+ink+'" font-size="9">Mass Deposition Rate dm/dt = Z · I</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="'+ink+'"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+92)+'" fill="#9fb498" font-size="7.5">Constant rate: 0.3293 mg s⁻¹ at I = 1.000 A</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+115)+'" fill="'+orange+'" font-size="9">Atomic Deposition Rate dN/dt = I / (2e)</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    const n_bar=(140+Math.sin(phase*3)*40).toFixed(1);
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="'+n_bar+'" height="12" rx="3" fill="'+orange+'"/>';
    // Faraday constant card
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+145)+'" width="220" height="52" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+162)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">FARADAY & AVOGADRO RELATION</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+176)+'" text-anchor="middle" fill="#fde68a" font-size="8">F = e · N_A = 96485.3 C mol⁻¹ ⟹ N_A = F / e</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+190)+'" text-anchor="middle" fill="#9fb498" font-size="7.5">N_A ≈ 6.022 × 10²³ mol⁻¹ · Elementary charge e = 1.602 × 10⁻¹⁹ C</text>';
    svg+=text(360,305,'Cathode Reaction: Cu²⁺ + 2e⁻ ⟶ Cu⁰ · Deposition: m = (M_Cu / 2F) I t ⇔ Z = M_Cu / 2F',soft,10);
  }
  else if(isElecHeat){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'MICROSCOPIC JOULE HEATING & PHONON DISSIPATION','#e2ecd7',11);

    // Nichrome wire heating channel (solid matrix)
    const wireX=cX+20,wireY=cY+25,wireW=80,wireH=170;
    svg+='<rect x="'+wireX+'" y="'+wireY+'" width="'+wireW+'" height="'+wireH+'" rx="4" fill="#331800" stroke="#f97316" stroke-width="1.5"/>';
    svg+='<text x="'+(wireX+wireW/2)+'" y="'+(wireY+14)+'" text-anchor="middle" fill="#fdba74" font-size="7.5" font-weight="bold">Nichrome Coil (80/20)</text>';

    // Lattice ions vibrating
    for(let i=0;i<6;i++){
      for(let j=0;j<4;j++){
        const ionX=wireX+14+j*18+Math.sin(phase*12+i+j)*2;
        const ionY=wireY+32+i*22+Math.cos(phase*12+i+j)*2;
        svg+='<circle cx="'+ionX.toFixed(1)+'" cy="'+ionY.toFixed(1)+'" r="4" fill="#ea580c" opacity="0.85"/>';
      }
    }

    // Accelerating electrons colliding inelastically with lattice
    for(let k=0;k<5;k++){
      const eProgress=((phase*2.0+k/5)%1);
      const eX=wireX+12+((k*19)%56);
      const eY=wireY+25+eProgress*140;
      svg+='<circle cx="'+eX.toFixed(1)+'" cy="'+eY.toFixed(1)+'" r="2.5" fill="#38bdf8"/>';
      if(eProgress>0.7&&k%2===0){
        // Thermal phonon spark
        svg+='<path d="M'+(eX-3)+' '+(eY-3)+'L'+(eX+3)+' '+(eY+3)+'M'+(eX+3)+' '+(eY-3)+'L'+(eX-3)+' '+(eY+3)+'" stroke="#fef08a" stroke-width="1"/>';
      }
    }

    // Thermal flux arrows crossing sheath into water
    for(let f=0;f<4;f++){
      const arrY=wireY+40+f*32;
      const pulseArrow=Math.sin(phase*6+f)*3;
      svg+='<path d="M'+(wireX+wireW+5)+' '+arrY+' L'+(wireX+wireW+22+pulseArrow)+' '+arrY+'" stroke="#f97316" stroke-width="2"/>';
    }

    // Water reservoir section
    const watX=wireX+wireW+28,watY=wireY,watW=cW-wireW-50,watH=wireH;
    svg+='<rect x="'+watX+'" y="'+watY+'" width="'+watW+'" height="'+watH+'" rx="4" fill="#0369a1" opacity="0.25" stroke="#38bdf8" stroke-width="1"/>';
    svg+='<text x="'+(watX+watW/2)+'" y="'+(watY+14)+'" text-anchor="middle" fill="#7dd3fc" font-size="7.5" font-weight="bold">Water Molecules (Thermalization)</text>';

    // Agitated water molecules (Brownian motion)
    for(let m=0;m<12;m++){
      const molX=watX+15+((m*27)%(watW-30))+Math.sin(phase*8+m)*4;
      const molY=watY+30+((m*21)%(watH-45))+Math.cos(phase*8+m)*4;
      svg+='<circle cx="'+molX.toFixed(1)+'" cy="'+molY.toFixed(1)+'" r="4.5" fill="#0284c7" stroke="#bae6fd" stroke-width="0.8"/>';
      // H atoms
      svg+='<circle cx="'+(molX-3.5).toFixed(1)+'" cy="'+(molY-3).toFixed(1)+'" r="2" fill="#e2ecd7"/>';
      svg+='<circle cx="'+(molX+3.5).toFixed(1)+'" cy="'+(molY-3).toFixed(1)+'" r="2" fill="#e2ecd7"/>';
    }

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'THERMODYNAMIC ENERGY CONSERVATION','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+58)+'" fill="'+ink+'" font-size="9">Electrical Work Input: W = V · I · t (J)</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="'+ink+'"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+92)+'" fill="#9fb498" font-size="7.5">Continuous power P = 25.00 W (10.00 V × 2.500 A)</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+115)+'" fill="'+orange+'" font-size="9">Thermal Internal Energy Gain: Q = C_sys ΔT</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    const q_bar=(180+Math.sin(phase*3)*25).toFixed(1);
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="'+q_bar+'" height="12" rx="3" fill="'+orange+'"/>';
    // Joule equivalence card
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+145)+'" width="220" height="52" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+162)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">CONSERVATION OF ENERGY RATIO</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+176)+'" text-anchor="middle" fill="#fde68a" font-size="8">J = W / Q = 4.1860 J cal⁻¹ (100.0% Equivalence)</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+190)+'" text-anchor="middle" fill="#9fb498" font-size="7.5">Heat Equivalent of Work a = 1 / J = 0.2389 cal J⁻¹</text>';
    svg+=text(360,305,"Microscopic Electron Collisions: dW/dt = I² R ⟹ Inelastic Phonon Production ⟹ dQ/dt = C_sys (dT/dt)",soft,10);
  }
  else if(isPotentiometer){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'POTENTIAL GRADIENT RAMP & GALVANOMETER NULL','#e2ecd7',11);

    // Coordinate grid for V(x) vs x
    const pX=cX+30,pY=cY+25,pW=cW-50,pH=cH-55;
    svg+='<line x1="'+pX+'" y1="'+(pY+pH)+'" x2="'+(pX+pW)+'" y2="'+(pY+pH)+'" stroke="'+soft+'" stroke-width="1.2"/>';
    svg+='<line x1="'+pX+'" y1="'+pY+'" x2="'+pX+'" y2="'+(pY+pH)+'" stroke="'+soft+'" stroke-width="1.2"/>';
    svg+='<text x="'+(pX+pW/2)+'" y="'+(pY+pH+15)+'" text-anchor="middle" fill="#9fb498" font-size="8">Slide-Wire Position x (0 to 100 cm)</text>';
    svg+='<text transform="translate('+(pX-12)+','+(pY+pH/2)+') rotate(-90)" text-anchor="middle" fill="#9fb498" font-size="8">Potential V (Volts)</text>';

    // Linear potential ramp V(x) = k * x (from 0 to 2.0 V)
    svg+='<line x1="'+pX+'" y1="'+(pY+pH)+'" x2="'+(pX+pW)+'" y2="'+pY+'" stroke="'+ink+'" stroke-width="2.5"/>';
    svg+='<text x="'+(pX+pW-10)+'" y="'+(pY-4)+'" fill="'+ink+'" font-size="7.5" font-weight="bold">V(x) = k · x</text>';

    // Horizontal test cell EMF reference line
    const E_norm=p.input/2.000;
    const refY=pY+pH-E_norm*pH;
    svg+='<line x1="'+pX+'" y1="'+refY.toFixed(1)+'" x2="'+(pX+pW)+'" y2="'+refY.toFixed(1)+'" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="3 3"/>';
    svg+='<text x="'+(pX+pW-25)+'" y="'+(refY-5).toFixed(1)+'" fill="#f59e0b" font-size="7.5" font-weight="bold">ℰ_cell = '+p.input.toFixed(3)+' V</text>';

    // Intersection null point (x_null, refY)
    const nullX=pX+E_norm*pW;
    svg+='<circle cx="'+nullX.toFixed(1)+'" cy="'+refY.toFixed(1)+'" r="5" fill="#ef4444" stroke="#fff" stroke-width="1.5"/>';
    svg+='<line x1="'+nullX.toFixed(1)+'" y1="'+refY.toFixed(1)+'" x2="'+nullX.toFixed(1)+'" y2="'+(pY+pH)+'" stroke="#ef4444" stroke-width="1" stroke-dasharray="2 2"/>';
    svg+='<text x="'+nullX.toFixed(1)+'" y="'+(pY+pH-6)+'" text-anchor="middle" fill="#fca5a5" font-size="7" font-weight="bold">ℓ_null</text>';

    // Galvanometer needle deflection indicator at top center
    const galDialX=cX+cW/2,galDialY=cY+35;
    svg+='<circle cx="'+galDialX+'" cy="'+galDialY+'" r="16" fill="#0f172a" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<line x1="'+(galDialX-10)+'" y1="'+galDialY+'" x2="'+(galDialX+10)+'" y2="'+galDialY+'" stroke="#334155" stroke-dasharray="2 2"/>';
    // Pointer resting at exact zero (I_G = 0)
    svg+='<line x1="'+galDialX+'" y1="'+galDialY+'" x2="'+galDialX+'" y2="'+(galDialY-12)+'" stroke="#10b981" stroke-width="2"/>';
    svg+='<circle cx="'+galDialX+'" cy="'+galDialY+'" r="2.5" fill="#10b981"/>';
    svg+='<text x="'+galDialX+'" y="'+(galDialY+22)+'" text-anchor="middle" fill="#10b981" font-size="7" font-weight="bold">I_G = 0.000 μA (NULL)</text>';

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'INFINITE INPUT IMPEDANCE THEOREM','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+58)+'" fill="'+ink+'" font-size="9">Wire Potential: V_wire = k · ℓ = '+p.input.toFixed(4)+' V</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="'+ink+'"/>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+92)+'" fill="#9fb498" font-size="7.5">Potential gradient k = 2.0000 V m⁻¹ (0.02000 V cm⁻¹)</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+115)+'" fill="'+orange+'" font-size="9">Net Galvanometer Branch Field: E_net = 0</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+122)+'" width="4" height="12" rx="1" fill="#10b981"/>';
    // Theorem card
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+145)+'" width="220" height="52" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+162)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">ZERO-CURRENT METROLOGY (R_in ⟶ ∞)</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+176)+'" text-anchor="middle" fill="#fde68a" font-size="8">V_terminal = ℰ − I_G · r_int = ℰ − 0 = ℰ</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+190)+'" text-anchor="middle" fill="#9fb498" font-size="7.5">Zero perturbation of chemical cell equilibrium</text>';
    svg+=text(360,305,"Opposing Potentials: V(ℓ) − ℰ_cell = 0 ⟹ Electron Drift v_d = 0 ⟹ Galvanometer Deflection = 0",soft,10);
  }
  else if(isSpectra){
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#080f14" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'BOHR ATOMIC ORBITS & PHOTON TRANSITION (n ⟶ 2)','#e2ecd7',11);

    const n_curr = Math.round(p.input);
    const centerX = cX + cW/2 - 20;
    const centerY = cY + cH/2;

    const rScale = [0, 16, 32, 50, 70, 92, 116];
    for(let k=1; k<=6; k++){
      const r_k = rScale[k];
      const isBalmer = (k === 2);
      const isSelected = (k === n_curr);
      const strokeCol = isSelected ? '#38bdf8' : isBalmer ? '#10b981' : '#334155';
      const strokeW = (isSelected || isBalmer) ? 1.8 : 0.8;
      const strokeDash = isBalmer ? '4 3' : (isSelected ? 'none' : '2 2');
      svg+='<circle cx="'+centerX+'" cy="'+centerY+'" r="'+r_k+'" fill="none" stroke="'+strokeCol+'" stroke-width="'+strokeW+'" stroke-dasharray="'+strokeDash+'"/>';
      svg+='<text x="'+(centerX+r_k+2)+'" y="'+(centerY-3)+'" fill="'+(isSelected?'#38bdf8':isBalmer?'#10b981':'#64748b')+'" font-size="7">n='+k+'</text>';
    }

    svg+='<circle cx="'+centerX+'" cy="'+centerY+'" r="7" fill="#ef4444" stroke="#fca5a5" stroke-width="1.5"/>';
    svg+='<text x="'+centerX+'" y="'+(centerY+3.5)+'" text-anchor="middle" fill="#ffffff" font-size="8" font-weight="bold">+e</text>';

    const omega = 4.0 / Math.pow(Math.min(6, n_curr), 1.2);
    const theta = (phase * omega * 2 * Math.PI) % (2 * Math.PI);
    const eR = rScale[Math.min(6, n_curr)];
    const eX = centerX + eR * Math.cos(theta);
    const eY = centerY + eR * Math.sin(theta);

    svg+='<circle cx="'+eX.toFixed(1)+'" cy="'+eY.toFixed(1)+'" r="5" fill="#38bdf8" stroke="#ffffff" stroke-width="1.5"/>';
    svg+='<circle cx="'+eX.toFixed(1)+'" cy="'+eY.toFixed(1)+'" r="9" fill="none" stroke="#38bdf8" stroke-width="1" opacity="0.6"/>';

    const r2 = rScale[2];
    const photonAng = -Math.PI / 4;
    const lineCols = {3:'#ef4444', 4:'#06b6d4', 5:'#6366f1', 6:'#8b5cf6', 7:'#a855f7', 8:'#d946ef'};
    const pCol = lineCols[n_curr] || '#38bdf8';

    svg+='<line x1="'+(centerX+eR*0.7)+'" y1="'+(centerY-eR*0.7)+'" x2="'+(centerX+r2*0.7)+'" y2="'+(centerY-r2*0.7)+'" stroke="#f59e0b" stroke-width="2" stroke-dasharray="3 3"/>';
    svg+='<polygon points="'+(centerX+r2*0.7)+','+(centerY-r2*0.7)+' '+(centerX+r2*0.7+4)+','+(centerY-r2*0.7-6)+' '+(centerX+r2*0.7+7)+','+(centerY-r2*0.7-2)+'" fill="#f59e0b"/>';

    const waveProgress = (phase * 1.5) % 1.0;
    const waveDist = r2 + waveProgress * 80;
    const waveX = centerX + waveDist * Math.cos(photonAng);
    const waveY = centerY + waveDist * Math.sin(photonAng);
    svg+='<circle cx="'+waveX.toFixed(1)+'" cy="'+waveY.toFixed(1)+'" r="4.5" fill="'+pCol+'" stroke="#ffffff" stroke-width="1"/>';
    svg+='<text x="'+(waveX+8).toFixed(1)+'" y="'+(waveY-6).toFixed(1)+'" fill="'+pCol+'" font-size="8.5" font-weight="bold">γ (hν)</text>';

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+20,'QUANTIZED ENERGY LEVELS (E_n = -13.6 eV / n²)','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+30)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+30)+'" stroke="#253a34"/>';

    const eTopY = bY + 45;
    const eH = 115;
    const levels = [
      {n:1, E:-13.60, label:'n=1: −13.60 eV (Ground State / Lyman)'},
      {n:2, E:-3.40,  label:'n=2: −3.40 eV (Balmer Base Level)'},
      {n:3, E:-1.51,  label:'n=3: −1.51 eV (Hα transition ΔE = 1.89 eV)'},
      {n:4, E:-0.85,  label:'n=4: −0.85 eV (Hβ transition ΔE = 2.55 eV)'},
      {n:5, E:-0.54,  label:'n=5: −0.54 eV (Hγ transition ΔE = 2.86 eV)'},
      {n:6, E:-0.38,  label:'n=6: −0.38 eV (Hδ transition ΔE = 3.02 eV)'}
    ];

    levels.forEach(lvl=>{
      const yLvl = eTopY + (lvl.E / -13.60) * eH;
      const isSel = (lvl.n === n_curr);
      const isBase = (lvl.n === 2);
      const colL = isSel ? '#38bdf8' : isBase ? '#10b981' : '#64748b';
      svg+='<line x1="'+(bX+25)+'" y1="'+yLvl.toFixed(1)+'" x2="'+(bX+155)+'" y2="'+yLvl.toFixed(1)+'" stroke="'+colL+'" stroke-width="'+(isSel||isBase?2:1)+'"/>';
      svg+='<text x="'+(bX+160)+'" y="'+(yLvl+3.5).toFixed(1)+'" fill="'+colL+'" font-size="7.5" font-family="monospace">'+(lvl.n===2?'★ n=2':'n='+lvl.n)+' ('+lvl.E.toFixed(2)+' eV)</text>';
    });

    const yFrom = eTopY + ((-13.6 / (n_curr * n_curr)) / -13.60) * eH;
    const yTo = eTopY + (-3.40 / -13.60) * eH;
    svg+='<line x1="'+(bX+90)+'" y1="'+yFrom.toFixed(1)+'" x2="'+(bX+90)+'" y2="'+yTo.toFixed(1)+'" stroke="'+pCol+'" stroke-width="2.5"/>';
    svg+='<polygon points="'+(bX+90)+','+yTo.toFixed(1)+' '+(bX+86)+','+(yTo-6).toFixed(1)+' '+(bX+94)+','+(yTo-6).toFixed(1)+'" fill="'+pCol+'"/>';

    const dE = 13.6 * (0.25 - 1.0 / (n_curr * n_curr));
    const h_ev_s = 4.135667696e-15;
    const c_speed = 299792458;
    const lambda_calc = (h_ev_s * c_speed / dE) * 1e9;
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+168)+'" width="220" height="42" rx="4" fill="#0f172a" stroke="'+pCol+'" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+182)+'" text-anchor="middle" fill="'+pCol+'" font-size="8" font-weight="bold">PHOTON ENERGY: ΔE = h · ν = '+dE.toFixed(3)+' eV</text>';
    svg+='<text x="'+(bX+bW/2)+'" y="'+(bY+196)+'" text-anchor="middle" fill="#fde68a" font-size="7.5">λ = h c / ΔE = '+lambda_calc.toFixed(1)+' nm (Measured: '+p.raw.toFixed(1)+' nm)</text>';
    svg+=text(360,305,"Bohr Postulate: Angular Momentum L = n ℏ · Photon Emission: ΔE = E_initial − E_final = h ν",soft,10);
  }
  else{
    const cX=50,cY=50,cW=340,cH=220;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#101c18" stroke="'+soft+'" stroke-width="2" rx="6"/>';
    svg+=text(cX+cW/2,cY-15,'DYNAMIC VECTOR OSCILLOSCOPE (v⃗, a⃗, F⃗_net)','#e2ecd7',11);

    const omega=3.5;
    const oscDisp=Math.cos(phase*omega);
    const oscVel=-Math.sin(phase*omega);
    const oscAcc=-Math.cos(phase*omega);

    const midX=cX+cW/2;
    const bodyX=midX+oscDisp*95;
    const bodyY=cY+cH/2;

    svg+='<line x1="'+midX+'" y1="'+(bodyY-45)+'" x2="'+midX+'" y2="'+(bodyY+45)+'" stroke="'+soft+'" stroke-dasharray="3 3"/>';
    svg+=text(midX,bodyY+58,'Equilibrium x = 0',soft,8);

    svg+='<line x1="'+(cX+20)+'" y1="'+bodyY+'" x2="'+bodyX+'" y2="'+bodyY+'" stroke="'+soft+'" stroke-width="2.5"/>';
    svg+='<circle cx="'+bodyX.toFixed(1)+'" cy="'+bodyY+'" r="16" fill="'+orange+'" stroke="#fde68a" stroke-width="2"/>';

    const vLen=oscVel*45;
    svg+='<line x1="'+bodyX.toFixed(1)+'" y1="'+(bodyY-22)+'" x2="'+(bodyX+vLen).toFixed(1)+'" y2="'+(bodyY-22)+'" stroke="'+ink+'" stroke-width="2.5"/>';
    svg+='<polygon points="'+(bodyX+vLen).toFixed(1)+','+(bodyY-22)+' '+(bodyX+vLen-Math.sign(vLen||1)*6).toFixed(1)+','+(bodyY-25)+' '+(bodyX+vLen-Math.sign(vLen||1)*6).toFixed(1)+','+(bodyY-19)+'" fill="'+ink+'"/>';
    svg+=text(bodyX+vLen/2,bodyY-28,'v⃗',ink,9);

    const aLen=oscAcc*40;
    svg+='<line x1="'+bodyX.toFixed(1)+'" y1="'+(bodyY+24)+'" x2="'+(bodyX+aLen).toFixed(1)+'" y2="'+(bodyY+24)+'" stroke="#38bdf8" stroke-width="2"/>';
    svg+='<polygon points="'+(bodyX+aLen).toFixed(1)+','+(bodyY+24)+' '+(bodyX+aLen-Math.sign(aLen||1)*5).toFixed(1)+','+(bodyY+21)+' '+(bodyX+aLen-Math.sign(aLen||1)*5).toFixed(1)+','+(bodyY+27)+'" fill="#38bdf8"/>';
    svg+=text(bodyX+aLen/2,bodyY+36,'a⃗','#38bdf8',9);

    const bX=420,bY=50,bW=270,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
    svg+=text(bX+bW/2,bY+22,'LIVE MECHANICAL ENERGY CONSERVATION','#718e79',9);
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+32)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+32)+'" stroke="#253a34"/>';

    const Ek=oscVel*oscVel;
    const Ep=oscDisp*oscDisp;

    svg+='<text x="'+(bX+25)+'" y="'+(bY+58)+'" fill="'+ink+'" font-size="9">Kinetic Energy E_k = 1/2 m v²</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+65)+'" width="'+(Ek*220).toFixed(1)+'" height="12" rx="3" fill="'+ink+'"/>';

    svg+='<text x="'+(bX+25)+'" y="'+(bY+100)+'" fill="'+orange+'" font-size="9">Potential Energy E_p = 1/2 k x²</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+107)+'" width="220" height="12" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+107)+'" width="'+(Ep*220).toFixed(1)+'" height="12" rx="3" fill="'+orange+'"/>';

    svg+='<text x="'+(bX+25)+'" y="'+(bY+142)+'" fill="#fde68a" font-size="9">Total Mechanical Energy E_tot = E_k + E_p</text>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+149)+'" width="220" height="14" rx="3" fill="#101c18" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<rect x="'+(bX+25)+'" y="'+(bY+149)+'" width="220" height="14" rx="3" fill="#fde68a"/>';

    svg+='<text x="'+(bX+25)+'" y="'+(bY+185)+'" fill="#9fb498" font-size="8.5">Conservation Law: dE_total / dt = 0 (Conservative Field)</text>';
    svg+='<text x="'+(bX+25)+'" y="'+(bY+202)+'" fill="'+soft+'" font-size="8">Phase Ellipse: (x/x₀)² + (v/v₀)² = 1 (Constant Area)</text>';

    svg+=text(360,305,'Harmonic Oscillations: Vector Calculus F⃗ = m a⃗ = −∇V · Symplectic Phase Space Conservation',soft,10);
  }

  $('apparatusDiagram').innerHTML=svg;
}

function draw(t){
  const p=params(),v=model.predict(cfg.slug,p.input,p.angle),phase=paused?0:t/1000,ink='#c4d7ae',soft='#718e79',orange='#d7a17b';
  if(currentSimMode==='compare'){
    drawComparativeSim(t,p,v,phase,ink,soft,orange);
    return;
  }
  if(currentSimMode==='sandbox'){
    drawDynamicSandbox(t,p,v,phase,ink,soft,orange);
    return;
  }
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern><filter id="blur"><feGaussianBlur stdDeviation="'+(cfg.slug==='convex-lens'?Math.min(10,Math.abs(p.screen-v.ideal)*.45):0)+'"/></filter></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#9fb498',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';
 if(cfg.slug==='simple-pendulum'){const len=115+p.input*85,a=p.angle*Math.PI/180*Math.cos(phase*2*Math.PI/v.period),x=350+len*Math.sin(a),y=55+len*Math.cos(a);svg+='<path d="M260 43H440M350 43V55" stroke="'+soft+'" stroke-width="5"/><line x1="350" y1="55" x2="'+x+'" y2="'+y+'" stroke="'+ink+'" stroke-width="2"/><circle cx="'+x+'" cy="'+y+'" r="17" fill="'+ink+'"/><path d="M490 55V'+(55+len)+'M483 55h14M483 '+(55+len)+'h14" stroke="'+soft+'"/>'+text(530,140,'L = '+p.input.toFixed(2)+' m')+text(350,302,'Length is measured from pivot to bob centre.');}
 else if(cfg.slug==='bifilar-suspension'){const len=100+p.input*90,yaw=p.angle*Math.PI/180*Math.cos(phase*2*Math.PI/v.period),rx=110*Math.cos(yaw),ry=65*Math.sin(yaw),cy=65+len;svg+='<path d="M180 48H530" stroke="'+soft+'" stroke-width="5"/><line x1="245" y1="50" x2="'+(355-rx)+'" y2="'+(cy-ry)+'" stroke="'+ink+'" stroke-width="2"/><line x1="465" y1="50" x2="'+(355+rx)+'" y2="'+(cy+ry)+'" stroke="'+ink+'" stroke-width="2"/><line x1="'+(355-rx*1.6)+'" y1="'+(cy-ry*1.6)+'" x2="'+(355+rx*1.6)+'" y2="'+(cy+ry*1.6)+'" stroke="'+orange+'" stroke-width="13" stroke-linecap="round"/>'+text(355,33,'Full string separation d = 0.20 m')+text(570,150,'L = '+p.input.toFixed(2)+' m')+text(355,305,'Top-oblique schematic · small yaw about the centre');}
 else if(cfg.slug==='young-modulus'){const bottom=210+p.input*2.2;svg+='<path d="M250 40H450" stroke="'+soft+'" stroke-width="6"/><path d="M350 43V'+bottom+'" stroke="'+ink+'" stroke-width="3"/><rect x="320" y="'+bottom+'" width="60" height="28" rx="4" fill="'+orange+'"/><path d="M455 210H530M455 '+bottom+'H530M500 210V'+bottom+'" stroke="'+soft+'" stroke-dasharray="4 4"/>'+text(580,240,'Extension enlarged')+text(350,300,'Incremental load F = '+p.input.toFixed(1)+' N')+text(170,135,'L₀ = 2.00 m')+text(170,160,'d = 0.50 mm');}
 else if(cfg.slug==='stokes-viscosity'){const a=105,b=250,y=a+((phase*v.velocity/.1*20)%1)*(b-a);svg+='<path d="M260 35V280Q360 305 460 280V35" stroke="'+soft+'" stroke-width="3" fill="#728e8010"/><path d="M265 60H455" stroke="'+soft+'"/><path d="M245 '+a+'H475M245 '+b+'H475" stroke="'+orange+'" stroke-dasharray="5 5"/><circle cx="360" cy="'+y+'" r="'+(p.input*15)+'" fill="'+ink+'"/>'+text(535,a+4,'Upper gate')+text(535,b+4,'Lower gate')+text(540,180,'s = 0.100 m')+text(360,318,'Sphere and motion enlarged · accelerated preview')+text(145,150,'r = '+p.input.toFixed(2)+' mm')+text(145,180,'Re ≈ '+v.reynolds.toFixed(4));}
 else if(cfg.slug==='ohms-law'){const current=v.ideal;svg+='<path d="M150 230V90H280M440 90H570V230H150" fill="none" stroke="'+ink+'" stroke-width="2"/><rect x="280" y="77" width="160" height="26" rx="4" stroke="'+orange+'" fill="#20312d"/><circle cx="570" cy="160" r="28" fill="#20312d" stroke="'+soft+'"/><circle cx="215" cy="230" r="28" fill="#20312d" stroke="'+soft+'"/><path d="M300 90V170H420V90" fill="none" stroke="'+soft+'"/><circle cx="360" cy="170" r="26" fill="#20312d" stroke="'+soft+'"/>'+text(360,97,'100 Ω',orange)+text(570,166,'A',ink,20)+text(360,176,'V',ink,20)+text(215,236,p.input.toFixed(1)+' V',ink)+text(360,285,'Series ammeter · parallel voltmeter')+text(570,207,current.toFixed(2)+' mA');const cx=150+((phase*current/10)%1)*420;svg+='<circle cx="'+cx+'" cy="230" r="4" fill="'+orange+'"/>';}
 else if(cfg.slug==='metre-bridge'){const j=120+p.balance*4.8,deflect=Math.max(-28,Math.min(28,(p.balance-v.ideal)*3));svg+='<path d="M120 240H600M120 240V80H270M330 80H430M490 80H600V240M380 80V150" fill="none" stroke="'+ink+'" stroke-width="2"/><rect x="270" y="65" width="60" height="30" stroke="'+orange+'" fill="#20312d"/><rect x="430" y="65" width="60" height="30" stroke="'+orange+'" fill="#20312d"/><circle cx="380" cy="175" r="25" stroke="'+soft+'" fill="none"/><path d="M380 196L'+(380+deflect)+' 159M380 200L'+j+' 240" stroke="'+orange+'"/><circle cx="'+j+'" cy="240" r="6" fill="'+orange+'"/>'+text(300,53,'Unknown R')+text(460,53,'S = '+p.input.toFixed(1)+' Ω')+text(380,140,Math.abs(p.balance-v.ideal)<=.050001?'NULL':'G: not balanced')+text(120,267,'0 cm')+text(600,267,'100 cm')+text(j,293,'Jockey: '+p.balance.toFixed(1)+' cm')+text(380,27,'Wheatstone bridge · schematic supply across wire ends');}
 else if(cfg.slug==='rc-charging'){const cx=t=>110+t/3*490,cy=volt=>250-volt/5*185;let points=[];for(let j=0;j<=100;j++){const t=j*.03;points.push(cx(t)+','+cy(5*(1-Math.exp(-t))));}svg+='<path d="M110 55V250H620" stroke="'+soft+'" fill="none"/><polyline points="'+points.join(' ')+'" stroke="'+ink+'" fill="none" stroke-width="2"/><path d="M110 65H620" stroke="'+soft+'" stroke-dasharray="5 5"/><line x1="'+cx(p.input)+'" y1="250" x2="'+cx(p.input)+'" y2="'+cy(v.ideal)+'" stroke="'+orange+'"/><circle cx="'+cx(p.input)+'" cy="'+cy(v.ideal)+'" r="6" fill="'+orange+'"/>'+text(350,300,'Elapsed time t = '+p.input.toFixed(1)+' s')+text(380,35,'Charging curve · E = 5 V · R = 10 kΩ')+text(70,65,'5 V')+text(70,250,'0 V')+text(590,282,'3 s')+text(270,120,'Vc = '+v.ideal.toFixed(3)+' V');}
 else if(cfg.slug==='glass-slab'){const top=80,bottom=80+p.input*10,apparent=top+v.ideal*10;svg+='<rect x="180" y="'+top+'" width="360" height="'+(bottom-top)+'" fill="#abc8ae16" stroke="'+ink+'"/><path d="M180 '+bottom+'H540" stroke="'+orange+'"/><path d="M230 '+apparent+'H490" stroke="'+orange+'" stroke-dasharray="5 5"/><path d="M340 35H380V58H340ZM360 58V76" fill="none" stroke="'+soft+'"/><path d="M360 '+apparent+'L330 80L345 58M360 '+apparent+'L390 80L375 58" fill="none" stroke="'+ink+'" opacity=".7"/>'+text(360,25,'Travelling microscope · paraxial schematic')+text(610,top+4,'Top surface R₂')+text(610,bottom+4,'Real mark R₁')+text(100,apparent+4,'Apparent R₃')+text(360,285,'Real depth: '+p.input.toFixed(1)+' mm · apparent depth is measured from the top')+text(360,310,'Focus and scale alignment are idealised in this model.');}
 else if(cfg.slug==='diffraction-grating'){const angle=v.ideal* Math.PI/180,dy=140*Math.sin(angle),rayX=300+140*Math.cos(angle);svg+='<path d="M70 160H300M300 50V270M300 160H650" stroke="'+ink+'" fill="none"/><path d="M300 160L'+rayX+' '+(160-dy)+'M300 160L'+rayX+' '+(160+dy)+'" stroke="'+orange+'" fill="none"/><path d="M300 110V210" stroke="'+ink+'" stroke-width="8"/>'+text(165,140,'Normal incident light')+text(300,30,'300 lines/mm')+text(530,80,'Order +'+p.input)+text(530,250,'Order −'+p.input)+text(510,152,'θ = '+v.raw.toFixed(2)+'°')+text(360,305,'Symmetric telescope readings · rays schematic');}
  else if(cfg.slug==='convex-lens'){const lens=350,y0=160,h=40,obj=lens-p.input*4,image=lens+v.ideal*4,screen=lens+p.screen*4,ih=h*v.magnification;svg+='<path d="M40 '+y0+'H690" stroke="'+soft+'" stroke-dasharray="5 5"/><path d="M350 60Q323 160 350 260Q377 160 350 60Z" fill="#abc8ae20" stroke="'+ink+'"/><path d="M'+obj+' '+y0+'V'+(y0-h)+'l-5 8m5-8 5 8" stroke="'+orange+'" stroke-width="3" fill="none"/><path d="M'+obj+' '+(y0-h)+'H350L'+image+' '+(y0+ih)+'M'+obj+' '+(y0-h)+'L'+image+' '+(y0+ih)+'" stroke="#c6b6e0" opacity=".65" fill="none"/><path d="M'+screen+' 55V270" stroke="'+soft+'" stroke-width="4"/><path d="M'+screen+' '+y0+'V'+(y0+ih)+'l-5-8m5 8 5-8" stroke="'+orange+'" stroke-width="4" fill="none" filter="url(#blur)"/><circle cx="290" cy="160" r="3" fill="'+ink+'"/><circle cx="410" cy="160" r="3" fill="'+ink+'"/>'+text(290,181,'F')+text(410,181,'F')+text(obj,290,'Object')+text(lens,290,'Lens')+text(screen,310,'Screen')+text(360,30,Math.abs(p.screen-v.ideal)<=.050001?'Sharp inverted image':'Move screen to sharpen the image');}
  else if(cfg.slug==='hookes-law'){const y0=60,yEnd=y0+55+v.ideal*0.9,nCoils=14,pitch=(yEnd-y0)/nCoils;let coilPath='M270 52V'+y0;for(let k=0;k<nCoils;k+=2){const yk=y0+pitch*k;coilPath+=' C252 '+(yk+pitch*0.5)+', 252 '+(yk+pitch*1.0)+', 270 '+(yk+pitch)+' C288 '+(yk+pitch*1.5)+', 288 '+(yk+pitch*2.0)+', 270 '+(yk+pitch*2);}
  svg+='<path d="M190 285H270M210 285V40H270M270 40V52" stroke="'+soft+'" stroke-width="4" fill="none"/><path d="'+coilPath+'" stroke="'+ink+'" stroke-width="2.5" fill="none"/><line x1="270" y1="'+yEnd+'" x2="380" y2="'+yEnd+'" stroke="'+orange+'" stroke-width="2"/><polygon points="380,'+yEnd+' 370,'+(yEnd-4)+' 370,'+(yEnd+4)+'" fill="'+orange+'"/><rect x="380" y="55" width="28" height="215" fill="#20312d" stroke="'+soft+'"/>';
  for(let j=0;j<=6;j++){const yMark=60+j*30,val=j*20;svg+='<line x1="380" y1="'+yMark+'" x2="390" y2="'+yMark+'" stroke="'+ink+'"/><text x="400" y="'+(yMark+4)+'" fill="#9fb498" font-size="9">'+val+'</text>';}
  const weightH=Math.min(30,p.input*10);svg+='<line x1="270" y1="'+yEnd+'" x2="270" y2="'+(yEnd+25)+'" stroke="'+ink+'" stroke-width="2"/><rect x="252" y="'+(yEnd+25)+'" width="36" height="5" rx="1" fill="'+soft+'"/><rect x="254" y="'+(yEnd+25-weightH)+'" width="32" height="'+weightH+'" rx="2" fill="'+orange+'"/>'+text(540,85,'Helical spring (k = 25 N/m)')+text(540,115,'Load F = '+p.input.toFixed(2)+' N')+text(540,145,'Extension δ = '+v.raw.toFixed(1)+' mm')+text(540,175,'Mass m ≈ '+(p.input/9.80665*1000).toFixed(1)+' g')+text(360,305,'Vertical retort stand · Anti-parallax mirror millimeter scale');}
  else if(cfg.slug==='density-measurement'){const bY=115,pLeft=130,pRight=270,fX=200,cylH=Math.min(48,p.input*0.8);svg+='<path d="M120 280H280M200 280V'+(bY+5)+'M170 280L200 260L230 280" stroke="'+soft+'" stroke-width="4" fill="none"/><polygon points="194,'+(bY+12)+' 206,'+(bY+12)+' 200,'+bY+'" fill="'+soft+'"/><line x1="'+pLeft+'" y1="'+bY+'" x2="'+pRight+'" y2="'+bY+'" stroke="'+ink+'" stroke-width="4"/><line x1="'+fX+'" y1="'+bY+'" x2="'+fX+'" y2="'+(bY+65)+'" stroke="'+orange+'" stroke-width="2"/><path d="M190 '+(bY+65)+'H210" stroke="'+soft+'"/><path d="M'+pLeft+' '+bY+'L110 190H150L'+pLeft+' '+bY+'" stroke="'+soft+'" fill="none"/><line x1="105" y1="190" x2="155" y2="190" stroke="'+ink+'" stroke-width="3"/><rect x="117" y="'+(190-cylH)+'" width="26" height="'+cylH+'" rx="3" fill="'+orange+'" stroke="#f0b691"/><path d="M'+pRight+' '+bY+'L250 190H290L'+pRight+' '+bY+'" stroke="'+soft+'" fill="none"/><line x1="245" y1="190" x2="295" y2="190" stroke="'+ink+'" stroke-width="3"/><rect x="255" y="174" width="30" height="16" rx="2" fill="'+soft+'"/><rect x="260" y="160" width="20" height="14" rx="2" fill="'+soft+'"/>';const waterLevel=220-p.input*1.8;svg+='<path d="M420 50V270Q470 285 520 270V50" stroke="'+soft+'" stroke-width="3" fill="#182824"/><path d="M422 '+waterLevel+'H518V268Q470 282 422 268Z" fill="#58a4b025"/><ellipse cx="470" cy="'+waterLevel+'" rx="48" ry="6" fill="#78b4c040" stroke="'+ink+'" stroke-width="1"/><line x1="470" y1="40" x2="470" y2="'+(260-cylH)+'" stroke="'+soft+'" stroke-dasharray="3 3"/><rect x="457" y="'+(260-cylH)+'" width="26" height="'+cylH+'" rx="3" fill="'+orange+'" opacity=".85"/>';for(let g=0;g<=5;g++){const gy=260-g*36;svg+='<line x1="420" y1="'+gy+'" x2="430" y2="'+gy+'" stroke="'+soft+'"/><text x="412" y="'+(gy+4)+'" text-anchor="end" fill="#9fb498" font-size="9">'+(g*20)+'</text>';}svg+=text(200,35,'Dual-pan precision balance')+text(200,305,'Mass M = '+v.raw.toFixed(2)+' g')+text(470,35,'Graduated cylinder')+text(470,305,'Displaced V = '+p.input.toFixed(1)+' cm³')+text(630,120,'Pure copper (Cu)')+text(630,145,'ρ = M / V')+text(630,170,'≈ '+(v.raw/p.input).toFixed(2)+' g/cm³')+text(630,195,'= '+(v.raw/p.input*1000).toFixed(1)+' kg/m³');}
  else if(cfg.slug==='vernier-micrometer'){const scale=4.0,gap=p.input*scale,fixedX=140,slideX=fixedX+gap,cylDiam=Math.min(90,p.input*2.2);svg+='<rect x="70" y="75" width="580" height="42" rx="3" fill="#1b2a26" stroke="'+soft+'" stroke-width="2"/><path d="M70 75V250L100 250L140 160V117H70" fill="#243833" stroke="'+soft+'" stroke-width="2"/><path d="M105 75V35L125 50V75M'+(slideX+35)+' 75V35L'+(slideX+15)+' 50V75" stroke="'+soft+'" fill="none" stroke-width="2"/><rect x="140" y="'+(245-cylDiam)+'" width="'+gap+'" height="'+cylDiam+'" rx="4" fill="'+orange+'" stroke="#f0b691"/><path d="M'+slideX+' 68V250L'+(slideX+35)+' 250L'+(slideX+70)+' 160V125H'+(slideX+130)+'V68Z" fill="#2d443e" stroke="'+ink+'" stroke-width="2"/>';for(let m=0;m<=12;m++){const mx=140+m*35;if(mx<=640){svg+='<line x1="'+mx+'" y1="102" x2="'+mx+'" y2="117" stroke="'+ink+'" stroke-width="1.5"/><text x="'+mx+'" y="96" text-anchor="middle" fill="#9fb498" font-size="9">'+(m*10)+'</text>';}}svg+='<rect x="'+(slideX+5)+'" y="76" width="60" height="26" fill="#13201d" stroke="'+soft+'"/>';for(let vi=0;vi<=5;vi++){const vx=slideX+10+vi*9.8;svg+='<line x1="'+vx+'" y1="76" x2="'+vx+'" y2="86" stroke="'+orange+'"/><text x="'+vx+'" y="97" text-anchor="middle" fill="'+orange+'" font-size="8">'+(vi*2)+'</text>';}svg+=text(360,25,'Precision Vernier Caliper · Least Count 0.02 mm')+text(200,285,'Cylinder Diameter d = '+p.input.toFixed(1)+' mm')+text(530,175,'Perimeter Circumference')+text(530,200,'C = πd = '+v.raw.toFixed(2)+' mm')+text(530,225,'π ≈ C/d = '+(v.raw/p.input).toFixed(5))+text(530,250,'OLS slope m → 3.14159')+text(360,310,'Sliding vernier coincidence · External measurement jaws');}
   else if(cfg.slug==='friction-laws'){const bedY=220,bW=Math.min(48,p.input*3.2),dynDisp=Math.min(50,v.raw*14);svg+='<path d="M70 '+bedY+'H650M100 '+bedY+'V270M620 '+bedY+'V270" stroke="'+soft+'" stroke-width="4"/><line x1="70" y1="'+(bedY+8)+'" x2="650" y2="'+(bedY+8)+'" stroke="#1b2a26" stroke-width="8"/><rect x="180" y="'+(bedY-38)+'" width="110" height="38" rx="2" fill="#805d3b" stroke="#a67c52" stroke-width="2"/><rect x="200" y="'+(bedY-38-bW)+'" width="70" height="'+bW+'" rx="2" fill="'+orange+'" stroke="#f0b691"/><line x1="290" y1="'+(bedY-18)+'" x2="340" y2="'+(bedY-18)+'" stroke="'+ink+'" stroke-width="2"/><rect x="340" y="'+(bedY-28)+'" width="160" height="20" rx="3" fill="#1b2a26" stroke="'+soft+'" stroke-width="2"/>';for(let k=0;k<=5;k++){const sx=350+k*24;svg+='<line x1="'+sx+'" y1="'+(bedY-28)+'" x2="'+sx+'" y2="'+(bedY-20)+'" stroke="'+soft+'"/><text x="'+sx+'" y="'+(bedY-11)+'" text-anchor="middle" fill="#9fb498" font-size="8">'+k+'</text>';}svg+='<line x1="340" y1="'+(bedY-18)+'" x2="'+(350+dynDisp)+'" y2="'+(bedY-18)+'" stroke="'+orange+'" stroke-width="3"/><polygon points="'+(350+dynDisp)+','+(bedY-26)+' '+(356+dynDisp)+','+(bedY-18)+' '+(350+dynDisp)+','+(bedY-10)+'" fill="'+orange+'"/><line x1="500" y1="'+(bedY-18)+'" x2="540" y2="'+(bedY-18)+'" stroke="'+ink+'" stroke-width="2"/><circle cx="548" cy="'+(bedY-18)+'" r="8" fill="none" stroke="'+soft+'" stroke-width="2"/><path d="M290 140H350L340 135M350 140L340 145" stroke="'+ink+'" stroke-width="2" fill="none"/><text x="320" y="130" text-anchor="middle" fill="#9fb498" font-size="10">v ≈ 0.05 m/s</text>';svg+=text(360,35,'Horizontal Friction Bed & Tubular Dynamometer')+text(235,275,'Normal Load N = '+p.input.toFixed(1)+' N')+text(435,275,'Traction Force Ff = '+v.raw.toFixed(2)+' N')+text(600,105,'Interfacial contact')+text(600,130,'Maple on maple')+text(600,155,'Ff = μ N')+text(600,180,'μ ≈ '+(v.raw/p.input).toFixed(3))+text(360,305,'Amontons-Coulomb kinetic friction · Uniform horizontal traction');}
   else if(cfg.slug==='principle-of-moments'){const rY=140,rH=18,rLeft=75,rRight=645,rW=rRight-rLeft,pxPerCm=5.7,pX=rLeft+35.0*pxPerCm,cgX=rLeft+50.0*pxPerCm,mPosCm=35.0-v.ideal,mX=rLeft+mPosCm*pxPerCm,wH=Math.min(38,Math.max(16,p.input*0.24));svg+='<rect x="'+rLeft+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="2" fill="#c49a6c" stroke="#8b6834" stroke-width="2"/>';for(let k=0;k<=10;k++){const tx=rLeft+k*57;svg+='<line x1="'+tx+'" y1="'+rY+'" x2="'+tx+'" y2="'+(rY+6)+'" stroke="#5a3d1b" stroke-width="1.5"/><text x="'+tx+'" y="'+(rY+14)+'" text-anchor="middle" fill="#5a3d1b" font-size="8">'+(k*10)+'</text>';}svg+='<polygon points="'+pX+','+(rY+rH)+' '+(pX-12)+','+(rY+rH+20)+' '+(pX+12)+','+(rY+rH+20)+'" fill="#889e80" stroke="'+soft+'" stroke-width="1.5"/><rect x="'+(pX-6)+'" y="'+(rY+rH+20)+'" width="12" height="75" fill="#20312d" stroke="'+soft+'"/><rect x="'+(pX-48)+'" y="'+(rY+rH+95)+'" width="96" height="16" rx="3" fill="#1b2a26" stroke="'+soft+'" stroke-width="2"/><circle cx="'+cgX+'" cy="'+(rY+rH/2)+'" r="4.5" fill="'+orange+'" stroke="#fff" stroke-width="1.5"/><line x1="'+cgX+'" y1="'+(rY+rH)+'" x2="'+cgX+'" y2="'+(rY+rH+50)+'" stroke="'+orange+'" stroke-width="2.5"/><polygon points="'+cgX+','+(rY+rH+56)+' '+(cgX-4)+','+(rY+rH+48)+' '+(cgX+4)+','+(rY+rH+48)+'" fill="'+orange+'"/>'+text(cgX,rY+rH+70,'W_rule = 1.18 N (120 g)',orange,10)+'<path d="M'+pX+' '+(rY-12)+'H'+cgX+'M'+pX+' '+(rY-17)+'V'+(rY-7)+'M'+cgX+' '+(rY-17)+'V'+(rY-7)+'" stroke="'+soft+'" stroke-width="1.5"/>'+text((pX+cgX)/2,rY-20,'d_rule = 15.0 cm',soft,10)+'<rect x="'+(mX-5)+'" y="'+(rY-2)+'" width="10" height="'+(rH+4)+'" rx="2" fill="none" stroke="'+ink+'" stroke-width="2"/><line x1="'+mX+'" y1="'+(rY+rH+2)+'" x2="'+mX+'" y2="'+(rY+rH+30)+'" stroke="'+ink+'" stroke-width="1.5"/><rect x="'+(mX-12)+'" y="'+(rY+rH+30)+'" width="24" height="'+wH+'" rx="2" fill="'+orange+'" stroke="#f0b691"/><line x1="'+mX+'" y1="'+(rY+rH+30)+'" x2="'+mX+'" y2="'+(rY+rH+30+wH+10)+'" stroke="'+ink+'" stroke-width="2"/><rect x="'+(mX-14)+'" y="'+(rY+rH+30+wH+10)+'" width="28" height="4" rx="1" fill="'+soft+'"/>'+text(mX,rY+rH+30+wH+24,'m = '+p.input.toFixed(1)+' g',ink,10)+'<path d="M'+mX+' '+(rY-12)+'H'+pX+'M'+mX+' '+(rY-17)+'V'+(rY-7)+'M'+pX+' '+(rY-17)+'V'+(rY-7)+'" stroke="'+orange+'" stroke-width="1.5"/>'+text((mX+pX)/2,rY-20,'d_m = '+v.raw.toFixed(1)+' cm',orange,10)+'<rect x="440" y="'+(rY-14)+'" width="56" height="12" rx="3" fill="#20312d" stroke="'+soft+'"/><line x1="462" y1="'+(rY-14)+'" x2="462" y2="'+(rY-2)+'" stroke="'+soft+'" stroke-width="1"/><line x1="474" y1="'+(rY-14)+'" x2="474" y2="'+(rY-2)+'" stroke="'+soft+'" stroke-width="1"/><circle cx="468" cy="'+(rY-8)+'" r="3.5" fill="#9fe690"/>'+text(468,rY-20,'Horizontal Level','#9fe690',9)+text(360,25,'Hardwood Meter Rule on Low-Friction Knife-Edge Fulcrum')+text(140,48,'Fulcrum: x₀ = 35.0 cm',soft,11)+text(580,48,'Rule CG: x_cg = 50.0 cm',soft,11)+text(575,195,'Clockwise moment (rule):',soft,11)+text(575,212,'τ_cw = M_rule · g · d_rule',soft,11)+text(575,238,'Counter-clockwise (load):',orange,11)+text(575,255,'τ_ccw = m · g · d_m',orange,11)+text(360,305,'Rotational Equilibrium: Σ τ = 0 ⇒ m · d_m = M_rule · d_rule ⇒ d_m = (M_rule · d_rule) / m');}
   else if(cfg.slug==='force-table'){const cx=360,cy=160,R=110,rad=p.input*Math.PI/180,x1=cx+R*Math.cos(rad),y1=cy-R*Math.sin(rad),x2=cx+R*Math.cos(rad),y2=cy+R*Math.sin(rad),x3=cx-R,y3=cy,wH_F=26,wH_E=Math.min(42,Math.max(18,v.raw*0.12));svg+='<circle cx="'+cx+'" cy="'+cy+'" r="'+(R+12)+'" fill="#182824" stroke="'+soft+'" stroke-width="4"/><circle cx="'+cx+'" cy="'+cy+'" r="'+R+'" fill="#20312d" stroke="'+ink+'" stroke-width="1.5"/>';for(let d=0;d<360;d+=30){const da=d*Math.PI/180,gx1=cx+(R-6)*Math.cos(da),gy1=cy-(R-6)*Math.sin(da),gx2=cx+R*Math.cos(da),gy2=cy-R*Math.sin(da);svg+='<line x1="'+gx1+'" y1="'+gy1+'" x2="'+gx2+'" y2="'+gy2+'" stroke="'+soft+'" stroke-width="1.5"/>';const tx=cx+(R-15)*Math.cos(da),ty=cy-(R-15)*Math.sin(da)+3;svg+='<text x="'+tx+'" y="'+ty+'" text-anchor="middle" fill="#9fb498" font-size="8">'+d+'°</text>';}svg+='<line x1="'+(cx-R)+'" y1="'+cy+'" x2="'+(cx+R)+'" y2="'+cy+'" stroke="#364e46" stroke-dasharray="3 3"/><line x1="'+cx+'" y1="'+(cy-R)+'" x2="'+cx+'" y2="'+(cy+R)+'" stroke="#364e46" stroke-dasharray="3 3"/>';[[x1,y1],[x2,y2],[x3,y3]].forEach(([px,py])=>{svg+='<circle cx="'+px+'" cy="'+py+'" r="7" fill="#889e80" stroke="#5b7454" stroke-width="1.5"/><circle cx="'+px+'" cy="'+py+'" r="2" fill="#20312d"/>';});svg+='<line x1="'+cx+'" y1="'+cy+'" x2="'+x1+'" y2="'+y1+'" stroke="'+ink+'" stroke-width="2"/><line x1="'+cx+'" y1="'+cy+'" x2="'+x2+'" y2="'+y2+'" stroke="'+ink+'" stroke-width="2"/><line x1="'+cx+'" y1="'+cy+'" x2="'+x3+'" y2="'+y3+'" stroke="'+orange+'" stroke-width="2.5"/><line x1="'+x1+'" y1="'+y1+'" x2="'+(x1+25)+'" y2="'+(y1+45)+'" stroke="'+ink+'" stroke-width="1.5"/><rect x="'+(x1+15)+'" y="'+(y1+45)+'" width="20" height="'+wH_F+'" rx="2" fill="'+soft+'" stroke="#9fb498"/>'+text(x1+25,y1+45+wH_F+12,'F₁ = 150 g',ink,9)+'<line x1="'+x2+'" y1="'+y2+'" x2="'+(x2+25)+'" y2="'+(y2+45)+'" stroke="'+ink+'" stroke-width="1.5"/><rect x="'+(x2+15)+'" y="'+(y2+45)+'" width="20" height="'+wH_F+'" rx="2" fill="'+soft+'" stroke="#9fb498"/>'+text(x2+25,y2+45+wH_F+12,'F₂ = 150 g',ink,9)+'<line x1="'+x3+'" y1="'+y3+'" x2="'+(x3-30)+'" y2="'+(y3+45)+'" stroke="'+orange+'" stroke-width="1.5"/><rect x="'+(x3-42)+'" y="'+(y3+45)+'" width="24" height="'+wH_E+'" rx="2" fill="'+orange+'" stroke="#f0b691"/>'+text(x3-30,y3+45+wH_E+12,'E = '+v.raw.toFixed(1)+' g',orange,10)+'<circle cx="'+cx+'" cy="'+cy+'" r="3" fill="#718e79"/><circle cx="'+cx+'" cy="'+cy+'" r="11" fill="none" stroke="'+orange+'" stroke-width="2"/>';const rLen=R*Math.cos(rad);svg+='<line x1="'+cx+'" y1="'+cy+'" x2="'+(cx+rLen)+'" y2="'+cy+'" stroke="'+orange+'" stroke-width="2" stroke-dasharray="3 3"/><polygon points="'+(cx+rLen)+','+cy+' '+(cx+rLen-6)+','+(cy-3)+' '+(cx+rLen-6)+','+(cy+3)+'" fill="'+orange+'"/>'+text(cx,22,'Precision Circular Force Table (360° Graduated Rim)')+text(cx,38,'Symmetric Concurrent Forces: F₁ = F₂ = 150.0 g at ±'+p.input.toFixed(1)+'°',soft,11)+text(cx+rLen/2,cy-8,'R = 2 F cos θ',orange,9)+text(110,65,'Equilibrant Vector (E):',soft,11)+text(110,82,'θ_E = 180°',soft,11)+text(110,99,'m_E = '+v.raw.toFixed(1)+' g',orange,12)+text(610,65,'Resultant Vector (R):',soft,11)+text(610,82,'θ_R = 0° (along x-axis)',soft,11)+text(610,99,'R = '+v.raw.toFixed(1)+' g',orange,12)+text(cx,305,'Vector Equilibrium: Σ F = F₁ + F₂ + E = 0 ⇔ m_E = 2 M₀ cos(θ)');}
   else if(cfg.slug==='flywheel-inertia'){const cx=240,cy=160,R_outer=95,R_inner=22,drumR=16,rotAngle=t*0.004,hangY=cy+drumR+40+(p.input/0.15)*50;svg+='<rect x="50" y="280" width="380" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><line x1="240" y1="280" x2="240" y2="160" stroke="#1b2a26" stroke-width="12"/><line x1="220" y1="280" x2="240" y2="160" stroke="'+soft+'" stroke-width="3"/><line x1="260" y1="280" x2="240" y2="160" stroke="'+soft+'" stroke-width="3"/>';svg+='<circle cx="'+cx+'" cy="'+cy+'" r="'+R_outer+'" fill="#20312d" stroke="'+soft+'" stroke-width="6"/><circle cx="'+cx+'" cy="'+cy+'" r="'+(R_outer-12)+'" fill="#182824" stroke="#253a34" stroke-width="2"/>';for(let d=0;d<360;d+=45){const da=(d*Math.PI/180)+rotAngle,sx=cx+(R_outer-18)*Math.cos(da),sy=cy+(R_outer-18)*Math.sin(da),ix=cx+R_inner*Math.cos(da),iy=cy+R_inner*Math.sin(da);svg+='<line x1="'+ix+'" y1="'+iy+'" x2="'+sx+'" y2="'+sy+'" stroke="'+soft+'" stroke-width="3"/><circle cx="'+sx+'" cy="'+sy+'" r="4" fill="'+orange+'"/>';}svg+='<circle cx="'+cx+'" cy="'+cy+'" r="'+R_inner+'" fill="#364e46" stroke="'+ink+'" stroke-width="2"/><circle cx="'+cx+'" cy="'+cy+'" r="'+drumR+'" fill="#182824" stroke="'+orange+'" stroke-width="2"/>';svg+='<line x1="'+(cx+drumR)+'" y1="'+cy+'" x2="'+(cx+drumR)+'" y2="'+hangY+'" stroke="'+ink+'" stroke-width="2"/><rect x="'+(cx+drumR-10)+'" y="'+hangY+'" width="20" height="26" rx="3" fill="'+orange+'" stroke="#f0b691"/>'+text(cx+drumR,hangY+38,'τ = '+p.input.toFixed(3)+' N m',orange,9);const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">ANGULAR ACCELERATION (α)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.raw.toFixed(3)+'</text><text x="'+(bX+95)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="10">rad s⁻²</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">APPLIED TORQUE (τ)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+p.input.toFixed(3)+' N m</text><text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#9fb498" font-size="8">Drum r = 0.020 m</text><line x1="'+(bX+15)+'" y1="'+(bY+135)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+135)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+152)+'" fill="#718e79" font-size="9">MOMENT OF INERTIA (I)</text><text x="'+(bX+15)+'" y="'+(bY+176)+'" fill="'+orange+'" font-size="18" font-family="monospace" font-weight="bold">I = 0.0500 kg m²</text><text x="'+(bX+15)+'" y="'+(bY+192)+'" fill="#9fb498" font-size="8">Disk M = 4.00 kg, R = 0.158 m</text><line x1="'+(bX+15)+'" y1="'+(bY+200)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+200)+'" stroke="#253a34"/>'+text(bX+15,bY+214,'α = (1 / I) · τ ⇔ I = 1 / S',ink,9)+text(240,22,'Precision Flywheel Rotational Dynamics System')+text(240,308,'Newton\'s Second Law for Rotation: τ = I · α');}
   else if(cfg.slug==='specific-heat-capacity'){const calX=270,calY=175,calW=140,calH=105,tMerc=Math.min(100,Math.max(15,(v.raw-18)*10)),qAbs=920.92*(v.raw-20.0);svg+='<rect x="40" y="280" width="410" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="70" y="110" width="90" height="150" rx="6" fill="#20312d" stroke="'+soft+'" stroke-width="2"/><rect x="78" y="125" width="74" height="120" rx="3" fill="#182824" stroke="#253a34"/><line x1="60" y1="260" x2="170" y2="260" stroke="#364e46" stroke-width="3"/><polygon points="105,275 115,260 125,275" fill="'+orange+'"/><text x="115" y="100" text-anchor="middle" fill="'+soft+'" font-size="9">STEAM BOILER (100°C)</text><line x1="115" y1="65" x2="115" y2="180" stroke="#e2e8f0" stroke-width="4"/><line x1="115" y1="120" x2="115" y2="180" stroke="#ef4444" stroke-width="2"/><rect x="100" y="175" width="30" height="25" rx="3" fill="#b45309" stroke="'+orange+'" stroke-width="1.5"/><text x="115" y="191" text-anchor="middle" fill="#fff" font-size="8">Cu</text><path d="M115 175 C140 140, 200 130, 250 170" fill="none" stroke="'+orange+'" stroke-width="1.5" stroke-dasharray="4 3"/><rect x="'+(calX-calW/2)+'" y="'+(calY-10)+'" width="'+calW+'" height="'+calH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="2"/><rect x="'+(calX-calW/2+15)+'" y="'+calY+'" width="'+(calW-30)+'" height="'+(calH-18)+'" rx="4" fill="#b45309" stroke="#d97706" stroke-width="1.5"/><rect x="'+(calX-calW/2+17)+'" y="'+(calY+20)+'" width="'+(calW-34)+'" height="'+(calH-40)+'" rx="2" fill="#0284c7" opacity="0.6"/><rect x="'+(calX-15)+'" y="'+(calY+calH-40)+'" width="30" height="20" rx="3" fill="#d97706" stroke="'+orange+'" stroke-width="1.5"/><text x="'+calX+'" y="'+(calY+calH-27)+'" text-anchor="middle" fill="#fff" font-size="8">Cu '+p.input.toFixed(0)+'g</text><path d="M'+(calX+35)+' '+(calY-25)+'V'+(calY+calH-30)+'H'+(calX+20)+'A8 8 0 0 1 '+(calX+35)+' '+(calY+calH-22)+'" fill="none" stroke="'+ink+'" stroke-width="2"/><rect x="'+(calX-5)+'" y="45" width="10" height="175" rx="4" fill="#1e293b" stroke="'+soft+'" stroke-width="1"/><line x1="'+calX+'" y1="'+(220-tMerc)+'" x2="'+calX+'" y2="215" stroke="#ef4444" stroke-width="3"/><circle cx="'+calX+'" cy="217" r="5" fill="#ef4444"/><text x="'+calX+'" y="38" text-anchor="middle" fill="'+orange+'" font-size="10" font-weight="bold">'+v.raw.toFixed(2)+'°C</text><text x="'+calX+'" y="'+(calY+calH+12)+'" text-anchor="middle" fill="'+soft+'" font-size="9">WATER EQUIVALENT CALORIMETER</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">EQUILIBRIUM TEMPERATURE (T_f)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.raw.toFixed(2)+'</text><text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">°C</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">COPPER SPECIMEN MASS (m_s)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+p.input.toFixed(1)+' g</text><text x="'+(bX+120)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="9">T_s = 100.0 °C</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">HEAT ABSORBED (Q_sys)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">'+qAbs.toFixed(1)+' J</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">C_sys = 920.92 J/K, T₀ = 20.0 °C</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'c_s = Q / [m_s (T_s − T_f)] ⇔ c_s = S',ink,9)+text(240,22,'Jacketed Calorimeter & Method of Mixtures Apparatus')+text(240,308,'Thermal Conservation: m_s c_s (T_s − T_f) = C_sys (T_f − T₀)');}
    else if(cfg.slug==='newtons-cooling'){const cx=240,cy=170,R_outer=90,R_inner=55,tMerc=Math.min(100,Math.max(10,(v.raw-20)*2.2)),theta=v.raw-20.0;svg+='<rect x="40" y="280" width="410" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="'+(cx-R_outer)+'" y="95" width="'+(2*R_outer)+'" height="180" rx="8" fill="#182824" stroke="'+soft+'" stroke-width="2.5"/><rect x="'+(cx-R_outer+8)+'" y="105" width="'+(2*R_outer-16)+'" height="162" rx="4" fill="#0284c7" opacity="0.35"/><rect x="'+(cx-R_inner)+'" y="115" width="'+(2*R_inner)+'" height="145" rx="5" fill="#20312d" stroke="#d97706" stroke-width="2"/><rect x="'+(cx-R_inner+5)+'" y="130" width="'+(2*R_inner-10)+'" height="125" rx="3" fill="#ea580c" opacity="0.5"/><rect x="'+(cx-R_outer-5)+'" y="90" width="'+(2*R_outer+10)+'" height="12" rx="2" fill="#78350f" stroke="#b45309" stroke-width="1.5"/><rect x="'+(cx-5)+'" y="38" width="10" height="185" rx="4" fill="#1e293b" stroke="'+soft+'" stroke-width="1"/><line x1="'+cx+'" y1="'+(220-tMerc)+'" x2="'+cx+'" y2="218" stroke="#ef4444" stroke-width="3"/><circle cx="'+cx+'" cy="220" r="5" fill="#ef4444"/><text x="'+cx+'" y="30" text-anchor="middle" fill="'+orange+'" font-size="11" font-weight="bold">'+v.raw.toFixed(2)+'°C</text><path d="M'+(cx+32)+' 70 V 225 H '+(cx+15)+' A 8 8 0 0 1 '+(cx+32)+' 233" fill="none" stroke="'+ink+'" stroke-width="2"/><text x="'+(cx-R_outer+15)+'" y="260" fill="#38bdf8" font-size="8">JACKET T₀ = 20.0°C</text><text x="'+cx+'" y="295" text-anchor="middle" fill="'+soft+'" font-size="9">WATER-JACKETED COOLING CALORIMETER</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">WATER TEMPERATURE (T)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.raw.toFixed(2)+'</text><text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">°C</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">ELAPSED TIME (t)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+p.input.toFixed(1)+' min</text><text x="'+(bX+125)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="9">('+(p.input*60).toFixed(0)+' s)</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">TEMPERATURE EXCESS (θ)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">'+theta.toFixed(2)+' °C</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">ln(θ₀/θ) = '+v.y.toFixed(4)+'</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'ln[(T_i − T_0)/(T − T_0)] = k · t ⇔ k = S',ink,9)+text(240,22,'Newton\'s Law of Cooling Apparatus')+text(240,308,'Exponential Thermal Decay: dT/dt = −k (T − T₀)');}
    else if(cfg.slug==='solidification-cooling'){const qLatent=v.raw*270.0;svg+='<rect x="40" y="280" width="410" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="70" y="274" width="70" height="8" rx="2" fill="#20312d" stroke="'+soft+'" stroke-width="1"/><line x1="105" y1="274" x2="105" y2="45" stroke="#1b2a26" stroke-width="8"/><line x1="102" y1="274" x2="102" y2="45" stroke="'+soft+'" stroke-width="2"/><rect x="96" y="98" width="18" height="14" rx="2" fill="#364e46" stroke="'+soft+'" stroke-width="1"/><line x1="110" y1="105" x2="190" y2="105" stroke="'+soft+'" stroke-width="4"/><path d="M185 96 C195 96, 205 104, 205 116" fill="none" stroke="'+soft+'" stroke-width="3"/><path d="M185 114 C195 114, 205 106, 205 94" fill="none" stroke="'+soft+'" stroke-width="3"/><path d="M165 115 V255 C165 265, 275 265, 275 255 V115" fill="#182824" stroke="'+soft+'" stroke-width="2" opacity="0.8"/><ellipse cx="220" cy="115" rx="55" ry="9" fill="#20312d" stroke="'+soft+'" stroke-width="1.5"/><rect x="202" y="85" width="36" height="6" rx="2" fill="#253a34" stroke="'+soft+'" stroke-width="1"/><path d="M204 90 V225 A16 16 0 0 0 236 225 V90" fill="#13201d" stroke="'+soft+'" stroke-width="2"/>';const salolH=Math.min(95,Math.max(30,p.input*2.5)),salolY=241-salolH,solidH=salolH*0.6,solidY=241-solidH;svg+='<path d="M206 '+salolY+' V225 A14 14 0 0 0 234 225 V'+salolY+' Z" fill="#e2e8f0" opacity="0.35"/><path d="M206 '+solidY+' V225 A14 14 0 0 0 234 225 V'+solidY+' Z" fill="#cbd5e1" opacity="0.65"/><line x1="210" y1="230" x2="218" y2="215" stroke="'+orange+'" stroke-width="1"/><line x1="220" y1="233" x2="228" y2="212" stroke="'+orange+'" stroke-width="1"/><line x1="214" y1="218" x2="226" y2="204" stroke="'+orange+'" stroke-width="1"/><rect x="217" y="38" width="6" height="175" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1"/><line x1="220" y1="130" x2="220" y2="208" stroke="#ef4444" stroke-width="2.5"/><circle cx="220" cy="209" r="4" fill="#ef4444"/><text x="220" y="30" text-anchor="middle" fill="'+orange+'" font-size="11" font-weight="bold">41.50 °C (T_m)</text><path d="M232 48 V195 A5 5 0 0 1 222 195" fill="none" stroke="'+ink+'" stroke-width="1.5"/><text x="220" y="272" text-anchor="middle" fill="#38bdf8" font-size="8">AIR JACKET ENCLOSURE</text><text x="220" y="295" text-anchor="middle" fill="'+soft+'" font-size="9">SALOL SOLIDIFICATION TUBE</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">SOLIDIFICATION DURATION (Δt)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.raw.toFixed(2)+'</text><text x="'+(bX+110)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">min</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">SALOL SAMPLE MASS (m)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+p.input.toFixed(1)+' g</text><text x="'+(bX+120)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="9">('+(p.input/1000).toFixed(4)+' kg)</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">HEAT LIBERATED (Q_latent)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">'+qLatent.toFixed(1)+' J</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">R_loss = 270.0 J/min (4.50 W)</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'Q_latent = m · L_f ⇔ L_f = S',ink,9)+text(240,22,'Solidification Cooling Curve Apparatus')+text(240,308,'Phase Transition Arrest: Q_latent = R_loss · Δt');}
    else if(cfg.slug==='latent-heat-vaporization'){const calX=290,calY=165,calW=120,calH=115,tMerc=Math.min(100,Math.max(10,(v.raw-15)*3.0)),qNet=v.y;svg+='<rect x="30" y="280" width="420" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><line x1="60" y1="280" x2="75" y2="200" stroke="#1b2a26" stroke-width="4"/><line x1="120" y1="280" x2="105" y2="200" stroke="#1b2a26" stroke-width="4"/><line x1="65" y1="200" x2="115" y2="200" stroke="'+soft+'" stroke-width="3"/><rect x="85" y="235" width="10" height="45" fill="#364e46" stroke="'+soft+'" stroke-width="1"/><polygon points="90,215 84,235 96,235" fill="'+orange+'"/><polygon points="90,222 87,235 93,235" fill="#38bdf8"/><rect x="65" y="125" width="50" height="75" rx="6" fill="#b45309" stroke="#d97706" stroke-width="2"/><text x="90" y="165" text-anchor="middle" fill="#fff" font-size="8">BOILER</text><text x="90" y="177" text-anchor="middle" fill="#fde68a" font-size="7">100°C</text><path d="M90 125 V80 H155" fill="none" stroke="'+ink+'" stroke-width="3"/><rect x="155" y="70" width="28" height="40" rx="10" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><path d="M155 80 H183 M175 80 V105" fill="none" stroke="'+ink+'" stroke-width="2"/><ellipse cx="169" cy="104" rx="10" ry="4" fill="#0284c7" opacity="0.6"/><text x="169" y="65" text-anchor="middle" fill="#38bdf8" font-size="7">WATER TRAP</text><path d="M183 80 H235 V190" fill="none" stroke="'+ink+'" stroke-width="3"/><rect x="'+(calX-calW/2)+'" y="'+(calY-5)+'" width="'+calW+'" height="'+calH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="2"/><rect x="'+(calX-calW/2+12)+'" y="'+calY+'" width="'+(calW-24)+'" height="'+(calH-14)+'" rx="4" fill="#b45309" stroke="#d97706" stroke-width="1.5"/><rect x="'+(calX-calW/2+14)+'" y="'+(calY+20)+'" width="'+(calW-28)+'" height="'+(calH-36)+'" rx="2" fill="#0284c7" opacity="0.6"/><circle cx="235" cy="205" r="3" fill="#fff" opacity="0.8"/><circle cx="238" cy="195" r="2" fill="#fff" opacity="0.6"/><circle cx="233" cy="185" r="2.5" fill="#fff" opacity="0.7"/><rect x="'+(calX+15)+'" y="45" width="8" height="175" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1"/><line x1="'+(calX+19)+'" y1="'+(220-tMerc)+'" x2="'+(calX+19)+'" y2="218" stroke="#ef4444" stroke-width="2.5"/><circle cx="'+(calX+19)+'" cy="220" r="4" fill="#ef4444"/><text x="'+(calX+19)+'" y="38" text-anchor="middle" fill="'+orange+'" font-size="10" font-weight="bold">'+v.raw.toFixed(2)+'°C</text><path d="M'+(calX-15)+' 55 V215 H'+(calX-5)+'" fill="none" stroke="'+ink+'" stroke-width="1.5"/><text x="'+calX+'" y="'+(calY+calH+12)+'" text-anchor="middle" fill="'+soft+'" font-size="9">JACKETED CONDENSATION CALORIMETER</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">CONDENSED STEAM MASS (m_v)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+p.input.toFixed(1)+'</text><text x="'+(bX+85)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">g</text><text x="'+(bX+110)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="9">('+(p.input/1000).toFixed(4)+' kg)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">FINAL TEMPERATURE (T_f)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+v.raw.toFixed(2)+' °C</text><text x="'+(bX+130)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="9">T₀ = 15.00 °C</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">NET LATENT HEAT (Q_net)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">'+qNet.toFixed(1)+' J</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">C_sys = 866.08 J/K, T_s = 100.0 °C</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'Q_net = m_v · L_v ⇔ L_v = S',ink,9)+text(240,22,'Steam Condensation Calorimetry Apparatus')+text(240,308,'Thermal Energy Balance: m_v L_v + m_v c_w (T_s − T_f) = C_sys (T_f − T₀)');}
    else if(cfg.slug==='latent-heat-fusion'){const calX=270,calY=165,calW=130,calH=115,tMerc=Math.min(100,Math.max(10,(v.raw-10)*3.5)),qNet=v.y;svg+='<rect x="30" y="280" width="420" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><ellipse cx="95" cy="235" rx="45" ry="12" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><ellipse cx="95" cy="232" rx="42" ry="9" fill="#20312d"/><rect x="75" y="215" width="14" height="14" rx="2" fill="#e0f2fe" stroke="#38bdf8" stroke-width="1" opacity="0.85"/><rect x="92" y="212" width="16" height="16" rx="2" fill="#bae6fd" stroke="#0284c7" stroke-width="1" opacity="0.85"/><rect x="85" y="202" width="12" height="12" rx="2" fill="#f0f9ff" stroke="#38bdf8" stroke-width="1" opacity="0.9"/><text x="95" y="260" text-anchor="middle" fill="#38bdf8" font-size="8">DRY ICE CHIPS (0°C)</text><path d="M120 205 Q170 150 220 185" fill="none" stroke="'+orange+'" stroke-width="1.5" stroke-dasharray="4 3"/><polygon points="222,189 216,181 224,180" fill="'+orange+'"/><rect x="'+(calX-calW/2)+'" y="'+(calY-5)+'" width="'+calW+'" height="'+calH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="2"/><rect x="'+(calX-calW/2+15)+'" y="'+(calY+calH-7)+'" width="10" height="8" fill="#78350f"/><rect x="'+(calX+calW/2-25)+'" y="'+(calY+calH-7)+'" width="10" height="8" fill="#78350f"/><rect x="'+(calX-calW/2+12)+'" y="'+calY+'" width="'+(calW-24)+'" height="'+(calH-14)+'" rx="4" fill="#b45309" stroke="#d97706" stroke-width="1.5"/><rect x="'+(calX-calW/2+14)+'" y="'+(calY+20)+'" width="'+(calW-28)+'" height="'+(calH-36)+'" rx="2" fill="#0284c7" opacity="0.55"/><rect x="'+(calX-30)+'" y="'+(calY+22)+'" width="12" height="10" rx="2" fill="#e0f2fe" stroke="#38bdf8" opacity="0.8"/><rect x="'+(calX-12)+'" y="'+(calY+24)+'" width="14" height="11" rx="2" fill="#bae6fd" stroke="#0284c7" opacity="0.85"/><rect x="'+(calX+8)+'" y="'+(calY+21)+'" width="10" height="9" rx="2" fill="#f0f9ff" stroke="#38bdf8" opacity="0.9"/><rect x="'+(calX+35)+'" y="45" width="8" height="175" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1"/><line x1="'+(calX+39)+'" y1="'+(220-tMerc)+'" x2="'+(calX+39)+'" y2="218" stroke="#ef4444" stroke-width="2.5"/><circle cx="'+(calX+39)+'" cy="220" r="4" fill="#ef4444"/><text x="'+(calX+39)+'" y="38" text-anchor="middle" fill="'+orange+'" font-size="10" font-weight="bold">'+v.raw.toFixed(2)+'°C</text><path d="M'+(calX-38)+' 55 V215 H'+(calX-20)+'" fill="none" stroke="'+ink+'" stroke-width="1.5"/><text x="'+calX+'" y="'+(calY+calH+14)+'" text-anchor="middle" fill="'+soft+'" font-size="9">JACKETED COPPER CALORIMETER</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">ICE SAMPLE MASS (m_i)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+p.input.toFixed(1)+'</text><text x="'+(bX+85)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">g</text><text x="'+(bX+110)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="9">('+(p.input/1000).toFixed(4)+' kg)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">FINAL EQUILIBRIUM TEMP (T_f)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+v.raw.toFixed(2)+' °C</text><text x="'+(bX+130)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="9">T₀ = 30.00 °C</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">NET LATENT HEAT (Q_net)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">'+qNet.toFixed(1)+' J</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">C_sys = 866.08 J/K, T_ice = 0.0 °C</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'Q_net = m_i · L_f ⇔ L_f = S',ink,9)+text(240,22,'Ice Melting Calorimetry Apparatus')+text(240,308,'Thermal Conservation: m_i L_f + m_i c_w T_f = C_sys (T_0 − T_f)');}
    else if(cfg.slug==='thermal-expansion'){const jX=60,jY=145,jW=360,jH=45,tMerc=Math.min(95,Math.max(15,(p.input/80)*90));svg+='<rect x="30" y="280" width="420" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="45" y="110" width="25" height="170" rx="3" fill="#20312d" stroke="'+soft+'" stroke-width="2"/><rect x="68" y="157" width="12" height="20" fill="#78350f" stroke="#b45309" stroke-width="1"/><rect x="405" y="110" width="25" height="170" rx="3" fill="#20312d" stroke="'+soft+'" stroke-width="2"/><rect x="150" y="190" width="14" height="90" fill="#182824" stroke="'+soft+'" stroke-width="1"/><rect x="315" y="190" width="14" height="90" fill="#182824" stroke="'+soft+'" stroke-width="1"/><rect x="'+jX+'" y="'+jY+'" width="'+jW+'" height="'+jH+'" rx="8" fill="#1e293b" stroke="'+soft+'" stroke-width="2" opacity="0.85"/><rect x="'+(jX+8)+'" y="'+(jY+6)+'" width="'+(jW-16)+'" height="'+(jH-12)+'" rx="4" fill="#334155" opacity="0.4"/><rect x="70" y="162" width="345" height="11" rx="2" fill="#b45309" stroke="#d97706" stroke-width="1.5"/><text x="240" y="171" text-anchor="middle" fill="#fde68a" font-size="8" font-weight="bold">COPPER SPECIMEN ROD (L₀ = 1.000 m)</text><rect x="115" y="115" width="16" height="30" fill="#475569" stroke="'+soft+'" stroke-width="1"/><path d="M123 115 V85 H85" fill="none" stroke="'+ink+'" stroke-width="3"/><text x="85" y="78" text-anchor="middle" fill="#38bdf8" font-size="8">STEAM INLET</text><rect x="350" y="190" width="16" height="25" fill="#475569" stroke="'+soft+'" stroke-width="1"/><path d="M358 215 V240" fill="none" stroke="'+ink+'" stroke-width="2"/><rect x="345" y="240" width="26" height="35" rx="3" fill="#182824" stroke="'+soft+'" stroke-width="1"/><text x="358" y="260" text-anchor="middle" fill="#38bdf8" font-size="7">DRAIN</text><rect x="232" y="115" width="16" height="30" fill="#475569" stroke="'+soft+'" stroke-width="1"/><rect x="236" y="45" width="8" height="115" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1"/><line x1="240" y1="'+(150-tMerc)+'" x2="240" y2="152" stroke="#ef4444" stroke-width="2.5"/><circle cx="240" cy="154" r="4" fill="#ef4444"/><text x="240" y="38" text-anchor="middle" fill="'+orange+'" font-size="10" font-weight="bold">'+(20.0+p.input).toFixed(1)+'°C</text><rect x="415" y="157" width="22" height="20" rx="2" fill="#475569" stroke="'+ink+'" stroke-width="1.5"/><rect x="400" y="163" width="15" height="8" rx="1" fill="#94a3b8" stroke="'+soft+'" stroke-width="1"/><rect x="437" y="153" width="16" height="28" rx="2" fill="#334155" stroke="'+soft+'" stroke-width="1.5"/><path d="M57 110 V70 H200 V95" fill="none" stroke="'+orange+'" stroke-width="1.5" stroke-dasharray="3 2"/><path d="M426 157 V70 H260 V95" fill="none" stroke="'+orange+'" stroke-width="1.5" stroke-dasharray="3 2"/><circle cx="230" cy="95" r="9" fill="#182824" stroke="'+orange+'" stroke-width="1.5"/><line x1="224" y1="89" x2="236" y2="101" stroke="'+orange+'" stroke-width="1.5"/><line x1="224" y1="101" x2="236" y2="89" stroke="'+orange+'" stroke-width="1.5"/><text x="230" y="78" text-anchor="middle" fill="'+orange+'" font-size="8">CONTACT SENSOR</text><text x="240" y="305" text-anchor="middle" fill="'+soft+'" font-size="9">STEAM DILATOMETER · MICROMETER SENSING CIRCUIT</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">TEMPERATURE ELEVATION (ΔT)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+p.input.toFixed(1)+'</text><text x="'+(bX+85)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">°C (K)</text><text x="'+(bX+130)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="9">(T = '+(20.0+p.input).toFixed(1)+'°C)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">MEASURED ELONGATION (ΔL)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+v.raw.toFixed(3)+' mm</text><text x="'+(bX+125)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="9">('+(v.raw/1000).toFixed(6)+' m)</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">EXPANSION COEFFICIENT (α)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">16.80 × 10⁻⁶ K⁻¹</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">L₀ = 1.000 m, Initial T₀ = 20.0 °C</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'ΔL = L₀ · α · ΔT ⇔ α = S',ink,9)+text(240,22,'Linear Thermal Dilatometer Apparatus')+text(240,308,'Linear Dilatation: ΔL = L₀ · α · (T − T₀)');}
    else if(cfg.slug==='mechanical-equivalent-heat'){const cx=220,cy=160,R=45,tMerc=Math.min(95,Math.max(12,(v.raw-20.0)*4.5)),rotAngle=t*0.005;svg+='<rect x="30" y="280" width="420" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="208" y="150" width="24" height="130" fill="#20312d" stroke="'+soft+'" stroke-width="2"/><rect x="185" y="270" width="70" height="10" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="75" y="135" width="55" height="50" rx="4" fill="#334155" stroke="'+soft+'" stroke-width="1.5"/><rect x="65" y="145" width="10" height="30" rx="2" fill="#1e293b" stroke="'+soft+'"/><text x="102" y="164" text-anchor="middle" fill="#94a3b8" font-size="8">MOTOR</text><line x1="130" y1="160" x2="175" y2="160" stroke="'+ink+'" stroke-width="6"/><rect x="135" y="185" width="50" height="24" rx="3" fill="#182824" stroke="'+orange+'" stroke-width="1.5"/><text x="160" y="201" text-anchor="middle" fill="'+orange+'" font-size="11" font-family="monospace" font-weight="bold">'+p.input.toFixed(0)+'</text><text x="160" y="222" text-anchor="middle" fill="#38bdf8" font-size="7">REVS (N)</text><circle cx="'+cx+'" cy="'+cy+'" r="'+R+'" fill="#b45309" stroke="#d97706" stroke-width="2"/><circle cx="'+cx+'" cy="'+cy+'" r="'+(R-8)+'" fill="#0284c7" opacity="0.6"/>';for(let a=0;a<360;a+=60){const rad=(a*Math.PI/180)+rotAngle;svg+='<line x1="'+(cx+12*Math.cos(rad))+'" y1="'+(cy+12*Math.sin(rad))+'" x2="'+(cx+(R-10)*Math.cos(rad))+'" y2="'+(cy+(R-10)*Math.sin(rad))+'" stroke="#fde68a" stroke-width="1.5" opacity="0.7"/>';}svg+='<circle cx="'+cx+'" cy="'+cy+'" r="10" fill="#1e293b" stroke="'+soft+'" stroke-width="1.5"/><line x1="175" y1="50" x2="175" y2="160" stroke="'+ink+'" stroke-width="2"/><rect x="168" y="70" width="14" height="35" rx="2" fill="#182824" stroke="'+soft+'" stroke-width="1"/><line x1="175" y1="78" x2="175" y2="98" stroke="'+orange+'" stroke-width="1.5"/><text x="175" y="65" text-anchor="middle" fill="#38bdf8" font-size="7">SPRING T₂</text><path d="M175 160 A45 45 0 0 1 265 160" fill="none" stroke="'+ink+'" stroke-width="3"/><line x1="265" y1="160" x2="265" y2="245" stroke="'+ink+'" stroke-width="2.5"/><rect x="250" y="245" width="30" height="26" rx="3" fill="'+orange+'" stroke="#f0b691" stroke-width="1.5"/><text x="265" y="261" text-anchor="middle" fill="#182824" font-size="9" font-weight="bold">3.0 kg</text><text x="265" y="280" text-anchor="middle" fill="'+orange+'" font-size="8">T₁ = Mg</text><rect x="'+(cx-4)+'" y="35" width="8" height="120" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1"/><line x1="'+cx+'" y1="'+(150-tMerc)+'" x2="'+cx+'" y2="152" stroke="#ef4444" stroke-width="2.5"/><circle cx="'+cx+'" cy="154" r="4" fill="#ef4444"/><text x="'+cx+'" y="28" text-anchor="middle" fill="'+orange+'" font-size="10" font-weight="bold">'+v.raw.toFixed(2)+'°C</text><text x="220" y="305" text-anchor="middle" fill="'+soft+'" font-size="9">FRICTION CALORIMETER · ROTATING DRUM & SUSPENDED LOAD</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">MECHANICAL WORK DONE (W)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.y.toFixed(1)+'</text><text x="'+(bX+110)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">J</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">REVOLUTIONS & EQUILIBRIUM TEMP</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+p.input.toFixed(0)+' rev</text><text x="'+(bX+120)+'" y="'+(bY+108)+'" fill="'+orange+'" font-size="14" font-family="monospace">'+v.raw.toFixed(2)+' °C</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">HEAT ABSORBED (Q)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">'+v.x.toFixed(1)+' cal</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">C_sys = 118.48 cal/K, M_load = 3.00 kg</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'W = J · Q ⇔ J = S = 4.186 J cal⁻¹',ink,9)+text(240,22,'Mechanical Equivalent of Heat Apparatus')+text(240,308,'Joule Equivalence: W = 2π r M g N = J · C_sys (T_f − T₀)');}
    else if(cfg.slug==='boyles-law'){const bBoardX=130,bBoardY=45,bBoardW=180,bBoardH=235,scX=220,clX=165,opX=275,yTop=60,yBot=265,yClosed=yTop+(p.input/50.0)*180,dh_mmHg=(v.raw-101.325)*7.5006,dh_px=(dh_mmHg/400.0)*80,yOpen=Math.max(yTop+5,Math.min(yBot-5,yClosed-dh_px)),k_J=(v.raw*p.input*0.001);svg+='<rect x="30" y="280" width="420" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="'+bBoardX+'" y="'+bBoardY+'" width="'+bBoardW+'" height="'+bBoardH+'" rx="4" fill="#182824" stroke="'+soft+'" stroke-width="2"/><line x1="'+scX+'" y1="'+yTop+'" x2="'+scX+'" y2="'+yBot+'" stroke="'+soft+'" stroke-width="1.5"/>';for(let k=0;k<=20;k++){const my=yTop+k*((yBot-yTop)/20);svg+='<line x1="'+(scX-4)+'" y1="'+my+'" x2="'+(scX+4)+'" y2="'+my+'" stroke="'+soft+'" stroke-width="'+(k%5===0?1.5:0.8)+'"/>';if(k%5===0){svg+='<text x="'+(scX+6)+'" y="'+(my+3)+'" fill="#9fb498" font-size="6.5">'+(100-k*5)+'</text>';}}svg+='<rect x="'+(clX-7)+'" y="'+yTop+'" width="14" height="'+(yBot-yTop)+'" rx="4" fill="none" stroke="'+soft+'" stroke-width="1.5"/><rect x="'+(clX-5)+'" y="'+(yTop+2)+'" width="10" height="'+(yClosed-yTop-2)+'" rx="2" fill="#38bdf8" opacity="0.25"/><rect x="'+(clX-5)+'" y="'+yClosed+'" width="10" height="'+(yBot-yClosed)+'" fill="#94a3b8" stroke="#64748b" stroke-width="0.5"/><ellipse cx="'+clX+'" cy="'+yClosed+'" rx="5" ry="2" fill="#cbd5e1"/><line x1="'+clX+'" y1="'+yClosed+'" x2="'+scX+'" y2="'+yClosed+'" stroke="'+orange+'" stroke-width="1.5" stroke-dasharray="3 2"/><text x="'+(clX-12)+'" y="'+((yTop+yClosed)/2+3)+'" text-anchor="end" fill="#38bdf8" font-size="8">V='+p.input.toFixed(1)+' cm³</text><rect x="'+(opX-7)+'" y="'+yTop+'" width="14" height="'+(yBot-yTop)+'" fill="none" stroke="'+soft+'" stroke-width="1.5"/><rect x="'+(opX-5)+'" y="'+yOpen+'" width="10" height="'+(yBot-yOpen)+'" fill="#94a3b8" stroke="#64748b" stroke-width="0.5"/><ellipse cx="'+opX+'" cy="'+yOpen+'" rx="5" ry="2" fill="#cbd5e1"/><line x1="'+opX+'" y1="'+yOpen+'" x2="'+scX+'" y2="'+yOpen+'" stroke="'+orange+'" stroke-width="1.5" stroke-dasharray="3 2"/><rect x="'+(opX-12)+'" y="'+(yOpen-8)+'" width="24" height="16" rx="2" fill="#334155" stroke="'+orange+'" stroke-width="1" opacity="0.7"/><circle cx="'+(opX+15)+'" cy="'+yOpen+'" r="4" fill="'+soft+'"/><path d="M'+(clX-5)+' '+yBot+' C '+(clX-5)+' '+(yBot+20)+', '+(opX+5)+' '+(yBot+20)+', '+(opX+5)+' '+yBot+'" fill="none" stroke="#94a3b8" stroke-width="10"/><path d="M'+(clX-5)+' '+yBot+' C '+(clX-5)+' '+(yBot+20)+', '+(opX+5)+' '+(yBot+20)+', '+(opX+5)+' '+yBot+'" fill="none" stroke="#334155" stroke-width="14" stroke-dasharray="1 0" opacity="0.4"/><rect x="45" y="60" width="75" height="45" rx="4" fill="#182824" stroke="'+soft+'" stroke-width="1"/><text x="82" y="75" text-anchor="middle" fill="#718e79" font-size="7.5">BAROMETER (B)</text><text x="82" y="92" text-anchor="middle" fill="'+ink+'" font-size="10" font-family="monospace" font-weight="bold">760.0 mmHg</text><text x="82" y="101" text-anchor="middle" fill="#9fb498" font-size="6.5">101.33 kPa</text><text x="220" y="305" text-anchor="middle" fill="'+soft+'" font-size="9">BOYLE\'S J-TUBE MANOMETER · MERCURY COLUMN</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">ABSOLUTE PRESSURE (P)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.raw.toFixed(2)+'</text><text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">kPa</text><text x="'+(bX+135)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">('+(v.raw*7.5006).toFixed(1)+' mmHg)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">CONFINED AIR VOLUME (V)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+p.input.toFixed(1)+' cm³</text><text x="'+(bX+125)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8">('+(p.input/1000).toFixed(4)+' L)</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">RECIPROCAL VOLUME (1/V)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">'+(v.x/1000).toFixed(2)+' L⁻¹</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">P · V = '+k_J.toFixed(3)+' J, Δh = '+dh_mmHg.toFixed(1)+' mmHg</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'P = k · (1/V) ⇔ k = S = 3.040 J',ink,9)+text(240,22,'Precision Boyle\'s Law J-Tube Manometer Apparatus')+text(240,308,'Isothermal Ideal Gas Law: P · V = n R T = constant (T = 20.0 °C)');}
    else if(cfg.slug==='charles-law-volume'){const y_men=115+((v.raw-100.0)/30.0)*110,tMerc=Math.min(100,Math.max(10,(p.input/80.0)*95)),dV=(v.raw-100.0),beta_cur=(p.input>0?(dV/(100.0*p.input)):(1.0/273.15));svg+='<rect x="30" y="280" width="420" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="80" y="115" width="110" height="150" rx="8" fill="#182824" stroke="'+soft+'" stroke-width="2"/><rect x="86" y="130" width="98" height="130" rx="4" fill="#0284c7" opacity="0.45"/><line x1="90" y1="265" x2="180" y2="265" stroke="#364e46" stroke-width="3"/><polygon points="130,278 135,265 140,278" fill="'+orange+'"/><path d="M100 85 V250 A8 8 0 0 1 116 250" fill="none" stroke="'+ink+'" stroke-width="1.5"/><rect x="160" y="55" width="8" height="175" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1"/><line x1="164" y1="'+(220-tMerc)+'" x2="164" y2="220" stroke="#ef4444" stroke-width="2.5"/><circle cx="164" cy="222" r="4" fill="#ef4444"/><text x="164" y="48" text-anchor="middle" fill="'+orange+'" font-size="10" font-weight="bold">'+p.input.toFixed(1)+'°C</text><ellipse cx="135" cy="195" rx="28" ry="36" fill="#38bdf8" opacity="0.2" stroke="'+soft+'" stroke-width="1.5"/><text x="135" y="198" text-anchor="middle" fill="#fff" font-size="8">AIR BULB (V₀)</text><path d="M135 159 V80 H245 V95" fill="none" stroke="'+soft+'" stroke-width="2.5"/><rect x="238" y="95" width="14" height="170" rx="3" fill="none" stroke="'+soft+'" stroke-width="1.5"/>';for(let k=0;k<=15;k++){const my=95+k*(170/15);svg+='<line x1="235" y1="'+my+'" x2="238" y2="'+my+'" stroke="'+soft+'" stroke-width="'+(k%5===0?1.5:0.8)+'"/>';}svg+='<rect x="240" y="97" width="10" height="'+Math.max(2,y_men-97)+'" fill="#38bdf8" opacity="0.25"/><rect x="240" y="'+y_men+'" width="10" height="'+Math.max(2,265-y_men)+'" fill="#94a3b8" stroke="#64748b" stroke-width="0.5"/><ellipse cx="245" cy="'+y_men+'" rx="5" ry="2" fill="#cbd5e1"/><text x="225" y="'+(y_men+3)+'" text-anchor="end" fill="#38bdf8" font-size="7.5">V='+v.raw.toFixed(2)+'</text><rect x="313" y="'+(y_men-15)+'" width="14" height="60" rx="3" fill="none" stroke="'+soft+'" stroke-width="1.5"/><rect x="315" y="'+y_men+'" width="10" height="45" fill="#94a3b8" stroke="#64748b" stroke-width="0.5"/><ellipse cx="320" cy="'+y_men+'" rx="5" ry="2" fill="#cbd5e1"/><line x1="245" y1="'+y_men+'" x2="320" y2="'+y_men+'" stroke="'+orange+'" stroke-width="1.5" stroke-dasharray="3 2"/><text x="282" y="'+(y_men-6)+'" text-anchor="middle" fill="'+orange+'" font-size="7.5">P = B (Isobaric Line)</text><path d="M245 265 C 245 285, 320 285, 320 '+(y_men+45)+'" fill="none" stroke="#94a3b8" stroke-width="8"/><path d="M245 265 C 245 285, 320 285, 320 '+(y_men+45)+'" fill="none" stroke="#334155" stroke-width="12" opacity="0.3"/><text x="220" y="305" text-anchor="middle" fill="'+soft+'" font-size="9">CONSTANT-PRESSURE AIR DILATOMETER · LEVELING RESERVOIR</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">CONFINED AIR VOLUME (V)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.raw.toFixed(2)+'</text><text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">cm³</text><text x="'+(bX+140)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">('+(v.raw/1000).toFixed(4)+' L)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">BATH TEMPERATURE (t)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+p.input.toFixed(1)+' °C</text><text x="'+(bX+115)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8">('+(p.input+273.15).toFixed(2)+' K)</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">THERMAL EXPANSION (ΔV)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">+'+dV.toFixed(2)+' cm³</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">β = '+beta_cur.toFixed(5)+' K⁻¹, P = 101.3 kPa</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'V_t = V_0(1 + β t) ⇔ β = S / V_0',ink,9)+text(240,22,'Constant-Pressure Air Thermometer Apparatus')+text(240,308,'Charles\' Law: V ∝ T (P = 101.33 kPa = constant)');}
    else if(cfg.slug==='charles-law-pressure'){const y_fixed=180,dh_mmHg=(v.raw-101.325)*7.5006,dh_px=(p.input/80.0)*85,y_open=y_fixed-dh_px,tMerc=Math.min(100,Math.max(10,(p.input/80.0)*95)),alpha_cur=(p.input>0?((v.raw*1000.0-101325.0)/(101325.0*p.input)):(1.0/273.15));svg+='<rect x="30" y="280" width="420" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="70" y="115" width="115" height="150" rx="8" fill="#182824" stroke="'+soft+'" stroke-width="2"/><rect x="76" y="130" width="103" height="130" rx="4" fill="#0284c7" opacity="0.45"/><line x1="80" y1="265" x2="175" y2="265" stroke="#364e46" stroke-width="3"/><polygon points="120,278 125,265 130,278" fill="'+orange+'"/><path d="M90 85 V250 A8 8 0 0 1 106 250" fill="none" stroke="'+ink+'" stroke-width="1.5"/><rect x="155" y="55" width="8" height="175" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1"/><line x1="159" y1="'+(220-tMerc)+'" x2="159" y2="220" stroke="#ef4444" stroke-width="2.5"/><circle cx="159" cy="222" r="4" fill="#ef4444"/><text x="159" y="48" text-anchor="middle" fill="'+orange+'" font-size="10" font-weight="bold">'+p.input.toFixed(1)+'°C</text><ellipse cx="120" cy="195" rx="28" ry="36" fill="#38bdf8" opacity="0.2" stroke="'+soft+'" stroke-width="1.5"/><text x="120" y="198" text-anchor="middle" fill="#fff" font-size="8">JOLLY BULB (V₀)</text><path d="M120 159 V80 H235 V110" fill="none" stroke="'+soft+'" stroke-width="2.5"/><rect x="228" y="105" width="14" height="160" rx="3" fill="none" stroke="'+soft+'" stroke-width="1.5"/><polygon points="235,180 231,168 239,168" fill="'+orange+'"/><line x1="210" y1="180" x2="255" y2="180" stroke="'+orange+'" stroke-width="1" stroke-dasharray="2 2"/><text x="206" y="183" text-anchor="end" fill="'+orange+'" font-size="7.5">INDEX TIP</text><rect x="230" y="180" width="10" height="85" fill="#94a3b8" stroke="#64748b" stroke-width="0.5"/><ellipse cx="235" cy="180" rx="5" ry="2" fill="#cbd5e1"/><line x1="275" y1="70" x2="275" y2="265" stroke="'+soft+'" stroke-width="1.5"/>';for(let k=0;k<=19;k++){const my=70+k*(195/19);svg+='<line x1="272" y1="'+my+'" x2="278" y2="'+my+'" stroke="'+soft+'" stroke-width="'+(k%5===0?1.5:0.8)+'"/>';}svg+='<rect x="308" y="60" width="14" height="205" rx="3" fill="none" stroke="'+soft+'" stroke-width="1.5"/><rect x="310" y="'+y_open+'" width="10" height="'+(265-y_open)+'" fill="#94a3b8" stroke="#64748b" stroke-width="0.5"/><ellipse cx="315" cy="'+y_open+'" rx="5" ry="2" fill="#cbd5e1"/><line x1="255" y1="180" x2="315" y2="180" stroke="#64748b" stroke-width="1" stroke-dasharray="2 2"/><line x1="324" y1="'+y_open+'" x2="350" y2="'+y_open+'" stroke="'+orange+'" stroke-width="1.5"/><line x1="324" y1="180" x2="350" y2="180" stroke="'+orange+'" stroke-width="1.5"/><line x1="345" y1="180" x2="345" y2="'+y_open+'" stroke="'+orange+'" stroke-width="1.5"/><text x="355" y="'+(180-dh_px/2+3)+'" fill="'+orange+'" font-size="8">Δh = '+dh_mmHg.toFixed(1)+' mmHg</text><path d="M235 265 C 235 295, 315 295, 315 265" fill="none" stroke="#94a3b8" stroke-width="8"/><path d="M235 265 C 235 295, 315 295, 315 265" fill="none" stroke="#334155" stroke-width="12" opacity="0.3"/><text x="210" y="305" text-anchor="middle" fill="'+soft+'" font-size="9">CONSTANT-VOLUME AIR THERMOMETER · JOLLY BULB & MANOMETER</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">ABSOLUTE PRESSURE (P)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.raw.toFixed(2)+'</text><text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">kPa</text><text x="'+(bX+135)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">('+(v.raw*7.5006).toFixed(1)+' mmHg)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">BATH TEMPERATURE (t)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+p.input.toFixed(1)+' °C</text><text x="'+(bX+115)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8">('+(p.input+273.15).toFixed(2)+' K)</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">GAUGE PRESSURE (Δh)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">'+(dh_mmHg>=0?'+':'')+dh_mmHg.toFixed(1)+' mmHg</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">α_v = '+alpha_cur.toFixed(5)+' K⁻¹, V = 100 cm³ const</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'P_t = P_0(1 + α_v t) ⇔ α_v = S / P_0',ink,9)+text(240,22,'Constant-Volume Air Thermometer (Jolly Bulb)')+text(240,308,'Charles\' Law / Gay-Lussac: P ∝ T (V = constant = 100.0 cm³)');}
    else if(cfg.slug==='vapor-pressure'){const T_K=p.input+273.15,invT=1.0/T_K,P_mmHg=v.raw*7.5006,dh_px=(v.raw/110.0)*110,y_cl=140+dh_px/2,y_op=140-dh_px/2,tMerc=Math.min(100,Math.max(10,((p.input-20.0)/60.0)*95));svg+='<rect x="30" y="280" width="420" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="65" y="115" width="125" height="150" rx="8" fill="#182824" stroke="'+soft+'" stroke-width="2"/><rect x="71" y="130" width="113" height="130" rx="4" fill="#0284c7" opacity="0.45"/><line x1="75" y1="265" x2="180" y2="265" stroke="#364e46" stroke-width="3"/><polygon points="122,278 127,265 132,278" fill="'+orange+'"/><path d="M85 85 V250 A8 8 0 0 1 101 250" fill="none" stroke="'+ink+'" stroke-width="1.5"/><rect x="165" y="55" width="8" height="175" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1"/><line x1="169" y1="'+(220-tMerc)+'" x2="169" y2="220" stroke="#ef4444" stroke-width="2.5"/><circle cx="169" cy="222" r="4" fill="#ef4444"/><text x="169" y="48" text-anchor="middle" fill="'+orange+'" font-size="10" font-weight="bold">'+p.input.toFixed(1)+'°C</text><ellipse cx="118" cy="185" rx="26" ry="32" fill="#a7f3d0" opacity="0.25" stroke="'+soft+'" stroke-width="1.5"/><path d="M96 195 C 96 215, 140 215, 140 195 Z" fill="#34d399" opacity="0.5"/><text x="118" y="172" text-anchor="middle" fill="#fff" font-size="7.5">ETHANOL VAPOR</text><text x="118" y="205" text-anchor="middle" fill="#a7f3d0" font-size="7">LIQUID C₂H₅OH</text><path d="M118 153 V75 H245 V105" fill="none" stroke="'+soft+'" stroke-width="2.5"/><rect x="238" y="105" width="14" height="160" rx="3" fill="none" stroke="'+soft+'" stroke-width="1.5"/><rect x="240" y="'+y_cl+'" width="10" height="'+(265-y_cl)+'" fill="#94a3b8" stroke="#64748b" stroke-width="0.5"/><ellipse cx="245" cy="'+y_cl+'" rx="5" ry="2" fill="#cbd5e1"/><line x1="280" y1="70" x2="280" y2="265" stroke="'+soft+'" stroke-width="1.5"/>';for(let k=0;k<=19;k++){const my=70+k*(195/19);svg+='<line x1="277" y1="'+my+'" x2="283" y2="'+my+'" stroke="'+soft+'" stroke-width="'+(k%5===0?1.5:0.8)+'"/>';}svg+='<rect x="315" y="60" width="14" height="205" rx="3" fill="none" stroke="'+soft+'" stroke-width="1.5"/><rect x="317" y="'+y_op+'" width="10" height="'+(265-y_op)+'" fill="#94a3b8" stroke="#64748b" stroke-width="0.5"/><ellipse cx="322" cy="'+y_op+'" rx="5" ry="2" fill="#cbd5e1"/><line x1="255" y1="'+y_cl+'" x2="315" y2="'+y_cl+'" stroke="#64748b" stroke-width="1" stroke-dasharray="2 2"/><line x1="330" y1="'+y_op+'" x2="355" y2="'+y_op+'" stroke="'+orange+'" stroke-width="1.5"/><line x1="330" y1="'+y_cl+'" x2="355" y2="'+y_cl+'" stroke="'+orange+'" stroke-width="1.5"/><line x1="350" y1="'+y_cl+'" x2="350" y2="'+y_op+'" stroke="'+orange+'" stroke-width="1.5"/><text x="360" y="'+(140+3)+'" fill="'+orange+'" font-size="8">P_sat = '+P_mmHg.toFixed(1)+' mmHg</text><path d="M245 265 C 245 295, 322 295, 322 265" fill="none" stroke="#94a3b8" stroke-width="8"/><path d="M245 265 C 245 295, 322 295, 322 265" fill="none" stroke="#334155" stroke-width="12" opacity="0.3"/><text x="210" y="305" text-anchor="middle" fill="'+soft+'" font-size="9">SATURATED VAPOR PRESSURE APPARATUS · MERCURY MANOMETER</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">SATURATED VAPOR PRESSURE (P)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.raw.toFixed(2)+'</text><text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">kPa</text><text x="'+(bX+135)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">('+P_mmHg.toFixed(1)+' mmHg)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">BATH TEMPERATURE (t)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+p.input.toFixed(1)+' °C</text><text x="'+(bX+115)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8">('+T_K.toFixed(2)+' K)</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">RECIPROCAL TEMPERATURE (1/T)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">'+(invT*1000).toFixed(3)+'</text><text x="'+(bX+100)+'" y="'+(bY+166)+'" fill="'+soft+'" font-size="9">× 10⁻³ K⁻¹</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">ln(P) = '+v.y.toFixed(3)+', ΔH = 41.92 kJ/mol</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'ln(P) = −(ΔH_vap / R)·(1/T) + C',ink,9)+text(240,22,'Saturated Vapor Pressure Apparatus (Clausius-Clapeyron)')+text(240,308,'Liquid-Vapor Phase Equilibrium: Ethanol (C₂H₅OH)');}
    else if(cfg.slug==='air-humidity'){const td=25.0,tw=25.0-p.input,es_td=3.168,es_tw=0.61078*Math.exp(17.27*tw/(tw+237.3)),e_act=Math.max(0.1,es_tw-v.raw/1000.0),rh=Math.min(100,Math.max(1,(e_act/es_td)*100)),alpha_dew=Math.log(e_act/0.61078),tdew=(237.3*alpha_dew)/(17.27-alpha_dew),tMercDry=65,tMercWet=Math.min(95,Math.max(10,65-(p.input/10.0)*35));svg+='<rect x="30" y="280" width="420" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="55" y="45" width="150" height="235" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="2"/><text x="130" y="60" text-anchor="middle" fill="#9fb498" font-size="8" font-weight="bold">VENTILATED PSYCHROMETER</text><rect x="80" y="70" width="8" height="160" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1"/><line x1="84" y1="'+(210-tMercDry)+'" x2="84" y2="210" stroke="#ef4444" stroke-width="2.5"/><circle cx="84" cy="214" r="5" fill="#ef4444"/><text x="84" y="234" text-anchor="middle" fill="'+orange+'" font-size="7.5" font-weight="bold">DRY 25°C</text><rect x="155" y="70" width="8" height="160" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1"/><line x1="159" y1="'+(210-tMercWet)+'" x2="159" y2="210" stroke="#ef4444" stroke-width="2.5"/><circle cx="159" cy="214" r="5" fill="#ef4444"/><rect x="152" y="206" width="14" height="18" rx="3" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/><rect x="151" y="224" width="16" height="22" rx="2" fill="#0284c7" opacity="0.6"/><line x1="159" y1="214" x2="159" y2="235" stroke="#f8fafc" stroke-width="2"/><text x="159" y="258" text-anchor="middle" fill="#38bdf8" font-size="7.5" font-weight="bold">WET '+tw.toFixed(1)+'°C</text>';for(let k=0;k<=3;k++){const ax=62+k*10;svg+='<path d="M'+ax+' 120 C '+(ax+15)+' 115, '+(ax+25)+' 125, '+(ax+40)+' 120" fill="none" stroke="#38bdf8" stroke-width="1" opacity="0.6"/>';}svg+='<rect x="235" y="145" width="85" height="120" rx="4" fill="#334155" stroke="#94a3b8" stroke-width="2"/><rect x="245" y="160" width="65" height="85" rx="3" fill="#cbd5e1" stroke="'+soft+'" stroke-width="1.5"/><ellipse cx="277" cy="202" rx="22" ry="28" fill="#38bdf8" opacity="0.35"/><text x="277" y="205" text-anchor="middle" fill="#0f172a" font-size="7.5" font-weight="bold">DEW MIST</text><text x="277" y="255" text-anchor="middle" fill="'+orange+'" font-size="8">T_dew = '+tdew.toFixed(1)+'°C</text><rect x="252" y="70" width="7" height="90" rx="2" fill="#1e293b" stroke="'+soft+'"/><line x1="255" y1="120" x2="255" y2="155" stroke="#ef4444" stroke-width="2"/><path d="M305 180 C 335 180, 350 220, 365 220" fill="none" stroke="'+soft+'" stroke-width="2.5"/><ellipse cx="380" cy="220" rx="15" ry="12" fill="#1b2a26" stroke="'+orange+'" stroke-width="1.5"/><text x="380" y="242" text-anchor="middle" fill="#9fb498" font-size="7">ASPIRATOR</text><text x="220" y="305" text-anchor="middle" fill="'+soft+'" font-size="9">VENTILATED PSYCHROMETER & REGNAULT DEW-POINT HYGROMETER</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">VAPOR PRESSURE DEPRESSION (Δe)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.raw.toFixed(1)+'</text><text x="'+(bX+100)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">Pa</text><text x="'+(bX+135)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">('+(v.raw*0.0075006).toFixed(2)+' mmHg)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">WET-BULB DEPRESSION (Δt)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+p.input.toFixed(1)+' °C</text><text x="'+(bX+105)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8">(t_d=25°, t_w='+tw.toFixed(1)+'°)</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">RELATIVE HUMIDITY (RH)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="18" font-family="monospace" font-weight="bold">'+rh.toFixed(1)+' %</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">e = '+(e_act*1000).toFixed(0)+' Pa, T_dew = '+tdew.toFixed(1)+' °C</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'Δe = A · P_atm · Δt ⇔ A = γ / P_atm',ink,9)+text(240,22,'Psychrometric & Dew-Point Hygrometer Apparatus')+text(240,308,'Ferrel-Sprung Equation: Δe = e_s(t_w) − e = A · P_atm · Δt');}
   else if(cfg.slug==='conical-pendulum'){const cx=240,cy=40,rad=p.input*Math.PI/180,L_px=180,h_px=L_px*Math.cos(rad),r_px=L_px*Math.sin(rad),planeY=cy+h_px,bobAngle=t*0.003,bobX=cx+r_px*Math.cos(bobAngle),bobY=planeY+(r_px/3.8)*Math.sin(bobAngle),T_sec=2*Math.PI*Math.sqrt((1.0*Math.cos(rad))/9.80665),T_sq=T_sec*T_sec;svg+='<ellipse cx="'+cx+'" cy="'+planeY+'" rx="'+r_px+'" ry="'+(r_px/3.8)+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5" stroke-dasharray="4 3"/>';for(let k=1;k<=3;k++){const gr=r_px*(k/3);svg+='<ellipse cx="'+cx+'" cy="'+planeY+'" rx="'+gr+'" ry="'+(gr/3.8)+'" fill="none" stroke="#253a34" stroke-width="1"/>';}svg+='<line x1="'+(cx-r_px)+'" y1="'+planeY+'" x2="'+(cx+r_px)+'" y2="'+planeY+'" stroke="#253a34" stroke-width="1"/><line x1="'+cx+'" y1="'+cy+'" x2="'+cx+'" y2="'+planeY+'" stroke="'+orange+'" stroke-width="1.5" stroke-dasharray="3 3"/>'+text(cx-18,(cy+planeY)/2,'h = '+(Math.cos(rad)).toFixed(3)+' m',orange,9)+'<path d="M'+cx+' '+(cy+35)+'A35 35 0 0 1 '+(cx+35*Math.sin(rad/2))+' '+(cy+35*Math.cos(rad/2))+'" fill="none" stroke="'+orange+'" stroke-width="1.5"/>'+text(cx+16,cy+46,'θ = '+p.input.toFixed(1)+'°',orange,9);svg+='<rect x="'+(cx-40)+'" y="'+(cy-10)+'" width="80" height="12" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><circle cx="'+cx+'" cy="'+cy+'" r="4" fill="'+orange+'" stroke="#fff" stroke-width="1"/>';svg+='<line x1="'+cx+'" y1="'+cy+'" x2="'+bobX+'" y2="'+bobY+'" stroke="'+soft+'" stroke-width="2"/><circle cx="'+bobX+'" cy="'+bobY+'" r="9" fill="'+orange+'" stroke="#f0b691" stroke-width="1.5"/>';const tanX=-Math.sin(bobAngle)*28,tanY=Math.cos(bobAngle)*8;svg+='<line x1="'+bobX+'" y1="'+bobY+'" x2="'+(bobX+tanX)+'" y2="'+(bobY+tanY)+'" stroke="'+ink+'" stroke-width="2"/><polygon points="'+(bobX+tanX)+','+(bobY+tanY)+' '+(bobX+tanX*0.75-tanY*0.3)+','+(bobY+tanY*0.75+tanX*0.1)+' '+(bobX+tanX*0.75+tanY*0.3)+','+(bobY+tanY*0.75-tanX*0.1)+'" fill="'+ink+'"/>'+text(bobX+tanX,bobY+tanY-6,'v',ink,8);const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">TIME FOR 20 REVS</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.raw.toFixed(2)+'</text><text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">s</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">SINGLE PERIOD T (s)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+T_sec.toFixed(4)+' s</text><text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#9fb498" font-size="8">T² = '+T_sq.toFixed(4)+' s²</text><line x1="'+(bX+15)+'" y1="'+(bY+135)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+135)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+152)+'" fill="#718e79" font-size="9">VERTICAL DEPTH h = L cos θ</text><text x="'+(bX+15)+'" y="'+(bY+176)+'" fill="'+orange+'" font-size="18" font-family="monospace" font-weight="bold">'+(Math.cos(rad)).toFixed(4)+' m</text><text x="'+(bX+15)+'" y="'+(bY+192)+'" fill="#9fb498" font-size="8">Radius r = '+(Math.sin(rad)).toFixed(3)+' m</text><line x1="'+(bX+15)+'" y1="'+(bY+200)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+200)+'" stroke="#253a34"/>'+text(bX+15,bY+214,'T² = (4π² / g) · h ⇔ g = 4π² / S',ink,9)+text(240,22,'Precision Conical Pendulum Apparatus')+text(240,308,'Uniform Circular Motion: T = 2π √(L cos θ / g)');}
  else if(cfg.slug==='ballistic-pendulum'){const pivX=240,pivY=48,pLen=150,mTot=(p.input+50)/1000,V=0.250/mTot,h_cm=v.raw,h_px=h_cm*9,theta=Math.asin(Math.min(0.95,Math.sqrt(Math.max(0,2*(h_px/pLen)-(h_px/pLen)**2)))),bobX=pivX+pLen*Math.sin(theta),bobY=pivY+pLen*Math.cos(theta),pW=40,pH=26;svg+='<rect x="50" y="280" width="380" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="60" y="170" width="100" height="20" rx="3" fill="#20312d" stroke="'+soft+'" stroke-width="2"/><line x1="75" y1="180" x2="155" y2="180" stroke="'+orange+'" stroke-width="3"/><circle cx="165" cy="180" r="7" fill="'+soft+'" stroke="'+ink+'" stroke-width="1.5"/><polygon points="80,170 70,155 90,155" fill="'+soft+'"/>'+text(110,165,'SPRING GUN',ink,8)+'<line x1="165" y1="180" x2="240" y2="180" stroke="#364e46" stroke-width="1.5" stroke-dasharray="3 3"/>';svg+='<line x1="180" y1="'+pivY+'" x2="300" y2="'+pivY+'" stroke="#1b2a26" stroke-width="6"/><circle cx="'+pivX+'" cy="'+pivY+'" r="5" fill="#20312d" stroke="'+soft+'" stroke-width="2"/><circle cx="'+pivX+'" cy="'+pivY+'" r="2" fill="'+orange+'"/><line x1="'+pivX+'" y1="'+pivY+'" x2="'+pivX+'" y2="'+(pivY+pLen)+'" stroke="#253a34" stroke-width="1.5" stroke-dasharray="2 2"/><rect x="'+(pivX-pW/2)+'" y="'+(pivY+pLen-pH/2)+'" width="'+pW+'" height="'+pH+'" rx="4" fill="none" stroke="#253a34" stroke-width="1" stroke-dasharray="2 2"/>';svg+='<line x1="'+pivX+'" y1="'+pivY+'" x2="'+bobX+'" y2="'+bobY+'" stroke="'+soft+'" stroke-width="2.5"/><rect x="'+(bobX-pW/2)+'" y="'+(bobY-pH/2)+'" width="'+pW+'" height="'+pH+'" rx="4" fill="#364e46" stroke="'+soft+'" stroke-width="1.5"/><circle cx="'+bobX+'" cy="'+bobY+'" r="6" fill="'+orange+'" stroke="#f0b691"/><rect x="'+(bobX-pW/2-4)+'" y="'+(bobY-6)+'" width="4" height="12" rx="1" fill="'+soft+'"/><rect x="'+(bobX+pW/2)+'" y="'+(bobY-6)+'" width="4" height="12" rx="1" fill="'+soft+'"/>'+text(bobX,bobY-16,'M_p = '+p.input.toFixed(0)+' g',soft,8);svg+='<path d="M'+pivX+' '+(pivY+pLen)+'A'+pLen+' '+pLen+' 0 0 1 '+(pivX+70)+' '+(pivY+pLen-18)+'" fill="none" stroke="'+orange+'" stroke-width="1.5" stroke-dasharray="3 2"/><line x1="'+(bobX+pW/2+10)+'" y1="'+(pivY+pLen)+'" x2="'+(bobX+pW/2+10)+'" y2="'+bobY+'" stroke="'+orange+'" stroke-width="1.5"/><line x1="'+(bobX+pW/2+5)+'" y1="'+(pivY+pLen)+'" x2="'+(bobX+pW/2+15)+'" y2="'+(pivY+pLen)+'" stroke="'+orange+'" stroke-width="1.5"/><line x1="'+(bobX+pW/2+5)+'" y1="'+bobY+'" x2="'+(bobX+pW/2+15)+'" y2="'+bobY+'" stroke="'+orange+'" stroke-width="1.5"/>'+text(bobX+pW/2+32,(pivY+pLen+bobY)/2,'h = '+h_cm.toFixed(2)+' cm',orange,10);const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">SWING HEIGHT (h)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+h_cm.toFixed(2)+'</text><text x="'+(bX+110)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">cm</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">POST-COLLISION VELOCITY (V)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+V.toFixed(3)+' m s⁻¹</text><text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#9fb498" font-size="8">V = √(2 g h)</text><line x1="'+(bX+15)+'" y1="'+(bY+135)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+135)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+152)+'" fill="#718e79" font-size="9">CALCULATED MUZZLE SPEED</text><text x="'+(bX+15)+'" y="'+(bY+176)+'" fill="'+orange+'" font-size="18" font-family="monospace" font-weight="bold">v₀ = 5.000 m s⁻¹</text><text x="'+(bX+15)+'" y="'+(bY+192)+'" fill="#9fb498" font-size="8">Initial momentum p₀ = 0.250 kg m s⁻¹</text><line x1="'+(bX+15)+'" y1="'+(bY+200)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+200)+'" stroke="#253a34"/>'+text(bX+15,bY+214,'Free Flight Range R = 2.258 m',ink,9)+text(240,22,'Precision Ballistic Pendulum & Projectile System')+text(240,308,'Inelastic Momentum Conservation: m_b · v₀ = (m_b + M_p) · V');}
  else if(cfg.slug==='newtons-second-law'){const trkY=160,trkL=60,trkR=520,pulX=520,pulY=trkY,pulR=12,cartW=70,cartH=32,cartX=120+(p.input/1.80)*140,cartY=trkY-cartH-4,gate1X=260,gate2X=460,hW=16,hH=24,hangY=pulY+35+(p.input/1.80)*45;svg+='<line x1="'+trkL+'" y1="'+(trkY+6)+'" x2="'+(trkR+15)+'" y2="'+(trkY+6)+'" stroke="#1b2a26" stroke-width="8"/><line x1="'+trkL+'" y1="'+trkY+'" x2="'+(trkR+15)+'" y2="'+trkY+'" stroke="'+soft+'" stroke-width="3"/><path d="M70 '+(trkY+6)+'L80 '+(trkY+35)+'M500 '+(trkY+6)+'L510 '+(trkY+35)+'" stroke="'+soft+'" stroke-width="3"/><line x1="60" y1="'+(trkY+35)+'" x2="100" y2="'+(trkY+35)+'" stroke="#1b2a26" stroke-width="4"/><line x1="490" y1="'+(trkY+35)+'" x2="530" y2="'+(trkY+35)+'" stroke="#1b2a26" stroke-width="4"/>';for(let k=0;k<=9;k++){const tx=trkL+k*50;svg+='<line x1="'+tx+'" y1="'+trkY+'" x2="'+tx+'" y2="'+(trkY+5)+'" stroke="#253a34" stroke-width="1.5"/><text x="'+tx+'" y="'+(trkY+14)+'" text-anchor="middle" fill="#9fb498" font-size="7">'+(k*20)+'</text>';}[gate1X,gate2X].forEach((gx,idx)=>{svg+='<path d="M'+(gx-8)+' '+(trkY-45)+'H'+(gx+8)+'V'+(trkY+2)+'H'+(gx-8)+'Z" fill="none" stroke="#364e46" stroke-width="2"/><circle cx="'+gx+'" cy="'+(trkY-30)+'" r="3" fill="#ef4444"/><line x1="'+gx+'" y1="'+(trkY-45)+'" x2="'+gx+'" y2="'+(trkY-55)+'" stroke="'+soft+'" stroke-width="1.5"/>'+text(gx,trkY-60,'Gate '+(idx+1),soft,8);});svg+='<rect x="'+cartX+'" y="'+cartY+'" width="'+cartW+'" height="'+cartH+'" rx="4" fill="#364e46" stroke="'+soft+'" stroke-width="1.5"/><circle cx="'+(cartX+16)+'" cy="'+(trkY-4)+'" r="4" fill="#1b2a26" stroke="'+ink+'" stroke-width="1.5"/><circle cx="'+(cartX+cartW-16)+'" cy="'+(trkY-4)+'" r="4" fill="#1b2a26" stroke="'+ink+'" stroke-width="1.5"/><rect x="'+(cartX+cartW/2-3)+'" y="'+(cartY-16)+'" width="6" height="16" fill="'+orange+'"/><rect x="'+(cartX+10)+'" y="'+(cartY+5)+'" width="20" height="14" rx="2" fill="'+soft+'"/><rect x="'+(cartX+cartW-30)+'" y="'+(cartY+5)+'" width="20" height="14" rx="2" fill="'+soft+'"/>'+text(cartX+cartW/2,cartY+16,'CART',ink,8);svg+='<circle cx="'+pulX+'" cy="'+pulY+'" r="'+pulR+'" fill="#20312d" stroke="'+soft+'" stroke-width="2"/><circle cx="'+pulX+'" cy="'+pulY+'" r="3" fill="'+orange+'"/><line x1="'+(cartX+cartW)+'" y1="'+(cartY+cartH/2)+'" x2="'+pulX+'" y2="'+(pulY-pulR)+'" stroke="'+ink+'" stroke-width="1.5"/><path d="M'+pulX+' '+(pulY-pulR)+'A'+pulR+' '+pulR+' 0 0 1 '+(pulX+pulR)+' '+pulY+'V'+hangY+'" fill="none" stroke="'+ink+'" stroke-width="1.5"/><rect x="'+(pulX+pulR-hW/2)+'" y="'+hangY+'" width="'+hW+'" height="'+hH+'" rx="2" fill="'+orange+'" stroke="#f0b691"/>'+text(pulX+pulR,hangY+hH+12,'F = '+p.input.toFixed(2)+' N',orange,9);const bX=555,bY=45,bW=150,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+12)+'" y="'+(bY+22)+'" fill="#718e79" font-size="9">ACCELERATION (a)</text><text x="'+(bX+12)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="20" font-family="monospace" font-weight="bold">'+v.raw.toFixed(3)+'</text><text x="'+(bX+100)+'" y="'+(bY+48)+'" fill="'+soft+'" font-size="10">m s⁻²</text><line x1="'+(bX+10)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-10)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+12)+'" y="'+(bY+82)+'" fill="#718e79" font-size="9">APPLIED FORCE (F)</text><text x="'+(bX+12)+'" y="'+(bY+105)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+p.input.toFixed(2)+' N</text><line x1="'+(bX+10)+'" y1="'+(bY+120)+'" x2="'+(bX+bW-10)+'" y2="'+(bY+120)+'" stroke="#253a34"/><text x="'+(bX+12)+'" y="'+(bY+138)+'" fill="#718e79" font-size="9">SYSTEM MASS (M)</text><text x="'+(bX+12)+'" y="'+(bY+160)+'" fill="'+ink+'" font-size="14" font-family="monospace">1.200 kg</text><text x="'+(bX+12)+'" y="'+(bY+176)+'" fill="#9fb498" font-size="8">(M_cart + m_hanger)</text><line x1="'+(bX+10)+'" y1="'+(bY+190)+'" x2="'+(bX+bW-10)+'" y2="'+(bY+190)+'" stroke="#253a34"/>'+text(bX+12,bY+206,'a = F / M_total',orange,10)+text(290,22,'Precision Linear Dynamic Track & Photogate Timers')+text(290,305,'Newton\'s Second Law: a = (1 / M_total) · F ⇔ M_total = 1 / S');}
  else if(cfg.slug==='free-fall'){const colX=190,topY=48,scaleH=210,botY=topY+scaleH,tH=p.input,yTarget=topY+(tH/1.20)*scaleH,v_imp=Math.sqrt(2*9.80665*tH),t_sq=v.raw*v.raw;svg+='<path d="M120 285L190 260L260 285" stroke="'+soft+'" stroke-width="4" fill="none"/><line x1="100" y1="285" x2="280" y2="285" stroke="#182824" stroke-width="6"/><circle cx="160" cy="275" r="5" fill="#20312d" stroke="'+soft+'"/><circle cx="160" cy="275" r="2" fill="'+orange+'"/><line x1="'+colX+'" y1="36" x2="'+colX+'" y2="260" stroke="#253a34" stroke-width="12"/><line x1="'+(colX-5)+'" y1="'+topY+'" x2="'+(colX-5)+'" y2="'+botY+'" stroke="'+soft+'" stroke-width="2"/>';for(let k=0;k<=12;k++){const my=topY+k*(scaleH/12);svg+='<line x1="'+(colX-10)+'" y1="'+my+'" x2="'+(colX-5)+'" y2="'+my+'" stroke="'+soft+'" stroke-width="'+(k%2===0?1.5:1)+'"/><text x="'+(colX-13)+'" y="'+(my+3)+'" text-anchor="end" fill="#9fb498" font-size="7">'+(k*0.1).toFixed(1)+' m</text>';}svg+='<rect x="'+(colX-14)+'" y="34" width="28" height="14" rx="2" fill="#889e80" stroke="#5b7454" stroke-width="1.5"/><circle cx="'+(colX+8)+'" cy="41" r="2.5" fill="#22c55e"/><rect x="'+(colX-20)+'" y="'+(yTarget-6)+'" width="40" height="12" rx="3" fill="#182824" stroke="'+orange+'" stroke-width="2"/><line x1="'+(colX-16)+'" y1="'+yTarget+'" x2="'+(colX+16)+'" y2="'+yTarget+'" stroke="'+orange+'" stroke-width="2"/><rect x="'+(colX-25)+'" y="260" width="50" height="14" rx="3" fill="#364e46" stroke="'+soft+'"/>'+text(colX,270,'STRIKE PAD',ink,7);const bobH=22,bobW=12,bobY=yTarget-bobH/2;svg+='<polygon points="'+(colX-bobW/2)+','+(bobY+bobH)+' '+(colX+bobW/2)+','+(bobY+bobH)+' '+colX+','+(bobY+bobH+8)+'" fill="'+soft+'"/><rect x="'+(colX-bobW/2)+'" y="'+bobY+'" width="'+bobW+'" height="'+bobH+'" rx="2" fill="'+soft+'" stroke="'+ink+'" stroke-width="1"/><polygon points="'+(colX-bobW/2)+','+bobY+' '+(colX+bobW/2)+','+bobY+' '+colX+','+(bobY-6)+'" fill="'+orange+'"/>';svg+='<line x1="'+(colX+30)+'" y1="'+topY+'" x2="'+(colX+30)+'" y2="'+yTarget+'" stroke="'+orange+'" stroke-width="1.5"/><line x1="'+(colX+24)+'" y1="'+topY+'" x2="'+(colX+36)+'" y2="'+topY+'" stroke="'+orange+'" stroke-width="1.5"/><line x1="'+(colX+24)+'" y1="'+yTarget+'" x2="'+(colX+36)+'" y2="'+yTarget+'" stroke="'+orange+'" stroke-width="1.5"/>'+text(colX+42,(topY+yTarget)/2,'h = '+tH.toFixed(2)+' m',orange,11);const bX=340,bY=45,bW=340,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="8" fill="#182824" stroke="'+soft+'" stroke-width="2"/><rect x="'+(bX+15)+'" y="'+(bY+20)+'" width="'+(bW-30)+'" height="65" rx="4" fill="#0d1815" stroke="#253a34"/><text x="'+(bX+30)+'" y="'+(bY+38)+'" fill="#718e79" font-size="10">TRANSIT CHRONOMETER (t)</text><text x="'+(bX+30)+'" y="'+(bY+72)+'" fill="'+orange+'" font-size="30" font-family="monospace" font-weight="bold">'+v.raw.toFixed(4)+' s</text><text x="'+(bX+220)+'" y="'+(bY+70)+'" fill="'+soft+'" font-size="14" font-family="monospace">('+ (v.raw*1000).toFixed(1) +' ms)</text><rect x="'+(bX+15)+'" y="'+(bY+100)+'" width="'+(bW/2-20)+'" height="50" rx="4" fill="#20312d" stroke="#364e46"/>'+text(bX+25,bY+118,'TIME SQUARED (t²)',soft,9)+'<text x="'+(bX+25)+'" y="'+(bY+140)+'" fill="'+ink+'" font-size="13" font-family="monospace">'+t_sq.toFixed(6)+' s²</text><rect x="'+(bX+bW/2+5)+'" y="'+(bY+100)+'" width="'+(bW/2-20)+'" height="50" rx="4" fill="#20312d" stroke="#364e46"/>'+text(bX+bW/2+15,bY+118,'IMPACT VELOCITY (v)',soft,9)+'<text x="'+(bX+bW/2+15)+'" y="'+(bY+140)+'" fill="'+ink+'" font-size="13" font-family="monospace">'+v_imp.toFixed(3)+' m/s</text><rect x="'+(bX+15)+'" y="'+(bY+160)+'" width="'+(bW-30)+'" height="48" rx="4" fill="#14221e" stroke="#253a34"/>'+text(bX+25,bY+178,'KINEMATIC GOVERNING RELATION',orange,9)+text(bX+25,bY+196,'h = 1/2 g · t² ⇔ S = 1/2 g ⇔ g = 2 · S',ink,11)+text(colX,22,'Precision Drop Tower & High-Speed Chronometer')+text(colX,308,'Free Fall from Rest under Gravitational Acceleration g = 9.80665 m s⁻²');}
   else if(cfg.slug==='equilibrium-forces'){const bY=165,bH=16,bLeft=75,bRight=645,bW=bRight-bLeft,pxPerM=570,xA=bLeft+0.10*pxPerM,xB=bLeft+0.90*pxPerM,xCG=bLeft+0.50*pxPerM,xLoad=bLeft+p.input*pxPerM,rA=7.00-v.raw,rB=v.raw,dDispA=Math.min(35,Math.max(10,rA*5)),dDispB=Math.min(35,Math.max(10,rB*5));svg+='<path d="M60 40H660M90 40V270M630 40V270" stroke="'+soft+'" stroke-width="4"/><line x1="60" y1="46" x2="660" y2="46" stroke="#1b2a26" stroke-width="6"/><line x1="'+xA+'" y1="46" x2="'+xA+'" y2="60" stroke="'+soft+'" stroke-width="2"/><rect x="'+(xA-10)+'" y="60" width="20" height="55" rx="3" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><line x1="'+xA+'" y1="65" x2="'+xA+'" y2="'+(65+dDispA)+'" stroke="'+orange+'" stroke-width="2"/><polygon points="'+xA+','+(65+dDispA+4)+' '+(xA-3)+','+(65+dDispA)+' '+(xA+3)+','+(65+dDispA)+'" fill="'+orange+'"/><line x1="'+xA+'" y1="115" x2="'+xA+'" y2="'+bY+'" stroke="'+ink+'" stroke-width="1.5"/>'+text(xA-28,92,rA.toFixed(2)+' N',orange,10)+text(xA,135,'Support A',soft,9)+'<line x1="'+xB+'" y1="46" x2="'+xB+'" y2="60" stroke="'+soft+'" stroke-width="2"/><rect x="'+(xB-10)+'" y="60" width="20" height="55" rx="3" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><line x1="'+xB+'" y1="65" x2="'+xB+'" y2="'+(65+dDispB)+'" stroke="'+orange+'" stroke-width="2"/><polygon points="'+xB+','+(65+dDispB+4)+' '+(xB-3)+','+(65+dDispB)+' '+(xB+3)+','+(65+dDispB)+'" fill="'+orange+'"/><line x1="'+xB+'" y1="115" x2="'+xB+'" y2="'+bY+'" stroke="'+ink+'" stroke-width="1.5"/>'+text(xB+28,92,rB.toFixed(2)+' N',orange,10)+text(xB,135,'Support B',soft,9)+'<rect x="'+bLeft+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="2" fill="#c49a6c" stroke="#8b6834" stroke-width="2"/>';for(let k=0;k<=10;k++){const tx=bLeft+k*57;svg+='<line x1="'+tx+'" y1="'+bY+'" x2="'+tx+'" y2="'+(bY+5)+'" stroke="#5a3d1b" stroke-width="1.5"/><text x="'+tx+'" y="'+(bY+13)+'" text-anchor="middle" fill="#5a3d1b" font-size="8">'+(k*10)+'</text>';}svg+='<circle cx="'+xCG+'" cy="'+(bY+bH/2)+'" r="4" fill="'+orange+'" stroke="#fff" stroke-width="1.5"/><line x1="'+xCG+'" y1="'+(bY+bH)+'" x2="'+xCG+'" y2="'+(bY+bH+35)+'" stroke="'+soft+'" stroke-width="2"/><polygon points="'+xCG+','+(bY+bH+40)+' '+(xCG-3)+','+(bY+bH+34)+' '+(xCG+3)+','+(bY+bH+34)+'" fill="'+soft+'"/>'+text(xCG,bY+bH+52,'W_bar = 2.00 N',soft,9)+'<rect x="'+(xLoad-6)+'" y="'+(bY-2)+'" width="12" height="'+(bH+4)+'" rx="2" fill="none" stroke="'+ink+'" stroke-width="2"/><line x1="'+xLoad+'" y1="'+(bY+bH)+'" x2="'+xLoad+'" y2="'+(bY+bH+25)+'" stroke="'+ink+'" stroke-width="1.5"/><rect x="'+(xLoad-14)+'" y="'+(bY+bH+25)+'" width="28" height="32" rx="3" fill="'+orange+'" stroke="#f0b691"/><line x1="'+xLoad+'" y1="'+(bY+bH+57)+'" x2="'+xLoad+'" y2="'+(bY+bH+70)+'" stroke="'+orange+'" stroke-width="2"/><polygon points="'+xLoad+','+(bY+bH+76)+' '+(xLoad-4)+','+(bY+bH+68)+' '+(xLoad+4)+','+(bY+bH+68)+'" fill="'+orange+'"/>'+text(xLoad,bY+bH+90,'W_load = 5.00 N',orange,10)+'<path d="M'+xA+' '+(bY-12)+'H'+xLoad+'M'+xA+' '+(bY-17)+'V'+(bY-7)+'M'+xLoad+' '+(bY-17)+'V'+(bY-7)+'" stroke="'+orange+'" stroke-width="1.5"/>'+text((xA+xLoad)/2,bY-20,'x = '+p.input.toFixed(2)+' m',orange,10)+'<path d="M'+xA+' 30H'+xB+'M'+xA+' 25V35M'+xB+' 25V35" stroke="'+soft+'" stroke-width="1.5"/>'+text((xA+xB)/2,22,'Span d_AB = 0.800 m',soft,10)+text(360,290,'Translational Balance: R_A + R_B = 2.00 N + 5.00 N = 7.00 N',ink,11)+text(360,308,'Moment Equilibrium about A: R_B = (W_load / d_AB) · (x − x_A) + R_B0');}
   else if(cfg.slug==='loaded-spring'){const spX=220,topY=50,m_kg=p.input/1000.0,M_tot=m_kg+0.0200,T_osc=v.period,oscAmp=14*Math.cos(phase*(2*Math.PI/T_osc)),eqExt=45+(p.input/350.0)*40,currExt=eqExt+oscAmp,botY=topY+currExt+60;svg+='<rect x="30" y="280" width="400" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="70" y="270" width="80" height="10" rx="2" fill="#20312d" stroke="'+soft+'" stroke-width="1.5"/><line x1="110" y1="270" x2="110" y2="40" stroke="#1b2a26" stroke-width="10"/><line x1="108" y1="270" x2="108" y2="40" stroke="'+soft+'" stroke-width="2"/><rect x="100" y="44" width="20" height="16" rx="2" fill="#364e46" stroke="'+soft+'" stroke-width="1.5"/><line x1="110" y1="52" x2="'+(spX+8)+'" y2="52" stroke="'+soft+'" stroke-width="5"/><circle cx="'+spX+'" cy="52" r="3" fill="'+orange+'"/>';const numTurns=16,coilW=14;let coilD='M '+spX+' 52 L '+spX+' '+(topY+5);const coilH=botY-topY-45;for(let i=0;i<numTurns;i++){const y1=topY+5+(i+0.25)*(coilH/numTurns),y2=topY+5+(i+0.75)*(coilH/numTurns),y3=topY+5+(i+1.0)*(coilH/numTurns);coilD+=' C '+(spX-coilW)+' '+y1+', '+(spX+coilW)+' '+y2+', '+spX+' '+y3;}coilD+=' L '+spX+' '+(botY-35);svg+='<path d="'+coilD+'" fill="none" stroke="'+ink+'" stroke-width="2.5" stroke-linecap="round"/><path d="M '+spX+' '+(botY-35)+' V '+(botY-25)+' A 4 4 0 0 0 '+(spX+8)+' '+(botY-25)+'" fill="none" stroke="'+orange+'" stroke-width="2"/><line x1="'+spX+'" y1="'+(botY-25)+'" x2="'+spX+'" y2="'+(botY+20)+'" stroke="'+orange+'" stroke-width="2.5"/>';const numDisks=Math.max(1,Math.round(p.input/50)),hBaseY=botY+20;svg+='<rect x="'+(spX-22)+'" y="'+hBaseY+'" width="44" height="6" rx="2" fill="#d97706" stroke="#b45309" stroke-width="1"/>';for(let d=0;d<numDisks;d++){const diskY=hBaseY-4-(d+1)*6;svg+='<rect x="'+(spX-18)+'" y="'+diskY+'" width="36" height="5.5" rx="1.5" fill="#f59e0b" stroke="#b45309" stroke-width="0.8"/><line x1="'+(spX-4)+'" y1="'+diskY+'" x2="'+(spX-4)+'" y2="'+(diskY+5.5)+'" stroke="#78350f" stroke-width="0.8"/>';}const ptrY=botY-25;svg+='<line x1="'+spX+'" y1="'+ptrY+'" x2="'+(spX+55)+'" y2="'+ptrY+'" stroke="'+orange+'" stroke-width="1.8"/><polygon points="'+(spX+55)+','+ptrY+' '+(spX+48)+','+(ptrY-3)+' '+(spX+48)+','+(ptrY+3)+'" fill="'+orange+'"/>';const scX=spX+60,scY1=50,scY2=270;svg+='<rect x="'+scX+'" y="'+scY1+'" width="22" height="'+(scY2-scY1)+'" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/>';for(let k=0;k<=22;k++){const sy=scY1+k*10,isMajor=k%5===0;svg+='<line x1="'+scX+'" y1="'+sy+'" x2="'+(scX+(isMajor?12:6))+'" y2="'+sy+'" stroke="'+soft+'" stroke-width="'+(isMajor?1.5:0.8)+'"/>';if(isMajor)svg+='<text x="'+(scX+14)+'" y="'+(sy+3)+'" fill="#9fb498" font-size="7">'+k+'</text>';}const eqPtrY=topY+eqExt+60-25;svg+='<line x1="'+(scX-15)+'" y1="'+eqPtrY+'" x2="'+(scX+25)+'" y2="'+eqPtrY+'" stroke="#38bdf8" stroke-width="1" stroke-dasharray="3 2"/><text x="'+(scX-18)+'" y="'+(eqPtrY+3)+'" text-anchor="end" fill="#38bdf8" font-size="7.5">y₀ eq</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">TIME FOR 20 CYCLES (t₂₀)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.raw.toFixed(2)+'</text><text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">s</text><text x="'+(bX+125)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">(±0.05 s)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">PERIOD T & PERIOD SQUARED T²</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+T_osc.toFixed(4)+' s</text><text x="'+(bX+125)+'" y="'+(bY+108)+'" fill="'+orange+'" font-size="13" font-family="monospace">T² = '+(T_osc*T_osc).toFixed(4)+' s²</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">SUSPENDED LOAD MASS (m)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">'+p.input.toFixed(1)+' g</text><text x="'+(bX+110)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">('+(p.input/1000).toFixed(4)+' kg)</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">Spring Wire m_s = 60.0 g · m_eff = 20.0 g</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'T² = (4π²/k)·m + (4π²/k)·m_eff ⇔ k = 4π²/S',ink,9)+text(240,22,'Helical Spring Oscillometer & Pointer Bench')+text(240,308,'Rayleigh Spring Self-Mass Theorem: m_eff = 1/3 · m_spring = 20.0 g');}
   else if(cfg.slug==='pendulum-coincidence'){const pivY=48,mPivX=150,tPivX=275,L0_px=160,L_px=100+(p.input-65.0)*2.0,T0=2.0000,T_test=v.period,amp0=0.08,amp1=0.08,th0=amp0*Math.sin(phase*(2*Math.PI/T0)),th1=amp1*Math.sin(phase*(2*Math.PI/T_test)),mBobX=mPivX+L0_px*Math.sin(th0),mBobY=pivY+L0_px*Math.cos(th0),tBobX=tPivX+L_px*Math.sin(th1),tBobY=pivY+L_px*Math.cos(th1),vel0=Math.cos(phase*(2*Math.PI/T0)),vel1=Math.cos(phase*(2*Math.PI/T_test)),isCoinc=(Math.abs(th0)<0.02&&Math.abs(th1)<0.02&&(vel0*vel1>0));svg+='<rect x="30" y="280" width="400" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="50" y="270" width="70" height="10" rx="2" fill="#20312d" stroke="'+soft+'" stroke-width="1.5"/><line x1="85" y1="270" x2="85" y2="40" stroke="#1b2a26" stroke-width="10"/><line x1="83" y1="270" x2="83" y2="40" stroke="'+soft+'" stroke-width="2"/><rect x="75" y="42" width="20" height="16" rx="2" fill="#364e46" stroke="'+soft+'" stroke-width="1.5"/><line x1="85" y1="48" x2="330" y2="48" stroke="'+soft+'" stroke-width="6"/>';[mPivX,tPivX].forEach(px=>{svg+='<polygon points="'+(px-8)+',48 '+(px+8)+',48 '+px+',55" fill="'+orange+'"/><circle cx="'+px+'" cy="48" r="3" fill="#1b2a26" stroke="'+soft+'"/>';});svg+='<line x1="'+mPivX+'" y1="48" x2="'+mBobX.toFixed(1)+'" y2="'+mBobY.toFixed(1)+'" stroke="'+soft+'" stroke-width="2"/><circle cx="'+mBobX.toFixed(1)+'" cy="'+mBobY.toFixed(1)+'" r="14" fill="#334155" stroke="'+soft+'" stroke-width="1.5"/><line x1="'+mBobX.toFixed(1)+'" y1="'+(mBobY-10).toFixed(1)+'" x2="'+mBobX.toFixed(1)+'" y2="'+(mBobY+10).toFixed(1)+'" stroke="#fde68a" stroke-width="1.5"/><text x="'+mPivX+'" y="38" text-anchor="middle" fill="#9fb498" font-size="8">MASTER CLOCK (T₀=2.00 s)</text><line x1="'+tPivX+'" y1="48" x2="'+tBobX.toFixed(1)+'" y2="'+tBobY.toFixed(1)+'" stroke="'+ink+'" stroke-width="2"/><circle cx="'+tBobX.toFixed(1)+'" cy="'+tBobY.toFixed(1)+'" r="13" fill="#b45309" stroke="#d97706" stroke-width="2"/><circle cx="'+tBobX.toFixed(1)+'" cy="'+tBobY.toFixed(1)+'" r="4" fill="#fde68a"/><text x="'+tPivX+'" y="38" text-anchor="middle" fill="'+orange+'" font-size="8">TEST PENDULUM (L='+p.input.toFixed(1)+' cm)</text>';const telX=212,telY=195;svg+='<rect x="'+(telX-22)+'" y="'+telY+'" width="44" height="26" rx="4" fill="#182824" stroke="'+(isCoinc?'#22c55e':soft)+'" stroke-width="'+(isCoinc?'2.5':'1.5')+'"/><line x1="'+telX+'" y1="'+(telY-15)+'" x2="'+telX+'" y2="'+(telY+40)+'" stroke="'+(isCoinc?'#22c55e':soft)+'" stroke-dasharray="3 2" stroke-width="1.5"/><line x1="'+(telX-18)+'" y1="'+(telY+13)+'" x2="'+(telX+18)+'" y2="'+(telY+13)+'" stroke="'+(isCoinc?'#22c55e':soft)+'" stroke-width="1.5"/><circle cx="'+telX+'" cy="'+(telY+13)+'" r="4" fill="'+(isCoinc?'#22c55e':'#101c18')+'" stroke="'+(isCoinc?'#fff':soft)+'"/>';if(isCoinc){svg+='<rect x="'+(telX-42)+'" y="'+(telY+45)+'" width="84" height="18" rx="3" fill="#052e16" stroke="#22c55e" stroke-width="1.5"/><text x="'+telX+'" y="'+(telY+58)+'" text-anchor="middle" fill="#4ade80" font-size="8" font-weight="bold">COINCIDENCE!</text>';}else{svg+='<text x="'+telX+'" y="'+(telY+56)+'" text-anchor="middle" fill="#718e79" font-size="7.5">OPTICAL SLIT</text>';}const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">COINCIDENCE INTERVAL (t_c)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.raw.toFixed(2)+'</text><text x="'+(bX+110)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">s</text><text x="'+(bX+130)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">(N = '+(v.raw/T_test).toFixed(1)+')</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">DEDUCED HIGH-PRECISION PERIOD</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+T_test.toFixed(5)+' s</text><text x="'+(bX+135)+'" y="'+(bY+108)+'" fill="'+orange+'" font-size="12" font-family="monospace">T²='+(T_test*T_test).toFixed(4)+'</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">EFFECTIVE LENGTH (L)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">'+p.input.toFixed(1)+' cm</text><text x="'+(bX+115)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">('+(p.input/100).toFixed(4)+' m)</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">T₀ = 2.00000 s (Master Invar Clock)</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'T = (T₀·t_c)/(t_c + T₀) ⇔ g = 4π² / S',ink,9)+text(240,22,'Borda-Laplace Pendulum Coincidence Bench')+text(240,308,'Temporal Vernier: Δf = 1/t_c · Precision Gravimetry g = 9.807 m s⁻²');}
   else if(cfg.slug==='torsion-pendulum'){const wX=220,topY=50,L_px=75+(p.input-40.0)*1.7,T_osc=v.period,maxTwist=0.28,twist=maxTwist*Math.cos(phase*(2*Math.PI/T_osc)),discY=topY+L_px,discRx=85,discRy=20,discH=14;svg+='<rect x="30" y="280" width="400" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><rect x="50" y="270" width="70" height="10" rx="2" fill="#20312d" stroke="'+soft+'" stroke-width="1.5"/><line x1="85" y1="270" x2="85" y2="40" stroke="#1b2a26" stroke-width="10"/><line x1="83" y1="270" x2="83" y2="40" stroke="'+soft+'" stroke-width="2"/><rect x="75" y="40" width="20" height="16" rx="2" fill="#364e46" stroke="'+soft+'" stroke-width="1.5"/><line x1="85" y1="46" x2="235" y2="46" stroke="'+soft+'" stroke-width="6"/><rect x="'+(wX-8)+'" y="46" width="16" height="14" rx="2" fill="#475569" stroke="'+ink+'" stroke-width="1.5"/><line x1="'+(wX-10)+'" y1="52" x2="'+(wX+10)+'" y2="52" stroke="'+orange+'" stroke-width="1"/><rect x="'+(wX-105)+'" y="35" width="210" height="240" rx="6" fill="#182824" opacity="0.3" stroke="'+soft+'" stroke-width="1" stroke-dasharray="4 2"/><text x="'+(wX-95)+'" y="270" fill="#718e79" font-size="7.5">DRAUGHT SHIELD</text><line x1="'+wX+'" y1="60" x2="'+wX+'" y2="'+discY+'" stroke="'+ink+'" stroke-width="2.5"/>';for(let i=0;i<5;i++){const wy=65+i*((discY-70)/5),off=Math.sin(twist+i*1.2)*2.5;svg+='<line x1="'+(wX-1.5+off)+'" y1="'+wy+'" x2="'+(wX+1.5-off)+'" y2="'+(wy+8)+'" stroke="'+orange+'" stroke-width="1" opacity="0.75"/>';}svg+='<rect x="'+(wX-7)+'" y="'+(discY-6)+'" width="14" height="12" rx="2" fill="#475569" stroke="'+ink+'" stroke-width="1.5"/><path d="M '+(wX-discRx)+' '+discY+' A '+discRx+' '+discRy+' 0 0 0 '+(wX+discRx)+' '+discY+' V '+(discY+discH)+' A '+discRx+' '+discRy+' 0 0 1 '+(wX-discRx)+' '+(discY+discH)+' Z" fill="#b45309" stroke="#d97706" stroke-width="1.5"/><ellipse cx="'+wX+'" cy="'+discY+'" rx="'+discRx+'" ry="'+discRy+'" fill="#d97706" stroke="#fde68a" stroke-width="1.5"/>';for(let a=0;a<4;a++){const spokeRad=twist+(a*Math.PI/2),sx=wX+(discRx-6)*Math.cos(spokeRad),sy=discY+(discRy-3)*Math.sin(spokeRad);svg+='<line x1="'+wX+'" y1="'+discY+'" x2="'+sx.toFixed(1)+'" y2="'+sy.toFixed(1)+'" stroke="#78350f" stroke-width="1.5"/><circle cx="'+sx.toFixed(1)+'" cy="'+sy.toFixed(1)+'" r="2" fill="#fde68a"/>';}svg+='<circle cx="'+wX+'" cy="'+discY+'" r="5" fill="#475569" stroke="'+ink+'" stroke-width="1"/>';const ptrRad=twist,pxEnd=wX+(discRx+16)*Math.cos(ptrRad),pyEnd=discY+(discRy+4)*Math.sin(ptrRad);svg+='<line x1="'+wX+'" y1="'+discY+'" x2="'+pxEnd.toFixed(1)+'" y2="'+pyEnd.toFixed(1)+'" stroke="'+orange+'" stroke-width="2"/><polygon points="'+pxEnd.toFixed(1)+','+pyEnd.toFixed(1)+' '+(pxEnd-Math.cos(ptrRad)*6+Math.sin(ptrRad)*3).toFixed(1)+','+(pyEnd-Math.sin(ptrRad)*6-Math.cos(ptrRad)*3).toFixed(1)+' '+(pxEnd-Math.cos(ptrRad)*6-Math.sin(ptrRad)*3).toFixed(1)+','+(pyEnd-Math.sin(ptrRad)*6+Math.cos(ptrRad)*3).toFixed(1)+'" fill="'+orange+'"/>';const eqX=wX+(discRx+16);svg+='<line x1="'+eqX+'" y1="'+(discY-12)+'" x2="'+eqX+'" y2="'+(discY+16)+'" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3 2"/><text x="'+(eqX+4)+'" y="'+(discY+4)+'" fill="#38bdf8" font-size="7.5">0° eq</text><line x1="'+(wX+30)+'" y1="60" x2="'+(wX+30)+'" y2="'+discY+'" stroke="'+soft+'" stroke-width="1" stroke-dasharray="2 2"/><line x1="'+(wX+25)+'" y1="60" x2="'+(wX+35)+'" y2="60" stroke="'+soft+'" stroke-width="1"/><line x1="'+(wX+25)+'" y1="'+discY+'" x2="'+(wX+35)+'" y2="'+discY+'" stroke="'+soft+'" stroke-width="1"/><text x="'+(wX+40)+'" y="'+((60+discY)/2)+'" fill="'+soft+'" font-size="8">L = '+p.input.toFixed(1)+' cm</text>';const bX=470,bY=45,bW=220,bH=220;svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">TIME FOR 20 OSCILLATIONS (t₂₀)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+v.raw.toFixed(2)+'</text><text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">s</text><text x="'+(bX+125)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">(±0.05 s)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">PERIOD T & PERIOD SQUARED T²</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace">'+T_osc.toFixed(4)+' s</text><text x="'+(bX+125)+'" y="'+(bY+108)+'" fill="'+orange+'" font-size="13" font-family="monospace">T² = '+(T_osc*T_osc).toFixed(4)+' s²</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">ACTIVE WIRE LENGTH (L)</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="16" font-family="monospace" font-weight="bold">'+p.input.toFixed(1)+' cm</text><text x="'+(bX+115)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">('+(p.input/100).toFixed(4)+' m)</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">Steel d = 1.200 mm · I = 0.0100 kg m²</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'T² = [8π I / (η r⁴)] · L ⇔ η = 8π I / (S · r⁴)',ink,9)+text(240,22,'Coulomb Torsion Pendulum Apparatus')+text(240,308,'Modulus of Rigidity: τ = −κ θ · Fourth-Power Radius Law r⁴ · η = 78.50 GPa');}
   else if(cfg.slug==='resonance-air-column'){
    const tX=200,topY=65,tubeW=32,tubeH=210;
    const L1_cm=v.raw;
    const waterY=topY+(L1_cm/45.0)*160.0;
    const fHz=p.input;
    const prongW=0.35*Math.cos(phase*(2*Math.PI*Math.min(30,fHz/15)));
    const forkY=topY-32;
    svg+='<rect x="30" y="280" width="400" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><line x1="80" y1="280" x2="80" y2="35" stroke="#1b2a26" stroke-width="10"/><line x1="78" y1="280" x2="78" y2="35" stroke="'+soft+'" stroke-width="2"/><rect x="70" y="80" width="135" height="8" rx="2" fill="#364e46" stroke="'+soft+'" stroke-width="1"/><rect x="70" y="210" width="135" height="8" rx="2" fill="#364e46" stroke="'+soft+'" stroke-width="1"/><rect x="'+(tX-tubeW/2)+'" y="'+topY+'" width="'+tubeW+'" height="'+tubeH+'" rx="3" fill="#13231e" stroke="#60a5fa" stroke-width="2" opacity="0.85"/><rect x="'+(tX-tubeW/2+2)+'" y="'+waterY+'" width="'+(tubeW-4)+'" height="'+(topY+tubeH-waterY)+'" fill="#0284c7" opacity="0.6"/>';
    const ripple=Math.sin(phase*12)*1.2;
    svg+='<ellipse cx="'+tX+'" cy="'+(waterY+ripple)+'" rx="'+(tubeW/2-2)+'" ry="4" fill="#38bdf8" stroke="#bae6fd" stroke-width="1"/>';
    for(let g=0;g<=20;g++){
      const gy=topY+g*(tubeH/20),isMajor=(g%5===0);
      svg+='<line x1="'+(tX+tubeW/2)+'" y1="'+gy+'" x2="'+(tX+tubeW/2+(isMajor?8:4))+'" y2="'+gy+'" stroke="'+soft+'" stroke-width="'+(isMajor?1.5:1)+'"/>';
      if(isMajor)svg+='<text x="'+(tX+tubeW/2+12)+'" y="'+(gy+3)+'" fill="'+soft+'" font-size="7">'+(g*2)+'</text>';
    }
    svg+='<rect x="'+(tX-tubeW/2-3)+'" y="'+(waterY-3)+'" width="'+(tubeW+6)+'" height="6" rx="2" fill="#ef4444" stroke="#fca5a5" stroke-width="1"/><text x="'+(tX-tubeW/2-6)+'" y="'+(waterY+2)+'" text-anchor="end" fill="#ef4444" font-size="8">L₁ marker</text>';
    const resX=340,resY=waterY-20,resW=38,resH=70;
    svg+='<line x1="375" y1="280" x2="375" y2="35" stroke="#1b2a26" stroke-width="8"/><line x1="373" y1="280" x2="373" y2="35" stroke="'+soft+'" stroke-width="1.5"/><rect x="365" y="'+(resY+15)+'" width="20" height="10" rx="2" fill="#364e46" stroke="'+soft+'" stroke-width="1"/><rect x="'+resX+'" y="'+resY+'" width="'+resW+'" height="'+resH+'" rx="4" fill="#164e63" stroke="#38bdf8" stroke-width="1.5"/><rect x="'+(resX+2)+'" y="'+(resY+15)+'" width="'+(resW-4)+'" height="'+(resH-17)+'" fill="#0284c7" opacity="0.6"/><text x="'+(resX+resW/2)+'" y="'+(resY+40)+'" text-anchor="middle" fill="#bae6fd" font-size="7.5">Reservoir</text>';
    const tubeBottom=topY+tubeH;
    svg+='<path d="M '+(resX+resW/2)+' '+(resY+resH)+' C '+(resX+resW/2)+' 275, '+tX+' 275, '+tX+' '+tubeBottom+'" fill="none" stroke="#78350f" stroke-width="6" stroke-linecap="round"/><path d="M '+(resX+resW/2)+' '+(resY+resH)+' C '+(resX+resW/2)+' 275, '+tX+' 275, '+tX+' '+tubeBottom+'" fill="none" stroke="#92400e" stroke-width="3" stroke-linecap="round"/>';
    svg+='<line x1="'+tX+'" y1="'+(forkY-15)+'" x2="'+tX+'" y2="'+forkY+'" stroke="'+soft+'" stroke-width="4"/><path d="M '+(tX-10+prongW*4)+' '+(forkY-28)+' V '+forkY+' H '+(tX+10-prongW*4)+' V '+(forkY-28)+'" fill="none" stroke="#e2e8f0" stroke-width="3" stroke-linecap="round"/><rect x="'+(tX-3)+'" y="'+forkY+'" width="6" height="12" rx="1" fill="#94a3b8"/><text x="'+tX+'" y="'+(forkY-33)+'" text-anchor="middle" fill="'+orange+'" font-size="8.5" font-weight="bold">'+fHz.toFixed(1)+' Hz</text>';
    for(let a=1;a<=3;a++){
      const arcR=a*7+((phase*18)%10),arcY=topY-8+arcR;
      if(arcY<topY+25)svg+='<path d="M '+(tX-arcR*.75)+' '+arcY+' Q '+tX+' '+(arcY+arcR*.4)+' '+(tX+arcR*.75)+' '+arcY+'" fill="none" stroke="'+orange+'" stroke-width="1.2" opacity="'+(1-a*0.25)+'"/>';
    }
    const antinodeY=topY-6;
    let waveL=[],waveR=[];
    for(let w=0;w<=20;w++){
      const nw=w/20,wy=antinodeY+nw*(waterY-antinodeY),ampl=Math.cos((Math.PI/2)*nw)*Math.cos(phase*12)*(tubeW/2-4);
      waveL.push((tX-ampl).toFixed(1)+','+wy.toFixed(1));waveR.push((tX+ampl).toFixed(1)+','+wy.toFixed(1));
    }
    svg+='<polyline points="'+waveL.join(' ')+'" fill="none" stroke="'+ink+'" stroke-width="1.5" stroke-dasharray="3 2" opacity="0.75"/><polyline points="'+waveR.join(' ')+'" fill="none" stroke="'+ink+'" stroke-width="1.5" stroke-dasharray="3 2" opacity="0.75"/>';
    svg+='<line x1="'+(tX-tubeW/2-10)+'" y1="'+topY+'" x2="'+(tX-tubeW/2-10)+'" y2="'+antinodeY+'" stroke="'+orange+'" stroke-width="1"/><text x="'+(tX-tubeW/2-14)+'" y="'+((topY+antinodeY)/2+3)+'" text-anchor="end" fill="'+orange+'" font-size="7">c≈0.98cm</text>';
    svg+='<line x1="'+(tX-tubeW/2-10)+'" y1="'+topY+'" x2="'+(tX-tubeW/2-10)+'" y2="'+waterY+'" stroke="'+soft+'" stroke-width="1"/><line x1="'+(tX-tubeW/2-14)+'" y1="'+topY+'" x2="'+(tX-tubeW/2-6)+'" y2="'+topY+'" stroke="'+soft+'" stroke-width="1"/><line x1="'+(tX-tubeW/2-14)+'" y1="'+waterY+'" x2="'+(tX-tubeW/2-6)+'" y2="'+waterY+'" stroke="'+soft+'" stroke-width="1"/><text x="'+(tX-tubeW/2-14)+'" y="'+((topY+waterY)/2+3)+'" text-anchor="end" fill="'+soft+'" font-size="8">L₁='+L1_cm.toFixed(1)+'cm</text>';
    const bX=470,bY=45,bW=220,bH=220,lambda_m=4.0*(L1_cm+0.98)/100.0,v_est=fHz*lambda_m;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">TUNING FORK FREQUENCY (f)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+fHz.toFixed(1)+'</text><text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">Hz</text><text x="'+(bX+130)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">(Middle Scale)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">FIRST RESONANCE LENGTH (L₁)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="18" font-family="monospace">'+L1_cm.toFixed(2)+' cm</text><text x="'+(bX+130)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">(±0.05 cm)</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">WAVELENGTH λ & SOUND VELOCITY v</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">'+v_est.toFixed(1)+' m s⁻¹</text><text x="'+(bX+135)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">(λ='+(lambda_m*100).toFixed(1)+' cm)</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">c = 0.6133 r = 0.98 cm · T = 20.0 °C</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'L₁ = (v/4)(1/f) − c ⇔ v = 4m · c = −b',ink,9)+text(240,22,'Resonance Tube Apparatus with Water Reservoir')+text(240,308,'Speed of Sound in Air: v = 343.2 m s⁻¹ · Rayleigh End Correction c = 0.6133 r');
  }
   else if(cfg.slug==='modes-air-column'){
    const fHz=p.input;
    const L_cm=v.raw;
    const pipeY=145,tubeH=42;
    const leftX=70;
    const pipeL_px=140.0+(L_cm-30.0)*5.5;
    const rightX=leftX+pipeL_px;
    svg+='<rect x="30" y="270" width="410" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/><polygon points="110,270 120,225 150,225 160,270" fill="#20312d" stroke="'+soft+'" stroke-width="1.5"/><polygon points="310,270 320,225 350,225 360,270" fill="#20312d" stroke="'+soft+'" stroke-width="1.5"/><path d="M 120 225 L 135 '+(pipeY+tubeH/2)+' L 150 225" fill="none" stroke="'+soft+'" stroke-width="2"/><path d="M 320 225 L 335 '+(pipeY+tubeH/2)+' L 350 225" fill="none" stroke="'+soft+'" stroke-width="2"/><rect x="'+leftX+'" y="'+pipeY+'" width="'+(pipeL_px*0.55)+'" height="'+tubeH+'" rx="3" fill="#b45309" stroke="#d97706" stroke-width="2" opacity="0.85"/><rect x="'+(leftX+pipeL_px*0.35)+'" y="'+(pipeY-3)+'" width="'+(pipeL_px*0.65)+'" height="'+(tubeH+6)+'" rx="4" fill="#0284c7" stroke="#38bdf8" stroke-width="2" opacity="0.75"/><rect x="'+(leftX+pipeL_px*0.35)+'" y="'+(pipeY-5)+'" width="10" height="'+(tubeH+10)+'" rx="2" fill="#364e46" stroke="'+soft+'" stroke-width="1.5"/><path d="M 38 '+(pipeY-8)+' L '+(leftX-12)+' '+(pipeY+4)+' V '+(pipeY+tubeH-4)+' L 38 '+(pipeY+tubeH+8)+' Z" fill="#334155" stroke="'+soft+'" stroke-width="1.5"/><rect x="24" y="'+(pipeY+6)+'" width="14" height="'+(tubeH-12)+'" rx="2" fill="#1e293b" stroke="'+soft+'" stroke-width="1.5"/><text x="31" y="'+(pipeY+tubeH/2+4)+'" text-anchor="middle" fill="'+orange+'" font-size="8" font-weight="bold">DRV</text>';
    for(let a=1;a<=3;a++){
      const arcOff=a*5+((phase*24)%8),arcX=leftX-10+arcOff;
      if(arcX<leftX+25)svg+='<path d="M '+arcX+' '+(pipeY+6)+' Q '+(arcX+6)+' '+(pipeY+tubeH/2)+' '+arcX+' '+(pipeY+tubeH-6)+'" fill="none" stroke="'+orange+'" stroke-width="1.2" opacity="'+(1-a*0.25)+'"/>';
    }
    for(let a=1;a<=3;a++){
      const arcOff=a*6+((phase*24)%10),arcX=rightX+arcOff;
      svg+='<path d="M '+arcX+' '+(pipeY+4)+' Q '+(arcX+8)+' '+(pipeY+tubeH/2)+' '+arcX+' '+(pipeY+tubeH-4)+'" fill="none" stroke="'+orange+'" stroke-width="1.2" opacity="'+(1-a*0.28)+'"/>';
    }
    const c_px=14.0,antinodeLeft=leftX-c_px,antinodeRight=rightX+c_px,midX=(antinodeLeft+antinodeRight)/2.0;
    let waveTop=[],waveBot=[];
    for(let w=0;w<=30;w++){
      const nw=w/30.0,wx=antinodeLeft+nw*(antinodeRight-antinodeLeft),uDisp=Math.cos(Math.PI*nw)*Math.cos(phase*14)*(tubeH/2-6);
      waveTop.push(wx.toFixed(1)+','+(pipeY+tubeH/2-uDisp).toFixed(1));waveBot.push(wx.toFixed(1)+','+(pipeY+tubeH/2+uDisp).toFixed(1));
    }
    svg+='<polyline points="'+waveTop.join(' ')+'" fill="none" stroke="'+ink+'" stroke-width="2" stroke-dasharray="3 2"/><polyline points="'+waveBot.join(' ')+'" fill="none" stroke="'+ink+'" stroke-width="2" stroke-dasharray="3 2"/><line x1="'+midX.toFixed(1)+'" y1="'+(pipeY-10)+'" x2="'+midX.toFixed(1)+'" y2="'+(pipeY+tubeH+10)+'" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3 2"/><circle cx="'+midX.toFixed(1)+'" cy="'+(pipeY+tubeH/2)+'" r="3.5" fill="#38bdf8"/><text x="'+midX.toFixed(1)+'" y="'+(pipeY-14)+'" text-anchor="middle" fill="#38bdf8" font-size="8">Displacement Node (u=0)</text><line x1="'+antinodeLeft.toFixed(1)+'" y1="'+(pipeY-8)+'" x2="'+leftX+'" y2="'+(pipeY-8)+'" stroke="'+orange+'" stroke-width="1.2"/><text x="'+((antinodeLeft+leftX)/2)+'" y="'+(pipeY-12)+'" text-anchor="middle" fill="'+orange+'" font-size="7">c≈1.2cm</text><line x1="'+rightX+'" y1="'+(pipeY-8)+'" x2="'+antinodeRight.toFixed(1)+'" y2="'+(pipeY-8)+'" stroke="'+orange+'" stroke-width="1.2"/><text x="'+((rightX+antinodeRight)/2)+'" y="'+(pipeY-12)+'" text-anchor="middle" fill="'+orange+'" font-size="7">c≈1.2cm</text><line x1="'+leftX+'" y1="'+(pipeY+tubeH+22)+'" x2="'+rightX.toFixed(1)+'" y2="'+(pipeY+tubeH+22)+'" stroke="'+soft+'" stroke-width="1.5"/><line x1="'+leftX+'" y1="'+(pipeY+tubeH+16)+'" x2="'+leftX+'" y2="'+(pipeY+tubeH+28)+'" stroke="'+soft+'" stroke-width="1.5"/><line x1="'+rightX.toFixed(1)+'" y1="'+(pipeY+tubeH+16)+'" x2="'+rightX.toFixed(1)+'" y2="'+(pipeY+tubeH+28)+'" stroke="'+soft+'" stroke-width="1.5"/><text x="'+((leftX+rightX)/2)+'" y="'+(pipeY+tubeH+36)+'" text-anchor="middle" fill="'+soft+'" font-size="9" font-weight="bold">Tube Length L = '+L_cm.toFixed(2)+' cm</text>';
    for(let g=0;g<=15;g++){
      const gx=leftX+g*(pipeL_px/15),isMaj=(g%5===0);
      svg+='<line x1="'+gx.toFixed(1)+'" y1="270" x2="'+gx.toFixed(1)+'" y2="'+(270-(isMaj?8:4))+'" stroke="'+soft+'" stroke-width="'+(isMaj?1.5:1)+'"/>';
      if(isMaj)svg+='<text x="'+gx.toFixed(1)+'" y="280" text-anchor="middle" fill="'+soft+'" font-size="7">'+(g*4)+'</text>';
    }
    const bX=470,bY=45,bW=220,bH=220,lambda_m=2.0*(L_cm+2.45)/100.0,v_est=fHz*lambda_m;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">EXCITATION FREQUENCY (f₁)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+fHz.toFixed(1)+'</text><text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">Hz</text><text x="'+(bX+130)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">(Fundamental)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">RESONANT LENGTH (L)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="18" font-family="monospace">'+L_cm.toFixed(2)+' cm</text><text x="'+(bX+130)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">(±0.05 cm)</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">WAVELENGTH λ & SOUND VELOCITY v</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">'+v_est.toFixed(1)+' m s⁻¹</text><text x="'+(bX+135)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">(λ='+(lambda_m*100).toFixed(1)+' cm)</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">2c = 2(0.6133 r) = 2.45 cm · T = 20.0 °C</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'L = (v/2)(1/f₁) − 2c ⇔ v = 2m · 2c = −b',ink,9)+text(240,22,'Telescoping Open Organ Pipe Apparatus')+text(240,308,'Open-Open Standing Wave: λ/2 = L + 2c · Dual Rayleigh End Correction 2c = 1.2266 r');
  }
   else if(cfg.slug==='vibration-strings-sonometer'){
    const fHz=p.input;
    const L_cm=v.raw;
    const boxX=50,boxY=180,boxW=370,boxH=55;
    const bridge1X=85;
    const segL_px=80.0+(L_cm-15.0)*6.5;
    const bridge2X=bridge1X+segL_px;
    const wireY=boxY-12;
    svg+='<rect x="'+boxX+'" y="'+boxY+'" width="'+boxW+'" height="'+boxH+'" rx="4" fill="#78350f" stroke="#b45309" stroke-width="2"/><rect x="'+(boxX+4)+'" y="'+(boxY+4)+'" width="'+(boxW-8)+'" height="'+(boxH-8)+'" rx="3" fill="#92400e" opacity="0.6"/><ellipse cx="'+(boxX+50)+'" cy="'+(boxY+28)+'" rx="16" ry="6" fill="#1b2a26" stroke="#451a03" stroke-width="1.5"/><ellipse cx="'+(boxX+boxW-50)+'" cy="'+(boxY+28)+'" rx="16" ry="6" fill="#1b2a26" stroke="#451a03" stroke-width="1.5"/><circle cx="'+(boxX+15)+'" cy="'+wireY+'" r="4.5" fill="#94a3b8" stroke="#475569" stroke-width="1.5"/>';
    const pulleyX=boxX+boxW+12,pulleyY=wireY+4;
    svg+='<circle cx="'+pulleyX+'" cy="'+pulleyY+'" r="14" fill="#475569" stroke="#94a3b8" stroke-width="2"/><circle cx="'+pulleyX+'" cy="'+pulleyY+'" r="4" fill="#1e293b"/>';
    const massY=pulleyY+60;
    svg+='<line x1="'+(pulleyX+14)+'" y1="'+pulleyY+'" x2="'+(pulleyX+14)+'" y2="'+massY+'" stroke="#cbd5e1" stroke-width="1.5"/><rect x="'+(pulleyX+4)+'" y="'+massY+'" width="20" height="25" rx="3" fill="#d97706" stroke="#f59e0b" stroke-width="1.5"/><text x="'+(pulleyX+14)+'" y="'+(massY+16)+'" text-anchor="middle" fill="#fff" font-size="8" font-weight="bold">3 kg</text><text x="'+(pulleyX+14)+'" y="'+(massY+36)+'" text-anchor="middle" fill="'+soft+'" font-size="7.5">T=29.4N</text><polygon points="'+(bridge1X-8)+','+boxY+' '+bridge1X+','+(boxY-12)+' '+(bridge1X+8)+','+boxY+'" fill="#fde68a" stroke="#d97706" stroke-width="1.5"/><circle cx="'+bridge1X+'" cy="'+(boxY-12)+'" r="1.5" fill="#475569"/><polygon points="'+(bridge2X-8)+','+boxY+' '+bridge2X+','+(boxY-12)+' '+(bridge2X+8)+','+boxY+'" fill="#fde68a" stroke="#d97706" stroke-width="1.5"/><circle cx="'+bridge2X+'" cy="'+(boxY-12)+'" r="1.5" fill="#475569"/><line x1="'+(boxX+15)+'" y1="'+wireY+'" x2="'+bridge1X+'" y2="'+wireY+'" stroke="#cbd5e1" stroke-width="1.5"/><line x1="'+bridge2X+'" y1="'+wireY+'" x2="'+(pulleyX)+'" y2="'+wireY+'" stroke="#cbd5e1" stroke-width="1.5"/>';
    let wirePts=[];
    const midBridgeX=(bridge1X+bridge2X)/2.0,standingAmp=Math.cos(phase*16)*8.0;
    for(let s=0;s<=30;s++){
      const ns=s/30.0,wx=bridge1X+ns*(bridge2X-bridge1X),wy=wireY+Math.sin(Math.PI*ns)*standingAmp;
      wirePts.push(wx.toFixed(1)+','+wy.toFixed(1));
    }
    svg+='<polyline points="'+wirePts.join(' ')+'" fill="none" stroke="'+ink+'" stroke-width="2"/>';
    const riderY=wireY+standingAmp,isEjected=Math.abs(standingAmp)>6.0,riderOffY=isEjected?riderY-Math.abs(Math.sin(phase*20)*18)-6:riderY-5;
    svg+='<path d="M '+(midBridgeX-4)+' '+(riderOffY+6)+' L '+midBridgeX+' '+riderOffY+' L '+(midBridgeX+4)+' '+(riderOffY+6)+'" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round"/><text x="'+midBridgeX+'" y="'+(riderOffY-6)+'" text-anchor="middle" fill="#ef4444" font-size="7.5" font-weight="bold">'+(isEjected?'Rider Ejected!':'Paper Rider')+'</text>';
    const forkX=boxX+32,forkY=boxY-28;
    svg+='<rect x="'+(forkX-2)+'" y="'+(boxY-8)+'" width="4" height="8" rx="1" fill="#94a3b8"/><path d="M '+(forkX-7)+' '+(forkY-18)+' V '+forkY+' H '+(forkX+7)+' V '+(forkY-18)+'" fill="none" stroke="#e2e8f0" stroke-width="2.5" stroke-linecap="round"/><line x1="'+forkX+'" y1="'+forkY+'" x2="'+forkX+'" y2="'+(boxY-8)+'" stroke="#94a3b8" stroke-width="3"/><text x="'+forkX+'" y="'+(forkY-22)+'" text-anchor="middle" fill="'+orange+'" font-size="8" font-weight="bold">'+fHz.toFixed(1)+' Hz</text>';
    for(let r=1;r<=3;r++){
      const ripR=r*8+((phase*20)%10);
      svg+='<ellipse cx="'+(boxX+50)+'" cy="'+(boxY+10)+'" rx="'+ripR+'" ry="'+(ripR*0.45)+'" fill="none" stroke="'+orange+'" stroke-width="1" opacity="'+(1-r*0.28)+'"/>';
    }
    svg+='<line x1="'+bridge1X+'" y1="'+(boxY+boxH+12)+'" x2="'+bridge2X+'" y2="'+(boxY+boxH+12)+'" stroke="'+soft+'" stroke-width="1.5"/><line x1="'+bridge1X+'" y1="'+(boxY+boxH+6)+'" x2="'+bridge1X+'" y2="'+(boxY+boxH+18)+'" stroke="'+soft+'" stroke-width="1.5"/><line x1="'+bridge2X+'" y1="'+(boxY+boxH+6)+'" x2="'+bridge2X+'" y2="'+(boxY+boxH+18)+'" stroke="'+soft+'" stroke-width="1.5"/><text x="'+((bridge1X+bridge2X)/2)+'" y="'+(boxY+boxH+26)+'" text-anchor="middle" fill="'+soft+'" font-size="9" font-weight="bold">Resonant Length L = '+L_cm.toFixed(2)+' cm</text>';
    for(let g=0;g<=20;g++){
      const gx=boxX+20+g*(300/20),isMaj=(g%5===0);
      svg+='<line x1="'+gx+'" y1="'+boxY+'" x2="'+gx+'" y2="'+(boxY+(isMaj?6:3))+'" stroke="'+soft+'" stroke-width="'+(isMaj?1.2:0.8)+'"/>';
    }
    const bX=470,bY=45,bW=220,bH=220,lambda_m=2.0*L_cm/100.0,v_est=fHz*lambda_m,mu_est=29.41995/(v_est*v_est);
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">TUNING FORK FREQUENCY (f)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+fHz.toFixed(1)+'</text><text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">Hz</text><text x="'+(bX+130)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">(Middle Scale)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">RESONANT SEGMENT LENGTH (L)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="18" font-family="monospace">'+L_cm.toFixed(2)+' cm</text><text x="'+(bX+130)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">(±0.05 cm)</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">WAVE SPEED v & LINEAR DENSITY μ</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">'+v_est.toFixed(1)+' m s⁻¹</text><text x="'+(bX+130)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">μ='+(mu_est*1000).toFixed(3)+' g/m</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">T = M g = 29.42 N (M = 3.0 kg) · d = 0.50 mm</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'L = (v/2)(1/f) ⇔ v = 2m · μ = T / (4m²)',ink,9)+text(240,22,'Sonometer Soundboard Apparatus')+text(240,308,'Mersenne\'s Laws: f = (1/2L)√(T/μ) · Transverse Wave Speed v = 138.2 m s⁻¹');
  }
   else if(cfg.slug==='interference-sound-waves'){
    const L_cm=p.input;
    const d_cm=v.raw;
    const clampX=115,clampY=150;
    const rodL_px=110.0+(L_cm-80.0)*1.6;
    const rodLeftX=clampX-rodL_px/2.0;
    const rodRightX=clampX+rodL_px/2.0;
    const rodY=clampY-4,rodH=8;
    svg+='<rect x="85" y="240" width="60" height="15" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1.5"/><rect x="110" y="170" width="10" height="70" fill="#334155" stroke="'+soft+'" stroke-width="1"/><rect x="105" y="138" width="20" height="32" rx="2" fill="#475569" stroke="#94a3b8" stroke-width="1.5"/><circle cx="115" cy="154" r="3" fill="#f59e0b"/><text x="115" y="132" text-anchor="middle" fill="#f59e0b" font-size="7.5" font-weight="bold">Center Clamp (Node)</text><rect x="'+rodLeftX.toFixed(1)+'" y="'+rodY+'" width="'+(clampX-rodLeftX).toFixed(1)+'" height="'+rodH+'" rx="2" fill="#d97706" stroke="#b45309" stroke-width="1"/><rect x="'+clampX+'" y="'+rodY+'" width="'+(rodRightX-clampX).toFixed(1)+'" height="'+rodH+'" rx="2" fill="#d97706" stroke="#b45309" stroke-width="1"/>';
    const discX=rodRightX,discVib=Math.cos(phase*18)*2.5;
    svg+='<rect x="'+(discX-2+discVib).toFixed(1)+'" y="'+(rodY-6)+'" width="6" height="20" rx="1.5" fill="#78350f" stroke="#b45309" stroke-width="1.2"/><text x="'+discX.toFixed(1)+'" y="'+(rodY-10)+'" text-anchor="middle" fill="#fde68a" font-size="7">Cork Disc</text>';
    let rodWaveTop=[],rodWaveBot=[];
    for(let w=0;w<=20;w++){
      const nw=w/20.0,wx=rodLeftX+nw*rodL_px,disp=Math.sin((nw-0.5)*Math.PI)*Math.cos(phase*18)*5.0;
      rodWaveTop.push(wx.toFixed(1)+','+(rodY-2-disp).toFixed(1));rodWaveBot.push(wx.toFixed(1)+','+(rodY+rodH+2+disp).toFixed(1));
    }
    svg+='<polyline points="'+rodWaveTop.join(' ')+'" fill="none" stroke="'+orange+'" stroke-width="1.2" stroke-dasharray="2 2"/><polyline points="'+rodWaveBot.join(' ')+'" fill="none" stroke="'+orange+'" stroke-width="1.2" stroke-dasharray="2 2"/><line x1="'+rodLeftX.toFixed(1)+'" y1="'+(rodY+22)+'" x2="'+rodRightX.toFixed(1)+'" y2="'+(rodY+22)+'" stroke="'+soft+'" stroke-width="1.2"/><line x1="'+rodLeftX.toFixed(1)+'" y1="'+(rodY+17)+'" x2="'+rodLeftX.toFixed(1)+'" y2="'+(rodY+27)+'" stroke="'+soft+'" stroke-width="1.2"/><line x1="'+rodRightX.toFixed(1)+'" y1="'+(rodY+17)+'" x2="'+rodRightX.toFixed(1)+'" y2="'+(rodY+27)+'" stroke="'+soft+'" stroke-width="1.2"/><text x="'+((rodLeftX+rodRightX)/2).toFixed(1)+'" y="'+(rodY+34)+'" text-anchor="middle" fill="'+soft+'" font-size="8.5" font-weight="bold">L_rod = '+L_cm.toFixed(1)+' cm</text>';
    const clothX=clampX-rodL_px*0.3;
    svg+='<rect x="'+(clothX-8)+'" y="'+(rodY-8)+'" width="16" height="24" rx="3" fill="#b91c1c" stroke="#fca5a5" stroke-width="1" opacity="0.85"/><path d="M '+(clothX-14)+' '+(rodY+4)+' L '+(clothX-22)+' '+(rodY+4)+' M '+(clothX-18)+' '+(rodY+1)+' L '+(clothX-22)+' '+(rodY+4)+' L '+(clothX-18)+' '+(rodY+7)+'" stroke="#fca5a5" stroke-width="1.5" stroke-linecap="round"/><text x="'+clothX+'" y="'+(rodY-11)+'" text-anchor="middle" fill="#fca5a5" font-size="6.5">Rosin Stroke</text>';
    const tubeX=discX-10,tubeW=450-tubeX,tubeY=clampY-18,tubeH=36;
    svg+='<polygon points="'+(tubeX+40)+',240 '+(tubeX+50)+',180 '+(tubeX+60)+',240" fill="#20312d" stroke="'+soft+'" stroke-width="1.2"/><polygon points="'+(tubeX+tubeW-40)+',240 '+(tubeX+tubeW-30)+',180 '+(tubeX+tubeW-20)+',240" fill="#20312d" stroke="'+soft+'" stroke-width="1.2"/><rect x="'+tubeX+'" y="'+tubeY+'" width="'+tubeW+'" height="'+tubeH+'" rx="3" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5" opacity="0.85"/><line x1="'+tubeX+'" y1="'+(tubeY+3)+'" x2="'+(tubeX+tubeW)+'" y2="'+(tubeY+3)+'" stroke="#bae6fd" stroke-width="0.8" opacity="0.6"/>';
    const pistonX=tubeX+tubeW-12;
    svg+='<rect x="'+pistonX+'" y="'+(tubeY+2)+'" width="8" height="'+(tubeH-4)+'" rx="1" fill="#475569" stroke="#94a3b8" stroke-width="1.2"/><line x1="'+(pistonX+8)+'" y1="'+(tubeY+tubeH/2)+'" x2="'+(pistonX+32)+'" y2="'+(tubeY+tubeH/2)+'" stroke="#cbd5e1" stroke-width="3"/><rect x="'+(pistonX+30)+'" y="'+(tubeY+tubeH/2-8)+'" width="4" height="16" rx="1" fill="#94a3b8"/><text x="'+(pistonX+16)+'" y="'+(tubeY-6)+'" text-anchor="middle" fill="#94a3b8" font-size="7">Tuning Piston</text>';
    const d_px=18.0+(d_cm-7.84)*3.5,startHeapX=tubeX+22,numHeaps=Math.floor((pistonX-startHeapX-10)/d_px);
    let waveAir=[];
    for(let px_i=0;px_i<=60;px_i++){
      const curX=startHeapX+(px_i/60.0)*(numHeaps*d_px),normX=(curX-startHeapX)/d_px,uAir=Math.sin(Math.PI*normX)*Math.cos(phase*18)*9.0;
      waveAir.push(curX.toFixed(1)+','+(tubeY+tubeH/2-uAir).toFixed(1));
    }
    svg+='<polyline points="'+waveAir.join(' ')+'" fill="none" stroke="'+ink+'" stroke-width="1.5" stroke-dasharray="2 2"/>';
    for(let h=0;h<=numHeaps;h++){
      const hX=startHeapX+h*d_px;
      if(hX<pistonX-10){
        svg+='<polygon points="'+(hX-5)+','+(tubeY+tubeH-2)+' '+hX+','+(tubeY+tubeH-9)+' '+(hX+5)+','+(tubeY+tubeH-2)+'" fill="#fde68a" stroke="#d97706" stroke-width="0.8"/><circle cx="'+hX+'" cy="'+(tubeY+tubeH-2)+'" r="1" fill="#d97706"/>';
        if(h<numHeaps){
          const antiX=hX+d_px/2.0;
          for(let s=-2;s<=2;s++){
            const stX=antiX+s*2.5,agitate=Math.abs(Math.sin(phase*18+s))*4.0;
            svg+='<line x1="'+stX.toFixed(1)+'" y1="'+(tubeY+tubeH-2)+'" x2="'+stX.toFixed(1)+'" y2="'+(tubeY+tubeH-4-agitate).toFixed(1)+'" stroke="#cbd5e1" stroke-width="1" stroke-linecap="round"/>';
          }
        }
      }
    }
    if(numHeaps>=1){
      const h1=startHeapX,h2=startHeapX+d_px;
      svg+='<line x1="'+h1+'" y1="'+(tubeY+tubeH+12)+'" x2="'+h2.toFixed(1)+'" y2="'+(tubeY+tubeH+12)+'" stroke="'+orange+'" stroke-width="1.2"/><line x1="'+h1+'" y1="'+(tubeY+tubeH+8)+'" x2="'+h1+'" y2="'+(tubeY+tubeH+16)+'" stroke="'+orange+'" stroke-width="1.2"/><line x1="'+h2.toFixed(1)+'" y1="'+(tubeY+tubeH+8)+'" x2="'+h2.toFixed(1)+'" y2="'+(tubeY+tubeH+16)+'" stroke="'+orange+'" stroke-width="1.2"/><text x="'+((h1+h2)/2).toFixed(1)+'" y="'+(tubeY+tubeH+24)+'" text-anchor="middle" fill="'+orange+'" font-size="8" font-weight="bold">d = '+d_cm.toFixed(2)+' cm (λ_air/2)</text>';
    }
    svg+='<rect x="'+tubeX+'" y="240" width="'+tubeW+'" height="10" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1"/>';
    for(let g=0;g<=16;g++){
      const gx=tubeX+10+g*((tubeW-20)/16),isMaj=(g%4===0);
      svg+='<line x1="'+gx.toFixed(1)+'" y1="240" x2="'+gx.toFixed(1)+'" y2="'+(240+(isMaj?6:3))+'" stroke="'+soft+'" stroke-width="'+(isMaj?1.2:0.8)+'"/>';
    }
    const bX=470,bY=45,bW=220,bH=220,lambda_air_m=2.0*d_cm/100.0,f_sound=343.20/lambda_air_m,v_rod_est=343.20*((L_cm/100.0)/(d_cm/100.0)),E_gpa=8500.0*(v_rod_est*v_rod_est)*1e-9;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/><text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">SOUNDING ROD LENGTH (L_rod)</text><text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+L_cm.toFixed(1)+'</text><text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">cm</text><text x="'+(bX+130)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">(Center Clamped)</text><line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">NODAL DUST SPACING (d = λ_air / 2)</text><text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="18" font-family="monospace">'+d_cm.toFixed(2)+' cm</text><text x="'+(bX+130)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">(±0.05 cm)</text><line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/><text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">ROD SOUND SPEED & YOUNG MODULUS</text><text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">'+v_rod_est.toFixed(1)+' m s⁻¹</text><text x="'+(bX+130)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">E='+E_gpa.toFixed(1)+' GPa</text><text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">f = '+f_sound.toFixed(1)+' Hz · v_air = 343.2 m/s · ρ = 8500 kg/m³</text><line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>'+text(bX+15,bY+210,'d = (v_air / v_rod) L ⇔ v_rod = v_air / m',ink,9)+text(240,22,'Kundt\'s Tube Acoustic Standing Wave Apparatus')+text(240,308,'Standing Waves in Air: d = λ_air / 2 · Rod Sound Speed: v_rod = 3500.0 m s⁻¹');
  }
   else if(cfg.slug==='electrostatics'){
    const r_cm=p.input;
    const F_uN=v.raw;
    // Grounded base table
    svg+='<rect x="50" y="250" width="390" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/>';
    // Cylindrical glass chamber of torsion balance
    const chX=70,chY=95,chW=235,chH=155;
    svg+='<rect x="'+chX+'" y="'+chY+'" width="'+chW+'" height="'+chH+'" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5" opacity="0.85"/>';
    svg+='<line x1="'+chX+'" y1="'+(chY+4)+'" x2="'+(chX+chW)+'" y2="'+(chY+4)+'" stroke="#bae6fd" stroke-width="0.8" opacity="0.5"/>';
    // Central vertical glass suspension tube
    svg+='<rect x="180" y="32" width="16" height="65" rx="2" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>';
    // Top torsion head
    svg+='<rect x="172" y="16" width="32" height="16" rx="3" fill="#d97706" stroke="#b45309" stroke-width="1.5"/>';
    svg+='<circle cx="188" cy="24" r="5" fill="#fde68a" stroke="#d97706" stroke-width="1"/>';
    svg+='<line x1="188" y1="24" x2="198" y2="20" stroke="#b91c1c" stroke-width="1.5"/>';
    svg+='<text x="188" y="12" text-anchor="middle" fill="#fde68a" font-size="7" font-weight="bold">Torsion Head (θ)</text>';
    // Torsion fiber
    svg+='<line x1="188" y1="32" x2="188" y2="165" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3 1"/>';
    // Horizontal insulating balance beam (length 110 px)
    const beamY=165;
    svg+='<rect x="133" y="'+(beamY-2)+'" width="110" height="4" rx="1.5" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>';
    // Sphere A (suspended on left end of beam)
    const spAX=133;
    svg+='<circle cx="'+spAX+'" cy="'+beamY+'" r="9" fill="#d97706" stroke="#f59e0b" stroke-width="1.5"/>';
    svg+='<text x="'+spAX+'" y="'+(beamY+3.5)+'" text-anchor="middle" fill="#fff" font-size="7.5" font-weight="bold">+q₁</text>';
    svg+='<text x="'+spAX+'" y="'+(beamY-12)+'" text-anchor="middle" fill="#fde68a" font-size="7">Sphere A</text>';
    // Counterweight and damping vane on right end
    svg+='<rect x="238" y="'+(beamY-7)+'" width="10" height="14" rx="2" fill="#475569" stroke="#94a3b8" stroke-width="1"/>';
    // Sliding carrier entering from left
    const r_px=22.0+(r_cm-3.0)*8.5;
    const spBX=spAX-r_px;
    svg+='<line x1="50" y1="'+beamY+'" x2="'+(spBX-2)+'" y2="'+beamY+'" stroke="#cbd5e1" stroke-width="2.5"/>';
    svg+='<circle cx="'+spBX.toFixed(1)+'" cy="'+beamY+'" r="9" fill="#d97706" stroke="#f59e0b" stroke-width="1.5"/>';
    svg+='<text x="'+spBX.toFixed(1)+'" y="'+(beamY+3.5)+'" text-anchor="middle" fill="#fff" font-size="7.5" font-weight="bold">+q₂</text>';
    svg+='<text x="'+spBX.toFixed(1)+'" y="'+(beamY-12)+'" text-anchor="middle" fill="#fde68a" font-size="7">Sphere B</text>';
    // Carrier vernier guide on bench
    svg+='<rect x="45" y="244" width="60" height="6" rx="1" fill="#475569"/>';
    // Repulsive vector arrows on spheres
    const fVecLen=Math.min(28,Math.max(8,(F_uN/120.0)));
    // Force on A pointing right
    svg+='<path d="M '+(spAX+11)+' '+beamY+' L '+(spAX+11+fVecLen).toFixed(1)+' '+beamY+' M '+(spAX+7+fVecLen).toFixed(1)+' '+(beamY-3)+' L '+(spAX+11+fVecLen).toFixed(1)+' '+beamY+' L '+(spAX+7+fVecLen).toFixed(1)+' '+(beamY+3)+'" stroke="#ef4444" stroke-width="2" stroke-linecap="round"/>';
    svg+='<text x="'+(spAX+14+fVecLen).toFixed(1)+'" y="'+(beamY-5)+'" fill="#ef4444" font-size="7" font-weight="bold">F⃗_e</text>';
    // Force on B pointing left
    svg+='<path d="M '+(spBX-11).toFixed(1)+' '+beamY+' L '+(spBX-11-fVecLen).toFixed(1)+' '+beamY+' M '+(spBX-7-fVecLen).toFixed(1)+' '+(beamY-3)+' L '+(spBX-11-fVecLen).toFixed(1)+' '+beamY+' L '+(spBX-7-fVecLen).toFixed(1)+' '+(beamY+3)+'" stroke="#ef4444" stroke-width="2" stroke-linecap="round"/>';
    svg+='<text x="'+(spBX-14-fVecLen).toFixed(1)+'" y="'+(beamY-5)+'" text-anchor="end" fill="#ef4444" font-size="7" font-weight="bold">F⃗_e</text>';
    // Distance dimension line
    svg+='<line x1="'+spBX.toFixed(1)+'" y1="'+(beamY+22)+'" x2="'+spAX+'" y2="'+(beamY+22)+'" stroke="'+orange+'" stroke-width="1.2"/>';
    svg+='<line x1="'+spBX.toFixed(1)+'" y1="'+(beamY+18)+'" x2="'+spBX.toFixed(1)+'" y2="'+(beamY+26)+'" stroke="'+orange+'" stroke-width="1.2"/>';
    svg+='<line x1="'+spAX+'" y1="'+(beamY+18)+'" x2="'+spAX+'" y2="'+(beamY+26)+'" stroke="'+orange+'" stroke-width="1.2"/>';
    svg+='<text x="'+((spBX+spAX)/2).toFixed(1)+'" y="'+(beamY+34)+'" text-anchor="middle" fill="'+orange+'" font-size="8.5" font-weight="bold">r = '+r_cm.toFixed(1)+' cm</text>';
    // Degree graduation ring inside chamber
    for(let deg=0;deg<=20;deg++){
      const gx=chX+15+deg*((chW-30)/20);
      svg+='<line x1="'+gx+'" y1="'+(chY+chH-10)+'" x2="'+gx+'" y2="'+(chY+chH-(deg%5===0?18:14))+'" stroke="'+soft+'" stroke-width="'+(deg%5===0?1.2:0.8)+'"/>';
    }
    // Side Bench Accessories: Gold-Leaf Electroscope & Proof Plane
    const elX=350,elY=175;
    svg+='<rect x="'+(elX-18)+'" y="'+elY+'" width="36" height="50" rx="4" fill="#0f172a" stroke="#cbd5e1" stroke-width="1.2"/>';
    svg+='<line x1="'+elX+'" y1="'+(elY-12)+'" x2="'+elX+'" y2="'+(elY+18)+'" stroke="#d97706" stroke-width="2"/>';
    svg+='<circle cx="'+elX+'" cy="'+(elY-14)+'" r="10" fill="#d97706" stroke="#b45309" stroke-width="1"/>';
    // Divergent gold leaves
    svg+='<line x1="'+elX+'" y1="'+(elY+18)+'" x2="'+(elX-8)+'" y2="'+(elY+38)+'" stroke="#fde68a" stroke-width="1.8"/>';
    svg+='<line x1="'+elX+'" y1="'+(elY+18)+'" x2="'+(elX+8)+'" y2="'+(elY+38)+'" stroke="#fde68a" stroke-width="1.8"/>';
    svg+='<text x="'+elX+'" y="'+(elY+62)+'" text-anchor="middle" fill="#fde68a" font-size="7">Electroscope</text>';
    // Proof plane
    const prX=415,prY=185;
    svg+='<line x1="'+prX+'" y1="'+(prY+30)+'" x2="'+prX+'" y2="'+prY+'" stroke="#78350f" stroke-width="2.5"/>';
    svg+='<circle cx="'+prX+'" cy="'+(prY-4)+'" r="6" fill="#94a3b8" stroke="#cbd5e1" stroke-width="1"/>';
    svg+='<text x="'+prX+'" y="'+(prY+45)+'" text-anchor="middle" fill="#94a3b8" font-size="7">Proof Plane</text>';
    // HUD Card at x=470, y=45, w=220, h=220
    const bX=470,bY=45,bW=220,bH=220;
    const inv_r2_m2=1.0/Math.pow(r_cm/100.0,2);
    const k_est=8.98755e9;
    const eps0_est=1.0/(4.0*Math.PI*k_est);
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">SEPARATION DISTANCE (r)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+r_cm.toFixed(1)+'</text>';
    svg+='<text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">cm</text>';
    svg+='<text x="'+(bX+130)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">(Center-to-Center)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">COULOMB REPULSIVE FORCE (F)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="18" font-family="monospace">'+F_uN.toFixed(2)+' μN</text>';
    svg+='<text x="'+(bX+130)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">(1/r² = '+inv_r2_m2.toFixed(1)+' m⁻²)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">COULOMB CONSTANT & PERMITTIVITY</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">8.988 × 10⁹</text>';
    svg+='<text x="'+(bX+130)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">N m² C⁻²</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">q₁ = q₂ = 20.0 nC · ε₀ = 8.854 × 10⁻¹² F m⁻¹</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>';
    svg+=text(bX+15,bY+210,'F = k_e q² (1/r²) ⇔ k_e = m / q²',ink,9);
    svg+=text(240,22,'Coulomb\'s Torsion Balance Electrostatic Apparatus');
    svg+=text(240,308,'Coulomb\'s Law: F = k_e (q₁ q₂ / r²) · Permittivity ε₀ = 8.854 × 10⁻¹² F m⁻¹');
  }
  else if(cfg.slug==='magnetic-fields'){
    const I_mA=p.input;
    const theta_deg=v.raw;
    const tan_theta=v.y;
    // Bench table
    svg+='<rect x="50" y="250" width="390" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/>';
    // Tangent Galvanometer Wooden Base & Leveling Tripod Screws
    const bseX=110,bseY=230,bseW=190,bseH=20;
    svg+='<rect x="'+bseX+'" y="'+bseY+'" width="'+bseW+'" height="'+bseH+'" rx="4" fill="#78350f" stroke="#451a03" stroke-width="2"/>';
    // Brass Leveling Screws
    svg+='<rect x="125" y="248" width="14" height="6" rx="1" fill="#d97706" stroke="#b45309" stroke-width="1"/>';
    svg+='<rect x="270" y="248" width="14" height="6" rx="1" fill="#d97706" stroke="#b45309" stroke-width="1"/>';
    // Vertical Brass Pillar
    svg+='<rect x="198" y="175" width="14" height="55" rx="2" fill="#d97706" stroke="#b45309" stroke-width="1.5"/>';
    // Galvanometer Circular Wooden Ring Frame (N = 50 turns copper coil)
    const coilX=205,coilY=115,coilR=72;
    svg+='<circle cx="'+coilX+'" cy="'+coilY+'" r="'+coilR+'" fill="none" stroke="#78350f" stroke-width="12"/>';
    svg+='<circle cx="'+coilX+'" cy="'+coilY+'" r="'+coilR+'" fill="none" stroke="#b45309" stroke-width="8"/>';
    svg+='<circle cx="'+coilX+'" cy="'+coilY+'" r="'+(coilR+4)+'" fill="none" stroke="#f59e0b" stroke-width="1" stroke-dasharray="2 2"/>';
    svg+='<circle cx="'+coilX+'" cy="'+coilY+'" r="'+(coilR-4)+'" fill="none" stroke="#f59e0b" stroke-width="1" stroke-dasharray="2 2"/>';
    svg+='<text x="'+coilX+'" y="32" text-anchor="middle" fill="#fde68a" font-size="8.5" font-weight="bold">50-Turn Vertical Circular Coil (R = 10.0 cm)</text>';
    // Central Compass Box with Glass Face and Mirror Ring
    const compR=38;
    svg+='<circle cx="'+coilX+'" cy="'+coilY+'" r="'+compR+'" fill="#0f172a" stroke="#cbd5e1" stroke-width="2"/>';
    // Anti-parallax mirror ring
    svg+='<circle cx="'+coilX+'" cy="'+coilY+'" r="'+(compR-10)+'" fill="none" stroke="#38bdf8" stroke-width="2.5" opacity="0.7"/>';
    // Protractor degree graduation marks (every 15° and 45°)
    for(let a=0;a<24;a++){
      const ang=(a/24)*2*Math.PI;
      const r1=compR-4,r2=compR-(a%6===0?9:6);
      const x1=coilX+Math.cos(ang)*r1,y1=coilY+Math.sin(ang)*r1;
      const x2=coilX+Math.cos(ang)*r2,y2=coilY+Math.sin(ang)*r2;
      svg+='<line x1="'+x1.toFixed(1)+'" y1="'+y1.toFixed(1)+'" x2="'+x2.toFixed(1)+'" y2="'+y2.toFixed(1)+'" stroke="'+(a%6===0?'#fde68a':'#64748b')+'" stroke-width="'+(a%6===0?1.5:0.8)+'"/>';
    }
    // Cardinal labels: N, S, E, W
    svg+='<text x="'+coilX+'" y="'+(coilY-compR+12)+'" text-anchor="middle" fill="#22c55e" font-size="7" font-weight="bold">N (0°)</text>';
    svg+='<text x="'+coilX+'" y="'+(coilY+compR-6)+'" text-anchor="middle" fill="#22c55e" font-size="7" font-weight="bold">S (0°)</text>';
    svg+='<text x="'+(coilX+compR-10)+'" y="'+(coilY+3)+'" text-anchor="middle" fill="#ef4444" font-size="6.5" font-weight="bold">90°</text>';
    svg+='<text x="'+(coilX-compR+10)+'" y="'+(coilY+3)+'" text-anchor="middle" fill="#ef4444" font-size="6.5" font-weight="bold">90°</text>';

    // Magnetic Needle & Aluminum Pointer Pivot Calculation
    const theta_rad=(theta_deg*Math.PI)/180.0;
    // Compass Needle (points along resultant field: theta away from North)
    const ndlLen=16;
    const nX1=coilX-Math.sin(theta_rad)*ndlLen,nY1=coilY-Math.cos(theta_rad)*ndlLen;
    const nX2=coilX+Math.sin(theta_rad)*ndlLen,nY2=coilY+Math.cos(theta_rad)*ndlLen;
    // Needle body: North tip (red), South tip (blue)
    svg+='<line x1="'+coilX+'" y1="'+coilY+'" x2="'+nX1.toFixed(1)+'" y2="'+nY1.toFixed(1)+'" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round"/>';
    svg+='<line x1="'+coilX+'" y1="'+coilY+'" x2="'+nX2.toFixed(1)+'" y2="'+nY2.toFixed(1)+'" stroke="#3b82f6" stroke-width="2.5" stroke-linecap="round"/>';
    // Aluminum Pointer (orthogonal to magnetic needle: length 32px each side)
    const ptrLen=32;
    const pX1=coilX-Math.cos(theta_rad)*ptrLen,pY1=coilY+Math.sin(theta_rad)*ptrLen;
    const pX2=coilX+Math.cos(theta_rad)*ptrLen,pY2=coilY-Math.sin(theta_rad)*ptrLen;
    svg+='<line x1="'+pX1.toFixed(1)+'" y1="'+pY1.toFixed(1)+'" x2="'+pX2.toFixed(1)+'" y2="'+pY2.toFixed(1)+'" stroke="#f8fafc" stroke-width="1.2"/>';
    svg+='<circle cx="'+pX1.toFixed(1)+'" cy="'+pY1.toFixed(1)+'" r="1.5" fill="#ef4444"/>';
    svg+='<circle cx="'+pX2.toFixed(1)+'" cy="'+pY2.toFixed(1)+'" r="1.5" fill="#ef4444"/>';
    // Central Agate Jewel Pivot
    svg+='<circle cx="'+coilX+'" cy="'+coilY+'" r="3.5" fill="#d97706" stroke="#fff" stroke-width="1"/>';

    // Deflection readout angle arc
    svg+='<text x="'+(coilX+compR+12)+'" y="'+(coilY-14)+'" fill="'+orange+'" font-size="9" font-weight="bold">θ = '+theta_deg.toFixed(2)+'°</text>';
    svg+='<text x="'+(coilX+compR+12)+'" y="'+(coilY-2)+'" fill="'+soft+'" font-size="8">tan θ = '+tan_theta.toFixed(4)+'</text>';

    // Bench Accessories: DC Power Supply & Reversing Pohl Commutator
    // DC Supply
    const psX=320,psY=165;
    svg+='<rect x="'+psX+'" y="'+psY+'" width="48" height="38" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1.2"/>';
    svg+='<rect x="'+(psX+6)+'" y="'+(psY+6)+'" width="36" height="12" rx="1" fill="#020617"/>';
    svg+='<text x="'+(psX+24)+'" y="'+(psY+15)+'" text-anchor="middle" fill="#22c55e" font-size="7" font-family="monospace">'+(I_mA*0.042).toFixed(1)+' V</text>';
    svg+='<circle cx="'+(psX+14)+'" cy="'+(psY+28)+'" r="3" fill="#ef4444"/>';
    svg+='<circle cx="'+(psX+34)+'" cy="'+(psY+28)+'" r="3" fill="#0f172a" stroke="#64748b" stroke-width="1"/>';
    svg+='<text x="'+(psX+24)+'" y="'+(psY+48)+'" text-anchor="middle" fill="#9fb498" font-size="7">DC Supply</text>';

    // Pohl Commutator
    const comX=390,comY=170;
    svg+='<rect x="'+comX+'" y="'+comY+'" width="38" height="32" rx="3" fill="#78350f" stroke="#451a03" stroke-width="1.5"/>';
    svg+='<circle cx="'+(comX+9)+'" cy="'+(comY+9)+'" r="2.5" fill="#d97706"/>';
    svg+='<circle cx="'+(comX+29)+'" cy="'+(comY+9)+'" r="2.5" fill="#d97706"/>';
    svg+='<circle cx="'+(comX+9)+'" cy="'+(comY+23)+'" r="2.5" fill="#d97706"/>';
    svg+='<circle cx="'+(comX+29)+'" cy="'+(comY+23)+'" r="2.5" fill="#d97706"/>';
    // Rocker cross-bars
    svg+='<line x1="'+(comX+9)+'" y1="'+(comY+9)+'" x2="'+(comX+29)+'" y2="'+(comY+23)+'" stroke="#cbd5e1" stroke-width="1.5"/>';
    svg+='<text x="'+(comX+19)+'" y="'+(comY+44)+'" text-anchor="middle" fill="#fde68a" font-size="7">Commutator</text>';

    // Connecting wires
    svg+='<path d="M '+(psX+14)+' '+(psY+31)+' Q '+(psX-15)+' 220 '+(coilX-10)+' 205" fill="none" stroke="#ef4444" stroke-width="1.2"/>';
    svg+='<path d="M '+(psX+34)+' '+(psY+31)+' Q '+(comX-10)+' 215 '+(comX+9)+' '+(comY+23)+'" fill="none" stroke="#3b82f6" stroke-width="1.2"/>';

    // HUD Card at x=470, y=45, w=220, h=220
    const bX=470,bY=45,bW=220,bH=220;
    const G_const=3.14159265e-4;
    const BH_uT=35.00;
    const K_mA=111.4;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">COIL DIRECT CURRENT (I)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+I_mA.toFixed(1)+'</text>';
    svg+='<text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">mA</text>';
    svg+='<text x="'+(bX+130)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">(±0.1 mA)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">COMPASS DEFLECTION (θ)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="18" font-family="monospace">'+theta_deg.toFixed(2)+'°</text>';
    svg+='<text x="'+(bX+125)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">(tan θ = '+tan_theta.toFixed(4)+')</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">EARTH HORIZONTAL FIELD & REDUCTION</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">'+BH_uT.toFixed(2)+' μT</text>';
    svg+='<text x="'+(bX+125)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">K = '+K_mA.toFixed(1)+' mA</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">G = μ₀ N / (2R) = 3.1416 × 10⁻⁴ T A⁻¹ · N = 50</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>';
    svg+=text(bX+15,bY+210,'tan θ = (G / B_H) I ⇔ B_H = G / m',ink,9);
    svg+=text(240,22,'Stewart & Gee Tangent Galvanometer Bench');
    svg+=text(240,308,'Tangent Law: B_coil = B_H tan θ · Coil Field: B_coil = μ₀ N I / (2R)');
  }
  else if(cfg.slug==='electric-fields'){
    const x_cm=p.input;
    const V_meas=v.raw;
    // Bench table
    svg+='<rect x="50" y="250" width="390" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/>';
    // Teledeltos Mapping Board (wood/acrylic backing)
    const bdX=70,bdY=45,bdW=320,bdH=195;
    svg+='<rect x="'+bdX+'" y="'+bdY+'" width="'+bdW+'" height="'+bdH+'" rx="5" fill="#1e293b" stroke="#334155" stroke-width="2"/>';
    // Carbon-impregnated Teledeltos Paper Sheet
    const ppX=bdX+15,ppY=bdY+15,ppW=bdW-30,ppH=bdH-30;
    svg+='<rect x="'+ppX+'" y="'+ppY+'" width="'+ppW+'" height="'+ppH+'" fill="#090d16" stroke="#475569" stroke-width="1.2"/>';
    // Grid overlay (10mm spacing)
    for(let gx=0;gx<=10;gx++){
      const lx=ppX+15+gx*((ppW-30)/10);
      svg+='<line x1="'+lx.toFixed(1)+'" y1="'+ppY+'" x2="'+lx.toFixed(1)+'" y2="'+(ppY+ppH)+'" stroke="#334155" stroke-width="0.5" stroke-dasharray="1 3"/>';
    }
    for(let gy=0;gy<=6;gy++){
      const ly=ppY+10+gy*((ppH-20)/6);
      svg+='<line x1="'+ppX+'" y1="'+ly.toFixed(1)+'" x2="'+(ppX+ppW)+'" y2="'+ly.toFixed(1)+'" stroke="#334155" stroke-width="0.5" stroke-dasharray="1 3"/>';
    }
    // Left Ground Electrode (x = 0 cm, V = 0.00 V)
    const el1X=ppX+15;
    svg+='<rect x="'+(el1X-4)+'" y="'+(ppY+10)+'" width="8" height="'+(ppH-20)+'" rx="1" fill="#d97706" stroke="#b45309" stroke-width="1.5"/>';
    svg+='<line x1="'+el1X+'" y1="'+(ppY+10)+'" x2="'+el1X+'" y2="'+(ppY+ppH-10)+'" stroke="#cbd5e1" stroke-width="1"/>';
    svg+='<text x="'+el1X+'" y="'+(ppY+ppH-2)+'" text-anchor="middle" fill="#93c5fd" font-size="7" font-weight="bold">Ground (0V)</text>';
    // Right Positive Electrode (x = 10 cm, V = 10.00 V)
    const el2X=ppX+ppW-15;
    svg+='<rect x="'+(el2X-4)+'" y="'+(ppY+10)+'" width="8" height="'+(ppH-20)+'" rx="1" fill="#d97706" stroke="#b45309" stroke-width="1.5"/>';
    svg+='<line x1="'+el2X+'" y1="'+(ppY+10)+'" x2="'+el2X+'" y2="'+(ppY+ppH-10)+'" stroke="#cbd5e1" stroke-width="1"/>';
    svg+='<text x="'+el2X+'" y="'+(ppY+ppH-2)+'" text-anchor="middle" fill="#fca5a5" font-size="7" font-weight="bold">+10.00V</text>';
    // Equipotential Lines (at 2V, 4V, 6V, 8V)
    for(let eq=1;eq<=4;eq++){
      const eqX=el1X+eq*((el2X-el1X)/5);
      svg+='<line x1="'+eqX.toFixed(1)+'" y1="'+(ppY+10)+'" x2="'+eqX.toFixed(1)+'" y2="'+(ppY+ppH-10)+'" stroke="#06b6d4" stroke-width="1.2" stroke-dasharray="3 2" opacity="0.75"/>';
      svg+='<text x="'+eqX.toFixed(1)+'" y="'+(ppY+8)+'" text-anchor="middle" fill="#06b6d4" font-size="6.5">'+(eq*2)+'V</text>';
    }
    // Current Probe Location at displacement x
    const probeX_px=el1X+(x_cm/10.0)*(el2X-el1X);
    const probeY_px=ppY+ppH/2;
    // Probe stylus
    svg+='<line x1="'+probeX_px.toFixed(1)+'" y1="'+(probeY_px-38)+'" x2="'+probeX_px.toFixed(1)+'" y2="'+probeY_px+'" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/>';
    svg+='<circle cx="'+probeX_px.toFixed(1)+'" cy="'+probeY_px+'" r="3.5" fill="#ef4444" stroke="#fff" stroke-width="1"/>';
    svg+='<line x1="'+probeX_px.toFixed(1)+'" y1="'+(probeY_px-38)+'" x2="'+(probeX_px-15)+'" y2="'+(probeY_px-60)+'" stroke="#3b82f6" stroke-width="1.5"/>';
    svg+='<text x="'+probeX_px.toFixed(1)+'" y="'+(probeY_px-44)+'" text-anchor="middle" fill="#fde68a" font-size="7.5" font-weight="bold">Probe Stylus</text>';
    // Probe readout badge on sheet
    svg+='<rect x="'+(probeX_px-22).toFixed(1)+'" y="'+(probeY_px+8)+'" width="44" height="14" rx="2" fill="#020617" stroke="'+orange+'" stroke-width="1"/>';
    svg+='<text x="'+probeX_px.toFixed(1)+'" y="'+(probeY_px+18)+'" text-anchor="middle" fill="'+orange+'" font-size="7.5" font-family="monospace" font-weight="bold">'+V_meas.toFixed(2)+' V</text>';
    // Dimension line along central axis
    svg+='<line x1="'+el1X+'" y1="'+(ppY+ppH+14)+'" x2="'+probeX_px.toFixed(1)+'" y2="'+(ppY+ppH+14)+'" stroke="'+orange+'" stroke-width="1.2"/>';
    svg+='<line x1="'+el1X+'" y1="'+(ppY+ppH+10)+'" x2="'+el1X+'" y2="'+(ppY+ppH+18)+'" stroke="'+orange+'" stroke-width="1.2"/>';
    svg+='<line x1="'+probeX_px.toFixed(1)+'" y1="'+(ppY+ppH+10)+'" x2="'+probeX_px.toFixed(1)+'" y2="'+(ppY+ppH+18)+'" stroke="'+orange+'" stroke-width="1.2"/>';
    svg+='<text x="'+((el1X+probeX_px)/2).toFixed(1)+'" y="'+(ppY+ppH+24)+'" text-anchor="middle" fill="'+orange+'" font-size="8" font-weight="bold">x = '+x_cm.toFixed(1)+' cm</text>';

    // Bench Accessories: DC Power Supply & High-Z Digital Voltmeter
    const psX=400,psY=165;
    svg+='<rect x="'+psX+'" y="'+psY+'" width="45" height="36" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1.2"/>';
    svg+='<rect x="'+(psX+5)+'" y="'+(psY+5)+'" width="35" height="12" rx="1" fill="#020617"/>';
    svg+='<text x="'+(psX+22)+'" y="'+(psY+14)+'" text-anchor="middle" fill="#ef4444" font-size="6.5" font-family="monospace">10.00 V</text>';
    svg+='<circle cx="'+(psX+12)+'" cy="'+(psY+26)+'" r="2.5" fill="#ef4444"/>';
    svg+='<circle cx="'+(psX+32)+'" cy="'+(psY+26)+'" r="2.5" fill="#020617" stroke="#64748b" stroke-width="1"/>';
    svg+='<text x="'+(psX+22)+'" y="'+(psY+45)+'" text-anchor="middle" fill="#9fb498" font-size="6.5">DC Supply</text>';

    // HUD Card at x=470, y=45, w=220, h=220
    const bX=470,bY=45,bW=220,bH=220;
    const E_field=100.00;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">PROBE DISPLACEMENT (x)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+x_cm.toFixed(1)+'</text>';
    svg+='<text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">cm</text>';
    svg+='<text x="'+(bX+130)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">(±0.5 mm)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">MEASURED ELECTRIC POTENTIAL (V)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="18" font-family="monospace">'+V_meas.toFixed(2)+' V</text>';
    svg+='<text x="'+(bX+130)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">(Z_in = 10 MΩ)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">POTENTIAL GRADIENT & FIELD STRENGTH</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">'+E_field.toFixed(2)+'</text>';
    svg+='<text x="'+(bX+110)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">V m⁻¹ (N C⁻¹)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">V₀ = 10.00 V · Plate Gap d = 10.00 cm = 0.100 m</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>';
    svg+=text(bX+15,bY+210,'V(x) = E x ⇔ E = −dV/dx = m',ink,9);
    svg+=text(240,22,'Teledeltos Conducting Paper Equipotential Mapping Bench');
    svg+=text(240,308,'Electric Field: E⃗ = −∇V · Field Strength: E = V₀ / d = 100.00 V m⁻¹');
  }
  else if(cfg.slug==='magnetic-moments'){
    const d_cm=p.input;
    const theta_deg=v.raw;
    const tan_theta=Math.tan(theta_deg*Math.PI/180.0);
    const inv_d3=1.0/Math.pow(d_cm/100.0, 3);
    const M_val=0.8750;
    const BH_uT=35.00;

    // Bench table
    svg+='<rect x="50" y="250" width="390" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/>';
    // Mahogany Meter Scale Bench (horizontal rule from 0 to 100 cm, center at 245)
    const ruleX=60,ruleY=195,ruleW=370,ruleH=32;
    svg+='<rect x="'+ruleX+'" y="'+ruleY+'" width="'+ruleW+'" height="'+ruleH+'" rx="3" fill="#3e2723" stroke="#5d4037" stroke-width="1.5"/>';
    // Centimeter graduation ticks along meter rule
    for(let g=0;g<=36;g++){
      const gx=ruleX+5+g*10;
      const gh=(g%5===0)?10:5;
      svg+='<line x1="'+gx+'" y1="'+(ruleY+ruleH)+'" x2="'+gx+'" y2="'+(ruleY+ruleH-gh)+'" stroke="#d7ccc8" stroke-width="'+(g%5===0?'1':'0.5')+'"/>';
    }
    svg+='<text x="'+(ruleX+10)+'" y="'+(ruleY+14)+'" fill="#d7ccc8" font-size="7.5" font-family="monospace">WEST ARM</text>';
    svg+='<text x="'+(ruleX+ruleW-10)+'" y="'+(ruleY+14)+'" text-anchor="end" fill="#d7ccc8" font-size="7.5" font-family="monospace">EAST ARM</text>';

    // Central Compass Box at x = 245, y = 145
    const cpX=245,cpY=145,cpR=44;
    // Circular brass casing
    svg+='<circle cx="'+cpX+'" cy="'+cpY+'" r="'+cpR+'" fill="#292524" stroke="#d97706" stroke-width="2.5"/>';
    // Glass cover inner ring & anti-parallax mirror strip
    svg+='<circle cx="'+cpX+'" cy="'+cpY+'" r="'+(cpR-6)+'" fill="#0c0a09" stroke="#78716c" stroke-width="1"/>';
    svg+='<circle cx="'+cpX+'" cy="'+cpY+'" r="'+(cpR-12)+'" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 3"/>';
    // Quadrant graduation marks (0, 90, 0, 90)
    svg+='<text x="'+cpX+'" y="'+(cpY-cpR+14)+'" text-anchor="middle" fill="#f8fafc" font-size="6.5" font-weight="bold">0° (N)</text>';
    svg+='<text x="'+cpX+'" y="'+(cpY+cpR-8)+'" text-anchor="middle" fill="#f8fafc" font-size="6.5" font-weight="bold">0° (S)</text>';
    svg+='<text x="'+(cpX-cpR+14)+'" y="'+(cpY+3)+'" text-anchor="middle" fill="#f8fafc" font-size="6.5" font-weight="bold">90°</text>';
    svg+='<text x="'+(cpX+cpR-14)+'" y="'+(cpY+3)+'" text-anchor="middle" fill="#f8fafc" font-size="6.5" font-weight="bold">90°</text>';

    // Rotating pointer at angle theta
    const rad=theta_deg*Math.PI/180.0;
    const pLen=32;
    // Long light aluminum pointer (perpendicular to magnetic needle: 90 deg offset)
    const apx1=cpX+pLen*Math.sin(rad), apy1=cpY-pLen*Math.cos(rad);
    const apx2=cpX-pLen*Math.sin(rad), apy2=cpY+pLen*Math.cos(rad);
    svg+='<line x1="'+apx1.toFixed(1)+'" y1="'+apy1.toFixed(1)+'" x2="'+apx2.toFixed(1)+'" y2="'+apy2.toFixed(1)+'" stroke="#ef4444" stroke-width="1.5"/>';
    // Short cobalt magnetic needle along magnetic axis
    const mLen=14;
    const mpx1=cpX+mLen*Math.cos(rad), mpy1=cpY+mLen*Math.sin(rad);
    const mpx2=cpX-mLen*Math.cos(rad), mpy2=cpY-mLen*Math.sin(rad);
    svg+='<line x1="'+mpx1.toFixed(1)+'" y1="'+mpy1.toFixed(1)+'" x2="'+mpx2.toFixed(1)+'" y2="'+mpy2.toFixed(1)+'" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>';
    // Agate jewel pivot cap
    svg+='<circle cx="'+cpX+'" cy="'+cpY+'" r="4" fill="#d97706" stroke="#fff" stroke-width="1"/>';
    svg+='<text x="'+cpX+'" y="'+(cpY+cpR+16)+'" text-anchor="middle" fill="'+orange+'" font-size="8" font-family="monospace" font-weight="bold">θ = '+theta_deg.toFixed(2)+'°</text>';

    // Alnico Bar Magnet on East Arm at distance d_cm
    const magOffset=75+((d_cm-14.0)/10.0)*60;
    const mBarX=cpX+magOffset, mBarY=170, mBarW=38, mBarH=16;
    // Magnet sliding carrier
    svg+='<rect x="'+(mBarX-mBarW/2-3)+'" y="'+(mBarY-2)+'" width="'+(mBarW+6)+'" height="'+(mBarH+14)+'" rx="2" fill="#475569" stroke="#334155" stroke-width="1"/>';
    // South pole (blue)
    svg+='<rect x="'+(mBarX-mBarW/2)+'" y="'+mBarY+'" width="'+(mBarW/2)+'" height="'+mBarH+'" fill="#3b82f6"/>';
    svg+='<text x="'+(mBarX-mBarW/4)+'" y="'+(mBarY+11)+'" text-anchor="middle" fill="#fff" font-size="7.5" font-weight="bold">S</text>';
    // North pole (red)
    svg+='<rect x="'+mBarX+'" y="'+mBarY+'" width="'+(mBarW/2)+'" height="'+mBarH+'" fill="#ef4444"/>';
    svg+='<text x="'+(mBarX+mBarW/4)+'" y="'+(mBarY+11)+'" text-anchor="middle" fill="#fff" font-size="7.5" font-weight="bold">N</text>';
    svg+='<rect x="'+(mBarX-mBarW/2)+'" y="'+mBarY+'" width="'+mBarW+'" height="'+mBarH+'" fill="none" stroke="#fff" stroke-width="0.8"/>';
    svg+='<text x="'+mBarX+'" y="'+(mBarY+mBarH+10)+'" text-anchor="middle" fill="#cbd5e1" font-size="6.5">Alnico Magnet</text>';

    // Dimension line from pivot cpX to magnet center mBarX
    svg+='<line x1="'+cpX+'" y1="95" x2="'+mBarX+'" y2="95" stroke="'+orange+'" stroke-width="1.2"/>';
    svg+='<line x1="'+cpX+'" y1="90" x2="'+cpX+'" y2="100" stroke="'+orange+'" stroke-width="1.2"/>';
    svg+='<line x1="'+mBarX+'" y1="90" x2="'+mBarX+'" y2="100" stroke="'+orange+'" stroke-width="1.2"/>';
    svg+='<text x="'+((cpX+mBarX)/2)+'" y="88" text-anchor="middle" fill="'+orange+'" font-size="8.5" font-weight="bold">d = '+d_cm.toFixed(1)+' cm</text>';

    // HUD Card at x=470, y=45, w=220, h=220
    const bX=470,bY=45,bW=220,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">MAGNET DISTANCE & INVERSE CUBE</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+d_cm.toFixed(1)+'</text>';
    svg+='<text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">cm</text>';
    svg+='<text x="'+(bX+130)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">1/d³ = '+inv_d3.toFixed(1)+' m⁻³</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">OBSERVED COMPASS DEFLECTION (θ)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="18" font-family="monospace">'+theta_deg.toFixed(2)+'°</text>';
    svg+='<text x="'+(bX+125)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">tan θ = '+tan_theta.toFixed(4)+'</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">MAGNETIC DIPOLE MOMENT & FIELD</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">'+M_val.toFixed(4)+'</text>';
    svg+='<text x="'+(bX+110)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">A m² (J T⁻¹)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">B_H = '+BH_uT.toFixed(2)+' μT · μ₀/(4π) = 1.000 × 10⁻⁷ T m A⁻¹</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>';
    svg+=text(bX+15,bY+210,'tan θ = [(2μ₀/4π) M / B_H] · (1/d³)',ink,9);
    svg+=text(240,22,'Gauss Deflection Magnetometer Bench (Tan-A Position)');
    svg+=text(240,308,'Axial Dipole Field: B_A = (μ₀ / 4π) (2M / d³) · Tangent Law: B_A = B_H tan θ');
  }
  else if(cfg.slug==='internal-resistance'){
    const I_mA=p.input;
    const I_A=I_mA/1000.0;
    const V_meas=v.raw;
    const P_mW=V_meas*I_mA;
    const r_val=2.500;
    const E_val=1.500;

    // Bench table
    svg+='<rect x="50" y="250" width="390" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/>';

    // Primary Cell (Leclanché dry cell) at x = 70, y = 140, w = 75, h = 95
    const cX=70,cY=140,cW=75,cH=95;
    svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" rx="4" fill="#1e293b" stroke="#334155" stroke-width="2"/>';
    svg+='<rect x="'+(cX+6)+'" y="'+(cY+18)+'" width="'+(cW-12)+'" height="'+(cH-24)+'" rx="2" fill="#0f172a"/>';
    // Battery Terminals (+ brass post, - zinc post)
    svg+='<rect x="'+(cX+14)+'" y="'+(cY-8)+'" width="10" height="8" rx="2" fill="#ef4444"/>';
    svg+='<text x="'+(cX+19)+'" y="'+(cY-11)+'" text-anchor="middle" fill="#fca5a5" font-size="7.5" font-weight="bold">+</text>';
    svg+='<rect x="'+(cX+cW-24)+'" y="'+(cY-8)+'" width="10" height="8" rx="2" fill="#3b82f6"/>';
    svg+='<text x="'+(cX+cW-19)+'" y="'+(cY-11)+'" text-anchor="middle" fill="#93c5fd" font-size="7.5" font-weight="bold">−</text>';
    // Cell labels
    svg+='<text x="'+(cX+cW/2)+'" y="'+(cY+38)+'" text-anchor="middle" fill="'+orange+'" font-size="8.5" font-weight="bold">Primary Cell</text>';
    svg+='<text x="'+(cX+cW/2)+'" y="'+(cY+52)+'" text-anchor="middle" fill="#cbd5e1" font-size="7.5">ℰ = 1.500 V</text>';
    svg+='<text x="'+(cX+cW/2)+'" y="'+(cY+66)+'" text-anchor="middle" fill="#94a3b8" font-size="7">r = 2.500 Ω</text>';

    // Precision Decade Resistance Box at x = 180, y = 155, w = 110, h = 80
    const rbX=180,rbY=155,rbW=110,rbH=80;
    svg+='<rect x="'+rbX+'" y="'+rbY+'" width="'+rbW+'" height="'+rbH+'" rx="4" fill="#332418" stroke="#5a3d28" stroke-width="2"/>';
    svg+='<text x="'+(rbX+rbW/2)+'" y="'+(rbY+18)+'" text-anchor="middle" fill="#e2ecd7" font-size="8" font-weight="bold">Decade Resistance</text>';
    // Resistance dials (x10, x1, x0.1)
    const dPos=[rbX+25, rbX+55, rbX+85];
    dPos.forEach((dx,idx)=>{
      svg+='<circle cx="'+dx+'" cy="'+(rbY+42)+'" r="11" fill="#1b120c" stroke="#8c6239" stroke-width="1.5"/>';
      svg+='<line x1="'+dx+'" y1="'+(rbY+42)+'" x2="'+(dx+6)+'" y2="'+(rbY+36)+'" stroke="#ef4444" stroke-width="1.5"/>';
      svg+='<circle cx="'+dx+'" cy="'+(rbY+42)+'" r="3" fill="#d97706"/>';
      svg+='<text x="'+dx+'" y="'+(rbY+65)+'" text-anchor="middle" fill="#cbd5e1" font-size="6.5">'+(idx===0?'x10':idx===1?'x1':'x0.1')+'</text>';
    });
    // Terminals on resistance box
    svg+='<circle cx="'+(rbX+12)+'" cy="'+(rbY+72)+'" r="3.5" fill="#d97706"/>';
    svg+='<circle cx="'+(rbX+rbW-12)+'" cy="'+(rbY+72)+'" r="3.5" fill="#d97706"/>';

    // Digital DC Voltmeter at x = 70, y = 50, w = 75, h = 60
    const vmX=70,vmY=50,vmW=75,vmH=60;
    svg+='<rect x="'+vmX+'" y="'+vmY+'" width="'+vmW+'" height="'+vmH+'" rx="3" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<rect x="'+(vmX+8)+'" y="'+(vmY+8)+'" width="'+(vmW-16)+'" height="20" rx="2" fill="#020617"/>';
    svg+='<text x="'+(vmX+vmW/2)+'" y="'+(vmY+22)+'" text-anchor="middle" fill="#38bdf8" font-size="11" font-family="monospace" font-weight="bold">'+V_meas.toFixed(3)+' V</text>';
    svg+='<text x="'+(vmX+vmW/2)+'" y="'+(vmY+44)+'" text-anchor="middle" fill="#cbd5e1" font-size="7">Digital Voltmeter</text>';
    svg+='<text x="'+(vmX+vmW/2)+'" y="'+(vmY+54)+'" text-anchor="middle" fill="#94a3b8" font-size="6">(Z_in = 10 MΩ)</text>';
    // Voltmeter Kelvin leads to cell terminals
    svg+='<line x1="'+(vmX+18)+'" y1="'+(vmY+vmH)+'" x2="'+(cX+19)+'" y2="'+(cY-8)+'" stroke="#ef4444" stroke-width="1.2" stroke-dasharray="2 2"/>';
    svg+='<line x1="'+(vmX+vmW-18)+'" y1="'+(vmY+vmH)+'" x2="'+(cX+cW-19)+'" y2="'+(cY-8)+'" stroke="#3b82f6" stroke-width="1.2" stroke-dasharray="2 2"/>';

    // Digital DC Ammeter at x = 320, y = 155, w = 90, h = 80
    const amX=320,amY=155,amW=90,amH=80;
    svg+='<rect x="'+amX+'" y="'+amY+'" width="'+amW+'" height="'+amH+'" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="2"/>';
    svg+='<rect x="'+(amX+8)+'" y="'+(amY+12)+'" width="'+(amW-16)+'" height="24" rx="2" fill="#020617"/>';
    svg+='<text x="'+(amX+amW/2)+'" y="'+(amY+28)+'" text-anchor="middle" fill="#f59e0b" font-size="13" font-family="monospace" font-weight="bold">'+I_mA.toFixed(1)+' mA</text>';
    svg+='<text x="'+(amX+amW/2)+'" y="'+(amY+52)+'" text-anchor="middle" fill="#e2ecd7" font-size="8" font-weight="bold">Digital Ammeter</text>';
    svg+='<text x="'+(amX+amW/2)+'" y="'+(amY+65)+'" text-anchor="middle" fill="#94a3b8" font-size="6.5">R_shunt = 0.050 Ω</text>';

    // Closed loop wiring:
    svg+='<line x1="'+(cX+19)+'" y1="'+(cY-8)+'" x2="'+(cX+19)+'" y2="28" stroke="#ef4444" stroke-width="2"/>';
    svg+='<line x1="'+(cX+19)+'" y1="28" x2="'+(rbX+12)+'" y2="28" stroke="#ef4444" stroke-width="2"/>';
    svg+='<line x1="'+(rbX+12)+'" y1="28" x2="'+(rbX+12)+'" y2="'+(rbY+72)+'" stroke="#ef4444" stroke-width="2"/>';
    svg+='<line x1="'+(rbX+rbW-12)+'" y1="'+(rbY+72)+'" x2="'+(amX+15)+'" y2="'+(rbY+72)+'" stroke="#ef4444" stroke-width="2"/>';
    svg+='<line x1="'+(amX+amW-15)+'" y1="'+(amY+40)+'" x2="'+(amX+amW-15)+'" y2="240" stroke="#3b82f6" stroke-width="2"/>';
    svg+='<line x1="'+(amX+amW-15)+'" y1="240" x2="'+(cX+cW-19)+'" y2="240" stroke="#3b82f6" stroke-width="2"/>';
    svg+='<line x1="'+(cX+cW-19)+'" y1="240" x2="'+(cX+cW-19)+'" y2="'+(cY-8)+'" stroke="#3b82f6" stroke-width="2"/>';

    // HUD Card at x=470, y=45, w=220, h=220
    const bX=470,bY=45,bW=220,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">DISCHARGE CURRENT (I)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+I_mA.toFixed(1)+'</text>';
    svg+='<text x="'+(bX+110)+'"; y="'+(bY+50)+'" fill="'+soft+'" font-size="11">mA</text>';
    svg+='<text x="'+(bX+135)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">('+I_A.toFixed(3)+' A)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">TERMINAL POTENTIAL DIFFERENCE (V)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="18" font-family="monospace">'+V_meas.toFixed(3)+' V</text>';
    svg+='<text x="'+(bX+125)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">P = '+P_mW.toFixed(1)+' mW</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">CELL INTERNAL RESISTANCE & EMF</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">'+r_val.toFixed(3)+'</text>';
    svg+='<text x="'+(bX+90)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">Ω (r = −m)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">ℰ = '+E_val.toFixed(3)+' V (b = ℰ) · I_sc = 600.0 mA</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>';
    svg+=text(bX+15,bY+210,'V = ℰ − I · r ⇔ r = (ℰ − V) / I',ink,9);
    svg+=text(240,22,'Cell Electromotive Force & Internal Resistance Bench');
    svg+=text(240,308,'Terminal Characteristic: V = ℰ − I · r · Max Power: P_max = ℰ² / (4r) at R_load = r');
  }
  else if(cfg.slug==='temperature-resistance'){
    const T_degC=p.input;
    const R_meas=v.raw;
    const R0_ref=100.00;
    const alpha_val=0.003930;
    const T_abs=-1.0/alpha_val;

    // Bench table
    svg+='<rect x="50" y="250" width="390" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/>';

    // Thermostatically Controlled Fluid Bath (insulated glass beaker) at x = 70, y = 90, w = 150, h = 150
    const btX=70,btY=90,btW=150,btH=150;
    svg+='<rect x="'+btX+'" y="'+btY+'" width="'+btW+'" height="'+btH+'" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>';
    // Water level inside bath
    svg+='<rect x="'+(btX+4)+'" y="'+(btY+25)+'" width="'+(btW-8)+'" height="'+(btH-29)+'" rx="4" fill="#0284c7" opacity="0.25"/>';
    svg+='<line x1="'+(btX+4)+'" y1="'+(btY+25)+'" x2="'+(btX+btW-4)+'" y2="'+(btY+25)+'" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="3 2"/>';
    svg+='<text x="'+(btX+btW/2)+'" y="'+(btY+20)+'" text-anchor="middle" fill="#7dd3fc" font-size="7.5">Thermostatic Water Bath</text>';

    // Copper Resistance Coil Sheath immersed at center of bath
    const csX=btX+50,csY=btY+45,csW=20,csH=80;
    svg+='<rect x="'+csX+'" y="'+csY+'" width="'+csW+'" height="'+csH+'" rx="3" fill="#b45309" stroke="#d97706" stroke-width="1.5"/>';
    // Internal bifilar winding lines
    for(let w=1;w<=7;w++){
      svg+='<line x1="'+(csX+2)+'" y1="'+(csY+w*10)+'" x2="'+(csX+csW-2)+'" y2="'+(csY+w*10)+'" stroke="#fde68a" stroke-width="1"/>';
    }
    svg+='<text x="'+(csX+csW/2)+'" y="'+(csY+csH+12)+'" text-anchor="middle" fill="#fde68a" font-size="7" font-weight="bold">Cu Coil</text>';

    // Mercury Thermometer immersed alongside coil
    const thX=btX+20,thY=btY-35,thW=10,thH=160;
    svg+='<rect x="'+thX+'" y="'+thY+'" width="'+thW+'" height="'+thH+'" rx="5" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.2"/>';
    // Mercury bulb at bottom
    svg+='<circle cx="'+(thX+thW/2)+'" cy="'+(thY+thH-5)+'" r="7" fill="#ef4444"/>';
    // Mercury column height proportional to T_degC
    const mHeight=20+(T_degC/100.0)*90;
    svg+='<rect x="'+(thX+3)+'" y="'+(thY+thH-10-mHeight)+'" width="4" height="'+mHeight+'" rx="1" fill="#ef4444"/>';
    svg+='<text x="'+(thX-6)+'" y="'+(thY+10)+'" text-anchor="end" fill="#ef4444" font-size="8" font-family="monospace" font-weight="bold">'+T_degC.toFixed(1)+'°C</text>';

    // Motorized Stirrer Paddle
    const stX=btX+110,stY=btY+10;
    svg+='<line x1="'+stX+'" y1="'+stY+'" x2="'+stX+'" y2="'+(stY+115)+'" stroke="#cbd5e1" stroke-width="2"/>';
    svg+='<ellipse cx="'+stX+'" cy="'+(stY+115)+'" rx="12" ry="4" fill="#64748b"/>';
    svg+='<text x="'+stX+'" y="'+(stY-4)+'" text-anchor="middle" fill="#94a3b8" font-size="6.5">Stirrer</text>';

    // Digital 4-Wire Ohmmeter at x = 270, y = 110, w = 120, h = 85
    const omX=270,omY=110,omW=120,omH=85;
    svg+='<rect x="'+omX+'" y="'+omY+'" width="'+omW+'" height="'+omH+'" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="2"/>';
    svg+='<rect x="'+(omX+10)+'" y="'+(omY+10)+'" width="'+(omW-20)+'" height="26" rx="2" fill="#020617"/>';
    svg+='<text x="'+(omX+omW/2)+'" y="'+(omY+28)+'" text-anchor="middle" fill="#10b981" font-size="16" font-family="monospace" font-weight="bold">'+R_meas.toFixed(2)+' Ω</text>';
    svg+='<text x="'+(omX+omW/2)+'" y="'+(omY+50)+'" text-anchor="middle" fill="#e2ecd7" font-size="8" font-weight="bold">Digital Kelvin Bridge</text>';
    svg+='<text x="'+(omX+omW/2)+'" y="'+(omY+64)+'" text-anchor="middle" fill="#94a3b8" font-size="6.5">4-Wire Sensing · I_test ≤ 1 mA</text>';
    // 4 binding posts (C1, P1, P2, C2)
    const bpX=[omX+18, omX+42, omX+78, omX+102];
    bpX.forEach((bx,idx)=>{
      svg+='<circle cx="'+bx+'" cy="'+(omY+74)+'" r="3.5" fill="'+(idx===0||idx===3?'#ef4444':'#3b82f6')+'"/>';
    });

    // 4 Kelvin leads connecting Ohmmeter posts to Coil Head
    svg+='<line x1="'+(csX+4)+'" y1="'+csY+'" x2="'+(csX+4)+'" y2="55" stroke="#ef4444" stroke-width="1.2"/>';
    svg+='<line x1="'+(csX+4)+'" y1="55" x2="'+bpX[0]+'" y2="55" stroke="#ef4444" stroke-width="1.2"/>';
    svg+='<line x1="'+bpX[0]+'" y1="55" x2="'+bpX[0]+'" y2="'+(omY+74)+'" stroke="#ef4444" stroke-width="1.2"/>';

    svg+='<line x1="'+(csX+8)+'" y1="'+csY+'" x2="'+(csX+8)+'" y2="65" stroke="#3b82f6" stroke-width="1.2"/>';
    svg+='<line x1="'+(csX+8)+'" y1="65" x2="'+bpX[1]+'" y2="65" stroke="#3b82f6" stroke-width="1.2"/>';
    svg+='<line x1="'+bpX[1]+'" y1="65" x2="'+bpX[1]+'" y2="'+(omY+74)+'" stroke="#3b82f6" stroke-width="1.2"/>';

    svg+='<line x1="'+(csX+12)+'" y1="'+csY+'" x2="'+(csX+12)+'" y2="75" stroke="#3b82f6" stroke-width="1.2"/>';
    svg+='<line x1="'+(csX+12)+'" y1="75" x2="'+bpX[2]+'" y2="75" stroke="#3b82f6" stroke-width="1.2"/>';
    svg+='<line x1="'+bpX[2]+'" y1="75" x2="'+bpX[2]+'" y2="'+(omY+74)+'" stroke="#3b82f6" stroke-width="1.2"/>';

    svg+='<line x1="'+(csX+16)+'" y1="'+csY+'" x2="'+(csX+16)+'" y2="85" stroke="#ef4444" stroke-width="1.2"/>';
    svg+='<line x1="'+(csX+16)+'" y1="85" x2="'+bpX[3]+'" y2="85" stroke="#ef4444" stroke-width="1.2"/>';
    svg+='<line x1="'+bpX[3]+'" y1="85" x2="'+bpX[3]+'" y2="'+(omY+74)+'" stroke="#ef4444" stroke-width="1.2"/>';

    // HUD Card at x=470, y=45, w=220, h=220
    const bX=470,bY=45,bW=220,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">BATH TEMPERATURE (T)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+T_degC.toFixed(1)+'</text>';
    svg+='<text x="'+(bX+95)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">°C</text>';
    svg+='<text x="'+(bX+125)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">('+(T_degC+273.15).toFixed(1)+' K)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">MEASURED COIL RESISTANCE (R)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="18" font-family="monospace">'+R_meas.toFixed(2)+' Ω</text>';
    svg+='<text x="'+(bX+125)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">R₀ = '+R0_ref.toFixed(2)+' Ω</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">TEMPERATURE COEFFICIENT (α)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">'+(alpha_val*1000.0).toFixed(3)+'</text>';
    svg+='<text x="'+(bX+75)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">× 10⁻³ °C⁻¹ (α = m/b)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">Inferred Absolute Zero: T_abs = −b/m = '+T_abs.toFixed(1)+' °C</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>';
    svg+=text(bX+15,bY+210,'R(T) = R₀(1 + α T) ⇔ α = (R − R₀) / (R₀ T)',ink,9);
    svg+=text(240,22,'Resistance vs. Temperature Measurement Bench');
    svg+=text(240,308,'Linear Law: R = (R₀ α) T + R₀ · Inferred Absolute Zero: T_abs = −1 / α = −254.5 °C');
  }
  else if(cfg.slug==='faradays-law-electrolysis'){
    const Q_C=p.input;
    const m_g=v.raw;
    const m_mg=m_g*1000.0;
    const I_A=1.000;
    const t_s=Q_C/I_A;
    const t_min=t_s/60.0;
    const Z_val=0.3293;
    const F_val=96485.3;

    // Bench table
    svg+='<rect x="50" y="250" width="390" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/>';

    // Copper Voltameter Glass Jar at x = 70, y = 100, w = 140, h = 140
    const vjX=70,vjY=100,vjW=140,vjH=140;
    svg+='<rect x="'+vjX+'" y="'+vjY+'" width="'+vjW+'" height="'+vjH+'" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>';
    // Deep blue CuSO4 electrolyte solution
    svg+='<rect x="'+(vjX+4)+'" y="'+(vjY+20)+'" width="'+(vjW-8)+'" height="'+(vjH-24)+'" rx="3" fill="#0369a1" opacity="0.45"/>';
    svg+='<line x1="'+(vjX+4)+'" y1="'+(vjY+20)+'" x2="'+(vjX+vjW-4)+'" y2="'+(vjY+20)+'" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="3 2"/>';
    svg+='<text x="'+(vjX+vjW/2)+'" y="'+(vjY+15)+'" text-anchor="middle" fill="#7dd3fc" font-size="7">Acidified CuSO₄ Solution</text>';

    // Ebonite suspension crossbar
    svg+='<rect x="'+(vjX-5)+'" y="'+(vjY+22)+'" width="'+(vjW+10)+'" height="8" rx="2" fill="#1e293b" stroke="#475569" stroke-width="1"/>';

    // Outer Anode Plates (two copper plates on sides)
    const an1X=vjX+22, an2X=vjX+vjW-34, anY=vjY+30, anW=12, anH=85;
    svg+='<rect x="'+an1X+'" y="'+anY+'" width="'+anW+'" height="'+anH+'" fill="#b45309" stroke="#d97706" stroke-width="1"/>';
    svg+='<rect x="'+an2X+'" y="'+anY+'" width="'+anW+'" height="'+anH+'" fill="#b45309" stroke="#d97706" stroke-width="1"/>';
    svg+='<text x="'+(an1X+anW/2)+'" y="'+(anY+anH+12)+'" text-anchor="middle" fill="#fde68a" font-size="6.5">Anode (+)</text>';
    svg+='<text x="'+(an2X+anW/2)+'" y="'+(anY+anH+12)+'" text-anchor="middle" fill="#fde68a" font-size="6.5">Anode (+)</text>';

    // Central Removable Cathode Plate
    const catX=vjX+vjW/2-7, catY=vjY+28, catW=14, catH=88;
    svg+='<rect x="'+catX+'" y="'+catY+'" width="'+catW+'" height="'+catH+'" fill="#64748b" stroke="#94a3b8" stroke-width="1.2"/>';
    // Salmon-pink copper crystalline deposit growing on cathode
    const depThick=1.5+(Q_C/3600.0)*3.5;
    svg+='<rect x="'+(catX-depThick)+'" y="'+(catY+5)+'" width="'+(catW+2*depThick)+'" height="'+(catH-10)+'" rx="1" fill="#ea580c" opacity="0.85"/>';
    svg+='<text x="'+(catX+catW/2)+'" y="'+(catY+catH+12)+'" text-anchor="middle" fill="#fca5a5" font-size="7" font-weight="bold">Cathode (−)</text>';

    // Regulated DC Power Supply at x = 250, y = 80, w = 85, h = 75
    const psX=250,psY=80,psW=85,psH=75;
    svg+='<rect x="'+psX+'" y="'+psY+'" width="'+psW+'" height="'+psH+'" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<rect x="'+(psX+8)+'" y="'+(psY+8)+'" width="'+(psW-16)+'" height="20" rx="2" fill="#020617"/>';
    svg+='<text x="'+(psX+psW/2)+'" y="'+(psY+22)+'" text-anchor="middle" fill="#38bdf8" font-size="11" font-family="monospace" font-weight="bold">1.000 A</text>';
    svg+='<text x="'+(psX+psW/2)+'" y="'+(psY+44)+'" text-anchor="middle" fill="#e2ecd7" font-size="7" font-weight="bold">DC Current Supply</text>';
    svg+='<circle cx="'+(psX+22)+'" cy="'+(psY+60)+'" r="4" fill="#ef4444"/>';
    svg+='<circle cx="'+(psX+psW-22)+'" cy="'+(psY+60)+'" r="4" fill="#3b82f6"/>';

    // Analytical Balance Display Card at x = 250, y = 168, w = 150, h = 72
    const abX=250,abY=168,abW=150,abH=72;
    svg+='<rect x="'+abX+'" y="'+abY+'" width="'+abW+'" height="'+abH+'" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>';
    svg+='<rect x="'+(abX+10)+'" y="'+(abY+10)+'" width="'+(abW-20)+'" height="26" rx="2" fill="#020617"/>';
    svg+='<text x="'+(abX+abW/2)+'" y="'+(abY+28)+'" text-anchor="middle" fill="#10b981" font-size="16" font-family="monospace" font-weight="bold">+'+m_g.toFixed(4)+' g</text>';
    svg+='<text x="'+(abX+abW/2)+'" y="'+(abY+50)+'" text-anchor="middle" fill="#e2ecd7" font-size="8" font-weight="bold">Analytical Balance (Δm)</text>';
    svg+='<text x="'+(abX+abW/2)+'" y="'+(abY+62)+'" text-anchor="middle" fill="#94a3b8" font-size="6.5">Resolution: 0.1 mg · Tare m₀ zeroed</text>';

    // Wiring:
    // Power Supply (+) to Anodes
    svg+='<line x1="'+(psX+22)+'" y1="'+(psY+60)+'" x2="'+(psX+22)+'" y2="50" stroke="#ef4444" stroke-width="1.8"/>';
    svg+='<line x1="'+(psX+22)+'" y1="50" x2="'+(an1X+anW/2)+'" y2="50" stroke="#ef4444" stroke-width="1.8"/>';
    svg+='<line x1="'+(an1X+anW/2)+'" y1="50" x2="'+(an1X+anW/2)+'" y2="'+anY+'" stroke="#ef4444" stroke-width="1.8"/>';
    svg+='<line x1="'+(an1X+anW/2)+'" y1="50" x2="'+(an2X+anW/2)+'" y2="50" stroke="#ef4444" stroke-width="1.8"/>';
    svg+='<line x1="'+(an2X+anW/2)+'" y1="50" x2="'+(an2X+anW/2)+'" y2="'+anY+'" stroke="#ef4444" stroke-width="1.8"/>';

    // Cathode (−) back to Power Supply (−)
    svg+='<line x1="'+(catX+catW/2)+'" y1="'+catY+'" x2="'+(catX+catW/2)+'" y2="60" stroke="#3b82f6" stroke-width="1.8"/>';
    svg+='<line x1="'+(catX+catW/2)+'" y1="60" x2="'+(psX+psW-22)+'" y2="60" stroke="#3b82f6" stroke-width="1.8"/>';

    // HUD Card at x=470, y=45, w=220, h=220
    const bX=470,bY=45,bW=220,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">ELECTRIC CHARGE & TIME</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+Q_C.toFixed(0)+'</text>';
    svg+='<text x="'+(bX+95)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">C</text>';
    svg+='<text x="'+(bX+125)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">('+t_min.toFixed(1)+' min at 1.0 A)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">DEPOSITED COPPER MASS (m)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="18" font-family="monospace">'+m_g.toFixed(4)+' g</text>';
    svg+='<text x="'+(bX+125)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">('+m_mg.toFixed(1)+' mg)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">ELECTROCHEMICAL EQUIVALENT (Z)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">'+Z_val.toFixed(4)+'</text>';
    svg+='<text x="'+(bX+85)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">mg C⁻¹ (g/C × 1000)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">Faraday F = '+F_val.toFixed(0)+' C mol⁻¹ · N_A = 6.022 × 10²³</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>';
    svg+=text(bX+15,bY+210,'m = Z · Q ⇔ Z = m / (I · t)',ink,9);
    svg+=text(240,22,"Faraday's Law of Electrolysis (Copper Voltameter)");
    svg+=text(240,308,"Faraday's 1st Law: m = Z · Q · Faraday Constant: F = M_Cu / (2Z) = 96485.3 C mol⁻¹");
  }
  else if(cfg.slug==='electrical-equivalent-heat'){
    const t_s=p.input;
    const T_final=v.raw;
    const P_W=25.00;
    const W_J=P_W*t_s;
    const C_sys=259.3;
    const T0=20.00;
    const dT=T_final-T0;
    const Q_cal=C_sys*dT;
    const J_est=W_J/Q_cal;

    svg+='<rect x="50" y="250" width="390" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/>';

    const jX=70,jY=90,jW=150,jH=150;
    svg+='<rect x="'+jX+'" y="'+jY+'" width="'+jW+'" height="'+jH+'" rx="8" fill="#1e293b" stroke="'+soft+'" stroke-width="2"/>';
    svg+='<rect x="'+(jX+12)+'" y="'+(jY+15)+'" width="'+(jW-24)+'" height="'+(jH-22)+'" rx="4" fill="#0f172a" stroke="#94a3b8" stroke-width="1.5"/>';
    svg+='<rect x="'+(jX+16)+'" y="'+(jY+35)+'" width="'+(jW-32)+'" height="'+(jH-45)+'" rx="2" fill="#0284c7" opacity="0.35"/>';
    svg+='<line x1="'+(jX+16)+'" y1="'+(jY+35)+'" x2="'+(jX+jW-16)+'" y2="'+(jY+35)+'" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<text x="'+(jX+jW/2)+'" y="'+(jY+28)+'" text-anchor="middle" fill="#7dd3fc" font-size="7.5">250.0 g Distilled Water</text>';

    svg+='<rect x="'+(jX-4)+'" y="'+(jY+10)+'" width="'+(jW+8)+'" height="10" rx="2" fill="#334155" stroke="#64748b" stroke-width="1"/>';

    const coilX=jX+jW/2-15, coilY=jY+95;
    svg+='<path d="M'+coilX+' '+(jY+20)+' V'+coilY+'" fill="none" stroke="#f59e0b" stroke-width="2"/>';
    svg+='<path d="M'+(coilX+30)+' '+(jY+20)+' V'+coilY+'" fill="none" stroke="#f59e0b" stroke-width="2"/>';
    svg+='<path d="M'+coilX+' '+coilY+' C'+(coilX+5)+' '+(coilY+15)+','+(coilX+10)+' '+(coilY-10)+','+(coilX+15)+' '+coilY+' C'+(coilX+20)+' '+(coilY+15)+','+(coilX+25)+' '+(coilY-10)+','+(coilX+30)+' '+coilY+'" fill="none" stroke="#ea580c" stroke-width="3"/>';
    svg+='<text x="'+(jX+jW/2)+'" y="'+(coilY+28)+'" text-anchor="middle" fill="#fde68a" font-size="7">Nichrome Coil (1.00 Ω)</text>';

    const thX=jX+32;
    svg+='<rect x="'+(thX-3)+'" y="30" width="6" height="150" rx="3" fill="#1e293b" stroke="'+soft+'" stroke-width="1"/>';
    const mercH=20+(dT/15.0)*80;
    svg+='<line x1="'+thX+'" y1="'+(180-mercH)+'" x2="'+thX+'" y2="180" stroke="#ef4444" stroke-width="2"/>';
    svg+='<circle cx="'+thX+'" cy="180" r="4.5" fill="#ef4444"/>';
    svg+='<text x="'+thX+'" y="24" text-anchor="middle" fill="'+orange+'" font-size="9" font-weight="bold">'+T_final.toFixed(2)+' °C</text>';

    const stX=jX+jW-32;
    svg+='<line x1="'+stX+'" y1="45" x2="'+stX+'" y2="'+(jY+jH-25)+'" stroke="#94a3b8" stroke-width="2"/>';
    svg+='<ellipse cx="'+stX+'" cy="'+(jY+jH-25)+'" rx="12" ry="3" fill="none" stroke="#94a3b8" stroke-width="1.5"/>';

    const psX=250,psY=70,psW=95,psH=80;
    svg+='<rect x="'+psX+'" y="'+psY+'" width="'+psW+'" height="'+psH+'" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<rect x="'+(psX+8)+'" y="'+(psY+8)+'" width="'+(psW-16)+'" height="18" rx="2" fill="#020617"/>';
    svg+='<text x="'+(psX+psW/2)+'" y="'+(psY+21)+'" text-anchor="middle" fill="#38bdf8" font-size="10" font-family="monospace" font-weight="bold">5.00V · 5.00A</text>';
    svg+='<text x="'+(psX+psW/2)+'" y="'+(psY+40)+'" text-anchor="middle" fill="#e2ecd7" font-size="7.5" font-weight="bold">P = 25.00 W</text>';
    svg+='<circle cx="'+(psX+25)+'" cy="'+(psY+62)+'" r="4" fill="#ef4444"/>';
    svg+='<circle cx="'+(psX+psW-25)+'" cy="'+(psY+62)+'" r="4" fill="#3b82f6"/>';

    const chX=250,chY=165,chW=95,chH=65;
    svg+='<rect x="'+chX+'" y="'+chY+'" width="'+chW+'" height="'+chH+'" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>';
    svg+='<rect x="'+(chX+8)+'" y="'+(chY+8)+'" width="'+(chW-16)+'" height="24" rx="2" fill="#020617"/>';
    const m_min=Math.floor(t_s/60);
    const s_sec=(t_s%60).toFixed(0).padStart(2,'0');
    svg+='<text x="'+(chX+chW/2)+'" y="'+(chY+25)+'" text-anchor="middle" fill="#10b981" font-size="14" font-family="monospace" font-weight="bold">'+m_min+':'+s_sec+'</text>';
    svg+='<text x="'+(chX+chW/2)+'" y="'+(chY+48)+'" text-anchor="middle" fill="#e2ecd7" font-size="7.5" font-weight="bold">Elapsed Heating Time</text>';

    svg+='<line x1="'+(psX+25)+'" y1="'+(psY+62)+'" x2="'+(coilX+30)+'" y2="'+(jY+20)+'" stroke="#ef4444" stroke-width="1.5"/>';
    svg+='<line x1="'+(psX+psW-25)+'" y1="'+(psY+62)+'" x2="'+coilX+'" y2="'+(jY+20)+'" stroke="#3b82f6" stroke-width="1.5"/>';

    const bX=470,bY=45,bW=220,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">ELECTRICAL WORK INPUT (W)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+W_J.toFixed(0)+'</text>';
    svg+='<text x="'+(bX+95)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">J</text>';
    svg+='<text x="'+(bX+120)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">(W = V · I · t)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">HEAT GENERATED (Q_sys)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="18" font-family="monospace">'+Q_cal.toFixed(1)+' cal</text>';
    svg+='<text x="'+(bX+125)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">(ΔT = '+dT.toFixed(2)+' °C)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">MECHANICAL EQUIVALENT (J)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">'+J_est.toFixed(4)+'</text>';
    svg+='<text x="'+(bX+85)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">J cal⁻¹ (100.0% match)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">Calorimeter Heat Capacity: C_sys = 259.3 cal/°C</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>';
    svg+=text(bX+15,bY+210,'W = J · Q ⇔ J = W / [C_sys (T_f − T₀)]',ink,9);
    svg+=text(240,22,'Joule Electrical Equivalent of Heat Calorimeter');
    svg+=text(240,308,'Joule Heating: W = V · I · t = J · C_sys · ΔT · Reference J = 4.1860 J cal⁻¹');
  }
  else if(cfg.slug==='potentiometer-emf-comparison'){
    const E_cell=p.input;
    const ell_cm=v.raw;
    const k_grad=0.02000;

    svg+='<rect x="30" y="250" width="410" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/>';

    const pbX=40,pbY=140,pbW=390,pbH=90;
    svg+='<rect x="'+pbX+'" y="'+pbY+'" width="'+pbW+'" height="'+pbH+'" rx="4" fill="#2d1b0e" stroke="#854d0e" stroke-width="2"/>';
    svg+='<rect x="'+(pbX+15)+'" y="'+(pbY+15)+'" width="'+(pbW-30)+'" height="22" rx="2" fill="#fde047" opacity="0.85"/>';
    for(let m=0;m<=10;m++){
      const tx=pbX+25+m*34;
      svg+='<line x1="'+tx+'" y1="'+(pbY+15)+'" x2="'+tx+'" y2="'+(pbY+27)+'" stroke="#713f12" stroke-width="1.5"/>';
      svg+='<text x="'+tx+'" y="'+(pbY+34)+'" text-anchor="middle" fill="#713f12" font-size="7.5" font-weight="bold">'+(m*10)+'</text>';
    }

    svg+='<rect x="'+(pbX+8)+'" y="'+(pbY+45)+'" width="20" height="30" rx="2" fill="#ca8a04" stroke="#eab308" stroke-width="1"/>';
    svg+='<rect x="'+(pbX+pbW-28)+'" y="'+(pbY+45)+'" width="20" height="30" rx="2" fill="#ca8a04" stroke="#eab308" stroke-width="1"/>';
    svg+='<line x1="'+(pbX+20)+'" y1="'+(pbY+60)+'" x2="'+(pbX+pbW-20)+'" y2="'+(pbY+60)+'" stroke="#e2e8f0" stroke-width="2"/>';
    svg+='<text x="'+(pbX+pbW/2)+'" y="'+(pbY+80)+'" text-anchor="middle" fill="#fef08a" font-size="7.5">Uniform Manganin Wire (100.0 cm · 2.000 V Total Drop)</text>';

    const jockX=pbX+25+(ell_cm/100.0)*340;
    svg+='<path d="M'+(jockX-6)+' '+(pbY+42)+' H'+(jockX+6)+' L'+jockX+' '+(pbY+60)+' Z" fill="#ef4444" stroke="#fca5a5" stroke-width="1"/>';
    svg+='<rect x="'+(jockX-3)+'" y="'+(pbY+25)+'" width="6" height="18" rx="1" fill="#475569"/>';
    svg+='<circle cx="'+jockX+'" cy="'+(pbY+24)+'" r="4.5" fill="#f59e0b"/>';
    svg+='<text x="'+jockX+'" y="'+(pbY+18)+'" text-anchor="middle" fill="'+orange+'" font-size="8" font-weight="bold">'+ell_cm.toFixed(1)+' cm</text>';

    const drX=50,drY=45,drW=70,drH=60;
    svg+='<rect x="'+drX+'" y="'+drY+'" width="'+drW+'" height="'+drH+'" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<text x="'+(drX+drW/2)+'" y="'+(drY+24)+'" text-anchor="middle" fill="#38bdf8" font-size="9" font-weight="bold">2.000 V</text>';
    svg+='<text x="'+(drX+drW/2)+'" y="'+(drY+42)+'" text-anchor="middle" fill="#94a3b8" font-size="7">Driver Battery</text>';
    svg+='<circle cx="'+(drX+16)+'" cy="'+(drY+52)+'" r="3.5" fill="#ef4444"/>';
    svg+='<circle cx="'+(drX+drW-16)+'" cy="'+(drY+52)+'" r="3.5" fill="#3b82f6"/>';

    const tcX=160,tcY=45,tcW=75,tcH=60;
    svg+='<rect x="'+tcX+'" y="'+tcY+'" width="'+tcW+'" height="'+tcH+'" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>';
    svg+='<text x="'+(tcX+tcW/2)+'" y="'+(tcY+24)+'" text-anchor="middle" fill="#10b981" font-size="9" font-weight="bold">ℰ = '+E_cell.toFixed(3)+' V</text>';
    svg+='<text x="'+(tcX+tcW/2)+'" y="'+(tcY+42)+'" text-anchor="middle" fill="#94a3b8" font-size="7">Test Cell (Unknown)</text>';
    svg+='<circle cx="'+(tcX+16)+'" cy="'+(tcY+52)+'" r="3.5" fill="#ef4444"/>';
    svg+='<circle cx="'+(tcX+tcW-16)+'" cy="'+(tcY+52)+'" r="3.5" fill="#3b82f6"/>';

    const gDialX=275,gDialY=45,gDialW=75,gDialH=60;
    svg+='<rect x="'+gDialX+'" y="'+gDialY+'" width="'+gDialW+'" height="'+gDialH+'" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5"/>';
    svg+='<circle cx="'+(gDialX+gDialW/2)+'" cy="'+(gDialY+26)+'" r="16" fill="#020617" stroke="#334155" stroke-width="1"/>';
    svg+='<line x1="'+(gDialX+gDialW/2)+'" y1="'+(gDialY+26)+'" x2="'+(gDialX+gDialW/2)+'" y2="'+(gDialY+13)+'" stroke="#10b981" stroke-width="2"/>';
    svg+='<circle cx="'+(gDialX+gDialW/2)+'" cy="'+(gDialY+26)+'" r="2" fill="#10b981"/>';
    svg+='<text x="'+(gDialX+gDialW/2)+'" y="'+(gDialY+52)+'" text-anchor="middle" fill="#10b981" font-size="7" font-weight="bold">I_G = 0.000 μA (NULL)</text>';

    svg+='<line x1="'+(drX+16)+'" y1="'+(drY+52)+'" x2="'+(pbX+20)+'" y2="'+(pbY+50)+'" stroke="#ef4444" stroke-width="1.5"/>';
    svg+='<line x1="'+(drX+drW-16)+'" y1="'+(drY+52)+'" x2="'+(pbX+pbW-20)+'" y2="'+(pbY+50)+'" stroke="#3b82f6" stroke-width="1.5"/>';
    svg+='<line x1="'+(tcX+16)+'" y1="'+(tcY+52)+'" x2="'+(pbX+20)+'" y2="'+(pbY+50)+'" stroke="#ef4444" stroke-width="1.2" stroke-dasharray="2 2"/>';
    svg+='<line x1="'+(tcX+tcW-16)+'" y1="'+(tcY+52)+'" x2="'+(gDialX+16)+'" y2="'+(gDialY+52)+'" stroke="#f59e0b" stroke-width="1.5"/>';
    svg+='<line x1="'+(gDialX+gDialW-16)+'" y1="'+(gDialY+52)+'" x2="'+jockX+'" y2="'+(pbY+24)+'" stroke="#f59e0b" stroke-width="1.5"/>';

    const bX=470,bY=45,bW=220,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">CELL ELECTROMOTIVE FORCE (ℰ)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+E_cell.toFixed(3)+'</text>';
    svg+='<text x="'+(bX+95)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">V</text>';
    svg+='<text x="'+(bX+120)+'" y="'+(bY+50)+'" fill="#9fb498" font-size="8">(Open-Circuit EMF)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">NULL BALANCING LENGTH (ℓ)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="18" font-family="monospace">'+ell_cm.toFixed(2)+' cm</text>';
    svg+='<text x="'+(bX+125)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">(±0.05 cm)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">POTENTIAL GRADIENT (k)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">'+k_grad.toFixed(4)+'</text>';
    svg+='<text x="'+(bX+85)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">V cm⁻¹ (2.0000 V m⁻¹)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">Potentiometer Sensitivity: 0.05 cm ≡ 1.0 mV</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>';
    svg+=text(bX+15,bY+210,'ℰ = k · ℓ ⇔ ℰ₁ / ℰ₂ = ℓ₁ / ℓ₂',ink,9);
    svg+=text(240,22,'Precision Slide-Wire Potentiometer Metrology Bench');
    svg+=text(240,308,'Null Method: ℰ_cell = k · ℓ · Zero Current I_G = 0 Eliminates Internal Drop I · r');
  }
  else if(cfg.slug==='emission-spectra-spectroscopy'){
    const n_val=p.input;
    const lambda_nm=v.raw;
    const lineNames={3:'Hα (Ruby-Red)', 4:'Hβ (Cyan)', 5:'Hγ (Blue-Violet)', 6:'Hδ (Deep Violet)', 7:'Hε (Near UV)', 8:'Hζ (Near UV)'};
    const lineCols={3:'#ef4444', 4:'#06b6d4', 5:'#6366f1', 6:'#8b5cf6', 7:'#a855f7', 8:'#d946ef'};
    const lineTitle=lineNames[n_val] || ('n = '+n_val);
    const lineCol=lineCols[n_val] || '#38bdf8';
    const c_speed=299792458;
    const nu_THz=(c_speed/(lambda_nm*1e-9))/1e12;
    const E_eV=(1239.84193/lambda_nm);
    const x_factor=0.25-1.0/(n_val*n_val);
    const R_H_meas=(1e9/lambda_nm)/x_factor;

    svg+='<rect x="40" y="250" width="410" height="14" rx="2" fill="#1b2a26" stroke="'+soft+'" stroke-width="1.5"/>';

    const spX=180,spY=175;
    svg+='<polygon points="'+(spX-45)+',250 '+(spX+45)+',250 '+(spX+20)+',215 '+(spX-20)+',215" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>';
    svg+='<rect x="'+(spX-12)+'" y="145" width="24" height="70" fill="#334155" stroke="#475569" stroke-width="1"/>';
    svg+='<circle cx="'+spX+'" cy="'+(spY-30)+'" r="48" fill="#0f172a" stroke="'+soft+'" stroke-width="2"/>';
    svg+='<circle cx="'+spX+'" cy="'+(spY-30)+'" r="44" fill="none" stroke="#334155" stroke-dasharray="2 3"/>';

    svg+='<rect x="50" y="'+(spY-37)+'" width="95" height="14" rx="2" fill="#334155" stroke="#64748b" stroke-width="1.5"/>';
    svg+='<rect x="44" y="'+(spY-40)+'" width="8" height="20" rx="1" fill="#475569" stroke="#94a3b8" stroke-width="1"/>';
    svg+='<text x="95" y="'+(spY-42)+'" text-anchor="middle" fill="#94a3b8" font-size="7">Collimator Tube</text>';

    svg+='<rect x="22" y="'+(spY-52)+'" width="18" height="44" rx="5" fill="#1e1e38" stroke="#818cf8" stroke-width="1.5"/>';
    svg+='<rect x="28" y="'+(spY-42)+'" width="6" height="24" rx="2" fill="#d946ef" opacity="0.85"/>';
    svg+='<circle cx="31" cy="'+(spY-30)+'" r="5" fill="#f43f5e" opacity="0.75"/>';
    svg+='<text x="31" y="'+(spY-58)+'" text-anchor="middle" fill="#f43f5e" font-size="6.5" font-weight="bold">H₂ Tube</text>';

    svg+='<rect x="'+(spX-3)+'" y="'+(spY-52)+'" width="6" height="44" rx="1" fill="#0284c7" stroke="#38bdf8" stroke-width="1.5" opacity="0.8"/>';
    svg+='<text x="'+spX+'" y="'+(spY-58)+'" text-anchor="middle" fill="#38bdf8" font-size="7" font-weight="bold">Grating (600 lines/mm)</text>';

    const telAngle = 0.28 + (n_val - 3) * 0.08;
    const telLen = 95;
    const telEndX = spX + telLen * Math.cos(telAngle);
    const telEndY = (spY - 30) - telLen * Math.sin(telAngle);
    svg+='<line x1="'+spX+'" y1="'+(spY-30)+'" x2="'+telEndX.toFixed(1)+'" y2="'+telEndY.toFixed(1)+'" stroke="'+lineCol+'" stroke-width="6" stroke-linecap="round"/>';
    svg+='<line x1="'+spX+'" y1="'+(spY-30)+'" x2="'+telEndX.toFixed(1)+'" y2="'+telEndY.toFixed(1)+'" stroke="#64748b" stroke-width="10" stroke-linecap="round" opacity="0.4"/>';

    const eyX=345, eyY=115, eyR=42;
    svg+='<circle cx="'+eyX+'" cy="'+eyY+'" r="'+(eyR+4)+'" fill="#0a0f14" stroke="#475569" stroke-width="2"/>';
    svg+='<circle cx="'+eyX+'" cy="'+eyY+'" r="'+eyR+'" fill="#020617"/>';
    svg+='<line x1="'+(eyX-eyR)+'" y1="'+eyY+'" x2="'+(eyX+eyR)+'" y2="'+eyY+'" stroke="#334155" stroke-width="1"/>';
    svg+='<line x1="'+eyX+'" y1="'+(eyY-eyR)+'" x2="'+eyX+'" y2="'+(eyY+eyR)+'" stroke="#334155" stroke-width="1"/>';
    svg+='<line x1="'+eyX+'" y1="'+(eyY-eyR+4)+'" x2="'+eyX+'" y2="'+(eyY+eyR-4)+'" stroke="'+lineCol+'" stroke-width="3"/>';
    svg+='<line x1="'+eyX+'" y1="'+(eyY-eyR+4)+'" x2="'+eyX+'" y2="'+(eyY+eyR-4)+'" stroke="#ffffff" stroke-width="1" opacity="0.8"/>';
    svg+='<circle cx="'+eyX+'" cy="'+eyY+'" r="2.5" fill="#fde68a"/>';
    svg+='<text x="'+eyX+'" y="'+(eyY+eyR+14)+'" text-anchor="middle" fill="'+lineCol+'" font-size="8" font-weight="bold">'+lineTitle+'</text>';
    svg+='<text x="'+eyX+'" y="'+(eyY-eyR-6)+'" text-anchor="middle" fill="#94a3b8" font-size="7">Eyepiece Reticle Field</text>';

    svg+='<rect x="130" y="222" width="100" height="20" rx="3" fill="#0f172a" stroke="'+soft+'" stroke-width="1"/>';
    svg+='<text x="180" y="235" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-family="monospace">θ = '+(telAngle*180/Math.PI).toFixed(2)+'°</text>';

    const bX=470,bY=45,bW=220,bH=220;
    svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#182824" stroke="'+soft+'" stroke-width="1.5"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#718e79" font-size="9">PRINCIPAL QUANTUM NUMBER (n)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+52)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+n_val+'</text>';
    svg+='<text x="'+(bX+55)+'" y="'+(bY+50)+'" fill="'+soft+'" font-size="11">⟶ 2</text>';
    svg+='<text x="'+(bX+95)+'" y="'+(bY+50)+'" fill="'+lineCol+'" font-size="9" font-weight="bold">('+lineTitle+')</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#718e79" font-size="9">SPECTRAL WAVELENGTH (λ)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+lineCol+'" font-size="18" font-family="monospace" font-weight="bold">'+lambda_nm.toFixed(1)+' nm</text>';
    svg+='<text x="'+(bX+125)+'" y="'+(bY+108)+'" fill="#9fb498" font-size="8.5">('+E_eV.toFixed(3)+' eV)</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+125)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+125)+'" stroke="#253a34"/>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+144)+'" fill="#718e79" font-size="9">INFERRED RYDBERG CONSTANT (R_H)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="'+orange+'" font-size="15" font-family="monospace" font-weight="bold">'+R_H_meas.toFixed(0)+'</text>';
    svg+='<text x="'+(bX+95)+'" y="'+(bY+168)+'" fill="#9fb498" font-size="9">m⁻¹ (diff < 0.02%)</text>';
    svg+='<text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#9fb498" font-size="8">Optical Frequency ν = '+nu_THz.toFixed(1)+' THz · 1/λ = '+((1e9/lambda_nm).toFixed(0))+' m⁻¹</text>';
    svg+='<line x1="'+(bX+15)+'" y1="'+(bY+195)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+195)+'" stroke="#253a34"/>';
    svg+=text(bX+15,bY+210,'1/λ = R_H (1/4 − 1/n²) ⇔ R_H = S',ink,9);
    svg+=text(240,22,'Transmission Grating Emission Spectrometer');
    svg+=text(240,308,'Balmer Series: 1/λ = R_H (1/2² − 1/n²) · Rydberg Reference: R_H = 1.0967758 × 10⁷ m⁻¹');
  }




   $('apparatusDiagram').innerHTML=svg;}
let last=0;function animate(t){if(!paused&&t-last>70){draw(t);last=t;}requestAnimationFrame(animate);}requestAnimationFrame(animate);update();renderResults();
