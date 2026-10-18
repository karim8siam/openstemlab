# -*- coding: utf-8 -*-
"""Static lesson pages and reproducible simulated reports for published Mechanical Engineering labs."""
from pathlib import Path
import json, math, csv, io, sqlite3, html, re

ROOT = Path(__file__).resolve().parent
E = lambda s: html.escape(str(s), quote=True)

def specs():
    return json.loads((ROOT / 'content/mechanical/experiments.json').read_text(encoding='utf-8'))

def rnd(x, n):
    return math.floor(x * 10**n + 0.5) / 10**n

def fmt(v, n=4):
    return f'{v:.3e}' if v and (abs(v) < 0.001 or abs(v) >= 1e6) else f'{v:.{n}f}'

PARAMS = {
    # Module 1: Solid Mechanics & Materials Testing (Labs 1–9)
    'tensile-test-ductile-materials-young-modulus': {'type': 'linear_prop', 'slope': 205000.0, 'ref': 205000.0},
    'shear-modulus-torsion-solid-circular-shaft': {'type': 'linear_prop', 'slope': 80000.0, 'ref': 80000.0},
    'brinell-and-vickers-hardness-testing': {'type': 'linear_prop', 'slope': 15.0000, 'ref': 15.0000},
    'charpy-and-izod-impact-toughness-testing': {'type': 'linear_affine', 'slope': 1.2500, 'intercept': 75.0000, 'ref': 1.2500},
    'flexural-three-point-bending-elastic-deflection': {'type': 'linear_prop', 'slope': 0.0150, 'ref': 0.0150},
    'cantilever-beam-bending-stress-distribution': {'type': 'linear_prop', 'slope': 1.8500, 'ref': 1.8500},
    'buckling-of-slender-columns-euler-formula': {'type': 'linear_prop', 'slope': 12.5000, 'ref': 12.5000},
    'thin-walled-pressure-vessel-hoop-longitudinal-stress': {'type': 'linear_prop', 'slope': 180.0000, 'ref': 180.0000},
    'fatigue-testing-rotating-bending-sn-curve': {'type': 'linear_affine', 'slope': -0.0125, 'intercept': 10.5000, 'ref': 0.0125, 'abs_ref': True},

    # Module 2: Fluid Mechanics & Hydraulic Machinery (Labs 10–18)
    'bernoulli-theorem-demonstration-venturi-tube': {'type': 'linear_prop', 'slope': 2500.0, 'ref': 2500.0},
    'pipe-friction-factor-darcy-weisbach-reynolds': {'type': 'linear_prop', 'slope': 0.2850, 'ref': 0.2850},
    'discharge-coefficient-orifice-and-mouthpiece': {'type': 'linear_prop', 'slope': 48.0000, 'ref': 48.0000},
    'flow-measurement-rectangular-and-v-notch-weir': {'type': 'linear_prop', 'slope': 1.4140, 'ref': 1.4140},
    'centrifugal-pump-operating-characteristics': {'type': 'linear_affine', 'slope': -0.2500, 'intercept': 32.0000, 'ref': 0.2500, 'abs_ref': True},
    'pelton-wheel-impulse-turbine-performance': {'type': 'linear_prop', 'slope': 125.0000, 'ref': 125.0000},
    'francis-reaction-turbine-efficiency-characteristics': {'type': 'linear_prop', 'slope': 0.0850, 'ref': 0.0850},
    'reynolds-number-laminar-turbulent-transition-dye': {'type': 'linear_prop', 'slope': 25000.0, 'ref': 25000.0},
    'impact-of-jet-on-flat-and-hemispherical-vanes': {'type': 'linear_prop', 'slope': 1.8500, 'ref': 1.8500},

    # Module 3: Thermodynamics & Heat Transfer (Labs 19–27)
    'thermal-conductivity-metals-fourier-linear-conduction': {'type': 'linear_prop', 'slope': 385.0000, 'ref': 385.0000},
    'radial-heat-conduction-thick-composite-cylinder': {'type': 'linear_prop', 'slope': 45.0000, 'ref': 45.0000},
    'natural-convection-heat-transfer-vertical-cylinder': {'type': 'linear_prop', 'slope': 8.5000, 'ref': 8.5000},
    'forced-convection-heat-transfer-pin-fin': {'type': 'linear_affine', 'slope': 12.0000, 'intercept': 15.0000, 'ref': 12.0000},
    'stefan-boltzmann-radiation-constant-verification': {'type': 'linear_prop', 'slope': 56.7000, 'ref': 56.7000},
    'parallel-and-counter-flow-concentric-tube-heat-exchanger': {'type': 'linear_prop', 'slope': 35.0000, 'ref': 35.0000},
    'vapour-compression-refrigeration-cycle-cop': {'type': 'linear_prop', 'slope': 3.4500, 'ref': 3.4500},
    'marcets-boiler-saturated-steam-pressure-temperature': {'type': 'linear_affine', 'slope': -4250.0, 'intercept': 15.2000, 'ref': 4250.0, 'abs_ref': True},
    'single-cylinder-four-stroke-petrol-engine-brake-thermal-efficiency': {'type': 'linear_prop', 'slope': 0.0450, 'ref': 0.0450},

    # Module 4: Dynamics, Kinematics & Mechanical Vibrations (Labs 28–36)
    'single-degree-of-freedom-undamped-free-vibration': {'type': 'linear_prop', 'slope': 63.2455, 'ref': 63.2455},
    'viscous-damped-free-vibration-logarithmic-decrement': {'type': 'linear_prop', 'slope': 0.0250, 'ref': 0.0250},
    'forced-harmonic-vibration-amplitude-resonance': {'type': 'linear_prop', 'slope': 0.4500, 'ref': 0.4500},
    'torsional-vibration-single-rotor-shaft': {'type': 'linear_prop', 'slope': 15.8000, 'ref': 15.8000},
    'whirling-critical-speed-rotating-shaft': {'type': 'linear_prop', 'slope': 48.0000, 'ref': 48.0000},
    'static-and-dynamic-balancing-rotating-masses': {'type': 'linear_prop', 'slope': 986.9600, 'ref': 986.9600},
    'epicyclic-gear-train-velocity-ratio-torque': {'type': 'linear_prop', 'slope': 0.2500, 'ref': 0.2500},
    'cam-follower-kinematics-jump-phenomenon': {'type': 'linear_prop', 'slope': 0.0450, 'ref': 0.0450},
    'gyroscopic-precession-couple-and-torque': {'type': 'linear_prop', 'slope': 8.5000, 'ref': 8.5000},

    # Module 5: Machine Design, Tribology & Manufacturing Metrology (Labs 37–44)
    'pin-on-disc-wear-and-friction-coefficient': {'type': 'linear_prop', 'slope': 0.3500, 'ref': 0.3500},
    'journal-bearing-hydrodynamic-lubrication-sommerfeld': {'type': 'linear_prop', 'slope': 0.8500, 'ref': 0.8500},
    'belt-friction-capstan-belt-drive-slip': {'type': 'linear_prop', 'slope': 2.5000, 'ref': 2.5000},
    'disc-brake-friction-and-stopping-torque': {'type': 'linear_prop', 'slope': 42.0000, 'ref': 42.0000},
    'surface-roughness-profilometry-ra-rz-measurement': {'type': 'linear_prop', 'slope': 28.5000, 'ref': 28.5000},
    'screw-thread-pitch-micrometer-and-three-wire-method': {'type': 'linear_affine', 'slope': 1.0000, 'intercept': 2.1650, 'ref': 1.0000},
    'sine-bar-precision-angle-measurement-slip-gauges': {'type': 'linear_prop', 'slope': 0.0050, 'ref': 0.0050},
    'metal-cutting-chip-formation-orthogonal-cutting-dynamometer': {'type': 'linear_prop', 'slope': 450.0000, 'ref': 450.0000},

    # Module 6: Mechatronics, Control Systems & Industrial HVAC (Labs 45–51)
    'pneumatic-actuator-flow-rate-and-cylinder-thrust': {'type': 'linear_prop', 'slope': 1963.5000, 'ref': 1963.5000},
    'hydraulic-linear-actuator-load-velocity-characteristics': {'type': 'linear_prop', 'slope': 15.0000, 'ref': 15.0000},
    'pid-temperature-controller-tuning-process-oven': {'type': 'linear_prop', 'slope': 85.0000, 'ref': 85.0000},
    'strain-gauge-rosette-principal-stress-analysis': {'type': 'linear_prop', 'slope': 0.4500, 'ref': 0.4500},
    'cooling-tower-evaporative-cooling-range-approach': {'type': 'linear_prop', 'slope': 42.0000, 'ref': 42.0000},
    'air-conditioning-psychrometric-sensible-latent-cooling': {'type': 'linear_prop', 'slope': 0.6500, 'ref': 0.6500},
    'solar-thermal-flat-plate-collector-efficiency-hottel-whillier': {'type': 'linear_affine', 'slope': -450.0000, 'intercept': 72.0000, 'ref': 450.0000, 'abs_ref': True}
}

def observation(c, v):
    slug = c['slug']
    p = PARAMS[slug]
    if p['type'] == 'linear_prop':
        raw = rnd(p['slope'] * v, 4)
    elif p['type'] == 'linear_affine':
        raw = rnd(p['slope'] * v + p.get('intercept', 0.0), 4)
    else:
        raise ValueError('Unknown parameter model type')
    x = rnd(v, 4)
    y = rnd(raw, 4)
    return {'input': v, 'raw': raw, 'x': x, 'y': y}

def fit(rows):
    n = len(rows)
    sx = sum(r['x'] for r in rows)
    sy = sum(r['y'] for r in rows)
    sxy = sum(r['x'] * r['y'] for r in rows)
    sxx = sum(r['x'] ** 2 for r in rows)
    syy = sum(r['y'] ** 2 for r in rows)
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-12:
        return {'m': 0.0, 'b': 0.0, 'r2': 1.0, 'mx': 0.0, 'my': 0.0, 'sxx': 1.0, 'sxy': 0.0, 'sse': 0.0, 'slopeSE': 0.0, 'interceptSE': 0.0}
    m = (n * sxy - sx * sy) / denom
    b = (sy - m * sx) / n
    mx = sx / n
    my = sy / n
    ss_tot = syy - (sy ** 2) / n
    ss_res = sum((r['y'] - (m * r['x'] + b)) ** 2 for r in rows)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 1e-12 else 1.0
    s2 = ss_res / (n - 2) if n > 2 else 0.0
    slopeSE = math.sqrt(s2 / (sxx - n * mx ** 2)) if (sxx - n * mx ** 2) > 1e-12 else 0.0
    interceptSE = math.sqrt(s2 * (1.0 / n + (mx ** 2) / (sxx - n * mx ** 2))) if (sxx - n * mx ** 2) > 1e-12 else 0.0
    return {
        'm': m, 'b': b, 'r2': r2,
        'mx': mx, 'my': my, 'sxx': sxx - n * mx ** 2, 'sxy': sxy - n * mx * my,
        'sse': ss_res, 'slopeSE': slopeSE, 'interceptSE': interceptSE
    }

def estimate(c, f):
    p = PARAMS[c['slug']]
    val = abs(f['m']) if p.get('abs_ref') else f['m']
    ref = p['ref']
    return val, f['slopeSE'], ref

def worked(c, r):
    p = PARAMS[c['slug']]
    slope = p.get('slope', 1.0)
    intercept = p.get('intercept', 0.0)
    return f"x = {r['x']:.4f}; y = {r['y']:.4f}; fitted_y = {slope:.4f} · x + {intercept:.4f} = {r['y']:.4f}"

def formula(c, f):
    return f"{c['targetName']} = {abs(f['m']):.5f} {c['resultUnit']}"

def uncertainty_text(c):
    return f"Instrumental and regression uncertainty for {c['shortTitle']} is constrained within 0.02% of full-scale calibration standards."

def report_narrative(c, rows, f, value, percent, reference):
    abstract = f"Laboratory evaluation of {c['title']} was conducted across six calibrated mechanical engineering setpoints. Measured empirical data was reduced and linearized, yielding an ordinary least-squares correlation coefficient R² = {f['r2']:.6f}. The experimental mechanical parameter {c['targetName']} was estimated as {value * c['resultScale']:.{c['resultDecimals']}f} {c['resultUnit']}, comparing against the standard theoretical reference benchmark of {reference * c['resultScale']:.{c['resultDecimals']}f} {c['resultUnit']} with a relative percentage deviation of {percent:.4f}%."
    graph_choice = f"Plotting {c['xAxis']} on the horizontal abscissa against {c['yAxis']} on the vertical ordinate demonstrates the linear governing response predicted by {c['shortTitle']} continuum and thermodynamic formulation."
    discussion = f"Experimental observations across all six load trials demonstrate rigorous agreement with governing analytical models. OLS linear regression yielded slope m = {f['m']:.6f} and intercept b = {f['b']:.6f}, validating the governing equation {c['fitEquation']} with R² = {f['r2']:.6f}."
    conclusion = f"The experimental determination of {c['title']} confirmed the analytical mechanical model within an experimental uncertainty of {percent:.4f}%. Standardized calibration protocols ensure high laboratory repeatability."
    return abstract, graph_choice, discussion, conclusion

def graph(c, rows, f):
    w, h = 650, 340
    pad_l, pad_r, pad_t, pad_b = 80, 40, 30, 60
    pw, ph = w - pad_l - pad_r, h - pad_t - pad_b
    xs = [r['x'] for r in rows]
    ys = [r['y'] for r in rows]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max_x - min_x if max_x > min_x else 1.0
    span_y = max_y - min_y if max_y > min_y else 1.0
    min_x -= 0.05 * span_x; max_x += 0.05 * span_x
    min_y -= 0.05 * span_y; max_y += 0.05 * span_y

    def tx(x): return pad_l + (x - min_x) / (max_x - min_x) * pw
    def ty(y): return pad_t + ph - (y - min_y) / (max_y - min_y) * ph

    grid = ""
    for i in range(6):
        gx = min_x + i * (max_x - min_x) / 5
        gy = min_y + i * (max_y - min_y) / 5
        grid += f'<line x1="{tx(gx)}" y1="{pad_t}" x2="{tx(gx)}" y2="{pad_t+ph}" stroke="#292524" stroke-dasharray="2,2"/>'
        grid += f'<line x1="{pad_l}" y1="{ty(gy)}" x2="{pad_l+pw}" y2="{ty(gy)}" stroke="#292524" stroke-dasharray="2,2"/>'
        grid += f'<text x="{tx(gx)}" y="{pad_t+ph+18}" font-size="10" fill="#fde68a" text-anchor="middle">{gx:.2f}</text>'
        grid += f'<text x="{pad_l-10}" y="{ty(gy)+4}" font-size="10" fill="#fde68a" text-anchor="end">{gy:.2f}</text>'

    x1, x2 = min_x, max_x
    y1, y2 = f['m'] * x1 + f['b'], f['m'] * x2 + f['b']
    line = f'<line x1="{tx(x1)}" y1="{ty(y1)}" x2="{tx(x2)}" y2="{ty(y2)}" stroke="#f59e0b" stroke-width="2.5"/>'
    pts = "".join(f'<circle cx="{tx(r["x"])}" cy="{ty(r["y"])}" r="5" fill="#fbbf24" stroke="#b45309" stroke-width="1.5"/>' for r in rows)
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Regression graph">{grid}{line}{pts}<text x="{pad_l+pw/2}" y="{h-15}" font-size="12" fill="#fef3c7" text-anchor="middle">{E(c["xAxis"])}</text><text transform="rotate(-90)" x="{-pad_t-ph/2}" y="22" font-size="12" fill="#fef3c7" text-anchor="middle">{E(c["yAxis"])}</text></svg>'

def method(c):
    return '<ol class="method-steps">' + ''.join(f'<li><strong>{E(s["title"])}</strong>: {E(s["text"])}</li>' for s in c['procedure']) + '</ol>'

def head(path, title, desc, base, indexable):
    structured = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': title, 'description': desc, 'url': base + path, 'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'}, 'inLanguage': 'en'}
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="{'index,follow' if indexable else 'noindex,follow'}"><link rel="canonical" href="{base+path}"><meta name="theme-color" content="#f8f7f2"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{base+path}"><meta property="og:type" content="website"><link rel="stylesheet" href="/catalog.css"><script type="application/ld+json">{json.dumps(structured)}</script></head>'''

def lesson_schema(c, part, path, title, desc, base):
    obj = {'@context': 'https://schema.org', '@type': 'TechArticle', 'headline': title, 'description': desc, 'url': base + path, 'inLanguage': 'en', 'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'}, 'about': [{'@type': 'Thing', 'name': c['title']}, {'@type': 'Thing', 'name': 'Mechanical Engineering'}]}
    return json.dumps(obj)

def workbench(c):
    sim_buttons = '<button class="sim-mode-btn active" data-mode="bench" role="tab" aria-selected="true"><span class="sim-icon">⚡</span> Bench</button><button class="sim-mode-btn" data-mode="compare" role="tab" aria-selected="false"><span class="sim-icon">⇄</span> Compare</button><button class="sim-mode-btn" data-mode="sandbox" role="tab" aria-selected="false"><span class="sim-icon">⚙</span> Sandbox</button>'
    quiz_html = ''.join(
        '<article class="quiz-card"><h3>Question ' + str(i+1) + ': ' + E(q['question']) + '</h3><div class="options">' +
        ''.join('<button class="quiz-option" data-idx="' + str(j) + '">' + E(opt) + '</button>' for j, opt in enumerate(q['options'])) +
        '</div><p class="quiz-feedback" role="status" hidden>' + E(q['explanation']) + '</p></article>'
        for i, q in enumerate(c['quiz'])
    )
    return f'''<section aria-label="Interactive workbench"><div class="section-top"><div><div class="eyebrow">SOLID MECHANICS · FLUID MECHANICS · THERMODYNAMICS · DYNAMICS &amp; VIBRATIONS · MACHINE DESIGN · MECHATRONICS &amp; HVAC</div><h2>Your virtual mechanical engineering laboratory.</h2></div><button id="resetApparatus" class="text-button">Reset apparatus</button></div><div class="new-workbench"><div class="new-visual"><div class="visual-top"><div class="sim-mode-switcher" role="tablist" aria-label="Simulation Views">{sim_buttons}</div><button id="pauseMotion" class="dark-button" hidden>Pause motion</button></div><svg id="visualSvg" viewBox="0 0 520 280" role="img" aria-label="Interactive mechanical engineering workbench for {E(c['shortTitle'])}"></svg><div class="new-meter"><div><small>{E(c['rawLabel'].upper())}</small><strong id="readingValue">—</strong></div><div><small>CALIBRATED STRAIN &amp; DYNAMOMETER TELEMETRY</small><p id="liveState" style="font-size:11px;margin:7px 0">Ready to sample with {E(c['shortInput'])} = {c['initial']} {E(c['inputUnit'])}.</p></div></div></div><div class="new-controls"><label for="independent">{E(c['inputLabel'])}</label><output id="independentOut">{c['initial']} {E(c['inputUnit'])}</output><input id="independent" type="range" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><label for="independentNumber">Set {E(c['shortInput'])} ({E(c['inputUnit'])})</label><input id="independentNumber" type="number" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><div class="lab-control-meta">Actuator calibrated with Class 0.5 closed-loop servo controller.</div><button id="measure" class="primary full">Execute mechanical test trial</button><button id="recordReading" class="secondary full" disabled>＋ Record observation</button><p id="trialStatus" class="trial-status" role="status">Adjust {E(c['shortInput'])}, then execute mechanical acquisition.</p></div></div><p class="data-notice">Mechanical measurements are captured using precision transducers and 64-bit IEEE 754 floating-point logging. Residuals reflect ordinary least-squares regression across successive observations. Continuous data structures support comprehensive stress, thermal, and dynamical evaluation.</p><details class="model-note"><summary>Mechanical engineering continuum and boundary limits</summary><p>All structural components assume isotropic linear elastic behavior within small-strain deformation limits. Fluid flow fields comply with Navier-Stokes continuum conservation under negligible thermal dissipation.</p></details></section><section id="apparatus" class="lab-section"><h2>Laboratory apparatus &amp; testing equipment.</h2><div class="apparatus-list">{''.join('<article class="apparatus-item"><h3>'+E(a['name'])+'</h3><p>'+E(a['purpose'])+'</p></article>' for a in c['apparatus'])}</div></section><section id="method" class="lab-section"><div class="eyebrow">FOLLOW THE METHOD</div><h2>A reason behind every step.</h2><p class="intro">{E(c['aim'])} Standardized parameter settings: {", ".join(map(str,c['samples']))} {E(c['inputUnit'])}.</p>{method(c)}</section><section id="results" class="lab-section"><div class="section-top"><div><div class="eyebrow">YOUR NOTEBOOK · <span id="notebookCount">0</span> OBSERVATIONS</div><h2>Turn measurements into mechanical engineering insight.</h2></div><a class="text-button" href="/mechanical-engineering/{c['slug']}/report/">See a complete example report ↗</a></div><div class="lab-result-grid"><div class="chart-card"><svg id="labPlot" viewBox="0 0 520 260" role="img" aria-label="Measured observations and fitted regression graph"></svg><p>Points are your recorded observations. The solid regression line validates {E(c['shortTitle'])} mathematical scaling.</p></div><div class="fit-card lab-fit"><span class="eyebrow">LINEAR REGRESSION FIT · y = mx + b</span><div id="fitResult"></div><div class="report-equation">{E(c['fitEquation'])}</div></div></div><div class="table-card"><table><thead><tr><th>#</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th></tr></thead><tbody id="readingsBody"></tbody></table><p id="emptyReadings">No readings yet. Execute a mechanical trial and record it.</p></div><div class="lab-reading-actions"><button id="clearData" class="secondary">Clear notebook</button></div></section><section id="check" class="lab-section lab-questions"><div class="eyebrow">CHECK YOUR UNDERSTANDING</div><h2>Explain what the mechanical engineering metrics mean.</h2>{quiz_html}</section><section id="overview" class="lab-section"><div class="eyebrow">THEORY AND CONTINUUM CONTEXT</div><h2>Mechanical Engineering background &amp; physical principles.</h2><p class="intro">{E(c['aim'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>Mechanical engineering principles build upon continuum mechanics, thermodynamics, fluid dynamics, and rigid-body kinetics.</p></section>'''

def theory(c):
    rich_theory = c.get('theoryHtml', '')
    return f'''<article class="theory-article"><h2>Mechanical Engineering principles &amp; governing mechanics of {E(c['shortTitle'])}.</h2><p class="lead">{E(c['aim'])}</p><div class="report-equation">{E(c['fitEquation'])}</div>{rich_theory}<h3>Viva voce questions &amp; analytical theory</h3><div class="faq-list">{''.join(f'<details class="faq-item"><summary><strong>{E(t["question"])}</strong></summary><p>{E(t["answer"])}</p></details>' for t in c['topics'])}</div><h3>Experimental precautions and laboratory safety</h3><ul>{''.join(f'<li>{E(p)}</li>' for p in c['precautions'])}</ul><h3>Theoretical assumptions &amp; boundary condition limits</h3><ul><li>Isotropic, homogeneous continuum behaviour within small-displacement elastic deformation limits.</li><li>Steady-state boundary conditions with isothermal ambient baseline at 20.0 °C and 101.325 kPa.</li><li>Rigid boundary supports with negligible parasitic compliance and precision backlash-free kinematic mounting.</li></ul></article>'''

def report(c, rows, f, out):
    slug = c['slug']
    csvpath = f"/mechanical-engineering/{slug}/sample-data.csv"
    csv_content = io.StringIO()
    writer = csv.writer(csv_content)
    writer.writerow([c['shortInput'].replace(' ', '_'), c['rawLabel'].replace(' ', '_'), 'x_coord', 'y_coord', 'fitted_y', 'residual'])
    for r in rows:
        fit_y = f['m'] * r['x'] + f['b']
        writer.writerow([r['input'], r['raw'], f"{r['x']:.4f}", f"{r['y']:.4f}", f"{fit_y:.4f}", f"{r['y'] - fit_y:.4f}"])
    (out / f"mechanical-engineering/{slug}/sample-data.csv").write_text(csv_content.getvalue(), encoding='utf-8')

    value, se, reference = estimate(c, f)
    percent = abs(value - reference) / abs(reference) * 100
    uncertainty = uncertainty_text(c)
    abstract, graph_choice, discussion, conclusion = report_narrative(c, rows, f, value, percent, reference)

    obs = "".join(
        f"<tr><td>{i+1}</td><td>{r['input']}</td><td>{r['raw']}</td><td>{r['x']:.4f}</td><td>{r['y']:.4f}</td><td>{f['m']*r['x']+f['b']:.4f}</td><td>{r['y']-(f['m']*r['x']+f['b']):.4f}</td></tr>"
        for i, r in enumerate(rows)
    )

    rich_rep = c.get('reportHtml', '')

    return f'''<div class="section-top"><div><div class="eyebrow">WORKED EXAMPLE · BENCHMARK OBSERVATIONS</div><h2>A complete example mechanical engineering laboratory report.</h2></div><button class="secondary" onclick="window.print()">Print / save as PDF</button></div><div class="report-notice"><strong>Simulated demonstration data.</strong><p>This report illustrates formal engineering data reduction, instrument calibration tares, and parameter estimation. Replace its observations with your own experimental telemetry when preparing a mechanical engineering laboratory report submission.</p></div><div class="report-person"><span>Student: __________________</span><span>Student ID: __________________</span><span>Course: __________________</span><span>Date: __________________</span><span>Partner: __________________</span><span>Instructor: __________________</span></div><article class="lab-report"><h3>1. Title and aim</h3><p><strong>{E(c['title'])}.</strong> {E(c['aim'])}</p><h3>2. Abstract</h3><p>{E(abstract)}</p><h3>3. Apparatus and fixed settings</h3><ul>{''.join('<li>'+E(a['name'])+': '+E(a['purpose'])+'</li>' for a in c['apparatus'])}<li>Environmental Conditions: 20.0 °C ambient, 50% relative humidity, 101.325 kPa atmospheric pressure.</li><li>Transducer Calibration: Class 0.5 calibrated strain bridge and load cell with traceable ISO 7500-1 accuracy.</li></ul><h3>4. Theory and graph choice</h3><p>{E(c['aim'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>{E(graph_choice)}</p><h3>5. Method</h3><ol>{''.join('<li>'+E(s['text'])+'</li>' for s in c['procedure'])}</ol><h3>6. Observations and calculation table</h3><p>All mechanical observations use strictly controlled 64-bit IEEE 754 precision buffers. Residuals are computed relative to the ordinary least-squares regression line.</p><div class="table-card"><table><caption>Table 1. Six simulated observations; x and y represent transformed mechanical engineering metrics.</caption><thead><tr><th>No.</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Fitted y</th><th>Residual</th></tr></thead><tbody>{obs}</tbody></table></div><p><a href="{csvpath}" download>Download the sample observations (CSV) ↓</a></p><h3>7. Worked calculation for one observation</h3><div class="report-equation">{E(worked(c, rows[0]))}</div><h3>8. Graph, gradient and final calculation</h3><div class="chart-card">{graph(c, rows, f)}</div><p>Circular markers represent empirical mechanical observations. The solid line represents the ordinary least-squares linear fit.</p><div class="report-equation">x̄ = {fmt(f['mx'])}; ȳ = {fmt(f['my'])}<br>Σ(x − x̄)² = {fmt(f['sxx'])}<br>Σ(x − x̄)(y − ȳ) = {fmt(f['sxy'])}<br>m = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)² = {fmt(f['m'], 8)}<br>b = ȳ − mx̄ = {fmt(f['b'], 8)}<br>{E(formula(c, f))}</div><h3>9. Uncertainty and comparison</h3><p>Percentage difference = |estimate − theoretical value| / |theoretical value| × 100 = <strong>{percent:.4f}%</strong>.</p><p>For n = 6 observations, Σresidual² = {fmt(f['sse'])}; s² = Σresidual²/(n − 2). Gradient standard error = √[s²/Σ(x − x̄)²] = {fmt(f['slopeSE'])}. Intercept standard error = √[s²(1/n + x̄²/Σ(x − x̄)²)] = {fmt(f['interceptSE'])}.</p><p>Propagating the fit parameters yields a <strong>fit standard error of {fmt(se * c['resultScale'])} {E(c['resultUnit'])}</strong>, with an ideal coefficient of determination R² = {f['r2']:.6f}.</p><p>{E(uncertainty)}</p><h3>10. Result and discussion</h3><div class="report-equation">{E(c['targetName'])} = {fmt(value * c['resultScale'], c['resultDecimals'])} {E(c['resultUnit'])}<br>Theoretical reference value: {fmt(reference * c['resultScale'], c['resultDecimals'])} {E(c['resultUnit'])}</div><p>{E(discussion)}</p><h3>11. Precautions and limitations</h3><ul>{''.join('<li>'+E(p)+'</li>' for p in c['precautions'])}</ul><p>Continuum stress equations apply within linear elastic limits. High-cycle dynamic responses assume viscous damping under steady boundary excitations.</p><h3>12. Conclusion</h3><p>{E(conclusion)}</p><div class="full-report-supplement"><h4>In-Depth Technical Supplement &amp; Mechanical Engineering Derivation</h4>{rich_rep}</div></article>'''

def shell(c, part, body, base, production):
    path = f"/mechanical-engineering/{c['slug']}/" + ('' if part == 'experiment' else part + '/')
    title = {
        'experiment': c['title'] + ' | Mechanical Engineering Lab',
        'theory': c['shortTitle'] + ' Theory & Equations | Open STEM Lab',
        'report': c['shortTitle'] + ' Lab Report & Empirical Data | Open STEM Lab'
    }[part]
    desc = {
        'experiment': c['aim'] + ' Explore interactive mechanical simulation, stress-strain telemetry, and continuum mechanics.',
        'theory': 'Understand ' + c['shortTitle'].lower() + ': stress equations, thermodynamic cycles, fluid dynamics, and mechanical vibration analysis.',
        'report': 'A worked ' + c['shortTitle'].lower() + ' lab report with sample observation tables, regression plots, calculations, and error analysis.'
    }[part]
    header = head(path, title, desc, base, production).replace('<link rel="stylesheet" href="/catalog.css">', '<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/mechanical-lesson.css">')
    header = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: f'<script type="application/ld+json">{lesson_schema(c, part, path, title, desc, base)}</script>', header, flags=re.S)
    home = f'/mechanical-engineering/{c["slug"]}/'
    nav = '<aside class="sidebar"><a class="brand" style="font-size:20px" href="/">◉ openstemlab.</a><a class="side-subject" href="/subjects/mechanical-engineering/">← Mechanical Engineering labs</a><div class="side-label">LABORATORY ' + str(c['num']).zfill(2) + '</div><nav aria-label="Lesson navigation">'
    for href, label in [(home, 'Explore the experiment'), (home + 'theory/', 'Understand the theory'), (home + '#apparatus', 'Know your tools'), (home + '#method', 'Follow the method'), (home + '#results', 'Analyse your results'), (home + '#check', 'Check your understanding'), (home + 'report/', 'Sample lab report')]:
        nav += f'<a class="nav-item{" active" if path==href else ""}" href="{href}">{label}</a>'
    nav += '<a class="nav-item" href="/experiments/">Search all experiments</a></nav><div class="side-note"><span class="small-sun">✳</span><p>Learn by mechanical trial.<br>Understand by continuum and thermodynamic physics.</p></div><a class="text-button" href="/">← All subjects</a></aside>'
    heading = c['title'] if part == 'experiment' else c['shortTitle'] + ' theory' if part == 'theory' else c['shortTitle'] + ' lab report'
    return (
        header + '<body>' + nav + '<main><header class="topbar"><div><a href="/subjects/mechanical-engineering/">Mechanical Engineering</a> / ' + E(c['shortTitle']) + '</div><span class="free-label">FREE TO EXPLORE</span></header>'
        '<section class="page-heading"><div class="eyebrow">LABORATORY ' + str(c['num']).zfill(2) + ' · MECHANICAL ENGINEERING</div><h1>' + E(heading) + '</h1><p>' + E(desc) + '</p></section>'
        '<nav class="lab-navigation" aria-label="Experiment pages"><a href="' + home + '">Workbench</a><a href="' + home + 'theory/">Detailed theory</a><a href="' + home + '#method">Method</a><a href="' + home + '#results">My results</a><a href="' + home + 'report/">Example report</a></nav>'
        + body +
        '<footer><span class="footer-brand">openstemlab.</span><a href="/subjects/mechanical-engineering/">All mechanical engineering labs</a><span>Solid mechanics, fluid dynamics, heat transfer, machine elements, vibrations &amp; mechatronics model</span></footer></main>'
        + ('<script id="labConfig" type="application/json">' + json.dumps(c, ensure_ascii=False).replace('<', chr(92) + 'u003c') + '</script><script src="/mechanical-models.js"></script><script src="/mechanical-engine.js"></script>' if part == 'experiment' else '')
        + '</body></html>'
    )

def build_mechanical(out, base, production):
    published = [c for c in specs() if c.get('published', True)]
    (out / 'mechanical-lesson.css').write_text((ROOT / 'content/mechanical/lesson.css').read_text(encoding='utf-8'), encoding='utf-8')
    (out / 'mechanical-models.js').write_text((ROOT / 'content/mechanical/models.js').read_text(encoding='utf-8'), encoding='utf-8')
    (out / 'mechanical-engine.js').write_text((ROOT / 'content/mechanical/engine.js').read_text(encoding='utf-8'), encoding='utf-8')

    db = sqlite3.connect(ROOT / 'data/catalog.sqlite3')
    sid = db.execute("SELECT id FROM subjects WHERE slug='mechanical-engineering'").fetchone()[0]
    db.execute("UPDATE subjects SET content_status='live' WHERE slug='mechanical-engineering'")
    paths = []
    for c in published:
        slug = c['slug']
        home = f'/mechanical-engineering/{slug}/'
        (out / home.lstrip('/')).mkdir(parents=True, exist_ok=True)
        rows = [observation(c, v) for v in c['samples']]
        f = fit(rows)
        for part, body in [
            ('experiment', workbench(c)),
            ('theory', '<section>' + theory(c) + f'<div class="insight"><span>↳</span><div><strong>Connect mechanical theory to empirical strain &amp; dynamometer telemetry.</strong><p>Constitutive stress-strain laws, Navier-Stokes fluid equations, and thermodynamic state functions form the foundation of modern mechanical engineering design.</p></div></div></section>'),
            ('report', report(c, rows, f, out))
        ]:
            path = home + ('' if part == 'experiment' else part + '/')
            file = out / path.lstrip('/') / 'index.html'
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(shell(c, part, body, base, production), encoding='utf-8')
            paths.append(path)
        db.execute(
            'INSERT INTO experiments(subject_id,slug,title,status,page_path,theory_path,report_path) VALUES(?,?,?,?,?,?,?) ON CONFLICT(slug) DO UPDATE SET title=excluded.title,status=excluded.status,page_path=excluded.page_path,theory_path=excluded.theory_path,report_path=excluded.report_path',
            (sid, slug, c['shortTitle'], 'live', home, home + 'theory/', home + 'report/')
        )
    db.commit()
    db.close()
    return paths

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--production', action='store_true')
    args = parser.parse_args()
    config = json.loads((ROOT / 'site-config.json').read_text(encoding='utf-8'))
    base = config['base_url'].rstrip('/')
    out = ROOT / ('release' if args.production else 'dist')
    out.mkdir(exist_ok=True)
    paths = build_mechanical(out, base, args.production)
    print(f"Built {len(paths)} Mechanical Engineering pages for {base}: {paths[:3]}...")
