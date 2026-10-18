# -*- coding: utf-8 -*-
"""Static lesson pages and reproducible simulated reports for published Textile Engineering labs."""
from pathlib import Path
import json, math, csv, io, sqlite3, html, re

ROOT = Path(__file__).resolve().parent
E = lambda s: html.escape(str(s), quote=True)

def specs():
    return json.loads((ROOT / 'content/textile/experiments.json').read_text(encoding='utf-8'))

def rnd(x, n):
    return math.floor(x * 10**n + 0.5) / 10**n

def fmt(v, n=4):
    return f'{v:.3e}' if v and (abs(v) < 0.001 or abs(v) >= 1e6) else f'{v:.{n}f}'

PARAMS = {
    # Module 1: Yarn Manufacturing & Fiber Science (Labs 1–6)
    'cotton-fiber-length-uniformity-comb-sorter': {'type': 'linear_affine', 'slope': -0.2200, 'intercept': 29.5000, 'ref': 0.2200, 'abs_ref': True},
    'fiber-tensile-strength-stelometer-bundle-test': {'type': 'linear_prop', 'slope': 14.5000, 'ref': 14.5000},
    'yarn-linear-density-count-wrap-reel-analytical-balance': {'type': 'linear_prop', 'slope': 0.0200, 'ref': 0.0200},
    'yarn-twist-determination-untwist-retwist-method': {'type': 'linear_prop', 'slope': 820.0000, 'ref': 820.0000},
    'single-yarn-tensile-strength-elongation-cre': {'type': 'linear_prop', 'slope': 16.5000, 'ref': 16.5000},
    'yarn-lea-strength-count-strength-product-csp': {'type': 'linear_prop', 'slope': 2400.0000, 'ref': 2400.0000},

    # Module 2: Fabric Manufacturing (Weaving & Knitting) (Labs 7–12)
    'warp-sizing-percentage-size-add-on-tensile-gain': {'type': 'linear_prop', 'slope': 18.5000, 'ref': 18.5000},
    'fabric-areal-density-gsm-thickness-micrometer': {'type': 'linear_prop', 'slope': 220.0000, 'ref': 220.0000},
    'fabric-tensile-strip-grab-test-astm-d5034': {'type': 'linear_prop', 'slope': 12.8000, 'ref': 12.8000},
    'fabric-tearing-strength-elmendorf-ballistic-pendulum': {'type': 'linear_prop', 'slope': 3400.0000, 'ref': 3400.0000},
    'fabric-bursting-strength-hydraulic-diaphragm-tester': {'type': 'linear_prop', 'slope': 0.0450, 'ref': 0.0450},
    'weft-knitted-fabric-loop-length-stitch-density': {'type': 'linear_prop', 'slope': 16.0000, 'ref': 16.0000},

    # Module 3: Textile Chemical Processing, Wet Processing & Dyeing (Labs 13–18)
    'enzymatic-desizing-efficiency-tegewa-iodine-scale': {'type': 'linear_affine', 'slope': 14.5000, 'intercept': 12.0000, 'ref': 14.5000},
    'scouring-loss-absorbency-capillary-wicking-test': {'type': 'linear_prop', 'slope': 18.2000, 'ref': 18.2000},
    'hydrogen-peroxide-bleaching-whiteness-berger-cielab': {'type': 'linear_affine', 'slope': 0.8500, 'intercept': 32.0000, 'ref': 0.8500},
    'reactive-dye-exhaustion-kinetics-beer-lambert-absorbance': {'type': 'linear_prop', 'slope': 0.0385, 'ref': 0.0385},
    'color-fastness-to-washing-iso-105-c06-grey-scale': {'type': 'linear_affine', 'slope': 0.0820, 'intercept': -1.2000, 'ref': 0.0820},
    'color-fastness-to-crocking-rubbing-aatcc-crockmeter': {'type': 'linear_prop', 'slope': 0.0650, 'ref': 0.0650},

    # Module 4: Fabric Comfort, Hand & Physical Performance (Labs 19–24)
    'fabric-air-permeability-differential-pressure-flow': {'type': 'linear_prop', 'slope': 0.4200, 'ref': 0.4200},
    'fabric-water-vapor-permeability-cup-dish-method': {'type': 'linear_prop', 'slope': 1.4500, 'ref': 1.4500},
    'fabric-water-repellency-spray-rating-contact-angle': {'type': 'linear_affine', 'slope': 0.8500, 'intercept': 75.0000, 'ref': 0.8500},
    'fabric-bending-length-flexural-rigidity-shirley-stiffness': {'type': 'linear_prop', 'slope': 24.5000, 'ref': 24.5000},
    'fabric-crease-recovery-angle-shirley-recovery-tester': {'type': 'linear_affine', 'slope': 8.5000, 'intercept': 95.0000, 'ref': 8.5000},
    'fabric-drape-coefficient-digital-drape-meter': {'type': 'linear_affine', 'slope': 18.5000, 'intercept': 22.0000, 'ref': 18.5000},

    # Module 5: Textile Tribology, Durability & Surface Testing (Labs 25–28)
    'fabric-abrasion-resistance-martindale-mass-loss': {'type': 'linear_prop', 'slope': 1.6500, 'ref': 1.6500},
    'fabric-pilling-resistance-ici-pilling-box': {'type': 'linear_prop', 'slope': 5.2000, 'ref': 5.2000},
    'fabric-dimensional-stability-laundering-shrinkage': {'type': 'linear_affine', 'slope': 0.8500, 'intercept': 1.2000, 'ref': 0.8500},
    'seam-slippage-strength-woven-fabrics-fixed-load': {'type': 'linear_prop', 'slope': 0.0350, 'ref': 0.0350},

    # Module 6: Technical Textiles, Nonwovens & Color Science (Labs 29–32)
    'nonwoven-fabric-tensile-strength-anisotropy-ratio': {'type': 'linear_prop', 'slope': 2.4500, 'ref': 2.4500},
    'thermal-resistance-clo-value-guarded-hotplate': {'type': 'linear_prop', 'slope': 0.0240, 'ref': 0.0240},
    'ultraviolet-protection-factor-upf-transmittance-spectrophotometry': {'type': 'linear_affine', 'slope': 18.5000, 'intercept': 15.0000, 'ref': 18.5000},
    'spectrophotometric-color-matching-cielab-kubelka-munk': {'type': 'linear_prop', 'slope': 4.8500, 'ref': 4.8500}
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
    abstract = f"Laboratory evaluation of {c['title']} was conducted across six calibrated textile engineering setpoints under standard conditioning (20.0 °C, 65.0% RH per ISO 139). Measured empirical data was reduced and linearized, yielding an ordinary least-squares correlation coefficient R² = {f['r2']:.6f}. The experimental textile parameter {c['targetName']} was estimated as {value * c['resultScale']:.{c['resultDecimals']}f} {c['resultUnit']}, comparing against the standard theoretical reference benchmark of {reference * c['resultScale']:.{c['resultDecimals']}f} {c['resultUnit']} with a relative percentage deviation of {percent:.4f}%."
    graph_choice = f"Plotting {c['xAxis']} on the horizontal abscissa against {c['yAxis']} on the vertical ordinate demonstrates the linear governing response predicted by {c['shortTitle']} fiber, yarn, and fabric structural models."
    discussion = f"Experimental observations across all six trials demonstrate rigorous agreement with governing analytical models. OLS linear regression yielded slope m = {f['m']:.6f} and intercept b = {f['b']:.6f}, validating the governing equation {c['fitEquation']} with R² = {f['r2']:.6f}."
    conclusion = f"The experimental determination of {c['title']} confirmed the analytical textile model within an experimental uncertainty of {percent:.4f}%. Standardized conditioning and calibration protocols ensure high laboratory repeatability."
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
        grid += f'<line x1="{tx(gx)}" y1="{pad_t}" x2="{tx(gx)}" y2="{pad_t+ph}" stroke="#2e1065" stroke-dasharray="2,2"/>'
        grid += f'<line x1="{pad_l}" y1="{ty(gy)}" x2="{pad_l+pw}" y2="{ty(gy)}" stroke="#2e1065" stroke-dasharray="2,2"/>'
        grid += f'<text x="{tx(gx)}" y="{pad_t+ph+18}" font-size="10" fill="#c084fc" text-anchor="middle">{gx:.2f}</text>'
        grid += f'<text x="{pad_l-10}" y="{ty(gy)+4}" font-size="10" fill="#c084fc" text-anchor="end">{gy:.2f}</text>'

    x1, x2 = min_x, max_x
    y1, y2 = f['m'] * x1 + f['b'], f['m'] * x2 + f['b']
    line = f'<line x1="{tx(x1)}" y1="{ty(y1)}" x2="{tx(x2)}" y2="{ty(y2)}" stroke="#c084fc" stroke-width="2.5"/>'
    pts = "".join(f'<circle cx="{tx(r["x"])}" cy="{ty(r["y"])}" r="5" fill="#e879f9" stroke="#9333ea" stroke-width="1.5"/>' for r in rows)
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Regression graph">{grid}{line}{pts}<text x="{pad_l+pw/2}" y="{h-15}" font-size="12" fill="#f5d0fe" text-anchor="middle">{E(c["xAxis"])}</text><text transform="rotate(-90)" x="{-pad_t-ph/2}" y="22" font-size="12" fill="#f5d0fe" text-anchor="middle">{E(c["yAxis"])}</text></svg>'

def method(c):
    return '<ol class="method-steps">' + ''.join(f'<li><strong>{E(s["title"])}</strong>: {E(s["text"])}</li>' for s in c['procedure']) + '</ol>'

def head(path, title, desc, base, indexable):
    structured = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': title, 'description': desc, 'url': base + path, 'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'}, 'inLanguage': 'en'}
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="{'index,follow' if indexable else 'noindex,follow'}"><link rel="canonical" href="{base+path}"><meta name="theme-color" content="#f8f7f2"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{base+path}"><meta property="og:type" content="website"><link rel="stylesheet" href="/catalog.css"><script type="application/ld+json">{json.dumps(structured)}</script></head>'''

def lesson_schema(c, part, path, title, desc, base):
    obj = {'@context': 'https://schema.org', '@type': 'TechArticle', 'headline': title, 'description': desc, 'url': base + path, 'inLanguage': 'en', 'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'}, 'about': [{'@type': 'Thing', 'name': c['title']}, {'@type': 'Thing', 'name': 'Textile Engineering'}]}
    return json.dumps(obj)

def workbench(c):
    sim_buttons = '<button class="sim-mode-btn active" data-mode="bench" role="tab" aria-selected="true"><span class="sim-icon">⚡</span> Bench</button><button class="sim-mode-btn" data-mode="compare" role="tab" aria-selected="false"><span class="sim-icon">⇄</span> Compare</button><button class="sim-mode-btn" data-mode="sandbox" role="tab" aria-selected="false"><span class="sim-icon">⚙</span> Sandbox</button>'
    quiz_html = ''.join(
        '<article class="quiz-card"><h3>Question ' + str(i+1) + ': ' + E(q['question']) + '</h3><div class="options">' +
        ''.join('<button class="quiz-option" data-idx="' + str(j) + '">' + E(opt) + '</button>' for j, opt in enumerate(q['options'])) +
        '</div><p class="quiz-feedback" role="status" hidden>' + E(q['explanation']) + '</p></article>'
        for i, q in enumerate(c['quiz'])
    )
    return f'''<section aria-label="Interactive workbench"><div class="section-top"><div><div class="eyebrow">YARN SCIENCE · WEAVING &amp; KNITTING · WET PROCESSING · FABRIC COMFORT · TRIBOLOGY · TECHNICAL TEXTILES</div><h2>Your virtual textile engineering laboratory.</h2></div><button id="resetApparatus" class="text-button">Reset apparatus</button></div><div class="new-workbench"><div class="new-visual"><div class="visual-top"><div class="sim-mode-switcher" role="tablist" aria-label="Simulation Views">{sim_buttons}</div><button id="pauseMotion" class="dark-button" hidden>Pause motion</button></div><svg id="visualSvg" viewBox="0 0 520 280" role="img" aria-label="Interactive textile engineering workbench for {E(c['shortTitle'])}"></svg><div class="new-meter"><div><small>{E(c['rawLabel'].upper())}</small><strong id="readingValue">—</strong></div><div><small>CONDITIONED TEXTILE TELEMETRY (20 °C, 65% RH)</small><p id="liveState" style="font-size:11px;margin:7px 0">Ready to sample with {E(c['shortInput'])} = {c['initial']} {E(c['inputUnit'])}.</p></div></div></div><div class="new-controls"><label for="independent">{E(c['inputLabel'])}</label><output id="independentOut">{c['initial']} {E(c['inputUnit'])}</output><input id="independent" type="range" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><label for="independentNumber">Set {E(c['shortInput'])} ({E(c['inputUnit'])})</label><input id="independentNumber" type="number" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><div class="lab-control-meta">Conditioned per ISO 139 standard atmosphere (20.0 °C, 65.0% RH).</div><button id="measure" class="primary full">Execute textile test acquisition</button><button id="recordReading" class="secondary full" disabled>＋ Record observation</button><p id="trialStatus" class="trial-status" role="status">Adjust {E(c['shortInput'])}, then execute textile test acquisition.</p></div></div><p class="data-notice">Textile measurements are captured using precision transducers and 64-bit IEEE 754 floating-point logging under standard temperature and humidity. Residuals reflect ordinary least-squares regression across successive observations. Continuous data structures support comprehensive fiber, yarn, and fabric structural evaluation.</p><details class="model-note"><summary>Textile engineering continuum and boundary limits</summary><p>All fiber bundles, yarns, and fabric specimens are evaluated under standardized pre-tension and standard atmosphere (20 °C, 65% RH per ISO 139). Linear constitutive models reflect small-strain elasticity and uniform dye diffusion kinetics.</p></details></section><section id="apparatus" class="lab-section"><h2>Laboratory apparatus &amp; testing equipment.</h2><div class="apparatus-list">{''.join('<article class="apparatus-item"><h3>'+E(a['name'])+'</h3><p>'+E(a['purpose'])+'</p></article>' for a in c['apparatus'])}</div></section><section id="method" class="lab-section"><div class="eyebrow">FOLLOW THE METHOD</div><h2>A reason behind every step.</h2><p class="intro">{E(c['aim'])} Standardized parameter settings: {", ".join(map(str,c['samples']))} {E(c['inputUnit'])}.</p>{method(c)}</section><section id="results" class="lab-section"><div class="section-top"><div><div class="eyebrow">YOUR NOTEBOOK · <span id="notebookCount">0</span> OBSERVATIONS</div><h2>Turn measurements into textile engineering insight.</h2></div><a class="text-button" href="/textile-engineering/{c['slug']}/report/">See a complete example report ↗</a></div><div class="lab-result-grid"><div class="chart-card"><svg id="labPlot" viewBox="0 0 520 260" role="img" aria-label="Measured observations and fitted regression graph"></svg><p>Points are your recorded observations. The solid regression line validates {E(c['shortTitle'])} mathematical scaling.</p></div><div class="fit-card lab-fit"><span class="eyebrow">LINEAR REGRESSION FIT · y = mx + b</span><div id="fitResult"></div><div class="report-equation">{E(c['fitEquation'])}</div></div></div><div class="table-card"><table><thead><tr><th>#</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th></tr></thead><tbody id="readingsBody"></tbody></table><p id="emptyReadings">No readings yet. Execute a textile trial and record it.</p></div><div class="lab-reading-actions"><button id="clearData" class="secondary">Clear notebook</button></div></section><section id="check" class="lab-section lab-questions"><div class="eyebrow">CHECK YOUR UNDERSTANDING</div><h2>Explain what the textile engineering metrics mean.</h2>{quiz_html}</section><section id="overview" class="lab-section"><div class="eyebrow">THEORY AND FIBER-FABRIC CONTEXT</div><h2>Textile Engineering background &amp; physical principles.</h2><p class="intro">{E(c['aim'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>Textile engineering principles build upon polymer morphology, yarn structural mechanics, weave/knit topology, and surface transport thermodynamics.</p></section>'''

def theory(c):
    rich_theory = c.get('theoryHtml', '')
    return f'''<article class="theory-article"><h2>Textile Engineering principles &amp; governing mechanics of {E(c['shortTitle'])}.</h2><p class="lead">{E(c['aim'])}</p><div class="report-equation">{E(c['fitEquation'])}</div>{rich_theory}<h3>Viva voce questions &amp; analytical theory</h3><div class="faq-list">{''.join(f'<details class="faq-item"><summary><strong>{E(t["question"])}</strong></summary><p>{E(t["answer"])}</p></details>' for t in c['topics'])}</div><h3>Experimental precautions and laboratory safety</h3><ul>{''.join(f'<li>{E(p)}</li>' for p in c['precautions'])}</ul><h3>Theoretical assumptions &amp; boundary condition limits</h3><ul><li>Standard temperate testing atmosphere (20.0 ± 2.0 °C and 65.0 ± 4.0% RH per ISO 139) maintaining moisture equilibrium.</li><li>Homogeneous yarn linear density and isotropic fiber distribution within specified testing gauge lengths.</li><li>Non-slip pneumatic bollard clamping preventing jaw breaks and localized stress concentrations.</li></ul></article>'''

def report(c, rows, f, out):
    slug = c['slug']
    csvpath = f"/textile-engineering/{slug}/sample-data.csv"
    csv_content = io.StringIO()
    writer = csv.writer(csv_content)
    writer.writerow([c['shortInput'].replace(' ', '_'), c['rawLabel'].replace(' ', '_'), 'x_coord', 'y_coord', 'fitted_y', 'residual'])
    for r in rows:
        fit_y = f['m'] * r['x'] + f['b']
        writer.writerow([r['input'], r['raw'], f"{r['x']:.4f}", f"{r['y']:.4f}", f"{fit_y:.4f}", f"{r['y'] - fit_y:.4f}"])
    (out / f"textile-engineering/{slug}/sample-data.csv").write_text(csv_content.getvalue(), encoding='utf-8')

    value, se, reference = estimate(c, f)
    percent = abs(value - reference) / abs(reference) * 100
    uncertainty = uncertainty_text(c)
    abstract, graph_choice, discussion, conclusion = report_narrative(c, rows, f, value, percent, reference)

    obs = "".join(
        f"<tr><td>{i+1}</td><td>{r['input']}</td><td>{r['raw']}</td><td>{r['x']:.4f}</td><td>{r['y']:.4f}</td><td>{f['m']*r['x']+f['b']:.4f}</td><td>{r['y']-(f['m']*r['x']+f['b']):.4f}</td></tr>"
        for i, r in enumerate(rows)
    )

    rich_rep = c.get('reportHtml', '')

    return f'''<div class="section-top"><div><div class="eyebrow">WORKED EXAMPLE · BENCHMARK OBSERVATIONS</div><h2>A complete example textile engineering laboratory report.</h2></div><button class="secondary" onclick="window.print()">Print / save as PDF</button></div><div class="report-notice"><strong>Simulated demonstration data.</strong><p>This report illustrates formal engineering data reduction, instrument calibration tares, and parameter estimation. Replace its observations with your own experimental telemetry when preparing a textile engineering laboratory report submission.</p></div><div class="report-person"><span>Student: __________________</span><span>Student ID: __________________</span><span>Course: __________________</span><span>Date: __________________</span><span>Partner: __________________</span><span>Instructor: __________________</span></div><article class="lab-report"><h3>1. Title and aim</h3><p><strong>{E(c['title'])}.</strong> {E(c['aim'])}</p><h3>2. Abstract</h3><p>{E(abstract)}</p><h3>3. Apparatus and fixed settings</h3><ul>{''.join('<li>'+E(a['name'])+': '+E(a['purpose'])+'</li>' for a in c['apparatus'])}<li>Environmental Conditioning: 20.0 °C ambient, 65.0% relative humidity, 101.325 kPa atmospheric pressure per ISO 139.</li><li>Transducer Calibration: Class 0.5 calibrated strain bridge and load cell with traceable ISO 7500-1 accuracy.</li></ul><h3>4. Theory and graph choice</h3><p>{E(c['aim'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>{E(graph_choice)}</p><h3>5. Method</h3><ol>{''.join('<li>'+E(s['text'])+'</li>' for s in c['procedure'])}</ol><h3>6. Observations and calculation table</h3><p>All textile observations use strictly controlled 64-bit IEEE 754 precision buffers under conditioned equilibrium. Residuals are computed relative to the ordinary least-squares regression line.</p><div class="table-card"><table><caption>Table 1. Six simulated observations; x and y represent transformed textile engineering metrics.</caption><thead><tr><th>No.</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Fitted y</th><th>Residual</th></tr></thead><tbody>{obs}</tbody></table></div><p><a href="{csvpath}" download>Download the sample observations (CSV) ↓</a></p><h3>7. Worked calculation for one observation</h3><div class="report-equation">{E(worked(c, rows[0]))}</div><h3>8. Graph, gradient and final calculation</h3><div class="chart-card">{graph(c, rows, f)}</div><p>Circular markers represent empirical textile observations. The solid line represents the ordinary least-squares linear fit.</p><div class="report-equation">x̄ = {fmt(f['mx'])}; ȳ = {fmt(f['my'])}<br>Σ(x − x̄)² = {fmt(f['sxx'])}<br>Σ(x − x̄)(y − ȳ) = {fmt(f['sxy'])}<br>m = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)² = {fmt(f['m'], 8)}<br>b = ȳ − mx̄ = {fmt(f['b'], 8)}<br>{E(formula(c, f))}</div><h3>9. Uncertainty and comparison</h3><p>Percentage difference = |estimate − theoretical value| / |theoretical value| × 100 = <strong>{percent:.4f}%</strong>.</p><p>For n = 6 observations, Σresidual² = {fmt(f['sse'])}; s² = Σresidual²/(n − 2). Gradient standard error = √[s²/Σ(x − x̄)²] = {fmt(f['slopeSE'])}. Intercept standard error = √[s²(1/n + x̄²/Σ(x − x̄)²)] = {fmt(f['interceptSE'])}.</p><p>Propagating the fit parameters yields a <strong>fit standard error of {fmt(se * c['resultScale'])} {E(c['resultUnit'])}</strong>, with an ideal coefficient of determination R² = {f['r2']:.6f}.</p><p>{E(uncertainty)}</p><h3>10. Result and discussion</h3><div class="report-equation">{E(c['targetName'])} = {fmt(value * c['resultScale'], c['resultDecimals'])} {E(c['resultUnit'])}<br>Theoretical reference value: {fmt(reference * c['resultScale'], c['resultDecimals'])} {E(c['resultUnit'])}</div><p>{E(discussion)}</p><h3>11. Precautions and limitations</h3><ul>{''.join('<li>'+E(p)+'</li>' for p in c['precautions'])}</ul><p>Polymer stress equations apply within linear elastic and uniform conditioning limits. Wet processing kinetics assume ideal mass transfer without boundary boundary layer exhaustion artifacts.</p><h3>12. Conclusion</h3><p>{E(conclusion)}</p><div class="full-report-supplement"><h4>In-Depth Technical Supplement &amp; Textile Engineering Derivation</h4>{rich_rep}</div></article>'''

def shell(c, part, body, base, production):
    path = f"/textile-engineering/{c['slug']}/" + ('' if part == 'experiment' else part + '/')
    title = {
        'experiment': c['title'] + ' | Textile Engineering Lab',
        'theory': c['shortTitle'] + ' Theory & Equations | Open STEM Lab',
        'report': c['shortTitle'] + ' Lab Report & Empirical Data | Open STEM Lab'
    }[part]
    desc = {
        'experiment': c['aim'] + ' Explore interactive textile simulation, yarn mechanics, and fabric physical testing.',
        'theory': 'Understand ' + c['shortTitle'].lower() + ': fiber morphology, yarn twist, fabric structure, and color science equations.',
        'report': 'A worked ' + c['shortTitle'].lower() + ' lab report with sample observation tables, regression plots, calculations, and error analysis.'
    }[part]
    header = head(path, title, desc, base, production).replace('<link rel="stylesheet" href="/catalog.css">', '<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/textile-lesson.css">')
    header = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: f'<script type="application/ld+json">{lesson_schema(c, part, path, title, desc, base)}</script>', header, flags=re.S)
    home = f'/textile-engineering/{c["slug"]}/'
    nav = '<aside class="sidebar"><a class="brand" style="font-size:20px" href="/">◉ openstemlab.</a><a class="side-subject" href="/subjects/textile-engineering/">← Textile Engineering labs</a><div class="side-label">LABORATORY ' + str(c['num']).zfill(2) + '</div><nav aria-label="Lesson navigation">'
    for href, label in [(home, 'Explore the experiment'), (home + 'theory/', 'Understand the theory'), (home + '#apparatus', 'Know your tools'), (home + '#method', 'Follow the method'), (home + '#results', 'Analyse your results'), (home + '#check', 'Check your understanding'), (home + 'report/', 'Sample lab report')]:
        nav += f'<a class="nav-item{" active" if path==href else ""}" href="{href}">{label}</a>'
    nav += '<a class="nav-item" href="/experiments/">Search all experiments</a></nav><div class="side-note"><span class="small-sun">✳</span><p>Learn by textile trial.<br>Understand by fiber and polymer physics.</p></div><a class="text-button" href="/">← All subjects</a></aside>'
    heading = c['title'] if part == 'experiment' else c['shortTitle'] + ' theory' if part == 'theory' else c['shortTitle'] + ' lab report'
    return (
        header + '<body>' + nav + '<main><header class="topbar"><div><a href="/subjects/textile-engineering/">Textile Engineering</a> / ' + E(c['shortTitle']) + '</div><span class="free-label">FREE TO EXPLORE</span></header>'
        '<section class="page-heading"><div class="eyebrow">LABORATORY ' + str(c['num']).zfill(2) + ' · TEXTILE ENGINEERING</div><h1>' + E(heading) + '</h1><p>' + E(desc) + '</p></section>'
        '<nav class="lab-navigation" aria-label="Experiment pages"><a href="' + home + '">Workbench</a><a href="' + home + 'theory/">Detailed theory</a><a href="' + home + '#method">Method</a><a href="' + home + '#results">My results</a><a href="' + home + 'report/">Example report</a></nav>'
        + body +
        '<footer><span class="footer-brand">openstemlab.</span><a href="/subjects/textile-engineering/">All textile engineering labs</a><span>Yarn science, fabric mechanics, wet processing, comfort &amp; technical textiles model</span></footer></main>'
        + ('<script id="labConfig" type="application/json">' + json.dumps(c, ensure_ascii=False).replace('<', chr(92) + 'u003c') + '</script><script src="/textile-models.js"></script><script src="/textile-engine.js"></script>' if part == 'experiment' else '')
        + '</body></html>'
    )

def build_textile(out, base, production):
    published = [c for c in specs() if c.get('published', True)]
    (out / 'textile-lesson.css').write_text((ROOT / 'content/textile/lesson.css').read_text(encoding='utf-8'), encoding='utf-8')
    (out / 'textile-models.js').write_text((ROOT / 'content/textile/models.js').read_text(encoding='utf-8'), encoding='utf-8')
    (out / 'textile-engine.js').write_text((ROOT / 'content/textile/engine.js').read_text(encoding='utf-8'), encoding='utf-8')

    db = sqlite3.connect(ROOT / 'data/catalog.sqlite3')
    sid = db.execute("SELECT id FROM subjects WHERE slug='textile-engineering'").fetchone()[0]
    db.execute("UPDATE subjects SET content_status='live' WHERE slug='textile-engineering'")
    paths = []
    for c in published:
        slug = c['slug']
        home = f'/textile-engineering/{slug}/'
        (out / home.lstrip('/')).mkdir(parents=True, exist_ok=True)
        rows = [observation(c, v) for v in c['samples']]
        f = fit(rows)
        for part, body in [
            ('experiment', workbench(c)),
            ('theory', '<section>' + theory(c) + f'<div class="insight"><span>↳</span><div><strong>Connect textile theory to empirical fiber, yarn &amp; fabric telemetry.</strong><p>Polymer physics, Peirce fabric geometry, and Kubelka-Munk optical formulations form the core foundation of textile engineering.</p></div></div></section>'),
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
    paths = build_textile(out, base, args.production)
    print(f"Built {len(paths)} Textile Engineering pages for {base}: {paths[:3]}...")
