(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Fluvial Geomorphology & Hydrology (Labs 1–4)
  'river-discharge-velocity-area-current-meter': { type: 'linear_prop', slope: 8.4000, ref: 8.4000 },
  'fluvial-sediment-grain-size-phi-scale': { type: 'linear_affine', slope: 16.5000, intercept: 45.0000, ref: 16.5000 },
  'bedload-transport-critical-shear-stress-shields': { type: 'linear_affine', slope: 2.8500, intercept: -8.5000, ref: 2.8500 },
  'river-hydraulic-geometry-downstream-scaling': { type: 'linear_affine', slope: 0.5000, intercept: 1.2000, ref: 0.5000 },

  // Module 2: Meteorology, Climatology & Microclimate (Labs 5–8)
  'psychrometric-relative-humidity-dew-point': { type: 'linear_affine', slope: -5.8000, intercept: 96.0000, ref: 5.8000, abs_ref: true },
  'surface-radiation-budget-albedo-pyranometer': { type: 'linear_prop', slope: 0.2200, ref: 0.2200 },
  'soil-heat-flux-thermal-diffusivity': { type: 'linear_prop', slope: 0.0820, ref: 0.0820 },
  'urban-heat-island-canopy-temperature-transect': { type: 'linear_affine', slope: 0.0480, intercept: 0.2500, ref: 0.0480 },

  // Module 3: Biogeography, Soil Geography & Ecology (Labs 9–12)
  'soil-moisture-gravimetric-water-content': { type: 'linear_prop', slope: 0.8200, ref: 0.8200 },
  'soil-infiltration-double-ring-infiltrometer': { type: 'linear_affine', slope: 45.0000, intercept: 15.0000, ref: 45.0000 },
  'plant-canopy-leaf-area-index-beers-law': { type: 'linear_prop', slope: 0.6500, ref: 0.6500 },
  'species-area-relationship-spatial-biodiversity': { type: 'linear_affine', slope: 0.2600, intercept: 1.8500, ref: 0.2600 },

  // Module 4: Coastal, Glacial & Slope Geomorphology (Labs 13–16)
  'slope-stability-safety-factor-infinite-slope': { type: 'linear_affine', slope: -0.0420, intercept: 2.4500, ref: 0.0420, abs_ref: true },
  'soil-erosion-pin-rill-depth-universal-soil-loss': { type: 'linear_prop', slope: 0.0420, ref: 0.0420 },
  'beach-profile-morphodynamics-emery-pole': { type: 'linear_prop', slope: 0.0650, ref: 0.0650 },
  'wave-shoaling-refraction-snells-law': { type: 'linear_prop', slope: 0.6200, ref: 0.6200 },

  // Module 5: Spatial Analysis, Cartography & Urban Geography (Labs 17–20)
  'gravity-model-spatial-interaction-trade': { type: 'linear_prop', slope: 3.4500, ref: 3.4500 },
  'rank-size-rule-urban-hierarchy-zipf': { type: 'linear_affine', slope: -1.0200, intercept: 15.2000, ref: 1.0200, abs_ref: true },
  'nearest-neighbor-spatial-point-pattern-analysis': { type: 'linear_affine', slope: -0.3800, intercept: 0.9500, ref: 0.3800, abs_ref: true },
  'land-surface-temperature-split-window-landsat': { type: 'linear_affine', slope: 1.0800, intercept: -21.5000, ref: 1.0800 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Geography experiment: ' + slug);

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
  root.GeographyModels = api;
}
})(typeof window !== 'undefined' ? window : globalThis);
