(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: DC/AC Circuit Analysis & Network Theorems (Labs 1–9)
  'thevenin-and-norton-equivalent-circuits': { type: 'linear_affine', slope: -50.0000, intercept: 12.0000, ref: 50.0000, abs_ref: true },
  'superposition-theorem-independent-sources': { type: 'linear_affine', slope: 0.4500, intercept: 1.2500, ref: 0.4500 },
  'maximum-power-transfer-theorem-dc-circuits': { type: 'linear_affine', slope: -25.0000, intercept: 15.0000, ref: 25.0000, abs_ref: true },
  'transient-response-series-rl-and-rc-circuits': { type: 'linear_prop', slope: 0.5000, ref: 0.5000 },
  'series-and-parallel-rlc-resonance': { type: 'linear_prop', slope: 6.2832, ref: 6.2832 },
  'reciprocity-and-millman-theorems': { type: 'linear_prop', slope: 0.6500, ref: 0.6500 },
  'two-port-network-z-and-y-parameters': { type: 'linear_prop', slope: 0.4500, ref: 0.4500 },
  'ac-power-factor-improvement-synchronous-condenser': { type: 'linear_prop', slope: 15.2000, ref: 15.2000 },
  'three-phase-power-measurement-two-wattmeter': { type: 'linear_prop', slope: 1.4500, ref: 1.4500 },

  // Module 2: Analog Electronics & Semiconductor Devices (Labs 10–18)
  'pn-junction-diode-forward-reverse-characteristics': { type: 'linear_affine', slope: 38.6000, intercept: -24.5000, ref: 38.6000 },
  'zener-diode-voltage-regulator-line-load-regulation': { type: 'linear_affine', slope: 0.0250, intercept: 5.1000, ref: 0.0250 },
  'bjt-common-emitter-input-output-characteristics': { type: 'linear_prop', slope: 120.0000, ref: 120.0000 },
  'jfet-and-mosfet-drain-and-transfer-characteristics': { type: 'linear_affine', slope: 0.6500, intercept: 2.6000, ref: 0.6500 },
  'op-amp-inverting-and-non-inverting-closed-loop-gain': { type: 'linear_prop', slope: -4.7000, ref: 4.7000, abs_ref: true },
  'op-amp-active-filters-butterworth-sallen-key': { type: 'linear_affine', slope: -40.0000, intercept: 0.0000, ref: 40.0000, abs_ref: true },
  'bjt-rc-coupled-audio-amplifier-frequency-response': { type: 'linear_prop', slope: 0.0850, ref: 0.0850 },
  'wien-bridge-and-rc-phase-shift-oscillators': { type: 'linear_prop', slope: 0.6283, ref: 0.6283 },
  'astable-and-monostable-multivibrators-555-timer': { type: 'linear_prop', slope: 11.0000, ref: 11.0000 },

  // Module 3: Digital Electronics, Logic Design & Microprocessors (Labs 19–27)
  'truth-tables-and-de-morgans-laws-logic-gates': { type: 'linear_affine', slope: 0.8500, intercept: 3.2000, ref: 0.8500 },
  'combinational-adders-and-subtractors-arithmetic-logic': { type: 'linear_affine', slope: 1.2500, intercept: 4.5000, ref: 1.2500 },
  'multiplexers-demultiplexers-and-data-routing': { type: 'linear_affine', slope: 0.9500, intercept: 5.2000, ref: 0.9500 },
  'synchronous-and-asynchronous-binary-counters': { type: 'linear_prop', slope: 3.6500, ref: 3.6500 },
  'digital-flip-flops-sr-jk-d-t-propagation-timing': { type: 'linear_prop', slope: 8.4000, ref: 8.4000 },
  'shift-registers-siso-sipo-piso-pipo-ring-johnson': { type: 'linear_affine', slope: 2.1500, intercept: 6.0000, ref: 2.1500 },
  'digital-to-analog-and-analog-to-digital-converters': { type: 'linear_prop', slope: 0.01953, ref: 0.01953 },
  'microprocessor-instruction-cycle-bus-timing': { type: 'linear_prop', slope: 1.0000, ref: 1.0000 },
  'microcontroller-gpio-timer-interrupts-pwm': { type: 'linear_prop', slope: 0.0500, ref: 0.0500 },

  // Module 4: Electrical Machines & Electromechanics (Labs 28–36)
  'dc-shunt-motor-speed-control-armature-field': { type: 'linear_prop', slope: 6.8000, ref: 6.8000 },
  'dc-series-motor-torque-speed-characteristics': { type: 'linear_prop', slope: 0.3500, ref: 0.3500 },
  'open-circuit-and-short-circuit-tests-transformer': { type: 'linear_prop', slope: 4.2500, ref: 4.2500 },
  'three-phase-transformer-connections-and-polarity': { type: 'linear_prop', slope: 0.5774, ref: 0.5774 },
  'three-phase-squirrel-cage-induction-motor-load-test': { type: 'linear_prop', slope: 0.6500, ref: 0.6500 },
  'synchronous-generator-open-circuit-short-circuit-v-curves': { type: 'linear_prop', slope: 185.0000, ref: 185.0000 },
  'synchronous-motor-v-and-inverted-v-curves': { type: 'linear_affine', slope: 4.5000, intercept: 2.0000, ref: 4.5000 },
  'single-phase-capacitor-start-induction-motor': { type: 'linear_prop', slope: 0.0450, ref: 0.0450 },
  'switched-reluctance-and-stepper-motor-step-angle': { type: 'linear_prop', slope: 1.8000, ref: 1.8000 },

  // Module 5: Power Systems, High Voltage & Renewable Energy (Labs 37–43)
  'transmission-line-abcd-parameters-ferranti-effect': { type: 'linear_affine', slope: -2.8500, intercept: 230.0000, ref: 2.8500, abs_ref: true },
  'earth-fault-and-overcurrent-relay-idmt-characteristics': { type: 'linear_prop', slope: 0.1400, ref: 0.1400 },
  'dielectric-breakdown-strength-transformer-insulating-oil': { type: 'linear_prop', slope: 22.5000, ref: 22.5000 },
  'photovoltaic-pv-cell-iv-and-pv-characteristics': { type: 'linear_prop', slope: 0.00485, ref: 0.00485 },
  'wind-turbine-generator-power-coefficient-betz-limit': { type: 'linear_prop', slope: 0.4200, ref: 0.4200 },
  'high-voltage-impulse-generator-marx-circuit': { type: 'linear_prop', slope: 45.0000, ref: 45.0000 },
  'harmonic-distortion-measurement-fft-spectrum': { type: 'linear_affine', slope: 0.5500, intercept: 12.0000, ref: 0.5500 },

  // Module 6: Control Systems, Instrumentation & Power Electronics (Labs 44–50)
  'scr-triac-phase-angle-firing-control-r-rl-loads': { type: 'linear_prop', slope: 48.0000, ref: 48.0000 },
  'buck-boost-dc-dc-converter-duty-cycle-efficiency': { type: 'linear_prop', slope: 24.0000, ref: 24.0000 },
  'single-phase-spwm-inverter-total-harmonic-distortion': { type: 'linear_prop', slope: 70.7100, ref: 70.7100 },
  'closed-loop-pid-dc-motor-speed-servomechanism': { type: 'linear_affine', slope: 5.2000, intercept: 10.0000, ref: 5.2000 },
  'bode-plot-and-nyquist-stability-criterion': { type: 'linear_affine', slope: -20.0000, intercept: 0.0000, ref: 20.0000, abs_ref: true },
  'linear-variable-differential-transformer-lvdt-transducer': { type: 'linear_prop', slope: 0.8500, ref: 0.8500 },
  'strain-gauge-quarter-half-full-wheatstone-bridge': { type: 'linear_prop', slope: 0.0125, ref: 0.0125 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Electrical Engineering experiment: ' + slug);

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
  root.ElectricalModels = api;
}
})(typeof window !== 'undefined' ? window : globalThis);
