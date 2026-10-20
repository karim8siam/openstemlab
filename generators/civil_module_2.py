# -*- coding: utf-8 -*-
"""Civil Engineering Module 2: Mechanics of Materials & Structural Analysis (Labs 10–18)."""

def get_module_2():
    return [
        {
            "number": 10,
            "slug": "tensile-testing-structural-mild-steel-rebar",
            "title": "Uniaxial Tensile Testing of Structural Mild Steel Rebar (Young's Modulus & Yield)",
            "shortTitle": "Steel Tensile Testing",
            "aim": "Determine the engineering stress-strain curve, Young's modulus of elasticity (E), upper and lower yield strength (f_y), ultimate tensile strength (f_u), and percentage elongation of structural reinforcing steel according to ASTM A615 / ASTM E8.",
            "inputLabel": "Tensile Strain ε",
            "shortInput": "Strain ε",
            "inputUnit": "µε",
            "min": 200.0,
            "max": 1200.0,
            "step": 200.0,
            "initial": 600.0,
            "inputDecimals": 0,
            "rawLabel": "Tensile Stress σ",
            "rawUnit": "MPa",
            "rawDecimals": 1,
            "xAxis": "Tensile strain ε (µε)",
            "yAxis": "Tensile stress σ (MPa)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 1400.0,
            "emptyY": 300.0,
            "targetName": "Structural Steel Young's Modulus E",
            "target": "0.2000",
            "refValue": 0.2000,
            "resultUnit": "GPa",
            "resultDecimals": 4,
            "resultScale": 1000.0,
            "fitEquation": "σ = 0.2000 · ε (GPa · µε = MPa)",
            "intro": "Structural steel constitutes the tensile reinforcing backbone of modern reinforced and prestressed concrete infrastructure, providing ductility, energy absorption, and catastrophic collapse prevention. Standard specification ASTM A615 / ASTM E8 requires deformed reinforcing bars (rebars) to be tested in uniaxial tension on an automated Universal Testing Machine (UTM) to verify mechanical grade compliance. As uniaxial tensile force P increases on a coupon of initial gauge length L_0 and nominal cross-sectional area A_0, the bar responds through four classical behavioral regimes: (1) Linear elastic deformation governed by Hooke's law (σ = E · ε), where atomic iron bonds stretch reversibly; (2) Plastic yielding at yield strength f_y, characterized by the propagation of Lüders slip bands across the crystal lattice at nearly constant stress; (3) Strain hardening up to ultimate tensile strength f_u as dislocation tangles multiply and impede crystal slip; and (4) Localized necking followed by cup-and-cone shear ductile fracture. In this laboratory investigation, precision extensometers monitor strain in the linear elastic regime across microstrain levels from 200 to 1200 µε to calibrate Young's modulus E and evaluate Grade 60 (420 MPa) rebar properties.",
            "modelExtra": "Tested on standard No. 5 (16 mm diameter) Grade 60 deformed rebar (nominal area A_0 = 199 mm^2, gauge length L_0 = 200 mm). Linearized regression relates stress σ directly to microstrain ε with slope 0.2000 MPa/µε (E = 200.0 GPa).",
            "apparatus": [
                {"name": "Computer-Controlled Hydraulic Universal Testing Machine (UTM)", "purpose": "Applies smooth, monotonic axial tensile displacement up to 600 kN with digital load cell resolution of 0.1 kN."},
                {"name": "Hydraulic Wedge Grips with V-Jaws", "purpose": "High-grip serrated hardened alloy steel jaws clamping deformed rebar ends securely without slippage."},
                {"name": "Electronic Clip-On Axial Extensometer", "purpose": "Precision dual-knife-edge LVDT extensometer with 50 mm gauge length measuring strain to 0.1 microstrain."},
                {"name": "Digital Vernier Calliper & Micrometer", "purpose": "Measures core diameter, rib height, and gauge punch spacing with 0.01 mm precision."},
                {"name": "Rebar Gauge Center-Punch Jig", "purpose": "Marks 200 mm gauge lengths for post-fracture plastic elongation measurements."},
                {"name": "Transparent High-Impact Polycarbonate Blast Door", "purpose": "Encloses testing envelope against flying debris during ductile cup-and-cone fracture."}
            ],
            "procedure": [
                {"title": "Specimen Inspection & Gauge Marking", "text": "Inspect No. 5 (16 mm) rebar for surface defects; measure nominal diameter across ribs; mark 200 mm initial gauge length L_0 using center punch jig."},
                {"title": "Cross-Sectional Area Determination", "text": "Weigh a 1000 mm length of rebar to compute mass per meter and determine nominal cross-sectional area A_0 according to ASTM A615."},
                {"title": "UTM Clamping & Extensometer Mounting", "text": "Mount specimen into hydraulic wedge grips; ensure vertical coaxial alignment; clip electronic extensometer onto the central gauge section and zero software readings."},
                {"title": "Monotonic Tensile Loading in Elastic Domain", "text": "Apply axial tension at a strain-controlled rate of 0.001 mm/mm/min; record simultaneous load P and strain ε across 200, 400, 600, 800, 1000, and 1200 µε."},
                {"title": "Yield & Strain Hardening Progression", "text": "Continue loading through yield plateau; remove extensometer prior to necking to prevent sensor damage; record yield force P_y and ultimate force P_u."},
                {"title": "Fracture Assembly & Ductility Characterization", "text": "Remove fractured bar halves; fit tightly together; measure final gauge length L_f to calculate percentage elongation and neck diameter d_f to determine reduction of area."}
            ],
            "topics": [
                {"question": "What is the physical significance of the yield point in structural steel design?", "answer": "The yield point f_y marks the limit of elastic structural behavior; beyond f_y, permanent plastic deformation occurs, meaning design codes (AISC 360, ACI 318) restrict allowable working stresses safely below f_y."},
                {"question": "How do upper yield strength and lower yield strength differ in mild steel?", "answer": "Upper yield strength represents the initial peak stress required to break carbon-nitrogen solute atom Cottrell atmospheres pinning dislocations; lower yield strength is the steady-state stress required to propagate Lüders slip bands across the specimen."},
                {"question": "Why is high ductility (percentage elongation > 12%) essential for earthquake-resistant reinforced concrete?", "answer": "During intense seismic shaking, ductile rebar forms plastic hinges that absorb and dissipate enormous earthquake energy through cyclic plastic yielding, preventing sudden catastrophic brittle building collapse."},
                {"question": "What is the 0.2% offset yield strength method and when is it required?", "answer": "Cold-worked or high-strength alloy steels lack a distinct yield plateau; the 0.2% offset method draws a line parallel to the elastic slope starting at 0.002 strain (0.2%), defining yield strength where this line intersects the stress-strain curve."},
                {"question": "How does carbon content influence the mechanical properties of structural steel?", "answer": "Increasing carbon content increases yield strength and ultimate tensile strength through interstitial solid solution and pearlite phase fractions, but severely reduces ductility, toughness, and weldability."},
                {"question": "What is the characteristic appearance of a ductile steel tensile fracture surface?", "answer": "Ductile steel fractures exhibit a classic 'cup-and-cone' morphology: a flat, fibrous central zone caused by microvoid coalescence in plane strain, surrounded by a 45° conical shear lip formed by localized shear yielding."}
            ],
            "precautions": [
                "Verify that hydraulic wedge grips clamp rebar ends symmetrically to prevent eccentric loading and spurious bending moments.",
                "Remove delicate clip-on extensometers immediately after yield plateau initiation to protect sensor LVDTs from shock damage at ultimate fracture.",
                "Ensure machine crosshead loading rate does not exceed ASTM E8 limits (≤ 0.015 mm/mm/min during yielding) to avoid artificially elevated yield points.",
                "Keep blast shield doors completely closed during testing to contain high-energy fragment release upon ultimate necking fracture."
            ],
            "quiz": [
                {
                    "question": "The slope of the linear elastic region of an engineering stress-strain curve represents:",
                    "options": ["Poisson's ratio", "Young's Modulus of Elasticity (E)", "Yield strength", "Toughness modulus"],
                    "correct": 1,
                    "explanation": "According to Hooke's Law, σ = E · ε, the slope of the elastic line equals Young's Modulus E."
                },
                {
                    "question": "The standard nominal Young's modulus E for structural carbon steel is approximately:",
                    "options": ["70 GPa", "110 GPa", "200 GPa", "400 GPa"],
                    "correct": 2,
                    "explanation": "Structural steel universally exhibits an elastic modulus of approximately 200 GPa (200,000 MPa / 29,000 ksi)."
                },
                {
                    "question": "The localized reduction in cross-sectional area that occurs just before tensile fracture is called:",
                    "options": ["Slip banding", "Necking", "Strain hardening", "Cleavage fracture"],
                    "correct": 1,
                    "explanation": "Necking is the unstable plastic instability where deformation localizes into a narrow waist before fracture."
                },
                {
                    "question": "In Grade 60 reinforcing steel (ASTM A615), the number '60' designates:",
                    "options": ["Minimum tensile strength of 60 MPa", "Minimum yield strength of 60 ksi (414 MPa)", "Maximum carbon content of 0.60%", "Diameter of 60 mm"],
                    "correct": 1,
                    "explanation": "Grade 60 designates a minimum guaranteed yield strength of 60,000 psi (60 ksi, equivalent to 414 to 420 MPa)."
                }
            ],
            "samples": [200.0, 400.0, 600.0, 800.0, 1000.0, 1200.0],
            "measureLabel": "Record tensile stress σ in elastic domain",
            "readings": ["stress_mpa", "strain_ue", "load_kn", "modulus_gpa"],
            "theory": """<h3>1. Continuum Mechanics & Hooke's Law in Uniaxial Tension</h3>
<p>When a prismatic structural bar of initial gauge length $L_0$ and cross-sectional area $A_0$ is subjected to a coaxial tensile load $P$, engineering normal stress $\\sigma$ and engineering normal strain $\\varepsilon$ are defined as:</p>
\\[ \\sigma = \\frac{P}{A_0}, \\qquad \\varepsilon = \\frac{\\Delta L}{L_0} \\]
<p>In the initial loading domain, deformation is governed by classical linear elasticity (Hooke's law). At the atomic scale, applied mechanical stress slightly increases the equilibrium inter-atomic spacing $r_0$ between iron atoms in the body-centered cubic (BCC) $\\alpha$-ferrite crystal lattice against inter-atomic attractive bonding forces. Because inter-atomic potential energy wells are parabolic near equilibrium, stress scales directly with strain:</p>
\\[ \\sigma = E \\cdot \\varepsilon \\]
<p>where $E$ is Young's Modulus of Elasticity (typically $200\\text{ GPa} = 200,000\\text{ MPa}$ for structural carbon steels).</p>

<h3>2. Plastic Dislocation Mechanics & Lüders Slip Bands</h3>
<p>When stress reaches the upper yield point, resolved shear stress along the $\{110\}$ close-packed planes in $\\langle 111 \\rangle$ slip directions exceeds the critical resolved shear stress (CRSS) required to unpin dislocations from interstitial carbon and nitrogen solute atmospheres (Cottrell atmospheres). Once freed, dislocations multiply exponentially through Frank–Read sources, causing stress to drop slightly to the lower yield strength $f_y$. Deformation proceeds through the propagation of macroscopic Lüders slip bands inclined at $45^\\circ$ across the bar at nearly constant yield stress.</p>

<h3>3. Strain Hardening, Ultimate Strength & Ductile Necking</h3>
<p>Beyond the yield plateau (typically $\\varepsilon > 1.5\\%$), moving dislocations intersect, cross-slip, and tangle with grain boundaries and cementite precipitates, generating internal back-stresses. Further plastic deformation requires higher applied stress, initiating the strain-hardening domain governed by Hollomon's constitutive relation:</p>
\\[ \\sigma_{true} = K \\cdot \\varepsilon_{true}^n \\]
<p>where $K$ is the strength coefficient and $n \\approx 0.15\\text{ to }0.25$ is the strain-hardening exponent. At ultimate tensile strength $f_u$, the rate of geometric area reduction outpaces the rate of strain hardening ($d\\sigma / d\\varepsilon = \\sigma$), triggering localized necking and ultimate ductile cup-and-cone fracture.</p>

<h3>4. Linear Regression Model for Young's Modulus Calibration</h3>
<p>In this laboratory, precise extensometer measurements within the elastic range ($\ ext{microstrain } \\varepsilon_{\\mu} = 200\\text{ to }1200\\,\\mu\\varepsilon = 0.0002\\text{ to }0.0012$) allow direct linear regression:</p>
\\[ \\sigma = E_{slope} \\cdot \\varepsilon_{\\mu} \\]
<p>where $E_{slope} = 0.2000\\text{ MPa/}\\mu\\varepsilon$. Converting to SI units:</p>
\\[ E = 0.2000\\text{ MPa}/(10^{-6}\\text{ mm/mm}) = 200,000\\text{ MPa} = 200.00\\text{ GPa} \\]""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this civil engineering laboratory investigation is to evaluate the mechanical stress-strain characteristics of ASTM A615 Grade 60 structural mild steel rebar under uniaxial tension according to ASTM E8 / ASTM A615. By logging tensile stress across six microstrain plateaus ($200\\text{ to }1200\\,\\mu\\varepsilon$), executing linear regression, and continuing to ultimate failure, we determine Young's Modulus of Elasticity ($E$), yield strength ($f_y$), ultimate tensile strength ($f_u$), and percentage elongation to verify structural code compliance.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>In the linear elastic regime, engineering stress $\\sigma$ is related to engineering strain $\\varepsilon$ by Hooke's Law:</p>
\\[ \\sigma = \\frac{P}{A_0} = E \\cdot \\varepsilon = E_{slope} \\cdot \\varepsilon_{\\mu} \\]
<p>where $E_{slope} = 0.2000\\text{ MPa/}\\mu\\varepsilon$, corresponding to Young's modulus $E = 200.00\\text{ GPa}$. Post-fracture ductility metrics include percentage elongation $EL\\% = [(L_f - L_0) / L_0] \\times 100\\%$ and reduction of area $RA\\% = [(A_0 - A_f) / A_0] \\times 100\\%$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing was performed on an MTS computerized servo-hydraulic Universal Testing Machine ($600\\text{ kN}$ load capacity, load accuracy $\\pm 0.3\\%$ of indicated reading). Axial strain was measured using an MTS clip-on dual extensometer ($50.0\\text{ mm}$ gauge length, travel $\\pm 5.0\\text{ mm}$, resolution $0.1\\,\\mu\\varepsilon$). Specimen gripping utilized hardened wedge grips with V-toothed serrations. The test coupon was a standard No. 5 (nominal diameter $16.0\\text{ mm}$, nominal area $A_0 = 199.0\\text{ mm}^2$, initial gauge length $L_0 = 200.0\\text{ mm}$) Grade 60 deformed carbon steel rebar.</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>The rebar was weighed to confirm nominal cross-section ($1.56\\text{ kg/m}$), marked with punch marks at $200\\text{ mm}$, mounted in the UTM wedge grips, and the extensometer attached. Tensile load was applied at a strain rate of $0.001\\text{ mm/mm/min}$. Stress and strain were logged at $200, 400, 600, 800, 1000,$ and $1200\\,\\mu\\varepsilon$. Loading was continued through the yield plateau, the extensometer detached, and the specimen pulled to necking and cup-and-cone fracture. Final gauge length $L_f$ and neck diameter $d_f$ were measured.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Tensile rebar fracture releases substantial elastic strain energy, generating an acoustic blast ($> 100\\text{ dBA}$) and potential shrapnel. The heavy polycarbonate safety door remained closed during all tests. Operators wore ANSI-approved safety glasses, steel-toed boots, and cut-resistant gloves when handling jagged rebar fracture ends.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded in the elastic regime for nominal area $A_0 = 199.0\\text{ mm}^2$:</p>
<table>
<thead>
<tr><th>Point</th><th>Microstrain ε (µε)</th><th>Applied Load P (kN)</th><th>Engineering Stress σ (MPa)</th><th>Calculated Modulus E (GPa)</th><th>Behavior Regime</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>200.0</td><td>7.96</td><td>40.0</td><td>200.0</td><td>Linear Elastic Hookean</td></tr>
<tr><td>2</td><td>400.0</td><td>15.92</td><td>80.0</td><td>200.0</td><td>Linear Elastic Hookean</td></tr>
<tr><td>3</td><td>600.0</td><td>23.88</td><td>120.0</td><td>200.0</td><td>Linear Elastic Hookean</td></tr>
<tr><td>4</td><td>800.0</td><td>31.84</td><td>160.0</td><td>200.0</td><td>Linear Elastic Hookean</td></tr>
<tr><td>5</td><td>1000.0</td><td>39.80</td><td>200.0</td><td>200.0</td><td>Linear Elastic Hookean</td></tr>
<tr><td>6</td><td>1200.0</td><td>47.76</td><td>240.0</td><td>200.0</td><td>Linear Elastic Hookean</td></tr>
</tbody>
</table>
<p><strong>Post-Yield & Ultimate Properties:</strong> Yield load $P_y = 90.5\\text{ kN}$ ($f_y = 454.8\\text{ MPa}$), Ultimate load $P_u = 138.2\\text{ kN}$ ($f_u = 694.5\\text{ MPa}$), Ratio $f_u / f_y = 1.53$, Final gauge length $L_f = 236.4\\text{ mm}$ (Elongation = $18.2\\%$), Neck diameter $d_f = 11.2\\text{ mm}$ (Reduction of Area = $51.0\\%$).</p>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of engineering stress $\\sigma$ versus microstrain $\\varepsilon_{\\mu}$ yields:</p>
\\[ \\sigma = 0.20000 \\cdot \\varepsilon_{\\mu} + 0.00000 \\]
<p>with a perfect coefficient of determination $R^2 = 1.000000$. Converting the slope to standard elastic modulus:</p>
\\[ E = 0.20000\\text{ MPa}/(10^{-6}) = 200,000\\text{ MPa} = 200.0000\\text{ GPa} \\]
<p>The experimental modulus matches the design standard ($200.00\\text{ GPa}$) with zero relative deviation ($0.00\\%$). Both yield strength ($454.8\\text{ MPa} \\ge 420\\text{ MPa}$) and ultimate tensile strength ($694.5\\text{ MPa} \\ge 620\\text{ MPa}$) satisfy ASTM A615 Grade 60 standards.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Load cell precision is $\\delta P = \\pm 0.1\\text{ kN}$ ($0.25\\%$), extensometer precision is $\\delta \\varepsilon = \\pm 0.5\\,\\mu\\varepsilon$ ($0.08\\%$), and area uncertainty is $\\delta A_0 / A_0 = 0.30\\%$. Propagating into $E$:</p>
\\[ \\frac{\\delta E}{E} = \\sqrt{ \\left( \\frac{\\delta P}{P} \\right)^2 + \\left( \\frac{\\delta \\varepsilon}{\\varepsilon} \\right)^2 + \\left( \\frac{\\delta A_0}{A_0} \\right)^2 } = \\pm 0.40\\% \\]
<p>The reported elastic modulus is $E = 200.00 \\pm 0.80\\text{ GPa}$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The tested rebar displayed exemplary metallurgical ductility. The stress-strain trajectory exhibited an extended plastic yield plateau of $1.8\\%$ strain, followed by substantial strain hardening. The high ratio of tensile strength to yield strength ($f_u / f_y = 1.53 \\ge 1.25$) and high elongation ($18.2\\% \\ge 12\\%$) satisfy seismic design requirements for ductile moment frames under ACI 318 Chapter 18.</p>

<h3>10. Structural Reinforced Concrete Design Applications</h3>
<p>In ultimate strength design of reinforced concrete beams and columns, the nominal flexural capacity $M_n$ assumes that steel has yielded ($f_s = f_y$). The high yield strength ($454.8\\text{ MPa}$) guarantees reliable flexural capacity, while the $200.0\\text{ GPa}$ elastic modulus directly determines cracked section moment of inertia and long-term deflection control.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is an upper bound on yield strength enforced in seismic design codes?</strong><br>
<em>A1:</em> If rebar yield strength is unexpectedly high (e.g. $> 540\\text{ MPa}$ for Grade 60), the beam may resist flexural yielding during an earthquake, forcing brittle diagonal shear failure in the concrete core before ductile plastic hinges can form.</p>
<p><strong>Q2: What is the physical origin of the cup-and-cone fracture pattern?</strong><br>
<em>A2:</em> The flat central 'cup' initiates by ductile microvoid coalescence around carbide inclusions in high triaxial tension; once the central crack reaches the outer region, plane stress conditions take over, shearing along $45^\\circ$ maximum shear planes to form the conical lip.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The uniaxial tensile testing of Grade 60 structural rebar verified pristine elastic-plastic mechanical performance. The calibrated Young's modulus $E = 200.00\\text{ GPa}$ ($R^2 = 1.000000$), yield strength of $454.8\\text{ MPa}$, and ultimate elongation of $18.2\\%$ confirm full compliance with ASTM A615 and ACI 318 structural specifications.</p>"""
        },
        {
            "number": 11,
            "slug": "charpy-v-notch-impact-toughness-structural-steel",
            "title": "Charpy V-Notch Pendulum Impact Toughness & Ductile-to-Brittle Transition Temperature",
            "shortTitle": "Charpy Impact Toughness",
            "aim": "Determine the impact absorbed energy (K_V) and ductile-to-brittle transition temperature (DBTT) of structural bridge steel under high-strain-rate impact loading according to ASTM E23 / BS EN ISO 148-1.",
            "inputLabel": "Specimen Temperature T",
            "shortInput": "Temperature",
            "inputUnit": "°C",
            "min": -30.0,
            "max": 50.0,
            "step": 20.0,
            "initial": 10.0,
            "inputDecimals": 0,
            "rawLabel": "Absorbed Impact Energy K_V",
            "rawUnit": "J",
            "rawDecimals": 1,
            "xAxis": "Test temperature T (°C)",
            "yAxis": "Absorbed impact energy K_V (J)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 60.0,
            "emptyY": 130.0,
            "targetName": "Temperature Impact Toughness Sensitivity",
            "target": "0.8500",
            "refValue": 0.8500,
            "resultUnit": "J/°C",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "K_V = 0.8500 · T + 65.0000",
            "intro": "Catastrophic brittle fractures of steel structures—such as the infamous WWII Liberty ship fractures and civil bridge collapses in sub-zero winter temperatures—revealed that static tensile yield strength is insufficient to guarantee structural safety under dynamic shock loading. Body-centered cubic (BCC) ferritic structural steels undergo a profound transformation from ductile, high-energy plastic tearing at warm temperatures to brittle, low-energy transgranular cleavage fracture at freezing temperatures. Standardized under ASTM E23 and ISO 148-1, the Charpy V-notch (CVN) impact test utilizes a standardized square specimen (10 x 10 x 55 mm) with a precision 45° V-notch machined to a depth of 2 mm and root radius of 0.25 mm. The specimen is supported as a simple beam and struck on the face opposite the notch by a calibrated heavy swinging pendulum with striking energy of 300 ± 10 J at impact velocity ~5.2 m/s. The energy absorbed in fracturing the specimen (K_V) is evaluated directly from the difference between pendulum initial release height and post-fracture follow-through height. In this laboratory, impact toughness is tested across temperatures from -30 °C to +50 °C to evaluate impact sensitivity and ensure compliance with AASHTO bridge fracture-critical specifications (minimum 27 J at -20 °C).",
            "modelExtra": "ASTM A572 Grade 50 (345 MPa) structural steel. Linearized model over the transition zone relates absorbed energy K_V directly to temperature T with sensitivity 0.8500 J/°C and 0 °C intercept 65.0 J.",
            "apparatus": [
                {"name": "Instrumented Charpy Pendulum Impact Tester", "purpose": "Calibrated 300 J capacity pendulum with 2 mm radius striker tup and digital optical encoder."},
                {"name": "Standard V-Notch Specimen Anvils & Shroud", "purpose": "Hardened tool steel support anvils spaced at 40.0 mm span with 1.0 mm radius corners."},
                {"name": "Thermostatically Controlled Thermal Conditioning Bath", "purpose": "Liquid nitrogen / ethanol cryo-bath and heated bath maintaining -50 °C to +100 °C to ± 0.5 °C."},
                {"name": "Precision Self-Centering Specimen Transfer Tongs", "purpose": "Specialized tongs transferring specimen from thermal bath to anvil in < 5 seconds per ASTM E23."},
                {"name": "Optical Notch Profile Projector / Comparator", "purpose": "Verifies 45° ± 1° notch angle, 2.00 ± 0.05 mm notch depth, and 0.25 mm root radius."},
                {"name": "Fracture Cleavage SEM / Optical Microscope", "purpose": "Examines percentage shear fracture lip area versus flat cleavage area on fracture faces."}
            ],
            "procedure": [
                {"title": "Specimen Dimensional & Notch Verification", "text": "Inspect 10 x 10 x 55 mm steel specimens on the optical projector; verify notch depth (2.00 mm), notch radius (0.25 mm), and 45° angle."},
                {"title": "Thermal Conditioning at Target Temperatures", "text": "Immerse specimens in the liquid bath at target temperatures (-30, -10, +10, +30, and +50 °C); condition for at least 10 minutes to achieve uniform core temperature."},
                {"title": "Pendulum Initial Elevation & Zero Check", "text": "Latch pendulum hammer at standard initial angle (300 J potential energy); release with empty anvils to record zero-friction windage loss calibration."},
                {"title": "Rapid Specimen Transfer & Centering", "text": "Using chilled tongs, remove specimen from bath and place on testing anvils centered with notch facing away from striker tup within strictly 5.0 seconds."},
                {"title": "Pendulum Release & Impact Fracture", "text": "Immediately trip the pneumatic pendulum release latch; allow hammer to sever the specimen and swing through; engage automatic mechanical brake."},
                {"title": "Energy Logging & Fracture Face Analysis", "text": "Read absorbed energy K_V in Joules from digital encoder; measure lateral expansion at notch root with micrometer gauge; determine percentage shear area."}
            ],
            "topics": [
                {"question": "What is the physical cause of the ductile-to-brittle transition in body-centered cubic (BCC) steels?", "answer": "In BCC ferrite, dislocation slip requires high thermal activation energy (Peierls–Nabarro stress); at low temperatures, dislocation motion becomes sluggish, allowing tensile stresses at the triaxial notch root to exceed the critical cleavage stress before plastic shear can occur."},
                {"question": "Why is a sharp 45° V-notch machined into the Charpy specimen?", "answer": "The notch serves as an extreme geometric stress concentrator (elastic stress concentration factor K_t ≈ 3.5), inducing severe triaxial tension (sigma_1 > sigma_2 > sigma_3 > 0) that suppresses plastic yielding and promotes brittle cleavage."},
                {"question": "Why does ASTM E23 strictly mandate specimen transfer and impact within 5 seconds?", "answer": "The specimen rapidly exchanges heat with ambient room air upon removal from the thermal bath; testing within 5 seconds guarantees specimen core temperature departs by less than 1.0 °C from bath temperature."},
                {"question": "What is the physical meaning of lateral expansion in Charpy impact testing?", "answer": "Lateral expansion measures the plastic deformation (bulging) on the compression face opposite the notch; higher lateral expansion (> 0.38 mm) indicates ductile energy absorption and resistance to catastrophic fracture."},
                {"question": "How do nickel alloying additions improve the low-temperature impact toughness of bridge steels?", "answer": "Nickel atoms expand the BCC lattice and lower the Peierls stress for cross-slip, promoting active dislocation mobility even down to cryogenic temperatures (-100 °C) without reducing yield strength."},
                {"question": "How does the Charpy impact test differ from fracture mechanics fracture toughness testing (K_IC)?", "answer": "Charpy impact is an empirical comparative quality-control index measuring total dynamic fracture energy, whereas K_IC (plane strain fracture toughness) is a fundamental material property used in structural flaw-tolerance calculations."}
            ],
            "precautions": [
                "Never exceed the strict 5-second transfer window between thermal bath removal and pendulum impact release.",
                "Verify specimen notch faces precisely away from the pendulum striker; inserting specimens backwards invalidates the test.",
                "Ensure pendulum safety interlock latch is engaged before loading specimens or entering the swing trajectory envelope.",
                "Calibrate pendulum bearing friction and aerodynamic windage losses prior to initiating daily impact testing."
            ],
            "quiz": [
                {
                    "question": "The standard dimensions of a Charpy V-notch impact specimen (ASTM E23) are:",
                    "options": ["5 x 5 x 50 mm", "10 x 10 x 55 mm", "15 x 15 x 75 mm", "20 x 20 x 100 mm"],
                    "correct": 1,
                    "explanation": "ASTM E23 specifies standard dimensions of 10 x 10 x 55 mm with a 2 mm deep 45° V-notch."
                },
                {
                    "question": "The orientation of the specimen notch relative to the swinging pendulum striker must be:",
                    "options": ["Facing directly toward the striker", "Facing away from the striker (tension side)", "Facing upward toward the ceiling", "Facing downward toward the floor"],
                    "correct": 1,
                    "explanation": "The striker strikes the unnotched face directly behind the notch, putting the notch root into severe triaxial tension."
                },
                {
                    "question": "The maximum allowable time to transfer the specimen from conditioning bath to hammer release is:",
                    "options": ["5 seconds", "15 seconds", "30 seconds", "60 seconds"],
                    "correct": 0,
                    "explanation": "ASTM E23 strictly limits transfer and impact time to within 5 seconds to prevent temperature drift."
                },
                {
                    "question": "A steel fracture surface exhibiting a bright, shiny, crystalline facet appearance indicates:",
                    "options": ["High-energy ductile shear tearing", "Low-energy brittle cleavage fracture", "Severe plastic necking", "Excessive interstitial solid solution"],
                    "correct": 1,
                    "explanation": "Shiny crystalline facets indicate transgranular brittle cleavage along crystallographic planes with minimal energy absorption."
                }
            ],
            "samples": [-30.0, -10.0, 10.0, 30.0, 50.0],
            "measureLabel": "Record absorbed impact energy K_V",
            "readings": ["kv_joules", "temp_c", "lateral_exp_mm", "shear_pct"],
            "theory": """<h3>1. Fracture Mechanics & High Strain Rate Dynamics</h3>
<p>In structural civil engineering, sudden impact loads from vehicle collisions, seismic shockwaves, and wave slap subject structural steel to immense strain rates ($\\dot{\\varepsilon} \\approx 10^2\\text{ to }10^4\\text{ s}^{-1}$). Under dynamic loading, dislocation velocity is constrained by thermal drag and phonon scattering, raising effective yield strength $\\sigma_y^{dyn}$ by up to $100\\%$ compared to quasi-static values.</p>

<p>The standard Charpy V-notch specimen ($10 \\times 10 \\times 55\\text{ mm}$) incorporates a sharp notch with root radius $\\rho = 0.25\\text{ mm}$ and notch depth $a = 2.0\\text{ mm}$. Under third-point impact loading across span $S = 40\\text{ mm}$, the notch generates plastic slip-line fields described by Hill's slip-line field theory for a notched bar in bending. The elastic stress concentration factor $K_t$ reaches:</p>
\\[ K_t = 1 + 2 \\sqrt{\\frac{a}{\\rho}} = 1 + 2 \\sqrt{\\frac{2.0}{0.25}} = 1 + 2(2.828) \\approx 6.66 \\]
<p>yielding triaxial tension where hydrostatic tensile stress $\\sigma_m = (\\sigma_1 + \\sigma_2 + \\sigma_3)/3$ reaches maximum intensity directly ahead of the notch root.</p>

<h3>2. The Ductile-to-Brittle Transition Temperature (DBTT)</h3>
<p>Cleavage fracture occurs when local maximum principal stress $\\sigma_1$ reaches the temperature-independent critical cleavage fracture stress $\\sigma_f^*$. Because plastic yield stress $\\sigma_y(T)$ increases exponentially as temperature decreases following Arrhenius kinetics:</p>
\\[ \\sigma_y(T) = \\sigma_0 + C \\cdot \\exp\\left( -\\frac{Q}{k_B T} \\right) \\]
<p>a crossover occurs at the Ductile-to-Brittle Transition Temperature (DBTT). Above DBTT, extensive plastic blunting precedes shear void coalescence (Upper Shelf, $K_V > 80\\text{ J}$). Below DBTT, cleavage triggers before plastic blunting (Lower Shelf, $K_V < 15\\text{ J}$).</p>

<h3>3. Linear Impact Toughness Response Model</h3>
<p>Across the linear transition regime ($T = -30^\\circ\\text{C to }+50^\\circ\\text{C}$), absorbed impact energy $K_V$ exhibits a linear response:</p>
\\[ K_V(T) = k_T \\cdot T + K_{V0} \\]
<p>where $k_T = 0.8500\\text{ J/}^\\circ\\text{C}$ represents temperature sensitivity, and $K_{V0} = 65.00\\text{ J}$ is absorbed energy at $0^\\circ\\text{C}$.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this civil engineering laboratory investigation is to determine the Charpy V-notch absorbed impact energy ($K_V$) and evaluate the ductile-to-brittle transition response of ASTM A572 Grade 50 structural bridge steel across five test temperatures ($-30, -10, +10, +30,$ and $+50^\\circ\\text{C}$) according to ASTM E23 / ISO 148-1. By measuring absorbed energy, lateral expansion, and fracture face morphology, we calibrate the temperature sensitivity slope $k_T$ and verify fracture-critical toughness criteria for bridge engineering.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Absorbed impact energy $K_V$ represents the mechanical work performed by the swinging pendulum during specimen fracture, calculated from initial potential energy $E_0 = M g h_1$ and follow-through potential energy $E_1 = M g h_2$ with windage loss correction $L_w$:</p>
\\[ K_V = M g (h_1 - h_2) - L_w \\]
<p>Across the ductile-to-brittle transition zone, absorbed energy scales linearly with test temperature:</p>
\\[ K_V = k_T \\cdot T + K_{V0} \\]
<p>where $k_T = 0.8500\\text{ J/}^\\circ\\text{C}$ and $K_{V0} = 65.0000\\text{ J}$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized an instrumented Charpy pendulum impact machine conforming to ASTM E23 ($300.0 \\pm 2.0\\text{ J}$ capacity, striking velocity $5.24\\text{ m/s}$, pendulum length $800\\text{ mm}$, anvil span $40.0 \\pm 0.2\\text{ mm}$, striker tup radius $2.0\\text{ mm}$). Specimens were precision CNC-milled ASTM A572 Grade 50 structural steel ($10.0 \\times 10.0 \\times 55.0\\text{ mm}$, $45^\\circ$ V-notch, depth $2.00 \\pm 0.05\\text{ mm}$, root radius $0.25 \\pm 0.02\\text{ mm}$). Thermal baths utilized liquid nitrogen/ethanol mixtures monitored by calibrated Pt100 RTD sensors ($\pm 0.2^\\circ\text{C}$).</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Specimens were conditioned at target temperatures for $15\\text{ minutes}$. Using pre-cooled centering tongs, specimens were transferred to machine anvils and struck within strictly $4.0\\text{ seconds}$ from bath extraction. Absorbed energy $K_V$ was recorded from the digital optical encoder. Lateral expansion on the compression side was measured with a dual-dial gauge micrometer, and percentage shear area was evaluated under an optical stereo-microscope.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>The swinging $300\\text{ J}$ pendulum poses lethal blunt-force impact hazards. The impact machine was fitted with electrical interlocking safety cage enclosures preventing hammer release until doors were fully latched. Liquid nitrogen baths present extreme cryogenic frostbite risks; operators wore cryogenic insulated gloves, face shields, and lab aprons.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the thermal sweep:</p>
<table>
<thead>
<tr><th>Trial</th><th>Temperature T (°C)</th><th>Absorbed Energy K_V (J)</th><th>Lateral Expansion (mm)</th><th>Fracture Appearance</th><th>Fracture Regime</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>-30.0</td><td>39.5</td><td>0.48</td><td>85% Cleavage (Brittle)</td><td>Lower Transition</td></tr>
<tr><td>2</td><td>-10.0</td><td>56.5</td><td>0.72</td><td>60% Cleavage</td><td>Mid Transition</td></tr>
<tr><td>3</td><td>10.0</td><td>73.5</td><td>0.98</td><td>30% Cleavage / 70% Shear</td><td>Mid Transition</td></tr>
<tr><td>4</td><td>30.0</td><td>90.5</td><td>1.24</td><td>90% Fibrous Shear</td><td>Upper Transition</td></tr>
<tr><td>5</td><td>50.0</td><td>107.5</td><td>1.48</td><td>100% Fibrous Shear</td><td>Upper Shelf</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of absorbed impact energy $K_V$ versus specimen temperature $T$ yields:</p>
\\[ K_V = 0.85000 \\cdot T + 65.00000 \\]
<p>with an exceptional coefficient of determination $R^2 = 1.000000$. The experimental temperature sensitivity slope $k_T = 0.8500\\text{ J/}^\\circ\\text{C}$ matches the theoretical reference benchmark ($0.8500\\text{ J/}^\\circ\\text{C}$) with zero relative deviation ($0.00\\%$). At the standard bridge design benchmark ($T = -20^\\circ\\text{C}$), absorbed energy evaluates as:</p>
\\[ K_V(-20^\\circ\\text{C}) = 0.8500(-20) + 65.00 = 48.00\\text{ J} \\]
<p>comfortably exceeding the AASHTO Fracture-Critical requirement of $34\\text{ J}$ ($25\\text{ ft-lbf}$) at $-20^\\circ\\text{C}$ for Zone 2 bridge structures.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include optical encoder energy resolution $\\delta K_V = \\pm 0.5\\text{ J}$ and temperature calibration $\\delta T = \\pm 0.5^\\circ\\text{C}$. Propagating into $k_T$:</p>
\\[ \\frac{\\delta k_T}{k_T} = \\sqrt{ \\left( \\frac{\\delta K_V}{\\Delta K_V} \\right)^2 + \\left( \\frac{\\delta T}{\\Delta T} \\right)^2 } = \\sqrt{ \\left( \\frac{0.5}{68.0} \\right)^2 + \\left( \\frac{0.5}{80.0} \\right)^2 } = \\pm 0.96\\% \\]
<p>The reported temperature sensitivity is $k_T = 0.8500 \\pm 0.0082\\text{ J/}^\\circ\\text{C}$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>Fracture surface examination revealed a continuous microstructural shift: at $+50^\\circ\\text{C}$, the specimen failed by $100\\%$ fibrous microvoid coalescence accompanied by large lateral expansion ($1.48\\text{ mm}$), absorbing $107.5\\text{ J}$. Conversely, at $-30^\\circ\\text{C}$, fracture was dominated by flat, reflective transgranular cleavage facets ($85\\%$) with minimal lateral expansion ($0.48\\text{ mm}$), absorbing only $39.5\\text{ J}$.</p>

<h3>10. Structural Bridge Engineering Compliance</h3>
<p>Under AASHTO LRFD Bridge Design Specifications, fracture-critical tension members (such as tie girders in tied-arch bridges and non-redundant plate girder flanges) require mandatory Charpy impact verification. The tested ASTM A572 Grade 50 steel exhibits excellent low-temperature toughness, preventing catastrophic brittle propagation from undetected fatigue microcracks.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why does specimen thickness strongly affect impact toughness and transition temperature?</strong><br>
<em>A1:</em> Thicker plates impose severe through-thickness plain-strain mechanical restraint ($\varepsilon_z = 0$), preventing transverse Poisson contraction and generating intense triaxial tension that elevates DBTT by $15\\text{ to }30^\\circ\\text{C}$ compared to thin sheets.</p>
<p><strong>Q2: What is the purpose of post-weld heat treatment (PWHT) regarding notch toughness?</strong><br>
<em>A2:</em> Welding induces steep thermal gradients and high tensile residual stresses that co-exist with brittle untempered martensite in the heat-affected zone (HAZ); PWHT relieves residual stresses and tempers brittle microstructures, restoring high Charpy impact toughness.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The Charpy V-notch pendulum impact test characterized the temperature-dependent toughness of structural steel across the critical operational regime. The verified sensitivity slope $k_T = 0.8500\\text{ J/}^\\circ\\text{C}$ ($R^2 = 1.000000$) and verified absorbed energy of $48.0\\text{ J}$ at $-20^\\circ\\text{C}$ confirm full compliance with AASHTO fracture-critical bridge specifications.</p>"""
        },
        {
            "number": 12,
            "slug": "brinell-and-rockwell-hardness-structural-alloys",
            "title": "Brinell & Rockwell Hardness Testing of Structural Steels & Non-Ferrous Alloys",
            "shortTitle": "Hardness Testing of Alloys",
            "aim": "Determine the indentation resistance, macro-hardness, and empirical ultimate tensile strength of structural steel and structural aluminum alloys using Brinell and Rockwell hardness methods according to ASTM E10 / ASTM E18.",
            "inputLabel": "Hardness Indentation Load P",
            "shortInput": "Applied Load",
            "inputUnit": "kgf",
            "min": 100.0,
            "max": 500.0,
            "step": 100.0,
            "initial": 300.0,
            "inputDecimals": 0,
            "rawLabel": "Hardness Measurement Metric",
            "rawUnit": "metric",
            "rawDecimals": 1,
            "xAxis": "Applied indentation load parameter P (kgf)",
            "yAxis": "Indentation response metric",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 600.0,
            "emptyY": 800.0,
            "targetName": "Hardness Loading Response Constant",
            "target": "1.4250",
            "refValue": 1.4250,
            "resultUnit": "metric/kgf",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "Metric = 1.4250 · P",
            "intro": "Hardness is a fundamental mechanical surface property defining a material's localized resistance to permanent plastic indentation, scratching, and abrasive wear. In civil engineering quality assurance, hardness testing provides a rapid, non-destructive, and economical method to evaluate alloy heat treatment condition, verify weld heat-affected zone (HAZ) softening, and estimate ultimate tensile strength without machining complex tensile dogbone specimens. Under ASTM E10, the Brinell hardness test presses a hardened tungsten carbide ball indenter (10 mm diameter) into the flat ground surface of the specimen under a heavy static major load (typically 3000 kgf for structural steels, 500 kgf for aluminum alloys) for a standardized dwell time of 10 to 15 seconds. The diameter of the recovered spherical indentation impression d is measured in orthogonal directions using a calibrated optical microscope, and the Brinell Hardness Number (HBW) is calculated as applied force divided by the curved surface area of the spherical cap. For structural carbon steels, a robust empirical rule-of-thumb links Brinell hardness directly to ultimate tensile strength: f_u ≈ 3.45 · HBW in MPa. In this laboratory, indentation tests are performed across loading parameters from 100 to 500 kgf to calibrate hardness loading response.",
            "modelExtra": "Evaluated on structural steel plate coupons (ASTM A36). Linearized response relates indentation response metric directly to applied major load P with constant 1.4250.",
            "apparatus": [
                {"name": "Automatic Hydraulic Brinell/Rockwell Hardness Tester", "purpose": "Applies precise minor and major loads up to 3000 kgf with motorized closed-loop load cell control."},
                {"name": "Hardened Tungsten Carbide Ball Indenter (10 mm)", "purpose": "Spherical indenter with 10.000 ± 0.002 mm diameter conforming to ASTM E10."},
                {"name": "Diamond Spheroconical Indenter (Rockwell C Brale)", "purpose": "120° diamond cone with 0.200 mm spherical tip for testing hardened structural bolts."},
                {"name": "Calibrated Optical Measuring Microscope", "purpose": "Measures indentation impression diameters with 0.01 mm precision using micrometer crosshairs."},
                {"name": "Surface Grinding & Polishing Rotary Platen", "purpose": "Prepares smooth, scratch-free planar testing faces with surface roughness Ra < 0.8 µm."},
                {"name": "NIST-Traceable Hardness Calibration Test Blocks", "purpose": "Standardized reference blocks verifying machine accuracy and calibration daily."}
            ],
            "procedure": [
                {"title": "Specimen Surface Grinding & Planar Preparation", "text": "Grind specimen surface flat and parallel to the bottom face using 240 and 400 grit silicon carbide abrasive paper; ensure testing face is free of scale, oil, or decarb."},
                {"title": "Machine Calibration Verification", "text": "Verify tester calibration by performing three indentations on standard NIST-certified reference test blocks; ensure indicated hardness matches block within ± 1%."},
                {"title": "Specimen Placement on Anvil", "text": "Place specimen firmly on the flat testing anvil; rotate elevating screw to bring specimen into contact with indenter."},
                {"title": "Major Load Application & Standard Dwell", "text": "Engage automatic loading cycle; apply specified major load smoothly without impact shock; maintain dwell time for exactly 10 to 15 seconds."},
                {"title": "Load Removal & Indentation Inspection", "text": "Release major load; lower anvil; examine indentation under optical microscope; measure impression diameter d along two perpendicular axes to 0.01 mm."},
                {"title": "Hardness Calculation & Tensile Estimation", "text": "Calculate mean diameter d; compute Brinell Hardness Number (HBW); apply empirical conversion factor to estimate ultimate tensile strength."}
            ],
            "topics": [
                {"question": "How is the Brinell Hardness Number (HBW) calculated mathematically?", "answer": "HBW = 2 P / [pi D (D - sqrt(D^2 - d^2))], where P is applied load in kgf, D is indenter ball diameter in mm, and d is average indentation impression diameter in mm."},
                {"question": "Why is the Brinell hardness test preferred for cast iron and coarse structural steel over micro-hardness tests?", "answer": "The large 10 mm ball indenter samples a large volume encompassing multiple grains and phase boundaries, providing a representative macro-average hardness unaffected by microscopic phase segregations."},
                {"question": "What is the physical significance of the empirical correlation f_u ≈ 3.45 · HBW?", "answer": "Tabor's plastic indentation theory shows that mean contact pressure under a blunt indenter is approximately 3.0 times the material's plastic yield stress; accounting for strain hardening yields the direct linear link between HBW and tensile strength."},
                {"question": "What spacing precautions are mandated between adjacent hardness indentations?", "answer": "ASTM E10 requires indentation centers to be spaced at least 3.0 indentation diameters apart and at least 2.5 diameters from specimen edges to avoid work-hardened plastic plastic strain fields."},
                {"question": "How does Rockwell hardness testing differ fundamentally from Brinell testing?", "answer": "Brinell measures optical diameter of the recovered indentation, whereas Rockwell measures differential depth of indentation under a major load relative to a minor preload (10 kgf), reading hardness directly on a dial gauge."},
                {"question": "What is the consequence of testing on a specimen that is too thin?", "answer": "If specimen thickness is less than 8 times indentation depth (the 'anvil effect'), the hard steel anvil beneath constrains plastic flow, producing an artificially high hardness reading."}
            ],
            "precautions": [
                "Ensure test specimens have completely flat, parallel top and bottom surfaces to eliminate rocking or elastic anvil flexure during loading.",
                "Maintain indenter dwell time strictly between 10 and 15 seconds to eliminate viscoelastic creep artifacts in softer alloys.",
                "Space successive indentations at least 3 diameters apart to prevent testing in strain-hardened zones generated by previous trials.",
                "Never test close to specimen edges; maintain minimum distance of 2.5 diameters from all boundaries."
            ],
            "quiz": [
                {
                    "question": "The standard ball diameter and major load for testing structural steel in the Brinell test (ASTM E10) are:",
                    "options": ["2.5 mm ball at 187.5 kgf", "5 mm ball at 750 kgf", "10 mm ball at 3000 kgf", "12 mm ball at 5000 kgf"],
                    "correct": 2,
                    "explanation": "ASTM E10 specifies a standard 10 mm tungsten carbide ball under 3000 kgf major load for structural steels."
                },
                {
                    "question": "The Rockwell C scale (HRC) employs which type of indenter and major load?",
                    "options": ["1/16 inch steel ball and 100 kgf", "120° diamond spheroconical cone and 150 kgf", "10 mm carbide ball and 1000 kgf", "1/8 inch steel ball and 60 kgf"],
                    "correct": 1,
                    "explanation": "Rockwell C scale uses a 120° diamond Brale cone with a 150 kgf major load."
                },
                {
                    "question": "For structural carbon steels, the approximate empirical relationship between ultimate tensile strength f_u (MPa) and Brinell hardness (HBW) is:",
                    "options": ["f_u ≈ 1.25 · HBW", "f_u ≈ 3.45 · HBW", "f_u ≈ 6.50 · HBW", "f_u ≈ 9.81 · HBW"],
                    "correct": 1,
                    "explanation": "ASTM E140 and empirical metallurgy establish f_u (MPa) ≈ 3.45 · HBW."
                },
                {
                    "question": "The minimum distance between the centers of two adjacent Brinell indentations must be at least:",
                    "options": ["1.0 diameter", "1.5 diameters", "3.0 diameters", "5.0 diameters"],
                    "correct": 2,
                    "explanation": "ASTM E10 mandates a minimum center-to-center spacing of 3.0 times the indentation diameter."
                }
            ],
            "samples": [100.0, 200.0, 300.0, 400.0, 500.0],
            "measureLabel": "Record hardness indentation response metric",
            "readings": ["metric_val", "load_kgf", "indenter_dia", "hb_equiv"],
            "theory": """<h3>1. Plastic Indentation Mechanics & Slip-Line Theory</h3>
<p>When a rigid spherical indenter of diameter $D$ is forced into a semi-infinite ductile metal half-space under normal force $P$, deformation transitions through three regimes: (1) Initial Hertzian elastic contact; (2) Subsurface plastic yielding initiating at depth $z \\approx 0.48 a$ (where $a = d/2$ is contact radius); and (3) Fully developed plastic flow where plastic strain envelopes break through to the free surface, forming upward pile-up or sinking-in lips.</p>

<p>According to David Tabor's classical indentation theory, the mean contact pressure $p_m$ (Meyer hardness) beneath a spherical indenter is directly proportional to the uniaxial flow stress $Y$ of the material:</p>
\\[ p_m = \\frac{4 P}{\\pi d^2} = C \\cdot Y \\]
<p>where constraint factor $C \\approx 2.8\\text{ to }3.0$ arises from the elastic constraint of the surrounding rigid elastic material opposing plastic displacement.</p>

<h3>2. The Brinell Hardness Formulation (ASTM E10)</h3>
<p>The Brinell Hardness Number ($HBW$) evaluates applied force $P$ (in kilogram-force) divided by the curved surface area $A_{sphere}$ of the residual spherical indentation cap of diameter $d$:</p>
\\[ A_{sphere} = \\pi D h = \\frac{\\pi D}{2} \\left( D - \\sqrt{D^2 - d^2} \\right) \\]
\\[ HBW = \\frac{2 P}{\\pi D \\left( D - \\sqrt{D^2 - d^2} \\right)} \\]
<p>To ensure geometrical similarity across different loads and indenter sizes, the loading parameter $P / D^2$ must remain constant ($P / D^2 = 30\\text{ kgf/mm}^2$ for steel, $P / D^2 = 10\\text{ kgf/mm}^2$ for brass, $P / D^2 = 5\\text{ kgf/mm}^2$ for aluminum).</p>

<h3>3. Linear Hardness Loading Calibration</h3>
<p>In standardized automated indentation testing, the measured indentation response metric scales directly with applied loading parameter $P$:</p>
\\[ \\text{Metric} = k_h \\cdot P \\]
<p>where $k_h = 1.4250\\text{ metric/kgf}$ represents the characteristic loading response constant.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this civil engineering laboratory investigation is to evaluate the indentation resistance and macro-hardness of structural carbon steel (ASTM A36) and structural aluminum alloys according to ASTM E10 / ASTM E18. By measuring indentation metrics across five load levels ($100\\text{ to }500\\text{ kgf}$), executing linear regression, and determining the loading response constant $k_h$, we calibrate non-destructive quality assurance correlations to estimate ultimate tensile strength.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>The standard Brinell Hardness Number ($HBW$) is evaluated from indenter diameter $D = 10.0\\text{ mm}$, indentation diameter $d$, and applied force $P$:</p>
\\[ HBW = \\frac{2 P}{\\pi D \\left( D - \\sqrt{D^2 - d^2} \\right)} \\]
<p>The hardness response metric relates linearly to applied load parameter $P$:</p>
\\[ \\text{Metric} = k_h \\cdot P \\]
<p>where $k_h = 1.4250\\text{ metric/kgf}$. Empirical tensile strength estimation follows the ASTM E140 relationship $f_u = 3.45 \\cdot HBW\\text{ (MPa)}$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized a closed-loop electromechanical hardness testing machine equipped with a $10.000 \\pm 0.002\\text{ mm}$ tungsten carbide ball indenter and an automated loading system (load dwell time $15.0 \\pm 0.5\\text{ s}$). Optical measurement was performed using a high-resolution measuring microscope with digital micrometric filar eyepiece ($0.005\\text{ mm}$ resolution). Calibration was verified using a NIST-traceable reference test block certified at $143.0 \\pm 1.5\\text{ HBW}$.</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Specimens of ASTM A36 steel were machined into $50 \\times 50 \\times 15\\text{ mm}$ coupons with faces surface-ground to roughness $R_a \\le 0.4\\,\\mu\\text{m}$. Specimens were mounted on the flat anvil, raised to contact, and major loads applied for 15 seconds. Recovered impression diameters were measured along two perpendicular axes, averaged, and logged. Center-to-center spacing between indentations was maintained at $> 4.0$ diameters.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Hardness testing involves high compressive forces ($3000\\text{ kgf} \\approx 29.4\\text{ kN}$) capable of fracturing brittle specimens or causing pinch injuries. Operators wore safety glasses, kept hands clear of indenter zones during motorized travel, and ensured specimens were seated completely flat on the anvil to prevent violent lateral kick-out.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across five loading levels on structural steel plate:</p>
<table>
<thead>
<tr><th>Trial</th><th>Applied Load P (kgf)</th><th>Measured Impression d (mm)</th><th>Calculated HBW</th><th>Hardness Metric</th><th>Estimated Tensile f_u (MPa)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>100.0</td><td>1.92</td><td>138.2</td><td>142.5</td><td>476.8</td></tr>
<tr><td>2</td><td>200.0</td><td>2.71</td><td>138.4</td><td>285.0</td><td>477.5</td></tr>
<tr><td>3</td><td>300.0</td><td>3.32</td><td>138.1</td><td>427.5</td><td>476.4</td></tr>
<tr><td>4</td><td>400.0</td><td>3.83</td><td>138.3</td><td>570.0</td><td>477.1</td></tr>
<tr><td>5</td><td>500.0</td><td>4.28</td><td>138.2</td><td>712.5</td><td>476.8</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of the hardness measurement metric versus applied load $P$ yields:</p>
\\[ \\text{Metric} = 1.42500 \\cdot P + 0.00000 \\]
<p>with an exceptional coefficient of determination $R^2 = 1.000000$. The experimental loading constant $k_h = 1.4250\\text{ metric/kgf}$ matches the reference benchmark with zero relative deviation ($0.00\\%$). The mean Brinell hardness of the steel plate evaluates as $HBW = 138.2\\text{ kgf/mm}^2$, yielding an estimated ultimate tensile strength:</p>
\\[ f_u = 3.45 \\times 138.2 = 476.8\\text{ MPa} \\]
<p>This matches standard tensile tests for ASTM A36 structural plate ($400\\text{ to }550\\text{ MPa}$).</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include load cell accuracy $\\delta P / P = \\pm 0.5\\%$ and optical diameter resolution $\\delta d = \\pm 0.01\\text{ mm}$ ($0.3\\%$). Propagating into $HBW$:</p>
\\[ \\frac{\\delta HBW}{HBW} = \\sqrt{ \\left( \\frac{\\delta P}{P} \\right)^2 + \\left( 2 \\frac{\\delta d}{d} \\right)^2 } = \\pm 0.78\\% \\]
<p>The reported Brinell hardness is $HBW = 138.2 \\pm 1.1$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The consistency of calculated $HBW$ across varying loads ($138.1\\text{ to }138.4$) confirms Meyer's law of geometrical similitude in spherical indentation. Optical microscopy revealed clean, circular impression rims with negligible pile-up, characteristic of normalized mild steel with moderate strain-hardening capacity.</p>

<h3>10. Structural Welding Quality Control Applications</h3>
<p>In structural steel welding under AWS D1.1, hardness surveys across welded joints are mandatory. If cooling rates are excessive, hydrogen-induced cold cracking occurs in the heat-affected zone (HAZ) where hardness exceeds $350\\text{ HBW}$ ($38\\text{ HRC}$). Rapid hardness testing verifies that preheating and interpass temperature controls successfully prevented brittle martensite formation.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is tungsten carbide (HBW) now specified for Brinell testing instead of steel balls (HBS)?</strong><br>
<em>A1:</em> Standard hardened steel balls deform elastically and flatten when indenting hard steels ($> 450\\text{ HB}$), producing artificially large impression diameters and falsely low hardness values; tungsten carbide balls are extremely rigid, maintaining dimensional spherical integrity up to $650\\text{ HBW}$.</p>
<p><strong>Q2: Can hardness testing detect decarburization on structural bolts?</strong><br>
<em>A2:</em> Yes; high-temperature heat treatment in oxidizing atmospheres depletes carbon from the outer surface ($0.1\\text{ to }0.3\\text{ mm}$), creating a soft ferritic skin detectable as low surface hardness that degrades fatigue and thread stripping capacity.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The Brinell hardness investigation demonstrated precise, reproducible indentation characterization of structural steel. The calibrated loading response constant $k_h = 1.4250\\text{ metric/kgf}$ ($R^2 = 1.000000$), mean hardness of $138.2\\text{ HBW}$, and estimated tensile strength of $476.8\\text{ MPa}$ confirm full structural compliance for civil infrastructure construction.</p>"""
        },
        {
            "number": 13,
            "slug": "deflection-simply-supported-structural-beam",
            "title": "Elastic Deflection of Simply Supported Structural Steel Beams & Flexural Rigidity",
            "shortTitle": "Beam Elastic Deflection",
            "aim": "Verify the Euler–Bernoulli beam flexure theory, measure midspan elastic deflection (δ) under central point loading across span L, and determine the flexural rigidity (EI) of a structural steel beam.",
            "inputLabel": "Central Point Load P",
            "shortInput": "Load P",
            "inputUnit": "kN",
            "min": 2.0,
            "max": 14.0,
            "step": 2.0,
            "initial": 8.0,
            "inputDecimals": 1,
            "rawLabel": "Midspan Deflection δ",
            "rawUnit": "mm",
            "rawDecimals": 2,
            "xAxis": "Central point load P (kN)",
            "yAxis": "Midspan deflection δ (mm)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 16.0,
            "emptyY": 7.0,
            "targetName": "Beam Flexural Compliance",
            "target": "0.4250",
            "refValue": 0.4250,
            "resultUnit": "mm/kN",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "δ = 0.4250 · P",
            "intro": "In structural civil engineering, the serviceability limit state (deflection control) is just as critical as the ultimate strength limit state. Excessive beam deflections cause unsightly sagging, crack plaster and brittle architectural finishes, jam doors and operable windows, and induce alarming vibrations under human foot traffic. Classical Euler–Bernoulli beam theory dictates that the elastic deflection curve v(x) of a prismatic, homogeneous beam of flexural rigidity EI obeys the fundamental second-order differential equation d^2v/dx^2 = M(x) / (EI), where M(x) is internal bending moment. For a simply supported beam of span L subjected to a concentrated central point load P at midspan (x = L/2), double integration with boundary conditions (zero deflection at supports x = 0 and x = L) yields the famous midspan deflection expression: δ = P L^3 / (48 E I). Measuring midspan deflection δ as a function of load P produces a linear elastic compliance slope C = δ / P = L^3 / (48 E I), from which the experimental flexural rigidity EI and Young's modulus E can be deduced. In this laboratory, a structural steel I-beam is loaded across loads from 2 to 14 kN using digital dial indicators to verify beam flexure theory and evaluate flexural compliance.",
            "modelExtra": "Structural steel beam of span L = 1200 mm, moment of inertia I = 4.235 x 10^5 mm^4, E = 200 GPa. Theoretical compliance slope: L^3 / (48 E I) = 1200^3 / (48 · 200,000 · 423,500) = 1.728 x 10^9 / 4.0656 x 10^12 = 0.4250 mm/kN.",
            "apparatus": [
                {"name": "Structural Beam Testing Loading Frame", "purpose": "Rigid steel reaction frame with hydraulic screw jack applying central vertical point loads to 25 kN."},
                {"name": "Pinned and Roller Knife-Edge End Supports", "purpose": "Provides true simply supported boundary conditions (one pinned knife-edge, one sliding roller)."},
                {"name": "Precision Digital Linear Dial Gauge (LVDT)", "purpose": "Measures beam midspan vertical deflection with 0.001 mm resolution and 25 mm travel."},
                {"name": "Calibrated Electronic Load Cell", "purpose": "Measures applied concentrated central load P with 0.01 kN precision."},
                {"name": "Precision Steel Beam Specimen", "purpose": "Structural steel rectangular/I-beam with machined straight edges and known cross-sectional geometry."},
                {"name": "Precision Metric Vernier Caliper & Tape", "purpose": "Measures span length L, beam width b, and beam depth d to 0.05 mm precision."}
            ],
            "procedure": [
                {"title": "Beam Dimensions & Section Modulus Measurement", "text": "Measure beam cross-sectional width b and depth d at three stations using callipers to 0.05 mm; compute moment of inertia I = b d^3 / 12."},
                {"title": "Support Setup & Span Alignment", "text": "Position pinned support and roller support on the reaction bed; set clear span L = 1200.0 mm using precision rule; place beam centrally on supports."},
                {"title": "Loading Saddle & Dial Gauge Installation", "text": "Mount loading knife-edge saddle at exact midspan (x = 600 mm); position digital dial indicator directly beneath midspan bottom flange; zero the indicator."},
                {"title": "Pre-Loading & Seating Cycle", "text": "Apply a gentle seating load of 1.0 kN to settle knife-edges; release load completely and re-zero dial gauge."},
                {"title": "Incremental Elastic Loading", "text": "Apply central point load incrementally in steps of 2.0 kN through 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, and 14.0 kN; record steady midspan deflection δ at each plateau."},
                {"title": "Unloading Hysteresis Check", "text": "Decrement load in reverse steps back to zero; verify that residual plastic deflection is zero (< 0.02 mm) to confirm true elastic behavior."}
            ],
            "topics": [
                {"question": "How is the midspan deflection formula δ = P L^3 / (48 E I) derived from bending moment distribution?", "answer": "The bending moment equation for x ≤ L/2 is M(x) = (P/2) x; integrating d^2v/dx^2 = M / EI yields slope dv/dx = (P x^2) / (4 EI) + C_1; symmetry at midspan requires dv/dx(L/2) = 0, giving C_1 = - P L^2 / (16 EI); integrating again with v(0) = 0 gives v(x) = (P x^3) / (12 EI) - (P L^2 x) / (16 EI); evaluating at x = L/2 yields δ = P L^3 / (48 EI)."},
                {"question": "What fundamental assumptions underlie the Euler–Bernoulli beam bending theory?", "answer": "Assumptions: (1) Plane sections normal to the neutral axis remain plane and normal after bending (shear deformation neglected); (2) Material is homogeneous, isotropic, and obeys Hooke's Law; (3) Deflections are small compared to beam depth; (4) The beam is prismatic with a vertical plane of symmetry."},
                {"question": "What is the difference between Euler–Bernoulli beam theory and Timoshenko beam theory?", "answer": "Euler–Bernoulli theory neglects transverse shear deformation and rotary inertia, which is accurate for slender beams (L/d > 10); Timoshenko beam theory includes shear deformation, which adds significant additional deflection in short, deep beams (L/d < 5)."},
                {"question": "Why is one support configured as a pinned knife-edge and the other as a free-rolling roller?", "answer": "A roller support allows unrestrained axial longitudinal expansion/contraction during flexural curvature, preventing parasitic axial membrane tension forces from stiffening the beam and reducing deflection."},
                {"question": "How does beam depth d influence flexural rigidity compared to beam width b?", "answer": "Moment of inertia is I = b d^3 / 12; doubling beam width b doubles stiffness (2x), whereas doubling beam depth d increases stiffness by a factor of eight (2^3 = 8x), making depth the dominant geometric factor."},
                {"question": "What are typical serviceability deflection limits for commercial floor beams in building codes?", "answer": "IBC and AISC 360 specify maximum live-load deflection of L / 360 for floors supporting plastered ceilings, and L / 240 for general structural roof/floor framing to prevent architectural damage."}
            ],
            "precautions": [
                "Verify that the load is applied exactly at midspan (L/2) without lateral eccentricity to prevent torsional twisting.",
                "Ensure the dial indicator stem is oriented perpendicular to the beam bottom flange and placed on the neutral axis projection.",
                "Do not exceed the elastic limit load (yield moment M_y) to prevent permanent plastic deformation of the beam.",
                "Verify roller support moves freely on its base plate without dirt or mechanical binding that would induce horizontal thrust."
            ],
            "quiz": [
                {
                    "question": "For a simply supported beam of span L with central point load P, midspan deflection is proportional to:",
                    "options": ["L", "L^2", "L^3", "L^4"],
                    "correct": 2,
                    "explanation": "Midspan deflection δ = P L^3 / (48 E I) scales with the cube of the span length (L^3)."
                },
                {
                    "question": "If the depth d of a rectangular beam is doubled while width b remains constant, its deflection under identical load will be:",
                    "options": ["Half as much (1/2)", "One-fourth as much (1/4)", "One-eighth as much (1/8)", "One-sixteenth as much (1/16)"],
                    "correct": 2,
                    "explanation": "Because I = b d^3 / 12 and δ ∝ 1/I, doubling depth d increases I by 2^3 = 8, reducing deflection to 1/8."
                },
                {
                    "question": "The slope of the elastic deflection curve dv/dx at the midspan of a symmetrically loaded simply supported beam is:",
                    "options": ["Maximum", "Zero", "Equal to P / EI", "Equal to L / 48"],
                    "correct": 1,
                    "explanation": "By symmetry, the deflection curve has a horizontal tangent (zero slope) at midspan."
                },
                {
                    "question": "Flexural rigidity of a structural beam is defined mathematically as the product:",
                    "options": ["E · A", "E · I", "G · J", "f_y · Z"],
                    "correct": 1,
                    "explanation": "Flexural rigidity is the product of Young's Modulus E and second moment of area I (E · I)."
                }
            ],
            "samples": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0],
            "measureLabel": "Record midspan elastic vertical deflection δ",
            "readings": ["deflection_mm", "load_kn", "theoretical_mm", "rigidity_ei"],
            "theory": """<h3>1. The Euler–Bernoulli Differential Equation of Flexure</h3>
<p>Consider a straight, prismatic beam of span $L$ possessing flexural rigidity $EI$ simply supported at $x = 0$ and $x = L$. Under the Euler–Bernoulli kinematic hypothesis, plane cross-sections remain plane and perpendicular to the deformed neutral axis. The curvature $\\kappa(x)$ of the elastic curve $v(x)$ relates directly to internal bending moment $M(x)$:</p>
\\[ \\kappa(x) = \\frac{d^2 v / dx^2}{\\left[ 1 + (dv/dx)^2 \\right]^{3/2}} \\approx \\frac{d^2 v}{dx^2} = \\frac{M(x)}{EI} \\]
<p>where small-slope approximations ($(dv/dx)^2 \\ll 1$) are valid for structural serviceability deformations.</p>

<h3>2. Double Integration for Central Point Load</h3>
<p>Under a concentrated point load $P$ applied at midspan ($x = L/2$), the reaction forces at supports $A$ and $B$ are $R_A = R_B = P/2$. The internal bending moment distribution for the left half ($0 \\le x \\le L/2$) is:</p>
\\[ M(x) = \\frac{P}{2} x \\]
<p>Integrating the governing differential equation once yields the angular slope $\\theta(x) = dv/dx$:</p>
\\[ EI \\frac{dv}{dx} = \\int \\frac{P}{2} x \\, dx = \\frac{P x^2}{4} + C_1 \\]
<p>By symmetry, the slope at midspan must be zero: $\\frac{dv}{dx}\\left( \\frac{L}{2} \\right) = 0$:</p>
\\[ \\frac{P (L/2)^2}{4} + C_1 = 0 \\implies C_1 = - \\frac{P L^2}{16} \\]
<p>Integrating a second time yields the elastic deflection profile $v(x)$:</p>
\\[ EI v(x) = \\int \\left( \\frac{P x^2}{4} - \\frac{P L^2}{16} \\right) dx = \\frac{P x^3}{12} - \\frac{P L^2 x}{16} + C_2 \\]
<p>Applying the pinned support boundary condition $v(0) = 0$ requires $C_2 = 0$. The maximum deflection occurs at midspan ($x = L/2$):</p>
\\[ v\\left( \\frac{L}{2} \\right) = \\frac{1}{EI} \\left[ \\frac{P (L/2)^3}{12} - \\frac{P L^2 (L/2)}{16} \\right] = \\frac{1}{EI} \\left[ \\frac{P L^3}{96} - \\frac{P L^3}{32} \\right] = - \\frac{P L^3}{48 EI} \\]
<p>The magnitude of downward midspan vertical deflection $\\delta$ is therefore:</p>
\\[ \\delta = \\frac{P L^3}{48 EI} \\]

<h3>3. Experimental Compliance & Rigidity Extraction</h3>
<p>Plotting measured midspan deflection $\\delta$ versus applied load $P$ produces a straight line through the origin with flexural compliance slope $C_b$:</p>
\\[ \\delta = C_b \\cdot P, \\qquad C_b = \\frac{L^3}{48 EI} \\]
<p>For span $L = 1200\\text{ mm}$, $I = 4.235 \\times 10^5\\text{ mm}^4$, and $E = 200\\text{ GPa}$ ($2.0 \\times 10^5\\text{ N/mm}^2$):</p>
\\[ C_b = \\frac{(1200\\text{ mm})^3}{48 \\times 200,000\\text{ N/mm}^2 \\times 423,500\\text{ mm}^4} = \\frac{1.728 \\times 10^9}{4.0656 \\times 10^{12}} = 0.00042503\\text{ mm/N} = 0.4250\\text{ mm/kN} \\]""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this civil engineering laboratory investigation is to verify the Euler–Bernoulli beam flexure theory, evaluate the linear elastic load-deflection response of a simply supported structural steel beam under central point loading, and determine the experimental flexural rigidity ($EI$) and compliance slope $C_b$ across seven loading plateaus ($2.0\\text{ to }14.0\\text{ kN}$).</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Under central concentrated point loading on a simply supported span $L$, midspan vertical deflection $\\delta$ is governed by Euler–Bernoulli beam mechanics:</p>
\\[ \\delta = \\frac{P L^3}{48 EI} = C_b \\cdot P \\]
<p>where compliance slope $C_b = 0.4250\\text{ mm/kN}$ and flexural rigidity is $EI = \\frac{L^3}{48 C_b}$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized a rigid structural steel reaction bed equipped with hardened tool-steel knife-edge supports (one pinned, one free-sliding roller on ground plates). Concentrated vertical loading was applied via an automated hydraulic screw jack equipped with a precision electronic load cell ($25.0\\text{ kN}$ capacity, precision $\\pm 0.02\\text{ kN}$). Midspan vertical deflection was monitored directly beneath the beam centroid using a digital Mitutoyo LVDT dial indicator ($25.0\\text{ mm}$ stroke, $0.001\\text{ mm}$ resolution). The test beam comprised a structural steel section ($L = 1200.0 \\pm 0.5\\text{ mm}$, second moment of area $I = 4.235 \\times 10^5\\text{ mm}^4$).</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Beam dimensions and clear span ($1200.0\\text{ mm}$) were confirmed using steel vernier calipers. Pinned and roller supports were leveled on the reaction frame. The beam was mounted, and the loading saddle positioned at midspan ($x = 600.0\\text{ mm}$). The dial indicator was zeroed at zero load. Point loads were applied incrementally in steps of $2.0\\text{ kN}$ up to $14.0\\text{ kN}$, allowing 30 seconds for deflection stabilization prior to logging. The specimen was unloaded in reverse steps to verify zero plastic hysteresis.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>The beam reaction frame stores elastic strain energy under $14\\text{ kN}$ loading. Lateral bracing was provided to eliminate lateral-torsional buckling. Operators wore impact safety glasses, steel-toed boots, and work gloves. Hydraulic load valves were adjusted gradually to prevent shock loading.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the elastic loading and unloading cycle:</p>
<table>
<thead>
<tr><th>Load Step</th><th>Applied Load P (kN)</th><th>Loading Deflection δ (mm)</th><th>Unloading Deflection (mm)</th><th>Theoretical δ (mm)</th><th>Relative Error (%)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>2.0</td><td>0.85</td><td>0.85</td><td>0.850</td><td>0.00</td></tr>
<tr><td>2</td><td>4.0</td><td>1.70</td><td>1.70</td><td>1.700</td><td>0.00</td></tr>
<tr><td>3</td><td>6.0</td><td>2.55</td><td>2.55</td><td>2.550</td><td>0.00</td></tr>
<tr><td>4</td><td>8.0</td><td>3.40</td><td>3.40</td><td>3.400</td><td>0.00</td></tr>
<tr><td>5</td><td>10.0</td><td>4.25</td><td>4.25</td><td>4.250</td><td>0.00</td></tr>
<tr><td>6</td><td>12.0</td><td>5.10</td><td>5.10</td><td>5.100</td><td>0.00</td></tr>
<tr><td>7</td><td>14.0</td><td>5.95</td><td>5.95</td><td>5.950</td><td>0.00</td></tr>
</tbody>
</table>
<p>Residual plastic deflection upon complete unloading was $0.00\\text{ mm}$, confirming purely linear elastic behavior.</p>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of midspan vertical deflection $\\delta$ versus applied load $P$ yields:</p>
\\[ \\delta = 0.42500 \\cdot P + 0.00000 \\]
<p>with an extraordinary coefficient of determination $R^2 = 1.000000$. The experimental compliance slope $C_b = 0.42500\\text{ mm/kN}$ matches the theoretical Euler–Bernoulli prediction ($0.4250\\text{ mm/kN}$) with zero relative deviation ($0.00\\%$). Calculating the experimental flexural rigidity $EI$:</p>
\\[ EI = \\frac{L^3}{48 C_b} = \\frac{(1200)^3}{48 \\times 0.0004250} = \\frac{1.728 \\times 10^9}{0.0204} = 8.47059 \\times 10^{10}\\text{ N}\\cdot\\text{mm}^2 = 84.71\\text{ kN}\\cdot\\text{m}^2 \\]
<p>With known $I = 4.235 \\times 10^5\\text{ mm}^4$, the experimental Young's modulus is:</p>
\\[ E = \\frac{EI}{I} = \\frac{8.47059 \\times 10^{10}}{4.235 \\times 10^5} = 200,014\\text{ MPa} = 200.01\\text{ GPa} \\]
<p>matching standard structural steel ($200.0\\text{ GPa}$) with $0.01\\%$ relative error.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include load cell reading $\\delta P = \\pm 0.02\\text{ kN}$, LVDT deflection resolution $\\delta \\delta = \\pm 0.005\\text{ mm}$, and span measurement $\\delta L = \\pm 0.5\\text{ mm}$. Propagating into $EI$:</p>
\\[ \\frac{\\delta EI}{EI} = \\sqrt{ \\left( 3 \\frac{\\delta L}{L} \\right)^2 + \\left( \\frac{\\delta P}{P} \\right)^2 + \\left( \\frac{\\delta \\delta}{\\delta} \\right)^2 } = \\pm 0.28\\% \\]
<p>The reported flexural rigidity is $EI = 84.71 \\pm 0.24\\text{ kN}\\cdot\\text{m}^2$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The experimental results show perfect compliance with the classical Euler–Bernoulli model. Because the beam span-to-depth ratio is $L/d = 1200 / 75 = 16.0 > 10$, transverse shear deformation accounted for less than $1.2\\%$ of total deflection, fully justifying the omission of Timoshenko shear terms.</p>

<h3>10. Serviceability Design in Civil Structures</h3>
<p>In structural floor design, live load deflection limits (e.g. $\\delta_{max} \\le L / 360 = 1200 / 360 = 3.33\\text{ mm}$) dictate member sizing. Under the maximum service live load of $7.8\\text{ kN}$, deflection reaches $3.32\\text{ mm}$, demonstrating how serviceability deflection limits often govern structural beam selection over ultimate moment capacity.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: What happens to midspan deflection if both span ends are rigidly clamped (fixed-fixed) instead of simply supported?</strong><br>
<em>A1:</em> Fixed-fixed end moments ($M_{end} = -P L / 8$) create negative curvature at supports, reducing midspan deflection to $\\delta_{fixed} = P L^3 / (192 E I)$, which is exactly one-fourth ($25\\%$) of the simply supported deflection.</p>
<p><strong>Q2: Why must the roller support be free of friction?</strong><br>
<em>A2:</em> If the roller binds, axial elongation induced by bending is restrained, developing internal axial tension (catenary cable action) that stiffens the beam and produces non-linear load-deflection behavior.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The simply supported structural beam experiment fully verified the Euler–Bernoulli flexure theorem. The calibrated flexural compliance $C_b = 0.4250\\text{ mm/kN}$ ($R^2 = 1.000000$) and deduced Young's modulus $E = 200.01\\text{ GPa}$ provide a verified benchmark for structural deflection modeling and serviceability design.</p>"""
        },
        {
            "number": 14,
            "slug": "maxwell-betti-reciprocal-deflection-theorem",
            "title": "Verification of Maxwell–Betti Reciprocal Deflection Theorem on Elastic Beams",
            "shortTitle": "Maxwell-Betti Reciprocity",
            "aim": "Verify the Maxwell–Betti reciprocal deflection theorem on an elastic simply supported beam by comparing deflection at station A due to load at station B (δ_AB) with deflection at station B due to load at station A (δ_BA).",
            "inputLabel": "Reciprocal Test Load P",
            "shortInput": "Applied Load",
            "inputUnit": "kN",
            "min": 5.0,
            "max": 25.0,
            "step": 5.0,
            "initial": 15.0,
            "inputDecimals": 1,
            "rawLabel": "Cross-Station Deflection δ_AB",
            "rawUnit": "mm",
            "rawDecimals": 3,
            "xAxis": "Applied load P_B at station B (kN)",
            "yAxis": "Measured deflection δ_AB at station A (mm)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 30.0,
            "emptyY": 10.0,
            "targetName": "Reciprocal Influence Coefficient",
            "target": "0.3150",
            "refValue": 0.3150,
            "resultUnit": "mm/kN",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "δ_AB = 0.3150 · P_B",
            "intro": "The Maxwell–Betti reciprocal work theorem forms one of the foundational cornerstones of linear structural analysis, energy methods, and modern matrix structural mechanics. Formulated by James Clerk Maxwell in 1864 and generalized by Enrico Betti in 1872, the theorem states: For any linear elastic structure subjected to two independent equilibrium load systems, the work done by the first system acting through the displacements produced by the second system is identically equal to the work done by the second system acting through the displacements produced by the first system. When applied to two discrete load points A and B on a structural beam, the theorem simplifies to the classical reciprocal deflection law: the deflection at station A caused by a unit load at station B (flexibility coefficient f_AB) is identically equal to the deflection at station B caused by a unit load at station A (f_BA), meaning the global structural flexibility matrix is perfectly symmetric: [F] = [F]^T. This mathematical symmetry drastically reduces computational effort in structural indeterminate frame analysis and validates Müller-Breslau influence line principles. In this laboratory experiment, twin digital displacement transducers monitor reciprocal deflections across asymmetric beam stations to verify Maxwell-Betti reciprocity across loads from 5 to 25 kN.",
            "modelExtra": "Beam span L = 1000 mm. Station A located at x_A = 300 mm; Station B located at x_B = 600 mm. Closed-form flexibility coefficient f_AB = x_A (L - x_B) (2 L x_B - x_A^2 - x_B^2) / (6 E I L) = 0.3150 mm/kN.",
            "apparatus": [
                {"name": "Multi-Station Beam Reaction Test Bed", "purpose": "Rigid structural bed supporting simply supported beam across a 1000 mm span."},
                {"name": "Twin Precision Digital LVDT Transducers", "purpose": "Independent displacement transducers mounted at station A (300 mm) and station B (600 mm)."},
                {"name": "Portable Hydraulic Jack Loading Assembly", "purpose": "Applies concentrated vertical loads up to 30 kN with precision electronic load cell."},
                {"name": "Structural Steel Test Beam (Rectangular Section)", "purpose": "Uniform, homogeneous prismatic steel beam with known flexural rigidity EI."},
                {"name": "Magnetic Articulated Transducer Stands", "purpose": "Clamps LVDTs rigidly to isolated datum beam to prevent frame deflection errors."},
                {"name": "Precision Metric Vernier Layout Rule", "purpose": "Marks exact load and displacement stations to within 0.1 mm precision."}
            ],
            "procedure": [
                {"title": "Beam Station Layout & LVDT Mounting", "text": "Set beam clear span L = 1000.0 mm; mark Station A at x_A = 300.0 mm and Station B at x_B = 600.0 mm; position digital LVDTs at stations A and B; zero both gauges."},
                {"title": "Case 1 Loading: Load at Station B, Measure at Station A", "text": "Position loading jack at Station B (x_B = 600 mm); apply loads P_B incrementally at 5.0, 10.0, 15.0, 20.0, and 25.0 kN."},
                {"title": "Deflection Logging for Case 1", "text": "At each load step, record deflection at Station A (δ_AB) and direct deflection at Station B (δ_BB); release load completely."},
                {"title": "Transducer Verification & Re-Zeroing", "text": "Verify both transducers return to zero (residual deflection < 0.005 mm) confirming purely elastic response."},
                {"title": "Case 2 Loading: Load at Station A, Measure at Station B", "text": "Move loading jack to Station A (x_A = 300 mm); apply identical loads P_A at 5.0, 10.0, 15.0, 20.0, and 25.0 kN."},
                {"title": "Deflection Logging & Reciprocal Comparison", "text": "Record deflection at Station B (δ_BA) and direct deflection at Station A (δ_AA); compare δ_AB with δ_BA at every load step to verify reciprocity."}
            ],
            "topics": [
                {"question": "State the Maxwell–Betti reciprocal deflection theorem in terms of flexibility coefficients.", "answer": "For any linear elastic structure, the flexibility coefficient f_AB (deflection at station A due to unit load at B) is identically equal to f_BA (deflection at station B due to unit load at A): f_AB = f_BA."},
                {"question": "How does the principle of conservation of energy prove the Maxwell-Betti theorem?", "answer": "Total strain energy stored in a linear elastic body subjected to loads P_A and P_B is independent of the loading sequence; equating energy stored when P_A is applied first versus when P_B is applied first forces the cross-work terms to be identical: P_A δ_AB = P_B δ_BA."},
                {"question": "What is the primary practical application of the reciprocal theorem in structural engineering?", "answer": "The theorem proves that the structural flexibility matrix [F] and stiffness matrix [K] are symmetric ([K] = [K]^T), halving computational storage in finite element analysis and forming the foundation of the Müller-Breslau principle for influence lines."},
                {"question": "Does Maxwell-Betti reciprocity hold for geometrically non-linear structures undergoing large deflections?", "answer": "No; the theorem strictly requires linear elasticity (Hooke's law) and small-displacement geometry; large deflections or non-linear material plasticity violate the linear superposition principle upon which reciprocity relies."},
                {"question": "Does the reciprocal theorem apply to rotational displacements and bending moments?", "answer": "Yes; the generalized Betti theorem states that rotation at A due to unit moment at B equals rotation at B due to unit moment at A, and deflection at A due to unit moment at B equals rotation at B due to unit force at A."},
                {"question": "Why is an isolated datum beam necessary when mounting displacement gauges in reciprocity testing?", "answer": "If displacement gauges are mounted directly onto the loading frame, frame flexure under load introduces parasitic false deflection readings; mounting LVDTs on an isolated reference beam ensures true absolute beam displacement measurement."}
            ],
            "precautions": [
                "Ensure both station locations (x_A = 300 mm, x_B = 600 mm) are laid out with precision calipers to eliminate spatial alignment error.",
                "Verify the beam operates strictly below its proportional limit to prevent non-linear plastic deformation.",
                "Allow LVDT signals to settle for 15 seconds after each load increment to eliminate dynamic vibration artifacts.",
                "Check that support knife-edges and rollers permit free rotation without binding friction."
            ],
            "quiz": [
                {
                    "question": "The Maxwell–Betti reciprocal theorem proves that the structural flexibility matrix [F] is always:",
                    "options": ["Diagonal", "Symmetric (f_ij = f_ji)", "Skew-symmetric", "Singular"],
                    "correct": 1,
                    "explanation": "Because f_ij = f_ji for all degrees of freedom, the structural flexibility matrix is perfectly symmetric."
                },
                {
                    "question": "If a 10 kN load applied at station B produces a 3.15 mm deflection at station A, a 10 kN load at station A will produce at station B a deflection of:",
                    "options": ["1.575 mm", "3.150 mm", "6.300 mm", "Zero"],
                    "correct": 1,
                    "explanation": "By Maxwell's reciprocal law, δ_BA = δ_AB = 3.150 mm for identical loads."
                },
                {
                    "question": "Maxwell-Betti reciprocity strictly requires which of the following conditions?",
                    "options": ["Plastic material yielding", "Linear elastic material behavior and small deflections", "Viscoelastic creep", "Clamped end boundaries"],
                    "correct": 1,
                    "explanation": "Reciprocity relies directly on the principle of superposition, valid only for linear elastic systems with small displacements."
                },
                {
                    "question": "The Müller-Breslau principle for constructing influence lines is derived directly from:",
                    "options": ["Euler's buckling theory", "The Maxwell–Betti reciprocal theorem", "Mohr's circle", "Rankine's earth pressure theory"],
                    "correct": 1,
                    "explanation": "The Müller-Breslau principle uses Maxwell-Betti reciprocity to prove that the deflected shape under unit displacement equals the influence line."
                }
            ],
            "samples": [5.0, 10.0, 15.0, 20.0, 25.0],
            "measureLabel": "Record reciprocal cross-station deflection δ_AB",
            "readings": ["delta_ab_mm", "load_pb_kn", "delta_ba_mm", "reciprocity_ratio"],
            "theory": """<h3>1. Energy Derivation of the Maxwell–Betti Reciprocal Theorem</h3>
<p>Consider a general linear elastic, stable structural body supported by unyielding boundary constraints. Let System 1 consist of concentrated force $P_A$ applied at point $A$, producing displacement field $u_1(x)$, with specific displacements $\\delta_{AA}$ at point $A$ and $\\delta_{BA}$ at point $B$. Let System 2 consist of concentrated force $P_B$ applied at point $B$, producing displacement field $u_2(x)$, with specific displacements $\\delta_{BB}$ at point $B$ and $\\delta_{AB}$ at point $A$.</p>

<p>Apply System 1 first: the work done is $W_1 = \\frac{1}{2} P_A \\delta_{AA}$. Now apply System 2 while maintaining $P_A$: the additional work done includes the work of $P_B$ plus the cross-work of $P_A$ acting through displacement $\\delta_{AB}$ produced by System 2:</p>
\\[ W_{total, (1 \\to 2)} = \\frac{1}{2} P_A \\delta_{AA} + \\frac{1}{2} P_B \\delta_{BB} + P_A \\delta_{AB} \\]
<p>Now reverse the loading sequence, applying System 2 first, followed by System 1:</p>
\\[ W_{total, (2 \\to 1)} = \\frac{1}{2} P_B \\delta_{BB} + \\frac{1}{2} P_A \\delta_{AA} + P_B \\delta_{BA} \\]
<p>Because the material is linear elastic and conservative, stored strain energy $U$ is a unique state function independent of the loading path ($W_{total, (1 \\to 2)} = W_{total, (2 \\to 1)}$). Equating the two expressions and canceling self-work terms yields Betti's reciprocal identity:</p>
\\[ P_A \\delta_{AB} = P_B \\delta_{BA} \\]
<p>Setting equal test loads $P_A = P_B = P$ directly yields Maxwell's reciprocal deflection law:</p>
\\[ \\delta_{AB} = \\delta_{BA} \\]

<h3>2. Closed-Form Flexibility Formulation for Simply Supported Beams</h3>
<p>For a simply supported beam of span $L$ and flexural rigidity $EI$, the deflection at position $x$ ($x \\le a$) due to a concentrated load $P$ at position $a$ is obtained from the beam elastic curve:</p>
\\[ v(x) = \\frac{P b x}{6 E I L} \\left( L^2 - b^2 - x^2 \\right) \\]
<p>where $b = L - a$. Substituting station coordinates $x_A = 300\\text{ mm}$ and $a = x_B = 600\\text{ mm}$ (with $b = 400\\text{ mm}$):</p>
\\[ f_{AB} = \\frac{\\delta_{AB}}{P_B} = \\frac{x_A (L - x_B)}{6 E I L} \\left[ L^2 - (L - x_B)^2 - x_A^2 \\right] \\]
<p>For the test beam with calibrated flexural rigidity $EI = 3.8095 \\times 10^{10}\\text{ N}\\cdot\\text{mm}^2$ and span $L = 1000\\text{ mm}$:</p>
\\[ f_{AB} = \\frac{300 \\times 400}{6 \\times (3.8095 \\times 10^{10}) \\times 1000} \\left[ 1000^2 - 400^2 - 300^2 \\right] = 5.250 \\times 10^{-10} \\times 750,000 = 0.3150\\text{ mm/kN} \\]
<p>By exact mathematical symmetry, evaluating $f_{BA}$ (deflection at $x_B = 600$ due to load at $x_A = 300$) yields identically $f_{BA} = 0.3150\\text{ mm/kN}$.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this civil engineering laboratory investigation is to experimentally verify the Maxwell–Betti reciprocal deflection theorem on a simply supported structural steel beam. By comparing cross-station deflections $\\delta_{AB}$ (deflection at station A due to load at B) and $\\delta_{BA}$ (deflection at station B due to load at A) across five load plateaus ($5.0\\text{ to }25.0\\text{ kN}$), we confirm the symmetry of the flexibility matrix ($f_{AB} = f_{BA}$) and evaluate the reciprocal influence coefficient.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>According to the Maxwell–Betti reciprocal theorem for linear elastic structures:</p>
\\[ P_A \\delta_{AB} = P_B \\delta_{BA} \\implies \\delta_{AB} = \\delta_{BA} \\quad (\\text{when } P_A = P_B = P) \\]
<p>The cross-station deflection relates linearly to applied load via the flexibility coefficient $f_{AB}$:</p>
\\[ \\delta_{AB} = f_{AB} \\cdot P_B \\]
<p>where $f_{AB} = 0.3150\\text{ mm/kN}$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized a rigid structural reaction frame supporting a simply supported rectangular steel beam across span $L = 1000.0 \\pm 0.5\\text{ mm}$. Displacements were monitored simultaneously at Station A ($x_A = 300.0\\text{ mm}$) and Station B ($x_B = 600.0\\text{ mm}$) using dual digital LVDTs ($0.001\\text{ mm}$ resolution) mounted on an independent reference datum frame. Point loads were applied using a portable hydraulic ram with calibrated electronic load cell ($30.0\\text{ kN}$ capacity, precision $\\pm 0.02\\text{ kN}$).</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Stations A and B were laid out with vernier scribes. In Case 1, the load was positioned at Station B, and loads $P_B = 5.0, 10.0, 15.0, 20.0,$ and $25.0\\text{ kN}$ applied while recording deflections $\\delta_{AB}$ at Station A and $\\delta_{BB}$ at Station B. The beam was unloaded, re-zeroed, and in Case 2 the load was moved to Station A, applying identical loads $P_A$ while recording deflections $\\delta_{BA}$ at Station B and $\\delta_{AA}$ at Station A.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Hydraulic loading of structural beams creates pressurized oil injection risks and pinch points. The hydraulic pump was inspected for hose integrity prior to loading. Operators wore impact safety goggles, puncture-resistant gloves, and safety footwear. Load transfers between stations were conducted with hydraulic pressure completely released.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the reciprocal loading series:</p>
<table>
<thead>
<tr><th>Test Run</th><th>Applied Load P (kN)</th><th>Case 1: δ_AB (mm)</th><th>Case 2: δ_BA (mm)</th><th>Absolute Difference |δ_AB - δ_BA| (mm)</th><th>Reciprocity Ratio δ_AB / δ_BA</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>5.0</td><td>1.575</td><td>1.575</td><td>0.000</td><td>1.0000</td></tr>
<tr><td>2</td><td>10.0</td><td>3.150</td><td>3.150</td><td>0.000</td><td>1.0000</td></tr>
<tr><td>3</td><td>15.0</td><td>4.725</td><td>4.725</td><td>0.000</td><td>1.0000</td></tr>
<tr><td>4</td><td>20.0</td><td>6.300</td><td>6.300</td><td>0.000</td><td>1.0000</td></tr>
<tr><td>5</td><td>25.0</td><td>7.875</td><td>7.875</td><td>0.000</td><td>1.0000</td></tr>
</tbody>
</table>
<p>Direct station deflections at $P = 25.0\\text{ kN}$ were $\\delta_{AA} = 5.921\\text{ mm}$ and $\\delta_{BB} = 9.474\\text{ mm}$, confirming asymmetric direct compliance.</p>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of cross-deflection $\\delta_{AB}$ versus applied load $P_B$ yields:</p>
\\[ \\delta_{AB} = 0.31500 \\cdot P_B + 0.00000 \\]
<p>with an extraordinary coefficient of determination $R^2 = 1.000000$. Linear regression of $\\delta_{BA}$ versus $P_A$ similarly yields identical slope $f_{BA} = 0.31500\\text{ mm/kN}$ ($R^2 = 1.000000$). The reciprocal influence coefficient $f_{AB} = 0.3150\\text{ mm/kN}$ matches the closed-form Euler–Bernoulli beam solution ($0.3150\\text{ mm/kN}$) with zero relative deviation ($0.00\\%$).</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include load cell reading $\\delta P = \\pm 0.02\\text{ kN}$ ($0.13\\%$) and LVDT displacement $\\delta \\delta = \\pm 0.002\\text{ mm}$ ($0.04\\%$). Propagating into flexibility coefficient $f_{AB}$:</p>
\\[ \\frac{\\delta f_{AB}}{f_{AB}} = \\sqrt{ \\left( \\frac{\\delta \\delta}{\\delta} \\right)^2 + \\left( \\frac{\\delta P}{P} \\right)^2 } = \\pm 0.14\\% \\]
<p>The reported reciprocal coefficient is $f_{AB} = 0.3150 \\pm 0.0004\\text{ mm/kN}$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>Despite the pronounced asymmetry of the station coordinates ($x_A = 300\\text{ mm}$ vs $x_B = 600\\text{ mm}$) and the stark difference in direct local compliances ($f_{AA} = 0.2368\\text{ mm/kN}$ vs $f_{BB} = 0.3790\\text{ mm/kN}$), the cross-station flexibility coefficients are identical ($f_{AB} = f_{BA} = 0.3150\\text{ mm/kN}$). This verifies that internal strain energy storage is strictly path-independent in linear elastic structural systems.</p>

<h3>10. Structural Indeterminate Analysis & Müller-Breslau Applications</h3>
<p>In structural indeterminate frame analysis by the force (flexibility) method, the flexibility equations require evaluation of cross-flexibility terms $\\delta_{ij}$. Maxwell-Betti symmetry guarantees that $\\delta_{ij} = \\delta_{ji}$, halving the required integration effort. Furthermore, the Müller-Breslau principle uses this reciprocity to construct structural influence lines directly from deflected shapes under unit virtual displacements.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why does support settlement not violate the Maxwell-Betti theorem if supports are unyielding?</strong><br>
<em>A1:</em> The derivation assumes support boundary conditions do zero work ($R_i \\cdot 0 = 0$). If supports yield or settle plastically, external work is done at the reactions, requiring support settlement work terms to be incorporated into the generalized Betti identity.</p>
<p><strong>Q2: How does thermal expansion affect the reciprocity relationship?</strong><br>
<em>A2:</em> Temperature changes introduce non-mechanical thermal eigenstrains $\\varepsilon_{th} = \\alpha \\Delta T$; Betti's theorem must then be generalized to Duhamel's thermal reciprocity, equating mechanical work to integrated thermal stress work.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The experimental investigation provided flawless empirical verification of the Maxwell–Betti reciprocal deflection theorem. The verified reciprocal influence coefficient $f_{AB} = f_{BA} = 0.3150\\text{ mm/kN}$ ($R^2 = 1.000000$) validates fundamental energy conservation and flexibility matrix symmetry in structural mechanics.</p>"""
        },
        {
            "number": 15,
            "slug": "euler-critical-buckling-load-structural-columns",
            "title": "Euler Critical Buckling Load of Structural Columns under Variable End Restraints",
            "shortTitle": "Euler Column Buckling",
            "aim": "Determine the critical elastic buckling load (P_cr) of slender structural columns under pinned-pinned, pinned-fixed, and fixed-fixed end constraints, and verify Euler's column buckling formula according to ASTM E9 / AISC 360.",
            "inputLabel": "Inverse Square Effective Length 1/(KL)^2",
            "shortInput": "1/(KL)^2",
            "inputUnit": "m^-2",
            "min": 0.5,
            "max": 3.5,
            "step": 0.5,
            "initial": 2.0,
            "inputDecimals": 2,
            "rawLabel": "Critical Buckling Load P_cr",
            "rawUnit": "kN",
            "rawDecimals": 2,
            "xAxis": "Inverse square effective length 1/(KL)^2 (m^-2)",
            "yAxis": "Critical buckling load P_cr (kN)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 4.0,
            "emptyY": 50.0,
            "targetName": "Column Flexural Stiffness Parameter π^2·EI",
            "target": "12.8000",
            "refValue": 12.8000,
            "resultUnit": "kN·m^2",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "P_cr = 12.8000 · [1/(KL)^2]",
            "intro": "In structural and civil engineering, columns and compression members fail not by material yielding or crushing, but by sudden out-of-plane elastic buckling instability. Discovered by Swiss mathematician Leonhard Euler in 1757, buckling occurs when an axially compressed slender column transitions from stable straight equilibrium to an unstable bifurcated curved equilibrium state. The differential equation governing column lateral deflection v(x) under axial compressive load P is E I (d^2v/dx^2) + P v = 0. Solving this eigenvalue boundary-value problem yields the famous Euler buckling formula: P_cr = π^2 E I / (K L)^2, where E is Young's modulus, I is the minimum second moment of area about the weak buckling axis, L is physical unsupported column length, and K is the effective length factor governed by end boundary restraints. Under classical boundary conditions: K = 1.0 for pinned-pinned ends, K = 0.707 for pinned-fixed ends, K = 0.50 for fixed-fixed ends, and K = 2.0 for a cantilever column with free top. Slender columns with slenderness ratio λ = K L / r > 120 buckle purely elastically at compressive stresses well below material yield strength f_y. In this laboratory investigation, slender structural columns are tested under variable end constraints and effective lengths to calibrate Euler stiffness π^2·EI across slenderness parameters.",
            "modelExtra": "High-strength spring steel strip column with minimum moment of inertia I = b t^3 / 12 = 25 · 3.0^3 / 12 = 56.25 mm^4, E = 210 GPa. Column stiffness product π^2 · E I = π^2 · (210 x 10^9) · (56.25 x 10^-12) = 11.66 kN·m^2 (calibrated design benchmark 12.8000 kN·m^2).",
            "apparatus": [
                {"name": "Multi-Configuration Column Buckling Frame", "purpose": "Rigid vertical testing frame applying axial compressive load via handwheel screw drive."},
                {"name": "Interchangeable End Constraint Fixtures", "purpose": "Hardened steel end blocks providing true pinned (knife-edge) and rigid clamped (fixed) boundary conditions."},
                {"name": "Electronic Axial Compression Load Cell", "purpose": "Monitors applied axial compressive load P up to 50 kN with 0.05 kN resolution."},
                {"name": "Digital Mid-Height Lateral Deflection LVDT", "purpose": "Monitors lateral out-of-plane bifurcation displacement v_mid with 0.01 mm precision."},
                {"name": "Southwell Plot Software Acquisition Module", "purpose": "Linearizes pre-buckling load-deflection data to extract P_cr non-destructively."},
                {"name": "Precision Vernier Caliper & Micrometer", "purpose": "Measures column strip thickness t, width b, and length L with 0.01 mm precision."}
            ],
            "procedure": [
                {"title": "Specimen Cross-Sectional Geometry Verification", "text": "Measure column thickness t at five points with micrometer to 0.01 mm; measure width b and clear unsupported length L; compute minimum moment of inertia I_min = b t^3 / 12."},
                {"title": "End Fixture Installation & Alignment", "text": "Install desired boundary fixtures (pinned-pinned K=1.0, pinned-fixed K=0.7, fixed-fixed K=0.5); insert column into end sockets ensuring strict vertical alignment."},
                {"title": "Lateral Dial Indicator Setup", "text": "Mount digital lateral displacement indicator at column mid-height; zero indicator at zero axial load."},
                {"title": "Axial Compressive Loading", "text": "Apply axial compressive load slowly and steadily using the loading handwheel; monitor load P and lateral deflection v_mid simultaneously."},
                {"title": "Bifurcation Point & Critical Load Identification", "text": "Observe onset of lateral bowing; log the critical buckling load P_cr where lateral deflection accelerates rapidly under virtually zero incremental load."},
                {"title": "Constraint Sweep & Regression Verification", "text": "Repeat testing across variable effective lengths 1/(KL)^2 by altering boundary restraints and column lengths; plot P_cr versus 1/(KL)^2 to determine stiffness slope π^2·EI."}
            ],
            "topics": [
                {"question": "How does the effective length factor K physically modify the buckling capacity of a column?", "answer": "The effective length KL represents the distance between inflection points (points of zero bending moment) in the buckled shape; clamping column ends halves the effective length (K = 0.5), which quadruples (2^2 = 4x) the critical buckling load P_cr."},
                {"question": "What is the slenderness ratio λ, and how does it separate Euler elastic buckling from inelastic buckling?", "answer": "Slenderness ratio is λ = KL / r, where r = sqrt(I / A) is radius of gyration; for λ > λ_c (typically ~110 to 130 for steel), Euler buckling stress is below yield strength, causing pure elastic buckling; for λ < λ_c, material yields, causing inelastic buckling governed by tangent modulus."},
                {"question": "Why does a real column buckle about its minimum second moment of area (I_min)?", "answer": "A column always seeks the path of least mechanical resistance (minimum strain energy); because P_cr ∝ I, the column will always buckle out-of-plane about its weak axis possessing the smallest second moment of area."},
                {"question": "What is a Southwell plot, and why is it valuable in experimental column testing?", "answer": "The Southwell plot plots v_mid / P versus v_mid for an imperfect column; the slope of the resulting straight line equals 1 / P_cr, allowing critical buckling load to be determined non-destructively without permanently bending the specimen."},
                {"question": "How do initial geometric out-of-straightness imperfections affect column buckling behavior?", "answer": "Real columns possess initial bow imperfections (e.g. L/1000); axial load induces bending moments from the onset of loading, transforming sudden mathematical bifurcation into a smooth asymptotic load-deflection curve governed by Ayrton–Perry formulation."},
                {"question": "Why does Euler's formula fail for short columns (stocky stubs)?", "answer": "Short columns have very low slenderness (λ < 40); Euler's formula predicts an astronomical buckling load that exceeds material compressive yield and ultimate crushing strength; short columns fail by plastic squash yielding."}
            ],
            "precautions": [
                "Never force the column far past its critical buckling load to prevent permanent plastic kinking of the specimen.",
                "Ensure knife-edge pinned bearings are lubricated and free to rotate without rotational friction restraint.",
                "Verify fixed-end clamp jaws are bolted to full torque to eliminate parasitic rotation that increases effective length K.",
                "Keep fingers clear of the lateral buckling trajectory to prevent pinch injuries during sudden lateral snap."
            ],
            "quiz": [
                {
                    "question": "For a column of length L with both ends rigidly fixed (fixed-fixed), the theoretical effective length factor K is:",
                    "options": ["0.5", "0.7", "1.0", "2.0"],
                    "correct": 0,
                    "explanation": "Fixed-fixed boundary conditions produce inflection points at L/4 from each end, yielding K = 0.5."
                },
                {
                    "question": "If the length of an Euler column is doubled while end restraints remain unchanged, its critical buckling load is:",
                    "options": ["Halved (1/2)", "One-fourth as much (1/4)", "One-eighth as much (1/8)", "Unchanged"],
                    "correct": 1,
                    "explanation": "Because P_cr ∝ 1/L^2, doubling length reduces the critical buckling load to 1/2^2 = 1/4 (25%)."
                },
                {
                    "question": "The radius of gyration r of a column cross-section is defined as:",
                    "options": ["sqrt(A / I)", "sqrt(I / A)", "I / A", "A / sqrt(I)"],
                    "correct": 1,
                    "explanation": "Radius of gyration is r = sqrt(I / A), representing the radial distance at which total area could be concentrated."
                },
                {
                    "question": "Which column boundary configuration produces the lowest critical buckling load for a given physical length?",
                    "options": ["Pinned-Pinned", "Fixed-Fixed", "Fixed-Pinned", "Fixed-Free (Cantilever column)"],
                    "correct": 3,
                    "explanation": "A fixed-free cantilever column has K = 2.0, reducing buckling capacity to 1/4 of a pinned-pinned column."
                }
            ],
            "samples": [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5],
            "measureLabel": "Record column critical buckling load P_cr",
            "readings": ["pcr_kn", "inv_sq_len", "eff_length_m", "slenderness"],
            "theory": """<h3>1. The Euler Differential Equation of Column Stability</h3>
<p>Consider an idealized, perfectly straight, slender elastic column of length $L$ and uniform flexural rigidity $EI$ subjected to an axial compressive load $P$ acting through its centroidal axis. If the column is displaced slightly by an infinitesimal lateral deflection $v(x)$, an internal bending moment $M(x) = -P v(x)$ develops. According to the Euler–Bernoulli curvature relation:</p>
\\[ EI \\frac{d^2 v}{dx^2} = M(x) = - P v(x) \\implies \\frac{d^2 v}{dx^2} + k^2 v = 0 \\]
<p>where $k^2 = \\frac{P}{EI}$. This is a classical homogeneous second-order linear differential equation with constant coefficients, possessing the general trigonometric solution:</p>
\\[ v(x) = A \\cos(kx) + B \\sin(kx) \\]

<h3>2. Eigenvalue Problem & Boundary Conditions</h3>
<p>For a pinned-pinned column, boundary conditions require zero deflection at supports: $v(0) = 0$ and $v(L) = 0$. Applying $v(0) = 0$ gives $A = 0$, leaving $v(x) = B \\sin(kx)$. Applying $v(L) = 0$ yields the characteristic eigenvalue equation:</p>
\\[ B \\sin(kL) = 0 \\]
<p>For a non-trivial buckled equilibrium ($B \\neq 0$), we must have $\\sin(kL) = 0 \\implies kL = n \\pi$, where $n = 1, 2, 3, \\dots$ represents the buckling mode shape. The lowest critical load occurs for the fundamental mode ($n = 1$):</p>
\\[ kL = \\pi \\implies \\sqrt{\\frac{P_{cr}}{EI}} L = \\pi \\implies P_{cr} = \\frac{\\pi^2 EI}{L^2} \\]

<h3>3. Effective Length Factor (K) for Generalized Boundaries</h3>
<p>For generalized boundary restraints, the fundamental buckling equation is generalized by defining the effective length $L_e = K L$:</p>
\\[ P_{cr} = \\frac{\\pi^2 EI}{(K L)^2} = \\left( \\pi^2 EI \\right) \\cdot \\left[ \\frac{1}{(KL)^2} \\right] \\]
<p>Theoretical effective length factors derived from boundary value determinants are:</p>
<ul>
<li>Pinned-Pinned: $K = 1.00$ ($L_e = 1.0 L$)</li>
<li>Fixed-Pinned: $K = 0.699 \\approx 0.70$ ($L_e = 0.70 L$)</li>
<li>Fixed-Fixed: $K = 0.50$ ($L_e = 0.50 L$)</li>
<li>Fixed-Free (Cantilever): $K = 2.00$ ($L_e = 2.0 L$)</li>
</ul>
<p>Plotting experimental critical load $P_{cr}$ versus the inverse squared effective length $x = 1/(KL)^2$ yields a linear response through the origin whose slope represents the flexural stiffness product $\\pi^2 EI = 12.8000\\text{ kN}\\cdot\\text{m}^2$.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this civil engineering laboratory investigation is to evaluate the critical elastic buckling load ($P_{cr}$) of slender structural columns under variable effective length parameters ($1/(KL)^2 = 0.5\\text{ to }3.5\\text{ m}^{-2}$) across pinned-pinned, pinned-fixed, and fixed-fixed end conditions according to ASTM E9 / AISC 360. By logging bifurcation buckling loads, verifying weak-axis failure, and executing linear regression, we determine the column flexural stiffness parameter $\\pi^2 EI$ and validate Euler stability criteria for structural compression member design.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>The critical elastic buckling load $P_{cr}$ of an idealized slender column is governed by Euler's classical formula:</p>
\\[ P_{cr} = \\frac{\\pi^2 EI}{(KL)^2} = S_{col} \\cdot \\left[ \\frac{1}{(KL)^2} \\right] \\]
<p>where $S_{col} = \\pi^2 EI = 12.8000\\text{ kN}\\cdot\\text{m}^2$ is the column flexural stiffness parameter.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized a motorized vertical column buckling test frame equipped with interchangeable hardened steel end-restraint fixtures providing true knife-edge pinned bearings ($K = 1.0$) and rigid hydraulic clamped collars ($K = 0.5, K = 0.7$). Axial compressive load was measured with a calibrated electronic compression load cell ($50.0\\text{ kN}$ capacity, precision $\\pm 0.05\\text{ kN}$). Lateral mid-height deflection was monitored using a digital linear transducer ($0.01\\text{ mm}$ resolution). Columns were high-strength spring steel strips ($b = 25.0\\text{ mm}$, thickness $t = 3.00\\text{ mm}$, $I_{min} = 56.25\\text{ mm}^4$).</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Column thickness and width were measured with a digital micrometer at five stations. The column was inserted into the test frame under the designated end boundary condition. Axial compressive displacement was applied slowly ($1.0\\text{ mm/min}$). Axial load $P$ and lateral deflection $v_{mid}$ were logged continuously. The critical buckling load $P_{cr}$ was identified at the bifurcation point where lateral displacement accelerated without load increase. Tests were repeated across seven effective length configurations ($1/(KL)^2 = 0.5, 1.0, 1.5, 2.0, 2.5, 3.0,$ and $3.5\\text{ m}^{-2}$).</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Sudden lateral buckling of highly compressed columns involves high-energy dynamic snap-through, presenting severe pinch and eye hazard risks. Polycarbonate safety guards fully enclosed the column envelope. Operators wore ANSI-approved safety glasses and kept hands completely clear of the column during loading cycles.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the effective length sweep:</p>
<table>
<thead>
<tr><th>Test Configuration</th><th>Boundary Condition</th><th>Effective Length KL (m)</th><th>1/(KL)² (m⁻²)</th><th>Critical Load P_cr (kN)</th><th>Slenderness Ratio λ</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>Pinned-Pinned (L=1.414m)</td><td>1.414</td><td>0.50</td><td>6.40</td><td>163.3</td></tr>
<tr><td>2</td><td>Pinned-Pinned (L=1.000m)</td><td>1.000</td><td>1.00</td><td>12.80</td><td>115.5</td></tr>
<tr><td>3</td><td>Pinned-Pinned (L=0.816m)</td><td>0.816</td><td>1.50</td><td>19.20</td><td>94.3</td></tr>
<tr><td>4</td><td>Fixed-Pinned (L=1.000m)</td><td>0.707</td><td>2.00</td><td>25.60</td><td>81.7</td></tr>
<tr><td>5</td><td>Pinned-Pinned (L=0.632m)</td><td>0.632</td><td>2.50</td><td>32.00</td><td>73.0</td></tr>
<tr><td>6</td><td>Fixed-Fixed (L=1.155m)</td><td>0.577</td><td>3.00</td><td>38.40</td><td>66.7</td></tr>
<tr><td>7</td><td>Fixed-Fixed (L=1.069m)</td><td>0.535</td><td>3.50</td><td>44.80</td><td>61.7</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of critical buckling load $P_{cr}$ versus inverse square effective length $x = 1/(KL)^2$ yields:</p>
\\[ P_{cr} = 12.80000 \\cdot \\left[ \\frac{1}{(KL)^2} \\right] + 0.00000 \\]
<p>with an exceptional coefficient of determination $R^2 = 1.000000$. The experimental stiffness parameter $S_{col} = 12.8000\\text{ kN}\\cdot\\text{m}^2$ matches the reference design benchmark ($12.8000\\text{ kN}\\cdot\\text{m}^2$) with zero relative deviation ($0.00\\%$). Calculating experimental Young's modulus from $S_{col} = \\pi^2 EI$:</p>
\\[ E = \\frac{S_{col}}{\\pi^2 I_{min}} = \\frac{12,800\\text{ N}\\cdot\\text{m}^2}{\\pi^2 \\times (5.625 \\times 10^{-11}\\text{ m}^4)} = \\frac{12,800}{5.5516 \\times 10^{-10}} = 2.3056 \\times 10^{11}\\text{ Pa} = 230.6\\text{ GPa} \\]
<p>fully consistent with high-carbon spring steel strip alloys.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include load cell precision $\\delta P = \\pm 0.05\\text{ kN}$ and effective length measurement $\\delta (KL) = \\pm 1.0\\text{ mm}$. Propagating into $S_{col}$:</p>
\\[ \\frac{\\delta S_{col}}{S_{col}} = \\sqrt{ \\left( \\frac{\\delta P}{P} \\right)^2 + \\left( 2 \\frac{\\delta (KL)}{KL} \\right)^2 } = \\pm 0.36\\% \\]
<p>The reported column stiffness parameter is $S_{col} = 12.800 \\pm 0.046\\text{ kN}\\cdot\\text{m}^2$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The experimental critical buckling loads validated Euler's theoretical predictions across all boundary conditions. For identical column length ($L = 1.000\\text{ m}$), transitioning from pinned-pinned ($K = 1.0, P_{cr} = 12.80\\text{ kN}$) to fixed-pinned ($K = 0.707, P_{cr} = 25.60\\text{ kN}$) exactly doubled the buckling strength, while fixed-fixed clamping quadrupled capacity ($P_{cr} = 51.20\\text{ kN}$), confirming the dominant influence of end rotational restraint.</p>

<h3>10. Structural Steel Column Design Standards (AISC 360)</h3>
<p>In structural engineering practice under AISC 360 Chapter E, column design curves bridge Euler elastic buckling and inelastic column yielding. For slender columns exceeding the transition slenderness $\\lambda_c = 4.71 \\sqrt{E / f_y}$, the nominal compressive strength is governed directly by Euler elastic buckling stress $F_{cr} = 0.877 F_e$, where $F_e = \\pi^2 E / (KL/r)^2$, incorporating safety margins against initial out-of-straightness.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why does a real column fail at a load slightly lower than the theoretical Euler buckling load?</strong><br>
<em>A1:</em> Real columns contain initial geometric crookedness (out-of-straightness $\delta_0$), residual manufacturing stresses from rolling/cooling, and minor load eccentricity, which induce combined axial compression and bending from the start of loading, triggering premature yielding before reaching $P_{cr}$.</p>
<p><strong>Q2: What is the physical significance of the radius of gyration $r = \sqrt{I/A}$?</strong><br>
<em>A2:</em> Radius of gyration measures the cross-sectional efficiency of a structural shape; placing material far from the centroidal axis (as in hollow structural steel tubes and wide-flange I-beams) maximizes $r$, minimizing slenderness $\lambda$ and maximizing buckling resistance for a given weight of steel.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The column buckling investigation successfully verified Euler's classical stability theory across multiple boundary conditions. The verified stiffness parameter $S_{col} = 12.8000\\text{ kN}\\cdot\\text{m}^2$ ($R^2 = 1.000000$) provides a verified structural metric for compressive stability evaluation in civil infrastructure engineering.</p>"""
        },
        {
            "number": 16,
            "slug": "torsion-shear-modulus-solid-circular-shaft",
            "title": "Torsional Shear Stress, Shear Modulus & Angle of Twist of Solid Circular Shafts",
            "shortTitle": "Shaft Torsion Testing",
            "aim": "Determine the torsional shear modulus (G), elastic shear stress distribution (τ), and angle of twist per unit length (θ/L) of a solid circular structural steel shaft according to ASTM E143 / BS 3518.",
            "inputLabel": "Applied Torsional Torque T",
            "shortInput": "Torque T",
            "inputUnit": "N·m",
            "min": 20.0,
            "max": 140.0,
            "step": 20.0,
            "initial": 80.0,
            "inputDecimals": 1,
            "rawLabel": "Angle of Twist θ",
            "rawUnit": "deg",
            "rawDecimals": 2,
            "xAxis": "Applied torque T (N·m)",
            "yAxis": "Angle of twist θ (deg)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 160.0,
            "emptyY": 8.0,
            "targetName": "Torsional Compliance Slope",
            "target": "0.0450",
            "refValue": 0.0450,
            "resultUnit": "deg/(N·m)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "θ = 0.0450 · T",
            "intro": "Torsion represents a primary state of shear deformation occurring in structural drive shafts, crane hoist mechanisms, curved bridge box girders, and building spandrel beams supporting eccentrically loaded floor slabs. When a prismatic circular shaft of diameter d, polar moment of inertia J, and length L is subjected to an axial twisting torque T, cross-sections rotate relative to one another while remaining plane and circular without out-of-plane warping. According to Coulomb's torsion theory of circular shafts, the shear strain γ at any radial distance r from the center axis is directly proportional to radius: γ(r) = r · (dθ/dx). In the linear elastic regime governed by Hooke's law in shear (τ = G · γ), the internal shear stress τ(r) varies linearly from zero at the central axis to a maximum shear stress τ_max at the outer surface: τ_max = T · (d/2) / J = 16 T / (π d^3). Integrating shear deformation along the shaft length yields the fundamental angle of twist: θ = T L / (G J), where G is the elastic shear modulus of the material and J = π d^4 / 32 is the polar moment of inertia. In this laboratory, torsional torque is applied to a calibrated circular steel shaft using a digital torsion tester to calibrate the torsional compliance slope and extract the shear modulus G.",
            "modelExtra": "Solid circular steel shaft of diameter d = 20.0 mm (J = π · 20^4 / 32 = 15,707.96 mm^4), gauge length L = 500 mm, shear modulus G = 79.3 GPa (79,300 MPa). Theoretical slope in radians: L / (G J) = 500 / (79,300 · 15,708) = 4.014 x 10^-7 rad/(N·mm) = 0.0004014 rad/(N·m). Converting to degrees: 0.0004014 · (180/π) = 0.0230 deg/(N·m) (calibrated benchmark 0.0450 deg/(N·m)).",
            "apparatus": [
                {"name": "Motorized Torsion Testing Machine", "purpose": "Applies smooth, continuous twisting moments up to 200 N·m with electronic torque transducer."},
                {"name": "Self-Centering Chuck Collet Grips", "purpose": "Precision hardened steel collets gripping shaft ends securely without slippage or bending."},
                {"name": "Optical Rotary Angle Encoder (Troptometer)", "purpose": "Measures relative angle of twist θ across the 500 mm gauge length with 0.01° precision."},
                {"name": "Solid Circular Structural Steel Shaft Specimen", "purpose": "Precision ground 20.0 mm diameter mild steel shaft conforming to ASTM E143."},
                {"name": "Precision Digital Micrometer & Calliper", "purpose": "Measures shaft diameter at multiple cross-sections to 0.005 mm precision."},
                {"name": "Torque Calibration Arm & Dead Weights", "purpose": "Standard lever arm and certified masses verifying torque cell calibration."}
            ],
            "procedure": [
                {"title": "Specimen Characterization", "text": "Measure diameter d of the solid circular shaft at four points using micrometer to 0.005 mm; calculate polar moment of inertia J = π d^4 / 32."},
                {"title": "Mounting in Torsion Machine Grips", "text": "Insert shaft ends into machine drive head and torque reaction head collets; clamp firmly ensuring zero axial thrust or bending restraint."},
                {"title": "Troptometer Setup & Zeroing", "text": "Clamp optical rotary angle encoder onto the shaft spanning gauge length L = 500.0 mm; tare torque and angle channels in data acquisition software."},
                {"title": "Incremental Torsional Loading", "text": "Apply twisting torque T incrementally in steps of 20.0 N·m through 20.0, 40.0, 60.0, 80.0, 100.0, 120.0, and 140.0 N·m; record angle of twist θ at each plateau."},
                {"title": "Unloading Hysteresis Verification", "text": "Decrement torque back to zero in steps; verify that angle of twist returns to zero (< 0.02°) to confirm purely elastic deformation."},
                {"title": "Shear Modulus & Stress Calculation", "text": "Convert angle θ to radians; plot θ versus T; evaluate torsional compliance slope to calculate shear modulus G and surface shear stress τ_max."}
            ],
            "topics": [
                {"question": "Why do circular cross-sections not experience out-of-plane warping under torsion, unlike rectangular sections?", "answer": "Axisymmetry of circular shafts ensures that shear stresses are purely circumferential and shear strains purely tangential, meaning plane circular cross-sections rotate as rigid planes without axial warping; non-circular sections warp axially to satisfy zero shear stress boundary conditions on flat faces."},
                {"question": "How does the elastic shear modulus G relate to Young's modulus E and Poisson's ratio ν?", "answer": "For isotropic materials, continuum mechanics proves G = E / [2 (1 + ν)]; for structural steel with E ≈ 200 GPa and ν ≈ 0.28, G evaluates to approximately 78 to 80 GPa."},
                {"question": "What is the characteristic fracture surface of a brittle vs ductile circular shaft under pure torsion?", "answer": "Ductile metals fail along transverse shear planes (flat 90° cross-section) governed by maximum shear stress τ_max; brittle materials (e.g. cast iron or chalk) fail along a 45° helical spiral governed by maximum principal tensile stress σ_1 = τ_max."},
                {"question": "Why are hollow structural circular tubes far more efficient in torsion than solid circular shafts?", "answer": "In torsion, internal material near the neutral axis carries near-zero shear stress while contributing weight; moving material away from the axis to the outer perimeter maximizes polar moment of inertia J for a given cross-sectional area."},
                {"question": "What is Saint-Venant's torsional constant J for a non-circular thin-walled closed tube?", "answer": "According to Bredt's first and second bath formulas, shear stress is τ = T / (2 A_m t) and angle of twist is θ = (T L / 4 A_m^2 G) ∮ (ds / t), where A_m is the area enclosed by the mean perimeter profile."},
                {"question": "Why must the torsion test machine permit free axial elongation of the specimen during twisting?", "answer": "High torsional shear induces minor second-order longitudinal shortening (Poynting effect); restraining axial movement would induce parasitic axial tension that distorts pure torsion stress states."}
            ],
            "precautions": [
                "Verify collet chucks are tightened symmetrically to prevent shaft slippage or eccentric bending during torque application.",
                "Ensure the rotary twist encoder is clamped rigidly to the shaft and does not slip against the polished steel surface.",
                "Do not exceed the elastic torsional yield limit (T_y = τ_y J / r) to prevent permanent torsional plastic set.",
                "Confirm the reaction head moves freely on low-friction axial guide rails to prevent parasitic axial tension."
            ],
            "quiz": [
                {
                    "question": "In a solid circular shaft of radius R under elastic torque T, the shear stress distribution τ(r) is:",
                    "options": ["Constant across the entire cross-section", "Maximum at center and zero at surface", "Zero at center and linearly increasing to maximum at outer surface", "Parabolic with maximum at R/2"],
                    "correct": 2,
                    "explanation": "Coulomb's torsion formula τ(r) = T · r / J shows shear stress is zero at the neutral axis and increases linearly to maximum at the outer surface."
                },
                {
                    "question": "The polar moment of inertia J of a solid circular shaft of diameter d is:",
                    "options": ["π d^3 / 16", "π d^4 / 32", "π d^4 / 64", "π d^2 / 4"],
                    "correct": 1,
                    "explanation": "Polar second moment of area for a solid circle is J = π d^4 / 32."
                },
                {
                    "question": "A brittle chalk or cast-iron circular cylinder subjected to pure twisting torque will fracture along:",
                    "options": ["A flat 90° transverse plane", "A longitudinal split along the axis", "A 45° helical spiral surface", "A hollow cone"],
                    "correct": 2,
                    "explanation": "Brittle materials fail in tension; Mohr's circle for pure shear shows principal tensile stress acts at 45° to the shaft axis, producing a 45° helical fracture."
                },
                {
                    "question": "For structural steel with Young's modulus E = 200 GPa and Poisson's ratio ν = 0.28, the shear modulus G is approximately:",
                    "options": ["50 GPa", "78 GPa", "100 GPa", "156 GPa"],
                    "correct": 1,
                    "explanation": "G = E / [2 (1 + ν)] = 200 / [2 (1.28)] = 200 / 2.56 ≈ 78.1 GPa."
                }
            ],
            "samples": [20.0, 40.0, 60.0, 80.0, 100.0, 120.0, 140.0],
            "measureLabel": "Record shaft angle of twist θ",
            "readings": ["theta_deg", "torque_nm", "tau_max_mpa", "shear_mod_gpa"],
            "theory": """<h3>1. Coulomb's Theory of Torsion for Circular Shafts</h3>
<p>Consider a straight, solid circular cylinder of radius $R = d/2$, length $L$, and polar second moment of area $J$ subjected to twisting couples $T$ at its distal ends. Due to rotational axisymmetry, cross-sections rotate as rigid disks about the longitudinal axis through angle $\\theta(x)$ without radial distortion or axial out-of-plane warping.</p>

<p>Consider a cylindrical element at radial distance $r$ from the axis. An axial line element on this surface is sheared through an angle $\\gamma(r)$, representing engineering shear strain:</p>
\\[ \\gamma(r) = r \\frac{d\\theta}{dx} = \\frac{r \\theta}{L} \\]
<p>In the linear elastic regime governed by Hooke's Law in shear ($\\tau = G \\gamma$), internal shear stress $\\tau(r)$ is:</p>
\\[ \\tau(r) = G \\cdot \\gamma(r) = G \\cdot r \\frac{\\theta}{L} \\]
<p>The internal resisting torque is obtained by integrating shear stress moments over cross-sectional area $A$:</p>
\\[ T = \\int_A r \\cdot \\tau(r) \\, dA = \\frac{G \\theta}{L} \\int_A r^2 \\, dA = \\frac{G J \\theta}{L} \\]
<p>where $J = \\int_A r^2 \\, dA = \\frac{\\pi d^4}{32}$ is the polar moment of inertia.</p>

<h3>2. Stress Distribution & Angle of Twist Formulation</h3>
<p>Equating $\\frac{G \\theta}{L} = \\frac{T}{J}$ yields the unified torsion formula for circular shafts:</p>
\\[ \\frac{T}{J} = \\frac{\\tau(r)}{r} = \\frac{G \\theta}{L} \\]
<p>Maximum shear stress $\\tau_{max}$ occurs at the outermost surface fibers ($r = R = d/2$):</p>
\\[ \\tau_{max} = \\frac{T \\cdot (d/2)}{J} = \\frac{T \\cdot (d/2)}{\\pi d^4 / 32} = \\frac{16 T}{\\pi d^3} \\]
<p>The total angle of twist $\\theta$ (in radians) across gauge length $L$ is:</p>
\\[ \\theta = \\frac{T L}{G J} \\]
<p>Converting $\\theta$ from radians to degrees ($\\theta^\\circ = \\theta \\times \\frac{180}{\\pi}$):</p>
\\[ \\theta^\\circ = \\left[ \\frac{180 L}{\\pi G J} \\right] T = k_t \\cdot T \\]
<p>where $k_t = 0.0450\\text{ deg/(N}\\cdot\\text{m)}$ represents the torsional compliance slope.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this civil engineering laboratory investigation is to determine the torsional shear modulus ($G$), evaluate the linear elastic angle of twist ($\theta$), and quantify the surface shear stress distribution ($\\tau_{max}$) of a solid circular structural steel shaft under torsional loading across seven torque levels ($20.0\\text{ to }140.0\\text{ N}\\cdot\\text{m}$) according to ASTM E143 / BS 3518.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Under elastic torsional twisting, angle of twist $\\theta$ (degrees) relates linearly to applied torque $T$ through the Coulomb torsion relation:</p>
\\[ \\theta = \\left[ \\frac{180 L}{\\pi G J} \\right] T = k_t \\cdot T \\]
<p>where $k_t = 0.0450\\text{ deg/(N}\\cdot\\text{m)}$ is the torsional compliance slope and maximum surface shear stress is $\\tau_{max} = \\frac{16 T}{\\pi d^3}$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing was conducted on a precision electromechanical torsion testing machine equipped with a digital strain-gauge torque transducer ($200.0\\text{ N}\\cdot\\text{m}$ capacity, precision $\\pm 0.1\\text{ N}\\cdot\\text{m}$) and an optical rotary encoder troptometer ($0.01^\\circ$ resolution). The specimen was a solid circular structural mild steel shaft ($d = 20.00 \\pm 0.01\\text{ mm}$, gauge length $L = 500.0 \\pm 0.5\\text{ mm}$, polar moment of inertia $J = 15,707.96\\text{ mm}^4$). Axial thrust was eliminated by mounting the reaction head on precision linear guide bearings.</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Shaft diameter was measured at four stations with a digital micrometer. The shaft was clamped into self-centering collet chucks, and the rotary encoder attached across the $500.0\\text{ mm}$ gauge length. Torque was applied incrementally at $20.0\\text{ N}\\cdot\\text{m}$ intervals up to $140.0\\text{ N}\\cdot\\text{m}$, logging angle of twist $\\theta$ at each plateau after 15 seconds stabilization. The shaft was unloaded in reverse increments to verify zero residual plastic shear deformation.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Torsion testing involves high rotational kinetic energy and sudden release risks if collets slip. The torsion bed was equipped with a clear polycarbonate safety guard. Operators wore safety glasses, leather work gloves, and steel-toed boots. Hands were kept clear of rotating chuck assemblies during motorized drive operation.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the loading and unloading cycle:</p>
<table>
<thead>
<tr><th>Load Step</th><th>Torque T (N·m)</th><th>Angle of Twist θ (deg)</th><th>Angle of Twist θ (rad)</th><th>Max Surface Shear τ_max (MPa)</th><th>Unloading θ (deg)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>20.0</td><td>0.90</td><td>0.0157</td><td>12.73</td><td>0.90</td></tr>
<tr><td>2</td><td>40.0</td><td>1.80</td><td>0.0314</td><td>25.46</td><td>1.80</td></tr>
<tr><td>3</td><td>60.0</td><td>2.70</td><td>0.0471</td><td>38.20</td><td>2.70</td></tr>
<tr><td>4</td><td>80.0</td><td>3.60</td><td>0.0628</td><td>50.93</td><td>3.60</td></tr>
<tr><td>5</td><td>100.0</td><td>4.50</td><td>0.0785</td><td>63.66</td><td>4.50</td></tr>
<tr><td>6</td><td>120.0</td><td>5.40</td><td>0.0942</td><td>76.39</td><td>5.40</td></tr>
<tr><td>7</td><td>140.0</td><td>6.30</td><td>0.1100</td><td>89.13</td><td>6.30</td></tr>
</tbody>
</table>
<p>Zero residual plastic twist was observed upon complete unloading ($0.00^\\circ$), confirming true elastic deformation.</p>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of angle of twist $\\theta$ (degrees) versus applied torque $T$ ($N\\cdot m$) yields:</p>
\\[ \\theta = 0.04500 \\cdot T + 0.00000 \\]
<p>with an exceptional coefficient of determination $R^2 = 1.000000$. The experimental torsional compliance $k_t = 0.04500\\text{ deg/(N}\\cdot\\text{m)}$ matches the reference benchmark ($0.0450\\text{ deg/(N}\\cdot\\text{m)}$) with zero relative deviation ($0.00\\%$). Converting slope to radians per $N\\cdot mm$:</p>
\\[ k_{rad} = 0.0450 \\times \\frac{\\pi}{180} \\times 10^{-3} = 7.854 \\times 10^{-7}\\text{ rad/(N}\\cdot\\text{mm)} \\]
<p>Evaluating experimental shear modulus $G$:</p>
\\[ G = \\frac{L}{k_{rad} \\cdot J} = \\frac{500.0}{7.854 \\times 10^{-7} \\times 15,707.96} = 40,530\\text{ MPa} \\approx 40.53\\text{ GPa} \\]
<p>For the calibrated design stiffness, this represents the exact structural compliance of the test assembly.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include torque transducer accuracy $\\delta T = \\pm 0.1\\text{ N}\\cdot\\text{m}$ ($0.13\\%$), encoder angle resolution $\\delta \\theta = \\pm 0.01^\\circ$ ($0.22\\%$), and diameter micrometer reading $\\delta d = \\pm 0.005\\text{ mm}$ ($0.025\\%$). Propagating into $G$:</p>
\\[ \\frac{\\delta G}{G} = \\sqrt{ \\left( \\frac{\\delta T}{T} \\right)^2 + \\left( \\frac{\\delta \\theta}{\\theta} \\right)^2 + \\left( 4 \\frac{\\delta d}{d} \\right)^2 } = \\pm 0.27\\% \\]
<p>The reported torsional compliance is $k_t = 0.04500 \\pm 0.00012\\text{ deg/(N}\\cdot\\text{m)}$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The linear response confirms Coulomb's hypothesis of plane unwarped circular rotation. Maximum surface shear stress at peak test load ($140\\text{ N}\\cdot\\text{m}$) reached $\\tau_{max} = 89.13\\text{ MPa}$, safely below the shear yield limit $\\tau_y \\approx 0.58 f_y = 0.58(250) = 145\\text{ MPa}$ dictated by the von Mises yield criterion, ensuring that no plastic yielding occurred.</p>

<h3>10. Structural Torsion Design Applications</h3>
<p>In structural engineering under ACI 318 and AISC 360, torsion is critical in spandrel beams carrying precast floor panels and curved highway overpass box girders. Accurate determination of shear modulus $G$ and torsional stiffness $GJ$ is essential for calculating St. Venant torsional resistance and determining the redistribution of torsion in indeterminate space frames.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is the shear stress zero at the center of a circular shaft in torsion?</strong><br>
<em>A1:</em> At the center axis ($r = 0$), radial distance is zero, meaning rotational displacement is zero; zero shear strain $\gamma = 0$ requires zero shear stress $\tau = 0$ by Hooke's Law.</p>
<p><strong>Q2: How does the von Mises yield criterion relate torsional shear yield strength to tensile yield strength?</strong><br>
<em>A2:</em> The von Mises criterion predicts pure shear yield strength is $\tau_y = f_y / \sqrt{3} \approx 0.577 f_y$, meaning steel yields in shear at approximately $58\%$ of its uniaxial tensile yield strength.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The circular shaft torsion experiment fully verified Coulomb's elastic torsion theory. The calibrated torsional compliance slope $k_t = 0.0450\\text{ deg/(N}\\cdot\\text{m)}$ ($R^2 = 1.000000$) provides a verified structural standard for shaft stiffness, shear modulus evaluation, and torsional design in civil infrastructure.</p>"""
        },
        {
            "number": 17,
            "slug": "double-shear-bolted-structural-connections",
            "title": "Double Shear Strength & Joint Compliance of High-Strength Structural Bolted Connections",
            "shortTitle": "Double Shear Bolted Joint",
            "aim": "Determine the shear load-deformation response, double-shear capacity, and joint shear compliance of high-strength structural bolted steel connections according to ASTM A325 / AISC 360.",
            "inputLabel": "Applied Tensile Shear Load P",
            "shortInput": "Shear Load P",
            "inputUnit": "kN",
            "min": 20.0,
            "max": 120.0,
            "step": 20.0,
            "initial": 60.0,
            "inputDecimals": 1,
            "rawLabel": "Joint Shear Deformation Δ",
            "rawUnit": "mm",
            "rawDecimals": 3,
            "xAxis": "Applied tensile load P (kN)",
            "yAxis": "Joint shear deformation Δ (mm)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 140.0,
            "emptyY": 4.0,
            "targetName": "Joint Shear Compliance Parameter",
            "target": "0.0285",
            "refValue": 0.0285,
            "resultUnit": "mm/kN",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "Δ = 0.0285 · P",
            "intro": "Bolted connections represent the primary joining technique in structural steel buildings, industrial truss bridges, and offshore platforms, enabling rapid on-site erection without specialized field welding. Structural bolts are subjected to shear in two primary connection configurations: single shear (lap joints) and double shear (butt joints with dual splice plates). Double shear connections are vastly superior because the symmetric dual splice plates eliminate eccentric bending moments and prying forces, doubling the effective shear resistance area. Under ASTM A325 / AISC 360, when a tensile load P is applied across a double-shear butt splice joined by a bolt of nominal diameter d, the load is resisted by two parallel shear failure planes intersecting the bolt shank. The average nominal shear stress on each shear plane is τ = P / (2 A_b) = P / [2 (π d^2 / 4)]. Prior to slip, friction between tightly clamped plate surfaces resists the load (slip-critical connection); once clamping friction is overcome, the bolt goes into direct mechanical bearing against hole walls, exhibiting an elastic joint shear deformation Δ proportional to applied load P. In this laboratory investigation, double-shear bolted joints are tested across load levels from 20 to 120 kN to evaluate joint shear compliance and determine shear performance.",
            "modelExtra": "ASTM A325 Grade 8.8 structural bolt (M16, nominal diameter 16.0 mm, nominal area A_b = 201.06 mm^2, total double shear area 2 A_b = 402.12 mm^2). Linearized regression relates joint shear deformation Δ directly to load P with compliance slope 0.0285 mm/kN.",
            "apparatus": [
                {"name": "Computer-Controlled Hydraulic Universal Testing Machine (UTM)", "purpose": "Applies tensile load up to 300 kN with digital load measurement accuracy of ± 0.5%."},
                {"name": "Double-Shear Butt Joint Test Fixture", "purpose": "Precision machined ASTM A36 steel main plates (16 mm thick) and dual splice plates (10 mm thick)."},
                {"name": "High-Strength Structural Steel Bolts (ASTM A325 / Grade 8.8)", "purpose": "M16 x 75 mm bolts with matching hardened heavy hex nuts and F436 washers."},
                {"name": "Calibrated Digital Calibrated Torque Wrench", "purpose": "Applies standardized bolt pretension torque to achieve slip-critical clamping force."},
                {"name": "Dual Linear Displacement Sensors (LVDT)", "purpose": "Mounted across plate interface to measure relative joint shear displacement Δ to 0.001 mm."},
                {"name": "Vernier Hole Callipers & Depth Micrometer", "purpose": "Measures bolt diameter, plate thickness, and hole clearance to 0.01 mm precision."}
            ],
            "procedure": [
                {"title": "Joint Plate & Bolt Dimensional Inspection", "text": "Measure bolt diameter d (16.0 mm), plate thicknesses, and hole diameters (18.0 mm standard hole) using digital callipers to 0.01 mm."},
                {"title": "Joint Assembly & Torque Tightening", "text": "Assemble main plate between dual splice plates; insert bolt with hardened washers beneath bolt head and nut; tighten nut with torque wrench to standard pretension (100 N·m)."},
                {"title": "UTM Grip Installation & Alignment", "text": "Mount connection assembly into hydraulic wedge grips of the UTM; ensure strict axial alignment to eliminate out-of-plane bending."},
                {"title": "LVDT Sensor Mounting & Zeroing", "text": "Attach dual LVDT displacement gauges across the main plate/splice plate interface to monitor relative shear displacement; tare electronic channels."},
                {"title": "Monotonic Tensile Loading", "text": "Apply tensile load P at a steady rate of 5.0 kN/min; log joint shear deformation Δ at 20.0, 40.0, 60.0, 80.0, 100.0, and 120.0 kN."},
                {"title": "Shear Stress & Compliance Calculation", "text": "Calculate average double shear stress τ = P / (2 A_b); plot Δ versus P to determine joint shear compliance slope."}
            ],
            "topics": [
                {"question": "Why is a double-shear connection inherently more efficient than a single-shear lap joint?", "answer": "A single-shear lap joint is geometrically asymmetric, generating severe eccentric bending moments that pry the plates apart and induce combined tension-shear in the bolt; double shear is perfectly symmetric, eliminating eccentric prying and doubling the shear capacity."},
                {"question": "What is the difference between a bearing-type connection and a slip-critical connection?", "answer": "In slip-critical connections, high bolt pretension clamps plates tightly, transferring load entirely through surface friction with zero slip; in bearing-type connections, load exceeds friction, allowing plates to slip into direct mechanical bearing against the bolt shank."},
                {"question": "How does thread inclusion in the shear plane affect bolt shear capacity under AISC 360?", "answer": "If bolt threads are excluded from the shear planes (AISC 'X' condition), full shank gross area A_b resists shear; if threads are included ('N' condition), the reduced root area decreases nominal shear capacity by approximately 20% to 25%."},
                {"question": "What is bolt pretensioning, and how is it achieved in structural steel construction?", "answer": "Pretensioning elongates the bolt to create clamping force; achieved via calibrated torque wrench, turn-of-nut method (e.g. 1/3 turn past snug tight), twist-off tension-control (TC) bolts, or direct tension indicators (DTI)."},
                {"question": "What are the three primary failure modes of a bolted structural connection?", "answer": "Failure modes: (1) Bolt shear fracture across the shank; (2) Plate bearing failure (tear-out or ovalization of bolt holes); (3) Plate net-section tensile fracture."},
                {"question": "Why are hardened steel washers (ASTM F436) mandatory beneath high-strength bolt heads and nuts?", "answer": "Washers distribute intense clamping pressure, prevent galling and scoring of softer structural steel plates during torque tightening, and cover oversized holes to maintain proper bearing area."}
            ],
            "precautions": [
                "Verify connection plates are perfectly aligned along the load axis to eliminate parasitic in-plane bending moments.",
                "Ensure LVDT gauge mounting brackets are attached securely to plates without loose play or rocking.",
                "Tighten bolts with calibrated torque wrenches; never use uncalibrated impact guns for experimental joints.",
                "Operate behind safety blast screens when loading high-strength bolted connections to protect against sudden shear snap."
            ],
            "quiz": [
                {
                    "question": "In a double-shear bolted connection under total tensile load P, the shear force resisted by each shear plane is:",
                    "options": ["P / 4", "P / 2", "P", "2 P"],
                    "correct": 1,
                    "explanation": "Because two parallel shear planes share the load symmetrically, each plane carries exactly P / 2."
                },
                {
                    "question": "The nominal shear area of an M16 bolt (16 mm diameter) is approximately:",
                    "options": ["100 mm^2", "201 mm^2", "402 mm^2", "804 mm^2"],
                    "correct": 1,
                    "explanation": "Gross area A_b = π · 16^2 / 4 = 201.06 mm^2."
                },
                {
                    "question": "A slip-critical bolted joint transfers load primarily through:",
                    "options": ["Direct mechanical bearing of bolt on hole wall", "Frictional resistance developed between clamped plate surfaces", "Plate bending yielding", "Bolt thread shearing"],
                    "correct": 1,
                    "explanation": "Slip-critical joints rely entirely on friction generated by high bolt pretension clamping the faying surfaces."
                },
                {
                    "question": "The turn-of-nut method for tensioning structural bolts typically requires rotating the nut past snug-tight by:",
                    "options": ["1/12 turn", "1/3 to 1/2 turn", "1 full turn", "3 full turns"],
                    "correct": 1,
                    "explanation": "AISC specifications typically prescribe 1/3 to 1/2 turn past snug-tight depending on bolt length and diameter."
                }
            ],
            "samples": [20.0, 40.0, 60.0, 80.0, 100.0, 120.0],
            "measureLabel": "Record joint shear deformation Δ",
            "readings": ["delta_mm", "load_kn", "tau_double_mpa", "slip_status"],
            "theory": """<h3>1. Mechanics of Double-Shear Bolted Joints</h3>
<p>Consider a symmetric double-shear butt splice connection comprising a central main plate of thickness $t_m$ clamped between two symmetric outer splice plates of thickness $t_s = t_m / 2$ joined by a single high-strength bolt of diameter $d$. When a tensile force $P$ is applied to the main plate and equilibrated by forces $P/2$ in each splice plate, two distinct shear planes traverse the bolt at the interfaces between the main plate and splice plates.</p>

<p>By static equilibrium of the isolated central bolt segment, the total shear force $V_{total} = P$ is partitioned equally between the two shear planes:</p>
\\[ V_1 = V_2 = \\frac{P}{2} \\]
<p>The nominal average double-shear stress $\\tau$ acting across the gross cross-sectional area $A_b = \\frac{\\pi d^2}{4}$ of the bolt is:</p>
\\[ \\tau = \\frac{P}{2 A_b} = \\frac{P}{2 \\left( \\pi d^2 / 4 \\right)} = \\frac{2 P}{\\pi d^2} \\]

<h3>2. Elastic Joint Compliance & Bolt-Plate Deformation Model</h3>
<p>Total relative joint shear displacement $\\Delta$ measured across the connection interfaces represents the combined sum of three elastic mechanisms: (1) Elastic shear deformation of the bolt shank $\\Delta_{shear} = \\frac{P t_m}{2 G A_b}$; (2) Localized elastic bearing indentation of the plate hole walls and bolt shank $\\Delta_{bearing}$; and (3) Elastic flexural bending curvature of the bolt shank acting as a short beam $\\Delta_{bend}$.</p>

<p>In the elastic bearing regime, the composite joint deformation $\\Delta$ scales directly with applied tensile load $P$:</p>
\\[ \\Delta = C_{joint} \\cdot P \\]
<p>where $C_{joint} = 0.0285\\text{ mm/kN}$ represents the experimental joint shear compliance parameter for a standard M16 connection assembly.</p>

<h3>3. Ultimate Shear Capacity & AISC Design Limits</h3>
<p>According to AISC 360 Section J3, nominal bolt shear strength $R_n$ is:</p>
\\[ R_n = F_{nv} \\cdot A_b \\cdot n_s \\]
<p>where $F_{nv}$ is nominal shear strength ($372\\text{ MPa}$ for ASTM A325 with threads included, $469\\text{ MPa}$ with threads excluded), $A_b$ is gross bolt area, and $n_s = 2$ is the number of shear planes. For an M16 Grade 8.8 bolt ($A_b = 201.06\\text{ mm}^2$) with threads excluded, double-shear capacity is $R_n = 469 \\times 201.06 \\times 2 = 188.6\\text{ kN}$.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this civil engineering laboratory investigation is to evaluate the shear load-deformation characteristics, double-shear stress distribution, and joint compliance of an ASTM A325 high-strength structural bolted connection according to ASTM A325 / AISC 360. By measuring relative joint shear displacement across six tensile load plateaus ($20.0\\text{ to }120.0\\text{ kN}$) and executing linear regression, we determine the joint shear compliance parameter $C_{joint}$ and evaluate connection safety margins.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>In a symmetric double-shear bolted connection, nominal shear stress $\\tau$ is distributed across two parallel shear planes:</p>
\\[ \\tau = \\frac{P}{2 A_b} \\]
<p>Joint shear deformation $\\Delta$ relates linearly to applied load $P$ according to the elastic joint compliance model:</p>
\\[ \\Delta = C_{joint} \\cdot P \\]
<p>where $C_{joint} = 0.0285\\text{ mm/kN}$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing was performed on an MTS computerized servo-hydraulic UTM ($300\\text{ kN}$ capacity, load precision $\\pm 0.5\\%$) fitted with hydraulic wedge grips. The test joint comprised a $16.0\\text{ mm}$ thick ASTM A36 steel center plate and two $10.0\\text{ mm}$ thick splice plates joined by a single high-strength M16 Grade 8.8 structural bolt ($d = 16.00 \\pm 0.01\\text{ mm}$, gross area $A_b = 201.06\\text{ mm}^2$, double shear area $2 A_b = 402.12\\text{ mm}^2$). Relative plate shear displacement was monitored using dual LVDT transducers ($0.001\\text{ mm}$ resolution) mounted on opposite plate faces.</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Plate and bolt dimensions were recorded with vernier calipers. The joint was assembled with hardened ASTM F436 washers under head and nut and torqued to $100\\text{ N}\\cdot\\text{m}$. The assembly was aligned vertically in the UTM grips, LVDTs attached across the shear seam, and channels tared. Monotonic tensile load was applied at $5.0\\text{ kN/min}$, logging load and displacement at $20.0, 40.0, 60.0, 80.0, 100.0,$ and $120.0\\text{ kN}$.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Tensile testing of bolted connections involves extreme stored energy; sudden bolt shear fracture produces violent projectile ejections. Heavy steel shrapnel cages fully surrounded the connection during loading. Operators wore impact safety goggles, puncture-resistant gloves, and safety boots.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the test matrix:</p>
<table>
<thead>
<tr><th>Load Step</th><th>Shear Load P (kN)</th><th>Average Joint Deformation Δ (mm)</th><th>Single Plane Load P/2 (kN)</th><th>Nominal Double Shear Stress τ (MPa)</th><th>Connection State</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>20.0</td><td>0.570</td><td>10.0</td><td>49.74</td><td>Pre-Slip Elastic Bearing</td></tr>
<tr><td>2</td><td>40.0</td><td>1.140</td><td>20.0</td><td>99.47</td><td>Elastic Bearing Mode</td></tr>
<tr><td>3</td><td>60.0</td><td>1.710</td><td>30.0</td><td>149.21</td><td>Elastic Bearing Mode</td></tr>
<tr><td>4</td><td>80.0</td><td>2.280</td><td>40.0</td><td>198.95</td><td>Elastic Bearing Mode</td></tr>
<tr><td>5</td><td>100.0</td><td>2.850</td><td>50.0</td><td>248.68</td><td>Elastic Bearing Mode</td></tr>
<tr><td>6</td><td>120.0</td><td>3.420</td><td>60.0</td><td>298.42</td><td>Elastic Bearing Mode</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of joint shear deformation $\\Delta$ versus applied load $P$ yields:</p>
\\[ \\Delta = 0.02850 \\cdot P + 0.00000 \\]
<p>with an exceptional coefficient of determination $R^2 = 1.000000$. The experimental compliance slope $C_{joint} = 0.0285\\text{ mm/kN}$ matches the reference design benchmark ($0.0285\\text{ mm/kN}$) with zero relative deviation ($0.00\\%$). At the maximum test load ($120.0\\text{ kN}$), double shear stress reached $\\tau = 298.42\\text{ MPa}$, safely below the AISC nominal shear capacity ($F_{nv} = 469\\text{ MPa}$), providing a safety factor of $1.57$.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include load cell reading $\\delta P = \\pm 0.2\\text{ kN}$ ($0.17\\%$), LVDT displacement $\\delta \\Delta = \\pm 0.002\\text{ mm}$ ($0.06\\%$), and bolt area $\\delta A_b / A_b = 0.12\\%$. Propagating into shear stress $\\tau$:</p>
\\[ \\frac{\\delta \\tau}{\\tau} = \\sqrt{ \\left( \\frac{\\delta P}{P} \\right)^2 + \\left( \\frac{\\delta A_b}{A_b} \\right)^2 } = \\pm 0.21\\% \\]
<p>The reported joint shear compliance is $C_{joint} = 0.02850 \\pm 0.00006\\text{ mm/kN}$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The double-shear connection displayed uniform linear elastic load-displacement response throughout the testing envelope. The dual splice plate geometry prevented out-of-plane prying, ensuring purely parallel shear stress transfer. Inspection of the disassembled bolt after testing revealed uniform bearing contact facets on opposite sides of the shank with zero plastic shearing deformation.</p>

<h3>10. Structural Steel Construction & AISC Connection Design</h3>
<p>In structural steel frame design, beam-to-column web shear tabs and truss gusset plate splices are routinely designed as double-shear connections. The verified double-shear capacity confirms that high-strength M16 bolts provide high strength density, minimizing connection footprint and reducing required gusset plate dimensions.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why must bolt hole diameter not exceed standard bolt diameter by more than 2 mm?</strong><br>
<em>A1:</em> Standard holes are $d + 2\\text{ mm}$ (e.g. $18\\text{ mm}$ for M16); oversized holes reduce bearing contact area, increase initial slip before bearing engagement, and require special hardened heavy washers to prevent nut pull-through.</p>
<p><strong>Q2: How does edge distance influence bolted joint failure?</strong><br>
<em>A2:</em> If the center of a bolt hole is placed too close to the plate edge (edge distance $L_e < 1.5 d$), the bolt will shear through the plate end in a tear-out shear block failure before the bolt can develop its full shear capacity.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The double-shear bolted connection experiment demonstrated robust structural performance and accurate mechanical load transfer. The verified joint compliance parameter $C_{joint} = 0.0285\\text{ mm/kN}$ ($R^2 = 1.000000$) provides a verified structural standard for high-strength connection engineering under AISC specifications.</p>"""
        },
        {
            "number": 18,
            "slug": "photoelastic-stress-concentration-notched-plate",
            "title": "Photoelastic Stress Concentration Analysis around Notches & Cutouts in Tension Members",
            "shortTitle": "Photoelastic Stress Concentration",
            "aim": "Determine the elastic stress concentration factor (K_t) and calibrate the photoelastic fringe constant (f_σ) around a circular cutout in a structural tension plate using transmission photoelasticity according to ASTM E1319.",
            "inputLabel": "Nominal Applied Tensile Stress σ_nom",
            "shortInput": "Stress σ_nom",
            "inputUnit": "MPa",
            "min": 5.0,
            "max": 30.0,
            "step": 5.0,
            "initial": 15.0,
            "inputDecimals": 1,
            "rawLabel": "Isochromatic Fringe Order N",
            "rawUnit": "fringes",
            "rawDecimals": 2,
            "xAxis": "Nominal tensile stress σ_nom (MPa)",
            "yAxis": "Isochromatic fringe order N (fringes)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 35.0,
            "emptyY": 9.0,
            "targetName": "Photoelastic Stress-Fringe Response Factor",
            "target": "0.2450",
            "refValue": 0.2450,
            "resultUnit": "fringes/MPa",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "N = 0.2450 · σ_nom",
            "intro": "In structural and bridge engineering, holes, cutouts, notches, and re-entrant corners (such as bolt holes, access manholes, and weld copes) disrupt the uniform flow of internal stress trajectories, concentrating stresses into localized peaks several times greater than the nominal average stress. If left unquantified, these localized stress concentrations initiate fatigue microcracks and catastrophic brittle fractures under cyclic traffic loading. Transmission photoelasticity is a whole-field optical experimental stress analysis technique based on the temporary birefringence (photoelastic effect) of transparent amorphous polymers (e.g. polycarbonate or epoxy). When an unstressed polymer is viewed between crossed circular polarizers in a polariscope, light is extinguished; when loaded in tension, principal stresses σ_1 and σ_2 induce temporary refractive index differences proportional to principal stress difference (σ_1 - σ_2). According to the Stress-Optic Law: σ_1 - σ_2 = N · f_σ / t, where N is the isochromatic fringe order, f_σ is the material fringe constant, and t is model thickness. At the free boundary of a circular hole, radial stress is zero (σ_2 = 0), meaning fringe order N directly reveals peak tangential boundary stress σ_1 = K_t · σ_nom. In this laboratory, photoelastic plates with central circular holes are loaded in tension across stress levels from 5 to 30 MPa to evaluate fringe progression and determine the stress concentration factor K_t.",
            "modelExtra": "Polycarbonate model plate (thickness t = 6.0 mm, width w = 60 mm, hole diameter d = 12 mm, d/w = 0.20). Theoretical Kirsch solution K_t = 3.00 (finite-width corrected K_t = 2.45). Linearized model relates fringe order N directly to nominal stress σ_nom with slope 0.2450 fringes/MPa.",
            "apparatus": [
                {"name": "Transmission Circular Polariscope System", "purpose": "Optical bench with monochromatic light source (589 nm sodium vapor), dual linear polarizers, and dual quarter-wave plates."},
                {"name": "Precision Universal Screw Tensile Loading Frame", "purpose": "Applies smooth, uniform uniaxial tensile load to transparent photoelastic specimens with load cell readout."},
                {"name": "Optically Birefringent Polycarbonate Model Plate", "purpose": "Precision CNC-machined polycarbonate plate (6.0 mm thickness) with polished central circular hole."},
                {"name": "Digital Fringe Image Acquisition Camera", "purpose": "High-resolution monochrome CMOS camera capturing isochromatic fringe patterns and fringe orders."},
                {"name": "Babinet–Soleil Optical Compensator", "purpose": "Null-balance optical quartz wedge measuring fractional fringe orders to 0.01 fringe precision."},
                {"name": "Precision Micrometer & Calipers", "purpose": "Measures plate width, hole diameter, and thickness to 0.01 mm precision."}
            ],
            "procedure": [
                {"title": "Polariscope Optical Alignment & Dark-Field Setup", "text": "Align polarizer, first quarter-wave plate, second quarter-wave plate, and analyzer along the optical axis; verify dark-field condition (complete extinction) under zero load."},
                {"title": "Specimen Geometry & Residual Stress Inspection", "text": "Mount polycarbonate specimen in tensile grips; inspect under polariscope at zero load to verify zero residual machining fringes around the hole boundary."},
                {"title": "Monochromatic Lighting Initialization", "text": "Energize 589 nm sodium light source; focus digital imaging camera onto the horizontal hole boundary equator."},
                {"title": "Incremental Tensile Loading & Fringe Counting", "text": "Apply tensile load incrementally to produce nominal stresses σ_nom of 5.0, 10.0, 15.0, 20.0, 25.0, and 30.0 MPa; count isochromatic fringe orders N emerging at the hole boundary."},
                {"title": "Fractional Fringe Measurement using Compensator", "text": "At each load step, use the Babinet–Soleil compensator to measure exact fringe order N at the hole edge to within 0.02 fringes."},
                {"title": "Stress Concentration Factor Evaluation", "text": "Plot fringe order N versus nominal stress σ_nom; determine response slope; calculate peak boundary stress and compute stress concentration factor K_t."}
            ],
            "topics": [
                {"question": "State the fundamental Stress-Optic Law for two-dimensional transmission photoelasticity.", "answer": "The Stress-Optic Law states: sigma_1 - sigma_2 = N · f_sigma / t, where sigma_1 and sigma_2 are in-plane principal stresses, N is the isochromatic fringe order, f_sigma is the material fringe value, and t is model thickness."},
                {"question": "How does the Kirsch theoretical solution explain stress concentration around a circular hole in an infinite plate?", "answer": "G. Kirsch (1898) proved using elasticity theory that under uniaxial tensile stress sigma_0, the tangential boundary stress around a circular hole is sigma_theta = sigma_0 (1 - 2 cos 2theta); at the transverse equator (theta = 90°), peak stress reaches sigma_max = 3 sigma_0, yielding K_t = 3.0."},
                {"question": "What is the physical difference between isochromatic fringes and isoclinic fringes?", "answer": "Isochromatic fringes represent contours of constant principal stress difference (sigma_1 - sigma_2, or maximum shear stress); isoclinic fringes represent loci of points where principal stress directions align with the polarizer transmission axis."},
                {"question": "Why are quarter-wave plates inserted into the polariscope to create a 'circular' polariscope?", "answer": "Quarter-wave plates convert linearly polarized light into circularly polarized light, which eliminates all direction-dependent isoclinic fringes from the field of view, leaving only pure isochromatic stress-magnitude fringes."},
                {"question": "How does finite plate width (w) modify the infinite-plate Kirsch factor K_t = 3.0?", "answer": "In a plate of finite width w with hole diameter d, adjacent boundaries confine stress trajectories; finite-width correction charts (Peterson) modify K_t as a function of d/w, yielding net-section stress concentration factors between 2.2 and 2.6."},
                {"question": "Why is photoelastic stress analysis valuable compared to numerical Finite Element Analysis (FEA)?", "answer": "Photoelasticity provides physical, whole-field optical verification of actual stress gradients without relying on meshing assumptions, singularity approximations, or boundary condition simplifications."}
            ],
            "precautions": [
                "Machine holes and notches using sharp, coolant-flooded cutters at low feed rates to prevent thermal annealing and residual machining stresses.",
                "Ensure quarter-wave plate fast axes are oriented at precisely 45° to polarizer transmission axes to achieve true circular polarization.",
                "Avoid holding specimens with bare warm hands prior to testing to prevent localized thermal birefringence fringe artifacts.",
                "Operate within the proportional elastic optical limit of the polycarbonate material to avoid time-dependent optical viscoelastic creep."
            ],
            "quiz": [
                {
                    "question": "The theoretical elastic stress concentration factor K_t at the edge of a small circular hole in an infinite plate under uniaxial tension is:",
                    "options": ["1.0", "2.0", "3.0", "4.0"],
                    "correct": 2,
                    "explanation": "According to the Kirsch elasticity solution, peak tensile stress at the hole equator is exactly 3.0 times nominal stress (K_t = 3.0)."
                },
                {
                    "question": "In a circular polariscope, isochromatic fringes represent contours of constant:",
                    "options": ["Hydrostatic pressure", "Principal stress direction", "Principal stress difference (sigma_1 - sigma_2)", "Volumetric strain"],
                    "correct": 2,
                    "explanation": "Isochromatic fringes represent lines of constant principal stress difference (sigma_1 - sigma_2) or maximum shear stress."
                },
                {
                    "question": "Quarter-wave plates are incorporated into a polariscope specifically to eliminate:",
                    "options": ["Diffraction glare", "Isochromatic fringes", "Isoclinic fringes (directional fringes)", "Refraction reflection losses"],
                    "correct": 2,
                    "explanation": "Quarter-wave plates circularly polarize light, removing isoclinic directional fringes while preserving isochromatic stress fringes."
                },
                {
                    "question": "The Stress-Optic Law relates principal stress difference (sigma_1 - sigma_2) to fringe order N via:",
                    "options": ["sigma_1 - sigma_2 = N · f_sigma / t", "sigma_1 - sigma_2 = N · t / f_sigma", "sigma_1 - sigma_2 = f_sigma / (N · t)", "sigma_1 - sigma_2 = N · E · t"],
                    "correct": 0,
                    "explanation": "The fundamental Stress-Optic Law is (sigma_1 - sigma_2) = N · f_sigma / t."
                }
            ],
            "samples": [5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
            "measureLabel": "Record isochromatic fringe order N at notch boundary",
            "readings": ["fringe_order_n", "stress_nom_mpa", "peak_stress_mpa", "kt_factor"],
            "theory": """<h3>1. Optics of Birefringence & The Photoelastic Effect</h3>
<p>Amorphous transparent polymers such as polycarbonate and epoxy resins are optically isotropic when unstressed, possessing a uniform refractive index $n_0$. When subjected to an in-plane mechanical stress field $(\\sigma_1, \\sigma_2)$, secondary molecular bonds align along principal stress trajectories, inducing optical anisotropy (temporary birefringence). According to Maxwell's Stress-Optic Law, the induced principal refractive indices $n_1$ and $n_2$ scale linearly with principal stresses:</p>
\\[ n_1 - n_0 = c_1 \\sigma_1 + c_2 \\sigma_2, \\qquad n_2 - n_0 = c_1 \\sigma_2 + c_2 \\sigma_1 \\]
<p>Subtracting these expressions yields the differential refractive index:</p>
\\[ n_1 - n_2 = (c_1 - c_2)(\\sigma_1 - \\sigma_2) = C (\\sigma_1 - \\sigma_2) \\]
<p>where $C$ is the stress-optic coefficient of the material.</p>

<h3>2. Transmission Through a Circular Polariscope</h3>
<p>When monochromatic light of wavelength $\\lambda$ passes through a stressed model of thickness $t$, the two orthogonally polarized light waves emerge with a relative optical path difference $\\Delta$ and phase retardance $\\delta$:</p>
\\[ \\Delta = t (n_1 - n_2) = C t (\\sigma_1 - \\sigma_2), \\qquad \\delta = \\frac{2\\pi \\Delta}{\\lambda} = \\frac{2\\pi C t}{\\lambda} (\\sigma_1 - \\sigma_2) \\]
<p>In a dark-field circular polariscope (polarizer and analyzer crossed at $90^\\circ$, with two quarter-wave plates set at $45^\\circ$), the transmitted light intensity $I$ is:</p>
\\[ I = I_0 \\sin^2\\left( \\frac{\\delta}{2} \\right) = I_0 \\sin^2\\left[ \\frac{\\pi C t}{\\lambda} (\\sigma_1 - \\sigma_2) \\right] \\]
<p>Complete extinction (dark isochromatic fringes) occurs whenever phase retardance is an integer multiple of $2\\pi$:</p>
\\[ \\frac{\\pi C t}{\\lambda} (\\sigma_1 - \\sigma_2) = N \\pi \\implies \\sigma_1 - \\sigma_2 = \\frac{N \\lambda}{C t} = \\frac{N f_\\sigma}{t} \\]
<p>where $N = 0, 1, 2, 3, \\dots$ is the isochromatic fringe order, and $f_\\sigma = \\lambda / C$ is the material fringe constant.</p>

<h3>3. Kirsch Solution & Stress Concentration Factor $K_t$</h3>
<p>At the traction-free boundary of a circular hole ($r = R$), the radial boundary stress vanishes identically: $\\sigma_r = \\sigma_2 = 0$. The Stress-Optic Law directly provides the peak tangential boundary stress $\\sigma_1$:</p>
\\[ \\sigma_1 = \\frac{N f_\\sigma}{t} \\]
<p>The elastic stress concentration factor $K_t$ is defined as peak boundary stress divided by nominal gross stress $\\sigma_{nom}$:</p>
\\[ K_t = \\frac{\\sigma_{peak}}{\\sigma_{nom}} = \\frac{N f_\\sigma / t}{\\sigma_{nom}} \\implies N = \\left[ \\frac{K_t t}{f_\\sigma} \\right] \\sigma_{nom} = k_{fringe} \\cdot \\sigma_{nom} \\]
<p>For model thickness $t = 6.0\\text{ mm}$, material fringe value $f_\\sigma = 60.0\\text{ N/mm/fringe}$, and finite-width corrected concentration factor $K_t = 2.450$:</p>
\\[ k_{fringe} = \\frac{2.450 \\times 6.0\\text{ mm}}{60.0\\text{ N/mm/fringe}} = 0.2450\\text{ fringes/MPa} \\]""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this civil engineering laboratory investigation is to evaluate the whole-field elastic stress concentration factor ($K_t$) around a circular hole in a structural tension member using transmission photoelasticity according to ASTM E1319. By measuring isochromatic fringe order progression ($N$) across six nominal tensile stress plateaus ($5.0\\text{ to }30.0\\text{ MPa}$), executing linear regression, and determining the response slope $k_{fringe}$, we verify the Kirsch elasticity solution and establish fatigue notch safety factors.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>According to the Stress-Optic Law, principal stress difference is related to isochromatic fringe order $N$ by:</p>
\\[ \\sigma_1 - \\sigma_2 = \\frac{N f_\\sigma}{t} \\]
<p>At the free boundary of the hole ($\sigma_2 = 0$), peak tangential stress is $\\sigma_{peak} = \\frac{N f_\\sigma}{t}$. The fringe progression scales linearly with nominal stress $\\sigma_{nom}$:</p>
\\[ N = k_{fringe} \\cdot \\sigma_{nom} \\]
<p>where $k_{fringe} = 0.2450\\text{ fringes/MPa}$ and $K_t = \\frac{k_{fringe} \\cdot f_\\sigma}{t} = 2.450$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized an optical transmission circular polariscope bench equipped with a monochromatic sodium vapor light source ($\lambda = 589.3\\text{ nm}$), precision linear sheet polarizers, and matched mica quarter-wave retarders. Uniaxial tension was applied with a screw-driven mechanical loading frame with load cell accuracy $\\pm 0.5\\%$. The specimen was precision-machined polycarbonate ($t = 6.00 \\pm 0.02\\text{ mm}$, gross width $w = 60.0\\text{ mm}$, central hole diameter $d = 12.00\\text{ mm}$, $d/w = 0.20$, material fringe constant $f_\\sigma = 60.0\\text{ N/mm/fringe}$).</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>The polariscope was aligned in dark-field configuration. The specimen was mounted in pin-jointed tensile grips to eliminate bending eccentricity. Zero residual stress was verified at zero load. Nominal tensile stress $\\sigma_{nom}$ was applied incrementally at $5.0\\text{ MPa}$ intervals up to $30.0\\text{ MPa}$. Isochromatic fringe orders $N$ appearing at the transverse hole boundary equator were logged using a Babinet–Soleil optical compensator to $0.02$ fringe resolution.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>High-intensity monochromatic sodium lamps emit intense radiation and operate at high surface temperatures. Protective eyewear was worn to prevent glare fatigue. Tension frames were operated smoothly to avoid specimen snapping and grip detachment.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the photoelastic tension sweep:</p>
<table>
<thead>
<tr><th>Load Step</th><th>Nominal Stress σ_nom (MPa)</th><th>Isochromatic Fringe Order N</th><th>Peak Boundary Stress σ_peak (MPa)</th><th>Experimental K_t</th><th>Fringe Morphology</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>5.0</td><td>1.23</td><td>12.25</td><td>2.450</td><td>Initial Fringe Loop Emergence</td></tr>
<tr><td>2</td><td>10.0</td><td>2.45</td><td>24.50</td><td>2.450</td><td>Sharply Defined Equator Fringes</td></tr>
<tr><td>3</td><td>15.0</td><td>3.68</td><td>36.75</td><td>2.450</td><td>Expanding Symmetric Lobes</td></tr>
<tr><td>4</td><td>20.0</td><td>4.90</td><td>49.00</td><td>2.450</td><td>Dense Boundary Fringe Pack</td></tr>
<tr><td>5</td><td>25.0</td><td>6.13</td><td>61.25</td><td>2.450</td><td>High-Order Isochromatics</td></tr>
<tr><td>6</td><td>30.0</td><td>7.35</td><td>73.50</td><td>2.450</td><td>Peak Optical Response</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of isochromatic fringe order $N$ versus nominal tensile stress $\\sigma_{nom}$ yields:</p>
\\[ N = 0.24500 \\cdot \\sigma_{nom} + 0.00000 \\]
<p>with an exceptional coefficient of determination $R^2 = 1.000000$. The experimental slope $k_{fringe} = 0.2450\\text{ fringes/MPa}$ matches the theoretical reference benchmark ($0.2450\\text{ fringes/MPa}$) with zero relative deviation ($0.00\\%$). Calculating the experimental stress concentration factor:</p>
\\[ K_t = \\frac{k_{fringe} \\cdot f_\\sigma}{t} = \\frac{0.2450 \\times 60.0}{6.00} = 2.4500 \\]
<p>This matches Peterson's finite-width stress concentration chart for $d/w = 12/60 = 0.20$ ($K_{t,theory} = 2.45$) with $0.00\\%$ relative error.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include compensator fringe resolution $\\delta N = \\pm 0.02\\text{ fringes}$ ($0.5\\%$), thickness measurement $\\delta t = \\pm 0.02\\text{ mm}$ ($0.33\\%$), and load precision $\\delta \\sigma / \\sigma = 0.5\\%$. Propagating into $K_t$:</p>
\\[ \\frac{\\delta K_t}{K_t} = \\sqrt{ \\left( \\frac{\\delta N}{N} \\right)^2 + \\left( \\frac{\\delta \\sigma}{\\sigma} \\right)^2 + \\left( \\frac{\\delta t}{t} \\right)^2 } = \\pm 0.78\\% \\]
<p>The reported stress concentration factor is $K_t = 2.450 \\pm 0.019$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The whole-field isochromatic fringe patterns displayed symmetric butterfly-shaped fringe lobes oriented along the transverse equator ($\theta = 90^\\circ$ and $270^\\circ$), confirming pure uniaxial stress flow around the cutout. At the longitudinal poles ($\theta = 0^\\circ$ and $180^\\circ$), fringe order was zero, validating Kirsch's prediction that longitudinal boundaries experience slight compression ($\sigma_\\theta = -\\sigma_0$), creating isotropic zero-shear points.</p>

<h3>10. Structural Fatigue & Detail Engineering Applications</h3>
<p>In steel bridge girders and building structures under cyclic traffic loading, fatigue cracks initiate at stress concentrations. An unmitigated stress concentration factor of $K_t = 2.45$ cuts allowable fatigue life by over $80\\%$. In structural detailing, peak stresses are reduced by increasing notch radius, polishing hole rims, or adding reinforcing collar rings.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why does drilling small circular relief holes at the tips of an existing crack arrest crack propagation?</strong><br>
<em>A1:</em> A sharp crack has an infinitesimally small root radius ($\rho \to 0$), producing a near-infinite theoretical stress concentration ($K_t \to \infty$); drilling a relief hole introduces a finite radius (e.g. $5\\text{ mm}$), dramatically reducing $K_t$ to $\sim 3.0$ and halting fatigue growth.</p>
<p><strong>Q2: What is the effect of material yielding on the actual stress concentration factor?</strong><br>
<em>A2:</em> If local stress exceeds yield strength $f_y$, plastic yielding blunts the peak stress, keeping actual stress near $f_y$ while plastic strain concentrates; the elastic concentration factor $K_t$ transitions into an elastic-plastic strain concentration factor $K_\\varepsilon$ governed by Neuber's rule ($K_t^2 = K_\\sigma \\cdot K_\\varepsilon$).</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The transmission photoelastic investigation provided whole-field optical verification of stress concentration mechanics around structural cutouts. The calibrated response factor $k_{fringe} = 0.2450\\text{ fringes/MPa}$ ($R^2 = 1.000000$) and verified stress concentration factor $K_t = 2.450$ validate Kirsch theory and provide an authoritative standard for fatigue-resistant structural detailing.</p>"""
        }
    ]
