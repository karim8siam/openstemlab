'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.AgriModels;
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
  message('Adjust ' + cfg.shortInput + ', then execute agricultural trial.');
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
    message('Apparatus settings reset. Notebook observations preserved.');
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
    message('Acquiring agricultural telemetry for ' + cfg.shortInput + ' = ' + p.input + ' ' + cfg.inputUnit + '…');
    await new Promise(resolve => setTimeout(resolve, 200));
    const raw = prediction.raw;
    measurement = model.reading(cfg.slug, p.input, raw);
    busy = false;
    if ($('independent')) $('independent').disabled = false;
    if ($('independentNumber')) $('independentNumber').disabled = false;
    $('measure').disabled = false;
    if ($('recordReading')) $('recordReading').disabled = false;
    if ($('readingValue')) $('readingValue').textContent = raw.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit;
    if ($('liveState')) $('liveState').textContent = 'Field equilibrium reached. Ready to record observation.';
    message(cfg.shortInput + ' = ' + p.input + ' logged: ' + cfg.rawLabel + ' = ' + raw + ' ' + cfg.rawUnit + '. Click Record observation.');
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
    saveNotebook();
    renderNotebook();
    message('Observation #' + rows.length + ' recorded in notebook.');
    draw();
  };
}

function saveNotebook() {
  try {
    localStorage.setItem('openstemlab-' + cfg.slug + '-v1', JSON.stringify(rows));
  } catch (e) {}
}

if ($('clearReadings')) {
  $('clearReadings').onclick = () => {
    if (rows.length === 0) return;
    if (!clearPending) {
      clearPending = true;
      $('clearReadings').textContent = 'Confirm clear?';
      message('Click again to erase all ' + rows.length + ' observations.');
      setTimeout(() => {
        if (clearPending) {
          clearPending = false;
          $('clearReadings').textContent = 'Clear notebook';
        }
      }, 3000);
      return;
    }
    clearPending = false;
    $('clearReadings').textContent = 'Clear notebook';
    rows = [];
    saveNotebook();
    renderNotebook();
    message('Notebook cleared.');
    draw();
  };
}

if ($('downloadReadings')) {
  $('downloadReadings').onclick = () => {
    if (rows.length === 0) return;
    let csv = cfg.shortInput.replace(/\s+/g, '_') + ',' + cfg.rawLabel.replace(/\s+/g, '_') + ',x_coord,y_coord\n';
    rows.forEach(r => {
      csv += r.input + ',' + r.raw + ',' + r.x.toFixed(4) + ',' + r.y.toFixed(4) + '\n';
    });
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = cfg.slug + '-readings.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };
}

function renderNotebook() {
  const count = $('notebookCount');
  if (count) count.textContent = rows.length;
  const tbody = $('readingRows');
  const empty = $('emptyReadings');
  const dl = $('downloadReadings');
  const clr = $('clearReadings');
  if (dl) dl.disabled = rows.length === 0;
  if (clr) clr.disabled = rows.length === 0;

  if (tbody) {
    tbody.innerHTML = '';
    rows.forEach((r, idx) => {
      const tr = document.createElement('tr');
      tr.innerHTML = '<td>' + (idx + 1) + '</td><td>' + r.input + '</td><td>' + r.raw + '</td><td>' + r.x.toFixed(4) + '</td><td>' + r.y.toFixed(4) + '</td><td><button class="remove-reading" data-index="' + idx + '" title="Remove observation" style="background:none;border:none;cursor:pointer;color:#94a3b8">×</button></td>';
      tbody.appendChild(tr);
    });
    tbody.querySelectorAll('.remove-reading').forEach(btn => {
      btn.onclick = e => {
        const i = +e.target.dataset.index;
        rows.splice(i, 1);
        saveNotebook();
        renderNotebook();
        draw();
      };
    });
  }
  if (empty) empty.hidden = rows.length > 0;
  drawFitAndPlot();
}

function drawFitAndPlot() {
  const sumEl = $('fitSummary');
  const plot = $('labPlot');
  if (!plot) return;

  if (rows.length < 3) {
    if (sumEl) sumEl.innerHTML = '<p class="fit-waiting">Record at least 3 observations to compute agricultural regression fit.</p>';
    plot.innerHTML = '<text x="325" y="170" text-anchor="middle" fill="#64748b" font-size="13">Take 3 or more observations to view linear fit and telemetry scatter</text>';
    return;
  }

  const f = model.fit(rows);
  if (!f) return;

  if (sumEl) {
    sumEl.innerHTML = '<div class="fit-values">' +
      '<div><small>GRADIENT (m)</small><strong>' + fmt(f.m, 6) + '</strong></div>' +
      '<div><small>INTERCEPT (b)</small><strong>' + fmt(f.b, 6) + '</strong></div>' +
      '<div><small>COEFF OF DET (R²)</small><strong>' + f.r2.toFixed(6) + '</strong></div>' +
      '<div><small>STANDARD ERROR (s_e)</small><strong>' + fmt(f.se, 6) + '</strong></div>' +
      '</div>';
  }

  // Draw plot SVG
  const pad = { left: 65, right: 25, top: 25, bottom: 45 };
  const w = 650, h = 340;
  const pw = w - pad.left - pad.right;
  const ph = h - pad.top - pad.bottom;

  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  rows.forEach(r => {
    if (r.x < minX) minX = r.x;
    if (r.x > maxX) maxX = r.x;
    if (r.y < minY) minY = r.y;
    if (r.y > maxY) maxY = r.y;
  });
  if (minX === maxX) { minX -= 1; maxX += 1; }
  if (minY === maxY) { minY -= 1; maxY += 1; }
  const spanX = maxX - minX;
  const spanY = maxY - minY;
  minX -= spanX * 0.08; maxX += spanX * 0.08;
  minY -= spanY * 0.08; maxY += spanY * 0.08;

  const tx = x => pad.left + (x - minX) / (maxX - minX) * pw;
  const ty = y => pad.top + ph - (y - minY) / (maxY - minY) * ph;

  let svg = '<rect width="' + w + '" height="' + h + '" fill="#05140b" rx="6"/>';
  // Grid lines
  for (let i = 0; i <= 4; i++) {
    const gy = minY + i * (maxY - minY) / 4;
    const py = ty(gy);
    svg += '<line x1="' + pad.left + '" y1="' + py + '" x2="' + (w - pad.right) + '" y2="' + py + '" stroke="#14532d" stroke-dasharray="2,2"/>';
    svg += '<text x="' + (pad.left - 8) + '" y="' + (py + 4) + '" text-anchor="end" fill="#86efac" font-size="10">' + gy.toFixed(2) + '</text>';
    const gx = minX + i * (maxX - minX) / 4;
    const px = tx(gx);
    svg += '<line x1="' + px + '" y1="' + pad.top + '" x2="' + px + '" y2="' + (h - pad.bottom) + '" stroke="#14532d" stroke-dasharray="2,2"/>';
    svg += '<text x="' + px + '" y="' + (h - pad.bottom + 16) + '" text-anchor="middle" fill="#86efac" font-size="10">' + gx.toFixed(2) + '</text>';
  }

  // Axes
  svg += '<line x1="' + pad.left + '" y1="' + pad.top + '" x2="' + pad.left + '" y2="' + (h - pad.bottom) + '" stroke="#16a34a" stroke-width="1.5"/>';
  svg += '<line x1="' + pad.left + '" y1="' + (h - pad.bottom) + '" x2="' + (w - pad.right) + '" y2="' + (h - pad.bottom) + '" stroke="#16a34a" stroke-width="1.5"/>';
  svg += '<text x="' + (w / 2) + '" y="' + (h - 10) + '" text-anchor="middle" fill="#bbf7d0" font-size="11">' + cfg.xAxis + '</text>';
  svg += '<text transform="translate(18 ' + (h / 2) + ') rotate(-90)" text-anchor="middle" fill="#bbf7d0" font-size="11">' + cfg.yAxis + '</text>';

  // Regression line
  const x1 = minX, y1 = f.m * x1 + f.b;
  const x2 = maxX, y2 = f.m * x2 + f.b;
  svg += '<line x1="' + tx(x1) + '" y1="' + ty(y1) + '" x2="' + tx(x2) + '" y2="' + ty(y2) + '" stroke="#4ade80" stroke-width="2.5"/>';

  // Data points
  rows.forEach(r => {
    svg += '<circle cx="' + tx(r.x) + '" cy="' + ty(r.y) + '" r="5" fill="#facc15" stroke="#052e16" stroke-width="1.5"/>';
  });

  plot.innerHTML = svg;
}

if ($('checkEstimate')) {
  $('checkEstimate').onclick = () => {
    const input = $('studentEstimate');
    const fb = $('estimateFeedback');
    if (!input || !fb) return;
    const est = +input.value;
    if (!Number.isFinite(est) || est <= 0) {
      fb.textContent = 'Please enter a valid positive numerical estimate.';
      fb.className = 'error';
      return;
    }
    const ref = cfg.refValue * cfg.resultScale;
    const diff = Math.abs(est - ref) / ref * 100;
    if (diff < 1.0) {
      fb.textContent = 'Excellent! Your calculation (' + est + ') matches theoretical reference ' + ref.toFixed(cfg.resultDecimals) + ' ' + cfg.resultUnit + ' within ' + diff.toFixed(2) + '%.';
      fb.className = 'success';
    } else if (diff < 5.0) {
      fb.textContent = 'Close! Your value differs by ' + diff.toFixed(2) + '% from reference ' + ref.toFixed(cfg.resultDecimals) + ' ' + cfg.resultUnit + '.';
      fb.className = 'info';
    } else {
      fb.textContent = 'Discrepancy is ' + diff.toFixed(1) + '%. Check your gradient conversion formula: ' + cfg.fitEquation;
      fb.className = 'error';
    }
  };
}

// Mode Switchers
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

// Quiz Evaluation
document.querySelectorAll('.quiz-option').forEach(opt => {
  opt.onclick = () => {
    const qIdx = +opt.dataset.quiz;
    const cIdx = +opt.dataset.choice;
    const qData = cfg.quiz[qIdx];
    const fb = $('quizFeedback' + qIdx);
    const parent = opt.parentElement;
    parent.querySelectorAll('.quiz-option').forEach(b => b.classList.remove('correct', 'incorrect'));
    if (cIdx === qData.correct) {
      opt.classList.add('correct');
      if (fb) {
        fb.textContent = 'Correct! ' + qData.explanation;
        fb.className = 'quiz-feedback success';
      }
    } else {
      opt.classList.add('incorrect');
      if (fb) {
        fb.textContent = 'Incorrect. ' + qData.explanation;
        fb.className = 'quiz-feedback error';
      }
    }
  };
});

// Primary SVG Diagram Drawing
function draw() {
  const svg = $('apparatusDiagram');
  if (!svg) return;
  const num = cfg.number;
  const p = params();
  const val = p.input;
  const mode = currentSimMode;

  let out = '<defs>' +
    '<linearGradient id="soilGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#3f2e18"/><stop offset="100%" stop-color="#1e1408"/></linearGradient>' +
    '<linearGradient id="cropGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#4ade80"/><stop offset="100%" stop-color="#15803d"/></linearGradient>' +
    '<linearGradient id="steelGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#475569"/><stop offset="50%" stop-color="#94a3b8"/><stop offset="100%" stop-color="#334155"/></linearGradient>' +
    '<linearGradient id="waterGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8"/><stop offset="100%" stop-color="#0284c7" stop-opacity="0.9"/></linearGradient>' +
    '<marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#86efac"/></marker>' +
    '</defs>';

  // Top header status bar
  out += '<rect x="15" y="10" width="690" height="26" rx="4" fill="#052010" stroke="#166534" stroke-width="1"/>';
  out += '<text x="25" y="27" fill="#86efac" font-size="11" font-weight="bold">AGRICULTURAL ENGINEERING TELEMETRY · LAB ' + String(num).padStart(2, '0') + '</text>';
  out += '<text x="450" y="27" fill="#bbf7d0" font-size="10">VIEW: ' + mode.toUpperCase() + ' | PARAM: ' + cfg.shortInput + ' = ' + val + ' ' + cfg.inputUnit + '</text>';

  if (num <= 10) {
    out += drawFarmMachineryModule(val, mode, num);
  } else if (num <= 19) {
    out += drawSoilWaterModule(val, mode, num);
  } else if (num <= 28) {
    out += drawPostHarvestModule(val, mode, num);
  } else if (num <= 35) {
    out += drawStructuresModule(val, mode, num);
  } else {
    out += drawPrecisionEnergyModule(val, mode, num);
  }

  svg.innerHTML = out;
}

function drawFarmMachineryModule(val, mode, num) {
  let s = '';
  // Field ground & furrow
  s += '<rect x="40" y="55" width="640" height="210" fill="#071d10" stroke="#15803d" stroke-width="1.5" rx="6"/>';
  s += '<rect x="40" y="185" width="640" height="80" fill="url(#soilGrad)"/>';
  s += '<line x1="40" y1="185" x2="680" y2="185" stroke="#86efac" stroke-width="2"/>';

  if (num === 1) {
    // Tractor wheel slip & drawbar pull
    const slipOffset = (val - 0.05) * 80;
    s += '<circle cx="240" cy="175" r="45" fill="#1e293b" stroke="#facc15" stroke-width="5"/>';
    s += '<circle cx="240" cy="175" r="25" fill="#0f172a" stroke="#94a3b8" stroke-width="2"/>';
    // Front wheel
    s += '<circle cx="380" cy="195" r="25" fill="#1e293b" stroke="#94a3b8" stroke-width="3"/>';
    // Chassis body
    s += '<polygon points="220,165 390,185 370,140 290,140 280,110 220,110" fill="#15803d" stroke="#86efac" stroke-width="2"/>';
    s += '<rect x="230" y="115" width="45" height="30" rx="3" fill="#38bdf8" opacity="0.6"/>';
    // Drawbar hitch
    s += '<line x1="220" y1="180" x2="130" y2="180" stroke="#facc15" stroke-width="4"/>';
    s += '<rect x="70" y="160" width="60" height="40" fill="#334155" stroke="#facc15" stroke-width="2" rx="4"/>';
    s += '<text x="100" y="185" fill="#facc15" font-size="9" text-anchor="middle">DYNAMO CAR</text>';
    s += '<line x1="210" y1="160" x2="140" y2="160" stroke="#ef4444" stroke-width="3" marker-end="url(#arrow)"/>';
    s += '<text x="175" y="152" fill="#f87171" font-size="10" text-anchor="middle" font-weight="bold">PULL P = ' + (val * 35.0 * 2.4 + 2.8).toFixed(1) + ' kN</text>';
  } else if (num === 2 || num === 3) {
    // Moldboard or Disc Plow
    s += '<polygon points="180,140 320,140 300,160 160,160" fill="url(#steelGrad)" stroke="#cbd5e1" stroke-width="1.5"/>';
    // Plow bottoms
    for (let i = 0; i < 3; i++) {
      const bx = 200 + i * 45;
      s += '<path d="M ' + bx + ' 160 Q ' + (bx + 20) + ' 195 ' + (bx + 35) + ' 210 Q ' + (bx + 15) + ' 215 ' + (bx - 5) + ' 190 Z" fill="#94a3b8" stroke="#facc15" stroke-width="2"/>';
      s += '<line x1="' + (bx + 35) + '" y1="210" x2="' + (bx + 15) + '" y2="210" stroke="#f87171" stroke-width="2.5"/>';
    }
    s += '<text x="270" y="240" fill="#facc15" font-size="11" text-anchor="middle">SOIL FURROW SLICE INVERSION</text>';
  } else if (num === 7) {
    // Hydraulic spray nozzle
    s += '<rect x="330" y="70" width="60" height="25" fill="url(#steelGrad)" stroke="#94a3b8" rx="3"/>';
    s += '<polygon points="350,95 370,95 365,115 355,115" fill="#facc15"/>';
    // Spray fan
    s += '<path d="M 360 115 L 260 215 L 460 215 Z" fill="url(#waterGrad)" stroke="#38bdf8" stroke-dasharray="4,2"/>';
    s += '<line x1="260" y1="215" x2="460" y2="215" stroke="#38bdf8" stroke-width="2"/>';
    s += '<text x="360" y="235" fill="#7dd3fc" font-size="11" text-anchor="middle">SPRAY DROPLET SWATH PATTERN</text>';
  } else {
    // General farm implement mechanism
    s += '<rect x="180" y="100" width="360" height="85" rx="6" fill="#1e293b" stroke="#16a34a" stroke-width="2"/>';
    s += '<circle cx="260" cy="142" r="28" fill="#0f172a" stroke="#facc15" stroke-width="2.5"/>';
    s += '<circle cx="460" cy="142" r="28" fill="#0f172a" stroke="#86efac" stroke-width="2.5"/>';
    s += '<line x1="260" y1="142" x2="460" y2="142" stroke="#94a3b8" stroke-dasharray="6,3" stroke-width="2"/>';
    s += '<text x="360" y="147" fill="#bbf7d0" font-size="12" text-anchor="middle">POWER TRAIN &amp; METERING SHAFT</text>';
  }

  // Instrument Display Box
  s += '<rect x="520" y="70" width="140" height="75" rx="4" fill="#051a0d" stroke="#166534" stroke-width="1.2"/>';
  s += '<text x="530" y="88" fill="#86efac" font-size="9" font-weight="bold">' + cfg.rawLabel.toUpperCase() + '</text>';
  s += '<text x="530" y="112" fill="#4ade80" font-size="17" font-weight="bold">' + (measurement ? measurement.raw.toFixed(cfg.rawDecimals) : '—') + ' ' + cfg.rawUnit + '</text>';
  s += '<text x="530" y="134" fill="#a7f3d0" font-size="9">' + cfg.shortInput + ': ' + val + ' ' + cfg.inputUnit + '</text>';
  return s;
}

function drawSoilWaterModule(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="55" width="640" height="210" fill="#041810" stroke="#0284c7" stroke-width="1.5" rx="6"/>';

  if (num === 11) {
    // Double-ring infiltrometer
    s += '<rect x="40" y="170" width="640" height="95" fill="url(#soilGrad)"/>';
    // Outer and inner rings
    s += '<rect x="250" y="125" width="220" height="75" fill="none" stroke="#94a3b8" stroke-width="4"/>';
    s += '<rect x="300" y="125" width="120" height="75" fill="none" stroke="#facc15" stroke-width="4"/>';
    // Water level
    const waterDepth = Math.max(15, 60 - val * 0.35);
    s += '<rect x="302" y="' + (127 + 65 - waterDepth) + '" width="116" height="' + waterDepth + '" fill="url(#waterGrad)"/>';
    s += '<line x1="360" y1="120" x2="360" y2="190" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="2,2"/>';
    s += '<text x="360" y="110" fill="#facc15" font-size="10" text-anchor="middle">HOOK GAUGE WATER LEVEL</text>';
  } else if (num === 14 || num === 15) {
    // Flume or Weir open channel
    s += '<path d="M 120 180 L 280 180 L 340 210 L 460 210 L 520 180 L 600 180" fill="none" stroke="#94a3b8" stroke-width="3"/>';
    s += '<path d="M 120 170 Q 300 170 340 190 Q 420 195 600 175" fill="none" stroke="#38bdf8" stroke-width="4"/>';
    s += '<text x="360" y="150" fill="#7dd3fc" font-size="11" text-anchor="middle">FREE CRITICAL CHANNEL DISCHARGE</text>';
  } else {
    // Irrigation permeameter / sprinkler system
    s += '<rect x="220" y="85" width="280" height="135" rx="6" fill="#0f172a" stroke="#0284c7" stroke-width="2"/>';
    s += '<circle cx="360" cy="150" r="42" fill="#1e293b" stroke="#38bdf8" stroke-width="3"/>';
    s += '<path d="M 360 115 L 360 185 M 325 150 L 395 150" stroke="#facc15" stroke-width="2"/>';
    s += '<text x="360" y="155" fill="#38bdf8" font-size="11" text-anchor="middle">HYDRAULIC FLOW CELL</text>';
  }

  // Instrument Display Box
  s += '<rect x="520" y="70" width="140" height="75" rx="4" fill="#031f13" stroke="#0284c7" stroke-width="1.2"/>';
  s += '<text x="530" y="88" fill="#7dd3fc" font-size="9" font-weight="bold">' + cfg.rawLabel.toUpperCase() + '</text>';
  s += '<text x="530" y="112" fill="#38bdf8" font-size="17" font-weight="bold">' + (measurement ? measurement.raw.toFixed(cfg.rawDecimals) : '—') + ' ' + cfg.rawUnit + '</text>';
  s += '<text x="530" y="134" fill="#bae6fd" font-size="9">' + cfg.shortInput + ': ' + val + ' ' + cfg.inputUnit + '</text>';
  return s;
}

function drawPostHarvestModule(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="55" width="640" height="210" fill="#121808" stroke="#ca8a04" stroke-width="1.5" rx="6"/>';

  // Drying chamber / silo / mill housing
  s += '<rect x="180" y="80" width="360" height="150" rx="8" fill="#1e293b" stroke="#facc15" stroke-width="2"/>';
  s += '<line x1="180" y1="165" x2="540" y2="165" stroke="#ca8a04" stroke-dasharray="4,3" stroke-width="1.5"/>';

  // Grain bed
  for (let gx = 200; gx <= 520; gx += 16) {
    s += '<ellipse cx="' + gx + '" cy="155" rx="5" ry="3" fill="#eab308"/>';
    s += '<ellipse cx="' + (gx + 6) + '" cy="148" rx="5" ry="3" fill="#fde047"/>';
  }
  // Airflow arrows
  for (let ax = 220; ax <= 500; ax += 50) {
    s += '<line x1="' + ax + '" y1="205" x2="' + ax + '" y2="175" stroke="#f97316" stroke-width="2" marker-end="url(#arrow)"/>';
  }
  s += '<text x="360" y="222" fill="#fdba74" font-size="10" text-anchor="middle">CONDITIONED HEATED AIRFLOW</text>';
  s += '<text x="360" y="115" fill="#fef08a" font-size="12" text-anchor="middle" font-weight="bold">POST-HARVEST PROCESSING UNIT</text>';

  // Telemetry Box
  s += '<rect x="520" y="70" width="140" height="75" rx="4" fill="#201a05" stroke="#ca8a04" stroke-width="1.2"/>';
  s += '<text x="530" y="88" fill="#fde047" font-size="9" font-weight="bold">' + cfg.rawLabel.toUpperCase() + '</text>';
  s += '<text x="530" y="112" fill="#facc15" font-size="17" font-weight="bold">' + (measurement ? measurement.raw.toFixed(cfg.rawDecimals) : '—') + ' ' + cfg.rawUnit + '</text>';
  s += '<text x="530" y="134" fill="#fef08a" font-size="9">' + cfg.shortInput + ': ' + val + ' ' + cfg.inputUnit + '</text>';
  return s;
}

function drawStructuresModule(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="55" width="640" height="210" fill="#081816" stroke="#0d9488" stroke-width="1.5" rx="6"/>';

  if (num === 29) {
    // Janssen deep-bin storage silo
    s += '<rect x="290" y="70" width="140" height="175" fill="#1e293b" stroke="#cbd5e1" stroke-width="2"/>';
    const grainH = Math.min(150, val * 24);
    s += '<rect x="292" y="' + (243 - grainH) + '" width="136" height="' + grainH + '" fill="#ca8a04" opacity="0.85"/>';
    s += '<text x="360" y="' + (240 - grainH / 2) + '" fill="#fef08a" font-size="10" text-anchor="middle">GRAIN DEPTH z = ' + val.toFixed(1) + ' m</text>';
  } else if (num === 30) {
    // Greenhouse enclosure
    s += '<polygon points="200,180 200,140 360,95 520,140 520,180" fill="#0f766e" opacity="0.4" stroke="#2dd4bf" stroke-width="2"/>';
    s += '<rect x="200" y="180" width="320" height="40" fill="#134e4a" stroke="#2dd4bf" stroke-width="2"/>';
    s += '<text x="360" y="150" fill="#99f6e4" font-size="11" text-anchor="middle">DOUBLE-POLY GREENHOUSE BAY</text>';
  } else if (num === 34) {
    // Timber roof truss Fink 'W'
    s += '<polygon points="180,210 360,110 540,210" fill="none" stroke="#f59e0b" stroke-width="3"/>';
    s += '<line x1="180" y1="210" x2="540" y2="210" stroke="#f59e0b" stroke-width="3"/>';
    // Internal W web members
    s += '<line x1="360" y1="110" x2="270" y2="210" stroke="#f59e0b" stroke-width="2"/>';
    s += '<line x1="360" y1="110" x2="450" y2="210" stroke="#f59e0b" stroke-width="2"/>';
    s += '<line x1="270" y1="160" x2="270" y2="210" stroke="#f59e0b" stroke-width="2"/>';
    s += '<line x1="450" y1="160" x2="450" y2="210" stroke="#f59e0b" stroke-width="2"/>';
    // Load arrow
    s += '<line x1="360" y1="75" x2="360" y2="105" stroke="#ef4444" stroke-width="3" marker-end="url(#arrow)"/>';
    s += '<text x="360" y="70" fill="#f87171" font-size="10" text-anchor="middle">LOAD W = ' + val + ' kN</text>';
  } else {
    // Anaerobic digester / livestock chamber
    s += '<rect x="250" y="85" width="220" height="145" rx="10" fill="#1e293b" stroke="#14b8a6" stroke-width="2.5"/>';
    s += '<circle cx="360" cy="155" r="45" fill="#0f172a" stroke="#2dd4bf" stroke-width="2"/>';
    s += '<text x="360" y="160" fill="#5eead4" font-size="12" text-anchor="middle">CONTROLLED REACTOR CELL</text>';
  }

  // Telemetry Box
  s += '<rect x="520" y="70" width="140" height="75" rx="4" fill="#042320" stroke="#0d9488" stroke-width="1.2"/>';
  s += '<text x="530" y="88" fill="#5eead4" font-size="9" font-weight="bold">' + cfg.rawLabel.toUpperCase() + '</text>';
  s += '<text x="530" y="112" fill="#2dd4bf" font-size="17" font-weight="bold">' + (measurement ? measurement.raw.toFixed(cfg.rawDecimals) : '—') + ' ' + cfg.rawUnit + '</text>';
  s += '<text x="530" y="134" fill="#99f6e4" font-size="9">' + cfg.shortInput + ': ' + val + ' ' + cfg.inputUnit + '</text>';
  return s;
}

function drawPrecisionEnergyModule(val, mode, num) {
  let s = '';
  s += '<rect x="40" y="55" width="640" height="210" fill="#141804" stroke="#84cc16" stroke-width="1.5" rx="6"/>';

  if (num === 36) {
    // Cone penetrometer profiling soil
    s += '<rect x="40" y="125" width="640" height="140" fill="url(#soilGrad)"/>';
    const coneDepth = 125 + val * 3.5;
    s += '<line x1="360" y1="75" x2="360" y2="' + coneDepth + '" stroke="#cbd5e1" stroke-width="4"/>';
    s += '<polygon points="354,' + coneDepth + ' 366,' + coneDepth + ' 360,' + (coneDepth + 12) + '" fill="#facc15"/>';
    s += '<text x="360" y="68" fill="#cbd5e1" font-size="10" text-anchor="middle">ASABE 30° CONE</text>';
  } else if (num === 38) {
    // Solar air collector
    s += '<polygon points="220,200 480,130 500,140 240,210" fill="#1e293b" stroke="#facc15" stroke-width="2"/>';
    // Sun rays
    for (let r = 0; r < 5; r++) {
      const rx = 280 + r * 45;
      s += '<line x1="' + rx + '" y1="80" x2="' + (rx + 20) + '" y2="135" stroke="#fde047" stroke-width="1.8" stroke-dasharray="3,2"/>';
    }
    s += '<text x="360" y="235" fill="#fde047" font-size="11" text-anchor="middle">SOLAR RADIATION ABSORBER ARRAY</text>';
  } else if (num === 41) {
    // Solar PV water pump
    s += '<rect x="180" y="90" width="120" height="80" fill="#1e3a8a" stroke="#38bdf8" stroke-width="2" rx="3"/>';
    s += '<line x1="300" y1="130" x2="420" y2="130" stroke="#facc15" stroke-width="2.5"/>';
    s += '<circle cx="450" cy="130" r="28" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>';
    s += '<path d="M 450 102 L 450 70 L 530 70" fill="none" stroke="#0284c7" stroke-width="4"/>';
    s += '<text x="240" y="185" fill="#7dd3fc" font-size="10" text-anchor="middle">PV ARRAY</text>';
    s += '<text x="450" y="175" fill="#38bdf8" font-size="10" text-anchor="middle">BLDC PUMP</text>';
  } else {
    // Biomass gasifier / biodiesel / variable rate
    s += '<rect x="220" y="80" width="280" height="145" rx="8" fill="#1e293b" stroke="#a3e635" stroke-width="2"/>';
    s += '<circle cx="360" cy="150" r="42" fill="#0f172a" stroke="#84cc16" stroke-width="2.5"/>';
    s += '<text x="360" y="155" fill="#bef264" font-size="11" text-anchor="middle">PRECISION ENERGY SYSTEM</text>';
  }

  // Telemetry Box
  s += '<rect x="520" y="70" width="140" height="75" rx="4" fill="#1c2404" stroke="#84cc16" stroke-width="1.2"/>';
  s += '<text x="530" y="88" fill="#bef264" font-size="9" font-weight="bold">' + cfg.rawLabel.toUpperCase() + '</text>';
  s += '<text x="530" y="112" fill="#a3e635" font-size="17" font-weight="bold">' + (measurement ? measurement.raw.toFixed(cfg.rawDecimals) : '—') + ' ' + cfg.rawUnit + '</text>';
  s += '<text x="530" y="134" fill="#d9f99d" font-size="9">' + cfg.shortInput + ': ' + val + ' ' + cfg.inputUnit + '</text>';
  return s;
}

// Initial Render
update();
renderNotebook();
