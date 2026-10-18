(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Proximate Analysis & Food Chemistry (Labs 1–6)
  'moisture-content-forced-air-oven-drying': { type: 'linear_affine', slope: 0.3800, intercept: 4.5000, ref: 0.3800 },
  'crude-protein-kjeldahl-nitrogen-titration': { type: 'linear_prop', slope: 1.1200, ref: 1.1200 },
  'soxhlet-crude-fat-petroleum-ether-extraction': { type: 'linear_affine', slope: 0.4200, intercept: 1.2000, ref: 0.4200 },
  'crude-fiber-acid-alkali-digestion-gravimetry': { type: 'linear_prop', slope: 0.0850, ref: 0.0850 },
  'food-ash-muffle-furnace-gravimetric-assay': { type: 'linear_prop', slope: 0.0480, ref: 0.0480 },
  'water-activity-chilled-mirror-dewpoint-isotherm': { type: 'linear_affine', slope: 0.0385, intercept: 0.1200, ref: 0.0385 },

  // Module 2: Micronutrients, Vitamins & Food Pigments (Labs 7–11)
  'vitamin-c-2-6-dichlorophenolindophenol-titrimetry': { type: 'linear_prop', slope: 1.8500, ref: 1.8500 },
  'total-anthocyanins-ph-differential-spectrophotometry': { type: 'linear_prop', slope: 0.0780, ref: 0.0780 },
  'beta-carotene-spectrophotometric-beer-lambert': { type: 'linear_prop', slope: 0.2450, ref: 0.2450 },
  'iron-content-ferrozine-spectrophotometric-assay': { type: 'linear_prop', slope: 0.4800, ref: 0.4800 },
  'total-polyphenols-folin-ciocalteu-gallic-acid': { type: 'linear_affine', slope: 0.0092, intercept: 0.0250, ref: 0.0092 },

  // Module 3: Food Quality, Lipids & Enzymatic Browning (Labs 12–16)
  'free-fatty-acids-titratable-acidity-oil': { type: 'linear_prop', slope: 0.5640, ref: 0.5640 },
  'peroxide-value-iodometric-thiosulfate-titration': { type: 'linear_prop', slope: 2.0000, ref: 2.0000 },
  'polyphenol-oxidase-enzymatic-browning-kinetics': { type: 'linear_affine', slope: 0.0280, intercept: 0.0150, ref: 0.0280 },
  'titratable-acidity-fruit-juice-citric-acid': { type: 'linear_prop', slope: 0.0640, ref: 0.0640 },
  'brix-refractometry-sugar-soluble-solids': { type: 'linear_prop', slope: 14.2000, ref: 14.2000 },

  // Module 4: Food Rheology, Processing & Nutrition (Labs 17–21)
  'apparent-viscosity-coaxial-cylinder-rheometer': { type: 'linear_prop', slope: 0.0850, ref: 0.0850 },
  'emulsion-stability-centrifugal-creaming-index': { type: 'linear_affine', slope: 0.0085, intercept: 4.2000, ref: 0.0085 },
  'thermal-death-time-d-value-bacterial-inactivation': { type: 'linear_prop', slope: -0.4500, ref: 0.4500, abs_ref: true },
  'glycemic-index-in-vitro-starch-amylolysis': { type: 'linear_affine', slope: 0.1650, intercept: 2.8000, ref: 0.1650 },
  'dietary-energy-bomb-calorimetry-enthalpy': { type: 'linear_prop', slope: 2.4500, ref: 2.4500 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Food & Nutrition experiment: ' + slug);

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
  root.FoodModels = api;
}
})(typeof window !== 'undefined' ? window : globalThis);
