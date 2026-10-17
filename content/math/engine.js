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
 $('liveState').textContent='Ready to execute '+cfg.shortInput+' = '+p.input+'.';
 message('Adjust '+cfg.shortInput+', then run computation.');
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
 message('Executing numerical computation for '+cfg.shortInput+' = '+p.input+'…');
 await new Promise(resolve=>setTimeout(resolve,220));
 const raw=prediction.raw;
 measurement=model.reading(cfg.slug,p.input,raw);
 busy=false;$('independent').disabled=false;$('independentNumber').disabled=false;$('measure').disabled=false;$('recordReading').disabled=false;
 $('readingValue').textContent=raw.toFixed(cfg.rawDecimals)+' '+cfg.rawUnit;
 $('liveState').textContent='Computation finished; ready to record.';
 message(cfg.shortInput+' = '+p.input+' completed: '+cfg.measureLabel+' = '+raw+'. Record in notebook.');
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
  const result=model.estimate(cfg.slug,f),pct=Math.abs(result.value-result.reference)/result.reference*100;
  $('fitSummary').innerHTML='<strong>'+fmt(result.value*cfg.resultScale,cfg.resultDecimals)+' '+cfg.resultUnit+'</strong><p>Estimated '+cfg.targetName+'<br>Gradient m: '+fmt(f.m)+'<br>Intercept b: '+fmt(f.b)+'<br>R²: '+f.r2.toFixed(6)+'<br>Difference from reference: '+pct.toFixed(4)+'%<br>Fit standard error: '+fmt(result.se*cfg.resultScale)+' '+cfg.resultUnit+'</p><p>Asymptotic convergence confirmed by linear regression.</p>';
 } else {
  $('fitSummary').innerHTML='<p>Record at least three distinct observations to fit an asymptotic line and calculate '+cfg.targetName+'.</p>';
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
 rows.forEach(r=>svg+='<circle cx="'+px(r.x*cfg.xScale)+'" cy="'+py(r.y*cfg.yScale)+'" r="5" fill="#f43f5e" stroke="#fff" stroke-width="1.2"><title>'+cfg.shortInput+' = '+r.input+' ('+r.raw+')</title></circle>');
 if(!rows.length)svg+='<text x="330" y="155" text-anchor="middle" fill="#475569" font-size="13">Your recorded observations will appear here.</text>';
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
 if(!f){$('estimateFeedback').textContent='Record at least three distinct observations first.';return;}
 if(!$('studentEstimate').value||!Number.isFinite(answer)||answer<=0){$('estimateFeedback').textContent='Enter a valid positive number.';return;}
 const expected=model.estimate(cfg.slug,f).value*cfg.resultScale;
 $('estimateFeedback').textContent=Math.abs(answer-expected)/expected<.02?'Your estimate agrees with the theoretical model within 2%! Asymptotic rate confirmed.':'Recheck your calculation. The fit yields '+fmt(expected,cfg.resultDecimals)+' '+cfg.resultUnit+'.';
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

 const val = p.input;
 const isMatrix = ['gaussian-elimination-partial-pivoting','lu-decomposition-doolittle-crout','cholesky-decomposition-positive-definite','qr-decomposition-gram-schmidt-householder'].includes(cfg.slug);
 const isIterLin = ['jacobi-iterative-linear-solver','gauss-seidel-successive-relaxation','conjugate-gradient-krylov-optimization'].includes(cfg.slug);
 const isEigen = ['power-iteration-dominant-eigenvalue','inverse-power-iteration-eigen-shift','singular-value-decomposition-pseudoinverse'].includes(cfg.slug);
 const isInterp = ['lagrange-polynomial-interpolation-error','newton-divided-differences-interpolation','runge-phenomenon-chebyshev-nodes','cubic-spline-interpolation-natural-clamped','least-squares-polynomial-curve-fitting'].includes(cfg.slug);
 const isQuad = ['trapezoidal-rule-romberg-extrapolation','simpson-one-third-three-eighths-quadrature','gauss-legendre-quadrature-nodes-weights'].includes(cfg.slug);
 const isMonte = cfg.slug === 'monte-carlo-numerical-multidimensional-integration';
 const isFFT = cfg.slug === 'fast-fourier-transform-spectral-analysis';

 if(currentSimMode==='bench'){
  content += rect(40, 25, 640, 270, '#090d16', '#312e81', 8);
  content += text(60, 52, cfg.title.toUpperCase(), '#818cf8', 12, 'start', 'bold');
  content += text(60, 70, cfg.shortInput + ' = ' + val + ' ' + cfg.inputUnit + ' · ' + cfg.measureLabel, '#94a3b8', 11);

  if(isMatrix){
   const n = Math.round(val);
   const mSize = 130;
   const mx1 = 70, my1 = 110;
   content += text(mx1, my1 - 10, 'A ∈ ℝⁿˣⁿ (n = '+n+')', '#38bdf8', 11, 'start', 'bold');
   content += rect(mx1, my1, mSize, mSize, '#0f172a', '#38bdf8', 4);
   for(let i=0; i<4; i++){
    for(let j=0; j<4; j++){
     const fill = i===j ? '#38bdf8' : (i>j ? '#6366f1' : '#1e293b');
     content += rect(mx1 + 6 + j*30, my1 + 6 + i*30, 26, 26, fill, '#334155', 2);
    }
   }
   content += text(225, my1 + 70, '⟹', '#f43f5e', 22, 'middle', 'bold');
   const mx2 = 255;
   content += text(mx2, my1 - 10, cfg.slug.includes('lu')?'L · U Factors':(cfg.slug.includes('cholesky')?'L · Lᵀ Factors':'Q · R Factors'), '#10b981', 11, 'start', 'bold');
   content += rect(mx2, my1, mSize, mSize, '#0f172a', '#10b981', 4);
   for(let i=0; i<4; i++){
    for(let j=0; j<4; j++){
     const fill = i>=j ? '#10b981' : '#090d16';
     content += rect(mx2 + 6 + j*30, my1 + 6 + i*30, 26, 26, fill, '#334155', 2);
    }
   }
   content += text(mx1, 265, 'Operational Complexity: FLOPs ≈ '+cfg.target+' · n³', '#f59e0b', 11, 'start');
  } else if(isIterLin){
   const k = Math.round(val);
   const cx = 220, cy = 180;
   content += `<ellipse cx="${cx}" cy="${cy}" rx="140" ry="80" fill="none" stroke="#1e293b" stroke-width="1.2"/>`;
   content += `<ellipse cx="${cx}" cy="${cy}" rx="90" ry="50" fill="none" stroke="#334155" stroke-width="1.2"/>`;
   content += `<ellipse cx="${cx}" cy="${cy}" rx="40" ry="22" fill="none" stroke="#475569" stroke-width="1.2"/>`;
   content += `<circle cx="${cx}" cy="${cy}" r="4" fill="#10b981"/>`;
   content += text(cx + 8, cy + 4, 'x*', '#10b981', 10, 'start', 'bold');
   let curX = cx - 120, curY = cy - 60;
   content += `<circle cx="${curX}" cy="${curY}" r="4" fill="#f43f5e"/>`;
   for(let step = 1; step <= Math.min(k, 8); step++){
    const factor = Math.pow(0.55, step);
    const angle = step * 1.2;
    const nextX = cx + Math.cos(angle) * 120 * factor;
    const nextY = cy + Math.sin(angle) * 60 * factor;
    content += line(curX, curY, nextX, nextY, '#38bdf8', 2);
    content += `<circle cx="${nextX}" cy="${nextY}" r="3" fill="#38bdf8"/>`;
    curX = nextX; curY = nextY;
   }
   content += text(cx - 120, 265, 'Error Norm ||e_k|| attenuated by spectral radius ρ = '+cfg.target, '#f59e0b', 11, 'start');
  } else if(isEigen){
   const k = Math.round(val);
   const ox = 220, oy = 180;
   content += `<circle cx="${ox}" cy="${oy}" r="75" fill="none" stroke="#1e293b" stroke-width="1.2"/>`;
   content += line(ox - 90, oy, ox + 90, oy, '#334155', 1);
   content += line(ox, oy - 90, ox, oy + 90, '#334155', 1);
   content += line(ox - 80, oy - 60, ox + 80, oy + 60, '#10b981', 2, '4,4');
   content += text(ox + 85, oy + 65, 'v₁ (Dominant)', '#10b981', 10, 'start', 'bold');
   const rot = Math.PI/4 * Math.pow(0.65, k);
   const vx = ox + 70 * Math.cos(rot + 0.6);
   const vy = oy + 70 * Math.sin(rot + 0.6);
   content += line(ox, oy, vx, vy, '#f43f5e', 2.5);
   content += `<circle cx="${vx}" cy="${vy}" r="4" fill="#f43f5e"/>`;
   content += text(vx + 6, vy, 'x_' + k, '#f43f5e', 10, 'start');
   content += text(80, 265, 'Spectral Dominance Ratio λ₁/λ₂ = '+cfg.target, '#f59e0b', 11, 'start');
  } else if(isInterp){
   // Interpolation curves & nodes
   const k = Math.round(val);
   const ox = 80, oy = 220, axW = 380, axH = 140;
   content += line(ox, oy, ox + axW, oy, '#475569', 1.5);
   content += line(ox, oy - axH, ox, oy + 20, '#475569', 1.5);
   content += text(ox + axW + 10, oy + 4, 'x', '#94a3b8', 11);
   content += text(ox - 8, oy - axH - 5, 'y', '#94a3b8', 11, 'end');
   // True function curve
   content += '<path d="M 80 200 Q 180 100 270 140 T 460 160" fill="none" stroke="#38bdf8" stroke-width="2"/>';
   content += text(465, 160, 'f(x)', '#38bdf8', 10);
   // Interpolation polynomial & nodes
   const numNodes = Math.min(2 + k, 8);
   for(let i=0; i<numNodes; i++){
    const nx = ox + 20 + i * ((axW - 40) / (numNodes - 1));
    const ny = 140 + Math.sin(i * 1.3) * 45;
    content += line(nx, oy, nx, ny, '#475569', 1, '2,2');
    content += `<circle cx="${nx}" cy="${ny}" r="4" fill="#f43f5e"/>`;
   }
   content += text(80, 265, 'Nodal Polynomial Interpolant P_n(x) · Degree n = '+(numNodes-1), '#f59e0b', 11);
  } else if(isQuad){
   // Numerical quadrature shaded panels
   const k = Math.round(val);
   const ox = 80, oy = 220, axW = 380, axH = 140;
   content += line(ox, oy, ox + axW, oy, '#475569', 1.5);
   content += line(ox, oy - axH, ox, oy + 20, '#475569', 1.5);
   const numPanels = Math.min(2 * Math.pow(2, k - 1), 16);
   const pw = (axW - 40) / numPanels;
   for(let i=0; i<numPanels; i++){
    const px1 = ox + 20 + i * pw;
    const px2 = px1 + pw;
    const py1 = oy - (30 + Math.sin(i*0.4)*70);
    const py2 = oy - (30 + Math.sin((i+1)*0.4)*70);
    content += `<polygon points="${px1},${oy} ${px1},${py1} ${px2},${py2} ${px2},${oy}" fill="rgba(56, 189, 248, 0.15)" stroke="#38bdf8" stroke-width="1.2"/>`;
   }
   content += '<path d="M 100 190 Q 220 90 320 130 T 440 180" fill="none" stroke="#10b981" stroke-width="2.5"/>';
   content += text(80, 265, 'Composite Quadrature Mesh: N = '+numPanels+' panels · Order α = '+cfg.target, '#f59e0b', 11);
  } else if(isMonte){
   // Monte Carlo hypercube projection & random points
   const k = Math.round(val);
   const bx = 110, by = 90, bSize = 140;
   content += rect(bx, by, bSize, bSize, '#0b1120', '#6366f1', 4);
   content += text(bx, by - 8, '5D Unit Hypercube Projection Ω = [0, 1]⁵', '#818cf8', 10);
   // Scatter sample points
   for(let i=0; i<45; i++){
    const rx = bx + 8 + ((i * 37 + k * 19) % (bSize - 16));
    const ry = by + 8 + ((i * 53 + k * 29) % (bSize - 16));
    content += `<circle cx="${rx}" cy="${ry}" r="2.5" fill="#38bdf8"/>`;
   }
   content += text(bx, 265, 'Sample Count N = '+(1000 * Math.pow(4, k-1))+' · Central Limit Rate: O(N^{-0.5})', '#f59e0b', 11);
  } else if(isFFT){
   // Cooley-Tukey FFT Butterfly Graph
   const N = Math.round(val);
   const stages = Math.min(Math.round(Math.log2(N)), 5);
   content += text(80, 95, 'Radix-2 FFT Butterfly Flow Graph (N = '+N+', log₂N = '+stages+' stages)', '#38bdf8', 11, 'start', 'bold');
   for(let s=0; s<stages; s++){
    const sx = 100 + s * 70;
    content += text(sx + 15, 120, 'Stage '+(s+1), '#94a3b8', 9);
    for(let b=0; b<4; b++){
     const by1 = 140 + b * 25;
     const by2 = by1 + 12;
     content += line(sx, by1, sx + 30, by2, '#818cf8', 1.5);
     content += line(sx, by2, sx + 30, by1, '#ec4899', 1.5);
    }
   }
   content += text(80, 265, 'Total Operational Cost: ~'+cfg.target+' N log₂(N) FLOPs', '#f59e0b', 11);
  } else {
   // Root finding coordinates
   const k = Math.round(val);
   const ox = 120, oy = 210, axW = 340, axH = 140;
   content += line(ox, oy, ox + axW, oy, '#475569', 1.5);
   content += line(ox, oy - axH, ox, oy + 40, '#475569', 1.5);
   content += text(ox + axW + 10, oy + 4, 'x', '#94a3b8', 11, 'start');
   content += text(ox - 8, oy - axH - 5, 'y', '#94a3b8', 11, 'end');

   if(cfg.slug.includes('bisection') || cfg.slug.includes('regula')){
    content += '<path d="M 140 230 Q 280 210 380 150 T 450 60" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';
    const rootX = 350;
    content += line(rootX, oy - 15, rootX, oy + 15, '#10b981', 2);
    content += text(rootX, oy + 28, 'Root x*', '#10b981', 10, 'middle', 'bold');
    const span = Math.max(10, 140 / Math.pow(1.6, k - 1));
    const aX = rootX - span * 0.7;
    const bX = rootX + span * 0.5;
    content += rect(aX, oy - 110, bX - aX, 130, 'rgba(99, 102, 241, 0.15)', '#6366f1', 2);
    content += line(aX, oy - 110, aX, oy + 20, '#818cf8', 2);
    content += line(bX, oy - 110, bX, oy + 20, '#818cf8', 2);
    content += text(aX, oy + 32, 'a_' + k, '#818cf8', 10, 'middle');
    content += text(bX, oy + 32, 'b_' + k, '#818cf8', 10, 'middle');
   } else if(cfg.slug.includes('fixed-point')){
    content += line(ox, oy, ox + 200, oy - 130, '#64748b', 1.5, '4,4');
    content += '<path d="M 120 180 Q 220 165 330 130" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';
    let cx = ox + 40, cy = oy;
    for(let i = 1; i <= Math.min(k, 5); i++){
     const nextY = oy - (35 + i * 18);
     const nextX = ox + (35 + i * 18);
     content += line(cx, cy, cx, nextY, '#f43f5e', 2);
     content += line(cx, nextY, nextX, nextY, '#f43f5e', 2);
     cx = nextX; cy = nextY;
    }
   } else {
    content += '<path d="M 140 240 Q 260 200 370 120 T 450 50" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';
    const rootX = 360;
    content += line(rootX, oy - 20, rootX, oy + 20, '#10b981', 2);
    content += text(rootX, oy + 30, 'Root x*', '#10b981', 10, 'middle', 'bold');
    const err = Math.max(2, 90 / Math.pow(2.0, k - 1));
    const curX = rootX + err;
    content += line(curX, oy, curX, 100, '#f59e0b', 1.8, '3,3');
    content += `<circle cx="${curX}" cy="100" r="5" fill="#f59e0b"/>`;
    content += text(curX, oy + 16, 'x_' + k, '#f59e0b', 10, 'middle');
   }
  }

  // Telemetry box on right
  content += rect(490, 80, 170, 180, '#0b1120', '#1e293b', 6);
  content += text(505, 105, 'COMPUTATION TELEMETRY', '#94a3b8', 9, 'start', 'bold');
  content += text(505, 130, cfg.shortInput + ': ' + val, '#cbd5e1', 11);
  content += text(505, 155, 'Target: ' + cfg.target, '#38bdf8', 11);
  content += text(505, 180, 'Metric: ' + cfg.targetName, '#cbd5e1', 10);
  content += text(505, 205, 'Status: Active', '#10b981', 11);
  content += text(505, 230, 'Mode: ' + currentSimMode.toUpperCase(), '#f59e0b', 11);

 } else if(currentSimMode==='compare'){
  content += rect(40, 25, 640, 270, '#090d16', '#312e81', 8);
  content += text(60, 52, 'COMPUTATIONAL COMPLEXITY & ASYMPTOTIC SPEED', '#818cf8', 12, 'start', 'bold');
  content += text(60, 70, 'Comparison across algorithmic paradigms in numerical analysis', '#94a3b8', 11);

  const methods = isMatrix ? [
   { name: 'Direct QR (Householder / Gram-Schmidt)', col: '#ec4899', rate: 'C ≈ 4/3 n³ FLOPs', speed: 1 },
   { name: 'Gaussian Elimination / LU Doolittle', col: '#10b981', rate: 'C ≈ 2/3 n³ FLOPs', speed: 2 },
   { name: 'Cholesky Factorization (Symmetric PD)', col: '#38bdf8', rate: 'C ≈ 1/3 n³ FLOPs (2x speedup)', speed: 4 },
   { name: 'Banded / Sparse Iterative Solvers', col: '#f59e0b', rate: 'O(k · n²) FLOPs', speed: 5 }
  ] : (isQuad || isMonte) ? [
   { name: 'Gauss-Legendre Quadrature (3-pt)', col: '#ec4899', rate: 'O(h⁶) Convergence (Fastest)', speed: 5 },
   { name: 'Simpson 1/3 & 3/8 Rules', col: '#10b981', rate: 'O(h⁴) Convergence (Parabolic)', speed: 4 },
   { name: 'Composite Trapezoidal Rule', col: '#38bdf8', rate: 'O(h²) Convergence (Linear Panels)', speed: 2 },
   { name: 'Monte Carlo Multidimensional', col: '#f59e0b', rate: 'O(N^{-1/2}) Dimension Independent', speed: 1 }
  ] : isFFT ? [
   { name: 'Cooley-Tukey Radix-2 FFT', col: '#10b981', rate: '5 N log₂(N) FLOPs', speed: 5 },
   { name: 'Split-Radix FFT Algorithm', col: '#38bdf8', rate: '4 N log₂(N) FLOPs', speed: 5 },
   { name: 'Chirp-Z Transform / Bluestein', col: '#f59e0b', rate: 'O(N log N) Arbitrary Primes', speed: 4 },
   { name: 'Naive Matrix-Vector DFT', col: '#ec4899', rate: '8 N² FLOPs (Untractable)', speed: 1 }
  ] : isInterp ? [
   { name: 'Cubic Spline (Natural / Clamped)', col: '#10b981', rate: 'O(h⁴) Convergence (C² Smooth)', speed: 5 },
   { name: 'Chebyshev Minimax Polynomial', col: '#38bdf8', rate: 'Geometric Attenuation (No Runge)', speed: 4 },
   { name: 'Least-Squares Normal Equations', col: '#f59e0b', rate: 'Noise Filtering BLUE Estimator', speed: 3 },
   { name: 'Uniform Equidistant Lagrange', col: '#ec4899', rate: 'Runge Divergence for High Degree', speed: 1 }
  ] : [
   { name: 'Halley Method / Cubic Acceleration', col: '#ec4899', rate: 'α = 3.000 (Cubic)', speed: 5 },
   { name: 'Newton-Raphson / Bairstow / Steffensen', col: '#10b981', rate: 'α = 2.000 (Quadratic)', speed: 4 },
   { name: 'Brent-Dekker / Muller / Secant', col: '#38bdf8', rate: 'α = 1.618 - 1.839 (Superlinear)', speed: 3 },
   { name: 'Bisection & Banach Contraction', col: '#f59e0b', rate: 'α = 1.000 (Linear, C = 0.5)', speed: 1 }
  ];

  methods.forEach((m, idx)=>{
   const yPos = 100 + idx * 42;
   content += rect(60, yPos, 600, 34, '#0f172a', '#1e293b', 4);
   content += text(75, yPos + 21, m.name, '#e2e8f0', 11, 'start', 'bold');
   content += text(340, yPos + 21, m.rate, m.col, 11, 'start');
   const barW = Math.max(20, m.speed * 40);
   content += rect(470, yPos + 8, barW, 18, m.col, 'none', 3);
   content += text(480 + barW, yPos + 21, m.speed + 'x throughput', '#94a3b8', 10, 'start');
  });

  content += text(60, 280, 'Selected Method: ' + cfg.targetName + ' = ' + cfg.target, '#f43f5e', 11, 'start', 'bold');

 } else {
  content += rect(40, 25, 640, 270, '#090d16', '#312e81', 8);
  content += text(60, 52, 'NUMERICAL STABILITY & CONDITIONING SANDBOX', '#818cf8', 12, 'start', 'bold');
  content += text(60, 70, 'Explore perturbation dynamics, condition numbers, and floating-point stability', '#94a3b8', 11);

  const boxW = 580, boxH = 120;
  content += rect(70, 95, boxW, boxH, '#0b1120', '#334155', 6);
  content += line(70, 155, 70 + boxW, 155, '#475569', 1.5);

  for(let x = 80; x < 640; x += 15){
   const wave = Math.sin((x + val * 20) * 0.05) * 40;
   content += line(x, 155, x, 155 - wave, '#6366f1', 1.2);
   content += `<circle cx="${x}" cy="${155 - wave}" r="2" fill="#38bdf8"/>`;
  }

  content += text(85, 120, 'Numerical Stability Landscape & Error Propagation', '#38bdf8', 10, 'start', 'bold');
  content += text(85, 200, isMatrix ? 'Relative Error Bound: ||δx||/||x|| ≤ κ(A) · ||δb||/||b||' : (isQuad || isInterp) ? 'Asymptotic Error Truncation: E ≤ C · h^α' : 'Lipschitz Bound L ≤ ' + (1.0 / Math.max(1, val)).toFixed(3) + ' · Stability: Convergent', '#10b981', 11);

  content += rect(70, 230, 280, 48, '#0f172a', '#1e293b', 4);
  content += text(85, 250, 'Machine Epsilon ε_mach', '#94a3b8', 10);
  content += text(85, 268, '2.220446 × 10⁻¹⁶ (IEEE 754 64-bit)', '#f59e0b', 11, 'start', 'bold');

  content += rect(370, 230, 280, 48, '#0f172a', '#1e293b', 4);
  content += text(385, 250, 'Target Parameter', '#94a3b8', 10);
  content += text(385, 268, cfg.target + ' (' + cfg.targetName + ')', '#ec4899', 11, 'start', 'bold');
 }

 svg.innerHTML = content;
}

update();
renderResults();
