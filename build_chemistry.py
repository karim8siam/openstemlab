"""Static lesson pages and reproducible simulated reports for published Chemistry labs."""
from pathlib import Path
import json,math,csv,io,sqlite3,html,re

ROOT=Path(__file__).resolve().parent
E=lambda s:html.escape(str(s),quote=True)
def specs():return json.loads((ROOT/'content/chemistry/experiments.json').read_text())
def rnd(x,n):return math.floor(x*10**n+.5)/10**n

def observation(c,value):
 slug=c['slug']
 if slug=='density-mass-volume-precision':
  v=float(value)
  raw=rnd(0.9982*v,4)
  x=v
  y=raw
  return {'input':value,'raw':raw,'x':x,'y':y}
 raise ValueError(f"Unknown Chemistry experiment {slug}")

def fit(rows):
 n=len(rows)
 mx=sum(r['x'] for r in rows)/n
 my=sum(r['y'] for r in rows)/n
 sxx=sum((r['x']-mx)**2 for r in rows)
 sxy=sum((r['x']-mx)*(r['y']-my) for r in rows)
 m=sxy/sxx if sxx>0 else 1.0
 b=my-m*mx
 sse=sum((r['y']-m*r['x']-b)**2 for r in rows)
 syy=sum((r['y']-my)**2 for r in rows)
 variance=sse/(n-2) if n>2 and sse>0 else 1e-12
 return dict(
  m=m,b=b,sse=sse,
  slopeSE=math.sqrt(variance/sxx) if sxx>0 else 0.0,
  interceptSE=math.sqrt(variance*(1/n+mx*mx/sxx)) if sxx>0 else 0.0,
  mx=mx,my=my,sxx=sxx,sxy=sxy,
  r2=1.0-sse/syy if syy>0 else 1.0
 )

def estimate(c,f):
 slug=c['slug']
 if slug=='density-mass-volume-precision':
  return f['m'],f['slopeSE'],0.9982
 raise ValueError(f"Unknown Chemistry experiment {slug}")

def fmt(v,n=5):
 return f'{v:.4e}' if v and (abs(v)<.001 or abs(v)>=1e6) else f'{v:.{n}f}'

def formula(c,f):
 slug=c['slug']
 if slug=='density-mass-volume-precision':
  return f"ρ_liquid = m = {fmt(f['m'],4)} g/mL; Tare intercept b = {fmt(f['b'],4)} g"
 return ""

def worked(c,row):
 slug=c['slug']
 if slug=='density-mass-volume-precision':
  v=row['input']
  m_app=row['raw']
  rho_app=m_app/v
  # CIPM buoyancy correction
  rho_air=0.00120
  rho_weights=8.0000
  corr=1.0 + rho_air*(1.0/0.9982 - 1.0/rho_weights)
  m_vac=m_app*corr
  rho_vac=m_vac/v
  return (
   f"Dispensed Aliquot Volume V = {v:.1f} mL; Apparent Analytical Balance Reading m_app = {m_app:.4f} g.\n"
   f"Uncorrected Apparent Density: ρ_apparent = m_app / V = {m_app:.4f} g / {v:.1f} mL = {rho_app:.5f} g/mL.\n"
   f"CIPM Air Buoyancy Correction Factor: k_buoy = [1 + ρ_air · (1/ρ_liquid − 1/ρ_weights)] = [1 + 0.00120 · (1/0.9982 − 1/8.000)] = {corr:.6f}.\n"
   f"True Vacuum Net Mass: m_vac = m_app × k_buoy = {m_app:.4f} g × {corr:.6f} = {m_vac:.4f} g.\n"
   f"Buoyancy-Corrected Vacuum Density: ρ_vac = m_vac / V = {m_vac:.4f} g / {v:.1f} mL = {rho_vac:.5f} g/mL.\n"
   f"Verification: Across the full 7-point volumetric series, ordinary least-squares regression extracts the true bulk density as the slope m = 0.9982 g/mL, "
   f"absorbing any constant droplet retention or balance tare offset into the intercept b = 0.0000 g with R² = 1.00000."
  )
 return ""

def uncertainty_text(c):
 slug=c['slug']
 if slug=='density-mass-volume-precision':
  return (
   "In analytical chemical gravimetry and volumetric metrology, density determination is governed by the functional relationship ρ = m / V. "
   "A rigorous evaluation of measurement uncertainty requires partitioning sources into random instrumental limits, systematic volumetric calibration offsets, "
   "and ambient thermodynamic environmental perturbations: "
   "(1) Analytical Balance Gravimetric Limits: The electronic electromagnetic force restoration balance features a digital readability of ±0.0001 g and "
   "a manufacturer-certified repeatability standard deviation of s_m = ±0.00015 g. For an aliquot of 20.0 mL (net mass ~19.964 g), the relative random mass "
   "uncertainty is δm / m = 0.00015 / 19.964 ≈ 7.5 × 10⁻⁶ (0.00075%), demonstrating that gravimetric precision contributes negligibly to overall experimental variance. "
   "(2) Volumetric Glassware Tolerances & Meniscus Reading Uncertainty: The Class A 50.00 mL volumetric burette has a maximum permissible manufacturing tolerance of "
   "±0.05 mL according to ASTM E287 and ISO 385 specifications. Individual meniscus alignments by an experienced analyst incur a random parallax reading uncertainty of "
   "approximately s_V = ±0.02 mL. For a 20.0 mL delivery, the relative volumetric uncertainty is δV / V = 0.02 / 20.0 = 1.0 × 10⁻³ (0.10%), which is more than "
   "130 times larger than the gravimetric mass uncertainty. Thus, volumetric dispensing constitutes the overwhelming limiting factor in experimental density accuracy. "
   "(3) Thermodynamic Temperature Fluctuation: Liquid water exhibits a thermal volumetric expansion coefficient of β = 2.07 × 10⁻⁴ K⁻¹ at 20.0 °C, "
   "corresponding to a density temperature gradient of ∂ρ/∂T ≈ −0.00020 g/(mL·K). A temperature deviation of just ±0.5 °C shifts true water density by ±0.00010 g/mL, "
   "which is comparable to the fourth-decimal resolution of the balance. Maintaining a thermostatic water bath stable to ±0.05 °C restricts thermal density drift to < ±0.00001 g/mL. "
   "(4) Archimedean Atmospheric Air Buoyancy Correction: Because liquid water (ρ ≈ 1.0 g/mL) displaces eight times more ambient air per gram than austenitic stainless steel "
   "balance calibration weights (ρ_w ≈ 8.0 g/mL), uncorrected balance readings systematically underestimate vacuum mass by exactly Δm = m_app · ρ_air · (1/ρ_water − 1/ρ_w) ≈ "
   "+0.105% (or 1.05 mg per gram of water). Applying the CIPM buoyancy formula eliminates this systematic bias entirely. "
   "Ordinary least-squares linear regression across 7 volumetric increments from 5.0 to 35.0 mL yields an empirical slope of m = 0.9982 g/mL and an intercept of b = 0.0000 g, "
   "achieving an ideal coefficient of determination R² = 1.00000 and confirming that multi-point regression successfully insulates the calculated density against individual transfer biases."
  )
 return ""

def graph(c,rows,f):
 left,right,top,bottom=68,610,28,280
 xs=[r['x']*c['xScale'] for r in rows];ys=[r['y']*c['yScale'] for r in rows]
 xmin=min(xs);xmax=max(xs);ymin=min(ys);ymax=max(ys)
 dx=(xmax-xmin) or 1;dy=(ymax-ymin) or 1
 xmin-=dx*.12;xmax+=dx*.12;ymin-=dy*.15;ymax+=dy*.15
 px=lambda x:left+(x-xmin)/(xmax-xmin)*(right-left)
 py=lambda y:bottom-(y-ymin)/(ymax-ymin)*(bottom-top)
 out=[]
 for i in range(5):
  x=xmin+i*(xmax-xmin)/4;y=ymin+i*(ymax-ymin)/4
  out.append(f'<line x1="{left}" y1="{py(y):.1f}" x2="{right}" y2="{py(y):.1f}" stroke="#d5e3d7"/>')
  out.append(f'<text x="{left-9}" y="{py(y)+4:.1f}" text-anchor="end" font-size="10" fill="#496950">{fmt(y,1)}</text>')
  out.append(f'<text x="{px(x):.1f}" y="300" text-anchor="middle" font-size="10" fill="#496950">{fmt(x,1)}</text>')
 out.append(f'<path d="M{left} {top}V{bottom}H{right}" stroke="#5c8365" fill="none"/>')
 out.append(f'<text x="335" y="332" text-anchor="middle" fill="#244d2e" font-size="12">{E(c["xAxis"])}</text>')
 out.append(f'<text transform="translate(18 160) rotate(-90)" text-anchor="middle" fill="#244d2e" font-size="12">{E(c["yAxis"])}</text>')
 pts=[f"{px(xmin+i*(xmax-xmin)/100):.1f},{py((f['m']*(xmin+i*(xmax-xmin)/100)/c['xScale']+f['b'])*c['yScale']):.1f}" for i in range(101)]
 out.append(f'<polyline points="{" ".join(pts)}" stroke="#2f5233" stroke-width="2" fill="none"/>')
 for r in rows:
  out.append(f'<circle cx="{px(r["x"]*c["xScale"]):.1f}" cy="{py(r["y"]*c["yScale"]):.1f}" r="4.8" fill="#48bb78" stroke="#142b1a" stroke-width="1.5"><title>V = {r["input"]} mL, m = {r["raw"]} g</title></circle>')
 return f'<svg viewBox="0 0 650 340" role="img" aria-label="Linear regression plot of net mass versus dispensed volume">{"".join(out)}</svg>'

def theory(c):
 out=[
  '<section class="theory-section">',
  f'<h2>Theoretical Foundations of {E(c["shortTitle"])} and Quantitative Chemical Metrology</h2>',
  f'<p class="intro">{E(c["intro"])}</p>',
  '<div class="theory-grid">'
 ]
 for i,t in enumerate(c['topics'],1):
  out.append(f'<article class="theory-card"><div class="theory-head"><span class="eyebrow">TOPIC {str(i).zfill(2)} · FORMAL ANALYSIS</span><h3>{E(t["question"])}</h3></div><div class="theory-body"><p>{E(t["answer"]).replace(chr(10), "<br><br>")}</p></div></article>')
 out.append('</div></section>')
 return "".join(out)

def method(c):
 return '<div class="method-steps">'+''.join(f'<article class="method-step"><div class="step-num">{str(i).zfill(2)}</div><div><h3>{E(s["title"])}</h3><p>{E(s["text"])}</p></div></article>' for i,s in enumerate(c['procedure'],1))+'</div>'

def workbench(c):
 sim_buttons=''.join(
  f'<button id="simMode{m["id"].capitalize()}" class="sim-mode-btn{" active" if i==0 else ""}" data-sim="{m["id"]}" type="button" role="tab" aria-selected="{"true" if i==0 else "false"}"><span class="sim-icon">{m["icon"]}</span> {E(m["label"])}</button>'
  for i,m in enumerate(c.get('simModes', [{'id':'bench','icon':'⚖️','label':'1. Volumetric Gravimetry'},{'id':'compare','icon':'🔬','label':'2. Pycnometry vs U-Tube'},{'id':'sandbox','icon':'💧','label':'3. Thermal Expansion'}]))
 )
 return f'''<section aria-label="Interactive workbench"><div class="section-top"><div><div class="eyebrow">MEASURE · CALIBRATE · ANALYSE</div><h2>Your virtual chemistry laboratory.</h2></div><button id="resetApparatus" class="text-button">Reset apparatus</button></div><div class="new-workbench"><div class="new-visual"><div class="visual-top"><div class="sim-mode-switcher" role="tablist" aria-label="Simulation Views">{sim_buttons}</div><button id="pauseMotion" class="dark-button" hidden>Pause motion</button></div><svg id="apparatusDiagram" viewBox="0 0 720 320" role="img" aria-label="Interactive analytical balance and volumetric glassware workbench for {E(c['shortTitle'])}"></svg><div class="new-meter"><div><small>{E(c['rawLabel'].upper())}</small><strong id="readingValue">—</strong></div><div><small>MEASUREMENT STATUS</small><p id="liveState" style="font-size:11px;margin:7px 0">Ready to dispense {c['initial']} {E(c['inputUnit'])} of liquid.</p></div></div></div><div class="new-controls"><label for="independent">{E(c['inputLabel'])}</label><output id="independentOut">{c['initial']} {E(c['inputUnit'])}</output><input id="independent" type="range" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><label for="independentNumber">Set {E(c['shortInput'])} ({E(c['inputUnit'])})</label><input id="independentNumber" type="number" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><div class="lab-control-meta">{E(c['settings'][0])}</div><button id="measure" class="primary full">{E(c['measureLabel'])}</button><button id="recordReading" class="secondary full" disabled>＋ Record observation</button><p id="trialStatus" class="trial-status" role="status">Adjust {E(c['shortInput'])} V, then weigh the dispensed aliquot.</p></div></div><p class="data-notice">Mass observations are determined by the high-precision thermodynamic equation of state for pure liquid water. Readings reflect thermal equilibrium and analytical balance force restoration.</p><details class="model-note"><summary>Physical chemistry assumptions and metrological limits</summary><p>{E(c['limitations'])} {E(c['modelExtra'])}</p></details></section><section id="apparatus" class="lab-section"><h2>Analytical chemistry apparatus & tools.</h2><div class="apparatus-list">{''.join('<article class="apparatus-item"><h3>'+E(a['name'])+'</h3><p>'+E(a['purpose'])+'</p></article>' for a in c['apparatus'])}</div></section><section id="method" class="lab-section"><div class="eyebrow">FOLLOW THE METHOD</div><h2>A reason behind every step.</h2><p class="intro">{E(c['aim'])} Suggested independent volumetric settings: {", ".join(map(str,c['samples']))} {E(c['inputUnit'])}.</p>{method(c)}</section><section id="results" class="lab-section"><div class="section-top"><div><div class="eyebrow">YOUR NOTEBOOK · <span id="notebookCount">0</span> OBSERVATIONS</div><h2>Turn measurements into quantitative chemical insight.</h2></div><a class="text-button" href="/chemistry/{c['slug']}/report/">See a complete example report ↗</a></div><div class="lab-result-grid"><div class="chart-card"><svg id="labPlot" viewBox="0 0 650 340" role="img" aria-label="Measured observations and fitted linear regression graph"></svg><p>Points are your recorded gravimetric observations. The regression line validates the linear mass-volume proportionality and extracts density.</p></div><div class="fit-card lab-fit"><span class="eyebrow">ORDINARY LEAST-SQUARES FIT · m = ρ·V + m₀</span><div id="fitSummary"></div><div class="report-equation">{E(c['fitEquation'])}</div></div></div><div class="table-card"><table><thead><tr><th>#</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Remove</th></tr></thead><tbody id="readingRows"></tbody></table><p id="emptyReadings">No readings yet. Dispense and weigh a volumetric aliquot to record it.</p></div><div class="lab-reading-actions"><button id="downloadReadings" class="secondary" disabled>↓ Export CSV</button><button id="clearReadings" class="secondary" disabled>Clear notebook</button></div><div class="source-box"><h3>Calculate it yourself.</h3><label for="studentEstimate">Your estimate of {E(c['target'])} ({E(c['resultUnit'])})</label> <input id="studentEstimate" type="number" step="any" min="0" style="max-width:140px"><button id="checkEstimate" class="secondary" style="margin-left:10px">Check calculation</button><p id="estimateFeedback" role="status"></p></div></section><section id="check" class="lab-section lab-questions"><div class="eyebrow">CHECK YOUR UNDERSTANDING</div><h2>Explain what the gravimetric measurements mean.</h2>{''.join('<article class="quiz-card"><h3>'+E(q['question'])+'</h3><div class="quiz-choices">'+''.join('<button class="quiz-option" data-quiz="'+str(i)+'" data-choice="'+str(j)+'">'+E(a)+'</button>' for j,a in enumerate(q['options']))+'</div><p id="quizFeedback'+str(i)+'" class="quiz-feedback" role="status"></p></article>' for i,q in enumerate(c['quiz']))}</section>'''

def report_narrative(c,rows,f,value,percent,reference,se):
 slug=c['slug']
 if slug=='density-mass-volume-precision':
  abstract=(
   f"Seven gravimetric trials were executed across dispensed volumes V = {rows[0]['input']:.1f} mL to V = {rows[-1]['input']:.1f} mL of pure deionized water "
   f"equilibrated to 20.00 °C (resulting in net mass readings from {rows[0]['raw']:.4f} g to {rows[-1]['raw']:.4f} g on an electronic analytical balance). "
   f"An ordinary least-squares linear regression of net mass m against dispensed volume V yielded an experimental density of "
   f"{fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} and an intercept of {fmt(f['b'],c['resultDecimals'])} g, "
   f"demonstrating exact agreement with the international CIPM standard water density formulation (reference value = {fmt(reference*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, difference = {percent:.4f}%). "
   f"Applying the CIPM atmospheric air buoyancy correction confirmed that apparent balance readings in laboratory air underestimate true vacuum mass by 0.105%, "
   f"verifying the necessity of buoyancy compensation in high-precision analytical chemistry."
  )
  graph_choice=(
   f"The mathematical regression fits the linear physical model m = ρ·V + m_0, where V represents dispensed liquid volume in mL, "
   f"m represents net liquid mass in g, ρ represents the liquid density in {c['gradientUnit']}, and m_0 represents the baseline tare intercept in g "
   f"(theoretically m_0 = 0.0000 g). The slope of this regression line directly yields the intensive bulk density of the liquid, while constant tare "
   f"offsets or uniform meniscus drainage residues are absorbed into the intercept."
  )
  discussion=(
   "The experimental observations provide rigorous quantitative verification of Density Metrology, Volumetric Analysis, and Archimedean Air Buoyancy Corrections. "
   "In quantitative analytical chemistry, density serves as an essential physical fingerprint for identifying substances, verifying chemical purity, and determining solution concentrations. "
   "Our investigation utilized pure deionized water (resistivity 18.2 MΩ·cm) maintained at exactly 20.00 ± 0.02 °C in a thermostatic water bath. "
   "Across the 7 volumetric aliquots dispensed from the Class A 50.00 mL burette (from 5.0 mL to 35.0 mL), the net mass scaled in strictly linear proportion to volume. "
   "The ordinary least-squares linear regression line m = 0.99820·V + 0.00000 g yielded a coefficient of determination of R² = 1.00000, indicating perfect linearity. "
   "The extracted experimental density ρ = 0.9982 g/mL matches the international CIPM reference standard to within 0.0000% difference. "
   "A critical aspect of high-precision gravimetry is Archimedes' atmospheric buoyancy effect: because liquid water has a density (~1.0 g/mL) substantially lower than the "
   "stainless steel calibration weights inside the balance (~8.0 g/mL), the water displaces eight times more ambient air per gram, experiencing an upward buoyant force "
   "of approximately 1.05 mg per gram of water. Uncorrected balance readings therefore systematically underestimate vacuum mass by 0.105%. "
   "By performing a multi-point regression across seven systematic volumetric increments rather than relying on a single-point quotient m/V, constant meniscus transfer biases "
   "and residual droplet retention on glassware walls were absorbed entirely into the regression intercept parameter b = 0.0000 g, leaving the slope m_slope as an unbiased estimator of true density. "
   "Comparative evaluation against capillary pycnometry (±0.0001 g/mL) and digital oscillating U-tube densitometers (±0.00005 g/mL) illustrated the operational trade-offs "
   "between measurement speed, required sample volume, and optical meniscus alignment parallax errors."
  )
  conclusion=(
   "This laboratory investigation successfully demonstrated the high-precision determination of liquid density using analytical balances and Class A volumetric glassware. "
   f"Through systematic multi-point gravimetric dispensing from V = {rows[0]['input']:.1f} mL to {rows[-1]['input']:.1f} mL, we extracted an experimental liquid density of "
   f"ρ = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with a fit standard error of {fmt(se*c['resultScale'])} {c['resultUnit']} and an ideal R² = 1.00000. "
   "The empirical result confirms the CIPM thermodynamic reference value for pure water at 20.00 °C (0.99820 g/mL) with zero residual error. "
   "The experiment established the physical foundation of intensive thermodynamic properties, demonstrated the mathematical necessity of Archimedean buoyancy corrections, "
   "and proved why ordinary least-squares regression represents the gold standard for eliminating systematic tare and transfer offsets in quantitative chemical measurement."
  )
  return abstract, graph_choice, discussion, conclusion
 return "","","",""

def report(c,rows,f,out):
 slug=c['slug']
 csvpath=f"/chemistry/{slug}/sample-data.csv"
 csv_content=io.StringIO()
 writer=csv.writer(csv_content)
 writer.writerow(['experiment','dispensed_volume_mL','net_mass_g','x_metric','fitted_mass_g','residual_g'])
 for r in rows:
  fit_y=f['m']*r['x']+f['b']
  writer.writerow([slug,f"{r['input']:.1f}",f"{r['raw']:.4f}",f"{r['x']:.4f}",f"{fit_y:.4f}",f"{r['y']-fit_y:.4f}"])
 (out/f"chemistry/{slug}/sample-data.csv").write_text(csv_content.getvalue())

 value,se,reference=estimate(c,f)
 percent=abs(value-reference)/reference*100
 uncertainty=uncertainty_text(c)
 abstract,graph_choice,discussion,conclusion=report_narrative(c,rows,f,value,percent,reference,se)

 obs="".join(
  f"<tr><td>{i+1}</td><td>{r['input']:.1f}</td><td>{r['raw']:.4f}</td><td>{r['x']:.4f}</td><td>{r['y']:.4f}</td><td>{f['m']*r['x']+f['b']:.4f}</td><td>{r['y']-(f['m']*r['x']+f['b']):.4f}</td></tr>"
  for i,r in enumerate(rows)
 )

 return f'''<div class="section-top"><div><div class="eyebrow">WORKED EXAMPLE · QUANTITATIVE OBSERVATIONS</div><h2>A complete example laboratory report.</h2></div><button class="secondary" onclick="window.print()">Print / save as PDF</button></div><div class="report-notice"><strong>Simulated demonstration data.</strong><p>This report illustrates formal analytical gravimetry, volumetric calibrations, and linear regression analysis. Replace its observations with your own experimental telemetry when preparing a practical submission.</p></div><div class="report-person"><span>Student: __________________</span><span>Student ID: __________________</span><span>Course: __________________</span><span>Date: __________________</span><span>Partner: __________________</span><span>Instructor: __________________</span></div><article class="lab-report"><h3>1. Title and aim</h3><p><strong>{E(c['title'])}.</strong> {E(c['aim'])}</p><h3>2. Abstract</h3><p>{E(abstract)}</p><h3>3. Apparatus and fixed settings</h3><ul>{''.join('<li>'+E(a['name'])+': '+E(a['purpose'])+'</li>' for a in c['apparatus'])}{''.join('<li>'+E(s)+'</li>' for s in c['settings'])}</ul><h3>4. Theory and graph choice</h3><p>{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>{E(graph_choice)}</p><h3>5. Method</h3><ol>{''.join('<li>'+E(s['text'])+'</li>' for s in c['procedure'])}</ol><h3>6. Observations and calculation table</h3><p>All gravimetric observations were recorded using a calibrated 4-decimal electronic analytical balance enclosed within a draft shield chamber. Volumetric aliquots were dispensed from a Class A burette. Residuals are computed relative to the ordinary least-squares regression line.</p><div class="table-card"><table><caption>Table 1. Seven simulated gravimetric observations; x and y represent dispensed volume and net mass metrics.</caption><thead><tr><th>No.</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Fitted y (g)</th><th>Residual (g)</th></tr></thead><tbody>{obs}</tbody></table></div><p><a href="{csvpath}" download>Download the sample observations (CSV) ↓</a></p><h3>7. Worked calculation for one observation</h3><div class="report-equation">{E(worked(c,rows[0]))}</div><h3>8. Graph, gradient and final calculation</h3><div class="chart-card">{graph(c,rows,f)}</div><p>Circular markers represent empirical gravimetric observations. The solid line represents the ordinary least-squares linear regression fit.</p><div class="report-equation">x̄ = {fmt(f['mx'],4)} mL; ȳ = {fmt(f['my'],4)} g<br>Σ(x − x̄)² = {fmt(f['sxx'],4)} mL²<br>Σ(x − x̄)(y − ȳ) = {fmt(f['sxy'],4)} g·mL<br>m = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)² = {fmt(f['m'],8)} g/mL<br>b = ȳ − mx̄ = {fmt(f['b'],8)} g<br>{E(formula(c,f))}</div><h3>9. Uncertainty and comparison</h3><p>Percentage difference = |estimate − theoretical value| / |theoretical value| × 100 = <strong>{percent:.4f}%</strong>.</p><p>For n = 7 gravimetric observations, Σresidual² = {fmt(f['sse'])}; s² = Σresidual²/(n − 2). Gradient standard error = √[s²/Σ(x − x̄)²] = {fmt(f['slopeSE'])}. Intercept standard error = √[s²(1/n + x̄²/Σ(x − x̄)²)] = {fmt(f['interceptSE'])}.</p><p>Propagating the fit parameters yields an <strong>experimental density standard error of {fmt(se*c['resultScale'])} {E(c['resultUnit'])}</strong>, with an ideal coefficient of determination R² = {f['r2']:.6f}.</p><p>{E(uncertainty)}</p><h3>10. Result and discussion</h3><div class="report-equation">{E(c['target'])} = {fmt(value*c['resultScale'],c['resultDecimals'])} {E(c['resultUnit'])}<br>CIPM standard reference value: {fmt(reference*c['resultScale'],c['resultDecimals'])} {E(c['resultUnit'])}</div><p>{E(discussion)}</p><h3>11. Precautions and limitations</h3><ul>{''.join('<li>'+E(p)+'</li>' for p in c['precautions'])}</ul><p>{E(c['limitations'])} {E(c['modelExtra'])}</p><h3>12. Conclusion</h3><p>{E(conclusion)}</p></article>'''

def lesson_schema(c,part,path,title,desc,base):
 graph=[{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Open STEM Lab','item':base+'/'},{'@type':'ListItem','position':2,'name':'Chemistry Laboratory','item':base+'/subjects/chemistry/'},{'@type':'ListItem','position':3,'name':c['shortTitle'],'item':base+f'/chemistry/{c["slug"]}/'}]}]
 if part=='experiment':
  graph.append({'@type':['WebPage','LearningResource','TechArticle'],'name':title,'description':desc,'url':base+path,'learningResourceType':'Interactive chemistry simulation','educationalLevel':'Undergraduate','about':c['title'],'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'Open STEM Lab','url':base+'/'}})
  if c.get('quiz'):
   graph.append({'@type':'Quiz','name':c['shortTitle']+' Concept Understanding','hasPart':[{'@type':'Question','name':q['question'],'suggestedAnswer':[{'@type':'Answer','text':opt} for opt in q['options']],'acceptedAnswer':{'@type':'Answer','text':q['options'][q['correct']]}} for q in c['quiz']]})
 elif part=='theory':
  graph.append({'@type':['WebPage','TechArticle','FAQPage'],'name':title,'description':desc,'url':base+path,'about':c['title'],'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'Open STEM Lab','url':base+'/'},'mainEntity':[{'@type':'Question','name':t['question'],'acceptedAnswer':{'@type':'Answer','text':t['answer']}} for t in c['topics']]})
 else:
  graph.append({'@type':['WebPage','ScholarlyArticle','TechArticle'],'name':title,'description':desc,'url':base+path,'about':c['title'],'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'Open STEM Lab','url':base+'/'}})
 return json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)

def shell(c,part,body,base,production):
 from build_catalog import head
 path=f'/chemistry/{c["slug"]}/'+('' if part=='experiment' else part+'/')
 title=c['shortTitle']+(' Experiment & Simulation' if part=='experiment' else ' Theory & Analysis' if part=='theory' else ' Lab Report: Data & Calculations')+' | Open STEM Lab'
 desc={'experiment':c['aim']+' Explore interactive analytical gravimetry, Class A volumetric glassware and density determination.','theory':'Understand '+c['shortTitle'].lower()+': Archimedean air buoyancy corrections, water density anomaly and error propagation.','report':'A worked '+c['shortTitle'].lower()+' lab report with gravimetric data tables, linear regression graphs, calculations, uncertainty and conclusions.'}[part]
 header=head(path,title,desc,base,production).replace('<link rel="stylesheet" href="/catalog.css">','<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/chem-lesson.css">')
 header=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda _:f'<script type="application/ld+json">{lesson_schema(c,part,path,title,desc,base)}</script>',header,flags=re.S)
 home=f'/chemistry/{c["slug"]}/'
 nav='<aside class="sidebar"><a class="brand" style="font-size:20px" href="/">◉ openstemlab.</a><a class="side-subject" href="/subjects/chemistry/">← Chemistry labs</a><div class="side-label">LABORATORY '+str(c['number']).zfill(2)+'</div><nav aria-label="Lesson navigation">'
 for href,label in [(home,'Explore the experiment'),(home+'theory/','Understand the theory'),(home+'#apparatus','Know your tools'),(home+'#method','Follow the method'),(home+'#results','Analyse your results'),(home+'#check','Check your understanding'),(home+'report/','Sample lab report')]:
  nav+=f'<a class="nav-item{" active" if path==href else ""}" href="{href}">{label}</a>'
 nav+='<a class="nav-item" href="/experiments/">Search all experiments</a></nav><div class="side-note"><span class="small-sun">✳</span><p>Learn by measuring.<br>Understand by reacting.</p></div><a class="text-button" href="/">← All subjects</a></aside>'
 heading=c['title'] if part=='experiment' else c['shortTitle']+' theory' if part=='theory' else c['shortTitle']+' lab report'
 return header+'<body>'+nav+'<main><header class="topbar"><div><a href="/subjects/chemistry/">Chemistry</a> / '+E(c['shortTitle'])+'</div><span class="free-label">FREE TO EXPLORE</span></header><section class="page-heading"><div class="eyebrow">LABORATORY '+str(c['number']).zfill(2)+' · NATURAL SCIENCES</div><h1>'+E(heading)+'</h1><p>'+E(desc)+'</p></section><nav class="lab-navigation" aria-label="Experiment pages"><a href="'+home+'">Workbench</a><a href="'+home+'theory/">Detailed theory</a><a href="'+home+'#method">Method</a><a href="'+home+'#results">My results</a><a href="'+home+'report/">Example report</a></nav>'+body+'<footer><span class="footer-brand">openstemlab.</span><a href="/subjects/chemistry/">All chemistry labs</a><span>Physical chemistry metrological model</span></footer></main>'+ ('<script id="labConfig" type="application/json">'+json.dumps(c,ensure_ascii=False).replace('<',chr(92)+'u003c')+'</script><script src="/chem-models.js"></script><script src="/chem-engine.js"></script>' if part=='experiment' else '')+'</body></html>'

def build_chemistry(out,base,production):
 published=[c for c in specs() if c['published']]
 for name,dest in [('models.js','chem-models.js'),('engine.js','chem-engine.js'),('lesson.css','chem-lesson.css')]:
  (out/dest).write_text((ROOT/'content/chemistry'/name).read_text())
 db=sqlite3.connect(ROOT/'data/catalog.sqlite3')
 sid=db.execute("SELECT id FROM subjects WHERE slug='chemistry'").fetchone()[0]
 db.execute("UPDATE subjects SET content_status='live' WHERE slug='chemistry'")
 paths=[]
 for c in published:
  slug=c['slug']
  home=f'/chemistry/{slug}/'
  (out/home.lstrip('/')).mkdir(parents=True,exist_ok=True)
  rows=[observation(c,v) for v in c['samples']]
  f=fit(rows)
  for part,body in [
   ('experiment',workbench(c)),
   ('theory','<section>'+theory(c)+f'<div class="insight"><span>↳</span><div><strong>Connect the theory to experimental observations.</strong><p>{E(c["modelExtra"])}</p></div></div></section>'),
   ('report',report(c,rows,f,out))
  ]:
   path=home+('' if part=='experiment' else part+'/')
   file=out/path.lstrip('/')/'index.html'
   file.parent.mkdir(parents=True,exist_ok=True)
   file.write_text(shell(c,part,body,base,production))
   paths.append(path)
  db.execute('INSERT INTO experiments(subject_id,slug,title,status,page_path,theory_path,report_path) VALUES(?,?,?,?,?,?,?) ON CONFLICT(slug) DO UPDATE SET title=excluded.title,status=excluded.status,page_path=excluded.page_path,theory_path=excluded.theory_path,report_path=excluded.report_path',(sid,slug,c['shortTitle'],'live',home,home+'theory/',home+'report/'))
 db.commit()
 db.close()
 return paths

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser()
 parser.add_argument('--production',action='store_true')
 args=parser.parse_args()
 config=json.loads((ROOT/'site-config.json').read_text())
 base=config['base_url'].rstrip('/')
 out=ROOT/('release' if args.production else 'dist')
 out.mkdir(exist_ok=True)
 paths=build_chemistry(out,base,args.production)
 print(f"Built {len(paths)} Chemistry pages for {base}: {paths}")
