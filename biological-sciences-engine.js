'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.BiologicalModels;
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
  message('Adjust ' + cfg.shortInput + ', then execute biological assay.');
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
  message('Initiating biological incubation, telemetry sampling and spectrophotometric scan…');

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
      if ($('liveState')) $('liveState').textContent = 'Biological assay completed: ' + cfg.rawLabel + ' = ' + measurement.displayed.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit + '.';
      message('Trial captured. Click "+ Record observation" to log data.');
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
  if (confirm('Clear all recorded biological observations from your log?')) {
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
      fitBox.innerHTML = '<p>Log at least 3 distinct observations to compute regression fit and empirical biological parameter.</p>';
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

  const spanX = maxX - minX || 1;
  const spanY = maxY - minY || 1;
  const toSvgX = x => pad.left + ((x - minX) / spanX) * pw;
  const toSvgY = y => (pad.top + ph) - ((y - minY) / spanY) * ph;

  let grid = '';
  for (let i = 0; i <= 5; i++) {
    const gx = minX + i * spanX / 5;
    const gy = minY + i * spanY / 5;
    const sx = toSvgX(gx);
    const sy = toSvgY(gy);
    grid += '<line x1="' + sx + '" y1="' + pad.top + '" x2="' + sx + '" y2="' + (pad.top + ph) + '" stroke="#064e3b" stroke-opacity="0.3" stroke-dasharray="2 3"/>';
    grid += '<line x1="' + pad.left + '" y1="' + sy + '" x2="' + (pad.left + pw) + '" y2="' + sy + '" stroke="#064e3b" stroke-opacity="0.3" stroke-dasharray="2 3"/>';
    grid += '<text x="' + sx + '" y="' + (pad.top + ph + 16) + '" font-size="9" fill="#a7f3d0" text-anchor="middle" font-family="monospace">' + fmt(gx, 1) + '</text>';
    grid += '<text x="' + (pad.left - 8) + '" y="' + (sy + 3) + '" font-size="9" fill="#a7f3d0" text-anchor="end" font-family="monospace">' + fmt(gy, 1) + '</text>';
  }

  let lineSvg = '';
  if (fitRes && rows.length >= 2) {
    const lx1 = minX, ly1 = fitRes.slope * lx1 + fitRes.intercept;
    const lx2 = maxX, ly2 = fitRes.slope * lx2 + fitRes.intercept;
    lineSvg = '<line x1="' + toSvgX(lx1) + '" y1="' + toSvgY(ly1) + '" x2="' + toSvgX(lx2) + '" y2="' + toSvgY(ly2) + '" stroke="#10b981" stroke-width="2.5"/>';
  }

  const pts = rows.map(r => {
    const cx = toSvgX(r.x * cfg.xScale);
    const cy = toSvgY(r.y * cfg.yScale);
    return '<circle cx="' + cx + '" cy="' + cy + '" r="5" fill="#059669" stroke="#ecfdf5" stroke-width="1.5"/>';
  }).join('');

  svg.innerHTML = '<rect width="' + W + '" height="' + H + '" fill="#022c22"/>' +
                  grid +
                  lineSvg +
                  pts +
                  '<text x="' + (W / 2) + '" y="' + (H - 8) + '" fill="#a7f3d0" font-size="11" text-anchor="middle" font-weight="600">' + cfg.xAxis + '</text>' +
                  '<text x="14" y="' + (H / 2) + '" fill="#a7f3d0" font-size="11" text-anchor="middle" transform="rotate(-90 14 ' + (H / 2) + ')" font-weight="600">' + cfg.yAxis + '</text>';
}

function draw(offset=0) {
  const svg = $('visualSvg');
  if (!svg) return;
  const p = params();
  const num = cfg.num;
  const norm = Math.max(0, Math.min(1, (p.input - cfg.min) / (cfg.max - cfg.min || 1)));

  // Module 1: Cell Biology (Labs 1–6)
  if (num <= 6) {
    svg.innerHTML = `
      <rect width="520" height="280" fill="#022c22"/>
      <g transform="translate(40, 20)">
        <rect width="210" height="230" rx="8" fill="#064e3b" stroke="#34d399" stroke-width="2"/>
        <circle cx="105" cy="115" r="75" fill="#011b15" stroke="#10b981" stroke-width="2"/>
        <!-- Onion / Epidermal Plant Cells -->
        <path d="M 45 80 Q 105 70 165 80 L 165 115 Q 105 105 45 115 Z" fill="#047857" opacity="0.85" stroke="#a7f3d0"/>
        <path d="M 45 115 Q 105 105 165 115 L 165 150 Q 105 140 45 150 Z" fill="#047857" opacity="0.85" stroke="#a7f3d0"/>
        <!-- Plasmolyzed / Turgid Protoplast -->
        <ellipse cx="105" cy="98" rx="${45 - norm * 15 + offset * 2}" ry="${12 - norm * 4}" fill="#10b981" opacity="0.9"/>
        <ellipse cx="105" cy="133" rx="${45 - norm * 15 + offset * 2}" ry="${12 - norm * 4}" fill="#10b981" opacity="0.9"/>
        <circle cx="105" cy="98" r="3" fill="#ecfdf5"/>
        <circle cx="105" cy="133" r="3" fill="#ecfdf5"/>
        <text x="105" y="215" fill="#a7f3d0" font-size="10" text-anchor="middle" font-weight="600">Cellular Micrometry Field</text>
      </g>
      <g transform="translate(280, 20)">
        <rect width="200" height="230" rx="8" fill="#011b15" stroke="#047857" stroke-width="2"/>
        <text x="20" y="30" fill="#6ee7b7" font-size="10" font-weight="600">MEMBRANE POTENTIAL / FLUX</text>
        <rect x="25" y="45" width="150" height="150" rx="4" fill="#064e3b" stroke="#10b981"/>
        <line x1="100" y1="45" x2="100" y2="195" stroke="#a7f3d0" stroke-dasharray="3 3" stroke-width="2"/>
        <text x="60" y="70" fill="#a7f3d0" font-size="9">SOLUTE</text>
        <text x="140" y="70" fill="#a7f3d0" font-size="9">SOLVENT</text>
        ${Array.from({length: Math.floor(8 + norm * 24)}).map((_, i) => {
          const cx = 35 + ((i * 29 + offset * 3) % 55);
          const cy = 80 + ((i * 37) % 100);
          return `<circle cx="${cx}" cy="${cy}" r="3" fill="#fbbf24"/>`;
        }).join('')}
        ${Array.from({length: Math.floor(25 - norm * 12)}).map((_, i) => {
          const cx = 110 + ((i * 23 + offset * 2) % 55);
          const cy = 80 + ((i * 31) % 100);
          return `<circle cx="${cx}" cy="${cy}" r="2" fill="#38bdf8"/>`;
        }).join('')}
      </g>
    `;
  }
  // Module 2: Enzymology & Respiration (Labs 7–12)
  else if (num <= 12) {
    const colH = 40 + norm * 130 + offset * 4;
    svg.innerHTML = `
      <rect width="520" height="280" fill="#022c22"/>
      <g transform="translate(40, 25)">
        <rect width="190" height="225" rx="8" fill="#064e3b" stroke="#34d399" stroke-width="2"/>
        <!-- Respirometer / Reaction Flask -->
        <path d="M 75 40 L 75 70 L 45 180 Q 45 195 95 195 Q 145 195 145 180 L 115 70 L 115 40 Z" fill="#011b15" stroke="#10b981" stroke-width="2"/>
        <rect x="52" y="${190 - colH}" width="86" height="${colH}" fill="#10b981" opacity="0.75" rx="4"/>
        ${Array.from({length: 8}).map((_, i) => {
          const bx = 65 + ((i * 21 + offset * 4) % 60);
          const by = 180 - ((i * 23 + offset * 6) % Math.max(10, colH));
          return `<circle cx="${bx}" cy="${by}" r="2.5" fill="#ecfdf5" opacity="0.8"/>`;
        }).join('')}
        <text x="95" y="215" fill="#a7f3d0" font-size="10" text-anchor="middle" font-weight="600">Enzyme Digestion Vessel</text>
      </g>
      <g transform="translate(260, 25)">
        <rect width="220" height="225" rx="8" fill="#011b15" stroke="#047857" stroke-width="2"/>
        <text x="20" y="30" fill="#6ee7b7" font-size="10" font-weight="600">GAS EVOLUTION MANOMETER</text>
        <rect x="35" y="50" width="20" height="150" rx="3" fill="#064e3b" stroke="#10b981"/>
        <rect x="37" y="${198 - colH * 0.9}" width="16" height="${colH * 0.9}" fill="#34d399" rx="2"/>
        ${[0, 30, 60, 90, 120].map(y => `<line x1="30" y1="${190-y}" x2="35" y2="${190-y}" stroke="#a7f3d0"/>`).join('')}
        <text x="80" y="110" fill="#ecfdf5" font-size="16" font-family="monospace" font-weight="700">${fmt(p.input * (cfg.refValue || 0.1), cfg.rawDecimals)}</text>
        <text x="80" y="130" fill="#a7f3d0" font-size="10">${cfg.rawUnit}</text>
      </g>
    `;
  }
  // Module 3: Molecular Genetics (Labs 13–18)
  else if (num <= 18) {
    const bandPos = 60 + norm * 120 + offset * 3;
    svg.innerHTML = `
      <rect width="520" height="280" fill="#022c22"/>
      <g transform="translate(30, 25)">
        <rect width="230" height="225" rx="8" fill="#011b15" stroke="#34d399" stroke-width="2"/>
        <text x="20" y="30" fill="#6ee7b7" font-size="10" font-weight="600">AGAROSE GEL ELECTROPHORESIS</text>
        <!-- Wells -->
        <rect x="35" y="45" width="25" height="8" rx="2" fill="#064e3b" stroke="#a7f3d0"/>
        <rect x="75" y="45" width="25" height="8" rx="2" fill="#064e3b" stroke="#a7f3d0"/>
        <rect x="115" y="45" width="25" height="8" rx="2" fill="#064e3b" stroke="#a7f3d0"/>
        <rect x="155" y="45" width="25" height="8" rx="2" fill="#064e3b" stroke="#a7f3d0"/>
        <!-- DNA Bands -->
        <rect x="37" y="70" width="21" height="4" rx="1" fill="#38bdf8" opacity="0.9"/>
        <rect x="37" y="110" width="21" height="4" rx="1" fill="#38bdf8" opacity="0.9"/>
        <rect x="37" y="160" width="21" height="4" rx="1" fill="#38bdf8" opacity="0.9"/>
        <rect x="77" y="${bandPos}" width="21" height="4" rx="1" fill="#10b981" opacity="0.95"/>
        <text x="105" y="${bandPos + 4}" fill="#ecfdf5" font-size="8" font-family="monospace">Target Amplicon</text>
      </g>
      <g transform="translate(280, 25)">
        <rect width="210" height="225" rx="8" fill="#064e3b" stroke="#047857" stroke-width="2"/>
        <text x="20" y="30" fill="#a7f3d0" font-size="10" font-weight="600">DNA UV ABSORBANCE PEAK</text>
        <!-- Spectrum curve with peak at 260nm -->
        <path d="M 25 180 Q 75 180 105 ${175 - norm * 120} T 185 180" fill="none" stroke="#10b981" stroke-width="3"/>
        <line x1="105" y1="30" x2="105" y2="190" stroke="#a7f3d0" stroke-dasharray="2 3"/>
        <text x="110" y="45" fill="#a7f3d0" font-size="9" font-family="monospace">260 nm</text>
        <circle cx="105" cy="${175 - norm * 120}" r="5" fill="#ecfdf5"/>
      </g>
    `;
  }
  // Module 4: Microbiology (Labs 19–24)
  else if (num <= 24) {
    const colDensity = Math.floor(15 + norm * 50);
    svg.innerHTML = `
      <rect width="520" height="280" fill="#022c22"/>
      <g transform="translate(40, 25)">
        <rect width="200" height="225" rx="8" fill="#064e3b" stroke="#34d399" stroke-width="2"/>
        <circle cx="100" cy="110" r="75" fill="#011b15" stroke="#10b981" stroke-width="2"/>
        <!-- Agar surface -->
        <circle cx="100" cy="110" r="68" fill="#047857" opacity="0.6"/>
        <!-- Colonies / Plaques -->
        ${Array.from({length: colDensity}).map((_, i) => {
          const cx = 55 + ((i * 31 + offset * 3) % 90);
          const cy = 65 + ((i * 47) % 90);
          return `<circle cx="${cx}" cy="${cy}" r="2.5" fill="#ecfdf5" opacity="0.9"/>`;
        }).join('')}
        <text x="100" y="210" fill="#a7f3d0" font-size="10" text-anchor="middle" font-weight="600">Petri Plate CFU / Lawn</text>
      </g>
      <g transform="translate(270, 25)">
        <rect width="210" height="225" rx="8" fill="#011b15" stroke="#047857" stroke-width="2"/>
        <text x="20" y="30" fill="#6ee7b7" font-size="10" font-weight="600">TURBIDITY OD600 SCAN</text>
        <!-- Spectrophotometer cuvette in beam -->
        <rect x="35" y="60" width="50" height="120" rx="3" fill="#064e3b" stroke="#34d399"/>
        <rect x="37" y="65" width="46" height="110" fill="#10b981" opacity="${0.2 + norm * 0.75}"/>
        <line x1="-10" y1="110" x2="35" y2="110" stroke="#fbbf24" stroke-width="5"/>
        <line x1="85" y1="110" x2="130" y2="110" stroke="#fbbf24" stroke-width="${Math.max(1, 5 * (1 - norm * 0.75))}"/>
        <text x="120" y="160" fill="#ecfdf5" font-size="18" font-family="monospace" font-weight="700">${fmt(p.input * (cfg.refValue || 0.05), cfg.rawDecimals)}</text>
      </g>
    `;
  }
  // Module 5: Plant Physiology & Ecology (Labs 25–30)
  else {
    const leafRate = 20 + norm * 140 + offset * 3;
    svg.innerHTML = `
      <rect width="520" height="280" fill="#022c22"/>
      <g transform="translate(40, 25)">
        <rect width="210" height="225" rx="8" fill="#064e3b" stroke="#34d399" stroke-width="2"/>
        <!-- Leaf Chamber / Potometer -->
        <path d="M 60 140 Q 105 50 150 140 Q 105 160 60 140 Z" fill="#10b981" opacity="0.9" stroke="#ecfdf5" stroke-width="1.5"/>
        <line x1="105" y1="150" x2="105" y2="80" stroke="#047857" stroke-width="2"/>
        <!-- Stomatal Pores -->
        ${[0, 1, 2, 3].map(i => `<ellipse cx="${85 + i * 14}" cy="${115 + (i%2)*10}" rx="${3 + norm * 2}" ry="1.5" fill="#011b15"/>`).join('')}
        <text x="105" y="210" fill="#a7f3d0" font-size="10" text-anchor="middle" font-weight="600">Leaf Boundary Layer</text>
      </g>
      <g transform="translate(280, 25)">
        <rect width="200" height="225" rx="8" fill="#011b15" stroke="#047857" stroke-width="2"/>
        <text x="20" y="30" fill="#6ee7b7" font-size="10" font-weight="600">GAS EXCHANGE FLUX</text>
        <path d="M 25 180 Q 70 180 110 ${180 - leafRate} T 180 ${175 - leafRate}" fill="none" stroke="#34d399" stroke-width="3"/>
        <circle cx="110" cy="${180 - leafRate}" r="5" fill="#ecfdf5"/>
        <text x="100" y="160" fill="#a7f3d0" font-size="10" font-family="monospace">Flux: ${fmt(p.input, 1)} ${cfg.inputUnit}</text>
      </g>
    `;
  }
}

window.addEventListener('DOMContentLoaded', () => {
  update();
  renderTable();
});
