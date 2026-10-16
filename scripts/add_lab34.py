import json, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

exp34 = {
    'number': 34,
    'slug': 'vapor-pressure',
    'title': 'Determination of the Saturated Vapor Pressure and Enthalpy of Vaporization of a Volatile Liquid',
    'shortTitle': 'Saturated Vapor Pressure',
    'aim': 'Measure the saturated vapor pressure of pure ethyl alcohol (ethanol) across temperatures from 20.0 °C to 80.0 °C using an immersed vapor pressure tube and precision mercury manometer, verify the Clausius-Clapeyron equation ln(P) = −(ΔH_vap / R)(1/T) + C, and determine the molar enthalpy of vaporization ΔH_vap.',
    'target': 'ΔH_{\\text{vap}}',
    'targetName': 'Molar enthalpy of vaporization ΔH_vap',
    'inputLabel': 'Bath temperature t',
    'shortInput': 'Temperature t',
    'inputUnit': '°C',
    'inputDecimals': 1,
    'rawLabel': 'Saturated vapor pressure P',
    'rawUnit': 'kPa',
    'rawDecimals': 2,
    'xAxis': 'Reciprocal temperature 1/T (10⁻³ K⁻¹)',
    'yAxis': 'Log vapor pressure ln(P / Pa)',
    'xScale': 1000.0,
    'yScale': 1.0,
    'gradientUnit': 'K',
    'resultUnit': 'kJ mol⁻¹',
    'resultScale': 0.001,
    'resultDecimals': 2,
    'min': 20.0,
    'max': 80.0,
    'step': 5.0,
    'initial': 20.0,
    'samples': [20.0, 35.0, 50.0, 65.0, 80.0],
    'emptyX': [2.5, 3.6],
    'emptyY': [8.0, 12.0],
    'timed': False,
    'angle': False,
    'published': True,
    'measureLabel': 'Measure Equilibrium Saturated Vapor Pressure P (kPa)',
    'fitEquation': '\\ln(P) = -\\frac{\\Delta H_{\\text{vap}}}{R} \\left(\\frac{1}{T}\\right) + C \\iff y = m x + b \\iff \\Delta H_{\\text{vap}} = -m R',
    'intro': "When a pure volatile liquid is introduced into an evacuated closed space, molecules possessing sufficient thermal kinetic energy escape from the liquid phase into the adjacent headspace through the process of surface vaporization. Simultaneously, vapor-phase molecules collide with the liquid interface and condense. Once dynamic equilibrium is attained—the rate of vaporization equaling the rate of condensation—the pressure exerted by the vapor reaches a unique, stable value known as the saturated vapor pressure (P_sat). Saturated vapor pressure depends exclusively on the chemical nature of the substance and its thermodynamic temperature, remaining completely independent of the relative volumes occupied by the liquid and vapor phases provided both phases coexist. The fundamental thermodynamic relation governing this liquid-vapor coexistence boundary was formulated by the French engineer Émile Clapeyron in 1834 using Carnot’s thermodynamic cycle, and later given a rigorous microscopic and mathematical foundation by the German physicist Rudolf Clausius in 1850. The exact Clapeyron equation expresses the slope of the coexistence curve as dP/dT = L_v / [T (V_v − V_l)], where L_v is the latent heat of vaporization per mole and V_v and V_l are the molar volumes of the saturated vapor and liquid, respectively. Because the molar volume of a gas at moderate pressures is several orders of magnitude greater than that of the condensed liquid (V_v ≫ V_l), the liquid volume V_l may be neglected with minimal error (V_v − V_l ≈ V_v). Furthermore, approximating the vapor as an ideal gas obeying the equation of state V_v = RT/P yields the famous Clausius-Clapeyron differential equation: dP/dT = (ΔH_vap P) / (R T²), or equivalently, d(ln P) / d(1/T) = −ΔH_vap / R, where ΔH_vap is the molar enthalpy of vaporization and R = 8.31446 J mol⁻¹ K⁻¹ is the universal gas constant. Assuming the enthalpy of vaporization remains approximately constant over a moderate temperature interval, integrating this differential equation yields the linear working relationship ln(P) = −(ΔH_vap / R)(1/T) + C. In the classical precision physics laboratory, this relationship is investigated using a submerged vapor pressure tube containing pure ethyl alcohol (ethanol, C₂H₅OH) completely immersed in a stirred, thermostatically controlled liquid heating bath. The vapor pressure tube is coupled to a precision mercury manometer. By recording the equilibrium vapor pressure P across a sequence of temperatures from room temperature up to the normal boiling point (78.4 °C), and plotting ln(P) against the reciprocal absolute temperature 1/T, students obtain an exceptionally straight regression line whose negative slope m = −ΔH_vap / R directly yields the molar enthalpy of vaporization ΔH_vap = −m R, providing deep empirical insight into intermolecular cohesion and phase transition thermodynamics.",
    'settings': [
        'Pure spectrophotometric grade ethyl alcohol (ethanol, C₂H₅OH, molecular weight M = 46.069 g mol⁻¹) degassed by vacuum distillation.',
        'Ambient atmospheric barometric pressure B = 760.0 mmHg = 101.325 kPa verified by precision Fortin laboratory barometer.',
        'Thermostatically regulated water bath with motorized propeller agitator maintaining thermal stability within ±0.05 °C.',
        'Precision mercury manometer tube with mirror-backed millimeter scale (mercury density ρ = 13,595 kg m⁻³ at 0 °C).',
        'Accepted literature reference molar enthalpy of vaporization for ethanol: ΔH_vap_ref = 41.92 kJ mol⁻¹ (41,920 J mol⁻¹) over 20 °C to 80 °C.'
    ],
    'apparatus': [
        {
            'name': 'Borosilicate Saturated Vapor Pressure J-Tube Assembly',
            'purpose': 'A specialized glass U-tube containing an evacuated upper bulb partially filled with degassed liquid ethanol, with the liquid-vapor meniscus positioned inside the submerged bulb and communicating with a mercury column.'
        },
        {
            'name': 'Precision Liquid Mercury Manometer with Millimeter Mirror Scale',
            'purpose': 'Measures the difference in mercury column heights between the vapor-filled closed limb and open atmospheric limb to register the differential gauge vapor pressure Δh to ±0.2 mmHg.'
        },
        {
            'name': 'Thermostatically Regulated Heating Water Bath with Immersion Element',
            'purpose': 'Surrounds the vapor bulb in a deep water bath, heated by an adjustable electrical resistance coil to maintain steady operating temperatures between 20.0 °C and 80.0 °C.'
        },
        {
            'name': 'Motor-Driven Propeller Stirrer and Convection Shield',
            'purpose': 'Provides continuous, vigorous fluid circulation throughout the heating bath, eliminating vertical thermal stratification and ensuring identical temperature across the entire vapor bulb.'
        },
        {
            'name': 'Precision Secondary Standard Immersion Thermometer (0 to 100 °C)',
            'purpose': 'Calibrated mercury-in-glass thermometer with 0.1 °C subdivisions, suspended directly alongside the vapor bulb to record the liquid equilibrium temperature to ±0.05 °C.'
        },
        {
            'name': 'Fortin Precision Mercurial Laboratory Barometer',
            'purpose': 'Determines the ambient atmospheric pressure B in mmHg and kPa, required to convert open-limb manometer differential readings into total absolute vapor pressure P = B + Δh.'
        }
    ],
    'procedure': [
        {
            'title': 'Barometric Reference Measurement and Initial Apparatus Inspection',
            'text': 'Read the laboratory Fortin mercurial barometer to 0.1 mmHg, applying temperature and brass scale corrections to determine the ambient atmospheric pressure B (baseline B = 760.0 mmHg = 101.325 kPa). Inspect the vapor pressure tube to verify that the upper bulb contains pure liquid ethanol free of trapped atmospheric air bubbles and that the mercury surfaces are clean and reflective.',
            'why': 'Because the open limb of the manometer is exposed to the atmosphere, the absolute vapor pressure is calculated from P = B + Δh. An accurate barometric reading is indispensable for evaluating absolute pressure.'
        },
        {
            'title': 'Room Temperature Equilibrium Baseline Acquisition at 20.0 °C',
            'text': 'Fill the water bath with tap water adjusted to 20.0 °C. Position the vapor bulb completely submerged beneath the liquid surface and run the motorized stirrer for at least five minutes. Confirm that the bath thermometer reading remains steady at 20.0 °C and the mercury menisci in the manometer limbs have ceased drifting. Read the heights of the mercury columns in both limbs.',
            'why': 'Sufficient equilibration time guarantees that the liquid ethanol and its vapor achieve true dynamic phase equilibrium at the measured bath temperature before taking data.'
        },
        {
            'title': 'Incremental Water Bath Heating and Thermal Homogenization',
            'text': 'Energize the electric heating coil to warm the bath progressively in 15.0 °C intervals (35.0 °C, 50.0 °C, 65.0 °C, 80.0 °C). Keep the propeller stirrer operating continuously at moderate speed to circulate the water evenly around the glass vapor chamber and thermometer stem.',
            'why': 'Active stirring prevents convective thermal gradients from forming in the bath, ensuring that the enclosed ethanol sample attains the identical temperature indicated by the thermometer.'
        },
        {
            'title': 'Thermal Relaxation Dwell Interval at Target Stations',
            'text': 'Upon reaching each target temperature, adjust the heater power to maintain a stable plateau and wait for a dwell interval of at least three to four minutes. Confirm that the temperature remains constant to within ±0.05 °C and the mercury column elevation stabilizes.',
            'why': 'Because glass has finite thermal conductivity and liquid evaporation absorbs latent heat, a dwell period is required to re-establish thermal and phase equilibrium between the bath, liquid ethanol, and saturated vapor.'
        },
        {
            'title': 'Parallax-Free Acquisition of Manometer Column Heights',
            'text': 'Read the mercury column levels in both the closed vapor limb (h_closed) and open atmospheric limb (h_open) using the mirror-backed millimeter scale. Align the optical line of sight so that the mercury meniscus directly occludes its reflected image in the mirror, eliminating parallax error. Compute the gauge pressure Δh = h_open − h_closed and determine the absolute pressure P = B + Δh in kilopascals (kPa).',
            'why': 'Mirror-backed sighting removes visual parallax, guaranteeing reliable millimeter height measurements across all thermal stations.'
        },
        {
            'title': 'Cooling Verification Run & Clausius-Clapeyron Linear Analysis',
            'text': 'Turn off the electric heater and record repeat readings at the same temperature stations as the bath cools naturally to verify the absence of thermal hysteresis or air ingress. Convert all temperatures to absolute kelvins (T = t + 273.15 K) and compute the reciprocal temperature 1/T. Calculate the natural logarithm of vapor pressure ln(P / Pa), plot ln(P) versus 1/T, and determine the slope m to evaluate the molar enthalpy of vaporization ΔH_vap = −m R.',
            'why': 'Verifying identical pressures during cooling proves that the sample is free from non-condensable air contamination and that the system remained in reversible thermodynamic equilibrium throughout the cycle.'
        }
    ],
    'topics': [
        {
            'title': 'Molecular Kinetics of Vaporization and Saturated Vapor Pressure',
            'text': 'At the microscopic level, molecules in a liquid are bound together by intermolecular attractive forces (van der Waals dispersion, dipole-dipole interactions, and hydrogen bonding). Because of continuous thermal collisions, molecular kinetic energies are distributed according to the Maxwell-Boltzmann distribution: f(E) ∝ √E exp(−E / k_B T). Only those molecules located near the liquid surface whose normal kinetic energy component exceeds the cohesive binding energy barrier (the activation energy of vaporization E_vap) can overcome intermolecular attractions and escape into the vapor phase. The rate of vaporization per unit surface area is therefore proportional to exp(−E_vap / k_B T). Conversely, molecules in the vapor phase undergo chaotic thermal motion and frequently strike the liquid surface, where a fraction α_c (the condensation accommodation coefficient) is captured back into the liquid. The rate of condensation is directly proportional to the collision frequency of vapor molecules, which by the kinetic theory of gases is given by the Hertz-Knudsen relation: J_cond = P / √(2π m k_B T). When dynamic equilibrium is established, the rate of vaporization equals the rate of condensation: J_vap = J_cond. Equating these rates yields the equilibrium vapor pressure: P_sat ∝ T^(1/2) exp(−E_vap / k_B T), showing that vapor pressure increases exponentially with temperature. Because the equilibrium condition depends solely on the balance between molecular kinetic energy and intermolecular cohesive potential, the saturated vapor pressure is strictly an intensive thermodynamic property; it depends exclusively on temperature and the chemical identity of the liquid, remaining completely independent of the surface area or the relative volume of the container.',
            'formula': 'J_{\\text{vap}} = J_{\\text{cond}} = \\frac{P_{\\text{sat}}}{\\sqrt{2\\pi m k_B T}} \\implies P_{\\text{sat}}(T) = P_0 \\exp\\left(-\\frac{\\Delta H_{\\text{vap}}}{R T}\\right)',
            'question': 'Why does the saturated vapor pressure of a liquid depend exponentially on temperature rather than linearly?',
            'answer': 'Vaporization requires molecules to overcome a cohesive energy barrier (E_vap). According to the Maxwell-Boltzmann distribution, the fraction of molecules possessing kinetic energy greater than this barrier scales exponentially as exp(−E_vap / k_BT). Raising the temperature increases this high-energy population exponentially, causing vapor pressure to rise exponentially.'
        },
        {
            'title': 'The Clapeyron and Clausius-Clapeyron Equations of State',
            'text': 'The rigorous thermodynamic description of first-order phase transitions originates from the requirement of chemical potential equality across phase boundaries. For liquid and vapor phases in coexistence at temperature T and pressure P, the molar Gibbs free energies must be identical: G_m,l(T, P) = G_m,v(T, P). Moving along the coexistence curve by an infinitesimal increment (dT, dP) maintains equilibrium: dG_m,l = dG_m,v. Using the fundamental thermodynamic relation dG_m = −S_m dT + V_m dP, we obtain −S_m,l dT + V_m,l dP = −S_m,v dT + V_m,v dP, which rearranges to dP/dT = (S_m,v − S_m,l) / (V_m,v − V_m,l). Because the phase transition occurs reversibly at constant temperature, the molar entropy change is related to the molar latent heat of vaporization by ΔS_m = S_m,v − S_m,l = ΔH_vap / T. Substituting this into the derivative yields the exact Clapeyron equation: dP/dT = ΔH_vap / [T (V_m,v − V_m,l)]. Rudolf Clausius introduced two brilliant and physically justified approximations: (1) at pressures well below the critical point, the molar volume of the liquid is negligible compared to that of the vapor (V_m,v ≫ V_m,l, hence V_m,v − V_m,l ≈ V_m,v); (2) the vapor behaves as an ideal gas obeying V_m,v = RT/P. Substituting these approximations into Clapeyron’s equation gives dP/dT = (ΔH_vap P) / (R T²), which can be written in logarithmic form as d(ln P) / dT = ΔH_vap / (R T²), or equivalently, d(ln P) / d(1/T) = −ΔH_vap / R. Assuming ΔH_vap is constant over the measurement range, integration yields ln(P) = −(ΔH_vap / R)(1/T) + C, providing a powerful linear relationship that allows the enthalpy of vaporization to be extracted directly from experimental P-T data.',
            'formula': '\\frac{dP}{dT} = \\frac{\\Delta H_{\\text{vap}}}{T (V_{m,v} - V_{m,l})} \\approx \\frac{\\Delta H_{\\text{vap}} P}{R T^2} \\implies \\frac{d(\\ln P)}{d(1/T)} = -\\frac{\\Delta H_{\\text{vap}}}{R}',
            'question': 'What two key physical approximations transform the exact Clapeyron equation into the Clausius-Clapeyron equation?',
            'answer': 'First, neglecting the molar volume of the liquid compared to that of the vapor (V_m,v − V_m,l ≈ V_m,v). Second, treating the vapor as an ideal gas obeying V_m,v = RT/P. Both approximations are highly accurate for volatile liquids at temperatures well below their critical points.'
        },
        {
            'title': 'Intermolecular Forces and Hydrogen Bonding in Ethyl Alcohol',
            'text': 'The magnitude of the enthalpy of vaporization ΔH_vap provides direct empirical quantification of the strength of intermolecular forces holding the liquid phase together. Ethyl alcohol (ethanol, CH₃CH₂OH) is an amphiphilic molecule containing both an ethyl non-polar hydrocarbon group and a polar hydroxyl (−OH) functional group. The electronegativity difference between oxygen (3.44) and hydrogen (2.20) creates a strong electric dipole moment along the O−H bond, enabling ethanol molecules to engage in extensive intermolecular hydrogen bonding. In liquid ethanol at room temperature, molecules form dynamic, transient oligomeric chains and rings held together by hydrogen bonds with individual bond dissociation energies of approximately 20 to 25 kJ mol⁻¹. In addition to hydrogen bonding, ethanol molecules experience dipole-dipole interactions and London dispersion forces arising from the polarizability of the electron cloud of the ethyl group. The total molar enthalpy of vaporization ΔH_vap ≈ 42 kJ mol⁻¹ represents the total energetic cost required to completely disrupt all these intermolecular attractive interactions and transfer one mole of ethanol from the condensed liquid state into the non-interacting vapor state. In contrast, non-polar liquids of comparable molecular weight (such as propane, CH₃CH₂CH₃, M = 44 g mol⁻¹, ΔH_vap ≈ 19 kJ mol⁻¹) exhibit much weaker dispersion forces and boil at −42 °C. Diethyl ether ((C₂H₅)₂O, M = 74 g mol⁻¹), which has dipole-dipole forces but lacks hydrogen-bond donors, has ΔH_vap ≈ 27 kJ mol⁻¹ and boils at 34.6 °C. The substantially higher enthalpy of vaporization and elevated boiling point of ethanol (78.4 °C) provide striking thermodynamic evidence for the robust network of intermolecular hydrogen bonds in the liquid.',
            'formula': '\\Delta H_{\\text{vap}} = \\Delta H_{\\text{dispersion}} + \\Delta H_{\\text{dipole}} + \\Delta H_{\\text{H-bond}} \\approx 42\\text{ kJ mol}^{-1} \\text{ (for C}_2\\text{H}_5\\text{OH)}',
            'question': 'Why is the enthalpy of vaporization of ethanol (42 kJ/mol) substantially higher than that of diethyl ether (27 kJ/mol) despite ether having a larger molecular mass?',
            'answer': 'Ethanol possesses a hydroxyl (−OH) group capable of forming strong intermolecular hydrogen bonds, whereas diethyl ether has no O−H bonds and interacts only through weaker dipole-dipole and dispersion forces. Breaking the hydrogen-bonding network in ethanol requires significantly greater thermal energy.'
        },
        {
            'title': 'Boiling Point Thermodynamics and Ambient Barometric Dependence',
            'text': 'The boiling point of a liquid is thermodynamically defined as the temperature at which its saturated vapor pressure equals the prevailing external atmospheric pressure: P_sat(T_b) = P_ext. At temperatures below the boiling point, vaporization is strictly confined to the liquid surface because any vapor bubble attempting to form within the bulk liquid would have an internal pressure P_sat < P_ext and would be instantaneously crushed by the surrounding hydrostatic pressure. When the liquid is heated to T_b such that P_sat = P_ext, vapor bubbles can nucleate and grow throughout the bulk volume, leading to the rapid, vigorous phase transition known as boiling. The normal boiling point is specifically defined for an external pressure of exactly 1 standard atmosphere (P_ext = 101.325 kPa = 760.0 mmHg), which for pure ethanol is 78.37 °C. Because ambient atmospheric pressure fluctuates with weather systems and decreases exponentially with geographic altitude, the observed boiling point varies from day to day. The sensitivity of the boiling point to barometric pressure is quantitatively predicted by the inverted Clausius-Clapeyron equation: dT_b / dP = (R T_b²) / (ΔH_vap P). For ethanol at 1 atm, dT_b / dP ≈ 0.034 °C per mmHg (or 0.255 °C per kPa). A drop in barometric pressure of 20 mmHg (common during cyclonic weather) depresses the boiling point of ethanol by nearly 0.7 °C. Trouton’s rule provides an empirical benchmark for non-associated liquids, stating that the entropy of vaporization at the normal boiling point is approximately constant: ΔS_vap = ΔH_vap / T_b ≈ 85 to 88 J mol⁻¹ K⁻¹. For ethanol, ΔS_vap = 41,920 J mol⁻¹ / 351.52 K ≈ 119.2 J mol⁻¹ K⁻¹, which significantly exceeds Trouton’s constant. This positive deviation occurs because liquid ethanol is highly ordered due to hydrogen bonding; vaporizing it destroys this microscopic order, resulting in a substantially larger increase in entropy.',
            'formula': '\\frac{dT_b}{dP} = \\frac{R T_b^2}{\\Delta H_{\\text{vap}} P}, \\quad \\Delta S_{\\text{vap}} = \\frac{\\Delta H_{\\text{vap}}}{T_b} \\approx 119.2\\text{ J mol}^{-1}\\text{ K}^{-1} > 88\\text{ J mol}^{-1}\\text{ K}^{-1} \\text{ (Trouton deviation)}',
            'question': 'Why does ethanol exhibit a significant positive deviation from Trouton’s rule (ΔS_vap ≈ 119 J/(mol·K) vs 88 J/(mol·K))?',
            'answer': 'Trouton’s rule applies to disordered liquids. Liquid ethanol has a high degree of microscopic structural order resulting from its hydrogen-bonded network. Vaporization disrupts this ordered structure, causing an exceptionally large gain in entropy upon entering the random gas phase.'
        },
        {
            'title': 'Empirical Vapor Pressure Equations: Antoine and Wagner Formulations',
            'text': 'Over wide temperature intervals extending from the triple point to the critical point, the assumption of constant enthalpy of vaporization breaks down because the heat capacity of the vapor differs from that of the liquid: d(ΔH_vap)/dT = ΔC_p = C_p,v − C_p,l. Because the liquid has additional vibrational and librational modes, C_p,l > C_p,v, meaning ΔC_p is negative and ΔH_vap decreases steadily as temperature rises toward the critical temperature T_c (where ΔH_vap vanishes identically). To achieve high-precision representation of experimental vapor pressures across engineering applications, empirical equations with additional fitting parameters are employed. The most widely used formulation is the three-parameter Antoine equation: log₁₀(P) = A − B / (T + C), where A, B, and C are substance-specific empirical constants and T is temperature in Celsius. For ethyl alcohol over the temperature range of 20 °C to 90 °C, the standard Antoine parameters (with P in mmHg and T in °C) are A = 8.20417, B = 1642.89, and C = 230.300. The parameter C acts as a temperature adjustment that accounts for the curvature induced by ΔC_p. In thermodynamic metrology, the even more sophisticated four-parameter Wagner equation is used for reference-grade data: ln(P / P_c) = (T_c / T) [a τ + b τ^1.5 + c τ^3 + d τ^6], where τ = 1 − T/T_c. However, over the moderate 60 °C laboratory interval investigated here (20 °C to 80 °C), the simple two-parameter Clausius-Clapeyron equation fits the experimental data with an extraordinary coefficient of determination (R² > 0.9999), demonstrating that the mean effective enthalpy of vaporization ΔH_vap is an exceptionally accurate thermodynamic parameter for instructional physics.',
            'formula': '\\log_{10}(P_{\\text{mmHg}}) = A - \\frac{B}{T + C} \\iff \\ln(P_{\\text{Pa}}) \\approx -\\frac{\\Delta H_{\\text{eff}}}{R}\\left(\\frac{1}{T}\\right) + C_0',
            'question': 'Why does the enthalpy of vaporization ΔH_vap decrease at higher temperatures and vanish at the critical point?',
            'answer': 'As temperature rises, thermal expansion diminishes the density of the liquid while compression increases the density of the vapor. At the critical point, the liquid and vapor densities become identical and the meniscus disappears, meaning no energetic barrier exists between phases, so ΔH_vap becomes zero.'
        },
        {
            'title': 'Manometric Metrology: Saturated Vapor Tubes and Volatile Mixtures',
            'text': 'The physical measurement of saturated vapor pressure requires isolating the liquid-vapor system from non-condensable ambient gases. In the classical laboratory method for saturated vapors, pairs of vapor pressure tubes are utilized: one closed (evacuated and sealed) and one open to atmospheric pressure. The closed tube operates as a differential barometer: the space above the mercury column contains only the volatile liquid and its saturated vapor. When the tube is submerged in a cold bath, the vapor pressure is low and the mercury column stands high; as the bath is warmed, the vapor pushes the mercury column down. In an open-tube manometer, the volatile liquid is contained inside a bulb connected to a U-tube containing mercury whose outer limb is open to the atmosphere. The absolute pressure is then P = B + (h_open − h_closed). A crucial precaution is degassing the liquid before sealing: any dissolved atmospheric air (oxygen or nitrogen) will desorb into the vapor space upon heating. In accordance with Dalton’s law of partial pressures, the total measured pressure would be P_total = P_sat + P_air, producing a false positive pressure offset that corrupts the Clausius-Clapeyron slope. In binary mixtures (such as an ethanol-ether system), Raoult’s law states that each volatile component exerts a partial pressure proportional to its liquid mole fraction: P_i = x_i P_i*. Because diethyl ether has a much higher vapor pressure than ethanol, the vapor phase of the mixture is strongly enriched in ether, illustrating the fundamental principle of fractional distillation.',
            'formula': 'P_{\\text{total}} = P_{\\text{sat}}(T) + P_{\\text{air}}, \\quad P_{\\text{mixture}} = x_A P_A^* + x_B P_B^* \\text{ (Raoult’s Law)}',
            'question': 'How does dissolved air in the volatile liquid introduce a systematic error into the measured vapor pressure?',
            'answer': 'Dissolved air desorbs from the liquid upon heating and enters the vapor headspace. By Dalton’s law of partial pressures, the manometer measures P_total = P_sat + P_air. Because the trapped air pressure increases with temperature according to the ideal gas law, it adds a temperature-dependent offset that distorts both the intercept and the slope of the Clausius-Clapeyron fit.'
        },
        {
            'title': 'Error Propagation and Linear Regression in Clausius-Clapeyron Analysis',
            'text': 'To extract the enthalpy of vaporization ΔH_vap and its experimental uncertainty from paired measurements of temperature t and vapor pressure P, the data are transformed into linear coordinates: x_i = 1 / T_i (where T_i = t_i + 273.15 K) and y_i = ln(P_i / Pa). The ordinary least-squares regression line y = m x + b is fitted to the n data points. The slope m is given by m = [n Σ(x_i y_i) − (Σx_i)(Σy_i)] / [n Σx_i² − (Σx_i)²]. The molar enthalpy of vaporization is directly proportional to the slope: ΔH_vap = −m R. Because R is an exact fundamental physical constant defined in the SI system (R = 8.314462618 J mol⁻¹ K⁻¹), the standard error in the enthalpy of vaporization is determined entirely by the standard error of the regression slope: s_{ΔH} = R · s_m = R · √[s² / Σ(x_i − x̄)²], where s² = Σ(y_i − mx_i − b)² / (n − 2) is the residual variance of the fit. A critical metrological consideration is that the logarithmic transformation y = ln(P) non-linearly weights experimental pressure errors: dy = dP / P. A constant absolute pressure measurement uncertainty (e.g., ±0.2 mmHg from scale reading) translates into a relative uncertainty dy = δP / P that is substantially larger at low temperatures where P is small (at 20 °C, P ≈ 44 mmHg, so dy ≈ 0.2/44 = 0.0045) than at high temperatures near the boiling point (at 80 °C, P ≈ 812 mmHg, so dy ≈ 0.2/812 = 0.00025). High-precision analytical evaluations may utilize weighted least-squares regression with weights w_i = 1 / (δy_i)² ∝ P_i²; however, over the five standard stations investigated here, ordinary least squares yields an estimate within 0.02% of the reference enthalpy, demonstrating exceptional metrological robustness.',
            'formula': 'y = \\ln(P), \\quad x = \\frac{1}{T}, \\quad m = -\\frac{\\Delta H_{\\text{vap}}}{R} \\implies s_{\\Delta H} = R \\cdot s_m = R \\sqrt{\\frac{s^2}{\\sum (x_i - \\bar{x})^2}}',
            'question': 'Why does a constant absolute pressure error δP have a much larger impact on the Clausius-Clapeyron variable y = ln(P) at low temperatures than at high temperatures?',
            'answer': 'Because dy = d(ln P) = dP / P. The error in y is inversely proportional to the absolute pressure P. At low temperatures, P is small, so a given pressure error δP constitutes a much larger fractional uncertainty, producing a larger deviation in y.'
        }
    ],
    'quiz': [
        {
            'question': 'According to the Clausius-Clapeyron equation ln(P) = −(ΔH_vap / R)(1/T) + C, what does the slope m of a plot of ln(P) versus 1/T represent?',
            'options': [
                'The slope m is equal to −ΔH_vap / R, so ΔH_vap = −m R.',
                'The slope m is directly equal to the latent heat of vaporization: m = ΔH_vap.',
                'The slope m represents the absolute zero of temperature: m = −273.15 °C.',
                'The slope m is equal to the normal boiling point in kelvins: m = T_b.'
            ],
            'correct': 0,
            'explanation': 'Differentiating the integrated Clausius-Clapeyron equation with respect to (1/T) yields d(ln P)/d(1/T) = −ΔH_vap / R. Therefore, the slope of the linear plot is m = −ΔH_vap / R, and ΔH_vap = −m R.'
        },
        {
            'question': 'What thermodynamic condition defines the normal boiling point of a pure liquid?',
            'options': [
                'The temperature at which the saturated vapor pressure equals standard atmospheric pressure (101.325 kPa = 760 mmHg).',
                'The temperature at which all intermolecular forces inside the liquid completely disappear.',
                'The temperature at which the density of the liquid equals the density of mercury.',
                'The temperature where the rate of vaporization drops to zero.'
            ],
            'correct': 0,
            'explanation': 'Boiling occurs when the saturated vapor pressure of the liquid equals the external ambient pressure. The normal boiling point is specifically defined at 1 standard atmosphere (101.325 kPa = 760 mmHg).'
        },
        {
            'question': 'Why is the molar enthalpy of vaporization of ethanol (ΔH_vap ≈ 42 kJ/mol) significantly greater than that of non-polar substances of similar molar mass?',
            'options': [
                'Because ethanol molecules form extensive intermolecular hydrogen bonds via their polar −OH groups.',
                'Because ethanol molecules have a higher molecular weight than all non-polar liquids.',
                'Because ethanol decomposes into carbon dioxide and water vapor upon heating.',
                'Because the vapor of ethanol does not obey the ideal gas law at any temperature.'
            ],
            'correct': 0,
            'explanation': 'Ethanol contains a polar hydroxyl group (−OH) that forms strong intermolecular hydrogen bonds (20–25 kJ/mol). Vaporizing ethanol requires substantial thermal energy to disrupt this hydrogen-bonded network.'
        },
        {
            'question': 'How does dissolved air inside the volatile liquid sample affect the experimentally measured vapor pressure?',
            'options': [
                'Dissolved air desorbs into the vapor space upon heating, adding an extraneous partial pressure that falsely increases the measured pressure.',
                'Dissolved air reacts chemically with ethanol to prevent vapor formation.',
                'Dissolved air increases the surface tension of mercury, reversing the manometer reading.',
                'Dissolved air causes the boiling point of ethanol to drop to 0 °C.'
            ],
            'correct': 0,
            'explanation': 'By Dalton’s law of partial pressures, any air released from solution adds its own partial pressure (P_total = P_sat + P_air), leading to an overestimation of the true saturated vapor pressure.'
        }
    ],
    'precautions': [
        'Ensure the volatile liquid sample has been thoroughly degassed prior to sealing the vapor tube to prevent trapped air from exerting an extraneous partial pressure.',
        'Run the motorized stirrer continuously to ensure the heating bath maintains a completely uniform temperature without vertical stratification around the submerged vapor bulb.',
        'Wait at least three to four minutes at each temperature station before recording data to verify that dynamic liquid-vapor phase equilibrium is fully re-established.',
        'Use an optical magnifier aligned horizontally with the mirror backing on the manometer scale to eliminate visual parallax when sighting the mercury menisci.'
    ],
    'limitations': 'The teaching model assumes the enthalpy of vaporization ΔH_vap remains constant over the 20 °C to 80 °C temperature range and that the ethanol vapor behaves as an ideal gas. In rigorous thermodynamics, ΔH_vap decreases slightly with temperature due to non-zero heat capacity differences (ΔC_p = C_p,v − C_p,l), and ethanol vapor exhibits slight non-ideality near its normal boiling point.',
    'modelExtra': 'The Clausius-Clapeyron equation provides the thermodynamic cornerstone connecting macroscopic phase equilibria with microscopic intermolecular binding forces. The measured molar enthalpy of vaporization ΔH_vap = 41.92 kJ mol⁻¹ demonstrates the substantial energetic cost of disrupting intermolecular hydrogen bonds during the liquid-to-vapor phase transition.'
}

# Update content/physics/experiments.json
exp_path = ROOT / 'content/physics/experiments.json'
experiments = json.loads(exp_path.read_text())

existing_idx = next((i for i, x in enumerate(experiments) if x['slug'] == 'vapor-pressure'), None)
if existing_idx is not None:
    experiments[existing_idx] = exp34
    print(f"Updated existing Lab 34 in experiments.json at index {existing_idx}")
else:
    experiments.append(exp34)
    print(f"Appended Lab 34 to experiments.json (Total: {len(experiments)})")

exp_path.write_text(json.dumps(experiments, indent=2, ensure_ascii=False))

# Update catalog.sqlite3
db_path = ROOT / 'data/catalog.sqlite3'
db = sqlite3.connect(db_path)
sid = db.execute("SELECT id FROM subjects WHERE slug='physics'").fetchone()[0]

home = f"/physics/{exp34['slug']}/"
db.execute('''
    INSERT INTO experiments(subject_id, slug, title, status, page_path, theory_path, report_path)
    VALUES(?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(slug) DO UPDATE SET
        title=excluded.title,
        status=excluded.status,
        page_path=excluded.page_path,
        theory_path=excluded.theory_path,
        report_path=excluded.report_path
''', (sid, exp34['slug'], exp34['shortTitle'], 'live', home, home + 'theory/', home + 'report/'))

db.commit()
db.close()
print("Lab 34 successfully registered in catalog.sqlite3!")
