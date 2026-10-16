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
 if(slug==='newtons-rings'){const LAMBDA=589.3e-9,R=1.000,idealD=Math.sqrt(4*input*LAMBDA*R),ideal=idealD*1000,raw=round(ideal,2),d_m=raw/1000;return{raw,ideal,x:input,y:d_m*d_m,valid:Number.isInteger(input)&&input>=1&&input<=24};}
 if(slug==='hookes-law'){const raw=round(input/25.0*1000,1);return{raw,ideal:input/25.0*1000,x:input,y:raw/1000,valid:input>=0.2&&input<=3.0};}
 if(slug==='density-measurement'){const raw=round(input*8.96,2);return{raw,ideal:input*8.96,x:input*1e-6,y:raw/1000,valid:input>=5.0&&input<=60.0};}
 if(slug==='vernier-micrometer'){const raw=round(input*PI,2);return{raw,ideal:input*PI,x:input/1000,y:raw/1000,valid:input>=10.0&&input<=50.0};}
 if(slug==='friction-laws'){const raw=round(input*0.35,2);return{raw,ideal:input*0.35,x:input,y:raw,valid:input>=1.0&&input<=14.0};}
 if(slug==='principle-of-moments'){const m_kg=input/1000,ideal=(0.018/m_kg)*100,raw=round(ideal,1);return{raw,ideal,x:1/m_kg,y:raw/100,valid:input>=50.0&&input<=200.0};}
 if(slug==='force-table'){const rad=input*PI/180,x=Math.cos(rad),ideal=2*150.0*x,raw=round(ideal,1);return{raw,ideal,x,y:raw/1000,valid:input>=15.0&&input<=75.0};}
 if(slug==='equilibrium-forces'){const d_AB=0.80,x_A=0.10,W_bar=2.00,W_load=5.00,ideal=(W_bar*0.40/d_AB)+(W_load/d_AB)*(input-x_A),raw=round(ideal,2);return{raw,ideal,x:input,y:raw,valid:input>=0.15&&input<=0.85};}
  if(slug==='free-fall'){const ideal=Math.sqrt(2*input/G),raw=round(ideal,4);return{raw,ideal,x:raw*raw,y:input,valid:input>=0.15&&input<=1.25};}
  if(slug==='newtons-second-law'){const ideal=input/1.200,raw=round(ideal,3);return{raw,ideal,x:input,y:raw,valid:input>=0.20&&input<=2.00};}
  if(slug==='ballistic-pendulum'){const p0=0.250,M=(input+50.0)/1000,V=p0/M,h=(V*V/(2*G))*100,raw=round(h,2),y=Math.sqrt(2*G*(raw/100));return{raw,ideal:h,x:1/M,y,valid:input>=100.0&&input<=500.0};}
  if(slug==='conical-pendulum'){const rad=input*PI/180,h=1.000*Math.cos(rad),T=2*PI*Math.sqrt(h/G),raw=round(20*T,2);return{raw,ideal:20*T,period:T,x:h,y:(raw/20)**2,valid:input>=15.0&&input<=70.0};}
  if(slug==='flywheel-inertia'){const ideal=input/0.050,raw=round(ideal,3);return{raw,ideal,x:input,y:raw,valid:input>=0.015&&input<=0.200};}
  if(slug==='specific-heat-capacity'){const m_kg=input/1000,Csys=920.92,Ts=100.0,T0=20.0,cs=385.0,ideal=(m_kg*cs*Ts+Csys*T0)/(m_kg*cs+Csys),raw=round(ideal,2),x=m_kg*(Ts-raw),y=Csys*(raw-T0);return{raw,ideal,x,y,valid:input>=40.0&&input<=240.0};}
  if(slug==='newtons-cooling'){const T0=20.0,theta0=60.0,k=0.0960,ideal=T0+theta0*Math.exp(-k*input),raw=round(ideal,2),theta=raw-T0,x=input,y=Math.log(theta0/theta);return{raw,ideal,x,y,valid:input>=1.0&&input<=15.0};}
 throw Error('Unknown experiment');
}
function reading(slug,input,raw,angle=3){const p=predict(slug,input,angle);if(!Number.isFinite(raw)||raw<=0)throw Error('Invalid reading');let y,x=p.x;if(['simple-pendulum','bifilar-suspension','conical-pendulum'].includes(slug))y=(raw/20)**2;else if(slug==='young-modulus')y=raw/1000;else if(slug==='stokes-viscosity')y=.1/raw;else if(slug==='ohms-law')y=raw/1000;else if(slug==='metre-bridge')y=(100-raw)/raw;else if(slug==='rc-charging')y=Math.log(5/(5-raw));else if(slug==='glass-slab')y=raw/1000;else if(slug==='diffraction-grating')y=Math.sin(raw*PI/180);else if(slug==='newtons-rings')y=(raw/1000)**2;else if(slug==='hookes-law'||slug==='density-measurement'||slug==='vernier-micrometer')y=raw/1000;else if(slug==='friction-laws')y=raw;else if(slug==='principle-of-moments')y=raw/100;else if(slug==='force-table')y=raw/1000;else if(slug==='equilibrium-forces')y=raw;else if(slug==='free-fall')y=input;else if(slug==='newtons-second-law')y=raw;else if(slug==='flywheel-inertia')y=raw;else if(slug==='specific-heat-capacity'){x=(input/1000)*(100.0-raw);y=920.92*(raw-20.0);}else if(slug==='newtons-cooling'){const theta=raw-20.0;y=Math.log(60.0/theta);}else if(slug==='ballistic-pendulum')y=Math.sqrt(2*G*(raw/100));else y=100/raw;return{input,raw,x,y,angle};}
function fit(rows){if(rows.length<3||new Set(rows.map(r=>r.x)).size<3)return null;const n=rows.length,mx=rows.reduce((s,r)=>s+r.x,0)/n,my=rows.reduce((s,r)=>s+r.y,0)/n,sxx=rows.reduce((s,r)=>s+(r.x-mx)**2,0),m=rows.reduce((s,r)=>s+(r.x-mx)*(r.y-my),0)/sxx,b=my-m*mx,sse=rows.reduce((s,r)=>s+(r.y-m*r.x-b)**2,0),syy=rows.reduce((s,r)=>s+(r.y-my)**2,0),variance=sse/(n-2);return{m,b,sse,rms:Math.sqrt(sse/n),slopeSE:Math.sqrt(variance/sxx),interceptSE:Math.sqrt(variance*(1/n+mx*mx/sxx)),r2:syy>0?1-sse/syy:1};}
function estimate(slug,f){
 if(slug==='ohms-law')return{value:1/f.m,se:f.slopeSE/f.m**2,reference:100};
 if(slug==='metre-bridge')return{value:1/f.m,se:f.slopeSE/f.m**2,reference:5};
 if(slug==='rc-charging')return{value:1/f.m,se:f.slopeSE/f.m**2,reference:1};
 if(slug==='glass-slab')return{value:1/f.m,se:f.slopeSE/f.m**2,reference:1.5};
 if(slug==='diffraction-grating')return{value:f.m*(1e-3/300),se:f.slopeSE*(1e-3/300),reference:550e-9};
 if(slug==='newtons-rings'){const LAMBDA=589.3e-9;return{value:f.m/(4*LAMBDA),se:f.slopeSE/(4*LAMBDA),reference:1.000};}
 if(slug==='hookes-law')return{value:1/f.m,se:f.slopeSE/f.m**2,reference:25.0};
 if(slug==='density-measurement')return{value:f.m,se:f.slopeSE,reference:8960.0};
 if(slug==='vernier-micrometer')return{value:f.m,se:f.slopeSE,reference:PI};
 if(slug==='friction-laws')return{value:f.m,se:f.slopeSE,reference:0.35};
 if(slug==='principle-of-moments')return{value:f.m/0.150,se:f.slopeSE/0.150,reference:0.120};
 if(slug==='force-table')return{value:f.m/2.0,se:f.slopeSE/2.0,reference:0.150};
 if(slug==='equilibrium-forces')return{value:f.m*0.80,se:f.slopeSE*0.80,reference:5.00};
 if(slug==='free-fall')return{value:2.0*f.m,se:2.0*f.slopeSE,reference:G};
 if(slug==='newtons-second-law')return{value:1.0/f.m,se:f.slopeSE/(f.m**2),reference:1.200};
 if(slug==='ballistic-pendulum')return{value:f.m/0.050,se:f.slopeSE/0.050,reference:5.000};
  if(slug==='conical-pendulum')return{value:(4*PI**2)/f.m,se:(4*PI**2)*f.slopeSE/(f.m**2),reference:G};
  if(slug==='flywheel-inertia')return{value:1.0/f.m,se:f.slopeSE/(f.m**2),reference:0.050};
  if(slug==='specific-heat-capacity')return{value:f.m,se:f.slopeSE,reference:385.0};
  if(slug==='newtons-cooling')return{value:f.m,se:f.slopeSE,reference:0.0960};
 const C=slug==='simple-pendulum'?4*PI**2:slug==='bifilar-suspension'?.5*G*.1**2/(4*PI**2):slug==='young-modulus'?2/(PI*.0005**2/4):2*(2500-1260)*G/9;
 if(slug==='convex-lens')return{value:1/f.b,se:f.interceptSE/f.b**2,reference:.15};
 if(slug==='bifilar-suspension')return{value:C*f.m,se:C*f.slopeSE,reference:.5*.5**2/12};
 return{value:C/f.m,se:C*f.slopeSE/f.m**2,reference:slug==='simple-pendulum'?G:slug==='young-modulus'?200e9:1.2};}
const api={predict,reading,fit,estimate,round};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.PhysicsModels=api;
})(typeof window==='undefined'?{}:window);
