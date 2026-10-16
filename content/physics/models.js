(function(root){
'use strict';
const G=9.80665,PI=Math.PI;
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;
function predict(slug,input,angle=3){
 if(slug==='simple-pendulum'){const a=angle*PI/180,T=2*PI*Math.sqrt(input/G)*(1+a*a/16+11*a**4/3072);return{raw:round(20*T,2),ideal:20*T,period:T,x:input,y:(round(20*T,2)/20)**2,valid:angle<=5};}
 if(slug==='bifilar-suspension'){const I=.5*.5**2/12,T=2*PI*Math.sqrt(I*input/(.5*G*.1**2));return{raw:round(20*T,2),ideal:20*T,period:T,x:input,y:(round(20*T,2)/20)**2,valid:angle<=5};}
 if(slug==='young-modulus'){const extension=input*2/(PI*(.0005**2)/4*200e9),raw=round(extension*1e3,3);return{raw,ideal:extension*1e3,x:input,y:raw/1e3,valid:true};}
 if(slug==='stokes-viscosity'){const r=input/1e3,v=2*(2500-1260)*G*r*r/(9*1.2),time=.1/v,raw=round(time,2);return{raw,ideal:time,velocity:v,reynolds:1260*v*2*r/1.2,x:r*r,y:.1/raw,valid:true};}
 if(slug==='convex-lens'){const u=input/100,v=1/(1/.15-1/u),raw=round(v*100,1);return{raw,ideal:v*100,x:1/u,y:1/(raw/100),magnification:v/u,valid:u>.15};}
 if(slug==='ohms-law'){const raw=round(input/100*1000,2);return{raw,ideal:input/100*1000,x:input,y:raw/1000,valid:true};}
 if(slug==='metre-bridge'){const ideal=100*5/(5+input),raw=round(ideal,1);return{raw,ideal,x:input,y:(100-raw)/raw,valid:true};}
 if(slug==='rc-charging'){const ideal=5*(1-Math.exp(-input)),raw=round(ideal,3);return{raw,ideal,x:input,y:Math.log(5/(5-raw)),valid:true};}
 if(slug==='glass-slab'){const ideal=input/1.5,raw=round(ideal,2);return{raw,ideal,x:input/1000,y:raw/1000,valid:true};}
 if(slug==='diffraction-grating'){const ideal=Math.asin(input*550e-9/(1e-3/300))*180/PI,raw=round(ideal,2);return{raw,ideal,x:input,y:Math.sin(raw*PI/180),valid:Number.isInteger(input)&&input>=1&&input<=5};}
 throw Error('Unknown experiment');
}
function reading(slug,input,raw,angle=3){const p=predict(slug,input,angle);if(!Number.isFinite(raw)||raw<=0)throw Error('Invalid reading');let y;if(['simple-pendulum','bifilar-suspension'].includes(slug))y=(raw/20)**2;else if(slug==='young-modulus')y=raw/1000;else if(slug==='stokes-viscosity')y=.1/raw;else if(slug==='ohms-law')y=raw/1000;else if(slug==='metre-bridge')y=(100-raw)/raw;else if(slug==='rc-charging')y=Math.log(5/(5-raw));else if(slug==='glass-slab')y=raw/1000;else if(slug==='diffraction-grating')y=Math.sin(raw*PI/180);else y=100/raw;return{input,raw,x:p.x,y,angle};}
function fit(rows){if(rows.length<3||new Set(rows.map(r=>r.x)).size<3)return null;const n=rows.length,mx=rows.reduce((s,r)=>s+r.x,0)/n,my=rows.reduce((s,r)=>s+r.y,0)/n,sxx=rows.reduce((s,r)=>s+(r.x-mx)**2,0),m=rows.reduce((s,r)=>s+(r.x-mx)*(r.y-my),0)/sxx,b=my-m*mx,sse=rows.reduce((s,r)=>s+(r.y-m*r.x-b)**2,0),syy=rows.reduce((s,r)=>s+(r.y-my)**2,0),variance=sse/(n-2);return{m,b,sse,rms:Math.sqrt(sse/n),slopeSE:Math.sqrt(variance/sxx),interceptSE:Math.sqrt(variance*(1/n+mx*mx/sxx)),r2:syy>0?1-sse/syy:1};}
function estimate(slug,f){
 if(slug==='ohms-law')return{value:1/f.m,se:f.slopeSE/f.m**2,reference:100};
 if(slug==='metre-bridge')return{value:1/f.m,se:f.slopeSE/f.m**2,reference:5};
 if(slug==='rc-charging')return{value:1/f.m,se:f.slopeSE/f.m**2,reference:1};
 if(slug==='glass-slab')return{value:1/f.m,se:f.slopeSE/f.m**2,reference:1.5};
 if(slug==='diffraction-grating')return{value:f.m*(1e-3/300),se:f.slopeSE*(1e-3/300),reference:550e-9};
 const C=slug==='simple-pendulum'?4*PI**2:slug==='bifilar-suspension'?.5*G*.1**2/(4*PI**2):slug==='young-modulus'?2/(PI*.0005**2/4):2*(2500-1260)*G/9;
 if(slug==='convex-lens')return{value:1/f.b,se:f.interceptSE/f.b**2,reference:.15};
 if(slug==='bifilar-suspension')return{value:C*f.m,se:C*f.slopeSE,reference:.5*.5**2/12};
 return{value:C/f.m,se:C*f.slopeSE/f.m**2,reference:slug==='simple-pendulum'?G:slug==='young-modulus'?200e9:1.2};}
const api={predict,reading,fit,estimate,round};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.PhysicsModels=api;
})(typeof window==='undefined'?{}:window);
