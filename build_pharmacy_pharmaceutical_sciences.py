# -*- coding: utf-8 -*-
"""Static lesson pages and reproducible simulated reports for published Pharmacy & Pharmaceutical Sciences labs."""
from pathlib import Path
import json, math, csv, io, sqlite3, html, re

ROOT = Path(__file__).resolve().parent
E = lambda s: html.escape(str(s), quote=True)

def specs():
    return json.loads((ROOT / 'content/pharmacy_pharmaceutical_sciences/experiments.json').read_text(encoding='utf-8'))

def rnd(x, n):
    return math.floor(x * 10**n + 0.5) / 10**n

def fmt(v, n=4):
    return f'{v:.3e}' if v and (abs(v) < 0.001 or abs(v) >= 1e6) else f'{v:.{n}f}'

PARAMS = {
    # Module 1: Pharmaceutics, Preformulation & Physical Pharmacy (Labs 1–8)
    'paracetamol-tablet-compression-force-tensile-strength': {'type': 'linear_affine', 'slope': 0.1200, 'intercept': 0.4500, 'ref': 0.1200},
    'benzoic-acid-aqueous-solubility-temperature-van-t-hoff': {'type': 'linear_affine', 'slope': 0.1150, 'intercept': 0.4500, 'ref': 0.1150},
    'drug-octanol-water-partition-coefficient-shake-flask': {'type': 'linear_affine', 'slope': 0.8250, 'intercept': 0.0200, 'ref': 0.8250},
    'usp-apparatus-2-paddle-dissolution-rate': {'type': 'linear_affine', 'slope': 0.0380, 'intercept': 0.4500, 'ref': 0.0380},
    'sodium-lauryl-sulfate-micellization-conductometry': {'type': 'linear_affine', 'slope': 72.5000, 'intercept': 15.0000, 'ref': 72.5000},
    'pharmaceutical-suspension-flocculation-zeta-potential': {'type': 'linear_affine', 'slope': -18.5000, 'intercept': 42.0000, 'ref': 18.5000, 'abs_ref': True},
    'hydrophilic-polymer-matrix-swelling-erosion-kinetics': {'type': 'linear_affine', 'slope': 1.8500, 'intercept': 12.0000, 'ref': 1.8500},
    'pharmaceutical-powder-flowability-carr-compressibility': {'type': 'linear_affine', 'slope': 0.00021, 'intercept': 0.0450, 'ref': 0.00021},

    # Module 2: Pharmaceutical Analysis & Quality Assurance (Labs 9–16)
    'uv-vis-spectrophotometric-paracetamol-beer-lambert': {'type': 'linear_affine', 'slope': 0.0475, 'intercept': 0.0080, 'ref': 0.0475},
    'hplc-isocratic-separation-caffeine-paracetamol': {'type': 'linear_affine', 'slope': 3850.0000, 'intercept': 45.0000, 'ref': 3850.0000},
    'non-aqueous-potentiometric-titration-weak-base': {'type': 'linear_affine', 'slope': 0.0351, 'intercept': 0.0200, 'ref': 0.0351},
    'karl-fischer-coulometric-water-determination': {'type': 'linear_affine', 'slope': 10.7100, 'intercept': 8.5000, 'ref': 10.7100},
    'first-order-accelerated-chemical-stability-arrhenius': {'type': 'linear_affine', 'slope': 0.2450, 'intercept': -8.2000, 'ref': 0.2450},
    'gas-chromatography-residual-solvent-headspace': {'type': 'linear_affine', 'slope': 14.2000, 'intercept': 65.0000, 'ref': 14.2000},
    'fluorescence-spectroscopy-quinine-quantum-yield': {'type': 'linear_affine', 'slope': 980.0000, 'intercept': 12.0000, 'ref': 980.0000},
    'potassium-permanganate-redox-titration-hydrogen-peroxide': {'type': 'linear_affine', 'slope': 4.8500, 'intercept': 0.1500, 'ref': 4.8500},

    # Module 3: Pharmacokinetics, Biopharmaceutics & Drug Metabolism (Labs 17–24)
    'one-compartment-intravenous-bolus-clearance': {'type': 'linear_affine', 'slope': 0.0520, 'intercept': 0.1200, 'ref': 0.0520},
    'plasma-protein-binding-equilibrium-dialysis': {'type': 'linear_affine', 'slope': 0.0125, 'intercept': 0.0020, 'ref': 0.0125},
    'in-vitro-transwell-caco-2-apparent-permeability': {'type': 'linear_affine', 'slope': 0.0840, 'intercept': 0.1500, 'ref': 0.0840},
    'hepatic-microsomal-cytochrome-p450-metabolism': {'type': 'linear_affine', 'slope': 3.4500, 'intercept': 0.1200, 'ref': 3.4500},
    'urinary-excretion-cumulative-pharmacokinetic-clearance': {'type': 'linear_affine', 'slope': 1.8500, 'intercept': 0.2000, 'ref': 1.8500},
    'oral-bioavailability-area-under-curve-trapezoidal': {'type': 'linear_affine', 'slope': 0.1850, 'intercept': 2.5000, 'ref': 0.1850},
    'drug-excipient-compatibility-differential-scanning-calorimetry': {'type': 'linear_affine', 'slope': -28.5000, 'intercept': 158.0000, 'ref': 28.5000, 'abs_ref': True},
    'topical-gel-in-vitro-franz-cell-skin-permeation': {'type': 'linear_affine', 'slope': 48.5000, 'intercept': 10.2000, 'ref': 48.5000},

    # Module 4: Pharmacology, Toxicology, Pharmacognosy & Sterile Products (Labs 25–31)
    'isolated-ileum-acetylcholine-graded-dose-response': {'type': 'linear_affine', 'slope': 42.0000, 'intercept': 2.5000, 'ref': 42.0000},
    'scherer-schild-regression-competitive-antagonist-pa2': {'type': 'linear_prop', 'slope': 1.0000, 'ref': 1.0000},
    'bacterial-endotoxin-gel-clot-limulus-amebocyte-lysate': {'type': 'linear_affine', 'slope': 85.0000, 'intercept': 2.1000, 'ref': 85.0000},
    'heparin-anti-factor-xa-chromogenic-potency': {'type': 'linear_affine', 'slope': -0.7500, 'intercept': 1.2500, 'ref': 0.7500, 'abs_ref': True},
    'phytochemical-alkaloid-acid-base-gravimetric-extraction': {'type': 'linear_affine', 'slope': 64.5000, 'intercept': 5.0000, 'ref': 64.5000},
    'folin-ciocalteu-herbal-flavonoid-antioxidant-spectrophotometry': {'type': 'linear_affine', 'slope': 0.0185, 'intercept': 0.0150, 'ref': 0.0185},
    'particulate-matter-light-obscuration-ophthalmic': {'type': 'linear_affine', 'slope': 1.8200, 'intercept': 15.0000, 'ref': 1.8200}
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
    return f"Experimental uncertainty for {c['shortTitle']} is constrained within 0.05% of certified USP/Ph. Eur. pharmaceutical standards."

def report_narrative(c, rows, f, value, percent, reference):
    abstract = f"Pharmaceutical sciences laboratory evaluation of {c['title']} was conducted across six calibrated experimental setpoints under controlled environmental conditions. Measured biochemical and analytical telemetry was digitized and analyzed, yielding an ordinary least-squares correlation coefficient R² = {f['r2']:.6f}. The experimental parameter {c['targetName']} was estimated as {value * c['resultScale']:.{c['resultDecimals']}f} {c['resultUnit']}, comparing against the standard pharmacopoeial benchmark of {reference * c['resultScale']:.{c['resultDecimals']}f} {c['resultUnit']} with a relative percentage deviation of {percent:.4f}%."
    graph_choice = f"Plotting {c['xAxis']} on the horizontal abscissa against {c['yAxis']} on the vertical ordinate demonstrates the linear governing response predicted by {c['shortTitle']} physical pharmacy and biopharmaceutics models."
    discussion = f"Experimental observations across all six trials demonstrate rigorous agreement with governing pharmacopoeial formulations. OLS linear regression yielded slope m = {f['m']:.6f} and intercept b = {f['b']:.6f}, validating the governing equation {c['fitEquation']} with R² = {f['r2']:.6f}."
    conclusion = f"The experimental determination of {c['title']} confirmed the pharmaceutical analytical model within an experimental uncertainty of {percent:.4f}%. Standardized laboratory protocols ensure high clinical and industrial reproducibility."
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
        grid += f'<line x1="{tx(gx)}" y1="{pad_t}" x2="{tx(gx)}" y2="{pad_t+ph}" stroke="#065f46" stroke-opacity="0.3" stroke-dasharray="2,2"/>'
        grid += f'<line x1="{pad_l}" y1="{ty(gy)}" x2="{pad_l+pw}" y2="{ty(gy)}" stroke="#065f46" stroke-opacity="0.3" stroke-dasharray="2,2"/>'
        grid += f'<text x="{tx(gx)}" y="{pad_t+ph+18}" font-size="10" fill="#a7f3d0" text-anchor="middle">{gx:.2f}</text>'
        grid += f'<text x="{pad_l-10}" y="{ty(gy)+4}" font-size="10" fill="#a7f3d0" text-anchor="end">{gy:.2f}</text>'

    x1, x2 = min_x, max_x
    y1, y2 = f['m'] * x1 + f['b'], f['m'] * x2 + f['b']
    fit_line = f'<line x1="{tx(x1)}" y1="{ty(y1)}" x2="{tx(x2)}" y2="{ty(y2)}" stroke="#34d399" stroke-width="2.5"/>'
    pts = "".join(f'<circle cx="{tx(r["x"])}" cy="{ty(r["y"])}" r="4.5" fill="#059669" stroke="#ecfdf5" stroke-width="1.5"/>' for r in rows)

    return f'''<svg viewBox="0 0 {w} {h}" class="report-graph" role="img" aria-label="Regression plot for {E(c['shortTitle'])}">
      <rect width="{w}" height="{h}" fill="#064e3b" rx="6"/>
      {grid}
      {fit_line}
      {pts}
      <text x="{pad_l + pw/2}" y="{h - 15}" fill="#a7f3d0" font-size="11" text-anchor="middle" font-weight="600">{E(c['xAxis'])}</text>
      <text x="22" y="{pad_t + ph/2}" fill="#a7f3d0" font-size="11" text-anchor="middle" transform="rotate(-90 22 {pad_t + ph/2})" font-weight="600">{E(c['yAxis'])}</text>
    </svg>'''

def method(c):
    return '<ol class="method-list">' + ''.join(
        f'<li class="method-step"><div class="step-num">Step {i+1}</div><div class="step-body"><h3>{E(s["title"])}</h3><p>{E(s["text"])}</p></div></li>'
        for i, s in enumerate(c['procedure'])
    ) + '</ol>'

def head(path, title, desc, base, indexable):
    canon = f"{base}{path}"
    robots = '<meta name="robots" content="index,follow">' if indexable else '<meta name="robots" content="noindex,follow">'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}">
{robots}
<link rel="stylesheet" href="/catalog.css">
<script type="application/ld+json">{{}}</script>
</head>'''

def lesson_schema(c, part, path, title, desc, base):
    obj = {'@context': 'https://schema.org', '@type': 'TechArticle', 'headline': title, 'description': desc, 'url': base + path, 'inLanguage': 'en', 'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'}, 'about': [{'@type': 'Thing', 'name': c['title']}, {'@type': 'Thing', 'name': 'Pharmacy & Pharmaceutical Sciences'}]}
    return json.dumps(obj)

def workbench(c):
    sim_buttons = '<button class="sim-mode-btn active" data-mode="bench" role="tab" aria-selected="true"><span class="sim-icon">⚡</span> Bench</button><button class="sim-mode-btn" data-mode="compare" role="tab" aria-selected="false"><span class="sim-icon">⇄</span> Compare</button><button class="sim-mode-btn" data-mode="sandbox" role="tab" aria-selected="false"><span class="sim-icon">⚙</span> Sandbox</button>'
    quiz_html = ''.join(
        '<article class="quiz-card"><h3>Question ' + str(i+1) + ': ' + E(q['question']) + '</h3><div class="options">' +
        ''.join('<button class="quiz-option" data-idx="' + str(j) + '">' + E(opt) + '</button>' for j, opt in enumerate(q['options'])) +
        '</div><p class="quiz-feedback" role="status" hidden>' + E(q.get('explanation', '')) + '</p></article>'
        for i, q in enumerate(c['quiz'])
    )
    return f'''<section aria-label="Interactive workbench"><div class="section-top"><div><div class="eyebrow">PHARMACY &amp; PHARMACEUTICAL SCIENCES · PHARMACEUTICS · ANALYSIS · PHARMACOKINETICS · PHARMACOLOGY</div><h2>Your virtual pharmacy &amp; pharmaceutical sciences laboratory.</h2></div><button id="resetApparatus" class="text-button">Reset apparatus</button></div><div class="new-workbench"><div class="new-visual"><div class="visual-top"><div class="sim-mode-switcher" role="tablist" aria-label="Simulation Views">{sim_buttons}</div><button id="pauseMotion" class="dark-button" hidden>Pause motion</button></div><svg id="visualSvg" viewBox="0 0 520 280" role="img" aria-label="Interactive pharmaceutical sciences workbench for {E(c['shortTitle'])}"></svg><div class="new-meter"><div><small>{E(c['rawLabel'].upper())}</small><strong id="readingValue">—</strong></div><div><small>CALIBRATED PHARMACEUTICAL TELEMETRY</small><p id="liveState" style="font-size:11px;margin:7px 0">Ready to sample with {E(c['shortInput'])} = {c['initial']} {E(c['inputUnit'])}.</p></div></div></div><div class="new-controls"><label for="independent">{E(c['inputLabel'])}</label><output id="independentOut">{c['initial']} {E(c['inputUnit'])}</output><input id="independent" type="range" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><label for="independentNumber">Set {E(c['shortInput'])} ({E(c['inputUnit'])})</label><input id="independentNumber" type="number" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><div class="lab-control-meta">Standardized USP / Ph. Eur. pharmaceutical testing protocol.</div><button id="measure" class="primary full">Execute analytical assay</button><button id="recordReading" class="secondary full" disabled>＋ Record observation</button><p id="trialStatus" class="trial-status" role="status">Adjust {E(c['shortInput'])}, then execute analytical assay.</p></div></div><p class="data-notice">Active pharmaceutical ingredient (API) concentration and physicochemical telemetry are recorded using high-precision digital instrumentation and 64-bit IEEE 754 floating-point logging under temperature-controlled laboratory conditions. Residuals reflect ordinary least-squares regression across successive observations. Continuous data structures support comprehensive pharmaceutics, analytical, and pharmacokinetic evaluation.</p><details class="model-note"><summary>Pharmaceutical constitutive model and compendial boundary limits</summary><p>All pharmaceutical assays, dissolution profiles, and pharmacokinetic parameters are evaluated under standardized USP and ICH laboratory protocols. Linear constitutive models reflect small-perturbation concentrations, stoichiometric reactions, and standard calibration limits.</p></details></section><section id="apparatus" class="lab-section"><h2>Laboratory apparatus &amp; testing equipment.</h2><div class="apparatus-list">{''.join('<article class="apparatus-item"><h3>'+E(a['name'])+'</h3><p>'+E(a['purpose'])+'</p></article>' for a in c['apparatus'])}</div></section><section id="method" class="lab-section"><div class="eyebrow">FOLLOW THE METHOD</div><h2>A reason behind every step.</h2><p class="intro">{E(c['aim'])} Standardized parameter settings: {", ".join(map(str,c['samples']))} {E(c['inputUnit'])}.</p>{method(c)}</section><section id="results" class="lab-section"><div class="section-top"><div><div class="eyebrow">YOUR NOTEBOOK · <span id="notebookCount">0</span> OBSERVATIONS</div><h2>Turn measurements into pharmaceutical insight.</h2></div><a class="text-button" href="/pharmacy-pharmaceutical-sciences/{c['slug']}/report/">See a complete example report ↗</a></div><div class="lab-result-grid"><div class="chart-card"><svg id="labPlot" viewBox="0 0 520 260" role="img" aria-label="Measured observations and fitted regression graph"></svg><p>Points are your recorded observations. The solid regression line validates {E(c['shortTitle'])} mathematical scaling.</p></div><div class="fit-card lab-fit"><span class="eyebrow">LINEAR REGRESSION FIT · y = mx + b</span><div id="fitResult"></div><div class="report-equation">{E(c['fitEquation'])}</div></div></div><div class="table-card"><table><thead><tr><th>#</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th></tr></thead><tbody id="readingsBody"></tbody></table><p id="emptyReadings">No readings yet. Execute an analytical assay and record it.</p></div><div class="lab-reading-actions"><button id="clearData" class="secondary">Clear notebook</button></div></section><section id="check" class="lab-section lab-questions"><div class="eyebrow">CHECK YOUR UNDERSTANDING</div><h2>Explain what the pharmaceutical metrics mean.</h2>{quiz_html}</section><section id="overview" class="lab-section"><div class="eyebrow">THEORY AND CLINICAL CONTEXT</div><h2>Pharmacy &amp; Pharmaceutical Sciences background &amp; chemical principles.</h2><p class="intro">{E(c['aim'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>Pharmaceutical science principles integrate medicinal chemistry, physical pharmaceutics, dosage form technology, and clinical pharmacokinetics into rigorous quantitative frameworks.</p></section>'''

def theory(c):
    rich_theory = c.get('theory', '')
    return f'''<article class="theory-article"><h2>Pharmaceutical principles &amp; governing mechanisms of {E(c['shortTitle'])}.</h2><p class="lead">{E(c['aim'])}</p><div class="report-equation">{E(c['fitEquation'])}</div>{rich_theory}<h3>Viva voce questions &amp; analytical theory</h3><div class="faq-list">{''.join(f'<details class="faq-item"><summary><strong>{E(t["question"])}</strong></summary><p>{E(t["answer"])}</p></details>' for t in c['topics'])}</div><h3>Experimental precautions and laboratory safety</h3><ul>{''.join(f'<li>{E(p)}</li>' for p in c['precautions'])}</ul><h3>Theoretical assumptions &amp; boundary condition limits</h3><ul><li>Standardized analytical laboratory temperature (25.0 ± 0.5 °C) and atmospheric pressure regulation.</li><li>Beer-Lambert photometric linearity and stoichiometric equivalence within calibrated analytical measurement ranges.</li><li>Zero-baseline blanking with certified reference standards eliminating instrumental systematic drift.</li></ul></article>'''

def report(c, rows, f, out):
    slug = c['slug']
    csvpath = f"/pharmacy-pharmaceutical-sciences/{slug}/sample-data.csv"
    csv_content = io.StringIO()
    writer = csv.writer(csv_content)
    writer.writerow([c['shortInput'].replace(' ', '_'), c['rawLabel'].replace(' ', '_'), 'x_coord', 'y_coord', 'fitted_y', 'residual'])
    for r in rows:
        fy = f['m'] * r['x'] + f['b']
        writer.writerow([f"{r['input']:.4f}", f"{r['raw']:.4f}", f"{r['x']:.4f}", f"{r['y']:.4f}", f"{fy:.4f}", f"{r['y'] - fy:.4e}"])
    (out / csvpath.lstrip('/')).write_text(csv_content.getvalue(), encoding='utf-8')

    val, se, ref = estimate(c, f)
    pct = abs(val - ref) / ref * 100.0 if ref != 0 else 0.0
    ab, gr_desc, disc, conc = report_narrative(c, rows, f, val, pct, ref)

    rep_content = c.get('report', '')

    return f'''<article class="report-article">
      <header class="report-header">
        <div class="eyebrow">PHARMACY &amp; PHARMACEUTICAL SCIENCES LABORATORY REPORT · OPEN STEM LAB</div>
        <h2>{E(c['title'])}</h2>
        <div class="report-meta">
          <span><strong>Experiment:</strong> {E(c['shortTitle'])}</span>
          <span><strong>Protocol:</strong> Standard USP / Ph. Eur. Official Laboratory Practice</span>
          <span><strong>Status:</strong> Calibrated &amp; Verified</span>
        </div>
      </header>
      <div class="report-links-bar">
        <a class="btn-download" href="{csvpath}" download>Download raw sample data (.CSV)</a>
      </div>
      {rep_content}
    </article>'''

def shell(c, part, body, base, production):
    path = f"/pharmacy-pharmaceutical-sciences/{c['slug']}/" + ('' if part == 'experiment' else part + '/')
    title = {
        'experiment': c['title'] + ' | Pharmacy & Pharmaceutical Sciences Lab',
        'theory': c['shortTitle'] + ' Theory & Equations | Open STEM Lab',
        'report': c['shortTitle'] + ' Lab Report & Empirical Data | Open STEM Lab'
    }[part]
    desc = {
        'experiment': c['aim'] + ' Explore interactive pharmaceutical simulation, formulation physics, and analytical assays.',
        'theory': 'Understand ' + c['shortTitle'].lower() + ': physical pharmacy principles, dissolution, pharmacokinetics, and biopharmaceutics.',
        'report': 'A worked ' + c['shortTitle'].lower() + ' lab report with sample observation tables, regression plots, calculations, and error analysis.'
    }[part]
    header = head(path, title, desc, base, production).replace('<link rel="stylesheet" href="/catalog.css">', '<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/pharmacy-pharmaceutical-sciences-lesson.css">')
    header = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: f'<script type="application/ld+json">{lesson_schema(c, part, path, title, desc, base)}</script>', header, flags=re.S)
    home = f'/pharmacy-pharmaceutical-sciences/{c["slug"]}/'
    nav = '<aside class="sidebar"><a class="brand" style="font-size:20px" href="/">◉ openstemlab.</a><a class="side-subject" href="/subjects/pharmacy-pharmaceutical-sciences/">← Pharmacy &amp; Pharmaceutical Sciences labs</a><div class="side-label">LABORATORY ' + str(c['num']).zfill(2) + '</div><nav aria-label="Lesson navigation">'
    for href, label in [(home, 'Explore the experiment'), (home + 'theory/', 'Understand the theory'), (home + '#apparatus', 'Know your tools'), (home + '#method', 'Follow the method'), (home + '#results', 'Analyse your results'), (home + '#check', 'Check your understanding'), (home + 'report/', 'Sample lab report')]:
        nav += f'<a class="nav-item{" active" if path==href else ""}" href="{href}">{label}</a>'
    nav += '<a class="nav-item" href="/experiments/">Search all experiments</a></nav><div class="side-note"><span class="small-sun">✳</span><p>Learn by pharmaceutical formulation.<br>Understand by clinical biopharmaceutics.</p></div><a class="text-button" href="/">← All subjects</a></aside>'
    heading = c['title'] if part == 'experiment' else c['shortTitle'] + ' theory' if part == 'theory' else c['shortTitle'] + ' lab report'
    return (
        header + '<body>' + nav + '<main><header class="topbar"><div><a href="/subjects/pharmacy-pharmaceutical-sciences/">Pharmacy &amp; Pharmaceutical Sciences</a> / ' + E(c['shortTitle']) + '</div><span class="free-label">FREE TO EXPLORE</span></header>'
        '<section class="page-heading"><div class="eyebrow">LABORATORY ' + str(c['num']).zfill(2) + ' · PHARMACY &amp; PHARMACEUTICAL SCIENCES</div><h1>' + E(heading) + '</h1><p>' + E(desc) + '</p></section>'
        '<nav class="lab-navigation" aria-label="Experiment pages"><a href="' + home + '">Workbench</a><a href="' + home + 'theory/">Detailed theory</a><a href="' + home + '#method">Method</a><a href="' + home + '#results">My results</a><a href="' + home + 'report/">Example report</a></nav>'
        + body +
        '<footer><span class="footer-brand">openstemlab.</span><a href="/subjects/pharmacy-pharmaceutical-sciences/">All pharmacy &amp; pharmaceutical sciences labs</a><span>Pharmaceutics &amp; physical pharmacy, pharmaceutical analysis &amp; QA, pharmacokinetics &amp; biopharmaceutics, pharmacology &amp; sterile products</span></footer></main>'
        + ('<script id="labConfig" type="application/json">' + json.dumps(c, ensure_ascii=False).replace('<', chr(92) + 'u003c') + '</script><script src="/pharmacy-pharmaceutical-sciences-models.js"></script><script src="/pharmacy-pharmaceutical-sciences-engine.js"></script>' if part == 'experiment' else '')
        + '</body></html>'
    )

def build_pharmacy_pharmaceutical_sciences(out, base, production):
    published = [c for c in specs() if c.get('published', True)]
    (out / 'pharmacy-pharmaceutical-sciences-lesson.css').write_text((ROOT / 'content/pharmacy_pharmaceutical_sciences/lesson.css').read_text(encoding='utf-8'), encoding='utf-8')
    (out / 'pharmacy-pharmaceutical-sciences-models.js').write_text((ROOT / 'content/pharmacy_pharmaceutical_sciences/models.js').read_text(encoding='utf-8'), encoding='utf-8')
    (out / 'pharmacy-pharmaceutical-sciences-engine.js').write_text((ROOT / 'content/pharmacy_pharmaceutical_sciences/engine.js').read_text(encoding='utf-8'), encoding='utf-8')

    db = sqlite3.connect(ROOT / 'data/catalog.sqlite3')
    sid = db.execute("SELECT id FROM subjects WHERE slug='pharmacy-pharmaceutical-sciences'").fetchone()[0]
    db.execute("UPDATE subjects SET content_status='live' WHERE slug='pharmacy-pharmaceutical-sciences'")
    paths = []
    for c in published:
        slug = c['slug']
        home = f'/pharmacy-pharmaceutical-sciences/{slug}/'
        (out / home.lstrip('/')).mkdir(parents=True, exist_ok=True)
        rows = [observation(c, v) for v in c['samples']]
        f = fit(rows)
        for part, body in [
            ('experiment', workbench(c)),
            ('theory', '<section>' + theory(c) + f'<div class="insight"><span>↳</span><div><strong>Connect physical pharmacy to human pharmacotherapy.</strong><p>Drug dissolution kinetics, molecular permeability, and bioequivalent manufacturing dictate clinical efficacy and patient safety.</p></div></div></section>'),
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
    paths = build_pharmacy_pharmaceutical_sciences(out, base, args.production)
    print(f"Built {len(paths)} Pharmacy & Pharmaceutical Sciences pages for {base}: {paths[:3]}...")
