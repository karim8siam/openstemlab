import json, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

exp28 = {
    'number': 28,
    'slug': 'latent-heat-fusion',
    'title': 'Determination of the Latent Heat of Fusion of Ice by the Method of Mixtures',
    'shortTitle': 'Latent Heat of Fusion of Ice',
    'aim': 'Determine the specific latent heat of fusion of ice (L_f) using the calorimetric method of mixtures, observing the temperature depression resulting from the melting of dried ice chips in warm water inside a calibrated copper calorimeter, and evaluating the thermal energy conservation balance with Rumford radiation compensation.',
    'target': 'L_f',
    'targetName': 'Latent heat of fusion L_f',
    'inputLabel': 'Mass of dry ice m_i',
    'shortInput': 'Ice mass m_i',
    'inputUnit': 'g',
    'inputDecimals': 1,
    'rawLabel': 'Equilibrium temperature T_f',
    'rawUnit': '°C',
    'rawDecimals': 2,
    'xAxis': 'Mass of dry ice m_i (kg)',
    'yAxis': 'Net latent heat absorbed Q_net (J)',
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
    'emptyY': [0.0, 15000.0],
    'timed': False,
    'angle': False,
    'published': True,
    'measureLabel': 'Measure final equilibrium temperature T_f for ice mass m_i',
    'fitEquation': 'Q_net = C_sys (T_0 − T_f) − m_i c_w T_f = m_i L_f ⇔ Y = L_f · X ⇔ L_f = S',
    'intro': "The solid-liquid phase transformation of water at 0 °C is a prototypical first-order thermodynamic transition characterized by a massive latent enthalpy absorption unaccompanied by any temperature variation. In hexagonal ice (ice Ih), water molecules are locked into an open, tetrahedral hydrogen-bonded crystal framework with a low packing density (ρ_ice ≈ 917 kg m⁻³). To break down this rigid lattice into the denser, mobile arrangement of liquid water (ρ_water ≈ 1,000 kg m⁻³), approximately 334 kilojoules of thermal energy must be absorbed per kilogram of ice melted: the specific latent heat of fusion L_f. In quantitative mixture calorimetry, ice chips at their equilibrium melting point (0.00 °C) are introduced into a known mass of warm water held within a calibrated copper calorimeter. As the ice melts, it absorbs latent heat Q_latent = m_i L_f to undergo isothermal phase change, while the resulting meltwater absorbs additional sensible heat Q_melt = m_i c_w (T_f − 0) to warm to the final mixture temperature T_f. Simultaneously, the warm water and calorimeter vessel cool from their initial temperature T_0 to T_f, releasing sensible heat Q_lost = C_sys (T_0 − T_f). Equating thermal loss to thermal gain yields the net latent heat relationship: Q_net = C_sys (T_0 − T_f) − m_i c_w T_f = m_i L_f. By varying the mass of ice added across serial runs and meticulously blotting each ice chip dry with filter paper immediately prior to immersion, ordinary least-squares regression of Q_net against m_i provides an exceptionally clean determination of L_f, while starting the warm water as far above room temperature as the final mixture drops below it eliminates net environmental radiation errors through Rumford compensation.",
    'settings': [
        'Dry melting ice chips at standard thermodynamic equilibrium temperature T_ice = 0.00 °C.',
        'Initial warm water mass m_w = 200.00 g; initial warm temperature T_0 = 30.00 °C (10.0 °C above ambient room temperature at 20.0 °C).',
        'Specularly polished copper calorimeter (mass 75.00 g, c_cu = 385.0 J kg⁻¹ K⁻¹); water equivalent W_cal = 28.88 J K⁻¹; C_sys = 866.08 J K⁻¹.',
        'Specific heat capacity of liquid water c_w = 4186.0 J kg⁻¹ K⁻¹; reference latent heat of fusion of ice L_f = 334.00 kJ kg⁻¹ (334,000 J kg⁻¹ = 79.82 cal g⁻¹).'
    ],
    'apparatus': [
        {
            'name': 'Insulated Jacketed Copper Calorimeter with Cork Supports',
            'purpose': 'A thin-walled specularly polished copper container (mass 75.0 g, volume 250 mL) supported on low-conductivity vulcanized cork pegs inside a concentric air jacket, sealed with a wooden lid featuring apertures for the thermometer and stirrer to minimize environmental heat exchange.'
        },
        {
            'name': 'Precision Immersion Calorimetric Thermometer (0.05°C Subdivisions)',
            'purpose': 'A sensitive mercury-in-glass thermometer graduated from 10 °C to 45 °C in 0.05 °C divisions, immersed centrally in the water bath to measure the initial warm temperature T_0 and track the cooling descent to the final equilibrium minimum T_f.'
        },
        {
            'name': 'Helical Brass Wire Loop Stirrer',
            'purpose': 'A low-thermal-mass brass wire stirrer formed into an open horizontal loop encircling the thermometer, used to gently circulate the water bath vertically to promote rapid melting and prevent thermal stratification.'
        },
        {
            'name': 'Ice Preparation Dish, Laboratory Tongs, and Absorbent Filter Paper',
            'purpose': 'A clean watch glass holding crushed melting ice chips, paired with laboratory tweezers and sheets of dry lint-free filter paper used to blot each ice fragment completely free of surface water film immediately before immersion.'
        }
    ],
    'procedure': [
        {
            'title': 'Calorimeter Tare and Warm Water Preparation',
            'text': 'Weigh the clean, dry copper calorimeter vessel together with its brass loop stirrer to ±0.01 g on an analytical balance. Add exactly 200.00 g of distilled water warmed to approximately 32 °C. Place the calorimeter inside the protective air jacket and seat the wooden lid firmly.',
            'why': 'Preparing the warm water near 30 °C to 32 °C ensures that after the ice melts, the final equilibrium temperature will fall roughly as far below room temperature (20 °C) as the initial water was above it, executing Rumford radiation compensation.'
        },
        {
            'title': 'Ice Crushing, Melting Point Stabilization, and Drying',
            'text': 'Crush clean, clear ice into small fragments (approximately pea to hazelnut size). Place the ice in a funnel or watch glass and allow it to drain until melting commences freely, establishing a true equilibrium ice-water mixture at 0.00 °C. Spread several dry filter paper sheets nearby.',
            'why': 'Small ice fragments possess a high surface-area-to-volume ratio, facilitating rapid dissolution and reducing the duration of environmental heat exchange. Allowing ice to begin melting confirms its temperature is strictly 0.00 °C rather than sub-zero freezer ice.'
        },
        {
            'title': 'Initial Warm Temperature Acquisition',
            'text': 'Insert the precision thermometer into the calorimeter water through the lid aperture. Agitate the bath with gentle vertical strokes of the stirrer until the temperature stabilizes. Record the steady initial warm temperature T_0 = 30.00 °C.',
            'why': 'Accurate initial temperature recording sets the exact thermal baseline from which the sensible heat release of the calorimeter and warm water is evaluated.'
        },
        {
            'title': 'Ice Blotting, Charge Addition, and Rapid Dissolution',
            'text': 'Take an ice chip with clean tongs, press it firmly between dry filter paper sheets to remove all adhering liquid water film, and drop it immediately into the calorimeter without splashing. Repeat swiftly until the target ice mass (e.g., 15.0 g) has been introduced, closing the lid immediately between additions.',
            'why': 'Thorough blotting is critical: any adhering liquid water is already melted and absorbs zero latent heat of fusion, which would cause an apparent deficit in the calculated latent heat value.'
        },
        {
            'title': 'Continuous Agitation and Equilibrium Temperature Tracking',
            'text': 'Stir the water bath continuously and smoothly with the helical stirrer, watching the thermometer meniscus through an optical magnifier. Track the temperature depression as the ice chips dissolve. Record the lowest stationary temperature attained before environmental re-warming begins as the equilibrium temperature T_f.',
            'why': 'Continuous stirring enforces thermal homogeneity, ensuring the thermometer bulb records the true bulk mixture temperature and identifies the exact moment of complete ice dissolution.'
        },
        {
            'title': 'Calorimeter Reweighing, Net Heat Computation, and Regression Analysis',
            'text': 'Remove the calorimeter vessel and reweigh it to ±0.01 g. Determine the exact mass of ice added m_i = m_final − m_initial. Repeat the measurement across five distinct ice charges (15.0 g, 20.0 g, 25.0 g, 30.0 g, and 35.0 g). For each run, compute Q_net = C_sys (T_0 − T_f) − m_i c_w T_f in joules. Plot Q_net against m_i (kg) and evaluate L_f from the slope of the regression line.',
            'why': 'Gravimetric reweighing provides an exact record of the dissolved ice mass, while regression across multiple charges eliminates single-trial timing and weighing anomalies.'
        }
    ],
    'topics': [
        {
            'title': 'Crystal Structure of Ice Ih and Hydrogen Bonding Energetics',
            'text': "Under standard terrestrial pressure, water crystallizes into hexagonal ice (ice Ih), a structure governed by the directional nature of sp³-hybridized oxygen orbitals. Each oxygen atom is situated at the center of a regular tetrahedron, covalently bonded to two hydrogen atoms (O–H bond length ~0.96 Å) and hydrogen-bonded to two neighboring water molecules (O···H distance ~1.76 Å, O···O separation ~2.76 Å). This geometry enforces the Pauling-Bernal-Fowler 'ice rules', creating a hexagonal honeycomb lattice with large hexagonal channels, resulting in a low density of 916.8 kg m⁻³ at 0 °C. The energy required to melt ice into liquid water—the specific latent heat of fusion L_f = 334.0 kJ kg⁻¹ (6.01 kJ mol⁻¹)—represents the enthalpy necessary to disrupt approximately 10% to 15% of these rigid intermolecular hydrogen bonds, collapsing the open crystalline scaffolding into a denser, fluid network of transient hydrogen-bonded clusters (ρ_water = 999.8 kg m⁻³ at 0 °C). The negative volume change upon melting (Δv_fusion = v_liquid − v_solid = −0.0905 cm³ g⁻¹) is an anomalous physical property shared by very few substances, directly explaining why ice floats on water and why increasing pressure lowers the melting point according to the Clapeyron relation.",
            'formula': 'L_f = \\Delta h_{\\text{fusion}} = 3.340 \\times 10^5 \\text{ J kg}^{-1} \\quad (6.01 \\text{ kJ mol}^{-1}) \\quad \\text{and} \\quad \\Delta v_{\\text{fusion}} < 0',
            'question': 'Why is ice less dense than liquid water, and how does this relate to the energy absorbed during melting?',
            'answer': 'Ice has an open, tetrahedral crystalline lattice held by rigid hydrogen bonds, creating large empty hexagonal channels. During melting, latent heat breaks enough hydrogen bonds to collapse this open structure into a denser, disordered liquid network, which is why ice floats on water.'
        },
        {
            'title': 'The Clapeyron Equation and Pressure Depression of Freezing Point (Regelation)',
            'text': "The thermodynamic equilibrium between solid ice and liquid water is quantified by the Clapeyron equation: dP/dT = L_f / [T_m (v_L − v_S)], where T_m is the absolute melting temperature, L_f is the specific latent heat of fusion, and v_L, v_S are the specific volumes of liquid and solid respectively. For water at 0 °C (273.15 K), v_L = 1.0001 × 10⁻³ m³ kg⁻¹ while v_S = 1.0908 × 10⁻³ m³ kg⁻¹, giving a negative specific volume change: Δv = v_L − v_S = −9.07 × 10⁻⁵ m³ kg⁻¹. Substituting these values yields the pressure slope: dP/dT = 334,000 / [273.15 × (−9.07 × 10⁻⁵)] = −1.348 × 10⁷ Pa K⁻¹ = −133 atm K⁻¹. Taking the reciprocal reveals that an applied pressure increase of 133 atmospheres lowers the equilibrium melting point of ice by exactly 1.00 °C (dT_m/dP = −0.0075 °C atm⁻¹). This negative slope underlies the fascinating physical phenomenon of regelation: when a thin wire supporting heavy weights is draped across a block of ice, the intense pressure beneath the wire depresses the melting point below 0 °C, melting the ice beneath it; as the meltwater slips around the wire to the low-pressure region above, it refreezes immediately, allowing the wire to traverse through the solid block without cleaving it in two.",
            'formula': '\\frac{dT_m}{dP} = \\frac{T_m (\\nu_L - \\nu_S)}{L_f} \\approx -0.00751 \\, ^\\circ\\text{C atm}^{-1} = -7.41 \\times 10^{-8} \\text{ K Pa}^{-1}',
            'question': 'How does an increase in mechanical pressure affect the melting point of ice, and why?',
            'answer': 'Increasing pressure lowers the melting point of ice (by approx. 0.0075 °C per atmosphere). According to the Clapeyron equation and Le Chatelier’s principle, because liquid water is denser than solid ice, applying pressure favors the phase that occupies smaller volume, driving the transition toward the liquid state.'
        },
        {
            'title': 'The Method of Mixtures: Energy Conservation and Sensible Heat Partitions',
            'text': "The method of mixtures applied to ice calorimetry is founded upon the first law of thermodynamics for an adiabatic control volume: Σ Q_absorbed = Σ Q_released. When a mass m_i of pure ice at 0 °C is submerged in a copper calorimeter containing mass m_w of water at initial warm temperature T_0, heat transfer proceeds along two parallel thermodynamic paths: (1) Heat lost by the system: the warm water and calorimeter vessel cool from T_0 to the final equilibrium temperature T_f, releasing sensible heat Q_lost = (m_w c_w + W_cal) (T_0 − T_f) = C_sys (T_0 − T_f); (2) Heat gained by the ice: the ice absorbs latent heat of fusion at 0 °C to transition into liquid meltwater, Q_latent = m_i L_f, and this cold meltwater then warms sensibly from 0 °C to T_f, absorbing Q_sens = m_i c_w (T_f − 0) = m_i c_w T_f. Equating these two energy terms yields: m_i L_f + m_i c_w T_f = C_sys (T_0 − T_f). Subtracting the sensible warming term m_i c_w T_f from the total heat lost isolates the net latent heat of transformation: Q_net = C_sys (T_0 − T_f) − m_i c_w T_f = m_i L_f. Plotting Q_net against m_i across multiple experimental trials forms a straight line passing through the origin with slope S = L_f.",
            'formula': 'm_i L_f + m_i c_w T_f = C_{\\text{sys}} (T_0 - T_f) \\iff Q_{\\text{net}} = m_i L_f',
            'question': 'What are the two components of thermal energy absorbed by ice added to warm water in a calorimeter?',
            'answer': 'First, the latent heat of fusion absorbed isothermally to melt the ice from solid to liquid at 0 °C (Q = mi Lf). Second, the sensible heat absorbed to warm the resulting meltwater from 0 °C up to the final equilibrium temperature Tf (Q = mi cw Tf).'
        },
        {
            'title': 'The Problem of Wet Ice and the Critical Role of Surface Blotting',
            'text': "The preeminent source of systematic error in ice calorimetry is the presence of adhering surface liquid moisture on the ice chips, commonly termed 'wet ice'. In an ice-water mixture at 0 °C, the ice fragments are bathed in a thin film of melted water. If an unblotted ice chip is transferred into the calorimeter, the adhering liquid film contributes directly to the measured mass m_i upon gravimetric weighing, but because it is already liquid, it absorbs zero latent heat of fusion. It only absorbs sensible heat as it warms from 0 °C to T_f. If the ice carries a liquid moisture fraction w = m_liquid / m_total, the apparent latent heat extracted from the mixture equation is severely depressed: L_f,apparent = (1 − w) L_f,true. For instance, a moisture film representing just 5% of the total chip mass causes an apparent latent heat deficit of approximately 16.7 kJ kg⁻¹ (depressing the result from 334 kJ kg⁻¹ down to ~317 kJ kg⁻¹). To eliminate this defect, every ice chip must be lifted with tweezers, pressed firmly between multiple layers of dry, absorbent filter paper until its surface turns matte and frosty, and dropped instantly into the calorimeter.",
            'formula': 'L_{f,\\text{apparent}} = (1 - w) L_{f,\\text{true}} \\quad \\text{where } w = \\frac{m_{\\text{surface liquid}}}{m_{\\text{total}}}',
            'question': 'How does water adhering to the surface of ice chips affect the experimental result for latent heat of fusion?',
            'answer': 'Surface water is already melted, so it absorbs no latent heat of fusion (only sensible heat). However, it adds to the measured mass of ice upon weighing. Consequently, the apparent heat absorbed per gram is falsely low, leading to a substantial systematic underestimation of Lf.'
        },
        {
            'title': 'Sub-Zero Freezer Ice vs. Melting Ice Equilibrium',
            'text': "A complementary thermometric error occurs if ice is taken directly from a sub-zero freezer (typically operating at −15 °C to −20 °C) without allowing it to reach equilibrium with meltwater. If ice at temperature T_ice < 0 °C is introduced into the calorimeter, it must first absorb sensible heat to warm from T_ice up to 0 °C before melting can commence: Q_sub = m_i c_ice (0 − T_ice) = m_i c_ice |T_ice|, where c_ice ≈ 2,090 J kg⁻¹ K⁻¹ is the specific heat capacity of solid ice. If this sensible pre-warming enthalpy is unmodelled in the mixture equation, the extra cooling is erroneously attributed to latent heat, causing the calculated value L_f,apparent = L_f,true + c_ice |T_ice| to be systematically inflated (by approximately 2.09 kJ kg⁻¹ per degree Celsius below zero). To guarantee that T_ice is strictly 0.00 °C, laboratory ice must be removed from the freezer well before the experiment, crushed into small pieces, and allowed to stand in a draining perforated funnel until water drips steadily from the melting mass, establishing unambiguous solid-liquid coexistence at 0.00 °C.",
            'formula': 'L_{f,\\text{apparent}} = L_{f,\\text{true}} + c_{\\text{ice}} |T_{\\text{ice}}| \\quad \\text{if } T_{\\text{ice}} < 0 \\, ^\\circ\\text{C} \\quad (c_{\\text{ice}} \\approx 2090 \\text{ J kg}^{-1} \\text{ K}^{-1})',
            'question': 'Why should ice taken directly from a deep freezer not be used immediately in a latent heat experiment?',
            'answer': 'Freezer ice is below 0 °C (often −15 °C to −20 °C). It absorbs sensible heat warming up to 0 °C before melting. If unmodelled, this extra heat absorption is mistaken for latent heat, causing the calculated latent heat of fusion to be systematically overestimated.'
        },
        {
            'title': "Rumford's Compensation and Newton's Cooling Corrections",
            'text': "During the 3 to 6 minutes required for ice to melt completely inside the calorimeter, heat exchange with the ambient laboratory room (at temperature T_room ≈ 20.0 °C) occurs through radiation and convection. Sir Benjamin Thompson, Count Rumford, demonstrated that choosing the initial warm water temperature T_0 symmetrically above ambient cancels this environmental heat transfer to first order. Specifically, if the warm water is prepared at T_0 = 30.0 °C (10 °C above T_room) and sufficient ice is added so that the final equilibrium temperature reaches approximately T_f = 10.0 °C (10 °C below T_room), the temperature difference (T − T_room) changes sign symmetrically across the midpoint of the cooling trajectory. In accordance with Newton's cooling law (dQ/dt = −k C_sys (T − T_room)), the calorimeter loses thermal energy to the room during the upper half of the run (when T > T_room) and gains an almost identical amount of heat from the room during the lower half (when T < T_room). The integral of environmental exchange vanishes: ∫ dQ_env dt ≈ 0. This elegant experimental design eliminates the need for complex graphical cooling corrections.",
            'formula': '(T_0 - T_{\\text{room}}) \\approx (T_{\\text{room}} - T_f) \\implies \\int_0^{t_{\\text{melt}}} \\frac{dQ_{\\text{env}}}{dt} dt \\approx 0',
            'question': 'How does Rumford’s method cancel heat exchange with the room during ice calorimetry?',
            'answer': 'By arranging for the water to start as many degrees above room temperature as it finishes below room temperature. The heat lost to the room while the vessel is warm is canceled by the heat absorbed from the room while the vessel is cold, producing zero net environmental heat exchange.'
        },
        {
            'title': 'Thermal Capacity of the Jacketed Calorimeter System C_sys',
            'text': "The thermal capacity C_sys represents the total quantity of thermal energy required to alter the temperature of the calorimeter vessel, stirrer, and initial water bath by one kelvin. For an open vessel, thermal capacity is evaluated as C_sys = m_w c_w + m_cal c_cu + m_stir c_brass. In our standardized university apparatus, the calorimeter container is spun from pure copper (mass m_cal = 75.00 g, specific heat c_cu = 385.0 J kg⁻¹ K⁻¹), yielding a vessel heat capacity of C_cal = 0.075 kg × 385.0 J kg⁻¹ K⁻¹ = 28.875 J K⁻¹. The brass wire loop stirrer (mass 15.0 g, specific heat c_brass = 380.0 J kg⁻¹ K⁻¹) and immersed thermometer bulb contribute an additional ~5.70 J K⁻¹, giving an aggregate water equivalent of W_cal = 28.88 J K⁻¹ (equivalent to 6.90 g of water). When filled with 200.00 g of distilled water (heat capacity C_w = 0.200 kg × 4,186 J kg⁻¹ K⁻¹ = 837.20 J K⁻¹), the aggregate system thermal capacity evaluates to C_sys = 837.20 + 28.88 = 866.08 J K⁻¹. Multiplying C_sys by the observed temperature drop (T_0 − T_f) quantifies the total sensible thermal energy released by the apparatus to melt the ice and warm the meltwater.",
            'formula': 'C_{\\text{sys}} = m_w c_w + m_{\\text{cal}} c_{\\text{cu}} + W_{\\text{stir}} = 866.08 \\text{ J K}^{-1} \\quad \\text{and} \\quad W_{\\text{cal}} = 28.88 \\text{ J K}^{-1}',
            'question': 'Why must the water equivalent of the calorimeter be included in the energy balance of the experiment?',
            'answer': 'Because the copper vessel and brass stirrer cool alongside the warm water through the identical temperature decrease (T0 − Tf), releasing sensible heat that contributes to melting the ice. Neglecting the calorimeter metal would systematically underestimate the total heat supplied.'
        }
    ],
    'precautions': [
        'Blot each ice chip thoroughly between dry filter paper sheets immediately before dropping it into the calorimeter to eliminate all adhering liquid moisture.',
        'Use melting ice chips that are visibly dripping with water at 0 °C rather than sub-zero ice taken directly from a freezer.',
        'Stir the water bath continuously and gently with the helical stirrer to accelerate dissolution and prevent cold water layers from settling at the bottom.',
        'Ensure that no water splashes out of the calorimeter when adding ice chips, as splashed water alters both the heat capacity and the final mass.'
    ],
    'quiz': [
        {
            'question': 'In the method of mixtures for determining the latent heat of fusion of ice, how is the net latent heat Q_net calculated?',
            'options': [
                'Q_net = C_sys (T_0 − T_f) − m_i c_w T_f',
                'Q_net = C_sys (T_0 − T_f) + m_i c_w T_f',
                'Q_net = m_i c_w (T_0 − T_f)',
                'Q_net = C_sys T_0 / m_i'
            ],
            'correct': 0,
            'explanation': 'The total sensible heat lost by the calorimeter and warm water is C_sys (T_0 − T_f). Subtracting the sensible heat absorbed to warm the meltwater from 0 °C to T_f (m_i c_w T_f) isolates the net latent heat absorbed during the melting phase change: Q_net = C_sys (T_0 − T_f) − m_i c_w T_f = m_i L_f.'
        },
        {
            'question': 'What is the consequence of failing to dry the ice chips with filter paper before adding them to the calorimeter?',
            'options': [
                'The calculated latent heat of fusion L_f will be systematically too low.',
                'The calculated latent heat of fusion L_f will be systematically too high.',
                'The equilibrium temperature T_f will drop below 0 °C.',
                'The specific heat of water will appear to increase.'
            ],
            'correct': 0,
            'explanation': 'Liquid water adhering to ice is already melted and absorbs no latent heat of fusion, but it adds to the measured ice mass m_i upon weighing. Consequently, the apparent heat absorbed per gram is reduced, systematically underestimating L_f.'
        },
        {
            'question': 'Why is ice at standard pressure less dense than liquid water at 0 °C?',
            'options': [
                'The tetrahedral hydrogen-bonded crystal lattice of ice Ih encloses open hexagonal channels.',
                'Air molecules are trapped inside the chemical formula of ice.',
                'Liquid water expands when heated above 4 °C.',
                'Ice molecules vibrate at a higher frequency than liquid molecules.'
            ],
            'correct': 0,
            'explanation': 'Ice Ih has an open hexagonal crystal lattice held by directional hydrogen bonds, creating large hexagonal cavities that result in a lower density (917 kg/m³) than liquid water (1,000 kg/m³).'
        },
        {
            'question': 'When plotting Q_net on the vertical axis against the mass of dry ice m_i on the horizontal axis, what does the gradient of the best-fit line represent?',
            'options': [
                'The specific latent heat of fusion of ice L_f (J kg⁻¹ or kJ kg⁻¹).',
                'The specific heat capacity of liquid water c_w.',
                'The initial warm water temperature T_0.',
                'The rate of heat loss to the ambient room.'
            ],
            'correct': 0,
            'explanation': 'Because Q_net = m_i · L_f, plotting Q_net against m_i yields a straight line whose slope S directly equals the specific latent heat of fusion L_f.'
        }
    ],
    'limitations': 'The teaching simulation models the melting of pure ice under ideal thermal conditions with constant initial warm water temperature T_0 = 30.00 °C, ice temperature T_ice = 0.00 °C, and an invariant system heat capacity C_sys = 866.08 J K⁻¹. In physical experiments, residual surface water film adhering to ice chips can cause negative systematic errors, using freezer ice below 0 °C causes positive errors, water splashing during ice transfer reduces the effective mass, evaporation from the warm surface during dissolution introduces unmodelled cooling, and small departures from symmetric Rumford compensation leave residual radiation exchanges with the room.',
    'modelExtra': 'The simulation evaluates equilibrium temperatures using the exact thermodynamic conservation relation T_f = (C_sys T_0 − m_i L_f) / (C_sys + m_i c_w), where m_i is the dry ice mass in kilograms, L_f = 334,000 J kg⁻¹ (334.00 kJ kg⁻¹) is the reference latent heat of fusion of ice, c_w = 4,186 J kg⁻¹ K⁻¹ is the specific heat capacity of water, T_0 = 30.00 °C is the initial warm water temperature, and C_sys = 866.08 J K⁻¹ is the aggregate thermal capacity. Equilibrium temperatures are rounded to 0.01 °C to simulate precision calorimetric thermometry, and ordinary least-squares regression of Q_net against m_i yields the reported latent heat of fusion.'
}

# 1. Update experiments.json
exp_path = ROOT / 'content/physics/experiments.json'
experiments = json.loads(exp_path.read_text())
existing_idx = next((i for i, e in enumerate(experiments) if e['slug'] == 'latent-heat-fusion'), None)
if existing_idx is not None:
    experiments[existing_idx] = exp28
else:
    experiments.append(exp28)
exp_path.write_text(json.dumps(experiments, indent=2, ensure_ascii=False))
print(f'experiments.json updated. Total experiments: {len(experiments)}')

# 2. Update catalog.sqlite3
db_path = ROOT / 'data/catalog.sqlite3'
db = sqlite3.connect(db_path)
cur = db.cursor()
cur.execute('DELETE FROM experiments WHERE slug = ?', ('latent-heat-fusion',))
cur.execute('''
    INSERT INTO experiments (subject_id, slug, title, status, page_path, theory_path, report_path)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    1,
    'latent-heat-fusion',
    'Determination of latent heat of fusion of ice',
    'live',
    '/physics/latent-heat-fusion/',
    '/physics/latent-heat-fusion/theory/',
    '/physics/latent-heat-fusion/report/'
))
db.commit()
db.close()
print('catalog.sqlite3 updated successfully for latent-heat-fusion.')
