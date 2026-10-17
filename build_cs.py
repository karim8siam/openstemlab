"""Static lesson pages and reproducible simulated reports for published Computer Science labs."""
from pathlib import Path
import json,math,csv,io,sqlite3,html,re

ROOT=Path(__file__).resolve().parent
E=lambda s:html.escape(str(s),quote=True)
def specs():return json.loads((ROOT/'content/cs/experiments.json').read_text())
def rnd(x,n):return math.floor(x*10**n+.5)/10**n

def observation(c,value):
 slug=c['slug']
 if slug=='search-algorithms-complexity':
  n=float(value)
  x=math.log2(n)
  raw=int(math.floor(x)+1)
  y=float(raw)
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='quadratic-sorting-algorithms':
  n=float(value)
  x=n*(n-1.0)
  raw=int(n*(n-1.0)/2.0)
  y=float(raw)
  return {'input':value,'raw':raw,'x':x,'y':y}
 raise ValueError(f"Unknown CS experiment {slug}")

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
 if slug=='search-algorithms-complexity':
  return f['m'],f['slopeSE'],1.0000
 elif slug=='quadratic-sorting-algorithms':
  return f['m'],f['slopeSE'],0.5000
 raise ValueError(f"Unknown CS experiment {slug}")

def fmt(v,n=5):
 return f'{v:.4e}' if v and (abs(v)<.001 or abs(v)>=1e6) else f'{v:.{n}f}'

def formula(c,f):
 slug=c['slug']
 if slug=='search-algorithms-complexity':
  val=f['m']*c['resultScale']
  return f"k_search = m = {fmt(val,c['resultDecimals'])} comparisons/bit; Intercept b = {fmt(f['b'],c['resultDecimals'])} comparisons (theoretical intercept = 1.0000)"
 elif slug=='quadratic-sorting-algorithms':
  val=f['m']*c['resultScale']
  return f"a_quad = m = {fmt(val,c['resultDecimals'])} comparisons/pair; Intercept b = {fmt(f['b'],c['resultDecimals'])} comparisons (theoretical a = 0.5000, b = 0.0000)"
 return ""

def worked(c,row):
 slug=c['slug']
 if slug=='search-algorithms-complexity':
  n=row['input']
  log2n=row['x']
  c_max=row['raw']
  return f"Array Size n = {int(n)} keys; Key Entropy log₂(n) = log₂({int(n)}) = {log2n:.4f} bits.\nWorst-Case Binary Search Key Comparisons: C_max = ⌊log₂(n)⌋ + 1 = ⌊{log2n:.4f}⌋ + 1 = {c_max} comparisons.\nVerification: At each step, remaining search space halves from {int(n)} ⟶ {int(n)//2} ⟶ {int(n)//4} ... terminating in exactly {c_max} iterations."
 elif slug=='quadratic-sorting-algorithms':
  n=row['input']
  x_pairs=row['x']
  c_ops=row['raw']
  return f"Array Size n = {int(n)} keys; Directed Pair Space n(n − 1) = {int(n)} × {int(n)-1} = {int(x_pairs)} pairs.\nTotal Unordered Pairs to Compare: C = n(n − 1) / 2 = {int(x_pairs)} / 2 = {c_ops} comparisons.\nVerification: In each pass i from 0 to n−2, exactly n − 1 − i comparisons occur: (n−1) + (n−2) + ... + 1 = {c_ops} comparisons."
 return ""

def uncertainty_text(c):
 slug=c['slug']
 if slug=='search-algorithms-complexity':
  return (
   "In deterministic comparison-based algorithm analysis, the theoretical worst-case operation count C_max(n) = ⌊log₂ n⌋ + 1 is an exact mathematical invariant. "
   "Unlike continuous physical instrumentation, there is no analog sensor noise, thermal fluctuation, or calibration drift in counting atomic discrete machine instructions. "
   "However, in physical semiconductor computers, wall-clock execution latency deviates from pure mathematical comparison counts due to hardware microarchitectural phenomena: "
   "(1) L1/L2/L3 cache line hierarchy fills and Translation Lookaside Buffer (TLB) virtual memory page walks; "
   "(2) Branch predictor mispredictions in conditional jumps (`if (A[mid] < K)`), which flush deep 14-to-20 stage microprocessor execution pipelines and incur 15 to 20 cycle stalls; "
   "(3) Hardware spatial prefetchers, which optimize sequential linear access patterns over random binary bisections for small arrays (n ≤ 64); and "
   "(4) Operating system preemptive kernel scheduling interrupts and thread context switches. "
   "Ordinary least-squares regression across systematically doubled array sizes n in [64, 4096] extracts the fundamental scaling multiplier k_search = 1.0000 comparisons/bit with zero residual variance (R² = 1.00000), verifying the asymptotic divide-and-conquer bound Θ(log₂ n) with mathematical certitude."
  )
 elif slug=='quadratic-sorting-algorithms':
  return (
   "In combinatorial sorting analysis, the comparison count C(n) = n(n − 1)/2 for Selection Sort and worst-case Bubble Sort is an exact deterministic combinatorial identity. "
   "Unlike noisy analog experimental instrumentation, discrete step counting in virtual machine execution registers exhibits zero random measurement error. "
   "However, physical hardware execution is influenced by microarchitectural phenomena: "
   "(1) L1 data cache spatial locality, where contiguous in-place array iterations execute with ~1 ns latency; "
   "(2) Branch predictor mispredictions during conditional element checks (`if (A[j] < A[min])`), which stall superscalar execution pipelines by 15–20 clock cycles; "
   "(3) Memory bus write contention during element swaps, where Selection Sort's O(n) write profile heavily outperforms Bubble Sort's O(n²) write churn; and "
   "(4) CPU dynamic frequency scaling under continuous nested-loop arithmetic. "
   "Ordinary least-squares linear regression of observed comparisons against permutation pair space x = n(n − 1) yields an empirical scaling slope a_quad = 0.5000 comparisons/pair with zero residual error (R² = 1.00000), rigorously verifying the quadratic complexity bound Θ(n²)."
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
  out.append(f'<line x1="{left}" y1="{py(y):.1f}" x2="{right}" y2="{py(y):.1f}" stroke="#dbe5eb"/>')
  out.append(f'<text x="{left-9}" y="{py(y)+4:.1f}" text-anchor="end" font-size="10" fill="#5a7687">{fmt(y,2)}</text>')
  out.append(f'<text x="{px(x):.1f}" y="300" text-anchor="middle" font-size="10" fill="#5a7687">{fmt(x,2)}</text>')
 out.append(f'<path d="M{left} {top}V{bottom}H{right}" stroke="#8ba5b5" fill="none"/>')
 out.append(f'<text x="335" y="332" text-anchor="middle" fill="#2b546b" font-size="12">{E(c["xAxis"])}</text>')
 out.append(f'<text transform="translate(15 160) rotate(-90)" text-anchor="middle" fill="#2b546b" font-size="12">{E(c["yAxis"])}</text>')
 pts=[f"{px(xmin+i*(xmax-xmin)/100):.1f},{py((f['m']*(xmin+i*(xmax-xmin)/100)/c['xScale']+f['b'])*c['yScale']):.1f}" for i in range(101)]
 out.append(f'<polyline points="{" ".join(pts)}" stroke="#1e3e52" stroke-width="2" fill="none"/>')
 for r in rows:
  out.append(f'<circle cx="{px(r["x"]*c["xScale"]):.1f}" cy="{py(r["y"]*c["yScale"]):.1f}" r="4.8" fill="#c05621"><title>n = {r["input"]}</title></circle>')
 return f'<svg viewBox="0 0 650 340" role="img" aria-label="Asymptotic regression plot of key comparisons against logarithmic entropy">{"".join(out)}</svg>'

def theory(c):
 out=[
  '<section class="theory-section">',
  f'<h2>Theoretical Foundations of {E(c["shortTitle"])} and Computational Complexity</h2>',
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
  for i,m in enumerate(c.get('simModes', [{'id':'bench','icon':'🔬','label':'1. Algorithm Bench'},{'id':'compare','icon':'⚖️','label':'2. Complexity Comparison'},{'id':'sandbox','icon':'⚛️','label':'3. Dynamic Sandbox'}]))
 )
 return f'''<section aria-label="Interactive workbench"><div class="section-top"><div><div class="eyebrow">COMPUTE · BENCHMARK · ANALYSE</div><h2>Your virtual algorithm laboratory.</h2></div><button id="resetApparatus" class="text-button">Reset benchmark</button></div><div class="new-workbench"><div class="new-visual"><div class="visual-top"><div class="sim-mode-switcher" role="tablist" aria-label="Simulation Views">{sim_buttons}</div><button id="pauseMotion" class="dark-button" hidden>Pause motion</button></div><svg id="apparatusDiagram" viewBox="0 0 720 320" role="img" aria-label="Interactive virtual array and comparator for {E(c['shortTitle'])}"></svg><div class="new-meter"><div><small>{E(c['rawLabel'].upper())}</small><strong id="readingValue">—</strong></div><div><small>EXECUTION STATUS</small><p id="liveState" style="font-size:11px;margin:7px 0">Ready to execute {E(c['shortInput'])} benchmark.</p></div></div></div><div class="new-controls"><label for="independent">{E(c['inputLabel'])}</label><output id="independentOut">{c['initial']} {E(c['inputUnit'])}</output><input id="independent" type="range" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><label for="independentNumber">Set {E(c['shortInput'])} ({E(c['inputUnit'])})</label><input id="independentNumber" type="number" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><div class="lab-control-meta">{E(c['settings'][0])}</div><button id="measure" class="primary full">{E(c['measureLabel'])}</button><button id="recordReading" class="secondary full" disabled>＋ Record observation</button><p id="trialStatus" class="trial-status" role="status">Adjust {E(c['shortInput'])} n, then execute benchmark.</p></div></div><p class="data-notice">Operation counts are generated deterministically by the exact algorithmic execution model. Modern hardware benchmarks additionally reflect cache line prefetching and branch misprediction penalties.</p><details class="model-note"><summary>Algorithmic assumptions and limits</summary><p>{E(c['limitations'])} {E(c['modelExtra'])}</p></details></section><section id="apparatus" class="lab-section"><h2>Computational tools & environment.</h2><div class="apparatus-list">{''.join('<article class="apparatus-item"><h3>'+E(a['name'])+'</h3><p>'+E(a['purpose'])+'</p></article>' for a in c['apparatus'])}</div></section><section id="method" class="lab-section"><div class="eyebrow">FOLLOW THE METHOD</div><h2>A reason behind every step.</h2><p class="intro">{E(c['aim'])} Suggested independent settings: {", ".join(map(str,c['samples']))} {E(c['inputUnit'])}.</p>{method(c)}</section><section id="results" class="lab-section"><div class="section-top"><div><div class="eyebrow">YOUR NOTEBOOK · <span id="notebookCount">0</span> OBSERVATIONS</div><h2>Turn measurements into asymptotic insight.</h2></div><a class="text-button" href="/computer-science/{c['slug']}/report/">See a complete example report ↗</a></div><div class="lab-result-grid"><div class="chart-card"><svg id="labPlot" viewBox="0 0 650 340" role="img" aria-label="Measured observations and fitted asymptotic graph"></svg><p>Points are your recorded benchmark observations. The regression line validates {E(c['shortTitle'])} complexity scaling.</p></div><div class="fit-card lab-fit"><span class="eyebrow">LINEAR ASYMPTOTIC FIT · y = mx + b</span><div id="fitSummary"></div><div class="report-equation">{E(c['fitEquation'])}</div></div></div><div class="table-card"><table><thead><tr><th>#</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Remove</th></tr></thead><tbody id="readingRows"></tbody></table><p id="emptyReadings">No readings yet. Execute a {E(c['shortInput'])} benchmark and record it.</p></div><div class="lab-reading-actions"><button id="downloadReadings" class="secondary" disabled>↓ Export CSV</button><button id="clearReadings" class="secondary" disabled>Clear notebook</button></div><div class="source-box"><h3>Calculate it yourself.</h3><label for="studentEstimate">Your estimate of {E(c['target'])} ({E(c['resultUnit'])})</label> <input id="studentEstimate" type="number" step="any" min="0" style="max-width:140px"><button id="checkEstimate" class="secondary" style="margin-left:10px">Check calculation</button><p id="estimateFeedback" role="status"></p></div></section><section id="check" class="lab-section lab-questions"><div class="eyebrow">CHECK YOUR UNDERSTANDING</div><h2>Explain what the operation counts mean.</h2>{''.join('<article class="quiz-card"><h3>'+E(q['question'])+'</h3><div class="quiz-choices">'+''.join('<button class="quiz-option" data-quiz="'+str(i)+'" data-choice="'+str(j)+'">'+E(a)+'</button>' for j,a in enumerate(q['options']))+'</div><p id="quizFeedback'+str(i)+'" class="quiz-feedback" role="status"></p></article>' for i,q in enumerate(c['quiz']))}</section>'''

def report_narrative(c,rows,f,value,percent,reference):
 slug=c['slug']
 if slug=='search-algorithms-complexity':
  abstract=(
   f"Seven benchmark trials were generated across input sizes n = {rows[0]['input']} to n = {rows[-1]['input']} {c['inputUnit']}. "
   f"An ordinary least-squares regression of worst-case key comparisons against logarithmic entropy log₂(n) yielded an empirical complexity multiplier of "
   f"{fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, demonstrating exact agreement with the theoretical divide-and-conquer bound "
   f"(difference = {percent:.4f}%). The results empirically prove that Binary Search exhibits optimal Θ(log₂ n) asymptotic scaling, outperforming "
   f"linear search by a factor of over 315× at n = {rows[-1]['input']}."
  )
  graph_choice=(
   f"The mathematical regression fits the linear model y = mx + b, where x = log₂(n) represents input entropy in bits, "
   f"y = C represents discrete key comparisons, m represents the logarithmic scaling factor, and b represents baseline termination "
   f"comparison overhead. The gradient has physical units {c['gradientUnit']}."
  )
  discussion=(
   "The empirical benchmark observations perfectly align with the theoretical divide-and-conquer recurrence T(n) = T(n/2) + O(1). "
   "The slope m = 1.0000 confirms that exactly one additional comparison is required each time the dataset size doubles, illustrating "
   "how logarithmic algorithms tame exponential data volume growth in modern computer systems."
  )
  conclusion=(
   "This laboratory investigation quantitatively demonstrated the asymptotic complexity of search algorithms. Through empirical "
   f"benchmarking across arrays ranging from {rows[0]['input']} to {rows[-1]['input']} elements, we verified that Binary Search achieves "
   f"an optimal logarithmic scaling gradient of k_search = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, matching "
   "the theoretical bound with zero residual error. The experiment highlights why divide-and-conquer is a foundational paradigm of modern "
   "computational infrastructure."
  )
 elif slug=='quadratic-sorting-algorithms':
  abstract=(
   f"Seven benchmark trials were generated across input sizes n = {rows[0]['input']} to n = {rows[-1]['input']} elements "
   f"(permutation pair space x = n(n − 1) from {int(rows[0]['x'])} to {int(rows[-1]['x'])} pairs). An ordinary least-squares regression "
   f"of key comparisons C against permutation pair space yielded an empirical quadratic scaling coefficient of "
   f"{fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, demonstrating exact agreement with the combinatorial identity "
   f"C(n) = 1/2 n(n − 1) (difference = {percent:.4f}%). The empirical telemetry proves that while Bubble, Selection, and Insertion Sort "
   f"all share Θ(n²) worst-case comparison complexity, Selection Sort strictly minimizes memory bus write amplification to at most n − 1 "
   f"element swaps (2n − 2 writes), compared to Bubble Sort's up to n(n − 1)/2 swaps (~3× writes per swap), explaining why Selection Sort "
   "is preferred in Flash/EEPROM architectures."
  )
  graph_choice=(
   f"The mathematical regression fits the linear model y = mx + b, where x = n(n − 1) represents the total permutation pair space in pairs, "
   f"y = C represents discrete key comparisons, m represents the quadratic scaling coefficient a_quad, and b represents baseline comparison "
   f"overhead. The gradient has physical units {c['gradientUnit']}."
  )
  discussion=(
   "The empirical benchmark observations perfectly align with the combinatorial pair summation C(n) = ∑_{i=1}^{n-1} (n − i) = n(n − 1)/2. "
   "The slope m = 0.5000 confirms that exactly half of the directed pair space is compared in an unordered array. Furthermore, the inversion "
   "analysis demonstrates why any algorithm relying strictly on adjacent element swaps requires Ω(n²) comparisons on average, as each adjacent "
   "swap can eliminate at most one Kendall-tau inversion from an initial expectation of n(n − 1)/4 inversions. Finally, the hardware telemetry "
   f"highlights the critical trade-off between comparisons and memory write amplification: Selection Sort achieves identical comparisons "
   f"to Bubble Sort while reducing physical memory writes by a factor of over 35× at n = {rows[-1]['input']}."
  )
  conclusion=(
   "This laboratory investigation quantitatively verified the asymptotic complexity and microarchitectural behavior of quadratic sorting "
   f"algorithms. Through systematic benchmarking across arrays from {rows[0]['input']} to {rows[-1]['input']} elements, we verified the "
   f"quadratic scaling multiplier a_quad = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, matching theoretical predictions "
   "with an ideal R² = 1.00000. The investigation established the theoretical necessity of non-adjacent partition and exchange primitives "
   "(such as Quicksort and Heapsort) to overcome the Ω(n²) barrier imposed by pairwise adjacent transpositions."
  )
 else:
  abstract=f"Empirical benchmark trials were generated across input sizes for {c['title']}."
  graph_choice=f"Regression fits y = mx + b for {c['fitEquation']}."
  discussion=f"Empirical observations align with theoretical bound {fmt(reference*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}."
  conclusion=f"Quantitative benchmarking verified complexity scaling for {c['title']}."
 return abstract, graph_choice, discussion, conclusion

def report(c,rows,f,out):
 slug=c['slug']
 csvpath=f"/computer-science/{slug}/sample-data.csv"
 csv_content=io.StringIO()
 writer=csv.writer(csv_content)
 writer.writerow(['experiment',c['shortInput'].replace(' ','_')+'_n','key_comparisons','x_metric','fitted_comparisons','residual'])
 for r in rows:
  fit_y=f['m']*r['x']+f['b']
  writer.writerow([slug,r['input'],r['raw'],f"{r['x']:.4f}",f"{fit_y:.4f}",f"{r['y']-fit_y:.4f}"])
 (out/f"computer-science/{slug}/sample-data.csv").write_text(csv_content.getvalue())

 value,se,reference=estimate(c,f)
 percent=abs(value-reference)/reference*100
 uncertainty=uncertainty_text(c)
 abstract,graph_choice,discussion,conclusion=report_narrative(c,rows,f,value,percent,reference)

 obs="".join(
  f"<tr><td>{i+1}</td><td>{r['input']}</td><td>{r['raw']}</td><td>{r['x']:.4f}</td><td>{r['y']:.4f}</td><td>{f['m']*r['x']+f['b']:.4f}</td><td>{r['y']-(f['m']*r['x']+f['b']):.4f}</td></tr>"
  for i,r in enumerate(rows)
 )

 return f'''<div class="section-top"><div><div class="eyebrow">WORKED EXAMPLE · BENCHMARK OBSERVATIONS</div><h2>A complete example laboratory report.</h2></div><button class="secondary" onclick="window.print()">Print / save as PDF</button></div><div class="report-notice"><strong>Simulated demonstration data.</strong><p>This report illustrates formal algorithmic benchmarking, operation counting arithmetic, and regression analysis. Replace its observations with your own benchmark telemetry when preparing a practical submission.</p></div><div class="report-person"><span>Student: __________________</span><span>Student ID: __________________</span><span>Course: __________________</span><span>Date: __________________</span><span>Partner: __________________</span><span>Instructor: __________________</span></div><article class="lab-report"><h3>1. Title and aim</h3><p><strong>{E(c['title'])}.</strong> {E(c['aim'])}</p><h3>2. Abstract</h3><p>{E(abstract)}</p><h3>3. Apparatus and fixed settings</h3><ul>{''.join('<li>'+E(a['name'])+': '+E(a['purpose'])+'</li>' for a in c['apparatus'])}{''.join('<li>'+E(s)+'</li>' for s in c['settings'])}</ul><h3>4. Theory and graph choice</h3><p>{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>{E(graph_choice)}</p><h3>5. Method</h3><ol>{''.join('<li>'+E(s['text'])+'</li>' for s in c['procedure'])}</ol><h3>6. Observations and calculation table</h3><p>All benchmark observations use strictly controlled memory buffers. Values are recorded deterministically from the algorithmic comparator register. Residuals are computed relative to the ordinary least-squares regression line.</p><div class="table-card"><table><caption>Table 1. Seven simulated algorithmic benchmarks; x and y represent computational state metrics.</caption><thead><tr><th>No.</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Fitted y</th><th>Residual</th></tr></thead><tbody>{obs}</tbody></table></div><p><a href="{csvpath}" download>Download the sample observations (CSV) ↓</a></p><h3>7. Worked calculation for one observation</h3><div class="report-equation">{E(worked(c,rows[0]))}</div><h3>8. Graph, gradient and final calculation</h3><div class="chart-card">{graph(c,rows,f)}</div><p>Circular markers represent empirical benchmark observations. The solid line represents the ordinary least-squares asymptotic linear fit.</p><div class="report-equation">x̄ = {fmt(f['mx'])}; ȳ = {fmt(f['my'])}<br>Σ(x − x̄)² = {fmt(f['sxx'])}<br>Σ(x − x̄)(y − ȳ) = {fmt(f['sxy'])}<br>m = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)² = {fmt(f['m'],8)}<br>b = ȳ − mx̄ = {fmt(f['b'],8)}<br>{E(formula(c,f))}</div><h3>9. Uncertainty and comparison</h3><p>Percentage difference = |estimate − theoretical value| / |theoretical value| × 100 = <strong>{percent:.4f}%</strong>.</p><p>For n = 7 benchmark observations, Σresidual² = {fmt(f['sse'])}; s² = Σresidual²/(n − 2). Gradient standard error = √[s²/Σ(x − x̄)²] = {fmt(f['slopeSE'])}. Intercept standard error = √[s²(1/n + x̄²/Σ(x − x̄)²)] = {fmt(f['interceptSE'])}.</p><p>Propagating the fit parameters yields a <strong>fit standard error of {fmt(se*c['resultScale'])} {E(c['resultUnit'])}</strong>, with an ideal coefficient of determination R² = {f['r2']:.6f}.</p><p>{E(uncertainty)}</p><h3>10. Result and discussion</h3><div class="report-equation">{E(c['target'])} = {fmt(value*c['resultScale'],c['resultDecimals'])} {E(c['resultUnit'])}<br>Theoretical reference value: {fmt(reference*c['resultScale'],c['resultDecimals'])} {E(c['resultUnit'])}</div><p>{E(discussion)}</p><h3>11. Precautions and limitations</h3><ul>{''.join('<li>'+E(p)+'</li>' for p in c['precautions'])}</ul><p>{E(c['limitations'])} {E(c['modelExtra'])}</p><h3>12. Conclusion</h3><p>{E(conclusion)}</p></article>'''

def lesson_schema(c,part,path,title,desc,base):
 graph=[{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Open STEM Lab','item':base+'/'},{'@type':'ListItem','position':2,'name':'Computer Science Laboratory','item':base+'/subjects/computer-science/'},{'@type':'ListItem','position':3,'name':c['shortTitle'],'item':base+f'/computer-science/{c["slug"]}/'}]}]
 if part=='experiment':
  graph.append({'@type':['WebPage','LearningResource','TechArticle'],'name':title,'description':desc,'url':base+path,'learningResourceType':'Interactive computational simulation','educationalLevel':'Undergraduate','about':c['title'],'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'Open STEM Lab','url':base+'/'}})
  if c.get('quiz'):
   graph.append({'@type':'Quiz','name':c['shortTitle']+' Concept Understanding','hasPart':[{'@type':'Question','name':q['question'],'suggestedAnswer':[{'@type':'Answer','text':opt} for opt in q['options']],'acceptedAnswer':{'@type':'Answer','text':q['options'][q['correct']]}} for q in c['quiz']]})
 elif part=='theory':
  graph.append({'@type':['WebPage','TechArticle','FAQPage'],'name':title,'description':desc,'url':base+path,'about':c['title'],'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'Open STEM Lab','url':base+'/'},'mainEntity':[{'@type':'Question','name':t['question'],'acceptedAnswer':{'@type':'Answer','text':t['answer']}} for t in c['topics']]})
 else:
  graph.append({'@type':['WebPage','ScholarlyArticle','TechArticle'],'name':title,'description':desc,'url':base+path,'about':c['title'],'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'Open STEM Lab','url':base+'/'}})
 return json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)

def shell(c,part,body,base,production):
 from build_catalog import head
 path=f'/computer-science/{c["slug"]}/'+('' if part=='experiment' else part+'/')
 title=c['shortTitle']+(' Experiment & Simulation' if part=='experiment' else ' Theory & Analysis' if part=='theory' else ' Lab Report: Benchmarks & Calculations')+' | Open STEM Lab'
 desc={'experiment':c['aim']+' Explore interactive search algorithms, compare operation counts and analyse complexity scaling.','theory':'Understand '+c['shortTitle'].lower()+': recurrence relations, Big-O bounds, decision trees and hardware cache interactions.','report':'A worked '+c['shortTitle'].lower()+' lab report with benchmark data tables, asymptotic graphs, calculations, uncertainty and conclusions.'}[part]
 header=head(path,title,desc,base,production).replace('<link rel="stylesheet" href="/catalog.css">','<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/cs-lesson.css">')
 header=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda _:f'<script type="application/ld+json">{lesson_schema(c,part,path,title,desc,base)}</script>',header,flags=re.S)
 home=f'/computer-science/{c["slug"]}/'
 nav='<aside class="sidebar"><a class="brand" style="font-size:20px" href="/">◉ openstemlab.</a><a class="side-subject" href="/subjects/computer-science/">← Computer Science labs</a><div class="side-label">LABORATORY '+str(c['number']).zfill(2)+'</div><nav aria-label="Lesson navigation">'
 for href,label in [(home,'Explore the experiment'),(home+'theory/','Understand the theory'),(home+'#apparatus','Know your tools'),(home+'#method','Follow the method'),(home+'#results','Analyse your results'),(home+'#check','Check your understanding'),(home+'report/','Sample lab report')]:
  nav+=f'<a class="nav-item{" active" if path==href else ""}" href="{href}">{label}</a>'
 nav+='<a class="nav-item" href="/experiments/">Search all experiments</a></nav><div class="side-note"><span class="small-sun">✳</span><p>Learn by computing.<br>Understand by benchmarking.</p></div><a class="text-button" href="/">← All subjects</a></aside>'
 heading=c['title'] if part=='experiment' else c['shortTitle']+' theory' if part=='theory' else c['shortTitle']+' lab report'
 return header+'<body>'+nav+'<main><header class="topbar"><div><a href="/subjects/computer-science/">Computer Science</a> / '+E(c['shortTitle'])+'</div><span class="free-label">FREE TO EXPLORE</span></header><section class="page-heading"><div class="eyebrow">LABORATORY '+str(c['number']).zfill(2)+' · COMPUTER SCIENCE</div><h1>'+E(heading)+'</h1><p>'+E(desc)+'</p></section><nav class="lab-navigation" aria-label="Experiment pages"><a href="'+home+'">Workbench</a><a href="'+home+'theory/">Detailed theory</a><a href="'+home+'#method">Method</a><a href="'+home+'#results">My results</a><a href="'+home+'report/">Example report</a></nav>'+body+'<footer><span class="footer-brand">openstemlab.</span><a href="/subjects/computer-science/">All computer science labs</a><span>Deterministic algorithmic model</span></footer></main>'+ ('<script id="labConfig" type="application/json">'+json.dumps(c,ensure_ascii=False).replace('<',chr(92)+'u003c')+'</script><script src="/cs-models.js"></script><script src="/cs-engine.js"></script>' if part=='experiment' else '')+'</body></html>'

def build_cs(out,base,production):
 published=[c for c in specs() if c['published']]
 for name,dest in [('models.js','cs-models.js'),('engine.js','cs-engine.js'),('lesson.css','cs-lesson.css')]:
  (out/dest).write_text((ROOT/'content/cs'/name).read_text())
 db=sqlite3.connect(ROOT/'data/catalog.sqlite3')
 sid=db.execute("SELECT id FROM subjects WHERE slug='computer-science'").fetchone()[0]
 db.execute("UPDATE subjects SET content_status='live' WHERE slug='computer-science'")
 paths=[]
 for c in published:
  slug=c['slug']
  home=f'/computer-science/{slug}/'
  (out/home.lstrip('/')).mkdir(parents=True,exist_ok=True)
  rows=[observation(c,v) for v in c['samples']]
  f=fit(rows)
  for part,body in [
   ('experiment',workbench(c)),
   ('theory','<section>'+theory(c)+f'<div class="insight"><span>↳</span><div><strong>Connect the theory to benchmark observations.</strong><p>{E(c["modelExtra"])}</p></div></div></section>'),
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
 paths=build_cs(out,base,args.production)
 print(f"Built {len(paths)} CS pages for {base}: {paths}")
