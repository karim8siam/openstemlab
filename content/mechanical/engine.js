'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.MechanicalModels;
const $ = id => document.getElementById(id);
const fmt = (v, n=4) => Math.abs(v) > 0 && (Math.abs(v) < 0.001 || Math.abs(v) >= 1e6) ? v.toExponential(3) : v.toFixed(n);

let rows = [];
let measurement = null;
let busy = false;
let currentSimMode = 'bench';

try {
  const saved = JSON.parse(localStorage.getItem('openstemlab-' + cfg.slug + '-v1') || '[]');
  if (Array.isArray(saved)) {
    rows = saved.filter(r => r && Number.isFinite(r.input) && r.input >= cfg.min && r.input <= cfg.max && Number.isFinite(r.raw))
                .slice(0, 100)
                .map(r => model.reading(cfg.slug, r.input, r.raw));
  }
} catch (e) {}

function params() {
  return { input: +$('independent').value };
}

function message(text, error=false) {
  const st = $('trialStatus');
  if (!st) return;
  st.textContent = text;
  st.classList.toggle('error', error);
}

function update() {
  const p = params();
  measurement = null;
  if ($('independentOut')) $('independentOut').textContent = p.input.toFixed(cfg.inputDecimals) + ' ' + cfg.inputUnit;
  if ($('readingValue')) $('readingValue').textContent = '—';
  if ($('recordReading')) $('recordReading').disabled = true;
  if ($('measure')) $('measure').disabled = busy;
  if ($('liveState')) $('liveState').textContent = 'Ready to sample with ' + cfg.shortInput + ' = ' + p.input + ' ' + cfg.inputUnit + '.';
  message('Adjust ' + cfg.shortInput + ', then execute mechanical testing trial.');
  draw();
}

if ($('independent')) $('independent').addEventListener('input', () => {
  if ($('independentNumber')) $('independentNumber').value = $('independent').value;
  update();
});

if ($('independentNumber')) {
  $('independentNumber').addEventListener('input', () => {
    const v = +$('independentNumber').value;
    if ($('independentNumber').value !== '' && Number.isFinite(v) && v >= cfg.min && v <= cfg.max) {
      if ($('independent')) $('independent').value = v;
      update();
    }
  });
  $('independentNumber').addEventListener('change', () => {
    const v = +$('independentNumber').value;
    if (!Number.isFinite(v) || v < cfg.min || v > cfg.max) {
      $('independentNumber').value = $('independent').value;
      update();
    }
  });
}

function setSimMode(mode) {
  currentSimMode = mode;
  document.querySelectorAll('.sim-mode-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.mode === mode);
  });
  const notice = $('simModeNotice');
  if (notice) {
    if (mode === 'bench') notice.textContent = 'Hardware Bench: Standard mechanical test frame and calibrated electronic instrumentation.';
    else if (mode === 'compare') notice.textContent = 'Analytical Compare: Direct comparison against classical continuum mechanics and FEA benchmarks.';
    else if (mode === 'sandbox') notice.textContent = 'Mechanical Sandbox: Extended multi-variable load, temperature, and kinematic parameter tuning.';
  }
  draw();
}

document.querySelectorAll('.sim-mode-btn').forEach(btn => {
  btn.addEventListener('click', () => setSimMode(btn.dataset.mode));
});

if ($('measure')) $('measure').addEventListener('click', () => {
  if (busy) return;
  busy = true;
  $('measure').disabled = true;
  if ($('recordReading')) $('recordReading').disabled = true;
  message('Applying mechanical excitation and acquiring load cell telemetry…');
  if ($('readingValue')) $('readingValue').textContent = 'Sampling…';

  let step = 0;
  const timer = setInterval(() => {
    step++;
    draw(step);
    if (step >= 5) {
      clearInterval(timer);
      busy = false;
      const p = params();
      const pred = model.predict(cfg.slug, p.input);
      measurement = pred.raw;
      if ($('readingValue')) $('readingValue').textContent = pred.displayed.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit;
      if ($('recordReading')) $('recordReading').disabled = false;
      if ($('measure')) $('measure').disabled = false;
      if ($('liveState')) $('liveState').textContent = 'Acquisition completed: ' + cfg.depName + ' = ' + pred.displayed.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit + '.';
      message('Telemetry stabilized. Log observation into laboratory dataset table.');
      draw();
    }
  }, 100);
});

if ($('recordReading')) $('recordReading').addEventListener('click', () => {
  if (measurement === null) return;
  const p = params();
  const entry = model.reading(cfg.slug, p.input, measurement);
  rows.push(entry);
  try {
    localStorage.setItem('openstemlab-' + cfg.slug + '-v1', JSON.stringify(rows));
  } catch (e) {}
  $('recordReading').disabled = true;
  message('Observation recorded (' + rows.length + ' total samples in dataset).');
  renderTable();
});

if ($('clearData')) $('clearData').addEventListener('click', () => {
  if (confirm('Clear all logged mechanical trials from this session?')) {
    rows = [];
    try {
      localStorage.removeItem('openstemlab-' + cfg.slug + '-v1');
    } catch (e) {}
    renderTable();
    message('Dataset cleared.');
    update();
  }
});

function renderTable() {
  const tbody = $('dataTableBody');
  if (tbody) {
    tbody.innerHTML = '';
    rows.forEach((r, idx) => {
      const tr = document.createElement('tr');
      tr.innerHTML = '<td>' + (idx + 1) + '</td>' +
                     '<td>' + r.input.toFixed(cfg.inputDecimals) + '</td>' +
                     '<td>' + r.raw.toFixed(cfg.rawDecimals) + '</td>' +
                     '<td>' + (r.x * cfg.xScale).toFixed(3) + '</td>' +
                     '<td>' + (r.y * cfg.yScale).toFixed(3) + '</td>';
      tbody.appendChild(tr);
    });
  }

  const fitRes = model.fit(rows);
  const fitBox = $('fitResult');
  if (fitBox) {
    if (fitRes && fitRes.n >= 3) {
      const est = model.estimate(cfg.slug, fitRes);
      fitBox.innerHTML = '<strong>' + cfg.targetName + ': ' + fmt(est.value, cfg.resultDecimals) + ' ' + cfg.resultUnit + '</strong>' +
                         '<p class="report-equation">Linear fit: <em>y</em> = ' + fmt(fitRes.slope, 4) + ' <em>x</em> ' + (fitRes.intercept >= 0 ? '+ ' : '- ') + fmt(Math.abs(fitRes.intercept), 4) + '</p>' +
                         '<p>Correlation coefficient: <em>R</em>² = ' + fitRes.r2.toFixed(6) + ' (<em>N</em> = ' + fitRes.n + ')</p>' +
                         '<p>Error vs Reference: ' + est.errorPercent.toFixed(3) + '% | Reference benchmark: ' + cfg.refValue + ' ' + cfg.resultUnit + '</p>';
    } else {
      fitBox.innerHTML = '<p>Log at least 3 distinct observations to compute regression fit and mechanical parameter.</p>';
    }
  }

  drawPlot(fitRes);
}

function drawPlot(fitRes) {
  const svg = $('labPlot');
  if (!svg) return;
  const W = 520, H = 260;
  const pad = { left: 65, right: 25, top: 25, bottom: 45 };
  const pw = W - pad.left - pad.right;
  const ph = H - pad.top - pad.bottom;

  let minX = 0, maxX = cfg.emptyX || 10;
  let minY = 0, maxY = cfg.emptyY || 10;

  if (rows.length > 0) {
    const xs = rows.map(r => r.x * cfg.xScale);
    const ys = rows.map(r => r.y * cfg.yScale);
    minX = Math.min(0, Math.min(...xs));
    maxX = Math.max(...xs) * 1.15 || 10;
    minY = Math.min(0, Math.min(...ys));
    maxY = Math.max(...ys) * 1.15 || 10;
  }

  const tx = x => pad.left + ((x - minX) / (maxX - minX || 1)) * pw;
  const ty = y => pad.top + ph - ((y - minY) / (maxY - minY || 1)) * ph;

  let s = '<rect width="' + W + '" height="' + H + '" fill="#0c0a09" rx="6"/>';

  // Grid
  for (let i = 0; i <= 5; i++) {
    const gx = minX + (maxX - minX) * (i / 5);
    const gy = minY + (maxY - minY) * (i / 5);
    s += '<line x1="' + tx(gx) + '" y1="' + pad.top + '" x2="' + tx(gx) + '" y2="' + (pad.top + ph) + '" stroke="#292524" stroke-dasharray="2,2"/>';
    s += '<line x1="' + pad.left + '" y1="' + ty(gy) + '" x2="' + (pad.left + pw) + '" y2="' + ty(gy) + '" stroke="#292524" stroke-dasharray="2,2"/>';
    s += '<text x="' + tx(gx) + '" y="' + (H - 12) + '" fill="#a8a29e" font-size="9" text-anchor="middle">' + fmt(gx, 1) + '</text>';
    s += '<text x="' + (pad.left - 8) + '" y="' + (ty(gy) + 3) + '" fill="#a8a29e" font-size="9" text-anchor="end">' + fmt(gy, 1) + '</text>';
  }

  // Regression line
  if (fitRes && fitRes.n >= 2) {
    const x1 = minX;
    const y1 = (fitRes.slope * (x1 / cfg.xScale) + fitRes.intercept) * cfg.yScale;
    const x2 = maxX;
    const y2 = (fitRes.slope * (x2 / cfg.xScale) + fitRes.intercept) * cfg.yScale;
    s += '<line x1="' + tx(x1) + '" y1="' + ty(y1) + '" x2="' + tx(x2) + '" y2="' + ty(y2) + '" stroke="#f59e0b" stroke-width="2"/>';
  }

  // Data points
  rows.forEach(r => {
    const px = tx(r.x * cfg.xScale);
    const py = ty(r.y * cfg.yScale);
    s += '<circle cx="' + px + '" cy="' + py + '" r="4.5" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>';
  });

  // Labels
  s += '<text x="' + (W / 2) + '" y="' + (H - 2) + '" fill="#fde68a" font-size="10" text-anchor="middle">' + cfg.xLabel + '</text>';
  s += '<text transform="rotate(-90)" x="' + (-H / 2) + '" y="16" fill="#fde68a" font-size="10" text-anchor="middle">' + cfg.yLabel + '</text>';

  svg.innerHTML = s;
}

function draw(animStep=0) {
  const svg = $('visualSvg');
  if (!svg) return;
  const p = params();
  const pred = model.predict(cfg.slug, p.input);
  const frac = Math.min(1, Math.max(0, (p.input - cfg.min) / (cfg.max - cfg.min || 1)));

  let html = '<rect width="520" height="280" fill="#0c0a09" rx="6"/>';

  if (currentSimMode === 'compare') {
    // Split screen: Experimental Mechanical Testing vs FEA / Analytical Benchmark
    html += '<line x1="260" y1="20" x2="260" y2="260" stroke="#44403c" stroke-width="2" stroke-dasharray="4,4"/>';
    html += '<text x="130" y="35" fill="#fbbf24" font-size="11" font-weight="600" text-anchor="middle">LIVE EXPERIMENTAL SPECIMEN</text>';
    html += '<text x="390" y="35" fill="#fed7aa" font-size="11" font-weight="600" text-anchor="middle">FEA / ANALYTICAL CONTINUUM MODEL</text>';

    // Left: Real physical specimen deflection
    html += '<rect x="25" y="55" width="210" height="180" fill="#1c1917" stroke="#44403c" rx="5"/>';
    const defl = 15 * frac + animStep;
    html += '<rect x="40" y="135" width="180" height="20" fill="#78716c" rx="2"/>';
    html += '<line x1="130" y1="75" x2="130" y2="' + (135 + defl) + '" stroke="#f59e0b" stroke-width="3"/>';
    html += '<polygon points="' + (125) + ',' + (130 + defl) + ' ' + (135) + ',' + (130 + defl) + ' ' + (130) + ',' + (138 + defl) + '" fill="#f59e0b"/>';
    html += '<text x="130" y="215" fill="#a8a29e" font-size="9" text-anchor="middle">Measured Metric: ' + pred.displayed.toFixed(2) + ' ' + cfg.rawUnit + '</text>';

    // Right: Ideal FEA stress/strain distribution
    html += '<rect x="285" y="55" width="210" height="180" fill="#1c1917" stroke="#44403c" rx="5"/>';
    html += '<defs><linearGradient id="feaGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#3b82f6"/><stop offset="50%" stop-color="#10b981"/><stop offset="100%" stop-color="#ef4444"/></linearGradient></defs>';
    html += '<rect x="300" y="135" width="180" height="20" fill="url(#feaGrad)" rx="2"/>';
    html += '<text x="390" y="215" fill="#a8a29e" font-size="9" text-anchor="middle">FEA Benchmark: ' + (p.input * cfg.refValue).toFixed(2) + ' ' + cfg.rawUnit + '</text>';

  } else {
    // Bench or Sandbox Mode: Full Mechanical Test Rig
    html += '<rect x="20" y="20" width="480" height="240" fill="#1c1917" stroke="#44403c" stroke-width="1.5" rx="6"/>';

    // Rigid test frame columns
    html += '<rect x="40" y="30" width="18" height="220" fill="#44403c" rx="3"/>';
    html += '<rect x="462" y="30" width="18" height="220" fill="#44403c" rx="3"/>';

    // Base platen & Top crosshead
    html += '<rect x="35" y="225" width="450" height="25" fill="#292524" rx="3"/>';
    html += '<rect x="35" y="30" width="450" height="22" fill="#292524" rx="3"/>';

    // Moveable crosshead & Hydraulic actuator
    const crossheadY = 85 + 40 * frac;
    html += '<rect x="40" y="' + crossheadY + '" width="440" height="18" fill="#57534e" rx="2"/>';

    // Load cell & Linear Transducer (LVDT)
    html += '<rect x="240" y="' + (crossheadY + 18) + '" width="40" height="28" fill="#d97706" rx="3"/>';
    html += '<text x="260" y="' + (crossheadY + 36) + '" fill="#ffffff" font-size="9" font-weight="600" text-anchor="middle">LOAD CELL</text>';

    // Specimen grips and test coupon
    html += '<rect x="245" y="' + (crossheadY + 46) + '" width="30" height="18" fill="#a8a29e" rx="2"/>';
    html += '<rect x="245" y="195" width="30" height="18" fill="#a8a29e" rx="2"/>';

    // Specimen gauge section (with necking or deflection under load)
    const specWidth = Math.max(6, 12 - 4 * frac);
    const specX = 260 - specWidth / 2;
    html += '<rect x="' + specX + '" y="' + (crossheadY + 64) + '" width="' + specWidth + '" height="' + (195 - (crossheadY + 64)) + '" fill="#f59e0b" rx="1"/>';

    // Dial gauge / Extensometer attachment
    html += '<circle cx="310" cy="155" r="14" fill="#0c0a09" stroke="#fbbf24" stroke-width="1.5"/>';
    html += '<line x1="310" y1="155" x2="' + (310 + 10 * Math.cos(frac * 4)) + '" y2="' + (155 + 10 * Math.sin(frac * 4)) + '" stroke="#ef4444" stroke-width="1.5"/>';

    // Readout banner
    html += '<rect x="58" y="32" width="404" height="18" fill="#0c0a09" rx="2"/>';
    html += '<text x="70" y="45" fill="#fbbf24" font-size="10" font-family="monospace">TEST: ' + cfg.shortTitle.toUpperCase() + '</text>';
    html += '<text x="280" y="45" fill="#a8a29e" font-size="10" font-family="monospace">RATE: 1.0 mm/min</text>';
    html += '<text x="400" y="45" fill="#34d399" font-size="10" font-family="monospace">ACTIVE</text>';

    // Lower Real-Time Telemetry Bar
    html += '<rect x="58" y="228" width="404" height="20" fill="rgba(12,10,9,0.9)" rx="2"/>';
    html += '<text x="75" y="242" fill="#fed7aa" font-size="10">' + cfg.indepName + ': <tspan fill="#ffffff" font-weight="600">' + p.input.toFixed(cfg.inputDecimals) + ' ' + cfg.inputUnit + '</tspan></text>';
    html += '<text x="270" y="242" fill="#fbbf24" font-size="10">' + cfg.depName + ': <tspan fill="#ffffff" font-weight="600">' + pred.displayed.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit + '</tspan></text>';
  }

  svg.innerHTML = html;
}

renderTable();
update();
