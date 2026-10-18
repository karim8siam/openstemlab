(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Hematology & Clinical Blood Analysis (Labs 1–7)
  'erythrocyte-sedimentation-rate-westergren': { type: 'linear_affine', slope: 0.6800, intercept: 2.5000, ref: 0.6800 },
  'hemoglobin-spectrophotometry-cyanmethemoglobin-drabkin': { type: 'linear_prop', slope: 0.0380, ref: 0.0380 },
  'red-blood-cell-osmotic-fragility-hemolysis': { type: 'linear_affine', slope: -145.0000, intercept: 115.0000, ref: 145.0000, abs_ref: true },
  'hematocrit-microcentrifugation-packed-cell-volume': { type: 'linear_prop', slope: 0.0100, ref: 0.0100 },
  'differential-leukocyte-count-leishman-smear': { type: 'linear_prop', slope: 75.0000, ref: 75.0000 },
  'bleeding-time-clotting-time-hemostasis': { type: 'linear_affine', slope: 1.8500, intercept: 2.2000, ref: 1.8500 },
  'blood-group-antigen-agglutination-titer': { type: 'linear_affine', slope: -0.6500, intercept: 10.5000, ref: 0.6500, abs_ref: true },

  // Module 2: Cardiovascular & Hemodynamic Physiology (Labs 8–14)
  'arterial-blood-pressure-sphygmomanometer-korotkoff': { type: 'linear_affine', slope: 0.6667, intercept: 26.6667, ref: 0.6667 },
  'electrocardiogram-ecg-intervals-axis-determination': { type: 'linear_prop', slope: 0.0312, ref: 0.0312 },
  'cardiac-output-fick-principle-oxygen-consumption': { type: 'linear_prop', slope: 0.0200, ref: 0.0200 },
  'arterial-pulse-wave-velocity-vascular-compliance': { type: 'linear_affine', slope: 0.8500, intercept: 1.2500, ref: 0.8500 },
  'cold-pressor-test-sympathetic-vasoreactivity': { type: 'linear_prop', slope: 1.2500, ref: 1.2500 },
  'venous-pressure-gaertner-jugular-pulsation': { type: 'linear_prop', slope: 0.7355, ref: 0.7355 },
  'capillary-fragility-hess-rumpel-leede-petechiae': { type: 'linear_affine', slope: 0.9500, intercept: 1.2000, ref: 0.9500 },

  // Module 3: Neurophysiology, Neuromuscular & Sensory Function (Labs 15–21)
  'motor-nerve-conduction-velocity-compound-muscle-potential': { type: 'linear_prop', slope: 0.01786, ref: 0.01786 },
  'h-reflex-hoffmann-monosynaptic-arc-latency': { type: 'linear_affine', slope: 0.4200, intercept: 16.5000, ref: 0.4200 },
  'surface-electromyography-isometric-force-fatigue': { type: 'linear_prop', slope: 7.5000, ref: 7.5000 },
  'visual-evoked-potentials-p100-latency-reversal': { type: 'linear_affine', slope: 0.7500, intercept: 45.0000, ref: 0.7500 },
  'pure-tone-audiometry-air-bone-conduction-threshold': { type: 'linear_affine', slope: 1.1500, intercept: -2.5000, ref: 1.1500 },
  'caloric-vestibulo-ocular-reflex-electronystagmography': { type: 'linear_prop', slope: 2.2000, ref: 2.2000 },
  'cutaneous-two-point-discrimination-weber-esthesiometer': { type: 'linear_prop', slope: 0.0850, ref: 0.0850 },

  // Module 4: Pulmonary Mechanics & Respiratory Gas Exchange (Labs 22–28)
  'spirometry-forced-vital-capacity-fev1-ratio': { type: 'linear_prop', slope: 0.0420, ref: 0.0420 },
  'peak-expiratory-flow-wright-meter-airway-resistance': { type: 'linear_affine', slope: -0.0035, intercept: 3.2000, ref: 0.0035, abs_ref: true },
  'alveolar-gas-equation-paO2-arterial-oxygen-gradient': { type: 'linear_affine', slope: -1.2500, intercept: 149.0000, ref: 1.2500, abs_ref: true },
  'static-pulmonary-compliance-transpulmonary-pressure': { type: 'linear_prop', slope: 0.2000, ref: 0.2000 },
  'anatomical-dead-space-fowler-single-breath-nitrogen': { type: 'linear_prop', slope: 2.2000, ref: 2.2000 },
  'diffusing-capacity-carbon-monoxide-dlco-gas-transfer': { type: 'linear_prop', slope: 0.2500, ref: 0.2500 },
  'arterial-blood-gas-henderson-hasselbalch-acid-base': { type: 'linear_affine', slope: 0.0320, intercept: 6.6300, ref: 0.0320 },

  // Module 5: Renal Physiology, Fluid-Electrolyte & Clinical Biochemistry (Labs 29–35)
  'creatinine-clearance-glomerular-filtration-rate': { type: 'linear_prop', slope: 0.7000, ref: 0.7000 },
  'urine-specific-gravity-refractometer-osmolality': { type: 'linear_prop', slope: 35000.0000, ref: 35000.0000 },
  'fractional-excretion-sodium-feNa-acute-kidney-injury': { type: 'linear_prop', slope: 1.0000, ref: 1.0000 },
  'spectrophotometric-blood-glucose-god-pod-enzymatic': { type: 'linear_prop', slope: 0.0035, ref: 0.0035 },
  'serum-total-protein-biuret-albumin-globulin-ratio': { type: 'linear_prop', slope: 0.0750, ref: 0.0750 },
  'serum-bilirubin-jendrassik-grof-diazo-method': { type: 'linear_prop', slope: 0.1250, ref: 0.1250 },
  'serum-amylase-caraway-iodometric-starch-hydrolysis': { type: 'linear_affine', slope: -0.0018, intercept: 0.8200, ref: 0.0018, abs_ref: true },

  // Module 6: Histopathology, Preclinical Pharmacology & Pharmacokinetics (Labs 36–42)
  'hematoxylin-eosin-tissue-morphometry-epithelium': { type: 'linear_prop', slope: 1.4500, ref: 1.4500 },
  'isolated-ileum-smooth-muscle-acetylcholine-dose-response': { type: 'linear_affine', slope: 18.5000, intercept: -35.0000, ref: 18.5000 },
  'competitive-receptor-antagonism-schild-regression-pa2': { type: 'linear_affine', slope: 1.0000, intercept: 8.8500, ref: 1.0000 },
  'pharmacokinetics-one-compartment-elimination-half-life': { type: 'linear_affine', slope: -0.2166, intercept: 4.6052, ref: 0.2166, abs_ref: true },
  'antimicrobial-susceptibility-kirby-bauer-zone-diameter': { type: 'linear_affine', slope: -3.8000, intercept: 34.5000, ref: 3.8000, abs_ref: true },
  'enzyme-kinetics-michaelis-menten-lineweaver-burk': { type: 'linear_affine', slope: 0.0450, intercept: 0.1000, ref: 0.0450 },
  'cardiac-glycoside-ouabain-na-k-atpase-inhibition': { type: 'linear_affine', slope: -22.5000, intercept: 95.0000, ref: 22.5000, abs_ref: true }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Basic Medical Sciences experiment: ' + slug);

  if (p.type === 'linear_prop') {
    const raw = round(p.slope * inp, 4);
    return { valid: true, raw: raw, displayed: raw };
  }

  if (p.type === 'linear_affine') {
    const raw = round(p.slope * inp + (p.intercept || 0), 4);
    return { valid: true, raw: raw, displayed: raw };
  }

  throw Error('Unknown parameter type: ' + p.type);
}

function reading(slug, input, raw){
  const inp = Number(input);
  const r = Number(raw);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown experiment: ' + slug);

  const x = round(inp, 4);
  const y = round(r, 4);
  return { input: inp, raw: r, x: x, y: y };
}

function fit(rows){
  const n = rows.length;
  if (n < 2) return null;
  let sx = 0, sy = 0, sxy = 0, sxx = 0, syy = 0;
  for (let i = 0; i < n; i++) {
    const x = rows[i].x;
    const y = rows[i].y;
    sx += x; sy += y;
    sxy += x * y;
    sxx += x * x;
    syy += y * y;
  }
  const denom = n * sxx - sx * sx;
  if (Math.abs(denom) < 1e-12) return null;
  const slope = round((n * sxy - sx * sy) / denom, 5);
  const intercept = round((sy - slope * sx) / n, 5);

  const ssTot = syy - (sy * sy) / n;
  let ssRes = 0;
  for (let i = 0; i < n; i++) {
    const yPred = slope * rows[i].x + intercept;
    const diff = rows[i].y - yPred;
    ssRes += diff * diff;
  }
  let r2 = 1.0;
  if (ssTot > 1e-12) {
    r2 = round(Math.max(0, 1 - ssRes / ssTot), 6);
  }
  return { slope: slope, intercept: intercept, r2: r2, n: n };
}

function estimate(slug, fitRes){
  const p = PARAMS[slug];
  if (!p || !fitRes) return { value: 0, reference: 0, errorPercent: 0 };
  let val = fitRes.slope;
  if (p.abs_ref) val = Math.abs(val);
  const ref = p.ref;
  const err = round(Math.abs(val - ref) / Math.abs(ref) * 100, 4);
  return { value: val, reference: ref, errorPercent: err };
}

const api = { predict, reading, fit, estimate, PARAMS };
if (typeof module !== 'undefined' && module.exports) {
  module.exports = api;
} else {
  root.BasicMedicalModels = api;
}
})(typeof window !== 'undefined' ? window : globalThis);
