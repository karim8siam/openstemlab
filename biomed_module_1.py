# -*- coding: utf-8 -*-
"""Biomedical Engineering Module 1: Bioinstrumentation, Biopotential Electrodes & Medical Sensors (Labs 1–8)."""

def get_module_1():
    return [
        {
            "number": 1,
            "slug": "thermistor-wheatstone-bridge-clinical-thermometer",
            "title": "Thermistor Wheatstone-Bridge Clinical Thermometer Calibration",
            "shortTitle": "Thermistor Clinical Thermometer",
            "aim": "Calibrate a negative temperature coefficient (NTC) bead thermistor in an operational Wheatstone bridge circuit across clinical core body temperatures (35.0 °C to 41.0 °C) and determine bridge sensitivity.",
            "inputLabel": "Bath Temperature T",
            "shortInput": "Temp T",
            "inputUnit": "°C",
            "min": 35.0,
            "max": 41.0,
            "step": 1.2,
            "initial": 37.4,
            "inputDecimals": 1,
            "rawLabel": "Bridge Output Voltage V_br",
            "rawUnit": "mV",
            "rawDecimals": 3,
            "xAxis": "Temperature T (°C)",
            "yAxis": "Bridge output voltage V_br (mV)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 38.0,
            "emptyY": 55.0,
            "targetName": "Bridge Thermal Sensitivity S_T",
            "target": "18.5000",
            "refValue": 18.5000,
            "resultUnit": "mV/°C",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "V_br = S_T · T + V_0 = 18.5000 · T - 647.5000",
            "intro": "In medical instrumentation and physiological patient monitoring, accurate measurement of core body temperature is vital for detecting hypothermia, fever, systemic infection, and post-surgical metabolic decompensation. Because human physiological core temperature is confined to a narrow clinical range (typically 35.0 °C to 41.0 °C), clinical electronic thermometers require transducers with exceptional sensitivity, rapid thermal response, and minimal self-heating errors. Negative temperature coefficient (NTC) semiconductor bead thermistors are the dominant sensor technology in esophageal, tympanic, and catheter probes due to their large temperature coefficient of resistance (approximately -4% / °C at 37 °C), described by the Steinhart-Hart and exponential resistance-temperature relation: R(T) = R_0 · exp[β · (1/T - 1/T_0)]. However, this intrinsic exponential non-linearity must be conditioned for linear analog-to-digital conversion. By placing the thermistor in a Wheatstone bridge with matched fixed precision metal-film resistors, the bridge output voltage V_br exhibits high linearity across the narrow ±3.0 °C clinical window around the bridge null point (balanced at 35.0 °C). In this laboratory investigation, an instrumented clinical thermistor probe immersed in a precision circulating water calibration bath is evaluated to quantify bridge output voltage, verify linearization, and evaluate thermal sensitivity S_T.",
            "modelExtra": "Evaluated using a 10.0 kΩ nominal (at 25 °C) medical bead thermistor (β = 3950 K) configured in a four-arm equal-resistance bridge with V_in = 5.00 V excitation. Bridge balanced at T_0 = 35.0 °C (V_br = 0 mV). Linear sensitivity S_T is determined across the 35.0 °C to 41.0 °C clinical span.",
            "apparatus": [
                {"name": "NTC Medical Bead Thermistor Probe", "purpose": "Provides high-sensitivity thermal transduction with fast thermal time constant (< 0.5 s in liquid)."},
                {"name": "Precision Constant-Temperature Water Bath", "purpose": "Maintains calibration temperature stable to within ±0.01 °C with continuous magnetic stirring."},
                {"name": "NIST-Traceable Reference Standard Thermometer", "purpose": "Monitors calibration water bath temperature with 0.005 °C absolute metrological accuracy."},
                {"name": "Equal-Arm Wheatstone Bridge Conditioning Circuit", "purpose": "Converts thermistor resistance changes into a differential millivolt signal with low-noise instrumentation amp."},
                {"name": "Low-Noise Regulated DC Voltage Source", "purpose": "Supplies stable 5.000 V excitation while limiting thermistor self-heating current to < 100 μA."},
                {"name": "6.5-Digit Precision Digital Multimeter", "purpose": "Measures differential bridge output voltage V_br with microvolt resolution and 60 Hz line rejection."}
            ],
            "procedure": [
                {"title": "Bridge Null Balance Initialization", "text": "Set the precision water bath to exactly 35.00 °C and trim the Wheatstone bridge balancing potentiometer until differential output voltage reads exactly 0.000 mV."},
                {"title": "Self-Heating Dissipation Verification", "text": "Measure thermistor current under 5.00 V excitation; verify power dissipation is under 0.2 mW to ensure thermal self-heating elevation remains below 0.01 °C."},
                {"title": "Bath Thermal Stabilization", "text": "Adjust bath setpoint to 36.20 °C and allow 10 minutes for the circulating bath and immersed probe to achieve thermal equilibrium."},
                {"title": "Equilibrium Output Voltage Logging", "text": "Record 10 successive bridge voltage samples over 60 seconds using the 6.5-digit DMM and compute the mean differential voltage V_br in millivolts."},
                {"title": "Clinical Temperature Progression", "text": "Increment the calibration bath temperature through 37.4, 38.6, 39.8, and 41.0 °C, repeating steady-state voltage logging at each step."},
                {"title": "Sensitivity Regression and Linearity Analysis", "text": "Plot differential bridge output voltage V_br versus temperature T, computing the thermal sensitivity S_T and coefficient of determination R²."}
            ],
            "topics": [
                {"question": "How does an NTC thermistor differ from a Platinum RTD in clinical temperature measurement?", "answer": "An NTC thermistor has an exponential semiconductor resistance-temperature response with high sensitivity (-4%/°C), providing excellent resolution over narrow physiological spans, whereas a Platinum RTD (e.g., Pt100) has a lower positive linear sensitivity (+0.385%/°C) but superior wide-range stability and linearity."},
                {"question": "What is the physical cause of self-heating error in clinical thermistors?", "answer": "Electrical current passing through the thermistor dissipates Joule heat (P = I²·R). If the heat dissipation constant of the surrounding medium is inadequate, this self-heating raises the sensor temperature above the true tissue temperature, creating a positive measurement artifact."},
                {"question": "Why is a Wheatstone bridge circuit effective at linearizing thermistor output over narrow spans?", "answer": "The differential voltage output of a bridge with an exponential sensor has an inflection point near the bridge balance condition where second-order curvature terms cancel, yielding a linear voltage-temperature response over narrow temperature excursions (±3 °C to ±5 °C)."},
                {"question": "What is the significance of the material constant β in the thermistor equation?", "answer": "The parameter β (expressed in Kelvin) represents the activation energy of charge carriers in the transition metal oxide semiconductor material; higher β values produce greater temperature sensitivity and steeper resistance slopes."},
                {"question": "Why is 37.0 °C considered standard normothermia and what are clinical alarm limits?", "answer": "Normal core body temperature is tightly regulated around 37.0 ± 0.5 °C by hypothalamic thermoregulation. Clinical hypothermia is diagnosed below 35.0 °C, while severe hyperpyrexia occurs above 40.0 °C, posing risks of protein denaturation and cellular injury."},
                {"question": "How does lead-wire resistance affect two-wire versus four-wire bridge measurements?", "answer": "In long catheter probes, lead-wire resistance adds directly to sensor resistance, causing false temperature offsets; four-wire Kelvin connections or symmetrical bridge arm placement cancel lead resistance errors."}
            ],
            "precautions": [
                "Verify water bath circulation avoids localized thermal stratification around the submerged sensor probe.",
                "Keep sensor excitation voltage low to avoid self-heating errors exceeding clinical tolerances.",
                "Allow full thermal equilibration at each temperature increment before recording bridge telemetry.",
                "Shield bridge circuitry and wiring inside an aluminum Faraday enclosure to suppress 60 Hz electromagnetic hum."
            ],
            "limitations": [
                "The linear sensitivity model applies across the clinical window (35.0 °C to 41.0 °C); wide temperature excursions require polynomial Steinhart-Hart corrections.",
                "Assumes high-input-impedance buffer amplifier (Z_in > 10 MΩ) preventing loading of the Wheatstone bridge.",
                "Does not account for long-term semiconductor aging drift over multi-year clinical deployments.",
                "Calibration is valid for liquid immersion; air calibration requires different heat transfer boundary parameters."
            ],
            "quiz": [
                {
                    "question": "What does NTC stand for in medical thermistor technology?",
                    "options": ["Null Temperature Constant", "Negative Temperature Coefficient", "Nonlinear Thermal Calibration", "Nominal Thermal Conductor"],
                    "correct": 1,
                    "explanation": "NTC stands for Negative Temperature Coefficient, meaning electrical resistance decreases as temperature increases."
                },
                {
                    "question": "Why must electrical current through a medical thermistor probe be minimized?",
                    "options": ["To avoid electrical shock to the patient and prevent sensor self-heating artifacts", "To prevent battery explosion", "Because thermistors only conduct AC current", "To increase bridge output resistance"],
                    "correct": 0,
                    "explanation": "Limiting current prevents patient microshock hazard and eliminates internal I²R self-heating that would skew temperature readings."
                },
                {
                    "question": "If bridge output is 44.40 mV at 37.4 °C and 88.80 mV at 39.8 °C, what is the bridge sensitivity S_T?",
                    "options": ["9.25 mV/°C", "18.50 mV/°C", "37.00 mV/°C", "44.40 mV/°C"],
                    "correct": 1,
                    "explanation": "Sensitivity S_T = ΔV / ΔT = (88.80 - 44.40) mV / (39.8 - 37.4) °C = 44.40 / 2.4 = 18.50 mV/°C."
                },
                {
                    "question": "Over what clinical temperature range is core body temperature typically evaluated?",
                    "options": ["0 °C to 100 °C", "20 °C to 50 °C", "35 °C to 41 °C", "-10 °C to +40 °C"],
                    "correct": 2,
                    "explanation": "Human physiological core temperature is confined to the narrow clinical vital window of approximately 35.0 °C to 41.0 °C."
                }
            ],
            "settings": ["Thermistor: 10 kΩ NTC bead probe (β = 3950 K)", "Bridge supply: 5.000 V regulated DC", "Calibration fluid: Deionized water in circulating stirred bath"],
            "samples": [35.0, 36.2, 37.4, 38.6, 39.8, 41.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🌡️", "label": "1. Thermistor Calibration Bath"},
                {"id": "compare", "icon": "📊", "label": "2. Wheatstone Linearity"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Bridge Resistance Sandbox"}
            ]
        },
        {
            "number": 2,
            "slug": "strain-gauge-cantilever-medical-force-sensor",
            "title": "Strain-Gauge Cantilever Beam Force Sensor & Sensitivity Calibration",
            "shortTitle": "Medical Force Sensor",
            "aim": "Measure the differential voltage output of a full-bridge foil strain gauge on a medical force sensor as a function of applied tip load to evaluate gauge factor and flexural sensitivity.",
            "inputLabel": "Applied Normal Force F",
            "shortInput": "Force F",
            "inputUnit": "N",
            "min": 1.0,
            "max": 6.0,
            "step": 1.0,
            "initial": 3.0,
            "inputDecimals": 1,
            "rawLabel": "Bridge Differential Output V_out",
            "rawUnit": "mV",
            "rawDecimals": 4,
            "xAxis": "Applied force F (N)",
            "yAxis": "Differential output V_out (mV)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.5,
            "emptyY": 8.5,
            "targetName": "Force Sensor Sensitivity S_f",
            "target": "2.4500",
            "refValue": 2.4500,
            "resultUnit": "mV/N",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "V_out = S_f · F = 2.4500 · F",
            "intro": "Accurate force transduction is essential across biomedical applications, including surgical robotic haptic feedback, infusion syringe pump occlusion pressure monitoring, biomechanical gait analysis, and prosthetic limb load-bearing controls. The fundamental principle of a resistive strain gauge relies on piezoresistive foil deformation: when bonded to an elastic substrate subjected to mechanical strain ε, the fractional change in electrical resistance is governed by the gauge factor GF: ΔR / R = GF · ε. For a prismatic cantilever beam of length L, width b, and thickness h loaded at its distal tip by a force F, elementary Euler-Bernoulli beam theory dictates that the surface bending strain at distance x from the load is ε = 6·F·x / (E·b·h²). By mounting four identical active strain gauges in a full Wheatstone bridge configuration (two in tension on the top surface, two in compression on the bottom surface), the bridge sensitivity is quadrupled compared to a quarter-bridge while providing complete intrinsic common-mode cancellation of ambient thermal drift. In this experiment, a calibrated biomedical cantilever beam load cell is subjected to precision static deadweights to quantify output linearity, establish voltage sensitivity S_f, and verify transducer mechanics.",
            "modelExtra": "Evaluated on a medical-grade aluminum alloy cantilever beam (E = 70 GPa) with four 350 Ω foil strain gauges (GF = 2.10) wired in a full-bridge circuit energized by a 10.0 V DC reference. Sensitivity S_f is evaluated across loads from 1.0 N to 6.0 N.",
            "apparatus": [
                {"name": "Instrumented Cantilever Load Cell Beam", "purpose": "Provides a precision-machined aluminum alloy flexure beam with four bonded 350 Ω foil strain gauges."},
                {"name": "Full Wheatstone Bridge Conditioning Board", "purpose": "Arranges two upper tensile and two lower compressive gauges in push-pull bridge configuration."},
                {"name": "Class F1 Precision Calibration Deadweight Set", "purpose": "Applies traceable vertical calibration forces from 1.0 N to 6.0 N (±0.01% tolerance)."},
                {"name": "Stable Low-Noise Bridge Power Supply", "purpose": "Provides highly regulated 10.000 V DC excitation with < 50 μV ripple."},
                {"name": "Precision Instrumentation Amplifier & DMM", "purpose": "Amplifies microvolt bridge output and digitizes differential signals with 6.5-digit precision."},
                {"name": "Rigid Clamped Mounting Fixture", "purpose": "Prevents base rotation or compliance slippage during tip load application."}
            ],
            "procedure": [
                {"title": "Bridge Zero Balancing and Shunt Calibration", "text": "Secure the cantilever base into the rigid clamping block and adjust the bridge balance circuit until unloaded differential output reads 0.0000 mV."},
                {"title": "Excitation Voltage Verification", "text": "Measure bridge input excitation voltage at terminals with calibrated DMM; confirm steady 10.000 V reference."},
                {"title": "Initial Load Increment Application", "text": "Gently place the 1.000 N calibration weight onto the knife-edge tip loading hanger without dynamic shock."},
                {"title": "Settling and Telemetry Acquisition", "text": "Allow 15 seconds for viscoelastic relaxation and mechanical vibrations to settle; record stabilized differential bridge voltage V_out in millivolts."},
                {"title": "Stepwise Loading Progression", "text": "Progressively add calibration masses to achieve loads of 2.0, 3.0, 4.0, 5.0, and 6.0 N, logging stabilized output voltage at each load."},
                {"title": "Sensitivity Regression and Linearity Verification", "text": "Plot differential voltage V_out against applied force F, performing least-squares linear regression to determine force sensitivity S_f."}
            ],
            "topics": [
                {"question": "How does a full-bridge strain gauge arrangement achieve temperature compensation?",
                "answer": "All four gauges experience identical thermal expansion and temperature-induced resistance changes (ΔR_T). In a full bridge, adjacent arm thermal changes oppose each other (V_out ∝ [(R1+ΔR_T)/(R2+ΔR_T) - (R4+ΔR_T)/(R3+ΔR_T)]), resulting in complete common-mode cancellation of temperature drift."},
                {"question": "What is the gauge factor (GF) of a metallic foil strain gauge?", "answer": "The gauge factor is the ratio of fractional change in electrical resistance to applied mechanical strain: GF = (ΔR / R) / ε. For constantan and karma alloy foil gauges, GF is typically between 2.0 and 2.1."},
                {"question": "Why is a full bridge four times more sensitive than a single-gauge quarter bridge?", "answer": "In a full bridge on a cantilever beam, two gauges undergo tensile strain (+ε) and two undergo compressive strain (-ε). The bridge voltage equation sums all four responses: V_out = V_in · (GF · ε), compared to V_out = V_in · (GF · ε) / 4 for a quarter bridge."},
                {"question": "Where on the cantilever beam should strain gauges be mounted for maximum sensitivity?", "answer": "Bending moment in a cantilever beam is maximum at the clamped root (M = F · L) and zero at the loaded tip. Therefore, gauges must be bonded as close as possible to the clamped fixed boundary to capture maximum surface strain."},
                {"question": "What is mechanical hysteresis in a biomedical load cell?", "answer": "Hysteresis is the maximum difference in sensor output at a given load when approached from ascending loading versus descending unloading, caused by internal friction in the beam alloy and bonding adhesive creep."},
                {"question": "How does an infusion syringe pump utilize force sensors?", "answer": "An inline strain-gauge load cell measures the axial reaction force on the syringe plunger. If an intravenous catheter becomes occluded by a clot or kink, inline fluid pressure rises rapidly, causing an increase in plunger force that triggers an emergency occlusion alarm."}
            ],
            "precautions": [
                "Apply calibration deadweights gently along the beam centerline to avoid dynamic impact and torsional loading.",
                "Verify that the cantilever mounting clamp is torqued evenly to prevent false compliance at the root.",
                "Ensure strain gauge lead wires are dressed and secured with strain relief to avoid parasitic mechanical pulling forces.",
                "Shield bridge wiring from ambient electrical noise and verify zero tare offset before each trial."
            ],
            "limitations": [
                "The linear model applies strictly within the elastic limit of the aluminum beam (strain ε < 1000 με).",
                "Assumes point-load application exactly at the calibrated moment arm distance L.",
                "Does not account for transverse lateral forces or off-axis bending moments.",
                "Neglects secondary adhesive creep under long-term sustained static loading."
            ],
            "quiz": [
                {
                    "question": "What is the typical gauge factor (GF) for standard metallic foil strain gauges?",
                    "options": ["0.1 to 0.5", "2.0 to 2.2", "50 to 100", "500 to 1000"],
                    "correct": 1,
                    "explanation": "Standard constantan metal foil strain gauges have a gauge factor between 2.0 and 2.2."
                },
                {
                    "question": "Why are two gauges mounted on top and two on the bottom of a cantilever beam load cell?",
                    "options": ["To measure temperature and humidity", "To create two tensile and two compressive arms that quadruple sensitivity and cancel thermal drift", "To provide backup gauges if one burns out", "To increase electrical resistance to 1000 Ω"],
                    "correct": 1,
                    "explanation": "A full-bridge with opposite strain signs quadruples output signal amplitude while canceling common-mode temperature expansion."
                },
                {
                    "question": "If applied force is 4.0 N and bridge output is 9.8000 mV, what is the force sensitivity S_f?",
                    "options": ["1.2250 mV/N", "2.4500 mV/N", "4.9000 mV/N", "9.8000 mV/N"],
                    "correct": 1,
                    "explanation": "Sensitivity S_f = V_out / F = 9.8000 mV / 4.0 N = 2.4500 mV/N."
                },
                {
                    "question": "Where is the surface bending strain maximum in an end-loaded cantilever beam?",
                    "options": ["At the free loaded tip", "At the exact mid-span point", "At the clamped fixed base", "Uniform across the entire beam"],
                    "correct": 2,
                    "explanation": "Bending moment M(x) = F · (L - x) is highest at the clamped base (x = 0), producing maximum surface bending strain."
                }
            ],
            "settings": ["Beam material: 6061-T6 Aluminum alloy (E = 70 GPa)", "Bridge configuration: 4-gauge full bridge (350 Ω each, GF = 2.10)", "Excitation: 10.000 V DC regulated"],
            "samples": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "⚖️", "label": "1. Cantilever Load Cell Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Voltage vs Force Linearity"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Strain Gauge Bridge Sandbox"}
            ]
        },
        {
            "number": 3,
            "slug": "piezoelectric-pulse-transducer-arterial-compliance",
            "title": "Piezoelectric Sensor Charge Output & Arterial Pulse Sensitivity",
            "shortTitle": "Piezoelectric Pulse Transducer",
            "aim": "Determine the dynamic piezoelectric voltage generation and charge sensitivity of a PVDF film transducer under simulated peripheral arterial pressure pulses.",
            "inputLabel": "Pressure Pulse Amplitude ΔP",
            "shortInput": "Pulse ΔP",
            "inputUnit": "kPa",
            "min": 2.0,
            "max": 12.0,
            "step": 2.0,
            "initial": 6.0,
            "inputDecimals": 1,
            "rawLabel": "Peak Sensor Voltage V_p",
            "rawUnit": "mV",
            "rawDecimals": 3,
            "xAxis": "Pressure pulse amplitude ΔP (kPa)",
            "yAxis": "Peak sensor voltage V_p (mV)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 7.0,
            "emptyY": 85.0,
            "targetName": "Pressure Voltage Sensitivity k_p",
            "target": "14.2000",
            "refValue": 14.2000,
            "resultUnit": "mV/kPa",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "V_p = k_p · ΔP = 14.2000 · ΔP",
            "intro": "Cardiovascular diagnosis and continuous non-invasive vital sign monitoring rely on detecting peripheral arterial pulse waveforms at superficial arterial sites (such as the radial, carotid, and superficial temporal arteries). Piezoelectric polymer films, particularly polarized polyvinylidene fluoride (PVDF), are widely utilized in biomedical pulsation pickups, acoustic phonocardiography, and sleep apnea respiratory effort belts due to their exceptional dynamic responsiveness, wide mechanical bandwidth, high piezoelectric voltage coefficient (g_33), and acoustic impedance matching biological soft tissues. Unlike piezoresistive sensors that measure static pressure, piezoelectric transducers generate surface electrical charge Q solely in response to dynamic, time-varying mechanical stress: Q = d_33 · F = d_33 · A · ΔP, where d_33 is the longitudinal piezoelectric charge coefficient and A is the sensor active area. When coupled to a high-input-impedance charge amplifier, the generated peak open-circuit voltage V_p is directly proportional to applied pulse pressure amplitude ΔP: V_p = k_p · ΔP. In this laboratory investigation, a calibrated PVDF arterial pulse transducer mounted on a phantom radial artery hydraulic pulsation bench is evaluated across clinical pulse pressure increments to determine sensitivity and verify dynamic transduction linearity.",
            "modelExtra": "Evaluated using a 28 μm metallized PVDF polymer sensor element coupled to a high-input-impedance JFET charge amplifier (time constant τ = 2.5 s). Dynamic pulsation frequency standardized at 1.2 Hz (72 beats/min) simulating resting radial arterial pulses.",
            "apparatus": [
                {"name": "PVDF Film Arterial Pulse Sensor", "purpose": "Flexible 28 μm piezoelectric transducer element with screen-printed silver ink electrodes."},
                {"name": "Hydraulic Radial Artery Pulsation Phantom", "purpose": "Provides compliant silicone artery embedded in tissue-mimicking phantom driven by pulsatile pump."},
                {"name": "Electromagnetic Pulsatile Piston Pump", "purpose": "Generates physiological pressure pulse waveforms with adjustable pulse pressure from 2 to 12 kPa."},
                {"name": "Precision Disposable Blood Pressure Transducer", "purpose": "Monitors internal lumen pressure pulses with NIST-traceable piezoresistive reference."},
                {"name": "Low-Noise High-Impedance Charge Amplifier", "purpose": "Converts sensor charge into proportional voltage without low-frequency signal droop."},
                {"name": "Dual-Channel Digital Storage Oscilloscope", "purpose": "Captures peak voltage V_p and pulse transit morphology at 1.0 kHz sampling rate."}
            ],
            "procedure": [
                {"title": "Arterial Phantom Priming and Pressure Calibration", "text": "Prime the silicone radial artery phantom with degassed physiological saline and calibrate the inline reference pressure transducer to read true systolic and diastolic pressures."},
                {"title": "Sensor Placement and Pre-Load Application", "text": "Position the PVDF pulse sensor over the superficial arterial phantom site with an elastic strap establishing a baseline contact pre-load of 2.0 kPa."},
                {"title": "Pulsatile Waveform Standardization", "text": "Set the pulsatile actuator to resting heart rate cadence (72 BPM, 1.2 Hz) and establish an initial pulse pressure amplitude ΔP of 2.0 kPa (15 mmHg)."},
                {"title": "Peak Voltage Telemetry Acquisition", "text": "Capture 10 consecutive pulse cycles on the digital oscilloscope and record the ensemble-averaged peak-to-peak output voltage V_p in millivolts."},
                {"title": "Pulse Pressure Progression", "text": "Increment dynamic pulse pressure amplitude through 4.0, 6.0, 8.0, 10.0, and 12.0 kPa, logging peak piezoelectric voltage at each stage."},
                {"title": "Sensitivity Regression Analysis", "text": "Plot peak voltage V_p against pulse pressure ΔP, performing linear regression through the origin to determine pressure voltage sensitivity k_p."}
            ],
            "topics": [
                {"question": "Why are piezoelectric sensors unable to measure purely static blood pressure?", "answer": "Under a constant static force, the generated charge across the internal capacitance leaks away through the finite internal electrical resistance of the crystal and amplifier input impedance, causing output voltage to decay to zero with time constant τ = R·C."},
                {"question": "What is the advantage of PVDF polymer over traditional PZT ceramics in biomedical sensors?", "answer": "PVDF is mechanically flexible, thin (9 to 28 μm), highly compliant, and has an acoustic impedance (3.9 × 10^6 kg/(m²·s)) very close to human skin and biological soft tissue, avoiding acoustic reflection and patient discomfort."},
                {"question": "How does a charge amplifier prevent cable capacitance from attenuating piezoelectric signals?", "answer": "A charge amplifier uses an operational amplifier with capacitive feedback in an inverting configuration. The inverting terminal acts as a virtual ground, maintaining the sensor cable voltage at virtually zero and shunting cable capacitance out of the gain equation."},
                {"question": "What physiological cardiovascular information is contained in the arterial pulse waveform?", "answer": "The waveform features an initial percussion wave (systolic ejection), a tidal wave (reflected pulse), a dicrotic notch (aortic valve closure), and a dicrotic wave (diastolic runoff), reflecting cardiac contractility and arterial wall stiffness."},
                {"question": "What is the piezoelectric charge coefficient d_33?", "answer": "The d_33 coefficient represents the quantity of electrical charge generated per unit of applied mechanical force in the direction parallel to the material polarization axis (expressed in Coulombs per Newton or pC/N)."},
                {"question": "How does sensor contact pre-load pressure affect arterial pulse amplitude?", "answer": "An optimal hold-down contact pressure (applanation) unloads the arterial wall tension, maximizing transmural pressure transfer to the sensor; insufficient pre-load yields attenuated signals, while excessive pressure occludes the artery."}
            ],
            "precautions": [
                "Maintain uniform hold-down strap tension throughout testing to avoid pre-load coupling artifacts.",
                "Ensure coaxial cable between sensor and charge amplifier is immobilized to eliminate triboelectric cable noise.",
                "Verify absence of air bubbles inside the arterial fluid column that could damp pulse pressure gradients.",
                "Allow the charge amplifier output to re-zero after adjusting pulse pressure increments."
            ],
            "limitations": [
                "The linear sensitivity model applies across the physiologic pulse range (2.0 to 12.0 kPa).",
                "Assumes pulse frequency remains within the flat passband of the charge amplifier (f > 0.1 Hz).",
                "Does not account for non-linear mechanical stiffening of biological arterial walls at extreme hypertension.",
                "Specific to the tested 28 μm PVDF film geometry and sensor active footprint area."
            ],
            "quiz": [
                {
                    "question": "What is the primary physical reason piezoelectric sensors cannot measure static DC pressure?",
                    "options": ["Piezoelectric crystals melt under DC load", "Internal charge leaks off through finite sensor and circuit resistance (time constant decay)", "Charge only flows at ultrasonic frequencies", "They require external magnetic fields"],
                    "correct": 1,
                    "explanation": "Piezoelectric charge is generated by crystal dipole displacement; under static load, generated charge leaks away through finite insulation resistance."
                },
                {
                    "question": "Which piezoelectric polymer material is widely favored for flexible skin pulse sensors?",
                    "options": ["Quartz crystal", "Polyvinylidene fluoride (PVDF)", "Barium titanate", "Lead zirconate titanate (PZT)"],
                    "correct": 1,
                    "explanation": "PVDF is a flexible, highly compliant piezoelectric polymer with acoustic impedance closely matched to human tissue."
                },
                {
                    "question": "If measured peak voltage is 85.20 mV at a pulse pressure of 6.0 kPa, what is the sensitivity k_p?",
                    "options": ["7.10 mV/kPa", "14.20 mV/kPa", "28.40 mV/kPa", "85.20 mV/kPa"],
                    "correct": 1,
                    "explanation": "Sensitivity k_p = V_p / ΔP = 85.20 mV / 6.0 kPa = 14.20 mV/kPa."
                },
                {
                    "question": "What physiological event produces the dicrotic notch in an arterial pressure waveform?",
                    "options": ["Atrial contraction", "Opening of the mitral valve", "Closure of the aortic valve", "Ventricular depolarization (QRS)"],
                    "correct": 2,
                    "explanation": "The dicrotic notch (incisura) is caused by the sudden closure of the aortic valve at the end of ventricular systole."
                }
            ],
            "settings": ["Sensor element: 28 μm polarized PVDF film (active area 1.0 cm²)", "Pulsation frequency: 1.2 Hz (72 BPM) radial pulse simulation", "Amplifier: Low-noise charge amplifier (τ = 2.5 s)"],
            "samples": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💓", "label": "1. Radial Artery Pulsation Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Peak Voltage vs Pulse Pressure"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Piezoelectric Charge Sandbox"}
            ]
        },
        {
            "number": 4,
            "slug": "ag-agcl-biopotential-electrode-half-cell-impedance",
            "title": "Ag/AgCl Biopotential Electrode Half-Cell Potential & Skin Contact Impedance",
            "shortTitle": "Biopotential Electrode Impedance",
            "aim": "Investigate the frequency-dependent contact impedance and half-cell potential stability of sintered Ag/AgCl skin biopotential electrodes across AC excitation frequencies.",
            "inputLabel": "Logarithm of Frequency ln(f)",
            "shortInput": "ln(f)",
            "inputUnit": "ln(Hz)",
            "min": 2.3026,
            "max": 6.9078,
            "step": 0.921,
            "initial": 4.1352,
            "inputDecimals": 4,
            "rawLabel": "Electrode-Skin Impedance Z_e",
            "rawUnit": "kΩ",
            "rawDecimals": 3,
            "xAxis": "ln(Frequency f in Hz) (ln[Hz])",
            "yAxis": "Contact impedance Z_e (kΩ)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 4.5,
            "emptyY": 20.0,
            "targetName": "Electrode Dispersion Gradient k_z",
            "target": "4.2000",
            "refValue": 4.2000,
            "resultUnit": "kΩ/ln(Hz)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "Z_e = -k_z · ln(f) + Z_0 = -4.2000 · ln(f) + 38.5000",
            "intro": "In clinical electrophysiology, accurate acquisition of diagnostic biopotentials—including the electrocardiogram (ECG), electromyogram (EMG), and electroencephalogram (EEG)—depends critically on the performance of the electrode-electrolyte-skin interface. Biopotential electrodes act as transducers that convert ionic current flow in biological tissue into electron current flow in metallic instrument lead wires via reversible Faradaic reduction-oxidation reactions: Ag + Cl⁻ ⇌ AgCl + e⁻. Sintered silver/silver chloride (Ag/AgCl) non-polarizable electrodes are the gold standard in clinical medicine because they maintain a stable, non-polarizable half-cell potential (approximately +222 mV relative to standard hydrogen electrode) and minimize motion artifact voltages. According to classical electrical double-layer theory (Warburg and Cole-Cole dispersion models), the electrode-electrolyte interface behaves as a parallel combination of charge-transfer resistance (R_ct) and double-layer capacitance (C_dl), coupled with the stratum corneum dielectric barrier. Consequently, the electrode-skin contact impedance magnitude Z_e decreases logarithmically with increasing AC excitation frequency f: Z_e = -k_z · ln(f) + Z_0. In this experiment, a pair of clinical Ag/AgCl electrodes coupled to a skin-mimicking electrolytic phantom is evaluated across excitation frequencies from 10 Hz to 1000 Hz using four-terminal impedance spectroscopy.",
            "modelExtra": "Evaluated using sintered Ag/AgCl disposable pre-gelled electrodes (conductive hydrogel, contact area 3.0 cm²) on a skin phantom (0.9% NaCl with agar substrate). Linearized impedance dispersion is evaluated across the clinical biopotential diagnostic band (10 Hz to 1000 Hz).",
            "apparatus": [
                {"name": "Clinical Sintered Ag/AgCl Electrodes", "purpose": "Standard disposable medical electrodes with medical-grade Ag/AgCl conductive hydrogel interface."},
                {"name": "Stratum Corneum Skin-Mimicking Phantom", "purpose": "Provides controlled resistive-capacitive biological tissue substrate (0.9% saline agar with polymer membrane)."},
                {"name": "Four-Terminal Precision LCR Impedance Analyzer", "purpose": "Applies low-amplitude sinusoidal current (10 μA RMS) and measures complex impedance Z(f)."},
                {"name": "Faraday Shielding Isolation Chamber", "purpose": "Eliminates capacitive 60 Hz hum pickup during high-impedance low-frequency measurements."},
                {"name": "High-Precision Digital Caliper", "purpose": "Measures exact inter-electrode spacing (50.0 mm) on the phantom surface."},
                {"name": "Calibrated DC Reference Half-Cell Potentiometer", "purpose": "Verifies electrode DC offset potential difference remains below 2.0 mV."}
            ],
            "procedure": [
                {"title": "Skin Phantom Hydration and Electrode Mounting", "text": "Apply a uniform 1.0 mm layer of chloride hydrogel to the phantom substrate and affix two Ag/AgCl electrodes at 50.0 mm center-to-center distance."},
                {"title": "DC Offset Potential Verification", "text": "Connect electrodes to the digital multimeter; verify DC half-cell offset potential is stable and under 2.0 mV (ensuring matched electrode pairs)."},
                {"title": "LCR Analyzer Excitation Setup", "text": "Configure the impedance analyzer in four-wire mode with safe physiological current excitation of 10.0 μA RMS."},
                {"title": "Low-Frequency Baseline Measurement", "text": "Apply 10 Hz sinusoidal excitation (ln(10) = 2.3026 ln[Hz]); record stabilized contact impedance magnitude Z_e in kΩ."},
                {"title": "Frequency Sweep Progression", "text": "Increment frequency through 25, 62.5, 156, 390, and 1000 Hz (ln(f) = 3.2189, 4.1352, 5.0515, 5.9678, 6.9078), recording Z_e at each point."},
                {"title": "Dispersion Regression Analysis", "text": "Plot contact impedance Z_e against ln(f), performing linear regression to evaluate the electrode dispersion gradient k_z."}
            ],
            "topics": [
                {"question": "What is the fundamental difference between a polarizable and a non-polarizable electrode?", "answer": "In a perfectly polarizable electrode (e.g., pure platinum or gold), no actual charge crosses the interface; current is purely capacitive displacement across the electrical double layer. In a non-polarizable electrode (Ag/AgCl), Faradaic chemical reactions freely exchange charge across the interface, eliminating voltage buildup and motion artifacts."},
                {"question": "Why is Ag/AgCl the preferred material for clinical ECG and EEG recording?", "answer": "Ag/AgCl is a reversible, non-polarizable electrode with a stable, reproducible half-cell potential, very low intrinsic noise, and low polarization overpotential, which suppresses low-frequency baseline wander and movement artifacts."},
                {"question": "Why does electrode-skin impedance decrease at higher frequencies?", "answer": "The skin's stratum corneum and the electrode double layer act as parallel resistor-capacitor networks (Warburg/Cole-Cole model). As AC frequency increases, capacitive reactance (X_C = 1 / (2πfC)) decreases, shunting AC current and lowering total impedance magnitude."},
                {"question": "What is the clinical consequence of high electrode contact impedance in ECG recording?", "answer": "High contact impedance attenuates biopotential amplitudes, unbalances differential amplifier input stages, converts common-mode 60 Hz electrical noise into severe differential interference, and degrades diagnostic fidelity."},
                {"question": "How does skin preparation (alcohol swabbing, mild abrasion) reduce contact impedance?", "answer": "Mild abrasion removes the outer dead, non-conductive keratinized cells of the stratum corneum and strips surface sebum oils, directly exposing the moist, conductive deeper epidermal layers."},
                {"question": "What is the purpose of the conductive chloride electrolyte gel in disposable electrodes?", "answer": "The gel contains mobile Cl⁻ ions necessary to maintain the Ag/AgCl equilibrium reaction, provides continuous ohmic contact with irregular skin pores, and displaces air bubbles that cause open-circuit contact."}
            ],
            "precautions": [
                "Verify electrode gel is fresh and moist; desiccated hydrogel causes catastrophic impedance spikes.",
                "Maintain constant inter-electrode distance and contact pressure on the phantom surface across all trials.",
                "Enclose the test phantom inside a grounded Faraday cage to suppress 60 Hz electrostatic pickup.",
                "Keep excitation current below 10 μA RMS to ensure strictly linear, non-destructive electrochemical impedance."
            ],
            "limitations": [
                "The logarithmic dispersion model applies across the diagnostic biopotential frequency band (10 Hz to 1000 Hz).",
                "Assumes homogeneous skin phantom; living human skin displays sweat gland dynamics and vasodilation shifts.",
                "Does not model motion-induced streaming potential artifacts caused by rapid physical cable tugging.",
                "Specific to 3.0 cm² Ag/AgCl electrodes; pediatric or needle electrodes have higher baseline impedances."
            ],
            "quiz": [
                {
                    "question": "What reversible electrochemical reaction occurs at the interface of an Ag/AgCl biopotential electrode?",
                    "options": ["2 H₂O → 2 H₂ + O₂", "Ag + Cl⁻ ⇌ AgCl + e⁻", "Zn + Cu²⁺ → Zn²⁺ + Cu", "NaCl → Na + Cl"],
                    "correct": 1,
                    "explanation": "Silver oxidizes with chloride to form silver chloride and an electron, establishing a reversible Faradaic non-polarizable interface."
                },
                {
                    "question": "Why does electrode-skin impedance decrease as frequency increases from 10 Hz to 1000 Hz?",
                    "options": ["The skin heats up and melts", "Capacitive reactance of the stratum corneum double-layer decreases (X_c = 1 / ωC)", "Electrode leads shorten at high frequency", "Electrons travel faster than ions"],
                    "correct": 1,
                    "explanation": "Because biological membranes and double layers act as capacitors, increasing frequency lowers capacitive reactance, providing an easy AC pathway."
                },
                {
                    "question": "If contact impedance is 28.84 kΩ at ln(f) = 2.3026 and 16.24 kΩ at ln(f) = 5.3026, what is the dispersion gradient k_z?",
                    "options": ["2.10 kΩ/ln(Hz)", "4.20 kΩ/ln(Hz)", "8.40 kΩ/ln(Hz)", "12.60 kΩ/ln(Hz)"],
                    "correct": 1,
                    "explanation": "k_z = -ΔZ / Δln(f) = -(16.24 - 28.84) kΩ / (5.3026 - 2.3026) = 12.60 / 3.00 = 4.20 kΩ/ln(Hz)."
                },
                {
                    "question": "What is the primary danger of using polarizable metal electrodes (like bare copper) for ECG recording?",
                    "options": ["They catch fire", "They produce massive DC offset voltages and severe motion artifacts", "They erase the cardiac pacemaker rhythm", "They generate X-rays"],
                    "correct": 1,
                    "explanation": "Polarizable metals build up capacitive charge layers that fluctuate wildly with patient movement, causing severe motion artifacts that obscure ECG signals."
                }
            ],
            "settings": ["Electrode type: Disposable Ag/AgCl with conductive hydrogel (3.0 cm²)", "Substrate: Agar saline skin phantom (0.9% NaCl)", "Excitation: 10 μA RMS sinusoidal four-terminal sensing"],
            "samples": [2.3026, 3.2189, 4.1352, 5.0515, 5.9678, 6.9078],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "⚡", "label": "1. Electrode Impedance Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Cole-Cole Dispersion Plot"},
                {"id": "sandbox", "icon": "🔬", "label": "3. Double-Layer Interface Sandbox"}
            ]
        },
        {
            "number": 5,
            "slug": "instrumentation-amplifier-cmrr-ecg-front-end",
            "title": "Three-Op-Amp Instrumentation Amplifier Common-Mode Rejection Ratio (CMRR)",
            "shortTitle": "Instrumentation Amplifier CMRR",
            "aim": "Measure differential gain and common-mode gain of a classic three-op-amp biomedical instrumentation amplifier to calculate CMRR across common-mode interference voltages.",
            "inputLabel": "Common-Mode Input Voltage V_cm",
            "shortInput": "V_cm",
            "inputUnit": "V",
            "min": 0.5,
            "max": 3.0,
            "step": 0.5,
            "initial": 1.5,
            "inputDecimals": 1,
            "rawLabel": "Common-Mode Output Voltage V_out,cm",
            "rawUnit": "mV",
            "rawDecimals": 4,
            "xAxis": "Common-mode input V_cm (V)",
            "yAxis": "Common-mode output V_out,cm (mV)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 1.75,
            "emptyY": 0.08,
            "targetName": "Common-Mode Voltage Gain A_cm",
            "target": "0.0480",
            "refValue": 0.0480,
            "resultUnit": "mV/V",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "V_out,cm = A_cm · V_cm = 0.0480 · V_cm",
            "intro": "In clinical biopotential recording (ECG, EEG, EMG), the target physiological signal is exceedingly small—typically 1.0 mV for ECG and under 50 μV for EEG. Simultaneously, the human body acts as an antenna that capacitively couples to 50/60 Hz powerline electric fields, inducing large common-mode interference voltages (often 1.0 V to 3.0 V peak-to-peak, thousands of times larger than the bioelectric signal). Extracting microvolt biopotentials in the presence of massive common-mode noise requires an analog front-end with an extraordinary Common-Mode Rejection Ratio (CMRR > 90 to 110 dB). The classic three-operational-amplifier instrumentation amplifier (INA) achieves this through a buffered input stage with gain R_G: differential gain is set by A_d = (1 + 2·R_1 / R_G) · (R_3 / R_2), while ideal common-mode gain is A_cm = 0. In physical hardware, small resistor mismatches (tolerance error ΔR/R) in the second-stage difference amplifier allow a fraction of common-mode input voltage V_cm to leak into the output: V_out,cm = A_cm · V_cm. The CMRR in decibels is defined as CMRR = 20 · log10(A_d / A_cm). In this laboratory experiment, a precision biomedical instrumentation amplifier (configured for differential gain A_d = 1000 V/V) is tested across regulated common-mode test voltages to quantify A_cm, verify linear leakage, and evaluate front-end CMRR.",
            "modelExtra": "Evaluated using a low-noise medical instrumentation amplifier (INA118 precision architecture) configured for fixed differential gain A_d = 1000. Common-mode gain A_cm is evaluated across 60 Hz sinusoidal common-mode voltages from 0.5 V to 3.0 V RMS.",
            "apparatus": [
                {"name": "Three-Op-Amp Precision Instrumentation Amplifier", "purpose": "Provides buffered high-input-impedance (10 GΩ) differential biopotential amplification."},
                {"name": "Calibrated Precision Resistor Network (0.01% matched)", "purpose": "Establishes difference stage symmetry to achieve high common-mode rejection."},
                {"name": "Dual-Channel Arbitrary Function Generator", "purpose": "Supplies calibrated 60 Hz common-mode sinusoidal test voltages from 0.5 V to 3.0 V RMS."},
                {"name": "Low-Noise True-RMS Digital Microvoltmeter", "purpose": "Measures microvolt-level common-mode leakage output V_out,cm with 100 nV resolution."},
                {"name": "Dual Regulated DC Power Supply (±15.00 V)", "purpose": "Powers the operational amplifier rails with ultra-low thermal noise and ripple."},
                {"name": "Digital Storage Oscilloscope with FFT Spectrum Analyzer", "purpose": "Monitors output waveform purity and verifies absence of rail saturation or clipping."}
            ],
            "procedure": [
                {"title": "Differential Gain Verification", "text": "Apply a 1.000 mV peak-to-peak 10 Hz pure differential input signal; verify that differential output reads exactly 1.000 V peak-to-peak, confirming A_d = 1000 V/V."},
                {"title": "Common-Mode Test Configuration", "text": "Tie both differential non-inverting and inverting inputs together to apply identical common-mode voltage V_cm simultaneously."},
                {"title": "Initial Common-Mode Excitation", "text": "Apply a 60 Hz sinusoidal common-mode voltage of 0.500 V RMS, monitoring amplifier rails to ensure linear range."},
                {"title": "Microvolt Output Leakage Measurement", "text": "Measure the residual 60 Hz output voltage V_out,cm using the precision true-RMS microvoltmeter over a 30-second integration window."},
                {"title": "Common-Mode Progression Sequence", "text": "Increment common-mode voltage V_cm through 1.0, 1.5, 2.0, 2.5, and 3.0 V RMS, recording V_out,cm at each stage."},
                {"title": "Gain Regression and CMRR Computation", "text": "Plot V_out,cm against V_cm to determine common-mode gain A_cm = slope / 1000 (in V/V), then calculate CMRR = 20·log10(A_d / A_cm)."}
            ],
            "topics": [
                {"question": "How is Common-Mode Rejection Ratio (CMRR) defined mathematically?", "answer": "CMRR is the ratio of differential voltage gain to common-mode voltage gain: CMRR = A_d / A_cm. Expressed in decibels: CMRR_dB = 20 · log10(A_d / A_cm). Higher values indicate superior suppression of common-mode interference."},
                {"question": "Why is high CMRR indispensable in biomedical ECG amplifiers?", "answer": "The human body picks up 1 to 3 V of 60 Hz electrostatic displacement current from power wiring, while the cardiac ECG signal is only ~1 mV. A CMRR of at least 100 dB (100,000:1) is required to reduce 1 V of noise to under 10 μV, preventing it from overwhelming the ECG."},
                {"question": "What is the primary factor limiting CMRR in real-world instrumentation amplifiers?", "answer": "Resistor mismatch in the subtractor difference stage. Even with 0.1% tolerance resistors, worst-case mismatch can limit second-stage CMRR to roughly 66 dB unless active laser trimming or high-gain input buffers are used."},
                {"question": "How does the first input stage of a three-op-amp INA affect common-mode gain?", "answer": "The two input buffer op-amps amplify differential signals by (1 + 2·R1/RG) while passing common-mode signals at unity gain (A_cm,1 = 1). This boosts differential amplitude before the difference stage, dramatically enhancing overall CMRR."},
                {"question": "What is the Right Leg Drive (RLD) circuit and how does it improve clinical ECG recording?", "answer": "The RLD circuit samples common-mode body noise, inverts it through an active op-amp, and feeds it back into the patient's right leg. This acts as an active electronic ground that cancels the body's common-mode voltage, reducing effective noise by 20 to 40 dB."},
                {"question": "Why must biomedical amplifiers possess extraordinarily high input impedance (> 10 GΩ)?", "answer": "Skin-electrode contact impedances are high and unequal (e.g., 5 kΩ vs 15 kΩ). High amplifier input impedance prevents these source imbalances from converting common-mode voltage into differential noise through voltage divider action."}
            ],
            "precautions": [
                "Verify both inputs receive identical common-mode voltage using matched shielded coaxial leads.",
                "Ensure common-mode voltage does not exceed op-amp common-mode input range (±13 V on ±15 V rails).",
                "Shield the test circuit in a grounded aluminum enclosure to prevent stray capacitive pickup from lighting.",
                "Warm up instrumentation for 20 minutes to achieve thermal equilibrium before logging microvolt data."
            ],
            "limitations": [
                "The linear leakage model applies within the linear common-mode input range (V_cm ≤ 3.0 V).",
                "Assumes balanced low-impedance signal source; does not model source impedance unbalance degradation.",
                "Valid for powerline frequencies (50/60 Hz); CMRR degrades at higher frequencies due to stray capacitance.",
                "Neglects op-amp input bias current offset voltage drift over ambient temperature shifts."
            ],
            "quiz": [
                {
                    "question": "If differential gain A_d is 1000 and common-mode gain A_cm is 0.000048 V/V, what is the CMRR in dB?",
                    "options": ["46.4 dB", "66.4 dB", "86.4 dB", "106.4 dB"],
                    "correct": 3,
                    "explanation": "CMRR = 1000 / 0.000048 = 20,833,333; in dB: 20 · log10(20,833,333) = 20 · 7.3188 = 106.4 dB."
                },
                {
                    "question": "What is the primary source of 60 Hz common-mode interference on a patient during clinical ECG recording?",
                    "options": ["Patient muscle shivering", "Capacitive displacement current coupled from ambient electrical wiring into the human body", "Electrochemical reaction of the electrode gel", "Blood flow friction against vessel walls"],
                    "correct": 1,
                    "explanation": "Displacement current capacitively coupled from powerlines (120/240 V AC) through air into the conductive human body creates 1 to 3 V of 60 Hz common-mode voltage."
                },
                {
                    "question": "If common-mode input is 2.50 V and common-mode output is 0.1200 mV, what is the gain A_cm in mV/V?",
                    "options": ["0.0120 mV/V", "0.0240 mV/V", "0.0480 mV/V", "0.0960 mV/V"],
                    "correct": 2,
                    "explanation": "A_cm = V_out,cm / V_cm = 0.1200 mV / 2.50 V = 0.0480 mV/V."
                },
                {
                    "question": "What clinical circuit actively inverts and cancels common-mode body noise in medical ECG monitors?",
                    "options": ["Bessel lowpass filter", "Right Leg Drive (RLD) circuit", "Schmitt trigger", "Envelope detector"],
                    "correct": 1,
                    "explanation": "The Right Leg Drive circuit detects common-mode voltage on the torso, inverts it, and drives it back to the patient to actively cancel common-mode noise."
                }
            ],
            "settings": ["Amplifier: Medical INA118 instrumentation topology", "Differential gain: A_d = 1000 V/V (60 dB)", "Test frequency: 60.0 Hz sinusoidal common-mode source"],
            "samples": [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🎛️", "label": "1. INA Test Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Common-Mode Linearity"},
                {"id": "sandbox", "icon": "⚡", "label": "3. CMRR Front-End Sandbox"}
            ]
        },
        {
            "number": 6,
            "slug": "clark-oxygen-polarographic-electrode-blood-po2",
            "title": "Clark Polarographic Electrode Limiting Diffusion Current & Oxygen Tension",
            "shortTitle": "Clark Oxygen Electrode",
            "aim": "Measure the steady-state cathodic reduction limiting diffusion current of a membrane-covered Clark polarographic oxygen electrode across calibrated dissolved oxygen partial pressures.",
            "inputLabel": "Oxygen Partial Pressure P_O2",
            "shortInput": "P_O2",
            "inputUnit": "kPa",
            "min": 2.0,
            "max": 17.0,
            "step": 3.0,
            "initial": 8.0,
            "inputDecimals": 1,
            "rawLabel": "Cathodic Reduction Current I_d",
            "rawUnit": "nA",
            "rawDecimals": 3,
            "xAxis": "Oxygen partial pressure P_O2 (kPa)",
            "yAxis": "Cathodic current I_d (nA)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 9.5,
            "emptyY": 15.0,
            "targetName": "Oxygen Diffusion Sensitivity k_O2",
            "target": "1.6500",
            "refValue": 1.6500,
            "resultUnit": "nA/kPa",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "I_d = k_O2 · P_O2 = 1.6500 · P_O2",
            "intro": "In critical care medicine, respiratory physiology, and arterial blood gas (ABG) clinical laboratories, continuous quantification of blood oxygen tension (PO2) is vital for managing patients with acute respiratory distress syndrome (ARDS), chronic obstructive pulmonary disease (COPD), and during mechanical ventilation. Invented by Leland Clark in 1956, the Clark polarographic electrode revolutionized medical diagnostics by isolating the working cathode and reference anode behind an oxygen-permeable, electrically insulating polymer membrane (typically Teflon or polypropylene). When a polarizing potential of -0.65 to -0.75 V is applied to the platinum working micro-cathode relative to an Ag/AgCl reference anode immersed in KCl buffer, molecular oxygen diffusing through the membrane undergoes immediate four-electron electrochemical reduction at the platinum surface: O2 + 2 H2O + 4 e⁻ → 4 OH⁻. Because the reduction reaction is virtually instantaneous at this polarizing plateau voltage, surface oxygen concentration drops to zero, and the resulting steady-state cathodic current I_d is strictly governed by Fick's first law of diffusion: I_d = 4·F·(P_m·A / x_m) · P_O2 = k_O2 · P_O2, where F is Faraday's constant, P_m is membrane permeability, A is cathode area, x_m is membrane thickness, and P_O2 is oxygen partial pressure. In this experiment, a clinical Clark electrode cell is tested across calibrated gas-equilibrated saline solutions to establish linearity and determine oxygen sensitivity k_O2.",
            "modelExtra": "Evaluated on a 25 μm diameter platinum micro-cathode with 12 μm Teflon membrane in a 37.0 °C thermostatted micro-flowcell with -0.70 V polarizing potential. Calibrated across 2.0 kPa to 17.0 kPa (15 to 128 mmHg) oxygen partial pressure.",
            "apparatus": [
                {"name": "Clark Polarographic Oxygen Electrode Probe", "purpose": "Platinum micro-cathode (25 μm) and concentric Ag/AgCl reference anode behind Teflon membrane."},
                {"name": "Thermostatted Water-Jacketed Micro-Flowcell", "purpose": "Maintains blood gas calibration temperature at strictly 37.00 ± 0.05 °C."},
                {"name": "Precision Potentiostat Polarographic Controller", "purpose": "Applies regulated -0.700 V cathodic polarizing voltage and buffers nanoamp currents."},
                {"name": "Calibrated Gas Tonometer Equilibration System", "purpose": "Equilibrates physiological saline with certified precision O2/N2/CO2 gas mixtures."},
                {"name": "Femtoammeter / Low-Current Electrometer", "purpose": "Digitizes steady-state cathodic reduction current with 0.01 nA measurement precision."},
                {"name": "NIST-Traceable Barometer & Humidity Sensor", "purpose": "Calculates true dry gas partial pressures accounting for water vapor saturation."}
            ],
            "procedure": [
                {"title": "Membrane Inspection and Polarizing Setup", "text": "Inspect the 12 μm Teflon membrane for micro-tears, fill electrolyte well with fresh 0.1 M KCl buffer, and apply -0.700 V cathodic polarizing potential."},
                {"title": "Zero-Oxygen Baseline Calibration", "text": "Perfuse the flowcell with zero-oxygen calibration fluid (deoxygenated with sodium sulfite) and record residual dark background current (I_0 < 0.1 nA)."},
                {"title": "Initial Oxygen Step Calibration", "text": "Perfuse saline tonometered to P_O2 = 2.0 kPa (15.0 mmHg) at 37.0 °C, establishing a constant perfusion velocity to prevent boundary layer depletion."},
                {"title": "Diffusion Plateau Current Acquisition", "text": "Allow 45 seconds for diffusion boundary layer stabilization; record steady-state cathodic current I_d in nanoamperes."},
                {"title": "Oxygen Partial Pressure Progression", "text": "Increment tonometered oxygen partial pressure through 5.0, 8.0, 11.0, 14.0, and 17.0 kPa (up to physiological normoxia ~100-128 mmHg), logging I_d at each step."},
                {"title": "Diffusion Sensitivity Regression Analysis", "text": "Plot reduction current I_d against oxygen partial pressure P_O2, performing linear regression through zero to calculate diffusion sensitivity k_O2."}
            ],
            "topics": [
                {"question": "What is the primary electrochemical reaction occurring at the platinum cathode of a Clark electrode?", "answer": "Molecular oxygen is reduced via a four-electron reaction: O2 + 2 H2O + 4 e⁻ → 4 OH⁻. Each mole of oxygen consumed transfers four moles of electrons, generating a measurable electric current directly proportional to the rate of oxygen diffusion."},
                {"question": "Why is the Teflon membrane essential in a Clark electrode?", "answer": "The membrane is permeable to non-polar gases like O2 and CO2 but impermeable to ions, proteins, red blood cells, and heavy metal contaminants in blood that would otherwise poison the catalytic platinum surface and short-circuit the electrochemical cell."},
                {"question": "Why is polarographic current independent of polarizing voltage between -0.6 V and -0.8 V?", "answer": "This range forms the 'limiting diffusion current plateau'. In this voltage region, electrochemical reduction kinetics are so rapid that all oxygen reaching the cathode is instantly consumed; therefore, current is limited solely by the physical rate of diffusion through the membrane."},
                {"question": "What is the 'stirring effect' (boundary layer depletion) in Clark oxygen electrodes?", "answer": "Because the electrode consumes oxygen as it measures it, a depleted stagnant fluid boundary layer forms adjacent to the outer membrane in stagnant liquids, reducing apparent current; continuous fluid flow or stirring is required to maintain true bulk PO2 at the membrane interface."},
                {"question": "Why must blood gas analysis be performed at exactly 37.0 °C?", "answer": "Both gas solubility in blood (Bunsen coefficient) and membrane permeability follow steep exponential Arrhenius relationships with temperature; a 1 °C temperature shift causes approximately a 5% to 7% error in measured PO2."},
                {"question": "What is normal arterial PO2 in healthy humans breathing room air at sea level?", "answer": "Normal arterial oxygen tension (PaO2) ranges between 11.0 and 13.3 kPa (80 to 100 mmHg); values below 8.0 kPa (60 mmHg) indicate clinical hypoxemia requiring supplemental oxygen therapy."}
            ],
            "precautions": [
                "Maintain constant fluid perfusion velocity over the membrane to eliminate stagnant boundary layer depletion.",
                "Control flowcell temperature strictly at 37.00 ± 0.05 °C to prevent thermal solubility and diffusion artifacts.",
                "Ensure zero air bubbles are trapped within the electrolyte cavity beneath the Teflon membrane.",
                "Allow polarizing current to stabilize for at least 15 minutes prior to initial calibration recording."
            ],
            "limitations": [
                "The linear diffusion model applies across physiological blood gas oxygen ranges (2.0 to 17.0 kPa).",
                "Assumes clean, non-fouled membrane; protein deposition during whole blood perfusion gradually reduces permeability.",
                "Consumes oxygen during measurement; not suitable for tiny un-stirred micro-droplet samples.",
                "Sensitive to anesthetic gases like halothane, which undergo cathodic reduction at similar polarizing potentials."
            ],
            "quiz": [
                {
                    "question": "How many electrons are transferred per molecule of oxygen reduced at the Clark electrode cathode?",
                    "options": ["1 electron", "2 electrons", "4 electrons", "8 electrons"],
                    "correct": 2,
                    "explanation": "The stoichiometric reduction of one O2 molecule consumes 4 electrons: O2 + 2 H2O + 4 e⁻ → 4 OH⁻."
                },
                {
                    "question": "What prevents red blood cells and plasma proteins from poisoning the platinum cathode in a Clark electrode?",
                    "options": ["High magnetic field", "Oxygen-permeable Teflon/polypropylene polymer membrane", "High electric voltage", "Enzyme catalyst"],
                    "correct": 1,
                    "explanation": "The hydrophobic Teflon membrane allows dissolved oxygen gas to diffuse through while blocking proteins, cells, and fouling ions."
                },
                {
                    "question": "If oxygen partial pressure is 11.0 kPa and reduction current is 18.15 nA, what is the sensitivity k_O2?",
                    "options": ["0.8250 nA/kPa", "1.6500 nA/kPa", "3.3000 nA/kPa", "6.6000 nA/kPa"],
                    "correct": 1,
                    "explanation": "k_O2 = I_d / P_O2 = 18.15 nA / 11.0 kPa = 1.6500 nA/kPa."
                },
                {
                    "question": "What happens if calibration fluid is completely stagnant against the Clark electrode membrane?",
                    "options": ["Current increases to infinity", "Current drops due to local oxygen consumption creating a depleted boundary layer", "Electrode polarity reverses", "Membrane dissolves"],
                    "correct": 1,
                    "explanation": "Continuous oxygen consumption creates a depleted boundary layer in stagnant fluid ('stirring effect'), lowering measured current."
                }
            ],
            "settings": ["Cathode: 25 μm Platinum wire polarized at -0.700 V", "Membrane: 12 μm Teflon with 0.1 M KCl buffer", "Temperature: 37.00 ± 0.05 °C constant water bath"],
            "samples": [2.0, 5.0, 8.0, 11.0, 14.0, 17.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🩸", "label": "1. Clark Electrode Flowcell"},
                {"id": "compare", "icon": "📊", "label": "2. Polarographic Diffusion Current"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Oxygen Electrochemistry Sandbox"}
            ]
        },
        {
            "number": 7,
            "slug": "linear-variable-differential-transformer-displacement",
            "title": "LVDT Displacement Sensor Linearity & Sensitivity for Chest Wall Expansion",
            "shortTitle": "LVDT Displacement Sensor",
            "aim": "Calibrate the differential secondary AC voltage output of a Linear Variable Differential Transformer (LVDT) as a function of core displacement for physiological respiration monitoring.",
            "inputLabel": "Core Displacement x",
            "shortInput": "Core x",
            "inputUnit": "mm",
            "min": 1.0,
            "max": 6.0,
            "step": 1.0,
            "initial": 3.0,
            "inputDecimals": 1,
            "rawLabel": "Demodulated Output Voltage V_dc",
            "rawUnit": "V",
            "rawDecimals": 4,
            "xAxis": "Core displacement x (mm)",
            "yAxis": "Demodulated output V_dc (V)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.5,
            "emptyY": 3.0,
            "targetName": "Displacement Calibration Sensitivity S_x",
            "target": "0.8500",
            "refValue": 0.8500,
            "resultUnit": "V/mm",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "V_dc = S_x · x = 0.8500 · x",
            "intro": "Accurate linear displacement transduction is vital in medical diagnostic systems, including respiratory chest-wall plethysmography, prosthetic knee joint articulation tracking, spinal distraction monitoring, and precision mechanical organ tissue biomechanics. The Linear Variable Differential Transformer (LVDT) is an electromechanical inductive sensor consisting of a central primary coil flanked symmetrically by two identical secondary coils wound on a cylindrical bobbin, with a high-permeability ferromagnetic nickel-iron core moving axially inside the bore. When energized with a carrier AC excitation voltage (typically 2.5 kHz to 5 kHz), the primary magnetic flux couples mutual inductances M1 and M2 into the two secondary windings, which are connected in series-opposition (differential pairing). At the magnetic null center position, the induced secondary voltages are equal and out of phase, yielding zero net differential output. As the core displaces by distance x, the magnetic coupling increases in one secondary and decreases in the other. Following phase-sensitive demodulation and low-pass filtering, the resulting DC output voltage V_dc is directly proportional to axial core displacement: V_dc = S_x · x. In this experiment, a medical-grade LVDT mounted on a micrometer calibration stage is tested to evaluate linearity, zero null symmetry, and displacement sensitivity S_x.",
            "modelExtra": "Evaluated using a miniature medical LVDT (stroke ±10.0 mm) excited by 3.0 V RMS at 2.5 kHz carrier frequency. Phase-sensitive synchronous demodulation outputs filtered DC voltage calibrated from 1.0 mm to 6.0 mm displacement.",
            "apparatus": [
                {"name": "Miniature Medical LVDT Sensor Assembly", "purpose": "Provides primary excitation coil, twin differentially paired secondaries, and movable core."},
                {"name": "Precision Non-Magnetic Micrometer Stage", "purpose": "Applies controlled axial core displacements with 1.0 μm mechanical positioning accuracy."},
                {"name": "2.5 kHz Low-Distortion Sine Wave Carrier Generator", "purpose": "Supplies stable 3.00 V RMS sinusoidal primary excitation with < 0.1% distortion."},
                {"name": "Phase-Sensitive Synchronous Demodulator & Filter", "purpose": "Converts differential AC carrier signal into rectified DC voltage with sign detection."},
                {"name": "High-Precision 6.5-Digit Digital Multimeter", "purpose": "Measures demodulated DC output voltage V_dc with microvolt accuracy."},
                {"name": "Non-Magnetic Aluminum Shielded Mounting Test Stand", "purpose": "Prevents external magnetic flux interference from distorting coil coupling."}
            ],
            "procedure": [
                {"title": "Mechanical and Magnetic Null Centering", "text": "Mount the LVDT into the micrometer stage and adjust the core position until secondary AC differential voltage reaches absolute minimum (null voltage < 2.0 mV)."},
                {"title": "Carrier Excitation Frequency Standardization", "text": "Set the carrier function generator to 2.500 kHz at 3.000 V RMS, verifying stable primary coil current."},
                {"title": "Initial Displacement Increment Seating", "text": "Advance the micrometer spindle to displace the magnetic core by exactly 1.000 mm from the calibrated null position."},
                {"title": "Demodulated Output Voltage Logging", "text": "Record the filtered DC output voltage V_dc on the 6.5-digit multimeter after allowing 5 seconds for filter settling."},
                {"title": "Displacement Step Progression", "text": "Advance the micrometer stage in 1.000 mm increments through 2.0, 3.0, 4.0, 5.0, and 6.0 mm, recording stabilized DC voltage at each step."},
                {"title": "Sensitivity Regression and Linearity Verification", "text": "Plot demodulated DC voltage V_dc against displacement x, performing linear regression through zero to determine displacement sensitivity S_x."}
            ],
            "topics": [
                {"question": "How does an LVDT eliminate physical friction and mechanical wear?",
                "answer": "There is no physical contact between the movable high-permeability magnetic core and the coil bore walls. Because the core floats freely in air or fluid inside the coil tube, there is virtually zero mechanical friction, no hysteresis, and an essentially infinite operational lifespan."},
                {"question": "Why are the two secondary coils connected in series-opposition?", "answer": "Series-opposition connection means their induced AC voltages subtract: V_sec = V_s1 - V_s2. At the center null position, V_s1 = V_s2, producing zero net voltage and allowing the polarity (phase) of the output to indicate the direction of core movement."},
                {"question": "What is the function of phase-sensitive demodulation in an LVDT signal conditioner?", "answer": "The raw differential secondary AC voltage only provides magnitude. A phase-sensitive demodulator compares the phase of the secondary signal with the primary carrier reference to assign a positive sign for displacement in one direction and a negative sign for the opposite direction."},
                {"question": "What causes residual 'null voltage' at the magnetic zero position?", "answer": "Residual null voltage (typically a few millivolts) is caused by small harmonic distortions in the primary excitation, slight capacitive coupling between primary and secondary windings, and minute metallurgical impurities in the magnetic core."},
                {"question": "How is an LVDT utilized in respiratory chest wall displacement monitoring?", "answer": "The LVDT core is connected to an elastic thoracic circumference harness; cyclic expansion and contraction of the ribcage during inhalation and exhalation moves the core, translating chest excursion directly into proportional respiratory volume waveforms."},
                {"question": "What are the advantages of LVDTs over resistive potentiometers in medical equipment?", "answer": "Potentiometers suffer from mechanical wiper contact wear, contact electrical noise, and poor resolution. LVDTs offer frictionless operation, infinite theoretical resolution, superior isolation, and immune hermetic sealing capability."}
            ],
            "precautions": [
                "Use non-magnetic fixtures (brass, aluminum, plastic) to mount the LVDT; ferrous metals distort flux pathways.",
                "Ensure the micrometer spindle advances axially without tilting or applying transverse radial loads to the core.",
                "Verify carrier excitation voltage and frequency remain strictly constant throughout calibration.",
                "Keep the sensor cable well-shielded to prevent capacitive pickup from external power wiring."
            ],
            "limitations": [
                "The linear sensitivity model applies within the linear stroke envelope (x ≤ 6.0 mm for the tested unit).",
                "Dynamic frequency response is limited by the carrier excitation frequency (typically bandwidth < 10% of carrier).",
                "Temperature changes alter coil copper resistance; high-end signal conditioners use primary current regulation.",
                "External strong stray magnetic fields can induce offset errors if ferromagnetic shielding is breached."
            ],
            "quiz": [
                {
                    "question": "What does LVDT stand for in medical displacement instrumentation?",
                    "options": ["Low Voltage Direct Transducer", "Linear Variable Differential Transformer", "Light Valved Diode Technology", "Laser Vector Displacement Tracking"],
                    "correct": 1,
                    "explanation": "LVDT stands for Linear Variable Differential Transformer, an inductive electromechanical position transducer."
                },
                {
                    "question": "Why do LVDTs possess virtually infinite theoretical measurement resolution?",
                    "options": ["Because they use digital optical lasers", "Because displacement relies on continuous electromagnetic flux variation without mechanical contact or discrete wire steps", "Because they operate at infinite voltage", "Because they use superconducting coils"],
                    "correct": 1,
                    "explanation": "Because magnetic flux coupling varies continuously as the non-contacting core moves, the sensor has no mechanical discrete steps, providing infinite resolution."
                },
                {
                    "question": "If core displacement is 4.0 mm and demodulated DC output is 3.4000 V, what is the sensitivity S_x?",
                    "options": ["0.4250 V/mm", "0.8500 V/mm", "1.7000 V/mm", "3.4000 V/mm"],
                    "correct": 1,
                    "explanation": "Sensitivity S_x = V_dc / x = 3.4000 V / 4.0 mm = 0.8500 V/mm."
                },
                {
                    "question": "Why is an AC carrier signal required to excite an LVDT rather than pure DC voltage?",
                    "options": ["DC would cause the core to melt", "Transformers operate exclusively on electromagnetic induction (Faraday's law), requiring time-varying magnetic flux", "AC current travels faster", "DC voltage is illegal in medical devices"],
                    "correct": 1,
                    "explanation": "Transformers require alternating current to generate time-varying magnetic flux (dΦ/dt) that induces voltage in secondary windings."
                }
            ],
            "settings": ["Transducer: Miniature medical LVDT (linear stroke ±10.0 mm)", "Carrier excitation: 2.500 kHz at 3.000 V RMS sinusoidal", "Demodulation: Synchronous phase-sensitive detector with 50 Hz low-pass filter"],
            "samples": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "📏", "label": "1. LVDT Micrometer Calibration Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Demodulated Voltage vs Core Stroke"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Inductive Coupling Sandbox"}
            ]
        },
        {
            "number": 8,
            "slug": "hall-effect-blood-flowmeter-electromagnetic-probe",
            "title": "Electromagnetic Blood Flowmeter Probe Calibration & Faraday Induction",
            "shortTitle": "Electromagnetic Blood Flowmeter",
            "aim": "Determine the induced transverse bio-potential across cannulated physiological saline flow under an applied transverse magnetic field and verify Faraday's law of induction.",
            "inputLabel": "Volumetric Flow Rate Q",
            "shortInput": "Flow Q",
            "inputUnit": "mL/min",
            "min": 50,
            "max": 300,
            "step": 50,
            "initial": 150,
            "inputDecimals": 0,
            "rawLabel": "Induced Transverse Potential V_i",
            "rawUnit": "μV",
            "rawDecimals": 2,
            "xAxis": "Volumetric flow rate Q (mL/min)",
            "yAxis": "Induced potential V_i (μV)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 175,
            "emptyY": 65,
            "targetName": "Flowmeter Induction Constant k_q",
            "target": "0.3600",
            "refValue": 0.3600,
            "resultUnit": "μV/(mL/min)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "V_i = k_q · Q = 0.3600 · Q",
            "intro": "In cardiovascular surgery, extracorporeal membrane oxygenation (ECMO), and organ perfusion hemodynamics, real-time continuous measurement of volumetric blood flow rate is essential for evaluating cardiac output and graft patency. Invented by Alexander Kolin in 1936, the electromagnetic blood flowmeter operates on the fundamental physical principle of Faraday's law of induction: when an electrically conductive fluid (such as blood containing dissociated Na⁺, K⁺, and Cl⁻ electrolytes) moves with mean velocity v through a transverse magnetic field of flux density B, moving ions experience Lorentz forces (F = q · (v × B)) that deflect positive and negative ions toward opposite vessel walls. This creates a transverse electric potential V_i perpendicular to both the flow velocity vector and magnetic field vector: V_i = B · d · v, where d is the inner lumen vessel diameter. Substituting volumetric flow rate Q = v · (π·d² / 4) yields a strictly linear relationship: V_i = [4·B / (π·d)] · Q = k_q · Q. To eliminate electrochemical DC half-cell offset drift, modern medical flowmeter probes utilize low-frequency square-wave or sinusoidal AC electromagnet excitation (typically 200 Hz to 400 Hz). In this experiment, a calibrated cannulated electromagnetic flow probe is tested with physiological saline across controlled volumetric flow rates to evaluate linear induction sensitivity k_q.",
            "modelExtra": "Evaluated using a 6.0 mm internal diameter cannulated flow probe with a 250 Hz square-wave AC magnetic excitation field (B = 0.050 Tesla). Perfusion fluid is physiological saline (0.9% NaCl, electrical conductivity 1.6 S/m) pumped from 50 to 300 mL/min.",
            "apparatus": [
                {"name": "Cannulated Electromagnetic Flow Probe (6 mm lumen)", "purpose": "Provides transverse electromagnet pole pieces and diametrically opposed platinum electrodes."},
                {"name": "Square-Wave AC Magnet Excitation Driver", "purpose": "Supplies regulated 250 Hz alternating current to electromagnet coils to eliminate DC polarization."},
                {"name": "Precision Peristaltic Physiological Perfusion Pump", "purpose": "Delivers calibrated, non-pulsatile volumetric saline flow rates from 50 to 300 mL/min."},
                {"name": "Synchronous Gated Demodulator & Preamplifier", "purpose": "Samples induced electrode potential during steady-state magnetic field plateaus."},
                {"name": "Precision Analytical Balance & Gravimetric Catch Reservoir", "purpose": "Verifies true volumetric flow rate by timed gravimetric mass collection (±0.1 mL/min)."},
                {"name": "Differential Bio-Potential Voltage Telemetry Console", "purpose": "Digitizes microvolt-level induced signals with 24-bit resolution and low-pass filtering."}
            ],
            "procedure": [
                {"title": "Fluid Circuit Priming and Zero Flow Balancing", "text": "Fill the flow loop with 0.9% physiological saline at 37.0 °C, purge all air bubbles from the probe lumen, stop pump, and adjust zero offset to 0.00 μV."},
                {"title": "Electromagnet AC Drive Stabilization", "text": "Energize probe electromagnet with 250 Hz square-wave excitation; verify magnetic flux density B = 0.050 T at center bore."},
                {"title": "Initial Flow Rate Standardization", "text": "Set perfusion pump to deliver steady 50 mL/min volumetric flow rate, verified via timed gravimetric collection on electronic balance."},
                {"title": "Induced Potential Sampling", "text": "Sample the synchronously gated microvolt potential V_i across platinum pickup electrodes over a 30-second integration window."},
                {"title": "Flow Progression Sequence", "text": "Increment pump delivery to 100, 150, 200, 250, and 300 mL/min, recording stabilized induced voltage V_i at each flow step."},
                {"title": "Induction Constant Regression Analysis", "text": "Plot induced voltage V_i against volumetric flow rate Q, computing the induction constant k_q via linear regression through the origin."}
            ],
            "topics": [
                {"question": "How does Faraday's law of induction apply to blood flow measurement?", "answer": "Blood is an electrical conductor containing dissociated electrolyte ions. When blood flows through an applied magnetic field B, the Lorentz force (F = q·[v × B]) pushes positive and negative ions to opposite sides of the vessel, generating an induced transverse voltage V = B·d·v directly proportional to flow velocity."},
                {"question": "Why is AC magnetic field excitation used instead of a static DC magnetic field?", "answer": "DC magnetic fields cause the platinum electrodes to suffer from huge, drifting electrochemical half-cell potentials and galvanic contact offsets that dwarf the microvolt flow signal. AC square-wave excitation alternates the signal polarity, allowing AC coupling and synchronous demodulation to completely reject DC drift."},
                {"question": "What is the 'transformer artifact' in electromagnetic flowmeters?", "answer": "Alternating current in the electromagnet generates time-varying magnetic flux (dΦ/dt) that induces an unwanted secondary transformer voltage in the loop formed by the pickup electrodes and lead wires. Sampling the signal only during the flat plateau of a square wave (where dB/dt = 0) eliminates this spike."},
                {"question": "Does blood hematocrit affect the calibration of an electromagnetic flowmeter?", "answer": "As long as blood electrical conductivity exceeds a minimum threshold (~0.1 S/m), the induced potential is strictly independent of fluid conductivity and hematocrit because the high amplifier input impedance draws virtually zero current."},
                {"question": "How does non-axisymmetric velocity profile affect measurement accuracy?", "answer": "According to Shercliff's weight function theory, if the magnetic field is uniform across a circular lumen, the induced potential reflects the true volume-averaged flow velocity regardless of whether the profile is laminar, parabolic, or turbulent."},
                {"question": "What is the difference between a cannulated flow probe and a perivascular cuff probe?", "answer": "A cannulated probe requires cutting the blood vessel and inserting the fluid through an internal rigid lumen (used in heart-lung bypass and ECMO), whereas a perivascular cuff snaps externally around the intact, pulsating blood vessel during surgical monitoring."}
            ],
            "precautions": [
                "Purge all microscopic air bubbles from the sensor lumen; air is an electrical insulator that open-circuits the electrode path.",
                "Ensure grounding of the fluid reservoir to avoid stray electrostatic charge buildup in plastic tubing.",
                "Verify that magnetic excitation frequency is locked to synchronous demodulator sampling gates.",
                "Maintain constant fluid temperature (37.0 °C) to stabilize electrolyte conductivity."
            ],
            "limitations": [
                "The linear induction model applies across non-turbulent and turbulent regimes up to 300 mL/min for the 6 mm probe.",
                "Assumes full lumen contact; partial filling or vessel collapse causes severe calibration errors.",
                "Requires minimum fluid electrical conductivity (> 0.05 S/m); cannot measure pure distilled water or non-conductive oils.",
                "Perivascular in-vivo applications can be affected by blood vessel wall thickness and non-conductive fat deposits."
            ],
            "quiz": [
                {
                    "question": "What fundamental physical law governs the operation of an electromagnetic blood flowmeter?",
                    "options": ["Coulomb's Law", "Faraday's Law of Electromagnetic Induction", "Hooke's Law", "Snell's Law of Refraction"],
                    "correct": 1,
                    "explanation": "Moving conductive blood through a magnetic field induces an electric potential according to Faraday's law: V = B · d · v."
                },
                {
                    "question": "Why do modern electromagnetic flowmeters use AC square-wave magnetic excitation instead of DC?",
                    "options": ["To lower electrical resistance of blood", "To eliminate large electrochemical DC electrode offset potentials through synchronous gating", "To make blood glow in the dark", "To accelerate blood flow velocity"],
                    "correct": 1,
                    "explanation": "AC square-wave excitation alternates signal polarity, allowing synchronous demodulation to completely reject drifting DC half-cell potentials."
                },
                {
                    "question": "If measured induced voltage is 72.00 μV at a volumetric flow rate of 200 mL/min, what is the induction constant k_q?",
                    "options": ["0.1800 μV/(mL/min)", "0.3600 μV/(mL/min)", "0.7200 μV/(mL/min)", "1.4400 μV/(mL/min)"],
                    "correct": 1,
                    "explanation": "k_q = V_i / Q = 72.00 μV / 200 mL/min = 0.3600 μV/(mL/min)."
                },
                {
                    "question": "What happens to the induced potential if an air bubble passes between the pickup electrodes?",
                    "options": ["Potential multiplies by 100", "Circuit opens, causing loss of signal and severe measurement artifact", "Magnetic field reverses", "Flowmeter switches to battery mode"],
                    "correct": 1,
                    "explanation": "Air is a dielectric insulator; an air bubble interrupts ionic conduction across the electrodes, causing immediate signal dropout."
                }
            ],
            "settings": ["Probe: 6.0 mm internal diameter cannulated flow head", "Excitation: 250 Hz square-wave AC (B = 0.050 T)", "Perfusion fluid: 0.9% physiological saline (conductivity 1.6 S/m)"],
            "samples": [50, 100, 150, 200, 250, 300],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🌊", "label": "1. Electromagnetic Flow Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Induced Voltage vs Flow"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Faraday Induction Sandbox"}
            ]
        }
    ]
