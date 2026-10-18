'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.CivilModels;
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
  message('Adjust ' + cfg.shortInput + ', then execute civil engineering measurement.');
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

// Mode switching
document.querySelectorAll('.sim-mode-btn').forEach(b => {
  b.onclick = () => {
    document.querySelectorAll('.sim-mode-btn').forEach(btn => btn.classList.remove('active'));
    b.classList.add('active');
    currentSimMode = b.dataset.mode;
    draw();
  };
});

if ($('measure')) {
  $('measure').onclick = () => {
    if (busy) return;
    busy = true;
    $('measure').disabled = true;
    if ($('recordReading')) $('recordReading').disabled = true;
    message('Sampling instrumentation transducer signals...');
    const p = params();
    const pred = model.predict(cfg.slug, p.input);
    setTimeout(() => {
      measurement = { input: p.input, raw: pred.raw };
      if ($('readingValue')) $('readingValue').textContent = pred.raw.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit;
      if ($('recordReading')) $('recordReading').disabled = false;
      if ($('liveState')) $('liveState').textContent = 'Observed ' + cfg.rawLabel + ' = ' + pred.raw.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit + '.';
      message('Acquisition complete. Record observation to notebook.');
      busy = false;
      $('measure').disabled = false;
      draw();
    }, 280);
  };
}

if ($('recordReading')) {
  $('recordReading').onclick = () => {
    if (!measurement) return;
    const r = model.reading(cfg.slug, measurement.input, measurement.raw);
    rows.push(r);
    persist();
    renderResults();
    $('recordReading').disabled = true;
    message('Sample logged to data table (' + rows.length + ' total observations).');
  };
}

function persist() {
  try {
    localStorage.setItem('openstemlab-' + cfg.slug + '-v1', JSON.stringify(rows));
  } catch (e) {}
}

function renderResults() {
  const tbody = $('readingsBody');
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
                         '<p class="report-equation">Linear fit: <em>y</em> = ' + fmt(fitRes.m, 4) + ' <em>x</em> ' + (fitRes.b >= 0 ? '+ ' : '- ') + fmt(Math.abs(fitRes.b), 4) + '</p>' +
                         '<p>Correlation coefficient: <em>R</em>² = ' + fitRes.r2.toFixed(6) + ' (<em>N</em> = ' + fitRes.n + ')</p>' +
                         '<p>Standard error: ±' + fmt(est.se, 5) + ' | Reference benchmark: ' + cfg.refValue + ' ' + cfg.resultUnit + '</p>';
    } else {
      fitBox.innerHTML = '<p>Log at least 3 distinct observations to compute regression fit and engineering parameter.</p>';
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

  let s = '<rect width="' + W + '" height="' + H + '" fill="#0f172a" rx="6"/>';

  // Grid
  for (let i = 0; i <= 5; i++) {
    const gx = minX + (maxX - minX) * (i / 5);
    const gy = minY + (maxY - minY) * (i / 5);
    s += '<line x1="' + tx(gx) + '" y1="' + pad.top + '" x2="' + tx(gx) + '" y2="' + (pad.top + ph) + '" stroke="#1e293b" stroke-dasharray="2,2"/>';
    s += '<line x1="' + pad.left + '" y1="' + ty(gy) + '" x2="' + (pad.left + pw) + '" y2="' + ty(gy) + '" stroke="#1e293b" stroke-dasharray="2,2"/>';
    s += '<text x="' + tx(gx) + '" y="' + (H - 12) + '" fill="#94a3b8" font-size="9" text-anchor="middle">' + fmt(gx, 1) + '</text>';
    s += '<text x="' + (pad.left - 8) + '" y="' + (ty(gy) + 3) + '" fill="#94a3b8" font-size="9" text-anchor="end">' + fmt(gy, 1) + '</text>';
  }

  // Axes
  s += '<line x1="' + pad.left + '" y1="' + (pad.top + ph) + '" x2="' + (pad.left + pw) + '" y2="' + (pad.top + ph) + '" stroke="#475569" stroke-width="1.5"/>';
  s += '<line x1="' + pad.left + '" y1="' + pad.top + '" x2="' + pad.left + '" y2="' + (pad.top + ph) + '" stroke="#475569" stroke-width="1.5"/>';
  s += '<text x="' + (pad.left + pw / 2) + '" y="' + (H - 2) + '" fill="#f97316" font-size="10" text-anchor="middle">' + cfg.xAxis + '</text>';
  s += '<text x="14" y="' + (pad.top + ph / 2) + '" fill="#f97316" font-size="10" text-anchor="middle" transform="rotate(-90 14 ' + (pad.top + ph / 2) + ')">' + cfg.yAxis + '</text>';

  // Fit line
  if (fitRes && fitRes.n >= 2) {
    const x1 = minX, y1 = fitRes.m * (x1 / cfg.xScale) + fitRes.b;
    const x2 = maxX, y2 = fitRes.m * (x2 / cfg.xScale) + fitRes.b;
    s += '<line x1="' + tx(x1) + '" y1="' + ty(y1 * cfg.yScale) + '" x2="' + tx(x2) + '" y2="' + ty(y2 * cfg.yScale) + '" stroke="#38bdf8" stroke-width="2"/>';
  }

  // Points
  rows.forEach(r => {
    const px = tx(r.x * cfg.xScale);
    const py = ty(r.y * cfg.yScale);
    s += '<circle cx="' + px + '" cy="' + py + '" r="4.5" fill="#f97316" stroke="#ffffff" stroke-width="1.5"/>';
  });

  svg.innerHTML = s;
}

function draw() {
  const svg = $('apparatusSvg');
  if (!svg) return;
  const p = params();
  const val = p.input;
  const num = cfg.number;
  const mode = currentSimMode;

  let s = '';
  if (num <= 9) {
    s = drawModule1Materials(val, mode, num);
  } else if (num <= 18) {
    s = drawModule2Structures(val, mode, num);
  } else if (num <= 27) {
    s = drawModule3Geotech(val, mode, num);
  } else if (num <= 36) {
    s = drawModule4Hydraulics(val, mode, num);
  } else if (num <= 43) {
    s = drawModule5Transportation(val, mode, num);
  } else {
    s = drawModule6SurveyingDynamics(val, mode, num);
  }

  svg.innerHTML = s;
}

function drawModule1Materials(val, mode, num) {
  let s = '<rect x="40" y="50" width="640" height="220" fill="#020617" stroke="#334155" stroke-width="1.5" rx="6"/>';
  if (num === 1) { // Slump cone
    const slumpH = Math.max(10, Math.min(120, (240 * val - 75) * 1.2));
    s += '<path d="M 330 90 L 390 90 L 420 220 L 300 220 Z" fill="#334155" stroke="#94a3b8" stroke-width="2"/>';
    s += '<path d="M 310 220 C 320 ' + (220 - slumpH) + ', 400 ' + (220 - slumpH) + ', 410 220 Z" fill="#f97316" opacity="0.8"/>';
    s += '<line x1="280" y1="90" x2="280" y2="' + (220 - slumpH) + '" stroke="#38bdf8" stroke-width="2" stroke-dasharray="3,3"/>';
    s += '<text x="360" y="250" fill="#f97316" font-size="12" text-anchor="middle">Abrams Slump = ' + (240 * val - 75).toFixed(1) + ' mm (w/c = ' + val.toFixed(2) + ')</text>';
  } else if (num === 2) { // Cylinder compressive strength
    s += '<rect x="310" y="90" width="100" height="130" fill="#475569" stroke="#94a3b8" stroke-width="2" rx="4"/>';
    s += '<rect x="290" y="70" width="140" height="20" fill="#1e293b" stroke="#f97316" stroke-width="2"/>';
    s += '<rect x="290" y="220" width="140" height="20" fill="#1e293b" stroke="#f97316" stroke-width="2"/>';
    const fc = 8.5 * Math.log(val) + 12.0;
    s += '<text x="360" y="160" fill="#f8fafc" font-size="13" font-weight="bold" text-anchor="middle">CURE: ' + val.toFixed(0) + ' DAYS</text>';
    s += '<text x="360" y="255" fill="#f97316" font-size="12" text-anchor="middle">Compressive Strength f\'c = ' + fc.toFixed(2) + ' MPa</text>';
  } else {
    s += '<rect x="250" y="75" width="220" height="160" fill="#1e293b" stroke="#f97316" stroke-width="2" rx="6"/>';
    s += '<text x="360" y="125" fill="#f97316" font-size="12" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="360" y="165" fill="#f8fafc" font-size="15" text-anchor="middle">' + cfg.shortInput + ': ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
    s += '<text x="360" y="200" fill="#38bdf8" font-size="11" text-anchor="middle">Specimen Testing Active</text>';
  }
  return s;
}

function drawModule2Structures(val, mode, num) {
  let s = '<rect x="40" y="50" width="640" height="220" fill="#020617" stroke="#334155" stroke-width="1.5" rx="6"/>';
  if (num === 10) { // UTM Tensile rebar
    s += '<line x1="360" y1="75" x2="360" y2="225" stroke="#f97316" stroke-width="10"/>';
    s += '<rect x="330" y="65" width="60" height="20" fill="#475569" stroke="#cbd5e1" stroke-width="1.5"/>';
    s += '<rect x="330" y="215" width="60" height="20" fill="#475569" stroke="#cbd5e1" stroke-width="1.5"/>';
    s += '<text x="360" y="255" fill="#f97316" font-size="12" text-anchor="middle">Tensile Stress σ = ' + (0.2 * val).toFixed(1) + ' MPa (ε = ' + val.toFixed(0) + ' µε)</text>';
  } else if (num === 13) { // Beam deflection
    const defl = val * 0.425 * 5;
    s += '<path d="M 200 150 Q 360 ' + (150 + defl) + ' 520 150" fill="none" stroke="#f97316" stroke-width="6"/>';
    s += '<polygon points="200,150 190,175 210,175" fill="#94a3b8"/>';
    s += '<polygon points="520,150 510,175 530,175" fill="#94a3b8"/>';
    s += '<line x1="360" y1="90" x2="360" y2="' + (150 + defl) + '" stroke="#ef4444" stroke-width="3" marker-end="url(#arrow)"/>';
    s += '<text x="360" y="255" fill="#f97316" font-size="12" text-anchor="middle">Central Deflection δ = ' + (val * 0.425).toFixed(2) + ' mm (P = ' + val.toFixed(1) + ' kN)</text>';
  } else {
    s += '<rect x="250" y="75" width="220" height="160" fill="#1e293b" stroke="#f97316" stroke-width="2" rx="6"/>';
    s += '<text x="360" y="125" fill="#f97316" font-size="12" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="360" y="165" fill="#f8fafc" font-size="15" text-anchor="middle">' + cfg.shortInput + ': ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
    s += '<text x="360" y="200" fill="#38bdf8" font-size="11" text-anchor="middle">Structural Test Active</text>';
  }
  return s;
}

function drawModule3Geotech(val, mode, num) {
  let s = '<rect x="40" y="50" width="640" height="220" fill="#020617" stroke="#334155" stroke-width="1.5" rx="6"/>';
  if (num === 20) { // Direct shear box
    s += '<rect x="280" y="110" width="160" height="50" fill="#78350f" stroke="#d97706" stroke-width="1.5"/>';
    s += '<rect x="290" y="160" width="160" height="50" fill="#78350f" stroke="#d97706" stroke-width="1.5"/>';
    s += '<line x1="360" y1="70" x2="360" y2="110" stroke="#f97316" stroke-width="4"/>';
    s += '<text x="360" y="255" fill="#f97316" font-size="12" text-anchor="middle">Direct Shear Failure τ_f = ' + (0.625 * val + 5.0).toFixed(1) + ' kPa (σ_n = ' + val.toFixed(0) + ' kPa)</text>';
  } else if (num === 21) { // Darcy permeameter
    s += '<rect x="320" y="75" width="80" height="140" fill="#1e293b" stroke="#0284c7" stroke-width="2"/>';
    s += '<rect x="325" y="115" width="70" height="60" fill="#d97706" opacity="0.8"/>';
    s += '<line x1="360" y1="60" x2="360" y2="75" stroke="#38bdf8" stroke-width="3"/>';
    s += '<text x="360" y="255" fill="#f97316" font-size="12" text-anchor="middle">Constant Head Permeameter Q = ' + (1.45 * val).toFixed(1) + ' cm³/s (Δh = ' + val.toFixed(1) + ' cm)</text>';
  } else {
    s += '<rect x="250" y="75" width="220" height="160" fill="#1e293b" stroke="#f97316" stroke-width="2" rx="6"/>';
    s += '<text x="360" y="125" fill="#f97316" font-size="12" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="360" y="165" fill="#f8fafc" font-size="15" text-anchor="middle">' + cfg.shortInput + ': ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
    s += '<text x="360" y="200" fill="#38bdf8" font-size="11" text-anchor="middle">Geotechnical Cell Equilibrated</text>';
  }
  return s;
}

function drawModule4Hydraulics(val, mode, num) {
  let s = '<rect x="40" y="50" width="640" height="220" fill="#020617" stroke="#334155" stroke-width="1.5" rx="6"/>';
  if (num === 28) { // V-notch weir
    s += '<rect x="180" y="100" width="360" height="110" fill="#0369a1" opacity="0.75" rx="4"/>';
    s += '<polygon points="360,165 320,100 400,100" fill="#020617" stroke="#f97316" stroke-width="2"/>';
    s += '<text x="360" y="250" fill="#f97316" font-size="12" text-anchor="middle">Sharp-Crested Weir Flow Q = ' + (1.38 * val).toFixed(3) + ' m³/s</text>';
  } else if (num === 29) { // Hydraulic jump
    s += '<path d="M 160 180 L 320 180 Q 360 130 420 120 L 560 120" stroke="#38bdf8" stroke-width="5" fill="none"/>';
    s += '<line x1="160" y1="200" x2="560" y2="200" stroke="#64748b" stroke-width="3"/>';
    s += '<text x="360" y="250" fill="#f97316" font-size="12" text-anchor="middle">Hydraulic Jump Sequent Depth Ratio y_2/y_1 = ' + val.toFixed(2) + '</text>';
  } else {
    s += '<rect x="250" y="75" width="220" height="160" fill="#1e293b" stroke="#f97316" stroke-width="2" rx="6"/>';
    s += '<text x="360" y="125" fill="#f97316" font-size="12" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="360" y="165" fill="#f8fafc" font-size="15" text-anchor="middle">' + cfg.shortInput + ': ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
    s += '<text x="360" y="200" fill="#38bdf8" font-size="11" text-anchor="middle">Hydraulics Channel Flow Active</text>';
  }
  return s;
}

function drawModule5Transportation(val, mode, num) {
  let s = '<rect x="40" y="50" width="640" height="220" fill="#020617" stroke="#334155" stroke-width="1.5" rx="6"/>';
  if (num === 37) { // LA Abrasion drum
    s += '<circle cx="360" cy="145" r="65" fill="#1e293b" stroke="#f97316" stroke-width="3"/>';
    s += '<circle cx="360" cy="145" r="10" fill="#94a3b8"/>';
    s += '<circle cx="340" cy="165" r="7" fill="#cbd5e1"/>';
    s += '<circle cx="380" cy="130" r="7" fill="#cbd5e1"/>';
    s += '<text x="360" y="250" fill="#f97316" font-size="12" text-anchor="middle">Los Angeles Abrasion Drum (N = ' + val.toFixed(0) + ' revs, Fines = ' + (2.45 * val).toFixed(1) + ' g)</text>';
  } else if (num === 40) { // Bitumen penetration
    s += '<rect x="320" y="140" width="80" height="60" fill="#0f172a" stroke="#d97706" stroke-width="2"/>';
    const dH = Math.min(45, (3.8 * val - 25) * 0.4);
    s += '<line x1="360" y1="90" x2="360" y2="' + (140 + dH) + '" stroke="#f97316" stroke-width="2.5"/>';
    s += '<text x="360" y="250" fill="#f97316" font-size="12" text-anchor="middle">Bitumen Needle Penetration d = ' + (3.8 * val - 25).toFixed(1) + ' dmm (T = ' + val.toFixed(1) + ' °C)</text>';
  } else {
    s += '<rect x="250" y="75" width="220" height="160" fill="#1e293b" stroke="#f97316" stroke-width="2" rx="6"/>';
    s += '<text x="360" y="125" fill="#f97316" font-size="12" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="360" y="165" fill="#f8fafc" font-size="15" text-anchor="middle">' + cfg.shortInput + ': ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
    s += '<text x="360" y="200" fill="#38bdf8" font-size="11" text-anchor="middle">Pavement Material Testing Active</text>';
  }
  return s;
}

function drawModule6SurveyingDynamics(val, mode, num) {
  let s = '<rect x="40" y="50" width="640" height="220" fill="#020617" stroke="#334155" stroke-width="1.5" rx="6"/>';
  if (num === 44) { // Total station EDM
    s += '<polygon points="250,190 230,230 270,230" fill="#475569" stroke="#94a3b8"/>';
    s += '<rect x="240" y="130" width="20" height="60" fill="#ea580c" stroke="#f97316"/>';
    s += '<circle cx="250" cy="140" r="14" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>';
    s += '<line x1="264" y1="140" x2="480" y2="140" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,3"/>';
    s += '<polygon points="480,140 470,125 470,155" fill="#f97316"/>';
    s += '<text x="360" y="250" fill="#f97316" font-size="12" text-anchor="middle">Total Station EDM Distance D = ' + val.toFixed(3) + ' m</text>';
  } else if (num === 47) { // Shear frame
    s += '<rect x="290" y="80" width="140" height="20" fill="#f97316" stroke="#ea580c"/>';
    s += '<line x1="310" y1="100" x2="310" y2="210" stroke="#cbd5e1" stroke-width="3"/>';
    s += '<line x1="410" y1="100" x2="410" y2="210" stroke="#cbd5e1" stroke-width="3"/>';
    s += '<rect x="270" y="210" width="180" height="15" fill="#334155"/>';
    s += '<text x="360" y="250" fill="#f97316" font-size="12" text-anchor="middle">Shear Frame Natural Freq ω_n = ' + Math.sqrt(1850 / val).toFixed(2) + ' rad/s (m = ' + val.toFixed(1) + ' kg)</text>';
  } else {
    s += '<rect x="250" y="75" width="220" height="160" fill="#1e293b" stroke="#f97316" stroke-width="2" rx="6"/>';
    s += '<text x="360" y="125" fill="#f97316" font-size="12" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="360" y="165" fill="#f8fafc" font-size="15" text-anchor="middle">' + cfg.shortInput + ': ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
    s += '<text x="360" y="200" fill="#38bdf8" font-size="11" text-anchor="middle">Surveying & Dynamics Channel Active</text>';
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
    renderResults();
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
