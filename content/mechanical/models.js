(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Solid Mechanics & Materials Testing (Labs 1–9)
  'tensile-test-ductile-materials-young-modulus': { type: 'linear_prop', slope: 205000.0, ref: 205000.0 },
  'shear-modulus-torsion-solid-circular-shaft': { type: 'linear_prop', slope: 80000.0, ref: 80000.0 },
  'brinell-and-vickers-hardness-testing': { type: 'linear_prop', slope: 15.0000, ref: 15.0000 },
  'charpy-and-izod-impact-toughness-testing': { type: 'linear_affine', slope: 1.2500, intercept: 75.0000, ref: 1.2500 },
  'flexural-three-point-bending-elastic-deflection': { type: 'linear_prop', slope: 0.0150, ref: 0.0150 },
  'cantilever-beam-bending-stress-distribution': { type: 'linear_prop', slope: 1.8500, ref: 1.8500 },
  'buckling-of-slender-columns-euler-formula': { type: 'linear_prop', slope: 12.5000, ref: 12.5000 },
  'thin-walled-pressure-vessel-hoop-longitudinal-stress': { type: 'linear_prop', slope: 180.0000, ref: 180.0000 },
  'fatigue-testing-rotating-bending-sn-curve': { type: 'linear_affine', slope: -0.0125, intercept: 10.5000, ref: 0.0125, abs_ref: true },

  // Module 2: Fluid Mechanics & Hydraulic Machinery (Labs 10–18)
  'bernoulli-theorem-demonstration-venturi-tube': { type: 'linear_prop', slope: 2500.0, ref: 2500.0 },
  'pipe-friction-factor-darcy-weisbach-reynolds': { type: 'linear_prop', slope: 0.2850, ref: 0.2850 },
  'discharge-coefficient-orifice-and-mouthpiece': { type: 'linear_prop', slope: 48.0000, ref: 48.0000 },
  'flow-measurement-rectangular-and-v-notch-weir': { type: 'linear_prop', slope: 1.4140, ref: 1.4140 },
  'centrifugal-pump-operating-characteristics': { type: 'linear_affine', slope: -0.2500, intercept: 32.0000, ref: 0.2500, abs_ref: true },
  'pelton-wheel-impulse-turbine-performance': { type: 'linear_prop', slope: 125.0000, ref: 125.0000 },
  'francis-reaction-turbine-efficiency-characteristics': { type: 'linear_prop', slope: 0.0850, ref: 0.0850 },
  'reynolds-number-laminar-turbulent-transition-dye': { type: 'linear_prop', slope: 25000.0, ref: 25000.0 },
  'impact-of-jet-on-flat-and-hemispherical-vanes': { type: 'linear_prop', slope: 1.8500, ref: 1.8500 },

  // Module 3: Thermodynamics & Heat Transfer (Labs 19–27)
  'thermal-conductivity-metals-fourier-linear-conduction': { type: 'linear_prop', slope: 385.0000, ref: 385.0000 },
  'radial-heat-conduction-thick-composite-cylinder': { type: 'linear_prop', slope: 45.0000, ref: 45.0000 },
  'natural-convection-heat-transfer-vertical-cylinder': { type: 'linear_prop', slope: 8.5000, ref: 8.5000 },
  'forced-convection-heat-transfer-pin-fin': { type: 'linear_affine', slope: 12.0000, intercept: 15.0000, ref: 12.0000 },
  'stefan-boltzmann-radiation-constant-verification': { type: 'linear_prop', slope: 56.7000, ref: 56.7000 },
  'parallel-and-counter-flow-concentric-tube-heat-exchanger': { type: 'linear_prop', slope: 35.0000, ref: 35.0000 },
  'vapour-compression-refrigeration-cycle-cop': { type: 'linear_prop', slope: 3.4500, ref: 3.4500 },
  'marcets-boiler-saturated-steam-pressure-temperature': { type: 'linear_affine', slope: -4250.0, intercept: 15.2000, ref: 4250.0, abs_ref: true },
  'single-cylinder-four-stroke-petrol-engine-brake-thermal-efficiency': { type: 'linear_prop', slope: 0.0450, ref: 0.0450 },

  // Module 4: Dynamics, Kinematics & Mechanical Vibrations (Labs 28–36)
  'single-degree-of-freedom-undamped-free-vibration': { type: 'linear_prop', slope: 63.2455, ref: 63.2455 },
  'viscous-damped-free-vibration-logarithmic-decrement': { type: 'linear_prop', slope: 0.0250, ref: 0.0250 },
  'forced-harmonic-vibration-amplitude-resonance': { type: 'linear_prop', slope: 0.4500, ref: 0.4500 },
  'torsional-vibration-single-rotor-shaft': { type: 'linear_prop', slope: 15.8000, ref: 15.8000 },
  'whirling-critical-speed-rotating-shaft': { type: 'linear_prop', slope: 48.0000, ref: 48.0000 },
  'static-and-dynamic-balancing-rotating-masses': { type: 'linear_prop', slope: 986.9600, ref: 986.9600 },
  'epicyclic-gear-train-velocity-ratio-torque': { type: 'linear_prop', slope: 0.2500, ref: 0.2500 },
  'cam-follower-kinematics-jump-phenomenon': { type: 'linear_prop', slope: 0.0450, ref: 0.0450 },
  'gyroscopic-precession-couple-and-torque': { type: 'linear_prop', slope: 8.5000, ref: 8.5000 },

  // Module 5: Machine Design, Tribology & Manufacturing Metrology (Labs 37–44)
  'pin-on-disc-wear-and-friction-coefficient': { type: 'linear_prop', slope: 0.3500, ref: 0.3500 },
  'journal-bearing-hydrodynamic-lubrication-sommerfeld': { type: 'linear_prop', slope: 0.8500, ref: 0.8500 },
  'belt-friction-capstan-belt-drive-slip': { type: 'linear_prop', slope: 2.5000, ref: 2.5000 },
  'disc-brake-friction-and-stopping-torque': { type: 'linear_prop', slope: 42.0000, ref: 42.0000 },
  'surface-roughness-profilometry-ra-rz-measurement': { type: 'linear_prop', slope: 28.5000, ref: 28.5000 },
  'screw-thread-pitch-micrometer-and-three-wire-method': { type: 'linear_affine', slope: 1.0000, intercept: 2.1650, ref: 1.0000 },
  'sine-bar-precision-angle-measurement-slip-gauges': { type: 'linear_prop', slope: 0.0050, ref: 0.0050 },
  'metal-cutting-chip-formation-orthogonal-cutting-dynamometer': { type: 'linear_prop', slope: 450.0000, ref: 450.0000 },

  // Module 6: Mechatronics, Control Systems & Industrial HVAC (Labs 45–51)
  'pneumatic-actuator-flow-rate-and-cylinder-thrust': { type: 'linear_prop', slope: 1963.5000, ref: 1963.5000 },
  'hydraulic-linear-actuator-load-velocity-characteristics': { type: 'linear_prop', slope: 15.0000, ref: 15.0000 },
  'pid-temperature-controller-tuning-process-oven': { type: 'linear_prop', slope: 85.0000, ref: 85.0000 },
  'strain-gauge-rosette-principal-stress-analysis': { type: 'linear_prop', slope: 0.4500, ref: 0.4500 },
  'cooling-tower-evaporative-cooling-range-approach': { type: 'linear_prop', slope: 42.0000, ref: 42.0000 },
  'air-conditioning-psychrometric-sensible-latent-cooling': { type: 'linear_prop', slope: 0.6500, ref: 0.6500 },
  'solar-thermal-flat-plate-collector-efficiency-hottel-whillier': { type: 'linear_affine', slope: -450.0000, intercept: 72.0000, ref: 450.0000, abs_ref: true }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Mechanical Engineering experiment: ' + slug);

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
  root.MechanicalModels = api;
}
})(typeof window !== 'undefined' ? window : globalThis);
