# -*- coding: utf-8 -*-
"""Agricultural Engineering Module 5: Terramechanics, Precision Agriculture & Renewable Farm Energy (Labs 36–42)."""

def get_module_5():
    return [
        {
            "number": 36,
            "slug": "cone-penetrometer-soil-strength-hardpan-profiling",
            "title": "Cone Penetrometer Soil Strength & Hardpan Identification",
            "shortTitle": "Soil Cone Index Profile",
            "aim": "Measure vertical cone penetration resistance force across soil depth to identify tillage pans, compaction layers, and calculate the ASABE Cone Index (CI).",
            "inputLabel": "Insertion Depth z",
            "shortInput": "Depth z",
            "inputUnit": "cm",
            "min": 5.0,
            "max": 30.0,
            "step": 5.0,
            "initial": 15.0,
            "inputDecimals": 1,
            "rawLabel": "Penetration Resistance Force F_p",
            "rawUnit": "N",
            "rawDecimals": 2,
            "xAxis": "Insertion depth z (cm)",
            "yAxis": "Penetration force F_p (N)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 17.5,
            "emptyY": 300.0,
            "targetName": "Penetration Resistance Gradient k_p",
            "target": "18.5000",
            "refValue": 18.5000,
            "resultUnit": "N/cm",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "F_p = k_p · z = 18.5000 · z",
            "intro": "In terramechanics and agricultural soil management, soil mechanical strength dictates root penetration resistance, crop seedling emergence, field trafficability, and the draft energy required for tillage implements. Heavy agricultural machinery traffic (tractors, grain carts, combine harvesters) induces subsoil compaction, creating dense 'plow pans' or 'traffic hardpans' that restrict root elongation and impede water infiltration. Under ASABE Standard S313 and EP542, the standard instrument for quantifying in-situ soil compaction is the soil cone penetrometer, which consists of a 30° circular stainless steel cone driven vertically into the soil at a uniform penetration rate of 30 mm/s (1.8 m/min). The penetrometer measures the axial insertion force F_p, which is normalized by the base area of the cone (typically 323 mm² for a large cone or 130 mm² for a small cone) to yield the ASABE Cone Index (CI = F_p / A_c, in kPa or MPa). In homogeneous topsoil profiles, insertion force increases linearly with depth with a characteristic penetration resistance gradient k_p governed by soil texture, bulk density, and soil matric water potential. In this experiment, an automated motor-driven hydraulic penetrometer rig equipped with a precision load cell and linear displacement transducer profiles an agricultural silt loam field to map penetration resistance and pinpoint subsurface compaction horizons.",
            "modelExtra": "Evaluated in an agricultural silt loam soil (gravimetric moisture content 17.5%, bulk density 1.35 g/cm³) using an ASABE standard 30° cone (base area 3.23 cm²). Linear penetration gradient is evaluated across the upper 30 cm depth profile at standard 30 mm/s penetration rate.",
            "apparatus": [
                {"name": "Motorized Hydraulic Penetrometer Rig", "purpose": "Drives the penetrometer shaft vertically into soil at standard ASABE velocity of 30 mm/s (±5 mm/s)."},
                {"name": "ASABE Standard 30° Stainless Steel Cone", "purpose": "Provides standardized soil cutting geometry with base diameter 20.27 mm (base area 323 mm²)."},
                {"name": "Tension-Compression S-Beam Load Cell", "purpose": "Measures vertical penetration resistance force with 1.0 N resolution up to 2000 N capacity."},
                {"name": "Draw-Wire Linear Position Transducer", "purpose": "Measures continuous insertion depth from 0 to 60 cm with 0.5 mm spatial resolution."},
                {"name": "Field Data Acquisition Telemetry Logger", "purpose": "Synchronously samples depth and force at 100 Hz to generate continuous high-density penetration curves."},
                {"name": "Time-Domain Reflectometry (TDR) Moisture Probe", "purpose": "Measures volumetric soil moisture content concurrently at 5 cm depth intervals."}
            ],
            "procedure": [
                {"title": "Rig Leveling and Anchor Stabilization", "text": "Position the mobile penetrometer frame over the surveyed test grid and anchor hydraulic outriggers to eliminate frame deflection."},
                {"title": "Transducer Zeroing and Taring", "text": "Inspect the 30° cone for surface wear, align the shaft vertically with a spirit level, and zero the load cell in free air above the soil."},
                {"title": "Penetration Rate Standardization", "text": "Set the electric-hydraulic servo actuator to maintain a constant vertical advance velocity of 30 mm/s."},
                {"title": "Continuous Insertion Profile Acquisition", "text": "Initiate automated insertion down to 30 cm depth while logging instantaneous force F_p and depth z continuously."},
                {"title": "Discrete Depth Sampling Extraction", "text": "Extract representative penetration force readings at standard 5 cm depth increments (5.0, 10.0, 15.0, 20.0, 25.0, 30.0 cm)."},
                {"title": "Cone Index and Gradient Calculation", "text": "Calculate Cone Index CI = F_p / A_c and plot F_p against depth z, performing linear regression to evaluate the penetration gradient k_p."}
            ],
            "topics": [
                {"question": "How is the ASABE Cone Index (CI) defined and calculated?", "answer": "Cone Index is defined as the vertical force required to push a standard circular 30° cone through soil divided by the cross-sectional base area of the cone: CI = F_p / A_base (expressed in kPa or MPa). Standard ASABE cones have base areas of 323 mm² (large) or 130 mm² (small)."},
                {"question": "What is the critical Cone Index threshold that inhibits crop root elongation?", "answer": "Extensive agronomic research indicates that root elongation of most agricultural crops (corn, soybeans, wheat) declines significantly at a CI of 1.5 MPa and ceases almost completely when soil Cone Index reaches 2.0 to 2.5 MPa."},
                {"question": "Why must the insertion speed of a penetrometer be maintained at 30 mm/s?", "answer": "Soil shearing exhibits strain-rate dependence; moving too slowly allows localized pore water dissipation, while moving too rapidly creates dynamic inertial shock waves. The standard 30 mm/s speed ensures repeatable quasi-static shear conditions across international studies."},
                {"question": "How does soil moisture content influence penetrometer resistance?", "answer": "Soil strength decreases dramatically with increasing soil moisture because water reduces matric suction (tension), lubricates soil particle contact interfaces, and lowers soil cohesion; hence, CI measurements must always be reported alongside soil water content."},
                {"question": "What does a sharp localized peak in the CI depth profile indicate?", "answer": "A sharp peak in resistance at depths between 15 cm and 30 cm typically indicates a tillage hardpan (plow pan) created by repeated moldboard plowing or wheel traffic at the base of the furrow."},
                {"question": "What is the difference between a static penetrometer and a dynamic penetrometer?", "answer": "A static penetrometer is pressed smoothly into the soil at constant velocity, whereas a dynamic penetrometer is driven by repeated hammer blows of a known mass falling through a fixed height, counting the number of blows per unit penetration depth."}
            ],
            "precautions": [
                "Maintain strictly constant penetration velocity (30 mm/s) to prevent strain-rate measurement artifacts.",
                "Verify vertical shaft alignment to prevent bending moments that cause parasitic friction in the guide bushings.",
                "Inspect the cone tip periodically; replace any cone showing visible rounding, nicking, or dimension loss.",
                "Collect concurrent soil moisture readings within 10 cm of the insertion hole to contextualize resistance data."
            ],
            "limitations": [
                "The linear model applies to the upper 30 cm of uniform, settled topsoil prior to reaching dense glacial till or bedrock.",
                "Assumes stone-free soil; encountering cobbles or coarse gravel causes instantaneous artificial force spikes.",
                "Applies to cohesive silt loam; pure sands exhibit different frictional depth profiles.",
                "Does not separate tip bearing resistance from slight shaft sleeve friction along deep insertions."
            ],
            "quiz": [
                {
                    "question": "What is the standard base apex angle of an ASABE standard soil penetrometer cone?",
                    "options": ["15°", "30°", "45°", "60°"],
                    "correct": 1,
                    "explanation": "ASABE Standards S313 and EP542 specify an apex angle of exactly 30° for agricultural soil cones."
                },
                {
                    "question": "At approximately what Cone Index value does crop root elongation become severely restricted?",
                    "options": ["0.2 MPa", "0.5 MPa", "2.0 MPa", "8.0 MPa"],
                    "correct": 2,
                    "explanation": "A Cone Index exceeding 2.0 MPa (2000 kPa) creates severe mechanical impedance that halts root growth."
                },
                {
                    "question": "If measured penetration force is 370 N at a depth of 20 cm, what is the penetration gradient?",
                    "options": ["9.25 N/cm", "18.50 N/cm", "37.00 N/cm", "74.00 N/cm"],
                    "correct": 1,
                    "explanation": "Penetration gradient k_p = F_p / z = 370 N / 20 cm = 18.50 N/cm."
                },
                {
                    "question": "What is the standardized penetration rate for agricultural cone penetrometer tests?",
                    "options": ["5 mm/s", "30 mm/s", "100 mm/s", "500 mm/s"],
                    "correct": 1,
                    "explanation": "ASABE S313 specifies an insertion rate of 30 mm/s (1.8 m/min or ~72 in/min)."
                }
            ],
            "settings": ["Soil classification: Silt loam (A-horizon)", "Soil moisture: 17.5% gravimetric", "Cone size: ASABE Large (323 mm² base area, 30° apex)"],
            "samples": [5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "📍", "label": "1. Field Penetrometer Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Cone Index Profile"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Soil Compaction Sandbox"}
            ]
        },
        {
            "number": 37,
            "slug": "bekker-theory-off-road-terramechanics-rigid-wheel-sinkage",
            "title": "Bekker Theory of Off-Road Terramechanics & Rigid Wheel Sinkage",
            "shortTitle": "Bekker Terramechanics Sinkage",
            "aim": "Evaluate pressure-sinkage behavior of agricultural soil under plate loading to determine Bekker terramechanic sinkage exponent and cohesive/frictional moduli.",
            "inputLabel": "Plate Sinkage z_s",
            "shortInput": "Sinkage z_s",
            "inputUnit": "cm",
            "min": 1.0,
            "max": 6.0,
            "step": 1.0,
            "initial": 3.0,
            "inputDecimals": 1,
            "rawLabel": "Soil Normal Pressure p",
            "rawUnit": "kPa",
            "rawDecimals": 3,
            "xAxis": "ln(Sinkage z_s) (ln[cm])",
            "yAxis": "ln(Normal pressure p) (ln[kPa])",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 1.1,
            "emptyY": 3.0,
            "targetName": "Bekker Sinkage Exponent n",
            "target": "0.8500",
            "refValue": 0.8500,
            "resultUnit": "dimensionless",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ln(p) = n · ln(z_s) + ln(k) = 0.8500 · ln(z_s) + 2.1000",
            "intro": "Terramechanics—the study of terrain-vehicle mechanics and off-road mobility—provides the theoretical foundation for sizing agricultural tractor drive tires, predicting wheel sinkage ruts, and minimizing motion resistance on deformable agricultural soils. Dr. M.G. Bekker in his foundational works formulated the classical semi-empirical pressure-sinkage relationship governing soils under footing loads. Under Bekker's theory, the normal pressure p exerted by a circular or rectangular bearing plate penetrating into soil is related to sinkage depth z_s by the power-law equation: p = (k_c / b + k_phi) · z_s^n, where k_c is the cohesive modulus of soil deformation, k_phi is the frictional modulus of deformation, b is the smaller dimension (width or radius) of the contact patch, and n is the dimensionless soil sinkage exponent. In logarithmic space, this fundamental relation linearizes into: ln(p) = n · ln(z_s) + ln(k), where the gradient corresponds directly to the sinkage exponent n. When n < 1, the soil displays strain-softening or typical agricultural loam behavior where incremental resistance diminishes with depth; when n > 1, the soil compacts into a denser strain-hardening state. In this experiment, a bevameter test apparatus equipped with circular penetration plates is hydraulically driven into agricultural tilled soil to record pressure-sinkage curves and extract Bekker terramechanic parameters.",
            "modelExtra": "Evaluated on tilled agricultural loam soil using a circular bevameter flat plate of diameter 10.0 cm (b = 5.0 cm). Data transformed into natural logarithmic coordinates ln(z_s) and ln(p) to extract sinkage exponent n and combined modulus k.",
            "apparatus": [
                {"name": "Agricultural Bevameter Test Rig", "purpose": "Applies controlled hydraulic vertical loads to soil penetration plates while logging displacement."},
                {"name": "Interchangeable Circular Bevameter Plates", "purpose": "Provides hardened steel plates of 50 mm, 100 mm, and 150 mm diameters for Bekker modulus separation."},
                {"name": "High-Precision Hydraulic Pressure Transducer", "purpose": "Measures hydraulic actuator pressure to compute plate normal contact force with 0.05 kN precision."},
                {"name": "Linear Potentiometer Sinkage Sensor", "purpose": "Monitors plate vertical penetration into the soil surface with 0.1 mm measurement accuracy."},
                {"name": "Digital Strain-Gauge Telemetry Console", "purpose": "Logs simultaneous force-displacement signals at 50 Hz during continuous plate depression."},
                {"name": "Core Soil Sampler & Bulk Density Ring", "purpose": "Extracts undisturbed 100 cm³ soil cores to establish pre-test bulk density and moisture content."}
            ],
            "procedure": [
                {"title": "Soil Surface Preparation and Bevameter Setup", "text": "Level the tilled field test patch, remove loose surface crop residue, and anchor the bevameter reaction truck firmly over the site."},
                {"title": "Plate Mounting and Zero Contact Referencing", "text": "Attach the 100 mm diameter circular test plate, lower it until light initial contact (0.5 kPa) occurs, and zero the displacement sensor."},
                {"title": "Constant-Velocity Hydraulic Loading", "text": "Advance the hydraulic actuator downward at a controlled rate of 10 mm/s, driving the plate into the soil up to 6.0 cm sinkage."},
                {"title": "Continuous Force-Sinkage Telemetry Logging", "text": "Record instantaneous sinkage depth z_s and vertical contact force continuously throughout the penetration stroke."},
                {"title": "Discrete Pressure-Sinkage Extraction", "text": "Extract normal contact pressure p = F / A_p at discrete sinkage depths of 1.0, 2.0, 3.0, 4.0, 5.0, and 6.0 cm."},
                {"title": "Logarithmic Transformation and Regression", "text": "Compute natural logarithms ln(z_s) and ln(p), plotting the linearized curve and determining the Bekker sinkage exponent n from the slope."}
            ],
            "topics": [
                {"question": "What is the physical meaning of Bekker's sinkage exponent n?", "answer": "The exponent n describes the rate of soil resistance buildup with sinkage: n = 1 represents perfectly linear elastic soil; n < 1 represents typical agricultural soils where resistance increases sub-linearly (strain-softening); n > 1 represents highly compressible, dry muskeg or loose sandy soils that strain-harden as they compact."},
                {"question": "How are the cohesive modulus k_c and frictional modulus k_phi separated experimentally?", "answer": "By performing pressure-sinkage tests with two circular plates of different radii (b1 and b2). Plotting the apparent modulus k against 1/b yields a straight line where the slope equals k_c and the vertical intercept equals k_phi."},
                {"question": "How does Bekker's theory predict tractor wheel rolling resistance?", "answer": "Bekker integrated soil pressure across the circumference of a sinking rigid wheel, showing that compaction rolling resistance equals R_c = b · ∫ p · z · dθ, which scales as R_c ∝ W^((2n+2)/(2n+1)) / (D^(1/(2n+1))), demonstrating that larger diameter wheels dramatically reduce sinkage and resistance."},
                {"question": "What is a bevameter in terramechanics research?", "answer": "A bevameter is a field instrument invented by M.G. Bekker that performs two tests: a plate penetration test to determine normal pressure-sinkage parameters (k_c, k_phi, n) and a shear ring/plate test to measure soil shear strength (c and phi)."},
                {"question": "How does soil compaction from tractor traffic affect crop yield?", "answer": "Excessive wheel sinkage compacts subsoil macro-pores, increasing bulk density, reducing aeration and saturated hydraulic conductivity, and impeding root development, leading to stunted growth and 10% to 25% yield penalties in wheel ruts."},
                {"question": "What is the difference between a rigid wheel and a pneumatic tire in terramechanic models?", "answer": "A rigid wheel does not deflect, forcing all deformation into the soil; a pneumatic tire deflects elastically, creating an elliptical contact patch that lowers peak ground pressure when tire inflation pressure is less than critical soil ground contact pressure."}
            ],
            "precautions": [
                "Ensure steady vertical penetration rate (10 mm/s) to prevent dynamic inertial or rapid pore-pressure effects.",
                "Verify the reaction truck is sufficiently ballasted so it does not lift during high-load plate sinkage.",
                "Conduct tests away from prior vehicle wheel tracks to test pristine, un-compacted tilled soil.",
                "Ensure test plates are perfectly perpendicular to the vertical loading axis to eliminate moment errors."
            ],
            "limitations": [
                "The power-law relationship applies to vertical sinkage up to 6.0 cm; at extreme sinkage, lateral soil flow causes blowout.",
                "Assumes homogeneous topsoil without encountering hard stones or subsurface plow pans.",
                "Neglects dynamic lug churning and slip-induced sinkage present in driven tractor drive wheels.",
                "Applies to cohesive-frictional loam; saturated mud exhibits viscous hydrodynamic resistance."
            ],
            "quiz": [
                {
                    "question": "In Bekker's classical terramechanic equation p = (k_c/b + k_phi) · z^n, what does n represent?",
                    "options": ["Wheel slip ratio", "Soil sinkage exponent", "Soil moisture fraction", "Coefficient of rolling friction"],
                    "correct": 1,
                    "explanation": "The exponent n is the dimensionless soil sinkage exponent characterizing the non-linearity of pressure-sinkage behavior."
                },
                {
                    "question": "For most tilled agricultural loams, the Bekker sinkage exponent n typically falls in what range?",
                    "options": ["0.1 to 0.3", "0.6 to 1.1", "2.5 to 3.5", "5.0 to 10.0"],
                    "correct": 1,
                    "explanation": "Agricultural topsoils typically exhibit sinkage exponents between 0.6 and 1.1 (often close to 0.8 to 0.9)."
                },
                {
                    "question": "If ln(p) = 0.8500 · ln(z_s) + 2.1000, what is the fitted Bekker sinkage exponent n?",
                    "options": ["0.4250", "0.8500", "1.7000", "2.1000"],
                    "correct": 1,
                    "explanation": "In logarithmic coordinates ln(p) vs ln(z_s), the slope corresponds directly to the exponent n = 0.8500."
                },
                {
                    "question": "What terramechanical instrument measures soil pressure-sinkage and shear strength in the field?",
                    "options": ["Hydrometer", "Bevameter", "Psychrometer", "Anemometer"],
                    "correct": 1,
                    "explanation": "The bevameter was developed specifically by M.G. Bekker to measure terramechanical properties of off-road terrain."
                }
            ],
            "settings": ["Test soil: Tilled agricultural silt loam", "Bevameter plate: 100 mm diameter circular steel (b = 5.0 cm)", "Penetration rate: 10.0 mm/s hydraulic advance"],
            "samples": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🚜", "label": "1. Bevameter Test Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Log Pressure-Sinkage"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Terramechanics Wheel Sandbox"}
            ]
        },
        {
            "number": 38,
            "slug": "flat-plate-solar-air-collector-thermal-efficiency",
            "title": "Flat-Plate Solar Air Collector Thermal Efficiency for Grain Drying",
            "shortTitle": "Solar Air Collector Efficiency",
            "aim": "Evaluate the steady-state thermal efficiency of an unglazed perforated agricultural solar air heater across varying normalized thermal loss parameters.",
            "inputLabel": "Reduced Temp Parameter T*",
            "shortInput": "Param T*",
            "inputUnit": "(°C·m²)/W",
            "min": 0.01,
            "max": 0.06,
            "step": 0.01,
            "initial": 0.03,
            "inputDecimals": 2,
            "rawLabel": "Collector Thermal Efficiency η",
            "rawUnit": "fraction",
            "rawDecimals": 4,
            "xAxis": "Reduced temperature (T_i - T_a)/I_t ((°C·m²)/W)",
            "yAxis": "Thermal efficiency η",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 0.035,
            "emptyY": 0.45,
            "targetName": "Overall Thermal Loss Coefficient a_1",
            "target": "6.2000",
            "refValue": 6.2000,
            "resultUnit": "W/(m²·°C)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "η = -a_1 · T* + η_0 = -6.2000 · T* + 0.6800",
            "intro": "Solar thermal air collectors provide a sustainable, low-cost renewable energy technology for pre-heating ventilation air in agricultural grain drying bins, crop dehydrators, and livestock building heating. In agricultural drying applications, air temperature only needs to be raised by 5 °C to 15 °C above ambient to cut relative humidity by 20% to 40%, vastly increasing drying capacity without scorching seeds. Under ASHRAE Standard 93 and ISO 9806 solar collector testing methodologies, the steady-state thermal performance of a solar air heater is governed by the Hottel-Whillier-Bliss equation: η = Q_u / (A_c · I_t) = F_R · (τα) - F_R · U_L · [(T_in - T_amb) / I_t], where η is the thermal collection efficiency, Q_u is useful thermal power collected (m_dot · C_p · ΔT), A_c is gross collector aperture area, I_t is incident global solar irradiance on the collector plane, F_R is the collector heat removal factor, τα is the effective transmittance-absorptance product, and U_L is the overall collector heat loss coefficient. Plotting thermal efficiency η against the reduced temperature parameter T* = (T_in - T_amb) / I_t yields a straight line with y-intercept η_0 = F_R · (τα) and negative slope magnitude a_1 = F_R · U_L. In this experiment, a 2.0 m² matrix-absorber agricultural solar air heater is evaluated on a solar simulator test stand across regulated inlet temperatures and flow rates to determine optical efficiency and overall thermal loss characteristics.",
            "modelExtra": "Evaluated on a 2.0 m² transpired perforated black-metal solar air collector under steady simulated solar irradiance of 850 W/m² at air mass flow rate of 0.04 kg/(s·m²). Linearized thermal performance is evaluated according to ASHRAE 93-2010.",
            "apparatus": [
                {"name": "Agricultural Solar Air Heater Collector", "purpose": "Provides 2.0 m² aperture absorber featuring blackened perforated corrugated aluminum matrix absorber."},
                {"name": "Indoor Solar Radiation Simulator Array", "purpose": "Delivers uniform artificial solar irradiance (850 W/m², class B spectrum) with metal halide lamps."},
                {"name": "Calibrated Precision Pyranometer", "purpose": "Measures total global solar irradiance incident on the collector tilt plane with ±1.5% accuracy."},
                {"name": "Variable-Speed Air Delivery Blower", "purpose": "Circulates drying air through the collector channel across regulated mass flow rates from 0.02 to 0.08 kg/(s·m²)."},
                {"name": "Multi-Point Thermopile Grid Sensors", "purpose": "Measures inlet, outlet, and ambient air dry-bulb temperatures with 0.05 °C differential precision."},
                {"name": "Orifice Plate Airflow Measurement Station", "purpose": "Monitors drying air mass flow rate according to ISO 5167 standards with differential pressure cell."}
            ],
            "procedure": [
                {"title": "Solar Simulator Irradiance Calibration", "text": "Energize the metal-halide lamp array and map irradiance across the 2.0 m² collector plane, setting average intensity to 850 W/m²."},
                {"title": "Blower Flow Rate Standardization", "text": "Adjust the air delivery blower frequency drive to establish a standardized mass flow rate of 0.080 kg/s (0.04 kg/(s·m²))."},
                {"title": "Initial Ambient Inlet Temperature Baseline", "text": "Operate the collector with entering air at ambient temperature (T_in = T_amb) to obtain the zero-loss maximum efficiency point."},
                {"title": "Steady-State Thermal Equilibrium Acquisition", "text": "Maintain operation for 20 minutes until air temperature rise (T_out - T_in) reaches steady-state (fluctuations < 0.1 °C over 5 min)."},
                {"title": "Reduced Temperature Parameter Progression", "text": "Increment entering air temperature using pre-heaters to generate T* values of 0.01, 0.02, 0.03, 0.04, 0.05, and 0.06 (°C·m²)/W."},
                {"title": "Hottel-Whillier-Bliss Regression Analysis", "text": "Calculate thermal efficiency η = m_dot · C_p · (T_out - T_in) / (A_c · I_t) and perform linear regression against T* to determine a_1 and η_0."}
            ],
            "topics": [
                {"question": "How does the Hottel-Whillier-Bliss equation describe solar collector thermal efficiency?", "answer": "The equation is η = F_R·(τα) - F_R·U_L·[(T_i - T_a) / I_t], stating that efficiency equals maximum optical efficiency minus thermal heat losses caused by the temperature difference between the collector and the surrounding ambient air."},
                {"question": "Why is solar air heating particularly well suited for agricultural grain drying?", "answer": "Grain drying requires large volumes of moderately warmed air (5 °C to 15 °C temperature lift). Because low operating temperatures minimize collector thermal radiation and convection losses, unglazed solar collectors operate at peak efficiencies (50% to 70%)."},
                {"question": "What is the physical significance of the collector heat removal factor F_R?", "answer": "F_R is the ratio of actual useful energy collected to the energy that would be collected if the entire collector absorber surface were at the fluid entering temperature. It reflects the convective heat transfer effectiveness between absorber plate and airstream."},
                {"question": "What are the advantages of a transpired (perforated) solar air collector over glazed flat-plate collectors?", "answer": "Transpired collectors draw ambient air directly through thousands of micro-perforations in the dark cladding, capturing heat that would otherwise be lost by convection, eliminating expensive glass covers, and achieving over 70% seasonal efficiency."},
                {"question": "How does air mass flow rate affect collector efficiency and air temperature rise?", "answer": "Increasing airflow rate improves internal convection heat transfer, increasing overall thermal efficiency η, but decreases the air residence time, resulting in a lower temperature rise ΔT between inlet and outlet."},
                {"question": "Why is thermal insulation on the collector back and sides critical?", "answer": "Without rear insulation, conductive and convective heat losses through the collector casing into ambient air dramatically increase the loss coefficient U_L, drastically reducing efficiency at higher operating temperatures."}
            ],
            "precautions": [
                "Maintain constant solar simulator irradiance and spatial uniformity across the entire collector aperture.",
                "Ensure steady ambient room temperature and eliminate stray drafts from external ventilation fans.",
                "Verify airtight duct connections between blower, collector, and orifice meter to eliminate air leakage.",
                "Allow full thermal steady-state to develop before integrating telemetry data for each testing point."
            ],
            "limitations": [
                "The linear model applies strictly to steady-state solar irradiance without rapid transient cloud effects.",
                "Assumes constant ambient wind speed over the collector face; high winds increase convective loss U_L.",
                "Valid for non-condensing dry air regimes without moisture phase change in the air channels.",
                "Applies to clean, un-soiled collector surfaces without agricultural dust accumulation."
            ],
            "quiz": [
                {
                    "question": "What does the y-intercept of a standard Hottel-Whillier-Bliss solar collector efficiency plot represent?",
                    "options": ["Heat loss coefficient", "Maximum optical efficiency F_R·(τα)", "Stagnation temperature", "Collector mass flow rate"],
                    "correct": 1,
                    "explanation": "When entering temperature equals ambient (T* = 0), heat losses vanish and efficiency equals maximum optical efficiency F_R·(τα)."
                },
                {
                    "question": "Why is only a modest temperature rise (5 °C to 15 °C) needed for agricultural solar grain drying?",
                    "options": ["To avoid melting the bin", "Because a 10 °C temperature lift cuts relative humidity by ~50%, creating massive drying capacity", "To prevent grain from germinating in the bin", "Because solar collectors cannot reach higher temperatures"],
                    "correct": 1,
                    "explanation": "Warming air by 10 °C cuts relative humidity roughly in half, dramatically increasing its moisture-carrying drying potential."
                },
                {
                    "question": "If fitted efficiency is η = -6.2000 · T* + 0.6800, what is the thermal loss coefficient a_1?",
                    "options": ["0.6800 W/(m²·°C)", "3.1000 W/(m²·°C)", "6.2000 W/(m²·°C)", "12.4000 W/(m²·°C)"],
                    "correct": 2,
                    "explanation": "The loss coefficient a_1 corresponds to the magnitude of the slope in the efficiency equation: a_1 = 6.2000 W/(m²·°C)."
                },
                {
                    "question": "What happens to collector thermal efficiency as airflow rate through the collector is increased?",
                    "options": ["Efficiency drops to zero", "Efficiency increases due to enhanced convective heat transfer", "Efficiency remains identical", "Absorber plate turns white"],
                    "correct": 1,
                    "explanation": "Higher airflow velocity enhances the convective heat transfer coefficient inside the air channel, increasing F_R and overall efficiency."
                }
            ],
            "settings": ["Collector type: Perforated unglazed matrix absorber (2.0 m²)", "Solar irradiance: 850 W/m² simulated global", "Air mass flow: 0.040 kg/(s·m²) (0.080 kg/s total)"],
            "samples": [0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "☀️", "label": "1. Solar Air Heater Test Stand"},
                {"id": "compare", "icon": "📊", "label": "2. Hottel-Whillier Efficiency"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Solar Drying Energy Sandbox"}
            ]
        },
        {
            "number": 39,
            "slug": "downdraft-biomass-gasifier-cold-gas-efficiency",
            "title": "Downdraft Biomass Gasifier Cold Gas Efficiency & Syngas Quality",
            "shortTitle": "Biomass Gasifier Efficiency",
            "aim": "Determine producer gas heating value and cold gas thermal efficiency of an agricultural residue downdraft gasifier as a function of equivalence ratio.",
            "inputLabel": "Equivalence Ratio Φ",
            "shortInput": "Ratio Φ",
            "inputUnit": "ratio",
            "min": 0.20,
            "max": 0.40,
            "step": 0.04,
            "initial": 0.28,
            "inputDecimals": 2,
            "rawLabel": "Syngas Heating Value HHV_g",
            "rawUnit": "MJ/Nm³",
            "rawDecimals": 3,
            "xAxis": "Equivalence ratio Φ (ratio)",
            "yAxis": "Syngas HHV (MJ/Nm³)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 0.30,
            "emptyY": 5.0,
            "targetName": "Gas Heating Equivalence Sensitivity k_Φ",
            "target": "12.5000",
            "refValue": 12.5000,
            "resultUnit": "MJ/(Nm³·ratio)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "HHV_g = -k_Φ · Φ + HHV_0 = -12.5000 · Φ + 8.8000",
            "intro": "Agricultural residues such as corncobs, rice husks, wood chips, and crop stalks represent abundant lignocellulosic feedstocks for thermochemical bioenergy conversion. Biomass gasification converts solid organic residues into a combustible gaseous fuel mixture known as producer gas or synthesis gas (syngas), primarily comprising carbon monoxide (CO), hydrogen (H2), methane (CH4), carbon dioxide (CO2), and nitrogen (N2). In small to medium decentralized agricultural power systems, downdraft (co-current) throat gasifiers are preferred because tars and pyrolysis vapors pass through a high-temperature incandescent char bed (900 °C to 1100 °C) where they are cracked into non-condensable fuel gases. The primary operational control parameter governing gasifier performance is the equivalence ratio Φ, defined as the actual air-to-fuel ratio divided by the stoichiometric air-to-fuel ratio required for complete combustion. In autothermal gasification, increasing Φ supplies more oxygen, which accelerates exothermic partial oxidation and raises bed temperature, but simultaneously promotes complete combustion of valuable H2 and CO into CO2 and H2O, thereby diluting the gas higher heating value (HHV_g). In this laboratory investigation, an instrumented 20 kW_th downdraft gasifier fed with dried corncob chunks is operated across controlled equivalence ratios to analyze syngas composition, higher heating value, and cold gas conversion efficiency.",
            "modelExtra": "Evaluated on dried agricultural corncob chunks (moisture content 11.2% d.b., lower heating value 16.8 MJ/kg) in an Imbert-type throat downdraft gasifier. Air supply is metered through calibrated tuyere nozzles to maintain equivalence ratios between 0.20 and 0.40.",
            "apparatus": [
                {"name": "Imbert-Type Downdraft Biomass Gasifier", "purpose": "20 kW_th gasification reactor with refractory-lined constriction throat, tuyere air nozzles, and rotating grate."},
                {"name": "Calibrated Syngas Venturi & Flare Station", "purpose": "Meters raw syngas production rate in Nm³/h and provides safe automated ignition flare for combustible off-gas."},
                {"name": "Gas Chromatography & Continuous Gas Analyzer", "purpose": "Measures volumetric percentages of CO, H2, CH4, CO2, and O2 in clean, dry producer gas."},
                {"name": "Multi-Zone Thermocouple Array", "purpose": "Monitors internal temperatures in drying (150 °C), pyrolysis (400 °C), throat (1050 °C), and reduction (800 °C) zones."},
                {"name": "Roots Positive-Displacement Air Blower", "purpose": "Supplies regulated primary blast air through calibrated rotameter to set exact equivalence ratios."},
                {"name": "Isokinetic Tar and Particulate Sampling Train", "purpose": "Samples raw gas according to CEN/TS 15439 standard to quantify condensable tar and soot loading."}
            ],
            "procedure": [
                {"title": "Feedstock Loading and Moisture Verification", "text": "Fill the reactor hopper with 25.0 kg of dried corncob chunks (size 25-50 mm, moisture 11.2%) and latch the airtight feed lid."},
                {"title": "Char Bed Ignition and Pre-Heating", "text": "Ignite the charcoal bed at the tuyeres with an LPG torch, drawing primary air via the suction blower until throat temperature exceeds 800 °C."},
                {"title": "Equivalence Ratio Standardization", "text": "Adjust blast air flow rate to establish the initial test equivalence ratio Φ = 0.20 based on measured biomass consumption rate."},
                {"title": "Steady Thermal Gasification Operation", "text": "Operate the gasifier for 30 minutes at steady state, monitoring throat temperature (950-1050 °C) and syngas flare flame stability."},
                {"title": "Syngas Composition and Flow Acquisition", "text": "Sample clean, conditioned syngas through the continuous infrared/thermal conductivity gas analyzer and log volumetric flow rate."},
                {"title": "Equivalence Progression and HHV Evaluation", "text": "Step the equivalence ratio through 0.24, 0.28, 0.32, 0.36, and 0.40, computing producer gas HHV = Σ (y_i · HHV_i) and fitting linear regression."}
            ],
            "topics": [
                {"question": "How is the equivalence ratio Φ defined in biomass gasification?", "answer": "The equivalence ratio Φ is the ratio of the actual air supplied per unit mass of dry biomass to the stoichiometric air required for complete combustion: Φ = (Air/Fuel)_actual / (Air/Fuel)_stoichiometric. For gasification, Φ typically ranges between 0.20 and 0.35."},
                {"question": "Why do downdraft gasifiers produce substantially less tar than updraft gasifiers?", "answer": "In a downdraft gasifier, biomass and air flow co-currently downward; volatile pyrolysis tars produced in the upper zone are forced to pass directly through the glowing incandescent char bed (1000 °C), where heavy tars undergo thermal cracking into light gases."},
                {"question": "What is the primary trade-off when increasing the equivalence ratio Φ?", "answer": "Increasing Φ generates more combustion heat, raising reactor temperatures and accelerating gasification kinetics, but consumes more fuel gas into CO2 and H2O while introducing more diluting atmospheric nitrogen, lowering the gas heating value."},
                {"question": "What is the definition of cold gas efficiency (CGE)?", "answer": "Cold gas efficiency is the ratio of chemical energy contained in the cooled producer gas to the chemical energy of the solid biomass fed: CGE = (V_gas · LHV_gas) / (M_biomass · LHV_biomass) × 100%, typically ranging from 65% to 75% in well-designed systems."},
                {"question": "What are the four primary reaction zones inside a downdraft gasifier?", "answer": "From top to bottom: (1) Drying zone (100-200 °C), (2) Pyrolysis zone (200-500 °C), (3) Oxidation/combustion throat zone (800-1100 °C), and (4) Reduction zone (600-900 °C) where CO2 and H2O react endothermically with hot carbon char to form CO and H2."},
                {"question": "Why is nitrogen dilution a major factor in air-blown gasification?", "answer": "Ambient air contains 79% inert nitrogen (N2); in air-blown gasification, nitrogen passes through unreacted and constitutes 45% to 55% of the raw producer gas volume, limiting its higher heating value to 4.5 - 6.5 MJ/Nm³."},
                {"question": "What happens if the equivalence ratio drops below 0.18?", "answer": "Insufficient oxygen fails to generate enough internal combustion heat to maintain the oxidation throat temperature above 800 °C, leading to incomplete cracking, severe tar condensation, and eventual reactor quenching."}
            ],
            "precautions": [
                "Verify airtight sealing of all gasifier flanges; producer gas contains deadly odorless carbon monoxide (CO).",
                "Ensure continuous operation of the syngas flare to prevent unburned combustible gas accumulation.",
                "Maintain biomass fuel moisture strictly below 15% to prevent excessive throat temperature suppression.",
                "Equip the laboratory with calibrated toxic gas monitors (CO and H2S alarms) and positive room ventilation."
            ],
            "limitations": [
                "The linear heating value decline model is valid across the practical autothermal gasification range (0.20 ≤ Φ ≤ 0.40).",
                "Assumes uniform corncob fuel particle size; excessive fines cause bridging and pressure drop channeling.",
                "Applies to air-blown atmospheric downdraft gasification; oxygen- or steam-blown systems achieve much higher HHV.",
                "Neglects transient warm-up periods prior to establishing steady-state char bed thermal equilibrium."
            ],
            "quiz": [
                {
                    "question": "What is the typical equivalence ratio range for autothermal biomass gasification?",
                    "options": ["0.05 to 0.10", "0.20 to 0.35", "0.75 to 0.90", "1.00 to 1.50"],
                    "correct": 1,
                    "explanation": "Biomass gasification requires partial oxidation, operating in the equivalence ratio range of 0.20 to 0.35."
                },
                {
                    "question": "Why is the higher heating value of air-blown producer gas relatively modest (4.5 to 6.5 MJ/Nm³)?",
                    "options": ["Absence of hydrogen", "High concentration (45-55%) of inert atmospheric nitrogen", "Excessive oxygen content", "Methane is destroyed"],
                    "correct": 1,
                    "explanation": "Because ambient air contains 79% nitrogen, the resulting producer gas is diluted with roughly 50% non-combustible N2."
                },
                {
                    "question": "If syngas HHV is 5.30 MJ/Nm³ at an equivalence ratio of 0.28, what does HHV become at Φ = 0.36 under HHV = -12.5000·Φ + 8.8000?",
                    "options": ["3.80 MJ/Nm³", "4.30 MJ/Nm³", "5.10 MJ/Nm³", "6.20 MJ/Nm³"],
                    "correct": 1,
                    "explanation": "HHV = -12.5000 · 0.36 + 8.8000 = -4.50 + 8.80 = 4.30 MJ/Nm³."
                },
                {
                    "question": "Which gasification reactor zone achieves the highest internal operating temperature (950-1100 °C)?",
                    "options": ["Drying zone", "Pyrolysis zone", "Oxidation throat zone", "Gas outlet pipe"],
                    "correct": 2,
                    "explanation": "The combustion/oxidation throat where blast air enters experiences exothermic reactions that reach 950-1100 °C."
                }
            ],
            "settings": ["Gasifier type: 20 kW_th Imbert-type downdraft throat", "Feedstock: Dried corncob chunks (moisture 11.2%, LHV 16.8 MJ/kg)", "Blast medium: Ambient air via mechanical blower"],
            "samples": [0.20, 0.24, 0.28, 0.32, 0.36, 0.40],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🔥", "label": "1. Downdraft Gasifier Reactor"},
                {"id": "compare", "icon": "📊", "label": "2. Syngas HHV vs Equivalence"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Biomass Energy Sandbox"}
            ]
        },
        {
            "number": 40,
            "slug": "vegetable-oil-biodiesel-transesterification-yield",
            "title": "Vegetable Oil Base Transesterification & Biodiesel Viscosity",
            "shortTitle": "Biodiesel Transesterification Yield",
            "aim": "Measure the ester conversion yield and kinematic viscosity reduction of non-edible agricultural seed oil during alkaline transesterification across varying methanol-to-oil molar ratios.",
            "inputLabel": "Methanol Molar Ratio R_m",
            "shortInput": "Ratio R_m",
            "inputUnit": "mol/mol",
            "min": 3.0,
            "max": 8.0,
            "step": 1.0,
            "initial": 6.0,
            "inputDecimals": 1,
            "rawLabel": "Biodiesel FAME Yield Y",
            "rawUnit": "%",
            "rawDecimals": 2,
            "xAxis": "Methanol molar ratio R_m (mol/mol)",
            "yAxis": "FAME ester yield Y (%)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 5.5,
            "emptyY": 75.0,
            "targetName": "Transesterification Molar Sensitivity b_m",
            "target": "5.2000",
            "refValue": 5.2000,
            "resultUnit": "%/(mol/mol)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "Y = b_m · R_m + Y_0 = 5.2000 · R_m + 51.0000",
            "intro": "Direct utilization of raw vegetable oils and animal fats in modern agricultural diesel engines is severely restricted by their high kinematic viscosity (typically 30 to 50 mm²/s at 40 °C, over ten times higher than petroleum diesel), poor fuel atomization, incomplete combustion, injector coking, and crankcase oil dilution. Transesterification chemically transforms bulky triglyceride macromolecules into fatty acid methyl esters (FAME, known as biodiesel) and glycerol byproduct through reaction with short-chain alcohol (methanol) in the presence of an alkaline catalyst (potassium hydroxide, KOH, or sodium methoxide). The overall stoichiometric reaction requires three moles of methanol per mole of triglyceride: Triglyceride + 3 CH3OH ⇌ 3 FAME + Glycerol. However, because transesterification is a reversible equilibrium reaction consisting of three consecutive steps (triglycerides → diglycerides → monoglycerides → glycerol), an excess alcohol molar ratio is required to shift chemical equilibrium forward according to Le Chatelier's principle. In agricultural biofuels engineering, optimizing the methanol-to-oil molar ratio R_m between 3:1 and 8:1 achieves high ester conversion yields (> 95%) and reduces kinematic viscosity into the ASTM D6751 / EN 14214 standard range of 3.5 to 5.0 mm²/s. In this laboratory experiment, refined jatropha seed oil is reacted across controlled alcohol molar ratios in an instrumented jacketed batch reactor to quantify ester yield, glycerin separation, and fuel viscosity reduction.",
            "modelExtra": "Evaluated on jatropha seed oil (free fatty acids < 1.0%) using 1.0% wt/wt KOH catalyst at constant reaction temperature of 60.0 °C and 60 minutes agitation time. FAME conversion yield is measured after gravitational glycerol settling and water washing.",
            "apparatus": [
                {"name": "Jacketed Glass Chemical Batch Reactor", "purpose": "2.0-liter borosilicate glass reactor with mechanical paddle stirrer, reflux condenser, and thermal jacket."},
                {"name": "Circulating Constant-Temperature Bath", "purpose": "Maintains reaction mixture at 60.0 ± 0.5 °C to prevent methanol vaporization while accelerating kinetics."},
                {"name": "Cannon-Fenske Capillary Viscometer", "purpose": "Measures kinematic viscosity of raw oil and biodiesel product at 40.0 °C in accordance with ASTM D445."},
                {"name": "High-Performance Gas Chromatograph (GC-FID)", "purpose": "Quantifies methyl ester content and residual glyceride fractions according to EN 14103 standard."},
                {"name": "Gravimetric Conical Separatory Funnel", "purpose": "Enables sharp visual separation and draining of dense glycerol byproduct layer from upper FAME ester phase."},
                {"name": "Analytical Laboratory Balance", "purpose": "Weighs raw feedstock oil, catalyst reagents, separated glycerol, and purified biodiesel to ±0.01 g precision."}
            ],
            "procedure": [
                {"title": "Feedstock Dehydration and Catalyst Preparation", "text": "Heat 500 g of jatropha oil to 105 °C to drive off moisture; dissolve 5.0 g of anhydrous KOH into designated methanol volumes."},
                {"title": "Molar Ratio Batch Charging", "text": "Prepare six distinct batches corresponding to methanol-to-oil molar ratios of 3:1, 4:1, 5:1, 6:1, 7:1, and 8:1."},
                {"title": "Controlled Transesterification Reaction", "text": "Charge the pre-heated oil (60 °C) with potassium methoxide solution, seal the reflux condenser, and agitate at 600 RPM for 60 minutes."},
                {"title": "Phase Separation and Glycerol Draining", "text": "Transfer the reaction mixture to a separatory funnel and allow gravity separation for 120 minutes; drain the dense lower glycerol layer."},
                {"title": "Water Washing and Fuel Drying", "text": "Wash the upper ester phase with warm acidified distilled water (50 °C) to remove residual catalyst and soap, followed by drying at 110 °C."},
                {"title": "Yield Calculation and Regression Analysis", "text": "Weigh purified FAME to calculate conversion yield Y = (m_FAME / m_oil) × 100% and plot Y against molar ratio R_m to determine b_m."}
            ],
            "topics": [
                {"question": "What is the primary chemical purpose of transesterifying vegetable oils into biodiesel?", "answer": "Transesterification removes the heavy glycerol backbone, replacing it with methyl groups to reduce kinematic viscosity from ~40 mm²/s down to 3.5 - 5.0 mm²/s at 40 °C, ensuring proper fuel droplet atomization and clean combustion in diesel injectors."},
                {"question": "Why is an excess methanol-to-oil molar ratio (typically 6:1) required when stoichiometry only requires 3:1?", "answer": "Because transesterification is a reversible stepwise equilibrium reaction; adding excess alcohol drives the equilibrium toward complete conversion of intermediate monoglycerides and diglycerides into FAME esters according to Le Chatelier's principle."},
                {"question": "What adverse reaction occurs if vegetable oil feedstock contains high free fatty acids (FFA)?", "answer": "Free fatty acids react with alkaline catalysts (KOH or NaOH) in a saponification reaction to produce undesirable soap and water: FFA + KOH → Soap + H2O. This consumes catalyst, creates stubborn emulsions, and prevents glycerol phase separation."},
                {"question": "What are the primary co-products and byproducts of agricultural biodiesel production?", "answer": "The primary byproduct is crude glycerol (approximately 10% by weight of the product stream), which can be refined for industrial applications, pharmaceutical uses, animal feed supplements, or anaerobic digestion feedstock."},
                {"question": "Why must the reaction temperature be kept below 64.7 °C during atmospheric transesterification?", "answer": "64.7 °C is the boiling point of methanol at standard atmospheric pressure; exceeding this temperature causes violent boiling, foaming, and loss of alcohol through the condenser."},
                {"question": "What key fuel quality specifications are defined in ASTM D6751 and EN 14214?", "answer": "Key parameters include: ester content (≥ 96.5%), kinematic viscosity at 40 °C (1.9 to 6.0 mm²/s ASTM, 3.5 to 5.0 mm²/s EN), flash point (≥ 93 °C or 130 °C), acid value (≤ 0.50 mg KOH/g), and free/total glycerin limits."},
                {"question": "How does biodiesel compare to petroleum diesel in terms of emissions and lubricity?", "answer": "Biodiesel is oxygenated (~11% O2 by mass), substantially reducing particulate matter (PM), carbon monoxide (CO), and unburned hydrocarbon (HC) emissions, and provides superior natural lubricity that protects high-pressure injection pumps, though NOx emissions may slightly increase."}
            ],
            "precautions": [
                "Handle methanol and potassium methoxide in a fume hood; methanol is toxic, flammable, and absorbed through skin.",
                "Ensure feed oil is thoroughly dried (moisture < 0.1%); water hydrolyzes triglycerides and promotes soap formation.",
                "Maintain agitation speed strictly constant (600 RPM) to ensure uniform mass transfer between immiscible liquid phases.",
                "Ensure separatory funnels stand undisturbed for at least 2 hours to allow complete coalescence of glycerol droplets."
            ],
            "limitations": [
                "The linear yield relation applies in the sub-saturation molar ratio range (3:1 to 8:1); beyond 9:1, excess alcohol hinders glycerol separation.",
                "Assumes low-FFA (< 1.0%) refined feedstock; high-FFA oils require acid-catalyzed pre-esterification.",
                "Applies to potassium hydroxide catalyst at 1.0% wt/wt concentration; other catalysts display distinct kinetic rates.",
                "Does not account for trace methanol solubility remaining dissolved within the unwashed ester phase."
            ],
            "quiz": [
                {
                    "question": "What is the stoichiometric molar ratio of alcohol to triglyceride for complete transesterification?",
                    "options": ["1 : 1", "3 : 1", "6 : 1", "12 : 1"],
                    "correct": 1,
                    "explanation": "One mole of triglyceride contains three fatty acid chains and requires exactly three moles of alcohol for stoichiometric conversion."
                },
                {
                    "question": "Why is the actual industrial molar ratio of methanol to oil typically maintained at 6:1?",
                    "options": ["To lower the boiling point", "To shift reversible reaction equilibrium toward maximum ester formation", "To increase viscosity", "To neutralize free fatty acids"],
                    "correct": 1,
                    "explanation": "Supplying excess methanol (6:1) forces the reversible equilibrium toward products, ensuring high ester conversion (>95%)."
                },
                {
                    "question": "What is the primary dense byproduct that separates to the bottom of the reactor after transesterification?",
                    "options": ["Water", "Glycerol (glycerin)", "Hexane", "Soapstone"],
                    "correct": 1,
                    "explanation": "Glycerol has a specific gravity of ~1.26 and separates rapidly to the bottom of the less dense FAME ester layer (~0.88)."
                },
                {
                    "question": "If FAME yield is 82.2% at a molar ratio of 6.0 under Y = 5.2000 · R_m + 51.0000, what is the yield at R_m = 8.0?",
                    "options": ["87.4%", "92.6%", "95.0%", "98.2%"],
                    "correct": 1,
                    "explanation": "Y = 5.2000 · 8.0 + 51.0000 = 41.6 + 51.0 = 92.6%."
                }
            ],
            "settings": ["Feedstock: Refined jatropha seed oil (FFA 0.65%)", "Catalyst: 1.0% wt/wt potassium hydroxide (KOH)", "Reaction conditions: 60.0 °C, 600 RPM, 60 minutes"],
            "samples": [3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "⚗️", "label": "1. Transesterification Reactor"},
                {"id": "compare", "icon": "📊", "label": "2. Ester Yield vs Molar Ratio"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Biodiesel Kinetics Sandbox"}
            ]
        },
        {
            "number": 41,
            "slug": "solar-pv-submersible-water-pump-hydraulic-performance",
            "title": "Solar PV Submersible Water Pump Hydraulic Array Performance",
            "shortTitle": "Solar PV Submersible Pump",
            "aim": "Evaluate the electrical-to-hydraulic power conversion efficiency and water discharge rate of a solar PV-powered brushless submersible drip irrigation pump across varying solar irradiance power levels.",
            "inputLabel": "Array Electrical Power P_elec",
            "shortInput": "Power P_el",
            "inputUnit": "W",
            "min": 200,
            "max": 950,
            "step": 150,
            "initial": 500,
            "inputDecimals": 0,
            "rawLabel": "Hydraulic Output Power P_hyd",
            "rawUnit": "W",
            "rawDecimals": 2,
            "xAxis": "Array electrical power P_elec (W)",
            "yAxis": "Hydraulic power P_hyd (W)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 600,
            "emptyY": 400,
            "targetName": "Subsystem Power Conversion Efficiency η_sys",
            "target": "0.6800",
            "refValue": 0.6800,
            "resultUnit": "ratio",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "P_hyd = η_sys · P_elec = 0.6800 · P_elec",
            "intro": "Solar photovoltaic (PV) powered water pumping systems represent one of the most critical renewable energy technologies for agricultural irrigation, livestock watering, and rural domestic water supply, particularly in off-grid arid and semi-arid regions. Modern agricultural solar pumping systems utilize high-efficiency permanent magnet brushless DC (BLDC) submersible motors coupled to multistage centrifugal or helical rotor pumps, driven through maximum power point tracking (MPPT) variable frequency inverters. Unlike conventional grid-powered pumps operating at fixed rotational speed, solar pumps operate under continuously varying solar irradiance and electrical power inputs. Sizing PV arrays, pump head capacity, and daily water delivery requires an accurate assessment of the subsystem power conversion efficiency η_sys, which relates incoming DC electrical power from the PV array P_elec to useful hydraulic water power delivered: P_hyd = ρ_w · g · Q · H, where ρ_w is water density, g is gravitational acceleration, Q is volumetric discharge flow rate (m³/s), and H is total dynamic head (m). Over the operational working range of the MPPT inverter, hydraulic output power scales in direct linear proportion to array electrical power through the subsystem efficiency η_sys = P_hyd / P_elec. In this experiment, a 1.0 kW submersible solar pump installed in a deep-well test column is tested across simulated PV electrical power levels to evaluate hydraulic discharge, power conversion efficiency, and motor-pump operating characteristics.",
            "modelExtra": "Evaluated on a 1.0 kW rated multistage centrifugal submersible pump with integrated MPPT BLDC motor controller pumping against a fixed total dynamic head H = 35.0 m. Electrical power input is varied from 200 W to 950 W.",
            "apparatus": [
                {"name": "Submersible Deep-Well Test Column", "purpose": "Vertical water test riser (diameter 150 mm, depth 40 m) equipped with calibrated backpressure throttling valve."},
                {"name": "Multistage Centrifugal BLDC Solar Pump", "purpose": "1.0 kW submersible water pump with high-efficiency brushless DC permanent magnet motor."},
                {"name": "Solar Array Electrical Simulator", "purpose": "Programmable DC power supply (0-150 V, 0-15 A) reproducing solar PV I-V curves across varying irradiance."},
                {"name": "Electromagnetic Pipe Flowmeter", "purpose": "Measures continuous water discharge flow rate Q with 0.1% volumetric accuracy."},
                {"name": "Piezo-Resistive Pressure Transducer", "purpose": "Monitors discharge head at pump outlet to compute exact total dynamic head (TDH) in meters."},
                {"name": "High-Precision DC Power Analyzer", "purpose": "Simultaneously logs array DC voltage, current, and true electrical power input to the MPPT controller."}
            ],
            "procedure": [
                {"title": "Test Column Priming and Pressure Calibration", "text": "Submerge the pump assembly, purge air from the discharge column, and adjust the throttle valve to maintain constant 35.0 m total dynamic head."},
                {"title": "DC Power Simulator Initialization", "text": "Configure the programmable DC power supply to simulate the output of a 1.2 kWp solar PV array at an initial power level of 200 W."},
                {"title": "MPPT Inverter Tracking Stabilization", "text": "Energize the motor controller and allow 3 minutes for the internal MPPT algorithm to track the optimum power voltage and stabilize pump RPM."},
                {"title": "Hydraulic Flow and Pressure Acquisition", "text": "Record stabilized discharge flow rate Q (m³/h), delivery pressure head H (m), DC voltage V_dc, and current I_dc over a 5-minute sampling window."},
                {"title": "Electrical Power Progression Sequence", "text": "Increment PV simulator power through 350, 500, 650, 800, and 950 W, repeating hydraulic power and telemetry logging at each step."},
                {"title": "Hydraulic Power Calculation and Regression", "text": "Calculate hydraulic power P_hyd = ρ · g · Q · H and plot against array electrical power P_elec, computing subsystem efficiency η_sys."}
            ],
            "topics": [
                {"question": "How is useful hydraulic water power defined and calculated?", "answer": "Hydraulic power is the mechanical energy transferred to the pumped water stream per unit time: P_hyd = ρ · g · Q · H, where ρ is water density (1000 kg/m³), g is gravitational acceleration (9.81 m/s²), Q is discharge rate (m³/s), and H is total dynamic head (m). Expressed in Watts, P_hyd = (Q in m³/h × H in m) / 0.367."},
                {"question": "What is the function of the Maximum Power Point Tracker (MPPT) in solar water pumping?", "answer": "The MPPT controller continuously adjusts electrical impedance to operate the PV modules at their maximum power voltage (V_mp) and current (I_mp) regardless of changing sunlight levels and cell temperatures, maximizing energy delivered to the pump motor."},
                {"question": "Why are Brushless DC (BLDC) permanent magnet motors preferred over conventional AC induction motors in solar pumps?", "answer": "BLDC motors offer significantly higher electrical efficiency (85% to 92% compared to 70% to 78% for small AC motors), superior starting torque at low solar irradiance, reduced maintenance (no brushes or commutators), and lower heat dissipation."},
                {"question": "What is the threshold solar irradiance required for a solar pump to initiate water discharge?", "answer": "Solar pumps require a minimum electrical power threshold (typically 15% to 25% of rated power, corresponding to ~150 to 200 W/m² irradiance) to overcome static head and mechanical bearing friction before water starts discharging at the surface."},
                {"question": "Why is water storage in elevated tanks generally preferred over battery electrical storage in agricultural solar pumping?", "answer": "Storing potential energy as pumped water in overhead reservoirs is vastly cheaper, longer-lasting (20+ year tank lifespan vs 3-5 years for batteries), virtually maintenance-free, and avoids battery round-trip charge/discharge efficiency losses."},
                {"question": "How does total dynamic head (TDH) affect pump discharge flow rate at constant solar irradiance?", "answer": "Under constant electrical power input, pump discharge flow rate Q is inversely proportional to total dynamic head H (Q ≈ P_hyd / (ρ·g·H)); doubling the head cuts delivery flow roughly in half."}
            ],
            "precautions": [
                "Verify constant discharge pressure head across all power levels using the calibrated throttling valve.",
                "Ensure submersible pump motor remains fully submerged to prevent motor winding overheating.",
                "Allow the MPPT controller sufficient time to converge on the true global power peak after each power change.",
                "Verify zero pipe leakage throughout the test column and calibration manifolds."
            ],
            "limitations": [
                "The linear power relationship applies above the minimum cut-in threshold (P_elec ≥ 200 W).",
                "Assumes clean water without suspended sand or abrasive sediments that cause impeller wear.",
                "Evaluated at constant fluid temperature (20.0 °C); warm water alters fluid density and motor cooling.",
                "Applies to a constant total dynamic head of 35.0 m; varying head shifts the pump operating point along its H-Q curve."
            ],
            "quiz": [
                {
                    "question": "What is the mathematical equation for useful hydraulic water power P_hyd?",
                    "options": ["P_hyd = V · I", "P_hyd = ρ · g · Q · H", "P_hyd = 0.5 · m · v²", "P_hyd = F / A"],
                    "correct": 1,
                    "explanation": "Hydraulic power is the rate of potential and pressure energy added to fluid: P_hyd = density × gravity × flow rate × head."
                },
                {
                    "question": "Why is maximum power point tracking (MPPT) vital in solar pumping systems?",
                    "options": ["It reverses water flow", "It continuously matches electrical load to extract peak solar PV panel wattage", "It charges the solar panels", "It prevents water freezing"],
                    "correct": 1,
                    "explanation": "MPPT dynamic impedance matching extracts the absolute maximum electrical wattage available from solar panels under varying sun intensity."
                },
                {
                    "question": "If measured hydraulic power is 340 W at an array electrical power input of 500 W, what is the subsystem efficiency?",
                    "options": ["0.34", "0.50", "0.68", "0.85"],
                    "correct": 2,
                    "explanation": "Subsystem efficiency η_sys = P_hyd / P_elec = 340 W / 500 W = 0.68 (or 68%)."
                },
                {
                    "question": "In off-grid agricultural solar pumping, what is the most economical method for storing energy for non-sunny hours?",
                    "options": ["Lead-acid batteries", "Elevated water storage tanks", "Flywheel kinetic storage", "Hydrogen fuel cells"],
                    "correct": 1,
                    "explanation": "Pumping water into elevated gravity storage tanks during peak sun is far more economical, durable, and reliable than electrical battery banks."
                }
            ],
            "settings": ["Pump model: 1.0 kW BLDC submersible multistage centrifugal", "Total dynamic head: Constant 35.0 m (343 kPa)", "Water medium: Clean potable water (20.0 °C)"],
            "samples": [200, 350, 500, 650, 800, 950],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💧", "label": "1. Deep-Well Pumping Column"},
                {"id": "compare", "icon": "📊", "label": "2. Hydraulic vs Electric Power"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Solar Irrigation Sandbox"}
            ]
        },
        {
            "number": 42,
            "slug": "variable-rate-precision-fertilizer-fluted-roller-kinetics",
            "title": "Variable-Rate Precision Fertilizer Fluted-Roller Actuation Kinetics",
            "shortTitle": "Variable-Rate Fertilizer Metering",
            "aim": "Calibrate mass discharge response, dynamic latency, and distribution linearity of an electro-hydraulic variable-rate granular fertilizer metering roller across stepper motor drive speeds.",
            "inputLabel": "Roller Drive Speed ω",
            "shortInput": "Drive Speed ω",
            "inputUnit": "RPM",
            "min": 10,
            "max": 60,
            "step": 10,
            "initial": 30,
            "inputDecimals": 0,
            "rawLabel": "Fertilizer Mass Flow Rate m_dot_f",
            "rawUnit": "kg/min",
            "rawDecimals": 3,
            "xAxis": "Roller drive speed ω (RPM)",
            "yAxis": "Mass flow rate m_dot_f (kg/min)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 35,
            "emptyY": 5.5,
            "targetName": "Mass Metering Speed Gradient c_m",
            "target": "0.1650",
            "refValue": 0.1650,
            "resultUnit": "(kg/min)/RPM",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "m_dot_f = c_m · ω = 0.1650 · ω",
            "intro": "Precision agriculture relies on variable-rate application (VRA) technology to apply granular fertilizers (urea, diammonium phosphate, potash) in site-specific quantities according to spatial soil fertility maps, vegetative greenness indices (NDVI), and real-time yield goals. Modern precision grain drills and air seeders modulate fertilizer application on-the-go by driving fluted-roller metering mechanisms with electronically controlled brushless servomotors or stepper drives interfaced via the ISOBUS (ISO 11783) standard. The metering mechanism captures granular fertilizer within external helical flutes from the hopper throat and discharges it into pneumatic venturi delivery tubes. Agronomic field efficacy requires that the instantaneous mass discharge rate m_dot_f responds in strict linear proportionality to roller angular speed ω, ensuring that rapid prescription rate adjustments and ground speed compensations do not result in over- or under-fertilization. In this laboratory experiment, a commercial variable-rate precision fluted-roller metering unit mounted on a dynamic test bench is evaluated across drive speeds from 10 to 60 RPM using continuous gravimetric load cell weighing to calibrate discharge linearity, verify flute filling efficiency, and determine the mass metering speed gradient c_m.",
            "modelExtra": "Evaluated on granular urea fertilizer (bulk density 760 kg/m³, granule diameter 2.5-3.5 mm) using a helical fluted metering roller (flute length 50 mm, 12 flutes) driven by an ISOBUS-controlled stepper motor. Gravimetric collection is evaluated across 10 to 60 RPM.",
            "apparatus": [
                {"name": "Precision Variable-Rate Metering Test Bench", "purpose": "Rigid aluminum mounting frame supporting gravity hopper, fluted roller assembly, and motor drive."},
                {"name": "Helical Fluted Metering Roller Assembly", "purpose": "Hardened polymer 12-flute metering wheel designed for controlled positive-displacement granular metering."},
                {"name": "Closed-Loop ISOBUS Stepper Motor Drive", "purpose": "Regulates roller angular speed from 5 to 80 RPM within ±0.2 RPM precision via CAN-bus commands."},
                {"name": "Dynamic Continuous Gravimetric Weighing Platform", "purpose": "Measures discharged fertilizer mass in real-time with 0.1 g resolution and 50 Hz digital filtering."},
                {"name": "Optical Shaft Speed Encoder", "purpose": "Monitors exact instantaneous shaft rotation and detects any motor step loss or mechanical jamming."},
                {"name": "Digital Particle Sieve & Moisture Analyzer", "purpose": "Verifies standardized granule size distribution and moisture content (< 0.5%) before test trials."}
            ],
            "procedure": [
                {"title": "Fertilizer Conditioning and Hopper Loading", "text": "Inspect granular urea for caking, pass through a 4.0 mm conditioning screen, and charge the 30-liter feed hopper."},
                {"title": "Motor Controller Zeroing and CAN Calibration", "text": "Initialize the stepper motor drive, verify zero backlash, and set the controller to 10 RPM test velocity."},
                {"title": "Pre-Run Flute Priming", "text": "Operate the roller for 60 seconds to ensure all 12 helical flute pockets are fully primed with granular material."},
                {"title": "Dynamic Gravimetric Mass Flow Acquisition", "text": "Initiate continuous mass data collection on the electronic catch scale over a precisely timed 60-second discharge window."},
                {"title": "Speed Progression Sequence", "text": "Systematically increase roller speed to 20, 30, 40, 50, and 60 RPM, recording 60-second gravimetric discharge collections at each speed."},
                {"title": "Linearity Regression and Gradient Analysis", "text": "Plot mass flow rate m_dot_f (kg/min) against drive speed ω (RPM), performing least-squares linear regression to determine c_m."}
            ],
            "topics": [
                {"question": "How does an ISOBUS variable-rate applicator modulate fertilizer application in the field?", "answer": "The task controller reads tractor GPS coordinates, matches them with a digital prescription grid map, calculates the target mass rate per hectare, factors in ground speed from radar, and issues real-time CAN-bus RPM commands to the metering motor."},
                {"question": "Why is a helical fluted roller preferred over a straight fluted roller?", "answer": "Straight fluted rollers release fertilizer in pulsating bursts as each flute clears the cutoff gate; helical flutes provide continuous, smooth discharge with minimal cyclic pulsation."},
                {"question": "What is the physical significance of the mass metering speed gradient c_m?", "answer": "The gradient c_m represents the mass of granular material discharged per revolution of the metering shaft (expressed in (kg/min)/RPM or kg/revolution), directly reflecting the geometric displacement volume and filling efficiency of the flutes."},
                {"question": "Why does flute filling efficiency decline at extremely high roller rotational speeds?", "answer": "At very high speeds (> 70-80 RPM), gravity does not allow sufficient time for granules to drop into and completely fill the passing flute pockets, causing volumetric filling efficiency to drop and introducing non-linearity."},
                {"question": "How does fertilizer hygroscopicity affect variable-rate metering accuracy?", "answer": "Fertilizers like urea and ammonium nitrate are highly hygroscopic; absorbing atmospheric moisture causes granules to soften, cake, and bridge across hopper throats, altering bulk density and flowability."},
                {"question": "What is the function of the bottom cutoff brush/gate in a fluted roller meter?", "answer": "The adjustable cutoff gate controls the clearance beneath the roller, shearing off excess grain and preventing uncontrolled gravity dribble when the roller stops turning."}
            ],
            "precautions": [
                "Ensure granular fertilizer is dry and free of lumps to prevent hopper bridging or jamming in flute pockets.",
                "Prime the metering roller for at least 30 seconds before initiating mass logging at each new speed.",
                "Verify accurate catch duration with high-precision digital electronic timer synchronizing scale tares.",
                "Maintain constant material head in the feed hopper to prevent head-pressure variations."
            ],
            "limitations": [
                "The linear metering model applies within the operational speed range of 10 to 60 RPM.",
                "Assumes free-flowing, non-cohesive granular fertilizer with consistent bulk density.",
                "Does not model pneumatic conveying lag times between meter discharge and soil injection coulters.",
                "Specific to granular urea; denser fertilizers like DAP (bulk density 960 kg/m³) produce steeper gradients."
            ],
            "quiz": [
                {
                    "question": "What international communication standard connects tractors, GPS displays, and variable-rate implements?",
                    "options": ["RS-232", "ISOBUS (ISO 11783)", "Bluetooth 5.0", "Modbus RTU"],
                    "correct": 1,
                    "explanation": "ISOBUS (ISO 11783) is the universal agricultural standard enabling electronic communication between tractors and smart implements."
                },
                {
                    "question": "Why do helical fluted rollers provide superior metering compared to straight flutes?",
                    "options": ["They crush granules finer", "They eliminate pulsating discharge cycles, ensuring continuous flow", "They use less electrical power", "They prevent rust"],
                    "correct": 1,
                    "explanation": "Helical flute geometry discharges fertilizer smoothly and continuously without the cyclic pulsing pulses of straight flutes."
                },
                {
                    "question": "If measured mass flow rate is 4.95 kg/min at a drive speed of 30 RPM, what is the metering gradient c_m?",
                    "options": ["0.0825 (kg/min)/RPM", "0.1650 (kg/min)/RPM", "0.3300 (kg/min)/RPM", "0.4950 (kg/min)/RPM"],
                    "correct": 1,
                    "explanation": "c_m = m_dot_f / ω = 4.95 kg/min / 30 RPM = 0.1650 (kg/min)/RPM."
                },
                {
                    "question": "What problem occurs if fertilizer absorbs excessive moisture during field storage?",
                    "options": ["Granules become lighter than air", "Caking and bridging occur in hopper throats, disrupting metering", "Fertilizer turns into petrol", "Roller RPM increases uncontrollably"],
                    "correct": 1,
                    "explanation": "Moisture absorption causes hygroscopic fertilizer granules to clump, causing bridging, clogging, and inaccurate delivery."
                }
            ],
            "settings": ["Fertilizer: Granular urea (bulk density 760 kg/m³, size 2.5-3.5 mm)", "Roller: Helical polymer 12-flute (length 50 mm)", "Drive motor: ISOBUS closed-loop stepper with optical encoder"],
            "samples": [10, 20, 30, 40, 50, 60],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "⚙️", "label": "1. Variable-Rate Metering Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Flow Rate vs RPM Linearity"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Precision Agronomy Sandbox"}
            ]
        }
    ]
