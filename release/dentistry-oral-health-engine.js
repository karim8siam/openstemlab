'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.DentistryModels;
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
  message('Adjust ' + cfg.shortInput + ', then execute dental acquisition.');
  draw();
}

if ($('independent')) $('independent').addEventListener('input', () => {
  if ($('independentNumber')) $('independentNumber').value = $('independent').value;
  update();
});

if ($('independentNumber')) {
  $('independentNumber').addEventListener('input', () => {
    let v = +$('independentNumber').value;
    if (Number.isFinite(v)) {
      v = Math.min(cfg.max, Math.max(cfg.min, v));
      $('independent').value = v;
      update();
    }
  });
}

function draw() {
  const svg = $('visualSvg');
  if (!svg) return;
  const p = params();
  const inputRatio = (p.input - cfg.min) / (cfg.max - cfg.min || 1.0);
  const measuredVal = measurement ? measurement.raw : (p.input * 0.5);

  let scene = '';
  if (currentSimMode === 'compare') {
    scene = `
      <rect x="20" y="20" width="225" height="240" fill="#083344" rx="8" stroke="#0e7490" stroke-width="1.5"/>
      <rect x="275" y="20" width="225" height="240" fill="#083344" rx="8" stroke="#06b6d4" stroke-width="1.5"/>
      <text x="132" y="44" fill="#a5f3fc" font-size="11" font-weight="600" text-anchor="middle">STANDARD SPECIMEN</text>
      <text x="387" y="44" fill="#a5f3fc" font-size="11" font-weight="600" text-anchor="middle">CALIBRATED CLINICAL SPECIMEN</text>
      <path d="M 132 80 L 100 190 Q 132 210 164 190 Z" fill="#155e75" stroke="#38bdf8" stroke-width="2"/>
      <path d="M 387 80 L 355 190 Q 387 210 419 190 Z" fill="#0e7490" stroke="#22d3ee" stroke-width="2"/>
      <line x1="320" y1="${190 - inputRatio * 80}" x2="450" y2="${190 - inputRatio * 80}" stroke="#facc15" stroke-width="2" stroke-dasharray="4,2"/>
      <text x="132" y="235" fill="#bae6fd" font-size="10" text-anchor="middle">Nominal Control</text>
      <text x="387" y="235" fill="#fde047" font-size="10" text-anchor="middle">${cfg.shortInput}: ${p.input.toFixed(cfg.inputDecimals)} ${cfg.inputUnit}</text>
    `;
  } else if (currentSimMode === 'sandbox') {
    scene = `
      <defs>
        <pattern id="dentalGrid" width="20" height="20" patternUnits="userSpaceOnUse">
          <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#155e75" stroke-width="0.8"/>
        </pattern>
      </defs>
      <rect x="20" y="20" width="480" height="240" fill="#083344" rx="8"/>
      <rect x="20" y="20" width="480" height="240" fill="url(#dentalGrid)" rx="8"/>
      <text x="260" y="45" fill="#22d3ee" font-size="12" font-weight="700" text-anchor="middle">BIOMATERIALS &amp; ORAL BIOMECHANICS SANDBOX</text>
      <circle cx="${60 + inputRatio * 400}" cy="${220 - (inputRatio * 140)}" r="10" fill="#06b6d4" stroke="#ffffff" stroke-width="2"/>
      <line x1="60" y1="220" x2="460" y2="80" stroke="#0284c7" stroke-width="2" stroke-dasharray="5,3"/>
      <text x="260" y="240" fill="#94a3b8" font-size="10" text-anchor="middle">Dynamic Biomaterial Stress-Deformation Mapping</text>
    `;
  } else {
    // Bench View
    const fillH = 30 + inputRatio * 110;
    scene = `
      <!-- Dental Apparatus Bench Frame -->
      <rect x="40" y="25" width="440" height="230" fill="#083344" rx="8" stroke="#155e75" stroke-width="2"/>
      <text x="60" y="50" fill="#38bdf8" font-size="12" font-weight="700">DENTAL CLINICAL WORKBENCH</text>
      <text x="60" y="66" fill="#94a3b8" font-size="10">${cfg.shortTitle}</text>

      <!-- Testing Chamber / Die Base -->
      <rect x="190" y="90" width="140" height="130" fill="#0f172a" rx="6" stroke="#0284c7" stroke-width="2"/>
      <!-- Tooth / Restoration Specimen -->
      <path d="M 230 180 C 230 140 240 120 260 120 C 280 120 290 140 290 180 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
      <!-- Measurement Indenter / Sensor Probe -->
      <line x1="260" y1="${60 + inputRatio * 40}" x2="260" y2="120" stroke="#f43f5e" stroke-width="3"/>
      <polygon points="255,120 265,120 260,126" fill="#f43f5e"/>

      <!-- Digital Telemetry Screen -->
      <rect x="350" y="90" width="115" height="120" fill="#020617" rx="4" stroke="#0e7490" stroke-width="1.5"/>
      <text x="360" y="112" fill="#38bdf8" font-size="9" font-weight="600">TRANSDUCER</text>
      <text x="360" y="132" fill="#22d3ee" font-size="14" font-weight="700" font-family="monospace">${measurement ? fmt(measurement.raw, cfg.rawDecimals) : '---'}</text>
      <text x="360" y="148" fill="#64748b" font-size="9">${cfg.rawUnit}</text>
      <text x="360" y="176" fill="#94a3b8" font-size="8">STATUS</text>
      <text x="360" y="192" fill="${measurement ? '#4ade80' : '#f59e0b'}" font-size="9" font-weight="600">${measurement ? 'ACQUIRED' : 'STANDBY'}</text>

      <!-- Input Scale Bar -->
      <rect x="60" y="90" width="110" height="120" fill="#0f172a" rx="4" stroke="#1e293b"/>
      <text x="70" y="112" fill="#94a3b8" font-size="9">SETPOINT</text>
      <text x="70" y="132" fill="#facc15" font-size="13" font-weight="700" font-family="monospace">${p.input.toFixed(cfg.inputDecimals)}</text>
      <text x="70" y="146" fill="#64748b" font-size="9">${cfg.inputUnit}</text>
      <rect x="70" y="165" width="90" height="8" fill="#1e293b" rx="2"/>
      <rect x="70" y="165" width="${inputRatio * 90}" height="8" fill="#38bdf8" rx="2"/>
    `;
  }
  svg.innerHTML = scene;
}

if ($('measure')) $('measure').addEventListener('click', () => {
  if (busy) return;
  busy = true;
  $('measure').disabled = true;
  message('Acquiring clinical telemetry and biophysical data…');
  setTimeout(() => {
    const p = params();
    const pred = model.predict(cfg.slug, p.input);
    measurement = model.reading(cfg.slug, p.input, pred.raw);
    busy = false;
    $('measure').disabled = false;
    $('recordReading').disabled = false;
    if ($('readingValue')) $('readingValue').textContent = fmt(measurement.raw, cfg.rawDecimals) + ' ' + cfg.rawUnit;
    if ($('liveState')) $('liveState').textContent = 'Telemetry acquired: ' + cfg.rawLabel + ' = ' + fmt(measurement.raw, cfg.rawDecimals) + ' ' + cfg.rawUnit + '.';
    message('Trial complete. Click "Record observation" to log in notebook.');
    draw();
  }, 250);
});

if ($('recordReading')) $('recordReading').addEventListener('click', () => {
  if (!measurement) return;
  rows.push(measurement);
  try {
    localStorage.setItem('openstemlab-' + cfg.slug + '-v1', JSON.stringify(rows));
  } catch (e) {}
  $('recordReading').disabled = true;
  message('Observation logged in notebook (' + rows.length + ' total).');
  renderTable();
  renderPlot();
});

if ($('clearData')) $('clearData').addEventListener('click', () => {
  if (confirm('Clear recorded observations for this experiment?')) {
    rows = [];
    try {
      localStorage.removeItem('openstemlab-' + cfg.slug + '-v1');
    } catch (e) {}
    renderTable();
    renderPlot();
    message('Notebook cleared.');
  }
});

if ($('resetApparatus')) $('resetApparatus').addEventListener('click', () => {
  $('independent').value = cfg.initial;
  if ($('independentNumber')) $('independentNumber').value = cfg.initial;
  measurement = null;
  update();
});

function renderTable() {
  const tb = $('readingsBody');
  const emp = $('emptyReadings');
  const count = $('notebookCount');
  if (count) count.textContent = rows.length;
  if (!tb) return;
  tb.innerHTML = '';
  if (rows.length === 0) {
    if (emp) emp.hidden = false;
    return;
  }
  if (emp) emp.hidden = true;
  rows.forEach((r, idx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${idx+1}</td><td>${fmt(r.input, cfg.inputDecimals)}</td><td>${fmt(r.raw, cfg.rawDecimals)}</td><td>${fmt(r.x, 4)}</td><td>${fmt(r.y, 4)}</td>`;
    tb.appendChild(tr);
  });
}

function renderPlot() {
  const plot = $('labPlot');
  const fitBox = $('fitResult');
  if (!plot) return;
  if (rows.length < 2) {
    plot.innerHTML = `<rect width="520" height="260" fill="#083344" rx="4"/><text x="260" y="135" fill="#38bdf8" font-size="12" text-anchor="middle">Record at least 2 observations to generate regression fit.</text>`;
    if (fitBox) fitBox.innerHTML = '<p style="color:#64748b;font-size:12px">Awaiting data points for OLS fit…</p>';
    return;
  }
  const fitRes = model.fit(rows);
  const xs = rows.map(r => r.x);
  const ys = rows.map(r => r.y);
  let minX = Math.min(...xs), maxX = Math.max(...xs);
  let minY = Math.min(...ys), maxY = Math.max(...ys);
  if (minX === maxX) { minX -= 1; maxX += 1; }
  if (minY === maxY) { minY -= 1; maxY += 1; }
  const spanX = maxX - minX, spanY = maxY - minY;
  minX -= spanX * 0.08; maxX += spanX * 0.08;
  minY -= spanY * 0.08; maxY += spanY * 0.08;

  const w = 520, h = 260;
  const padL = 60, padR = 25, padT = 20, padB = 45;
  const pw = w - padL - padR, ph = h - padT - padB;
  const tx = x => padL + (x - minX) / (maxX - minX) * pw;
  const ty = y => padT + ph - (y - minY) / (maxY - minY) * ph;

  let grid = '';
  for (let i = 0; i <= 4; i++) {
    const gx = minX + i * (maxX - minX) / 4;
    const gy = minY + i * (maxY - minY) / 4;
    grid += `<line x1="${tx(gx)}" y1="${padT}" x2="${tx(gx)}" y2="${padT+ph}" stroke="#155e75" stroke-dasharray="2,2"/>`;
    grid += `<line x1="${padL}" y1="${ty(gy)}" x2="${padL+pw}" y2="${ty(gy)}" stroke="#155e75" stroke-dasharray="2,2"/>`;
    grid += `<text x="${tx(gx)}" y="${padT+ph+14}" fill="#7dd3fc" font-size="9" text-anchor="middle">${gx.toFixed(1)}</text>`;
    grid += `<text x="${padL-6}" y="${ty(gy)+3}" fill="#7dd3fc" font-size="9" text-anchor="end">${gy.toFixed(1)}</text>`;
  }

  let line = '';
  if (fitRes) {
    const x1 = minX, x2 = maxX;
    const y1 = fitRes.slope * x1 + fitRes.intercept;
    const y2 = fitRes.slope * x2 + fitRes.intercept;
    line = `<line x1="${tx(x1)}" y1="${ty(y1)}" x2="${tx(x2)}" y2="${ty(y2)}" stroke="#38bdf8" stroke-width="2.2"/>`;
  }

  const pts = rows.map(r => `<circle cx="${tx(r.x)}" cy="${ty(r.y)}" r="4.5" fill="#f43f5e" stroke="#ffffff" stroke-width="1.5"/>`).join('');

  plot.innerHTML = `
    <rect width="${w}" height="${h}" fill="#083344" rx="4"/>
    ${grid}
    ${line}
    ${pts}
    <text x="${padL + pw/2}" y="${h-8}" fill="#a5f3fc" font-size="10" font-weight="600" text-anchor="middle">${cfg.xAxis}</text>
    <text x="16" y="${padT + ph/2}" fill="#a5f3fc" font-size="10" font-weight="600" text-anchor="middle" transform="rotate(-90 16 ${padT + ph/2})">${cfg.yAxis}</text>
  `;

  if (fitBox && fitRes) {
    const est = model.estimate(cfg.slug, fitRes);
    fitBox.innerHTML = `
      <div style="font-size:12px;display:flex;flex-direction:column;gap:4px">
        <div><strong>Slope (m):</strong> ${fmt(fitRes.slope, 5)}</div>
        <div><strong>Intercept (b):</strong> ${fmt(fitRes.intercept, 5)}</div>
        <div><strong>Correlation R²:</strong> ${fitRes.r2.toFixed(6)}</div>
        <div><strong>Estimated ${cfg.targetName}:</strong> ${fmt(est.value * cfg.resultScale, cfg.resultDecimals)} ${cfg.resultUnit}</div>
        <div><strong>Standard Reference:</strong> ${fmt(est.reference * cfg.resultScale, cfg.resultDecimals)} ${cfg.resultUnit} (dev: ${est.errorPercent.toFixed(3)}%)</div>
      </div>
    `;
  }
}

// Mode Switcher Buttons
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

// Quiz evaluation
document.querySelectorAll('.quiz-option').forEach(btn => {
  btn.addEventListener('click', e => {
    const card = btn.closest('.quiz-card');
    const idx = +btn.dataset.idx;
    const qIdx = Array.from(document.querySelectorAll('.quiz-card')).indexOf(card);
    const qData = cfg.quiz[qIdx];
    card.querySelectorAll('.quiz-option').forEach(b => {
      b.disabled = true;
      b.classList.remove('correct', 'incorrect');
    });
    if (idx === qData.correct) {
      btn.classList.add('correct');
    } else {
      btn.classList.add('incorrect');
      const correctBtn = card.querySelector(`[data-idx="${qData.correct}"]`);
      if (correctBtn) correctBtn.classList.add('correct');
    }
    const fb = card.querySelector('.quiz-feedback');
    if (fb) fb.hidden = false;
  });
});

update();
renderTable();
renderPlot();
