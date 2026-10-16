import json, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

exp27 = {
    'number': 27,
    'slug': 'latent-heat-vaporization',
    'title': 'Determination of the Latent Heat of Vaporization of Water by Condensation Calorimetry',
    'shortTitle': 'Latent Heat of Vaporization',
    'aim': 'Determine the specific latent heat of vaporization of water (L_v) by condensing dry steam into a known mass of cold water inside a calibrated copper calorimeter, measuring the resulting temperature elevation, and analyzing the thermal energy balance with radiation exchange corrections.',
    'target': 'L_v',
    'targetName': 'Latent heat of vaporization L_v',
    'inputLabel': 'Mass of condensed steam m_v',
    'shortInput': 'Steam mass m_v',
    'inputUnit': 'g',
    'inputDecimals': 1,
    'rawLabel': 'Equilibrium temperature T_f',
    'rawUnit': '°C',
    'rawDecimals': 2,
    'xAxis': 'Mass of condensed steam m_v (kg)',
    'yAxis': 'Net latent heat liberated Q_net (J)',
    'xScale': 1000.0,
    'yScale': 0.001,
    'gradientUnit': 'J kg⁻¹',
    'resultUnit': 'kJ kg⁻¹',
    'resultScale': 0.001,
    'resultDecimals': 2,
    'min': 2.0,
    'max': 12.0,
    'step': 0.5,
    'initial': 6.0,
    'samples': [3.0, 4.5, 6.0, 7.5, 9.0],
    'emptyX': [0.0, 0.015],
    'emptyY': [0.0, 25000.0],
    'timed': False,
    'angle': False,
    'published': True,
    'measureLabel': 'Measure final equilibrium temperature T_f for condensed steam mass m_v',
    'fitEquation': 'Q_net = C_sys (T_f − T_0) − m_v c_w (T_s − T_f) = m_v L_v ⇔ Y = L_v · X ⇔ L_v = S',
    'intro': "Vaporization represents one of the most energetic first-order phase transformations in classical thermodynamics. When liquid water at its boiling point transforms into saturated water vapor, an immense quantity of thermal energy—the specific latent heat of vaporization L_v—must be supplied to overcome the robust intermolecular hydrogen-bonding network and to perform mechanical expansion work against the surrounding atmospheric pressure as the specific volume increases by a factor of over 1,600. Conversely, when dry saturated steam condenses inside a cooler aqueous medium, it releases this identical quantity of latent enthalpy alongside the sensible heat of the condensed liquid as it cools from the boiling temperature T_s to the final mixture temperature T_f. In quantitative condensation calorimetry, dry steam generated in a dedicated boiler is conducted through a glass water trap designed to intercept entrained liquid droplets, ensuring that only pure gaseous phase enters the calorimeter. The thermal energy absorbed by the cold water bath, the thin-walled copper calorimeter vessel, and its stirrer equals the total heat liberated by the condensing steam: C_sys (T_f − T_0) = m_v L_v + m_v c_w (T_s − T_f). Rearranging this fundamental conservation equation isolates the net latent heat transfer: Q_net = C_sys (T_f − T_0) − m_v c_w (T_s − T_f) = m_v L_v. By executing condensation trials across varying charges of condensed steam, ordinary least-squares regression of Q_net against m_v yields a highly accurate evaluation of L_v, while the implementation of Count Rumford's radiation compensation technique—initiating trials as far below ambient room temperature as the final mixture rises above it—effectively eliminates net environmental radiation bias.",
    'settings': [
        'Steam boiler temperature T_s = 100.00 °C (under standard barometric pressure of 760 mmHg).',
        'Initial cold water mass m_w = 200.00 g; initial chilled temperature T_0 = 15.00 °C (compensating for room temperature at 20.0 °C).',
        'Specularly polished copper calorimeter (mass 75.00 g, c_cu = 385.0 J kg⁻¹ K⁻¹); water equivalent W_cal = 28.88 J K⁻¹; C_sys = 866.08 J K⁻¹.',
        'Reference latent heat of vaporization of water: L_v = 2260.00 kJ kg⁻¹ (2,260,000 J kg⁻¹ = 539.8 cal g⁻¹).'
    ],
    'apparatus': [
        {
            'name': 'Copper Steam Generator Boiler with Safety Manometer and Burner',
            'purpose': 'A robust cylindrical copper boiler equipped with a water-level sight glass, a vertical safety pressure-release manometer tube, and an adjustable Bunsen burner to produce a steady, vigorous stream of saturated steam at 100.0 °C.'
        },
        {
            'name': 'Glass Condensate Water Trap (Steam Dryer)',
            'purpose': 'An inline bulbous glass trap inserted between the boiler and delivery tube to catch, collect, and drain entrained liquid water droplets, guaranteeing that only dry saturated vapor reaches the calorimeter vessel.'
        },
        {
            'name': 'Polished Copper Calorimeter in Water-Jacketed Enclosure with Insulated Lid',
            'purpose': 'A thin-walled cylindrical copper container (mass 75.0 g) supported on insulating cork pegs inside a concentric air jacket, sealed with a vulcanite lid with apertures for the steam delivery tube, thermometer, and stirrer.'
        },
        {
            'name': 'Precision Calorimetric Thermometer and Analytical Balance',
            'purpose': 'A high-resolution mercury-in-glass thermometer graduated from 10 °C to 50 °C in 0.05 °C divisions to measure T_0 and T_f, paired with a dual-pan analytical balance resolving mass to ±0.01 g to determine the condensed steam mass m_v.'
        }
    ],
    'procedure': [
        {
            'title': 'Calorimeter Tare, Water Measurement, and Pre-Cooling',
            'text': 'Weigh the clean, dry copper calorimeter vessel together with its brass wire loop stirrer to ±0.01 g. Add exactly 200.00 g of distilled water pre-cooled to approximately 14 °C to 15 °C (approximately 5 °C below room temperature, T_room = 20.0 °C). Place the calorimeter vessel inside the double-walled outer jacket and seat the insulated lid firmly.',
            'why': 'Pre-cooling the initial water below room temperature implements Rumford\'s radiation compensation principle: heat gained from the room during the cool half of the experiment balances heat radiated to the room during the warm half.'
        },
        {
            'title': 'Boiler Activation, Steam Trap Pre-Heating, and Flow Stabilization',
            'text': 'Fill the copper boiler two-thirds full with distilled water, add anti-bumping boiling chips, and heat vigorously with the Bunsen burner. Connect the delivery tube through the glass water trap. Allow steam to blast freely through the trap into a waste beaker for at least three minutes until the trap and delivery nozzle are thoroughly pre-heated and discharging clean, dry steam without sputtering.',
            'why': 'Pre-heating the glass walls prevents steam from condensing prematurely in cold tubing before reaching the calorimeter, which would otherwise introduce liquid water droplets and severely distort the latent heat calculation.'
        },
        {
            'title': 'Initial Temperature Acquisition and Steam Injection',
            'text': 'Agitate the calorimeter water bath gently with the wire stirrer and record the steady initial temperature T_0 = 15.00 °C. Position the calorimeter beneath the pre-heated steam delivery nozzle, lower the nozzle tip approximately 2 cm below the water surface, and allow steam to bubble into the liquid while maintaining continuous, gentle stirring.',
            'why': 'Submerging the nozzle tip ensures complete thermal capture and instantaneous condensation of the steam bubbles before vapor can escape into the atmosphere.'
        },
        {
            'title': 'Condensation Termination and Nozzle Withdrawal',
            'text': 'Monitor the rising temperature closely. When the water temperature approaches approximately 25 °C to 35 °C (so the final temperature excess above room temperature roughly mirrors the initial depression below room temperature), pinch the rubber delivery hose, remove the delivery nozzle promptly from the water, and shake any adhering droplets back into the calorimeter.',
            'why': 'Withdrawing the nozzle promptly prevents back-siphoning of calorimeter water into the cooling delivery tube as internal steam pressure collapses.'
        },
        {
            'title': 'Final Equilibrium Temperature and Condensed Mass Determination',
            'text': 'Continue stirring the water bath thoroughly until the thermometer reaches its maximum steady reading, recording this value as the final equilibrium temperature T_f. Remove the calorimeter vessel from its jacket and reweigh it to ±0.01 g. Subtract the initial tare mass to determine the exact mass of condensed steam m_v = m_final − m_initial.',
            'why': 'The condensed mass m_v is the central independent variable; gravimetric determination on a precision analytical balance provides high experimental accuracy.'
        },
        {
            'title': 'Net Latent Heat Computation and Regression Analysis',
            'text': 'Repeat the condensation procedure across five distinct steam charges (m_v = 3.0 g, 4.5 g, 6.0 g, 7.5 g, and 9.0 g). For each run, compute the sensible heat absorbed by the system Q_gain = C_sys (T_f − T_0) and subtract the sensible heat lost by the condensed water cooling from 100 °C to T_f: Q_sens = m_v c_w (T_s − T_f). Plot Q_net = Q_gain − Q_sens against m_v (kg) and extract the latent heat of vaporization L_v from the slope.',
            'why': 'Linear regression over multiple condensation runs isolates the latent heat of transformation from random weighing and reading fluctuations, validating the first-order thermodynamic energy balance.'
        }
    ],
    'topics': [
        {
            'title': 'Thermodynamics of Vaporization and Latent Enthalpy of Phase Change',
            'text': "Vaporization is the first-order thermodynamic phase transformation wherein liquid molecules overcome intermolecular cohesion to transition into the gaseous state. In liquid water, each molecule participates in an extensive, dynamic three-dimensional hydrogen-bonding network with an average binding energy of approximately 20 kJ mol⁻¹ per bond. Transforming one kilogram of liquid water into steam at 100 °C requires breaking the vast majority of these hydrogen bonds, which accounts for the extraordinarily high specific latent heat of vaporization of water (L_v ≈ 2.260 × 10⁶ J kg⁻¹ = 539.8 cal g⁻¹), one of the highest of all known molecular liquids. Thermodynamically, the latent heat of vaporization represents the change in specific enthalpy between the saturated vapor and saturated liquid states: L_v = Δh_vap = h_g − h_f. This enthalpy change comprises two distinct microscopic components: internal energy change Δu_vap (the work done against intermolecular attractive forces, often termed internal latent heat) and external expansion work P Δv_vap done against the surrounding atmospheric pressure as the specific volume expands from v_f = 0.00104 m³ kg⁻¹ to v_g = 1.673 m³ kg⁻¹. At 100 °C and 101.325 kPa, external work P (v_g − v_f) accounts for approximately 169.5 kJ kg⁻¹ (about 7.5% of L_v), while internal bond disruption accounts for the remaining 2,090.5 kJ kg⁻¹ (92.5%).",
            'formula': 'L_v = \\Delta h_{\\text{vap}} = \\Delta u_{\\text{vap}} + P(\\nu_g - \\nu_f) \\approx 2.260 \\times 10^6 \\text{ J kg}^{-1}',
            'question': 'What are the two physical components that constitute the latent heat of vaporization of water?',
            'answer': 'The latent heat of vaporization comprises: (1) internal latent heat, which is the energy required to overcome intermolecular hydrogen bonding attractions; and (2) external latent heat, which is the mechanical work performed against atmospheric pressure as the vapor expands to more than 1,600 times its liquid volume.'
        },
        {
            'title': 'The Clapeyron-Clausius Equation and Temperature Dependence of L_v',
            'text': "The thermodynamic relationship governing the coexistence of liquid and vapor phases along the saturation curve is expressed by the Clapeyron equation, formulated by Émile Clapeyron in 1834: dP/dT = L_v / [T (v_g − v_f)], where P is the saturation vapor pressure, T is the absolute temperature, and v_g, v_f are the specific volumes of vapor and liquid respectively. Neglecting the minuscule liquid volume v_f ≪ v_g and modeling the saturated vapor as an ideal gas (v_g = R_specific T / P), Rudolf Clausius simplified this into the celebrated Clausius-Clapeyron equation: d(ln P)/dT = L_v / (R_specific T²). Integrating under the assumption of constant L_v gives ln(P / P_0) = −(L_v / R_specific) (1/T − 1/T_0). Furthermore, according to Kirchhoff's thermochemical law, the latent heat of vaporization itself is not strictly invariant with temperature; its derivative along the saturation line is dL_v/dT = c_{p,\\text{vap}} − c_{p,\\text{liq}}. Because the specific heat of liquid water (c_w ≈ 4,186 J kg⁻¹ K⁻¹) is roughly double that of steam (c_p,steam ≈ 2,010 J kg⁻¹ K⁻¹), L_v decreases linearly with increasing temperature, declining from 2,501 kJ kg⁻¹ at 0 °C to 2,260 kJ kg⁻¹ at 100 °C, and vanishing entirely at the thermodynamic critical point (T_c = 373.95 °C, P_c = 22.06 MPa) where the meniscus between liquid and vapor disappears.",
            'formula': '\\frac{dP}{dT} = \\frac{L_v}{T(\\nu_g - \\nu_f)} \\approx \\frac{P L_v}{R_{\\text{spec}} T^2} \\quad \\text{and} \\quad \\frac{dL_v}{dT} = c_{p,\\text{vap}} - c_{p,\\text{liq}}',
            'question': 'Why does the latent heat of vaporization of water decrease as temperature rises, and what happens to it at the critical point?',
            'answer': 'As temperature rises, thermal expansion separates liquid molecules, weakening intermolecular bonds prior to boiling, while the density of saturated vapor increases. The difference in enthalpy between liquid and vapor diminishes according to Kirchhoff’s equation dLv/dT = cp,vap − cp,liq. At the critical point (374 °C), the liquid and vapor densities become identical and Lv drops to zero.'
        },
        {
            'title': 'Condensation Calorimetry: Heat Exchange Conservation Equations',
            'text': "The method of mixtures applied to condensation calorimetry establishes a rigorous thermal energy balance inside the calorimeter. When a mass m_v of dry saturated steam at temperature T_s condenses in a calorimeter containing mass m_w of water at initial temperature T_0, two distinct heat release stages occur: (1) Phase change: m_v kilograms of steam condense isothermally into liquid water at T_s, liberating latent enthalpy Q_latent = m_v L_v; (2) Sensible cooling: the resulting m_v kilograms of condensed water cool from T_s down to the final equilibrium temperature T_f, releasing sensible heat Q_sens = m_v c_w (T_s − T_f). Simultaneously, the heat absorbed by the calorimeter assembly comprises: (3) Water warming: the initial water of mass m_w warms from T_0 to T_f, absorbing m_w c_w (T_f − T_0); (4) Vessel warming: the copper calorimeter vessel and stirrer of total water equivalent W_cal warm from T_0 to T_f, absorbing W_cal (T_f − T_0). Under adiabatic conditions, heat lost equals heat gained: m_v L_v + m_v c_w (T_s − T_f) = (m_w c_w + W_cal) (T_f − T_0) = C_sys (T_f − T_0). Isolating the latent contribution defines the net heat metric: Q_net = C_sys (T_f − T_0) − m_v c_w (T_s − T_f) = m_v L_v.",
            'formula': 'm_v L_v + m_v c_w (T_s - T_f) = C_{\\text{sys}} (T_f - T_0) \\implies Q_{\\text{net}} = m_v L_v',
            'question': 'In condensation calorimetry, what two distinct quantities of heat are released by the incoming steam?',
            'answer': 'First, the latent heat of vaporization released isothermally during the phase change from steam to liquid at 100 °C (Q = mv Lv). Second, the sensible heat released as the condensed water cools from 100 °C to the final equilibrium temperature Tf (Q = mv cw (Ts − Tf)).'
        },
        {
            'title': 'The Function of the Condensate Water Trap and Wet Steam Errors',
            'text': "In experimental steam calorimetry, the single largest source of systematic positive error is wet steam—the carryover of entrained microscopic liquid water droplets suspended in the vapor stream. If steam emerges directly from the boiling water surface through a simple tube, turbulent boiling entrains a fine mist of liquid droplets at 100 °C. If these liquid droplets enter the calorimeter, they contribute to the final measured mass m_v upon weighing, but they release zero latent heat of vaporization (they only release sensible heat as they cool from 100 °C to T_f). Consequently, the calculated latent heat L_v = [Q_gain − m_v c_w (T_s − T_f)] / m_v is severely depressed below its true value. If an entrained moisture fraction x_m = m_liquid / m_total is present, the apparent latent heat is related to the true latent heat by L_v,apparent = (1 − x_m) L_v,true. Even a 3% liquid carryover produces an unacceptable ~68 kJ kg⁻¹ deficit. To eliminate this defect, a specialized glass water trap (or Berthelot steam separator) is inserted immediately ahead of the calorimeter. The trap abruptly expands the flow channel, compelling droplet impingement against glass baffles and draining condensate downward, while only dry, super-saturated vapor flows upward into the calorimeter delivery nozzle.",
            'formula': 'L_{v,\\text{apparent}} = (1 - x_m) L_{v,\\text{true}} \\quad \\text{where } x_m = \\frac{m_{\\text{droplets}}}{m_{\\text{total}}}',
            'question': 'How does entrained liquid water (wet steam) affect the experimental calculation of latent heat of vaporization?',
            'answer': 'Liquid water droplets contribute to the measured condensed mass mv upon weighing, but they release no latent heat of vaporization (only sensible heat). Consequently, the heat released per gram of condensate appears falsely low, causing the calculated latent heat Lv to be systematically underestimated.'
        },
        {
            'title': "Count Rumford's Radiation Compensation Technique",
            'text': "During the 5 to 10 minutes required to bubble several grams of steam into the calorimeter, heat exchange between the calorimeter vessel and the ambient laboratory environment introduces thermal drift. Sir Benjamin Thompson, Count Rumford, devised an ingenious experimental procedure to cancel this environmental heat exchange without requiring complex numerical cooling corrections. Rumford observed that if the initial water temperature T_0 is adjusted below the ambient room temperature T_room by exactly the same amount that the final equilibrium temperature T_f will rise above it (such that T_room − T_0 ≈ T_f − T_room), the rate of heat gained by the calorimeter from the room during the first half of the experiment will approximately equal the rate of heat lost by the calorimeter to the room during the second half. Because Newton's law of cooling dictates that heat transfer rate is proportional to temperature excess (dQ/dt ∝ T − T_room), the integral of environmental heat exchange over the symmetric thermal excursion evaluates close to zero: ∫ dQ_env dt ≈ 0. In our standardized configuration with room temperature at 20.0 °C and an initial chilled temperature T_0 = 15.00 °C (5 °C below ambient), steam is injected until T_f reaches 25 °C to 35 °C, maintaining the average temperature of the vessel very near ambient and minimizing radiation bias.",
            'formula': '(T_{\\text{room}} - T_0) \\approx (T_f - T_{\\text{room}}) \\implies \\int_0^{t_{\\text{final}}} \\frac{dQ_{\\text{env}}}{dt} dt \\approx 0',
            'question': "What is Rumford's method of radiation compensation, and how does it eliminate environmental heat exchange errors?",
            'answer': "Rumford's method starts the experiment with the calorimeter water chilled as many degrees below room temperature as it is expected to rise above room temperature by the end. The heat absorbed from the room while the vessel is cooler than ambient cancels the heat lost to the room while it is warmer, making the net environmental heat exchange negligible."
        },
        {
            'title': 'Barometric Pressure Corrections to the Boiling Temperature T_s',
            'text': "The temperature T_s of saturated steam in equilibrium with boiling water depends directly upon the prevailing atmospheric barometric pressure P_atm. The canonical boiling temperature of 100.00 °C applies strictly at standard sea-level atmospheric pressure of 760.00 mmHg (101.325 kPa = 1.01325 bar). In a physical laboratory, day-to-day barometric fluctuations typically range between 730 mmHg and 780 mmHg, which shifts the actual steam temperature. Over this meteorological span, Regnault's empirical relation provides the boiling point correction: T_s = 100.00 °C + 0.0373 (P_atm − 760) − 0.00005 (P_atm − 760)², where P_atm is the barometric reading in millimeters of mercury corrected for temperature and local gravity. For instance, on a low-pressure stormy day with P_atm = 745 mmHg, steam boils at 99.44 °C, while at high elevations (e.g., 1,000 meters above sea level, P ≈ 674 mmHg), water boils near 96.8 °C. Assuming T_s = 100.0 °C when the true temperature is lower alters the sensible heat subtraction m_v c_w (T_s − T_f), introducing a systematic offset into L_v. Recording the laboratory barometer is therefore a mandatory step in high-precision steam calorimetry.",
            'formula': 'T_s = 100.00 \\, ^\\circ\\text{C} + 0.0373 (P_{\\text{atm}} - 760) \\quad (P_{\\text{atm}} \\text{ in mmHg})',
            'question': 'Why must the ambient barometric pressure be measured when determining the latent heat of vaporization?',
            'answer': 'The boiling point of water is 100 °C only at standard atmospheric pressure (760 mmHg). Departures in barometric pressure shift the steam temperature by approximately 0.037 °C per mmHg. Measuring barometric pressure ensures the exact steam temperature Ts is used when calculating sensible heat.'
        },
        {
            'title': 'Evaluation of Water Equivalent and System Heat Capacity C_sys',
            'text': "Accurate calculation of the absorbed thermal energy Q_gain requires accounting for all physical components that warm alongside the water bath. The water equivalent W_cal of a calorimeter vessel is defined as the mass of water that would absorb the identical quantity of thermal energy as the calorimeter body for the same temperature rise: W_cal = m_cal · (c_material / c_water). For a specularly polished thin-walled copper vessel of mass m_cal = 75.00 g and specific heat c_cu = 385.0 J kg⁻¹ K⁻¹, its thermal capacity is C_cal = 0.0750 kg × 385.0 J kg⁻¹ K⁻¹ = 28.875 J K⁻¹. Dividing by c_w = 4,186 J kg⁻¹ K⁻¹ yields a water equivalent of W_cal = 28.875 / 4186 = 0.00690 kg = 6.90 g of water. Adding the wire stirrer (mass 15.0 g, brass, c = 380 J kg⁻¹ K⁻¹; C_stir = 5.70 J K⁻¹) and the submerged glass bulb of the thermometer (approximate heat capacity C_therm ≈ 1.5 J K⁻¹) gives a total apparatus thermal capacity of approximately 36.08 J K⁻¹. When filled with 200.00 g of pure water (C_water = 0.200 kg × 4,186 J kg⁻¹ K⁻¹ = 837.20 J K⁻¹), the aggregate heat capacity of the system is C_sys = 837.20 + 28.88 = 866.08 J K⁻¹. The aggregate capacity C_sys scales the observed temperature rise (T_f − T_0) into total absorbed joules.",
            'formula': 'C_{\\text{sys}} = m_w c_w + m_{\\text{cal}} c_{\\text{cu}} + W_{\\text{acc}} = 866.08 \\text{ J K}^{-1}',
            'question': 'What is the physical meaning of the water equivalent of a calorimeter, and why must it be added to the water mass?',
            'answer': 'The water equivalent represents the mass of water that would have the same thermal capacity as the metal calorimeter vessel and stirrer. Because the metal warms through the identical temperature rise as the water, its thermal capacity must be included to account for all heat absorbed.'
        }
    ],
    'precautions': [
        'Blast steam vigorously through the water trap into a waste beaker for several minutes to thoroughly pre-heat the glass delivery tube before inserting it into the calorimeter.',
        'Wipe the exterior of the delivery nozzle immediately before immersion and withdraw it promptly when heating ceases to avoid back-siphoning.',
        'Stir the calorimeter water continuously and gently to ensure rapid mixing and complete thermal equilibration without splashing.',
        'Reweigh the calorimeter immediately after the run with its lid on to prevent evaporative loss from corrupting the condensed steam mass measurement.'
    ],
    'quiz': [
        {
            'question': 'In the condensation method for determining the latent heat of vaporization of water, how is the net latent heat Q_net calculated?',
            'options': [
                'Q_net = C_sys (T_f − T_0) − m_v c_w (T_s − T_f)',
                'Q_net = C_sys (T_f − T_0) + m_v c_w (T_s − T_f)',
                'Q_net = m_v c_w (T_s − T_0)',
                'Q_net = C_sys (T_s − T_f) / m_v'
            ],
            'correct': 0,
            'explanation': 'The total heat absorbed by the calorimeter and water is C_sys (T_f − T_0). Subtracting the sensible heat released by the condensed water cooling from T_s to T_f isolates the net latent heat released during the condensation phase change: Q_net = C_sys (T_f − T_0) − m_v c_w (T_s − T_f) = m_v L_v.'
        },
        {
            'question': 'What is the purpose of the water trap connected between the steam boiler and the calorimeter?',
            'options': [
                'To capture and drain entrained liquid water droplets, ensuring only dry steam enters the calorimeter.',
                'To increase the steam pressure to superheated levels.',
                'To measure the volume of steam produced by the boiler.',
                'To cool the steam down to room temperature before entering the water.'
            ],
            'correct': 0,
            'explanation': 'The water trap removes entrained liquid water droplets from the steam stream. If liquid droplets entered the calorimeter, they would add to the measured mass without releasing latent heat, falsely depressing the calculated latent heat of vaporization.'
        },
        {
            'question': 'How does Rumford’s radiation compensation method reduce heat exchange errors with the surroundings?',
            'options': [
                'By starting the water below room temperature by the same amount it ends above room temperature, balancing heat gain and loss.',
                'By surrounding the calorimeter with an electric heating coil maintained at 100 °C.',
                'By evacuating the air around the calorimeter to create a high vacuum.',
                'By coating the calorimeter with black paint to maximize radiative emission.'
            ],
            'correct': 0,
            'explanation': 'Rumford’s method balances environmental heat exchange by having the calorimeter absorb heat from the room while cooler than ambient and lose an equal amount of heat while warmer than ambient, producing zero net environmental exchange.'
        },
        {
            'question': 'When plotting Q_net on the vertical axis against the mass of condensed steam m_v on the horizontal axis, what physical constant is given by the gradient?',
            'options': [
                'The specific latent heat of vaporization L_v of water (J kg⁻¹ or kJ kg⁻¹).',
                'The specific heat capacity of liquid water c_w.',
                'The thermal water equivalent of the calorimeter W_cal.',
                'The boiling point temperature of water T_s.'
            ],
            'correct': 0,
            'explanation': 'Because Q_net = m_v · L_v, plotting Q_net against m_v yields a straight line through the origin whose slope S directly equals the specific latent heat of vaporization L_v.'
        }
    ],
    'limitations': 'The teaching simulation models condensation calorimetry under ideal dry steam conditions with constant steam temperature T_s = 100.00 °C, initial water temperature T_0 = 15.00 °C, and an invariant system heat capacity C_sys = 866.08 J K⁻¹. In physical laboratory execution, entrained liquid water droplets escaping through the steam trap can introduce wet steam errors, evaporative cooling from the warm water surface can reduce the apparent equilibrium temperature, thermometer stem emergent exposure can slightly depress readings, and barometric pressure departures alter the true boiling point from 100 °C.',
    'modelExtra': 'The simulation evaluates equilibrium temperatures using the exact thermodynamic conservation relation T_f = (m_v L_v + m_v c_w T_s + C_sys T_0) / (C_sys + m_v c_w), where m_v is the condensed steam mass in kilograms, L_v = 2,260,000 J kg⁻¹ (2,260.00 kJ kg⁻¹) is the reference latent heat of vaporization, c_w = 4,186 J kg⁻¹ K⁻¹ is the specific heat capacity of water, T_s = 100.00 °C is the steam temperature, T_0 = 15.00 °C is the initial chilled water temperature, and C_sys = 866.08 J K⁻¹ is the aggregate thermal capacity. Equilibrium temperatures are rounded to 0.01 °C to simulate precision calorimetric thermometry, and ordinary least-squares regression of Q_net against m_v yields the reported latent heat of vaporization.'
}

# 1. Update experiments.json
exp_path = ROOT / 'content/physics/experiments.json'
experiments = json.loads(exp_path.read_text())
existing_idx = next((i for i, e in enumerate(experiments) if e['slug'] == 'latent-heat-vaporization'), None)
if existing_idx is not None:
    experiments[existing_idx] = exp27
else:
    experiments.append(exp27)
exp_path.write_text(json.dumps(experiments, indent=2, ensure_ascii=False))
print(f'experiments.json updated. Total experiments: {len(experiments)}')

# 2. Update catalog.sqlite3
db_path = ROOT / 'data/catalog.sqlite3'
db = sqlite3.connect(db_path)
cur = db.cursor()
cur.execute('DELETE FROM experiments WHERE slug = ?', ('latent-heat-vaporization',))
cur.execute('''
    INSERT INTO experiments (subject_id, slug, title, status, page_path, theory_path, report_path)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    1,
    'latent-heat-vaporization',
    'Determination of latent heat of vaporization of water',
    'live',
    '/physics/latent-heat-vaporization/',
    '/physics/latent-heat-vaporization/theory/',
    '/physics/latent-heat-vaporization/report/'
))
db.commit()
db.close()
print('catalog.sqlite3 updated successfully for latent-heat-vaporization.')
