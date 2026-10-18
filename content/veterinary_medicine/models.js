(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Veterinary Hematology, Urinalysis & Clinical Pathology (Labs 1–8)
  'canine-microhematocrit-packed-cell-volume-refractometry': { type: 'linear_affine', slope: 6.5000, intercept: 12.0000, ref: 6.5000 },
  'feline-complete-blood-count-hemocytometer-erythrocyte': { type: 'linear_affine', slope: 0.3200, intercept: 0.4000, ref: 0.3200 },
  'equine-peritoneal-fluid-refractometric-total-protein': { type: 'linear_affine', slope: 18.2000, intercept: 4.5000, ref: 18.2000 },
  'canine-urinalysis-refractometric-specific-gravity': { type: 'linear_affine', slope: 0.6500, intercept: 2.0000, ref: 0.6500 },
  'veterinary-blood-gas-potentiometric-pco2-henderson-hasselbalch': { type: 'linear_affine', slope: -0.5850, intercept: 88.0000, ref: 0.5850, abs_ref: true },
  'avian-reptilian-natt-herrick-manual-thrombocyte-count': { type: 'linear_affine', slope: 0.4400, intercept: 2.2000, ref: 0.4400 },
  'bovine-mastitis-california-mastitis-test-somatic-cell': { type: 'linear_affine', slope: 1.7500, intercept: 4.2000, ref: 1.7500 },
  'canine-pancreatic-lipase-immunoreactivity-elisa': { type: 'linear_affine', slope: 1.8500, intercept: 45.0000, ref: 1.8500 },

  // Module 2: Veterinary Parasitology, Microbiology & Immunology (Labs 9–16)
  'mcmaster-chamber-fecal-egg-count-nematode': { type: 'linear_affine', slope: 14.0000, intercept: 3.0000, ref: 14.0000 },
  'baermann-technique-lungworm-larval-sedimentation': { type: 'linear_affine', slope: 3.2000, intercept: 2.5000, ref: 3.2000 },
  'modified-knott-test-microfilariae-concentration': { type: 'linear_affine', slope: 26.0000, intercept: 4.0000, ref: 26.0000 },
  'kirby-bauer-veterinary-antibiotic-zone-inhibition': { type: 'linear_affine', slope: 1.1500, intercept: 12.4000, ref: 1.1500 },
  'veterinary-bacterial-colony-cfu-serial-dilution': { type: 'linear_affine', slope: -18.5000, intercept: 138.0000, ref: 18.5000, abs_ref: true },
  'canine-parvovirus-fecal-antigen-lateral-flow': { type: 'linear_affine', slope: 7.4000, intercept: 25.0000, ref: 7.4000 },
  'bovine-brucellosis-rose-bengal-agglutination': { type: 'linear_affine', slope: 0.1250, intercept: 0.8500, ref: 0.1250 },
  'equine-infectious-anemia-coggins-agar-gel-diffusion': { type: 'linear_affine', slope: 0.0850, intercept: 0.4500, ref: 0.0850 },

  // Module 3: Veterinary Pharmacology, Anesthesiology & Toxicology (Labs 17–24)
  'veterinary-propofol-anesthetic-induction-dose-mac': { type: 'linear_affine', slope: 11.5000, intercept: 6.0000, ref: 11.5000 },
  'isoflurane-minimum-alveolar-concentration-mac-canine': { type: 'linear_affine', slope: 0.8800, intercept: 0.0800, ref: 0.8800 },
  'veterinary-xylazine-alpha2-adrenergic-sedation-reversal': { type: 'linear_affine', slope: 38.0000, intercept: 4.5000, ref: 38.0000 },
  'canine-theobromine-chocolate-toxicity-toxicokinetics': { type: 'linear_affine', slope: 0.8200, intercept: 2.5000, ref: 0.8200 },
  'rodenticide-anticoagulant-prothrombin-time-prolongation': { type: 'linear_affine', slope: 1.4500, intercept: 8.5000, ref: 1.4500 },
  'organophosphate-toxicity-blood-cholinesterase-inhibition': { type: 'linear_affine', slope: -0.1850, intercept: 9.8000, ref: 0.1850, abs_ref: true },
  'veterinary-nsaid-cyclooxygenase-inhibition-assay': { type: 'linear_affine', slope: -420.0000, intercept: 780.0000, ref: 420.0000, abs_ref: true },
  'feline-methimazole-hyperthyroidism-t4-radioimmunoassay': { type: 'linear_affine', slope: -14.5000, intercept: 135.0000, ref: 14.5000, abs_ref: true },

  // Module 4: Large Animal, Reproduction & Surgery/Diagnostics (Labs 25–31)
  'bovine-rumen-fluid-volatile-fatty-acids-titration': { type: 'linear_affine', slope: 1.2800, intercept: 55.0000, ref: 1.2800 },
  'bovine-milk-progesterone-ovulation-timing-elisa': { type: 'linear_affine', slope: 1.3500, intercept: -1.2000, ref: 1.3500 },
  'equine-semen-progressive-motility-computer-assisted': { type: 'linear_affine', slope: -8.4000, intercept: 115.0000, ref: 8.4000, abs_ref: true },
  'canine-electrocardiogram-mean-electrical-axis': { type: 'linear_affine', slope: 75.0000, intercept: 25.0000, ref: 75.0000 },
  'veterinary-orthopedic-bone-plate-four-point-bending': { type: 'linear_affine', slope: 0.00165, intercept: 0.0500, ref: 0.00165 },
  'equine-joint-synovial-fluid-mucin-clot-viscosity': { type: 'linear_affine', slope: 2.2500, intercept: 0.8000, ref: 2.2500 },
  'canine-craniocaudal-stifle-drawer-joint-laxity': { type: 'linear_affine', slope: 0.1450, intercept: 0.8500, ref: 0.1450 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Veterinary experiment: ' + slug);

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
if (typeof root !== 'undefined') root.VeterinaryModels = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
