(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Group I: Nonlinear Equations
  'bisection-method-root-convergence': { type: 'bisection', ref: 0.500 },
  'newton-raphson-quadratic-convergence': { type: 'order', alpha: 2.000, lnC: -1.4979, x0: -0.2693, ref: 2.000 },
  'secant-method-superlinear-convergence': { type: 'order', alpha: 1.618, lnC: -0.5982, x0: -0.8715, ref: 1.618 },
  'regula-falsi-false-position-bracketing': { type: 'order', alpha: 1.442, lnC: -1.7580, x0: -3.0290, ref: 1.442 },
  'fixed-point-iteration-banach-contraction': { type: 'fixed_point', ref: 0.125 },
  'muller-method-complex-polynomial-roots': { type: 'order', alpha: 1.839, lnC: -0.1625, x0: -1.5000, ref: 1.839 },
  'bairstow-method-polynomial-quadratic-factors': { type: 'order', alpha: 2.000, lnC: -0.6120, x0: -1.1468, ref: 2.000 },
  'brent-dekker-hybrid-root-finding': { type: 'order', alpha: 1.839, lnC: -0.1054, x0: -1.4000, ref: 1.839 },
  'halley-method-cubic-root-convergence': { type: 'order', alpha: 3.000, lnC: -0.9163, x0: -1.0000, ref: 3.000 },
  'steffensen-method-accelerated-convergence': { type: 'order', alpha: 2.000, lnC: -0.5877, x0: -1.3000, ref: 2.000 },

  // Group II: Linear Systems & Matrix Decompositions
  'gaussian-elimination-partial-pivoting': { type: 'cubic_ops', coeff: 2.0/3.0, ref: 0.667 },
  'lu-decomposition-doolittle-crout': { type: 'cubic_ops', coeff: 2.0/3.0, ref: 0.667 },
  'cholesky-decomposition-positive-definite': { type: 'cubic_ops', coeff: 1.0/3.0, ref: 0.333 },
  'jacobi-iterative-linear-solver': { type: 'spectral_radius', rho: 0.500, ref: 0.500 },
  'gauss-seidel-successive-relaxation': { type: 'linear_step', slope: 1.268, ref: 1.268 },
  'power-iteration-dominant-eigenvalue': { type: 'linear_step', slope: 1.500, ref: 1.500 },
  'inverse-power-iteration-eigen-shift': { type: 'order', alpha: 3.000, lnC: -0.9163, x0: -1.0000, ref: 3.000 },
  'qr-decomposition-gram-schmidt-householder': { type: 'cubic_ops', coeff: 4.0/3.0, ref: 1.333 },
  'singular-value-decomposition-pseudoinverse': { type: 'linear_step', slope: 25.000, ref: 25.000 },
  'conjugate-gradient-krylov-optimization': { type: 'linear_step', slope: 0.600, ref: 0.600 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Mathematics experiment predict: ' + slug);

  if (p.type === 'cubic_ops') {
    // Dimension n in [10, 60]
    const valid = inp >= 10.0 && inp <= 60.0;
    const n = Math.max(10, Math.min(60, inp));
    const x = round((n * n * n) / 1000.0, 3);
    const y = round(p.coeff * x, 3);
    const raw = y;
    return { raw, ideal: raw, period: n, x, y, valid };
  }

  if (p.type === 'bisection') {
    const valid = inp >= 1.0 && inp <= 10.0;
    const step = Math.max(1, Math.min(10, Math.round(inp)));
    const x = step;
    const y = -step;
    const raw = round(1.0 / Math.pow(2, step), 4);
    return { raw, ideal: raw, period: step, x, y, valid };
  }

  if (p.type === 'fixed_point') {
    const valid = inp >= 1.0 && inp <= 10.0;
    const step = Math.max(1, Math.min(10, Math.round(inp)));
    const x = round(0.500000 * Math.pow(0.125, step - 1), 6);
    const y = round(0.125 * x, 6);
    const raw = round(1.000000 + x, 6);
    return { raw, ideal: raw, period: step, x, y, valid };
  }

  if (p.type === 'spectral_radius') {
    const valid = inp >= 1.0 && inp <= 10.0;
    const step = Math.max(1, Math.min(10, Math.round(inp)));
    const cur_ln = -1.0000 - (step - 1) * Math.LN2;
    const x = round(cur_ln, 4);
    const y = round(1.0000 * x - Math.LN2, 4);
    const raw = round(Math.exp(x), 6);
    return { raw, ideal: raw, period: step, x, y, valid };
  }

  if (p.type === 'linear_step') {
    const valid = inp >= 1.0 && inp <= 10.0;
    const step = Math.max(1, Math.min(10, Math.round(inp)));
    const x = step;
    const y = round(p.slope * x, 3);
    const raw = y;
    return { raw, ideal: raw, period: step, x, y, valid };
  }

  if (p.type === 'order') {
    const valid = inp >= 1.0 && inp <= 10.0;
    const step = Math.max(1, Math.min(10, Math.round(inp)));
    let cur_x = p.x0;
    for (let i = 1; i < step; i++) {
      cur_x = p.alpha * cur_x + p.lnC;
    }
    const x = round(cur_x, 4);
    const y = round(p.alpha * x + p.lnC, 4);
    const raw = round(step, 0);
    return { raw, ideal: raw, period: step, x, y, valid };
  }

  throw Error('Unknown type for math predict: ' + p.type);
}

function reading(slug, input, raw){
  const p = predict(slug, input);
  return { input: Number(input), raw: Number(raw), x: p.x, y: p.y };
}

function fit(rows){
  if (rows.length < 3 || new Set(rows.map(r => r.x)).size < 3) return null;
  const n = rows.length;
  const mx = rows.reduce((s, r) => s + r.x, 0) / n;
  const my = rows.reduce((s, r) => s + r.y, 0) / n;
  const sxx = rows.reduce((s, r) => s + (r.x - mx)**2, 0);
  const m = rows.reduce((s, r) => s + (r.x - mx) * (r.y - my), 0) / sxx;
  const b = my - m * mx;
  const sse = rows.reduce((s, r) => s + (r.y - m * r.x - b)**2, 0);
  const syy = rows.reduce((s, r) => s + (r.y - my)**2, 0);
  const variance = sse / (n - 2);
  return {
    m, b, sse,
    rms: Math.sqrt(sse / n),
    slopeSE: Math.sqrt(variance / sxx),
    interceptSE: Math.sqrt(variance * (1 / n + mx * mx / sxx)),
    r2: syy > 0 ? 1 - sse / syy : 1
  };
}

function estimate(slug, f){
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Mathematics experiment estimate: ' + slug);
  if (p.type === 'bisection') {
    const C_est = Math.pow(2, f.m);
    const se = Math.abs(C_est * Math.LN2 * (f.slopeSE || 0.0001));
    return { value: C_est, se: se, reference: p.ref };
  }
  if (p.type === 'spectral_radius') {
    const rho_est = Math.exp(f.b);
    const se = Math.abs(rho_est * (f.interceptSE || 0.0001));
    return { value: rho_est, se: se, reference: p.ref };
  }
  return { value: f.m, se: f.slopeSE || 0.0001, reference: p.ref };
}

const api = { predict, reading, fit, estimate, round };
if (typeof module !== 'undefined' && module.exports) module.exports = api;
else root.MathModels = api;
})(typeof window === 'undefined' ? {} : window);
