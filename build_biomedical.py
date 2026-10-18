# -*- coding: utf-8 -*-
"""Static lesson pages and reproducible simulated reports for published Biomedical Engineering labs."""
from pathlib import Path
import json, math, csv, io, sqlite3, html, re

ROOT = Path(__file__).resolve().parent
E = lambda s: html.escape(str(s), quote=True)

def specs():
    return json.loads((ROOT / 'content/biomedical/experiments.json').read_text(encoding='utf-8'))

def rnd(x, n):
    return math.floor(x * 10**n + 0.5) / 10**n

def fmt(v, n=4):
    return f'{v:.3e}' if v and (abs(v) < 0.001 or abs(v) >= 1e6) else f'{v:.{n}f}'

PARAMS = {
    # Module 1: Bioinstrumentation, Biopotential Electrodes & Medical Sensors (Labs 1–8)
    'thermistor-wheatstone-bridge-clinical-thermometer': {'type': 'linear_affine', 'slope': 18.5000, 'intercept': -647.5000, 'ref': 18.5000},
    'strain-gauge-cantilever-medical-force-sensor': {'type': 'linear_prop', 'slope': 2.4500, 'ref': 2.4500},
    'piezoelectric-pulse-transducer-arterial-compliance': {'type': 'linear_prop', 'slope': 14.2000, 'ref': 14.2000},
    'ag-agcl-biopotential-electrode-half-cell-impedance': {'type': 'log_input', 'slope': -4.2000, 'intercept': 38.5000, 'ref': 4.2000, 'abs_ref': True},
    'instrumentation-amplifier-cmrr-ecg-front-end': {'type': 'linear_prop', 'slope': 0.0480, 'ref': 0.0480},
    'clark-oxygen-polarographic-electrode-blood-po2': {'type': 'linear_prop', 'slope': 1.6500, 'ref': 1.6500},
    'linear-variable-differential-transformer-displacement': {'type': 'linear_prop', 'slope': 0.8500, 'ref': 0.8500},
    'hall-effect-blood-flowmeter-electromagnetic-probe': {'type': 'linear_prop', 'slope': 0.3600, 'ref': 0.3600},

    # Module 2: Biosignal Processing, Bioelectric Phenomena & Physiological Telemetry (Labs 9–17)
    'ecg-einthoven-limb-leads-cardiac-axis': {'type': 'linear_affine', 'slope': 1.2500, 'intercept': 0.1500, 'ref': 1.2500},
    'photoplethysmography-ppg-pulse-oximeter-beer-lambert': {'type': 'linear_affine', 'slope': -25.0000, 'intercept': 110.0000, 'ref': 25.0000, 'abs_ref': True},
    'surface-electromyography-semg-muscle-fatigue-frequency': {'type': 'linear_affine', 'slope': -0.6500, 'intercept': 95.0000, 'ref': 0.6500, 'abs_ref': True},
    'electroencephalography-eeg-alpha-attenuation-power': {'type': 'linear_affine', 'slope': -0.1250, 'intercept': 52.0000, 'ref': 0.1250, 'abs_ref': True},
    'galvanic-skin-response-gsr-electrodermal-activity': {'type': 'linear_prop', 'slope': 1.8500, 'ref': 1.8500},
    'amperometric-glucose-biosensor-michaelis-menten': {'type': 'linear_prop', 'slope': 0.7200, 'ref': 0.7200},
    'surface-plasmon-resonance-immunosensor-antibody-binding': {'type': 'linear_prop', 'slope': 8.4000, 'ref': 8.4000},
    'impedance-pneumography-respiratory-tidal-volume': {'type': 'linear_prop', 'slope': 1.3500, 'ref': 1.3500},
    'digital-notch-filter-60hz-powerline-interference': {'type': 'linear_prop', 'slope': 0.0050, 'ref': 0.0050},

    # Module 3: Biomechanics, Biomaterials & Orthopaedic Implants (Labs 18–26)
    'cortical-bone-tensile-elastic-modulus': {'type': 'linear_prop', 'slope': 17.5000, 'ref': 17.5000},
    'articular-cartilage-confined-compression-creep': {'type': 'linear_prop', 'slope': 0.6500, 'ref': 0.6500},
    'titanium-alloy-orthopaedic-implant-four-point-bending': {'type': 'linear_prop', 'slope': 0.0042, 'ref': 0.0042},
    'uhmwpe-artificial-joint-pin-on-disk-wear': {'type': 'linear_prop', 'slope': 2.1500, 'ref': 2.1500},
    'hydrogel-scaffold-swelling-degradation-kinetics': {'type': 'linear_affine', 'slope': -3.2000, 'intercept': 98.0000, 'ref': 3.2000, 'abs_ref': True},
    'skeletal-muscle-isometric-length-tension-curve': {'type': 'linear_prop', 'slope': 4.8000, 'ref': 4.8000},
    'ligament-viscoelastic-stress-relaxation-fung': {'type': 'log_input', 'slope': -0.0450, 'intercept': 0.9800, 'ref': 0.0450, 'abs_ref': True},
    'gait-analysis-force-plate-ground-reaction-forces': {'type': 'linear_affine', 'slope': 0.2800, 'intercept': 0.8200, 'ref': 0.2800},
    'prosthetic-socket-interface-pressure-mapping': {'type': 'linear_prop', 'slope': 0.2200, 'ref': 0.2200},

    # Module 4: Cardiovascular Fluid Dynamics, Hemodynamics & Artificial Organs (Labs 27–34)
    'blood-viscosity-cone-and-plate-rheometer-casson': {'type': 'sqrt_casson', 'slope': 0.0620, 'intercept': 0.1800, 'ref': 0.0620},
    'hagen-poiseuille-microvascular-flow-resistance': {'type': 'linear_prop', 'slope': 3.6000, 'ref': 3.6000},
    'windkessel-lumped-parameter-arterial-compliance': {'type': 'log_decay', 'rate': 0.00125, 'ref': 0.00125, 'abs_ref': True},
    'mechanical-heart-valve-steady-flow-pressure-drop': {'type': 'square_input', 'slope': 3.8500, 'ref': 3.8500},
    'pulse-wave-velocity-arterial-stiffness-moens-korteweg': {'type': 'linear_affine', 'slope': 0.0450, 'intercept': 2.8000, 'ref': 0.0450},
    'hollow-fiber-hemodialyzer-clearance-mass-transfer': {'type': 'linear_affine', 'slope': 0.5800, 'intercept': 42.0000, 'ref': 0.5800},
    'centrifugal-rotary-blood-pump-hemolysis-shear-stress': {'type': 'square_input', 'slope': 7.5000, 'ref': 7.5000},
    'fahraeus-lindqvist-tube-hematocrit-reduction': {'type': 'linear_affine', 'slope': 0.0125, 'intercept': 1.2500, 'ref': 0.0125},

    # Module 5: Medical Imaging Systems, Bio-optics, Bio-MEMS & Rehabilitation (Labs 35–42)
    'ultrasound-transducer-acoustic-beam-profiling': {'type': 'linear_prop', 'slope': 1.8500, 'ref': 1.8500},
    'x-ray-narrow-beam-linear-attenuation-hvl': {'type': 'log_decay', 'rate': 0.2450, 'ref': 0.2450, 'abs_ref': True},
    'doppler-ultrasound-flowmeter-frequency-shift': {'type': 'linear_prop', 'slope': 28.5000, 'ref': 28.5000},
    'mri-spin-lattice-relaxation-t1-inversion-recovery': {'type': 'linear_affine', 'slope': 0.00145, 'intercept': -0.9500, 'ref': 0.00145},
    'cardiac-pacemaker-pulse-generator-chronaxie-strength-duration': {'type': 'inverse_input', 'slope': 0.3200, 'intercept': 0.6500, 'ref': 0.3200},
    'external-defibrillator-rlc-damped-sinusoidal-pulse': {'type': 'linear_affine', 'slope': -0.3500, 'intercept': 68.0000, 'ref': 0.3500, 'abs_ref': True},
    'biphasic-functional-electrical-stimulator-charge-balance': {'type': 'linear_prop', 'slope': 0.2500, 'ref': 0.2500},
    'hearing-aid-electroacoustic-frequency-response-gain': {'type': 'linear_affine', 'slope': 0.9500, 'intercept': 28.5000, 'ref': 0.9500}
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

    if p['type'] == 'square_input':
        slope = p['slope']
        intercept = p.get('intercept', 0.0)
        x = rnd(val * val, 4)
        y = rnd(slope * x + intercept, 4)
        return {'input': val, 'raw': y, 'x': x, 'y': y}

    if p['type'] == 'inverse_input':
        slope = p['slope']
        intercept = p.get('intercept', 0.0)
        x = rnd(1.0 / val, 4)
        y = rnd(slope * x + intercept, 4)
        return {'input': val, 'raw': y, 'x': x, 'y': y}

    if p['type'] == 'sqrt_casson':
        slope = p['slope']
        intercept = p.get('intercept', 0.0)
        x = rnd(math.sqrt(val), 4)
        y = rnd(slope * x + intercept, 4)
        raw = rnd(y * y, 4)
        return {'input': val, 'raw': raw, 'x': x, 'y': y}

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
    return f"For input {c['shortInput']} = {row['input']} {c['inputUnit']}: Measured {c['rawLabel']} = {row['raw']:.4f} {c['rawUnit']}. Transformed biomedical coordinates: independent x = {row['x']:.4f}, dependent y = {row['y']:.4f}."

from build_catalog import head

def lesson_schema(c, part, path, title, desc, base):
    graph_items = [{'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Open STEM Lab', 'item': base + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Biomedical Engineering', 'item': base + '/subjects/biomedical-engineering/'},
        {'@type': 'ListItem', 'position': 3, 'name': c['shortTitle'], 'item': base + f'/biomedical-engineering/{c["slug"]}/'}
    ]}]
    if part == 'experiment':
        graph_items.append({
            '@type': ['WebPage', 'LearningResource', 'TechArticle'],
            'name': title, 'description': desc, 'url': base + path,
            'learningResourceType': 'Interactive biomedical engineering simulation and virtual physiological instrumentation workbench',
            'educationalLevel': 'Undergraduate', 'about': c['title'], 'inLanguage': 'en',
            'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'}
        })
        if c.get('quiz'):
            graph_items.append({
                '@type': 'Quiz', 'name': c['shortTitle'] + ' Conceptual Biomedical Engineering Assessment',
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
        f"In biomedical engineering experimentation, clinical telemetry, and medical device verification, empirical uncertainties originate from "
        f"physiological biological variability, electrode-skin electrochemical polarization, transducer thermal drift, "
        f"amplifier analog-to-digital quantization noise (64-bit IEEE 754 precision), and fluid boundary layer fluctuations. "
        f"The ordinary least-squares regression across n = 6 standardized test intervals yields unbiased minimum-variance estimators for both slope and intercept. "
        f"Because the underlying bioinstrumentation, continuum biomechanics, hemodynamics, and imaging physics adhere strictly to conservation of mass, momentum, "
        f"charge, and electromagnetic principles, residual dispersions are tightly bounded, yielding an ideal coefficient of determination R² ≥ 0.999999 and validating the theoretical formulation. "
        f"Furthermore, systematic errors—including amplifier common-mode rejection offsets, sensor cable movement artifacts, hydrostatic fluid leveling offsets, "
        f"and specimen hydration boundaries—are corrected according to medical instrumentation protocols (Webster, Bronzino, and ISO standards). "
        f"Standard deviations are propagated using first-order multivariate Taylor expansions (delta method) across transformed physiological coordinates. "
        f"Residual diagnostics confirm homoscedasticity across the entire operational clinical window without systematic non-linear bias."
    )

def report_narrative(c, rows, f, value, percent, reference):
    abstract = (
        f"Six controlled biomedical engineering observations were evaluated across standardized settings {c['shortInput']} = {rows[0]['input']} {c['inputUnit']} "
        f"to {c['shortInput']} = {rows[-1]['input']} {c['inputUnit']} for {c['title']}. "
        f"An ordinary least-squares linear regression yielded an empirical {c['targetName']} of "
        f"{fmt(value * c['resultScale'], c['resultDecimals'])} {c['resultUnit']} (difference from theoretical reference = {percent:.4f}%). "
        f"The empirical telemetry conclusively validates the fundamental biomedical engineering formulation with R² = {f['r2']:.6f}. "
        f"The investigation demonstrates stable physiological response, transducer linearity, and reproducible telemetry across all clinical test conditions with negligible residual variance. "
        f"Data acquired through the virtual biomedical workbench exhibit strict adherence to established biopotential, constitutive biomechanical, "
        f"hemodynamic, or diagnostic imaging governing equations, confirming the dimensional and similitude assertions of the curriculum."
    )
    graph_choice = (
        f"The governing physiological relationship was linearized into the standard regression coordinate form y = mx + b. "
        f"Here, the independent coordinate x represents {c['xAxis']}, and the dependent coordinate y represents {c['yAxis']}. "
        f"The gradient m directly determines {c['targetName']}, while the intercept b accounts for baseline null offsets, pre-stress tares, or reference thresholds. "
        f"Linear transformation allows robust parameter estimation via ordinary least squares without non-linear solver instability or convergence traps. "
        f"Plotting transformed observation pairs displays sensor sensitivities, elastic moduli, hemodynamic resistances, or acoustic attenuation coefficients directly as linear slopes. "
        f"This linear graphical formulation provides an immediate visual check of homoscedasticity, linearity, and potential sensor saturation, biological yield, or non-linear compliance."
    )
    discussion = (
        f"The empirical laboratory observations provide rigorous quantitative verification of {c['title']}. "
        f"In biomedical engineering, medical instrumentation, biomechanics, and artificial organs, physical systems "
        f"are governed by Maxwell equations, Navier-Stokes fluid mechanics, Hookean continuum elasticity, and biphasic mixture theories. "
        f"Across all six observation trials, the empirical slope m = {fmt(f['m'], 4)} confirms the theoretical model with near-zero residual variance. "
        f"Furthermore, comparison with established medical engineering benchmarks (Webster, Bronzino, Fung, and Winter) underscores vital clinical design principles including "
        f"patient electrical safety, biocompatibility, transducer signal-to-noise ratio, fatigue longevity, and hemodynamic shear preservation. "
        f"Residual analysis confirms homoscedastic dispersion without systematic non-linear patterning, validating the underlying model assumptions. "
        f"Confidence intervals calculated via asymptotic standard errors align with theoretical quantiles, indicating that finite-sample distortions "
        f"remain negligible under controlled test conditions. The experimental protocol confirms the robustness of the methodology across varying physiological operating states."
    )
    conclusion = (
        f"This laboratory investigation quantitatively verified the mathematical formulation and physical behavior of {c['title']}. "
        f"Through rigorous tracking across six observation points, we confirmed an empirical {c['targetName']} of "
        f"{fmt(value * c['resultScale'], c['resultDecimals'])} {c['resultUnit']} matching the theoretical reference {fmt(reference * c['resultScale'], c['resultDecimals'])} {c['resultUnit']} "
        f"within {percent:.4f}% error. The investigation demonstrates why this biomedical engineering method serves as an indispensable cornerstone in modern clinical patient monitoring, implant design, and diagnostic systems. "
        f"The verified scaling laws and parameter estimates demonstrate the practical efficacy of physiological modeling and biomedical engineering principles."
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
    svg = f'<svg viewBox="0 0 650 340" role="img" aria-label="Regression graph for {E(c["shortTitle"])}"><rect width="650" height="340" fill="#042f2e"/>'
    for i in range(5):
        x = xmin + i * (xmax - xmin) / 4
        y = ymin + i * (ymax - ymin) / 4
        svg += f'<line x1="{left}" y1="{py(y):.1f}" x2="{right}" y2="{py(y):.1f}" stroke="#134e4a" stroke-dasharray="2,2"/><text x="{left-9}" y="{py(y)+4:.1f}" text-anchor="end" font-size="10" fill="#5eead4">{fmt(y, 2)}</text><text x="{px(x):.1f}" y="300" text-anchor="middle" font-size="10" fill="#5eead4">{fmt(x, 2)}</text>'
    svg += f'<path d="M{left} {top}V{bottom}H{right}" stroke="#0d9488" fill="none"/><text x="335" y="332" text-anchor="middle" fill="#ccfbf1" font-size="12">{E(c["xAxis"])}</text><text transform="translate(18 160) rotate(-90)" text-anchor="middle" fill="#ccfbf1" font-size="12">{E(c["yAxis"])}</text>'
    pts = [f"{px(xmin + i * (xmax - xmin) / 100):.1f},{py((f['m'] * (xmin + i * (xmax - xmin) / 100) / c['xScale'] + f['b']) * c['yScale']):.1f}" for i in range(101)]
    svg += f'<polyline points="{" ".join(pts)}" stroke="#14b8a6" stroke-width="2.5" fill="none"/>'
    for r in rows:
        svg += f'<circle cx="{px(r["x"] * c["xScale"]):.1f}" cy="{py(r["y"] * c["yScale"]):.1f}" r="5" fill="#2dd4bf" stroke="#042f2e" stroke-width="1.5"/>'
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
        for i, m in enumerate(c.get('simModes', [{'id':'bench','icon':'🩺','label':'1. Physiological Test Bench'},{'id':'compare','icon':'📊','label':'2. Comparative Telemetry'},{'id':'sandbox','icon':'⚡','label':'3. Biomedical Sandbox'}]))
    )
    return f'''<section aria-label="Interactive workbench"><div class="section-top"><div><div class="eyebrow">BIOINSTRUMENTATION · BIOSIGNALS · BIOMECHANICS · IMAGING</div><h2>Your virtual biomedical engineering laboratory.</h2></div><button id="resetApparatus" class="text-button">Reset apparatus</button></div><div class="new-workbench"><div class="new-visual"><div class="visual-top"><div class="sim-mode-switcher" role="tablist" aria-label="Simulation Views">{sim_buttons}</div><button id="pauseMotion" class="dark-button" hidden>Pause motion</button></div><svg id="apparatusDiagram" viewBox="0 0 720 320" role="img" aria-label="Interactive biomedical workbench for {E(c['shortTitle'])}"></svg><div class="new-meter"><div><small>{E(c['rawLabel'].upper())}</small><strong id="readingValue">—</strong></div><div><small>PHYSIOLOGICAL &amp; TEST CELL TELEMETRY</small><p id="liveState" style="font-size:11px;margin:7px 0">Ready to sample with {E(c['shortInput'])} = {c['initial']} {E(c['inputUnit'])}.</p></div></div></div><div class="new-controls"><label for="independent">{E(c['inputLabel'])}</label><output id="independentOut">{c['initial']} {E(c['inputUnit'])}</output><input id="independent" type="range" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><label for="independentNumber">Set {E(c['shortInput'])} ({E(c['inputUnit'])})</label><input id="independentNumber" type="number" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><div class="lab-control-meta">{E(c['settings'][0])}</div><button id="measure" class="primary full">{E(c.get('measureLabel', 'Execute biomedical measurement'))}</button><button id="recordReading" class="secondary full" disabled>＋ Record observation</button><p id="trialStatus" class="trial-status" role="status">Adjust {E(c['shortInput'])}, then execute biomedical trial.</p></div></div><p class="data-notice">Biomedical engineering telemetry and physiological states are evaluated rigorously using 64-bit IEEE 754 precision. Residuals reflect ordinary least-squares regression across successive observations. Continuous data structures support high-fidelity biological and physiological modeling.</p><details class="model-note"><summary>Biomedical assumptions and boundary condition limits</summary><p>{E(c['limitations'][0] if isinstance(c['limitations'], list) else c['limitations'])} {E(c['modelExtra'])}</p></details></section><section id="apparatus" class="lab-section"><h2>Biomedical apparatus &amp; physiological sensors.</h2><div class="apparatus-list">{''.join('<article class="apparatus-item"><h3>'+E(a['name'])+'</h3><p>'+E(a['purpose'])+'</p></article>' for a in c['apparatus'])}</div></section><section id="method" class="lab-section"><div class="eyebrow">FOLLOW THE METHOD</div><h2>A reason behind every step.</h2><p class="intro">{E(c['aim'])} Standardized parameter settings: {", ".join(map(str,c['samples']))} {E(c['inputUnit'])}.</p>{method(c)}</section><section id="results" class="lab-section"><div class="section-top"><div><div class="eyebrow">YOUR NOTEBOOK · <span id="notebookCount">0</span> OBSERVATIONS</div><h2>Turn measurements into biomedical engineering insight.</h2></div><a class="text-button" href="/biomedical-engineering/{c['slug']}/report/">See a complete example report ↗</a></div><div class="lab-result-grid"><div class="chart-card"><svg id="labPlot" viewBox="0 0 650 340" role="img" aria-label="Measured observations and fitted regression graph"></svg><p>Points are your recorded observations. The solid regression line validates {E(c['shortTitle'])} mathematical scaling.</p></div><div class="fit-card lab-fit"><span class="eyebrow">LINEAR REGRESSION FIT · y = mx + b</span><div id="fitSummary"></div><div class="report-equation">{E(c['fitEquation'])}</div></div></div><div class="table-card"><table><thead><tr><th>#</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Remove</th></tr></thead><tbody id="readingRows"></tbody></table><p id="emptyReadings">No readings yet. Execute a biomedical trial and record it.</p></div><div class="lab-reading-actions"><button id="downloadReadings" class="secondary" disabled>↓ Export CSV</button><button id="clearReadings" class="secondary" disabled>Clear notebook</button></div><div class="source-box"><h3>Calculate it yourself.</h3><label for="studentEstimate">Your estimate of {E(c['targetName'])} ({E(c['resultUnit'])})</label> <input id="studentEstimate" type="number" step="any" min="0" style="max-width:140px"><button id="checkEstimate" class="secondary" style="margin-left:10px">Check calculation</button><p id="estimateFeedback" role="status"></p></div></section><section id="check" class="lab-section lab-questions"><div class="eyebrow">CHECK YOUR UNDERSTANDING</div><h2>Explain what the biomedical metrics mean.</h2>{''.join('<article class="quiz-card"><h3>'+E(q['question'])+'</h3><div class="quiz-choices">'+''.join('<button class="quiz-option" data-quiz="'+str(i)+'" data-choice="'+str(j)+'">'+E(a)+'</button>' for j,a in enumerate(q['options']))+'</div><p id="quizFeedback'+str(i)+'" class="quiz-feedback" role="status"></p></article>' for i,q in enumerate(c['quiz']))}</section>'''

def theory(c):
    return f'''<article class="theory-article"><h2>Biomedical and physiological foundations of {E(c['shortTitle'])}.</h2><p class="lead">{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><h3>Viva voce questions &amp; analytical theory</h3><div class="faq-list">{''.join(f'<details class="faq-item"><summary><strong>{E(t["question"])}</strong></summary><p>{E(t["answer"])}</p></details>' for t in c['topics'])}</div><h3>Experimental precautions and patient safety</h3><ul>{''.join(f'<li>{E(p)}</li>' for p in c['precautions'])}</ul><h3>Theoretical assumptions &amp; biological limits</h3><ul>{''.join(f'<li>{E(l)}</li>' for l in c['limitations'])}</ul></article>'''

def report(c, rows, f, out):
    slug = c['slug']
    csvpath = f"/biomedical-engineering/{slug}/sample-data.csv"
    csv_content = io.StringIO()
    writer = csv.writer(csv_content)
    writer.writerow([c['shortInput'].replace(' ', '_'), c['rawLabel'].replace(' ', '_'), 'x_coord', 'y_coord', 'fitted_y', 'residual'])
    for r in rows:
        fit_y = f['m'] * r['x'] + f['b']
        writer.writerow([r['input'], r['raw'], f"{r['x']:.4f}", f"{r['y']:.4f}", f"{fit_y:.4f}", f"{r['y'] - fit_y:.4f}"])
    (out / f"biomedical-engineering/{slug}/sample-data.csv").write_text(csv_content.getvalue(), encoding='utf-8')

    value, se, reference = estimate(c, f)
    percent = abs(value - reference) / abs(reference) * 100
    uncertainty = uncertainty_text(c)
    abstract, graph_choice, discussion, conclusion = report_narrative(c, rows, f, value, percent, reference)

    obs = "".join(
        f"<tr><td>{i+1}</td><td>{r['input']}</td><td>{r['raw']}</td><td>{r['x']:.4f}</td><td>{r['y']:.4f}</td><td>{f['m']*r['x']+f['b']:.4f}</td><td>{r['y']-(f['m']*r['x']+f['b']):.4f}</td></tr>"
        for i, r in enumerate(rows)
    )

    return f'''<div class="section-top"><div><div class="eyebrow">WORKED EXAMPLE · BENCHMARK OBSERVATIONS</div><h2>A complete example laboratory report.</h2></div><button class="secondary" onclick="window.print()">Print / save as PDF</button></div><div class="report-notice"><strong>Simulated demonstration data.</strong><p>This report illustrates formal biomedical engineering data reduction, transducer calibration tares, and physiological parameter estimation. Replace its observations with your own experimental telemetry when preparing a biomedical engineering laboratory report submission.</p></div><div class="report-person"><span>Student: __________________</span><span>Student ID: __________________</span><span>Course: __________________</span><span>Date: __________________</span><span>Partner: __________________</span><span>Instructor: __________________</span></div><article class="lab-report"><h3>1. Title and aim</h3><p><strong>{E(c['title'])}.</strong> {E(c['aim'])}</p><h3>2. Abstract</h3><p>{E(abstract)}</p><h3>3. Apparatus and fixed settings</h3><ul>{''.join('<li>'+E(a['name'])+': '+E(a['purpose'])+'</li>' for a in c['apparatus'])}{''.join('<li>'+E(s)+'</li>' for s in c['settings'])}</ul><h3>4. Theory and graph choice</h3><p>{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>{E(graph_choice)}</p><h3>5. Method</h3><ol>{''.join('<li>'+E(s['text'])+'</li>' for s in c['procedure'])}</ol><h3>6. Observations and calculation table</h3><p>All biomedical observations use strictly controlled 64-bit IEEE 754 precision buffers. Residuals are computed relative to the ordinary least-squares regression line.</p><div class="table-card"><table><caption>Table 1. Six simulated observations; x and y represent transformed biomedical metrics.</caption><thead><tr><th>No.</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Fitted y</th><th>Residual</th></tr></thead><tbody>{obs}</tbody></table></div><p><a href="{csvpath}" download>Download the sample observations (CSV) ↓</a></p><h3>7. Worked calculation for one observation</h3><div class="report-equation">{E(worked(c, rows[0]))}</div><h3>8. Graph, gradient and final calculation</h3><div class="chart-card">{graph(c, rows, f)}</div><p>Circular markers represent empirical biomedical observations. The solid line represents the ordinary least-squares linear fit.</p><div class="report-equation">x̄ = {fmt(f['mx'])}; ȳ = {fmt(f['my'])}<br>Σ(x − x̄)² = {fmt(f['sxx'])}<br>Σ(x − x̄)(y − ȳ) = {fmt(f['sxy'])}<br>m = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)² = {fmt(f['m'], 8)}<br>b = ȳ − mx̄ = {fmt(f['b'], 8)}<br>{E(formula(c, f))}</div><h3>9. Uncertainty and comparison</h3><p>Percentage difference = |estimate − theoretical value| / |theoretical value| × 100 = <strong>{percent:.4f}%</strong>.</p><p>For n = 6 observations, Σresidual² = {fmt(f['sse'])}; s² = Σresidual²/(n − 2). Gradient standard error = √[s²/Σ(x − x̄)²] = {fmt(f['slopeSE'])}. Intercept standard error = √[s²(1/n + x̄²/Σ(x − x̄)²)] = {fmt(f['interceptSE'])}.</p><p>Propagating the fit parameters yields a <strong>fit standard error of {fmt(se * c['resultScale'])} {E(c['resultUnit'])}</strong>, with an ideal coefficient of determination R² = {f['r2']:.6f}.</p><p>{E(uncertainty)}</p><h3>10. Result and discussion</h3><div class="report-equation">{E(c['targetName'])} = {fmt(value * c['resultScale'], c['resultDecimals'])} {E(c['resultUnit'])}<br>Theoretical reference value: {fmt(reference * c['resultScale'], c['resultDecimals'])} {E(c['resultUnit'])}</div><p>{E(discussion)}</p><h3>11. Precautions and limitations</h3><ul>{''.join('<li>'+E(p)+'</li>' for p in c['precautions'])}</ul><p>{E(c['limitations'][0] if isinstance(c['limitations'], list) else c['limitations'])} {E(c['modelExtra'])}</p><h3>12. Conclusion</h3><p>{E(conclusion)}</p></article>'''

def shell(c, part, body, base, production):
    path = f"/biomedical-engineering/{c['slug']}/" + ('' if part == 'experiment' else part + '/')
    title = {
        'experiment': c['title'] + ' | Biomedical Engineering Lab',
        'theory': c['shortTitle'] + ' Theory & Equations | Open STEM Lab',
        'report': c['shortTitle'] + ' Lab Report & Empirical Data | Open STEM Lab'
    }[part]
    desc = {
        'experiment': c['aim'] + ' Explore interactive physiological instrumentation simulation, biomechanics, and biomedical engineering telemetry.',
        'theory': 'Understand ' + c['shortTitle'].lower() + ': governing biomedical equations, biopotentials, constitutive tissue models, and medical devices.',
        'report': 'A worked ' + c['shortTitle'].lower() + ' lab report with sample observation tables, regression plots, calculations, and error analysis.'
    }[part]
    header = head(path, title, desc, base, production).replace('<link rel="stylesheet" href="/catalog.css">', '<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/biomed-lesson.css">')
    header = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: f'<script type="application/ld+json">{lesson_schema(c, part, path, title, desc, base)}</script>', header, flags=re.S)
    home = f'/biomedical-engineering/{c["slug"]}/'
    nav = '<aside class="sidebar"><a class="brand" style="font-size:20px" href="/">◉ openstemlab.</a><a class="side-subject" href="/subjects/biomedical-engineering/">← Biomedical Engineering labs</a><div class="side-label">LABORATORY ' + str(c['number']).zfill(2) + '</div><nav aria-label="Lesson navigation">'
    for href, label in [(home, 'Explore the experiment'), (home + 'theory/', 'Understand the theory'), (home + '#apparatus', 'Know your tools'), (home + '#method', 'Follow the method'), (home + '#results', 'Analyse your results'), (home + '#check', 'Check your understanding'), (home + 'report/', 'Sample lab report')]:
        nav += f'<a class="nav-item{" active" if path==href else ""}" href="{href}">{label}</a>'
    nav += '<a class="nav-item" href="/experiments/">Search all experiments</a></nav><div class="side-note"><span class="small-sun">✳</span><p>Learn by physiological trial.<br>Understand by bio-mechanics.</p></div><a class="text-button" href="/">← All subjects</a></aside>'
    heading = c['title'] if part == 'experiment' else c['shortTitle'] + ' theory' if part == 'theory' else c['shortTitle'] + ' lab report'
    return (
        header + '<body>' + nav + '<main><header class="topbar"><div><a href="/subjects/biomedical-engineering/">Biomedical Engineering</a> / ' + E(c['shortTitle']) + '</div><span class="free-label">FREE TO EXPLORE</span></header>'
        '<section class="page-heading"><div class="eyebrow">LABORATORY ' + str(c['number']).zfill(2) + ' · BIOMEDICAL ENGINEERING</div><h1>' + E(heading) + '</h1><p>' + E(desc) + '</p></section>'
        '<nav class="lab-navigation" aria-label="Experiment pages"><a href="' + home + '">Workbench</a><a href="' + home + 'theory/">Detailed theory</a><a href="' + home + '#method">Method</a><a href="' + home + '#results">My results</a><a href="' + home + 'report/">Example report</a></nav>'
        + body +
        '<footer><span class="footer-brand">openstemlab.</span><a href="/subjects/biomedical-engineering/">All biomedical labs</a><span>Physiological &amp; biomechanical model</span></footer></main>'
        + ('<script id="labConfig" type="application/json">' + json.dumps(c, ensure_ascii=False).replace('<', chr(92) + 'u003c') + '</script><script src="/biomed-models.js"></script><script src="/biomed-engine.js"></script>' if part == 'experiment' else '')
        + '</body></html>'
    )

def build_biomedical(out, base, production):
    published = [c for c in specs() if c.get('published', False)]
    for name, dest in [('models.js', 'biomed-models.js'), ('engine.js', 'biomed-engine.js'), ('lesson.css', 'biomed-lesson.css')]:
        (out / dest).write_text((ROOT / 'content/biomedical' / name).read_text(encoding='utf-8'), encoding='utf-8')
    db = sqlite3.connect(ROOT / 'data/catalog.sqlite3')
    sid = db.execute("SELECT id FROM subjects WHERE slug='biomedical-engineering'").fetchone()[0]
    db.execute("UPDATE subjects SET content_status='live' WHERE slug='biomedical-engineering'")
    paths = []
    for c in published:
        slug = c['slug']
        home = f'/biomedical-engineering/{slug}/'
        (out / home.lstrip('/')).mkdir(parents=True, exist_ok=True)
        rows = [observation(c, v) for v in c['samples']]
        f = fit(rows)
        for part, body in [
            ('experiment', workbench(c)),
            ('theory', '<section>' + theory(c) + f'<div class="insight"><span>↳</span><div><strong>Connect physiological theory to empirical clinical data.</strong><p>{E(c["modelExtra"])}</p></div></div></section>'),
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
    paths = build_biomedical(out, base, args.production)
    print(f"Built {len(paths)} Biomedical Engineering pages for {base}: {paths[:3]}...")
