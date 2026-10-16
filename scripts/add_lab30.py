import json, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

exp30 = {
    'number': 30,
    'slug': 'mechanical-equivalent-heat',
    'title': 'Determination of the Mechanical Equivalent of Heat (Joule’s Constant) by Friction Calorimetry',
    'shortTitle': 'Mechanical Equivalent of Heat',
    'aim': 'Determine Joule’s mechanical equivalent of heat (J) using a rotating friction calorimeter with suspended load and revolution counter, measuring the mechanical work done against friction (W) and the corresponding thermal heat absorbed (Q) by the calorimeter water system.',
    'target': 'J',
    'targetName': 'Mechanical equivalent of heat J',
    'inputLabel': 'Revolutions N',
    'shortInput': 'Rotations N',
    'inputUnit': 'rev',
    'inputDecimals': 0,
    'rawLabel': 'Final temperature T_f',
    'rawUnit': '°C',
    'rawDecimals': 2,
    'xAxis': 'Heat absorbed Q (cal)',
    'yAxis': 'Mechanical work W (J)',
    'xScale': 1.0,
    'yScale': 1.0,
    'gradientUnit': 'J cal⁻¹',
    'resultUnit': 'J cal⁻¹',
    'resultScale': 1.0,
    'resultDecimals': 3,
    'min': 100.0,
    'max': 1200.0,
    'step': 100.0,
    'initial': 600.0,
    'samples': [200.0, 400.0, 600.0, 800.0, 1000.0],
    'emptyX': [0.0, 2500.0],
    'emptyY': [0.0, 10000.0],
    'timed': False,
    'angle': False,
    'published': True,
    'measureLabel': 'Measure final equilibrium temperature T_f after N friction revolutions',
    'fitEquation': 'W = 2π r M_load g N = J · C_sys (T_f − T_0) = J · Q ⇔ Y = J · X ⇔ J = S',
    'intro': "The establishment of the mechanical equivalent of heat represents one of the monumental conceptual revolutions in nineteenth-century physics, dismantling Antoine Lavoisier's caloric theory—which treated heat as an indestructible, weightless fluid conserved in all physical processes—and laying the cornerstone for the first law of thermodynamics. In 1798, Benjamin Thompson (Count Rumford) observed during the boring of brass cannons in Munich that a dull drill bit produced an inexhaustible quantity of heat as long as horses continued to turn the shaft, concluding that heat could not be a material substance but was a mode of microscopic motion excited by mechanical work. Between 1843 and 1850, James Prescott Joule performed a landmark series of quantitative experiments—measuring the temperature rise of water agitated by falling-weight paddle wheels, fluid friction in mercury, and electrical dissipation in resistive coils—demonstrating that regardless of the mechanism, the expenditure of a fixed quantity of mechanical work W always produces a strictly proportional quantity of thermal energy Q: W = J · Q, where J is Joule's mechanical equivalent of heat. In the classic Callendar and Rowland friction calorimeter apparatus, a hollow copper cylinder of radius r containing a known mass of water is rotated continuously about its horizontal axis. A flexible woven friction belt is wrapped around the drum; one end supports a suspended load M_load, while the opposite end is restrained by a light spring balance. When rotated at steady speed, the frictional torque exerted by the drum lifts the suspended weight until it floats freely in dynamic equilibrium, while the mechanical work dissipated against sliding friction is completely absorbed by the drum and water. For N complete rotations, the relative sliding distance traversed by the drum surface beneath the belt is s = 2π r N, giving a mechanical work input of W = 2π r M_load g N (in joules). The heat absorbed by the calorimeter and water is evaluated as Q = C_sys (T_f − T_0) (in calories), where C_sys is the aggregate heat capacity of the water and vessel metal. Ordinary least-squares regression of W against Q across serial revolution settings yields an exceptionally robust measurement of Joule's constant J ≈ 4.186 J cal⁻¹.",
    'settings': [
        'Cylindrical copper friction drum (outer radius r = 0.0500 m, mass m_cal = 200.00 g, c_cu = 0.0924 cal g⁻¹ K⁻¹; water equivalent W_cal = 18.48 g).',
        'Distilled water charge m_w = 100.00 g (water equivalent 100.00 g); aggregate calorimeter system capacity C_sys = 118.48 cal K⁻¹ (495.96 J K⁻¹).',
        'Suspended counter-load mass M_load = 3.000 kg suspended by a flexible canvas friction belt wrapped 1.5 turns over the drum.',
        'Initial baseline ambient and calorimeter temperature T_0 = 20.00 °C; local gravitational acceleration g = 9.80665 m s⁻².',
        'Reference mechanical equivalent of heat: J = 4.1860 J cal⁻¹ (4186.0 J kcal⁻¹ = 4.1860 kJ kcal⁻¹).'
    ],
    'apparatus': [
        {
            'name': 'Precision Rotating Friction Drum Calorimeter with Mechanical Drive',
            'purpose': 'A thin-walled, specularly turned electrolytic copper cylinder (outer diameter 100.0 mm, radius 50.0 mm) mounted upon a low-friction horizontal axle with thermal insulating phenolic couplings, driven at steady rotational speeds (100–200 RPM) by a variable-speed motor or geared hand crank.'
        },
        {
            'name': 'Calibrated Canvas Friction Belt with Suspended Counter-Load and Spring Balance',
            'purpose': 'A wide, flexible woven friction band wrapped 1.5 turns around the circumference of the drum, supporting a calibrated suspended load mass (M_load = 3.000 kg) on the descending side and anchored through an adjustable helical spring balance (measuring back-tension T_2) on the ascending side to maintain steady floating equilibrium.'
        },
        {
            'name': 'Mechanical Digital Revolution Counter',
            'purpose': 'A precision five-digit mechanical cyclometer directly geared to the rotating drum drive shaft to record the exact total number of revolutions N traversed during each experimental run with single-rotation resolution.'
        },
        {
            'name': 'Calibrated Precision Immersion Thermometer (0.05°C Subdivisions)',
            'purpose': 'A sensitive mercury-in-glass thermometer graduated from 15 °C to 45 °C in 0.05 °C increments, inserted axially into the hollow interior of the drum through a water-tight seal to monitor water temperature before and after friction cycling.'
        }
    ],
    'procedure': [
        {
            'title': 'Calorimeter Drum Tare and Water Mass Charge',
            'text': 'Weigh the clean, dry copper drum to ±0.01 g on a laboratory analytical balance, recording its empty mass m_cal = 200.00 g. Add exactly 100.00 g of distilled water at room temperature. Seal the drum cap securely and remeasure the total mass to confirm the water charge.',
            'why': 'Exact gravimetric measurement of the copper drum and water mass is essential to evaluate the total thermal heat capacity C_sys = m_w + W_cal in calories per kelvin.'
        },
        {
            'title': 'Friction Belt Rigging and Drum Installation',
            'text': 'Mount the filled drum onto the insulated drive axle. Wrap the woven friction belt 1.5 times around the copper drum circumference. Attach the 3.000 kg load mass to the free hanging tail and hook the opposing end to the upper spring balance. Verify that the belt tracks centrally without wandering off the drum edges.',
            'why': 'Proper belt alignment ensures uniform interfacial contact pressure and prevents edge-rubbing against stationary frame components.'
        },
        {
            'title': 'Baseline Temperature Recording and Counter Reset',
            'text': 'Insert the precision thermometer axially into the drum cavity. Rotate the drum slowly by hand for several turns to mix the internal water, allow the reading to stabilize, and record the initial baseline temperature T_0 = 20.00 °C. Reset the mechanical revolution counter to 00000.',
            'why': 'Establishing a uniform baseline temperature guarantees that all subsequent thermal elevation originates exclusively from friction work during the timed run.'
        },
        {
            'title': 'Rotational Friction Cycling and Steady Floating Balance',
            'text': 'Start the drive motor or turn the hand crank smoothly, accelerating the drum to a steady speed of approximately 120 to 150 RPM. Observe that the friction between the spinning drum and belt lifts the 3.000 kg load slightly off the bench rest so that it floats in free dynamic equilibrium. Monitor the small residual tension T_2 on the spring balance.',
            'why': 'Floating equilibrium confirms that the net tangential frictional force acting on the drum surface is exactly equal to the suspended weight F_f = M_load · g − T_2.'
        },
        {
            'title': 'Target Revolution Completion and Peak Temperature Acquisition',
            'text': 'Continue rotating smoothly until the target number of revolutions N is attained (e.g., N = 200 revs). Immediately halt the rotation, disengage the belt, and gently agitate the water inside the drum by rocking the axle. Watch the thermometer meniscus rise through an optical magnifier and record the maximum equilibrium temperature T_f attained before cooling commences.',
            'why': 'Recording the maximum temperature after thorough internal mixing captures the true adiabatic thermal plateau before environmental radiation dissipation occurs.'
        },
        {
            'title': 'Multi-Station Revolution Acquisition and Linear Regression Analysis',
            'text': 'Allow the drum to cool back to ambient baseline temperature. Repeat the measurement across five distinct revolution settings (N = 200, 400, 600, 800, and 1000 revolutions). For each run, compute the mechanical work W = 2π r M_load g N in joules and the heat absorbed Q = C_sys (T_f − T_0) in calories. Plot W against Q and determine Joule’s constant J from the slope of the regression line.',
            'why': 'Linear regression over multiple revolution settings eliminates single-trial zero offsets and provides a statistically rigorous determination of the mechanical equivalent of heat.'
        }
    ],
    'topics': [
        {
            'title': 'The Downfall of the Caloric Theory and Rumford’s Cannon-Boring Experiments',
            'text': "Throughout the eighteenth century, thermal physics was dominated by the caloric theory pioneered by Antoine Lavoisier and Joseph Black. Caloric was conceived as an elastic, weightless, self-repulsive fluid that permeated all matter, flowing spontaneously from warmer bodies to colder ones. In this framework, heat absorbed or released during physical processes was simply caloric changing its spatial concentration, and friction was explained as mechanical rubbing 'squeezing out' caloric from the interstices between metal particles, akin to squeezing water from a sponge. In 1798, Benjamin Thompson, Count Rumford, delivered a fatal experimental blow to this concept while supervising the boring of brass cannons at the military arsenal in Munich. Rumford submerged a cannon cylinder and a dull boring tool inside a wooden box containing 18.75 pounds of cold water. Driven by two horses, the blunt borer rubbed continuously against the brass bottom without cutting away any metal shavings. Within thirty minutes, the water warmed noticeably, and after two and a half hours, the water boiled vigorously. Rumford pointed out that the supply of heat was entirely inexhaustible as long as mechanical rotation was maintained. Because a finite quantity of brass could not possess an infinite store of caloric fluid, Rumford reasoned that heat could not be a material substance; it had to be a form of microscopic mechanical motion excited by the macroscopic work done by the horses.",
            'formula': '\\text{Caloric Fluid Theory (Lavoisier)} \\implies \\Delta Q = 0 \\quad \\text{vs.} \\quad \\text{Kinetic Heat Theory (Rumford)} \\implies W \\to Q \\quad (\\text{Inexhaustible})',
            'question': 'How did Count Rumford’s cannon-boring experiments disprove the caloric theory of heat?',
            'answer': 'Rumford showed that a blunt boring tool rubbing against brass generated an inexhaustible, continuous supply of heat that boiled gallons of water without producing metal chips. Because a finite mass of brass could not contain an infinite amount of caloric fluid, heat could not be a material substance; it had to be a mode of motion generated by mechanical work.'
        },
        {
            'title': 'The First Law of Thermodynamics and Joule’s Principle of Equivalence',
            'text': "Between 1843 and 1850, the English physicist James Prescott Joule placed the kinetic nature of heat on an exact mathematical and experimental foundation. Using a falling-weight apparatus that drove a set of brass paddle wheels inside an insulated copper container filled with water, Joule measured the mechanical work performed by the descending weights (W = M g h) and the resulting temperature rise ΔT of the water. Over hundreds of meticulous trials, Joule established the principle of mechanical equivalence: whenever mechanical work is dissipated in a closed system to produce thermal effects, the ratio of mechanical work expended to thermal heat absorbed is an invariant universal physical constant: J = W / Q. This empirical equivalence led directly to Rudolf Clausius's and William Thomson's (Lord Kelvin's) mathematical formulation of the First Law of Thermodynamics: for any thermodynamic system, energy is conserved, and heat Q and work W are two mutually convertible forms of energy transfer across the system boundary: ΔU = Q − W (in modern SI notation where both are measured in joules). Historically, because thermal energy was quantified using the calorie (the heat required to raise 1 g of water by 1 °C), Joule’s constant J served as the conversion factor between mechanical units (foot-pounds, ergs, or joules) and thermal units (calories). In modern SI, Joule’s constant is recognized as the conversion factor J = 4.1860 J cal⁻¹ (or 4186 J kcal⁻¹).",
            'formula': 'W = J \\cdot Q \\iff J = \\frac{W}{Q} \\approx 4.1860 \\text{ J cal}^{-1} \\quad \\text{and} \\quad \\Delta U = Q - W',
            'question': 'What is the physical significance of Joule’s constant J in the context of the first law of thermodynamics?',
            'answer': 'Joule’s constant J represents the mechanical equivalent of heat—the conversion factor relating mechanical work (in joules) to thermal energy (in calories). It demonstrated that heat is a form of energy, establishing the First Law of Thermodynamics (energy conservation).'
        },
        {
            'title': 'The Callendar and Rowland Friction Calorimeter Mechanics',
            'text': "In 1879, Henry Rowland improved upon Joule's paddle-wheel method by introducing continuous mechanical rotation of a calorimeter drum, later refined into the elegant bench apparatus devised by Hugh Longbourne Callendar. The apparatus consists of a thin-walled copper drum of outer radius r mounted horizontally and driven at a constant angular velocity ω. A flexible woven belt is wrapped around the drum circumference, carrying a heavy suspended load of mass M_load on the downward-running side, while the upward-running side is connected to a light spring balance. When the drum rotates, kinetic friction between the rotating drum surface and the stationary belt produces a tangential frictional traction force F_f. By adjusting the rotational speed, the student achieves a dynamic equilibrium state where the suspended weight is lifted slightly off the bench rest and hovers steadily in mid-air. In this floating state, the downward gravitational force M_load g is balanced by the upward frictional traction plus the small spring tension T_2: F_f = M_load g − T_2. For a drum rotating through N complete cycles, the peripheral contact surface moves through a linear distance s = 2π r N. The total mechanical work dissipated against sliding friction is therefore: W = F_f · s = (M_load g − T_2) · 2π r N = τ · (2π N), where τ = F_f r is the frictional torque exerted by the drum. If the spring tension T_2 is made negligible (or subtracted explicitly), W = 2π r M_load g N.",
            'formula': 'W = F_f \\cdot s = (M_{\\text{load}} g - T_2) \\cdot 2\\pi r N = \\tau \\cdot (2\\pi N) \\quad \\text{where } s = 2\\pi r N',
            'question': 'How is the mechanical work calculated in the Callendar rotating drum friction calorimeter?',
            'answer': 'The work is calculated as the product of the net frictional force (F = M_load g − T_spring) and the total distance traversed by the drum surface (s = 2π r N): W = (M_load g − T_spring) · 2π r N = τ · (2π N).'
        },
        {
            'title': 'Belt Friction Mechanics and the Capstan Equation',
            'text': "The mechanical equilibrium of the flexible friction belt wrapped around the rotating cylinder is governed by Euler's capstan (or belt friction) equation: T_1 / T_2 = exp(μ θ), where T_1 is the tension on the tight side (supporting the hanging load M_load g), T_2 is the tension on the slack side (the spring balance), μ is the coefficient of kinetic friction between the canvas belt and copper drum, and θ is the total angular wrap in radians. For a belt wrapped 1.5 complete turns around the drum, the wrap angle is θ = 1.5 × 2π = 3π radians ≈ 9.42 rad. If the kinetic friction coefficient between woven canvas and smooth copper is μ ≈ 0.25, the exponential amplification factor evaluates to exp(0.25 × 3π) = exp(2.356) ≈ 10.55. Consequently, the tension T_1 on the load side is over ten times larger than the tension T_2 on the spring balance: T_2 = T_1 / 10.55. For a hanging load of M_load = 3.00 kg (T_1 = 3.00 × 9.807 = 29.42 N), the spring balance experiences a counter-tension of only T_2 ≈ 2.79 N. The net effective frictional force driving thermal generation is F_f = T_1 − T_2 = 29.42 − 2.79 = 26.63 N. The capstan relation explains why a small holding force on the spring end can comfortably support and stabilize a heavy hanging weight without requiring massive clamping mechanisms.",
            'formula': '\\frac{T_1}{T_2} = e^{\\mu \\theta} \\implies T_2 = M_{\\text{load}} g \\, e^{-\\mu \\theta} \\quad \\text{and} \\quad F_f = T_1 - T_2 = M_{\\text{load}} g (1 - e^{-\\mu \\theta})',
            'question': 'What does the capstan equation describe in the context of the friction calorimeter belt?',
            'answer': 'The capstan equation T1/T2 = exp(μθ) describes how tension increases exponentially around a curved friction surface. It explains why a small tension T2 on the spring balance side can balance a much larger load T1 = Mg on the hanging side over a wrap of 1.5 turns (θ = 3π).'
        },
        {
            'title': 'Heat Capacity of the Calorimeter Assembly and Water Equivalent',
            'text': "The thermal heat Q absorbed during friction cycling is evaluated from the temperature elevation of the calorimeter assembly: Q = C_sys (T_f − T_0), where C_sys is the total heat capacity expressed in calories per kelvin. By historical definition, one calorie is the thermal energy required to elevate the temperature of one gram of pure liquid water by one degree Celsius (from 14.5 °C to 15.5 °C), meaning the specific heat capacity of water is c_w = 1.000 cal g⁻¹ K⁻¹. The copper drum, however, also absorbs sensible heat as its temperature rises. For a copper vessel of mass m_cal = 200.00 g and specific heat capacity c_cu = 0.0924 cal g⁻¹ K⁻¹, the heat capacity of the metal drum alone evaluates to C_cal = m_cal c_cu = 200.00 g × 0.0924 cal g⁻¹ K⁻¹ = 18.48 cal K⁻¹. In calorimetric terminology, this is called the water equivalent of the calorimeter: W_cal = 18.48 g of water. When charged with m_w = 100.00 g of distilled water, the aggregate system capacity in calories evaluates to C_sys = m_w c_w + m_cal c_cu = 100.00 + 18.48 = 118.48 cal K⁻¹. In SI units, multiplying C_sys by 4.1860 J cal⁻¹ gives C_sys,J = 495.96 J K⁻¹. Multiplying C_sys by the measured temperature rise ΔT = T_f − T_0 quantifies the total thermal energy in calories absorbed by the apparatus.",
            'formula': 'C_{\\text{sys}} = m_w c_w + m_{\\text{cal}} c_{\\text{cu}} = 100.00 + 18.48 = 118.48 \\text{ cal K}^{-1} \\quad (W_{\\text{cal}} = 18.48 \\text{ g})',
            'question': 'What is meant by the water equivalent of the calorimeter drum, and why must it be included in the calculation of heat absorbed?',
            'answer': 'The water equivalent W_cal is the mass of water that would absorb the identical quantity of thermal energy as the metal calorimeter drum for a 1 °C temperature rise (W_cal = m_cal · c_cu). It must be included because the copper drum warms alongside the water, absorbing a substantial fraction (~15%) of the total heat generated.'
        },
        {
            'title': 'Newton’s Cooling Corrections and Ambient Heat Loss Management',
            'text': "Because friction cycling requires between 2 and 6 minutes of continuous rotation, the calorimeter drum experiences heat exchange with the ambient room via convection and radiation. In accordance with Newton's law of cooling, the rate of environmental heat loss is proportional to the temperature excess over the room: dQ_loss/dt = k (T − T_ambient). If the drum begins at room temperature T_0 = T_ambient = 20.0 °C and warms to T_f = 35.0 °C, the drum is hotter than the ambient air throughout the entire rotation interval, continuously leaking thermal energy to the room. If uncorrected, the observed final temperature T_f is systematically lower than the ideal adiabatic temperature, causing the calculated heat Q = C_sys (T_f − T_0) to be underestimated and driving the apparent mechanical equivalent J = W / Q to be falsely inflated. Two techniques minimize this systematic defect: (1) Symmetrical thermal swing (Rumford's method): if the water is pre-cooled to 7 °C below room temperature (T_0 = 13 °C) and rotated until it reaches 7 °C above room temperature (T_f = 27 °C), the heat absorbed from the room during the cold half cancels the heat lost to the room during the hot half; (2) Graphical rate correction: tracking the post-rotation cooling rate for 5 minutes and extrapolating back to the midpoint of the rotation run restores the true adiabatic peak.",
            'formula': '\\frac{dQ_{\\text{loss}}}{dt} = k (T - T_{\\text{room}}) \\implies T_{f,\\text{corrected}} = T_{f,\\text{obs}} + \\int_0^{t_{\\text{run}}} k (T - T_{\\text{room}}) dt',
            'question': 'How does uncorrected heat loss to the room affect the experimental value of Joule’s constant J?',
            'answer': 'Heat lost to the room during rotation reduces the measured temperature rise ΔT, causing the calculated heat absorbed Q to be too low. Because J = W / Q, dividing the work by an underestimated Q causes the calculated value of J to be systematically too high.'
        },
        {
            'title': 'Thermodynamic Definition of the Calorie and Modern SI Energy Units',
            'text': "Historically, the calorie was defined in terms of water thermometry: the 15 °C calorie (cal_15) was defined as the quantity of thermal energy required to warm 1 gram of air-free water from 14.5 °C to 15.5 °C at standard atmospheric pressure (101.325 kPa). Because the specific heat capacity of liquid water c_w(T) varies slightly with temperature (exhibiting a broad minimum near 35 °C and rising toward 0 °C and 100 °C), different historical calorie definitions yielded slightly different mechanical equivalents: the 15 °C calorie corresponds to J = 4.1855 J; the 20 °C calorie corresponds to J = 4.1818 J; and the mean calorie (1/100 of the heat required to warm water from 0 °C to 100 °C) equals J = 4.1897 J. In 1929, the International Steam Table conference defined the International Table calorie as exactly 1 cal_IT ≡ 4.1868 J, while in 1948 the Ninth General Conference on Weights and Measures (CGPM) adopted the joule (1 J = 1 N m = 1 kg m² s⁻²) as the sole standard SI unit for all forms of energy, work, and heat. The thermochemical calorie was fixed by convention as exactly 1 cal_th ≡ 4.184 J. Today, the mechanical equivalent of heat is not treated as an empirical conversion factor, but rather as an essential historical milestone confirming that heat and mechanical work are dimensionally identical manifestations of energy.",
            'formula': '1 \\text{ cal}_{15} = 4.1855 \\text{ J}, \\quad 1 \\text{ cal}_{\\text{IT}} \\equiv 4.1868 \\text{ J}, \\quad 1 \\text{ cal}_{\\text{th}} \\equiv 4.1840 \\text{ J}',
            'question': 'Why did different historical definitions of the calorie yield slightly different values for Joule’s constant J?',
            'answer': 'Because the specific heat capacity of liquid water varies slightly with temperature (by about 1% between 0 °C and 100 °C). Defining the calorie over different temperature intervals (e.g. 14.5–15.5 °C vs 19.5–20.5 °C vs mean 0–100 °C) produced minor differences in the exact mechanical equivalent.'
        }
    ],
    'precautions': [
        'Ensure the drum is rotated at a steady, uniform speed so that the suspended load floats stably in mid-air without bouncing or bottoming out on the bench.',
        'Record the small residual tension on the spring balance and subtract it from the suspended load to evaluate the true net frictional force.',
        'Gently rock or agitate the drum after rotation ceases to thoroughly mix the internal water before recording the maximum equilibrium temperature.',
        'Inspect the canvas friction belt and copper drum surface to ensure they remain completely clean and free of oil or grease, which could cause erratic slipping.'
    ],
    'quiz': [
        {
            'question': 'When plotting mechanical work W (J) on the vertical axis against thermal heat Q (cal) on the horizontal axis, what does the gradient of the best-fit line represent?',
            'options': [
                'Joule’s mechanical equivalent of heat J (J cal⁻¹).',
                'The specific heat capacity of copper c_cu.',
                'The coefficient of kinetic friction μ.',
                'The angular velocity of the rotating drum ω.'
            ],
            'correct': 0,
            'explanation': 'Because the governing energy conservation relation is W = J · Q, plotting W on the y-axis against Q on the x-axis yields a straight line y = m x whose slope m directly equals Joule’s mechanical equivalent of heat J.'
        },
        {
            'question': 'In the Callendar friction calorimeter, what is the mechanical work performed during N revolutions of a drum of radius r against a suspended load M_load?',
            'options': [
                'W = 2π r M_load g N',
                'W = π r² M_load g N',
                'W = (1/2) M_load (2π r N)²',
                'W = M_load g / (2π r N)'
            ],
            'correct': 0,
            'explanation': 'In one revolution, the drum surface moves through distance s = 2π r against the frictional force F = M_load g. For N revolutions, the total work done is W = F · (N · 2π r) = 2π r M_load g N.'
        },
        {
            'question': 'Why must the water equivalent of the copper calorimeter drum be added to the mass of the water when calculating heat absorbed Q?',
            'options': [
                'Because the copper drum warms through the identical temperature rise as the water, absorbing a significant portion of the generated heat.',
                'Because the copper drum expands and increases the internal volume of the water.',
                'Because water reacts chemically with the copper drum at elevated temperatures.',
                'Because the friction belt rubs against the water directly inside the drum.'
            ],
            'correct': 0,
            'explanation': 'The copper drum is in intimate thermal contact with the water and heats up alongside it. The drum’s heat capacity (m_cal · c_cu = W_cal) must be included to account for the total heat absorbed by the system.'
        },
        {
            'question': 'What was the revolutionary scientific conclusion established by Joule’s mechanical equivalent of heat experiments?',
            'options': [
                'Heat is a form of energy that is universally convertible with mechanical work, disproving the caloric fluid theory.',
                'Heat is an indestructible fluid that can be created but never destroyed.',
                'Mechanical friction generates heat by destroying kinetic energy completely.',
                'Temperature is a vector quantity that depends on the direction of mechanical rotation.'
            ],
            'correct': 0,
            'explanation': 'Joule proved that heat is not a material fluid (caloric) but a form of energy that is interconvertible with mechanical work according to a fixed numerical ratio, establishing the First Law of Thermodynamics.'
        }
    ],
    'limitations': 'The teaching simulation models friction calorimetry under idealized thermal conditions with constant initial baseline temperature T_0 = 20.00 °C, constant drum radius r = 0.0500 m, suspended load mass M_load = 3.000 kg, and invariant system heat capacity C_sys = 118.48 cal K⁻¹. In physical experiments, convective and radiative heat losses to the ambient room during rotation (~3–8 min) cause the observed final temperature to fall below the adiabatic value, belt tension fluctuations and spring balance vibrations cause small work variations, friction between the axle bearings and support pillars dissipates a small fraction of work outside the water chamber, water evaporation through drum seals can cause minor latent heat cooling, and thermometer thermal response lag introduces slight peak temperature reading delays.',
    'modelExtra': 'The simulation evaluates mechanical work using W = 2π r M_load g N, where r = 0.0500 m is the drum radius, M_load = 3.000 kg is the suspended load, g = 9.80665 m s⁻² is gravitational acceleration, and N is the revolution count. Heat absorbed is evaluated using Q = C_sys (T_f − T_0) in calories, where C_sys = 118.48 cal K⁻¹ is the total thermal capacity (100.00 g water + 18.48 g water equivalent of the copper drum). Equilibrium temperatures are calculated using T_f = T_0 + W / (C_sys · J), with J = 4.1860 J cal⁻¹ and rounded to 0.01 °C to simulate precision laboratory thermometry. Ordinary least-squares regression of W against Q across five revolution settings yields the reported mechanical equivalent of heat.'
}

# 1. Update experiments.json
exp_path = ROOT / 'content/physics/experiments.json'
experiments = json.loads(exp_path.read_text())
existing_idx = next((i for i, e in enumerate(experiments) if e['slug'] == 'mechanical-equivalent-heat'), None)
if existing_idx is not None:
    experiments[existing_idx] = exp30
else:
    experiments.append(exp30)
exp_path.write_text(json.dumps(experiments, indent=2, ensure_ascii=False))
print(f'experiments.json updated. Total experiments: {len(experiments)}')

# 2. Update catalog.sqlite3
db_path = ROOT / 'data/catalog.sqlite3'
db = sqlite3.connect(db_path)
cur = db.cursor()
cur.execute('DELETE FROM experiments WHERE slug = ?', ('mechanical-equivalent-heat',))
cur.execute('''
    INSERT INTO experiments (subject_id, slug, title, status, page_path, theory_path, report_path)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    1,
    'mechanical-equivalent-heat',
    'Determination of the mechanical equivalent of heat (Joule constant)',
    'live',
    '/physics/mechanical-equivalent-heat/',
    '/physics/mechanical-equivalent-heat/theory/',
    '/physics/mechanical-equivalent-heat/report/'
))
db.commit()
db.close()
print('catalog.sqlite3 updated successfully for mechanical-equivalent-heat.')
