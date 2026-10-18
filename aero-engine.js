'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.AeroModels;
const $ = id => document.getElementById(id);
const fmt = (v, n=4) => Math.abs(v) > 0 && (Math.abs(v) < 0.001 || Math.abs(v) >= 1e6) ? v.toExponential(3) : v.toFixed(n);

let rows = [];
let measurement = null;
let busy = false;
let clearPending = false;
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
  message('Adjust ' + cfg.shortInput + ', then execute wind tunnel / aerospace measurement.');
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

if ($('pauseMotion')) $('pauseMotion').hidden = true;

if ($('resetApparatus')) {
  $('resetApparatus').onclick = () => {
    if (busy) return;
    if ($('independent')) $('independent').value = cfg.initial;
    if ($('independentNumber')) $('independentNumber').value = cfg.initial;
    update();
    message('Apparatus telemetry reset. Notebook observations preserved.');
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
    message('Calibrating flow field and logging sensors for ' + cfg.shortInput + ' = ' + p.input + ' ' + cfg.inputUnit + '…');
    await new Promise(resolve => setTimeout(resolve, 200));
    const raw = prediction.raw;
    measurement = model.reading(cfg.slug, p.input, raw);
    busy = false;
    if ($('independent')) $('independent').disabled = false;
    if ($('independentNumber')) $('independentNumber').disabled = false;
    $('measure').disabled = false;
    if ($('recordReading')) $('recordReading').disabled = false;
    if ($('readingValue')) $('readingValue').textContent = raw.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit;
    if ($('liveState')) $('liveState').textContent = 'Steady state reached. Ready to record telemetry.';
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
    message('Observation ' + rows.length + ' logged. Adjust ' + cfg.shortInput + ' for next flight/test point.');
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
        fmt(result.se * cfg.resultScale) + ' ' + cfg.resultUnit + '</p><p>Aerodynamic scaling verified by ordinary least-squares regression.</p>';
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

  let svg = '<rect width="650" height="340" fill="#0b192c"/>';
  for (let i = 0; i <= 5; i++) {
    const gx = left + i * (right - left) / 5;
    const gy = top + i * (bottom - top) / 5;
    svg += '<line x1="' + gx + '" y1="' + top + '" x2="' + gx + '" y2="' + bottom + '" stroke="#1e293b" stroke-width="1" stroke-dasharray="2,3"/>';
    svg += '<line x1="' + left + '" y1="' + gy + '" x2="' + right + '" y2="' + gy + '" stroke="#1e293b" stroke-width="1" stroke-dasharray="2,3"/>';
    const valX = xmin + i * (xmax - xmin) / 5;
    const valY = ymax - i * (ymax - ymin) / 5;
    svg += '<text x="' + gx + '" y="' + (bottom + 18) + '" fill="#7dd3fc" font-size="10" text-anchor="middle">' + fmt(valX, 2) + '</text>';
    svg += '<text x="' + (left - 10) + '" y="' + (gy + 3) + '" fill="#7dd3fc" font-size="10" text-anchor="end">' + fmt(valY, 2) + '</text>';
  }
  svg += '<text x="' + ((left + right) / 2) + '" y="325" fill="#bae6fd" font-size="12" text-anchor="middle">' + cfg.xAxis + '</text>';
  svg += '<text x="18" y="' + ((top + bottom) / 2) + '" fill="#bae6fd" font-size="12" text-anchor="middle" transform="rotate(-90 18 ' + ((top + bottom) / 2) + ')">' + cfg.yAxis + '</text>';

  if (f && rows.length >= 2) {
    const x1 = xmin, x2 = xmax;
    const y1 = f.m * (x1 / cfg.xScale) + f.b;
    const y2 = f.m * (x2 / cfg.xScale) + f.b;
    svg += '<line x1="' + px(x1) + '" y1="' + py(y1 * cfg.yScale) + '" x2="' + px(x2) + '" y2="' + py(y2 * cfg.yScale) + '" stroke="#38bdf8" stroke-width="2.5"/>';
  }

  rows.forEach((r, i) => {
    const cx = px(r.x * cfg.xScale), cy = py(r.y * cfg.yScale);
    svg += '<circle cx="' + cx + '" cy="' + cy + '" r="5.5" fill="#facc15" stroke="#0b192c" stroke-width="1.5"/>';
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
  const svg = $('apparatusDiagram') || $('simCanvas');
  if (!svg) return;
  const p = params();
  const val = p.input;
  const num = cfg.number;
  const mode = currentSimMode;

  let out = '<defs>';
  out += '<pattern id="aeroGrid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M 25 0 L 0 0 0 25" fill="none" stroke="#1e293b" stroke-width="0.8" opacity="0.6"/></pattern>';
  out += '<linearGradient id="flowGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#0284c7" stop-opacity="0.8"/><stop offset="100%" stop-color="#38bdf8" stop-opacity="0.2"/></linearGradient>';
  out += '<linearGradient id="shockGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ef4444" stop-opacity="0.9"/><stop offset="100%" stop-color="#f59e0b" stop-opacity="0.4"/></linearGradient>';
  out += '<linearGradient id="thrustGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#f97316" stop-opacity="0.9"/><stop offset="50%" stop-color="#eab308" stop-opacity="0.7"/><stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/></linearGradient>';
  out += '</defs>';

  out += '<rect width="100%" height="100%" fill="#0b192c"/>';
  out += '<rect width="100%" height="100%" fill="url(#aeroGrid)"/>';

  // Header Telemetry Bar
  out += '<rect x="15" y="12" width="690" height="26" rx="4" fill="#05101e" stroke="#0369a1" stroke-width="1"/>';
  out += '<text x="25" y="29" fill="#38bdf8" font-size="11" font-weight="bold">AEROSPACE TEST CELL TELEMETRY · LAB ' + String(num).padStart(2, '0') + '</text>';
  out += '<text x="450" y="29" fill="#7dd3fc" font-size="10">MODE: ' + mode.toUpperCase() + ' | PARAM: ' + cfg.shortInput + ' = ' + val + ' ' + cfg.inputUnit + '</text>';

  if (num <= 10) {
    // Module 1: Subsonic Aerodynamics & Wind Tunnel Testing
    out += drawSubsonicModule(val, mode, num);
  } else if (num <= 18) {
    // Module 2: Compressible Aerodynamics & High-Speed Gas Dynamics
    out += drawCompressibleModule(val, mode, num);
  } else if (num <= 26) {
    // Module 3: Aircraft Flight Mechanics & Stability
    out += drawFlightMechModule(val, mode, num);
  } else if (num <= 34) {
    // Module 4: Aerospace Propulsion & Rocket Dynamics
    out += drawPropulsionModule(val, mode, num);
  } else {
    // Module 5: Aerospace Structures, Aeroelasticity & Space Flight
    out += drawStructuresSpaceModule(val, mode, num);
  }

  svg.innerHTML = out;
}

function drawSubsonicModule(val, mode, num) {
  let s = '';
  // Tunnel test section walls
  s += '<rect x="40" y="55" width="640" height="210" fill="#061426" stroke="#0284c7" stroke-width="1.5" rx="6"/>';
  s += '<line x1="40" y1="55" x2="680" y2="55" stroke="#38bdf8" stroke-width="3"/>';
  s += '<line x1="40" y1="265" x2="680" y2="265" stroke="#38bdf8" stroke-width="3"/>';

  // Streamlines
  const speedRatio = Math.max(0.2, Math.min(1.5, val / (cfg.max || 50)));
  const offsetAoA = (num === 2 || num === 3 || num === 4) ? (val * 1.5) : 0;
  for (let y = 80; y <= 240; y += 22) {
    const dy = (y > 140 && y < 180) ? -Math.sin((y - 140) / 40 * Math.PI) * (18 + offsetAoA * 0.4) : 0;
    s += '<path d="M 50 ' + y + ' Q 320 ' + (y + dy) + ' 670 ' + y + '" fill="none" stroke="#0284c7" stroke-width="1.2" stroke-dasharray="8,4" opacity="0.65"/>';
  }

  // Model in Test Section
  const cx = 330, cy = 160;
  if (num === 10) {
    // Circular cylinder with vortex shedding
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="26" fill="#1e293b" stroke="#38bdf8" stroke-width="2.5"/>';
    s += '<path d="M 360 145 Q 420 120 480 155 T 580 145 T 670 160" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,3"/>';
    s += '<path d="M 360 175 Q 420 200 480 165 T 580 175 T 670 160" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4,3"/>';
    s += '<text x="' + cx + '" y="' + (cy + 5) + '" fill="#e0f2fe" font-size="10" text-anchor="middle">CYLINDER</text>';
  } else if (num === 5) {
    // Boundary layer flat plate
    s += '<rect x="180" y="195" width="380" height="12" fill="#334155" stroke="#7dd3fc" stroke-width="1.5"/>';
    s += '<path d="M 180 195 Q 360 145 560 125 L 560 195 Z" fill="url(#flowGrad)" stroke="#38bdf8" stroke-width="1.5"/>';
    s += '<text x="370" y="222" fill="#7dd3fc" font-size="11" text-anchor="middle">LAMINAR / TURBULENT BOUNDARY LAYER δ(x)</text>';
  } else {
    // Airfoil profile (NACA)
    s += '<g transform="rotate(' + (-offsetAoA) + ' ' + cx + ' ' + cy + ')">';
    s += '<path d="M 190 ' + cy + ' C 240 ' + (cy - 38) + ', 380 ' + (cy - 28) + ', 470 ' + cy + ' C 380 ' + (cy + 18) + ', 240 ' + (cy + 24) + ', 190 ' + cy + ' Z" fill="#1e293b" stroke="#38bdf8" stroke-width="2.5"/>';
    s += '<circle cx="260" cy="' + cy + '" r="4" fill="#facc15"/>';
    s += '<line x1="260" y1="' + cy + '" x2="260" y2="' + (cy - 48 - offsetAoA * 2) + '" stroke="#22c55e" stroke-width="2.5" marker-end="url(#arrow)"/>';
    s += '<line x1="260" y1="' + cy + '" x2="' + (260 + 35 + offsetAoA) + '" y2="' + cy + '" stroke="#ef4444" stroke-width="2.5"/>';
    s += '<text x="260" y="' + (cy - 54 - offsetAoA * 2) + '" fill="#4ade80" font-size="10" text-anchor="middle" font-weight="bold">LIFT L</text>';
    s += '<text x="' + (305 + offsetAoA) + '" y="' + (cy + 14) + '" fill="#f87171" font-size="10" font-weight="bold">DRAG D</text>';
    s += '</g>';
  }

  // Instrumentation Gauges / Monometers
  s += '<rect x="520" y="70" width="140" height="80" rx="4" fill="#05101e" stroke="#0284c7" stroke-width="1.2"/>';
  s += '<text x="530" y="88" fill="#7dd3fc" font-size="9" font-weight="bold">DYNAMIC PRESSURE q</text>';
  s += '<text x="530" y="112" fill="#38bdf8" font-size="18" font-weight="bold">' + (0.5 * 1.225 * val * val).toFixed(1) + ' Pa</text>';
  s += '<text x="530" y="136" fill="#94a3b8" font-size="9">FLOW SPEED: ' + val.toFixed(1) + ' m/s</text>';
  return s;
}

function drawCompressibleModule(val, mode, num) {
  let s = '';
  // Supersonic wind tunnel / nozzle contour
  s += '<rect x="40" y="55" width="640" height="210" fill="#05101e" stroke="#0369a1" stroke-width="1.5" rx="6"/>';

  // Converging-Diverging Nozzle walls
  s += '<path d="M 60 70 Q 220 70 290 125 Q 360 125 640 80 L 640 60 L 60 60 Z" fill="#1e293b" stroke="#38bdf8" stroke-width="1.8"/>';
  s += '<path d="M 60 250 Q 220 250 290 195 Q 360 195 640 240 L 640 260 L 60 260 Z" fill="#1e293b" stroke="#38bdf8" stroke-width="1.8"/>';

  // Throat marker
  s += '<line x1="290" y1="125" x2="290" y2="195" stroke="#facc15" stroke-dasharray="3,3" stroke-width="1.5"/>';
  s += '<text x="290" y="164" fill="#facc15" font-size="9" text-anchor="middle">THROAT (M = 1.0)</text>';

  // Shock wave discontinuity or Expansion Fan
  const shockX = Math.min(620, Math.max(340, 320 + val * 65));
  if (num === 12) {
    // Normal Shock
    s += '<line x1="' + shockX + '" y1="108" x2="' + shockX + '" y2="212" stroke="#ef4444" stroke-width="4"/>';
    s += '<text x="' + (shockX - 10) + '" y="102" fill="#f87171" font-size="10" text-anchor="end" font-weight="bold">M₁ = ' + val.toFixed(2) + ' (SUPERSONIC)</text>';
    s += '<text x="' + (shockX + 10) + '" y="102" fill="#60a5fa" font-size="10" font-weight="bold">M₂ &lt; 1.0 (SUBSONIC)</text>';
  } else if (num === 13) {
    // Oblique Shock Wedge
    s += '<polygon points="360,160 480,120 480,200" fill="#334155" stroke="#7dd3fc" stroke-width="1.5"/>';
    s += '<line x1="360" y1="160" x2="590" y2="90" stroke="#f59e0b" stroke-width="3"/>';
    s += '<line x1="360" y1="160" x2="590" y2="230" stroke="#f59e0b" stroke-width="3"/>';
    s += '<text x="595" y="88" fill="#fbbf24" font-size="10">OBLIQUE SHOCK WAVE β</text>';
  } else {
    // Expansion waves
    for (let a = -30; a <= 30; a += 15) {
      const rad = a * Math.PI / 180;
      s += '<line x1="320" y1="160" x2="' + (320 + Math.cos(rad) * 260) + '" y2="' + (160 + Math.sin(rad) * 70) + '" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="4,2"/>';
    }
  }

  // Telemetry HUD
  s += '<rect x="80" y="75" width="130" height="50" rx="3" fill="#0b192c" stroke="#0284c7" stroke-width="1"/>';
  s += '<text x="90" y="93" fill="#7dd3fc" font-size="9">STAGNATION P₀</text>';
  s += '<text x="90" y="112" fill="#38bdf8" font-size="14" font-weight="bold">500.0 kPa</text>';
  return s;
}

function drawFlightMechModule(val, mode, num) {
  let s = '';
  // Flight Horizon / Attitude Canvas
  s += '<rect x="40" y="55" width="640" height="210" fill="#041220" stroke="#0369a1" stroke-width="1.5" rx="6"/>';

  // Artificial Horizon Line
  const pitchAngle = (num === 20 || num === 21) ? (val * 0.8) : 4;
  s += '<line x1="60" y1="' + (160 + pitchAngle * 2) + '" x2="660" y2="' + (160 - pitchAngle * 2) + '" stroke="#0284c7" stroke-width="1.5"/>';
  s += '<text x="640" y="152" fill="#7dd3fc" font-size="9" text-anchor="end">HORIZON REF</text>';

  // Aircraft Silhouette
  const cx = 350, cy = 160;
  s += '<g transform="rotate(' + (-pitchAngle) + ' ' + cx + ' ' + cy + ')">';
  // Fuselage
  s += '<ellipse cx="' + cx + '" cy="' + cy + '" rx="110" ry="16" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>';
  // Wing
  s += '<polygon points="' + (cx - 20) + ',' + (cy - 8) + ' ' + (cx + 10) + ',' + (cy - 55) + ' ' + (cx + 35) + ',' + (cy - 55) + ' ' + (cx + 25) + ',' + (cy - 8) + '" fill="#0284c7" stroke="#7dd3fc" stroke-width="1.2"/>';
  s += '<polygon points="' + (cx - 20) + ',' + (cy + 8) + ' ' + (cx + 10) + ',' + (cy + 55) + ' ' + (cx + 35) + ',' + (cy + 55) + ' ' + (cx + 25) + ',' + (cy + 8) + '" fill="#0284c7" stroke="#7dd3fc" stroke-width="1.2"/>';
  // Tail / Elevator
  s += '<polygon points="' + (cx - 95) + ',' + (cy - 4) + ' ' + (cx - 80) + ',' + (cy - 34) + ' ' + (cx - 65) + ',' + (cy - 34) + ' ' + (cx - 75) + ',' + (cy - 4) + '" fill="#0369a1" stroke="#38bdf8" stroke-width="1.2"/>';
  // Neutral Point vs CG
  s += '<circle cx="' + (cx - 5) + '" cy="' + cy + '" r="5" fill="#facc15"/>';
  s += '<text x="' + (cx - 5) + '" y="' + (cy - 10) + '" fill="#facc15" font-size="8" text-anchor="middle">CG</text>';
  s += '<circle cx="' + (cx + 15) + '" cy="' + cy + '" r="4" fill="#ef4444"/>';
  s += '<text x="' + (cx + 15) + '" y="' + (cy - 10) + '" fill="#f87171" font-size="8" text-anchor="middle">NP</text>';
  s += '</g>';

  // Stability / Phugoid Wave Overlay (if dynamic mode)
  if (num === 25 || num === 26) {
    let wave = 'M 80 230';
    for (let x = 80; x <= 620; x += 15) {
      const damp = Math.exp(-(x - 80) / 300);
      const yw = 230 - Math.sin((x - 80) / (val * 4)) * 30 * damp;
      wave += ' L ' + x + ' ' + yw;
    }
    s += '<path d="' + wave + '" fill="none" stroke="#f59e0b" stroke-width="2"/>';
    s += '<text x="85" y="215" fill="#fbbf24" font-size="9">EIGENMODE TRAJECTORY (PHUGOID / SHORT PERIOD)</text>';
  }

  // Airspeed Indicator Gauge
  s += '<rect x="60" y="70" width="130" height="60" rx="4" fill="#05101e" stroke="#0369a1" stroke-width="1.2"/>';
  s += '<text x="70" y="88" fill="#7dd3fc" font-size="9" font-weight="bold">INDICATED AIRSPEED</text>';
  s += '<text x="70" y="112" fill="#38bdf8" font-size="16" font-weight="bold">' + (val * 3.6).toFixed(1) + ' km/h</text>';
  return s;
}

function drawPropulsionModule(val, mode, num) {
  let s = '';
  // Engine test bench structure
  s += '<rect x="40" y="55" width="640" height="210" fill="#061220" stroke="#0369a1" stroke-width="1.5" rx="6"/>';

  if (num === 27) {
    // Propeller Blade Element Disk
    s += '<rect x="290" y="85" width="25" height="150" rx="3" fill="#334155" stroke="#7dd3fc" stroke-width="1.5"/>';
    s += '<ellipse cx="302" cy="160" rx="14" ry="75" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="5,3"/>';
    s += '<polygon points="315,160 520,110 520,210" fill="url(#flowGrad)" opacity="0.6"/>';
    s += '<text x="302" y="75" fill="#38bdf8" font-size="11" text-anchor="middle">PROPELLER SLIPSTREAM (J = ' + val.toFixed(2) + ')</text>';
  } else if (num >= 32) {
    // Rocket Chamber & Expansion Nozzle
    s += '<rect x="120" y="115" width="160" height="90" rx="5" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>';
    s += '<text x="200" y="165" fill="#facc15" font-size="11" text-anchor="middle" font-weight="bold">COMBUSTION CHAMBER</text>';
    s += '<path d="M 280 135 L 320 150 L 440 105 L 440 215 L 320 170 L 280 185 Z" fill="#334155" stroke="#38bdf8" stroke-width="2"/>';
    // Exhaust Plume
    s += '<polygon points="440,110 650,75 670,160 650,245 440,210" fill="url(#thrustGrad)"/>';
    s += '<text x="540" y="164" fill="#ffffff" font-size="12" text-anchor="middle" font-weight="bold">SUPERSONIC PLUME</text>';
  } else {
    // Gas Turbine Engine Spool
    s += '<path d="M 120 110 L 220 125 L 340 125 L 420 100 L 480 100 L 480 220 L 420 220 L 340 195 L 220 195 L 120 210 Z" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>';
    s += '<line x1="160" y1="116" x2="160" y2="204" stroke="#7dd3fc" stroke-width="3"/>';
    s += '<line x1="260" y1="125" x2="260" y2="195" stroke="#facc15" stroke-width="4"/>';
    s += '<line x1="390" y1="110" x2="390" y2="210" stroke="#f87171" stroke-width="3"/>';
    s += '<text x="160" y="98" fill="#7dd3fc" font-size="9" text-anchor="middle">FAN / COMP</text>';
    s += '<text x="260" y="98" fill="#facc15" font-size="9" text-anchor="middle">BURNER</text>';
    s += '<text x="390" y="98" fill="#f87171" font-size="9" text-anchor="middle">TURBINE</text>';
  }

  // Test Stand Load Cell Readout
  s += '<rect x="520" y="68" width="140" height="60" rx="3" fill="#05101e" stroke="#0284c7" stroke-width="1"/>';
  s += '<text x="530" y="85" fill="#7dd3fc" font-size="9">LOAD CELL THRUST</text>';
  s += '<text x="530" y="108" fill="#38bdf8" font-size="16" font-weight="bold">' + (val * 12.5).toFixed(1) + ' kN</text>';
  return s;
}

function drawStructuresSpaceModule(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="55" width="640" height="210" fill="#030b17" stroke="#0369a1" stroke-width="1.5" rx="6"/>';

  if (num >= 41) {
    // Spaceflight Keplerian / Hohmann Orbit
    s += '<circle cx="340" cy="160" r="28" fill="#0284c7" stroke="#38bdf8" stroke-width="2"/>';
    s += '<text x="340" y="164" fill="#ffffff" font-size="9" text-anchor="middle" font-weight="bold">EARTH</text>';
    // Orbit 1 & 2
    s += '<ellipse cx="340" cy="160" rx="90" ry="70" fill="none" stroke="#22c55e" stroke-width="1.5" stroke-dasharray="4,3"/>';
    s += '<ellipse cx="340" cy="160" rx="220" ry="85" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="6,4"/>';
    // Hohmann transfer ellipse
    s += '<path d="M 250 160 A 155 80 0 0 1 560 160" fill="none" stroke="#f59e0b" stroke-width="2"/>';
    s += '<circle cx="250" cy="160" r="5" fill="#facc15"/>';
    s += '<text x="250" y="180" fill="#facc15" font-size="9" text-anchor="middle">Δv₁</text>';
    s += '<circle cx="560" cy="160" r="5" fill="#facc15"/>';
    s += '<text x="560" y="180" fill="#facc15" font-size="9" text-anchor="middle">Δv₂</text>';
    s += '<text x="405" y="75" fill="#fbbf24" font-size="10" text-anchor="middle">HOHMANN TRANSFER TRAJECTORY</text>';
  } else {
    // Aircraft Wing Spar / Box Section / Flutter Rig
    s += '<rect x="220" y="95" width="280" height="130" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>';
    s += '<line x1="220" y1="135" x2="500" y2="135" stroke="#0284c7" stroke-width="1.5"/>';
    s += '<line x1="360" y1="95" x2="360" y2="225" stroke="#0284c7" stroke-width="1.5"/>';
    // Shear Center marker
    const scX = 190, scY = 160;
    s += '<circle cx="' + scX + '" cy="' + scY + '" r="6" fill="#ef4444"/>';
    s += '<text x="' + scX + '" y="' + (scY - 10) + '" fill="#f87171" font-size="9" text-anchor="middle">SHEAR CENTER</text>';
    s += '<line x1="' + scX + '" y1="' + scY + '" x2="220" y2="160" stroke="#f87171" stroke-width="1.5" stroke-dasharray="3,2"/>';
    s += '<text x="360" y="170" fill="#e0f2fe" font-size="11" text-anchor="middle">THIN-WALLED BOX CELL</text>';
    s += '<text x="360" y="245" fill="#7dd3fc" font-size="10" text-anchor="middle">TEST LOAD: P = ' + val.toFixed(1) + ' ' + cfg.inputUnit + '</text>';
  }
  return s;
}

// Download CSV
if ($('downloadReadings')) {
  $('downloadReadings').onclick = () => {
    if (!rows.length) return;
    const header = ['Trial', cfg.shortInput, cfg.rawLabel, cfg.xAxis, cfg.yAxis].join(',');
    const content = rows.map((r, i) => [(i + 1), r.input, r.raw, r.x * cfg.xScale, r.y * cfg.yScale].join(',')).join('\n');
    const blob = new Blob([header + '\n' + content], { type: 'text/csv' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = cfg.slug + '-observations.csv';
    a.click();
  };
}

// Clear Notebook
if ($('clearReadings')) {
  $('clearReadings').onclick = () => {
    if (!rows.length) return;
    if (clearPending) {
      rows = [];
      clearPending = false;
      $('clearReadings').textContent = 'Clear notebook';
      persist();
      message('Notebook cleared.');
      return;
    }
    clearPending = true;
    $('clearReadings').textContent = 'Confirm clear?';
    message('Click Confirm clear to reset observation notebook.');
    setTimeout(() => {
      clearPending = false;
      if ($('clearReadings')) $('clearReadings').textContent = 'Clear notebook';
    }, 3000);
  };
}

// Check Student Estimate
if ($('checkEstimate')) {
  $('checkEstimate').onclick = () => {
    const f = model.fit(rows);
    const answer = +$('studentEstimate').value;
    if (!f) {
      if ($('estimateFeedback')) $('estimateFeedback').textContent = 'Record at least three distinct observations first.';
      return;
    }
    if (!$('studentEstimate').value || !Number.isFinite(answer) || answer <= 0) {
      if ($('estimateFeedback')) $('estimateFeedback').textContent = 'Enter a valid positive number.';
      return;
    }
    const expected = model.estimate(cfg.slug, f).value * cfg.resultScale;
    const err = Math.abs(answer - expected) / Math.abs(expected);
    if ($('estimateFeedback')) {
      $('estimateFeedback').textContent = err < 0.03
        ? 'Your estimate agrees with the theoretical aerodynamic model within 3%! Measurement confirmed.'
        : 'Recheck your calculation. The ordinary least-squares regression yields ' + fmt(expected, cfg.resultDecimals) + ' ' + cfg.resultUnit + '.';
    }
  };
}

// Quiz Handlers
document.querySelectorAll('[data-quiz]').forEach(b => {
  b.onclick = () => {
    const q = cfg.quiz[+b.dataset.quiz];
    const j = +b.dataset.choice;
    document.querySelectorAll('[data-quiz="' + b.dataset.quiz + '"]').forEach(x => x.classList.remove('correct', 'wrong'));
    b.classList.add(j === q.correct ? 'correct' : 'wrong');
    const fb = $('quizFeedback' + b.dataset.quiz);
    if (fb) {
      fb.textContent = (j === q.correct ? 'Correct! ' : 'Incorrect. ') + q.explanation;
    }
  };
});

// Initial Setup
update();
renderResults();
window.addEventListener('resize', () => draw());
