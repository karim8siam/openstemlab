(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Analog Modulation & Superheterodyne Systems (Labs 1–5)
  'amplitude-modulation-and-demodulation-envelope-detector': { type: 'linear_prop', slope: 10.0000, ref: 10.0000 },
  'frequency-modulation-and-demodulation-foster-seeley-discriminator': { type: 'linear_prop', slope: 0.0500, ref: 0.0500 },
  'double-sideband-suppressed-carrier-dsbsc-balanced-modulator': { type: 'linear_prop', slope: 1.5000, ref: 1.5000 },
  'single-sideband-suppressed-carrier-ssbsc-filter-method': { type: 'linear_prop', slope: 0.7500, ref: 0.7500 },
  'superheterodyne-receiver-intermediate-frequency-and-selectivity': { type: 'linear_prop', slope: 2.2000, ref: 2.2000 },

  // Module 2: Pulse Modulation & Digital Baseband Transmission (Labs 6–10)
  'sampling-theorem-and-pulse-amplitude-modulation-pam': { type: 'linear_affine', slope: -0.0025, intercept: 12.0000, ref: 0.0025, abs_ref: true },
  'pulse-width-and-pulse-position-modulation-pwm-ppm': { type: 'linear_affine', slope: 15.0000, intercept: 5.0000, ref: 15.0000 },
  'pulse-code-modulation-pcm-and-quantization-noise': { type: 'linear_affine', slope: 6.0200, intercept: 1.7600, ref: 6.0200 },
  'delta-modulation-and-adaptive-delta-modulation-slope-overload': { type: 'linear_prop', slope: 12.5000, ref: 12.5000 },
  'line-coding-techniques-and-eye-diagram-analysis': { type: 'linear_affine', slope: -150.0000, intercept: 98.0000, ref: 150.0000, abs_ref: true },

  // Module 3: Digital Passband Modulation & Detection (Labs 11–15)
  'amplitude-shift-keying-ask-ook-coherent-detection': { type: 'linear_prop', slope: 2.0000, ref: 2.0000 },
  'frequency-shift-keying-fsk-and-phase-locked-loop-detection': { type: 'linear_prop', slope: 0.0800, ref: 0.0800 },
  'binary-phase-shift-keying-bpsk-and-costas-loop-carrier-recovery': { type: 'linear_prop', slope: 1.4142, ref: 1.4142 },
  'quadrature-phase-shift-keying-qpsk-constellation-mapping': { type: 'linear_prop', slope: 1.4142, ref: 1.4142 },
  'quadrature-amplitude-modulation-16qam-error-vector-magnitude': { type: 'linear_affine', slope: -0.8500, intercept: 28.5000, ref: 0.8500, abs_ref: true },

  // Module 4: Antennas, RF Circuits & Microwave Propagation (Labs 16–20)
  'half-wave-dipole-antenna-radiation-pattern-and-gain': { type: 'linear_affine', slope: 1.0000, intercept: -18.5000, ref: 1.0000 },
  'horn-antenna-directivity-and-absolute-gain-measurement': { type: 'linear_prop', slope: 45.0000, ref: 45.0000 },
  'rectangular-waveguide-te10-cutoff-frequency-and-guide-wavelength': { type: 'linear_prop', slope: 18.8496, ref: 18.8496 },
  'voltage-standing-wave-ratio-vswr-and-slotted-line-impedance': { type: 'linear_prop', slope: 1.0000, ref: 1.0000 },
  'microstrip-line-characteristic-impedance-and-effective-dielectric-constant': { type: 'linear_affine', slope: 24.5000, intercept: 35.0000, ref: 24.5000 },

  // Module 5: Optical Fiber Communication & Optoelectronics (Labs 21–25)
  'optical-fiber-numerical-aperture-and-acceptance-angle': { type: 'linear_prop', slope: 0.4200, ref: 0.4200 },
  'optical-fiber-attenuation-and-cutback-loss-measurement': { type: 'linear_prop', slope: 0.0028, ref: 0.0028 },
  'fiber-optic-macro-and-micro-bending-losses': { type: 'linear_prop', slope: 18.5000, ref: 18.5000 },
  'semiconductor-laser-diode-optical-power-current-pi-curve': { type: 'linear_prop', slope: 0.2800, ref: 0.2800 },
  'pin-photodiode-responsivity-and-quantum-efficiency': { type: 'linear_prop', slope: 0.8500, ref: 0.8500 },

  // Module 6: Digital Signal Processing, Spread Spectrum & Information Theory (Labs 26–30)
  'discrete-fourier-transform-dft-and-fft-spectral-leakage': { type: 'linear_prop', slope: 0.5000, ref: 0.5000 },
  'finite-impulse-response-fir-digital-filter-design-window-method': { type: 'linear_affine', slope: 7.2000, intercept: 13.5000, ref: 7.2000 },
  'infinite-impulse-response-iir-bilinear-transformation-filter': { type: 'linear_prop', slope: 0.00005, ref: 0.00005 },
  'direct-sequence-spread-spectrum-dsss-processing-gain': { type: 'linear_affine', slope: 10.0000, intercept: -40.0000, ref: 10.0000 },
  'shannon-hartley-channel-capacity-and-entropy-limits': { type: 'linear_prop', slope: 5.0444, ref: 5.0444 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Electronics & Communication experiment: ' + slug);

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
  root.ECEModels = api;
}
})(typeof window !== 'undefined' ? window : globalThis);
