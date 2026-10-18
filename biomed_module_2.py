# -*- coding: utf-8 -*-
"""Biomedical Engineering Module 2: Physiological Signal Processing, Biosensing & Diagnostic Telemetry (Labs 9–17)."""

def get_module_2():
    return [
        {
            "number": 9,
            "slug": "ecg-einthoven-limb-leads-cardiac-axis",
            "title": "Einthoven Triangle Limb Leads & Mean Electrical Axis of the Heart",
            "shortTitle": "Einthoven ECG Vector Axis",
            "aim": "Synthesize Einthoven bipolar limb leads (I, II, III), verify Einthoven's law (Lead II = Lead I + Lead III), and calculate the frontal plane mean electrical cardiac axis from QRS complex vector amplitudes.",
            "inputLabel": "Lead I QRS Amplitude R_I",
            "shortInput": "Lead I R_I",
            "inputUnit": "mV",
            "min": 0.2,
            "max": 1.2,
            "step": 0.2,
            "initial": 0.6,
            "inputDecimals": 2,
            "rawLabel": "Lead II QRS Amplitude R_II",
            "rawUnit": "mV",
            "rawDecimals": 3,
            "xAxis": "Lead I QRS amplitude R_I (mV)",
            "yAxis": "Lead II QRS amplitude R_II (mV)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 0.7,
            "emptyY": 1.0,
            "targetName": "Cardiac Frontal Vector Ratio k_axis",
            "target": "1.2500",
            "refValue": 1.2500,
            "resultUnit": "ratio",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "R_II = k_axis · R_I + R_0 = 1.2500 · R_I + 0.1500",
            "intro": "The electrocardiogram (ECG) represents the spatial summation of electrical action potentials propagating through myocardial conduction pathways and ventricular muscle fibers during each cardiac cycle. Willem Einthoven in 1901 formalized the mathematical foundation of electrocardiology by conceptualizing the human torso as an equilateral triangle with the heart at the electrical center. By convention, bipolar limb leads measure potential differences between electrodes placed on the limbs: Lead I measures right arm to left arm (V_LA - V_RA), Lead II measures right arm to left leg (V_LL - V_RA), and Lead III measures left arm to left leg (V_LL - V_LA). Kirchoff's voltage law dictates Einthoven's fundamental triangle law: Lead II = Lead I + Lead III. During ventricular depolarization (QRS complex), the instantaneous spatial dipole vector can be projected onto the hexaxial frontal reference system to calculate the mean electrical cardiac axis (normally between -30° and +90°). Deviations from this normal axis provide crucial clinical diagnostic markers for left ventricular hypertrophy (left axis deviation), right ventricular strain, pulmonary embolism, and bundle branch conduction blocks. In this laboratory experiment, a multi-lead medical electrocardiograph is coupled to an anatomical thoracic cardiac vector phantom to record standard frontal limb leads, evaluate lead proportionality, and calculate the anatomical cardiac electrical axis.",
            "modelExtra": "Evaluated on an anatomical conductive torso phantom with calibrated dipole orientation (normal mean electrical axis θ = 51.3°). Linearized projection ratio between Lead I and Lead II is evaluated across QRS amplitudes from 0.2 mV to 1.2 mV.",
            "apparatus": [
                {"name": "Multi-Lead Diagnostic Clinical ECG Recorder", "purpose": "Provides 12-lead acquisition with 0.05 to 150 Hz diagnostic clinical frequency bandwidth."},
                {"name": "Anatomical Electrolytic Torso Vector Phantom", "purpose": "Saline-filled humanoid torso model featuring rotating central dipole generator."},
                {"name": "Programmable Cardiac Waveform Synthesizer", "purpose": "Generates standard P-QRS-T waveforms with calibrated dipole amplitudes and heart rates."},
                {"name": "Four-Limb Sintered Ag/AgCl Strap Electrodes", "purpose": "Captures RA, LA, LL, and RL biopotentials with < 2.0 kΩ contact impedance."},
                {"name": "Precision Active Right-Leg Drive Circuit", "purpose": "Suppresses 60 Hz common-mode mains interference by 40 dB via negative feedback."},
                {"name": "Biomedical Telemetry Vector Display Software", "purpose": "Computes instantaneous frontal plane vector loops and calculates numerical axis angle."}
            ],
            "procedure": [
                {"title": "Limb Lead Electrode Placement", "text": "Affix Ag/AgCl electrodes to standard phantom limb terminals: RA (Right Arm), LA (Left Arm), LL (Left Leg), and RL (Right Leg ground reference)."},
                {"title": "Phantom Dipole Axis Standardization", "text": "Set the internal dipole generator angle to standard anatomical normal orientation of +51.3° in the frontal plane."},
                {"title": "Einthoven's Law Verification", "text": "Record baseline resting traces; verify that instantaneous voltages satisfy Einthoven's law: V_II(t) = V_I(t) + V_III(t) at all points along the QRS."},
                {"title": "Initial QRS Amplitude Setting", "text": "Set cardiac synthesizer dipole strength to produce a Lead I QRS peak amplitude R_I of 0.20 mV; log stabilized Lead II amplitude R_II in millivolts."},
                {"title": "Dipole Amplitude Progression", "text": "Increment dipole strength so that Lead I reads 0.40, 0.60, 0.80, 1.00, and 1.20 mV, recording corresponding Lead II amplitudes."},
                {"title": "Vector Regression and Axis Calculation", "text": "Plot R_II versus R_I to determine vector ratio k_axis, calculating frontal plane axis angle θ = arctan[(2·R_II - R_I) / (√3 · R_I)]."}
            ],
            "topics": [
                {"question": "State Einthoven's triangle law and explain its theoretical physical basis.", "answer": "Einthoven's law states that Lead II = Lead I + Lead III. Because Lead I is (V_LA - V_RA), Lead III is (V_LL - V_LA), and Lead II is (V_LL - V_RA), adding Lead I and Lead III algebraically yields (V_LA - V_RA) + (V_LL - V_LA) = V_LL - V_RA, which identically equals Lead II by Kirchhoff's voltage law."},
                {"question": "What is the normal clinical range for the mean electrical cardiac axis in adults?", "answer": "The normal mean electrical axis in adults lies between -30° and +90° in the frontal plane. An axis between -30° and -90° indicates Left Axis Deviation (LAD), while an axis between +90° and +180° indicates Right Axis Deviation (RAD)."},
                {"question": "How are augmented unipolar limb leads (aVR, aVL, aVF) derived?", "answer": "Emmanuel Goldberger created augmented leads by disconnecting the explored limb from Wilson's central terminal, increasing signal amplitude by 50%. aVR explores the right arm, aVL explores the left arm, and aVF explores the foot (aVF = Lead II/2 + Lead III/2)."},
                {"question": "What physiological event corresponds to the QRS complex in the surface ECG?", "answer": "The QRS complex represents rapid electrical depolarization of the right and left ventricles through the His-Purkinje conduction system, initiating mechanical ventricular systole and pumping blood into the pulmonary artery and aorta."},
                {"question": "Why does left ventricular hypertrophy shift the electrical axis to the left?", "answer": "In left ventricular hypertrophy, the muscular wall of the left ventricle thickens substantially. More electrical dipoles are generated by the enlarged muscle mass, skewing the net vector toward the left and superiorly (producing Left Axis Deviation)."},
                {"question": "What is Wilson's Central Terminal (WCT) and what role does it serve?", "answer": "Wilson's central terminal connects the RA, LA, and LL electrodes through three equal 5.0 kΩ resistors to a common node. Because the sum of currents is zero, WCT provides a stable virtual electrical zero potential against which unipolar chest and augmented leads are referenced."}
            ],
            "precautions": [
                "Verify low electrode contact impedance (< 2 kΩ) across all four limbs to prevent differential unbalance noise.",
                "Ensure patient/phantom cables are bundled and shielded to suppress magnetic induction loops.",
                "Verify highpass filter is set to diagnostic bandwidth (0.05 Hz) to prevent ST-segment distortion and baseline tilt.",
                "Check that the Right Leg Drive circuit is engaged and active to suppress 60 Hz powerline hum."
            ],
            "limitations": [
                "The linear dipole model assumes an electrically homogeneous, isotropic volume conductor.",
                "Assumes a single lumped equivalent dipole; does not model complex localized multipole cardiac fields.",
                "Neglects respiratory baseline wander caused by diaphragm movement shifting the heart during breathing.",
                "Applies to the frontal plane projection; spatial orientation requires 3D vectorcardiography."
            ],
            "quiz": [
                {
                    "question": "According to Einthoven's triangle law, which equation is always strictly satisfied?",
                    "options": ["Lead I = Lead II + Lead III", "Lead II = Lead I + Lead III", "Lead III = Lead I + Lead II", "Lead II = Lead I · Lead III"],
                    "correct": 1,
                    "explanation": "Kirchhoff's voltage law applied to the limb potentials dictates that Lead II = Lead I + Lead III."
                },
                {
                    "question": "What is considered the normal range for the frontal plane mean electrical cardiac axis in an adult?",
                    "options": ["-90° to -180°", "-30° to +90°", "+120° to +180°", "+180° to +270°"],
                    "correct": 1,
                    "explanation": "In healthy adults, the normal frontal plane mean electrical QRS axis lies between -30° and +90°."
                },
                {
                    "question": "If Lead I amplitude is 0.80 mV and follows R_II = 1.2500 · R_I + 0.1500, what is the Lead II amplitude?",
                    "options": ["0.95 mV", "1.00 mV", "1.15 mV", "1.40 mV"],
                    "correct": 2,
                    "explanation": "R_II = 1.2500 · 0.80 + 0.1500 = 1.00 + 0.15 = 1.15 mV."
                },
                {
                    "question": "What is Wilson's Central Terminal (WCT) used for in clinical 12-lead ECG machines?",
                    "options": ["To power the battery", "To provide an average reference potential close to zero for unipolar leads", "To defibrillate the patient", "To measure body temperature"],
                    "correct": 1,
                    "explanation": "Wilson's Central Terminal sums the three limb potentials through equal resistors, creating a stable virtual zero reference."
                }
            ],
            "settings": ["ECG Bandwidth: 0.05 Hz to 150 Hz diagnostic standard", "Sampling rate: 500 Hz per channel (24-bit resolution)", "Dipole orientation: θ = 51.3° frontal normal axis"],
            "samples": [0.2, 0.4, 0.6, 0.8, 1.0, 1.2],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "❤️", "label": "1. Multi-Lead ECG Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Einthoven Frontal Vector Loop"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Cardiac Vector Axis Sandbox"}
            ]
        },
        {
            "number": 10,
            "slug": "photoplethysmography-ppg-pulse-oximeter-beer-lambert",
            "title": "Pulse Oximeter Dual-Wavelength PPG & Ratio-of-Ratios Calibration",
            "shortTitle": "Pulse Oximeter PPG Calibration",
            "aim": "Determine the ratio-of-ratios parameter R = (AC660/DC660) / (AC940/DC940) across blood oxygen saturations (SpO2) and calibrate the empirical calibration curve.",
            "inputLabel": "Ratio-of-Ratios Parameter R",
            "shortInput": "Ratio R",
            "inputUnit": "ratio",
            "min": 0.40,
            "max": 1.40,
            "step": 0.20,
            "initial": 0.80,
            "inputDecimals": 2,
            "rawLabel": "Arterial Oxygen Saturation SpO2",
            "rawUnit": "%",
            "rawDecimals": 2,
            "xAxis": "Ratio-of-ratios parameter R (ratio)",
            "yAxis": "Oxygen saturation SpO2 (%)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 0.90,
            "emptyY": 87.5,
            "targetName": "Oximeter Calibration Slope k_ox",
            "target": "25.0000",
            "refValue": 25.0000,
            "resultUnit": "%/ratio",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "SpO2 = -k_ox · R + SpO2,0 = -25.0000 · R + 110.0000",
            "intro": "Pulse oximetry is one of the most pervasive vital sign monitoring technologies in modern anesthesia, intensive care, and emergency medicine, enabling continuous, non-invasive assessment of arterial blood oxygenation. Invented by Takuo Aoyagi in 1974, pulse oximetry exploits the optical absorption differences between oxygenated hemoglobin (HbO2) and deoxygenated hemoglobin (RHb) based on the Beer-Lambert law. At red wavelengths (λ = 660 nm), deoxygenated hemoglobin absorbs significantly more light than HbO2; at near-infrared wavelengths (λ = 940 nm), HbO2 absorbs slightly more light than RHb, with an isobestic point occurring near 805 nm. By illuminating vascularized tissue (such as a fingertip or earlobe) with alternating red and infrared LEDs, a photodiode captures transmitted light. The signal is partitioned into a non-pulsatile DC component (representing static tissue, bone, and venous blood) and a pulsatile AC component (representing expanding arterial blood with each cardiac heartbeat). Normalizing AC by DC at each wavelength yields the dimensionless ratio-of-ratios: R = (AC_660 / DC_660) / (AC_940 / DC_940). Across clinical saturation ranges (75% to 100%), arterial oxygen saturation SpO2 relates linearly to R through the empirical calibration equation: SpO2 = -k_ox · R + 110.0. In this experiment, a calibrated dual-wavelength optical pulse oximeter probe is evaluated on an optical blood perfusion phantom to establish the calibration curve.",
            "modelExtra": "Evaluated using a clinical finger-clip probe with 660 nm red LED and 940 nm infrared LED paired with a low-noise silicon PIN photodiode. Calibrated across ratio-of-ratios R from 0.40 (SpO2 = 100%) to 1.40 (SpO2 = 75%) in 0.20 increments.",
            "apparatus": [
                {"name": "Clinical Finger-Clip Pulse Oximeter Probe", "purpose": "Provides dual-wavelength red (660 nm) and infrared (940 nm) LEDs and silicon PIN photodiode."},
                {"name": "Optical Tissue-Blood Perfusion Phantom", "purpose": "Calibrated optical phantom with variable pulsatile blood mimicking fluid and controlled oxygenation."},
                {"name": "Dual-Wavelength LED Multiplex Driver", "purpose": "Switches red and infrared LEDs alternately at 500 Hz with dark interval for ambient cancellation."},
                {"name": "Precision Co-Oximeter Blood Reference Analyzer", "purpose": "Measures true fractional oxygen saturation (SaO2) via multi-wavelength spectrophotometry."},
                {"name": "Photodiode Transimpedance Preamplifier & Demodulator", "purpose": "Separates 660 nm and 940 nm channels and splits each into filtered AC and DC analog signals."},
                {"name": "Digital Signal Processor Telemetry Console", "purpose": "Samples PPG signals, extracts pulse peak-to-peak amplitudes, and calculates modulation ratio R."}
            ],
            "procedure": [
                {"title": "Optical Alignment and Ambient Light Cancellation", "text": "Clip the sensor probe onto the optical phantom; verify that the ambient dark-period subtraction circuit eliminates background room light hum."},
                {"title": "LED Drive Current Standardization", "text": "Adjust LED drive currents so that baseline DC voltages on both red and infrared channels settle to equal 2.000 V levels."},
                {"title": "Full Oxygenation Baseline (R = 0.40)", "text": "Oxygenate blood phantom to 100.0% SaO2; record pulsatile AC and DC amplitudes, confirming ratio R = (AC660/DC660)/(AC940/DC940) = 0.400."},
                {"title": "Controlled Desaturation Step Progression", "text": "Deoxygenate the circulating phantom fluid in controlled steps to achieve parameter R values of 0.60, 0.80, 1.00, 1.20, and 1.40."},
                {"title": "Simultaneous Reference SpO2 Logging", "text": "Record gold-standard SaO2 from the bench co-oximeter and log corresponding SpO2 readings over 20 cardiac pulse cycles."},
                {"title": "Calibration Curve Regression Analysis", "text": "Plot SpO2 against modulation ratio R, fitting least-squares linear regression to determine calibration slope k_ox and intercept SpO2,0."}
            ],
            "topics": [
                {"question": "How does pulse oximetry isolate arterial blood from surrounding venous blood and tissue?", "answer": "Pulse oximetry utilizes the 'plethysmographic principle': only arterial blood volume pulses with each heartbeat. By dividing the pulsatile AC signal by the non-pulsatile DC background at each wavelength (AC/DC), the static absorption of bone, skin, muscle, and venous blood cancels completely, isolating the arterial blood optical properties."},
                {"question": "Why are 660 nm (red) and 940 nm (infrared) chosen as the two wavelengths?", "answer": "At 660 nm, deoxygenated hemoglobin has roughly ten times higher absorption than oxygenated hemoglobin. At 940 nm, the relationship flips and HbO2 absorbs more than RHb. This high contrast provides maximum sensitivity to changes in blood oxygen saturation."},
                {"question": "What is the isobestic wavelength in hemoglobin spectroscopy?", "answer": "An isobestic point is a wavelength where the extinction coefficients of oxygenated and deoxygenated hemoglobin are strictly identical (such as 805 nm). At an isobestic wavelength, light absorption is proportional to total hemoglobin concentration regardless of saturation."},
                {"question": "How do dyshemoglobins (carboxyhemoglobin and methemoglobin) cause erroneous pulse oximeter readings?", "answer": "Carboxyhemoglobin (COHb, carbon monoxide poisoning) absorbs light at 660 nm identically to HbO2, causing the pulse oximeter to falsely report near-100% saturation. Methemoglobin absorbs strongly at both 660 nm and 940 nm, driving the ratio R toward 1.0 (locking readings at a false 85%)."},
                {"question": "Why is pulse oximetry calibrated empirically on human volunteers rather than purely theoretically?", "answer": "The Beer-Lambert law assumes pure absorption in non-scattering media. Biological tissue causes massive multiple optical scattering, altering the effective photon optical pathlength; therefore, all commercial pulse oximeters rely on empirical calibration curves."},
                {"question": "What is the physiological significance of the oxyhemoglobin dissociation curve?", "answer": "The sigmoidal curve relates blood PO2 to Hb saturation. Because of its steep shape below 90% SpO2 (corresponding to PaO2 ≈ 60 mmHg), a small drop in partial pressure causes rapid, precipitous desaturation, making SpO2 an early warning indicator of impending hypoxemia."}
            ],
            "precautions": [
                "Shield the finger probe from direct surgical lights and sunlight to prevent photodiode saturation.",
                "Ensure steady phantom pulsatile flow; severe hypoperfusion reduces AC amplitude, dropping signal-to-noise ratio.",
                "Verify absence of dark-period optical crosstalk between interleaved red and infrared LED firings.",
                "Verify reference co-oximeter is calibrated with multi-wavelength certified hemolyzed blood standards."
            ],
            "limitations": [
                "The linear calibration model applies across the clinical diagnostic range (SpO2 75% to 100%).",
                "Fails to detect carbon monoxide poisoning (COHb) and methemoglobinemia (MetHb).",
                "Patient motion artifacts and severe peripheral vasoconstriction can cause false pulse readings or loss of tracking.",
                "Skin pigmentation (melanin) adds optical attenuation that can introduce small calibration offsets at low saturations."
            ],
            "quiz": [
                {
                    "question": "At which wavelength does deoxygenated hemoglobin (RHb) absorb significantly more light than oxygenated hemoglobin (HbO2)?",
                    "options": ["450 nm (blue)", "660 nm (red)", "940 nm (infrared)", "1310 nm (telecom)"],
                    "correct": 1,
                    "explanation": "At 660 nm red light, deoxygenated hemoglobin (RHb) has approximately 10 times higher optical extinction than oxygenated HbO2."
                },
                {
                    "question": "Why is the AC pulsatile component divided by the DC baseline component (AC/DC) in pulse oximetry?",
                    "options": ["To double the battery life", "To cancel out static light absorption from skin, bone, muscle, and venous blood", "To convert light into sound", "To filter out ECG electrical signals"],
                    "correct": 1,
                    "explanation": "Normalizing AC by DC isolates the expanding arterial blood pulse, eliminating the non-pulsatile absorption of background tissue."
                },
                {
                    "question": "If calibration ratio R is 0.80 and follows SpO2 = -25.0000 · R + 110.0000, what is the oxygen saturation?",
                    "options": ["85.0%", "90.0%", "95.0%", "98.0%"],
                    "correct": 1,
                    "explanation": "SpO2 = -25.0000 · 0.80 + 110.0000 = -20.0 + 110.0 = 90.0%."
                },
                {
                    "question": "What is the primary diagnostic hazard of standard two-wavelength pulse oximeters in carbon monoxide (CO) poisoning?",
                    "options": ["The screen turns black", "Carboxyhemoglobin absorbs like oxyhemoglobin at 660 nm, giving false normal (>95%) readings", "The sensor catches fire", "It reports zero pulse rate"],
                    "correct": 1,
                    "explanation": "Carboxyhemoglobin has optical absorption at 660 nm very similar to HbO2, causing the pulse oximeter to dangerously overestimate saturation."
                }
            ],
            "settings": ["Wavelengths: Red 660 nm / Infrared 940 nm LED pair", "Demodulation: Synchronous ambient dark-subtraction at 500 Hz", "Calibration target: SaO2 clinical co-oximeter reference"],
            "samples": [0.40, 0.60, 0.80, 1.00, 1.20, 1.40],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🩸", "label": "1. Pulse Oximeter Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Dual PPG Modulation Ratio"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Beer-Lambert Optical Sandbox"}
            ]
        },
        {
            "number": 11,
            "slug": "surface-electromyography-semg-muscle-fatigue-frequency",
            "title": "Surface Electromyography (sEMG) Root-Mean-Square & Muscle Fatigue Shift",
            "shortTitle": "sEMG Muscle Fatigue Spectral Shift",
            "aim": "Measure the median frequency shift and root-mean-square (RMS) amplitude of surface EMG signals during sustained isometric biceps brachii muscle contraction as a function of contraction duration.",
            "inputLabel": "Sustained Contraction Time t",
            "shortInput": "Time t",
            "inputUnit": "s",
            "min": 10,
            "max": 60,
            "step": 10,
            "initial": 30,
            "inputDecimals": 0,
            "rawLabel": "Power Spectrum Median Frequency MDF",
            "rawUnit": "Hz",
            "rawDecimals": 2,
            "xAxis": "Contraction time t (s)",
            "yAxis": "Median frequency MDF (Hz)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 35,
            "emptyY": 75,
            "targetName": "Spectral Fatigue Rate k_f",
            "target": "0.6500",
            "refValue": 0.6500,
            "resultUnit": "Hz/s",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "MDF = -k_f · t + MDF_0 = -0.6500 · t + 95.0000",
            "intro": "Surface electromyography (sEMG) records the spatial-temporal summation of motor unit action potential trains (MUAPTs) propagating along skeletal muscle sarcolemmas during voluntary muscle activation. In rehabilitation engineering, sports biomechanics, and ergonomic assessment, sEMG provides an objective non-invasive biomarker of localized muscle fatigue. When a muscle sustains a constant submaximal isometric contraction (e.g., holding 50% of maximum voluntary contraction, MVC), anaerobic metabolism leads to intramuscular lactic acid accumulation, intracellular H⁺ ion buildup, and extracellular K⁺ accumulation. These biochemical shifts impair sarcolemmal excitability and reduce the Muscle Fiber Conduction Velocity (MFCV) from approximately 4.5 m/s down to 2.5 m/s. Because the power spectral density (PSD) of the surface EMG signal scales proportionally with conduction velocity, muscle fatigue manifests as a progressive downward shift of the spectral energy toward lower frequencies. The median frequency (MDF)—the frequency that divides the power spectrum into two equal halves—exhibits a steady, linear decline across sustained contraction time t: MDF = -k_f · t + MDF_0. Concurrently, motor unit recruitment and synchronization increase, causing the root-mean-square (RMS) amplitude to rise. In this laboratory experiment, sEMG signals from the biceps brachii are analyzed via Fast Fourier Transform (FFT) during a 60-second isometric hold to evaluate the spectral fatigue rate k_f.",
            "modelExtra": "Evaluated on the biceps brachii of a healthy subject maintaining 50% MVC isometric forearm flexion against a load cell. Differential sEMG sampled at 2048 Hz (bandpass 20-450 Hz). Power spectral density calculated using 1024-point Hanning-windowed FFT epochs.",
            "apparatus": [
                {"name": "Bipolar Ag/AgCl Surface EMG Electrode Pair", "purpose": "Provides bar-electrode differential recording (20 mm inter-electrode spacing aligned with muscle fibers)."},
                {"name": "Precision Biomedical Biopotential Preamplifier", "purpose": "Amplifies microvolt myoelectric potentials (gain 1000, CMRR > 105 dB, input impedance 10 GΩ)."},
                {"name": "Electronic Isometric Dynamometer Arm Rig", "purpose": "Constrains forearm flexion at 90° and logs isometric force to maintain strict 50% MVC target."},
                {"name": "Precision Analog Bandpass Filter (20-450 Hz)", "purpose": "Eliminates motion artifacts (< 20 Hz) and prevents high-frequency aliasing (> 450 Hz)."},
                {"name": "16-Bit High-Speed Data Acquisition Card", "purpose": "Digitizes raw myoelectric waveforms at 2048 samples/second per channel."},
                {"name": "Real-Time Spectral Analysis Software Console", "purpose": "Computes instantaneous FFT power spectrum, RMS amplitude, and median frequency (MDF)."}
            ],
            "procedure": [
                {"title": "Skin Preparation and Electrode Alignment", "text": "Shave and abrade skin over the biceps brachii belly with alcohol; place bipolar electrodes parallel to fiber orientation with 20 mm inter-electrode distance."},
                {"title": "Maximum Voluntary Contraction (MVC) Calibration", "text": "Perform two 3-second maximal isometric contractions; record peak force to establish the 50% MVC target level."},
                {"title": "Sustained Isometric Hold Initiation", "text": "Instruct subject to maintain steady 50% MVC forearm flexion against the visual feedback load indicator for 60 seconds."},
                {"title": "Epoch Segmentation and FFT Processing", "text": "Segment raw sEMG into 1.0-second epochs and compute power spectral density (PSD) using 1024-point Hanning-windowed FFT."},
                {"title": "Median Frequency (MDF) Extraction", "text": "Extract MDF at 10, 20, 30, 40, 50, and 60 seconds by finding the frequency where cumulative power equals 50% of total spectral power."},
                {"title": "Fatigue Rate Regression Analysis", "text": "Plot MDF versus contraction time t, fitting linear regression to calculate the spectral fatigue rate k_f in Hz/s."}
            ],
            "topics": [
                {"question": "What is the physiological cause of the EMG spectral compression toward lower frequencies during muscle fatigue?", "answer": "During sustained isometric contraction, lactic acid and H⁺ ions accumulate, lowering intracellular pH, while K⁺ builds up in extracellular t-tubules. This impairs membrane excitability and slows Muscle Fiber Conduction Velocity (MFCV). Because the surface EMG power spectrum scales directly with conduction velocity, the entire spectrum compresses toward lower frequencies."},
                {"question": "How is the Median Frequency (MDF) defined mathematically?", "answer": "The median frequency MDF satisfies the integral equation: ∫[0 to MDF] P(f) df = ∫[MDF to ∞] P(f) df = 0.5 · ∫[0 to ∞] P(f) df, where P(f) is the power spectral density. It is less sensitive to noise and high-frequency harmonics than the mean frequency."},
                {"question": "Why does the Root-Mean-Square (RMS) amplitude of sEMG often increase during submaximal fatiguing contractions?", "answer": "As active motor units fatigue and produce less mechanical twitch force, the central nervous system compensates by recruiting additional motor units and increasing motor unit firing synchronization to maintain the target force, increasing the net electrical amplitude at the skin surface."},
                {"question": "Why must the highpass filter cutoff be set to at least 20 Hz in surface EMG recording?", "answer": "Electrode-skin contact motion artifacts and mechanical cable vibrations produce high-amplitude low-frequency noise predominantly between 0 and 15 Hz; a 20 Hz highpass filter strips these artifacts without losing significant myoelectric signal energy."},
                {"question": "What is the recommended inter-electrode distance (IED) under SENIAM guidelines?", "answer": "The Surface ElectroMyoGraphy for the Non-Invasive Assessment of Muscles (SENIAM) European project recommends an inter-electrode distance of 20 mm placed parallel to muscle fibers, halfway between the innervation zone and distal tendon."},
                {"question": "How does muscle fiber type (Type I vs Type II) influence the rate of spectral fatigue?", "answer": "Fast-twitch glycolytic fibers (Type II) have higher conduction velocities and higher baseline median frequencies, but fatigue rapidly due to anaerobic glycogen depletion, producing steeper MDF decline slopes than fatigue-resistant slow-twitch oxidative fibers (Type I)."}
            ],
            "precautions": [
                "Align electrodes strictly parallel to the longitudinal axis of muscle fibers to prevent spatial filtering distortion.",
                "Ensure subject maintains strictly constant isometric force; force fluctuations alter motor unit recruitment.",
                "Avoid placing electrodes over the muscle motor point (innervation zone) where bidirectional action potentials collide.",
                "Allow at least 15 minutes of rest between trials to ensure full metabolic clearance of muscle metabolites."
            ],
            "limitations": [
                "The linear spectral decline model applies during constant-force isometric contractions (10 s to 60 s).",
                "Does not model dynamic contractions (concentric/eccentric) where muscle geometry shifts under electrodes.",
                "Skin subcutaneous fat thickness attenuates high frequencies, acting as an anatomical spatial lowpass filter.",
                "Crosstalk from adjacent synergist muscles (brachialis, coracobrachialis) can contaminate the detected signal."
            ],
            "quiz": [
                {
                    "question": "What happens to the median frequency (MDF) of an sEMG signal during sustained fatiguing isometric contraction?",
                    "options": ["It increases exponentially", "It shifts downward toward lower frequencies due to decreased muscle fiber conduction velocity", "It remains strictly constant at 60 Hz", "It oscillates randomly between 1000 Hz and 2000 Hz"],
                    "correct": 1,
                    "explanation": "Accumulation of metabolites (H+, lactic acid) slows muscle fiber conduction velocity, causing the power spectrum and MDF to shift downward."
                },
                {
                    "question": "What is the definition of the Median Frequency (MDF) of a power spectrum?",
                    "options": ["The peak amplitude of the spectrum", "The frequency that divides the total power spectrum area into two equal halves", "The frequency of the 60 Hz notch filter", "The highest frequency recorded"],
                    "correct": 1,
                    "explanation": "MDF is the exact frequency at which 50% of the total spectral power lies below it and 50% lies above it."
                },
                {
                    "question": "If MDF is 88.50 Hz at t = 10 s and 69.00 Hz at t = 40 s, what is the spectral fatigue rate k_f?",
                    "options": ["0.3250 Hz/s", "0.6500 Hz/s", "1.3000 Hz/s", "2.6000 Hz/s"],
                    "correct": 1,
                    "explanation": "Fatigue rate k_f = -(69.00 - 88.50) Hz / (40 - 10) s = 19.50 / 30 = 0.6500 Hz/s."
                },
                {
                    "question": "According to international SENIAM guidelines, what is the recommended inter-electrode distance for surface EMG?",
                    "options": ["2 mm", "20 mm", "100 mm", "200 mm"],
                    "correct": 1,
                    "explanation": "SENIAM guidelines specify a 20 mm center-to-center inter-electrode distance for bipolar surface EMG."
                }
            ],
            "settings": ["Muscle: Biceps brachii (isometric 50% MVC flexion)", "Electrode spacing: 20 mm bipolar Ag/AgCl parallel to fibers", "Sampling & Filter: 2048 Hz sampling, 20-450 Hz bandpass"],
            "samples": [10, 20, 30, 40, 50, 60],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💪", "label": "1. sEMG Dynamometer Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Power Spectrum FFT Shift"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Muscle Conduction Sandbox"}
            ]
        },
        {
            "number": 12,
            "slug": "electroencephalography-eeg-alpha-attenuation-power",
            "title": "EEG Spectral Power Density & Berger Alpha-Wave Attenuation",
            "shortTitle": "EEG Alpha Wave Spectral Power",
            "aim": "Quantify the reduction in occipital 8–12 Hz alpha-band spectral power during eye-opening (Berger effect) and determine visual sensory attenuation ratio using Fast Fourier Transform (FFT).",
            "inputLabel": "Ambient Visual Illuminance E_v",
            "shortInput": "Light E_v",
            "inputUnit": "lux",
            "min": 50,
            "max": 300,
            "step": 50,
            "initial": 150,
            "inputDecimals": 0,
            "rawLabel": "Alpha Band Peak Power P_alpha",
            "rawUnit": "μV²/Hz",
            "rawDecimals": 3,
            "xAxis": "Illuminance E_v (lux)",
            "yAxis": "Alpha band power P_alpha (μV²/Hz)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 175,
            "emptyY": 30,
            "targetName": "Photopic Attenuation Gradient k_alpha",
            "target": "0.1250",
            "refValue": 0.1250,
            "resultUnit": "(μV²/Hz)/lux",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "P_alpha = -k_alpha · E_v + P_0 = -0.1250 · E_v + 52.0000",
            "intro": "Electroencephalography (EEG) records continuous postsynaptic potential fluctuations generated by pyramidal neurons in the cerebral cortex. Discovered by Hans Berger in 1929, the dominant rhythm of the relaxed, awake human brain with eyes closed is the alpha rhythm (8 to 12 Hz, amplitude 20 to 80 μV), most prominent over occipital and parietal electrode sites (O1, O2, Pz). Alpha oscillations originate from synchronized reciprocal thalamocortical reverberating loops that reflect a sensory idling or gating state of visual cortices. When an individual opens their eyes or engages in focused visual-spatial problem solving, visual photic input via the optic nerve and lateral geniculate nucleus desynchronizes these thalamocortical networks—a phenomenon known as the 'Berger effect' or alpha desynchronization (alpha blocking). In neuroengineering, brain-computer interfaces (BCIs), and cognitive ergonomics, the attenuation of alpha power serves as a quantifiable metric of cortical sensory processing and mental workload. Across increasing ambient visual illuminance E_v, occipital alpha spectral power density P_alpha declines in a predictable linear relationship: P_alpha = -k_alpha · E_v + P_0. In this experiment, occipital EEG signals recorded using the International 10-20 system are digitized to analyze alpha band spectral power attenuation across calibrated photopic illumination levels.",
            "modelExtra": "Evaluated using occipital lead O1 referenced to linked mastoids (A1+A2) on a healthy awake volunteer inside a sound-attenuated Faraday room. EEG bandpass filtered from 0.5 to 35 Hz and sampled at 512 Hz. Alpha peak power (8-12 Hz) extracted via 1024-point FFT Welch periodogram.",
            "apparatus": [
                {"name": "Clinical Research EEG Headbox & Cap", "purpose": "International 10-20 sintered Ag/AgCl multi-channel electrode array with active shielding."},
                {"name": "Ultra-Low-Noise 24-Bit EEG Amplifier", "purpose": "Provides < 0.3 μV RMS input noise with 100 MΩ differential input impedance and optical isolation."},
                {"name": "Calibrated Full-Spectrum Photopic Light Source", "purpose": "Delivers uniform ambient room illuminance from 50 to 300 lux with DC regulation (flicker-free)."},
                {"name": "Precision Cosine-Corrected Digital Luxmeter", "purpose": "Measures ambient eye-level illuminance with 0.1 lux accuracy traceable to NIST."},
                {"name": "Acoustically Isolated Faraday Shielding Chamber", "purpose": "Eliminates auditory distraction and suppresses 60 Hz electrostatic line pickup."},
                {"name": "Real-Time EEG Power Spectral Analysis Console", "purpose": "Computes instantaneous Welch periodograms and integrates 8-12 Hz alpha band power."}
            ],
            "procedure": [
                {"title": "Electrode Montage and Impedance Calibration", "text": "Position Ag/AgCl electrodes at O1, O2, Cz, and linked earlobe references (A1, A2); verify all contact impedances are under 3.0 kΩ."},
                {"title": "Dark-Adapted Closed-Eye Baseline", "text": "Record 60 seconds of resting EEG with eyes closed in darkness; verify presence of synchronized 10.0 Hz occipital alpha rhythm."},
                {"title": "Illuminance Step Standardization", "text": "Instruct subject to open eyes and gaze at a neutral fixation cross; set photopic illuminance to initial test level of 50 lux."},
                {"title": "Alpha Spectral Power Density Acquisition", "text": "Record 30 seconds of artifact-free EEG; compute average power spectral density in the 8-12 Hz band (P_alpha in μV²/Hz)."},
                {"title": "Illuminance Progression Sequence", "text": "Stepwise increment ambient light through 100, 150, 200, 250, and 300 lux, allowing 60 seconds for visual adaptation before logging P_alpha."},
                {"title": "Attenuation Regression Analysis", "text": "Plot alpha band power P_alpha against illuminance E_v, performing least-squares linear regression to determine the photopic attenuation gradient k_alpha."}
            ],
            "topics": [
                {"question": "What is the Berger effect (alpha blocking) in neurophysiology?", "answer": "The Berger effect is the immediate desynchronization and reduction in amplitude of the 8–12 Hz occipital alpha rhythm when a relaxed subject opens their eyes or directs active attention to visual stimuli, transitioning the cortex from synchronized idling to active desynchronized processing."},
                {"question": "What neural structures generate the occipital alpha rhythm?", "answer": "Alpha oscillations are generated by reciprocal resonant loops between thalamic relay neurons (lateral geniculate nucleus and pulvinar) and cortical pyramidal neurons in visual areas (Brodmann areas 17, 18, 19). Thalamic pacemakers drive the rhythmic synchrony."},
                {"question": "What are the four primary frequency bands in clinical human EEG?", "answer": "Delta (0.5 to 4 Hz, deep slow-wave sleep, pathology), Theta (4 to 8 Hz, drowsiness, memory encoding), Alpha (8 to 12 Hz, relaxed wakefulness with eyes closed), and Beta (13 to 30 Hz, active thinking, motor planning, alertness). Gamma (> 30 Hz) reflects cross-modal binding."},
                {"question": "What is the International 10-20 System for electrode placement?", "answer": "The 10-20 system is an internationally standardized method to place EEG electrodes based on anatomical landmarks (nasion, inion, and preauricular points). Electrode spacings are placed at intervals of 10% or 20% of the total skull contour distances, ensuring reproducible anatomical coverage."},
                {"question": "Why are ocular electrooculogram (EOG) artifacts so prominent in frontal EEG leads?", "answer": "The human eyeball behaves as a permanent electrical dipole (+6 mV cornea relative to retina). Blinking and saccadic eye movements rotate this dipole, inducing massive (100 to 400 μV) artifact potentials that propagate into frontal EEG channels (Fp1, Fp2)."},
                {"question": "How do Brain-Computer Interfaces (BCIs) utilize alpha rhythms?", "answer": "BCIs use changes in alpha power (such as sensorimotor mu-rhythms over C3/C4 during motor imagery, or occipital alpha during visual attention) as voluntary control signals to operate computer cursors, communication spellers, or neuro-prosthetic robotic hands."}
            ],
            "precautions": [
                "Instruct the subject to refrain from blinking or clenching their jaw during the 30-second EEG data recording epochs.",
                "Ensure all electrode contact impedances are balanced and strictly under 3.0 kΩ to prevent noise unbalance.",
                "Use ripple-free DC power for lighting; standard AC fluorescent lamps induce 120 Hz optical flicker artifacts.",
                "Enclose the recording station in a Faraday cage to eliminate 60 Hz mains interference."
            ],
            "limitations": [
                "The linear attenuation model applies across photopic ambient light levels (50 to 300 lux).",
                "Assumes calm, non-anxious subject; psychological anxiety or arousal can suppress alpha rhythm independently of light.",
                "Approximately 5% to 10% of the healthy human population naturally produces little to no surface-recordable alpha rhythm.",
                "Subject to drowsiness effects: onset of sleep transitions the alpha rhythm into slower theta frequencies."
            ],
            "quiz": [
                {
                    "question": "What frequency band defines the classical human alpha rhythm in EEG?",
                    "options": ["0.5 to 4 Hz", "4 to 8 Hz", "8 to 12 Hz", "15 to 30 Hz"],
                    "correct": 2,
                    "explanation": "The human alpha rhythm is defined as sinusoidal oscillatory activity within the 8 to 12 Hz band."
                },
                {
                    "question": "What occurs to occipital alpha waves when an individual opens their eyes (Berger effect)?",
                    "options": ["Alpha waves quadruple in amplitude", "Alpha waves desynchronize and attenuate significantly in amplitude", "Frequency drops to 1 Hz", "The brain stops producing electrical signals"],
                    "correct": 1,
                    "explanation": "Visual input desynchronizes the underlying thalamocortical networks, dramatically attenuating alpha band power (alpha blocking)."
                },
                {
                    "question": "If alpha power is 39.50 μV²/Hz at 100 lux and 27.00 μV²/Hz at 200 lux, what is the attenuation gradient k_alpha?",
                    "options": ["0.0625 (μV²/Hz)/lux", "0.1250 (μV²/Hz)/lux", "0.2500 (μV²/Hz)/lux", "0.5000 (μV²/Hz)/lux"],
                    "correct": 1,
                    "explanation": "k_alpha = -(27.00 - 39.50) / (200 - 100) = 12.50 / 100 = 0.1250 (μV²/Hz)/lux."
                },
                {
                    "question": "Over which anatomical region of the cerebral cortex is the alpha rhythm most prominent?",
                    "options": ["Frontal cortex", "Temporal cortex", "Occipital cortex (O1, O2)", "Motor strip"],
                    "correct": 2,
                    "explanation": "The alpha rhythm is strongest over the visual processing areas of the occipital and parietal cortices."
                }
            ],
            "settings": ["Lead configuration: Occipital O1 referenced to linked mastoids (A1+A2)", "Sampling rate: 512 Hz (bandpass 0.5 to 35 Hz)", "Analysis window: 1024-point FFT Welch periodogram with 50% overlap"],
            "samples": [50, 100, 150, 200, 250, 300],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🧠", "label": "1. EEG Acquisition Stand"},
                {"id": "compare", "icon": "📊", "label": "2. Alpha Spectrum vs Light"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Thalamocortical Sandbox"}
            ]
        },
        {
            "number": 13,
            "slug": "galvanic-skin-response-gsr-electrodermal-activity",
            "title": "Galvanic Skin Response (GSR) & Sympathetic Electrodermal Conductance",
            "shortTitle": "Galvanic Skin Conductance",
            "aim": "Measure skin conductance level (SCL) and phasic skin conductance responses (SCR) across calibrated psychological arousal stimuli using constant-voltage DC bridge circuitry.",
            "inputLabel": "Stimulus Arousal Intensity I_stim",
            "shortInput": "Arousal I",
            "inputUnit": "units",
            "min": 1.0,
            "max": 6.0,
            "step": 1.0,
            "initial": 3.0,
            "inputDecimals": 1,
            "rawLabel": "Phasic Conductance Change ΔG",
            "rawUnit": "μS",
            "rawDecimals": 3,
            "xAxis": "Stimulus intensity index (units)",
            "yAxis": "Phasic skin conductance ΔG (μS)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.5,
            "emptyY": 6.5,
            "targetName": "Electrodermal Arousal Sensitivity k_g",
            "target": "1.8500",
            "refValue": 1.8500,
            "resultUnit": "μS/unit",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ΔG = k_g · I_stim = 1.8500 · I_stim",
            "intro": "Electrodermal activity (EDA), historically termed the Galvanic Skin Response (GSR), provides a sensitive, involuntary peripheral biomarker of sympathetic autonomic nervous system arousal. Innervated exclusively by postganglionic sympathetic sudomotor nerve fibers releasing acetylcholine, human eccrine sweat glands (densely concentrated on the palmar surfaces of the hands and plantar surfaces of the feet) fill with sweat in response to emotional, cognitive, and sensory stimuli. Because sweat is an electrolyte solution rich in NaCl, sweat filling the non-conductive pores of the stratum corneum creates parallel electrical conductance pathways that dramatically lower the electrical resistance of the skin. In modern psychophysiology and lie detection (polygraphy), endosomatic and exosomatic recording techniques are employed. Under the standard Lykken exosomatic method, a constant regulated DC voltage (typically 0.50 V) is applied across two Ag/AgCl finger electrodes, and the resulting current is measured to evaluate skin conductance G (expressed in microsiemens, μS). The signal decomposes into a slowly varying tonic baseline (Skin Conductance Level, SCL) and fast, transient phasic peaks (Skin Conductance Responses, SCR) that occur 1 to 3 seconds following a stimulus. Across standardized sensory stimulus intensities I_stim, the peak phasic conductance amplitude ΔG exhibits direct linear proportionality: ΔG = k_g · I_stim. In this experiment, an instrumented GSR constant-voltage circuit evaluates palmar skin conductance during calibrated arousal tasks.",
            "modelExtra": "Evaluated using two un-gelled Ag/AgCl palmar finger electrodes on the distal phalanges of the index and middle fingers with constant 0.500 V DC excitation. Phasic conductance response ΔG is evaluated across calibrated acoustic startle stimulus intensities from 1.0 to 6.0 arbitrary arousal units.",
            "apparatus": [
                {"name": "Constant-Voltage Exosomatic EDA Circuit", "purpose": "Applies strictly constant 0.500 V DC across electrodes and converts current to voltage (1.0 V / 10 μS)."},
                {"name": "Ag/AgCl Dry Palmar Finger Band Electrodes", "purpose": "Constructed with 1.0 cm² Ag/AgCl contact plates without gel to avoid artificial skin hydration."},
                {"name": "Calibrated Acoustic Startle Stimulator", "purpose": "Delivers calibrated white-noise acoustic tone bursts across six standardized intensity levels."},
                {"name": "Isolated Low-Noise Biomedical DAQ Unit", "purpose": "Samples conductance waveforms with 24-bit resolution and optical isolation compliant with IEC 60601-1."},
                {"name": "Digital Ambient Temperature & Humidity Monitor", "purpose": "Logs room ambient conditions (22.0 °C, 45% RH) to verify stable baseline perspiration."},
                {"name": "EDA Peak Detection Software Analyzer", "purpose": "Extracts tonic SCL baseline, peak SCR latency, and phasic amplitude ΔG in microsiemens."}
            ],
            "procedure": [
                {"title": "Electrode Placement and Baseline Acclimation", "text": "Attach Ag/AgCl electrodes to the palmar surface of the distal phalanges of fingers II and III; allow 10 minutes for baseline thermal acclimation."},
                {"title": "Constant-Voltage Excitation Verification", "text": "Verify with precision DMM that circuit applies exactly 0.500 V DC across the finger electrodes without voltage droop."},
                {"title": "Tonic Skin Conductance Level (SCL) Logging", "text": "Record resting tonic conductance for 2 minutes to confirm a stable baseline (typically 2.0 to 10.0 μS) and absence of spontaneous spikes."},
                {"title": "Calibrated Stimulus Delivery (Intensity 1.0)", "text": "Deliver the initial acoustic stimulus (Level 1.0); identify the phasic SCR wave occurring 1.5 to 2.5 seconds post-stimulus."},
                {"title": "Phasic Amplitude ΔG Measurement", "text": "Compute peak phasic conductance increase ΔG = G_peak - G_onset in microsiemens (μS)."},
                {"title": "Arousal Progression Sequence", "text": "Deliver stimuli of intensities 2.0, 3.0, 4.0, 5.0, and 6.0 at randomized 45-second intervals, plotting ΔG against stimulus level to determine k_g."}
            ],
            "topics": [
                {"question": "What is the physiological mechanism responsible for changes in skin conductance?",
                "answer": "Sympathetic cholinergic nerves stimulate eccrine sweat glands to secrete sweat (a conductive saline solution). As sweat rises into sweat ducts toward the skin surface, it creates low-resistance parallel ionic conduction paths through the insulating stratum corneum, increasing overall skin conductance."},
                {"question": "Why is a constant voltage of 0.50 V used rather than a higher voltage?", "answer": "Voltages above 0.8 to 1.0 V cause non-linear electrical breakdown of cell membranes in the stratum corneum (electroporation) and induce sweat gland damage and polarization overpotentials. A low 0.50 V potential ensures strictly linear ohmic current flow."},
                {"question": "What is the difference between tonic and phasic electrodermal activity?", "answer": "Tonic activity (Skin Conductance Level, SCL) is the slow, continuous baseline conductance that changes over minutes reflecting general arousal or body temperature. Phasic activity (Skin Conductance Response, SCR) refers to rapid, transient spikes occurring 1 to 3 seconds after specific emotional or sensory stimuli."},
                {"question": "Why are palmar and plantar skin sites preferred for GSR recording?", "answer": "The palms and soles have the highest density of eccrine sweat glands in the human body (> 600 glands/cm²) and are primarily responsive to psychological, cognitive, and emotional stimuli rather than thermal regulation."},
                {"question": "What is the typical latency of a skin conductance response following a stimulus?", "answer": "The physiological latency is approximately 1.0 to 3.0 seconds, caused by the time required for sympathetic unmyelinated C-fibers to conduct action potentials to the glands, followed by sweat secretion and duct filling."},
                {"question": "How does sweat gland habituation affect repetitive GSR trials?", "answer": "Repetitive exposure to the same stimulus causes psychological habituation; sympathetic nervous discharge decreases, and subsequent SCR amplitudes diminish unless stimulus intensity is altered or rest intervals are provided."}
            ],
            "precautions": [
                "Instruct the subject to keep hand completely relaxed and motionless; finger twitches create mechanical motion artifacts.",
                "Maintain randomized inter-stimulus intervals (> 30 s) to prevent sensory anticipation and habituation.",
                "Do not use abrasive skin preps or alcohol swabs; skin abrasion destroys the natural stratum corneum barrier.",
                "Ensure ambient room temperature is kept at thermoneutral levels (21-23 °C) to avoid thermoregulatory sweating."
            ],
            "limitations": [
                "The linear arousal model applies across sub-saturation sensory intensities (1.0 to 6.0 units).",
                "Assumes normal sympathetic autonomic function; peripheral neuropathies (e.g., in diabetes) abolish SCR.",
                "Does not differentiate between positive arousal (excitement) and negative arousal (fear/stress); both increase GSR.",
                "Varies widely between individuals based on basal sweat gland density and skin hydration state."
            ],
            "quiz": [
                {
                    "question": "Which division of the human nervous system controls eccrine sweat gland secretion in the palms?",
                    "options": ["Somatic motor nervous system", "Sympathetic autonomic nervous system", "Parasympathetic nervous system", "Enteric nervous system"],
                    "correct": 1,
                    "explanation": "Palmar eccrine sweat glands are innervated solely by postganglionic sympathetic fibers responsive to emotional arousal."
                },
                {
                    "question": "What standard unit of electrical conductance is used in modern electrodermal recordings?",
                    "options": ["Ohms (Ω)", "Volts (V)", "Microsiemens (μS)", "Coulombs (C)"],
                    "correct": 2,
                    "explanation": "Skin conductance is the reciprocal of resistance (G = 1/R) and is measured in microsiemens (μS) or micromhos."
                },
                {
                    "question": "If stimulus intensity is 4.0 units and phasic response ΔG is 7.400 μS, what is the arousal sensitivity k_g?",
                    "options": ["0.9250 μS/unit", "1.8500 μS/unit", "3.7000 μS/unit", "7.4000 μS/unit"],
                    "correct": 1,
                    "explanation": "Sensitivity k_g = ΔG / I_stim = 7.400 μS / 4.0 units = 1.8500 μS/unit."
                },
                {
                    "question": "What is the typical physiological latency between a sudden stimulus and the onset of an SCR peak?",
                    "options": ["10 milliseconds", "1 to 3 seconds", "30 to 60 seconds", "5 minutes"],
                    "correct": 1,
                    "explanation": "Due to slow unmyelinated C-fiber conduction and sweat gland fluid filling, SCR latency is typically 1 to 3 seconds."
                }
            ],
            "settings": ["Excitation: 0.500 V DC constant potential across finger electrodes", "Electrode site: Palmar distal phalanges of index and middle fingers", "Room conditions: 22.0 °C, 45% relative humidity"],
            "samples": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "✋", "label": "1. GSR Polygraph Test Stand"},
                {"id": "compare", "icon": "📊", "label": "2. Phasic SCR vs Stimulus"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Sympathetic Sudomotor Sandbox"}
            ]
        },
        {
            "number": 14,
            "slug": "amperometric-glucose-biosensor-michaelis-menten",
            "title": "Enzymatic Amperometric Glucose Biosensor Kinetics & Linearity",
            "shortTitle": "Glucose Biosensor Amperometry",
            "aim": "Evaluate the steady-state catalytic current of a glucose oxidase (GOx) platinum-carbon amperometric electrode across blood glucose concentrations to evaluate sensor sensitivity and linear dynamic range.",
            "inputLabel": "Glucose Concentration C_glu",
            "shortInput": "Glucose C",
            "inputUnit": "mmol/L",
            "min": 2.0,
            "max": 12.0,
            "step": 2.0,
            "initial": 6.0,
            "inputDecimals": 1,
            "rawLabel": "Catalytic Oxidation Current I_a",
            "rawUnit": "μA",
            "rawDecimals": 3,
            "xAxis": "Glucose concentration C_glu (mmol/L)",
            "yAxis": "Catalytic current I_a (μA)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 7.0,
            "emptyY": 5.0,
            "targetName": "Biosensor Amperometric Sensitivity S_glu",
            "target": "0.7200",
            "refValue": 0.7200,
            "resultUnit": "μA/(mmol/L)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "I_a = S_glu · C_glu = 0.7200 · C_glu",
            "intro": "In diabetes management and point-of-care clinical diagnostics, enzymatic electrochemical biosensors represent the most widespread commercial medical biosensing technology in the world, utilized daily by millions of diabetic patients in personal glucometers and continuous glucose monitors (CGMs). The classic first-generation glucose biosensor couples the biocatalytic enzyme Glucose Oxidase (GOx, immobilized in a glutaraldehyde or chitosan membrane matrix) with an amperometric platinum working electrode. GOx catalyzes the oxidation of β-D-glucose by dissolved molecular oxygen to produce D-glucono-1,5-lactone and hydrogen peroxide: Glucose + O2 + H2O —[GOx]→ Gluconic Acid + H2O2. The generated hydrogen peroxide diffuses to the polarized platinum anode (held at +0.65 V versus Ag/AgCl), where it undergoes stoichiometric electrocatalytic oxidation: H2O2 → O2 + 2 H⁺ + 2 e⁻. Each mole of glucose consumed transfers two electrons to the electrode. In accordance with Michaelis-Menten enzyme kinetics, when the substrate concentration C_glu is well below the apparent Michaelis constant (C_glu << K_m,app), the rate of enzymatic turnover is first-order, and the resulting steady-state anodic current I_a is directly proportional to glucose concentration: I_a = S_glu · C_glu. In this laboratory experiment, a screen-printed platinum-carbon GOx biosensor is tested in physiological buffer across clinical glycemic levels (2.0 to 12.0 mmol/L) to evaluate linear sensitivity S_glu.",
            "modelExtra": "Evaluated using a screen-printed three-electrode sensor (platinum working electrode, Ag/AgCl reference, carbon counter) polarized at +0.650 V in PBS buffer (pH 7.4, 37.0 °C). Evaluated across clinical normo- and hyperglycemic concentrations (2.0 to 12.0 mmol/L).",
            "apparatus": [
                {"name": "Screen-Printed GOx Platinum Biosensor Strip", "purpose": "Working electrode with immobilized glucose oxidase and permselective polyurethane outer membrane."},
                {"name": "Precision Analytical Electrochemical Potentiostat", "purpose": "Applies constant +0.650 V anodic polarizing potential and records microampere currents."},
                {"name": "Stirred Water-Jacketed Electrochemical Cell", "purpose": "Maintains reaction buffer at 37.00 ± 0.05 °C with constant 250 RPM magnetic stirring."},
                {"name": "Calibrated Micropipette Set (10-1000 μL)", "purpose": "Dispenses calibrated standard glucose stock solution aliquots into the reaction cell."},
                {"name": "Certified Glucose Standard Reference Solutions", "purpose": "Traceable 100 mmol/L β-D-glucose stock solution in saturated benzoic acid preservative."},
                {"name": "Low-Noise Electrometer Data Logging Console", "purpose": "Digitizes anodic oxidation current at 10 Hz with 1.0 nA measurement precision."}
            ],
            "procedure": [
                {"title": "Electrochemical Cell Conditioning", "text": "Fill the glass cell with 10.0 mL of phosphate-buffered saline (PBS, pH 7.4) at 37.0 °C; insert the three-electrode sensor strip and start magnetic stirring at 250 RPM."},
                {"title": "Polarization and Background Current Decay", "text": "Apply +0.650 V polarizing potential to the platinum working electrode; wait 10 minutes until background capacitive current stabilizes (< 0.05 μA)."},
                {"title": "Initial Glucose Step Injection (2.0 mmol/L)", "text": "Inject calibrated volume of glucose stock to achieve 2.0 mmol/L (36 mg/dL); allow 30 seconds for enzymatic steady-state current plateau."},
                {"title": "Catalytic Current Logging", "text": "Record steady-state anodic oxidation current I_a in microamperes over a 15-second integration window."},
                {"title": "Concentration Progression Sequence", "text": "Perform sequential spiked standard additions to achieve 4.0, 6.0, 8.0, 10.0, and 12.0 mmol/L (up to severe hyperglycemia ~216 mg/dL), logging I_a at each step."},
                {"title": "Sensitivity Regression and Linearity Verification", "text": "Plot catalytic current I_a against glucose concentration C_glu, performing linear regression through zero to determine biosensor sensitivity S_glu."}
            ],
            "topics": [
                {"question": "What is the biochemical reaction catalyzed by Glucose Oxidase (GOx)?", "answer": "Glucose oxidase contains flavin adenine dinucleotide (FAD) cofactors and catalyzes: β-D-glucose + O2 + H2O → D-gluconic acid + H2O2. FAD is reduced to FADH2 by glucose and subsequently re-oxidized by oxygen to regenerate the active enzyme."},
                {"question": "How is hydrogen peroxide detected at the platinum working electrode?", "answer": "The platinum anode is held at a positive potential (+0.65 V vs Ag/AgCl). H2O2 is electrochemically oxidized: H2O2 → O2 + 2 H⁺ + 2 e⁻. The resulting anodic current is proportional to the concentration of H2O2 and therefore to the original glucose concentration."},
                {"question": "Why is an outer diffusion-limiting membrane needed on clinical glucose biosensors?", "answer": "Native GOx has a Michaelis constant (Km) of ~4 to 6 mmol/L, causing saturation above 5 mmol/L. A diffusion-limiting membrane (polyurethane or Nafion) slows glucose diffusion relative to oxygen, artificially extending the linear dynamic range up to 25-30 mmol/L."},
                {"question": "What is the 'oxygen deficit' problem in first-generation glucose biosensors?", "answer": "In subcutaneous tissue, dissolved oxygen concentration (~0.1 mmol/L) is much lower than glucose concentration (~5.0 mmol/L). If oxygen becomes rate-limiting, the enzyme cannot regenerate, leading to non-linear saturation unless mediators or barrier membranes are employed."},
                {"question": "What physiological glucose range defines normal fasting glycemia, hypoglycemia, and hyperglycemia?", "answer": "Normal fasting blood glucose in healthy adults is 3.9 to 5.6 mmol/L (70 to 100 mg/dL). Clinical hypoglycemia is defined below 3.9 mmol/L (< 70 mg/dL), while postprandial diabetes thresholds exceed 11.1 mmol/L (> 200 mg/dL)."},
                {"question": "What interfering electroactive species in blood can cause false positive readings?", "answer": "Ascorbic acid (vitamin C), acetaminophen (paracetamol), and uric acid also undergo electrochemical oxidation at +0.65 V on bare platinum. Permselective membranes (such as negatively charged Nafion) repel these interferents to protect sensor specificity."}
            ],
            "precautions": [
                "Maintain constant magnetic stirring velocity to ensure stable diffusion boundary layer thickness.",
                "Control reaction temperature strictly at 37.0 °C; GOx enzyme turnover velocity is highly temperature-dependent.",
                "Ensure glucose solutions mutarotate for 24 hours prior to use so the α/β anomer ratio reaches thermodynamic equilibrium.",
                "Shield the electrochemical cell inside an aluminum Faraday enclosure to eliminate electrical line noise."
            ],
            "limitations": [
                "The linear kinetic model applies across the clinical range (2.0 to 12.0 mmol/L); higher levels enter enzyme saturation.",
                "Assumes excess dissolved oxygen in the buffer; severe hypoxia suppresses catalytic current.",
                "Enzyme activity gradually degrades over weeks due to thermal denaturing and peroxide self-inactivation.",
                "Subject to potential chemical interference from high therapeutic doses of acetaminophen."
            ],
            "quiz": [
                {
                    "question": "What enzyme is most widely used in commercial clinical blood glucose test strips?",
                    "options": ["Lactate dehydrogenase", "Glucose oxidase (GOx)", "Alkaline phosphatase", "Amylase"],
                    "correct": 1,
                    "explanation": "Glucose oxidase (GOx) is highly specific for β-D-glucose and is the primary enzyme used in commercial glucometers."
                },
                {
                    "question": "What chemical product of the enzymatic reaction is directly oxidized at the platinum electrode?",
                    "options": ["Water", "Hydrogen peroxide (H2O2)", "Gluconic acid", "Carbon dioxide"],
                    "correct": 1,
                    "explanation": "Hydrogen peroxide produced by GOx is oxidized at the polarized platinum anode: H2O2 → O2 + 2 H⁺ + 2 e⁻."
                },
                {
                    "question": "If measured current is 4.320 μA at a glucose concentration of 6.0 mmol/L, what is the sensitivity S_glu?",
                    "options": ["0.3600 μA/(mmol/L)", "0.7200 μA/(mmol/L)", "1.4400 μA/(mmol/L)", "2.8800 μA/(mmol/L)"],
                    "correct": 1,
                    "explanation": "Sensitivity S_glu = I_a / C_glu = 4.320 μA / 6.0 mmol/L = 0.7200 μA/(mmol/L)."
                },
                {
                    "question": "What is the normal fasting blood glucose concentration in healthy adults?",
                    "options": ["0.5 to 1.5 mmol/L", "3.9 to 5.6 mmol/L (70 to 100 mg/dL)", "15.0 to 25.0 mmol/L", "50 to 100 mmol/L"],
                    "correct": 1,
                    "explanation": "Normal fasting blood glucose in healthy non-diabetic adults is 3.9 to 5.6 mmol/L (70 to 100 mg/dL)."
                }
            ],
            "settings": ["Working electrode: Platinum screen-printed with immobilized GOx", "Polarizing potential: +0.650 V vs Ag/AgCl", "Buffer medium: 0.1 M PBS (pH 7.4, 37.0 °C, 250 RPM stirring)"],
            "samples": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🧪", "label": "1. Electrochemical Biosensor Cell"},
                {"id": "compare", "icon": "📊", "label": "2. Current vs Glucose Linearity"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Michaelis-Menten Sandbox"}
            ]
        },
        {
            "number": 15,
            "slug": "surface-plasmon-resonance-immunosensor-antibody-binding",
            "title": "Surface Plasmon Resonance (SPR) Biosensor Angle Shift & Biomolecular Affinity",
            "shortTitle": "SPR Immunosensor Kinetics",
            "aim": "Quantify the resonance angle shift of a gold-film SPR immunosensor as a function of analyte protein concentration to determine association kinetics and Langmuir adsorption linearity.",
            "inputLabel": "Antigen Concentration C_ag",
            "shortInput": "Antigen C",
            "inputUnit": "nM",
            "min": 5.0,
            "max": 30.0,
            "step": 5.0,
            "initial": 15.0,
            "inputDecimals": 1,
            "rawLabel": "Resonance Angle Shift Δθ",
            "rawUnit": "mdeg",
            "rawDecimals": 2,
            "xAxis": "Antigen concentration C_ag (nM)",
            "yAxis": "Resonance angle shift Δθ (millidegrees)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 17.5,
            "emptyY": 150.0,
            "targetName": "SPR Refractive Sensitivity k_spr",
            "target": "8.4000",
            "refValue": 8.4000,
            "resultUnit": "mdeg/nM",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "Δθ = k_spr · C_ag = 8.4000 · C_ag",
            "intro": "In modern pharmacology, biomarker discovery, and clinical immunology, Surface Plasmon Resonance (SPR) is the gold-standard label-free optical biosensing technology for measuring real-time macromolecular binding kinetics (antibody-antigen affinity, protein-protein interactions, and DNA hybridization). Under the Kretschmann prism-coupling optical configuration, p-polarized monochromatic laser light undergoes Total Internal Reflection (TIR) at the interface of a high-refractive-index glass prism coated with a 50 nm thin gold film. At a critical resonance angle θ_spr, photon energy couples into collective oscillations of free conduction-band electrons at the gold-dielectric interface, generating non-radiative surface plasmon polaritons that propagate along the metal surface. This resonance produces a sharp, localized intensity dip in the reflected light spectrum. The evanescent electromagnetic field decays exponentially into the sample solution (penetration depth ~200 nm), making the resonance angle exquisitely sensitive to minute refractive index changes in the immediate dielectric vicinity. When target antigen proteins bind specifically to immobilized antibodies on the sensor chip surface, the local mass density and refractive index increase, causing the SPR angle dip to shift by Δθ. In the sub-saturation Langmuir binding regime, angle shift Δθ is strictly linear with analyte concentration: Δθ = k_spr · C_ag. In this experiment, a functionalized anti-IgG gold sensor chip is tested across nano-molar antigen concentrations.",
            "modelExtra": "Evaluated using a 50 nm gold sensor chip functionalized with covalently coupled monoclonal anti-human IgG via an alkanethiol self-assembled monolayer (SAM). Analyte is human IgG diluted in HBS-EP running buffer (pH 7.4) perfused at 30 μL/min.",
            "apparatus": [
                {"name": "Biacore-Type Dual-Channel SPR Optical Engine", "purpose": "Kretschmann prism geometry with high-resolution 780 nm diode laser and linear CCD array."},
                {"name": "50 nm Sputtered Gold Sensor Chip (CM5 carboxymethylated)", "purpose": "Provides plasmonic gold surface with covalently immobilized anti-human IgG capture antibodies."},
                {"name": "Integrated Microfluidic Cartridge (IFC)", "purpose": "Maintains continuous laminar flow (30 μL/min) across sample and reference flowcells."},
                {"name": "Precision Temperature-Controlled Optical Deck (25.0 °C)", "purpose": "Eliminates refractive index thermal drift with ±0.01 °C Peltier thermal control."},
                {"name": "Certified Purified Human IgG Target Antigen Stock", "purpose": "NIST-traceable protein standards prepared in HBS-EP running buffer (10 to 60 nM)."},
                {"name": "Sensorgram Real-Time Kinetic Telemetry Software", "purpose": "Tracks angle dip minimum with 0.1 millidegree (0.1 Resonance Unit, RU) resolution."}
            ],
            "procedure": [
                {"title": "Sensor Chip Docking and Buffer Baseline Stabilization", "text": "Dock the functionalized CM5 gold chip into the optical block and prime flow channels with HBS-EP running buffer at 30 μL/min until baseline drift is < 0.2 mdeg/min."},
                {"title": "Reference Flowcell Subtraction Setup", "text": "Configure Channel 1 as non-specific reference (mock-immobilized) and Channel 2 as active antibody surface for inline differential subtraction."},
                {"title": "Initial Antigen Injection (5.0 nM)", "text": "Inject 5.0 nM human IgG antigen for 180 seconds, allowing binding association to reach equilibrium plateau; log net resonance angle shift Δθ in millidegrees."},
                {"title": "Surface Regeneration Cycle", "text": "Inject a 30-second pulse of 10 mM glycine-HCl (pH 2.0) to dissociate bound antigen and regenerate baseline antibody binding capacity."},
                {"title": "Concentration Progression Sequence", "text": "Sequentially inject antigen standards of 10.0, 15.0, 20.0, 25.0, and 30.0 nM, executing regeneration and baseline re-referencing at each step."},
                {"title": "Sensitivity Regression and Affinity Analysis", "text": "Plot steady-state angle shift Δθ against concentration C_ag, performing linear regression to evaluate SPR refractive sensitivity k_spr."}
            ],
            "topics": [
                {"question": "What physical phenomenon occurs at the resonance angle θ_spr in an SPR biosensor?", "answer": "At the resonance angle, the momentum of incoming p-polarized photons matches the momentum of surface plasmons (collective electron oscillations) at the gold-dielectric boundary. Photons couple their energy into the plasmon wave, resulting in a dramatic loss of reflected light intensity (a sharp absorption dip)."},
                {"question": "Why does biomolecular binding shift the SPR angle to a higher value?", "answer": "The evanescent wave penetrates approximately 200 nm into the liquid medium. When target biomolecules bind to capture antibodies on the gold surface, they displace water molecules with denser protein, raising the local refractive index. Higher refractive index increases plasmon momentum, shifting the resonance angle outward to a higher value."},
                {"question": "What is a 'Resonance Unit' (RU) in commercial Biacore SPR instruments?", "answer": "One Resonance Unit (RU) corresponds to an angle shift of 0.0001° (0.1 millidegree). In typical protein interactions, 1000 RU corresponds approximately to a surface protein mass density of 1.0 ng/mm²."},
                {"question": "What are the key advantages of SPR over traditional ELISA assays?", "answer": "SPR is completely label-free (no fluorescent tags or secondary enzyme-linked antibodies needed), provides real-time kinetic binding data (association rate k_on and dissociation rate k_off), and can be performed automatically in minutes."},
                {"question": "Why is an inline reference flowcell used in dual-channel SPR instruments?", "answer": "Injecting sample solutions causes a bulk refractive index shift due to differences in buffer salt or DMSO content. Subtracting the non-specific reference flowcell response (Fc2 - Fc1) eliminates this bulk refractive shift, isolating true molecular binding."},
                {"question": "What chemical reagent is commonly used to regenerate the antibody surface?", "answer": "Low pH buffers (such as 10 mM Glycine-HCl, pH 2.0 to 2.5) disrupt electrostatic interactions between antibody and antigen, dissociating the bound target while leaving the covalently immobilized capture antibody intact and ready for the next test."}
            ],
            "precautions": [
                "Degas all running buffers thoroughly; micro-bubbles in the flowcell create massive optical scattering spikes.",
                "Maintain strictly constant flow rate (30 μL/min) to prevent mass-transport-limited binding artifacts.",
                "Control optical deck temperature within ±0.01 °C; refractive index is highly sensitive to temperature.",
                "Ensure regeneration pulses are brief (30 s) to avoid irreversible antibody denaturation."
            ],
            "limitations": [
                "The linear sensitivity model applies in the low-concentration sub-saturation regime (C_ag ≤ 30 nM).",
                "Evanescent wave decays exponentially; molecules binding beyond 200 nm from the gold surface are invisible.",
                "Small molecules (< 300 Daltons) produce very small mass changes, requiring high-sensitivity competitive assays.",
                "Non-specific adsorption of sticky proteins from serum samples can cause false-positive refractive shifts."
            ],
            "quiz": [
                {
                    "question": "What metal is most widely used to produce surface plasmons in commercial SPR biosensors?",
                    "options": ["Lead", "Gold (Au)", "Iron", "Zinc"],
                    "correct": 1,
                    "explanation": "A 50 nm gold film provides excellent plasmonic resonance in the near-infrared and possesses outstanding chemical inertness."
                },
                {
                    "question": "Approximately what physical distance does the SPR evanescent wave penetrate into the sample solution?",
                    "options": ["1 nanometer", "200 nanometers", "10 millimeters", "1 meter"],
                    "correct": 1,
                    "explanation": "The evanescent electromagnetic field decays exponentially into the dielectric fluid, penetrating approximately 100 to 200 nm."
                },
                {
                    "question": "If measured resonance angle shift is 126.0 mdeg at an antigen concentration of 15.0 nM, what is the sensitivity k_spr?",
                    "options": ["4.2000 mdeg/nM", "8.4000 mdeg/nM", "16.8000 mdeg/nM", "25.2000 mdeg/nM"],
                    "correct": 1,
                    "explanation": "k_spr = Δθ / C_ag = 126.0 mdeg / 15.0 nM = 8.4000 mdeg/nM."
                },
                {
                    "question": "What is the primary benefit of SPR over traditional enzyme-linked immunosorbent assays (ELISA)?",
                    "options": ["SPR requires radioactive labels", "SPR provides real-time label-free measurement of binding kinetics (k_on and k_off)", "SPR only works with plastic", "SPR takes several weeks per test"],
                    "correct": 1,
                    "explanation": "SPR eliminates fluorescent or enzyme labels and monitors molecular association and dissociation kinetics continuously in real time."
                }
            ],
            "settings": ["Optics: Kretschmann prism geometry with 780 nm polarized diode laser", "Chip surface: 50 nm Au with covalently immobilized monoclonal anti-IgG", "Flow buffer: HBS-EP (pH 7.4, 25.0 °C, 30 μL/min continuous perfusion)"],
            "samples": [5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🔬", "label": "1. SPR Optical Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Sensorgram Binding Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Surface Plasmon Sandbox"}
            ]
        },
        {
            "number": 16,
            "slug": "impedance-pneumography-respiratory-tidal-volume",
            "title": "Transthoracic Electrical Impedance Pneumography & Tidal Volume Scaling",
            "shortTitle": "Impedance Pneumography",
            "aim": "Measure high-frequency (50 kHz) four-electrode transthoracic electrical impedance changes (ΔZ) during breathing cycles and calibrate against spirometric tidal volume.",
            "inputLabel": "Spirometric Tidal Volume V_t",
            "shortInput": "Volume V_t",
            "inputUnit": "L",
            "min": 0.5,
            "max": 3.0,
            "step": 0.5,
            "initial": 1.5,
            "inputDecimals": 1,
            "rawLabel": "Transthoracic Impedance Amplitude ΔZ",
            "rawUnit": "Ω",
            "rawDecimals": 3,
            "xAxis": "Tidal volume V_t (L)",
            "yAxis": "Transthoracic impedance change ΔZ (Ω)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 1.75,
            "emptyY": 2.5,
            "targetName": "Pneumographic Volume Sensitivity k_v",
            "target": "1.3500",
            "refValue": 1.3500,
            "resultUnit": "Ω/L",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ΔZ = k_v · V_t = 1.3500 · V_t",
            "intro": "Continuous non-invasive monitoring of respiratory rate and tidal volume is essential in intensive care units, neonatal incubators, sleep medicine polysomnography, and post-anesthesia recovery rooms. Transthoracic electrical impedance pneumography provides an elegant bedside method to record respiration without requiring invasive face masks or mouthpieces. The physiological principle exploits the dramatic electrical conductivity difference between air and thoracic tissues. De-aerated lung tissue and thoracic blood have relatively high electrical conductivity (saline and blood ~0.7 S/m), whereas inhaled atmospheric air has zero electrical conductivity. During inspiration, the lungs inflate with air, increasing the non-conductive alveolar gas volume and lengthening electrical current streamlines across the ribcage, which causes baseline transthoracic electrical impedance to rise. Under a four-electrode (tetrapolar) configuration, a safe, high-frequency constant AC carrier current (typically 50 kHz, 100 μA RMS, far above the neuromuscular excitation threshold) is injected through outer drive electrodes, while inner pickup electrodes detect the resulting surface voltage drop. Across normal physiological tidal volumes V_t (0.5 to 3.0 L), the peak-to-peak respiratory impedance change ΔZ scales in direct linear proportion: ΔZ = k_v · V_t. In this experiment, an instrumented impedance pneumograph is calibrated simultaneously against a digital clinical spirometer.",
            "modelExtra": "Evaluated using a four-electrode tetrapolar chest band montage at mid-axillary level (6th intercostal space) with 50 kHz, 200 μA RMS carrier excitation. Synchronously calibrated against a turbine spirometer across voluntary tidal volumes from 0.5 L to 3.0 L.",
            "apparatus": [
                {"name": "Tetrapolar High-Frequency Impedance Pneumograph", "purpose": "Generates 50 kHz constant-current excitation (200 μA RMS) and detects differential voltage."},
                {"name": "Calibrated Turbine Digital Spirometer", "purpose": "Provides gold-standard primary reference measurement of inspired and expired tidal volume in Liters."},
                {"name": "Four Sintered Ag/AgCl Disposable Pre-Gelled Electrodes", "purpose": "Affixed in bilateral mid-axillary line across the 6th intercostal space (tetrapolar arrangement)."},
                {"name": "Precision Synchronous AM Demodulator & Bandpass Filter", "purpose": "Demodulates 50 kHz carrier and filters respiratory band (0.05 to 2.0 Hz)."},
                {"name": "Cardiogenic Artifact Rejection Filter", "purpose": "Suppresses small (0.1 to 0.2 Ω) cardiogenic impedance oscillations synchronous with heartbeats."},
                {"name": "Multi-Channel Bio-Telemetry Logging Workstation", "purpose": "Simultaneously records spirometry flow, integrated volume V_t, and thoracic impedance ΔZ."}
            ],
            "procedure": [
                {"title": "Tetrapolar Electrode Montage Application", "text": "Clean skin with alcohol wipes and affix four electrodes along the mid-axillary line: outer pair for 50 kHz current injection, inner pair for voltage pickup."},
                {"title": "Baseline Impedance Balance and Carrier Setup", "text": "Energize 50 kHz 200 μA oscillator; record baseline thoracic resting end-expiratory impedance (Z_0, typically 25 to 50 Ω)."},
                {"title": "Simultaneous Spirometer Coupling", "text": "Seat subject comfortably and fit nose clip; connect subject to calibrated turbine spirometer to log air volume simultaneously."},
                {"title": "Standardized Shallow Inhalation (0.5 L)", "text": "Instruct subject to inhale to achieve a spirometric tidal volume V_t of exactly 0.50 L; log stabilized peak impedance excursion ΔZ in Ohms."},
                {"title": "Tidal Volume Step Progression", "text": "Guide subject through voluntary breathing increments of 1.0, 1.5, 2.0, 2.5, and 3.0 L, recording paired (V_t, ΔZ) values across 5 breaths per step."},
                {"title": "Pneumographic Sensitivity Regression", "text": "Plot respiratory impedance amplitude ΔZ against tidal volume V_t, fitting linear regression through the origin to determine sensitivity k_v."}
            ],
            "topics": [
                {"question": "Why is a four-electrode (tetrapolar) arrangement used instead of two electrodes in impedance pneumography?",
                "answer": "A two-electrode setup measures the huge, variable contact impedances of the skin-electrode interfaces in series with the tissue. In a four-electrode arrangement, current is injected through outer electrodes while inner voltage-sensing electrodes draw virtually zero current, eliminating contact impedance artifacts and isolating true deep thoracic impedance."},
                {"question": "Why is a high-frequency AC carrier (e.g., 50 kHz) used rather than DC or low-frequency current?",
                "answer": "At 50 kHz, the current easily bypasses the capacitive impedance of the skin's stratum corneum without stinging, and high frequency prevents any risk of depolarizing cardiac or skeletal muscle membranes (avoiding ventricular fibrillation hazards)."},
                {"question": "What is the cardiogenic impedance artifact and how is it filtered?",
                "answer": "With each cardiac cycle, blood ejected from the ventricles into the pulmonary circulation and aorta alters regional thoracic conductivity, producing small rhythmic impedance pulses (0.1 to 0.3 Ω). Because their frequency matches the heart rate (1 to 2 Hz), digital notch filtering or R-wave triggered averaging removes them."},
                {"question": "How does lung tissue conductivity change during inhalation?", "answer": "Inhalation fills the alveolar sacs with air (conductivity ≈ 0 S/m), displacing conductive blood and interstitial fluid, lengthening electrical conduction pathways through the thoracic cage, and causing total electrical impedance to increase."},
                {"question": "What clinical limitation affects impedance pneumography in detecting obstructive sleep apnea?",
                "answer": "In obstructive sleep apnea, the upper airway is blocked, but the patient continues to make vigorous thoracic and abdominal respiratory efforts against the obstruction. The chest expands, producing an apparent impedance signal despite zero actual airflow, creating a false-negative apnea detection."},
                {"question": "What is Electrical Impedance Tomography (EIT)?", "answer": "EIT is an advanced extension of impedance pneumography that uses a ring of 16 to 32 electrodes around the chest to reconstruct cross-sectional 2D dynamic images of regional lung ventilation and perfusion in real time."}
            ],
            "precautions": [
                "Instruct subject to breathe steadily without torso twisting or posture shifts that alter baseline ribcage geometry.",
                "Ensure outer current-drive electrodes are spaced at least 5 cm away from inner voltage-pickup electrodes.",
                "Verify that spirometer turbine calibration is zeroed and calibrated with a certified 3.00 L calibration syringe.",
                "Verify carrier current remains under IEC 60601-1 patient safety auxiliary current limits (under 500 μA at 50 kHz)."
            ],
            "limitations": [
                "The linear sensitivity model applies across normal physiological tidal volumes (0.5 to 3.0 L).",
                "Calibrations shift significantly if patient changes posture (e.g., transitioning from supine to upright sitting).",
                "Does not differentiate between ribcage expansion and abdominal diaphragm excursions without dual-band montage.",
                "Severe pulmonary edema (fluid in the lungs) lowers baseline impedance and attenuates respiratory swings."
            ],
            "quiz": [
                {
                    "question": "Why does transthoracic electrical impedance increase during lung inhalation?",
                    "options": ["Blood flow stops completely", "Inhaled atmospheric air is non-conductive, displacing conductive blood and lengthening tissue current paths", "The chest gets colder", "The electrodes become disconnected"],
                    "correct": 1,
                    "explanation": "Air has zero electrical conductivity; expanding the lungs with air increases total thoracic electrical resistance."
                },
                {
                    "question": "What is the primary advantage of a four-electrode (tetrapolar) impedance measurement?",
                    "options": ["It uses half as many wires", "It eliminates skin-electrode contact impedance errors from the measured voltage", "It works without electricity", "It doubles the patient's heart rate"],
                    "correct": 1,
                    "explanation": "Because the inner sensing electrodes draw virtually zero current, skin-electrode contact impedances drop out of the measurement."
                },
                {
                    "question": "If inspired tidal volume is 2.0 L and measured impedance change is 2.700 Ω, what is the sensitivity k_v?",
                    "options": ["0.6750 Ω/L", "1.3500 Ω/L", "2.7000 Ω/L", "5.4000 Ω/L"],
                    "correct": 1,
                    "explanation": "Sensitivity k_v = ΔZ / V_t = 2.700 Ω / 2.0 L = 1.3500 Ω/L."
                },
                {
                    "question": "What frequency is typically used for the carrier excitation current in impedance pneumographs?",
                    "options": ["0.1 Hz", "10 Hz", "50 to 100 kHz", "100 MHz"],
                    "correct": 2,
                    "explanation": "A high frequency of 50 to 100 kHz easily penetrates skin capacitance and avoids stimulating nerves or the heart."
                }
            ],
            "settings": ["Carrier excitation: 50.0 kHz sinusoidal constant current (200 μA RMS)", "Montage: Mid-axillary tetrapolar Ag/AgCl chest bands", "Reference: Turbine digital spirometer (BTPS corrected)"],
            "samples": [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🫁", "label": "1. Impedance Pneumograph Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Delta-Z vs Spirometric Volume"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Thoracic Bio-Impedance Sandbox"}
            ]
        },
        {
            "number": 17,
            "slug": "digital-notch-filter-60hz-powerline-interference",
            "title": "IIR Digital Notch Filter Design & 50/60 Hz Powerline Interference Removal",
            "shortTitle": "ECG Powerline Notch Filter",
            "aim": "Design and implement a second-order IIR notch filter (Q = 30) to suppress 60 Hz hum from corrupted ECG telemetry while preserving diagnostic ST-segment and QRS morphology.",
            "inputLabel": "Input Interference Power P_in",
            "shortInput": "Noise P_in",
            "inputUnit": "mV²",
            "min": 0.1,
            "max": 1.1,
            "step": 0.2,
            "initial": 0.5,
            "inputDecimals": 1,
            "rawLabel": "Residual Output Power P_out",
            "rawUnit": "μV²",
            "rawDecimals": 3,
            "xAxis": "Input interference power P_in (mV²)",
            "yAxis": "Output residual power P_out (μV²)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 0.6,
            "emptyY": 3.0,
            "targetName": "Notch Filter Power Transmission k_n",
            "target": "0.0050",
            "refValue": 0.0050,
            "resultUnit": "ratio",
            "resultDecimals": 4,
            "resultScale": 1000.0,
            "fitEquation": "P_out = k_n · P_in = 0.0050 · P_in",
            "intro": "In clinical electrophysiology, 50 Hz or 60 Hz powerline interference is the most pervasive electromagnetic contaminant obscuring biopotential telemetry (ECG, EEG, EMG). Radiated by AC power cabling, fluorescent lighting ballasts, and hospital equipment, powerline interference manifests as a sharp sinusoidal artifact superimposed on microvolt biopotentials. While differential instrumentation amplifiers and Right Leg Drive circuits attenuate a large fraction of common-mode hum, residual common-mode-to-differential conversion caused by electrode impedance imbalances necessitates digital filtering in the digital signal processor (DSP). To eliminate 60 Hz hum without distorting critical clinical features—such as the sharp high-frequency QRS peak or subtle low-frequency ST-segment elevations diagnostic of acute myocardial infarction—a specialized second-order Infinite Impulse Response (IIR) digital notch filter is synthesized via bilinear transformation. The transfer function places conjugate complex zeros on the unit circle at z = exp(±j · 2π · f_0 / f_s) and matching poles at r · exp(±j · 2π · f_0 / f_s) with radius r = 1 - (π · BW / f_s), establishing a sharp notch (Q = f_0 / BW = 30). In this laboratory investigation, synthesized ECG signals corrupted by controlled 60 Hz interference are processed through the digital notch filter to quantify power attenuation and verify linear power suppression.",
            "modelExtra": "Evaluated using a second-order IIR digital notch filter centered at f_0 = 60.0 Hz with sampling frequency f_s = 500 Hz and 3 dB notch bandwidth BW = 2.0 Hz (Q = 30). Input 60 Hz interference power is varied from 0.1 to 1.1 mV².",
            "apparatus": [
                {"name": "Digital Signal Processing Biosignal Testbed", "purpose": "Real-time DSP hardware platform executing discrete-time IIR filtering algorithms."},
                {"name": "Calibrated ECG Waveform Synthesizer", "purpose": "Generates clean 12-lead diagnostic ECG signals at 72 BPM with standard amplitude (1.0 mV peak)."},
                {"name": "Precision 60.0 Hz Interference Generator", "purpose": "Injects calibrated 60 Hz sinusoidal noise power into the synthesized ECG signal."},
                {"name": "Fast Fourier Transform (FFT) Power Spectrum Analyzer", "purpose": "Computes power spectral density before and after filtering with 0.1 Hz spectral resolution."},
                {"name": "Digital Storage Oscilloscope with Telemetry Display", "purpose": "Displays raw corrupted ECG, filtered ECG, and residual error waveform in real time."},
                {"name": "Digital Filter Coefficient Synthesis Tool", "purpose": "Calculates floating-point biquad numerator and denominator coefficients for IIR notch filter."}
            ],
            "procedure": [
                {"title": "Filter Coefficient Calculation and DSP Initialization", "text": "Compute second-order IIR notch coefficients for f_0 = 60.0 Hz, f_s = 500 Hz, Q = 30: b = [1, -2·cos(ω_0), 1], a = [1, -2·r·cos(ω_0), r²] with r = 0.9874; load into DSP memory."},
                {"title": "Clean ECG Baseline Reference", "text": "Input pure clean 1.0 mV ECG waveform without noise; confirm that filter passband causes zero visible attenuation or phase distortion of the QRS complex."},
                {"title": "Initial 60 Hz Noise Injection (P_in = 0.10 mV²)", "text": "Superimpose 60.0 Hz sinusoidal hum to establish an input noise power P_in = 0.10 mV² (amplitude ~0.45 mV peak-to-peak)."},
                {"title": "Residual Filtered Power Acquisition", "text": "Run real-time biquad filtering and compute FFT power spectral density at 60 Hz; log residual output power P_out in μV²."},
                {"title": "Noise Power Progression Sequence", "text": "Increment 60 Hz interference power through 0.30, 0.50, 0.70, 0.90, and 1.10 mV², recording residual output power P_out at each step."},
                {"title": "Rejection Ratio Regression Analysis", "text": "Plot residual output power P_out against input interference power P_in, performing linear regression to evaluate the power transmission ratio k_n."}
            ],
            "topics": [
                {"question": "How is a digital notch filter transfer function constructed using z-plane poles and zeros?", "answer": "The filter places a pair of complex-conjugate zeros directly on the unit circle at angle ω_0 = 2π·f_0/f_s to create infinite theoretical attenuation at the notch frequency. Matching poles are placed at the same angle just inside the unit circle at radius r (e.g., r = 0.985) to cancel attenuation at neighboring frequencies, creating a sharp, narrow notch."},
                {"question": "What is the Quality Factor (Q) of a notch filter and why is high Q desirable?", "answer": "The Quality Factor is defined as Q = f_0 / BW, where BW is the 3 dB notch bandwidth. A high Q (e.g., Q = 30) produces an extremely narrow notch (BW = 2 Hz), which removes the 60 Hz interference while preserving adjacent physiological ECG spectral energy at 58 Hz and 62 Hz."},
                {"question": "What distortion can an IIR notch filter introduce into an ECG waveform?", "answer": "Because IIR filters have non-linear phase response, frequency components near the notch frequency experience different time delays. This can cause phase ringing (oscillation tails) immediately following sharp QRS complexes and can distort the clinical ST-segment, potentially mimicking or masking myocardial ischemia."},
                {"question": "How does an FIR notch filter compare with an IIR notch filter?", "answer": "An FIR filter can achieve perfectly linear phase (zero phase distortion when filtered forward and backward), but requires hundreds of filter taps to achieve a sharp notch, creating significant computational latency; an IIR filter achieves a sharp notch with only 2nd-order complexity."},
                {"question": "Why is powerline interference 60 Hz in the Americas and 50 Hz in Europe and Asia?", "answer": "Electrical grid standards differ by region: North America and parts of South America and Japan use 60 Hz AC electrical distribution, whereas Europe, Asia, Africa, and Australia standardize on 50 Hz AC. Digital medical devices often feature auto-detecting notch filters."},
                {"question": "Why should analog filtering not be solely relied upon for powerline rejection?", "answer": "High-Q analog notch filters using operational amplifiers and capacitors suffer from component tolerance drift (resistor and capacitor aging and temperature drift), causing the notch center frequency to drift away from exact 60.0 Hz; digital DSP filters have stable, drift-free center frequencies."}
            ],
            "precautions": [
                "Verify that sampling frequency f_s is strictly synchronous and stable to prevent filter center frequency drift.",
                "Ensure floating-point arithmetic uses 64-bit precision to prevent numerical quantization limit cycles in the IIR feedback loop.",
                "Allow the filter to settle for 500 samples before measuring output power to eliminate initial transient step ringing.",
                "Verify input signal does not clip or saturate the integer analog-to-digital converter dynamic range."
            ],
            "limitations": [
                "The linear power transmission model applies across the tested linear range (P_in ≤ 1.1 mV²).",
                "Does not remove harmonic powerline frequencies (120 Hz, 180 Hz); harmonic rejection requires comb filters.",
                "Phase non-linearity can introduce ringing artifacts on fast spikes like pacemaker pulses.",
                "Assumes stationary 60.0 Hz hum; rapid frequency fluctuations on unstable backup generators cause leakage."
            ],
            "quiz": [
                {
                    "question": "Where are the transmission zeros of an ideal digital notch filter placed in the z-plane?",
                    "options": ["At the origin z = 0", "Directly on the unit circle |z| = 1 at angle ω_0 = ±2π·f_0/f_s", "At infinity", "On the negative real axis"],
                    "correct": 1,
                    "explanation": "Placing zeros directly on the unit circle at the notch frequency angle causes the frequency response magnitude to drop to zero."
                },
                {
                    "question": "Why is a high Quality Factor (Q ≥ 30) preferred for ECG powerline notch filtering?",
                    "options": ["To make the filter run faster", "To narrow the notch bandwidth so only 60 Hz is removed without attenuating physiological ECG frequencies", "To invert the signal polarity", "To amplify the cardiac QRS wave"],
                    "correct": 1,
                    "explanation": "High Q creates a surgical, narrow notch (e.g., 59 to 61 Hz) that preserves clinical ECG spectral energy at adjacent frequencies."
                },
                {
                    "question": "If input noise power is 0.80 mV² and power transmission ratio k_n is 0.0050, what is the residual power in μV²?",
                    "options": ["0.004 μV²", "4.000 μV²", "40.00 μV²", "400.0 μV²"],
                    "correct": 1,
                    "explanation": "P_out = 0.0050 · 0.80 mV² = 0.0040 mV² = 4.000 μV² (an attenuation factor of 200:1 or -23 dB power, -46 dB voltage)."
                },
                {
                    "question": "What type of artifact can an IIR notch filter introduce near sharp QRS complexes due to non-linear phase?",
                    "options": ["High-frequency ringing and artificial ST-segment elevation", "Immediate flatlining", "DC offset of 100 Volts", "Inversion of the P wave"],
                    "correct": 0,
                    "explanation": "Non-linear phase response near the notch frequency produces phase ringing and can distort the ST-segment."
                }
            ],
            "settings": ["Filter topology: 2nd-order IIR biquad notch (Q = 30, BW = 2.0 Hz)", "Sampling rate: f_s = 500 Hz (f_0 = 60.0 Hz notch center)", "ECG baseline: Clean 1.0 mV peak QRS at 72 BPM"],
            "samples": [0.1, 0.3, 0.5, 0.7, 0.9, 1.1],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "⚡", "label": "1. DSP Filtering Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Power Spectrum Rejection"},
                {"id": "sandbox", "icon": "🔬", "label": "3. Z-Plane Pole-Zero Sandbox"}
            ]
        }
    ]
