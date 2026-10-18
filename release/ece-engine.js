'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.ECEModels;
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
  message('Adjust ' + cfg.shortInput + ', then execute telecommunication RF/baseband acquisition.');
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
    if (mode === 'bench') notice.textContent = 'Hardware Bench: Standard telecommunication testbench with DSO and spectrum analyzer.';
    else if (mode === 'compare') notice.textContent = 'Analytical Compare: Direct comparison against Shannon-Nyquist / theoretical RF models.';
    else if (mode === 'sandbox') notice.textContent = 'RF Sandbox: Extended multi-variable modulation and channel parameter tuning.';
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
  message('Synchronizing RF oscillator and sampling channel signals…');
  if ($('readingValue')) $('readingValue').textContent = 'Acquiring…';

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
      message('Signal digitized. Log observation into laboratory dataset table.');
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
  if (confirm('Clear all logged communication trials from this session?')) {
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
      fitBox.innerHTML = '<p>Log at least 3 distinct observations to compute regression fit and communication parameter.</p>';
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

  let s = '<rect width="' + W + '" height="' + H + '" fill="#090d16" rx="6"/>';

  // Grid
  for (let i = 0; i <= 5; i++) {
    const gx = minX + (maxX - minX) * (i / 5);
    const gy = minY + (maxY - minY) * (i / 5);
    s += '<line x1="' + tx(gx) + '" y1="' + pad.top + '" x2="' + tx(gx) + '" y2="' + (pad.top + ph) + '" stroke="#1e1b4b" stroke-dasharray="2,2"/>';
    s += '<line x1="' + pad.left + '" y1="' + ty(gy) + '" x2="' + (pad.left + pw) + '" y2="' + ty(gy) + '" stroke="#1e1b4b" stroke-dasharray="2,2"/>';
    s += '<text x="' + tx(gx) + '" y="' + (H - 12) + '" fill="#a5b4fc" font-size="9" text-anchor="middle">' + fmt(gx, 1) + '</text>';
    s += '<text x="' + (pad.left - 8) + '" y="' + (ty(gy) + 3) + '" fill="#a5b4fc" font-size="9" text-anchor="end">' + fmt(gy, 1) + '</text>';
  }

  // Regression line
  if (fitRes && fitRes.n >= 2) {
    const x1 = minX;
    const y1 = (fitRes.slope * (x1 / cfg.xScale) + fitRes.intercept) * cfg.yScale;
    const x2 = maxX;
    const y2 = (fitRes.slope * (x2 / cfg.xScale) + fitRes.intercept) * cfg.yScale;
    s += '<line x1="' + tx(x1) + '" y1="' + ty(y1) + '" x2="' + tx(x2) + '" y2="' + ty(y2) + '" stroke="#818cf8" stroke-width="2"/>';
  }

  // Data points
  rows.forEach(r => {
    const px = tx(r.x * cfg.xScale);
    const py = ty(r.y * cfg.yScale);
    s += '<circle cx="' + px + '" cy="' + py + '" r="4.5" fill="#38bdf8" stroke="#4f46e5" stroke-width="1.5"/>';
  });

  // Labels
  s += '<text x="' + (W / 2) + '" y="' + (H - 2) + '" fill="#c7d2fe" font-size="10" text-anchor="middle">' + cfg.xLabel + '</text>';
  s += '<text transform="rotate(-90)" x="' + (-H / 2) + '" y="16" fill="#c7d2fe" font-size="10" text-anchor="middle">' + cfg.yLabel + '</text>';

  svg.innerHTML = s;
}

function draw(animStep=0) {
  const svg = $('visualSvg');
  if (!svg) return;
  const p = params();
  const pred = model.predict(cfg.slug, p.input);
  const frac = Math.min(1, Math.max(0, (p.input - cfg.min) / (cfg.max - cfg.min || 1)));

  let html = '<rect width="520" height="280" fill="#050811" rx="6"/>';

  if (currentSimMode === 'compare') {
    // Split screen: Experimental Transceiver vs Theoretical Channel
    html += '<line x1="260" y1="20" x2="260" y2="260" stroke="#1e1b4b" stroke-width="2" stroke-dasharray="4,4"/>';
    html += '<text x="130" y="35" fill="#818cf8" font-size="11" font-weight="600" text-anchor="middle">LIVE TRANSDUCER & CHANNEL</text>';
    html += '<text x="390" y="35" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="middle">IDEAL THEORETICAL BENCHMARK</text>';

    // Left: Measured signal waveform
    html += '<rect x="25" y="55" width="210" height="180" fill="#090d16" stroke="#312e81" rx="5"/>';
    let path1 = 'M 30 ' + (145 + Math.sin(0) * 40 * frac);
    for (let x = 30; x <= 230; x += 5) {
      const angle = (x - 30) * 0.15 + animStep * 0.5;
      const noise = (Math.random() - 0.5) * 6 * (1 - frac);
      const y = 145 + Math.sin(angle) * (35 * frac + 10) + noise;
      path1 += ' L ' + x + ' ' + y.toFixed(1);
    }
    html += '<path d="' + path1 + '" fill="none" stroke="#818cf8" stroke-width="2"/>';
    html += '<text x="130" y="225" fill="#94a3b8" font-size="9" text-anchor="middle">Observed Output: ' + pred.displayed.toFixed(2) + ' ' + cfg.rawUnit + '</text>';

    // Right: Ideal theoretical waveform
    html += '<rect x="285" y="55" width="210" height="180" fill="#090d16" stroke="#312e81" rx="5"/>';
    let path2 = 'M 290 ' + (145 + Math.sin(0) * 40 * frac);
    for (let x = 290; x <= 490; x += 5) {
      const angle = (x - 290) * 0.15 + animStep * 0.5;
      const y = 145 + Math.sin(angle) * (35 * frac + 10);
      path2 += ' L ' + x + ' ' + y.toFixed(1);
    }
    html += '<path d="' + path2 + '" fill="none" stroke="#38bdf8" stroke-width="2"/>';
    html += '<text x="390" y="225" fill="#94a3b8" font-size="9" text-anchor="middle">Theoretical Model: ' + (p.input * cfg.refValue).toFixed(2) + ' ' + cfg.rawUnit + '</text>';

  } else {
    // Bench or Sandbox Mode: Full DSO & Spectrum Analyzer Display
    html += '<rect x="20" y="20" width="480" height="240" fill="#090d16" stroke="#312e81" stroke-width="1.5" rx="6"/>';

    // Graticule Grid (Oscilloscope style)
    for (let x = 50; x <= 470; x += 40) {
      html += '<line x1="' + x + '" y1="30" x2="' + x + '" y2="250" stroke="#1e1b4b" stroke-width="0.75" stroke-dasharray="2,2"/>';
    }
    for (let y = 45; y <= 235; y += 38) {
      html += '<line x1="30" y1="' + y + '" x2="' + x + '" y2="' + y + '" stroke="#1e1b4b" stroke-width="0.75" stroke-dasharray="2,2"/>';
    }

    // Central crosshair graticules
    html += '<line x1="260" y1="30" x2="260" y2="250" stroke="#3730a3" stroke-width="1"/>';
    html += '<line x1="30" y1="140" x2="490" y2="140" stroke="#3730a3" stroke-width="1"/>';

    // Top status readout
    html += '<rect x="30" y="26" width="460" height="22" fill="#030712" rx="3"/>';
    html += '<text x="40" y="41" fill="#818cf8" font-size="10" font-family="monospace">CH1: 1.00V/div</text>';
    html += '<text x="140" y="41" fill="#38bdf8" font-size="10" font-family="monospace">TIME: 200us/div</text>';
    html += '<text x="250" y="41" fill="#34d399" font-size="10" font-family="monospace">TRIG: AUTO 0.00V</text>';
    html += '<text x="400" y="41" fill="#f43f5e" font-size="10" font-family="monospace">SAMPL: 100MS/s</text>';

    // Animated RF / Communication Waveform
    let wPath = 'M 30 ' + (140 + Math.sin(0) * (45 * frac + 10));
    for (let x = 30; x <= 490; x += 3) {
      const angle = (x - 30) * 0.1 + animStep * 0.6;
      let amp = (45 * frac + 10);
      // If modulation or carrier, create beating/envelope
      if (cfg.slug.includes('amplitude') || cfg.slug.includes('suppressed') || cfg.slug.includes('qam')) {
        amp *= (0.6 + 0.4 * Math.cos((x - 30) * 0.02));
      }
      const y = 140 + Math.sin(angle) * amp;
      wPath += ' L ' + x + ' ' + y.toFixed(1);
    }
    html += '<path d="' + wPath + '" fill="none" stroke="#818cf8" stroke-width="2.2" stroke-linecap="round"/>';

    // Modulation envelope or carrier guide
    if (cfg.slug.includes('amplitude') || cfg.slug.includes('suppressed')) {
      let envTop = 'M 30 ' + (140 - (45 * frac + 10) * (0.6 + 0.4 * Math.cos(0)));
      let envBot = 'M 30 ' + (140 + (45 * frac + 10) * (0.6 + 0.4 * Math.cos(0)));
      for (let x = 30; x <= 490; x += 10) {
        const topY = 140 - (45 * frac + 10) * (0.6 + 0.4 * Math.cos((x - 30) * 0.02));
        const botY = 140 + (45 * frac + 10) * (0.6 + 0.4 * Math.cos((x - 30) * 0.02));
        envTop += ' L ' + x + ' ' + topY.toFixed(1);
        envBot += ' L ' + x + ' ' + botY.toFixed(1);
      }
      html += '<path d="' + envTop + '" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="3,3"/>';
      html += '<path d="' + envBot + '" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="3,3"/>';
    }

    // Lower DSO Banner / Measured Value
    html += '<rect x="30" y="215" width="460" height="28" fill="rgba(3,7,18,0.85)" rx="3"/>';
    html += '<text x="45" y="233" fill="#a5b4fc" font-size="10">' + cfg.indepName + ': <tspan fill="#ffffff" font-weight="600">' + p.input.toFixed(cfg.inputDecimals) + ' ' + cfg.inputUnit + '</tspan></text>';
    html += '<text x="270" y="233" fill="#38bdf8" font-size="10">' + cfg.depName + ': <tspan fill="#ffffff" font-weight="600">' + pred.displayed.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit + '</tspan></text>';
  }

  svg.innerHTML = html;
}

renderTable();
update();
