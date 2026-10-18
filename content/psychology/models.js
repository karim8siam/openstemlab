(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Cognitive Psychology, Perception & Psychophysics (Labs 1–4)
  'choice-reaction-time-hicks-law': { type: 'linear_affine', slope: 152.0000, intercept: 185.0000, ref: 152.0000 },
  'stroop-interference-effect-naming-latency': { type: 'linear_affine', slope: 18.5000, intercept: 520.0000, ref: 18.5000 },
  'weber-fechner-fraction-luminance-discrimination': { type: 'linear_prop', slope: 0.0820, ref: 0.0820 },
  'mental-rotation-reaction-time-shepard-metzler': { type: 'linear_affine', slope: 3.2500, intercept: 480.0000, ref: 3.2500 },

  // Module 2: Memory, Attention & Executive Function (Labs 5–8)
  'working-memory-span-sternberg-search-rate': { type: 'linear_affine', slope: 38.0000, intercept: 395.0000, ref: 38.0000 },
  'ebbinghaus-forgetting-curve-savings-retention': { type: 'linear_affine', slope: -12.4000, intercept: 88.5000, ref: 12.4000, abs_ref: true },
  'fitts-law-pointing-index-of-difficulty': { type: 'linear_affine', slope: 145.0000, intercept: 120.0000, ref: 145.0000 },
  'signal-detection-theory-perceptual-sensitivity-dprime': { type: 'linear_prop', slope: 0.2850, ref: 0.2850 },

  // Module 3: Learning, Conditioning & Behavioral Decision Making (Labs 9–12)
  'rescorla-wagner-associative-strength-conditioning': { type: 'linear_affine', slope: 4.8000, intercept: 15.0000, ref: 4.8000 },
  'delay-discounting-hyperbolic-value-decay': { type: 'linear_affine', slope: -0.6500, intercept: 98.0000, ref: 0.6500, abs_ref: true },
  'prospect-theory-loss-aversion-subjective-value': { type: 'linear_prop', slope: 2.1500, ref: 2.1500 },
  'visual-search-feature-conjunction-slope': { type: 'linear_affine', slope: 24.5000, intercept: 410.0000, ref: 24.5000 },

  // Module 4: Physiological & Neuropsychological Measurement (Labs 13–16)
  'galvanic-skin-response-electrodermal-arousal': { type: 'linear_affine', slope: 0.0480, intercept: -1.2000, ref: 0.0480 },
  'pupillometric-dilation-cognitive-load': { type: 'linear_affine', slope: 0.0750, intercept: 0.1000, ref: 0.0750 },
  'eeg-p300-event-related-potential-amplitude': { type: 'linear_affine', slope: 1.6500, intercept: 3.2000, ref: 1.6500 },
  'visual-acuity-snellen-logmar-contrast-sensitivity': { type: 'linear_affine', slope: -0.0650, intercept: 2.1500, ref: 0.0650, abs_ref: true },

  // Module 5: Social, Developmental & Differential Psychology (Labs 17–20)
  'implicit-association-test-d-score-evaluative-bias': { type: 'linear_affine', slope: 28.5000, intercept: 45.0000, ref: 28.5000 },
  'bistable-necker-cube-perceptual-switching-rate': { type: 'linear_affine', slope: 3.8000, intercept: 4.2000, ref: 3.8000 },
  'serial-position-effect-primacy-recency-memory': { type: 'linear_affine', slope: -5.4000, intercept: 84.0000, ref: 5.4000, abs_ref: true },
  'eye-tracking-saccadic-latency-fixation-duration': { type: 'linear_affine', slope: 4.6000, intercept: 195.0000, ref: 4.6000 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Psychology experiment: ' + slug);

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
  root.PsychologyModels = api;
}
})(typeof window !== 'undefined' ? window : globalThis);
