'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.MarineOceanModels;
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
  message('Adjust ' + cfg.shortInput + ', then execute oceanographic sampling assay.');
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
  const inputRatio = Math.max(0, Math.min(1, (p.input - cfg.min) / (cfg.max - cfg.min || 1.0)));

  let scene = '';
  if (currentSimMode === 'compare') {
    scene = `
      <rect x="20" y="20" width="225" height="240" fill="#082f49" rx="8" stroke="#0369a1" stroke-width="1.5"/>
      <rect x="275" y="20" width="225" height="240" fill="#082f49" rx="8" stroke="#0284c7" stroke-width="1.5"/>
      <text x="132" y="44" fill="#7dd3fc" font-size="11" font-weight="600" text-anchor="middle">IAPSO STANDARD SEAWATER</text>
      <text x="387" y="44" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="middle">OCEANOGRAPHIC WATER MASS</text>
      <!-- Reference Salinometer / Cuvette 1 -->
      <rect x="110" y="80" width="44" height="110" fill="#0c4a6e" rx="3" stroke="#0284c7" stroke-width="2"/>
      <rect x="114" y="110" width="36" height="76" fill="#38bdf8" opacity="0.3"/>
      <!-- Active Hydrographic Sample 2 -->
      <rect x="365" y="80" width="44" height="110" fill="#0c4a6e" rx="3" stroke="#38bdf8" stroke-width="2"/>
      <rect x="369" y="${190 - inputRatio * 80}" width="36" height="${inputRatio * 80}" fill="#0284c7" opacity="0.8"/>
      <text x="132" y="230" fill="#bae6fd" font-size="10" text-anchor="middle">Standard Salinity / Zero Blank</text>
      <text x="387" y="230" fill="#38bdf8" font-size="10" text-anchor="middle">${cfg.shortInput}: ${p.input.toFixed(cfg.inputDecimals)} ${cfg.inputUnit}</text>
    `;
  } else if (currentSimMode === 'sandbox') {
    scene = `
      <defs>
        <pattern id="marineGrid" width="20" height="20" patternUnits="userSpaceOnUse">
          <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#0c4a6e" stroke-width="0.8"/>
        </pattern>
      </defs>
      <rect x="20" y="20" width="480" height="240" fill="#031e30" rx="8"/>
      <rect x="20" y="20" width="480" height="240" fill="url(#marineGrid)" rx="8"/>
      <text x="260" y="45" fill="#38bdf8" font-size="12" font-weight="700" text-anchor="middle">OCEANIC WATER COLUMN &amp; HYDRODYNAMIC SANDBOX</text>
      <circle cx="${60 + inputRatio * 400}" cy="${220 - (inputRatio * 140)}" r="9" fill="#06b6d4" stroke="#ffffff" stroke-width="2"/>
      <line x1="60" y1="220" x2="460" y2="80" stroke="#0284c7" stroke-width="2" stroke-dasharray="5,3"/>
      <text x="260" y="240" fill="#7dd3fc" font-size="10" text-anchor="middle">Thermocline, Halocline &amp; Wave Energy Propagation Profile</text>
    `;
  } else {
    // Bench View
    const fillH = 20 + inputRatio * 100;
    scene = `
      <!-- Oceanographic Sampling Console -->
      <rect x="40" y="25" width="440" height="230" fill="#082f49" rx="8" stroke="#075985" stroke-width="2"/>
      <text x="60" y="50" fill="#38bdf8" font-size="12" font-weight="700">MARINE HYDROGRAPHIC WORKBENCH</text>
      <text x="60" y="66" fill="#bae6fd" font-size="10">${cfg.shortTitle}</text>

      <!-- CTD Rosette / Water Sampler Vessel -->
      <rect x="210" y="90" width="100" height="130" fill="#031e30" rx="6" stroke="#0284c7" stroke-width="2"/>
      <path d="M 230 190 L 230 130 L 250 110 L 270 110 L 290 130 L 290 190 Z" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.5"/>
      <rect x="235" y="${190 - fillH * 0.7}" width="50" height="${fillH * 0.7}" fill="#0284c7" opacity="0.85" rx="2"/>

      <!-- Digital Telemetry Screen -->
      <rect x="340" y="90" width="125" height="120" fill="#02131f" rx="4" stroke="#0369a1" stroke-width="1.5"/>
      <text x="352" y="112" fill="#7dd3fc" font-size="9" font-weight="600">OCEAN TELEMETRY</text>
      <text x="352" y="132" fill="#38bdf8" font-size="14" font-weight="700" font-family="monospace">${measurement ? fmt(measurement.raw, cfg.rawDecimals) : '---'}</text>
      <text x="352" y="148" fill="#94a3b8" font-size="9">${cfg.rawUnit}</text>
      <text x="352" y="176" fill="#64748b" font-size="8">SENSOR STATUS</text>
      <text x="352" y="192" fill="${measurement ? '#4ade80' : '#06b6d4'}" font-size="9" font-weight="600">${measurement ? 'CAPTURED' : 'STANDBY'}</text>

      <!-- Input Setpoint Readout -->
      <rect x="60" y="90" width="120" height="120" fill="#18181b" rx="4" stroke="#27272a"/>
      <text x="70" y="112" fill="#94a3b8" font-size="9">SETPOINT</text>
      <text x="70" y="132" fill="#38bdf8" font-size="13" font-weight="700" font-family="monospace">${p.input.toFixed(cfg.inputDecimals)}</text>
      <text x="70" y="146" fill="#64748b" font-size="9">${cfg.inputUnit}</text>
      <rect x="70" y="165" width="100" height="8" fill="#27272a" rx="2"/>
      <rect x="70" y="165" width="${inputRatio * 100}" height="8" fill="#0284c7" rx="2"/>
    `;
  }
  svg.innerHTML = scene;
}

if ($('measure')) $('measure').addEventListener('click', () => {
  if (busy) return;
  busy = true;
  $('measure').disabled = true;
  message('Executing marine hydrographic / spectrophotometric assay…');
  setTimeout(() => {
    const p = params();
    const pred = model.predict(cfg.slug, p.input);
    measurement = model.reading(cfg.slug, p.input, pred.raw);
    busy = false;
    $('measure').disabled = false;
    $('recordReading').disabled = false;
    if ($('readingValue')) $('readingValue').textContent = fmt(measurement.raw, cfg.rawDecimals) + ' ' + cfg.rawUnit;
    if ($('liveState')) $('liveState').textContent = 'Assay logged: ' + cfg.rawLabel + ' = ' + fmt(measurement.raw, cfg.rawDecimals) + ' ' + cfg.rawUnit + '.';
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
    plot.innerHTML = `<rect width="520" height="260" fill="#021a2c" rx="4"/><text x="260" y="135" fill="#38bdf8" font-size="12" text-anchor="middle">Record at least 2 observations to generate regression fit.</text>`;
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
    grid += `<line x1="${tx(gx)}" y1="${padT}" x2="${tx(gx)}" y2="${padT+ph}" stroke="#075985" stroke-dasharray="2,2"/>`;
    grid += `<line x1="${padL}" y1="${ty(gy)}" x2="${padL+pw}" y2="${ty(gy)}" stroke="#075985" stroke-dasharray="2,2"/>`;
    grid += `<text x="${tx(gx)}" y="${padT+ph+16}" font-size="9" fill="#7dd3fc" text-anchor="middle">${gx.toFixed(1)}</text>`;
    grid += `<text x="${padL-8}" y="${ty(gy)+3}" font-size="9" fill="#7dd3fc" text-anchor="end">${gy.toFixed(1)}</text>`;
  }

  const x1 = minX, x2 = maxX;
  const y1 = fitRes.slope * x1 + fitRes.intercept;
  const y2 = fitRes.slope * x2 + fitRes.intercept;
  const fitLine = `<line x1="${tx(x1)}" y1="${ty(y1)}" x2="${tx(x2)}" y2="${ty(y2)}" stroke="#38bdf8" stroke-width="2"/>`;

  let pts = '';
  rows.forEach(r => {
    pts += `<circle cx="${tx(r.x)}" cy="${ty(r.y)}" r="4" fill="#0284c7" stroke="#f0f9ff" stroke-width="1.5"/>`;
  });

  plot.innerHTML = `
    <rect width="${w}" height="${h}" fill="#021a2c" rx="4"/>
    ${grid}
    ${fitLine}
    ${pts}
    <text x="${padL + pw/2}" y="${h - 8}" fill="#7dd3fc" font-size="10" text-anchor="middle">${cfg.xAxis}</text>
    <text x="14" y="${padT + ph/2}" fill="#7dd3fc" font-size="10" text-anchor="middle" transform="rotate(-90 14 ${padT + ph/2})">${cfg.yAxis}</text>
  `;

  if (fitBox) {
    const est = model.estimate(cfg.slug, fitRes);
    const pct = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100.0;
    fitBox.innerHTML = `
      <p style="margin:0 0 6px 0;font-size:12px;color:#075985"><strong>Fitted slope (m):</strong> ${fmt(fitRes.slope, 6)}</p>
      <p style="margin:0 0 6px 0;font-size:12px;color:#075985"><strong>Fitted intercept (b):</strong> ${fmt(fitRes.intercept, 6)}</p>
      <p style="margin:0 0 6px 0;font-size:12px;color:#075985"><strong>R² correlation:</strong> ${fitRes.r2.toFixed(6)}</p>
      <p style="margin:6px 0 0 0;font-size:12px;color:#0284c7"><strong>Target ${cfg.target}:</strong> ${fmt(est.value, cfg.resultDecimals)} ${cfg.resultUnit} (Ref: ${fmt(est.reference, cfg.resultDecimals)}; dev: ${pct.toFixed(4)}%)</p>
    `;
  }
}

document.querySelectorAll('.sim-mode-btn').forEach(btn => {
  btn.addEventListener('click', e => {
    document.querySelectorAll('.sim-mode-btn').forEach(b => {
      b.classList.remove('active');
      b.setAttribute('aria-selected', 'false');
    });
    btn.classList.add('active');
    btn.setAttribute('aria-selected', 'true');
    currentSimMode = btn.getAttribute('data-mode');
    draw();
  });
});

document.querySelectorAll('.quiz-option').forEach(btn => {
  btn.addEventListener('click', e => {
    const card = btn.closest('.quiz-card');
    const fb = card.querySelector('.quiz-feedback');
    const idx = +btn.getAttribute('data-idx');
    const cardIdx = Array.from(card.parentNode.children).indexOf(card);
    const correctIdx = cfg.quiz[cardIdx].correct;
    card.querySelectorAll('.quiz-option').forEach(b => b.classList.remove('correct', 'wrong'));
    if (idx === correctIdx) {
      btn.classList.add('correct');
      fb.hidden = false;
      fb.textContent = '✓ Correct. ' + cfg.quiz[cardIdx].explanation;
    } else {
      btn.classList.add('wrong');
      fb.hidden = false;
      fb.textContent = '✗ Incorrect. ' + cfg.quiz[cardIdx].explanation;
    }
  });
});

update();
renderTable();
renderPlot();
