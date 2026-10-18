(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Fluid Mechanics & Transport Phenomena in Process Systems (Labs 1–8)
  'venturi-meter-bernoulli-discharge-coefficient': { type: 'linear_prop', slope: 0.4850, ref: 0.4850 },
  'orifice-meter-flow-metering-pressure-loss': { type: 'linear_prop', slope: 0.6120, ref: 0.6120 },
  'pipe-friction-factor-reynolds-moody-chart': { type: 'square_input', slope: 0.2850, ref: 0.2850 },
  'fluidized-bed-minimum-fluidization-ergun': { type: 'linear_prop', slope: 0.4250, ref: 0.4250 },
  'packed-bed-pressure-drop-kozeny-carman': { type: 'linear_prop', slope: 1.6500, ref: 1.6500 },
  'centrifugal-slurry-pump-characteristic-curves': { type: 'square_input', slope: -0.0280, intercept: 35.0000, ref: 0.0280, abs_ref: true },
  'falling-film-viscometer-non-newtonian-power-law': { type: 'log_input', slope: 1.3500, intercept: -0.4500, ref: 1.3500 },
  'rotameter-calibration-variable-area-flowmeter': { type: 'linear_affine', slope: 6.5000, intercept: 5.0000, ref: 6.5000 },

  // Module 2: Heat Transfer & Thermal Unit Operations (Labs 9–16)
  'shell-and-tube-heat-exchanger-lmtd-effectiveness': { type: 'power_input', power: 0.8, slope: 85.0000, ref: 85.0000 },
  'concentric-pipe-heat-exchanger-countercurrent': { type: 'linear_prop', slope: 0.4200, ref: 0.4200 },
  'plate-and-frame-heat-exchanger-thermal-efficiency': { type: 'power_input', power: 0.65, slope: 3200.0000, ref: 3200.0000 },
  'natural-and-forced-convection-finned-tube': { type: 'power_input', power: 0.6, slope: 18.5000, ref: 18.5000 },
  'thermal-conductivity-radial-steady-state-fourier': { type: 'linear_prop', slope: 0.3850, ref: 0.3850 },
  'unsteady-state-transient-heat-conduction-lumped': { type: 'log_decay', rate: 0.0320, ref: 0.0320, abs_ref: true },
  'boiling-heat-transfer-nukiyama-curve': { type: 'linear_prop', slope: 2.4500, ref: 2.4500 },
  'tubular-falling-film-evaporator-steam-economy': { type: 'linear_prop', slope: 4.8000, ref: 4.8000 },

  // Module 3: Mass Transfer, Distillation & Separation Processes (Labs 17–24)
  'fractional-distillation-mccabe-thiele-reflux': { type: 'linear_affine', slope: 2.8500, intercept: 1.2500, ref: 2.8500 },
  'gas-absorption-packed-column-mass-transfer-kga': { type: 'power_input', power: 0.7, slope: 0.0820, ref: 0.0820 },
  'liquid-liquid-extraction-ternary-tie-lines': { type: 'linear_prop', slope: 0.8850, ref: 0.8850 },
  'batch-rotary-drum-vacuum-filtration-cake-resistance': { type: 'linear_affine', slope: 18.5000, intercept: 4.2000, ref: 18.5000 },
  'solid-liquid-leaching-crosscurrent-stage-efficiency': { type: 'linear_affine', slope: -0.4200, intercept: -0.1500, ref: 0.4200, abs_ref: true },
  'adsorption-isotherm-activated-carbon-langmuir-freundlich': { type: 'linear_affine', slope: 0.4500, intercept: 0.2200, ref: 0.4500 },
  'crossflow-membrane-ultrafiltration-gel-polarization': { type: 'linear_prop', slope: 42.5000, ref: 42.5000 },
  'tray-dryer-drying-rate-curve-constant-falling-rate': { type: 'power_input', power: 0.8, slope: 0.6500, ref: 0.6500 },

  // Module 4: Chemical Reaction Engineering, Catalysis & Bioreactors (Labs 25–32)
  'continuous-stirred-tank-reactor-cstr-saponification': { type: 'linear_prop', slope: 0.2800, ref: 0.2800 },
  'plug-flow-tubular-reactor-pfr-residence-time': { type: 'linear_prop', slope: 0.1850, ref: 0.1850 },
  'reactors-in-series-cstr-cascade-conversion': { type: 'linear_affine', slope: 0.0450, intercept: 1.0000, ref: 0.0450 },
  'residence-time-distribution-rtd-axial-dispersion': { type: 'linear_prop', slope: 0.0025, ref: 0.0025 },
  'heterogeneous-catalytic-fixed-bed-thiele-modulus': { type: 'linear_affine', slope: 0.3500, intercept: 1.0000, ref: 0.3500 },
  'batch-isothermal-reactor-rate-constant-arrhenius': { type: 'arrhenius_inv_t', slope: -5.7740, intercept: 21.1300, ref: 5.7740, abs_ref: true },
  'aerated-bioreactor-oxygen-mass-transfer-kla': { type: 'power_input', power: 1.2, slope: 0.0240, ref: 0.0240 },
  'enzyme-membrane-reactor-continuous-biocatalysis': { type: 'inverse_input', slope: 1.4500, intercept: 0.4500, ref: 1.4500 },

  // Module 5: Chemical Thermodynamics, Phase Equilibria & Solution Properties (Labs 33–39)
  'vapor-liquid-equilibrium-vle-wilson-margules': { type: 'linear_prop', slope: 0.7250, ref: 0.7250 },
  'differential-scanning-calorimetry-dsc-glass-transition': { type: 'log_input', slope: 2.1500, intercept: 100.0000, ref: 2.1500 },
  'bomb-calorimeter-heat-of-combustion-hydrocarbons': { type: 'linear_prop', slope: 2.6500, ref: 2.6500 },
  'partial-molar-volume-binary-solution-dilatometry': { type: 'linear_affine', slope: 14.5000, intercept: 54.2000, ref: 14.5000 },
  'solid-liquid-equilibrium-sle-eutectic-phase-diagram': { type: 'linear_prop', slope: 58.5000, ref: 58.5000 },
  'excess-enthalpy-of-mixing-isothermal-titration-calorimetry': { type: 'linear_prop', slope: -3450.0000, ref: 3450.0000, abs_ref: true },
  'gas-solubility-henry-law-pressure-decay': { type: 'linear_prop', slope: 0.0340, ref: 0.0340 },

  // Module 6: Process Dynamics, Automatic Control & Mechanical Separations (Labs 40–46)
  'first-order-gravity-drained-tank-level-dynamics': { type: 'linear_prop', slope: 3.8500, ref: 3.8500 },
  'two-tank-interacting-liquid-level-system': { type: 'linear_prop', slope: 4.2500, ref: 4.2500 },
  'feedback-pid-temperature-control-tuning-ziegler-nichols': { type: 'linear_prop', slope: 0.1250, ref: 0.1250 },
  'pneumatic-control-valve-flow-characteristic-hysteresis': { type: 'linear_prop', slope: 0.8500, ref: 0.8500 },
  'feedforward-plus-feedback-ratio-flow-control': { type: 'linear_prop', slope: 0.4000, ref: 0.4000 },
  'continuous-crystallization-msmpr-crystal-size-distribution': { type: 'linear_affine', slope: -0.0125, intercept: 15.2000, ref: 0.0125, abs_ref: true },
  'sedimentation-and-centrifugal-clarification-stokes': { type: 'linear_affine', slope: -1.8500, intercept: 120.0000, ref: 1.8500, abs_ref: true }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Chemical Engineering experiment predict: ' + slug);

  if (p.type === 'linear_prop') {
    const x = round(inp, 4);
    const y = round(p.slope * x, 4);
    return { input: inp, raw: y, x: x, y: y };
  }

  if (p.type === 'linear_affine') {
    const x = round(inp, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: y, x: x, y: y };
  }

  if (p.type === 'square_input') {
    const x = round(inp * inp, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: y, x: x, y: y };
  }

  if (p.type === 'log_input') {
    const x = round(Math.log(inp), 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: y, x: x, y: y };
  }

  if (p.type === 'log_decay') {
    const x = round(inp, 4);
    const raw = round(Math.exp(-p.rate * x), 5);
    const y = round(-p.rate * x, 4);
    return { input: inp, raw: raw, x: x, y: y };
  }

  if (p.type === 'inverse_input') {
    const x = round(1.0 / inp, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: y, x: x, y: y };
  }

  if (p.type === 'arrhenius_inv_t') {
    const absT = inp + 273.15;
    const x = round(1000.0 / absT, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: y, x: x, y: y };
  }

  if (p.type === 'power_input') {
    const x = round(inp ** p.power, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: y, x: x, y: y };
  }

  throw Error('Unknown parameter type: ' + p.type);
}

function reading(slug, input, raw){
  const inp = Number(input);
  const r = Number(raw);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Chemical Engineering experiment reading: ' + slug);

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

  if (p.type === 'log_decay') {
    const x = round(inp, 4);
    const y = round(-p.rate * x, 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  if (p.type === 'inverse_input') {
    const x = round(1.0 / inp, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  if (p.type === 'arrhenius_inv_t') {
    const absT = inp + 273.15;
    const x = round(1000.0 / absT, 4);
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
  if (!p) throw Error('Unknown Chemical Engineering experiment estimate: ' + slug);
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
  root.ChemEngModels = api;
}

})(typeof globalThis !== 'undefined' ? globalThis : this);
