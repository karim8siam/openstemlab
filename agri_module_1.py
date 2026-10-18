# -*- coding: utf-8 -*-
"""Agricultural Engineering Module 1: Farm Machinery & Tractor Power Mechanics (Labs 1–10)."""

def get_module_1():
    return [
        {
            "number": 1,
            "slug": "tractor-drawbar-pull-tractive-efficiency",
            "title": "Tractor Drawbar Pull, Wheel Slip & Tractive Efficiency Determination",
            "shortTitle": "Tractor Drawbar Performance",
            "aim": "Determine tractor wheel slip, net traction coefficient, and tractive efficiency on agricultural soils across varying drawbar pull loads using an instrumented loading car and fifth-wheel tachometer.",
            "inputLabel": "Wheel Slip Ratio s",
            "shortInput": "Slip s",
            "inputUnit": "fraction",
            "min": 0.05,
            "max": 0.25,
            "step": 0.04,
            "initial": 0.13,
            "inputDecimals": 2,
            "rawLabel": "Net Traction Coefficient κ",
            "rawUnit": "ratio",
            "rawDecimals": 4,
            "xAxis": "Slip ratio s",
            "yAxis": "Net traction coefficient κ = P / W",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 0.15,
            "emptyY": 0.40,
            "targetName": "Traction Development Slope μ_t",
            "target": "2.4000",
            "refValue": 2.4000,
            "resultUnit": "fraction⁻¹",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "κ = μ_t · s + κ_0 = 2.4000 · s + 0.0800",
            "intro": "In agricultural mechanization and tractor mechanics, tractive efficiency defines the proportion of power delivered by the drive axles that is successfully converted into useful linear drawbar work. When a pneumatic drive tire develops forward thrust on deformable agricultural soil, micro-shearing and soil strain invariably induce wheel slip. In accordance with the classical ASABE D497 and Wismer-Luth traction models, the net traction ratio κ (defined as the drawbar pull force P divided by the dynamic vertical wheel load W) increases rapidly with slip in the initial deformation zone before asymptoting toward the ultimate soil shear strength envelope. Simultaneously, rolling resistance absorbs axle torque through soil rut compaction and tire carcass deflection. Identifying the optimum slip operating point (typically 8% to 15% on firm loam and 12% to 18% on tilled soil) ensures peak fuel economy, minimum tire wear, and maximum field tractive efficiency. In this investigation, an instrumented research tractor coupled with an eddy-current dynamometer loading car is evaluated across controlled drawbar pull increments while logging drive wheel revolutions and true ground speed via an optical fifth-wheel radar sensor.",
            "modelExtra": "Linearized traction development model valid in the operational working range of 5% to 25% slip on settled silt loam soil. Dynamic weight transfer from the front axle to the rear drive axle is accounted for using moment equilibrium about the tire-soil contact patches.",
            "apparatus": [
                {"name": "Agricultural Research Tractor", "purpose": "Provides controlled PTO and axle torque with ballast weights establishing a static rear axle load of 35.0 kN."},
                {"name": "Eddy-Current Dynamometer Car", "purpose": "Applies variable braking resistance to generate continuous, regulated drawbar pull loads."},
                {"name": "Drawbar Strain-Gauge Load Cell", "purpose": "Measures horizontal draft force with 0.1 kN resolution and continuous telemetry logging."},
                {"name": "Non-Contact Doppler Radar Sensor", "purpose": "Measures true tractor ground speed eliminating rolling tire slip errors."},
                {"name": "Drive Wheel Optical Encoders", "purpose": "Monitors exact axle angular velocity and theoretical zero-slip forward travel velocity."},
                {"name": "Soil Cone Penetrometer", "purpose": "Assesses pre-test topsoil cone index and moisture profile to ensure consistent field shear strength."}
            ],
            "procedure": [
                {"title": "Zero-Load Distance Calibration", "text": "Operate the tractor over a surveyed 100-meter test course in neutral drawbar condition to record baseline drive wheel revolutions and establish theoretical rolling radius under zero net pull."},
                {"title": "Dynamometer Car Hitching", "text": "Hitch the mobile loading car horizontally through the calibrated strain-gauge load cell, verifying that the hitch line is parallel to the ground surface to prevent spurious vertical forces."},
                {"title": "Engine Speed Standardization", "text": "Set tractor engine throttle to rated speed (2200 RPM) in standard field gear (Gear B-2) to ensure constant input mechanical power to the transmission."},
                {"title": "Incremental Drawbar Loading", "text": "Increment the eddy-current braking load on the dynamometer car in six distinct steps, allowing the tractor to reach steady-state velocity for at least 30 seconds per trial."},
                {"title": "Synchronous Telemetry Acquisition", "text": "Simultaneously log true ground velocity from the Doppler radar, wheel rotation counts from axle encoders, and drawbar draft force from the load cell over standard 50-meter runs."},
                {"title": "Tractive Metrics Reduction", "text": "Calculate slip ratio s = (V_t - V_a)/V_t and net traction coefficient κ = P/W_d, plotting the traction curve and identifying peak tractive efficiency."}
            ],
            "topics": [
                {"question": "How is tractor drive wheel slip defined and measured experimentally?", "answer": "Wheel slip is defined as s = (V_theoretical - V_actual) / V_theoretical, where V_theoretical is the forward velocity the tractor would travel if the drive wheels rolled without soil deformation (determined from axle RPM and rolling radius on concrete), and V_actual is the true ground velocity measured via radar or fifth-wheel."},
                {"question": "Why does tractive efficiency decline at both very low and very high wheel slip values?", "answer": "At very low slip (under 5%), rolling resistance forms a disproportionately large fraction of gross traction, lowering net efficiency. At high slip (over 20%), excessive rotational energy is dissipated into churning, grinding, and shearing the soil rather than producing forward motion."},
                {"question": "Explain dynamic weight transfer in two-wheel-drive tractors during draft operations.", "answer": "When a horizontal drawbar pull P is exerted at hitch height h, static equilibrium dictates that a moment P·h pitches the tractor upward about the rear axle, reducing front axle load by (P·h)/wheelbase and transferring that load directly onto the rear drive wheels, which beneficially increases rear normal force and tractive capacity."},
                {"question": "What is the difference between gross traction and net traction?", "answer": "Gross traction is the total shear force generated at the tire-soil interface developed by axle torque, whereas net traction is the useful pull remaining at the drawbar after subtracting tire rolling resistance and soil compaction energy."},
                {"question": "How does soil moisture content influence the optimal slip range of agricultural tires?", "answer": "High soil moisture weakens inter-particle cohesion and soil internal friction angle, lowering the shear strength envelope and shifting the peak tractive efficiency point toward higher slip values while dramatically increasing rolling sinkage."},
                {"question": "What role does tire inflation pressure play in tractor field performance?", "answer": "Lowering tire inflation pressure increases contact patch footprint area, decreases average contact pressure, reduces soil rut sinkage, and increases gross traction on soft agricultural soils, while excessive pressure promotes rutting and slip."}
            ],
            "precautions": [
                "Maintain uniform hitch height across all trials to prevent erratic pitch moments on the rear axle.",
                "Ensure constant engine governor throttle setting to avoid confounding engine torque droop with traction limits.",
                "Perform all comparative slip trials along identical soil tracks with uniform bulk density and moisture content.",
                "Verify zero-tare offset of the drawbar strain-gauge load cell before each loading increment."
            ],
            "limitations": [
                "The linear model applies strictly to the steady pre-saturation slip range (s ≤ 0.25) before catastrophic soil shear failure occurs.",
                "Does not account for non-linear tire lug flexing and rubber tread carcass hysteresis at extreme tractive loads.",
                "Assumes homogeneous topsoil shear strength without localized hardpan encounters.",
                "Transient slip fluctuations caused by governor micro-hunting are averaged over the 50-meter measurement run."
            ],
            "quiz": [
                {
                    "question": "What is the primary physical cause of wheel slip in agricultural tractors on soil?",
                    "options": ["Transmission gear backlash", "Continuous tangential soil shearing and plastic deformation under tire lugs", "Differential lock disengagement", "Engine governor throttling"],
                    "correct": 1,
                    "explanation": "Wheel slip occurs because the soil beneath the tire lugs must undergo shear strain and plastic displacement to generate reactive horizontal thrust."
                },
                {
                    "question": "On firm tilled soil, what is the typical slip range for optimum tractive efficiency?",
                    "options": ["0% to 2%", "10% to 15%", "35% to 50%", "70% to 85%"],
                    "correct": 1,
                    "explanation": "Standard ASABE recommendations specify that peak tractive efficiency on tilled agricultural loam occurs between 10% and 15% slip."
                },
                {
                    "question": "If dynamic rear axle weight is 40 kN and measured drawbar pull is 16 kN, what is the net traction coefficient?",
                    "options": ["0.10", "0.25", "0.40", "0.65"],
                    "correct": 2,
                    "explanation": "The net traction coefficient κ is calculated as Drawbar Pull / Dynamic Normal Load = 16 kN / 40 kN = 0.40."
                },
                {
                    "question": "How does dynamic weight transfer affect the front wheels of a pulling tractor?",
                    "options": ["Front wheel load increases", "Front wheel load decreases proportionally to pull and hitch height", "Front wheel load is completely unaffected", "Front wheel load oscillates randomly"],
                    "correct": 1,
                    "explanation": "The moment generated by drawbar pull about the rear contact patch unloads the front axle by P·h / wheelbase."
                }
            ],
            "settings": ["Test soil: Silt loam (moisture 18.2% d.b.)", "Tractor static rear axle weight: 35.0 kN", "Rear tire inflation: 110 kPa"],
            "samples": [0.05, 0.09, 0.13, 0.17, 0.21, 0.25],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🚜", "label": "1. Tractor Field Test"},
                {"id": "compare", "icon": "📊", "label": "2. Traction vs Slip Polar"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Soil Slip Sandbox"}
            ]
        },
        {
            "number": 2,
            "slug": "moldboard-plow-draft-specific-resistance",
            "title": "Moldboard Plow Draft Force & Specific Soil Resistance Calibration",
            "shortTitle": "Moldboard Plow Specific Draft",
            "aim": "Measure the horizontal draft force of a multi-bottom moldboard plow as a function of furrow cross-sectional area and evaluate specific soil resistance.",
            "inputLabel": "Furrow Cross-Sectional Area A",
            "shortInput": "Area A",
            "inputUnit": "m²",
            "min": 0.04,
            "max": 0.14,
            "step": 0.02,
            "initial": 0.08,
            "inputDecimals": 2,
            "rawLabel": "Total Plow Draft Force D",
            "rawUnit": "kN",
            "rawDecimals": 3,
            "xAxis": "Furrow area A (m²)",
            "yAxis": "Draft force D (kN)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 0.09,
            "emptyY": 4.5,
            "targetName": "Specific Soil Resistance k_s",
            "target": "48.5000",
            "refValue": 48.5000,
            "resultUnit": "kPa",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "D = k_s · A = 48.5000 · A",
            "intro": "Primary tillage via moldboard plowing represents one of the most energy-intensive operations in agricultural crop production. The moldboard plow functions by cutting a rectangular prism of soil (furrow slice) with the horizontal share and vertical coulter, lifting it along the curved shin and breast, and inverting it across the moldboard wing to bury crop residues and aerate the root zone. The total horizontal draft resistance D is governed by soil mechanical properties (cohesion, internal friction, soil-metal adhesion), cutting geometry, and operating speed. In classical tillage mechanics (ASABE D497 and Gorjatschkin's rational equation), draft is partitioned into three terms: static cutting and friction resistance proportional to furrow cross-sectional area (A = w·d), soil acceleration and throwing resistance proportional to velocity squared, and parasitic landside friction. At steady field speed, specific soil resistance k_s = D / A (expressed in kPa or N/cm²) provides an objective benchmark of soil workability and structural state.",
            "modelExtra": "Evaluated at constant forward plowing speed of 5.5 km/h on settled clay loam. Specific soil draft k_s integrates soil cutting, lifting, inversion friction, and landside reaction.",
            "apparatus": [
                {"name": "Three-Bottom Mounted Moldboard Plow", "purpose": "Standard agricultural implement with 35 cm share width per bottom and adjustable depth wheel."},
                {"name": "Three-Point Hitch Dynamometer Frame", "purpose": "Measures tri-axial hitch forces and moments between tractor lift arms and plow mast."},
                {"name": "Digital Depth Gauge Profiler", "purpose": "Records continuous depth of plowing along the furrow wall."},
                {"name": "Soil Core Sampling Cylinder", "purpose": "Extracts undisturbed volumetric core samples to determine field dry bulk density and moisture content."},
                {"name": "Tractor Ground Speed Radar", "purpose": "Monitors forward travel velocity to ensure steady Gorjatschkin kinetic regime."},
                {"name": "Electronic Data Logger", "purpose": "Synchronizes and records load cell signals at 50 Hz with anti-aliasing filtration."}
            ],
            "procedure": [
                {"title": "Plow Leveling & Alignment", "text": "Set tractor wheel tread to match furrow bottom width and adjust tractor three-point top link and leveling rod so the plow frame sits parallel to the ground in both lateral and longitudinal directions."},
                {"title": "Baseline Soil Profiling", "text": "Sample soil moisture and bulk density at 5 cm depth increments across the test plot to verify uniform pre-tillage soil mechanical conditions."},
                {"title": "Initial Depth Calibration", "text": "Set the gage wheel to initial shallow depth (d = 12 cm, A = 0.042 m²) and verify full furrow slice inversion without scouring failure."},
                {"title": "Steady-State Draft Logging", "text": "Operate the tractor at constant 5.5 km/h over a 60-meter measuring strip, recording three-point hitch draft load cell channels continuously."},
                {"title": "Depth Incrementation", "text": "Systematically lower the plow depth in five discrete steps from 12 cm to 28 cm, measuring furrow width and depth with the profiler for each run."},
                {"title": "Specific Resistance Computation", "text": "Calculate furrow cross-sectional area A = width × depth, plot draft force versus area, and compute the slope representing specific soil resistance k_s."}
            ],
            "topics": [
                {"question": "State Gorjatschkin's rational formula for tillage tool draft.", "answer": "Gorjatschkin's equation is D = f·G + k_s·a·b + ε·a·b·v², where f·G is parasitic sliding resistance of the plow body weight, k_s·a·b is static soil cutting and deforming resistance, and ε·a·b·v² represents the dynamic inertial force required to accelerate the furrow slice sideways and upward."},
                {"question": "What is specific soil resistance and what factors determine its magnitude?", "answer": "Specific soil resistance k_s = D / (w·d) is the draft force required per unit cross-sectional area of tilled soil. It depends on soil texture (clay vs sand), moisture content, bulk density, root proliferation, and moldboard surface scouring quality."},
                {"question": "How does soil moisture content affect moldboard plow draft?", "answer": "At very low moisture (dry soil), high cohesion and shear strength produce hard clods and extreme draft. As moisture increases to the friable range, draft drops to a minimum. Above the plastic limit, draft increases again due to sticky soil-metal adhesion and friction."},
                {"question": "Why is proper plow horizontal and vertical suction critical?", "answer": "Vertical suction (downward pitch of share point) pulls the plow into the ground to maintain working depth without ballast, while horizontal suction (inward angle) holds the landside against the furrow wall to maintain consistent cutting width."},
                {"question": "What role does the rolling coulter play in reducing overall draft?", "answer": "The circular coulter cuts clean vertical edges through surface trash and roots ahead of the shin, reducing tearing friction and preventing residue accumulation on the plow frog."},
                {"question": "How does increasing plowing speed alter specific soil draft?", "answer": "Increasing speed increases draft quadratically due to the kinetic energy imparted to throw and invert the soil slice (the ε·v² term in Gorjatschkin's equation), increasing fuel consumption per hectare."}
            ],
            "precautions": [
                "Scour all moldboard surfaces thoroughly with abrasive pads before testing to eliminate rust and establish steady soil-metal friction.",
                "Ensure tractor right wheels run inside the previous furrow wall at constant offset to prevent variation in first-bottom width.",
                "Check that draft load cells are properly temperature-compensated to prevent zero drift under field solar radiation.",
                "Disengage the differential lock only after entering the straight test run to maintain true axial alignment."
            ],
            "limitations": [
                "Linear proportionality D = k_s·A holds strictly at constant operating speed; speed variations introduce quadratic dynamic errors.",
                "Does not separate landside lateral friction from moldboard normal reaction forces.",
                "Assumes uniform furrow depth across all three bottoms; slight linkage flexure can introduce small inter-bottom depth disparities.",
                "Field stones or root obstacles produce transient draft spikes that must be filtered using median windowing."
            ],
            "quiz": [
                {
                    "question": "What unit is typically used to quantify specific soil resistance in agricultural engineering?",
                    "options": ["kW/h", "kPa (or N/cm²)", "Joules/sec", "kg/m³"],
                    "correct": 1,
                    "explanation": "Specific soil resistance is force per unit area of furrow slice, quantified in kPa (kN/m²) or N/cm²."
                },
                {
                    "question": "If a 3-bottom plow with 35 cm width per bottom operates at 20 cm depth in soil with k_s = 50 kPa, what is the total draft?",
                    "options": ["5.25 kN", "10.5 kN", "15.0 kN", "25.0 kN"],
                    "correct": 1,
                    "explanation": "Total width = 3 × 0.35 m = 1.05 m; Area A = 1.05 m × 0.20 m = 0.21 m²; Draft D = 50 kPa × 0.21 m² = 10.5 kN."
                },
                {
                    "question": "Which term in Gorjatschkin's draft formula accounts for soil acceleration at high speed?",
                    "options": ["f·G", "k_s·a·b", "ε·a·b·v²", "μ·N"],
                    "correct": 2,
                    "explanation": "The velocity-squared term ε·a·b·v² accounts for the kinetic energy required to accelerate and throw the soil slice."
                },
                {
                    "question": "What condition occurs when soil sticks to the moldboard face rather than sliding smoothly?",
                    "options": ["Cavitation", "Non-scouring", "Chatter vibration", "Liquefaction"],
                    "correct": 1,
                    "explanation": "Non-scouring occurs when soil-metal adhesion exceeds soil-soil cohesion, drastically increasing friction and plowing draft."
                }
            ],
            "settings": ["Implement: 3-bottom moldboard plow (35 cm share)", "Plowing speed: 5.5 km/h", "Soil bulk density: 1.32 g/cm³"],
            "samples": [0.04, 0.06, 0.08, 0.10, 0.12, 0.14],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🚜", "label": "1. Plowing Force Dynamometer"},
                {"id": "compare", "icon": "📊", "label": "2. Draft vs Depth Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Furrow Area Sandbox"}
            ]
        },
        {
            "number": 3,
            "slug": "disc-plow-side-draft-penetration",
            "title": "Disc Plow Side Draft, Tilt Angle & Furrow Penetration Mechanics",
            "shortTitle": "Disc Plow Penetration Draft",
            "aim": "Investigate the relationship between plowing depth and total draft force for an agricultural disc plow and evaluate penetration resistance under varying disc angles.",
            "inputLabel": "Operating Depth of Cut d",
            "shortInput": "Depth d",
            "inputUnit": "cm",
            "min": 10.0,
            "max": 25.0,
            "step": 3.0,
            "initial": 16.0,
            "inputDecimals": 1,
            "rawLabel": "Total Draft Force F",
            "rawUnit": "kN",
            "rawDecimals": 3,
            "xAxis": "Plowing depth d (cm)",
            "yAxis": "Draft force F (kN)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 17.5,
            "emptyY": 5.6,
            "targetName": "Depth Draft Gradient c_d",
            "target": "0.3200",
            "refValue": 0.3200,
            "resultUnit": "kN/cm",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "F = c_d · d = 0.3200 · d",
            "intro": "Disc plows are widely employed in hard, dry, stony, or root-infested soils where moldboard plows suffer severe share wear or fail to penetrate. Unlike moldboard plows which slide continuously through the furrow slice, the individually mounted concave steel discs roll along the furrow line, cutting, lifting, and rolling the soil through a combined action of disc angle (the horizontal angle between the disc diameter and the direction of travel, typically 40° to 45°) and tilt angle (the vertical inclination from perpendicular, typically 15° to 25°). Penetration depends almost entirely on implement deadweight rather than suction. Because the soil reaction force exerts an oblique thrust across the disc face, disc plows generate substantial lateral side draft which must be balanced by a spring-loaded furrow wheel or tractor stabilizer sway chains. In this laboratory investigation, a mounted 3-disc plow instrumented with multi-axis load cells is tested across increasing working depths to evaluate the penetration resistance gradient c_d and the resultant draft vector.",
            "modelExtra": "Evaluated at constant disc angle of 42° and tilt angle of 20° on hard clay soil. Draft F represents the forward horizontal component of total soil resistance.",
            "apparatus": [
                {"name": "Three-Disc Mounted Agricultural Plow", "purpose": "Features 66 cm diameter heat-treated boron steel concave discs with heavy-duty roller bearings."},
                {"name": "Tri-Axial Three-Point Hitch Dynamometer", "purpose": "Measures longitudinal draft, vertical penetration reaction, and lateral side forces simultaneously."},
                {"name": "Spring-Loaded Rear Furrow Wheel", "purpose": "Absorbs lateral side draft and maintains plow tracking in the furrow bottom."},
                {"name": "Mechanical Disc Inclinometer & Protractor", "purpose": "Sets and verifies disc angle (horizontal) and tilt angle (vertical) with 0.5° precision."},
                {"name": "Ultrasonic Tillage Depth Sensor", "purpose": "Continuously measures distance from plow frame to unplowed ground surface."},
                {"name": "Multi-Channel Digital Telemetry Hub", "purpose": "Logs forces, tractor forward speed, and wheel draft signals at 100 Hz."}
            ],
            "procedure": [
                {"title": "Disc Angle & Tilt Angle Calibration", "text": "Adjust the disc standard clamps to set disc angle to exactly 42° and tilt angle to 20° using the mechanical protractor and inclinometer."},
                {"title": "Hitch Geometry & Sway Setup", "text": "Attach the plow to the tractor Category II three-point linkage, adjusting check chains to allow slight floating sway for the furrow wheel to seat against the furrow corner."},
                {"title": "Zero-Load Sensor Balancing", "text": "Elevate the plow fully with the hydraulic lift and record tare offsets on all draft, vertical, and side load cell channels."},
                {"title": "Shallow Penetration Run", "text": "Set the rear furrow wheel depth stop to d = 10.0 cm, engage tractor forward speed at 5.0 km/h, and log steady draft force over a 50-meter test course."},
                {"title": "Sequential Depth Increments", "text": "Increment the working depth in five uniform stages up to 25.0 cm, checking furrow slice throw and soil pulverization consistency."},
                {"title": "Penetration Gradient Analysis", "text": "Plot draft force F against depth d, perform ordinary least-squares regression to extract the depth draft gradient c_d, and calculate side force ratio."}
            ],
            "topics": [
                {"question": "Distinguish between disc angle and tilt angle in a disc plow.", "answer": "Disc angle is the horizontal angle formed between the plane of the cutting disc rim and the direction of forward travel (controlling furrow width and cutting action), while tilt angle is the vertical angle between the disc face and the vertical plane (controlling soil lifting, turning, and penetration)."},
                {"question": "Why do disc plows rely primarily on heavy deadweight for soil penetration?", "answer": "Unlike moldboard plows which feature bottom share suction that draws the tool into the ground, rolling discs have upward vertical soil reactions that tend to push the discs out of the ground; hence, heavy frame weight is required to force the cutting edges into hard soil."},
                {"question": "How is lateral side draft counteracted in mounted disc plows?", "answer": "Side draft is counteracted by a spring-loaded, angled rear furrow wheel that presses against the vertical furrow wall, transferring lateral soil reactions into the undisturbed ground, supplemented by tractor lower link sway stabilizers."},
                {"question": "Under what agricultural conditions is a disc plow preferred over a moldboard plow?", "answer": "Disc plows are preferred in very hard dry soils, abrasive stony ground where shares would break, sticky soils that do not scour on moldboards, and land with heavy roots or shrub stumps because the rolling discs roll over obstacles."},
                {"question": "What is the function of the disc scrapers mounted on each disc standard?", "answer": "Scrapers peel sticky soil and residues from the concave disc face, assisting in inverting the furrow slice and preventing soil buildup that would destroy the cutting and rolling geometry."},
                {"question": "How does increasing the tilt angle affect penetration and draft?", "answer": "Increasing tilt angle improves penetration in soft to medium soils by providing more horizontal cutting action, but excessive tilt reduces the soil turning ability and can increase vertical bearing resistance."}
            ],
            "precautions": [
                "Ensure disc sealed bearings spin freely by hand without axial play or binding before field trials.",
                "Verify that the rear furrow wheel spring tension is sufficiently preloaded to prevent lateral crab steering.",
                "Keep clear of rotating discs during operation; never stand behind the implement when lowering under hydraulic power.",
                "Check that all three discs are set to identical disc and tilt angles to avoid inter-disc draft imbalances."
            ],
            "limitations": [
                "Assumes consistent soil penetration resistance without hidden boulder strikes or subsoil rock shelves.",
                "Linear depth relationship applies within normal plowing depth limits (10 to 25 cm) before the disc hub begins to drag on the soil surface.",
                "Side draft measurements can be influenced by tire side-wall deflection in the furrow bottom.",
                "Does not account for bearing frictional torque degradation under prolonged dusty field service."
            ],
            "quiz": [
                {
                    "question": "What is the typical disc angle range for standard agricultural disc plows?",
                    "options": ["5° to 10°", "20° to 25°", "40° to 45°", "80° to 90°"],
                    "correct": 2,
                    "explanation": "Standard disc plows operate with a horizontal disc angle between 40° and 45° to balance cutting width with forward draft resistance."
                },
                {
                    "question": "Why does a disc plow generate substantial lateral side force?",
                    "options": ["Because of rear PTO rotation", "Because the discs are set at an oblique angle pushing soil sideways", "Due to uneven tire inflation", "Due to hydraulic pump pressure pulsations"],
                    "correct": 1,
                    "explanation": "Because the concave discs cut and push soil to one side at an oblique angle, an equal and opposite lateral force is exerted on the plow frame."
                },
                {
                    "question": "If the depth draft gradient is c_d = 0.32 kN/cm, what is the expected draft at d = 20 cm?",
                    "options": ["3.2 kN", "6.4 kN", "9.6 kN", "12.8 kN"],
                    "correct": 1,
                    "explanation": "Draft F = c_d · d = 0.32 kN/cm × 20 cm = 6.4 kN."
                },
                {
                    "question": "What primary mechanism prevents disc plows from clogging in sticky, trashy soils?",
                    "options": ["High-frequency electric vibration", "The continuous rolling action of the disc assisted by scrapers", "Pressurized air jets", "Teflon spray coating"],
                    "correct": 1,
                    "explanation": "The rolling motion of the circular blade combined with curved scrapers continuously cleans the disc surface."
                }
            ],
            "settings": ["Disc diameter: 66 cm (3 discs)", "Disc angle: 42°", "Tilt angle: 20°", "Plowing speed: 5.0 km/h"],
            "samples": [10.0, 13.0, 16.0, 19.0, 22.0, 25.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🚜", "label": "1. Disc Penetration Test"},
                {"id": "compare", "icon": "📊", "label": "2. Draft vs Depth Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Disc Angle Sandbox"}
            ]
        },
        {
            "number": 4,
            "slug": "rotary-tiller-rotor-torque-specific-energy",
            "title": "Tractor PTO Rotary Tiller Dynamic Torque & Specific Energy Requirement",
            "shortTitle": "Rotary Tiller PTO Torque",
            "aim": "Determine the PTO shaft torque, rotor power consumption, and specific tilling energy of an agricultural rotavator as a function of forward velocity ratio.",
            "inputLabel": "Forward Velocity Ratio λ = u / v_f",
            "shortInput": "Velocity Ratio λ",
            "inputUnit": "ratio",
            "min": 1.5,
            "max": 4.5,
            "step": 0.6,
            "initial": 2.7,
            "inputDecimals": 1,
            "rawLabel": "Specific Tilling Energy E_s",
            "rawUnit": "kJ/m³",
            "rawDecimals": 2,
            "xAxis": "Forward velocity ratio λ = u / v_f",
            "yAxis": "Specific energy E_s (kJ/m³)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.0,
            "emptyY": 54.6,
            "targetName": "Specific Energy Slope k_e",
            "target": "18.2000",
            "refValue": 18.2000,
            "resultUnit": "kJ/m³",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "E_s = k_e · λ = 18.2000 · λ",
            "intro": "Rotary tillers (rotavators) are active PTO-driven tillage implements widely utilized in seedbed preparation, paddy puddling, and intensive horticulture. Unlike passive draft implements that rely on tractor drawbar pull to slice soil, rotary tillers transmit mechanical engine power directly through the tractor PTO shaft and bevel gearbox to a transverse rotor shaft fitted with curved L-shaped or C-shaped blades. As the tractor advances at forward speed v_f while the rotor rotates with peripheral tip speed u, each blade executes a trochoidal trajectory through the soil, cutting curved slices (trowel bites) of length L_b = 2π·v_f / (z·ω). The forward velocity ratio λ = u / v_f dictates the degree of soil pulverization, tilling bite thickness, and energy consumption. As λ increases, the bite size decreases, producing finer soil tilth at the expense of higher rotor torque and specific tilling energy E_s (energy consumed per unit volume of tilled soil, kJ/m³). In this trial, an instrumented telemetry slip-ring PTO torquemeter measures shaft torque, angular speed, and specific energy across six regulated velocity ratios.",
            "modelExtra": "Evaluated at constant rotor speed of 220 RPM and working depth of 12 cm on sandy clay loam. Forward tractor speed is varied from 1.8 to 5.4 km/h to modulate λ.",
            "apparatus": [
                {"name": "Tractor PTO Rotary Tiller (1.5 m Width)", "purpose": "Fitted with 36 L-shaped blades on 6 flange discs with rear trailing leveling shield."},
                {"name": "In-Line PTO Strain-Gauge Torquemeter", "purpose": "Measures dynamic drive shaft torque up to 1500 N·m with wireless telemetry link."},
                {"name": "Optical Shaft Tachometer", "purpose": "Continuously records tractor PTO angular velocity and rotor shaft RPM."},
                {"name": "Doppler Ground Speed Radar", "purpose": "Measures actual tractor forward travel speed v_f with 0.05 km/h accuracy."},
                {"name": "Rotary Tillage Depth Gauge", "purpose": "Verifies constant depth of cut along the tilled swath."},
                {"name": "Sieve Aggregate Shaker Set", "purpose": "Determines mean weight diameter (MWD) of tilled soil clods to quantify pulverization."}
            ],
            "procedure": [
                {"title": "Torquemeter Installation & Zeroing", "text": "Install the in-line strain-gauge torque sensor onto the tractor 540 RPM PTO spline shaft, zeroing the static tare calibration before attaching the rotavator drive shaft."},
                {"title": "Implement Depth & Shield Adjustment", "text": "Set the rotavator side skid shoes to maintain a uniform 12.0 cm tilling depth, and adjust the rear trailing hood to standard spring pressure."},
                {"title": "Rated PTO Speed Stabilization", "text": "Engage tractor PTO and adjust engine throttle to deliver exactly 540 RPM PTO speed (rotor shaft speed 220 RPM)."},
                {"title": "Tillage Run at Initial Speed Ratio", "text": "Engage tractor transmission in Gear B-1 (high λ = 4.5, slow forward travel) and log torque, RPM, and speed over a 40-meter run."},
                {"title": "Systematic Velocity Ratio Stepping", "text": "Progressively increase tractor forward travel speed across five additional transmission gears (decreasing λ toward 1.5) while keeping PTO RPM constant."},
                {"title": "Specific Energy Calculation", "text": "Calculate tilled volume rate V_dot = width × depth × v_f, average shaft power P = T·ω, specific energy E_s = P / V_dot, and evaluate the slope k_e against λ."}
            ],
            "topics": [
                {"question": "What is the trochoidal path of a rotary tiller blade?", "answer": "The path traced by a rotary tiller blade tip is a prolate trochoid resulting from the combination of linear forward translation of the tractor and circular rotation of the rotor shaft."},
                {"question": "Define the forward velocity ratio λ and explain its significance.", "answer": "The velocity ratio is λ = u / v_f = (R·ω) / v_f, representing the ratio of blade peripheral tip speed to tractor forward speed. Higher λ produces smaller bite lengths and finer clod pulverization but requires significantly higher energy."},
                {"question": "How does an active PTO-driven tiller affect tractor drawbar force?", "answer": "In conventional down-cut rotation, the blades strike the soil downward and backward, generating a forward thrust on the tractor that can push the tractor forward, effectively resulting in negative drawbar pull."},
                {"question": "Why are L-shaped blades preferred in trashy and weed-infested fields?", "answer": "L-shaped blades have a distinct cutting edge along both the shank and the wing, making them superior for cutting crop residues, chopping green manure, and clearing weeds without excessive wrapping around the rotor shaft."},
                {"question": "What is the relationship between tilling bite length and soil pulverization?", "answer": "Tilling bite length L_b = (2π·v_f) / (z·ω) is inversely proportional to pulverization. Shorter bites slice thinner soil chips, which shatter into smaller aggregates, reducing mean weight diameter."},
                {"question": "How does the position of the rear trailing hood influence soil pulverization?", "answer": "Lowering the spring-loaded rear hood forces thrown soil clods to rebound repeatedly against the steel shield and rotating blades, increasing secondary shatter and producing a much finer seedbed."}
            ],
            "precautions": [
                "Verify PTO safety slip clutch torque setting to ensure immediate disengagement upon striking underground obstructions.",
                "Never open or inspect the rear trailing shield while the PTO drive is engaged.",
                "Ensure constant tractor engine governor setting to avoid confounding torque drops with speed changes.",
                "Check blade bolt torques before and after trials; loose blades cause severe dynamic rotor imbalance."
            ],
            "limitations": [
                "Linear specific energy model applies to standard down-cut rotation within normal moisture and velocity ratio limits.",
                "Assumes homogeneous soil moisture; localized wet spots increase soil adhesion and parasitic rotor friction.",
                "Does not account for gearbox thermal losses, which typically absorb 4% to 7% of gross PTO power.",
                "High-frequency blade entry torque pulses are averaged over 10 rotor revolutions per data record."
            ],
            "quiz": [
                {
                    "question": "What does a high forward velocity ratio λ in a rotary tiller indicate?",
                    "options": ["High tractor travel speed with very coarse clods", "High rotor tip speed relative to forward travel producing fine pulverization", "Stalled tractor transmission", "Zero energy consumption"],
                    "correct": 1,
                    "explanation": "A high λ means the rotor tips travel much faster than the tractor advances, slicing very thin soil bites and producing fine pulverization."
                },
                {
                    "question": "If rotor power is 24 kW, working width is 1.5 m, depth is 0.12 m, and forward speed is 1.0 m/s, what is the specific energy?",
                    "options": ["133.3 kJ/m³", "240.0 kJ/m³", "500.0 kJ/m³", "1200.0 kJ/m³"],
                    "correct": 0,
                    "explanation": "Volume rate V_dot = 1.5 m × 0.12 m × 1.0 m/s = 0.18 m³/s. Specific energy E_s = 24 kW / 0.18 m³/s = 133.3 kJ/m³."
                },
                {
                    "question": "What unique tractive phenomenon occurs during down-cut rotary tillage?",
                    "options": ["Extreme tractor wheel slip exceeding 40%", "Rotor blades push the tractor forward, reducing drawbar draft to zero or negative", "Front tractor wheels lift off the ground", "Implement swings laterally"],
                    "correct": 1,
                    "explanation": "In standard down-cut rotation, blade impact forces impart forward momentum to the machine, generating a forward push."
                },
                {
                    "question": "Which blade type is most widely used for puddling wetland paddy soils?",
                    "options": ["Chisel sweep", "C-shaped blade", "Twisted shovel", "Spike tooth"],
                    "correct": 1,
                    "explanation": "C-shaped blades have curved profiles with minimal side surface area, preventing mud clogging and excessive power loss in wet paddy soils."
                }
            ],
            "settings": ["Rotavator width: 1.5 m (36 L-blades)", "Tilling depth: 12.0 cm", "PTO speed: 540 RPM (rotor 220 RPM)"],
            "samples": [1.5, 2.1, 2.7, 3.3, 3.9, 4.5],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🚜", "label": "1. PTO Torquemeter Test"},
                {"id": "compare", "icon": "📊", "label": "2. Energy vs Lambda Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Blade Velocity Sandbox"}
            ]
        },
        {
            "number": 5,
            "slug": "fluted-roller-seed-drill-metering-calibration",
            "title": "Fluted-Roller Seed Drill Metering Mechanism Discharge Calibration",
            "shortTitle": "Seed Drill Metering Calibration",
            "aim": "Calibrate an agricultural fluted-roller seed drill metering mechanism and establish the linear discharge characteristic across variable active roller exposures.",
            "inputLabel": "Active Fluted Roller Exposure L",
            "shortInput": "Exposure L",
            "inputUnit": "mm",
            "min": 10.0,
            "max": 35.0,
            "step": 5.0,
            "initial": 20.0,
            "inputDecimals": 1,
            "rawLabel": "Seed Discharge Rate per Row q",
            "rawUnit": "g/min",
            "rawDecimals": 2,
            "xAxis": "Fluted roller exposure L (mm)",
            "yAxis": "Seed discharge rate q (g/min)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 22.5,
            "emptyY": 191.25,
            "targetName": "Metering Discharge Gradient c_q",
            "target": "8.5000",
            "refValue": 8.5000,
            "resultUnit": "g/(min·mm)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "q = c_q · L = 8.5000 · L",
            "intro": "Accurate seed metering is fundamental to establishing optimal crop plant population, maximizing light interception, and eliminating wasteful over-seeding in mechanized agriculture. The fluted-roller feed mechanism is the standard metering device in universal grain drills for planting cereals (wheat, barley, oats) and small oilseeds. It consists of an axially sliding fluted brass or nylon cylinder positioned within a seed cup beneath the seed hopper. As the drill ground wheel rotates the fluted shaft via a chain-and-sprocket drive, seeds enter the longitudinal flute cavities and are carried over the cutoff tongue into the seed tubes. The seeding rate (kg/ha) is modulated primarily by shifting the feed shaft laterally to adjust the active exposed length of the flutes inside the seed cup, with secondary adjustment via drive sprocket gear ratios. Because gravity feeding and positive displacement combine in the seed cup, the discharge rate exhibits a highly repeatable, linear relationship with flute exposure length for clean, graded seed. In this calibration laboratory, an instrumented stationary test stand with electric variable-speed ground-wheel simulation is used to calibrate discharge per row.",
            "modelExtra": "Evaluated at constant drive shaft rotational speed of 40 RPM using certified seed wheat (thousand-grain weight 42.5 g, bulk density 0.78 g/cm³).",
            "apparatus": [
                {"name": "Stationary Seed Drill Calibration Stand", "purpose": "Mounts a full-scale 9-row grain drill hopper and fluted-roller metering drive assembly."},
                {"name": "Variable-Speed Electric Drive Motor", "purpose": "Simulates ground wheel rotation at an equivalent forward field speed of 6.0 km/h."},
                {"name": "Individual Seed Catch Cups", "purpose": "Collects discharged grain from each row drop tube independently."},
                {"name": "High-Precision Electronic Balance", "purpose": "Weighs collected seed samples with 0.01 g accuracy."},
                {"name": "Digital Vernier Flute Micrometer", "purpose": "Measures active exposed flute length inside the feed cup with 0.1 mm precision."},
                {"name": "Optical Revolution Counter", "purpose": "Counts exactly 50 drive shaft revolutions per test increment."}
            ],
            "procedure": [
                {"title": "Seed Inspection & Hopper Loading", "text": "Fill the seed drill hopper with clean, certified seed wheat, ensuring seeds are free of chaff, broken kernels, and foreign matter to prevent flute clogging."},
                {"title": "Initial Flute Exposure Setting", "text": "Loosen the lateral feed adjustment collar and set the fluted roller active exposure to L = 10.0 mm using the vernier micrometer, locking the collar clamp securely."},
                {"title": "Pre-Run Prime & Leveling", "text": "Operate the drive shaft for 20 revolutions to fill all flute recesses and establish steady-state gravity seed flow across all cups."},
                {"title": "Timed Calibration Collection", "text": "Place catch pans under the seed tubes, operate the drive shaft at exactly 40 RPM for exactly 1.0 minute (or 50 revolutions), and collect all discharged grain."},
                {"title": "Gravimetric Weighing", "text": "Weigh the collected seed from each row on the electronic balance, averaging across the rows to calculate mean discharge rate q (g/min)."},
                {"title": "Linear Calibration Curve", "text": "Repeat the procedure at 15, 20, 25, 30, and 35 mm flute exposures, plot discharge versus exposure, and extract the calibration gradient c_q."}
            ],
            "topics": [
                {"question": "How does a fluted-roller feed mechanism meter agricultural seeds?", "answer": "The mechanism combines two delivery actions: positive displacement of seeds trapped inside the rotating flute flutes, and dragging flow in the active mantle layer immediately surrounding the outer periphery of the rotating cylinder."},
                {"question": "Why is seed drill calibration essential before every planting season?", "answer": "Variations in seed size, seed dressing treatments, moisture content, and thousand-grain weight alter bulk density and internal friction, causing substantial deviations from nominal factory calibration charts."},
                {"question": "How is laboratory stationary calibration converted to field application rate (kg/ha)?", "answer": "Application rate Q (kg/ha) = (q_total × 10,000) / (W × D), where q_total is total seed discharged per test run (kg), W is drill working width (m), and D is equivalent travel distance = π × wheel diameter × revolutions (m)."},
                {"question": "What is the primary cause of inter-row variation in a multi-row seed drill?", "answer": "Inter-row variation is caused by unequal flute exposure due to manufacturing tolerances or loose set screws on the common feed shaft, warped seed cup castings, or uneven hopper filling."},
                {"question": "What adjustments are made when switching from small seeds (wheat) to very small seeds (canola)?", "answer": "Canola requires very small exposures or special fine-seed inserts, closing the bottom gate tongue clearance, and using the slowest drive sprocket ratio to avoid crushing delicate seed coats."},
                {"question": "How does ground wheel drive wheel slip affect seeding rate in the field?", "answer": "Drive wheel slip causes the wheel to turn fewer revolutions than the actual ground distance traveled, leading to under-seeding unless the drill calibration factor is corrected for expected field slip (typically 5% to 10%)."}
            ],
            "precautions": [
                "Always run the mechanism through a prime cycle before collecting data so flutes are fully charged with seed.",
                "Ensure all row feed cut-off gates are clamped tightly against the common adjustment bar to prevent inter-row divergence.",
                "Maintain seed hopper level above one-third capacity to ensure constant hydrostatic seed head pressure.",
                "Verify that drop tubes hang vertically without kinks or bends that could cause seed bridging."
            ],
            "limitations": [
                "The calibration applies strictly to the tested seed lot; different crop varieties or seed treatments require re-calibration.",
                "Assumes zero drive wheel slip in stationary stand conditions; field correction factors must be applied for soft soils.",
                "At very low exposures (L < 5 mm), mechanical seed damage and crushing can occur along the cutoff edge.",
                "High ambient relative humidity can increase seed surface friction, slightly reducing gravity flow rates."
            ],
            "quiz": [
                {
                    "question": "What is the primary method of adjusting seeding rate on a fluted-roller grain drill?",
                    "options": ["Changing tractor engine oil pressure", "Sliding the fluted feed shaft laterally to change exposed flute length inside the seed cup", "Tilting the entire hopper backwards", "Varying drop tube diameter"],
                    "correct": 1,
                    "explanation": "Seeding rate is adjusted primarily by shifting the feed shaft laterally to vary the active exposed length of the fluted cylinder inside the seed cup."
                },
                {
                    "question": "If a drill discharges 170 g/min at L = 20 mm, what discharge is expected at L = 30 mm given linear calibration?",
                    "options": ["170 g/min", "255 g/min", "340 g/min", "510 g/min"],
                    "correct": 1,
                    "explanation": "Gradient c_q = 170 / 20 = 8.5 g/(min·mm). At L = 30 mm, q = 8.5 × 30 = 255 g/min."
                },
                {
                    "question": "If tractor wheel slip in the field is 10%, how will uncorrected seed rate compare to stationary calibration?",
                    "options": ["10% over-seeded", "10% under-seeded", "Unaffected", "Double the rate"],
                    "correct": 1,
                    "explanation": "Because the drive wheel turns 10% fewer revolutions over the same distance, 10% less seed is metered per hectare."
                },
                {
                    "question": "Which agricultural crop is conventionally planted using fluted-roller seed drills?",
                    "options": ["Cotton", "Wheat", "Corn", "Potatoes"],
                    "correct": 1,
                    "explanation": "Wheat and other small cereals are universally drilled using fluted-roller continuous metering mechanisms."
                }
            ],
            "settings": ["Crop: Seed wheat (TGW = 42.5 g)", "Test shaft speed: 40 RPM (6.0 km/h equivalent)", "Row spacing: 17.5 cm"],
            "samples": [10.0, 15.0, 20.0, 25.0, 30.0, 35.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🚜", "label": "1. Seed Drill Metering Stand"},
                {"id": "compare", "icon": "📊", "label": "2. Discharge vs Exposure Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Flute Opening Sandbox"}
            ]
        },
        {
            "number": 6,
            "slug": "precision-planter-seed-spacing-uniformity",
            "title": "Vacuum Precision Planter Seed Spacing Uniformity & Miss/Multiple Indices",
            "shortTitle": "Precision Planter Spacing",
            "aim": "Evaluate the seed spacing uniformity, miss index, and multiple index of a vacuum disc precision planter unit as a function of forward planting speed.",
            "inputLabel": "Forward Planting Speed V",
            "shortInput": "Speed V",
            "inputUnit": "km/h",
            "min": 3.0,
            "max": 9.0,
            "step": 1.2,
            "initial": 5.4,
            "inputDecimals": 1,
            "rawLabel": "Seed Spacing Standard Deviation σ_s",
            "rawUnit": "cm",
            "rawDecimals": 2,
            "xAxis": "Forward speed V (km/h)",
            "yAxis": "Spacing standard deviation σ_s (cm)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 6.0,
            "emptyY": 3.2,
            "targetName": "Spacing Velocity Sensitivity b_v",
            "target": "0.4500",
            "refValue": 0.4500,
            "resultUnit": "cm/(km/h)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "σ_s = b_v · V + σ_0 = 0.4500 · V + 0.5000",
            "intro": "Row crop precision planting of corn, soybeans, sunflower, and cotton demands strict singulation—depositing individual seeds at precise, equidistant intervals along the furrow to minimize plant-to-plant competition and optimize grain yield. Vacuum precision metering units utilize a vertical perforated circular plate rotating through a seed reservoir under differential pneumatic pressure. A vacuum blower creates suction across plate seed holes, holding individual seeds securely against the plate until they reach the release cutoff point above the seed delivery tube, where vacuum is interrupted. In accordance with ISO 7256/1 and ASABE S561 standards, planter performance is characterized by three key metrics: quality of feed index (spacings between 0.5 and 1.5 times the theoretical spacing), miss index (spacings > 1.5 times nominal), and multiple index (spacings < 0.5 times nominal). As forward travel velocity V increases, the required angular speed of the metering plate increases proportionally, reducing cell fill time, inducing pneumatic bounce in the drop tube, and increasing the spacing standard deviation σ_s.",
            "modelExtra": "Evaluated on a laboratory greased belt test stand using hybrid seed corn (nominal target spacing = 15.0 cm, vacuum level = 4.5 kPa).",
            "apparatus": [
                {"name": "Laboratory Greased Belt Planter Test Stand", "purpose": "Continuously captures dropped seeds without rolling or bouncing on a sticky oil-coated belt."},
                {"name": "Vacuum Precision Planter Row Unit", "purpose": "Commercial row unit with 24-hole seed disc, adjustable seed singulator, and optical sensor."},
                {"name": "Variable-Frequency Vacuum Blower", "purpose": "Maintains constant negative gauge pressure across the seed disc chamber."},
                {"name": "High-Speed Optical Seed Drop Sensor", "purpose": "Logs microsecond time-stamps of seed transit down the delivery tube."},
                {"name": "Digital Laser Displacement Scanner", "purpose": "Measures exact spatial positions of seeds adhered to the greased belt."},
                {"name": "Digital Vacuum Manometer", "purpose": "Monitors metering chamber differential pressure with 0.05 kPa precision."}
            ],
            "procedure": [
                {"title": "Seed Disc Selection & Vacuum Set", "text": "Install a 24-hole corn disc (4.5 mm hole diameter) into the metering unit, setting the vacuum level to 4.5 kPa using the variable-frequency blower."},
                {"title": "Singulator Clearance Adjustment", "text": "Adjust the dual singulator fingers to dislodge doubles while retaining single kernels over each suction orifice."},
                {"title": "Greased Belt Stand Synchronization", "text": "Set the belt drive motor to initial forward speed V = 3.0 km/h, synchronizing the planter drive shaft to achieve a nominal theoretical seed spacing of 15.0 cm."},
                {"title": "Continuous Seed Drop Logging", "text": "Operate the planter unit to deposit a sample run of at least 250 consecutive seeds onto the moving greased belt."},
                {"title": "Spatial Coordinate Mapping", "text": "Record the center-to-center distances between consecutive seeds using the laser scanner, computing mean spacing x_bar, standard deviation σ_s, miss index, and multiple index."},
                {"title": "Velocity Stepping", "text": "Repeat the test across speeds of 4.2, 5.4, 6.6, 7.8, and 9.0 km/h, plotting spacing standard deviation versus speed to determine sensitivity b_v."}
            ],
            "topics": [
                {"question": "Explain the working principle of a vacuum precision planter metering unit.", "answer": "A vacuum fan evacuates air from one side of a perforated disc rotating through the seed pool. Atmospheric pressure holds individual seeds against each orifice. An adjustable singulator removes excess seeds, and a vacuum cutoff seal releases the single seed at the top of the drop tube into the furrow."},
                {"question": "How are Miss Index, Multiple Index, and Quality of Feed Index defined by ASABE S561?", "answer": "For a theoretical spacing x_ref: Multiple Index is the percentage of spacings ≤ 0.5·x_ref; Miss Index is the percentage > 1.5·x_ref; and Quality of Feed Index is the percentage falling within the acceptable target window 0.5·x_ref to 1.5·x_ref."},
                {"question": "Why does planter speed adversely affect seed spacing uniformity?", "answer": "Higher speed forces the metering disc to rotate faster, reducing seed cell residence time in the hopper (causing misses), while seeds falling down the drop tube experience higher air turbulence and tube wall collisions, scattering furrow arrival times."},
                {"question": "What is the role of the seed singulator mechanism?", "answer": "The singulator consists of staggered scalloped edge plates that gently bump seeds perched on disc holes, dislodging extra clinging seeds so exactly one seed remains seated over each hole."},
                {"question": "How does drop tube curvature design influence seed spacing on the ground?", "answer": "A parabolic rear-curved drop tube imparts a rearward exit velocity to the seed matching the forward ground speed of the planter, achieving zero relative ground speed at exit to eliminate seed rolling and bounce in the furrow."},
                {"question": "What are the consequences of poor seed spacing uniformity on final corn grain yield?", "answer": "Non-uniform spacing creates crowded clusters (inducing mutual shading and barren stalks) alongside wide gaps (wasting solar radiation and soil nutrients), reducing overall field yield by 5% to 15%."}
            ],
            "precautions": [
                "Ensure vacuum seals between disc and housing are airtight; worn rubber seals cause pressure leakage and erratic cell filling.",
                "Maintain uniform grease coating thickness on the test stand belt to prevent seed rolling upon impact.",
                "Use graded, sized hybrid seed corn matched to disc orifice diameter.",
                "Ensure optical drop sensors are free from graphite and talc seed lubricant dust."
            ],
            "limitations": [
                "Greased belt test stands eliminate furrow bounce and soil roll, reflecting pure metering unit performance rather than rough field furrow dynamics.",
                "Assumes perfect seed sizing; cracked or irregular seeds degrade singulation accuracy.",
                "Applies to singulated row crops (corn, sunflower) and is not applicable to mass-drilled cereal grains.",
                "Static stand eliminates tractor pitch and roll vibrations present under real field terrain."
            ],
            "quiz": [
                {
                    "question": "According to ASABE standards, a seed spacing measured at 6.0 cm when target spacing is 15.0 cm is classified as:",
                    "options": ["A Quality of Feed spacing", "A Multiple", "A Miss", "An Outlier"],
                    "correct": 1,
                    "explanation": "Because 6.0 cm is less than 0.5 × 15.0 cm (7.5 cm), it falls into the multiple index category."
                },
                {
                    "question": "What physical parameter dictates the maximum operational planting speed of a vacuum planter?",
                    "options": ["Tractor alternator voltage", "Seed plate cell fill time and drop tube bounce kinetics", "Fuel tank capacity", "Exhaust gas temperature"],
                    "correct": 1,
                    "explanation": "As speed increases, seed cell fill time in the hopper becomes too short to capture seeds reliably, while drop tube bounce scatters spacing."
                },
                {
                    "question": "What is the function of talc or graphite lubricants mixed with seed in vacuum planters?",
                    "options": ["Provide fertilizer nutrition", "Reduce seed-to-disc and seed-to-seed friction to prevent bridging and static cling", "Repel birds", "Accelerate germination"],
                    "correct": 1,
                    "explanation": "Talc and graphite powder lubricate seeds and dissipate electrostatic charges, ensuring smooth release from metering discs."
                },
                {
                    "question": "If spacing standard deviation is σ_s = 0.45·V + 0.50 cm, what is the expected deviation at V = 8.0 km/h?",
                    "options": ["2.5 cm", "3.6 cm", "4.1 cm", "5.2 cm"],
                    "correct": 2,
                    "explanation": "σ_s = 0.45 × 8.0 + 0.50 = 3.60 + 0.50 = 4.10 cm."
                }
            ],
            "settings": ["Disc: 24-hole corn disc (4.5 mm)", "Target spacing: 15.0 cm", "Vacuum level: 4.5 kPa"],
            "samples": [3.0, 4.2, 5.4, 6.6, 7.8, 9.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🚜", "label": "1. Greased Belt Planter Stand"},
                {"id": "compare", "icon": "📊", "label": "2. Spacing Histogram"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Speed & Vacuum Sandbox"}
            ]
        },
        {
            "number": 7,
            "slug": "hydraulic-spray-nozzle-droplet-distribution",
            "title": "Hydraulic Spray Nozzle Discharge, Droplet VMD & Patternation Uniformity",
            "shortTitle": "Spray Nozzle Patternation",
            "aim": "Measure the liquid discharge rate and patternation uniformity of an agricultural hydraulic flat-fan spray nozzle across varying operating pressures using a patterned patternator table.",
            "inputLabel": "Square Root of Pressure √P",
            "shortInput": "√Pressure",
            "inputUnit": "bar^0.5",
            "min": 1.0,
            "max": 2.5,
            "step": 0.3,
            "initial": 1.6,
            "inputDecimals": 2,
            "rawLabel": "Nozzle Liquid Discharge Q",
            "rawUnit": "L/min",
            "rawDecimals": 3,
            "xAxis": "Square root of pressure √P (bar^0.5)",
            "yAxis": "Liquid discharge Q (L/min)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 1.75,
            "emptyY": 1.488,
            "targetName": "Nozzle Flow Coefficient C_n",
            "target": "0.8500",
            "refValue": 0.8500,
            "resultUnit": "L/(min·bar^0.5)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "Q = C_n · √P = 0.8500 · √P",
            "intro": "Agricultural chemical application via tractor-mounted boom sprayers is critical for crop protection, weed management, and foliar fertilization. Hydraulic flat-fan spray nozzles convert pressurized liquid into a sheet of liquid that atomizes into millions of airborne droplets through aerodynamic surface wave instability. The flow rate through an orifice nozzle adheres strictly to the Torricelli orifice discharge law, scaling linearly with the square root of pressure: Q = C_n·√P. Simultaneously, pressure governs atomization quality: increasing operating pressure reduces the Volume Median Diameter (VMD or D_v0.5) of the droplets, shifting the spectrum toward fine mists (< 150 μm) that are highly susceptible to airborne spray drift. Conversely, insufficient pressure produces coarse droplets and narrow spray fan angles that cause streaking and non-uniform chemical deposition. Evaluating the transversal distribution pattern on a grooved patternator table allows calculation of Christiansen's Uniformity Coefficient (CU) and determination of the optimum boom height and nozzle overlap.",
            "modelExtra": "Evaluated using standard ISO 110-02 flat-fan brass nozzle spraying clean water at 20°C across pressures from 1.0 to 6.25 bar (√P from 1.0 to 2.5 bar^0.5).",
            "apparatus": [
                {"name": "Agricultural Spray Nozzle Test Bench", "purpose": "Closed-circuit pump system with pressure regulator, pulsation damper, and boom height adjustment."},
                {"name": "Standard ISO 110-02 Extended Range Flat-Fan Nozzle", "purpose": "Industry standard 110° fan angle hydraulic atomizing nozzle."},
                {"name": "Patternator Grooved Table & Manometer Tubes", "purpose": "Collects transverse spray liquid in 2.5 cm channels across a 1.5 m swath width."},
                {"name": "Digital Calibrated Pressure Transducer", "purpose": "Measures nozzle inlet hydrostatic pressure with 0.01 bar precision."},
                {"name": "Electronic Volumetric Cylinder & Balance", "purpose": "Measures total timed nozzle liquid discharge with 1.0 mL accuracy."},
                {"name": "Laser Diffraction Droplet Size Analyzer", "purpose": "Records droplet spectrum, VMD (D_v0.5), and driftable fine fraction (< 105 μm)."}
            ],
            "procedure": [
                {"title": "Nozzle Mounting & Boom Alignment", "text": "Mount the ISO 110-02 nozzle on the test boom at exactly 50 cm height above the patternator table, aligning the spray fan at a 5° angle to the boom axis to prevent interference."},
                {"title": "Pressure Stabilization", "text": "Start the diaphragm pump, bleeding all air from the boom line, and adjust the pressure relief valve to initial pressure P = 1.00 bar (√P = 1.00 bar^0.5)."},
                {"title": "Timed Discharge Measurement", "text": "Collect the full nozzle discharge in a graduated cylinder over exactly 60 seconds, recording the total volume Q (L/min) on the digital balance."},
                {"title": "Patternator Volume Logging", "text": "Allow spray to drain into the patternator graduated tubes for 2.0 minutes, recording the liquid height in each channel to plot the transverse distribution profile."},
                {"title": "Pressure Stepping", "text": "Increase operating pressure across five additional increments up to 6.25 bar (√P = 1.3, 1.6, 1.9, 2.2, 2.5 bar^0.5), repeating discharge and droplet VMD scans."},
                {"title": "Flow Coefficient Extraction", "text": "Plot discharge Q against √P, perform linear regression to determine nozzle flow coefficient C_n, and evaluate the pressure-droplet size trade-off."}
            ],
            "topics": [
                {"question": "State the Torricelli orifice flow law governing agricultural hydraulic spray nozzles.", "answer": "Flow rate through a hydraulic orifice is Q = C_d·A·√(2·ΔP / ρ), where C_d is the discharge coefficient, A is orifice area, ΔP is pressure drop, and ρ is liquid density. Consolidating constants yields Q = C_n·√P."},
                {"question": "What is Volume Median Diameter (VMD or D_v0.5)?", "answer": "VMD is the droplet diameter such that 50% of the total sprayed liquid volume is contained in droplets larger than this diameter, and 50% is contained in droplets smaller, serving as the benchmark metric for spray coarseness."},
                {"question": "Explain the trade-off between biological efficacy and airborne spray drift.", "answer": "Smaller droplets (< 150 μm) provide superior leaf surface coverage and chemical uptake but drift off-target under wind currents, causing environmental contamination. Larger droplets (> 300 μm) resist drift but can bounce off leaves or provide inadequate pest coverage."},
                {"question": "What is the standard nozzle spacing and overlap for a 110° flat-fan boom?", "answer": "Standard nozzle spacing along the boom is 50 cm. At 50 cm boom height, 110° nozzles produce overlapping spray fans such that each point on the crop canopy receives 100% overlap (double coverage) from adjacent nozzles, ensuring uniform deposition."},
                {"question": "How do air-induction (venturi) spray nozzles reduce drift?", "answer": "Air-induction nozzles use a venturi orifice to aspirate air into the fluid stream, producing larger, air-filled liquid droplets that resist wind drift and shatter upon leaf impact to maintain surface spreading."},
                {"question": "Why are nozzle spray tips rotated 5° to 10° relative to the boom line?", "answer": "Rotating the tips slightly prevents the outer edges of adjacent overlapping spray fans from colliding in mid-air, which would cause droplet coalescence and heavy liquid streaks along the overlap zone."}
            ],
            "precautions": [
                "Operate spray test equipment exclusively with clean water; never use hazardous crop protection chemicals in laboratory teaching patternators.",
                "Inspect nozzle orifice under an optical microscope for erosion, scratches, or burrs prior to testing.",
                "Ensure pressure transducer is mounted directly at the nozzle check-valve body to avoid boom friction pressure drops.",
                "Wear protective safety goggles and operate exhaust ventilation during high-pressure mist trials."
            ],
            "limitations": [
                "Water calibration curves differ slightly from commercial pesticide tank mixes containing surfactants, adjuvants, or crop oils that alter surface tension and viscosity.",
                "Orifice wear increases C_n over time; nozzles discharging > 10% above nominal rating must be replaced.",
                "Patternator table channels evaluate static 1D transverse profile without simulating tractor forward travel dynamics.",
                "Drop size laser measurements can be distorted by multiple scattering in ultra-dense spray plumes."
            ],
            "quiz": [
                {
                    "question": "If nozzle pressure increases by a factor of 4 (from 1 bar to 4 bar), how does flow rate change?",
                    "options": ["Flow rate increases by a factor of 4", "Flow rate doubles (increases by a factor of 2)", "Flow rate increases by a factor of 16", "Flow rate remains unchanged"],
                    "correct": 1,
                    "explanation": "Because Q ∝ √P, quadrupling pressure doubles the discharge rate (√4 = 2)."
                },
                {
                    "question": "Which droplet size category is most susceptible to airborne spray drift?",
                    "options": ["Droplets > 500 μm", "Droplets between 300 and 450 μm", "Droplets < 105 μm (driftable fines)", "Solid fertilizer pellets"],
                    "correct": 2,
                    "explanation": "Droplets smaller than 105 μm fall very slowly through air and are easily carried away by ambient crosswinds before reaching the crop canopy."
                },
                {
                    "question": "What ISO nozzle color code corresponds to an ISO 02 nozzle (0.2 gallons/min at 40 psi)?",
                    "options": ["Blue", "Yellow", "Red", "Brown"],
                    "correct": 1,
                    "explanation": "In the international ISO 10625 color coding standard, Yellow corresponds to size 02 (0.8 L/min at 3 bar)."
                },
                {
                    "question": "For an ISO 110° nozzle spaced at 50 cm along the boom, what is the standard recommended boom height?",
                    "options": ["15 cm", "50 cm", "120 cm", "200 cm"],
                    "correct": 1,
                    "explanation": "A 50 cm boom height with 50 cm nozzle spacing provides the optimal 100% overlap pattern for 110° flat-fan nozzles."
                }
            ],
            "settings": ["Nozzle type: ISO 110-02 Extended Range", "Boom height: 50.0 cm", "Test fluid: Water at 20°C"],
            "samples": [1.0, 1.3, 1.6, 1.9, 2.2, 2.5],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🚜", "label": "1. Spray Patternator Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Q vs √Pressure Plot"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Pressure & VMD Sandbox"}
            ]
        },
        {
            "number": 8,
            "slug": "reciprocating-cutterbar-knife-velocity-ratio",
            "title": "Combine Reciprocating Cutterbar Kinematics & Knife Velocity Ratio",
            "shortTitle": "Reciprocating Cutterbar Kinematics",
            "aim": "Analyze the kinematics of an agricultural reciprocating mower/combine cutterbar and determine the knife-to-forward velocity ratio across increasing machine travel speeds.",
            "inputLabel": "Machine Forward Travel Speed V_f",
            "shortInput": "Speed V_f",
            "inputUnit": "m/s",
            "min": 1.0,
            "max": 3.0,
            "step": 0.4,
            "initial": 1.8,
            "inputDecimals": 1,
            "rawLabel": "Peak Cutterbar Knife Velocity V_k",
            "rawUnit": "m/s",
            "rawDecimals": 3,
            "xAxis": "Forward speed V_f (m/s)",
            "yAxis": "Peak knife speed V_k (m/s)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 2.0,
            "emptyY": 2.7,
            "targetName": "Kinematic Velocity Ratio K_v",
            "target": "1.3500",
            "refValue": 1.3500,
            "resultUnit": "ratio",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "V_k = K_v · V_f = 1.3500 · V_f",
            "intro": "Reciprocating cutterbars are universally utilized on combine harvester grain platforms, forage mowers, and swathers to sever crop stems cleanly at ground level. The cutting mechanism consists of a row of triangular serrated knife sections riveted to a reciprocating knifeback sliding between stationary forged-steel ledger plates and crop guards. The knife is driven in simple harmonic motion by a wobble-box or slider-crank pitman drive powered by the combine header shaft. Proper cutting action requires that the cutterbar knife achieve a critical kinematic velocity ratio K_v = V_k / V_f (where V_k is peak knife speed and V_f is machine forward velocity). If K_v is too low (excessive ground speed or slow knife speed), crop stems are pushed forward and bruised rather than cleanly sheared, resulting in high shattering losses, uneven stubble, and cutterbar plugging. Conversely, excessively high K_v causes severe machine structural vibration, accelerated ledger wear, and wasted kinetic energy. In this investigation, an instrumented cutterbar test rig equipped with linear optical encoders and a variable-speed track carriage evaluates cutting kinematics.",
            "modelExtra": "Evaluated at synchronized crank stroke S = 76.2 mm (3 inches) matching guard spacing (standard registration). Linear velocity ratio K_v = 1.3500 establishes clean shearing.",
            "apparatus": [
                {"name": "Laboratory Reciprocating Cutterbar Test Rig", "purpose": "Standard 2.0 m combine header section with 76.2 mm guard spacing and hardened knife sections."},
                {"name": "Precision Wobble-Box Drive Mechanism", "purpose": "Converts rotary input torque into pure linear reciprocating cutterbar motion with minimal vertical deflection."},
                {"name": "Linear Magnetic Optical Encoder", "purpose": "Tracks instantaneous knife position x(t) and velocity v(t) with 0.05 mm accuracy."},
                {"name": "Carriage Rail Drive System", "purpose": "Propels the test rig forward at controlled speeds from 1.0 to 3.0 m/s."},
                {"name": "Crop Stem Shearing Load Cell", "purpose": "Measures cutting peak shear forces on individual ledger plates."},
                {"name": "High-Speed Video Motion Analyzer", "purpose": "Records visual stem deflection, knife entrance, and shear severance timing."}
            ],
            "procedure": [
                {"title": "Cutterbar Alignment & Register Check", "text": "Verify cutterbar knife register by ensuring that knife section tip centers align precisely with guard centers at the stroke reversal dead-center points."},
                {"title": "Knife Clip Clearance Adjustment", "text": "Set hold-down knife clips to provide 0.25 to 0.50 mm vertical clearance above knife sections, preventing binding while maintaining close shear contact with ledger plates."},
                {"title": "Initial Speed Synchronization", "text": "Set forward carriage drive speed to V_f = 1.0 m/s and synchronize wobble-box crank speed to establish target cutting ratio."},
                {"title": "Kinematic Waveform Logging", "text": "Execute test run over the 15-meter track, recording linear encoder position-time telemetry at 1000 Hz throughout the cutting stroke."},
                {"title": "Speed Stepping", "text": "Increment machine forward speed across five additional steps up to 3.0 m/s, measuring peak knife velocity V_k for each trial."},
                {"title": "Velocity Ratio Extraction", "text": "Compute peak knife velocity V_k = ω·(S/2), plot V_k against V_f, and determine the kinematic velocity ratio K_v via linear regression."}
            ],
            "topics": [
                {"question": "What is cutterbar 'register' and why is it critical?", "answer": "Register refers to the position of the knife section relative to the guard at the ends of the stroke. In standard registration, the knife center must align exactly with the guard ledger plate center at dead center to ensure the full cutting stroke shears the stem against the stationary ledger."},
                {"question": "How is the cutting action of a reciprocating cutterbar accomplished?", "answer": "The plant stem is gathered by adjacent crop guards, supported against the ledger plate shear edge, and severed by the dual cutting edges of the advancing knife section in a shearing action analogous to scissors."},
                {"question": "What happens when machine forward speed is too high relative to knife speed?", "answer": "The plant stems are pushed forward and bent over before the knife can shear them, leading to uneven stubble height, severe seed head shattering losses, and stalk clogging in the guard throats."},
                {"question": "Describe the mathematical motion of a pitman-driven knife.", "answer": "The knife displacement is x(t) = r·cos(ω·t), its velocity is v(t) = -r·ω·sin(ω·t), and acceleration is a(t) = -r·ω²·cos(ω·t), where r = S/2 is the crank radius and ω is angular velocity in rad/s."},
                {"question": "Why do modern combine headers utilize wobble-boxes rather than long pitman arms?", "answer": "Wobble-boxes eliminate the heavy reciprocating pitman arm, reduce angular vertical shaking forces, allow higher cyclic speeds (up to 600-700 RPM), and fit compactly within the header side sheet."},
                {"question": "What is the function of the wear plates beneath the knifeback?", "answer": "Wear plates support the rear edge of the knifeback, absorbing the rearward thrust of the cutting action and maintaining parallel alignment with the ledger plates."}
            ],
            "precautions": [
                "Keep hands and clothing clear of the reciprocating knife at all times; always lock out carriage power during clearance checks.",
                "Verify hold-down clip clearances across all guards to prevent localized knife friction and drive overheating.",
                "Ensure knife section rivets or bolts are torqued to specification; a loose section can jam the cutterbar instantly.",
                "Inspect guard ledger plates for chipped or rounded shear edges prior to test runs."
            ],
            "limitations": [
                "Harmonic kinematics assume a rigid knifeback; real-world flexure under heavy stem loads introduces slight harmonic distortion.",
                "Tested on simulated straw/dowel stands; natural crop lodging and weeds create variable cutting resistance.",
                "Does not account for reel finger gathering interactions ahead of the cutterbar.",
                "Applies to conventional single-knife systems; dual-knife drive systems operate with opposed reciprocating masses."
            ],
            "quiz": [
                {
                    "question": "What is the standard guard spacing on modern agricultural combine grain platforms?",
                    "options": ["25.4 mm (1 inch)", "76.2 mm (3 inches)", "152.4 mm (6 inches)", "300 mm (12 inches)"],
                    "correct": 1,
                    "explanation": "Standard agricultural reciprocating cutterbars feature 76.2 mm (3 inches) spacing between guard centers and knife stroke."
                },
                {
                    "question": "What is the primary cutting mechanism between knife section and ledger plate?",
                    "options": ["Tensile rupture", "True scissor-action shearing", "Impact shattering", "Abrasive grinding"],
                    "correct": 1,
                    "explanation": "The cutterbar functions as a continuous scissor mechanism, shearing stems between the moving knife edge and the stationary ledger plate."
                },
                {
                    "question": "At dead center (ends of the cutterbar stroke), what is the instantaneous knife velocity?",
                    "options": ["Maximum velocity", "Zero velocity", "Half of maximum", "Double of maximum"],
                    "correct": 1,
                    "explanation": "At the stroke reversal points (dead centers), the reciprocating knife momentarily comes to a complete stop (velocity = 0)."
                },
                {
                    "question": "If forward speed is V_f = 2.0 m/s and velocity ratio is K_v = 1.35, what is the peak knife speed?",
                    "options": ["1.35 m/s", "2.00 m/s", "2.70 m/s", "4.05 m/s"],
                    "correct": 2,
                    "explanation": "Peak knife speed V_k = K_v × V_f = 1.35 × 2.0 m/s = 2.70 m/s."
                }
            ],
            "settings": ["Stroke S: 76.2 mm (3.0 in)", "Guard spacing: 76.2 mm", "Hold-down clearance: 0.35 mm"],
            "samples": [1.0, 1.4, 1.8, 2.2, 2.6, 3.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🚜", "label": "1. Cutterbar Kinematic Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Velocity Ratio Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Crank Speed Sandbox"}
            ]
        },
        {
            "number": 9,
            "slug": "axial-flow-threshing-cylinder-grain-separation",
            "title": "Axial-Flow Threshing Cylinder Peripheral Speed & Grain Separation Efficiency",
            "shortTitle": "Threshing Cylinder Efficiency",
            "aim": "Determine the effect of threshing drum peripheral speed on grain separation efficiency and unthreshed grain loss in an axial-flow combine threshing mechanism.",
            "inputLabel": "Cylinder Peripheral Velocity v_c",
            "shortInput": "Velocity v_c",
            "inputUnit": "m/s",
            "min": 20.0,
            "max": 32.0,
            "step": 2.4,
            "initial": 26.0,
            "inputDecimals": 1,
            "rawLabel": "Threshing Separation Metric E_t",
            "rawUnit": "%",
            "rawDecimals": 2,
            "xAxis": "Cylinder velocity v_c (m/s)",
            "yAxis": "Threshing separation metric E_t (%)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 26.0,
            "emptyY": 89.9,
            "targetName": "Threshing Sensitivity Gradient s_t",
            "target": "1.1500",
            "refValue": 1.1500,
            "resultUnit": "%/(m/s)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "E_t = s_t · v_c + E_0 = 1.1500 · v_c + 60.0000",
            "intro": "Grain threshing in modern combine harvesters detaches grain kernels from their seed heads or pods through a combination of impact, rubbing friction, and centrifugal separation. In axial-flow threshing cylinders, crop material spirals longitudinally along the rotor axis inside a perforated concave grate, making multiple passes over rasp-bars or spiked teeth. The drum peripheral speed v_c = π·D·N / 60 is the dominant operational variable governing threshing effectiveness. Increasing peripheral velocity imparts higher kinetic impact energy to shatter glumes and pods, accelerating grain detachment and improving the separation percentage through the concave grates. However, excessive cylinder speed shatters brittle straw (overloading the cleaning shoe sieves) and induces internal grain pericarp cracking and embryo damage, reducing germination and seed market grade. Conversely, insufficient speed leaves unthreshed heads that are lost in the straw discharge. In this laboratory investigation, an instrumented pilot threshing drum processes standard grain batches across six controlled peripheral speeds to calibrate the separation sensitivity gradient.",
            "modelExtra": "Evaluated using conditioned wheat sheaves (grain moisture 13.5% d.b.) at constant concave clearance of 12 mm inlet / 6 mm outlet.",
            "apparatus": [
                {"name": "Instrumented Axial-Flow Threshing Test Unit", "purpose": "Single-rotor laboratory combine cylinder with adjustable concave grate and variable-speed drive."},
                {"name": "Variable-Frequency Rotor Motor Drive", "purpose": "Regulates cylinder rotational speed from 400 to 900 RPM with 1.0 RPM digital feedback."},
                {"name": "Concave Under-Grate Collection Pans", "purpose": "Captures separated grain and chaff passing through the concave bars."},
                {"name": "Straw Discharge Collector", "purpose": "Traps all expelled straw and unthreshed seed heads for manual loss auditing."},
                {"name": "Electronic Analytical Grain Balance", "purpose": "Weighs separated grain, unthreshed grain, and straw fractions with 0.1 g accuracy."},
                {"name": "Optical Grain Crack / Damage Inspection Stand", "purpose": "Quantifies mechanical kernel damage and pericarp cracking using tetrazolium staining."}
            ],
            "procedure": [
                {"title": "Concave Clearance Calibration", "text": "Set the front concave inlet clearance to 12.0 mm and the rear outlet clearance to 6.0 mm using feeler thickness gauges, locking the adjustment lever."},
                {"title": "Standardized Batch Preparation", "text": "Prepare uniform 10.0 kg batches of conditioned wheat sheaves with known grain-to-straw ratio (approximately 1:1.2)."},
                {"title": "Initial Speed Setting", "text": "Set rotor peripheral velocity to v_c = 20.0 m/s (rotor speed 510 RPM on 75 cm diameter cylinder), allowing the motor to stabilize at idle."},
                {"title": "Uniform Batch Feeding", "text": "Feed the 10.0 kg wheat batch uniformly onto the feed conveyor over exactly 15 seconds, collecting all concave-separated material and straw discharge."},
                {"title": "Grain Separation Recovery", "text": "Clean and weigh all grain separated through the concave (m_sep), hand-thresh all remaining unthreshed heads in the straw to find unthreshed loss (m_loss), and compute separation percentage E_t = m_sep / (m_sep + m_loss) × 100%."},
                {"title": "Velocity Incrementation", "text": "Repeat testing across velocities of 22.4, 24.8, 27.2, 29.6, and 32.0 m/s, plotting E_t versus v_c and evaluating kernel mechanical damage."}
            ],
            "topics": [
                {"question": "What are the three physical actions responsible for grain detachment in a combine cylinder?", "answer": "The three actions are: (1) direct mechanical impact of rasp-bars striking seed heads, (2) rubbing and shearing friction between straw stalks as they are squeezed through the concave clearance, and (3) centrifugal force ejecting detached grain through concave grate openings."},
                {"question": "How does axial-flow threshing differ from conventional tangential threshing?", "answer": "In tangential systems, crop feeds perpendicular to the drum axis and passes through the concave in less than 0.1 seconds. In axial-flow systems, crop spirals longitudinally along the rotor axis, making multiple revolutions (typically 3 to 4 turns) over 1 to 2 seconds, which gentler handling and higher grain separation efficiency."},
                {"question": "What are the consequences of excessively high cylinder speed?", "answer": "Excessive speed causes mechanical grain cracking, embryo rupture (lowering seed germination), excessive straw pulverization that overloads cleaning sieves, and increased power consumption."},
                {"question": "What is the function of the concave grate?", "answer": "The concave grate provides a stationary curved semi-circular surface against which the rotating rasp-bars rub the crop, while its slotted openings allow separated grain to fall through immediately onto the grain pan before reaching the straw walkers or discharge rotor."},
                {"question": "How does grain moisture content affect the required threshing speed?", "answer": "Wet, tough grain requires higher cylinder speeds and tighter concave clearances to break the damp, flexible glumes, whereas dry, brittle grain requires lower speeds and wider clearances to prevent severe kernel cracking."},
                {"question": "What is unthreshed grain loss and where does it exit the combine?", "answer": "Unthreshed loss represents grain kernels that remain firmly attached to unthreshed seed heads or pods after passing through the threshing mechanism; it exits the combine at the rear in the straw discharge."}
            ],
            "precautions": [
                "Feed crop uniformly along the conveyor; slug feeding causes cylinder speed drop and inaccurate loss measurements.",
                "Ensure protective wire safety cage is locked around the rotor before engaging drive motors.",
                "Allow the cylinder to run for 30 seconds after feeding to clear all residual grain before collecting samples.",
                "Inspect rasp-bars for stone damage, bent teeth, or uneven wear that would create localized clearance variations."
            ],
            "limitations": [
                "Tested with wheat; crops with delicate seed coats (e.g., soybeans, edible dry beans) require much lower peripheral speeds (10 to 18 m/s).",
                "Laboratory batch feeder does not capture dynamic continuous header auger pulsations.",
                "Assumes uniform crop moisture; wet green weeds in crop batches significantly degrade concave separation.",
                "Mechanical damage evaluations require chemical staining protocols to detect micro-cracks invisible to the naked eye."
            ],
            "quiz": [
                {
                    "question": "What is the primary operational cause of mechanical grain cracking in combine harvesters?",
                    "options": ["Excessively high cleaning fan speed", "Excessive threshing cylinder peripheral speed", "Wide concave clearance", "Dull cutterbar knife"],
                    "correct": 1,
                    "explanation": "High cylinder speed imparts excessive kinetic impact energy to kernels, cracking pericarps and shattering fragile seed embryos."
                },
                {
                    "question": "In an axial-flow combine, how does crop material travel through the threshing chamber?",
                    "options": ["Straight across tangentially in a single pass", "Spiraling longitudinally along the rotor axis", "Dropped vertically under pure gravity", "Reciprocating back and forth"],
                    "correct": 1,
                    "explanation": "Crop material in axial-flow threshers follows a helical spiral path along the length of the longitudinal rotor."
                },
                {
                    "question": "If 9.0 kg of grain is separated through the concave and 0.5 kg of grain remains unthreshed in the straw, what is the separation efficiency?",
                    "options": ["5.5%", "50.0%", "94.7%", "100.0%"],
                    "correct": 2,
                    "explanation": "Separation efficiency = 9.0 / (9.0 + 0.5) × 100% = 9.0 / 9.5 × 100% = 94.74%."
                },
                {
                    "question": "What parameter is adjusted on a combine threshing cylinder when harvesting damp, tough wheat?",
                    "options": ["Increase cylinder speed and narrow the concave clearance", "Decrease cylinder speed and open concave clearance", "Shut off the vacuum fan", "Remove all rasp-bars"],
                    "correct": 0,
                    "explanation": "Tough, damp glumes require higher impact energy (higher speed) and tighter rubbing clearance to detach kernels."
                }
            ],
            "settings": ["Concave inlet clearance: 12.0 mm", "Concave outlet clearance: 6.0 mm", "Rotor diameter: 75.0 cm"],
            "samples": [20.0, 22.4, 24.8, 27.2, 29.6, 32.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🚜", "label": "1. Axial Cylinder Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Separation vs Speed Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Concave Clearance Sandbox"}
            ]
        },
        {
            "number": 10,
            "slug": "combine-cleaning-shoe-aerodynamic-chaff-separation",
            "title": "Combine Cleaning Shoe Aerodynamic Airflow & Grain-Chaff Separation",
            "shortTitle": "Cleaning Shoe Airflow Separation",
            "aim": "Measure the aerodynamic velocity distribution and chaff winnowing separation efficiency across a reciprocating combine cleaning shoe sieve under variable cleaning fan speeds.",
            "inputLabel": "Cleaning Fan Air Velocity U",
            "shortInput": "Air Velocity U",
            "inputUnit": "m/s",
            "min": 3.0,
            "max": 7.0,
            "step": 0.8,
            "initial": 4.6,
            "inputDecimals": 1,
            "rawLabel": "Chaff Removal Efficiency R_c",
            "rawUnit": "%",
            "rawDecimals": 2,
            "xAxis": "Cleaning air velocity U (m/s)",
            "yAxis": "Chaff removal efficiency R_c (%)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 5.0,
            "emptyY": 72.5,
            "targetName": "Chaff Separation Gradient k_c",
            "target": "14.5000",
            "refValue": 14.5000,
            "resultUnit": "%/(m/s)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "R_c = k_c · U = 14.5000 · U",
            "intro": "The cleaning shoe of a modern combine harvester performs the final critical separation of clean grain from chaff, short straw, weed seeds, and broken husks (Material Other than Grain, or MOG). The cleaning system operates through a combined aerodynamic and mechanical mechanism consisting of a centrifugal cross-flow cleaning fan, a reciprocating chaffer sieve, an adjustable lower cleaning sieve, and grain collection augers. As the threshed mixture drops from the grain pan onto the chaffer, the upward and rearward directed airflow fluidizes the mat. Because the terminal velocity of cereal grain (typically 8.0 to 10.5 m/s for wheat) is substantially higher than the terminal velocity of chaff and light straw (1.5 to 3.5 m/s), an intermediate air velocity (3.0 to 7.0 m/s) floats and suspends the chaff, blowing it out the rear of the machine, while the heavier grain kernels fall downward through the adjustable louvers onto the clean grain auger. If fan air velocity U is too low, chaff blankets the sieve louvers and grain cannot penetrate, causing sieve overload and heavy shoe loss. If air velocity exceeds the grain terminal threshold, clean grain is blown out the rear into the field. In this laboratory investigation, an instrumented full-scale cleaning shoe test rig with hot-wire anemometer arrays measures air velocity and chaff winnowing removal.",
            "modelExtra": "Evaluated using a standardized mixture of 70% wheat grain and 30% wheat chaff (by weight) at chaffer sieve louver opening of 12 mm and stroke frequency of 300 cycles/min.",
            "apparatus": [
                {"name": "Full-Scale Cleaning Shoe Laboratory Test Rig", "purpose": "Includes cross-flow fan, eccentric reciprocating chaffer and shoe sieve, and air duct vanes."},
                {"name": "Variable-Speed Centrifugal Cleaning Fan", "purpose": "Delivers controllable airflow velocities from 2.0 to 9.0 m/s across the sieve area."},
                {"name": "Multi-Point Hot-Wire Anemometer Array", "purpose": "Maps 2D airflow velocity profiles across 16 grid locations above the chaffer sieve."},
                {"name": "Clean Grain Catch Hopper & Load Cell", "purpose": "Continuously logs mass of clean grain successfully passing through the sieves."},
                {"name": "Rear Air-Chaff Cyclone Separator", "purpose": "Traps all airborne chaff blown out the rear to quantify winnowing separation."},
                {"name": "Shoe Grain Loss Sensor", "purpose": "Acoustic impact plate that counts grain kernels blown over with the chaff."}
            ],
            "procedure": [
                {"title": "Sieve Louver & Fan Choke Setup", "text": "Set the chaffer sieve louvers to 12 mm opening and lower cleaning sieve to 8 mm opening, aligning the fan windboard deflectors toward the front third of the chaffer."},
                {"title": "Velocity Grid Mapping", "text": "Engage the cleaning fan and traverse the hot-wire anemometer array across the sieve grid to establish average baseline face air velocity U = 3.0 m/s."},
                {"title": "Test Mixture Preparation", "text": "Blend a standardized 15.0 kg test batch containing 10.5 kg clean wheat and 4.5 kg wheat chaff (70:30 grain-to-chaff ratio)."},
                {"title": "Feed Delivery & Sieve Operation", "text": "Engage sieve reciprocating shake (300 cycles/min) and feed the mixture onto the pre-cleaner pan over 30 seconds."},
                {"title": "Fraction Separation & Weighing", "text": "Weigh clean grain collected in the bottom hopper (m_clean), chaff captured in the rear cyclone (m_chaff_out), and residual chaff on the sieve to calculate chaff removal efficiency R_c = (m_chaff_out / m_chaff_total) × 100%."},
                {"title": "Airflow Velocity Stepping", "text": "Increase fan speed across velocities of 3.8, 4.6, 5.4, 6.2, and 7.0 m/s, recording chaff removal R_c and monitoring grain blown-over loss."}
            ],
            "topics": [
                {"question": "Explain the principle of aerodynamic winnowing in a combine cleaning shoe.", "answer": "Winnowing exploits the difference in terminal floating velocity between grain and chaff. Airflow velocity is set between the terminal velocity of chaff (2 to 3 m/s) and grain (8 to 10 m/s), causing chaff to fluidize and blow out the rear while dense grain drops through sieve louvers."},
                {"question": "What is the function of the chaffer sieve versus the lower cleaning sieve?", "answer": "The upper chaffer sieve has coarse adjustable louvers designed to scalp off unthreshed heads and long straw while allowing grain and fine chaff through. The lower cleaning sieve has smaller openings to perform final separation, allowing only clean grain into the clean grain auger."},
                {"question": "What happens if the cleaning fan speed is set too low?", "answer": "Chaff is not fluidized and accumulates as a dense blanket over the chaffer louvers, blinding the openings and preventing clean grain from falling through, causing heavy shoe grain loss over the rear of the sieve."},
                {"question": "How do windboard deflectors influence airflow distribution over the sieves?", "answer": "Windboard deflectors direct fan air toward the front third of the chaffer where the crop mixture first drops, ensuring immediate fluidization of the dense incoming mat before it can pack onto the sieve."},
                {"question": "How does uphill versus downhill harvesting on hillsides affect cleaning shoe performance?", "answer": "On side slopes, gravity causes the fluidized crop mat to slide toward the downhill side of the sieves, leaving the uphill side bare (where air escapes uselessly) and overloading the downhill side, causing severe grain loss."},
                {"question": "What is the role of acoustic grain loss sensors at the rear of the cleaning shoe?", "answer": "Acoustic sensors use piezoelectric plates that emit electrical voltage spikes when struck by hard grain kernels, allowing the combine computer to differentiate grain strikes from soft chaff impacts and alert the operator to shoe grain loss."}
            ],
            "precautions": [
                "Ensure anemometer probes are clean and protected from dust when operating with dry agricultural chaff.",
                "Verify that reciprocating sieve drive eccentric bearings are properly lubricated to avoid excessive frame vibration.",
                "Check that sieve louvers open uniformly across the full width without bent or binding slats.",
                "Avoid operating fan at velocities > 7.5 m/s to prevent blowing sound grain out the rear."
            ],
            "limitations": [
                "Laboratory stand uses clean ambient air; field combines experience engine heat and ambient crosswinds that alter air density.",
                "Evaluates steady level terrain; hillside tilt dynamics require specialized 3D leveling shoe test rigs.",
                "Assumes dry chaff; damp green weed seeds dramatically increase chaff terminal velocity and reduce separation efficiency.",
                "Acoustic loss sensors require grain-specific calibration to accurately quantify absolute grain loss in kg/ha."
            ],
            "quiz": [
                {
                    "question": "What is the typical terminal aerodynamic floating velocity of wheat grain?",
                    "options": ["1.0 to 2.5 m/s", "4.0 to 5.5 m/s", "8.5 to 10.5 m/s", "25.0 to 30.0 m/s"],
                    "correct": 2,
                    "explanation": "Wheat kernels have a terminal velocity of approximately 8.5 to 10.5 m/s, whereas light chaff floats at 2.0 to 3.5 m/s."
                },
                {
                    "question": "If cleaning fan air velocity is set above 11 m/s in a wheat harvest, what will occur?",
                    "options": ["Severe grain cracking", "Grain will be lifted and blown out the rear with the chaff", "Engine stalling", "Sieve louvers will lock shut"],
                    "correct": 1,
                    "explanation": "Because 11 m/s exceeds the terminal velocity of wheat kernels, the airflow will suspend and blow clean grain out the rear of the combine."
                },
                {
                    "question": "What is the primary role of the chaffer sieve reciprocating shaking motion?",
                    "options": ["Crush wheat straw into silage", "Transport the fluidized crop mat rearward while allowing grain to drop through louvers", "Cool the combine transmission", "Generate vacuum suction"],
                    "correct": 1,
                    "explanation": "Reciprocating motion shakes and conveys the crop mat rearward toward the discharge while allowing dense grain to settle and drop."
                },
                {
                    "question": "If the chaff removal gradient is k_c = 14.5%/(m/s), what is the expected removal efficiency at U = 5.0 m/s?",
                    "options": ["29.0%", "50.0%", "72.5%", "95.0%"],
                    "correct": 2,
                    "explanation": "R_c = k_c × U = 14.5%/(m/s) × 5.0 m/s = 72.5%."
                }
            ],
            "settings": ["Chaffer louver opening: 12.0 mm", "Shoe frequency: 300 cycles/min", "Crop: Wheat (grain-chaff ratio 70:30)"],
            "samples": [3.0, 3.8, 4.6, 5.4, 6.2, 7.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🚜", "label": "1. Cleaning Shoe Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Chaff Removal Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Airflow Velocity Sandbox"}
            ]
        }
    ]
