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
 if(slug==='hydrate-stoichiometric-composition'){
  const m_hydrate=Number(input);
  const factor=(5.0*18.0154)/(159.609 + 5.0*18.0154);
  const raw=round(m_hydrate*factor,4);
  const x=round(m_hydrate - raw,4);
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:m_hydrate>=1.5&&m_hydrate<=7.5};
 }
 if(slug==='limiting-reactant-precipitation'){
  const v=Number(input);
  const C=0.1000;
  const M_BaSO4=233.390;
  const raw=round((C * v / 1000.0) * M_BaSO4, 4);
  const x=v;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:v>=4.0&&v<=24.0};
 }
 if(slug==='molar-volume-ideal-gas'){
  const m_mg=Number(input);
  const M_Mg=24.305;
  const Vm_ref=22.414;
  const raw=round((m_mg / 1000.0 / M_Mg) * Vm_ref * 1000.0, 3);
  const x=m_mg;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:m_mg>=10.0&&m_mg<=35.0};
 }
 if(slug==='volatile-liquid-molar-mass'){
  const v=Number(input);
  const M_ref=84.161;
  const R=82.0574;
  const T=373.15;
  const P=1.000;
  const rho_ideal=(P * M_ref) / (R * T);
  const raw=round(rho_ideal * v, 4);
  const x=v;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:v>=125.0&&v<=375.0};
 }
 if(slug==='chemical-reactions-copper-cycle'){
  const m_init=Number(input);
  const raw=round(m_init * 1.0000, 4);
  const x=m_init;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:m_init>=0.20&&m_init<=0.70};
 }
 if(slug==='empirical-formula-magnesium-oxide'){
  const m_mg=Number(input);
  const ratio=15.9994 / 24.305;
  const raw=round(m_mg * ratio, 4);
  const x=m_mg;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:m_mg>=0.20&&m_mg<=0.70};
 }
 if(slug==='liquid-viscosity-poiseuille'){
  const h=Number(input);
  const const_geom=6.006263e-5;
  const eta_ref=0.0010020;
  const raw=round((const_geom / eta_ref) * h, 3);
  const x=h;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:h>=10.0&&h<=35.0};
 }
 if(slug==='surface-tension-stalagmometry'){
  const n_drops=Number(input);
  const m_single=0.10040;
  const raw=round(n_drops * m_single, 4);
  const x=n_drops;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:n_drops>=10&&n_drops<=60};
 }
 if(slug==='colligative-freezing-point-depression'){
  const w=Number(input);
  const Kf=20.00;
  const w_solv=0.0250;
  const M_true=154.21;
  const raw=round((Kf * w) / (M_true * w_solv), 3);
  const x=w;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:w>=0.20&&w<=1.20};
 }
 if(slug==='solution-calorimetry-neutralization'){
  const n=Number(input);
  const C_eff=0.44365;
  const dH=55.84;
  const raw=round((dH * n) / C_eff, 3);
  const x=n;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:n>=0.020&&n<=0.070};
 }
 if(slug==='hess-law-magnesium-calorimetry'){
  const m=Number(input);
  const M_Mg=24.305;
  const C_eff=0.44365;
  const dH1=462.00;
  const raw=round((dH1 * m) / (M_Mg * C_eff), 3);
  const x=m;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:m>=0.100&&m<=0.350};
 }
 if(slug==='combustion-bomb-calorimetry-benzoic'){
  const m=Number(input);
  const M_benzoic=122.12;
  const C_cal=10.500;
  const dU=3227.0;
  const raw=round((dU * m) / (M_benzoic * C_cal), 3);
  const x=m;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:m>=0.600&&m<=1.600};
 }
 if(slug==='heat-solution-crystallization-calorimetry'){
  const m=Number(input);
  const M_KNO3=101.103;
  const C_eff=0.44590;
  const dH=34.890;
  const raw=round((dH * m) / (M_KNO3 * C_eff), 3);
  const x=m;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:m>=2.000&&m<=7.000};
 }
 if(slug==='vapor-pressure-liquid-clausius-clapeyron'){
  const t=Number(input);
  const T=t + 273.15;
  const R=8.31446;
  const dH=38560.0;
  const Tb=351.52;
  const Pb=101.325;
  const ln_P=Math.log(Pb) - (dH / R) * (1.0 / T - 1.0 / Tb);
  const raw=round(Math.exp(ln_P), 2);
  const x=round(1000.0 / T, 4);
  const y=round(Math.log(raw), 4);
  return {raw,ideal:raw,period:1.0,x,y,valid:t>=30.0&&t<=78.0};
 }
 throw Error('Unknown Chemistry experiment predict: '+slug);
}

function reading(slug,input,raw){
 let x=Number(input),y=Number(raw);
 if(slug==='density-mass-volume-precision'){
  x=Number(input);
  y=Number(raw);
 }
 if(slug==='hydrate-stoichiometric-composition'){
  const m_hydrate=Number(input);
  const r=Number(raw);
  x=round(m_hydrate - r,4);
  y=r;
 }
 if(slug==='limiting-reactant-precipitation'){
  x=Number(input);
  y=Number(raw);
 }
 if(slug==='molar-volume-ideal-gas'){
  x=Number(input);
  y=Number(raw);
 }
 if(slug==='volatile-liquid-molar-mass'){
  x=Number(input);
  y=Number(raw);
 }
 if(slug==='chemical-reactions-copper-cycle'){
  x=Number(input);
  y=Number(raw);
 }
 if(slug==='empirical-formula-magnesium-oxide'){
  x=Number(input);
  y=Number(raw);
 }
 if(slug==='liquid-viscosity-poiseuille'){
  x=Number(input);
  y=Number(raw);
 }
 if(slug==='surface-tension-stalagmometry'){
  x=Number(input);
  y=Number(raw);
 }
 if(slug==='colligative-freezing-point-depression'){
  x=Number(input);
  y=Number(raw);
 }
 if(slug==='solution-calorimetry-neutralization'){
  x=Number(input);
  y=Number(raw);
 }
 if(slug==='hess-law-magnesium-calorimetry'){
  x=Number(input);
  y=Number(raw);
 }
 if(slug==='combustion-bomb-calorimetry-benzoic'){
  x=Number(input);
  y=Number(raw);
 }
 if(slug==='heat-solution-crystallization-calorimetry'){
  x=Number(input);
  y=Number(raw);
 }
 if(slug==='vapor-pressure-liquid-clausius-clapeyron'){
  const t=Number(input);
  const P=Number(raw);
  const T=t + 273.15;
  x=round(1000.0 / T, 4);
  y=round(Math.log(P), 4);
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
 if(slug==='hydrate-stoichiometric-composition'){
  const x_coeff=f.m * (159.609 / 18.0154);
  const se=f.slopeSE * (159.609 / 18.0154);
  return {value:x_coeff,se:se,reference:5.0000};
 }
 if(slug==='limiting-reactant-precipitation'){
  const M_est=f.m * 10000.0;
  const se=f.slopeSE * 10000.0;
  return {value:M_est,se:se,reference:233.390};
 }
 if(slug==='molar-volume-ideal-gas'){
  const Vm_est=f.m * 24.305;
  const se=f.slopeSE * 24.305;
  return {value:Vm_est,se:se,reference:22.414};
 }
 if(slug==='volatile-liquid-molar-mass'){
  const R=82.0574;
  const T=373.15;
  const P=1.000;
  const M_est=(f.m * R * T) / P;
  const se=(f.slopeSE * R * T) / P;
  return {value:M_est,se:se,reference:84.161};
 }
 if(slug==='chemical-reactions-copper-cycle'){
  return {value:f.m,se:f.slopeSE,reference:1.0000};
 }
 if(slug==='empirical-formula-magnesium-oxide'){
  const conv=24.305 / 15.9994;
  const ratio_est=f.m * conv;
  const se=f.slopeSE * conv;
  return {value:ratio_est,se:se,reference:1.0000};
 }
 if(slug==='liquid-viscosity-poiseuille'){
  const const_geom=6.006263e-5;
  const eta_est=(const_geom / f.m) * 1000.0;
  const se=(const_geom / (f.m * f.m)) * f.slopeSE * 1000.0;
  return {value:eta_est,se:se,reference:1.0020};
 }
 if(slug==='surface-tension-stalagmometry'){
  const g=9.80665;
  const r=0.00350;
  const phi=0.6150;
  const k_tip=g / (2.0 * Math.PI * r * phi);
  const gamma_est=f.m * k_tip;
  const se=f.slopeSE * k_tip;
  return {value:gamma_est,se:se,reference:72.80};
 }
 if(slug==='colligative-freezing-point-depression'){
  const Kf=20.00;
  const w_solv=0.0250;
  const M_est=Kf / (w_solv * f.m);
  const se=(M_est / f.m) * f.slopeSE;
  return {value:M_est,se:se,reference:154.21};
 }
 if(slug==='solution-calorimetry-neutralization'){
  const C_eff=0.44365;
  const dH_est= -f.m * C_eff;
  const se=f.slopeSE * C_eff;
  return {value:dH_est,se:se,reference:-55.84};
 }
 if(slug==='hess-law-magnesium-calorimetry'){
  const M_Mg=24.305;
  const C_eff=0.44365;
  const dH1_est= -f.m * M_Mg * C_eff;
  const dH2= -146.00;
  const dH3= -285.83;
  const dHf_est= dH1_est - dH2 + dH3;
  const se= f.slopeSE * M_Mg * C_eff;
  return {value:dHf_est,se:se,reference:-601.83};
 }
 if(slug==='combustion-bomb-calorimetry-benzoic'){
  const M_benzoic=122.12;
  const C_cal=10.500;
  const dU_est= -f.m * M_benzoic * C_cal;
  const se= f.slopeSE * M_benzoic * C_cal;
  return {value:dU_est,se:se,reference:-3227.0};
 }
 if(slug==='heat-solution-crystallization-calorimetry'){
  const M_KNO3=101.103;
  const C_eff=0.44590;
  const dH_est= f.m * M_KNO3 * C_eff;
  const se= f.slopeSE * M_KNO3 * C_eff;
  return {value:dH_est,se:se,reference:34.89};
 }
 if(slug==='vapor-pressure-liquid-clausius-clapeyron'){
  const dH_est= -f.m * 8.31446;
  const se= f.slopeSE * 8.31446;
  return {value:dH_est,se:se,reference:38.56};
 }
 throw Error('Unknown Chemistry experiment estimate: '+slug);
}

const api={predict,reading,fit,estimate,round};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
else root.ChemistryModels=api;
})(typeof window==='undefined'?{}:window);
