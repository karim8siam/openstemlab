# -*- coding: utf-8 -*-
"""Electrical & Electronics Engineering Module 6: Labs 44–50."""
from builder_helpers import (
    make_apparatus, make_procedure, make_topics,
    make_precautions, make_quiz, make_theory, make_report
)

def get_module_6():
    labs_data = [{'num': 44, 'slug': 'scr-triac-phase-angle-firing-control-r-rl-loads', 'title': 'Silicon Controlled Rectifier (SCR) and TRIAC Phase-Angle Firing Control with R and RL Loads', 'shortTitle': 'SCR & TRIAC Firing Control', 'aim': 'Investigate phase-angle triggering of SCRs and TRIACs with resistive and inductive loads, measuring gate trigger current, latching/holding currents, and average DC output voltage as a function of firing angle (alpha).', 'inputLabel': 'Firing Factor (1 + cos α)', 'shortInput': 'Firing Factor', 'inputUnit': 'factor', 'min': 0.2, 'max': 2.0, 'step': 0.2, 'initial': 1.0, 'inputDecimals': 2, 'rawLabel': 'Average DC Output Voltage V_dc', 'rawUnit': 'V', 'rawDecimals': 2, 'xAxis': 'Firing factor (1 + cos α) (factor)', 'yAxis': 'Average DC output voltage V_dc (V)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 2.2, 'emptyY': 100.0, 'targetName': 'Controlled Rectification Peak Scaling (V_m/π)', 'target': '48.0000', 'refValue': 48.0, 'resultUnit': 'V', 'resultDecimals': 4, 'resultScale': 1.0, 'fitEquation': 'V_dc = 48.0000 · (1 + cos α)', 'samples': [0.3, 0.6, 0.9, 1.2, 1.5, 1.8], 'subsystem': 'Phase-Controlled Rectifier Module & UJT Firing Trigger Circuit', 'focus': 'Four-Layer PNPN Shockley Dynamics, Free-Wheeling Diode Commutation & Gate Triggering'}, {'num': 45, 'slug': 'buck-boost-dc-dc-converter-duty-cycle-efficiency', 'title': 'High-Efficiency DC-DC Step-Down (Buck) and Step-Up (Boost) Switched-Mode Power Converters', 'shortTitle': 'Buck-Boost DC-DC Converters', 'aim': 'Design, assemble, and test a high-frequency MOSFET-switched buck converter, determining output voltage transfer ratio (V_out = D·V_in), inductor current ripple, and conversion efficiency.', 'inputLabel': 'Switched PWM Duty Ratio D', 'shortInput': 'Duty Ratio D', 'inputUnit': 'ratio', 'min': 0.1, 'max': 0.9, 'step': 0.1, 'initial': 0.5, 'inputDecimals': 2, 'rawLabel': 'Step-Down Output Voltage V_out', 'rawUnit': 'V', 'rawDecimals': 2, 'xAxis': 'PWM duty ratio D (ratio)', 'yAxis': 'Step-down output voltage V_out (V)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 1.0, 'emptyY': 25.0, 'targetName': 'Buck Converter Input Voltage Scaling (V_in)', 'target': '24.0000', 'refValue': 24.0, 'resultUnit': 'V', 'resultDecimals': 4, 'resultScale': 1.0, 'fitEquation': 'V_out = 24.0000 · D', 'samples': [0.15, 0.28, 0.42, 0.55, 0.68, 0.8], 'subsystem': '100-kHz Switched-Mode Power Supply (SMPS) Breadboard', 'focus': 'Continuous vs Discontinuous Conduction Modes (CCM/DCM), Inductor Volt-Second Balance'}, {'num': 46, 'slug': 'single-phase-spwm-inverter-total-harmonic-distortion', 'title': 'Single-Phase Full-Bridge Sinusoidal Pulse-Width Modulation (SPWM) DC-AC Inverter', 'shortTitle': 'Single-Phase SPWM Inverter', 'aim': 'Construct an H-bridge IGBT inverter using unipolar and bipolar sinusoidal PWM, evaluating fundamental RMS AC output voltage and harmonic spectrum as a function of modulation index (m_a).', 'inputLabel': 'Modulation Amplitude Index m_a', 'shortInput': 'Modulation Index m_a', 'inputUnit': 'ratio', 'min': 0.2, 'max': 1.1, 'step': 0.1, 'initial': 0.6, 'inputDecimals': 2, 'rawLabel': 'Fundamental RMS AC Voltage V_rms1', 'rawUnit': 'V', 'rawDecimals': 2, 'xAxis': 'Modulation amplitude index m_a (ratio)', 'yAxis': 'Fundamental RMS AC voltage V_rms1 (V)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 1.2, 'emptyY': 80.0, 'targetName': 'SPWM Inverter DC-to-RMS Scaling (V_dc/√2)', 'target': '70.7100', 'refValue': 70.71, 'resultUnit': 'V', 'resultDecimals': 4, 'resultScale': 1.0, 'fitEquation': 'V_rms1 = 70.7100 · m_a', 'samples': [0.2, 0.35, 0.5, 0.65, 0.8, 0.95], 'subsystem': 'H-Bridge IGBT Inverter & LC Low-Pass Filter Workbench', 'focus': 'Triangular Carrier Modulation, Dead-Time Insertion & Low-Order Harmonic Cancellation'}, {'num': 47, 'slug': 'closed-loop-pid-dc-motor-speed-servomechanism', 'title': 'Closed-Loop Proportional-Integral-Derivative (PID) DC Motor Speed Servomechanism', 'shortTitle': 'PID Speed Servomechanism', 'aim': 'Implement analog and digital PID feedback control on a DC servomotor, analyzing step response overshoot, steady-state error, settling time, and disturbance rejection under variable loop gains.', 'inputLabel': 'Controller Proportional Gain K_p', 'shortInput': 'Proportional Gain K_p', 'inputUnit': 'gain', 'min': 1.0, 'max': 7.0, 'step': 0.5, 'initial': 3.0, 'inputDecimals': 1, 'rawLabel': 'Closed-Loop Natural Angular Frequency ω_n', 'rawUnit': 'rad/s', 'rawDecimals': 2, 'xAxis': 'Controller proportional gain K_p (gain)', 'yAxis': 'Natural frequency ω_n (rad/s)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 8.0, 'emptyY': 45.0, 'targetName': 'Closed-Loop Bandwidth Scaling Gradient', 'target': '5.2000', 'refValue': 5.2, 'resultUnit': 'rad/s/gain', 'resultDecimals': 4, 'resultScale': 1.0, 'fitEquation': 'ω_n = 5.2000 · K_p + 10.0000', 'samples': [1.0, 1.8, 2.6, 3.4, 4.2, 5.0], 'subsystem': 'Analog PID Controller Board & Optical Quadrature Encoder Servomotor', 'focus': 'Root Locus Dynamics, Ziegler-Nichols Tuning, Integral Windup & Phase Margin'}, {'num': 48, 'slug': 'bode-plot-and-nyquist-stability-criterion', 'title': 'Frequency Response Analysis: Bode Magnitude/Phase Plots and Nyquist Stability Criterion', 'shortTitle': 'Bode & Nyquist Stability', 'aim': 'Measure open-loop frequency response of a linear dynamical control system, constructing experimental Bode plots, identifying gain margin (GM) and phase margin (PM), and evaluating stability via Nyquist encirclements.', 'inputLabel': 'Log Normalized Frequency log₁₀(ω/ω_c)', 'shortInput': 'Log Frequency', 'inputUnit': 'decade', 'min': 0.2, 'max': 2.0, 'step': 0.2, 'initial': 1.0, 'inputDecimals': 2, 'rawLabel': 'High-Frequency Asymptotic Magnitude', 'rawUnit': 'dB', 'rawDecimals': 2, 'xAxis': 'Log normalized frequency decade log₁₀(ω/ω_c)', 'yAxis': 'Asymptotic magnitude (dB)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 2.2, 'emptyY': -40.0, 'targetName': 'Single-Pole Asymptotic Roll-Off Slope', 'target': '20.0000', 'refValue': 20.0, 'resultUnit': 'dB/decade', 'resultDecimals': 4, 'resultScale': 1.0, 'fitEquation': 'Magnitude = -20.0000 · log₁₀(ω/ω_c)', 'samples': [0.2, 0.5, 0.8, 1.1, 1.4, 1.7], 'subsystem': 'Dynamic Signal Analyzer & Configurable Analog Plant', 'focus': 'Cauchy Argument Principle, Nyquist Critical Point (-1 + j0) & Closed-Loop Stability'}, {'num': 49, 'slug': 'linear-variable-differential-transformer-lvdt-transducer', 'title': 'Linear Variable Differential Transformer (LVDT) Displacement Transducer Calibration', 'shortTitle': 'LVDT Transducer Calibration', 'aim': 'Calibrate an AC-excited Linear Variable Differential Transformer (LVDT), measuring differential secondary voltage, phase reversal across the null point, linearity, and transducer sensitivity.', 'inputLabel': 'Core Axial Linear Displacement x', 'shortInput': 'Core Displacement x', 'inputUnit': 'mm', 'min': 0.5, 'max': 5.5, 'step': 0.5, 'initial': 2.5, 'inputDecimals': 2, 'rawLabel': 'Differential Secondary RMS Voltage V_sec', 'rawUnit': 'V', 'rawDecimals': 3, 'xAxis': 'Core axial displacement x (mm)', 'yAxis': 'Differential secondary voltage V_sec (V)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 6.0, 'emptyY': 5.0, 'targetName': 'LVDT Transducer Displacement Sensitivity (S)', 'target': '0.8500', 'refValue': 0.85, 'resultUnit': 'V/mm', 'resultDecimals': 4, 'resultScale': 1.0, 'fitEquation': 'V_sec = 0.8500 · x', 'samples': [0.5, 1.2, 2.0, 2.8, 3.6, 4.5], 'subsystem': 'Micrometer Calibration Rig & Carrier Demodulator Board', 'focus': 'Differential Transformer Mutual Inductance, Phase-Sensitive Demodulation & Null Voltage'}, {'num': 50, 'slug': 'strain-gauge-quarter-half-full-wheatstone-bridge', 'title': 'Piezoresistive Foil Strain Gauge and Temperature-Compensated Wheatstone Bridge Circuitry', 'shortTitle': 'Strain Gauge Wheatstone Bridge', 'aim': 'Measure mechanical microstrain on a cantilever beam using quarter-, half-, and full-bridge Wheatstone configurations, determining gauge factor (GF), circuit sensitivity, and thermal compensation.', 'inputLabel': 'Applied Mechanical Microstrain με', 'shortInput': 'Microstrain με', 'inputUnit': 'με', 'min': 100.0, 'max': 900.0, 'step': 100.0, 'initial': 400.0, 'inputDecimals': 1, 'rawLabel': 'Bridge Differential Output Voltage V_out', 'rawUnit': 'mV', 'rawDecimals': 3, 'xAxis': 'Applied mechanical microstrain με (με)', 'yAxis': 'Bridge differential output voltage V_out (mV)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 1000.0, 'emptyY': 12.0, 'targetName': 'Full-Bridge Strain Sensitivity Factor (GF·V_ex/4)', 'target': '0.0125', 'refValue': 0.0125, 'resultUnit': 'mV/με', 'resultDecimals': 5, 'resultScale': 1.0, 'fitEquation': 'V_out = 0.0125 · με', 'samples': [100.0, 220.0, 350.0, 480.0, 600.0, 750.0], 'subsystem': 'Precision Cantilever Bending Rig & Instrumentation Amplifier', 'focus': 'Piezoresistive Strain Effect, Dummy Gauge Thermal Compensation & Full-Bridge Gain'}]
    results = []
    for lab in labs_data:
        lab_dict = {
            "number": lab["num"],
            "slug": lab["slug"],
            "title": lab["title"],
            "shortTitle": lab["shortTitle"],
            "aim": lab["aim"],
            "inputLabel": lab["inputLabel"],
            "shortInput": lab["shortInput"],
            "inputUnit": lab["inputUnit"],
            "min": lab["min"],
            "max": lab["max"],
            "step": lab["step"],
            "initial": lab["initial"],
            "inputDecimals": lab["inputDecimals"],
            "rawLabel": lab["rawLabel"],
            "rawUnit": lab["rawUnit"],
            "rawDecimals": lab["rawDecimals"],
            "xAxis": lab["xAxis"],
            "yAxis": lab["yAxis"],
            "xScale": lab["xScale"],
            "yScale": lab["yScale"],
            "emptyX": lab["emptyX"],
            "emptyY": lab["emptyY"],
            "targetName": lab["targetName"],
            "target": lab["target"],
            "refValue": lab["refValue"],
            "resultUnit": lab["resultUnit"],
            "resultDecimals": lab["resultDecimals"],
            "resultScale": lab["resultScale"],
            "fitEquation": lab["fitEquation"],
            "intro": f"The experimental analysis of {lab['title'].lower()} investigates the electrotechnical behavior of {lab['subsystem'].lower()}. This university laboratory module focuses on {lab['focus'].lower()}, establishing accurate mathematical transfer characteristics across standard operational domains.",
            "modelExtra": f"Calibrated using the {lab['subsystem']} under controlled temperature and 64-bit IEEE 754 precision instrumentation buffers. Ordinary least-squares regression yields R² > 0.99999.",
            "settings": [
                f"Calibrated {lab['subsystem']} baseline operating point stabilized at 25.0 °C",
                f"Precision reference instrument accuracy verified within ±0.005% of full scale"
            ],
            "limitations": [
                "Assumes ideal linear operating conditions without thermal breakdown or non-linear core saturation",
                "Transient settling times allowed prior to analog-to-digital telemetry acquisition"
            ],
            "apparatus": make_apparatus(lab),
            "procedure": make_procedure(lab),
            "topics": make_topics(lab),
            "precautions": make_precautions(lab),
            "quiz": make_quiz(lab),
            "samples": lab["samples"],
            "measureLabel": f"Acquire {lab['shortTitle']} telemetry",
            "readings": ["independent_val", "raw_output", "transformed_x", "transformed_y"],
            "theory": make_theory(lab),
            "report": make_report(lab)
        }
        results.append(lab_dict)
    return results
