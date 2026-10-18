'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.TextileModels;
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
  message('Adjust ' + cfg.shortInput + ', then execute textile test acquisition.');
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
  message('Conditioning standard atmosphere (20 °C, 65% RH) and acquiring textile transducer telemetry…');

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
      message('Measurement captured. Click "+ Record observation" to save to the notebook.');
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
  message('Observation recorded (' + rows.length + ' in notebook). Select new setpoint or repeat trial.');
});

if ($('clearData')) $('clearData').addEventListener('click', () => {
  if (rows.length === 0) return;
  if (confirm('Clear all recorded textile observations from your notebook?')) {
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
      fitBox.innerHTML = '<p>Log at least 3 distinct observations to compute regression fit and textile parameter.</p>';
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

  let s = '<rect width="' + W + '" height="' + H + '" fill="#0f051d" rx="6"/>';

  // Grid
  for (let i = 0; i <= 5; i++) {
    const gx = minX + (maxX - minX) * (i / 5);
    const gy = minY + (maxY - minY) * (i / 5);
    s += '<line x1="' + tx(gx) + '" y1="' + pad.top + '" x2="' + tx(gx) + '" y2="' + (pad.top + ph) + '" stroke="#2e1065" stroke-dasharray="2,2"/>';
    s += '<line x1="' + pad.left + '" y1="' + ty(gy) + '" x2="' + (pad.left + pw) + '" y2="' + ty(gy) + '" stroke="#2e1065" stroke-dasharray="2,2"/>';
    s += '<text x="' + tx(gx) + '" y="' + (H - 12) + '" fill="#c084fc" font-size="9" text-anchor="middle">' + fmt(gx, 1) + '</text>';
    s += '<text x="' + (pad.left - 8) + '" y="' + (ty(gy) + 3) + '" fill="#c084fc" font-size="9" text-anchor="end">' + fmt(gy, 1) + '</text>';
  }

  // Regression line
  if (fitRes && fitRes.n >= 2) {
    const x1 = minX;
    const y1 = (fitRes.slope * (x1 / cfg.xScale) + fitRes.intercept) * cfg.yScale;
    const x2 = maxX;
    const y2 = (fitRes.slope * (x2 / cfg.xScale) + fitRes.intercept) * cfg.yScale;
    s += '<line x1="' + tx(x1) + '" y1="' + ty(y1) + '" x2="' + tx(x2) + '" y2="' + ty(y2) + '" stroke="#c084fc" stroke-width="2"/>';
  }

  // Data points
  rows.forEach(r => {
    const px = tx(r.x * cfg.xScale);
    const py = ty(r.y * cfg.yScale);
    s += '<circle cx="' + px + '" cy="' + py + '" r="4.5" fill="#e879f9" stroke="#9333ea" stroke-width="1.5"/>';
  });

  // Labels
  s += '<text x="' + (W / 2) + '" y="' + (H - 2) + '" fill="#f5d0fe" font-size="10" text-anchor="middle">' + cfg.xAxis + '</text>';
  s += '<text transform="rotate(-90)" x="' + (-H / 2) + '" y="16" fill="#f5d0fe" font-size="10" text-anchor="middle">' + cfg.yAxis + '</text>';

  svg.innerHTML = s;
}

function draw(animStep=0) {
  const svg = $('visualSvg');
  if (!svg) return;
  const p = params();
  const pred = model.predict(cfg.slug, p.input);
  const frac = Math.min(1, Math.max(0, (p.input - cfg.min) / (cfg.max - cfg.min || 1)));

  let html = '<rect width="520" height="280" fill="#0f051d" rx="6"/>';

  if (currentSimMode === 'compare') {
    // Split screen: Experimental Textile Testing vs ASTM/ISO Reference Standard
    html += '<line x1="260" y1="20" x2="260" y2="260" stroke="#581c87" stroke-width="2" stroke-dasharray="4,4"/>';
    html += '<text x="130" y="35" fill="#e879f9" font-size="11" font-weight="600" text-anchor="middle">LIVE TEXTILE SPECIMEN</text>';
    html += '<text x="390" y="35" fill="#d8b4fe" font-size="11" font-weight="600" text-anchor="middle">STANDARD ASTM / ISO REFERENCE</text>';

    // Left: Real physical specimen
    html += '<rect x="25" y="55" width="210" height="180" fill="#1a0b2e" stroke="#581c87" rx="5"/>';
    const defl = 12 * frac + animStep;
    html += '<rect x="40" y="130" width="180" height="22" fill="#701a75" rx="2"/>';
    html += '<line x1="130" y1="70" x2="130" y2="' + (130 + defl) + '" stroke="#e879f9" stroke-width="3"/>';
    html += '<polygon points="' + (125) + ',' + (125 + defl) + ' ' + (135) + ',' + (125 + defl) + ' ' + (130) + ',' + (134 + defl) + '" fill="#e879f9"/>';
    html += '<text x="130" y="215" fill="#c084fc" font-size="9" text-anchor="middle">Measured Metric: ' + pred.displayed.toFixed(2) + ' ' + cfg.rawUnit + '</text>';

    // Right: Ideal reference characteristic
    html += '<rect x="285" y="55" width="210" height="180" fill="#1a0b2e" stroke="#581c87" rx="5"/>';
    html += '<path d="M305,200 C340,180 400,120 475,85" stroke="#a855f7" stroke-width="2" fill="none" stroke-dasharray="3,3"/>';
    const idealY = 200 - 110 * frac;
    html += '<circle cx="' + (305 + 165 * frac) + '" cy="' + idealY + '" r="5" fill="#c084fc"/>';
    html += '<text x="390" y="215" fill="#d8b4fe" font-size="9" text-anchor="middle">Reference Target: ' + (cfg.refValue || 0) + ' ' + cfg.resultUnit + '</text>';
  } else if (currentSimMode === 'sandbox') {
    // Sandbox: Multi-Parameter Conditioning Environment (Humidity, Clamping, Pre-tension)
    html += '<rect x="20" y="25" width="480" height="230" fill="#1a0b2e" stroke="#581c87" rx="6"/>';
    html += '<text x="260" y="48" fill="#f5d0fe" font-size="12" font-weight="600" text-anchor="middle">TEXTILE TESTING ENVIRONMENT &amp; CLIMATE LAB</text>';

    html += '<rect x="40" y="70" width="130" height="65" fill="#2e1065" stroke="#581c87" rx="4"/>';
    html += '<text x="105" y="90" fill="#c084fc" font-size="9" text-anchor="middle">STANDARD CLIMATE</text>';
    html += '<text x="105" y="112" fill="#e879f9" font-size="14" font-weight="700" text-anchor="middle">20.0 °C / 65% RH</text>';

    html += '<rect x="195" y="70" width="130" height="65" fill="#2e1065" stroke="#581c87" rx="4"/>';
    html += '<text x="260" y="90" fill="#c084fc" font-size="9" text-anchor="middle">SETPOINT INPUT</text>';
    html += '<text x="260" y="112" fill="#e879f9" font-size="14" font-weight="700" text-anchor="middle">' + p.input.toFixed(1) + ' ' + cfg.inputUnit + '</text>';

    html += '<rect x="350" y="70" width="130" height="65" fill="#2e1065" stroke="#581c87" rx="4"/>';
    html += '<text x="415" y="90" fill="#c084fc" font-size="9" text-anchor="middle">INSTRUMENT TELEMETRY</text>';
    html += '<text x="415" y="112" fill="#e879f9" font-size="14" font-weight="700" text-anchor="middle">' + pred.displayed.toFixed(2) + ' ' + cfg.rawUnit + '</text>';

    // Animated textile fiber / yarn / weave preview
    html += '<g transform="translate(60, 155)">';
    for (let i = 0; i < 20; i++) {
      const x = i * 20;
      html += '<line x1="' + x + '" y1="0" x2="' + x + '" y2="70" stroke="#701a75" stroke-width="2"/>';
    }
    for (let j = 0; j < 4; j++) {
      const y = j * 20 + 5;
      html += '<line x1="0" y1="' + y + '" x2="380" y2="' + y + '" stroke="#a855f7" stroke-width="2.5" stroke-dasharray="10,10"/>';
    }
    html += '</g>';
    html += '<text x="260" y="246" fill="#a855f7" font-size="9" text-anchor="middle">Yarn interlacing / fiber morphology dynamically conditioned under continuous tension</text>';
  } else {
    // Bench Mode: High-Precision Instrument Visualizer
    html += '<rect x="30" y="20" width="460" height="240" fill="#140727" stroke="#3b0764" rx="8"/>';

    // Top Header
    html += '<text x="50" y="42" fill="#f5d0fe" font-size="11" font-weight="600">' + cfg.title.toUpperCase() + '</text>';
    html += '<text x="470" y="42" fill="#c084fc" font-size="10" text-anchor="end">CALIBRATED ISO/ASTM GAUGE</text>';
    html += '<line x1="50" y1="50" x2="470" y2="50" stroke="#581c87" stroke-width="1"/>';

    // Instrument Jaws / Clamps / Beaker / Chamber
    const jawY = 80 + 35 * frac + animStep;
    html += '<rect x="70" y="65" width="120" height="15" fill="#3b0764" stroke="#a855f7" rx="3"/>';
    html += '<rect x="70" y="210" width="120" height="15" fill="#3b0764" stroke="#a855f7" rx="3"/>';
    html += '<text x="130" y="76" fill="#f5d0fe" font-size="8" text-anchor="middle">UPPER PNEUMATIC CLAMP</text>';
    html += '<text x="130" y="221" fill="#f5d0fe" font-size="8" text-anchor="middle">LOWER FIXED ANVIL</text>';

    // Yarn / Fabric specimen strip clamped between jaws
    const specWidth = 12 + 10 * (1 - frac * 0.3);
    html += '<rect x="' + (130 - specWidth/2) + '" y="80" width="' + specWidth + '" height="130" fill="#c026d3" opacity="0.85" rx="1"/>';
    // Tension lines across specimen
    for (let k = 0; k < 5; k++) {
      const lineY = 95 + k * 23;
      html += '<line x1="' + (130 - specWidth/2) + '" y1="' + lineY + '" x2="' + (130 + specWidth/2) + '" y2="' + lineY + '" stroke="#fdf4ff" stroke-width="1" opacity="0.6"/>';
    }

    // Force / Displacement / Optical Gauge Dial
    html += '<g transform="translate(340, 145)">';
    html += '<circle cx="0" cy="0" r="62" fill="#1e1035" stroke="#581c87" stroke-width="3"/>';
    html += '<circle cx="0" cy="0" r="54" fill="#0f051d" stroke="#3b0764" stroke-width="1"/>';
    for (let a = 0; a < 12; a++) {
      const rad = (a * 30 - 90) * Math.PI / 180;
      html += '<line x1="' + (46 * Math.cos(rad)) + '" y1="' + (46 * Math.sin(rad)) + '" x2="' + (52 * Math.cos(rad)) + '" y2="' + (52 * Math.sin(rad)) + '" stroke="#a855f7" stroke-width="1.5"/>';
    }
    const angle = (-120 + 240 * frac) * Math.PI / 180;
    html += '<line x1="0" y1="0" x2="' + (44 * Math.cos(angle)) + '" y2="' + (44 * Math.sin(angle)) + '" stroke="#e879f9" stroke-width="2.5"/>';
    html += '<circle cx="0" cy="0" r="4" fill="#fdf4ff"/>';
    html += '<text x="0" y="24" fill="#f5d0fe" font-size="10" font-weight="700" text-anchor="middle">' + pred.displayed.toFixed(1) + '</text>';
    html += '<text x="0" y="36" fill="#c084fc" font-size="8" text-anchor="middle">' + cfg.rawUnit + '</text>';
    html += '</g>';

    // Status readout overlay
    html += '<rect x="220" y="222" width="250" height="24" fill="#2e1065" stroke="#581c87" rx="3"/>';
    html += '<text x="345" y="238" fill="#f5d0fe" font-size="9" text-anchor="middle">' + cfg.shortInput + ': ' + p.input.toFixed(1) + ' ' + cfg.inputUnit + ' ➔ ' + pred.displayed.toFixed(2) + ' ' + cfg.rawUnit + '</text>';
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
