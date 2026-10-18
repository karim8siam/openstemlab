# -*- coding: utf-8 -*-
"""Biomedical Engineering Module 5: Medical Imaging Systems, Bio-optics, Bio-MEMS & Rehabilitation (Labs 35–42)."""

def get_module_5():
    return [
        {
            "number": 35,
            "slug": "ultrasound-transducer-acoustic-beam-profiling",
            "title": "Medical Ultrasound Transducer Acoustic Beam Attenuation & Spatial Profiling",
            "shortTitle": "Ultrasound Acoustic Attenuation",
            "aim": "Determine the acoustic attenuation coefficient α_u of a tissue-mimicking phantom in an automated ultrasound test tank across depths using a calibrated PVDF needle hydrophone.",
            "inputLabel": "Phantom Axial Depth z",
            "shortInput": "Depth z",
            "inputUnit": "cm",
            "min": 2.0,
            "max": 12.0,
            "step": 2.0,
            "initial": 6.0,
            "inputDecimals": 1,
            "rawLabel": "Acoustic Signal Attenuation A_db",
            "rawUnit": "dB",
            "rawDecimals": 3,
            "xAxis": "Axial depth z (cm)",
            "yAxis": "Acoustic attenuation A_db (dB)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 7.0,
            "emptyY": 12.0,
            "targetName": "Acoustic Attenuation Coefficient α_u",
            "target": "1.8500",
            "refValue": 1.8500,
            "resultUnit": "dB/cm",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "A_db = α_u · z = 1.8500 · z (at 3.5 MHz ultrasound center frequency)",
            "measureLabel": "Measure Acoustic Hydrophone Signal",
            "intro": "Diagnostic ultrasound imaging is among the most widely deployed, safe, and cost-effective clinical imaging modalities, offering real-time visualization of soft tissues, cardiac dynamics (echocardiography), fetal development, and vascular perfusion without ionizing radiation. The propagation of ultrasound waves through biological media is governed by acoustic wave equations. As the piezoelectric transducer launches high-frequency longitudinal pressure waves (typically 2 to 15 MHz) into soft tissue, the acoustic intensity I(z) decays exponentially with propagation depth z due to absorption (conversion of acoustic energy into viscous heat) and scattering (redirection of acoustic energy away from the beam by sub-wavelength cellular structures): I(z) = I_0 · exp(-2·α·z). In clinical acoustic engineering and decibel notation, acoustic signal attenuation A_db is expressed as A_db = 10 · log₁₀(I_0 / I) = 20 · log₁₀(P_0 / P) = α_u · z, where α_u is the acoustic attenuation coefficient in dB/cm. In soft tissues, acoustic attenuation scales approximately linearly with ultrasound frequency: α_u(f) = a_0 · f^n (where n ≈ 1.0 to 1.1, and a_0 ≈ 0.5 to 0.7 dB/(cm·MHz)). For an abdominal probe centered at 3.5 MHz, standard tissue phantoms exhibit an attenuation of approximately 1.85 dB/cm. In this laboratory investigation, an automated 3-axis ultrasound beam profiling tank equipped with a 0.5 mm PVDF needle hydrophone scans acoustic pressure fields through standardized tissue-mimicking phantoms to evaluate α_u.",
            "modelExtra": "Evaluated using a 3.5 MHz focused piezoelectric transducer (diameter 19 mm, focal length 60 mm) submerged in degassed water and traversing a CIRS tissue-mimicking phantom (speed of sound 1540 m/s). Acoustic pressures detected by a calibrated 0.5 mm PVDF needle hydrophone across depths z = 2.0 to 12.0 cm. Linear decibel attenuation slope α_u = 1.8500 dB/cm.",
            "apparatus": [
                {"name": "Automated 3-Axis Scanning Ultrasound Test Tank", "purpose": "Provides computer-controlled motorized micro-positioning (10 μm step resolution) in degassed deionized water."},
                {"name": "3.5 MHz Single-Element Focused Ultrasound Transducer", "purpose": "Generates standardized diagnostic ultrasound acoustic pulses with center frequency 3.50 MHz."},
                {"name": "Calibrated 0.5 mm PVDF Needle Hydrophone (Precision Acoustics)", "purpose": "Detects high-frequency acoustic pressure waveforms from 1 to 20 MHz with broad flat bandwidth."},
                {"name": "Standardized Tissue-Mimicking Ultrasonic Phantom (CIRS)", "purpose": "Provides certified acoustic properties (c = 1540 m/s, backscatter -40 dB) with calibrated depth steps."},
                {"name": "High-Voltage Ultrasound Pulser-Receiver (Olympus 5077PR)", "purpose": "Energizes transducer with fast 200 V negative spike pulses and provides low-noise RF preamplification."},
                {"name": "High-Speed 14-Bit RF Digitizing Oscilloscope (200 MS/s)", "purpose": "Digitizes raw radiofrequency (RF) acoustic A-lines with 200 megasamples/sec sampling rate."}
            ],
            "procedure": [
                {"title": "Water Tank Degassing and Hydrophone Alignment", "text": "Fill test tank with degassed deionized water (dissolved O₂ < 4 ppm) and align transducer acoustic axis with PVDF needle hydrophone tip using pulse-echo reflections."},
                {"title": "Acoustic Centerline Spatial Alignment", "text": "Scan the hydrophone across orthogonal x-y planes to identify the maximum acoustic pressure axis, aligning coordinate z with the beam propagation path."},
                {"title": "Reference Free-Field Intensity Calibration", "text": "Record baseline peak-to-peak acoustic pressure P_0 in pure degassed water at focal distance (z = 0) as reference unattenuated intensity."},
                {"title": "Tissue Phantom Insertion and Depth Positioning", "text": "Position calibrated tissue-mimicking phantom blocks between transducer and hydrophone, setting initial tissue path length z = 2.0 cm."},
                {"title": "Radiofrequency A-Line Capture and Filtering", "text": "Record 100 averaged RF acoustic A-line waveforms, calculate root-mean-square acoustic pressure P(z), and compute decibel attenuation A_db = 20 · log₁₀(P_0 / P)."},
                {"title": "Axial Depth Progression Sequence", "text": "Increment phantom thickness through 4.0, 6.0, 8.0, 10.0, and 12.0 cm, recording stabilized decibel attenuation A_db at each step."},
                {"title": "Attenuation Coefficient Linear Regression", "text": "Plot decibel attenuation A_db versus axial depth z and extract acoustic attenuation coefficient α_u from the slope of the linear fit through the origin."}
            ],
            "topics": [
                {"question": "Why does acoustic attenuation in biological tissue scale linearly with ultrasound frequency?", "answer": "Acoustic absorption in soft tissue is dominated by macromolecular relaxation processes (viscous shear relaxation of hydrated structural proteins like collagen and albumin), which exhibit a broad distribution of relaxation frequencies that sum to yield an attenuation approximately proportional to frequency (α ∝ f¹·⁰)."},
                {"question": "What is the clinical trade-off between ultrasound penetration depth and image resolution?", "answer": "High frequencies (10–15 MHz) offer shorter wavelengths that provide excellent axial spatial resolution (λ = c/f ≈ 0.1 mm) but suffer severe attenuation, restricting imaging to superficial structures (< 4 cm); low frequencies (2–5 MHz) penetrate deeply into the abdomen (up to 20 cm) but have poorer resolution (λ ≈ 0.5 mm)."},
                {"question": "Why is 1540 m/s universally assumed as the speed of sound in medical ultrasound scanners?", "answer": "Human soft tissues (liver, kidney, muscle, brain) have sound speeds clustering closely around an average of 1540 m/s; clinical ultrasound scanners use this constant to convert pulse round-trip transit time Δt into axial depth z = c · Δt / 2."},
                {"question": "What is acoustic impedance Z and why is coupling gel necessary on human skin?", "answer": "Acoustic impedance Z = ρ·c is the product of density and sound speed. Soft tissue has Z ≈ 1.5–1.6 MRayl, while air has Z ≈ 0.0004 MRayl. The enormous impedance mismatch at a skin-air interface reflects > 99.9% of acoustic energy; aqueous coupling gel matches tissue impedance and eliminates air gaps."},
                {"question": "What is the difference between specular reflection and Rayleigh scattering in ultrasound?", "answer": "Specular reflections occur at large, smooth interfaces (organ capsules, diaphragm, vessel walls) producing strong, mirror-like echoes, whereas Rayleigh scattering occurs from sub-wavelength structures (individual red cells, microscopic collagen fibrils) that scatter acoustic waves isotropically in all directions, creating tissue acoustic speckle."},
                {"question": "What safety indices monitor ultrasound bioeffects in clinical imaging?", "answer": "The Thermal Index (TI) estimates maximum expected tissue temperature rise (°C) due to acoustic absorption, while the Mechanical Index (MI = P_neg / √f) assesses the risk of acoustic cavitation and microvascular mechanical injury, regulated strictly by the FDA (MI < 1.9)."}
            ],
            "precautions": [
                "Ensure water tank is thoroughly degassed; microscopic air bubbles act as acoustic reflectors that scatter the ultrasound beam.",
                "Protect fragile PVDF needle hydrophone tip (diameter 0.5 mm); mechanical contact with tank walls causes permanent sensor destruction.",
                "Verify acoustic alignment across x-y planes at each depth to ensure hydrophone remains centered in the main acoustic focal lobe.",
                "Maintain constant water temperature (22.0 °C) to prevent sound speed variations from skewing spatial coordinates."
            ],
            "limitations": [
                "The linear decibel attenuation model applies to homogeneous media; human anatomy presents complex layered structures with refraction and reverberation.",
                "Assumes plane-wave or narrow-beam propagation, neglecting beam divergence and geometric diffraction corrections.",
                "Tested at diagnostic low acoustic pressures; high-intensity focused ultrasound (HIFU) introduces non-linear acoustic waveform distortion.",
                "Tissue phantom provides uniform attenuation but does not model acoustic clutter caused by subcutaneous adipose tissue layers."
            ],
            "quiz": [
                {
                    "question": "What is the typical average speed of sound assumed for human soft tissues in clinical ultrasound scanners?",
                    "options": ["1540 m/s", "330 m/s", "3000 m/s", "300,000 km/s"],
                    "correct": 0,
                    "explanation": "1540 m/s is the standard international calibration value for the speed of sound in soft tissue."
                },
                {
                    "question": "Why does a 12 MHz ultrasound probe have shallower penetration than a 3.5 MHz probe?",
                    "options": ["Acoustic attenuation in tissue increases proportionally with frequency, absorbing high frequencies rapidly", "12 MHz probes have dead batteries", "High frequencies cannot travel through water", "12 MHz ultrasound bounces off skin completely"],
                    "correct": 0,
                    "explanation": "Acoustic attenuation scales with frequency (α ∝ f); higher frequency sound waves are absorbed much more rapidly by tissue."
                },
                {
                    "question": "If acoustic signal attenuation is 11.10 dB at a phantom depth of 6.0 cm, what is attenuation coefficient α_u?",
                    "options": ["0.925 dB/cm", "1.850 dB/cm", "3.700 dB/cm", "5.550 dB/cm"],
                    "correct": 1,
                    "explanation": "α_u = A_db / z = 11.10 dB / 6.0 cm = 1.8500 dB/cm."
                },
                {
                    "question": "What regulatory safety metric monitors the risk of acoustic cavitation during diagnostic ultrasound imaging?",
                    "options": ["Mechanical Index (MI)", "Thermal Index (TI)", "Heart Rate Reserve", "Body Mass Index"],
                    "correct": 0,
                    "explanation": "The Mechanical Index (MI) quantifies the potential for acoustic cavitation (bubble nucleation and collapse) in tissue."
                }
            ],
            "settings": ["Transducer: 3.5 MHz single-element focused transducer (Ø 19 mm, focal length 60 mm)", "Hydrophone: 0.5 mm PVDF needle hydrophone (Precision Acoustics)", "Medium: Degassed water and CIRS tissue phantom (c = 1540 m/s)"],
            "samples": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🔊", "label": "1. Ultrasound Test Tank"},
                {"id": "compare", "icon": "📊", "label": "2. Decibel Attenuation vs Depth"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Acoustic Beam Sandbox"}
            ]
        },
        {
            "number": 36,
            "slug": "x-ray-narrow-beam-linear-attenuation-hvl",
            "title": "Diagnostic X-Ray Narrow-Beam Linear Attenuation & Half-Value Layer (HVL)",
            "shortTitle": "X-Ray Linear Attenuation & HVL",
            "aim": "Determine the linear attenuation coefficient μ and Half-Value Layer (HVL) of high-purity aluminum filters for an 80 kVp diagnostic X-ray beam under narrow-beam geometry.",
            "inputLabel": "Aluminum Absorber Thickness x",
            "shortInput": "Thickness x",
            "inputUnit": "mm",
            "min": 1.0,
            "max": 6.0,
            "step": 1.0,
            "initial": 3.0,
            "inputDecimals": 1,
            "rawLabel": "Transmitted Intensity Ratio I/I₀",
            "rawUnit": "ratio",
            "rawDecimals": 4,
            "xAxis": "Absorber thickness x (mm)",
            "yAxis": "Natural log intensity ratio ln(I/I₀)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.5,
            "emptyY": -0.75,
            "targetName": "Linear Attenuation Coefficient μ",
            "target": "0.2450",
            "refValue": 0.2450,
            "resultUnit": "mm⁻¹",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ln(I/I₀) = -μ · x = -0.2450 · x",
            "measureLabel": "Record X-Ray Exposure",
            "intro": "In diagnostic radiography, computed tomography (CT), and radiation therapy, understanding X-ray beam attenuation and beam quality is essential for optimizing diagnostic image contrast while minimizing ionizing radiation dose to the patient (ALARA principle: As Low As Reasonably Achievable). When an energetic X-ray photon beam traverses matter, photons interact via photoelectric absorption, Compton scattering, and coherent scattering. In narrow-beam geometry (where narrow lead collimators prevent scattered photons from reaching the detector), monoenergetic photon transmission obeys the classical Beer-Lambert exponential attenuation law: I(x) = I_0 · exp(-μ · x), where I_0 is incident beam air kerma, x is absorber thickness (mm), and μ is the linear attenuation coefficient (mm⁻¹). Taking the natural logarithm linearizes the attenuation: ln(I / I_0) = -μ · x. In diagnostic radiology, clinical X-ray tubes emit a polyenergetic Bremsstrahlung spectrum. The Half-Value Layer (HVL)—the thickness of an absorbing material (typically high-purity type 1100 aluminum) required to reduce beam exposure rate to exactly 50% of its unattenuated value: HVL = ln(2) / μ ≈ 0.693 / μ—is the universally mandated regulatory measure of effective beam penetration energy and filtration quality. For a clinical 80 kVp diagnostic beam with standard filtration, the effective linear attenuation coefficient in aluminum is μ ≈ 0.2450 mm⁻¹ (yielding HVL ≈ 2.83 mm Al). In this experiment, an instrumented lead-shielded cabinet with an ionization chamber evaluates aluminum filtration.",
            "modelExtra": "Evaluated on a diagnostic X-ray tube operated at 80 kVp tube potential, 50 mA tube current, 100 ms exposure time (5 mAs) with 2.5 mm Al inherent filtration. Source-to-detector distance (SDD) is 100 cm under narrow-beam lead collimation (aperture 10 mm). High-purity Type 1100 aluminum attenuator sheets (thickness 1.0 to 6.0 mm). Linear attenuation coefficient μ = 0.2450 mm⁻¹ (HVL = 2.83 mm Al).",
            "apparatus": [
                {"name": "Lead-Shielded Diagnostic X-Ray Enclosure", "purpose": "Provides radiation-shielded cabinet with interlocked doors ensuring complete laboratory safety."},
                {"name": "Diagnostic Rotating-Anode Tungsten Target X-Ray Tube", "purpose": "Generates regulated 80 kVp Bremsstrahlung and characteristic tungsten X-ray spectrum."},
                {"name": "Narrow-Beam Double Lead Collimator System", "purpose": "Restricts beam to a 10 mm diameter pencil beam and rejects Compton-scattered secondary photons."},
                {"name": "NIST-Calibrated 6.0 cc Air-Equivalent Ionization Chamber", "purpose": "Measures exposure and air kerma with ±1% precision and negligible energy dependence."},
                {"name": "Electrometer / Digital Dosimetry Console (Radcal 9010)", "purpose": "Measures integrated ionization charge (nano-Coulombs) and converts to air kerma (μGy)."},
                {"name": "High-Purity Type 1100 Aluminum Filter Sheets (0.5 to 6.0 mm)", "purpose": "Provides certified uniform thickness (±0.01 mm) standard absorbers for HVL testing."}
            ],
            "procedure": [
                {"title": "Cabinet Interlock and Dosimeter Zero Calibration", "text": "Power on the shielded cabinet, zero the electrometer dosimeter, and record background radiation rate to verify complete radiation shielding."},
                {"title": "Generator Technique Standardization", "text": "Set X-ray generator to exactly 80 kVp, 50 mA, 100 ms (5.0 mAs), and verify source-to-detector distance SDD = 100.0 cm."},
                {"title": "Unattenuated Incident Exposure I_0 Measurement", "text": "Fire three calibration exposures through open narrow-beam collimator with zero aluminum filters; record mean unattenuated air kerma I_0 (μGy)."},
                {"title": "Aluminum Filter Step Placement", "text": "Insert a 1.0 mm high-purity aluminum filter plate into the central collimator filter slot and fire identical 80 kVp, 5 mAs exposure."},
                {"title": "Ionization Charge Logging", "text": "Record transmitted air kerma I(x) on the electrometer console and calculate intensity ratio I/I_0."},
                {"title": "Thickness Progression Sequence", "text": "Increment aluminum absorber thickness through 2.0, 3.0, 4.0, 5.0, and 6.0 mm, recording transmitted air kerma at each step."},
                {"title": "Beer-Lambert Semi-Logarithmic Regression", "text": "Plot ln(I/I_0) versus thickness x, extract linear attenuation coefficient μ from the slope, and calculate the Half-Value Layer HVL = 0.6931 / μ."}
            ],
            "topics": [
                {"question": "What is the physical interpretation of the Half-Value Layer (HVL) in radiology?", "answer": "HVL is the thickness of a specified absorbing material (aluminum in diagnostic X-ray, copper in orthovoltage, lead in shielding) that attenuates the air kerma of an X-ray beam by exactly 50%; it serves as the international standard for characterizing beam penetration quality and hardness."},
                {"question": "What is 'beam hardening' in polyenergetic X-ray transmission?", "answer": "A clinical X-ray tube produces a broad spectrum of photon energies. Because low-energy photons are preferentially absorbed by matter (photoelectric effect ∝ 1/E³), the average photon energy of the transmitted beam increases ('hardens') as it penetrates deeper, causing the second HVL to be thicker than the first."},
                {"question": "Why does narrow-beam geometry differ from broad-beam geometry?", "answer": "In narrow-beam geometry, lead collimators reject virtually all Compton-scattered photons, so the detector measures only primary unscattered photons, strictly obeying the exponential Beer-Lambert law; broad-beam geometry allows scattered photons to reach the detector, requiring build-up factors B > 1."},
                {"question": "Why is aluminum universally used as the filtration standard for diagnostic X-rays?", "answer": "Aluminum has an atomic number (Z = 13) and K-edge energy (1.56 keV) well suited to preferentially attenuate low-energy 'soft' X-rays (< 20 keV) that would otherwise be absorbed by the patient's skin without contributing to image formation."},
                {"question": "What is the regulatory minimum HVL for an 80 kVp medical X-ray system?", "answer": "Under US FDA Title 21 CFR and IEC standards, a diagnostic X-ray system operating at 80 kVp must exhibit a minimum half-value layer of at least 2.3 mm of aluminum equivalent to ensure adequate patient radiation protection."},
                {"question": "What are the two dominant physical interaction mechanisms for diagnostic X-rays in tissue?", "answer": "Photoelectric absorption (dominant at lower energies < 30 keV and in high-Z materials like bone and iodinated contrast, scaling as Z³/E³) provides radiographic contrast, while Compton scattering (dominant at higher energies > 30 keV in soft tissue) degrades image quality by creating background scatter fog."}
            ],
            "precautions": [
                "Verify safety interlocks prevent X-ray tube activation whenever the cabinet door is open; radiation safety is paramount.",
                "Ensure narrow-beam collimator apertures are perfectly aligned along the beam central axis to prevent partial penumbra shadowing.",
                "Warm up the X-ray tube with low-dose exposures prior to testing to stabilize the high-voltage generator and focal spot output.",
                "Wait 15 seconds between exposures to allow electrometer reading integration and prevent detector thermal drift."
            ],
            "limitations": [
                "The simple exponential model assumes monoenergetic photons; polyenergetic diagnostic beams exhibit subtle beam hardening curvature over thick filters.",
                "Narrow-beam geometry does not include scattered radiation scatter-to-primary ratios (SPR) present in clinical patient radiography.",
                "Ionization chamber measures air kerma, which approximates absorbed dose in soft tissue but differs in bone or contrast media.",
                "Evaluates aluminum absorbers; human anatomy consists of heterogeneous combinations of fat, muscle, air, and bone."
            ],
            "quiz": [
                {
                    "question": "What mathematical law governs the narrow-beam exponential attenuation of X-ray photons through matter?",
                    "options": ["Beer-Lambert Law (I = I_0 · exp(-μ·x))", "Hooke's Law", "Ohm's Law", "Faraday's Law"],
                    "correct": 0,
                    "explanation": "The Beer-Lambert law describes exponential photon attenuation as a function of linear attenuation coefficient μ and thickness x."
                },
                {
                    "question": "How is the Half-Value Layer (HVL) calculated from the linear attenuation coefficient μ?",
                    "options": ["HVL = ln(2) / μ ≈ 0.693 / μ", "HVL = μ / 2", "HVL = 2 · μ", "HVL = μ²"],
                    "correct": 0,
                    "explanation": "By definition, I / I_0 = 0.5 at x = HVL; therefore, exp(-μ · HVL) = 0.5, yielding HVL = ln(2) / μ ≈ 0.6931 / μ."
                },
                {
                    "question": "If linear attenuation coefficient is μ = 0.2450 mm⁻¹, what is the aluminum Half-Value Layer (HVL)?",
                    "options": ["1.41 mm Al", "2.83 mm Al", "5.66 mm Al", "8.16 mm Al"],
                    "correct": 1,
                    "explanation": "HVL = ln(2) / μ = 0.69315 / 0.2450 mm⁻¹ = 2.829 mm Al ≈ 2.83 mm Al."
                },
                {
                    "question": "What is the primary clinical purpose of adding aluminum filtration to diagnostic X-ray tubes?",
                    "options": ["To remove low-energy 'soft' X-rays that increase patient skin dose without contributing to the image", "To make the X-ray beam visible to the naked eye", "To make X-rays travel faster", "To cool down the room"],
                    "correct": 0,
                    "explanation": "Aluminum filters absorb low-energy photons that would be absorbed in skin without reaching the detector, lowering patient dose."
                }
            ],
            "settings": ["X-Ray tube: 80 kVp, 50 mA, 100 ms (5.0 mAs), rotating tungsten anode", "Geometry: Narrow-beam lead collimation (10 mm aperture), SDD = 100 cm", "Detector: NIST-calibrated 6.0 cc air-equivalent ionization chamber"],
            "samples": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "☢️", "label": "1. Shielded X-Ray Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Beer-Lambert Attenuation"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Beam Hardening Sandbox"}
            ]
        },
        {
            "number": 37,
            "slug": "doppler-ultrasound-flowmeter-frequency-shift",
            "title": "Continuous-Wave Doppler Ultrasound Blood Velocimetry Frequency Shift",
            "shortTitle": "Doppler Ultrasound Velocimetry",
            "aim": "Determine the Doppler frequency shift sensitivity k_d and verify the clinical Doppler ultrasound equation using a blood-mimicking fluid string phantom across flow velocities.",
            "inputLabel": "Target Flow Velocity v",
            "shortInput": "Velocity v",
            "inputUnit": "cm/s",
            "min": 10.0,
            "max": 60.0,
            "step": 10.0,
            "initial": 30.0,
            "inputDecimals": 1,
            "rawLabel": "Doppler Audio Frequency Shift Δf",
            "rawUnit": "Hz",
            "rawDecimals": 2,
            "xAxis": "Flow velocity v (cm/s)",
            "yAxis": "Doppler frequency shift Δf (Hz)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 35.0,
            "emptyY": 1000.0,
            "targetName": "Doppler Velocity Sensitivity Slope k_d",
            "target": "28.5000",
            "refValue": 28.5000,
            "resultUnit": "Hz/(cm/s)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "Δf = k_d · v = 28.5000 · v (at f₀ = 4.0 MHz, θ = 60°)",
            "measureLabel": "Measure Doppler Frequency Shift",
            "intro": "Doppler ultrasound velocimetry is a non-invasive diagnostic technique in clinical vascular surgery, cardiology, and maternal-fetal medicine, enabling quantitative evaluation of carotid artery stenosis, deep vein thrombosis (DVT), and peripheral arterial occlusive disease. The technique exploits the classical Doppler effect: when ultrasound waves emitted by a piezoelectric crystal encounter moving acoustic reflectors (primarily circulating red blood cells), the frequency of the scattered echo is shifted relative to the transmitted carrier frequency f_0. Because the red blood cell acts first as a moving receiver and then as a moving emitter, the frequency shift occurs twice. The clinical Doppler equation is given by: Δf = [2 · f_0 · v · cos(θ)] / c = k_d · v, where Δf is the Doppler frequency shift (Hz), f_0 is the transmitted carrier frequency (typically 2 to 8 MHz), v is blood flow velocity, θ is the Doppler insonation angle between the ultrasound beam and the flow vector, c is the speed of sound in soft tissue (1540 m/s), and k_d is the Doppler sensitivity constant (Hz/(cm/s)). In clinical Doppler systems operating at f_0 = 4.0 MHz and a standard insonation angle θ = 60°, the Doppler shift falls precisely within the human audible spectrum (hundreds to thousands of Hertz), allowing clinicians to listen directly to arterial pulsatility and heart murmur turbulence. In this experiment, a calibrated Doppler string and fluid flow phantom evaluates Doppler frequency shifts across velocities from 10 to 60 cm/s.",
            "modelExtra": "Evaluated using a 4.0 MHz continuous-wave (CW) split-crystal Doppler pencil probe insonating a precision Doppler flow phantom (mimicking carotid blood flow) at an angle of θ = 60.0° in tissue-mimicking fluid (c = 1540 m/s). Theoretical sensitivity k_d = (2 · 4.0×10⁶ · cos(60°)) / (154,000 cm/s) = 25.97 Hz/(cm/s) adjusted for phantom refractive wall geometry to k_d = 28.5000 Hz/(cm/s). Velocities from 10.0 to 60.0 cm/s.",
            "apparatus": [
                {"name": "Calibrated Doppler Ultrasound Fluid Flow Phantom", "purpose": "Provides straight vascular conduit with acoustic tissue-mimicking phantom and certified backscatter."},
                {"name": "4.0 MHz Continuous-Wave (CW) Dual-Crystal Doppler Probe", "purpose": "Contains separate transmit and receive PZT crystals for continuous Doppler telemetry."},
                {"name": "Precision Goniometric Probe Positioning Stage", "purpose": "Sets and maintains exact Doppler insonation angle θ = 60.0° relative to flow lumen axis."},
                {"name": "Microprocessor-Controlled Blood-Mimicking Fluid Pump", "purpose": "Circulates blood-mimicking fluid (BMF) containing nylon micro-particles at certified steady velocities."},
                {"name": "Quadrature Heterodyne Demodulator & Audio Preamplifier", "purpose": "Mixes RF echoes with carrier f_0 to extract in-phase (I) and quadrature (Q) directional audio signals."},
                {"name": "High-Resolution Real-Time Audio Fast Fourier Transform (FFT) Analyzer", "purpose": "Computes power spectral density and identifies modal peak Doppler shift frequency Δf."}
            ],
            "procedure": [
                {"title": "Flow Loop Priming and BMF Verification", "text": "Fill the flow phantom with certified blood-mimicking fluid (nylon scattering particles, density 1050 kg/m³, c = 1540 m/s) and purge all air bubbles."},
                {"title": "Goniometric Doppler Angle Alignment", "text": "Mount the 4.0 MHz CW Doppler probe on the goniometric stage and position probe at precisely θ = 60.0° relative to the flow channel axis."},
                {"title": "Zero Flow Demodulator Calibration", "text": "With the perfusion pump halted, verify zero Doppler audio frequency shift (Δf = 0.0 Hz) and null baseline wall-filter noise."},
                {"title": "Steady Velocity Initialization", "text": "Engage the calibrated pump driver to produce steady centerline flow velocity v = 10.0 cm/s and allow 60 seconds for steady laminar flow."},
                {"title": "FFT Power Spectrum Peak Extraction", "text": "Execute real-time 1024-point FFT spectral analysis on the demodulated Doppler audio stream, averaging 20 spectra to extract peak frequency shift Δf (Hz)."},
                {"title": "Velocity Progression Sequence", "text": "Increment flow delivery through 20.0, 30.0, 40.0, 50.0, and 60.0 cm/s, logging peak Doppler frequency shift Δf at each velocity step."},
                {"title": "Doppler Sensitivity Linear Regression", "text": "Plot Doppler frequency shift Δf versus flow velocity v and determine sensitivity slope k_d via linear regression through the origin."}
            ],
            "topics": [
                {"question": "Why is a factor of 2 present in the clinical Doppler equation?", "answer": "The Doppler shift occurs twice: first, when the moving red blood cell acts as an observer receiving waves from the stationary transducer, and second, when the moving cell acts as an acoustic source scattering waves back to the stationary receiving crystal."},
                {"question": "Why is an insonation angle of 60° considered standard in clinical vascular ultrasound?", "answer": "At 90° (perpendicular), cos(90°) = 0, producing zero Doppler shift. At very shallow angles (< 30°), the ultrasound beam reflects off superficial vessel walls and cannot enter. An angle of 60° provides an optimal compromise between adequate Doppler signal and practical probe orientation."},
                {"question": "What happens to velocity calculation error when the insonation angle exceeds 60°?", "answer": "The derivative of cosine (d(cos θ)/dθ = -sin θ) increases steeply at higher angles; above 60°, a tiny 2° error in probe angle alignment causes enormous percentage errors (> 15–20%) in calculated blood velocity, making angle correction highly unreliable."},
                {"question": "What is the Nyquist limit and aliasing in Pulsed-Wave (PW) Doppler?", "answer": "In PW Doppler, pulses are transmitted at a pulse repetition frequency (PRF). According to the Nyquist sampling theorem, the maximum Doppler shift that can be detected without ambiguity is f_Nyquist = PRF / 2. If blood velocity creates a shift exceeding PRF/2, aliasing occurs, causing high velocities to wrap around and appear in the reverse direction."},
                {"question": "Why does continuous-wave (CW) Doppler never suffer from aliasing?", "answer": "CW Doppler uses separate crystals that transmit and receive continuously rather than in discrete pulses; with no sampling interval, there is no Nyquist limit, allowing CW Doppler to measure arbitrarily high jet velocities (e.g., severe aortic stenosis)."},
                {"question": "How does quadrature demodulation determine whether blood is flowing toward or away from the probe?", "answer": "Quadrature detection splits the received RF signal and mixes it with two reference carriers 90° out of phase (cosine and sine), generating In-phase (I) and Quadrature (Q) baseband signals; the phase lead or lag between I and Q reveals whether flow is forward or reverse."}
            ],
            "precautions": [
                "Maintain probe insonation angle at exactly 60.0°; angle misalignment introduces severe cosine scaling errors.",
                "Verify acoustic coupling with generous ultrasound transmission gel; air gaps completely reflect the 4.0 MHz acoustic wave.",
                "Set the electronic wall filter (high-pass filter) to low (~50 Hz) to eliminate vessel wall motion artifacts without clipping low-velocity blood signals.",
                "Ensure blood-mimicking fluid particles remain fully suspended without gravitational settling."
            ],
            "limitations": [
                "The linear Doppler relation applies across laminar velocities; severe turbulent flow creates broad spectral broadening rather than a single discrete shift.",
                "CW Doppler has no range resolution; it measures all moving reflectors along the entire acoustic beam line of sight.",
                "Assumes uniform insonation across the lumen, whereas parabolic flow profiles produce a spectrum of velocities from zero to peak.",
                "Refraction at the vessel wall-tissue interface can alter the true internal insonation angle slightly from the external probe angle."
            ],
            "quiz": [
                {
                    "question": "What happens to the Doppler frequency shift if the ultrasound beam is positioned exactly perpendicular (90°) to blood flow?",
                    "options": ["The Doppler shift drops to zero because cos(90°) = 0", "The Doppler shift reaches maximum", "The probe explodes", "The blood stops flowing"],
                    "correct": 0,
                    "explanation": "Because cos(90°) = 0, no relative velocity component exists along the acoustic beam axis, yielding zero Doppler frequency shift."
                },
                {
                    "question": "Why do Doppler ultrasound frequency shifts produce sounds that can be heard through audio speakers?",
                    "options": ["At medical ultrasound frequencies (2–8 MHz), blood velocities generate frequency shifts in the audible range (20 Hz to 15 kHz)", "Because red blood cells scream", "Because ultrasound is loud", "Because the computer synthesizes music"],
                    "correct": 0,
                    "explanation": "Doppler frequency shifts for physiological blood velocities typically range from a few hundred Hz to several kHz, falling squarely in the audible human hearing range."
                },
                {
                    "question": "If flow velocity is v = 40.0 cm/s and measured Doppler shift is Δf = 1140.0 Hz, what is sensitivity k_d?",
                    "options": ["14.25 Hz/(cm/s)", "28.50 Hz/(cm/s)", "57.00 Hz/(cm/s)", "114.0 Hz/(cm/s)"],
                    "correct": 1,
                    "explanation": "k_d = Δf / v = 1140.0 Hz / 40.0 cm/s = 28.5000 Hz/(cm/s)."
                },
                {
                    "question": "What is the primary advantage of Continuous-Wave (CW) Doppler over Pulsed-Wave (PW) Doppler?",
                    "options": ["CW Doppler has no Nyquist limit and cannot alias, allowing measurement of extremely high velocities", "CW Doppler produces 3D color pictures", "CW Doppler uses less power", "CW Doppler requires no coupling gel"],
                    "correct": 0,
                    "explanation": "CW Doppler samples continuously without pulsing, eliminating the Nyquist sampling limit and preventing velocity aliasing."
                }
            ],
            "settings": ["Transducer: 4.0 MHz continuous-wave split-crystal Doppler pencil probe", "Insonation: Precision goniometer set to θ = 60.0°", "Fluid: Certified blood-mimicking fluid (nylon scatterers, c = 1540 m/s)"],
            "samples": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "📟", "label": "1. Doppler Flow Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Frequency Shift vs Velocity"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Doppler Equation Sandbox"}
            ]
        },
        {
            "number": 38,
            "slug": "mri-spin-lattice-relaxation-t1-inversion-recovery",
            "title": "Magnetic Resonance Imaging (MRI) Spin-Lattice Relaxation T₁ Mapping",
            "shortTitle": "MRI T₁ Inversion Recovery",
            "aim": "Determine the longitudinal spin-lattice relaxation rate constant k_t and calculate T₁ relaxation time of a biological tissue phantom using an MRI inversion recovery pulse sequence.",
            "inputLabel": "Inversion Time Delay TI",
            "shortInput": "Inversion TI",
            "inputUnit": "ms",
            "min": 100.0,
            "max": 600.0,
            "step": 100.0,
            "initial": 300.0,
            "inputDecimals": 1,
            "rawLabel": "Normalized Longitudinal Magnetization M_z/M₀",
            "rawUnit": "ratio",
            "rawDecimals": 4,
            "xAxis": "Inversion time TI (ms)",
            "yAxis": "Normalized longitudinal magnetization M_z/M₀ (ratio)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 350.0,
            "emptyY": -0.45,
            "targetName": "Inversion Recovery Initial Slope k_t",
            "target": "0.00145",
            "refValue": 0.00145,
            "resultUnit": "ms⁻¹",
            "resultDecimals": 5,
            "resultScale": 1.0,
            "fitEquation": "M_z/M₀ = k_t · TI - 0.9500 = 0.00145 · TI - 0.9500",
            "measureLabel": "Execute MRI Inversion Sequence",
            "intro": "Magnetic Resonance Imaging (MRI) is a non-invasive diagnostic imaging modality that provides exquisite soft-tissue anatomical and functional contrast based on the nuclear magnetic resonance (NMR) properties of hydrogen protons (¹H) in water and lipids. In a strong static magnetic field B_0, proton nuclear spins align with the field, establishing a net macroscopic equilibrium longitudinal magnetization M_0. When excited by radiofrequency (RF) pulses, proton spins absorb energy and perturb away from equilibrium. The recovery of longitudinal magnetization back toward thermal equilibrium along the z-axis is governed by the Bloch equation for spin-lattice (T₁) relaxation: dM_z/dt = -(M_z - M_0) / T_1, where T_1 is the longitudinal relaxation time representing energy dissipation from spinning nuclei to the surrounding thermal molecular lattice. The gold-standard pulse sequence for measuring T_1 is the Inversion Recovery (IR) sequence: a 180° RF pulse inverts longitudinal magnetization to -M_0, followed after an inversion time delay TI by a 90° readout pulse that tips remaining M_z into the transverse plane for signal detection. The theoretical recovery equation is M_z(TI) / M_0 = 1 - 2 · exp(-TI / T_1). For short-to-intermediate inversion times (TI ≪ T_1), the exponential recovery expands via Taylor series into a linear relation: M_z(TI) / M_0 ≈ -1 + (2 / T_1) · TI = k_t · TI - 0.9500, where k_t = 2 / T_1 is the initial recovery slope (ms⁻¹). In this laboratory investigation, an instrumented benchtop NMR/MRI spectrometer evaluates an aqueous copper sulfate biological tissue phantom across inversion times from 100 to 600 ms to map T_1.",
            "modelExtra": "Evaluated on a benchtop 1.0 Tesla permanent-magnet NMR/MRI spectrometer (Larmor frequency f_0 = 42.58 MHz for ¹H) using an aqueous CuSO₄ doped tissue phantom at 22 °C. Repetition time TR = 5000 ms ensures full equilibrium recovery between shots. Linear inversion recovery slope k_t = 0.00145 ms⁻¹ yields an empirical T_1 ≈ 2 / k_t = 1379 ms across inversion times TI from 100 to 600 ms.",
            "apparatus": [
                {"name": "Benchtop 1.0 Tesla Permanent-Magnet NMR/MRI Spectrometer", "purpose": "Provides highly homogeneous 1.000 T static magnetic field (B_0) with 42.58 MHz ¹H Larmor frequency."},
                {"name": "Precision RF Transceiver Coil & Resonant Probe Head", "purpose": "Transmits calibrated 180° inversion and 90° excitation RF pulses and detects FID echo signals."},
                {"name": "Aqueous Copper Sulfate (CuSO₄) Tissue-Mimicking Phantom", "purpose": "Standardized paramagnetic NMR calibration phantom with stable T_1 relaxation (~1380 ms)."},
                {"name": "Microprocessor Pulse Programmer Console", "purpose": "Generates precise RF pulse timing sequences with sub-microsecond inversion delay accuracy."},
                {"name": "Quadrature Phase-Sensitive RF Receiver", "purpose": "Demodulates high-frequency FID signals into real and imaginary baseband components."},
                {"name": "Thermostatically Controlled RF Probe Chamber (22.0 ± 0.1 °C)", "purpose": "Stabilizes sample temperature preventing temperature-dependent relaxation drift."}
            ],
            "procedure": [
                {"title": "Magnet Thermal Stabilization and Shimming", "text": "Power on permanent magnet temperature controller, allow 30 minutes for thermal stabilization, and adjust active gradient shim coils to achieve linewidth < 5 Hz."},
                {"title": "90° and 180° RF Pulse Duration Calibration", "text": "Execute nutation pulse sweep to determine exact RF pulse widths for 90° excitation (typically 6.5 μs) and 180° inversion (13.0 μs)."},
                {"title": "Sample Loading and Thermal Equilibration", "text": "Insert 5 mm NMR sample tube containing aqueous CuSO₄ phantom into probe coil and allow 10 minutes for thermal equilibration at 22.0 °C."},
                {"title": "Inversion Recovery Sequence Execution", "text": "Set repetition time TR = 5000 ms (> 3 · T_1) and apply 180° inversion pulse; after inversion time delay TI = 100 ms, apply 90° readout pulse."},
                {"title": "FID Amplitude Integration", "text": "Digitize the free induction decay (FID) signal, perform phase correction, and record initial FID amplitude as proportional to M_z(TI)."},
                {"title": "Inversion Time Progression Sequence", "text": "Increment inversion delay TI through 200, 300, 400, 500, and 600 ms, capturing normalized longitudinal magnetization M_z/M_0 at each step."},
                {"title": "T_1 Relaxation Rate Linear Regression", "text": "Plot normalized magnetization M_z/M_0 versus inversion time TI, extract initial slope k_t, and compute spin-lattice relaxation time T_1 = 2 / k_t."}
            ],
            "topics": [
                {"question": "What is the physical difference between T_1 and T_2 relaxation in MRI?", "answer": "T_1 (spin-lattice) relaxation involves energy exchange between proton nuclear spins and the surrounding molecular thermal environment, restoring longitudinal magnetization along the z-axis; T_2 (spin-spin) relaxation involves loss of phase coherence among transverse spins due to local magnetic field fluctuations without energy dissipation to the lattice, destroying transverse magnetization (T_2 is always ≤ T_1)."},
                {"question": "What is the 'null point' in an inversion recovery sequence and how is it used clinically?", "answer": "The null point is the specific inversion time TI_null where recovering longitudinal magnetization passes through zero (M_z = 0, where TI_null = T_1 · ln 2 ≈ 0.693 · T_1). Applying a 90° pulse at this exact moment produces zero signal, allowing selective tissue suppression (e.g., STIR suppresses fat; FLAIR suppresses cerebrospinal fluid)."},
                {"question": "How do paramagnetic contrast agents (e.g., Gadolinium-DTPA) enhance MRI images?", "answer": "Gadolinium ions possess seven unpaired inner-shell electrons that generate large fluctuating local magnetic fields; when water molecules coordinate with gadolinium, their proton T_1 relaxation rate is drastically accelerated (higher 1/T_1 relaxivity), producing bright hyperintense signal on T_1-weighted scans."},
                {"question": "Why does free water have a much longer T_1 than bound water or lipids?", "answer": "Small free water molecules tumble rapidly (picosecond correlation times) far above the megahertz Larmor frequency, making energy transfer inefficient and yielding long T_1 (> 3000 ms); structured lipids and tissue-bound water tumble near the Larmor frequency, enabling efficient energy transfer and yielding short T_1 (~200–800 ms)."},
                {"question": "Why must the repetition time TR be set to at least 3 to 5 times T_1 in inversion recovery?", "answer": "If TR is too short, longitudinal magnetization does not fully recover to equilibrium (+M_0) before the next 180° pulse, causing progressive saturation that leads to severe underestimation of T_1."},
                {"question": "What is the Larmor equation in magnetic resonance?", "answer": "The Larmor equation f_0 = (γ / 2π) · B_0 dictates that the precessional frequency of nuclear spins is directly proportional to the applied magnetic field strength B_0, where γ is the gyromagnetic ratio (42.58 MHz/Tesla for ¹H protons)."}
            ],
            "precautions": [
                "Ensure repetition time TR is at least 5000 ms to guarantee full longitudinal relaxation recovery between successive inversion cycles.",
                "Calibrate the 180° inversion RF pulse width accurately; incomplete inversion leaves residual transverse magnetization that corrupts T_1.",
                "Maintain constant magnet temperature; thermal drift in permanent magnets shifts B_0 and detunes the RF resonance frequency.",
                "Perform phase-sensitive detection so that inverted signals are correctly recorded as negative amplitudes."
            ],
            "limitations": [
                "The linear approximation applies to initial inversion times (TI ≤ 600 ms); full recovery curves require three-parameter non-linear fitting.",
                "Assumes a single mono-exponential T_1, whereas complex biological tissues (e.g., brain white matter) display multi-compartment water pools.",
                "Long TR requirements make standard inversion recovery slow; clinical scanners use accelerated Look-Locker or MOLLI sequences.",
                "RF transmit field B_1 inhomogeneity can cause non-uniform inversion flip angles across large imaging volumes."
            ],
            "quiz": [
                {
                    "question": "What physical process does T_1 relaxation represent in magnetic resonance physics?",
                    "options": ["Spin-lattice relaxation: transfer of energy from proton spins to the thermal molecular lattice", "Radioactive decay of atomic nuclei", "Melting of ice inside the magnet", "Static electricity buildup on the patient"],
                    "correct": 0,
                    "explanation": "T_1 (spin-lattice) relaxation describes the exponential recovery of longitudinal magnetization as spins transfer absorbed RF energy to the surrounding lattice."
                },
                {
                    "question": "What clinical MRI sequence uses an inversion pulse to completely suppress fluid signal (CSF) in brain imaging?",
                    "options": ["FLAIR (Fluid-Attenuated Inversion Recovery)", "DWI (Diffusion Weighted Imaging)", "CT Angiography", "X-ray Fluoroscopy"],
                    "correct": 0,
                    "explanation": "FLAIR sets inversion time TI to the null point of cerebrospinal fluid (CSF), completely nulling CSF signal to highlight periventricular brain lesions."
                },
                {
                    "question": "If the initial inversion recovery slope is k_t = 0.00145 ms⁻¹, what is the estimated T_1 relaxation time (T_1 ≈ 2 / k_t)?",
                    "options": ["690 ms", "1379 ms", "2000 ms", "2758 ms"],
                    "correct": 1,
                    "explanation": "T_1 = 2 / k_t = 2 / 0.00145 ms⁻¹ = 1379.3 ms ≈ 1379 ms."
                },
                {
                    "question": "What happens to the sign of longitudinal magnetization immediately following an ideal 180° RF pulse?",
                    "options": ["Magnetization inverts from +M_0 to -M_0", "Magnetization doubles to +2M_0", "Magnetization drops permanently to zero", "Magnetization rotates backwards in time"],
                    "correct": 0,
                    "explanation": "An ideal 180° inversion pulse completely flips longitudinal magnetization upside down along the negative z-axis (-M_0)."
                }
            ],
            "settings": ["Field: 1.0 Tesla permanent magnet (B_0 = 1.000 T, ¹H f_0 = 42.58 MHz)", "Sequence: Inversion Recovery (180° - TI - 90°), TR = 5000 ms", "Phantom: Aqueous CuSO₄ paramagnetic tissue phantom at 22.0 °C"],
            "samples": [100.0, 200.0, 300.0, 400.0, 500.0, 600.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🧲", "label": "1. Benchtop MRI Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Inversion Recovery M_z(TI)"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Bloch Equation Sandbox"}
            ]
        },
        {
            "number": 39,
            "slug": "cardiac-pacemaker-pulse-generator-chronaxie-strength-duration",
            "title": "Implantable Cardiac Pacemaker Lapicque Strength-Duration & Chronaxie Curve",
            "shortTitle": "Pacemaker Strength-Duration",
            "aim": "Determine the chronaxie time t_ch and rheobase voltage V_rh of an implantable cardiac pacemaker lead-tissue interface across pulse widths using the Lapicque-Weiss model.",
            "inputLabel": "Pacing Pulse Duration t_p",
            "shortInput": "Pulse Width t_p",
            "inputUnit": "ms",
            "min": 0.20,
            "max": 1.00,
            "step": 0.15,
            "initial": 0.50,
            "inputDecimals": 2,
            "rawLabel": "Pacing Capture Threshold Voltage V_th",
            "rawUnit": "V",
            "rawDecimals": 4,
            "xAxis": "Inverse pulse duration 1/t_p (ms⁻¹)",
            "yAxis": "Threshold voltage V_th (V)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.0,
            "emptyY": 1.5,
            "targetName": "Lapicque Slope Parameter m_ch",
            "target": "0.3200",
            "refValue": 0.3200,
            "resultUnit": "V·ms",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "V_th = m_ch · (1/t_p) + V_rh = 0.3200 · (1/t_p) + 0.6500",
            "measureLabel": "Determine Pacing Capture Threshold",
            "intro": "Implantable cardiac pacemakers are life-sustaining electronic medical devices that treat symptomatic bradyarrhythmias, high-grade atrioventricular (AV) blocks, and sick sinus syndrome by delivering timed electrical stimulation pulses to myocardial tissue. The electrical excitability of excitable cardiac cell membranes is governed by the classic neurostimulation principles formulated by Louis Lapicque and Georges Weiss. To trigger an action potential that propagates across the myocardium and initiates coordinated ventricular contraction ('capture'), the delivered electrical pulse must depolarize the cell membrane from its resting potential (-85 mV) to its threshold potential (-65 mV). The minimum stimulation voltage V_th required for capture depends on pulse duration t_p according to the Lapicque strength-duration relationship: V_th = V_rh · (1 + t_ch / t_p) = (V_rh · t_ch) · (1 / t_p) + V_rh = m_ch · (1 / t_p) + V_rh, where V_rh is the rheobase voltage (the asymptotic minimum voltage threshold at infinitely long pulse width), t_ch is the chronaxie time (the pulse duration required to achieve capture at exactly twice the rheobase voltage: V_th = 2 · V_rh), and m_ch = V_rh · t_ch is the Lapicque slope constant (V·ms). In clinical pacemaker programming, setting pulse width near the chronaxie (typically 0.4 to 0.5 ms for modern steroid-eluting steroid collar leads) optimizes battery longevity by minimizing delivered pacing energy (E = V² · t_p / R). In this experiment, an instrumented cardiac electrophysiology simulator evaluates pacemaker threshold voltages across pulse durations from 0.2 to 1.0 ms.",
            "modelExtra": "Evaluated on a Medtronic clinical cardiac pulse generator interfaced with a steroid-eluting active-fixation bipolar endocardial pacing lead (tip area 1.2 mm², pacing impedance R = 550 Ω) immersed in 37.0 °C physiological saline. Rheobase voltage V_rh = 0.6500 V, chronaxie time t_ch = 0.4923 ms, yielding Lapicque slope m_ch = 0.3200 V·ms across pulse widths t_p from 0.20 to 1.00 ms (1/t_p from 5.0 to 1.0 ms⁻¹).",
            "apparatus": [
                {"name": "Clinical Implantable Cardiac Pacemaker Pulse Generator", "purpose": "Provides programmable constant-voltage pacing pulses with telemetry programming head."},
                {"name": "Steroid-Eluting Bipolar Endocardial Pacing Lead (1.2 mm² tip)", "purpose": "Provides platinized titanium pacing electrode with dexamethasone sodium phosphate elution."},
                {"name": "Cardiac Tissue Impedance & Evoked Response Simulator", "purpose": "Simulates 550 Ω tissue impedance and generates evoked R-wave action potential upon capture."},
                {"name": "High-Speed Isolated Digital Storage Oscilloscope (100 MS/s)", "purpose": "Measures delivered voltage pulse amplitudes and duration with sub-microsecond accuracy."},
                {"name": "Pacemaker RF Telemetry Programming Wand", "purpose": "Adjusts pulse duration t_p and executes automated threshold search algorithms via wireless RF telemetry."},
                {"name": "Thermostatically Controlled Saline Tissue Bath (37.0 °C)", "purpose": "Maintains physiological temperature and electrolyte conductance matching human blood."}
            ],
            "procedure": [
                {"title": "Pacing Lead Bath Mounting and Impedance Verification", "text": "Submerge bipolar pacing lead tip in 37.0 °C saline, connect to pacing simulator, and verify pacing impedance R = 550 ± 20 Ω via telemetry."},
                {"title": "Telemetry Programmer Interrogation", "text": "Position wireless programming wand over pacemaker, establish bidirectional telemetry link, and select automated capture threshold testing mode."},
                {"title": "Initial Pulse Width Configuration", "text": "Program pacemaker pulse duration to t_p = 0.20 ms (inverse width 1/t_p = 5.00 ms⁻¹)."},
                {"title": "Capture Threshold Voltage Search", "text": "Step pacing voltage downward from 3.0 V in 0.05 V increments until evoked electrical response ceases, recording last successful capture voltage as V_th."},
                {"title": "Pulse Width Progression Sequence", "text": "Increment pulse width through 0.25 ms (1/t_p = 4.00), 0.333 ms (3.00), 0.50 ms (2.00), 0.667 ms (1.50), and 1.00 ms (1.00 ms⁻¹), measuring capture threshold V_th at each setting."},
                {"title": "Lapicque-Weiss Linear Regression Analysis", "text": "Plot threshold voltage V_th versus inverse pulse width 1/t_p, extract slope m_ch and y-intercept V_rh, and calculate chronaxie time t_ch = m_ch / V_rh."}
            ],
            "topics": [
                {"question": "What is the physical definition of rheobase voltage and chronaxie time?", "answer": "Rheobase is the absolute minimum electrical potential required to elicit an action potential at infinitely long pulse duration; chronaxie is the specific pulse duration at which the threshold voltage is exactly twice the rheobase voltage (V_th = 2 · V_rh)."},
                {"question": "Why is the chronaxie pulse width considered the energy-optimal setting for pacemaker programming?", "answer": "Delivered pacing energy is E = V²·t_p / R. At very short pulse widths, required voltage rises sharply, causing high V² energy loss; at very long pulse widths, extra duration wastes energy after the cell has already depolarized. Mathematical optimization proves that delivered pacing energy reaches a minimum near t_p ≈ chronaxie (typically 0.4 to 0.5 ms)."},
                {"question": "How do steroid-eluting pacing leads lower chronic pacing thresholds?", "answer": "Mechanical insertion of a lead causes local foreign-body trauma, acute inflammation, and fibrous capsule formation around the electrode tip. A slow-eluting steroid (dexamethasone) suppresses local inflammation and minimizes fibrous scar tissue thickness, reducing the effective pacing radius and lowering chronic capture thresholds by > 50%."},
                {"question": "What is the difference between unipolar and bipolar pacing configurations?", "answer": "In unipolar pacing, the cathode is the lead tip in contact with myocardium and the anode is the metallic pacemaker casing (can), creating large pacing spikes on surface ECG but risking pectoral muscle twitching; in bipolar pacing, both cathode (tip) and anode (ring) are on the lead tip inside the heart, eliminating pectoral stimulation and reducing electromagnetic interference (EMI)."},
                {"question": "What is automated capture management (AutoCapture) in modern pacemakers?", "answer": "AutoCapture delivers a pacing pulse, listens for an evoked myocardial response (depolarization wave) within a 50 ms window, delivers a high-voltage safety backup pulse if capture is lost, and periodically recalibrates the threshold, maintaining a safe 0.3 V safety margin to dramatically extend battery life."},
                {"question": "What is pacemaker lead maturation and how does threshold change over time?", "answer": "Immediately post-implant, thresholds are low (~0.5 V); over 1 to 3 weeks, acute inflammation causes thresholds to rise to a peak (peaking phase); after 6 to 12 weeks, steroid elution resolves inflammation, stabilizing the chronic threshold at a low, permanent baseline."}
            ],
            "precautions": [
                "Always maintain a clinical safety margin (typically programming output voltage to at least 2 times capture threshold or 3 times safety margin) to prevent loss of capture.",
                "Ensure pacemaker lead tip is fully submerged in physiological saline to prevent electrode polarization artifacts.",
                "Verify oscilloscope input impedance is > 1 MΩ to avoid loading the pacemaker output circuit.",
                "Allow 10 pacing cycles at each voltage step during threshold testing to ensure 100% reliable myocardial capture."
            ],
            "limitations": [
                "The Lapicque-Weiss model assumes a simple parallel R-C membrane circuit, neglecting active voltage-gated sodium channel reactivation dynamics.",
                "In-vitro saline testing uses a fixed resistor-capacitor network; living human myocardium exhibits time-varying non-linear polarization impedances.",
                "Evaluates acute thresholds; does not model chronic fibrous capsule remodeling or post-operative threshold maturation.",
                "Does not simulate autonomic tone variations (exercise, circadian catecholamine surges) that alter in-vivo myocardial excitability."
            ],
            "quiz": [
                {
                    "question": "What is the chronaxie time in cardiac electrostimulation?",
                    "options": ["The pulse duration required to stimulate tissue at exactly twice the rheobase voltage", "The time required to recharge the pacemaker battery", "The lifespan of a pacing lead", "The duration of an atrial contraction"],
                    "correct": 0,
                    "explanation": "Chronaxie is defined as the pulse duration at which the threshold stimulation voltage is exactly double the rheobase voltage."
                },
                {
                    "question": "Why is the pacemaker pulse duration typically programmed near the chronaxie (0.4 to 0.5 ms)?",
                    "options": ["It minimizes delivered pacing energy (E = V²·t/R), maximizing pacemaker battery longevity", "It makes the heart beat faster", "It prevents battery explosion", "It is the only setting allowed by law"],
                    "correct": 0,
                    "explanation": "Pacing at or near the chronaxie time minimizes electrical energy consumption per pulse, extending pacemaker battery lifespan."
                },
                {
                    "question": "If rheobase is V_rh = 0.650 V and Lapicque slope is m_ch = 0.320 V·ms, what is threshold V_th at pulse width t_p = 0.50 ms (1/t_p = 2.0 ms⁻¹)?",
                    "options": ["0.970 V", "1.290 V", "1.610 V", "2.250 V"],
                    "correct": 1,
                    "explanation": "V_th = m_ch · (1/t_p) + V_rh = 0.320 · 2.0 + 0.650 = 0.640 + 0.650 = 1.2900 V."
                },
                {
                    "question": "What is the purpose of eluting a corticosteroid (dexamethasone) from the tip of modern pacing leads?",
                    "options": ["To suppress post-implant fibrous scar tissue formation, keeping chronic capture thresholds low", "To numb heart pain", "To dissolve blood clots", "To power the microchip"],
                    "correct": 0,
                    "explanation": "Steroid elution suppresses the inflammatory foreign-body reaction, minimizing fibrous capsule thickness and maintaining low capture thresholds."
                }
            ],
            "settings": ["Pacemaker: Medtronic clinical pulse generator with telemetry programming wand", "Lead: Steroid-eluting bipolar endocardial lead (1.2 mm² tip, R = 550 Ω)", "Bath: 37.0 °C physiological saline with evoked response cardiac simulator"],
            "samples": [0.20, 0.25, 0.3333, 0.50, 0.6667, 1.00],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "⚡", "label": "1. Pacemaker Test Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Strength-Duration Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Lapicque-Weiss Sandbox"}
            ]
        },
        {
            "number": 40,
            "slug": "external-defibrillator-rlc-damped-sinusoidal-pulse",
            "title": "External Defibrillator RLC Damped Sinusoidal Discharge & Transthoracic Impedance",
            "shortTitle": "Defibrillator Transthoracic Discharge",
            "aim": "Evaluate the peak discharge current I_peak of a clinical external defibrillator across human transthoracic impedances (TTI) using an RLC damped sinusoidal circuit.",
            "inputLabel": "Patient Transthoracic Impedance R_th",
            "shortInput": "Impedance R_th",
            "inputUnit": "Ω",
            "min": 30.0,
            "max": 105.0,
            "step": 15.0,
            "initial": 60.0,
            "inputDecimals": 1,
            "rawLabel": "Peak Defibrillation Discharge Current I_peak",
            "rawUnit": "A",
            "rawDecimals": 3,
            "xAxis": "Transthoracic impedance R_th (Ω)",
            "yAxis": "Peak discharge current I_peak (A)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 65.0,
            "emptyY": 45.0,
            "targetName": "Current-Impedance Sensitivity Slope k_r",
            "target": "0.3500",
            "refValue": 0.3500,
            "resultUnit": "A/Ω",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "I_peak = -k_r · R_th + I_0 = -0.3500 · R_th + 68.0000",
            "measureLabel": "Discharge Defibrillator Pulse",
            "intro": "Ventricular fibrillation (VF) is a lethal cardiac arrhythmia characterized by disorganized, chaotic electrical depolarization of ventricular myocytes, causing loss of coordinated mechanical pumping, immediate cessation of cardiac output, and sudden cardiac death within minutes. External defibrillation is the definitive clinical treatment, delivering a controlled electrical shock across the thoracic chest to simultaneously depolarize a critical mass (> 75–90%) of myocardium, extinguish re-entrant wavelets, and allow the intrinsic sinoatrial node to re-establish normal sinus rhythm. In classical Lown and Edmark RLC defibrillators, a high-voltage capacitor C (typically 32 to 50 μF) charged up to several thousand volts (1500 to 5000 V, delivering 200 to 360 Joules) discharges through an internal series inductor L (~50 to 100 mH) and the patient's transthoracic impedance R_th. The governing differential equation of the series RLC circuit is L · (d²i/dt²) + R_th · (di/dt) + i/C = 0. In human clinical resuscitation, transthoracic impedance R_th varies widely (from 25 to 150 Ω) depending on body mass, chest hair, electrode size, coupling gel, and electrode paddle contact pressure. Because higher patient impedance dampens the discharge waveform, the peak delivered electrical current I_peak scales inversely with patient impedance: I_peak = -k_r · R_th + I_0, where k_r is the impedance sensitivity constant (A/Ω). In this laboratory investigation, an instrumented high-voltage defibrillator test analyzer evaluates discharge currents across standardized non-inductive load resistors from 30 to 105 Ω.",
            "modelExtra": "Evaluated on a clinical external defibrillator set to 200 Joules delivered energy (internal storage capacitor C = 32 μF charged to V_0 = 3600 V, internal choke inductor L = 50 mH, internal coil resistance r_i = 12 Ω). Discharging into precision non-inductive load resistors representing patient transthoracic impedance R_th from 30.0 to 105.0 Ω. Linear peak current slope k_r = 0.3500 A/Ω with intercept I_0 = 68.0000 A.",
            "apparatus": [
                {"name": "Clinical High-Energy External Defibrillator Unit", "purpose": "Delivers calibrated 200 J defibrillation shocks with synchronized cardioversion capability."},
                {"name": "High-Voltage Defibrillator Analyzer & Load Bank (Fluke Impulse 7000DP)", "purpose": "Provides certified non-inductive load resistances (30 to 105 Ω) and measures pulse energy, current, and voltage."},
                {"name": "Calibrated 1000:1 High-Voltage Passive Probe (Tektronix P6015A)", "purpose": "Scales kilovolt discharge waveforms safely for digital oscilloscope acquisition (75 MHz bandwidth)."},
                {"name": "Fast Current Transformer / Rogowski Coil (100 A full scale)", "purpose": "Measures peak discharge current I_peak with sub-microsecond rise-time response."},
                {"name": "Self-Adhesive Adult Defibrillation Electrode Pads (80 cm²)", "purpose": "Standard hydrogel-coated clinical electrode pads designed for anterolateral chest placement."},
                {"name": "High-Speed Isolated Digital Storage Oscilloscope (200 MS/s)", "purpose": "Digitizes high-voltage damped sinusoidal current and voltage discharge waveforms."}
            ],
            "procedure": [
                {"title": "High-Voltage Safety and Analyzer Setup", "text": "Connect defibrillator paddle cables to high-voltage analyzer load bank; verify equipment grounding and post high-voltage safety warning signage."},
                {"title": "Defibrillator Energy Selection", "text": "Power on defibrillator and select standard adult energy level: 200 Joules delivered into 50 Ω."},
                {"title": "Transthoracic Load Resistance Initialization", "text": "Configure analyzer precision non-inductive load resistance to R_th = 30.0 Ω and arm the measurement digitizer."},
                {"title": "Capacitor Charging and Discharge Execution", "text": "Charge the internal capacitor bank to full 200 J potential; clear the testing perimeter and depress the shock discharge button."},
                {"title": "Peak Discharge Current Capture", "text": "Capture the damped sinusoidal current waveform on the analyzer oscilloscope and record peak current I_peak (A) and total delivered energy (J)."},
                {"title": "Transthoracic Impedance Progression", "text": "Increment load resistance through 45.0, 60.0, 75.0, 90.0, and 105.0 Ω, executing standardized 200 J discharges and recording peak current at each step."},
                {"title": "Current-Impedance Sensitivity Regression", "text": "Plot peak discharge current I_peak versus transthoracic impedance R_th and calculate sensitivity slope k_r and zero-impedance current I_0 via linear regression."}
            ],
            "topics": [
                {"question": "Why is peak electrical current I_peak critical for successful defibrillation?", "answer": "Myocardial cell depolarization is driven by electric field intensity and current density traversing cardiac tissue, not by stored voltage or nominal energy alone; if high patient impedance reduces current below ~15–20 A, defibrillation fails regardless of delivered Joules."},
                {"question": "How does an RLC damped sinusoidal (Lown) waveform differ from a modern Biphasic Truncated Exponential (BTE) waveform?", "answer": "An RLC damped sinusoidal waveform delivers a single-direction current pulse shaped by a heavy inductor; modern BTE defibrillators use solid-state H-bridge switching to deliver an initial positive current pulse followed by an inverted negative pulse, achieving successful defibrillation at significantly lower energies (150 J vs 360 J) and causing less myocardial damage."},
                {"question": "What factors influence human transthoracic impedance (TTI) during clinical resuscitation?", "answer": "TTI is lowered by larger electrode pad surface area, conductive electrode hydrogel, firm paddle pressure (firm pressure expels air from the lungs, lowering impedance by up to 20%), shaving chest hair, and delivering repeated shocks in rapid succession."},
                {"question": "What is the physical function of the series inductor (choke) in an RLC defibrillator?", "answer": "Without an inductor, discharging a high-voltage capacitor directly into a human chest would produce a lethal instantaneous current spike (thousands of amperes with microsecond rise time) that denatures myocardial proteins and causes severe cardiac burns; the inductor limits di/dt, shaping a smooth, rounded millisecond pulse."},
                {"question": "What is the difference between defibrillation and synchronized cardioversion?", "answer": "Defibrillation delivers an unsynchronized high-energy shock at any moment in the cardiac cycle (used for pulseless VF and pulseless VT); synchronized cardioversion detects the ECG R-wave and fires the shock exactly on the R-wave peak to avoid the vulnerable T-wave period, which could otherwise induce ventricular fibrillation (R-on-T phenomenon)."},
                {"question": "Why must defibrillator test banks use non-inductive resistors?", "answer": "Standard wire-wound power resistors have significant parasitic inductance that distorts high-voltage pulse rise times and alters RLC resonant damping; non-inductive metal-oxide or carbon composition resistors guarantee pure resistive impedance."}
            ],
            "precautions": [
                "High-voltage electrical hazard: Defibrillator discharges deliver kilovolt pulses; never touch test leads or analyzer contacts during firing.",
                "Ensure analyzer load resistors are non-inductive and rated for high peak pulse energy (minimum 500 J surge capacity).",
                "Allow 30 seconds between successive high-energy discharges to prevent thermal buildup in the internal defibrillator components and load bank.",
                "Verify high-voltage probe ground lead is securely bonded to analyzer ground to prevent hazardous floating chassis potentials."
            ],
            "limitations": [
                "The linear current-impedance model applies across normal clinical human adult impedances (30 to 105 Ω); extreme impedances exhibit non-linear RLC damping transitions.",
                "Pure resistive load banks simulate real impedance, neglecting the small capacitive phase shifts present in biological human skin-electrode interfaces.",
                "Evaluates static resistance, whereas living human tissue impedance decreases dynamically by 5–10% during the high-voltage discharge itself.",
                "Does not model internal multi-dimensional thoracic current path distributions through lungs, myocardium, and skeletal muscle."
            ],
            "quiz": [
                {
                    "question": "What is the primary lethal cardiac arrhythmia that requires immediate electrical defibrillation?",
                    "options": ["Ventricular Fibrillation (VF)", "Sinus Bradycardia", "First-Degree AV Block", "Premature Atrial Contraction"],
                    "correct": 0,
                    "explanation": "Ventricular Fibrillation is chaotic electrical quivering of the ventricles with zero cardiac output; immediate defibrillation is life-saving."
                },
                {
                    "question": "What happens to the peak discharge current I_peak delivered to a patient if transthoracic impedance R_th increases?",
                    "options": ["Peak current decreases proportionally", "Peak current increases exponentially", "Peak current remains exactly identical", "Peak current reverses direction"],
                    "correct": 0,
                    "explanation": "According to Ohm's law and RLC damping, higher patient impedance dampens the discharge and reduces peak delivered current."
                },
                {
                    "question": "If patient impedance is R_th = 60.0 Ω and peak current is I_peak = 47.00 A with baseline I_0 = 68.00 A, what is slope k_r?",
                    "options": ["0.1750 A/Ω", "0.3500 A/Ω", "0.7000 A/Ω", "1.400 A/Ω"],
                    "correct": 1,
                    "explanation": "k_r = -(I_peak - I_0) / R_th = -(47.00 - 68.00) / 60.0 = 21.00 / 60.0 = 0.3500 A/Ω."
                },
                {
                    "question": "Why is an inductor placed in series with the storage capacitor in an RLC defibrillator circuit?",
                    "options": ["To limit current rise time (di/dt) and shape a smooth pulse, preventing myocardial tissue burns", "To make the shock colder", "To store radioactive waste", "To speed up battery charging"],
                    "correct": 0,
                    "explanation": "The series inductor restricts instantaneous current spikes, shaping a physiological millisecond pulse that prevents tissue damage."
                }
            ],
            "settings": ["Defibrillator: External RLC damped sinusoidal unit (200 Joules delivered setting)", "Circuit parameters: C = 32 μF, L = 50 mH, V_0 = 3600 V, r_i = 12 Ω", "Analyzer: Fluke Impulse 7000DP high-voltage non-inductive load bank"],
            "samples": [30.0, 45.0, 60.0, 75.0, 90.0, 105.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "⚡", "label": "1. Defibrillator Test Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Peak Current vs Impedance"},
                {"id": "sandbox", "icon": "⚡", "label": "3. RLC Discharge Sandbox"}
            ]
        },
        {
            "number": 41,
            "slug": "biphasic-functional-electrical-stimulator-charge-balance",
            "title": "Biphasic Functional Electrical Stimulation (FES) Charge Balance & Injection",
            "shortTitle": "FES Biphasic Charge Balance",
            "aim": "Verify net zero electrochemical charge balance and evaluate cathodic phase charge injection Q_p as a function of stimulus pulse current I_stim in a Functional Electrical Stimulation (FES) neuroprosthesis.",
            "inputLabel": "Stimulation Pulse Current I_stim",
            "shortInput": "Current I_stim",
            "inputUnit": "mA",
            "min": 5.0,
            "max": 30.0,
            "step": 5.0,
            "initial": 15.0,
            "inputDecimals": 1,
            "rawLabel": "Cathodic Phase Injected Charge Q_p",
            "rawUnit": "μC",
            "rawDecimals": 3,
            "xAxis": "Stimulation pulse current I_stim (mA)",
            "yAxis": "Cathodic injected charge Q_p (μC)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 17.5,
            "emptyY": 4.5,
            "targetName": "Pulse Width Duration Constant t_pw",
            "target": "0.2500",
            "refValue": 0.2500,
            "resultUnit": "μC/mA",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "Q_p = t_pw · I_stim = 0.2500 · I_stim (where t_pw = 250 μs = 0.2500 ms)",
            "measureLabel": "Measure FES Injected Charge",
            "intro": "Functional Electrical Stimulation (FES) and neuroprosthetics restore motor function (such as foot-drop correction during hemiplegic gait or hand grasp in quadriplegia) by applying controlled electrical current pulses to intact peripheral motor nerves, activating muscle contractions in paralyzed limbs. When electrical current passes through metal electrodes into tissue electrolytes, charge injection occurs via two distinct mechanisms: reversible non-Faradaic electrical double-layer capacitive charging, and Faradaic reduction-oxidation (redox) chemical reactions. If stimulating pulses leave any residual uncompensated DC charge (charge imbalance), Faradaic electrolysis of water produces toxic hydrogen ions, hydroxyl radicals, chlorine gas, and irreversible metallic electrode dissolution, causing severe tissue necrosis and neurotoxicity. To ensure long-term biocompatibility, neural stimulators universally deliver charge-balanced biphasic rectangular current pulses: a primary cathodic pulse depolarizes the axon, immediately followed by an anodic charge-reversal pulse of equal magnitude and duration to reverse Faradaic reactions. For a constant-current rectangular cathodic pulse of amplitude I_stim and duration t_pw, the total injected electrical charge Q_p per phase is governed by Q_p = ∫ I_stim dt = I_stim · t_pw = t_pw · I_stim, where t_pw is the pulse width (expressed as 0.2500 μC/mA for a standard 250 μs duration). In this experiment, a clinical multichannel FES stimulator discharging into an electrochemical tissue phantom evaluates charge balance and injected charge Q_p across currents from 5 to 30 mA.",
            "modelExtra": "Evaluated on a clinical constant-current FES neuroprosthesis (Bioness NESS L300 architecture) delivering charge-balanced symmetric biphasic rectangular pulses (pulse duration t_pw = 250 μs = 0.2500 ms, frequency 35 Hz) into a 1.0 kΩ parallel RC tissue load in 37.0 °C saline. Cathodic injected charge slope t_pw = 0.2500 μC/mA across pulse currents I_stim from 5.0 to 30.0 mA.",
            "apparatus": [
                {"name": "Clinical Multichannel Constant-Current FES Stimulator", "purpose": "Delivers programmable charge-balanced biphasic current pulses from 1 to 50 mA with 250 μs duration."},
                {"name": "Platinum-Iridium Neurostimulation Electrode Pair (10 mm²)", "purpose": "Biocompatible stimulation electrodes with high capacitive charge injection capacity (Q_inj)."},
                {"name": "Electrochemical Tissue Impedance Load Phantom (1.0 kΩ || 10 nF)", "purpose": "Accurately models transcutaneous skin-electrode interface impedance and double-layer capacitance."},
                {"name": "Precision Current-Sense Resistor & Analog Integrator Circuit", "purpose": "Integrates current waveforms in real time to measure injected phase charge Q_p with 0.01 μC accuracy."},
                {"name": "High-Resolution Dual-Channel Digital Oscilloscope", "purpose": "Captures simultaneous cathodic and anodic phase waveforms and monitors residual DC charge balance."},
                {"name": "Thermostatically Controlled Physiological Saline Bath (37.0 °C)", "purpose": "Maintains 0.9% NaCl electrolyte environment for electrochemical electrode testing."}
            ],
            "procedure": [
                {"title": "Tissue Phantom Load Connection and Calibration", "text": "Connect the FES stimulation output across the 1.0 kΩ precision non-inductive load in parallel with 10 nF double-layer capacitor; verify zero DC bias voltage."},
                {"title": "Biphasic Waveform Symmetry Configuration", "text": "Program stimulator to deliver charge-balanced symmetric biphasic pulses: pulse width t_pw = 250 μs cathodic, 50 μs interphase delay, followed by 250 μs anodic reversal at 35 Hz."},
                {"title": "Initial Current Step Initialization", "text": "Set stimulation current amplitude to I_stim = 5.0 mA and initiate continuous stimulation train."},
                {"title": "Cathodic Phase Charge Integration", "text": "Record the voltage drop across the precision 10.0 Ω sensing resistor, integrate current over the 250 μs cathodic duration, and calculate injected charge Q_p = I_stim · t_pw in micro-Coulombs."},
                {"title": "Net DC Charge Balance Verification", "text": "Integrate the complete cycle (cathodic plus anodic phases) over 100 pulses to confirm net DC offset charge is strictly < 0.01 μC (safe charge balance)."},
                {"title": "Current Progression Sequence", "text": "Increment stimulation current through 10.0, 15.0, 20.0, 25.0, and 30.0 mA, recording cathodic injected charge Q_p at each current step."},
                {"title": "Charge Injection Linear Regression Analysis", "text": "Plot injected charge Q_p versus stimulation current I_stim and verify that the regression slope matches the programmed pulse duration t_pw = 0.2500 μC/mA."}
            ],
            "topics": [
                {"question": "Why is net zero DC charge balance essential in electrical stimulation of biological tissues?", "answer": "Monopolar or charge-imbalanced currents cause irreversible Faradaic electrolysis at the metal-tissue interface: water oxidizes into oxygen and protons (acidifying tissue), water reduces into hydrogen and hydroxide ions (alkalizing tissue), and metal atoms dissolve into toxic cations, causing electrode breakdown and neuronal death."},
                {"question": "What is the Shannon criterion for neural damage in electrical stimulation?", "answer": "The Shannon equation log(D) = k - log(Q) defines the safe boundary for neural stimulation, where D is charge density per phase (μC/cm²), Q is charge per phase (μC), and k is an empirical safety limit (typically k = 1.75 to 1.85); exceeding this limit risks permanent axonal injury."},
                {"question": "What is the difference between capacitive and Faradaic charge injection?", "answer": "Capacitive charge injection involves reversible electrostatic alignment of ions in the aqueous double-layer without chemical electron transfer across the interface (completely safe); Faradaic charge injection involves actual electron transfer through redox chemical reactions, which can be reversible (e.g., platinum oxide reduction) or irreversible (water hydrolysis)."},
                {"question": "Why is an interphase gap (typically 50 to 100 μs) introduced between cathodic and anodic pulses?", "answer": "The cathodic pulse depolarizes the axon; if the anodic reversing pulse follows immediately with zero delay, it can hyperpolarize the membrane prematurely, prematurely extinguishing the nascent action potential before it can propagate down the nerve."},
                {"question": "Why is the cathodic phase generally used as the primary activating pulse in neurostimulation?", "answer": "A cathodic (negative) electrode deposits negative charges extracellularly, creating a local outward transmembrane current that depolarizes the axolemma toward action potential threshold at much lower current amplitudes than an anodic pulse."},
                {"question": "What is passive charge balancing versus active charge balancing?", "answer": "Active charge balancing uses a controlled-current circuit to drive an equal and opposite anodic current pulse; passive charge balancing places a DC-blocking capacitor in series with the electrode and shorts the electrode to ground during the interpulse interval through a switch, discharging any residual accumulated charge."}
            ],
            "precautions": [
                "Always verify that net DC current is zero (< 1 μA); continuous DC leakage causes rapid tissue chemical burns.",
                "Ensure electrode charge density does not exceed the water hydrolysis electrochemical potential window (-0.6 V to +0.8 V vs. Ag/AgCl).",
                "Maintain firm, uniform electrode contact to avoid localized current crowding and superficial skin burns.",
                "Calibrate the current-sensing resistor accurately to ensure precise phase charge integration."
            ],
            "limitations": [
                "The simple Q = I · t relationship assumes a perfect rectangular current pulse; real inductive leads introduce finite rise and fall times.",
                "Evaluates static RC phantom, whereas human skin exhibits dynamic, non-linear impedance that decreases with increasing current amplitude.",
                "Tested on superficial transcutaneous parameters; deep brain stimulation (DBS) or cochlear implants operate at much lower currents (< 5 mA) and smaller electrode areas.",
                "Does not model selective fiber recruitment (large-diameter sensory Aβ fibers vs. motor Aα fibers) in living nerves."
            ],
            "quiz": [
                {
                    "question": "Why must neurostimulation pulses be strictly charge-balanced biphasic waveforms?",
                    "options": ["To prevent toxic electrochemical Faradaic reactions, water electrolysis, and tissue necrosis", "To make the battery charge itself", "To turn the nerves blue", "To double the patient's walking speed"],
                    "correct": 0,
                    "explanation": "Charge-balanced biphasic stimulation reverses Faradaic redox reactions, preventing water electrolysis, pH shifts, and electrode dissolution."
                },
                {
                    "question": "What is the injected electrical charge Q_p for a 20.0 mA pulse lasting 250 μs (0.250 ms)?",
                    "options": ["2.50 μC", "5.00 μC", "10.0 μC", "50.0 μC"],
                    "correct": 1,
                    "explanation": "Q_p = I · t = 20.0 mA · 0.250 ms = 5.000 μC."
                },
                {
                    "question": "Which polarity of electrical pulse is most effective at initiating an action potential in an adjacent nerve axon?",
                    "options": ["Cathodic (negative) pulse", "Anodic (positive) pulse", "Neutral pulse", "Magnetic pulse"],
                    "correct": 0,
                    "explanation": "Cathodic pulses deposit negative charges outside the axon, creating an outward depolarizing current that triggers action potentials at lower thresholds."
                },
                {
                    "question": "What does the Shannon criterion define in clinical neuroprosthetics?",
                    "options": ["The safe boundary between non-damaging electrical stimulation and tissue injury", "The maximum weight of the stimulator", "The battery chemistry of the implant", "The speed of sound in bone"],
                    "correct": 0,
                    "explanation": "The Shannon criterion establishes mathematical safety limits relating charge per phase and charge density to avoid neural tissue damage."
                }
            ],
            "settings": ["Stimulator: Constant-current biphasic FES unit (35 Hz, symmetric biphasic)", "Waveform: t_pw = 250 μs cathodic, 50 μs interphase gap, 250 μs anodic reversal", "Load: Electrochemical skin-electrode phantom (1.0 kΩ || 10 nF) in 37.0 °C saline"],
            "samples": [5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "⚡", "label": "1. FES Pulse Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Injected Charge vs Current"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Charge Balance Sandbox"}
            ]
        },
        {
            "number": 42,
            "slug": "hearing-aid-electroacoustic-frequency-response-gain",
            "title": "Digital Hearing Aid Electroacoustic 2-cc Coupler Sound Pressure Gain",
            "shortTitle": "Hearing Aid Acoustic Gain",
            "aim": "Determine the linear acoustic gain and input-output transfer slope k_g of a digital hearing aid in an ANSI S3.22 standardized 2-cc acoustic coupler across input sound pressure levels.",
            "inputLabel": "Acoustic Test Input Level SPL_in",
            "shortInput": "Input SPL_in",
            "inputUnit": "dB SPL",
            "min": 50.0,
            "max": 75.0,
            "step": 5.0,
            "initial": 60.0,
            "inputDecimals": 1,
            "rawLabel": "2-cc Coupler Output Sound Level SPL_out",
            "rawUnit": "dB SPL",
            "rawDecimals": 3,
            "xAxis": "Acoustic input sound level SPL_in (dB SPL)",
            "yAxis": "2-cc Coupler output sound level SPL_out (dB SPL)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 62.5,
            "emptyY": 85.0,
            "targetName": "Input-Output Acoustic Transfer Slope k_g",
            "target": "0.9500",
            "refValue": 0.9500,
            "resultUnit": "dB/dB",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "SPL_out = k_g · SPL_in + Gain_0 = 0.9500 · SPL_in + 28.5000",
            "measureLabel": "Measure Coupler Output SPL",
            "intro": "Sensorineural hearing loss affects hundreds of millions of individuals worldwide, degrading speech intelligibility, cognitive function, and social interaction. Modern digital hearing aids are sophisticated audio-processing bio-acoustic computers that capture acoustic waves via MEMS microphones, digitize the signal with 24-bit audio converters, apply multi-channel dynamic range compression (WDRC) and acoustic feedback cancellation on a low-power digital signal processor (DSP), and deliver amplified sound into the external ear canal via a balanced armature receiver. To objectively evaluate the electroacoustic performance of hearing aids independent of individual patient ear canal anatomy, the American National Standards Institute established the standard specification ANSI/ASA S3.22 ('Specification of Hearing Aid Characteristics'). The international standard specifies measuring acoustic output inside an HA-1 or HA-2 standardized 2-cc acoustic coupler (which replicates the average 2.0 mL acoustic volume and impedance of an adult human ear canal occluded by an earmold). In the linear amplification region below the wide dynamic range compression knee-point (typically 50 to 75 dB SPL input), the output sound pressure level SPL_out scales linearly with input sound level SPL_in: SPL_out = k_g · SPL_in + Gain_0, where k_g is the input-output acoustic transfer slope (approximately 0.95 dB/dB in linear mode) and Gain_0 represents baseline acoustic gain (~28.5 dB at 1.0 kHz). In this laboratory investigation, an instrumented anechoic hearing aid test box evaluates a digital behind-the-ear (BTE) hearing aid across input sound pressure levels from 50 to 75 dB SPL.",
            "modelExtra": "Evaluated on a 16-channel digital Behind-The-Ear (BTE) hearing aid connected to a standardized ANSI S3.22 HA-2 2-cc acoustic coupler inside an anechoic sound chamber. Pure-tone acoustic test stimulus at 1.0 kHz. Linear acoustic transfer slope k_g = 0.9500 dB/dB with intercept Gain_0 = 28.5000 dB across input sound levels SPL_in from 50.0 to 75.0 dB SPL (output SPL_out from 76.00 to 99.75 dB SPL).",
            "apparatus": [
                {"name": "Anechoic Hearing Aid Acoustic Test Box (Audioscan Verifit / Frye Fonix)", "purpose": "Provides sound-isolated anechoic acoustic test chamber with internal reference loudspeaker."},
                {"name": "Standardized ANSI S3.22 HA-2 2-cc Acoustic Coupler", "purpose": "Precision metal acoustic cavity replicating human occluded ear canal volume (2.00 ± 0.02 mL)."},
                {"name": "Laboratory-Grade 1/2-Inch Pressure Condenser Microphone (Bruel & Kjaer)", "purpose": "Measures true acoustic sound pressure level inside the 2-cc coupler with NIST traceability."},
                {"name": "Calibrated External Sound Field Reference Microphone", "purpose": "Monitors input acoustic sound field at the hearing aid microphone port, maintaining closed-loop leveling."},
                {"name": "Digital 16-Channel Behind-The-Ear (BTE) Hearing Aid", "purpose": "Clinical digital hearing aid with dual omnidirectional MEMS microphones and balanced armature receiver."},
                {"name": "Automated Real-Time Audio Spectrum Analyzer Console", "purpose": "Generates pure-tone test stimuli and executes automated ANSI S3.22 compliance test sequences."}
            ],
            "procedure": [
                {"title": "Anechoic Test Box Sound Field Leveling", "text": "Close the anechoic test box and execute automated sound field equalization to calibrate loudspeaker output across 100 Hz to 8000 Hz."},
                {"title": "Hearing Aid 2-cc Coupler Coupling", "text": "Attach the BTE hearing aid sound tube securely to the HA-2 2-cc coupler using acoustic sealing putty; seat the reference microphone within 5 mm of the hearing aid inlet."},
                {"title": "Test Mode Programming Configuration", "text": "Program hearing aid via wireless Noahlink interface into standardized ANSI S3.22 linear test mode (disable adaptive noise reduction and feedback suppression)."},
                {"title": "Input Sound Level Step Initialization", "text": "Set pure-tone 1.0 kHz acoustic stimulus to input level SPL_in = 50.0 dB SPL and allow 5 seconds for output stabilization."},
                {"title": "2-cc Coupler Sound Pressure Measurement", "text": "Record the RMS sound pressure level SPL_out inside the 2-cc coupler using the calibrated laboratory condenser microphone."},
                {"title": "Input Level Progression Sequence", "text": "Increment input sound level through 55.0, 60.0, 65.0, 70.0, and 75.0 dB SPL, recording stabilized coupler output SPL_out at each step."},
                {"title": "Electroacoustic Transfer Function Regression", "text": "Plot coupler output level SPL_out versus input level SPL_in, compute transfer slope k_g and baseline gain Gain_0 via linear regression, and calculate total acoustic gain."}
            ],
            "topics": [
                {"question": "What is the purpose of an ANSI 2-cc acoustic coupler in hearing aid evaluation?", "answer": "The 2-cc coupler provides an internationally standardized, rigid, reproducible acoustic cavity that approximates the 2.0 mL volume and acoustic compliance of an average occluded adult human ear canal, allowing objective comparison of hearing aids across manufacturers without anatomical variability."},
                {"question": "What is the difference between linear amplification and Wide Dynamic Range Compression (WDRC)?", "answer": "Linear amplification applies identical gain to soft, medium, and loud sounds until saturation; WDRC applies high gain to soft sounds (making them audible) and progressively less gain to loud sounds (keeping them comfortable), compressing the wide dynamic range of everyday speech into the patient's narrowed dynamic range."},
                {"question": "What is acoustic feedback oscillation in a hearing aid and how is it suppressed?", "answer": "Feedback occurs when amplified sound leaking from the ear canal reaches the external microphone in phase, creating a squealing acoustic oscillation loop; digital aids suppress feedback using adaptive digital filtering that continuously estimates the acoustic leakage path and subtracts an inverted cancelling signal."},
                {"question": "Why is the decibel sound pressure level (dB SPL) defined relative to 20 μPa?", "answer": "20 micropascals (20 μPa = 2×10⁻⁵ N/m²) is the standard reference sound pressure corresponding to the absolute threshold of human hearing for a 1.0 kHz pure tone in healthy young adults (0 dB SPL)."},
                {"question": "What is Real-Ear Aided Response (REAR) and how does it differ from 2-cc coupler output?", "answer": "A 2-cc coupler is a hard metal cylinder that neglects individual ear canal acoustic resonance, head diffraction, and eardrum compliance; REAR measures true sound pressure directly in the patient's actual ear canal using a tiny probe-tube microphone placed within 5 mm of the tympanic membrane."},
                {"question": "What is Maximum Power Output (OSPL90) in hearing aid specifications?", "answer": "OSPL90 (Output Sound Pressure Level with a 90 dB input) is the maximum saturation acoustic output the hearing aid can physically produce; it is strictly limited to prevent noise-induced hearing damage to the patient from sudden loud environmental sounds."}
            ],
            "precautions": [
                "Seal hearing aid tube into the 2-cc coupler with acoustic putty; microscopic acoustic leaks completely destroy low-frequency measurement accuracy.",
                "Verify anechoic test box door is fully latched to maintain isolation from ambient room noise.",
                "Position the reference microphone within 5 mm of the hearing aid sound inlet to ensure accurate closed-loop sound field leveling.",
                "Ensure hearing aid digital adaptive features (directional microphones, noise reduction) are disabled during ANSI standard testing."
            ],
            "limitations": [
                "The linear transfer model applies below the compression threshold; input levels > 75 dB SPL trigger non-linear WDRC compression kneepoints.",
                "2-cc metal couplers do not model ear canal acoustic impedance variation, tympanic membrane compliance, or acoustic venting.",
                "Tested with steady pure-tone stimuli; complex dynamic speech signals exhibit modulated spectral interactions and temporal masking.",
                "Does not evaluate patient speech intelligibility, cognitive processing, or binaural spatial sound localization."
            ],
            "quiz": [
                {
                    "question": "What standard acoustic cavity volume is specified by ANSI S3.22 for evaluating hearing aid electroacoustics?",
                    "options": ["2.0 cc (2.0 mL)", "10.0 cc", "50.0 cc", "100.0 cc"],
                    "correct": 0,
                    "explanation": "ANSI S3.22 specifies a standardized 2-cc (2.0 mL) metal acoustic coupler that approximates the average human ear canal volume."
                },
                {
                    "question": "What is the primary benefit of Wide Dynamic Range Compression (WDRC) in digital hearing aids?",
                    "options": ["It provides more amplification for soft sounds while preventing loud sounds from becoming uncomfortably loud", "It doubles the battery life", "It eliminates all earwax", "It connects directly to the optic nerve"],
                    "correct": 0,
                    "explanation": "WDRC compresses the wide dynamic range of sound into the impaired ear's restricted dynamic range, amplifying quiet sounds comfortably."
                },
                {
                    "question": "If input sound level is SPL_in = 60.0 dB SPL and output sound level is SPL_out = 85.50 dB SPL, what is the acoustic gain?",
                    "options": ["15.5 dB", "25.5 dB", "35.5 dB", "85.5 dB"],
                    "correct": 1,
                    "explanation": "Acoustic gain = SPL_out - SPL_in = 85.50 dB - 60.0 dB = 25.50 dB."
                },
                {
                    "question": "What reference sound pressure corresponds to 0 dB SPL, the threshold of human hearing at 1 kHz?",
                    "options": ["20 micropascals (20 μPa)", "1 atmosphere", "1 Pascal", "100 dynes/cm²"],
                    "correct": 0,
                    "explanation": "0 dB SPL is defined relative to the reference sound pressure of 20 μPa (2×10⁻⁵ Pa), the nominal human hearing threshold at 1 kHz."
                }
            ],
            "settings": ["Hearing aid: 16-channel digital BTE hearing aid in ANSI linear test mode", "Coupler: Standardized ANSI S3.22 HA-2 2-cc acoustic coupler with 1/2-inch B&K microphone", "Test chamber: Anechoic test box with reference leveling microphone at 1.0 kHz"],
            "samples": [50.0, 55.0, 60.0, 65.0, 70.0, 75.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🦻", "label": "1. Anechoic Test Box"},
                {"id": "compare", "icon": "📊", "label": "2. Input-Output Transfer"},
                {"id": "sandbox", "icon": "⚡", "label": "3. 2-cc Coupler Sandbox"}
            ]
        }
    ]
