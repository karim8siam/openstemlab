(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Farm Machinery & Tractor Power Mechanics (Labs 1–10)
  'tractor-drawbar-pull-tractive-efficiency': { type: 'linear_affine', slope: 2.4000, intercept: 0.0800, ref: 2.4000 },
  'moldboard-plow-draft-specific-resistance': { type: 'linear_prop', slope: 48.5000, ref: 48.5000 },
  'disc-plow-side-draft-penetration': { type: 'linear_prop', slope: 0.3200, ref: 0.3200 },
  'rotary-tiller-rotor-torque-specific-energy': { type: 'linear_prop', slope: 18.2000, ref: 18.2000 },
  'fluted-roller-seed-drill-metering-calibration': { type: 'linear_prop', slope: 8.5000, ref: 8.5000 },
  'precision-planter-seed-spacing-uniformity': { type: 'linear_affine', slope: 0.4500, intercept: 0.5000, ref: 0.4500 },
  'hydraulic-spray-nozzle-droplet-distribution': { type: 'linear_prop', slope: 0.8500, ref: 0.8500 },
  'reciprocating-cutterbar-knife-velocity-ratio': { type: 'linear_prop', slope: 1.3500, ref: 1.3500 },
  'axial-flow-threshing-cylinder-grain-separation': { type: 'linear_affine', slope: 1.1500, intercept: 60.0000, ref: 1.1500 },
  'combine-cleaning-shoe-aerodynamic-chaff-separation': { type: 'linear_prop', slope: 14.5000, ref: 14.5000 },

  // Module 2: Soil, Water & Irrigation Engineering (Labs 11–19)
  'double-ring-infiltrometer-kostiakov-infiltration': { type: 'log_power', alpha: 0.6500, lnC: 1.2500, ref: 0.6500 },
  'constant-head-soil-hydraulic-conductivity': { type: 'linear_prop', slope: 0.1800, ref: 0.1800 },
  'soil-moisture-retention-pf-curve': { type: 'linear_affine', slope: -0.0650, intercept: 0.4800, ref: 0.0650, abs_ref: true },
  'parshall-flume-open-channel-flow-measurement': { type: 'linear_affine', slope: 1.5500, intercept: 0.3800, ref: 1.5500 },
  'v-notch-sharp-crested-weir-discharge': { type: 'linear_prop', slope: 1.3800, ref: 1.3800 },
  'centrifugal-irrigation-pump-characteristic-curves': { type: 'linear_prop', slope: 8.2000, ref: 8.2000 },
  'drip-irrigation-emitter-discharge-uniformity': { type: 'linear_affine', slope: 0.5000, intercept: -0.7500, ref: 0.5000 },
  'agricultural-sprinkler-christiansen-uniformity': { type: 'linear_affine', slope: 0.0550, intercept: 64.0000, ref: 0.0550 },
  'rainfall-simulator-runoff-soil-loss-usle': { type: 'linear_prop', slope: 12.5000, ref: 12.5000 },

  // Module 3: Post-Harvest Processing & Crop Value Addition (Labs 20–28)
  'grain-moisture-content-oven-drying-method': { type: 'linear_prop', slope: 6.2500, ref: 6.2500 },
  'equilibrium-moisture-content-sorption-isotherms': { type: 'linear_affine', slope: 0.5200, intercept: 2.1000, ref: 0.5200 },
  'thin-layer-grain-drying-kinetics-page-model': { type: 'linear_affine', slope: 1.2500, intercept: -4.5000, ref: 1.2500 },
  'air-grain-psychrometrics-drying-potential': { type: 'linear_affine', slope: 0.4200, intercept: -5.0000, ref: 0.4200 },
  'aerodynamic-terminal-velocity-pneumatic-separation': { type: 'linear_prop', slope: 1.7500, ref: 1.7500 },
  'physical-gravimetric-properties-agricultural-grains': { type: 'linear_prop', slope: 0.7850, ref: 0.7850 },
  'grain-internal-friction-angle-of-repose': { type: 'linear_prop', slope: 0.5774, ref: 0.5774 },
  'hammer-mill-size-reduction-rittinger-bond-laws': { type: 'linear_prop', slope: 4.8000, ref: 4.8000 },
  'paddy-rubber-roll-husking-head-rice-yield': { type: 'linear_affine', slope: 12.5000, intercept: 42.0000, ref: 12.5000 },

  // Module 4: Agricultural Structures & Environmental Control (Labs 29–35)
  'janssen-deep-bin-grain-pressure-distribution': { type: 'linear_prop', slope: 2.4500, ref: 2.4500 },
  'greenhouse-thermal-heat-loss-overall-u-factor': { type: 'linear_prop', slope: 5.8000, ref: 5.8000 },
  'evaporative-cooling-pad-saturation-efficiency': { type: 'linear_prop', slope: 8.5000, ref: 8.5000 },
  'fruit-vegetable-respiration-heat-rate-cold-storage': { type: 'linear_affine', slope: 1.4500, intercept: 3.2000, ref: 1.4500 },
  'livestock-housing-sensible-heat-balance-ventilation': { type: 'linear_prop', slope: 0.0012, ref: 0.0012 },
  'agricultural-timber-roof-truss-load-deflection': { type: 'linear_prop', slope: 1.8500, ref: 1.8500 },
  'anaerobic-digester-biogas-yield-methane-kinetics': { type: 'linear_prop', slope: 0.4200, ref: 0.4200 },

  // Module 5: Terramechanics, Precision Agriculture & Renewable Farm Energy (Labs 36–42)
  'cone-penetrometer-soil-strength-hardpan-profiling': { type: 'linear_prop', slope: 18.5000, ref: 18.5000 },
  'bekker-theory-off-road-terramechanics-rigid-wheel-sinkage': { type: 'log_power', alpha: 0.8500, lnC: 2.1000, ref: 0.8500 },
  'flat-plate-solar-air-collector-thermal-efficiency': { type: 'linear_affine', slope: -6.2000, intercept: 0.6800, ref: 6.2000, abs_ref: true },
  'downdraft-biomass-gasifier-cold-gas-efficiency': { type: 'linear_affine', slope: -12.5000, intercept: 8.8000, ref: 12.5000, abs_ref: true },
  'vegetable-oil-biodiesel-transesterification-yield': { type: 'linear_affine', slope: 5.2000, intercept: 51.0000, ref: 5.2000 },
  'solar-pv-submersible-water-pump-hydraulic-performance': { type: 'linear_prop', slope: 0.6800, ref: 0.6800 },
  'variable-rate-precision-fertilizer-fluted-roller-kinetics': { type: 'linear_prop', slope: 0.1650, ref: 0.1650 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Agricultural experiment predict: ' + slug);

  if (p.type === 'log_power') {
    const x = Math.log(inp);
    const y = p.alpha * x + p.lnC;
    const raw = Math.exp(y);
    return { valid: true, raw: round(raw, 5), x: round(x, 4), y: round(y, 4) };
  }

  if (p.type === 'linear_affine') {
    const x = inp;
    const y = p.slope * x + (p.intercept || 0);
    return { valid: true, raw: round(y, 4), x: round(x, 4), y: round(y, 4) };
  }

  if (p.type === 'linear_prop') {
    const x = inp;
    const y = p.slope * x;
    return { valid: true, raw: round(y, 4), x: round(x, 4), y: round(y, 4) };
  }

  throw Error('Unknown parameter type: ' + p.type);
}

function reading(slug, input, raw){
  const inp = Number(input);
  const r = Number(raw);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Agricultural experiment reading: ' + slug);

  if (p.type === 'log_power') {
    const x = round(Math.log(inp), 4);
    const y = round(p.alpha * x + p.lnC, 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  if (p.type === 'linear_affine') {
    const x = round(inp, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  if (p.type === 'linear_prop') {
    const x = round(inp, 4);
    const y = round(p.slope * x, 4);
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
  if (!p) throw Error('Unknown Agricultural experiment estimate: ' + slug);
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
  root.AgriModels = api;
}

})(typeof globalThis !== 'undefined' ? globalThis : this);
