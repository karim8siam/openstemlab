'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.BiomedModels;
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
  message('Adjust ' + cfg.shortInput + ', then execute biomedical measurement.');
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
      message('Use a value between ' + cfg.min + ' and ' + cfg.max + ' ' + cfg.inputUnit + '.', true);
      return;
    }
    if ($('independent')) $('independent').value = v;
    update();
  });
}

if ($('resetApparatus')) {
  $('resetApparatus').onclick = () => {
    if (busy) return;
    if ($('independent')) $('independent').value = cfg.initial;
    if ($('independentNumber')) $('independentNumber').value = cfg.initial;
    update();
    message('Biomedical apparatus telemetry reset. Notebook observations preserved.');
  };
}

if ($('measure')) {
  $('measure').onclick = async () => {
    if (busy) return;
    const p = params();
    const prediction = model.predict(cfg.slug, p.input);
    if (!prediction.valid) {
      message('Select a valid parameter between ' + cfg.min + ' and ' + cfg.max + '.', true);
      return;
    }
    busy = true;
    $('measure').disabled = true;
    if ($('recordReading')) $('recordReading').disabled = true;
    if ($('independent')) $('independent').disabled = true;
    if ($('independentNumber')) $('independentNumber').disabled = true;
    message('Stabilizing physiological sensors and sampling telemetry for ' + cfg.shortInput + ' = ' + p.input + ' ' + cfg.inputUnit + '…');
    await new Promise(resolve => setTimeout(resolve, 200));
    const raw = prediction.raw;
    measurement = model.reading(cfg.slug, p.input, raw);
    busy = false;
    if ($('independent')) $('independent').disabled = false;
    if ($('independentNumber')) $('independentNumber').disabled = false;
    $('measure').disabled = false;
    if ($('recordReading')) $('recordReading').disabled = false;
    if ($('readingValue')) $('readingValue').textContent = raw.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit;
    if ($('liveState')) $('liveState').textContent = 'Physiological equilibrium achieved. Ready to record observation.';
    message(cfg.shortInput + ' = ' + p.input + ' recorded: ' + cfg.rawLabel + ' = ' + raw + ' ' + cfg.rawUnit + '. Click Record observation.');
    draw();
  };
}

if ($('recordReading')) {
  $('recordReading').onclick = () => {
    if (!measurement) return;
    if (rows.length >= 100) {
      message('Observation notebook full (100 trials maximum). Export CSV or clear.', true);
      return;
    }
    rows.push({ ...measurement });
    measurement = null;
    $('recordReading').disabled = true;
    persist();
    message('Observation ' + rows.length + ' logged. Adjust ' + cfg.shortInput + ' for next clinical trial point.');
  };
}

function persist() {
  try {
    localStorage.setItem('openstemlab-' + cfg.slug + '-v1', JSON.stringify(rows));
  } catch (e) {}
  renderResults();
}

function renderResults() {
  const f = model.fit(rows);
  if ($('notebookCount')) $('notebookCount').textContent = rows.length;
  if ($('emptyReadings')) $('emptyReadings').hidden = rows.length > 0;
  if ($('downloadReadings')) $('downloadReadings').disabled = !rows.length;
  if ($('clearReadings')) $('clearReadings').disabled = !rows.length;

  if ($('readingRows')) {
    $('readingRows').innerHTML = rows.map((r, i) =>
      '<tr><td>' + (i + 1) + '</td><td>' + r.input.toFixed(cfg.inputDecimals) + '</td><td>' +
      r.raw.toFixed(cfg.rawDecimals) + '</td><td>' + fmt(r.x * cfg.xScale) + '</td><td>' +
      fmt(r.y * cfg.yScale) + '</td><td><button class="text-button" data-remove="' + i +
      '" aria-label="Remove observation ' + (i + 1) + '">×</button></td></tr>'
    ).join('');
    document.querySelectorAll('[data-remove]').forEach(b => {
      b.onclick = () => {
        rows.splice(+b.dataset.remove, 1);
        persist();
      };
    });
  }

  if ($('fitSummary')) {
    if (f) {
      const result = model.estimate(cfg.slug, f);
      const pct = Math.abs(result.value - result.reference) / Math.abs(result.reference) * 100;
      $('fitSummary').innerHTML = '<strong>' + fmt(result.value * cfg.resultScale, cfg.resultDecimals) + ' ' +
        cfg.resultUnit + '</strong><p>Estimated ' + cfg.targetName + '<br>Gradient m: ' + fmt(f.m) +
        '<br>Intercept b: ' + fmt(f.b) + '<br>R²: ' + f.r2.toFixed(6) +
        '<br>Difference from reference: ' + pct.toFixed(4) + '%<br>Standard error: ' +
        fmt(result.se * cfg.resultScale) + ' ' + cfg.resultUnit + '</p><p>Biomedical model verified by ordinary least-squares regression.</p>';
    } else {
      $('fitSummary').innerHTML = '<p>Record at least three distinct observations across the parameter range to evaluate ordinary least-squares fit and extract ' + cfg.targetName + '.</p>';
    }
  }

  drawPlot(f);
}

function drawPlot(f) {
  const plot = $('labPlot');
  if (!plot) return;
  const left = 68, right = 610, top = 28, bottom = 280;
  let xs = rows.map(r => r.x * cfg.xScale), ys = rows.map(r => r.y * cfg.yScale);
  let xmin = xs.length ? Math.min(...xs) : cfg.emptyX;
  let xmax = xs.length ? Math.max(...xs) : cfg.emptyX + 1;
  let ymin = ys.length ? Math.min(...ys) : cfg.emptyY;
  let ymax = ys.length ? Math.max(...ys) : cfg.emptyY + 1;
  const dx = (xmax - xmin) || Math.max(Math.abs(xmax) * 0.2, 1);
  const dy = (ymax - ymin) || Math.max(Math.abs(ymax) * 0.2, 1);
  xmin -= dx * 0.12; xmax += dx * 0.12; ymin -= dy * 0.15; ymax += dy * 0.15;
  const px = x => left + (x - xmin) / (xmax - xmin) * (right - left);
  const py = y => bottom - (y - ymin) / (ymax - ymin) * (bottom - top);

  let svg = '<rect width="650" height="340" fill="#042f2e"/>';
  for (let i = 0; i <= 5; i++) {
    const gx = left + i * (right - left) / 5;
    const gy = top + i * (bottom - top) / 5;
    svg += '<line x1="' + gx + '" y1="' + top + '" x2="' + gx + '" y2="' + bottom + '" stroke="#134e4a" stroke-width="1" stroke-dasharray="2,3"/>';
    svg += '<line x1="' + left + '" y1="' + gy + '" x2="' + right + '" y2="' + gy + '" stroke="#134e4a" stroke-width="1" stroke-dasharray="2,3"/>';
    const valX = xmin + i * (xmax - xmin) / 5;
    const valY = ymax - i * (ymax - ymin) / 5;
    svg += '<text x="' + gx + '" y="' + (bottom + 18) + '" fill="#5eead4" font-size="10" text-anchor="middle">' + fmt(valX, 2) + '</text>';
    svg += '<text x="' + (left - 10) + '" y="' + (gy + 3) + '" fill="#5eead4" font-size="10" text-anchor="end">' + fmt(valY, 2) + '</text>';
  }
  svg += '<text x="' + ((left + right) / 2) + '" y="325" fill="#ccfbf1" font-size="12" text-anchor="middle">' + cfg.xAxis + '</text>';
  svg += '<text x="18" y="' + ((top + bottom) / 2) + '" fill="#ccfbf1" font-size="12" text-anchor="middle" transform="rotate(-90 18 ' + ((top + bottom) / 2) + ')">' + cfg.yAxis + '</text>';

  if (f && rows.length >= 2) {
    const x1 = xmin, x2 = xmax;
    const y1 = f.m * (x1 / cfg.xScale) + f.b;
    const y2 = f.m * (x2 / cfg.xScale) + f.b;
    svg += '<line x1="' + px(x1) + '" y1="' + py(y1 * cfg.yScale) + '" x2="' + px(x2) + '" y2="' + py(y2 * cfg.yScale) + '" stroke="#14b8a6" stroke-width="2.5"/>';
  }

  rows.forEach((r, i) => {
    const cx = px(r.x * cfg.xScale), cy = py(r.y * cfg.yScale);
    svg += '<circle cx="' + cx + '" cy="' + cy + '" r="5.5" fill="#2dd4bf" stroke="#042f2e" stroke-width="1.5"/>';
    svg += '<text x="' + cx + '" y="' + (cy - 8) + '" fill="#fef08a" font-size="9" text-anchor="middle" font-weight="bold">' + (i + 1) + '</text>';
  });

  plot.innerHTML = svg;
}

// Interactive Simulation Mode Switching
document.querySelectorAll('.sim-mode-btn').forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll('.sim-mode-btn').forEach(b => {
      b.classList.remove('active');
      b.setAttribute('aria-selected', 'false');
    });
    btn.classList.add('active');
    btn.setAttribute('aria-selected', 'true');
    currentSimMode = btn.dataset.sim || 'bench';
    draw();
  };
});

function draw() {
  const svg = $('apparatusDiagram');
  if (!svg) return;
  const p = params();
  const val = p.input;
  const num = cfg.number;
  const mode = currentSimMode;

  let out = '<defs>';
  out += '<pattern id="biomedGrid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M 25 0 L 0 0 0 25" fill="none" stroke="#115e59" stroke-width="0.8" opacity="0.5"/></pattern>';
  out += '<linearGradient id="tealGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#0f766e" stop-opacity="0.9"/><stop offset="100%" stop-color="#2dd4bf" stop-opacity="0.3"/></linearGradient>';
  out += '<linearGradient id="pulseGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ef4444" stop-opacity="0.8"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0.3"/></linearGradient>';
  out += '<linearGradient id="beamGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8"/><stop offset="100%" stop-color="#0284c7" stop-opacity="0.1"/></linearGradient>';
  out += '</defs>';

  out += '<rect width="100%" height="100%" fill="#042f2e"/>';
  out += '<rect width="100%" height="100%" fill="url(#biomedGrid)"/>';

  // Header Telemetry Bar
  out += '<rect x="15" y="12" width="690" height="26" rx="4" fill="#021f1e" stroke="#0d9488" stroke-width="1"/>';
  out += '<text x="25" y="29" fill="#2dd4bf" font-size="11" font-weight="bold">BIOMEDICAL ENGINEERING TELEMETRY · LAB ' + String(num).padStart(2, '0') + '</text>';
  out += '<text x="440" y="29" fill="#5eead4" font-size="10">VIEW: ' + mode.toUpperCase() + ' | PARAMETER: ' + cfg.shortInput + ' = ' + val + ' ' + cfg.inputUnit + '</text>';

  if (num <= 8) {
    out += drawModule1Sensors(val, mode, num);
  } else if (num <= 17) {
    out += drawModule2Biosignals(val, mode, num);
  } else if (num <= 26) {
    out += drawModule3Biomechanics(val, mode, num);
  } else if (num <= 34) {
    out += drawModule4Hemodynamics(val, mode, num);
  } else {
    out += drawModule5ImagingDevices(val, mode, num);
  }

  svg.innerHTML = out;
}

function drawModule1Sensors(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="55" width="640" height="210" fill="#031e1d" stroke="#0f766e" stroke-width="1.5" rx="6"/>';

  if (num === 1) {
    // Thermistor Wheatstone bridge bath
    s += '<rect x="80" y="80" width="220" height="150" fill="#042f2e" stroke="#14b8a6" stroke-width="1.5" rx="4"/>';
    s += '<rect x="90" y="120" width="200" height="100" fill="#0d9488" opacity="0.4" rx="2"/>';
    s += '<text x="190" y="105" fill="#5eead4" font-size="11" text-anchor="middle" font-weight="bold">CALIBRATION WATER BATH</text>';
    s += '<path d="M 180 80 L 180 180" stroke="#f59e0b" stroke-width="4"/>';
    s += '<circle cx="180" cy="180" r="7" fill="#ef4444"/>';
    s += '<text x="195" y="185" fill="#fde047" font-size="10">NTC Bead (T = ' + val.toFixed(1) + ' °C)</text>';
    // Bridge schematic
    s += '<polygon points="460,90 530,150 460,210 390,150" fill="none" stroke="#2dd4bf" stroke-width="2"/>';
    s += '<circle cx="460" cy="90" r="3" fill="#5eead4"/><circle cx="530" cy="150" r="3" fill="#5eead4"/><circle cx="460" cy="210" r="3" fill="#5eead4"/><circle cx="390" cy="150" r="3" fill="#5eead4"/>';
    s += '<line x1="390" y1="150" x2="530" y2="150" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="3,3"/>';
    const vbr = (18.5 * val - 647.5);
    s += '<text x="460" y="145" fill="#f43f5e" font-size="11" text-anchor="middle" font-weight="bold">V_br = ' + vbr.toFixed(1) + ' mV</text>';
  } else if (num === 2) {
    // Strain gauge cantilever
    const defl = val * 6;
    s += '<rect x="80" y="120" width="40" height="80" fill="#334155" stroke="#94a3b8" stroke-width="2"/>';
    s += '<path d="M 120 150 Q 280 ' + (150 + defl * 0.4) + ' 440 ' + (150 + defl) + '" fill="none" stroke="#cbd5e1" stroke-width="8"/>';
    s += '<rect x="150" y="142" width="45" height="6" fill="#f59e0b"/>';
    s += '<rect x="150" y="152" width="45" height="6" fill="#38bdf8"/>';
    s += '<line x1="440" y1="' + (150 + defl) + '" x2="440" y2="' + (195 + defl) + '" stroke="#ef4444" stroke-width="3"/>';
    s += '<polygon points="436,' + (195 + defl) + ' 444,' + (195 + defl) + ' 440,' + (205 + defl) + '" fill="#ef4444"/>';
    s += '<text x="440" y="' + (222 + defl) + '" fill="#f87171" font-size="11" text-anchor="middle" font-weight="bold">F = ' + val.toFixed(1) + ' N</text>';
  } else {
    // Sensor transducer bench
    s += '<rect x="100" y="90" width="260" height="130" fill="#042f2e" stroke="#14b8a6" stroke-width="1.5" rx="4"/>';
    s += '<circle cx="230" cy="155" r="45" fill="url(#tealGrad)" stroke="#2dd4bf" stroke-width="2"/>';
    s += '<text x="230" y="150" fill="#ffffff" font-size="11" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="230" y="170" fill="#5eead4" font-size="10" text-anchor="middle">' + cfg.shortInput + ': ' + val + ' ' + cfg.inputUnit + '</text>';
    s += '<line x1="360" y1="155" x2="470" y2="155" stroke="#f59e0b" stroke-width="3" stroke-dasharray="4,2"/>';
    s += '<rect x="470" y="110" width="160" height="90" fill="#021f1e" stroke="#0d9488" stroke-width="1.5" rx="4"/>';
    s += '<text x="550" y="135" fill="#5eead4" font-size="10" text-anchor="middle">TRANSDUCER OUTPUT</text>';
    s += '<text x="550" y="165" fill="#2dd4bf" font-size="16" text-anchor="middle" font-weight="bold">' + cfg.rawLabel + '</text>';
  }
  return s;
}

function drawModule2Biosignals(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="55" width="640" height="210" fill="#031e1d" stroke="#0f766e" stroke-width="1.5" rx="6"/>';

  if (num === 9) {
    // Einthoven ECG triangle
    s += '<polygon points="340,80 200,210 480,210" fill="none" stroke="#0d9488" stroke-width="2" stroke-dasharray="4,4"/>';
    s += '<circle cx="340" cy="80" r="8" fill="#ef4444"/><text x="340" y="72" fill="#f87171" font-size="10" text-anchor="middle">RA</text>';
    s += '<circle cx="200" cy="210" r="8" fill="#eab308"/><text x="180" y="215" fill="#fde047" font-size="10">LA</text>';
    s += '<circle cx="480" cy="210" r="8" fill="#22c55e"/><text x="495" y="215" fill="#4ade80" font-size="10">LL</text>';
    // Cardiac vector arrow
    const angle = 45 + val * 15;
    const rad = angle * Math.PI / 180;
    const vx = 340 + 70 * Math.cos(rad);
    const vy = 160 + 70 * Math.sin(rad);
    s += '<line x1="340" y1="160" x2="' + vx + '" y2="' + vy + '" stroke="#38bdf8" stroke-width="3.5"/>';
    s += '<text x="340" y="150" fill="#7dd3fc" font-size="11" text-anchor="middle" font-weight="bold">Cardiac Mean Axis θ</text>';
  } else if (num === 10) {
    // Pulse oximeter PPG finger
    s += '<rect x="120" y="110" width="240" height="90" rx="20" fill="#be123c" stroke="#f43f5e" stroke-width="2"/>';
    s += '<text x="240" y="155" fill="#ffe4e6" font-size="12" text-anchor="middle" font-weight="bold">FINGER ARTERIAL BED</text>';
    s += '<circle cx="180" cy="90" r="12" fill="#ef4444"/><text x="180" y="70" fill="#fca5a5" font-size="9" text-anchor="middle">RED (660 nm)</text>';
    s += '<circle cx="300" cy="90" r="12" fill="#881337"/><text x="300" y="70" fill="#fda4af" font-size="9" text-anchor="middle">IR (940 nm)</text>';
    s += '<rect x="420" y="100" width="190" height="100" fill="#021f1e" stroke="#14b8a6" stroke-width="1.5" rx="4"/>';
    const spo2 = Math.min(100, Math.max(70, -25.0 * val + 110.0));
    s += '<text x="515" y="130" fill="#5eead4" font-size="11" text-anchor="middle">PULSE OXIMETRY</text>';
    s += '<text x="515" y="165" fill="#2dd4bf" font-size="22" text-anchor="middle" font-weight="bold">SpO₂: ' + spo2.toFixed(1) + ' %</text>';
    s += '<text x="515" y="188" fill="#99f6e4" font-size="10" text-anchor="middle">Modulation Ratio R = ' + val.toFixed(2) + '</text>';
  } else {
    // Biosignal waveform monitor
    s += '<rect x="80" y="80" width="560" height="150" fill="#021f1e" stroke="#0f766e" stroke-width="2" rx="4"/>';
    let pts = [];
    for (let x = 90; x <= 620; x += 10) {
      const y = 155 - Math.sin((x - 90) * 0.08) * (20 + (val % 5) * 5) - Math.cos((x - 90) * 0.15) * 10;
      pts.push(x + ',' + y);
    }
    s += '<polyline points="' + pts.join(' ') + '" fill="none" stroke="#2dd4bf" stroke-width="2"/>';
    s += '<text x="100" y="105" fill="#5eead4" font-size="11" font-weight="bold">REAL-TIME BIOSIGNAL ACQUISITION · ' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<text x="100" y="125" fill="#99f6e4" font-size="10">Channel Input: ' + cfg.shortInput + ' = ' + val + ' ' + cfg.inputUnit + '</text>';
  }
  return s;
}

function drawModule3Biomechanics(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="55" width="640" height="210" fill="#031e1d" stroke="#0f766e" stroke-width="1.5" rx="6"/>';

  if (num === 18) {
    // Cortical bone tensile test
    s += '<rect x="220" y="70" width="80" height="25" fill="#475569" stroke="#94a3b8" stroke-width="1.5"/>';
    s += '<rect x="220" y="225" width="80" height="25" fill="#475569" stroke="#94a3b8" stroke-width="1.5"/>';
    // Dog-bone bone specimen
    s += '<path d="M 240 95 L 280 95 L 265 130 L 265 190 L 280 225 L 240 225 L 255 190 L 255 130 Z" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>';
    s += '<line x1="260" y1="135" x2="330" y2="135" stroke="#38bdf8" stroke-dasharray="2,2"/>';
    s += '<line x1="260" y1="185" x2="330" y2="185" stroke="#38bdf8" stroke-dasharray="2,2"/>';
    s += '<text x="340" y="163" fill="#38bdf8" font-size="10">Laser Gauge L₀ (25 mm)</text>';
    s += '<line x1="260" y1="70" x2="260" y2="40" stroke="#ef4444" stroke-width="3"/>';
    s += '<polygon points="256,40 264,40 260,30" fill="#ef4444"/>';
    s += '<text x="260" y="25" fill="#f87171" font-size="10" text-anchor="middle" font-weight="bold">TENSILE LOAD</text>';
    // Stress readout
    s += '<rect x="440" y="100" width="190" height="100" fill="#021f1e" stroke="#14b8a6" stroke-width="1.5" rx="4"/>';
    s += '<text x="535" y="130" fill="#5eead4" font-size="11" text-anchor="middle">TENSILE STRESS</text>';
    s += '<text x="535" y="165" fill="#2dd4bf" font-size="20" text-anchor="middle" font-weight="bold">' + (17.5 * val).toFixed(1) + ' MPa</text>';
    s += '<text x="535" y="188" fill="#99f6e4" font-size="10" text-anchor="middle">Strain ε = ' + val.toFixed(1) + ' mstrain</text>';
  } else if (num === 20) {
    // 4-point bending bone plate
    s += '<rect x="140" y="145" width="380" height="15" rx="3" fill="#64748b" stroke="#cbd5e1" stroke-width="1.5"/>';
    // Support rollers
    s += '<circle cx="180" cy="168" r="8" fill="#38bdf8"/><circle cx="480" cy="168" r="8" fill="#38bdf8"/>';
    s += '<text x="330" y="195" fill="#7dd3fc" font-size="10" text-anchor="middle">OUTER SPAN L = 100 mm</text>';
    // Loading rollers
    const dy = val * 0.02;
    s += '<circle cx="280" cy="' + (137 + dy) + '" r="8" fill="#ef4444"/><circle cx="380" cy="' + (137 + dy) + '" r="8" fill="#ef4444"/>';
    s += '<line x1="280" y1="' + (125 + dy) + '" x2="280" y2="' + (100 + dy) + '" stroke="#ef4444" stroke-width="2"/>';
    s += '<line x1="380" y1="' + (125 + dy) + '" x2="380" y2="' + (100 + dy) + '" stroke="#ef4444" stroke-width="2"/>';
    s += '<text x="330" y="' + (95 + dy) + '" fill="#f87171" font-size="10" text-anchor="middle" font-weight="bold">TOTAL LOAD W = ' + val + ' N</text>';
  } else {
    // Biomechanical load stage
    s += '<rect x="120" y="90" width="420" height="130" fill="#042f2e" stroke="#14b8a6" stroke-width="1.5" rx="4"/>';
    s += '<text x="330" y="125" fill="#5eead4" font-size="13" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<rect x="230" y="145" width="200" height="45" fill="#021f1e" stroke="#2dd4bf" stroke-width="1" rx="3"/>';
    s += '<text x="330" y="172" fill="#fde047" font-size="12" text-anchor="middle">' + cfg.shortInput + ': ' + val + ' ' + cfg.inputUnit + '</text>';
  }
  return s;
}

function drawModule4Hemodynamics(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="55" width="640" height="210" fill="#031e1d" stroke="#0f766e" stroke-width="1.5" rx="6"/>';

  if (num === 28) {
    // Microvascular flow resistance
    s += '<rect x="100" y="110" width="380" height="70" fill="#450a0a" stroke="#dc2626" stroke-width="2" rx="4"/>';
    for (let y = 125; y <= 165; y += 12) {
      s += '<line x1="120" y1="' + y + '" x2="460" y2="' + y + '" stroke="#fca5a5" stroke-dasharray="8,4" stroke-width="1.5"/>';
    }
    s += '<text x="290" y="148" fill="#ffffff" font-size="11" text-anchor="middle" font-weight="bold">MICROVASCULAR NETWORK (D = 120 μm)</text>';
    s += '<rect x="500" y="100" width="150" height="90" fill="#021f1e" stroke="#14b8a6" stroke-width="1.5" rx="4"/>';
    s += '<text x="575" y="125" fill="#5eead4" font-size="10" text-anchor="middle">PRESSURE DROP</text>';
    s += '<text x="575" y="155" fill="#2dd4bf" font-size="18" text-anchor="middle" font-weight="bold">' + (3.6 * val).toFixed(1) + ' kPa</text>';
    s += '<text x="575" y="178" fill="#99f6e4" font-size="9" text-anchor="middle">Q = ' + val.toFixed(1) + ' mL/min</text>';
  } else if (num === 30) {
    // Bileaflet mechanical heart valve
    s += '<circle cx="260" cy="155" r="55" fill="#1e293b" stroke="#cbd5e1" stroke-width="4"/>';
    s += '<polygon points="230,130 255,155 245,175 220,150" fill="#0284c7"/>';
    s += '<polygon points="290,130 265,155 275,175 300,150" fill="#0284c7"/>';
    s += '<text x="260" y="160" fill="#ffffff" font-size="10" text-anchor="middle">BILEAFLET</text>';
    s += '<rect x="420" y="100" width="200" height="100" fill="#021f1e" stroke="#14b8a6" stroke-width="1.5" rx="4"/>';
    const dp = 3.85 * val * val;
    s += '<text x="520" y="130" fill="#5eead4" font-size="11" text-anchor="middle">TRANSVALVULAR GRADIENT</text>';
    s += '<text x="520" y="165" fill="#2dd4bf" font-size="20" text-anchor="middle" font-weight="bold">' + dp.toFixed(1) + ' mmHg</text>';
    s += '<text x="520" y="188" fill="#99f6e4" font-size="10" text-anchor="middle">Jet Velocity v = ' + val.toFixed(1) + ' m/s</text>';
  } else {
    // Hemodynamic perfusion circuit
    s += '<path d="M 120 155 Q 260 90 400 155 T 580 155" fill="none" stroke="#ef4444" stroke-width="6"/>';
    s += '<text x="340" y="135" fill="#fca5a5" font-size="12" text-anchor="middle" font-weight="bold">CARDIOVASCULAR FLOW CIRCUIT</text>';
    s += '<rect x="230" y="165" width="220" height="40" fill="#021f1e" stroke="#2dd4bf" stroke-width="1" rx="3"/>';
    s += '<text x="340" y="190" fill="#fde047" font-size="11" text-anchor="middle">' + cfg.shortInput + ': ' + val + ' ' + cfg.inputUnit + '</text>';
  }
  return s;
}

function drawModule5ImagingDevices(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="55" width="640" height="210" fill="#031e1d" stroke="#0f766e" stroke-width="1.5" rx="6"/>';

  if (num === 35) {
    // Ultrasound attenuation tank
    s += '<rect x="80" y="80" width="60" height="80" fill="#334155" stroke="#38bdf8" stroke-width="2" rx="4"/>';
    s += '<text x="110" y="125" fill="#7dd3fc" font-size="9" text-anchor="middle">3.5 MHz PZT</text>';
    const zx = 160 + val * 35;
    s += '<path d="M 140 100 L ' + zx + ' 75 L ' + zx + ' 205 L 140 180 Z" fill="url(#beamGrad)" stroke="#38bdf8" stroke-width="1.2"/>';
    s += '<line x1="' + zx + '" y1="70" x2="' + zx + '" y2="210" stroke="#f59e0b" stroke-width="2.5"/>';
    s += '<circle cx="' + zx + '" cy="140" r="5" fill="#ef4444"/>';
    s += '<text x="' + zx + '" y="228" fill="#fde047" font-size="10" text-anchor="middle">Hydrophone (z = ' + val.toFixed(1) + ' cm)</text>';
  } else if (num === 36) {
    // Diagnostic X-ray narrow beam
    s += '<circle cx="120" cy="155" r="28" fill="#451a03" stroke="#f59e0b" stroke-width="2"/>';
    s += '<text x="120" y="160" fill="#fde047" font-size="9" text-anchor="middle">80 kVp TUBE</text>';
    s += '<line x1="150" y1="155" x2="300" y2="155" stroke="#facc15" stroke-width="3"/>';
    // Aluminum filter
    const th = val * 5;
    s += '<rect x="300" y="115" width="' + th + '" height="80" fill="#94a3b8" stroke="#cbd5e1" stroke-width="1.5"/>';
    s += '<text x="' + (300 + th/2) + '" y="105" fill="#e2e8f0" font-size="10" text-anchor="middle">Al Filter (' + val.toFixed(1) + ' mm)</text>';
    s += '<line x1="' + (300 + th) + '" y1="155" x2="480" y2="155" stroke="#facc15" stroke-dasharray="4,2" stroke-width="2"/>';
    s += '<rect x="480" y="125" width="50" height="60" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5" rx="3"/>';
    s += '<text x="505" y="160" fill="#7dd3fc" font-size="9" text-anchor="middle">Ion Chamber</text>';
  } else {
    // Medical device workbench
    s += '<rect x="120" y="90" width="440" height="130" fill="#042f2e" stroke="#14b8a6" stroke-width="1.5" rx="4"/>';
    s += '<text x="340" y="130" fill="#5eead4" font-size="13" text-anchor="middle" font-weight="bold">' + cfg.shortTitle.toUpperCase() + '</text>';
    s += '<rect x="230" y="150" width="220" height="40" fill="#021f1e" stroke="#2dd4bf" stroke-width="1" rx="3"/>';
    s += '<text x="340" y="175" fill="#fde047" font-size="11" text-anchor="middle">' + cfg.shortInput + ': ' + val + ' ' + cfg.inputUnit + '</text>';
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
