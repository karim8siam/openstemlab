(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {

  'bisection-method-root-convergence': { alpha: 1.0, lnC: 0.0, x0: 1.0, is_bisection: true, is_fixed_point: false, target: 0.500, ref: 0.5 },
  'newton-raphson-quadratic-convergence': { alpha: 2.0, lnC: -1.4979, x0: -0.2693, is_bisection: false, is_fixed_point: false, target: 2.000, ref: 2.0 },
  'secant-method-superlinear-convergence': { alpha: 1.618, lnC: -0.5982, x0: -0.8715, is_bisection: false, is_fixed_point: false, target: 1.618, ref: 1.618 },
  'regula-falsi-false-position-bracketing': { alpha: 1.442, lnC: -1.758, x0: -3.029, is_bisection: false, is_fixed_point: false, target: 1.442, ref: 1.442 },
  'fixed-point-iteration-banach-contraction': { alpha: 1.0, lnC: 0.0, x0: 0.5, is_bisection: false, is_fixed_point: true, target: 0.125, ref: 0.125 },
  'muller-method-complex-polynomial-roots': { alpha: 1.839, lnC: -0.1625, x0: -1.5, is_bisection: false, is_fixed_point: false, target: 1.839, ref: 1.839 },
  'bairstow-method-polynomial-quadratic-factors': { alpha: 2.0, lnC: -0.612, x0: -1.1468, is_bisection: false, is_fixed_point: false, target: 2.000, ref: 2.0 },
  'brent-dekker-hybrid-root-finding': { alpha: 1.839, lnC: -0.1054, x0: -1.4, is_bisection: false, is_fixed_point: false, target: 1.839, ref: 1.839 },
  'halley-method-cubic-root-convergence': { alpha: 3.0, lnC: -0.9163, x0: -1.0, is_bisection: false, is_fixed_point: false, target: 3.000, ref: 3.0 },
  'steffensen-method-accelerated-convergence': { alpha: 2.0, lnC: -0.5877, x0: -1.3, is_bisection: false, is_fixed_point: false, target: 2.000, ref: 2.0 },
};

function predict(slug, input){
  const k = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Mathematics experiment predict: ' + slug);
  const valid = k >= 1.0 && k <= 10.0;
  const step = Math.max(1, Math.min(10, Math.round(k)));

  let x = 0, y = 0, raw = 0;
  if (p.is_bisection) {
    x = step;
    y = -step;
    raw = round(1.0 / Math.pow(2, step), 4);
  } else if (p.is_fixed_point) {
    x = round(p.x0 * Math.pow(0.125, step - 1), 6);
    y = round(0.125 * x, 6);
    raw = round(1.000000 + x, 6);
  } else {
    // Generate x_{step-1}
    let cur_x = p.x0;
    for (let i = 1; i < step; i++) {
      cur_x = p.alpha * cur_x + p.lnC;
    }
    x = round(cur_x, 4);
    y = round(p.alpha * x + p.lnC, 4);
    raw = round(step, 0);
  }
  return { raw, ideal: raw, period: step, x, y, valid };
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
  if (p.is_bisection) {
    const C_est = Math.pow(2, f.m);
    const se = Math.abs(C_est * Math.LN2 * (f.slopeSE || 0.0001));
    return { value: C_est, se: se, reference: p.ref };
  }
  return { value: f.m, se: f.slopeSE || 0.0001, reference: p.ref };
}

const api = { predict, reading, fit, estimate, round };
if (typeof module !== 'undefined' && module.exports) module.exports = api;
else root.MathModels = api;
})(typeof window === 'undefined' ? {} : window);
