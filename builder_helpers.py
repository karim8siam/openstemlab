# -*- coding: utf-8 -*-
"""Master builder script to construct electrical_module_1.py to electrical_module_6.py."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def make_apparatus(lab):
    return [
        {"name": f"{lab['shortTitle']} Precision Workstation", "purpose": f"Provides regulated excitation, calibrated terminal access, and low-parasitic interconnects for {lab['focus'].lower()}."},
        {"name": "True-RMS Digital Multimeter (6.5-digit Keysight / Fluke)", "purpose": f"Measures terminal voltages, branch currents, and precision DC/AC parameters with ±0.0035% baseline accuracy."},
        {"name": "Dual-Channel Digital Storage Oscilloscope (100 MHz, 1 GSa/s)", "purpose": f"Captures time-domain waveforms, phase shifts, transient dynamics, and harmonic spectra for {lab['shortTitle'].lower()}."},
        {"name": "Regulated Linear DC / AC Variable Power Source", "purpose": "Supplies low-noise, ripple-free voltage and current excitation with adjustable current limiting."},
        {"name": "Calibrated Decade Resistance & Component Substitution Box", "purpose": f"Provides precision 0.1% tolerance standard passive values to establish calibrated {lab['shortInput'].lower()} conditions."},
        {"name": "Four-Terminal Kelvin Lead Wire & BNC Coaxial Cable Set", "purpose": "Minimizes lead resistance, inductive pickup, and ambient EMI interference across all test ports."}
    ]

def make_procedure(lab):
    return [
        {"title": "Visual Inspection & Pre-Flight Zero Tare", "text": f"Inspect all circuit connections, breadboard jumpers, and terminal blocks. Verify that instrument ground planes are tied to earth and execute zero tare on all digital meters."},
        {"title": "Excitation Source & Baseline Calibration", "text": f"Energize the regulated supply, set baseline operating thresholds, and calibrate the {lab['shortInput'].lower()} using the precision standard reference meter."},
        {"title": "Systematic Parameter Variation & Settling", "text": f"Increment the {lab['shortInput'].lower()} systematically across the designated experimental range ({lab['samples'][0]} to {lab['samples'][-1]} {lab['inputUnit']}), permitting thermal settling at each setpoint."},
        {"title": "Multi-Meter & Oscilloscope Waveform Acquisition", "text": f"Record the primary output metric ({lab['rawLabel']}) alongside auxiliary telemetry. Verify waveform symmetry, DC offset, and harmonic integrity on the oscilloscope."},
        {"title": "Cross-Validation & Redundant Trial Verification", "text": f"Execute repeated forward and reverse sweeps to detect hysteresis, thermal drift, or non-linear saturation effects across the device under test (DUT)."},
        {"title": "Shutdown, De-energization & Data Archival", "text": f"Reduce source excitation smoothly to zero, de-energize all primary supplies, discharge residual capacitive elements, and export raw telemetry to the data buffer."}
    ]

def make_topics(lab):
    return [
        {"question": f"What is the foundational physical principle underlying {lab['shortTitle']}?", "answer": f"It relies on Maxwell's electromagnetic equations, Kirchhoff's laws, and linear network theory, governing how electrical energy is distributed, converted, or controlled within the {lab['subsystem'].lower()}."},
        {"question": f"How does varying {lab['shortInput']} affect the circuit response?", "answer": f"Changing {lab['shortInput']} shifts the operating point along the characteristic transfer function, modulating internal voltage drops and current distributions as governed by {lab['fitEquation']}."},
        {"question": "Why is impedance matching essential in high-frequency and power systems?", "answer": "Impedance matching eliminates reflected wave power in transmission networks and maximizes energy transfer efficiency from source to load according to the Maximum Power Transfer Theorem."},
        {"question": "How do non-linear parasitic components introduce measurement error in this lab?", "answer": "Parasitic lead inductances, stray capacitances, and temperature-dependent resistance shifts introduce high-frequency distortion and baseline drift if not compensated by Kelvin four-wire sensing."},
        {"question": f"What distinguishes the analytical model from experimental observations in {lab['shortTitle']}?", "answer": f"Ideal analytical formulas assume zero internal dissipation and infinite bandwidth, whereas real physical components exhibit finite dielectric losses, saturation limits, and ambient thermal sensitivity."},
        {"question": "How are these electrical principles applied in modern microelectronics and grid infrastructure?", "answer": "The concepts form the backbone of power electronics converters, integrated circuit biasing, smart grid protection relays, renewable energy inverters, and high-speed communication transceivers."}
    ]

def make_precautions(lab):
    return [
        "Verify all terminal polarities and ensure supply voltage does not exceed component maximum breakdown ratings prior to power-up.",
        "Maintain current limits on regulated DC bench supplies to protect semiconductor junctions and precision resistors from thermal burnout.",
        "Ensure oscilloscope probes are grounded to the true circuit ground reference to avoid creating destructive ground loop short circuits.",
        "Allow circuit components to reach steady-state thermal equilibrium for at least 30 seconds before recording final analog telemetry."
    ]

def make_quiz(lab):
    return [
        {
            "question": f"In the study of {lab['shortTitle']}, the primary dependent variable measured is:",
            "options": [lab['rawLabel'], "Ambient atmospheric temperature", "Rotational shaft eccentricity", "Gravitational acceleration constant"],
            "correct": 0,
            "explanation": f"The experimental protocol directly measures {lab['rawLabel']} as a function of the manipulated {lab['shortInput']}."
        },
        {
            "question": f"The mathematical relationship governing {lab['shortTitle']} is modeled as:",
            "options": [lab['fitEquation'], "E = mc²", "F = ma", "PV = nRT"],
            "correct": 0,
            "explanation": f"Linear regression across calibrated observations confirms the governing equation {lab['fitEquation']} with R² > 0.999."
        },
        {
            "question": f"The target benchmark parameter derived from regression analysis is:",
            "options": [f"{lab['targetName']} ({lab['refValue']} {lab['resultUnit']})", "Speed of light in vacuum", "Planck's quantum constant", "Avogadro's number"],
            "correct": 0,
            "explanation": f"The experimental slope and intercept directly yield {lab['targetName']} with a theoretical reference value of {lab['refValue']} {lab['resultUnit']}."
        },
        {
            "question": "Which instrumentation technique effectively eliminates lead wire resistance error?",
            "options": ["Four-terminal Kelvin connection sensing", "Increasing supply voltage to maximum", "Using unshielded twisted pair wiring", "Disconnecting the circuit ground reference"],
            "correct": 0,
            "explanation": "Four-terminal Kelvin sensing uses separate pairs of current-carrying and voltage-sensing electrodes, eliminating voltage drops along current-carrying leads."
        }
    ]

def make_theory(lab):
    return f"""<h3>1. Theoretical Principles of {lab['title']}</h3>
<p>Electrical and Electronics Engineering rests upon Maxwell's field equations, Ohm's empirical law of conduction, and Kirchhoff's conservation laws for current (KCL) and voltage (KVL). In this laboratory investigation of <strong>{lab['title']}</strong>, we examine the fundamental electrotechnical relationships within the {lab['subsystem'].lower()}. The core focus of this module addresses {lab['focus'].lower()}.</p>
<p>Under steady-state excitation, the physical system conforms to the governing linear transfer characteristic:</p>
\\[ y = m \\cdot x + b \\]
<p>where $x$ represents the normalized independent input variable ({lab['inputLabel']}, in units of ${lab['inputUnit']}$), $y$ denotes the measured response variable ({lab['rawLabel']}, in units of ${lab['rawUnit']}$), $m$ represents the characteristic transfer gradient (${lab['target']}$), and $b$ accounts for the intrinsic offset or baseline bias.</p>

<h3>2. Mathematical Derivations & Network Formulations</h3>
<p>Consider the canonical lumped-parameter circuit model representing the device under test. Applying Kirchhoff's voltage law around the primary loop yields:</p>
\\[ \\sum_{{k=1}}^{{N}} V_k = 0 \\implies V_{{source}} - I \\cdot R_{{int}} - V_{{term}} = 0 \\]
<p>Rearranging in terms of measurable terminal telemetry provides the explicit affine calibration equation:</p>
\\[ {lab['fitEquation']} \\]
<p>The derivative $\\frac{{dy}}{{dx}} = m = {lab['target']}$ represents the fundamental sensitivity coefficient ({lab['targetName']}). For active linear networks, this slope characterizes internal Thévenin/Norton source impedances, transconductance gains, resonance quality factors, or machine electromechanical couplings depending on the specific circuit topology.</p>

<h3>3. Dynamic Behavior, Energy Storage & Frequency Dependencies</h3>
<p>In circuits containing reactive elements (inductors $L$ and capacitors $C$), the instantaneous terminal dynamics obey differential operator equations:</p>
\\[ v_L(t) = L \\frac{{di(t)}}{{dt}}, \\quad i_C(t) = C \\frac{{dv_C(t)}}{{dt}} \\]
<p>Under sinusoidal steady-state AC conditions, time-domain derivatives map directly to the complex frequency domain via the Laplace transform $s = j\\omega = j 2\\pi f$. The total complex impedance $\\mathbf{{Z}}(j\\omega)$ combines real resistive dissipation $R$ with quadrature reactive energy storage $X(\\omega) = \\omega L - \\frac{{1}}{{\\omega C}}$:</p>
\\[ \\mathbf{{Z}}(j\\omega) = R + j \\left( \\omega L - \\frac{{1}}{{\\omega C}} \\right) = |Z| e^{{j\\phi}} \\]
<p>Phase angle $\\phi = \\arctan\\left(\\frac{{X}}{{R}}\\right)$ dictates power factor ($\cos\\phi$), defining the balance between real work-producing power $P = V I \\cos\\phi$ and circulating reactive power $Q = V I \\sin\\phi$.</p>

<h3>4. Semiconductor Physics & Operational Boundary Limits</h3>
<p>When active solid-state semiconductors or magnetic cores are present in the subsystem, small-signal linearity holds strictly within small-signal perturbation bounds. For semiconductor junctions, minority carrier diffusion and space-charge recombination follow Shockley's exponential law $I = I_s (e^{{V / \\eta V_T}} - 1)$. For ferromagnetic inductors and transformer cores, magnetic flux density $B$ relates to magnetic field intensity $H$ through the non-linear hysteresis loop $B = \\mu(H) H$, reaching magnetic saturation at high flux densities. Standard laboratory operating points are deliberately biased within the linear, unsaturated small-signal domain to guarantee high parameter reproducibility and minimal harmonic distortion.</p>

<h3>5. Instrumentation Architecture & Error Minimization</h3>
<p>To eliminate systematic measurement offsets, modern electrical metrology incorporates digital signal processing (DSP) filters, high-input-impedance JFET-input instrumentation amplifiers ($Z_{{in}} > 10^{{12}}\\,\\Omega$), and true-RMS AC conversion algorithms. The calibrated measurement protocol utilizes four-terminal Kelvin connections to isolate lead resistance drops, while high-frequency coaxial lines are terminated in their characteristic impedance ($50\\,\\Omega$) to suppress transmission line standing wave reflections.</p>"""

def make_report(lab):
    return f"""<h3>1. Title and Objective</h3>
<p><strong>{lab['title']}.</strong> {lab['aim']} This formal laboratory report documents experimental data acquisition, mathematical model calibration, regression analysis, and error propagation for {lab['shortTitle'].lower()}.</p>

<h3>2. Abstract</h3>
<p>An experimental investigation of {lab['shortTitle'].lower()} was conducted using precision laboratory instrumentation across six systematic setpoints of {lab['shortInput'].lower()} ranging from {lab['samples'][0]} to {lab['samples'][-1]} {lab['inputUnit']}. Measured {lab['rawLabel'].lower()} data were logged using 6.5-digit digital multimeters and digital storage oscilloscopes. Ordinary least-squares regression yielded an empirical calibration line of {lab['fitEquation']} with a coefficient of determination R² = 1.000000. The derived experimental parameter {lab['targetName']} was evaluated as {lab['refValue']} {lab['resultUnit']}, demonstrating complete agreement with theoretical benchmark expectations within 0.02% experimental error.</p>

<h3>3. Experimental Apparatus & Standard Settings</h3>
<ul>
{''.join(f"<li><strong>{a['name']}</strong>: {a['purpose']}</li>" for a in make_apparatus(lab))}
<li><strong>Environmental Ambient Conditions</strong>: Ambient laboratory temperature 23.5 ± 0.5 °C; relative humidity 45 ± 5%; atmospheric pressure 101.3 kPa.</li>
<li><strong>Excitation Calibration Settings</strong>: Primary source stabilized within ±0.01% using closed-loop linear voltage regulation.</li>
</ul>

<h3>4. Theory & Graphical Coordinate Selection</h3>
<p>According to the principles of {lab['shortTitle'].lower()}, the circuit response follows the linear transformation:</p>
<div class="report-equation">{lab['fitEquation']}</div>
<p>To evaluate the intrinsic physical parameter ({lab['targetName']}), the experimental data are plotted with {lab['xAxis']} on the horizontal abscissa and {lab['yAxis']} on the vertical ordinate. The gradient of the resulting least-squares linear line directly yields the parameter magnitude.</p>

<h3>5. Step-by-Step Experimental Method</h3>
<ol>
{''.join(f"<li><strong>{s['title']}</strong>: {s['text']}</li>" for s in make_procedure(lab))}
</ol>

<h3>6. Raw Experimental Observations & Data Tabulation</h3>
<p>All experimental observations were recorded under steady-state thermal and electrical equilibrium. The table below summarizes the recorded telemetry across the experimental domain.</p>
<div class="table-card">
<table>
<caption>Table 1. Experimental observation telemetry for {lab['shortTitle']}.</caption>
<thead>
<tr>
<th>Trial #</th>
<th>{lab['inputLabel']} ({lab['inputUnit']})</th>
<th>{lab['rawLabel']} ({lab['rawUnit']})</th>
<th>Transformed x</th>
<th>Transformed y</th>
<th>Residual</th>
</tr>
</thead>
<tbody>
{''.join(f"<tr><td>{i+1}</td><td>{v}</td><td>{round(float(lab['target']) * v if '-' not in lab['fitEquation'] else 12.0 - 50.0 * v, 3)}</td><td>{v:.3f}</td><td>{round(float(lab['target']) * v if '-' not in lab['fitEquation'] else 12.0 - 50.0 * v, 3):.3f}</td><td>0.000</td></tr>" for i, v in enumerate(lab['samples']))}
</tbody>
</table>
</div>

<h3>7. Worked Calculation for Representative Observation</h3>
<p>For Trial 3 ({lab['shortInput']} = {lab['samples'][2]} {lab['inputUnit']}):</p>
<div class="report-equation">
x_3 = {lab['samples'][2]} {lab['inputUnit']}<br>
y_3 = m \\cdot x_3 + b = {lab['fitEquation'].replace('I_L', str(lab['samples'][2])).replace('V_1', str(lab['samples'][2])).replace('t', str(lab['samples'][2])).replace('f', str(lab['samples'][2])).replace('I_s', str(lab['samples'][2])).replace('I_1', str(lab['samples'][2])).replace('C', str(lab['samples'][2])).replace('(100/R)', str(lab['samples'][2]))}<br>
Derived Parameter Value = {lab['refValue']} {lab['resultUnit']}
</div>

<h3>8. Regression Analysis, Gradient & Parameter Extraction</h3>
<p>Ordinary least-squares (OLS) linear regression was performed across the six observation pairs. The regression statistics are summarized below:</p>
<div class="report-equation">
Slope m = {lab['target']} {lab['resultUnit']}<br>
Intercept b = Calculated baseline offset<br>
Correlation Coefficient R² = 1.000000<br>
Standard Error of Slope SE_m = ±0.00008 {lab['resultUnit']}
</div>

<h3>9. Uncertainty Propagation & Comparison with Reference</h3>
<p>Measurement uncertainty was calculated following the ISO Guide to the Expression of Uncertainty in Measurement (GUM). Type A uncertainty evaluated from observation residuals yielded u_A = 0.0002. Type B instrumental calibration uncertainty from the 6.5-digit multimeter was u_B = 0.0005. The combined expanded uncertainty at a 95% confidence interval (coverage factor k = 2) is:</p>
\\[ U = k \\cdot \\sqrt{{u_A^2 + u_B^2}} = 2 \\cdot \\sqrt{{(0.0002)^2 + (0.0005)^2}} = \\pm 0.0011\\text{{ {lab['resultUnit']}}} \\]
<p>The experimental estimate of {lab['refValue']} {lab['resultUnit']} agrees with the theoretical reference value ({lab['refValue']} {lab['resultUnit']}) within an absolute deviation of 0.015%, well within the expanded uncertainty band.</p>

<h3>10. Engineering Discussion & Phenomenological Interpretations</h3>
<p>The experimental results confirm the theoretical behavior of {lab['shortTitle'].lower()}. The linearity observed across all six test points validates the assumption of linear, bilateral network characteristics. Thermal drift was effectively suppressed by maintaining low duty cycles and utilizing precision metal-film components. The minor residual fluctuations observed are attributable to quantization resolution and Johnson–Nyquist thermal noise in the passive bridge elements.</p>

<h3>11. Industrial Applications & Construction Practice</h3>
<p>The electrotechnical principles demonstrated in this laboratory form the core foundation of numerous modern engineering systems, including:</p>
<ul>
<li><strong>Power Grid & Transmission Engineering</strong>: Network equivalent modeling, short-circuit current calculations, power factor correction capacitor banks, and substation protective relay coordination.</li>
<li><strong>Consumer Electronics & Integrated Circuits</strong>: Analog front-end amplification, active Butterworth filtering, switching power supply voltage regulation, and precision ADC/DAC mixed-signal conversion.</li>
<li><strong>Industrial Automation & Drives</strong>: Variable frequency motor speed control, servomechanism closed-loop feedback, electromechanical energy conversion, and industrial PLC signal conditioning.</li>
</ul>

<h3>12. Conclusion & Recommendations</h3>
<p>The experimental investigation of {lab['title']} was completed with complete success. The linear regression model verified the governing transfer equation with R² = 1.000000. All experimental safety protocols and precision measurement guidelines were strictly observed. For future investigations, automated GPIB/USB telemetry acquisition and environmental temperature chamber testing are recommended to characterize high-temperature coefficients.</p>

<div class="report-notice">
<strong>Simulated demonstration data.</strong>
<p>This report presents simulated benchmark observations generated for demonstration and academic instruction purposes. When submitting coursework, replace all numerical values with your actual laboratory workbench observations.</p>
</div>"""
