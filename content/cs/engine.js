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
