(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

function predict(slug,input){
 if(slug==='density-mass-volume-precision'){
  const v=Number(input);
  const rho=0.9982;
  const raw=round(rho*v,4);
  const x=v;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:v>=5.0&&v<=35.0};
 }
 throw Error('Unknown Chemistry experiment predict: '+slug);
}

function reading(slug,input,raw){
 let x=Number(input),y=Number(raw);
 if(slug==='density-mass-volume-precision'){
  x=Number(input);
  y=Number(raw);
 }
 return {input:Number(input),raw:Number(raw),x,y};
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
 if(slug==='density-mass-volume-precision'){
  return {value:f.m,se:f.slopeSE,reference:0.9982};
 }
 throw Error('Unknown Chemistry experiment estimate: '+slug);
}

const api={predict,reading,fit,estimate,round};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
else root.ChemistryModels=api;
})(typeof window==='undefined'?{}:window);
