(function(root){
'use strict';
const round=(v,n)=>Math.round((v+Number.EPSILON)*10**n)/10**n;

const PARAMS = {
  // Module 1: Descriptive Statistics, EDA & Sampling Distributions (Labs 1–11)
  'sample-moments-skewness-kurtosis': { type: 'linear_affine', slope: 1.000, intercept: 1.000, ref: 1.000 },
  'kernel-density-estimation-bandwidth': { type: 'log_power', alpha: -0.200, lnC: 0.8000, ref: -0.200 },
  'empirical-cumulative-distribution-ecdf': { type: 'log_power', alpha: -0.500, lnC: 1.2000, ref: -0.500 },
  'box-plot-tukey-fences-outliers': { type: 'linear_prop', slope: 1.349, ref: 1.349 },
  'chebyshev-markov-probability-bounds': { type: 'log_power', alpha: -2.000, lnC: 0.0000, ref: -2.000 },
  'law-of-large-numbers-weak-strong': { type: 'linear_prop', slope: 1.000, ref: 1.000 },
  'central-limit-theorem-lindeberg-levy': { type: 'log_power', alpha: -0.500, lnC: 1.0000, ref: -0.500 },
  'bivariate-correlation-spearman-pearson': { type: 'linear_prop', slope: 1.000, ref: 1.000 },
  'order-statistics-sample-quantiles': { type: 'linear_prop', slope: 0.125, ref: 0.125 },
  'bootstrap-resampling-confidence-intervals': { type: 'log_power', alpha: -0.500, lnC: 1.5000, ref: -0.500 },
  'jackknife-pseudovalues-bias-reduction': { type: 'linear_prop', slope: 1.000, ref: 1.000 },

  // Module 2: Classical Probability Distributions & Stochastic Simulations (Labs 12–22)
  'bernoulli-binomial-hypergeometric': { type: 'linear_prop', slope: 0.240, ref: 0.240 },
  'poisson-process-exponential-waiting': { type: 'linear_prop', slope: 1.000, ref: 1.000 },
  'geometric-negative-binomial-trials': { type: 'linear_prop', slope: 2.000, ref: 2.000 },
  'normal-gaussian-error-function': { type: 'linear_prop', slope: 2.355, ref: 2.355 },
  'gamma-erlang-chi-squared-family': { type: 'linear_prop', slope: 2.000, ref: 2.000 },
  'student-t-distribution-heavy-tails': { type: 'linear_prop', slope: 2.000, ref: 2.000 },
  'snedecor-f-distribution-variance-ratio': { type: 'linear_affine', slope: 0.500, intercept: -1.000, ref: 0.500 },
  'weibull-distribution-reliability-hazard': { type: 'log_power', alpha: 2.000, lnC: -1.8326, ref: 2.000 },
  'beta-distribution-bayesian-conjugate': { type: 'linear_prop', slope: 4.000, ref: 4.000 },
  'multinomial-distribution-joint-sampling': { type: 'linear_prop', slope: 0.060, ref: 0.060 },
  'inverse-transform-rejection-sampling': { type: 'linear_prop', slope: 1.500, ref: 1.500 },

  // Module 3: Statistical Inference, Estimation & Hypothesis Testing (Labs 23–33)
  'maximum-likelihood-estimation-mle': { type: 'linear_prop', slope: 2.000, ref: 2.000 },
  'method-of-moments-parameter-fitting': { type: 'linear_prop', slope: 1.000, ref: 1.000 },
  'cramer-rao-lower-bound-efficiency': { type: 'linear_prop', slope: 1.000, ref: 1.000 },
  'single-sample-z-and-t-hypothesis-tests': { type: 'linear_prop', slope: 2.000, ref: 2.000 },
  'two-sample-welch-t-test-unequal-variance': { type: 'linear_prop', slope: 2.500, ref: 2.500 },
  'paired-samples-t-test-matched-pairs': { type: 'linear_prop', slope: 5.000, ref: 5.000 },
  'chi-squared-goodness-of-fit-pearson': { type: 'linear_prop', slope: 2.400, ref: 2.400 },
  'chi-squared-contingency-independence': { type: 'linear_prop', slope: 0.040, ref: 0.040 },
  'one-way-anova-f-test-homogeneity': { type: 'linear_prop', slope: 1.500, ref: 1.500 },
  'two-way-anova-factorial-interactions': { type: 'linear_prop', slope: 3.000, ref: 3.000 },
  'nonparametric-mann-whitney-wilcoxon': { type: 'linear_prop', slope: 5.000, ref: 5.000 },

  // Module 4: Regression Modeling, Bayesian Inference & Advanced Stochastic Processes (Labs 34–44)
  'simple-linear-regression-ols-gauss-markov': { type: 'linear_prop', slope: 0.500, ref: 0.500 },
  'multiple-linear-regression-multicollinearity': { type: 'linear_prop', slope: 0.250, ref: 0.250 },
  'logistic-regression-binary-odds-ratio': { type: 'linear_affine', slope: 0.800, intercept: -2.000, ref: 0.800 },
  'polynomial-regression-bias-variance-tradeoff': { type: 'linear_prop', slope: 0.200, ref: 0.200 },
  'ridge-and-lasso-shrinkage-regularization': { type: 'linear_prop', slope: 1.000, ref: 1.000 },
  'bayes-theorem-conjugate-updating': { type: 'linear_prop', slope: 1.000, ref: 1.000 },
  'markov-chain-transition-stationary-distribution': { type: 'linear_prop', slope: 0.693, ref: 0.693 },
  'metropolis-hastings-mcmc-sampling': { type: 'log_power', alpha: -0.500, lnC: 1.2000, ref: -0.500 },
  'autoregressive-ar1-time-series-stationarity': { type: 'linear_prop', slope: 0.511, ref: 0.511 },
  'principal-component-analysis-covariance-svd': { type: 'linear_prop', slope: 0.400, ref: 0.400 },
  'receiver-operating-characteristic-confusion-matrix': { type: 'linear_prop', slope: 1.000, ref: 1.000 }
};

function predict(slug, input){
  const inp = Number(input);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Statistics experiment predict: ' + slug);

  if (p.type === 'log_power') {
    const x = Math.log(inp);
    const y = p.alpha * x + p.lnC;
    const raw = Math.exp(y);
    return { valid: true, raw: round(raw, 5), x: round(x, 4), y: round(y, 4) };
  }

  if (p.type === 'linear_affine') {
    const x = inp;
    const y = p.slope * x + (p.intercept || 0);
    return { valid: true, raw: round(y, 4), x: round(x, 4), y: round(y, 4) };
  }

  if (p.type === 'linear_prop') {
    const x = inp;
    const y = p.slope * x;
    return { valid: true, raw: round(y, 4), x: round(x, 4), y: round(y, 4) };
  }

  throw Error('Unknown parameter type: ' + p.type);
}

function reading(slug, input, raw){
  const inp = Number(input);
  const r = Number(raw);
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Statistics experiment reading: ' + slug);

  if (p.type === 'log_power') {
    const x = round(Math.log(inp), 4);
    const y = round(p.alpha * x + p.lnC, 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  if (p.type === 'linear_affine') {
    const x = round(inp, 4);
    const y = round(p.slope * x + (p.intercept || 0), 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  if (p.type === 'linear_prop') {
    const x = round(inp, 4);
    const y = round(p.slope * x, 4);
    return { input: inp, raw: r, x: x, y: y };
  }

  throw Error('Unknown parameter type: ' + p.type);
}

function fit(rows){
  if (!rows || rows.length < 3) return null;
  const n = rows.length;
  let sx = 0, sy = 0, sxx = 0, syy = 0, sxy = 0;
  for (let i = 0; i < n; i++) {
    const x = rows[i].x, y = rows[i].y;
    sx += x; sy += y;
    sxx += x * x; syy += y * y;
    sxy += x * y;
  }
  const denom = n * sxx - sx * sx;
  if (Math.abs(denom) < 1e-12) return null;
  const m = (n * sxy - sx * sy) / denom;
  const b = (sy - m * sx) / n;
  const numR = n * sxy - sx * sy;
  const denR = Math.sqrt(Math.max(0, (n * sxx - sx * sx) * (n * syy - sy * sy)));
  const r2 = denR > 1e-12 ? Math.min(1.0, (numR / denR) ** 2) : 1.0;
  let ssRes = 0;
  for (let i = 0; i < n; i++) {
    const yHat = m * rows[i].x + b;
    ssRes += (rows[i].y - yHat) ** 2;
  }
  const se = n > 2 ? Math.sqrt(ssRes / (n - 2) / (sxx - sx * sx / n)) : 0;
  return { m, b, r2, se, n };
}

function estimate(slug, fitRes){
  const p = PARAMS[slug];
  if (!p) throw Error('Unknown Statistics experiment estimate: ' + slug);
  const targetSlope = p.ref;
  return {
    value: fitRes.m,
    reference: targetSlope,
    se: fitRes.se || 0.00001
  };
}

const api = {
  PARAMS,
  predict,
  reading,
  fit,
  estimate
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = api;
}
if (typeof root !== 'undefined') {
  root.StatsModels = api;
}

})(typeof globalThis !== 'undefined' ? globalThis : this);
