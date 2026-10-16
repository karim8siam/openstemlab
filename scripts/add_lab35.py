import json, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

exp35 = {
    'number': 35,
    'slug': 'air-humidity',
    'title': 'Determination of Atmospheric Humidity and the Psychrometric Constant',
    'shortTitle': 'Atmospheric Humidity',
    'aim': 'Determine the psychrometric constant A, actual water vapor pressure e, relative humidity RH, and dew-point temperature of ambient air across wet-bulb depressions from 2.0 °C to 10.0 °C at dry-bulb temperature 25.0 °C using a ventilated wet-and-dry bulb psychrometer and a polished-mirror dew-point hygrometer, verifying the Ferrel-Sprung psychrometric equation Δe = e_s(t_w) − e = A · P_atm · (t_d − t_w).',
    'target': 'A',
    'targetName': 'Psychrometric constant A',
    'inputLabel': 'Wet-bulb depression Δt',
    'shortInput': 'Depression Δt',
    'inputUnit': '°C',
    'inputDecimals': 1,
    'rawLabel': 'Vapor pressure depression Δe',
    'rawUnit': 'Pa',
    'rawDecimals': 1,
    'xAxis': 'Wet-bulb depression Δt (°C)',
    'yAxis': 'Vapor pressure depression Δe (Pa)',
    'xScale': 1.0,
    'yScale': 1.0,
    'gradientUnit': 'Pa K⁻¹',
    'resultUnit': 'K⁻¹',
    'resultScale': 1.0,
    'resultDecimals': 7,
    'min': 2.0,
    'max': 10.0,
    'step': 1.0,
    'initial': 2.0,
    'samples': [2.0, 4.0, 6.0, 8.0, 10.0],
    'emptyX': [0.0, 12.0],
    'emptyY': [0.0, 800.0],
    'timed': False,
    'angle': False,
    'published': True,
    'measureLabel': 'Measure Equilibrium Vapor Pressure Depression Δe (Pa)',
    'fitEquation': '\\Delta e = e_s(t_w) - e = \\gamma \\cdot \\Delta t = (A \\cdot P_{\\text{atm}}) \\cdot (t_d - t_w) \\iff y = m x + b \\iff A = \\frac{m}{P_{\\text{atm}}}',
    'intro': "Atmospheric humidity—the concentration of invisible gaseous water vapor dispersed throughout ambient air—is a paramount meteorological parameter that governs terrestrial weather dynamics, atmospheric thermodynamics, cloud formation, precipitation, and biophysical evaporative cooling. In atmospheric physics, humidity is characterized through several complementary metrics: absolute humidity (vapor density, expressed in grams of water vapor per cubic meter of air), specific humidity (mass of vapor per unit mass of moist air), mixing ratio (mass of vapor per unit mass of dry air), partial vapor pressure e (exerted by water molecules in Pascals or millimeters of mercury), and relative humidity (RH, the ratio of actual vapor pressure e to the saturation vapor pressure e_s at prevailing dry-bulb temperature t_d, expressed as a percentage: RH = (e / e_s(t_d)) × 100%). While direct gravimetric determination—drawing a metered volume of air through desiccating tubes containing phosphorus pentoxide or anhydrous calcium chloride and weighing the absorbed water—is conceptually straightforward, it is experimentally tedious and slow. Consequently, physical meteorology universally relies on indirect thermodynamic instruments, principally the wet-and-dry bulb psychrometer (formulated by Ernst Ferdinand August in 1825 and Adolf Sprung in 1888) and the dew-point hygrometer (devised by John Frederic Daniell in 1820 and Henri Victor Regnault in 1845). In a psychrometer, two matched thermometers are exposed to a steady stream of air: the dry bulb indicates true ambient air temperature t_d, while the wet bulb is enveloped in a porous cotton muslin sleeve saturated with pure distilled water. Evaporation of water into the unsaturated airstream absorbs latent heat of vaporization (L_v ≈ 2.45 × 10⁶ J kg⁻¹), chilling the wet bulb until dynamic thermal equilibrium is established—where convective heat transfer from the warmer ambient air to the wet bulb exactly balances the latent heat carried away by the diffusing water vapor. The resulting wet-bulb depression Δt = t_d − t_w is thermodynamically related to ambient vapor pressure e via the classical Ferrel-Sprung psychrometric equation: e = e_s(t_w) − A · P_atm · (t_d − t_w), where e_s(t_w) is the saturation vapor pressure at wet-bulb temperature t_w, P_atm is ambient barometric pressure, and A is the empirical psychrometric constant (A ≈ 6.60 × 10⁻⁴ K⁻¹ for ventilated airflow ≥ 2.5 m s⁻¹). In complementary dew-point hygrometry, ambient air is brought into contact with a brightly polished metallic mirror whose temperature is progressively lowered by evaporative cooling of an internal volatile liquid until the surrounding air layer becomes saturated, whereupon the first microscopic film of dew dulls the mirror finish. At this dew-point temperature t_dew, the actual vapor pressure equals the saturation vapor pressure: e = e_s(t_dew). By pairing psychrometric wet-bulb depressions with dew-point determinations across diverse ambient humidity states, students can directly verify the Ferrel-Sprung relation, plot the vapor pressure depression Δe = e_s(t_w) − e against wet-bulb depression Δt, extract the psychrometric slope γ = A · P_atm, determine the universal psychrometric constant A = γ / P_atm, and accurately calculate atmospheric relative humidity.",
    'settings': [
        'Ambient dry-bulb laboratory temperature maintained at t_d = 25.00 °C (saturation vapor pressure e_s(25 °C) = 3.168 kPa = 23.76 mmHg).',
        'Standard ambient atmospheric barometric pressure P_atm = 101.325 kPa (760.0 mmHg) verified by Fortin mercurial barometer.',
        'Ventilated psychrometer airflow maintained at constant forced convection velocity v ≥ 3.0 m s⁻¹ via motorized aspiration fan.',
        'Regnault-style polished silvered-copper dew-point mirror cup with integral internal optical illumination and magnifier.',
        'Accepted standard psychrometric constant for ventilated psychrometer: A_ref = 6.600 × 10⁻⁴ K⁻¹ (psychrometric slope γ = 66.875 Pa K⁻¹).'
    ],
    'apparatus': [
        {
            'name': 'Precision Ventilated Wet-and-Dry Bulb Psychrometer (Assmann Type)',
            'purpose': 'Comprises two matched, radiation-shielded secondary standard thermometers graduated in 0.1 °C divisions, equipped with a motor-driven aspiration fan delivering a uniform airflow (≥ 3.0 m s⁻¹) across the dry bulb and cotton-sleeved wet bulb.'
        },
        {
            'name': 'Regnault Polished-Mirror Dew-Point Hygrometer Apparatus',
            'purpose': 'A thin-walled silvered copper thimble containing volatile diethyl ether, equipped with an aspirator air tube to induce rapid evaporative cooling and an illuminated viewing window to detect the exact onset of moisture condensation.'
        },
        {
            'name': 'Fortin Precision Mercurial Laboratory Barometer',
            'purpose': 'Measures the prevailing ambient atmospheric pressure P_atm in mmHg and kPa to ±0.1 mmHg, required for the barometric factor in the Ferrel-Sprung psychrometric relation.'
        },
        {
            'name': 'Fine Muslin Wick and Distilled Water Reservoir',
            'purpose': 'A high-purity, degreased tubular cotton sleeve fitted snugly over the wet bulb, drawing pure distilled water continuously by capillary action without introducing dissolved salts that would lower water vapor pressure.'
        },
        {
            'name': 'Digital Immersion RTD Temperature Sensor (Reference Dew Sensor)',
            'purpose': 'Submerged inside the dew cup ether bath adjacent to the polished silver mirror wall to register the appearance and disappearance dew temperatures to ±0.02 °C.'
        },
        {
            'name': 'Rubber Squeeze Bulb and Needle Valve Aspiration Tube',
            'purpose': 'Provides controlled, gentle airflow through the volatile ether bath, allowing the experimenter to regulate the rate of cooling and warming around the dew point.'
        }
    ],
    'procedure': [
        {
            'title': 'Barometric Pressure Calibration and Muslin Wick Conditioning',
            'text': 'Read the laboratory Fortin mercurial barometer to 0.1 mmHg, applying temperature corrections to establish the true ambient barometric pressure P_atm (baseline P_atm = 101.325 kPa = 760.0 mmHg). Clean the wet-bulb cotton muslin sleeve thoroughly with pure distilled water, ensuring it fits snugly without wrinkles or air gaps over the thermometer bulb, and fill the wetting reservoir with fresh distilled water.',
            'why': 'Ambient pressure directly scales the psychrometric constant term (γ = A · P_atm). Clean muslin and pure distilled water ensure unimpeded capillary wicking and prevent dissolved minerals from depressing the saturation vapor pressure.'
        },
        {
            'title': 'Aspiration Fan Activation and Dry-Bulb Baseline Acquisition',
            'text': 'Activate the motor-driven aspiration fan on the psychrometer to generate a steady airflow of at least 3.0 m s⁻¹ through the protective radiation shields. Allow the airflow to stabilize for three minutes, then record the steady dry-bulb temperature t_d (nominal baseline t_d = 25.0 °C). Confirm that the dry bulb reading remains constant to within ±0.05 °C.',
            'why': 'A minimum air speed of 2.5 to 3.0 m s⁻¹ is required to saturate the convective boundary layer and render the psychrometric constant A independent of airflow fluctuations.'
        },
        {
            'title': 'Wet-Bulb Equilibrium Temperature Reading',
            'text': 'Observe the descending temperature of the wet-bulb thermometer under forced aspiration, recording readings every thirty seconds. Once the wet-bulb temperature stabilizes at its minimum plateau for two consecutive minutes (indicating dynamic equilibrium between convective sensible heat gain and latent heat loss), record the wet-bulb temperature t_w and compute the wet-bulb depression Δt = t_d − t_w.',
            'why': 'The steady minimum wet-bulb reading represents true thermodynamic psychrometric equilibrium, free from transient thermal lag.'
        },
        {
            'title': 'Dew-Point Mirror Condensation Sighting (Appearance Temperature)',
            'text': 'Gently squeeze the rubber aspirator bulb to bubble ambient air through the volatile ether contained within the silvered dew cup, watching the highly polished mirror surface through the optical magnifier. As evaporative cooling lowers the cup temperature, note the exact thermometer reading t_1 at the first instant a dulling film of condensed dew droplets mists the silver mirror.',
            'why': 'The initial dulling marks the exact point where the adjacent air layer reaches 100% saturation, providing the upper bound for the dew point.'
        },
        {
            'title': 'Dew Evaporation Sighting (Disappearance Temperature) & Mean Dew Point',
            'text': 'Immediately cease air aspiration through the ether, allowing the dew cup to warm slowly by heat conduction from the room. Note the exact temperature t_2 at which the moisture film completely vanishes and the mirror regains its brilliant specular reflection. Compute the true dew-point temperature as the arithmetic mean: t_dew = (t_1 + t_2) / 2.',
            'why': 'Averaging the appearance and disappearance temperatures cancels thermal conduction lag across the metallic cup wall, yielding an accurate measure of the true thermodynamic dew point.'
        },
        {
            'title': 'Vapor Pressure Computation & Psychrometric Slope Regression',
            'text': 'Using saturation vapor pressure tables (or the Tetens equation), evaluate the saturation vapor pressure at the wet-bulb temperature e_s(t_w) and the actual vapor pressure e = e_s(t_dew). Compute the vapor pressure depression Δe = e_s(t_w) − e in Pascals. Repeat the observations across multiple ambient humidity states (wet-bulb depressions Δt = 2.0, 4.0, 6.0, 8.0, 10.0 °C). Plot Δe versus Δt, determine the slope γ, and compute the psychrometric constant A = γ / P_atm.',
            'why': 'Linear regression of Δe against Δt directly verifies the Ferrel-Sprung relation and yields the psychrometric constant A with high statistical precision.'
        }
    ],
    'topics': [
        {
            'title': 'Thermodynamic Theory of the Wet-Bulb Psychrometer',
            'text': 'The wet-bulb psychrometer operates on the principle of coupled simultaneous heat and mass transfer within the convective boundary layer surrounding an evaporating liquid water film. Consider a wet thermometer bulb of surface area A_s immersed in an airstream moving with velocity v. The ambient air is at dry-bulb temperature t_d, total atmospheric pressure P_atm, and partial vapor pressure e. The wet-bulb surface is at equilibrium temperature t_w and is saturated with water vapor at saturation pressure e_s(t_w). Because t_d > t_w, heat is transferred by convection from the warmer air to the cooler bulb at a rate given by Newton’s law of cooling: dQ/dt = h_c A_s (t_d − t_w), where h_c is the convective heat transfer coefficient (W m⁻² K⁻¹). Simultaneously, water evaporates from the wet surface into the unsaturated air at a molar mass transfer rate given by convection-diffusion: dm/dt = k_m A_s (e_s(t_w) − e) / P_atm, where k_m is the convective mass transfer coefficient (mol m⁻² s⁻¹). Evaporating water absorbs the molar latent heat of vaporization ΔH_vap (J mol⁻¹), which removes thermal energy from the bulb at a rate dQ_evap/dt = (dm/dt) ΔH_vap = k_m A_s ΔH_vap (e_s(t_w) − e) / P_atm. At steady-state dynamic equilibrium, the rate of convective heat gain exactly balances the rate of latent heat loss: dQ/dt = dQ_evap/dt. Equating these two expressions and canceling the surface area A_s yields: h_c (t_d − t_w) = [k_m ΔH_vap / P_atm] (e_s(t_w) − e). Rearranging for the vapor pressure difference gives the psychrometric equation: e_s(t_w) − e = [h_c P_atm / (k_m ΔH_vap)] (t_d − t_w) = A P_atm (t_d − t_w), where A = h_c / (k_m ΔH_vap) is the psychrometric constant. According to the Chilton-Colburn analogy between heat and mass transfer, the ratio of heat to mass transfer coefficients is governed by the Lewis number: h_c / k_m = C_p,air (Sc / Pr)^(2/3) ≈ C_p,air (Le)^(2/3), where C_p,air is the humid air molar heat capacity, Pr is the Prandtl number, and Sc is the Schmidt number. For water vapor in air, the Lewis number is Le ≈ 0.86, making the ratio h_c / k_m nearly constant over normal meteorological temperatures.',
            'formula': 'h_c (t_d - t_w) = \\frac{k_m \\Delta H_{\\text{vap}}}{P_{\\text{atm}}} [e_s(t_w) - e] \\implies e_s(t_w) - e = A \\cdot P_{\\text{atm}} (t_d - t_w) \\text{ where } A = \\frac{h_c}{k_m \\Delta H_{\\text{vap}}}',
            'question': 'How does steady-state dynamic equilibrium explain why the wet bulb maintains a constant temperature below ambient air temperature?',
            'answer': 'At steady state, the rate of sensible heat transferred by convection from the warmer ambient air into the wet bulb exactly equals the rate of latent heat extracted by the evaporating water vapor. As long as the airflow and ambient humidity remain steady, the two opposing heat flows balance at a fixed, lower equilibrium temperature t_w.'
        },
        {
            'title': 'The Ferrel and Sprung Psychrometric Formulations',
            'text': 'The practical application of psychrometry requires empirical calibration to account for residual radiative heat transfer from surrounding walls and non-unity Lewis number effects. In 1888, the German meteorologist Adolf Sprung conducted exhaustive wind-tunnel investigations that established the standard psychrometric formula adopted internationally by the World Meteorological Organization (WMO): e = e_s(t_w) − A P_atm (t_d − t_w), where for a ventilated psychrometer with forced airflow velocity v ≥ 2.5 m s⁻¹, Sprung’s constant is A = 6.60 × 10⁻⁴ K⁻¹ (for mercury temperatures above 0 °C) and A = 5.80 × 10⁻⁴ K⁻¹ (over an ice-covered wick below 0 °C). In the United States, William Ferrel in 1886 developed an equivalent formulation for the U.S. Weather Bureau incorporating a slight temperature correction: e = e_s(t_w) − 0.000660 P_atm (t_d − t_w) [1 + 0.00115 (t_w − 0)]. In unventilated (stagnant) hygrometers, such as the simple wall-mounted Mason psychrometer, the absence of forced convection allows a stagnant, semi-saturated boundary layer to accumulate around the wet bulb. Consequently, molecular diffusion dominates over turbulent convection, radiative heat exchange from room walls contributes a larger relative fraction of the total heat budget (~15–20%), and the effective psychrometric constant increases significantly to A ≈ 7.9 × 10⁻⁴ to 8.2 × 10⁻⁴ K⁻¹. This sensitivity to air velocity explains why standard meteorological practice mandates the use of either the sling psychrometer (whirled vigorously by hand at ~200 rpm to achieve tip velocities of 4–5 m s⁻¹) or the Assmann aspiration psychrometer (utilizing a spring-driven or electric centrifugal fan). Once airflow exceeds 2.5 m s⁻¹, the convective heat transfer coefficient h_c becomes so large that radiative heat transfer contributes less than 1% of the total heat flux, and A becomes strictly constant at 6.60 × 10⁻⁴ K⁻¹.',
            'formula': 'e = e_s(t_w) - A \\cdot P_{\\text{atm}} (t_d - t_w), \\quad A_{\\text{ventilated}} = 6.60 \\times 10^{-4}\\text{ K}^{-1}, \\quad A_{\\text{stagnant}} \\approx 8.0 \\times 10^{-4}\\text{ K}^{-1}',
            'question': 'Why does an unventilated (stagnant air) psychrometer require a larger psychrometric constant A than a ventilated psychrometer?',
            'answer': 'In stagnant air, evaporation builds up a localized humid boundary layer that retards mass transfer, while radiative heat exchange from surrounding room walls supplies an unshielded heat flow into the wet bulb. This extra thermal input diminishes the wet-bulb depression, requiring a higher empirical constant A (~8.0 × 10⁻⁴ K⁻¹ vs 6.6 × 10⁻⁴ K⁻¹) to compute the correct vapor pressure.'
        },
        {
            'title': 'The Dew-Point Method and Physical Phase Boundary Condensation',
            'text': 'The dew-point method is a fundamental, direct thermodynamic technique that measures the saturation temperature of water vapor without relying on empirical convection models. Consider unsaturated moist air at dry-bulb temperature t_d possessing an actual partial vapor pressure e. If this air parcel is cooled isobarically at constant atmospheric pressure P_atm without adding or removing moisture, its actual vapor pressure e remains strictly constant. However, the saturation vapor pressure e_s(T) decreases rapidly with falling temperature following the exponential Clausius-Clapeyron curve. Eventually, a critical temperature is reached where the saturation vapor pressure of the cooled air equals the prevailing partial vapor pressure: e_s(t_dew) = e. This critical temperature is the dew-point temperature t_dew. Any infinitesimal further cooling forces the air into a supersaturated state (e > e_s), inducing heterogeneous nucleation of liquid water droplets onto adjacent solid surfaces. In the Regnault and Alluard dew-point hygrometers, a thin-walled polished silver or gold-plated copper cup containing a volatile liquid (diethyl ether) is cooled by passing a gentle stream of air bubbles through the liquid. The experimenter observes the polished specular surface with an illuminated magnifying viewer. The moment the surface temperature reaches t_dew, the mirror finish is abruptly dulled by the deposition of a microscopic fog of condensed liquid water droplets. When aspiration ceases, the mirror warms by conductive heat transfer from the room; the temperature at which the mist completely evaporates is recorded. Averaging the appearance and disappearance temperatures cancels the thermal conduction gradient across the metal wall. Because e_s(t_dew) = e, the dew point provides an absolute, primary physical standard for evaluating water vapor pressure: e = 0.61078 exp[17.27 t_dew / (t_dew + 237.3)] kPa.',
            'formula': 'e = e_s(t_{\\text{dew}}) \\implies \\text{RH} = \\frac{e}{e_s(t_d)} \\times 100\\% = \\frac{e_s(t_{\\text{dew}})}{e_s(t_d)} \\times 100\\%',
            'question': 'Why is the dew-point temperature t_dew always less than or equal to the dry-bulb temperature t_d?',
            'answer': 'Air cannot hold more water vapor than its saturation limit under equilibrium conditions. Unless the air is already at 100% relative humidity (in which case t_d = t_w = t_dew), the actual vapor pressure e is less than the saturation pressure e_s(t_d). Cooling the air is therefore necessary to lower e_s down to e, ensuring t_dew ≤ t_w ≤ t_d.'
        },
        {
            'title': 'Saturation Vapor Pressure Formulations: Tetens and Goff-Gratch',
            'text': 'To convert measured temperatures into vapor pressures with high metrological precision, atmospheric scientists utilize empirical and semi-empirical equations derived from the Clausius-Clapeyron relation. Over pure liquid water between −20 °C and +50 °C, the widely used formulation is the three-parameter Tetens equation (1930): e_s(t) = 0.61078 exp[17.27 t / (t + 237.3)], where t is in degrees Celsius and e_s is obtained in kilopascals (kPa). To express pressure in millimeters of mercury, the pre-exponential factor is multiplied by 7.5006, yielding e_s(t) = 4.581 exp[17.27 t / (t + 237.3)] mmHg. For reference-grade metrology, the World Meteorological Organization recommends the more complex Goff-Gratch equation (1946), which integrates the Clausius-Clapeyron equation while accounting for the temperature dependence of the latent heat of vaporization ΔH_vap(T) and the non-ideality of moist air through virial compressibility factors: log₁₀(e_s / e_st) = −7.90298 (T_st/T − 1) + 5.02808 log₁₀(T_st/T) − 1.3816 × 10⁻⁷ [10^(11.344 (1 − T/T_st)) − 1] + 8.1328 × 10⁻³ [10^(−3.49149 (T_st/T − 1)) − 1], where T_st = 373.16 K is the steam point and e_st = 1013.25 hPa. Over the 10 °C to 30 °C temperature domain investigated in standard educational laboratories, the Tetens equation agrees with the rigorous Goff-Gratch standard to within less than 0.05%, providing an outstanding analytical tool for laboratory psychrometric computations.',
            'formula': 'e_s(t) = 0.61078 \\exp\\left(\\frac{17.27 t}{t + 237.3}\\right)\\text{ kPa} = 4.581 \\exp\\left(\\frac{17.27 t}{t + 237.3}\\right)\\text{ mmHg}',
            'question': 'What is the saturation vapor pressure of pure water at the standard dry-bulb temperature of 25.0 °C?',
            'answer': 'Using the Tetens equation at t = 25.0 °C: e_s(25) = 0.61078 exp[(17.27 × 25) / (25 + 237.3)] = 0.61078 exp(1.6460) = 3.168 kPa (which equals 23.76 mmHg).'
        },
        {
            'title': 'Molecular Density of Moist Air: Avogadro’s Law and Buoyancy',
            'text': 'A common intuitive misconception is that humid air is denser (heavier) than dry air. In reality, Dalton’s law of partial pressures and Avogadro’s hypothesis dictate that moist air is strictly lighter (less dense) than dry air at the identical temperature and barometric pressure. Dry air is a mixture primarily composed of diatomic nitrogen (N₂, molecular weight M_N2 = 28.013 g mol⁻¹) and diatomic oxygen (O₂, molecular weight M_O2 = 31.999 g mol⁻¹), yielding an effective mean molecular weight of M_dry ≈ 28.964 g mol⁻¹. In contrast, a water molecule (H₂O) consists of two hydrogen atoms and one oxygen atom, giving a molecular weight of only M_H2O = 18.015 g mol⁻¹. According to Avogadro’s law, equal volumes of all gases at identical temperature and pressure contain an equal number of moles (and molecules). When water vapor evaporates into dry air at constant total pressure P_atm, water molecules do not simply squeeze in between air molecules; instead, by Dalton’s law of partial pressures P_atm = P_dry + e, each water molecule displaces an average dry air molecule of significantly greater mass (18 g mol⁻¹ replaces 29 g mol⁻¹). The density of moist air ρ_moist is calculated from the ideal gas equation of state: ρ_moist = (P_dry M_dry + e M_H2O) / (R_univ T) = [P_atm M_dry − e (M_dry − M_H2O)] / (R_univ T) = ρ_dry [1 − 0.378 (e / P_atm)]. Because M_dry > M_H2O, the bracketed term is strictly less than unity, proving that increasing the water vapor pressure e diminishes the overall density of the air parcel. This lower density of warm, humid air provides the buoyancy that drives atmospheric thermal updrafts, cumulus cloud development, and thunderstorm convective towers.',
            'formula': '\\rho_{\\text{moist}} = \\frac{P_{\\text{atm}} M_{\\text{dry}} - e (M_{\\text{dry}} - M_{\\text{H}_2\\text{O}})}{R T} = \\rho_{\\text{dry}} \\left(1 - 0.378 \\frac{e}{P_{\\text{atm}}}\\right) < \\rho_{\\text{dry}}',
            'question': 'Which is heavier: a cubic meter of dry air or a cubic meter of moist air at the same temperature and pressure?',
            'answer': 'Dry air is heavier (denser). By Avogadro’s law, a cubic meter contains the same total number of gas molecules. In moist air, lighter water molecules (M = 18 g/mol) displace heavier nitrogen (M = 28 g/mol) and oxygen (M = 32 g/mol) molecules, reducing the total mass per unit volume.'
        },
        {
            'title': 'Biophysical Psychrometry: Evaporative Cooling and the Heat Index',
            'text': 'The thermodynamic principles governing the wet-bulb psychrometer are identical to the biophysical mechanisms regulating human thermoregulation. The human body maintains a homeostatic core temperature near 37.0 °C. Metabolic heat generated by cellular respiration is dissipated to the environment via radiation, convection, and cutaneous perspiration (sweating). When the ambient dry-bulb temperature t_d approaches or exceeds skin temperature (~33–35 °C), sensible heat loss by radiation and convection ceases, and evaporative cooling becomes the sole physical pathway for dissipating excess body heat. The skin functions as a biological wet bulb: sweat glands secrete an aqueous saline film that evaporates into ambient air, absorbing the latent heat of vaporization (L_v ≈ 2430 J g⁻¹ of sweat). However, the rate of sweat evaporation is governed by the psychrometric driving force: dQ_evap/dt ∝ [e_s(t_skin) − e]. If the ambient relative humidity is low (large wet-bulb depression Δt), e is small, sweat evaporates rapidly, and effective cooling occurs. Conversely, if ambient humidity is high (small wet-bulb depression Δt), e approaches e_s, evaporation is suppressed, sweat accumulates as liquid dripping without phase transition, and the body cannot dissipate metabolic heat. The wet-bulb temperature t_w represents the absolute theoretical lower limit to which any sweating surface can be cooled by evaporation. In environmental physiology, a sustained outdoor wet-bulb temperature exceeding t_w = 35.0 °C (the physiological survivability threshold) is fatal to humans and mammals within hours even in shaded, well-ventilated environments, because skin temperature cannot drop below 35 °C, leading inevitably to hyperthermia and fatal heat stroke. The National Weather Service Heat Index and Wet-Bulb Globe Temperature (WBGT) directly quantify these biophysical psychrometric limits.',
            'formula': '\\frac{dQ_{\\text{perspiration}}}{dt} = k_{\\text{skin}} A_{\\text{body}} [e_s(t_{\\text{skin}}) - e] \\implies \\lim_{e \\to e_s(t_d)} \\frac{dQ_{\\text{perspiration}}}{dt} = 0',
            'question': 'Why is a hot, humid day (e.g., 35 °C, 80% RH) vastly more dangerous to human health than a hot, dry day (e.g., 40 °C, 15% RH)?',
            'answer': 'High ambient humidity elevates the vapor pressure e, sharply reducing the gradient [e_s(t_skin) − e] that drives sweat evaporation. Without evaporation, the body cannot shed metabolic heat. On a dry day, the large psychrometric depression permits rapid, efficient sweat evaporation, maintaining skin cooling.'
        },
        {
            'title': 'Error Analysis and Linear Regression for the Psychrometric Constant',
            'text': 'To extract the psychrometric constant A with rigorous statistical uncertainty from paired observations, the Ferrel-Sprung relation is cast in linear form: y_i = m x_i + b, where the independent variable is the wet-bulb depression x_i = Δt_i = (t_d − t_w)_i (in kelvins or degrees Celsius) and the dependent variable is the vapor pressure depression y_i = Δe_i = e_s(t_w)_i − e_i (in Pascals). The ordinary least-squares regression line has slope m = γ = A · P_atm and vertical intercept b ≈ 0. The slope is evaluated from m = Σ(x_i − x̄)(y_i − ȳ) / Σ(x_i − x̄)². The experimental psychrometric constant is then computed as A = m / P_atm. Because the barometric pressure P_atm is measured independently with high precision using a Fortin mercurial barometer (uncertainty u(P_atm) / P_atm < 0.05%), the standard error in the psychrometric constant is dominated by the regression slope standard error: s_A = s_m / P_atm = √[s² / Σ(x_i − x̄)²] / P_atm, where s² = Σ(y_i − m x_i − b)² / (n − 2) is the residual variance for n = 5 observations. A key source of systematic experimental uncertainty is the airflow velocity across the wet bulb: if the aspiration velocity falls below 2.5 m s⁻¹, convective heat transfer h_c decreases and radiative heat exchange from surrounding objects becomes non-negligible, causing the apparent slope m to rise and overestimating A by up to 20%. Other significant uncertainties include: (1) wick contamination with dissolved salts or organic oils (which depresses e_s(t_w) by Raoult’s law); (2) visual detection latency in identifying the microscopic dew film on the polished mirror (which introduces a ±0.2 °C uncertainty in t_dew); and (3) emergent stem cooling of mercury columns. The high correlation coefficient (R² = 1.0000) obtained across the five test stations demonstrates the high metrological precision of the dual psychrometric and dew-point method.',
            'formula': 'y = \\Delta e = e_s(t_w) - e, \\quad x = \\Delta t, \\quad m = \\gamma = A \\cdot P_{\\text{atm}} \\implies A = \\frac{m}{P_{\\text{atm}}}, \\quad s_A = \\frac{s_m}{P_{\\text{atm}}}',
            'question': 'How does linear regression of vapor pressure depression Δe against wet-bulb depression Δt allow determination of the psychrometric constant A?',
            'answer': 'According to the Ferrel-Sprung equation, Δe = (A · P_atm) · Δt. Plotting Δe versus Δt yields a straight line with slope m = A · P_atm. Dividing the fitted slope by the measured barometric pressure P_atm yields the psychrometric constant: A = m / P_atm.'
        }
    ],
    'quiz': [
        {
            'question': 'In the Ferrel-Sprung psychrometric equation e = e_s(t_w) − A · P_atm · (t_d − t_w), what does the slope m of a plot of vapor pressure depression Δe versus wet-bulb depression Δt represent?',
            'options': [
                'The slope m represents the psychrometric slope γ = A · P_atm, from which A = m / P_atm.',
                'The slope m is directly equal to the relative humidity of the room: m = RH.',
                'The slope m represents the latent heat of vaporization of water: m = L_v.',
                'The slope m equals the saturation vapor pressure at room temperature: m = e_s(t_d).'
            ],
            'correct': 0,
            'explanation': 'In the linear relation Δe = e_s(t_w) − e = (A · P_atm) Δt, the slope is m = γ = A · P_atm. Dividing the slope by barometric pressure P_atm gives the psychrometric constant A.'
        },
        {
            'question': 'How is actual atmospheric water vapor pressure e directly determined using a polished-mirror dew-point hygrometer?',
            'options': [
                'By finding the saturation vapor pressure at the measured dew-point temperature: e = e_s(t_dew).',
                'By measuring the electrical resistance of the silver mirror when wet.',
                'By weighing the water droplets that condense onto the mirror surface.',
                'By multiplying the dry-bulb temperature by the barometric pressure.'
            ],
            'correct': 0,
            'explanation': 'At the dew point, ambient air becomes 100% saturated with water vapor without changing its moisture content, meaning the actual vapor pressure e is identically equal to the saturation vapor pressure at that temperature: e = e_s(t_dew).'
        },
        {
            'question': 'Why is moist air less dense than dry air at the same temperature and barometric pressure?',
            'options': [
                'Because water molecules (M = 18 g/mol) displace heavier nitrogen (M = 28 g/mol) and oxygen (M = 32 g/mol) molecules in an equal volume of gas.',
                'Because water vapor molecules repel air molecules, forcing them further apart.',
                'Because water vapor has a lower temperature than surrounding air.',
                'Because moist air expands due to surface tension.'
            ],
            'correct': 0,
            'explanation': 'By Avogadro’s law, equal volumes contain equal numbers of gas molecules. In moist air, lighter water vapor molecules (molecular weight 18) replace heavier diatomic nitrogen (28) and oxygen (32) molecules, lowering the overall mixture density.'
        },
        {
            'question': 'Why must the airflow across the wet bulb of a psychrometer be maintained at a velocity of at least 2.5 to 3.0 m/s?',
            'options': [
                'To ensure that convective heat and mass transfer dominate over radiative exchange, making the psychrometric constant A stable and reproducible.',
                'To prevent the water on the wick from freezing into ice.',
                'To blow away dust particles from the thermometer graduations.',
                'To increase the barometric pressure inside the protective radiation shield.'
            ],
            'correct': 0,
            'explanation': 'At forced aspiration velocities ≥ 2.5 m/s, convective heat transfer becomes so large that thermal radiation from room walls accounts for less than 1% of the heat exchange, stabilizing the psychrometric constant at its standard value A ≈ 6.60 × 10⁻⁴ K⁻¹.'
        }
    ],
    'precautions': [
        'Always use pure distilled or deionized water on the wet-bulb muslin sleeve; tap water leaves mineral deposits that depress the saturation vapor pressure.',
        'Ensure the aspiration fan operates continuously at ≥ 3.0 m/s during psychrometric readings to maintain a standardized convective boundary layer.',
        'Carefully average the temperatures of appearance and disappearance of the dew film on the polished mirror to cancel thermal conduction gradients through the metal cup.',
        'Avoid breathing toward the psychrometer or dew cup during observations, as exhaled moisture and carbon dioxide will alter local humidity and temperature.'
    ],
    'limitations': 'The teaching model assumes a constant psychrometric factor A = 6.60 × 10⁻⁴ K⁻¹ corresponding to ideal forced ventilation and pure water. In an unventilated room or with a contaminated wick, A can increase to ~8.0 × 10⁻⁴ K⁻¹, and non-ideal gas compressibility factors become slightly noticeable at high ambient temperatures.',
    'modelExtra': 'The Ferrel-Sprung psychrometric equation and the dew-point method illustrate the fundamental thermodynamic balance between sensible convective heat transfer and latent mass transfer. The experimental psychrometric constant A = 6.60 × 10⁻⁴ K⁻¹ bridges microscopic molecular diffusion with macroscopic meteorological observations of humidity and weather.'
}

# Update content/physics/experiments.json
exp_path = ROOT / 'content/physics/experiments.json'
experiments = json.loads(exp_path.read_text())

existing_idx = next((i for i, x in enumerate(experiments) if x['slug'] == 'air-humidity'), None)
if existing_idx is not None:
    experiments[existing_idx] = exp35
    print(f"Updated existing Lab 35 in experiments.json at index {existing_idx}")
else:
    experiments.append(exp35)
    print(f"Appended Lab 35 to experiments.json (Total: {len(experiments)})")

exp_path.write_text(json.dumps(experiments, indent=2, ensure_ascii=False))

# Update catalog.sqlite3
db_path = ROOT / 'data/catalog.sqlite3'
db = sqlite3.connect(db_path)
sid = db.execute("SELECT id FROM subjects WHERE slug='physics'").fetchone()[0]

home = f"/physics/{exp35['slug']}/"
db.execute('''
    INSERT INTO experiments(subject_id, slug, title, status, page_path, theory_path, report_path)
    VALUES(?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(slug) DO UPDATE SET
        title=excluded.title,
        status=excluded.status,
        page_path=excluded.page_path,
        theory_path=excluded.theory_path,
        report_path=excluded.report_path
''', (sid, exp35['slug'], exp35['shortTitle'], 'live', home, home + 'theory/', home + 'report/'))

db.commit()
db.close()
print("Lab 35 successfully registered in catalog.sqlite3!")
