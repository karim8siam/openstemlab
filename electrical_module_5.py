# -*- coding: utf-8 -*-
"""Electrical & Electronics Engineering Module 5: Labs 37–43."""
from builder_helpers import (
    make_apparatus, make_procedure, make_topics,
    make_precautions, make_quiz, make_theory, make_report
)

def get_module_5():
    labs_data = [{'num': 37, 'slug': 'transmission-line-abcd-parameters-ferranti-effect', 'title': 'Transmission Line ABCD Two-Port Parameters, Voltage Regulation & Ferranti Effect', 'shortTitle': 'Transmission Line Parameters', 'aim': 'Determine ABCD transmission parameters of an artificial medium-length transmission line (Pi-model), evaluating voltage regulation and observing the Ferranti voltage rise under no-load conditions.', 'inputLabel': 'Receiving End Load Current I_R', 'shortInput': 'Load Current I_R', 'inputUnit': 'A', 'min': 2.0, 'max': 16.0, 'step': 2.0, 'initial': 8.0, 'inputDecimals': 2, 'rawLabel': 'Receiving End Voltage V_R', 'rawUnit': 'V', 'rawDecimals': 2, 'xAxis': 'Receiving end current I_R (A)', 'yAxis': 'Receiving end voltage V_R (V)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 18.0, 'emptyY': 250.0, 'targetName': 'Series Line Impedance Magnitude (|Z_line|)', 'target': '2.8500', 'refValue': 2.85, 'resultUnit': 'Ω', 'resultDecimals': 4, 'resultScale': 1.0, 'fitEquation': 'V_R = -2.8500 · I_R + 230.0000', 'samples': [2.0, 4.5, 7.0, 9.5, 12.0, 14.5], 'subsystem': 'Lumped-Parameter Transmission Line Simulator', 'focus': 'Surge Impedance Loading (SIL), Charging Current & Voltage Regulation'}, {'num': 38, 'slug': 'earth-fault-and-overcurrent-relay-idmt-characteristics', 'title': 'Inverse Definite Minimum Time (IDMT) Overcurrent and Earth-Fault Relay Characteristics', 'shortTitle': 'IDMT Protective Relays', 'aim': 'Calibrate and verify operating time-current characteristics of an induction disc / numerical IDMT overcurrent relay against standard IEC 60255 curves across variable plug settings.', 'inputLabel': 'IDMT Characteristic Factor 1/(PSM⁰˙⁰² - 1)', 'shortInput': 'IDMT Factor', 'inputUnit': 'factor', 'min': 5.0, 'max': 35.0, 'step': 5.0, 'initial': 15.0, 'inputDecimals': 2, 'rawLabel': 'Relay Operating Tripping Time t_trip', 'rawUnit': 's', 'rawDecimals': 3, 'xAxis': 'IDMT factor 1/(PSM⁰˙⁰² - 1)', 'yAxis': 'Relay operating time t_trip (s)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 40.0, 'emptyY': 6.0, 'targetName': 'Standard Inverse Time Multiplier Constant (TMS·0.14)', 'target': '0.1400', 'refValue': 0.14, 'resultUnit': 's', 'resultDecimals': 4, 'resultScale': 1.0, 'fitEquation': 't_trip = 0.1400 · [1/(PSM⁰˙⁰² - 1)]', 'samples': [6.0, 10.0, 15.0, 20.0, 26.0, 32.0], 'subsystem': 'Secondary Current Injection Test Set & Digital Relay Workstation', 'focus': 'Disc Driving Torque, Shading Ring Flux, Time Multiplier Setting (TMS) & Discrimination'}, {'num': 39, 'slug': 'dielectric-breakdown-strength-transformer-insulating-oil', 'title': 'Dielectric Breakdown Voltage Strength of Transformer Mineral Insulating Oil', 'shortTitle': 'Insulating Oil Breakdown', 'aim': 'Determine dielectric breakdown strength of high-voltage transformer mineral insulating oil using standard mushroom/spherical electrodes according to IEC 60156 / ASTM D877.', 'inputLabel': 'Standard Electrode Test Gap d', 'shortInput': 'Electrode Gap d', 'inputUnit': 'mm', 'min': 1.0, 'max': 4.0, 'step': 0.5, 'initial': 2.5, 'inputDecimals': 2, 'rawLabel': 'Dielectric Breakdown Voltage V_bd', 'rawUnit': 'kV', 'rawDecimals': 2, 'xAxis': 'Electrode test gap d (mm)', 'yAxis': 'Dielectric breakdown voltage V_bd (kV)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 4.5, 'emptyY': 100.0, 'targetName': 'Dielectric Withstand Field Strength (E_crit)', 'target': '22.5000', 'refValue': 22.5, 'resultUnit': 'kV/mm', 'resultDecimals': 4, 'resultScale': 1.0, 'fitEquation': 'V_bd = 22.5000 · d', 'samples': [1.0, 1.5, 2.0, 2.5, 3.0, 3.5], 'subsystem': 'Automated 100-kV Oil Breakdown Test Vessel', 'focus': 'Townsend Avalanche, Moisture Contamination, Bubble Cavitation & IEC 60156 Ramping'}, {'num': 40, 'slug': 'photovoltaic-pv-cell-iv-and-pv-characteristics', 'title': 'Solar Photovoltaic (PV) Module IV/PV Characteristics & Maximum Power Point Tracking (MPPT)', 'shortTitle': 'Solar PV Cell Characteristics', 'aim': 'Measure current-voltage (IV) and power-voltage (PV) curves of a silicon solar photovoltaic panel under variable solar irradiance, determining short-circuit current (I_sc), open-circuit voltage (V_oc), fill factor (FF), and maximum power point (P_mpp).', 'inputLabel': 'Incident Solar Irradiance G', 'shortInput': 'Solar Irradiance G', 'inputUnit': 'W/m²', 'min': 200.0, 'max': 1000.0, 'step': 100.0, 'initial': 600.0, 'inputDecimals': 1, 'rawLabel': 'Short-Circuit Photocurrent I_sc', 'rawUnit': 'A', 'rawDecimals': 3, 'xAxis': 'Incident solar irradiance G (W/m²)', 'yAxis': 'Short-circuit photocurrent I_sc (A)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 1100.0, 'emptyY': 6.0, 'targetName': 'Photovoltaic Current Responsivity (I_sc/G)', 'target': '0.00485', 'refValue': 0.00485, 'resultUnit': 'A/(W/m²)', 'resultDecimals': 5, 'resultScale': 1.0, 'fitEquation': 'I_sc = 0.00485 · G', 'samples': [200.0, 350.0, 500.0, 650.0, 800.0, 950.0], 'subsystem': 'Solar Simulator & Electronic Load MPPT Controller', 'focus': 'Photon Absorption, Carrier Recombination, Single-Diode Model & Temperature De-rating'}, {'num': 41, 'slug': 'wind-turbine-generator-power-coefficient-betz-limit', 'title': 'Wind Turbine Generator Aerodynamic Power Curve, Tip-Speed Ratio & Betz Limit', 'shortTitle': 'Wind Turbine Power Curve', 'aim': 'Evaluate aerodynamic power coefficient (C_p), tip-speed ratio (lambda), and electrical output power in a wind turbine generator under controlled wind tunnel velocities, verifying theoretical Betz limit constraints.', 'inputLabel': 'Cubed Wind Velocity v³', 'shortInput': 'Velocity Cubed v³', 'inputUnit': '(m/s)³', 'min': 100.0, 'max': 1100.0, 'step': 100.0, 'initial': 512.0, 'inputDecimals': 1, 'rawLabel': 'Generator Output Power P_e', 'rawUnit': 'W', 'rawDecimals': 2, 'xAxis': 'Cubed wind velocity v³ ((m/s)³)', 'yAxis': 'Generator electrical power P_e (W)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 1200.0, 'emptyY': 500.0, 'targetName': 'Aerodynamic Power Scaling Constant (0.5·ρ·A·C_p·η)', 'target': '0.4200', 'refValue': 0.42, 'resultUnit': 'W/(m/s)³', 'resultDecimals': 4, 'resultScale': 1.0, 'fitEquation': 'P_e = 0.4200 · v³', 'samples': [125.0, 216.0, 343.0, 512.0, 729.0, 1000.0], 'subsystem': 'Subsonic Wind Tunnel & Variable-Pitch Turbine Generator', 'focus': 'Betz Limit (59.3%), Blade Pitch Control, Aerodynamic Lift & Maximum Power Curve'}, {'num': 42, 'slug': 'high-voltage-impulse-generator-marx-circuit', 'title': 'Multi-Stage High-Voltage Lightning and Switching Impulse Generator (Marx Circuit)', 'shortTitle': 'Marx Impulse Generator', 'aim': 'Investigate the generation of standard 1.2/50 μs lightning impulse voltage waveforms using a multi-stage capacitive Marx circuit with calibrated sphere-gap triggers.', 'inputLabel': 'Charged Marx Stages N', 'shortInput': 'Stages N', 'inputUnit': 'stages', 'min': 1, 'max': 7, 'step': 1, 'initial': 3, 'inputDecimals': 0, 'rawLabel': 'Peak Output Impulse Voltage V_peak', 'rawUnit': 'kV', 'rawDecimals': 1, 'xAxis': 'Charged Marx stages N (stages)', 'yAxis': 'Peak output impulse voltage V_peak (kV)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 8.0, 'emptyY': 300.0, 'targetName': 'Per-Stage Impulse Voltage Multiplication (η·V_dc)', 'target': '45.0000', 'refValue': 45.0, 'resultUnit': 'kV/stage', 'resultDecimals': 4, 'resultScale': 1.0, 'fitEquation': 'V_peak = 45.0000 · N', 'samples': [1, 2, 3, 4, 5, 6], 'subsystem': 'High-Voltage Laboratory Impulse Column & Capacitive Divider', 'focus': 'Parallel Charging / Series Discharging, Wavefront Resistance & Standard 1.2/50 μs Waveform'}, {'num': 43, 'slug': 'harmonic-distortion-measurement-fft-spectrum', 'title': 'Power Quality Analysis: Total Harmonic Distortion (THD) and FFT Spectral Harmonics', 'shortTitle': 'Power Quality & THD', 'aim': 'Measure Total Harmonic Distortion (THD_V and THD_I), individual harmonic amplitudes, and distortion power factor generated by non-linear phase-controlled rectifier loads.', 'inputLabel': 'Thyristor Firing Angle Delay α', 'shortInput': 'Firing Angle α', 'inputUnit': 'deg', 'min': 15.0, 'max': 75.0, 'step': 10.0, 'initial': 45.0, 'inputDecimals': 1, 'rawLabel': 'Current Total Harmonic Distortion THD_I', 'rawUnit': '%', 'rawDecimals': 2, 'xAxis': 'Firing angle delay α (deg)', 'yAxis': 'Current total harmonic distortion THD_I (%)', 'xScale': 1.0, 'yScale': 1.0, 'emptyX': 80.0, 'emptyY': 60.0, 'targetName': 'Harmonic Distortion Angular Sensitivity Slope', 'target': '0.5500', 'refValue': 0.55, 'resultUnit': '%/deg', 'resultDecimals': 4, 'resultScale': 1.0, 'fitEquation': 'THD_I = 0.5500 · α + 12.0000', 'samples': [15.0, 25.0, 35.0, 45.0, 55.0, 65.0], 'subsystem': 'Power Quality Analyzer & Controllable Thyristor Bridge', 'focus': 'Fourier Decomposition, Non-Linear Load Harmonics, IEEE 519 Compliance & Active Filtering'}]
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
