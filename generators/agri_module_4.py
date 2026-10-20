# -*- coding: utf-8 -*-
"""Agricultural Engineering Module 4: Agricultural Structures & Environmental Control (Labs 29–35)."""

def get_module_4():
    return [
        {
            "number": 29,
            "slug": "janssen-deep-bin-grain-pressure-distribution",
            "title": "Janssen Deep-Bin Grain Pressure Distribution & Wall Friction",
            "shortTitle": "Janssen Bin Pressure",
            "aim": "Measure vertical and lateral static grain pressures in a deep storage silo as a function of depth and validate Janssen's bin pressure theory.",
            "inputLabel": "Grain Depth z",
            "shortInput": "Depth z",
            "inputUnit": "m",
            "min": 1.0,
            "max": 6.0,
            "step": 1.0,
            "initial": 3.0,
            "inputDecimals": 1,
            "rawLabel": "Lateral Wall Pressure L",
            "rawUnit": "kPa",
            "rawDecimals": 4,
            "xAxis": "Grain depth z (m)",
            "yAxis": "Lateral pressure L (kPa)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.5,
            "emptyY": 8.5,
            "targetName": "Lateral Pressure Gradient k_L",
            "target": "2.4500",
            "refValue": 2.4500,
            "resultUnit": "kPa/m",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "L = k_L · z = 2.4500 · z",
            "intro": "In structural agricultural engineering, the design of bulk grain storage silos, bins, and elevator hoppers requires precise knowledge of the internal stress distribution exerted by ensiled granular agricultural crops. Unlike hydrostatic liquids where pressure increases linearly without bound, stored agricultural grains support shear stresses through inter-granular internal friction and friction against the bin walls. H.A. Janssen in 1895 derived the fundamental differential equation of deep-bin pressure by balancing the gravitational weight of a differential grain slice against the vertical support of lateral friction along the perimeter walls. For deep bins where height exceeds twice the diameter, wall friction transfers a major fraction of the vertical grain weight directly into the bin walls, causing both vertical and lateral pressures to asymptote toward a limiting maximum value. In the upper depth range examined in this experiment, the lateral wall pressure L (related to vertical pressure V through Rankine's lateral pressure ratio k = L/V) increases with depth with an effective pressure gradient k_L governed by bulk density, internal friction angle, and wall friction coefficient. In this laboratory investigation, an instrumented cylindrical model grain silo equipped with flush diaphragm pressure transducers and wall strain gauges is loaded with hard red winter wheat to measure static wall pressures across incremental grain fill depths.",
            "modelExtra": "Evaluated on hard red winter wheat (bulk density 785 kg/m³, internal friction angle 27°) in a cylindrical smooth-galvanized steel bin of hydraulic radius R = 0.50 m. Linearized lateral pressure gradient is determined across depth intervals up to 6.0 m before asymptotic saturation dominates.",
            "apparatus": [
                {"name": "Instrumented Cylindrical Silo Model", "purpose": "Provides a rigid vertical storage bin (diameter 1.2 m, height 7.0 m) fabricated with galvanized structural steel rings."},
                {"name": "Flush Diaphragm Pressure Transducers", "purpose": "Measures lateral static grain pressure normal to the bin wall at 1.0-meter vertical intervals without disturbing grain flow."},
                {"name": "Base Support Load Cells", "purpose": "Quantifies the total vertical floor reaction to determine the fraction of grain weight supported by bottom versus perimeter walls."},
                {"name": "Wheat Grain Elevator & Distributor", "purpose": "Fills the silo uniformly along the central vertical axis to establish axisymmetric grain packing and prevent eccentric loading."},
                {"name": "Multi-Channel Bridge Telemetry Unit", "purpose": "Samples strain and piezoresistive pressure voltages with 24-bit resolution and temperature compensation."},
                {"name": "Grain Sampling Tripper", "purpose": "Extracts grain samples at varying depths to verify uniform packing bulk density and moisture content."}
            ],
            "procedure": [
                {"title": "Zero-Load Transducer Calibration", "text": "Inspect all wall-mounted pressure transducers, balance Wheatstone bridge circuits, and log baseline zero offsets before grain loading begins."},
                {"title": "Axial Central Filling", "text": "Operate the bucket elevator and overhead distributor spout to deliver hard red winter wheat down the centerline, minimizing grain trajectory kinetic energy."},
                {"title": "Depth Increment Stabilization", "text": "Pause grain loading at 1.0-meter fill depth increments (from 1.0 m to 6.0 m), allowing grain packing settlement for 15 minutes before reading telemetry."},
                {"title": "Lateral Wall Pressure Acquisition", "text": "Record lateral wall pressures at all submerged transducer heights and compute average wall pressure at each surveyed depth level."},
                {"title": "Vertical Floor Load Logging", "text": "Measure total floor load cell reaction and compare with total mass of grain ensiled to calculate percentage wall friction support."},
                {"title": "Regression and Gradient Evaluation", "text": "Plot lateral wall pressure L versus grain fill depth z, performing least-squares linear regression to extract the lateral pressure gradient k_L."}
            ],
            "topics": [
                {"question": "How does grain pressure in a deep silo differ fundamentally from fluid hydrostatic pressure?", "answer": "In hydrostatic fluids, pressure increases linearly with depth without limit (P = ρ·g·z) and is equal in all directions. In bulk grains, internal friction and friction against silo walls support a large fraction of the vertical weight, causing pressure to asymptote to a maximum asymptote defined by Janssen's equation."},
                {"question": "What is Rankine's lateral pressure ratio k in grain storage mechanics?", "answer": "Rankine's lateral pressure ratio k is the ratio of horizontal lateral wall pressure to vertical grain pressure (k = L / V), typically calculated for active conditions as k = (1 - sin φ) / (1 + sin φ), where φ is the internal angle of friction of the grain mass."},
                {"question": "What geometric criterion distinguishes a deep bin from a shallow bin in ASABE standards?", "answer": "Under ASABE EP433 and classical structural criteria, a bin is classified as deep if the plane of rupture extending from the bottom wall intersection intersects the grain surface before contacting the opposite wall (typically when depth-to-diameter ratio H/D > 1.5 to 2.0)."},
                {"question": "Why do overpressures occur during grain discharge from a silo hopper?", "answer": "During discharge, the static active stress field converts into a dynamic passive stress field; arched stress trajectories collapse, leading to dynamic switch pressures at the bin-hopper transition that can multiply local wall stresses by 1.5 to 2.5 times static values."},
                {"question": "How does grain moisture content affect silo wall pressures?", "answer": "Higher grain moisture increases the coefficient of wall friction μ' and internal friction angle, lowering the asymptotic maximum pressure, but can induce dangerous localized swelling pressures if moisture ingress occurs after filling."},
                {"question": "What is the physical meaning of the hydraulic radius R of a storage bin?", "answer": "The hydraulic radius R is defined as the cross-sectional area of the bin divided by its inside perimeter (R = A / U). For a circular silo of diameter D, R = (π D² / 4) / (π D) = D / 4."}
            ],
            "precautions": [
                "Ensure central axial grain discharge and filling to avoid asymmetric loading and catastrophic shell buckling.",
                "Allow sufficient settling time after each fill increment for inter-particle friction to establish static equilibrium.",
                "Verify that diaphragm pressure transducers sit strictly flush with the interior wall surface to avoid localized stress concentrations.",
                "Check that grain moisture content remains stable throughout the experiment to prevent swelling artifacts."
            ],
            "limitations": [
                "The linear model represents the initial pre-asymptotic depth regime (z ≤ 6.0 m) for the 1.2 m diameter test bin.",
                "Assumes axisymmetric grain packing and constant bulk density throughout the grain volume.",
                "Neglects dynamic thermal ratcheting caused by daily ambient temperature fluctuations.",
                "Applies strictly to static conditions; does not model dynamic mass flow discharge overpressures."
            ],
            "quiz": [
                {
                    "question": "Who derived the fundamental mathematical theory describing grain pressures in deep storage bins?",
                    "options": ["H.A. Janssen", "Carl von Terzaghi", "G. Gorjatschkin", "W.J.M. Rankine"],
                    "correct": 0,
                    "explanation": "H.A. Janssen published his seminal differential balance equation for deep bin pressures in 1895."
                },
                {
                    "question": "What happens to vertical grain pressure at very large depths in a deep silo?",
                    "options": ["Increases exponentially", "Approaches a finite asymptotic maximum value", "Drops to zero", "Oscillates periodically"],
                    "correct": 1,
                    "explanation": "Because wall friction absorbs vertical grain weight, vertical pressure approaches a constant asymptotic limit: V_max = (ρ·g·R)/(μ'·k)."
                },
                {
                    "question": "For a circular silo of internal diameter D, what is the hydraulic radius R?",
                    "options": ["D / 2", "D / 4", "π · D", "D² / 4"],
                    "correct": 1,
                    "explanation": "Hydraulic radius is cross-sectional area divided by perimeter: (π D² / 4) / (π D) = D / 4."
                },
                {
                    "question": "If measured lateral pressure is 7.35 kPa at a depth of 3.0 m, what is the lateral pressure gradient?",
                    "options": ["1.20 kPa/m", "2.45 kPa/m", "4.90 kPa/m", "7.35 kPa/m"],
                    "correct": 1,
                    "explanation": "The lateral pressure gradient is k_L = L / z = 7.35 kPa / 3.0 m = 2.45 kPa/m."
                }
            ],
            "settings": ["Stored crop: Hard red winter wheat", "Silo geometry: D = 1.2 m circular galvanized steel", "Ambient temperature: 20.0 °C"],
            "samples": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🏢", "label": "1. Silo Test Cell"},
                {"id": "compare", "icon": "📊", "label": "2. Janssen Pressure Profile"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Bin Wall Friction Sandbox"}
            ]
        },
        {
            "number": 30,
            "slug": "greenhouse-thermal-heat-loss-overall-u-factor",
            "title": "Greenhouse Thermal Heat Loss & Overall U-Factor Assessment",
            "shortTitle": "Greenhouse Thermal Loss",
            "aim": "Evaluate the sensible heat loss from an agricultural greenhouse enclosure across varying indoor-outdoor temperature differentials to determine the overall heat transfer coefficient (U-factor).",
            "inputLabel": "Temperature Difference ΔT",
            "shortInput": "ΔT",
            "inputUnit": "°C",
            "min": 5.0,
            "max": 30.0,
            "step": 5.0,
            "initial": 15.0,
            "inputDecimals": 1,
            "rawLabel": "Heat Loss Flux q_h",
            "rawUnit": "W/m²",
            "rawDecimals": 3,
            "xAxis": "Temperature difference ΔT (°C)",
            "yAxis": "Heat loss flux q_h (W/m²)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 17.5,
            "emptyY": 100.0,
            "targetName": "Overall Heat Transfer Coefficient U_ov",
            "target": "5.8000",
            "refValue": 5.8000,
            "resultUnit": "W/(m²·°C)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "q_h = U_ov · ΔT = 5.8000 · ΔT",
            "intro": "Controlled environment agriculture (CEA) relies heavily on greenhouses to cultivate high-value horticultural crops outside standard growing seasons. However, the high solar transmittance of greenhouse glazing materials (single or double polyethylene, polycarbonate, or glass) is accompanied by substantial thermal conductance and long-wave infrared radiation loss during cold nighttime hours. Sizing heating systems and modeling heating energy budgets require an accurate determination of the overall heat transmission coefficient U_ov (U-factor). In thermal engineering of agricultural structures, steady-state heat loss per unit envelope surface area q_h is governed by Fourier's law and boundary layer convection: q_h = U_ov · (T_in - T_out) = U_ov · ΔT. The overall coefficient U_ov integrates interior natural convection, thermal conduction through glazing and structural framing, and exterior forced convection driven by ambient wind speed. In this laboratory investigation, an experimental research greenhouse bay with double-layer inflated polyethylene film is instrumented with calibrated thermopile heat flux plates, aspirated psychrometers, and precision electrical resistance heaters to evaluate steady-state thermal loss across controlled temperature differentials.",
            "modelExtra": "Evaluated during nocturnal steady-state conditions (zero solar radiation) with double-polyethylene glazing under steady calm wind conditions (ambient wind speed 1.5 m/s). Heat loss includes combined envelope conduction, convection, and long-wave radiation.",
            "apparatus": [
                {"name": "Research Greenhouse Test Bay", "purpose": "Provides a controlled agricultural enclosure (6.0 m span, 12.0 m length) with double-layer inflated polyethylene cover."},
                {"name": "Calibrated Electrical Convective Heaters", "purpose": "Supplies regulated thermal energy inputs with solid-state SCR power controllers and power meters."},
                {"name": "Thermopile Heat Flux Transducers", "purpose": "Measures conductive-convective heat flow directly through representative glazing panels in W/m²."},
                {"name": "Aspirated Psychrometric Towers", "purpose": "Monitors vertical indoor and outdoor dry-bulb and wet-bulb temperatures with 0.05 °C accuracy."},
                {"name": "Infrared Thermal Imaging Radiometer", "purpose": "Scans structural ribs, perimeter sills, and glazing surfaces to detect localized infiltration thermal bridges."},
                {"name": "Micro-Anetometer & Weather Station", "purpose": "Logs exterior ambient air velocity, wind direction, and nocturnal clear-sky longwave radiation."}
            ],
            "procedure": [
                {"title": "Nocturnal Test Standardization", "text": "Initiate testing at least two hours after sunset to ensure zero solar thermal storage influence in the floor and soil profile."},
                {"title": "Heating Power Step Input", "text": "Energize internal electric heaters to establish an initial indoor-outdoor temperature difference ΔT of approximately 5 °C."},
                {"title": "Thermal Equilibrium Verification", "text": "Maintain heater output until all interior aspirated thermocouples and heat flux plates achieve steady-state (dT/dt < 0.2 °C/h for 30 minutes)."},
                {"title": "Synchronous Telemetry Acquisition", "text": "Log heater power consumption, individual heat flux sensor signals, and spatial air temperatures over a 15-minute integration window."},
                {"title": "Incremental Differential Progression", "text": "Increment the heating controller through 10, 15, 20, 25, and 30 °C differentials, repeating steady-state heat loss logging at each step."},
                {"title": "U-Factor Regression Analysis", "text": "Plot envelope heat loss flux q_h against temperature difference ΔT, fitting a linear regression line to compute overall U_ov."}
            ],
            "topics": [
                {"question": "What is the physical meaning of the overall heat transfer coefficient (U-factor)?", "answer": "The U-factor represents the steady-state thermal transmission rate per unit surface area per degree temperature difference across the envelope (expressed in W/(m²·°C) or W/(m²·K)). A lower U-factor indicates superior thermal insulating performance."},
                {"question": "How does double-layer inflated polyethylene reduce greenhouse heat loss compared to single glazing?", "answer": "The 5 to 10 cm dead-air space maintained between the inflated films acts as a stagnant insulating boundary layer, substantially lowering conductive-convective heat transfer and cutting heating demand by 30% to 40% compared to single glass or single poly."},
                {"question": "How does exterior wind speed influence greenhouse U-factors?", "answer": "Higher exterior wind speeds increase the external convective heat transfer coefficient (h_o) by thinning the laminar boundary layer on the outer glazing surface, significantly increasing the overall U-factor."},
                {"question": "What is thermal radiation trapping (the greenhouse effect)?", "answer": "Glazing materials are transparent to shortwave solar radiation (0.3 to 3.0 μm) which heats indoor surfaces, but largely opaque to longwave thermal infrared radiation (3.0 to 50 μm) emitted by interior surfaces, trapping heat inside the structure."},
                {"question": "Why is structural frame heat loss significant in commercial greenhouses?", "answer": "Aluminum and steel structural mullions have thermal conductivities thousands of times higher than glazing air spaces, acting as thermal bridges that can account for 10% to 20% of total envelope heat loss."},
                {"question": "How is structural infiltration heat loss distinguished from envelope transmission loss?", "answer": "Envelope transmission occurs via conduction, convection, and radiation through solid surfaces, whereas infiltration represents sensible heat lost through physical air exchange through cracks, laps, and vents, quantified as Q_inf = V_dot · ρ · C_p · ΔT."}
            ],
            "precautions": [
                "Conduct all testing during nocturnal periods to prevent shortwave solar radiation and thermal lag errors.",
                "Ensure greenhouse ventilation louvers and perimeter access doors are fully sealed with weatherstripping.",
                "Maintain uniform air circulation with low-velocity horizontal air flow (HAF) fans to eliminate thermal stratification.",
                "Avoid tests during sudden wind gusts or precipitation events that alter exterior convection dynamics."
            ],
            "limitations": [
                "The linear relation assumes a constant external convective boundary layer valid under calm ambient wind (≤ 2.0 m/s).",
                "Does not account for latent heat loss associated with internal plant transpiration and condensation on glazing.",
                "Neglects deep soil perimeter conductive heat losses through foundation walls.",
                "Assumes grey-body radiative heat exchange between outer glazing and sky vault."
            ],
            "quiz": [
                {
                    "question": "What are the standard SI units for the greenhouse overall heat transfer coefficient (U-factor)?",
                    "options": ["W / m²", "W / (m² · °C)", "J / (kg · °C)", "kW · h / m²"],
                    "correct": 1,
                    "explanation": "The overall heat transfer coefficient U is expressed in Watts per square meter per degree Celsius (W/(m²·°C)) or W/(m²·K)."
                },
                {
                    "question": "Compared to single-layer glass, inflating two layers of polyethylene film typically reduces greenhouse heat loss by:",
                    "options": ["5% to 10%", "30% to 40%", "70% to 80%", "No reduction occurs"],
                    "correct": 1,
                    "explanation": "Double-layer inflated polyethylene creates a stagnant insulating air blanket that reduces heat loss by roughly 30% to 40%."
                },
                {
                    "question": "If measured heat flux is 116.0 W/m² at an indoor-outdoor temperature difference of 20.0 °C, what is the U-factor?",
                    "options": ["2.90 W/(m²·°C)", "5.80 W/(m²·°C)", "8.70 W/(m²·°C)", "11.60 W/(m²·°C)"],
                    "correct": 1,
                    "explanation": "U_ov = q_h / ΔT = 116.0 W/m² / 20.0 °C = 5.80 W/(m²·°C)."
                },
                {
                    "question": "Which mode of heat loss is eliminated when greenhouse tests are conducted under zero-wind nocturnal conditions?",
                    "options": ["Envelope conduction", "Direct shortwave solar gain", "Thermal radiation", "Internal convection"],
                    "correct": 1,
                    "explanation": "Nighttime testing completely eliminates incoming shortwave solar radiation gains, isolating envelope thermal transmission."
                }
            ],
            "settings": ["Glazing type: Double-layer inflated polyethylene", "Wind speed: Steady 1.5 m/s", "Indoor circulation: Low-speed HAF active"],
            "samples": [5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🏡", "label": "1. Greenhouse Chamber"},
                {"id": "compare", "icon": "📊", "label": "2. Heat Flux vs Delta-T"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Thermal Envelope Sandbox"}
            ]
        },
        {
            "number": 31,
            "slug": "evaporative-cooling-pad-saturation-efficiency",
            "title": "Evaporative Cooling Pad Saturation Efficiency & Water Consumption Rate",
            "shortTitle": "Evaporative Pad Cooling",
            "aim": "Determine the cooling saturation efficiency and water evaporation rate of a cellulose wet-pad ventilation system under varying approach face air velocities.",
            "inputLabel": "Pad Face Air Velocity v_pad",
            "shortInput": "Face Velocity v",
            "inputUnit": "m/s",
            "min": 0.5,
            "max": 2.0,
            "step": 0.3,
            "initial": 1.1,
            "inputDecimals": 1,
            "rawLabel": "Water Evaporation Rate m_dot_w",
            "rawUnit": "g/(min·m²)",
            "rawDecimals": 3,
            "xAxis": "Pad face velocity v_pad (m/s)",
            "yAxis": "Evaporation rate m_dot_w (g/(min·m²))",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 1.25,
            "emptyY": 10.5,
            "targetName": "Evaporation Velocity Gradient k_w",
            "target": "8.5000",
            "refValue": 8.5000,
            "resultUnit": "(g/min·m²)/(m/s)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "m_dot_w = k_w · v_pad = 8.5000 · v_pad",
            "intro": "In agricultural environmental control, evaporative cooling pads coupled with negative-pressure exhaust fans provide the primary method for moderating extreme summer temperatures inside commercial greenhouses and intensive poultry or swine housing. Evaporative cooling operates on the psychrometric principle of adiabatic saturation: warm, unsaturated ambient air passes through a cross-fluted cellulose pad continuously wetted with recirculating water. Sensible heat from the airstream is absorbed as latent heat of vaporization, converting liquid water into water vapor, which lowers the dry-bulb air temperature toward the thermodynamic wet-bulb temperature while increasing relative humidity. Sizing water storage reservoirs, recirculation pumps, and bleed-off rates requires accurate knowledge of the water evaporation rate m_dot_w as a function of face air velocity v_pad. At higher face velocities, increased volumetric airflow drives a proportional increase in total moisture uptake across the pad face area. In this experiment, an instrumented wind tunnel test section containing a 100 mm thick cross-fluted cellulose pad is tested across varying approach velocities while monitoring psychrometric properties, airflow rates, and water mass depletion.",
            "modelExtra": "Evaluated on a 100 mm thick cross-fluted cellulose pad (flute angle 45°/15°) at standard ambient conditions (35.0 °C dry-bulb, 22.0 °C wet-bulb). Face air velocity is controlled between 0.5 and 2.0 m/s with uniform top-header water distribution.",
            "apparatus": [
                {"name": "Cross-Fluted Cellulose Pad Test Section", "purpose": "Provides standard 100 mm thick corrugated pad media (1.0 m wide by 1.0 m high) with top distribution header."},
                {"name": "Variable-Speed Centrifugal Exhaust Fan", "purpose": "Draws air through the wind tunnel to establish uniform face velocities from 0.5 to 2.0 m/s."},
                {"name": "Aspirated Dry & Wet Bulb Psychrometers", "purpose": "Measures upstream and downstream psychrometric states with calibrated precision thermistors."},
                {"name": "Water Recirculation Sump on Electronic Balance", "purpose": "Monitors net evaporative water consumption in real time with 1.0 gram gravimetric resolution."},
                {"name": "Rotameter Water Flow Indicator", "purpose": "Monitors pad wetting water flow rate to ensure complete wetting above the minimum dry-out threshold."},
                {"name": "Differential Pressure Inclined Manometer", "purpose": "Measures static pressure drop across the cooling pad in Pascals."}
            ],
            "procedure": [
                {"title": "Pad Pre-Wetting and Saturation", "text": "Energize the recirculation pump for 20 minutes to thoroughly wet the cellulose pad until uniform water curtaining is established."},
                {"title": "Initial Airflow Adjustment", "text": "Set the exhaust fan frequency drive to produce an approach face velocity of 0.5 m/s measured via multi-point pitot tube array."},
                {"title": "Steady-State Conditioning", "text": "Operate the system for 10 minutes until downstream dry-bulb temperature reaches steady equilibrium."},
                {"title": "Psychrometric and Gravimetric Logging", "text": "Record upstream and downstream dry-bulb and wet-bulb temperatures and log water reservoir mass depletion over a 15-minute window."},
                {"title": "Face Velocity Increment Progression", "text": "Increment face air velocity to 0.8, 1.1, 1.4, 1.7, and 2.0 m/s, repeating gravimetric and psychrometric measurements at each stage."},
                {"title": "Saturation Efficiency and Consumption Analysis", "text": "Calculate cooling saturation efficiency η_c = (T_db,in - T_db,out)/(T_db,in - T_wb,in) and plot evaporation rate m_dot_w against face velocity v_pad."}
            ],
            "topics": [
                {"question": "How is evaporative cooling saturation efficiency defined mathematically?", "answer": "Cooling efficiency (saturation effectiveness) is defined as η = (T_dry_in - T_dry_out) / (T_dry_in - T_wet_in) × 100%, where T_wet_in represents the theoretical thermodynamic limit of cooling achievable via adiabatic saturation."},
                {"question": "Why does cooling efficiency decline slightly as face air velocity increases?", "answer": "At higher face velocities, air residence time inside the wetted flutes decreases, giving sensible heat less contact time to transfer to the liquid boundary layer and reach thermal equilibrium."},
                {"question": "What is the function of the bleed-off water discharge in recirculating evaporative systems?", "answer": "Continuous evaporation leaves dissolved minerals and salts behind; bleed-off discharges a fraction of circulating water (typically 5% to 10%) to prevent scale accumulation, clogging, and algae growth on the pad media."},
                {"question": "Explain the significance of the 45°/15° unequal angle flute geometry in modern cellulose pads.", "answer": "The steeper 45° angle directs water toward the air-inlet face where evaporation demand is highest, flushing dirt outward, while the flatter 15° angle ensures adequate air contact and low static pressure drop."},
                {"question": "Under what ambient climate conditions is evaporative pad cooling most effective?", "answer": "Evaporative cooling is most effective in hot, arid climates where the wet-bulb depression (T_dry - T_wet) is large (often 10 °C to 18 °C), yielding substantial temperature drops."},
                {"question": "What causes water carry-over (drift) in agricultural evaporative cooling systems?", "answer": "Face velocities exceeding 2.0 to 2.5 m/s exert aerodynamic drag forces that strip droplets from the pad face, blowing liquid mist into the greenhouse or barn."}
            ],
            "precautions": [
                "Verify uniform water flow along the distribution pipe header to prevent localized dry streaks on the pad.",
                "Ensure steady ambient inlet dry-bulb and wet-bulb temperatures throughout the test duration.",
                "Shield psychrometer wick temperature sensors from radiant heat and ensure pure distilled water supply to wicks.",
                "Zero and tare the electronic sump balance before each 15-minute gravimetric test interval."
            ],
            "limitations": [
                "The linear evaporation model is valid for the design operational velocity range of 0.5 to 2.0 m/s.",
                "Assumes constant ambient entering air enthalpy and moisture content during the testing sequence.",
                "Does not account for calcium scale deposition effects present in long-term field operation.",
                "Applies to clean, un-degraded cellulose media without biological biofilm fouling."
            ],
            "quiz": [
                {
                    "question": "What is the theoretical minimum temperature achievable by an evaporative cooling pad?",
                    "options": ["Entering air dew point", "Entering air wet-bulb temperature", "Freezing point of water (0 °C)", "Mean radiant temperature"],
                    "correct": 1,
                    "explanation": "Adiabatic saturation cools air along a constant enthalpy line toward its entering thermodynamic wet-bulb temperature."
                },
                {
                    "question": "If entering dry-bulb is 36 °C, entering wet-bulb is 24 °C, and exit dry-bulb is 27 °C, what is the cooling efficiency?",
                    "options": ["50%", "65%", "75%", "90%"],
                    "correct": 2,
                    "explanation": "Efficiency η = (36 - 27) / (36 - 24) = 9 / 12 = 0.75 or 75%."
                },
                {
                    "question": "Why is bleed-off water discharge essential in agricultural evaporative cooling pads?",
                    "options": ["To lower air velocity", "To prevent mineral salt crystallization and pad scaling", "To warm the water supply", "To increase air pressure drop"],
                    "correct": 1,
                    "explanation": "As pure water evaporates, mineral concentrations rise; bleed-off removes salts to prevent scale buildup."
                },
                {
                    "question": "If measured evaporation rate is 17.0 g/(min·m²) at a face velocity of 2.0 m/s, what is the evaporation velocity gradient?",
                    "options": ["4.25 (g/min·m²)/(m/s)", "8.50 (g/min·m²)/(m/s)", "12.75 (g/min·m²)/(m/s)", "17.00 (g/min·m²)/(m/s)"],
                    "correct": 1,
                    "explanation": "k_w = 17.0 g/(min·m²) / 2.0 m/s = 8.50 (g/min·m²)/(m/s)."
                }
            ],
            "settings": ["Pad thickness: 100 mm cross-fluted cellulose (45°/15°)", "Inlet air: 35.0 °C DB / 22.0 °C WB", "Water temperature: 21.5 °C"],
            "samples": [0.5, 0.8, 1.1, 1.4, 1.7, 2.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💨", "label": "1. Cooling Pad Wind Tunnel"},
                {"id": "compare", "icon": "📊", "label": "2. Psychrometric Saturation"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Evaporative Pad Sandbox"}
            ]
        },
        {
            "number": 32,
            "slug": "fruit-vegetable-respiration-heat-rate-cold-storage",
            "title": "Fruit & Vegetable Respiration Heat Rate under Controlled Atmosphere",
            "shortTitle": "Produce Respiration Kinetics",
            "aim": "Measure the carbon dioxide evolution rate and respiration heat production of stored agricultural produce across storage temperatures using closed-system gas analysis.",
            "inputLabel": "Storage Temperature T",
            "shortInput": "Temp T",
            "inputUnit": "°C",
            "min": 2.0,
            "max": 22.0,
            "step": 4.0,
            "initial": 10.0,
            "inputDecimals": 1,
            "rawLabel": "CO2 Evolution Rate R_CO2",
            "rawUnit": "mg/(kg·h)",
            "rawDecimals": 3,
            "xAxis": "Temperature T (°C)",
            "yAxis": "CO2 evolution rate R_CO2 (mg/(kg·h))",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 12.0,
            "emptyY": 20.0,
            "targetName": "Thermal Respiration Sensitivity k_r",
            "target": "1.4500",
            "refValue": 1.4500,
            "resultUnit": "mg/(kg·h·°C)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "R_CO2 = k_r · T + R_0 = 1.4500 · T + 3.2000",
            "intro": "Fresh agricultural horticultural produce (fruits, vegetables, and ornamentals) remains metabolically active living tissue following post-harvest harvest. Cellular respiration consumes stored carbohydrates (primarily glucose) and oxygen while generating carbon dioxide, water vapor, and vital metabolic heat: C6H12O6 + 6 O2 → 6 CO2 + 6 H2O + 2870 kJ/mol. In cold storage design and refrigeration load calculations, respiration heat represents a dynamic, internal thermal load that must be continuously extracted by the evaporator coils to prevent temperature rise, quality degradation, and senescent breakdown. In accordance with Arrhenius and van 't Hoff biological temperature kinetics, respiration rate accelerates markedly with increasing pulp temperature, approximately doubling or tripling for each 10 °C temperature increase (Q10 coefficient). Within the commercial refrigerated storage window of 2 °C to 22 °C, the carbon dioxide evolution rate R_CO2 displays a predictable linear sensitivity k_r to storage temperature. In this laboratory experiment, a batch of fresh Gala apples is sealed inside a temperature-controlled hermetic respiration chamber equipped with non-dispersive infrared (NDIR) CO2 gas analyzers and oxygen sensors to measure respiration kinetics and determine refrigeration heat loads.",
            "modelExtra": "Evaluated on fresh Gala apples (moisture content 84.5% w.b.) in a sealed 50-liter acrylic respiration chamber under normoxic atmospheric conditions (21% O2 baseline). Linearized temperature sensitivity is evaluated between 2 °C and 22 °C.",
            "apparatus": [
                {"name": "Hermetic Acrylic Respiration Chamber", "purpose": "Provides an airtight 50-liter test enclosure with internal gas circulation fan and sampling ports."},
                {"name": "Refrigerated Environmental Test Chamber", "purpose": "Regulates ambient chamber temperature from 0 °C to 25 °C within ±0.1 °C stability."},
                {"name": "Non-Dispersive Infrared (NDIR) CO2 Analyzer", "purpose": "Monitors carbon dioxide concentration rise with 1 ppm resolution over discrete sampling intervals."},
                {"name": "Galvanic Fuel-Cell Oxygen Sensor", "purpose": "Measures oxygen depletion rate to compute the respiratory quotient (RQ = CO2 produced / O2 consumed)."},
                {"name": "Pulp Core Thermistor Probes", "purpose": "Monitors internal flesh temperature of representative fruit specimens to verify core thermal equilibrium."},
                {"name": "Precision Platform Balance", "purpose": "Measures total fresh produce test mass to normalize gas evolution rates to milligrams per kilogram-hour."}
            ],
            "procedure": [
                {"title": "Produce Sample Preparation", "text": "Weigh exactly 10.00 kg of uniform, blemish-free Gala apples and insert core thermistors into two representative reference fruits."},
                {"title": "Chamber Temperature Equilibration", "text": "Place the produce in the environmental chamber at 2.0 °C for 6 hours until fruit pulp core reaches within 0.2 °C of setpoint."},
                {"title": "Hermetic Sealing and Baseline Purge", "text": "Seal the respiration chamber lid and flush briefly with fresh air to establish standard 400 ppm baseline atmospheric CO2."},
                {"title": "Gas Evolution Rate Measurement", "text": "Isolate the chamber and record NDIR CO2 accumulation over a 60-minute incubation period, ensuring CO2 remains below 10,000 ppm."},
                {"title": "Temperature Progression Sequence", "text": "Repeat thermal equilibration and 60-minute CO2 accumulation trials at 6.0, 10.0, 14.0, 18.0, and 22.0 °C."},
                {"title": "Rate Calculation and Kinetic Regression", "text": "Calculate R_CO2 in mg/(kg·h) and plot against temperature T, fitting a linear regression to determine thermal respiration sensitivity k_r."}
            ],
            "topics": [
                {"question": "How is respiration heat related quantitatively to carbon dioxide evolution?", "answer": "Based on complete glucose oxidation, production of 1 mg of CO2 releases approximately 10.7 Joules of metabolic heat. Therefore, multiplying R_CO2 (mg/(kg·h)) by 10.7 / 3600 converts respiration directly into specific thermal power in W/kg."},
                {"question": "What is the respiratory quotient (RQ) and what does its value indicate?", "answer": "The respiratory quotient is the molar ratio of CO2 produced to O2 consumed (RQ = mol CO2 / mol O2). An RQ of 1.0 indicates pure carbohydrate oxidation; RQ < 1.0 indicates lipid/protein oxidation, while RQ > 1.3 signifies onset of anaerobic fermentation."},
                {"question": "What is the temperature coefficient Q10 in post-harvest biology?", "answer": "Q10 is the factor by which respiration rate increases when temperature is raised by 10 °C: Q10 = (R2 / R1)^(10 / (T2 - T1)). For most agricultural crops, Q10 ranges between 2.0 and 3.0 in the 0 °C to 20 °C range."},
                {"question": "How does controlled atmosphere (CA) storage retard produce respiration?", "answer": "CA storage lowers oxygen concentration (typically to 1% to 3%) and elevates CO2 (to 1% to 5%), slowing down respiratory enzyme kinetics, suppressing ethylene biosynthesis, and extending post-harvest storage life."},
                {"question": "What is the climacteric rise in fruit ripening?", "answer": "Climacteric fruits (e.g., apples, bananas, tomatoes) exhibit a dramatic surge in respiration rate and ethylene production at the onset of ripening, whereas non-climacteric fruits (e.g., citrus, grapes) show a steady, gradual decline."},
                {"question": "Why must CO2 concentrations not exceed critical thresholds during respiration tests?", "answer": "Excessive CO2 buildup (above 1% to 2%) can induce physiological injury, alter natural enzyme activity, and trigger anaerobic fermentation, distorting true aerobic respiration measurements."}
            ],
            "precautions": [
                "Ensure produce pulp core temperature reaches true thermal equilibrium before initiating gas collection.",
                "Verify airtight seal integrity with pressure decay test prior to each gas accumulation run.",
                "Limit measurement duration so that O2 depletion remains under 1.5% and CO2 buildup does not exceed 1.0%.",
                "Calibrate the NDIR CO2 analyzer with certified zero and span gases before testing."
            ],
            "limitations": [
                "The linear kinetic model applies within the commercial refrigerated storage range of 2 °C to 22 °C.",
                "Assumes pre-climacteric or steady ripening state without sudden ethylene-triggered respiratory spikes.",
                "Neglects potential latent heat of transpiration occurring simultaneously inside the chamber.",
                "Specific to Gala apple cultivars; other commodities exhibit distinct basal respiration magnitudes."
            ],
            "quiz": [
                {
                    "question": "What biochemical process is primarily responsible for internal metabolic heat generation in stored fruit?",
                    "options": ["Photosynthesis", "Aerobic cellular respiration", "Lactic acid fermentation", "Lipid saponification"],
                    "correct": 1,
                    "explanation": "Aerobic respiration oxidizes stored sugars into CO2, H2O, and metabolic heat."
                },
                {
                    "question": "For complete aerobic oxidation of glucose, what is the theoretical Respiratory Quotient (RQ)?",
                    "options": ["0.5", "0.7", "1.0", "1.4"],
                    "correct": 2,
                    "explanation": "Oxidation of glucose (C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O) consumes 6 moles of O2 per 6 moles of CO2, giving RQ = 6/6 = 1.0."
                },
                {
                    "question": "If measured CO2 evolution is 17.7 mg/(kg·h) at 10.0 °C and follows R = 1.4500 · T + 3.2000, what is R at 20.0 °C?",
                    "options": ["20.9 mg/(kg·h)", "26.3 mg/(kg·h)", "32.2 mg/(kg·h)", "41.5 mg/(kg·h)"],
                    "correct": 2,
                    "explanation": "R = 1.4500 · 20.0 + 3.2000 = 29.0 + 3.2 = 32.2 mg/(kg·h)."
                },
                {
                    "question": "Approximately how much metabolic heat is released per milligram of CO2 produced in respiration?",
                    "options": ["1.07 J", "10.7 J", "107 J", "1070 J"],
                    "correct": 1,
                    "explanation": "The stoichiometric heat of combustion of glucose releases approximately 10.7 Joules per milligram of evolved CO2."
                }
            ],
            "settings": ["Commodity: Gala apples (freshly harvested)", "Chamber volume: 50.0 L hermetic acrylic", "Baseline gas: Standard air (21% O2, 400 ppm CO2)"],
            "samples": [2.0, 6.0, 10.0, 14.0, 18.0, 22.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🍎", "label": "1. Respiration Chamber"},
                {"id": "compare", "icon": "📊", "label": "2. Arrhenius Kinetics"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Cold Storage Heat Sandbox"}
            ]
        },
        {
            "number": 33,
            "slug": "livestock-housing-sensible-heat-balance-ventilation",
            "title": "Livestock Housing Sensible Heat Balance & Minimum Ventilation",
            "shortTitle": "Livestock Heat Balance",
            "aim": "Quantify sensible heat production and determine minimum winter ventilation airflow in a confinement livestock housing facility across varying animal biomass loads.",
            "inputLabel": "Total Animal Biomass M_a",
            "shortInput": "Biomass M_a",
            "inputUnit": "kg",
            "min": 2000,
            "max": 12000,
            "step": 2000,
            "initial": 6000,
            "inputDecimals": 0,
            "rawLabel": "Sensible Heat Output Q_s",
            "rawUnit": "kW",
            "rawDecimals": 3,
            "xAxis": "Animal biomass M_a (kg)",
            "yAxis": "Sensible heat output Q_s (kW)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 7000,
            "emptyY": 8.5,
            "targetName": "Specific Sensible Heat Coefficient q_a",
            "target": "0.0012",
            "refValue": 0.0012,
            "resultUnit": "kW/kg",
            "resultDecimals": 6,
            "resultScale": 1000.0,
            "fitEquation": "Q_s = q_a · M_a = 0.0012 · M_a",
            "intro": "In agricultural structures and bio-environmental engineering, designing intensive livestock and poultry housing requires strict thermal and psychrometric balance calculations. Animals dissipate metabolic energy into their housing environment in two distinct components: sensible heat (convection and radiation to surrounding air and building surfaces) and latent heat (moisture evaporation via skin perspiration and respiratory tract vapor). During cold weather conditions, sensible heat produced by the animals serves as the primary thermal source maintaining barn temperature above critical design thresholds. However, minimum mechanical ventilation must be continuously operated to remove animal respiratory moisture, carbon dioxide, ammonia, and pathogens without chilling the building. Under ASABE Standard EP270 and CIGR environmental guidelines, sensible heat generation Q_s scales directly with total active biomass M_a housed within the facility. In this laboratory investigation, an instrumented swine nursery housing module is evaluated across controlled stocking biomass increments to quantify total sensible heat production, verify thermal energy conservation, and size minimum winter ventilation capacity.",
            "modelExtra": "Evaluated in a controlled swine nursery room at standard thermoneutral indoor temperature (22.0 °C) with growing feeder pigs. Sensible heat output reflects steady-state thermal power generation after accounting for structural building envelope transmission losses.",
            "apparatus": [
                {"name": "Controlled Swine Housing Test Module", "purpose": "Provides an insulated environmental room (8.0 m × 12.0 m) with fully slatted flooring and variable stocking pens."},
                {"name": "Variable-Frequency Exhaust Ventilation Fan", "purpose": "Delivers calibrated continuous airflow rates from 200 to 3000 m³/h with airflow nozzle meter."},
                {"name": "Multi-Point Aspirated Thermocouple Grid", "purpose": "Measures intake, spatial room, and exhaust air dry-bulb temperatures with 0.1 °C precision."},
                {"name": "High-Precision Calibrated Dew-Point Hygrometer", "purpose": "Determines indoor and exhaust moisture humidity ratio to isolate sensible from latent heat flux."},
                {"name": "Livestock Platform Scale", "purpose": "Weighs individual and group animal batches to establish exact live biomass stocking totals."},
                {"name": "Building Envelope Heat Flux Meter Network", "purpose": "Monitors conductive heat transmission through walls, ceiling, and foundation to close energy balance."}
            ],
            "procedure": [
                {"title": "Stocking Biomass Standardization", "text": "Weigh and group nursery feeder pigs into uniform pens to establish the initial test biomass level of 2000 kg."},
                {"title": "Ventilation Rate Calibration", "text": "Set exhaust ventilation to a constant continuous airflow rate verified via calibrated intake orifice plate."},
                {"title": "Room Thermal Stabilization", "text": "Allow animals to acclimate for 4 hours until spatial room temperatures and floor temperatures achieve steady thermal balance."},
                {"title": "Enthalpy and Heat Balance Acquisition", "text": "Measure ventilation airflow rate, temperature rise (T_exhaust - T_inlet), and wall transmission losses over a 2-hour monitoring window."},
                {"title": "Biomass Incrementation Progression", "text": "Systematically increase pen stocking biomass to 4000, 6000, 8000, 10000, and 12000 kg, repeating thermal balance measurements."},
                {"title": "Sensible Heat Coefficient Derivation", "text": "Calculate sensible heat output Q_s = V_dot · ρ · C_p · (T_exhaust - T_inlet) + Q_structural and plot Q_s versus biomass M_a to determine q_a."}
            ],
            "topics": [
                {"question": "How is animal total heat production partitioned between sensible and latent heat?", "answer": "Total metabolic heat equals sensible heat (radiation and convection) plus latent heat (moisture evaporation). At low ambient temperatures, sensible heat dominates (up to 75% to 80% of total); as ambient temperature approaches body core temperature, sensible heat drops toward zero and latent heat becomes the primary heat loss mechanism."},
                {"question": "What is the primary governing criterion for minimum winter ventilation in livestock barns?", "answer": "In winter, minimum ventilation is governed by moisture removal (preventing condensation and high humidity that promotes respiratory disease) while ensuring CO2 remains below 3000 ppm and ammonia below 15-20 ppm."},
                {"question": "What is the thermoneutral zone in animal bioenergetics?", "answer": "The thermoneutral zone is the ambient temperature range within which an animal can maintain normal core body temperature without expending additional metabolic energy on shivering or active evaporative cooling."},
                {"question": "Why does specific heat production per kilogram decrease as individual animals grow larger?", "answer": "Based on Kleiber's law (metabolic rate ∝ M^0.75), smaller animals have a higher surface-area-to-mass ratio and higher basal metabolic rate per unit body weight than mature animals."},
                {"question": "How does supplemental heating interact with animal sensible heat during winter?", "answer": "If animal sensible heat production is insufficient to offset building envelope transmission losses and minimum ventilation sensible heating loads, supplemental heaters must supply the deficit to prevent indoor temperature drops."},
                {"question": "What role does slatted flooring play in building sensible heat balance?", "answer": "Slatted floors allow rapid drainage of manure into underfloor pits, reducing wet surface area and limiting parasitic evaporative cooling that would otherwise convert sensible room heat into unwanted latent room humidity."}
            ],
            "precautions": [
                "Maintain uniform indoor air distribution to prevent draft chilling on animals while avoiding stagnant dead zones.",
                "Verify accurate calibration of ventilation airflow measurement stations to prevent large mass flow errors.",
                "Ensure steady animal activity levels during data collection windows (avoid measuring during feeding frenzies).",
                "Account rigorously for building envelope transmission heat losses using calibrated wall heat flux sensors."
            ],
            "limitations": [
                "The linear sensible heat scaling applies within the thermoneutral zone (indoor temperature 20 °C to 24 °C).",
                "Assumes calm animal behavior without extreme physical exertion or stress-induced metabolic elevation.",
                "Valid for growing swine; ruminants and poultry exhibit different specific sensible heat generation constants.",
                "Neglects minor heat contributions from indoor electrical lighting and feed motor equipment."
            ],
            "quiz": [
                {
                    "question": "What is the primary heat dissipation mechanism for livestock at low ambient temperatures?",
                    "options": ["Sensible convection and radiation", "Respiratory panting", "Skin sweating", "Latent vaporization"],
                    "correct": 0,
                    "explanation": "In cold conditions, sensible heat (convection and longwave radiation) accounts for the vast majority (70-80%) of metabolic heat release."
                },
                {
                    "question": "What is the primary objective of minimum winter ventilation in an insulated swine barn?",
                    "options": ["Cooling the building", "Removing animal moisture and noxious gases without chilling", "Creating high air speed drafts", "Increasing indoor relative humidity"],
                    "correct": 1,
                    "explanation": "Minimum ventilation removes respired moisture and gases (CO2, NH3) while conserving sensible heat."
                },
                {
                    "question": "If 6000 kg of feeder pigs generate 7.20 kW of sensible heat, what is the specific sensible heat coefficient?",
                    "options": ["0.0006 kW/kg", "0.0012 kW/kg", "0.0024 kW/kg", "0.0048 kW/kg"],
                    "correct": 1,
                    "explanation": "q_a = 7.20 kW / 6000 kg = 0.0012 kW/kg (or 1.20 W/kg)."
                },
                {
                    "question": "As ambient room temperature rises toward an animal's body temperature, sensible heat output:",
                    "options": ["Increases linearly", "Decreases toward zero while latent heat increases", "Remains strictly constant", "Doubles every 5 °C"],
                    "correct": 1,
                    "explanation": "As the temperature difference between animal skin and ambient air shrinks, sensible heat transfer drops to zero, requiring evaporative cooling."
                }
            ],
            "settings": ["Livestock species: Growing nursery pigs (25-45 kg)", "Indoor temperature: 22.0 °C thermoneutral", "Ventilation control: Negative pressure continuous exhaust"],
            "samples": [2000, 4000, 6000, 8000, 10000, 12000],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🐖", "label": "1. Livestock Housing Module"},
                {"id": "compare", "icon": "📊", "label": "2. Thermal Balance Curves"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Ventilation Sizing Sandbox"}
            ]
        },
        {
            "number": 34,
            "slug": "agricultural-timber-roof-truss-load-deflection",
            "title": "Agricultural Timber Roof Truss Load-Deflection Mechanics",
            "shortTitle": "Timber Truss Deflection",
            "aim": "Investigate vertical ridge and mid-span flexural deflections of a full-scale timber Fink roof truss under symmetrical distributed vertical roof loading.",
            "inputLabel": "Total Applied Load W",
            "shortInput": "Load W",
            "inputUnit": "kN",
            "min": 2.0,
            "max": 12.0,
            "step": 2.0,
            "initial": 6.0,
            "inputDecimals": 1,
            "rawLabel": "Ridge Joint Deflection δ",
            "rawUnit": "mm",
            "rawDecimals": 3,
            "xAxis": "Total applied load W (kN)",
            "yAxis": "Ridge deflection δ (mm)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 7.0,
            "emptyY": 12.5,
            "targetName": "Truss Flexural Compliance C_f",
            "target": "1.8500",
            "refValue": 1.8500,
            "resultUnit": "mm/kN",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "δ = C_f · W = 1.8500 · W",
            "intro": "Agricultural post-frame buildings, grain flat storage sheds, and livestock shelters require economical, wide-span roof structural framing capable of resisting heavy design dead, snow, and wind loads. Light-frame timber roof trusses (commonly configured as Fink 'W', Howe, or Pratt planar frameworks) assembled with punched metal-plate tooth connectors provide high strength-to-weight ratios and structural stiffness. Structural safety and serviceability design (under ASABE EP486 and National Design Specification for Wood Construction) require that elastic vertical deflections under service snow and gravity loads remain well below serviceability thresholds (typically span/240 to span/360) to prevent roof ponding, ceiling finish cracking, and purlin displacement. In linear structural mechanics, overall elastic deflection δ at the apex ridge joint is directly proportional to applied total gravity load W through the structural flexural compliance coefficient C_f = δ / W (the inverse of truss stiffness). Compliance integrates axial elasticity of chords and webs, joint rotational semi-rigidity, and metal tooth connector tooth slip. In this experiment, a full-scale 9.0-meter span agricultural timber Fink truss mounted in a heavy reaction loading frame is subjected to hydraulic cylinder gravity loads to quantify load-deflection linearity and serviceability deflection limits.",
            "modelExtra": "Evaluated on a 9.0-meter span, 4:12 pitch timber Fink roof truss fabricated with No. 2 Southern Pine lumber and 20-gauge punched metal connector plates. Symmetrical vertical loads are applied through multi-point hydraulic whiffletree loading linkages.",
            "apparatus": [
                {"name": "Heavy Structural Reaction Frame", "purpose": "Provides rigid steel reaction columns and cross-beams capable of withstanding 50 kN structural reactions."},
                {"name": "Agricultural Timber Fink Truss", "purpose": "Full-scale 9.0-meter span test truss (4:12 pitch, Southern Pine chords, toothed metal plate joints)."},
                {"name": "Hydraulic Cylinder Whiffletree Loading Linkage", "purpose": "Applies symmetrical vertical point loads to purlin node joints simulating uniform roof snow loading."},
                {"name": "Calibrated Precision Load Cell", "purpose": "Measures total vertical hydraulic force applied to the truss system with 0.05 kN resolution."},
                {"name": "Linear Variable Differential Transformers (LVDTs)", "purpose": "Monitors vertical deflections at ridge apex, lower chord mid-span, and quarter points to 0.01 mm accuracy."},
                {"name": "Lateral Bracing Restraint System", "purpose": "Prevents out-of-plane lateral-torsional buckling of the top compression chord during gravity loading."}
            ],
            "procedure": [
                {"title": "Truss Alignment and Lateral Bracing Setup", "text": "Position the test truss onto pin and roller support fixtures, verifying span alignment and securing low-friction lateral guide rollers."},
                {"title": "Displacement Sensor Positioning and Taring", "text": "Mount digital LVDT sensors beneath the apex ridge joint, mid-span bottom chord, and node joints, zeroing all telemetry channels."},
                {"title": "Initial Preload Seating", "text": "Apply a seating preload of 1.0 kN to engage whiffletree linkages and bedding of metal plate teeth, then release back to zero."},
                {"title": "Incremental Symmetrical Loading", "text": "Apply vertical gravity loads in 2.0 kN increments from 2.0 kN up to 12.0 kN using the hydraulic servo-valve controller."},
                {"title": "Steady-State Deflection Acquisition", "text": "Hold load constant for 3 minutes at each increment to record stabilized vertical deflections and verify absence of joint slippage."},
                {"title": "Compliance Regression Analysis", "text": "Plot apex ridge deflection δ against total applied load W, computing the structural flexural compliance C_f via linear regression."}
            ],
            "topics": [
                {"question": "What is the structural role of punched metal connector plates in modern timber trusses?", "answer": "Punched metal tooth plates transfer tension, compression, and shear stresses between adjacent wood members without requiring bulky bolted lap splices, providing high joint rigidity and automated manufacturing capability."},
                {"question": "How is structural serviceability deflection limited in agricultural roof truss design?", "answer": "Building codes generally limit total load deflection to L / 180 or L / 240, and live load (snow) deflection to L / 360 of the clear span L to prevent aesthetic sagging, roof leaks, and interference with interior equipment."},
                {"question": "Why is lateral bracing of the top chord essential in agricultural truss construction?", "answer": "Under downward gravity loads, the top chords are in heavy axial compression; without continuous lateral purlin bracing, they would buckle prematurely in lateral-torsional failure long before reaching wood crushing limits."},
                {"question": "What is a 'whiffletree' loading mechanism in structural testing?", "answer": "A whiffletree is a system of pivoting beams and linkages that distributes a single hydraulic actuator force into multiple equal or proportional concentrated loads across truss nodes to simulate uniform distributed loading."},
                {"question": "How does wood moisture content affect truss stiffness and long-term creep deflection?", "answer": "Higher wood moisture content reduces the modulus of elasticity (MOE) of timber. In service, repeated seasonal moisture cycling under sustained load causes creep deflection that can double initial elastic deflections over several years."},
                {"question": "What is the primary difference between a Fink truss and a Howe truss?", "answer": "In a Fink ('W') truss, web members are arranged in a 'W' pattern such that the longest web members act in tension under gravity load, whereas in a Howe truss, vertical web members are in tension and diagonals are in compression."}
            ],
            "precautions": [
                "Install rigid lateral guide braces to prevent out-of-plane truss buckling while ensuring zero vertical friction.",
                "Verify that load application pads are aligned exactly over panel nodes to avoid inducing parasitic local bending moments.",
                "Ensure hydraulic loading rate does not exceed 1.0 kN/min to prevent dynamic inertia shock.",
                "Verify solid seating of end reaction bearings to prevent rigid-body settlement errors in deflection readings."
            ],
            "limitations": [
                "The linear compliance model applies strictly within the elastic working range (W ≤ 12.0 kN) prior to wood yielding.",
                "Does not model long-term rheological creep deflection caused by sustained multi-year snow loads.",
                "Assumes symmetrical loading; asymmetric wind or drifted snow loads induce unsymmetrical web force reversals.",
                "Specific to the tested 9.0-meter span Fink geometry with No. 2 Southern Pine lumber."
            ],
            "quiz": [
                {
                    "question": "In a typical agricultural Fink roof truss under gravity downward loading, the top chord members are in:",
                    "options": ["Pure tension", "Axial compression and local bending", "Pure torsion", "Zero stress"],
                    "correct": 1,
                    "explanation": "Gravity loads create overall truss bending that puts the upper top chords into combined axial compression and purlin bending."
                },
                {
                    "question": "What is the standard serviceability deflection limit for agricultural roofs under live load?",
                    "options": ["Span / 50", "Span / 120", "Span / 360", "Span / 1000"],
                    "correct": 2,
                    "explanation": "Standard building codes and ASABE EP486 typically specify a live load deflection limit of Span / 360."
                },
                {
                    "question": "If measured ridge deflection is 11.1 mm under a total vertical load of 6.0 kN, what is the flexural compliance?",
                    "options": ["0.54 mm/kN", "1.85 mm/kN", "3.70 mm/kN", "6.00 mm/kN"],
                    "correct": 1,
                    "explanation": "Compliance C_f = δ / W = 11.1 mm / 6.0 kN = 1.85 mm/kN."
                },
                {
                    "question": "What failure mode is prevented by installing continuous purlins and diagonal bracing along top chords?",
                    "options": ["Foundation settlement", "Lateral-torsional compression buckling", "Tooth plate corrosion", "Tension chord rupture"],
                    "correct": 1,
                    "explanation": "Lateral bracing restrains the slender top compression chord from buckling sideways out of the truss plane."
                }
            ],
            "settings": ["Truss type: 9.0 m span Fink 'W' (4:12 pitch)", "Lumber grade: No. 2 Southern Pine (MOE = 9.6 GPa)", "Connectors: 20-gauge galvanized steel tooth plates"],
            "samples": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🏗️", "label": "1. Truss Load Frame"},
                {"id": "compare", "icon": "📊", "label": "2. Load-Deflection Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Structural Roof Sandbox"}
            ]
        },
        {
            "number": 35,
            "slug": "anaerobic-digester-biogas-yield-methane-kinetics",
            "title": "Anaerobic Digester Biogas Yield & Mesophilic Methane Kinetics",
            "shortTitle": "Anaerobic Biogas Production",
            "aim": "Measure specific biogas yield and methane generation kinetics from dairy manure slurry in a continuously stirred mesophilic anaerobic digester as a function of volatile solids loading.",
            "inputLabel": "Volatile Solids Loaded VS",
            "shortInput": "Solids VS",
            "inputUnit": "kg",
            "min": 1.0,
            "max": 6.0,
            "step": 1.0,
            "initial": 3.0,
            "inputDecimals": 1,
            "rawLabel": "Cumulative Biogas Production V_g",
            "rawUnit": "m³",
            "rawDecimals": 4,
            "xAxis": "Volatile solids VS (kg)",
            "yAxis": "Cumulative biogas V_g (m³)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.5,
            "emptyY": 1.5,
            "targetName": "Specific Biogas Yield Y_vs",
            "target": "0.4200",
            "refValue": 0.4200,
            "resultUnit": "m³/kg-VS",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "V_g = Y_vs · VS = 0.4200 · VS",
            "intro": "Agricultural anaerobic digestion represents a vital bioenergy and waste management technology that converts livestock manure, agricultural residues, and food waste into renewable biogas while mitigating greenhouse gas emissions and producing nutrient-rich digestate fertilizer. Anaerobic biodegradation of organic waste proceeds through four consecutive biochemical stages mediated by diverse syntrophic bacterial and archaeal consortia: hydrolysis of complex polymers into monomers, acidogenesis into volatile fatty acids (VFAs), acetogenesis into acetate and hydrogen, and methanogenesis into methane (CH4) and carbon dioxide (CO2). Sizing on-farm anaerobic digester vessels, combined heat and power (CHP) generation units, and gas storage flares requires accurate determination of the specific biogas yield Y_vs (expressed in normal cubic meters of biogas produced per kilogram of volatile solids loaded, m³/kg-VS). Under steady mesophilic digestion conditions (37.0 °C) with stable hydraulic retention times, cumulative biogas generation V_g scales in direct linear proportion to the volatile organic solids mass VS fed to the microbial reactor. In this laboratory investigation, an instrumented pilot-scale continuously stirred tank reactor (CSTR) digester fed with dairy cattle manure slurry is monitored to quantify biogas yield, methane concentration, and chemical oxygen demand (COD) conversion kinetics.",
            "modelExtra": "Evaluated in a 200-liter continuously stirred mesophilic anaerobic digester operating at 37.0 ± 0.5 °C with dairy manure slurry (total solids 8.5%, volatile solids fraction 82.0% of TS). Methane fraction averages 60.5% by volume with pH maintained at 7.2 to 7.4.",
            "apparatus": [
                {"name": "Mesophilic CSTR Anaerobic Digester", "purpose": "Provides a 200-liter stainless steel jacketed anaerobic vessel with variable-speed paddle mixer."},
                {"name": "Circulating Water Jacket Thermostat", "purpose": "Maintains constant slurry temperature at 37.0 °C with digital PID temperature controller."},
                {"name": "Wet-Tip Precision Gas Meter", "purpose": "Measures continuous cumulative biogas production with 100 mL volumetric tip resolution."},
                {"name": "Dual-Beam NDIR Biogas Composition Analyzer", "purpose": "Monitors continuous volumetric concentrations of CH4 (0-100%) and CO2 (0-100%) and H2S ppm."},
                {"name": "Industrial In-Line pH and ORP Probe", "purpose": "Tracks digester slurry pH and oxidation-reduction potential (-350 mV) to verify healthy methanogenic state."},
                {"name": "Analytical Muffle Furnace & Desiccator", "purpose": "Determines total solids (TS at 105 °C) and volatile solids (VS ash burn at 550 °C) of feed manure."}
            ],
            "procedure": [
                {"title": "Substrate Characterization and Inoculum Stabilization", "text": "Analyze dairy manure slurry total solids (TS) and volatile solids (VS); verify active digester inoculum with stable pH (7.3) and low VFA baseline."},
                {"title": "Incremental VS Feed Batching", "text": "Prepare standardized manure feed batches corresponding to volatile solids additions of 1.0, 2.0, 3.0, 4.0, 5.0, and 6.0 kg-VS."},
                {"title": "Anaerobic Feeding and Purge", "text": "Inject the initial feed batch into the digester through the sub-surface feed port without introducing atmospheric oxygen."},
                {"title": "Gas Production Monitoring", "text": "Record daily and cumulative biogas volume produced over the active degradation cycle using the wet-tip volumetric flow meter."},
                {"title": "Gas Composition and Quality Analysis", "text": "Sample biogas composition daily using the NDIR analyzer to verify steady methane concentration (58% to 62% CH4)."},
                {"title": "Yield Calculation and Kinetic Plotting", "text": "Normalize gas volume to standard temperature and pressure (STP: 0 °C, 1 atm) and plot V_g against loaded VS to extract specific yield Y_vs."}
            ],
            "topics": [
                {"question": "What are the four sequential biochemical stages of anaerobic digestion?", "answer": "The four stages are: (1) Hydrolysis (complex polymers broken into soluble monomers), (2) Acidogenesis (monomers converted to volatile fatty acids and alcohols), (3) Acetogenesis (VFAs converted to acetic acid, CO2, and H2), and (4) Methanogenesis (methanogenic archaea convert acetate and H2/CO2 into CH4 and CO2)."},
                {"question": "What is the typical composition of agricultural biogas produced from dairy manure?", "answer": "Biogas typically consists of 55% to 65% methane (CH4), 35% to 45% carbon dioxide (CO2), with trace amounts of water vapor, nitrogen, hydrogen, and 500 to 3000 ppm hydrogen sulfide (H2S)."},
                {"question": "Why is methanogenesis the most sensitive stage in the anaerobic digestion process?", "answer": "Methanogenic archaea have slow growth rates and are strictly obligate anaerobes with narrow pH tolerance (6.8 to 7.6); excessive organic loading can cause acid accumulation ('sour digester') which halts methanogenesis."},
                {"question": "What is the difference between total solids (TS) and volatile solids (VS)?", "answer": "Total solids (TS) is the dry matter remaining after heating at 105 °C. Volatile solids (VS) is the portion of TS that combusts when heated to 550 °C in a muffle furnace, representing the biodegradable organic fraction."},
                {"question": "What are the optimal operating temperature ranges for mesophilic versus thermophilic digestion?", "answer": "Mesophilic digestion operates optimally between 35 °C and 38 °C (typically 37 °C), while thermophilic digestion operates between 50 °C and 55 °C, offering faster reaction rates but requiring higher heating energy and greater operational stability."},
                {"question": "Why must hydrogen sulfide (H2S) be scrubbed from biogas prior to engine combustion?", "answer": "When burned in an engine, H2S forms sulfur dioxide and sulfuric acid (H2SO4), causing severe corrosive degradation of engine cylinder liners, exhaust valves, and heat exchangers."}
            ],
            "precautions": [
                "Ensure strict exclusion of atmospheric oxygen; methanogenic archaea are obligate anaerobes damaged by air.",
                "Monitor digester pH daily; add sodium bicarbonate buffer immediately if pH drops below 6.8.",
                "Maintain constant digester mixing to prevent thermal stratification and crust formation at the slurry surface.",
                "Verify biogas gas-tightness using bubble leak tests; biogas contains explosive methane and toxic H2S."
            ],
            "limitations": [
                "The linear yield model applies under stable organic loading without substrate shock or VFA souring.",
                "Assumes consistent dairy manure diet and manure composition across all test batches.",
                "Applies to mesophilic CSTR operation; plug-flow and covered lagoon digesters exhibit different kinetics.",
                "Neglects minor gas production lag during the initial 12-hour acclimation period following feeding."
            ],
            "quiz": [
                {
                    "question": "Which group of microorganisms carries out the final step producing methane in anaerobic digesters?",
                    "options": ["Lactic acid bacteria", "Cellulolytic fungi", "Methanogenic archaea", "Nitrifying bacteria"],
                    "correct": 2,
                    "explanation": "Methanogenic archaea (such as Methanosaeta and Methanosarcina) convert acetate, H2, and CO2 into methane."
                },
                {
                    "question": "What is the typical volumetric methane concentration in raw agricultural biogas from cattle manure?",
                    "options": ["10% to 20%", "30% to 40%", "55% to 65%", "90% to 99%"],
                    "correct": 2,
                    "explanation": "Biogas from dairy and cattle manure typically contains 55% to 65% methane, with the remainder mostly CO2."
                },
                {
                    "question": "If 5.0 kg of volatile solids generates 2.10 m³ of biogas at STP, what is the specific biogas yield?",
                    "options": ["0.21 m³/kg-VS", "0.42 m³/kg-VS", "0.84 m³/kg-VS", "1.05 m³/kg-VS"],
                    "correct": 1,
                    "explanation": "Specific biogas yield Y_vs = 2.10 m³ / 5.0 kg-VS = 0.42 m³/kg-VS."
                },
                {
                    "question": "What temperature range defines mesophilic anaerobic digestion?",
                    "options": ["10 °C to 20 °C", "35 °C to 38 °C", "50 °C to 55 °C", "70 °C to 80 °C"],
                    "correct": 1,
                    "explanation": "Mesophilic digestion operates in the biological range of 35 °C to 38 °C, typically maintained at 37 °C."
                }
            ],
            "settings": ["Digester type: 200 L jacketed CSTR mesophilic", "Operating temperature: 37.0 ± 0.5 °C", "Substrate: Dairy cattle manure (TS 8.5%, VS 82% of TS)"],
            "samples": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🧪", "label": "1. Biogas Digester CSTR"},
                {"id": "compare", "icon": "📊", "label": "2. Biogas Yield vs VS"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Methane Production Sandbox"}
            ]
        }
    ]
