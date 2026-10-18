(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Geology, Mineralogy & Petrology (Labs 1–5)
  'mohs-hardness-mineral-scratch-indentation': { type: 'linear_affine', slope: 1.4500, intercept: 0.5000, ref: 1.4500 },
  'stokes-sediment-grain-size-settling-velocity': { type: 'linear_affine', slope: 0.2400, intercept: 0.0500, ref: 0.2400 },
  'mineral-specific-gravity-jolly-balance': { type: 'linear_affine', slope: 2.6500, intercept: 0.1500, ref: 2.6500 },
  'snells-law-thin-section-birefringence-petrography': { type: 'linear_affine', slope: 0.0450, intercept: 0.0020, ref: 0.0450 },
  'brinell-rock-compressive-strength-schmidt-hammer': { type: 'linear_affine', slope: 1.8500, intercept: 15.0000, ref: 1.8500 },

  // Module 2: Geophysics, Seismology & Plate Tectonics (Labs 6–10)
  'seismic-p-s-travel-time-epicenter-distance': { type: 'linear_affine', slope: 8.2500, intercept: 12.0000, ref: 8.2500 },
  'wadati-benioff-seismic-velocity-ratio': { type: 'linear_affine', slope: 1.7320, intercept: 0.0500, ref: 1.7320 },
  'paleomagnetic-seafloor-spreading-vine-matthews': { type: 'linear_affine', slope: 24.5000, intercept: 5.0000, ref: 24.5000 },
  'free-air-gravity-bouguer-anomaly-elevation': { type: 'linear_affine', slope: -0.1119, intercept: 2.4000, ref: 0.1119, abs_ref: true },
  'resistivity-vertical-electrical-sounding-schlumberger': { type: 'linear_affine', slope: 4.5000, intercept: 25.0000, ref: 4.5000 },

  // Module 3: Planetary Sciences, Celestial Mechanics & Telescopes (Labs 11–16)
  'keplers-third-law-orbital-harmonic-resonance': { type: 'linear_prop', slope: 1.0000, ref: 1.0000 },
  'telescope-resolving-power-rayleigh-criterion': { type: 'linear_affine', slope: 0.1380, intercept: 0.0200, ref: 0.1380 },
  'hertzsprung-russell-stellar-parallax-distance': { type: 'linear_affine', slope: 3.2616, intercept: 0.0000, ref: 3.2616 },
  'hubbles-law-galaxy-redshift-expansion': { type: 'linear_affine', slope: 70.4000, intercept: 15.0000, ref: 70.4000 },
  'stefan-boltzmann-blackbody-radiation-temperature': { type: 'linear_affine', slope: 5.6704, intercept: 1.2000, ref: 5.6704 },
  'solar-limb-darkening-photometric-profile': { type: 'linear_affine', slope: 0.6400, intercept: 0.3600, ref: 0.6400 },

  // Module 4: Atmospheric Sciences, Climatology & Remote Sensing (Labs 17–21)
  'barometric-hypsometric-atmospheric-lapse-rate': { type: 'linear_affine', slope: -0.0065, intercept: 15.0000, ref: 0.0065, abs_ref: true },
  'greenhouse-gas-infrared-absorption-beer-lambert': { type: 'linear_affine', slope: 0.0850, intercept: 0.0150, ref: 0.0850 },
  'coriolis-deflection-planetary-vorticity-geostrophic': { type: 'linear_affine', slope: 1.4580, intercept: 0.0200, ref: 1.4580 },
  'landsat-ndvi-multispectral-vegetation-reflectance': { type: 'linear_affine', slope: 0.8500, intercept: -0.1200, ref: 0.8500 },
  'radar-doppler-tropospheric-wind-profiling': { type: 'linear_affine', slope: 2.4500, intercept: 5.0000, ref: 2.4500 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Earth & Space experiment: ' + slug);

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
if (typeof root !== 'undefined') root.EarthSpaceModels = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
