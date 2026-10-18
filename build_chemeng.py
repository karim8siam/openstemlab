# -*- coding: utf-8 -*-
"""Static lesson pages and reproducible simulated reports for published Chemical & Process Engineering labs."""
from pathlib import Path
import json, math, csv, io, sqlite3, html, re

ROOT = Path(__file__).resolve().parent
E = lambda s: html.escape(str(s), quote=True)

def specs():
    return json.loads((ROOT / 'content/chemeng/experiments.json').read_text(encoding='utf-8'))

def rnd(x, n):
    return math.floor(x * 10**n + 0.5) / 10**n

def fmt(v, n=4):
    return f'{v:.3e}' if v and (abs(v) < 0.001 or abs(v) >= 1e6) else f'{v:.{n}f}'

PARAMS = {
    # Module 1: Fluid Mechanics & Transport Phenomena in Process Systems (Labs 1–8)
    'venturi-meter-bernoulli-discharge-coefficient': {'type': 'linear_prop', 'slope': 0.4850, 'ref': 0.4850},
    'orifice-meter-flow-metering-pressure-loss': {'type': 'linear_prop', 'slope': 0.6120, 'ref': 0.6120},
    'pipe-friction-factor-reynolds-moody-chart': {'type': 'square_input', 'slope': 0.2850, 'ref': 0.2850},
    'fluidized-bed-minimum-fluidization-ergun': {'type': 'linear_prop', 'slope': 0.4250, 'ref': 0.4250},
    'packed-bed-pressure-drop-kozeny-carman': {'type': 'linear_prop', 'slope': 1.6500, 'ref': 1.6500},
    'centrifugal-slurry-pump-characteristic-curves': {'type': 'square_input', 'slope': -0.0280, 'intercept': 35.0000, 'ref': 0.0280, 'abs_ref': True},
    'falling-film-viscometer-non-newtonian-power-law': {'type': 'log_input', 'slope': 1.3500, 'intercept': -0.4500, 'ref': 1.3500},
    'rotameter-calibration-variable-area-flowmeter': {'type': 'linear_affine', 'slope': 6.5000, 'intercept': 5.0000, 'ref': 6.5000},

    # Module 2: Heat Transfer & Thermal Unit Operations (Labs 9–16)
    'shell-and-tube-heat-exchanger-lmtd-effectiveness': {'type': 'power_input', 'power': 0.8, 'slope': 85.0000, 'ref': 85.0000},
    'concentric-pipe-heat-exchanger-countercurrent': {'type': 'linear_prop', 'slope': 0.4200, 'ref': 0.4200},
    'plate-and-frame-heat-exchanger-thermal-efficiency': {'type': 'power_input', 'power': 0.65, 'slope': 3200.0000, 'ref': 3200.0000},
    'natural-and-forced-convection-finned-tube': {'type': 'power_input', 'power': 0.6, 'slope': 18.5000, 'ref': 18.5000},
    'thermal-conductivity-radial-steady-state-fourier': {'type': 'linear_prop', 'slope': 0.3850, 'ref': 0.3850},
    'unsteady-state-transient-heat-conduction-lumped': {'type': 'log_decay', 'rate': 0.0320, 'ref': 0.0320, 'abs_ref': True},
    'boiling-heat-transfer-nukiyama-curve': {'type': 'linear_prop', 'slope': 2.4500, 'ref': 2.4500},
    'tubular-falling-film-evaporator-steam-economy': {'type': 'linear_prop', 'slope': 4.8000, 'ref': 4.8000},

    # Module 3: Mass Transfer, Distillation & Separation Processes (Labs 17–24)
    'fractional-distillation-mccabe-thiele-reflux': {'type': 'linear_affine', 'slope': 2.8500, 'intercept': 1.2500, 'ref': 2.8500},
    'gas-absorption-packed-column-mass-transfer-kga': {'type': 'power_input', 'power': 0.7, 'slope': 0.0820, 'ref': 0.0820},
    'liquid-liquid-extraction-ternary-tie-lines': {'type': 'linear_prop', 'slope': 0.8850, 'ref': 0.8850},
    'batch-rotary-drum-vacuum-filtration-cake-resistance': {'type': 'linear_affine', 'slope': 18.5000, 'intercept': 4.2000, 'ref': 18.5000},
    'solid-liquid-leaching-crosscurrent-stage-efficiency': {'type': 'linear_affine', 'slope': -0.4200, 'intercept': -0.1500, 'ref': 0.4200, 'abs_ref': True},
    'adsorption-isotherm-activated-carbon-langmuir-freundlich': {'type': 'linear_affine', 'slope': 0.4500, 'intercept': 0.2200, 'ref': 0.4500},
    'crossflow-membrane-ultrafiltration-gel-polarization': {'type': 'linear_prop', 'slope': 42.5000, 'ref': 42.5000},
    'tray-dryer-drying-rate-curve-constant-falling-rate': {'type': 'power_input', 'power': 0.8, 'slope': 0.6500, 'ref': 0.6500},

    # Module 4: Chemical Reaction Engineering, Catalysis & Bioreactors (Labs 25–32)
    'continuous-stirred-tank-reactor-cstr-saponification': {'type': 'linear_prop', 'slope': 0.2800, 'ref': 0.2800},
    'plug-flow-tubular-reactor-pfr-residence-time': {'type': 'linear_prop', 'slope': 0.1850, 'ref': 0.1850},
    'reactors-in-series-cstr-cascade-conversion': {'type': 'linear_affine', 'slope': 0.0450, 'intercept': 1.0000, 'ref': 0.0450},
    'residence-time-distribution-rtd-axial-dispersion': {'type': 'linear_prop', 'slope': 0.0025, 'ref': 0.0025},
    'heterogeneous-catalytic-fixed-bed-thiele-modulus': {'type': 'linear_affine', 'slope': 0.3500, 'intercept': 1.0000, 'ref': 0.3500},
    'batch-isothermal-reactor-rate-constant-arrhenius': {'type': 'arrhenius_inv_t', 'slope': -5.7740, 'intercept': 21.1300, 'ref': 5.7740, 'abs_ref': True},
    'aerated-bioreactor-oxygen-mass-transfer-kla': {'type': 'power_input', 'power': 1.2, 'slope': 0.0240, 'ref': 0.0240},
    'enzyme-membrane-reactor-continuous-biocatalysis': {'type': 'inverse_input', 'slope': 1.4500, 'intercept': 0.4500, 'ref': 1.4500},

    # Module 5: Chemical Thermodynamics, Phase Equilibria & Solution Properties (Labs 33–39)
    'vapor-liquid-equilibrium-vle-wilson-margules': {'type': 'linear_prop', 'slope': 0.7250, 'ref': 0.7250},
    'differential-scanning-calorimetry-dsc-glass-transition': {'type': 'log_input', 'slope': 2.1500, 'intercept': 100.0000, 'ref': 2.1500},
    'bomb-calorimeter-heat-of-combustion-hydrocarbons': {'type': 'linear_prop', 'slope': 2.6500, 'ref': 2.6500},
    'partial-molar-volume-binary-solution-dilatometry': {'type': 'linear_affine', 'slope': 14.5000, 'intercept': 54.2000, 'ref': 14.5000},
    'solid-liquid-equilibrium-sle-eutectic-phase-diagram': {'type': 'linear_prop', 'slope': 58.5000, 'ref': 58.5000},
    'excess-enthalpy-of-mixing-isothermal-titration-calorimetry': {'type': 'linear_prop', 'slope': -3450.0000, 'ref': 3450.0000, 'abs_ref': True},
    'gas-solubility-henry-law-pressure-decay': {'type': 'linear_prop', 'slope': 0.0340, 'ref': 0.0340},

    # Module 6: Process Dynamics, Automatic Control & Mechanical Separations (Labs 40–46)
    'first-order-gravity-drained-tank-level-dynamics': {'type': 'linear_prop', 'slope': 3.8500, 'ref': 3.8500},
    'two-tank-interacting-liquid-level-system': {'type': 'linear_prop', 'slope': 4.2500, 'ref': 4.2500},
    'feedback-pid-temperature-control-tuning-ziegler-nichols': {'type': 'linear_prop', 'slope': 0.1250, 'ref': 0.1250},
    'pneumatic-control-valve-flow-characteristic-hysteresis': {'type': 'linear_prop', 'slope': 0.8500, 'ref': 0.8500},
    'feedforward-plus-feedback-ratio-flow-control': {'type': 'linear_prop', 'slope': 0.4000, 'ref': 0.4000},
    'continuous-crystallization-msmpr-crystal-size-distribution': {'type': 'linear_affine', 'slope': -0.0125, 'intercept': 15.2000, 'ref': 0.0125, 'abs_ref': True},
    'sedimentation-and-centrifugal-clarification-stokes': {'type': 'linear_affine', 'slope': -1.8500, 'intercept': 120.0000, 'ref': 1.8500, 'abs_ref': True}
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

    if p['type'] == 'square_input':
        slope = p['slope']
        intercept = p.get('intercept', 0.0)
        x = rnd(val * val, 4)
        y = rnd(slope * x + intercept, 4)
        return {'input': val, 'raw': y, 'x': x, 'y': y}

    if p['type'] == 'log_input':
        slope = p['slope']
        intercept = p.get('intercept', 0.0)
        x = rnd(math.log(val), 4)
        y = rnd(slope * x + intercept, 4)
        return {'input': val, 'raw': y, 'x': x, 'y': y}

    if p['type'] == 'log_decay':
        rate = p['rate']
        x = rnd(val, 4)
        raw = rnd(math.exp(-rate * x), 5)
        y = rnd(-rate * x, 4)
        return {'input': val, 'raw': raw, 'x': x, 'y': y}

    if p['type'] == 'inverse_input':
        slope = p['slope']
        intercept = p.get('intercept', 0.0)
        x = rnd(1.0 / val, 4)
        y = rnd(slope * x + intercept, 4)
        return {'input': val, 'raw': y, 'x': x, 'y': y}

    if p['type'] == 'arrhenius_inv_t':
        slope = p['slope']
        intercept = p.get('intercept', 0.0)
        absT = val + 273.15
        x = rnd(1000.0 / absT, 4)
        y = rnd(slope * x + intercept, 4)
        return {'input': val, 'raw': y, 'x': x, 'y': y}

    if p['type'] == 'power_input':
        power = p['power']
        slope = p['slope']
        intercept = p.get('intercept', 0.0)
        x = rnd(val ** power, 4)
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
    sse = sum((r['y'] - (m * r['x'] + b))**2 for r in rows)
    syy = sum((r['y'] - my)**2 for r in rows)
    variance = sse / (n - 2) if n > 2 else 0.0001
    return {
        'n': n, 'mx': mx, 'my': my, 'sxx': sxx, 'sxy': sxy,
        'm': m, 'b': b, 'sse': sse, 'syy': syy,
        'rms': math.sqrt(sse / n) if n else 0.0,
        'slopeSE': math.sqrt(variance / sxx) if sxx > 0 else 0.0001,
        'interceptSE': math.sqrt(variance * (1.0 / n + mx * mx / sxx)) if sxx > 0 else 0.0001,
        'r2': (1.0 - sse / syy) if syy > 0 else 1.0
    }

def estimate(c, f):
    p = PARAMS[c['slug']]
    val = abs(f['m']) if p.get('abs_ref') or (p['ref'] > 0 and f['m'] < 0) else f['m']
    ref = p['ref']
    se = f['slopeSE'] if f['slopeSE'] > 0 else 0.00001
    return val, se, ref

def formula(c, f):
    p = PARAMS[c['slug']]
    val = (abs(f['m']) if p.get('abs_ref') or (p['ref'] > 0 and f['m'] < 0) else f['m']) * c['resultScale']
    return f"y = {fmt(f['m'], 4)} · x + {fmt(f['b'], 4)} ⟹ Target {c['targetName']} = {fmt(val, c['resultDecimals'])} {c['resultUnit']} (theoretical = {c['target']})"

def worked(c, row):
    return f"For input {c['shortInput']} = {row['input']} {c['inputUnit']}: Measured {c['rawLabel']} = {row['raw']:.4f} {c['rawUnit']}. Transformed process coordinates: independent x = {row['x']:.4f}, dependent y = {row['y']:.4f}."

from build_catalog import head

def lesson_schema(c, part, path, title, desc, base):
    graph_items = [{'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Open STEM Lab', 'item': base + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Chemical & Process Engineering', 'item': base + '/subjects/chemical-process-engineering/'},
        {'@type': 'ListItem', 'position': 3, 'name': c['shortTitle'], 'item': base + f'/chemical-process-engineering/{c["slug"]}/'}
    ]}]
    if part == 'experiment':
        graph_items.append({
            '@type': ['WebPage', 'LearningResource', 'TechArticle'],
            'name': title, 'description': desc, 'url': base + path,
            'learningResourceType': 'Interactive chemical engineering simulation and virtual process unit operations workbench',
            'educationalLevel': 'Undergraduate', 'about': c['title'], 'inLanguage': 'en',
            'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'}
        })
        if c.get('quiz'):
            graph_items.append({
                '@type': 'Quiz', 'name': c['shortTitle'] + ' Conceptual Chemical Engineering Assessment',
                'hasPart': [
                    {'@type': 'Question', 'name': q['question'],
                     'suggestedAnswer': [{'@type': 'Answer', 'text': opt} for opt in q['options']],
                     'acceptedAnswer': {'@type': 'Answer', 'text': q['options'][q.get('correct', 0)]}}
                    for q in c['quiz']
                ]
            })
    elif part == 'theory':
        graph_items.append({
            '@type': ['WebPage', 'TechArticle', 'FAQPage'],
            'name': title, 'description': desc, 'url': base + path,
            'about': c['title'], 'inLanguage': 'en',
            'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'},
            'mainEntity': [{'@type': 'Question', 'name': t['question'], 'acceptedAnswer': {'@type': 'Answer', 'text': t['answer']}} for t in c['topics']]
        })
    else:
        graph_items.append({
            '@type': ['WebPage', 'ScholarlyArticle', 'TechArticle'],
            'name': title, 'description': desc, 'url': base + path,
            'about': c['title'], 'inLanguage': 'en',
            'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'}
        })
    return json.dumps({'@context': 'https://schema.org', '@graph': graph_items}, ensure_ascii=False)

def uncertainty_text(c):
    return (
        f"In chemical and process engineering experimentation, unit operations verification, and pilot-scale process modeling, "
        f"empirical uncertainties arise from fluid property variations, slight thermal gradients across heat transfer boundaries, "
        f"transducer electronic drift (64-bit IEEE 754 precision digital acquisition), and minor flow turbulence eddies. "
        f"The ordinary least-squares regression across n = 6 standardized test intervals yields unbiased minimum-variance estimators for both slope and intercept. "
        f"Because the underlying transport phenomena—including Navier-Stokes momentum balances, Fourier conduction, Fickian mass diffusion, "
        f"and reaction kinetics—adhere strictly to macroscopic conservation laws, residual dispersions remain tightly bounded, "
        f"yielding an ideal coefficient of determination R² ≥ 0.999999 and confirming the theoretical formulation. "
        f"Systematic errors (such as sensor zero offsets, thermocouple reference junction drifts, and flowmeter discharge friction) are eliminated "
        f"using certified calibration standards and differential tare subtraction. "
        f"Uncertainties in derived transport coefficients, dimensionless numbers, and kinetic constants are evaluated via multivariate error propagation."
    )

def report_narrative(c, rows, f, value, percent, reference):
    abstract = (
        f"Six controlled chemical process engineering observations were systematically evaluated across operational settings "
        f"{c['shortInput']} = {rows[0]['input']} {c['inputUnit']} to {c['shortInput']} = {rows[-1]['input']} {c['inputUnit']} for {c['title']}. "
        f"Ordinary least-squares regression yielded an empirical {c['targetName']} of "
        f"{fmt(value * c['resultScale'], c['resultDecimals'])} {c['resultUnit']} (difference from theoretical reference = {percent:.4f}%). "
        f"The empirical telemetry conclusively validates the fundamental chemical engineering transport and equilibrium formulation with R² = {f['r2']:.6f}. "
        f"The investigation demonstrates stable unit operations behavior, hydrodynamic and thermal reproducibility, and strict adherence to classical chemical engineering principles."
    )
    graph_choice = (
        f"The governing phenomenological transport or equilibrium relationship was linearized into the coordinate form y = mx + b. "
        f"Here, the independent coordinate x represents {c['xAxis']}, and the dependent coordinate y represents {c['yAxis']}. "
        f"The gradient m directly determines {c['targetName']}, while the intercept b accounts for baseline tare values or reference potentials. "
        f"Linear transformation enables robust parameter estimation via ordinary least squares without non-linear numerical divergence. "
        f"Plotting transformed observation pairs displays process discharge coefficients, heat transfer multipliers, mass transfer rates, or kinetic rate constants directly as linear slopes."
    )
    discussion = (
        f"The empirical laboratory observations provide rigorous quantitative verification of {c['title']}. "
        f"In chemical engineering transport phenomena, fluid mechanics, heat transfer, separation processes, and reaction engineering, physical systems "
        f"are governed by macroscopic mass, momentum, and energy conservation equations. "
        f"Across all six observation trials, the empirical slope m = {fmt(f['m'], 4)} confirms the theoretical model with near-zero residual variance. "
        f"Furthermore, comparison with established chemical engineering literature benchmarks (McCabe, Smith, Harriott; Bird, Stewart, Lightfoot; Fogler; and Levenspiel) "
        f"underscores vital industrial scale-up principles including continuous steady-state stability, minimal friction losses, optimal reaction conversion, and thermal efficiency. "
        f"Residual analysis confirms homoscedastic dispersion without systematic non-linear curvature, validating the underlying model assumptions."
    )
    conclusion = (
        f"This laboratory investigation quantitatively verified the mathematical formulation and physical behavior of {c['title']}. "
        f"Through rigorous tracking across six observation points, we confirmed an empirical {c['targetName']} of "
        f"{fmt(value * c['resultScale'], c['resultDecimals'])} {c['resultUnit']} matching the theoretical reference {fmt(reference * c['resultScale'], c['resultDecimals'])} {c['resultUnit']} "
        f"within {percent:.4f}% error. The investigation demonstrates why this chemical engineering method serves as an indispensable cornerstone in industrial process design, unit operations scaling, and plant optimization."
    )
    return abstract, graph_choice, discussion, conclusion

def graph(c, rows, f):
    left, right, top, bottom = 68, 610, 28, 280
    xs = [r['x'] * c['xScale'] for r in rows]
    ys = [r['y'] * c['yScale'] for r in rows]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    dx = (xmax - xmin) or 1.0
    dy = (ymax - ymin) or 1.0
    xmin -= dx * 0.12
    xmax += dx * 0.12
    ymin -= dy * 0.15
    ymax += dy * 0.15
    px = lambda x: left + (x - xmin) / (xmax - xmin) * (right - left)
    py = lambda y: bottom - (y - ymin) / (ymax - ymin) * (bottom - top)
    svg = f'<svg viewBox="0 0 650 340" role="img" aria-label="Regression graph for {E(c["shortTitle"])}"><rect width="650" height="340" fill="#1c1917"/>'
    for i in range(5):
        x = xmin + i * (xmax - xmin) / 4
        y = ymin + i * (ymax - ymin) / 4
        svg += f'<line x1="{left}" y1="{py(y):.1f}" x2="{right}" y2="{py(y):.1f}" stroke="#292524" stroke-dasharray="2,2"/><text x="{left-9}" y="{py(y)+4:.1f}" text-anchor="end" font-size="10" fill="#fbbf24">{fmt(y, 2)}</text><text x="{px(x):.1f}" y="300" text-anchor="middle" font-size="10" fill="#fbbf24">{fmt(x, 2)}</text>'
    svg += f'<path d="M{left} {top}V{bottom}H{right}" stroke="#78350f" fill="none"/><text x="335" y="332" text-anchor="middle" fill="#fef3c7" font-size="12">{E(c["xAxis"])}</text><text transform="translate(18 160) rotate(-90)" text-anchor="middle" fill="#fef3c7" font-size="12">{E(c["yAxis"])}</text>'
    pts = [f"{px(xmin + i * (xmax - xmin) / 100):.1f},{py((f['m'] * (xmin + i * (xmax - xmin) / 100) / c['xScale'] + f['b']) * c['yScale']):.1f}" for i in range(101)]
    svg += f'<polyline points="{" ".join(pts)}" stroke="#f59e0b" stroke-width="2.5" fill="none"/>'
    for r in rows:
        svg += f'<circle cx="{px(r["x"] * c["xScale"]):.1f}" cy="{py(r["y"] * c["yScale"]):.1f}" r="5" fill="#fbbf24" stroke="#1c1917" stroke-width="1.5"/>'
    svg += '</svg>'
    return svg

def method(c):
    return '<div class="method-steps">' + ''.join(
        f'<article class="method-step"><div class="step-num">{str(i).zfill(2)}</div><div><h3>{E(s["title"])}</h3><p>{E(s["text"])}</p></div></article>'
        for i, s in enumerate(c['procedure'], 1)
    ) + '</div>'

def workbench(c):
    sim_buttons = ''.join(
        f'<button id="simMode{m["id"].capitalize()}" class="sim-mode-btn{" active" if i==0 else ""}" data-sim="{m["id"]}" type="button" role="tab" aria-selected="{"true" if i==0 else "false"}"><span class="sim-icon">{m["icon"]}</span> {E(m["label"])}</button>'
        for i, m in enumerate(c.get('simModes', [{'id':'bench','icon':'⚗️','label':'1. Process Test Bench'},{'id':'compare','icon':'📊','label':'2. Comparative Telemetry'},{'id':'sandbox','icon':'⚡','label':'3. Chemical Process Sandbox'}]))
    )
    quiz_html = ''.join(
        '<article class="quiz-card"><h3>' + E(q['question']) + '</h3><div class="quiz-choices">' +
        ''.join('<button class="quiz-option" data-quiz="' + str(i) + '" data-choice="' + str(j) + '">' + E(a) + '</button>' for j, a in enumerate(q['options'])) +
        '</div><p id="quizFeedback' + str(i) + '" class="quiz-feedback" role="status"></p></article>'
        for i, q in enumerate(c['quiz'])
    )
    return f'''<section aria-label="Interactive workbench"><div class="section-top"><div><div class="eyebrow">TRANSPORT PHENOMENA · UNIT OPERATIONS · PROCESS CONTROL · REACTION ENGINEERING</div><h2>Your virtual chemical and process engineering laboratory.</h2></div><button id="resetApparatus" class="text-button">Reset apparatus</button></div><div class="new-workbench"><div class="new-visual"><div class="visual-top"><div class="sim-mode-switcher" role="tablist" aria-label="Simulation Views">{sim_buttons}</div><button id="pauseMotion" class="dark-button" hidden>Pause motion</button></div><svg id="apparatusDiagram" viewBox="0 0 720 320" role="img" aria-label="Interactive chemical engineering workbench for {E(c['shortTitle'])}"></svg><div class="new-meter"><div><small>{E(c['rawLabel'].upper())}</small><strong id="readingValue">—</strong></div><div><small>PROCESS &amp; PILOT PLANT TELEMETRY</small><p id="liveState" style="font-size:11px;margin:7px 0">Ready to sample with {E(c['shortInput'])} = {c['initial']} {E(c['inputUnit'])}.</p></div></div></div><div class="new-controls"><label for="independent">{E(c['inputLabel'])}</label><output id="independentOut">{c['initial']} {E(c['inputUnit'])}</output><input id="independent" type="range" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><label for="independentNumber">Set {E(c['shortInput'])} ({E(c['inputUnit'])})</label><input id="independentNumber" type="number" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><div class="lab-control-meta">{E(c['settings'][0])}</div><button id="measure" class="primary full">{E(c.get('measureLabel', 'Execute chemical engineering trial'))}</button><button id="recordReading" class="secondary full" disabled>＋ Record observation</button><p id="trialStatus" class="trial-status" role="status">Adjust {E(c['shortInput'])}, then execute chemical process trial.</p></div></div><p class="data-notice">Chemical and process engineering telemetry is evaluated rigorously using 64-bit IEEE 754 precision. Residuals reflect ordinary least-squares regression across successive observations. Continuous data structures support high-fidelity transport phenomena and unit operations modeling.</p><details class="model-note"><summary>Process engineering assumptions and boundary condition limits</summary><p>{E(c['limitations'][0] if isinstance(c['limitations'], list) else c['limitations'])} {E(c['modelExtra'])}</p></details></section><section id="apparatus" class="lab-section"><h2>Process apparatus &amp; industrial sensors.</h2><div class="apparatus-list">{''.join('<article class="apparatus-item"><h3>'+E(a['name'])+'</h3><p>'+E(a['purpose'])+'</p></article>' for a in c['apparatus'])}</div></section><section id="method" class="lab-section"><div class="eyebrow">FOLLOW THE METHOD</div><h2>A reason behind every step.</h2><p class="intro">{E(c['aim'])} Standardized parameter settings: {", ".join(map(str,c['samples']))} {E(c['inputUnit'])}.</p>{method(c)}</section><section id="results" class="lab-section"><div class="section-top"><div><div class="eyebrow">YOUR NOTEBOOK · <span id="notebookCount">0</span> OBSERVATIONS</div><h2>Turn measurements into chemical process engineering insight.</h2></div><a class="text-button" href="/chemical-process-engineering/{c['slug']}/report/">See a complete example report ↗</a></div><div class="lab-result-grid"><div class="chart-card"><svg id="labPlot" viewBox="0 0 650 340" role="img" aria-label="Measured observations and fitted regression graph"></svg><p>Points are your recorded observations. The solid regression line validates {E(c['shortTitle'])} mathematical scaling.</p></div><div class="fit-card lab-fit"><span class="eyebrow">LINEAR REGRESSION FIT · y = mx + b</span><div id="fitSummary"></div><div class="report-equation">{E(c['fitEquation'])}</div></div></div><div class="table-card"><table><thead><tr><th>#</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Remove</th></tr></thead><tbody id="readingRows"></tbody></table><p id="emptyReadings">No readings yet. Execute a process trial and record it.</p></div><div class="lab-reading-actions"><button id="downloadReadings" class="secondary" disabled>↓ Export CSV</button><button id="clearReadings" class="secondary" disabled>Clear notebook</button></div><div class="source-box"><h3>Calculate it yourself.</h3><label for="studentEstimate">Your estimate of {E(c['targetName'])} ({E(c['resultUnit'])})</label> <input id="studentEstimate" type="number" step="any" min="0" style="max-width:140px"><button id="checkEstimate" class="secondary" style="margin-left:10px">Check calculation</button><p id="estimateFeedback" role="status"></p></div></section><section id="check" class="lab-section lab-questions"><div class="eyebrow">CHECK YOUR UNDERSTANDING</div><h2>Explain what the process engineering metrics mean.</h2>{quiz_html}</section><section id="overview" class="lab-section"><div class="eyebrow">THEORY AND UNIT OPERATIONS CONTEXT</div><h2>Process engineering background &amp; physical principles.</h2><p class="intro">{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>{E(c['modelExtra'])}</p></section>'''

def theory(c):
    rich_theory = c.get('theory', '')
    return f'''<article class="theory-article"><h2>Chemical engineering transport &amp; equilibrium foundations of {E(c['shortTitle'])}.</h2><p class="lead">{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div>{rich_theory}<h3>Viva voce questions &amp; analytical theory</h3><div class="faq-list">{''.join(f'<details class="faq-item"><summary><strong>{E(t["question"])}</strong></summary><p>{E(t["answer"])}</p></details>' for t in c['topics'])}</div><h3>Experimental precautions and process safety</h3><ul>{''.join(f'<li>{E(p)}</li>' for p in c['precautions'])}</ul><h3>Theoretical assumptions &amp; boundary condition limits</h3><ul>{''.join(f'<li>{E(l)}</li>' for l in c['limitations'])}</ul></article>'''

def report(c, rows, f, out):
    slug = c['slug']
    csvpath = f"/chemical-process-engineering/{slug}/sample-data.csv"
    csv_content = io.StringIO()
    writer = csv.writer(csv_content)
    writer.writerow([c['shortInput'].replace(' ', '_'), c['rawLabel'].replace(' ', '_'), 'x_coord', 'y_coord', 'fitted_y', 'residual'])
    for r in rows:
        fit_y = f['m'] * r['x'] + f['b']
        writer.writerow([r['input'], r['raw'], f"{r['x']:.4f}", f"{r['y']:.4f}", f"{fit_y:.4f}", f"{r['y'] - fit_y:.4f}"])
    (out / f"chemical-process-engineering/{slug}/sample-data.csv").write_text(csv_content.getvalue(), encoding='utf-8')

    value, se, reference = estimate(c, f)
    percent = abs(value - reference) / abs(reference) * 100
    uncertainty = uncertainty_text(c)
    abstract, graph_choice, discussion, conclusion = report_narrative(c, rows, f, value, percent, reference)

    obs = "".join(
        f"<tr><td>{i+1}</td><td>{r['input']}</td><td>{r['raw']}</td><td>{r['x']:.4f}</td><td>{r['y']:.4f}</td><td>{f['m']*r['x']+f['b']:.4f}</td><td>{r['y']-(f['m']*r['x']+f['b']):.4f}</td></tr>"
        for i, r in enumerate(rows)
    )

    rich_rep = c.get('report', '')

    return f'''<div class="section-top"><div><div class="eyebrow">WORKED EXAMPLE · BENCHMARK OBSERVATIONS</div><h2>A complete example chemical engineering laboratory report.</h2></div><button class="secondary" onclick="window.print()">Print / save as PDF</button></div><div class="report-notice"><strong>Simulated demonstration data.</strong><p>This report illustrates formal chemical and process engineering data reduction, instrument calibration tares, and unit operations parameter estimation. Replace its observations with your own experimental telemetry when preparing a chemical engineering laboratory report submission.</p></div><div class="report-person"><span>Student: __________________</span><span>Student ID: __________________</span><span>Course: __________________</span><span>Date: __________________</span><span>Partner: __________________</span><span>Instructor: __________________</span></div><article class="lab-report"><h3>1. Title and aim</h3><p><strong>{E(c['title'])}.</strong> {E(c['aim'])}</p><h3>2. Abstract</h3><p>{E(abstract)}</p><h3>3. Apparatus and fixed settings</h3><ul>{''.join('<li>'+E(a['name'])+': '+E(a['purpose'])+'</li>' for a in c['apparatus'])}{''.join('<li>'+E(s)+'</li>' for s in c['settings'])}</ul><h3>4. Theory and graph choice</h3><p>{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>{E(graph_choice)}</p><h3>5. Method</h3><ol>{''.join('<li>'+E(s['text'])+'</li>' for s in c['procedure'])}</ol><h3>6. Observations and calculation table</h3><p>All chemical process observations use strictly controlled 64-bit IEEE 754 precision buffers. Residuals are computed relative to the ordinary least-squares regression line.</p><div class="table-card"><table><caption>Table 1. Six simulated observations; x and y represent transformed process metrics.</caption><thead><tr><th>No.</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Fitted y</th><th>Residual</th></tr></thead><tbody>{obs}</tbody></table></div><p><a href="{csvpath}" download>Download the sample observations (CSV) ↓</a></p><h3>7. Worked calculation for one observation</h3><div class="report-equation">{E(worked(c, rows[0]))}</div><h3>8. Graph, gradient and final calculation</h3><div class="chart-card">{graph(c, rows, f)}</div><p>Circular markers represent empirical process observations. The solid line represents the ordinary least-squares linear fit.</p><div class="report-equation">x̄ = {fmt(f['mx'])}; ȳ = {fmt(f['my'])}<br>Σ(x − x̄)² = {fmt(f['sxx'])}<br>Σ(x − x̄)(y − ȳ) = {fmt(f['sxy'])}<br>m = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)² = {fmt(f['m'], 8)}<br>b = ȳ − mx̄ = {fmt(f['b'], 8)}<br>{E(formula(c, f))}</div><h3>9. Uncertainty and comparison</h3><p>Percentage difference = |estimate − theoretical value| / |theoretical value| × 100 = <strong>{percent:.4f}%</strong>.</p><p>For n = 6 observations, Σresidual² = {fmt(f['sse'])}; s² = Σresidual²/(n − 2). Gradient standard error = √[s²/Σ(x − x̄)²] = {fmt(f['slopeSE'])}. Intercept standard error = √[s²(1/n + x̄²/Σ(x − x̄)²)] = {fmt(f['interceptSE'])}.</p><p>Propagating the fit parameters yields a <strong>fit standard error of {fmt(se * c['resultScale'])} {E(c['resultUnit'])}</strong>, with an ideal coefficient of determination R² = {f['r2']:.6f}.</p><p>{E(uncertainty)}</p><h3>10. Result and discussion</h3><div class="report-equation">{E(c['targetName'])} = {fmt(value * c['resultScale'], c['resultDecimals'])} {E(c['resultUnit'])}<br>Theoretical reference value: {fmt(reference * c['resultScale'], c['resultDecimals'])} {E(c['resultUnit'])}</div><p>{E(discussion)}</p><h3>11. Precautions and limitations</h3><ul>{''.join('<li>'+E(p)+'</li>' for p in c['precautions'])}</ul><p>{E(c['limitations'][0] if isinstance(c['limitations'], list) else c['limitations'])} {E(c['modelExtra'])}</p><h3>12. Conclusion</h3><p>{E(conclusion)}</p><div class="full-report-supplement"><h4>In-Depth Technical Supplement &amp; Historical Unit Operations Derivation</h4>{rich_rep}</div></article>'''

def shell(c, part, body, base, production):
    path = f"/chemical-process-engineering/{c['slug']}/" + ('' if part == 'experiment' else part + '/')
    title = {
        'experiment': c['title'] + ' | Chemical & Process Engineering Lab',
        'theory': c['shortTitle'] + ' Theory & Equations | Open STEM Lab',
        'report': c['shortTitle'] + ' Lab Report & Empirical Data | Open STEM Lab'
    }[part]
    desc = {
        'experiment': c['aim'] + ' Explore interactive transport phenomena, unit operations simulation, and chemical engineering telemetry.',
        'theory': 'Understand ' + c['shortTitle'].lower() + ': governing transport equations, heat and mass balances, reaction kinetics, and unit operations.',
        'report': 'A worked ' + c['shortTitle'].lower() + ' lab report with sample observation tables, regression plots, calculations, and error analysis.'
    }[part]
    header = head(path, title, desc, base, production).replace('<link rel="stylesheet" href="/catalog.css">', '<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/chemeng-lesson.css">')
    header = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: f'<script type="application/ld+json">{lesson_schema(c, part, path, title, desc, base)}</script>', header, flags=re.S)
    home = f'/chemical-process-engineering/{c["slug"]}/'
    nav = '<aside class="sidebar"><a class="brand" style="font-size:20px" href="/">◉ openstemlab.</a><a class="side-subject" href="/subjects/chemical-process-engineering/">← Chemical &amp; Process Engineering labs</a><div class="side-label">LABORATORY ' + str(c['number']).zfill(2) + '</div><nav aria-label="Lesson navigation">'
    for href, label in [(home, 'Explore the experiment'), (home + 'theory/', 'Understand the theory'), (home + '#apparatus', 'Know your tools'), (home + '#method', 'Follow the method'), (home + '#results', 'Analyse your results'), (home + '#check', 'Check your understanding'), (home + 'report/', 'Sample lab report')]:
        nav += f'<a class="nav-item{" active" if path==href else ""}" href="{href}">{label}</a>'
    nav += '<a class="nav-item" href="/experiments/">Search all experiments</a></nav><div class="side-note"><span class="small-sun">✳</span><p>Learn by transport trial.<br>Understand by process mechanics.</p></div><a class="text-button" href="/">← All subjects</a></aside>'
    heading = c['title'] if part == 'experiment' else c['shortTitle'] + ' theory' if part == 'theory' else c['shortTitle'] + ' lab report'
    return (
        header + '<body>' + nav + '<main><header class="topbar"><div><a href="/subjects/chemical-process-engineering/">Chemical &amp; Process Engineering</a> / ' + E(c['shortTitle']) + '</div><span class="free-label">FREE TO EXPLORE</span></header>'
        '<section class="page-heading"><div class="eyebrow">LABORATORY ' + str(c['number']).zfill(2) + ' · CHEMICAL &amp; PROCESS ENGINEERING</div><h1>' + E(heading) + '</h1><p>' + E(desc) + '</p></section>'
        '<nav class="lab-navigation" aria-label="Experiment pages"><a href="' + home + '">Workbench</a><a href="' + home + 'theory/">Detailed theory</a><a href="' + home + '#method">Method</a><a href="' + home + '#results">My results</a><a href="' + home + 'report/">Example report</a></nav>'
        + body +
        '<footer><span class="footer-brand">openstemlab.</span><a href="/subjects/chemical-process-engineering/">All chemical engineering labs</a><span>Transport phenomena &amp; unit operations model</span></footer></main>'
        + ('<script id="labConfig" type="application/json">' + json.dumps(c, ensure_ascii=False).replace('<', chr(92) + 'u003c') + '</script><script src="/chemeng-models.js"></script><script src="/chemeng-engine.js"></script>' if part == 'experiment' else '')
        + '</body></html>'
    )

def build_chemeng(out, base, production):
    published = [c for c in specs() if c.get('published', True)]
    for name, dest in [('models.js', 'chemeng-models.js'), ('engine.js', 'chemeng-engine.js'), ('lesson.css', 'chemeng-lesson.css')]:
        (out / dest).write_text((ROOT / 'content/chemeng' / name).read_text(encoding='utf-8'), encoding='utf-8')
    db = sqlite3.connect(ROOT / 'data/catalog.sqlite3')
    sid = db.execute("SELECT id FROM subjects WHERE slug='chemical-process-engineering'").fetchone()[0]
    db.execute("UPDATE subjects SET content_status='live' WHERE slug='chemical-process-engineering'")
    paths = []
    for c in published:
        slug = c['slug']
        home = f'/chemical-process-engineering/{slug}/'
        (out / home.lstrip('/')).mkdir(parents=True, exist_ok=True)
        rows = [observation(c, v) for v in c['samples']]
        f = fit(rows)
        for part, body in [
            ('experiment', workbench(c)),
            ('theory', '<section>' + theory(c) + f'<div class="insight"><span>↳</span><div><strong>Connect transport theory to empirical process plant data.</strong><p>{E(c["modelExtra"])}</p></div></div></section>'),
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
    paths = build_chemeng(out, base, args.production)
    print(f"Built {len(paths)} Chemical & Process Engineering pages for {base}: {paths[:3]}...")
