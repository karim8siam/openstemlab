'use strict';
const cfg = JSON.parse(document.getElementById('labConfig').textContent);
const model = window.BasicMedicalModels;
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
  message('Adjust ' + cfg.shortInput + ', then execute preclinical measurement.');
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
  message('Initiating preclinical sensor acquisition and baseline tracking…');

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
      if ($('liveState')) $('liveState').textContent = 'Preclinical telemetry captured: ' + cfg.rawLabel + ' = ' + measurement.displayed.toFixed(cfg.rawDecimals) + ' ' + cfg.rawUnit + '.';
      message('Trial captured. Click "+ Record observation" to save to the notebook.');
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
  if (confirm('Clear all recorded medical science observations from your log?')) {
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
      fitBox.innerHTML = '<p>Log at least 3 distinct observations to compute regression fit and empirical preclinical parameter.</p>';
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
    grid += '<line x1="' + sx + '" y1="' + pad.top + '" x2="' + sx + '" y2="' + (pad.top + ph) + '" stroke="#4c0519" stroke-opacity="0.3" stroke-dasharray="2 3"/>';
    grid += '<line x1="' + pad.left + '" y1="' + sy + '" x2="' + (pad.left + pw) + '" y2="' + sy + '" stroke="#4c0519" stroke-opacity="0.3" stroke-dasharray="2 3"/>';
    grid += '<text x="' + sx + '" y="' + (pad.top + ph + 16) + '" font-size="9" fill="#fda4af" text-anchor="middle" font-family="monospace">' + fmt(gx, 1) + '</text>';
    grid += '<text x="' + (pad.left - 8) + '" y="' + (sy + 3) + '" font-size="9" fill="#fda4af" text-anchor="end" font-family="monospace">' + fmt(gy, 1) + '</text>';
  }

  let lineSvg = '';
  if (fitRes && rows.length >= 2) {
    const lx1 = minX, ly1 = fitRes.slope * lx1 + fitRes.intercept;
    const lx2 = maxX, ly2 = fitRes.slope * lx2 + fitRes.intercept;
    lineSvg = '<line x1="' + toSvgX(lx1) + '" y1="' + toSvgY(ly1) + '" x2="' + toSvgX(lx2) + '" y2="' + toSvgY(ly2) + '" stroke="#f43f5e" stroke-width="2.5"/>';
  }

  const pts = rows.map(r => {
    const cx = toSvgX(r.x * cfg.xScale);
    const cy = toSvgY(r.y * cfg.yScale);
    return '<circle cx="' + cx + '" cy="' + cy + '" r="5" fill="#be123c" stroke="#fff1f2" stroke-width="1.5"/>';
  }).join('');

  svg.innerHTML = '<rect width="' + W + '" height="' + H + '" fill="#1c0209"/>' +
                  grid +
                  lineSvg +
                  pts +
                  '<text x="' + (W / 2) + '" y="' + (H - 8) + '" fill="#fda4af" font-size="11" text-anchor="middle" font-weight="600">' + cfg.xAxis + '</text>' +
                  '<text x="14" y="' + (H / 2) + '" fill="#fda4af" font-size="11" text-anchor="middle" transform="rotate(-90 14 ' + (H / 2) + ')" font-weight="600">' + cfg.yAxis + '</text>';
}

function draw(offset=0) {
  const svg = $('visualSvg');
  if (!svg) return;
  const p = params();
  const num = cfg.num;
  const norm = Math.max(0, Math.min(1, (p.input - cfg.min) / (cfg.max - cfg.min || 1)));

  // Module 1: Hematology (Labs 1–7)
  if (num <= 7) {
    const liquidH = 30 + norm * 150 + offset * 3;
    const rbcY = 230 - liquidH;
    svg.innerHTML = `
      <rect width="520" height="280" fill="#1c0209"/>
      <g transform="translate(60, 20)">
        <rect x="70" y="20" width="30" height="220" rx="3" fill="#380613" stroke="#fda4af" stroke-width="2"/>
        <line x1="85" y1="20" x2="85" y2="240" stroke="#fda4af" stroke-opacity="0.3" stroke-dasharray="2 4"/>
        <rect x="72" y="22" width="26" height="216" fill="rgba(254, 205, 211, 0.25)"/>
        <rect x="72" y="${rbcY}" width="26" height="${liquidH}" fill="#e11d48" rx="2"/>
        ${[0, 50, 100, 150, 200].map(y => `
          <line x1="60" y1="${230 - y}" x2="70" y2="${230 - y}" stroke="#fda4af" stroke-width="1.5"/>
          <text x="52" y="${234 - y}" fill="#fda4af" font-size="9" text-anchor="end" font-family="monospace">${y}</text>
        `).join('')}
        <text x="85" y="255" fill="#fda4af" font-size="10" text-anchor="middle" font-weight="600">Pipette / Column</text>
      </g>
      <g transform="translate(240, 30)">
        <rect x="20" y="20" width="200" height="180" rx="8" fill="#2b040e" stroke="#be123c" stroke-width="2"/>
        <circle cx="120" cy="110" r="65" fill="#1c0209" stroke="#f43f5e" stroke-width="2"/>
        <path d="M 70 110 H 170 M 120 60 V 160 M 95 60 V 160 M 145 60 V 160 M 70 85 H 170 M 70 135 H 170" stroke="#fda4af" stroke-opacity="0.35" stroke-width="1"/>
        ${Array.from({length: Math.floor(12 + norm * 35)}).map((_, i) => {
          const cx = 80 + ((i * 23 + offset * 2) % 75);
          const cy = 80 + ((i * 37) % 75);
          return `<circle cx="${cx}" cy="${cy}" r="3.5" fill="#f43f5e" opacity="0.85"/>`;
        }).join('')}
        <text x="120" y="215" fill="#fff1f2" font-size="11" text-anchor="middle" font-weight="600">Cellular Field</text>
      </g>
    `;
  }
  // Module 2: Cardiovascular (Labs 8–14)
  else if (num <= 14) {
    svg.innerHTML = `
      <rect width="520" height="280" fill="#1c0209"/>
      <g transform="translate(20, 20)">
        <rect width="280" height="230" rx="8" fill="#140207" stroke="#be123c" stroke-width="2"/>
        ${Array.from({length: 10}).map((_, i) => `<line x1="${i*28+14}" y1="10" x2="${i*28+14}" y2="220" stroke="#4c0519" stroke-width="1"/>`).join('')}
        ${Array.from({length: 7}).map((_, i) => `<line x1="14" y1="${i*30+20}" x2="266" y2="${i*30+20}" stroke="#4c0519" stroke-width="1"/>`).join('')}
        <path d="M 20 125 L 60 125 Q 75 115 85 125 L 98 125 L 105 140 L 115 45 L 125 165 L 132 125 L 155 125 Q 180 ${125 - norm * 45 + offset * 4} 200 125 L 265 125"
              fill="none" stroke="#f43f5e" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        <text x="25" y="32" fill="#fda4af" font-size="10" font-family="monospace">HEMODYNAMICS TRACE</text>
        <circle cx="115" cy="45" r="4" fill="#fb7185"/>
      </g>
      <g transform="translate(325, 35)">
        <circle cx="85" cy="85" r="70" fill="#2b040e" stroke="#fda4af" stroke-width="3"/>
        <circle cx="85" cy="85" r="63" fill="#1c0209" stroke="#be123c" stroke-width="1"/>
        ${Array.from({length: 12}).map((_, i) => {
          const ang = -120 + i * 24;
          const rad = ang * Math.PI / 180;
          const x1 = 85 + 53 * Math.cos(rad);
          const y1 = 85 + 53 * Math.sin(rad);
          const x2 = 85 + 61 * Math.cos(rad);
          const y2 = 85 + 61 * Math.sin(rad);
          return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#fda4af" stroke-width="2"/>`;
        }).join('')}
        <line x1="85" y1="85"
              x2="${85 + 48 * Math.cos((-120 + norm * 240 + offset * 2) * Math.PI / 180)}"
              y2="${85 + 48 * Math.sin((-120 + norm * 240 + offset * 2) * Math.PI / 180)}"
              stroke="#e11d48" stroke-width="3" stroke-linecap="round"/>
        <circle cx="85" cy="85" r="5" fill="#fda4af"/>
        <text x="85" y="120" fill="#fff1f2" font-size="13" text-anchor="middle" font-weight="700" font-family="monospace">${fmt(p.input, 1)}</text>
        <text x="85" y="135" fill="#fda4af" font-size="9" text-anchor="middle">${cfg.inputUnit}</text>
      </g>
    `;
  }
  // Module 3: Neurophysiology & Sensory (Labs 15–21)
  else if (num <= 21) {
    const ampY = 140 - norm * 65 + offset * 5;
    svg.innerHTML = `
      <rect width="520" height="280" fill="#1c0209"/>
      <g transform="translate(25, 25)">
        <rect width="230" height="225" rx="8" fill="#2b040e" stroke="#be123c" stroke-width="2"/>
        <text x="18" y="28" fill="#fda4af" font-size="10" font-weight="600">STIMULUS &amp; CMAP</text>
        <line x1="25" y1="75" x2="205" y2="75" stroke="#fda4af" stroke-width="5" stroke-linecap="round"/>
        <line x1="25" y1="75" x2="${25 + norm * 180}" y2="75" stroke="#e11d48" stroke-width="5" stroke-linecap="round"/>
        <path d="M 25 175 L 80 175 L 90 160 L 105 ${ampY} L 125 ${ampY + 80} L 145 175 L 205 175"
              fill="none" stroke="#f43f5e" stroke-width="3" stroke-linejoin="round"/>
        <circle cx="105" cy="${ampY}" r="4" fill="#fb7185"/>
      </g>
      <g transform="translate(275, 25)">
        <rect width="220" height="225" rx="8" fill="#140207" stroke="#4c0519" stroke-width="2"/>
        <text x="18" y="28" fill="#fda4af" font-size="10" font-weight="600">THRESHOLD MATRIX</text>
        ${Array.from({length: 6}).map((_, i) => `<line x1="25" y1="${45 + i * 30}" x2="195" y2="${45 + i * 30}" stroke="#380613" stroke-width="1"/>`).join('')}
        ${Array.from({length: 6}).map((_, i) => `<line x1="${25 + i * 34}" y1="45" x2="${25 + i * 34}" y2="195" stroke="#380613" stroke-width="1"/>`).join('')}
        <polyline points="35,${170 - norm*35} 69,${150 - norm*45} 103,${110 - norm*25} 137,${90 - norm*35} 171,${70 - norm*45}"
                  fill="none" stroke="#be123c" stroke-width="2" stroke-dasharray="3 3"/>
        <circle cx="${25 + norm * 160}" cy="${45 + norm * 130 + offset * 3}" r="6" fill="#f43f5e"/>
      </g>
    `;
  }
  // Module 4: Pulmonary Mechanics (Labs 22–28)
  else if (num <= 28) {
    const lungH = 50 + norm * 110 + offset * 4;
    svg.innerHTML = `
      <rect width="520" height="280" fill="#1c0209"/>
      <g transform="translate(40, 25)">
        <rect x="25" y="20" width="85" height="190" rx="4" fill="#2b040e" stroke="#fda4af" stroke-width="2"/>
        <rect x="28" y="${208 - lungH}" width="79" height="${lungH}" fill="#e11d48" opacity="0.85" rx="3"/>
        <text x="67" y="232" fill="#fda4af" font-size="10" text-anchor="middle" font-weight="600">Spiro-Bell</text>
      </g>
      <g transform="translate(165, 25)">
        <rect width="320" height="205" rx="8" fill="#140207" stroke="#be123c" stroke-width="2"/>
        ${Array.from({length: 7}).map((_, i) => `<line x1="${i*45+20}" y1="15" x2="${i*45+20}" y2="190" stroke="#380613" stroke-width="1"/>`).join('')}
        ${Array.from({length: 5}).map((_, i) => `<line x1="20" y1="${i*40+20}" x2="300" y2="${i*40+20}" stroke="#380613" stroke-width="1"/>`).join('')}
        <path d="M 25 185 Q 55 60, 95 ${180 - norm * 120 + offset * 3} T 290 ${180 - norm * 135}"
              fill="none" stroke="#f43f5e" stroke-width="3" stroke-linecap="round"/>
        <line x1="95" y1="20" x2="95" y2="185" stroke="#fda4af" stroke-dasharray="2 3"/>
        <text x="100" y="32" fill="#fda4af" font-size="9" font-family="monospace">FEV1 Interval</text>
        <circle cx="95" cy="${180 - norm * 120 + offset * 3}" r="5" fill="#fb7185"/>
      </g>
    `;
  }
  // Module 5: Renal & Clinical Biochemistry (Labs 29–35)
  else if (num <= 35) {
    const colDensity = 0.2 + norm * 0.75;
    svg.innerHTML = `
      <rect width="520" height="280" fill="#1c0209"/>
      <g transform="translate(45, 30)">
        <rect x="20" y="20" width="60" height="170" rx="4" fill="#380613" stroke="#fda4af" stroke-width="2"/>
        <rect x="23" y="24" width="54" height="162" fill="#be123c" opacity="${colDensity}" rx="2"/>
        <line x1="-25" y1="105" x2="20" y2="105" stroke="#fbbf24" stroke-width="5"/>
        <polygon points="15,102 23,105 15,108" fill="#fbbf24"/>
        <line x1="80" y1="105" x2="125" y2="105" stroke="#fbbf24" stroke-width="${Math.max(1, 5 * (1 - colDensity * 0.8))}"/>
        <text x="50" y="210" fill="#fda4af" font-size="10" text-anchor="middle" font-weight="600">Sample Cuvette</text>
      </g>
      <g transform="translate(200, 30)">
        <rect width="280" height="180" rx="8" fill="#140207" stroke="#be123c" stroke-width="2"/>
        <text x="25" y="32" fill="#fda4af" font-size="10" font-weight="600">SPECTROPHOTOMETER</text>
        <rect x="25" y="50" width="230" height="60" rx="4" fill="#2b040e" stroke="#4c0519"/>
        <text x="140" y="92" fill="#fff1f2" font-size="24" text-anchor="middle" font-family="monospace" font-weight="700">${fmt(p.input * (cfg.refValue || 0.05), cfg.rawDecimals)}</text>
        <text x="140" y="135" fill="#fda4af" font-size="10" text-anchor="middle">Optical Transmittance / Absorbance</text>
        <circle cx="45" cy="155" r="4" fill="#10b981"/>
        <text x="58" y="159" fill="#a7f3d0" font-size="9">LINEAR ABSORPTIVITY CALIBRATED</text>
      </g>
    `;
  }
  // Module 6: Histopathology & Pharmacology (Labs 36–42)
  else {
    svg.innerHTML = `
      <rect width="520" height="280" fill="#1c0209"/>
      <g transform="translate(40, 25)">
        <rect width="200" height="215" rx="8" fill="#2b040e" stroke="#fda4af" stroke-width="2"/>
        <circle cx="100" cy="105" r="75" fill="#1c0209" stroke="#be123c" stroke-width="2"/>
        <path d="M 75 80 Q 100 ${65 + norm * 35 + offset * 3} 125 80 Q 135 115 125 135 Q 100 ${145 - norm * 20} 75 135 Z"
              fill="#e11d48" opacity="0.85" stroke="#fda4af" stroke-width="1.5"/>
        <text x="100" y="205" fill="#fda4af" font-size="10" text-anchor="middle" font-weight="600">Tissue / Organ Field</text>
      </g>
      <g transform="translate(270, 25)">
        <rect width="215" height="215" rx="8" fill="#140207" stroke="#be123c" stroke-width="2"/>
        <text x="18" y="28" fill="#fda4af" font-size="10" font-weight="600">DOSE-RESPONSE LOG</text>
        ${Array.from({length: 5}).map((_, i) => `<line x1="20" y1="${50 + i * 32}" x2="195" y2="${50 + i * 32}" stroke="#380613" stroke-width="1"/>`).join('')}
        <path d="M 25 180 Q 85 180 105 115 T 190 60" fill="none" stroke="#f43f5e" stroke-width="3"/>
        <circle cx="${25 + norm * 155}" cy="${180 - norm * 115 + offset * 3}" r="5" fill="#fb7185"/>
      </g>
    `;
  }
}

// Initial draw and table population
window.addEventListener('DOMContentLoaded', () => {
  update();
  renderTable();
});
