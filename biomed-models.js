(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Bioinstrumentation, Biopotential Electrodes & Medical Sensors (Labs 1–8)
  'thermistor-wheatstone-bridge-clinical-thermometer': { type: 'linear_affine', slope: 18.5000, intercept: -647.5000, ref: 18.5000 },
  'strain-gauge-cantilever-medical-force-sensor': { type: 'linear_prop', slope: 2.4500, ref: 2.4500 },
  'piezoelectric-pulse-transducer-arterial-compliance': { type: 'linear_prop', slope: 14.2000, ref: 14.2000 },
  'ag-agcl-biopotential-electrode-half-cell-impedance': { type: 'log_input', slope: -4.2000, intercept: 38.5000, ref: 4.2000, abs_ref: true },
  'instrumentation-amplifier-cmrr-ecg-front-end': { type: 'linear_prop', slope: 0.0480, ref: 0.0480 },
  'clark-oxygen-polarographic-electrode-blood-po2': { type: 'linear_prop', slope: 1.6500, ref: 1.6500 },
  'linear-variable-differential-transformer-displacement': { type: 'linear_prop', slope: 0.8500, ref: 0.8500 },
  'hall-effect-blood-flowmeter-electromagnetic-probe': { type: 'linear_prop', slope: 0.3600, ref: 0.3600 },

  // Module 2: Biosignal Processing, Bioelectric Phenomena & Physiological Telemetry (Labs 9–17)
  'ecg-einthoven-limb-leads-cardiac-axis': { type: 'linear_affine', slope: 1.2500, intercept: 0.1500, ref: 1.2500 },
  'photoplethysmography-ppg-pulse-oximeter-beer-lambert': { type: 'linear_affine', slope: -25.0000, intercept: 110.0000, ref: 25.0000, abs_ref: true },
  'surface-electromyography-semg-muscle-fatigue-frequency': { type: 'linear_affine', slope: -0.6500, intercept: 95.0000, ref: 0.6500, abs_ref: true },
  'electroencephalography-eeg-alpha-attenuation-power': { type: 'linear_affine', slope: -0.1250, intercept: 52.0000, ref: 0.1250, abs_ref: true },
  'galvanic-skin-response-gsr-electrodermal-activity': { type: 'linear_prop', slope: 1.8500, ref: 1.8500 },
  'amperometric-glucose-biosensor-michaelis-menten': { type: 'linear_prop', slope: 0.7200, ref: 0.7200 },
  'surface-plasmon-resonance-immunosensor-antibody-binding': { type: 'linear_prop', slope: 8.4000, ref: 8.4000 },
  'impedance-pneumography-respiratory-tidal-volume': { type: 'linear_prop', slope: 1.3500, ref: 1.3500 },
  'digital-notch-filter-60hz-powerline-interference': { type: 'linear_prop', slope: 0.0050, ref: 0.0050 },

  // Module 3: Biomechanics, Biomaterials & Orthopaedic Implants (Labs 18–26)
  'cortical-bone-tensile-elastic-modulus': { type: 'linear_prop', slope: 17.5000, ref: 17.5000 },
  'articular-cartilage-confined-compression-creep': { type: 'linear_prop', slope: 0.6500, ref: 0.6500 },
  'titanium-alloy-orthopaedic-implant-four-point-bending': { type: 'linear_prop', slope: 0.0042, ref: 0.0042 },
  'uhmwpe-artificial-joint-pin-on-disk-wear': { type: 'linear_prop', slope: 2.1500, ref: 2.1500 },
  'hydrogel-scaffold-swelling-degradation-kinetics': { type: 'linear_affine', slope: -3.2000, intercept: 98.0000, ref: 3.2000, abs_ref: true },
  'skeletal-muscle-isometric-length-tension-curve': { type: 'linear_prop', slope: 4.8000, ref: 4.8000 },
  'ligament-viscoelastic-stress-relaxation-fung': { type: 'log_input', slope: -0.0450, intercept: 0.9800, ref: 0.0450, abs_ref: true },
  'gait-analysis-force-plate-ground-reaction-forces': { type: 'linear_affine', slope: 0.2800, intercept: 0.8200, ref: 0.2800 },
  'prosthetic-socket-interface-pressure-mapping': { type: 'linear_prop', slope: 0.2200, ref: 0.2200 },

  // Module 4: Cardiovascular Fluid Dynamics, Hemodynamics & Artificial Organs (Labs 27–34)
  'blood-viscosity-cone-and-plate-rheometer-casson': { type: 'sqrt_casson', slope: 0.0620, intercept: 0.1800, ref: 0.0620 },
  'hagen-poiseuille-microvascular-flow-resistance': { type: 'linear_prop', slope: 3.6000, ref: 3.6000 },
  'windkessel-lumped-parameter-arterial-compliance': { type: 'log_decay', rate: 0.00125, ref: 0.00125, abs_ref: true },
  'mechanical-heart-valve-steady-flow-pressure-drop': { type: 'square_input', slope: 3.8500, ref: 3.8500 },
  'pulse-wave-velocity-arterial-stiffness-moens-korteweg': { type: 'linear_affine', slope: 0.0450, intercept: 2.8000, ref: 0.0450 },
  'hollow-fiber-hemodialyzer-clearance-mass-transfer': { type: 'linear_affine', slope: 0.5800, intercept: 42.0000, ref: 0.5800 },
  'centrifugal-rotary-blood-pump-hemolysis-shear-stress': { type: 'square_input', slope: 7.5000, ref: 7.5000 },
  'fahraeus-lindqvist-tube-hematocrit-reduction': { type: 'linear_affine', slope: 0.0125, intercept: 1.2500, ref: 0.0125 },

  // Module 5: Medical Imaging Systems, Bio-optics, Bio-MEMS & Rehabilitation (Labs 35–42)
  'ultrasound-transducer-acoustic-beam-profiling': { type: 'linear_prop', slope: 1.8500, ref: 1.8500 },
  'x-ray-narrow-beam-linear-attenuation-hvl': { type: 'log_decay', rate: 0.2450, ref: 0.2450, abs_ref: true },
  'doppler-ultrasound-flowmeter-frequency-shift': { type: 'linear_prop', slope: 28.5000, ref: 28.5000 },
  'mri-spin-lattice-relaxation-t1-inversion-recovery': { type: 'linear_affine', slope: 0.00145, intercept: -0.9500, ref: 0.00145 },
  'cardiac-pacemaker-pulse-generator-chronaxie-strength-duration': { type: 'inverse_input', slope: 0.3200, intercept: 0.6500, ref: 0.3200 },
  'external-defibrillator-rlc-damped-sinusoidal-pulse': { type: 'linear_affine', slope: -0.3500, intercept: 68.0000, ref: 0.3500, abs_ref: true },
  'biphasic-functional-electrical-stimulator-charge-balance': { type: 'linear_prop', slope: 0.2500, ref: 0.2500 },
  'hearing-aid-electroacoustic-frequency-response-gain': { type: 'linear_affine', slope: 0.9500, intercept: 28.5000, ref: 0.9500 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Biomedical experiment predict: ' + slug);

  if (p.type === 'linear_prop') {
    const x = inp;
    const y = p.slope * x;
    return { valid: true, raw: round(y, 4), x: round(x, 4), y: round(y, 4) };
  }

  if (p.type === 'linear_affine') {
    const x = inp;
    const y = p.slope * x + (p.intercept || 0);
    return { valid: true, raw: round(y, 4), x: round(x, 4), y: round(y, 4) };
  }

  if (p.type === 'log_input') {
    const x = Math.log(inp);
    const y = p.slope * x + (p.intercept || 0);
    return { valid: true, raw: round(y, 4), x: round(x, 4), y: round(y, 4) };
  }

  if (p.type === 'log_decay') {
    const x = inp;
    const raw = Math.exp(-p.rate * x);
    const y = -p.rate * x;
    return { valid: true, raw: round(raw, 5), x: round(x, 4), y: round(y, 4) };
  }

  if (p.type === 'square_input') {
    const x = inp * inp;
    const y = p.slope * x + (p.intercept || 0);
    return { valid: true, raw: round(y, 4), x: round(x, 4), y: round(y, 4) };
  }

  if (p.type === 'inverse_input') {
    const x = 1.0 / inp;
    const y = p.slope * x + (p.intercept || 0);
    return { valid: true, raw: round(y, 4), x: round(x, 4), y: round(y, 4) };
  }

  if (p.type === 'sqrt_casson') {
    const x = Math.sqrt(inp);
    const y = p.slope * x + (p.intercept || 0);
    const raw = y * y;
    return { valid: true, raw: round(raw, 4), x: round(x, 4), y: round(y, 4) };
  }

  throw Error('Unknown parameter type: ' + p.type);
}

function reading(slug, input, raw){
  const inp = Number(input);
  const r = Number(raw);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Biomedical experiment reading: ' + slug);

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

  if (p.type === 'square_input') {
    const x = round(inp * inp, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  if (p.type === 'inverse_input') {
    const x = round(1.0 / inp, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  if (p.type === 'sqrt_casson') {
    const x = round(Math.sqrt(inp), 4);
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
  if (!p) throw Error('Unknown Biomedical experiment estimate: ' + slug);
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
  root.BiomedModels = api;
}

})(typeof globalThis !== 'undefined' ? globalThis : this);
