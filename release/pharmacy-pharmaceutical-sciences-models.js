(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Pharmaceutics, Preformulation & Physical Pharmacy (Labs 1–8)
  'paracetamol-tablet-compression-force-tensile-strength': { type: 'linear_affine', slope: 0.1200, intercept: 0.4500, ref: 0.1200 },
  'benzoic-acid-aqueous-solubility-temperature-van-t-hoff': { type: 'linear_affine', slope: 0.1150, intercept: 0.4500, ref: 0.1150 },
  'drug-octanol-water-partition-coefficient-shake-flask': { type: 'linear_affine', slope: 0.8250, intercept: 0.0200, ref: 0.8250 },
  'usp-apparatus-2-paddle-dissolution-rate': { type: 'linear_affine', slope: 0.0380, intercept: 0.4500, ref: 0.0380 },
  'sodium-lauryl-sulfate-micellization-conductometry': { type: 'linear_affine', slope: 72.5000, intercept: 15.0000, ref: 72.5000 },
  'pharmaceutical-suspension-flocculation-zeta-potential': { type: 'linear_affine', slope: -18.5000, intercept: 42.0000, ref: 18.5000, abs_ref: true },
  'hydrophilic-polymer-matrix-swelling-erosion-kinetics': { type: 'linear_affine', slope: 1.8500, intercept: 12.0000, ref: 1.8500 },
  'pharmaceutical-powder-flowability-carr-compressibility': { type: 'linear_affine', slope: 0.00021, intercept: 0.0450, ref: 0.00021 },

  // Module 2: Pharmaceutical Analysis & Quality Assurance (Labs 9–16)
  'uv-vis-spectrophotometric-paracetamol-beer-lambert': { type: 'linear_affine', slope: 0.0475, intercept: 0.0080, ref: 0.0475 },
  'hplc-isocratic-separation-caffeine-paracetamol': { type: 'linear_affine', slope: 3850.0000, intercept: 45.0000, ref: 3850.0000 },
  'non-aqueous-potentiometric-titration-weak-base': { type: 'linear_affine', slope: 0.0351, intercept: 0.0200, ref: 0.0351 },
  'karl-fischer-coulometric-water-determination': { type: 'linear_affine', slope: 10.7100, intercept: 8.5000, ref: 10.7100 },
  'first-order-accelerated-chemical-stability-arrhenius': { type: 'linear_affine', slope: 0.2450, intercept: -8.2000, ref: 0.2450 },
  'gas-chromatography-residual-solvent-headspace': { type: 'linear_affine', slope: 14.2000, intercept: 65.0000, ref: 14.2000 },
  'fluorescence-spectroscopy-quinine-quantum-yield': { type: 'linear_affine', slope: 980.0000, intercept: 12.0000, ref: 980.0000 },
  'potassium-permanganate-redox-titration-hydrogen-peroxide': { type: 'linear_affine', slope: 4.8500, intercept: 0.1500, ref: 4.8500 },

  // Module 3: Pharmacokinetics, Biopharmaceutics & Drug Metabolism (Labs 17–24)
  'one-compartment-intravenous-bolus-clearance': { type: 'linear_affine', slope: 0.0520, intercept: 0.1200, ref: 0.0520 },
  'plasma-protein-binding-equilibrium-dialysis': { type: 'linear_affine', slope: 0.0125, intercept: 0.0020, ref: 0.0125 },
  'in-vitro-transwell-caco-2-apparent-permeability': { type: 'linear_affine', slope: 0.0840, intercept: 0.1500, ref: 0.0840 },
  'hepatic-microsomal-cytochrome-p450-metabolism': { type: 'linear_affine', slope: 3.4500, intercept: 0.1200, ref: 3.4500 },
  'urinary-excretion-cumulative-pharmacokinetic-clearance': { type: 'linear_affine', slope: 1.8500, intercept: 0.2000, ref: 1.8500 },
  'oral-bioavailability-area-under-curve-trapezoidal': { type: 'linear_affine', slope: 0.1850, intercept: 2.5000, ref: 0.1850 },
  'drug-excipient-compatibility-differential-scanning-calorimetry': { type: 'linear_affine', slope: -28.5000, intercept: 158.0000, ref: 28.5000, abs_ref: true },
  'topical-gel-in-vitro-franz-cell-skin-permeation': { type: 'linear_affine', slope: 48.5000, intercept: 10.2000, ref: 48.5000 },

  // Module 4: Pharmacology, Toxicology, Pharmacognosy & Sterile Products (Labs 25–31)
  'isolated-ileum-acetylcholine-graded-dose-response': { type: 'linear_affine', slope: 42.0000, intercept: 2.5000, ref: 42.0000 },
  'scherer-schild-regression-competitive-antagonist-pa2': { type: 'linear_prop', slope: 1.0000, ref: 1.0000 },
  'bacterial-endotoxin-gel-clot-limulus-amebocyte-lysate': { type: 'linear_affine', slope: 85.0000, intercept: 2.1000, ref: 85.0000 },
  'heparin-anti-factor-xa-chromogenic-potency': { type: 'linear_affine', slope: -0.7500, intercept: 1.2500, ref: 0.7500, abs_ref: true },
  'phytochemical-alkaloid-acid-base-gravimetric-extraction': { type: 'linear_affine', slope: 64.5000, intercept: 5.0000, ref: 64.5000 },
  'folin-ciocalteu-herbal-flavonoid-antioxidant-spectrophotometry': { type: 'linear_affine', slope: 0.0185, intercept: 0.0150, ref: 0.0185 },
  'particulate-matter-light-obscuration-ophthalmic': { type: 'linear_affine', slope: 1.8200, intercept: 15.0000, ref: 1.8200 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Pharmacy experiment: ' + slug);

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
  return { input: x, raw: y, x: x, y: y };
}

function fit(points){
  if (!points || points.length < 2) return null;
  const n = points.length;
  let sx = 0, sy = 0, sxx = 0, sxy = 0, syy = 0;
  for (let i = 0; i < n; i++) {
    const pt = points[i];
    sx += pt.x;
    sy += pt.y;
    sxx += pt.x * pt.x;
    sxy += pt.x * pt.y;
    syy += pt.y * pt.y;
  }
  const denom = (n * sxx - sx * sx);
  if (Math.abs(denom) < 1e-12) return null;
  const slope = (n * sxy - sx * sy) / denom;
  const intercept = (sy - slope * sx) / n;

  const ssTot = syy - (sy * sy) / n;
  let ssRes = 0;
  for (let i = 0; i < n; i++) {
    const yHat = slope * points[i].x + intercept;
    const res = points[i].y - yHat;
    ssRes += res * res;
  }
  const r2 = ssTot > 1e-12 ? Math.max(0, 1 - (ssRes / ssTot)) : 1.0;
  return { slope: round(slope, 6), intercept: round(intercept, 6), r2: round(r2, 6) };
}

function estimate(slug, fitResult){
  const p = PARAMS[slug];
  if (!p || !fitResult) return { value: 0, reference: 0 };
  let val = fitResult.slope;
  if (p.abs_ref) val = Math.abs(val);
  return { value: round(val, 6), reference: round(p.ref, 6) };
}

const api = { PARAMS, predict, reading, fit, estimate };
if (typeof module !== 'undefined' && module.exports) module.exports = api;
if (typeof root !== 'undefined') root.PharmacyModels = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
