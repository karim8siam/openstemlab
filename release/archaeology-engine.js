'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.ArchaeologyModels;
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
  message('Adjust ' + cfg.shortInput + ', then execute archaeometric field acquisition.');
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

// Mode Switcher
document.querySelectorAll('.sim-mode-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.sim-mode-btn').forEach(b => {
      b.classList.remove('active');
      b.setAttribute('aria-selected', 'false');
    });
    btn.classList.add('active');
    btn.setAttribute('aria-selected', 'true');
    currentSimMode = btn.dataset.mode;
    draw();
  });
});

if ($('measure')) $('measure').addEventListener('click', () => {
  if (busy) return;
  busy = true;
  $('measure').disabled = true;
  message('Aligning field sensor array, calibrating isotopic/mineral standard, and acquiring telemetry…');

  let step = 0;
  const interval = setInterval(() => {
    step++;
    draw(step % 2 === 0 ? 1 : -1);
    if (step >= 5) {
      clearInterval(interval);
      busy = false;
      const p = params();
      measurement = model.predict(cfg.slug, p.input);
      if ($('readingValue')) $('readingValue').textContent = measurement.displayed.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit;
      if ($('recordReading')) $('recordReading').disabled = false;
      if ($('measure')) $('measure').disabled = false;
      if ($('liveState')) $('liveState').textContent = 'Acquisition completed: ' + cfg.rawLabel + ' = ' + measurement.displayed.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit + '.';
      message('Measurement captured. Click "+ Record observation" to save to the archaeological log.');
      draw();
    }
  }, 70);
});

if ($('recordReading')) $('recordReading').addEventListener('click', () => {
  if (!measurement) return;
  const p = params();
  const row = model.reading(cfg.slug, p.input, measurement.raw);
  rows.push(row);
  try {
    localStorage.setItem('openstemlab-' + cfg.slug + '-v1', JSON.stringify(rows));
  } catch (e) {}
  renderTable();
  $('recordReading').disabled = true;
  message('Observation recorded (' + rows.length + ' in log). Select new setpoint or repeat trial.');
});

if ($('clearData')) $('clearData').addEventListener('click', () => {
  if (rows.length === 0) return;
  if (confirm('Clear all recorded archaeological observations from your log?')) {
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
  const tbody = $('readingsBody') || $('dataTableBody');
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

  const emptyMsg = $('emptyReadings');
  if (emptyMsg) {
    emptyMsg.style.display = rows.length > 0 ? 'none' : 'block';
  }

  const cnt = $('notebookCount');
  if (cnt) cnt.textContent = rows.length;

  const fitRes = model.fit(rows);
  const fitBox = $('fitResult');
  if (fitBox) {
    if (fitRes && fitRes.n >= 3) {
      const est = model.estimate(cfg.slug, fitRes);
      fitBox.innerHTML = '<strong>' + cfg.targetName + ': ' + fmt(est.value, cfg.resultDecimals) + ' ' + cfg.resultUnit + '</strong>' +
                         '<p class="report-equation">Linear fit: <em>y</em> = ' + fmt(fitRes.slope, 4) + ' <em>x</em> ' + (fitRes.intercept >= 0 ? '+ ' : '- ') + fmt(Math.abs(fitRes.intercept), 4) + '</p>' +
                         '<p>Correlation coefficient: <em>R</em>² = ' + fitRes.r2.toFixed(6) + ' (<em>N</em> = ' + fitRes.n + ')</p>' +
                         '<p>Deviation vs Reference: ' + est.errorPercent.toFixed(3) + '% | Standard reference: ' + cfg.refValue + ' ' + cfg.resultUnit + '</p>';
    } else {
      fitBox.innerHTML = '<p>Log at least 3 distinct observations to compute regression fit and empirical archaeological parameter.</p>';
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

  let s = '<rect width="' + W + '" height="' + H + '" fill="#1c0d06" rx="6"/>';

  // Grid
  for (let i = 0; i <= 5; i++) {
    const gx = minX + (maxX - minX) * (i / 5);
    const gy = minY + (maxY - minY) * (i / 5);
    s += '<line x1="' + tx(gx) + '" y1="' + pad.top + '" x2="' + tx(gx) + '" y2="' + (pad.top + ph) + '" stroke="#431407" stroke-dasharray="2,2"/>';
    s += '<line x1="' + pad.left + '" y1="' + ty(gy) + '" x2="' + (pad.left + pw) + '" y2="' + ty(gy) + '" stroke="#431407" stroke-dasharray="2,2"/>';
    s += '<text x="' + tx(gx) + '" y="' + (H - 12) + '" fill="#fdba74" font-size="9" text-anchor="middle">' + fmt(gx, 1) + '</text>';
    s += '<text x="' + (pad.left - 8) + '" y="' + (ty(gy) + 3) + '" fill="#fdba74" font-size="9" text-anchor="end">' + fmt(gy, 1) + '</text>';
  }

  // Regression line
  if (fitRes && fitRes.n >= 2) {
    const x1 = minX;
    const y1 = (fitRes.slope * (x1 / cfg.xScale) + fitRes.intercept) * cfg.yScale;
    const x2 = maxX;
    const y2 = (fitRes.slope * (x2 / cfg.xScale) + fitRes.intercept) * cfg.yScale;
    s += '<line x1="' + tx(x1) + '" y1="' + ty(y1) + '" x2="' + tx(x2) + '" y2="' + ty(y2) + '" stroke="#ea580c" stroke-width="2"/>';
  }

  // Data points
  rows.forEach(r => {
    const px = tx(r.x * cfg.xScale);
    const py = ty(r.y * cfg.yScale);
    s += '<circle cx="' + px + '" cy="' + py + '" r="4.5" fill="#fed7aa" stroke="#c2410c" stroke-width="1.5"/>';
  });

  // Labels
  s += '<text x="' + (W / 2) + '" y="' + (H - 2) + '" fill="#fed7aa" font-size="10" text-anchor="middle">' + cfg.xAxis + '</text>';
  s += '<text transform="rotate(-90)" x="' + (-H / 2) + '" y="16" fill="#fed7aa" font-size="10" text-anchor="middle">' + cfg.yAxis + '</text>';

  svg.innerHTML = s;
}

function draw(animStep=0) {
  const svg = $('visualSvg');
  if (!svg) return;
  const p = params();
  const pred = model.predict(cfg.slug, p.input);
  const frac = Math.min(1, Math.max(0, (p.input - cfg.min) / (cfg.max - cfg.min || 1)));

  let html = '<rect width="520" height="280" fill="#1c0d06" rx="6"/>';

  if (currentSimMode === 'compare') {
    // Split screen: Live Excavated Specimen vs Chronological / Geological Reference Baseline
    html += '<line x1="260" y1="20" x2="260" y2="260" stroke="#7c2d12" stroke-width="2" stroke-dasharray="4,4"/>';
    html += '<text x="130" y="35" fill="#fdba74" font-size="11" font-weight="600" text-anchor="middle">LIVE ARTIFACT / MATRIX</text>';
    html += '<text x="390" y="35" fill="#fed7aa" font-size="11" font-weight="600" text-anchor="middle">CHRONOLOGICAL &amp; ISOTOPIC BASELINE</text>';

    // Left: Real excavated artifact / trench stratum
    html += '<rect x="25" y="55" width="210" height="180" fill="#2a140a" stroke="#7c2d12" rx="5"/>';
    const defl = 12 * frac + animStep;
    // Stratified sediment profile
    html += '<rect x="35" y="70" width="190" height="35" fill="#451a03" opacity="0.9"/>';
    html += '<rect x="35" y="105" width="190" height="40" fill="#78350f" opacity="0.85"/>';
    html += '<rect x="35" y="145" width="190" height="45" fill="#92400e" opacity="0.8"/>';
    html += '<line x1="35" y1="' + (125 + defl) + '" x2="225" y2="' + (125 + defl) + '" stroke="#ea580c" stroke-width="2"/>';
    html += '<circle cx="' + (130) + '" cy="' + (125 + defl) + '" r="6" fill="#fed7aa" stroke="#c2410c" stroke-width="2"/>';
    html += '<text x="130" y="215" fill="#fdba74" font-size="9" text-anchor="middle">Measured Value: ' + pred.displayed.toFixed(2) + ' ' + cfg.rawUnit + '</text>';

    // Right: Ideal reference calibration curve
    html += '<rect x="285" y="55" width="210" height="180" fill="#2a140a" stroke="#7c2d12" rx="5"/>';
    html += '<path d="M305,200 C340,170 410,110 475,75" stroke="#f97316" stroke-width="2" fill="none" stroke-dasharray="3,3"/>';
    const idealY = 200 - 120 * frac;
    html += '<circle cx="' + (305 + 165 * frac) + '" cy="' + idealY + '" r="5" fill="#fdba74"/>';
    html += '<text x="390" y="215" fill="#fed7aa" font-size="9" text-anchor="middle">Reference Target: ' + (cfg.refValue || 0) + ' ' + cfg.resultUnit + '</text>';
  } else if (currentSimMode === 'sandbox') {
    // Sandbox: Multi-Parameter Stratigraphic & Taphonomic Simulation
    html += '<rect x="20" y="25" width="480" height="230" fill="#2a140a" stroke="#7c2d12" rx="6"/>';
    html += '<text x="260" y="48" fill="#fed7aa" font-size="12" font-weight="600" text-anchor="middle">ARCHAEOMETRIC CONTEXT &amp; FIELD TAPHONOMY SIMULATOR</text>';

    html += '<rect x="40" y="70" width="130" height="65" fill="#431407" stroke="#7c2d12" rx="4"/>';
    html += '<text x="105" y="90" fill="#fdba74" font-size="9" text-anchor="middle">GEOCHRONOLOGY</text>';
    html += '<text x="105" y="112" fill="#fed7aa" font-size="13" font-weight="700" text-anchor="middle">HOLOCENE / INTCAL</text>';

    html += '<rect x="195" y="70" width="130" height="65" fill="#431407" stroke="#7c2d12" rx="4"/>';
    html += '<text x="260" y="90" fill="#fdba74" font-size="9" text-anchor="middle">SETPOINT INPUT</text>';
    html += '<text x="260" y="112" fill="#fed7aa" font-size="14" font-weight="700" text-anchor="middle">' + p.input.toFixed(1) + ' ' + cfg.inputUnit + '</text>';

    html += '<rect x="350" y="70" width="130" height="65" fill="#431407" stroke="#7c2d12" rx="4"/>';
    html += '<text x="415" y="90" fill="#fdba74" font-size="9" text-anchor="middle">FIELD TELEMETRY</text>';
    html += '<text x="415" y="112" fill="#fed7aa" font-size="14" font-weight="700" text-anchor="middle">' + pred.displayed.toFixed(2) + ' ' + cfg.rawUnit + '</text>';

    // Animated excavation grid & artifact distribution
    html += '<g transform="translate(60, 155)">';
    for (let i = 0; i < 20; i++) {
      const x = i * 20;
      html += '<line x1="' + x + '" y1="0" x2="' + x + '" y2="70" stroke="#7c2d12" stroke-width="1.5"/>';
    }
    for (let j = 0; j < 4; j++) {
      const y = j * 20 + 5;
      html += '<line x1="0" y1="' + y + '" x2="380" y2="' + y + '" stroke="#ea580c" stroke-width="1.5" stroke-dasharray="6,6"/>';
    }
    html += '</g>';
    html += '<text x="260" y="246" fill="#ea580c" font-size="9" text-anchor="middle">Stratigraphic context matrix dynamically resolving Harris phasing &amp; taphonomic boundaries</text>';
  } else {
    // Bench Mode: High-Precision Field & Laboratory Archaeometric Visualizer
    html += '<rect x="30" y="20" width="460" height="240" fill="#240e07" stroke="#431407" rx="8"/>';

    // Top Header
    html += '<text x="50" y="42" fill="#fed7aa" font-size="11" font-weight="600">' + cfg.title.toUpperCase() + '</text>';
    html += '<text x="470" y="42" fill="#fdba74" font-size="10" text-anchor="end">CALIBRATED FIELD PROTOCOL</text>';
    html += '<line x1="50" y1="50" x2="470" y2="50" stroke="#7c2d12" stroke-width="1"/>';

    // Excavation Profile / Specimen Sensor Chamber
    html += '<rect x="60" y="65" width="160" height="150" fill="#1c0d06" stroke="#ea580c" rx="4"/>';
    // Stratum layers
    html += '<rect x="65" y="70" width="150" height="30" fill="#78350f" opacity="0.9"/>';
    html += '<rect x="65" y="100" width="150" height="35" fill="#92400e" opacity="0.85"/>';
    html += '<rect x="65" y="135" width="150" height="40" fill="#b45309" opacity="0.8"/>';
    html += '<rect x="65" y="175" width="150" height="35" fill="#451a03" opacity="0.95"/>';

    // Sensor probe / lens traversing the profile
    const probeY = 75 + 110 * frac + animStep;
    html += '<line x1="50" y1="' + probeY + '" x2="225" y2="' + probeY + '" stroke="#fed7aa" stroke-width="2" stroke-dasharray="3,3"/>';
    html += '<circle cx="140" cy="' + probeY + '" r="7" fill="#ea580c" stroke="#fed7aa" stroke-width="2"/>';

    // Meter Dial / Spectrometric Gauge
    html += '<g transform="translate(350, 140)">';
    html += '<circle cx="0" cy="0" r="62" fill="#2a140a" stroke="#7c2d12" stroke-width="3"/>';
    html += '<circle cx="0" cy="0" r="54" fill="#1c0d06" stroke="#431407" stroke-width="1"/>';
    for (let a = 0; a < 12; a++) {
      const rad = (a * 30 - 90) * Math.PI / 180;
      html += '<line x1="' + (46 * Math.cos(rad)) + '" y1="' + (46 * Math.sin(rad)) + '" x2="' + (52 * Math.cos(rad)) + '" y2="' + (52 * Math.sin(rad)) + '" stroke="#ea580c" stroke-width="1.5"/>';
    }
    const angle = (-120 + 240 * frac) * Math.PI / 180;
    html += '<line x1="0" y1="0" x2="' + (44 * Math.cos(angle)) + '" y2="' + (44 * Math.sin(angle)) + '" stroke="#fdba74" stroke-width="2.5"/>';
    html += '<circle cx="0" cy="0" r="4" fill="#fed7aa"/>';
    html += '<text x="0" y="24" fill="#fed7aa" font-size="10" font-weight="700" text-anchor="middle">' + pred.displayed.toFixed(1) + '</text>';
    html += '<text x="0" y="36" fill="#fdba74" font-size="8" text-anchor="middle">' + cfg.rawUnit + '</text>';
    html += '</g>';

    // Status readout overlay
    html += '<rect x="230" y="222" width="245" height="24" fill="#2a140a" stroke="#7c2d12" rx="3"/>';
    html += '<text x="352" y="238" fill="#fed7aa" font-size="9" text-anchor="middle">' + cfg.shortInput + ': ' + p.input.toFixed(1) + ' ' + cfg.inputUnit + ' ➔ ' + pred.displayed.toFixed(2) + ' ' + cfg.rawUnit + '</text>';
  }

  svg.innerHTML = html;
}

// Reset apparatus button
if ($('resetApparatus')) $('resetApparatus').addEventListener('click', () => {
  if ($('independent')) $('independent').value = cfg.initial;
  if ($('independentNumber')) $('independentNumber').value = cfg.initial;
  update();
});

// Initial state render
update();
renderTable();
