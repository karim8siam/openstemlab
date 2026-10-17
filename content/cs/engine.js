'use strict';
const cfg=JSON.parse(document.getElementById('labConfig').textContent),model=window.CSModels,$=id=>document.getElementById(id);
const fmt=(v,n=4)=>Math.abs(v)>0&&(Math.abs(v)<.001||Math.abs(v)>=1e6)?v.toExponential(3):v.toFixed(n);
let rows=[],measurement=null,busy=false,paused=matchMedia('(prefers-reduced-motion: reduce)').matches,clearPending=false;
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
 $('liveState').textContent='Ready to execute '+cfg.shortInput+' benchmark.';
 message('Adjust '+cfg.shortInput+' n, then execute benchmark.');
 draw(performance.now());
}

$('independent').addEventListener('input',()=>{$('independentNumber').value=$('independent').value;update();});
$('independentNumber').addEventListener('input',()=>{const v=+$('independentNumber').value;if($('independentNumber').value!==''&&Number.isFinite(v)&&v>=cfg.min&&v<=cfg.max){$('independent').value=v;update();}});
$('independentNumber').addEventListener('change',()=>{const v=+$('independentNumber').value;if(!Number.isFinite(v)||v<cfg.min||v>cfg.max){$('independentNumber').value=$('independent').value;message('Use a value between '+cfg.min+' and '+cfg.max+' '+cfg.inputUnit+'.',true);return;}$('independent').value=v;$('independentNumber').value=$('independent').value;update();});

$('pauseMotion').hidden=true;
$('resetApparatus').onclick=()=>{if(busy)return;$('independent').value=cfg.initial;$('independentNumber').value=cfg.initial;update();message('Benchmark environment reset. Your notebook is kept.');};

$('measure').onclick=async()=>{
 if(busy)return;
 const p=params(),prediction=model.predict(cfg.slug,p.input);
 if(!prediction.valid){message('Select a valid '+cfg.shortInput+' between '+cfg.min+' and '+cfg.max+' '+cfg.inputUnit+'.',true);return;}
 busy=true;$('measure').disabled=true;$('recordReading').disabled=true;$('independent').disabled=true;$('independentNumber').disabled=true;
 message('Running algorithmic benchmark on n = '+p.input+' '+cfg.inputUnit+'…');
 await new Promise(resolve=>setTimeout(resolve,400));
 const raw=prediction.raw;
 measurement=model.reading(cfg.slug,p.input,raw);
 busy=false;$('independent').disabled=false;$('independentNumber').disabled=false;$('measure').disabled=false;$('recordReading').disabled=false;
 $('readingValue').textContent=raw.toFixed(cfg.rawDecimals)+' '+cfg.rawUnit;
 $('liveState').textContent='Benchmark observation ready to record.';
 message('Benchmark completed: '+raw+' '+cfg.rawUnit+' for n = '+p.input+'. Record in notebook.');
};

$('recordReading').onclick=()=>{
 if(!measurement)return;
 if(rows.length>=100){message('Notebook full. Export readings or clear the notebook.',true);return;}
 rows.push({...measurement});
 measurement=null;
 $('recordReading').disabled=true;
 persist();
 message('Observation '+rows.length+' recorded. Change '+cfg.shortInput+' for the next benchmark.');
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
  $('fitSummary').innerHTML='<strong>'+fmt(result.value*cfg.resultScale,cfg.resultDecimals)+' '+cfg.resultUnit+'</strong><p>Estimated '+cfg.target+'<br>Gradient: '+fmt(f.m)+'<br>Intercept: '+fmt(f.b)+'<br>R²: '+f.r2.toFixed(5)+'<br>Difference from theoretical bound: '+pct.toFixed(3)+'%<br>Fit standard error: '+fmt(result.se*cfg.resultScale)+' '+cfg.resultUnit+'</p><p>Deterministic algorithmic counts exhibit ideal asymptotic bounds.</p>';
 } else {
  $('fitSummary').innerHTML='<p>Record at least three distinct '+cfg.shortInput+' values to fit an asymptotic line and calculate '+cfg.target+'.</p>';
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
 for(let i=0;i<=4;i++){
  const x=xmin+i*(xmax-xmin)/4,y=ymin+i*(ymax-ymin)/4;
  svg+='<line x1="'+left+'" y1="'+py(y)+'" x2="'+right+'" y2="'+py(y)+'" stroke="#dbe5eb"/><text x="'+(left-9)+'" y="'+(py(y)+4)+'" text-anchor="end" font-size="10" fill="#5a7687">'+fmt(y,2)+'</text><text x="'+px(x)+'" y="300" text-anchor="middle" font-size="10" fill="#5a7687">'+fmt(x,2)+'</text>';
 }
 svg+='<path d="M'+left+' '+top+'V'+bottom+'H'+right+'" stroke="#8ba5b5" fill="none"/><text x="335" y="332" text-anchor="middle" fill="#2b546b" font-size="12">'+cfg.xAxis+'</text><text transform="translate(15 160) rotate(-90)" text-anchor="middle" fill="#2b546b" font-size="12">'+cfg.yAxis+'</text>';
 if(f){
  const points=[];
  for(let i=0;i<=100;i++){
   const x=xmin+i*(xmax-xmin)/100,y=(f.m*x/cfg.xScale+f.b)*cfg.yScale;
   if(y>=ymin&&y<=ymax)points.push(px(x)+','+py(y));
  }
  svg+='<polyline points="'+points.join(' ')+'" stroke="#1e3e52" stroke-width="2" fill="none"/>';
 }
 rows.forEach(r=>svg+='<circle cx="'+px(r.x*cfg.xScale)+'" cy="'+py(r.y*cfg.yScale)+'" r="4.8" fill="#c05621"><title>n = '+r.input+' ('+r.raw+' comparisons)</title></circle>');
 if(!rows.length)svg+='<text x="330" y="155" text-anchor="middle" fill="#7e9bab" font-size="13">Your benchmark observations will appear here.</text>';
 $('labPlot').innerHTML=svg;
}

$('downloadReadings').onclick=()=>{
 if(!rows.length)return;
 const csv=[['experiment',cfg.shortInput.replace(/\s+/g,'_')+'_n','observed_comparisons',cfg.xAxis,cfg.yAxis],...rows.map(r=>[cfg.slug,r.input,r.raw,r.x,r.y])].map(row=>row.join(',')).join('\r\n');
 const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'})),a=document.createElement('a');
 a.href=url;a.download=cfg.slug+'-observations.csv';a.click();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
};

$('clearReadings').onclick=()=>{
 if(!clearPending){clearPending=true;$('clearReadings').textContent='Confirm clear';setTimeout(()=>{clearPending=false;$('clearReadings').textContent='Clear notebook';},4000);return;}
 rows=[];clearPending=false;$('clearReadings').textContent='Clear notebook';persist();message('Notebook cleared.');
};

$('checkEstimate').onclick=()=>{
 const f=model.fit(rows),answer=+$('studentEstimate').value;
 if(!f){$('estimateFeedback').textContent='Collect at least three distinct array sizes first.';return;}
 if(!$('studentEstimate').value||!Number.isFinite(answer)||answer<=0){$('estimateFeedback').textContent='Enter a positive numerical estimate in '+cfg.resultUnit+'.';return;}
 const expected=model.estimate(cfg.slug,f).value*cfg.resultScale;
 $('estimateFeedback').textContent=Math.abs(answer-expected)/expected<.02?'Your calculation agrees with the notebook fit within 2%! Asymptotic gradient confirmed.':'Recheck units and the slope conversion. The fit gives '+fmt(expected,cfg.resultDecimals)+' '+cfg.resultUnit+'.';
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

function drawComparativeSim(t,p,v,ink,soft,orange){
 const cX=50,cY=45,cW=380,cH=230;
 let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
 const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

 if(cfg.slug==='quadratic-sorting-algorithms'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'QUADRATIC SORTING COMPARATIVE BENCHMARK (n = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  const c_worst=Math.round(n*(n-1)/2);
  const c_avg=Math.round(n*(n-1)/4);
  const c_best_ins=n-1;
  const s_bubble_worst=c_worst;
  const s_select_worst=n-1;
  const s_ins_worst=c_worst;

  const algos=[
   {name:'Bubble Sort (Worst-Case)',col:'#ef4444',ops:c_worst,writes:s_bubble_worst*3,scale:'O(n²)',desc:'Max comparisons & high write churn'},
   {name:'Selection Sort (All Cases)',col:'#38bdf8',ops:c_worst,writes:s_select_worst*2,scale:'Θ(n²)',desc:'Fixed comparisons, minimum O(n) writes'},
   {name:'Insertion Sort (Worst-Case)',col:'#f97316',ops:c_worst,writes:s_ins_worst,scale:'O(n²)',desc:'Reverse order maximum shifts'},
   {name:'Insertion Sort (Average-Case)',col:'#a855f7',ops:c_avg,writes:Math.round(s_ins_worst/2),scale:'Θ(n²)',desc:'Random array expected half-distance'},
   {name:'Insertion Sort (Best-Case)',col:'#10b981',ops:c_best_ins,writes:0,scale:'O(n)',desc:'Pre-sorted adaptive early termination'}
  ];

  algos.forEach((item,idx)=>{
   const rowY=cY+16+idx*42;
   svg+='<text x="'+(cX+15)+'" y="'+(rowY+12)+'" fill="#dcebf2" font-size="8.5" font-weight="bold">'+item.name+'</text>';
   svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+12)+'" text-anchor="end" fill="'+item.col+'" font-size="8.5" font-family="monospace" font-weight="bold">'+item.ops+' comp | '+item.writes+' wr ('+item.scale+')</text>';
   
   const barX=cX+15,barY=rowY+16,barMaxW=cW-30;
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="7" rx="2" fill="#16242c"/>';
   const frac=Math.min(1.0,item.ops/(70*69/2));
   const fillW=Math.max(4,frac*barMaxW);
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="7" rx="2" fill="'+item.col+'"/>';
  });

  const bX=460,bY=45,bW=220,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">MEMORY WRITE REDUCTION</text>';
  const writeRatio=((s_bubble_worst*3)/(Math.max(1,s_select_worst*2))).toFixed(1);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+writeRatio+'×</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#dcebf2" font-size="10">Selection vs Bubble</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">NON-VOLATILE MEMORY WEAR</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="15" font-family="monospace" font-weight="bold">O(n) Swaps Max</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">Selection sort preserves Flash/EEPROM endurance</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">ASYMPTOTIC RELATIONS</text>';
  svg+=text(bX+bW/2,bY+180,'C(n) = n(n − 1) / 2 = Θ(n²)','#38bdf8',11);
  svg+=text(bX+bW/2,bY+202,'Insertion Best Case: C(n) = n − 1 = Θ(n)',orange,9);
  svg+=text(360,305,'Comparative Invariant: Selection minimizes physical writes · Insertion adapts to existing order',soft,10);
  return svg;
 }

 const n=p.input;
 const c_lin_worst=n;
 const c_lin_avg=Math.round((n+1)/2);
 const c_bin_worst=Math.floor(Math.log2(n))+1;
 const c_bin_avg=Math.max(1,Math.round(Math.log2(n)-1));
 const c_int_avg=Math.max(1,Math.round(Math.log2(Math.max(2,Math.log2(n)))));

 const algos=[
  {name:'Linear Search (Worst-Case)',col:'#ef4444',count:c_lin_worst,scale:'O(n)',desc:'Sequential scan visiting all '+n+' elements'},
  {name:'Linear Search (Average-Case)',col:'#f97316',count:c_lin_avg,scale:'Θ(n)',desc:'Expected (n+1)/2 matches = '+c_lin_avg+' comparisons'},
  {name:'Binary Search (Worst-Case)',col:'#38bdf8',count:c_bin_worst,scale:'O(log₂ n)',desc:'Bisection halving search space: '+c_bin_worst+' comparisons'},
  {name:'Binary Search (Average-Case)',col:'#10b981',count:c_bin_avg,scale:'Θ(log₂ n)',desc:'Average successful match = '+c_bin_avg+' comparisons'},
  {name:'Interpolation Search (Avg)',col:'#a855f7',count:c_int_avg,scale:'O(log log n)',desc:'Proportional probe on uniform keys = '+c_int_avg+' comparisons'}
 ];

 svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
 svg+=text(cX+cW/2,cY-14,'SEARCH ALGORITHM COMPARATIVE BENCHMARK (n = '+p.input+')','#e2f0f8',11);

 algos.forEach((item,idx)=>{
  const rowY=cY+20+idx*40;
  svg+='<text x="'+(cX+15)+'" y="'+(rowY+14)+'" fill="#dcebf2" font-size="9" font-weight="bold">'+item.name+'</text>';
  svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+14)+'" text-anchor="end" fill="'+item.col+'" font-size="9" font-family="monospace" font-weight="bold">'+item.count+' ops ('+item.scale+')</text>';
  
  const barX=cX+15,barY=rowY+18,barMaxW=cW-30;
  svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="8" rx="2" fill="#16242c"/>';
  const frac=Math.min(1.0,Math.log10(item.count+1)/Math.log10(4096+1));
  const fillW=Math.max(4,frac*barMaxW);
  svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="8" rx="2" fill="'+item.col+'"/>';
 });

 const bX=460,bY=45,bW=220,bH=230;
 svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">EFFICIENCY RATIO (SPEEDUP)</text>';
 const speedup=(c_lin_worst/c_bin_worst).toFixed(1);
 svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+speedup+'×</text>';
 svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#dcebf2" font-size="10">Binary vs Linear</text>';
 svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">INFORMATION ENTROPY</text>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">'+Math.log2(n).toFixed(2)+' bits</text>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">1 comparison eliminates 1 bit of uncertainty</text>';
 svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">ASYMPTOTIC EQUATION</text>';
 svg+=text(bX+bW/2,bY+180,'T(n) = T(n/2) + O(1)','#38bdf8',11);
 svg+=text(bX+bW/2,bY+202,'⟹ T(n) = Θ(log₂ n) (Master Thm)',orange,9.5);
 svg+=text(360,305,'Information-Theoretic Bound: L >= n + 1 ⟹ Height h >= ⌈log₂(n+1)⌉ = Ω(log n)',soft,10);
 return svg;
}

function drawDynamicSandbox(t,p,v,ink,soft,orange){
 const cX=45,cY=45,cW=400,cH=230;
 let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
 const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

 if(cfg.slug==='quadratic-sorting-algorithms'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'KENDALL-TAU INVERSION VECTOR & PAIR MATRIX (n = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  const totalPairs=Math.round(n*(n-1)/2);
  const avgInversions=Math.round(totalPairs/2);

  const gridSize=Math.min(9,n);
  const cellW=32,cellH=18;
  const gridX=cX+25,gridY=cY+22;

  svg+='<text x="'+gridX+'" y="'+(gridY-5)+'" fill="#7e9bab" font-size="8" font-weight="bold">PAIR INVERSION GRID (SAMPLE UPPER TRIANGLE i < j)</text>';
  for(let i=0;i<gridSize;i++){
   for(let j=i+1;j<gridSize;j++){
    const isInverted=(i+j)%2===1||(i*3+j)%5===0;
    const px=gridX+(j-1)*(cellW+4);
    const py=gridY+i*(cellH+4);
    svg+='<rect x="'+px+'" y="'+py+'" width="'+cellW+'" height="'+cellH+'" rx="2" fill="'+(isInverted?'#ef444433':'#10b98122')+'" stroke="'+(isInverted?'#ef4444':'#10b981')+'" stroke-width="1"/>';
    svg+='<text x="'+(px+cellW/2)+'" y="'+(py+cellH/2+3)+'" text-anchor="middle" fill="'+(isInverted?'#fca5a5':'#6ee7b7')+'" font-size="7" font-family="monospace">'+(isInverted?'INV':'OK')+'</text>';
   }
  }

  svg+='<rect x="'+(cX+15)+'" y="'+(cY+cH-38)+'" width="'+(cW-30)+'" height="30" rx="4" fill="#0e1a22" stroke="#1e3340"/>';
  svg+='<text x="'+(cX+25)+'" y="'+(cY+cH-20)+'" fill="#38bdf8" font-size="8.5" font-family="monospace">Swap Invariant: Adjacent swap changes inversions I(A) by exactly ±1</text>';

  const bX=470,bY=45,bW=210,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">TOTAL PAIR SPACE n(n − 1)/2</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+totalPairs+'</text>';
  svg+='<text x="'+(bX+110)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="11">pairs</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+68)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+68)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+88)+'" fill="#7e9bab" font-size="9">EXPECTED INVERSIONS E[I(A)]</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+112)+'" fill="'+ink+'" font-size="17" font-family="monospace" font-weight="bold">'+avgInversions+'</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+108)+'" fill="#8ba5b5" font-size="9">n(n − 1) / 4</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+124)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+124)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+142)+'" fill="#7e9bab" font-size="9">LOWER BOUND THEOREM</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+166)+'" fill="#fde047" font-size="14" font-family="monospace" font-weight="bold">Ω(n²) swaps</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#8ba5b5" font-size="8">Any adjacent-swap algorithm requires Ω(n²)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+198)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+198)+'" stroke="#1e3340"/>';

  svg+=text(bX+bW/2,bY+218,'Cayley Distance: at most n − 1 arbitrary swaps',orange,8.5);
  svg+=text(360,305,'Mathematical Theorem: E[I] = n(n − 1)/4 ⟹ Average adjacent transpositions = Ω(n²)',soft,10);
  return svg;
 }

 svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
 svg+=text(cX+cW/2,cY-14,'BINARY SEARCH DECISION TREE TRAVERSAL','#e2f0f8',11);

 const nodes=[
  {id:'mid0',label:'mid=n/2',x:cX+cW/2,y:cY+35,col:orange},
  {id:'l1a',label:'< K',x:cX+cW/4,y:cY+85,col:'#38bdf8'},
  {id:'l1b',label:'> K',x:cX+3*cW/4,y:cY+85,col:'#38bdf8'},
  {id:'l2a',label:'L.half',x:cX+cW/8,y:cY+135,col:ink},
  {id:'l2b',label:'R.half',x:cX+3*cW/8,y:cY+135,col:ink},
  {id:'l2c',label:'L.half',x:cX+5*cW/8,y:cY+135,col:ink},
  {id:'l2d',label:'R.half',x:cX+7*cW/8,y:cY+135,col:ink}
 ];

 svg+='<line x1="'+nodes[0].x+'" y1="'+nodes[0].y+'" x2="'+nodes[1].x+'" y2="'+nodes[1].y+'" stroke="'+orange+'" stroke-width="2"/>';
 svg+='<line x1="'+nodes[0].x+'" y1="'+nodes[0].y+'" x2="'+nodes[2].x+'" y2="'+nodes[2].y+'" stroke="#334d5c" stroke-width="1.5" stroke-dasharray="3 3"/>';
 svg+='<line x1="'+nodes[1].x+'" y1="'+nodes[1].y+'" x2="'+nodes[3].x+'" y2="'+nodes[3].y+'" stroke="#334d5c" stroke-width="1.5" stroke-dasharray="3 3"/>';
 svg+='<line x1="'+nodes[1].x+'" y1="'+nodes[1].y+'" x2="'+nodes[4].x+'" y2="'+nodes[4].y+'" stroke="'+orange+'" stroke-width="2"/>';
 svg+='<line x1="'+nodes[2].x+'" y1="'+nodes[2].y+'" x2="'+nodes[5].x+'" y2="'+nodes[5].y+'" stroke="#334d5c" stroke-width="1.5" stroke-dasharray="3 3"/>';
 svg+='<line x1="'+nodes[2].x+'" y1="'+nodes[2].y+'" x2="'+nodes[6].x+'" y2="'+nodes[6].y+'" stroke="#334d5c" stroke-width="1.5" stroke-dasharray="3 3"/>';

 nodes.forEach(n=>{
  svg+='<circle cx="'+n.x+'" cy="'+n.y+'" r="16" fill="#0f1f28" stroke="'+n.col+'" stroke-width="2"/>';
  svg+='<text x="'+n.x+'" y="'+(n.y+4)+'" text-anchor="middle" fill="#dcebf2" font-size="7.5" font-weight="bold">'+n.label+'</text>';
 });

 svg+='<rect x="'+(cX+15)+'" y="'+(cY+cH-42)+'" width="'+(cW-30)+'" height="32" rx="4" fill="#0e1a22" stroke="#1e3340"/>';
 svg+='<text x="'+(cX+25)+'" y="'+(cY+cH-22)+'" fill="#38bdf8" font-size="8.5" font-family="monospace">Path Traversed: Root (Depth 0) ⟶ Right (Depth 1) ⟶ Search Bisection Path</text>';

 const bX=470,bY=45,bW=210,bH=230;
 svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">DECISION TREE HEIGHT (h)</text>';
 const h_bound=Math.ceil(Math.log2(p.input+1));
 svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">'+h_bound+'</text>';
 svg+='<text x="'+(bX+65)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="11">levels</text>';
 svg+='<line x1="'+(bX+15)+'" y1="'+(bY+68)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+68)+'" stroke="#1e3340"/>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+88)+'" fill="#7e9bab" font-size="9">TOTAL EXTERNAL LEAVES (L)</text>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+112)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">'+(p.input+1)+'</text>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+128)+'" fill="#8ba5b5" font-size="8">n match leaves + (n+1) failure leaves</text>';
 svg+='<line x1="'+(bX+15)+'" y1="'+(bY+142)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+142)+'" stroke="#1e3340"/>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+160)+'" fill="#7e9bab" font-size="9">BITWISE HALVING STRIDE</text>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#38bdf8" font-size="13" font-family="monospace" font-weight="bold">stride = ⌊n / 2ᵏ⌋</text>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+202)+'" fill="#8ba5b5" font-size="8">Shrinks to 0 in ⌊log₂ n⌋ + 1 iterations</text>';
 svg+=text(360,305,'Decision Tree Invariant: Leaves L <= 2^h ⟹ Height h >= ⌈log₂(n + 1)⌉ = Ω(log n)',soft,10);
 return svg;
}

function draw(t){
 const p=params(),v=model.predict(cfg.slug,p.input);
 const ink='#38bdf8',soft='#7e9bab',orange='#f97316';
 if(currentSimMode==='compare'){$('apparatusDiagram').innerHTML=drawComparativeSim(t,p,v,ink,soft,orange);return;}
 if(currentSimMode==='sandbox'){$('apparatusDiagram').innerHTML=drawDynamicSandbox(t,p,v,ink,soft,orange);return;}

 if(cfg.slug==='quadratic-sorting-algorithms'){
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  const n=p.input;
  const pairSpace=n*(n-1);
  const c_total=v.raw;

  svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+=text(240,24,'Virtual Memory Buffer & Quadratic Sorting Workbench');

  const numBars=14;
  const barW=22;
  const startX=55,baseY=195,maxBarH=110;
  const sortedCount=Math.floor(numBars/3);
  const scanIdx=sortedCount+3;
  const minIdx=sortedCount+1;

  svg+='<text x="55" y="60" fill="#7e9bab" font-size="8.5" font-weight="bold">ARRAY BUFFER A[0 .. '+(n-1)+'] (SAMPLE WINDOW)</text>';
  svg+='<text x="430" y="60" text-anchor="end" fill="'+orange+'" font-size="8.5" font-weight="bold">PASS i = '+Math.floor(n/3)+' / '+(n-1)+'</text>';

  const sampleKeys=[12, 28, 45, 92, 63, 31, 74, 55, 88, 19, 67, 81, 40, 99];
  for(let i=0;i<numBars;i++){
   const bx=startX+i*(barW+4);
   const h=Math.round((sampleKeys[i]/100)*maxBarH);
   const by=baseY-h;
   const isSorted=i<sortedCount;
   const isScanning=i===scanIdx;
   const isMin=i===minIdx;

   let fillCol='#1e3e52',strokeCol='#334d5c';
   if(isSorted){fillCol='#065f46';strokeCol='#10b981';}
   else if(isMin){fillCol='#0c4a6e';strokeCol='#38bdf8';}
   else if(isScanning){fillCol='#7c2d12';strokeCol=orange;}

   svg+='<rect x="'+bx+'" y="'+by+'" width="'+barW+'" height="'+h+'" rx="2" fill="'+fillCol+'" stroke="'+strokeCol+'" stroke-width="'+(isScanning||isMin?2:1)+'"/>';
   svg+='<text x="'+(bx+barW/2)+'" y="'+(by-5)+'" text-anchor="middle" fill="'+(isScanning?orange:isMin?'#38bdf8':isSorted?'#34d399':'#8ba5b5')+'" font-size="7.5" font-family="monospace">'+sampleKeys[i]+'</text>';
   svg+='<text x="'+(bx+barW/2)+'" y="'+(baseY+12)+'" text-anchor="middle" fill="#5a7687" font-size="7">['+i+']</text>';
  }

  const scanPx=startX+scanIdx*(barW+4)+barW/2;
  svg+='<polygon points="'+scanPx+','+(baseY+16)+' '+(scanPx-4)+','+(baseY+24)+' '+(scanPx+4)+','+(baseY+24)+'" fill="'+orange+'"/>';
  svg+='<text x="'+scanPx+'" y="'+(baseY+33)+'" text-anchor="middle" fill="'+orange+'" font-size="7.5" font-weight="bold">j (scan)</text>';

  const minPx=startX+minIdx*(barW+4)+barW/2;
  svg+='<polygon points="'+minPx+','+(baseY+16)+' '+(minPx-4)+','+(baseY+24)+' '+(minPx+4)+','+(baseY+24)+'" fill="#38bdf8"/>';
  svg+='<text x="'+minPx+'" y="'+(baseY+33)+'" text-anchor="middle" fill="#38bdf8" font-size="7.5" font-weight="bold">min_idx</text>';

  const sortedPx=startX+(sortedCount-1)*(barW+4)+barW;
  svg+='<line x1="'+sortedPx+'" y1="70" x2="'+sortedPx+'" y2="'+baseY+'" stroke="#10b981" stroke-width="1.5" stroke-dasharray="3 3"/>';
  svg+='<text x="'+(startX+sortedCount*(barW+4)/2)+'" y="78" text-anchor="middle" fill="#10b981" font-size="7.5" font-weight="bold">Sorted Prefix</text>';

  const regX=55,regY=235,regW=370,regH=32;
  svg+='<rect x="'+regX+'" y="'+regY+'" width="'+regW+'" height="'+regH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+14)+'" fill="#38bdf8" font-size="8" font-family="monospace">ALU Comparator: A[j] < A[min] ? ⟹ Evaluating Pair ('+scanIdx+', '+minIdx+')</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+26)+'" fill="#8ba5b5" font-size="7.5">Inner comparisons remaining in pass i: '+(n - 1 - Math.floor(n/3))+' comparisons</text>';

  const bX=465,bY=38,bW=220,bH=235;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">ARRAY SIZE (n)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+n+'</text>';
  svg+='<text x="'+(bX+85)+'" y="'+(bY+46)+'" fill="#8ba5b5" font-size="11">elements</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+64)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+64)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+82)+'" fill="#7e9bab" font-size="9">PAIR SPACE n(n − 1)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+106)+'" fill="'+ink+'" font-size="18" font-family="monospace" font-weight="bold">'+pairSpace+'</text>';
  svg+='<text x="'+(bX+100)+'" y="'+(bY+104)+'" fill="#8ba5b5" font-size="10">pairs</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+120)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+120)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+138)+'" fill="#7e9bab" font-size="9">KEY COMPARISONS C(n)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+164)+'" fill="#fde047" font-size="20" font-family="monospace" font-weight="bold">'+c_total+'</text>';
  svg+='<text x="'+(bX+85)+'" y="'+(bY+160)+'" fill="#8ba5b5" font-size="9">n(n − 1) / 2</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+178)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+178)+'" stroke="#1e3340"/>';

  svg+=text(bX+bW/2,bY+200,'C = a_quad · n(n − 1) + b',ink,10);
  svg+=text(bX+bW/2,bY+218,'Scaling Gradient: a = 0.5000 comp/pair',orange,9);

  svg+=text(360,305,'Algorithmic Complexity: C(n) = n(n − 1) / 2 = Θ(n²) · In-Place Space: O(1) Auxiliary',soft,10);
  $('apparatusDiagram').innerHTML=svg;
  return;
 }

 let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
 const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

 const n=p.input;
 const log2n=Math.log2(n);
 const c_max=v.raw;

 svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
 svg+=text(240,24,'Virtual Memory Array & Binary Search Execution Bench');

 const numCells=12;
 const cellW=28,cellH=38;
 const startX=55,startY=110;
 const midIdx=Math.floor(numCells/2);

 svg+='<text x="55" y="60" fill="#7e9bab" font-size="8.5" font-weight="bold">ARRAY BUFFER A[0 .. '+(n-1)+'] (SAMPLE WINDOW)</text>';
 svg+='<text x="430" y="60" text-anchor="end" fill="'+orange+'" font-size="8.5" font-weight="bold">TARGET KEY K = '+(2*n+10)+' (ABSENT)</text>';

 for(let i=0;i<numCells;i++){
  const cx=startX+i*(cellW+4);
  const isMid=i===midIdx;
  const isLower=i<midIdx;
  const fillCol=isMid?'#1e3e52':isLower?'#111c24':'#162a36';
  const strokeCol=isMid?orange:isLower?'#334d5c':'#38bdf8';
  svg+='<rect x="'+cx+'" y="'+startY+'" width="'+cellW+'" height="'+cellH+'" rx="3" fill="'+fillCol+'" stroke="'+strokeCol+'" stroke-width="'+(isMid?2:1)+'"/>';
  const val=2*Math.round(i*(n/numCells))+1;
  svg+='<text x="'+(cx+cellW/2)+'" y="'+(startY+cellH/2+4)+'" text-anchor="middle" fill="'+(isMid?'#fde047':'#dcebf2')+'" font-size="8.5" font-family="monospace">'+val+'</text>';
  svg+='<text x="'+(cx+cellW/2)+'" y="'+(startY+cellH+12)+'" text-anchor="middle" fill="#5a7687" font-size="7">['+Math.round(i*(n/numCells))+']</text>';
 }

 const midPx=startX+midIdx*(cellW+4)+cellW/2;
 svg+='<polygon points="'+midPx+','+(startY-4)+' '+(midPx-5)+','+(startY-12)+' '+(midPx+5)+','+(startY-12)+'" fill="'+orange+'"/>';
 svg+='<text x="'+midPx+'" y="'+(startY-16)+'" text-anchor="middle" fill="'+orange+'" font-size="8" font-weight="bold">mid</text>';

 const lowPx=startX+cellW/2;
 svg+='<polygon points="'+lowPx+','+(startY-4)+' '+(lowPx-5)+','+(startY-12)+' '+(lowPx+5)+','+(startY-12)+'" fill="#38bdf8"/>';
 svg+='<text x="'+lowPx+'" y="'+(startY-16)+'" text-anchor="middle" fill="#38bdf8" font-size="8" font-weight="bold">low</text>';

 const highPx=startX+(numCells-1)*(cellW+4)+cellW/2;
 svg+='<polygon points="'+highPx+','+(startY-4)+' '+(highPx-5)+','+(startY-12)+' '+(highPx+5)+','+(startY-12)+'" fill="#10b981"/>';
 svg+='<text x="'+highPx+'" y="'+(startY-16)+'" text-anchor="middle" fill="#10b981" font-size="8" font-weight="bold">high</text>';

 const regX=55,regY=185,regW=370,regH=70;
 svg+='<rect x="'+regX+'" y="'+regY+'" width="'+regW+'" height="'+regH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
 svg+='<text x="'+(regX+15)+'" y="'+(regY+18)+'" fill="#7e9bab" font-size="8" font-weight="bold">CPU EXECUTION STATE & COMPARATOR STATUS</text>';
 svg+='<text x="'+(regX+15)+'" y="'+(regY+36)+'" fill="#38bdf8" font-size="9" font-family="monospace">Active Subarray: [low=0 .. high='+(n-1)+'] ⟹ Candidates: '+n+'</text>';
 svg+='<text x="'+(regX+15)+'" y="'+(regY+52)+'" fill="'+orange+'" font-size="9" font-family="monospace">ALU Comparison: A[mid] < K ⟹ low = mid + 1 (Discard lower 50%)</text>';

 const bX=465,bY=38,bW=220,bH=235;
 svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">ARRAY SIZE (n)</text>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+n+'</text>';
 svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#8ba5b5" font-size="11">keys</text>';
 svg+='<line x1="'+(bX+15)+'" y1="'+(bY+64)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+64)+'" stroke="#1e3340"/>';

 svg+='<text x="'+(bX+15)+'" y="'+(bY+82)+'" fill="#7e9bab" font-size="9">KEY ENTROPY log₂(n)</text>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+106)+'" fill="'+ink+'" font-size="17" font-family="monospace" font-weight="bold">'+log2n.toFixed(2)+'</text>';
 svg+='<text x="'+(bX+95)+'" y="'+(bY+104)+'" fill="#8ba5b5" font-size="10">bits</text>';
 svg+='<line x1="'+(bX+15)+'" y1="'+(bY+120)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+120)+'" stroke="#1e3340"/>';

 svg+='<text x="'+(bX+15)+'" y="'+(bY+138)+'" fill="#7e9bab" font-size="9">WORST-CASE COMPARISONS (C_max)</text>';
 svg+='<text x="'+(bX+15)+'" y="'+(bY+164)+'" fill="#fde047" font-size="20" font-family="monospace" font-weight="bold">'+c_max+'</text>';
 svg+='<text x="'+(bX+75)+'" y="'+(bY+160)+'" fill="#8ba5b5" font-size="9">⌊log₂ n⌋ + 1</text>';
 svg+='<line x1="'+(bX+15)+'" y1="'+(bY+178)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+178)+'" stroke="#1e3340"/>';

 svg+=text(bX+bW/2,bY+200,'C = k_search · log₂(n) + 1',ink,10);
 svg+=text(bX+bW/2,bY+218,'Scaling Gradient: k = 1.0000 comp/bit',orange,9);

 svg+=text(360,305,'Algorithmic Complexity: T_worst(n) = ⌊log₂ n⌋ + 1 = Θ(log₂ n) · Space: O(1) Iterative',soft,10);
 $('apparatusDiagram').innerHTML=svg;
}

let last=0;
function animate(t){if(!paused&&t-last>70){draw(t);last=t;}requestAnimationFrame(animate);}
requestAnimationFrame(animate);
update();
renderResults();
