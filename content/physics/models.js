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
  if(slug==='solidification-cooling'){const Lf=79500,R_loss=270.0,m_kg=input/1000,ideal=(m_kg*Lf)/R_loss,raw=round(ideal,2),x=m_kg,y=raw*R_loss;return{raw,ideal,x,y,valid:input>=10.0&&input<=45.0};}
  if(slug==='latent-heat-vaporization'){const cw=4186.0,Csys=866.08,Ts=100.0,T0=15.0,Lv=2260000.0,m_kg=input/1000,ideal=(m_kg*Lv+m_kg*cw*Ts+Csys*T0)/(Csys+m_kg*cw),raw=round(ideal,2),x=m_kg,y=Csys*(raw-T0)-m_kg*cw*(Ts-raw);return{raw,ideal,x,y,valid:input>=2.0&&input<=12.0};}
  if(slug==='latent-heat-fusion'){const cw=4186.0,Csys=866.08,T0=30.0,Lf=334000.0,m_kg=input/1000,ideal=(Csys*T0-m_kg*Lf)/(Csys+m_kg*cw),raw=round(ideal,2),x=m_kg,y=Csys*(T0-raw)-m_kg*cw*raw;return{raw,ideal,x,y,valid:input>=10.0&&input<=45.0};}
  if(slug==='thermal-expansion'){const L0=1.000,alpha=16.80e-6,ideal=L0*alpha*input*1000.0,raw=round(ideal,3),x=L0*input,y=raw/1000.0;return{raw,ideal,x,y,valid:input>=10.0&&input<=85.0};}
  if(slug==='mechanical-equivalent-heat'){const r=0.050,M=3.00,g=9.80665,W1=2*Math.PI*r*M*g,Csys_cal=118.48,J_ref=4.1860,T0=20.00,W=input*W1,Q_cal=W/J_ref,dT=Q_cal/Csys_cal,ideal=T0+dT,raw=round(ideal,2),dT_obs=raw-T0,x=Csys_cal*dT_obs,y=W;return{raw,ideal,x,y,valid:input>=100&&input<=1200};}
  if(slug==='boyles-law'){const k_ref=3.03975,V_m3=input*1e-6,P_Pa=k_ref/V_m3,P_kPa=P_Pa/1000.0,raw=round(P_kPa,2),x=1.0/V_m3,y=raw*1000.0;return{raw,ideal:P_kPa,x,y,valid:input>=15.0&&input<=50.0};}
  if(slug==='charles-law-volume'){const V0_cm3=100.00,beta_ref=1.0/273.15,ideal=V0_cm3*(1.0+beta_ref*input),raw=round(ideal,2),x=input,y=raw*1e-6;return{raw,ideal,x,y,valid:input>=0.0&&input<=95.0};}
  if(slug==='charles-law-pressure'){const P0_kPa=101.325,alpha_ref=1.0/273.15,ideal=P0_kPa*(1.0+alpha_ref*input),raw=round(ideal,2),x=input,y=raw*1000.0;return{raw,ideal:P0_kPa,x,y,valid:input>=0.0&&input<=95.0};}
  if(slug==='vapor-pressure'){const R_gas=8.314462618,dH_ref=41920.0,T0_K=351.52,P0_Pa=101325.0,T_K=input+273.15,inv_T=1.0/T_K,ideal_Pa=P0_Pa*Math.exp(-dH_ref/R_gas*(inv_T-1.0/T0_K)),raw=round(ideal_Pa/1000.0,2),x=inv_T,y=Math.log(raw*1000.0);return{raw,ideal:ideal_Pa/1000.0,x,y,valid:input>=15.0&&input<=95.0};}
  if(slug==='air-humidity'){const gamma_ref=66.875,raw=round(gamma_ref*input,1);return{raw,ideal:gamma_ref*input,x:input,y:raw,valid:input>=1.0&&input<=15.0};}
  if(slug==='loaded-spring'){const k_ref=20.00,m_eff=0.0200,m_kg=input/1000.0,M=m_kg+m_eff,T=2*PI*Math.sqrt(M/k_ref),raw=round(20*T,2);return{raw,ideal:20*T,period:T,x:m_kg,y:(raw/20)**2,valid:input>=80.0&&input<=350.0};}
  if(slug==='pendulum-coincidence'){const g_ref=9.80665,T0=2.0000,L_m=input/100.0,T_ideal=2*PI*Math.sqrt(L_m/g_ref),tc_ideal=(T0*T_ideal)/(T0-T_ideal),raw=round(tc_ideal,2),T_meas=(T0*raw)/(raw+T0);return{raw,ideal:tc_ideal,period:T_meas,x:L_m,y:T_meas**2,valid:input>=65.0&&input<=95.0};}
  if(slug==='torsion-pendulum'){const eta_ref=7.850e10,I_disc=0.01000,r_wire=0.000600,C_const=(8*PI*I_disc)/(r_wire**4),S_ideal=C_const/eta_ref,L_m=input/100.0,T_ideal=Math.sqrt(S_ideal*L_m),raw=round(20*T_ideal,2),T_meas=raw/20.0;return{raw,ideal:20*T_ideal,period:T_meas,x:L_m,y:T_meas**2,valid:input>=40.0&&input<=90.0};}
  if(slug==='resonance-air-column'){const v_ref=343.20,r_tube=0.0160,c_ref=0.6133*r_tube,inv_f=1.0/input,L1_m=(v_ref/4.0)*inv_f-c_ref,raw=round(L1_m*100.0,2),x=inv_f,y=raw/100.0;return{raw,ideal:L1_m*100.0,period:1.0/input,x,y,valid:input>=200.0&&input<=600.0};}
  if(slug==='modes-air-column'){const v_ref=343.20,r_tube=0.0200,c_both=2.0*0.6133*r_tube,inv_f=1.0/input,L_m=(v_ref/2.0)*inv_f-c_both,raw=round(L_m*100.0,2),x=inv_f,y=raw/100.0;return{raw,ideal:L_m*100.0,period:1.0/input,x,y,valid:input>=200.0&&input<=600.0};}
  if(slug==='vibration-strings-sonometer'){const v_ref=138.16,inv_f=1.0/input,L_m=(v_ref/2.0)*inv_f,raw=round(L_m*100.0,2),x=inv_f,y=raw/100.0;return{raw,ideal:L_m*100.0,period:1.0/input,x,y,valid:input>=100.0&&input<=500.0};}
 throw Error('Unknown experiment');
}
function reading(slug,input,raw,angle=3){const p=predict(slug,input,angle);if(!Number.isFinite(raw)||raw<=0)throw Error('Invalid reading');let y,x=p.x;if(['simple-pendulum','bifilar-suspension','conical-pendulum','loaded-spring','torsion-pendulum'].includes(slug))y=(raw/20)**2;else if(slug==='young-modulus')y=raw/1000;else if(slug==='stokes-viscosity')y=.1/raw;else if(slug==='ohms-law')y=raw/1000;else if(slug==='metre-bridge')y=(100-raw)/raw;else if(slug==='rc-charging')y=Math.log(5/(5-raw));else if(slug==='glass-slab')y=raw/1000;else if(slug==='diffraction-grating')y=Math.sin(raw*PI/180);else if(slug==='newtons-rings')y=(raw/1000)**2;else if(slug==='hookes-law'||slug==='density-measurement'||slug==='vernier-micrometer')y=raw/1000;else if(slug==='friction-laws')y=raw;else if(slug==='principle-of-moments')y=raw/100;else if(slug==='force-table')y=raw/1000;else if(slug==='equilibrium-forces')y=raw;else if(slug==='free-fall')y=input;else if(slug==='newtons-second-law')y=raw;else if(slug==='flywheel-inertia')y=raw;else if(slug==='specific-heat-capacity'){x=(input/1000)*(100.0-raw);y=920.92*(raw-20.0);}else if(slug==='newtons-cooling'){const theta=raw-20.0;y=Math.log(60.0/theta);}else if(slug==='solidification-cooling'){y=raw*270.0;}else if(slug==='latent-heat-vaporization'){const cw=4186.0,Csys=866.08,Ts=100.0,T0=15.0,m_kg=input/1000;x=m_kg;y=Csys*(raw-T0)-m_kg*cw*(Ts-raw);}else if(slug==='latent-heat-fusion'){const cw=4186.0,Csys=866.08,T0=30.0,m_kg=input/1000;x=m_kg;y=Csys*(T0-raw)-m_kg*cw*raw;}else if(slug==='thermal-expansion'){const L0=1.000;x=L0*input;y=raw/1000.0;}else if(slug==='mechanical-equivalent-heat'){const r=0.050,M=3.00,g=9.80665,W1=2*Math.PI*r*M*g,Csys_cal=118.48,T0=20.00;x=Csys_cal*(raw-T0);y=input*W1;}else if(slug==='boyles-law'){const V_m3=input*1e-6;x=1.0/V_m3;y=raw*1000.0;}else if(slug==='charles-law-volume'){x=input;y=raw*1e-6;}else if(slug==='charles-law-pressure'){x=input;y=raw*1000.0;}else if(slug==='vapor-pressure'){x=1.0/(input+273.15);y=Math.log(raw*1000.0);}else if(slug==='air-humidity'){x=input;y=raw;}else if(slug==='pendulum-coincidence'){const T_meas=(2.0000*raw)/(raw+2.0000);x=input/100.0;y=T_meas**2;}else if(slug==='resonance-air-column'){x=1.0/input;y=raw/100.0;}else if(slug==='modes-air-column'){x=1.0/input;y=raw/100.0;}else if(slug==='vibration-strings-sonometer'){x=1.0/input;y=raw/100.0;}else if(slug==='ballistic-pendulum')y=Math.sqrt(2*G*(raw/100));else y=100/raw;return{input,raw,x,y,angle};}
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
  if(slug==='solidification-cooling')return{value:f.m,se:f.slopeSE,reference:79500.0};
  if(slug==='latent-heat-vaporization')return{value:f.m,se:f.slopeSE,reference:2260000.0};
  if(slug==='latent-heat-fusion')return{value:f.m,se:f.slopeSE,reference:334000.0};
  if(slug==='thermal-expansion')return{value:f.m,se:f.slopeSE,reference:16.80e-6};
  if(slug==='mechanical-equivalent-heat')return{value:f.m,se:f.slopeSE,reference:4.1860};
  if(slug==='boyles-law')return{value:f.m,se:f.slopeSE,reference:3.03975};
  if(slug==='charles-law-volume')return{value:f.m/1e-4,se:f.slopeSE/1e-4,reference:1.0/273.15};
  if(slug==='charles-law-pressure')return{value:f.m/101325.0,se:f.slopeSE/101325.0,reference:1.0/273.15};
  if(slug==='vapor-pressure')return{value:-f.m*8.314462618,se:f.slopeSE*8.314462618,reference:41920.0};
  if(slug==='air-humidity')return{value:f.m/101325.0,se:f.slopeSE/101325.0,reference:6.60e-4};
  if(slug==='loaded-spring')return{value:(4*PI**2)/f.m,se:(4*PI**2)*f.slopeSE/(f.m**2),reference:20.00};
  if(slug==='pendulum-coincidence')return{value:(4*PI**2)/f.m,se:(4*PI**2)*f.slopeSE/(f.m**2),reference:9.80665};
  if(slug==='torsion-pendulum'){const I_disc=0.01000,r_wire=0.000600,C_const=(8*PI*I_disc)/(r_wire**4);return{value:C_const/f.m,se:C_const*f.slopeSE/(f.m**2),reference:7.850e10};}
  if(slug==='resonance-air-column')return{value:4.0*f.m,se:4.0*f.slopeSE,reference:343.20};
  if(slug==='modes-air-column')return{value:2.0*f.m,se:2.0*f.slopeSE,reference:343.20};
  if(slug==='vibration-strings-sonometer')return{value:2.0*f.m,se:2.0*f.slopeSE,reference:138.16};
 const C=slug==='simple-pendulum'?4*PI**2:slug==='bifilar-suspension'?.5*G*.1**2/(4*PI**2):slug==='young-modulus'?2/(PI*.0005**2/4):2*(2500-1260)*G/9;
 if(slug==='convex-lens')return{value:1/f.b,se:f.interceptSE/f.b**2,reference:.15};
 if(slug==='bifilar-suspension')return{value:C*f.m,se:C*f.slopeSE,reference:.5*.5**2/12};
 return{value:C/f.m,se:C*f.slopeSE/f.m**2,reference:slug==='simple-pendulum'?G:slug==='young-modulus'?200e9:1.2};}
const api={predict,reading,fit,estimate,round};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.PhysicsModels=api;
})(typeof window==='undefined'?{}:window);
