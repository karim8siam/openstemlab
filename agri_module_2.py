# -*- coding: utf-8 -*-
"""Agricultural Engineering Module 2: Soil, Water & Irrigation Engineering (Labs 11–19)."""

def get_module_2():
    return [
        {
            "number": 11,
            "slug": "double-ring-infiltrometer-kostiakov-infiltration",
            "title": "Double-Ring Infiltrometer Soil Infiltration Dynamics & Kostiakov Model",
            "shortTitle": "Infiltrometer Kostiakov Model",
            "aim": "Measure the cumulative water infiltration and infiltration rate of an agricultural soil using a double-ring infiltrometer and determine Kostiakov model parameters.",
            "inputLabel": "Elapsed Infiltration Time t",
            "shortInput": "Time t",
            "inputUnit": "min",
            "min": 10.0,
            "max": 120.0,
            "step": 20.0,
            "initial": 50.0,
            "inputDecimals": 1,
            "rawLabel": "Cumulative Infiltration I",
            "rawUnit": "mm",
            "rawDecimals": 2,
            "xAxis": "ln(Time t in min)",
            "yAxis": "ln(Cumulative infiltration I in mm)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.5,
            "emptyY": 3.525,
            "targetName": "Kostiakov Infiltration Exponent α",
            "target": "0.6500",
            "refValue": 0.6500,
            "resultUnit": "dimensionless",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ln(I) = α · ln(t) + ln(c) = 0.6500 · ln(t) + 1.2500",
            "intro": "Infiltration is the physical process by which water on the ground surface enters the soil matrix under the combined influence of gravity and matric suction gradients. Accurately determining infiltration capacity is essential for designing surface irrigation systems (furrows and borders), predicting sprinkler runoff, sizing watershed drainage structures, and calculating groundwater recharge. Field infiltration is universally measured using a double-ring infiltrometer consisting of two concentric metal cylinders driven vertically into the soil. The outer buffer ring restricts horizontal lateral seepage beneath the inner ring, forcing water from the inner ring to infiltrate vertically downward in a 1D column. The empirical Kostiakov equation I = c·t^α (or its linearized logarithmic form ln I = α·ln t + ln c) describes cumulative infiltration I over time t, where α is the time exponent (typically between 0.3 and 0.8 depending on soil structure) and c is a measure of initial soil sorptivity. Differentiating yields the transient infiltration rate i = dI/dt = α·c·t^(α-1), which asymptotically approaches the basic steady-state infiltration rate i_b governed by saturated hydraulic conductivity.",
            "modelExtra": "Evaluated on undisturbed agricultural silt loam soil at 14% initial moisture. Cumulative infiltration data is linearized via natural logarithm transformation to extract α and c.",
            "apparatus": [
                {"name": "Standard Double-Ring Infiltrometer Set", "purpose": "Inner ring diameter 30 cm, outer buffer ring diameter 60 cm, height 30 cm, welded rolled steel."},
                {"name": "Heavy Steel Driving Plate & Sledgehammer", "purpose": "Drives rings into soil to 10 cm depth without disturbing the internal soil surface."},
                {"name": "Mariotte Syphon Constant-Head Bottle", "purpose": "Maintains a constant 5.0 cm water depth in the inner ring and logs water level changes."},
                {"name": "Hook Gauge & Stillwell Tube", "purpose": "Measures water level elevation in the inner ring with 0.1 mm precision."},
                {"name": "Soil Core Sampler & TDR Moisture Probe", "purpose": "Measures initial soil water content and dry bulk density in the surrounding test plot."},
                {"name": "Precision Electronic Digital Stopwatch", "purpose": "Records elapsed infiltration intervals from 1.0 to 120.0 minutes."}
            ],
            "procedure": [
                {"title": "Ring Siting & Driving", "text": "Select a representative, level site free of large stones and surface cracks. Place the double rings concentrically and drive them vertically into the soil to exactly 10 cm depth using the driving plate and hammer."},
                {"title": "Surface Scour Protection", "text": "Place a thin burlap fabric or perforated plastic sheet inside the inner ring to prevent soil surface puddling, detachment, and slaking when pouring water."},
                {"title": "Buffer Ring Filling", "text": "Fill the outer ring with water first to approximately 5 cm depth to establish an outer saturated buffer zone and prevent lateral capillary spread."},
                {"title": "Inner Ring Mariotte Startup", "text": "Rapidly fill the inner ring to exactly 5 cm depth, remove the burlap, connect the Mariotte syphon or hook gauge, and start the master stopwatch at t = 0."},
                {"title": "Elapsed Interval Logging", "text": "Record hook gauge water level drops at standardized elapsed intervals: 10, 30, 50, 70, 90, and 120 minutes, replenishing the water level to maintain steady head."},
                {"title": "Kostiakov Logarithmic Regression", "text": "Transform cumulative infiltration I (mm) and elapsed time t (min) into natural logarithms, plot ln I versus ln t, and perform linear regression to evaluate α and c."}
            ],
            "topics": [
                {"question": "Why is an outer buffer ring required in a double-ring infiltrometer?", "answer": "The outer ring saturates the perimeter soil, creating a buffer zone of water that absorbs lateral capillary spreading. This confines the water infiltrating from the inner ring to purely vertical 1D flow, yielding a true 1D infiltration measurement."},
                {"question": "State the Kostiakov and Horton infiltration equations.", "answer": "Kostiakov equation: I = c·t^α (cumulative) and i = α·c·t^(α-1) (rate). Horton's equation: i = i_c + (i_0 - i_c)·e^(-k·t), where i_0 is initial infiltration rate, i_c is steady-state ultimate rate, and k is the decay constant."},
                {"question": "How does initial soil moisture content affect the infiltration curve?", "answer": "Drier soil has higher initial matric suction gradients, resulting in a much higher initial infiltration rate. However, as the wetting front advances, matric suction gradients diminish, and the final basic infiltration rate approaches the same value regardless of initial moisture."},
                {"question": "What is the physical meaning of the Kostiakov exponent α?", "answer": "The exponent α reflects how rapidly the infiltration rate decays over time. For ideal Darcy flow under gravity, α approaches 1.0; for pure capillary diffusion, α = 0.5. In agricultural soils, α typically ranges from 0.4 to 0.7."},
                {"question": "What causes the basic infiltration rate (i_b) to remain constant after prolonged ponding?", "answer": "Once the soil profile is fully saturated to significant depth, the matric suction gradient approaches zero (dψ/dz ≈ 0). Infiltration is driven solely by gravity (unit hydraulic gradient dh/dz = 1), so the infiltration rate equals the saturated hydraulic conductivity."},
                {"question": "How does soil compaction from heavy farm machinery alter infiltration?", "answer": "Compaction crushes soil macropores, increases dry bulk density, reduces total porosity, and creates a dense subsoil plow pan, reducing the basic infiltration rate by 50% to 90% and accelerating surface runoff and erosion."}
            ],
            "precautions": [
                "Drive rings straight down without rocking; tilting or rocking creates annular voids along the metal wall that cause artificial edge leakage.",
                "Maintain equal water levels in both inner and outer rings at all times to eliminate horizontal hydraulic gradients between rings.",
                "Ensure water used is from the local irrigation source to match natural soil-water chemical and salinity equilibrium.",
                "Never walk within 1.5 meters of the infiltrometer rings during testing to prevent soil compaction and surface disturbance."
            ],
            "limitations": [
                "Double-ring measurements evaluate positive ponding head, whereas sprinkler and rainfall infiltration occur under zero-ponding negative pressure.",
                "Driving steel rings can disturb the topsoil structure and slice through macropores, slightly altering natural root channel pathways.",
                "The Kostiakov model predicts i → 0 as t → ∞, which is physically unrealistic; the modified Kostiakov model adds a constant term (i_b·t).",
                "Spatial soil heterogeneity requires at least three spatial replications per field for representative irrigation design."
            ],
            "quiz": [
                {
                    "question": "What is the primary function of the outer ring in a double-ring infiltrometer?",
                    "options": ["Provide structural balance", "Prevent lateral spreading of water from the inner ring by creating a buffer zone", "Store excess water for refilling", "Measure wind evaporation"],
                    "correct": 1,
                    "explanation": "The outer ring saturates the boundary soil to eliminate horizontal capillary suction, ensuring 1D vertical flow under the inner ring."
                },
                {
                    "question": "In the Kostiakov equation I = c·t^α, if α = 0.65 and t = 100 min with c = 3.5 mm/min^α, what is cumulative infiltration?",
                    "options": ["35.0 mm", "69.8 mm", "125.4 mm", "227.5 mm"],
                    "correct": 1,
                    "explanation": "I = 3.5 × (100)^0.65 = 3.5 × 19.95 = 69.83 mm."
                },
                {
                    "question": "What happens to the infiltration rate of an agricultural soil as time progresses during ponding?",
                    "options": ["It increases linearly", "It starts high and decays asymptotically to a constant basic infiltration rate", "It remains completely constant throughout", "It oscillates sinusoidally"],
                    "correct": 1,
                    "explanation": "Infiltration rate starts high due to strong initial matric suction and decays to a steady-state rate governed by gravity."
                },
                {
                    "question": "Which soil texture typically exhibits the highest basic steady-state infiltration rate?",
                    "options": ["Heavy clay", "Silty clay loam", "Coarse sand", "Dense clay pan"],
                    "correct": 2,
                    "explanation": "Coarse sand possesses large interconnected macropores that allow rapid gravitational water movement."
                }
            ],
            "settings": ["Inner ring diameter: 30.0 cm", "Outer ring diameter: 60.0 cm", "Ponding depth: 5.0 cm"],
            "samples": [10.0, 30.0, 50.0, 70.0, 90.0, 120.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💧", "label": "1. Double-Ring Field Setup"},
                {"id": "compare", "icon": "📊", "label": "2. ln(I) vs ln(t) Plot"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Infiltration Sandbox"}
            ]
        },
        {
            "number": 12,
            "slug": "constant-head-soil-hydraulic-conductivity",
            "title": "Constant-Head Soil Saturated Hydraulic Conductivity (K_sat) Determination",
            "shortTitle": "Saturated Hydraulic Conductivity",
            "aim": "Determine the saturated hydraulic conductivity (K_sat) of agricultural soil cores using a constant-head permeameter and verify Darcy's linear filtration law.",
            "inputLabel": "Hydraulic Head Gradient i = ΔH / L",
            "shortInput": "Gradient i",
            "inputUnit": "m/m",
            "min": 0.5,
            "max": 2.5,
            "step": 0.4,
            "initial": 1.3,
            "inputDecimals": 1,
            "rawLabel": "Darcy Discharge Velocity v",
            "rawUnit": "cm/min",
            "rawDecimals": 4,
            "xAxis": "Hydraulic gradient i = ΔH / L (m/m)",
            "yAxis": "Darcy velocity v (cm/min)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 1.5,
            "emptyY": 0.27,
            "targetName": "Saturated Hydraulic Conductivity K_sat",
            "target": "0.1800",
            "refValue": 0.1800,
            "resultUnit": "cm/min",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "v = K_sat · i = 0.1800 · i",
            "intro": "Saturated hydraulic conductivity (K_sat) is the fundamental quantitative measure of a soil's ability to transmit water when all pore spaces are completely saturated under laminar flow conditions. It serves as the cornerstone parameter for agricultural tile drainage design (Hooghoudt's equation), irrigation scheduling, seepage loss calculations from farm ponds and earthen canals, and solute transport modeling. For coarse-textured soils and undisturbed agricultural topsoils possessing moderate to high permeability, K_sat is determined in accordance with ASTM D2434 and standard soil physics protocols using a constant-head permeameter. In accordance with Darcy's classical law, the specific volumetric discharge rate per unit cross-sectional area (the Darcy flux or apparent velocity v = Q / (A·t)) is directly proportional to the dimensionless hydraulic gradient i = ΔH / L (the hydraulic head loss ΔH across a soil column of length L). The constant of proportionality is K_sat, which depends on soil pore geometry, pore size distribution, fluid density, and dynamic viscosity. In this experiment, de-aired water is passed through undisturbed soil core samples across controlled hydraulic gradients to extract K_sat.",
            "modelExtra": "Evaluated using undisturbed sandy loam soil core (diameter 7.5 cm, length 10.0 cm, dry bulk density 1.45 g/cm³) using de-aired water at 20°C.",
            "apparatus": [
                {"name": "Rigid-Wall Constant-Head Soil Permeameter", "purpose": "Holds 7.5 cm diameter soil core with porous stone plates and adjustable overflow weir."},
                {"name": "Constant-Head Reservoir Tank", "purpose": "Supplies de-aired water at precisely regulated upstream hydraulic head elevation."},
                {"name": "Differential Piezometer Manometer Board", "purpose": "Measures upstream and downstream pressure heads with 1.0 mm water column precision."},
                {"name": "Graduated Volumetric Effluent Cylinder", "purpose": "Collects percolated water over measured time intervals with 0.5 mL accuracy."},
                {"name": "Vacuum De-Airing Water Tank", "purpose": "Removes dissolved gases from permeate water to prevent entrapped air bubbles in soil pores."},
                {"name": "Laboratory Electronic Analytical Balance", "purpose": "Weighs collected effluent to verify volumetric discharge gravimetrically."}
            ],
            "procedure": [
                {"title": "Soil Core Preparation & Saturation", "text": "Trim the ends of the undisturbed soil core flush with the sample cylinder. Place the core in a vacuum saturator and slowly saturate from the bottom upward with de-aired water over 24 hours to eliminate entrapped air."},
                {"title": "Permeameter Cell Assembly", "text": "Assemble the saturated core into the permeameter cell between fine mesh screens and saturated porous stones, tightening tie rods to seal against side-wall bypass leakage."},
                {"title": "Constant-Head Gradient Setup", "text": "Connect the constant-head reservoir to establish an initial hydraulic head loss ΔH = 5.0 cm across the 10.0 cm core (gradient i = 0.50 m/m)."},
                {"title": "Steady Effluent Collection", "text": "Allow water to flow until effluent discharge reaches steady state, then collect water in a graduated cylinder over exactly 5.0 minutes, logging collected volume Q."},
                {"title": "Gradient Stepping", "text": "Increment hydraulic head gradient in four stages up to i = 2.5 m/m (ΔH = 9.0, 13.0, 17.0, 21.0, 25.0 cm), collecting timed effluent for each gradient."},
                {"title": "Darcy Velocity & K_sat Calculation", "text": "Calculate Darcy velocity v = Q / (A·Δt) (cm/min), plot v against hydraulic gradient i, and perform linear regression through the origin to determine K_sat."}
            ],
            "topics": [
                {"question": "State Darcy's law for 1D flow through saturated porous media.", "answer": "Darcy's law states that Q = -K_sat·A·(dh/dl), or v = Q/A = K_sat·i, where Q is volumetric flow rate, A is cross-sectional area, dh/dl = i is hydraulic gradient, and K_sat is saturated hydraulic conductivity."},
                {"question": "Distinguish between Darcy velocity and actual pore water seepage velocity.", "answer": "Darcy velocity v = Q/A is an apparent bulk velocity assuming flow across the entire cross-section. The actual pore seepage velocity v_s = v / n_e (where n_e is effective porosity) is significantly faster because water flows only through interconnected pore channels."},
                {"question": "Why must permeameter water be de-aired prior to testing?", "answer": "Dissolved air in water will come out of solution inside the soil matrix as pressure drops, forming microscopic bubbles that block pore necks, drastically reducing apparent hydraulic conductivity."},
                {"question": "How does water temperature affect measured hydraulic conductivity?", "answer": "Viscosity of water decreases as temperature rises (approximately 2% per °C). Hydraulic conductivity measurements are standardized to 20°C using K_20 = K_T × (μ_T / μ_20)."},
                {"question": "What is the difference between constant-head and falling-head permeameters?", "answer": "Constant-head permeameters maintain a constant water level and are suited for high to moderate permeability soils (sands, loams). Falling-head permeameters measure the rate of water level drop in a standpipe and are used for low-permeability soils (clays)."},
                {"question": "What is side-wall bypass leakage and how is it prevented in rigid-wall permeameters?", "answer": "Water tends to flow preferentially along the smooth interface between the soil core and the permeameter wall rather than through the soil pores; it is prevented by applying bentonite clay paste or expanding silicone seals around the core perimeter."}
            ],
            "precautions": [
                "Always saturate soil cores from bottom to top; top-down saturation traps air pockets in blind pores.",
                "Verify zero side-wall leakage around the core perimeter before recording effluent measurements.",
                "Record water temperature during each trial to apply dynamic viscosity temperature corrections.",
                "Ensure flow velocities remain laminar; avoid excessive hydraulic gradients that cause soil particle piping or wash-out."
            ],
            "limitations": [
                "Rigid-wall cells do not permit confining radial stress, making them susceptible to edge effects in swelling clay soils.",
                "Disturbed laboratory cores destroy natural earthworm macropores and root fissures found in field conditions.",
                "Chemical composition of the permeating water must match field soil solution to prevent clay dispersion or swelling.",
                "Darcy's linear law fails at extremely high gradients where turbulent pore flow and non-linear inertial forces emerge."
            ],
            "quiz": [
                {
                    "question": "If a soil core has a cross-sectional area of 44.2 cm² and discharges 39.8 cm³ in 5 minutes under a gradient of 1.0, what is K_sat?",
                    "options": ["0.018 cm/min", "0.180 cm/min", "1.800 cm/min", "18.00 cm/min"],
                    "correct": 1,
                    "explanation": "Darcy velocity v = 39.8 / (44.2 × 5) = 0.180 cm/min. Under gradient i = 1.0, K_sat = v / i = 0.180 cm/min."
                },
                {
                    "question": "How does actual microscopic pore seepage velocity v_s compare to Darcy velocity v?",
                    "options": ["v_s is identical to v", "v_s is always greater than v (v_s = v / porosity)", "v_s is much smaller than v", "v_s is zero"],
                    "correct": 1,
                    "explanation": "Because soil grains occupy solid volume, water flows only through the open pores, making seepage velocity v_s = v / n_e greater than bulk Darcy flux."
                },
                {
                    "question": "Which agricultural soil type is best suited for constant-head (rather than falling-head) permeameter testing?",
                    "options": ["Dense heavy clay", "Compacted plow pan", "Coarse sand and sandy loam", "Unweathered shale"],
                    "correct": 2,
                    "explanation": "Coarse sand and sandy loam have high permeability that produces measurable steady effluent volumes under constant head."
                },
                {
                    "question": "What is the standard reference temperature for reporting saturated hydraulic conductivity?",
                    "options": ["0°C", "4°C", "20°C", "100°C"],
                    "correct": 2,
                    "explanation": "Hydraulic conductivity is standardized to 20°C to eliminate fluid viscosity variations."
                }
            ],
            "settings": ["Core diameter: 7.50 cm", "Core length: 10.0 cm", "Water temperature: 20.0°C"],
            "samples": [0.5, 0.9, 1.3, 1.7, 2.1, 2.5],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💧", "label": "1. Permeameter Column"},
                {"id": "compare", "icon": "📊", "label": "2. Darcy Flux vs Gradient"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Hydraulic Head Sandbox"}
            ]
        },
        {
            "number": 13,
            "slug": "soil-moisture-retention-pf-curve",
            "title": "Soil Moisture Retention Characteristic (pF Curves) & Pressure Plate Extraction",
            "shortTitle": "Soil Moisture Retention pF",
            "aim": "Determine the soil water retention curve (pF curve) of an agricultural loam using a porous ceramic pressure plate extractor across varying matric suctions.",
            "inputLabel": "Logarithm of Matric Suction ln(ψ)",
            "shortInput": "ln(Suction ψ)",
            "inputUnit": "ln(kPa)",
            "min": 1.0,
            "max": 4.0,
            "step": 0.6,
            "initial": 2.2,
            "inputDecimals": 2,
            "rawLabel": "Volumetric Water Content θ",
            "rawUnit": "m³/m³",
            "rawDecimals": 4,
            "xAxis": "ln(Matric suction ψ in kPa)",
            "yAxis": "Volumetric water content θ (m³/m³)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 2.5,
            "emptyY": 0.3175,
            "targetName": "Retention Curve Slope λ_ret",
            "target": "0.0650",
            "refValue": 0.0650,
            "resultUnit": "m³/m³",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "θ = -λ_ret · ln(ψ) + θ_0 = -0.0650 · ln(ψ) + 0.4800",
            "intro": "The soil water retention characteristic curve (also termed the soil water characteristic curve, or pF curve) describes the thermodynamic relationship between matric suction (energy potential with which water is held by soil capillary and adsorptive forces) and volumetric water content θ. It is the defining constitutive property used to evaluate Field Capacity (FC, typically -33 kPa or pF 2.54), Permanent Wilting Point (PWP, -1500 kPa or pF 4.18), and Available Water Capacity (AWC = FC - PWP) for irrigation water management. Saturated porous ceramic plates inside sealed pressure chambers allow positive pneumatic air pressure to be applied to soil cores resting on water-saturated ceramic discs. The applied air pressure forces water out through microscopic ceramic pores into an atmospheric drain until matric potential inside the soil exactly balances the applied pneumatic chamber pressure. In the intermediate desaturation zone between air-entry suction and permanent wilting, the retention curve follows a linear semi-logarithmic relationship θ = -λ_ret·ln(ψ) + θ_0 in accordance with the Brooks-Corey model.",
            "modelExtra": "Evaluated using silt loam soil cores (dry bulk density 1.35 g/cm³, porosity 0.48 m³/m³) placed in a 15-bar pressure plate extractor.",
            "apparatus": [
                {"name": "15-Bar High-Pressure Ceramic Plate Extractor", "purpose": "Applies regulated pneumatic pressure from 10 to 1500 kPa across soil retaining rings."},
                {"name": "Saturated High-Flow Ceramic Porous Plate", "purpose": "Allows liquid water passage while preventing air breakthrough up to its rated bubble pressure."},
                {"name": "Precision Pressure Regulators & Manometers", "purpose": "Maintains constant chamber air pressure with 0.5 kPa accuracy."},
                {"name": "Undisturbed Soil Retaining Core Rings", "purpose": "Confines soil cores (5.0 cm diameter, 1.0 cm height) on the ceramic plate surface."},
                {"name": "Forced-Draft Drying Oven (105°C)", "purpose": "Dries soil samples to constant weight after pressure equilibration."},
                {"name": "High-Precision Analytical Balance (0.001 g)", "purpose": "Measures soil core wet mass at each equilibrium suction stage."}
            ],
            "procedure": [
                {"title": "Ceramic Plate Pre-Saturation", "text": "Submerge the porous ceramic plate in de-aired water for 24 hours to ensure 100% saturation of all ceramic microscopic pores, verifying zero air entry."},
                {"title": "Soil Core Loading & Saturation", "text": "Place soil sample rings onto the plate, add water to the plate surface, and allow soil cores to saturate by capillarity from the bottom for 18 hours."},
                {"title": "Initial Suction Chamber Seal", "text": "Transfer the loaded plate into the pressure vessel, connect the effluent drain tube, seal the chamber lid, and apply initial pneumatic pressure P = 2.7 kPa (ln ψ = 1.0)."},
                {"title": "Hydraulic Equilibrium Attainment", "text": "Maintain pressure until outflow from the drain tube ceases completely (typically 24 to 48 hours), confirming thermodynamic equilibrium between soil water and air pressure."},
                {"title": "Sample Extraction & Weighing", "text": "Quickly depressurize the chamber, extract replicate soil rings, record wet mass, and oven-dry at 105°C for 24 hours to calculate volumetric water content θ."},
                {"title": "Multi-Pressure Retention Curve", "text": "Repeat testing across suctions corresponding to ln ψ = 1.6, 2.2, 2.8, 3.4, and 4.0 (up to 54.6 kPa in the ceramic extractor), plotting θ versus ln ψ to evaluate λ_ret."}
            ],
            "topics": [
                {"question": "Define Field Capacity (FC) and Permanent Wilting Point (PWP).", "answer": "Field Capacity is the volumetric water content retained in soil after rapid gravitational drainage has ceased (typically at matric suction of -10 to -33 kPa). Permanent Wilting Point is the soil moisture content at -1500 kPa suction where plant roots can no longer extract water, causing permanent wilting."},
                {"question": "What is the pF scale for expressing soil matric suction?", "answer": "The pF scale, introduced by Schofield, is the common logarithm of matric suction expressed in centimeters of water column head: pF = log10(h_cm). For example, 1000 cm head (~100 kPa) corresponds to pF 3.0."},
                {"question": "How does soil texture influence the shape of the pF curve?", "answer": "Sandy soils have large uniform macropores that drain rapidly at low suction, producing a steep drop in water content. Clay soils have tiny micropores and high surface area, retaining significant water even at very high suction with a gentle, flatter retention curve."},
                {"question": "What is Available Water Capacity (AWC)?", "answer": "Available Water Capacity is the total volume of water held in the crop root zone between Field Capacity and Permanent Wilting Point (AWC = θ_FC - θ_PWP), representing the soil water reservoir available for crop transpiration."},
                {"question": "Why does soil water retention exhibit hysteresis during wetting versus drying?", "answer": "Hysteresis (different moisture contents at the same suction during wetting vs drying) is caused by the 'ink-bottle' pore neck effect, trapped air during wetting, contact angle differences during advancing vs receding water menisci, and clay swelling/shrinkage."},
                {"question": "What is the air-entry value (bubbling pressure) of a porous ceramic plate?", "answer": "The air-entry value is the critical pneumatic pressure at which air can force water out of the largest pores of the ceramic plate and break through. Ceramic plates must operate below their air-entry rating to maintain a continuous water bridge."}
            ],
            "precautions": [
                "Ensure ceramic plates are fully saturated before placing soil cores; dry spots prevent capillary drainage.",
                "Verify that the outflow drain tube remains submerged in a water vial to prevent air back-diffusion into the drain line.",
                "Depressurize and clamp drain tubes immediately when stopping the test to prevent back-absorption of water into the soil cores.",
                "Maintain constant laboratory temperature to avoid thermal expansion and evaporation errors during multi-day equilibration."
            ],
            "limitations": [
                "Pressure plate extraction requires several days to reach true hydraulic equilibrium at high suctions.",
                "Hysteresis is not captured when testing only the primary desorption (drying) branch.",
                "Pneumatic pressure in the laboratory simulates matric suction but does not reproduce natural mechanical overburden stress present in deep subsoils.",
                "Solute concentration differences in soil water can induce secondary osmotic potentials not measured by ceramic plates."
            ],
            "quiz": [
                {
                    "question": "What matric suction is conventionally accepted as the Permanent Wilting Point (PWP) for agricultural crops?",
                    "options": ["-10 kPa", "-33 kPa", "-100 kPa", "-1500 kPa (15 bar)"],
                    "correct": 3,
                    "explanation": "Permanent Wilting Point is universally defined at -1500 kPa (-15 bar) matric suction."
                },
                {
                    "question": "If a soil has a field capacity of 0.32 m³/m³ and a wilting point of 0.14 m³/m³, what is its Available Water Capacity?",
                    "options": ["0.14 m³/m³", "0.18 m³/m³", "0.32 m³/m³", "0.46 m³/m³"],
                    "correct": 1,
                    "explanation": "AWC = θ_FC - θ_PWP = 0.32 - 0.14 = 0.18 m³/m³."
                },
                {
                    "question": "On the Schofield pF scale, what suction does pF 2.0 represent?",
                    "options": ["2 cm water head", "20 cm water head", "100 cm water head", "1000 cm water head"],
                    "correct": 2,
                    "explanation": "pF = log10(h_cm); therefore, pF 2.0 corresponds to 10² = 100 cm of water head (approx. 10 kPa)."
                },
                {
                    "question": "Why does a clay soil hold more water at permanent wilting point than a sandy soil?",
                    "options": ["Clay has large air macropores", "Clay has enormous specific surface area and microscopic pores that hold water tightly", "Clay has zero internal friction", "Clay contains organic matter only"],
                    "correct": 1,
                    "explanation": "Clay particles have massive specific surface areas with sub-micron pores that bind water tightly by adsorptive and capillary forces."
                }
            ],
            "settings": ["Soil texture: Silt loam (porosity 0.48)", "Ceramic plate: 15-bar rated", "Test mode: Primary desorption"],
            "samples": [1.0, 1.6, 2.2, 2.8, 3.4, 4.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💧", "label": "1. Pressure Plate Extractor"},
                {"id": "compare", "icon": "📊", "label": "2. Retention pF Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Matric Suction Sandbox"}
            ]
        },
        {
            "number": 14,
            "slug": "parshall-flume-open-channel-flow-measurement",
            "title": "Parshall Flume Open-Channel Flow Discharge Calibration & Submergence",
            "shortTitle": "Parshall Flume Calibration",
            "aim": "Calibrate a standard Parshall flume in an open irrigation channel, determine the free-flow power-law discharge rating equation, and evaluate the critical submergence limit.",
            "inputLabel": "Logarithm of Upstream Gauge Head ln(H_a)",
            "shortInput": "ln(Head H_a)",
            "inputUnit": "ln(m)",
            "min": -2.9957,
            "max": -0.9163,
            "step": 0.4158,
            "initial": -1.7429,
            "inputDecimals": 4,
            "rawLabel": "Logarithm of Discharge ln(Q)",
            "rawUnit": "ln(m³/s)",
            "rawDecimals": 4,
            "xAxis": "ln(Upstream head H_a in m)",
            "yAxis": "ln(Discharge Q in m³/s)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": -1.8,
            "emptyY": -2.41,
            "targetName": "Parshall Flume Exponent n",
            "target": "1.5500",
            "refValue": 1.5500,
            "resultUnit": "dimensionless",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ln(Q) = n · ln(H_a) + ln(C) = 1.5500 · ln(H_a) + 0.3800",
            "intro": "Accurate measurement of open-channel water discharge is essential for fair water allocation in irrigation districts, monitoring canal conveyance efficiency, and preventing canal bank overtopping. The Parshall flume, developed by Ralph L. Parshall, is a specialized self-cleaning Venturi-type open channel constriction widely recognized as the international standard for irrigation flow measurement. It features a converging contracting entrance section with a level floor, a contracted throat section with a downward-sloping floor, and a diverging expanding exit section with an upward-sloping floor. The drop in throat elevation induces critical depth and supercritical flow, establishing a unique relationship between the upstream water depth H_a (measured in a stilling well at two-thirds the length of the converging section) and discharge Q. In free-flow conditions, the rating equation follows a power law Q = C·H_a^n (or ln Q = n·ln H_a + ln C). When downstream tailwater rises such that the submergence ratio S = H_b / H_a exceeds the critical limit (0.60 for small flumes, 0.70 for medium flumes), flow transitions to submerged flow requiring a submergence correction. In this experiment, a calibrated flume is tested across multiple flow rates to extract n and C.",
            "modelExtra": "Evaluated using a standard 6-inch (15.2 cm) throat width Parshall flume in free-flow regime across upstream heads from 0.05 m to 0.40 m.",
            "apparatus": [
                {"name": "Standard 6-Inch Throat Parshall Flume", "purpose": "Precision fabricated stainless steel flume with standardized converging, throat, and diverging sections."},
                {"name": "Hydraulic Tilting Open-Channel Flume", "purpose": "Laboratory flume canal 60 cm wide and 10 m long with recirculating water pump and tailwater gate."},
                {"name": "Dual Point-Gauge Stilling Wells (H_a & H_b)", "purpose": "Measures upstream water depth H_a and throat depth H_b with 0.1 mm accuracy."},
                {"name": "Magnetic Flowmeter Reference Sensor", "purpose": "Supplies independent benchmark volumetric discharge rate Q with 0.5% precision."},
                {"name": "Adjustable Downstream Tailwater Weir", "purpose": "Modulates downstream water level to test free-flow versus submerged-flow regimes."},
                {"name": "Digital Differential Pressure Transmitter", "purpose": "Continuously records water surface elevation heads in the stilling wells."}
            ],
            "procedure": [
                {"title": "Flume Leveling & Zero Setting", "text": "Level the Parshall flume longitudinally and laterally in the channel. Set the stilling well point gauges to exactly zero against the flat crest of the flume converging floor."},
                {"title": "Free-Flow Calibration Setup", "text": "Lower the downstream tailwater gate completely to ensure free-fall discharge, ensuring the submergence ratio H_b / H_a remains well below 0.60."},
                {"title": "Initial Low-Flow Stabilization", "text": "Regulate pump throttle to deliver initial low discharge producing an upstream head H_a = 0.05 m (ln H_a = -2.9957), allowing water levels in the stilling wells to stabilize."},
                {"title": "Synchronous Discharge Logging", "text": "Record the upstream head H_a from the stilling well and the reference discharge Q from the magnetic flowmeter simultaneously over 3 minutes."},
                {"title": "Head Range Stepping", "text": "Increment pump discharge in five uniform stages to achieve upstream heads of 0.08, 0.12, 0.18, 0.27, and 0.40 m, recording H_a and Q for each flow rate."},
                {"title": "Power-Law Logarithmic Regression", "text": "Transform H_a and Q into natural logarithms, plot ln Q versus ln H_a, and perform linear regression to determine the exponent n and coefficient C."}
            ],
            "topics": [
                {"question": "What are the primary operational advantages of a Parshall flume over a sharp-crested weir?", "answer": "Parshall flumes have low head loss (about one-fourth that of a weir), high velocity through the throat that makes them self-cleaning (preventing sediment and debris accumulation), and the ability to operate under substantial submergence without losing calibration."},
                {"question": "Explain the difference between free flow and submerged flow in a Parshall flume.", "answer": "In free flow, critical velocity occurs in the throat, creating a hydraulic drop such that downstream tailwater has zero effect on the upstream head H_a (discharge depends solely on H_a). In submerged flow, high tailwater submerges the throat, causing backwater that elevates H_a and requires both H_a and H_b to compute discharge."},
                {"question": "What is the critical submergence ratio for a 6-inch Parshall flume?", "answer": "For throat widths between 6 inches and 9 inches, the critical submergence limit is S_c = H_b / H_a = 0.60 (60%). Below 60%, free-flow equations apply; above 60%, a submergence correction must be subtracted."},
                {"question": "Where is the upstream head measurement location H_a located?", "answer": "H_a is measured in a stilling well connected to a tap located on the side wall of the converging section at a distance equal to two-thirds of the converging section length upstream from the throat crest."},
                {"question": "How does sediment deposition in the approach canal affect flume accuracy?", "answer": "Sediment deposition upstream can distort the approach velocity profile and create excessive approach velocity, causing the flume to under-read discharge relative to standard calibration tables."},
                {"question": "Why is the throat floor of a Parshall flume sloped downward?", "answer": "The downward slope of the throat (slope 3:8) accelerates water rapidly through critical depth into supercritical flow, ensuring a stable, well-defined free-flow rating relation."}
            ],
            "precautions": [
                "Verify that the flume crest floor is perfectly level across both lateral and longitudinal directions using a precision spirit level.",
                "Ensure stilling well piezometer tubes are free of trapped air bubbles and sediment silt.",
                "Maintain approach flow conditions smooth and symmetrical without surface waves or cross-currents.",
                "Check that the flume operates under free-flow conditions (H_b / H_a < 0.60) during calibration runs."
            ],
            "limitations": [
                "Flumes must be fabricated strictly to standardized ASTM/USBR dimensions; geometric scaling errors invalidate published discharge coefficients.",
                "At very low heads (H_a < 0.03 m), surface tension and boundary layer viscosity distort the power-law exponent.",
                "Submerged flow corrections introduce higher measurement uncertainty (±5%) compared to free-flow calibration (±2%).",
                "High approach velocities (> 0.5 m/s) require baffle straighteners to prevent kinetic energy head distortion."
            ],
            "quiz": [
                {
                    "question": "What physical phenomenon occurs in the throat of a Parshall flume under free-flow conditions?",
                    "options": ["Complete stagnation", "Flow passes through critical depth (Froude number = 1.0)", "Cavitation bubbles", "Reverse hydraulic vortex"],
                    "correct": 1,
                    "explanation": "Critical flow occurs in the contracted throat, decoupling upstream water depth from downstream tailwater fluctuations."
                },
                {
                    "question": "For a flume with rating equation Q = 1.462 · H_a^1.55 (in m³/s), what is the discharge when H_a = 0.20 m?",
                    "options": ["0.012 m³/s", "0.052 m³/s", "0.122 m³/s", "0.292 m³/s"],
                    "correct": 1,
                    "explanation": "Q = 1.462 × (0.20)^1.55 = 1.462 × 0.0357 = 0.0522 m³/s (approx. 52.2 L/s)."
                },
                {
                    "question": "Why is a Parshall flume considered 'self-cleaning' in agricultural irrigation canals?",
                    "options": ["It uses ultrasonic transducer waves", "High velocity and bottom slope in the throat flush silt and sand through without settling", "It features an internal rotary brush", "Chemical dispersants are added"],
                    "correct": 1,
                    "explanation": "The contracting walls and sloped throat accelerate water velocity, scouring sediment through and preventing silt accumulation."
                },
                {
                    "question": "If upstream head H_a = 0.30 m and downstream throat head H_b = 0.24 m, what is the submergence ratio?",
                    "options": ["0.55", "0.70", "0.80", "1.25"],
                    "correct": 2,
                    "explanation": "Submergence ratio S = H_b / H_a = 0.24 / 0.30 = 0.80 (80%), indicating submerged flow."
                }
            ],
            "settings": ["Flume throat width W: 6 inches (15.24 cm)", "Regime: Free flow (H_b/H_a < 0.60)", "Channel width: 60.0 cm"],
            "samples": [-2.9957, -2.5257, -2.1203, -1.7148, -1.3093, -0.9163],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💧", "label": "1. Parshall Flume Channel"},
                {"id": "compare", "icon": "📊", "label": "2. ln(Q) vs ln(H_a) Rating"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Submergence Sandbox"}
            ]
        },
        {
            "number": 15,
            "slug": "v-notch-sharp-crested-weir-discharge",
            "title": "90° V-Notch Sharp-Crested Weir Flow Rate & Discharge Coefficient (C_d)",
            "shortTitle": "V-Notch Weir Calibration",
            "aim": "Calibrate a 90° V-notch sharp-crested weir in an open irrigation flume and evaluate the weir discharge coefficient C_d and proportionality constant C_w.",
            "inputLabel": "Head Raised to 2.5 Power H^2.5",
            "shortInput": "H^2.5",
            "inputUnit": "m^2.5",
            "min": 0.005,
            "max": 0.045,
            "step": 0.008,
            "initial": 0.021,
            "inputDecimals": 4,
            "rawLabel": "Measured Weir Discharge Q",
            "rawUnit": "m³/s",
            "rawDecimals": 5,
            "xAxis": "Head raised to 2.5 power H^2.5 (m^2.5)",
            "yAxis": "Discharge Q (m³/s)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 0.025,
            "emptyY": 0.0345,
            "targetName": "Thomson Weir Discharge Coefficient C_w",
            "target": "1.3800",
            "refValue": 1.3800,
            "resultUnit": "m^0.5/s",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "Q = C_w · H^2.5 = 1.3800 · H^2.5",
            "intro": "Sharp-crested weirs are among the oldest and most precise primary devices used to measure water flow in small agricultural irrigation canals, spring catchments, furrow runoff channels, and drainage ditches. The 90° triangular (V-notch or Thomson) weir is especially suited for low and variable flow rates because the flow cross-section expands triangularly with water depth, maintaining high sensitivity and measurable head even during minimal trickles. Flow over a sharp-crested V-notch weir is governed by integration of the Torricelli velocity profile across triangular horizontal slices: Q = (8/15)·C_d·√(2g)·tan(θ/2)·H^(5/2). For a standard 90° notch (θ = 90°, tan(θ/2) = 1) with clean, fully aerated nappe, this simplifies to the Thomson rating formula Q = C_w·H^2.5, where C_w = (8/15)·C_d·√(2g) ≈ 1.38 m^0.5/s for an empirical discharge coefficient C_d ≈ 0.585. To ensure accurate measurement without end contractions, the weir plate must be chamfered with a sharp bevel facing downstream, and the upstream head H must be measured at least four times the maximum head upstream to avoid surface drawdown curvature.",
            "modelExtra": "Evaluated using a precision brass 90° V-notch plate mounted in a rectangular flume across water heads from 0.12 m to 0.28 m (H^2.5 from 0.005 to 0.045 m^2.5).",
            "apparatus": [
                {"name": "90° Triangular Sharp-Crested Weir Plate", "purpose": "Precision milled brass plate with 90° notch angle and 45° downstream beveled knife edge."},
                {"name": "Hydraulic Open-Channel Laboratory Flume", "purpose": "Recirculating water flume with wave-damping baffles and upstream calming section."},
                {"name": "Vernier Point Gauge with Micrometer", "purpose": "Measures upstream water surface elevation H with 0.1 mm precision."},
                {"name": "Primary Volumetric Gravimetric Tank", "purpose": "Captures discharged water over timed intervals to determine true benchmark flow rate Q."},
                {"name": "Nappe Aeration Vent Pipes", "purpose": "Supplies ambient air beneath the falling nappe to prevent vacuum cling and calibration distortion."},
                {"name": "Electromagnetic Reference Flow Meter", "purpose": "Monitors flume inflow rate continuously for flow stability verification."}
            ],
            "procedure": [
                {"title": "Weir Zero Datum Setting", "text": "Fill the flume until water is exactly level with the vertex of the V-notch. Lower the vernier point gauge until its tip touches the meniscus at the notch vertex and record the zero datum reading H_0."},
                {"title": "Calming Screen Alignment", "text": "Place mesh calming baffles 3.0 meters upstream of the weir to dissipate surface waves and establish uniform approach velocity."},
                {"title": "Initial Flow Stabilization", "text": "Start the supply pump to establish an upstream head H = 0.120 m (H^2.5 = 0.0050 m^2.5), verifying that the nappe springs clear of the crest and is fully aerated."},
                {"title": "Timed Volumetric Collection", "text": "Divert the weir discharge into the gravimetric weigh tank for exactly 60.0 seconds, measuring collected mass to calculate volumetric flow rate Q (m³/s)."},
                {"title": "Head Incrementation", "text": "Systematically increase pump flow across five additional stages up to H = 0.280 m (H^2.5 = 0.0450 m^2.5), logging H and Q for each trial."},
                {"title": "Weir Coefficient Regression", "text": "Plot measured discharge Q against H^2.5, perform linear regression through the origin, and determine the Thomson weir discharge coefficient C_w and C_d."}
            ],
            "topics": [
                {"question": "Derive the theoretical discharge equation for a triangular sharp-crested weir.", "answer": "Consider an elemental strip of thickness dh at depth h below water surface: width b = 2·(H - h)·tan(θ/2). Elemental discharge dQ = C_d·b·dh·√(2gh). Integrating from h = 0 to h = H yields Q = (8/15)·C_d·√(2g)·tan(θ/2)·H^(5/2)."},
                {"question": "Why is a V-notch weir superior to a rectangular weir for measuring low agricultural discharges?", "answer": "At low flow rates, a rectangular weir spreads water thinly across its crest, resulting in very small heads (H < 2 cm) that are difficult to measure accurately. In contrast, a V-notch concentrates low flows into the apex, maintaining large measurable heads and high precision."},
                {"question": "What is 'nappe cling' and why must the nappe be aerated?", "answer": "If air beneath the falling water sheet (nappe) is evacuated by flowing water, a partial vacuum develops behind the weir plate, sucking the nappe downward and clinging it to the weir face, which artificially increases discharge by up to 10%."},
                {"question": "Where should the point gauge be located to measure true weir head H?", "answer": "The point gauge must be positioned at a distance equal to 4 to 5 times the maximum expected head upstream from the weir plate to avoid the drawdown curve where the water surface dips as it accelerates toward the crest."},
                {"question": "What is the physical meaning of the discharge coefficient C_d in a weir?", "answer": "C_d accounts for two non-ideal effects: (1) contraction of the flow stream as water streamlines curve inward around the sharp edges (vena contracta), and (2) friction and energy dissipation along the weir plate."},
                {"question": "What maintenance is required for field V-notch weirs?", "answer": "Regular removal of accumulated sediment silt upstream of the weir plate, clearing floating debris and leaves caught in the notch, and inspecting the metal knife edge for nicks or algae growth."}
            ],
            "precautions": [
                "Verify that the weir plate knife-edge bevel faces downstream, presenting a sharp 90° square edge to the oncoming flow.",
                "Ensure point gauge tip is lowered smoothly to touch the water surface without puncturing the surface tension meniscus.",
                "Verify atmospheric air access ports beneath the nappe remain completely unobstructed during all runs.",
                "Allow at least 3 minutes after adjusting pump throttle for flume wave oscillations to dissipate."
            ],
            "limitations": [
                "The 5/2 power law applies strictly for heads H > 0.05 m; below 5 cm, water surface tension and fluid viscosity dominate.",
                "Assumes negligible approach velocity; in narrow channels, approach velocity kinetic head (v²/2g) must be added to H.",
                "Cannot tolerate downstream submergence; the downstream water level must remain below the vertex of the V-notch.",
                "Sediment accumulation upstream alters approach geometry and gradually degrades measurement accuracy."
            ],
            "quiz": [
                {
                    "question": "What is the theoretical head exponent in the discharge equation for a triangular V-notch weir?",
                    "options": ["1.0", "1.5 (3/2)", "2.0", "2.5 (5/2)"],
                    "correct": 3,
                    "explanation": "Integrating the triangular area elements with the Torricelli velocity profile yields an exponent of 5/2 (2.5)."
                },
                {
                    "question": "If head H over a 90° V-notch weir is 0.20 m and C_w = 1.38 m^0.5/s, what is the discharge Q?",
                    "options": ["0.0075 m³/s", "0.0247 m³/s", "0.0552 m³/s", "0.1380 m³/s"],
                    "correct": 1,
                    "explanation": "Q = 1.38 × (0.20)^2.5 = 1.38 × 0.01789 = 0.02469 m³/s (approx. 24.7 L/s)."
                },
                {
                    "question": "What happens if the nappe behind a sharp-crested weir becomes de-aerated (vacuum forms)?",
                    "options": ["Discharge stops entirely", "Measured discharge increases above calibrated rating due to suction", "The weir plate collapses upstream", "Water turns into steam"],
                    "correct": 1,
                    "explanation": "A partial vacuum beneath the nappe draws water downward, increasing effective head and causing the weir to discharge more water than calibrated."
                },
                {
                    "question": "What is the standard angle for the most common triangular sharp-crested weir?",
                    "options": ["30°", "45°", "60°", "90°"],
                    "correct": 3,
                    "explanation": "The 90° V-notch (Thomson weir) is the universal standard for small open-channel flow measurement."
                }
            ],
            "settings": ["Weir notch angle θ: 90°", "Weir plate: Sharp-crested brass with 45° bevel", "Flume width: 60.0 cm"],
            "samples": [0.005, 0.013, 0.021, 0.029, 0.037, 0.045],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💧", "label": "1. V-Notch Weir Flume"},
                {"id": "compare", "icon": "📊", "label": "2. Q vs H^2.5 Linear Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Notch Head Sandbox"}
            ]
        },
        {
            "number": 16,
            "slug": "centrifugal-irrigation-pump-characteristic-curves",
            "title": "Agricultural Centrifugal Irrigation Pump Characteristic Performance Curves (H-Q, η)",
            "shortTitle": "Centrifugal Pump Curves",
            "aim": "Determine the head-discharge (H-Q), brake power, and overall efficiency characteristic curves of an agricultural centrifugal pump and verify affinity affinity laws across speeds.",
            "inputLabel": "Normalized Pump Speed Squared (N / 1000)²",
            "shortInput": "(N/1000)²",
            "inputUnit": "(k-rpm)²",
            "min": 1.0,
            "max": 5.76,
            "step": 0.952,
            "initial": 2.56,
            "inputDecimals": 2,
            "rawLabel": "Shutoff Total Dynamic Head H_0",
            "rawUnit": "m",
            "rawDecimals": 2,
            "xAxis": "Normalized speed squared (N/1000)²",
            "yAxis": "Shutoff head H_0 (m)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.0,
            "emptyY": 24.6,
            "targetName": "Pump Head Affinity Constant k_N",
            "target": "8.2000",
            "refValue": 8.2000,
            "resultUnit": "m/(k-rpm)²",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "H_0 = k_N · (N / 1000)² = 8.2000 · (N / 1000)²",
            "intro": "Centrifugal pumps are the workhorses of agricultural water management, lifting water from tube-wells, rivers, and canals to pressurized sprinkler networks, drip irrigation lines, and surface distribution ditches. Inside the volute casing, an enclosed backward-curved impeller rotates at high speed, imparting kinetic kinetic energy to the fluid before diffusing it into static pressure head. Pump performance is dictated by its characteristic curves: Total Dynamic Head versus Discharge (H-Q curve), Brake Power versus Discharge (P-Q curve), and Efficiency versus Discharge (η-Q curve). Operating near the Best Efficiency Point (BEP) minimizes electric energy or diesel fuel consumption per cubic meter of pumped water. In accordance with centrifugal affinity laws, pump capacity scales linearly with rotational speed (Q ∝ N), total head scales with speed squared (H ∝ N²), and brake power scales with speed cubed (P ∝ N³). Evaluating the shutoff head H_0 (head at zero discharge) as a function of speed squared (N/1000)² provides a direct empirical verification of Euler's turbomachinery head equation H_0 = u₂² / g. In this test, an instrumented centrifugal test bench calibrates pump affinity scaling.",
            "modelExtra": "Evaluated using a single-stage end-suction centrifugal pump (impeller diameter D = 160 mm) pumping clean water across speeds from 1000 to 2400 RPM.",
            "apparatus": [
                {"name": "Agricultural Centrifugal Pump Test Station", "purpose": "Single-stage end-suction volute pump with transparent acrylic suction and discharge sections."},
                {"name": "Variable-Frequency Three-Phase Electric Motor", "purpose": "Regulates pump rotational speed from 1000 to 2400 RPM with 1.0 RPM digital control."},
                {"name": "Suction Vacuum Gauge & Discharge Pressure Transducer", "purpose": "Measures suction head h_s (-kPa) and discharge head h_d (kPa) to calculate total dynamic head."},
                {"name": "Electromagnetic Flowmeter & Throttle Gate Valve", "purpose": "Measures discharge Q (L/s) while the downstream throttle valve regulates operating point."},
                {"name": "In-Line Shaft Reaction Torquemeter & Optical Tachometer", "purpose": "Measures pump input shaft torque and rotational speed for brake horsepower calculation."},
                {"name": "Digital Hydraulic Telemetry Console", "purpose": "Logs pressures, flow, torque, power, and computes real-time pump efficiency η."}
            ],
            "procedure": [
                {"title": "Pump Priming & Sensor Zeroing", "text": "Fill the suction line and pump volute casing with water, bleeding all air through the top vent valve until no bubbles emerge. Zero all pressure transducers at static equilibrium."},
                {"title": "Initial Speed Setting", "text": "Set variable-frequency motor drive to N = 1000 RPM ((N/1000)² = 1.00), leaving the discharge throttle valve fully closed to establish the shutoff point."},
                {"title": "Shutoff Head Measurement", "text": "Record suction vacuum and discharge gauge pressure at zero flow (Q = 0) and compute total shutoff dynamic head H_0 = (P_d - P_s)/(ρ·g) + Δz."},
                {"title": "H-Q Characteristic Curve Run", "text": "At 1750 RPM, systematically open the discharge valve in eight increments from shutoff (Q = 0) to maximum discharge, recording H, Q, shaft power P, and efficiency η."},
                {"title": "Speed Affinity Stepping", "text": "Return throttle valve to shutoff and increment pump speed across five additional stages: 1300, 1600, 1900, 2200, and 2400 RPM, recording H_0 for each speed."},
                {"title": "Affinity Scaling Regression", "text": "Plot shutoff head H_0 against normalized speed squared (N/1000)², perform linear regression through the origin, and determine affinity constant k_N."}
            ],
            "topics": [
                {"question": "State Euler's turbomachinery head equation for a centrifugal pump.", "answer": "Euler's equation is H_ideal = (u₂·v_u2 - u₁·v_u1) / g, where u is peripheral blade velocity and v_u is tangential fluid velocity. Assuming radial inlet flow (v_u1 = 0), H_ideal = u₂·v_u2 / g."},
                {"question": "State the three centrifugal pump affinity laws.", "answer": "The affinity laws state that for a given pump: (1) Discharge Q is directly proportional to speed N (Q₁/Q₂ = N₁/N₂); (2) Head H is proportional to speed squared (H₁/H₂ = (N₁/N₂)²); (3) Brake power P is proportional to speed cubed (P₁/P₂ = (N₁/N₂)³)."},
                {"question": "What is Total Dynamic Head (TDH)?", "answer": "Total Dynamic Head is the total energy imparted to water by the pump, calculated as TDH = (P_d - P_s)/(ρ·g) + (V_d² - V_s²)/(2g) + Δz, where P is pressure, V is velocity, and Δz is the vertical distance between measurement gauges."},
                {"question": "What is Net Positive Suction Head (NPSH) and why is it critical?", "answer": "NPSH is the absolute pressure head at the suction port above the fluid vapor pressure: NPSH = (P_s - P_v)/(ρ·g) + V_s²/(2g). If available NPSH (NPSHA) falls below required NPSH (NPSHR), cavitation occurs, causing severe blade erosion, noise, and loss of prime."},
                {"question": "Why do centrifugal pump impellers use backward-curved blades?", "answer": "Backward-curved blades (blade angle β₂ < 90°) produce a stable, drooping H-Q characteristic curve where head decreases as flow increases, preventing motor overload at high discharge and providing smooth, self-governing operation."},
                {"question": "What is the Best Efficiency Point (BEP)?", "answer": "BEP is the unique operating flow rate and head where hydraulic friction, shock losses, and mechanical losses reach a combined minimum, yielding the peak overall wire-to-water efficiency."}
            ],
            "precautions": [
                "Never run a centrifugal pump dry; mechanical seals and shaft bushings overheat and fail within seconds without lubricating water.",
                "Do not operate at shutoff head (valve fully closed) for more than 1 minute to prevent water boiling inside the volute casing.",
                "Ensure suction lift does not exceed 6.0 meters to prevent acoustic cavitation and impeller pitting.",
                "Verify correct direction of motor rotation (clockwise viewed from driver end for most standard volutes) before coupling."
            ],
            "limitations": [
                "Affinity laws assume identical internal fluid streamlines and neglect Reynolds number viscosity changes at low speeds.",
                "Pump efficiency drops slightly at reduced speeds because mechanical seal friction forms a larger percentage of total power.",
                "Evaluates clear cold water; pumping sandy irrigation water increases wear and decreases head output over time.",
                "Air ingestion through worn suction pipe joints causes immediate surging and loss of prime."
            ],
            "quiz": [
                {
                    "question": "If a centrifugal pump running at 1200 RPM delivers a head of 10 m, what head will it deliver at 2400 RPM according to affinity laws?",
                    "options": ["10 m", "20 m", "40 m", "80 m"],
                    "correct": 2,
                    "explanation": "Because H ∝ N², doubling the speed (from 1200 to 2400 RPM) increases head by a factor of 2² = 4; hence, 10 m × 4 = 40 m."
                },
                {
                    "question": "What destructive physical phenomenon occurs when absolute pressure in the pump suction drops below water vapor pressure?",
                    "options": ["Water hammer", "Cavitation", "Reverse siphon", "Viscous fingering"],
                    "correct": 1,
                    "explanation": "Cavitation occurs when water vaporizes into bubbles that violently collapse against the impeller, causing shock waves and pitting."
                },
                {
                    "question": "If pump shaft torque is 25 N·m at 1750 RPM (183.26 rad/s) and hydraulic power is 3.5 kW, what is the pump efficiency?",
                    "options": ["35.0%", "50.0%", "76.4%", "92.0%"],
                    "correct": 2,
                    "explanation": "Shaft power P_shaft = T × ω = 25 N·m × 183.26 rad/s = 4.58 kW. Efficiency η = P_hyd / P_shaft = 3.5 kW / 4.58 kW = 76.4%."
                },
                {
                    "question": "Why is a foot valve installed at the bottom of an irrigation pump suction pipe?",
                    "options": ["Filter out dissolved salts", "Retain water in the pump casing and suction pipe when stopped, maintaining prime", "Increase water velocity", "Reduce engine emissions"],
                    "correct": 1,
                    "explanation": "The foot valve is a check valve that prevents water from draining out of the suction pipe, keeping the pump primed for restarting."
                }
            ],
            "settings": ["Impeller diameter: 160 mm", "Rated speed: 1750 RPM", "Fluid: Clean water at 20°C"],
            "samples": [1.0, 1.69, 2.56, 3.61, 4.84, 5.76],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💧", "label": "1. Centrifugal Pump Bench"},
                {"id": "compare", "icon": "📊", "label": "2. H-Q & Affinity Plot"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Pump Speed Sandbox"}
            ]
        },
        {
            "number": 17,
            "slug": "drip-irrigation-emitter-discharge-uniformity",
            "title": "Micro-Irrigation Drip Emitter Flow vs Pressure & Manufacturing Variation (CV)",
            "shortTitle": "Drip Emitter Uniformity",
            "aim": "Determine the discharge-pressure relationship, emitter discharge exponent x, and manufacturing coefficient of variation (CV) for agricultural drip irrigation emitters.",
            "inputLabel": "Logarithm of Operating Pressure ln(P)",
            "shortInput": "ln(Pressure P)",
            "inputUnit": "ln(kPa)",
            "min": 3.9120,
            "max": 5.5215,
            "step": 0.3219,
            "initial": 4.6052,
            "inputDecimals": 4,
            "rawLabel": "Logarithm of Emitter Discharge ln(q)",
            "rawUnit": "ln(L/h)",
            "rawDecimals": 4,
            "xAxis": "ln(Pressure P in kPa)",
            "yAxis": "ln(Discharge q in L/h)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 4.6,
            "emptyY": 1.55,
            "targetName": "Emitter Discharge Exponent x",
            "target": "0.5000",
            "refValue": 0.5000,
            "resultUnit": "dimensionless",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ln(q) = x · ln(P) + ln(k) = 0.5000 · ln(P) - 0.7500",
            "intro": "Drip (trickle) irrigation represents the most water-efficient irrigation method in modern agriculture, applying small, frequent quantities of water directly to the crop root zone through labyrinthine emitters at near-ambient pressure. Emitter hydraulic behavior follows the power-law flow equation q = k·P^x (linearized as ln q = x·ln P + ln k), where q is emitter discharge (L/h), P is operating pressure (kPa), k is the emitter discharge coefficient, and x is the emitter discharge exponent. The exponent x characterizes pressure sensitivity: for fully turbulent non-compensating orifice emitters, x ≈ 0.50; for laminar long-path micro-tubes, x ≈ 1.00; while for pressure-compensating (PC) elastomeric diaphragm emitters, x approaches 0.0 (0.0 to 0.1), delivering constant discharge despite lateral elevation drops and friction losses. In accordance with ASABE EP405 and ISO 9261, emitter manufacturing variability is quantified by the coefficient of manufacturing variation CV = s_q / q_bar across 25 replicate emitters, which directly governs field Emission Uniformity EU = 100·(1 - 1.27·CV)·(q_min / q_bar). In this lab, an automated drip test manifold tests 25 inline emitters across pressures from 50 to 250 kPa.",
            "modelExtra": "Evaluated using a manifold of 25 non-compensating turbulent vortex inline emitters (nominal 4.0 L/h at 100 kPa) across pressures from 50 to 250 kPa.",
            "apparatus": [
                {"name": "Agricultural Drip Emitter Test Manifold", "purpose": "Rigid manifold holding 25 inline drip emitters spaced at 30 cm intervals with graduated collection tubes."},
                {"name": "Booster Pump & Electronic Pressure Regulator", "purpose": "Regulates water pressure from 50 to 250 kPa with 0.5 kPa digital closed-loop control."},
                {"name": "Digital Pressure Gauge & Temperature Sensor", "purpose": "Logs manifold pressure and water temperature at 1 Hz."},
                {"name": "25-Cup Automated Graduated Catch System", "purpose": "Catches discharged water from all 25 emitters simultaneously."},
                {"name": "High-Precision Laboratory Electronic Balance", "purpose": "Weighs individual emitter catch aliquots with 0.01 g accuracy."},
                {"name": "Micro-Filtration 120-Mesh Disc Filter", "purpose": "Prevents suspended particulate clogging of intricate emitter labyrinth pathways."}
            ],
            "procedure": [
                {"title": "Manifold Flushing & Filter Inspection", "text": "Flush the drip manifold with clean water through the end flush valve for 2.0 minutes, verifying that the 120-mesh disc filter is clean."},
                {"title": "Pressure Stabilization at 50 kPa", "text": "Set the electronic regulator to P = 50 kPa (ln P = 3.9120), allowing all 25 emitters to discharge into waste troughs until steady flow is established."},
                {"title": "Timed Catch Collection", "text": "Position the 25 graduated catch cups under the emitters simultaneously for exactly 10.0 minutes, then remove them synchronously."},
                {"title": "Gravimetric Emitter Auditing", "text": "Weigh each individual catch cup to calculate the discharge q_i (L/h) of each emitter, computing mean discharge q_bar and standard deviation s_q to find CV."},
                {"title": "Pressure Stepping", "text": "Increment operating pressure across five additional stages: 75, 100, 140, 190, and 250 kPa (ln P up to 5.5215), repeating catch audits at each pressure."},
                {"title": "Flow Exponent Logarithmic Regression", "text": "Plot ln(q_bar) versus ln(P), perform linear regression to determine the emitter flow exponent x and coefficient k, and compute Emission Uniformity EU."}
            ],
            "topics": [
                {"question": "What is the physical significance of the emitter discharge exponent x?", "answer": "The exponent x characterizes the emitter's sensitivity to pressure variations along the lateral line. A value of x = 0.5 indicates turbulent orifice flow; x = 1.0 indicates laminar flow (highly sensitive to pressure); and x = 0.0 indicates a pressure-compensating emitter where discharge is independent of pressure."},
                {"question": "How does manufacturing coefficient of variation (CV) affect drip system uniformity?", "answer": "CV measures physical dimensional variations between emitters resulting from molding tolerances. Higher CV degrades field Emission Uniformity (EU) regardless of hydraulic design, leading to uneven crop watering and localized water stress."},
                {"question": "How do pressure-compensating (PC) drip emitters maintain constant flow?", "answer": "PC emitters incorporate a flexible silicone elastomeric diaphragm that deflects into the labyrinth flow channel as pressure increases, restricting the passage area to maintain a constant flow rate over a wide pressure range (typically 100 to 400 kPa)."},
                {"question": "What is the maximum allowable pressure variation (ΔP) along a non-compensating drip lateral?", "answer": "In standard micro-irrigation engineering, total hydraulic pressure variation along a lateral is limited to 20% (ΔP ≤ 0.20·P_avg), which restricts flow variation between the first and last emitter to within 10% (Δq ≤ 0.10·q_avg) for turbulent emitters (x = 0.5)."},
                {"question": "Why is 120-mesh (125-micron) filtration universally mandatory in micro-irrigation?", "answer": "Emitter labyrinth channels have tiny cross-sectional dimensions (typically 0.5 to 1.0 mm wide); any suspended sand, silt, or algae will lodge in the turns, causing permanent physical clogging and emitter failure."},
                {"question": "How does water temperature affect the discharge of laminar versus turbulent emitters?", "answer": "Laminar emitters (x = 1.0) are governed by Poiseuille's law and are highly sensitive to water viscosity, discharging up to 2% more water per °C rise in temperature. Turbulent emitters (x = 0.5) are governed by inertial forces and are virtually unaffected by water temperature."}
            ],
            "precautions": [
                "Always operate with pre-filtered water; microscopic particles permanently lodge inside emitter labyrinths.",
                "Ensure manifold lateral sits level so that static elevation heads across emitters remain identical.",
                "Empty catch cups thoroughly between runs to prevent residual tare weight errors.",
                "Verify that water temperature remains constant within ±1.5°C during pressure stepping."
            ],
            "limitations": [
                "Evaluates clean tap water; field irrigation water containing biological slimes, iron precipitates, or carbonates requires chemical chlorination and acid injection.",
                "Elastomeric diaphragms in PC emitters suffer hysteresis and fatigue over multi-year field service.",
                "Static test bench eliminates wind drift and soil surface evaporation present in field drip installations.",
                "Manufacturing CV measured across 25 emitters represents a small sample; industrial QA protocols test 100+ units per production lot."
            ],
            "quiz": [
                {
                    "question": "What emitter discharge exponent x indicates a fully pressure-compensating (PC) emitter?",
                    "options": ["x = 1.0", "x = 0.5", "x ≈ 0.0", "x = 2.0"],
                    "correct": 2,
                    "explanation": "A pressure-compensating emitter maintains constant discharge regardless of pressure, corresponding to an exponent x ≈ 0.0 (P⁰ = 1)."
                },
                {
                    "question": "According to ASABE standards, an emitter manufacturing coefficient of variation (CV) below what threshold is rated 'excellent'?",
                    "options": ["CV < 0.05 (5%)", "CV < 0.15 (15%)", "CV < 0.30 (30%)", "CV < 0.50 (50%)"],
                    "correct": 0,
                    "explanation": "ASABE EP405 classifies emitter manufacturing quality as 'excellent' when CV is less than 0.05 (5%)."
                },
                {
                    "question": "If a turbulent emitter (x = 0.50) discharges 4.0 L/h at 100 kPa, what discharge is expected at 225 kPa?",
                    "options": ["4.0 L/h", "6.0 L/h", "8.0 L/h", "9.0 L/h"],
                    "correct": 1,
                    "explanation": "q₂ / q₁ = (P₂ / P₁)^0.5 = (225 / 100)^0.5 = √2.25 = 1.50. Discharge q₂ = 4.0 × 1.50 = 6.0 L/h."
                },
                {
                    "question": "What primary water treatment is used to eliminate bacterial slime and algae in drip irrigation laterals?",
                    "options": ["Periodic chlorine injection (chlorination)", "Adding engine oil", "High-frequency ultrasound", "Freezing the lines"],
                    "correct": 0,
                    "explanation": "Periodic injection of chlorine (sodium hypochlorite or gas chlorine) oxidizes organic slimes and kills algae that clog emitter labyrinths."
                }
            ],
            "settings": ["Number of emitters tested: 25", "Nominal rating: 4.0 L/h at 100 kPa", "Water temperature: 20°C"],
            "samples": [3.9120, 4.3175, 4.6052, 4.9416, 5.2470, 5.5215],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💧", "label": "1. Drip Manifold Bench"},
                {"id": "compare", "icon": "📊", "label": "2. ln(q) vs ln(P) Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Pressure & CV Sandbox"}
            ]
        },
        {
            "number": 18,
            "slug": "agricultural-sprinkler-christiansen-uniformity",
            "title": "Agricultural Impact Sprinkler Christiansen Uniformity Coefficient (CU) Catch-Can Analysis",
            "shortTitle": "Sprinkler Christiansen Uniformity",
            "aim": "Determine the radial water distribution profile, Christiansen Uniformity Coefficient (CU), and overlapping pattern efficiency of an agricultural impact sprinkler nozzle across varying operating pressures.",
            "inputLabel": "Sprinkler Operating Pressure P",
            "shortInput": "Pressure P",
            "inputUnit": "kPa",
            "min": 150.0,
            "max": 400.0,
            "step": 50.0,
            "initial": 250.0,
            "inputDecimals": 1,
            "rawLabel": "Christiansen Uniformity Coefficient CU",
            "rawUnit": "%",
            "rawDecimals": 2,
            "xAxis": "Operating pressure P (kPa)",
            "yAxis": "Christiansen Uniformity CU (%)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 275.0,
            "emptyY": 79.1,
            "targetName": "Uniformity Pressure Sensitivity s_p",
            "target": "0.0550",
            "refValue": 0.0550,
            "resultUnit": "%/kPa",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "CU = s_p · P + CU_0 = 0.0550 · P + 64.0000",
            "intro": "Sprinkler irrigation applies water by spraying high-velocity droplets through air under pressure, simulating natural rainfall across field crops, pastures, and orchards. An agricultural impact sprinkler utilizes an oscillating spring-loaded drive arm that repeatedly deflects into the water jet, intermittently rotating the nozzle body around its vertical axis. The spatial distribution of water caught on the ground is governed by nozzle pressure, nozzle orifice diameter, jet trajectory angle (typically 23° to 27°), and ambient wind speed. In accordance with ASABE S398, sprinkler water distribution is quantified using a radial grid of catch cans, and uniformity across overlapping sprinkler spacings (rectangular or triangular layouts) is calculated using the Christiansen Uniformity Coefficient: CU = 100·[1 - (Σ|X_i - X_bar|) / (n·X_bar)], where X_i is the water depth caught in each can and X_bar is the mean catch depth. Operating at sub-optimal low pressure causes 'doughnut' patterns where water falls in an outer ring while the center remains dry, producing poor CU (< 70%). Increasing pressure breaks the jet into fine droplets that fill the inner radius, boosting CU above 85% until excessive misting and wind drift emerge. In this indoor laboratory trial, a 100-catch-can grid records sprinkler precipitation profiles.",
            "modelExtra": "Evaluated using a single 4.8 mm brass agricultural impact sprinkler mounted on a 1.2 m riser in zero-wind indoor catch-can grid with 12 m × 12 m simulated overlap.",
            "apparatus": [
                {"name": "Agricultural Impact Sprinkler (4.8 mm Nozzle)", "purpose": "Standard brass agricultural impact sprinkler with 23° trajectory angle and drive vane."},
                {"name": "Indoor Catch-Can Matrix Array (100 Cans)", "purpose": "Graduated catch cans spaced on a 1.5 m × 1.5 m grid over a 15 m radius."},
                {"name": "Booster Pump & Electronic Pressure Regulator", "purpose": "Supplies regulated water pressure from 150 to 400 kPa with digital readout."},
                {"name": "Calibrated Graduated Measuring Cylinders", "purpose": "Measures water depth caught in each catch can with 0.5 mL precision."},
                {"name": "Electronic In-Line Turbine Flowmeter", "purpose": "Records total sprinkler discharge rate Q (L/min) with 0.1 L/min accuracy."},
                {"name": "Ultrasonic Droplet Velocity Sensor", "purpose": "Monitors jet breakup distance and droplet exit velocity."}
            ],
            "procedure": [
                {"title": "Catch-Can Grid Siting & Leveling", "text": "Lay out the catch cans in a square 1.5 m × 1.5 m matrix across the indoor test hall, ensuring all can rims sit level and at uniform elevation."},
                {"title": "Riser Mounting & Pressure Set", "text": "Mount the impact sprinkler on the central 1.2 m vertical riser, setting the pressure regulator to initial low pressure P = 150.0 kPa."},
                {"title": "Timed Test Precipitation Run", "text": "Start the sprinkler pump and allow the sprinkler to rotate continuously for exactly 30.0 minutes, distributing water across the catch-can grid."},
                {"title": "Can Volumetric Auditing", "text": "Measure and record the depth of water caught in each can X_i (mm), computing the mean depth X_bar and the mean absolute deviation Σ|X_i - X_bar| / n."},
                {"title": "Christiansen CU Computation", "text": "Simulate a 12 m × 12 m overlapping sprinkler layout and calculate the Christiansen Uniformity Coefficient CU = 100·[1 - Σ|X_i - X_bar| / (n·X_bar)]."},
                {"title": "Pressure Stepping", "text": "Repeat the procedure at 200, 250, 300, 350, and 400 kPa, plotting CU versus pressure to extract the sensitivity slope s_p."}
            ],
            "topics": [
                {"question": "State the Christiansen Uniformity Coefficient (CU) mathematical formula.", "answer": "CU = 100·[1.0 - (Σ|X_i - X_bar|) / (n·X_bar)], where X_i is individual catch-can depth, X_bar is mean catch depth, and n is the total number of catch cans in the overlapping pattern area."},
                {"question": "How does low nozzle pressure distort the sprinkler distribution profile?", "answer": "Insufficient pressure fails to atomize the water jet, causing the stream to travel as a solid ropy cylinder that lands predominantly at the outer perimeter. This produces a 'doughnut' pattern with very low water depth in the middle radius, yielding unacceptably low CU."},
                {"question": "What is the Distribution Uniformity (DU) metric?", "answer": "Distribution Uniformity (DU = X_low_quarter / X_bar) compares the average catch depth in the lowest 25% of the cans to the overall average depth, serving as a conservative measure of under-irrigation risk."},
                {"question": "What sprinkler spacing is recommended relative to wetted diameter?", "answer": "In calm conditions, square sprinkler spacing is typically set to 50% to 60% of the wetted diameter (e.g., for a 24 m diameter, spacing is 12 m × 12 m) to ensure sufficient overlapping and acceptable Christiansen uniformity (> 80%)."},
                {"question": "How does ambient crosswind affect field sprinkler uniformity?", "answer": "Wind distorts the circular pattern into an elongated ellipse, drifts fine droplets downwind, reduces the upwind throw radius, and severely degrades CU, often requiring closer sprinkler spacing on laterals."},
                {"question": "What is the function of the oscillating impact arm on the sprinkler?", "answer": "The spring-loaded arm is swung outward by the jet and snapped back by a torsion spring, repeatedly striking the nozzle body to impart small rotational increments that rotate the sprinkler 360° around its vertical axis."}
            ],
            "precautions": [
                "Perform all sprinkler patternation testing indoors or in zero-wind (< 1.0 m/s) conditions to prevent wind drift distortion.",
                "Verify that catch cans are clean and dry before each run; check that can lips are sharp and burr-free.",
                "Ensure the sprinkler riser is perfectly plumb; any vertical tilt skews water distribution into an asymmetric pattern.",
                "Do not stand in the spray path during rotation to avoid intercepting water before it reaches catch cans."
            ],
            "limitations": [
                "Indoor tests eliminate wind drift and atmospheric evaporative droplet losses occurring in open fields.",
                "Assumes a flat horizontal ground surface; undulating field topography alters local throw distances.",
                "Single-nozzle tests rely on mathematical superposition to model multiple overlapping sprinklers.",
                "Can evaporation during long test runs (> 1 hour) can slightly reduce measured depths in hot, dry climates."
            ],
            "quiz": [
                {
                    "question": "What is the minimum Christiansen Uniformity Coefficient (CU) considered acceptable for commercial agricultural sprinkler systems?",
                    "options": ["40%", "60%", "80%", "99%"],
                    "correct": 2,
                    "explanation": "Standard agricultural irrigation engineering design requires a minimum CU of 80% to 85% to ensure uniform crop growth."
                },
                {
                    "question": "What water distribution profile is produced by an impact sprinkler operating at severely sub-optimal low pressure?",
                    "options": ["Uniform triangular pattern", "Doughnut (ring) pattern with dry center", "Inverted cone pattern", "Flat horizontal sheet"],
                    "correct": 1,
                    "explanation": "Low pressure fails to atomize the jet, causing the solid stream to throw water only to the outer perimeter, leaving a dry center (doughnut pattern)."
                },
                {
                    "question": "If 100 cans have an average depth of 10.0 mm and the sum of absolute deviations is 150 mm, what is CU?",
                    "options": ["75.0%", "85.0%", "90.0%", "95.0%"],
                    "correct": 1,
                    "explanation": "CU = 100 × [1 - (150) / (100 × 10.0)] = 100 × [1 - 0.15] = 85.0%."
                },
                {
                    "question": "To achieve high uniformity in solid-set sprinkler systems, adjacent sprinklers must:",
                    "options": ["Be spaced so their spray patterns significantly overlap", "Be shielded from each other with tarps", "Rotate in opposite directions at double speed", "Operate only at midnight"],
                    "correct": 0,
                    "explanation": "Sprinklers must be spaced at 50% to 60% of their throw diameter so overlapping spray patterns blend into a uniform water depth."
                }
            ],
            "settings": ["Nozzle diameter: 4.8 mm", "Riser height: 1.2 m", "Simulated spacing: 12 m × 12 m square"],
            "samples": [150.0, 200.0, 250.0, 300.0, 350.0, 400.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💧", "label": "1. Catch-Can Test Grid"},
                {"id": "compare", "icon": "📊", "label": "2. CU vs Pressure Plot"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Sprinkler Radius Sandbox"}
            ]
        },
        {
            "number": 19,
            "slug": "rainfall-simulator-runoff-soil-loss-usle",
            "title": "Rainfall Simulator Surface Runoff & Sediment Yield (Universal Soil Loss Equation)",
            "shortTitle": "Rainfall Runoff Soil Loss",
            "aim": "Measure surface runoff volume and soil sediment detachment under controlled artificial rainfall and calibrate the soil erodibility factor (K) in the Universal Soil Loss Equation (USLE).",
            "inputLabel": "Normalized Rainfall Erosivity Index EI_30 / 100",
            "shortInput": "Erosivity EI/100",
            "inputUnit": "index/100",
            "min": 1.0,
            "max": 4.5,
            "step": 0.7,
            "initial": 2.4,
            "inputDecimals": 2,
            "rawLabel": "Total Soil Sediment Yield A",
            "rawUnit": "kg/ha",
            "rawDecimals": 2,
            "xAxis": "Rainfall erosivity index EI_30 / 100",
            "yAxis": "Sediment yield A (kg/ha)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 2.75,
            "emptyY": 34.375,
            "targetName": "Soil Erodibility Scaling Factor K_usle",
            "target": "12.5000",
            "refValue": 12.5000,
            "resultUnit": "kg/(ha·index)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "A = K_usle · (EI_30 / 100) = 12.5000 · (EI_30 / 100)",
            "intro": "Soil erosion by water degrades agricultural soil productivity, depletes topsoil organic matter, and causes severe downstream reservoir sedimentation and water pollution. The Universal Soil Loss Equation (USLE) and its revised form (RUSLE), developed by Wischmeier and Smith, is the international standard empirical model for estimating long-term average annual soil loss: A = R·K·LS·C·P, where A is soil loss, R is the rainfall-runoff erosivity factor, K is the soil erodibility factor, LS is the slope length-steepness topographic factor, C is the cover-management factor, and P is the support practice conservation factor. Rainfall erosivity R is quantified by the product of total storm kinetic energy E and maximum 30-minute rainfall intensity I_30 (the EI_30 index). High-energy raindrop impact detaches soil aggregates by splash detachment, while excess rainfall exceeding the infiltration capacity generates overland sheet and rill runoff that transports suspended sediment. In this laboratory investigation, an oscillating nozzle rainfall simulator applies controlled storm intensities across a standard 1.0 m × 2.0 m tilted soil erosion flume to quantify runoff hydrographs, sediment discharge, and soil erodibility K.",
            "modelExtra": "Evaluated using bare tilled sandy clay loam soil packed in a 9% slope erosion flume (LS = 1.0, C = 1.0, P = 1.0) under simulated rainfall intensities from 35 to 110 mm/h.",
            "apparatus": [
                {"name": "Laboratory Oscillating Nozzle Rainfall Simulator", "purpose": "Applies realistic drop size distribution and terminal impact velocity across the flume."},
                {"name": "Tilting Soil Erosion Flume (1.0 m × 2.0 m)", "purpose": "Heavy-duty steel soil bed with porous drainage floor and adjustable slope from 0% to 20%."},
                {"name": "Runoff & Sediment Collection Flume End-Trough", "purpose": "Captures all overland runoff water and detached soil sediment continuously."},
                {"name": "Electronic Runoff Hydrograph Weighing Logger", "purpose": "Measures cumulative runoff mass at 5-second intervals to plot the hydrograph."},
                {"name": "Suspended Sediment Centrifuge & Convection Oven", "purpose": "Separates suspended sediment from runoff aliquots and dries soil at 105°C."},
                {"name": "Optical Disdrometer Raindrop Sensor", "purpose": "Measures droplet size spectrum and kinetic impact energy E with 0.1 mm precision."}
            ],
            "procedure": [
                {"title": "Soil Flume Packing & Slope Setup", "text": "Pack the erosion flume with sieved agricultural soil in 5 cm lifts to achieve uniform bulk density (1.30 g/cm³), setting flume tilt to exactly 9% standard slope."},
                {"title": "Soil Pre-Wetting Calibration", "text": "Pre-wet the soil bed with fine mist for 15 minutes to bring topsoil to consistent field capacity and eliminate antecedent moisture variability."},
                {"title": "Simulator Intensity Setting", "text": "Set oscillating nozzle frequency and water pressure to deliver rainfall intensity I = 35 mm/h (corresponding to EI_30 / 100 = 1.00)."},
                {"title": "Runoff Hydrograph & Sediment Sampling", "text": "Engage rainfall for exactly 30 minutes, recording the time to runoff initiation and collecting 1-liter runoff-sediment samples every 5 minutes from the collection trough."},
                {"title": "Sediment Separation & Gravimetry", "text": "Flocculate and centrifuge runoff samples, decant clear water, and dry sediment in the 105°C oven to compute total sediment yield A (kg/ha)."},
                {"title": "Erosivity Stepping & Erodibility Slope", "text": "Increment rainfall erosivity across five additional levels (EI_30 / 100 = 1.7, 2.4, 3.1, 3.8, 4.5), plot sediment yield A versus erosivity, and extract the erodibility slope K_usle."}
            ],
            "topics": [
                {"question": "State the Universal Soil Loss Equation (USLE) and define each factor.", "answer": "A = R·K·LS·C·P, where A is computed average annual soil loss (t/ha), R is rainfall-runoff erosivity index, K is soil erodibility factor, LS is slope length and steepness factor, C is crop cover and management factor, and P is conservation support practice factor."},
                {"question": "How is rainfall erosivity (EI_30) defined mathematically?", "answer": "EI_30 is the product of total storm kinetic energy E (MJ/ha) and the maximum continuous 30-minute rainfall intensity I_30 (mm/h), reflecting the combined capacity of raindrop impact energy and peak runoff volume to erode soil."},
                {"question": "What is the physical significance of the soil erodibility factor K?", "answer": "Factor K represents the intrinsic susceptibility of a soil to detachment and transport by raindrops and runoff under standard unit plot conditions (bare fallow, 9% slope, 22.1 m length). It is governed by soil texture (% silt, sand, clay), organic matter, structure, and permeability."},
                {"question": "Distinguish between splash erosion, sheet erosion, and rill erosion.", "answer": "Splash erosion is the detachment and local airborne displacement of soil particles by falling raindrop impacts. Sheet erosion is the uniform removal of a thin topsoil layer by overland sheet flow. Rill erosion occurs when runoff concentrates into small, distinct micro-channels (rills)."},
                {"question": "How does vegetative cover (C factor) dramatically reduce soil erosion?", "answer": "Canopy cover intercepts falling raindrops, absorbing their kinetic impact energy so water drips gently to the ground. Surface mulch and root networks slow overland runoff velocity, increase infiltration time, and physically bind soil aggregates against shearing."},
                {"question": "What conservation practices are quantified by the P factor in USLE?", "answer": "The P factor quantifies specific soil-conserving mechanical practices: contour farming (tilling across the slope), contour strip-cropping, and terrace construction, which reduce runoff velocity and trap sediment before it leaves the field."}
            ],
            "precautions": [
                "Calibrate nozzle oscillation and pressure before test runs to ensure uniform spatial rainfall coverage across the entire soil bed.",
                "Ensure runoff collection trough is completely cleared of settled sediment between consecutive storm trials.",
                "Maintain flume side-wall seals tight; gaps along walls create artificial rills that skew sediment yield.",
                "Oven-dry sediment samples for a full 24 hours at 105°C to ensure 100% moisture removal before gravimetric weighing."
            ],
            "limitations": [
                "USLE predicts average sheet and rill erosion; it does not model gully erosion, stream bank collapse, or mass landslides.",
                "Simulator flumes (2.0 m length) scale down standard USLE unit plots (22.1 m), requiring slope length factor (L) adjustments.",
                "Simulated rainfall uses oscillating nozzles that produce droplet distributions differing slightly from natural cyclonic storms.",
                "Sediment delivery ratios (SDR) must be applied when extrapolating field flume plot losses to whole watershed scale."
            ],
            "quiz": [
                {
                    "question": "In the Universal Soil Loss Equation A = R·K·LS·C·P, what does the factor K represent?",
                    "options": ["Crop cover factor", "Soil erodibility factor", "Rainfall kinetic energy", "Conservation practice factor"],
                    "correct": 1,
                    "explanation": "K is the soil erodibility factor, quantifying the intrinsic vulnerability of a specific soil type to detachment and erosion."
                },
                {
                    "question": "What standard slope steepness is defined as the baseline (LS = 1.0) in USLE unit plot calibration?",
                    "options": ["1%", "5%", "9%", "25%"],
                    "correct": 2,
                    "explanation": "The standard USLE unit plot is defined on a 9% slope (with 22.1 m length, bare tilled fallow soil)."
                },
                {
                    "question": "If rainfall erosivity index increases by a factor of 3 on bare soil, how does soil loss A respond?",
                    "options": ["Soil loss triples (increases linearly by 3×)", "Soil loss drops to zero", "Soil loss increases by 9×", "Soil loss is unaffected"],
                    "correct": 0,
                    "explanation": "Because A is directly proportional to R (A = R·K·LS·C·P), tripling erosivity triples soil loss on identical bare plots."
                },
                {
                    "question": "Which soil component provides the greatest resistance against raindrop detachment and surface crusting?",
                    "options": ["Fine silt particles", "Soil organic matter and stable humus aggregates", "Sodium ions", "Coarse gravel"],
                    "correct": 1,
                    "explanation": "Soil organic matter binds particles into water-stable aggregates that resist raindrop impact and prevent surface pore clogging."
                }
            ],
            "settings": ["Flume dimensions: 1.0 m × 2.0 m", "Bed slope: 9.0% (standard USLE)", "Soil: Bare tilled sandy clay loam"],
            "samples": [1.0, 1.7, 2.4, 3.1, 3.8, 4.5],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💧", "label": "1. Rainfall Simulator Flume"},
                {"id": "compare", "icon": "📊", "label": "2. Sediment vs Erosivity Plot"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Slope & Rainfall Sandbox"}
            ]
        }
    ]
