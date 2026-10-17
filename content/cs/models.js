(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

function predict(slug,input){
 if(slug==='search-algorithms-complexity'){
  const n=Number(input);
  const log2n=Math.log2(n);
  const raw=Math.floor(log2n)+1;
  const x=log2n;
  const y=raw;
  return {raw,ideal:raw,period:raw/10.0,x,y,valid:n>=64&&n<=4096};
 }
 if(slug==='quadratic-sorting-algorithms'){
  const n=Number(input);
  const raw=n*(n-1)/2;
  const x=n*(n-1);
  const y=raw;
  return {raw,ideal:raw,period:raw/50.0,x,y,valid:n>=10&&n<=70};
 }
 if(slug==='divide-conquer-sorting'){
  const n=Number(input);
  const log2n=Math.log2(n);
  const raw=Math.round(n*log2n - n + 1);
  const x=n*(log2n - 1);
  const y=raw;
  return {raw,ideal:raw,period:raw/100.0,x,y,valid:n>=64&&n<=4096};
 }
 if(slug==='stack-adt-recursion'){
  const n=Number(input);
  const raw=Math.round(64*n + 128);
  const x=n;
  const y=raw;
  return {raw,ideal:raw,period:raw/500.0,x,y,valid:n>=64&&n<=16384};
 }
 if(slug==='queue-buffer-management'){
  const n=Number(input);
  const raw=Math.round(64*n + 256);
  const x=n;
  const y=raw;
  return {raw,ideal:raw,period:raw/1000.0,x,y,valid:n>=128&&n<=32768};
 }
 if(slug==='linked-list-architectures'){
  const n=Number(input);
  const raw=Math.round(32*n + 64);
  const x=n;
  const y=raw;
  return {raw,ideal:raw,period:raw/500.0,x,y,valid:n>=64&&n<=16384};
 }
 if(slug==='binary-search-trees'){
  const n=Number(input);
  const x=Math.log2(n);
  const raw=Math.floor(x)+1;
  const y=raw;
  return {raw,ideal:raw,period:raw/2.0,x,y,valid:n>=32&&n<=8192};
 }
 if(slug==='binary-heaps-priority-queues'){
  const n=Number(input);
  const log2n=Math.log2(n);
  const raw=Math.round(2*n - 2*log2n);
  const x=n - log2n;
  const y=raw;
  return {raw,ideal:raw,period:raw/1000.0,x,y,valid:n>=32&&n<=8192};
 }
 if(slug==='hash-tables-collision-resolution'){
  const n=Number(input);
  const m_cap=1000;
  const alpha=n/m_cap;
  const x=1/(1 - alpha);
  const raw=round(x, 4);
  const y=raw;
  return {raw,ideal:raw,period:raw/5.0,x,y,valid:n>=100&&n<=950};
 }
 if(slug==='graph-traversal-shortest-paths'){
  const v=Number(input);
  const e=4*v;
  const raw=Math.round(v + e);
  const x=v;
  const y=raw;
  return {raw,ideal:raw,period:raw/500.0,x,y,valid:v>=50&&v<=1000};
 }
 if(slug==='dynamic-programming-memoization'){
  const n=Number(input);
  const w_cap=100;
  const raw=Math.round(w_cap * n);
  const x=n;
  const y=raw;
  return {raw,ideal:raw,period:raw/1000.0,x,y,valid:n>=10&&n<=200};
 }
 if(slug==='greedy-minimum-spanning-trees'){
  const v=Number(input);
  const e=4*v;
  const raw=Math.round(2*e);
  const x=v;
  const y=raw;
  return {raw,ideal:raw,period:raw/800.0,x,y,valid:v>=50&&v<=1000};
 }
 if(slug==='string-matching-automata'){
  const n=Number(input);
  const m=20;
  const raw=Math.round(n + m);
  const x=n;
  const y=raw;
  return {raw,ideal:raw,period:raw/1000.0,x,y,valid:n>=200&&n<=20000};
 }
 if(slug==='network-flow-max-cut'){
  const v=Number(input);
  const raw=Math.round(10*v);
  const x=v;
  const y=raw;
  return {raw,ideal:raw,period:raw/1000.0,x,y,valid:v>=50&&v<=1000};
 }
 if(slug==='trie-prefix-trees'){
  const l=Number(input);
  const raw=Math.round(l + 1);
  const x=l;
  const y=raw;
  return {raw,ideal:raw,period:raw/50.0,x,y,valid:l>=4&&l<=64};
 }
 if(slug==='huffman-coding-compression'){
  const n=Number(input);
  const raw=Math.round(2.5 * n + 64);
  const x=n;
  const y=raw;
  return {raw,ideal:raw,period:raw/20000.0,x,y,valid:n>=500&&n<=50000};
 }
 if(slug==='computational-geometry-convex-hull'){
  const n=Number(input);
  const raw=Math.round(2 * n);
  const x=n;
  const y=raw;
  return {raw,ideal:raw,period:raw/2000.0,x,y,valid:n>=50&&n<=5000};
 }
 if(slug==='backtracking-n-queens-sat'){
  const n=Number(input);
  const raw=Math.round(4 * n);
  const x=n;
  const y=raw;
  return {raw,ideal:raw,period:raw/200.0,x,y,valid:n>=4&&n<=16};
 }
 if(slug==='concurrency-synchronization-deadlock'){
  const n=Number(input);
  const raw=Math.round(4 * n);
  const x=n;
  const y=raw;
  return {raw,ideal:raw,period:raw/200.0,x,y,valid:n>=2&&n<=14};
 }
 if(slug==='cryptographic-rsa-modular'){
  const b=Number(input);
  const raw=Math.round(1.5 * b);
  const x=b;
  const y=raw;
  return {raw,ideal:raw,period:raw/2000.0,x,y,valid:b>=64&&b<=4096};
 }
 if(slug==='lru-cache-replacement'){
  const c=Number(input);
  const raw=Math.round(6 * c);
  const x=c;
  const y=raw;
  return {raw,ideal:raw,period:raw/200.0,x,y,valid:c>=4&&c<=28};
 }
 if(slug==='a-star-pathfinding-heuristics'){
  const d=Number(input);
  const raw=Math.round(3 * d);
  const x=d;
  const y=raw;
  return {raw,ideal:raw,period:raw/200.0,x,y,valid:d>=10&&d<=70};
 }
 if(slug==='fast-fourier-transform'){
  const n=Number(input);
  const log2n=Math.round(Math.log2(n));
  const raw=Math.round(0.5 * n * log2n);
  const x=n * log2n;
  const y=raw;
  return {raw,ideal:raw,period:raw/2000.0,x,y,valid:n>=64&&n<=4096};
 }
 if(slug==='b-tree-disk-indexing'){
  const h=Number(input);
  const raw=Math.round(8 * h);
  const x=h;
  const y=raw;
  return {raw,ideal:raw,period:raw/200.0,x,y,valid:h>=2&&h<=8};
 }
 throw Error('Unknown CS experiment: '+slug);
}

function reading(slug,input,raw){
 const p=predict(slug,input);
 if(!Number.isFinite(raw)||raw<=0)throw Error('Invalid reading');
 let x=p.x,y=raw;
 if(slug==='search-algorithms-complexity'){
  x=Math.log2(Number(input));
  y=raw;
 }
 if(slug==='quadratic-sorting-algorithms'){
  x=Number(input)*(Number(input)-1);
  y=raw;
 }
 if(slug==='divide-conquer-sorting'){
  const n=Number(input);
  const log2n=Math.log2(n);
  x=n*(log2n - 1);
  y=raw;
 }
 if(slug==='stack-adt-recursion'){
  x=Number(input);
  y=raw;
 }
 if(slug==='queue-buffer-management'){
  x=Number(input);
  y=raw;
 }
 if(slug==='linked-list-architectures'){
  x=Number(input);
  y=raw;
 }
 if(slug==='binary-search-trees'){
  x=Math.log2(Number(input));
  y=raw;
 }
 if(slug==='binary-heaps-priority-queues'){
  const n=Number(input);
  x=n - Math.log2(n);
  y=raw;
 }
 if(slug==='hash-tables-collision-resolution'){
  const n=Number(input);
  const m_cap=1000;
  const alpha=n/m_cap;
  x=1/(1 - alpha);
  y=raw;
 }
 if(slug==='graph-traversal-shortest-paths'){
  x=Number(input);
  y=raw;
 }
 if(slug==='dynamic-programming-memoization'){
  x=Number(input);
  y=raw;
 }
 if(slug==='greedy-minimum-spanning-trees'){
  x=Number(input);
  y=raw;
 }
 if(slug==='string-matching-automata'){
  x=Number(input);
  y=raw;
 }
 if(slug==='network-flow-max-cut'){
  x=Number(input);
  y=raw;
 }
 if(slug==='trie-prefix-trees'){
  x=Number(input);
  y=raw;
 }
 if(slug==='huffman-coding-compression'){
  x=Number(input);
  y=raw;
 }
 if(slug==='computational-geometry-convex-hull'){
  x=Number(input);
  y=raw;
 }
 if(slug==='backtracking-n-queens-sat'){
  x=Number(input);
  y=raw;
 }
 if(slug==='fast-fourier-transform'){
  const n=Number(input);
  const log2n=Math.round(Math.log2(n));
  x=n * log2n;
  y=raw;
 }
 if(slug==='concurrency-synchronization-deadlock'){
  x=Number(input);
  y=raw;
 }
 if(slug==='cryptographic-rsa-modular'){
  x=Number(input);
  y=raw;
 }
 if(slug==='lru-cache-replacement'){
  x=Number(input);
  y=raw;
 }
 if(slug==='a-star-pathfinding-heuristics'){
  x=Number(input);
  y=raw;
 }
 if(slug==='b-tree-disk-indexing'){
  x=Number(input);
  y=raw;
 }
 return {input,raw,x,y};
}

function fit(rows){
 if(rows.length<3||new Set(rows.map(r=>r.x)).size<3)return null;
 const n=rows.length;
 const mx=rows.reduce((s,r)=>s+r.x,0)/n;
 const my=rows.reduce((s,r)=>s+r.y,0)/n;
 const sxx=rows.reduce((s,r)=>s+(r.x-mx)**2,0);
 const m=rows.reduce((s,r)=>s+(r.x-mx)*(r.y-my),0)/sxx;
 const b=my-m*mx;
 const sse=rows.reduce((s,r)=>s+(r.y-m*r.x-b)**2,0);
 const syy=rows.reduce((s,r)=>s+(r.y-my)**2,0);
 const variance=sse/(n-2);
 return {
  m,b,sse,
  rms:Math.sqrt(sse/n),
  slopeSE:Math.sqrt(variance/sxx),
  interceptSE:Math.sqrt(variance*(1/n+mx*mx/sxx)),
  r2:syy>0?1-sse/syy:1
 };
}

function estimate(slug,f){
 if(slug==='search-algorithms-complexity'){
  return {value:f.m,se:f.slopeSE,reference:1.0000};
 }
 if(slug==='quadratic-sorting-algorithms'){
  return {value:f.m,se:f.slopeSE,reference:0.5000};
 }
 if(slug==='divide-conquer-sorting'){
  return {value:f.m,se:f.slopeSE,reference:1.0000};
 }
 if(slug==='stack-adt-recursion'){
  return {value:f.m,se:f.slopeSE,reference:64.0000};
 }
 if(slug==='queue-buffer-management'){
  return {value:f.m,se:f.slopeSE,reference:64.0000};
 }
 if(slug==='linked-list-architectures'){
  return {value:f.m,se:f.slopeSE,reference:32.0000};
 }
 if(slug==='binary-search-trees'){
  return {value:f.m,se:f.slopeSE,reference:1.0000};
 }
 if(slug==='binary-heaps-priority-queues'){
  return {value:f.m,se:f.slopeSE,reference:2.0000};
 }
 if(slug==='hash-tables-collision-resolution'){
  return {value:f.m,se:f.slopeSE,reference:1.0000};
 }
 if(slug==='graph-traversal-shortest-paths'){
  return {value:f.m,se:f.slopeSE,reference:5.0000};
 }
 if(slug==='dynamic-programming-memoization'){
  return {value:f.m,se:f.slopeSE,reference:100.0000};
 }
 if(slug==='greedy-minimum-spanning-trees'){
  return {value:f.m,se:f.slopeSE,reference:8.0000};
 }
 if(slug==='string-matching-automata'){
  return {value:f.m,se:f.slopeSE,reference:1.0000};
 }
 if(slug==='network-flow-max-cut'){
  return {value:f.m,se:f.slopeSE,reference:10.0000};
 }
 if(slug==='trie-prefix-trees'){
  return {value:f.m,se:f.slopeSE,reference:1.0000};
 }
 if(slug==='huffman-coding-compression'){
  return {value:f.m,se:f.slopeSE,reference:2.5000};
 }
 if(slug==='computational-geometry-convex-hull'){
  return {value:f.m,se:f.slopeSE,reference:2.0000};
 }
 if(slug==='backtracking-n-queens-sat'){
  return {value:f.m,se:f.slopeSE,reference:4.0000};
 }
 if(slug==='fast-fourier-transform'){
  return {value:f.m,se:f.slopeSE,reference:0.5000};
 }
 if(slug==='concurrency-synchronization-deadlock'){
  return {value:f.m,se:f.slopeSE,reference:4.0000};
 }
 if(slug==='cryptographic-rsa-modular'){
  return {value:f.m,se:f.slopeSE,reference:1.5000};
 }
 if(slug==='lru-cache-replacement'){
  return {value:f.m,se:f.slopeSE,reference:6.0000};
 }
 if(slug==='a-star-pathfinding-heuristics'){
  return {value:f.m,se:f.slopeSE,reference:3.0000};
 }
 if(slug==='b-tree-disk-indexing'){
  return {value:f.m,se:f.slopeSE,reference:8.0000};
 }
 throw Error('Unknown CS experiment: '+slug);
}

const api={predict,reading,fit,estimate,round};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
else root.CSModels=api;
})(typeof window==='undefined'?{}:window);
