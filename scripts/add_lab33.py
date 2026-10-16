import json, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

exp33 = {
    'number': 33,
    'slug': 'charles-law-pressure',
    'title': 'Determination of the Thermal Pressure Coefficient of a Gas at Constant Volume (Charles’ Law)',
    'shortTitle': 'Pressure Coefficient of a Gas',
    'aim': 'Determine the thermal pressure coefficient of dry air at constant volume (α_v) across temperatures from 0.0 °C to 80.0 °C using a constant-volume air thermometer (Jolly bulb) with a mercury manometer, verify the linear pressure-temperature relation P = P_0(1 + α_v t), and extrapolate to calculate the absolute zero of temperature.',
    'target': 'α_v',
    'targetName': 'Thermal pressure coefficient α_v',
    'inputLabel': 'Bath temperature t',
    'shortInput': 'Temperature t',
    'inputUnit': '°C',
    'inputDecimals': 1,
    'rawLabel': 'Absolute pressure P',
    'rawUnit': 'kPa',
    'rawDecimals': 2,
    'xAxis': 'Temperature t (°C)',
    'yAxis': 'Absolute pressure P (kPa)',
    'xScale': 1.0,
    'yScale': 0.001,
    'gradientUnit': 'Pa K⁻¹',
    'resultUnit': 'K⁻¹',
    'resultScale': 1.0,
    'resultDecimals': 6,
    'min': 0.0,
    'max': 80.0,
    'step': 5.0,
    'initial': 0.0,
    'samples': [0.0, 20.0, 40.0, 60.0, 80.0],
    'emptyX': [-20.0, 100.0],
    'emptyY': [90.0, 150.0],
    'timed': False,
    'angle': False,
    'published': True,
    'measureLabel': 'Align Meniscus to Fiducial Pointer & Measure Pressure P (kPa)',
    'fitEquation': 'P_t = P_0 (1 + α_v t) = P_0 + (P_0 α_v) · t ⇔ Y = m X + b ⇔ α_v = m / P_0 = m / b',
    'intro': "Charles' law at constant volume—frequently designated Gay-Lussac's law of pressure or Amontons' law of pressure-temperature dependence—is a cornerstone principle of classical thermodynamics and kinetic gas theory. It asserts that for a fixed mass of an ideal gas maintained at constant volume, the absolute pressure exerted by the gas against the boundaries of its containment vessel increases linearly with thermodynamic temperature. Preliminary investigations into the pressure of heated air were conducted as early as 1699 and 1702 by the French mechanical philosopher Guillaume Amontons, who designed a constant-volume air thermometer and posited that the pressure of air would diminish to zero at an extreme minimum temperature, providing the first historical inkling of an absolute zero. Exactly one century later, between 1802 and 1808, Joseph Louis Gay-Lussac and John Dalton conducted comprehensive quantitative experiments demonstrating that all permanent gases, when confined to an unvarying geometric volume, exhibit a uniform relative rate of pressure increase per unit temperature rise. The mathematical formulation of this isochoric relationship, referenced to the ice point at 0.00 °C, is P_t = P_0 (1 + α_v t), where P_0 represents the absolute gas pressure at 0.00 °C, t is the Celsius temperature, and α_v is the thermal pressure coefficient of the gas at constant volume (often called the isochoric pressure-temperature coefficient). For an ideal gas adhering to the equation of state PV = nRT, the pressure coefficient α_v is numerically identical to the isobaric volume expansion coefficient β, both being precisely equal to the reciprocal of the absolute temperature of the ice point: α_v = β = 1 / T_0 = 1 / 273.15 K⁻¹ ≈ 0.003661 K⁻¹. In the classical precision laboratory, this relationship is investigated using a constant-volume air thermometer, historically perfected by the German physicist Philipp von Jolly in 1874 (the Jolly bulb air thermometer). The apparatus consists of a rigid spherical glass bulb containing dry air, immersed completely in a thermostatically regulated, stirred liquid bath. The bulb neck is fused to a narrow capillary stem leading to a closed vertical manometer tube featuring a sharp, downward-pointing glass or ivory fiducial index tip (the index pointer). This closed limb is connected via thick flexible rubber tubing to an open, vertically movable manometer tube (the leveling reservoir). At every operating temperature, thermal expansion would tend to push the mercury column downward away from the pointer; however, the experimenter restores the gas to its exact original reference volume by raising the open leveling tube until the summit of the mercury meniscus in the closed capillary just touches the tip of the fiducial index pointer. Once this constant-volume condition is established, the absolute internal pressure of the confined air is determined directly by summing the local barometric atmospheric pressure B with the difference in mercury column elevations: P = B + Δh = B + (h_open − h_closed). Plotting the resulting absolute pressure P against Celsius temperature t yields a linear curve whose slope m = P_0 α_v and vertical intercept b = P_0 provide a direct determination of the pressure coefficient α_v = m / P_0. Furthermore, extrapolating this regression line to the point where absolute pressure theoretically vanishes (P → 0) determines the absolute zero of temperature: T_0 = −b / m = −1 / α_v ≈ −273.15 °C. This elegant measurement confirms that the gas thermometer is not merely an empirical sensor, but a thermodynamic instrument that defines the fundamental absolute temperature scale.",
    'settings': [
        'Confined dry atmospheric air mass held at constant volume V = 100.00 cm³ via fiducial pointer index alignment.',
        'Ambient atmospheric barometric pressure P_0 = B = 760.0 mmHg = 101.325 kPa verified by precision Fortin laboratory barometer.',
        'Borosilicate glass bulb envelope with linear thermal expansion coefficient α_g = 3.3 × 10⁻⁶ K⁻¹ (cubical expansion γ = 9.9 × 10⁻⁶ K⁻¹).',
        'Triple-distilled liquid mercury manometer fluid (density ρ_Hg = 13,595 kg m⁻³ at 0 °C, local gravitational acceleration g = 9.80665 m s⁻²).',
        'Theoretical reference thermal pressure coefficient for an ideal gas: α_v_ref = 1 / 273.15 K⁻¹ = 0.00366099 K⁻¹ (3.6610 × 10⁻³ K⁻¹).'
    ],
    'apparatus': [
        {
            'name': 'Constant-Volume Air Thermometer (Jolly Bulb Apparatus)',
            'purpose': 'A rigid spherical borosilicate glass bulb of nominal capacity 100.00 cm³ terminating in a narrow capillary stem, enclosing a fixed dry air charge and designed for total immersion in the variable-temperature bath.'
        },
        {
            'name': 'Precision Vertical Mercury Manometer with Fiducial Index Pointer',
            'purpose': 'Two parallel glass manometer tubes: a closed limb containing a sharp downward-pointing glass fiducial index tip defining the fixed reference volume, and an open limb connected via flexible tubing to register gauge pressure Δh.'
        },
        {
            'name': 'Adjustable Vertical Rack-and-Pinion Leveling Reservoir Mount',
            'purpose': 'Provides fine vertical translation of the open manometer tube across a 600 mm range, allowing the operator to adjust the mercury column height precisely until the closed-tube meniscus touches the index pointer.'
        },
        {
            'name': 'Thermostatically Controlled Stirred Heating Bath with Mechanical Agitator',
            'purpose': 'A transparent cylindrical jacket surrounding the bulb, equipped with an electric heating element and a motorized propeller stirrer to ensure homogeneous temperature distribution throughout the liquid volume without spatial gradients.'
        },
        {
            'name': 'Precision Laboratory Thermometer (0.0 °C to 100.0 °C, 0.1 °C Divisions)',
            'purpose': 'Calibrated mercury-in-glass secondary standard thermometer suspended directly adjacent to the Jolly bulb to register the bath thermal equilibrium temperature to ±0.05 °C.'
        },
        {
            'name': 'Fortin Mercurial Precision Laboratory Barometer',
            'purpose': 'Measures the prevailing ambient atmospheric pressure B in millimeters of mercury (mmHg) and kilopascals (kPa), essential for converting measured manometer gauge pressure Δh into absolute gas pressure P = B + Δh.'
        }
    ],
    'procedure': [
        {
            'title': 'Atmospheric Barometric Pressure Determination & Initial Zeroing',
            'text': 'Read the laboratory Fortin mercurial barometer to 0.1 mmHg, applying brass scale and temperature reductions to determine the true ambient atmospheric pressure B (nominal baseline B = 760.0 mmHg = 101.325 kPa). Inspect the Jolly bulb capillary and manometer tubes to verify that the mercury surfaces are clean, free of oxidation films, and that no air bubbles reside in the flexible connecting hose.',
            'why': 'Because the open limb of the manometer is exposed to the room, the absolute pressure of the confined gas is the sum of atmospheric pressure and the differential mercury head (P = B + Δh). An accurate barometric reading is essential for absolute pressure calculations.'
        },
        {
            'title': 'Ice-Point Calibration & Constant-Volume Index Alignment at 0.0 °C',
            'text': 'Fill the bath vessel surrounding the Jolly bulb with finely crushed pure melting ice and distilled water. Agitate the slurry thoroughly for at least five minutes until the immersion thermometer stabilizes at 0.00 °C. Adjust the movable open manometer tube until the apex of the convex mercury meniscus in the closed capillary just touches the sharp tip of the fiducial index pointer. Sighting with an optical magnifier, confirm zero differential head between the two tubes (Δh = 0) at 0 °C, establishing the baseline absolute pressure P_0 = 101.325 kPa.',
            'why': 'Bringing the mercury meniscus precisely to the fiducial pointer fixes the enclosed gas volume to the invariant reference value V_0, while the ice bath provides the fundamental thermodynamic reference baseline for computing the thermal pressure coefficient α_v.'
        },
        {
            'title': 'Progressive Stepwise Heating & Active Bath Agitation',
            'text': 'Drain the ice water and fill the jacket with tap water. Energize the electric heater to raise the bath temperature progressively in 20.0 °C increments (20.0 °C, 40.0 °C, 60.0 °C, 80.0 °C). Run the motorized stirrer continuously at moderate speed to circulate the water around the spherical bulb and prevent thermal stratification.',
            'why': 'Continuous mechanical agitation prevents convective hot spots from developing near the heating element, ensuring that the enclosed air reaches the exact temperature registered by the immersion thermometer.'
        },
        {
            'title': 'Manometer Elevation & Exact Pointer Re-alignment',
            'text': 'As the gas temperature rises, the increased internal thermal pressure tends to depress the mercury in the closed capillary. Use the fine rack-and-pinion control to raise the open leveling tube until the mercury meniscus in the closed limb is restored exactly to touch the fiducial index pointer tip. Confirm that no gap and no meniscus deformation exists at the contact point.',
            'why': 'This restoration step enforces the fundamental condition of Charles’ law: the gas volume is held strictly constant (dV = 0) so that the entire thermal energy input manifests solely as an increase in thermodynamic pressure.'
        },
        {
            'title': 'Paired Acquisition of Temperature and Differential Mercury Height',
            'text': 'Once thermal equilibrium is established (constant temperature for at least 3 minutes), record the bath temperature t to the nearest 0.1 °C. Read the heights of the mercury columns in the closed tube (h_closed) and open tube (h_open) on the mirror-backed millimeter scale. Calculate the gauge head Δh = h_open − h_closed and compute the absolute pressure P = B + Δh in kilopascals (kPa).',
            'why': 'Mirror-backed scale readings eliminate optical parallax error. Recording paired values of t and P under verified thermal equilibrium ensures high fidelity in the subsequent linear regression analysis.'
        },
        {
            'title': 'Descending Temperature Verification & Absolute Zero Extrapolation',
            'text': 'De-energize the heater and allow the bath to cool slowly, recording repeat pressure readings at the same temperature stations with falling temperatures to check for thermal hysteresis or gas leakage. Plot the equilibrium absolute pressure P against Celsius temperature t, compute the best-fit slope m and intercept b, and extrapolate the line to P = 0 to calculate the absolute zero of temperature T_0 = −b / m.',
            'why': 'Verifying identical readings during cooling confirms that no gas leaked past the mercury seal and that the glass bulb underwent elastic, reversible thermal cycling.'
        }
    ],
    'topics': [
        {
            'title': 'Kinetic Theory of Gases and the Origin of Thermal Gas Pressure',
            'text': 'According to the classical kinetic theory of gases formulated by Clausius, Maxwell, and Boltzmann, a macroscopic gas consists of an enormous ensemble of point-like molecules of mass m moving with randomly oriented velocities in continuous chaotic motion. The absolute pressure P exerted by the gas against the interior walls of its container represents the macroscopic time-averaged rate of normal momentum transfer imparted by molecular collisions per unit surface area: P = (1/3) n m <v²> = (2/3) n <E_k>, where n = N/V is the molecular number density and <E_k> = (1/2) m <v²> is the mean translational kinetic energy of a molecule. In classical statistical thermodynamics, temperature is fundamentally defined through the equipartition theorem as a measure of this average translational kinetic energy: <E_k> = (3/2) k_B T, where k_B = 1.380649 × 10⁻²³ J K⁻¹ is the Boltzmann constant and T is the absolute thermodynamic temperature in kelvins. Substituting this kinetic definition into the pressure equation yields P = n k_B T = (N/V) k_B T, which is the microscopic statement of the ideal gas law. When the gas is confined to a rigid container of invariant volume (V = constant), the number density n remains strictly fixed. Consequently, raising the temperature T increases the root-mean-square molecular velocity according to v_rms = √(3 k_B T / m). This elevated velocity has a twofold effect on wall collisions: first, each individual collision transfers greater momentum (Δp = 2 m v_x); second, the frequency of collisions per second against each unit area of the wall increases proportionally to v_rms. Because both the momentum transfer per impact and the impact frequency scale with molecular speed, the macroscopic pressure scales directly with <v²> and therefore directly with absolute temperature T. This kinetic derivation provides the theoretical foundation for Charles’ law at constant volume: pressure is directly proportional to thermodynamic temperature because temperature is the direct macroscopic reflection of molecular kinetic energy.',
            'formula': 'P = \\frac{1}{3} n m \\langle v^2 \\rangle = \\frac{2}{3} n \\langle E_k \\rangle = n k_B T = \\frac{N k_B T}{V} \\implies \\left(\\frac{\\partial P}{\\partial T}\\right)_V = \\frac{N k_B}{V} = \\text{constant}',
            'question': 'How does the microscopic kinetic theory explain why gas pressure increases when a sealed rigid bulb is heated?',
            'answer': 'Heating the gas increases the mean translational kinetic energy of the molecules (<E_k> = (3/2) k_B T), which raises their average speed. Because the volume is constant, faster molecules collide with the container walls more frequently and deliver greater momentum per collision, resulting in a higher time-averaged normal force per unit area, which macroscopically constitutes increased pressure.'
        },
        {
            'title': 'Charles’ Law at Constant Volume and Gay-Lussac’s Isochoric Relation',
            'text': 'Charles’ law at constant volume (often historically designated Gay-Lussac’s second law or Amontons’ law) states that for an ideal gas held at constant volume, the pressure P varies linearly with temperature. When referenced to the Celsius temperature scale where 0 °C corresponds to the freezing point of water, the mathematical relationship is written as P_t = P_0 (1 + α_v t), where P_0 is the absolute pressure at 0.00 °C, t is the Celsius temperature, and α_v is the thermal pressure coefficient at constant volume. The coefficient α_v is formally defined as the fractional rate of pressure increase per degree Celsius relative to the ice-point pressure: α_v = (1 / P_0) (dP / dt)_V. For an ideal gas adhering to the equation of state PV = nRT, taking the partial derivative of pressure with respect to Celsius temperature t (where T = t + T_0 and T_0 is the absolute temperature of the ice point) yields (dP / dt)_V = nR / V. At t = 0 °C, the ice-point pressure is P_0 = nR T_0 / V. Dividing the derivative by P_0 gives α_v = (nR / V) / (nR T_0 / V) = 1 / T_0. Because the ice point on the thermodynamic Kelvin scale is defined as T_0 = 273.15 K, the theoretical thermal pressure coefficient for an ideal gas is α_v = 1 / 273.15 K⁻¹ ≈ 0.00366099 K⁻¹ (or approximately 3.661 × 10⁻³ K⁻¹). Remarkably, this pressure coefficient α_v is identically equal to the thermal volume expansion coefficient β obtained under isobaric conditions (β = (1 / V_0) (dV / dt)_P = 1 / T_0). The identity α_v = β holds strictly for any substance that obeys the ideal gas equation of state, reflecting the underlying symmetry of the thermodynamic surface P(V, T). In an experimental plot of P against t, the data form a straight line with slope m = P_0 α_v and vertical intercept b = P_0. From these two regression parameters, the experimental pressure coefficient is computed directly as α_v = m / b, completely independent of any external temperature calibration beyond the Celsius scale definition.',
            'formula': 'P_t = P_0 (1 + \\alpha_v t) \\iff \\alpha_v = \\frac{1}{P_0} \\left(\\frac{\\partial P}{\\partial t}\\right)_V = \\frac{m}{b} = \\frac{1}{T_0} \\approx \\frac{1}{273.15\\text{ K}} \\approx 0.003661\\text{ K}^{-1}',
            'question': 'Why is the thermal pressure coefficient α_v at constant volume numerically equal to the thermal volume expansion coefficient β at constant pressure for an ideal gas?',
            'answer': 'Both coefficients represent the reciprocal of the absolute ice-point temperature (1 / T_0 = 1 / 273.15 K). From the ideal gas law PV = nRT, (∂P/∂T)_V = nR/V and P_0 = nRT_0/V, so α_v = 1/T_0. Similarly, (∂V/∂T)_P = nR/P and V_0 = nRT_0/P, giving β = 1/T_0. Therefore, α_v = β = 1/T_0.'
        },
        {
            'title': 'The Jolly Constant-Volume Air Thermometer: Design and Manometry',
            'text': 'The constant-volume air thermometer, perfected by Philipp von Jolly in 1874, remains the premier primary instrument for thermometric metrology across the cryogenic and moderate temperature domains. The core apparatus comprises a spherical borosilicate glass bulb (capacity ~100 cm³) submerged in a stirred heating bath and fused to an unheated glass capillary tube of narrow capillary bore (diameter ~0.5 mm). The capillary bends vertically downward into a closed manometer tube that terminates in a pointed glass or ivory index pin (the fiducial pointer). This closed limb is joined via heavy-duty vulcanized rubber or flexible fluoropolymer tubing to an open manometer limb mounted on a vertical sliding carriage controlled by a rack-and-pinion screw drive. Liquid mercury fills the flexible tube and both manometer limbs. When the air inside the bulb is heated, its expansion tends to push the mercury column downward. To maintain a strictly constant volume, the experimenter raises the open limb until the apex of the convex mercury meniscus in the closed capillary exactly touches the sharp tip of the fiducial index pin. Because the volume enclosed between the bulb and the pointer tip is geometrically invariant, the condition of constant volume is rigorously fulfilled. The total absolute pressure P of the enclosed gas is then obtained from the fundamental hydrostatic balance equation: P = B + ρ_Hg g (h_open − h_closed) = B + Δh, where B is the prevailing barometric pressure of the surrounding atmosphere and Δh = h_open − h_closed is the vertical height difference between the mercury menisci in the open and closed tubes. If the open tube meniscus stands higher than the closed tube meniscus, Δh is positive (gauge overpressure); if lower (as occurs below 0 °C), Δh is negative. By referencing all readings to the sharp index pointer, the Jolly air thermometer eliminates errors associated with scale calibration variations along the closed tube and ensures that the volume of the gas remains constant within less than 0.01% across the entire experimental range.',
            'formula': 'P = B + \\rho_{\\text{Hg}} g (h_{\\text{open}} - h_{\\text{closed}}) = B + \\Delta h_{\\text{mmHg}} = B + \\frac{\\Delta h}{7.5006} \\text{ (in kPa)}',
            'question': 'Why is it critical to adjust the mercury meniscus to touch the fiducial pointer tip before taking every pressure reading?',
            'answer': 'The fiducial pointer defines the boundary of the constant volume V_0. If the meniscus were allowed to move away from the pointer, the gas volume would vary with temperature, violating the isochoric condition (V = const) and invalidating the simple linear relationship P = P_0(1 + α_v t).'
        },
        {
            'title': 'The Concept and Extrapolation of Absolute Zero of Temperature',
            'text': 'One of the most profound conceptual triumphs arising from the study of the gas laws is the discovery and thermodynamic definition of absolute zero. In the linear relationship P_t = P_0 (1 + α_v t), as temperature decreases below 0 °C, the pressure exerted by the gas progressively diminishes. Setting the absolute pressure to zero (P_t = 0) defines a theoretical lower limit of temperature below which the pressure would become unphysically negative: 0 = P_0 (1 + α_v T_0) ⟹ T_0 = −1 / α_v. Using the experimental value of the pressure coefficient α_v ≈ 0.003661 K⁻¹, the extrapolated temperature where gas pressure vanishes is T_0 = −1 / 0.003661 °C ≈ −273.15 °C. Lord Kelvin (William Thomson) recognized in 1848 that this zero-pressure intercept is not an accidental property of dry air, but a universal thermodynamic property common to all dilute gases. Kelvin utilized Carnot’s reversible heat engine cycle to establish the absolute thermodynamic temperature scale, defining the absolute Kelvin temperature T by the linear transformation T = t + 273.15. In terms of absolute temperature, Charles’ law at constant volume simplifies to the direct proportionality P = (P_0 / T_0) T = C T, or P_1 / T_1 = P_2 / T_2. Microscopic quantum mechanics reveals that even at absolute zero, molecules do not come to a complete halt; instead, they retain irreducible quantum zero-point vibrational energy E_0 = (1/2) ħ ω. However, at absolute zero, all thermal kinetic excitations cease, the entropy of a pure crystalline substance approaches zero in accordance with the Third Law of Thermodynamics (Nernst Heat Theorem), and a classical ideal gas would exert exactly zero pressure because it possesses zero thermal momentum to transfer to the containment walls. Extrapolating the linear regression line P(t) to its horizontal intercept where P = 0 provides a direct experimental determination of absolute zero on the Celsius scale: T_0 = −b / m.',
            'formula': 'P_t = 0 \\implies 1 + \\alpha_v T_0 = 0 \\implies T_0 = -\\frac{1}{\\alpha_v} = -\\frac{b}{m} \\approx -273.15\\,^\\circ\\text{C} \\implies T = t + 273.15\\text{ K}',
            'question': 'Does the extrapolation of Charles’ law to absolute zero imply that real gas molecules stop moving and have zero volume at −273.15 °C?',
            'answer': 'No. Real gases liquefy and solidify long before reaching absolute zero (e.g., air liquefies near −194 °C). Furthermore, quantum mechanics dictates that atoms retain non-zero quantum zero-point energy at 0 K. Absolute zero represents the state where all thermal kinetic energy is removed, not the annihilation of atomic volume or quantum motion.'
        },
        {
            'title': 'Systematic Corrections: Capillary Dead-Space and Bulb Thermal Dilatation',
            'text': 'In high-precision gas thermometry, two systematic physical phenomena cause the observed pressure-temperature slope to deviate slightly from the ideal behavior of a rigid vessel: the capillary dead-space effect and the cubical thermal expansion of the glass bulb envelope. First, the gas contained in the narrow capillary stem between the liquid bath surface and the index pointer does not reside at the bath temperature t, but at an intermediate room temperature t_r. Let V_0 be the bulb volume at bath temperature t and v be the unheated capillary dead-space volume at ambient room temperature t_r. The total number of gas moles is divided into two thermal zones: n = n_bulb + n_cap = (P V_0) / [R (T_0 + t)] + (P v) / [R (T_0 + t_r)]. Because the capillary gas is cooler than the bath, its density is higher, drawing a small fraction of the gas mass out of the hot bulb. The true corrected pressure P_corr that would be exerted if the entire volume V_0 + v were maintained at bath temperature t is given to first order by P_corr = P_obs [1 + (v / V_0) (t − t_r) / (T_0 + t_r)]. For a well-designed Jolly bulb where v / V_0 < 0.005, this dead-space correction increases the calculated pressure by approximately 0.2% to 0.5% at 80 °C. Second, glass is not a perfectly rigid material; upon heating from 0 °C to t, the borosilicate glass bulb expands cubically according to V_t = V_0 (1 + γ_g t), where γ_g = 3 α_g ≈ 9.9 × 10⁻⁶ K⁻¹ is the cubical thermal expansion coefficient of borosilicate glass. Because the containment volume actually increases slightly at elevated temperatures, the observed gas pressure is slightly lower than it would be in an ideally rigid vessel. Applying the bulb expansion correction gives P_corr = P_obs (1 + γ_g t). Combining both corrections yields the fully corrected thermal pressure coefficient: α_v_true = α_v_apparent + γ_g + (v / V_0) (1 / T_0) [1 − t_r / (T_0 + t_r)]. Neglecting glass expansion underestimates α_v by approximately 0.010 × 10⁻³ K⁻¹ (about 0.27%).',
            'formula': 'P_{\\text{corr}} = P_{\\text{obs}} \\left[1 + \\gamma_g t + \\frac{v}{V_0} \\left(\\frac{t - t_r}{T_0 + t_r}\\right)\\right] \\iff \\alpha_{v,\\text{true}} \\approx \\alpha_{v,\\text{obs}} + \\gamma_g',
            'question': 'How does the thermal expansion of the glass bulb affect the experimentally determined value of the gas pressure coefficient?',
            'answer': 'Because the glass bulb expands when heated, the gas occupies a slightly larger volume at higher temperatures than at 0 °C. This volume increase reduces the pressure buildup, causing the observed pressure P to be lower than in a truly rigid vessel. Consequently, the apparent slope m and apparent α_v are underestimated by an amount equal to the cubical expansion coefficient of glass (γ_g ≈ 10 × 10⁻⁶ K⁻¹).'
        },
        {
            'title': 'Virial Equation of State, Real Gas Departures, and the Ideal Gas Scale',
            'text': 'While Charles’ law assumes an ideal gas with non-interacting point particles, real gases such as atmospheric air (predominantly nitrogen and oxygen) deviate subtly from ideal behavior due to intermolecular forces and finite molecular excluded volume. In modern thermodynamics, real gas isotherms are described by the virial equation of state expanded in powers of molar density ρ = 1 / V_m: P V_m = R T [1 + B(T) ρ + C(T) ρ² + ...], where B(T) is the second virial coefficient representing pairwise molecular interactions and C(T) represents three-body interactions. At moderate pressures near 1 atmosphere (101.3 kPa), higher-order terms are negligible, and the equation of state reduces to P = (R T / V_m) [1 + B(T) / V_m]. Differentiating with respect to temperature at constant molar volume yields the isochoric pressure derivative: (dP / dt)_V = (R / V_m) [1 + (B(T) + T dB/dT) / V_m]. The experimental pressure coefficient for a real gas therefore depends slightly on density (and hence on the filling pressure P_0): α_v(P_0) = α_v_ideal + (P_0 / R) [dB/dT − B(T_0)/T_0]. For nitrogen and dry air at room temperature, the second virial coefficient B(T) is slightly negative (B ≈ −5 to −10 cm³ mol⁻¹) because attractive van der Waals dispersion forces dominate over repulsive hard-core exclusions. As temperature rises, thermal kinetic energy overcomes these intermolecular attractions, so dB/dT is positive. Consequently, the measured pressure coefficient α_v of dry air at 1 atmosphere (0.003673 K⁻¹) is slightly higher than the true thermodynamic ideal gas limit (0.003661 K⁻¹). To establish the absolute thermodynamic temperature scale independently of gas identity, metrologists measure α_v across several lower filling pressures P_0 (e.g., 0.75, 0.50, and 0.25 atm) and extrapolate linearly to zero initial pressure (P_0 → 0): lim_{P_0 → 0} α_v(P_0) = 1 / T_0 = 1 / 273.15 K⁻¹. This zero-pressure extrapolation defines the international gas thermometric temperature scale.',
            'formula': 'P V_m = R T \\left[1 + \\frac{B(T)}{V_m}\\right] \\implies \\alpha_v(P_0) = \\alpha_{v,\\text{ideal}} + P_0 \\cdot \\phi(T) \\implies \\lim_{P_0 \\to 0} \\alpha_v(P_0) = \\frac{1}{273.15\\text{ K}}',
            'question': 'Why is the pressure coefficient α_v of dry air at 1 atmosphere (~0.003673 K⁻¹) slightly larger than the ideal gas value (0.003661 K⁻¹)?',
            'answer': 'At atmospheric pressure and near 0 °C, attractive intermolecular van der Waals forces between air molecules slightly diminish the ice-point pressure P_0. As temperature rises, thermal kinetic motion weakens the relative effect of these attractive forces (dB/dT > 0), causing the pressure to increase slightly faster than in an ideal gas, making the ratio α_v = (dP/dt)/P_0 slightly greater.'
        },
        {
            'title': 'Atmospheric Barometric Reduction and Meniscus Capillary Depression',
            'text': 'The determination of absolute pressure from a liquid manometer requires careful metrological corrections for atmospheric barometric pressure and capillary surface tension. The absolute pressure of the gas is P = B + Δh. The barometric pressure B is read from a Fortin mercurial barometer whose raw mercury height H_bar must be corrected for: (1) thermal expansion of the mercury column and brass vernier scale, H_0 = H_bar [1 − (β_Hg − α_brass) t_room] / [1 + β_Hg t_room], where β_Hg = 1.818 × 10⁻⁴ K⁻¹ and α_brass = 1.84 × 10⁻⁵ K⁻¹; and (2) standard gravity reduction, B = H_0 (g_local / 9.80665 m s⁻²). Furthermore, liquid mercury does not wet glass (contact angle θ ≈ 130° to 140°), forming a convex curved meniscus that experiences capillary depression due to Laplace surface tension: ΔP_cap = (2 σ cos θ) / r, where σ = 0.485 N m⁻¹ is the surface tension of mercury and r is the internal tube radius. This downward capillary force depresses the mercury column by an amount h_cap = (2 σ cos θ) / (ρ_Hg g r). In a manometer where both the closed and open tubes have identical bore diameters (e.g., both 8.0 mm), the capillary depressions in both limbs are equal in magnitude and oppose each other, canceling out in the height difference Δh = h_open − h_closed. However, if the closed capillary tube is narrower than the open leveling reservoir tube (as is common in Jolly thermometers, where the capillary has a bore of 1.0 mm while the reservoir has a bore of 10.0 mm), the capillary depression in the narrow closed tube is significantly larger (~2.8 mm vs ~0.2 mm). This differential capillary depression artificially raises the measured open column height relative to the closed column, adding an apparent positive gauge pressure. Because the closed tube meniscus is always aligned to the identical index pointer at all temperatures, this capillary depression represents a constant additive offset that contributes solely to the vertical intercept b without altering the slope m = dP/dt. The thermal pressure coefficient α_v = m / P_0 remains robust against constant capillary offsets provided P_0 is evaluated from the true zero-degree reading.',
            'formula': 'B_{\\text{true}} = H_{\\text{bar}} \\left[1 - (\\beta_{\\text{Hg}} - \\alpha_{\\text{brass}}) t_{\\text{room}}\\right] \\frac{g_{\\text{local}}}{g_{\\text{std}}}, \\quad h_{\\text{cap}} = \\frac{2 \\sigma \\cos \\theta}{\\rho_{\\text{Hg}} g r}',
            'question': 'Why does capillary depression in an unequal-bore manometer not distort the slope of the pressure-temperature graph?',
            'answer': 'Because the meniscus in the narrow capillary is always brought to the identical vertical fiducial pointer at every temperature, the capillary depression force is constant across all trials. A constant offset shifts the vertical intercept b of the linear graph uniformly without altering the gradient m = dP/dt.'
        }
    ],
    'quiz': [
        {
            'question': 'In a constant-volume air thermometer (Jolly bulb), what is the primary physical function of the movable leveling reservoir?',
            'options': [
                'To adjust the mercury level in the closed tube until it touches the fiducial index pointer, thereby keeping the gas volume constant.',
                'To increase the total mass of air inside the spherical bulb as the temperature is raised.',
                'To regulate the water bath heating rate by adjusting hydrostatic back-pressure.',
                'To measure the volume of expanding gas directly in cubic centimeters.'
            ],
            'correct': 0,
            'explanation': 'The movable leveling tube is raised or lowered so that the mercury meniscus in the closed limb is restored exactly to the fiducial pointer tip at each temperature, guaranteeing that the volume of the gas remains strictly constant (V = V_0).'
        },
        {
            'question': 'How is the thermal pressure coefficient α_v calculated from the linear regression line P = m t + b of absolute pressure versus Celsius temperature?',
            'options': [
                'α_v is calculated as the ratio of the slope to the vertical intercept: α_v = m / b = m / P_0.',
                'α_v is calculated as the product of the slope and intercept: α_v = m · b.',
                'α_v is equal to the negative reciprocal of the slope: α_v = −1 / m.',
                'α_v is determined by dividing the intercept by the bath boiling point: α_v = b / 100.'
            ],
            'correct': 0,
            'explanation': 'In the equation P_t = P_0 (1 + α_v t) = P_0 + (P_0 α_v) t, the vertical intercept is b = P_0 and the slope is m = P_0 α_v. Therefore, α_v = m / P_0 = m / b.'
        },
        {
            'question': 'When the linear graph of absolute pressure P versus Celsius temperature t is extrapolated to the point of zero pressure (P = 0), what fundamental physical quantity is obtained?',
            'options': [
                'The absolute zero of temperature on the Celsius scale: T_0 = −b / m = −1 / α_v ≈ −273.15 °C.',
                'The critical temperature of water where liquid and vapor become indistinguishable.',
                'The boiling point of liquid nitrogen at standard atmospheric pressure.',
                'The room temperature at which the manometer was initially calibrated.'
            ],
            'correct': 0,
            'explanation': 'Setting P = 0 in P = m t + b yields t = −b / m = −1 / α_v ≈ −273.15 °C, which defines the absolute zero of thermodynamic temperature.'
        },
        {
            'question': 'Why does thermal expansion of the borosilicate glass bulb cause an apparent underestimation of the gas pressure coefficient α_v?',
            'options': [
                'Because the expanding glass increases the containment volume at higher temperatures, causing gas pressure to rise less than it would in an ideally rigid bulb.',
                'Because expanding glass absorbs gas molecules into its crystal lattice, reducing the number of moles.',
                'Because glass expansion increases the density of the mercury column in the manometer.',
                'Because the glass bulb becomes permeable to air at temperatures above 50 °C.'
            ],
            'correct': 0,
            'explanation': 'As the glass envelope expands (γ_glass ≈ 10 × 10⁻⁶ K⁻¹), the volume available to the gas increases slightly upon heating. This volumetric relaxation reduces the pressure buildup, yielding an apparent pressure coefficient that is lower than the true rigid-vessel value by an amount equal to γ_glass.'
        }
    ],
    'precautions': [
        'Always lower the movable leveling reservoir well down before heating or cooling the bath to prevent sudden thermal contractions from drawing mercury up into the capillary bulb.',
        'Ensure the water bath is agitated continuously with the mechanical stirrer for at least three minutes prior to reading, eliminating convective thermal gradients around the Jolly bulb.',
        'Use an optical magnifying lens and align your line of sight horizontally with the mirror backing on the millimeter scale to eliminate optical parallax when reading mercury levels.',
        'Confirm that the mercury meniscus touches the fiducial index pointer tip precisely—neither leaving a gap nor engulfing the tip—before recording the differential manometer height.'
    ],
    'limitations': 'The teaching model assumes dry air behaves as a classical ideal gas with negligible intermolecular van der Waals forces and zero dead-space volume in the capillary stem. In a physical laboratory, small corrections must be applied for capillary dead space (~0.6% unheated volume), cubical thermal expansion of the borosilicate glass envelope (γ ≈ 9.9 × 10⁻⁶ K⁻¹), and real-gas virial departures.',
    'modelExtra': 'The linear relationship P = P_0(1 + α_v t) directly bridges classical pneumatic manometry with Kelvin’s absolute thermodynamic temperature scale. The experimental pressure coefficient α_v = 1/273.15 K⁻¹ demonstrates that gas pressure approaches zero at −273.15 °C, establishing the physical foundation for the absolute scale of temperature where T = t + 273.15.'
}

# Update content/physics/experiments.json
exp_path = ROOT / 'content/physics/experiments.json'
experiments = json.loads(exp_path.read_text())

# Check if lab 33 already exists; update or append
existing_idx = next((i for i, x in enumerate(experiments) if x['slug'] == 'charles-law-pressure'), None)
if existing_idx is not None:
    experiments[existing_idx] = exp33
    print(f"Updated existing Lab 33 in experiments.json at index {existing_idx}")
else:
    experiments.append(exp33)
    print(f"Appended Lab 33 to experiments.json (Total: {len(experiments)})")

exp_path.write_text(json.dumps(experiments, indent=2, ensure_ascii=False))

# Update catalog.sqlite3
db_path = ROOT / 'data/catalog.sqlite3'
db = sqlite3.connect(db_path)
sid = db.execute("SELECT id FROM subjects WHERE slug='physics'").fetchone()[0]

home = f"/physics/{exp33['slug']}/"
db.execute('''
    INSERT INTO experiments(subject_id, slug, title, status, page_path, theory_path, report_path)
    VALUES(?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(slug) DO UPDATE SET
        title=excluded.title,
        status=excluded.status,
        page_path=excluded.page_path,
        theory_path=excluded.theory_path,
        report_path=excluded.report_path
''', (sid, exp33['slug'], exp33['shortTitle'], 'live', home, home + 'theory/', home + 'report/'))

db.commit()
db.close()
print("Lab 33 successfully registered in catalog.sqlite3!")
