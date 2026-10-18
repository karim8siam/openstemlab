(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Archaeological Survey, Field Geophysics & Site Prospection (Labs 1–4)
  'radiometric-carbon14-decay-dating-calibration': { type: 'linear_prop', slope: 5730.0000, ref: 5730.0000 },
  'magnetic-susceptibility-soil-prospection': { type: 'linear_prop', slope: 14.5000, ref: 14.5000 },
  'electrical-resistivity-pseudosection-archaeological-survey': { type: 'linear_affine', slope: 38.5000, intercept: 65.0000, ref: 38.5000 },
  'stratigraphic-harris-matrix-seriation': { type: 'linear_prop', slope: 125.0000, ref: 125.0000 },

  // Module 2: Lithic Technology & Material Sourcing (Archaeometry) (Labs 5–8)
  'flint-knapping-conchoidal-fracture-angle': { type: 'linear_affine', slope: -0.1200, intercept: 14.8000, ref: 0.1200, abs_ref: true },
  'obsidian-hydration-layer-thickness-chronometry': { type: 'linear_prop', slope: 0.0850, ref: 0.0850 },
  'xrf-provenance-obsidian-lithic-sourcing': { type: 'linear_prop', slope: 1.8500, ref: 1.8500 },
  'ceramic-thin-section-petrography-temper-density': { type: 'linear_prop', slope: 0.7500, ref: 0.7500 },

  // Module 3: Ceramic Archaeometry & Pyrotechnology (Labs 9–12)
  'ceramic-thermal-expansion-firing-temperature': { type: 'linear_affine', slope: 0.1650, intercept: 0.1200, ref: 0.1650 },
  'archaeomagnetic-inclination-paleointensity': { type: 'linear_affine', slope: -4.2000, intercept: 58.5000, ref: 4.2000, abs_ref: true },
  'pottery-water-absorption-open-porosity': { type: 'linear_affine', slope: -1.4500, intercept: 22.8000, ref: 1.4500, abs_ref: true },
  'residue-gas-chromatography-lipid-biomarkers': { type: 'linear_prop', slope: 1.6200, ref: 1.6200 },

  // Module 4: Bioarchaeology, Zooarchaeology & Skeletal Analysis (Labs 13–16)
  'dental-cementum-increment-age-seasonality': { type: 'linear_affine', slope: 1.0000, intercept: 2.5000, ref: 1.0000 },
  'stable-isotope-paleodiet-carbon-nitrogen': { type: 'linear_affine', slope: 0.5500, intercept: 21.2000, ref: 0.5500 },
  'strontium-isotope-ratio-human-mobility': { type: 'linear_affine', slope: 0.4200, intercept: 7080.0000, ref: 0.4200 },
  'osteometric-sex-estimation-femur-diameter': { type: 'linear_affine', slope: 0.1850, intercept: -8.2500, ref: 0.1850 },

  // Module 5: Geoarchaeology, Site Formation & Micro-Artifact Analysis (Labs 17–20)
  'soil-phosphorus-spot-test-anthropic-settlement': { type: 'linear_prop', slope: 0.0028, ref: 0.0028 },
  'sediment-particle-size-settling-settlement-matrix': { type: 'linear_prop', slope: 480.0000, ref: 480.0000 },
  'heavy-fraction-soil-micromorphology-loss-on-ignition': { type: 'linear_prop', slope: 0.5400, ref: 0.5400 },
  'phytolith-morphometric-silica-taxonomic-ratio': { type: 'linear_affine', slope: 1.7500, intercept: 2.4000, ref: 1.7500 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Archaeology experiment: ' + slug);

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
  root.ArchaeologyModels = api;
}
})(typeof window !== 'undefined' ? window : globalThis);
