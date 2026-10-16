import json, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

exp29 = {
    'number': 29,
    'slug': 'thermal-expansion',
    'title': 'Determination of the Coefficient of Linear Thermal Expansion of Copper by Steam Dilatometry',
    'shortTitle': 'Linear Thermal Expansion of Copper',
    'aim': 'Determine the coefficient of linear thermal expansion (α) of a solid copper specimen using a steam-jacketed dilatometer with precision micrometer screw gauge and electrical contact indicator, measuring the longitudinal elongation (ΔL) resulting from controlled thermal elevation (ΔT) and evaluating the linear dilatation slope.',
    'target': 'alpha',
    'targetName': 'Linear expansion coefficient alpha',
    'inputLabel': 'Temperature elevation Delta T',
    'shortInput': 'Elevation Delta T',
    'inputUnit': '°C',
    'inputDecimals': 1,
    'rawLabel': 'Elongation Delta L',
    'rawUnit': 'mm',
    'rawDecimals': 3,
    'xAxis': 'Product L_0 Delta T (m K)',
    'yAxis': 'Longitudinal elongation Delta L (m)',
    'xScale': 1.0,
    'yScale': 1000.0,
    'gradientUnit': 'K⁻¹',
    'resultUnit': '× 10⁻⁶ K⁻¹',
    'resultScale': 1000000.0,
    'resultDecimals': 2,
    'min': 10.0,
    'max': 80.0,
    'step': 5.0,
    'initial': 45.0,
    'samples': [15.0, 30.0, 45.0, 60.0, 75.0],
    'emptyX': [0.0, 80.0],
    'emptyY': [0.0, 1.5],
    'timed': False,
    'angle': False,
    'published': True,
    'measureLabel': 'Measure longitudinal elongation Delta L for temperature elevation Delta T',
    'fitEquation': 'ΔL = L_0 · α · ΔT ⇔ Y = α · X ⇔ α = S',
    'intro': "Thermal expansion in crystalline condensed matter is a direct microscopic manifestation of the anharmonicity of interatomic binding potential energy wells. At absolute zero, lattice ions reside at the bottom of an asymmetric potential energy minimum U(r). In a purely harmonic potential well where U(r) = (1/2)k(r − r_0)², thermal agitation increases vibrational amplitude symmetrically about the equilibrium spacing r_0, resulting in zero net shift in mean atomic separation regardless of temperature. In real solids, however, the short-range repulsive force arising from Pauli exclusion overlap between electron clouds is significantly steeper than the longer-range attractive electrostatic or metallic bonding forces. Consequently, as thermal energy kT increases the mean vibrational energy of phonons in the lattice, atoms oscillate across an asymmetric potential curve, vibrating more widely toward larger interatomic separations than toward compressed ones. The time-averaged atomic position ⟨r⟩ shifts outward with rising temperature, macroscopic evidence of which is observed as the thermal expansion of the solid body. For an isotropic solid bar of initial length L_0 at baseline temperature T_0, a uniform temperature increase to T = T_0 + ΔT produces a longitudinal elongation ΔL proportional to both L_0 and ΔT: ΔL = L_0 · α · ΔT, where α is the coefficient of linear thermal expansion (expressed in reciprocal kelvins, K⁻¹ or °C⁻¹). In steam dilatometry, a copper tube or rod is enclosed within an insulated metal steam jacket supported between rigid end frames. One end of the rod bears firmly against a fixed abutment stop, while the opposite end projects through a low-friction packing gland against a precision micrometer screw gauge. To eliminate mechanical deformation and anvil pressure errors, an electrical circuit comprising a dry cell and galvanometer detects the exact physical contact between the micrometer spindle and rod tip. Passing dry steam through the jacket heats the specimen uniformly, and the resulting elongation ΔL is measured across multiple steady-state temperature elevations. Plotting ΔL against the product L_0 · ΔT generates a straight line whose slope directly yields the linear expansion coefficient α.",
    'settings': [
        'Electrolytic copper rod specimen (OFHC, 99.95% Cu); initial length L_0 = 1.0000 m (1000.0 mm) at ambient baseline temperature T_0 = 20.00 °C.',
        'Insulated brass steam dilatometer jacket with central mercury thermometer port, steam inlet tube, and condensation drainage nipple.',
        'Precision micrometer head with pitch p = 0.500 mm and 50 thimble divisions (least count 0.010 mm; optical vernier estimation to ±0.001 mm).',
        'Low-voltage DC contact indicator circuit (1.5 V cell, current-limiting 10 kΩ resistor, and high-sensitivity microammeter / galvanometer).',
        'Reference coefficient of linear thermal expansion of pure copper: α = 16.80 × 10⁻⁶ K⁻¹ (16.80 × 10⁻⁶ °C⁻¹ at 20 °C).'
    ],
    'apparatus': [
        {
            'name': 'Steam Dilatometer Enclosure with Rigid End Abutments',
            'purpose': 'A double-walled brass jacket 1.1 m in length mounted upon a rigid heavy cast-iron bed plate, equipped with low-friction internal guide rollers to support the specimen rod horizontally, an internal thermometer socket, a steam inlet nozzle, a bottom condensate drain, and a hardened steel fixed abutment block at the left end.'
        },
        {
            'name': 'Precision Micrometer Screw Gauge with Spherometer Carriage',
            'purpose': 'A hardened stainless steel micrometer head having a calibrated lead screw pitch of 0.500 mm and 50 circular thimble subdivisions, rigidly clamped to the right end frame to measure longitudinal specimen displacements with an instrument resolution of 0.001 mm.'
        },
        {
            'name': 'Low-Voltage Electrical Contact Indicator Circuit',
            'purpose': 'A 1.5 V dry cell battery connected in series with a 10 kΩ current-limiting resistor and sensitive center-zero galvanometer between the insulated fixed frame and the micrometer spindle, providing instantaneous, zero-force visual indication when the advancing micrometer tip touches the expanding copper rod.'
        },
        {
            'name': 'Regulated Steam Boiler and High-Precision Thermometer',
            'purpose': 'An electric steam generator supplying saturated water vapor at 100 °C through flexible insulated tubing to elevate the specimen temperature uniformly, monitored by a 0.1 °C immersion thermometer inserted into the central dilatometer chamber.'
        }
    ],
    'procedure': [
        {
            'title': 'Initial Rod Length Measurement and Baseline Temperature Recording',
            'text': 'Measure the overall length of the clean, polished copper rod at ambient room temperature using a precision steel meter scale and vernier calipers to ±0.5 mm, recording L_0 = 1.0000 m. Insert the rod into the steam jacket, seating its left end firmly against the hardened steel fixed abutment stop. Insert the calibrated thermometer into the central socket and record the steady initial room temperature T_0 = 20.00 °C.',
            'why': 'Accurate baseline length and temperature measurements establish the fundamental thermodynamic reference state from which all subsequent longitudinal strain is evaluated.'
        },
        {
            'title': 'Micrometer Spindle Alignment and Zero-Contact Indexing',
            'text': 'Connect the electrical contact indicator leads to the rod and micrometer head. Slowly advance the micrometer thimble until the galvanometer needle deflects, indicating that the spindle has touched the cold rod tip without exerting compressive mechanical strain. Read the micrometer drum to ±0.001 mm and record this initial baseline reading R_0. Back the micrometer screw off by 2 to 3 turns to allow room for free expansion.',
            'why': 'The electrical circuit ensures zero-pressure contact sensing, completely eliminating compressive deformation of the rod and flexion of the mounting frame.'
        },
        {
            'title': 'Steam Generation and Jacket Heating',
            'text': 'Connect the steam generator to the dilatometer inlet and place a beaker beneath the drain nipple to collect condensed water. Activate the boiler and admit steam steadily into the jacket. Observe the rapid temperature rise on the central thermometer and allow steam to circulate until condensate flows smoothly and the thermometer reading stabilizes.',
            'why': 'Uniform circulation of saturated steam sweeps air from the chamber and guarantees that the entire length of the copper rod achieves an isothermal steady state.'
        },
        {
            'title': 'Thermal Elongation Measurement at Elevated Temperature',
            'text': 'Once steady-state equilibrium is attained at the target temperature (e.g., T = 65.0 °C, giving ΔT = 45.0 °C), carefully advance the micrometer thimble until the galvanometer needle just twitches. Record the hot micrometer reading R_hot to ±0.001 mm. The longitudinal elongation is evaluated as ΔL = R_hot − R_0. Immediately retract the screw to prevent jamming.',
            'why': 'Making the measurement precisely at steady-state equilibrium prevents transient temperature gradients from distorting the calculated elongation.'
        },
        {
            'title': 'Multi-Station Thermal Elevation Acquisition',
            'text': 'Repeat the measurement procedure across five distinct temperature elevations (ΔT = 15.0 °C, 30.0 °C, 45.0 °C, 60.0 °C, and 75.0 °C) by adjusting the steam-air mixing ratio or tracking the cooling curve of the jacket. For each setting, record the stable temperature elevation ΔT and corresponding micrometer elongation ΔL.',
            'why': 'Collecting multiple data pairs across a wide thermal span verifies the linearity of the thermal dilatation law and provides statistical redundancy for regression analysis.'
        },
        {
            'title': 'Linear Regression and Expansion Coefficient Evaluation',
            'text': 'For each observation, calculate the independent variable X = L_0 · ΔT in m K (or m °C) and the dependent displacement Y = ΔL in meters. Plot Y against X, perform ordinary least-squares linear regression to determine the gradient S, and evaluate the linear thermal expansion coefficient α = S. Compare α with the standard reference value for electrolytic copper.',
            'why': 'Ordinary least-squares regression averages out minor micrometer reading scatter and isolates the true linear slope independent of single-trial zero offsets.'
        }
    ],
    'topics': [
        {
            'title': 'Anharmonicity of Interatomic Potential and Origin of Thermal Dilatation',
            'text': "The physical origin of thermal expansion in crystalline solids is rooted in the asymmetric shape of the interatomic potential energy curve U(r). In a realistic crystal, the interatomic potential can be modeled by a Lennard-Jones (12-6) or Morse function: U(r) = U_0 [(r_0/r)¹² − 2(r_0/r)⁶], or expanded as a Taylor series about the equilibrium separation r_0: U(x) = c x² − g x³ − f x⁴, where x = r − r_0 represents atomic displacement, c is the harmonic restoring force constant, g is the cubic anharmonicity coefficient, and f is the quartic coefficient. If the potential were strictly harmonic (g = 0, f = 0), the Boltzmann distribution P(x) ∝ exp[−U(x)/(kT)] would be symmetric in ±x, meaning the expectation value ⟨x⟩ = ∫ x exp[−U(x)/(kT)] dx / ∫ exp[−U(x)/(kT)] dx would remain identically zero at all temperatures. However, because atomic electron shells strongly resist overlapping (producing a steep repulsive wall for x < 0) while attractive bonding forces decay gradually with distance (a shallow trough for x > 0), the cubic anharmonic term g is strictly positive. Evaluating the thermal expectation value using perturbation theory yields: ⟨x⟩ ≈ (3g / 4c²) · kT. Thus, as temperature T rises, the average interatomic separation increases linearly with T, giving rise to macroscopic thermal expansion. Without lattice anharmonicity, solids would not expand when heated.",
            'formula': 'U(x) = c x^2 - g x^3 - f x^4 \\implies \\langle x \\rangle \\approx \\frac{3g}{4c^2} k_B T \\implies \\alpha = \\frac{1}{r_0}\\frac{d\\langle x \\rangle}{dT} = \\frac{3g k_B}{4 c^2 r_0}',
            'question': 'Why would a solid with a purely harmonic interatomic potential experience zero thermal expansion?',
            'answer': 'In a purely harmonic potential U(x) = cx², the energy well is perfectly symmetrical about the equilibrium position. When heated, atoms vibrate with larger amplitudes, but their time-averaged position ⟨x⟩ remains exactly at the center. Thermal expansion requires anharmonicity (the cubic term −gx³), which creates an asymmetric well that shifts the average atomic separation outward as energy increases.'
        },
        {
            'title': 'Linear, Areal, and Volumetric Expansion Relationships in Isotropic Solids',
            'text': "In isotropic materials where physical properties are identical in all spatial directions, thermal dilatation is described by a single scalar coefficient. Consider a rectangular block of dimensions L_x, L_y, L_z at baseline temperature T_0. When heated through ΔT, each linear dimension expands according to L_i(T) = L_{i,0}(1 + α ΔT). The resulting area of any face (e.g., A = L_x L_y) becomes A(T) = L_{x,0} L_{y,0}(1 + α ΔT)² = A_0(1 + 2α ΔT + α² ΔT²). Because typical expansion coefficients for metals are of order 10⁻⁵ K⁻¹, the second-order term α² ΔT² is negligible (e.g., (1.68 × 10⁻⁵ × 50)² ≈ 7 × 10⁻⁷), allowing the areal thermal expansion coefficient to be approximated as β ≈ 2α. Similarly, the expanded volume evaluates to V(T) = V_0(1 + α ΔT)³ = V_0(1 + 3α ΔT + 3α² ΔT² + α³ ΔT³). Neglecting higher-order terms yields V(T) ≈ V_0(1 + γ ΔT), establishing the fundamental thermodynamic relation γ ≈ 3α for isotropic solids. For anisotropic crystals such as calcite, zinc, or graphite, thermal expansion is a second-rank tensor α_ij, where expansion along different crystallographic axes can vary dramatically and may even exhibit negative thermal expansion along specific axes.",
            'formula': '\\beta = \\frac{1}{A_0}\\frac{dA}{dT} \\approx 2\\alpha \\quad \\text{and} \\quad \\gamma = \\frac{1}{V_0}\\frac{dV}{dT} \\approx 3\\alpha \\quad (\\text{for isotropic solids where } \\alpha \\Delta T \\ll 1)',
            'question': 'What is the mathematical relationship connecting the linear, areal, and volumetric thermal expansion coefficients in an isotropic solid?',
            'answer': 'For isotropic solids where αΔT is small compared to unity, the areal coefficient is β ≈ 2α and the volumetric coefficient is γ ≈ 3α. This derives directly from expanding (1 + αΔT)² and (1 + αΔT)³ and dropping the negligible higher-order terms in α² and α³.'
        },
        {
            'title': 'The Steam Dilatometer and Electrical Contact Sensing Principle',
            'text': "Measuring the thermal expansion of a 1.00-meter rod over a temperature elevation of 50 °C poses a delicate metrological challenge: the total elongation is only ΔL = 1.000 m × 16.80 × 10⁻⁶ K⁻¹ × 50 K = 0.840 mm (840 microns). If a mechanical micrometer screw is turned until it physically pinches the expanding rod, the compressive contact force can easily distort the frame, indent the soft copper rod tip, and compress the specimen longitudinally according to Hooke's law: δ_comp = F L_0 / (A Y). For a 6 mm diameter copper rod (A ≈ 2.83 × 10⁻⁵ m², Young's modulus Y ≈ 110 GPa), an anvil contact force of just 10 newtons causes a compressive strain of δ_comp ≈ 3.2 microns—introducing a 0.4% systematic measurement error. To eliminate contact force entirely, modern university steam dilatometers employ an electrical indicator circuit. The micrometer screw and specimen rod are placed in series with a 1.5 V DC source, a high-value current-limiting resistor, and a sensitive galvanometer or LED. As the micrometer screw is advanced slowly, the very first atomic contact between the polished spindle face and rod end closes the electrical circuit, instantly triggering a galvanometer deflection or lighting the indicator. The observer records the drum reading at this exact threshold of zero mechanical pressure, ensuring sub-micron accuracy.",
            'formula': '\\Delta L = L_0 \\alpha \\Delta T \\quad \\text{with} \\quad \\delta_{\\text{compression}} = \\frac{F L_0}{A Y} \\to 0 \\quad (\\text{via electrical contact sensing})',
            'question': 'Why is an electrical contact circuit used with the micrometer screw gauge in precision dilatometry?',
            'answer': 'If the micrometer screw is tightened manually against the rod until mechanical resistance is felt, the applied force flexes the support frame and compresses the copper rod elastically, introducing significant systematic error. The electrical circuit detects the instant of microscopic touch with zero contact pressure, eliminating mechanical deformation errors.'
        },
        {
            'title': 'Thermodynamic and Mechanical Stress in Constrained Thermal Expansion',
            'text': "When a solid bar is heated while its ends are rigidly constrained between unyielding walls, its natural tendency to expand is frustrated, generating immense internal compressive stress. The free thermal strain that would occur without constraint is ε_th = ΔL/L_0 = α ΔT. To maintain the bar at its original length (net strain ε_net = 0), the rigid supports must exert an opposing mechanical compressive strain equal in magnitude to the thermal strain: ε_mech = −σ / Y, where σ is the internal stress and Y is Young's modulus of the material. Equating strains yields the thermal stress equation: σ = −Y α ΔT. For a copper bar (Y = 110 GPa, α = 16.80 × 10⁻⁶ K⁻¹) heated through ΔT = 50 °C, the resulting compressive stress is σ = 110 × 10⁹ Pa × 16.80 × 10⁻⁶ K⁻¹ × 50 K = 92.4 MPa (924 atmospheres). If the bar has a cross-sectional area of 1.0 cm² (1.0 × 10⁻⁴ m²), the compressive thrust against the end walls reaches F = σ A = 9,240 newtons (~940 kg-force). This dramatic thermal stress explains why railway tracks require expansion gaps or prestressed continuous welding, why concrete bridges feature expansion joint combs, and why dilatometers must permit one end of the specimen to expand freely against the measuring instrument.",
            'formula': '\\sigma = -Y \\alpha \\Delta T \\quad \\text{and} \\quad F = A Y \\alpha \\Delta T \\quad (\\text{for rigidly constrained ends})',
            'question': 'What happens if a metal rod is heated while both of its ends are held completely rigid and immovable?',
            'answer': 'Immense internal compressive stress develops, equal to σ = Y α ΔT, where Y is Young’s modulus. For copper heated by 50 °C, this thermal stress exceeds 92 MPa, exerting thousands of newtons of thrust on the supports and risking severe buckling or mechanical failure.'
        },
        {
            'title': 'Temperature Non-Uniformity and Longitudinal Heat Loss Gradients',
            'text': "A principal source of systematic error in jacketed steam dilatometry is longitudinal temperature non-uniformity along the specimen rod. In an ideal dilatometer, saturated dry steam at 100 °C flows rapidly through the jacket, bathing the entire surface of the rod and establishing an isothermal boundary condition. However, at the two extremities where the rod emerges through rubber stoppers or glands to contact the fixed stop and micrometer spindle, significant conductive heat loss occurs along the exposed metal ends to the ambient room air. Furthermore, if condensed water pools along the bottom of the jacket, the lower surface of the rod may experience a different heat transfer coefficient than the upper surface exposed to turbulent steam vapor. The effective thermal elongation of the rod represents the integral of the local thermal strain across the full length: ΔL = ∫_0^{L_0} α [T(x) − T_0] dx = L_0 α (T_avg − T_0), where T_avg is the true length-averaged temperature. If the thermometer bulb is located near the central steam inlet, it may record 100.0 °C while the exposed rod ends are at only 85 °C to 90 °C, causing T_avg to be lower than the recorded temperature T_therm. Neglecting this end-loss gradient causes the calculated expansion coefficient α = ΔL / [L_0(T_therm − T_0)] to be systematically underestimated by 1% to 3%. To minimize this error, well-designed dilatometers utilize thermal insulating collars around the projecting tips and maintain high steam throughput.",
            'formula': '\\Delta L = \\int_0^{L_0} \\alpha [T(x) - T_0] dx = L_0 \\alpha (\\bar{T} - T_0) \\quad \\text{where } \\bar{T} = \\frac{1}{L_0} \\int_0^{L_0} T(x) dx',
            'question': 'Why might the measured expansion coefficient be systematically too low if the rod ends protrude outside the steam jacket?',
            'answer': 'The protruding metal ends conduct heat to the cool room air, causing them to stay cooler than the central steam chamber. If the thermometer only measures the hot center, the assumed temperature rise is higher than the true length-averaged temperature rise along the entire rod, causing the calculated expansion coefficient α = ΔL / (L₀ΔT) to be systematically underestimated.'
        },
        {
            'title': 'Instrumental Backlash, Zero Indexing, and Pitch Calibration of Micrometer Screws',
            'text': "The precision micrometer screw gauge is the primary displacement sensor in the dilatometer apparatus. A standard metric micrometer features a precision ground lead screw with a pitch of p = 0.500 mm, meaning one complete 360° revolution of the thimble advances the spindle by exactly half a millimeter. With 50 equal graduations etched along the circumference of the thimble, the least count (smallest directly readable division) evaluates to LC = pitch / divisions = 0.500 mm / 50 = 0.010 mm (10 microns). With careful interpolation using an optical loupe or vernier sleeve graduations, readings can be estimated to ±0.001 mm (1 micron). However, screw mechanisms are vulnerable to mechanical backlash: the slight clearance between the male screw threads and female nut threads required to permit low-friction rotation. If the screw is reversed during a measurement, the spindle does not move immediately until the thread clearance is traversed. To eliminate backlash error, the micrometer must always approach the contact point from the same direction (advancing forward toward the rod). Furthermore, the zero reading R_0 must be recorded under identical directional approach at baseline temperature before heating.",
            'formula': '\\text{Least Count (LC)} = \\frac{\\text{Pitch (mm)}}{\\text{Thimble Divisions}} = \\frac{0.500 \\text{ mm}}{50} = 0.010 \\text{ mm} \\quad (\\pm 0.001 \\text{ mm estimated})',
            'question': 'What is mechanical backlash in a micrometer screw, and how is it avoided during thermal expansion measurements?',
            'answer': 'Backlash is the mechanical slack or clearance between the internal mating screw threads, which causes lost motion when reversing rotational direction. It is eliminated by always rotating the micrometer thimble in the same forward direction when approaching the contact point for both cold and hot readings.'
        },
        {
            'title': 'Comparative Expansion Coefficients of Engineering Metals and Invar Alloys',
            'text': "The magnitude of the linear thermal expansion coefficient α varies widely across engineering materials, reflecting differences in crystal structure, bond strength, and melting points. Refractory metals with deep interatomic potential wells and high melting points generally exhibit small expansion coefficients: tungsten (T_m = 3,422 °C, α ≈ 4.5 × 10⁻⁶ K⁻¹), molybdenum (α ≈ 5.0 × 10⁻⁶ K⁻¹), and platinum (α ≈ 9.0 × 10⁻⁶ K⁻¹). Common engineering metals possess moderate expansion rates: iron and mild steel (α ≈ 11.5–12.0 × 10⁻⁶ K⁻¹), copper (α ≈ 16.80 × 10⁻⁶ K⁻¹), brass (α ≈ 19.0 × 10⁻⁶ K⁻¹), and aluminum (α ≈ 23.1 × 10⁻⁶ K⁻¹). The difference between copper and steel underlies the operation of bimetallic strips: when bonded together and heated, the copper expands more than the steel, forcing the strip to bend into an arc toward the steel side, widely exploited in mechanical thermostats, fire alarms, and thermal circuit breakers. In 1896, Charles Édouard Guillaume discovered Invar (Fe-36% Ni), an alloy possessing an extraordinarily low expansion coefficient: α_invar ≈ 1.2 × 10⁻⁶ K⁻¹ near room temperature. In Invar, an anomalous spontaneous volume magnetostriction arising from the alignment of ferromagnetic d-electron spins expands the lattice as temperature drops, almost exactly canceling the normal thermal contraction from lattice vibrations over the range −20 °C to +100 °C, earning Guillaume the 1920 Nobel Prize in Physics.",
            'formula': '\\alpha_{\\text{Al}} (23.1) > \\alpha_{\\text{Brass}} (19.0) > \\alpha_{\\text{Cu}} (16.8) > \\alpha_{\\text{Steel}} (11.8) > \\alpha_{\\text{Invar}} (1.2) \\quad [\\times 10^{-6} \\text{ K}^{-1}]',
            'question': 'Why does a bimetallic strip made of copper and iron bend when heated, and in which direction does it bend?',
            'answer': 'Copper has a higher thermal expansion coefficient (16.8 × 10⁻⁶ K⁻¹) than iron (11.8 × 10⁻⁶ K⁻¹). When bonded together and heated, the copper side expands more than the iron side, forcing the strip to bend into an arc with the copper on the outside (convex side) and the iron on the inside (concave side).'
        }
    ],
    'precautions': [
        'Always advance the micrometer spindle in the forward direction when approaching the rod tip to eliminate mechanical screw backlash.',
        'Ensure the electrical contact circuit is operational and watch for the earliest galvanometer deflection to avoid compressive strain on the specimen.',
        'Allow saturated steam to flow through the jacket until condensation drains steadily and the thermometer reading is completely stationary before recording hot measurements.',
        'Ensure that the fixed end stop remains completely rigid and immovably clamped to the bed plate throughout the thermal cycle.'
    ],
    'quiz': [
        {
            'question': 'When plotting longitudinal elongation ΔL on the vertical axis against the product L_0 · ΔT on the horizontal axis, what does the slope of the regression line represent?',
            'options': [
                'The coefficient of linear thermal expansion α (K⁻¹ or °C⁻¹).',
                'The volumetric thermal expansion coefficient γ.',
                'Young’s modulus of the copper specimen Y.',
                'The thermal conductivity of the metal k.'
            ],
            'correct': 0,
            'explanation': 'Because the governing dilatation relation is ΔL = L_0 · α · ΔT, plotting ΔL against L_0 · ΔT gives a straight line y = m x where y = ΔL, x = L_0 ΔT, and the gradient m directly equals the linear expansion coefficient α.'
        },
        {
            'question': 'What microscopic property of a crystal lattice is directly responsible for thermal expansion in solids?',
            'options': [
                'The cubic anharmonicity of the interatomic potential energy well.',
                'The Pauli exclusion principle acting purely symmetrically.',
                'The presence of free valence electrons in the conduction band.',
                'The mass difference between valence protons and electrons.'
            ],
            'correct': 0,
            'explanation': 'In an ideal harmonic potential well U(x) = cx², the mean position of vibrating atoms is temperature-independent. The cubic anharmonic term −gx³ creates an asymmetric potential well that shifts the average atomic separation outward as vibrational energy increases.'
        },
        {
            'question': 'A copper rod of initial length 1.000 m is heated through a temperature rise of 50.0 °C. Given α = 16.80 × 10⁻⁶ K⁻¹, what is the expected longitudinal elongation?',
            'options': [
                '0.840 mm',
                '0.084 mm',
                '1.680 mm',
                '8.400 mm'
            ],
            'correct': 0,
            'explanation': 'ΔL = L_0 · α · ΔT = 1.000 m × 16.80 × 10⁻⁶ K⁻¹ × 50.0 K = 8.40 × 10⁻⁴ m = 0.840 mm.'
        },
        {
            'question': 'Why is Invar (an iron-nickel alloy) widely used in precision pendulums, clock balances, and surveying tapes?',
            'options': [
                'Its spontaneous magnetostriction counteracts lattice thermal expansion, giving an exceptionally low α near room temperature (~1.2 × 10⁻⁶ K⁻¹).',
                'It has the highest electrical conductivity of any known alloy.',
                'It melts at a lower temperature than ice, preventing thermal stresses.',
                'It expands identically in all three dimensions with zero internal strain.'
            ],
            'correct': 0,
            'explanation': 'Invar (Fe-36% Ni) exhibits an anomalously low thermal expansion coefficient (~1.2 × 10⁻⁶ K⁻¹) due to magnetic electron interactions that expand the lattice as temperature decreases, canceling normal thermal contraction.'
        }
    ],
    'limitations': 'The teaching simulation models linear thermal dilatation under steady-state isothermal conditions with an initial rod length L_0 = 1.0000 m at T_0 = 20.00 °C and an invariant reference expansion coefficient α = 16.80 × 10⁻⁶ K⁻¹. In physical experiments, minor temperature gradients exist along the length of the steam jacket (especially near the protruding ends), thermometer thermal lag and stem emergent column errors can cause small temperature reading offsets, mechanical micrometer backlash or pitch errors contribute displacement uncertainty (±0.002 mm), electrical contact threshold sensitivity can vary with surface oxide film formation on the copper tip, and slight frame flexion during thermal elevation can introduce small structural offsets.',
    'modelExtra': 'The simulation calculates longitudinal elongation using the linear dilatation relationship ΔL = L_0 · α · ΔT, where L_0 = 1.0000 m is the baseline length, α = 16.80 × 10⁻⁶ K⁻¹ is the reference linear expansion coefficient for pure copper, and ΔT = T − T_0 is the temperature elevation above 20.00 °C. Elongation readings are rounded to 0.001 mm to match high-precision micrometer screw resolutions, and ordinary least-squares regression of ΔL against L_0 · ΔT across five temperature stations yields the reported linear expansion coefficient.'
}

# 1. Update experiments.json
exp_path = ROOT / 'content/physics/experiments.json'
experiments = json.loads(exp_path.read_text())
existing_idx = next((i for i, e in enumerate(experiments) if e['slug'] == 'thermal-expansion'), None)
if existing_idx is not None:
    experiments[existing_idx] = exp29
else:
    experiments.append(exp29)
exp_path.write_text(json.dumps(experiments, indent=2, ensure_ascii=False))
print(f'experiments.json updated. Total experiments: {len(experiments)}')

# 2. Update catalog.sqlite3
db_path = ROOT / 'data/catalog.sqlite3'
db = sqlite3.connect(db_path)
cur = db.cursor()
cur.execute('DELETE FROM experiments WHERE slug = ?', ('thermal-expansion',))
cur.execute('''
    INSERT INTO experiments (subject_id, slug, title, status, page_path, theory_path, report_path)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    1,
    'thermal-expansion',
    'Determination of the coefficient of linear thermal expansion of copper',
    'live',
    '/physics/thermal-expansion/',
    '/physics/thermal-expansion/theory/',
    '/physics/thermal-expansion/report/'
))
db.commit()
db.close()
print('catalog.sqlite3 updated successfully for thermal-expansion.')
