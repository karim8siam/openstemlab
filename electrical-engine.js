'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.ElectricalModels;
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
  message('Adjust ' + cfg.shortInput + ', then execute electrical instrumentation acquisition.');
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
    message('Sampling instrumentation signals & digital acquisition...');
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
                         '<p class="report-equation">Linear fit: <em>y</em> = ' + fmt(fitRes.slope, 4) + ' <em>x</em> ' + (fitRes.intercept >= 0 ? '+ ' : '- ') + fmt(Math.abs(fitRes.intercept), 4) + '</p>' +
                         '<p>Correlation coefficient: <em>R</em>² = ' + fitRes.r2.toFixed(6) + ' (<em>N</em> = ' + fitRes.n + ')</p>' +
                         '<p>Error vs Reference: ' + est.errorPercent.toFixed(3) + '% | Reference benchmark: ' + cfg.refValue + ' ' + cfg.resultUnit + '</p>';
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

  // Regression line
  if (fitRes && fitRes.n >= 2) {
    const x1 = minX;
    const y1 = (fitRes.slope * (x1 / cfg.xScale) + fitRes.intercept) * cfg.yScale;
    const x2 = maxX;
    const y2 = (fitRes.slope * (x2 / cfg.xScale) + fitRes.intercept) * cfg.yScale;
    s += '<line x1="' + tx(x1) + '" y1="' + ty(y1) + '" x2="' + tx(x2) + '" y2="' + ty(y2) + '" stroke="#38bdf8" stroke-width="2"/>';
  }

  // Data points
  rows.forEach(r => {
    const px = tx(r.x * cfg.xScale);
    const py = ty(r.y * cfg.yScale);
    s += '<circle cx="' + px + '" cy="' + py + '" r="4.5" fill="#38bdf8" stroke="#0284c7" stroke-width="1.5"/>';
  });

  // Labels
  s += '<text x="' + (W / 2) + '" y="' + (H - 2) + '" fill="#cbd5e1" font-size="10" text-anchor="middle">' + cfg.xLabel + '</text>';
  s += '<text transform="rotate(-90)" x="' + (-H / 2) + '" y="16" fill="#cbd5e1" font-size="10" text-anchor="middle">' + cfg.yLabel + '</text>';

  svg.innerHTML = s;
}

function draw() {
  const svg = $('visualSvg');
  if (!svg) return;
  const p = params();
  const pred = model.predict(cfg.slug, p.input);
  const frac = Math.min(1, Math.max(0, (p.input - cfg.min) / (cfg.max - cfg.min || 1)));

  let html = '<rect width="520" height="280" fill="#0b1329" rx="6"/>';

  if (currentSimMode === 'compare') {
    // Split screen: Experimental Circuit vs SPICE / Analytical Benchmark
    html += '<line x1="260" y1="20" x2="260" y2="260" stroke="#1e293b" stroke-width="2" stroke-dasharray="4,4"/>';
    html += '<text x="130" y="35" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="middle">LIVE TRANSDUCER & CIRCUIT</text>';
    html += '<text x="390" y="35" fill="#a5f3fc" font-size="11" font-weight="600" text-anchor="middle">SPICE / THEORETICAL BENCHMARK</text>';

    // Left: Hardware schematic trace
    html += '<rect x="30" y="60" width="200" height="170" rx="6" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>';
    html += '<circle cx="60" cy="145" r="18" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>';
    html += '<text x="60" y="149" fill="#38bdf8" font-size="10" font-weight="bold" text-anchor="middle">~</text>';
    html += '<line x1="78" y1="145" x2="110" y2="145" stroke="#38bdf8" stroke-width="2"/>';
    html += '<rect x="110" y="137" width="40" height="16" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>';
    html += '<text x="130" y="149" fill="#cbd5e1" font-size="9" text-anchor="middle">DUT</text>';
    html += '<line x1="150" y1="145" x2="190" y2="145" stroke="#38bdf8" stroke-width="2"/>';
    html += '<circle cx="190" cy="145" r="4" fill="#38bdf8"/>';
    html += '<text x="130" y="215" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="middle">V_meas = ' + pred.raw.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit + '</text>';

    // Right: SPICE reference trace
    html += '<rect x="290" y="60" width="200" height="170" rx="6" fill="#0f172a" stroke="#06b6d4" stroke-width="1.5"/>';
    html += '<path d="M 310 ' + (180 - frac * 80) + ' Q 380 ' + (140 - frac * 40) + ' 470 ' + (100 - frac * 20) + '" fill="none" stroke="#22d3ee" stroke-width="2.5"/>';
    html += '<text x="390" y="215" fill="#22d3ee" font-size="11" font-weight="600" text-anchor="middle">V_ref = ' + (cfg.refValue) + ' ' + cfg.resultUnit + '</text>';
  } else if (currentSimMode === 'sandbox') {
    // Sandbox oscilloscope & interactive vector display
    html += '<rect x="25" y="25" width="470" height="230" rx="6" fill="#050b14" stroke="#0284c7" stroke-width="2"/>';
    // Oscilloscope grid
    for (let gx = 50; gx <= 470; gx += 35) {
      html += '<line x1="' + gx + '" y1="35" x2="' + gx + '" y2="245" stroke="#0f2942" stroke-width="1" stroke-dasharray="1,3"/>';
    }
    for (let gy = 45; gy <= 245; gy += 25) {
      html += '<line x1="35" y1="' + gy + '" x2="' + 485 + '" y2="' + gy + '" stroke="#0f2942" stroke-width="1" stroke-dasharray="1,3"/>';
    }
    // Dynamic waveform trace
    let dWave = 'M 35 140 ';
    for (let x = 35; x <= 485; x += 5) {
      const theta = (x - 35) * 0.04 * (1 + frac * 2);
      const y = 140 - Math.sin(theta) * (20 + frac * 65);
      dWave += 'L ' + x + ' ' + y.toFixed(1) + ' ';
    }
    html += '<path d="' + dWave + '" fill="none" stroke="#38bdf8" stroke-width="2.5"/>';
    html += '<rect x="40" y="40" width="160" height="42" rx="4" fill="#0f172a" stroke="#0284c7" opacity="0.9"/>';
    html += '<text x="48" y="56" fill="#38bdf8" font-size="10" font-weight="bold">CH1: 5.0 V/div  AC Coupling</text>';
    html += '<text x="48" y="72" fill="#cbd5e1" font-size="9">f_sig = ' + (p.input).toFixed(1) + ' ' + cfg.inputUnit + ' | PK-PK = ' + pred.raw.toFixed(2) + ' ' + cfg.rawUnit + '</text>';
  } else {
    // Default Bench Mode: Comprehensive Circuit Schematic & Instrumentation Rack
    html += '<rect x="25" y="25" width="470" height="230" rx="6" fill="#080e1e" stroke="#1e293b" stroke-width="1.5"/>';

    // Instrumentation Display Rack (Power Supply, Digital Multimeter & Function Generator)
    html += '<rect x="45" y="45" width="200" height="90" rx="5" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>';
    html += '<rect x="55" y="55" width="180" height="34" rx="3" fill="#020617"/>';
    html += '<text x="65" y="78" fill="#38bdf8" font-size="16" font-family="monospace" font-weight="bold">' + p.input.toFixed(cfg.inputDecimals) + ' ' + cfg.inputUnit + '</text>';
    html += '<text x="55" y="105" fill="#94a3b8" font-size="9">REGULATED INPUT SOURCE (' + cfg.shortInput + ')</text>';
    html += '<circle cx="65" cy="120" r="4" fill="#ef4444"/><circle cx="85" cy="120" r="4" fill="#0f172a" stroke="#cbd5e1"/>';

    // Digital Multimeter (DMM) / Output Monitor
    html += '<rect x="275" y="45" width="200" height="90" rx="5" fill="#0f172a" stroke="#0369a1" stroke-width="1.5"/>';
    html += '<rect x="285" y="55" width="180" height="34" rx="3" fill="#020617"/>';
    html += '<text x="295" y="78" fill="#38bdf8" font-size="16" font-family="monospace" font-weight="bold">' + pred.raw.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit + '</text>';
    html += '<text x="285" y="105" fill="#94a3b8" font-size="9">TRUE-RMS MEASUREMENT (' + cfg.rawLabel + ')</text>';
    html += '<circle cx="295" cy="120" r="4" fill="#ef4444"/><circle cx="315" cy="120" r="4" fill="#0f172a" stroke="#cbd5e1"/>';

    // Circuit Breadboard / Subsystem Interconnect
    html += '<rect x="45" y="150" width="430" height="90" rx="5" fill="#020617" stroke="#334155" stroke-width="1.5"/>';
    html += '<line x1="80" y1="195" x2="160" y2="195" stroke="#38bdf8" stroke-width="2.5"/>';
    html += '<rect x="160" y="185" width="60" height="20" rx="3" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>';
    html += '<text x="190" y="199" fill="#f8fafc" font-size="10" text-anchor="middle">CIRCUIT</text>';
    html += '<line x1="220" y1="195" x2="300" y2="195" stroke="#38bdf8" stroke-width="2.5"/>';
    html += '<circle cx="300" cy="195" r="14" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>';
    html += '<text x="300" y="199" fill="#38bdf8" font-size="10" font-weight="bold" text-anchor="middle">A/V</text>';
    html += '<line x1="314" y1="195" x2="440" y2="195" stroke="#38bdf8" stroke-width="2.5"/>';
    html += '<text x="260" y="228" fill="#94a3b8" font-size="10" text-anchor="middle">' + cfg.title + '</text>';
  }

  svg.innerHTML = html;
}

if ($('clearData')) {
  $('clearData').onclick = () => {
    if (confirm('Clear all recorded observations for this experiment?')) {
      rows = [];
      persist();
      renderResults();
      message('Observation table cleared.');
    }
  };
}

update();
renderResults();
