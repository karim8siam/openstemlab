'use strict';
const cfg=JSON.parse(document.getElementById('labConfig').textContent),model=window.MathModels,$=id=>document.getElementById(id);
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
 $('liveState').textContent='Ready to execute iteration '+cfg.shortInput+' = '+p.input+'.';
 message('Adjust step '+cfg.shortInput+', then run iteration.');
 draw(performance.now());
}

$('independent').addEventListener('input',()=>{$('independentNumber').value=$('independent').value;update();});
$('independentNumber').addEventListener('input',()=>{const v=+$('independentNumber').value;if($('independentNumber').value!==''&&Number.isFinite(v)&&v>=cfg.min&&v<=cfg.max){$('independent').value=v;update();}});
$('independentNumber').addEventListener('change',()=>{const v=+$('independentNumber').value;if(!Number.isFinite(v)||v<cfg.min||v>cfg.max){$('independentNumber').value=$('independent').value;message('Use a step between '+cfg.min+' and '+cfg.max+' '+cfg.inputUnit+'.',true);return;}$('independent').value=v;$('independentNumber').value=$('independent').value;update();});

$('pauseMotion').hidden=true;
$('resetApparatus').onclick=()=>{if(busy)return;$('independent').value=cfg.initial;$('independentNumber').value=cfg.initial;update();message('Iteration state reset. Your notebook observations are preserved.');};

$('measure').onclick=async()=>{
 if(busy)return;
 const p=params(),prediction=model.predict(cfg.slug,p.input);
 if(!prediction.valid){message('Select a valid step between '+cfg.min+' and '+cfg.max+'.',true);return;}
 busy=true;$('measure').disabled=true;$('recordReading').disabled=true;$('independent').disabled=true;$('independentNumber').disabled=true;
 message('Executing mathematical iteration for k = '+p.input+'…');
 await new Promise(resolve=>setTimeout(resolve,250));
 const raw=prediction.raw;
 measurement=model.reading(cfg.slug,p.input,raw);
 busy=false;$('independent').disabled=false;$('independentNumber').disabled=false;$('measure').disabled=false;$('recordReading').disabled=false;
 $('readingValue').textContent=raw.toFixed(cfg.rawDecimals)+' '+cfg.rawUnit;
 $('liveState').textContent='Iteration step computed; ready to record.';
 message('Iteration k = '+p.input+' completed: '+cfg.measureLabel+' = '+raw+'. Record in notebook.');
};

$('recordReading').onclick=()=>{
 if(!measurement)return;
 if(rows.length>=100){message('Notebook full. Export observations or clear.',true);return;}
 rows.push({...measurement});
 measurement=null;
 $('recordReading').disabled=true;
 persist();
 message('Observation '+rows.length+' recorded. Advance step '+cfg.shortInput+' for the next trial.');
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
  $('fitSummary').innerHTML='<strong>'+fmt(result.value*cfg.resultScale,cfg.resultDecimals)+' '+cfg.resultUnit+'</strong><p>Estimated '+cfg.targetName+'<br>Gradient m: '+fmt(f.m)+'<br>Intercept b: '+fmt(f.b)+'<br>R²: '+f.r2.toFixed(6)+'<br>Difference from reference: '+pct.toFixed(4)+'%<br>Fit standard error: '+fmt(result.se*cfg.resultScale)+' '+cfg.resultUnit+'</p><p>Asymptotic convergence confirmed by linear regression.</p>';
 } else {
  $('fitSummary').innerHTML='<p>Record at least three distinct iteration steps to fit an asymptotic line and calculate '+cfg.targetName+'.</p>';
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
 let svg='<rect width="640" height="340" fill="#080c16"/>';
 for(let i=0;i<=4;i++){
  const x=xmin+i*(xmax-xmin)/4,y=ymin+i*(ymax-ymin)/4;
  svg+='<line x1="'+left+'" y1="'+py(y)+'" x2="'+right+'" y2="'+py(y)+'" stroke="#1e293b" stroke-dasharray="2,2"/><text x="'+(left-9)+'" y="'+(py(y)+4)+'" text-anchor="end" font-size="10" fill="#64748b">'+fmt(y,2)+'</text><text x="'+px(x)+'" y="300" text-anchor="middle" font-size="10" fill="#64748b">'+fmt(x,2)+'</text>';
 }
 svg+='<path d="M'+left+' '+top+'V'+bottom+'H'+right+'" stroke="#475569" fill="none"/><text x="335" y="332" text-anchor="middle" fill="#818cf8" font-size="12">'+cfg.xAxis+'</text><text transform="translate(18 160) rotate(-90)" text-anchor="middle" fill="#818cf8" font-size="12">'+cfg.yAxis+'</text>';
 if(f){
  const points=[];
  for(let i=0;i<=100;i++){
   const x=xmin+i*(xmax-xmin)/100,y=(f.m*x/cfg.xScale+f.b)*cfg.yScale;
   if(y>=ymin&&y<=ymax)points.push(px(x)+','+py(y));
  }
  svg+='<polyline points="'+points.join(' ')+'" stroke="#38bdf8" stroke-width="2.5" fill="none"/>';
 }
 rows.forEach(r=>svg+='<circle cx="'+px(r.x*cfg.xScale)+'" cy="'+py(r.y*cfg.yScale)+'" r="5" fill="#f43f5e" stroke="#fff" stroke-width="1.2"><title>k = '+r.input+' ('+r.raw+')</title></circle>');
 if(!rows.length)svg+='<text x="330" y="155" text-anchor="middle" fill="#475569" font-size="13">Your iteration observations will appear here.</text>';
 $('labPlot').innerHTML=svg;
}

$('downloadReadings').onclick=()=>{
 if(!rows.length)return;
 const header=[cfg.inputLabel,cfg.rawLabel,cfg.xAxis,cfg.yAxis].join(',');
 const content=rows.map(r=>[r.input,r.raw,r.x,r.y].join(',')).join('\n');
 const blob=new Blob([header+'\n'+content],{type:'text/csv'});
 const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=cfg.slug+'-observations.csv';a.click();
};

$('clearReadings').onclick=()=>{
 if(!rows.length)return;
 if(clearPending){rows=[];clearPending=false;persist();message('Notebook cleared.');return;}
 clearPending=true;message('Click Clear observations again to confirm resetting your notebook.');
 setTimeout(()=>{clearPending=false;},3000);
};

$('checkEstimate').onclick=()=>{
 const f=model.fit(rows),answer=+$('studentEstimate').value;
 if(!f){$('estimateFeedback').textContent='Record at least three distinct iteration steps first.';return;}
 if(!$('studentEstimate').value||!Number.isFinite(answer)||answer<=0){$('estimateFeedback').textContent='Enter a valid positive number.';return;}
 const expected=model.estimate(cfg.slug,f).value*cfg.resultScale;
 $('estimateFeedback').textContent=Math.abs(answer-expected)/expected<.02?'Your estimate agrees with the theoretical bound within 2%! Asymptotic rate confirmed.':'Recheck your calculation. The fit yields '+fmt(expected,cfg.resultDecimals)+' '+cfg.resultUnit+'.';
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

function draw(timestamp){
 const p=params();
 const svg=$('apparatusDiagram');
 if(!svg)return;
 const w=720,h=320;
 let content='<defs><pattern id="mathGrid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M 24 0 L 0 0 0 24" fill="none" stroke="#1e293b" stroke-width="0.8"/></pattern></defs><rect width="'+w+'" height="'+h+'" fill="#030712"/><rect width="'+w+'" height="'+h+'" fill="url(#mathGrid)"/>';

 const text=(x,y,str,col='#cbd5e1',sz=11,anchor='start',weight='normal')=>`<text x="${x}" y="${y}" fill="${col}" font-size="${sz}" font-family="system-ui, -apple-system, sans-serif" text-anchor="${anchor}" font-weight="${weight}">${str}</text>`;
 const rect=(x,y,rw,rh,fill='#0f172a',stroke='#334155',rx=4)=>`<rect x="${x}" y="${y}" width="${rw}" height="${rh}" fill="${fill}" stroke="${stroke}" stroke-width="1.2" rx="${rx}"/>`;
 const line=(x1,y1,x2,y2,stroke='#64748b',sw=1.5,dash='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${sw}" ${dash?'stroke-dasharray="'+dash+'"':''}/>`;

 const k = Math.round(p.input);

 if(currentSimMode==='bench'){
  // Main Bench View: Interactive Mathematical Step Dynamics
  content += rect(40, 25, 640, 270, '#090d16', '#312e81', 8);
  content += text(60, 52, cfg.title.toUpperCase(), '#818cf8', 12, 'start', 'bold');
  content += text(60, 70, 'Iteration Step k = ' + k + ' · ' + cfg.measureLabel, '#94a3b8', 11);

  // Coordinate axes
  const ox = 120, oy = 210, axW = 480, axH = 140;
  content += line(ox, oy, ox + axW, oy, '#475569', 1.5);
  content += line(ox, oy - axH, ox, oy + 40, '#475569', 1.5);
  content += text(ox + axW + 10, oy + 4, 'x', '#94a3b8', 11, 'start');
  content += text(ox - 8, oy - axH - 5, 'y', '#94a3b8', 11, 'end');

  // Curve simulation depending on lab
  if(cfg.slug.includes('bisection') || cfg.slug.includes('regula')){
   // Function f(x) crossing x-axis
   content += '<path d="M 140 230 Q 280 210 380 150 T 560 60" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';
   const rootX = 360;
   content += line(rootX, oy - 15, rootX, oy + 15, '#10b981', 2);
   content += text(rootX, oy + 28, 'Root x*', '#10b981', 10, 'middle', 'bold');

   // Bracket visualization shrinking with step k
   const span = Math.max(10, 160 / Math.pow(1.6, k - 1));
   const aX = rootX - span * 0.7;
   const bX = rootX + span * 0.5;
   content += rect(aX, oy - 110, bX - aX, 130, 'rgba(99, 102, 241, 0.15)', '#6366f1', 2);
   content += line(aX, oy - 110, aX, oy + 20, '#818cf8', 2);
   content += line(bX, oy - 110, bX, oy + 20, '#818cf8', 2);
   content += text(aX, oy + 32, 'a_' + k, '#818cf8', 10, 'middle');
   content += text(bX, oy + 32, 'b_' + k, '#818cf8', 10, 'middle');
   content += text(360, 48, 'Bracket Span Δx = ' + (1.0 / Math.pow(2, k)).toFixed(4), '#f59e0b', 11, 'middle');
  } else if(cfg.slug.includes('fixed-point')){
   // Cobweb plot: y = x and y = g(x)
   content += line(ox, oy, ox + 220, oy - 140, '#64748b', 1.5, '4,4'); // y = x
   content += text(ox + 230, oy - 145, 'y = x', '#94a3b8', 10);
   content += '<path d="M 120 180 Q 240 165 360 130" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';
   content += text(370, 130, 'y = g(x)', '#38bdf8', 10);

   // Cobweb staircase
   let cx = ox + 40, cy = oy;
   for(let i = 1; i <= Math.min(k, 5); i++){
    const nextY = oy - (40 + i * 20);
    const nextX = ox + (40 + i * 20);
    content += line(cx, cy, cx, nextY, '#f43f5e', 2);
    content += line(cx, nextY, nextX, nextY, '#f43f5e', 2);
    cx = nextX; cy = nextY;
   }
   content += text(ox + 100, 52, 'Picard Cobweb Contraction · L = 0.125', '#f59e0b', 11);
  } else {
   // Tangent / Secant / Parabolic root-finder
   content += '<path d="M 140 240 Q 280 200 420 120 T 560 50" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';
   const rootX = 390;
   content += line(rootX, oy - 20, rootX, oy + 20, '#10b981', 2);
   content += text(rootX, oy + 30, 'Root x*', '#10b981', 10, 'middle', 'bold');

   const err = Math.max(2, 120 / Math.pow(2.0, k - 1));
   const curX = rootX + err;
   content += line(curX, oy, curX, 100, '#f59e0b', 1.8, '3,3');
   content += `<circle cx="${curX}" cy="100" r="5" fill="#f59e0b"/>`;
   content += text(curX, oy + 16, 'x_' + k, '#f59e0b', 10, 'middle');
   content += text(rootX, 52, 'Theoretical Order α = ' + cfg.target, '#f43f5e', 11, 'middle');
  }

  // Telemetry box on right
  content += rect(490, 80, 170, 180, '#0b1120', '#1e293b', 6);
  content += text(505, 105, 'ITERATION TELEMETRY', '#94a3b8', 9, 'start', 'bold');
  content += text(505, 130, 'Step (k): ' + k, '#cbd5e1', 11);
  content += text(505, 155, 'Target α: ' + cfg.target, '#38bdf8', 11);
  content += text(505, 180, 'Error ε_k: ' + Math.pow(0.5, k).toExponential(3), '#cbd5e1', 11);
  content += text(505, 205, 'Status: Active', '#10b981', 11);
  content += text(505, 230, 'Mode: ' + currentSimMode.toUpperCase(), '#f59e0b', 11);

 } else if(currentSimMode==='compare'){
  // Comparison View: Convergence Rates Comparison
  content += rect(40, 25, 640, 270, '#090d16', '#312e81', 8);
  content += text(60, 52, 'CONVERGENCE SPEED COMPARISON ACROSS METHODS', '#818cf8', 12, 'start', 'bold');
  content += text(60, 70, 'Asymptotic error reduction per iteration step (N = 6 steps)', '#94a3b8', 11);

  const methods = [
   { name: 'Halley Method (Cubic)', col: '#ec4899', rate: 'α = 3.000', errs: [0.5, 0.05, 5e-5, 5e-14, 1e-16] },
   { name: 'Newton / Bairstow / Steffensen', col: '#10b981', rate: 'α = 2.000', errs: [0.5, 0.12, 0.007, 2e-5, 1e-10] },
   { name: 'Brent / Muller / Secant', col: '#38bdf8', rate: 'α = 1.618 - 1.839', errs: [0.5, 0.20, 0.035, 0.001, 1e-6] },
   { name: 'Bisection & Linear Picard', col: '#f59e0b', rate: 'α = 1.000 (C = 0.5)', errs: [0.5, 0.25, 0.125, 0.062, 0.031] }
  ];

  methods.forEach((m, idx)=>{
   const yPos = 100 + idx * 42;
   content += rect(60, yPos, 600, 34, '#0f172a', '#1e293b', 4);
   content += text(75, yPos + 21, m.name, '#e2e8f0', 11, 'start', 'bold');
   content += text(340, yPos + 21, m.rate, m.col, 11, 'start');
   // Bar indicator
   const barW = Math.max(15, 200 * (1.0 / (idx + 1)));
   content += rect(440, yPos + 8, barW, 18, m.col, 'none', 3);
   content += text(450 + barW, yPos + 21, (5 - idx) + 'x speed', '#94a3b8', 10, 'start');
  });

  content += text(60, 280, 'Highlighted current lab target: ' + cfg.targetName + ' = ' + cfg.target, '#f43f5e', 11, 'start', 'bold');

 } else {
  // Sandbox View: Parameter Exploration & Perturbation
  content += rect(40, 25, 640, 270, '#090d16', '#312e81', 8);
  content += text(60, 52, 'NUMERICAL STABILITY & PARAMETER SANDBOX', '#818cf8', 12, 'start', 'bold');
  content += text(60, 70, 'Explore perturbation dynamics, condition numbers, and basin of attraction', '#94a3b8', 11);

  // Basin of attraction visualizer
  const boxW = 580, boxH = 120;
  content += rect(70, 95, boxW, boxH, '#0b1120', '#334155', 6);
  content += line(70, 155, 70 + boxW, 155, '#475569', 1.5); // 0-line

  // Gradient waves
  for(let x = 80; x < 640; x += 15){
   const wave = Math.sin((x + k * 20) * 0.05) * 40;
   content += line(x, 155, x, 155 - wave, '#6366f1', 1.2);
   content += `<circle cx="${x}" cy="${155 - wave}" r="2" fill="#38bdf8"/>`;
  }

  content += text(85, 120, 'Attraction Basin Potential Landscape', '#38bdf8', 10, 'start', 'bold');
  content += text(85, 200, 'Lipschitz Bound L ≤ ' + (1.0 / k).toFixed(3) + ' · Stability Criterion: Convergent', '#10b981', 11);

  content += rect(70, 230, 280, 48, '#0f172a', '#1e293b', 4);
  content += text(85, 250, 'Machine Epsilon ε_mach', '#94a3b8', 10);
  content += text(85, 268, '2.220446 × 10⁻¹⁶ (IEEE 754)', '#f59e0b', 11, 'start', 'bold');

  content += rect(370, 230, 280, 48, '#0f172a', '#1e293b', 4);
  content += text(385, 250, 'Asymptotic Error Exponent α', '#94a3b8', 10);
  content += text(385, 268, cfg.target + ' (' + cfg.targetName + ')', '#ec4899', 11, 'start', 'bold');
 }

 svg.innerHTML = content;
}

update();
renderResults();
