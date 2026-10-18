(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Dental Materials Science & Biomaterials (Labs 1–6)
  'gypsum-water-powder-ratio-setting-time': { type: 'linear_affine', slope: 0.5500, intercept: -3.2000, ref: 0.5500 },
  'dental-alginate-gelation-temperature-kinetics': { type: 'linear_affine', slope: -6.8000, intercept: 285.0000, ref: 6.8000, abs_ref: true },
  'elastomeric-impression-polymerization-shrinkage': { type: 'linear_affine', slope: -0.0075, intercept: 0.6800, ref: 0.0075, abs_ref: true },
  'composite-resin-light-cure-depth-irradiance': { type: 'linear_affine', slope: 0.0018, intercept: 1.2500, ref: 0.0018 },
  'diametral-tensile-strength-resin-composite': { type: 'linear_affine', slope: 0.9200, intercept: -16.5000, ref: 0.9200 },
  'dental-amalgam-creep-compliance-viscoelasticity': { type: 'linear_prop', slope: 0.0380, ref: 0.0380 },

  // Module 2: Dental Anatomy, Enamel/Dentin Biomechanics & Adhesion (Labs 7–11)
  'acid-etching-enamel-depth-demineralization': { type: 'linear_affine', slope: 0.2800, intercept: 1.5000, ref: 0.2800 },
  'microtensile-bond-strength-dentin-adhesive': { type: 'linear_affine', slope: 1.3500, intercept: 8.2000, ref: 1.3500 },
  'dentin-hydraulic-conductance-tubule-occlusion': { type: 'linear_prop', slope: 0.0450, ref: 0.0450 },
  'knop-microhardness-enamel-demineralization': { type: 'linear_affine', slope: 0.0950, intercept: 210.0000, ref: 0.0950 },
  'thermal-expansion-mismatch-porcelain-fused-metal': { type: 'linear_prop', slope: 1.2500, ref: 1.2500 },

  // Module 3: Periodontics, Endodontics & Oral Microbiome (Labs 12–16)
  'periodontal-probing-depth-fluid-exudate': { type: 'linear_affine', slope: 0.3200, intercept: -0.2500, ref: 0.3200 },
  'endodontic-file-torsional-fatigue-resistance': { type: 'linear_affine', slope: 78.0000, intercept: 25.0000, ref: 78.0000 },
  'sodium-hypochlorite-tissue-dissolution-rate': { type: 'linear_prop', slope: 4.2000, ref: 4.2000 },
  'streptococcus-mutans-biofilm-acidogenesis': { type: 'linear_affine', slope: 0.0340, intercept: 0.1200, ref: 0.0340 },
  'chlorhexidine-substantivity-salivary-pellicle': { type: 'linear_prop', slope: 6.5000, ref: 6.5000 },

  // Module 4: Prosthodontics, Orthodontics & Oral Mechanics (Labs 17–21)
  'orthodontic-archwire-load-deflection-rate': { type: 'linear_prop', slope: 65.0000, ref: 65.0000 },
  'acrylic-denture-base-residual-monomer-cure': { type: 'linear_affine', slope: -0.0180, intercept: 2.1500, ref: 0.0180, abs_ref: true },
  'dental-cement-film-thickness-seating-pressure': { type: 'linear_affine', slope: -0.1100, intercept: 44.5000, ref: 0.1100, abs_ref: true },
  'occlusal-bite-force-transducer-calibration': { type: 'linear_affine', slope: 1.6500, intercept: -15.0000, ref: 1.6500 },
  'dental-implant-primary-stability-torque': { type: 'linear_affine', slope: 0.6500, intercept: 42.0000, ref: 0.6500 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Dentistry experiment: ' + slug);

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
  root.DentistryModels = api;
}
})(typeof window !== 'undefined' ? window : globalThis);
