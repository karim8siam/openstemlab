import json, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

exp24 = {
    'number': 24,
    'slug': 'specific-heat-capacity',
    'title': 'Determination of Specific Heat Capacity by the Method of Mixtures',
    'shortTitle': 'Specific Heat Capacity',
    'aim': 'Determine the specific heat capacity c_s of copper using a water-equivalent jacketed calorimeter and the classical method of mixtures, verifying thermal energy conservation across variable specimen masses, and evaluating radiation heat exchange corrections.',
    'target': 'c_s',
    'targetName': 'Specific heat capacity of copper',
    'inputLabel': 'Specimen mass m_s',
    'shortInput': 'Mass m_s',
    'inputUnit': 'g',
    'inputDecimals': 1,
    'rawLabel': 'Equilibrium temperature T_f',
    'rawUnit': '°C',
    'rawDecimals': 2,
    'xAxis': 'Heat drop factor m_s (T_s − T_f) (kg K)',
    'yAxis': 'Heat absorbed C_sys (T_f − T_0) (J)',
    'xScale': 1.0,
    'yScale': 1.0,
    'gradientUnit': 'J kg⁻¹ K⁻¹',
    'resultUnit': 'J kg⁻¹ K⁻¹',
    'resultScale': 1.0,
    'resultDecimals': 1,
    'min': 40.0,
    'max': 240.0,
    'step': 10.0,
    'initial': 140.0,
    'samples': [60.0, 100.0, 140.0, 180.0, 220.0],
    'emptyX': [0.0, 20.0],
    'emptyY': [0.0, 7000.0],
    'timed': False,
    'angle': False,
    'published': True,
    'measureLabel': 'Transfer heated specimen to calorimeter and measure equilibrium temperature',
    'fitEquation': 'C_sys · (T_f − T_0) = c_s · [m_s · (T_s − T_f)] ⇔ Y = c_s · X ⇔ c_s = S',
    'intro': 'The quantitative measurement of heat as an extensive physical entity forms the bedrock of classical thermodynamics. Pioneered by Joseph Black in Edinburgh during the mid-eighteenth century, the distinction between temperature (an intensive thermodynamic state variable measuring average molecular kinetic energy) and heat (an extensive form of thermal energy transferred across a system boundary due to a macroscopic temperature gradient) transformed calorimetry into a rigorous precision science. The method of mixtures operates upon the foundational postulate of thermal energy conservation: in an adiabatic enclosure isolated from external work and heat exchange, the total enthalpy lost by a hot solid specimen upon immersion into a cooler liquid medium must identically equal the total enthalpy gained by the liquid, the containing calorimetric vessel, the thermometer bulb, and the mechanical stirrer as the combined system equilibrates to a uniform final temperature T_f. Because the container and its accessories participate directly in the thermal exchange, their aggregate thermal capacity is represented through the system water equivalent W_cal, defined as the mass of pure liquid water that would absorb an identical quantity of heat per degree temperature rise. By measuring the initial temperature of the boiling-water-heated specimen T_s, the initial ambient temperature of the calorimeter water T_0, and the asymptotic equilibrium temperature T_f across an incremental sequence of specimen masses, the specific heat capacity c_s of the metallic analyte is directly extracted from the linear slope of heat absorbed versus the thermal mass factor m_s (T_s - T_f).',
    'settings': [
        'Initial specimen temperature T_s = 100.0 °C (steam boiler at standard atmospheric pressure 101.325 kPa).',
        'Initial calorimeter water mass m_w = 0.200 kg (200.0 g), initial temperature T_0 = 20.0 °C, specific heat c_w = 4186.0 J kg⁻¹ K⁻¹.',
        'Calorimeter inner copper vessel (mass 150.0 g) and brass stirrer water equivalent W_cal = 0.020 kg; effective system thermal capacity C_sys = (m_w + W_cal) · c_w = 920.92 J K⁻¹.',
        'Pure copper reference specific heat capacity c_s = 385.0 J kg⁻¹ K⁻¹.'
    ],
    'apparatus': [
        {
            'name': 'Precision Double-Walled Jacketed Calorimeter Assembly',
            'purpose': 'Consists of an inner polished thin-walled copper containment vessel (mass 150.0 g, thermal capacity ~57.8 J K⁻¹), supported on insulating vulcanized cork pegs inside an outer concentric nickel-plated draft-shield jacket with an annular stagnant air gap to suppress convective and conductive heat transfer to the laboratory environment.'
        },
        {
            'name': 'Regnault Steam Boiler and Specimen Heating Chamber',
            'purpose': 'A cylindrical brass double-walled steam generator equipped with a vertical central heating chamber, rubber delivery tubing, and a sliding drop bottom shutter, designed to suspend metallic specimens in dry saturated water vapor at 100.0 °C until thermal equilibrium is verified without wetting the sample with condensation.'
        },
        {
            'name': 'Calibrated Precision Immersion Thermometers (0.01°C / 0.1°C Division)',
            'purpose': 'A paired set of mercury-in-glass standards: one graduated from 0°C to 105°C in 0.5°C divisions for monitoring the steam chamber core temperature, and a high-precision calorimetric thermometer graduated from 15°C to 35°C in 0.05°C subdivisions for detecting slight temperature excursions in the calorimeter.'
        },
        {
            'name': 'Mechanical Helical Brass Stirrer and Precision Analytical Balance',
            'purpose': 'A low-thermal-capacity looped brass wire stirrer designed to produce rapid convective mixing throughout the 200.0 g water bath without inducing kinetic frictional heating, alongside a two-pan analytical balance resolving mass to ±0.01 g for gravimetric metrology of water and copper specimens.'
        }
    ],
    'procedure': [
        {
            'title': 'Gravimetric Determination of Calorimeter Water Equivalent and Water Tare',
            'text': 'Carefully clean, dry, and weigh the empty inner copper calorimeter vessel together with the dry brass spiral stirrer to ±0.01 g. Record the dry mass m_cal. Multiply m_cal by the specific heat of copper (385 J kg⁻¹ K⁻¹) and the stirrer mass by that of brass (380 J kg⁻¹ K⁻¹), dividing by the specific heat of water (4186 J kg⁻¹ K⁻¹) to establish the theoretical water equivalent W_cal = 0.020 kg (20.0 g). Pipette or dispense exactly 200.0 g of distilled water into the inner vessel, reweigh the filled vessel to confirm m_w = 0.200 kg, mount the vessel on its cork support within the outer insulating jacket, and insert the precision calorimetric thermometer.',
            'why': 'Establishing the precise baseline heat capacity of the calorimetric vessel and water bath is critical because all heat transferred from the test specimen distributes across both the liquid water and the metallic containment structures. Any gravimetric error in water mass propagates directly into the inferred system thermal capacity.'
        },
        {
            'title': 'Specimen Suspension and Thermal Soaking in the Steam Boiler',
            'text': 'Weigh the dry copper specimen pellet charge (selected from 60.0 g to 220.0 g) on the analytical balance to ±0.01 g. Secure the charge inside the perforated copper specimen basket attached to a fine silk suspension thread. Lower the basket into the central heating tube of the Regnault steam generator, plug the top aperture with a loose non-absorbent cotton wool stopper to prevent vertical convective draft losses, and insert the 0–100°C reference thermometer directly into the core of the copper mass. Bring the boiler water to an active, vigorous boil, ensuring steam vents freely through the exhaust port, and soak the specimen until the core thermometer remains perfectly stationary at 100.0 °C for at least five continuous minutes.',
            'why': 'Metallic specimens possess finite bulk thermal conductivity, requiring sufficient soaking time for internal temperature gradients to completely decay. Ensuring dry saturated steam conditions guarantees that the specimen surface carries no liquid water droplets into the calorimeter, which would introduce severe latent heat contamination.'
        },
        {
            'title': 'Initial Calorimetric Temperature Baseline and Drift Monitoring',
            'text': 'Position the jacketed calorimeter assembly adjacent to the steam boiler delivery chute, but shielded by a rigid thermal insulating cardboard screen to prevent radiant heat from the boiler flame reaching the cold calorimeter. Stir the calorimeter water bath gently and continuously with the helical stirrer in steady vertical strokes. Read and record the calorimetric thermometer every 30 seconds for three minutes prior to the transfer to establish the preliminary natural background drift rate ΔT / Δt under ambient laboratory conditions. Confirm that the initial water temperature T_0 is steady at approximately 20.0 °C.',
            'why': 'A precise preliminary baseline establishes whether the calorimeter is gaining or losing heat to the ambient room air prior to specimen immersion, which is indispensable for applying Newton\'s law of cooling radiation corrections to the subsequent temperature rise.'
        },
        {
            'title': 'Rapid Specimen Transfer and Immersion',
            'text': 'At an agreed timer signal, smoothly swing the calorimeter under the boiler transfer chute or rapidly extract the copper specimen basket by its suspension thread. Immediately lower the glowing hot specimen cleanly into the water of the inner calorimeter vessel, submerging it completely beneath the water surface without touching the thermometer bulb or inner walls, and close the calorimeter lid within one to two seconds. Ensure that no water droplets splash outward from the vessel during entry.',
            'why': 'The transfer stage represents the most vulnerable operational window where radiative and convective heat losses to ambient air occur. Minimizing transit duration to under two seconds prevents sensible cooling of the specimen before immersion and eliminates mass loss from splashing.'
        },
        {
            'title': 'Agitation and Equilibrium Temperature Trajectory Tracking',
            'text': 'Commence continuous, smooth vertical agitation using the mechanical brass stirrer at approximately two strokes per second, ensuring intimate liquid circulation around the submerged copper pellets while avoiding surface splashing. Continuously observe the calorimetric thermometer meniscus using a magnifying cathetometer or reading lens to avoid parallax. Record the temperature at 15-second intervals as the mercury column climbs rapidly through an initial transient, peaks at an asymptotic maximum, and begins a very slow subsequent decay. Identify and record the peak equilibrium temperature T_f to ±0.01 °C.',
            'why': 'Water has a relatively low thermal conductivity, making mechanical agitation mandatory to break boundary-layer stagnation and achieve isothermal temperature distribution across the bath. Capturing the apex of the cooling curve pinpoints the true state of thermal equilibrium before environmental losses dominate.'
        },
        {
            'title': 'Radiation Cooling Drift Correction and Linear Least-Squares Analysis',
            'text': 'Continue recording the calorimeter temperature at one-minute intervals for five minutes following the peak to measure the final cooling rate into the room. Apply the Rumelin or Regnault-Pfaundler radiation correction to adjust T_f for convective and radiative dissipation during the mixing interval. Compute the net thermal energy absorbed by the system Q_sys = C_sys (T_f - T_0) and the thermal mass factor X = m_s (T_s - T_f). Repeat the complete operational sequence for all five specimen masses (60.0, 100.0, 140.0, 180.0, 220.0 g) and perform an ordinary least-squares regression of Q_sys against X to extract the specific heat capacity c_s from the gradient.',
            'why': 'Plotting thermal energy absorbed across varied specimen masses linearizes the energy balance equation, averaging out random transfer losses and isolating any constant systematic heat offset as the y-intercept, while the slope yields an unbiased, high-precision estimate of specific heat capacity.'
        }
    ],
    'topics': [
        {
            'title': 'The Nature of Heat, Internal Energy, and the First Law of Thermodynamics',
            'text': 'In classical physics prior to the thermodynamic revolution, heat was conceptualized as caloric—an indestructible, weightless fluid that flowed from warmer to cooler bodies. The decisive mechanical equivalent experiments of Benjamin Thompson (Count Rumford) boring cannon brass, followed by the rigorous quantitative paddle-wheel experiments of James Prescott Joule, permanently dismantled the caloric hypothesis by demonstrating that mechanical work could be converted indefinitely into thermal energy. Under the modern thermodynamic framework synthesized by Clausius and Kelvin, heat Q is strictly defined as thermal energy in transit across the macroscopic boundary of a thermodynamic system driven solely by a difference in temperature between the system and its surroundings. Heat is not a state function and cannot be regarded as an intrinsic property possessed by a substance. Instead, a system possesses internal energy U, which encompasses the microscopic translational kinetic energy of constituent particles, the rotational and vibrational energies of molecular bonds, and the potential energy associated with interatomic electrostatic lattice forces. When thermal energy is transferred into an incompressible solid without macroscopic work (dW = P dV = 0), the First Law of Thermodynamics dQ = dU + dW dictates that the entire absorbed heat manifests as an increment in the system internal energy dU = m c(T) dT, where c(T) is the specific heat capacity of the material.',
            'formula': 'dQ = dU + dW \\implies \\Delta U = m \\int_{T_1}^{T_2} c(T) \\, dT',
            'question': 'What is the thermodynamic distinction between heat, temperature, and internal energy?',
            'answer': 'Temperature is an intensive thermodynamic state variable measuring the mean kinetic energy per degree of freedom of the constituent particles. Internal energy is an extensive state function representing the total microscopic kinetic and potential energy stored within the molecular and lattice structures of the system. Heat is not a state function and cannot be possessed by a body; rather, it is energy in transit across a system boundary solely by virtue of a macroscopic temperature gradient.'
        },
        {
            'title': 'The Method of Mixtures and the Enthalpy Conservation Balance',
            'text': 'The method of mixtures constitutes the foundational experimental technique of quantitative calorimetry. When two or more bodies initially residing at differing uniform temperatures are brought into intimate physical contact inside an adiabatic enclosure (a container impermeable to heat exchange with the exterior surroundings, dQ_ext = 0), energy conservation demands that the net thermal enthalpy exchange across all interacting components must sum identically to zero: \\Sigma Q_i = 0. In the specific heat capacity determination of copper, a solid specimen of mass m_s and specific heat c_s preheated to initial temperature T_s is immersed into a calorimeter containing water of mass m_w and specific heat c_w at initial temperature T_0, alongside the containment vessel of mass m_cal and stirrer of mass m_stir. As heat flows spontaneously from the hot metal into the cooler liquid, the temperature of the specimen decreases while the temperature of the liquid bath and containment hardware increases until a common asymptotic equilibrium temperature T_f is attained. The sensible heat surrendered by the specimen is Q_lost = m_s c_s (T_s - T_f), while the sensible heat absorbed by the water and calorimetric accessories is Q_gained = (m_w c_w + m_cal c_cal + m_stir c_stir) (T_f - T_0). Equating heat lost to heat gained establishes the fundamental calorimetric balance equation from which c_s is algebraically determined.',
            'formula': 'm_s c_s (T_s - T_f) = (m_w c_w + m_{\\text{cal}} c_{\\text{cal}} + m_{\\text{stir}} c_{\\text{stir}}) (T_f - T_0)',
            'question': 'Why must the water equivalent of the calorimeter vessel and stirrer be incorporated into the mixture calculation?',
            'answer': 'The inner calorimeter vessel, the submerged portion of the stirrer, and the bulb of the thermometer are in direct, intimate thermal contact with the liquid water bath throughout the experiment. As the water warms from T_0 to T_f, these metallic and glass components necessarily undergo the identical temperature excursion, absorbing thermal energy in proportion to their respective heat capacities. Treating the vessel as an inactive boundary would underestimate the total heat surrendered by the specimen, causing a severe negative systematic error in the calculated specific heat.'
        },
        {
            'title': 'Calorimeter Water Equivalent and Thermal Capacity Formulation',
            'text': 'In every real calorimetric measurement, the vessel containing the working fluid, the stirrer employed to maintain spatial temperature uniformity, and the bulb of the thermometer participate directly in the thermal exchange. Because it is computationally cumbersome to separately account for each individual structural component, classical calorimetry introduces the concept of the water equivalent W_cal. The water equivalent is rigorously defined as the mass of pure liquid water that exhibits a thermal heat capacity exactly equal to the aggregate heat capacity of the calorimeter vessel and its submerged accessories. Mathematically, if a calorimeter consists of an inner copper vessel of mass m_cal with specific heat c_cal and a brass stirrer of mass m_stir with specific heat c_stir, the total thermal capacity of the dry apparatus is C_cal = m_cal c_cal + m_stir c_stir + C_therm, where C_therm is the small heat capacity of the immersed mercury thermometer bulb. Dividing C_cal by the specific heat capacity of water c_w yields the effective water equivalent: W_cal = C_cal / c_w. The total effective thermal capacity of the liquid-loaded calorimeter system is consequently expressed compactly as C_sys = (m_w + W_cal) c_w. For an inner copper vessel of 150.0 g (c_Cu = 385 J kg⁻¹ K⁻¹) and brass stirrer (c_brass = 380 J kg⁻¹ K⁻¹), W_cal evaluates to approximately 0.020 kg (20.0 g), giving C_sys = (0.200 + 0.020) × 4186.0 = 920.92 J K⁻¹.',
            'formula': 'W_{\\text{cal}} = \\frac{m_{\\text{cal}} c_{\\text{Cu}} + m_{\\text{stir}} c_{\\text{brass}} + C_{\\text{therm}}}{c_w} \\implies C_{\\text{sys}} = (m_w + W_{\\text{cal}}) c_w',
            'question': 'How can the water equivalent of a calorimeter be determined experimentally rather than calculated from published specific heats?',
            'answer': 'The water equivalent can be measured experimentally using the method of mixtures with water alone: a known mass of cold water at temperature T_c is placed in the calorimeter, and a known mass of warm water at temperature T_h is added from a reservoir. By measuring the resultant equilibrium temperature T_m, the energy conservation equation m_h c_w (T_h - T_m) = (m_c + W_cal) c_w (T_m - T_c) is solved directly for W_cal without relying upon assumed specific heat values for the vessel alloys.'
        },
        {
            'title': 'Newton\'s Law of Cooling and Radiation Exchange Corrections',
            'text': 'The ideal calorimetric equation assumes a strictly adiabatic boundary where no thermal energy escapes to or enters from the surrounding environment. In real laboratory conditions, complete adiabatic isolation is impossible: the calorimeter continuously exchanges heat with the room via radiation, convective air currents across the open top aperture, and conduction through the support pegs. Sir Isaac Newton formulated the empirical law of cooling, which states that for small temperature differences between a body and its environment (T - T_env < 30°C), the instantaneous rate of heat loss dQ/dt—and consequently the rate of temperature decrease dT/dt—is strictly proportional to the temperature excess: dT/dt = -k (T - T_env), where k is a cooling constant dependent upon the exposed surface area, emissivity, and ambient air circulation. During the finite time interval \\Delta t = t_f - t_0 required for the hot copper specimen to transfer its heat to the water and establish peak equilibrium, the calorimeter operates at temperatures above room ambient, shedding an unavoidable quantity of heat to the laboratory. To eliminate this systematic bias, experimentalists apply the Regnault-Pfaundler or Rumelin radiation correction: the ambient drift rate is monitored before immersion and after peak equilibrium, and numerical integration of k(T(t) - T_env) dt over the mixing interval provides the compensating temperature increment \\Delta T_rad to be added to the observed peak temperature T_f.',
            'formula': '\\frac{dT}{dt} = -k (T - T_{\\text{env}}) \\implies \\Delta T_{\\text{rad}} = k \\int_{t_0}^{t_f} (T(t) - T_{\\text{env}}) \\, dt',
            'question': 'How does Newton\'s law of cooling justify the radiation correction applied to the peak temperature in calorimetry?',
            'answer': 'For moderate temperature differences above ambient room temperature, the rate of heat loss by combined convection and radiation is strictly proportional to the instantaneous temperature excess (T - T_env). By recording the cooling rate in the post-equilibrium period where (T - T_env) is known, the cooling constant k is evaluated. Integrating k(T(t) - T_env) dt over the transient mixing interval provides the cumulative temperature loss \\Delta T_rad that escaped to the surroundings, which when added to the observed peak temperature restores the true adiabatic equilibrium temperature.'
        },
        {
            'title': 'Lattice Dynamics and the Dulong-Petit Classical Heat Capacity Law',
            'text': 'The microscopic origin of specific heat capacity in crystalline metallic solids was first systematized in 1819 by French physicists Pierre Louis Dulong and Alexis Thérèse Petit. Their empirical observation—now known as the Dulong-Petit Law—states that the molar heat capacity of all solid metallic elements is approximately constant and equal to 3R \\approx 24.94 J mol⁻¹ K⁻¹ (approximately 6 calories per mole per kelvin). In modern statistical mechanics, this law is derived from the classical equipartition theorem applied to harmonic lattice vibrations. In a solid crystal lattice consisting of N_A atoms per mole, each atom is bound in a three-dimensional harmonic potential well formed by adjacent nuclei, possessing three independent spatial vibrational modes. Each vibrational mode contributes two quadratic energy degrees of freedom (one for kinetic energy 1/2 m v² and one for harmonic potential energy 1/2 k x²). According to the equipartition theorem, each quadratic term contributes an average thermal energy of 1/2 k_B T at thermal equilibrium, yielding a total internal lattice vibrational energy of U_m = 6 \\times (1/2 k_B T) \\times N_A = 3 N_A k_B T = 3 R T. Differentiating with respect to temperature gives the constant molar heat capacity C_V = dU_m/dT = 3R. For pure copper with an atomic molar mass of M = 0.06355 kg mol⁻¹, the Dulong-Petit prediction for specific heat capacity is c_s = 3R / M = (3 \\times 8.314) / 0.06355 \\approx 392.5 J kg⁻¹ K⁻¹, which closely matches the experimental room-temperature value of 385.0 J kg⁻¹ K⁻¹. At cryogenic temperatures, quantum mechanical discretization of phonon modes freezes out high-frequency vibrations, causing specific heat to depart from the Dulong-Petit asymptote and collapse toward zero following the Debye T³ law.',
            'formula': 'C_{V,m} = 3R \\approx 24.94 \\, \\text{J mol}^{-1}\\text{ K}^{-1} \\implies c_s \\approx \\frac{3R}{M_{\\text{atomic}}} = \\frac{3 \\times 8.314}{0.06355} \\approx 392.5 \\, \\text{J kg}^{-1}\\text{ K}^{-1}',
            'question': 'Why does the classical Dulong-Petit law predict a universal molar heat capacity of approximately 3R for metallic solids at room temperature?',
            'answer': 'In a solid crystalline metallic lattice, each atom is bound to neighboring lattice sites and possesses three independent spatial vibrational degrees of freedom. Under the classical equipartition theorem of statistical mechanics, each harmonic vibrational mode contributes an average energy of k_B T (1/2 k_B T for kinetic energy and 1/2 k_B T for potential energy). For one mole (N_A atoms), the total thermal vibrational energy is U = 3 N_A k_B T = 3 R T. Differentiating with respect to temperature yields the molar heat capacity C_V = (\\partial U / \\partial T)_V = 3R \\approx 24.94 J mol⁻¹ K⁻¹, which holds with high accuracy for metals whose Debye temperatures are well below room temperature.'
        },
        {
            'title': 'Calorimetric Metrology, Thermometer Lag, and Immersion Corrections',
            'text': 'High-precision calorimetry imposes stringent demands on temperature metrology. In a typical method of mixtures experiment, the total temperature rise of the water bath is modest—often between 2°C and 7°C—meaning that an uncertainty of merely 0.05°C in temperature measurement induces a fractional error of 1% to 2.5% in the inferred specific heat capacity. Mercury-in-glass thermometers must possess fine capillary bores allowing readings to 0.01°C or 0.02°C. However, the physical thermometer bulb exhibits finite thermal mass and a thermal response time constant \\tau = m_bulb c_glass / (h A_bulb). If the water is stirred inadequately, the mercury thread will lag behind the true transient fluid temperature, underestimating the true peak equilibrium value. Furthermore, when a partial-immersion thermometer is utilized, the emergent mercury column residing in the stem above the calorimeter lid is exposed to ambient room air rather than the bath temperature, necessitating an emergent stem correction: \\Delta T_stem = K \\cdot N \\cdot (T - t_s), where K \\approx 0.00016 °C⁻¹ is the relative thermal expansion coefficient of mercury in glass, N is the length of the emergent column in scale degrees, T is the observed reading, and t_s is the mean temperature of the exposed stem. Continuous, gentle mechanical stirring with a low-conductivity brass or glass helical loop breaks laminar boundary layers around the thermometer bulb, guaranteeing rapid thermal equilibration without generating viscous dissipation heating.',
            'formula': '\\Delta T_{\\text{stem}} = K \\cdot N \\cdot (T - t_s) \\quad \\text{where } K \\approx 0.00016 \\, ^\\circ\\text{C}^{-1}',
            'question': 'Why is rapid, uniform mechanical stirring essential during the temperature equilibration phase?',
            'answer': 'Liquid water has a relatively poor thermal conductivity (k \\approx 0.6 W m⁻¹ K⁻¹), meaning that heat transferred from the hot copper specimen would remain localized in thermal plumes near the bottom of the vessel in the absence of active mixing. Mechanical stirring induces forced convection, ensuring that thermal energy is distributed uniformly throughout the entire water volume and to the calorimeter walls before significant heat is lost by radiation to the environment.'
        },
        {
            'title': 'Systematic Uncertainties, Heat Exchange Deficits, and Linearized Analysis',
            'text': 'A critical source of systematic error in classical calorimetry occurs during the rapid transfer of the specimen from the steam boiler into the calorimeter. During this 1-to-2-second aerial transit, the metallic charge sheds heat through intense convective cooling and blackbody radiation, causing the actual temperature of the specimen upon entering the water to be slightly lower than the measured steam boiler temperature T_s. If a single experimental measurement is analyzed in isolation, this transit heat deficit is inevitably attributed to an artificially lowered specific heat capacity. To circumvent this vulnerability, an advanced experimental design measures the equilibrium temperature across five distinct specimen masses (60 g to 220 g) under identical transfer protocols. The energy balance equation is rearranged into a linear mathematical form: Y = c_s \\cdot X + Q_loss, where Y = C_sys (T_f - T_0) represents the heat absorbed by the calorimeter and water, and X = m_s (T_s - T_f) represents the thermal mass drop factor. When Y is plotted against X in an ordinary least-squares regression, any constant transfer loss or water equivalent zero tare offset is absorbed harmlessly into the vertical intercept Q_loss, while the true, unbiased specific heat capacity c_s is isolated directly as the slope of the line. Achieving a coefficient of determination R² > 0.999 validates the linearity of thermal energy conservation across the investigated temperature regime.',
            'formula': 'Y = C_{\\text{sys}} (T_f - T_0), \\quad X = m_s (T_s - T_f) \\implies Y = c_s X + Q_{\\text{loss}}',
            'question': 'What physical insight is gained by plotting Q_sys against m_s(T_s - T_f) rather than calculating c_s from a single trial?',
            'answer': 'A single trial calculation forces the regression through the origin, attributing any unmodelled transfer loss (such as radiant heat lost during the transit from boiler to calorimeter) directly to the sample, thereby corrupting the specific heat estimate. Linear regression across varied sample masses decouples the constant transfer offset (which manifests as a non-zero intercept) from the true specific heat capacity, which is governed exclusively by the slope dY/dX.'
        }
    ],
    'precautions': [
        'Shield the calorimeter completely from the steam boiler flame and radiant heating using an insulating wooden or double-layered cardboard partition screen.',
        'Ensure the metallic specimen is suspended in dry steam for at least five minutes after the internal thermometer stabilizes at 100.0 °C to guarantee isothermal equilibrium without condensed water droplets.',
        'Execute the transfer of the heated specimen into the calorimeter within two seconds, keeping transit distance minimal to prevent convective cooling in ambient air.',
        'Maintain smooth, continuous vertical agitation with the stirrer while reading the thermometer to eliminate local thermal stratification without causing splashing.'
    ],
    'quiz': [
        {
            'question': 'Under the classical Dulong-Petit law, what is the approximate molar heat capacity of solid copper at room temperature?',
            'options': [
                'Approximately 3R ≈ 24.9 J mol⁻¹ K⁻¹',
                'Approximately 1/2 R ≈ 4.16 J mol⁻¹ K⁻¹',
                'Approximately 5/2 R ≈ 20.8 J mol⁻¹ K⁻¹',
                'Approximately 6R ≈ 49.8 J mol⁻¹ K⁻¹'
            ],
            'correct': 0,
            'explanation': 'Under the classical equipartition theorem for a 3D harmonic lattice, each atom possesses 3 vibrational modes each contributing k_B T of energy (kinetic plus potential), yielding a total molar energy U = 3 N_A k_B T = 3 R T. The molar heat capacity is C_V = dU/dT = 3R ≈ 24.94 J mol⁻¹ K⁻¹.'
        },
        {
            'question': 'How does an aerial transit delay during the transfer of the heated specimen affect the uncorrected single-trial calculated specific heat capacity?',
            'options': [
                'It underestimates c_s because heat lost to ambient air reduces the observed temperature rise of the water bath.',
                'It overestimates c_s because ambient air heats the specimen further during transit.',
                'It has no effect because specific heat capacity is an intensive material constant independent of heat loss.',
                'It increases the apparent water equivalent of the calorimeter vessel.'
            ],
            'correct': 0,
            'explanation': 'If the specimen sheds heat to the room during aerial transit, it enters the calorimeter at a temperature below T_s. The resulting water bath temperature rise is smaller than expected for an adiabatic transfer at T_s, leading the uncorrected mixture formula to underestimate the true specific heat capacity.'
        },
        {
            'question': 'What is the physical definition of the water equivalent of a calorimeter?',
            'options': [
                'The mass of water that possesses the same thermal heat capacity as the calorimeter vessel and its accessories.',
                'The volume of water required to fill the inner calorimeter vessel to exactly half capacity.',
                'The mass of water evaporated from the calorimeter during one hour of continuous operation.',
                'The ratio of the density of the calorimeter metal to the density of pure liquid water.'
            ],
            'correct': 0,
            'explanation': 'The water equivalent W_cal represents the effective mass of water whose thermal capacity (W_cal · c_w) equals the total heat capacity of the calorimeter vessel, stirrer, and thermometer bulb (m_cal c_cal + m_stir c_stir + C_therm).'
        },
        {
            'question': 'In the linear regression of heat absorbed Y = C_sys (T_f − T_0) versus thermal mass factor X = m_s (T_s − T_f), what physical property is represented by the slope?',
            'options': [
                'The specific heat capacity c_s of the metallic specimen (J kg⁻¹ K⁻¹).',
                'The latent heat of vaporization of water at standard atmospheric pressure.',
                'The thermal conductivity of the inner copper calorimeter vessel.',
                'The Newton cooling rate constant k of the double-walled jacket.'
            ],
            'correct': 0,
            'explanation': 'From the heat balance equation C_sys (T_f − T_0) = c_s · [m_s (T_s − T_f)], the dependent variable Y is proportional to the independent variable X through the constant of proportionality c_s, making the regression slope directly equal to the specific heat capacity.'
        }
    ],
    'limitations': 'The teaching simulation assumes zero heat transfer during the rapid 1.5-second transit from the steam boiler to the calorimeter, constant specific heats of water and copper over the 20°C to 100°C interval, and instantaneous thermal conduction throughout the specimen pellets. In actual laboratory calorimetry, sensible cooling during transit, radiative and convective heat exchange with room air during the non-isothermal mixing interval, evaporative losses from the agitated warm water surface, and finite thermometer response time constants must be rigorously quantified using Regnault-Pfaundler radiation corrections.',
    'modelExtra': 'The mathematical model integrates a constant calorimeter system thermal capacity C_sys = 920.92 J K⁻¹ (comprising 200.0 g pure water with c_w = 4186.0 J kg⁻¹ K⁻¹ and a 20.0 g water equivalent calorimeter vessel and brass stirrer) and evaluates final equilibrium temperatures using the exact energy balance equation T_f = (m_s c_s T_s + C_sys T_0) / (m_s c_s + C_sys) with pure copper reference specific heat c_s = 385.0 J kg⁻¹ K⁻¹, initial sample temperature T_s = 100.0°C, and initial water temperature T_0 = 20.0°C.'
}

# 1. Update experiments.json
exp_path = ROOT / 'content/physics/experiments.json'
experiments = json.loads(exp_path.read_text())
existing_idx = next((i for i, e in enumerate(experiments) if e['slug'] == 'specific-heat-capacity'), None)
if existing_idx is not None:
    experiments[existing_idx] = exp24
else:
    experiments.append(exp24)
exp_path.write_text(json.dumps(experiments, indent=2, ensure_ascii=False))
print(f'experiments.json updated. Total experiments: {len(experiments)}')

# 2. Update catalog.sqlite3
db_path = ROOT / 'data/catalog.sqlite3'
db = sqlite3.connect(db_path)
cur = db.cursor()
cur.execute('DELETE FROM experiments WHERE slug = ?', ('specific-heat-capacity',))
cur.execute('''
    INSERT INTO experiments (subject_id, slug, title, status, page_path, theory_path, report_path)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    1,
    'specific-heat-capacity',
    'Specific heat capacity by method of mixtures',
    'live',
    '/physics/specific-heat-capacity/',
    '/physics/specific-heat-capacity/theory/',
    '/physics/specific-heat-capacity/report/'
))
db.commit()
db.close()
print('catalog.sqlite3 updated successfully.')
