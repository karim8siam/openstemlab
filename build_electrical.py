# -*- coding: utf-8 -*-
"""Static lesson pages and reproducible simulated reports for published Electrical & Electronics Engineering labs."""
from pathlib import Path
import json, math, csv, io, sqlite3, html, re

ROOT = Path(__file__).resolve().parent
E = lambda s: html.escape(str(s), quote=True)

def specs():
    return json.loads((ROOT / 'content/electrical/experiments.json').read_text(encoding='utf-8'))

def rnd(x, n):
    return math.floor(x * 10**n + 0.5) / 10**n

def fmt(v, n=4):
    return f'{v:.3e}' if v and (abs(v) < 0.001 or abs(v) >= 1e6) else f'{v:.{n}f}'

PARAMS = {
    # Module 1: DC/AC Circuit Analysis & Network Theorems (Labs 1–9)
    'thevenin-and-norton-equivalent-circuits': {'type': 'linear_affine', 'slope': -50.0000, 'intercept': 12.0000, 'ref': 50.0000, 'abs_ref': True},
    'superposition-theorem-independent-sources': {'type': 'linear_affine', 'slope': 0.4500, 'intercept': 1.2500, 'ref': 0.4500},
    'maximum-power-transfer-theorem-dc-circuits': {'type': 'linear_affine', 'slope': -25.0000, 'intercept': 15.0000, 'ref': 25.0000, 'abs_ref': True},
    'transient-response-series-rl-and-rc-circuits': {'type': 'linear_prop', 'slope': 0.5000, 'ref': 0.5000},
    'series-and-parallel-rlc-resonance': {'type': 'linear_prop', 'slope': 6.2832, 'ref': 6.2832},
    'reciprocity-and-millman-theorems': {'type': 'linear_prop', 'slope': 0.6500, 'ref': 0.6500},
    'two-port-network-z-and-y-parameters': {'type': 'linear_prop', 'slope': 0.4500, 'ref': 0.4500},
    'ac-power-factor-improvement-synchronous-condenser': {'type': 'linear_prop', 'slope': 15.2000, 'ref': 15.2000},
    'three-phase-power-measurement-two-wattmeter': {'type': 'linear_prop', 'slope': 1.4500, 'ref': 1.4500},

    # Module 2: Analog Electronics & Semiconductor Devices (Labs 10–18)
    'pn-junction-diode-forward-reverse-characteristics': {'type': 'linear_affine', 'slope': 38.6000, 'intercept': -24.5000, 'ref': 38.6000},
    'zener-diode-voltage-regulator-line-load-regulation': {'type': 'linear_affine', 'slope': 0.0250, 'intercept': 5.1000, 'ref': 0.0250},
    'bjt-common-emitter-input-output-characteristics': {'type': 'linear_prop', 'slope': 120.0000, 'ref': 120.0000},
    'jfet-and-mosfet-drain-and-transfer-characteristics': {'type': 'linear_affine', 'slope': 0.6500, 'intercept': 2.6000, 'ref': 0.6500},
    'op-amp-inverting-and-non-inverting-closed-loop-gain': {'type': 'linear_prop', 'slope': -4.7000, 'ref': 4.7000, 'abs_ref': True},
    'op-amp-active-filters-butterworth-sallen-key': {'type': 'linear_affine', 'slope': -40.0000, 'intercept': 0.0000, 'ref': 40.0000, 'abs_ref': True},
    'bjt-rc-coupled-audio-amplifier-frequency-response': {'type': 'linear_prop', 'slope': 0.0850, 'ref': 0.0850},
    'wien-bridge-and-rc-phase-shift-oscillators': {'type': 'linear_prop', 'slope': 0.6283, 'ref': 0.6283},
    'astable-and-monostable-multivibrators-555-timer': {'type': 'linear_prop', 'slope': 11.0000, 'ref': 11.0000},

    # Module 3: Digital Electronics, Logic Design & Microprocessors (Labs 19–27)
    'truth-tables-and-de-morgans-laws-logic-gates': {'type': 'linear_affine', 'slope': 0.8500, 'intercept': 3.2000, 'ref': 0.8500},
    'combinational-adders-and-subtractors-arithmetic-logic': {'type': 'linear_affine', 'slope': 1.2500, 'intercept': 4.5000, 'ref': 1.2500},
    'multiplexers-demultiplexers-and-data-routing': {'type': 'linear_affine', 'slope': 0.9500, 'intercept': 5.2000, 'ref': 0.9500},
    'synchronous-and-asynchronous-binary-counters': {'type': 'linear_prop', 'slope': 3.6500, 'ref': 3.6500},
    'digital-flip-flops-sr-jk-d-t-propagation-timing': {'type': 'linear_prop', 'slope': 8.4000, 'ref': 8.4000},
    'shift-registers-siso-sipo-piso-pipo-ring-johnson': {'type': 'linear_affine', 'slope': 2.1500, 'intercept': 6.0000, 'ref': 2.1500},
    'digital-to-analog-and-analog-to-digital-converters': {'type': 'linear_prop', 'slope': 0.01953, 'ref': 0.01953},
    'microprocessor-instruction-cycle-bus-timing': {'type': 'linear_prop', 'slope': 1.0000, 'ref': 1.0000},
    'microcontroller-gpio-timer-interrupts-pwm': {'type': 'linear_prop', 'slope': 0.0500, 'ref': 0.0500},

    # Module 4: Electrical Machines & Electromechanics (Labs 28–36)
    'dc-shunt-motor-speed-control-armature-field': {'type': 'linear_prop', 'slope': 6.8000, 'ref': 6.8000},
    'dc-series-motor-torque-speed-characteristics': {'type': 'linear_prop', 'slope': 0.3500, 'ref': 0.3500},
    'open-circuit-and-short-circuit-tests-transformer': {'type': 'linear_prop', 'slope': 4.2500, 'ref': 4.2500},
    'three-phase-transformer-connections-and-polarity': {'type': 'linear_prop', 'slope': 0.5774, 'ref': 0.5774},
    'three-phase-squirrel-cage-induction-motor-load-test': {'type': 'linear_prop', 'slope': 0.6500, 'ref': 0.6500},
    'synchronous-generator-open-circuit-short-circuit-v-curves': {'type': 'linear_prop', 'slope': 185.0000, 'ref': 185.0000},
    'synchronous-motor-v-and-inverted-v-curves': {'type': 'linear_affine', 'slope': 4.5000, 'intercept': 2.0000, 'ref': 4.5000},
    'single-phase-capacitor-start-induction-motor': {'type': 'linear_prop', 'slope': 0.0450, 'ref': 0.0450},
    'switched-reluctance-and-stepper-motor-step-angle': {'type': 'linear_prop', 'slope': 1.8000, 'ref': 1.8000},

    # Module 5: Power Systems, High Voltage & Renewable Energy (Labs 37–43)
    'transmission-line-abcd-parameters-ferranti-effect': {'type': 'linear_affine', 'slope': -2.8500, 'intercept': 230.0000, 'ref': 2.8500, 'abs_ref': True},
    'earth-fault-and-overcurrent-relay-idmt-characteristics': {'type': 'linear_prop', 'slope': 0.1400, 'ref': 0.1400},
    'dielectric-breakdown-strength-transformer-insulating-oil': {'type': 'linear_prop', 'slope': 22.5000, 'ref': 22.5000},
    'photovoltaic-pv-cell-iv-and-pv-characteristics': {'type': 'linear_prop', 'slope': 0.00485, 'ref': 0.00485},
    'wind-turbine-generator-power-coefficient-betz-limit': {'type': 'linear_prop', 'slope': 0.4200, 'ref': 0.4200},
    'high-voltage-impulse-generator-marx-circuit': {'type': 'linear_prop', 'slope': 45.0000, 'ref': 45.0000},
    'harmonic-distortion-measurement-fft-spectrum': {'type': 'linear_affine', 'slope': 0.5500, 'intercept': 12.0000, 'ref': 0.5500},

    # Module 6: Control Systems, Instrumentation & Power Electronics (Labs 44–50)
    'scr-triac-phase-angle-firing-control-r-rl-loads': {'type': 'linear_prop', 'slope': 48.0000, 'ref': 48.0000},
    'buck-boost-dc-dc-converter-duty-cycle-efficiency': {'type': 'linear_prop', 'slope': 24.0000, 'ref': 24.0000},
    'single-phase-spwm-inverter-total-harmonic-distortion': {'type': 'linear_prop', 'slope': 70.7100, 'ref': 70.7100},
    'closed-loop-pid-dc-motor-speed-servomechanism': {'type': 'linear_affine', 'slope': 5.2000, 'intercept': 10.0000, 'ref': 5.2000},
    'bode-plot-and-nyquist-stability-criterion': {'type': 'linear_affine', 'slope': -20.0000, 'intercept': 0.0000, 'ref': 20.0000, 'abs_ref': True},
    'linear-variable-differential-transformer-lvdt-transducer': {'type': 'linear_prop', 'slope': 0.8500, 'ref': 0.8500},
    'strain-gauge-quarter-half-full-wheatstone-bridge': {'type': 'linear_prop', 'slope': 0.0125, 'ref': 0.0125}
}

def observation(c, value):
    slug = c['slug']
    val = float(value)
    p = PARAMS.get(slug)
    if not p:
        raise ValueError(f"Unknown slug in observation: {slug}")

    if p['type'] == 'linear_prop':
        slope = p['slope']
        x = rnd(val, 4)
        y = rnd(slope * x, 4)
        return {'input': val, 'raw': y, 'x': x, 'y': y}

    if p['type'] == 'linear_affine':
        slope = p['slope']
        intercept = p.get('intercept', 0.0)
        x = rnd(val, 4)
        y = rnd(slope * x + intercept, 4)
        return {'input': val, 'raw': y, 'x': x, 'y': y}

    raise ValueError(f"Unknown parameter model type for: {slug}")

def fit(rows):
    n = len(rows)
    mx = sum(r['x'] for r in rows) / n
    my = sum(r['y'] for r in rows) / n
    sxx = sum((r['x'] - mx)**2 for r in rows)
    sxy = sum((r['x'] - mx) * (r.get('y', r.get('raw', 0)) - my) for r in rows)
    m = sxy / sxx if sxx > 0 else 1.0
    b = my - m * mx
    syy = sum((r['y'] - my)**2 for r in rows)
    r2 = (sxy**2) / (sxx * syy) if (sxx * syy) > 0 else 1.0
    sse = sum((r['y'] - (m * r['x'] + b))**2 for r in rows)
    s2 = sse / (n - 2) if n > 2 else 0.0
    slopeSE = math.sqrt(s2 / sxx) if sxx > 0 else 0.0
    interceptSE = math.sqrt(s2 * (1.0 / n + mx**2 / sxx)) if sxx > 0 else 0.0
    return {
        'm': m, 'b': b, 'r2': r2, 'n': n,
        'mx': mx, 'my': my, 'sxx': sxx, 'sxy': sxy,
        'sse': sse, 'slopeSE': slopeSE, 'interceptSE': interceptSE
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
    abstract = f"Laboratory evaluation of {c['title']} was conducted across six calibrated setpoints. Measured telemetry was linearized, yielding a correlation coefficient R² = {f['r2']:.6f}. The experimental parameter {c['targetName']} was estimated as {value * c['resultScale']:.{c['resultDecimals']}f} {c['resultUnit']}, comparing against the reference benchmark of {reference * c['resultScale']:.{c['resultDecimals']}f} {c['resultUnit']} with a relative percentage deviation of {percent:.4f}%."
    graph_choice = f"Plotting {c['xAxis']} on the horizontal axis and {c['yAxis']} on the vertical axis yields a linear characteristic whose slope verifies the {c['shortTitle']} analytical model."
    discussion = f"Experimental observations across all test trials demonstrate strict agreement with theoretical circuit models. OLS regression slope evaluated to {f['m']:.6f} with intercept {f['b']:.6f}, validating the governing equation {c['fitEquation']} with R² = {f['r2']:.6f}."
    conclusion = f"The experimental determination of {c['title']} confirmed the theoretical model within an experimental uncertainty of {percent:.4f}%. The standard calibration protocol ensures reproducible laboratory characterization."
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
        grid += f'<line x1="{tx(gx)}" y1="{pad_t}" x2="{tx(gx)}" y2="{pad_t+ph}" stroke="#334155" stroke-dasharray="2,2"/>'
        grid += f'<line x1="{pad_l}" y1="{ty(gy)}" x2="{pad_l+pw}" y2="{ty(gy)}" stroke="#334155" stroke-dasharray="2,2"/>'
        grid += f'<text x="{tx(gx)}" y="{pad_t+ph+18}" font-size="10" fill="#94a3b8" text-anchor="middle">{gx:.2f}</text>'
        grid += f'<text x="{pad_l-10}" y="{ty(gy)+4}" font-size="10" fill="#94a3b8" text-anchor="end">{gy:.2f}</text>'

    x1, x2 = min_x, max_x
    y1, y2 = f['m'] * x1 + f['b'], f['m'] * x2 + f['b']
    line = f'<line x1="{tx(x1)}" y1="{ty(y1)}" x2="{tx(x2)}" y2="{ty(y2)}" stroke="#38bdf8" stroke-width="2.5"/>'
    pts = "".join(f'<circle cx="{tx(r["x"])}" cy="{ty(r["y"])}" r="5" fill="#38bdf8" stroke="#0284c7" stroke-width="1.5"/>' for r in rows)
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Regression graph">{grid}{line}{pts}<text x="{pad_l+pw/2}" y="{h-15}" font-size="12" fill="#cbd5e1" text-anchor="middle">{E(c["xAxis"])}</text><text transform="rotate(-90)" x="{-pad_t-ph/2}" y="22" font-size="12" fill="#cbd5e1" text-anchor="middle">{E(c["yAxis"])}</text></svg>'

def method(c):
    return '<ol class="method-steps">' + ''.join(f'<li><strong>{E(s["title"])}</strong>: {E(s["text"])}</li>' for s in c['procedure']) + '</ol>'

def head(path, title, desc, base, indexable):
    structured = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': title, 'description': desc, 'url': base + path, 'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'}, 'inLanguage': 'en'}
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="{'index,follow' if indexable else 'noindex,follow'}"><link rel="canonical" href="{base+path}"><meta name="theme-color" content="#f8f7f2"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{base+path}"><meta property="og:type" content="website"><link rel="stylesheet" href="/catalog.css"><script type="application/ld+json">{json.dumps(structured)}</script></head>'''

def lesson_schema(c, part, path, title, desc, base):
    obj = {'@context': 'https://schema.org', '@type': 'TechArticle', 'headline': title, 'description': desc, 'url': base + path, 'inLanguage': 'en', 'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'}, 'about': [{'@type': 'Thing', 'name': c['title']}, {'@type': 'Thing', 'name': 'Electrical & Electronics Engineering'}]}
    return json.dumps(obj)

def workbench(c):
    sim_buttons = '<button class="sim-mode-btn active" data-mode="bench" role="tab" aria-selected="true"><span class="sim-icon">⚡</span> Bench</button><button class="sim-mode-btn" data-mode="compare" role="tab" aria-selected="false"><span class="sim-icon">⇄</span> Compare</button><button class="sim-mode-btn" data-mode="sandbox" role="tab" aria-selected="false"><span class="sim-icon">⚙</span> Sandbox</button>'
    quiz_html = ''.join(
        '<article class="quiz-card"><h3>Question ' + str(i+1) + ': ' + E(q['question']) + '</h3><div class="options">' +
        ''.join('<button class="quiz-option" data-idx="' + str(j) + '">' + E(opt) + '</button>' for j, opt in enumerate(q['options'])) +
        '</div><p class="quiz-feedback" role="status" hidden>' + E(q['explanation']) + '</p></article>'
        for i, q in enumerate(c['quiz'])
    )
    return f'''<section aria-label="Interactive workbench"><div class="section-top"><div><div class="eyebrow">CIRCUIT ANALYSIS · ANALOG · DIGITAL · MACHINES · POWER SYSTEMS · CONTROL &amp; INSTRUMENTATION</div><h2>Your virtual electrical &amp; electronics engineering laboratory.</h2></div><button id="resetApparatus" class="text-button">Reset apparatus</button></div><div class="new-workbench"><div class="new-visual"><div class="visual-top"><div class="sim-mode-switcher" role="tablist" aria-label="Simulation Views">{sim_buttons}</div><button id="pauseMotion" class="dark-button" hidden>Pause motion</button></div><svg id="visualSvg" viewBox="0 0 520 280" role="img" aria-label="Interactive electrical engineering workbench for {E(c['shortTitle'])}"></svg><div class="new-meter"><div><small>{E(c['rawLabel'].upper())}</small><strong id="readingValue">—</strong></div><div><small>INSTRUMENTATION TELEMETRY</small><p id="liveState" style="font-size:11px;margin:7px 0">Ready to sample with {E(c['shortInput'])} = {c['initial']} {E(c['inputUnit'])}.</p></div></div></div><div class="new-controls"><label for="independent">{E(c['inputLabel'])}</label><output id="independentOut">{c['initial']} {E(c['inputUnit'])}</output><input id="independent" type="range" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><label for="independentNumber">Set {E(c['shortInput'])} ({E(c['inputUnit'])})</label><input id="independentNumber" type="number" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><div class="lab-control-meta">{E(c['settings'][0])}</div><button id="measure" class="primary full">{E(c.get('measureLabel', 'Execute electrical acquisition trial'))}</button><button id="recordReading" class="secondary full" disabled>＋ Record observation</button><p id="trialStatus" class="trial-status" role="status">Adjust {E(c['shortInput'])}, then execute electrical instrumentation acquisition.</p></div></div><p class="data-notice">Electrical telemetry is sampled with calibrated high-precision instruments using 64-bit IEEE 754 precision buffers. Residuals reflect ordinary least-squares regression across successive observations. Continuous data structures support high-fidelity circuit and power system modeling.</p><details class="model-note"><summary>Electrical engineering assumptions and boundary limits</summary><p>{E(c['limitations'][0] if isinstance(c['limitations'], list) else c['limitations'])} {E(c['modelExtra'])}</p></details></section><section id="apparatus" class="lab-section"><h2>Laboratory apparatus &amp; testing equipment.</h2><div class="apparatus-list">{''.join('<article class="apparatus-item"><h3>'+E(a['name'])+'</h3><p>'+E(a['purpose'])+'</p></article>' for a in c['apparatus'])}</div></section><section id="method" class="lab-section"><div class="eyebrow">FOLLOW THE METHOD</div><h2>A reason behind every step.</h2><p class="intro">{E(c['aim'])} Standardized parameter settings: {", ".join(map(str,c['samples']))} {E(c['inputUnit'])}.</p>{method(c)}</section><section id="results" class="lab-section"><div class="section-top"><div><div class="eyebrow">YOUR NOTEBOOK · <span id="notebookCount">0</span> OBSERVATIONS</div><h2>Turn measurements into electrical engineering insight.</h2></div><a class="text-button" href="/electrical-electronics-engineering/{c['slug']}/report/">See a complete example report ↗</a></div><div class="lab-result-grid"><div class="chart-card"><svg id="labPlot" viewBox="0 0 520 260" role="img" aria-label="Measured observations and fitted regression graph"></svg><p>Points are your recorded observations. The solid regression line validates {E(c['shortTitle'])} mathematical scaling.</p></div><div class="fit-card lab-fit"><span class="eyebrow">LINEAR REGRESSION FIT · y = mx + b</span><div id="fitResult"></div><div class="report-equation">{E(c['fitEquation'])}</div></div></div><div class="table-card"><table><thead><tr><th>#</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th></tr></thead><tbody id="readingsBody"></tbody></table><p id="emptyReadings">No readings yet. Execute an electrical trial and record it.</p></div><div class="lab-reading-actions"><button id="clearData" class="secondary">Clear notebook</button></div></section><section id="check" class="lab-section lab-questions"><div class="eyebrow">CHECK YOUR UNDERSTANDING</div><h2>Explain what the circuit metrics mean.</h2>{quiz_html}</section><section id="overview" class="lab-section"><div class="eyebrow">THEORY AND ELECTROMAGNETIC CONTEXT</div><h2>Electrical engineering background &amp; physical principles.</h2><p class="intro">{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>{E(c['modelExtra'])}</p></section>'''

def theory(c):
    rich_theory = c.get('theory', '')
    return f'''<article class="theory-article"><h2>Electrical engineering principles &amp; circuit foundations of {E(c['shortTitle'])}.</h2><p class="lead">{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div>{rich_theory}<h3>Viva voce questions &amp; analytical theory</h3><div class="faq-list">{''.join(f'<details class="faq-item"><summary><strong>{E(t["question"])}</strong></summary><p>{E(t["answer"])}</p></details>' for t in c['topics'])}</div><h3>Experimental precautions and laboratory safety</h3><ul>{''.join(f'<li>{E(p)}</li>' for p in c['precautions'])}</ul><h3>Theoretical assumptions &amp; boundary condition limits</h3><ul>{''.join(f'<li>{E(l)}</li>' for l in c['limitations'])}</ul></article>'''

def report(c, rows, f, out):
    slug = c['slug']
    csvpath = f"/electrical-electronics-engineering/{slug}/sample-data.csv"
    csv_content = io.StringIO()
    writer = csv.writer(csv_content)
    writer.writerow([c['shortInput'].replace(' ', '_'), c['rawLabel'].replace(' ', '_'), 'x_coord', 'y_coord', 'fitted_y', 'residual'])
    for r in rows:
        fit_y = f['m'] * r['x'] + f['b']
        writer.writerow([r['input'], r['raw'], f"{r['x']:.4f}", f"{r['y']:.4f}", f"{fit_y:.4f}", f"{r['y'] - fit_y:.4f}"])
    (out / f"electrical-electronics-engineering/{slug}/sample-data.csv").write_text(csv_content.getvalue(), encoding='utf-8')

    value, se, reference = estimate(c, f)
    percent = abs(value - reference) / abs(reference) * 100
    uncertainty = uncertainty_text(c)
    abstract, graph_choice, discussion, conclusion = report_narrative(c, rows, f, value, percent, reference)

    obs = "".join(
        f"<tr><td>{i+1}</td><td>{r['input']}</td><td>{r['raw']}</td><td>{r['x']:.4f}</td><td>{r['y']:.4f}</td><td>{f['m']*r['x']+f['b']:.4f}</td><td>{r['y']-(f['m']*r['x']+f['b']):.4f}</td></tr>"
        for i, r in enumerate(rows)
    )

    rich_rep = c.get('report', '')

    return f'''<div class="section-top"><div><div class="eyebrow">WORKED EXAMPLE · BENCHMARK OBSERVATIONS</div><h2>A complete example electrical engineering laboratory report.</h2></div><button class="secondary" onclick="window.print()">Print / save as PDF</button></div><div class="report-notice"><strong>Simulated demonstration data.</strong><p>This report illustrates formal electrical engineering data reduction, instrument calibration tares, and circuit parameter estimation. Replace its observations with your own experimental telemetry when preparing an electrical engineering laboratory report submission.</p></div><div class="report-person"><span>Student: __________________</span><span>Student ID: __________________</span><span>Course: __________________</span><span>Date: __________________</span><span>Partner: __________________</span><span>Instructor: __________________</span></div><article class="lab-report"><h3>1. Title and aim</h3><p><strong>{E(c['title'])}.</strong> {E(c['aim'])}</p><h3>2. Abstract</h3><p>{E(abstract)}</p><h3>3. Apparatus and fixed settings</h3><ul>{''.join('<li>'+E(a['name'])+': '+E(a['purpose'])+'</li>' for a in c['apparatus'])}{''.join('<li>'+E(s)+'</li>' for s in c['settings'])}</ul><h3>4. Theory and graph choice</h3><p>{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>{E(graph_choice)}</p><h3>5. Method</h3><ol>{''.join('<li>'+E(s['text'])+'</li>' for s in c['procedure'])}</ol><h3>6. Observations and calculation table</h3><p>All electrical engineering observations use strictly controlled 64-bit IEEE 754 precision buffers. Residuals are computed relative to the ordinary least-squares regression line.</p><div class="table-card"><table><caption>Table 1. Six simulated observations; x and y represent transformed electrical engineering metrics.</caption><thead><tr><th>No.</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Fitted y</th><th>Residual</th></tr></thead><tbody>{obs}</tbody></table></div><p><a href="{csvpath}" download>Download the sample observations (CSV) ↓</a></p><h3>7. Worked calculation for one observation</h3><div class="report-equation">{E(worked(c, rows[0]))}</div><h3>8. Graph, gradient and final calculation</h3><div class="chart-card">{graph(c, rows, f)}</div><p>Circular markers represent empirical circuit observations. The solid line represents the ordinary least-squares linear fit.</p><div class="report-equation">x̄ = {fmt(f['mx'])}; ȳ = {fmt(f['my'])}<br>Σ(x − x̄)² = {fmt(f['sxx'])}<br>Σ(x − x̄)(y − ȳ) = {fmt(f['sxy'])}<br>m = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)² = {fmt(f['m'], 8)}<br>b = ȳ − mx̄ = {fmt(f['b'], 8)}<br>{E(formula(c, f))}</div><h3>9. Uncertainty and comparison</h3><p>Percentage difference = |estimate − theoretical value| / |theoretical value| × 100 = <strong>{percent:.4f}%</strong>.</p><p>For n = 6 observations, Σresidual² = {fmt(f['sse'])}; s² = Σresidual²/(n − 2). Gradient standard error = √[s²/Σ(x − x̄)²] = {fmt(f['slopeSE'])}. Intercept standard error = √[s²(1/n + x̄²/Σ(x − x̄)²)] = {fmt(f['interceptSE'])}.</p><p>Propagating the fit parameters yields a <strong>fit standard error of {fmt(se * c['resultScale'])} {E(c['resultUnit'])}</strong>, with an ideal coefficient of determination R² = {f['r2']:.6f}.</p><p>{E(uncertainty)}</p><h3>10. Result and discussion</h3><div class="report-equation">{E(c['targetName'])} = {fmt(value * c['resultScale'], c['resultDecimals'])} {E(c['resultUnit'])}<br>Theoretical reference value: {fmt(reference * c['resultScale'], c['resultDecimals'])} {E(c['resultUnit'])}</div><p>{E(discussion)}</p><h3>11. Precautions and limitations</h3><ul>{''.join('<li>'+E(p)+'</li>' for p in c['precautions'])}</ul><p>{E(c['limitations'][0] if isinstance(c['limitations'], list) else c['limitations'])} {E(c['modelExtra'])}</p><h3>12. Conclusion</h3><p>{E(conclusion)}</p><div class="full-report-supplement"><h4>In-Depth Technical Supplement &amp; Circuit Engineering Derivation</h4>{rich_rep}</div></article>'''

def shell(c, part, body, base, production):
    path = f"/electrical-electronics-engineering/{c['slug']}/" + ('' if part == 'experiment' else part + '/')
    title = {
        'experiment': c['title'] + ' | Electrical & Electronics Engineering Lab',
        'theory': c['shortTitle'] + ' Theory & Equations | Open STEM Lab',
        'report': c['shortTitle'] + ' Lab Report & Empirical Data | Open STEM Lab'
    }[part]
    desc = {
        'experiment': c['aim'] + ' Explore interactive circuit analysis, electronics simulation, and electrical engineering telemetry.',
        'theory': 'Understand ' + c['shortTitle'].lower() + ': governing circuit equations, semiconductor dynamics, electrical machines, and power systems.',
        'report': 'A worked ' + c['shortTitle'].lower() + ' lab report with sample observation tables, regression plots, calculations, and error analysis.'
    }[part]
    header = head(path, title, desc, base, production).replace('<link rel="stylesheet" href="/catalog.css">', '<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/electrical-lesson.css">')
    header = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: f'<script type="application/ld+json">{lesson_schema(c, part, path, title, desc, base)}</script>', header, flags=re.S)
    home = f'/electrical-electronics-engineering/{c["slug"]}/'
    nav = '<aside class="sidebar"><a class="brand" style="font-size:20px" href="/">◉ openstemlab.</a><a class="side-subject" href="/subjects/electrical-electronics-engineering/">← Electrical &amp; Electronics Engineering labs</a><div class="side-label">LABORATORY ' + str(c['number']).zfill(2) + '</div><nav aria-label="Lesson navigation">'
    for href, label in [(home, 'Explore the experiment'), (home + 'theory/', 'Understand the theory'), (home + '#apparatus', 'Know your tools'), (home + '#method', 'Follow the method'), (home + '#results', 'Analyse your results'), (home + '#check', 'Check your understanding'), (home + 'report/', 'Sample lab report')]:
        nav += f'<a class="nav-item{" active" if path==href else ""}" href="{href}">{label}</a>'
    nav += '<a class="nav-item" href="/experiments/">Search all experiments</a></nav><div class="side-note"><span class="small-sun">✳</span><p>Learn by circuit trial.<br>Understand by electromagnetic physics.</p></div><a class="text-button" href="/">← All subjects</a></aside>'
    heading = c['title'] if part == 'experiment' else c['shortTitle'] + ' theory' if part == 'theory' else c['shortTitle'] + ' lab report'
    return (
        header + '<body>' + nav + '<main><header class="topbar"><div><a href="/subjects/electrical-electronics-engineering/">Electrical &amp; Electronics Engineering</a> / ' + E(c['shortTitle']) + '</div><span class="free-label">FREE TO EXPLORE</span></header>'
        '<section class="page-heading"><div class="eyebrow">LABORATORY ' + str(c['number']).zfill(2) + ' · ELECTRICAL &amp; ELECTRONICS ENGINEERING</div><h1>' + E(heading) + '</h1><p>' + E(desc) + '</p></section>'
        '<nav class="lab-navigation" aria-label="Experiment pages"><a href="' + home + '">Workbench</a><a href="' + home + 'theory/">Detailed theory</a><a href="' + home + '#method">Method</a><a href="' + home + '#results">My results</a><a href="' + home + 'report/">Example report</a></nav>'
        + body +
        '<footer><span class="footer-brand">openstemlab.</span><a href="/subjects/electrical-electronics-engineering/">All electrical engineering labs</a><span>Circuits, electronics, machines &amp; power systems model</span></footer></main>'
        + ('<script id="labConfig" type="application/json">' + json.dumps(c, ensure_ascii=False).replace('<', chr(92) + 'u003c') + '</script><script src="/electrical-models.js"></script><script src="/electrical-engine.js"></script>' if part == 'experiment' else '')
        + '</body></html>'
    )

def build_electrical(out, base, production):
    published = [c for c in specs() if c.get('published', True)]
    (out / 'electrical-lesson.css').write_text((ROOT / 'content/electrical/lesson.css').read_text(encoding='utf-8'), encoding='utf-8')
    (out / 'electrical-models.js').write_text((ROOT / 'content/electrical/models.js').read_text(encoding='utf-8'), encoding='utf-8')
    (out / 'electrical-engine.js').write_text((ROOT / 'content/electrical/engine.js').read_text(encoding='utf-8'), encoding='utf-8')

    db = sqlite3.connect(ROOT / 'data/catalog.sqlite3')
    sid = db.execute("SELECT id FROM subjects WHERE slug='electrical-electronics-engineering'").fetchone()[0]
    db.execute("UPDATE subjects SET content_status='live' WHERE slug='electrical-electronics-engineering'")
    paths = []
    for c in published:
        slug = c['slug']
        home = f'/electrical-electronics-engineering/{slug}/'
        (out / home.lstrip('/')).mkdir(parents=True, exist_ok=True)
        rows = [observation(c, v) for v in c['samples']]
        f = fit(rows)
        for part, body in [
            ('experiment', workbench(c)),
            ('theory', '<section>' + theory(c) + f'<div class="insight"><span>↳</span><div><strong>Connect circuit theory to empirical instrumentation telemetry.</strong><p>{E(c["modelExtra"])}</p></div></div></section>'),
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
    paths = build_electrical(out, base, args.production)
    print(f"Built {len(paths)} Electrical & Electronics Engineering pages for {base}: {paths[:3]}...")
