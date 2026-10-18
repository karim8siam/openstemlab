'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.PharmacyModels;
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
  message('Adjust ' + cfg.shortInput + ', then execute pharmaceutical assay.');
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
  const svg = $('pharmaSvg');
  if (!svg) return;
  const p = params();
  const ratio = Math.max(0, Math.min(1, (p.input - cfg.min) / (cfg.max - cfg.min || 1)));

  let html = `<defs>
    <linearGradient id="pharmaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ecfdf5"/>
      <stop offset="100%" stop-color="#a7f3d0"/>
    </linearGradient>
    <linearGradient id="pharmaLiquid" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#047857" stop-opacity="0.95"/>
    </linearGradient>
    <pattern id="pharmaGrid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e2e8f0" stroke-width="0.5"/>
    </pattern>
  </defs>
  <rect width="600" height="375" fill="#f8fafc"/>
  <rect width="600" height="375" fill="url(#pharmaGrid)"/>`;

  if (currentSimMode === 'bench') {
    // Standard laboratory bench visualization: cuvette / column / tablet press
    const liquidH = 60 + ratio * 120;
    const meniscusY = 280 - liquidH;
    html += `
      <!-- Analytical Cuvette / Dissolution Vessel Assembly -->
      <rect x="230" y="80" width="140" height="220" rx="8" fill="url(#pharmaGrad)" stroke="#059669" stroke-width="2.5"/>
      <rect x="238" y="${meniscusY}" width="124" height="${liquidH}" rx="4" fill="url(#pharmaLiquid)"/>
      <ellipse cx="300" cy="${meniscusY}" rx="62" ry="7" fill="#34d399" fill-opacity="0.7"/>

      <!-- Optical Path / Sensor Beam -->
      <line x1="80" y1="200" x2="230" y2="200" stroke="#f59e0b" stroke-width="3" stroke-dasharray="4 2"/>
      <line x1="370" y1="200" x2="520" y2="200" stroke="#f59e0b" stroke-width="3"/>
      <circle cx="80" cy="200" r="10" fill="#f59e0b"/>
      <rect x="510" y="180" width="40" height="40" rx="4" fill="#047857" stroke="#022c22"/>
      <text x="530" y="205" font-family="monospace" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">DET</text>

      <!-- Digital Sensor Telemetry Tag -->
      <rect x="200" y="30" width="200" height="34" rx="6" fill="#065f46" stroke="#047857"/>
      <text x="300" y="52" font-family="monospace" font-size="13" font-weight="bold" fill="#ffffff" text-anchor="middle">
        ${cfg.shortInput}: ${p.input.toFixed(cfg.inputDecimals)} ${cfg.inputUnit}
      </text>`;
  } else if (currentSimMode === 'compare') {
    // Comparative response overlay
    html += `
      <rect x="40" y="40" width="520" height="295" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
      <line x1="80" y1="290" x2="520" y2="290" stroke="#94a3b8" stroke-width="1.5"/>
      <line x1="80" y1="290" x2="80" y2="60" stroke="#94a3b8" stroke-width="1.5"/>
      <text x="300" y="325" font-family="sans-serif" font-size="11" fill="#475569" text-anchor="middle">${cfg.xAxis}</text>
      <text x="30" y="170" font-family="sans-serif" font-size="11" fill="#475569" text-anchor="middle" transform="rotate(-90 30 170)">${cfg.yAxis}</text>`;
    
    // Theoretical model line
    const y1 = 290 - 20;
    const y2 = 290 - 210;
    html += `<line x1="80" y1="${y1}" x2="500" y2="${y2}" stroke="#10b981" stroke-width="2.5" stroke-dasharray="6 3"/>`;

    // Plotted experimental points
    rows.forEach(r => {
      const rx = 80 + ((r.x - cfg.min) / (cfg.max - cfg.min || 1)) * 420;
      const ry = 290 - ((r.y - (cfg.emptyY || 0)) / (Math.abs(cfg.refValue * 1.5) || 1)) * 180;
      const clampedY = Math.max(70, Math.min(285, ry));
      html += `<circle cx="${rx}" cy="${clampedY}" r="4.5" fill="#047857" stroke="#ffffff" stroke-width="1.5"/>`;
    });
  } else if (currentSimMode === 'sandbox') {
    // Multi-parameter sandbox simulation view
    html += `
      <rect x="50" y="50" width="500" height="275" rx="8" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="2"/>
      <circle cx="300" cy="180" r="${40 + ratio * 60}" fill="#059669" fill-opacity="0.15" stroke="#059669" stroke-width="2" stroke-dasharray="5 3"/>
      <text x="300" y="140" font-family="sans-serif" font-size="14" font-weight="bold" fill="#065f46" text-anchor="middle">Pharmaceutical Sandbox Dynamics</text>
      <text x="300" y="170" font-family="monospace" font-size="12" fill="#047857" text-anchor="middle">Transfer Ratio: ${(ratio * 100).toFixed(1)}%</text>
      <text x="300" y="195" font-family="monospace" font-size="12" fill="#047857" text-anchor="middle">Equilibrium Response: ${fmt(p.input * (cfg.refValue || 1))} ${cfg.rawUnit}</text>`;
  }

  svg.innerHTML = html;
}

function renderTable() {
  const tbody = $('dataTableBody');
  if (!tbody) return;
  tbody.innerHTML = '';
  rows.forEach((r, idx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${idx + 1}</td>
      <td>${r.input.toFixed(cfg.inputDecimals)}</td>
      <td>${r.raw.toFixed(cfg.rawDecimals)}</td>
      <td><button class="btn-secondary" style="padding:2px 6px;font-size:10px" onclick="removeRow(${idx})">×</button></td>`;
    tbody.appendChild(tr);
  });

  const countBadge = $('observationCount');
  if (countBadge) countBadge.textContent = rows.length;

  // Run OLS Fit
  const fitRes = model.fit(rows);
  if (fitRes && $('fitEquation')) {
    $('fitEquation').textContent = `y = ${fmt(fitRes.slope)}x + ${fmt(fitRes.intercept)} (R² = ${fitRes.r2.toFixed(4)})`;
  }
  if (fitRes && $('derivedEstimate')) {
    const est = model.estimate(cfg.slug, fitRes);
    $('derivedEstimate').textContent = `${fmt(est.value, cfg.resultDecimals)} ${cfg.resultUnit} (Ref: ${fmt(est.reference, cfg.resultDecimals)})`;
  }
}

window.removeRow = function(idx) {
  rows.splice(idx, 1);
  try { localStorage.setItem('openstemlab-' + cfg.slug + '-v1', JSON.stringify(rows)); } catch(e) {}
  renderTable();
  draw();
};

if ($('measure')) {
  $('measure').addEventListener('click', () => {
    if (busy) return;
    busy = true;
    $('measure').disabled = true;
    message('Acquiring analytical telemetry...');

    setTimeout(() => {
      const p = params();
      const pred = model.predict(cfg.slug, p.input);
      measurement = { input: p.input, raw: pred.raw };
      if ($('readingValue')) $('readingValue').textContent = pred.raw.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit;
      if ($('recordReading')) $('recordReading').disabled = false;
      message('Analytical signal stabilized. Record observation.');
      busy = false;
      $('measure').disabled = false;
      draw();
    }, 250);
  });
}

if ($('recordReading')) {
  $('recordReading').addEventListener('click', () => {
    if (!measurement) return;
    const r = model.reading(cfg.slug, measurement.input, measurement.raw);
    rows.push(r);
    try { localStorage.setItem('openstemlab-' + cfg.slug + '-v1', JSON.stringify(rows)); } catch(e) {}
    renderTable();
    $('recordReading').disabled = true;
    message('Reading recorded to observation ledger.');
    draw();
  });
}

if ($('clearData')) {
  $('clearData').addEventListener('click', () => {
    rows = [];
    try { localStorage.removeItem('openstemlab-' + cfg.slug + '-v1'); } catch(e) {}
    renderTable();
    message('Observation records cleared.');
    draw();
  });
}

if ($('exportData')) {
  $('exportData').addEventListener('click', () => {
    if (!rows.length) return;
    let csv = `Run,${cfg.inputLabel} (${cfg.inputUnit}),${cfg.rawLabel} (${cfg.rawUnit})\n`;
    rows.forEach((r, idx) => {
      csv += `${idx + 1},${r.input},${r.raw}\n`;
    });
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${cfg.slug}-observations.csv`;
    a.click();
    URL.revokeObjectURL(url);
  });
}

document.querySelectorAll('.sim-mode-tab').forEach(tab => {
  tab.addEventListener('click', e => {
    document.querySelectorAll('.sim-mode-tab').forEach(t => t.classList.remove('active'));
    e.target.classList.add('active');
    currentSimMode = e.target.getAttribute('data-mode');
    draw();
  });
});

// Quiz interactive feedback
document.querySelectorAll('.quiz-opt').forEach(opt => {
  opt.addEventListener('click', e => {
    const card = e.target.closest('.quiz-card');
    const correctIdx = +card.getAttribute('data-correct');
    const chosenIdx = +e.target.getAttribute('data-idx');
    const fb = card.querySelector('.quiz-feedback');
    if (chosenIdx === correctIdx) {
      fb.className = 'quiz-feedback correct';
      fb.textContent = '✓ Correct: ' + card.getAttribute('data-expl');
    } else {
      fb.className = 'quiz-feedback incorrect';
      fb.textContent = '✗ Incorrect. Try again or review the theory section.';
    }
  });
});

update();
renderTable();
