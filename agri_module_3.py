# -*- coding: utf-8 -*-
"""Agricultural Engineering Module 3: Post-Harvest Processing & Crop Value Addition (Labs 20–28)."""

def get_module_3():
    return [
        {
            "number": 20,
            "slug": "grain-moisture-content-oven-drying-method",
            "title": "Grain Moisture Content Determination via Standard Air-Oven Method (ASABE S352)",
            "shortTitle": "Oven Grain Moisture Content",
            "aim": "Determine the dry-basis and wet-basis moisture content of agricultural grains using the standard air-oven method and calibrate an electronic capacitance grain moisture meter.",
            "inputLabel": "Evaporated Moisture Mass Loss Δm",
            "shortInput": "Mass Loss Δm",
            "inputUnit": "g",
            "min": 1.0,
            "max": 4.5,
            "step": 0.7,
            "initial": 2.4,
            "inputDecimals": 2,
            "rawLabel": "Dry-Basis Moisture Content M_db",
            "rawUnit": "%",
            "rawDecimals": 2,
            "xAxis": "Moisture mass loss Δm (g)",
            "yAxis": "Dry-basis moisture content M_db (%)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 2.75,
            "emptyY": 17.19,
            "targetName": "Gravimetric Moisture Gradient k_m",
            "target": "6.2500",
            "refValue": 6.2500,
            "resultUnit": "%/g",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "M_db = k_m · Δm = 6.2500 · Δm",
            "intro": "Moisture content is the single most critical quality parameter in post-harvest grain handling, storage, commercial trading, and milling. Grains harvested with excessive moisture (e.g. corn at 22% to 28% w.b.) rapidly heat up, respire, and spoil from fungal mold (Aspergillus, Penicillium) and mycotoxin accumulation, while over-dried grain suffers kernel brittleness and stress cracking during handling. Moisture content is expressed on either a wet basis (M_wb = m_w / m_total × 100%) for commercial marketing, or on a dry basis (M_db = m_w / m_dry × 100%) for engineering drying calculations and mass balances. The primary reference standard for moisture determination in agricultural engineering is the forced-draft air-oven method specified by ASABE Standard S352 (for whole unground wheat: 130°C for 19 hours; for corn: 103°C for 72 hours). Electronic moisture meters deployed in commercial elevators measure electrical capacitance or conductance, which are rapid non-destructive secondary methods that must be calibrated directly against primary gravimetric oven data. In this laboratory, calibrated moisture samples are evaluated across controlled moisture mass loss intervals.",
            "modelExtra": "Evaluated using standard 20.0 g samples of clean wheat (constant dry solid mass m_dry = 16.0 g). Dry basis moisture M_db scales linearly with evaporated moisture mass loss Δm.",
            "apparatus": [
                {"name": "Standard Forced-Convection Drying Oven (130°C)", "purpose": "Maintains constant thermal desiccation temperature within ±0.5°C with uniform internal airflow."},
                {"name": "Hermetic Glass Desiccator with Blue Silica Gel", "purpose": "Cools heated moisture dishes to room temperature in moisture-free atmosphere before weighing."},
                {"name": "Aluminum Grain Moisture Weighing Dishes", "purpose": "Low-profile shallow metal dishes with tight-fitting slip-over lids to prevent moisture re-absorption."},
                {"name": "Analytical Laboratory Balance (0.0001 g)", "purpose": "Measures wet sample and oven-dry bone-dry mass with high analytical precision."},
                {"name": "Electronic Dielectric Capacitance Moisture Meter", "purpose": "Provides non-destructive secondary dielectric grain moisture readouts for calibration."},
                {"name": "Hermetic Polyethylene Conditioning Jars", "purpose": "Equilibrates grain lots at graded moisture levels with distilled water rehydration."}
            ],
            "procedure": [
                {"title": "Oven Pre-Heating & Dish Taring", "text": "Pre-heat the forced-convection oven to exactly 130°C. Clean, dry, and tare aluminum moisture dishes with lids, recording tare mass m_dish on the analytical balance."},
                {"title": "Sample Preparation & Weighing", "text": "Weigh exactly 20.000 g of unground grain sample into each dish, spreading kernels in a uniform thin layer, and record initial wet sample mass m_initial."},
                {"title": "Oven Thermal Desiccation", "text": "Place uncovered dishes into the 130°C oven (resting lids beside dishes), closing the door and initiating timer for exactly 19.0 hours in accordance with ASABE S352."},
                {"title": "Desiccator Cooling", "text": "At 19 hours, quickly cover dishes with lids, transfer immediately into the silica gel desiccator, and allow dishes to cool to room temperature (30 to 45 minutes)."},
                {"title": "Dry Mass Weighing & Loss Calculation", "text": "Weigh cooled covered dishes to determine final bone-dry mass m_final, calculating moisture loss Δm = m_initial - m_final and dry-basis moisture M_db = (Δm / m_dry) × 100%."},
                {"title": "Capacitance Meter Cross-Calibration", "text": "Repeat testing across six grain moisture levels, plot oven M_db versus Δm to confirm gradient k_m = 100 / m_dry, and plot electronic meter readings against true oven moisture."}
            ],
            "topics": [
                {"question": "Distinguish mathematically between wet-basis and dry-basis moisture content.", "answer": "Wet-basis moisture M_wb = [m_w / (m_w + m_d)] × 100% divides water mass by total wet grain weight. Dry-basis moisture M_db = (m_w / m_d) × 100% divides water mass by constant bone-dry matter weight. They are related by M_db = M_wb / (100 - M_wb) × 100%."},
                {"question": "Why do engineering drying calculations use dry-basis rather than wet-basis moisture?", "answer": "During drying, water evaporates while the dry solid matter mass m_d remains perfectly constant. Using dry basis maintains a constant denominator throughout mass balances and drying rate equations, whereas wet basis has a continuously changing total weight denominator."},
                {"question": "Why is whole unground wheat dried at 130°C for 19 hours, whereas corn is dried at 103°C for 72 hours in ASABE S352?", "answer": "Corn contains higher oil and lipid content; high temperatures (> 103°C) cause thermal decomposition and oxidation of volatile lipids, leading to erroneous mass loss. Lower temperatures over longer periods safely drive off water without decomposing organic grain compounds."},
                {"question": "What is the role of the desiccator in moisture determination?", "answer": "Hot moisture dishes transferred directly to open air create convective air currents that disrupt balance pans, and bone-dry grain absorbs ambient atmospheric moisture within seconds. The desiccator cools samples in dry air, ensuring true dry mass measurement."},
                {"question": "How do electronic capacitance grain moisture meters work?", "answer": "Water has a very high dielectric constant (approx. 80 at 20°C) compared to dry grain starch and protein (approx. 3 to 5). Measuring the electrical capacitance of a grain cell directly reflects the volume fraction of water present."},
                {"question": "What is 'bound water' versus 'free water' in agricultural seeds?", "answer": "Free water occupies capillary spaces between cells, freezes at 0°C, and evaporates easily during drying. Bound water is held chemically by hydrogen bonds to polar hydroxyl groups of starch and protein, requires higher energy to remove, and does not freeze at 0°C."}
            ],
            "precautions": [
                "Never open the oven door during the 19-hour drying cycle; door openings drop chamber temperature and disrupt drying kinetics.",
                "Ensure silica gel in the desiccator is active (deep blue); pink silica gel is saturated and must be regenerated at 150°C.",
                "Never leave dry sample dishes uncovered outside the desiccator; bone-dry grain is extremely hygroscopic.",
                "Ensure sample dishes are sealed with well-fitting lids during transfer and balance weighing."
            ],
            "limitations": [
                "The air-oven method is destructive and requires 19 to 72 hours, making it unsuitable for instant elevator grain receiving.",
                "Extremely high initial moisture (> 25%) can cause kernel boiling and foaming unless pre-dried in a gentle two-stage process.",
                "Does not differentiate between evaporated water and volatilization of trace organic essential oils.",
                "Electronic capacitance meters require variety-specific temperature and test-weight density calibrations."
            ],
            "quiz": [
                {
                    "question": "If 100 g of wet paddy contains 20 g of water, what are its wet-basis and dry-basis moisture contents?",
                    "options": ["M_wb = 20%, M_db = 20%", "M_wb = 20%, M_db = 25%", "M_wb = 25%, M_db = 20%", "M_wb = 16.7%, M_db = 20%"],
                    "correct": 1,
                    "explanation": "M_wb = 20 / 100 = 20%. Dry matter = 100 - 20 = 80 g. M_db = 20 / 80 = 25%."
                },
                {
                    "question": "What is the international reference standard method for calibrating commercial grain moisture meters?",
                    "options": ["Microwave heating for 3 minutes", "ASABE standard forced-air oven drying method", "Sun drying on a concrete apron", "Visual color inspection"],
                    "correct": 1,
                    "explanation": "The standard air-oven method (ASABE S352) is the universally accepted primary calibration benchmark for grain moisture."
                },
                {
                    "question": "Why must cooled moisture dishes be stored in a desiccator with active desiccant before weighing?",
                    "options": ["To cool the dishes slowly and prevent re-absorption of ambient moisture by dry grain", "To sterilize the kernels against bacteria", "To bleach the grain color", "To add chemical weight"],
                    "correct": 0,
                    "explanation": "Bone-dry grain is intensely hygroscopic and rapidly absorbs atmospheric water vapor unless kept in a sealed desiccator."
                },
                {
                    "question": "For a 20.0 g sample with 16.0 g dry matter, if moisture loss is Δm = 3.2 g, what is M_db?",
                    "options": ["16.0%", "20.0%", "25.0%", "32.0%"],
                    "correct": 1,
                    "explanation": "M_db = (Δm / m_dry) × 100% = (3.2 g / 16.0 g) × 100% = 20.0%."
                }
            ],
            "settings": ["Sample mass: 20.000 g", "Oven temp: 130.0°C (19 hours)", "Crop: Hard red winter wheat"],
            "samples": [1.0, 1.7, 2.4, 3.1, 3.8, 4.5],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🌾", "label": "1. Air-Oven Moisture Bench"},
                {"id": "compare", "icon": "📊", "label": "2. M_db vs Mass Loss Plot"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Wet vs Dry Basis Sandbox"}
            ]
        },
        {
            "number": 21,
            "slug": "equilibrium-moisture-content-sorption-isotherms",
            "title": "Equilibrium Moisture Content (EMC) & Sorption Isotherms (Modified Henderson Model)",
            "shortTitle": "Equilibrium Moisture Isotherms",
            "aim": "Determine the equilibrium moisture content (EMC) of agricultural cereal grain at constant temperature across variable relative humidities and calibrate the Modified Henderson sorption isotherm model.",
            "inputLabel": "Transformed Relative Humidity ln(-ln(1 - RH))",
            "shortInput": "ln(-ln(1-RH))",
            "inputUnit": "transformed",
            "min": -2.25,
            "max": 0.45,
            "step": 0.54,
            "initial": -0.63,
            "inputDecimals": 2,
            "rawLabel": "Logarithm of Equilibrium Moisture ln(M_e)",
            "rawUnit": "ln(%)",
            "rawDecimals": 4,
            "xAxis": "ln(-ln(1 - RH))",
            "yAxis": "ln(Equilibrium moisture M_e in %)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": -0.9,
            "emptyY": 1.632,
            "targetName": "Henderson Model Slope c_h",
            "target": "0.5200",
            "refValue": 0.5200,
            "resultUnit": "dimensionless",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ln(M_e) = c_h · ln(-ln(1 - RH)) + ln(K_h) = 0.5200 · ln(-ln(1 - RH)) + 2.1000",
            "intro": "Equilibrium Moisture Content (EMC) is the moisture level a hygroscopic biological material approaches when exposed to an environment of constant temperature and relative humidity for an extended duration. In agricultural grain drying and bulk storage aeration, EMC dictates the ultimate limit to which grain can be dried with ambient air, as well as the threshold relative humidity above which grain will reabsorb moisture from humid weather and spoil in silos. A plot of EMC versus equilibrium relative humidity (water activity a_w = RH/100) at constant temperature is known as a moisture sorption isotherm, which displays a characteristic sigmoidal (Type II) curve for starchy agricultural grains. Multiple empirical and semi-theoretical equations describe grain isotherms, among which the Modified Henderson equation 1 - RH = exp(-K·(T + C)·M_e^N) is universally adopted by ASABE Standard D245. Linearizing the Henderson formulation into ln(M_e) = c_h·ln[-ln(1 - RH)] + ln(K_h) allows direct extraction of sorption coefficients. In this investigation, sealed saturated salt solution desiccators provide controlled equilibrium relative humidities from 11% to 85% at 25°C to construct the desorption isotherm.",
            "modelExtra": "Evaluated using shelled yellow dent corn at constant 25°C in static gravimetric chambers containing analytical saturated salt solutions (LiCl, MgCl₂, Mg(NO₃)₂, NaCl, KCl).",
            "apparatus": [
                {"name": "Static Saturated Salt Equilibrium Desiccators", "purpose": "Maintains constant chemical water vapor activities (RH 11% to 85%) inside sealed glass jars."},
                {"name": "Temperature-Controlled Environmental Incubator (25.0°C)", "purpose": "Maintains isothermal test conditions within ±0.2°C over multi-week equilibration."},
                {"name": "Perforated Stainless Steel Sample Baskets", "purpose": "Suspends thin layers of grain kernels directly above the saturated salt solutions."},
                {"name": "High-Precision Analytical Balance (0.0001 g)", "purpose": "Logs grain sample mass changes every 48 hours until true asymptotic equilibrium is verified."},
                {"name": "Forced-Air Drying Oven (103°C)", "purpose": "Determines final bone-dry mass of equilibrated grain samples in accordance with ASABE S352."},
                {"name": "Chilled-Mirror Dew-Point Water Activity Meter", "purpose": "Verifies equilibrium headspace relative humidity with ±0.003 a_w precision."}
            ],
            "procedure": [
                {"title": "Saturated Salt Solution Preparation", "text": "Prepare analytical saturated salt solutions (LiCl, MgCl₂, K₂CO₃, NaNO₂, NaCl, KCl) with excess undissolved crystals in six sealed desiccator jars to establish standard relative humidities: 11.3%, 32.8%, 43.2%, 64.3%, 75.3%, and 84.3% at 25.0°C."},
                {"title": "Grain Sample Weighing & Loading", "text": "Weigh exactly 10.000 g of pre-wetted corn kernels into perforated stainless steel baskets, suspending one basket in the vapor headspace of each sealed salt jar."},
                {"title": "Isothermal Incubation", "text": "Place all sealed desiccator jars inside the 25.0°C environmental incubator, leaving undisturbed for 21 days to ensure complete vapor-solid thermodynamic equilibrium."},
                {"title": "Equilibrium Mass Verification", "text": "Weigh sample baskets every 48 hours until consecutive readings over 4 days show mass stability within ±0.002 g, confirming asymptotic EMC."},
                {"title": "Oven Bone-Dry Determination", "text": "Transfer equilibrated grain samples into the 103°C oven for 72 hours to determine bone-dry mass and calculate dry-basis equilibrium moisture content M_e (%)."},
                {"title": "Modified Henderson Model Linearization", "text": "Transform RH and M_e into ln[-ln(1 - RH)] and ln(M_e), plot the linearized relationship, and evaluate Henderson parameters c_h and K_h via linear regression."}
            ],
            "topics": [
                {"question": "What is Equilibrium Moisture Content (EMC)?", "answer": "EMC is the steady-state moisture content that a hygroscopic material like grain attains when exposed to an environment of constant temperature and relative humidity, where water vapor pressure in the grain equals water vapor pressure in the ambient air."},
                {"question": "Explain the difference between adsorption and desorption isotherms.", "answer": "An adsorption isotherm is measured by exposing dry grain to increasing humidity (wetting branch), whereas a desorption isotherm is measured by drying moist grain in decreasing humidity. Due to hysteresis, the desorption moisture content is always higher than adsorption moisture at the same RH."},
                {"question": "What is water activity (a_w) and how does it relate to grain microbial safety?", "answer": "Water activity is the ratio of vapor pressure of water in grain to pure water at the same temperature (a_w = RH_equilibrium / 100). Mold growth and mycotoxin production cease completely below a_w = 0.65 to 0.70 (approx. 13% to 14% moisture in cereal grains)."},
                {"question": "State the Modified Henderson equation for grain sorption isotherms.", "answer": "The Modified Henderson equation is 1 - RH = exp[-K·(T + C)·M_e^N], where RH is relative humidity in decimal, T is temperature in °C, M_e is dry basis moisture content in %, and K, C, N are crop-specific empirical constants."},
                {"question": "How does temperature affect the equilibrium moisture content of grains?", "answer": "At a constant relative humidity, increasing temperature decreases the equilibrium moisture content of grain because higher thermal energy weakens the adsorptive binding forces of water molecules on grain starch."},
                {"question": "Why are saturated salt solutions used to generate constant relative humidity?", "answer": "A saturated salt solution with excess solute maintains a constant chemical thermodynamic activity of water in the liquid phase, producing a fixed, highly stable vapor pressure and relative humidity in a sealed headspace at a given temperature."}
            ],
            "precautions": [
                "Ensure excess solid salt crystals are visible at the bottom of the solution jars; unsaturated solutions will not maintain target RH.",
                "Never allow liquid salt solution to splash onto the grain basket; chemical contamination invalidates gravimetric results.",
                "Keep desiccator lids greased with silicone vacuum grease to ensure an airtight seal during the 3-week incubation.",
                "Minimize time sample baskets spend outside the desiccator during intermediate weighing to prevent moisture exchange with room air."
            ],
            "limitations": [
                "Static gravimetric equilibration requires 2 to 4 weeks per trial, during which mold can develop at high humidities (RH > 80%).",
                "Addition of anti-fungal agents (e.g. toluene) to prevent mold at high RH can slightly shift sorption thermodynamics.",
                "Evaluates whole intact kernels; cracked or milled grain exhibits faster sorption kinetics and slightly altered isotherms.",
                "Linearized model applies between 15% and 80% RH; extreme humidities (> 85%) exhibit capillary condensation deviations."
            ],
            "quiz": [
                {
                    "question": "What is the critical water activity (a_w) threshold below which storage mold growth is completely suppressed?",
                    "options": ["a_w = 0.95", "a_w = 0.85", "a_w = 0.65 to 0.70", "a_w = 0.20"],
                    "correct": 2,
                    "explanation": "Storage fungi cannot germinate or produce harmful mycotoxins below water activity 0.65 to 0.70 (approx. 13-14% moisture in cereals)."
                },
                {
                    "question": "In a grain silo, if ambient air has a higher relative humidity than the grain's equilibrium RH, what occurs?",
                    "options": ["Grain continues to dry", "Grain reabsorbs moisture from the air, increasing storage spoilage risk", "Grain explodes", "Air temperature drops to absolute zero"],
                    "correct": 1,
                    "explanation": "When ambient air RH exceeds the grain's equilibrium RH, a vapor pressure gradient forces water to transfer into the grain."
                },
                {
                    "question": "What is the phenomenon where desorption EMC is higher than adsorption EMC at identical relative humidity?",
                    "options": ["Capillary cavitation", "Hysteresis", "Sublimation", "Syneresis"],
                    "correct": 1,
                    "explanation": "Sorption hysteresis causes the desorption (drying) curve to sit above the adsorption (wetting) curve."
                },
                {
                    "question": "How does increasing grain temperature at constant relative humidity affect EMC?",
                    "options": ["EMC increases", "EMC decreases", "EMC remains completely unaffected", "EMC doubles instantly"],
                    "correct": 1,
                    "explanation": "Higher temperatures increase thermal kinetic energy, weakening hydrogen bonds and reducing the amount of water held at equilibrium."
                }
            ],
            "settings": ["Test crop: Yellow dent corn", "Incubation temperature: 25.0°C", "Equilibration time: 21 days"],
            "samples": [-2.25, -1.71, -1.17, -0.63, -0.09, 0.45],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🌾", "label": "1. Salt Desiccator Chamber"},
                {"id": "compare", "icon": "📊", "label": "2. Henderson Isotherm Plot"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Temperature & a_w Sandbox"}
            ]
        },
        {
            "number": 22,
            "slug": "thin-layer-grain-drying-kinetics-page-model",
            "title": "Thin-Layer Forced-Air Grain Drying Kinetics & Page Empirical Model Evaluation",
            "shortTitle": "Thin-Layer Drying Kinetics",
            "aim": "Investigate the forced-air thin-layer drying kinetics of agricultural cereal grain, determine moisture ratio decay over time, and evaluate Page model drying parameters.",
            "inputLabel": "Logarithm of Drying Time ln(t)",
            "shortInput": "ln(Time t)",
            "inputUnit": "ln(min)",
            "min": 2.3026,
            "max": 4.4998,
            "step": 0.4394,
            "initial": 3.4012,
            "inputDecimals": 4,
            "rawLabel": "Double Logarithm ln(-ln(MR))",
            "rawUnit": "transformed",
            "rawDecimals": 4,
            "xAxis": "ln(Drying time t in min)",
            "yAxis": "ln(-ln(Moisture ratio MR))",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.4,
            "emptyY": -0.25,
            "targetName": "Page Model Time Exponent n_p",
            "target": "1.2500",
            "refValue": 1.2500,
            "resultUnit": "dimensionless",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ln(-ln(MR)) = n_p · ln(t) + ln(k_p) = 1.2500 · ln(t) - 4.5000",
            "intro": "Artificial thermal drying of grain is essential to safely store crops harvested at high moisture, preventing post-harvest respiration, insect infestation, and fungal spoilage. In deep-bed grain dryers (cross-flow, concurrent-flow, or in-bin radial systems), the drying process is modeled mathematically by summing the performance of successive thin layers of grain. A thin layer is defined as a grain layer one or two kernels thick where drying air temperature, humidity, and velocity remain uniform throughout. Thin-layer drying kinetics are governed by internal moisture diffusion through the endosperm, germ, and pericarp according to Fick's second law. The moisture ratio MR = (M_t - M_e) / (M_0 - M_e) describes the fraction of removable moisture remaining at time t. While Newton's exponential model MR = exp(-k·t) assumes pure surface resistance, agricultural grains exhibit super-exponential diffusion behavior best captured by Page's empirical model: MR = exp(-k_p·t^n_p), where k_p is the drying rate constant and n_p is Page's exponent. Linearizing into ln[-ln(MR)] = n_p·ln(t) + ln(k_p) enables precise parameter estimation. In this laboratory, a laboratory thin-layer drying tunnel with continuous load-cell logging records drying curves across controlled temperatures.",
            "modelExtra": "Evaluated using rough paddy rice (initial moisture 24.5% d.b., equilibrium moisture 9.2% d.b.) dried under forced air at 50°C and 1.2 m/s face velocity.",
            "apparatus": [
                {"name": "Laboratory Thin-Layer Drying Wind Tunnel", "purpose": "Insulated aerodynamic duct delivering precisely controlled temperature, velocity, and humidity."},
                {"name": "Continuous Electronic Strain-Gauge Balance", "purpose": "Suspends the grain tray inside the air duct, recording mass loss every 10 seconds without stopping airflow."},
                {"name": "PID-Controlled Electric Air Heater", "purpose": "Maintains drying air temperature at exactly 50.0°C within ±0.2°C precision."},
                {"name": "Perforated Mesh Monolayer Grain Tray", "purpose": "Holds a single layer of grain kernels (300 g) with 85% open mesh area for unrestricted airflow."},
                {"name": "Hot-Wire Duct Anemometer", "purpose": "Measures face air velocity entering the grain layer with 0.05 m/s precision."},
                {"name": "Chilled-Mirror Relative Humidity Transmitter", "purpose": "Logs drying air psychrometric properties at the test section inlet."}
            ],
            "procedure": [
                {"title": "Drying Tunnel Warm-Up & Stabilization", "text": "Turn on the tunnel blower and PID heater, setting airflow to 1.2 m/s and air temperature to 50.0°C, allowing the empty duct to reach steady thermal equilibrium for 20 minutes."},
                {"title": "Initial Moisture & Tare Setup", "text": "Determine initial grain moisture content M_0 via rapid moisture tester (24.5% d.b.). Tare the suspended perforated tray on the continuous balance."},
                {"title": "Monolayer Grain Loading", "text": "Evenly spread 300.0 g of moist paddy rice in a single kernel layer across the tray, immediately inserting it into the drying air stream and zeroing the timer at t = 0."},
                {"title": "Continuous Mass Loss Acquisition", "text": "Log instantaneous tray mass m(t) at 10, 15, 25, 40, 60, and 90 minutes as moisture evaporates into the conditioned air stream."},
                {"title": "Moisture Ratio Transformation", "text": "Convert instantaneous mass into dry-basis moisture M_t, calculate Moisture Ratio MR = (M_t - M_e) / (M_0 - M_e), and compute the double logarithm ln[-ln(MR)]."},
                {"title": "Page Model Regression", "text": "Plot ln[-ln(MR)] against ln(t), perform linear regression, and extract Page's drying exponent n_p and drying rate constant k_p."}
            ],
            "topics": [
                {"question": "Define the dimensionless Moisture Ratio (MR) in grain drying.", "answer": "Moisture Ratio is defined as MR = (M_t - M_e) / (M_0 - M_e), where M_t is moisture content at time t, M_0 is initial moisture content, and M_e is equilibrium moisture content, representing the unaccomplished fraction of removable water."},
                {"question": "Why does Page's model provide superior fitting compared to Newton's exponential model for agricultural grains?", "answer": "Newton's model (MR = e^(-kt)) assumes a constant surface resistance and uniform internal diffusion. Agricultural seeds are complex composite structures with heterogeneous pericarp and endosperm layers that produce variable diffusion resistances; Page's exponent n_p modifies the time scale to account for this non-Fickian internal moisture movement."},
                {"question": "What is the physical mechanism controlling drying rate during the falling rate period?", "answer": "In agricultural grains, virtually the entire drying process occurs in the falling rate period, where drying is governed by internal liquid and vapor moisture diffusion to the seed surface rather than external convective boundary layer evaporation."},
                {"question": "How does drying air temperature influence the drying rate constant k_p?", "answer": "Higher air temperature dramatically increases k_p in accordance with the Arrhenius equation (k_p = A·e^(-E_a / (R·T))), increasing water molecule thermal kinetic energy and accelerating diffusion through grain tissue."},
                {"question": "What is stress cracking in grain drying and how is it caused?", "answer": "Stress cracking refers to internal fissures that form inside the grain endosperm when high drying temperatures create steep moisture and thermal gradients between the dry outer pericarp and the moist inner core. These cracks cause kernel breakage during subsequent milling."},
                {"question": "What is 'tempering' in multi-pass commercial grain drying?", "answer": "Tempering involves holding hot, partially dried grain in an unventilated holding bin for several hours without airflow, allowing internal moisture gradients to equilibrate as moisture diffuses from the wet center to the dry perimeter, dramatically reducing stress cracking and improving energy efficiency."}
            ],
            "precautions": [
                "Ensure grain is spread in a true monolayer; overlapping kernels create deep-bed temperature gradients that violate thin-layer assumptions.",
                "Maintain continuous airflow during weighing; never remove the tray from the air stream during data logging.",
                "Ensure drying air velocity is sufficient (> 0.5 m/s) to ensure that external boundary layer resistance is negligible compared to internal diffusion.",
                "Do not exceed 55°C when drying seed grain to avoid denaturing seed proteins and destroying germination viability."
            ],
            "limitations": [
                "Page's model is purely empirical; its parameters n_p and k_p do not directly represent fundamental physical transport properties like Fickian diffusivity.",
                "Extrapolation of Page parameters beyond the calibrated temperature and velocity domain can lead to substantial errors.",
                "Assumes constant drying air temperature and relative humidity throughout the test run.",
                "Does not account for kernel shrinkage that occurs during moisture loss, which alters surface area."
            ],
            "quiz": [
                {
                    "question": "What drying stage characterizes virtually the entire drying cycle of cereal grains?",
                    "options": ["Constant rate drying period", "Falling rate drying period", "Sublimation period", "Condensation period"],
                    "correct": 1,
                    "explanation": "Because agricultural grains are diffusion-limited hygroscopic materials, drying occurs almost entirely in the falling rate period."
                },
                {
                    "question": "In the Moisture Ratio equation MR = (M_t - M_e) / (M_0 - M_e), what is the value of MR at t = 0?",
                    "options": ["0.0", "0.5", "1.0", "Infinity"],
                    "correct": 2,
                    "explanation": "At t = 0, M_t = M_0; therefore, MR = (M_0 - M_e) / (M_0 - M_e) = 1.0."
                },
                {
                    "question": "Why is 'tempering' widely practiced in commercial paddy and corn drying?",
                    "options": ["To cool grain for freezing", "To allow internal moisture gradients to equilibrate, preventing stress cracks and kernel breakage", "To increase grain weight with water", "To polish the rice husk"],
                    "correct": 1,
                    "explanation": "Tempering allows moisture from the core to diffuse to the surface during rest periods, preventing stress cracks caused by steep moisture gradients."
                },
                {
                    "question": "If drying air temperature is increased from 40°C to 60°C, how does drying rate respond?",
                    "options": ["Drying rate increases significantly due to higher vapor pressure gradients and diffusivity", "Drying rate drops to zero", "Drying rate is unchanged", "Grain stops drying"],
                    "correct": 0,
                    "explanation": "Higher temperature increases internal moisture diffusivity and creates a much larger water vapor pressure deficit between grain and air."
                }
            ],
            "settings": ["Air temperature: 50.0°C", "Air velocity: 1.2 m/s", "Crop: Rough paddy rice"],
            "samples": [2.3026, 2.7081, 3.2189, 3.6889, 4.0943, 4.4998],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🌾", "label": "1. Thin-Layer Tunnel"},
                {"id": "compare", "icon": "📊", "label": "2. ln[-ln(MR)] vs ln(t)"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Air Temperature Sandbox"}
            ]
        },
        {
            "number": 23,
            "slug": "air-grain-psychrometrics-drying-potential",
            "title": "Moist Air Psychrometrics & Evaporative Drying Potential Across Grain Beds",
            "shortTitle": "Air-Grain Psychrometrics",
            "aim": "Determine the sensible heat transfer, moisture carrying capacity, and psychrometric drying potential of heated air across deep grain beds using psychrometric enthalpy balances.",
            "inputLabel": "Heated Drying Air Dry-Bulb Temperature T_db",
            "shortInput": "Air Temp T_db",
            "inputUnit": "°C",
            "min": 35.0,
            "max": 70.0,
            "step": 7.0,
            "initial": 49.0,
            "inputDecimals": 1,
            "rawLabel": "Drying Potential Evaporative Capacity ΔW",
            "rawUnit": "g/kg",
            "rawDecimals": 2,
            "xAxis": "Drying air temperature T_db (°C)",
            "yAxis": "Evaporative capacity ΔW (g H₂O/kg dry air)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 52.5,
            "emptyY": 17.05,
            "targetName": "Thermal Drying Potential Sensitivity s_dp",
            "target": "0.4200",
            "refValue": 0.4200,
            "resultUnit": "g/(kg·°C)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ΔW = s_dp · T_db + ΔW_0 = 0.4200 · T_db - 5.0000",
            "intro": "Psychrometrics—the thermodynamic study of moist air mixtures—governs all agricultural grain drying, greenhouse climatization, livestock barn ventilation, and cold storage operations. In a convection grain dryer, ambient air is heated sensibly before passing through the crop bed. During sensible heating, the dry-bulb temperature rises while absolute humidity ratio W (mass of water vapor per unit mass of dry air, g/kg) remains constant, causing relative humidity to drop dramatically and expanding the air's vapor pressure deficit. As this warm, dry air flows through moist grain, it undergoes an adiabatic evaporative cooling process along a constant wet-bulb (or constant enthalpy) line on the psychrometric chart: sensible heat from the air supplies the latent heat of vaporization (approx. 2400 kJ/kg H₂O), causing air dry-bulb temperature to fall while humidity ratio increases until the air reaches saturation (or equilibrium with grain moisture). The drying potential evaporative capacity ΔW = W_sat - W_in (g H₂O/kg dry air) represents the maximum water a kilogram of air can absorb in a single pass. In this laboratory investigation, an instrumented psychrometric duct evaluates evaporative drying potential across temperatures from 35°C to 70°C.",
            "modelExtra": "Evaluated at ambient intake air conditions of 20°C dry-bulb and 60% RH (ambient humidity ratio W_in = 8.8 g/kg dry air) across drying temperatures from 35°C to 70°C.",
            "apparatus": [
                {"name": "Psychrometric Air-Conditioning Tunnel", "purpose": "Includes variable-speed fan, electric heating elements, steam humidifier, and measurement stations."},
                {"name": "Precision Aspirated Wet & Dry Bulb Psychrometer", "purpose": "Measures dry-bulb (T_db) and wet-bulb (T_wb) temperatures with 0.1°C matched thermistors."},
                {"name": "Digital Psychrometric Humidity Transmitters", "purpose": "Logs dew point, absolute humidity ratio W, and relative humidity across duct stations."},
                {"name": "Experimental Deep-Bed Grain Column (0.5 m Depth)", "purpose": "Standard test bed of moist corn through which conditioned air percolates."},
                {"name": "Differential Pressure Transmitter across Grain Bed", "purpose": "Measures airflow static resistance and Shedd's curve pressure drop (Pa/m)."},
                {"name": "Digital Orifice Flowmeter", "purpose": "Measures total air mass flow rate m_dot_air (kg/s) with 1.0% accuracy."}
            ],
            "procedure": [
                {"title": "Ambient Air Baseline Acquisition", "text": "Record ambient air dry-bulb temperature (20.0°C) and relative humidity (60.0%), calculating baseline humidity ratio W_in = 8.80 g H₂O/kg dry air from psychrometric relations."},
                {"title": "Duct Heating & Airflow Stabilization", "text": "Set duct air velocity to 0.4 m/s through the grain column, powering the heating stage to achieve initial dry-bulb temperature T_db = 35.0°C."},
                {"title": "Sensible Heating Verification", "text": "Verify that absolute humidity ratio W upstream of the grain bed matches ambient W_in, confirming pure sensible heating without moisture addition."},
                {"title": "Exhaust Psychrometric Logging", "text": "Measure exhaust air wet-bulb and dry-bulb temperatures downstream of the grain bed, determining saturation humidity ratio W_sat at the adiabatic wet-bulb temperature."},
                {"title": "Temperature Stepping", "text": "Increment heater temperature in five uniform stages to 42, 49, 56, 63, and 70°C, recording steady-state inlet and outlet psychrometric states for each run."},
                {"title": "Drying Potential Linear Regression", "text": "Calculate evaporative capacity ΔW = W_sat - W_in for each temperature, plot ΔW versus T_db, and determine the thermal drying sensitivity gradient s_dp."}
            ],
            "topics": [
                {"question": "What is the difference between dry-bulb, wet-bulb, and dew-point temperatures?", "answer": "Dry-bulb temperature is the true thermodynamic temperature of moist air. Wet-bulb temperature is the lowest temperature attainable by adiabatic evaporative cooling of water into air. Dew-point temperature is the temperature at which moist air must be cooled at constant pressure to reach 100% saturation and initiate condensation."},
                {"question": "Describe the psychrometric path of air passing through a grain dryer.", "answer": "The process has two stages: (1) Sensible heating through the heater, moving horizontally to the right on the psychrometric chart (increasing T_db at constant W), followed by (2) Adiabatic evaporative cooling through the grain bed, moving upward and to the left along a constant wet-bulb/enthalpy line as sensible heat converts into latent heat of vaporization."},
                {"question": "How does heating ambient air increase its drying capacity?", "answer": "Heating air increases its saturation vapor pressure exponentially. While the absolute moisture W remains constant during heating, the relative humidity drops sharply, creating a massive vapor pressure deficit between the dry air and moist grain that accelerates evaporation."},
                {"question": "What is the latent heat of vaporization of water in grain compared to free water?", "answer": "At free water surfaces, latent heat of vaporization is approx. 2400 kJ/kg at 25°C. In grains, water is bound by adsorptive forces to starch and protein; at low moisture contents, latent heat can be 10% to 25% higher (up to 2800 kJ/kg), requiring additional thermal energy to vaporize."},
                {"question": "Explain Shedd's curves in agricultural grain aeration.", "answer": "Shedd's curves (ASABE D272) plot the static pressure drop per unit depth of grain (Pa/m) against airflow velocity (m³/s per m² of floor area). They are used to calculate the fan static pressure required to force drying air through deep grain beds."},
                {"question": "What is the consequence of overdrying grain in the bottom layers of a bin dryer?", "answer": "In deep-bed drying, a drying front moves upward slowly. The bottom grain near the hot air inlet dries to extremely low moisture (< 8%) before the top layer begins to dry, causing energy waste, kernel cracking, and economic loss from selling grain below commercial market weight."}
            ],
            "precautions": [
                "Ensure wet-bulb wicks are clean, saturated with distilled water, and aspirated at air velocities > 3.5 m/s to prevent radiation errors.",
                "Allow thermal equilibrium to stabilize for at least 15 minutes after adjusting electric heater settings.",
                "Verify airtight duct seals; ambient air infiltration downstream of the heater skews psychrometric mass balances.",
                "Do not exceed 70°C drying temperature to avoid scorch and thermal degradation of grain endosperm."
            ],
            "limitations": [
                "Assumes ideal adiabatic drying conditions; heat losses through uninsulated duct walls cause slight departures from constant enthalpy lines.",
                "As grain moisture drops below 14%, grain water activity drops, preventing exhaust air from reaching 100% saturation.",
                "Constant enthalpy model neglects the sensible heating of the grain kernel mass itself during initial startup.",
                "Psychrometric chart equations assume standard atmospheric pressure (101.325 kPa); elevation adjustments are required at high altitudes."
            ],
            "quiz": [
                {
                    "question": "What psychrometric line does air follow as it evaporates moisture adiabatically from a grain bed?",
                    "options": ["Constant dry-bulb temperature line", "Constant wet-bulb / enthalpy line", "Constant relative humidity line", "Vertical line"],
                    "correct": 1,
                    "explanation": "Adiabatic evaporation converts sensible heat directly into latent heat, maintaining constant total enthalpy and wet-bulb temperature."
                },
                {
                    "question": "During sensible heating of air through an electric heater without moisture addition, what parameter remains constant?",
                    "options": ["Relative humidity", "Dry-bulb temperature", "Humidity ratio (absolute moisture W in g/kg)", "Dew-point depression"],
                    "correct": 2,
                    "explanation": "Sensible heating changes temperature only; no water is added or removed, so absolute humidity ratio W remains constant."
                },
                {
                    "question": "If drying air enters at W_in = 8.8 g/kg and exits at W_sat = 21.4 g/kg, what is the moisture carried per kg of dry air?",
                    "options": ["8.8 g/kg", "12.6 g/kg", "21.4 g/kg", "30.2 g/kg"],
                    "correct": 1,
                    "explanation": "Moisture carrying capacity ΔW = W_sat - W_in = 21.4 - 8.8 = 12.6 g H₂O/kg dry air."
                },
                {
                    "question": "What engineering chart is used to determine pressure drop across agricultural grain beds?",
                    "options": ["Mollier diagram", "Shedd's curves", "Moody diagram", "Smith chart"],
                    "correct": 1,
                    "explanation": "Shedd's curves (ASABE D272) define the airflow resistance and static pressure drop per meter of grain depth."
                }
            ],
            "settings": ["Ambient inlet: 20°C, 60% RH (W = 8.8 g/kg)", "Grain bed depth: 0.50 m", "Face velocity: 0.40 m/s"],
            "samples": [35.0, 42.0, 49.0, 56.0, 63.0, 70.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🌾", "label": "1. Psychrometric Tunnel"},
                {"id": "compare", "icon": "📊", "label": "2. ΔW vs Temperature Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Air Enthalpy Sandbox"}
            ]
        },
        {
            "number": 24,
            "slug": "aerodynamic-terminal-velocity-pneumatic-separation",
            "title": "Aerodynamic Terminal Velocity & Pneumatic Separation of Grains and Chaff",
            "shortTitle": "Grain Terminal Velocity",
            "aim": "Measure the aerodynamic terminal suspension velocity of agricultural grain kernels across varying seed equivalent diameters using a vertical wind column elutriator.",
            "inputLabel": "Equivalent Kernel Particle Diameter D_p",
            "shortInput": "Diameter D_p",
            "inputUnit": "mm",
            "min": 2.5,
            "max": 6.0,
            "step": 0.7,
            "initial": 3.9,
            "inputDecimals": 1,
            "rawLabel": "Terminal Suspension Velocity v_t",
            "rawUnit": "m/s",
            "rawDecimals": 3,
            "xAxis": "Kernel diameter D_p (mm)",
            "yAxis": "Terminal velocity v_t (m/s)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 4.25,
            "emptyY": 7.438,
            "targetName": "Terminal Velocity Scaling Slope k_v",
            "target": "1.7500",
            "refValue": 1.7500,
            "resultUnit": "(m/s)/mm",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "v_t = k_v · D_p = 1.7500 · D_p",
            "intro": "Aerodynamic properties of agricultural seeds and biological materials govern the design of pneumatic conveyors, aspirators, combine cleaning shoes, air-screen grain cleaners, and fluidized bed dryers. The terminal velocity (v_t) of a particle is defined as the steady vertical velocity of an upward airstream that suspends the particle in stationary equilibrium, where the upward aerodynamic drag force F_d exactly equals the downward gravitational force F_g minus buoyant force F_b: F_d = C_d·A_p·(ρ_a·v_t² / 2) = m·g·(1 - ρ_a / ρ_p). Because drag depends on particle projected area, density, shape, and surface roughness, agricultural seeds exhibit distinct terminal velocities that enable clean pneumatic separation from lighter weed seeds, chaff, straw pieces, and dust. For intermediate Reynolds numbers characteristic of cereal seed suspensions (Re ≈ 1000 to 4000), terminal velocity scales near-linearly with equivalent seed diameter D_p and the square root of particle density. In this laboratory experiment, a vertical transparent acrylic wind column elutriator with variable-speed blower and precision hot-wire anemometer determines the exact floating terminal velocity across six seed size fractions.",
            "modelExtra": "Evaluated using calibrated fractions of cereal wheat kernels (particle density ρ_p = 1320 kg/m³) across equivalent diameters from 2.5 mm to 6.0 mm in air at 20°C.",
            "apparatus": [
                {"name": "Vertical Transparent Aerodynamic Elutriator Column", "purpose": "Clear acrylic vertical duct (15 cm diameter, 1.5 m height) with wire mesh suspension grid."},
                {"name": "Variable-Frequency Centrifugal Air Blower", "purpose": "Supplies upward airflow with continuous velocity control from 2.0 to 14.0 m/s."},
                {"name": "Multi-Point Hot-Wire Anemometer Probe", "purpose": "Measures centerline air velocity at the seed suspension plane with 0.05 m/s accuracy."},
                {"name": "Digital Sieve Sizer & Micrometer Caliper", "purpose": "Classifies wheat kernels into narrow geometric equivalent diameter fractions."},
                {"name": "Air Flow Straightener Honeycomb Section", "purpose": "Eliminates swirl, eddies, and non-uniform turbulence ahead of the suspension zone."},
                {"name": "High-Speed Video Camera (240 FPS)", "purpose": "Records particle floating stability, orientation, and rotational tumbling dynamics."}
            ],
            "procedure": [
                {"title": "Seed Fraction Classification", "text": "Screen certified wheat seed through precision round-hole sieves into six distinct equivalent diameter fractions: 2.5, 3.2, 3.9, 4.6, 5.3, and 6.0 mm, measuring tri-axial dimensions with calipers."},
                {"title": "Elutriator Column Zeroing", "text": "Inspect the vertical column, zero the hot-wire anemometer, and ensure honeycomb flow straighteners are clean and free of dust."},
                {"title": "Initial Grain Fraction Introduction", "text": "Place 10 kernels of the 2.5 mm diameter fraction onto the wire mesh screen at the base of the transparent column."},
                {"title": "Terminal Suspension Adjustment", "text": "Slowly increase blower frequency until the kernels lift off the screen and hover in stable floating suspension at the column mid-height without exiting the top."},
                {"title": "Air Velocity Logging", "text": "Record the vertical air velocity v_t (m/s) from the anemometer probe at the suspension plane, repeating 5 times to compute mean terminal velocity."},
                {"title": "Diameter Stepping & Regression", "text": "Repeat the suspension procedure for the remaining five diameter fractions up to 6.0 mm, plot v_t versus D_p, and determine the aerodynamic scaling slope k_v."}
            ],
            "topics": [
                {"question": "Define terminal velocity in the context of agricultural pneumatic separation.", "answer": "Terminal velocity is the upward air velocity required to balance the downward gravitational force acting on a seed, causing the particle to remain stationary in suspension (net vertical force = 0)."},
                {"question": "How is aerodynamic drag formulated for an irregularly shaped grain kernel?", "answer": "Drag force is F_d = 0.5·C_d·ρ_a·A_p·v_t², where C_d is the drag coefficient (dependent on particle shape and Reynolds number), ρ_a is air density, A_p is projected cross-sectional area, and v_t is relative velocity."},
                {"question": "Why do grain kernels tumble and rotate when suspended in an elutriator?", "answer": "Seeds are asymmetric non-spherical bodies whose center of mass does not coincide with their center of aerodynamic pressure, producing aerodynamic pitching and yawing moments that cause continuous rotational tumbling in turbulent airflow."},
                {"question": "Explain how an air-screen cleaner uses differences in terminal velocity.", "answer": "An aspirator duct passes upward air through a falling curtain of grain. Air velocity is set above the terminal velocity of chaff (3 m/s) but below that of grain (9 m/s); chaff is entrained and carried away, while clean grain falls downward into the screen grading shoe."},
                {"question": "How does moisture content affect seed terminal velocity?", "answer": "Moist grain has higher mass and swells in volume, altering both density and projected area. Generally, increasing grain moisture increases terminal velocity, requiring higher air velocities in cleaning equipment."},
                {"question": "What is the equivalent diameter D_p of a tri-axial ellipsoid seed?", "answer": "Geometric equivalent diameter is D_p = (L·W·T)^(1/3), the geometric mean of length (L), width (W), and thickness (T), representing the diameter of an equivalent sphere with identical volume."}
            ],
            "precautions": [
                "Ensure airflow in the vertical column is completely laminarized by honeycomb straighteners to prevent wall downdrafts.",
                "Introduce kernels one fraction at a time to prevent inter-particle collisions that disrupt suspension equilibrium.",
                "Record air barometric pressure and temperature to correct for air density variations.",
                "Ensure anemometer probe is positioned exactly at the vertical floating height of the suspended seeds."
            ],
            "limitations": [
                "Individual kernels within the same sieve fraction exhibit minor shape and density variations, producing a ±5% velocity band.",
                "Wall proximity effects in 15 cm ducts slightly alter velocity profiles compared to open field airflow.",
                "High-speed tumbling alters instantaneous projected area, requiring time-averaged velocity measurements.",
                "Cannot separate weed seeds that share identical aerodynamic terminal velocity with the crop grain."
            ],
            "quiz": [
                {
                    "question": "When a wheat kernel is suspended stationary in a vertical air column, what is the net vertical force on the kernel?",
                    "options": ["Equal to its weight", "Equal to double its weight", "Zero (aerodynamic drag equals gravitational weight minus buoyancy)", "Negative infinity"],
                    "correct": 2,
                    "explanation": "At terminal suspension velocity, upward aerodynamic drag exactly balances the downward gravitational force, yielding net force = 0."
                },
                {
                    "question": "If wheat has a terminal velocity of 9.0 m/s and chaff has 2.5 m/s, what aspirator air velocity achieves clean separation?",
                    "options": ["1.0 m/s", "5.5 m/s", "12.0 m/s", "25.0 m/s"],
                    "correct": 1,
                    "explanation": "An intermediate air velocity of 5.5 m/s exceeds the chaff terminal velocity (blowing it out) while remaining safely below the wheat terminal velocity."
                },
                {
                    "question": "What is the geometric equivalent diameter D_p of a seed with L = 6 mm, W = 3 mm, and T = 2 mm?",
                    "options": ["2.0 mm", "3.3 mm", "4.5 mm", "6.0 mm"],
                    "correct": 1,
                    "explanation": "D_p = (6 × 3 × 2)^(1/3) = (36)^(1/3) = 3.30 mm."
                },
                {
                    "question": "If the terminal velocity slope is k_v = 1.75 (m/s)/mm, what is the terminal velocity of a 4.0 mm kernel?",
                    "options": ["4.0 m/s", "5.25 m/s", "7.0 m/s", "10.5 m/s"],
                    "correct": 2,
                    "explanation": "v_t = 1.75 × 4.0 mm = 7.00 m/s."
                }
            ],
            "settings": ["Column diameter: 15.0 cm", "Air temp: 20°C (ρ_a = 1.204 kg/m³)", "Crop: Hard red winter wheat"],
            "samples": [2.5, 3.2, 3.9, 4.6, 5.3, 6.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🌾", "label": "1. Vertical Air Elutriator"},
                {"id": "compare", "icon": "📊", "label": "2. v_t vs Diameter Plot"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Suspension Velocity Sandbox"}
            ]
        },
        {
            "number": 25,
            "slug": "physical-gravimetric-properties-agricultural-grains",
            "title": "Physical & Gravimetric Properties: Bulk Density, Porosity & Sphericity of Seeds",
            "shortTitle": "Grain Gravimetric Properties",
            "aim": "Determine the true density, bulk density, porosity, thousand-grain mass, and sphericity of cereal grains and verify the linear mass-volume relation in bulk storage.",
            "inputLabel": "Standard Bulk Volume V_b",
            "shortInput": "Volume V_b",
            "inputUnit": "mL",
            "min": 100.0,
            "max": 500.0,
            "step": 80.0,
            "initial": 260.0,
            "inputDecimals": 1,
            "rawLabel": "Measured Bulk Grain Mass m_b",
            "rawUnit": "g",
            "rawDecimals": 2,
            "xAxis": "Bulk volume V_b (mL)",
            "yAxis": "Bulk grain mass m_b (g)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 300.0,
            "emptyY": 235.5,
            "targetName": "Bulk Density ρ_b",
            "target": "0.7850",
            "refValue": 0.7850,
            "resultUnit": "g/mL",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "m_b = ρ_b · V_b = 0.7850 · V_b",
            "intro": "Physical and gravimetric properties of agricultural seeds—including bulk density (test weight), true particle density, porosity, thousand-grain weight (TGW), and sphericity—are primary engineering parameters in bulk storage silo sizing, aeration resistance modeling, commercial grain grading, and pneumatic handling. Bulk density ρ_b is the mass of grain divided by the total volume occupied including inter-granular air voids, measured in standard bushel testers or Winchester volume cylinders. True density ρ_t is the density of the individual grain kernel excluding interstitial pores, measured via gas pycnometry or liquid displacement using non-wetting fluids (toluene or kerosene). Inter-granular porosity ε = (1 - ρ_b / ρ_t) × 100% defines the void fraction available for airflow during aeration and drying. Sphericity Φ = (L·W·T)^(1/3) / L expresses the degree to which an ellipsoidal grain kernel resembles a true sphere. In this laboratory investigation, standardized volumetric measures quantify the linear relationship m_b = ρ_b·V_b across graduated volumes from 100 to 500 mL.",
            "modelExtra": "Evaluated using clean seed wheat at 12.5% moisture (true kernel density ρ_t = 1.340 g/mL, porosity ε = 41.4%) across standardized graduated cylinders.",
            "apparatus": [
                {"name": "Standard Winchester Bushel & Funnel Measure (1-Liter)", "purpose": "Ensures standardized free-fall dropping height and packing density in bulk volume cylinders."},
                {"name": "Gas Displacement Helium Pycnometer", "purpose": "Measures true solid volume and true density of grain kernels with 0.001 g/cm³ accuracy."},
                {"name": "Electronic Digital Analytical Balance (0.01 g)", "purpose": "Weighs bulk grain samples and thousand-grain lots with high precision."},
                {"name": "Digital Vernier Micrometer Caliper (0.01 mm)", "purpose": "Measures principal tri-axial dimensions (length L, width W, thickness T) of 100 kernels."},
                {"name": "Electronic Seed Counter (Automatic Carousel)", "purpose": "Counts exactly 1000 sound kernels for Thousand-Grain Weight (TGW) determination."},
                {"name": "Graduated Glass Cylinders (100 to 500 mL)", "purpose": "Measures bulk volumes under standardized strike-off filling."}
            ],
            "procedure": [
                {"title": "Funnel Hopper Standardization", "text": "Position the standard filling funnel 5.0 cm above the graduated cylinder, ensuring the discharge shutter is centered and level."},
                {"title": "Initial 100 mL Bulk Filling", "text": "Pour wheat into the funnel, open the shutter to allow free-fall filling into the 100 mL cylinder until overflowing, and strike off excess grain level with the rim using a wooden straightedge."},
                {"title": "Bulk Mass Determination", "text": "Weigh the filled cylinder, subtract tare mass, and record bulk grain mass m_b (g) for V_b = 100.0 mL."},
                {"title": "Volume Incrementation", "text": "Repeat standardized filling across cylinders of 180, 260, 340, 420, and 500 mL, recording mass m_b for each volume."},
                {"title": "True Density & Porosity Determination", "text": "Place 50 g of wheat into the helium pycnometer to measure true volume and calculate true density ρ_t, then compute porosity ε = (1 - ρ_b / ρ_t) × 100%."},
                {"title": "Linear Bulk Density Regression", "text": "Plot bulk mass m_b versus volume V_b, perform linear regression through the origin, and determine the bulk density slope ρ_b."}
            ],
            "topics": [
                {"question": "Distinguish between bulk density and true kernel density.", "answer": "Bulk density ρ_b is the mass of grain divided by the total bulk volume it occupies (including interstitial air pores between kernels), typically 750 to 820 kg/m³ for wheat. True density ρ_t is the mass of the solid kernel divided by its true volume excluding all air spaces, typically 1250 to 1400 kg/m³."},
                {"question": "How is grain porosity calculated from densities?", "answer": "Inter-granular porosity is calculated as ε = (1 - ρ_b / ρ_t) × 100%, representing the percentage of total bulk volume occupied by void air spaces through which ventilation and drying air can flow."},
                {"question": "What is 'test weight' in commercial grain marketing?", "answer": "Test weight is the bulk density expressed in pounds per bushel (lb/bu) or kg/hL, serving as a primary commercial grading factor indicating grain maturity, starch packing density, and milling flour yield."},
                {"question": "Why is toluene or helium used instead of water to measure true grain volume?", "answer": "Water is rapidly absorbed by dry grain through capillary pores, causing swelling and inaccurate volume readings. Helium gas penetrates microscopic surface crevices without absorbing, while toluene is a non-polar organic liquid that does not wet starch."},
                {"question": "What is sphericity Φ and why is it important in agricultural engineering?", "answer": "Sphericity is Φ = (L·W·T)^(1/3) / L. High sphericity (> 0.8) seeds roll easily in chutes and metering discs, whereas low sphericity seeds (oats, sunflower) require special cell shapes and steeper hopper slopes to prevent bridging."},
                {"question": "How does moisture content affect the bulk density of cereal grains?", "answer": "Increasing moisture causes grain kernels to swell in volume faster than they gain water mass, and increases surface friction that prevents tight packing; hence, bulk density decreases as moisture increases."}
            ],
            "precautions": [
                "Always use a standard funnel with uniform drop height; shaking or tapping the cylinder compacts grain and falsely elevates bulk density by up to 8%.",
                "Use a single, smooth stroke of the straightedge held at a 45° angle to strike off grain flush with the container rim.",
                "Ensure seed samples are clean and free of chaff, broken kernels, and weed seeds before density measurements.",
                "Verify balance calibration using certified analytical check weights before each run."
            ],
            "limitations": [
                "Laboratory small-cylinder bulk densities are slightly lower than deep silo densities where thousands of tons of overburden compact the grain.",
                "Grain packing density varies depending on whether grain is filled via central spout versus mechanical spreaders.",
                "Helium pycnometers measure internal closed pores differently than liquid displacement methods.",
                "Tri-axial dimensions vary across individual kernels; at least 100 kernels must be averaged for reliable sphericity."
            ],
            "quiz": [
                {
                    "question": "If a grain sample has bulk density ρ_b = 0.785 g/cm³ and true density ρ_t = 1.340 g/cm³, what is its porosity?",
                    "options": ["21.4%", "41.4%", "58.6%", "78.5%"],
                    "correct": 1,
                    "explanation": "Porosity ε = (1 - ρ_b / ρ_t) × 100% = (1 - 0.785 / 1.340) × 100% = (1 - 0.5858) × 100% = 41.42%."
                },
                {
                    "question": "What happens to the measured bulk density if an operator taps and shakes the measuring cylinder during filling?",
                    "options": ["Bulk density decreases", "Bulk density increases significantly due to artificial particle settling and packing", "Bulk density drops to zero", "Porosity increases to 100%"],
                    "correct": 1,
                    "explanation": "Vibration settles smaller kernels into void spaces, packing grain tighter and increasing measured bulk density."
                },
                {
                    "question": "What is the standard volume of a Winchester bushel?",
                    "options": ["10.0 liters", "21.5 liters", "35.24 liters (2150.42 in³)", "100.0 liters"],
                    "correct": 2,
                    "explanation": "A standard US Winchester bushel equals 35.239 liters (2150.42 cubic inches)."
                },
                {
                    "question": "If bulk density is 0.785 g/mL, what is the mass of 400 mL of wheat?",
                    "options": ["157.0 g", "314.0 g", "392.5 g", "509.5 g"],
                    "correct": 1,
                    "explanation": "Mass m_b = ρ_b × V_b = 0.785 g/mL × 400 mL = 314.0 g."
                }
            ],
            "settings": ["Test grain: Hard red winter wheat", "True density ρ_t: 1.340 g/mL", "Grain moisture: 12.5% w.b."],
            "samples": [100.0, 180.0, 260.0, 340.0, 420.0, 500.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🌾", "label": "1. Winchester Volume Cylinder"},
                {"id": "compare", "icon": "📊", "label": "2. Mass vs Volume Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Density & Porosity Sandbox"}
            ]
        },
        {
            "number": 26,
            "slug": "grain-internal-friction-angle-of-repose",
            "title": "Static & Dynamic Angle of Repose and Grain-on-Surface Friction Coefficients",
            "shortTitle": "Angle of Repose & Friction",
            "aim": "Measure the static and dynamic angle of repose of agricultural grains using a circular heaping platform and determine grain-on-metal sliding friction coefficients on a tilting plane.",
            "inputLabel": "Circular Heaping Platform Base Radius R",
            "shortInput": "Radius R",
            "inputUnit": "cm",
            "min": 10.0,
            "max": 35.0,
            "step": 5.0,
            "initial": 20.0,
            "inputDecimals": 1,
            "rawLabel": "Conical Grain Heap Height H",
            "rawUnit": "cm",
            "rawDecimals": 2,
            "xAxis": "Platform base radius R (cm)",
            "yAxis": "Conical heap height H (cm)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 22.5,
            "emptyY": 12.99,
            "targetName": "Tangent of Angle of Repose tan(θ)",
            "target": "0.5774",
            "refValue": 0.5774,
            "resultUnit": "dimensionless",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "H = tan(θ) · R = 0.5774 · R",
            "intro": "The angle of repose and surface friction coefficients of bulk granular agricultural products govern the structural design of storage silos, self-emptying hopper bottoms, grain chutes, conveyor spouts, and front-end loader buckets. The angle of repose θ is the maximum angle of slope at which loose, cohesionless bulk material will remain stationary without sliding down the conical pile face. It is directly related to the internal friction angle of the grain mass: tan θ = μ_internal. When grain is poured freely onto a circular horizontal platform with a retained boundary rim, the excess grain rolls over the edge, forming a stable natural cone of height H and base radius R such that H = R·tan θ. The dynamic (emptying) angle of repose is similarly evaluated by draining grain through an orifice at the bottom of a bin. Furthermore, the external friction coefficient μ_s = tan α (where α is the angle of inclination of a tilting steel plate at which grain begins to slide) defines the minimum valley angle required for self-cleaning gravity discharge hoppers (typically 40° to 50° for galvanized sheet steel). In this test, an adjustable circular platform and tilting friction plane evaluate repose geometry.",
            "modelExtra": "Evaluated using dry clean wheat grain on a circular retained platform (target angle of repose θ = 30.0°, tan 30° = 0.5774).",
            "apparatus": [
                {"name": "Circular Base Grain Repose Platform Set", "purpose": "Interchangeable circular acrylic disks with base radii from 10 to 35 cm and sharp overflow edges."},
                {"name": "Overhead Central Gravity Discharge Funnel", "purpose": "Pours grain vertically into the center of the platform from a fixed drop height."},
                {"name": "Vernier Height Gauge with Point Tip", "purpose": "Measures the central peak height H of the conical grain pile with 0.1 mm precision."},
                {"name": "Tilting Plate Friction Apparatus", "purpose": "Inclinable plane with galvanized steel, stainless steel, and rubber surfaces and digital protractor."},
                {"name": "Electronic Angle Inclinometer (0.1°)", "purpose": "Measures angle of inclination α at which grain mass begins sliding."},
                {"name": "Grain Catch Pan & Sieve", "purpose": "Collects overflow grain for re-circulation."}
            ],
            "procedure": [
                {"title": "Platform Leveling & Funnel Centering", "text": "Mount the 10.0 cm radius circular platform on the rigid test base, verifying horizontal level with a bubble spirit level. Center the discharge funnel 10 cm above the platform."},
                {"title": "Grain Heap Formation", "text": "Fill the funnel with clean wheat, release the bottom gate, and allow grain to pour continuously until excess grain rolls off all sides and a stable symmetrical cone is formed."},
                {"title": "Peak Height Measurement", "text": "Carefully lower the vernier height gauge point to touch the exact central apex of the conical grain pile, recording cone height H (cm)."},
                {"title": "Radius Stepping", "text": "Repeat the conical formation on circular platforms of 15, 20, 25, 30, and 35 cm radius, measuring cone height H for each base radius."},
                {"title": "Tilting Plate Friction Test", "text": "Place a bottomless wooden box filled with grain onto the horizontal galvanized steel plate, slowly elevating the plate with the lead screw until the box begins sliding, logging the friction angle α."},
                {"title": "Repose Tangent Linear Regression", "text": "Plot cone height H against radius R, perform linear regression through the origin, and determine the slope tan θ to calculate the angle of repose θ = arctan(slope)."}
            ],
            "topics": [
                {"question": "Distinguish between the static (filling) and dynamic (emptying) angle of repose.", "answer": "The static (filling or piling) angle of repose is formed when grain is poured onto a flat surface to form a cone. The dynamic (emptying or funneling) angle of repose is formed when grain is drained from the bottom orifice of a bin, leaving an inverted conical crater. The dynamic angle is typically 2° to 5° steeper than the static angle."},
                {"question": "How does grain moisture content affect the angle of repose?", "answer": "Increasing moisture content increases surface capillary adhesion and surface stickiness between kernels, significantly increasing the angle of repose (e.g. wheat angle increases from 28° at 10% moisture to over 38° at 22% moisture)."},
                {"question": "Why must hopper bottom slope angles exceed the grain friction angle?", "answer": "To ensure 100% complete cleanout by gravity without mechanical shoveling, hopper valley angles must exceed the grain-on-hopper material friction angle by at least 10° to 15° (typically 45° to 60° for galvanized steel)."},
                {"question": "What is 'grain bridging' in storage bins and what causes it?", "answer": "Bridging occurs when kernels lock together by inter-particle friction and cohesion to form a rigid structural dome across the hopper opening, preventing gravity discharge despite an open gate. It is caused by high moisture, fines/trash, small discharge orifices, or shallow hopper slopes."},
                {"question": "How does surface roughness of the chute material affect grain sliding velocity?", "answer": "Rough surfaces (unpolished rusty steel, rough plywood) have high friction coefficients (μ_s > 0.5), requiring steep chute angles and reducing grain flow velocity. Smooth polished stainless steel or UHMW polyethylene has low friction (μ_s < 0.25), facilitating rapid sliding at gentle slopes."},
                {"question": "What is the relation between angle of repose and Rankine's earth pressure theory in silos?", "answer": "In silo design (Rankine and Janssen theories), the lateral-to-vertical pressure ratio is k = (1 - sin φ) / (1 + sin φ), where φ is the internal friction angle, closely approximated by the angle of repose θ."},
            ],
            "precautions": [
                "Pour grain smoothly without pausing; pulsating flow creates stair-stepped irregularities on the conical heap face.",
                "Avoid vibrating the test bench; floor vibrations shake the heap, causing premature avalanching and falsely lowering the angle of repose.",
                "Ensure the height gauge point touches the peak gently without plunging into the loose grain apex.",
                "Clean the tilting friction plate with solvent before testing to remove oil films and dust."
            ],
            "limitations": [
                "Small laboratory platforms (R < 10 cm) exhibit edge effects where individual kernel size forms a significant fraction of radius.",
                "Angle of repose assumes free-flowing, cohesionless grain; cohesive milled flours form vertical cliffs rather than smooth cones.",
                "Laboratory heaps represent uncompacted grain; deep silo pressures increase effective internal friction angles.",
                "Moisture migration during prolonged testing can alter surface stickiness."
            ],
            "quiz": [
                {
                    "question": "If the slope of the H versus R regression line is 0.5774, what is the angle of repose θ?",
                    "options": ["15.0°", "30.0°", "45.0°", "60.0°"],
                    "correct": 1,
                    "explanation": "θ = arctan(0.5774) = 30.0°."
                },
                {
                    "question": "Why is the dynamic (emptying) angle of repose typically steeper than the filling angle?",
                    "options": ["Because of air cooling", "Because grain kernels interlocking during discharge must overcome static interlocking friction", "Because grain gains mass", "Due to magnetic attraction"],
                    "correct": 1,
                    "explanation": "During emptying, moving kernels interlock against stationary boundary kernels, creating additional shear resistance that steepens the crater angle."
                },
                {
                    "question": "What minimum hopper bottom slope is typically specified for self-cleaning grain discharge chutes on galvanized steel?",
                    "options": ["10° to 15°", "20° to 25°", "45° to 50°", "85° to 90°"],
                    "correct": 2,
                    "explanation": "Hopper slopes of 45° to 50° exceed the static friction angle of cereal grains on steel (typically 25° to 35°), ensuring free gravity flow."
                },
                {
                    "question": "How does increasing moisture content affect grain angle of repose?",
                    "options": ["Angle of repose decreases", "Angle of repose increases significantly due to capillary adhesion", "Angle of repose drops to zero", "Angle of repose is unaffected"],
                    "correct": 1,
                    "explanation": "Higher moisture increases surface liquid bridging and stickiness between kernels, increasing internal friction and steepening the angle of repose."
                }
            ],
            "settings": ["Crop: Clean wheat (12.5% moisture)", "Target repose angle θ: 30.0°", "Drop height: 10.0 cm"],
            "samples": [10.0, 15.0, 20.0, 25.0, 30.0, 35.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🌾", "label": "1. Conical Heap Platform"},
                {"id": "compare", "icon": "📊", "label": "2. Height vs Radius Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Friction & Repose Sandbox"}
            ]
        },
        {
            "number": 27,
            "slug": "hammer-mill-size-reduction-rittinger-bond-laws",
            "title": "Hammer Mill Size Reduction, Sieve Fineness Modulus & Bond's Comminution Law",
            "shortTitle": "Hammer Mill Size Reduction",
            "aim": "Determine the specific electrical grinding energy, particle size distribution, and fineness modulus of ground grain in a hammer mill, and calibrate Bond's comminution law.",
            "inputLabel": "Comminution Size Parameter 1 / √d_p",
            "shortInput": "1/√d_p",
            "inputUnit": "mm^-0.5",
            "min": 0.5,
            "max": 2.0,
            "step": 0.3,
            "initial": 1.1,
            "inputDecimals": 2,
            "rawLabel": "Specific Grinding Energy E_s",
            "rawUnit": "kWh/t",
            "rawDecimals": 3,
            "xAxis": "Size parameter 1/√d_p (mm^-0.5)",
            "yAxis": "Specific energy E_s (kWh/t)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 1.25,
            "emptyY": 6.0,
            "targetName": "Bond Work Index Scaling Factor K_b",
            "target": "4.8000",
            "refValue": 4.8000,
            "resultUnit": "kWh·mm^0.5/t",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "E_s = K_b · (1 / √d_p) = 4.8000 · (1 / √d_p)",
            "intro": "Size reduction (comminution) of agricultural cereal grains (corn, barley, sorghum) is universally practiced in animal feed manufacturing to increase surface area, improve digestive enzyme accessibility, and enhance feed conversion efficiency in livestock and poultry. The hammer mill is the primary industrial comminution machine in feed mills, reducing particle size through high-speed impact between swinging hardened steel hammers (peripheral tip speeds 60 to 90 m/s) and grain kernels, supplemented by attrition against a perforated cylindrical screen. The energy required for mechanical size reduction is governed by classical comminution laws: Rittinger's law states that energy is proportional to the new surface area created (E ∝ 1/d_p); Kick's law states that energy is proportional to the reduction ratio (E ∝ ln(d_initial / d_p)); while Bond's third law of comminution states that energy scales inversely with the square root of particle diameter: E_s = 10·W_i·(1/√d_p - 1/√d_initial) ≈ K_b·(1/√d_p). The ground feed particle size distribution and uniform fineness modulus (FM) are evaluated using standard Tyler sieve shakers in accordance with ASABE Standard S319. In this laboratory investigation, an instrumented pilot hammer mill with digital power analyzer grinds corn through varying screen sizes to calibrate Bond's work factor.",
            "modelExtra": "Evaluated using shelled feed corn (initial diameter d_initial = 7.5 mm) ground through hammer mill screens from 1.0 mm to 6.0 mm (1/√d_p from 0.5 to 2.0 mm^-0.5).",
            "apparatus": [
                {"name": "Laboratory Pilot Hammer Mill", "purpose": "Fitted with 16 reversible hardened steel hammers, 3.0 kW motor, and interchangeable screen inserts."},
                {"name": "Digital Three-Phase Power Analyzer", "purpose": "Measures active electrical power (kW) and energy consumption (kWh) with 0.1% accuracy."},
                {"name": "Standard Interchangeable Perforated Screens", "purpose": "Perforated screens with circular openings of 1.0, 1.5, 2.0, 3.0, 4.5, and 6.0 mm."},
                {"name": "Ro-Tap Mechanical Sieve Shaker & Sieve Nest", "purpose": "ASABE S319 standard nest of 14 sieves from No. 4 to No. 270 with pan."},
                {"name": "Vibratory Electromagnetic Feed Hopper", "purpose": "Delivers a constant, uniform grain feed rate of 100 kg/h into the grinding chamber."},
                {"name": "Precision Analytical Balance (0.01 g)", "purpose": "Weighs sieved grain fractions to calculate geometric mean diameter d_gw and fineness modulus."}
            ],
            "procedure": [
                {"title": "Initial Screen Installation & Tare Power", "text": "Install the 6.0 mm perforated screen in the hammer mill. Run the mill empty at rated speed (3600 RPM) to record baseline idle mechanical friction and windage power (P_idle)."},
                {"title": "Batch Feeding & Energy Logging", "text": "Weigh exactly 10.0 kg of shelled corn, start the vibratory feeder to deliver grain at 100 kg/h, and integrate net active electrical energy (kWh) until the batch is completely ground."},
                {"title": "Specific Energy Calculation", "text": "Calculate net specific grinding energy E_s = (E_total - E_idle) / Mass_batch (kWh/tonne)."},
                {"title": "Sieve Shaker Fineness Analysis", "text": "Take a representative 100 g sample of ground meal, place in the standard Ro-Tap sieve shaker for 10.0 minutes, weigh fractions on each sieve, and compute geometric mean diameter d_p in accordance with ASABE S319."},
                {"title": "Screen Size Stepping", "text": "Repeat the grinding trial across screens of 4.5, 3.0, 2.0, 1.5, and 1.0 mm, recording specific energy E_s and particle diameter d_p for each trial."},
                {"title": "Bond's Law Linear Regression", "text": "Calculate size parameter 1/√d_p (mm^-0.5), plot specific energy E_s versus 1/√d_p, and determine Bond's work scaling factor K_b via linear regression."}
            ],
            "topics": [
                {"question": "State Bond's, Rittinger's, and Kick's comminution laws.", "answer": "All three derive from dE = -C·dx / x^n. Kick's law (n = 1) states E = C·ln(d_1/d_2); Rittinger's law (n = 2) states E = C·(1/d_2 - 1/d_1), linking energy to new surface area; Bond's law (n = 1.5) states E = C·(1/√d_2 - 1/√d_1), successfully describing intermediate grinding ranges."},
                {"question": "What is the Fineness Modulus (FM) of ground feed?", "answer": "Fineness Modulus (ASABE S319) is a single numerical index indicating the coarseness of ground feed, calculated by summing the cumulative percentages of material retained on a standard series of seven sieves (3/8\", 4, 8, 14, 28, 48, 100 mesh) divided by 100."},
                {"question": "How does hammer tip speed influence hammer mill efficiency?", "answer": "Hammer tip speed (v = π·D·N) dictates kinetic impact energy (E_k = 0.5·m·v²). Optimal tip speed is 60 to 90 m/s; lower speeds fail to shatter kernels upon first impact, while excessively high speeds create excessive fines and increase idle windage power loss."},
                {"question": "What is the function of the hammer mill screen?", "answer": "The screen acts as a classification barrier; particles remain inside the turbulent grinding chamber until they are fractured smaller than the screen holes, at which point centrifugal force and air draft sweep them out into the collection cyclone."},
                {"question": "How does grain moisture content affect grinding energy consumption?", "answer": "High moisture makes grain flexible, rubbery, and viscoelastic, absorbing hammer impacts without shattering. This drastically increases specific grinding energy (up to 200% higher) and causes screen blinding and mill choking."},
                {"question": "Why is pneumatic suction air assist used in modern commercial hammer mills?", "answer": "Air assist draws cooling airflow through the grinding chamber, which rapidly evacuates ground meal through screen perforations, reduces internal friction, prevents screen blinding, and lowers specific energy consumption by 15% to 30%."}
            ],
            "precautions": [
                "Install a strong permanent magnet at the feed hopper inlet to trap tramp metal (bolts, nails) that would cause sparks or explode in the mill.",
                "Ensure ear defenders and dust respirator masks are worn during all hammer mill operating trials.",
                "Never open the grinding chamber door until the rotor has come to a complete, verified stop.",
                "Allow the motor to reach full operating speed before initiating grain feeding to prevent electrical stalling."
            ],
            "limitations": [
                "Hammer mills produce a wide, polydisperse particle size distribution with substantial fines compared to roller mills.",
                "Electric motor efficiency (typically 85% to 92%) must be accounted for when converting electrical kWh into true shaft mechanical work.",
                "Bond's law assumes brittle fracture; grains exhibit ductile viscoelastic deformation at higher moisture contents.",
                "Screen wear (rounded hole edges) increases specific energy consumption over prolonged industrial operation."
            ],
            "quiz": [
                {
                    "question": "According to Bond's third law of comminution, grinding energy scales inversely with:",
                    "options": ["Particle diameter d_p", "Square root of particle diameter √d_p", "Cube of particle diameter d_p³", "Logarithm of particle diameter ln(d_p)"],
                    "correct": 1,
                    "explanation": "Bond's comminution law states that grinding energy is inversely proportional to the square root of particle diameter: E ∝ 1/√d_p."
                },
                {
                    "question": "What primary mechanism produces size reduction inside a hammer mill?",
                    "options": ["Slow hydraulic squeezing", "High-velocity dynamic impact by rotating steel hammers against suspended kernels", "Chemical dissolution", "Microwave radiation"],
                    "correct": 1,
                    "explanation": "Hammer mills rely on high-speed kinetic impacts (tip speeds 60-90 m/s) between rotating steel hammers and grain kernels."
                },
                {
                    "question": "If Bond work factor K_b = 4.8 kWh·mm^0.5/t and mean particle diameter is d_p = 1.0 mm (1/√d_p = 1.0), what is E_s?",
                    "options": ["1.2 kWh/t", "2.4 kWh/t", "4.8 kWh/t", "9.6 kWh/t"],
                    "correct": 2,
                    "explanation": "E_s = K_b × (1/√d_p) = 4.8 × 1.0 = 4.80 kWh/t."
                },
                {
                    "question": "Why are roller mills preferred over hammer mills when uniform, coarse particle size is required for dairy cattle?",
                    "options": ["Roller mills use no electricity", "Roller mills crush grain between cylindrical rolls without generating excessive fine dust", "Roller mills cook the grain", "Roller mills extract oil"],
                    "correct": 1,
                    "explanation": "Roller mills shear grain into uniform, coarse cracked pieces with minimal dust, ideal for ruminant rumen function."
                }
            ],
            "settings": ["Motor power: 3.0 kW (3600 RPM)", "Feed rate: 100 kg/h", "Crop: Shelled feed corn (12% moisture)"],
            "samples": [0.5, 0.8, 1.1, 1.4, 1.7, 2.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🌾", "label": "1. Pilot Hammer Mill"},
                {"id": "compare", "icon": "📊", "label": "2. Energy vs 1/√d_p Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Screen Size Sandbox"}
            ]
        },
        {
            "number": 28,
            "slug": "paddy-rubber-roll-husking-head-rice-yield",
            "title": "Paddy Rubber-Roll Husker Differential Speed & Head Rice Yield Recovery",
            "shortTitle": "Paddy Rubber-Roll Husking",
            "aim": "Evaluate the dehusking efficiency, brown rice breakage percentage, and head rice recovery yield in an agricultural rubber-roll paddy husker as a function of roller speed differential.",
            "inputLabel": "Roller Peripheral Speed Differential Δv",
            "shortInput": "Speed Diff Δv",
            "inputUnit": "m/s",
            "min": 1.5,
            "max": 4.0,
            "step": 0.5,
            "initial": 2.5,
            "inputDecimals": 1,
            "rawLabel": "Dehusking Hulling Efficiency η_h",
            "rawUnit": "%",
            "rawDecimals": 2,
            "xAxis": "Speed differential Δv (m/s)",
            "yAxis": "Hulling efficiency η_h (%)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 2.75,
            "emptyY": 76.38,
            "targetName": "Husking Differential Sensitivity b_h",
            "target": "12.5000",
            "refValue": 12.5000,
            "resultUnit": "%/(m/s)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "η_h = b_h · Δv + η_0 = 12.5000 · Δv + 42.0000",
            "intro": "Paddy rice milling converts raw harvested paddy (rough rice) into polished white rice for human consumption through two sequential mechanical unit operations: dehusking (removal of the fibrous protective outer hull to produce brown rice) and whitening/polishing (removal of the bran layer and germ). The rubber-roll husker is the global industry standard machine for paddy dehusking, offering superior hulling efficiency with minimal grain breakage compared to obsolete steel hullers or emery stone discs. The machine consists of two resilient vulcanized rubber rollers rotating in opposite directions at different peripheral velocities (typically a fast roller at 10 to 12 m/s and a slow roller at 8 to 9 m/s, yielding a differential velocity ratio of 1:1.20 to 1:1.30). As paddy kernels enter the narrow clearance between the rollers, the slower roller retards one side of the husk while the faster roller strips the opposite side, exerting a pure shearing force that peels off the loose hull without crushing the fragile starch endosperm. If the speed differential Δv = v_fast - v_slow is too low, unhusked paddy passes through, lowering efficiency. If Δv is too high, excessive friction generates heat, wears the expensive rubber rolls rapidly, and fractures kernels, depressing Head Rice Yield (HRY). In this laboratory, an instrumented pilot rubber-roll husker calibrates hulling metrics across varying differential speeds.",
            "modelExtra": "Evaluated using long-grain paddy rice (moisture 13.0% d.b.) at constant rubber roll clearance of 0.8 mm across differential speeds from 1.5 to 4.0 m/s.",
            "apparatus": [
                {"name": "Laboratory Precision Rubber-Roll Paddy Husker", "purpose": "Fitted with dual independent variable-speed rubber rollers (150 mm diameter, 50 mm width)."},
                {"name": "Independent Dual Variable-Frequency Motor Drives", "purpose": "Regulates fast roller and slow roller peripheral speeds independently with 0.1 m/s accuracy."},
                {"name": "Aspirator Chaff Separation Column", "purpose": "Pneumatically winnows removed husks from brown rice and unhusked paddy discharge."},
                {"name": "Paddy-Brown Rice Separator Tray (Laboratory Indented Cylinder)", "purpose": "Separates unhusked paddy from dehulled brown rice mechanically."},
                {"name": "Laboratory Rice Sizing Sieve (1.4 mm Slot)", "purpose": "Separates whole head rice from broken kernels in accordance with ISO 7301 standards."},
                {"name": "Precision Electronic Balance (0.01 g)", "purpose": "Weighs unhusked paddy, brown rice, broken rice, and husk fractions."}
            ],
            "procedure": [
                {"title": "Roller Clearance & Durometer Inspection", "text": "Inspect rubber roller surfaces for even wear and hardness (Shore A 85 to 90 durometer). Set the roll clearance to exactly 0.8 mm using a thickness feeler gauge."},
                {"title": "Initial Speed Differential Setup", "text": "Set slow roller peripheral velocity to v_slow = 8.0 m/s and fast roller to v_fast = 9.5 m/s, establishing an initial speed differential Δv = 1.5 m/s."},
                {"title": "Standardized Batch Feeding", "text": "Feed exactly 1000.0 g of clean, graded paddy rice through the vibrating hopper over 60 seconds into the husking nip."},
                {"title": "Aspiration & Fraction Sorting", "text": "Collect the discharge from the aspirator column, separating the three fractions: separated husks, dehulled brown rice (m_brown), and unhusked paddy (m_unhusked)."},
                {"title": "Hulling Efficiency & Breakage Calculation", "text": "Calculate dehusking hulling efficiency η_h = [m_brown / (m_brown + m_unhusked)] × 100%, and screen brown rice through the slotted sieve to determine broken rice percentage."},
                {"title": "Speed Differential Stepping", "text": "Increment fast roller speed across five additional stages to achieve Δv = 2.0, 2.5, 3.0, 3.5, and 4.0 m/s, plotting η_h versus Δv to extract sensitivity b_h."}
            ],
            "topics": [
                {"question": "How does a rubber-roll husker accomplish paddy dehusking?", "answer": "Paddy is fed into the nip between two rubber rollers rotating in opposite directions at different speeds. The slow roll grips and holds one side of the husk while the faster roll shears the opposite side, creating a mechanical shear couple that peels off the hull without crushing the kernel."},
                {"question": "Define Head Rice Yield (HRY) and explain its commercial significance.", "answer": "Head Rice Yield is the percentage by weight of rough paddy rice that is recovered as whole unbroken milled kernels (kernels that are at least three-fourths of their original length). Broken rice sells at a 50% discount; thus, maximizing HRY is the primary economic objective in rice milling."},
                {"question": "What is the typical speed ratio between the fast and slow rolls in a commercial rubber-roll husker?", "answer": "The standard commercial speed ratio is approximately 1:1.20 to 1:1.30 (fast roller rotates 20% to 30% faster than the slow roller), providing optimal shearing force without excessive frictional heating."},
                {"question": "Why do rubber rollers wear out, and why must their positions be periodically reversed?", "answer": "The faster roller does more abrasive shearing work and wears down faster than the slow roller. Reversing the positions of the two rollers (swapping fast and slow drives) balances wear and extends total rubber roll service life."},
                {"question": "What causes rice kernel breakage during dehusking?", "answer": "Kernel breakage is caused by excessive roller pressure (clearance too tight), excessively high speed differential, pre-existing internal sun-cracks or drying stress fissures in the paddy, and thermal shock from overheated rubber rolls."},
                {"question": "What is the function of the aspirator immediately following the rubber-roll husker?", "answer": "The aspirator uses an upward airstream (velocity approx. 4 to 5 m/s) to lift and blow away the lightweight, bulky hulls (which constitute about 20% of paddy weight), leaving clean brown rice and unhusked paddy for subsequent separation."}
            ],
            "precautions": [
                "Never operate rubber rolls without paddy feeding; contact between rotating rubber faces generates extreme friction that burns and melts the rubber within seconds.",
                "Ensure paddy is free from stones, gravel, and metal by passing through a pre-cleaner destoner prior to husking.",
                "Check roller parallelism across the entire width using feeler gauges; tapering clearance causes uneven hulling and localized roller grooving.",
                "Maintain uniform paddy feed across the full 50 mm roll width to ensure uniform wear."
            ],
            "limitations": [
                "Rubber rolls soften as operational temperature rises (> 60°C), slightly shifting the effective friction coefficient and hulling efficiency during prolonged continuous runs.",
                "Requires paddy moisture strictly between 12.5% and 14.0%; wet paddy (> 15%) deforms without dehusking, while over-dry paddy (< 11%) shatters into brokens.",
                "Evaluates single-pass dehusking; commercial mills recirculate unhusked paddy back through a secondary return husker.",
                "Rubber durometer hardness degrades with storage age and UV exposure."
            ],
            "quiz": [
                {
                    "question": "What mechanical force is primarily responsible for stripping the husk in a rubber-roll paddy husker?",
                    "options": ["Tensile stretching", "Shearing force caused by the differential peripheral speed between the two rubber rolls", "Impact shattering", "Chemical digestion"],
                    "correct": 1,
                    "explanation": "The differential speed between the counter-rotating rubber rollers creates a shearing action that peels off the husk."
                },
                {
                    "question": "What is the definition of Head Rice in grain processing standards?",
                    "options": ["Rice with the husk attached", "Kernels that are at least 75% (three-fourths) of their original unbroken length", "Rice flour", "Parboiled rice only"],
                    "correct": 1,
                    "explanation": "Head rice is defined as milled whole kernels that are at least three-fourths of their original whole length."
                },
                {
                    "question": "If 1000 g of paddy yields 750 g of dehulled brown rice and 50 g of unhusked paddy in the discharge, what is the hulling efficiency?",
                    "options": ["75.0%", "85.0%", "93.75%", "100.0%"],
                    "correct": 2,
                    "explanation": "Hulling efficiency η_h = 750 / (750 + 50) × 100% = 750 / 800 × 100% = 93.75%."
                },
                {
                    "question": "Why must the positions of the fast and slow rubber rolls be periodically swapped in rice mills?",
                    "options": ["To reverse the electric motor polarity", "Because the fast roll wears down faster, swapping balances rubber roll wear and extends lifespan", "To change rice color", "To cool the bearings"],
                    "correct": 1,
                    "explanation": "The fast roll performs more frictional work and wears faster; swapping rollers balances wear across both rolls."
                }
            ],
            "settings": ["Roll clearance: 0.8 mm", "Slow roll speed: 8.0 m/s", "Crop: Long-grain paddy (13.0% moisture)"],
            "samples": [1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🌾", "label": "1. Rubber-Roll Husker"},
                {"id": "compare", "icon": "📊", "label": "2. Efficiency vs Δv Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Roll Clearance Sandbox"}
            ]
        }
    ]
