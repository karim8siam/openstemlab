# -*- coding: utf-8 -*-
"""Biomedical Engineering Module 4: Cardiovascular Fluid Dynamics, Hemodynamics & Artificial Organs (Labs 27–34)."""

def get_module_4():
    return [
        {
            "number": 27,
            "slug": "blood-viscosity-cone-and-plate-rheometer-casson",
            "title": "Non-Newtonian Blood Rheology & Casson Fluid Model Cone-and-Plate Viscometry",
            "shortTitle": "Blood Rheology Casson Model",
            "aim": "Determine the Casson asymptotic plastic viscosity μ_c and yield stress τ_y of whole human blood across low-to-medium shear rates using cone-and-plate rheometry.",
            "inputLabel": "Fluid Shear Rate γ̇",
            "shortInput": "Shear Rate γ̇",
            "inputUnit": "s⁻¹",
            "min": 16.0,
            "max": 196.0,
            "step": 25.0,
            "initial": 64.0,
            "inputDecimals": 1,
            "rawLabel": "Measured Shear Stress τ",
            "rawUnit": "Pa",
            "rawDecimals": 4,
            "xAxis": "Square root of shear rate √γ̇ (s⁻⁰·⁵)",
            "yAxis": "Square root of shear stress √τ (Pa⁰·⁵)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 10.0,
            "emptyY": 0.80,
            "targetName": "Casson Plastic Viscosity Root √μ_c",
            "target": "0.0620",
            "refValue": 0.0620,
            "resultUnit": "Pa⁰·⁵·s⁰·⁵",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "√τ = √μ_c · √γ̇ + √τ_y = 0.0620 · √γ̇ + 0.1800",
            "measureLabel": "Measure Rheological Shear Stress",
            "intro": "Human blood is not a simple homogeneous Newtonian fluid; it is a dense suspension of cellular elements (erythrocytes/RBCs, leukocytes, and platelets) suspended in an aqueous electrolyte-protein matrix (blood plasma). Erythrocytes comprise approximately 40% to 45% of total blood volume (normal hematocrit Hct). At low shear rates (γ̇ < 50 s⁻¹), red blood cells aggregate face-to-face into reversible, rouleaux structures and three-dimensional cellular networks stabilized by plasma fibrinogen and globulins. This cellular networking creates shear-thinning (pseudoplastic) non-Newtonian flow behavior and a finite yield stress τ_y below which blood resists flow. At elevated shear rates, rouleaux disperse into individual deformable biconcave discs that elongate and align with streamlines, causing apparent viscosity to asymptote toward a constant high-shear baseline. To mathematically characterize this non-Newtonian behavior, the Casson fluid model is the universally adopted standard: √τ = √μ_c · √γ̇ + √τ_y, where τ is shear stress, γ̇ is shear rate, μ_c is the Casson asymptotic plastic viscosity (Pa·s), and τ_y is the blood yield stress (Pa). In a cone-and-plate rotational rheometer, the shear rate is geometrically uniform throughout the entire wedge gap, providing ideal conditions to evaluate blood rheology. In this laboratory investigation, anti-coagulated whole blood at 37.0 °C is tested across shear rates from 16 to 196 s⁻¹ to determine Casson parameters.",
            "modelExtra": "Evaluated on anti-coagulated human whole blood (Hct = 45%, EDTA treated) at 37.0 °C in a titanium cone-and-plate rheometer (cone angle θ = 1.0°, diameter 60 mm). Standard shear rates γ̇ = 16, 36, 64, 100, 144, 196 s⁻¹ correspond to √γ̇ = 4, 6, 8, 10, 12, 14 s⁻⁰·⁵. Casson slope √μ_c = 0.0620 Pa⁰·⁵·s⁰·⁵ (asymptotic viscosity μ_c = 0.00384 Pa·s = 3.84 cP) with yield root √τ_y = 0.1800 Pa⁰·⁵ (yield stress τ_y = 0.0324 Pa).",
            "apparatus": [
                {"name": "Precision Controlled-Stress Cone-and-Plate Rheometer", "purpose": "Applies controlled angular velocity and measures torque with micro-Newton-meter magnetic bearing."},
                {"name": "Titanium Rheometer Cone (diameter 60 mm, cone angle 1.0°)", "purpose": "Generates strictly uniform shear rate γ̇ = ω / tan(θ) throughout the entire measurement fluid volume."},
                {"name": "Peltier Thermoelectric Temperature Control Plate (37.0 ± 0.05 °C)", "purpose": "Maintains physiological temperature preventing blood viscosity thermal artifacts."},
                {"name": "Anti-Evaporation Solvent Trap with Humidified Ring", "purpose": "Prevents plasma water evaporation and blood drying during multi-point shear sweeps."},
                {"name": "Pre-Analytical Blood Roller Mixer", "purpose": "Maintains uniform erythrocyte resuspension prior to pipetting into the rheometer gap."},
                {"name": "High-Precision Micro-Pipettor (500 μL)", "purpose": "Delivers exact sample volume (0.50 mL) to perfectly fill the cone-plate truncation gap."}
            ],
            "procedure": [
                {"title": "Blood Specimen Resuspension and Hematocrit Verification", "text": "Mix EDTA-anticoagulated whole blood on roller mixer for 10 minutes; verify standard hematocrit (Hct = 45 ± 1%) via microhematocrit centrifuge."},
                {"title": "Peltier Plate Thermal Stabilization", "text": "Set rheometer Peltier bottom plate to exactly 37.0 °C and allow 15 minutes for thermal equilibrium."},
                {"title": "Zero Gap Calibration and Specimen Loading", "text": "Zero the normal force and calibrate the mechanical contact gap; pipette exactly 500 μL of blood onto the plate center and lower cone to truncation height (50 μm)."},
                {"title": "Solvent Trap Placement and High-Shear Preshear", "text": "Engage the humidified solvent trap and apply a 30-second preshear at 300 s⁻¹ to completely disperse pre-existing rouleaux aggregates."},
                {"title": "Stepwise Shear Rate Sweep", "text": "Step through shear rates γ̇ = 16, 36, 64, 100, 144, and 196 s⁻¹, holding each step for 15 seconds to achieve steady torque before recording shear stress τ."},
                {"title": "Casson Linearized Coordinate Regression", "text": "Compute √γ̇ and √τ, plot √τ versus √γ̇, and extract Casson asymptotic viscosity root √μ_c from the slope and yield stress root √τ_y from the y-intercept."}
            ],
            "topics": [
                {"question": "What is the physical cause of blood shear-thinning at low shear rates?", "answer": "At low shear rates, red blood cells aggregate into stacked coin-like rouleaux structures bound by plasma fibrinogen; as shear rate increases, hydrodynamic shear stresses break these rouleaux apart and deform individual erythrocytes into streamlined ellipsoids, decreasing flow resistance."},
                {"question": "Why does a cone-and-plate rheometer produce a uniform shear rate?", "answer": "The linear velocity of the rotating cone increases linearly with radius r (v = ω·r), but the gap height between the cone and plate also increases linearly with radius (h = r·tan θ). Because shear rate is velocity divided by gap height (γ̇ = v/h = ω/tan θ), the radius r cancels, making shear rate mathematically identical at every point in the fluid."},
                {"question": "What physiological role does plasma fibrinogen play in blood rheology?", "answer": "Fibrinogen is a large, asymmetrical 340 kDa plasma glycoprotein that adsorbs simultaneously onto adjacent erythrocyte membranes, acting as a molecular bridge that drives rouleaux aggregation and establishes the blood yield stress τ_y."},
                {"question": "How does hematocrit affect whole blood viscosity?", "answer": "Viscosity increases exponentially with hematocrit. In polycythemia (Hct > 55–60%), blood viscosity doubles or triples, drastically elevating vascular resistance and cardiac workload; in severe anemia (Hct < 25%), blood becomes less viscous, reducing peripheral vascular resistance."},
                {"question": "What is the clinical significance of blood yield stress in microcirculatory stasis?", "answer": "If perfusion pressure drops below the threshold needed to generate the yield stress τ_y in post-capillary venules, blood flow halts completely, resulting in microvascular stasis, thrombosis, and tissue infarction (as seen in septic shock and sickle cell crisis)."},
                {"question": "Why is blood treated as Newtonian in large arteries but non-Newtonian in microvessels?", "answer": "In large arteries (aorta, femoral), shear rates typically exceed 200–500 s⁻¹, where blood viscosity plateaus at a constant asymptotic value (~3.5–4.0 cP); in microvessels and low-flow recirculating zones, shear rates drop below 50 s⁻¹, where non-Newtonian rouleaux dynamics dominate."}
            ],
            "precautions": [
                "Always use a humidified solvent trap; blood drying around the cone perimeter creates enormous edge-drying torque artifacts.",
                "Ensure exact sample volume pipetting (500 μL); underfilling or overfilling the gap distorts the meniscus and invalidates shear geometry.",
                "Verify that anti-coagulated blood shows no microscopic clot formation or hemolysis before testing.",
                "Perform a high-shear preshear (300 s⁻¹ for 30 s) before each run to establish a reproducible uniform initial cellular dispersion state."
            ],
            "limitations": [
                "The Casson model is an empirical continuum approximation; it applies across 10 to 300 s⁻¹ but does not capture zero-shear viscoelasticity.",
                "Assumes homogeneous suspension, neglecting the Fahraeus-Lindqvist cell-free layer present in narrow channels.",
                "In-vitro rotational testing uses steady shear, whereas in-vivo arterial flow is pulsatile with oscillating shear directions.",
                "Blood samples age rapidly in vitro; measurements must be completed within 4 hours of venipuncture to avoid erythrocyte echinocyte crenation."
            ],
            "quiz": [
                {
                    "question": "What happens to the apparent viscosity of whole human blood as shear rate increases from 10 to 200 s⁻¹?",
                    "options": ["Viscosity decreases (shear-thinning pseudoplastic behavior)", "Viscosity increases (shear-thickening dilatant behavior)", "Viscosity remains strictly constant", "Viscosity drops to zero instantly"],
                    "correct": 0,
                    "explanation": "Blood is a shear-thinning fluid: increasing shear breaks up red cell rouleaux aggregates and aligns cells with streamlines, reducing apparent viscosity."
                },
                {
                    "question": "Which mathematical equation is the clinical standard for modeling non-Newtonian blood rheology?",
                    "options": ["The Casson fluid equation (√τ = √μ_c · √γ̇ + √τ_y)", "The Ideal Gas Law", "Newton's Second Law", "Schrödinger's Equation"],
                    "correct": 0,
                    "explanation": "The Casson equation relates the square root of shear stress to the square root of shear rate, accounting for both yield stress and asymptotic viscosity."
                },
                {
                    "question": "If √γ̇ = 10.0 s⁻⁰·⁵ produces √τ = 0.8000 Pa⁰·⁵ and the y-intercept is 0.1800 Pa⁰·⁵, what is √μ_c?",
                    "options": ["0.0310 Pa⁰·⁵·s⁰·⁵", "0.0620 Pa⁰·⁵·s⁰·⁵", "0.1240 Pa⁰·⁵·s⁰·⁵", "0.6200 Pa⁰·⁵·s⁰·⁵"],
                    "correct": 1,
                    "explanation": "√μ_c = (√τ - √τ_y) / √γ̇ = (0.8000 - 0.1800) / 10.0 = 0.6200 / 10.0 = 0.0620 Pa⁰·⁵·s⁰·⁵."
                },
                {
                    "question": "Which plasma protein is primarily responsible for bridging red blood cells into rouleaux aggregates?",
                    "options": ["Fibrinogen", "Albumin", "Insulin", "Hemoglobin"],
                    "correct": 0,
                    "explanation": "Fibrinogen is an elongated, large plasma glycoprotein that adsorbs across adjacent red cell membranes, forming rouleaux bridges."
                }
            ],
            "settings": ["Fluid: Human whole blood (Hct = 45%, EDTA anticoagulated)", "Geometry: Cone-and-plate (60 mm diameter, θ = 1.0°, truncation gap 50 μm)", "Temperature: 37.0 ± 0.05 °C Peltier controlled"],
            "samples": [16.0, 36.0, 64.0, 100.0, 144.0, 196.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🩸", "label": "1. Cone-Plate Rheometer"},
                {"id": "compare", "icon": "📊", "label": "2. Casson Linear Plot"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Rouleaux Shearing Sandbox"}
            ]
        },
        {
            "number": 28,
            "slug": "hagen-poiseuille-microvascular-flow-resistance",
            "title": "Microvascular Perfusion Hydraulic Resistance & Hagen-Poiseuille Flow Verification",
            "shortTitle": "Microvascular Hydraulic Resistance",
            "aim": "Determine the hydraulic flow resistance R_hyd of a precision microvascular capillary network perfusion model and verify Hagen-Poiseuille laminar resistance scaling.",
            "inputLabel": "Perfusion Volumetric Flow Rate Q",
            "shortInput": "Flow Rate Q",
            "inputUnit": "mL/min",
            "min": 2.0,
            "max": 12.0,
            "step": 2.0,
            "initial": 6.0,
            "inputDecimals": 1,
            "rawLabel": "Perfusion Pressure Drop ΔP",
            "rawUnit": "kPa",
            "rawDecimals": 3,
            "xAxis": "Perfusion flow rate Q (mL/min)",
            "yAxis": "Perfusion pressure drop ΔP (kPa)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 7.0,
            "emptyY": 25.0,
            "targetName": "Microvascular Hydraulic Resistance R_hyd",
            "target": "3.6000",
            "refValue": 3.6000,
            "resultUnit": "kPa/(mL/min)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ΔP = R_hyd · Q = 3.6000 · Q",
            "measureLabel": "Measure Perfusion Pressure Drop",
            "intro": "In human cardiovascular physiology and microcirculation, peripheral vascular resistance across arterioles and capillary networks governs systemic blood pressure, capillary filtration, and local tissue perfusion. The relationship between driving pressure drop ΔP and steady volumetric flow rate Q through a circular cylindrical conduit of lumen radius r and length L is governed by the classical Hagen-Poiseuille law for laminar viscous flow: ΔP = [8·μ·L / (π·r⁴)] · Q = R_hyd · Q, where μ is dynamic fluid viscosity and R_hyd is hydraulic resistance. The defining hallmark of Hagen-Poiseuille resistance is its extreme inverse sensitivity to vascular radius: halving the lumen radius increases hydraulic resistance by a factor of 16 (r⁻⁴ scaling). In physiological arterioles (the primary 'stopcocks' of the systemic circulation), small degrees of vascular smooth muscle contraction (vasoconstriction) or relaxation (vasodilation) dramatically modulate peripheral vascular resistance and divert blood to metabolically active tissues. In organ preservation perfusion machines (used for hypothermic machine perfusion of donor kidneys and livers) and microfluidic organ-on-a-chip platforms, continuous monitoring of hydraulic resistance R_hyd is vital for detecting microvascular thrombosis, vasospasm, and endothelial swelling. In this laboratory investigation, an instrumented microvascular capillary network perfused with physiological saline evaluates the linear pressure-flow relationship to determine hydraulic resistance R_hyd.",
            "modelExtra": "Evaluated on a biomimetic PDMS microvascular capillary perfusion cartridge (lumen diameter 120 μm, length 40 mm, 8 parallel microchannels) perfused with physiological saline (viscosity μ = 0.0010 Pa·s) at 37.0 °C. Perfusion flow rates from 2.0 to 12.0 mL/min yield Reynolds numbers Re < 50 (strictly laminar). Hydraulic resistance R_hyd = 3.6000 kPa/(mL/min).",
            "apparatus": [
                {"name": "Precision Dual-Syringe Pulseless Perfusion Pump", "purpose": "Delivers pulseless volumetric flow rates from 0.1 to 20 mL/min with stepper-motor accuracy."},
                {"name": "Biomimetic Microvascular Perfusion Cartridge", "purpose": "Provides microfabricated parallel cylindrical conduits with optically transparent viewing windows."},
                {"name": "Differential Wet-Wet Piezoresistive Pressure Transducer", "purpose": "Measures trans-vascular pressure drop ΔP from 0 to 50 kPa with 0.05% accuracy."},
                {"name": "Thermostatically Controlled Perfusion Warming Circuit (37.0 °C)", "purpose": "Maintains perfusate fluid temperature stable within ±0.1 °C to fix fluid viscosity."},
                {"name": "In-Line Degasser & Hydrophobic Bubble Trap", "purpose": "Eliminates microscopic air bubbles that would lodge in microchannels and alter hydraulic resistance."},
                {"name": "Precision Analytical Catch Balance", "purpose": "Validates actual volumetric delivery rate by timed gravimetric fluid collection."}
            ],
            "procedure": [
                {"title": "Perfusion Circuit Degassing and Priming", "text": "Prime the microvascular flow loop with degassed physiological saline at 37.0 °C, ensuring zero air bubbles remain in the tubing or differential pressure ports."},
                {"title": "Differential Pressure Transducer Zeroing", "text": "With the perfusion pump halted, open the bypass valve to equalize pressure ports and zero the differential pressure transducer to exactly 0.000 kPa."},
                {"title": "Perfusion Pump Initialization", "text": "Set the dual-syringe infusion pump to deliver 2.0 mL/min and close the bypass valve, allowing 2 minutes for pressure to achieve steady state."},
                {"title": "Pressure Drop Telemetry Logging", "text": "Record 100 consecutive differential pressure readings over 30 seconds and calculate mean pressure drop ΔP in kilopascals."},
                {"title": "Flow Rate Progression Sequence", "text": "Increment pump delivery rate through 4.0, 6.0, 8.0, 10.0, and 12.0 mL/min, logging stabilized pressure drop at each flow rate."},
                {"title": "Hydraulic Resistance Regression Analysis", "text": "Plot trans-vascular pressure drop ΔP versus flow rate Q and determine hydraulic resistance R_hyd from the slope of the linear fit through the origin."}
            ],
            "topics": [
                {"question": "Why does vascular resistance depend on the fourth power of vessel radius (r⁻⁴)?", "answer": "In laminar flow, velocity follows a parabolic profile where maximum velocity scales as r² and cross-sectional lumen area scales as r²; multiplying area by average velocity yields volumetric flow proportional to r⁴, making resistance R = ΔP/Q proportional to 1/r⁴."},
                {"question": "What is the Reynolds number and what value defines the laminar regime in microvessels?", "answer": "Reynolds number Re = ρ·v·D / μ represents the ratio of inertial to viscous forces; in human microvessels and arterioles, Re is typically between 0.01 and 10, placing flow deep within the laminar Stokes flow regime where viscous dissipation dominates."},
                {"question": "How do precapillary arterioles control systemic blood pressure and organ perfusion?", "answer": "Arterioles have thick muscular walls that contract or dilate in response to sympathetic nerve activity, angiotensin II, and local metabolites (nitric oxide, adenosine). Because of r⁻⁴ scaling, a 16% reduction in radius doubles arteriolar resistance, drastically lowering capillary flow and raising upstream arterial pressure."},
                {"question": "What is the entrance length in capillary flow and why is it negligible here?", "answer": "The hydrodynamic entrance length L_e ≈ 0.06 · Re · D is the distance required for a flat velocity profile to develop into fully developed parabolic Poiseuille flow; at Re < 50 in 120 μm channels, L_e is under 0.3 mm, comprising less than 1% of total channel length."},
                {"question": "How does fluid temperature affect hydraulic resistance?", "answer": "Dynamic viscosity μ of water and saline decreases by approximately 2% to 3% per degree Celsius rise; warming perfusate from 20 °C to 37 °C decreases fluid viscosity by ~30%, lowering hydraulic resistance by the exact same proportion."},
                {"question": "What is the clinical significance of rising hydraulic resistance in donor organ perfusion?", "answer": "During kidney or liver machine perfusion, a progressive rise in R_hyd indicates microvascular endothelial cell edema, vasospasm, or micro-thrombosis, warning clinicians of severe ischemia-reperfusion injury and potential graft failure."}
            ],
            "precautions": [
                "Ensure all microscopic air bubbles are purged; an air bubble lodged in a 120 μm channel causes capillary locking and huge resistance spikes.",
                "Maintain constant fluid temperature at 37.0 °C to avoid temperature-dependent viscosity variations.",
                "Verify that differential pressure transducer ports are purged of bubbles and leveled at identical gravitational heights.",
                "Do not exceed 15 mL/min to prevent over-pressurization of the microfluidic PDMS-to-glass bonding interface."
            ],
            "limitations": [
                "Hagen-Poiseuille law assumes a rigid, circular, straight tube; physiological blood vessels are compliant, branching, and tapered.",
                "Assumes steady, non-pulsatile flow, whereas cardiac output generates pulsatile pressure and flow waves.",
                "Tested using homogeneous Newtonian saline; whole blood displays non-Newtonian Fahraeus-Lindqvist cellular effects in microvessels.",
                "Neglects endothelial surface glycocalyx layer brush resistance found in living microvessels."
            ],
            "quiz": [
                {
                    "question": "According to the Hagen-Poiseuille law, what happens to flow resistance if a vessel's radius is halved?",
                    "options": ["Resistance doubles (2x)", "Resistance quadruples (4x)", "Resistance increases 16-fold (16x)", "Resistance drops to zero"],
                    "correct": 2,
                    "explanation": "Resistance scales with the inverse fourth power of radius (1/r⁴); reducing radius by half increases resistance by 2⁴ = 16 times."
                },
                {
                    "question": "Which vascular segment provides the greatest contribution to total peripheral resistance in the human body?",
                    "options": ["Precapillary arterioles", "Large elastic aorta", "Vena cava veins", "Pulmonary capillaries"],
                    "correct": 0,
                    "explanation": "Muscular arterioles account for approximately 60% of total systemic peripheral resistance and regulate local tissue perfusion."
                },
                {
                    "question": "If a flow rate of 10.0 mL/min produces a pressure drop of 36.00 kPa, what is hydraulic resistance R_hyd?",
                    "options": ["1.800 kPa/(mL/min)", "3.600 kPa/(mL/min)", "7.200 kPa/(mL/min)", "36.00 kPa/(mL/min)"],
                    "correct": 1,
                    "explanation": "R_hyd = ΔP / Q = 36.00 kPa / 10.0 mL/min = 3.6000 kPa/(mL/min)."
                },
                {
                    "question": "Why is flow through microvessels strictly laminar rather than turbulent?",
                    "options": ["Because Reynolds number Re is far below 2000 (typically Re < 10) due to small lumen diameter", "Because blood contains red cells", "Because veins have valves", "Because vessels are blue"],
                    "correct": 0,
                    "explanation": "Due to microscopic vessel diameters (D < 150 μm), the Reynolds number is very small (Re ≪ 2000), keeping flow deeply laminar."
                }
            ],
            "settings": ["Cartridge: Biomimetic PDMS microvascular array (8 parallel 120 μm channels, L = 40 mm)", "Fluid: Degassed physiological saline (μ = 0.0010 Pa·s at 37.0 °C)", "Pump: Dual-syringe pulseless syringe driver"],
            "samples": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🔬", "label": "1. Microvascular Perfusion Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Pressure Drop vs Flow"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Poiseuille r⁴ Sandbox"}
            ]
        },
        {
            "number": 29,
            "slug": "windkessel-lumped-parameter-arterial-compliance",
            "title": "Two-Element Windkessel Lumped-Parameter Arterial Compliance & Diastolic Decay",
            "shortTitle": "Windkessel Arterial Compliance",
            "aim": "Determine the arterial Windkessel decay rate constant k_w and evaluate total systemic arterial compliance C_a from the exponential diastolic pressure runoff curve.",
            "inputLabel": "Diastolic Decay Time t",
            "shortInput": "Time t",
            "inputUnit": "ms",
            "min": 100.0,
            "max": 600.0,
            "step": 100.0,
            "initial": 300.0,
            "inputDecimals": 1,
            "rawLabel": "Arterial Pressure Ratio P/P_es",
            "rawUnit": "ratio",
            "rawDecimals": 4,
            "xAxis": "Diastolic decay time t (ms)",
            "yAxis": "Natural log pressure ratio ln(P/P_es)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 350.0,
            "emptyY": -0.45,
            "targetName": "Windkessel Diastolic Decay Rate k_w",
            "target": "0.00125",
            "refValue": 0.00125,
            "resultUnit": "ms⁻¹",
            "resultDecimals": 5,
            "resultScale": 1.0,
            "fitEquation": "ln(P/P_es) = -k_w · t = -0.00125 · t",
            "measureLabel": "Sample Diastolic Pressure Runoff",
            "intro": "In cardiovascular hemodynamics, Otto Frank's classic 1899 Windkessel model represents the arterial system as an elastic reservoir (analogous to the antique German fire-engine air chamber, 'Windkessel') that cushions pulsatile stroke volume from the left ventricle into continuous peripheral capillary perfusion. In the two-element Windkessel circuit, the systemic vasculature is modeled as a parallel electrical analog: total arterial compliance C_a (capacitance, storing elastic strain energy during systolic distension) discharging through total peripheral resistance R_p (resistor, representing arteriolar resistance) to central venous pressure. During diastole, the aortic valve is closed, ventricular ejection is zero, and the elastic recoil of the stretched aorta and large conduit arteries drives blood into the periphery. The governing differential equation during diastole is C_a · (dP/dt) + P/R_p = 0. Solving this gives an exponential pressure decay: P(t) = P_es · exp[-t / (R_p · C_a)], where P_es is end-systolic incisura pressure at t = 0 (aortic dicrotic notch) and τ = R_p · C_a is the arterial time constant (typically 800 ms in healthy young adults). Taking the natural logarithm linearizes the decay: ln(P/P_es) = -k_w · t, where k_w = 1 / (R_p · C_a) is the diastolic runoff rate constant (ms⁻¹). In this laboratory investigation, an instrumented cardiovascular pulse simulator reproduces systemic aortic pressure waves to evaluate diastolic pressure runoff and determine compliance C_a.",
            "modelExtra": "Evaluated on a mock cardiovascular circulatory flow loop with a silicone elastic aorta and variable peripheral resistance valve. Systemic parameters: peripheral resistance R_p = 1.00 mmHg·s/mL (133.3 kPa·s/L), end-systolic dicrotic notch pressure P_es = 100 mmHg. Diastolic time constant τ = R_p · C_a = 800 ms, yielding decay rate k_w = 1/800 ms = 0.00125 ms⁻¹ (arterial compliance C_a = 1.067 mL/mmHg). Evaluated across times 100 to 600 ms.",
            "apparatus": [
                {"name": "Cardiovascular Mock Circulatory Flow Simulator", "purpose": "Replicates left ventricular stroke volume, tri-leaflet aortic valve, and systemic impedance."},
                {"name": "Compliant Silicone Aortic Phantom Chamber", "purpose": "Provides physiological elastic capacitance (compliance C_a ~ 1.0 mL/mmHg) storing systolic volume."},
                {"name": "Adjustable Micro-Precision Peripheral Resistance Valve", "purpose": "Calibrates total peripheral resistance R_p to standard physiological value (1.00 mmHg·s/mL)."},
                {"name": "Catheter-Tipped Solid-State Pressure Transducer (Millar Mikro-Tip)", "purpose": "Records high-fidelity intravascular pressure waveforms at 2000 Hz with zero fluid inertia."},
                {"name": "Pneumatic Piston Left Ventricle Pulsatile Driver", "purpose": "Generates 70 mL stroke volumes at 72 beats/min with realistic systolic ejection and diastolic rest times."},
                {"name": "Synchronous ECG & Aortic Waveform Telemetry Workstation", "purpose": "Identifies dicrotic notch incisura and isolates diastolic exponential decay segments."}
            ],
            "procedure": [
                {"title": "Circulatory Loop Priming and Transducer Calibration", "text": "Prime flow loop with 40% glycerol-water blood analog (viscosity 3.8 cP at 22 °C), purge air, and calibrate Millar pressure transducer against mercury manometer."},
                {"title": "Ventricular Hemodynamic Stabilization", "text": "Set pneumatic driver to 72 BPM (stroke volume 70 mL, systolic duration 300 ms, diastolic duration 533 ms); verify stable 120/80 mmHg aortic pressure wave."},
                {"title": "Dicrotic Notch Incisura Identification", "text": "Locate the dicrotic notch (closure of aortic valve) marking end-systole (t = 0, P_es = 100.0 mmHg) to define the onset of pure diastolic runoff."},
                {"title": "Diastolic Pressure Waveform Sampling", "text": "Sample decaying arterial pressure P(t) at standardized post-incisura intervals: t = 100, 200, 300, 400, 500, and 600 ms across 10 cardiac cycles."},
                {"title": "Logarithmic Transformation Calculation", "text": "Compute normalized pressure ratio P(t)/P_es and take natural logarithm y = ln(P/P_es) at each time step."},
                {"title": "Windkessel Decay Regression Analysis", "text": "Plot ln(P/P_es) versus decay time t, determine slope -k_w via linear regression, and calculate total arterial compliance C_a = 1 / (R_p · k_w)."}
            ],
            "topics": [
                {"question": "What is the physiological function of the Windkessel effect in the human aorta?", "answer": "The compliant aorta absorbs approximately 50% of left ventricular stroke volume during systole, storing it as potential elastic energy. During diastole, elastic recoil discharges this stored blood into capillaries, maintaining continuous tissue perfusion and converting pulsatile flow into steady flow."},
                {"question": "How does arterial stiffening in aging alter pulse pressure and cardiac workload?", "answer": "Aging causes fragmentation of elastin fibers and accumulation of stiff collagen in the aortic wall, decreasing compliance C_a. With less cushioning capacity, systolic pressure spikes (isolated systolic hypertension) while diastolic pressure falls, widening pulse pressure and increasing left ventricular afterload."},
                {"question": "What is the physical meaning of the arterial time constant τ = R_p · C_a?", "answer": "The time constant τ represents the time required for arterial pressure to decay to 1/e (~36.8%) of its initial value during un-interrupted diastole; a longer time constant indicates a highly compliant aorta and healthy peripheral resistance."},
                {"question": "What marks the transition from systole to diastole on the aortic pressure waveform?", "answer": "The dicrotic notch (incisura) marks the abrupt closure of the aortic valve following left ventricular pressure decline, physically isolating the arterial reservoir from the heart and initiating pure Windkessel diastolic decay."},
                {"question": "Why is the two-element Windkessel model insufficient at high frequencies?", "answer": "The two-element model treats the arterial tree as a single lumped compartment with infinite wave speed, neglecting arterial wave propagation and aortic characteristic impedance Z_c; modern models add a third element (Z_c in series) or fourth element (inertance)."},
                {"question": "How is total peripheral resistance R_p calculated clinically?", "answer": "R_p is calculated by dividing mean arterial pressure minus central venous pressure by cardiac output: R_p = (MAP - CVP) / CO, expressed in Wood units or mmHg·s/mL."}
            ],
            "precautions": [
                "Ensure zero air bubbles in the aortic silicone chamber; stray air acts as an uncalibrated pneumatic spring that falsely inflates compliance.",
                "Identify the dicrotic notch accurately; including late-systolic ejection data distorts the pure exponential decay regression.",
                "Verify that Millar solid-state pressure catheter is zeroed at mid-aortic height to avoid hydrostatic pressure offsets.",
                "Maintain constant stroke volume and heart rate throughout the logging sequence."
            ],
            "limitations": [
                "The two-element Windkessel model neglects wave reflection phenomena that create localized systolic pressure amplification in peripheral arteries.",
                "Assumes linear elastic compliance C_a, whereas biological arterial walls exhibit non-linear strain-stiffening elastin-collagen recruitment.",
                "Neglects blood inertance (fluid acceleration mass), which becomes significant during rapid early systolic ejection.",
                "Applies to diastole when aortic valve is closed; cannot model systolic ventricular-vascular interaction without impedance elements."
            ],
            "quiz": [
                {
                    "question": "What mathematical function describes arterial pressure decay during diastole in the two-element Windkessel model?",
                    "options": ["Exponential decay: P(t) = P_es · exp(-t / τ)", "Linear ramp: P(t) = P_es - m·t", "Sine wave oscillation", "Cubic polynomial"],
                    "correct": 0,
                    "explanation": "During diastole with the aortic valve closed, arterial compliance discharges through peripheral resistance as a classic exponential decay."
                },
                {
                    "question": "What happens to aortic compliance C_a as humans age and develop arteriosclerosis?",
                    "options": ["Compliance decreases as elastic fibers degrade and collagen stiffens", "Compliance increases tenfold", "Compliance converts to electrical voltage", "Compliance remains identical to birth"],
                    "correct": 0,
                    "explanation": "Arteriosclerosis stiffens conduit arteries by degrading elastin and cross-linking collagen, significantly reducing arterial compliance C_a."
                },
                {
                    "question": "If the diastolic decay rate constant is k_w = 0.00125 ms⁻¹, what is the arterial time constant τ?",
                    "options": ["125 ms", "400 ms", "800 ms", "1250 ms"],
                    "correct": 2,
                    "explanation": "τ = 1 / k_w = 1 / (0.00125 ms⁻¹) = 800 ms."
                },
                {
                    "question": "What anatomical event causes the dicrotic notch (incisura) on the aortic pressure tracing?",
                    "options": ["Abrupt closure of the aortic valve", "Opening of the mitral valve", "Contraction of the atria", "Heel strike during walking"],
                    "correct": 0,
                    "explanation": "The dicrotic notch is caused by transient backflow and sharp closure of the aortic valve leaflets at the end of ventricular systole."
                }
            ],
            "settings": ["System: Mock circulatory flow loop with silicone aorta", "Parameters: R_p = 1.00 mmHg·s/mL, P_es = 100.0 mmHg, HR = 72 BPM", "Sensor: Millar Mikro-Tip catheter pressure transducer (2000 Hz)"],
            "samples": [100.0, 200.0, 300.0, 400.0, 500.0, 600.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💓", "label": "1. Mock Circulatory Loop"},
                {"id": "compare", "icon": "📊", "label": "2. Diastolic Pressure Decay"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Windkessel R-C Sandbox"}
            ]
        },
        {
            "number": 30,
            "slug": "mechanical-heart-valve-steady-flow-pressure-drop",
            "title": "Bileaflet Mechanical Heart Valve Steady-Flow Pressure Drop & Orifice Area",
            "shortTitle": "Heart Valve Steady Pressure Drop",
            "aim": "Measure the transvalvular pressure gradient ΔP across a 25 mm bileaflet mechanical aortic heart valve under steady forward flow and evaluate the quadratic Bernoulli loss coefficient k_v.",
            "inputLabel": "Transvalvular Jet Velocity v",
            "shortInput": "Velocity v",
            "inputUnit": "m/s",
            "min": 1.0,
            "max": 2.0,
            "step": 0.2,
            "initial": 1.4,
            "inputDecimals": 1,
            "rawLabel": "Transvalvular Pressure Drop ΔP",
            "rawUnit": "mmHg",
            "rawDecimals": 3,
            "xAxis": "Square of transvalvular velocity v² (m²/s²)",
            "yAxis": "Transvalvular pressure drop ΔP (mmHg)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 2.5,
            "emptyY": 10.0,
            "targetName": "Bernoulli Pressure Loss Coefficient k_v",
            "target": "3.8500",
            "refValue": 3.8500,
            "resultUnit": "mmHg/(m²/s²)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ΔP = k_v · v² = 3.8500 · v²",
            "measureLabel": "Measure Valve Pressure Drop",
            "intro": "Valvular heart disease (such as calcific aortic stenosis) impairs unidirectional intracardiac hemodynamics, requiring surgical replacement with prosthetic heart valves. Bileaflet mechanical heart valves (such as the St. Jude Medical or CarboMedics pyrolytic carbon designs) are widely implanted due to their exceptional structural durability and life expectancy (> 25 years). However, prosthetic valves introduce geometric flow restrictions: the valve sewing ring, leaflet pivot hinges, and central open leaflets create flow separation, turbulent dissipation, and elevated transvalvular pressure gradients. According to the Gorlin formula and modified Bernoulli equation commonly utilized in clinical cardiology and ISO 5840 testing, the steady-flow pressure drop ΔP across a stenotic orifice or prosthetic valve is governed by convective acceleration and turbulent kinetic energy dissipation: ΔP = (ρ / 2·C_d²) · v² = k_v · v², where ρ is blood fluid density, C_d is the discharge coefficient, v is the peak transvalvular jet velocity (m/s), and k_v is the quadratic pressure loss coefficient (mmHg/(m²/s²)). In clinical echocardiography, the simplified Bernoulli formula ΔP ≈ 4·v² (assuming blood density ρ ≈ 1060 kg/m³) is universally used to estimate peak valve gradients. In this laboratory investigation, a 25 mm pyrolytic carbon bileaflet aortic valve mounted in an ISO 5840 steady-flow testing chamber evaluates transvalvular pressure drop across velocities from 1.0 to 2.0 m/s to determine k_v and effective orifice area (EOA).",
            "modelExtra": "Evaluated on a 25 mm bileaflet pyrolytic carbon mechanical aortic valve mounted in an acrylic aortic root chamber meeting ISO 5840 standards. Perfusion fluid is 36% glycerol blood analog (density ρ = 1055 kg/m³, viscosity 3.6 cP at 37 °C). Velocities v = 1.0, 1.2, 1.4, 1.6, 1.8, 2.0 m/s correspond to v² = 1.00, 1.44, 1.96, 2.56, 3.24, 4.00 m²/s². Quadratic Bernoulli slope k_v = 3.8500 mmHg/(m²/s²).",
            "apparatus": [
                {"name": "ISO 5840 Steady-Flow Heart Valve Test Rig", "purpose": "Provides straight upstream and anatomical sinus of Valsalva downstream flow conduits with pressure taps."},
                {"name": "25 mm Pyrolytic Carbon Bileaflet Mechanical Aortic Valve", "purpose": "Clinical prosthesis with dual semicircular pyrolytic carbon leaflets and Dacron sewing cuff."},
                {"name": "Variable-Speed Centrifugal Perfusion Pump", "purpose": "Supplies stable, continuous non-pulsatile forward flow from 5 to 35 L/min."},
                {"name": "Differential Wet-Wet Differential Pressure Transducer", "purpose": "Measures transvalvular pressure drop ΔP with pressure taps located 1 diameter upstream and 3 diameters downstream."},
                {"name": "Ultrasonic Clamp-On Flowmeter (Transonic Systems)", "purpose": "Measures volumetric forward flow rate Q with 1% accuracy and sub-millisecond response."},
                {"name": "Thermostatically Controlled Glycerol-Water Reservoir (37.0 °C)", "purpose": "Maintains fluid density ρ = 1055 kg/m³ and blood-analog viscosity 3.6 cP."}
            ],
            "procedure": [
                {"title": "Valve Mounting and Alignment Verification", "text": "Mount 25 mm mechanical valve securely in acrylic test chamber, ensuring leaflets open symmetrically without sewing ring impingement."},
                {"title": "Perfusion Fluid Priming and Temperature Stabilization", "text": "Fill system with 36% glycerol-water blood analog, purge all trapped air from pressure lines, and heat reservoir to 37.0 °C."},
                {"title": "Zero Differential Pressure Baseline", "text": "Open transducer bypass valve at zero flow to establish precise 0.00 mmHg baseline differential pressure."},
                {"title": "Velocity Increment and Stabilization", "text": "Adjust centrifugal pump to establish transvalvular jet velocity v = 1.0 m/s (verified by flowmeter Q and effective orifice area) and record steady pressure drop ΔP."},
                {"title": "Velocity Progression Sequence", "text": "Increment jet velocity through 1.2, 1.4, 1.6, 1.8, and 2.0 m/s, recording stabilized pressure gradient ΔP over 30 seconds at each step."},
                {"title": "Bernoulli Quadratic Regression Analysis", "text": "Plot transvalvular pressure drop ΔP against v², compute the slope k_v via linear regression through the origin, and calculate effective orifice area EOA."}
            ],
            "topics": [
                {"question": "How does the simplified Bernoulli equation ΔP = 4·v² derive from fluid mechanics?", "answer": "The unsteady Bernoulli equation for a streamline through an orifice is ΔP = 1/2·ρ·(v₂² - v₁²). Assuming upstream velocity v₁ ≪ v₂ and substituting blood density ρ = 1060 kg/m³: ΔP = 0.5 · 1060 · v² N/m² = 530 · v² Pa. Converting Pascals to mmHg (1 mmHg = 133.32 Pa) gives ΔP = (530 / 133.32) · v² = 3.975 · v² ≈ 4 · v²."},
                {"question": "What is the difference between geometric orifice area (GOA) and effective orifice area (EOA)?", "answer": "GOA is the physical internal cross-sectional area of the open valve ring, whereas EOA is the minimal cross-sectional area of the downstream jet core at the vena contracta (EOA = C_d · GOA); EOA is always smaller than GOA due to flow separation and contraction."},
                {"question": "What causes the pressure recovery phenomenon downstream of a prosthetic valve?", "answer": "At the vena contracta, velocity is maximal and pressure is minimal. As the jet expands into the downstream ascending aorta, some kinetic energy decelerates and converts back into static pressure (pressure recovery), causing downstream pressure to be higher than at the vena contracta."},
                {"question": "Why do mechanical valves carry a lifetime risk of thromboembolism requiring anticoagulation?", "answer": "High shear stresses through narrow leaflet pivot gaps activate platelets, while recirculation vortices and stagnation zones downstream of leaflets trap activated clotting factors, promoting thrombus formation unless the patient takes oral anticoagulants (e.g., warfarin)."},
                {"question": "What is the distinction between a bileaflet mechanical valve and a bioprosthetic tissue valve?", "answer": "Bileaflet valves are made of rigid pyrolytic carbon with indefinite fatigue life but require lifelong anticoagulation, whereas bioprosthetic valves (bovine pericardium or porcine aortic roots) provide physiological central flow without lifelong anticoagulation but suffer calcific structural deterioration within 10 to 15 years."},
                {"question": "What standard governs hydrodynamic testing of prosthetic heart valves?", "answer": "ISO 5840 ('Cardiovascular implants — Cardiac valve prostheses') prescribes international standards for steady-flow pressure drop, pulsatile flow simulator performance, regurgitant fraction, and accelerated wear endurance testing."}
            ],
            "precautions": [
                "Purge all air from differential pressure lines; bubbles act as capacitive dampers that severely distort pressure readings.",
                "Position pressure taps strictly according to ISO 5840 (1 diameter upstream, 3 diameters downstream) to capture true net unrecovered loss.",
                "Verify leaflet mobility before testing; ensure pyrolytic carbon leaflets pivot freely to their maximum 85° opening angle.",
                "Keep fluid temperature precisely at 37.0 °C to stabilize blood-analog viscosity and density."
            ],
            "limitations": [
                "Steady forward flow does not simulate transient valve opening/closing leaflet dynamics or dynamic regurgitation phases.",
                "Assumes rigid aortic root chamber, neglecting the natural compliance and expansion of the biological sinus of Valsalva.",
                "Glycerol blood analog reproduces bulk viscosity and density but does not simulate cellular platelet activation or shear-induced hemolysis.",
                "Does not account for non-axial inflow skewing caused by asymmetric left ventricular outflow tract (LVOT) geometry."
            ],
            "quiz": [
                {
                    "question": "What is the simplified Bernoulli relationship used in clinical cardiology to relate peak velocity v to pressure gradient ΔP?",
                    "options": ["ΔP ≈ 4 · v² (in mmHg for v in m/s)", "ΔP = 10 · v", "ΔP = v / 4", "ΔP = 133.3 · v"],
                    "correct": 0,
                    "explanation": "The simplified Bernoulli equation ΔP ≈ 4·v² converts transvalvular jet velocity in m/s into pressure gradient in mmHg."
                },
                {
                    "question": "Why is the Effective Orifice Area (EOA) always smaller than the Geometric Orifice Area (GOA)?",
                    "options": ["Due to streamline contraction at the vena contracta and flow separation", "Because the valve shrinks in warm fluid", "Because blood evaporates", "Due to acoustic interference"],
                    "correct": 0,
                    "explanation": "Flow separation and fluid vena contracta contraction restrict the effective cross-sectional flow area below the physical geometric area."
                },
                {
                    "question": "If a jet velocity of v = 1.40 m/s (v² = 1.96 m²/s²) produces a pressure drop of 7.546 mmHg, what is k_v?",
                    "options": ["1.925 mmHg/(m²/s²)", "3.850 mmHg/(m²/s²)", "7.700 mmHg/(m²/s²)", "15.40 mmHg/(m²/s²)"],
                    "correct": 1,
                    "explanation": "k_v = ΔP / v² = 7.546 mmHg / 1.96 m²/s² = 3.8500 mmHg/(m²/s²)."
                },
                {
                    "question": "What material is universally used for the leaflets and housing of modern mechanical heart valves?",
                    "options": ["Pyrolytic carbon", "Cast iron", "Polystyrene plastic", "Solid gold"],
                    "correct": 0,
                    "explanation": "Pyrolytic carbon possesses exceptional thromboresistance, fatigue strength, and wear resistance, making it the premier material for mechanical heart valves."
                }
            ],
            "settings": ["Prosthesis: 25 mm bileaflet pyrolytic carbon aortic valve", "Test chamber: ISO 5840 rigid aortic root with sinus of Valsalva", "Perfusion fluid: 36% glycerol-water (ρ = 1055 kg/m³, μ = 3.6 cP at 37 °C)"],
            "samples": [1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "❤️", "label": "1. ISO 5840 Flow Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Bernoulli v² Pressure Drop"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Orifice EOA Sandbox"}
            ]
        },
        {
            "number": 31,
            "slug": "pulse-wave-velocity-arterial-stiffness-moens-korteweg",
            "title": "Carotid-Femoral Pulse Wave Velocity & Moens-Korteweg Arterial Stiffness",
            "shortTitle": "Pulse Wave Velocity Arterial Stiffness",
            "aim": "Determine carotid-femoral pulse wave velocity (cfPWV) across varying mean arterial pressures (MAP) using dual applanation tonometry and evaluate pressure-dependent vascular stiffening.",
            "inputLabel": "Mean Arterial Pressure MAP",
            "shortInput": "Pressure MAP",
            "inputUnit": "mmHg",
            "min": 70.0,
            "max": 120.0,
            "step": 10.0,
            "initial": 90.0,
            "inputDecimals": 1,
            "rawLabel": "Carotid-Femoral PWV",
            "rawUnit": "m/s",
            "rawDecimals": 3,
            "xAxis": "Mean arterial pressure MAP (mmHg)",
            "yAxis": "Carotid-femoral PWV (m/s)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 95.0,
            "emptyY": 7.0,
            "targetName": "PWV-Pressure Sensitivity Slope k_p",
            "target": "0.0450",
            "refValue": 0.0450,
            "resultUnit": "(m/s)/mmHg",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "PWV = k_p · MAP + PWV_0 = 0.0450 · MAP + 2.8000",
            "measureLabel": "Record Arterial Pulse Waves",
            "intro": "In cardiovascular medicine and epidemiology, arterial stiffness is an independent predictor of coronary artery disease, stroke, renal failure, and all-cause cardiovascular mortality. The gold-standard non-invasive clinical metric of central aortic stiffness is carotid-femoral Pulse Wave Velocity (cfPWV). When the left ventricle ejects blood into the ascending aorta, it initiates a mechanical pressure pulse wave that travels down the arterial tree at a speed governed by the elastic properties of the vascular wall and blood density. According to the classical Moens-Korteweg equation and the Bramwell-Hill relationship: PWV = √[E · h / (2 · r · ρ)], where E is the incremental Young's modulus of the arterial wall, h is wall thickness, r is lumen radius, and ρ is blood density. Because the arterial wall is a non-linear viscoelastic biomaterial composed of distensible elastin fibers and stiff collagen fibrils, vascular stiffness increases with transmural distending pressure: at higher blood pressure, collagen fibers are progressively recruited, increasing apparent Young's modulus E. Consequently, empirical clinical data demonstrate that cfPWV scales linearly with mean arterial pressure (MAP): PWV = k_p · MAP + PWV_0, where k_p is the pressure sensitivity coefficient ((m/s)/mmHg). In this laboratory investigation, dual-channel applanation tonometry on an instrumented cardiovascular simulator tracks carotid and femoral pressure foot transit times across varying MAP to determine cfPWV and evaluate k_p.",
            "modelExtra": "Evaluated on a simulated human arterial tree phantom with anatomically branched elastic silicone aorta, carotid, and femoral conduits (effective carotid-to-femoral transit distance Δx = 0.450 m). Mean arterial pressure MAP controlled from 70.0 to 120.0 mmHg. Pressure-dependent PWV scaling slope k_p = 0.0450 (m/s)/mmHg with baseline PWV_0 = 2.8000 m/s (PWV = 6.85 m/s at normotensive MAP = 90 mmHg).",
            "apparatus": [
                {"name": "Dual High-Fidelity Applanation Tonometers (Millar SPT-301)", "purpose": "Applanates surface of superficial arteries (carotid and femoral) to record non-distorted pulse waveforms."},
                {"name": "Cardiovascular Arterial Tree Hemodynamic Simulator", "purpose": "Provides anatomically scaled compliant conduits with independent mean pressure and pulse pressure control."},
                {"name": "Precision Caliper & Tape Transit Distance Gauge", "purpose": "Measures anatomical carotid-to-femoral surface distance Δx with millimeter accuracy."},
                {"name": "Synchronous Dual-Channel High-Speed Bio-Amplifier (2000 Hz)", "purpose": "Digitizes simultaneous carotid and femoral pulse waves with sub-millisecond time resolution."},
                {"name": "Automated Foot-to-Foot Waveform Intersection Algorithm", "purpose": "Identifies initial systolic upstroke inflection point (transit time foot) via intersecting tangent method."},
                {"name": "Continuous Arterial Line Reference Transducer", "purpose": "Measures true transmural mean arterial pressure (MAP) to ±0.1 mmHg."}
            ],
            "procedure": [
                {"title": "Anatomical Transit Distance Calibration", "text": "Measure superficial surface distance from suprasternal notch to carotid site and from suprasternal notch to femoral site; calculate net aortic transit distance Δx = 0.450 m."},
                {"title": "Applanation Tonometer Positioning", "text": "Position tonometer probes over the right common carotid artery and right femoral artery, adjusting hold-down pressure until maximum signal amplitude is registered."},
                {"title": "Baseline MAP Stabilization", "text": "Set circulatory simulator mean arterial pressure to 70.0 mmHg and verify stable heart rate (70 BPM) and cardiac output."},
                {"title": "Synchronous Foot-to-Foot Transit Time Capture", "text": "Record 10 consecutive pulse wave pairs at 2000 Hz; execute intersecting tangent algorithm to detect foot transit time delay Δt, calculating PWV = Δx / Δt."},
                {"title": "Mean Arterial Pressure Progression", "text": "Increment circulatory MAP through 80, 90, 100, 110, and 120 mmHg, capturing stabilized cfPWV over 10 cycles at each pressure step."},
                {"title": "Pressure Sensitivity Linear Regression", "text": "Plot cfPWV versus MAP and determine the vascular pressure sensitivity slope k_p and baseline velocity PWV_0 via linear regression."}
            ],
            "topics": [
                {"question": "How does the Moens-Korteweg equation relate wave velocity to vascular stiffness?", "answer": "The equation PWV = √[E·h / (2·r·ρ)] demonstrates that wave speed is proportional to the square root of wall elastic modulus E; stiffer arteries transmit pressure waves significantly faster than compliant, distensible vessels."},
                {"question": "Why does pulse wave velocity increase with higher blood pressure?", "answer": "The arterial wall contains stretchy elastin and stiff collagen. At low pressure, elastin carries the load; as transmural pressure rises, the vessel expands and uncoils wavy collagen fibers, which are 100 to 1000 times stiffer than elastin, dramatically increasing effective wall modulus E."},
                {"question": "What is the 'foot-to-foot' method in clinical PWV measurement?", "answer": "The foot of the arterial pulse waveform represents the earliest onset of systolic upstroke, generated before wave reflections return from peripheral vascular beds; measuring the transit time delay between carotid and femoral wave feet avoids reflection interference."},
                {"question": "Why is cfPWV considered the clinical gold standard over brachial-ankle PWV?", "answer": "Carotid-femoral PWV travels directly through the thoracic and abdominal aorta, the central elastic reservoir responsible for buffering cardiac output; brachial-ankle PWV traverses muscular peripheral arteries that do not reflect central aortic stiffness."},
                {"question": "What is the threshold for abnormal aortic stiffness in clinical hypertension guidelines?", "answer": "The European Society of Cardiology (ESC) defines a cfPWV exceeding 10.0 m/s as an established threshold for asymptomatic hypertension-mediated target organ damage in adults."},
                {"question": "How do reflected pressure waves contribute to central systolic hypertension?", "answer": "In young compliant arteries, slow wave velocity causes reflections to return during diastole, boosting coronary perfusion; in stiff arteries, rapid PWV causes reflections to return during late systole, augmenting peak systolic aortic pressure and increasing myocardial oxygen demand."}
            ],
            "precautions": [
                "Accurately determine surface transit distance Δx; distance measurement error is the largest contributor to clinical PWV uncertainty.",
                "Ensure consistent tonometer probe hold-down pressure to prevent artificial flattening or distortion of pulse wave upstrokes.",
                "Verify that ECG R-wave or simultaneous dual-tonometer channels are perfectly synchronized without inter-channel clock skew.",
                "Allow 3 minutes of hemodynamic stabilization after altering simulator MAP before logging pulse wave transit times."
            ],
            "limitations": [
                "The linear PWV-MAP relationship applies over physiological pressure ranges (70 to 120 mmHg); extreme pressures display exponential stiffening.",
                "Assumes uniform aortic diameter and wall thickness, whereas the human aorta tapers continuously from root to bifurcation.",
                "Surface distance measurement overestimates true internal curvilinear aortic path length in elderly patients with tortuous aortas.",
                "Does not account for local endothelial nitric oxide-mediated active vasomotor tone in living patients."
            ],
            "quiz": [
                {
                    "question": "What is the physical relationship between arterial wall stiffness (Young's modulus E) and Pulse Wave Velocity (PWV)?",
                    "options": ["PWV is proportional to the square root of Young's modulus (√E)", "PWV is inversely proportional to E", "PWV is completely independent of E", "PWV drops to zero in stiff vessels"],
                    "correct": 0,
                    "explanation": "According to the Moens-Korteweg equation, PWV = √[E·h / (2·r·ρ)]; stiffer vessels with higher E conduct pulse waves faster."
                },
                {
                    "question": "Why does carotid-femoral PWV increase at elevated blood pressures?",
                    "options": ["High pressure distends the arterial wall, recruiting stiff collagen fibers that elevate effective modulus E", "Blood thins out", "The heart stops beating", "Arteries become wider than veins"],
                    "correct": 0,
                    "explanation": "Increased transmural pressure stretches the vascular wall, transferring tensile stress from distensible elastin to much stiffer collagen fibers."
                },
                {
                    "question": "If MAP = 100 mmHg and measured PWV is 7.300 m/s with a baseline PWV_0 = 2.800 m/s, what is slope k_p?",
                    "options": ["0.0225 (m/s)/mmHg", "0.0450 (m/s)/mmHg", "0.0900 (m/s)/mmHg", "0.4500 (m/s)/mmHg"],
                    "correct": 1,
                    "explanation": "k_p = (PWV - PWV_0) / MAP = (7.300 - 2.800) / 100 = 4.500 / 100 = 0.0450 (m/s)/mmHg."
                },
                {
                    "question": "What clinical threshold for carotid-femoral PWV indicates target organ damage under ESC guidelines?",
                    "options": ["cfPWV > 10.0 m/s", "cfPWV > 2.0 m/s", "cfPWV > 50.0 m/s", "cfPWV > 100 m/s"],
                    "correct": 0,
                    "explanation": "European cardiology guidelines define cfPWV > 10.0 m/s as evidence of significant asymptomatic vascular target organ damage."
                }
            ],
            "settings": ["System: Compliant aortic tree phantom (effective transit distance Δx = 0.450 m)", "Tonometry: Millar SPT-301 dual high-fidelity applanation tonometers (2000 Hz)", "Hemodynamics: MAP varied from 70.0 to 120.0 mmHg, HR = 70 BPM"],
            "samples": [70.0, 80.0, 90.0, 100.0, 110.0, 120.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "📈", "label": "1. Dual Tonometry Rig"},
                {"id": "compare", "icon": "📊", "label": "2. PWV vs Blood Pressure"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Moens-Korteweg Sandbox"}
            ]
        },
        {
            "number": 32,
            "slug": "hollow-fiber-hemodialyzer-clearance-mass-transfer",
            "title": "Hollow-Fiber Hemodialyzer Urea Clearance & Mass Transfer Coefficient",
            "shortTitle": "Hemodialyzer Urea Clearance",
            "aim": "Evaluate small-solute (urea) clearance K_u of a clinical hollow-fiber hemodialyzer across varying blood flow rates Q_b at fixed dialysate flow rate Q_d.",
            "inputLabel": "Blood Compartment Flow Rate Q_b",
            "shortInput": "Blood Flow Q_b",
            "inputUnit": "mL/min",
            "min": 150.0,
            "max": 400.0,
            "step": 50.0,
            "initial": 250.0,
            "inputDecimals": 1,
            "rawLabel": "Dialytic Urea Clearance K_u",
            "rawUnit": "mL/min",
            "rawDecimals": 3,
            "xAxis": "Blood flow rate Q_b (mL/min)",
            "yAxis": "Urea clearance K_u (mL/min)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 275.0,
            "emptyY": 200.0,
            "targetName": "Clearance-Flow Sensitivity Slope m_c",
            "target": "0.5800",
            "refValue": 0.5800,
            "resultUnit": "ratio",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "K_u = m_c · Q_b + K_u0 = 0.5800 · Q_b + 42.0000",
            "measureLabel": "Measure Dialytic Clearance",
            "intro": "In end-stage renal disease (ESRD), loss of native renal function leads to fatal accumulation of uremic toxins, fluid overload, and electrolyte disturbances. Hemodialysis serves as life-sustaining renal replacement therapy by passing the patient's blood through an artificial kidney (hollow-fiber hemodialyzer) counter-current to an aqueous dialysate solution. A clinical dialyzer contains 10,000 to 15,000 semipermeable capillary fibers (inner diameter ~200 μm, wall thickness ~30 μm, effective surface area 1.5 to 2.0 m²) composed of synthetic polysulfone or polyethersulfone polymers. Solute removal is driven by diffusion across the membrane pore network down concentration gradients. The dialyzer clearance K of a solute (such as urea, MW 60 Da) is defined as the volume of blood completely cleared of solute per unit time: K = Q_bi · (C_bi - C_bo) / C_bi + Q_f · (C_bo / C_bi), where Q_bi is blood inlet flow, C_bi and C_bo are inlet and outlet solute concentrations, and Q_f is ultrafiltration rate. In the absence of ultrafiltration (pure diffusion), clearance depends on membrane mass transfer-area coefficient K_0·A, dialysate flow Q_d, and blood flow Q_b. Over typical clinical blood flows (150 to 400 mL/min) with high dialysate flow (Q_d = 500 mL/min), urea clearance scales linearly with blood pump delivery: K_u = m_c · Q_b + K_u0, where m_c is the flow sensitivity coefficient. In this laboratory experiment, a clinical dialysis machine test station evaluates hollow-fiber dialyzer urea mass transfer across blood flows from 150 to 400 mL/min.",
            "modelExtra": "Evaluated on a 1.8 m² high-flux polysulfone hollow-fiber hemodialyzer (Fresenius FX80, mass transfer-area coefficient K_0·A = 950 mL/min for urea). Constant counter-current dialysate flow Q_d = 500 mL/min at 37.0 °C with zero ultrafiltration (Q_f = 0). Linear blood flow clearance slope m_c = 0.5800 with baseline K_u0 = 42.0000 mL/min across blood flow rates Q_b from 150 to 400 mL/min.",
            "apparatus": [
                {"name": "Clinical Hemodialysis Delivery System Test Bench", "purpose": "Provides calibrated peristaltic blood pump and heated, degassed dialysate preparation system."},
                {"name": "High-Flux Polysulfone Hollow-Fiber Dialyzer (1.8 m²)", "purpose": "Contains ~12,000 semipermeable hollow fibers with 1.8 m² effective mass transfer surface area."},
                {"name": "Closed-Loop Synthetic Blood Reservoir (Urea 25.0 mmol/L)", "purpose": "Provides standardized blood substitute containing physiological electrolytes and clinical urea concentration."},
                {"name": "Counter-Current Dialysate Proportioning Circuit (500 mL/min)", "purpose": "Prepares bicarbonate-buffered dialysate at 37.0 °C and meters counter-current flow through shell side."},
                {"name": "Automated Spectrophotometric Enzymatic Urea Analyzer", "purpose": "Measures blood inlet (C_bi) and outlet (C_bo) urea concentrations using the urease-GLDH method."},
                {"name": "Dual Ultrasonic In-Line Flow Transducers", "purpose": "Continuously measures blood compartment flow Q_b and dialysate flow Q_d with 1 mL/min accuracy."}
            ],
            "procedure": [
                {"title": "Dialyzer Priming and Air Purging", "text": "Mount dialyzer vertically, prime blood side with 1 L heparinized saline at 150 mL/min to displace air, and invert to purge dialysate compartment."},
                {"title": "Dialysate Temperature and Flow Stabilization", "text": "Set dialysate delivery to 500 mL/min at 37.0 °C with bicarbonate conductivity 14.0 mS/cm and verify zero ultrafiltration transmembrane pressure."},
                {"title": "Blood Reservoir Urea Standardization", "text": "Prepare synthetic blood reservoir with urea concentration C_bi = 25.0 mmol/L (150 mg/dL BUN) at 37.0 °C under gentle magnetic stirring."},
                {"title": "Blood Flow Step Initialization", "text": "Set blood pump to delivery rate Q_b = 150 mL/min, circulate counter-current to dialysate, and allow 5 minutes for concentration steady state."},
                {"title": "Paired Blood Sampling and Urea Assay", "text": "Simultaneously sample inlet port (C_bi) and dialyzer outlet port (C_bo), assaying urea concentrations via spectrophotometric enzymatic assay to calculate clearance K_u."},
                {"title": "Blood Flow Progression and Regression Analysis", "text": "Repeat sampling at Q_b = 200, 250, 300, 350, and 400 mL/min, plot urea clearance K_u versus Q_b, and determine flow sensitivity slope m_c."},
                {"title": "Mass Transfer-Area Coefficient K_0·A Calculation", "text": "Verify dialyzer performance against the theoretical logarithmic mean mass transfer relation K_0·A = [Q_b·Q_d / (Q_d - Q_b)] · ln[(1 - K/Q_d)/(1 - K/Q_b)]."}
            ],
            "topics": [
                {"question": "Why is blood and dialysate flow arranged in a counter-current direction?", "answer": "Counter-current flow maintains a continuous concentration gradient (C_blood > C_dialysate) across the entire length of the hollow fibers, maximizing diffusion driving force and achieving significantly higher clearance than co-current flow."},
                {"question": "What is the mass transfer-area coefficient K_0·A of a hemodialyzer?", "answer": "K_0·A (expressed in mL/min) represents the maximum theoretical clearance achievable at infinite blood and dialysate flow rates; it quantifies the intrinsic membrane diffusive permeability K_0 multiplied by effective membrane surface area A."},
                {"question": "What is the difference between diffusive clearance and convective clearance in dialysis?", "answer": "Diffusive clearance relies on thermal random motion of solute molecules down a concentration gradient across the membrane (effective for small molecules like urea, 60 Da); convective clearance (hemofiltration) drags solutes across via bulk solvent ultrafiltration flow (solvent drag), effective for middle molecules like β₂-microglobulin (11.8 kDa)."},
                {"question": "Why does clearance level off as blood flow rate Q_b becomes very high?", "answer": "At high blood flow rates, solute removal becomes membrane-limited rather than flow-limited; the finite surface area and diffusion resistance of the fiber membrane restrict the rate of solute passage regardless of how rapidly blood is pumped through."},
                {"question": "What is the clinical definition and target for Kt/V in hemodialysis adequacy?", "answer": "Kt/V is a dimensionless index of dialysis adequacy, where K is dialyzer urea clearance (mL/min), t is treatment duration (min), and V is patient total body water urea distribution volume (mL); clinical guidelines recommend a minimum single-pool Kt/V ≥ 1.2 per treatment (delivered 1.4)."},
                {"question": "Why must dialysate be degassed before entering the hollow-fiber dialyzer?", "answer": "Heating cold water liberates dissolved air into micro-bubbles. In a dialyzer, air bubbles coat hollow-fiber exterior surfaces, blocking dialysate contact, reducing effective membrane area A, and creating false blood leak optical detector alarms."}
            ],
            "precautions": [
                "Ensure dialysate is thoroughly degassed; air bubbles trapped in the fiber bundle reduce effective surface area and impair clearance.",
                "Verify zero net ultrafiltration (Q_f = 0) so that measured solute clearance reflects pure diffusive mass transfer.",
                "Calibrate blood pump roller tubing occlusion; under-occlusion causes internal back-leakage and false blood delivery rate readings.",
                "Draw blood inlet and outlet samples simultaneously to account for any gradual drawdown in the recirculation reservoir."
            ],
            "limitations": [
                "The linear clearance-flow model applies across standard clinical blood flows (150 to 400 mL/min); at extreme flows (> 500 mL/min), clearance plateaus asymptotically.",
                "Assumes aqueous synthetic blood; whole human blood exhibits lower diffusive clearance due to red cell boundary layer resistance and cellular urea partitioning.",
                "Pure diffusion testing neglects convective solvent drag clearance present during clinical fluid removal (ultrafiltration).",
                "Dialyzer clearance degrades over successive reuse reprocessing due to residual fiber clotting and protein fouling."
            ],
            "quiz": [
                {
                    "question": "Why do clinical hemodialyzers utilize counter-current flow between blood and dialysate?",
                    "options": ["To maintain a concentration gradient along the entire fiber length, maximizing diffusive clearance", "To prevent the dialyzer from spinning", "To heat the blood faster", "To reduce electrical power consumption"],
                    "correct": 0,
                    "explanation": "Counter-current flow preserves a positive concentration driving gradient from blood to dialysate along the entire fiber bundle."
                },
                {
                    "question": "What is the molecular weight of urea, the primary small-solute marker for dialysis adequacy?",
                    "options": ["60 Daltons", "600 Daltons", "11,800 Daltons", "66,000 Daltons"],
                    "correct": 0,
                    "explanation": "Urea is a small, easily diffusible nitrogenous waste molecule with a molecular weight of 60 Da."
                },
                {
                    "question": "If blood flow Q_b is 300 mL/min and measured urea clearance is 216.0 mL/min with K_u0 = 42.0 mL/min, what is slope m_c?",
                    "options": ["0.2900", "0.5800", "0.7200", "1.1600"],
                    "correct": 1,
                    "explanation": "m_c = (K_u - K_u0) / Q_b = (216.0 - 42.0) / 300 = 174.0 / 300 = 0.5800."
                },
                {
                    "question": "What clinical metric expresses the fractional clearance of urea normalized to patient total body water?",
                    "options": ["Kt/V", "Reynolds Number", "Hagen-Poiseuille ratio", "Cardiac Index"],
                    "correct": 0,
                    "explanation": "Kt/V is the universally recognized dimensionless metric of dialysis dose adequacy, where V is total body water."
                }
            ],
            "settings": ["Dialyzer: High-flux polysulfone hollow-fiber cartridge (1.8 m²)", "Dialysate flow: Q_d = 500 mL/min at 37.0 °C (zero ultrafiltration, Q_f = 0)", "Solute: Urea in synthetic electrolyte buffer (C_bi = 25.0 mmol/L)"],
            "samples": [150.0, 200.0, 250.0, 300.0, 350.0, 400.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🧪", "label": "1. Hemodialysis Test Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Urea Clearance vs Flow"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Hollow-Fiber Mass Transfer"}
            ]
        },
        {
            "number": 33,
            "slug": "centrifugal-rotary-blood-pump-hemolysis-shear-stress",
            "title": "Centrifugal Continuous-Flow Rotary Blood Pump Head-Flow Characteristic",
            "shortTitle": "Rotary Blood Pump Head-Flow",
            "aim": "Determine the shut-off pressure head scaling constant k_N of a magnetically levitated continuous-flow rotary blood pump (LVAD) across operating speeds.",
            "inputLabel": "Impeller Rotational Speed N",
            "shortInput": "Speed N",
            "inputUnit": "k-RPM",
            "min": 2.0,
            "max": 4.5,
            "step": 0.5,
            "initial": 3.0,
            "inputDecimals": 1,
            "rawLabel": "Zero-Flow Shut-Off Head H₀",
            "rawUnit": "mmHg",
            "rawDecimals": 3,
            "xAxis": "Square of rotational speed N² (k-RPM²)",
            "yAxis": "Shut-off pressure head H₀ (mmHg)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 10.0,
            "emptyY": 75.0,
            "targetName": "Rotary Pump Head Scaling Factor k_N",
            "target": "7.5000",
            "refValue": 7.5000,
            "resultUnit": "mmHg/k-RPM²",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "H₀ = k_N · N² = 7.5000 · N² (where N is in k-RPM = RPM/1000)",
            "measureLabel": "Measure Blood Pump Head",
            "intro": "In advanced heart failure management, Left Ventricular Assist Devices (LVADs) provide mechanical circulatory support as a bridge to heart transplantation or lifelong destination therapy. Modern third-generation LVADs (such as the Abbott HeartMate 3) utilize continuous-flow centrifugal rotary blood pumps featuring magnetically levitated (MagLev) impellers with wide fluid flow passages and no mechanical contact bearings. The rotating impeller imparts centrifugal kinetic energy to blood, converting velocity into pressure head across the volute housing to pump blood from the left ventricular apex into the ascending aorta. According to Euler's turbomachinery head equation and pump affinity laws, the hydrodynamic pressure head generated by a centrifugal pump at zero volumetric delivery (shut-off head H_0) is governed by centrifugal kinetic energy, scaling strictly with the square of impeller angular velocity: H_0 = (u₂² / 2·g) = k_N · N², where N is impeller speed in thousands of revolutions per minute (k-RPM = RPM/1000) and k_N is the pump head scaling coefficient (mmHg/k-RPM²). Excessive rotor speeds generate elevated fluid shear stresses that induce mechanical hemolysis (erythrocyte rupture releasing free hemoglobin) and shear-mediated destruction of von Willebrand factor (vWF), leading to bleeding risks. In this laboratory investigation, an instrumented MagLev continuous-flow blood pump circuit evaluates shut-off pressure head across operational speeds from 2.0 to 4.5 k-RPM to quantify pump scaling.",
            "modelExtra": "Evaluated on a magnetically levitated continuous-flow centrifugal blood pump (impeller diameter 36 mm) circulating a blood-analog fluid (38% glycerol-water, density ρ = 1055 kg/m³, viscosity 3.6 cP at 37 °C). Speeds N = 2.0, 2.5, 3.0, 3.5, 4.0, 4.5 k-RPM correspond to N² = 4.00, 6.25, 9.00, 12.25, 16.00, 20.25 k-RPM². Shut-off head scaling constant k_N = 7.5000 mmHg/k-RPM².",
            "apparatus": [
                {"name": "Magnetically Levitated Centrifugal Blood Pump Cartridge", "purpose": "Features bearingless MagLev impeller (diameter 36 mm) driven by brushless DC stator coils."},
                {"name": "Mock Circulatory Cardiovascular Test Loop", "purpose": "Provides compliant hydraulic flow circuit with precision pinch valve for zero-flow shut-off testing."},
                {"name": "Dual High-Precision Differential Pressure Transducers", "purpose": "Measures pump inlet pressure P_in and outlet pressure P_out to determine pressure head H = P_out - P_in."},
                {"name": "Ultrasonic Transit-Time Clamp-On Flowmeter (Transonic Systems)", "purpose": "Verifies true zero flow (Q = 0.00 L/min) during shut-off head measurements."},
                {"name": "Optical Tachometer & Hall Sensor Speed Controller", "purpose": "Maintains closed-loop impeller rotational speed N within ±1 RPM of setpoint."},
                {"name": "Thermostatically Controlled Glycerol-Water Reservoir (37.0 °C)", "purpose": "Maintains blood-analog fluid viscosity (3.6 cP) and density (1055 kg/m³)."}
            ],
            "procedure": [
                {"title": "Pump Cartridge Installation and Priming", "text": "Mount the centrifugal blood pump in the mock loop, prime with 38% glycerol blood-analog at 37.0 °C, and purge all microscopic air bubbles."},
                {"title": "Magnetic Levitation and Rotor Calibration", "text": "Energize active magnetic levitation coils and verify central impeller suspension without mechanical housing contact."},
                {"title": "Pressure Transducer Zeroing at Rest", "text": "With the pump stopped (N = 0 RPM), open cross-bypass to confirm equal inlet and outlet pressure, zeroing differential transducer to 0.00 mmHg."},
                {"title": "Zero-Flow Shut-Off Head Initialization", "text": "Close the downstream outflow valve to establish zero volumetric flow (Q = 0.00 L/min), set impeller speed to N = 2.0 k-RPM (2000 RPM), and log shut-off head H_0."},
                {"title": "Impeller Speed Progression Sequence", "text": "Increment rotor speed through 2.5, 3.0, 3.5, 4.0, and 4.5 k-RPM, recording stabilized shut-off pressure head H_0 at each speed step."},
                {"title": "Euler Affinity Quadratic Regression Analysis", "text": "Plot shut-off head H_0 against N², determine pump scaling constant k_N via linear regression through the origin, and calculate maximum blade tip velocity."}
            ],
            "topics": [
                {"question": "How do pump affinity laws dictate pressure head scaling in rotary blood pumps?", "answer": "Centrifugal pump affinity laws state that volumetric flow rate Q scales linearly with impeller speed N (Q ∝ N), while pressure head H scales with the square of speed (H ∝ N²), and power consumption scales with the cube of speed (P ∝ N³)."},
                {"question": "What is the primary advantage of a magnetically levitated (MagLev) impeller over mechanical bearings?", "answer": "Mechanical pivot bearings or shaft seals create high frictional heating, localized shear stress concentrations, and blood stagnation crevices that cause severe thrombosis; MagLev impellers float freely in an active magnetic field, eliminating mechanical contact, wear, and thrombosis sites."},
                {"question": "What causes mechanical hemolysis in continuous-flow blood pumps?", "answer": "When red blood cells experience fluid shear stresses exceeding ~150 to 250 Pa (especially in narrow blade-tip clearances), cell membranes stretch, form transient pores, or rupture, releasing free hemoglobin into the plasma (plasma free hemoglobin, PfH)."},
                {"question": "What is the acquired von Willebrand syndrome in LVAD patients?", "answer": "High shear forces within rotary pumps unravel large multimers of von Willebrand factor (vWF), exposing them to cleavage by the plasma enzyme ADAMTS13; loss of high-molecular-weight vWF multimers impairs platelet adhesion and causes gastrointestinal bleeding."},
                {"question": "How does pump flow respond to changes in physiological vascular resistance (afterload)?", "answer": "Rotary blood pumps are continuous-flow devices with a steep H-Q slope: if patient blood pressure (afterload) rises, pump flow drops significantly; conversely, if vascular resistance drops, pump flow increases, making LVAD output highly load-dependent."},
                {"question": "What is an LVAD suction event and how is it detected?", "answer": "If the left ventricle underfills (hypovolemia or right heart failure), the rotary pump sucks the ventricular septum against the inflow cannula, causing a sudden spike in negative inlet pressure, drop in flow, and motor current oscillations that trigger automated speed-reduction algorithms."}
            ],
            "precautions": [
                "Do not maintain zero-flow shut-off conditions for extended periods (> 60 s); without through-flow, fluid within the pump housing experiences rapid frictional heating.",
                "Ensure active magnetic levitation is fully stable before spinning the impeller to avoid rotor-stator contact scoring.",
                "Verify zero air bubbles in pressure lines; bubble compliance introduces sluggish pressure response.",
                "Keep fluid temperature strictly at 37.0 °C to stabilize blood-analog viscosity and density."
            ],
            "limitations": [
                "Zero-flow shut-off testing evaluates the maximum static head; operational LVADs deliver 4 to 6 L/min where dynamic frictional losses reduce delivered head.",
                "Tested using non-cellular glycerol-water; cellular blood exhibits non-Newtonian shear-thinning and biological platelet/erythrocyte damage kinetics.",
                "Mock loop provides steady downstream resistance, whereas clinical LVADs pump into a pulsatile aorta with residual native ventricular contractions.",
                "Does not simulate biological protein deposition and cellular thrombus formation over months of continuous clinical pumping."
            ],
            "quiz": [
                {
                    "question": "According to turbomachinery affinity laws, how does centrifugal pump shut-off head H_0 scale with impeller speed N?",
                    "options": ["Proportional to the square of speed: H_0 ∝ N²", "Linearly: H_0 ∝ N", "Inversely: H_0 ∝ 1/N", "Logarithmically: H_0 ∝ ln(N)"],
                    "correct": 0,
                    "explanation": "Pump affinity laws dictate that shut-off pressure head generated by centrifugal kinetic energy scales with the square of rotational speed (N²)."
                },
                {
                    "question": "What is the primary clinical benefit of magnetic levitation (MagLev) in modern continuous-flow LVADs?",
                    "options": ["Eliminates mechanical contact bearings, reducing thrombosis, blood trauma, and mechanical wear", "Makes the pump completely silent", "Allows the pump to operate without electricity", "Cures diabetes"],
                    "correct": 0,
                    "explanation": "MagLev impellers float freely in an electromagnetic field, eliminating mechanical friction, wear, and stagnation crevices that promote blood clotting."
                },
                {
                    "question": "If impeller speed is N = 3.0 k-RPM (N² = 9.0 k-RPM²) and measured shut-off head is 67.50 mmHg, what is k_N?",
                    "options": ["3.750 mmHg/k-RPM²", "7.500 mmHg/k-RPM²", "15.00 mmHg/k-RPM²", "22.50 mmHg/k-RPM²"],
                    "correct": 1,
                    "explanation": "k_N = H_0 / N² = 67.50 mmHg / 9.0 k-RPM² = 7.5000 mmHg/k-RPM²."
                },
                {
                    "question": "What pathological hematological consequence occurs when high pump shear stresses degrade von Willebrand factor?",
                    "options": ["Acquired von Willebrand syndrome causing gastrointestinal bleeding", "Sickle cell anemia", "Leukemia", "Iron deficiency"],
                    "correct": 0,
                    "explanation": "Rotary pump shear stress uncoils vWF, allowing ADAMTS13 to cleave high-molecular-weight multimers and causing bleeding complications."
                }
            ],
            "settings": ["Pump: Centrifugal rotary blood pump with MagLev impeller (Ø 36 mm)", "Fluid: 38% glycerol blood analog (ρ = 1055 kg/m³, μ = 3.6 cP at 37 °C)", "Condition: Zero volumetric flow shut-off (Q = 0.00 L/min)"],
            "samples": [2.0, 2.5, 3.0, 3.5, 4.0, 4.5],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "⚙️", "label": "1. Rotary LVAD Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Head vs Speed² (N²)"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Turbomachinery Sandbox"}
            ]
        },
        {
            "number": 34,
            "slug": "fahraeus-lindqvist-tube-hematocrit-reduction",
            "title": "Fåhræus-Lindqvist Effect & Apparent Relative Blood Viscosity in Micro-Capillaries",
            "shortTitle": "Fåhræus-Lindqvist Effect",
            "aim": "Quantify the Fåhræus-Lindqvist reduction in apparent relative blood viscosity η_rel in micro-capillary glass tubes as lumen diameter D narrows from 95 μm to 20 μm.",
            "inputLabel": "Micro-Capillary Lumen Diameter D",
            "shortInput": "Diameter D",
            "inputUnit": "μm",
            "min": 20.0,
            "max": 95.0,
            "step": 15.0,
            "initial": 50.0,
            "inputDecimals": 1,
            "rawLabel": "Apparent Relative Blood Viscosity η_rel",
            "rawUnit": "ratio",
            "rawDecimals": 4,
            "xAxis": "Capillary lumen diameter D (μm)",
            "yAxis": "Apparent relative blood viscosity η_rel (ratio)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 55.0,
            "emptyY": 1.9,
            "targetName": "Fåhræus-Lindqvist Slope k_d",
            "target": "0.0125",
            "refValue": 0.0125,
            "resultUnit": "μm⁻¹",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "η_rel = k_d · D + η_0 = 0.0125 · D + 1.2500",
            "measureLabel": "Record Capillary Viscosity",
            "intro": "In 1931, Swedish physiologists Robin Fåhræus and Torsten Lindqvist discovered one of the most remarkable phenomena in microvascular hemodynamics: when whole blood flows through narrow cylindrical tubes with internal lumen diameters smaller than ~300 μm down to ~10 μm, the apparent relative viscosity of blood η_rel (normalized to plasma viscosity) decreases progressively as tube diameter narrows. This counter-intuitive reduction in flow resistance—the Fåhræus-Lindqvist effect—plays a profound physiological role, drastically reducing the cardiac pumping work required to perfuse the extensive microvascular networks of human organs. The physical mechanism underlying this phenomenon stems from red blood cell lateral migration toward the central high-velocity axis of the tube. This axial migration leaves an erythrocyte-depleted, cell-free marginal plasma layer along the vessel wall (thickness δ ≈ 2 to 4 μm). Because the low-viscosity plasma layer lubricates the high-shear region adjacent to the endothelium while the dense cellular core travels at higher average velocity, the overall tube hematocrit H_T becomes significantly lower than the feed reservoir hematocrit H_F (the Fåhræus effect). Over the microvascular diameter range from 20 μm to 95 μm, apparent relative viscosity η_rel scales linearly with capillary lumen diameter: η_rel = k_d · D + η_0, where k_d is the Fåhræus-Lindqvist dimensional slope (μm⁻¹). In this laboratory investigation, precision micro-capillary silica tubes perfused with anti-coagulated human blood evaluate pressure-flow scaling to quantify the Fåhræus-Lindqvist effect.",
            "modelExtra": "Evaluated on calibrated silica micro-capillary tubes (diameters D = 20, 35, 50, 65, 80, 95 μm; length L = 30 mm) perfused with human blood (feed hematocrit H_F = 45%, plasma viscosity η_p = 1.20 mPa·s) at high shear rates (γ̇_w > 500 s⁻¹) at 37.0 °C. Apparent relative viscosity slope k_d = 0.0125 μm⁻¹ with baseline η_0 = 1.2500 (η_rel = 1.500 at 20 μm, rising to 2.438 at 95 μm).",
            "apparatus": [
                {"name": "Calibrated Precision Silica Micro-Capillary Tubes", "purpose": "Provides internal lumen diameters D = 20, 35, 50, 65, 80, and 95 μm with circular cross-sections (±0.5 μm)."},
                {"name": "Pneumatic Micro-Perfusion Driving Pressure Controller", "purpose": "Applies regulated driving pressure drops ΔP from 1 to 50 kPa with 0.01 kPa stability."},
                {"name": "High-Speed Fluorescent Micro-PIV Microscope", "purpose": "Visualizes red cell axial migration and measures cell-free marginal plasma layer thickness δ."},
                {"name": "Sub-Micron Electronic Catch Microbalance", "purpose": "Determines volumetric flow rate Q by timed gravimetric catch with anti-evaporation cover."},
                {"name": "Thermostatically Controlled Perfusion Chamber (37.0 °C)", "purpose": "Maintains blood and capillary tubes at constant physiological temperature."},
                {"name": "Cone-and-Plate Plasma Viscometer", "purpose": "Measures baseline dynamic viscosity of cell-free blood plasma (η_p = 1.20 mPa·s)."}
            ],
            "procedure": [
                {"title": "Blood Specimen Standardization and Plasma Viscometry", "text": "Prepare fresh anti-coagulated human blood (Hct = 45.0%); centrifuge an aliquot to isolate plasma and measure plasma viscosity η_p on cone-plate viscometer (1.20 mPa·s)."},
                {"title": "Micro-Capillary Alignment and Pre-Wetting", "text": "Mount 20 μm silica micro-capillary into the perfusion manifold, pre-wet with plasma to prevent bubble entrapment, and seal pressure ports."},
                {"title": "Driving Pressure Application", "text": "Apply pneumatic pressure drop ΔP to achieve high wall shear rate (γ̇_w > 500 s⁻¹), ensuring fully dispersed non-rouleaux flow."},
                {"title": "Volumetric Flow Rate Measurement", "text": "Determine steady volumetric flow rate Q via timed micro-gravimetric collection on ultra-microbalance over 180 seconds."},
                {"title": "Apparent Viscosity Computation", "text": "Calculate apparent blood viscosity from Poiseuille's formula: η_app = [π · D⁴ · ΔP] / [128 · L · Q], and compute relative viscosity η_rel = η_app / η_p."},
                {"title": "Capillary Diameter Progression Sequence", "text": "Repeat standardized perfusion across tube diameters D = 35, 50, 65, 80, and 95 μm, recording apparent relative viscosity η_rel at each diameter."},
                {"title": "Fåhræus-Lindqvist Linear Regression", "text": "Plot apparent relative viscosity η_rel against capillary diameter D and extract slope k_d and baseline intercept η_0 via linear regression."}
            ],
            "topics": [
                {"question": "What is the physical cause of the Fåhræus-Lindqvist effect in microvessels?", "answer": "In narrow vessels, red blood cells migrate toward the central axis due to wall-induced hydrodynamic lift forces, creating an erythrocyte-rich fast core surrounded by an erythrocyte-depleted, low-viscosity plasma layer along the wall that lubricates flow."},
                {"question": "What is the difference between the Fåhræus effect and the Fåhræus-Lindqvist effect?", "answer": "The Fåhræus effect refers to the reduction in tube hematocrit H_T relative to discharge hematocrit H_F (H_T < H_F) because red cells travel faster in the center than slower plasma near the walls; the Fåhræus-Lindqvist effect refers to the resulting reduction in apparent blood viscosity."},
                {"question": "What happens to apparent blood viscosity when vessel diameter narrows below 5 to 7 μm?", "answer": "Below ~5 to 7 μm (the capillary diameter smaller than the resting red cell diameter of 8 μm), the Fåhræus-Lindqvist effect reverses (inversion phenomenon); red cells must undergo extreme single-file folding and deformation, causing apparent viscosity to rise sharply."},
                {"question": "What is the physiological benefit of the Fåhræus-Lindqvist effect for the human heart?", "answer": "By lowering apparent blood viscosity by more than 50% in the vast capillary beds compared to large vessels, it drastically reduces total peripheral resistance, lowering the hydraulic workload and oxygen consumption of the left ventricle."},
                {"question": "Why must shear rate be maintained high (γ̇_w > 500 s⁻¹) during Fåhræus-Lindqvist testing?", "answer": "High shear rates fully break up rouleaux aggregates, isolating the pure geometric and hydrodynamic cell-free layer effects without confounding shear-thinning aggregation artifacts."},
                {"question": "How does red blood cell deformability affect the Fåhræus-Lindqvist effect?", "answer": "Flexible normal erythrocytes readily deform into parachutes and migrate axially to form a thick lubricating layer; in sickle cell disease or diabetes where cells become rigid, axial migration is impaired, the cell-free layer thins, and apparent capillary viscosity remains pathologically high."}
            ],
            "precautions": [
                "Ensure micro-capillary lumen is pristine; particulate debris in a 20 μm capillary causes catastrophic clogging.",
                "Maintain wall shear rate above 500 s⁻¹ to avoid non-Newtonian rouleaux aggregation from corrupting the geometric diameter scaling.",
                "Verify zero fluid evaporation during micro-gravimetric catch weighing using an oil-sealed evaporation trap.",
                "Maintain constant temperature at 37.0 °C to stabilize baseline plasma viscosity."
            ],
            "limitations": [
                "The linear relation applies across the classic microvascular range (20 to 100 μm); below 7 μm, the curve inverts sharply upward.",
                "Silica glass micro-capillaries have rigid, smooth, circular walls, whereas living capillaries are lined with compliant endothelial glycocalyx.",
                "Tested at constant steady pressure, neglecting in-vivo capillary pressure pulsatility and leukocyte capillary plugging.",
                "Assumes isolated straight tubes, neglecting microvascular bifurcations and plasma skimming (Zweifach-Fung effect) at branches."
            ],
            "quiz": [
                {
                    "question": "What is the Fåhræus-Lindqvist effect in cardiovascular hemodynamics?",
                    "options": ["The reduction in apparent blood viscosity as tube diameter narrows from 300 μm down to ~10 μm", "The clotting of blood at high temperatures", "The acceleration of sound in the aorta", "The expansion of veins during exercise"],
                    "correct": 0,
                    "explanation": "The Fåhræus-Lindqvist effect describes how blood viscosity drops as vessel lumen diameter decreases from 300 to ~10 μm."
                },
                {
                    "question": "What microscopic fluid mechanism causes the Fåhræus-Lindqvist reduction in viscosity?",
                    "options": ["Red cells migrate to the central axis, leaving a low-viscosity cell-free plasma lubrication layer along the wall", "Red cells dissolve in narrow tubes", "Blood plasma turns into gas", "Capillary walls secrete engine oil"],
                    "correct": 0,
                    "explanation": "Axial red cell migration creates an erythrocyte-depleted marginal plasma layer that lubricates the wall and reduces flow resistance."
                },
                {
                    "question": "If tube diameter is D = 80.0 μm and apparent relative viscosity is η_rel = 2.250 with baseline η_0 = 1.250, what is k_d?",
                    "options": ["0.00625 μm⁻¹", "0.0125 μm⁻¹", "0.0250 μm⁻¹", "0.1250 μm⁻¹"],
                    "correct": 1,
                    "explanation": "k_d = (η_rel - η_0) / D = (2.250 - 1.250) / 80.0 = 1.000 / 80.0 = 0.0125 μm⁻¹."
                },
                {
                    "question": "What happens to apparent blood viscosity when vessel diameter becomes smaller than ~5 μm (inversion phenomenon)?",
                    "options": ["Viscosity rises sharply because red blood cells must deform into single-file folded shapes", "Viscosity drops to zero", "Flow becomes supersonic", "Viscosity turns negative"],
                    "correct": 0,
                    "explanation": "Below ~5 μm, red cells must undergo extreme single-file deformation, causing apparent viscosity to reverse and rise steeply."
                }
            ],
            "settings": ["Capillaries: Precision fused-silica micro-tubes (L = 30 mm, D = 20 to 95 μm)", "Blood: Normal human whole blood (H_F = 45%, η_p = 1.20 mPa·s)", "Condition: High wall shear rate (γ̇_w > 500 s⁻¹) at 37.0 °C"],
            "samples": [20.0, 35.0, 50.0, 65.0, 80.0, 95.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🩸", "label": "1. Micro-Capillary Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Viscosity vs Diameter"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Cell-Free Layer Sandbox"}
            ]
        }
    ]
