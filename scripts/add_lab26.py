import json, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

exp26 = {
    'number': 26,
    'slug': 'solidification-cooling',
    'title': 'Determination of the Latent Heat of Fusion by the Method of Cooling',
    'shortTitle': 'Solidification Cooling Curve',
    'aim': 'Investigate the cooling curve of a substance passing through a change of state from liquid to solid, observe the isothermal solidification arrest plateau, and determine the latent heat of fusion of salol (phenyl salicylate) from the duration of the solidification arrest under a known steady rate of heat loss.',
    'target': 'L_f',
    'targetName': 'Latent heat of fusion L_f',
    'inputLabel': 'Mass of salol m',
    'shortInput': 'Salol mass m',
    'inputUnit': 'g',
    'inputDecimals': 1,
    'rawLabel': 'Solidification arrest duration Δt',
    'rawUnit': 'min',
    'rawDecimals': 2,
    'xAxis': 'Mass of substance m (kg)',
    'yAxis': 'Total latent heat liberated Q_latent (J)',
    'xScale': 1000.0,
    'yScale': 0.001,
    'gradientUnit': 'J kg⁻¹',
    'resultUnit': 'kJ kg⁻¹',
    'resultScale': 0.001,
    'resultDecimals': 2,
    'min': 10.0,
    'max': 45.0,
    'step': 2.5,
    'initial': 25.0,
    'samples': [15.0, 20.0, 25.0, 30.0, 35.0],
    'emptyX': [0.0, 0.050],
    'emptyY': [0.0, 3500.0],
    'timed': False,
    'angle': False,
    'published': True,
    'measureLabel': 'Measure solidification plateau duration Δt for mass m of salol',
    'fitEquation': 'Q_latent = R_loss · Δt = m · L_f ⇔ Y = L_f · X ⇔ L_f = S',
    'intro': "When a pure crystalline chemical substance in the molten state undergoes continuous cooling, its thermodynamic trajectory exhibits a sharp, qualitative distinction from the smooth exponential decay characteristic of homogeneous single-phase cooling. As sensible heat is initially extracted, the liquid temperature drops monotonically according to Newton's law of cooling until reaching the melting temperature T_m. At this critical boundary, the thermodynamic driving force initiates a first-order phase transition: disordered liquid molecules assemble into a rigid crystalline lattice, releasing their latent heat of fusion L_f. Throughout this crystallization process, the liberation of latent enthalpy exactly compensates for the thermal energy dissipated to the environment, pinning the temperature of the coexisting liquid-solid mixture at the constant equilibrium melting point. This creates an extended horizontal arrest plateau on the cooling curve whose temporal duration Δt is directly proportional to the total mass m of the crystallizing specimen. By enclosing the test vessel in a standardized air-jacketed container surrounded by a constant-temperature bath, the ambient rate of heat loss R_loss at the freezing temperature remains invariant across successive trials. Equating the liberated latent heat Q_latent = R_loss · Δt to m · L_f yields a direct linear relationship between the thermal arrest duration and the mass of the charge. Linear regression over varying sample masses provides an exceptionally clean determination of the latent heat of fusion, while contrasting the sharp arrest plateau of crystalline salol with the continuous, sloped vitrification curves of amorphous substances such as paraffin wax reveals fundamental insights into solid-state thermodynamics.",
    'settings': [
        'Pure crystalline test substance: Salol (phenyl salicylate, C₁₃H₁₀O₃); equilibrium melting point T_m = 41.5 °C.',
        'Standardized thin-walled boiling tube (outer diameter 25.0 mm) suspended in a concentric air-jacketed outer beaker.',
        'Calibrated steady heat loss rate to surroundings at 41.5 °C: R_loss = 270.0 J min⁻¹ (4.50 W).',
        'Reference latent heat of fusion for phenyl salicylate: L_f = 79.50 kJ kg⁻¹ (79,500 J kg⁻¹).'
    ],
    'apparatus': [
        {
            'name': 'Standardized Boiling Tube with Air-Jacketed Cooling Enclosure',
            'purpose': 'A thin-walled borosilicate glass test tube (25 mm diameter, 150 mm length) held coaxially inside a wider glass cylinder by a split cork ring, providing a stagnant annular air buffer that ensures uniform, draft-free convective and radiative cooling to ambient surroundings.'
        },
        {
            'name': 'Precision Immersion Calorimetric Thermometer (0.1°C Divisions)',
            'purpose': 'A short-range mercury-in-glass thermometer graduated from 20°C to 70°C in 0.1°C subdivisions, positioned centrally within the molten salol to record the temperature descent, supercooling dip, and the steady horizontal solidification plateau.'
        },
        {
            'name': 'Helical Wire Stirrer and Seeding Probe',
            'purpose': 'A fine nichrome wire formed into a loop encircling the thermometer stem, used to agitate the liquid gently prior to crystallization and to introduce a microscopic seed crystal to arrest supercooling promptly at 41.5 °C.'
        },
        {
            'name': 'Digital Laboratory Stopclock and Regulated Water Heating Bath',
            'purpose': 'A precision digital timer recording elapsed time to 0.01 min, paired with a thermostatically controlled warm water bath used to melt the salol sample completely to approximately 60 °C before cooling runs.'
        }
    ],
    'procedure': [
        {
            'title': 'Apparatus Assembly and Mass Determination',
            'text': 'Weigh the clean, dry boiling tube together with its wire stirrer to ±0.01 g using an analytical balance. Introduce a known mass m of pure crystalline salol (e.g., 15.0 g) into the tube, reweigh the assembly to confirm the exact specimen charge, and secure the tube in a clamp ready for melting.',
            'why': 'Accurate gravimetric determination of the sample mass is critical because the total latent heat liberated during phase transition scales directly with mass (Q = m · L_f).'
        },
        {
            'title': 'Thermal Liquefaction in Warm Water Bath',
            'text': 'Immerse the lower half of the boiling tube in a beaker of water maintained between 60 °C and 65 °C. Allow the salol crystals to melt entirely until an optical inspection confirms complete liquefaction with no residual solid crust adhering to the inner walls, reaching a uniform liquid temperature of approximately 55 °C to 60 °C.',
            'why': 'Complete melting dissolves all pre-existing crystal nuclei, ensuring that subsequent cooling commences from an entirely homogeneous liquid state and that thermal history does not introduce erratic crystallization artifacts.'
        },
        {
            'title': 'Air-Jacket Mounting and Thermometer Placement',
            'text': 'Remove the tube from the warm water bath, wipe its outer surface thoroughly dry, and seat it firmly inside the wider outer air-jacket cylinder using the split cork collar. Insert the precision thermometer through the cork so its mercury bulb is centered vertically and horizontally within the molten salol volume.',
            'why': 'Drying the outer surface prevents evaporative cooling from lingering water droplets, while the concentric air jacket eliminates ambient air drafts and establishes a reproducible, uniform heat loss rate R_loss.'
        },
        {
            'title': 'Cooling Curve Observation and Nucleation Seeding',
            'text': 'Start the digital stopclock and record the temperature of the salol every 30 seconds as it cools. As the temperature nears 41.5 °C, monitor for supercooling (where the liquid drops 1°C to 2°C below T_m without solidifying). Touch a microscopic speck of solid salol on the tip of the stirrer wire to seed nucleation, observing the immediate thermal rebound to the steady arrest temperature T_m = 41.5 °C.',
            'why': 'Salol readily supercools in clean glassware. Prompt seeding initiates crystallization at the true thermodynamic transition point, preventing prolonged metastable liquid states from corrupting the plateau duration measurement.'
        },
        {
            'title': 'Measurement of Solidification Arrest Duration',
            'text': 'Observe the thermometer reading during the crystallization process. Note the precise time t_start when the temperature stabilizes at 41.5 °C and the time t_end when all liquid has transformed into crystalline solid and the temperature resumes a rapid downward decline. Evaluate the plateau duration Δt = t_end − t_start in minutes.',
            'why': 'The duration of the horizontal temperature plateau represents the exact interval during which the rate of latent heat liberation matches the steady rate of heat loss to the jacket (Q_latent = R_loss · Δt).'
        },
        {
            'title': 'Series Repetition, Tabulation, and Regression Analysis',
            'text': 'Repeat the measurement for five distinct masses of salol (15.0 g, 20.0 g, 25.0 g, 30.0 g, and 35.0 g). For each run, compute the total heat liberated Q_latent = R_loss · Δt in joules. Plot Q_latent against mass m (kg), perform an ordinary least-squares fit through the origin, and determine the latent heat of fusion L_f from the gradient.',
            'why': 'Testing multiple sample masses distributes instrumental timing and mass reading uncertainties across the regression line, verifying the direct proportionality Q = m · L_f and suppressing random errors.'
        }
    ],
    'topics': [
        {
            'title': 'First-Order Phase Transitions and Latent Heat of Fusion',
            'text': "In classical thermodynamics, phase transitions are classified according to the Ehrenfest taxonomy by the lowest derivative of the Gibbs free energy G that exhibits a discontinuity at the transition point. For a first-order phase change such as solid-liquid melting or freezing, the chemical potential μ and Gibbs free energy are continuous across the phase boundary, but the first partial derivatives—entropy S = −(∂G/∂T)_P and volume V = (∂G/∂P)_T—undergo finite step discontinuities. The discontinuity in entropy ΔS_trans = S_liquid − S_solid corresponds directly to the absorption or liberation of a finite quantity of thermal energy at constant temperature: the latent heat of transition Q_latent = T_m ΔS_trans. Per unit mass, this is the specific latent heat of fusion L_f = Q_latent / m. During solidification, disordered molecular bonds in the molten state collapse into an ordered crystalline lattice, shedding intermolecular potential energy into thermal agitation. Because this latent enthalpy release exactly compensates for external heat loss, the coexisting two-phase system possesses zero thermodynamic degrees of freedom under constant pressure (Gibbs phase rule: F = C − P + 1 = 1 − 2 + 1 = 0), holding the temperature rigorously constant at T_m until phase transformation is complete.",
            'formula': 'L_f = \\frac{Q_{\\text{latent}}}{m} = T_m \\Delta s_{\\text{trans}} \\quad \\text{and} \\quad F = C - P + 1 = 0',
            'question': 'Why does the temperature of a pure substance remain constant during solidification even while losing heat to the surroundings?',
            'answer': 'Solidification is a first-order phase transition where latent heat of fusion is liberated as molecules transition from disordered liquid to an ordered crystalline lattice. This internal enthalpy release exactly balances the heat lost to the surroundings, keeping the temperature constant until the entire liquid mass has crystallized.'
        },
        {
            'title': 'The Cooling Curve Method: Energy Balance and Rate of Heat Loss',
            'text': "The determination of latent heat by the method of cooling relies upon establishing an energy conservation balance for a body cooling inside a constant-temperature enclosure. Consider a boiling tube containing mass m of a substance possessing liquid specific heat c_L, solid specific heat c_S, and latent heat of fusion L_f, held in an enclosure maintained at ambient temperature T_0. When the contents are liquid at temperature T > T_m, sensible heat is lost at rate dQ/dt = (m c_L + W_tube) (dT/dt) = −R_loss(T). During the solidification arrest at T = T_m, sensible temperature change ceases (dT/dt = 0). The rate of latent heat liberation dm_solid/dt · L_f must balance the external heat loss rate R_loss(T_m). Integrating over the complete duration of the plateau Δt yields the total latent heat: Q_latent = ∫₀^{Δt} R_loss(T_m) dt = R_loss(T_m) · Δt = m · L_f. If the heat loss rate R_loss at the melting point is independently calibrated (or determined from the sensible cooling slopes immediately preceding and following the arrest), the latent heat of fusion evaluates simply as L_f = (R_loss · Δt) / m. Plotting Q_latent = R_loss · Δt on the vertical axis against mass m on the horizontal axis yields a linear plot passing through the origin with slope equal to L_f.",
            'formula': 'Q_{\\text{latent}} = R_{\\text{loss}}(T_m) \\cdot \\Delta t = m \\cdot L_f \\iff \\Delta t = \\left(\\frac{L_f}{R_{\\text{loss}}}\\right) m',
            'question': 'How does the duration of the solidification plateau relate to the mass of the substance and the rate of heat loss?',
            'answer': 'The plateau duration Δt is directly proportional to the sample mass m and inversely proportional to the ambient heat loss rate R_loss at the melting point: Δt = (m · L_f) / R_loss. A larger mass contains more latent enthalpy and requires a longer time to solidify at a given rate of heat dissipation.'
        },
        {
            'title': 'Supercooling, Nucleation Kinetics, and Metastable States',
            'text': "A ubiquitous phenomenon encountered in cooling curves of liquids is supercooling (undercooling), wherein the liquid temperature dips significantly below the thermodynamic melting point T_m without crystallizing. Classical nucleation theory explains that the formation of a microscopic crystalline embryo of radius r inside a homogeneous liquid requires creating a solid-liquid interface with interfacial surface energy γ. The total change in Gibbs free energy to form an embryo is ΔG(r) = 4π r² γ − (4/3)π r³ Δg_v, where Δg_v is the volumetric thermodynamic driving force, which is proportional to the undercooling degree ΔT = T_m − T. For small undercooling, the positive interfacial energy term dominates, creating a free energy barrier ΔG* at a critical nucleus radius r* = 2γ / Δg_v. Embryos smaller than r* spontaneously redissolve. Consequently, a clean, undisturbed liquid remains trapped in a metastable state. Once a critical nucleus forms spontaneously or is introduced via artificial seeding, crystal growth proceeds rapidly. The rapid liberation of latent heat of fusion heats the surrounding liquid back up to the equilibrium transition temperature T_m, producing a characteristic sharp dip followed by an immediate temperature recovery to the horizontal plateau.",
            'formula': '\\Delta G^* = \\frac{16\\pi \\gamma^3}{3 (\\Delta g_v)^2} \\quad \\text{and} \\quad r^* = \\frac{2\\gamma}{\\Delta g_v} \\propto \\frac{1}{T_m - T}',
            'question': 'What causes supercooling, and why does the temperature rise back to the melting point once crystallization begins?',
            'answer': 'Supercooling occurs because forming initial microscopic crystal nuclei requires overcoming an interfacial energy barrier. In the absence of nuclei, the liquid remains metastable below T_m. Once nucleation is triggered, rapid crystal growth liberates latent heat faster than it can escape to the surroundings, warming the mixture back to the equilibrium melting point T_m.'
        },
        {
            'title': 'Contrasting Crystalline Solids and Amorphous Glass Formers',
            'text': "The cooling curve provides a decisive diagnostic test to differentiate true crystalline materials from amorphous or vitreous substances. In a crystalline material like salol (phenyl salicylate), naphthalene, or water, the molecules possess long-range periodic translational order. The solid-liquid transition occurs at a sharply defined thermodynamic temperature T_m, manifesting on the cooling curve as an abrupt change in slope from negative to zero, forming an extended horizontal plateau. In contrast, amorphous substances like paraffin wax, glass, or pitch lack long-range periodic order. As molten paraffin wax cools, its long, tangled alkane chains experience increasing van der Waals attractions and steric hindrance, leading to a continuous, progressive increase in dynamic viscosity. Rather than a sharp first-order phase arrest, the cooling curve of paraffin displays a continuous, smoothly downward-sloping sigmoidal trajectory with only a slight inflection marking the glass transition or gradual softening range. Comparing the cooling curves of salol and paraffin wax vividly demonstrates the distinction between true latent heat release at a singular melting point and continuous vitrification without latent enthalpy discontinuity.",
            'formula': '\\text{Crystalline: } \\left(\\frac{dT}{dt}\\right)_{T_m} = 0 \\quad \\text{vs.} \\quad \\text{Amorphous: } \\left(\\frac{dT}{dt}\\right) < 0 \\text{ everywhere}',
            'question': 'How does the cooling curve of a crystalline substance differ fundamentally from that of an amorphous substance like wax?',
            'answer': 'A crystalline substance exhibits a distinct horizontal arrest plateau (dT/dt = 0) at its exact melting point due to the liberation of latent heat. An amorphous substance has no fixed melting point or latent heat; its cooling curve slopes continuously downward through a broad softening and glass transition zone.'
        },
        {
            'title': 'Calibration of Heat Loss Rate R_loss from Pre- and Post-Arrest Slopes',
            'text': "To evaluate the latent heat of fusion quantitatively without relying on an external electrical calibration heater, the heat loss rate R_loss at the melting point can be extracted directly from the cooling curve geometry. Just prior to the onset of crystallization, the liquid of mass m and specific heat c_L cools with instantaneous slope (dT/dt)_L at T = T_m. The rate of heat dissipation at this instant is R_loss = (m c_L + W_tube) |dT/dt|_L. Similarly, immediately following complete solidification, the solid substance of specific heat c_S cools with slope (dT/dt)_S, giving R_loss = (m c_S + W_tube) |dT/dt|_S. Averaging these two independent estimates accounts for minor differences between liquid and solid specific heat capacities: R_loss(T_m) ≈ ½ [ (m c_L + W_tube) |dT/dt|_L + (m c_S + W_tube) |dT/dt|_S ]. For standardized boiling tubes of salol in our apparatus configuration, the total rate of radiative and convective heat loss at 41.5 °C into ambient air at 20.0 °C is R_loss = 270.0 J min⁻¹ (4.50 W). This calibration allows the measured plateau duration Δt (min) to be converted directly into total latent enthalpy Q_latent = R_loss · Δt.",
            'formula': 'R_{\\text{loss}}(T_m) = (m c_L + W_{\\text{tube}}) \\left|\\frac{dT}{dt}\\right|_L \\approx 270.0 \\text{ J min}^{-1}',
            'question': 'How can the rate of heat loss R_loss at the freezing point be determined from the cooling curve itself?',
            'answer': 'By measuring the cooling rate (dT/dt) immediately before the plateau begins (in the liquid phase) and immediately after it ends (in the solid phase). Multiplying these slopes by the respective heat capacities of the tube and contents gives the instantaneous heat loss rate at T_m.'
        },
        {
            'title': 'Chemical Properties, Purity, and Physical Constants of Salol',
            'text': "Salol, the common chemical name for phenyl salicylate (C₁₃H₁₀O₃, molecular weight 214.22 g mol⁻¹), is an ester synthesized by the condensation of salicylic acid with phenol. It serves as an exemplary teaching substance for phase change calorimetry due to several advantageous physical properties: it is non-toxic, chemically stable, non-hygroscopic, and possesses a convenient melting point of T_m = 41.5 °C (314.65 K), which is safely above ambient room temperature (20 °C) yet low enough to handle without hazardous heating equipment. Its accepted literature value for the latent heat of fusion is L_f = 79.50 kJ kg⁻¹ (79,500 J kg⁻¹ = 17.03 kJ mol⁻¹). Salol has a liquid density of approximately 1,250 kg m⁻³ and a specific heat capacity of c_L ≈ 1,420 J kg⁻¹ K⁻¹ in the liquid phase and c_S ≈ 1,250 J kg⁻¹ K⁻¹ in the solid crystalline phase. Its pronounced propensity to supercool makes it ideal for demonstrating nucleation seeding and the sharp recovery to the equilibrium phase arrest plateau.",
            'formula': '\\text{Salol: } \\text{C}_{13}\\text{H}_{10}\\text{O}_3, \\; M = 214.22 \\text{ g/mol}, \\; T_m = 41.50 \\text{ }^\\circ\\text{C}, \\; L_f = 79.50 \\text{ kJ/kg}',
            'question': 'Why is phenyl salicylate (salol) particularly well-suited for university laboratory demonstrations of cooling curves and latent heat?',
            'answer': 'Salol has a convenient melting point (41.5 °C) easily accessible with a warm water bath, is non-toxic and chemically stable, possesses a well-documented latent heat of fusion (79.5 kJ/kg), and exhibits clean supercooling and a flat, distinct crystallization plateau.'
        },
        {
            'title': 'Systematic Uncertainties, Incomplete Crystallization, and Radial Gradients',
            'text': "A rigorous analysis of cooling curve calorimetry must account for non-ideal transport mechanisms that perturb the idealized isothermal arrest plateau. In a cylindrical boiling tube, heat escapes radially through the cylindrical glass perimeter and axially through the open tube mouth. Because solid salol is a poor thermal conductor (thermal conductivity k ≈ 0.20 W m⁻¹ K⁻¹), a radial temperature gradient develops across the tube: a solid crust forms against the inner glass wall while the center remains molten. The thermometer bulb, positioned along the central axis, may record a slightly rounded termination of the plateau as the final crystallizing front contracts toward the stem. Furthermore, if the sample is not stirred gently, localized supercooling can cause dendritic crystal growth that traps pockets of liquid, skewing the apparent plateau duration. To minimize these errors, the boiling tube should have a modest diameter (≤ 25 mm), the outer air jacket must remain draft-free to preserve radial symmetry, and sample charges should span a two-fold mass range to ensure robust ordinary least-squares slope extraction.",
            'formula': '\\frac{\\partial T}{\\partial t} = \\frac{k}{\\rho c} \\left(\\frac{\\partial^2 T}{\\partial r^2} + \\frac{1}{r}\\frac{\\partial T}{\\partial r}\\right) \\quad \\text{(radial thermal conduction)}',
            'question': 'Why does the end of the solidification plateau often round off gradually rather than ending with a sharp corner in real experiments?',
            'answer': 'Because salol is a poor thermal conductor, solidification proceeds from the colder outer tube walls inward. The central liquid core around the thermometer freezes last, and sensible cooling begins at the perimeter before the core is completely solid, producing a rounded transition into the post-arrest cooling curve.'
        }
    ],
    'precautions': [
        'Ensure the salol crystals are melted completely in the warm water bath before placing the tube in the air jacket, eliminating all unmolten crystal seeds.',
        'Wipe the exterior of the boiling tube completely dry before inserting it into the air jacket to prevent erratic evaporative heat loss.',
        'Position the thermometer bulb centrally within the salol charge without allowing it to touch the glass walls or bottom of the tube.',
        'If significant supercooling occurs below 40 °C, touch the liquid gently with a tiny seed crystal on the stirrer wire to prompt immediate crystallization at 41.5 °C.'
    ],
    'quiz': [
        {
            'question': 'During the solidification arrest plateau of a pure crystalline substance, what happens to the temperature of the liquid-solid mixture?',
            'options': [
                'The temperature remains constant at the melting point T_m as latent heat is released.',
                'The temperature rises steadily as latent heat heats up the substance.',
                'The temperature drops exponentially according to Newton’s law of cooling.',
                'The temperature oscillates sinusoidally due to thermal expansion.'
            ],
            'correct': 0,
            'explanation': 'In a first-order phase transition, the liberation of latent heat of fusion exactly compensates for external heat loss, pinning the temperature of the coexisting liquid-solid mixture at the constant equilibrium melting point until crystallization is complete.'
        },
        {
            'question': 'When plotting total latent heat Q_latent = R_loss · Δt against mass m, what does the gradient of the best-fit line represent?',
            'options': [
                'The specific latent heat of fusion L_f of the substance (J kg⁻¹ or kJ kg⁻¹).',
                'The specific heat capacity of the liquid phase.',
                'The rate of heat loss R_loss to the surroundings.',
                'The equilibrium melting point temperature T_m.'
            ],
            'correct': 0,
            'explanation': 'Because Q_latent = m · L_f, plotting Q_latent against mass m gives a linear relationship whose slope S directly equals the specific latent heat of fusion L_f.'
        },
        {
            'question': 'What is the phenomenon where a liquid cools below its freezing point without solidifying called?',
            'options': [
                'Supercooling (or undercooling).',
                'Sublimation.',
                'Vitrification.',
                'Thermal expansion.'
            ],
            'correct': 0,
            'explanation': 'Supercooling occurs when a liquid cools below its equilibrium freezing temperature without crystallizing, caused by the free energy barrier required to form critical solid crystal nuclei.'
        },
        {
            'question': 'How does the cooling curve of an amorphous substance like paraffin wax differ from that of crystalline salol?',
            'options': [
                'Wax shows a continuous downward slope without a flat arrest plateau, whereas salol exhibits a sharp horizontal plateau.',
                'Wax displays multiple sharp arrest plateaus while salol has none.',
                'Wax maintains a constant temperature indefinitely without cooling.',
                'Wax cools along a straight horizontal line while salol cools vertically.'
            ],
            'correct': 0,
            'explanation': 'Amorphous substances lack a long-range crystalline lattice and have no definite melting point or latent heat of fusion, so their cooling curves slope continuously downward through a gradual softening range without a flat arrest plateau.'
        }
    ],
    'limitations': 'The teaching simulation models the phase change of pure phenyl salicylate (salol) with an ideal, flat solidification plateau at T_m = 41.50 °C under a calibrated steady heat loss rate R_loss = 270.0 J min⁻¹ (4.50 W) into an isothermal ambient air jacket. In physical laboratory practice, chemical impurities can depress the melting point and cause a slight slope on the plateau, supercooling may delay crystallization onset by several degrees if unseeded, radial temperature gradients across the viscous solid salol cause the termination of the plateau to round off gradually, and ambient room temperature drafts can induce small variations in the effective heat loss rate.',
    'modelExtra': 'The simulation evaluates the solidification plateau duration using the exact thermodynamic conservation relation Δt = (m · L_f) / R_loss, where m is the sample mass in kilograms, L_f = 79,500 J kg⁻¹ (79.50 kJ kg⁻¹) is the reference latent heat of fusion of salol, and R_loss = 270.0 J min⁻¹ (4.50 W) is the calibrated heat loss rate. Plateau durations are rounded to 0.01 min to model standard laboratory stopclock precision, and ordinary least-squares linear regression of Q_latent = R_loss · Δt against mass m provides the reported latent heat of fusion.'
}

# 1. Update experiments.json
exp_path = ROOT / 'content/physics/experiments.json'
experiments = json.loads(exp_path.read_text())
existing_idx = next((i for i, e in enumerate(experiments) if e['slug'] == 'solidification-cooling'), None)
if existing_idx is not None:
    experiments[existing_idx] = exp26
else:
    experiments.append(exp26)
exp_path.write_text(json.dumps(experiments, indent=2, ensure_ascii=False))
print(f'experiments.json updated. Total experiments: {len(experiments)}')

# 2. Update catalog.sqlite3
db_path = ROOT / 'data/catalog.sqlite3'
db = sqlite3.connect(db_path)
cur = db.cursor()
cur.execute('DELETE FROM experiments WHERE slug = ?', ('solidification-cooling',))
cur.execute('''
    INSERT INTO experiments (subject_id, slug, title, status, page_path, theory_path, report_path)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    1,
    'solidification-cooling',
    'Determination of latent heat of fusion by cooling curve',
    'live',
    '/physics/solidification-cooling/',
    '/physics/solidification-cooling/theory/',
    '/physics/solidification-cooling/report/'
))
db.commit()
db.close()
print('catalog.sqlite3 updated successfully for solidification-cooling.')
