(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Cell Biology & Biomembrane Transport (Labs 1–6)
  'microscope-micrometry-cell-size-calibration': { type: 'linear_prop', slope: 2.5000, ref: 2.5000 },
  'osmosis-dialysis-tubing-sucrose-water-potential': { type: 'linear_prop', slope: 0.0550, ref: 0.0550 },
  'plant-cell-plasmolysis-incipient-osmotic-pressure': { type: 'linear_affine', slope: 18.0000, intercept: -15.0000, ref: 18.0000 },
  'erythrocyte-hemolysis-solute-permeability-overton': { type: 'linear_prop', slope: 1.4500, ref: 1.4500 },
  'mitotic-index-allium-cepa-cell-cycle-kinetics': { type: 'linear_affine', slope: 0.8500, intercept: 2.2000, ref: 0.8500 },
  'chloroplast-hill-reaction-dcip-photoreduction': { type: 'linear_prop', slope: 0.0028, ref: 0.0028 },

  // Module 2: Enzymology & Cellular Metabolism (Labs 7–12)
  'catalase-enzyme-kinetics-substrate-concentration': { type: 'linear_prop', slope: 0.4200, ref: 0.4200 },
  'temperature-coefficient-q10-enzyme-catalysis': { type: 'linear_affine', slope: 0.0750, intercept: 0.1500, ref: 0.0750 },
  'ph-optimum-salivary-amylase-starch-digestion': { type: 'linear_affine', slope: -0.1800, intercept: 1.8500, ref: 0.1800, abs_ref: true },
  'yeast-fermentation-rate-durham-tube-respirometry': { type: 'linear_prop', slope: 0.3500, ref: 0.3500 },
  'cellular-respiration-germinating-seeds-respirometer': { type: 'linear_prop', slope: 0.0820, ref: 0.0820 },
  'succinate-dehydrogenase-mitochondrial-electron-transport': { type: 'linear_affine', slope: -0.0150, intercept: 0.2800, ref: 0.0150, abs_ref: true },

  // Module 3: Molecular Biology & Genetics (Labs 13–18)
  'agarose-gel-electrophoresis-dna-fragment-migration': { type: 'linear_affine', slope: -15.5000, intercept: 85.0000, ref: 15.5000, abs_ref: true },
  'spectrophotometric-dna-quantification-purity-ratio': { type: 'linear_prop', slope: 50.0000, ref: 50.0000 },
  'bacterial-transformation-plasmid-competent-efficiency': { type: 'linear_prop', slope: 1.2500, ref: 1.2500 },
  'mendelian-dihybrid-cross-drosophila-chi-square': { type: 'linear_prop', slope: 1.0000, ref: 1.0000 },
  'polytene-chromosome-puff-transcription-mapping': { type: 'linear_prop', slope: 0.4500, ref: 0.4500 },
  'pcr-amplification-cycle-efficiency-kinetics': { type: 'linear_affine', slope: 0.3010, intercept: 1.2000, ref: 0.3010 },

  // Module 4: Microbiology & Microbial Physiology (Labs 19–24)
  'bacterial-growth-curve-turbidimetric-spectrophotometry': { type: 'linear_affine', slope: 0.0185, intercept: 0.0500, ref: 0.0185 },
  'serial-dilution-pour-plate-colony-forming-units': { type: 'linear_prop', slope: 1.0000, ref: 1.0000 },
  'gram-staining-peptidoglycan-cell-wall-differentiation': { type: 'linear_affine', slope: -0.0450, intercept: 0.9500, ref: 0.0450, abs_ref: true },
  'bacteriophage-plaque-assay-titer-quantification': { type: 'linear_prop', slope: 0.8500, ref: 0.8500 },
  'nitrogen-fixation-acetylene-reduction-rhizobium': { type: 'linear_prop', slope: 3.2000, ref: 3.2000 },
  'bacterial-motility-soft-agar-chemotaxis-gradient': { type: 'linear_prop', slope: 0.6500, ref: 0.6500 },

  // Module 5: Plant Physiology & Ecology (Labs 25–30)
  'photosynthetic-light-response-curve-light-saturation': { type: 'linear_prop', slope: 0.0520, ref: 0.0520 },
  'potometer-transpiration-rate-vpd-environmental-stress': { type: 'linear_prop', slope: 0.4800, ref: 0.4800 },
  'stomata-density-conductance-carbon-dioxide-diffusion': { type: 'linear_prop', slope: 0.0035, ref: 0.0035 },
  'plant-pigment-rf-values-paper-chromatography': { type: 'linear_prop', slope: 0.0100, ref: 0.0100 },
  'seed-dormancy-gibberellic-acid-alpha-amylase-induction': { type: 'linear_affine', slope: 12.5000, intercept: 8.0000, ref: 12.5000 },
  'plankton-primary-productivity-light-dark-bottle-winkler': { type: 'linear_prop', slope: 0.3750, ref: 0.3750 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Biological Sciences experiment: ' + slug);

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
  root.BiologicalModels = api;
}
})(typeof window !== 'undefined' ? window : globalThis);
