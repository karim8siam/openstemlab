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
 throw Error('Unknown CS experiment: '+slug);
}

const api={predict,reading,fit,estimate,round};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
else root.CSModels=api;
})(typeof window==='undefined'?{}:window);
