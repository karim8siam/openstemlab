(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Yarn Manufacturing & Fiber Science (Labs 1–6)
  'cotton-fiber-length-uniformity-comb-sorter': { type: 'linear_affine', slope: -0.2200, intercept: 29.5000, ref: 0.2200, abs_ref: true },
  'fiber-tensile-strength-stelometer-bundle-test': { type: 'linear_prop', slope: 14.5000, ref: 14.5000 },
  'yarn-linear-density-count-wrap-reel-analytical-balance': { type: 'linear_prop', slope: 0.0200, ref: 0.0200 },
  'yarn-twist-determination-untwist-retwist-method': { type: 'linear_prop', slope: 820.0000, ref: 820.0000 },
  'single-yarn-tensile-strength-elongation-cre': { type: 'linear_prop', slope: 16.5000, ref: 16.5000 },
  'yarn-lea-strength-count-strength-product-csp': { type: 'linear_prop', slope: 2400.0000, ref: 2400.0000 },

  // Module 2: Fabric Manufacturing (Weaving & Knitting) (Labs 7–12)
  'warp-sizing-percentage-size-add-on-tensile-gain': { type: 'linear_prop', slope: 18.5000, ref: 18.5000 },
  'fabric-areal-density-gsm-thickness-micrometer': { type: 'linear_prop', slope: 220.0000, ref: 220.0000 },
  'fabric-tensile-strip-grab-test-astm-d5034': { type: 'linear_prop', slope: 12.8000, ref: 12.8000 },
  'fabric-tearing-strength-elmendorf-ballistic-pendulum': { type: 'linear_prop', slope: 3400.0000, ref: 3400.0000 },
  'fabric-bursting-strength-hydraulic-diaphragm-tester': { type: 'linear_prop', slope: 0.0450, ref: 0.0450 },
  'weft-knitted-fabric-loop-length-stitch-density': { type: 'linear_prop', slope: 16.0000, ref: 16.0000 },

  // Module 3: Textile Chemical Processing, Wet Processing & Dyeing (Labs 13–18)
  'enzymatic-desizing-efficiency-tegewa-iodine-scale': { type: 'linear_affine', slope: 14.5000, intercept: 12.0000, ref: 14.5000 },
  'scouring-loss-absorbency-capillary-wicking-test': { type: 'linear_prop', slope: 18.2000, ref: 18.2000 },
  'hydrogen-peroxide-bleaching-whiteness-berger-cielab': { type: 'linear_affine', slope: 0.8500, intercept: 32.0000, ref: 0.8500 },
  'reactive-dye-exhaustion-kinetics-beer-lambert-absorbance': { type: 'linear_prop', slope: 0.0385, ref: 0.0385 },
  'color-fastness-to-washing-iso-105-c06-grey-scale': { type: 'linear_affine', slope: 0.0820, intercept: -1.2000, ref: 0.0820 },
  'color-fastness-to-crocking-rubbing-aatcc-crockmeter': { type: 'linear_prop', slope: 0.0650, ref: 0.0650 },

  // Module 4: Fabric Comfort, Hand & Physical Performance (Labs 19–24)
  'fabric-air-permeability-differential-pressure-flow': { type: 'linear_prop', slope: 0.4200, ref: 0.4200 },
  'fabric-water-vapor-permeability-cup-dish-method': { type: 'linear_prop', slope: 1.4500, ref: 1.4500 },
  'fabric-water-repellency-spray-rating-contact-angle': { type: 'linear_affine', slope: 0.8500, intercept: 75.0000, ref: 0.8500 },
  'fabric-bending-length-flexural-rigidity-shirley-stiffness': { type: 'linear_prop', slope: 24.5000, ref: 24.5000 },
  'fabric-crease-recovery-angle-shirley-recovery-tester': { type: 'linear_affine', slope: 8.5000, intercept: 95.0000, ref: 8.5000 },
  'fabric-drape-coefficient-digital-drape-meter': { type: 'linear_affine', slope: 18.5000, intercept: 22.0000, ref: 18.5000 },

  // Module 5: Textile Tribology, Durability & Surface Testing (Labs 25–28)
  'fabric-abrasion-resistance-martindale-mass-loss': { type: 'linear_prop', slope: 1.6500, ref: 1.6500 },
  'fabric-pilling-resistance-ici-pilling-box': { type: 'linear_prop', slope: 5.2000, ref: 5.2000 },
  'fabric-dimensional-stability-laundering-shrinkage': { type: 'linear_affine', slope: 0.8500, intercept: 1.2000, ref: 0.8500 },
  'seam-slippage-strength-woven-fabrics-fixed-load': { type: 'linear_prop', slope: 0.0350, ref: 0.0350 },

  // Module 6: Technical Textiles, Nonwovens & Color Science (Labs 29–32)
  'nonwoven-fabric-tensile-strength-anisotropy-ratio': { type: 'linear_prop', slope: 2.4500, ref: 2.4500 },
  'thermal-resistance-clo-value-guarded-hotplate': { type: 'linear_prop', slope: 0.0240, ref: 0.0240 },
  'ultraviolet-protection-factor-upf-transmittance-spectrophotometry': { type: 'linear_affine', slope: 18.5000, intercept: 15.0000, ref: 18.5000 },
  'spectrophotometric-color-matching-cielab-kubelka-munk': { type: 'linear_prop', slope: 4.8500, ref: 4.8500 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Textile Engineering experiment: ' + slug);

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
  root.TextileModels = api;
}
})(typeof window !== 'undefined' ? window : globalThis);
