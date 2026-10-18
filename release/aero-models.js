(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Subsonic Aerodynamics & Wind Tunnel Testing (Labs 1–10)
  'wind-tunnel-calibration-dynamic-pressure': { type: 'linear_prop', slope: 0.6125, ref: 0.6125 },
  'symmetric-airfoil-pressure-distribution-naca0012': { type: 'linear_prop', slope: 0.1097, ref: 0.1097 },
  'cambered-airfoil-pitching-moment-naca4412': { type: 'linear_affine', slope: 0.1080, intercept: 0.4320, ref: 0.1080 },
  'direct-force-balance-aerodynamic-polars': { type: 'linear_affine', slope: 0.0450, intercept: 0.0180, ref: 0.0450 },
  'boundary-layer-velocity-profile-flat-plate': { type: 'linear_prop', slope: 4.2500, ref: 4.2500 },
  'wake-survey-momentum-deficit-profile-drag': { type: 'linear_prop', slope: 0.0240, ref: 0.0240 },
  'finite-wing-aspect-ratio-induced-drag': { type: 'linear_prop', slope: 0.1348, ref: 0.1348 },
  'high-lift-trailing-edge-flap-deflection': { type: 'linear_prop', slope: 0.0580, ref: 0.0580 },
  'boundary-layer-flow-separation-smoke-visualization': { type: 'linear_prop', slope: 0.0650, ref: 0.0650 },
  'circular-cylinder-crossflow-vortex-shedding': { type: 'linear_prop', slope: 0.2050, ref: 0.2050 },

  // Module 2: Compressible Aerodynamics & High-Speed Gas Dynamics (Labs 11–18)
  'converging-diverging-nozzle-mach-area-relation': { type: 'linear_prop', slope: 0.8500, ref: 0.8500 },
  'normal-shock-wave-jump-conditions': { type: 'linear_prop', slope: 1.1667, ref: 1.1667 },
  'oblique-shock-theta-beta-mach-relation': { type: 'linear_prop', slope: 1.2500, ref: 1.2500 },
  'prandtl-meyer-supersonic-expansion-fan': { type: 'linear_prop', slope: 0.0520, ref: 0.0520 },
  'supersonic-wind-tunnel-schlieren-optical-imaging': { type: 'linear_prop', slope: 5.0000, ref: 5.0000 },
  'subsonic-compressibility-prandtl-glauert-rule': { type: 'linear_prop', slope: 0.6500, ref: 0.6500 },
  'transonic-critical-mach-number-drag-divergence': { type: 'linear_prop', slope: 25.0000, ref: 25.0000 },
  'shock-tube-wave-propagation-incident-mach': { type: 'linear_prop', slope: 1.8500, ref: 1.8500 },

  // Module 3: Aircraft Flight Mechanics, Stability & Control (Labs 19–26)
  'standard-atmosphere-airspeed-calibration': { type: 'linear_prop', slope: 70.0000, ref: 70.0000 },
  'steady-level-flight-power-required-curves': { type: 'linear_prop', slope: 0.4500, ref: 0.4500 },
  'aircraft-rate-of-climb-flight-envelope': { type: 'linear_prop', slope: 1.0000, ref: 1.0000 },
  'longitudinal-static-stability-neutral-point': { type: 'linear_affine', slope: 1.0000, intercept: -0.3600, ref: 1.0000 },
  'elevator-control-power-stick-free-trim': { type: 'linear_prop', slope: 8.5000, ref: 8.5000 },
  'lateral-directional-weathercock-dihedral-effect': { type: 'linear_prop', slope: 1.8000, ref: 1.8000 },
  'longitudinal-dynamic-modes-phugoid-short-period': { type: 'linear_prop', slope: 0.0721, ref: 0.0721 },
  'lateral-directional-dynamic-modes-dutch-roll-spiral': { type: 'linear_prop', slope: 4.5000, ref: 4.5000 },

  // Module 4: Aerospace Propulsion & Rocket Dynamics (Labs 27–34)
  'propeller-momentum-blade-element-thrust-efficiency': { type: 'linear_prop', slope: 0.1350, ref: 0.1350 },
  'gas-turbine-joule-brayton-thermodynamic-cycle': { type: 'linear_prop', slope: 345.0000, ref: 345.0000 },
  'turbofan-bypass-ratio-propulsive-efficiency': { type: 'linear_prop', slope: 0.8500, ref: 0.8500 },
  'axial-compressor-cascade-diffusion-stall-margin': { type: 'linear_prop', slope: 0.0165, ref: 0.0165 },
  'ramjet-supersonic-inlet-rayleigh-heating': { type: 'linear_prop', slope: 0.1800, ref: 0.1800 },
  'solid-rocket-motor-grain-geometry-ballistics': { type: 'log_power', alpha: 0.3500, lnC: 1.2000, ref: 0.3500 },
  'liquid-rocket-thrust-chamber-characteristic-velocity': { type: 'linear_prop', slope: 700.0000, ref: 700.0000 },
  'rocket-nozzle-altitude-compensation-flow-separation': { type: 'linear_prop', slope: 1.4500, ref: 1.4500 },

  // Module 5: Aerospace Structures, Aeroelasticity & Space Flight (Labs 35–42)
  'unsymmetrical-bending-aircraft-wing-spars': { type: 'linear_prop', slope: 1.8500, ref: 1.8500 },
  'shear-center-determination-thin-walled-open-sections': { type: 'linear_affine', slope: 0.2400, intercept: 4.4400, ref: 0.2400 },
  'torsion-shear-flow-multi-cell-wing-boxes': { type: 'linear_prop', slope: 1.1765, ref: 1.1765 },
  'euler-buckling-southwell-plot-aircraft-struts': { type: 'linear_prop', slope: 0.0800, ref: 0.0800 },
  'aeroelastic-torsional-divergence-wing-rigidity': { type: 'linear_prop', slope: 0.3125, ref: 0.3125 },
  'classical-two-degree-of-freedom-airfoil-flutter': { type: 'linear_prop', slope: 0.0450, ref: 0.0450 },
  'keplerian-two-body-orbit-determination': { type: 'linear_prop', slope: 7.9720, ref: 7.9720 },
  'hohmann-transfer-interplanetary-orbital-maneuvers': { type: 'linear_prop', slope: 7.7800, ref: 7.7800 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Aerospace experiment predict: ' + slug);

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
  if (!p) throw Error('Unknown Aerospace experiment reading: ' + slug);

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
  if (!p) throw Error('Unknown Aerospace experiment estimate: ' + slug);
  const targetSlope = p.ref;
  return {
    value: fitRes.m,
    reference: targetSlope,
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
  root.AeroModels = api;
}

})(typeof globalThis !== 'undefined' ? globalThis : this);
