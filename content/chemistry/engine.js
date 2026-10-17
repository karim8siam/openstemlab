'use strict';
const cfg=JSON.parse(document.getElementById('labConfig').textContent),model=window.ChemistryModels,$=id=>document.getElementById(id);
const fmt=(v,n=4)=>Math.abs(v)>0&&(Math.abs(v)<.001||Math.abs(v)>=1e6)?v.toExponential(3):v.toFixed(n);
let rows=[],measurement=null,busy=false,clearPending=false;
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
 if(cfg.slug==='hydrate-stoichiometric-composition'){
  $('liveState').textContent='Ready to calcine crucible containing '+p.input.toFixed(1)+' g hydrate.';
  message('Adjust initial hydrate mass, then calcine to constant mass.');
 }else if(cfg.slug==='limiting-reactant-precipitation'){
  $('liveState').textContent='Ready to deliver '+p.input.toFixed(1)+' mL of 0.1000 M Na₂SO₄ into excess BaCl₂.';
  message('Adjust sulfate volume V, then precipitate, digest, filter & weigh.');
 }else if(cfg.slug==='molar-volume-ideal-gas'){
  $('liveState').textContent='Ready to react '+p.input.toFixed(1)+' mg magnesium ribbon in eudiometer.';
  message('Set magnesium mass m_Mg, then react, equilibrate meniscus & convert to STP.');
 }else if(cfg.slug==='volatile-liquid-molar-mass'){
  $('liveState').textContent='Ready to vaporize liquid in calibrated '+p.input.toFixed(1)+' mL Dumas bulb.';
  message('Set Dumas bulb volume V_flask, then vaporize, flush air, condense & weigh.');
 }else if(cfg.slug==='chemical-reactions-copper-cycle'){
  $('liveState').textContent='Ready to cycle '+p.input.toFixed(2)+' g copper wire through 5 reactions.';
  message('Set initial copper mass m_initial, then run cyclic reactions, isolate, wash & dry.');
 }else if(cfg.slug==='empirical-formula-magnesium-oxide'){
  $('liveState').textContent='Ready to burn '+p.input.toFixed(2)+' g burnished magnesium ribbon in porcelain crucible.';
  message('Set initial magnesium mass m_Mg, then oxidize, digest nitride with steam, calcine & weigh.');
 }else if(cfg.slug==='liquid-viscosity-poiseuille'){
  $('liveState').textContent='Ready to establish '+p.input.toFixed(1)+' cm hydrostatic head across capillary.';
  message('Set hydrostatic head Δh, equilibrate at 20.0 °C, purge bubbles & record flow rate.');
 }else if(cfg.slug==='surface-tension-stalagmometry'){
  $('liveState').textContent='Ready to collect '+p.input.toFixed(0)+' drops from Traube stalagmometer tip.';
  message('Set drop count N, throttle needle valve to 8–10 s/drop, collect into weighing bottle & weigh.');
 }else if(cfg.slug==='colligative-freezing-point-depression'){
  $('liveState').textContent='Ready to dissolve '+p.input.toFixed(2)+' g solute in 25.00 g cyclohexane.';
  message('Set solute mass w_solute, cool cell in 2 °C ice bath, resolve cooling curve & record ΔT_f.');
 }else if(cfg.slug==='solution-calorimetry-neutralization'){
  $('liveState').textContent='Ready to neutralize '+p.input.toFixed(3)+' mol H3O+/OH- in 100 mL solution.';
  message('Set stoichiometric moles n, dispense 50 mL acid & 50 mL base, seal Dewar & log temperature rise ΔT.');
 }else if(cfg.slug==='hess-law-magnesium-calorimetry'){
  $('liveState').textContent='Ready to dissolve '+p.input.toFixed(3)+' g Mg ribbon in 100 mL 1.0 M HCl.';
  message('Set magnesium mass m_Mg, abrade ribbon, charge into Dewar & monitor exothermic rise ΔT₁.');
 }else if(cfg.slug==='combustion-bomb-calorimetry-benzoic'){
  $('liveState').textContent='Ready to combust '+p.input.toFixed(3)+' g benzoic acid pellet under 30 atm O2.';
  message('Set pellet mass m, verify 10 cm fuse wire contact, pressurize bomb to 30 atm O2 & fire.');
 }else if(cfg.slug==='heat-solution-crystallization-calorimetry'){
  $('liveState').textContent='Ready to dissolve '+p.input.toFixed(3)+' g KNO3 crystals in 100 mL H2O.';
  message('Set solute mass m_KNO3, transfer crystals via powder funnel into Dewar & log temperature drop.');
 }else if(cfg.slug==='vapor-pressure-liquid-clausius-clapeyron'){
  $('liveState').textContent='Ready to equilibrate ethanol isoteniscope at '+p.input.toFixed(1)+' °C.';
  message('Set bath temperature t, adjust vacuum ballast manifold until U-tube levels match & log P.');
 }else if(cfg.slug==='gibbs-free-energy-solubility-van-t-hoff'){
  $('liveState').textContent='Ready to equilibrate saturated borax slurry at '+p.input.toFixed(1)+' °C.';
  message('Equilibrate borax flask, pre-warm filter pipette, draw 5.00 mL aliquot & titrate with 0.50 M HCl.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  $('liveState').textContent='Ready to reflux Othmer still with x_liquid = '+p.input.toFixed(2)+' ethanol.';
  message('Energize heating mantle, establish Cottrell thermo-lift pumping, reflux 30 min & sample condensate.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  const x1 = p.input;
  const x2 = 1.0 - x1;
  const raw_val = raw;
  let low = 77.0, high = 100.0;
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
  const gamma1=(raw_val * 101.325) / (x1 * P1sat);
  const nD = 1.3330 + 0.0284 * raw_val;
  $('liveState').textContent='VLE equilibrium reached: T_b = '+Tb.toFixed(2)+' °C, y_vapor = '+raw_val.toFixed(4)+'.';
  message('Distillation equilibrium established: T_b = '+Tb.toFixed(2)+' °C, n_D²⁰ = '+nD.toFixed(4)+' (y₁ = '+raw_val.toFixed(4)+', γ₁ = '+gamma1.toFixed(3)+'). Record in notebook.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawVleCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawVleSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawVleBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='partial-molar-volume-binary-mixtures'){
  $('liveState').textContent='Ready to equilibrate pycnometer with m = '+p.input.toFixed(2)+' mol/kg ethanol.';
  message('Fill 25 mL pycnometer, seat capillary stopper, equilibrate in 25.00 °C bath & weigh on balance.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  $('liveState').textContent='Ready to reflux Othmer still with x_liquid = '+p.input.toFixed(2)+' ethanol.';
  message('Energize heating mantle, establish Cottrell thermo-lift pumping, reflux 30 min & sample condensate.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  const x1 = p.input;
  const x2 = 1.0 - x1;
  const raw_val = raw;
  let low = 77.0, high = 100.0;
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
  const gamma1=(raw_val * 101.325) / (x1 * P1sat);
  const nD = 1.3330 + 0.0284 * raw_val;
  $('liveState').textContent='VLE equilibrium reached: T_b = '+Tb.toFixed(2)+' °C, y_vapor = '+raw_val.toFixed(4)+'.';
  message('Distillation equilibrium established: T_b = '+Tb.toFixed(2)+' °C, n_D²⁰ = '+nD.toFixed(4)+' (y₁ = '+raw_val.toFixed(4)+', γ₁ = '+gamma1.toFixed(3)+'). Record in notebook.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawVleCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawVleSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawVleBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='partial-molar-volume-binary-mixtures'){
  const m = p.input;
  const m_liq = raw - 18.4250;
  const rho = m_liq / 25.0;
  const phi = ((1000.0 + m * 46.069) / rho - 1000.0 / 0.997047) / m;
  $('liveState').textContent='Pycnometer weighed: m_filled = '+raw.toFixed(4)+' g (ρ = '+rho.toFixed(5)+' g/cm³).';
  message('Pycnometric weighing complete: m_filled = '+raw.toFixed(4)+' g (ρ = '+rho.toFixed(5)+' g/cm³, φ_V = '+phi.toFixed(3)+' cm³/mol). Record in notebook.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  $('liveState').textContent='Ready to reflux Othmer still with x_liquid = '+p.input.toFixed(2)+' ethanol.';
  message('Energize heating mantle, establish Cottrell thermo-lift pumping, reflux 30 min & sample condensate.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  const x1 = p.input;
  const x2 = 1.0 - x1;
  const raw_val = raw;
  let low = 77.0, high = 100.0;
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
  const gamma1=(raw_val * 101.325) / (x1 * P1sat);
  const nD = 1.3330 + 0.0284 * raw_val;
  $('liveState').textContent='VLE equilibrium reached: T_b = '+Tb.toFixed(2)+' °C, y_vapor = '+raw_val.toFixed(4)+'.';
  message('Distillation equilibrium established: T_b = '+Tb.toFixed(2)+' °C, n_D²⁰ = '+nD.toFixed(4)+' (y₁ = '+raw_val.toFixed(4)+', γ₁ = '+gamma1.toFixed(3)+'). Record in notebook.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawVleCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawVleSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawVleBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='partial-molar-volume-binary-mixtures'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawPycCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawPycSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawPycBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='heat-capacity-ratio-gases-clement-desormes'){
  $('liveState').textContent='Ready to pressurize 15 L carboy with dry air to h₁ = '+p.input.toFixed(1)+' cm.';
  message('Pressurize carboy with bellows pump, pre-equilibrate temperature, vent for 0.8 s & record h₂.');
 }else{
  $('liveState').textContent='Ready to dispense '+p.input.toFixed(cfg.inputDecimals)+' '+cfg.inputUnit+' of liquid.';
  message('Adjust '+cfg.shortInput+' V, then weigh the dispensed aliquot.');
 }
 draw(performance.now());
}

$('independent').addEventListener('input',()=>{$('independentNumber').value=$('independent').value;update();});
$('independentNumber').addEventListener('input',()=>{const v=+$('independentNumber').value;if($('independentNumber').value!==''&&Number.isFinite(v)&&v>=cfg.min&&v<=cfg.max){$('independent').value=v;update();}});
$('independentNumber').addEventListener('change',()=>{const v=+$('independentNumber').value;if(!Number.isFinite(v)||v<cfg.min||v>cfg.max){$('independentNumber').value=$('independent').value;message('Use a value between '+cfg.min+' and '+cfg.max+' '+cfg.inputUnit+'.',true);return;}$('independent').value=v;$('independentNumber').value=$('independent').value;update();});

$('pauseMotion').hidden=true;
$('resetApparatus').onclick=()=>{if(busy)return;$('independent').value=cfg.initial;$('independentNumber').value=cfg.initial;update();message('Apparatus reset to standard tare baseline. Your notebook is kept.');};

$('measure').onclick=async()=>{
 if(busy)return;
 const p=params(),prediction=model.predict(cfg.slug,p.input);
 if(!prediction.valid){message('Select a valid '+cfg.shortInput+' between '+cfg.min+' and '+cfg.max+' '+cfg.inputUnit+'.',true);return;}
 busy=true;$('measure').disabled=true;$('recordReading').disabled=true;$('independent').disabled=true;$('independentNumber').disabled=true;
 let msgStart='Dispensing '+p.input.toFixed(cfg.inputDecimals)+' '+cfg.inputUnit+' into tared beaker…';
 if(cfg.slug==='hydrate-stoichiometric-composition') msgStart='Heating crucible at 250 °C and evolving steam…';
 if(cfg.slug==='limiting-reactant-precipitation') msgStart='Adding Na₂SO₄ dropwise at 85 °C, digesting, filtering through Gooch crucible, drying to constant mass…';
 if(cfg.slug==='molar-volume-ideal-gas') msgStart='Inverting eudiometer, diffusing 6 M HCl, evolving H₂ gas, leveling menisci…';
 if(cfg.slug==='volatile-liquid-molar-mass') msgStart='Immersing Dumas bulb at 100 °C, flushing air through pinhole, condensing & weighing…';
 if(cfg.slug==='chemical-reactions-copper-cycle') msgStart='Dissolving in HNO₃, precipitating Cu(OH)₂, dehydrating to CuO, dissolving in H₂SO₄, reducing with Zn, washing & desiccation…';
 if(cfg.slug==='empirical-formula-magnesium-oxide') msgStart='Igniting magnesium ribbon, throttling aerosol smoke, digesting nitride with hot water, calcining at 850 °C…';
 if(cfg.slug==='liquid-viscosity-poiseuille') msgStart='Equilibrating jacket at 20.0 °C, establishing constant overflow head, timing effluent discharge…';
 if(cfg.slug==='surface-tension-stalagmometry') msgStart='Forming quasi-static pendent drops at 20.0 °C, detaching at razor tip, collecting into stoppered bottle…';
 if(cfg.slug==='colligative-freezing-point-depression') msgStart='Cooling in ice bath, stirring at 60 strokes/min, supercooling & extrapolating plateau…';
 if(cfg.slug==='solution-calorimetry-neutralization') msgStart='Dispensing base into Dewar, sealing lid, stirring at 200 rpm, logging exothermic adiabatic curve…';
 if(cfg.slug==='hess-law-magnesium-calorimetry') msgStart='Dropping polished Mg ribbon into 1.0 M HCl, sealing lid, vigorous H2 evolution & logging ΔT₁…';
 if(cfg.slug==='combustion-bomb-calorimetry-benzoic') msgStart='Discharging 23 V through ignition fuse wire, deflagration in 30 atm O2, logging temperature rise ΔT…';
 if(cfg.slug==='heat-solution-crystallization-calorimetry') msgStart='Pouring KNO3 crystals into Dewar, motorized stirring at 200 rpm, endothermic cooling plunge & logging ΔT_drop…';
 if(cfg.slug==='vapor-pressure-liquid-clausius-clapeyron') msgStart='Regulating water bath, throttling air-bleed needle valve, nulling U-tube menisci & reading transducer…';
 if(cfg.slug==='gibbs-free-energy-solubility-van-t-hoff') msgStart='Filtering 5.00 mL saturated borax aliquot, adding bromocresol green, titrating dropwise to yellow endpoint…';
 if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope') msgStart='Boiling in Othmer still, Cottrell pump washing PT100 sensor, sampling condensate onto Abbe refractometer…';
 if(cfg.slug==='partial-molar-volume-binary-mixtures') msgStart='Immersing pycnometer in 25.00 °C bath (20 min), blotting capillary rim, weighing on analytical balance…';
 if(cfg.slug==='heat-capacity-ratio-gases-clement-desormes') msgStart='Triggering quick-release valve, rapid adiabatic expansion (0.80 s), isochoric thermal re-warming…';
 message(msgStart);
 await new Promise(resolve=>setTimeout(resolve,400));
 const raw=prediction.raw;
 measurement=model.reading(cfg.slug,p.input,raw);
 busy=false;$('independent').disabled=false;$('independentNumber').disabled=false;$('measure').disabled=false;$('recordReading').disabled=false;
 $('readingValue').textContent=raw.toFixed(cfg.rawDecimals)+' '+cfg.rawUnit;
 if(cfg.slug==='hydrate-stoichiometric-composition'){
  $('liveState').textContent='Crucible cooled in desiccator: '+raw.toFixed(4)+' g water evolved.';
  message('Calcination complete: evolved '+raw.toFixed(4)+' g H₂O from '+p.input.toFixed(1)+' g hydrate. Record in notebook.');
 }else if(cfg.slug==='limiting-reactant-precipitation'){
  $('liveState').textContent='Isolated dry BaSO₄ precipitate: '+raw.toFixed(4)+' g.';
  message('Gravimetric precipitation complete: isolated '+raw.toFixed(4)+' g BaSO₄ from '+p.input.toFixed(1)+' mL sulfate. Record in notebook.');
 }else if(cfg.slug==='molar-volume-ideal-gas'){
  $('liveState').textContent='Eudiometric gas volume at STP: '+raw.toFixed(3)+' mL H₂.';
  message('Reaction complete: generated '+raw.toFixed(3)+' mL H₂ at STP from '+p.input.toFixed(1)+' mg Mg. Record in notebook.');
 }else if(cfg.slug==='volatile-liquid-molar-mass'){
  $('liveState').textContent='Condensed vapor mass: '+raw.toFixed(4)+' g in '+p.input.toFixed(1)+' mL bulb.';
  message('Vapor density determination complete: condensed '+raw.toFixed(4)+' g vapor in '+p.input.toFixed(1)+' mL flask. Record in notebook.');
 }else if(cfg.slug==='chemical-reactions-copper-cycle'){
  $('liveState').textContent='Desiccated recovered metallic copper: '+raw.toFixed(4)+' g.';
  message('Copper cycle complete: recovered '+raw.toFixed(4)+' g pure Cu from '+p.input.toFixed(2)+' g wire (100.00% yield). Record in notebook.');
 }else if(cfg.slug==='empirical-formula-magnesium-oxide'){
  $('liveState').textContent='Calcined magnesium oxide: incorporated '+raw.toFixed(4)+' g bound oxygen.';
  message('Crucible thermal oxidation complete: incorporated '+raw.toFixed(4)+' g O into '+p.input.toFixed(2)+' g Mg (formula MgO). Record in notebook.');
 }else if(cfg.slug==='liquid-viscosity-poiseuille'){
  $('liveState').textContent='Volumetric capillary discharge: '+raw.toFixed(3)+' mL/min at Δh = '+p.input.toFixed(1)+' cm.';
  message('Poiseuille flow stabilized: discharge rate '+raw.toFixed(3)+' mL/min under '+p.input.toFixed(1)+' cm head (Re < 90, laminar). Record in notebook.');
 }else if(cfg.slug==='surface-tension-stalagmometry'){
  $('liveState').textContent='Collected '+p.input.toFixed(0)+' drops: net mass '+raw.toFixed(4)+' g.';
  message('Drop-weight stalagmometry complete: '+p.input.toFixed(0)+' drops = '+raw.toFixed(4)+' g (m_drop = '+(raw/p.input).toFixed(5)+' g/drop). Record in notebook.');
 }else if(cfg.slug==='colligative-freezing-point-depression'){
  $('liveState').textContent='Freezing point depressed: ΔT_f = '+raw.toFixed(3)+' °C (T_f = '+(6.550-raw).toFixed(3)+' °C).';
  message('Cryoscopic determination complete: ΔT_f = '+raw.toFixed(3)+' °C for '+p.input.toFixed(2)+' g solute in cyclohexane (M = 154.2 g/mol). Record in notebook.');
 }else if(cfg.slug==='solution-calorimetry-neutralization'){
  $('liveState').textContent='Neutralization complete: ΔT = '+raw.toFixed(3)+' °C for '+p.input.toFixed(3)+' mol reacted.';
  message('Calorimetric measurement complete: ΔT = '+raw.toFixed(3)+' °C (q_rxn = '+(0.44365*raw).toFixed(3)+' kJ, ΔH = '+(-0.44365*raw/p.input).toFixed(2)+' kJ/mol). Record in notebook.');
 }else if(cfg.slug==='hess-law-magnesium-calorimetry'){
  const q_cal = 0.44365 * raw;
  const n_Mg = p.input / 24.305;
  const dH1 = -q_cal / n_Mg;
  const dHf = dH1 - (-146.0) + (-285.83);
  $('liveState').textContent='Reaction complete: ΔT₁ = '+raw.toFixed(3)+' °C for '+p.input.toFixed(3)+' g Mg.';
  message('Calorimetric dissolution complete: ΔT₁ = '+raw.toFixed(3)+' °C (ΔH₁ = '+dH1.toFixed(1)+' kJ/mol, Hess ΔH_f°[MgO] = '+dHf.toFixed(1)+' kJ/mol). Record in notebook.');
 }else if(cfg.slug==='combustion-bomb-calorimetry-benzoic'){
  const q_cal = 10.500 * raw;
  const n_mol = p.input / 122.12;
  const dU = -q_cal / n_mol;
  $('liveState').textContent='Combustion complete: ΔT = '+raw.toFixed(3)+' °C for '+p.input.toFixed(3)+' g pellet.';
  message('Bomb calorimetric combustion complete: ΔT = '+raw.toFixed(3)+' °C (ΔU_comb = '+dU.toFixed(1)+' kJ/mol, ΔH_comb = '+(dU - 1.24).toFixed(1)+' kJ/mol). Record in notebook.');
 }else if(cfg.slug==='heat-solution-crystallization-calorimetry'){
  const q_soln = 0.44590 * raw;
  const n_mol = p.input / 101.103;
  const dH = q_soln / n_mol;
  $('liveState').textContent='Dissolution complete: ΔT_drop = '+raw.toFixed(3)+' °C for '+p.input.toFixed(3)+' g KNO3.';
  message('Endothermic dissolution complete: ΔT_drop = '+raw.toFixed(3)+' °C (T_min = '+(25.000-raw).toFixed(3)+' °C, ΔH_soln = +'+dH.toFixed(2)+' kJ/mol). Record in notebook.');
 }else if(cfg.slug==='vapor-pressure-liquid-clausius-clapeyron'){
  const T_K = p.input + 273.15;
  const inv_T = 1000.0 / T_K;
  const ln_P = Math.log(raw);
  $('liveState').textContent='Equilibrium established: P = '+raw.toFixed(2)+' kPa at '+p.input.toFixed(1)+' °C.';
  message('Vapor pressure recorded: P = '+raw.toFixed(2)+' kPa ('+(raw*7.50062).toFixed(1)+' mmHg, ln P = '+ln_P.toFixed(4)+', 1000/T = '+inv_T.toFixed(4)+' K⁻¹). Record in notebook.');
 }else if(cfg.slug==='gibbs-free-energy-solubility-van-t-hoff'){
  const s = raw / 20.0;
  const Ksp = 4.0 * Math.pow(s, 3);
  const ln_Ksp = Math.log(Ksp);
  $('liveState').textContent='Titration endpoint reached: V_HCl = '+raw.toFixed(2)+' mL at '+p.input.toFixed(1)+' °C.';
  message('Titration complete: V_HCl = '+raw.toFixed(2)+' mL (s = '+s.toFixed(4)+' M, K_sp = '+Ksp.toExponential(3)+', ln K_sp = '+ln_Ksp.toFixed(3)+'). Record in notebook.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  $('liveState').textContent='Ready to reflux Othmer still with x_liquid = '+p.input.toFixed(2)+' ethanol.';
  message('Energize heating mantle, establish Cottrell thermo-lift pumping, reflux 30 min & sample condensate.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  const x1 = p.input;
  const x2 = 1.0 - x1;
  const raw_val = raw;
  let low = 77.0, high = 100.0;
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
  const gamma1=(raw_val * 101.325) / (x1 * P1sat);
  const nD = 1.3330 + 0.0284 * raw_val;
  $('liveState').textContent='VLE equilibrium reached: T_b = '+Tb.toFixed(2)+' °C, y_vapor = '+raw_val.toFixed(4)+'.';
  message('Distillation equilibrium established: T_b = '+Tb.toFixed(2)+' °C, n_D²⁰ = '+nD.toFixed(4)+' (y₁ = '+raw_val.toFixed(4)+', γ₁ = '+gamma1.toFixed(3)+'). Record in notebook.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawVleCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawVleSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawVleBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='partial-molar-volume-binary-mixtures'){
  $('liveState').textContent='Ready to equilibrate pycnometer with m = '+p.input.toFixed(2)+' mol/kg ethanol.';
  message('Fill 25 mL pycnometer, seat capillary stopper, equilibrate in 25.00 °C bath & weigh on balance.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  $('liveState').textContent='Ready to reflux Othmer still with x_liquid = '+p.input.toFixed(2)+' ethanol.';
  message('Energize heating mantle, establish Cottrell thermo-lift pumping, reflux 30 min & sample condensate.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  const x1 = p.input;
  const x2 = 1.0 - x1;
  const raw_val = raw;
  let low = 77.0, high = 100.0;
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
  const gamma1=(raw_val * 101.325) / (x1 * P1sat);
  const nD = 1.3330 + 0.0284 * raw_val;
  $('liveState').textContent='VLE equilibrium reached: T_b = '+Tb.toFixed(2)+' °C, y_vapor = '+raw_val.toFixed(4)+'.';
  message('Distillation equilibrium established: T_b = '+Tb.toFixed(2)+' °C, n_D²⁰ = '+nD.toFixed(4)+' (y₁ = '+raw_val.toFixed(4)+', γ₁ = '+gamma1.toFixed(3)+'). Record in notebook.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawVleCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawVleSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawVleBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='partial-molar-volume-binary-mixtures'){
  const m = p.input;
  const m_liq = raw - 18.4250;
  const rho = m_liq / 25.0;
  const phi = ((1000.0 + m * 46.069) / rho - 1000.0 / 0.997047) / m;
  $('liveState').textContent='Pycnometer weighed: m_filled = '+raw.toFixed(4)+' g (ρ = '+rho.toFixed(5)+' g/cm³).';
  message('Pycnometric weighing complete: m_filled = '+raw.toFixed(4)+' g (ρ = '+rho.toFixed(5)+' g/cm³, φ_V = '+phi.toFixed(3)+' cm³/mol). Record in notebook.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  $('liveState').textContent='Ready to reflux Othmer still with x_liquid = '+p.input.toFixed(2)+' ethanol.';
  message('Energize heating mantle, establish Cottrell thermo-lift pumping, reflux 30 min & sample condensate.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  const x1 = p.input;
  const x2 = 1.0 - x1;
  const raw_val = raw;
  let low = 77.0, high = 100.0;
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
  const gamma1=(raw_val * 101.325) / (x1 * P1sat);
  const nD = 1.3330 + 0.0284 * raw_val;
  $('liveState').textContent='VLE equilibrium reached: T_b = '+Tb.toFixed(2)+' °C, y_vapor = '+raw_val.toFixed(4)+'.';
  message('Distillation equilibrium established: T_b = '+Tb.toFixed(2)+' °C, n_D²⁰ = '+nD.toFixed(4)+' (y₁ = '+raw_val.toFixed(4)+', γ₁ = '+gamma1.toFixed(3)+'). Record in notebook.');
 }else if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawVleCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawVleSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawVleBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='partial-molar-volume-binary-mixtures'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawPycCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawPycSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawPycBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='heat-capacity-ratio-gases-clement-desormes'){
  const gamma_calc = p.input / (p.input - raw);
  $('liveState').textContent='Cycle complete: h₂ = '+raw.toFixed(2)+' cm for h₁ = '+p.input.toFixed(1)+' cm.';
  message('Clément-Desormes expansion complete: h₂ = '+raw.toFixed(2)+' cm (γ = '+gamma_calc.toFixed(3)+'). Record in notebook.');
 }else{
  $('liveState').textContent='Analytical balance stabilized: '+raw.toFixed(cfg.rawDecimals)+' g net mass.';
  message('Gravimetric measurement complete: '+raw.toFixed(cfg.rawDecimals)+' '+cfg.rawUnit+' for '+p.input.toFixed(cfg.inputDecimals)+' '+cfg.inputUnit+'. Record in notebook.');
 }
 draw(performance.now());
};

$('recordReading').onclick=()=>{
 if(!measurement)return;
 if(rows.length>=100){message('Notebook full. Export readings or clear the notebook.',true);return;}
 rows.push({...measurement});
 measurement=null;
 $('recordReading').disabled=true;
 persist();
 message('Observation '+rows.length+' recorded. Change '+cfg.shortInput+' for the next trial.');
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
  $('fitSummary').innerHTML='<strong>'+fmt(result.value*cfg.resultScale,cfg.resultDecimals)+' '+cfg.resultUnit+'</strong><p>Estimated '+cfg.target+'<br>Gradient: '+fmt(f.m)+'<br>Intercept: '+fmt(f.b)+' g<br>R²: '+f.r2.toFixed(5)+'<br>Difference from CIPM reference: '+pct.toFixed(3)+'%<br>Fit standard error: '+fmt(result.se*cfg.resultScale)+' '+cfg.resultUnit+'</p><p>Linear regression eliminates constant tare and meniscus biases.</p>';
 } else {
  $('fitSummary').innerHTML='<p>Record at least three distinct '+cfg.shortInput+' values to fit a regression line and calculate '+cfg.target+'.</p>';
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
 for(let i=0;i<5;i++){
  const x=xmin+i*(xmax-xmin)/4,y=ymin+i*(ymax-ymin)/4;
  svg+='<line x1="'+left+'" y1="'+py(y)+'" x2="'+right+'" y2="'+py(y)+'" stroke="#223b28" stroke-width="1"/>';
  svg+='<text x="'+(left-8)+'" y="'+(py(y)+4)+'" text-anchor="end" font-size="10" fill="#789c80">'+fmt(y,1)+'</text>';
  svg+='<text x="'+px(x)+'" y="300" text-anchor="middle" font-size="10" fill="#789c80">'+fmt(x,1)+'</text>';
 }
 svg+='<path d="M'+left+' '+top+'V'+bottom+'H'+right+'" stroke="#466e4e" fill="none"/>';
 svg+='<text x="335" y="332" text-anchor="middle" fill="#9ec4a6" font-size="12">'+cfg.xAxis+'</text>';
 svg+='<text transform="translate(18 160) rotate(-90)" text-anchor="middle" fill="#9ec4a6" font-size="12">'+cfg.yAxis+'</text>';
 if(f){
  const pts=[];
  for(let i=0;i<=100;i++){
   const x=xmin+i*(xmax-xmin)/100,y=(f.m*(x/cfg.xScale)+f.b)*cfg.yScale;
   pts.push(px(x).toFixed(1)+','+py(y).toFixed(1));
  }
  svg+='<polyline points="'+pts.join(' ')+'" stroke="#38a169" stroke-width="2" fill="none"/>';
 }
 rows.forEach((r,i)=>{
  svg+='<circle cx="'+px(r.x*cfg.xScale)+'" cy="'+py(r.y*cfg.yScale)+'" r="4.5" fill="#48bb78" stroke="#142b1a" stroke-width="1.5"><title>Aliquot '+(i+1)+': V = '+r.input.toFixed(cfg.inputDecimals)+' mL, m = '+r.raw.toFixed(cfg.rawDecimals)+' g</title></circle>';
 });
 $('labPlot').innerHTML=svg;
}

$('downloadReadings').onclick=()=>{
 if(!rows.length)return;
 let csv='aliquot,volume_mL,mass_g,x_metric,y_metric\n';
 rows.forEach((r,i)=>{csv+=(i+1)+','+r.input.toFixed(cfg.inputDecimals)+','+r.raw.toFixed(cfg.rawDecimals)+','+(r.x*cfg.xScale).toFixed(4)+','+(r.y*cfg.yScale).toFixed(4)+'\n';});
 const a=document.createElement('a');
 a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));
 a.download=cfg.slug+'-observations.csv';
 a.click();
};

$('clearReadings').onclick=()=>{
 if(!clearPending){clearPending=true;$('clearReadings').textContent='Confirm clear?';setTimeout(()=>{clearPending=false;$('clearReadings').textContent='Clear notebook';},3000);return;}
 rows=[];clearPending=false;$('clearReadings').textContent='Clear notebook';persist();message('Notebook cleared. Apparatus remains ready.');
};

$('checkEstimate').onclick=()=>{
 const val=+$('studentEstimate').value,f=model.fit(rows);
 if(!Number.isFinite(val)||val<=0){$('estimateFeedback').textContent='Enter a positive calculated density value.';return;}
 if(!f){$('estimateFeedback').textContent='Record at least three observations first to compare with regression.';return;}
 const result=model.estimate(cfg.slug,f),pct=Math.abs(val-result.value*cfg.resultScale)/(result.value*cfg.resultScale)*100;
 $('estimateFeedback').textContent=pct<1.0?'Excellent! Within '+pct.toFixed(2)+'% of regression slope ('+fmt(result.value*cfg.resultScale,cfg.resultDecimals)+' '+cfg.resultUnit+').':'Off by '+pct.toFixed(1)+'%. Fitted slope is '+fmt(result.value*cfg.resultScale,cfg.resultDecimals)+' '+cfg.resultUnit+'. Check S_xy / S_xx.';
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

function draw(t){
 const p=params();
 const rawVal=measurement?measurement.raw:model.predict(cfg.slug,p.input).raw;
 if(cfg.slug==='hydrate-stoichiometric-composition'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawHydrateCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawHydrateSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawHydrateBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='limiting-reactant-precipitation'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawLimitingCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawLimitingSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawLimitingBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='molar-volume-ideal-gas'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawGasCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawGasSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawGasBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='volatile-liquid-molar-mass'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawDumasCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawDumasSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawDumasBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='chemical-reactions-copper-cycle'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawCopperCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawCopperSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawCopperBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='empirical-formula-magnesium-oxide'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawMgCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawMgSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawMgBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='liquid-viscosity-poiseuille'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawPoiseuilleCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawPoiseuilleSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawPoiseuilleBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='surface-tension-stalagmometry'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawStalagCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawStalagSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawStalagBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='colligative-freezing-point-depression'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawCryoCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawCryoSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawCryoBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='solution-calorimetry-neutralization'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawCalorimetryCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawCalorimetrySandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawCalorimetryBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='hess-law-magnesium-calorimetry'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawHessCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawHessSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawHessBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='combustion-bomb-calorimetry-benzoic'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawBombCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawBombSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawBombBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='heat-solution-crystallization-calorimetry'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawSolnCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawSolnSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawSolnBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='vapor-pressure-liquid-clausius-clapeyron'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawVapCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawVapSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawVapBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='gibbs-free-energy-solubility-van-t-hoff'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawHoffCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawHoffSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawHoffBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='liquid-vapor-phase-equilibrium-azeotrope'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawVleCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawVleSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawVleBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='partial-molar-volume-binary-mixtures'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawPycCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawPycSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawPycBenchView(p,rawVal);
  return;
 }
 if(cfg.slug==='heat-capacity-ratio-gases-clement-desormes'){
  if(currentSimMode==='compare'){
   $('apparatusDiagram').innerHTML=drawClementCompareView(p,rawVal);
   return;
  }
  if(currentSimMode==='sandbox'){
   $('apparatusDiagram').innerHTML=drawClementSandboxView(p,rawVal);
   return;
  }
  $('apparatusDiagram').innerHTML=drawClementBenchView(p,rawVal);
  return;
 }
 if(currentSimMode==='compare'){
  $('apparatusDiagram').innerHTML=drawCompareView(p,rawVal);
  return;
 }
 if(currentSimMode==='sandbox'){
  $('apparatusDiagram').innerHTML=drawSandboxView(p,rawVal);
  return;
 }
 $('apparatusDiagram').innerHTML=drawBenchView(p,rawVal);
}

function drawBenchView(p,rawVal){
 const v=p.input;
 const m_disp=measurement?measurement.raw:(busy?rawVal*0.75:0.0000);
 const v_pct=v/35.0;
 const liquidHeight=Math.min(48, Math.max(6, v_pct*45));
 
 let svg='<defs><pattern id="chemGrid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" stroke="#ffffff" stroke-opacity=".03" fill="none"/></pattern>';
 svg+='<linearGradient id="glassGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#ffffff" stop-opacity=".15"/><stop offset="30%" stop-color="#ffffff" stop-opacity=".05"/><stop offset="80%" stop-color="#ffffff" stop-opacity=".12"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".25"/></linearGradient>';
 svg+='<linearGradient id="waterGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#38a169" stop-opacity=".4"/><stop offset="50%" stop-color="#48bb78" stop-opacity=".55"/><stop offset="100%" stop-color="#2f855a" stop-opacity=".45"/></linearGradient>';
 svg+='<linearGradient id="metalGrad" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#2d3748"/><stop offset="100%" stop-color="#1a202c"/></linearGradient>';
 svg+='</defs><rect width="720" height="320" fill="#0b140e"/><rect width="720" height="320" fill="url(#chemGrid)"/>';

 // Lab Table surface
 svg+='<rect x="0" y="270" width="720" height="50" fill="#132419" stroke="#1f3b2a" stroke-width="1"/>';
 svg+='<line x1="0" y1="270" x2="720" y2="270" stroke="#2d523b" stroke-width="2"/>';

 // Retort Stand (holding burette on left)
 svg+='<rect x="60" y="260" width="100" height="10" rx="2" fill="url(#metalGrad)" stroke="#4a5568" stroke-width="1"/>';
 svg+='<rect x="105" y="25" width="8" height="235" fill="url(#metalGrad)" stroke="#4a5568" stroke-width="1"/>';
 // Clamps
 svg+='<rect x="95" y="70" width="55" height="8" rx="2" fill="#718096"/>';
 svg+='<circle cx="109" cy="74" r="5" fill="#4a5568"/>';
 svg+='<rect x="95" y="160" width="55" height="8" rx="2" fill="#718096"/>';
 svg+='<circle cx="109" cy="164" r="5" fill="#4a5568"/>';

 // Burette body (x = 135 to 155)
 const bX=140,bW=14,bTop=35,bBottom=210;
 svg+='<rect x="'+bX+'" y="'+bTop+'" width="'+bW+'" height="'+(bBottom-bTop)+'" fill="url(#glassGrad)" stroke="#789c80" stroke-width="1.2" rx="1"/>';
 // Schellbach blue line in burette
 svg+='<line x1="'+(bX+bW/2)+'" y1="'+bTop+'" x2="'+(bX+bW/2)+'" y2="'+bBottom+'" stroke="#3182ce" stroke-width="1.2" stroke-opacity=".7"/>';
 // Liquid inside burette (draining as volume increases)
 const bLiquidTop=bTop + v_pct*110;
 svg+='<rect x="'+(bX+1)+'" y="'+bLiquidTop+'" width="'+(bW-2)+'" height="'+(bBottom-bLiquidTop)+'" fill="url(#waterGrad)"/>';
 svg+='<ellipse cx="'+(bX+bW/2)+'" cy="'+bLiquidTop+'" rx="'+(bW/2-1)+'" ry="2.5" fill="#68d391" fill-opacity=".7"/>';
 // Burette graduation lines
 for(let gy=bTop+10;gy<bBottom-10;gy+=8){
  const isMajor=(gy-bTop-10)%32===0;
  svg+='<line x1="'+bX+'" y1="'+gy+'" x2="'+(bX+(isMajor?6:3))+'" y2="'+gy+'" stroke="#a0aec0" stroke-width="'+(isMajor?1:0.7)+'"/>';
 }
 // Burette stopcock and tip
 svg+='<path d="M'+(bX+2)+' '+bBottom+' L'+(bX+5)+' '+(bBottom+14)+' L'+(bX+9)+' '+(bBottom+14)+' L'+(bX+12)+' '+bBottom+' Z" fill="url(#glassGrad)" stroke="#789c80"/>';
 svg+='<rect x="'+(bX-3)+'" y="'+(bBottom+8)+'" width="20" height="6" rx="2" fill="#e2e8f0" stroke="#a0aec0"/>'; // stopcock
 svg+='<path d="M'+(bX+5)+' '+(bBottom+14)+' L'+(bX+6)+' '+(bBottom+30)+' L'+(bX+8)+' '+(bBottom+30)+' L'+(bX+9)+' '+(bBottom+14)+' Z" fill="url(#glassGrad)" stroke="#789c80"/>';
 // Droplet stream when dispensing
 if(busy){
  svg+='<line x1="'+(bX+7)+'" y1="'+(bBottom+30)+'" x2="'+(bX+7)+'" y2="240" stroke="#48bb78" stroke-width="1.5" stroke-dasharray="4,3"/>';
  svg+='<circle cx="'+(bX+7)+'" cy="236" r="2.2" fill="#68d391"/>';
 }

 // Analytical Balance (centered at x = 360)
 const balX=240,balW=240,balBaseY=220,balH=50;
 // Granite slab
 svg+='<rect x="'+(balX-15)+'" y="262" width="'+(balW+30)+'" height="8" rx="2" fill="#2d3748" stroke="#1a202c"/>';
 // Balance housing
 svg+='<rect x="'+balX+'" y="'+balBaseY+'" width="'+balW+'" height="'+balH+'" rx="4" fill="#1a271f" stroke="#2d523b" stroke-width="1.5"/>';
 // Digital Display Screen
 svg+='<rect x="'+(balX+45)+'" y="'+(balBaseY+18)+'" width="150" height="24" rx="3" fill="#061009" stroke="#1e3b27" stroke-width="1"/>';
 svg+='<text x="'+(balX+185)+'" y="'+(balBaseY+35)+'" text-anchor="end" fill="#48bb78" font-size="15" font-family="monospace" font-weight="bold">'+(measurement?m_disp.toFixed(4):(busy?(rawVal*0.75).toFixed(4):'0.0000'))+' g</text>';
 svg+='<circle cx="'+(balX+55)+'" cy="'+(balBaseY+30)+'" r="2.5" fill="'+(busy?'#ecc94b':'#48bb78')+'"/>';
 svg+='<text x="'+(balX+62)+'" y="'+(balBaseY+33)+'" fill="#718096" font-size="7">STABLE</text>';
 // Tare and Cal buttons
 svg+='<rect x="'+(balX+18)+'" y="'+(balBaseY+22)+'" width="20" height="14" rx="2" fill="#274632" stroke="#3b6b4c"/><text x="'+(balX+28)+'" y="'+(balBaseY+32)+'" text-anchor="middle" fill="#a0aec0" font-size="6">TARE</text>';
 svg+='<rect x="'+(balX+202)+'" y="'+(balBaseY+22)+'" width="20" height="14" rx="2" fill="#274632" stroke="#3b6b4c"/><text x="'+(balX+212)+'" y="'+(balBaseY+32)+'" text-anchor="middle" fill="#a0aec0" font-size="6">CAL</text>';

 // Glass Draft Shield Enclosure
 const dsX=balX+25,dsW=balW-50,dsTop=75,dsH=balBaseY-dsTop;
 svg+='<rect x="'+dsX+'" y="'+dsTop+'" width="'+dsW+'" height="'+dsH+'" fill="url(#glassGrad)" stroke="#386b48" stroke-width="1.2" rx="2"/>';
 svg+='<line x1="'+(dsX+dsW/2)+'" y1="'+dsTop+'" x2="'+(dsX+dsW/2)+'" y2="'+balBaseY+'" stroke="#ffffff" stroke-opacity=".08" stroke-width="1"/>';
 // Weighing Pan inside draft shield
 svg+='<rect x="'+(dsX+dsW/2-35)+'" y="'+(balBaseY-8)+'" width="70" height="5" rx="1.5" fill="#cbd5e0" stroke="#718096"/>';
 svg+='<rect x="'+(dsX+dsW/2-4)+'" y="'+(balBaseY-3)+'" width="8" height="3" fill="#a0aec0"/>';

 // Receiving Beaker (100 mL) on Pan (x centered at dsX + dsW/2 = 360)
 const bkX=330,bkW=60,bkH=70,bkY=balBaseY-8-bkH;
 svg+='<rect x="'+bkX+'" y="'+bkY+'" width="'+bkW+'" height="'+bkH+'" rx="2" fill="url(#glassGrad)" stroke="#789c80" stroke-width="1.2"/>';
 svg+='<path d="M'+(bkX+bkW)+' '+bkY+' L'+(bkX+bkW+6)+' '+(bkY-4)+' L'+(bkX+bkW)+' '+(bkY+4)+' Z" fill="url(#glassGrad)" stroke="#789c80"/>'; // spout
 // Water inside beaker
 const wY=bkY+bkH-liquidHeight;
 svg+='<rect x="'+(bkX+1.5)+'" y="'+wY+'" width="'+(bkW-3)+'" height="'+(liquidHeight-1)+'" rx="1" fill="url(#waterGrad)"/>';
 svg+='<ellipse cx="'+(bkX+bkW/2)+'" cy="'+wY+'" rx="'+(bkW/2-2)+'" ry="3" fill="#68d391" fill-opacity=".65"/>';
 // Beaker graduation markings
 for(let gy=bkY+15;gy<bkY+bkH-10;gy+=12){
  svg+='<line x1="'+bkX+'" y1="'+gy+'" x2="'+(bkX+8)+'" y2="'+gy+'" stroke="#e2e8f0" stroke-opacity=".4" stroke-width="1"/>';
 }
 svg+='<text x="'+(bkX+12)+'" y="'+(bkY+28)+'" fill="#cbd5e0" fill-opacity=".5" font-size="7">100 mL</text>';

 // Right Side: Thermostat Water Bath & Thermometer
 const bathX=530,bathY=175,bathW=150,bathH=95;
 svg+='<rect x="'+bathX+'" y="'+bathY+'" width="'+bathW+'" height="'+bathH+'" rx="5" fill="#12251a" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<rect x="'+(bathX+10)+'" y="'+(bathY+12)+'" width="'+(bathW-20)+'" height="'+(bathH-22)+'" rx="3" fill="#09140e" stroke="#1a3825"/>';
 svg+='<text x="'+(bathX+bathW/2)+'" y="'+(bathY+28)+'" text-anchor="middle" fill="#789c80" font-size="9" font-weight="bold">THERMOSTATIC CONTROLLER</text>';
 // LED display of temperature
 svg+='<rect x="'+(bathX+25)+'" y="'+(bathY+36)+'" width="100" height="26" rx="3" fill="#040d07" stroke="#163820"/>';
 svg+='<text x="'+(bathX+75)+'" y="'+(bathY+54)+'" text-anchor="middle" fill="#48bb78" font-size="15" font-family="monospace" font-weight="bold">20.00 °C</text>';
 svg+='<text x="'+(bathX+bathW/2)+'" y="'+(bathY+76)+'" text-anchor="middle" fill="#81e6d9" font-size="8">±0.01 °C PELTIER REGULATED</text>';

 // Status overlay on top bar
 svg+='<text x="360" y="24" text-anchor="middle" fill="#81e6d9" font-size="11" font-weight="bold">CLASS A VOLUMETRIC GRAVIMETRY · ρ = m / V = 0.9982 g/mL</text>';
 return svg;
}

function drawCompareView(p,rawVal){
 let svg='<rect width="720" height="320" fill="#0b140e"/>';
 const text=(x,y,str,color='#789c80',size=11)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';
 svg+=text(360,26,'ANALYTICAL METROLOGY COMPARISON: THREE DENSITY METHODOLOGIES','#a7f3d0',12);

 const methods=[
  {
   name:'1. Capillary Pycnometer',
   type:'Hydrostatic Confinement (Gay-Lussac)',
   prec:'±0.0001 g/mL',
   vol:'25.000 mL',
   time:'30–45 min',
   adv:'Eliminates optical meniscus reading; exact volume calibration via CIPM water standard.',
   col:'#38a169',
   bar:88
  },
  {
   name:'2. Class A Volumetric Burette',
   type:'Gravimetric Aliquot Titration',
   prec:'±0.0020 g/mL',
   vol:'5.0–50.0 mL',
   time:'5–10 min',
   adv:'Rapid sequential aliquots; linear regression slope eliminates constant tare/meniscus offsets.',
   col:'#3182ce',
   bar:62
  },
  {
   name:'3. Digital Oscillating U-Tube',
   type:'Harmonic Resonance (Anton Paar)',
   prec:'±0.00005 g/mL',
   vol:'1.5 mL',
   time:'1–2 min',
   adv:'Frequency period T² = A + B·ρ; minimal sample volume; automated Peltier control.',
   col:'#d69e2e',
   bar:98
  }
 ];

 methods.forEach((m,idx)=>{
  const cx=50+idx*215,cy=45,cw=195,ch=245;
  svg+='<rect x="'+cx+'" y="'+cy+'" width="'+cw+'" height="'+ch+'" rx="6" fill="#101e14" stroke="'+m.col+'" stroke-width="1.5"/>';
  svg+='<rect x="'+cx+'" y="'+cy+'" width="'+cw+'" height="28" rx="5" fill="'+m.col+'" fill-opacity=".2"/>';
  svg+='<text x="'+(cx+cw/2)+'" y="'+(cy+18)+'" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="bold">'+m.name+'</text>';
  svg+='<text x="'+(cx+cw/2)+'" y="'+(cy+42)+'" text-anchor="middle" fill="#a0aec0" font-size="8.5">'+m.type+'</text>';
  svg+='<line x1="'+(cx+12)+'" y1="'+(cy+52)+'" x2="'+(cx+cw-12)+'" y2="'+(cy+52)+'" stroke="#1f3b28"/>';

  svg+='<text x="'+(cx+15)+'" y="'+(cy+70)+'" fill="#789c80" font-size="8.5">PRECISION LIMIT:</text>';
  svg+='<text x="'+(cx+cw-15)+'" y="'+(cy+70)+'" text-anchor="end" fill="'+m.col+'" font-size="10" font-family="monospace" font-weight="bold">'+m.prec+'</text>';

  svg+='<text x="'+(cx+15)+'" y="'+(cy+92)+'" fill="#789c80" font-size="8.5">SAMPLE VOLUME:</text>';
  svg+='<text x="'+(cx+cw-15)+'" y="'+(cy+92)+'" text-anchor="end" fill="#e2e8f0" font-size="9" font-family="monospace">'+m.vol+'</text>';

  svg+='<text x="'+(cx+15)+'" y="'+(cy+114)+'" fill="#789c80" font-size="8.5">EQUILIBRATION TIME:</text>';
  svg+='<text x="'+(cx+cw-15)+'" y="'+(cy+114)+'" text-anchor="end" fill="#e2e8f0" font-size="9" font-family="monospace">'+m.time+'</text>';

  svg+='<line x1="'+(cx+12)+'" y1="'+(cy+126)+'" x2="'+(cx+cw-12)+'" y2="'+(cy+126)+'" stroke="#1f3b28"/>';
  svg+='<text x="'+(cx+15)+'" y="'+(cy+144)+'" fill="#789c80" font-size="8">ANALYTICAL RESOLUTION SCORE</text>';
  svg+='<rect x="'+(cx+15)+'" y="'+(cy+152)+'" width="'+(cw-30)+'" height="8" rx="2" fill="#08140c"/>';
  svg+='<rect x="'+(cx+15)+'" y="'+(cy+152)+'" width="'+((cw-30)*m.bar/100)+'" height="8" rx="2" fill="'+m.col+'"/>';

  svg+='<foreignObject x="'+(cx+12)+'" y="'+(cy+170)+'" width="'+(cw-24)+'" height="68"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:8.5px;color:#a0aec0;line-height:1.4;margin:0">'+m.adv+'</p></foreignObject>';
 });

 svg+=text(360,306,'CIPM Recommendation: Buoyancy correction Δm = m_app · ρ_air · (1/ρ_sample - 1/ρ_weights) is mandatory for 4-decimal precision.','#68d391',9.5);
 return svg;
}

function drawSandboxView(p,rawVal){
 let svg='<rect width="720" height="320" fill="#0b140e"/>';
 const text=(x,y,str,color='#789c80',size=11)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';
 svg+=text(360,24,'THERMODYNAMIC EQUATION OF STATE: WATER DENSITY ANOMALY (0 °C TO 100 °C)','#68d391',12);

 // Density vs Temperature Plot (0 to 100 C)
 const pX=60,pY=50,pW=400,pH=220;
 svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" fill="#061009" stroke="#1f3b28" rx="4"/>';
 // Axes
 const tMin=0,tMax=100,rhoMin=0.95,rhoMax=1.005;
 const mapX=t=>pX+(t-tMin)/(tMax-tMin)*pW;
 const mapY=r=>pY+pH-(r-rhoMin)/(rhoMax-rhoMin)*pH;

 // Grid lines
 [0,20,40,60,80,100].forEach(deg=>{
  svg+='<line x1="'+mapX(deg)+'" y1="'+pY+'" x2="'+mapX(deg)+'" y2="'+(pY+pH)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+mapX(deg)+'" y="'+(pY+pH+14)+'" text-anchor="middle" fill="#789c80" font-size="8.5">'+deg+' °C</text>';
 });
 [0.96,0.98,1.00].forEach(r=>{
  svg+='<line x1="'+pX+'" y1="'+mapY(r)+'" x2="'+(pX+pW)+'" y2="'+mapY(r)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+(pX-6)+'" y="'+(mapY(r)+3)+'" text-anchor="end" fill="#789c80" font-size="8.5">'+r.toFixed(2)+'</text>';
 });

 // Water density curve using Tilton-Taylor formula approximation
 const pts=[];
 for(let deg=0;deg<=100;deg+=1){
  // Polynomial approximation of water density: ρ(T) ≈ 0.99984 + 6.79e-5·T - 9.10e-6·T² + 1.00e-7·T³ - 1.12e-9·T⁴ + 6.53e-12·T⁵
  const t_val=deg;
  const r_val=0.9998395 + 6.79829998e-5*t_val - 9.106025e-6*t_val**2 + 1.0052729e-7*t_val**3 - 1.1267135e-9*t_val**4 + 6.536332e-12*t_val**5;
  pts.push(mapX(t_val).toFixed(1)+','+mapY(r_val).toFixed(1));
 }
 svg+='<polyline points="'+pts.join(' ')+'" fill="none" stroke="#48bb78" stroke-width="2.5"/>';

 // Highlight Density Peak at 3.98 °C
 const xPeak=mapX(3.98),yPeak=mapY(0.99997);
 svg+='<circle cx="'+xPeak+'" cy="'+yPeak+'" r="4.5" fill="#f6e05e" stroke="#142b1a" stroke-width="1.5"/>';
 svg+='<line x1="'+xPeak+'" y1="'+yPeak+'" x2="'+xPeak+'" y2="'+(pY+20)+'" stroke="#f6e05e" stroke-dasharray="3,2"/>';
 svg+='<text x="'+(xPeak+8)+'" y="'+(pY+28)+'" fill="#f6e05e" font-size="8.5" font-weight="bold">MAX DENSITY: 3.98 °C (0.99997 g/mL)</text>';

 // Current Laboratory Operating Point (20.0 °C)
 const xLab=mapX(20.0),yLab=mapY(0.99820);
 svg+='<circle cx="'+xLab+'" cy="'+yLab+'" r="5" fill="#63b3ed" stroke="#142b1a" stroke-width="1.5"/>';
 svg+='<text x="'+(xLab+10)+'" y="'+(yLab-6)+'" fill="#63b3ed" font-size="8.5" font-weight="bold">BENCH TARGET: 20.00 °C (0.99820 g/mL)</text>';

 // Sidebar Explanations (Right Side)
 const sX=480,sY=50,sW=200,sH=220;
 svg+='<rect x="'+sX+'" y="'+sY+'" width="'+sW+'" height="'+sH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+22)+'" text-anchor="middle" fill="#81e6d9" font-size="10" font-weight="bold">STRUCTURAL ANOMALY</text>';
 svg+='<line x1="'+(sX+15)+'" y1="'+(sY+32)+'" x2="'+(sX+sW-15)+'" y2="'+(sY+32)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+50)+'" fill="#f6e05e" font-size="9" font-weight="bold">1. Hydrogen Bond Collapse</text>';
 svg+='<foreignObject x="'+(sX+12)+'" y="'+(sY+56)+'" width="'+(sW-24)+'" height="48"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#a0aec0;line-height:1.35;margin:0">Below 3.98 °C, melting collapses open tetrahedral Ice Ih cages into dense interstitial monomers, increasing ρ.</p></foreignObject>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+115)+'" fill="#68d391" font-size="9" font-weight="bold">2. Thermal Expansion</text>';
 svg+='<foreignObject x="'+(sX+12)+'" y="'+(sY+121)+'" width="'+(sW-24)+'" height="48"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#a0aec0;line-height:1.35;margin:0">Above 3.98 °C, kinetic thermal expansion overwhelms network collapse, causing monotonic density reduction.</p></foreignObject>';

 svg+='<rect x="'+(sX+12)+'" y="'+(sY+176)+'" width="'+(sW-24)+'" height="32" rx="3" fill="#061009" stroke="#1f3b28"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+190)+'" text-anchor="middle" fill="#9ae6b4" font-size="8">Thermal Coefficient β at 20 °C:</text>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+202)+'" text-anchor="middle" fill="#e2e8f0" font-size="9" font-family="monospace">2.07 × 10⁻⁴ K⁻¹</text>';

 svg+=text(360,305,'Tilton-Taylor Thermodynamic Formulation: Pure water density is an international primary measurement standard.','#789c80',9);
 return svg;
}

function drawHydrateBenchView(p,rawVal){
 const m_hyd=p.input;
 const m_wat=measurement?measurement.raw:(busy?rawVal*0.8:rawVal);
 const m_salt=measurement?m_hyd-m_wat:(busy?m_hyd-m_wat:m_hyd*0.63924);
 const isDehydrated=Boolean(measurement);

 let svg='<defs><pattern id="chemGrid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" stroke="#ffffff" stroke-opacity=".03" fill="none"/></pattern>';
 svg+='<linearGradient id="flameInner" x1="0%" y1="100%" x2="0%" y2="0%"><stop offset="0%" stop-color="#93c5fd"/><stop offset="60%" stop-color="#60a5fa"/><stop offset="100%" stop-color="#3b82f6" stop-opacity=".2"/></linearGradient>';
 svg+='<linearGradient id="flameOuter" x1="0%" y1="100%" x2="0%" y2="0%"><stop offset="0%" stop-color="#2563eb" stop-opacity=".7"/><stop offset="100%" stop-color="#1d4ed8" stop-opacity="0"/></linearGradient>';
 svg+='<linearGradient id="crucibleGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#e2e8f0"/><stop offset="30%" stop-color="#ffffff"/><stop offset="80%" stop-color="#f1f5f9"/><stop offset="100%" stop-color="#cbd5e1"/></linearGradient>';
 svg+='<linearGradient id="blueCrystals" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0284c7"/><stop offset="50%" stop-color="#0369a1"/><stop offset="100%" stop-color="#075985"/></linearGradient>';
 svg+='<linearGradient id="whiteSalt" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#f8fafc"/><stop offset="50%" stop-color="#e2e8f0"/><stop offset="100%" stop-color="#cbd5e1"/></linearGradient>';
 svg+='</defs><rect width="720" height="320" fill="#0b140e"/><rect width="720" height="320" fill="url(#chemGrid)"/>';

 // Workbench surface
 svg+='<rect x="0" y="270" width="720" height="50" fill="#132419" stroke="#1f3b28" stroke-width="1"/>';
 svg+='<line x1="0" y1="270" x2="720" y2="270" stroke="#2d523b" stroke-width="2"/>';

 // 1. LEFT STATION: Tirrill Gas Burner & Porcelain Crucible on Ring Stand
 const rBaseX=40,rBaseY=258,rBaseW=120,rBaseH=12;
 svg+='<rect x="'+rBaseX+'" y="'+rBaseY+'" width="'+rBaseW+'" height="'+rBaseH+'" rx="2" fill="#1e293b" stroke="#334155"/>';
 svg+='<rect x="'+(rBaseX+20)+'" y="35" width="8" height="223" fill="#334155" stroke="#475569"/>';
 // Iron Ring
 const ringY=145;
 svg+='<rect x="'+(rBaseX+15)+'" y="'+ringY+'" width="85" height="7" rx="2" fill="#475569"/>';
 svg+='<ellipse cx="'+(rBaseX+85)+'" cy="'+(ringY+3)+'" rx="26" ry="7" fill="none" stroke="#64748b" stroke-width="3"/>';
 // Pipe Clay Triangle
 const cX=rBaseX+85;
 svg+='<polygon points="'+(cX-22)+','+(ringY+2)+' '+(cX+22)+','+(ringY+2)+' '+cX+','+(ringY-14)+'" fill="none" stroke="#e2e8f0" stroke-width="4"/>';

 // Tirrill Burner under Crucible
 const bX=cX-12,bY=205;
 svg+='<rect x="'+(bX-12)+'" y="260" width="48" height="10" rx="3" fill="#334155" stroke="#475569"/>'; // burner base
 svg+='<rect x="'+(bX+7)+'" y="215" width="10" height="45" fill="#64748b" stroke="#475569"/>'; // barrel
 svg+='<circle cx="'+(bX+12)+'" cy="250" r="4" fill="#94a3b8"/>'; // air collar
 // Gas flame
 svg+='<path d="M'+(bX+4)+' 215 Q'+(bX+12)+' '+(ringY+25)+' '+(bX+20)+' 215 Z" fill="url(#flameOuter)"/>';
 svg+='<path d="M'+(bX+7)+' 215 Q'+(bX+12)+' '+(ringY+38)+' '+(bX+17)+' 215 Z" fill="url(#flameInner)"/>';

 // Porcelain Crucible sitting in triangle
 const crucY=ringY-22;
 svg+='<path d="M'+(cX-18)+' '+crucY+' L'+(cX-12)+' '+(crucY+28)+' Q'+cX+' '+(crucY+34)+' '+(cX+12)+' '+(crucY+28)+' L'+(cX+18)+' '+crucY+' Z" fill="url(#crucibleGrad)" stroke="#94a3b8" stroke-width="1.2"/>';
 // Salt inside crucible
 const saltGrad=isDehydrated?'url(#whiteSalt)':'url(#blueCrystals)';
 svg+='<ellipse cx="'+cX+'" cy="'+(crucY+18)+'" rx="12" ry="4" fill="'+saltGrad+'"/>';

 // Crucible Lid (slightly ajar 3 mm to vent steam)
 const lidY=crucY-5;
 svg+='<path d="M'+(cX-20)+' '+(lidY+3)+' L'+(cX+18)+' '+(lidY-4)+' L'+(cX+19)+' '+(lidY-7)+' L'+(cX-19)+' '+(lidY)+' Z" fill="url(#crucibleGrad)" stroke="#94a3b8" stroke-width="1"/>';
 svg+='<circle cx="'+cX+'" cy="'+(lidY-3)+'" r="2.5" fill="#cbd5e1"/>'; // lid handle

 // Steam vapor wisps when busy heating
 if(busy){
  svg+='<path d="M'+(cX+14)+' '+(lidY-8)+' Q'+(cX+20)+' '+(lidY-25)+' '+(cX+10)+' '+(lidY-45)+' T'+(cX+18)+' '+(lidY-75)+'" fill="none" stroke="#e2e8f0" stroke-width="2" stroke-opacity=".6" stroke-dasharray="4,3"/>';
  svg+='<path d="M'+(cX+8)+' '+(lidY-10)+' Q'+(cX+4)+' '+(lidY-30)+' '+(cX+16)+' '+(lidY-55)+' T'+(cX+8)+' '+(lidY-85)+'" fill="none" stroke="#e2e8f0" stroke-width="1.5" stroke-opacity=".4" stroke-dasharray="3,3"/>';
 }
 svg+='<text x="'+cX+'" y="295" text-anchor="middle" fill="#94a3b8" font-size="9" font-weight="bold">CALCINATION (250 °C)</text>';

 // 2. MIDDLE STATION: Vacuum Desiccator
 const dX=250,dY=145,dW=130,dH=125;
 // Desiccator Base
 svg+='<path d="M'+dX+' '+(dY+dH)+' L'+(dX+10)+' '+(dY+dH-30)+' L'+(dX+dW-10)+' '+(dY+dH-30)+' L'+(dX+dW)+' '+(dY+dH)+' Z" fill="#1e293b" stroke="#334155" stroke-width="1.2"/>';
 // Cobalt-blue Drierite Crystals in bottom
 for(let bx=dX+20;bx<dX+dW-20;bx+=10){
  svg+='<circle cx="'+bx+'" cy="'+(dY+dH-12)+'" r="3.5" fill="#1d4ed8"/>';
  svg+='<circle cx="'+(bx+5)+'" cy="'+(dY+dH-7)+'" r="3" fill="#2563eb"/>';
 }
 // Perforated porcelain plate
 svg+='<rect x="'+(dX+10)+'" y="'+(dY+dH-34)+'" width="'+(dW-20)+'" height="5" fill="#e2e8f0" stroke="#94a3b8"/>';
 // Desiccator Glass Dome
 svg+='<path d="M'+(dX+8)+' '+(dY+dH-34)+' Q'+(dX+8)+' '+(dY+20)+' '+(dX+dW/2)+' '+(dY+10)+' Q'+(dX+dW-8)+' '+(dY+20)+' '+(dX+dW-8)+' '+(dY+dH-34)+' Z" fill="#ffffff" fill-opacity=".06" stroke="#475569" stroke-width="1.5"/>';
 // Stopcock valve on top
 svg+='<rect x="'+(dX+dW/2-4)+'" y="'+(dY-2)+'" width="8" height="12" fill="#94a3b8" stroke="#64748b"/>';
 svg+='<circle cx="'+(dX+dW/2)+'" cy="'+(dY-6)+'" r="4.5" fill="#3b82f6"/>';
 // Cooled crucible inside desiccator
 svg+='<path d="M'+(dX+dW/2-12)+' '+(dY+dH-34)+' L'+(dX+dW/2-8)+' '+(dY+dH-52)+' L'+(dX+dW/2+8)+' '+(dY+dH-52)+' L'+(dX+dW/2+12)+' '+(dY+dH-34)+' Z" fill="url(#crucibleGrad)" stroke="#94a3b8"/>';
 svg+='<text x="'+(dX+dW/2)+'" y="295" text-anchor="middle" fill="#60a5fa" font-size="9" font-weight="bold">DESICCATOR COOLING</text>';

 // 3. RIGHT STATION: Electronic Analytical Balance & Live Stoichiometric Telemetry
 const balX=420,balY=115,balW=270,balH=155;
 svg+='<rect x="'+balX+'" y="'+balY+'" width="'+balW+'" height="'+balH+'" rx="6" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<rect x="'+balX+'" y="'+balY+'" width="'+balW+'" height="26" rx="5" fill="#14331e"/>';
 svg+='<text x="'+(balX+balW/2)+'" y="'+(balY+17)+'" text-anchor="middle" fill="#86efac" font-size="10.5" font-weight="bold">ANALYTICAL GRAVIMETRIC TELEMETRY</text>';

 const rows_meta=[
  {lbl:'INITIAL HYDRATE MASS (m_hyd):',val:m_hyd.toFixed(4)+' g',col:'#60a5fa'},
  {lbl:'RECOVERED ANHYDROUS SALT (m_salt):',val:(isDehydrated?m_salt.toFixed(4):'—')+' g',col:'#f8fafc'},
  {lbl:'EVOLVED WATER OF CRYSTALLIZATION:',val:(isDehydrated?m_wat.toFixed(4):'—')+' g',col:'#4ade80'},
  {lbl:'ANHYDROUS MOLES n(CuSO₄):',val:(isDehydrated?(m_salt/159.609).toFixed(5):'—')+' mol',col:'#cbd5e1'},
  {lbl:'WATER MOLES n(H₂O):',val:(isDehydrated?(m_wat/18.0154).toFixed(5):'—')+' mol',col:'#cbd5e1'},
  {lbl:'EMPIRICAL HYDRATION RATIO x:',val:isDehydrated?((m_wat/18.0154)/(m_salt/159.609)).toFixed(4):'5.0000',col:'#fde047'}
 ];

 rows_meta.forEach((item,idx)=>{
  const ry=balY+38+idx*19;
  svg+='<text x="'+(balX+12)+'" y="'+ry+'" fill="#789c80" font-size="8">'+item.lbl+'</text>';
  svg+='<text x="'+(balX+balW-12)+'" y="'+ry+'" text-anchor="end" fill="'+item.col+'" font-size="9" font-family="monospace" font-weight="bold">'+item.val+'</text>';
 });

 svg+='<rect x="'+(balX+10)+'" y="'+(balY+balH-24)+'" width="'+(balW-20)+'" height="18" rx="3" fill="#061209" stroke="#1a3d24"/>';
 svg+='<text x="'+(balX+balW/2)+'" y="'+(balY+balH-12)+'" text-anchor="middle" fill="#86efac" font-size="8.5" font-family="monospace">CuSO₄ · 5 H₂O ⟶ CuSO₄ (s) + 5 H₂O (g)</text>';

 svg+=text(360,22,'GRAVIMETRIC HYDRATE STOICHIOMETRY: THERMAL DESICCATION OF COPPER(II) SULFATE','#86efac',11.5);
 return svg;
}

function drawHydrateCompareView(p,rawVal){
 let svg='<rect width="720" height="320" fill="#0b140e"/>';
 const text=(x,y,str,color='#789c80',size=11)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';
 svg+=text(360,26,'WATER OF CRYSTALLIZATION DETERMINATION: THREE ANALYTICAL TECHNIQUES','#86efac',12);

 const methods=[
  {
   name:'1. Crucible Calcination',
   type:'Classical Thermal Gravimetry',
   prec:'±0.02 mol H₂O',
   sample:'2.0–5.0 g',
   dur:'45–60 min',
   adv:'Simple classical student bench method; requires repeated heating to constant mass to prevent moisture reabsorption.',
   col:'#38a169',
   score:75
  },
  {
   name:'2. Thermogravimetric (TGA)',
   type:'Continuous Microbalance Heating',
   prec:'±0.002 mol H₂O',
   sample:'10–20 mg',
   dur:'30 min',
   adv:'Resolves stepwise intermediate hydrates (trihydrate, monohydrate) via derivative DTG peaks under inert N₂ purge.',
   col:'#3b82f6',
   score:96
  },
  {
   name:'3. Karl Fischer Titration',
   type:'Coulometric Iodine Redox Reaction',
   prec:'±0.0005 mol H₂O',
   sample:'100 mg',
   dur:'5 min',
   adv:'Direct chemical reaction with H₂O: I₂ + SO₂ + CH₃OH + H₂O; operates at room temperature without risk of overheating.',
   col:'#eab308',
   score:98
  }
 ];

 methods.forEach((m,idx)=>{
  const cx=50+idx*215,cy=45,cw=195,ch=245;
  svg+='<rect x="'+cx+'" y="'+cy+'" width="'+cw+'" height="'+ch+'" rx="6" fill="#101e14" stroke="'+m.col+'" stroke-width="1.5"/>';
  svg+='<rect x="'+cx+'" y="'+cy+'" width="'+cw+'" height="28" rx="5" fill="'+m.col+'" fill-opacity=".2"/>';
  svg+='<text x="'+(cx+cw/2)+'" y="'+(cy+18)+'" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="bold">'+m.name+'</text>';
  svg+='<text x="'+(cx+cw/2)+'" y="'+(cy+42)+'" text-anchor="middle" fill="#a0aec0" font-size="8.5">'+m.type+'</text>';
  svg+='<line x1="'+(cx+12)+'" y1="'+(cy+52)+'" x2="'+(cx+cw-12)+'" y2="'+(cy+52)+'" stroke="#1f3b28"/>';

  svg+='<text x="'+(cx+15)+'" y="'+(cy+70)+'" fill="#789c80" font-size="8.5">PRECISION LIMIT:</text>';
  svg+='<text x="'+(cx+cw-15)+'" y="'+(cy+70)+'" text-anchor="end" fill="'+m.col+'" font-size="10" font-family="monospace" font-weight="bold">'+m.prec+'</text>';

  svg+='<text x="'+(cx+15)+'" y="'+(cy+92)+'" fill="#789c80" font-size="8.5">SAMPLE REQUIREMENT:</text>';
  svg+='<text x="'+(cx+cw-15)+'" y="'+(cy+92)+'" text-anchor="end" fill="#e2e8f0" font-size="9" font-family="monospace">'+m.sample+'</text>';

  svg+='<text x="'+(cx+15)+'" y="'+(cy+114)+'" fill="#789c80" font-size="8.5">TOTAL RUN DURATION:</text>';
  svg+='<text x="'+(cx+cw-15)+'" y="'+(cy+114)+'" text-anchor="end" fill="#e2e8f0" font-size="9" font-family="monospace">'+m.dur+'</text>';

  svg+='<line x1="'+(cx+12)+'" y1="'+(cy+126)+'" x2="'+(cx+cw-12)+'" y2="'+(cy+126)+'" stroke="#1f3b28"/>';
  svg+='<text x="'+(cx+15)+'" y="'+(cy+144)+'" fill="#789c80" font-size="8">ANALYTICAL RESOLUTION SCORE</text>';
  svg+='<rect x="'+(cx+15)+'" y="'+(cy+152)+'" width="'+(cw-30)+'" height="8" rx="2" fill="#08140c"/>';
  svg+='<rect x="'+(cx+15)+'" y="'+(cy+152)+'" width="'+((cw-30)*m.score/100)+'" height="8" rx="2" fill="'+m.col+'"/>';

  svg+='<foreignObject x="'+(cx+12)+'" y="'+(cy+170)+'" width="'+(cw-24)+'" height="68"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:8.5px;color:#a0aec0;line-height:1.4;margin:0">'+m.adv+'</p></foreignObject>';
 });

 svg+=text(360,306,'Safety Rule: Never exceed 600 °C during calcination to prevent decomposition of CuSO₄ into black CuO and SO₃ gas.','#86efac',9.5);
 return svg;
}

function drawHydrateSandboxView(p,rawVal){
 let svg='<rect width="720" height="320" fill="#0b140e"/>';
 const text=(x,y,str,color='#789c80',size=11)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" fill="'+color+'" font-size="'+size+'">'+str+'</text>';
 svg+=text(360,24,'THERMOGRAVIMETRIC (TGA) STEPWISE DEHYDRATION PROFILE: CuSO₄ · 5 H₂O','#86efac',12);

 // TGA Curve Plot (X: Temp 0 to 750 C; Y: Mass % remaining 100% to 20%)
 const pX=60,pY=50,pW=400,pH=220;
 svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" fill="#061009" stroke="#1f3b28" rx="4"/>';
 const mapX=t=>pX+(t/750)*pW;
 const mapY=pct=>pY+pH-((pct-20)/85)*pH;

 // TGA step curve coordinates
 const tgaSteps=[
  [25,100],[60,100],[95,85.6],[105,85.6],[130,71.2],[200,71.2],[245,63.9],[600,63.9],[680,31.8],[750,31.8]
 ];
 const pts=tgaSteps.map(pair=>mapX(pair[0]).toFixed(1)+','+mapY(pair[1]).toFixed(1));
 svg+='<polyline points="'+pts.join(' ')+'" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';

 // Grid labels
 [100,200,300,400,500,600,700].forEach(deg=>{
  svg+='<line x1="'+mapX(deg)+'" y1="'+pY+'" x2="'+mapX(deg)+'" y2="'+(pY+pH)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+mapX(deg)+'" y="'+(pY+pH+14)+'" text-anchor="middle" fill="#789c80" font-size="8.5">'+deg+' °C</text>';
 });
 [40,60,80,100].forEach(pct=>{
  svg+='<line x1="'+pX+'" y1="'+mapY(pct)+'" x2="'+(pX+pW)+'" y2="'+mapY(pct)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+(pX-6)+'" y="'+(mapY(pct)+3)+'" text-anchor="end" fill="#789c80" font-size="8.5">'+pct+'%</text>';
 });

 // Labels on Plateaus
 svg+='<text x="'+(mapX(75))+'" y="'+(mapY(85.6)-6)+'" text-anchor="middle" fill="#fde047" font-size="7.5">−2 H₂O (Trihydrate)</text>';
 svg+='<text x="'+(mapX(160))+'" y="'+(mapY(71.2)-6)+'" text-anchor="middle" fill="#fde047" font-size="7.5">−2 H₂O (Monohydrate)</text>';
 svg+='<text x="'+(mapX(400))+'" y="'+(mapY(63.9)-7)+'" text-anchor="middle" fill="#86efac" font-size="8.5" font-weight="bold">ANHYDROUS CuSO₄ (63.9%)</text>';
 svg+='<text x="'+(mapX(700))+'" y="'+(mapY(31.8)-6)+'" text-anchor="middle" fill="#ef4444" font-size="7.5">CuO residue (31.8%)</text>';

 // Right Sidebar: Crystal Field & Structural Coordination
 const sX=480,sY=50,sW=200,sH=220;
 svg+='<rect x="'+sX+'" y="'+sY+'" width="'+sW+'" height="'+sH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+20)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">COORDINATION SPHERE</text>';
 svg+='<line x1="'+(sX+15)+'" y1="'+(sY+28)+'" x2="'+(sX+sW-15)+'" y2="'+(sY+28)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+46)+'" fill="#60a5fa" font-size="9" font-weight="bold">Equatorial Ligands (4 H₂O)</text>';
 svg+='<foreignObject x="'+(sX+12)+'" y="'+(sY+50)+'" width="'+(sW-24)+'" height="45"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#a0aec0;line-height:1.35;margin:0">4 water molecules coordinate equatorially to Cu²⁺ with short bonds (1.97 Å); split d-orbitals produce azure blue color.</p></foreignObject>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+108)+'" fill="#fde047" font-size="9" font-weight="bold">Bridging Water (5th H₂O)</text>';
 svg+='<foreignObject x="'+(sX+12)+'" y="'+(sY+112)+'" width="'+(sW-24)+'" height="45"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#a0aec0;line-height:1.35;margin:0">Held by 4 hydrogen bonds between sulfate anions and coordinated waters; released only above 200 °C.</p></foreignObject>';

 svg+='<rect x="'+(sX+12)+'" y="'+(sY+170)+'" width="'+(sW-24)+'" height="38" rx="3" fill="#061209" stroke="#1f3b28"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+185)+'" text-anchor="middle" fill="#86efac" font-size="8">Hydration Exothermicity:</text>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+198)+'" text-anchor="middle" fill="#f8fafc" font-size="8.5" font-family="monospace">ΔH_hyd = −78.2 kJ/mol</text>';

 svg+=text(360,305,'TGA Thermogravimetry: Stepwise mass plateaus isolate discrete stoichiometric intermediate hydrate phases.','#789c80',9);
 return svg;
}

update();
renderResults();

// ======================================================================
// CHEMISTRY LAB 03: LIMITING REACTANTS & GRAVIMETRIC PRECIPITATION
// ======================================================================
function drawLimitingBenchView(p,rawVal){
 const v=p.input;
 const m_ppt=rawVal;
 let svg='<defs>';
 svg+='<linearGradient id="flaskGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ffffff" stop-opacity=".15"/><stop offset="30%" stop-color="#ffffff" stop-opacity=".05"/><stop offset="80%" stop-color="#38bdf8" stop-opacity=".08"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".2"/></linearGradient>';
 svg+='<linearGradient id="buretteGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#bae6fd" stop-opacity=".3"/><stop offset="50%" stop-color="#e0f2fe" stop-opacity=".1"/><stop offset="100%" stop-color="#bae6fd" stop-opacity=".35"/></linearGradient>';
 svg+='<linearGradient id="pptCake" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#f8fafc"/><stop offset="50%" stop-color="#e2e8f0"/><stop offset="100%" stop-color="#cbd5e1"/></linearGradient>';
 svg+='<linearGradient id="heatPlate" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#334155"/><stop offset="100%" stop-color="#0f172a"/></linearGradient>';
 svg+='<filter id="glow"><feGaussianBlur stdDeviation="2" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';
 svg+='</defs>';

 // Background bench layout
 svg+='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+='<line x1="20" y1="280" x2="700" y2="280" stroke="#1f3b28" stroke-width="2"/>';

 // Header banner
 svg+=text(360,20,'GRAVIMETRIC PRECIPITATION & VACUUM FILTRATION: Ba²⁺(aq) + SO₄²⁻(aq) ⟶ BaSO₄(s)↓','#86efac',11);

 // 1. LEFT STATION: Precision Burette & Heated Digestion Reaction
 const bX=110,bY=32;
 svg+='<rect x="'+(bX-45)+'" y="30" width="5" height="250" fill="#64748b"/>';
 svg+='<rect x="'+(bX-65)+'" y="276" width="45" height="6" rx="2" fill="#475569"/>';
 svg+='<rect x="'+(bX-45)+'" y="80" width="40" height="6" fill="#94a3b8"/>';
 svg+='<circle cx="'+(bX-5)+'" cy="83" r="5" fill="#cbd5e1"/>';

 // Glass Burette
 svg+='<rect x="'+(bX-7)+'" y="'+bY+'" width="14" height="130" fill="url(#buretteGrad)" stroke="#7dd3fc" stroke-width="1.2"/>';
 const menY=bY+15+(v/24.0)*85;
 svg+='<rect x="'+(bX-6)+'" y="'+menY+'" width="12" height="'+(bY+130-menY)+'" fill="#0284c7" fill-opacity=".35"/>';
 svg+='<path d="M'+(bX-6)+' '+menY+' Q'+bX+' '+(menY+3)+' '+(bX+6)+' '+menY+'" fill="none" stroke="#38bdf8" stroke-width="1.2"/>';
 for(let gy=bY+15;gy<=bY+120;gy+=10){
  svg+='<line x1="'+(bX+1)+'" y1="'+gy+'" x2="'+(bX+6)+'" y2="'+gy+'" stroke="#bae6fd" stroke-width="0.8"/>';
 }
 svg+='<polygon points="'+(bX-7)+','+(bY+130)+' '+(bX+7)+','+(bY+130)+' '+(bX+3)+','+(bY+144)+' '+(bX-3)+','+(bY+144)+'" fill="#cbd5e1"/>';
 svg+='<rect x="'+(bX-8)+'" y="'+(bY+134)+'" width="16" height="5" rx="1.5" fill="#ef4444"/>';
 svg+='<line x1="'+bX+'" y1="'+(bY+144)+'" x2="'+bX+'" y2="'+(bY+154)+'" stroke="#7dd3fc" stroke-width="1.5"/>';

 if(busy){
  svg+='<circle cx="'+bX+'" cy="'+(bY+162)+'" r="2" fill="#38bdf8" filter="url(#glow)"/>';
  svg+='<circle cx="'+bX+'" cy="'+(bY+172)+'" r="1.5" fill="#38bdf8"/>';
 }

 // Hotplate Magnetic Stirrer
 const hpX=bX-50,hpY=240,hpW=100,hpH=38;
 svg+='<rect x="'+hpX+'" y="'+hpY+'" width="'+hpW+'" height="'+hpH+'" rx="4" fill="url(#heatPlate)" stroke="#475569" stroke-width="1.2"/>';
 svg+='<rect x="'+(hpX+6)+'" y="'+(hpY+8)+'" width="36" height="20" rx="2" fill="#020617" stroke="#1e293b"/>';
 svg+='<text x="'+(hpX+24)+'" y="'+(hpY+22)+'" text-anchor="middle" fill="#ef4444" font-size="8" font-family="monospace">85.0°C</text>';
 svg+='<circle cx="'+(hpX+60)+'" cy="'+(hpY+18)+'" r="7" fill="#64748b"/>';
 svg+='<text x="'+(hpX+80)+'" y="'+(hpY+22)+'" text-anchor="middle" fill="#86efac" font-size="7">300 rpm</text>';

 // Reaction Beaker
 const bkX=bX-35,bkY=175,bkW=70,bkH=65;
 svg+='<rect x="'+bkX+'" y="'+bkY+'" width="'+bkW+'" height="'+bkH+'" rx="2" fill="url(#flaskGrad)" stroke="#94a3b8" stroke-width="1.2"/>';
 const liqH=42;
 svg+='<rect x="'+(bkX+1)+'" y="'+(bkY+bkH-liqH)+'" width="'+(bkW-2)+'" height="'+liqH+'" fill="#0284c7" fill-opacity=".15"/>';
 for(let i=0;i<18;i++){
  const px=bkX+8+(i*13)%(bkW-16);
  const py=bkY+bkH-8-((i*17)%(liqH-12));
  svg+='<circle cx="'+px+'" cy="'+py+'" r="1.8" fill="#f8fafc" fill-opacity=".85"/>';
 }
 svg+='<rect x="'+(bX-10)+'" y="'+(bkY+bkH-7)+'" width="20" height="5" rx="2.5" fill="#f1f5f9" stroke="#94a3b8"/>';
 svg+='<text x="'+bX+'" y="295" text-anchor="middle" fill="#94a3b8" font-size="9" font-weight="bold">1. DIGESTION BEAKER (85 °C)</text>';

 // 2. MIDDLE STATION: Vacuum Buchner / Gooch Filtration Manifold
 const fX=330,fY=150;
 svg+='<path d="M'+(fX-14)+' '+(fY+24)+' L'+(fX-12)+' '+(fY+45)+' L'+(fX-42)+' '+(fY+120)+' Q'+fX+' '+(fY+126)+' '+(fX+42)+' '+(fY+120)+' L'+(fX+12)+' '+(fY+45)+' L'+(fX+14)+' '+(fY+24)+' Z" fill="url(#flaskGrad)" stroke="#64748b" stroke-width="1.2"/>';
 svg+='<line x1="'+(fX+12)+'" y1="'+(fY+42)+'" x2="'+(fX+28)+'" y2="'+(fY+38)+'" stroke="#64748b" stroke-width="4"/>';
 svg+='<path d="M'+(fX+28)+' '+(fY+38)+' Q'+(fX+50)+' '+(fY+32)+' '+(fX+65)+' '+(fY+70)+'" fill="none" stroke="#d97706" stroke-width="3.5" stroke-linecap="round"/>';
 svg+='<text x="'+(fX+75)+'" y="'+(fY+65)+'" fill="#fbbf24" font-size="7.5">VACUUM (−20 kPa)</text>';

 svg+='<polygon points="'+(fX-15)+','+(fY+22)+' '+(fX+15)+','+(fY+22)+' '+(fX+12)+','+(fY+32)+' '+(fX-12)+','+(fY+32)+'" fill="#020617" stroke="#334155"/>';

 const crX=fX-18,crY=fY-14,crW=36,crH=36;
 svg+='<path d="M'+crX+' '+crY+' L'+(crX+4)+' '+(crY+crH)+' L'+(crX+crW-4)+' '+(crY+crH)+' L'+(crX+crW)+' '+crY+' Z" fill="#1e293b" stroke="#94a3b8" stroke-width="1.2"/>';
 svg+='<line x1="'+(crX+5)+'" y1="'+(crY+crH-8)+'" x2="'+(crX+crW-5)+'" y2="'+(crY+crH-8)+'" stroke="#64748b" stroke-dasharray="2,1.5" stroke-width="2"/>';
 const cakeH=3+(v/24.0)*8;
 svg+='<rect x="'+(crX+6)+'" y="'+(crY+crH-8-cakeH)+'" width="'+(crW-12)+'" height="'+cakeH+'" fill="url(#pptCake)" rx="1.5"/>';
 svg+='<rect x="'+(fX-3.5)+'" y="'+(crY+crH)+'" width="7" height="35" fill="url(#buretteGrad)" stroke="#7dd3fc" stroke-width="0.8"/>';

 svg+='<path d="M'+(fX-34)+' '+(fY+105)+' Q'+fX+' '+(fY+110)+' '+(fX+34)+' '+(fY+105)+' L'+(fX+40)+' '+(fY+118)+' Q'+fX+' '+(fY+125)+' '+(fX-40)+' '+(fY+118)+' Z" fill="#38bdf8" fill-opacity=".25"/>';

 const ttX=fX+75,ttY=fY+110;
 svg+='<rect x="'+ttX+'" y="'+ttY+'" width="14" height="45" rx="7" fill="url(#flaskGrad)" stroke="#94a3b8"/>';
 svg+='<rect x="'+(ttX+1.5)+'" y="'+(ttY+18)+'" width="11" height="24" rx="5" fill="#38bdf8" fill-opacity=".2"/>';
 svg+='<text x="'+(ttX+7)+'" y="'+(ttY+32)+'" text-anchor="middle" fill="#4ade80" font-size="6.5" font-weight="bold">AgNO₃ ✓</text>';
 svg+='<text x="'+(ttX+7)+'" y="'+(ttY+62)+'" text-anchor="middle" fill="#86efac" font-size="7">0.0 ppm Cl⁻</text>';

 svg+='<text x="'+fX+'" y="295" text-anchor="middle" fill="#60a5fa" font-size="9" font-weight="bold">2. GOOCH VACUUM FILTRATION</text>';

 // 3. RIGHT STATION: 4-Decimal Analytical Balance
 const abX=540,abY=120,abW=145,abH=150;
 svg+='<rect x="'+abX+'" y="'+abY+'" width="'+abW+'" height="'+abH+'" rx="4" fill="#0f172a" fill-opacity=".7" stroke="#334155" stroke-width="1.5"/>';
 svg+='<rect x="'+(abX+5)+'" y="'+(abY+5)+'" width="'+(abW-10)+'" height="85" fill="#ffffff" fill-opacity=".04" stroke="#475569" stroke-width="1"/>';
 const panX=abX+abW/2;
 svg+='<rect x="'+(panX-25)+'" y="'+(abY+70)+'" width="50" height="4" fill="#e2e8f0" stroke="#94a3b8"/>';
 svg+='<rect x="'+(panX-3)+'" y="'+(abY+74)+'" width="6" height="16" fill="#64748b"/>';

 const cbX=panX-14,cbY=abY+45;
 svg+='<path d="M'+cbX+' '+cbY+' L'+(cbX+3)+' '+(cbY+25)+' L'+(cbX+25)+' '+(cbY+25)+' L'+(cbX+28)+' '+cbY+' Z" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>';
 svg+='<rect x="'+(cbX+5)+' " y="'+(cbY+16)+'" width="18" height="7" fill="url(#pptCake)" rx="1"/>';

 const conY=abY+95;
 svg+='<rect x="'+(abX+10)+'" y="'+conY+'" width="'+(abW-20)+'" height="'+(abH-105)+'" rx="3" fill="#020617" stroke="#1e293b"/>';
 svg+='<rect x="'+(abX+16)+'" y="'+(conY+6)+'" width="'+(abW-32)+'" height="24" rx="2" fill="#061c10" stroke="#14532d"/>';
 const dispText=m_ppt>0?m_ppt.toFixed(4)+' g':'0.0000 g';
 svg+='<text x="'+(abX+abW-22)+'" y="'+(conY+23)+'" text-anchor="end" fill="#4ade80" font-size="12" font-family="monospace" font-weight="bold">'+dispText+'</text>';
 svg+='<text x="'+(abX+20)+'" y="'+(conY+14)+'" fill="#15803d" font-size="6">TARE NET</text>';

 svg+='<text x="'+(abX+20)+'" y="'+(conY+38)+'" fill="#94a3b8" font-size="7">Product: BaSO₄ (dry)</text>';
 svg+='<text x="'+(abX+abW-20)+'" y="'+(conY+38)+'" text-anchor="end" fill="#86efac" font-size="7">Yield: 100.0%</text>';

 svg+='<text x="'+panX+'" y="295" text-anchor="middle" fill="#4ade80" font-size="9" font-weight="bold">3. ANALYTICAL BALANCE (±0.1 mg)</text>';

 svg+=text(360,312,'Quantitative Metathesis: Limiting SO₄²⁻ governs isolated dry BaSO₄ mass. All excess Ba²⁺ remains dissolved.','#789c80',8.5);
 return svg;
}

function drawLimitingCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'ANALYTICAL METROLOGY COMPARISON: QUANTITATIVE SULFATE DETERMINATION','#86efac',12);

 const cards=[
  {
   title:'1. Gravimetric Precipitation',
   sub:'Classical Absolute Primary Method',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Principle: Ba²⁺ + SO₄²⁻ ⟶ BaSO₄(s)↓',
    'Mass isolated via sintered glass Gooch crucible',
    'Primary method: No calibration standards needed',
    'Analytical Precision: ±0.0001 g (±0.1 mg)',
    'Dynamic Range: 10 mg to 5.0 g sulfate',
    'Analysis Time: 90–120 minutes (digestion/drying)',
    'Systematic Biases: Coprecipitation, slight K_sp loss'
   ]
  },
  {
   title:'2. Turbidimetric Titration',
   sub:'Optical Rayleigh-Gans Scattering',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Principle: 90° light scattering by micro-crystallites',
    'Optical scatter intensity: I_scatter ∝ [SO₄²⁻]',
    'Secondary method: Requires matrix-matched calibration',
    'Analytical Precision: ±1.5% to ±3.0% RSD',
    'Dynamic Range: 1.0 mg/L to 40 mg/L (ppm)',
    'Analysis Time: 1 to 3 minutes per sample',
    'Systematic Biases: Particle ripening, stirring speed'
   ]
  },
  {
   title:'3. ICP-OES Emission',
   sub:'Inductively Coupled Argon Plasma',
   color:'#fde047',
   border:'#5a4814',
   items:[
    'Principle: Atomic emission lines (S: 180.7 nm, Ba: 455.4 nm)',
    'Thermal atomization & ionization at 7000–8000 K',
    'Instrumental method: Multi-element calibration curve',
    'Analytical Precision: ±0.5% to ±1.0% RSD',
    'Dynamic Range: 5 μg/L to 100 mg/L (ppb to ppm)',
    'Analysis Time: 30 seconds per injection',
    'Systematic Biases: Plasma drift, spectral interferences'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Classical gravimetry provides absolute primary SI traceability without calibration curve drift.','#789c80',9);
 return svg;
}

function drawLimitingSandboxView(p,rawVal){
 const v=p.input;
 const m_ppt=rawVal;
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'STOICHIOMETRIC RESPONSE & EQUIVALENCE PLATEAU: Ba²⁺ + SO₄²⁻ ⟶ BaSO₄↓','#86efac',12);

 // Left Plot: Precipitate mass vs added Na2SO4 volume (0 to 40 mL)
 const pX=55,pY=48,pW=420,pH=225;
 svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" fill="#061209" stroke="#1f3b28" rx="4"/>';

 const mapX=vol=>pX+(vol/40.0)*pW;
 const mapY=mass=>pY+pH-(mass/0.85)*pH;

 // Draw Equivalence zone line at V = 30.0 mL (3.00 mmol)
 const eqX=mapX(30.0);
 svg+='<line x1="'+eqX+'" y1="'+pY+'" x2="'+eqX+'" y2="'+(pY+pH)+'" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,3"/>';
 svg+='<text x="'+eqX+'" y="'+(pY+15)+'" text-anchor="middle" fill="#ef4444" font-size="8" font-weight="bold">EQUIVALENCE POINT (V = 30.0 mL)</text>';

 // Linear stoichiometric line (0 to 30 mL) and plateau line (30 to 40 mL)
 const p0=[mapX(0),mapY(0)];
 const pEq=[mapX(30.0),mapY(0.7002)];
 const pEnd=[mapX(40.0),mapY(0.7002)];
 svg+='<polyline points="'+p0[0]+','+p0[1]+' '+pEq[0]+','+pEq[1]+' '+pEnd[0]+','+pEnd[1]+'" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';

 // Grid lines & labels
 [10,20,30,40].forEach(vol=>{
  svg+='<line x1="'+mapX(vol)+'" y1="'+pY+'" x2="'+mapX(vol)+'" y2="'+(pY+pH)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+mapX(vol)+'" y="'+(pY+pH+14)+'" text-anchor="middle" fill="#789c80" font-size="8.5">'+vol+' mL</text>';
 });
 [0.2,0.4,0.6,0.8].forEach(mass=>{
  svg+='<line x1="'+pX+'" y1="'+mapY(mass)+'" x2="'+(pX+pW)+'" y2="'+mapY(mass)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+(pX-6)+'" y="'+(mapY(mass)+3)+'" text-anchor="end" fill="#789c80" font-size="8.5">'+mass.toFixed(1)+' g</text>';
 });

 // Shaded regimes
 svg+='<text x="'+(pX+110)+'" y="'+(pY+pH-40)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">SULFATE LIMITING (Linear)</text>';
 svg+='<text x="'+(pX+110)+'" y="'+(pY+pH-28)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">m = 0.02334 · V_SO₄</text>';
 svg+='<text x="'+(eqX+45)+'" y="'+(mapY(0.7002)-10)+'" text-anchor="middle" fill="#fde047" font-size="8.5" font-weight="bold">BARIUM LIMITING (Plateau)</text>';
 svg+='<text x="'+(eqX+45)+'" y="'+(mapY(0.7002)+14)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">m_max = 0.7002 g</text>';

 // Active current operating point
 const curX=mapX(v);
 const curY=mapY(m_ppt);
 svg+='<circle cx="'+curX+'" cy="'+curY+'" r="6" fill="#4ade80" stroke="#08140c" stroke-width="2"/>';
 svg+='<circle cx="'+curX+'" cy="'+curY+'" r="9" fill="none" stroke="#4ade80" stroke-width="1.2" stroke-opacity=".6"/>';
 svg+='<line x1="'+curX+'" y1="'+curY+'" x2="'+curX+'" y2="'+(pY+pH)+'" stroke="#4ade80" stroke-dasharray="2,2"/>';

 // Right Sidebar: Stoichiometric Balance & Baryte Crystallography
 const sX=490,sY=48,sW=205,sH=225;
 svg+='<rect x="'+sX+'" y="'+sY+'" width="'+sW+'" height="'+sH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">STOICHIOMETRIC STATUS</text>';
 svg+='<line x1="'+(sX+15)+'" y1="'+(sY+25)+'" x2="'+(sX+sW-15)+'" y2="'+(sY+25)+'" stroke="#1f3b28"/>';

 const n_SO4=(0.1000*v);
 const n_Ba_init=3.000;
 const n_Ba_rem=Math.max(0,n_Ba_init-n_SO4);
 svg+='<text x="'+(sX+12)+'" y="'+(sY+42)+'" fill="#94a3b8" font-size="8">Initial Ba²⁺ Aliquot: 3.000 mmol</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+57)+'" fill="#38bdf8" font-size="8">Delivered SO₄²⁻: '+n_SO4.toFixed(3)+' mmol</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+72)+'" fill="#fde047" font-size="8">Excess Ba²⁺ in soln: '+n_Ba_rem.toFixed(3)+' mmol</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+87)+'" fill="#4ade80" font-size="8">Precipitated BaSO₄: '+n_SO4.toFixed(3)+' mmol</text>';

 svg+='<rect x="'+(sX+10)+'" y="'+(sY+98)+'" width="'+(sW-20)+'" height="32" rx="3" fill="#061209" stroke="#1f3b28"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+112)+'" text-anchor="middle" fill="#86efac" font-size="7.5">Limiting Reagent Condition:</text>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+124)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-family="monospace">SO₄²⁻ IS LIMITING (100% Yield)</text>';

 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+148)+'" text-anchor="middle" fill="#86efac" font-size="9" font-weight="bold">BARYTE LATTICE (Pnma)</text>';
 svg+='<foreignObject x="'+(sX+10)+'" y="'+(sY+154)+'" width="'+(sW-20)+'" height="60"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7px;color:#a0aec0;line-height:1.3;margin:0">BaSO₄ crystallizes in the orthorhombic baryte structure where each Ba²⁺ cation is coordinated by 12 oxygen atoms from neighboring tetrahedral SO₄²⁻ anions, providing immense thermodynamic lattice enthalpy (ΔH_lat = −2469 kJ/mol) and insoluble stability.</p></foreignObject>';

 svg+=text(360,305,'Sandbox: Beyond 30.0 mL, Ba²⁺ becomes limiting and precipitate mass plateaus at 0.7002 g.','#789c80',9);
 return svg;
}

// ======================================================================
// CHEMISTRY LAB 04: MOLAR VOLUME OF AN IDEAL GAS (EUDIOMETRY)
// ======================================================================
function drawGasBenchView(p,rawVal){
 const m_mg=p.input;
 const v_stp=rawVal;
 // Raw experimental volume at 20 C and P_H2 = 742.46 mmHg
 const v_exp=(v_stp * (760.0 / 742.46) * (293.15 / 273.15));

 let svg='<defs>';
 svg+='<linearGradient id="eudioGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#bae6fd" stop-opacity=".35"/><stop offset="30%" stop-color="#ffffff" stop-opacity=".1"/><stop offset="70%" stop-color="#38bdf8" stop-opacity=".15"/><stop offset="100%" stop-color="#bae6fd" stop-opacity=".4"/></linearGradient>';
 svg+='<linearGradient id="waterCyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#0284c7" stop-opacity=".25"/><stop offset="50%" stop-color="#38bdf8" stop-opacity=".12"/><stop offset="100%" stop-color="#0284c7" stop-opacity=".3"/></linearGradient>';
 svg+='<linearGradient id="gasZone" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#f8fafc" stop-opacity=".25"/><stop offset="100%" stop-color="#38bdf8" stop-opacity=".08"/></linearGradient>';
 svg+='<linearGradient id="copperCage" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#f59e0b"/><stop offset="50%" stop-color="#b45309"/><stop offset="100%" stop-color="#78350f"/></linearGradient>';
 svg+='</defs>';

 // Background bench layout
 svg+='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+='<line x1="20" y1="280" x2="700" y2="280" stroke="#1f3b28" stroke-width="2"/>';

 // Header banner
 svg+=text(360,20,'EUDIOMETRIC GAS DISPLACEMENT: Mg(s) + 2 HCl(aq) ⟶ MgCl₂(aq) + H₂(g)↑','#86efac',11);

 // -------------------------------------------------------------
 // 1. LEFT STATION: Microbalance & Magnesium Ribbon Preparation
 // -------------------------------------------------------------
 const mbX=40,mbY=135,mbW=140,mbH=140;
 svg+='<rect x="'+mbX+'" y="'+mbY+'" width="'+mbW+'" height="'+mbH+'" rx="4" fill="#0f172a" fill-opacity=".7" stroke="#334155" stroke-width="1.2"/>';
 svg+='<rect x="'+(mbX+5)+'" y="'+(mbY+5)+'" width="'+(mbW-10)+'" height="75" fill="#ffffff" fill-opacity=".04" stroke="#475569" stroke-width="1"/>';

 // Weighing pan & boat
 const panX=mbX+mbW/2;
 svg+='<rect x="'+(panX-22)+'" y="'+(mbY+62)+'" width="44" height="3.5" fill="#e2e8f0" stroke="#94a3b8"/>';
 svg+='<rect x="'+(panX-2.5)+'" y="'+(mbY+65)+'" width="5" height="15" fill="#64748b"/>';
 // Polished Magnesium Ribbon in Copper Cage
 svg+='<path d="M'+(panX-12)+' '+(mbY+52)+' Q'+(panX-6)+' '+(mbY+44)+' '+panX+' '+(mbY+52)+' Q'+(panX+6)+' '+(mbY+60)+' '+(panX+12)+' '+(mbY+52)+'" fill="none" stroke="#f59e0b" stroke-width="2"/>';
 svg+='<rect x="'+(panX-6)+'" y="'+(mbY+48)+'" width="12" height="6" rx="1.5" fill="#e2e8f0" stroke="#94a3b8"/>'; // Mg strip

 // Balance console
 const cY=mbY+86;
 svg+='<rect x="'+(mbX+8)+'" y="'+cY+'" width="'+(mbW-16)+'" height="46" rx="3" fill="#020617" stroke="#1e293b"/>';
 svg+='<rect x="'+(mbX+14)+'" y="'+(cY+6)+'" width="'+(mbW-28)+'" height="20" rx="2" fill="#061c10" stroke="#14532d"/>';
 svg+='<text x="'+(mbX+mbW-18)+'" y="'+(cY+20)+'" text-anchor="end" fill="#4ade80" font-size="11" font-family="monospace" font-weight="bold">'+(m_mg/1000.0).toFixed(5)+' g</text>';
 svg+='<text x="'+(mbX+18)+'" y="'+(cY+13)+'" fill="#15803d" font-size="6">Mg TARE</text>';
 svg+='<text x="'+panX+'" y="'+(cY+38)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">m_Mg = '+m_mg.toFixed(1)+' mg</text>';

 svg+='<text x="'+panX+'" y="295" text-anchor="middle" fill="#94a3b8" font-size="9" font-weight="bold">1. MICROBALANCE (±0.01 mg)</text>';

 // -------------------------------------------------------------
 // 2. CENTER STATION: Tall-Form Leveling Cylinder & Eudiometer
 // -------------------------------------------------------------
 const eX=340,eY=35;
 // Tall-Form Water Leveling Cylinder (1000 mL)
 const cylX=eX-60,cylY=70,cylW=120,cylH=205;
 svg+='<rect x="'+cylX+'" y="'+cylY+'" width="'+cylW+'" height="'+cylH+'" rx="4" fill="url(#waterCyl)" stroke="#38bdf8" stroke-width="1.5"/>';
 svg+='<rect x="'+(cylX-8)+'" y="'+(cylY+cylH-6)+'" width="'+(cylW+16)+'" height="10" rx="3" fill="#1e293b" stroke="#475569"/>'; // base
 // Water in leveling jar
 const waterLevelY=cylY+45;
 svg+='<rect x="'+(cylX+2)+'" y="'+waterLevelY+'" width="'+(cylW-4)+'" height="'+(cylH-47)+'" fill="#0284c7" fill-opacity=".2"/>';
 svg+='<line x1="'+cylX+'" y1="'+waterLevelY+'" x2="'+(cylX+cylW)+'" y2="'+waterLevelY+'" stroke="#38bdf8" stroke-width="1.5"/>';

 // Eudiometer Tube (Inverted 50 mL burette)
 const eudW=26,eudH=220;
 const eudTop=eY+10;
 // Outer glass wall
 svg+='<rect x="'+(eX-eudW/2)+'" y="'+eudTop+'" width="'+eudW+'" height="'+eudH+'" rx="6" fill="url(#eudioGrad)" stroke="#7dd3fc" stroke-width="1.2"/>';

 // Gas space at top of inverted tube (proportional to v_exp)
 const gasH=20+(v_exp/50.0)*135;
 const gasBottom=eudTop+gasH;
 svg+='<rect x="'+(eX-eudW/2+1)+'" y="'+eudTop+'" width="'+(eudW-2)+'" height="'+gasH+'" fill="url(#gasZone)" rx="5"/>';
 // Inverted meniscus (concave downward)
 svg+='<path d="M'+(eX-eudW/2+1)+' '+gasBottom+' Q'+eX+' '+(gasBottom-4)+' '+(eX+eudW/2-1)+' '+gasBottom+'" fill="#0284c7" fill-opacity=".3" stroke="#38bdf8" stroke-width="1.5"/>';

 // Leveling indicator line showing Δh = 0 (Internal Meniscus == External Meniscus)
 svg+='<line x1="'+(cylX-25)+'" y1="'+gasBottom+'" x2="'+(cylX+cylW+25)+'" y2="'+gasBottom+'" stroke="#4ade80" stroke-width="1.2" stroke-dasharray="3,2"/>';
 svg+='<text x="'+(cylX+cylW+28)+'" y="'+(gasBottom+3)+'" fill="#4ade80" font-size="7.5" font-weight="bold">MENISCUS LEVEL (Δh = 0)</text>';

 // Eudiometer graduations
 for(let gy=eudTop+15;gy<eudTop+eudH-30;gy+=8){
  svg+='<line x1="'+(eX+eudW/2-6)+'" y1="'+gy+'" x2="'+(eX+eudW/2-1)+'" y2="'+gy+'" stroke="#ffffff" stroke-opacity=".7" stroke-width="0.8"/>';
 }
 svg+='<text x="'+(eX+eudW/2-8)+'" y="'+(gasBottom-6)+'" text-anchor="end" fill="#f8fafc" font-size="8" font-family="monospace">'+v_exp.toFixed(1)+' mL</text>';

 // Effervescent bubbles ascending if busy
 if(busy){
  for(let bi=0;bi<12;bi++){
   const bx=eX-6+(bi*7)%12;
   const by=gasBottom+10+(bi*15);
   svg+='<circle cx="'+bx+'" cy="'+by+'" r="1.8" fill="#f8fafc" fill-opacity=".9"/>';
  }
 }

 // Copper wire cage at bottom orifice of eudiometer
 const cageY=eudTop+eudH-25;
 svg+='<path d="M'+(eX-8)+' '+cageY+' Q'+eX+' '+(cageY-6)+' '+(eX+8)+' '+cageY+' Q'+eX+' '+(cageY+6)+' '+(eX-8)+' '+cageY+'" fill="none" stroke="url(#copperCage)" stroke-width="2"/>';
 svg+='<rect x="'+(eX-4)+'" y="'+(cageY-3)+'" width="8" height="6" rx="1" fill="#cbd5e1"/>'; // dissolving Mg strip
 svg+='<line x1="'+eX+'" y1="'+(cageY+6)+'" x2="'+eX+'" y2="'+(eudTop+eudH+5)+'" stroke="#b45309" stroke-width="1.5"/>'; // copper tail

 // One-hole rubber stopper at tube mouth
 svg+='<polygon points="'+(eX-eudW/2-2)+','+(eudTop+eudH)+' '+(eX+eudW/2+2)+','+(eudTop+eudH)+' '+(eX+eudW/2-1)+','+(eudTop+eudH+15)+' '+(eX-eudW/2+1)+','+(eudTop+eudH+15)+'" fill="#020617" stroke="#334155"/>';

 svg+='<text x="'+eX+'" y="295" text-anchor="middle" fill="#60a5fa" font-size="9" font-weight="bold">2. LEVELING CYLINDER (Δh = 0)</text>';

 // -------------------------------------------------------------
 // 3. RIGHT STATION: Fortin Barometer & NIST Thermometer Station
 // -------------------------------------------------------------
 const barX=520,barY=60,barW=175,barH=215;
 svg+='<rect x="'+barX+'" y="'+barY+'" width="'+barW+'" height="'+barH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(barX+barW/2)+'" y="'+(barY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">GAS METROLOGY TELEMETRY</text>';
 svg+='<line x1="'+(barX+12)+'" y1="'+(barY+25)+'" x2="'+(barX+barW-12)+'" y2="'+(barY+25)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+44)+'" fill="#94a3b8" font-size="8">Barometer P_atm:</text>';
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+44)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">760.00 mmHg</text>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+60)+'" fill="#94a3b8" font-size="8">Bath Temp T_water:</text>';
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+60)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">20.00 °C (293.15 K)</text>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+76)+'" fill="#38bdf8" font-size="8">P_H₂O* (Antoine):</text>';
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+76)+'" text-anchor="end" fill="#38bdf8" font-size="8.5" font-family="monospace">17.54 mmHg</text>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+92)+'" fill="#4ade80" font-size="8">P_dry (H₂):</text>';
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+92)+'" text-anchor="end" fill="#4ade80" font-size="8.5" font-family="monospace">742.46 mmHg</text>';

 svg+='<line x1="'+(barX+12)+'" y1="'+(barY+102)+'" x2="'+(barX+barW-12)+'" y2="'+(barY+102)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+118)+'" fill="#94a3b8" font-size="8">Raw Volume V_exp:</text>';
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+118)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">'+v_exp.toFixed(2)+' mL</text>';

 svg+='<rect x="'+(barX+10)+'" y="'+(barY+128)+'" width="'+(barW-20)+'" height="32" rx="3" fill="#061209" stroke="#1f3b28"/>';
 svg+='<text x="'+(barX+barW/2)+'" y="'+(barY+142)+'" text-anchor="middle" fill="#86efac" font-size="7.5">Standardized Volume at STP:</text>';
 svg+='<text x="'+(barX+barW/2)+'" y="'+(barY+154)+'" text-anchor="middle" fill="#4ade80" font-size="9" font-family="monospace" font-weight="bold">'+v_stp.toFixed(3)+' mL H₂</text>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+176)+'" fill="#94a3b8" font-size="7.5">Moles Generated n(H₂):</text>';
 const n_moles=(m_mg/1000.0/24.305);
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+176)+'" text-anchor="end" fill="#86efac" font-size="8" font-family="monospace">'+(n_moles*1000).toFixed(3)+' mmol</text>';

 svg+='<text x="'+(barX+14)+'" y="'+(barY+192)+'" fill="#94a3b8" font-size="7.5">Instantaneous V_m:</text>';
 const inst_vm=v_stp/1000.0/n_moles;
 svg+='<text x="'+(barX+barW-14)+'" y="'+(barY+192)+'" text-anchor="end" fill="#fde047" font-size="8" font-family="monospace">'+inst_vm.toFixed(3)+' L/mol</text>';

 svg+='<text x="'+(barX+barW/2)+'" y="295" text-anchor="middle" fill="#4ade80" font-size="9" font-weight="bold">3. STP REDUCTION TELEMETRY</text>';

 svg+=text(360,312,'Dalton Gas Law: P_dry = P_atm − P_H₂O*(T). Internal and external water surfaces leveled to eliminate Δh head.','#789c80',8.5);
 return svg;
}

function drawGasCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'COMPARATIVE ANALYTICAL METROLOGY: GAS VOLUME & MOLAR MASS DETERMINATION','#86efac',12);

 const cards=[
  {
   title:'1. Eudiometry Displacement',
   sub:'Acid-Metal Gas Evolution over Water',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Principle: Stoichiometric metal dissolution (Mg + 2HCl ⟶ H₂)',
    'Measurement: Gas volume collected in Class A eudiometer',
    'Corrections: Dalton vapor pressure + hydrostatic head',
    'Precision: ±0.05 mL (±0.2% relative volumetric error)',
    'Dynamic Range: 5 to 50 mL gas evolution',
    'Primary advantage: Simple direct absolute stoichiometry',
    'Limitation: Saturated water vapor, trace gas solubility'
   ]
  },
  {
   title:'2. Dumas Vapor Density',
   sub:'Condensation of Vaporized Volatiles',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Principle: Volatilization in boiling water bath (100 °C)',
    'Measurement: Mass of condensed vapor filling bulb of volume V',
    'Formula: M = (m · R · T) / (P · V)',
    'Precision: ±0.5% to ±1.5% molar mass accuracy',
    'Applicability: Volatile liquids (bp 40 °C to 90 °C)',
    'Primary advantage: Determines unknown molecular weight',
    'Limitation: Premature condensation, vapor non-ideality'
   ]
  },
  {
   title:'3. Gas Chromatography (TCD)',
   sub:'Thermal Conductivity Gas Analysis',
   color:'#fde047',
   border:'#5a4814',
   items:[
    'Principle: Differential thermal conductivity detector (TCD)',
    'Helium/Argon carrier gas across heated tungsten filament',
    'Calibration: Multi-point certified calibration gas mixtures',
    'Precision: ±0.1% to ±0.5% RSD',
    'Detection Limits: 10 ppm to 100% composition',
    'Primary advantage: Simultaneous multi-gas separation',
    'Limitation: Expensive capital equipment, carrier gases'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Eudiometry directly connects macroscopic reactant mass to microscopic Avogadro mole volume.','#789c80',9);
 return svg;
}

function drawGasSandboxView(p,rawVal){
 const m_mg=p.input;
 const v_stp=rawVal;
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'GAS THERMODYNAMICS & REAL-GAS INTERMOLECULAR FORCES','#86efac',12);

 // Left Plot: STP Volume vs Magnesium Mass (0 to 40 mg)
 const pX=55,pY=48,pW=400,pH=225;
 svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" fill="#061209" stroke="#1f3b28" rx="4"/>';

 const mapX=m=>pX+(m/40.0)*pW;
 const mapY=v=>pY+pH-(v/40.0)*pH;

 // Linear ideal gas response line
 const x0=mapX(0),y0=mapY(0);
 const xEnd=mapX(40.0),yEnd=mapY(40.0*0.922197);
 svg+='<line x1="'+x0+'" y1="'+y0+'" x2="'+xEnd+'" y2="'+yEnd+'" stroke="#38bdf8" stroke-width="2.5"/>';

 // Grid lines & labels
 [10,20,30,40].forEach(m=>{
  svg+='<line x1="'+mapX(m)+'" y1="'+pY+'" x2="'+mapX(m)+'" y2="'+(pY+pH)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+mapX(m)+'" y="'+(pY+pH+14)+'" text-anchor="middle" fill="#789c80" font-size="8.5">'+m+' mg</text>';
 });
 [10,20,30,40].forEach(v=>{
  svg+='<line x1="'+pX+'" y1="'+mapY(v)+'" x2="'+(pX+pW)+'" y2="'+mapY(v)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+(pX-6)+'" y="'+(mapY(v)+3)+'" text-anchor="end" fill="#789c80" font-size="8.5">'+v+' mL</text>';
 });

 // Current operating point
 const curX=mapX(m_mg);
 const curY=mapY(v_stp);
 svg+='<circle cx="'+curX+'" cy="'+curY+'" r="6" fill="#4ade80" stroke="#08140c" stroke-width="2"/>';
 svg+='<circle cx="'+curX+'" cy="'+curY+'" r="9" fill="none" stroke="#4ade80" stroke-width="1.2" stroke-opacity=".6"/>';
 svg+='<line x1="'+curX+'" y1="'+curY+'" x2="'+curX+'" y2="'+(pY+pH)+'" stroke="#4ade80" stroke-dasharray="2,2"/>';
 svg+='<text x="'+(curX+10)+'" y="'+(curY-8)+'" fill="#86efac" font-size="8.5" font-family="monospace">V_STP = '+v_stp.toFixed(3)+' mL</text>';

 // Right Sidebar: Real Gas Virial / van der Waals Comparison
 const sX=475,sY=48,sW=220,sH=225;
 svg+='<rect x="'+sX+'" y="'+sY+'" width="'+sW+'" height="'+sH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">REAL GAS NON-IDEALITY</text>';
 svg+='<line x1="'+(sX+15)+'" y1="'+(sY+25)+'" x2="'+(sX+sW-15)+'" y2="'+(sY+25)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+42)+'" fill="#38bdf8" font-size="8.5" font-weight="bold">Hydrogen (H₂): Z = 1.0006</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+55)+'" fill="#94a3b8" font-size="7.5">a = 0.248 L²·bar/mol², b = 0.0266 L/mol</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+67)+'" fill="#94a3b8" font-size="7.5">Real V_m = 22.428 L/mol (+0.06% offset)</text>';

 svg+='<line x1="'+(sX+12)+'" y1="'+(sY+76)+'" x2="'+(sX+sW-12)+'" y2="'+(sY+76)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+92)+'" fill="#fde047" font-size="8.5" font-weight="bold">Carbon Dioxide (CO₂): Z = 0.9950</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+105)+'" fill="#94a3b8" font-size="7.5">a = 3.640 L²·bar/mol², b = 0.0427 L/mol</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+117)+'" fill="#94a3b8" font-size="7.5">Real V_m = 22.302 L/mol (−0.50% offset)</text>';

 svg+='<line x1="'+(sX+12)+'" y1="'+(sY+126)+'" x2="'+(sX+sW-12)+'" y2="'+(sY+126)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+142)+'" fill="#ef4444" font-size="8.5" font-weight="bold">Ammonia (NH₃): Z = 0.9880</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+155)+'" fill="#94a3b8" font-size="7.5">a = 4.225 L²·bar/mol², b = 0.0371 L/mol</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+167)+'" fill="#94a3b8" font-size="7.5">Real V_m = 22.145 L/mol (−1.20% offset)</text>';

 svg+='<rect x="'+(sX+10)+'" y="'+(sY+178)+'" width="'+(sW-20)+'" height="36" rx="3" fill="#061209" stroke="#1f3b28"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+192)+'" text-anchor="middle" fill="#86efac" font-size="7.5">Conclusion: H₂ is the closest of all</text>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+205)+'" text-anchor="middle" fill="#38bdf8" font-size="8" font-family="monospace">gases to ideal Avogadro behavior.</text>';

 svg+=text(360,305,'Thermodynamics: Repulsive excluded volume slightly exceeds attractive dispersion for H₂ at STP.','#789c80',9);
 return svg;
}

// ======================================================================
// CHEMISTRY LAB 05: DUMAS VAPOR DENSITY METHOD (MOLAR MASS)
// ======================================================================
function drawDumasBenchView(p,rawVal){
 const v_flask=p.input;
 const m_vap=rawVal;
 const rho_vap=(m_vap/v_flask);

 let svg='<defs>';
 svg+='<linearGradient id="boilWater" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#0284c7" stop-opacity=".3"/><stop offset="50%" stop-color="#38bdf8" stop-opacity=".15"/><stop offset="100%" stop-color="#0284c7" stop-opacity=".35"/></linearGradient>';
 svg+='<linearGradient id="flaskGlass" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ffffff" stop-opacity=".2"/><stop offset="25%" stop-color="#ffffff" stop-opacity=".06"/><stop offset="75%" stop-color="#38bdf8" stop-opacity=".1"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".25"/></linearGradient>';
 svg+='<linearGradient id="alumFoil" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#f1f5f9"/><stop offset="50%" stop-color="#94a3b8"/><stop offset="100%" stop-color="#64748b"/></linearGradient>';
 svg+='<linearGradient id="heatPlateDumas" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#334155"/><stop offset="100%" stop-color="#0f172a"/></linearGradient>';
 svg+='<filter id="plumeGlow"><feGaussianBlur stdDeviation="2.5" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';
 svg+='</defs>';

 // Background bench layout
 svg+='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+='<line x1="20" y1="280" x2="700" y2="280" stroke="#1f3b28" stroke-width="2"/>';

 // Header banner
 svg+=text(360,20,'DUMAS VAPOR DENSITY: PV = (m/M)RT ⟹ M = (m·R·T) / (P·V) [CYCLOHEXANE]','#86efac',11);

 // -------------------------------------------------------------
 // 1. LEFT STATION: Boiling Water Bath & Submerged Dumas Bulb
 // -------------------------------------------------------------
 const bX=145,bY=80;
 // Retort Stand & Clamp
 svg+='<rect x="'+(bX-85)+'" y="30" width="5" height="250" fill="#64748b"/>';
 svg+='<rect x="'+(bX-105)+'" y="276" width="45" height="6" rx="2" fill="#475569"/>';
 svg+='<rect x="'+(bX-85)+'" y="75" width="80" height="6" fill="#94a3b8"/>'; // clamp rod
 svg+='<circle cx="'+(bX-5)+'" cy="78" r="5" fill="#cbd5e1"/>'; // boss head
 // Clamp jaws grasping flask neck
 svg+='<path d="M'+(bX-14)+' 90 Q'+(bX-5)+' 84 '+bX+' 90" fill="none" stroke="#ef4444" stroke-width="4"/>';
 svg+='<path d="M'+bX+' 90 Q'+(bX+5)+' 84 '+(bX+14)+' 90" fill="none" stroke="#ef4444" stroke-width="4"/>';

 // Hotplate
 const hpX=bX-65,hpY=245,hpW=130,hpH=35;
 svg+='<rect x="'+hpX+'" y="'+hpY+'" width="'+hpW+'" height="'+hpH+'" rx="4" fill="url(#heatPlateDumas)" stroke="#475569" stroke-width="1.2"/>';
 svg+='<rect x="'+(hpX+8)+'" y="'+(hpY+8)+'" width="42" height="18" rx="2" fill="#020617" stroke="#1e293b"/>';
 svg+='<text x="'+(hpX+29)+'" y="'+(hpY+21)+'" text-anchor="middle" fill="#ef4444" font-size="8.5" font-family="monospace">100.0°C</text>';
 svg+='<circle cx="'+(hpX+75)+'" cy="'+(hpY+17)+'" r="6" fill="#64748b"/>';
 svg+='<text x="'+(hpX+102)+'" y="'+(hpY+21)+'" text-anchor="middle" fill="#86efac" font-size="7.5">BOIL</text>';

 // 2000 mL Tall Pyrex Beaker Water Bath
 const bkX=bX-55,bkY=115,bkW=110,bkH=130;
 svg+='<rect x="'+bkX+'" y="'+bkY+'" width="'+bkW+'" height="'+bkH+'" rx="3" fill="url(#boilWater)" stroke="#94a3b8" stroke-width="1.5"/>';
 // Boiling water level (near top)
 const boilTop=bkY+20;
 svg+='<rect x="'+(bkX+2)+'" y="'+boilTop+'" width="'+(bkW-4)+'" height="'+(bkH-22)+'" fill="#0284c7" fill-opacity=".2"/>';
 svg+='<line x1="'+bkX+'" y1="'+boilTop+'" x2="'+(bkX+bkW)+'" y2="'+boilTop+'" stroke="#38bdf8" stroke-width="1.2"/>';
 // Boiling bubbles
 for(let bi=0;bi<14;bi++){
  const bx=bkX+12+(bi*13)%(bkW-24);
  const by=bkY+bkH-10-((bi*19)%(bkH-35));
  svg+='<circle cx="'+bx+'" cy="'+by+'" r="2" fill="#ffffff" fill-opacity=".7"/>';
 }

 // Submerged Dumas Bulb (Erlenmeyer / bulb form)
 const flW=46,flH=95;
 const flTop=bkY+5;
 svg+='<path d="M'+(bX-8)+' '+flTop+' L'+(bX-8)+' '+(flTop+35)+' L'+(bX-flW/2)+' '+(flTop+flH)+' Q'+bX+' '+(flTop+flH+6)+' '+(bX+flW/2)+' '+(flTop+flH)+' L'+(bX+8)+' '+(flTop+35)+' L'+(bX+8)+' '+flTop+' Z" fill="url(#flaskGlass)" stroke="#e0f2fe" stroke-width="1.2"/>';

 // Aluminum foil cap with pinhole
 svg+='<polygon points="'+(bX-12)+','+(flTop-4)+' '+(bX+12)+','+(flTop-4)+' '+(bX+10)+','+(flTop+8)+' '+(bX-10)+','+(flTop+8)+'" fill="url(#alumFoil)" stroke="#475569"/>';
 svg+='<circle cx="'+bX+'" cy="'+(flTop-4)+'" r="1.2" fill="#020617"/>'; // pinhole

 // Vapor venting jet / plume from pinhole if busy
 if(busy){
  svg+='<path d="M'+bX+' '+(flTop-6)+' Q'+(bX-6)+' '+(flTop-25)+' '+(bX+4)+' '+(flTop-45)+' T'+(bX-2)+' '+(flTop-65)+'" fill="none" stroke="#f8fafc" stroke-width="2" stroke-opacity=".8" filter="url(#plumeGlow)"/>';
  svg+='<path d="M'+(bX+2)+' '+(flTop-6)+' Q'+(bX+8)+' '+(flTop-20)+' '+(bX-4)+' '+(flTop-40)+'" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-opacity=".6"/>';
 }
 svg+='<text x="'+(bX+18)+'" y="'+(flTop-15)+'" fill="#38bdf8" font-size="7.5">0.5 mm Pinhole</text>';

 svg+='<text x="'+bX+'" y="295" text-anchor="middle" fill="#94a3b8" font-size="9" font-weight="bold">1. BOILING WATER BATH (100.0 °C)</text>';

 // -------------------------------------------------------------
 // 2. CENTER STATION: Water Pycnometry Calibration
 // -------------------------------------------------------------
 const pycX=350,pycY=125;
 svg+='<rect x="'+(pycX-40)+'" y="'+pycY+'" width="80" height="120" rx="4" fill="#0f172a" fill-opacity=".6" stroke="#334155" stroke-width="1.2"/>';
 // Calibrated flask filled with water to brim
 svg+='<path d="M'+(pycX-7)+' '+(pycY+20)+' L'+(pycX-7)+' '+(pycY+40)+' L'+(pycX-25)+' '+(pycY+105)+' Q'+pycX+' '+(pycY+110)+' '+(pycX+25)+' '+(pycY+105)+' L'+(pycX+7)+' '+(pycY+40)+' L'+(pycX+7)+' '+(pycY+20)+' Z" fill="url(#boilWater)" stroke="#7dd3fc" stroke-width="1.2"/>';
 // Flat ground glass optical plate shearing meniscus
 svg+='<rect x="'+(pycX-15)+'" y="'+(pycY+17)+'" width="30" height="3" fill="#cbd5e1" stroke="#94a3b8"/>';
 svg+='<text x="'+pycX+'" y="'+(pycY+12)+'" text-anchor="middle" fill="#38bdf8" font-size="7">Optical Flat Plate</text>';
 svg+='<text x="'+pycX+'" y="'+(pycY+70)+'" text-anchor="middle" fill="#f8fafc" font-size="8.5" font-family="monospace">'+v_flask.toFixed(1)+' mL</text>';
 svg+='<text x="'+pycX+'" y="'+(pycY+82)+'" text-anchor="middle" fill="#94a3b8" font-size="7">±0.02 mL (Pycnometry)</text>';

 svg+='<text x="'+pycX+'" y="295" text-anchor="middle" fill="#60a5fa" font-size="9" font-weight="bold">2. VOLUME PYCNOMETRY</text>';

 // -------------------------------------------------------------
 // 3. RIGHT STATION: Analytical Balance & Condensed Vapor Telemetry
 // -------------------------------------------------------------
 const abX=490,abY=95,abW=205,abH=175;
 svg+='<rect x="'+abX+'" y="'+abY+'" width="'+abW+'" height="'+abH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(abX+abW/2)+'" y="'+(abY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">VAPOR DENSITY TELEMETRY</text>';
 svg+='<line x1="'+(abX+12)+'" y1="'+(abY+25)+'" x2="'+(abX+abW-12)+'" y2="'+(abY+25)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(abX+14)+'" y="'+(abY+42)+'" fill="#94a3b8" font-size="8">Bulb Volume V_flask:</text>';
 svg+='<text x="'+(abX+abW-14)+'" y="'+(abY+42)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">'+v_flask.toFixed(1)+' mL</text>';

 svg+='<text x="'+(abX+14)+'" y="'+(abY+57)+'" fill="#94a3b8" font-size="8">Bath Temp T_bath:</text>';
 svg+='<text x="'+(abX+abW-14)+'" y="'+(abY+57)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">100.00 °C (373.15 K)</text>';

 svg+='<text x="'+(abX+14)+'" y="'+(abY+72)+'" fill="#94a3b8" font-size="8">Barometric Pressure P:</text>';
 svg+='<text x="'+(abX+abW-14)+'" y="'+(abY+72)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">1.0000 atm (760.0 mmHg)</text>';

 svg+='<line x1="'+(abX+12)+'" y1="'+(abY+80)+'" x2="'+(abX+abW-12)+'" y2="'+(abY+80)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(abX+14)+'" y="'+(abY+96)+'" fill="#38bdf8" font-size="8">Condensed Vapor m:</text>';
 svg+='<text x="'+(abX+abW-14)+'" y="'+(abY+96)+'" text-anchor="end" fill="#4ade80" font-size="8.5" font-family="monospace">'+m_vap.toFixed(4)+' g</text>';

 svg+='<text x="'+(abX+14)+'" y="'+(abY+111)+'" fill="#94a3b8" font-size="8">Vapor Density ρ_vap:</text>';
 svg+='<text x="'+(abX+abW-14)+'" y="'+(abY+111)+'" text-anchor="end" fill="#f8fafc" font-size="8.5" font-family="monospace">'+rho_vap.toFixed(6)+' g/mL</text>';

 svg+='<rect x="'+(abX+10)+'" y="'+(abY+120)+'" width="'+(abW-20)+'" height="30" rx="3" fill="#061209" stroke="#1f3b28"/>';
 svg+='<text x="'+(abX+abW/2)+'" y="'+(abY+133)+'" text-anchor="middle" fill="#86efac" font-size="7.5">Calculated Molar Mass M:</text>';
 const m_calc=(m_vap*82.0574*373.15)/(1.000*v_flask);
 svg+='<text x="'+(abX+abW/2)+'" y="'+(abY+145)+'" text-anchor="middle" fill="#38bdf8" font-size="9" font-family="monospace" font-weight="bold">'+m_calc.toFixed(2)+' g/mol</text>';

 svg+='<text x="'+(abX+14)+'" y="'+(abY+164)+'" fill="#94a3b8" font-size="7.5">Substance Identification:</text>';
 svg+='<text x="'+(abX+abW-14)+'" y="'+(abY+164)+'" text-anchor="end" fill="#fde047" font-size="8" font-weight="bold">Cyclohexane (C₆H₁₂)</text>';

 svg+='<text x="'+(abX+abW/2)+'" y="295" text-anchor="middle" fill="#4ade80" font-size="9" font-weight="bold">3. ANALYTICAL BALANCE (±0.1 mg)</text>';

 svg+=text(360,312,'Dumas Metrology: Pure vapor fills bulb at T_bath and P_atm. Condensation isolates exact mole mass.','#789c80',8.5);
 return svg;
}

function drawDumasCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'COMPARATIVE ANALYTICAL METROLOGY: MOLECULAR WEIGHT DETERMINATION TECHNIQUES','#86efac',12);

 const cards=[
  {
   title:'1. Dumas Vapor Method',
   sub:'Open Bulb Boiling Bath Gravimetry',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Principle: Vapor sweeps air; bulb filled at T_bath & P_atm',
    'Measurement: Mass of condensed vapor filling bulb of volume V',
    'Formula: M = (m_vapor · R · T) / (P · V)',
    'Precision: ±0.5% to ±1.0% molar mass accuracy',
    'Applicability: Volatile liquids with bp 40 °C to 95 °C',
    'Primary advantage: Classical direct physical gravimetry',
    'Limitation: Saturated vapor near bp exhibits non-ideality'
   ]
  },
  {
   title:'2. Victor Meyer Method',
   sub:'Closed Chamber Air Displacement',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Principle: Fragile sample ampoule dropped into heated tube',
    'Measurement: Displaced air volume collected over water',
    'Formula: M = (m_sample · R · T_room) / (P_dry · V_air)',
    'Precision: ±1.0% to ±2.0% accuracy',
    'Applicability: High-boiling volatiles up to 300 °C (vapor jackets)',
    'Primary advantage: Requires only tiny sample aliquot (~0.1 g)',
    'Limitation: Thermal convection currents, rubber stopper leakage'
   ]
  },
  {
   title:'3. Cryoscopic Osmometry',
   sub:'Freezing-Point Depression Colligative',
   color:'#fde047',
   border:'#5a4814',
   items:[
    'Principle: Colligative freezing point shift: ΔT_f = K_f · m_solute',
    'Measurement: Differential temperature drop via Beckmann sensor',
    'Formula: M = (K_f · w_solute · 1000) / (ΔT_f · W_solvent)',
    'Precision: ±0.2% to ±0.8% with large K_f solvents (camphor)',
    'Applicability: Non-volatile and volatile solutes in solution',
    'Primary advantage: Operates at low temperature, zero vapor loss',
    'Limitation: Solute association/dissociation shifts van\'t Hoff i'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Dumas measures vapor mass directly; Victor Meyer measures displaced air volume.','#789c80',9);
 return svg;
}

function drawDumasSandboxView(p,rawVal){
 const v_flask=p.input;
 const m_vap=rawVal;
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'VAPOR DENSITY LINEARITY & VAN DER WAALS NON-IDEALITY: CYCLOHEXANE (C₆H₁₂)','#86efac',12);

 // Left Plot: Condensed vapor mass vs Flask volume (0 to 420 mL)
 const pX=55,pY=48,pW=390,pH=225;
 svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" fill="#061209" stroke="#1f3b28" rx="4"/>';

 const mapX=vol=>pX+(vol/420.0)*pW;
 const mapY=mass=>pY+pH-(mass/1.20)*pH;

 const x0=mapX(0),y0=mapY(0);
 const xEnd=mapX(420.0),yEnd=mapY(420.0*0.00274859);
 svg+='<line x1="'+x0+'" y1="'+y0+'" x2="'+xEnd+'" y2="'+yEnd+'" stroke="#38bdf8" stroke-width="2.5"/>';

 [100,200,300,400].forEach(vol=>{
  svg+='<line x1="'+mapX(vol)+'" y1="'+pY+'" x2="'+mapX(vol)+'" y2="'+(pY+pH)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+mapX(vol)+'" y="'+(pY+pH+14)+'" text-anchor="middle" fill="#789c80" font-size="8.5">'+vol+' mL</text>';
 });
 [0.3,0.6,0.9,1.2].forEach(mass=>{
  svg+='<line x1="'+pX+'" y1="'+mapY(mass)+'" x2="'+(pX+pW)+'" y2="'+mapY(mass)+'" stroke="#16291c" stroke-width="1"/>';
  svg+='<text x="'+(pX-6)+'" y="'+(mapY(mass)+3)+'" text-anchor="end" fill="#789c80" font-size="8.5">'+mass.toFixed(1)+' g</text>';
 });

 const curX=mapX(v_flask);
 const curY=mapY(m_vap);
 svg+='<circle cx="'+curX+'" cy="'+curY+'" r="6" fill="#4ade80" stroke="#08140c" stroke-width="2"/>';
 svg+='<circle cx="'+curX+'" cy="'+curY+'" r="9" fill="none" stroke="#4ade80" stroke-width="1.2" stroke-opacity=".6"/>';
 svg+='<line x1="'+curX+'" y1="'+curY+'" x2="'+curX+'" y2="'+(pY+pH)+'" stroke="#4ade80" stroke-dasharray="2,2"/>';
 svg+='<text x="'+(curX+10)+'" y="'+(curY-8)+'" fill="#86efac" font-size="8.5" font-family="monospace">m_vap = '+m_vap.toFixed(4)+' g</text>';

 // Right Sidebar: Molecular Chair Conformation & Non-Ideality
 const sX=465,sY=48,sW=235,sH=225;
 svg+='<rect x="'+sX+'" y="'+sY+'" width="'+sW+'" height="'+sH+'" rx="5" fill="#101e14" stroke="#254d33" stroke-width="1.5"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">MOLECULAR THERMODYNAMICS</text>';
 svg+='<line x1="'+(sX+15)+'" y1="'+(sY+25)+'" x2="'+(sX+sW-15)+'" y2="'+(sY+25)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+42)+'" fill="#38bdf8" font-size="8.5" font-weight="bold">Cyclohexane (C₆H₁₂, Chair Form):</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+55)+'" fill="#94a3b8" font-size="7.5">Molar Mass M = 84.161 g/mol, bp = 80.7 °C</text>';
 svg+='<text x="'+(sX+12)+'" y="'+(sY+67)+'" fill="#94a3b8" font-size="7.5">van der Waals a = 23.3 L²·bar/mol², b = 0.144 L/mol</text>';

 svg+='<line x1="'+(sX+12)+'" y1="'+(sY+76)+'" x2="'+(sX+sW-12)+'" y2="'+(sY+76)+'" stroke="#1f3b28"/>';

 svg+='<text x="'+(sX+12)+'" y="'+(sY+92)+'" fill="#fde047" font-size="8.5" font-weight="bold">Compressibility Factors (Z = PV/nRT):</text>';
 svg+='<text x="'+(sX+14)+'" y="'+(sY+106)+'" fill="#86efac" font-size="7.5">Ideal Gas: Z = 1.0000 ⟹ M = 84.16 g/mol</text>';
 svg+='<text x="'+(sX+14)+'" y="'+(sY+118)+'" fill="#38bdf8" font-size="7.5">Real Cyclohexane at 100 °C: Z = 0.985</text>';
 svg+='<text x="'+(sX+14)+'" y="'+(sY+130)+'" fill="#94a3b8" font-size="7.5">Uncorrected M_apparent = M_true / Z ≈ 85.4 g/mol</text>';

 svg+='<line x1="'+(sX+12)+'" y1="'+(sY+138)+'" x2="'+(sX+sW-12)+'" y2="'+(sY+138)+'" stroke="#1f3b28"/>';

 svg+='<rect x="'+(sX+10)+'" y="'+(sY+146)+'" width="'+(sW-20)+'" height="68" rx="3" fill="#061209" stroke="#1f3b28"/>';
 svg+='<text x="'+(sX+sW/2)+'" y="'+(sY+160)+'" text-anchor="middle" fill="#86efac" font-size="7.5" font-weight="bold">Multi-Point Regression Benefit:</text>';
 svg+='<foreignObject x="'+(sX+14)+'" y="'+(sY+165)+'" width="'+(sW-28)+'" height="46"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7px;color:#a0aec0;line-height:1.25;margin:0">Plotting m_vapor vs V_flask across 6 calibrated bulbs absorbs constant aluminum foil tare errors into the intercept m₀ = 0.0000 g, isolating true vapor density with R² = 1.00000.</p></foreignObject>';

 svg+=text(360,305,'Thermodynamics: Dense organic vapors near condensation exhibit attractive London dispersion (Z < 1).','#789c80',9);
 return svg;
}



// ======================================================================
// CHEMISTRY LAB 06: THE COPPER CYCLE (MASS CONSERVATION)
// ======================================================================
function drawCopperBenchView(p,rawVal){
 const m_init=p.input;
 const m_rec=rawVal;
 const n_moles=m_init/63.546;

 let svg='<defs>';
 svg+='<linearGradient id="cuNitrateGrad" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#10b981" stop-opacity=".7"/><stop offset="100%" stop-color="#059669" stop-opacity=".9"/></linearGradient>';
 svg+='<linearGradient id="cuHydroxideGrad" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#38bdf8" stop-opacity=".8"/><stop offset="100%" stop-color="#0284c7" stop-opacity=".95"/></linearGradient>';
 svg+='<linearGradient id="cuOxideGrad" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#27272a" stop-opacity=".95"/><stop offset="100%" stop-color="#09090b" stop-opacity=".98"/></linearGradient>';
 svg+='<linearGradient id="cuSulfateGrad" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#3b82f6" stop-opacity=".8"/><stop offset="100%" stop-color="#1d4ed8" stop-opacity=".95"/></linearGradient>';
 svg+='<linearGradient id="cuMetalGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#f97316"/><stop offset="50%" stop-color="#ea580c"/><stop offset="100%" stop-color="#9a3412"/></linearGradient>';
 svg+='<linearGradient id="glassWall" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#ffffff" stop-opacity=".2"/><stop offset="10%" stop-color="#ffffff" stop-opacity=".04"/><stop offset="90%" stop-color="#ffffff" stop-opacity=".06"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".25"/></linearGradient>';
 svg+='</defs><rect width="720" height="320" fill="#08140c"/>';

 svg+=text(360,20,'QUANTITATIVE FIVE-STEP CHEMICAL TRANSFORMATION CYCLE: COPPER CONSERVATION','#86efac',12);

 // Table surface
 svg+='<rect x="0" y="275" width="720" height="45" fill="#132419" stroke="#1f3b2a" stroke-width="1"/>';
 svg+='<line x1="0" y1="275" x2="720" y2="275" stroke="#2d523b" stroke-width="2"/>';

 // Draw 5 Reaction Stations
 const stations=[
  {num:'1',label:'HNO₃ Oxidation',formula:'Cu ⟶ Cu(NO₃)₂',color:'#10b981',grad:'url(#cuNitrateGrad)',sub:'Brown NO₂↑ gas'},
  {num:'2',label:'NaOH Metathesis',formula:'Cu²⁺ ⟶ Cu(OH)₂↓',color:'#38bdf8',grad:'url(#cuHydroxideGrad)',sub:'Gelatinous sky blue'},
  {num:'3',label:'Thermal Dehyd.',formula:'Cu(OH)₂ ⟶ CuO↓',color:'#a1a1aa',grad:'url(#cuOxideGrad)',sub:'Granular black at 90°C'},
  {num:'4',label:'H₂SO₄ Leaching',formula:'CuO ⟶ CuSO₄',color:'#60a5fa',grad:'url(#cuSulfateGrad)',sub:'Royal blue solution'},
  {num:'5',label:'Zn Reduction',formula:'Cu²⁺ ⟶ Cu(s)↓',color:'#fb923c',grad:'url(#cuMetalGrad)',sub:'Spongy copper isolated'}
 ];

 stations.forEach((st,idx)=>{
  const bx=20+idx*104,bw=92,by=42,bh=158;
  // Card container
  svg+='<rect x="'+bx+'" y="'+by+'" width="'+bw+'" height="'+bh+'" rx="5" fill="#0b1a10" stroke="#1f3b2a" stroke-width="1.2"/>';
  // Step badge
  svg+='<rect x="'+(bx+6)+'" y="'+(by+6)+'" width="20" height="14" rx="3" fill="#162e1e"/>';
  svg+='<text x="'+(bx+16)+'" y="'+(by+17)+'" text-anchor="middle" fill="#86efac" font-size="9" font-weight="bold">'+st.num+'</text>';
  svg+='<text x="'+(bx+30)+'" y="'+(by+17)+'" fill="#cbd5e1" font-size="8" font-weight="bold">'+st.label+'</text>';
  svg+='<text x="'+(bx+bw/2)+'" y="'+(by+30)+'" text-anchor="middle" fill="'+st.color+'" font-size="7.5" font-family="monospace">'+st.formula+'</text>';

  // Miniature Beaker
  const bkX=bx+18,bkY=by+38,bkW=56,bkH=68;
  svg+='<rect x="'+bkX+'" y="'+bkY+'" width="'+bkW+'" height="'+bkH+'" rx="3" fill="url(#glassWall)" stroke="#4b7055" stroke-width="1"/>';
  // Beaker lip
  svg+='<ellipse cx="'+(bkX+bkW/2)+'" cy="'+bkY+'" rx="'+(bkW/2)+'" ry="3" fill="none" stroke="#789c80" stroke-width="1"/>';
  // Solution / Precipitate inside beaker
  const fillH=idx===2?42:(idx===4?38:46);
  svg+='<rect x="'+(bkX+2)+'" y="'+(bkY+bkH-fillH)+'" width="'+(bkW-4)+'" height="'+fillH+'" rx="2" fill="'+st.grad+'"/>';

  if(idx===0){
   // NO2 gas bubbles / fumes rising
   svg+='<circle cx="'+(bkX+20)+'" cy="'+(bkY+28)+'" r="3.5" fill="#ca8a04" fill-opacity=".8"/>';
   svg+='<circle cx="'+(bkX+36)+'" cy="'+(bkY+18)+'" r="4.5" fill="#b45309" fill-opacity=".7"/>';
   svg+='<circle cx="'+(bkX+28)+'" cy="'+(bkY+8)+'" r="5.5" fill="#9a3412" fill-opacity=".6"/>';
  }else if(idx===1){
   // Gelatinous precipitate flakes
   for(let f=0;f<5;f++){
    svg+='<ellipse cx="'+(bkX+12+f*8)+'" cy="'+(bkY+bkH-12-((f*7)%20))+'" rx="4" ry="2" fill="#7dd3fc" fill-opacity=".9"/>';
   }
  }else if(idx===2){
   // Dense black particles settled + heat waves underneath
   for(let p=0;p<8;p++){
    svg+='<circle cx="'+(bkX+10+p*5)+'" cy="'+(bkY+bkH-6-((p*3)%10))+'" r="2.5" fill="#000000"/>';
   }
   svg+='<path d="M'+(bkX+10)+' '+(bkY+bkH+6)+' Q'+(bkX+18)+' '+(bkY+bkH+2)+' '+(bkX+26)+' '+(bkY+bkH+6)+' Q'+(bkX+34)+' '+(bkY+bkH+10)+' '+(bkX+42)+' '+(bkY+bkH+6)+'" fill="none" stroke="#ef4444" stroke-width="1.5"/>';
  }else if(idx===3){
   // Clear royal blue solution
   svg+='<rect x="'+(bkX+6)+'" y="'+(bkY+bkH-fillH+4)+'" width="6" height="30" fill="#93c5fd" fill-opacity=".4" rx="2"/>';
  }else if(idx===4){
   // Spongy reddish copper cake at bottom + bubbles
   svg+='<rect x="'+(bkX+6)+'" y="'+(bkY+bkH-16)+'" width="'+(bkW-12)+'" height="14" rx="2" fill="url(#cuMetalGrad)"/>';
   svg+='<circle cx="'+(bkX+22)+'" cy="'+(bkY+bkH-22)+'" r="2" fill="#ffffff" fill-opacity=".7"/>';
   svg+='<circle cx="'+(bkX+34)+'" cy="'+(bkY+bkH-30)+'" r="1.8" fill="#ffffff" fill-opacity=".7"/>';
  }

  // Description footer
  svg+='<text x="'+(bx+bw/2)+'" y="'+(by+122)+'" text-anchor="middle" fill="#94a3b8" font-size="7">'+st.sub+'</text>';

  // Status pill
  svg+='<rect x="'+(bx+8)+'" y="'+(by+132)+'" width="'+(bw-16)+'" height="18" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg+='<text x="'+(bx+bw/2)+'" y="'+(by+144)+'" text-anchor="middle" fill="#86efac" font-size="7.5" font-family="monospace">Cu: '+(idx<4?'100% In System':'100% Isolated')+'</text>';

  // Reaction arrow connecting to next station
  if(idx<4){
   svg+='<path d="M'+(bx+bw)+' '+(by+bh/2)+' L'+(bx+bw+12)+' '+(by+bh/2)+'" stroke="#38a169" stroke-width="2" stroke-dasharray="2,2"/>';
   svg+='<polygon points="'+(bx+bw+12)+','+(by+bh/2-3)+' '+(bx+bw+16)+','+(by+bh/2)+' '+(bx+bw+12)+','+(by+bh/2+3)+'" fill="#38a169"/>';
  }
 });

 // Analytical Pan & Quantitative Readout Banner (Bottom)
 const panX=20,panY=210,panW=680,panH=58;
 svg+='<rect x="'+panX+'" y="'+panY+'" width="'+panW+'" height="'+panH+'" rx="6" fill="#0a190e" stroke="#22422c" stroke-width="1.5"/>';

 // Initial mass badge
 svg+='<rect x="'+(panX+15)+'" y="'+(panY+10)+'" width="145" height="38" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(panX+25)+'" y="'+(panY+24)+'" fill="#789c80" font-size="8" font-weight="bold">INITIAL COPPER WIRE</text>';
 svg+='<text x="'+(panX+25)+'" y="'+(panY+40)+'" fill="#f97316" font-size="13" font-family="monospace" font-weight="bold">m₀ = '+m_init.toFixed(4)+' g</text>';

 // Stoichiometric mole conservation
 svg+='<rect x="'+(panX+175)+'" y="'+(panY+10)+'" width="165" height="38" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(panX+185)+'" y="'+(panY+24)+'" fill="#789c80" font-size="8" font-weight="bold">MOLAR QUANTITY [M=63.546]</text>';
 svg+='<text x="'+(panX+185)+'" y="'+(panY+40)+'" fill="#38bdf8" font-size="12" font-family="monospace" font-weight="bold">n(Cu) = '+n_moles.toFixed(5)+' mol</text>';

 // Final recovered mass badge
 svg+='<rect x="'+(panX+355)+'" y="'+(panY+10)+'" width="155" height="38" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(panX+365)+'" y="'+(panY+24)+'" fill="#789c80" font-size="8" font-weight="bold">RECOVERED PURE COPPER</text>';
 svg+='<text x="'+(panX+365)+'" y="'+(panY+40)+'" fill="#86efac" font-size="13" font-family="monospace" font-weight="bold">m_rec = '+m_rec.toFixed(4)+' g</text>';

 // Recovery % & Conservation status
 svg+='<rect x="'+(panX+525)+'" y="'+(panY+10)+'" width="140" height="38" rx="4" fill="#051009" stroke="#22543d"/>';
 svg+='<text x="'+(panX+535)+'" y="'+(panY+24)+'" fill="#86efac" font-size="8" font-weight="bold">STOICHIOMETRIC YIELD</text>';
 svg+='<text x="'+(panX+535)+'" y="'+(panY+40)+'" fill="#48bb78" font-size="13" font-family="monospace" font-weight="bold">Yield = 100.00%</text>';

 svg+=text(360,305,'Conservation Metrology: Cu ⟶ Cu(NO₃)₂ ⟶ Cu(OH)₂ ⟶ CuO ⟶ CuSO₄ ⟶ Cu (100.00% Recovery).','#789c80',8.5);
 return svg;
}

function drawCopperCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'COMPARATIVE EXTRACTIVE & REFINING METALLURGY: COPPER PROCESSING ROUTES','#86efac',12);

 const cards=[
  {
   title:'1. Cyclic Hydrometallurgy',
   sub:'Aqueous Closed Cycle (Our Protocol)',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Principle: Sequential aqueous redox, metathesis & dehydration',
    'Reactions: HNO₃ oxid. ⟶ NaOH ppt ⟶ Dehyd. ⟶ H₂SO₄ ⟶ Zn red.',
    'Energy & Temp: Ambient to 90 °C (low carbon/energy demand)',
    'Theoretical Yield: 100.00% closed-loop stoichiometric conservation',
    'Selectivity: Eliminates iron & zinc via acidic extraction',
    'Primary advantage: Rigorous quantitative proof of mass conservation',
    'Limitation: Multi-step transfers require meticulous wall rinsing'
   ]
  },
  {
   title:'2. Pyrometallurgical Smelting',
   sub:'Flash Furnace Carbothermal Smelting',
   color:'#fb923c',
   border:'#5a3014',
   items:[
    'Principle: High-temperature oxidation of chalcopyrite (CuFeS₂)',
    'Reactions: 2CuFeS₂ + 2.5O₂ ⟶ Cu₂S·FeS (matte) + FeO + 2SO₂',
    'Energy & Temp: 1250 °C to 1350 °C in oxygen-enriched blast furnace',
    'Theoretical Yield: 95% to 98% copper recovered into blister cake',
    'Selectivity: Produces 98.5% crude blister copper (requires refining)',
    'Primary advantage: Massive industrial capacity (millions of tons/yr)',
    'Limitation: Massive SO₂ emissions, slag disposal, huge energy demand'
   ]
  },
  {
   title:'3. Electrolytic Refining',
   sub:'Acidic CuSO₄ Electrorefining (Cathode)',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Principle: Anodic dissolution & cathodic deposition of Cu²⁺ ions',
    'Reactions: Cu(blister anode) ⟶ Cu²⁺ + 2e⁻ ⟶ Cu(pure cathode)',
    'Energy & Temp: 55 °C to 65 °C; electrical power ~300 kWh/ton',
    'Theoretical Yield: >99.5% cathode current efficiency (Faraday's law)',
    'Selectivity: Produces 99.99% Grade A electrolytic copper cathode',
    'Primary advantage: Precious metals (Au, Ag, Pt) drop as anode slime',
    'Limitation: Requires pre-smelted copper anodes and high DC power'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Hydrometallurgy conserves atom mass in closed cycles; Pyrometallurgy processes high-volume ore.','#789c80',9);
 return svg;
}

function drawCopperSandboxView(p,rawVal){
 const m_init=p.input;
 const m_rec=rawVal;
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'MASS CONSERVATION BUDGET & MULTI-STEP REACTION EFFICIENCY: COPPER CYCLE','#86efac',12);

 // Left Plot: Stage-by-Stage Copper Mass Conservation (0 to 5)
 const pX=50,pY=48,pW=395,pH=225;
 svg+='<rect x="'+pX+'" y="'+pY+'" width="'+pW+'" height="'+pH+'" fill="#061209" stroke="#1f3b28" rx="4"/>';

 const stages=['Start (Cu)','Step 1 (NO₃)','Step 2 (OH)','Step 3 (CuO)','Step 4 (SO₄)','Step 5 (Cu)'];
 const barW=36;

 stages.forEach((stg,idx)=>{
  const cx=pX+35+idx*60;
  const h=(m_init/0.80)*170;
  const by=pY+pH-h-25;

  // Background guide line
  svg+='<line x1="'+cx+'" y1="'+pY+'" x2="'+cx+'" y2="'+(pY+pH)+'" stroke="#132418" stroke-width="1"/>';
  // Mass bar
  const col=idx===0?'#f97316':(idx===5?'#48bb78':'#38bdf8');
  svg+='<rect x="'+(cx-barW/2)+'" y="'+by+'" width="'+barW+'" height="'+h+'" rx="3" fill="'+col+'" fill-opacity=".85" stroke="'+col+'" stroke-width="1"/>';
  // Mass label on bar
  svg+='<text x="'+cx+'" y="'+(by-6)+'" text-anchor="middle" fill="#f8fafc" font-size="8" font-family="monospace">'+m_init.toFixed(3)+'g</text>';
  // X axis label
  svg+='<text x="'+cx+'" y="'+(pY+pH-8)+'" text-anchor="middle" fill="#789c80" font-size="7.5">'+stg+'</text>';
 });

 // Conservation boundary line across all bars
 const idealY=pY+pH-((m_init/0.80)*170)-25;
 svg+='<line x1="'+(pX+15)+'" y1="'+idealY+'" x2="'+(pX+pW-15)+'" y2="'+idealY+'" stroke="#facc15" stroke-width="1.8" stroke-dasharray="3,3"/>';
 svg+='<text x="'+(pX+pW-18)+'" y="'+(idealY-4)+'" text-anchor="end" fill="#facc15" font-size="8">100.00% Theoretical Invariant</text>';

 // Right Panel: Systematic Error Sensitivity & Yield Perturbations
 const rX=460,rY=48,rW=235,rH=225;
 svg+='<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="5" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">ANALYTICAL SENSITIVITY AUDIT</text>';

 const errItems=[
  {label:'Residual Zinc Metal (+)',desc:'Unreacted Zn in spongy Cu falsely inflates yield',val:'+2.0% per 10 mg Zn',col:'#f87171'},
  {label:'Transfer Decantation (-)',desc:'Loss of CuO/Cu during decant or beaker wall rinse',val:'-1.0% per 5 mg Cu',col:'#fbbf24'},
  {label:'Surface Oxidation (+)',desc:'Hot drying in air oxidizes Cu ⟶ CuO (+25.2% O)',val:'Prevented by ethanol/desicc.',col:'#38bdf8'},
  {label:'Colloidal Passing (-)',desc:'Cu(OH)₂ bypassing filter paper without dehydration',val:'Prevented by 90°C heating',col:'#a78bfa'},
  {label:'OLS Slope Insulation (★)',desc:'Constant transfer losses absorbed into intercept m₀',val:'Slope = 1.0000 g/g Unbiased',col:'#48bb78'}
 ];

 errItems.forEach((ei,idx)=>{
  const ey=rY+32+idx*38;
  svg+='<rect x="'+(rX+8)+'" y="'+ey+'" width="'+(rW-16)+'" height="32" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+12)+'" fill="'+ei.col+'" font-size="7.5" font-weight="bold">'+ei.label+'</text>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+24)+'" fill="#94a3b8" font-size="6.8">'+ei.desc+'</text>';
  svg+='<text x="'+(rX+rW-14)+'" y="'+(ey+12)+'" text-anchor="end" fill="'+ei.col+'" font-size="7.5" font-family="monospace">'+ei.val+'</text>';
 });

 svg+=text(360,305,'Mass Budget: OLS regression slope m_slope = 1.0000 g/g insulates true stoichiometry against transfer offsets.','#789c80',9);
 return svg;
}


// ======================================================================
// CHEMISTRY LAB 07: EMPIRICAL FORMULA OF MAGNESIUM OXIDE (MgO)
// ======================================================================
function drawMgBenchView(p,rawVal){
 const m_mg=p.input;
 const m_ox=rawVal;
 const m_tot=m_mg+m_ox;
 const n_mg=m_mg/24.305;
 const n_ox=m_ox/15.9994;
 const ratio=n_ox/n_mg;

 let svg='<defs>';
 svg+='<linearGradient id="flameGrad" x1="0%" y1="100%" x2="0%" y2="0%"><stop offset="0%" stop-color="#1e3a8a"/><stop offset="30%" stop-color="#3b82f6"/><stop offset="70%" stop-color="#38bdf8"/><stop offset="100%" stop-color="#fef08a"/></linearGradient>';
 svg+='<linearGradient id="innerCone" x1="0%" y1="100%" x2="0%" y2="0%"><stop offset="0%" stop-color="#0284c7"/><stop offset="100%" stop-color="#a7f3d0"/></linearGradient>';
 svg+='<linearGradient id="porcelainGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#e2e8f0"/><stop offset="25%" stop-color="#ffffff"/><stop offset="75%" stop-color="#cbd5e1"/><stop offset="100%" stop-color="#94a3b8"/></linearGradient>';
 svg+='<linearGradient id="incandescentGlow" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#ffffff"/><stop offset="40%" stop-color="#fef08a"/><stop offset="80%" stop-color="#f97316"/><stop offset="100%" stop-color="#dc2626"/></linearGradient>';
 svg+='<linearGradient id="burnerMetal" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#334155"/><stop offset="50%" stop-color="#64748b"/><stop offset="100%" stop-color="#1e293b"/></linearGradient>';
 svg+='</defs><rect width="720" height="320" fill="#08140c"/>';

 svg+=text(360,20,'CRUCIBLE THERMAL OXIDATION & EMPIRICAL FORMULA DETERMINATION: MAGNESIUM OXIDE (MgO)','#86efac',12);

 // Table surface
 svg+='<rect x="0" y="275" width="720" height="45" fill="#132419" stroke="#1f3b2a" stroke-width="1"/>';
 svg+='<line x1="0" y1="275" x2="720" y2="275" stroke="#2d523b" stroke-width="2"/>';

 // --- LEFT SYSTEM: Meker Burner & High-Form Porcelain Crucible (x = 30 to 340) ---
 // Burner base & barrel
 const bX=175;
 svg+='<rect x="'+(bX-45)+'" y="260" width="90" height="15" rx="3" fill="url(#burnerMetal)" stroke="#0f172a"/>';
 svg+='<rect x="'+(bX-12)+'" y="180" width="24" height="80" fill="url(#burnerMetal)" stroke="#0f172a"/>';
 // Meker burner expanded grid head
 svg+='<path d="M'+(bX-18)+' 180 L'+(bX-26)+' 162 L'+(bX+26)+' 162 L'+(bX+18)+' 180 Z" fill="url(#burnerMetal)" stroke="#0f172a"/>';
 // Grid lines on Meker head
 for(let g=-20;g<=20;g+=8){
  svg+='<line x1="'+(bX+g)+'" y1="162" x2="'+(bX+g)+'" y2="168" stroke="#94a3b8" stroke-width="1"/>';
 }

 // Iron Ring & Clay Pipe Triangle
 svg+='<line x1="'+(bX-75)+'" y1="125" x2="'+(bX+75)+'" y2="125" stroke="#475569" stroke-width="5"/>'; // Iron ring
 // Ceramic clay pipes of triangle
 svg+='<line x1="'+(bX-38)+'" y1="125" x2="'+(bX+38)+'" y2="125" stroke="#e2e8f0" stroke-width="7" stroke-linecap="round"/>';
 svg+='<line x1="'+(bX-38)+'" y1="125" x2="'+bX+'" y2="92" stroke="#e2e8f0" stroke-width="7" stroke-linecap="round"/>';
 svg+='<line x1="'+(bX+38)+'" y1="125" x2="'+bX+'" y2="92" stroke="#e2e8f0" stroke-width="7" stroke-linecap="round"/>';

 // High-temperature Meker flame
 svg+='<path d="M'+(bX-24)+' 162 Q'+(bX-12)+' 120 '+bX+' 95 Q'+(bX+12)+' 120 '+(bX+24)+' 162 Z" fill="url(#flameGrad)" fill-opacity=".85"/>';
 svg+='<path d="M'+(bX-14)+' 162 Q'+(bX-6)+' 136 '+bX+' 118 Q'+(bX+6)+' 136 '+(bX+14)+' 162 Z" fill="url(#innerCone)" fill-opacity=".95"/>';

 // High-Form Porcelain Crucible (seated in clay triangle)
 const cX=bX,cY=68,cW=52,cH=54;
 // Glowing bottom when heating
 svg+='<ellipse cx="'+cX+'" cy="'+(cY+cH)+'" rx="'+(cW/3.2)+'" ry="4" fill="#ef4444" fill-opacity=".9"/>';
 // Crucible body (tapered)
 svg+='<path d="M'+(cX-cW/2)+' '+cY+' L'+(cX-cW/3.2)+' '+(cY+cH)+' Q'+cX+' '+(cY+cH+5)+' '+(cX+cW/3.2)+' '+(cY+cH)+' L'+(cX+cW/2)+' '+cY+' Z" fill="url(#porcelainGrad)" stroke="#64748b" stroke-width="1"/>';
 // Crucible rim lip
 svg+='<ellipse cx="'+cX+'" cy="'+cY+'" rx="'+(cW/2)+'" ry="5" fill="#f8fafc" stroke="#64748b" stroke-width="1"/>';

 // Incandescent magnesium flare / ash inside crucible
 svg+='<ellipse cx="'+cX+'" cy="'+(cY+12)+'" rx="'+(cW/2.4)+'" ry="4" fill="url(#incandescentGlow)"/>';
 if(busy){
  // Active combustion sparks & light rays
  svg+='<circle cx="'+cX+'" cy="'+(cY+8)+'" r="12" fill="#ffffff" fill-opacity=".7"/>';
  svg+='<line x1="'+(cX-18)+'" y1="'+(cY-6)+'" x2="'+(cX+18)+'" y2="'+(cY+22)+'" stroke="#ffffff" stroke-width="1.5"/>';
  svg+='<line x1="'+(cX+18)+'" y1="'+(cY-6)+'" x2="'+(cX-18)+'" y2="'+(cY+22)+'" stroke="#ffffff" stroke-width="1.5"/>';
 }

 // Crucible Lid (tilted / cracked open 1.5 mm to admit O2)
 svg+='<path d="M'+(cX-cW/2-2)+' '+(cY-4)+' L'+(cX+cW/2+4)+' '+(cY-8)+' L'+(cX+cW/2+2)+' '+(cY-12)+' L'+(cX-cW/2-4)+' '+(cY-8)+' Z" fill="url(#porcelainGrad)" stroke="#64748b" stroke-width="1"/>';
 // Lid handle loop
 svg+='<rect x="'+(cX-4)+'" y="'+(cY-15)+'" width="8" height="5" rx="2" fill="url(#porcelainGrad)" stroke="#64748b"/>';
 // Tiny arrow indicating air O2 diffusing into crucible
 svg+='<path d="M'+(cX+cW/2+18)+' '+(cY-18)+' Q'+(cX+cW/2+10)+' '+(cY-8)+' '+(cX+cW/2-2)+' '+(cY-5)+'" fill="none" stroke="#38bdf8" stroke-width="1.5"/>';
 svg+='<text x="'+(cX+cW/2+24)+'" y="'+(cY-16)+'" fill="#38bdf8" font-size="7.5" font-weight="bold">O₂ influx</text>';

 svg+='<rect x="'+(bX-95)+'" y="38" width="190" height="20" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+bX+'" y="52" text-anchor="middle" fill="#86efac" font-size="8.5" font-weight="bold">Meker Flame Calcination: 850 °C</text>';


 // --- RIGHT SYSTEM: Analytical Force Restoration Balance (x = 370 to 690) ---
 const balX=390,balY=95,balW=300,balH=175;
 // Granite anti-vibration base
 svg+='<rect x="'+(balX-10)+'" y="260" width="'+(balW+20)+'" height="15" rx="3" fill="#1e293b" stroke="#0f172a"/>';
 // Main balance enclosure
 svg+='<rect x="'+balX+'" y="'+balY+'" width="'+balW+'" height="'+balH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';

 // Glass Draft Chamber (upper half of balance)
 const dX=balX+15,dY=balY+12,dW=balW-30,dH=98;
 svg+='<rect x="'+dX+'" y="'+dY+'" width="'+dW+'" height="'+dH+'" rx="4" fill="#061209" stroke="#334155" stroke-width="1.2"/>';
 // Stainless steel balance pan
 svg+='<rect x="'+(dX+dW/2-35)+'" y="'+(dY+dH-8)+'" width="70" height="6" rx="2" fill="#94a3b8" stroke="#475569"/>';
 svg+='<rect x="'+(dX+dW/2-5)+'" y="'+(dY+dH-2)+'" width="10" height="8" fill="#64748b"/>';

 // Cooled porcelain crucible on balance pan with snow-white MgO product
 const pX=dX+dW/2,pY=dY+dH-42,pW=36,pH=34;
 svg+='<path d="M'+(pX-pW/2)+' '+pY+' L'+(pX-pW/3.2)+' '+(pY+pH)+' L'+(pX+pW/3.2)+' '+(pY+pH)+' L'+(pX+pW/2)+' '+pY+' Z" fill="url(#porcelainGrad)" stroke="#475569" stroke-width="1"/>';
 svg+='<ellipse cx="'+pX+'" cy="'+pY+'" rx="'+(pW/2)+'" ry="3.5" fill="#f8fafc" stroke="#64748b"/>';
 // White MgO powder cake inside crucible
 svg+='<ellipse cx="'+pX+'" cy="'+(pY+8)+'" rx="'+(pW/2.5)+'" ry="2.8" fill="#ffffff"/>';

 // Balance LCD Display
 const lcdX=balX+25,lcdY=balY+120,lcdW=balW-50,lcdH=42;
 svg+='<rect x="'+lcdX+'" y="'+lcdY+'" width="'+lcdW+'" height="'+lcdH+'" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.5"/>';
 svg+='<circle cx="'+(lcdX+16)+'" cy="'+(lcdY+21)+'" r="4" fill="'+(busy?'#eab308':'#48bb78')+'"/>';
 svg+='<text x="'+(lcdX+26)+'" y="'+(lcdY+17)+'" fill="#789c80" font-size="7.5">STABLE</text>';
 svg+='<text x="'+(lcdX+26)+'" y="'+(lcdY+28)+'" fill="#789c80" font-size="7.5">NET MASS</text>';

 const dispVal=measurement?m_ox.toFixed(4):(busy?(rawVal*0.75).toFixed(4):'0.0000');
 svg+='<text x="'+(lcdX+lcdW-16)+'" y="'+(lcdY+28)+'" text-anchor="end" fill="#86efac" font-size="19" font-family="monospace" font-weight="bold">'+dispVal+' g O</text>';

 // Summary Data Card (Bottom Banner)
 const bannerX=20,bannerY=215,bannerW=340,bannerH=52;
 svg+='<rect x="'+bannerX+'" y="'+bannerY+'" width="'+bannerW+'" height="'+bannerH+'" rx="5" fill="#0a190e" stroke="#22422c"/>';
 svg+='<text x="'+(bannerX+12)+'" y="'+(bannerY+16)+'" fill="#f97316" font-size="8.5" font-weight="bold">m(Mg) = '+m_mg.toFixed(4)+' g  [n = '+n_mg.toFixed(5)+' mol]</text>';
 svg+='<text x="'+(bannerX+12)+'" y="'+(bannerY+31)+'" fill="#38bdf8" font-size="8.5" font-weight="bold">m(O)  = '+m_ox.toFixed(4)+' g  [n = '+n_ox.toFixed(5)+' mol]</text>';
 svg+='<text x="'+(bannerX+12)+'" y="'+(bannerY+45)+'" fill="#86efac" font-size="8.5" font-family="monospace" font-weight="bold">n(O)/n(Mg) = '+ratio.toFixed(4)+' ⟹ Empirical Formula MgO</text>';

 svg+=text(360,305,'Metrology: 2Mg(s) + O₂(g) ⟶ 2MgO(s); Steam hydrolyzes intermediate Mg₃N₂ ⟶ MgO.','#789c80',8.5);
 return svg;
}

function drawMgCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'COMPARATIVE ANALYTICAL STOICHIOMETRY: FORMULA & EQUIVALENT DETERMINATIONS','#86efac',12);

 const cards=[
  {
   title:'1. Crucible Thermal Oxidation',
   sub:'Direct High-Temp Binary Synthesis (Our Lab)',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Analyte: Electropositive metals (Mg ribbon, Cu, Sn)',
    'Principle: Direct combustion with atmospheric oxygen',
    'Reagents: 99.9% Mg ribbon, porcelain crucible, Meker burner',
    'Digestion: Hot steam destroys intermediate Mg₃N₂ ⟶ NH₃↑',
    'Temperature: 850 °C (cherry red calcination to constant mass)',
    'Measurement: Mass gain of bound lattice oxygen (m_oxygen)',
    'Invariant: Slope directly isolates stoichiometric ratio M(O)/M(Mg)'
   ]
  },
  {
   title:'2. Solution Metathesis Ppt.',
   sub:'Aqueous Ionic Double Displacement',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Analyte: Insoluble inorganic salts (BaSO₄, AgCl, PbCrO₄)',
    'Principle: Metathesis precipitation under low supersaturation',
    'Reagents: Standard aqueous salt solutions (e.g., BaCl₂ + Na₂SO₄)',
    'Digestion: 85 °C Ostwald ripening converts colloid to granular',
    'Temperature: 80 °C to 90 °C water bath; Gooch filtration',
    'Measurement: Isolated anhydrous precipitate cake mass',
    'Invariant: Slope isolates formula weight via limiting reactant'
   ]
  },
  {
   title:'3. Dumas Vapor Density',
   sub:'Gas-Phase Molecular Weight Metrology',
   color:'#fde047',
   border:'#5a4814',
   items:[
    'Analyte: Volatile organic liquids (cyclohexane, CCl₄, ethanol)',
    'Principle: Vapor sweeps air; bulb filled at T_bath and P_atm',
    'Reagents: Volatile organic analyte, boiling water bath, barometer',
    'Digestion: Rapid air quenching condenses vapor inside bulb',
    'Temperature: 100.0 °C (boiling water bath immersion)',
    'Measurement: Mass of condensed vapor filling flask volume V',
    'Invariant: Slope isolates ideal gas equation of state molar mass'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Thermal oxidation synthesizes binary solid; Precipitation filters ions; Dumas weighs vapor.','#789c80',9);
 return svg;
}

function drawMgSandboxView(p,rawVal){
 const m_mg=p.input;
 const m_ox=rawVal;
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'STOICHIOMETRIC MECHANISM, NITRIDE HYDROLYSIS & DEFECT AUDIT: MgO','#86efac',12);

 // Left Panel: Rocksalt FCC Lattice & Thermochemical Cycle
 const lX=25,lY=46,lW=340,lH=230;
 svg+='<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">ROCKSALT FCC LATTICE (SPACE GROUP Fm3̄m)</text>';

 // 3D perspective wireframe cube of MgO unit cell
 const ox=lX+80,oy=lY+95,s=70;
 // Back square
 svg+='<rect x="'+(ox+25)+'" y="'+(oy-25)+'" width="'+s+'" height="'+s+'" fill="none" stroke="#1e3a29" stroke-width="1.2"/>';
 // Connecting lines
 svg+='<line x1="'+ox+'" y1="'+oy+'" x2="'+(ox+25)+'" y2="'+(oy-25)+'" stroke="#1e3a29" stroke-width="1.2"/>';
 svg+='<line x1="'+(ox+s)+'" y1="'+oy+'" x2="'+(ox+s+25)+'" y2="'+(oy-25)+'" stroke="#1e3a29" stroke-width="1.2"/>';
 svg+='<line x1="'+ox+'" y1="'+(oy+s)+'" x2="'+(ox+25)+'" y2="'+(oy+s-25)+'" stroke="#1e3a29" stroke-width="1.2"/>';
 svg+='<line x1="'+(ox+s)+'" y1="'+(oy+s)+'" x2="'+(ox+s+25)+'" y2="'+(oy+s-25)+'" stroke="#1e3a29" stroke-width="1.2"/>';
 // Front square
 svg+='<rect x="'+ox+'" y="'+oy+'" width="'+s+'" height="'+s+'" fill="none" stroke="#2d523b" stroke-width="1.5"/>';

 // Corner & edge ions (alternating Mg2+ green, O2- red)
 const ions=[
  {x:ox,y:oy,col:'#48bb78',r:6,label:'Mg²⁺'},
  {x:ox+s/2,y:oy,col:'#ef4444',r:8,label:'O²⁻'},
  {x:ox+s,y:oy,col:'#48bb78',r:6,label:'Mg²⁺'},
  {x:ox,y:oy+s/2,col:'#ef4444',r:8,label:'O²⁻'},
  {x:ox+s/2,y:oy+s/2,col:'#48bb78',r:6,label:'Mg²⁺'},
  {x:ox+s,y:oy+s/2,col:'#ef4444',r:8,label:'O²⁻'},
  {x:ox,y:oy+s,col:'#48bb78',r:6,label:'Mg²⁺'},
  {x:ox+s/2,y:oy+s,col:'#ef4444',r:8,label:'O²⁻'},
  {x:ox+s,y:oy+s,col:'#48bb78',r:6,label:'Mg²⁺'}
 ];
 ions.forEach(i=>{
  svg+='<circle cx="'+i.x+'" cy="'+i.y+'" r="'+i.r+'" fill="'+i.col+'" stroke="#051009" stroke-width="1"/>';
 });

 // Lattice thermochemistry legend
 svg+='<rect x="'+(lX+190)+'" y="'+(lY+38)+'" width="138" height="120" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+52)+'" fill="#789c80" font-size="7.5" font-weight="bold">BORN-HABER THERMODYNAMICS</text>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+67)+'" fill="#cbd5e1" font-size="7">ΔH_sub(Mg) = +148 kJ/mol</text>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+80)+'" fill="#cbd5e1" font-size="7">IE₁ + IE₂  = +2188 kJ/mol</text>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+93)+'" fill="#cbd5e1" font-size="7">½ D(O₂)    = +249 kJ/mol</text>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+106)+'" fill="#cbd5e1" font-size="7">EA₁ + EA₂  = +603 kJ/mol</text>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+120)+'" fill="#38bdf8" font-size="7.5" font-weight="bold">U_lattice  = -3791 kJ/mol</text>';
 svg+='<text x="'+(lX+198)+'" y="'+(lY+134)+'" fill="#86efac" font-size="8" font-weight="bold">ΔH°_f(MgO) = -601.7 kJ/mol</text>';

 svg+='<text x="'+(lX+lW/2)+'" y="'+(lY+215)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">Stoichiometric charge neutrality: 1 Mg²⁺ cation per 1 O²⁻ anion (Coordination Number 6:6)</text>';


 // Right Panel: Systematic Error & Nitride Audit
 const rX=380,rY=46,rW=315,rH=230;
 svg+='<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">NITRIDE DIGESTION & ERROR SENSITIVITY AUDIT</text>';

 const errItems=[
  {label:'Unhydrolyzed Mg₃N₂ (-)',desc:'Omitting water leaves N instead of O (M_N=14 vs M_O=16)',val:'-0.274 g O / g Mg error',col:'#f87171'},
  {label:'Aerosol Smoke Loss (-)',desc:'Escaping white MgO nanoparticles if lid kept open',val:'-2% to -8% mass deficit',col:'#fbbf24'},
  {label:'Glaze Silica Attack (+)',desc:'Basic MgO reacts with porcelain SiO₂ at >900 °C',val:'Minor tare alteration',col:'#38bdf8'},
  {label:'Atmospheric Moisture (+)',desc:'Cooled MgO powder chemisorbs H₂O and CO₂ from air',val:'Prevented by desiccator',col:'#a78bfa'},
  {label:'OLS Slope Insulation (★)',desc:'Constant crucible glaze tare absorbed into intercept m₀',val:'Slope = 0.6582 g/g Unbiased',col:'#48bb78'}
 ];

 errItems.forEach((ei,idx)=>{
  const ey=rY+30+idx*39;
  svg+='<rect x="'+(rX+8)+'" y="'+ey+'" width="'+(rW-16)+'" height="33" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+12)+'" fill="'+ei.col+'" font-size="7.5" font-weight="bold">'+ei.label+'</text>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+25)+'" fill="#94a3b8" font-size="6.8">'+ei.desc+'</text>';
  svg+='<text x="'+(rX+rW-14)+'" y="'+(ey+12)+'" text-anchor="end" fill="'+ei.col+'" font-size="7.5" font-family="monospace">'+ei.val+'</text>';
 });

 svg+=text(360,305,'Formula Verification: Ordinary least-squares regression slope m_slope = 0.65823 g O / g Mg isolations ratio n(O)/n(Mg) = 1.0000.','#789c80',9);
 return svg;
}


// ======================================================================
// CHEMISTRY LAB 08: LIQUID VISCOSITY & POISEUILLE FLOW
// ======================================================================
function drawPoiseuilleBenchView(p,rawVal){
 const h_cm=p.input;
 const q_val=rawVal;
 const dP_pa=998.2*9.80665*(h_cm/100.0);
 const v_mean=(q_val/60.0/1e6)/(Math.PI*Math.pow(0.00025,2));
 const reynolds=(2.0*0.00025*v_mean*998.2)/0.0010020;

 let svg='<defs>';
 svg+='<linearGradient id="waterFlow" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#0284c7" stop-opacity=".7"/><stop offset="50%" stop-color="#38bdf8" stop-opacity=".9"/><stop offset="100%" stop-color="#0284c7" stop-opacity=".7"/></linearGradient>';
 svg+='<linearGradient id="jacketGlass" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#ffffff" stop-opacity=".2"/><stop offset="15%" stop-color="#38bdf8" stop-opacity=".08"/><stop offset="85%" stop-color="#38bdf8" stop-opacity=".12"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".3"/></linearGradient>';
 svg+='<linearGradient id="reservoirGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#ffffff" stop-opacity=".25"/><stop offset="20%" stop-color="#ffffff" stop-opacity=".05"/><stop offset="80%" stop-color="#ffffff" stop-opacity=".08"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".3"/></linearGradient>';
 svg+='</defs><rect width="720" height="320" fill="#08140c"/>';

 svg+=text(360,20,'HAGEN-POISEUILLE CONSTANT-HEAD CAPILLARY VISCOMETER (20.0 °C THERMOSTATED)','#86efac',12);

 // Table surface
 svg+='<rect x="0" y="275" width="720" height="45" fill="#132419" stroke="#1f3b2a" stroke-width="1"/>';
 svg+='<line x1="0" y1="275" x2="720" y2="275" stroke="#2d523b" stroke-width="2"/>';

 // --- 1. Constant-Head Reservoir (Left: x = 30 to 140) ---
 const resX=45,resW=65,resH=180,resY=45;
 svg+='<rect x="'+resX+'" y="'+resY+'" width="'+resW+'" height="'+resH+'" rx="4" fill="url(#reservoirGrad)" stroke="#475569" stroke-width="1.2"/>';

 // Liquid column height in reservoir corresponding to Delta h (cm)
 const hPixels=(h_cm/40.0)*130;
 const liquidY=resY+resH-30-hPixels;
 svg+='<rect x="'+(resX+2)+'" y="'+liquidY+'" width="'+(resW-4)+'" height="'+(resY+resH-liquidY)+'" rx="2" fill="url(#waterFlow)" fill-opacity=".65"/>';
 svg+='<ellipse cx="'+(resX+resW/2)+'" cy="'+liquidY+'" rx="'+(resW/2-2)+'" ry="4" fill="#7dd3fc" fill-opacity=".8"/>';

 // Overflow weir tube on left of reservoir
 svg+='<path d="M'+resX+' '+(liquidY+5)+' L'+(resX-18)+' '+(liquidY+5)+' L'+(resX-18)+' '+(resY+resH)+' L'+(resX-24)+' '+(resY+resH)+'" fill="none" stroke="#64748b" stroke-width="3"/>';
 svg+='<text x="'+(resX-20)+'" y="'+(liquidY)+'" text-anchor="end" fill="#94a3b8" font-size="7">Overflow Weir</text>';

 // Cathetometer height indicator scale
 svg+='<line x1="'+(resX+resW+8)+'" y1="'+(resY+resH-30)+'" x2="'+(resX+resW+8)+'" y2="'+liquidY+'" stroke="#facc15" stroke-width="2"/>';
 svg+='<line x1="'+(resX+resW+4)+'" y1="'+liquidY+'" x2="'+(resX+resW+12)+'" y2="'+liquidY+'" stroke="#facc15" stroke-width="2"/>';
 svg+='<line x1="'+(resX+resW+4)+'" y1="'+(resY+resH-30)+'" x2="'+(resX+resW+12)+'" y2="'+(resY+resH-30)+'" stroke="#facc15" stroke-width="2"/>';
 svg+='<text x="'+(resX+resW+16)+'" y="'+(liquidY+hPixels/2+4)+'" fill="#facc15" font-size="9" font-weight="bold">Δh = '+h_cm.toFixed(1)+' cm</text>';

 // Feed line connecting reservoir bottom to capillary
 svg+='<path d="M'+(resX+resW/2)+' '+(resY+resH)+' L'+(resX+resW/2)+' '+(resY+resH+15)+' L160 '+(resY+resH+15)+' L160 170" fill="none" stroke="#38bdf8" stroke-width="5" stroke-opacity=".8"/>';


 // --- 2. Jacketed Precision Capillary Tube (Center: x = 160 to 490) ---
 const capX=170,capY=162,capW=310,capH=16;
 // Thermostatic Water Jacket (outer cylinder)
 const jX=155,jY=146,jW=340,jH=48;
 svg+='<rect x="'+jX+'" y="'+jY+'" width="'+jW+'" height="'+jH+'" rx="8" fill="url(#jacketGlass)" stroke="#38bdf8" stroke-width="1.5"/>';
 svg+='<text x="'+(jX+jW/2)+'" y="'+(jY-6)+'" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">Water Jacket: 20.0 ± 0.05 °C (Length L = 15.00 cm)</text>';

 // Precision Capillary Tube inside (inner tube)
 svg+='<rect x="'+capX+'" y="'+capY+'" width="'+capW+'" height="'+capH+'" rx="2" fill="url(#reservoirGrad)" stroke="#64748b" stroke-width="1"/>';
 // Flowing liquid stream inside capillary
 svg+='<rect x="'+(capX+1)+'" y="'+(capY+4)+'" width="'+(capW-2)+'" height="'+(capH-8)+'" fill="url(#waterFlow)"/>';

 // Laminar streamline dashes
 if(busy){
  for(let l=0;l<5;l++){
   svg+='<line x1="'+(capX+20+l*55)+'" y1="'+(capY+capH/2)+'" x2="'+(capX+45+l*55)+'" y2="'+(capY+capH/2)+'" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,2"/>';
  }
 }
 svg+='<text x="'+(capX+capW/2)+'" y="'+(capY+capH/2+3)+'" text-anchor="middle" fill="#ffffff" font-size="7.5" font-weight="bold">Radius r = 0.250 mm (Poiseuille Laminar Streamlines)</text>';

 // Jacket circulating coolant ports
 svg+='<rect x="'+(jX+30)+'" y="'+(jY+jH)+'" width="12" height="15" fill="#38bdf8" stroke="#0284c7"/>';
 svg+='<text x="'+(jX+36)+'" y="'+(jY+jH+24)+'" text-anchor="middle" fill="#38bdf8" font-size="7">Bath In (20°C)</text>';
 svg+='<rect x="'+(jX+jW-42)+'" y="'+(jY-15)+'" width="12" height="15" fill="#38bdf8" stroke="#0284c7"/>';
 svg+='<text x="'+(jX+jW-36)+'" y="'+(jY-18)+'" text-anchor="middle" fill="#38bdf8" font-size="7">Bath Out</text>';


 // --- 3. Receiving Vessel / Effluent Burette (Right: x = 520 to 690) ---
 const bX=540,bY=120,bW=34,bH=150;
 svg+='<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="3" fill="url(#reservoirGrad)" stroke="#64748b" stroke-width="1.2"/>';
 // Capillary exit nozzle into receiving burette
 svg+='<path d="M'+(capX+capW)+' '+(capY+capH/2)+' L'+(bX+bW/2)+' '+(capY+capH/2)+' L'+(bX+bW/2)+' '+(bY+15)+'" fill="none" stroke="#38bdf8" stroke-width="3"/>';
 // Dripping effluent
 svg+='<line x1="'+(bX+bW/2)+'" y1="'+(bY+15)+'" x2="'+(bX+bW/2)+'" y2="'+(bY+35)+'" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3,3"/>';
 svg+='<circle cx="'+(bX+bW/2)+'" cy="'+(bY+38)+'" r="2" fill="#7dd3fc"/>';

 // Collected liquid in receiving burette
 const collH=Math.min(90, Math.max(10, (q_val/2.2)*80));
 svg+='<rect x="'+(bX+2)+'" y="'+(bY+bH-collH)+'" width="'+(bW-4)+'" height="'+collH+'" rx="2" fill="url(#waterFlow)" fill-opacity=".75"/>';
 // Burette graduation lines
 for(let gy=bY+20;gy<bY+bH-10;gy+=12){
  svg+='<line x1="'+bX+'" y1="'+gy+'" x2="'+(bX+6)+'" y2="'+gy+'" stroke="#94a3b8" stroke-width="0.8"/>';
 }

 // Analytical Digital Readout Screen (Right Panel)
 const panX=590,panY=85,panW=115,panH=150;
 svg+='<rect x="'+panX+'" y="'+panY+'" width="'+panW+'" height="'+panH+'" rx="5" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(panX+panW/2)+'" y="'+(panY+18)+'" text-anchor="middle" fill="#86efac" font-size="9" font-weight="bold">DISCHARGE RATE</text>';

 svg+='<rect x="'+(panX+8)+'" y="'+(panY+26)+'" width="'+(panW-16)+'" height="32" rx="3" fill="#051009" stroke="#162e1e"/>';
 const dispQ=measurement?q_val.toFixed(3):(busy?(rawVal*0.75).toFixed(3):'0.000');
 svg+='<text x="'+(panX+panW/2)+'" y="'+(panY+48)+'" text-anchor="middle" fill="#38bdf8" font-size="14" font-family="monospace" font-weight="bold">'+dispQ+'</text>';
 svg+='<text x="'+(panX+panW/2)+'" y="'+(panY+70)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">mL / min</text>';

 svg+='<rect x="'+(panX+8)+'" y="'+(panY+78)+'" width="'+(panW-16)+'" height="58" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(panX+12)+'" y="'+(panY+92)+'" fill="#789c80" font-size="7">ΔP = '+dP_pa.toFixed(0)+' Pa</text>';
 svg+='<text x="'+(panX+12)+'" y="'+(panY+105)+'" fill="#789c80" font-size="7">v = '+v_mean.toFixed(3)+' m/s</text>';
 svg+='<text x="'+(panX+12)+'" y="'+(panY+118)+'" fill="#86efac" font-size="7" font-weight="bold">Re = '+reynolds.toFixed(1)+' (Laminar)</text>';
 svg+='<text x="'+(panX+12)+'" y="'+(panY+130)+'" fill="#facc15" font-size="7">η = 1.0020 mPa·s</text>';

 svg+=text(360,305,'Poiseuille Metrology: Q = (π·r⁴·ΔP) / (8·η·L); High aspect ratio (L/r = 600) eliminates Couette end-effects.','#789c80',8.5);
 return svg;
}

function drawPoiseuilleCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'COMPARATIVE VISCOMETRY METROLOGY: PRIMARY VS SECONDARY FLUID TRANSPORT METHODS','#86efac',12);

 const cards=[
  {
   title:'1. Absolute Poiseuille Capillary',
   sub:'Primary Hydrostatic Capillary Flow (Our Lab)',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Principle: Steady laminar flow under constant hydrostatic head Δh',
    'Equation: Q = (π · r⁴ · ρ · g · Δh) / (8 · η · L)',
    'Classification: Fundamental primary method (no calibration fluid needed)',
    'Fluid range: Low-viscosity fluids (0.3 to 20 mPa·s, water/solvents)',
    'Temperature control: Thermostated water jacket stable to ±0.05 °C',
    'Primary advantage: Extracts true absolute dynamic viscosity directly',
    'Limitation: Highly sensitive to capillary radius bore uniformity (r⁴)'
   ]
  },
  {
   title:'2. Relative Ostwald / Ubbelohde',
   sub:'Gravity Efflux Timing in U-Tube',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Principle: Efflux time t of fixed volume draining between etched marks',
    'Equation: η_unk / η_ref = (ρ_unk · t_unk) / (ρ_ref · t_ref)',
    'Classification: Secondary relative method (requires pure water reference)',
    'Fluid range: Polymer solutions, intrinsic viscosity [η], biological serums',
    'Temperature control: Immersion in large optical thermostatic bath',
    'Primary advantage: Simple glassware, fast execution, small sample volume',
    'Limitation: Relative only; variable driving head requires meniscus alignment'
   ]
  },
  {
   title:'3. Falling Sphere / Rotational',
   sub:'Stokes Terminal Drag & Concentric Cylinder Shear',
   color:'#fde047',
   border:'#5a4814',
   items:[
    'Principle: Stokes settling sphere (Höppler) or Couette drag torque',
    'Equation: Höppler: η = K · (ρ_s - ρ) · t; Couette: τ = η · (du/dy)',
    'Classification: Direct mechanical shear rate rheometry',
    'Fluid range: Medium to ultra-high viscosity (1 to 10⁶ mPa·s, oils/polymers)',
    'Temperature control: Jacketed cell with Peltier heating/cooling',
    'Primary advantage: Sweeps shear rates to detect shear-thinning (non-Newtonian)',
    'Limitation: High-viscosity requirement; wall effects alter settling speed'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Poiseuille measures absolute viscosity standard-free; Ostwald requires water calibration.','#789c80',9);
 return svg;
}

function drawPoiseuilleSandboxView(p,rawVal){
 const h_cm=p.input;
 const q_val=rawVal;
 const dP_pa=998.2*9.80665*(h_cm/100.0);
 const v_mean=(q_val/60.0/1e6)/(Math.PI*Math.pow(0.00025,2));
 const reynolds=(2.0*0.00025*v_mean*998.2)/0.0010020;

 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'PARABOLIC SHEAR VELOCITY PROFILE & LAMINAR FLOW STABILITY: POISEUILLE','#86efac',12);

 // Left Panel: Parabolic Velocity Profile across Capillary Bore (r = -R to +R)
 const lX=25,lY=46,lW=340,lH=230;
 svg+='<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">PARABOLIC SHEAR VELOCITY PROFILE v(r)</text>';

 // Upper & lower capillary walls
 const wY1=lY+45,wY2=lY+165;
 svg+='<line x1="'+(lX+20)+'" y1="'+wY1+'" x2="'+(lX+lW-20)+'" y2="'+wY1+'" stroke="#94a3b8" stroke-width="3"/>';
 svg+='<text x="'+(lX+25)+'" y="'+(wY1-6)+'" fill="#94a3b8" font-size="7.5">Upper Capillary Wall (r = +R, v = 0 No-Slip)</text>';
 svg+='<line x1="'+(lX+20)+'" y1="'+wY2+'" x2="'+(lX+lW-20)+'" y2="'+wY2+'" stroke="#94a3b8" stroke-width="3"/>';
 svg+='<text x="'+(lX+25)+'" y="'+(wY2+12)+'" fill="#94a3b8" font-size="7.5">Lower Capillary Wall (r = -R, v = 0 No-Slip)</text>';

 // Centerline dashed line
 const cY=(wY1+wY2)/2;
 svg+='<line x1="'+(lX+20)+'" y1="'+cY+'" x2="'+(lX+lW-20)+'" y2="'+cY+'" stroke="#334155" stroke-width="1" stroke-dasharray="3,3"/>';

 // Velocity profile arrows (parabolic curve)
 const vMaxPix=(v_mean/0.20)*130;
 for(let step=-5;step<=5;step++){
  const rFrac=step/5.0;
  const py=cY+rFrac*((wY2-wY1)/2 - 5);
  const vxLen=vMaxPix*(1 - rFrac*rFrac);
  if(vxLen>2){
   svg+='<line x1="'+(lX+50)+'" y1="'+py+'" x2="'+(lX+50+vxLen)+'" y2="'+py+'" stroke="#38bdf8" stroke-width="1.5"/>';
   svg+='<polygon points="'+(lX+50+vxLen)+','+(py-2.5)+' '+(lX+54+vxLen)+','+py+' '+(lX+50+vxLen)+','+(py+2.5)+'" fill="#38bdf8"/>';
  }
 }
 // Curve connecting arrow heads
 const pts=[];
 for(let s=-20;s<=20;s++){
  const rf=s/20.0;
  const y=cY+rf*((wY2-wY1)/2 - 5);
  const x=lX+54+vMaxPix*(1 - rf*rf);
  pts.push(x.toFixed(1)+','+y.toFixed(1));
 }
 svg+='<polyline points="'+pts.join(' ')+'" fill="none" stroke="#facc15" stroke-width="1.8"/>';

 // Data summary below velocity profile
 svg+='<rect x="'+(lX+15)+'" y="'+(lY+180)+'" width="'+(lW-30)+'" height="38" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(lX+25)+'" y="'+(lY+194)+'" fill="#789c80" font-size="7.5">Mean Velocity: v_mean = '+v_mean.toFixed(3)+' m/s  |  Max Velocity: v_max = '+(2*v_mean).toFixed(3)+' m/s</text>';
 svg+='<text x="'+(lX+25)+'" y="'+(lY+208)+'" fill="#86efac" font-size="7.5" font-family="monospace">v(r) = [ΔP/(4ηL)] · (R² - r²)  ⟹  Shear Rate at Wall γ̇_w = '+((4*v_mean)/0.00025).toFixed(0)+' s⁻¹</text>';


 // Right Panel: Reynolds Number & End-Correction Analysis
 const rX=380,rY=46,rW=315,rH=230;
 svg+='<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">REYNOLDS CRITERION & HYDRODYNAMIC AUDIT</text>';

 const errItems=[
  {label:'Reynolds Number',desc:'Re = (2·r·v·ρ)/η = '+reynolds.toFixed(1)+' ≪ 2000',val:'Strictly Laminar Flow',col:'#48bb78'},
  {label:'Couette End-Losses',desc:'Entrance length L_e ≈ 0.22 cm ≪ 15 cm (L/r = 600)',val:'< 0.2% Dissipation',col:'#38bdf8'},
  {label:'Radius Sensitivity (r⁴)',desc:'δr/r = 0.4% propagates as 4·(δr/r) = 1.6%',val:'Calibrated to ±0.001 mm',col:'#f87171'},
  {label:'Thermal Gradient (T)',desc:'∂η/∂T ≈ -2.5%/°C near 20.0 °C',val:'Thermostated ±0.05 °C',col:'#fbbf24'},
  {label:'OLS Slope Insulation (★)',desc:'Residual meniscus pressure absorbed into Q₀',val:'Slope = 0.05995 Unbiased',col:'#86efac'}
 ];

 errItems.forEach((ei,idx)=>{
  const ey=rY+30+idx*39;
  svg+='<rect x="'+(rX+8)+'" y="'+ey+'" width="'+(rW-16)+'" height="33" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+12)+'" fill="'+ei.col+'" font-size="7.5" font-weight="bold">'+ei.label+'</text>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+25)+'" fill="#94a3b8" font-size="6.8">'+ei.desc+'</text>';
  svg+='<text x="'+(rX+rW-14)+'" y="'+(ey+12)+'" text-anchor="end" fill="'+ei.col+'" font-size="7.5" font-family="monospace">'+ei.val+'</text>';
 });

 svg+=text(360,305,'Laminar Invariant: Reynolds number Re = '+reynolds.toFixed(1)+' guarantees pure Poiseuille streamline shear.','#789c80',9);
 return svg;
}


// ======================================================================
// CHEMISTRY LAB 09: SURFACE TENSION & DROP-WEIGHT STALAGMOMETRY
// ======================================================================
function drawStalagBenchView(p,rawVal){
 const n_drops=p.input;
 const m_tot=rawVal;
 const m_drop=m_tot/n_drops;
 const v_drop=(m_drop/0.9982)*1000.0;
 const r_V=(3.50/Math.cbrt(v_drop));

 let svg='<defs>';
 svg+='<linearGradient id="dropGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#0284c7" stop-opacity=".75"/><stop offset="50%" stop-color="#38bdf8" stop-opacity=".95"/><stop offset="100%" stop-color="#0284c7" stop-opacity=".8"/></linearGradient>';
 svg+='<linearGradient id="stalagGlass" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#ffffff" stop-opacity=".25"/><stop offset="15%" stop-color="#ffffff" stop-opacity=".05"/><stop offset="85%" stop-color="#ffffff" stop-opacity=".08"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".3"/></linearGradient>';
 svg+='<linearGradient id="jacketBlue" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#38bdf8" stop-opacity=".15"/><stop offset="100%" stop-color="#0284c7" stop-opacity=".1"/></linearGradient>';
 svg+='</defs><rect width="720" height="320" fill="#08140c"/>';

 svg+=text(360,20,'TRAUBE DROP-WEIGHT STALAGMOMETER: SURFACE TENSION (20.0 °C THERMOSTATED)','#86efac',12);

 // Table surface
 svg+='<rect x="0" y="275" width="720" height="45" fill="#132419" stroke="#1f3b2a" stroke-width="1"/>';
 svg+='<line x1="0" y1="275" x2="720" y2="275" stroke="#2d523b" stroke-width="2"/>';

 // Retort Stand & Clamps (Left: x = 40 to 120)
 svg+='<rect x="40" y="260" width="85" height="15" rx="3" fill="#334155" stroke="#0f172a"/>';
 svg+='<rect x="78" y="30" width="8" height="230" fill="#475569" stroke="#1e293b"/>';
 // Clamps
 svg+='<rect x="70" y="70" width="85" height="8" rx="2" fill="#64748b"/>';
 svg+='<rect x="70" y="160" width="85" height="8" rx="2" fill="#64748b"/>';


 // --- Stalagmometer Assembly (x = 135 to 225) ---
 const sX=160;
 // Top Needle Valve & Rubber Aspirator
 svg+='<rect x="'+(sX-8)+'" y="35" width="16" height="18" rx="2" fill="#334155" stroke="#475569"/>';
 svg+='<circle cx="'+sX+'" cy="30" r="8" fill="#f97316"/>';
 svg+='<text x="'+(sX+14)+'" y="45" fill="#f97316" font-size="7">PTFE Needle Valve (8-10 s/drop)</text>';

 // Outer Circulating Water Jacket
 const jX=sX-22,jY=55,jW=44,jH=145;
 svg+='<rect x="'+jX+'" y="'+jY+'" width="'+jW+'" height="'+jH+'" rx="8" fill="url(#jacketBlue)" stroke="#38bdf8" stroke-width="1.2"/>';
 svg+='<text x="'+(jX-8)+'" y="'+(jY+20)+'" text-anchor="end" fill="#38bdf8" font-size="7">Bath (20°C)</text>';
 svg+='<text x="'+(jX-8)+'" y="'+(jY+jH-15)+'" text-anchor="end" fill="#38bdf8" font-size="7">Circulator In</text>';

 // Stalagmometer glass stem & central bulb
 svg+='<rect x="'+(sX-4)+'" y="52" width="8" height="35" fill="url(#stalagGlass)" stroke="#64748b" stroke-width="0.8"/>';
 // Upper Bulb
 svg+='<ellipse cx="'+sX+'" cy="115" rx="14" ry="24" fill="url(#stalagGlass)" stroke="#64748b" stroke-width="1"/>';
 // Liquid inside bulb
 svg+='<ellipse cx="'+sX+'" cy="118" rx="12" ry="20" fill="url(#dropGrad)" fill-opacity=".7"/>';
 // Etched ring marks (fiducial lines)
 svg+='<line x1="'+(sX-10)+'" y1="88" x2="'+(sX+10)+'" y2="88" stroke="#ffffff" stroke-width="1"/>';
 svg+='<line x1="'+(sX-10)+'" y1="142" x2="'+(sX+10)+'" y2="142" stroke="#ffffff" stroke-width="1"/>';

 // Lower capillary stem
 svg+='<rect x="'+(sX-3)+'" y="140" width="6" height="60" fill="url(#stalagGlass)" stroke="#64748b" stroke-width="0.8"/>';
 svg+='<rect x="'+(sX-1)+'" y="140" width="2" height="60" fill="url(#dropGrad)"/>';

 // Precision Ground Razor Tip (external radius r = 3.500 mm, diameter 7.0 mm)
 const tipY=200,tipW=20;
 svg+='<rect x="'+(sX-tipW/2)+'" y="'+tipY+'" width="'+tipW+'" height="4" fill="#94a3b8" stroke="#475569" stroke-width="1"/>';
 svg+='<line x1="'+(sX-tipW/2)+'" y1="'+(tipY+4)+'" x2="'+(sX+tipW/2)+'" y2="'+(tipY+4)+'" stroke="#facc15" stroke-width="1.8"/>';
 svg+='<text x="'+(sX-tipW/2-4)+'" y="'+(tipY+4)+'" text-anchor="end" fill="#facc15" font-size="7.5" font-weight="bold">r = 3.500 mm</text>';

 // Forming Pendent Droplet & Neck Pinch-off
 svg+='<path d="M'+(sX-7)+' '+(tipY+4)+' Q'+(sX-4)+' '+(tipY+12)+' '+(sX-8)+' '+(tipY+18)+' Q'+sX+' '+(tipY+28)+' '+(sX+8)+' '+(tipY+18)+' Q'+(sX+4)+' '+(tipY+12)+' '+(sX+7)+' '+(tipY+4)+' Z" fill="url(#dropGrad)"/>';
 if(busy){
  // Detaching drop in mid-air + satellite drop
  svg+='<circle cx="'+sX+'" cy="'+(tipY+36)+'" r="1.5" fill="#38bdf8"/>'; // satellite droplet
  svg+='<path d="M'+(sX-6)+' '+(tipY+46)+' Q'+sX+' '+(tipY+42)+' '+(sX+6)+' '+(tipY+46)+' Q'+(sX+7)+' '+(tipY+54)+' '+sX+' '+(tipY+58)+' Q'+(sX-7)+' '+(tipY+54)+' '+(sX-6)+' '+(tipY+46)+' Z" fill="url(#dropGrad)"/>';
 }

 // Stoppered glass weighing bottle catching droplets (x = 135 to 185, y = 225 to 275)
 const wbX=sX-22,wbY=226,wbW=44,wbH=48;
 svg+='<rect x="'+wbX+'" y="'+wbY+'" width="'+wbW+'" height="'+wbH+'" rx="4" fill="url(#stalagGlass)" stroke="#64748b" stroke-width="1"/>';
 // Liquid accumulating in weighing bottle
 const collH=Math.min(32, Math.max(6, (n_drops/60.0)*28));
 svg+='<rect x="'+(wbX+2)+'" y="'+(wbY+wbH-collH)+'" width="'+(wbW-4)+'" height="'+collH+'" rx="2" fill="url(#dropGrad)" fill-opacity=".75"/>';
 svg+='<text x="'+sX+'" y="'+(wbY+wbH-8)+'" text-anchor="middle" fill="#ffffff" font-size="7.5" font-weight="bold">'+n_drops.toFixed(0)+' Drops</text>';


 // --- 2. Four-Decimal Analytical Balance (Right: x = 280 to 690) ---
 const balX=280,balY=90,balW=410,balH=180;
 // Granite block
 svg+='<rect x="'+(balX-10)+'" y="260" width="'+(balW+20)+'" height="15" rx="3" fill="#1e293b" stroke="#0f172a"/>';
 // Main balance housing
 svg+='<rect x="'+balX+'" y="'+balY+'" width="'+balW+'" height="'+balH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';

 // Draft shield enclosure
 const dX=balX+18,dY=balY+14,dW=balW-36,dH=95;
 svg+='<rect x="'+dX+'" y="'+dY+'" width="'+dW+'" height="'+dH+'" rx="4" fill="#061209" stroke="#334155" stroke-width="1.2"/>';

 // Weighing Pan & Bottle Replica inside Draft Chamber
 const panCx=dX+75,panCy=dY+dH-10;
 svg+='<rect x="'+(panCx-35)+'" y="'+panCy+'" width="70" height="6" rx="2" fill="#94a3b8" stroke="#475569"/>';
 svg+='<rect x="'+(panCx-5)+'" y="'+(panCy+6)+'" width="10" height="6" fill="#64748b"/>';
 // Bottle on pan
 svg+='<rect x="'+(panCx-16)+'" y="'+(panCy-30)+'" width="32" height="30" rx="3" fill="url(#stalagGlass)" stroke="#64748b"/>';
 svg+='<rect x="'+(panCx-14)+'" y="'+(panCy-14)+'" width="28" height="14" rx="2" fill="url(#dropGrad)" fill-opacity=".75"/>';

 // Data Readout Display inside Draft Chamber (right side)
 svg+='<rect x="'+(panCx+55)+'" y="'+(dY+10)+'" width="200" height="75" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(panCx+65)+'" y="'+(dY+26)+'" fill="#789c80" font-size="7.5" font-weight="bold">QUASI-STATIC METROLOGY</text>';
 svg+='<text x="'+(panCx+65)+'" y="'+(dY+40)+'" fill="#cbd5e1" font-size="7.5">Tip Radius: r = 3.500 mm</text>';
 svg+='<text x="'+(panCx+65)+'" y="'+(dY+53)+'" fill="#cbd5e1" font-size="7.5">Harkins-Jordan: φ = 0.6150 (r/V⅓ = 0.753)</text>';
 svg+='<text x="'+(panCx+65)+'" y="'+(dY+66)+'" fill="#facc15" font-size="7.5" font-family="monospace">m_drop = '+(m_drop).toFixed(5)+' g/drop</text>';
 svg+='<text x="'+(panCx+65)+'" y="'+(dY+79)+'" fill="#86efac" font-size="8" font-family="monospace" font-weight="bold">γ = 72.80 mN/m (Water at 20.0 °C)</text>';

 // Analytical LCD Display Screen (Bottom of Balance)
 const lcdX=balX+30,lcdY=balY+120,lcdW=balW-60,lcdH=45;
 svg+='<rect x="'+lcdX+'" y="'+lcdY+'" width="'+lcdW+'" height="'+lcdH+'" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.5"/>';
 svg+='<circle cx="'+(lcdX+16)+'" cy="'+(lcdY+22)+'" r="4" fill="'+(busy?'#eab308':'#48bb78')+'"/>';
 svg+='<text x="'+(lcdX+26)+'" y="'+(lcdY+18)+'" fill="#789c80" font-size="7.5">STABLE</text>';
 svg+='<text x="'+(lcdX+26)+'" y="'+(lcdY+30)+'" fill="#789c80" font-size="7.5">NET TARE</text>';

 const dispVal=measurement?m_tot.toFixed(4):(busy?(rawVal*0.75).toFixed(4):'0.0000');
 svg+='<text x="'+(lcdX+lcdW-20)+'" y="'+(lcdY+30)+'" text-anchor="end" fill="#86efac" font-size="20" font-family="monospace" font-weight="bold">'+dispVal+' g</text>';

 svg+=text(360,305,'Tate Formulation with Harkins-Jordan: W = 2π·r·γ·φ; Incomplete neck detachment (φ = 0.615) is rigorously compensated.','#789c80',8.5);
 return svg;
}

function drawStalagCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'COMPARATIVE TENSIOMETRY METROLOGY: INTERFACIAL MEASUREMENT TECHNIQUES','#86efac',12);

 const cards=[
  {
   title:'1. Drop-Weight Stalagmometry',
   sub:'Quasi-Static Gravimetric Detachment (Our Lab)',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Principle: Tate law with Harkins-Jordan hydrodynamic correction',
    'Equation: γ = (m_drop · g) / [2π · r · φ(r/V⅓)]',
    'Geometry: Optically ground razor-sharp circular tip (r = 3.500 mm)',
    'Correction: φ = 0.6150 compensates for residual neck stub on tip',
    'Precision: ±0.1% to ±0.2% absolute surface tension accuracy',
    'Primary advantage: Robust glassware, vibration-tolerant, small volume',
    'Limitation: Requires slow detachment (8-10 s/drop) to avoid inertia'
   ]
  },
  {
   title:'2. Du Noüy Platinum Ring',
   sub:'Torsion Wire Meniscus Detachment',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Principle: Maximum detachment pull on submerged Pt-Ir wire ring',
    'Equation: γ = [F_max / (4π · R_ring)] · F_Zuidema-Waters',
    'Geometry: Thin circular platinum ring (R ≈ 9.55 mm, r_wire ≈ 0.18 mm)',
    'Correction: Complex empirical ring factors (F = 0.75 to 1.05)',
    'Precision: ±0.2% to ±0.5% with certified tensiometer calibration',
    'Primary advantage: Fast, automated, measures liquid-liquid interfaces',
    'Limitation: Wire ring must remain perfectly planar; fragile to warping'
   ]
  },
  {
   title:'3. Wilhelmy Plate / Capillary Rise',
   sub:'Wetted Plate Force & Meniscus Height',
   color:'#fde047',
   border:'#5a4814',
   items:[
    'Principle: Vertical capillary pull on sandblasted Pt plate (θ = 0°)',
    'Equation: Wilhelmy: γ = F / (2 · w); Capillary: γ = (r · h · Δρ · g) / 2',
    'Geometry: Thin roughened platinum plate or precision glass bore',
    'Correction: Zero empirical factor required if complete wetting (θ = 0°)',
    'Precision: Premier absolute benchmark for Langmuir dynamic films',
    'Primary advantage: Continuous real-time dynamic monolayer tracking',
    'Limitation: Acute sensitivity to surface dust and contact angle errors'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Stalagmometry measures drop mass; Du Noüy measures ring pull; Wilhelmy measures wetted plate force.','#789c80',9);
 return svg;
}

function drawStalagSandboxView(p,rawVal){
 const n_drops=p.input;
 const m_tot=rawVal;
 const m_drop=m_tot/n_drops;
 const v_drop=(m_drop/0.9982)*1000.0;
 const r_V=(3.50/Math.cbrt(v_drop));

 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'PENDENT DROP HYDRODYNAMIC PINCH-OFF & HARKINS-JORDAN CORRECTION','#86efac',12);

 // Left Panel: Drop Neck Rupture Anatomy
 const lX=25,lY=46,lW=340,lH=230;
 svg+='<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">RAYLEIGH-PLATEAU NECK PINCH-OFF ANATOMY</text>';

 // Capillary tip outline
 const cx=lX+85,cy=lY+45;
 svg+='<rect x="'+(cx-20)+'" y="'+cy+'" width="40" height="8" fill="#94a3b8" stroke="#475569"/>';
 svg+='<text x="'+(cx+26)+'" y="'+(cy+7)+'" fill="#facc15" font-size="7.5">Tip Radius r = 3.50 mm</text>';

 // Residual liquid stub remaining on tip (38.5% of volume)
 svg+='<path d="M'+(cx-18)+' '+(cy+8)+' Q'+cx+' '+(cy+22)+' '+(cx+18)+' '+(cy+8)+' Z" fill="#38bdf8" fill-opacity=".4" stroke="#38bdf8" stroke-dasharray="2,2"/>';
 svg+='<text x="'+(cx+24)+'" y="'+(cy+20)+'" fill="#94a3b8" font-size="7">Residual Stub (38.5% volume stays)</text>';

 // Detaching primary drop (61.5% of volume, phi = 0.615)
 svg+='<path d="M'+(cx-16)+' '+(cy+40)+' Q'+cx+' '+(cy+30)+' '+(cx+16)+' '+(cy+40)+' Q'+(cx+18)+' '+(cy+65)+' '+cx+' '+(cy+72)+' Q'+(cx-18)+' '+(cy+65)+' '+(cx-16)+' '+(cy+40)+' Z" fill="#0284c7" stroke="#38bdf8" stroke-width="1.2"/>';
 svg+='<circle cx="'+cx+'" cy="'+(cy+28)+'" r="2" fill="#38bdf8"/>'; // Satellite drop
 svg+='<text x="'+(cx+24)+'" y="'+(cy+55)+'" fill="#38bdf8" font-size="7.5" font-weight="bold">Primary Detached Drop (61.5%)</text>';
 svg+='<text x="'+(cx+24)+'" y="'+(cy+66)+'" fill="#789c80" font-size="7">φ = W_det / W_ideal = 0.6150</text>';

 // Data summary card on left panel
 svg+='<rect x="'+(lX+15)+'" y="'+(lY+145)+'" width="'+(lW-30)+'" height="70" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(lX+25)+'" y="'+(lY+160)+'" fill="#789c80" font-size="7.5" font-weight="bold">DIMENSIONLESS SCALING PARAMETERS</text>';
 svg+='<text x="'+(lX+25)+'" y="'+(lY+174)+'" fill="#cbd5e1" font-size="7.5">Single Drop Volume: V = '+(v_drop).toFixed(2)+' mm³ = '+(v_drop/1000).toFixed(5)+' mL</text>';
 svg+='<text x="'+(lX+25)+'" y="'+(lY+188)+'" fill="#facc15" font-size="7.5" font-family="monospace">Characteristic Shape: r / V⅓ = 3.50 / '+(Math.cbrt(v_drop)).toFixed(2)+' = 0.7526</text>';
 svg+='<text x="'+(lX+25)+'" y="'+(lY+202)+'" fill="#86efac" font-size="8" font-family="monospace" font-weight="bold">Harkins-Jordan Factor: φ(0.7526) = 0.6150 (Optimal Plateau)</text>';


 // Right Panel: Systematic Error & Interfacial Sensitivity Audit
 const rX=380,rY=46,rW=315,rH=230;
 svg+='<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">INTERFACIAL SENSITIVITY & ERROR AUDIT</text>';

 const errItems=[
  {label:'Tate Detachment Factor (φ)',desc:'φ = 0.6150 compensates for incomplete neck snap',val:'Exact +62.6% Tate Correction',col:'#48bb78'},
  {label:'Detachment Rate (<5 s/drop)',desc:'Fast dripping introduces inertial momentum push',val:'Prevented: 8-10 s/drop',col:'#38bdf8'},
  {label:'Surfactant Contamination (-)',desc:'Trace organics concentrate at surface (Gibbs excess)',val:'Prevented by chromic acid',col:'#f87171'},
  {label:'Temperature Drift (T)',desc:'∂γ/∂T ≈ -0.151 mN/(m·°C) near 20.0 °C',val:'Thermostated ±0.05 °C',col:'#fbbf24'},
  {label:'OLS Slope Insulation (★)',desc:'Weighing bottle tare drift absorbed into m₀',val:'Slope = 0.1004 g/drop Unbiased',col:'#86efac'}
 ];

 errItems.forEach((ei,idx)=>{
  const ey=rY+30+idx*39;
  svg+='<rect x="'+(rX+8)+'" y="'+ey+'" width="'+(rW-16)+'" height="33" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+12)+'" fill="'+ei.col+'" font-size="7.5" font-weight="bold">'+ei.label+'</text>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+25)+'" fill="#94a3b8" font-size="6.8">'+ei.desc+'</text>';
  svg+='<text x="'+(rX+rW-14)+'" y="'+(ey+12)+'" text-anchor="end" fill="'+ei.col+'" font-size="7.5" font-family="monospace">'+ei.val+'</text>';
 });

 svg+=text(360,305,'Plateau Invariant: Operating at r/V⅓ = 0.7526 insulates Harkins-Jordan factor against droplet volume shifts.','#789c80',9);
 return svg;
}


// ======================================================================
// CHEMISTRY LAB 10: CRYOSCOPIC FREEZING-POINT DEPRESSION (MOLAR MASS)
// ======================================================================
function drawCryoBenchView(p,rawVal){
 const w_solute=p.input;
 const dt_f=rawVal;
 const t_freeze=6.550-dt_f;
 const molality=dt_f/20.00;
 const m_calc=w_solute/(molality*0.025);

 let svg='<defs>';
 svg+='<linearGradient id="iceBath" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#bae6fd" stop-opacity=".6"/><stop offset="100%" stop-color="#38bdf8" stop-opacity=".85"/></linearGradient>';
 svg+='<linearGradient id="solvGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#a7f3d0" stop-opacity=".5"/><stop offset="50%" stop-color="#6ee7b7" stop-opacity=".7"/><stop offset="100%" stop-color="#34d399" stop-opacity=".6"/></linearGradient>';
 svg+='<linearGradient id="cellGlass" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#ffffff" stop-opacity=".25"/><stop offset="15%" stop-color="#ffffff" stop-opacity=".06"/><stop offset="85%" stop-color="#ffffff" stop-opacity=".08"/><stop offset="100%" stop-color="#ffffff" stop-opacity=".3"/></linearGradient>';
 svg+='<linearGradient id="hgGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#94a3b8"/><stop offset="50%" stop-color="#cbd5e1"/><stop offset="100%" stop-color="#64748b"/></linearGradient>';
 svg+='</defs><rect width="720" height="320" fill="#08140c"/>';

 svg+=text(360,20,'BECKMANN CRYOSCOPIC FREEZING-POINT CELL: CYCLOHEXANE (K_f = 20.00 K·kg/mol)','#86efac',12);

 // Table surface
 svg+='<rect x="0" y="275" width="720" height="45" fill="#132419" stroke="#1f3b2a" stroke-width="1"/>';
 svg+='<line x1="0" y1="275" x2="720" y2="275" stroke="#2d523b" stroke-width="2"/>';

 // --- 1. Jacketed Cryostat Bath & Beckmann Cell (Left: x = 50 to 330) ---
 const bX=175;
 // Outer Cryostat Beaker (Crushed Ice & Water at 2.0 °C)
 const bkX=bX-85,bkY=90,bkW=170,bkH=175;
 svg+='<rect x="'+bkX+'" y="'+bkY+'" width="'+bkW+'" height="'+bkH+'" rx="8" fill="url(#iceBath)" stroke="#38bdf8" stroke-width="1.5"/>';
 // Floating ice chunks
 for(let ic=0;ic<6;ic++){
  const ix=bkX+15+((ic*28)%135),iy=bkY+15+((ic*24)%45);
  svg+='<polygon points="'+ix+','+iy+' '+(ix+16)+','+(iy-5)+' '+(ix+22)+','+(iy+10)+' '+(ix+8)+','+(iy+18)+' '+(ix-2)+','+(iy+10)+'" fill="#ffffff" fill-opacity=".7" stroke="#e0f2fe"/>';
 }
 svg+='<text x="'+(bkX+10)+'" y="'+(bkY+bkH-8)+'" fill="#0369a1" font-size="7.5" font-weight="bold">Ice-Water Cryostat (2.0 ± 0.5 °C)</text>';

 // Outer Air Jacket Tube
 const ajX=bX-34,ajY=65,ajW=68,ajH=185;
 svg+='<rect x="'+ajX+'" y="'+ajY+'" width="'+ajW+'" height="'+ajH+'" rx="6" fill="url(#cellGlass)" stroke="#64748b" stroke-width="1.2"/>';
 svg+='<text x="'+(ajX-4)+'" y="'+(ajY+45)+'" text-anchor="end" fill="#94a3b8" font-size="7">Air Jacket (Annular Insulation)</text>';

 // Inner Boiling Tube containing 25.00 g Cyclohexane Solution
 const itX=bX-22,itY=50,itW=44,itH=185;
 svg+='<rect x="'+itX+'" y="'+itY+'" width="'+itW+'" height="'+itH+'" rx="5" fill="url(#cellGlass)" stroke="#475569" stroke-width="1"/>';
 // Solution inside inner tube
 const solH=75;
 svg+='<rect x="'+(itX+2)+'" y="'+(itY+itH-solH)+'" width="'+(itW-4)+'" height="solH" rx="3" fill="url(#solvGrad)"/>';
 // Needle-like cyclohexane crystals appearing if freezing
 if(busy){
  for(let cr=0;cr<8;cr++){
   const cx1=itX+8+((cr*11)%28),cy1=itY+itH-12-((cr*8)%55);
   svg+='<line x1="'+cx1+'" y1="'+cy1+'" x2="'+(cx1+10)+'" y2="'+(cy1-8)+'" stroke="#ffffff" stroke-width="1.5"/>';
  }
 }
 svg+='<text x="'+bX+'" y="'+(itY+itH-8)+'" text-anchor="middle" fill="#065f46" font-size="7" font-weight="bold">25.00 g Cyclohexane + '+w_solute.toFixed(2)+' g Solute</text>';

 // Beckmann Differential Thermometer (inserted through center stopper)
 const thX=bX-4,thW=8;
 // Thermometer stem extending up into the air
 svg+='<rect x="'+thX+'" y="25" width="'+thW+'" height="150" fill="url(#cellGlass)" stroke="#475569" stroke-width="0.8"/>';
 // Large lower mercury bulb submerged in solution
 svg+='<rect x="'+(bX-6)+'" y="175" width="12" height="38" rx="4" fill="url(#hgGrad)" stroke="#475569"/>';
 // Mercury thread in capillary stem
 const hgH=Math.min(95, Math.max(15, (dt_f/6.5)*85));
 svg+='<rect x="'+(thX+2)+'" y="'+(150-hgH)+'" width="4" height="'+(hgH+25)+'" fill="#cbd5e1"/>';
 // Beckmann 5-degree etched scale lines
 for(let sy=40;sy<=140;sy+=10){
  svg+='<line x1="'+thX+'" y1="'+sy+'" x2="'+(thX+3)+'" y2="'+sy+'" stroke="#ffffff" stroke-width="0.7"/>';
 }
 // Top auxiliary mercury reservoir
 svg+='<ellipse cx="'+(bX)+'" cy="25" rx="7" ry="5" fill="url(#cellGlass)" stroke="#475569"/>';
 svg+='<circle cx="'+bX+'" cy="25" r="3.5" fill="#94a3b8"/>';
 svg+='<text x="'+(bX+12)+'" y="28" fill="#cbd5e1" font-size="7">Auxiliary Mercury Chamber</text>';

 // Motorized Wire Loop Stirrer (ring moving around thermometer)
 const stY=busy?185:198;
 svg+='<ellipse cx="'+bX+'" cy="'+stY+'" rx="16" ry="4" fill="none" stroke="#facc15" stroke-width="1.5"/>';
 svg+='<line x1="'+(bX+16)+'" y1="'+stY+'" x2="'+(bX+16)+'" y2="45" stroke="#facc15" stroke-width="1.2"/>';
 svg+='<text x="'+(bX+20)+'" y="52" fill="#facc15" font-size="7">Stirrer (60/min)</text>';


 // --- 2. Digital Readout & Analysis Dashboard (Right: x = 360 to 695) ---
 const dDashX=360,dDashY=45,dDashW=335,dDashH=220;
 svg+='<rect x="'+dDashX+'" y="'+dDashY+'" width="'+dDashW+'" height="'+dDashH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(dDashX+dDashW/2)+'" y="'+(dDashY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">BECKMANN THERMOMETRIC READOUT & CRYOSCOPY</text>';

 // Upper digital readouts (two side-by-side cards)
 const c1X=dDashX+12,c1Y=dDashY+28,c1W=148,c1H=65;
 svg+='<rect x="'+c1X+'" y="'+c1Y+'" width="'+c1W+'" height="'+c1H+'" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(c1X+10)+'" y="'+(c1Y+15)+'" fill="#789c80" font-size="7.5" font-weight="bold">FREEZING-POINT DEPRESSION</text>';
 const dispDT=measurement?dt_f.toFixed(3):(busy?(rawVal*0.75).toFixed(3):'0.000');
 svg+='<text x="'+(c1X+10)+'" y="'+(c1Y+40)+'" fill="#38bdf8" font-size="20" font-family="monospace" font-weight="bold">ΔT = '+dispDT+' °C</text>';
 svg+='<text x="'+(c1X+10)+'" y="'+(c1Y+55)+'" fill="#94a3b8" font-size="7.5">T_f = '+(6.550-dt_f).toFixed(3)+' °C (Pure: 6.550 °C)</text>';

 const c2X=dDashX+175,c2Y=dDashY+28,c2W=148,c2H=65;
 svg+='<rect x="'+c2X+'" y="'+c2Y+'" width="'+c2W+'" height="'+c2H+'" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(c2X+10)+'" y="'+(c2Y+15)+'" fill="#789c80" font-size="7.5" font-weight="bold">SOLUTE MOLALITY & MOLAR MASS</text>';
 svg+='<text x="'+(c2X+10)+'" y="'+(c2Y+32)+'" fill="#cbd5e1" font-size="8">m = ΔT/K_f = '+molality.toFixed(4)+' mol/kg</text>';
 svg+='<text x="'+(c2X+10)+'" y="'+(c2Y+47)+'" fill="#facc15" font-size="8" font-family="monospace">w_solute = '+w_solute.toFixed(2)+' g in 25.00 g solv</text>';
 svg+='<text x="'+(c2X+10)+'" y="'+(c2Y+60)+'" fill="#86efac" font-size="8.5" font-family="monospace" font-weight="bold">M = '+m_calc.toFixed(2)+' g/mol (Biphenyl)</text>';

 // Lower Detailed Specification Box
 const specX=dDashX+12,specY=dDashY+102,specW=dDashW-24,specH=105;
 svg+='<rect x="'+specX+'" y="'+specY+'" width="'+specW+'" height="'+specH+'" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(specX+12)+'" y="'+(specY+16)+'" fill="#86efac" font-size="8" font-weight="bold">THERMODYNAMIC CRYOSCOPIC PARAMETERS</text>';

 svg+='<text x="'+(specX+12)+'" y="'+(specY+32)+'" fill="#cbd5e1" font-size="7.5">• Solvent: Anhydrous Cyclohexane (C₆H₁₂), w_solvent = 25.000 g (0.0250 kg)</text>';
 svg+='<text x="'+(specX+12)+'" y="'+(specY+46)+'" fill="#cbd5e1" font-size="7.5">• Cryoscopic Constant: K_f = (R·T_f²·M_s) / (1000·ΔH_fus) = 20.00 K·kg/mol</text>';
 svg+='<text x="'+(specX+12)+'" y="'+(specY+60)+'" fill="#cbd5e1" font-size="7.5">• Low Enthalpy of Fusion: ΔH_fus = 2.68 kJ/mol (Plastic Crystal Phase Tumbling)</text>';
 svg+='<text x="'+(specX+12)+'" y="'+(specY+74)+'" fill="#38bdf8" font-size="7.5">• Unknown Solute: Pure crystalline biphenyl (C₁₂H₁₀, formula weight M = 154.21 g/mol)</text>';
 svg+='<text x="'+(specX+12)+'" y="'+(specY+88)+'" fill="#86efac" font-size="8" font-family="monospace" font-weight="bold">• Invariant: ΔT_f = [K_f / (w_solv·M)] · w_solute ⟹ Slope m = 5.1873 °C/g (R² = 1.00000)</text>';

 svg+=text(360,305,'Raoult Colligative Law: ΔT_f = K_f · m_solute; High K_f of cyclohexane (20.00) delivers extreme molecular weight precision.','#789c80',8.5);
 return svg;
}

function drawCryoCompareView(p,rawVal){
 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,24,'COMPARATIVE MOLECULAR WEIGHT METROLOGY: THERMODYNAMIC COLLIGATIVE METHODS','#86efac',12);

 const cards=[
  {
   title:'1. Cryoscopy (Freezing-Point)',
   sub:'Beckmann Freezing Depression (Our Lab)',
   color:'#86efac',
   border:'#254d33',
   items:[
    'Principle: Solute lowers solvent chemical potential: ΔT_f = K_f · m',
    'Sensitivity: Enormous K_f in plastic cyclohexane (K_f = 20.00 K·kg/mol)',
    'Temperature: Low temperature (6.55 °C), prevents thermal degradation',
    'Solute range: Small to medium non-volatiles (M = 50 to 800 g/mol)',
    'Thermometry: Beckmann differential sensor (±0.002 °C precision)',
    'Primary advantage: High temperature resolution, no thermal decomposition',
    'Limitation: Cooling curves require supercooling extrapolation'
   ]
  },
  {
   title:'2. Ebulliometry (Boiling-Point)',
   sub:'Cottrell Boiling Point Elevation',
   color:'#38bdf8',
   border:'#1e3a5f',
   items:[
    'Principle: Vapor pressure reduction raises bp: ΔT_b = K_b · m',
    'Sensitivity: Modest K_b (water K_b = 0.512; benzene K_b = 2.53 K·kg/mol)',
    'Temperature: High temperatures (solvent bp); can decompose biomolecules',
    'Pumping system: Requires Cottrell vapor pump to spray equilibrium liquid',
    'Thermometry: Beckmann thermometer submerged in boiling spray',
    'Primary advantage: Direct thermodynamic liquid-vapor equilibrium',
    'Limitation: Acute barometric pressure sensitivity (±0.1 mmHg shifts bp)'
   ]
  },
  {
   title:'3. Membrane & Vapor Osmometry',
   sub:'Semipermeable Osmotic Pressure (VPO)',
   color:'#fde047',
   border:'#5a4814',
   items:[
    'Principle: Van 't Hoff osmotic pressure across membrane: Π = (c/M)·RT',
    'Sensitivity: Immense pressure signals (0.001 M produces ~25 cm head)',
    'Temperature: Isothermal ambient operation (25.0 °C)',
    'Solute range: Macromolecules & synthetic polymers (M = 10⁴ to 10⁶ g/mol)',
    'Thermometry: Matched thermistor bridges (in VPO) or pressure transducer',
    'Primary advantage: Unrivaled for polymers where ΔT_f < 0.0001 °C',
    'Limitation: Membrane leakage for low molecular weight solutes (M < 5000)'
   ]
  }
 ];

 cards.forEach((c,idx)=>{
  const x=25+idx*230,y=46,w=210,h=242;
  svg+='<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg+='<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="32" rx="4" fill="#051009"/>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9.5" font-weight="bold">'+c.title+'</text>';
  svg+='<text x="'+(x+w/2)+'" y="'+(y+34)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">'+c.sub+'</text>';

  c.items.forEach((item,ii)=>{
   const iy=y+54+ii*26;
   svg+='<circle cx="'+(x+16)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg+='<foreignObject x="'+(x+24)+'" y="'+(iy-10)+'" width="'+(w-32)+'" height="26"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.5px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg+=text(360,305,'Comparison: Cryoscopy uses plastic crystal solvents for small molecules; Osmometry measures macromolecules.','#789c80',9);
 return svg;
}

function drawCryoSandboxView(p,rawVal){
 const w_solute=p.input;
 const dt_f=rawVal;
 const t_freeze=6.550-dt_f;
 const molality=dt_f/20.00;
 const m_calc=w_solute/(molality*0.025);

 let svg='<rect x="0" y="0" width="720" height="320" fill="#08140c"/>';
 svg+=text(360,22,'SUPERCOOLING KINETICS, COOLING CURVE REBOUND & TEMPERATURE EXTRAPOLATION','#86efac',12);

 // Left Panel: Experimental Cooling Curve (Temperature vs Time)
 const lX=25,lY=46,lW=340,lH=230;
 svg+='<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">COOLING CURVE KINETICS: T(t) RESOLUTION</text>';

 // Axes
 const axX=lX+45,axY=lY+40,axW=270,axH=145;
 svg+='<rect x="'+axX+'" y="'+axY+'" width="'+axW+'" height="'+axH+'" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(axX+axW/2)+'" y="'+(axY+axH+14)+'" text-anchor="middle" fill="#789c80" font-size="8">Time elapsed t (min)</text>';
 svg+='<text transform="translate('+(axX-14)+' '+(axY+axH/2)+') rotate(-90)" text-anchor="middle" fill="#789c80" font-size="8">Temperature T (°C)</text>';

 // Pure solvent cooling curve (gray dashed)
 svg+='<path d="M'+axX+' '+(axY+15)+' L'+(axX+50)+' '+(axY+45)+' L'+(axX+65)+' '+(axY+65)+' L'+(axX+75)+' '+(axY+45)+' L'+(axX+axW)+' '+(axY+45)+'" fill="none" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3"/>';
 svg+='<text x="'+(axX+axW-5)+'" y="'+(axY+40)+'" text-anchor="end" fill="#94a3b8" font-size="7">Pure Cyclohexane T_f° = 6.550 °C</text>';

 // Solution cooling curve showing supercooling & rebound
 const dropPix=Math.min(65, (dt_f/6.5)*60);
 const pY1=axY+25,pY2=axY+60+dropPix,pY3=axY+80+dropPix,pY4=axY+50+dropPix,pY5=axY+58+dropPix;
 svg+='<path d="M'+axX+' '+pY1+' L'+(axX+55)+' '+pY2+' L'+(axX+75)+' '+pY3+' L'+(axX+90)+' '+pY4+' L'+(axX+axW)+' '+pY5+'" fill="none" stroke="#38bdf8" stroke-width="2"/>';

 // Supercooling dip annotation
 svg+='<circle cx="'+(axX+75)+'" cy="'+pY3+'" r="3" fill="#ef4444"/>';
 svg+='<text x="'+(axX+75)+'" y="'+(pY3+12)+'" text-anchor="middle" fill="#ef4444" font-size="7">Supercooling Dip (~0.5 °C)</text>';

 // Extrapolation line of crystallization plateau
 svg+='<line x1="'+(axX+65)+'" y1="'+pY4+'" x2="'+(axX+axW)+'" y2="'+pY5+'" stroke="#facc15" stroke-width="1.5" stroke-dasharray="2,2"/>';
 svg+='<text x="'+(axX+axW-5)+'" y="'+(pY4-5)+'" text-anchor="end" fill="#facc15" font-size="7.5" font-weight="bold">Extrapolated Equilibrium T_f = '+(6.550-dt_f).toFixed(3)+' °C</text>';

 // Bottom delta T badge
 svg+='<rect x="'+(lX+15)+'" y="'+(lY+190)+'" width="'+(lW-30)+'" height="30" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg+='<text x="'+(lX+lW/2)+'" y="'+(lY+208)+'" text-anchor="middle" fill="#86efac" font-size="8" font-family="monospace" font-weight="bold">Measured Freezing Depression: ΔT_f = T_f° − T_f = '+dt_f.toFixed(3)+' °C</text>';


 // Right Panel: Phase Diagram & Error Sensitivity Audit
 const rX=380,rY=46,rW=315,rH=230;
 svg+='<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg+='<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="10" font-weight="bold">COLLIGATIVE MECHANISM & ERROR AUDIT</text>';

 const errItems=[
  {label:'K_f Plastic Crystal (20.00)',desc:'ΔH_fus = 2.68 kJ/mol gives 10× higher resolution than water',val:'K_f = 20.00 K·kg/mol',col:'#48bb78'},
  {label:'Supercooling Extrapolation',desc:'Linear plateau extrapolation removes kinetic undercooling',val:'±0.004 °C Precision',col:'#38bdf8'},
  {label:'Solute Monomer Ideality',desc:'Biphenyl lacks H-bonding; discrete monomers (i = 1.000)',val:'Zero Dimerization Error',col:'#86efac'},
  {label:'Solvent Volatility Headspace',desc:'Cyclohexane vapor (40 mmHg at 6 °C) sealed in side arm',val:'Prevented by ground stopper',col:'#fbbf24'},
  {label:'OLS Slope Insulation (★)',desc:'Beckmann zero-setting calibration absorbed into ΔT₀',val:'Slope = 5.1873 °C/g Unbiased',col:'#86efac'}
 ];

 errItems.forEach((ei,idx)=>{
  const ey=rY+30+idx*39;
  svg+='<rect x="'+(rX+8)+'" y="'+ey+'" width="'+(rW-16)+'" height="33" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+12)+'" fill="'+ei.col+'" font-size="7.5" font-weight="bold">'+ei.label+'</text>';
  svg+='<text x="'+(rX+14)+'" y="'+(ey+25)+'" fill="#94a3b8" font-size="6.8">'+ei.desc+'</text>';
  svg+='<text x="'+(rX+rW-14)+'" y="'+(ey+12)+'" text-anchor="end" fill="'+ei.col+'" font-size="7.5" font-family="monospace">'+ei.val+'</text>';
 });

 svg+=text(360,305,'Molar Mass Invariant: Ordinary least-squares regression slope m_slope = 5.1873 °C/g isolates M = 154.22 g/mol.','#789c80',9);
 return svg;
}


// --- LAB 11: ENTHALPY OF NEUTRALIZATION VIA SOLUTION CALORIMETRY ---

function drawCalorimetryBenchView(p, rawVal){
 const n = (p && p.input) ? p.input : 0.040;
 const C_eff = 0.44365;
 const dt = rawVal !== null ? rawVal : (55.84 * n / C_eff);
 const T_init = 25.000;
 const T_max = T_init + dt;
 const q_rxn = C_eff * dt;
 const dH = -q_rxn / n;

 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'CONSTANT-PRESSURE SOLUTION CALORIMETER (DEWAR FLASK ASSEMBLY)', '#4ade80', 13);
 svg += text(360, 39, 'H3O+(aq) + OH-(aq) -> 2 H2O(l) | Net Molar Enthalpy of Neutralization ΔH_neut° = -55.84 kJ/mol', '#94a3b8', 9);

 // --- LEFT PANEL: VACUUM DEWAR FLASK CROSS-SECTION ---
 const dX = 140, dY = 70;
 // Outer calorimeter casing
 svg += '<rect x="'+(dX-65)+'" y="'+(dY+20)+'" width="130" height="180" rx="8" fill="#1e293b" stroke="#334155" stroke-width="2"/>';
 svg += '<text x="'+dX+'" y="'+(dY+190)+'" text-anchor="middle" fill="#64748b" font-size="7.5">Double-Walled Outer Protective Casing</text>';

 // Silvered vacuum jacket
 svg += '<path d="M '+(dX-52)+' '+(dY+30)+' L '+(dX-52)+' '+(dY+165)+' Q '+(dX-52)+' '+(dY+175)+' '+(dX-42)+' '+(dY+175)+' L '+(dX+42)+' '+(dY+175)+' Q '+(dX+52)+' '+(dY+175)+' '+(dX+52)+' '+(dY+165)+' L '+(dX+52)+' '+(dY+30)+'" fill="none" stroke="#94a3b8" stroke-width="5" stroke-opacity="0.4"/>';
 svg += '<path d="M '+(dX-46)+' '+(dY+30)+' L '+(dX-46)+' '+(dY+160)+' Q '+(dX-46)+' '+(dY+168)+' '+(dX-38)+' '+(dY+168)+' L '+(dX+38)+' '+(dY+168)+' Q '+(dX+46)+' '+(dY+168)+' '+(dX+46)+' '+(dY+30)+'" fill="#0b1712" stroke="#38bdf8" stroke-width="1.5"/>';

 // High vacuum space badge
 svg += '<text x="'+dX+'" y="'+(dY+50)+'" text-anchor="middle" fill="#38bdf8" font-size="7" opacity="0.6">EVACUATED VACUUM SPACE</text>';

 // Liquid fill (100 mL aqueous solution)
 const liqTop = dY + 90;
 svg += '<path d="M '+(dX-44)+' '+liqTop+' L '+(dX-44)+' '+(dY+158)+' Q '+(dX-44)+' '+(dY+166)+' '+(dX-36)+' '+(dY+166)+' L '+(dX+36)+' '+(dY+166)+' Q '+(dX+44)+' '+(dY+166)+' '+(dX+44)+' '+liqTop+' Z" fill="#0284c7" fill-opacity="0.35"/>';
 svg += '<ellipse cx="'+dX+'" cy="'+liqTop+'" rx="44" ry="4" fill="#38bdf8" fill-opacity="0.4"/>';
 svg += '<text x="'+dX+'" y="'+(liqTop+35)+'" text-anchor="middle" fill="#bae6fd" font-size="8" font-weight="bold">100.0 mL Mixed Solution</text>';
 svg += '<text x="'+dX+'" y="'+(liqTop+47)+'" text-anchor="middle" fill="#7dd3fc" font-size="7">50 mL HCl(aq) + 50 mL NaOH(aq)</text>';

 // Insulated PTFE lid
 svg += '<rect x="'+(dX-60)+'" y="'+(dY+15)+'" width="120" height="18" rx="3" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1.5"/>';
 svg += '<text x="'+(dX-40)+'" y="'+(dY+27)+'" fill="#1e293b" font-size="7" font-weight="bold">PTFE LID</text>';

 // Motorized Paddle Stirrer
 svg += '<rect x="'+(dX-20)+'" y="'+(dY-10)+'" width="5" height="150" fill="#94a3b8"/>';
 svg += '<rect x="'+(dX-30)+'" y="'+(dY+135)+'" width="25" height="8" rx="2" fill="#64748b"/>';
 // Motor head
 svg += '<rect x="'+(dX-28)+'" y="'+(dY-24)+'" width="21" height="16" rx="2" fill="#475569" stroke="#334155"/>';
 svg += '<text x="'+(dX-17)+'" y="'+(dY-13)+'" text-anchor="middle" fill="#f8fafc" font-size="6.5">200rpm</text>';

 // Digital Thermistor probe
 svg += '<rect x="'+(dX+14)+'" y="'+(dY+2)+'" width="4" height="135" rx="1.5" fill="#f59e0b"/>';
 svg += '<circle cx="'+(dX+16)+'" cy="'+(dY+137)+'" r="3" fill="#ef4444"/>';
 svg += '<path d="M '+(dX+16)+' '+(dY+2)+' Q '+(dX+25)+' '+(dY-20)+' '+(dX+70)+' '+(dY-15)+'" fill="none" stroke="#f59e0b" stroke-width="1.5"/>';

 // Reagent Pipette Dispenser (simulated)
 svg += '<path d="M '+(dX-42)+' '+(dY-15)+' L '+(dX-40)+' '+(dY+15)+'" stroke="#38bdf8" stroke-width="2" stroke-dasharray="3,2"/>';
 svg += '<text x="'+(dX-45)+'" y="'+(dY-18)+'" text-anchor="end" fill="#38bdf8" font-size="7">Class-A Pipette (50 mL)</text>';


 // --- RIGHT PANEL: THERMOMETRIC MONITOR & CALORIMETRIC AUDIT ---
 const rX = 260, rY = 55, rW = 435, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';

 // Digital Multimeter / Thermistor Readout
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+12)+'" width="200" height="72" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+26)+'" fill="#86efac" font-size="8" font-weight="bold">HIGH-PRECISION DIGITAL THERMISTOR</text>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+56)+'" fill="#facc15" font-size="22" font-family="monospace" font-weight="bold">'+T_max.toFixed(3)+' °C</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+44)+'" fill="#94a3b8" font-size="7.5">T_init = '+T_init.toFixed(3)+' °C</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+56)+'" fill="#4ade80" font-size="7.5" font-weight="bold">ΔT = +'+dt.toFixed(3)+' °C</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+68)+'" fill="#38bdf8" font-size="7">±0.001 °C Res.</text>';

 // Mini Live Heating Curve in top-right
 const cX = rX + 225, cY = rY + 12, cW = 195, cH = 72;
 svg += '<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(cX+8)+'" y="'+(cY+12)+'" fill="#94a3b8" font-size="7">Time-Temperature Response Profile</text>';
 // baseline
 svg += '<line x1="'+(cX+15)+'" y1="'+(cY+55)+'" x2="'+(cX+55)+'" y2="'+(cY+55)+'" stroke="#64748b" stroke-width="1.5"/>';
 // sharp exothermic rise
 const peakY = cY + 55 - Math.min(38, dt * 4.2);
 svg += '<path d="M '+(cX+55)+' '+(cY+55)+' Q '+(cX+65)+' '+(cY+55)+' '+(cX+75)+' '+peakY+'" fill="none" stroke="#ef4444" stroke-width="2"/>';
 // slow cooling tail
 svg += '<path d="M '+(cX+75)+' '+peakY+' L '+(cX+185)+' '+(peakY+6)+'" fill="none" stroke="#f59e0b" stroke-width="1.5"/>';
 svg += '<line x1="'+(cX+55)+'" y1="'+(cY+15)+'" x2="'+(cX+55)+'" y2="'+(cY+65)+'" stroke="#94a3b8" stroke-width="0.7" stroke-dasharray="2,2"/>';
 svg += '<text x="'+(cX+58)+'" y="'+(cY+23)+'" fill="#38bdf8" font-size="6.5">t_mix</text>';
 svg += '<text x="'+(cX+185)+'" y="'+(peakY-3)+'" text-anchor="end" fill="#facc15" font-size="6.8" font-weight="bold">Extrapolated ΔT = '+dt.toFixed(3)+' °C</text>';

 // Calorimetric Energy Balance Grid
 const gY = rY + 92;
 const metrics = [
  {label: 'Stoichiometric Moles n', val: n.toFixed(3) + ' mol H3O+/OH-', col: '#86efac', sub: 'n = V_acid · M_acid = 50.0 mL × M'},
  {label: 'System Heat Capacity C_eff', val: '0.44365 kJ/K (443.65 J/K)', col: '#38bdf8', sub: 'm_soln·c_p (416.15) + C_cal (27.50)'},
  {label: 'Thermal Energy Evolved q_cal', val: q_rxn.toFixed(4) + ' kJ (' + (q_rxn*1000).toFixed(1) + ' J)', col: '#facc15', sub: 'q_cal = C_eff · ΔT'},
  {label: 'Calculated Enthalpy ΔH_neut', val: dH.toFixed(2) + ' kJ/mol', col: '#f87171', sub: 'ΔH = -q_cal / n (Target: -55.84 kJ/mol)'}
 ];

 metrics.forEach((m, idx)=>{
  const mx = rX + 15 + (idx % 2) * 205;
  const my = gY + Math.floor(idx / 2) * 52;
  svg += '<rect x="'+mx+'" y="'+my+'" width="195" height="46" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+13)+'" fill="#94a3b8" font-size="7">'+m.label+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+28)+'" fill="'+m.col+'" font-size="9.5" font-weight="bold">'+m.val+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+39)+'" fill="#64748b" font-size="6.5">'+m.sub+'</text>';
 });

 // Bottom Verification Banner
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+200)+'" width="405" height="30" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
 svg += '<text x="'+(rX+217)+'" y="'+(rY+218)+'" text-anchor="middle" fill="#4ade80" font-size="8.5" font-family="monospace" font-weight="bold">Linear Regression Invariant: ΔT = 125.87 · n => ΔH_neut = -125.87 × 0.44365 = -55.84 kJ/mol (R² = 1.000)</text>';

 svg += text(360, 310, 'Constant-pressure solution calorimetry measures heat evolved directly in a calibrated vacuum Dewar assembly.', '#789c80', 8.5);
 return svg;
}

function drawCalorimetryCompareView(p, rawVal){
 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'CALORIMETRIC METHODS & ACID-BASE THERMODYNAMICS', '#4ade80', 13);
 svg += text(360, 39, 'Comparative Analysis of Calorimeters, Acid Strengths & Thermometric Enthalpy Profiles', '#94a3b8', 9);

 const cards = [
  {
   title: '1. Strong Acid + Strong Base',
   sub: 'HCl(aq) + NaOH(aq) -> NaCl + H2O',
   color: '#4ade80',
   border: '#166534',
   items: [
    'Net Ionic: H3O+(aq) + OH-(aq) -> 2 H2O(l)',
    'Standard Enthalpy: ΔH_neut° = -55.84 kJ/mol',
    'Spectator Ions: Na+ and Cl- remain hydrated without state change',
    'Invariant: Identical for HNO3, HClO4, HBr with KOH, LiOH',
    'Effective Heat Capacity: C_eff = m_soln·c_p + C_cal = 443.65 J/K',
    'Linearity: Adiabatic ΔT exhibits flawless R² = 1.000 vs moles'
   ]
  },
  {
   title: '2. Weak Acid + Strong Base',
   sub: 'CH3COOH(aq) + NaOH(aq) -> NaCH3COO + H2O',
   color: '#38bdf8',
   border: '#0369a1',
   items: [
    'Net Ionic: CH3COOH(aq) + OH-(aq) -> CH3COO-(aq) + H2O(l)',
    'Measured Enthalpy: ΔH_neut° = -56.10 kJ/mol',
    'Coupled Ionization: ΔH_neut = ΔH_water + ΔH_ioniz(CH3COOH)',
    'Weak Acid Ionization: ΔH_ioniz ≈ -0.26 kJ/mol (near zero due to entropy)',
    'Hydrogen Fluoride (HF): Strongly exothermic ionization (ΔH = -68.3 kJ/mol)',
    'HCN Neutralization: Endothermic ionization yields ΔH_neut = -12.1 kJ/mol'
   ]
  },
  {
   title: '3. Oxygen Bomb Calorimeter',
   sub: 'Constant-Volume Combustion Calorimetry',
   color: '#facc15',
   border: '#854d0e',
   items: [
    'Thermodynamic State: Constant Volume (ΔV = 0), measures ΔU_comb',
    'Conversion to Enthalpy: ΔH = ΔU + Δ(n_gas)·R·T',
    'Vessel Structure: Thick-walled stainless steel bomb pressurized to 30 atm O2',
    'Heat Capacity: Large water jacket (C_cal ≈ 10.5 kJ/K)',
    'Applications: Benzoic acid calibration, fuel calorific values, foods',
    'Versus Solution: High pressure, electrical ignition wire, dry combustion'
   ]
  }
 ];

 cards.forEach((c, idx)=>{
  const x = 20 + idx * 230, y = 50, w = 220, h = 240;
  svg += '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg += '<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="34" rx="4" fill="#051009"/>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9" font-weight="bold">'+c.title+'</text>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+35)+'" text-anchor="middle" fill="#94a3b8" font-size="7">'+c.sub+'</text>';

  c.items.forEach((item, ii)=>{
   const iy = y + 54 + ii * 29;
   svg += '<circle cx="'+(x+14)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg += '<foreignObject x="'+(x+22)+'" y="'+(iy-10)+'" width="'+(w-28)+'" height="29"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.2px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg += text(360, 305, 'Thermodynamic Invariant: Neutralization of any strong monoprotic acid by a strong base yields ΔH° = -55.84 kJ/mol.', '#789c80', 8.5);
 return svg;
}

function drawCalorimetrySandboxView(p, rawVal){
 const n = (p && p.input) ? p.input : 0.040;
 const C_eff = 0.44365;
 const dt = rawVal !== null ? rawVal : (55.84 * n / C_eff);
 const T_init = 25.000;
 const T_max_ad = T_init + dt;
 const T_obs_peak = T_max_ad - 0.085;

 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'ADIABATIC COOLING EXTRAPOLATION & REGNAULT-PFAUNDLER AUDIT', '#4ade80', 13);
 svg += text(360, 39, 'Graphical Newton Heat-Leak Correction for Quasi-Adiabatic Solution Calorimeters', '#94a3b8', 9);

 // --- LEFT PANEL: DETAILED TEMPERATURE-TIME GRAPH ---
 const lX = 25, lY = 50, lW = 390, lH = 240;
 svg += '<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">CALORIMETER THERMOGRAM & NEWTON COOLING FIT</text>';

 // Coordinate box inside left panel
 const gX = lX + 45, gY = lY + 35, gW = 325, gH = 155;
 svg += '<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#051009" stroke="#162e1e" stroke-width="1"/>';

 // Grid lines
 for(let gy = gY + 30; gy < gY + gH; gy += 30){
  svg += '<line x1="'+gX+'" y1="'+gy+'" x2="'+(gX+gW)+'" y2="'+gy+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
 }
 for(let gx = gX + 65; gx < gX + gW; gx += 65){
  svg += '<line x1="'+gx+'" y1="'+gY+'" x2="'+gx+'" y2="'+(gY+gH)+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
 }

 // Axes labels
 svg += '<text x="'+(gX+gW/2)+'" y="'+(gY+gH+14)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">Time t (seconds)</text>';
 svg += '<text x="'+(gX-8)+'" y="'+(gY+gH/2)+'" text-anchor="middle" transform="rotate(-90 '+(gX-8)+' '+(gY+gH/2)+')" fill="#94a3b8" font-size="7.5">Calorimeter Temperature T (°C)</text>';

 // Time ticks
 svg += '<text x="'+gX+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">0s</text>';
 svg += '<text x="'+(gX+65)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">180s (t_mix)</text>';
 svg += '<text x="'+(gX+130)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">360s</text>';
 svg += '<text x="'+(gX+195)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">540s</text>';
 svg += '<text x="'+(gX+gW)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">900s</text>';

 // Temperature curve calculation
 const yInit = gY + gH - 25;
 const yAdMax = yInit - Math.min(105, dt * 12.5);
 const yObsPeak = yAdMax + 10;
 const tMixX = gX + 65;
 const tMidX = gX + 90;

 // Pre-period baseline (slight drift)
 svg += '<line x1="'+gX+'" y1="'+yInit+'" x2="'+tMixX+'" y2="'+yInit+'" stroke="#38bdf8" stroke-width="2"/>';
 svg += '<text x="'+(gX+30)+'" y="'+(yInit-6)+'" fill="#38bdf8" font-size="6.5">Pre-Period Baseline</text>';

 // Reaction temperature rise
 svg += '<path d="M '+tMixX+' '+yInit+' Q '+(tMixX+15)+' '+(yInit-5)+' '+(tMixX+35)+' '+yObsPeak+'" fill="none" stroke="#ef4444" stroke-width="2.5"/>';

 // Post-period cooling line (real data)
 const postEndX = gX + gW - 10;
 const postEndY = yObsPeak + 14;
 svg += '<line x1="'+(tMixX+35)+'" y1="'+yObsPeak+'" x2="'+postEndX+'" y2="'+postEndY+'" stroke="#f59e0b" stroke-width="2"/>';
 svg += '<text x="'+(postEndX-10)+'" y="'+(postEndY-6)+'" text-anchor="end" fill="#f59e0b" font-size="6.5">Post-Period Cooling Tail</text>';

 // Backward linear extrapolation of post-period cooling tail to t_mid
 const extrapStartX = tMidX;
 const extrapStartY = yAdMax;
 svg += '<line x1="'+extrapStartX+'" y1="'+extrapStartY+'" x2="'+(tMixX+35)+'" y2="'+yObsPeak+'" stroke="#facc15" stroke-width="1.8" stroke-dasharray="3,2"/>';
 svg += '<circle cx="'+tMidX+'" cy="'+yAdMax+'" r="3.5" fill="#facc15"/>';
 svg += '<text x="'+(tMidX+8)+'" y="'+(yAdMax-4)+'" fill="#facc15" font-size="7" font-weight="bold">Adiabatic Extrapolation T_ad = '+T_max_ad.toFixed(3)+' °C</text>';

 // Vertical line at t_mid
 svg += '<line x1="'+tMidX+'" y1="'+gY+'" x2="'+tMidX+'" y2="'+(gY+gH)+'" stroke="#94a3b8" stroke-width="0.8" stroke-dasharray="2,2"/>';
 svg += '<text x="'+tMidX+'" y="'+(gY+12)+'" text-anchor="middle" fill="#94a3b8" font-size="6.5">t_mid (63.2% rise)</text>';

 // Bottom delta T badge
 svg += '<rect x="'+(lX+15)+'" y="'+(lY+198)+'" width="'+(lW-30)+'" height="32" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+218)+'" text-anchor="middle" fill="#86efac" font-size="8" font-family="monospace" font-weight="bold">Corrected Adiabatic Rise: ΔT_ad = T_ad − T_init = +'+dt.toFixed(3)+' °C</text>';


 // --- RIGHT PANEL: REGNAULT-PFAUNDLER CORRECTION AUDIT ---
 const rX = 425, rY = 50, rW = 275, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">HEAT LOSS & APPARATUS AUDIT</text>';

 const lossItems = [
  {label: 'Regnault-Pfaundler Extrapolation', desc: 'Eliminates Newton heat leak to room environment', val: '+0.085 °C Restored', col: '#4ade80'},
  {label: 'Dewar Vacuum Jacket', desc: 'Silvered double walls reflect radiative heat transfer', val: 'k = 0.0008 s⁻¹', col: '#38bdf8'},
  {label: 'PTFE Lid Insulation', desc: 'Low thermal conductivity prevents conduction to air', val: '< 0.01 W/m·K', col: '#86efac'},
  {label: 'Stirring Friction Bias', desc: 'Constant 200 rpm paddle induces <0.002 °C/min heating', val: 'Absorbed in baseline', col: '#fbbf24'},
  {label: 'OLS Regression Insulation', desc: 'Multi-point slope isolates ΔH independent of zero offset', val: 'R² = 1.00000 Unbiased', col: '#4ade80'}
 ];

 lossItems.forEach((li, idx)=>{
  const ly = rY + 30 + idx * 40;
  svg += '<rect x="'+(rX+8)+'" y="'+ly+'" width="'+(rW-16)+'" height="34" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+12)+'" fill="'+li.col+'" font-size="7.5" font-weight="bold">'+li.label+'</text>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+25)+'" fill="#94a3b8" font-size="6.8">'+li.desc+'</text>';
  svg += '<text x="'+(rX+rW-14)+'" y="'+(ly+12)+'" text-anchor="end" fill="'+li.col+'" font-size="7.5" font-family="monospace">'+li.val+'</text>';
 });

 svg += text(360, 305, 'Thermodynamic Invariant: Adiabatic extrapolation recovers true zero-leakage chemical enthalpy rise.', '#789c80', 8.5);
 return svg;
}


// --- LAB 12: HESS'S LAW CALORIMETRY (ENTHALPY OF FORMATION OF MgO) ---

function drawHessBenchView(p, rawVal){
 const m = (p && p.input) ? p.input : 0.200;
 const M_Mg = 24.305;
 const C_eff = 0.44365;
 const dt = rawVal !== null ? rawVal : (462.00 * m / (M_Mg * C_eff));
 const T_init = 25.000;
 const T_max = T_init + dt;
 const n_Mg = m / M_Mg;
 const q_rxn = C_eff * dt;
 const dH1 = -q_rxn / n_Mg;
 const dH2 = -146.00;
 const dH3 = -285.83;
 const dHf = dH1 - dH2 + dH3;

 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'HESS THERMOCHEMICAL CYCLE: ENTHALPY OF FORMATION OF MAGNESIUM OXIDE', '#4ade80', 13);
 svg += text(360, 39, 'Reaction 1: Mg(s) + 2 HCl(aq) -> MgCl2(aq) + H2(g) | Hess Target: Mg(s) + 1/2 O2(g) -> MgO(s)', '#94a3b8', 9);

 // --- LEFT PANEL: VACUUM DEWAR REACTION CELL WITH H2 EVOLUTION ---
 const dX = 140, dY = 70;
 // Outer protective jacket
 svg += '<rect x="'+(dX-65)+'" y="'+(dY+20)+'" width="130" height="180" rx="8" fill="#1e293b" stroke="#334155" stroke-width="2"/>';
 svg += '<text x="'+dX+'" y="'+(dY+190)+'" text-anchor="middle" fill="#64748b" font-size="7.5">Vacuum-Jacketed Reaction Cell</text>';

 // Silvered vacuum jacket
 svg += '<path d="M '+(dX-52)+' '+(dY+30)+' L '+(dX-52)+' '+(dY+165)+' Q '+(dX-52)+' '+(dY+175)+' '+(dX-42)+' '+(dY+175)+' L '+(dX+42)+' '+(dY+175)+' Q '+(dX+52)+' '+(dY+175)+' '+(dX+52)+' '+(dY+30)+'" fill="none" stroke="#94a3b8" stroke-width="5" stroke-opacity="0.4"/>';
 svg += '<path d="M '+(dX-46)+' '+(dY+30)+' L '+(dX-46)+' '+(dY+160)+' Q '+(dX-46)+' '+(dY+168)+' '+(dX-38)+' '+(dY+168)+' L '+(dX+38)+' '+(dY+168)+' Q '+(dX+46)+' '+(dY+168)+' '+(dX+46)+' '+(dY+30)+'" fill="#0b1712" stroke="#38bdf8" stroke-width="1.5"/>';

 // Liquid fill (100 mL 1.0 M HCl)
 const liqTop = dY + 90;
 svg += '<path d="M '+(dX-44)+' '+liqTop+' L '+(dX-44)+' '+(dY+158)+' Q '+(dX-44)+' '+(dY+166)+' '+(dX-36)+' '+(dY+166)+' L '+(dX+36)+' '+(dY+166)+' Q '+(dX+44)+' '+(dY+166)+' '+(dX+44)+' '+liqTop+' Z" fill="#0284c7" fill-opacity="0.3"/>';
 svg += '<ellipse cx="'+dX+'" cy="'+liqTop+'" rx="44" ry="4" fill="#38bdf8" fill-opacity="0.4"/>';
 svg += '<text x="'+dX+'" y="'+(liqTop+24)+'" text-anchor="middle" fill="#bae6fd" font-size="7.5" font-weight="bold">100.0 mL 1.0 M HCl(aq)</text>';

 // Evolving H2 bubbles rising through acid
 const bubbles = [
  {bx: dX - 18, by: liqTop + 55, r: 2.2},
  {bx: dX - 8,  by: liqTop + 38, r: 3.0},
  {bx: dX - 22, by: liqTop + 25, r: 2.5},
  {bx: dX + 12, by: liqTop + 48, r: 2.8},
  {bx: dX + 6,  by: liqTop + 30, r: 3.2},
  {bx: dX + 22, by: liqTop + 20, r: 2.0}
 ];
 bubbles.forEach(b=>{
  svg += '<circle cx="'+b.bx+'" cy="'+b.by+'" r="'+b.r+'" fill="#bae6fd" fill-opacity="0.7" stroke="#38bdf8" stroke-width="0.8"/>';
 });
 svg += '<text x="'+(dX-20)+'" y="'+(liqTop+42)+'" fill="#e0f2fe" font-size="6.5">H2(g) ↑</text>';

 // Dissolving Mg ribbon segments at bottom
 svg += '<rect x="'+(dX-18)+'" y="'+(dY+158)+'" width="12" height="3" rx="1" fill="#e2e8f0" stroke="#94a3b8"/>';
 svg += '<rect x="'+(dX+6)+'" y="'+(dY+160)+'" width="10" height="3" rx="1" fill="#cbd5e1" stroke="#94a3b8"/>';
 svg += '<text x="'+dX+'" y="'+(dY+170)+'" text-anchor="middle" fill="#cbd5e1" font-size="6.5">Polished Mg Ribbon</text>';

 // Insulated PTFE lid with vent port
 svg += '<rect x="'+(dX-60)+'" y="'+(dY+15)+'" width="120" height="18" rx="3" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1.5"/>';
 svg += '<text x="'+(dX-40)+'" y="'+(dY+27)+'" fill="#1e293b" font-size="7" font-weight="bold">PTFE LID</text>';

 // H2 Gas Vent Tube
 svg += '<rect x="'+(dX+32)+'" y="'+(dY-5)+'" width="6" height="22" fill="#94a3b8"/>';
 svg += '<path d="M '+(dX+35)+' '+(dY-5)+' Q '+(dX+45)+' '+(dY-18)+' '+(dX+65)+' '+(dY-16)+'" fill="none" stroke="#94a3b8" stroke-width="2"/>';
 svg += '<text x="'+(dX+70)+'" y="'+(dY-14)+'" fill="#38bdf8" font-size="6.5">Fume Hood Vent</text>';

 // Motorized Stirrer
 svg += '<rect x="'+(dX-5)+'" y="'+(dY-12)+'" width="4" height="145" fill="#94a3b8"/>';
 svg += '<rect x="'+(dX-12)+'" y="'+(dY+130)+'" width="18" height="7" rx="2" fill="#64748b"/>';
 // Stirrer motor
 svg += '<rect x="'+(dX-14)+'" y="'+(dY-24)+'" width="22" height="14" rx="2" fill="#475569" stroke="#334155"/>';
 svg += '<text x="'+(dX-3)+'" y="'+(dY-14)+'" text-anchor="middle" fill="#f8fafc" font-size="6">200rpm</text>';

 // Digital Thermistor probe
 svg += '<rect x="'+(dX+16)+'" y="'+(dY+5)+'" width="3" height="130" rx="1" fill="#f59e0b"/>';
 svg += '<circle cx="'+(dX+17)+'" cy="'+(dY+135)+'" r="2.8" fill="#ef4444"/>';
 svg += '<path d="M '+(dX+17)+' '+(dY+5)+' Q '+(dX+28)+' '+(dY-18)+' '+(dX+75)+' '+(dY-20)+'" fill="none" stroke="#f59e0b" stroke-width="1.5"/>';


 // --- RIGHT PANEL: DIGITAL THERMOMETER & THERMOCHEMICAL AUDIT ---
 const rX = 260, rY = 55, rW = 435, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';

 // Thermistor Display Readout
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+12)+'" width="200" height="72" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+26)+'" fill="#86efac" font-size="8" font-weight="bold">DIGITAL THERMISTOR (REACTION 1)</text>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+56)+'" fill="#facc15" font-size="22" font-family="monospace" font-weight="bold">'+T_max.toFixed(3)+' °C</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+44)+'" fill="#94a3b8" font-size="7.5">T_init = '+T_init.toFixed(3)+' °C</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+56)+'" fill="#ef4444" font-size="7.5" font-weight="bold">ΔT₁ = +'+dt.toFixed(3)+' °C</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+68)+'" fill="#38bdf8" font-size="7">±0.001 °C Res.</text>';

 // Mini Reaction Thermogram Profile
 const cX = rX + 225, cY = rY + 12, cW = 195, cH = 72;
 svg += '<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(cX+8)+'" y="'+(cY+12)+'" fill="#94a3b8" font-size="7">Dissolution Thermogram (Pre/Reaction/Post)</text>';
 // baseline
 svg += '<line x1="'+(cX+12)+'" y1="'+(cY+56)+'" x2="'+(cX+48)+'" y2="'+(cY+56)+'" stroke="#38bdf8" stroke-width="1.5"/>';
 // rapid rise
 const peakY = cY + 56 - Math.min(42, dt * 2.7);
 svg += '<path d="M '+(cX+48)+' '+(cY+56)+' Q '+(cX+56)+' '+(cY+56)+' '+(cX+72)+' '+peakY+'" fill="none" stroke="#ef4444" stroke-width="2"/>';
 // cooling tail
 svg += '<path d="M '+(cX+72)+' '+peakY+' L '+(cX+185)+' '+(peakY+8)+'" fill="none" stroke="#f59e0b" stroke-width="1.5"/>';
 svg += '<text x="'+(cX+185)+'" y="'+(peakY-3)+'" text-anchor="end" fill="#facc15" font-size="6.8" font-weight="bold">Extrapolated ΔT₁ = '+dt.toFixed(3)+' °C</text>';

 // Thermochemical State Matrix Grid
 const gY = rY + 92;
 const metrics = [
  {label: 'Magnesium Ribbon Mass m', val: m.toFixed(4) + ' g (' + (n_Mg*1000).toFixed(2) + ' mmol)', col: '#86efac', sub: 'n_Mg = m / 24.305 g/mol'},
  {label: 'Dissolution Enthalpy ΔH₁', val: dH1.toFixed(2) + ' kJ/mol', col: '#ef4444', sub: 'Mg + 2HCl -> MgCl2 + H2'},
  {label: 'Standard Oxide ΔH₂ & Water ΔH₃', val: 'ΔH₂ = −146.00 | ΔH₃ = −285.83', col: '#38bdf8', sub: 'MgO dissolution & H2O formation'},
  {label: 'Hess Formation Enthalpy ΔH_f°[MgO]', val: dHf.toFixed(2) + ' kJ/mol', col: '#facc15', sub: 'ΔH_f° = ΔH₁ − ΔH₂ + ΔH₃ (Lit: −601.83)'}
 ];

 metrics.forEach((mi, idx)=>{
  const mx = rX + 15 + (idx % 2) * 205;
  const my = gY + Math.floor(idx / 2) * 52;
  svg += '<rect x="'+mx+'" y="'+my+'" width="195" height="46" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+13)+'" fill="#94a3b8" font-size="7">'+mi.label+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+28)+'" fill="'+mi.col+'" font-size="9" font-weight="bold">'+mi.val+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+39)+'" fill="#64748b" font-size="6.5">'+mi.sub+'</text>';
 });

 // Bottom Verification Banner
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+200)+'" width="405" height="30" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
 svg += '<text x="'+(rX+217)+'" y="'+(rY+218)+'" text-anchor="middle" fill="#4ade80" font-size="8.2" font-family="monospace" font-weight="bold">Hess Law Invariant: ΔH_f° = −m_slope·(10.783) + 146.00 − 285.83 = −601.82 kJ/mol (R² = 1.000)</text>';

 svg += text(360, 310, 'Hess's Law couples solution calorimetry with standard thermochemical cycles to isolate formation enthalpies.', '#789c80', 8.5);
 return svg;
}

function drawHessCompareView(p, rawVal){
 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'THERMOCHEMICAL ROUTES TO MAGNESIUM OXIDE ENTHALPY', '#4ade80', 13);
 svg += text(360, 39, 'Hess Solution Cycle vs Direct Elemental Combustion vs Born-Haber Lattice Energy', '#94a3b8', 9);

 const cards = [
  {
   title: '1. Hess Solution Cycle (★)',
   sub: 'Room-Temperature Calorimetry',
   color: '#4ade80',
   border: '#166534',
   items: [
    'Cycle: ΔH_f° = ΔH₁(Mg) − ΔH₂(MgO) + ΔH₃(H₂O)',
    'Temperature: Room temperature (25.0 °C ambient)',
    'Safety: Controlled, non-explosive, gentle H2 evolution',
    'Stoichiometry: 100% complete dissolution in excess acid',
    'Apparatus: Low-cost Dewar flask + digital thermistor',
    'Accuracy: Multi-point regression R² = 1.000, error <0.02%'
   ]
  },
  {
   title: '2. Direct Elemental Combustion',
   sub: 'Mg(s) + 1/2 O2(g) -> MgO(s)',
   color: '#ef4444',
   border: '#7f1d1d',
   items: [
    'Reaction: Blinding, violent exothermic combustion',
    'Flame Temperature: T > 2800 °C (blinding UV emission)',
    'Physical Hazard: Severe burns, aerosolized white smoke',
    'Calorimetry Failure: Violent boiling & massive radiative loss',
    'Side Reaction: Forms magnesium nitride (3 Mg + N2 -> Mg3N2)',
    'Verdict: Impossible to measure directly in solution calorimeters'
   ]
  },
  {
   title: '3. Born-Haber Lattice Cycle',
   sub: 'Microscopic Ionic Bonding Cycle',
   color: '#facc15',
   border: '#854d0e',
   items: [
    'Cycle Steps: Sublimation + Ionization + Dissociation + EA + Lattice',
    'Sublimation of Mg(s): ΔH_sub = +147 kJ/mol',
    '1st + 2nd Ionization: IE₁ + IE₂ = +2189 kJ/mol',
    'O2 Dissociation + EA: 1/2 D_O2 + EA₁ + EA₂ = +897 kJ/mol',
    'Lattice Energy U_L: Highly exothermic U_L = −3840 kJ/mol',
    'Result: Sums to ΔH_f°[MgO] = −601 kJ/mol from fundamental physics'
   ]
  }
 ];

 cards.forEach((c, idx)=>{
  const x = 20 + idx * 230, y = 50, w = 220, h = 240;
  svg += '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg += '<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="34" rx="4" fill="#051009"/>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9" font-weight="bold">'+c.title+'</text>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+35)+'" text-anchor="middle" fill="#94a3b8" font-size="7">'+c.sub+'</text>';

  c.items.forEach((item, ii)=>{
   const iy = y + 54 + ii * 29;
   svg += '<circle cx="'+(x+14)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg += '<foreignObject x="'+(x+22)+'" y="'+(iy-10)+'" width="'+(w-28)+'" height="29"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.2px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg += text(360, 305, 'Thermodynamic Invariant: Hess's law bridges macroscopic bench calorimetry with microscopic lattice energy cycles.', '#789c80', 8.5);
 return svg;
}

function drawHessSandboxView(p, rawVal){
 const m = (p && p.input) ? p.input : 0.200;
 const M_Mg = 24.305;
 const C_eff = 0.44365;
 const dt = rawVal !== null ? rawVal : (462.00 * m / (M_Mg * C_eff));
 const n_Mg = m / M_Mg;
 const q_rxn = C_eff * dt;
 const dH1 = -q_rxn / n_Mg;
 const dH2 = -146.00;
 const dH3 = -285.83;
 const dHf = dH1 - dH2 + dH3;

 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'HESS STATE FUNCTION ENTHALPY LEVEL DIAGRAM & ERROR AUDIT', '#4ade80', 13);
 svg += text(360, 39, 'Path Independence of Enthalpy (∮ dH = 0) and Adiabatic Midpoint Correction', '#94a3b8', 9);

 // --- LEFT PANEL: ENTHALPY LEVEL DIAGRAM ---
 const lX = 25, lY = 50, lW = 390, lH = 240;
 svg += '<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">THERMODYNAMIC ENTHALPY LEVELS (kJ/mol)</text>';

 const eX = lX + 40, eW = 310;
 // Vertical Enthalpy Axis
 svg += '<line x1="'+eX+'" y1="'+(lY+35)+'" x2="'+eX+'" y2="'+(lY+205)+'" stroke="#94a3b8" stroke-width="1.5"/>';
 svg += '<polygon points="'+eX+','+(lY+30)+' '+(eX-4)+','+(lY+40)+' '+(eX+4)+','+(lY+40)+'" fill="#94a3b8"/>';
 svg += '<text x="'+(eX-8)+'" y="'+(lY+120)+'" text-anchor="middle" transform="rotate(-90 '+(eX-8)+' '+(lY+120)+')" fill="#94a3b8" font-size="7.5">Standard Enthalpy H° (kJ)</text>';

 // Levels
 // Level 0: Elements [Mg(s) + 2 HCl(aq) + 1/2 O2(g)] (Top datum: H = 0)
 const y0 = lY + 50;
 svg += '<line x1="'+(eX+10)+'" y1="'+y0+'" x2="'+(eX+eW)+'" y2="'+y0+'" stroke="#38bdf8" stroke-width="2"/>';
 svg += '<text x="'+(eX+15)+'" y="'+(y0-4)+'" fill="#38bdf8" font-size="7.5" font-weight="bold">Mg(s) + 2 HCl(aq) + 1/2 O₂(g) [Initial Elements]</text>';
 svg += '<text x="'+(eX+eW)+'" y="'+(y0-4)+'" text-anchor="end" fill="#94a3b8" font-size="7">H = 0 kJ</text>';

 // Level 1: Intermediate 1 [MgCl2(aq) + H2(g) + 1/2 O2(g)] (After Reaction 1: -462 kJ)
 const y1 = lY + 115;
 svg += '<line x1="'+(eX+10)+'" y1="'+y1+'" x2="'+(eX+eW)+'" y2="'+y1+'" stroke="#ef4444" stroke-width="2"/>';
 svg += '<text x="'+(eX+15)+'" y="'+(y1-4)+'" fill="#ef4444" font-size="7.5" font-weight="bold">MgCl₂(aq) + H₂(g) + 1/2 O₂(g) [Post-Reaction 1]</text>';
 svg += '<text x="'+(eX+eW)+'" y="'+(y1-4)+'" text-anchor="end" fill="#f87171" font-size="7">ΔH₁ = '+dH1.toFixed(1)+' kJ</text>';

 // Arrow 1: ΔH1 downwards
 svg += '<line x1="'+(eX+50)+'" y1="'+(y0+2)+'" x2="'+(eX+50)+'" y2="'+(y1-2)+'" stroke="#ef4444" stroke-width="1.8"/>';
 svg += '<polygon points="'+(eX+50)+','+y1+' '+(eX+46)+','+(y1-8)+' '+(eX+54)+','+(y1-8)+'" fill="#ef4444"/>';
 svg += '<text x="'+(eX+56)+'" y="'+((y0+y1)/2+3)+'" fill="#ef4444" font-size="7">ΔH₁ = −462.0 kJ</text>';

 // Level 2: Intermediate 2 [MgCl2(aq) + H2O(l)] (After Reaction 3: -462 - 285.8 = -747.8 kJ)
 const y2 = lY + 165;
 svg += '<line x1="'+(eX+10)+'" y1="'+y2+'" x2="'+(eX+eW)+'" y2="'+y2+'" stroke="#f59e0b" stroke-width="2"/>';
 svg += '<text x="'+(eX+15)+'" y="'+(y2-4)+'" fill="#f59e0b" font-size="7.5" font-weight="bold">MgCl₂(aq) + H₂O(l) [Deep Solution State]</text>';

 // Arrow 3: ΔH3 downwards
 svg += '<line x1="'+(eX+140)+'" y1="'+(y1+2)+'" x2="'+(eX+140)+'" y2="'+(y2-2)+'" stroke="#f59e0b" stroke-width="1.8"/>';
 svg += '<polygon points="'+(eX+140)+','+y2+' '+(eX+136)+','+(y2-8)+' '+(eX+144)+','+(y2-8)+'" fill="#f59e0b"/>';
 svg += '<text x="'+(eX+146)+'" y="'+((y1+y2)/2+3)+'" fill="#f59e0b" font-size="7">ΔH₃ = −285.8 kJ</text>';

 // Level 3: Target Product [MgO(s) + 2 HCl(aq)] (Step up from Level 2 by -ΔH2 = +146 kJ: -747.8 + 146 = -601.8 kJ)
 const y3 = lY + 140;
 svg += '<line x1="'+(eX+160)+'" y1="'+y3+'" x2="'+(eX+eW)+'" y2="'+y3+'" stroke="#4ade80" stroke-width="2.5"/>';
 svg += '<text x="'+(eX+170)+'" y="'+(y3-4)+'" fill="#4ade80" font-size="7.5" font-weight="bold">MgO(s) + 2 HCl(aq) [Target Formation State]</text>';

 // Arrow 2: -ΔH2 upwards
 svg += '<line x1="'+(eX+230)+'" y1="'+(y2-2)+'" x2="'+(eX+230)+'" y2="'+(y3+2)+'" stroke="#38bdf8" stroke-width="1.8"/>';
 svg += '<polygon points="'+(eX+230)+','+y3+' '+(eX+226)+','+(y3+8)+' '+(eX+234)+','+(y3+8)+'" fill="#38bdf8"/>';
 svg += '<text x="'+(eX+236)+'" y="'+((y2+y3)/2+3)+'" fill="#38bdf8" font-size="7">−ΔH₂ = +146.0 kJ</text>';

 // Target Direct Formation Arrow (from Level 0 directly to Level 3)
 svg += '<path d="M '+(eX+290)+' '+(y0+2)+' L '+(eX+290)+' '+(y3-2)+'" stroke="#facc15" stroke-width="2.5" stroke-dasharray="3,2"/>';
 svg += '<polygon points="'+(eX+290)+','+y3+' '+(eX+286)+','+(y3-8)+' '+(eX+294)+','+(y3-8)+'" fill="#facc15"/>';
 svg += '<text x="'+(eX+285)+'" y="'+((y0+y3)/2+3)+'" text-anchor="end" fill="#facc15" font-size="7.5" font-weight="bold">ΔH_f°[MgO] = −601.8 kJ</text>';

 // Bottom cycle formula
 svg += '<rect x="'+(lX+15)+'" y="'+(lY+198)+'" width="'+(lW-30)+'" height="32" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+218)+'" text-anchor="middle" fill="#86efac" font-size="8.2" font-family="monospace" font-weight="bold">∮ dH = ΔH₁ + ΔH₃ − ΔH₂ − ΔH_f° = 0 => ΔH_f° = −601.82 kJ/mol</text>';


 // --- RIGHT PANEL: SOURCES OF BIAS & MITIGATION AUDIT ---
 const rX = 425, rY = 50, rW = 275, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">SOURCES OF BIAS & SYSTEM AUDIT</text>';

 const lossItems = [
  {label: 'Magnesium Surface Oxide', desc: 'Emery cloth polishing removes unreactive MgO/Mg(OH)2', val: 'Passivation eliminated', col: '#4ade80'},
  {label: 'H2 Evaporative Carry-Out', desc: 'Vapor swept with gas carries ~18 J (<0.27% of total)', val: 'Linear in slope m', col: '#38bdf8'},
  {label: 'Regnault-Pfaundler Correction', desc: 'Newton cooling extrapolated to 63.2% reaction time', val: '+0.12 °C Restored', col: '#4ade80'},
  {label: 'Dewar Vacuum Jacket', desc: 'Silvered walls reflect radiative heat transfer', val: 'k = 0.0008 s⁻¹', col: '#86efac'},
  {label: 'Multi-Point OLS Regression', desc: 'Intercept absorbs baseline drift & zero errors', val: 'R² = 1.00000 Unbiased', col: '#facc15'}
 ];

 lossItems.forEach((li, idx)=>{
  const ly = rY + 30 + idx * 40;
  svg += '<rect x="'+(rX+8)+'" y="'+ly+'" width="'+(rW-16)+'" height="34" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+12)+'" fill="'+li.col+'" font-size="7.5" font-weight="bold">'+li.label+'</text>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+25)+'" fill="#94a3b8" font-size="6.8">'+li.desc+'</text>';
  svg += '<text x="'+(rX+rW-14)+'" y="'+(ly+12)+'" text-anchor="end" fill="'+li.col+'" font-size="7.5" font-family="monospace">'+li.val+'</text>';
 });

 svg += text(360, 305, 'Thermodynamic Invariant: Enthalpy state function eliminates kinetic and combustion path hazards.', '#789c80', 8.5);
 return svg;
}


// --- LAB 13: CONSTANT-VOLUME OXYGEN BOMB CALORIMETRY ---

function drawBombBenchView(p, rawVal){
 const m = (p && p.input) ? p.input : 1.000;
 const M_benzoic = 122.12;
 const C_cal = 10.500;
 const dt = rawVal !== null ? rawVal : (3227.0 * m / (M_benzoic * C_cal));
 const T_init = 25.000;
 const T_max = T_init + dt;
 const n_mol = m / M_benzoic;
 const q_rxn = C_cal * dt;
 const dU = -q_rxn / n_mol;
 const dH = dU - 1.24;

 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'CONSTANT-VOLUME OXYGEN BOMB CALORIMETER (PARR 1341 ASSEMBLY)', '#4ade80', 13);
 svg += text(360, 39, 'C7H6O2(s) + 15/2 O2(g, 30 atm) -> 7 CO2(g) + 3 H2O(l) | ΔV = 0 => q_v = ΔU_comb° = -3227.0 kJ/mol', '#94a3b8', 9);

 // --- LEFT PANEL: OXYGEN BOMB & WATER BUCKET CUTAWAY ---
 const bX = 140, bY = 70;
 // Outer insulated calorimeter jacket
 svg += '<rect x="'+(bX-75)+'" y="'+(bY+10)+'" width="150" height="195" rx="8" fill="#1e293b" stroke="#334155" stroke-width="2"/>';
 svg += '<text x="'+bX+'" y="'+(bY+198)+'" text-anchor="middle" fill="#64748b" font-size="7.5">Insulated Calorimeter Jacket</text>';

 // Distilled water bucket (2000.0 g H2O)
 svg += '<rect x="'+(bX-62)+'" y="'+(bY+26)+'" width="124" height="158" rx="5" fill="#0284c7" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1.2"/>';
 svg += '<text x="'+(bX-55)+'" y="'+(bY+38)+'" fill="#38bdf8" font-size="7">2000.0 g H2O</text>';

 // Stainless steel combustion bomb body
 const sX = bX, sY = bY + 55;
 svg += '<rect x="'+(sX-34)+'" y="'+sY+'" width="68" height="110" rx="6" fill="#475569" stroke="#94a3b8" stroke-width="2"/>';
 // Threaded bomb cap
 svg += '<rect x="'+(sX-37)+'" y="'+(sY-12)+'" width="74" height="16" rx="3" fill="#64748b" stroke="#cbd5e1" stroke-width="1.5"/>';
 svg += '<text x="'+sX+'" y="'+(sY-2)+'" text-anchor="middle" fill="#f8fafc" font-size="6.8" font-weight="bold">FORGED BOMB (30 atm O₂)</text>';

 // Bomb cavity interior
 svg += '<rect x="'+(sX-26)+'" y="'+(sY+8)+'" width="52" height="92" rx="3" fill="#0f172a"/>';

 // Base water (1.0 mL)
 svg += '<rect x="'+(sX-24)+'" y="'+(sY+92)+'" width="48" height="6" rx="1" fill="#38bdf8" fill-opacity="0.5"/>';

 // Combustion crucible and support ring
 svg += '<path d="M '+(sX-14)+' '+(sY+66)+' L '+(sX+14)+' '+(sY+66)+' L '+(sX+11)+' '+(sY+82)+' L '+(sX-11)+' '+(sY+82)+' Z" fill="#94a3b8" stroke="#cbd5e1" stroke-width="1"/>';

 // Benzoic acid pellet in crucible
 svg += '<rect x="'+(sX-7)+'" y="'+(sY+68)+'" width="14" height="10" rx="1.5" fill="#f8fafc" stroke="#e2e8f0" stroke-width="0.8"/>';
 // Incandescent combustion flame / glowing wire
 svg += '<circle cx="'+sX+'" cy="'+(sY+65)+'" r="5" fill="#facc15" fill-opacity="0.8"/>';
 svg += '<circle cx="'+sX+'" cy="'+(sY+65)+'" r="2.5" fill="#ef4444"/>';

 // Ignition electrodes & fuse wire
 svg += '<line x1="'+(sX-12)+'" y1="'+(sY+8)+'" x2="'+(sX-12)+'" y2="'+(sY+65)+'" stroke="#cbd5e1" stroke-width="1.5"/>';
 svg += '<line x1="'+(sX+12)+'" y1="'+(sY+8)+'" x2="'+(sX+12)+'" y2="'+(sY+65)+'" stroke="#cbd5e1" stroke-width="1.5"/>';
 svg += '<path d="M '+(sX-12)+' '+(sY+65)+' Q '+sX+' '+(sY+69)+' '+(sX+12)+' '+(sY+65)+'" fill="none" stroke="#ef4444" stroke-width="1.2"/>';

 // Oxygen valve and filling stem
 svg += '<rect x="'+(sX-4)+'" y="'+(sY-22)+'" width="8" height="12" fill="#94a3b8"/>';
 svg += '<circle cx="'+sX+'" cy="'+(sY-24)+'" r="4" fill="#38bdf8"/>';

 // Impeller stirrer shaft & blades in water bucket
 svg += '<rect x="'+(bX-48)+'" y="'+(bY+5)+'" width="3" height="150" fill="#94a3b8"/>';
 svg += '<ellipse cx="'+(bX-46)+'" cy="'+(bY+145)+'" rx="9" ry="3" fill="#64748b"/>';
 // Stirrer motor
 svg += '<rect x="'+(bX-55)+'" y="'+(bY-12)+'" width="18" height="14" rx="2" fill="#475569" stroke="#334155"/>';
 svg += '<text x="'+(bX-46)+'" y="'+(bY-2)+'" text-anchor="middle" fill="#f8fafc" font-size="6">400rpm</text>';

 // Thermistor probe in water
 svg += '<rect x="'+(bX+45)+'" y="'+(bY+15)+'" width="3.5" height="125" rx="1" fill="#f59e0b"/>';
 svg += '<circle cx="'+(bX+47)+'" cy="'+(bY+140)+'" r="2.8" fill="#ef4444"/>';
 svg += '<path d="M '+(bX+47)+' '+(bY+15)+' Q '+(bX+56)+' '+(bY-15)+' '+(bX+85)+' '+(bY-16)+'" fill="none" stroke="#f59e0b" stroke-width="1.5"/>';


 // --- RIGHT PANEL: DIGITAL DISPLAY & BOMB THERMOCHEMICAL AUDIT ---
 const rX = 260, rY = 55, rW = 435, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';

 // Thermistor Display Readout
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+12)+'" width="200" height="72" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+26)+'" fill="#86efac" font-size="8" font-weight="bold">BOMB WATER BATH THERMISTOR</text>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+56)+'" fill="#facc15" font-size="22" font-family="monospace" font-weight="bold">'+T_max.toFixed(3)+' °C</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+44)+'" fill="#94a3b8" font-size="7.5">T_init = '+T_init.toFixed(3)+' °C</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+56)+'" fill="#f87171" font-size="7.5" font-weight="bold">ΔT = +'+dt.toFixed(3)+' °C</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+68)+'" fill="#38bdf8" font-size="7">±0.001 °C Res.</text>';

 // Mini Reaction Thermogram Profile
 const cX = rX + 225, cY = rY + 12, cW = 195, cH = 72;
 svg += '<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(cX+8)+'" y="'+(cY+12)+'" fill="#94a3b8" font-size="7">Thermogram (Pre / 23V Fire / Post-Cooling)</text>';
 // baseline
 svg += '<line x1="'+(cX+12)+'" y1="'+(cY+56)+'" x2="'+(cX+45)+'" y2="'+(cY+56)+'" stroke="#38bdf8" stroke-width="1.5"/>';
 // steep exothermic rise
 const peakY = cY + 56 - Math.min(42, dt * 9.5);
 svg += '<path d="M '+(cX+45)+' '+(cY+56)+' Q '+(cX+52)+' '+(cY+56)+' '+(cX+68)+' '+peakY+'" fill="none" stroke="#ef4444" stroke-width="2"/>';
 // cooling tail
 svg += '<path d="M '+(cX+68)+' '+peakY+' L '+(cX+185)+' '+(peakY+6)+'" fill="none" stroke="#f59e0b" stroke-width="1.5"/>';
 svg += '<text x="'+(cX+185)+'" y="'+(peakY-3)+'" text-anchor="end" fill="#facc15" font-size="6.8" font-weight="bold">Extrapolated ΔT = '+dt.toFixed(3)+' °C</text>';

 // Thermochemical State Matrix Grid
 const gY = rY + 92;
 const metrics = [
  {label: 'Benzoic Acid Pellet Mass m', val: m.toFixed(4) + ' g (' + (n_mol*1000).toFixed(2) + ' mmol)', col: '#86efac', sub: 'NIST SRM 39j primary standard (M = 122.12)'},
  {label: 'Calorimeter Heat Capacity C_cal', val: '10.500 kJ/K (10500 J/K)', col: '#38bdf8', sub: '2000 g H2O (8368 J/K) + bomb (2132 J/K)'},
  {label: 'Internal Energy ΔU_comb', val: dU.toFixed(1) + ' kJ/mol', col: '#facc15', sub: 'ΔU = -C_cal · ΔT / n (Target: -3227.0)'},
  {label: 'Enthalpy of Combustion ΔH_comb°', val: dH.toFixed(1) + ' kJ/mol', col: '#f87171', sub: 'ΔH = ΔU + Δn_g·R·T (Δn_g = -0.5 mol)'}
 ];

 metrics.forEach((mi, idx)=>{
  const mx = rX + 15 + (idx % 2) * 205;
  const my = gY + Math.floor(idx / 2) * 52;
  svg += '<rect x="'+mx+'" y="'+my+'" width="195" height="46" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+13)+'" fill="#94a3b8" font-size="7">'+mi.label+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+28)+'" fill="'+mi.col+'" font-size="9" font-weight="bold">'+mi.val+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+39)+'" fill="#64748b" font-size="6.5">'+mi.sub+'</text>';
 });

 // Bottom Verification Banner
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+200)+'" width="405" height="30" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
 svg += '<text x="'+(rX+217)+'" y="'+(rY+218)+'" text-anchor="middle" fill="#4ade80" font-size="8.2" font-family="monospace" font-weight="bold">Constant-Volume Invariant: ΔT = 2.517 · m => ΔU_comb = -3227.3 kJ/mol (R² = 1.000)</text>';

 svg += text(360, 310, 'Constant-volume bomb calorimetry eliminates pressure-volume work (w = 0) so that q_v = ΔU_comb directly.', '#789c80', 8.5);
 return svg;
}

function drawBombCompareView(p, rawVal){
 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'COMPARATIVE ANALYSIS OF CALORIMETRIC METHODOLOGIES', '#4ade80', 13);
 svg += text(360, 39, 'Constant-Volume Oxygen Bomb vs Constant-Pressure Solution vs Differential Scanning (DSC)', '#94a3b8', 9);

 const cards = [
  {
   title: '1. Oxygen Bomb Calorimeter',
   sub: 'Constant-Volume Combustion (★)',
   color: '#4ade80',
   border: '#166534',
   items: [
    'Thermodynamic Boundary: Rigid steel walls (ΔV = 0)',
    'Mechanical Work: w = −∫ P dV = 0 identically',
    'Measured Heat: q_v = ΔU_comb (internal energy)',
    'Enthalpy Transform: ΔH = ΔU + Δ(n_gas)·R·T',
    'Operating Pressure: 30 atm (3.0 MPa) pure O2 gas',
    'Primary Standards: Benzoic acid (NIST SRM 39j)'
   ]
  },
  {
   title: '2. Solution Dewar Calorimeter',
   sub: 'Constant-Pressure Reaction',
   color: '#38bdf8',
   border: '#0369a1',
   items: [
    'Thermodynamic Boundary: Open / vented lid (P = 1 atm)',
    'Mechanical Work: w = −P_ext ΔV against atmospheric air',
    'Measured Heat: q_p = ΔH_rxn (enthalpy directly)',
    'Enthalpy Transform: No conversion needed; q_p = ΔH',
    'Operating Pressure: 1.0 atm ambient laboratory air',
    'Primary Applications: Neutralization, Hess cycles, heats of solution'
   ]
  },
  {
   title: '3. Differential Scanning (DSC)',
   sub: 'Dynamic Micro-Calorimetry',
   color: '#facc15',
   border: '#854d0e',
   items: [
    'Thermodynamic Mode: Controlled heating rate dT/dt',
    'Signal: Differential heat flow dH/dt vs inert reference',
    'Sample Mass: Microgram to milligram quantities (2–10 mg)',
    'Sensors: Platinum thermoelectric resistance transducers',
    'Primary Applications: Polymer glass transition Tg, melting Tm',
    'Kinetic Capability: Measures reaction activation energy Ea'
   ]
  }
 ];

 cards.forEach((c, idx)=>{
  const x = 20 + idx * 230, y = 50, w = 220, h = 240;
  svg += '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg += '<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="34" rx="4" fill="#051009"/>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9" font-weight="bold">'+c.title+'</text>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+35)+'" text-anchor="middle" fill="#94a3b8" font-size="7">'+c.sub+'</text>';

  c.items.forEach((item, ii)=>{
   const iy = y + 54 + ii * 29;
   svg += '<circle cx="'+(x+14)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg += '<foreignObject x="'+(x+22)+'" y="'+(iy-10)+'" width="'+(w-28)+'" height="29"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.2px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg += text(360, 305, 'Thermodynamic Distinction: Constant-volume measures ΔU (w = 0); constant-pressure measures ΔH (w = -PΔV).', '#789c80', 8.5);
 return svg;
}

function drawBombSandboxView(p, rawVal){
 const m = (p && p.input) ? p.input : 1.000;
 const M_benzoic = 122.12;
 const C_cal = 10.500;
 const dt = rawVal !== null ? rawVal : (3227.0 * m / (M_benzoic * C_cal));
 const n_mol = m / M_benzoic;
 const q_rxn = C_cal * dt;
 const dU = -q_rxn / n_mol;
 const dH = dU - 1.24;

 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'THERMODYNAMIC WORK CONVERSION & FUSE WIRE AUDIT', '#4ade80', 13);
 svg += text(360, 39, 'Legendre Transform (ΔH = ΔU + Δn_g·R·T) and Certified Thermochemical Corrections', '#94a3b8', 9);

 // --- LEFT PANEL: LEGENDRE TRANSFORM & WORK DIAGRAM ---
 const lX = 25, lY = 50, lW = 390, lH = 240;
 svg += '<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">PRESSURE-VOLUME WORK & STATE TRANSFORMATION</text>';

 // Reaction Stoichiometry Box
 svg += '<rect x="'+(lX+15)+'" y="'+(lY+30)+'" width="'+(lW-30)+'" height="32" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+45)+'" text-anchor="middle" fill="#38bdf8" font-size="8" font-weight="bold">C₇H₆O₂(s) + 7.5 O₂(g) ⟶ 7.0 CO₂(g) + 3.0 H₂O(l)</text>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+56)+'" text-anchor="middle" fill="#94a3b8" font-size="6.8">Gaseous Moles: n_reactants = 7.5 mol O₂  |  n_products = 7.0 mol CO₂</text>';

 // Gas Moles Contraction Calculation
 svg += '<rect x="'+(lX+15)+'" y="'+(lY+70)+'" width="'+(lW-30)+'" height="65" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg += '<text x="'+(lX+25)+'" y="'+(lY+84)+'" fill="#facc15" font-size="7.5" font-weight="bold">1. Gas Mole Contraction (Δn_gas):</text>';
 svg += '<text x="'+(lX+35)+'" y="'+(lY+96)+'" fill="#cbd5e1" font-size="7">Δn_gas = n_gas(products) − n_gas(reactants) = 7.0 − 7.5 = −0.5 mol</text>';
 svg += '<text x="'+(lX+25)+'" y="'+(lY+112)+'" fill="#facc15" font-size="7.5" font-weight="bold">2. Pressure-Volume Work Equivalent:</text>';
 svg += '<text x="'+(lX+35)+'" y="'+(lY+124)+'" fill="#cbd5e1" font-size="7">Δ(n_gas)·R·T = (−0.5 mol) × (8.3145 J/mol·K) × (298.15 K) = −1239.5 J = −1.24 kJ/mol</text>';

 // Conversion Formula
 svg += '<rect x="'+(lX+15)+'" y="'+(lY+142)+'" width="'+(lW-30)+'" height="48" rx="4" fill="#051009" stroke="#162e1e"/>';
 svg += '<text x="'+(lX+25)+'" y="'+(lY+156)+'" fill="#4ade80" font-size="8" font-weight="bold">3. Constant-Pressure Enthalpy of Combustion:</text>';
 svg += '<text x="'+(lX+35)+'" y="'+(lY+170)+'" fill="#86efac" font-size="7.5" font-family="monospace">ΔH_comb° = ΔU_comb° + Δn_g·R·T = '+dU.toFixed(1)+' + (−1.24) = '+dH.toFixed(1)+' kJ/mol</text>';
 svg += '<text x="'+(lX+35)+'" y="'+(lY+182)+'" fill="#94a3b8" font-size="6.8">Atmospheric compression adds 1.24 kJ/mol of boundary work to the system.</text>';

 // Bottom invariant
 svg += '<rect x="'+(lX+15)+'" y="'+(lY+198)+'" width="'+(lW-30)+'" height="32" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+218)+'" text-anchor="middle" fill="#86efac" font-size="8" font-family="monospace" font-weight="bold">Legendre Identity: H ≡ U + PV => ΔH_comb° = −3228.2 kJ/mol (Accepted NIST)</text>';


 // --- RIGHT PANEL: SOURCES OF BIAS & SYSTEM AUDIT ---
 const rX = 425, rY = 50, rW = 275, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">THERMOCHEMICAL AUDIT</text>';

 const lossItems = [
  {label: 'Ni-Cr Fuse Wire Heat', desc: '10 cm wire burned releases ~35.0 J (e_fuse = 9.6 J/cm)', val: 'Absorbed in intercept', col: '#4ade80'},
  {label: 'Nitric Acid Side-Reaction', desc: 'Trace N2 impurity forms HNO3 releasing ~15.0 J (titrated)', val: 'Absorbed in intercept', col: '#38bdf8'},
  {label: 'Regnault-Pfaundler Correction', desc: 'Newton cooling extrapolated to 63.2% reaction midpoint', val: '+0.025 °C Restored', col: '#4ade80'},
  {label: 'Pellet Compaction Force', desc: '5-ton pressing prevents particle splattering & soot', val: '100% Complete Deflagration', col: '#86efac'},
  {label: 'OLS Regression Insulation', desc: 'Slope m_slope isolates pure benzoic acid energy', val: 'R² = 1.00000 Unbiased', col: '#facc15'}
 ];

 lossItems.forEach((li, idx)=>{
  const ly = rY + 30 + idx * 40;
  svg += '<rect x="'+(rX+8)+'" y="'+ly+'" width="'+(rW-16)+'" height="34" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+12)+'" fill="'+li.col+'" font-size="7.5" font-weight="bold">'+li.label+'</text>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+25)+'" fill="#94a3b8" font-size="6.8">'+li.desc+'</text>';
  svg += '<text x="'+(rX+rW-14)+'" y="'+(ly+12)+'" text-anchor="end" fill="'+li.col+'" font-size="7.5" font-family="monospace">'+li.val+'</text>';
 });

 svg += text(360, 305, 'Thermodynamic Invariant: Multi-point regression purges fuse wire and nitric acid biases.', '#789c80', 8.5);
 return svg;
}


// --- LAB 14: HEAT OF SOLUTION VIA SOLUTION CALORIMETRY ---

function drawSolnBenchView(p, rawVal){
 const m = (p && p.input) ? p.input : 4.000;
 const M_KNO3 = 101.103;
 const C_eff = 0.44590;
 const dt_drop = rawVal !== null ? rawVal : (34.890 * m / (M_KNO3 * C_eff));
 const T_init = 25.000;
 const T_min = T_init - dt_drop;
 const n_mol = m / M_KNO3;
 const q_soln = C_eff * dt_drop;
 const dH = q_soln / n_mol;

 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'ENDOTHERMIC SOLUTION CALORIMETER (DEWAR FLASK CELL)', '#4ade80', 13);
 svg += text(360, 39, 'KNO3(s) + aq -> K+(aq) + NO3-(aq) | Endothermic Lattice-Hydration Enthalpy ΔH_soln° = +34.89 kJ/mol', '#94a3b8', 9);

 // --- LEFT PANEL: VACUUM DEWAR VESSEL WITH DISSOLVING CRYSTALS ---
 const dX = 140, dY = 70;
 // Outer protective jacket
 svg += '<rect x="'+(dX-65)+'" y="'+(dY+20)+'" width="130" height="180" rx="8" fill="#1e293b" stroke="#334155" stroke-width="2"/>';
 svg += '<text x="'+dX+'" y="'+(dY+190)+'" text-anchor="middle" fill="#64748b" font-size="7.5">Vacuum-Insulated Dewar Vessel</text>';

 // Silvered vacuum jacket
 svg += '<path d="M '+(dX-52)+' '+(dY+30)+' L '+(dX-52)+' '+(dY+165)+' Q '+(dX-52)+' '+(dY+175)+' '+(dX-42)+' '+(dY+175)+' L '+(dX+42)+' '+(dY+175)+' Q '+(dX+52)+' '+(dY+175)+' '+(dX+52)+' '+(dY+30)+'" fill="none" stroke="#94a3b8" stroke-width="5" stroke-opacity="0.4"/>';
 svg += '<path d="M '+(dX-46)+' '+(dY+30)+' L '+(dX-46)+' '+(dY+160)+' Q '+(dX-46)+' '+(dY+168)+' '+(dX-38)+' '+(dY+168)+' L '+(dX+38)+' '+(dY+168)+' Q '+(dX+46)+' '+(dY+168)+' '+(dX+46)+' '+(dY+30)+'" fill="#0b1712" stroke="#38bdf8" stroke-width="1.5"/>';

 // Liquid fill (100.0 mL H2O, chilled blue shade)
 const liqTop = dY + 90;
 svg += '<path d="M '+(dX-44)+' '+liqTop+' L '+(dX-44)+' '+(dY+158)+' Q '+(dX-44)+' '+(dY+166)+' '+(dX-36)+' '+(dY+166)+' L '+(dX+36)+' '+(dY+166)+' Q '+(dX+44)+' '+(dY+166)+' '+(dX+44)+' '+liqTop+' Z" fill="#0284c7" fill-opacity="0.4"/>';
 svg += '<ellipse cx="'+dX+'" cy="'+liqTop+'" rx="44" ry="4" fill="#38bdf8" fill-opacity="0.5"/>';
 svg += '<text x="'+dX+'" y="'+(liqTop+24)+'" text-anchor="middle" fill="#bae6fd" font-size="7.5" font-weight="bold">100.0 mL Aqueous Solution</text>';

 // Dissolving crystalline particles swirling in solvent
 const crystals = [
  {cx: dX - 18, cy: liqTop + 50, s: 3.5},
  {cx: dX - 5,  cy: liqTop + 62, s: 2.8},
  {cx: dX + 16, cy: liqTop + 45, s: 3.2},
  {cx: dX - 25, cy: liqTop + 35, s: 2.5},
  {cx: dX + 8,  cy: liqTop + 32, s: 3.0},
  {cx: dX + 22, cy: liqTop + 58, s: 2.4}
 ];
 crystals.forEach(c=>{
  svg += '<rect x="'+(c.cx-c.s/2)+'" y="'+(c.cy-c.s/2)+'" width="'+c.s+'" height="'+c.s+'" rx="0.5" fill="#f8fafc" stroke="#38bdf8" stroke-width="0.7"/>';
 });
 svg += '<text x="'+(dX-10)+'" y="'+(liqTop+44)+'" fill="#e0f2fe" font-size="6.5">KNO₃ Dissolving</text>';

 // Powder funnel in addition port
 svg += '<polygon points="'+(dX+32)+','+(dY-12)+' '+(dX+48)+','+(dY-12)+' '+(dX+42)+','+(dY+14)+' '+(dX+38)+','+(dY+14)+'" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1"/>';
 svg += '<text x="'+(dX+50)+'" y="'+(dY-8)+'" fill="#38bdf8" font-size="6.5">Powder Funnel</text>';

 // Insulated PTFE lid
 svg += '<rect x="'+(dX-60)+'" y="'+(dY+15)+'" width="120" height="18" rx="3" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1.5"/>';
 svg += '<text x="'+(dX-40)+'" y="'+(dY+27)+'" fill="#1e293b" font-size="7" font-weight="bold">PTFE LID</text>';

 // Motorized Paddle Stirrer
 svg += '<rect x="'+(dX-6)+'" y="'+(dY-12)+'" width="4" height="145" fill="#94a3b8"/>';
 svg += '<rect x="'+(dX-14)+'" y="'+(dY+130)+'" width="20" height="7" rx="2" fill="#64748b"/>';
 // Motor head
 svg += '<rect x="'+(dX-15)+'" y="'+(dY-24)+'" width="22" height="14" rx="2" fill="#475569" stroke="#334155"/>';
 svg += '<text x="'+(dX-4)+'" y="'+(dY-14)+'" text-anchor="middle" fill="#f8fafc" font-size="6">200rpm</text>';

 // Digital Thermistor probe
 svg += '<rect x="'+(dX+16)+'" y="'+(dY+5)+'" width="3" height="130" rx="1" fill="#f59e0b"/>';
 svg += '<circle cx="'+(dX+17)+'" cy="'+(dY+135)+'" r="2.8" fill="#ef4444"/>';
 svg += '<path d="M '+(dX+17)+' '+(dY+5)+' Q '+(dX+28)+' '+(dY-18)+' '+(dX+75)+' '+(dY-20)+'" fill="none" stroke="#f59e0b" stroke-width="1.5"/>';


 // --- RIGHT PANEL: DIGITAL DISPLAY & ENDOTHERMIC AUDIT ---
 const rX = 260, rY = 55, rW = 435, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';

 // Thermistor Display Readout (chilled reading)
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+12)+'" width="200" height="72" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+26)+'" fill="#86efac" font-size="8" font-weight="bold">DIGITAL THERMISTOR (ENDOTHERMIC)</text>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+56)+'" fill="#38bdf8" font-size="22" font-family="monospace" font-weight="bold">'+T_min.toFixed(3)+' °C</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+44)+'" fill="#94a3b8" font-size="7.5">T_init = '+T_init.toFixed(3)+' °C</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+56)+'" fill="#38bdf8" font-size="7.5" font-weight="bold">ΔT = −'+dt_drop.toFixed(3)+' °C</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+68)+'" fill="#86efac" font-size="7">±0.001 °C Res.</text>';

 // Mini Reaction Thermogram Profile (cooling curve)
 const cX = rX + 225, cY = rY + 12, cW = 195, cH = 72;
 svg += '<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(cX+8)+'" y="'+(cY+12)+'" fill="#94a3b8" font-size="7">Thermogram (Pre / Endothermic Drop / Re-warm)</text>';
 // baseline
 svg += '<line x1="'+(cX+12)+'" y1="'+(cY+28)+'" x2="'+(cX+45)+'" y2="'+(cY+28)+'" stroke="#38bdf8" stroke-width="1.5"/>';
 // steep endothermic drop
 const bottomY = cY + 28 + Math.min(36, dt_drop * 6.5);
 svg += '<path d="M '+(cX+45)+' '+(cY+28)+' Q '+(cX+52)+' '+(cY+28)+' '+(cX+68)+' '+bottomY+'" fill="none" stroke="#38bdf8" stroke-width="2"/>';
 // slow ambient re-warming tail upwards
 svg += '<path d="M '+(cX+68)+' '+bottomY+' L '+(cX+185)+' '+(bottomY-6)+'" fill="none" stroke="#f59e0b" stroke-width="1.5"/>';
 svg += '<text x="'+(cX+185)+'" y="'+(bottomY+8)+'" text-anchor="end" fill="#facc15" font-size="6.8" font-weight="bold">Extrapolated ΔT_drop = '+dt_drop.toFixed(3)+' °C</text>';

 // Thermochemical State Matrix Grid
 const gY = rY + 92;
 const metrics = [
  {label: 'Potassium Nitrate Mass m', val: m.toFixed(4) + ' g (' + (n_mol*1000).toFixed(2) + ' mmol)', col: '#86efac', sub: 'n = m / 101.103 g/mol'},
  {label: 'Calorimeter Heat Capacity C_eff', val: '0.44590 kJ/K (445.9 J/K)', col: '#38bdf8', sub: '100 g H2O (418.4) + Dewar body (27.5)'},
  {label: 'Thermal Energy Absorbed q_soln', val: q_soln.toFixed(4) + ' kJ (' + (q_soln*1000).toFixed(1) + ' J)', col: '#38bdf8', sub: 'q_soln = C_eff · ΔT_drop'},
  {label: 'Integral Enthalpy ΔH_soln°', val: '+' + dH.toFixed(2) + ' kJ/mol', col: '#facc15', sub: 'ΔH = q_soln / n (Target: +34.89 kJ/mol)'}
 ];

 metrics.forEach((mi, idx)=>{
  const mx = rX + 15 + (idx % 2) * 205;
  const my = gY + Math.floor(idx / 2) * 52;
  svg += '<rect x="'+mx+'" y="'+my+'" width="195" height="46" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+13)+'" fill="#94a3b8" font-size="7">'+mi.label+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+28)+'" fill="'+mi.col+'" font-size="9" font-weight="bold">'+mi.val+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+39)+'" fill="#64748b" font-size="6.5">'+mi.sub+'</text>';
 });

 // Bottom Verification Banner
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+200)+'" width="405" height="30" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
 svg += '<text x="'+(rX+217)+'" y="'+(rY+218)+'" text-anchor="middle" fill="#4ade80" font-size="8.2" font-family="monospace" font-weight="bold">Linear Regression Invariant: ΔT_drop = 0.7739 · m => ΔH_soln° = +34.89 kJ/mol (R² = 1.000)</text>';

 svg += text(360, 310, 'Endothermic dissolution absorbs thermal energy from the solvent, lowering temperature in proportion to solute mass.', '#789c80', 8.5);
 return svg;
}

function drawSolnCompareView(p, rawVal){
 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'ELECTROLYTE DISSOLUTION THERMODYNAMICS & SOLVATION CYCLES', '#4ade80', 13);
 svg += text(360, 39, 'Integral vs Differential Heat of Solution vs Born-Haber Solvation Partitioning', '#94a3b8', 9);

 const cards = [
  {
   title: '1. Integral Heat of Solution',
   sub: 'ΔH_int = q_p / n_solute',
   color: '#4ade80',
   border: '#166534',
   items: [
    'Definition: Total heat evolved/absorbed dissolving 1 mol in finite solvent',
    'Concentration: Dependent on final molality m (kJ per mol solute)',
    'Infinite Dilution: Approaches standard limiting value ΔH_soln° as m -> 0',
    'Calorimetric Signal: Directly measured from observed ΔT_drop',
    'Potassium Nitrate: ΔH_soln° = +34.89 kJ/mol (endothermic cooling)',
    'Linearity: Ideal Henry-Debye behavior across 0.2 to 0.7 mol/kg'
   ]
  },
  {
   title: '2. Differential Heat of Solution',
   sub: 'ΔH_diff = (∂H / ∂n₂)_P,T,n₁',
   color: '#38bdf8',
   border: '#0369a1',
   items: [
    'Definition: Incremental enthalpy change adding 1 mol to infinite solution',
    'Partial Molar Quantity: Equal to H̄₂ − H₂* (solute partial molar enthalpy)',
    'Concentration Derivative: ΔH_diff = ΔH_int + n₂ · (dΔH_int / dn₂)',
    'Infinite Dilution Limit: Identical to integral heat at m = 0',
    'Physical Meaning: Energetics of inserting solute into pre-formed solution',
    'Applications: Industrial crystallizers, evaporators, phase equilibria'
   ]
  },
  {
   title: '3. Born Solvation Energetics',
   sub: 'ΔH_soln = ΔH_lattice + ΔH_hyd',
   color: '#facc15',
   border: '#854d0e',
   items: [
    'Crystal Lattice Energy: KNO3(s) -> K+(g) + NO3-(g) (ΔH_L = +687.0 kJ/mol)',
    'Ion Hydration Enthalpy: K+(g) + NO3-(g) -> aq (ΔH_hyd = −652.1 kJ/mol)',
    'Enthalpic Deficit: Lattice cost exceeds hydration by +34.89 kJ/mol',
    'Entropic Driving Force: Crystal breakdown yields ΔS_soln ≈ +115 J/(mol·K)',
    'Gibbs Free Energy: ΔG = ΔH − TΔS = +34.9 − (298 × 0.115) = −0.6 kJ/mol < 0',
    'Exothermic Contrast: CaCl2 dissolves exothermically (ΔH = −82.8 kJ/mol)'
   ]
  }
 ];

 cards.forEach((c, idx)=>{
  const x = 20 + idx * 230, y = 50, w = 220, h = 240;
  svg += '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg += '<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="34" rx="4" fill="#051009"/>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9" font-weight="bold">'+c.title+'</text>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+35)+'" text-anchor="middle" fill="#94a3b8" font-size="7">'+c.sub+'</text>';

  c.items.forEach((item, ii)=>{
   const iy = y + 54 + ii * 29;
   svg += '<circle cx="'+(x+14)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg += '<foreignObject x="'+(x+22)+'" y="'+(iy-10)+'" width="'+(w-28)+'" height="29"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.2px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg += text(360, 305, 'Thermodynamic Invariant: Endothermic dissolution (ΔH > 0) is driven spontaneously by large positive entropy (ΔS > 0).', '#789c80', 8.5);
 return svg;
}

function drawSolnSandboxView(p, rawVal){
 const m = (p && p.input) ? p.input : 4.000;
 const M_KNO3 = 101.103;
 const C_eff = 0.44590;
 const dt_drop = rawVal !== null ? rawVal : (34.890 * m / (M_KNO3 * C_eff));
 const n_mol = m / M_KNO3;
 const q_soln = C_eff * dt_drop;
 const dH = q_soln / n_mol;

 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'VAN 'T HOFF SOLUBILITY DEPENDENCE & HEAT-LEAK EXTRAPOLATION', '#4ade80', 13);
 svg += text(360, 39, 'd(ln K_sp)/dT = ΔH_soln° / (R T²) and Newton Inward Heat Leak Correction', '#94a3b8', 9);

 // --- LEFT PANEL: TEMPERATURE-DEPENDENT SOLUBILITY CURVE ---
 const lX = 25, lY = 50, lW = 390, lH = 240;
 svg += '<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">VAN 'T HOFF SOLUBILITY PROFILE (g KNO₃ / 100 g H₂O)</text>';

 const gX = lX + 45, gY = lY + 35, gW = 325, gH = 155;
 svg += '<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#051009" stroke="#162e1e" stroke-width="1"/>';

 // Grid lines
 for(let gy = gY + 30; gy < gY + gH; gy += 30){
  svg += '<line x1="'+gX+'" y1="'+gy+'" x2="'+(gX+gW)+'" y2="'+gy+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
 }
 for(let gx = gX + 65; gx < gX + gW; gx += 65){
  svg += '<line x1="'+gx+'" y1="'+gY+'" x2="'+gx+'" y2="'+(gY+gH)+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
 }

 // Axes labels
 svg += '<text x="'+(gX+gW/2)+'" y="'+(gY+gH+14)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">Solution Temperature T (°C)</text>';
 svg += '<text x="'+(gX-8)+'" y="'+(gY+gH/2)+'" text-anchor="middle" transform="rotate(-90 '+(gX-8)+' '+(gY+gH/2)+')" fill="#94a3b8" font-size="7.5">Solubility S (g/100g H₂O)</text>';

 // Ticks
 svg += '<text x="'+gX+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">0 °C</text>';
 svg += '<text x="'+(gX+65)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">25 °C</text>';
 svg += '<text x="'+(gX+130)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">50 °C</text>';
 svg += '<text x="'+(gX+195)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">75 °C</text>';
 svg += '<text x="'+(gX+gW)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">100 °C</text>';

 // Exponential steep solubility curve for KNO3: 0C->13.3g, 25C->38g, 50C->85g, 75C->155g, 100C->246g
 const p0 = {x: gX, y: gY + gH - 10};
 const p25 = {x: gX + 65, y: gY + gH - 26};
 const p50 = {x: gX + 130, y: gY + gH - 55};
 const p75 = {x: gX + 195, y: gY + gH - 98};
 const p100 = {x: gX + gW, y: gY + 12};

 svg += '<path d="M '+p0.x+' '+p0.y+' Q '+(p25.x-10)+' '+p25.y+' '+p25.x+' '+p25.y+' T '+p50.x+' '+p50.y+' T '+p75.x+' '+p75.y+' T '+p100.x+' '+p100.y+'" fill="none" stroke="#facc15" stroke-width="2.5"/>';
 svg += '<circle cx="'+p25.x+'" cy="'+p25.y+'" r="3" fill="#4ade80"/>';
 svg += '<text x="'+(p25.x+8)+'" y="'+(p25.y-4)+'" fill="#4ade80" font-size="7" font-weight="bold">25 °C: 38 g/100g (ΔH° = +34.9 kJ)</text>';
 svg += '<circle cx="'+p100.x+'" cy="'+p100.y+'" r="3" fill="#ef4444"/>';
 svg += '<text x="'+(p100.x-8)+'" y="'+(p100.y+12)+'" text-anchor="end" fill="#f87171" font-size="7">100 °C: 246 g/100g</text>';

 // Bottom delta T badge
 svg += '<rect x="'+(lX+15)+'" y="'+(lY+198)+'" width="'+(lW-30)+'" height="32" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+218)+'" text-anchor="middle" fill="#86efac" font-size="8" font-family="monospace" font-weight="bold">Van 't Hoff Relation: d(ln K_sp)/dT > 0 due to positive endothermic ΔH_soln°</text>';


 // --- RIGHT PANEL: SOURCES OF BIAS & SYSTEM AUDIT ---
 const rX = 425, rY = 50, rW = 275, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">SOURCES OF BIAS & SYSTEM AUDIT</text>';

 const lossItems = [
  {label: 'Inward Newton Heat Leak', desc: 'Room air warms cold solution; extrapolated to 63.2% t_mid', val: '+0.09 °C Restored', col: '#4ade80'},
  {label: 'Crystal Moisture Absence', desc: 'Dried at 110 °C and stored in desiccator prevents hydrate bias', val: 'Pure anhydrous salt', col: '#38bdf8'},
  {label: 'Stirrer Dissipation Heat', desc: 'Constant 200 rpm paddle imparts ~0.02 W mechanical heat', val: 'Absorbed in intercept', col: '#86efac'},
  {label: 'Solvent Volumetric Delivery', desc: 'Class-A 100.00 mL pipette delivers exactly 100.0 g H2O', val: 'δV/V = 0.05%', col: '#facc15'},
  {label: 'Multi-Point OLS Regression', desc: 'Slope eliminates zero-datum and crystal entry offsets', val: 'R² = 1.00000 Unbiased', col: '#4ade80'}
 ];

 lossItems.forEach((li, idx)=>{
  const ly = rY + 30 + idx * 40;
  svg += '<rect x="'+(rX+8)+'" y="'+ly+'" width="'+(rW-16)+'" height="34" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+12)+'" fill="'+li.col+'" font-size="7.5" font-weight="bold">'+li.label+'</text>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+25)+'" fill="#94a3b8" font-size="6.8">'+li.desc+'</text>';
  svg += '<text x="'+(rX+rW-14)+'" y="'+(ly+12)+'" text-anchor="end" fill="'+li.col+'" font-size="7.5" font-family="monospace">'+li.val+'</text>';
 });

 svg += text(360, 305, 'Thermodynamic Invariant: Regnault-Pfaundler extrapolation restores true adiabatic temperature depression.', '#789c80', 8.5);
 return svg;
}


// --- LAB 15: CLAUSIUS-CLAPEYRON VAPOR PRESSURE & ENTHALPY OF VAPORIZATION ---

function drawVapBenchView(p, rawVal){
 const t = (p && p.input) ? p.input : 50.0;
 const T_K = t + 273.15;
 const inv_T = 1000.0 / T_K;
 const R = 8.31446;
 const dH = 38560.0;
 const Tb = 351.52;
 const Pb = 101.325;
 const ln_P_calc = Math.log(Pb) - (dH / R) * (1.0 / T_K - 1.0 / Tb);
 const P = rawVal !== null ? rawVal : Math.exp(ln_P_calc);
 const ln_P = Math.log(P);
 const P_mmHg = P * 7.50062;

 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'STATIC ISOTENISCOPE APPARATUS (LIQUID-VAPOR EQUILIBRIUM)', '#4ade80', 13);
 svg += text(360, 39, 'C2H5OH(l) <=> C2H5OH(g) | Clausius-Clapeyron Enthalpy of Vaporization ΔH_vap° = 38.56 kJ/mol', '#94a3b8', 9);

 // --- LEFT PANEL: SUBMERGED ISOTENISCOPE IN WATER BATH ---
 const iX = 140, iY = 70;
 // Water bath tank (transparent glass)
 svg += '<rect x="'+(iX-70)+'" y="'+(iY+20)+'" width="140" height="180" rx="8" fill="#0284c7" fill-opacity="0.15" stroke="#38bdf8" stroke-width="1.8"/>';
 svg += '<text x="'+iX+'" y="'+(iY+190)+'" text-anchor="middle" fill="#64748b" font-size="7.5">Thermostatted Water Bath ('+t.toFixed(1)+' °C)</text>';

 // Liquid level in bath
 svg += '<line x1="'+(iX-68)+'" y1="'+(iY+35)+'" x2="'+(iX+68)+'" y2="'+(iY+35)+'" stroke="#38bdf8" stroke-width="1" stroke-dasharray="3,2"/>';

 // Bath heater coil & impeller stirrer
 svg += '<path d="M '+(iX-55)+' '+(iY+50)+' L '+(iX-55)+' '+(iY+160)+' Q '+(iX-50)+' '+(iY+165)+' '+(iX-45)+' '+(iY+160)+' L '+(iX-45)+' '+(iY+50)+'" fill="none" stroke="#ef4444" stroke-width="2"/>';
 svg += '<text x="'+(iX-50)+'" y="'+(iY+45)+'" text-anchor="middle" fill="#ef4444" font-size="6">PID Heater</text>';

 // Glass Isoteniscope Cell Assembly
 // Reservoir bulb containing liquid ethanol
 svg += '<circle cx="'+(iX-15)+'" cy="'+(iY+145)+'" r="18" fill="#38bdf8" fill-opacity="0.25" stroke="#cbd5e1" stroke-width="1.5"/>';
 // Liquid fill in bulb
 svg += '<path d="M '+(iX-31)+' '+(iY+148)+' A 18 18 0 0 0 '+(iX+1)+' '+(iY+148)+' Z" fill="#38bdf8" fill-opacity="0.6"/>';
 svg += '<text x="'+(iX-15)+'" y="'+(iY+148)+'" text-anchor="middle" fill="#ffffff" font-size="6.5">Ethanol</text>';

 // Neck connecting bulb to U-tube
 svg += '<path d="M '+(iX-15)+' '+(iY+127)+' L '+(iX-15)+' '+(iY+100)+' Q '+(iX-15)+' '+(iY+90)+' '+(iX-5)+' '+(iY+90)+' L '+(iX+10)+' '+(iY+90)+'" fill="none" stroke="#cbd5e1" stroke-width="3"/>';

 // Differential U-Tube Manometer (nulled)
 const uLeft = iX + 15, uRight = iX + 30, uBot = iY + 155, uLvl = iY + 130;
 svg += '<path d="M '+uLeft+' '+(iY+90)+' L '+uLeft+' '+uBot+' Q '+((uLeft+uRight)/2)+' '+(uBot+8)+' '+uRight+' '+uBot+' L '+uRight+' '+(iY+70)+'" fill="none" stroke="#cbd5e1" stroke-width="3.5"/>';
 // Liquid fill in U-tube (nulled: exact same height in both arms)
 svg += '<path d="M '+uLeft+' '+uLvl+' L '+uLeft+' '+uBot+' Q '+((uLeft+uRight)/2)+' '+(uBot+8)+' '+uRight+' '+uBot+' L '+uRight+' '+uLvl+'" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';
 // Level indicator line across U-tube
 svg += '<line x1="'+(uLeft-5)+'" y1="'+uLvl+'" x2="'+(uRight+5)+'" y2="'+uLvl+'" stroke="#4ade80" stroke-width="1" stroke-dasharray="2,2"/>';
 svg += '<text x="'+(uRight+8)+'" y="'+(uLvl+3)+'" fill="#4ade80" font-size="6.5" font-weight="bold">Nulled (h₁ = h₂)</text>';

 // Connecting line to vacuum ballast manifold
 svg += '<path d="M '+uRight+' '+(iY+70)+' L '+uRight+' '+(iY+15)+' Q '+uRight+' '+(iY+5)+' '+(uRight+15)+' '+(iY+5)+' L '+(iX+85)+' '+(iY+5)+'" fill="none" stroke="#94a3b8" stroke-width="2"/>';
 svg += '<text x="'+(iX+88)+'" y="'+(iY+8)+'" fill="#38bdf8" font-size="6.5">To Vacuum Ballast</text>';

 // Thermistor probe in bath adjacent to bulb
 svg += '<rect x="'+(iX+42)+'" y="'+(iY+25)+'" width="3" height="120" rx="1" fill="#f59e0b"/>';
 svg += '<circle cx="'+(iX+43.5)+'" cy="'+(iY+145)+'" r="2.8" fill="#ef4444"/>';


 // --- RIGHT PANEL: DIGITAL TRANSDUCER & THERMODYNAMIC AUDIT ---
 const rX = 260, rY = 55, rW = 435, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';

 // Digital Pressure Transducer Readout
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+12)+'" width="200" height="72" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+26)+'" fill="#86efac" font-size="8" font-weight="bold">DIGITAL PRESSURE TRANSDUCER</text>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+56)+'" fill="#facc15" font-size="22" font-family="monospace" font-weight="bold">'+P.toFixed(2)+' kPa</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+44)+'" fill="#94a3b8" font-size="7.5">'+P_mmHg.toFixed(1)+' mmHg</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+56)+'" fill="#38bdf8" font-size="7.5" font-weight="bold">ln P = '+ln_P.toFixed(3)+'</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+68)+'" fill="#86efac" font-size="7">±0.01 kPa Res.</text>';

 // Mini Clausius-Clapeyron Linear Regression Profile
 const cX = rX + 225, cY = rY + 12, cW = 195, cH = 72;
 svg += '<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(cX+8)+'" y="'+(cY+12)+'" fill="#94a3b8" font-size="7">ln(P) vs 1000/T Coexistence Line</text>';
 // Axes inside mini box
 svg += '<line x1="'+(cX+15)+'" y1="'+(cY+60)+'" x2="'+(cX+185)+'" y2="'+(cY+60)+'" stroke="#162e1e" stroke-width="1"/>';
 svg += '<line x1="'+(cX+15)+'" y1="'+(cY+18)+'" x2="'+(cX+15)+'" y2="'+(cY+60)+'" stroke="#162e1e" stroke-width="1"/>';
 // Linear regression line sloping downwards (higher 1000/T = lower T => lower ln P)
 svg += '<line x1="'+(cX+25)+'" y1="'+(cY+22)+'" x2="'+(cX+175)+'" y2="'+(cY+56)+'" stroke="#4ade80" stroke-width="1.8"/>';
 // Current data point
 const ptX = cX + 25 + (3.3 - inv_T) / (3.3 - 2.8) * 150;
 const ptY = cY + 56 - (ln_P - 2.5) / (4.65 - 2.5) * 34;
 svg += '<circle cx="'+ptX+'" cy="'+ptY+'" r="3.5" fill="#facc15" stroke="#ef4444" stroke-width="1"/>';
 svg += '<text x="'+(cX+185)+'" y="'+(cY+24)+'" text-anchor="end" fill="#facc15" font-size="6.8" font-weight="bold">Slope = −4.639 K</text>';

 // Thermochemical State Matrix Grid
 const gY = rY + 92;
 const metrics = [
  {label: 'Water Bath Temperature t', val: t.toFixed(1) + ' °C (' + T_K.toFixed(2) + ' K)', col: '#86efac', sub: '1000/T = ' + inv_T.toFixed(4) + ' K⁻¹'},
  {label: 'Equilibrium Vapor Pressure P', val: P.toFixed(2) + ' kPa (' + P_mmHg.toFixed(1) + ' mmHg)', col: '#38bdf8', sub: 'Isoteniscope differential manometer nulled'},
  {label: 'Logarithmic Coordinate ln(P)', val: ln_P.toFixed(4), col: '#facc15', sub: 'Linear coordinate y = ln(P/kPa)'},
  {label: 'Enthalpy of Vaporization ΔH_vap°', val: '38.57 kJ/mol', col: '#f87171', sub: 'ΔH_vap = −m_slope · 8.3145 (Lit: 38.56)'}
 ];

 metrics.forEach((mi, idx)=>{
  const mx = rX + 15 + (idx % 2) * 205;
  const my = gY + Math.floor(idx / 2) * 52;
  svg += '<rect x="'+mx+'" y="'+my+'" width="195" height="46" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+13)+'" fill="#94a3b8" font-size="7">'+mi.label+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+28)+'" fill="'+mi.col+'" font-size="9" font-weight="bold">'+mi.val+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+39)+'" fill="#64748b" font-size="6.5">'+mi.sub+'</text>';
 });

 // Bottom Verification Banner
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+200)+'" width="405" height="30" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
 svg += '<text x="'+(rX+217)+'" y="'+(rY+218)+'" text-anchor="middle" fill="#4ade80" font-size="8.2" font-family="monospace" font-weight="bold">Clausius-Clapeyron Invariant: ln P = −4.639·(1000/T) + 17.814 => ΔH_vap° = 38.57 kJ/mol (R² = 1.000)</text>';

 svg += text(360, 310, 'Static isoteniscope nulls differential pressure, isolating true vapor pressure free from non-condensable air.', '#789c80', 8.5);
 return svg;
}

function drawVapCompareView(p, rawVal){
 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'VAPOR PRESSURE THERMODYNAMIC MODELS & DEPARTURES', '#4ade80', 13);
 svg += text(360, 39, 'Clausius-Clapeyron Linear Model vs Antoine 3-Parameter vs Trouton Entropy Rule', '#94a3b8', 9);

 const cards = [
  {
   title: '1. Clausius-Clapeyron',
   sub: 'ln P = −(ΔH/R)·(1/T) + C',
   color: '#4ade80',
   border: '#166534',
   items: [
    'Thermodynamic Derivation: Integrated exact Clapeyron equation',
    'Approximations: V_liq << V_gas; vapor obeys ideal gas law (PV = nRT)',
    'Enthalpy Assumption: ΔH_vap constant over narrow temperature range',
    'Linearity: Ideal R² = 1.000 across 30 °C to 78 °C',
    'Ethanol Result: ΔH_vap° = 38.56 kJ/mol; Normal T_b = 78.37 °C',
    'Physical Value: Direct measurement of molecular cohesion energy'
   ]
  },
  {
   title: '2. Antoine Equation',
   sub: 'log₁₀ P = A − [ B / (T + C) ]',
   color: '#38bdf8',
   border: '#0369a1',
   items: [
    'Empirical Extension: Adds 3rd parameter C for non-ideality',
    'Temperature Range: Accurate over hundreds of degrees to near T_crit',
    'Compressibility Correction: Accommodates vapor non-ideality (Z < 1)',
    'Enthalpy Variation: Accounts for temperature dependence dΔH_vap/dT',
    'Ethanol Parameters: A = 8.204, B = 1642.9, C = 230.3 (°C / mmHg)',
    'Primary Use: Industrial chemical engineering and distillation design'
   ]
  },
  {
   title: '3. Trouton's Rule',
   sub: 'ΔS_vap° = ΔH_vap / T_b ≈ 88 J/(mol·K)',
   color: '#facc15',
   border: '#854d0e',
   items: [
    'Non-Polar Standard: ΔS_vap ≈ 85–88 J/(mol·K) for inert liquids (CCl4, C6H6)',
    'Physical Basis: Vaporization produces similar translational entropy gain',
    'Ethanol Anomaly: ΔS_vap = 38560 / 351.52 = 109.7 J/(mol·K)',
    'Molecular Cause: Strong intermolecular hydrogen bonding in liquid',
    'Structured Liquid: Liquid has low entropy; vaporization destroys H-bonds',
    'Diagnostic Power: Proves presence of liquid-state associated networks'
   ]
  }
 ];

 cards.forEach((c, idx)=>{
  const x = 20 + idx * 230, y = 50, w = 220, h = 240;
  svg += '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg += '<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="34" rx="4" fill="#051009"/>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9" font-weight="bold">'+c.title+'</text>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+35)+'" text-anchor="middle" fill="#94a3b8" font-size="7">'+c.sub+'</text>';

  c.items.forEach((item, ii)=>{
   const iy = y + 54 + ii * 29;
   svg += '<circle cx="'+(x+14)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg += '<foreignObject x="'+(x+22)+'" y="'+(iy-10)+'" width="'+(w-28)+'" height="29"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.2px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg += text(360, 305, 'Thermodynamic Invariant: Clausius-Clapeyron linearity proves that ethanol vaporization is governed by constant enthalpy.', '#789c80', 8.5);
 return svg;
}

function drawVapSandboxView(p, rawVal){
 const t = (p && p.input) ? p.input : 50.0;
 const T_K = t + 273.15;
 const R = 8.31446;
 const dH = 38560.0;
 const Tb = 351.52;
 const Pb = 101.325;
 const ln_P_calc = Math.log(Pb) - (dH / R) * (1.0 / T_K - 1.0 / Tb);
 const P = rawVal !== null ? rawVal : Math.exp(ln_P_calc);

 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'LIQUID-VAPOR P-T COEXISTENCE PHASE DIAGRAM & ERROR AUDIT', '#4ade80', 13);
 svg += text(360, 39, 'Exponential Vapor Pressure Boundary and Vacuum Degassing Efficacy', '#94a3b8', 9);

 // --- LEFT PANEL: EXPONENTIAL P-T PHASE BOUNDARY ---
 const lX = 25, lY = 50, lW = 390, lH = 240;
 svg += '<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">LIQUID-VAPOR P-T COEXISTENCE BOUNDARY</text>';

 const gX = lX + 45, gY = lY + 35, gW = 325, gH = 155;
 svg += '<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#051009" stroke="#162e1e" stroke-width="1"/>';

 // Grid lines
 for(let gy = gY + 30; gy < gY + gH; gy += 30){
  svg += '<line x1="'+gX+'" y1="'+gy+'" x2="'+(gX+gW)+'" y2="'+gy+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
 }
 for(let gx = gX + 65; gx < gX + gW; gx += 65){
  svg += '<line x1="'+gx+'" y1="'+gY+'" x2="'+gx+'" y2="'+(gY+gH)+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
 }

 // Labels
 svg += '<text x="'+(gX+gW/2)+'" y="'+(gY+gH+14)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">Bath Temperature t (°C)</text>';
 svg += '<text x="'+(gX-8)+'" y="'+(gY+gH/2)+'" text-anchor="middle" transform="rotate(-90 '+(gX-8)+' '+(gY+gH/2)+')" fill="#94a3b8" font-size="7.5">Vapor Pressure P (kPa)</text>';

 // Ticks
 svg += '<text x="'+gX+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">20 °C</text>';
 svg += '<text x="'+(gX+80)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">40 °C</text>';
 svg += '<text x="'+(gX+160)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">60 °C</text>';
 svg += '<text x="'+(gX+240)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">80 °C</text>';
 svg += '<text x="'+(gX+gW)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">100 °C</text>';

 // Exponential vapor pressure curve
 svg += '<path d="M '+gX+' '+(gY+gH-10)+' Q '+(gX+140)+' '+(gY+gH-16)+' '+(gX+200)+' '+(gY+gH-45)+' T '+(gX+235)+' '+(gY+25)+'" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';

 // Normal boiling point point at T = 78.37 °C, P = 101.325 kPa
 const nbX = gX + 233.5, nbY = gY + 25;
 svg += '<circle cx="'+nbX+'" cy="'+nbY+'" r="3.5" fill="#ef4444"/>';
 svg += '<text x="'+(nbX-8)+'" y="'+(nbY-6)+'" text-anchor="end" fill="#f87171" font-size="7" font-weight="bold">Normal T_b = 78.37 °C (101.3 kPa)</text>';

 // Liquid region vs vapor region text
 svg += '<text x="'+(gX+50)+'" y="'+(gY+40)+'" fill="#38bdf8" font-size="8" font-weight="bold" opacity="0.6">LIQUID PHASE (μ_liq < μ_vap)</text>';
 svg += '<text x="'+(gX+180)+'" y="'+(gY+130)+'" fill="#facc15" font-size="8" font-weight="bold" opacity="0.6">VAPOR PHASE (μ_vap < μ_liq)</text>';

 // Current experimental point
 const curX = gX + (t - 20) / 80 * 240;
 const curY = gY + gH - (P / 105.0) * (gH - 25);
 svg += '<circle cx="'+curX+'" cy="'+curY+'" r="4" fill="#facc15" stroke="#4ade80" stroke-width="1.5"/>';
 svg += '<text x="'+(curX+8)+'" y="'+(curY+3)+'" fill="#facc15" font-size="7" font-weight="bold">'+P.toFixed(1)+' kPa</text>';

 // Bottom invariant badge
 svg += '<rect x="'+(lX+15)+'" y="'+(lY+198)+'" width="'+(lW-30)+'" height="32" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+218)+'" text-anchor="middle" fill="#86efac" font-size="8" font-family="monospace" font-weight="bold">Phase Equilibrium: μ_liquid(T,P) = μ_vapor(T,P) along Coexistence Curve</text>';


 // --- RIGHT PANEL: SOURCES OF BIAS & SYSTEM AUDIT ---
 const rX = 425, rY = 50, rW = 275, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">SOURCES OF BIAS & SYSTEM AUDIT</text>';

 const lossItems = [
  {label: 'Air Headspace Degassing', desc: 'Vacuum boiling purges Dalton non-condensable air', val: 'P_air < 0.02 kPa', col: '#4ade80'},
  {label: 'Manometer Nulling Accuracy', desc: 'Twin U-tube menisci nulled to ±0.2 mm using cathetometer', val: 'δP < 0.002 kPa', col: '#38bdf8'},
  {label: 'Zero External Contamination', desc: 'Ethanol serves as own manometric fluid; no mercury film', val: 'Zero foreign vapor', col: '#86efac'},
  {label: 'Capillary Depression Null', desc: 'Identical bore arms cancel surface tension forces', val: 'Zero capillary error', col: '#facc15'},
  {label: 'Multi-Point OLS Regression', desc: 'Linearization ln(P) vs 1000/T averages non-idealities', val: 'R² = 1.00000 Unbiased', col: '#4ade80'}
 ];

 lossItems.forEach((li, idx)=>{
  const ly = rY + 30 + idx * 40;
  svg += '<rect x="'+(rX+8)+'" y="'+ly+'" width="'+(rW-16)+'" height="34" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+12)+'" fill="'+li.col+'" font-size="7.5" font-weight="bold">'+li.label+'</text>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+25)+'" fill="#94a3b8" font-size="6.8">'+li.desc+'</text>';
  svg += '<text x="'+(rX+rW-14)+'" y="'+(ly+12)+'" text-anchor="end" fill="'+li.col+'" font-size="7.5" font-family="monospace">'+li.val+'</text>';
 });

 svg += text(360, 305, 'Thermodynamic Invariant: Isoteniscope eliminates air contamination, isolating pure vapor pressure.', '#789c80', 8.5);
 return svg;
}


// --- LAB 16: VAN 'T HOFF THERMODYNAMIC SOLUBILITY ANALYSIS ---

function drawHoffBenchView(p, rawVal){
 const t = (p && p.input) ? p.input : 40.0;
 const T_K = t + 273.15;
 const inv_T = 1000.0 / T_K;
 const R = 8.31446;
 const dH = 110000.0;
 const dS = 330.0;
 const ln_Ksp_calc = -dH / (R * T_K) + dS / R;
 const Ksp_calc = Math.exp(ln_Ksp_calc);
 const s_calc = Math.pow(Ksp_calc / 4.0, 1.0 / 3.0);
 const v_calc = 20.0 * s_calc;
 const V_HCl = rawVal !== null ? rawVal : v_calc;
 const s = V_HCl / 20.0;
 const Ksp = 4.0 * Math.pow(s, 3);
 const ln_Ksp = Math.log(Ksp);
 const dG = (dH - T_K * dS) / 1000.0;

 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'SATURATED BORAX THERMOSTAT & QUANTITATIVE BURETTE TITRATION', '#4ade80', 13);
 svg += text(360, 39, 'Na2B4O7·10H2O(s) <=> 2 Na+(aq) + B4O5(OH)4^2-(aq) + 8 H2O(l) | van 't Hoff ΔH° = +110.1 kJ/mol', '#94a3b8', 9);

 // --- LEFT PANEL: THERMOSTATTED BORAX FLASK & BURETTE TITRATION ---
 const bX = 140, bY = 70;

 // Water Bath Tank for Borax Slurry
 svg += '<rect x="'+(bX-75)+'" y="'+(bY+40)+'" width="90" height="150" rx="6" fill="#0284c7" fill-opacity="0.15" stroke="#38bdf8" stroke-width="1.5"/>';
 svg += '<text x="'+(bX-30)+'" y="'+(bY+180)+'" text-anchor="middle" fill="#64748b" font-size="7">Bath ('+t.toFixed(1)+' °C)</text>';

 // Borax Erlenmeyer Flask inside bath
 svg += '<path d="M '+(bX-40)+' '+(bY+60)+' L '+(bX-40)+' '+(bY+75)+' L '+(bX-58)+' '+(bY+150)+' Q '+(bX-58)+' '+(bY+156)+' '+(bX-50)+' '+(bY+156)+' L '+(bX-10)+' '+(bY+156)+' Q '+(bX-2)+' '+(bY+156)+' '+(bX-2)+' '+(bY+150)+' L '+(bX-20)+' '+(bY+75)+' L '+(bX-20)+' '+(bY+60)+' Z" fill="#0d1f14" stroke="#cbd5e1" stroke-width="1.5"/>';
 // Liquid fill
 svg += '<path d="M '+(bX-48)+' '+(bY+115)+' L '+(bX-56)+' '+(bY+148)+' L '+(bX-4)+' '+(bY+148)+' L '+(bX-12)+' '+(bY+115)+' Z" fill="#38bdf8" fill-opacity="0.4"/>';
 // Undissolved borax crystals settled at bottom
 svg += '<rect x="'+(bX-52)+'" y="'+(bY+148)+'" width="44" height="6" rx="1.5" fill="#f8fafc" stroke="#94a3b8" stroke-width="0.8"/>';
 svg += '<text x="'+(bX-30)+'" y="'+(bY+142)+'" text-anchor="middle" fill="#bae6fd" font-size="6">Saturated Slurry</text>';

 // Cotton filter-plugged transfer pipette
 svg += '<path d="M '+(bX-30)+' '+(bY+20)+' L '+(bX-30)+' '+(bY+125)+' L '+(bX-31)+' '+(bY+135)+' L '+(bX-29)+' '+(bY+135)+' L '+(bX-30)+' '+(bY+125)+'" fill="none" stroke="#cbd5e1" stroke-width="2"/>';
 svg += '<ellipse cx="'+(bX-30)+'" cy="'+(bY+75)+'" rx="5" ry="12" fill="#cbd5e1" fill-opacity="0.5"/>';
 svg += '<circle cx="'+(bX-30)+'" cy="'+(bY+135)+'" r="2" fill="#facc15"/>';
 svg += '<text x="'+(bX-30)+'" y="'+(bY+16)+'" text-anchor="middle" fill="#facc15" font-size="6">Filter Plug Pipette</text>';

 // Titration Assembly on right side of left panel
 const tX = bX + 45;
 // Class-A Glass Burette filled with 0.50 M HCl
 svg += '<rect x="'+(tX-3)+'" y="'+(bY-5)+'" width="6" height="110" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>';
 const bFillH = Math.min(85, V_HCl * 7.5);
 svg += '<rect x="'+(tX-2)+'" y="'+(bY+10)+'" width="4" height="'+bFillH+'" fill="#38bdf8" fill-opacity="0.6"/>';
 svg += '<line x1="'+(tX-6)+'" y1="'+(bY+80)+'" x2="'+(tX+6)+'" y2="'+(bY+80)+'" stroke="#ef4444" stroke-width="1.5"/>'; // stopcock
 svg += '<text x="'+(tX+12)+'" y="'+(bY+20)+'" fill="#94a3b8" font-size="6.5">0.50 M HCl</text>';

 // Titration Flask (Erlenmeyer) below burette
 const fY = bY + 115;
 svg += '<path d="M '+(tX-10)+' '+fY+' L '+(tX-10)+' '+(fY+10)+' L '+(tX-24)+' '+(fY+60)+' Q '+(tX-24)+' '+(fY+64)+' '+(tX-18)+' '+(fY+64)+' L '+(tX+18)+' '+(fY+64)+' Q '+(tX+24)+' '+(fY+64)+' '+(tX+24)+' '+(fY+60)+' L '+(tX+10)+' '+(fY+10)+' L '+(tX+10)+' '+fY+' Z" fill="#0d1f14" stroke="#cbd5e1" stroke-width="1.5"/>';
 // Bromocresol green liquid fill (yellow at endpoint pH 4.0)
 svg += '<path d="M '+(tX-18)+' '+(fY+32)+' L '+(tX-22)+' '+(fY+58)+' L '+(tX+22)+' '+(fY+58)+' L '+(tX+18)+' '+(fY+32)+' Z" fill="#facc15" fill-opacity="0.8"/>';
 svg += '<text x="'+tX+'" y="'+(fY+50)+'" text-anchor="middle" fill="#051009" font-size="6.5" font-weight="bold">pH 4.0 Yellow</text>';
 svg += '<text x="'+tX+'" y="'+(fY+74)+'" text-anchor="middle" fill="#64748b" font-size="7">5.00 mL Aliquot</text>';


 // --- RIGHT PANEL: DIGITAL TITRANT DISPLAY & VAN 'T HOFF AUDIT ---
 const rX = 260, rY = 55, rW = 435, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';

 // Digital Titrant Volume Readout
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+12)+'" width="200" height="72" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+26)+'" fill="#86efac" font-size="8" font-weight="bold">BURETTE TITRANT VOLUME (0.50 M HCl)</text>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+56)+'" fill="#facc15" font-size="22" font-family="monospace" font-weight="bold">'+V_HCl.toFixed(2)+' mL</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+44)+'" fill="#94a3b8" font-size="7.5">s = '+s.toFixed(4)+' M</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+56)+'" fill="#38bdf8" font-size="7.5" font-weight="bold">ln K_sp = '+ln_Ksp.toFixed(3)+'</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+68)+'" fill="#86efac" font-size="7">±0.02 mL Res.</text>';

 // Mini van 't Hoff Linear Profile Profile
 const cX = rX + 225, cY = rY + 12, cW = 195, cH = 72;
 svg += '<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(cX+8)+'" y="'+(cY+12)+'" fill="#94a3b8" font-size="7">ln(K_sp) vs 1000/T van 't Hoff Plot</text>';
 // Axes inside mini box
 svg += '<line x1="'+(cX+15)+'" y1="'+(cY+60)+'" x2="'+(cX+185)+'" y2="'+(cY+60)+'" stroke="#162e1e" stroke-width="1"/>';
 svg += '<line x1="'+(cX+15)+'" y1="'+(cY+18)+'" x2="'+(cX+15)+'" y2="'+(cY+60)+'" stroke="#162e1e" stroke-width="1"/>';
 // Sloping downwards (steeper slope: m = -13.24 K)
 svg += '<line x1="'+(cX+25)+'" y1="'+(cY+20)+'" x2="'+(cX+175)+'" y2="'+(cY+58)+'" stroke="#4ade80" stroke-width="1.8"/>';
 // Current data point
 const ptX = cX + 25 + (3.3 - inv_T) / (3.3 - 3.0) * 150;
 const ptY = cY + 58 - (ln_Ksp - (-4.0)) / ((-0.5) - (-4.0)) * 38;
 svg += '<circle cx="'+ptX+'" cy="'+ptY+'" r="3.5" fill="#facc15" stroke="#ef4444" stroke-width="1"/>';
 svg += '<text x="'+(cX+185)+'" y="'+(cY+24)+'" text-anchor="end" fill="#facc15" font-size="6.8" font-weight="bold">Slope = −13.24 K</text>';

 // State Function Matrix Grid
 const gY = rY + 92;
 const metrics = [
  {label: 'Equilibration Temperature t', val: t.toFixed(1) + ' °C (' + T_K.toFixed(2) + ' K)', col: '#86efac', sub: '1000/T = ' + inv_T.toFixed(4) + ' K⁻¹'},
  {label: 'Solubility Product K_sp', val: Ksp.toExponential(3) + ' (s = ' + s.toFixed(4) + ' M)', col: '#38bdf8', sub: 'K_sp = 4·s³ = 4·[Na+]²·[B4O5(OH)4^2-]'},
  {label: 'Standard Enthalpy ΔH°', val: '+110.1 kJ/mol', col: '#facc15', sub: 'ΔH° = −m_slope · (1000·R) (Target: +110.0)'},
  {label: 'Standard Entropy ΔS°', val: '+330.3 J/(mol·K)', col: '#f87171', sub: 'ΔS° = b · R (1 solid -> 11 aqueous species)'}
 ];

 metrics.forEach((mi, idx)=>{
  const mx = rX + 15 + (idx % 2) * 205;
  const my = gY + Math.floor(idx / 2) * 52;
  svg += '<rect x="'+mx+'" y="'+my+'" width="195" height="46" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+13)+'" fill="#94a3b8" font-size="7">'+mi.label+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+28)+'" fill="'+mi.col+'" font-size="9" font-weight="bold">'+mi.val+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+39)+'" fill="#64748b" font-size="6.5">'+mi.sub+'</text>';
 });

 // Bottom Verification Banner
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+200)+'" width="405" height="30" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
 svg += '<text x="'+(rX+217)+'" y="'+(rY+218)+'" text-anchor="middle" fill="#4ade80" font-size="8.2" font-family="monospace" font-weight="bold">van 't Hoff Invariant: ln K_sp = −13.241·(1000/T) + 39.723 => ΔH° = +110.1 kJ/mol, ΔS° = +330.3 J/mol·K (R² = 1.000)</text>';

 svg += text(360, 310, 'van 't Hoff analysis extracts enthalpy and entropy purely from equilibrium solubility without calorimetry.', '#789c80', 8.5);
 return svg;
}

function drawHoffCompareView(p, rawVal){
 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'THERMODYNAMIC ANALYSIS OF ELECTROLYTE DISSOLUTION', '#4ade80', 13);
 svg += text(360, 39, 'van 't Hoff Linear Ideal Model vs Debye-Hückel Extended Law vs Entropic Compensation', '#94a3b8', 9);

 const cards = [
  {
   title: '1. van 't Hoff Linear Model',
   sub: 'ln K_sp = −(ΔH°/R)·(1/T) + ΔS°/R',
   color: '#4ade80',
   border: '#166534',
   items: [
    'Thermodynamic Derivation: Integrated Gibbs-Helmholtz equation',
    'Linear Coordinates: ln K_sp against scaled reciprocal 1000/T',
    'Slope Physical Meaning: m_slope = −ΔH° / (1000·R) isolates enthalpy',
    'Intercept Physical Meaning: b = ΔS° / R isolates dissolution entropy',
    'Borax Results: ΔH° = +110.1 kJ/mol, ΔS° = +330.3 J/(mol·K)',
    'Regression Quality: Ideal linearity with R² = 1.000 across 30–55 °C'
   ]
  },
  {
   title: '2. Debye-Hückel Extended Law',
   sub: 'K_sp,true = γ_±³ · 4 s³',
   color: '#38bdf8',
   border: '#0369a1',
   items: [
    'Ionic Activity: Real solutions replace concentration with activity a_i',
    'Ionic Strength: I = 1/2 ∑ c_i z_i² ranges from 0.17 M to 0.51 M',
    'Mean Activity Coefficient: γ_± decreases from 0.75 to 0.65 as T rises',
    'Davies Equation: log γ_± = −0.51 · |z+z-| · [√I / (1 + √I) − 0.3 I]',
    'Correction Effect: Slightly shifts ΔH° by ~1.5% towards higher value',
    'Regression Absorption: Temperature-induced activity shift is linear'
   ]
  },
  {
   title: '3. Entropic Compensation',
   sub: 'ΔG° = ΔH° − T ΔS° = 0 at T_cross',
   color: '#facc15',
   border: '#854d0e',
   items: [
    'Enthalpic Barrier: ΔH° = +110.1 kJ/mol strongly opposes dissolution',
    'Entropic Driving Force: ΔS° = +330.3 J/(mol·K) massively favors dissolution',
    'Microscopic Cause: 1 mol solid decahydrate releases 11 aqueous species',
    'Crossover Temperature: T_cross = ΔH° / ΔS° = 110.1 / 0.3303 = 333.3 K (60.2 °C)',
    'Room Temperature (25 °C): ΔG° = +11.6 kJ/mol (K_sp < 1, moderate solubility)',
    'Elevated Temperature (65 °C): ΔG° < 0 (K_sp > 1, dramatic surge in solubility)'
   ]
  }
 ];

 cards.forEach((c, idx)=>{
  const x = 20 + idx * 230, y = 50, w = 220, h = 240;
  svg += '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg += '<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="34" rx="4" fill="#051009"/>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9" font-weight="bold">'+c.title+'</text>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+35)+'" text-anchor="middle" fill="#94a3b8" font-size="7">'+c.sub+'</text>';

  c.items.forEach((item, ii)=>{
   const iy = y + 54 + ii * 29;
   svg += '<circle cx="'+(x+14)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg += '<foreignObject x="'+(x+22)+'" y="'+(iy-10)+'" width="'+(w-28)+'" height="29"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.2px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg += text(360, 305, 'Thermodynamic Invariant: Borax dissolution illustrates entropy-driven solubility (ΔS° = +330 J/mol·K).', '#789c80', 8.5);
 return svg;
}

function drawHoffSandboxView(p, rawVal){
 const t = (p && p.input) ? p.input : 40.0;
 const T_K = t + 273.15;
 const dH = 110.09; // kJ/mol
 const dS = 0.33027; // kJ/(mol*K)
 const dG_cur = dH - T_K * dS;

 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'GIBBS FREE ENERGY SURFACE & TITRIMETRIC AUDIT', '#4ade80', 13);
 svg += text(360, 39, 'ΔG°(T) = ΔH° − T ΔS° Crossover and Pipetting Error Elimination', '#94a3b8', 9);

 // --- LEFT PANEL: GIBBS FREE ENERGY VS TEMPERATURE ---
 const lX = 25, lY = 50, lW = 390, lH = 240;
 svg += '<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">STANDARD GIBBS FREE ENERGY ΔG°(T) (kJ/mol)</text>';

 const gX = lX + 45, gY = lY + 35, gW = 325, gH = 155;
 svg += '<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#051009" stroke="#162e1e" stroke-width="1"/>';

 // Grid lines
 for(let gy = gY + 30; gy < gY + gH; gy += 30){
  svg += '<line x1="'+gX+'" y1="'+gy+'" x2="'+(gX+gW)+'" y2="'+gy+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
 }
 for(let gx = gX + 65; gx < gX + gW; gx += 65){
  svg += '<line x1="'+gx+'" y1="'+gY+'" x2="'+gx+'" y2="'+(gY+gH)+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
 }

 // Zero Gibbs Free Energy horizontal line (ΔG° = 0)
 const zeroY = gY + gH - 50;
 svg += '<line x1="'+gX+'" y1="'+zeroY+'" x2="'+(gX+gW)+'" y2="'+zeroY+'" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="3,2"/>';
 svg += '<text x="'+(gX+gW-5)+'" y="'+(zeroY-4)+'" text-anchor="end" fill="#94a3b8" font-size="6.8">ΔG° = 0 (K_sp = 1)</text>';

 // Labels
 svg += '<text x="'+(gX+gW/2)+'" y="'+(gY+gH+14)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">Absolute Temperature T (K)</text>';
 svg += '<text x="'+(gX-8)+'" y="'+(gY+gH/2)+'" text-anchor="middle" transform="rotate(-90 '+(gX-8)+' '+(gY+gH/2)+')" fill="#94a3b8" font-size="7.5">ΔG° (kJ/mol)</text>';

 // Ticks: 290K to 350K
 svg += '<text x="'+gX+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">290 K</text>';
 svg += '<text x="'+(gX+65)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">305 K</text>';
 svg += '<text x="'+(gX+130)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">320 K</text>';
 svg += '<text x="'+(gX+195)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">335 K (T_cross)</text>';
 svg += '<text x="'+(gX+gW)+'" y="'+(gY+gH+10)+'" text-anchor="middle" fill="#64748b" font-size="6.5">350 K</text>';

 // Linear downward slope of ΔG° = ΔH° - T ΔS°
 const lineX1 = gX + 15, lineY1 = gY + 15;
 const lineX2 = gX + gW - 15, lineY2 = gY + gH - 15;
 svg += '<line x1="'+lineX1+'" y1="'+lineY1+'" x2="'+lineX2+'" y2="'+lineY2+'" stroke="#ef4444" stroke-width="2.5"/>';

 // Spontaneous crossover point at 333.3 K (60.2 °C)
 const crossX = gX + (333.3 - 290.0) / 60.0 * gW;
 svg += '<circle cx="'+crossX+'" cy="'+zeroY+'" r="3.5" fill="#facc15"/>';
 svg += '<text x="'+(crossX+8)+'" y="'+(zeroY-5)+'" fill="#facc15" font-size="7" font-weight="bold">T_cross = 333.3 K (60.2 °C)</text>';

 // Current experimental point
 const curX = gX + (T_K - 290.0) / 60.0 * gW;
 const curY = zeroY - (dG_cur / 20.0) * (zeroY - gY);
 svg += '<circle cx="'+curX+'" cy="'+curY+'" r="4" fill="#4ade80" stroke="#facc15" stroke-width="1.5"/>';
 svg += '<text x="'+(curX+8)+'" y="'+(curY+4)+'" fill="#4ade80" font-size="7" font-weight="bold">ΔG° = +'+dG_cur.toFixed(1)+' kJ/mol</text>';

 // Bottom invariant badge
 svg += '<rect x="'+(lX+15)+'" y="'+(lY+198)+'" width="'+(lW-30)+'" height="32" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+218)+'" text-anchor="middle" fill="#86efac" font-size="8" font-family="monospace" font-weight="bold">Thermodynamic Crossover: Above 60.2 °C, T·ΔS° > ΔH° => ΔG° < 0 (Spontaneous)</text>';


 // --- RIGHT PANEL: SOURCES OF BIAS & SYSTEM AUDIT ---
 const rX = 425, rY = 50, rW = 275, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">SOURCES OF BIAS & SYSTEM AUDIT</text>';

 const lossItems = [
  {label: 'Cotton Filter Plug', desc: 'Blocks suspended solid borax crystals from entering pipette', val: 'Zero particulate bias', col: '#4ade80'},
  {label: 'Pre-Warmed Pipette Barrel', desc: 'Prevents thermal shock premature precipitation on glass', val: 'Thermal shock eliminated', col: '#38bdf8'},
  {label: 'Bromocresol Green Endpoint', desc: 'Sharp color change at pH 4.0 matches boric acid stoichiometry', val: 'Exact 1:2 neutralization', col: '#86efac'},
  {label: 'Excess Solid Verification', desc: 'Continuous excess solid ensures 100% thermodynamic saturation', val: 'Solid-liquid equilibrium', col: '#facc15'},
  {label: 'Multi-Point OLS Regression', desc: 'Linearization ln(K_sp) vs 1000/T purges systematic titration drift', val: 'R² = 1.00000 Unbiased', col: '#4ade80'}
 ];

 lossItems.forEach((li, idx)=>{
  const ly = rY + 30 + idx * 40;
  svg += '<rect x="'+(rX+8)+'" y="'+ly+'" width="'+(rW-16)+'" height="34" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+12)+'" fill="'+li.col+'" font-size="7.5" font-weight="bold">'+li.label+'</text>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+25)+'" fill="#94a3b8" font-size="6.8">'+li.desc+'</text>';
  svg += '<text x="'+(rX+rW-14)+'" y="'+(ly+12)+'" text-anchor="end" fill="'+li.col+'" font-size="7.5" font-family="monospace">'+li.val+'</text>';
 });

 svg += text(360, 305, 'Thermodynamic Invariant: van 't Hoff analysis provides complete state function derivation.', '#789c80', 8.5);
 return svg;
}


// --- LAB 17: HEAT CAPACITY RATIO OF GASES (CLÉMENT-DESORMES METHOD) ---

function drawClementBenchView(p, rawVal){
 const h1 = (p && p.input) ? p.input : 25.0;
 const gamma_true = 1.400;
 const slope_true = 0.285714;
 const h2 = rawVal !== null ? rawVal : (h1 * slope_true);
 const gamma_calc = h1 / (h1 - h2);

 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'CLÉMENT-DESORMES GAS EXPANSION APPARATUS (ADIABATIC INDEX)', '#4ade80', 13);
 svg += text(360, 39, 'Dry Atmospheric Air (N2 + O2) | Adiabatic Index γ = Cp/Cv = 7/5 = 1.400 (5 Active Degrees of Freedom)', '#94a3b8', 9);

 // --- LEFT PANEL: 15-LITER GLASS CARBOY & DBP MANOMETER ---
 const cX = 140, cY = 70;

 // Protective mesh wire cage around carboy
 svg += '<rect x="'+(cX-70)+'" y="'+(cY+35)+'" width="95" height="155" rx="10" fill="none" stroke="#334155" stroke-width="1.5" stroke-dasharray="4,4"/>';

 // 15-Liter Glass Carboy Body
 svg += '<path d="M '+(cX-30)+' '+(cY+45)+' L '+(cX-15)+' '+(cY+45)+' L '+(cX-15)+' '+(cY+55)+' Q '+(cX-55)+' '+(cY+75)+' '+(cX-55)+' '+(cY+120)+' L '+(cX-55)+' '+(cY+165)+' Q '+(cX-55)+' '+(cY+180)+' '+(cX-40)+' '+(cY+180)+' L '+(cX-5)+' '+(cY+180)+' Q '+(cX+10)+' '+(cY+180)+' '+(cX+10)+' '+(cY+165)+' L '+(cX+10)+' '+(cY+120)+' Q '+(cX+10)+' '+(cY+75)+' '+(cX-30)+' '+(cY+55)+' Z" fill="#0284c7" fill-opacity="0.12" stroke="#cbd5e1" stroke-width="1.8"/>';
 svg += '<text x="'+(cX-22)+'" y="'+(cY+130)+'" text-anchor="middle" fill="#bae6fd" font-size="8" font-weight="bold">15 L Carboy</text>';
 svg += '<text x="'+(cX-22)+'" y="'+(cY+142)+'" text-anchor="middle" fill="#38bdf8" font-size="6.5">Dry Air (f = 5)</text>';

 // Quick-release ground-glass valve at top of carboy
 svg += '<rect x="'+(cX-26)+'" y="'+(cY+20)+'" width="12" height="25" fill="#94a3b8" stroke="#cbd5e1" stroke-width="1"/>';
 // Valve lever / Solenoid
 svg += '<rect x="'+(cX-34)+'" y="'+(cY+15)+'" width="28" height="8" rx="2" fill="#ef4444"/>';
 svg += '<text x="'+(cX-20)+'" y="'+(cY+11)+'" text-anchor="middle" fill="#f87171" font-size="6">0.80s Valve</text>';

 // Side connecting tube from carboy to manometer and bellows
 svg += '<path d="M '+(cX-15)+' '+(cY+50)+' L '+(cX+35)+' '+(cY+50)+'" fill="none" stroke="#cbd5e1" stroke-width="2.5"/>';

 // Hand bellows pump and drying tube on far left
 svg += '<ellipse cx="'+(cX-78)+'" cy="'+(cY+95)+'" rx="10" ry="16" fill="#475569" stroke="#334155"/>';
 svg += '<rect x="'+(cX-72)+'" y="'+(cY+70)+'" width="16" height="6" rx="1.5" fill="#facc15" stroke="#ca8a04"/>';
 svg += '<text x="'+(cX-64)+'" y="'+(cY+64)+'" text-anchor="middle" fill="#facc15" font-size="5.5">CaCl₂ Tube</text>';
 svg += '<path d="M '+(cX-64)+' '+(cY+76)+' L '+(cX-64)+' '+(cY+50)+' L '+(cX-30)+' '+(cY+50)+'" fill="none" stroke="#94a3b8" stroke-width="1.5"/>';

 // Open-ended U-Tube Manometer with Dibutyl Phthalate (colored fluid)
 const mX = cX + 45, mY = cY + 50;
 const uW = 16, uH = 135;
 svg += '<path d="M '+mX+' '+mY+' L '+mX+' '+(mY+uH)+' Q '+(mX+uW/2)+' '+(mY+uH+8)+' '+(mX+uW)+' '+(mY+uH)+' L '+(mX+uW)+' '+(mY-15)+'" fill="none" stroke="#cbd5e1" stroke-width="3"/>';

 // Manometer fluid levels (Left arm pushed down, right arm pushed up by h)
 const dispH = Math.min(45, (h2 / 40.0) * 45);
 const leftLvl = mY + uH/2 + dispH;
 const rightLvl = mY + uH/2 - dispH;
 svg += '<path d="M '+mX+' '+leftLvl+' L '+mX+' '+(mY+uH)+' Q '+(mX+uW/2)+' '+(mY+uH+8)+' '+(mX+uW)+' '+(mY+uH)+' L '+(mX+uW)+' '+rightLvl+'" fill="none" stroke="#ef4444" stroke-width="2"/>';

 // Height difference indicator bracket
 svg += '<line x1="'+(mX+uW+4)+'" y1="'+leftLvl+'" x2="'+(mX+uW+12)+'" y2="'+leftLvl+'" stroke="#facc15" stroke-width="1"/>';
 svg += '<line x1="'+(mX+uW+4)+'" y1="'+rightLvl+'" x2="'+(mX+uW+12)+'" y2="'+rightLvl+'" stroke="#facc15" stroke-width="1"/>';
 svg += '<line x1="'+(mX+uW+8)+'" y1="'+leftLvl+'" x2="'+(mX+uW+8)+'" y2="'+rightLvl+'" stroke="#facc15" stroke-width="1"/>';
 svg += '<text x="'+(mX+uW+14)+'" y="'+((leftLvl+rightLvl)/2+3)+'" fill="#facc15" font-size="7" font-weight="bold">h₂ = '+h2.toFixed(1)+' cm</text>';


 // --- RIGHT PANEL: DIGITAL MANOMETER DISPLAY & ADIABATIC AUDIT ---
 const rX = 260, rY = 55, rW = 435, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';

 // Digital Reading Readout
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+12)+'" width="200" height="72" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+26)+'" fill="#86efac" font-size="8" font-weight="bold">RE-EQUILIBRATED PRESSURE h₂ (DBP)</text>';
 svg += '<text x="'+(rX+25)+'" y="'+(rY+56)+'" fill="#facc15" font-size="22" font-family="monospace" font-weight="bold">'+h2.toFixed(2)+' cm</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+44)+'" fill="#94a3b8" font-size="7.5">h₁ = '+h1.toFixed(1)+' cm</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+56)+'" fill="#4ade80" font-size="7.5" font-weight="bold">γ = '+gamma_calc.toFixed(3)+'</text>';
 svg += '<text x="'+(rX+140)+'" y="'+(rY+68)+'" fill="#38bdf8" font-size="7">±0.05 cm Res.</text>';

 // Mini h2 vs h1 Linear Regression Profile
 const cX = rX + 225, cY = rY + 12, cW = 195, cH = 72;
 svg += '<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1.2"/>';
 svg += '<text x="'+(cX+8)+'" y="'+(cY+12)+'" fill="#94a3b8" font-size="7">Linear Fit: h₂ = [(γ−1)/γ] · h₁</text>';
 // Axes inside mini box
 svg += '<line x1="'+(cX+15)+'" y1="'+(cY+60)+'" x2="'+(cX+185)+'" y2="'+(cY+60)+'" stroke="#162e1e" stroke-width="1"/>';
 svg += '<line x1="'+(cX+15)+'" y1="'+(cY+18)+'" x2="'+(cX+15)+'" y2="'+(cY+60)+'" stroke="#162e1e" stroke-width="1"/>';
 // Sloping line with m = 2/7 = 0.2857
 svg += '<line x1="'+(cX+15)+'" y1="'+(cY+60)+'" x2="'+(cX+180)+'" y2="'+(cY+20)+'" stroke="#4ade80" stroke-width="1.8"/>';
 // Current data point
 const ptX = cX + 15 + (h1 / 45.0) * 165;
 const ptY = cY + 60 - (h2 / 14.0) * 40;
 svg += '<circle cx="'+ptX+'" cy="'+ptY+'" r="3.5" fill="#facc15" stroke="#ef4444" stroke-width="1"/>';
 svg += '<text x="'+(cX+185)+'" y="'+(cY+22)+'" text-anchor="end" fill="#facc15" font-size="6.8" font-weight="bold">Slope = 0.2857</text>';

 // State Matrix Grid
 const gY = rY + 92;
 const metrics = [
  {label: 'Initial Excess Pressure h₁', val: h1.toFixed(1) + ' cm DBP (' + (h1*0.1027).toFixed(2) + ' kPa)', col: '#86efac', sub: 'P₁ = P₀ + h₁ (at room temperature T₀)'},
  {label: 'Re-Equilibrated Pressure h₂', val: h2.toFixed(2) + ' cm DBP (' + (h2*0.1027).toFixed(2) + ' kPa)', col: '#38bdf8', sub: 'P₃ = P₀ + h₂ (post isochoric re-warming)'},
  {label: 'Regression Slope m_slope', val: '0.2857 (2/7 exact)', col: '#facc15', sub: 'm_slope = (γ − 1) / γ'},
  {label: 'Derived Adiabatic Index γ', val: '1.400 (7/5 Diatomic)', col: '#f87171', sub: 'γ = 1 / (1 − m_slope) = Cp/Cv'}
 ];

 metrics.forEach((mi, idx)=>{
  const mx = rX + 15 + (idx % 2) * 205;
  const my = gY + Math.floor(idx / 2) * 52;
  svg += '<rect x="'+mx+'" y="'+my+'" width="195" height="46" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+13)+'" fill="#94a3b8" font-size="7">'+mi.label+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+28)+'" fill="'+mi.col+'" font-size="9" font-weight="bold">'+mi.val+'</text>';
  svg += '<text x="'+(mx+10)+'" y="'+(my+39)+'" fill="#64748b" font-size="6.5">'+mi.sub+'</text>';
 });

 // Bottom Verification Banner
 svg += '<rect x="'+(rX+15)+'" y="'+(rY+200)+'" width="405" height="30" rx="4" fill="#051009" stroke="#162e1e" stroke-width="1"/>';
 svg += '<text x="'+(rX+217)+'" y="'+(rY+218)+'" text-anchor="middle" fill="#4ade80" font-size="8.2" font-family="monospace" font-weight="bold">Clément-Desormes Invariant: γ = 1 / (1 − 0.285714) = 1.400 (R² = 1.000, 0.00% Error)</text>';

 svg += text(360, 310, 'Rapid adiabatic expansion followed by isochoric thermal recovery isolates the heat capacity ratio directly.', '#789c80', 8.5);
 return svg;
}

function drawClementCompareView(p, rawVal){
 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'GAS MOLECULAR ARCHITECTURE & ADIABATIC EXPANSION INDICES', '#4ade80', 13);
 svg += text(360, 39, 'Monatomic (γ = 1.667) vs Diatomic (γ = 1.400) vs Polyatomic (γ = 1.333) vs Dynamic Rüchhardt', '#94a3b8', 9);

 const cards = [
  {
   title: '1. Monatomic Gas',
   sub: 'Helium, Argon, Neon (f = 3)',
   color: '#38bdf8',
   border: '#0369a1',
   items: [
    'Degrees of Freedom: 3 translational (f = 3; no rotation/vibration)',
    'Constant-Volume Heat Capacity: C_v = (3/2) R = 12.47 J/(mol·K)',
    'Constant-Pressure Heat Capacity: C_p = (5/2) R = 20.79 J/(mol·K)',
    'Adiabatic Index: γ = 5/3 = 1.667',
    'Clément-Desormes Slope: m_slope = (γ−1)/γ = 2/5 = 0.4000',
    'Acoustic Velocity: Fastest speed of sound per unit molecular weight'
   ]
  },
  {
   title: '2. Diatomic Gas (★)',
   sub: 'Dry Air, N2, O2, CO (f = 5)',
   color: '#4ade80',
   border: '#166534',
   items: [
    'Degrees of Freedom: 3 trans + 2 rot (f = 5 at 298 K; vib frozen)',
    'Constant-Volume Heat Capacity: C_v = (5/2) R = 20.79 J/(mol·K)',
    'Constant-Pressure Heat Capacity: C_p = (7/2) R = 29.10 J/(mol·K)',
    'Adiabatic Index: γ = 7/5 = 1.400',
    'Clément-Desormes Slope: m_slope = (γ−1)/γ = 2/7 = 0.2857',
    'Laboratory Benchmark: Diatomic atmospheric air investigated here'
   ]
  },
  {
   title: '3. Polyatomic / Rüchhardt',
   sub: 'CO2, CH4 (f = 6) & Dynamic Piston',
   color: '#facc15',
   border: '#854d0e',
   items: [
    'Degrees of Freedom: 3 trans + 3 rot (f = 6), C_v = 3 R, C_p = 4 R',
    'Adiabatic Index: γ = 4/3 = 1.333 (CO2 reaches ~1.30 with bending)',
    'Rüchhardt Method: Precision steel ball oscillates harmonically in tube',
    'Oscillation Frequency: f = (1/2π) · √[ (γ · P · A²) / (m · V) ]',
    'Comparison: Dynamic Rüchhardt suffers from ball friction & tube leakage',
    'Clément-Desormes Superiority: Static equilibrium purges frictional errors'
   ]
  }
 ];

 cards.forEach((c, idx)=>{
  const x = 20 + idx * 230, y = 50, w = 220, h = 240;
  svg += '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="6" fill="#0d1f14" stroke="'+c.border+'" stroke-width="1.5"/>';
  svg += '<rect x="'+(x+8)+'" y="'+(y+8)+'" width="'+(w-16)+'" height="34" rx="4" fill="#051009"/>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="'+c.color+'" font-size="9" font-weight="bold">'+c.title+'</text>';
  svg += '<text x="'+(x+w/2)+'" y="'+(y+35)+'" text-anchor="middle" fill="#94a3b8" font-size="7">'+c.sub+'</text>';

  c.items.forEach((item, ii)=>{
   const iy = y + 54 + ii * 29;
   svg += '<circle cx="'+(x+14)+'" cy="'+(iy-3)+'" r="2" fill="'+c.color+'"/>';
   svg += '<foreignObject x="'+(x+22)+'" y="'+(iy-10)+'" width="'+(w-28)+'" height="29"><p xmlns="http://www.w3.org/1999/xhtml" style="font-size:7.2px;color:#cbd5e1;line-height:1.2;margin:0">'+item+'</p></foreignObject>';
  });
 });

 svg += text(360, 305, 'Thermodynamic Invariant: Classical equipartition dictates γ = (f + 2) / f directly from molecular geometry.', '#789c80', 8.5);
 return svg;
}

function drawClementSandboxView(p, rawVal){
 let svg = '';
 svg += '<rect x="0" y="0" width="720" height="320" fill="#051009"/>';
 svg += text(360, 24, 'THERMODYNAMIC P-V INDICATOR DIAGRAM & ERROR AUDIT', '#4ade80', 13);
 svg += text(360, 39, 'Adiabatic Isentrope (PV^γ = const) vs Isothermal (PV = const) vs Isochoric Warming (V = const)', '#94a3b8', 9);

 // --- LEFT PANEL: P-V INDICATOR DIAGRAM ---
 const lX = 25, lY = 50, lW = 390, lH = 240;
 svg += '<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">THERMODYNAMIC P-V CYCLE TRAJECTORY</text>';

 const gX = lX + 45, gY = lY + 35, gW = 325, gH = 155;
 svg += '<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#051009" stroke="#162e1e" stroke-width="1"/>';

 // Grid lines
 for(let gy = gY + 30; gy < gY + gH; gy += 30){
  svg += '<line x1="'+gX+'" y1="'+gy+'" x2="'+(gX+gW)+'" y2="'+gy+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
 }
 for(let gx = gX + 65; gx < gX + gW; gx += 65){
  svg += '<line x1="'+gx+'" y1="'+gY+'" x2="'+gx+'" y2="'+(gY+gH)+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
 }

 // Labels
 svg += '<text x="'+(gX+gW/2)+'" y="'+(gY+gH+14)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">Gas Specific Volume V</text>';
 svg += '<text x="'+(gX-8)+'" y="'+(gY+gH/2)+'" text-anchor="middle" transform="rotate(-90 '+(gX-8)+' '+(gY+gH/2)+')" fill="#94a3b8" font-size="7.5">Absolute Pressure P</text>';

 // State 1: (V1, P1) = (low V, high P)
 const s1 = {x: gX + 50, y: gY + 25};
 // State 2: (V2, P2 = P0) = (high V, atm P) via steep adiabatic expansion
 const s2 = {x: gX + 260, y: gY + gH - 25};
 // State 3: (V3 = V2, P3 = P0 + h2) via vertical isochoric warming
 const s3 = {x: gX + 260, y: gY + 65};

 // Adiabatic curve 1 -> 2 (steep red line)
 svg += '<path d="M '+s1.x+' '+s1.y+' Q '+(s1.x+90)+' '+(s1.y+65)+' '+s2.x+' '+s2.y+'" fill="none" stroke="#ef4444" stroke-width="2.5"/>';
 svg += '<text x="'+(s1.x+70)+'" y="'+(s1.y+40)+'" fill="#ef4444" font-size="7" font-weight="bold">Adiabatic PV^γ = const (0.8s)</text>';

 // Isochoric line 2 -> 3 (vertical green line at V2 = const)
 svg += '<line x1="'+s2.x+'" y1="'+s2.y+'" x2="'+s3.x+'" y2="'+s3.y+'" stroke="#4ade80" stroke-width="2.5"/>';
 svg += '<text x="'+(s3.x+8)+'" y="'+((s2.y+s3.y)/2)+'" fill="#4ade80" font-size="7" font-weight="bold">Isochoric Warming (V=const)</text>';

 // Isothermal curve 1 -> 3 (gentle dashed blue line T0 = const)
 svg += '<path d="M '+s1.x+' '+s1.y+' Q '+(s1.x+110)+' '+(s1.y+20)+' '+s3.x+' '+s3.y+'" fill="none" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="3,2"/>';
 svg += '<text x="'+((s1.x+s3.x)/2)+'" y="'+(s1.y+10)+'" text-anchor="middle" fill="#38bdf8" font-size="7">Isothermal PV = const (T₀)</text>';

 // Points
 svg += '<circle cx="'+s1.x+'" cy="'+s1.y+'" r="4" fill="#38bdf8"/>';
 svg += '<text x="'+(s1.x-8)+'" y="'+(s1.y-5)+'" fill="#38bdf8" font-size="7.5" font-weight="bold">State 1 (P₀+h₁, T₀)</text>';

 svg += '<circle cx="'+s2.x+'" cy="'+s2.y+'" r="4" fill="#ef4444"/>';
 svg += '<text x="'+(s2.x+8)+'" y="'+(s2.y+2)+'" fill="#ef4444" font-size="7.5" font-weight="bold">State 2 (P₀, T₂<T₀)</text>';

 svg += '<circle cx="'+s3.x+'" cy="'+s3.y+'" r="4" fill="#4ade80"/>';
 svg += '<text x="'+(s3.x-8)+'" y="'+(s3.y-5)+'" text-anchor="end" fill="#4ade80" font-size="7.5" font-weight="bold">State 3 (P₀+h₂, T₀)</text>';

 // Bottom invariant badge
 svg += '<rect x="'+(lX+15)+'" y="'+(lY+198)+'" width="'+(lW-30)+'" height="32" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+218)+'" text-anchor="middle" fill="#86efac" font-size="8" font-family="monospace" font-weight="bold">Thermodynamic Invariant: Adiabatic curve is steeper than Isotherm by exactly factor γ = 1.400</text>';


 // --- RIGHT PANEL: SOURCES OF BIAS & SYSTEM AUDIT ---
 const rX = 425, rY = 50, rW = 275, rH = 240;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="9.5" font-weight="bold">SOURCES OF BIAS & SYSTEM AUDIT</text>';

 const lossItems = [
  {label: 'Valve Actuation Window', desc: '0.80 s solenoid timing prevents boundary heat conduction', val: 'Timing error < 0.02 s', col: '#4ade80'},
  {label: '15 L Volume Core Shielding', desc: 'Large volume confines wall heat diffusion to thin outer skin', val: '>95% bulk isentropic', col: '#38bdf8'},
  {label: 'Low-Volatility DBP Fluid', desc: 'Zero vapor pressure prevents condensable solvent evaporation', val: 'P_vap < 10⁻⁵ mmHg', col: '#86efac'},
  {label: 'Desiccant Inline Purging', desc: 'Anhydrous CaCl2 removes triatomic H2O vapor (γ = 1.33)', val: '<0.05% Rel. Humidity', col: '#facc15'},
  {label: 'Multi-Point OLS Regression', desc: 'Slope eliminates zero-point parallax and barometric drift', val: 'R² = 1.00000 Unbiased', col: '#4ade80'}
 ];

 lossItems.forEach((li, idx)=>{
  const ly = rY + 30 + idx * 40;
  svg += '<rect x="'+(rX+8)+'" y="'+ly+'" width="'+(rW-16)+'" height="34" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+12)+'" fill="'+li.col+'" font-size="7.5" font-weight="bold">'+li.label+'</text>';
  svg += '<text x="'+(rX+14)+'" y="'+(ly+25)+'" fill="#94a3b8" font-size="6.8">'+li.desc+'</text>';
  svg += '<text x="'+(rX+rW-14)+'" y="'+(ly+12)+'" text-anchor="end" fill="'+li.col+'" font-size="7.5" font-family="monospace">'+li.val+'</text>';
 });

 svg += text(360, 305, 'Thermodynamic Invariant: Slope m = 0.2857 yields γ = 1.400 with zero baseline offset.', '#789c80', 8.5);
 return svg;
}


// ======================================================================
// LAB 18: PARTIAL MOLAR VOLUME OF BINARY MIXTURES
// ======================================================================

function drawPycBenchView(p, rawVal){
 const m = p.input;
 const m_tare = 18.4250;
 const V_pyc = 25.0000;
 const M2 = 46.069;
 const rho0 = 0.997047;
 const phi_calc = 54.20 + 0.25 * m;
 const rho_soln = (1000.0 + m * M2) / (1000.0 / rho0 + m * phi_calc);
 const m_liq = rho_soln * V_pyc;
 const m_filled = rawVal || (m_tare + m_liq);
 const V2_bar = phi_calc + 2.0 * 0.25 * m;

 let svg = header('Gay-Lussac Pycnometry & Constant-Temperature Bath (25.00 °C)');

 // Background Lab Bench
 svg += '<rect x="20" y="45" width="680" height="255" rx="6" fill="#06120b" stroke="#162e1e"/>';

 // --- LEFT: THERMOSTATIC CIRCULATING BATH (x: 40, y: 65, w: 220, h: 220) ---
 const bX = 40, bY = 65, bW = 210, bH = 210;
 svg += '<rect x="'+bX+'" y="'+bY+'" width="'+bW+'" height="'+bH+'" rx="8" fill="#0a1a12" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<rect x="'+(bX+8)+'" y="'+(bY+8)+'" width="'+(bW-16)+'" height="22" rx="4" fill="#0d2419" stroke="#163824"/>';
 svg += '<text x="'+(bX+bW/2)+'" y="'+(bY+22)+'" text-anchor="middle" fill="#86efac" font-size="9" font-weight="bold">THERMOSTATIC BATH (25.00 ± 0.01 °C)</text>';

 // Water Tank
 const tX = bX + 15, tY = bY + 38, tW = bW - 30, tH = 120;
 svg += '<rect x="'+tX+'" y="'+tY+'" width="'+tW+'" height="'+tH+'" rx="4" fill="#04121a" stroke="#0284c7" stroke-width="1.2"/>';
 // Water Fill
 svg += '<rect x="'+(tX+2)+'" y="'+(tY+15)+'" width="'+(tW-4)+'" height="'+(tH-17)+'" fill="#0369a1" fill-opacity="0.3"/>';
 // Waves
 svg += '<path d="M '+(tX+4)+' '+(tY+16)+' Q '+(tX+35)+' '+(tY+11)+', '+(tX+70)+' '+(tY+16)+' T '+(tX+140)+' '+(tY+16)+' T '+(tX+tW-4)+' '+(tY+16)+'" fill="none" stroke="#38bdf8" stroke-width="1"/>';

 // Digital Bath Controller
 svg += '<rect x="'+(bX+15)+'" y="'+(bY+165)+'" width="'+(bW-30)+'" height="36" rx="4" fill="#020804" stroke="#163824"/>';
 svg += '<rect x="'+(bX+25)+'" y="'+(bY+170)+'" width="80" height="25" rx="3" fill="#061208" stroke="#22c55e" stroke-width="0.8"/>';
 svg += '<text x="'+(bX+65)+'" y="'+(bY+187)+'" text-anchor="middle" fill="#4ade80" font-size="12" font-family="monospace" font-weight="bold">25.00°C</text>';
 svg += '<circle cx="'+(bX+125)+'" cy="'+(bY+178)+'" r="4" fill="#22c55e"/>';
 svg += '<text x="'+(bX+135)+'" y="'+(bY+181)+'" fill="#86efac" font-size="7">HEATING OK</text>';
 svg += '<circle cx="'+(bX+125)+'" cy="'+(bY+191)+'" r="4" fill="#38bdf8"/>';
 svg += '<text x="'+(bX+135)+'" y="'+(bY+194)+'" fill="#38bdf8" font-size="7">CIRCULATOR</text>';

 // Pycnometer inside Bath (Immersed)
 const pyX = tX + 70, pyY = tY + 40;
 // Flask body (pear-shaped)
 svg += '<path d="M '+(pyX-18)+' '+(pyY+50)+' C '+(pyX-28)+' '+(pyY+30)+', '+(pyX-14)+' '+(pyY+12)+', '+(pyX-6)+' '+(pyY)+' L '+(pyX+6)+' '+(pyY)+' C '+(pyX+14)+' '+(pyY+12)+', '+(pyX+28)+' '+(pyY+30)+', '+(pyX+18)+' '+(pyY+50)+' Z" fill="#0ea5e9" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1.2"/>';
 // Liquid inside pycnometer
 svg += '<path d="M '+(pyX-17)+' '+(pyY+49)+' C '+(pyX-26)+' '+(pyY+30)+', '+(pyX-13)+' '+(pyY+13)+', '+(pyX-5)+' '+(pyY+2)+' L '+(pyX+5)+' '+(pyY+2)+' C '+(pyX+13)+' '+(pyY+13)+', '+(pyX+26)+' '+(pyY+30)+', '+(pyX+17)+' '+(pyY+49)+' Z" fill="#22c55e" fill-opacity="0.35"/>';
 // Capillary Stopper neck
 svg += '<rect x="'+(pyX-5)+'" y="'+(pyY-20)+'" width="10" height="20" fill="#0284c7" fill-opacity="0.2" stroke="#38bdf8" stroke-width="1"/>';
 // Central capillary bore
 svg += '<line x1="'+pyX+'" y1="'+(pyY-25)+'" x2="'+pyX+'" y2="'+(pyY+35)+'" stroke="#4ade80" stroke-width="1.2"/>';
 // Meniscus at ground flat tip
 svg += '<ellipse cx="'+pyX+'" cy="'+(pyY-25)+'" rx="2.5" ry="1.2" fill="#4ade80"/>';
 svg += '<text x="'+pyX+'" y="'+(pyY+32)+'" text-anchor="middle" fill="#ffffff" font-size="6.5" font-weight="bold">25 mL</text>';
 svg += '<text x="'+pyX+'" y="'+(pyY+62)+'" text-anchor="middle" fill="#a7f3d0" font-size="6.8">m = '+m.toFixed(2)+' mol/kg</text>';


 // --- CENTER: METTLER TOLEDO ANALYTICAL BALANCE (x: 270, y: 65, w: 220, h: 220) ---
 const aX = 270, aY = 65, aW = 210, aH = 210;
 svg += '<rect x="'+aX+'" y="'+aY+'" width="'+aW+'" height="'+aH+'" rx="8" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<rect x="'+(aX+8)+'" y="'+(aY+8)+'" width="'+(aW-16)+'" height="22" rx="4" fill="#132e1f" stroke="#1e4d31"/>';
 svg += '<text x="'+(aX+aW/2)+'" y="'+(aY+22)+'" text-anchor="middle" fill="#86efac" font-size="9" font-weight="bold">METTLER TOLEDO XPE205 (±0.0001 g)</text>';

 // Glass Draft Chamber
 const dX = aX + 25, dY = aY + 38, dW = aW - 50, dH = 100;
 svg += '<rect x="'+dX+'" y="'+dY+'" width="'+dW+'" height="'+dH+'" rx="3" fill="#030d07" stroke="#38bdf8" stroke-width="1" stroke-dasharray="4,2"/>';
 svg += '<text x="'+(dX+dW/2)+'" y="'+(dY+12)+'" text-anchor="middle" fill="#38bdf8" font-size="6.5">Air-Draft Glass Shield</text>';

 // Weighing Pan & Stand
 const pPanX = dX + dW/2, pPanY = dY + dH - 12;
 svg += '<rect x="'+(pPanX-35)+'" y="'+pPanY+'" width="70" height="4" rx="2" fill="#94a3b8" stroke="#cbd5e1" stroke-width="0.8"/>';
 svg += '<rect x="'+(pPanX-6)+'" y="'+(pPanY+4)+'" width="12" height="8" fill="#64748b"/>';

 // Pycnometer on Pan (Weighed)
 const bPyX = pPanX, bPyY = pPanY - 48;
 svg += '<path d="M '+(bPyX-15)+' '+(bPyY+45)+' C '+(bPyX-24)+' '+(bPyY+27)+', '+(bPyX-12)+' '+(bPyY+10)+', '+(bPyX-5)+' '+(bPyY)+' L '+(bPyX+5)+' '+(bPyY)+' C '+(bPyX+12)+' '+(bPyY+10)+', '+(bPyX+24)+' '+(bPyY+27)+', '+(bPyX+15)+' '+(bPyY+45)+' Z" fill="#0ea5e9" fill-opacity="0.3" stroke="#38bdf8" stroke-width="1.2"/>';
 svg += '<path d="M '+(bPyX-14)+' '+(bPyY+44)+' C '+(bPyX-22)+' '+(bPyY+27)+', '+(bPyX-11)+' '+(bPyY+11)+', '+(bPyX-4)+' '+(bPyY+2)+' L '+(bPyX+4)+' '+(bPyY+2)+' C '+(bPyX+11)+' '+(bPyY+11)+', '+(bPyX+22)+' '+(bPyY+27)+', '+(bPyX+14)+' '+(bPyY+44)+' Z" fill="#10b981" fill-opacity="0.45"/>';
 svg += '<rect x="'+(bPyX-4)+'" y="'+(bPyY-18)+'" width="8" height="18" fill="#38bdf8" fill-opacity="0.25" stroke="#38bdf8" stroke-width="1"/>';
 svg += '<line x1="'+bPyX+'" y1="'+(bPyY-22)+'" x2="'+bPyX+'" y2="'+(bPyY+30)+'" stroke="#a7f3d0" stroke-width="1.2"/>';
 svg += '<ellipse cx="'+bPyX+'" cy="'+(bPyY-22)+'" rx="2" ry="1" fill="#4ade80"/>';

 // Digital Display Panel
 const dpX = aX + 20, dpY = aY + 148, dpW = aW - 40, dpH = 48;
 svg += '<rect x="'+dpX+'" y="'+dpY+'" width="'+dpW+'" height="'+dpH+'" rx="4" fill="#020804" stroke="#163824"/>';
 svg += '<rect x="'+(dpX+10)+'" y="'+(dpY+8)+'" width="'+(dpW-20)+'" height="32" rx="3" fill="#041208" stroke="#22c55e" stroke-width="0.8"/>';
 svg += '<text x="'+(dpX+dpW-20)+'" y="'+(dpY+30)+'" text-anchor="end" fill="#4ade80" font-size="16" font-family="monospace" font-weight="bold">'+m_filled.toFixed(4)+' g</text>';
 svg += '<text x="'+(dpX+16)+'" y="'+(dpY+22)+'" fill="#86efac" font-size="6.8" font-family="monospace">STABLE</text>';
 svg += '<text x="'+(dpX+16)+'" y="'+(dpY+32)+'" fill="#22c55e" font-size="6.8" font-family="monospace">NET</text>';


 // --- RIGHT: THERMODYNAMIC CALCULATOR & INVARIANTS (x: 500, y: 65, w: 185, h: 220) ---
 const cX = 500, cY = 65, cW = 185, cH = 220;
 svg += '<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" rx="8" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<rect x="'+(cX+8)+'" y="'+(cY+8)+'" width="'+(cW-16)+'" height="22" rx="4" fill="#132e1f" stroke="#1e4d31"/>';
 svg += '<text x="'+(cX+cW/2)+'" y="'+(cY+22)+'" text-anchor="middle" fill="#86efac" font-size="8.5" font-weight="bold">THERMODYNAMIC VALUES</text>';

 const statItems = [
  {label: 'Solute Molality m', val: m.toFixed(2)+' mol/kg', col: '#a7f3d0'},
  {label: 'Empty Pycnometer m₀', val: m_tare.toFixed(4)+' g', col: '#94a3b8'},
  {label: 'Liquid Mass m_liq', val: m_liq.toFixed(4)+' g', col: '#38bdf8'},
  {label: 'Solution Density ρ', val: rho_soln.toFixed(5)+' g/cm³', col: '#facc15'},
  {label: 'Apparent Volume φ_V', val: phi_calc.toFixed(3)+' cm³/mol', col: '#4ade80'},
  {label: 'Partial Molar V̄₂', val: V2_bar.toFixed(3)+' cm³/mol', col: '#38bdf8'},
  {label: 'Infinite Dilution V̄₂^∞', val: '54.20 cm³/mol', col: '#4ade80'}
 ];

 statItems.forEach((it, idx)=>{
  const sy = cY + 36 + idx * 24;
  svg += '<rect x="'+(cX+8)+'" y="'+sy+'" width="'+(cW-16)+'" height="20" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg += '<text x="'+(cX+14)+'" y="'+(sy+13)+'" fill="#94a3b8" font-size="7">'+it.label+'</text>';
  svg += '<text x="'+(cX+cW-14)+'" y="'+(sy+13)+'" text-anchor="end" fill="'+it.col+'" font-size="7.5" font-family="monospace" font-weight="bold">'+it.val+'</text>';
 });

 svg += '<rect x="'+(cX+8)+'" y="'+(cY+204)+'" width="'+(cW-16)+'" height="12" rx="2" fill="#022c22"/>';
 svg += '<text x="'+(cX+cW/2)+'" y="'+(cY+213)+'" text-anchor="middle" fill="#86efac" font-size="6.5" font-weight="bold">Contraction: ΔV_dil = −4.48 cm³/mol</text>';

 svg += text(360, 312, 'High-precision Gay-Lussac pycnometry at 25.00 °C: m₀ = 18.4250 g, V_pyc = 25.000 cm³.', '#789c80', 8.5);
 return svg;
}

function drawPycCompareView(p, rawVal){
 let svg = header('Excess Molar Volume & Hydrophobic Hydration Comparison');

 // Background
 svg += '<rect x="20" y="45" width="680" height="255" rx="6" fill="#06120b" stroke="#162e1e"/>';

 // 4 Comparative Stages
 const cols = [
  {title: 'Pure Solvent H₂O', m: 0.0, rho: 0.99705, phi: 18.068, v2: 18.068, desc: 'Open tetrahedral ice-like hydrogen cage network', col: '#38bdf8'},
  {title: 'Dilute EtOH (0.50 m)', m: 0.50, rho: 0.99312, phi: 54.325, v2: 54.450, desc: 'Interstitial ethyl packing in clathrate water cavities', col: '#4ade80'},
  {title: 'Moderate EtOH (2.0 m)', m: 2.00, rho: 0.98182, phi: 54.700, v2: 55.700, desc: 'Hydration shell overlap & hydrophobic contact', col: '#facc15'},
  {title: 'Pure Liquid EtOH', m: 'Pure', rho: 0.78520, phi: 58.680, v2: 58.680, desc: 'Bulk ethanol liquid with open linear hydrogen chains', col: '#f87171'}
 ];

 cols.forEach((c, idx)=>{
  const cx = 35 + idx * 165;
  const cy = 60, cw = 155, ch = 225;
  svg += '<rect x="'+cx+'" y="'+cy+'" width="'+cw+'" height="'+ch+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.2"/>';
  svg += '<rect x="'+(cx+6)+'" y="'+(cy+6)+'" width="'+(cw-12)+'" height="20" rx="3" fill="#132e1f"/>';
  svg += '<text x="'+(cx+cw/2)+'" y="'+(cy+19)+'" text-anchor="middle" fill="'+c.col+'" font-size="8" font-weight="bold">'+c.title+'</text>';

  // Visual Flask representation
  const flX = cx + cw/2, flY = cy + 40;
  svg += '<path d="M '+(flX-18)+' '+(flY+45)+' C '+(flX-28)+' '+(flY+25)+', '+(flX-12)+' '+(flY+8)+', '+(flX-5)+' '+(flY)+' L '+(flX+5)+' '+(flY)+' C '+(flX+12)+' '+(flY+8)+', '+(flX+28)+' '+(flY+25)+', '+(flX+18)+' '+(flY+45)+' Z" fill="'+c.col+'" fill-opacity="0.25" stroke="'+c.col+'" stroke-width="1.2"/>';

  // Molecular Representation Diagram
  if(idx === 0){
   // Pure water tetrahedral
   svg += '<circle cx="'+(flX)+' " cy="'+(flY+25)+'" r="4" fill="#38bdf8"/>';
   svg += '<circle cx="'+(flX-10)+'" cy="'+(flY+35)+'" r="3" fill="#e2e8f0"/>';
   svg += '<circle cx="'+(flX+10)+'" cy="'+(flY+35)+'" r="3" fill="#e2e8f0"/>';
   svg += '<line x1="'+flX+'" y1="'+(flY+25)+'" x2="'+(flX-10)+'" y2="'+(flY+35)+'" stroke="#38bdf8" stroke-dasharray="1,1"/>';
   svg += '<line x1="'+flX+'" y1="'+(flY+25)+'" x2="'+(flX+10)+'" y2="'+(flY+35)+'" stroke="#38bdf8" stroke-dasharray="1,1"/>';
  }else if(idx === 1){
   // Interstitial cavity
   svg += '<rect x="'+(flX-7)+'" y="'+(flY+22)+'" width="14" height="8" rx="3" fill="#4ade80"/>';
   svg += '<circle cx="'+(flX-14)+'" cy="'+(flY+26)+'" r="3" fill="#38bdf8" fill-opacity="0.6"/>';
   svg += '<circle cx="'+(flX+14)+'" cy="'+(flY+26)+'" r="3" fill="#38bdf8" fill-opacity="0.6"/>';
   svg += '<circle cx="'+flX+'" cy="'+(flY+14)+'" r="3" fill="#38bdf8" fill-opacity="0.6"/>';
   svg += '<circle cx="'+flX+'" cy="'+(flY+38)+'" r="3" fill="#38bdf8" fill-opacity="0.6"/>';
  }else if(idx === 2){
   // Cluster
   svg += '<rect x="'+(flX-12)+'" y="'+(flY+20)+'" width="12" height="7" rx="2" fill="#facc15"/>';
   svg += '<rect x="'+(flX)+'" y="'+(flY+24)+'" width="12" height="7" rx="2" fill="#facc15"/>';
  }else{
   // Pure ethanol chains
   svg += '<rect x="'+(flX-14)+'" y="'+(flY+16)+'" width="12" height="6" rx="2" fill="#f87171"/>';
   svg += '<rect x="'+(flX-2)+'" y="'+(flY+26)+'" width="12" height="6" rx="2" fill="#f87171"/>';
   svg += '<rect x="'+(flX-12)+'" y="'+(flY+36)+'" width="12" height="6" rx="2" fill="#f87171"/>';
  }

  // Quantitative Stats
  const infoY = cy + 100;
  svg += '<rect x="'+(cx+8)+'" y="'+infoY+'" width="'+(cw-16)+'" height="55" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg += '<text x="'+(cx+14)+'" y="'+(infoY+13)+'" fill="#94a3b8" font-size="6.8">Density ρ: <tspan fill="'+c.col+'" font-weight="bold">'+c.rho.toFixed(4)+' g/cm³</tspan></text>';
  svg += '<text x="'+(cx+14)+'" y="'+(infoY+26)+'" fill="#94a3b8" font-size="6.8">φ_V: <tspan fill="'+c.col+'" font-weight="bold">'+(typeof c.phi==='number'?c.phi.toFixed(2):c.phi)+' cm³/mol</tspan></text>';
  svg += '<text x="'+(cx+14)+'" y="'+(infoY+39)+'" fill="#94a3b8" font-size="6.8">Partial V̄₂: <tspan fill="'+c.col+'" font-weight="bold">'+(typeof c.v2==='number'?c.v2.toFixed(2):c.v2)+' cm³/mol</tspan></text>';
  svg += '<text x="'+(cx+14)+'" y="'+(infoY+50)+'" fill="#a7f3d0" font-size="6">ΔV_dil: '+(typeof c.v2==='number'?(c.v2-58.68).toFixed(2):'0.00')+' cm³/mol</text>';

  // Textual description
  svg += '<rect x="'+(cx+8)+'" y="'+(cy+162)+'" width="'+(cw-16)+'" height="55" rx="3" fill="#030805"/>';
  svg += '<text x="'+(cx+12)+'" y="'+(cy+174)+'" fill="#cbd5e1" font-size="6.5" width="'+(cw-24)+'">'+c.desc+'</text>';
 });

 svg += text(360, 312, 'Hydrophobic Hydration Invariant: V̄₂^∞ (54.20 cm³/mol) is 4.48 cm³/mol less than pure ethanol (58.68 cm³/mol).', '#789c80', 8.5);
 return svg;
}

function drawPycSandboxView(p, rawVal){
 let svg = header('Thermodynamic Indicator & Excess Volume Diagram ΔV^E');

 // Background
 svg += '<rect x="20" y="45" width="680" height="255" rx="6" fill="#06120b" stroke="#162e1e"/>';

 // --- LEFT: EXCESS MOLAR VOLUME & GIBBS-DUHEM CURVE (x: 35, y: 55, w: 370, h: 235) ---
 const lX = 35, lY = 55, lW = 370, lH = 235;
 svg += '<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="9" font-weight="bold">EXCESS MOLAR VOLUME ΔV^E & PARTIAL VOLUMES V̄_i</text>';

 // Plot Axes
 const gX = lX + 45, gY = lY + 35, gW = lW - 65, gH = lH - 80;
 svg += '<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#051009" stroke="#162e1e"/>';

 // Grid lines
 for(let i=1; i<5; i++){
  const gy = gY + (gH * i / 5);
  svg += '<line x1="'+gX+'" y1="'+gy+'" x2="'+(gX+gW)+'" y2="'+gy+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
  const gx = gX + (gW * i / 5);
  svg += '<line x1="'+gx+'" y1="'+gY+'" x2="'+gx+'" y2="'+(gY+gH)+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
 }

 // Labels
 svg += '<text x="'+(gX+gW/2)+'" y="'+(gY+gH+14)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">Ethanol Mole Fraction x₂</text>';
 svg += '<text x="'+(gX-8)+'" y="'+(gY+gH/2)+'" text-anchor="middle" transform="rotate(-90 '+(gX-8)+' '+(gY+gH/2)+')" fill="#94a3b8" font-size="7.5">Molar Volume (cm³/mol)</text>';

 // Zero line (Ideal mixing line for excess volume)
 const zeroY = gY + gH - 30;
 svg += '<line x1="'+gX+'" y1="'+zeroY+'" x2="'+(gX+gW)+'" y2="'+zeroY+'" stroke="#64748b" stroke-width="1" stroke-dasharray="3,2"/>';
 svg += '<text x="'+(gX+gW-5)+'" y="'+(zeroY-3)+'" text-anchor="end" fill="#64748b" font-size="6.5">ΔV_ideal = 0</text>';

 // Negative Excess Volume Curve ΔV^E = x1*x2 * [-4.48 ...]
 // Minimum at x2 ≈ 0.38, depth ΔV^E ≈ -1.1 cm³/mol
 const curveP = 'M '+gX+' '+zeroY+' Q '+(gX+gW*0.38)+' '+(zeroY+25)+' '+(gX+gW)+' '+zeroY;
 svg += '<path d="'+curveP+'" fill="none" stroke="#ef4444" stroke-width="2.2"/>';
 svg += '<text x="'+(gX+gW*0.38)+'" y="'+(zeroY+22)+'" text-anchor="middle" fill="#ef4444" font-size="7" font-weight="bold">Excess Volume ΔV^E < 0 (Contraction)</text>';

 // Ethanol Partial Molar Volume Curve V2_bar(x)
 // Starts at 54.20 (x=0) and rises to 58.68 (x=1)
 const v2_0_y = gY + 80; // corresponds to 54.20
 const v2_1_y = gY + 30; // corresponds to 58.68
 svg += '<path d="M '+gX+' '+v2_0_y+' Q '+(gX+gW*0.4)+' '+(v2_0_y-5)+' '+(gX+gW)+' '+v2_1_y+'" fill="none" stroke="#38bdf8" stroke-width="2"/>';
 svg += '<text x="'+(gX+10)+'" y="'+(v2_0_y-6)+'" fill="#38bdf8" font-size="7" font-weight="bold">V̄₂^∞ = 54.20 cm³/mol</text>';
 svg += '<text x="'+(gX+gW-10)+'" y="'+(v2_1_y-6)+'" text-anchor="end" fill="#38bdf8" font-size="7" font-weight="bold">V₂* = 58.68</text>';

 // Water Partial Molar Volume Curve V1_bar(x)
 // Starts at 18.07 (x=0) and drops slightly
 const v1_0_y = gY + 120;
 const v1_1_y = gY + 135;
 svg += '<path d="M '+gX+' '+v1_0_y+' Q '+(gX+gW*0.6)+' '+(v1_0_y+2)+' '+(gX+gW)+' '+v1_1_y+'" fill="none" stroke="#4ade80" stroke-width="1.8"/>';
 svg += '<text x="'+(gX+10)+'" y="'+(v1_0_y-6)+'" fill="#4ade80" font-size="7">V̄₁(H₂O) = 18.07 cm³/mol</text>';

 // Invariant badge at bottom
 svg += '<rect x="'+(lX+15)+'" y="'+(lY+195)+'" width="'+(lW-30)+'" height="32" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+215)+'" text-anchor="middle" fill="#86efac" font-size="7.8" font-family="monospace" font-weight="bold">Gibbs-Duhem Invariant: n₁ dV̄₁ + n₂ dV̄₂ = 0 across all compositions</text>';


 // --- RIGHT: SYSTEM AUDIT & PRECISION PYCNOMETRY CRITERIA ---
 const rX = 420, rY = 55, rW = 280, rH = 235;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="9" font-weight="bold">PRECISION PYCNOMETRY & AUDIT</text>';

 const auditItems = [
  {label: '±0.01 °C Thermal Stability', desc: 'Circulating water bath eliminates thermal expansion density drift', val: 'δρ < 7×10⁻⁶ g/cm³', col: '#4ade80'},
  {label: 'Lint-Free Meniscus Blotting', desc: 'Capillary flush wiping prevents interior suction wicking', val: 'δV < 0.08 μL', col: '#38bdf8'},
  {label: 'Dual Glass Counterpoise', desc: 'Symmetric tare vessel cancels air buoyancy & electrostatic drift', val: 'δm = ±0.0001 g', col: '#86efac'},
  {label: 'Vacuum Degassed Millipore', desc: 'Zero microbubble nucleations on internal pycnometer walls', val: 'No wall voids', col: '#facc15'},
  {label: 'Linear OLS Dilute Molality', desc: 'φ_V = φ_V° + b_V·m extrapolation eliminates random tare bias', val: 'R² = 0.99998', col: '#4ade80'}
 ];

 auditItems.forEach((it, idx)=>{
  const ay = rY + 30 + idx * 39;
  svg += '<rect x="'+(rX+8)+'" y="'+ay+'" width="'+(rW-16)+'" height="33" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg += '<text x="'+(rX+14)+'" y="'+(ay+12)+'" fill="'+it.col+'" font-size="7.5" font-weight="bold">'+it.label+'</text>';
  svg += '<text x="'+(rX+14)+'" y="'+(ay+24)+'" fill="#94a3b8" font-size="6.8">'+it.desc+'</text>';
  svg += '<text x="'+(rX+rW-14)+'" y="'+(ay+12)+'" text-anchor="end" fill="'+it.col+'" font-size="7.2" font-family="monospace">'+it.val+'</text>';
 });

 svg += text(360, 312, 'Thermodynamic Invariant: Limiting partial molar volume V̄₂^∞ = 54.20 cm³/mol with R² = 0.99998.', '#789c80', 8.5);
 return svg;
}


// ======================================================================
// LAB 19: LIQUID-VAPOR PHASE EQUILIBRIUM & AZEOTROPIC DISTILLATION
// ======================================================================

function getVleTb(x1){
 const x2 = 1.0 - x1;
 const A = 1.400;
 const gamma1 = Math.exp(A * x2 * x2);
 const gamma2 = Math.exp(A * x1 * x1);
 let low = 77.0, high = 100.0;
 for(let i=0; i<25; i++){
  const mid = (low + high) / 2.0;
  const P1 = 0.133322368 * Math.pow(10, 8.20417 - 1642.89 / (mid + 230.300));
  const P2 = 0.133322368 * Math.pow(10, 8.07131 - 1730.63 / (mid + 233.426));
  const P = P1 * x1 * gamma1 + P2 * x2 * gamma2;
  if(P < 101.325) low = mid;
  else high = mid;
 }
 return (low + high) / 2.0;
}

function getVleP1sat(T){
 return 0.133322368 * Math.pow(10, 8.20417 - 1642.89 / (T + 230.300));
}

function drawVleBenchView(p, rawVal){
 const x1 = p.input;
 const x2 = 1.0 - x1;
 const Tb = getVleTb(x1);
 const P1sat = getVleP1sat(Tb);
 const gamma1 = Math.exp(1.400 * x2 * x2);
 const P1 = P1sat * x1 * gamma1;
 const y1 = rawVal || (P1 / 101.325);
 const nD = 1.3330 + 0.0284 * y1;
 const alpha = (y1 / (1.0 - y1)) / (x1 / (1.0 - x1));

 let svg = header('Othmer Dynamic Recirculating VLE Still & Abbe Refractometer');

 // Background Lab Bench
 svg += '<rect x="20" y="45" width="680" height="255" rx="6" fill="#06120b" stroke="#162e1e"/>';

 // --- LEFT: OTHMER VLE STILL WITH COTTRELL PUMP (x: 35, y: 60, w: 250, h: 225) ---
 const sX = 35, sY = 60, sW = 250, sH = 225;
 svg += '<rect x="'+sX+'" y="'+sY+'" width="'+sW+'" height="'+sH+'" rx="8" fill="#0a1a12" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<rect x="'+(sX+8)+'" y="'+(sY+8)+'" width="'+(sW-16)+'" height="20" rx="3" fill="#0d2419" stroke="#163824"/>';
 svg += '<text x="'+(sX+sW/2)+'" y="'+(sY+22)+'" text-anchor="middle" fill="#86efac" font-size="8.5" font-weight="bold">OTHMER RECIRCULATING STILL (101.3 kPa)</text>';

 // Heating mantle at bottom
 const mX = sX + 35, mY = sY + 140, mW = 80, mH = 55;
 svg += '<path d="M '+mX+' '+(mY+15)+' Q '+(mX+mW/2)+' '+(mY+mH+10)+' '+(mX+mW)+' '+(mY+15)+' Z" fill="#991b1b" stroke="#ef4444" stroke-width="1.2"/>';
 svg += '<text x="'+(mX+mW/2)+'" y="'+(mY+mH+4)+'" text-anchor="middle" fill="#fca5a5" font-size="6.5">Heating Mantle (350 W)</text>';

 // Boiling flask (round bottom, vacuum-jacketed)
 const flX = mX + mW/2, flY = mY + 10, flR = 34;
 svg += '<circle cx="'+flX+'" cy="'+flY+'" r="'+flR+'" fill="#03150d" stroke="#38bdf8" stroke-width="1.2"/>';
 svg += '<path d="M '+(flX-flR+4)+' '+(flY+6)+' Q '+flX+' '+(flY+flR+2)+' '+(flX+flR-4)+' '+(flY+6)+' Z" fill="#0284c7" fill-opacity="0.4"/>';

 // Boiling bubbles
 for(let b=0; b<6; b++){
  const bx = flX - 18 + b * 7;
  const by = flY + 20 - (b % 3) * 6;
  svg += '<circle cx="'+bx+'" cy="'+by+'" r="2" fill="#e0f2fe" fill-opacity="0.7"/>';
 }

 // Cottrell Thermo-Lift Pump (inverted funnel + central lift tube)
 svg += '<path d="M '+(flX-14)+' '+(flY+24)+' L '+(flX-3)+' '+(flY)+' L '+(flX-3)+' '+(sY+50)+' L '+(flX+3)+' '+(sY+50)+' L '+(flX+3)+' '+(flY)+' L '+(flX+14)+' '+(flY+24)+' Z" fill="none" stroke="#4ade80" stroke-width="1.2"/>';
 // Spray hood over thermometer
 svg += '<path d="M '+(flX-10)+' '+(sY+48)+' Q '+flX+' '+(sY+38)+' '+(flX+10)+' '+(sY+48)+'" fill="none" stroke="#4ade80" stroke-width="1.5"/>';
 svg += '<circle cx="'+(flX-4)+'" cy="'+(sY+45)+'" r="1.5" fill="#38bdf8"/>';
 svg += '<circle cx="'+(flX+4)+'" cy="'+(sY+45)+'" r="1.5" fill="#38bdf8"/>';

 // PT100 Temperature Sensor (immersed in spray)
 svg += '<rect x="'+(flX-2)+'" y="'+(sY+32)+'" width="4" height="28" fill="#e2e8f0" stroke="#94a3b8" stroke-width="0.8"/>';
 svg += '<rect x="'+(flX-22)+'" y="'+(sY+28)+'" width="44" height="14" rx="2" fill="#020804" stroke="#22c55e" stroke-width="0.8"/>';
 svg += '<text x="'+flX+'" y="'+(sY+39)+'" text-anchor="middle" fill="#4ade80" font-size="8.5" font-family="monospace" font-weight="bold">'+Tb.toFixed(2)+'°C</text>';

 // Vapor Tube to Condenser
 const vX = flX + 2, vY = sY + 65;
 svg += '<path d="M '+vX+' '+vY+' L '+(sX+160)+' '+vY+' L '+(sX+160)+' '+(sY+115)+'" fill="none" stroke="#38bdf8" stroke-width="2"/>';

 // Water-Cooled Condenser
 const cdX = sX + 150, cdY = sY + 70, cdW = 20, cdH = 65;
 svg += '<rect x="'+cdX+'" y="'+cdY+'" width="'+cdW+'" height="'+cdH+'" rx="3" fill="#0369a1" fill-opacity="0.3" stroke="#0284c7" stroke-width="1"/>';
 svg += '<line x1="'+(cdX+cdW/2)+'" y1="'+cdY+'" x2="'+(cdX+cdW/2)+'" y2="'+(cdY+cdH)+'" stroke="#e0f2fe" stroke-width="1.5"/>';
 svg += '<text x="'+(cdX+cdW+4)+'" y="'+(cdY+30)+'" fill="#38bdf8" font-size="6.5">Condenser</text>';

 // Condensate Receiver Trap & Return Loop
 const rcX = sX + 150, rcY = sY + 140, rcW = 22, rcH = 40;
 svg += '<rect x="'+rcX+'" y="'+rcY+'" width="'+rcW+'" height="'+rcH+'" rx="3" fill="#041208" stroke="#22c55e" stroke-width="1"/>';
 svg += '<rect x="'+(rcX+2)+'" y="'+(rcY+15)+'" width="'+(rcW-4)+'" height="'+(rcH-17)+'" fill="#22c55e" fill-opacity="0.4"/>';
 svg += '<text x="'+(rcX+rcW/2)+'" y="'+(rcY+28)+'" text-anchor="middle" fill="#86efac" font-size="6.5" font-weight="bold">y₁</text>';
 // Return U-tube loop back to boiling flask
 svg += '<path d="M '+(rcX+rcW/2)+' '+(rcY+rcH)+' L '+(rcX+rcW/2)+' '+(sY+195)+' L '+(flX+15)+' '+(sY+195)+' L '+(flX+15)+' '+(flY+20)+'" fill="none" stroke="#22c55e" stroke-width="1.2" stroke-dasharray="3,2"/>';
 svg += '<text x="'+(sX+140)+'" y="'+(sY+205)+'" fill="#4ade80" font-size="6">Continuous Recirculation Reflux</text>';


 // --- CENTER: ABBE OPTICAL REFRACTOMETER (x: 295, y: 60, w: 220, h: 225) ---
 const aX = 295, aY = 60, aW = 220, aH = 225;
 svg += '<rect x="'+aX+'" y="'+aY+'" width="'+aW+'" height="'+aH+'" rx="8" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<rect x="'+(aX+8)+'" y="'+(aY+8)+'" width="'+(aW-16)+'" height="20" rx="3" fill="#132e1f" stroke="#1e4d31"/>';
 svg += '<text x="'+(aX+aW/2)+'" y="'+(aY+22)+'" text-anchor="middle" fill="#86efac" font-size="8.5" font-weight="bold">ABBE REFRACTOMETER (20.00 °C)</text>';

 // Refractometer Body & Prism Block
 const prX = aX + 25, prY = aY + 38;
 svg += '<rect x="'+prX+'" y="'+prY+'" width="55" height="30" rx="3" fill="#334155" stroke="#cbd5e1" stroke-width="1"/>';
 svg += '<path d="M '+(prX+5)+' '+(prY+5)+' L '+(prX+45)+' '+(prY+5)+' L '+(prX+25)+' '+(prY+25)+' Z" fill="#94a3b8" stroke="#f8fafc" stroke-width="0.8"/>';
 svg += '<text x="'+(prX+25)+'" y="'+(prY+15)+'" text-anchor="middle" fill="#0f172a" font-size="6" font-weight="bold">Prism</text>';
 svg += '<rect x="'+(prX+58)+'" y="'+(prY+8)+'" width="40" height="15" rx="2" fill="#022c22"/>';
 svg += '<text x="'+(prX+78)+'" y="'+(prY+19)+'" text-anchor="middle" fill="#4ade80" font-size="7" font-weight="bold">20.00 °C</text>';

 // Eyepiece Reticle Field of View (Circular split field)
 const retX = aX + aW/2 + 25, retY = aY + 115, retR = 40;
 svg += '<circle cx="'+retX+'" cy="'+retY+'" r="'+retR+'" fill="#030712" stroke="#38bdf8" stroke-width="1.5"/>';

 // Split boundary: top half dark, bottom half illuminated
 const boundY = retY - 5; // aligned to shadow line
 svg += '<clipPath id="reticleClip"><circle cx="'+retX+'" cy="'+retY+'" r="'+(retR-1)+'"/></clipPath>';
 svg += '<g clip-path="url(#reticleClip)">';
 svg += '<rect x="'+(retX-retR)+'" y="'+(retY-retR)+'" width="'+(2*retR)+'" height="'+(retR-5)+'" fill="#090d16"/>';
 svg += '<rect x="'+(retX-retR)+'" y="'+boundY+'" width="'+(2*retR)+'" height="'+(retR+5)+'" fill="#facc15" fill-opacity="0.85"/>';
 // Crosshairs
 svg += '<line x1="'+(retX-retR)+'" y1="'+retY+'" x2="'+(retX+retR)+'" y2="'+retY+'" stroke="#ef4444" stroke-width="1"/>';
 svg += '<line x1="'+retX+'" y1="'+(retY-retR)+'" x2="'+retX+'" y2="'+(retY+retR)+'" stroke="#ef4444" stroke-width="1"/>';
 svg += '</g>';
 svg += '<text x="'+retX+'" y="'+(retY+retR+12)+'" text-anchor="middle" fill="#facc15" font-size="7" font-weight="bold">Optical Reticle Horizon</text>';

 // Refractometer Scale Readout
 const scY = aY + 175;
 svg += '<rect x="'+(aX+15)+'" y="'+scY+'" width="85" height="38" rx="3" fill="#020804" stroke="#163824"/>';
 svg += '<text x="'+(aX+57)+'" y="'+(scY+13)+'" text-anchor="middle" fill="#94a3b8" font-size="6.8">Refractive Index</text>';
 svg += '<text x="'+(aX+57)+'" y="'+(scY+30)+'" text-anchor="middle" fill="#38bdf8" font-size="12" font-family="monospace" font-weight="bold">'+nD.toFixed(4)+'</text>';


 // --- RIGHT: PHASE EQUILIBRIUM VALUES & INVARIANTS (x: 525, y: 60, w: 165, h: 225) ---
 const cX = 525, cY = 60, cW = 165, cH = 225;
 svg += '<rect x="'+cX+'" y="'+cY+'" width="'+cW+'" height="'+cH+'" rx="8" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<rect x="'+(cX+8)+'" y="'+(cY+8)+'" width="'+(cW-16)+'" height="20" rx="3" fill="#132e1f" stroke="#1e4d31"/>';
 svg += '<text x="'+(cX+cW/2)+'" y="'+(cY+22)+'" text-anchor="middle" fill="#86efac" font-size="8" font-weight="bold">VLE EQUILIBRIUM DATA</text>';

 const statItems = [
  {label: 'Liquid x_EtOH', val: x1.toFixed(2), col: '#a7f3d0'},
  {label: 'Boiling Temp T_b', val: Tb.toFixed(2)+' °C', col: '#facc15'},
  {label: 'Vapor y_EtOH', val: y1.toFixed(4), col: '#38bdf8'},
  {label: 'P₁*(T_b) Pure Sat', val: P1sat.toFixed(1)+' kPa', col: '#94a3b8'},
  {label: 'Activity Coeff γ₁', val: gamma1.toFixed(3), col: '#4ade80'},
  {label: 'ln(γ₁) Margules', val: Math.log(gamma1).toFixed(4), col: '#4ade80'},
  {label: 'Relative Volatility α', val: alpha.toFixed(3), col: '#38bdf8'}
 ];

 statItems.forEach((it, idx)=>{
  const sy = cY + 34 + idx * 22;
  svg += '<rect x="'+(cX+6)+'" y="'+sy+'" width="'+(cW-12)+'" height="19" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg += '<text x="'+(cX+10)+'" y="'+(sy+13)+'" fill="#94a3b8" font-size="6.8">'+it.label+'</text>';
  svg += '<text x="'+(cX+cW-10)+'" y="'+(sy+13)+'" text-anchor="end" fill="'+it.col+'" font-size="7.2" font-family="monospace" font-weight="bold">'+it.val+'</text>';
 });

 svg += '<rect x="'+(cX+6)+'" y="'+(cY+194)+'" width="'+(cW-12)+'" height="22" rx="3" fill="#022c22"/>';
 svg += '<text x="'+(cX+cW/2)+'" y="'+(cY+204)+'" text-anchor="middle" fill="#86efac" font-size="6.5" font-weight="bold">Azeotrope: x_azeo = 0.894</text>';
 svg += '<text x="'+(cX+cW/2)+'" y="'+(cY+213)+'" text-anchor="middle" fill="#a7f3d0" font-size="6">Boiling Min: T_azeo = 78.15 °C</text>';

 svg += text(360, 312, 'Othmer dynamic VLE still at 101.325 kPa: Cottrell pump eliminates superheating, Abbe n_D²⁰ yields y₁.', '#789c80', 8.5);
 return svg;
}

function drawVleCompareView(p, rawVal){
 const curX = p.input;
 const curY = rawVal || (getVleP1sat(getVleTb(curX)) * curX * Math.exp(1.400 * (1-curX)**2) / 101.325);
 const curTb = getVleTb(curX);

 let svg = header('T-x-y Phase Diagram & Azeotropic Pinch (101.325 kPa)');

 // Background
 svg += '<rect x="20" y="45" width="680" height="255" rx="6" fill="#06120b" stroke="#162e1e"/>';

 // Plot Frame (x: 40, y: 55, w: 410, h: 235)
 const gX = 45, gY = 60, gW = 390, gH = 185;
 svg += '<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" rx="4" fill="#0d1f14" stroke="#22422c" stroke-width="1.2"/>';

 // Grid lines & Axis labels
 for(let i=1; i<5; i++){
  const gy = gY + (gH * i / 5);
  svg += '<line x1="'+gX+'" y1="'+gy+'" x2="'+(gX+gW)+'" y2="'+gy+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
  const gx = gX + (gW * i / 5);
  svg += '<line x1="'+gx+'" y1="'+gY+'" x2="'+gx+'" y2="'+(gY+gH)+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
 }

 svg += '<text x="'+(gX+gW/2)+'" y="'+(gY+gH+14)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">Ethanol Mole Fraction (x₁, y₁)</text>';
 svg += '<text x="'+(gX-8)+'" y="'+(gY+gH/2)+'" text-anchor="middle" transform="rotate(-90 '+(gX-8)+' '+(gY+gH/2)+')" fill="#94a3b8" font-size="7.5">Boiling Temperature T_b (°C)</text>';

 // Temperature calibration: T goes from 100 °C (bottom or top?) -> Top is 102 C (y=gY), Bottom is 76 C (y=gY+gH)
 // y_coord(T) = gY + (102.0 - T) / (102.0 - 76.0) * gH
 function tempY(T){
  return gY + (102.0 - T) / (26.0) * gH;
 }
 function moleX(z){
  return gX + z * gW;
 }

 // Liquidus curve (bubble point curve Tb(x1))
 // Water (x=0, T=100.0 C), Azeotrope (x=0.894, T=78.15 C), Pure EtOH (x=1.0, T=78.37 C)
 let liqPath = 'M '+moleX(0)+' '+tempY(100.0);
 for(let step=1; step<=40; step++){
  const z = step / 40.0;
  const T = getVleTb(z);
  liqPath += ' L '+moleX(z)+' '+tempY(T);
 }
 svg += '<path d="'+liqPath+'" fill="none" stroke="#38bdf8" stroke-width="2.2"/>';
 svg += '<text x="'+(gX+40)+'" y="'+(tempY(93.0))+'" fill="#38bdf8" font-size="7" font-weight="bold">Liquidus Bubble Curve T(x)</text>';

 // Vaporus curve (dew point curve Tb(y1))
 let vapPath = 'M '+moleX(0)+' '+tempY(100.0);
 for(let step=1; step<=40; step++){
  const z = step / 40.0;
  const T = getVleTb(z);
  const P1s = getVleP1sat(T);
  const yz = P1s * z * Math.exp(1.400 * (1-z)**2) / 101.325;
  vapPath += ' L '+moleX(yz)+' '+tempY(T);
 }
 svg += '<path d="'+vapPath+'" fill="none" stroke="#f87171" stroke-width="2.2"/>';
 svg += '<text x="'+(gX+170)+'" y="'+(tempY(83.5))+'" fill="#f87171" font-size="7" font-weight="bold">Vaporus Dew Curve T(y)</text>';

 // Minimum Azeotropic Point (x=0.894, T=78.15 C)
 const azX = moleX(0.894), azY = tempY(78.15);
 svg += '<circle cx="'+azX+'" cy="'+azY+'" r="5" fill="#facc15" stroke="#ffffff" stroke-width="1.2"/>';
 svg += '<text x="'+(azX)+'" y="'+(azY-8)+'" text-anchor="middle" fill="#facc15" font-size="7.5" font-weight="bold">Azeotrope (0.894, 78.15 °C)</text>';

 // Current Tie Line at input x1
 const curLiqX = moleX(curX), curLiqY = tempY(curTb);
 const curVapX = moleX(curY), curVapY = tempY(curTb);
 svg += '<line x1="'+curLiqX+'" y1="'+curLiqY+'" x2="'+curVapX+'" y2="'+curVapY+'" stroke="#4ade80" stroke-width="2" stroke-dasharray="3,2"/>';
 svg += '<circle cx="'+curLiqX+'" cy="'+curLiqY+'" r="4" fill="#38bdf8"/>';
 svg += '<circle cx="'+curVapX+'" cy="'+curVapY+'" r="4" fill="#f87171"/>';
 svg += '<text x="'+(curLiqX)+'" y="'+(curLiqY+12)+'" text-anchor="middle" fill="#38bdf8" font-size="6.8">x₁='+curX.toFixed(2)+'</text>';
 svg += '<text x="'+(curVapX)+'" y="'+(curVapY-8)+'" text-anchor="middle" fill="#f87171" font-size="6.8">y₁='+curY.toFixed(3)+'</text>';

 // Legend & Phase Regions
 svg += '<text x="'+(gX+85)+'" y="'+(gY+25)+'" fill="#94a3b8" font-size="7">Subcooled Liquid</text>';
 svg += '<text x="'+(gX+140)+'" y="'+(gY+110)+'" fill="#4ade80" font-size="7.5" font-weight="bold">Two-Phase Liquid + Vapor Coexistence</text>';
 svg += '<text x="'+(gX+280)+'" y="'+(gY+165)+'" fill="#fca5a5" font-size="7">Superheated Vapor</text>';


 // --- RIGHT: AZEOTROPE BREAKER TECHNOLOGIES (x: 450, y: 55, w: 250, h: 235) ---
 const rX = 450, rY = 55, rW = 250, rH = 235;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="8" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<rect x="'+(rX+8)+'" y="'+(rY+8)+'" width="'+(rW-16)+'" height="20" rx="3" fill="#132e1f" stroke="#1e4d31"/>';
 svg += '<text x="'+(rX+rW/2)+'" y="'+(rY+22)+'" text-anchor="middle" fill="#86efac" font-size="8.5" font-weight="bold">HOW INDUSTRY BREAKS THE AZEOTROPE</text>';

 const techItems = [
  {name: '1. Type 3A Molecular Sieves', desc: 'Synthetic zeolite pores (3 Å) adsorb H2O (2.8 Å) & reject EtOH (4.4 Å)', eff: '>99.9% Anhydrous', col: '#4ade80'},
  {name: '2. Pressure-Swing Distillation', desc: 'Azeotrope vanishes below 11.5 kPa; dual columns cross pinch', eff: 'No Entrainer', col: '#38bdf8'},
  {name: '3. Cyclohexane Entrainer Distillation', desc: 'Forms ternary azeotrope (64.9 °C) taking water overhead', eff: '99.8% Pure', col: '#facc15'},
  {name: '4. Extractive Distillation (Glycol)', desc: 'High-boiling ethylene glycol breaks relative volatility pinch', eff: 'Continuous Process', col: '#86efac'},
  {name: '5. Vapor Pervaporation Membranes', desc: 'Hydrophilic polymeric membrane preferentially diffuses water', eff: 'Energy Efficient', col: '#38bdf8'}
 ];

 techItems.forEach((t, idx)=>{
  const ty = rY + 32 + idx * 39;
  svg += '<rect x="'+(rX+8)+'" y="'+ty+'" width="'+(rW-16)+'" height="33" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg += '<text x="'+(rX+12)+'" y="'+(ty+11)+'" fill="'+t.col+'" font-size="7.2" font-weight="bold">'+t.name+'</text>';
  svg += '<text x="'+(rX+12)+'" y="'+(ty+23)+'" fill="#94a3b8" font-size="6.5">'+t.desc+'</text>';
  svg += '<text x="'+(rX+rW-12)+'" y="'+(ty+11)+'" text-anchor="end" fill="'+t.col+'" font-size="7" font-family="monospace">'+t.eff+'</text>';
 });

 svg += text(360, 312, 'Gibbs-Konovalov Invariant: At the azeotrope x₁ = y₁ = 0.894, dT/dx₁ = 0 and relative volatility α = 1.000.', '#789c80', 8.5);
 return svg;
}

function drawVleSandboxView(p, rawVal){
 let svg = header('Margules Thermodynamic Regular Solution & Excess Gibbs Energy');

 // Background
 svg += '<rect x="20" y="45" width="680" height="255" rx="6" fill="#06120b" stroke="#162e1e"/>';

 // --- LEFT: MARGULES EXCESS GIBBS ENERGY & ACTIVITY PLOT (x: 35, y: 55, w: 370, h: 235) ---
 const lX = 35, lY = 55, lW = 370, lH = 235;
 svg += '<rect x="'+lX+'" y="'+lY+'" width="'+lW+'" height="'+lH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+18)+'" text-anchor="middle" fill="#86efac" font-size="9" font-weight="bold">MARGULES EXCESS GIBBS ENERGY g^E & ln(γ_i)</text>';

 const gX = lX + 45, gY = lY + 35, gW = lW - 65, gH = lH - 80;
 svg += '<rect x="'+gX+'" y="'+gY+'" width="'+gW+'" height="'+gH+'" fill="#051009" stroke="#162e1e"/>';

 // Grid
 for(let i=1; i<5; i++){
  const gy = gY + (gH * i / 5);
  svg += '<line x1="'+gX+'" y1="'+gy+'" x2="'+(gX+gW)+'" y2="'+gy+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
  const gx = gX + (gW * i / 5);
  svg += '<line x1="'+gx+'" y1="'+gY+'" x2="'+gx+'" y2="'+(gY+gH)+'" stroke="#162e1e" stroke-width="0.8" stroke-dasharray="2,2"/>';
 }

 svg += '<text x="'+(gX+gW/2)+'" y="'+(gY+gH+14)+'" text-anchor="middle" fill="#94a3b8" font-size="7.5">Ethanol Mole Fraction x₁</text>';
 svg += '<text x="'+(gX-8)+'" y="'+(gY+gH/2)+'" text-anchor="middle" transform="rotate(-90 '+(gX-8)+' '+(gY+gH/2)+')" fill="#94a3b8" font-size="7.5">Thermodynamic Function</text>';

 // g^E / RT curve = 1.4 * x1 * (1 - x1), peak at x=0.5 with value 0.35
 const zeroY = gY + gH - 10;
 const peakY = zeroY - (0.35 / 1.5) * (gH - 20);
 const gePath = 'M '+gX+' '+zeroY+' Q '+(gX+gW*0.5)+' '+(peakY-15)+' '+(gX+gW)+' '+zeroY;
 svg += '<path d="'+gePath+'" fill="none" stroke="#4ade80" stroke-width="2.2"/>';
 svg += '<text x="'+(gX+gW*0.5)+'" y="'+(peakY-22)+'" text-anchor="middle" fill="#4ade80" font-size="7" font-weight="bold">g^E / RT = 1.400·x₁·x₂</text>';

 // ln(gamma1) curve = 1.4 * (1 - x1)^2: starts at 1.40 (x=0) and drops to 0 (x=1)
 const ln1_0 = zeroY - (1.40 / 1.5) * (gH - 20);
 const ln1Path = 'M '+gX+' '+ln1_0+' Q '+(gX+gW*0.4)+' '+(zeroY-25)+' '+(gX+gW)+' '+zeroY;
 svg += '<path d="'+ln1Path+'" fill="none" stroke="#38bdf8" stroke-width="2"/>';
 svg += '<text x="'+(gX+10)+'" y="'+(ln1_0-6)+'" fill="#38bdf8" font-size="7" font-weight="bold">ln(γ₁) = A(1−x₁)² (γ₁^∞ = 4.055)</text>';

 // ln(gamma2) curve = 1.4 * x1^2: starts at 0 (x=0) and rises to 1.40 (x=1)
 const ln2Path = 'M '+gX+' '+zeroY+' Q '+(gX+gW*0.6)+' '+(zeroY-25)+' '+(gX+gW)+' '+ln1_0;
 svg += '<path d="'+ln2Path+'" fill="none" stroke="#f87171" stroke-width="1.8" stroke-dasharray="3,2"/>';
 svg += '<text x="'+(gX+gW-10)+'" y="'+(ln1_0-6)+'" text-anchor="end" fill="#f87171" font-size="7">ln(γ₂ Water)</text>';

 // Invariant badge at bottom
 svg += '<rect x="'+(lX+15)+'" y="'+(lY+195)+'" width="'+(lW-30)+'" height="32" rx="3" fill="#051009" stroke="#162e1e"/>';
 svg += '<text x="'+(lX+lW/2)+'" y="'+(lY+215)+'" text-anchor="middle" fill="#86efac" font-size="7.8" font-family="monospace" font-weight="bold">Thermodynamic Invariant: Symmetric Margules model A = 1.400 yields R² = 1.00000</text>';


 // --- RIGHT: SOURCES OF BIAS & VLE AUDIT ---
 const rX = 420, rY = 55, rW = 280, rH = 235;
 svg += '<rect x="'+rX+'" y="'+rY+'" width="'+rW+'" height="'+rH+'" rx="6" fill="#0d1f14" stroke="#22422c" stroke-width="1.5"/>';
 svg += '<text x="'+(rX+rW/2)+'" y="'+(rY+18)+'" text-anchor="middle" fill="#86efac" font-size="9" font-weight="bold">VLE METROLOGY & SYSTEM AUDIT</text>';

 const auditItems = [
  {label: 'Cottrell Thermo-Lift Pumping', desc: 'Eliminates 1.5 °C liquid superheating; washes sensor in spray', val: 'δT = ±0.02 °C', col: '#4ade80'},
  {label: 'Abbe Water-Jacket Prism (20.00 °C)', desc: 'Suppresses thermal refractive drift dn_D/dT (-4.0×10⁻⁴ K⁻¹)', val: 'δn_D = ±0.0001', col: '#38bdf8'},
  {label: 'Digital Absolute Barometer', desc: 'Real-time 101.325 kPa pressure normalization via Antoine law', val: 'δP < 0.01 kPa', col: '#86efac'},
  {label: 'Chilled Airtight Septum Syringes', desc: 'Prevents flash evaporation of volatile ethanol during transfer', val: 'δx < 0.001', col: '#facc15'},
  {label: 'Margules Linear Least-Squares', desc: 'Linearization ln(γ₁) vs (1−x₁)² eliminates tare/parallax bias', val: 'R² = 1.00000', col: '#4ade80'}
 ];

 auditItems.forEach((it, idx)=>{
  const ay = rY + 30 + idx * 39;
  svg += '<rect x="'+(rX+8)+'" y="'+ay+'" width="'+(rW-16)+'" height="33" rx="3" fill="#051009" stroke="#162e1e"/>';
  svg += '<text x="'+(rX+14)+'" y="'+(ay+12)+'" fill="'+it.col+'" font-size="7.5" font-weight="bold">'+it.label+'</text>';
  svg += '<text x="'+(rX+14)+'" y="'+(ay+24)+'" fill="#94a3b8" font-size="6.8">'+it.desc+'</text>';
  svg += '<text x="'+(rX+rW-14)+'" y="'+(ay+12)+'" text-anchor="end" fill="'+it.col+'" font-size="7.2" font-family="monospace">'+it.val+'</text>';
 });

 svg += text(360, 312, 'Phase Invariant: Activity coefficient ln(γ₁) = 1.400·(1−x₁)² isolates A = 1.400 with R² = 1.00000.', '#789c80', 8.5);
 return svg;
}
