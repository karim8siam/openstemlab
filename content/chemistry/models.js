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
 if(slug==='gibbs-free-energy-solubility-van-t-hoff'){
  const t=Number(input);
  const T=t + 273.15;
  const R=8.31446;
  const dH=110000.0;
  const dS=330.0;
  const ln_Ksp= -dH / (R * T) + dS / R;
  const Ksp=Math.exp(ln_Ksp);
  const s=Math.pow(Ksp / 4.0, 1.0 / 3.0);
  const v_hcl=20.0 * s;
  const raw=round(v_hcl, 2);
  const x=round(1000.0 / T, 4);
  const s_calc=raw / 20.0;
  const ksp_calc=4.0 * Math.pow(s_calc, 3);
  const y=round(Math.log(ksp_calc), 4);
  return {raw,ideal:raw,period:1.0,x,y,valid:t>=30.0&&t<=55.0};
 }
 if(slug==='enzyme-kinetics-michaelis-menten-spectrophotometry'){
  const s_val=Number(input);
  const KM_ref=0.500;
  const Vmax_ref=0.0400;
  const table={0.200:11.43, 0.350:16.47, 0.500:20.00, 0.800:24.62, 1.500:30.00, 3.000:34.29};
  const sKey=round(s_val, 3);
  const raw=table.hasOwnProperty(sKey)?table[sKey]:round((Vmax_ref * s_val / (KM_ref + s_val)) * 1000.0, 2);
  const x=round(1.0 / s_val, 3);
  const v0_mM=raw / 1000.0;
  const y=round(1.0 / v0_mM, 2);
  return {raw,ideal:raw,period:1.0,x,y,valid:s_val>=0.10&&s_val<=4.00};
 }
 if(slug==='photochemical-decomposition-uranyl-oxalate'){
  const t=Number(input);
  const V0=20.00;
  const phi=0.570;
  const q0=10.00; // ueinstein/min
  const rate_umol=phi * q0; // 5.700 umol/min
  const table={5.0:18.86, 10.0:17.72, 15.0:16.58, 20.0:15.44, 30.0:13.16, 40.0:10.88};
  const key=round(t, 1);
  const raw=table.hasOwnProperty(key)?table[key]:round(V0 - (rate_umol * t) / 25.0, 2);
  const x=t;
  const y=round(25.0 * (V0 - raw), 2);
  return {raw,ideal:raw,period:1.0,x,y,valid:t>=2.0&&t<=60.0};
 }
 if(slug==='clock-reaction-landolt-iodate-sulfite'){
  const io3=Number(input);
  const k_prime=0.00500;
  const table={4.00:50.00, 6.00:33.33, 8.00:25.00, 10.00:20.00, 14.00:14.29, 20.00:10.00};
  const key=round(io3, 2);
  const raw=table.hasOwnProperty(key)?table[key]:round(1.0 / (k_prime * io3), 2);
  const x=io3;
  const y=round(1.0 / raw, 4);
  return {raw,ideal:raw,period:1.0,x,y,valid:io3>=2.0&&io3<=25.0};
 }
 if(slug==='second-order-saponification-conductivity'){
  const t=Number(input);
  const c_0=0.0200;
  const k_ref=6.60;
  const kappa_0=4.974;
  const kappa_inf=1.820;
  const delta_max=kappa_0 - kappa_inf;
  const inv_c_t=(1.0 / c_0) + k_ref * t;
  const c_t=1.0 / inv_c_t;
  const kappa_ideal=kappa_inf + delta_max * (c_t / c_0);
  const raw=round(kappa_ideal, 3);
  const c_t_calc=c_0 * (raw - kappa_inf) / delta_max;
  const x=t;
  const y=round(1.0 / c_t_calc, 2);
  return {raw,ideal:raw,period:1.0,x,y,valid:t>=2.0&&t<=35.0};
 }
 if(slug==='first-order-kinetics-ester-hydrolysis'){
  const t=Number(input);
  const V_0=12.50;
  const V_inf=28.23;
  const k_ref=0.00685;
  const frac=1.0 - Math.exp(-k_ref * t);
  const V_t_ideal=V_0 + (V_inf - V_0) * frac;
  const raw=round(V_t_ideal, 2);
  const x=t;
  const y=round(Math.log((V_inf - V_0) / (V_inf - raw)), 4);
  return {raw,ideal:raw,period:1.0,x,y,valid:t>=10.0&&t<=120.0};
 }
 if(slug==='activation-energy-arrhenius-acetone-iodination'){
  const T_c=Number(input);
  const T_k=T_c + 273.15;
  const R_const=8.314462618;
  const E_a=84140.0;
  const A_arr=1.541094e10;
  const k_ideal=A_arr * Math.exp(-E_a / (R_const * T_k));
  const dt_ideal=0.00200 / k_ideal;
  const raw=round(dt_ideal, 2);
  const k_calc=0.00200 / raw;
  const x=round(1000.0 / T_k, 4);
  const y=round(Math.log(k_calc), 4);
  return {raw,ideal:raw,period:1.0,x,y,valid:T_c>=20.0&&T_c<=45.0};
 }
 if(slug==='chemical-kinetics-iodine-clock-persulfate'){
  const p_mM=Number(input);
  const p_M=p_mM * 1e-3;
  const k_ref=0.0220;
  const I_conc=0.0800;
  const delta_thiosulfate=0.00100;
  const rate_ideal=k_ref * p_M * I_conc;
  const dt_ideal=delta_thiosulfate / (2.0 * rate_ideal);
  const raw=round(dt_ideal, 3);
  const rate_calc=delta_thiosulfate / (2.0 * raw);
  const x=p_mM;
  const y=round(rate_calc * 1e5, 4);
  return {raw,ideal:raw,period:1.0,x,y,valid:p_mM>=10.0&&p_mM<=60.0};
 }
 if(slug==='three-component-liquid-liquid-ternary-phase'){
  const C_aq=Number(input);
  const K_D=0.100;
  const K_dim=100.0;
  const m_slope=2.0 * K_dim * (K_D * K_D); // 2.000 L/mol
  const C_org=K_D * C_aq + m_slope * (C_aq * C_aq);
  // Titrating 5.00 mL aliquot with 0.250 M NaOH:
  // V_NaOH = C_org * 5.00 / 0.250 = 20.0 * C_org (mL)
  const raw=round(20.0 * C_org, 2);
  const C_org_calc=raw / 20.0;
  const D_calc=C_org_calc / C_aq;
  const x=C_aq;
  const y=round(D_calc, 4);
  return {raw,ideal:raw,period:1.0,x,y,valid:C_aq>=0.20&&C_aq<=1.20};
 }

 if(slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  const x1=Number(input);
  const x2=1.0 - x1;
  const A=1.400;
  const gamma1=Math.exp(A * x2 * x2);
  const gamma2=Math.exp(A * x1 * x1);
  let low=77.0, high=100.0;
  for(let i=0; i<25; i++){
    const mid=(low + high) / 2.0;
    const P1=0.133322368 * Math.pow(10, 8.20417 - 1642.89 / (mid + 230.300));
    const P2=0.133322368 * Math.pow(10, 8.07131 - 1730.63 / (mid + 233.426));
    const P=P1 * x1 * gamma1 + P2 * x2 * gamma2;
    if(P < 101.325) low=mid;
    else high=mid;
  }
  const Tb=(low + high) / 2.0;
  const P1sat=0.133322368 * Math.pow(10, 8.20417 - 1642.89 / (Tb + 230.300));
  const P1=P1sat * x1 * gamma1;
  const raw=round(P1 / 101.325, 4);
  const gamma1_calc=(raw * 101.325) / (x1 * P1sat);
  const x=round(x2 * x2, 4);
  const y=round(Math.log(gamma1_calc), 4);
  return {raw,ideal:raw,period:1.0,x,y,valid:x1>=0.10&&x1<=0.60};
 }

 if(slug==='partial-molar-volume-binary-mixtures'){
  const m=Number(input);
  const M2=46.069;
  const rho0=0.997047;
  const V_pyc=25.0000;
  const m_pyc=18.4250;
  const phi_ideal=54.20 + 0.25 * m;
  const rho_ideal=(1000.0 + m * M2) / (1000.0 / rho0 + m * phi_ideal);
  const raw=round(m_pyc + rho_ideal * V_pyc, 4);
  const rho_calc=(raw - m_pyc) / V_pyc;
  const phi_calc=((1000.0 + m * M2) / rho_calc - 1000.0 / rho0) / m;
  const x=m;
  const y=round(phi_calc, 4);
  return {raw,ideal:raw,period:1.0,x,y,valid:m>=0.5&&m<=3.0};
 }
 if(slug==='heat-capacity-ratio-gases-clement-desormes'){
  const h1=Number(input);
  const gamma=1.400;
  const slope=(gamma - 1.0) / gamma;
  const raw=round(h1 * slope, 2);
  const x=h1;
  const y=raw;
  return {raw,ideal:raw,period:1.0,x,y,valid:h1>=15.0&&h1<=40.0};
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
 if(slug==='gibbs-free-energy-solubility-van-t-hoff'){
  const t=Number(input);
  const V=Number(raw);
  const T=t + 273.15;
  x=round(1000.0 / T, 4);
  const s_calc=V / 20.0;
  const ksp_calc=4.0 * Math.pow(s_calc, 3);
  y=round(Math.log(ksp_calc), 4);
 }
 if(slug==='enzyme-kinetics-michaelis-menten-spectrophotometry'){
  const s_val=Number(input);
  const raw_val=Number(raw);
  x=round(1.0 / s_val, 3);
  const v0_mM=raw_val / 1000.0;
  y=round(1.0 / v0_mM, 2);
 }
 if(slug==='photochemical-decomposition-uranyl-oxalate'){
  const t=Number(input);
  const raw_val=Number(raw);
  const V0=20.00;
  x=t;
  y=round(25.0 * (V0 - raw_val), 2);
 }
 if(slug==='clock-reaction-landolt-iodate-sulfite'){
  const io3=Number(input);
  const raw_val=Number(raw);
  x=io3;
  y=round(1.0 / raw_val, 4);
 }
 if(slug==='second-order-saponification-conductivity'){
  const t=Number(input);
  const raw_val=Number(raw);
  const c_0=0.0200;
  const kappa_0=4.974;
  const kappa_inf=1.820;
  const delta_max=kappa_0 - kappa_inf;
  const c_t_calc=c_0 * (raw_val - kappa_inf) / delta_max;
  x=t;
  y=round(1.0 / c_t_calc, 2);
 }
 if(slug==='first-order-kinetics-ester-hydrolysis'){
  const t=Number(input);
  const raw_val=Number(raw);
  const V_0=12.50;
  const V_inf=28.23;
  x=t;
  y=round(Math.log((V_inf - V_0) / (V_inf - raw_val)), 4);
 }
 if(slug==='activation-energy-arrhenius-acetone-iodination'){
  const T_c=Number(input);
  const T_k=T_c + 273.15;
  const raw_val=Number(raw);
  const k_calc=0.00200 / raw_val;
  x=round(1000.0 / T_k, 4);
  y=round(Math.log(k_calc), 4);
 }
 if(slug==='chemical-kinetics-iodine-clock-persulfate'){
  const p_mM=Number(input);
  const raw_val=Number(raw);
  const delta_thiosulfate=0.00100;
  const rate_calc=delta_thiosulfate / (2.0 * raw_val);
  x=p_mM;
  y=round(rate_calc * 1e5, 4);
 }
 if(slug==='three-component-liquid-liquid-ternary-phase'){
  const C_aq=Number(input);
  const raw_val=Number(raw);
  const C_org_calc=raw_val / 20.0;
  const D_calc=C_org_calc / C_aq;
  x=C_aq;
  y=round(D_calc, 4);
 }
 if(slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  const x1=Number(input);
  const x2=1.0 - x1;
  const raw_val=Number(raw);
  let low=77.0, high=100.0;
  for(let i=0; i<25; i++){
    const mid=(low + high) / 2.0;
    const P1=0.133322368 * Math.pow(10, 8.20417 - 1642.89 / (mid + 230.300));
    const P2=0.133322368 * Math.pow(10, 8.07131 - 1730.63 / (mid + 233.426));
    const P=P1 * x1 * Math.exp(1.400 * x2 * x2) + P2 * x2 * Math.exp(1.400 * x1 * x1);
    if(P < 101.325) low=mid;
    else high=mid;
  }
  const Tb=(low + high) / 2.0;
  const P1sat=0.133322368 * Math.pow(10, 8.20417 - 1642.89 / (Tb + 230.300));
  const gamma1_calc=(raw_val * 101.325) / (x1 * P1sat);
  x=round(x2 * x2, 4);
  y=round(Math.log(gamma1_calc), 4);
 }
 if(slug==='partial-molar-volume-binary-mixtures'){
  const m=Number(input);
  const M2=46.069;
  const rho0=0.997047;
  const V_pyc=25.0000;
  const m_pyc=18.4250;
  const raw_val=Number(raw);
  const rho_calc=(raw_val - m_pyc) / V_pyc;
  const phi_calc=((1000.0 + m * M2) / rho_calc - 1000.0 / rho0) / m;
  x=m;
  y=round(phi_calc, 4);
 }
 if(slug==='heat-capacity-ratio-gases-clement-desormes'){
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
 if(slug==='gibbs-free-energy-solubility-van-t-hoff'){
  const dH_est= -f.m * 8.31446;
  const se= f.slopeSE * 8.31446;
  return {value:dH_est,se:se,reference:110.0};
 }
 if(slug==='enzyme-kinetics-michaelis-menten-spectrophotometry'){
  const KM=f.m / f.b;
  const se=Math.abs(f.slopeSE / f.b);
  return {value:KM,se:se,reference:0.500};
 }
 if(slug==='photochemical-decomposition-uranyl-oxalate'){
  const q0=10.00; // ueinstein/min
  const phi=f.m / q0;
  const se=f.slopeSE / q0;
  return {value:phi,se:se,reference:0.570};
 }
 if(slug==='clock-reaction-landolt-iodate-sulfite'){
  const k_prime=f.m;
  const k_val=k_prime * 1000.0;
  const se=f.slopeSE * 1000.0;
  return {value:k_val,se:se,reference:5.000};
 }
 if(slug==='second-order-saponification-conductivity'){
  const slope= f.m;
  const se= f.slopeSE;
  return {value:slope,se:se,reference:6.60};
 }
 if(slug==='first-order-kinetics-ester-hydrolysis'){
  const slope= f.m;
  const se= f.slopeSE;
  return {value:slope,se:se,reference:0.00685};
 }
 if(slug==='activation-energy-arrhenius-acetone-iodination'){
  const slope= f.m;
  const R_const= 8.314462618;
  const E_a_est= -slope * R_const;
  const se= f.slopeSE * R_const;
  return {value:E_a_est,se:se,reference:84.14};
 }
 if(slug==='chemical-kinetics-iodine-clock-persulfate'){
  const slope= f.m;
  const I_conc= 0.0800;
  const k_prime_est= slope * 1e-2;
  const k_second_est= k_prime_est / I_conc;
  const se= (f.slopeSE * 1e-2) / I_conc;
  return {value:k_second_est,se:se,reference:0.0220};
 }
 if(slug==='three-component-liquid-liquid-ternary-phase'){
  const K_D_est= f.b;
  const m_slope= f.m;
  const K_dim_est= m_slope / (2.0 * K_D_est * K_D_est);
  const se= (f.slopeSE / (2.0 * K_D_est * K_D_est));
  return {value:K_dim_est,se:se,reference:100.0};
 }
 if(slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  const A_est= f.m;
  const se= f.slopeSE;
  return {value:A_est,se:se,reference:1.400};
 }
 if(slug==='partial-molar-volume-binary-mixtures'){
  const V2_inf_est= f.b;
  const se= f.interceptSE;
  return {value:V2_inf_est,se:se,reference:54.20};
 }
 if(slug==='heat-capacity-ratio-gases-clement-desormes'){
  const gamma_est= 1.0 / (1.0 - f.m);
  const se= (gamma_est * gamma_est) * f.slopeSE;
  return {value:gamma_est,se:se,reference:1.400};
 }
 throw Error('Unknown Chemistry experiment estimate: '+slug);
}

const api={predict,reading,fit,estimate,round};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
else root.ChemistryModels=api;
})(typeof window==='undefined'?{}:window);
