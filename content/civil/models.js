(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Structural Materials & Concrete Technology (Labs 1–9)
  'concrete-slump-test-workability-abrams-cone': { type: 'linear_affine', slope: 240.0000, intercept: -75.0000, ref: 240.0000 },
  'compressive-strength-concrete-cylinders-curing-age': { type: 'log_input', slope: 8.5000, intercept: 12.0000, ref: 8.5000 },
  'flexural-tensile-strength-concrete-modulus-rupture': { type: 'linear_prop', slope: 0.1333, ref: 0.1333 },
  'splitting-tensile-strength-concrete-brazilian-test': { type: 'linear_prop', slope: 0.01415, ref: 0.01415 },
  'sieve-analysis-fine-aggregate-fineness-modulus': { type: 'linear_prop', slope: 28.5000, ref: 28.5000 },
  'specific-gravity-water-absorption-coarse-aggregate': { type: 'linear_prop', slope: 1.0185, ref: 1.0185 },
  'setting-time-portland-cement-vicat-needle': { type: 'linear_affine', slope: -0.1850, intercept: 45.0000, ref: 0.1850, abs_ref: true },
  'standard-consistency-portland-cement-paste': { type: 'linear_affine', slope: 3.2000, intercept: -70.0000, ref: 3.2000 },
  'soundness-of-cement-le-chatelier-autoclave-expansion': { type: 'linear_prop', slope: 2.4500, ref: 2.4500 },

  // Module 2: Mechanics of Materials & Structural Analysis (Labs 10–18)
  'tensile-testing-structural-mild-steel-rebar': { type: 'linear_prop', slope: 0.2000, ref: 0.2000 },
  'charpy-v-notch-impact-toughness-structural-steel': { type: 'linear_affine', slope: 0.8500, intercept: 65.0000, ref: 0.8500 },
  'brinell-and-rockwell-hardness-structural-alloys': { type: 'linear_prop', slope: 1.4250, ref: 1.4250 },
  'deflection-simply-supported-structural-beam': { type: 'linear_prop', slope: 0.4250, ref: 0.4250 },
  'maxwell-betti-reciprocal-deflection-theorem': { type: 'linear_prop', slope: 0.3150, ref: 0.3150 },
  'euler-critical-buckling-load-structural-columns': { type: 'linear_prop', slope: 12.8000, ref: 12.8000 },
  'torsion-shear-modulus-solid-circular-shaft': { type: 'linear_prop', slope: 0.0450, ref: 0.0450 },
  'double-shear-bolted-structural-connections': { type: 'linear_prop', slope: 0.0285, ref: 0.0285 },
  'photoelastic-stress-concentration-notched-plate': { type: 'linear_prop', slope: 0.2450, ref: 0.2450 },

  // Module 3: Geotechnical & Foundation Engineering (Labs 19–27)
  'standard-proctor-compaction-moisture-density': { type: 'linear_prop', slope: 0.0380, ref: 0.0380 },
  'direct-shear-box-soil-friction-angle': { type: 'linear_affine', slope: 0.6250, intercept: 5.0000, ref: 0.6250 },
  'constant-head-soil-permeability-darcy': { type: 'linear_prop', slope: 1.4500, ref: 1.4500 },
  'one-dimensional-consolidation-oedometer-test': { type: 'log_input', slope: -0.2850, intercept: 1.2500, ref: 0.2850, abs_ref: true },
  'unconfined-compressive-strength-cohesive-soil': { type: 'linear_prop', slope: 28.5000, ref: 28.5000 },
  'triaxial-consolidated-undrained-shear-test': { type: 'linear_affine', slope: 1.3500, intercept: 45.0000, ref: 1.3500 },
  'atterberg-limits-casagrande-liquid-limit': { type: 'log_input', slope: -14.5000, intercept: 62.0000, ref: 14.5000, abs_ref: true },
  'in-situ-field-density-sand-cone-method': { type: 'linear_prop', slope: 1.8500, ref: 1.8500 },
  'california-bearing-ratio-cbr-subgrade-soils': { type: 'linear_prop', slope: 2.4000, ref: 2.4000 },

  // Module 4: Hydraulics, Water Resources & Environmental Engineering (Labs 28–36)
  'flow-over-sharp-crested-rectangular-v-notch-weirs': { type: 'linear_prop', slope: 1.3800, ref: 1.3800 },
  'hydraulic-jump-energy-dissipation-open-channel': { type: 'linear_prop', slope: 1.0000, ref: 1.0000 },
  'manning-roughness-coefficient-open-tilting-flume': { type: 'linear_prop', slope: 66.6667, ref: 66.6667 },
  'pipe-friction-darcy-weisbach-head-loss': { type: 'square_input', slope: 0.4200, ref: 0.4200 },
  'minor-losses-pipe-expansions-valves-fittings': { type: 'linear_prop', slope: 2.4500, ref: 2.4500 },
  'jar-test-coagulation-flocculation-turbidity-removal': { type: 'linear_affine', slope: -0.8500, intercept: 48.0000, ref: 0.8500, abs_ref: true },
  'biochemical-oxygen-demand-bod5-depletion-kinetics': { type: 'linear_prop', slope: 32.5000, ref: 32.5000 },
  'total-suspended-solids-tss-gravimetric-filtration': { type: 'linear_prop', slope: 185.0000, ref: 185.0000 },
  'activated-sludge-sedimentation-sludge-volume-index': { type: 'linear_prop', slope: 95.0000, ref: 95.0000 },

  // Module 5: Transportation, Highway & Pavement Engineering (Labs 37–43)
  'los-angeles-abrasion-test-aggregate-degradation': { type: 'linear_prop', slope: 2.4500, ref: 2.4500 },
  'aggregate-impact-and-crushing-value-ten-percent-fines': { type: 'linear_prop', slope: 1.6500, ref: 1.6500 },
  'marshall-stability-and-flow-asphalt-mixtures': { type: 'linear_prop', slope: 2.8500, ref: 2.8500 },
  'bitumen-penetration-grade-test-standard-needle': { type: 'linear_affine', slope: 3.8000, intercept: -25.0000, ref: 3.8000 },
  'softening-point-bituminous-binders-ring-and-ball': { type: 'linear_affine', slope: 2.1500, intercept: -84.0000, ref: 2.1500 },
  'ductility-testing-of-bituminous-paving-materials': { type: 'linear_prop', slope: 5.0000, ref: 5.0000 },
  'pavement-skid-resistance-british-pendulum-tester': { type: 'linear_affine', slope: 1.2500, intercept: 22.0000, ref: 1.2500 },

  // Module 6: Surveying, Geomatics & Construction Dynamics (Labs 44–50)
  'total-station-electronic-distance-measurement-edm': { type: 'linear_affine', slope: 1.0000, intercept: 0.0020, ref: 1.0000 },
  'differential-leveling-two-peg-collimation-error': { type: 'linear_prop', slope: 0.00185, ref: 0.00185 },
  'closed-traverse-bowditch-compass-rule-adjustment': { type: 'linear_prop', slope: 0.00035, ref: 0.00035 },
  'free-vibration-natural-frequency-shear-frame': { type: 'inverse_input', slope: 1850.0000, ref: 1850.0000 },
  'forced-vibration-resonance-shake-table-amplification': { type: 'linear_prop', slope: 8.5000, ref: 8.5000 },
  'ultrasonic-pulse-velocity-concrete-quality-upv': { type: 'linear_prop', slope: 0.2450, ref: 0.2450 },
  'rebound-hammer-schmidt-concrete-compressive-strength': { type: 'linear_affine', slope: 0.8500, intercept: 12.0000, ref: 0.8500 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Civil Engineering experiment: ' + slug);

  if (p.type === 'linear_prop') {
    const raw = round(p.slope * inp, 4);
    return { valid: true, raw: raw, displayed: raw };
  }

  if (p.type === 'linear_affine') {
    const raw = round(p.slope * inp + (p.intercept || 0), 4);
    return { valid: true, raw: raw, displayed: raw };
  }

  if (p.type === 'square_input') {
    const raw = round(p.slope * inp * inp + (p.intercept || 0), 4);
    return { valid: true, raw: raw, displayed: raw };
  }

  if (p.type === 'log_input') {
    const raw = round(p.slope * Math.log(inp) + (p.intercept || 0), 4);
    return { valid: true, raw: raw, displayed: raw };
  }

  if (p.type === 'inverse_input') {
    const raw = round(p.slope / inp + (p.intercept || 0), 4);
    return { valid: true, raw: raw, displayed: raw };
  }

  if (p.type === 'power_input') {
    const raw = round(p.slope * (inp ** p.power) + (p.intercept || 0), 4);
    return { valid: true, raw: raw, displayed: raw };
  }

  throw Error('Unknown parameter type: ' + p.type);
}

function reading(slug, input, raw){
  const inp = Number(input);
  const r = Number(raw);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Civil Engineering experiment reading: ' + slug);

  if (p.type === 'linear_prop') {
    const x = round(inp, 4);
    const y = round(p.slope * x, 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  if (p.type === 'linear_affine') {
    const x = round(inp, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  if (p.type === 'square_input') {
    const x = round(inp * inp, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  if (p.type === 'log_input') {
    const x = round(Math.log(inp), 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  if (p.type === 'inverse_input') {
    const x = round(1.0 / inp, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  if (p.type === 'power_input') {
    const x = round(inp ** p.power, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  throw Error('Unknown parameter type: ' + p.type);
}

function fit(rows){
  if (!rows || rows.length < 3) return null;
  const n = rows.length;
  let sx = 0, sy = 0, sxx = 0, syy = 0, sxy = 0;
  for (let i = 0; i < n; i++) {
    const x = rows[i].x, y = rows[i].y;
    sx += x; sy += y;
    sxx += x * x; syy += y * y;
    sxy += x * y;
  }
  const denom = n * sxx - sx * sx;
  if (Math.abs(denom) < 1e-12) return null;
  const m = (n * sxy - sx * sy) / denom;
  const b = (sy - m * sx) / n;
  const numR = n * sxy - sx * sy;
  const denR = Math.sqrt(Math.max(0, (n * sxx - sx * sx) * (n * syy - sy * sy)));
  const r2 = denR > 1e-12 ? Math.min(1.0, (numR / denR) ** 2) : 1.0;
  let ssRes = 0;
  for (let i = 0; i < n; i++) {
    const yHat = m * rows[i].x + b;
    ssRes += (rows[i].y - yHat) ** 2;
  }
  const se = n > 2 ? Math.sqrt(ssRes / (n - 2) / (sxx - sx * sx / n)) : 0;
  return { m, b, r2, se, n };
}

function estimate(slug, fitRes){
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Civil Engineering experiment estimate: ' + slug);
  const val = (p.abs_ref || (p.ref > 0 && fitRes.m < 0)) ? Math.abs(fitRes.m) : fitRes.m;
  return {
    value: val,
    reference: p.ref,
    se: fitRes.se || 0.00001
  };
}

const api = {
  PARAMS,
  predict,
  reading,
  fit,
  estimate
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = api;
}
if (typeof root !== 'undefined') {
  root.CivilModels = api;
}

})(typeof globalThis !== 'undefined' ? globalThis : this);
