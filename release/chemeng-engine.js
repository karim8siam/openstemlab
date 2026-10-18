'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.ChemEngModels;
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
  message('Adjust ' + cfg.shortInput + ', then execute chemical engineering measurement.');
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
    }
  });
}

if ($('measure')) $('measure').onclick = () => {
  if (busy) return;
  busy = true;
  $('measure').disabled = true;
  message('Executing chemical engineering process measurement...');
  const p = params();
  setTimeout(() => {
    measurement = model.predict(cfg.slug, p.input);
    busy = false;
    $('measure').disabled = false;
    if ($('recordReading')) $('recordReading').disabled = false;
    if ($('readingValue')) $('readingValue').textContent = fmt(measurement.raw, cfg.rawDecimals) + ' ' + cfg.rawUnit;
    if ($('liveState')) $('liveState').textContent = 'Telemetry captured: ' + cfg.rawLabel + ' = ' + fmt(measurement.raw, cfg.rawDecimals) + ' ' + cfg.rawUnit + '.';
    message('Measurement acquired. Record observation in laboratory notebook.');
    draw();
  }, 350);
};

if ($('recordReading')) $('recordReading').onclick = () => {
  if (!measurement) return;
  rows.push(measurement);
  if (rows.length > 60) rows.shift();
  persist();
  $('recordReading').disabled = true;
  message('Observation added to laboratory notebook. Total readings: ' + rows.length);
};

if ($('resetApparatus')) $('resetApparatus').onclick = () => {
  $('independent').value = cfg.initial;
  if ($('independentNumber')) $('independentNumber').value = cfg.initial;
  update();
};

document.querySelectorAll('.sim-mode-btn').forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll('.sim-mode-btn').forEach(b => {
      b.classList.remove('active');
      b.setAttribute('aria-selected', 'false');
    });
    btn.classList.add('active');
    btn.setAttribute('aria-selected', 'true');
    currentSimMode = btn.dataset.sim;
    draw();
  };
});

function persist() {
  try {
    localStorage.setItem('openstemlab-' + cfg.slug + '-v1', JSON.stringify(rows));
  } catch (e) {}
  renderResults();
}

function renderResults() {
  if ($('notebookCount')) $('notebookCount').textContent = rows.length;
  const tbody = $('readingRows');
  if (tbody) {
    tbody.innerHTML = rows.map((r, i) =>
      '<tr><td>' + (i + 1) + '</td><td>' + r.input.toFixed(cfg.inputDecimals) + '</td><td>' +
      fmt(r.raw, cfg.rawDecimals) + '</td><td>' + (r.x * cfg.xScale).toFixed(4) + '</td><td>' +
      (r.y * cfg.yScale).toFixed(4) + '</td><td><button class="text-button remove-btn" data-idx="' +
      i + '" style="color:#b91c1c;padding:2px 6px">✕</button></td></tr>'
    ).join('');

    tbody.querySelectorAll('.remove-btn').forEach(b => {
      b.onclick = () => {
        const idx = +b.dataset.idx;
        rows.splice(idx, 1);
        persist();
      };
    });
  }

  if ($('emptyReadings')) $('emptyReadings').style.display = rows.length ? 'none' : 'block';
  if ($('downloadReadings')) $('downloadReadings').disabled = !rows.length;
  if ($('clearReadings')) $('clearReadings').disabled = !rows.length;

  const f = model.fit(rows);
  const sumDiv = $('fitSummary');
  if (sumDiv) {
    if (f) {
      const est = model.estimate(cfg.slug, f);
      sumDiv.innerHTML =
        '<div style="font-size:12px;line-height:1.6">' +
        '<strong>Slope m:</strong> ' + fmt(f.m, 4) + ' | <strong>Intercept b:</strong> ' + fmt(f.b, 4) + '<br>' +
        '<strong>R² Fit:</strong> ' + f.r2.toFixed(5) + ' | <strong>N:</strong> ' + f.n + '<br>' +
        '<span style="color:#b45309;font-weight:600">Extracted ' + cfg.targetName + ': ' + fmt(est.value * cfg.resultScale, cfg.resultDecimals) + ' ' + cfg.resultUnit + '</span>' +
        '</div>';
    } else {
      sumDiv.innerHTML = '<p style="font-size:11px;color:#78350f">Record at least 3 distinct observations to compute regression fit.</p>';
    }
  }

  drawPlot(f);
}

function drawPlot(f) {
  const svg = $('labPlot');
  if (!svg) return;
  const w = 650, h = 340;
  const pad = { left: 65, right: 30, top: 25, bottom: 50 };
  const pw = w - pad.left - pad.right;
  const ph = h - pad.top - pad.bottom;

  let pts = rows.map(r => ({ x: r.x * cfg.xScale, y: r.y * cfg.yScale }));
  let minX = cfg.emptyX * 0.5, maxX = cfg.emptyX * 1.5;
  let minY = cfg.emptyY * 0.5, maxY = cfg.emptyY * 1.5;

  if (pts.length) {
    minX = Math.min(...pts.map(p => p.x));
    maxX = Math.max(...pts.map(p => p.x));
    minY = Math.min(...pts.map(p => p.y));
    maxY = Math.max(...pts.map(p => p.y));
    if (minX === maxX) { minX -= 1; maxX += 1; }
    if (minY === maxY) { minY -= 1; maxY += 1; }
    const spanX = maxX - minX;
    minX = Math.max(0, minX - spanX * 0.1);
    maxX += spanX * 0.1;
    const spanY = maxY - minY;
    minY -= spanY * 0.1;
    maxY += spanY * 0.1;
  }

  const mapX = x => pad.left + (x - minX) / (maxX - minX) * pw;
  const mapY = y => pad.top + ph - (y - minY) / (maxY - minY) * ph;

  let s = '<rect width="' + w + '" height="' + h + '" fill="#fffdfa"/>';
  // Grid lines
  for (let i = 0; i <= 5; i++) {
    const gx = pad.left + i * pw / 5;
    const gy = pad.top + i * ph / 5;
    s += '<line x1="' + gx + '" y1="' + pad.top + '" x2="' + gx + '" y2="' + (pad.top + ph) + '" stroke="#fde68a" stroke-width="1"/>';
    s += '<line x1="' + pad.left + '" y1="' + gy + '" x2="' + (pad.left + pw) + '" y2="' + gy + '" stroke="#fde68a" stroke-width="1"/>';
    const xv = minX + i * (maxX - minX) / 5;
    const yv = maxY - i * (maxY - minY) / 5;
    s += '<text x="' + gx + '" y="' + (pad.top + ph + 16) + '" font-size="10" fill="#78350f" text-anchor="middle">' + fmt(xv, 2) + '</text>';
    s += '<text x="' + (pad.left - 8) + '" y="' + (gy + 4) + '" font-size="10" fill="#78350f" text-anchor="end">' + fmt(yv, 2) + '</text>';
  }

  // Regression line
  if (f && pts.length >= 2) {
    const x1 = minX, y1 = (f.m * (x1 / cfg.xScale) + f.b) * cfg.yScale;
    const x2 = maxX, y2 = (f.m * (x2 / cfg.xScale) + f.b) * cfg.yScale;
    s += '<line x1="' + mapX(x1) + '" y1="' + mapY(y1) + '" x2="' + mapX(x2) + '" y2="' + mapY(y2) + '" stroke="#b45309" stroke-width="2.5"/>';
  }

  // Data points
  pts.forEach(p => {
    s += '<circle cx="' + mapX(p.x) + '" cy="' + mapY(p.y) + '" r="4.5" fill="#d97706" stroke="#1c1917" stroke-width="1.5"/>';
  });

  // Axis Labels
  s += '<text x="' + (pad.left + pw / 2) + '" y="' + (h - 10) + '" font-size="11" fill="#1c1917" text-anchor="middle" font-weight="600">' + cfg.xAxis + '</text>';
  s += '<text x="18" y="' + (pad.top + ph / 2) + '" font-size="11" fill="#1c1917" text-anchor="middle" transform="rotate(-90 18 ' + (pad.top + ph / 2) + ')" font-weight="600">' + cfg.yAxis + '</text>';

  svg.innerHTML = s;
}

function draw() {
  const svg = $('apparatusDiagram');
  if (!svg) return;
  const p = params();
  const val = p.input;
  const num = cfg.number;

  let s = '<defs>';
  s += '<linearGradient id="fluidGrad" x1="0%" y1="0%" x2="100%" y2="0%">';
  s += '<stop offset="0%" stop-color="#f59e0b" stop-opacity="0.8"/>';
  s += '<stop offset="100%" stop-color="#b45309" stop-opacity="0.8"/>';
  s += '</linearGradient>';
  s += '<linearGradient id="metalGrad" x1="0%" y1="0%" x2="0%" y2="100%">';
  s += '<stop offset="0%" stop-color="#64748b"/>';
  s += '<stop offset="50%" stop-color="#334155"/>';
  s += '<stop offset="100%" stop-color="#1e293b"/>';
  s += '</linearGradient>';
  s += '<linearGradient id="vaporGrad" x1="0%" y1="100%" x2="0%" y2="0%">';
  s += '<stop offset="0%" stop-color="#fbbf24" stop-opacity="0.3"/>';
  s += '<stop offset="100%" stop-color="#fde68a" stop-opacity="0.9"/>';
  s += '</linearGradient>';
  s += '</defs>';

  // Base background
  s += '<rect width="720" height="320" fill="#1c1917"/>';

  // Routing to appropriate module SVG visualizer
  if (num <= 8) {
    s += drawModule1Fluids(val, currentSimMode, num);
  } else if (num <= 16) {
    s += drawModule2HeatTransfer(val, currentSimMode, num);
  } else if (num <= 24) {
    s += drawModule3MassTransfer(val, currentSimMode, num);
  } else if (num <= 32) {
    s += drawModule4Reactions(val, currentSimMode, num);
  } else if (num <= 39) {
    s += drawModule5Thermodynamics(val, currentSimMode, num);
  } else {
    s += drawModule6DynamicsControl(val, currentSimMode, num);
  }

  svg.innerHTML = s;
}

function drawModule1Fluids(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="50" width="640" height="220" fill="#0c0a09" stroke="#78350f" stroke-width="1.5" rx="6"/>';

  if (num === 1) { // Venturi meter
    s += '<path d="M 60 140 L 220 140 L 290 155 L 360 155 L 480 140 L 660 140 L 660 180 L 480 180 L 360 165 L 290 165 L 220 180 L 60 180 Z" fill="url(#metalGrad)" stroke="#fbbf24" stroke-width="1.5"/>';
    const dh = (0.485 * val) ** 2 * 0.8;
    s += '<rect x="235" y="' + (140 - dh) + '" width="14" height="' + dh + '" fill="#0284c7" opacity="0.8"/>';
    s += '<rect x="320" y="110" width="14" height="45" fill="#0284c7" opacity="0.8"/>';
    s += '<line x1="235" y1="140" x2="249" y2="140" stroke="#f59e0b" stroke-width="2"/>';
    s += '<line x1="320" y1="155" x2="334" y2="155" stroke="#f59e0b" stroke-width="2"/>';
    s += '<text x="242" y="' + (130 - dh) + '" fill="#38bdf8" font-size="10" text-anchor="middle">h_1</text>';
    s += '<text x="327" y="100" fill="#38bdf8" font-size="10" text-anchor="middle">h_2 (Throat)</text>';
    s += '<text x="360" y="225" fill="#fbbf24" font-size="12" text-anchor="middle">Venturi Flow Rate Q = ' + val.toFixed(1) + ' L/min (Δh = ' + dh.toFixed(1) + ' cm)</text>';
  } else if (num === 4 || num === 5) { // Fluidized or packed bed
    s += '<rect x="280" y="70" width="160" height="180" fill="#292524" stroke="#f59e0b" stroke-width="2" rx="4"/>';
    const bedH = num === 4 ? 60 + val * 5 : 110;
    s += '<rect x="285" y="' + (245 - bedH) + '" width="150" height="' + bedH + '" fill="#78350f" opacity="0.85"/>';
    s += '<line x1="260" y1="240" x2="260" y2="' + (240 - val * 8) + '" stroke="#ef4444" stroke-width="3"/>';
    s += '<text x="360" y="' + (235 - bedH/2) + '" fill="#fef3c7" font-size="11" text-anchor="middle">Granular Packing</text>';
    s += '<text x="360" y="265" fill="#fbbf24" font-size="11" text-anchor="middle">' + cfg.shortInput + ': ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
  } else {
    // Pipe / flow loop
    s += '<line x1="80" y1="160" x2="640" y2="160" stroke="#f59e0b" stroke-width="8"/>';
    s += '<circle cx="360" cy="160" r="35" fill="#334155" stroke="#fbbf24" stroke-width="2"/>';
    s += '<text x="360" y="165" fill="#fbbf24" font-size="11" text-anchor="middle">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="360" y="235" fill="#fbbf24" font-size="12" text-anchor="middle">' + cfg.shortInput + ' = ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
  }
  return s;
}

function drawModule2HeatTransfer(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="50" width="640" height="220" fill="#0c0a09" stroke="#b45309" stroke-width="1.5" rx="6"/>';

  if (num === 9) { // Shell & tube
    s += '<rect x="140" y="85" width="440" height="150" fill="#292524" stroke="#f59e0b" stroke-width="2" rx="10"/>';
    for (let i = 0; i < 4; i++) {
      s += '<line x1="140" y1="' + (110 + i * 32) + '" x2="580" y2="' + (110 + i * 32) + '" stroke="#38bdf8" stroke-width="5"/>';
    }
    s += '<text x="360" y="125" fill="#f87171" font-size="11" text-anchor="middle">SHELL SIDE HOT STREAM</text>';
    s += '<text x="360" y="175" fill="#38bdf8" font-size="11" text-anchor="middle">TUBE BUNDLE COLD STREAM</text>';
    s += '<text x="360" y="255" fill="#fbbf24" font-size="12" text-anchor="middle">Shell Flow V_h = ' + val.toFixed(1) + ' L/min (U = ' + (85 * val**0.8).toFixed(1) + ' W/m²K)</text>';
  } else {
    // Thermal unit operation
    s += '<rect x="220" y="80" width="280" height="150" fill="#292524" stroke="#f59e0b" stroke-width="2" rx="6"/>';
    s += '<text x="360" y="125" fill="#f59e0b" font-size="12" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="360" y="165" fill="#fde68a" font-size="16" text-anchor="middle">' + cfg.shortInput + ': ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
    s += '<text x="360" y="200" fill="#fbbf24" font-size="11" text-anchor="middle">Thermal Steady State Active</text>';
  }
  return s;
}

function drawModule3MassTransfer(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="50" width="640" height="220" fill="#0c0a09" stroke="#b45309" stroke-width="1.5" rx="6"/>';

  if (num === 17) { // Distillation column
    s += '<rect x="310" y="60" width="100" height="190" fill="#292524" stroke="#f59e0b" stroke-width="2" rx="8"/>';
    for (let i = 0; i < 7; i++) {
      s += '<line x1="315" y1="' + (85 + i * 22) + '" x2="405" y2="' + (85 + i * 22) + '" stroke="#fbbf24" stroke-width="1.5" stroke-dasharray="6,3"/>';
    }
    s += '<path d="M 410 75 L 460 75 L 460 120 L 405 120" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';
    s += '<text x="500" y="95" fill="#38bdf8" font-size="10">Reflux R = ' + val.toFixed(1) + '</text>';
    s += '<text x="360" y="270" fill="#fbbf24" font-size="12" text-anchor="middle">McCabe–Thiele Fractional Column (x_D = ' + (1 - 1/(2.85*val + 1.25)).toFixed(3) + ')</text>';
  } else {
    // Mass transfer contactor
    s += '<rect x="250" y="75" width="220" height="170" fill="#292524" stroke="#f59e0b" stroke-width="2" rx="6"/>';
    s += '<text x="360" y="125" fill="#f59e0b" font-size="12" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="360" y="165" fill="#fde68a" font-size="16" text-anchor="middle">' + cfg.shortInput + ': ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
    s += '<text x="360" y="200" fill="#fbbf24" font-size="11" text-anchor="middle">Separation Stage Operating</text>';
  }
  return s;
}

function drawModule4Reactions(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="50" width="640" height="220" fill="#0c0a09" stroke="#b45309" stroke-width="1.5" rx="6"/>';

  if (num === 25) { // CSTR
    s += '<rect x="280" y="75" width="160" height="170" fill="#292524" stroke="#f59e0b" stroke-width="2" rx="12"/>';
    s += '<rect x="290" y="125" width="140" height="110" fill="#b45309" opacity="0.65" rx="6"/>';
    s += '<line x1="360" y1="65" x2="360" y2="185" stroke="#94a3b8" stroke-width="4"/>';
    s += '<line x1="330" y1="185" x2="390" y2="185" stroke="#94a3b8" stroke-width="6"/>';
    s += '<path d="M 230 110 L 280 110" stroke="#f59e0b" stroke-width="3"/>';
    s += '<path d="M 440 210 L 490 210" stroke="#f59e0b" stroke-width="3"/>';
    s += '<text x="360" y="265" fill="#fbbf24" font-size="12" text-anchor="middle">CSTR Reactor Space Time τ = ' + val.toFixed(1) + ' min</text>';
  } else if (num === 26) { // PFR
    s += '<path d="M 120 160 L 600 160" stroke="#78350f" stroke-width="26" stroke-linecap="round"/>';
    s += '<path d="M 120 160 L 600 160" stroke="#f59e0b" stroke-width="18" stroke-dasharray="10,6" stroke-linecap="round"/>';
    s += '<text x="360" y="135" fill="#fbbf24" font-size="11" text-anchor="middle">PLUG FLOW TUBULAR REACTOR</text>';
    s += '<text x="360" y="215" fill="#fde68a" font-size="12" text-anchor="middle">Residence Time τ = ' + val.toFixed(1) + ' min</text>';
  } else {
    // Bioreactor / Catalytic bed
    s += '<rect x="250" y="75" width="220" height="170" fill="#292524" stroke="#f59e0b" stroke-width="2" rx="8"/>';
    s += '<text x="360" y="125" fill="#f59e0b" font-size="12" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="360" y="165" fill="#fde68a" font-size="16" text-anchor="middle">' + cfg.shortInput + ': ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
    s += '<text x="360" y="200" fill="#fbbf24" font-size="11" text-anchor="middle">Reaction System Equilibrated</text>';
  }
  return s;
}

function drawModule5Thermodynamics(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="50" width="640" height="220" fill="#0c0a09" stroke="#b45309" stroke-width="1.5" rx="6"/>';

  if (num === 33) { // VLE still
    s += '<circle cx="310" cy="180" r="45" fill="#292524" stroke="#f59e0b" stroke-width="2"/>';
    s += '<rect x="300" y="85" width="20" height="55" fill="#334155" stroke="#f59e0b" stroke-width="1.5"/>';
    s += '<path d="M 320 85 L 420 85 L 420 180 L 355 180" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';
    s += '<text x="360" y="255" fill="#fbbf24" font-size="12" text-anchor="middle">Othmer VLE Recirculating Still (x_1 = ' + val.toFixed(2) + ')</text>';
  } else if (num === 35) { // Bomb calorimeter
    s += '<rect x="300" y="75" width="120" height="160" fill="#292524" stroke="#f59e0b" stroke-width="2.5" rx="6"/>';
    s += '<rect x="325" y="105" width="70" height="100" fill="#475569" stroke="#e2e8f0" stroke-width="1.5" rx="4"/>';
    s += '<line x1="360" y1="105" x2="360" y2="155" stroke="#ef4444" stroke-width="2"/>';
    s += '<text x="360" y="260" fill="#fbbf24" font-size="12" text-anchor="middle">Oxygen Bomb (m_s = ' + val.toFixed(2) + ' g, P_O2 = 3.0 MPa)</text>';
  } else {
    // Phase equilibria cell
    s += '<rect x="250" y="75" width="220" height="170" fill="#292524" stroke="#f59e0b" stroke-width="2" rx="6"/>';
    s += '<text x="360" y="125" fill="#f59e0b" font-size="12" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="360" y="165" fill="#fde68a" font-size="16" text-anchor="middle">' + cfg.shortInput + ': ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
    s += '<text x="360" y="200" fill="#fbbf24" font-size="11" text-anchor="middle">Thermodynamic Equilibrium State</text>';
  }
  return s;
}

function drawModule6DynamicsControl(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="50" width="640" height="220" fill="#0c0a09" stroke="#b45309" stroke-width="1.5" rx="6"/>';

  if (num === 40) { // Gravity drained tank
    s += '<rect x="290" y="70" width="140" height="170" fill="#292524" stroke="#f59e0b" stroke-width="2" rx="4"/>';
    const hPx = Math.min(150, val * 3.85 * 3.2);
    s += '<rect x="295" y="' + (235 - hPx) + '" width="130" height="' + hPx + '" fill="#0284c7" opacity="0.75"/>';
    s += '<path d="M 240 60 L 330 60 L 330 85" fill="none" stroke="#38bdf8" stroke-width="4"/>';
    s += '<path d="M 430 230 L 480 230" stroke="#38bdf8" stroke-width="4"/>';
    s += '<text x="360" y="265" fill="#fbbf24" font-size="12" text-anchor="middle">Surge Tank Level h_ss = ' + (val * 3.85).toFixed(1) + ' cm (F_in = ' + val.toFixed(1) + ' L/min)</text>';
  } else if (num === 43) { // Pneumatic control valve
    s += '<path d="M 220 160 L 330 160 L 390 190 L 390 130 L 450 160 L 520 160" stroke="#f59e0b" stroke-width="6" fill="none"/>';
    s += '<circle cx="360" cy="100" r="30" fill="#334155" stroke="#fbbf24" stroke-width="2"/>';
    s += '<line x1="360" y1="130" x2="360" y2="160" stroke="#e2e8f0" stroke-width="4"/>';
    s += '<text x="360" y="105" fill="#fbbf24" font-size="10" text-anchor="middle">ACTUATOR</text>';
    s += '<text x="360" y="240" fill="#fbbf24" font-size="12" text-anchor="middle">Pneumatic Valve Lift x = ' + val.toFixed(1) + '% (Q = ' + (0.85 * val).toFixed(1) + ' m³/h)</text>';
  } else {
    // Process control rig
    s += '<rect x="250" y="75" width="220" height="170" fill="#292524" stroke="#f59e0b" stroke-width="2" rx="6"/>';
    s += '<text x="360" y="125" fill="#f59e0b" font-size="12" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="360" y="165" fill="#fde68a" font-size="16" text-anchor="middle">' + cfg.shortInput + ': ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
    s += '<text x="360" y="200" fill="#fbbf24" font-size="11" text-anchor="middle">Automatic Process Control Active</text>';
  }
  return s;
}

if ($('downloadReadings')) {
  $('downloadReadings').onclick = () => {
    if (!rows.length) return;
    const header = [cfg.shortInput, cfg.rawLabel, 'x_transformed', 'y_transformed'];
    const lines = [header.join(',')];
    rows.forEach(r => {
      lines.push([r.input, r.raw, (r.x * cfg.xScale).toFixed(4), (r.y * cfg.yScale).toFixed(4)].join(','));
    });
    const blob = new Blob([lines.join('\n')], { type: 'text/csv' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = cfg.slug + '-observations.csv';
    a.click();
  };
}

if ($('clearReadings')) {
  $('clearReadings').onclick = () => {
    if (!rows.length) return;
    rows = [];
    persist();
    message('Observation notebook cleared.');
  };
}

if ($('checkEstimate')) {
  $('checkEstimate').onclick = () => {
    const val = +$('studentEstimate').value;
    const fb = $('estimateFeedback');
    if (!fb || !Number.isFinite(val)) return;
    const ref = cfg.refValue;
    const err = Math.abs(val - ref) / Math.abs(ref) * 100;
    if (err <= 2.0) {
      fb.className = 'quiz-feedback correct';
      fb.textContent = 'Excellent! Your calculation of ' + val + ' ' + cfg.resultUnit + ' matches the theoretical target within ' + err.toFixed(2) + '%.';
    } else {
      fb.className = 'quiz-feedback wrong';
      fb.textContent = 'Calculation difference is ' + err.toFixed(1) + '%. Review the regression gradient and calculation formula above.';
    }
  };
}

// Quiz Handlers
document.querySelectorAll('.quiz-option').forEach(b => {
  b.onclick = () => {
    const qIdx = +b.dataset.quiz;
    const cIdx = +b.dataset.choice;
    const q = cfg.quiz[qIdx];
    const fb = $('quizFeedback' + qIdx);
    if (!q || !fb) return;
    const card = b.closest('.quiz-card');
    if (card) {
      card.querySelectorAll('.quiz-option').forEach(opt => opt.classList.remove('selected', 'correct', 'wrong'));
    }
    b.classList.add('selected');
    if (cIdx === q.correct) {
      b.classList.add('correct');
      fb.className = 'quiz-feedback correct';
      fb.textContent = '✓ Correct! ' + q.explanation;
    } else {
      b.classList.add('wrong');
      fb.className = 'quiz-feedback wrong';
      fb.textContent = '✗ Incorrect. ' + q.explanation;
    }
  };
});

// Initialization
update();
renderResults();
