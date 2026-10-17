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

 if(cfg.slug==='network-flow-max-cut'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'MAXIMUM FLOW ALGORITHMIC PARADIGMS (|V| = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  const e=3*n;
  const c_dinic=Math.round(Math.min(1000000, (n * n * e) / 800));
  const c_ek=Math.round(Math.min(5000000, (n * e * e) / 300));
  const c_push=Math.round(Math.min(2000000, (n * n * n) / 150));
  const c_ff_int=Math.round(e * 45);
  const c_ff_path=9999999;

  const strategies=[
   {name:'Dinic Level Graph (Blocking Flow)',col:'#10b981',cost:c_dinic,scale:'O(|V|² · |E|)',desc:'Layered DAG via BFS; multiple paths via DFS; O(|E|√|V|) on unit networks'},
   {name:'Edmonds-Karp (Shortest Augmenting Path)',col:'#38bdf8',cost:c_ek,scale:'O(|V| · |E|²) strongly polynomial',desc:'BFS shortest paths; monotonic distance growth; capacity-independent'},
   {name:'Push-Relabel (Highest Vertex Rule)',col:'#f97316',cost:c_push,scale:'O(|V|³)',desc:'Local preflow-push & height relabeling; GPU & SIMD parallelizable'},
   {name:'Ford-Fulkerson (Integer Capacities)',col:'#a855f7',cost:c_ff_int,scale:'O(|E| · |f*|) pseudo-polynomial',desc:'Arbitrary DFS path selection; capacity-dependent iteration count'},
   {name:'Ford-Fulkerson (Pathological / Irrational)',col:'#ef4444',cost:c_ff_path,scale:'Non-convergent / infinite loop',desc:'Zwick irrational capacity cycle; fails to reach maximum flow'}
  ];

  strategies.forEach((item,idx)=>{
   const rowY=cY+16+idx*42;
   svg+='<text x="'+(cX+15)+'" y="'+(rowY+12)+'" fill="#dcebf2" font-size="8.5" font-weight="bold">'+item.name+'</text>';
   const costStr=item.cost>=1000000?(item.cost/1000000).toFixed(1)+'M':item.cost>=1000?(item.cost/1000).toFixed(1)+'k':item.cost;
   svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+12)+'" text-anchor="end" fill="'+item.col+'" font-size="8.5" font-family="monospace" font-weight="bold">'+costStr+' ops ('+item.scale+')</text>';
   
   const barX=cX+15,barY=rowY+16,barMaxW=cW-30;
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="7" rx="2" fill="#16242c"/>';
   const maxVal=Math.max(1000, c_ek);
   const frac=Math.min(1.0,Math.log10(item.cost+1)/Math.log10(maxVal+1));
   const fillW=Math.max(4,frac*barMaxW);
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="7" rx="2" fill="'+item.col+'"/>';
  });

  const bX=460,bY=45,bW=220,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">MAX-FLOW MIN-CUT DUALITY</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">|f*| ≡ c(S,T)</text>';
  svg+='<text x="'+(bX+125)+'" y="'+(bY+46)+'" fill="#10b981" font-size="10">Strong Duality</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">EDMONDS-KARP SATURATION BOUND</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">≤ |V| · |E| Rounds</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">Each edge critical at most |V|/2 times</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">DISTANCE MONOTONICITY</text>';
  svg+=text(bX+bW/2,bY+180,'δ_f(s, v) never decreases in G_f','#10b981',9.5);
  svg+=text(bX+bW/2,bY+202,'Polynomial bound independent of capacity',orange,8.5);
  svg+=text(360,305,'Comparative Invariant: Edmonds-Karp BFS guarantees strongly polynomial O(|V| · |E|²); Dinic achieves O(|V|² · |E|) via Level Graphs',soft,10);
  return svg;
 }

 if(cfg.slug==='string-matching-automata'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'STRING MATCHING PARADIGMS & ARCHITECTURES (n = '+p.input+', m = 20)','#e2f0f8',11);

  const n=p.input;
  const m_pat=20;
  const c_kmp=Math.round(n + m_pat);
  const c_bm=Math.round(n / 3.5 + m_pat * 1.5);
  const c_rk=Math.round(n + m_pat * 2);
  const c_ac=Math.round(n + m_pat);
  const c_naive=Math.round(n * (m_pat / 2.5));

  const strategies=[
   {name:'Boyer-Moore (Bad Char + Good Suffix)',col:'#10b981',cost:c_bm,scale:'O(n/m) sublinear average',desc:'Right-to-left scan; skips up to m characters per mismatch on large alphabets'},
   {name:'Knuth-Morris-Pratt (π-Prefix Array)',col:'#38bdf8',cost:c_kmp,scale:'O(n + m) linear stream',desc:'Monotonic text pointer i; π-table fallback; zero text buffer rewinding'},
   {name:'Rabin-Karp Rolling Hash (Horner)',col:'#f97316',cost:c_rk,scale:'O(n + m) expected',desc:'Polynomial rolling hash; O(1) window slide; multi-pattern capable'},
   {name:'Aho-Corasick Multi-Pattern Trie',col:'#a855f7',cost:c_ac,scale:'O(n + M) dictionary search',desc:'Trie failure & output links; simultaneous multi-string scanning; Snort NIDS'},
   {name:'Naive Brute-Force (Worst Case)',col:'#ef4444',cost:c_naive,scale:'Θ(n · m) worst-case',desc:'Full text pointer rewind on mismatch; L1 cache line thrashing'}
  ];

  strategies.forEach((item,idx)=>{
   const rowY=cY+16+idx*42;
   svg+='<text x="'+(cX+15)+'" y="'+(rowY+12)+'" fill="#dcebf2" font-size="8.5" font-weight="bold">'+item.name+'</text>';
   const costStr=item.cost>=1000000?(item.cost/1000000).toFixed(1)+'M':item.cost>=1000?(item.cost/1000).toFixed(1)+'k':item.cost;
   svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+12)+'" text-anchor="end" fill="'+item.col+'" font-size="8.5" font-family="monospace" font-weight="bold">'+costStr+' comps ('+item.scale+')</text>';
   
   const barX=cX+15,barY=rowY+16,barMaxW=cW-30;
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="7" rx="2" fill="#16242c"/>';
   const maxVal=Math.max(1000, c_naive);
   const frac=Math.min(1.0,Math.log10(item.cost+1)/Math.log10(maxVal+1));
   const fillW=Math.max(4,frac*barMaxW);
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="7" rx="2" fill="'+item.col+'"/>';
  });

  const bX=460,bY=45,bW=220,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">STREAMING SPEEDUP VS NAIVE</text>';
  const speedup=(c_naive / Math.max(1, c_kmp)).toFixed(1);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+speedup+'×</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#dcebf2" font-size="10">Zero Rewind</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">FAILURE TABLE FOOTPRINT</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">π[0..19] = 80 Bytes</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">O(m) auxiliary table fits in CPU L1 cache</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">AMORTIZED COMPLEXITY BOUND</text>';
  svg+=text(bX+bW/2,bY+180,'Comparisons ≤ 2n in text scan','#10b981',9.5);
  svg+=text(bX+bW/2,bY+202,'Monotonic text pointer i ∈ [0..n-1]',orange,8.5);
  svg+=text(360,305,'Comparative Invariant: KMP guarantees linear O(n + m) without rewinding text; Boyer-Moore achieves sublinear O(n/m) on large alphabets',soft,10);
  return svg;
 }

 if(cfg.slug==='greedy-minimum-spanning-trees'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'MINIMUM SPANNING TREE PARADIGMS & ARCHITECTURES (|V| = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  const e=4*n;
  const c_kruskal=Math.round(e * Math.log2(e) + 2 * e * 1.05);
  const c_prim_fib=Math.round(e + n * Math.log2(n));
  const c_prim_bin=Math.round((n + e) * Math.log2(n));
  const c_boruvka=Math.round(e * Math.log2(n));
  const c_naive_dsu=Math.round(e * Math.log2(e) + e * (n / 4));

  const strategies=[
   {name:'Kruskal with DSU (Path Comp + Rank)',col:'#10b981',cost:c_kruskal,scale:'O(|E| log |V| + |E|α(|V|))',desc:'Optimal on sparse networks; flat edge array sorting; amortized inverse Ackermann DSU'},
   {name:'Prim with Fibonacci Heap',col:'#38bdf8',cost:c_prim_fib,scale:'O(|E| + |V| log |V|)',desc:'O(1) amortized decrease_key; vertex-growing tree frontier; optimal on dense graphs'},
   {name:'Prim with Binary Min-Heap',col:'#f97316',cost:c_prim_bin,scale:'O((|V|+|E|) log |V|)',desc:'Standard binary priority queue; O(log |V|) decrease_key; simple heap implementation'},
   {name:'Borůvka Parallel Contraction',col:'#a855f7',cost:c_boruvka,scale:'O(|E| log |V|) parallel rounds',desc:'Multi-component simultaneous contraction; ⌈log₂ |V|⌉ rounds; GPU/cluster scalable'},
   {name:'Kruskal Naive DSU (No Path Comp)',col:'#ef4444',cost:c_naive_dsu,scale:'O(|E| · |V|) degraded DSU',desc:'Degenerate parent chains without path compression; catastrophic tree walk stalls'}
  ];

  strategies.forEach((item,idx)=>{
   const rowY=cY+16+idx*42;
   svg+='<text x="'+(cX+15)+'" y="'+(rowY+12)+'" fill="#dcebf2" font-size="8.5" font-weight="bold">'+item.name+'</text>';
   const costStr=item.cost>=1000000?(item.cost/1000000).toFixed(1)+'M':item.cost>=1000?(item.cost/1000).toFixed(1)+'k':item.cost;
   svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+12)+'" text-anchor="end" fill="'+item.col+'" font-size="8.5" font-family="monospace" font-weight="bold">'+costStr+' ops ('+item.scale+')</text>';
   
   const barX=cX+15,barY=rowY+16,barMaxW=cW-30;
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="7" rx="2" fill="#16242c"/>';
   const maxVal=Math.max(10000, c_naive_dsu);
   const frac=Math.min(1.0,Math.log10(item.cost+1)/Math.log10(maxVal+1));
   const fillW=Math.max(4,frac*barMaxW);
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="7" rx="2" fill="'+item.col+'"/>';
  });

  const bX=460,bY=45,bW=220,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">DSU TREE COMPRESSION RATIO</text>';
  const compressionRatio=(c_naive_dsu / Math.max(1, c_kruskal)).toFixed(1);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+compressionRatio+'×</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#dcebf2" font-size="10">Rank & Path Comp</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">SPANNING TREE INVARIANT</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">|E_mst| = '+(n-1)+' Edges</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">Cayley Theorem: Exactly |V| − 1 edges in tree</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">INVERSE ACKERMANN BOUND</text>';
  svg+=text(bX+bW/2,bY+180,'α(|V|) ≤ 4 for all |V| ≤ 10¹⁰⁰','#10b981',9.5);
  svg+=text(bX+bW/2,bY+202,'Amortized near O(1) query time',orange,8.5);
  svg+=text(360,305,'Comparative Invariant: Kruskal + DSU achieves optimal O(|E| log |V|) on sparse graphs, enforcing the Cut Property',soft,10);
  return svg;
 }

 if(cfg.slug==='dynamic-programming-memoization'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'DYNAMIC PROGRAMMING COMPUTATIONAL STRATEGIES (n = '+p.input+', W = 100)','#e2f0f8',11);

  const n=p.input;
  const w=100;
  const c_tab1d=n * w;
  const c_tab2d=n * w;
  const c_memo=Math.round(n * w * 1.35);
  const c_greedy=Math.round(n * Math.log2(Math.max(2, n)));
  const c_naive=n>=30?1000000000:Math.pow(2, n);

  const strategies=[
   {name:'Bottom-Up Tabulation (1D Rolling)',col:'#10b981',cost:c_tab1d,scale:'O(nW) time, O(W) space',desc:'Optimal reverse scan (W down to w_i); 100% L1 cache resident; zero pointer chasing'},
   {name:'Bottom-Up Tabulation (2D Matrix)',col:'#38bdf8',cost:c_tab2d,scale:'O(nW) time, O(nW) space',desc:'Sequential row-major matrix; enables O(n) backtracking subset recovery'},
   {name:'Top-Down Memoization (Cached)',col:'#f97316',cost:c_memo,scale:'O(nW) time, O(nW) space',desc:'On-demand recursive evaluation; skips unreachable states; AMD64 stack overhead'},
   {name:'Greedy Value Density Heuristic',col:'#a855f7',cost:c_greedy,scale:'O(n log n) sub-optimal',desc:'Sorts by v_i/w_i ratio; fast approximation but fails discrete 0/1 optimality'},
   {name:'Naive Recursive Call Tree',col:'#ef4444',cost:c_naive,scale:'Θ(2ⁿ) exponential tree',desc:'Full inclusion/exclusion tree; duplicate subproblem explosion; intractable for n>35'}
  ];

  strategies.forEach((item,idx)=>{
   const rowY=cY+16+idx*42;
   svg+='<text x="'+(cX+15)+'" y="'+(rowY+12)+'" fill="#dcebf2" font-size="8.5" font-weight="bold">'+item.name+'</text>';
   const costStr=item.cost>=1000000000?'>1.0B (2ⁿ)':item.cost>=1000000?(item.cost/1000000).toFixed(1)+'M':item.cost>=1000?(item.cost/1000).toFixed(1)+'k':item.cost;
   svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+12)+'" text-anchor="end" fill="'+item.col+'" font-size="8.5" font-family="monospace" font-weight="bold">'+costStr+' ops ('+item.scale+')</text>';
   
   const barX=cX+15,barY=rowY+16,barMaxW=cW-30;
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="7" rx="2" fill="#16242c"/>';
   const maxVal=1000000000;
   const frac=Math.min(1.0,Math.log10(item.cost+1)/Math.log10(maxVal+1));
   const fillW=Math.max(4,frac*barMaxW);
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="7" rx="2" fill="'+item.col+'"/>';
  });

  const bX=460,bY=45,bW=220,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">PRUNING SPEEDUP (vs 2ⁿ NAIVE)</text>';
  const speedupStr=n>=30?'10¹²×+':((Math.pow(2, n))/(c_tab1d)).toFixed(1)+'×';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+speedupStr+'</text>';
  svg+='<text x="'+(bX+110)+'" y="'+(bY+46)+'" fill="#dcebf2" font-size="10">DP vs Naive Tree</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">MEMORY COMPRESSION</text>';
  const mem2d=( ((n+1)*(w+1)*8)/1024 ).toFixed(1);
  const mem1d=( ((w+1)*8)/1024 ).toFixed(2);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="15" font-family="monospace" font-weight="bold">'+mem1d+' vs '+mem2d+' KiB</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">1D Rolling Array vs 2D Matrix (W vs n·W)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">PSEUDO-POLYNOMIAL BOUND</text>';
  svg+=text(bX+bW/2,bY+180,'T(n, W) = n · W = 100.0000 · n','#10b981',9.5);
  svg+=text(bX+bW/2,bY+202,'Polynomial in numeric W; Weak NP-C',orange,8.5);
  svg+=text(360,305,'Comparative Invariant: Dynamic Programming eliminates exponential recursion Θ(2ⁿ) ⟶ pseudo-polynomial Θ(nW)',soft,10);
  return svg;
 }

 if(cfg.slug==='graph-traversal-shortest-paths'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'GRAPH ALGORITHM & REPRESENTATION BENCHMARK (|V| = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  const e=4*n;
  const c_csr=n + e;
  const c_adj=n + e;
  const c_dijkstra=Math.round((n + e) * Math.log2(n));
  const c_matrix=n * n;
  const c_floyd=Math.min(100000000, n * n * n);

  const strategies=[
   {name:'Compressed Sparse Row (CSR)',col:'#10b981',cost:c_csr,scale:'O(|V|+|E|) flat arrays',desc:'Packed contiguous edge & row pointers; zero pointer chasing; SIMD vectorized'},
   {name:'Adjacency List (Dynamic Vectors)',col:'#38bdf8',cost:c_adj,scale:'O(|V|+|E|) optimal',desc:'Optimal sparse graph memory; neighbor scan time proportional to out-degree'},
   {name:'Dijkstra Shortest Path (Min-Heap)',col:'#f97316',cost:c_dijkstra,scale:'O((|V|+|E|) log |V|)',desc:'Non-negative edge weights; priority queue extracts minimal tentative distance'},
   {name:'Adjacency Matrix (Dense 2D)',col:'#ef4444',cost:c_matrix,scale:'O(|V|²) matrix scan',desc:'O(1) edge lookup, but catastrophic quadratic memory and full-row scans'},
   {name:'Floyd-Warshall All-Pairs SP',col:'#a855f7',cost:c_floyd,scale:'O(|V|³) cubic scan',desc:'Dynamic programming all-pairs shortest paths; scans triple nested loops'}
  ];

  strategies.forEach((item,idx)=>{
   const rowY=cY+16+idx*42;
   svg+='<text x="'+(cX+15)+'" y="'+(rowY+12)+'" fill="#dcebf2" font-size="8.5" font-weight="bold">'+item.name+'</text>';
   const costStr=item.cost>=1000000?(item.cost/1000000).toFixed(1)+'M':item.cost>=1000?(item.cost/1000).toFixed(1)+'k':item.cost;
   svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+12)+'" text-anchor="end" fill="'+item.col+'" font-size="8.5" font-family="monospace" font-weight="bold">'+costStr+' ops ('+item.scale+')</text>';
   
   const barX=cX+15,barY=rowY+16,barMaxW=cW-30;
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="7" rx="2" fill="#16242c"/>';
   const maxVal=Math.max(10, c_matrix);
   const frac=Math.min(1.0,Math.log10(item.cost+1)/Math.log10(maxVal+1));
   const fillW=Math.max(4,frac*barMaxW);
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="7" rx="2" fill="'+item.col+'"/>';
  });

  const bX=460,bY=45,bW=220,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">SPARSE GRAPH SPEEDUP</text>';
  const matrixSpeedup=(c_matrix / Math.max(1, c_adj)).toFixed(1);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+matrixSpeedup+'×</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#dcebf2" font-size="10">List vs Matrix</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">MEMORY SCALING FOOTPRINT</text>';
  const memList=( (n*8 + e*16)/1024 ).toFixed(1);
  const memMat=( (n*n)/1024 ).toFixed(1);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="15" font-family="monospace" font-weight="bold">'+memList+' vs '+memMat+' KiB</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">List: Θ(|V|+|E|) · Matrix: Θ(|V|²)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">SHORTEST PATH COMPLEXITY</text>';
  svg+=text(bX+bW/2,bY+180,'BFS (Unweighted): O(|V| + |E|) FIFO','#10b981',9.5);
  svg+=text(bX+bW/2,bY+202,'Dijkstra (Weighted): O((V+E) log V)',orange,8.5);
  svg+=text(360,305,'Comparative Invariant: Adjacency List achieves optimal O(|V| + |E|) traversal, avoiding quadratic O(|V|²) matrix scanning waste',soft,10);
  return svg;
 }

 if(cfg.slug==='hash-tables-collision-resolution'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'COLLISION RESOLUTION PROBE COMPARISON (m = 1000 · n = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  const alpha=n/1000.0;
  const c_chain=(alpha).toFixed(2);
  const c_double=(1.0/(1.0 - alpha)).toFixed(2);
  const c_quad=(1.0 - Math.log(1.0 - alpha) - alpha/2.0).toFixed(2);
  const c_linear=(0.5*(1.0 + 1.0/((1.0 - alpha)**2))).toFixed(2);
  const c_swiss='1.00';

  const strategies=[
   {name:'Swiss Tables (16-Way SIMD Vector)',col:'#a855f7',cost:c_swiss,scale:'~1.00 vector probe',desc:'16 control bytes tested in 1 cycle via SSE2/AVX2; zero cache misses'},
   {name:'Separate Chaining (Linked Buckets)',col:'#10b981',cost:c_chain,scale:'α = '+alpha.toFixed(2)+' probes',desc:'Linear degradation; no saturation limit; non-contiguous heap pointer hops'},
   {name:'Double Hashing (Coprime Strides)',col:'#38bdf8',cost:c_double,scale:'1/(1−α) probes',desc:'Optimal open addressing; eliminates both primary & secondary clustering'},
   {name:'Quadratic Probing (Triangular Steps)',col:'#f97316',cost:c_quad,scale:'1−ln(1−α)−α/2',desc:'Eliminates primary clustering runs; mild secondary clustering'},
   {name:'Linear Probing (Sequential Stepping)',col:'#ef4444',cost:c_linear,scale:'0.5(1 + 1/(1−α)²)',desc:'Severe primary clustering; contiguous runs act as gravitational attractors'}
  ];

  strategies.forEach((item,idx)=>{
   const rowY=cY+16+idx*42;
   svg+='<text x="'+(cX+15)+'" y="'+(rowY+12)+'" fill="#dcebf2" font-size="8.5" font-weight="bold">'+item.name+'</text>';
   svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+12)+'" text-anchor="end" fill="'+item.col+'" font-size="8.5" font-family="monospace" font-weight="bold">'+item.cost+' probes ('+item.scale+')</text>';
   
   const barX=cX+15,barY=rowY+16,barMaxW=cW-30;
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="7" rx="2" fill="#16242c"/>';
   const maxVal=Math.max(10, parseFloat(c_linear));
   const frac=Math.min(1.0,Math.log10(parseFloat(item.cost)+1)/Math.log10(maxVal+1));
   const fillW=Math.max(4,frac*barMaxW);
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="7" rx="2" fill="'+item.col+'"/>';
  });

  const bX=460,bY=45,bW=220,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">PRIMARY CLUSTERING PENALTY</text>';
  const linOverDouble=(parseFloat(c_linear)/Math.max(0.1, parseFloat(c_double))).toFixed(1);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+linOverDouble+'×</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#dcebf2" font-size="10">Linear vs Double</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">UNSUCCESSFUL PROBE BOUND</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="15" font-family="monospace" font-weight="bold">'+c_double+' vs '+c_linear+' probes</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">Double: 1/(1−α) · Linear: 0.5(1 + 1/(1−α)²)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">METADATA CACHE EFFICIENCY</text>';
  svg+=text(bX+bW/2,bY+180,'Swiss Table: 1 Byte/slot (Control array)','#10b981',9.5);
  svg+=text(bX+bW/2,bY+202,'Chaining: 24 Bytes/node (600% overhead)',orange,8.5);
  svg+=text(360,305,'Comparative Invariant: Double Hashing achieves optimal 1/(1−α) probe depth without primary clustering degradation',soft,10);
  return svg;
 }

 if(cfg.slug==='binary-heaps-priority-queues'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'PRIORITY QUEUE IMPLEMENTATION & EXTRACTION BENCHMARK (n = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  const log2n=Math.log2(n);
  const log4n=Math.log(n)/Math.log(4);
  const c_dary=Math.round(4*log4n);
  const c_bin=Math.round(2*log2n);
  const c_fib=Math.round(2*log2n);
  const c_sorted=1;
  const c_unsorted=n-1;

  const queues=[
   {name:'4-Way D-Ary Heap (d=4)',col:'#10b981',cost:c_dary,scale:'4 log₄ n comps',desc:'Tree height reduced 2×; 4 keys fit in single 64B L1 cache line'},
   {name:'Binary Max-Heap (In-Place Array)',col:'#38bdf8',cost:c_bin,scale:'2 log₂ n comps',desc:'Zero pointer overhead; implicit arithmetic 2i+1, 2i+2; cache dense'},
   {name:'Fibonacci Heap (Pointer Forest)',col:'#f97316',cost:c_fib,scale:'O(log n) amortized',desc:'48B metadata/node; 600% pointer overhead; frequent cache misses'},
   {name:'Sorted Contiguous Array',col:'#ef4444',cost:c_sorted,scale:'1 comparison',desc:'O(1) extract-max, but catastrophic O(n) element shifting on insert'},
   {name:'Unsorted Dynamic Array',col:'#a855f7',cost:c_unsorted,scale:'O(n) linear scan',desc:'O(1) append, but catastrophic n-1 comparisons to find maximum'}
  ];

  queues.forEach((item,idx)=>{
   const rowY=cY+16+idx*42;
   svg+='<text x="'+(cX+15)+'" y="'+(rowY+12)+'" fill="#dcebf2" font-size="8.5" font-weight="bold">'+item.name+'</text>';
   svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+12)+'" text-anchor="end" fill="'+item.col+'" font-size="8.5" font-family="monospace" font-weight="bold">'+item.cost+' ('+item.scale+')</text>';
   
   const barX=cX+15,barY=rowY+16,barMaxW=cW-30;
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="7" rx="2" fill="#16242c"/>';
   const frac=Math.min(1.0,Math.log10(item.cost+1)/Math.log10(c_unsorted+1));
   const fillW=Math.max(4,frac*barMaxW);
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="7" rx="2" fill="'+item.col+'"/>';
  });

  const bX=460,bY=45,bW=220,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">FLOYD HEAPIFY SPEEDUP</text>';
  const naiveOps=Math.round(n*log2n);
  const floydOps=v.raw;
  const speedup=(naiveOps/Math.max(1,floydOps)).toFixed(1);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+speedup+'×</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#dcebf2" font-size="10">vs Naive Insert</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">CONSTRUCTION ASYMPTOTICS</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="15" font-family="monospace" font-weight="bold">'+floydOps+' vs '+naiveOps+' ops</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">Floyd: O(n) · Repeated Insert: O(n log n)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">METADATA POINTER OVERHEAD</text>';
  svg+=text(bX+bW/2,bY+180,'Binary Heap: 0 B/node (In-Place Array)','#10b981',9.5);
  svg+=text(bX+bW/2,bY+202,'Fibonacci: 48 B/node (4 ptrs + degree)',orange,8.5);
  svg+=text(360,305,'Comparative Invariant: Floyd\'s in-place heapify achieves optimal O(n) construction without pointer overhead or heap allocations',soft,10);
  return svg;
 }

 if(cfg.slug==='binary-search-trees'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'TREE & INDEXING TOPOLOGY COMPARISON (n = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  const log2n=Math.log2(n);
  const h_avl=Math.floor(log2n)+1;
  const h_rb=Math.min(2*h_avl, Math.round(1.3*log2n + 1));
  const h_random=Math.round(2.07*log2n);
  const h_btree=Math.max(2, Math.ceil(Math.log(n)/Math.log(64)));
  const h_degen=n;

  const topologies=[
   {name:'B-Tree (Fan-Out B = 64)',col:'#10b981',height:h_btree,scale:'O(log_B n)',desc:'Massive branching; cache & disk block aligned'},
   {name:'AVL Balanced Binary Tree',col:'#38bdf8',height:h_avl,scale:'1.00 log₂ n',desc:'Strict balance |BF| ≤ 1; optimal read lookup depth'},
   {name:'Red-Black Balanced Tree',col:'#f97316',height:h_rb,scale:'≤ 1.44 log₂ n',desc:'Relaxed balance; at most 2 rotations on insert'},
   {name:'Random Insertion BST',col:'#a855f7',height:h_random,scale:'~2.07 log₂ n',desc:'No rebalancing; 1.386 ln n average search depth'},
   {name:'Degenerate List (Sorted Input)',col:'#ef4444',height:h_degen,scale:'O(n) height',desc:'Linear collapse; catastrophic O(n) search latency'}
  ];

  topologies.forEach((item,idx)=>{
   const rowY=cY+16+idx*42;
   svg+='<text x="'+(cX+15)+'" y="'+(rowY+12)+'" fill="#dcebf2" font-size="8.5" font-weight="bold">'+item.name+'</text>';
   svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+12)+'" text-anchor="end" fill="'+item.col+'" font-size="8.5" font-family="monospace" font-weight="bold">'+item.height+' levels ('+item.scale+')</text>';
   
   const barX=cX+15,barY=rowY+16,barMaxW=cW-30;
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="7" rx="2" fill="#16242c"/>';
   const frac=Math.min(1.0,Math.log10(item.height+1)/Math.log10(h_degen+1));
   const fillW=Math.max(4,frac*barMaxW);
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="7" rx="2" fill="'+item.col+'"/>';
  });

  const bX=460,bY=45,bW=220,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">DEGENERACY COLLAPSE RATIO</text>';
  const degRatio=(h_degen/h_avl).toFixed(1);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+degRatio+'×</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#dcebf2" font-size="10">List vs Balanced</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">SEARCH PATH COMPARISON</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">'+h_avl+' vs '+h_degen+' hops</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">Balanced: O(log n) · Degenerate: O(n)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">ROTATION REBALANCING BOUND</text>';
  svg+=text(bX+bW/2,bY+180,'AVL: at most 1 rotation on insert','#10b981',10.5);
  svg+=text(bX+bW/2,bY+202,'Red-Black: at most 2 rotations',orange,9.5);
  svg+=text(360,305,'Comparative Invariant: Tree balancing bounds height to O(log n), preventing catastrophic 300× latency collapse',soft,10);
  return svg;
 }

 if(cfg.slug==='linked-list-architectures'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'SEQUENTIAL CONTAINER & CACHE LOCALITY BENCHMARK (n = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  const m_vector=Math.round(8*n);
  const m_unrolled=Math.round(12*n);
  const m_singly=Math.round(16*n + 16);
  const m_doubly=Math.round(32*n + 64);
  const m_skip=Math.round(48*n + 64);

  const containers=[
   {name:'Contiguous Vector (std::vector)',col:'#10b981',mem:m_vector,scale:'8 B/elem',desc:'Dense array, 8 items/L1 cache line, spatial prefetcher'},
   {name:'Unrolled Linked List (Chunked)',col:'#38bdf8',mem:m_unrolled,scale:'12 B/elem',desc:'Nodes contain 8-item arrays, amortized cache locality'},
   {name:'Singly Linked List (Forward)',col:'#f97316',mem:m_singly,scale:'16 B/elem',desc:'8B data + 8B next pointer, unidirectional traversal'},
   {name:'Doubly Linked List (Sentinel)',col:'#ef4444',mem:m_doubly,scale:'32 B/elem',desc:'8B data + 16B ptrs + 8B pad; 300% metadata overhead'},
   {name:'Skip List (Probabilistic Index)',col:'#a855f7',mem:m_skip,scale:'48 B/elem',desc:'Multi-level forward pointer tower, O(log n) search'}
  ];

  containers.forEach((item,idx)=>{
   const rowY=cY+16+idx*42;
   svg+='<text x="'+(cX+15)+'" y="'+(rowY+12)+'" fill="#dcebf2" font-size="8.5" font-weight="bold">'+item.name+'</text>';
   const memStr=item.mem>=1024?(item.mem/1024).toFixed(1)+' KiB':item.mem+' B';
   svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+12)+'" text-anchor="end" fill="'+item.col+'" font-size="8.5" font-family="monospace" font-weight="bold">'+memStr+' ('+item.scale+')</text>';
   
   const barX=cX+15,barY=rowY+16,barMaxW=cW-30;
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="7" rx="2" fill="#16242c"/>';
   const frac=Math.min(1.0,Math.log10(item.mem+1)/Math.log10(m_skip+1));
   const fillW=Math.max(4,frac*barMaxW);
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="7" rx="2" fill="'+item.col+'"/>';
  });

  const bX=460,bY=45,bW=220,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">POINTER CHASE LATENCY PENALTY</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">~12.5×</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#dcebf2" font-size="10">List vs Vector</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">L1 CACHE LINE UTILIZATION</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">100% vs 25%</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">Vector: 8 elems/line · List: 1-2 nodes</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">SPATIAL PREFETCHER STATUS</text>';
  svg+=text(bX+bW/2,bY+180,'Hardware Prefetch: INACTIVE','#ef4444',10.5);
  svg+=text(bX+bW/2,bY+202,'Heap pointer hopping defeats stride prefetching',orange,8.5);
  svg+=text(360,305,'Comparative Invariant: Vector delivers 4× memory density and ~12× faster sequential streaming than Linked List',soft,10);
  return svg;
 }

 if(cfg.slug==='queue-buffer-management'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'QUEUE ARCHITECTURES & THROUGHPUT BENCHMARK (n = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  const t_ring=Math.round(n * 0.05);
  const t_disruptor=Math.round(n * 0.015);
  const t_dyn=Math.round(n * 0.12);
  const t_linked=Math.round(n * 0.65);
  const t_naive=Math.round(n * 2.8);

  const algos=[
   {name:'Lock-Free Disruptor Ring',col:'#10b981',time:t_disruptor,scale:'O(1) lock-free',desc:'Zero malloc, atomic sequence, padded lines'},
   {name:'Circular Ring Buffer (Mutex)',col:'#38bdf8',time:t_ring,scale:'O(1) in-place',desc:'Cyclic modular indexing, zero reallocations'},
   {name:'Dynamic Array Queue',col:'#f97316',time:t_dyn,scale:'Amortized O(1)',desc:'Occasional O(N) capacity doubling spikes'},
   {name:'Singly-Linked Node Queue',col:'#a855f7',time:t_linked,scale:'O(1) pointer',desc:'Heap malloc per node, pointer chasing cache misses'},
   {name:'Naive Array (Dequeue Shift)',col:'#ef4444',time:t_naive,scale:'O(n) per dequeue',desc:'Shifts elements left; catastrophic latency'}
  ];

  algos.forEach((item,idx)=>{
   const rowY=cY+16+idx*42;
   svg+='<text x="'+(cX+15)+'" y="'+(rowY+12)+'" fill="#dcebf2" font-size="8.5" font-weight="bold">'+item.name+'</text>';
   svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+12)+'" text-anchor="end" fill="'+item.col+'" font-size="8.5" font-family="monospace" font-weight="bold">'+item.time+' µs ('+item.scale+')</text>';
   
   const barX=cX+15,barY=rowY+16,barMaxW=cW-30;
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="7" rx="2" fill="#16242c"/>';
   const frac=Math.min(1.0,Math.log10(item.time+1)/Math.log10(t_naive+1));
   const fillW=Math.max(4,frac*barMaxW);
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="7" rx="2" fill="'+item.col+'"/>';
  });

  const bX=460,bY=45,bW=220,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">THROUGHPUT ADVANTAGE RATIO</text>';
  const speedRatio=(t_naive/t_ring).toFixed(1);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+speedRatio+'×</text>';
  svg+='<text x="'+(bX+85)+'" y="'+(bY+46)+'" fill="#dcebf2" font-size="10">Ring vs Naive Shift</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">FALSE SHARING ELIMINATION</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="15" font-family="monospace" font-weight="bold">64-Byte Padding</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">Head and tail on separate cache lines</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">POWER-OF-TWO BITMASKING</text>';
  svg+=text(bX+bW/2,bY+180,'index & (N − 1) (1 cycle)','#38bdf8',11);
  svg+=text(bX+bW/2,bY+202,'Replaces IDIV instruction (30 cycles)',orange,9.5);
  svg+=text(360,305,'Comparative Invariant: Circular buffer provides O(1) in-place operations with zero memory churn',soft,10);
  return svg;
 }

 if(cfg.slug==='stack-adt-recursion'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'RECURSION & CALL STACK MEMORY COMPARISON (n = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  const m_linear=64*n + 128;
  const m_tco=64;
  const m_tree=Math.round(64*(Math.floor(Math.log2(n))+1));
  const m_heap=16*n;
  const m_parse=Math.round(24*Math.min(16, Math.floor(Math.log2(n))+1));

  const algos=[
   {name:'Linear Recursion (Unoptimized)',col:'#ef4444',mem:m_linear,scale:'O(n) stack',desc:'64 B/frame; risk of Stack Overflow'},
   {name:'Tail-Call Optimization (TCO)',col:'#10b981',mem:m_tco,scale:'O(1) stack',desc:'Reuses single frame via in-place jmp'},
   {name:'Divide-and-Conquer Tree',col:'#38bdf8',mem:m_tree,scale:'O(log n) stack',desc:'Height h = ⌊log₂ n⌋ + 1 frames'},
   {name:'Heap-Allocated Stack Vector',col:'#f97316',mem:m_heap,scale:'O(n) heap',desc:'Dynamic payload in RAM; no stack limit'},
   {name:'Shunting-Yard Parser Stack',col:'#a855f7',mem:m_parse,scale:'O(depth) stack',desc:'Bounded by syntax nesting depth d'}
  ];

  algos.forEach((item,idx)=>{
   const rowY=cY+16+idx*42;
   svg+='<text x="'+(cX+15)+'" y="'+(rowY+12)+'" fill="#dcebf2" font-size="8.5" font-weight="bold">'+item.name+'</text>';
   const memStr=item.mem>=1024?(item.mem/1024).toFixed(1)+' KiB':item.mem+' B';
   svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+12)+'" text-anchor="end" fill="'+item.col+'" font-size="8.5" font-family="monospace" font-weight="bold">'+memStr+' ('+item.scale+')</text>';
   
   const barX=cX+15,barY=rowY+16,barMaxW=cW-30;
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="7" rx="2" fill="#16242c"/>';
   const frac=Math.min(1.0,Math.log10(item.mem+1)/Math.log10(m_linear+1));
   const fillW=Math.max(4,frac*barMaxW);
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="7" rx="2" fill="'+item.col+'"/>';
  });

  const bX=460,bY=45,bW=220,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">TCO MEMORY REDUCTION RATIO</text>';
  const redRatio=(m_linear/m_tco).toFixed(0);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+redRatio+'×</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#dcebf2" font-size="10">Linear vs TCO</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">8 MiB THREAD QUOTA WATERMARK</text>';
  const quotaPct=(m_linear/(8*1024*1024)*100).toFixed(2);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">'+quotaPct+'% used</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">Overflow boundary at 131,072 frames</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">ABI CALLING CONVENTION</text>';
  svg+=text(bX+bW/2,bY+180,'RSP % 16 == 0 before CALL','#38bdf8',10.5);
  svg+=text(bX+bW/2,bY+202,'TCO: Replaces CALL/RET with JMP',orange,9.5);
  svg+=text(360,305,'Comparative Invariant: Linear recursion requires O(n) stack · TCO and Heap vectors preserve O(1) stack',soft,10);
  return svg;
 }

 if(cfg.slug==='divide-conquer-sorting'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#0b151b" stroke="'+soft+'" stroke-width="1.5" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'DIVIDE-AND-CONQUER COMPARATIVE BENCHMARK (n = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  const log2n=Math.log2(n);
  const c_merge=Math.round(n*log2n - n + 1);
  const c_quick_avg=Math.round(1.386*n*log2n);
  const c_quick_worst=Math.round(n*(n-1)/2);
  const c_heap=Math.round(2*n*log2n);
  const c_tim=Math.round(n*log2n*0.85);

  const algos=[
   {name:'Merge Sort (Guaranteed Worst)',col:'#38bdf8',ops:c_merge,space:'O(n) heap',stable:'Stable (Yes)',desc:'Predictable comparisons, streaming memory'},
   {name:'Quick Sort (Expected Average)',col:'#10b981',ops:c_quick_avg,space:'O(log n) stack',stable:'Unstable (No)',desc:'Superior L1/L2 cache locality, in-place'},
   {name:'Quick Sort (Deterministic Worst)',col:'#ef4444',ops:c_quick_worst,space:'O(n) stack',stable:'Unstable (No)',desc:'Unbalanced pivot partition collapse'},
   {name:'Heap Sort (Guaranteed Worst)',col:'#f97316',ops:c_heap,space:'O(1) in-place',stable:'Unstable (No)',desc:'In-place heapify, poor cache locality'},
   {name:'Timsort / Introsort (Hybrid)',col:'#a855f7',ops:c_tim,space:'O(n) / O(log n)',stable:'Adaptive',desc:'Insertion below threshold, worst O(n log n)'}
  ];

  algos.forEach((item,idx)=>{
   const rowY=cY+16+idx*42;
   svg+='<text x="'+(cX+15)+'" y="'+(rowY+12)+'" fill="#dcebf2" font-size="8.5" font-weight="bold">'+item.name+'</text>';
   svg+='<text x="'+(cX+cW-15)+'" y="'+(rowY+12)+'" text-anchor="end" fill="'+item.col+'" font-size="8.5" font-family="monospace" font-weight="bold">'+item.ops+' comp | '+item.space+'</text>';
   
   const barX=cX+15,barY=rowY+16,barMaxW=cW-30;
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barMaxW+'" height="7" rx="2" fill="#16242c"/>';
   const maxVal=Math.max(c_quick_worst, c_heap, 1);
   const frac=Math.min(1.0,item.ops/maxVal);
   const fillW=Math.max(4,frac*barMaxW);
   svg+='<rect x="'+barX+'" y="'+barY+'" width="'+fillW+'" height="7" rx="2" fill="'+item.col+'"/>';
  });

  const bX=460,bY=45,bW=220,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">AUXILIARY BUFFER OVERHEAD</text>';
  const auxBytes=(n*8);
  const auxText=auxBytes>=1024?(auxBytes/1024).toFixed(1)+' KiB':auxBytes+' B';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+auxText+'</text>';
  svg+='<text x="'+(bX+110)+'" y="'+(bY+46)+'" fill="#dcebf2" font-size="10">Merge Scratchpad</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+65)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+65)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+84)+'" fill="#7e9bab" font-size="9">CACHE LOCALITY PROFILE</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+108)+'" fill="'+ink+'" font-size="14" font-family="monospace" font-weight="bold">Quick > Merge >> Heap</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">Heap non-local jumps degrade hardware prefetch</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+136)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+136)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+154)+'" fill="#7e9bab" font-size="9">ASYMPTOTIC MASTER THEOREM</text>';
  svg+=text(bX+bW/2,bY+180,'T(n) = 2T(n/2) + Θ(n)','#38bdf8',11);
  svg+=text(bX+bW/2,bY+202,'⟹ T(n) = Θ(n log₂ n) (Case 2)',orange,9.5);
  svg+=text(360,305,'Comparative Invariant: Merge guarantees stability with O(n) space · Quick optimizes CPU cache · Heap guarantees O(1) space',soft,10);
  return svg;
 }

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

 if(cfg.slug==='network-flow-max-cut'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'MAX-FLOW MIN-CUT DUALITY & RESIDUAL CUT SANDBOX (|V| = '+p.input+')','#e2f0f8',11);

  svg+='<text x="'+(cX+15)+'" y="'+(cY+20)+'" fill="#10b981" font-size="8.5" font-weight="bold">DUALITY THEOREM: MAX FLOW |f*| ≡ MIN CUT c(S, T) = 20 UNITS</text>';

  const sBoxX=cX+20, sBoxY=cY+36, sBoxW=155, sBoxH=118;
  svg+='<rect x="'+sBoxX+'" y="'+sBoxY+'" width="'+sBoxW+'" height="'+sBoxH+'" rx="6" fill="#042f2e" stroke="#14b8a6" stroke-width="1.2" stroke-dasharray="3,2"/>';
  svg+='<text x="'+(sBoxX+12)+'" y="'+(sBoxY+18)+'" fill="#2dd4bf" font-size="8" font-weight="bold">SOURCE CUT SET S (Reachable in G_f)</text>';

  const tBoxX=cX+225, tBoxY=cY+36, tBoxW=155, tBoxH=118;
  svg+='<rect x="'+tBoxX+'" y="'+tBoxY+'" width="'+tBoxW+'" height="'+tBoxH+'" rx="6" fill="#0c1929" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="3,2"/>';
  svg+='<text x="'+(tBoxX+12)+'" y="'+(tBoxY+18)+'" fill="#7dd3fc" font-size="8" font-weight="bold">SINK CUT SET T = V \\ S (Unreachable)</text>';

  const vS={x:sBoxX+35, y:sBoxY+58}, v1={x:sBoxX+115, y:sBoxY+48}, v2={x:sBoxX+115, y:sBoxY+95};
  const v3={x:tBoxX+45, y:tBoxY+48}, v4={x:tBoxX+45, y:tBoxY+95}, vT={x:tBoxX+125, y:tBoxY+58};

  svg+='<line x1="'+vS.x+'" y1="'+vS.y+'" x2="'+v1.x+'" y2="'+v1.y+'" stroke="#10b981" stroke-width="2"/>';
  svg+='<text x="'+((vS.x+v1.x)/2)+'" y="'+((vS.y+v1.y)/2-4)+'" fill="#10b981" font-size="6.5" font-family="monospace">f:12/12</text>';

  svg+='<line x1="'+vS.x+'" y1="'+vS.y+'" x2="'+v2.x+'" y2="'+v2.y+'" stroke="#10b981" stroke-width="2"/>';
  svg+='<text x="'+((vS.x+v2.x)/2)+'" y="'+((vS.y+v2.y)/2+12)+'" fill="#10b981" font-size="6.5" font-family="monospace">f:8/8</text>';

  svg+='<line x1="'+v3.x+'" y1="'+v3.y+'" x2="'+vT.x+'" y2="'+vT.y+'" stroke="#38bdf8" stroke-width="2"/>';
  svg+='<text x="'+((v3.x+vT.x)/2)+'" y="'+((v3.y+vT.y)/2-4)+'" fill="#38bdf8" font-size="6.5" font-family="monospace">f:12/12</text>';

  svg+='<line x1="'+v4.x+'" y1="'+v4.y+'" x2="'+vT.x+'" y2="'+vT.y+'" stroke="#38bdf8" stroke-width="2"/>';
  svg+='<text x="'+((v4.x+vT.x)/2)+'" y="'+((v4.y+vT.y)/2+12)+'" fill="#38bdf8" font-size="6.5" font-family="monospace">f:8/8</text>';

  svg+='<line x1="'+v1.x+'" y1="'+v1.y+'" x2="'+v3.x+'" y2="'+v3.y+'" stroke="#ef4444" stroke-width="2.5"/>';
  svg+='<text x="'+((v1.x+v3.x)/2)+'" y="'+((v1.y+v3.y)/2-6)+'" fill="#ef4444" font-size="7.5" font-family="monospace" font-weight="bold">c:12 (c_f=0! ✖)</text>';

  svg+='<line x1="'+v2.x+'" y1="'+v2.y+'" x2="'+v4.x+'" y2="'+v4.y+'" stroke="#ef4444" stroke-width="2.5"/>';
  svg+='<text x="'+((v2.x+v4.x)/2)+'" y="'+((v2.y+v4.y)/2-6)+'" fill="#ef4444" font-size="7.5" font-family="monospace" font-weight="bold">c:8 (c_f=0! ✖)</text>';

  const sbNodes=[
   {id:'s',x:vS.x,y:vS.y,col:'#10b981',fill:'#064e3b'},
   {id:'V1',x:v1.x,y:v1.y,col:'#10b981',fill:'#064e3b'},
   {id:'V2',x:v2.x,y:v2.y,col:'#10b981',fill:'#064e3b'},
   {id:'V3',x:v3.x,y:v3.y,col:'#38bdf8',fill:'#0f172a'},
   {id:'V4',x:v4.x,y:v4.y,col:'#38bdf8',fill:'#0f172a'},
   {id:'t',x:vT.x,y:vT.y,col:'#38bdf8',fill:'#0f172a'}
  ];
  sbNodes.forEach(nd=>{
   svg+='<circle cx="'+nd.x+'" cy="'+nd.y+'" r="12" fill="'+nd.fill+'" stroke="'+nd.col+'" stroke-width="2"/>';
   svg+='<text x="'+nd.x+'" y="'+(nd.y+4)+'" text-anchor="middle" fill="#dcebf2" font-size="7.5" font-weight="bold">'+nd.id+'</text>';
  });

  const cdX=cX+15, cdY=cY+162, cdW=cW-30, cdH=58;
  svg+='<rect x="'+cdX+'" y="'+cdY+'" width="'+cdW+'" height="'+cdH+'" rx="4" fill="#050b0e" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(cdX+10)+'" y="'+(cdY+16)+'" fill="#10b981" font-size="7.5" font-family="monospace">Total Maximum Flow: |f*| = f(s,V1) + f(s,V2) = 12 + 8 = 20 units</text>';
  svg+='<text x="'+(cdX+10)+'" y="'+(cdY+30)+'" fill="#ef4444" font-size="7.5" font-family="monospace">Min Cut (S, T): S = {s, V1, V2}, T = {V3, V4, t} ⟶ Capacity c(S, T) = 12 + 8 = 20 units</text>';
  svg+='<text x="'+(cdX+10)+'" y="'+(cdY+44)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">Residual Reachability Invariant: All edges crossing from S to T have c_f = 0 (Saturated!)</text>';

  const bX=465,bY=45,bW=210,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">MINIMUM CUT CAPACITY</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">c(S,T) = 20</text>';
  svg+='<text x="'+(bX+125)+'" y="'+(bY+50)+'" fill="#10b981" font-size="10">(Min Cut)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+80)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+80)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+98)+'" fill="#7e9bab" font-size="9">MAXIMUM FLOW VALUE</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+120)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">|f*| = 20 units</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+136)+'" fill="#8ba5b5" font-size="8">Weak Duality: |f| ≤ c(S, T) tight at optimum</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+150)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+150)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="#7e9bab" font-size="9">RESIDUAL REACHABILITY</text>';
  svg+=text(bX+bW/2,bY+190,'S = {v : s ⇝ v in G_f*}','#10b981',9.5);
  svg+=text(bX+bW/2,bY+208,'Zero augmenting paths from s to t',orange,8.5);
  svg+=text(360,305,'Sandbox Invariant: Min-cut capacity c(S, T) identically equals maximum flow |f*|; residual capacity across cut is strictly 0',soft,10);
  return svg;
 }

 if(cfg.slug==='string-matching-automata'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'KMP FAILURE FUNCTION (π-ARRAY) JUMP & FALLBACK EXPLORER','#e2f0f8',11);

  svg+='<text x="'+(cX+15)+'" y="'+(cY+20)+'" fill="#10b981" font-size="8.5" font-weight="bold">PATTERN P = "ABABCABAB" · π-ARRAY PRECOMPUTATION IN O(m) TIME</text>';

  const pat="ABABCABAB";
  const pi=[0,0,1,2,0,1,2,3,4];
  const tCells=pat.length;
  const cellW=36, cellH=22, tblX=cX+20, tblY=cY+32;

  svg+='<text x="'+(tblX-10)+'" y="'+(tblY+15)+'" text-anchor="end" fill="#64748b" font-size="7.5" font-family="monospace">P[j]:</text>';
  svg+='<text x="'+(tblX-10)+'" y="'+(tblY+38)+'" text-anchor="end" fill="'+orange+'" font-size="7.5" font-family="monospace">π[j]:</text>';

  for(let j=0; j<tCells; j++){
   const xPos=tblX+j*cellW;
   const isMatch=j<4;
   const isMismatch=(j===4);
   const bgCol=isMatch?'#064e3b':isMismatch?'#450a0a':'#0f172a';
   const borderCol=isMatch?'#10b981':isMismatch?'#ef4444':'#1e293b';
   
   svg+='<rect x="'+xPos+'" y="'+tblY+'" width="'+(cellW-3)+'" height="'+cellH+'" rx="3" fill="'+bgCol+'" stroke="'+borderCol+'" stroke-width="1.2"/>';
   svg+='<text x="'+(xPos+(cellW-3)/2)+'" y="'+(tblY+15)+'" text-anchor="middle" fill="#dcebf2" font-size="10" font-family="monospace" font-weight="bold">'+pat[j]+'</text>';

   svg+='<rect x="'+xPos+'" y="'+(tblY+24)+'" width="'+(cellW-3)+'" height="'+cellH+'" rx="3" fill="#081016" stroke="#1e3340" stroke-width="1"/>';
   svg+='<text x="'+(xPos+(cellW-3)/2)+'" y="'+(tblY+39)+'" text-anchor="middle" fill="'+(isMismatch?orange:'#38bdf8')+'" font-size="9" font-family="monospace" font-weight="bold">'+pi[j]+'</text>';

   svg+='<text x="'+(xPos+(cellW-3)/2)+'" y="'+(tblY-4)+'" text-anchor="middle" fill="#475569" font-size="7" font-family="monospace">'+j+'</text>';
  }

  const txtDemoY=cY+88;
  svg+='<text x="'+(cX+15)+'" y="'+(txtDemoY+12)+'" fill="#7dd3fc" font-size="8" font-weight="bold">TEXT STREAM T[0..11]: "A B A B D A B A C D A B"</text>';
  const textChars=["A","B","A","B","D","A","B","A","C","D","A","B"];
  for(let i=0; i<textChars.length; i++){
   const xPos=tblX+i*28;
   const isTMatch=(i<4);
   const isTMis=(i===4);
   const tBg=isTMatch?'#064e3b':isTMis?'#7f1d1d':'#0b161f';
   const tBdr=isTMatch?'#10b981':isTMis?'#ef4444':'#1e293b';
   svg+='<rect x="'+xPos+'" y="'+(txtDemoY+18)+'" width="25" height="20" rx="3" fill="'+tBg+'" stroke="'+tBdr+'" stroke-width="1"/>';
   svg+='<text x="'+(xPos+12.5)+'" y="'+(txtDemoY+32)+'" text-anchor="middle" fill="#e2f0f8" font-size="9" font-family="monospace" font-weight="bold">'+textChars[i]+'</text>';
  }

  const cdX=cX+15, cdY=cY+155, cdW=cW-30, cdH=65;
  svg+='<rect x="'+cdX+'" y="'+cdY+'" width="'+cdW+'" height="'+cdH+'" rx="4" fill="#050b0e" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(cdX+10)+'" y="'+(cdY+16)+'" fill="#ef4444" font-size="7.5" font-family="monospace">Mismatch at index i = 4: Text T[4] = \'D\' ≠ Pattern P[4] = \'C\'</text>';
  svg+='<text x="'+(cdX+10)+'" y="'+(cdY+30)+'" fill="#10b981" font-size="7.5" font-family="monospace">Matched Prefix: P[0..3] = "ABAB" ⟶ Longest Proper Suffix/Prefix π[3] = 2 ("AB")</text>';
  svg+='<text x="'+(cdX+10)+'" y="'+(cdY+44)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">Fallback Jump: j ⟶ π[3] = 2. Text pointer i stays at 4 (ZERO BACKTRACKING!)</text>';
  svg+='<text x="'+(cdX+10)+'" y="'+(cdY+58)+'" fill="#38bdf8" font-size="7.5" font-family="monospace">Next Comparison: T[4] (\'D\') vs P[2] (\'A\') directly without rewinding the text stream</text>';

  const bX=465,bY=45,bW=210,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">ACTIVE PREFIX STATE</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">j = 4 ⟶ 2</text>';
  svg+='<text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="#10b981" font-size="10">(π[3] = 2)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+80)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+80)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+98)+'" fill="#7e9bab" font-size="9">PRESERVED PREFIX</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+120)+'" fill="'+ink+'" font-size="14" font-family="monospace" font-weight="bold">"AB" (2 chars)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+136)+'" fill="#8ba5b5" font-size="8">Suffix of matched matches prefix of pattern</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+150)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+150)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+168)+'" fill="#7e9bab" font-size="9">TEXT POINTER INVARIANT</text>';
  svg+=text(bX+bW/2,bY+190,'Text Pointer i Never Decrements','#10b981',9.5);
  svg+=text(bX+bW/2,bY+208,'i strictly advances 0 ⟶ n-1',orange,8.5);
  svg+=text(360,305,'Sandbox Invariant: π-failure function directs pattern alignment fallback; text pointer i never moves backwards',soft,10);
  return svg;
 }

 if(cfg.slug==='greedy-minimum-spanning-trees'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'CUT PROPERTY & CYCLE DETECTION SANDBOX (|V| = '+p.input+')','#e2f0f8',11);

  svg+='<text x="'+(cX+15)+'" y="'+(cY+22)+'" fill="#10b981" font-size="8.5" font-weight="bold">CUT THEOREM: MIN-CROSSING EDGE e* ∈ CUT(S, V\\S) MUST BELONG TO MST</text>';

  const sBoxX=cX+20, sBoxY=cY+40, sBoxW=155, sBoxH=115;
  svg+='<rect x="'+sBoxX+'" y="'+sBoxY+'" width="'+sBoxW+'" height="'+sBoxH+'" rx="6" fill="#042f2e" stroke="#14b8a6" stroke-width="1.2" stroke-dasharray="3,2"/>';
  svg+='<text x="'+(sBoxX+12)+'" y="'+(sBoxY+18)+'" fill="#2dd4bf" font-size="8" font-weight="bold">CUT SET S (3 Vertices)</text>';

  const rBoxX=cX+225, rBoxY=cY+40, rBoxW=155, rBoxH=115;
  svg+='<rect x="'+rBoxX+'" y="'+rBoxY+'" width="'+rBoxW+'" height="'+rBoxH+'" rx="6" fill="#0c1929" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="3,2"/>';
  svg+='<text x="'+(rBoxX+12)+'" y="'+(rBoxY+18)+'" fill="#7dd3fc" font-size="8" font-weight="bold">CUT SET V \\ S (2 Vertices)</text>';

  const v0={x:sBoxX+35,y:sBoxY+55}, v1={x:sBoxX+120,y:sBoxY+50}, v2={x:sBoxX+75,y:sBoxY+95};
  const v3={x:rBoxX+45,y:rBoxY+50}, v4={x:rBoxX+115,y:rBoxY+85};

  svg+='<line x1="'+v0.x+'" y1="'+v0.y+'" x2="'+v1.x+'" y2="'+v1.y+'" stroke="#10b981" stroke-width="2"/>';
  svg+='<text x="'+((v0.x+v1.x)/2)+'" y="'+((v0.y+v1.y)/2-5)+'" fill="#10b981" font-size="6.5" font-family="monospace">w=2</text>';

  svg+='<line x1="'+v0.x+'" y1="'+v0.y+'" x2="'+v2.x+'" y2="'+v2.y+'" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3,2"/>';
  svg+='<text x="'+((v0.x+v2.x)/2-12)+'" y="'+((v0.y+v2.y)/2+5)+'" fill="#ef4444" font-size="6.5" font-family="monospace">w=8 ✖</text>';

  svg+='<line x1="'+v1.x+'" y1="'+v1.y+'" x2="'+v3.x+'" y2="'+v3.y+'" stroke="'+orange+'" stroke-width="2.5"/>';
  svg+='<text x="'+((v1.x+v3.x)/2)+'" y="'+((v1.y+v3.y)/2-7)+'" fill="'+orange+'" font-size="8" font-family="monospace" font-weight="bold">w=3 (CUT MIN!)</text>';

  svg+='<line x1="'+v2.x+'" y1="'+v2.y+'" x2="'+v4.x+'" y2="'+v4.y+'" stroke="#475569" stroke-width="1.5" stroke-dasharray="2,2"/>';
  svg+='<text x="'+((v2.x+v4.x)/2)+'" y="'+((v2.y+v4.y)/2-4)+'" fill="#64748b" font-size="6.5" font-family="monospace">w=7</text>';

  const sbNodes=[
   {id:'V0',x:v0.x,y:v0.y,col:'#10b981',fill:'#064e3b'},
   {id:'V1',x:v1.x,y:v1.y,col:orange,fill:'#431407'},
   {id:'V2',x:v2.x,y:v2.y,col:'#10b981',fill:'#064e3b'},
   {id:'V3',x:v3.x,y:v3.y,col:orange,fill:'#431407'},
   {id:'V4',x:v4.x,y:v4.y,col:'#38bdf8',fill:'#0f172a'}
  ];
  sbNodes.forEach(nd=>{
   svg+='<circle cx="'+nd.x+'" cy="'+nd.y+'" r="12" fill="'+nd.fill+'" stroke="'+nd.col+'" stroke-width="2"/>';
   svg+='<text x="'+nd.x+'" y="'+(nd.y+4)+'" text-anchor="middle" fill="#dcebf2" font-size="7.5" font-weight="bold">'+nd.id+'</text>';
  });

  const cdX=cX+15,cdY=cY+168,cdW=cW-30,cdH=52;
  svg+='<rect x="'+cdX+'" y="'+cdY+'" width="'+cdW+'" height="'+cdH+'" rx="4" fill="#050b0e" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+16)+'" fill="#38bdf8" font-size="7.5" font-family="monospace">Candidate Edge (V0, V2, w=8): Find(V0)==Find(V2) ⟶ Both in S ⟶ REJECT (Cycle!)</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+30)+'" fill="#10b981" font-size="7.5" font-family="monospace">Crossing Edge (V1, V3, w=3): Find(V1)!=Find(V3) ⟶ Cut Min Edge ⟶ ACCEPT into MST</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+44)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">DSU Union(Find(V1), Find(V3)): Merges S and V\\S via Union by Rank in O(α(V))</text>';

  const bX=465,bY=45,bW=210,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">MIN CROSSING WEIGHT</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">w = 3</text>';
  svg+='<text x="'+(bX+85)+'" y="'+(bY+50)+'" fill="#10b981" font-size="11">(Cut Minimum)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">CUT PROPERTY THEOREM</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="'+ink+'" font-size="14" font-family="monospace" font-weight="bold">e* = argmin w(u,v)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+140)+'" fill="#8ba5b5" font-size="8">Exchange proof guarantees MST membership</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+154)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+154)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+172)+'" fill="#7e9bab" font-size="9">CYCLE REJECTION</text>';
  svg+=text(bX+bW/2,bY+194,'Find(u) == Find(v) ⟹ Cycle','#ef4444',9.5);
  svg+=text(bX+bW/2,bY+212,'Discarded in O(α(V)) amortized time',orange,8.5);
  svg+=text(360,305,'Sandbox Invariant: Cut Property guarantees min-crossing edge in MST; DSU Find(u)==Find(v) prevents cycles in O(α(V))',soft,10);
  return svg;
 }

 if(cfg.slug==='dynamic-programming-memoization'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'BELLMAN RECURRENCE & OPTIMAL DECISION SANDBOX (n = '+p.input+', W = 100)','#e2f0f8',11);

  svg+='<text x="'+(cX+15)+'" y="'+(cY+22)+'" fill="#10b981" font-size="8.5" font-weight="bold">BELLMAN EQUATION: DP[i][w] = max(DP[i-1][w], DP[i-1][w - w_i] + v_i)</text>';

  const c1X=cX+50, c1Y=cY+50, cBoxW=105, cBoxH=42;
  const c2X=cX+245, c2Y=cY+50;
  const c3X=cX+140, c3Y=cY+118, c3W=120, c3H=46;

  svg+='<rect x="'+c1X+'" y="'+c1Y+'" width="'+cBoxW+'" height="'+cBoxH+'" rx="4" fill="#0f172a" stroke="#64748b" stroke-width="1.5"/>';
  svg+='<text x="'+(c1X+cBoxW/2)+'" y="'+(c1Y+14)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5" font-family="monospace">DP[3][40] (Exclude)</text>';
  svg+='<text x="'+(c1X+cBoxW/2)+'" y="'+(c1Y+32)+'" text-anchor="middle" fill="#dcebf2" font-size="14" font-weight="bold">Val: 62</text>';

  svg+='<rect x="'+c2X+'" y="'+c2Y+'" width="'+cBoxW+'" height="'+cBoxH+'" rx="4" fill="#064e3b" stroke="#10b981" stroke-width="1.5"/>';
  svg+='<text x="'+(c2X+cBoxW/2)+'" y="'+(c2Y+14)+'" text-anchor="middle" fill="#6ee7b7" font-size="7.5" font-family="monospace">DP[3][25] + v₄=35</text>';
  svg+='<text x="'+(c2X+cBoxW/2)+'" y="'+(c2Y+32)+'" text-anchor="middle" fill="#34d399" font-size="14" font-weight="bold">45 + 35 = 80</text>';

  svg+='<path d="M '+(c1X+cBoxW/2)+' '+(c1Y+cBoxH)+' Q '+(c1X+cBoxW/2)+' '+(c3Y+15)+' '+(c3X)+' '+(c3Y+15)+'" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3,2"/>';
  svg+='<polygon points="'+(c3X)+','+(c3Y+15)+' '+(c3X-6)+','+(c3Y+11)+' '+(c3X-6)+','+(c3Y+19)+'" fill="#64748b"/>';

  svg+='<path d="M '+(c2X+cBoxW/2)+' '+(c2Y+cBoxH)+' Q '+(c2X+cBoxW/2)+' '+(c3Y+15)+' '+(c3X+c3W)+' '+(c3Y+15)+'" fill="none" stroke="'+orange+'" stroke-width="2.5"/>';
  svg+='<polygon points="'+(c3X+c3W)+','+(c3Y+15)+' '+(c3X+c3W+6)+','+(c3Y+11)+' '+(c3X+c3W+6)+','+(c3Y+19)+'" fill="'+orange+'"/>';

  svg+='<rect x="'+c3X+'" y="'+c3Y+'" width="'+c3W+'" height="'+c3H+'" rx="5" fill="#431407" stroke="'+orange+'" stroke-width="2"/>';
  svg+='<text x="'+(c3X+c3W/2)+'" y="'+(c3Y+16)+'" text-anchor="middle" fill="#fca5a5" font-size="8" font-family="monospace">DP[4][40] = max(62, 80)</text>';
  svg+='<text x="'+(c3X+c3W/2)+'" y="'+(c3Y+36)+'" text-anchor="middle" fill="'+orange+'" font-size="16" font-weight="bold">80 (INCLUDE!)</text>';

  const cdX=cX+15,cdY=cY+172,cdW=cW-30,cdH=48;
  svg+='<rect x="'+cdX+'" y="'+cdY+'" width="'+cdW+'" height="'+cdH+'" rx="4" fill="#050b0e" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+16)+'" fill="#38bdf8" font-size="7.5" font-family="monospace">Item 4 Metadata: Weight w₄ = 15 kg · Valuation v₄ = 35 credits</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+30)+'" fill="#10b981" font-size="7.5" font-family="monospace">Evaluation: max(DP[3][40], DP[3][40 - 15] + 35) = max(62, 45 + 35) = 80</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+42)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">Backtracking Decision: x₄ = 1 (Item 4 selected; residual capacity = 25 kg)</text>';

  const bX=465,bY=45,bW=210,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">MAXIMUM CELL VALUE</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">80</text>';
  svg+='<text x="'+(bX+75)+'" y="'+(bY+50)+'" fill="#10b981" font-size="11">(+18 over exclude)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">OPTIMAL SUBSTRUCTURE</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="'+ink+'" font-size="15" font-family="monospace" font-weight="bold">DP[3][25] is Optimal</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+140)+'" fill="#8ba5b5" font-size="8">Cut-and-paste proof guarantees global max</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+154)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+154)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+172)+'" fill="#7e9bab" font-size="9">DECISION VECTOR</text>';
  svg+=text(bX+bW/2,bY+194,'x = [ 1, 0, 1, 1, ... ]','#38bdf8',9.5);
  svg+=text(bX+bW/2,bY+212,'O(n) linear backward reconstruction',orange,8.5);
  svg+=text(360,305,'Sandbox Invariant: Bellman recurrence balances marginal value against remaining capacity: max(62, 45+35) = 80',soft,10);
  return svg;
 }

 if(cfg.slug==='graph-traversal-shortest-paths'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'DIJKSTRA EDGE RELAXATION & SHORTEST PATH SANDBOX (|V| = '+p.input+')','#e2f0f8',11);

  // Top header for network sub-graph
  svg+='<text x="'+(cX+15)+'" y="'+(cY+22)+'" fill="#10b981" font-size="8.5" font-weight="bold">TRIANGULAR INEQUALITY RELAXATION: dist[v] &gt; dist[u] + w(u, v)</text>';

  // Vertices coordinates
  const sX=cX+60,sY=cY+90;
  const uX=cX+180,uY=cY+55;
  const aX=cX+180,aY=cY+130;
  const vX=cX+320,vY=cY+90;

  // Edges: S -> U (w=4), S -> A (w=5), A -> V (w=7, old path), U -> V (w=3, relaxing edge)
  // S -> U
  svg+='<line x1="'+sX+'" y1="'+sY+'" x2="'+uX+'" y2="'+uY+'" stroke="#10b981" stroke-width="2"/>';
  svg+='<text x="'+((sX+uX)/2-10)+'" y="'+((sY+uY)/2-6)+'" fill="#10b981" font-size="7.5" font-weight="bold">w=4</text>';

  // S -> A
  svg+='<line x1="'+sX+'" y1="'+sY+'" x2="'+aX+'" y2="'+aY+'" stroke="#334155" stroke-width="1.5"/>';
  svg+='<text x="'+((sX+aX)/2-10)+'" y="'+((sY+aY)/2+14)+'" fill="#64748b" font-size="7.5" font-weight="bold">w=5</text>';

  // A -> V (Old path, weight 7, total cost 12)
  svg+='<line x1="'+aX+'" y1="'+aY+'" x2="'+vX+'" y2="'+vY+'" stroke="#475569" stroke-width="1.5" stroke-dasharray="3,2"/>';
  svg+='<text x="'+((aX+vX)/2+10)+'" y="'+((aY+vY)/2+14)+'" fill="#64748b" font-size="7.5">w=7 (old: 5+7=12)</text>';

  // U -> V (Relaxing edge, weight 3, new cost 4+3=7)
  svg+='<line x1="'+uX+'" y1="'+uY+'" x2="'+vX+'" y2="'+vY+'" stroke="'+orange+'" stroke-width="2.5"/>';
  svg+='<text x="'+((uX+vX)/2+10)+'" y="'+((uY+vY)/2-6)+'" fill="'+orange+'" font-size="8" font-weight="bold">w=3 (RELAX! 4+3=7)</text>';

  // Draw vertices
  const gNodes=[
   {name:'S',x:sX,y:sY,dist:'0',col:'#10b981',fill:'#064e3b'},
   {name:'U',x:uX,y:uY,dist:'4',col:'#10b981',fill:'#064e3b'},
   {name:'A',x:aX,y:aY,dist:'5',col:'#334155',fill:'#0f172a'},
   {name:'V',x:vX,y:vY,dist:'12 ⟶ 7',col:orange,fill:'#431407'}
  ];

  gNodes.forEach(nd=>{
   svg+='<circle cx="'+nd.x+'" cy="'+nd.y+'" r="15" fill="'+nd.fill+'" stroke="'+nd.col+'" stroke-width="2"/>';
   svg+='<text x="'+nd.x+'" y="'+(nd.y+4)+'" text-anchor="middle" fill="#dcebf2" font-size="8.5" font-weight="bold">'+nd.name+'</text>';
   svg+='<text x="'+nd.x+'" y="'+(nd.y+26)+'" text-anchor="middle" fill="'+nd.col+'" font-size="7" font-family="monospace">d:'+nd.dist+'</text>';
  });

  // Code sequence box at bottom
  const cdX=cX+15,cdY=cY+148,cdW=cW-30,cdH=72;
  svg+='<rect x="'+cdX+'" y="'+cdY+'" width="'+cdW+'" height="'+cdH+'" rx="4" fill="#050b0e" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+16)+'" fill="#38bdf8" font-size="8" font-weight="bold">DIJKSTRA EDGE RELAXATION PRIMITIVE (TRIANGULAR SHORTENING)</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+32)+'" fill="#10b981" font-size="7.5" font-family="monospace">1: if (dist[v] &gt; dist[u] + w(u, v)) { // 12 &gt; 4 + 3</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+46)+'" fill="#10b981" font-size="7.5" font-family="monospace">2:   dist[v] = dist[u] + w(u, v); prev[v] = u; // Tentative dist updated to 7</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+60)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">3:   min_heap.decrease_key(v, 7); }           // O(log V) priority queue shift</text>';

  const bX=465,bY=45,bW=210,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">TENTATIVE DISTANCE DELTA</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">12 ⟶ 7</text>';
  svg+='<text x="'+(bX+110)+'" y="'+(bY+50)+'" fill="#10b981" font-size="11">(-5 cost)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">GREEDY CHOICE PROPERTY</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">dist[u*] = δ(S, u*)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+140)+'" fill="#8ba5b5" font-size="8">Optimal sub-structure guarantees finality</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+154)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+154)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+172)+'" fill="#7e9bab" font-size="9">WEIGHT NON-NEGATIVITY BOUND</text>';
  svg+=text(bX+bW/2,bY+194,'w(u, v) ≥ 0 required','#38bdf8',9.5);
  svg+=text(bX+bW/2,bY+212,'Negative weights require Bellman-Ford',orange,8.5);
  svg+=text(360,305,'Sandbox Invariant: Dijkstra greedily settles minimal unvisited vertex; negative edges break triangular inequality invariant',soft,10);
  return svg;
 }

 if(cfg.slug==='hash-tables-collision-resolution'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'PRIMARY CLUSTERING CASCADE & AVALANCHE SANDBOX (n = '+p.input+')','#e2f0f8',11);

  // Top header for array segment
  svg+='<text x="'+(cX+15)+'" y="'+(cY+22)+'" fill="#ef4444" font-size="8.5" font-weight="bold">LINEAR PROBE GRAVITATIONAL CLUSTER (SLOTS 3..7 OCCUPIED · L = 5)</text>';

  // Contiguous slot array representation
  const arrY=cY+42,slotW=28,slotH=38,startX=cX+18;
  const slots=[
   {idx:0,val:'NULL',occ:false},{idx:1,val:'NULL',occ:false},{idx:2,val:'NULL',occ:false},
   {idx:3,val:'512',occ:true},{idx:4,val:'108',occ:true},{idx:5,val:'934',occ:true},
   {idx:6,val:'427',occ:true},{idx:7,val:'615',occ:true},{idx:8,val:'+743',occ:true,isNew:true},
   {idx:9,val:'NULL',occ:false},{idx:10,val:'NULL',occ:false},{idx:11,val:'NULL',occ:false}
  ];

  slots.forEach((s,i)=>{
   const sX=startX+i*(slotW+3);
   const fillCol=s.isNew?'#431407':s.occ?'#1e293b':'#050b0e';
   const strokeCol=s.isNew?orange:s.occ?'#ef4444':'#1e3340';
   svg+='<rect x="'+sX+'" y="'+arrY+'" width="'+slotW+'" height="'+slotH+'" rx="3" fill="'+fillCol+'" stroke="'+strokeCol+'" stroke-width="'+(s.isNew||s.occ?1.5:1)+'"/>';
   svg+='<text x="'+(sX+slotW/2)+'" y="'+(arrY+12)+'" text-anchor="middle" fill="#64748b" font-size="6" font-family="monospace">['+s.idx+']</text>';
   svg+='<text x="'+(sX+slotW/2)+'" y="'+(arrY+28)+'" text-anchor="middle" fill="'+(s.isNew?orange:s.occ?'#fca5a5':'#334155')+'" font-size="7" font-weight="bold">'+s.val+'</text>';
  });

  // Collision Hop Arrows from slot 4 to slot 8
  const hopY=arrY-10;
  svg+='<path d="M '+(startX+4*(slotW+3)+slotW/2)+' '+arrY+' Q '+(startX+6*(slotW+3))+' '+(arrY-22)+' '+(startX+8*(slotW+3)+slotW/2)+' '+arrY+'" fill="none" stroke="'+orange+'" stroke-width="2" stroke-dasharray="3,2"/>';
  svg+='<polygon points="'+(startX+8*(slotW+3)+slotW/2)+','+arrY+' '+(startX+8*(slotW+3)+slotW/2-4)+','+(arrY-7)+' '+(startX+8*(slotW+3)+slotW/2+4)+','+(arrY-7)+'" fill="'+orange+'"/>';
  svg+='<text x="'+(startX+6*(slotW+3))+'" y="'+(arrY-25)+'" text-anchor="middle" fill="'+orange+'" font-size="7" font-weight="bold">Key 743 hashes to [4] ⟶ 4 Collision Hops ⟶ Committed at [8]</text>';

  // Probability comparison box
  const prX=cX+15,prY=cY+92,prW=cW-30,prH=50;
  svg+='<rect x="'+prX+'" y="'+prY+'" width="'+prW+'" height="'+prH+'" rx="4" fill="#050b0e" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(prX+12)+'" y="'+(prY+16)+'" fill="#38bdf8" font-size="8" font-weight="bold">GRAVITATIONAL ATTRACTION PROBABILITY THEOREM</text>';
  svg+='<text x="'+(prX+12)+'" y="'+(prY+30)+'" fill="#dcebf2" font-size="7.5" font-family="monospace">P(hitting empty slot [8]) = (L + 1) / m = (5 + 1) / 1000 = 0.0060 (6× baseline!)</text>';
  svg+='<text x="'+(prX+12)+'" y="'+(prY+42)+'" fill="#ef4444" font-size="7" font-family="monospace">P(hitting isolated slot [0]) = 1 / m = 1 / 1000 = 0.0010</text>';

  // Code sequence box
  const cdX=cX+15,cdY=cY+148,cdW=cW-30,cdH=72;
  svg+='<rect x="'+cdX+'" y="'+cdY+'" width="'+cdW+'" height="'+cdH+'" rx="4" fill="#050b0e" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+16)+'" fill="#10b981" font-size="8" font-weight="bold">DOUBLE HASHING RESOLUTION (AVOIDING CLUSTERING CASCADE)</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+32)+'" fill="#38bdf8" font-size="7.5" font-family="monospace">1: int h1 = hash1(k) % m; int h2 = 1 + (hash2(k) % (m - 1)); // Coprime stride</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+46)+'" fill="#10b981" font-size="7.5" font-family="monospace">2: for (int i = 0; i &lt; m; ++i) { int idx = (h1 + i * h2) % m; // Divergent cyclic path</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+60)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">3:   if (table[idx] == NULL) { table[idx] = k; break; } } // Zero cluster merging</text>';

  const bX=465,bY=45,bW=210,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">CLUSTER ATTRACTION MULTIPLIER</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">6.0×</text>';
  svg+='<text x="'+(bX+85)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="10">vs Isolated Slot</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">KNUTH CLUSTERING PENALTY</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">(1 − α)⁻²</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+140)+'" fill="#8ba5b5" font-size="8">Quadratic expansion of probe length</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+154)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+154)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+172)+'" fill="#7e9bab" font-size="9">DOUBLE HASHING COUNTERMEASURE</text>';
  svg+=text(bX+bW/2,bY+194,'h(k,i) = (h₁ + i·h₂) mod m','#38bdf8',9.5);
  svg+=text(bX+bW/2,bY+212,'Strict gcd(h₂, m) = 1 (Coprimality)',orange,8.5);
  svg+=text(360,305,'Sandbox Invariant: In linear probing, contiguous runs act as gravitational attractors, expanding at rate proportional to cluster length',soft,10);
  return svg;
 }

 if(cfg.slug==='binary-heaps-priority-queues'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'FLOYD SIFT-DOWN & BOUNCE OPTIMIZATION SANDBOX (n = '+p.input+')','#e2f0f8',11);

  // Left Section: Step 1 & Step 2 Comparison breakdown
  svg+='<text x="'+(cX+100)+'" y="'+(cY+22)+'" text-anchor="middle" fill="#ef4444" font-size="8.5" font-weight="bold">SIFT STEP 1: CHILD COMPARISON</text>';
  svg+='<text x="'+(cX+290)+'" y="'+(cY+22)+'" text-anchor="middle" fill="#10b981" font-size="8.5" font-weight="bold">SIFT STEP 2: PARENT SWAP</text>';

  // Step 1: Parent 15 with Children 82 and 68
  const p1X=cX+100,p1Y=cY+50;
  svg+='<circle cx="'+p1X+'" cy="'+p1Y+'" r="14" fill="#1e293b" stroke="#ef4444" stroke-width="1.5"/>';
  svg+='<text x="'+p1X+'" y="'+(p1Y+4)+'" text-anchor="middle" fill="#fed7aa" font-size="8" font-weight="bold">15</text>';
  svg+='<text x="'+(p1X+20)+'" y="'+(p1Y+3)+'" fill="#ef4444" font-size="7" font-family="monospace">P[0]</text>';

  // Left child 82
  const c1X=cX+65,c1Y=cY+95;
  svg+='<line x1="'+p1X+'" y1="'+(p1Y+14)+'" x2="'+c1X+'" y2="'+(c1Y-14)+'" stroke="#10b981" stroke-width="2"/>';
  svg+='<circle cx="'+c1X+'" cy="'+c1Y+'" r="13" fill="#064e3b" stroke="#10b981" stroke-width="2"/>';
  svg+='<text x="'+c1X+'" y="'+(c1Y+4)+'" text-anchor="middle" fill="#a7f3d0" font-size="8" font-weight="bold">82</text>';
  svg+='<text x="'+(c1X-20)+'" y="'+(c1Y+3)+'" text-anchor="end" fill="#10b981" font-size="7" font-family="monospace">L[1] WIN</text>';

  // Right child 68
  const c2X=cX+135,c2Y=cY+95;
  svg+='<line x1="'+p1X+'" y1="'+(p1Y+14)+'" x2="'+c2X+'" y2="'+(c2Y-14)+'" stroke="#334155" stroke-width="1.5"/>';
  svg+='<circle cx="'+c2X+'" cy="'+c2Y+'" r="13" fill="#0f172a" stroke="#475569" stroke-width="1.5"/>';
  svg+='<text x="'+c2X+'" y="'+(c2Y+4)+'" text-anchor="middle" fill="#94a3b8" font-size="8" font-weight="bold">68</text>';
  svg+='<text x="'+(c2X+20)+'" y="'+(c2Y+3)+'" fill="#64748b" font-size="7" font-family="monospace">R[2]</text>';

  // Child vs child comparison indicator
  svg+='<path d="M '+(c1X+14)+' '+(c1Y)+' Q '+((c1X+c2X)/2)+' '+(c1Y+15)+' '+(c2X-14)+' '+(c1Y)+'" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="2,2"/>';
  svg+='<text x="'+((c1X+c2X)/2)+'" y="'+(c1Y+24)+'" text-anchor="middle" fill="#38bdf8" font-size="6.5">Comp 1: 82 &gt; 68 (select left)</text>';

  // Transition Arrow between step 1 and step 2
  const trX=cX+195;
  svg+='<path d="M '+(trX-10)+' '+(cY+70)+' L '+(trX+10)+' '+(cY+70)+'" fill="none" stroke="'+orange+'" stroke-width="2"/>';
  svg+='<polygon points="'+(trX+12)+','+(cY+70)+' '+(trX+6)+','+(cY+66)+' '+(trX+6)+','+(cY+74)+'" fill="'+orange+'"/>';
  svg+='<text x="'+trX+'" y="'+(cY+86)+'" text-anchor="middle" fill="'+orange+'" font-size="7">Comp 2: 82 &gt; 15</text>';

  // Step 2: After Swap
  const p2X=cX+290,p2Y=cY+50;
  svg+='<circle cx="'+p2X+'" cy="'+p2Y+'" r="14" fill="#064e3b" stroke="#10b981" stroke-width="2"/>';
  svg+='<text x="'+p2X+'" y="'+(p2Y+4)+'" text-anchor="middle" fill="#a7f3d0" font-size="8" font-weight="bold">82</text>';
  svg+='<text x="'+(p2X+20)+'" y="'+(p2Y+3)+'" fill="#10b981" font-size="7" font-family="monospace">P[0]</text>';

  const nc1X=cX+255,nc1Y=cY+95;
  svg+='<line x1="'+p2X+'" y1="'+(p2Y+14)+'" x2="'+nc1X+'" y2="'+(nc1Y-14)+'" stroke="#10b981" stroke-width="2"/>';
  svg+='<circle cx="'+nc1X+'" cy="'+nc1Y+'" r="13" fill="#431407" stroke="'+orange+'" stroke-width="1.5"/>';
  svg+='<text x="'+nc1X+'" y="'+(nc1Y+4)+'" text-anchor="middle" fill="#fed7aa" font-size="8" font-weight="bold">15</text>';
  svg+='<text x="'+(nc1X-20)+'" y="'+(nc1Y+3)+'" text-anchor="end" fill="'+orange+'" font-size="7" font-family="monospace">Sunk L[1]</text>';

  const nc2X=cX+325,nc2Y=cY+95;
  svg+='<line x1="'+p2X+'" y1="'+(p2Y+14)+'" x2="'+nc2X+'" y2="'+(nc2Y-14)+'" stroke="#334155" stroke-width="1.5"/>';
  svg+='<circle cx="'+nc2X+'" cy="'+nc2Y+'" r="13" fill="#0f172a" stroke="#475569" stroke-width="1.5"/>';
  svg+='<text x="'+nc2X+'" y="'+(nc2Y+4)+'" text-anchor="middle" fill="#94a3b8" font-size="8" font-weight="bold">68</text>';
  svg+='<text x="'+(nc2X+20)+'" y="'+(nc2Y+3)+'" fill="#64748b" font-size="7" font-family="monospace">R[2]</text>';

  // Code Sequence Box at Bottom
  const cdX=cX+15,cdY=cY+142,cdW=cW-30,cdH=78;
  svg+='<rect x="'+cdX+'" y="'+cdY+'" width="'+cdW+'" height="'+cdH+'" rx="4" fill="#050b0e" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+16)+'" fill="#38bdf8" font-size="8" font-weight="bold">FLOYD SIFT-DOWN PRIMITIVE (EXACTLY 2 COMPARISONS / LEVEL)</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+32)+'" fill="#10b981" font-size="7.5" font-family="monospace">1: int c = (i &lt;&lt; 1) + 1;                  // Left child index</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+46)+'" fill="#10b981" font-size="7.5" font-family="monospace">2: if (c+1 &lt; n &amp;&amp; A[c+1] &gt; A[c]) c++;      // Comp 1: Select max child</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+60)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">3: if (A[c] &gt; A[i]) { swap(A[i], A[c]); i = c; } // Comp 2: Sink parent</text>';

  const bX=465,bY=45,bW=210,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">COMPARISONS PER LEVEL</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">2 comps</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+70)+'" fill="#8ba5b5" font-size="8">1 child-child + 1 parent-child</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">FLOYD BOUNCE OPTIMIZATION</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">1 comp / level</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+140)+'" fill="#8ba5b5" font-size="8">Sink to leaf, then sift up 1-2 steps</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+154)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+154)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+172)+'" fill="#7e9bab" font-size="9">HEAPIFY BOUND CONVERGENCE</text>';
  svg+=text(bX+bW/2,bY+194,'∑ (h / 2ʰ) ≤ 2 (Geometric Series)','#38bdf8',9.5);
  svg+=text(bX+bW/2,bY+212,'Strict C(n) ≤ 2n comparisons',orange,8.5);
  svg+=text(360,305,'Sandbox Invariant: Sift-down compares children first (1 comp) then parent (1 comp), sinking non-leaves in O(1) average time',soft,10);
  return svg;
 }

 if(cfg.slug==='binary-search-trees'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'AVL TREE ROTATION & REBALANCING SANDBOX (n = '+p.input+')','#e2f0f8',11);

  // Before Rotation (LL Heavy) - Left Column
  svg+='<text x="'+(cX+100)+'" y="'+(cY+22)+'" text-anchor="middle" fill="#ef4444" font-size="8.5" font-weight="bold">BEFORE: LL-HEAVY (|BF| = 2)</text>';

  // Node Z (Root, key 50, BF = +2)
  const zX=cX+100,zY=cY+45;
  svg+='<circle cx="'+zX+'" cy="'+zY+'" r="14" fill="#450a0a" stroke="#ef4444" stroke-width="2"/>';
  svg+='<text x="'+zX+'" y="'+(zY+4)+'" text-anchor="middle" fill="#fca5a5" font-size="8" font-weight="bold">50</text>';
  svg+='<text x="'+(zX+22)+'" y="'+(zY+3)+'" fill="#ef4444" font-size="7" font-family="monospace">BF:+2</text>';

  // Node Y (Left child, key 25, BF = +1)
  const yX=cX+60,yY=cY+85;
  svg+='<line x1="'+zX+'" y1="'+(zY+14)+'" x2="'+yX+'" y2="'+(yY-14)+'" stroke="#ef4444" stroke-width="2"/>';
  svg+='<circle cx="'+yX+'" cy="'+yY+'" r="14" fill="#1e293b" stroke="'+orange+'" stroke-width="1.5"/>';
  svg+='<text x="'+yX+'" y="'+(yY+4)+'" text-anchor="middle" fill="#fed7aa" font-size="8" font-weight="bold">25</text>';
  svg+='<text x="'+(yX-22)+'" y="'+(yY+3)+'" text-anchor="end" fill="'+orange+'" font-size="7" font-family="monospace">BF:+1</text>';

  // Node X (Grandchild, key 12, BF = 0)
  const xX=cX+30,xY=cY+125;
  svg+='<line x1="'+yX+'" y1="'+(yY+14)+'" x2="'+xX+'" y2="'+(xY-14)+'" stroke="'+orange+'" stroke-width="2"/>';
  svg+='<circle cx="'+xX+'" cy="'+xY+'" r="12" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
  svg+='<text x="'+xX+'" y="'+(xY+3.5)+'" text-anchor="middle" fill="#bae6fd" font-size="7.5" font-weight="bold">12</text>';

  // Rotation Arrow in middle
  const arrX=cX+200;
  svg+='<path d="M '+(arrX-15)+' '+(cY+75)+' Q '+arrX+' '+(cY+55)+' '+(arrX+15)+' '+(cY+75)+'" fill="none" stroke="#10b981" stroke-width="2.5"/>';
  svg+='<polygon points="'+(arrX+15)+','+(cY+75)+' '+(arrX+9)+','+(cY+68)+' '+(arrX+18)+','+(cY+67)+'" fill="#10b981"/>';
  svg+='<text x="'+arrX+'" y="'+(cY+92)+'" text-anchor="middle" fill="#10b981" font-size="8" font-weight="bold">RotateRight(50)</text>';

  // After Rotation (Balanced) - Right Column
  svg+='<text x="'+(cX+300)+'" y="'+(cY+22)+'" text-anchor="middle" fill="#10b981" font-size="8.5" font-weight="bold">AFTER: EQUILIBRIUM (|BF| = 0)</text>';

  // New Root Y (key 25, BF = 0)
  const nyX=cX+300,nyY=cY+45;
  svg+='<circle cx="'+nyX+'" cy="'+nyY+'" r="14" fill="#064e3b" stroke="#10b981" stroke-width="2"/>';
  svg+='<text x="'+nyX+'" y="'+(nyY+4)+'" text-anchor="middle" fill="#a7f3d0" font-size="8" font-weight="bold">25</text>';
  svg+='<text x="'+(nyX+22)+'" y="'+(nyY+3)+'" fill="#10b981" font-size="7" font-family="monospace">BF:0</text>';

  // Left child X (key 12, BF = 0)
  const nxX=cX+260,nxY=cY+85;
  svg+='<line x1="'+nyX+'" y1="'+(nyY+14)+'" x2="'+nxX+'" y2="'+(nxY-14)+'" stroke="#10b981" stroke-width="2"/>';
  svg+='<circle cx="'+nxX+'" cy="'+nxY+'" r="13" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
  svg+='<text x="'+nxX+'" y="'+(nxY+4)+'" text-anchor="middle" fill="#bae6fd" font-size="7.5" font-weight="bold">12</text>';

  // Right child Z (key 50, BF = 0)
  const nzX=cX+340,nzY=cY+85;
  svg+='<line x1="'+nyX+'" y1="'+(nyY+14)+'" x2="'+nzX+'" y2="'+(nzY-14)+'" stroke="#10b981" stroke-width="2"/>';
  svg+='<circle cx="'+nzX+'" cy="'+nzY+'" r="13" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>';
  svg+='<text x="'+nzX+'" y="'+(nzY+4)+'" text-anchor="middle" fill="#bae6fd" font-size="7.5" font-weight="bold">50</text>';

  // Code Sequence Box at Bottom
  const cdX=cX+15,cdY=cY+145,cdW=cW-30,cdH=75;
  svg+='<rect x="'+cdX+'" y="'+cdY+'" width="'+cdW+'" height="'+cdH+'" rx="4" fill="#050b0e" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+16)+'" fill="#38bdf8" font-size="8" font-weight="bold">BRANCHLESS ROTATION PRIMITIVE (O(1) TIME · 3 POINTER UPDATES)</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+32)+'" fill="#10b981" font-size="7.5" font-family="monospace">1: Node* y = z-&gt;left;           // Elevate left child</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+46)+'" fill="#10b981" font-size="7.5" font-family="monospace">2: z-&gt;left = y-&gt;right;          // Adopt subtree T2</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+60)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">3: y-&gt;right = z;                // Subtree root becomes right child</text>';

  const bX=465,bY=45,bW=210,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">BALANCE EQUILIBRIUM RESTORED</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">ΔBF = 2 ⟶ 0</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+70)+'" fill="#8ba5b5" font-size="8">Single rotation reduces subtree height by 1</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">ROTATION COMPLEXITY</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">Strict O(1)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+140)+'" fill="#8ba5b5" font-size="8">3 pointer updates, zero key reallocations</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+154)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+154)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+172)+'" fill="#7e9bab" font-size="9">FIBONACCI HEIGHT BOUND</text>';
  svg+=text(bX+bW/2,bY+194,'h < 1.4404 · log₂(n + 2) - 0.328','#38bdf8',9.5);
  svg+=text(bX+bW/2,bY+212,'Golden ratio base φ = (1+√5)/2',orange,8.5);
  svg+=text(360,305,'Rotation Sandbox: Local O(1) single and double rotations restore balance without traversing whole tree',soft,10);
  return svg;
 }

 if(cfg.slug==='linked-list-architectures'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'SENTINEL SPLICING & BRANCHLESS NODE INSERTION (n = '+p.input+')','#e2f0f8',11);

  // Sentinel Head Box
  const shX=cX+20,shY=cY+40,shW=70,shH=65;
  svg+='<rect x="'+shX+'" y="'+shY+'" width="'+shW+'" height="'+shH+'" rx="4" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.5"/>';
  svg+='<text x="'+(shX+shW/2)+'" y="'+(shY+18)+'" text-anchor="middle" fill="#38bdf8" font-size="8" font-weight="bold">HEAD SENTINEL</text>';
  svg+='<text x="'+(shX+shW/2)+'" y="'+(shY+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7" font-family="monospace">prev: NULL</text>';
  svg+='<text x="'+(shX+shW/2)+'" y="'+(shY+50)+'" text-anchor="middle" fill="#6ee7b7" font-size="7" font-family="monospace">next: &gt;&gt;</text>';

  // Inserted / Target Node
  const ndX=cX+120,ndY=cY+35,ndW=90,ndH=75;
  svg+='<rect x="'+ndX+'" y="'+ndY+'" width="'+ndW+'" height="'+ndH+'" rx="4" fill="#132733" stroke="'+orange+'" stroke-width="2"/>';
  svg+='<text x="'+(ndX+ndW/2)+'" y="'+(ndY+18)+'" text-anchor="middle" fill="'+orange+'" font-size="8.5" font-weight="bold">NEW NODE (X)</text>';
  svg+='<text x="'+(ndX+ndW/2)+'" y="'+(ndY+34)+'" text-anchor="middle" fill="#dcebf2" font-size="7.5" font-family="monospace">val: 0xDEADBEEF</text>';
  svg+='<text x="'+(ndX+ndW/2)+'" y="'+(ndY+50)+'" text-anchor="middle" fill="#38bdf8" font-size="7" font-family="monospace">prev: &amp;Head</text>';
  svg+='<text x="'+(ndX+ndW/2)+'" y="'+(ndY+64)+'" text-anchor="middle" fill="#10b981" font-size="7" font-family="monospace">next: &amp;Tail</text>';

  // Target Node / Sentinel Tail Box
  const stX=cX+240,stY=cY+40,stW=70,stH=65;
  svg+='<rect x="'+stX+'" y="'+stY+'" width="'+stW+'" height="'+stH+'" rx="4" fill="#431407" stroke="#ef4444" stroke-width="1.5"/>';
  svg+='<text x="'+(stX+stW/2)+'" y="'+(stY+18)+'" text-anchor="middle" fill="#f87171" font-size="8" font-weight="bold">TAIL SENTINEL</text>';
  svg+='<text x="'+(stX+stW/2)+'" y="'+(stY+34)+'" text-anchor="middle" fill="#6ee7b7" font-size="7" font-family="monospace">prev: &lt;&lt;</text>';
  svg+='<text x="'+(stX+stW/2)+'" y="'+(stY+50)+'" text-anchor="middle" fill="#94a3b8" font-size="7" font-family="monospace">next: NULL</text>';

  // Splice Pointer Arrows
  // Forward arrow Head -> Node
  svg+='<path d="M '+(shX+shW)+' '+(shY+25)+' L '+(ndX)+' '+(shY+25)+'" fill="none" stroke="#10b981" stroke-width="2"/>';
  svg+='<polygon points="'+ndX+','+(shY+25)+' '+(ndX-6)+','+(shY+21)+' '+(ndX-6)+','+(shY+29)+'" fill="#10b981"/>';

  // Backward arrow Node -> Head
  svg+='<path d="M '+(ndX)+' '+(shY+45)+' L '+(shX+shW)+' '+(shY+45)+'" fill="none" stroke="'+orange+'" stroke-width="2"/>';
  svg+='<polygon points="'+(shX+shW)+','+(shY+45)+' '+(shX+shW+6)+','+(shY+41)+' '+(shX+shW+6)+','+(shY+49)+'" fill="'+orange+'"/>';

  // Forward arrow Node -> Tail
  svg+='<path d="M '+(ndX+ndW)+' '+(stY+25)+' L '+(stX)+' '+(stY+25)+'" fill="none" stroke="#10b981" stroke-width="2"/>';
  svg+='<polygon points="'+stX+','+(stY+25)+' '+(stX-6)+','+(stY+21)+' '+(stX-6)+','+(stY+29)+'" fill="#10b981"/>';

  // Backward arrow Tail -> Node
  svg+='<path d="M '+(stX)+' '+(stY+45)+' L '+(ndX+ndW)+' '+(stY+45)+'" fill="none" stroke="'+orange+'" stroke-width="2"/>';
  svg+='<polygon points="'+(ndX+ndW)+','+(stY+45)+' '+(ndX+ndW+6)+','+(stY+41)+' '+(ndX+ndW+6)+','+(stY+49)+'" fill="'+orange+'"/>';

  // Branchless Code Box at bottom
  const cdX=cX+15,cdY=cY+125,cdW=cW-30,cdH=90;
  svg+='<rect x="'+cdX+'" y="'+cdY+'" width="'+cdW+'" height="'+cdH+'" rx="4" fill="#050b0e" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+18)+'" fill="#38bdf8" font-size="8" font-weight="bold">BRANCHLESS 4-POINTER SPLICE (ZERO CONDITIONAL JUMPS)</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+36)+'" fill="#10b981" font-size="7.5" font-family="monospace">1: newNode-&gt;next = target;          // Store target successor</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+52)+'" fill="#10b981" font-size="7.5" font-family="monospace">2: newNode-&gt;prev = target-&gt;prev;    // Link to target predecessor</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+68)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">3: target-&gt;prev-&gt;next = newNode;    // Splice forward link</text>';
  svg+='<text x="'+(cdX+12)+'" y="'+(cdY+84)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">4: target-&gt;prev = newNode;          // Splice backward link</text>';

  const bX=465,bY=45,bW=210,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">BRANCH PREDICTION PENALTY</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">0 stalls</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+70)+'" fill="#8ba5b5" font-size="8">Sentinel eliminates if(head == NULL) checks</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">COMPLEXITY PROFILE</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">O(1) Strict</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+140)+'" fill="#8ba5b5" font-size="8">Exactly 4 pointer writes, 0 shifts</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+154)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+154)+'" stroke="#1e3340"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+172)+'" fill="#7e9bab" font-size="9">LINUX INTRUSIVE ARCHITECTURE</text>';
  svg+=text(bX+bW/2,bY+194,'struct list_head { next, prev }','#38bdf8',9.5);
  svg+=text(bX+bW/2,bY+212,'container_of() macro retrieves payload',orange,8.5);
  svg+=text(360,305,'Sentinel Sandbox: Sentinels eliminate branch mispredictions and simplify edge cases into standard splices',soft,10);
  return svg;
 }

 if(cfg.slug==='queue-buffer-management'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'PRODUCER-CONSUMER PIPELINE & BACKPRESSURE FLOW (n = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  // Producer Box on Left
  const prX=cX+20,prY=cY+35,prW=90,prH=110;
  svg+='<rect x="'+prX+'" y="'+prY+'" width="'+prW+'" height="'+prH+'" rx="4" fill="#0f291e" stroke="#10b981" stroke-width="1.5"/>';
  svg+='<text x="'+(prX+prW/2)+'" y="'+(prY+20)+'" text-anchor="middle" fill="#10b981" font-size="9" font-weight="bold">PRODUCER</text>';
  svg+='<text x="'+(prX+prW/2)+'" y="'+(prY+40)+'" text-anchor="middle" fill="#6ee7b7" font-size="7.5">Rate: λ_p pkts/s</text>';
  svg+='<text x="'+(prX+prW/2)+'" y="'+(prY+58)+'" text-anchor="middle" fill="#dcebf2" font-size="7.5" font-family="monospace">Stream Gen</text>';
  svg+='<rect x="'+(prX+10)+'" y="'+(prY+72)+'" width="'+(prW-20)+'" height="22" rx="2" fill="#064e3b" stroke="#34d399"/>';
  svg+='<text x="'+(prX+prW/2)+'" y="'+(prY+86)+'" text-anchor="middle" fill="#a7f3d0" font-size="7" font-weight="bold">enqueue()</text>';

  // Flow Arrow into Buffer
  svg+='<line x1="'+(prX+prW)+'" y1="'+(prY+83)+'" x2="'+(cX+140)+'" y2="'+(prY+83)+'" stroke="#10b981" stroke-width="2"/>';
  svg+='<polygon points="'+(cX+140)+','+(prY+83)+' '+(cX+133)+','+(prY+79)+' '+(cX+133)+','+(prY+87)+'" fill="#10b981"/>';

  // Ring Buffer Reservoir in Center
  const rfX=cX+145,rfY=cY+30,rfW=110,rfH=120;
  svg+='<rect x="'+rfX+'" y="'+rfY+'" width="'+rfW+'" height="'+rfH+'" rx="5" fill="#0c1e28" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(rfX+rfW/2)+'" y="'+(rfY+18)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">RING RESERVOIR</text>';
  svg+='<text x="'+(rfX+rfW/2)+'" y="'+(rfY+32)+'" text-anchor="middle" fill="#8ba5b5" font-size="7">Capacity: 12 slots</text>';

  // Fill gauge
  const fillPct=0.58;
  const gaugeW=rfW-30,gaugeH=12;
  svg+='<rect x="'+(rfX+15)+'" y="'+(rfY+44)+'" width="'+gaugeW+'" height="'+gaugeH+'" rx="3" fill="#16242c" stroke="#334d5c"/>';
  svg+='<rect x="'+(rfX+15)+'" y="'+(rfY+44)+'" width="'+(gaugeW*fillPct)+'" height="'+gaugeH+'" rx="3" fill="'+orange+'"/>';
  svg+='<text x="'+(rfX+rfW/2)+'" y="'+(rfY+70)+'" text-anchor="middle" fill="'+orange+'" font-size="8" font-family="monospace" font-weight="bold">7 / 12 (58% Full)</text>';

  svg+='<rect x="'+(rfX+10)+'" y="'+(rfY+82)+'" width="'+(rfW-20)+'" height="26" rx="2" fill="#111c24" stroke="#223a4a"/>';
  svg+='<text x="'+(rfX+rfW/2)+'" y="'+(rfY+94)+'" text-anchor="middle" fill="#6ee7b7" font-size="6.5">State: STABLE FLOW</text>';
  svg+='<text x="'+(rfX+rfW/2)+'" y="'+(rfY+104)+'" text-anchor="middle" fill="#8ba5b5" font-size="6">λ_p <= λ_c (No Drops)</text>';

  // Flow Arrow out of Buffer
  svg+='<line x1="'+(rfX+rfW)+'" y1="'+(prY+83)+'" x2="'+(cX+285)+'" y2="'+(prY+83)+'" stroke="#38bdf8" stroke-width="2"/>';
  svg+='<polygon points="'+(cX+285)+','+(prY+83)+' '+(cX+278)+','+(prY+79)+' '+(cX+278)+','+(prY+87)+'" fill="#38bdf8"/>';

  // Consumer Box on Right
  const csX=cX+290,csY=cY+35,csW=90,csH=110;
  svg+='<rect x="'+csX+'" y="'+csY+'" width="'+csW+'" height="'+csH+'" rx="4" fill="#082f49" stroke="#38bdf8" stroke-width="1.5"/>';
  svg+='<text x="'+(csX+csW/2)+'" y="'+(csY+20)+'" text-anchor="middle" fill="#38bdf8" font-size="9" font-weight="bold">CONSUMER</text>';
  svg+='<text x="'+(csX+csW/2)+'" y="'+(csY+40)+'" text-anchor="middle" fill="#7dd3fc" font-size="7.5">Rate: λ_c pkts/s</text>';
  svg+='<text x="'+(csX+csW/2)+'" y="'+(csY+58)+'" text-anchor="middle" fill="#dcebf2" font-size="7.5" font-family="monospace">Work Drain</text>';
  svg+='<rect x="'+(csX+10)+'" y="'+(csY+72)+'" width="'+(csW-20)+'" height="22" rx="2" fill="#0369a1" stroke="#38bdf8"/>';
  svg+='<text x="'+(csX+csW/2)+'" y="'+(csY+86)+'" text-anchor="middle" fill="#e0f2fe" font-size="7" font-weight="bold">dequeue()</text>';

  svg+='<rect x="'+(cX+15)+'" y="'+(cY+cH-42)+'" width="'+(cW-30)+'" height="32" rx="4" fill="#0e1a22" stroke="#1e3340"/>';
  svg+='<text x="'+(cX+25)+'" y="'+(cY+cH-26)+'" fill="#38bdf8" font-size="8" font-family="monospace">Queuing Invariant: Little\'s Law L = λ · W ⟹ Buffer Occupancy = Arrival Rate × Residence Time</text>';
  svg+='<text x="'+(cX+25)+'" y="'+(cY+cH-14)+'" fill="#8ba5b5" font-size="7.5">Backpressure Policy: Mutex wait on full buffer · Prevents packet loss without unmapped heap growth</text>';

  const bX=470,bY=45,bW=210,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">BUFFER CAPACITY (N)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">12</text>';
  svg+='<text x="'+(bX+55)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="11">ring slots</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+68)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+68)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+88)+'" fill="#7e9bab" font-size="9">FLOW EQUILIBRIUM STATE</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+112)+'" fill="'+ink+'" font-size="15" font-family="monospace" font-weight="bold">λ_p ≤ λ_c Safe</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">Zero buffer overflow drop events</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+138)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+138)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+156)+'" fill="#7e9bab" font-size="9">SYNCHRONIZATION PRIMITIVES</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+180)+'" fill="#fde047" font-size="12" font-family="monospace" font-weight="bold">Condition Variables</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+196)+'" fill="#8ba5b5" font-size="8">not_empty / not_full kernel wait queues</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+208)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+208)+'" stroke="#1e3340"/>';

  svg+=text(bX+bW/2,bY+224,'Elastic Reservoir: Smooths bursty network I/O',orange,8.5);
  svg+=text(360,305,'Mathematical Theorem: Bounded buffer guarantees stability when service rate exceeds arrival rate',soft,10);
  return svg;
 }

 if(cfg.slug==='stack-adt-recursion'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'PARSING PUSHDOWN AUTOMATON & LIFO DELIMITER STACK (n = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  // Visual Token Stream at top
  svg+='<text x="'+(cX+15)+'" y="'+(cY+20)+'" fill="#7e9bab" font-size="8.5" font-weight="bold">INPUT TOKEN STREAM (INFIX SYNTAX & DELIMITERS)</text>';
  const tokens=['{', 'a', '+', '[', 'b', '*', '(', 'c', '-', 'd', ')', ']', '}'];
  const tW=22,tH=20,tY=cY+26;
  for(let i=0;i<tokens.length;i++){
   const tx=cX+15+i*(tW+5);
   const isDelimiter=Boolean(tokens[i].match(/[{}\[\]()]/));
   const isMatch=i===10||i===11||i===12;
   const col=isMatch?'#10b981':isDelimiter?'#38bdf8':'#8ba5b5';
   const bg=isMatch?'#064e3b':isDelimiter?'#0c4a6e':'#111c24';
   svg+='<rect x="'+tx+'" y="'+tY+'" width="'+tW+'" height="'+tH+'" rx="2" fill="'+bg+'" stroke="'+col+'" stroke-width="1"/>';
   svg+='<text x="'+(tx+tW/2)+'" y="'+(tY+14)+'" text-anchor="middle" fill="#dcebf2" font-size="9" font-family="monospace">'+tokens[i]+'</text>';
  }

  // Visual Vertical Stack container
  const sX=cX+30,sY=cY+58,sW=140,sH=125;
  svg+='<rect x="'+sX+'" y="'+sY+'" width="'+sW+'" height="'+sH+'" rx="4" fill="#0b151b" stroke="#334d5c" stroke-width="1.5"/>';
  svg+='<text x="'+(sX+sW/2)+'" y="'+(sY-5)+'" text-anchor="middle" fill="#7e9bab" font-size="8">LIFO OPERAND/DELIMITER STACK</text>';

  const stackElements=[
   {val:'{ (scope base)',col:'#38bdf8'},
   {val:'[ (array idx)',col:'#a855f7'},
   {val:'( (expr sub)',col:'#f97316'},
   {val:'TOP OF STACK',col:'#10b981'}
  ];
  for(let i=0;i<stackElements.length;i++){
   const ey=sY+sH-26-i*26;
   svg+='<rect x="'+(sX+8)+'" y="'+ey+'" width="'+(sW-16)+'" height="22" rx="2" fill="#162a36" stroke="'+stackElements[i].col+'" stroke-width="1.5"/>';
   svg+='<text x="'+(sX+sW/2)+'" y="'+(ey+15)+'" text-anchor="middle" fill="#dcebf2" font-size="8" font-family="monospace">'+stackElements[i].val+'</text>';
  }
  // Stack top pointer arrow
  const topY=sY+sH-26-(stackElements.length-1)*26+11;
  svg+='<polygon points="'+(sX+sW+12)+','+topY+' '+(sX+sW+18)+','+(topY-4)+' '+(sX+sW+18)+','+(topY+4)+'" fill="'+orange+'"/>';
  svg+='<text x="'+(sX+sW+24)+'" y="'+(topY+3)+'" fill="'+orange+'" font-size="8" font-weight="bold">RSP / top</text>';

  // Parsing engine explanation on right of sandbox
  const pX=cX+200,pY=cY+58,pW=180,pH=125;
  svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" rx="4" fill="#0e1a22" stroke="#1e3340"/>';
  svg+='<text x="'+(pX+10)+'" y="'+(pY+18)+'" fill="#38bdf8" font-size="8" font-weight="bold">PUSHDOWN AUTOMATON LOGIC</text>';
  svg+='<text x="'+(pX+10)+'" y="'+(pY+36)+'" fill="#8ba5b5" font-size="7.5">Open delimiter: push(S, token)</text>';
  svg+='<text x="'+(pX+10)+'" y="'+(pY+50)+'" fill="#8ba5b5" font-size="7.5">Close delimiter: token == pop(S) ?</text>';
  svg+='<text x="'+(pX+10)+'" y="'+(pY+64)+'" fill="#10b981" font-size="7.5" font-weight="bold">Match Verified: ( matched with )</text>';
  svg+='<text x="'+(pX+10)+'" y="'+(pY+82)+'" fill="#fde047" font-size="7.5">Language: Dyck Language D_k</text>';
  svg+='<text x="'+(pX+10)+'" y="'+(pY+96)+'" fill="#8ba5b5" font-size="7">Requires unbounded memory stack</text>';
  svg+='<text x="'+(pX+10)+'" y="'+(pY+112)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">Parser State: VALID (O(n) time)</text>';

  svg+='<rect x="'+(cX+15)+'" y="'+(cY+cH-34)+'" width="'+(cW-30)+'" height="26" rx="4" fill="#0e1a22" stroke="#1e3340"/>';
  svg+='<text x="'+(cX+25)+'" y="'+(cY+cH-17)+'" fill="#38bdf8" font-size="8" font-family="monospace">Pumping Lemma Theorem: Finite State Automata (O(1)) cannot count arbitrary nested depth ⟹ LIFO Stack Required</text>';

  const bX=470,bY=45,bW=210,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">NESTING DEPTH WATERMARK (d)</text>';
  const d_water=Math.min(16,Math.round(Math.log2(n))+2);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+d_water+'</text>';
  svg+='<text x="'+(bX+55)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="11">nested frames</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+68)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+68)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+88)+'" fill="#7e9bab" font-size="9">LIFO POP ACCESS LATENCY</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+112)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">Θ(1) Constant</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+124)+'" fill="#8ba5b5" font-size="8">L1 CPU Cache Hit Rate > 99.8%</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+138)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+138)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+156)+'" fill="#7e9bab" font-size="9">FORMAL GRAMMAR HIERARCHY</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+180)+'" fill="#fde047" font-size="12" font-family="monospace" font-weight="bold">Context-Free Grammar</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+196)+'" fill="#8ba5b5" font-size="8">Chomsky Type-2 Language Model</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+208)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+208)+'" stroke="#1e3340"/>';

  svg+=text(bX+bW/2,bY+224,'Dyck Language Invariant: S ⟶ (S) | SS | ε',orange,8.5);
  svg+=text(360,305,'Mathematical Theorem: Context-Free parsing requires a LIFO stack · Shunting-Yard evaluates in O(n) time',soft,10);
  return svg;
 }

 if(cfg.slug==='divide-conquer-sorting'){
  svg+='<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" fill="#081116" stroke="'+soft+'" stroke-width="2" rx="6"/>';
  svg+=text(cX+cW/2,cY-14,'RECURSION TREE & MASTER THEOREM UNROLLING (n = '+p.input+')','#e2f0f8',11);

  const n=p.input;
  const treeY=cY+22;
  
  // Level 0
  const l0W=140,l0H=20;
  const l0X=cX+(cW-l0W)/2;
  svg+='<rect x="'+l0X+'" y="'+treeY+'" width="'+l0W+'" height="'+l0H+'" rx="3" fill="#1e3e52" stroke="'+orange+'" stroke-width="1.5"/>';
  svg+='<text x="'+(l0X+l0W/2)+'" y="'+(treeY+13)+'" text-anchor="middle" fill="#dcebf2" font-size="8" font-family="monospace">Problem T(n) · Work: c·n</text>';
  svg+='<text x="'+(cX+cW-15)+'" y="'+(treeY+13)+'" text-anchor="end" fill="'+orange+'" font-size="8" font-family="monospace">c·n</text>';

  // Level 1
  const l1Y=treeY+45;
  const l1W=80,l1H=18;
  const l1X1=cX+cW/4-l1W/2, l1X2=cX+3*cW/4-l1W/2;
  svg+='<line x1="'+(l0X+l0W/4)+'" y1="'+(treeY+l0H)+'" x2="'+(l1X1+l1W/2)+'" y2="'+l1Y+'" stroke="#334d5c" stroke-width="1.5"/>';
  svg+='<line x1="'+(l0X+3*l0W/4)+'" y1="'+(treeY+l0H)+'" x2="'+(l1X2+l1W/2)+'" y2="'+l1Y+'" stroke="#334d5c" stroke-width="1.5"/>';
  svg+='<rect x="'+l1X1+'" y="'+l1Y+'" width="'+l1W+'" height="'+l1H+'" rx="2" fill="#162a36" stroke="#38bdf8" stroke-width="1"/>';
  svg+='<text x="'+(l1X1+l1W/2)+'" y="'+(l1Y+12)+'" text-anchor="middle" fill="#dcebf2" font-size="7" font-family="monospace">T(n/2) [c·n/2]</text>';
  svg+='<rect x="'+l1X2+'" y="'+l1Y+'" width="'+l1W+'" height="'+l1H+'" rx="2" fill="#162a36" stroke="#38bdf8" stroke-width="1"/>';
  svg+='<text x="'+(l1X2+l1W/2)+'" y="'+(l1Y+12)+'" text-anchor="middle" fill="#dcebf2" font-size="7" font-family="monospace">T(n/2) [c·n/2]</text>';
  svg+='<text x="'+(cX+cW-15)+'" y="'+(l1Y+12)+'" text-anchor="end" fill="'+orange+'" font-size="8" font-family="monospace">2·(cn/2) = c·n</text>';

  // Level 2
  const l2Y=l1Y+42;
  const l2W=46,l2H=16;
  const centers=[cX+cW/8, cX+3*cW/8, cX+5*cW/8, cX+7*cW/8];
  svg+='<line x1="'+(l1X1+l1W/4)+'" y1="'+(l1Y+l1H)+'" x2="'+centers[0]+'" y2="'+l2Y+'" stroke="#334d5c" stroke-width="1"/>';
  svg+='<line x1="'+(l1X1+3*l1W/4)+'" y1="'+(l1Y+l1H)+'" x2="'+centers[1]+'" y2="'+l2Y+'" stroke="#334d5c" stroke-width="1"/>';
  svg+='<line x1="'+(l1X2+l1W/4)+'" y1="'+(l1Y+l1H)+'" x2="'+centers[2]+'" y2="'+l2Y+'" stroke="#334d5c" stroke-width="1"/>';
  svg+='<line x1="'+(l1X2+3*l1W/4)+'" y1="'+(l1Y+l1H)+'" x2="'+centers[3]+'" y2="'+l2Y+'" stroke="#334d5c" stroke-width="1"/>';
  for(let i=0;i<4;i++){
   svg+='<rect x="'+(centers[i]-l2W/2)+'" y="'+l2Y+'" width="'+l2W+'" height="'+l2H+'" rx="2" fill="#111c24" stroke="#5a7687" stroke-width="1"/>';
   svg+='<text x="'+centers[i]+'" y="'+(l2Y+11)+'" text-anchor="middle" fill="#8ba5b5" font-size="6.5" font-family="monospace">T(n/4)</text>';
  }
  svg+='<text x="'+(cX+cW-15)+'" y="'+(l2Y+12)+'" text-anchor="end" fill="'+orange+'" font-size="8" font-family="monospace">4·(cn/4) = c·n</text>';

  // Leaves level
  const leafY=l2Y+38;
  svg+='<line x1="'+(cX+cW/2)+'" y1="'+(l2Y+l2H)+'" x2="'+(cX+cW/2)+'" y2="'+leafY+'" stroke="#334d5c" stroke-width="1" stroke-dasharray="3 3"/>';
  svg+='<text x="'+(cX+cW/2)+'" y="'+(leafY-5)+'" text-anchor="middle" fill="#5a7687" font-size="7">⋮ (tree height = log₂ n levels)</text>';
  svg+='<rect x="'+(cX+20)+'" y="'+leafY+'" width="'+(cW-100)+'" height="18" rx="2" fill="#0c4a6e" stroke="#10b981" stroke-width="1"/>';
  svg+='<text x="'+(cX+20+(cW-100)/2)+'" y="'+(leafY+12)+'" text-anchor="middle" fill="#6ee7b7" font-size="7.5" font-family="monospace">Base Leaves: n subproblems of size 1 ⟹ Θ(n) work</text>';
  svg+='<text x="'+(cX+cW-15)+'" y="'+(leafY+12)+'" text-anchor="end" fill="'+orange+'" font-size="8" font-family="monospace">Θ(n)</text>';

  svg+='<rect x="'+(cX+15)+'" y="'+(cY+cH-34)+'" width="'+(cW-30)+'" height="26" rx="4" fill="#0e1a22" stroke="#1e3340"/>';
  svg+='<text x="'+(cX+25)+'" y="'+(cY+cH-17)+'" fill="#38bdf8" font-size="8" font-family="monospace">Total Work = ∑_{i=0}^{log₂ n - 1} (c·n) + Θ(n) = c·n·log₂ n + Θ(n) = Θ(n log n)</text>';

  const bX=470,bY=45,bW=210,bH=230;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">RECURSION TREE DEPTH (h)</text>';
  const h_levels=Math.round(Math.log2(n));
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+h_levels+'</text>';
  svg+='<text x="'+(bX+65)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="11">log₂('+n+') levels</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+68)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+68)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+88)+'" fill="#7e9bab" font-size="9">WORK ACROSS EACH DEPTH</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+112)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">c · '+n+'</text>';
  svg+='<text x="'+(bX+105)+'" y="'+(bY+108)+'" fill="#8ba5b5" font-size="9">ops/level</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+124)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+124)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+142)+'" fill="#7e9bab" font-size="9">INFORMATION LOWER BOUND</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+166)+'" fill="#fde047" font-size="13" font-family="monospace" font-weight="bold">Ω(n log n)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+184)+'" fill="#8ba5b5" font-size="8">Leaves L ≥ n! ⟹ Height ≥ log₂(n!)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+198)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+198)+'" stroke="#1e3340"/>';

  svg+=text(bX+bW/2,bY+218,'Stirling Bound: log₂(n!) ≈ n log₂ n − 1.44n',orange,8.5);
  svg+=text(360,305,'Mathematical Theorem: All tree levels do uniform c·n work ⟹ Total Work = Θ(n log n)',soft,10);
  return svg;
 }

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

 if(cfg.slug==='network-flow-max-cut'){
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  const n=p.input;
  const e_count=3*n;
  const t_insps=v.raw;

  svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+=text(240,24,'Edmonds-Karp Residual Network Flow & Augmenting Path Geometry');

  svg+='<text x="50" y="56" fill="#7e9bab" font-size="8.5" font-weight="bold">FLOW NETWORK G=(V, E) · |V| = '+n+' · |E| = '+e_count+' EDGES · SOURCE s = 0 · SINK t = '+(n-1)+'</text>';

  const nodes=[
   {id:'s',x:75,y:115,col:'#10b981',st:'Source',d:'elev:0'},
   {id:'V1',x:165,y:80,col:'#10b981',st:'Cut-S',d:'elev:1'},
   {id:'V2',x:165,y:155,col:'#10b981',st:'Cut-S',d:'elev:1'},
   {id:'V3',x:275,y:80,col:'#38bdf8',st:'Cut-T',d:'elev:2'},
   {id:'V4',x:275,y:155,col:'#38bdf8',st:'Cut-T',d:'elev:2'},
   {id:'t',x:380,y:115,col:'#38bdf8',st:'Sink',d:'elev:3'}
  ];

  const edges=[
   {u:0,v:1,flow:'f:12/12',col:'#ef4444',wdt:2.5,dash:null},
   {u:0,v:2,flow:'f:8/8',col:'#ef4444',wdt:2.5,dash:null},
   {u:1,v:3,flow:'f:12/12 (SAT!)',col:'#ef4444',wdt:2.5,dash:null},
   {u:2,v:4,flow:'f:8/8 (SAT!)',col:'#ef4444',wdt:2.5,dash:null},
   {u:3,v:5,flow:'f:12/12',col:'#ef4444',wdt:2.5,dash:null},
   {u:4,v:5,flow:'f:8/8',col:'#ef4444',wdt:2.5,dash:null},
   {u:1,v:4,flow:'c_f:0',col:'#334155',wdt:1.2,dash:'2,2'},
   {u:2,v:3,flow:'c_f:0',col:'#334155',wdt:1.2,dash:'2,2'}
  ];

  edges.forEach(e=>{
   const u=nodes[e.u],v=nodes[e.v];
   const dashAttr=e.dash?' stroke-dasharray="'+e.dash+'"':'';
   svg+='<line x1="'+u.x+'" y1="'+u.y+'" x2="'+v.x+'" y2="'+v.y+'" stroke="'+e.col+'" stroke-width="'+e.wdt+'"'+dashAttr+'/>';
   const midX=(u.x+v.x)/2, midY=(u.y+v.y)/2 - 5;
   svg+='<text x="'+midX+'" y="'+midY+'" text-anchor="middle" fill="'+e.col+'" font-size="6.5" font-family="monospace">'+e.flow+'</text>';
  });

  nodes.forEach(nd=>{
   svg+='<circle cx="'+nd.x+'" cy="'+nd.y+'" r="13" fill="#081016" stroke="'+nd.col+'" stroke-width="2"/>';
   svg+='<text x="'+nd.x+'" y="'+(nd.y+4)+'" text-anchor="middle" fill="#dcebf2" font-size="8" font-family="monospace" font-weight="bold">'+nd.id+'</text>';
   svg+='<text x="'+nd.x+'" y="'+(nd.y+21)+'" text-anchor="middle" fill="#64748b" font-size="6" font-family="monospace">'+nd.d+'</text>';
  });

  const fsX=50,fsY=178,fsW=380,fsH=38;
  svg+='<rect x="'+fsX+'" y="'+fsY+'" width="'+fsW+'" height="'+fsH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(fsX+10)+'" y="'+(fsY+14)+'" fill="#10b981" font-size="7.5" font-family="monospace">Shortest Augmenting Path: BFS found P = s ⟶ V1 ⟶ V3 ⟶ t (Shortest Hop)</text>';
  svg+='<text x="'+(fsX+10)+'" y="'+(fsY+26)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">Backward Residual Edges: c_f(V3, V1) = 12 allows exact flow cancellation</text>';

  const cbX=50,cbY=222,cbW=380,cbH=44;
  svg+='<rect x="'+cbX+'" y="'+cbY+'" width="'+cbW+'" height="'+cbH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(cbX+10)+'" y="'+(cbY+14)+'" fill="#38bdf8" font-size="7.5" font-family="monospace">Total Residual Inspections: T(|V|) = 10 · |V| = '+t_insps+' inspections</text>';
  svg+='<text x="'+(cbX+10)+'" y="'+(cbY+26)+'" fill="#10b981" font-size="7" font-family="monospace">Linear Model: k_flow = 10.0000 inspections/vertex · Intercept T_0 = 0.0000</text>';
  svg+='<text x="'+(cbX+10)+'" y="'+(cbY+38)+'" fill="#8ba5b5" font-size="6.5">Max-Flow Min-Cut Equality: Max Flow |f*| = 20 units · Min Cut c(S, T) = 20 units</text>';

  const bX=465,bY=38,bW=220,bH=235;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">TOTAL RESIDUAL INSPECTIONS</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">'+t_insps+'</text>';
  svg+='<text x="'+(bX+115)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="11">inspections</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">NETWORK SCALE PARAMETERS</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+126)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">|V| = '+n+' · |E| = '+e_count+'</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+142)+'" fill="#8ba5b5" font-size="8">3-regular directed flow topology</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+156)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+156)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+174)+'" fill="#7e9bab" font-size="9">LINEAR AUGMENTATION ASYMPTOTE</text>';
  svg+=text(bX+bW/2,bY+196,'T(|V|) = 10.0000 · |V|','#10b981',10);
  svg+=text(bX+bW/2,bY+214,'Linear Coordinate: |V| (vertices)',orange,8.5);

  svg+=text(360,305,'Mathematical Model: T(|V|) = 10.0000 · |V| + 0.0000 inspections · R² = 1.000000 · Diff = 0.0000%',soft,10);
  return svg;
 }

 if(cfg.slug==='string-matching-automata'){
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  const n=p.input;
  const m_pat=20;
  const c_comps=v.raw;

  svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+=text(240,24,'Knuth-Morris-Pratt Prefix Automaton & Text Stream Scanner');

  svg+='<text x="50" y="56" fill="#7e9bab" font-size="8.5" font-weight="bold">TEXT STREAM T[0 .. '+(n-1)+'] · PATTERN P[0 .. 19] (m = 20) · SCAN POINTER i ∈ [0 .. '+(n-1)+']</text>';

  const stX=50, stY=68, stW=380, stH=40;
  svg+='<rect x="'+stX+'" y="'+stY+'" width="'+stW+'" height="'+stH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(stX+10)+'" y="'+(stY+14)+'" fill="#7dd3fc" font-size="7.5" font-family="monospace">Incoming Stream: [ A C G T A C G T A A T C G G T A A C G T ... ]</text>';
  svg+='<text x="'+(stX+10)+'" y="'+(stY+28)+'" fill="#10b981" font-size="7.5" font-family="monospace">Text Pointer i = '+(Math.min(n-1, 1420))+': Monotonically advancing (NO BACKTRACKING)</text>';

  const patX=50, patY=116, patW=380, patH=48;
  svg+='<rect x="'+patX+'" y="'+patY+'" width="'+patW+'" height="'+patH+'" rx="4" fill="#050b0e" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(patX+10)+'" y="'+(patY+15)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">Pattern P[0..19]: [ A C G T A C G T A A T C G G T A A C G T ]</text>';
  svg+='<text x="'+(patX+10)+'" y="'+(patY+29)+'" fill="#38bdf8" font-size="7" font-family="monospace">π-Failure Array:  [ 0 0 0 0 1 2 3 4 1 1 0 1 0 0 0 1 1 2 3 4 ]</text>';
  svg+='<text x="'+(patX+10)+'" y="'+(patY+42)+'" fill="#10b981" font-size="7" font-family="monospace">Preprocessing Cost: C_0 = m = 20 comparisons · Space: 80 bytes (L1 Cache Resident)</text>';

  const regX=50, regY=172, regW=380, regH=44;
  svg+='<rect x="'+regX+'" y="'+regY+'" width="'+regW+'" height="'+regH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+14)+'" fill="#dcebf2" font-size="7.5" font-family="monospace">State: j = Pattern State Pointer [0 .. 19] | Text Character T[i] vs P[j]</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+28)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">Fallback Rule: On mismatch, j ⟵ π[j - 1] (Preserves matched prefix history)</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+40)+'" fill="#8ba5b5" font-size="6.5">Amortized Analysis: Potential Φ = j; comparisons ≤ 2n across entire stream</text>';

  const sumX=50, sumY=224, sumW=380, sumH=42;
  svg+='<rect x="'+sumX+'" y="'+sumY+'" width="'+sumW+'" height="'+sumH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(sumX+10)+'" y="'+(sumY+14)+'" fill="#38bdf8" font-size="7.5" font-family="monospace">Total Comparisons: C(n) = n + m = '+n+' + 20 = '+c_comps+' comparisons</text>';
  svg+='<text x="'+(sumX+10)+'" y="'+(sumY+26)+'" fill="#10b981" font-size="7" font-family="monospace">Linear Model: k_kmp = 1.0000 comparisons/char · Intercept C_0 = 20.0000</text>';
  svg+='<text x="'+(sumX+10)+'" y="'+(sumY+38)+'" fill="#8ba5b5" font-size="6.5">Stream Scanning Invariant: Linear time O(n + m) with strictly O(1) auxiliary working space</text>';

  const bX=465,bY=38,bW=220,bH=235;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">TOTAL KMP COMPARISONS C(n)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">'+c_comps+'</text>';
  svg+='<text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="11">comps</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">PATTERN REGISTER & π-TABLE</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+126)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">m = 20 chars</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+142)+'" fill="#8ba5b5" font-size="8">C_0 = 20 preprocessing ops</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+156)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+156)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+174)+'" fill="#7e9bab" font-size="9">LINEAR SCAN ASYMPTOTE</text>';
  svg+=text(bX+bW/2,bY+196,'C(n) = 1.0000 · n + 20.0000','#10b981',10);
  svg+=text(bX+bW/2,bY+214,'Linear Coordinate: n (chars)',orange,8.5);

  svg+=text(360,305,'Mathematical Model: C(n) = 1.0000 · n + 20.0000 comparisons · R² = 1.000000 · Diff = 0.0000%',soft,10);
  return svg;
 }

 if(cfg.slug==='greedy-minimum-spanning-trees'){
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  const n=p.input;
  const e_count=4*n;
  const q_lookups=v.raw;
  const mst_edges=n - 1;

  svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+=text(240,24,'Minimum Spanning Tree Construction & Disjoint Set Forest Geometry');

  svg+='<text x="50" y="56" fill="#7e9bab" font-size="8.5" font-weight="bold">NETWORK G=(V, E) · |V| = '+n+' · |E| = '+e_count+' EDGES · MST BRANCHES = '+mst_edges+' EDGES</text>';

  const nodes=[
   {id:'V0',x:75,y:115,col:'#10b981',st:'Root',d:'p:V0'},
   {id:'V1',x:165,y:80,col:'#10b981',st:'Tree',d:'p:V0'},
   {id:'V2',x:165,y:155,col:'#10b981',st:'Tree',d:'p:V0'},
   {id:'V3',x:275,y:80,col:'#10b981',st:'Tree',d:'p:V0'},
   {id:'V4',x:275,y:155,col:'#10b981',st:'Tree',d:'p:V0'},
   {id:'V5',x:380,y:115,col:'#10b981',st:'Tree',d:'p:V0'}
  ];

  const edges=[
   {u:0,v:1,w:'w:2',col:'#10b981',wCol:'#10b981',wdt:2.5,dash:null},
   {u:0,v:2,w:'w:4',col:'#10b981',wCol:'#10b981',wdt:2.5,dash:null},
   {u:1,v:3,w:'w:3',col:'#10b981',wCol:'#10b981',wdt:2.5,dash:null},
   {u:2,v:4,w:'w:5',col:'#10b981',wCol:'#10b981',wdt:2.5,dash:null},
   {u:4,v:5,w:'w:1',col:'#10b981',wCol:'#10b981',wdt:2.5,dash:null},
   {u:1,v:2,w:'w:8 (CYCLE!)',col:'#ef4444',wCol:'#ef4444',wdt:1.5,dash:'3,2'},
   {u:3,v:5,w:'w:7',col:'#334155',wCol:'#64748b',wdt:1.2,dash:'2,2'},
   {u:3,v:4,w:'w:6',col:'#334155',wCol:'#64748b',wdt:1.2,dash:'2,2'}
  ];

  edges.forEach(e=>{
   const u=nodes[e.u],v=nodes[e.v];
   const dashAttr=e.dash?' stroke-dasharray="'+e.dash+'"':'';
   svg+='<line x1="'+u.x+'" y1="'+u.y+'" x2="'+v.x+'" y2="'+v.y+'" stroke="'+e.col+'" stroke-width="'+e.wdt+'"'+dashAttr+'/>';
   const midX=(u.x+v.x)/2, midY=(u.y+v.y)/2 - 5;
   svg+='<text x="'+midX+'" y="'+midY+'" text-anchor="middle" fill="'+e.wCol+'" font-size="6.5" font-family="monospace">'+e.w+'</text>';
  });

  nodes.forEach(nd=>{
   svg+='<circle cx="'+nd.x+'" cy="'+nd.y+'" r="13" fill="#081016" stroke="'+nd.col+'" stroke-width="2"/>';
   svg+='<text x="'+nd.x+'" y="'+(nd.y+4)+'" text-anchor="middle" fill="#dcebf2" font-size="8" font-family="monospace" font-weight="bold">'+nd.id+'</text>';
   svg+='<text x="'+nd.x+'" y="'+(nd.y+21)+'" text-anchor="middle" fill="#64748b" font-size="6" font-family="monospace">'+nd.d+'</text>';
  });

  const fsX=50,fsY=180,fsW=380,fsH=34;
  svg+='<rect x="'+fsX+'" y="'+fsY+'" width="'+fsW+'" height="'+fsH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(fsX+10)+'" y="'+(fsY+14)+'" fill="#10b981" font-size="7.5" font-family="monospace">DSU Parent Map: parent[V1..V5] ⟶ V0 (Path Compressed to Root V0)</text>';
  svg+='<text x="'+(fsX+10)+'" y="'+(fsY+26)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">Cycle Filter: Edge (V1, V2, w=8) ⟶ Find(V1)==Find(V2)==V0 ⟶ Discarded!</text>';

  const cbX=50,cbY=220,cbW=380,cbH=46;
  svg+='<rect x="'+cbX+'" y="'+cbY+'" width="'+cbW+'" height="'+cbH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(cbX+10)+'" y="'+(cbY+14)+'" fill="#38bdf8" font-size="7.5" font-family="monospace">Total DSU Queries: Q(|V|) = 2|E| = 2(4 × '+n+') = '+q_lookups+' lookups</text>';
  svg+='<text x="'+(cbX+10)+'" y="'+(cbY+26)+'" fill="#dcebf2" font-size="7" font-family="monospace">Linear Model: k_mst = 8.0000 lookups/vertex · Intercept Q_0 = 0.0000</text>';
  svg+='<text x="'+(cbX+10)+'" y="'+(cbY+38)+'" fill="#8ba5b5" font-size="6.5">Spanning Tree Invariant: |E_mst| = |V| − 1 = '+mst_edges+' edges · Total MST Weight W_mst = 15</text>';

  const bX=465,bY=38,bW=220,bH=235;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">TOTAL DSU QUERIES Q(|V|)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">'+q_lookups+'</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="11">lookups</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">SPANNING TREE TOPOLOGY</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+126)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">|E_mst| = '+mst_edges+' edges</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+142)+'" fill="#8ba5b5" font-size="8">From |E| = '+e_count+' candidate edges</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+156)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+156)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+174)+'" fill="#7e9bab" font-size="9">LINEAR QUERY ASYMPTOTE</text>';
  svg+=text(bX+bW/2,bY+196,'Q(|V|) = 2|E| = 8.0000 · |V|','#10b981',10);
  svg+=text(bX+bW/2,bY+214,'Linear Coordinate: |V| (vertices)',orange,8.5);

  svg+=text(360,305,'Mathematical Model: Q(|V|) = 8.0000 · |V| + 0.0000 lookups · R² = 1.000000 · Diff = 0.0000%',soft,10);
  return svg;
 }

 if(cfg.slug==='dynamic-programming-memoization'){
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  const n=p.input;
  const w_cap=100;
  const t_states=v.raw;

  svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+=text(240,24,'2D 0/1 Knapsack Tabulation Matrix & Bellman Dependency Geometry');

  svg+='<text x="50" y="56" fill="#7e9bab" font-size="8.5" font-weight="bold">TABULATION GRID [n = '+n+', W = 100] · '+t_states+' TOTAL CELLS · ROW-MAJOR STREAMING</text>';

  const cols=[
   {w:0,x:60},
   {w:15,x:115},
   {w:25,x:175},
   {w:40,x:245},
   {w:60,x:315},
   {w:100,x:385}
  ];

  cols.forEach(c=>{
   svg+='<text x="'+c.x+'" y="78" text-anchor="middle" fill="#64748b" font-size="7" font-family="monospace">w='+c.w+'</text>';
  });

  const r3Y=88, rowH=24, cellW=44;
  svg+='<text x="48" y="'+(r3Y+16)+'" fill="#94a3b8" font-size="7.5" font-family="monospace">i=3</text>';
  const r3Vals=[
   {x:60,val:'0',col:'#475569',bg:'#0b151b'},
   {x:115,val:'25',col:'#475569',bg:'#0b151b'},
   {x:175,val:'45',col:'#10b981',bg:'#064e3b',isInc:true},
   {x:245,val:'62',col:'#64748b',bg:'#0f172a',isExc:true},
   {x:315,val:'78',col:'#475569',bg:'#0b151b'},
   {x:385,val:'95',col:'#475569',bg:'#0b151b'}
  ];
  r3Vals.forEach(c=>{
   const strokeCol=c.isInc?'#10b981':c.isExc?'#64748b':'#1e293b';
   svg+='<rect x="'+(c.x-cellW/2)+'" y="'+r3Y+'" width="'+cellW+'" height="'+rowH+'" rx="3" fill="'+c.bg+'" stroke="'+strokeCol+'" stroke-width="1.2"/>';
   svg+='<text x="'+c.x+'" y="'+(r3Y+16)+'" text-anchor="middle" fill="'+c.col+'" font-size="8" font-family="monospace" font-weight="bold">'+c.val+'</text>';
  });

  const r4Y=120;
  svg+='<text x="48" y="'+(r4Y+16)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">i=4*</text>';
  const r4Vals=[
   {x:60,val:'0',col:'#475569',bg:'#0b151b'},
   {x:115,val:'35',col:'#475569',bg:'#0b151b'},
   {x:175,val:'45',col:'#475569',bg:'#0b151b'},
   {x:245,val:'80',col:orange,bg:'#431407',isTarget:true},
   {x:315,val:'97',col:'#475569',bg:'#0b151b'},
   {x:385,val:'115',col:'#475569',bg:'#0b151b'}
  ];
  r4Vals.forEach(c=>{
   const strokeCol=c.isTarget?orange:'#1e293b';
   svg+='<rect x="'+(c.x-cellW/2)+'" y="'+r4Y+'" width="'+cellW+'" height="'+rowH+'" rx="3" fill="'+c.bg+'" stroke="'+strokeCol+'" stroke-width="'+(c.isTarget?1.8:1.2)+'"/>';
   svg+='<text x="'+c.x+'" y="'+(r4Y+16)+'" text-anchor="middle" fill="'+c.col+'" font-size="8" font-family="monospace" font-weight="bold">'+c.val+'</text>';
  });

  svg+='<line x1="235" y1="'+(r3Y+rowH)+'" x2="235" y2="'+r4Y+'" stroke="#64748b" stroke-width="1.5" stroke-dasharray="2,2"/>';
  svg+='<polygon points="235,'+r4Y+' 232,'+(r4Y-4)+' 238,'+(r4Y-4)+'" fill="#64748b"/>';

  svg+='<path d="M 175 '+(r3Y+rowH)+' Q 195 '+(r4Y-2)+' 245 '+r4Y+'" fill="none" stroke="'+orange+'" stroke-width="2"/>';
  svg+='<polygon points="245,'+r4Y+' 240,'+(r4Y-6)+' 248,'+(r4Y-3)+'" fill="'+orange+'"/>';
  svg+='<text x="210" y="117" text-anchor="middle" fill="'+orange+'" font-size="6.5" font-weight="bold">+35</text>';

  const fsX=50,fsY=152,fsW=380,fsH=40;
  svg+='<rect x="'+fsX+'" y="'+fsY+'" width="'+fsW+'" height="'+fsH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(fsX+10)+'" y="'+(fsY+14)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">Item 4 (w₄=15, v₄=35): DP[4][40] = max(DP[3][40], DP[3][40-15] + 35)</text>';
  svg+='<text x="'+(fsX+10)+'" y="'+(fsY+26)+'" fill="#10b981" font-size="7.5" font-family="monospace">Evaluation: max(62, 45 + 35) = max(62, 80) = 80 [Optimal: Include Item 4]</text>';
  svg+='<text x="'+(fsX+10)+'" y="'+(fsY+36)+'" fill="#38bdf8" font-size="6.5" font-family="monospace">1D Space Compression: Traverse w from 100 down to 15 to prevent item reuse</text>';

  const cbX=50,cbY=198,cbW=380,cbH=68;
  svg+='<rect x="'+cbX+'" y="'+cbY+'" width="'+cbW+'" height="'+cbH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(cbX+10)+'" y="'+(cbY+16)+'" fill="#38bdf8" font-size="7.5" font-family="monospace">Complexity Invariant: T(n) = W · n = 100 × '+n+' = '+t_states+' evaluations</text>';
  svg+='<text x="'+(cbX+10)+'" y="'+(cbY+30)+'" fill="#dcebf2" font-size="7" font-family="monospace">Linear Model: k_dp = 100.0000 states/item · Intercept T_0 = 0.0000</text>';
  const mem2dBytes=(n+1)*101*8;
  const mem1dBytes=101*8;
  svg+='<text x="'+(cbX+10)+'" y="'+(cbY+44)+'" fill="#8ba5b5" font-size="6.5">Spatial Footprint: 2D Matrix = '+mem2dBytes+' B ('+(mem2dBytes/1024).toFixed(1)+' KiB) · 1D Rolling Buffer = '+mem1dBytes+' B (L1 resident)</text>';
  svg+='<text x="'+(cbX+10)+'" y="'+(cbY+56)+'" fill="#8ba5b5" font-size="6.5">Cache Streaming: 64-byte L1 cache line brings 8 contiguous cells; 100% prefetch hit rate</text>';

  const bX=465,bY=38,bW=220,bH=235;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">TOTAL STATE EVALUATIONS T(n)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">'+t_states+'</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="11">operations</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">PROBLEM SCALE</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+126)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">n='+n+' items, W=100</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+142)+'" fill="#8ba5b5" font-size="8">Table Dimensions: '+(n+1)+' × 101 cells</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+156)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+156)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+174)+'" fill="#7e9bab" font-size="9">PSEUDO-POLYNOMIAL BOUND</text>';
  svg+=text(bX+bW/2,bY+196,'T(n) = W · n = 100.0000 · n','#10b981',10);
  svg+=text(bX+bW/2,bY+214,'Linear Coordinate: n (items)',orange,8.5);

  svg+=text(360,305,'Mathematical Model: T(n) = 100.0000 · n + 0.0000 operations · R² = 1.000000 · Diff = 0.0000%',soft,10);
  return svg;
 }

 if(cfg.slug==='graph-traversal-shortest-paths'){
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  const n=p.input;
  const e_count=4*n;
  const t_ops=v.raw;

  svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+=text(240,24,'Directed Graph Traversal & Adjacency List Traversal Frontier');

  svg+='<text x="50" y="56" fill="#7e9bab" font-size="8.5" font-weight="bold">DIRECTED GRAPH G = (V, E) · |V| = '+n+' VERTICES · |E| = '+e_count+' EDGES (d_avg = 4.0)</text>';

  const nodes=[
   {id:'V0',x:75,y:120,col:'#10b981',st:'Settled',d:'d=0'},
   {id:'V1',x:165,y:85,col:orange,st:'Frontier',d:'d=2'},
   {id:'V2',x:165,y:155,col:orange,st:'Frontier',d:'d=5'},
   {id:'V3',x:275,y:85,col:'#38bdf8',st:'Discovered',d:'d=5'},
   {id:'V4',x:275,y:155,col:'#38bdf8',st:'Discovered',d:'d=6'},
   {id:'V5',x:380,y:120,col:'#64748b',st:'Unvisited',d:'d=8'}
  ];

  const edges=[
   {u:0,v:1,w:'w:2',col:'#10b981',wCol:'#10b981'},
   {u:0,v:2,w:'w:5',col:'#10b981',wCol:'#10b981'},
   {u:1,v:3,w:'w:3',col:orange,wCol:orange},
   {u:1,v:4,w:'w:4',col:orange,wCol:orange},
   {u:2,v:4,w:'w:1',col:orange,wCol:orange},
   {u:3,v:5,w:'w:3',col:'#38bdf8',wCol:'#38bdf8'},
   {u:4,v:5,w:'w:2',col:'#38bdf8',wCol:'#38bdf8'},
   {u:2,v:3,w:'w:2',col:'#334155',wCol:'#64748b',dash:'3,2'}
  ];

  edges.forEach(e=>{
   const u=nodes[e.u],v=nodes[e.v];
   const dashAttr=e.dash?' stroke-dasharray="'+e.dash+'"':'';
   svg+='<line x1="'+u.x+'" y1="'+u.y+'" x2="'+v.x+'" y2="'+v.y+'" stroke="'+e.col+'" stroke-width="1.5"'+dashAttr+'/>';
   const midX=(u.x+v.x)/2, midY=(u.y+v.y)/2 - 4;
   svg+='<text x="'+midX+'" y="'+midY+'" text-anchor="middle" fill="'+e.wCol+'" font-size="6.5" font-family="monospace">'+e.w+'</text>';
  });

  nodes.forEach(nd=>{
   svg+='<circle cx="'+nd.x+'" cy="'+nd.y+'" r="14" fill="#081016" stroke="'+nd.col+'" stroke-width="2"/>';
   svg+='<text x="'+nd.x+'" y="'+(nd.y+4)+'" text-anchor="middle" fill="#dcebf2" font-size="8.5" font-family="monospace" font-weight="bold">'+nd.id+'</text>';
   svg+='<text x="'+nd.x+'" y="'+(nd.y+22)+'" text-anchor="middle" fill="'+nd.col+'" font-size="6.5" font-family="monospace">'+nd.d+'</text>';
  });

  const fsX=50,fsY=182,fsW=380,fsH=34;
  svg+='<rect x="'+fsX+'" y="'+fsY+'" width="'+fsW+'" height="'+fsH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(fsX+10)+'" y="'+(fsY+14)+'" fill="'+orange+'" font-size="7.5" font-family="monospace">FIFO Queue / Min-Heap Frontier: [ V1 (dist=2), V2 (dist=5) ]</text>';
  svg+='<text x="'+(fsX+10)+'" y="'+(fsY+26)+'" fill="#10b981" font-size="7.5" font-family="monospace">Settled Set S = { V0 } · Adjacent Neighbors Scanned: Adj[V0] ⟶ (V1, 2) ⟶ (V2, 5)</text>';

  const cbX=50,cbY=222,cbW=380,cbH=44;
  svg+='<rect x="'+cbX+'" y="'+cbY+'" width="'+cbW+'" height="'+cbH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(cbX+10)+'" y="'+(cbY+14)+'" fill="#38bdf8" font-size="7.5" font-family="monospace">Handshaking Sum: ∑ out_deg(v) = |E| = '+e_count+' edges</text>';
  svg+='<text x="'+(cbX+10)+'" y="'+(cbY+26)+'" fill="#dcebf2" font-size="7" font-family="monospace">Traversal Complexity: T(|V|) = |V| + |E| = '+n+' + '+e_count+' = '+t_ops+' ops</text>';
  svg+='<text x="'+(cbX+10)+'" y="'+(cbY+38)+'" fill="#8ba5b5" font-size="6.5">Memory Layout: 8|V| head pointers + 16|E| edge nodes = '+(8*n + 16*e_count)+' bytes</text>';

  const bX=465,bY=38,bW=220,bH=235;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">TOTAL TRAVERSAL OPS T(|V|)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">'+t_ops+'</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="11">operations</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">GRAPH TOPOLOGY</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+126)+'" fill="'+ink+'" font-size="16" font-family="monospace" font-weight="bold">|V|='+n+', |E|='+e_count+'</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+142)+'" fill="#8ba5b5" font-size="8">Average Out-Degree d = 4.0 edges/node</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+156)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+156)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+174)+'" fill="#7e9bab" font-size="9">LINEAR TRAVERSAL BOUND</text>';
  svg+=text(bX+bW/2,bY+196,'T(|V|) = |V| + |E| = 5.0000 · |V|','#10b981',10);
  svg+=text(bX+bW/2,bY+214,'Linear Coordinate: |V| (nodes)',orange,8.5);

  svg+=text(360,305,'Mathematical Model: T(|V|) = 5.0000 · |V| + 0.0000 operations · R² = 1.000000 · Diff = 0.0000%',soft,10);
  return svg;
 }

 if(cfg.slug==='hash-tables-collision-resolution'){
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  const n=p.input;
  const alpha=n/1000.0;
  const p_exp=v.raw;
  const x_coord=(1.0/(1.0 - alpha));

  svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+=text(240,24,'Open Addressing Hash Table Architecture & Double Hashing Path');

  svg+='<text x="50" y="56" fill="#7e9bab" font-size="8.5" font-weight="bold">TABLE SLOTS [m = 1000] · n = '+n+' KEYS · LOAD FACTOR α = '+alpha.toFixed(2)+'</text>';

  // Representative array slots (14 slots)
  const slotW=25,slotH=42,startX=48,arrY=75;
  const slots=[
   {idx:0,val:'NULL',occ:false,isPath:false},
   {idx:1,val:'412',occ:true,isPath:false},
   {idx:2,val:'791',occ:true,isPath:true},
   {idx:3,val:'NULL',occ:false,isPath:false},
   {idx:4,val:'155',occ:true,isPath:false},
   {idx:5,val:'683',occ:true,isPath:false},
   {idx:6,val:'NULL',occ:false,isPath:false},
   {idx:7,val:'920',occ:true,isPath:true},
   {idx:8,val:'NULL',occ:false,isPath:false},
   {idx:9,val:'347',occ:true,isPath:false},
   {idx:10,val:'NULL',occ:false,isPath:false},
   {idx:11,val:'582',occ:true,isPath:false},
   {idx:12,val:'+773',occ:true,isPath:true,isNew:true},
   {idx:13,val:'NULL',occ:false,isPath:false}
  ];

  slots.forEach((s,i)=>{
   const sX=startX+i*(slotW+2);
   const fillCol=s.isNew?'#431407':s.isPath?'#1e293b':s.occ?'#0f172a':'#081016';
   const strokeCol=s.isNew?orange:s.isPath?'#ef4444':s.occ?'#38bdf8':'#1e3340';
   svg+='<rect x="'+sX+'" y="'+arrY+'" width="'+slotW+'" height="'+slotH+'" rx="3" fill="'+fillCol+'" stroke="'+strokeCol+'" stroke-width="'+(s.isPath||s.isNew?1.5:1)+'"/>';
   svg+='<text x="'+(sX+slotW/2)+'" y="'+(arrY+12)+'" text-anchor="middle" fill="#64748b" font-size="5.5" font-family="monospace">['+s.idx+']</text>';
   svg+='<text x="'+(sX+slotW/2)+'" y="'+(arrY+28)+'" text-anchor="middle" fill="'+(s.isNew?orange:s.isPath?'#fca5a5':s.occ?'#38bdf8':'#334155')+'" font-size="6.5" font-weight="bold">'+s.val+'</text>';
  });

  // Probe path hopping curve: 2 -> 7 -> 12
  const p2X=startX+2*(slotW+2)+slotW/2;
  const p7X=startX+7*(slotW+2)+slotW/2;
  const p12X=startX+12*(slotW+2)+slotW/2;
  const hopY=arrY-10;

  // Hop 1: 2 to 7
  svg+='<path d="M '+p2X+' '+arrY+' Q '+((p2X+p7X)/2)+' '+(arrY-22)+' '+p7X+' '+arrY+'" fill="none" stroke="'+orange+'" stroke-width="2" stroke-dasharray="3,2"/>';
  svg+='<polygon points="'+p7X+','+arrY+' '+(p7X-3)+','+(arrY-6)+' '+(p7X+3)+','+(arrY-6)+'" fill="'+orange+'"/>';

  // Hop 2: 7 to 12
  svg+='<path d="M '+p7X+' '+arrY+' Q '+((p7X+p12X)/2)+' '+(arrY-22)+' '+p12X+' '+arrY+'" fill="none" stroke="#10b981" stroke-width="2" stroke-dasharray="3,2"/>';
  svg+='<polygon points="'+p12X+','+arrY+' '+(p12X-3)+','+(arrY-6)+' '+(p12X+3)+','+(arrY-6)+'" fill="#10b981"/>';

  // Path narration box
  const nbX=50,nbY=135,nbW=380,nbH=45;
  svg+='<rect x="'+nbX+'" y="'+nbY+'" width="'+nbW+'" height="'+nbH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(nbX+10)+'" y="'+(nbY+16)+'" fill="'+orange+'" font-size="8" font-family="monospace">Search Query K = 773: Base h₁(K) = 2 (Occupied, 791) [Probe 1]</text>';
  svg+='<text x="'+(nbX+10)+'" y="'+(nbY+28)+'" fill="'+orange+'" font-size="8" font-family="monospace">Stride h₂(K) = 5 ⟶ Slot 7 (Occupied, 920) [Probe 2]</text>';
  svg+='<text x="'+(nbX+10)+'" y="'+(nbY+40)+'" fill="#10b981" font-size="8" font-family="monospace">Stride + 5 ⟶ Slot 12 (Found NULL/Target!) [Terminated in 3 probes]</text>';

  // Telemetry box below array
  const regX=50,regY=192,regW=380,regH=65;
  svg+='<rect x="'+regX+'" y="'+regY+'" width="'+regW+'" height="'+regH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+16)+'" fill="#38bdf8" font-size="7.5" font-family="monospace">Knuth Model: E[P_unsuccessful] = 1 / (1 − α) = '+p_exp.toFixed(4)+' probes</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+30)+'" fill="#dcebf2" font-size="7" font-family="monospace">Transformed Coordinate: x = 1 / (1 − '+alpha.toFixed(2)+') = '+x_coord.toFixed(4)+' · Baseline b = 0.0000</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+44)+'" fill="#8ba5b5" font-size="6.5">Coprimality Invariant: gcd(h₂(k), 1000) = 1 guarantees probe sequence traverses full table permutation</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+56)+'" fill="#8ba5b5" font-size="6.5">Memory Layout: Contiguous 8000 bytes (1000 slots × 8 bytes), zero pointer overhead</text>';

  const bX=465,bY=38,bW=220,bH=235;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">EXPECTED PROBES E[P]</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">'+p_exp.toFixed(2)+'</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="11">probes</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">TABLE LOAD FACTOR (α)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+126)+'" fill="'+ink+'" font-size="18" font-family="monospace" font-weight="bold">α = '+alpha.toFixed(2)+'</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+142)+'" fill="#8ba5b5" font-size="8">'+n+' / 1000 occupied slots</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+156)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+156)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+174)+'" fill="#7e9bab" font-size="9">UNIFORM HASHING ASYMPTOTE</text>';
  svg+=text(bX+bW/2,bY+196,'E[P] = 1 / (1 − α)','#10b981',10);
  svg+=text(bX+bW/2,bY+214,'Linearized Coordinate: 1/(1−α)',orange,8.5);

  svg+=text(360,305,'Mathematical Model: E[P] = 1.0000 · [1 / (1 − α)] + 0.0000 probes · R² = 1.000000',soft,10);
  return svg;
 }

 if(cfg.slug==='binary-heaps-priority-queues'){
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  const n=p.input;
  const c_total=v.raw;
  const h=Math.floor(Math.log2(n));

  svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+=text(240,24,'In-Place Binary Max-Heap Architecture & Implicit Array Layout');

  svg+='<text x="50" y="56" fill="#7e9bab" font-size="8.5" font-weight="bold">COMPLETE BINARY MAX-HEAP (n = '+n+' KEYS · HEIGHT = '+h+' LEVELS)</text>';

  // Tree nodes: Level 0 (Root), Level 1 (2 nodes), Level 2 (4 nodes)
  const treeNodes=[
   {idx:0,key:98,x:240,y:80,isRoot:true},
   {idx:1,key:85,x:150,y:118,isRoot:false},
   {idx:2,key:72,x:330,y:118,isRoot:false},
   {idx:3,key:64,x:105,y:154,isRoot:false},
   {idx:4,key:51,x:195,y:154,isRoot:false},
   {idx:5,key:43,x:285,y:154,isRoot:false},
   {idx:6,key:39,x:375,y:154,isRoot:false}
  ];

  // Tree edges
  const edges=[
   {from:0,to:1},{from:0,to:2},
   {from:1,to:3},{from:1,to:4},
   {from:2,to:5},{from:2,to:6}
  ];

  edges.forEach(e=>{
   const n1=treeNodes[e.from],n2=treeNodes[e.to];
   svg+='<line x1="'+n1.x+'" y1="'+n1.y+'" x2="'+n2.x+'" y2="'+n2.y+'" stroke="#243c4a" stroke-width="1.8"/>';
  });

  treeNodes.forEach(nd=>{
   const fillCol=nd.isRoot?'#431407':'#081016';
   const strokeCol=nd.isRoot?orange:'#38bdf8';
   svg+='<circle cx="'+nd.x+'" cy="'+nd.y+'" r="12" fill="'+fillCol+'" stroke="'+strokeCol+'" stroke-width="1.8"/>';
   svg+='<text x="'+nd.x+'" y="'+(nd.y+3.5)+'" text-anchor="middle" fill="'+(nd.isRoot?'#fed7aa':'#dcebf2')+'" font-size="7.5" font-weight="bold">'+nd.key+'</text>';
   svg+='<text x="'+nd.x+'" y="'+(nd.y-14)+'" text-anchor="middle" fill="#64748b" font-size="6.5" font-family="monospace">['+nd.idx+']</text>';
  });

  // Array Buffer Visualization at Bottom
  const arrY=184;
  svg+='<text x="50" y="'+(arrY-6)+'" fill="#38bdf8" font-size="7.5" font-weight="bold">CONTIGUOUS ARRAY BUFFER A[0..n-1] (ZERO POINTER OVERHEAD)</text>';
  
  const cellW=48,cellH=28,startX=55;
  treeNodes.forEach((nd,i)=>{
   const cX=startX+i*(cellW+6);
   svg+='<rect x="'+cX+'" y="'+arrY+'" width="'+cellW+'" height="'+cellH+'" rx="3" fill="#081016" stroke="'+(nd.isRoot?orange:'#1e3340')+'" stroke-width="1.2"/>';
   svg+='<text x="'+(cX+cellW/2)+'" y="'+(arrY+12)+'" text-anchor="middle" fill="#64748b" font-size="6" font-family="monospace">A['+nd.idx+']</text>';
   svg+='<text x="'+(cX+cellW/2)+'" y="'+(arrY+24)+'" text-anchor="middle" fill="'+(nd.isRoot?'#fed7aa':'#38bdf8')+'" font-size="8" font-weight="bold">'+nd.key+'</text>';
  });

  // Telemetry box below array
  const regX=50,regY=226,regW=380,regH=38;
  svg+='<rect x="'+regX+'" y="'+regY+'" width="'+regW+'" height="'+regH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+14)+'" fill="#38bdf8" font-size="7.5" font-family="monospace">Floyd Model: C(n) = 2(n − log₂ n) = '+c_total+' comparisons · Height h = ⌊log₂('+n+')⌋ = '+h+'</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+28)+'" fill="#8ba5b5" font-size="6.5">Implicit Arithmetic: Left = 2i + 1 · Right = 2i + 2 · Parent = ⌊(i − 1) / 2⌋ · Space: 8n bytes</text>';

  const bX=465,bY=38,bW=220,bH=235;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">FLOYD HEAPIFY COMPARISONS C(n)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">'+c_total+'</text>';
  svg+='<text x="'+(bX+105)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="11">comps</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">DATASET SCALE (n)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+126)+'" fill="'+ink+'" font-size="18" font-family="monospace" font-weight="bold">'+n+' keys</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+142)+'" fill="#8ba5b5" font-size="8">Complete binary tree height: '+h+' levels</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+156)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+156)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+174)+'" fill="#7e9bab" font-size="9">HEAP INVARIANT VERIFICATION</text>';
  svg+=text(bX+bW/2,bY+196,'Max-Heap: A[Parent] ≥ A[Child]','#10b981',10);
  svg+=text(bX+bW/2,bY+214,'Pointer Overhead: 0 Bytes (Contiguous)',orange,8.5);

  svg+=text(360,305,'Mathematical Model: C(n) = 2.0000 · (n - log₂ n) comps · R² = 1.000000',soft,10);
  return svg;
 }

 if(cfg.slug==='binary-search-trees'){
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  const n=p.input;
  const h_levels=v.raw;
  const maxCap=(2**Math.min(20, h_levels)) - 1;

  svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+=text(240,24,'Complete Binary Search Tree Architecture & Search Path Telemetry');

  svg+='<text x="50" y="58" fill="#7e9bab" font-size="8.5" font-weight="bold">BALANCED BINARY TREE TOPOLOGY (n = '+n+' KEYS · HEIGHT = '+h_levels+' LEVELS)</text>';

  // Tree nodes: Level 0 (Root), Level 1 (2 nodes), Level 2 (4 nodes), Level 3 (8 leaf stubs)
  const treeNodes=[
   {key:50,x:240,y:80,isPath:true,lvl:0},
   {key:25,x:140,y:125,isPath:false,lvl:1},
   {key:75,x:340,y:125,isPath:true,lvl:1},
   {key:12,x:90,y:168,isPath:false,lvl:2},
   {key:37,x:190,y:168,isPath:false,lvl:2},
   {key:62,x:290,y:168,isPath:true,lvl:2},
   {key:87,x:390,y:168,isPath:false,lvl:2}
  ];

  // Tree edges
  const edges=[
   {from:0,to:1,isPath:false},
   {from:0,to:2,isPath:true},
   {from:1,to:3,isPath:false},
   {from:1,to:4,isPath:false},
   {from:2,to:5,isPath:true},
   {from:2,to:6,isPath:false}
  ];

  edges.forEach(e=>{
   const n1=treeNodes[e.from],n2=treeNodes[e.to];
   const strokeCol=e.isPath?orange:'#243c4a';
   const strokeW=e.isPath?2.5:1.5;
   svg+='<line x1="'+n1.x+'" y1="'+n1.y+'" x2="'+n2.x+'" y2="'+n2.y+'" stroke="'+strokeCol+'" stroke-width="'+strokeW+'"/>';
  });

  treeNodes.forEach(nd=>{
   const fillCol=nd.isPath?'#431407':'#081016';
   const strokeCol=nd.isPath?orange:'#38bdf8';
   svg+='<circle cx="'+nd.x+'" cy="'+nd.y+'" r="14" fill="'+fillCol+'" stroke="'+strokeCol+'" stroke-width="2"/>';
   svg+='<text x="'+nd.x+'" y="'+(nd.y+4)+'" text-anchor="middle" fill="'+(nd.isPath?'#fed7aa':'#dcebf2')+'" font-size="8" font-weight="bold">'+nd.key+'</text>';
  });

  // Query search banner
  const qbX=50,qbY=195,qbW=375,qbH=32;
  svg+='<rect x="'+qbX+'" y="'+qbY+'" width="'+qbW+'" height="'+qbH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(qbX+10)+'" y="'+(qbY+20)+'" fill="'+orange+'" font-size="8" font-family="monospace">Search Query k = 62: Root (50) ⟶ Right (75) ⟶ Left (62) [Found in 3 comparisons]</text>';

  // Telemetry box
  const regX=50,regY=232,regW=375,regH=35;
  svg+='<rect x="'+regX+'" y="'+regY+'" width="'+regW+'" height="'+regH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+14)+'" fill="#38bdf8" font-size="7.5" font-family="monospace">Height Model: h(n) = ⌊log₂('+n+')⌋ + 1 = '+h_levels+' levels · Capacity N_max = 2^'+h_levels+' − 1 = '+maxCap+'</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+27)+'" fill="#8ba5b5" font-size="6.5">Invariant: In-order traversal (Left, Node, Right) outputs keys in strictly ascending sorted order</text>';

  const bX=465,bY=38,bW=220,bH=235;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">BALANCED TREE HEIGHT (h)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">'+h_levels+'</text>';
  svg+='<text x="'+(bX+75)+'" y="'+(bY+50)+'" fill="#8ba5b5" font-size="11">levels</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">KEY DATASET SCALE (n)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+126)+'" fill="'+ink+'" font-size="18" font-family="monospace" font-weight="bold">'+n+' keys</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+142)+'" fill="#8ba5b5" font-size="8">Entropy log₂(n) = '+(Math.log2(n)).toFixed(2)+' bits</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+156)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+156)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+174)+'" fill="#7e9bab" font-size="9">SEARCH PATH COMPLEXITY</text>';
  svg+=text(bX+bW/2,bY+196,'Worst-Case: O(log n)','#10b981',11);
  svg+=text(bX+bW/2,bY+214,'Degenerate without balancing: O(n)',orange,8.5);

  svg+=text(360,305,'Mathematical Model: h(n) = 1.0000 · log₂(n) + 1.0000 levels · R² = 1.000000',soft,10);
  return svg;
 }

 if(cfg.slug==='linked-list-architectures'){
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  const n=p.input;
  const m_total=v.raw;

  svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+=text(240,24,'Doubly Linked List Heap Architecture & Sentinel Invariants');

  svg+='<text x="50" y="58" fill="#7e9bab" font-size="8.5" font-weight="bold">DYNAMIC HEAP NODES [32 BYTES EACH] &amp; SENTINELS (n = '+n+')</text>';

  // Nodes visualization: Head, Node 1, Node 2, Tail
  const nodes=[
   {name:'HEAD',addr:'0x10A0',val:'[SENTINEL]',isSent:true,col:'#38bdf8'},
   {name:'NODE 1',addr:'0x23F8',val:'val: 42',isSent:false,col:'#10b981'},
   {name:'NODE 2',addr:'0x3A10',val:'val: 87',isSent:false,col:'#10b981'},
   {name:'TAIL',addr:'0x41E0',val:'[SENTINEL]',isSent:true,col:'#ef4444'}
  ];

  const nW=76,nH=70;
  const startX=48,nY=72;
  const spacing=18;

  nodes.forEach((nd,i)=>{
   const nx=startX+i*(nW+spacing);
   svg+='<rect x="'+nx+'" y="'+nY+'" width="'+nW+'" height="'+nH+'" rx="4" fill="#081016" stroke="'+nd.col+'" stroke-width="'+(nd.isSent?1.5:2)+'"/>';
   svg+='<rect x="'+nx+'" y="'+nY+'" width="'+nW+'" height="16" rx="4" fill="'+(nd.isSent?(i===0?'#0c4a6e':'#451a03'):'#064e3b')+'"/>';
   svg+='<text x="'+(nx+nW/2)+'" y="'+(nY+11)+'" text-anchor="middle" fill="#dcebf2" font-size="7" font-weight="bold">'+nd.name+'</text>';
   svg+='<text x="'+(nx+nW/2)+'" y="'+(nY+28)+'" text-anchor="middle" fill="#94a3b8" font-size="6.5" font-family="monospace">'+nd.addr+'</text>';
   svg+='<text x="'+(nx+nW/2)+'" y="'+(nY+42)+'" text-anchor="middle" fill="'+(nd.isSent?'#94a3b8':'#fde047')+'" font-size="7.5" font-family="monospace">'+nd.val+'</text>';
   svg+='<text x="'+(nx+nW/2)+'" y="'+(nY+56)+'" text-anchor="middle" fill="#38bdf8" font-size="6" font-family="monospace">prev:8B | next:8B</text>';
   svg+='<text x="'+(nx+nW/2)+'" y="'+(nY+66)+'" text-anchor="middle" fill="#64748b" font-size="5.5">pad: 8B (16B align)</text>';

   if(i<nodes.length-1){
    const arrowX1=nx+nW,arrowX2=nx+nW+spacing;
    // Next forward arrow (blue/green, top)
    svg+='<line x1="'+arrowX1+'" y1="'+(nY+30)+'" x2="'+arrowX2+'" y2="'+(nY+30)+'" stroke="#38bdf8" stroke-width="1.5"/>';
    svg+='<polygon points="'+arrowX2+','+(nY+30)+' '+(arrowX2-4)+','+(nY+27)+' '+(arrowX2-4)+','+(nY+33)+'" fill="#38bdf8"/>';
    // Prev backward arrow (orange, bottom)
    svg+='<line x1="'+arrowX2+'" y1="'+(nY+50)+'" x2="'+arrowX1+'" y2="'+(nY+50)+'" stroke="'+orange+'" stroke-width="1.5"/>';
    svg+='<polygon points="'+arrowX1+','+(nY+50)+' '+(arrowX1+4)+','+(nY+47)+' '+(arrowX1+4)+','+(nY+53)+'" fill="'+orange+'"/>';
   }
  });

  // Pointer legend and node memory breakdown
  const legX=50,legY=155,legW=375,legH=45;
  svg+='<rect x="'+legX+'" y="'+legY+'" width="'+legW+'" height="'+legH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(legX+10)+'" y="'+(legY+15)+'" fill="#38bdf8" font-size="8" font-weight="bold">64-BIT NODE MEMORY LAYOUT (32 BYTES TOTAL)</text>';
  svg+='<rect x="'+(legX+10)+'" y="'+(legY+22)+'" width="80" height="16" rx="2" fill="#064e3b" stroke="#10b981"/>';
  svg+='<text x="'+(legX+50)+'" y="'+(legY+33)+'" text-anchor="middle" fill="#dcebf2" font-size="6.5" font-family="monospace">Data: 8B</text>';
  svg+='<rect x="'+(legX+95)+'" y="'+(legY+22)+'" width="80" height="16" rx="2" fill="#0c4a6e" stroke="#38bdf8"/>';
  svg+='<text x="'+(legX+135)+'" y="'+(legY+33)+'" text-anchor="middle" fill="#dcebf2" font-size="6.5" font-family="monospace">Next*: 8B</text>';
  svg+='<rect x="'+(legX+180)+'" y="'+(legY+22)+'" width="80" height="16" rx="2" fill="#431407" stroke="'+orange+'"/>';
  svg+='<text x="'+(legX+220)+'" y="'+(legY+33)+'" text-anchor="middle" fill="#dcebf2" font-size="6.5" font-family="monospace">Prev*: 8B</text>';
  svg+='<rect x="'+(legX+265)+'" y="'+(legY+22)+'" width="100" height="16" rx="2" fill="#1e293b" stroke="#64748b"/>';
  svg+='<text x="'+(legX+315)+'" y="'+(legY+33)+'" text-anchor="middle" fill="#94a3b8" font-size="6.5" font-family="monospace">Align Pad: 8B</text>';

  // Telemetry box
  const regX=50,regY=210,regW=375,regH=55;
  svg+='<rect x="'+regX+'" y="'+regY+'" width="'+regW+'" height="'+regH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+16)+'" fill="#38bdf8" font-size="8" font-family="monospace">Heap Model: M(n) = 32 × '+n+' + 64 = '+m_total+' bytes ('+(m_total/1024).toFixed(2)+' KiB)</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+32)+'" fill="'+orange+'" font-size="8" font-family="monospace">Metadata Overhead: 24 bytes metadata per 8 bytes data ⟹ 300% pointer overhead</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+48)+'" fill="#8ba5b5" font-size="7">Sentinel Optimization: Eliminates head/tail null checks; splices execute in strict O(1) time</text>';

  const bX=465,bY=38,bW=220,bH=235;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+24)+'" fill="#7e9bab" font-size="9">HEAP FOOTPRINT PER NODE</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+54)+'" fill="'+orange+'" font-size="24" font-family="monospace" font-weight="bold">32 Bytes</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+70)+'" fill="#8ba5b5" font-size="8">8B Data + 16B Pointers + 8B Padding</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+84)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+84)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+102)+'" fill="#7e9bab" font-size="9">SENTINEL BASE OVERHEAD</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+126)+'" fill="'+ink+'" font-size="18" font-family="monospace" font-weight="bold">64 Bytes</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+142)+'" fill="#8ba5b5" font-size="8">Sentinel Head (32B) + Sentinel Tail (32B)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+156)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+156)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+174)+'" fill="#7e9bab" font-size="9">POINTER SPLICE TIME</text>';
  svg+=text(bX+bW/2,bY+196,'Strict O(1) Splicing','#10b981',11);
  svg+=text(bX+bW/2,bY+214,'4 pointer updates, 0 array copies',orange,8.5);

  svg+=text(360,305,'Mathematical Model: M(n) = 32.0000 · n + 64.0000 bytes · R² = 1.000000',soft,10);
  return svg;
 }

 if(cfg.slug==='queue-buffer-management'){
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  const n=p.input;
  const v_total=v.raw;
  const wrapCycles=Math.floor(n/12);

  svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+=text(240,24,'Circular Ring Buffer Memory Architecture & Pointer Invariants');

  // Ring Array slots layout
  const numSlots=12;
  const slotW=28,slotH=36;
  const startX=48,slotY=70;
  const frontIdx=3,rearIdx=8;

  svg+='<text x="50" y="58" fill="#7e9bab" font-size="8.5" font-weight="bold">CIRCULAR BUFFER ARRAY SLOTS [0 .. 11] (N = 12)</text>';
  svg+='<text x="430" y="58" text-anchor="end" fill="'+orange+'" font-size="8.5" font-weight="bold">OCCUPANCY = 5 / 12</text>';

  for(let i=0;i<numSlots;i++){
   const sx=startX+i*(slotW+3);
   const isOccupied=(i>=frontIdx && i<rearIdx);
   const isFront=i===frontIdx;
   const isRear=i===rearIdx;

   let fillCol='#111c24',strokeCol='#243c4a';
   if(isOccupied){fillCol='#064e3b';strokeCol='#10b981';}
   if(isFront){strokeCol='#38bdf8';}
   if(isRear){strokeCol=orange;}

   svg+='<rect x="'+sx+'" y="'+slotY+'" width="'+slotW+'" height="'+slotH+'" rx="2" fill="'+fillCol+'" stroke="'+strokeCol+'" stroke-width="'+(isFront||isRear?2:1)+'"/>';
   svg+='<text x="'+(sx+slotW/2)+'" y="'+(slotY+slotH/2+4)+'" text-anchor="middle" fill="'+(isOccupied?'#6ee7b7':'#5a7687')+'" font-size="8" font-family="monospace">'+(isOccupied?'P'+(i+1):'—')+'</text>';
   svg+='<text x="'+(sx+slotW/2)+'" y="'+(slotY+slotH+11)+'" text-anchor="middle" fill="#5a7687" font-size="6.5">['+i+']</text>';
  }

  // Front Cursor Arrow (Top)
  const frontPx=startX+frontIdx*(slotW+3)+slotW/2;
  svg+='<polygon points="'+frontPx+','+(slotY-3)+' '+(frontPx-4)+','+(slotY-9)+' '+(frontPx+4)+','+(slotY-9)+'" fill="#38bdf8"/>';
  svg+='<text x="'+frontPx+'" y="'+(slotY-11)+'" text-anchor="middle" fill="#38bdf8" font-size="7.5" font-weight="bold">front (head)</text>';

  // Rear Cursor Arrow (Top)
  const rearPx=startX+rearIdx*(slotW+3)+slotW/2;
  svg+='<polygon points="'+rearPx+','+(slotY-3)+' '+(rearPx-4)+','+(slotY-9)+' '+(rearPx+4)+','+(slotY-9)+'" fill="'+orange+'"/>';
  svg+='<text x="'+rearPx+'" y="'+(slotY-11)+'" text-anchor="middle" fill="'+orange+'" font-size="7.5" font-weight="bold">rear (tail)</text>';

  // Modular Wrap-Around Arrow beneath array
  svg+='<path d="M '+(startX+(numSlots-1)*(slotW+3)+slotW)+' '+(slotY+slotH+18)+' Q 240 '+(slotY+slotH+35)+' '+startX+' '+(slotY+slotH+18)+'" fill="none" stroke="'+orange+'" stroke-width="1.5" stroke-dasharray="3 3"/>';
  svg+='<polygon points="'+startX+','+(slotY+slotH+18)+' '+(startX+6)+','+(slotY+slotH+14)+' '+(startX+6)+','+(slotY+slotH+22)+'" fill="'+orange+'"/>';
  svg+='<text x="240" y="'+(slotY+slotH+32)+'" text-anchor="middle" fill="'+orange+'" font-size="7.5" font-family="monospace">Modular Wrap: next = (index + 1) mod 12</text>';

  // Cache line padding diagram (Descriptor)
  const padX=50,padY=145,padW=375,padH=50;
  svg+='<rect x="'+padX+'" y="'+padY+'" width="'+padW+'" height="'+padH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(padX+10)+'" y="'+(padY+15)+'" fill="#38bdf8" font-size="8" font-weight="bold">CACHE-LINE PADDED DESCRIPTOR BLOCK (256 BYTES)</text>';
  
  // Cache Line 0 (Head)
  svg+='<rect x="'+(padX+10)+'" y="'+(padY+22)+'" width="80" height="20" rx="2" fill="#0c4a6e" stroke="#38bdf8"/>';
  svg+='<text x="'+(padX+50)+'" y="'+(padY+35)+'" text-anchor="middle" fill="#dcebf2" font-size="7" font-family="monospace">Head (64B Pad)</text>';

  // Cache Line 1 (Tail)
  svg+='<rect x="'+(padX+95)+'" y="'+(padY+22)+'" width="80" height="20" rx="2" fill="#431407" stroke="'+orange+'"/>';
  svg+='<text x="'+(padX+135)+'" y="'+(padY+35)+'" text-anchor="middle" fill="#dcebf2" font-size="7" font-family="monospace">Tail (64B Pad)</text>';

  // Cache Line 2 & 3 (Capacity & Mutex)
  svg+='<rect x="'+(padX+180)+'" y="'+(padY+22)+'" width="95" height="20" rx="2" fill="#1e293b" stroke="#64748b"/>';
  svg+='<text x="'+(padX+227)+'" y="'+(padY+35)+'" text-anchor="middle" fill="#94a3b8" font-size="7" font-family="monospace">Capacity & Flags (64B)</text>';

  svg+='<rect x="'+(padX+280)+'" y="'+(padY+22)+'" width="85" height="20" rx="2" fill="#1e293b" stroke="#64748b"/>';
  svg+='<text x="'+(padX+322)+'" y="'+(padY+35)+'" text-anchor="middle" fill="#94a3b8" font-size="7" font-family="monospace">Mutex State (64B)</text>';

  const regX=50,regY=205,regW=375,regH=58;
  svg+='<rect x="'+regX+'" y="'+regY+'" width="'+regW+'" height="'+regH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+16)+'" fill="#38bdf8" font-size="8" font-family="monospace">Atomic Cursors: front = '+frontIdx+' · rear = '+rearIdx+' ⟹ Occupancy = ('+rearIdx+' − '+frontIdx+' + 12) % 12 = 5</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+32)+'" fill="'+orange+'" font-size="8" font-family="monospace">Memory Bus Telemetry: Cumulative Volume V = '+v_total+' bytes ('+(v_total/1024).toFixed(2)+' KiB)</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+48)+'" fill="#8ba5b5" font-size="7">Full/Empty Invariant: (rear + 1) % N == front ⟹ Buffer Full · front == rear ⟹ Buffer Empty</text>';

  const bX=465,bY=38,bW=220,bH=235;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">PACKET BATCH SIZE (n)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+n+'</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#8ba5b5" font-size="11">packets</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+64)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+64)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+82)+'" fill="#7e9bab" font-size="9">MEMORY TRANSFER VOLUME V(n)</text>';
  const volKb=(v_total/1024).toFixed(2);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+106)+'" fill="'+ink+'" font-size="18" font-family="monospace" font-weight="bold">'+v_total+'</text>';
  svg+='<text x="'+(bX+120)+'" y="'+(bY+104)+'" fill="#8ba5b5" font-size="10">bytes ('+volKb+' KiB)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+120)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+120)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+138)+'" fill="#7e9bab" font-size="9">UNIT PACKET PAYLOAD L_packet</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+164)+'" fill="#fde047" font-size="20" font-family="monospace" font-weight="bold">64.0000</text>';
  svg+='<text x="'+(bX+125)+'" y="'+(bY+160)+'" fill="#8ba5b5" font-size="9">bytes/packet</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+178)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+178)+'" stroke="#1e3340"/>';

  svg+=text(bX+bW/2,bY+200,'V = L_packet · n + V_0',ink,10);
  svg+=text(bX+bW/2,bY+218,'Cache Line Unit: 64 B/packet',orange,9);

  svg+=text(360,305,'Microarchitectural Invariant: V(n) = 64·n + 256 bytes = Θ(n) · Ring Wraparounds: '+wrapCycles,soft,10);
  $('apparatusDiagram').innerHTML=svg;
  return;
 }

 if(cfg.slug==='stack-adt-recursion'){
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  const n=p.input;
  const m_total=v.raw;
  const delta_rsp=m_total;

  svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+=text(240,24,'Microarchitectural Thread Call Stack & Activation Records');

  // Memory Stack Segment growing downward
  const sX=55,sY=55,sW=175,sH=150;
  svg+='<text x="'+sX+'" y="48" fill="#7e9bab" font-size="8">VIRTUAL ADDRESS SPACE (THREAD STACK)</text>';
  svg+='<text x="'+(sX+sW)+'" y="48" text-anchor="end" fill="'+orange+'" font-size="7.5">GROWTH 🠗 TOWARD LOW ADDR</text>';
  svg+='<rect x="'+sX+'" y="'+sY+'" width="'+sW+'" height="'+sH+'" rx="3" fill="#0a1218" stroke="#223a4a" stroke-width="1.5"/>';

  // Base Frame (CRT startup, 128 bytes)
  svg+='<rect x="'+(sX+4)+'" y="'+(sY+4)+'" width="'+(sW-8)+'" height="20" rx="2" fill="#1e293b" stroke="#475569"/>';
  svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+18)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5" font-family="monospace">Base Frame M_0 [128 B]</text>';

  // Frame 1
  svg+='<rect x="'+(sX+4)+'" y="'+(sY+28)+'" width="'+(sW-8)+'" height="20" rx="2" fill="#162a36" stroke="#334d5c"/>';
  svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+42)+'" text-anchor="middle" fill="#8ba5b5" font-size="7.5" font-family="monospace">Frame 1: rec(n) [64 B]</text>';

  // Frame 2
  svg+='<rect x="'+(sX+4)+'" y="'+(sY+52)+'" width="'+(sW-8)+'" height="20" rx="2" fill="#162a36" stroke="#334d5c"/>';
  svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+66)+'" text-anchor="middle" fill="#8ba5b5" font-size="7.5" font-family="monospace">Frame 2: rec(n-1) [64 B]</text>';

  // Ellipsis
  svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+82)+'" text-anchor="middle" fill="#5a7687" font-size="9">⋮ (depth = '+n+' frames)</text>';

  // Active Frame n (Top of Stack)
  const activeFrameY=sY+92;
  svg+='<rect x="'+(sX+4)+'" y="'+activeFrameY+'" width="'+(sW-8)+'" height="26" rx="2" fill="#0c4a6e" stroke="'+orange+'" stroke-width="1.5"/>';
  svg+='<text x="'+(sX+sW/2)+'" y="'+(activeFrameY+13)+'" text-anchor="middle" fill="#fde047" font-size="7.5" font-family="monospace" font-weight="bold">Active Frame n: rec(1)</text>';
  svg+='<text x="'+(sX+sW/2)+'" y="'+(activeFrameY+23)+'" text-anchor="middle" fill="'+orange+'" font-size="6.5">64 Bytes (RBP + RIP + Locals)</text>';

  // Guard page at bottom of stack
  const guardY=sY+124;
  svg+='<rect x="'+(sX+4)+'" y="'+guardY+'" width="'+(sW-8)+'" height="18" rx="2" fill="#450a0a" stroke="#ef4444" stroke-dasharray="3 3"/>';
  svg+='<text x="'+(sX+sW/2)+'" y="'+(guardY+12)+'" text-anchor="middle" fill="#fca5a5" font-size="7" font-family="monospace">MMU Guard Page (4 KiB)</text>';

  // RSP Pointer Arrow
  const rspY=activeFrameY+13;
  svg+='<line x1="'+(sX-22)+'" y1="'+rspY+'" x2="'+(sX-3)+'" y2="'+rspY+'" stroke="'+orange+'" stroke-width="2"/>';
  svg+='<polygon points="'+(sX-3)+','+rspY+' '+(sX-8)+','+(rspY-4)+' '+(sX-8)+','+(rspY+4)+'" fill="'+orange+'"/>';
  svg+='<text x="'+(sX-25)+'" y="'+(rspY+3)+'" text-anchor="end" fill="'+orange+'" font-size="8.5" font-weight="bold">RSP</text>';

  // Detail card of the 64-Byte Activation Record
  const dX=245,dY=55,dW=185,dH=150;
  svg+='<rect x="'+dX+'" y="'+dY+'" width="'+dW+'" height="'+dH+'" rx="4" fill="#0b151b" stroke="#38bdf8" stroke-width="1.5"/>';
  svg+='<text x="'+(dX+dW/2)+'" y="'+(dY-5)+'" text-anchor="middle" fill="#38bdf8" font-size="8" font-weight="bold">SYSTEM V AMD64 FRAME (64 BYTES)</text>';

  const frameParts=[
   {name:'Return Address (RIP+5)',size:'8 B',col:'#38bdf8',off:'[RSP + 56]'},
   {name:'Saved Base Pointer (RBP)',size:'8 B',col:'#10b981',off:'[RSP + 48]'},
   {name:'Callee Registers (RBX,R12)',size:'16 B',col:'#a855f7',off:'[RSP + 32]'},
   {name:'Local Variables & Spill',size:'32 B',col:orange,off:'[RSP + 0]'}
  ];
  let curY=dY+12;
  frameParts.forEach(fp=>{
   const partH=24;
   svg+='<rect x="'+(dX+8)+'" y="'+curY+'" width="'+(dW-16)+'" height="'+partH+'" rx="2" fill="#16242c" stroke="'+fp.col+'" stroke-width="1"/>';
   svg+='<text x="'+(dX+14)+'" y="'+(curY+12)+'" fill="#dcebf2" font-size="7.5" font-weight="bold">'+fp.name+'</text>';
   svg+='<text x="'+(dX+dW-14)+'" y="'+(curY+12)+'" text-anchor="end" fill="'+fp.col+'" font-size="7.5" font-family="monospace">'+fp.size+'</text>';
   svg+='<text x="'+(dX+14)+'" y="'+(curY+21)+'" fill="#5a7687" font-size="6.5" font-family="monospace">'+fp.off+'</text>';
   curY+=partH+6;
  });

  const regX=55,regY=215,regW=375,regH=48;
  svg+='<rect x="'+regX+'" y="'+regY+'" width="'+regW+'" height="'+regH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+16)+'" fill="#38bdf8" font-size="8" font-family="monospace">CPU Registers: RSP = 0x7FFF_FFFF_E000 − '+delta_rsp+' B · RBP = [Frame Base]</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+30)+'" fill="'+orange+'" font-size="8" font-family="monospace">Memory Bus: Peak Stack Watermark = '+m_total+' bytes ('+(m_total/1024).toFixed(2)+' KiB)</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+42)+'" fill="#8ba5b5" font-size="7">ABI Invariant: RSP aligned to 16-byte boundary prior to CALL · Base Frame M_0 = 128 bytes</text>';

  const bX=465,bY=38,bW=220,bH=235;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">RECURSION DEPTH (n)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+n+'</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#8ba5b5" font-size="11">frames</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+64)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+64)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+82)+'" fill="#7e9bab" font-size="9">PEAK STACK MEMORY M(n)</text>';
  const memKb=(m_total/1024).toFixed(2);
  svg+='<text x="'+(bX+15)+'" y="'+(bY+106)+'" fill="'+ink+'" font-size="18" font-family="monospace" font-weight="bold">'+m_total+'</text>';
  svg+='<text x="'+(bX+120)+'" y="'+(bY+104)+'" fill="#8ba5b5" font-size="10">bytes ('+memKb+' KiB)</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+120)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+120)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+138)+'" fill="#7e9bab" font-size="9">ESTIMATED FRAME SIZE F_frame</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+164)+'" fill="#fde047" font-size="20" font-family="monospace" font-weight="bold">64.0000</text>';
  svg+='<text x="'+(bX+125)+'" y="'+(bY+160)+'" fill="#8ba5b5" font-size="9">bytes/frame</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+178)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+178)+'" stroke="#1e3340"/>';

  svg+=text(bX+bW/2,bY+200,'M = F_frame · n + M_0',ink,10);
  svg+=text(bX+bW/2,bY+218,'System V ABI Gradient: 64 B/frame',orange,9);

  svg+=text(360,305,'Microarchitectural Invariant: M(n) = 64·n + 128 bytes = Θ(n) · Thread Limit: 8 MiB',soft,10);
  $('apparatusDiagram').innerHTML=svg;
  return;
 }

 if(cfg.slug==='divide-conquer-sorting'){
  let svg='<defs><pattern id="labGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".035" fill="none"/></pattern></defs><rect width="720" height="320" fill="url(#labGrid)"/>';
  const text=(x,y,str,color='#8ba5b5',size=12)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';

  const n=p.input;
  const log2n=Math.log2(n);
  const intervalSpace=Math.round(n*(log2n - 1));
  const c_total=v.raw;

  svg+='<rect x="35" y="38" width="410" height="235" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+=text(240,24,'Virtual Memory Buffer & Divide-and-Conquer Merge Bench');

  const halfN=6;
  const cellW=26,cellH=30;
  const leftX=55,rightX=leftX+halfN*(cellW+3)+12,rowY=70;
  const leftVals=[14, 29, 42, 58, 77, 91];
  const rightVals=[18, 25, 36, 64, 83, 95];
  const p1=2,p2=1;

  svg+='<text x="55" y="58" fill="#38bdf8" font-size="8.5" font-weight="bold">LEFT SUBARRAY L[0..'+(Math.floor(n/2)-1)+']</text>';
  for(let i=0;i<halfN;i++){
   const cx=leftX+i*(cellW+3);
   const isCur=i===p1;
   svg+='<rect x="'+cx+'" y="'+rowY+'" width="'+cellW+'" height="'+cellH+'" rx="2" fill="'+(isCur?'#0c4a6e':'#11222c')+'" stroke="'+(isCur?orange:'#38bdf8')+'" stroke-width="'+(isCur?2:1)+'"/>';
   svg+='<text x="'+(cx+cellW/2)+'" y="'+(rowY+cellH/2+4)+'" text-anchor="middle" fill="'+(isCur?'#fde047':'#dcebf2')+'" font-size="8" font-family="monospace">'+leftVals[i]+'</text>';
   svg+='<text x="'+(cx+cellW/2)+'" y="'+(rowY+cellH+10)+'" text-anchor="middle" fill="#5a7687" font-size="6.5">['+i+']</text>';
  }
  const p1Px=leftX+p1*(cellW+3)+cellW/2;
  svg+='<polygon points="'+p1Px+','+(rowY-3)+' '+(p1Px-4)+','+(rowY-9)+' '+(p1Px+4)+','+(rowY-9)+'" fill="'+orange+'"/>';
  svg+='<text x="'+p1Px+'" y="'+(rowY-11)+'" text-anchor="middle" fill="'+orange+'" font-size="7" font-weight="bold">p1</text>';

  svg+='<text x="'+rightX+'" y="58" fill="#a855f7" font-size="8.5" font-weight="bold">RIGHT SUBARRAY R[0..'+(Math.floor(n/2)-1)+']</text>';
  for(let i=0;i<halfN;i++){
   const cx=rightX+i*(cellW+3);
   const isCur=i===p2;
   svg+='<rect x="'+cx+'" y="'+rowY+'" width="'+cellW+'" height="'+cellH+'" rx="2" fill="'+(isCur?'#3b0764':'#1a1128')+'" stroke="'+(isCur?orange:'#a855f7')+'" stroke-width="'+(isCur?2:1)+'"/>';
   svg+='<text x="'+(cx+cellW/2)+'" y="'+(rowY+cellH/2+4)+'" text-anchor="middle" fill="'+(isCur?'#fde047':'#dcebf2')+'" font-size="8" font-family="monospace">'+rightVals[i]+'</text>';
   svg+='<text x="'+(cx+cellW/2)+'" y="'+(rowY+cellH+10)+'" text-anchor="middle" fill="#5a7687" font-size="6.5">['+i+']</text>';
  }
  const p2Px=rightX+p2*(cellW+3)+cellW/2;
  svg+='<polygon points="'+p2Px+','+(rowY-3)+' '+(p2Px-4)+','+(rowY-9)+' '+(p2Px+4)+','+(rowY-9)+'" fill="'+orange+'"/>';
  svg+='<text x="'+p2Px+'" y="'+(rowY-11)+'" text-anchor="middle" fill="'+orange+'" font-size="7" font-weight="bold">p2</text>';

  // Scratchpad
  const scratchY=145,sW=24,sH=28;
  const mergedVals=[14, 18, 25];
  svg+='<text x="55" y="'+(scratchY-8)+'" fill="#10b981" font-size="8.5" font-weight="bold">MERGE SCRATCHPAD M[0 .. '+(n-1)+'] (AUXILIARY BUFFER O(n))</text>';
  for(let i=0;i<12;i++){
   const cx=55+i*(sW+4);
   const hasVal=i<mergedVals.length;
   const isWriteTarget=i===mergedVals.length;
   svg+='<rect x="'+cx+'" y="'+scratchY+'" width="'+sW+'" height="'+sH+'" rx="2" fill="'+(hasVal?'#064e3b':isWriteTarget?'#1e3e52':'#0f171d')+'" stroke="'+(hasVal?'#10b981':isWriteTarget?orange:'#243c4a')+'" stroke-width="'+(isWriteTarget?1.5:1)+'"/>';
   if(hasVal){
    svg+='<text x="'+(cx+sW/2)+'" y="'+(scratchY+sH/2+4)+'" text-anchor="middle" fill="#6ee7b7" font-size="7.5" font-family="monospace">'+mergedVals[i]+'</text>';
   } else if(isWriteTarget){
    svg+='<text x="'+(cx+sW/2)+'" y="'+(scratchY+sH/2+4)+'" text-anchor="middle" fill="'+orange+'" font-size="7">next</text>';
   }
   svg+='<text x="'+(cx+sW/2)+'" y="'+(scratchY+sH+10)+'" text-anchor="middle" fill="#5a7687" font-size="6">['+i+']</text>';
  }

  const regX=55,regY=195,regW=370,regH=65;
  svg+='<rect x="'+regX+'" y="'+regY+'" width="'+regW+'" height="'+regH+'" rx="4" fill="#081016" stroke="#1e3340" stroke-width="1.2"/>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+16)+'" fill="#38bdf8" font-size="8" font-family="monospace">ALU Comparator: L['+p1+'] ('+leftVals[p1]+') <= R['+p2+'] ('+rightVals[p2]+') ? ⟹ TRUE</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+32)+'" fill="'+orange+'" font-size="8" font-family="monospace">Memory Bus: Writing L['+p1+'] ('+leftVals[p1]+') to Scratchpad M['+mergedVals.length+'] · Increment p1</text>';
  svg+='<text x="'+(regX+10)+'" y="'+(regY+48)+'" fill="#8ba5b5" font-size="7.5">Merge Invariant: Subarrays already sorted ⟹ at most (len(L) + len(R) - 1) comparisons</text>';

  const bX=465,bY=38,bW=220,bH=235;
  svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="6" fill="#0d1820" stroke="'+soft+'" stroke-width="1.5"/>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+22)+'" fill="#7e9bab" font-size="9">ARRAY SIZE (n)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+50)+'" fill="'+orange+'" font-size="22" font-family="monospace" font-weight="bold">'+n+'</text>';
  svg+='<text x="'+(bX+95)+'" y="'+(bY+46)+'" fill="#8ba5b5" font-size="11">elements</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+64)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+64)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+82)+'" fill="#7e9bab" font-size="9">RECURSIVE INTERVALS n(log₂ n − 1)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+106)+'" fill="'+ink+'" font-size="18" font-family="monospace" font-weight="bold">'+intervalSpace+'</text>';
  svg+='<text x="'+(bX+120)+'" y="'+(bY+104)+'" fill="#8ba5b5" font-size="10">intervals</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+120)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+120)+'" stroke="#1e3340"/>';

  svg+='<text x="'+(bX+15)+'" y="'+(bY+138)+'" fill="#7e9bab" font-size="9">KEY COMPARISONS C(n)</text>';
  svg+='<text x="'+(bX+15)+'" y="'+(bY+164)+'" fill="#fde047" font-size="20" font-family="monospace" font-weight="bold">'+c_total+'</text>';
  svg+='<text x="'+(bX+105)+'" y="'+(bY+160)+'" fill="#8ba5b5" font-size="9">n log₂ n − n + 1</text>';
  svg+='<line x1="'+(bX+15)+'" y1="'+(bY+178)+'" x2="'+(bX+bW-15)+'" y2="'+(bY+178)+'" stroke="#1e3340"/>';

  svg+=text(bX+bW/2,bY+200,'C = k_merge · n(log₂ n − 1) + 1',ink,10);
  svg+=text(bX+bW/2,bY+218,'Scaling Gradient: k = 1.0000 comp/interval',orange,9);

  svg+=text(360,305,'Algorithmic Complexity: C(n) = n log₂ n − n + 1 = Θ(n log n) · Auxiliary Space: O(n) Buffer',soft,10);
  $('apparatusDiagram').innerHTML=svg;
  return;
 }

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
