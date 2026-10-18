(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Physical Oceanography, Waves & Currents (Labs 1–6)
  'practical-salinity-scale-conductometric-salinometer': { type: 'linear_affine', slope: 35.0000, intercept: 0.1500, ref: 35.0000 },
  'seawater-density-equation-of-state-temperature': { type: 'linear_affine', slope: -0.2850, intercept: 28.5000, ref: 0.2850, abs_ref: true },
  'shallow-water-wave-celerity-depth-dispersion': { type: 'linear_affine', slope: 3.1320, intercept: 0.2500, ref: 3.1320 },
  'ekman-spiral-wind-drift-surface-current': { type: 'linear_affine', slope: 0.0250, intercept: 0.0100, ref: 0.0250 },
  'seawater-sound-velocity-temperature-depth-profile': { type: 'linear_affine', slope: 4.5600, intercept: 1449.2000, ref: 4.5600 },
  'coastal-tidal-resonance-harmonic-analysis': { type: 'linear_affine', slope: 1.8500, intercept: 0.4000, ref: 1.8500 },

  // Module 2: Chemical Oceanography & Biogeochemical Cycles (Labs 7–11)
  'winkler-dissolved-oxygen-iodometric-titration': { type: 'linear_affine', slope: 1.4000, intercept: 0.1000, ref: 1.4000 },
  'ocean-acidification-seawater-carbonate-alkalinity': { type: 'linear_affine', slope: -0.0450, intercept: 2.4500, ref: 0.0450, abs_ref: true },
  'marine-soluble-reactive-phosphate-molybdenum-blue': { type: 'linear_affine', slope: 0.0385, intercept: 0.0050, ref: 0.0385 },
  'seawater-nitrate-reduction-cadmium-spectrophotometry': { type: 'linear_affine', slope: 0.0245, intercept: 0.0080, ref: 0.0245 },
  'oceanic-dissolved-silicate-silicomolybdate-spectrophotometry': { type: 'linear_affine', slope: 0.0182, intercept: 0.0060, ref: 0.0182 },

  // Module 3: Biological Oceanography & Marine Ecology (Labs 12–16)
  'chlorophyll-a-trichromatic-spectrophotometric-assay': { type: 'linear_affine', slope: 11.8500, intercept: 0.0500, ref: 11.8500 },
  'secchi-disk-seawater-turbidity-photic-zone': { type: 'linear_affine', slope: 1.7000, intercept: 0.1000, ref: 1.7000 },
  'marine-bacterial-respiration-microbial-loop': { type: 'linear_affine', slope: -0.1250, intercept: 8.5000, ref: 0.1250, abs_ref: true },
  'benthic-intertidal-quadrat-species-diversity': { type: 'linear_affine', slope: 0.3800, intercept: 0.8500, ref: 0.3800 },
  'zooplankton-settling-volume-biomass-abundance': { type: 'linear_affine', slope: 1.6500, intercept: 0.5000, ref: 1.6500 },

  // Module 4: Marine Geology, Coastal Processes & Instrumentation (Labs 17–21)
  'coastal-beach-profile-emery-rod-sedimentation': { type: 'linear_affine', slope: 0.0450, intercept: 0.0100, ref: 0.0450 },
  'marine-sediment-porosity-gravimetric-water-content': { type: 'linear_affine', slope: -0.0125, intercept: 0.7500, ref: 0.0125, abs_ref: true },
  'acoustic-doppler-current-profiler-adcp-discharge': { type: 'linear_affine', slope: 0.0325, intercept: 0.0500, ref: 0.0325 },
  'coastal-longshore-current-tracer-dispersion': { type: 'linear_affine', slope: 0.1450, intercept: 0.0200, ref: 0.1450 },
  'ctd-rosette-conductivity-temperature-depth-profiler': { type: 'linear_affine', slope: 0.9850, intercept: 0.0100, ref: 0.9850 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Marine & Ocean experiment: ' + slug);

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
if (typeof root !== 'undefined') root.MarineOceanModels = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
