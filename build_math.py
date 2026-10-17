"""Static lesson pages and reproducible simulated reports for published Mathematics labs."""
from pathlib import Path
import json, math, csv, io, sqlite3, html, re

ROOT = Path(__file__).resolve().parent
E = lambda s: html.escape(str(s), quote=True)

def specs():
    return json.loads((ROOT / 'content/math/experiments.json').read_text())

def rnd(x, n):
    return math.floor(x * 10**n + .5) / 10**n

def fmt(v, n=5):
    return f'{v:.4e}' if v and (abs(v) < .001 or abs(v) >= 1e6) else f'{v:.{n}f}'

def observation(c, value):
    slug = c['slug']
    step = int(round(float(value)))
    samples = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    
    if slug == 'bisection-method-root-convergence':
        raw = rnd(1.0 / (2**step), 4)
        x = float(step)
        y = float(-step)
        return {'input': value, 'raw': raw, 'x': x, 'y': y}
    elif slug == 'fixed-point-iteration-banach-contraction':
        x = rnd(0.500000 * (0.125**(step - 1)), 6)
        y = rnd(0.125 * x, 6)
        raw = rnd(1.000000 + x, 6)
        return {'input': value, 'raw': raw, 'x': x, 'y': y}
    else:
        # General convergence order model: ln(e_{k+1}) = alpha * ln(e_k) + ln(C)
        params = {
            'newton-raphson-quadratic-convergence': (2.000, -1.4979, -0.2693, 2.236068),
            'secant-method-superlinear-convergence': (1.618, -0.5982, -0.8715, 2.094551),
            'regula-falsi-false-position-bracketing': (1.442, -1.7580, -3.0290, 0.201638),
            'muller-method-complex-polynomial-roots': (1.839, -0.1625, -1.5000, 1.839287),
            'bairstow-method-polynomial-quadratic-factors': (2.000, -0.6120, -1.1468, 2.000000),
            'brent-dekker-hybrid-root-finding': (1.839, -0.1054, -1.4000, 0.910008),
            'halley-method-cubic-root-convergence': (3.000, -0.9163, -1.0000, 1.912931),
            'steffensen-method-accelerated-convergence': (2.000, -0.5877, -1.3000, 1.414214)
        }
        alpha, lnC, x0, root_val = params[slug]
        cur_x = x0
        for _ in range(1, step):
            cur_x = alpha * cur_x + lnC
        x = rnd(cur_x, 4)
        y = rnd(alpha * x + lnC, 4)
        raw = float(step)
        return {'input': value, 'raw': raw, 'x': x, 'y': y}

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
    slug = c['slug']
    if slug == 'bisection-method-root-convergence':
        C_est = 2.0**f['m']
        se = abs(C_est * math.log(2.0) * (f['slopeSE'] or 0.0001))
        return C_est, se, 0.500
    elif slug == 'newton-raphson-quadratic-convergence':
        return f['m'], f['slopeSE'], 2.000
    elif slug == 'secant-method-superlinear-convergence':
        return f['m'], f['slopeSE'], 1.618
    elif slug == 'regula-falsi-false-position-bracketing':
        return f['m'], f['slopeSE'], 1.442
    elif slug == 'fixed-point-iteration-banach-contraction':
        return f['m'], f['slopeSE'], 0.125
    elif slug == 'muller-method-complex-polynomial-roots':
        return f['m'], f['slopeSE'], 1.839
    elif slug == 'bairstow-method-polynomial-quadratic-factors':
        return f['m'], f['slopeSE'], 2.000
    elif slug == 'brent-dekker-hybrid-root-finding':
        return f['m'], f['slopeSE'], 1.839
    elif slug == 'halley-method-cubic-root-convergence':
        return f['m'], f['slopeSE'], 3.000
    elif slug == 'steffensen-method-accelerated-convergence':
        return f['m'], f['slopeSE'], 2.000
    raise ValueError(f"Unknown math estimate slug: {slug}")

def formula(c, f):
    slug = c['slug']
    val = f['m'] * c['resultScale']
    if slug == 'bisection-method-root-convergence':
        return f"log2(Δx_k) = {fmt(f['m'], 4)} · k + {fmt(f['b'], 4)} ⟹ C = 2^({fmt(f['m'], 4)}) = {fmt(val, c['resultDecimals'])} (theoretical C = 0.500)"
    elif slug == 'fixed-point-iteration-banach-contraction':
        return f"ε_(k+1) = {fmt(f['m'], 4)} · ε_k + {fmt(f['b'], 4)} ⟹ L = |g'(x*)| = {fmt(val, c['resultDecimals'])} (theoretical L = 0.125)"
    else:
        return f"ln(ε_(k+1)) = {fmt(f['m'], 4)} · ln(ε_k) + {fmt(f['b'], 4)} ⟹ α = {fmt(val, c['resultDecimals'])} (theoretical α = {c['target']})"

def worked(c, row):
    slug = c['slug']
    k = row['input']
    if slug == 'bisection-method-root-convergence':
        return f"For step k = {k}: Bracket width Δx_{k} = (b₀ − a₀) / 2^{k} = 1.0 / 2^{k} = {row['raw']:.4f}. Logarithmic coordinate: y = log₂(Δx_{k}) = log₂({row['raw']:.4f}) = {row['y']:.4f}. Independent coordinate: x = k = {row['x']:.4f}."
    elif slug == 'fixed-point-iteration-banach-contraction':
        return f"For step k = {k}: Current Picard error ε_{k} = |x_{k} − x*| = {row['x']:.6f}. Contracted next error ε_{k+1} = L · ε_{k} = 0.125 · {row['x']:.6f} = {row['y']:.6f}. Output iterate x_{k+1} = 1.000000 + {row['y']:.6f} = {row['raw']:.6f}."
    else:
        return f"For step k = {k}: Current logarithmic error x = ln(ε_{k}) = {row['x']:.4f}. Asymptotic next logarithmic error y = ln(ε_{k+1}) = α · ln(ε_{k}) + ln(C) = {row['y']:.4f}. Empirical iterate count: {row['raw']:.0f}."

def uncertainty_text(c):
    return (
        f"In computational mathematics and numerical analysis, errors arise from algorithmic truncation, finite precision IEEE 754 floating-point arithmetic "
        f"(machine epsilon ε_mach ≈ 2.22 × 10⁻¹⁶ for 64-bit double precision), and condition number propagation. "
        f"The ordinary least-squares fit across n = 6 standardized iterations provides standard errors for the gradient and intercept. "
        f"Because the mathematical recurrence is evaluated with high precision, the residual sum of squares is vanishingly small, "
        f"yielding a coefficient of determination R² ≥ 0.999999 and confirming the theoretical convergence order."
    )

def report_narrative(c, rows, f, value, percent, reference):
    slug = c['slug']
    abstract = (
        f"Six computational iterations were executed across standardized steps k = {rows[0]['input']} to k = {rows[-1]['input']} "
        f"for {c['title']}. An ordinary least-squares regression on the linearized error recurrence yielded an empirical "
        f"{c['targetName']} of {fmt(value * c['resultScale'], c['resultDecimals'])} {c['resultUnit']} (difference from theoretical reference = {percent:.4f}%). "
        f"The empirical telemetry conclusively validates the theoretical convergence rate and error attenuation dynamics with R² = {f['r2']:.6f}."
    )
    graph_choice = (
        f"The mathematical regression linearizes the error recurrence into the form y = mx + b. "
        f"Here, the independent variable x represents {c['xAxis']}, and the dependent variable y represents {c['yAxis']}. "
        f"The slope m directly extracts {c['targetName']}, while the intercept b accounts for the asymptotic error constant ln(C)."
    )
    discussion = (
        f"The empirical benchmark observations provide rigorous quantitative verification of {c['title']}. "
        f"In numerical analysis, root-finding algorithms are characterized by their asymptotic order of convergence α and computational efficiency. "
        f"Across all six iterations, the empirical slope m = {fmt(f['m'], 4)} confirms the theoretical model with near-zero residual variance. "
        f"Furthermore, comparison with alternative root-finding paradigms underscores critical trade-offs between per-iteration evaluation cost "
        f"and global convergence robustness. The algorithm's behavior confirms the mathematical predictions established by numerical analysis literature."
    )
    conclusion = (
        f"This computational laboratory investigation quantitatively verified the mathematical formulation and asymptotic convergence of {c['title']}. "
        f"Through rigorous iterative tracking across six steps, we confirmed an empirical {c['targetName']} of "
        f"{fmt(value * c['resultScale'], c['resultDecimals'])} {c['resultUnit']} matching the theoretical reference {fmt(reference * c['resultScale'], c['resultDecimals'])} {c['resultUnit']} "
        f"within {percent:.4f}% error. The investigation demonstrates why this method serves as an indispensable tool in modern computational science."
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
    svg = f'<svg viewBox="0 0 650 340" role="img" aria-label="Regression graph for {E(c["shortTitle"])}"><rect width="650" height="340" fill="#080c16"/>'
    for i in range(5):
        x = xmin + i * (xmax - xmin) / 4
        y = ymin + i * (ymax - ymin) / 4
        svg += f'<line x1="{left}" y1="{py(y):.1f}" x2="{right}" y2="{py(y):.1f}" stroke="#1e293b" stroke-dasharray="2,2"/><text x="{left-9}" y="{py(y)+4:.1f}" text-anchor="end" font-size="10" fill="#64748b">{fmt(y, 2)}</text><text x="{px(x):.1f}" y="300" text-anchor="middle" font-size="10" fill="#64748b">{fmt(x, 2)}</text>'
    svg += f'<path d="M{left} {top}V{bottom}H{right}" stroke="#475569" fill="none"/><text x="335" y="332" text-anchor="middle" fill="#818cf8" font-size="12">{E(c["xAxis"])}</text><text transform="translate(18 160) rotate(-90)" text-anchor="middle" fill="#818cf8" font-size="12">{E(c["yAxis"])}</text>'
    pts = [f"{px(xmin + i * (xmax - xmin) / 100):.1f},{py((f['m'] * (xmin + i * (xmax - xmin) / 100) / c['xScale'] + f['b']) * c['yScale']):.1f}" for i in range(101)]
    svg += f'<polyline points="{" ".join(pts)}" stroke="#38bdf8" stroke-width="2.5" fill="none"/>'
    for r in rows:
        svg += f'<circle cx="{px(r["x"] * c["xScale"]):.1f}" cy="{py(r["y"] * c["yScale"]):.1f}" r="5" fill="#f43f5e" stroke="#fff" stroke-width="1.2"/>'
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
        for i, m in enumerate(c.get('simModes', [{'id':'bench','icon':'📐','label':'1. Iteration Dynamics'},{'id':'compare','icon':'📊','label':'2. Rate Comparison'},{'id':'sandbox','icon':'⚡','label':'3. Parameter Sandbox'}]))
    )
    return f'''<section aria-label="Interactive workbench"><div class="section-top"><div><div class="eyebrow">COMPUTE · CONVERGE · ANALYSE</div><h2>Your virtual mathematics laboratory.</h2></div><button id="resetApparatus" class="text-button">Reset iterations</button></div><div class="new-workbench"><div class="new-visual"><div class="visual-top"><div class="sim-mode-switcher" role="tablist" aria-label="Simulation Views">{sim_buttons}</div><button id="pauseMotion" class="dark-button" hidden>Pause motion</button></div><svg id="apparatusDiagram" viewBox="0 0 720 320" role="img" aria-label="Interactive mathematical visualization for {E(c['shortTitle'])}"></svg><div class="new-meter"><div><small>{E(c['rawLabel'].upper())}</small><strong id="readingValue">—</strong></div><div><small>CONVERGENCE STATUS</small><p id="liveState" style="font-size:11px;margin:7px 0">Ready to execute iteration step k = {c['initial']}.</p></div></div></div><div class="new-controls"><label for="independent">{E(c['inputLabel'])}</label><output id="independentOut">{c['initial']} {E(c['inputUnit'])}</output><input id="independent" type="range" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><label for="independentNumber">Set {E(c['shortInput'])} ({E(c['inputUnit'])})</label><input id="independentNumber" type="number" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><div class="lab-control-meta">{E(c['settings'][0])}</div><button id="measure" class="primary full">{E(c['measureLabel'])}</button><button id="recordReading" class="secondary full" disabled>＋ Record observation</button><p id="trialStatus" class="trial-status" role="status">Adjust {E(c['shortInput'])}, then execute iteration.</p></div></div><p class="data-notice">Mathematical iterates are computed deterministically using 64-bit IEEE 754 precision. Residuals reflect ordinary least-squares regression across successive error coordinates.</p><details class="model-note"><summary>Numerical assumptions and limits</summary><p>{E(c['limitations'][0] if isinstance(c['limitations'], list) else c['limitations'])} {E(c['modelExtra'])}</p></details></section><section id="apparatus" class="lab-section"><h2>Computational tools & numerical modules.</h2><div class="apparatus-list">{''.join('<article class="apparatus-item"><h3>'+E(a['name'])+'</h3><p>'+E(a['purpose'])+'</p></article>' for a in c['apparatus'])}</div></section><section id="method" class="lab-section"><div class="eyebrow">FOLLOW THE METHOD</div><h2>A reason behind every step.</h2><p class="intro">{E(c['aim'])} Standardized iteration sequence: {", ".join(map(str,c['samples']))} {E(c['inputUnit'])}.</p>{method(c)}</section><section id="results" class="lab-section"><div class="section-top"><div><div class="eyebrow">YOUR NOTEBOOK · <span id="notebookCount">0</span> OBSERVATIONS</div><h2>Turn measurements into mathematical insight.</h2></div><a class="text-button" href="/mathematics/{c['slug']}/report/">See a complete example report ↗</a></div><div class="lab-result-grid"><div class="chart-card"><svg id="labPlot" viewBox="0 0 650 340" role="img" aria-label="Measured observations and fitted asymptotic graph"></svg><p>Points are your recorded iteration observations. The solid regression line validates {E(c['shortTitle'])} convergence order.</p></div><div class="fit-card lab-fit"><span class="eyebrow">LINEAR ASYMPTOTIC FIT · y = mx + b</span><div id="fitSummary"></div><div class="report-equation">{E(c['fitEquation'])}</div></div></div><div class="table-card"><table><thead><tr><th>#</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Remove</th></tr></thead><tbody id="readingRows"></tbody></table><p id="emptyReadings">No readings yet. Execute an iteration and record it.</p></div><div class="lab-reading-actions"><button id="downloadReadings" class="secondary" disabled>↓ Export CSV</button><button id="clearReadings" class="secondary" disabled>Clear notebook</button></div><div class="source-box"><h3>Calculate it yourself.</h3><label for="studentEstimate">Your estimate of {E(c['targetName'])} ({E(c['resultUnit'])})</label> <input id="studentEstimate" type="number" step="any" min="0" style="max-width:140px"><button id="checkEstimate" class="secondary" style="margin-left:10px">Check calculation</button><p id="estimateFeedback" role="status"></p></div></section><section id="check" class="lab-section lab-questions"><div class="eyebrow">CHECK YOUR UNDERSTANDING</div><h2>Explain what the mathematical rates mean.</h2>{''.join('<article class="quiz-card"><h3>'+E(q['question'])+'</h3><div class="quiz-choices">'+''.join('<button class="quiz-option" data-quiz="'+str(i)+'" data-choice="'+str(j)+'">'+E(a)+'</button>' for j,a in enumerate(q['options']))+'</div><p id="quizFeedback'+str(i)+'" class="quiz-feedback" role="status"></p></article>' for i,q in enumerate(c['quiz']))}</section>'''

def theory(c):
    return f'''<article class="theory-article"><h2>Mathematical foundations of {E(c['shortTitle'])}.</h2><p class="lead">{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><h3>Viva voce questions & analytical theory</h3><div class="faq-list">{''.join(f'<details class="faq-item"><summary><strong>{E(t["question"])}</strong></summary><p>{E(t["answer"])}</p></details>' for t in c['topics'])}</div><h3>Algorithm precautions and stability rules</h3><ul>{''.join(f'<li>{E(p)}</li>' for p in c['precautions'])}</ul><h3>Theoretical limitations</h3><ul>{''.join(f'<li>{E(l)}</li>' for l in c['limitations'])}</ul></article>'''

def report(c, rows, f, out):
    slug = c['slug']
    csvpath = f"/mathematics/{slug}/sample-data.csv"
    csv_content = io.StringIO()
    writer = csv.writer(csv_content)
    writer.writerow(['step_k', c['rawLabel'].replace(' ', '_'), 'x_coord', 'y_coord', 'fitted_y', 'residual'])
    for r in rows:
        fit_y = f['m'] * r['x'] + f['b']
        writer.writerow([r['input'], r['raw'], f"{r['x']:.4f}", f"{r['y']:.4f}", f"{fit_y:.4f}", f"{r['y'] - fit_y:.4f}"])
    (out / f"mathematics/{slug}/sample-data.csv").write_text(csv_content.getvalue(), encoding='utf-8')

    value, se, reference = estimate(c, f)
    percent = abs(value - reference) / reference * 100
    uncertainty = uncertainty_text(c)
    abstract, graph_choice, discussion, conclusion = report_narrative(c, rows, f, value, percent, reference)

    obs = "".join(
        f"<tr><td>{i+1}</td><td>{r['input']}</td><td>{r['raw']}</td><td>{r['x']:.4f}</td><td>{r['y']:.4f}</td><td>{f['m']*r['x']+f['b']:.4f}</td><td>{r['y']-(f['m']*r['x']+f['b']):.4f}</td></tr>"
        for i, r in enumerate(rows)
    )

    return f'''<div class="section-top"><div><div class="eyebrow">WORKED EXAMPLE · BENCHMARK OBSERVATIONS</div><h2>A complete example laboratory report.</h2></div><button class="secondary" onclick="window.print()">Print / save as PDF</button></div><div class="report-notice"><strong>Simulated demonstration data.</strong><p>This report illustrates formal numerical analysis, iteration tracking, and convergence rate extraction. Replace its observations with your own computational telemetry when preparing a practical submission.</p></div><div class="report-person"><span>Student: __________________</span><span>Student ID: __________________</span><span>Course: __________________</span><span>Date: __________________</span><span>Partner: __________________</span><span>Instructor: __________________</span></div><article class="lab-report"><h3>1. Title and aim</h3><p><strong>{E(c['title'])}.</strong> {E(c['aim'])}</p><h3>2. Abstract</h3><p>{E(abstract)}</p><h3>3. Apparatus and fixed settings</h3><ul>{''.join('<li>'+E(a['name'])+': '+E(a['purpose'])+'</li>' for a in c['apparatus'])}{''.join('<li>'+E(s)+'</li>' for s in c['settings'])}</ul><h3>4. Theory and graph choice</h3><p>{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>{E(graph_choice)}</p><h3>5. Method</h3><ol>{''.join('<li>'+E(s['text'])+'</li>' for s in c['procedure'])}</ol><h3>6. Observations and calculation table</h3><p>All iterative observations use strictly controlled 64-bit IEEE 754 precision buffers. Residuals are computed relative to the ordinary least-squares regression line.</p><div class="table-card"><table><caption>Table 1. Six simulated iteration steps; x and y represent linearized error metrics.</caption><thead><tr><th>No.</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Fitted y</th><th>Residual</th></tr></thead><tbody>{obs}</tbody></table></div><p><a href="{csvpath}" download>Download the sample observations (CSV) ↓</a></p><h3>7. Worked calculation for one observation</h3><div class="report-equation">{E(worked(c, rows[0]))}</div><h3>8. Graph, gradient and final calculation</h3><div class="chart-card">{graph(c, rows, f)}</div><p>Circular markers represent empirical computational observations. The solid line represents the ordinary least-squares linear fit.</p><div class="report-equation">x̄ = {fmt(f['mx'])}; ȳ = {fmt(f['my'])}<br>Σ(x − x̄)² = {fmt(f['sxx'])}<br>Σ(x − x̄)(y − ȳ) = {fmt(f['sxy'])}<br>m = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)² = {fmt(f['m'], 8)}<br>b = ȳ − mx̄ = {fmt(f['b'], 8)}<br>{E(formula(c, f))}</div><h3>9. Uncertainty and comparison</h3><p>Percentage difference = |estimate − theoretical value| / |theoretical value| × 100 = <strong>{percent:.4f}%</strong>.</p><p>For n = 6 iteration observations, Σresidual² = {fmt(f['sse'])}; s² = Σresidual²/(n − 2). Gradient standard error = √[s²/Σ(x − x̄)²] = {fmt(f['slopeSE'])}. Intercept standard error = √[s²(1/n + x̄²/Σ(x − x̄)²)] = {fmt(f['interceptSE'])}.</p><p>Propagating the fit parameters yields a <strong>fit standard error of {fmt(se * c['resultScale'])} {E(c['resultUnit'])}</strong>, with an ideal coefficient of determination R² = {f['r2']:.6f}.</p><p>{E(uncertainty)}</p><h3>10. Result and discussion</h3><div class="report-equation">{E(c['targetName'])} = {fmt(value * c['resultScale'], c['resultDecimals'])} {E(c['resultUnit'])}<br>Theoretical reference value: {fmt(reference * c['resultScale'], c['resultDecimals'])} {E(c['resultUnit'])}</div><p>{E(discussion)}</p><h3>11. Precautions and limitations</h3><ul>{''.join('<li>'+E(p)+'</li>' for p in c['precautions'])}</ul><p>{E(c['limitations'][0] if isinstance(c['limitations'], list) else c['limitations'])} {E(c['modelExtra'])}</p><h3>12. Conclusion</h3><p>{E(conclusion)}</p></article>'''

def lesson_schema(c, part, path, title, desc, base):
    graph = [{'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Open STEM Lab', 'item': base + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Mathematics Laboratory', 'item': base + '/subjects/mathematics/'},
        {'@type': 'ListItem', 'position': 3, 'name': c['shortTitle'], 'item': base + f'/mathematics/{c["slug"]}/'}
    ]}]
    if part == 'experiment':
        graph.append({
            '@type': ['WebPage', 'LearningResource', 'TechArticle'],
            'name': title, 'description': desc, 'url': base + path,
            'learningResourceType': 'Interactive computational simulation',
            'educationalLevel': 'Undergraduate', 'about': c['title'], 'inLanguage': 'en',
            'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'}
        })
        if c.get('quiz'):
            graph.append({
                '@type': 'Quiz', 'name': c['shortTitle'] + ' Concept Understanding',
                'hasPart': [
                    {'@type': 'Question', 'name': q['question'],
                     'suggestedAnswer': [{'@type': 'Answer', 'text': opt} for opt in q['options']],
                     'acceptedAnswer': {'@type': 'Answer', 'text': q['options'][q['correct']]}}
                    for q in c['quiz']
                ]
            })
    elif part == 'theory':
        graph.append({
            '@type': ['WebPage', 'TechArticle', 'FAQPage'],
            'name': title, 'description': desc, 'url': base + path,
            'about': c['title'], 'inLanguage': 'en',
            'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'},
            'mainEntity': [{'@type': 'Question', 'name': t['question'], 'acceptedAnswer': {'@type': 'Answer', 'text': t['answer']}} for t in c['topics']]
        })
    else:
        graph.append({
            '@type': ['WebPage', 'ScholarlyArticle', 'TechArticle'],
            'name': title, 'description': desc, 'url': base + path,
            'about': c['title'], 'inLanguage': 'en',
            'isPartOf': {'@type': 'WebSite', 'name': 'Open STEM Lab', 'url': base + '/'}
        })
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)

def shell(c, part, body, base, production):
    from build_catalog import head
    path = f'/mathematics/{c["slug"]}/' + ('' if part == 'experiment' else part + '/')
    title = c['shortTitle'] + (' Experiment & Simulation' if part == 'experiment' else ' Theory & Analysis' if part == 'theory' else ' Lab Report: Iteration & Calculations') + ' | Open STEM Lab'
    desc = {
        'experiment': c['aim'] + ' Explore interactive numerical methods, evaluate error attenuation and verify convergence orders.',
        'theory': 'Understand ' + c['shortTitle'].lower() + ': mathematical proofs, error recurrences, asymptotic rates and stability criteria.',
        'report': 'A worked ' + c['shortTitle'].lower() + ' lab report with iteration data tables, logarithmic graphs, calculations, uncertainty and conclusions.'
    }[part]
    header = head(path, title, desc, base, production).replace('<link rel="stylesheet" href="/catalog.css">', '<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/math-lesson.css">')
    header = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: f'<script type="application/ld+json">{lesson_schema(c, part, path, title, desc, base)}</script>', header, flags=re.S)
    home = f'/mathematics/{c["slug"]}/'
    nav = '<aside class="sidebar"><a class="brand" style="font-size:20px" href="/">◉ openstemlab.</a><a class="side-subject" href="/subjects/mathematics/">← Mathematics labs</a><div class="side-label">LABORATORY ' + str(c['number']).zfill(2) + '</div><nav aria-label="Lesson navigation">'
    for href, label in [(home, 'Explore the experiment'), (home + 'theory/', 'Understand the theory'), (home + '#apparatus', 'Know your tools'), (home + '#method', 'Follow the method'), (home + '#results', 'Analyse your results'), (home + '#check', 'Check your understanding'), (home + 'report/', 'Sample lab report')]:
        nav += f'<a class="nav-item{" active" if path==href else ""}" href="{href}">{label}</a>'
    nav += '<a class="nav-item" href="/experiments/">Search all experiments</a></nav><div class="side-note"><span class="small-sun">✳</span><p>Learn by computing.<br>Understand by convergence.</p></div><a class="text-button" href="/">← All subjects</a></aside>'
    heading = c['title'] if part == 'experiment' else c['shortTitle'] + ' theory' if part == 'theory' else c['shortTitle'] + ' lab report'
    return (
        header + '<body>' + nav + '<main><header class="topbar"><div><a href="/subjects/mathematics/">Mathematics</a> / ' + E(c['shortTitle']) + '</div><span class="free-label">FREE TO EXPLORE</span></header>'
        '<section class="page-heading"><div class="eyebrow">LABORATORY ' + str(c['number']).zfill(2) + ' · MATHEMATICS</div><h1>' + E(heading) + '</h1><p>' + E(desc) + '</p></section>'
        '<nav class="lab-navigation" aria-label="Experiment pages"><a href="' + home + '">Workbench</a><a href="' + home + 'theory/">Detailed theory</a><a href="' + home + '#method">Method</a><a href="' + home + '#results">My results</a><a href="' + home + 'report/">Example report</a></nav>'
        + body +
        '<footer><span class="footer-brand">openstemlab.</span><a href="/subjects/mathematics/">All mathematics labs</a><span>Deterministic numerical model</span></footer></main>'
        + ('<script id="labConfig" type="application/json">' + json.dumps(c, ensure_ascii=False).replace('<', chr(92) + 'u003c') + '</script><script src="/math-models.js"></script><script src="/math-engine.js"></script>' if part == 'experiment' else '')
        + '</body></html>'
    )

def build_math(out, base, production):
    published = [c for c in specs() if c.get('published', False)]
    for name, dest in [('models.js', 'math-models.js'), ('engine.js', 'math-engine.js'), ('lesson.css', 'math-lesson.css')]:
        (out / dest).write_text((ROOT / 'content/math' / name).read_text(encoding='utf-8'), encoding='utf-8')
    db = sqlite3.connect(ROOT / 'data/catalog.sqlite3')
    sid = db.execute("SELECT id FROM subjects WHERE slug='mathematics'").fetchone()[0]
    db.execute("UPDATE subjects SET content_status='live' WHERE slug='mathematics'")
    paths = []
    for c in published:
        slug = c['slug']
        home = f'/mathematics/{slug}/'
        (out / home.lstrip('/')).mkdir(parents=True, exist_ok=True)
        rows = [observation(c, v) for v in c['samples']]
        f = fit(rows)
        for part, body in [
            ('experiment', workbench(c)),
            ('theory', '<section>' + theory(c) + f'<div class="insight"><span>↳</span><div><strong>Connect theory to numerical computation.</strong><p>{E(c["modelExtra"])}</p></div></div></section>'),
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
    config = json.loads((ROOT / 'site-config.json').read_text())
    base = config['base_url'].rstrip('/')
    out = ROOT / ('release' if args.production else 'dist')
    out.mkdir(exist_ok=True)
    paths = build_math(out, base, args.production)
    print(f"Built {len(paths)} Mathematics pages for {base}: {paths[:3]}...")
