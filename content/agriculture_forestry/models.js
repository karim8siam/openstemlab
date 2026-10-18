(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Agronomy, Crop Physiology & Seed Science (Labs 1–4)
  'seed-germination-vigor-tetrazolium-viability': { type: 'linear_affine', slope: 2.4500, intercept: 12.0000, ref: 2.4500 },
  'soil-moisture-neutron-probe-calibration': { type: 'linear_affine', slope: 2.8500, intercept: 0.1200, ref: 2.8500 },
  'crop-water-stress-index-infrared-thermometry': { type: 'linear_affine', slope: -1.6500, intercept: 2.1000, ref: 1.6500, abs_ref: true },
  'chlorophyll-spad-meter-nitrogen-status': { type: 'linear_affine', slope: 0.0650, intercept: 0.4500, ref: 0.0650 },

  // Module 2: Soil Science, Plant Nutrition & Fertilizer Dynamics (Labs 5–8)
  'soil-cation-exchange-capacity-ammonium-acetate': { type: 'linear_affine', slope: 0.5800, intercept: 4.2000, ref: 0.5800 },
  'bray-curtis-soil-available-phosphorus': { type: 'linear_affine', slope: 0.0280, intercept: 0.0120, ref: 0.0280 },
  'soil-salinity-electrical-conductivity-extract': { type: 'linear_prop', slope: 12.8000, ref: 12.8000 },
  'plant-tissue-potassium-flame-photometry': { type: 'linear_affine', slope: 7.8500, intercept: 1.2000, ref: 7.8500 },

  // Module 3: Irrigation, Agrohydrology & Drainage Engineering (Labs 9–12)
  'subsurface-drip-irrigation-emitter-discharge-uniformity': { type: 'linear_affine', slope: 0.0240, intercept: 1.1500, ref: 0.0240 },
  'penman-monteith-reference-evapotranspiration': { type: 'linear_affine', slope: 0.1850, intercept: 0.6500, ref: 0.1850 },
  'furrow-irrigation-advance-infiltration-kostiakov': { type: 'linear_affine', slope: 0.8500, intercept: 8.5000, ref: 0.8500 },
  'tensiometer-soil-matric-potential-retention': { type: 'linear_affine', slope: -0.0035, intercept: 0.4200, ref: 0.0035, abs_ref: true },

  // Module 4: Plant Pathology, Entomology & Crop Protection (Labs 13–16)
  'fungicide-bioassay-mycelial-growth-inhibition': { type: 'linear_affine', slope: 2.8500, intercept: 8.2000, ref: 2.8500 },
  'insect-population-sweep-net-economic-threshold': { type: 'linear_affine', slope: 0.8500, intercept: 1.5000, ref: 0.8500 },
  'herbicide-spray-droplet-spectrum-water-sensitive-paper': { type: 'linear_affine', slope: -0.4200, intercept: 380.0000, ref: 0.4200, abs_ref: true },
  'seed-borne-pathogen-blotter-infection-incidence': { type: 'linear_affine', slope: 1.2500, intercept: 3.5000, ref: 1.2500 },

  // Module 5: Silviculture, Forest Mensuration & Agroforestry (Labs 17–20)
  'forest-stand-basal-area-wedge-prism-relascope': { type: 'linear_prop', slope: 2.0000, ref: 2.0000 },
  'tree-height-clinometer-hypsometer-allometry': { type: 'linear_affine', slope: 20.0000, intercept: 1.6500, ref: 20.0000 },
  'tree-ring-growth-increment-borer-site-index': { type: 'linear_affine', slope: 0.3800, intercept: 4.5000, ref: 0.3800 },
  'forest-fuel-moisture-timelag-fire-danger': { type: 'linear_affine', slope: 0.1750, intercept: 2.2000, ref: 0.1750 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Agriculture & Forestry experiment: ' + slug);

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
  root.AgricultureForestryModels = api;
}
})(typeof window !== 'undefined' ? window : globalThis);
