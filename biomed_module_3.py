# -*- coding: utf-8 -*-
"""Biomedical Engineering Module 3: Biomechanics, Biomaterials & Orthopaedic Implants (Labs 18–26)."""

def get_module_3():
    return [
        {
            "number": 18,
            "slug": "cortical-bone-tensile-elastic-modulus",
            "title": "Cortical Bone Tensile Elastic Modulus & Stress-Strain Tensile Testing",
            "shortTitle": "Bone Tensile Elastic Modulus",
            "aim": "Determine the longitudinal Young's modulus of cortical bone specimens loaded in uniaxial tension using extensometer strain tracking in a physiological saline bath.",
            "inputLabel": "Longitudinal Tensile Strain ε",
            "shortInput": "Strain ε",
            "inputUnit": "mstrain",
            "min": 1.0,
            "max": 6.0,
            "step": 1.0,
            "initial": 3.0,
            "inputDecimals": 1,
            "rawLabel": "Tensile Stress σ",
            "rawUnit": "MPa",
            "rawDecimals": 3,
            "xAxis": "Tensile strain ε (mstrain)",
            "yAxis": "Tensile stress σ (MPa)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.5,
            "emptyY": 60.0,
            "targetName": "Cortical Bone Young's Modulus E",
            "target": "17.5000",
            "refValue": 17.5000,
            "resultUnit": "GPa",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "σ = E · ε = 17.5000 · ε (where 1 mstrain = 10⁻³ mm/mm)",
            "measureLabel": "Execute Bone Tensile Test",
            "intro": "Bone is a complex, hierarchical, anisotropic composite biomaterial composed of mineralized collagen fibrils (hydroxyapatite crystals embedded in a type-I collagen matrix) organized into osteons (Haversian systems) in cortical compact bone. In biomechanical engineering and orthopaedic implant design, characterizing the mechanical stiffness and yield behavior of bone is critical for predicting fracture risk, modeling joint contact forces, and avoiding stress shielding in femoral hip prostheses. Under physiological tensile loading along the longitudinal axis of long bones (such as the human or bovine femur and tibia), cortical bone displays linear elastic behavior at small strains (typically ε < 0.007 or 7000 microstrain) before yielding into plastic deformation and microcracking. According to Hooke's law for linear orthotropic continuum elasticity, the uniaxial stress-strain relation along the osteon orientation is given by σ = E_L · ε, where E_L is the longitudinal Young's modulus (typically 15 to 20 GPa for mature Haversian cortical bone). In this laboratory investigation, standardized dog-bone cortical bone specimens milled along the femoral diaphysis are maintained in hydrated physiological saline at 37.0 °C and loaded in uniaxial tension using a servohydraulic materials testing system equipped with a high-resolution laser extensometer to accurately determine Young's modulus E.",
            "modelExtra": "Evaluated on machined cortical bone test coupons (gauge length 25.0 mm, rectangular cross-section 4.0 mm × 2.0 mm) excised along the longitudinal diaphyseal axis. Tested in 37 °C phosphate buffered saline (PBS) at a quasi-static strain rate of 0.001 s⁻¹. Linear elastic slope E = 17.5000 GPa is determined over strains from 1.0 to 6.0 mstrain.",
            "apparatus": [
                {"name": "Servohydraulic Biomechanical Testing Frame", "purpose": "Applies controlled uniaxial tensile displacement at constant strain rates with closed-loop actuator control."},
                {"name": "High-Precision Non-Contact Optical Video Extensometer", "purpose": "Tracks gauge-length marker displacements to 0.1 μm without contacting the delicate bone surface."},
                {"name": "Submerged Physiological Saline Chamber (37.0 °C)", "purpose": "Maintains specimen hydration and physiological temperature to prevent tissue embrittlement."},
                {"name": "Low-Capacity 5 kN Dynamic Load Cell", "purpose": "Measures applied axial tensile force with 0.1% accuracy and sub-Newton resolution."},
                {"name": "Precision Specimen Collet Grips with Serrated Inserts", "purpose": "Prevents end-slip and minimizes stress concentration outside the calibrated gauge section."},
                {"name": "Digital Micro-Caliper & Optical Measurement Microscope", "purpose": "Determines cross-sectional gauge dimensions (width and thickness) with 1 μm precision."}
            ],
            "procedure": [
                {"title": "Specimen Preparation and Hydration Equilibrium", "text": "Retrieve machined longitudinal cortical bone specimen from -20 °C storage, thaw in PBS at 37 °C, and measure cross-sectional gauge dimensions with optical micrometer."},
                {"title": "Grip Alignment and Zero Load Setting", "text": "Mount the bone specimen in the mechanical testing collet grips, verify axial alignment to prevent bending moments, and zero the 5 kN load cell in the slack position."},
                {"title": "Optical Extensometer Marker Calibration", "text": "Affix two high-contrast retro-reflective gauge markers 25.0 mm apart on the bone face and calibrate the video extensometer tracking algorithms."},
                {"title": "Preconditioning Cyclic Loading", "text": "Apply 10 cycles of triangular tensile preconditioning from 0 to 0.5 mstrain at 0.1 Hz to establish steady-state viscoelastic baseline."},
                {"title": "Quasi-Static Uniaxial Tensile Progression", "text": "Execute tensile loading ramp at 0.001 s⁻¹ through strain increments of 1.0, 2.0, 3.0, 4.0, 5.0, and 6.0 mstrain, logging load and extensometer strain at 100 Hz."},
                {"title": "Elastic Modulus Linear Regression Analysis", "text": "Convert load to engineering stress σ = F/A, plot σ versus strain ε, and calculate Young's modulus E from the slope of the linear elastic region."}
            ],
            "topics": [
                {"question": "Why is cortical bone mechanically anisotropic?", "answer": "Cortical bone consists of longitudinally aligned cylindrical osteons surrounded by cement lines; it is significantly stiffer and stronger in tension and compression along its longitudinal axis (E ≈ 17–18 GPa) than in the transverse radial or circumferential directions (E ≈ 10–12 GPa)."},
                {"question": "How does specimen hydration influence the mechanical properties of bone?", "answer": "Dehydration removes water bound within the collagen fibrils and hydroxyapatite crystal lattice, drastically increasing apparent stiffness and brittleness while decreasing ultimate strain to failure and fracture toughness by up to 50%."},
                {"question": "What is the phenomenon of stress shielding in orthopaedic joint replacement?", "answer": "When a metallic implant (e.g., cobalt-chromium or titanium, E = 110–210 GPa) is implanted into bone (E ≈ 18 GPa), the much stiffer metal carries the majority of the physiological load. Deprived of normal mechanical stress, surrounding bone undergoes osteoclast-mediated resorption according to Wolff's Law."},
                {"question": "What is the distinction between cortical (compact) bone and trabecular (cancellous) bone?", "answer": "Cortical bone is dense (porosity 5–10%) and forms the outer structural shell of bones, providing high stiffness and bending resistance, whereas trabecular bone is a porous cellular lattice (porosity 70–90%) found at epiphyses that absorbs impact energy and houses marrow."},
                {"question": "Why must strain rate be strictly controlled during bone biomechanical testing?", "answer": "Bone is a viscoelastic material whose apparent elastic modulus, yield stress, and ultimate strength increase with higher strain rates due to viscous fluid flow within canaliculi and time-dependent collagen fibril deformation."},
                {"question": "How does aging and osteoporosis alter the cortical bone tensile stress-strain curve?", "answer": "Aging and osteoporosis increase cortical porosity, widen Haversian canals, accumulate advanced glycation end-products (AGEs) in collagen, and reduce mineral density, causing significant reductions in elastic modulus, yield strength, and work to fracture."}
            ],
            "precautions": [
                "Keep specimens continuously submerged in phosphate buffered saline; surface drying alters mechanical compliance within minutes.",
                "Ensure perfect axial alignment between upper and lower grips to prevent spurious bending moments from corrupting tensile strain.",
                "Verify that strain rate remains within the quasi-static regime (0.001 s⁻¹) to avoid viscoelastic rate-hardening artifacts.",
                "Do not exceed 7.0 mstrain to ensure testing remains strictly within the linear elastic, non-damaging reversible regime."
            ],
            "limitations": [
                "The linear elastic Hookean model applies strictly to small strains (ε < 0.006); post-yield microcracking requires continuum damage mechanics.",
                "Assumes homogeneous continuum stress distribution, neglecting microscopic stress concentrations around individual Haversian canals.",
                "Modulus value is specific to the diaphyseal longitudinal orientation; transverse and shear moduli require separate directional testing.",
                "Testing is performed at room or 37 °C saline in vitro; living bone exhibits active cellular repair and remodeling not captured in vitro."
            ],
            "quiz": [
                {
                    "question": "What is the typical longitudinal Young's modulus of mature human femoral cortical bone?",
                    "options": ["1.5 to 2.0 GPa", "15 to 20 GPa", "100 to 120 GPa", "200 to 220 GPa"],
                    "correct": 1,
                    "explanation": "Human cortical bone has a longitudinal elastic modulus of approximately 17 to 18 GPa, balanced between stiffness and fracture toughness."
                },
                {
                    "question": "Why does orthopaedic femoral stem implantation cause bone resorption?",
                    "options": ["Due to stress shielding where the much stiffer metal implant carries load away from bone", "Because metal dissolves bone minerals directly", "Due to bone overheating from friction", "Because bone cannot grow near titanium"],
                    "correct": 0,
                    "explanation": "Stress shielding occurs because stiff titanium or CoCr implants bear disproportionate stress, causing bone to resorb according to Wolff's Law."
                },
                {
                    "question": "If an applied strain of 4.0 mstrain (0.004) produces a tensile stress of 70.0 MPa, what is Young's modulus E?",
                    "options": ["8.75 GPa", "17.50 GPa", "35.00 GPa", "70.00 GPa"],
                    "correct": 1,
                    "explanation": "E = σ / ε = 70.0 MPa / (0.0040) = 17,500 MPa = 17.50 GPa."
                },
                {
                    "question": "What is the primary organic constituent of the bone extracellular matrix?",
                    "options": ["Type-I collagen", "Elastin", "Keratin", "Actin"],
                    "correct": 0,
                    "explanation": "Type-I collagen fibrils comprise over 90% of the organic matrix of bone, providing tensile strength and toughness."
                }
            ],
            "settings": ["Specimen: Bovine diaphyseal cortical bone (longitudinal)", "Gauge dimensions: 25.0 mm length × 4.0 mm width × 2.0 mm thickness", "Environment: 37.0 °C phosphate buffered saline (PBS)"],
            "samples": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🦴", "label": "1. Bone Tensile Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Stress-Strain Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Extensometer Sandbox"}
            ]
        },
        {
            "number": 19,
            "slug": "articular-cartilage-confined-compression-creep",
            "title": "Articular Cartilage Confined Compression & Equilibrium Aggregate Modulus",
            "shortTitle": "Cartilage Aggregate Modulus",
            "aim": "Determine the equilibrium aggregate compressive modulus H_A of articular cartilage under confined compression creep testing using Mow's biphasic biomechanical theory.",
            "inputLabel": "Equilibrium Compressive Strain ε_c",
            "shortInput": "Strain ε_c",
            "inputUnit": "ratio",
            "min": 0.05,
            "max": 0.30,
            "step": 0.05,
            "initial": 0.15,
            "inputDecimals": 2,
            "rawLabel": "Equilibrium Compressive Stress σ_c",
            "rawUnit": "MPa",
            "rawDecimals": 4,
            "xAxis": "Equilibrium compressive strain ε_c",
            "yAxis": "Equilibrium compressive stress σ_c (MPa)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 0.18,
            "emptyY": 0.12,
            "targetName": "Equilibrium Aggregate Modulus H_A",
            "target": "0.6500",
            "refValue": 0.6500,
            "resultUnit": "MPa",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "σ_c = H_A · ε_c = 0.6500 · ε_c",
            "measureLabel": "Execute Cartilage Creep Step",
            "intro": "Articular cartilage is a specialized avascular, aneural connective tissue that lines the articulating surfaces of diarthrodial joints (e.g., knee and hip), providing near-frictionless gliding and load transmission across millions of gait cycles. Mechanically, cartilage is modeled using the biphasic theory formulated by Van C. Mow, which treats the tissue as a mixture of an incompressible porous-permeable solid matrix (composed of a type-II collagen fibrillar network entrapping negatively charged aggregating proteoglycans/aggrecan) and an interstitial fluid phase (water with mobile physiological electrolytes, comprising 65–80% of wet weight). Under confined compression within an impermeable chamber loaded via a rigid porous filter platen, fluid exudes axially until interstitial fluid pressure dissipates completely. At creep equilibrium (as t → ∞), fluid flow ceases, the solid matrix alone supports the total applied compressive stress σ_c, and the tissue strain ε_c reaches a steady plateau governed by the aggregate modulus: σ_c = H_A · ε_c. The aggregate modulus H_A represents the intrinsic stiffness of the cartilage solid matrix in uniaxial confined compression, combining Young's modulus and Poisson's ratio: H_A = E·(1 - ν)/[(1 + ν)·(1 - 2ν)]. In this experiment, cylindrical osteochondral cartilage plugs are tested in a precision confined compression chamber to evaluate equilibrium stress-strain behavior and quantify H_A.",
            "modelExtra": "Evaluated on cylindrical articular cartilage test plugs (diameter 4.0 mm, initial thickness h_0 = 1.50 mm) excised from bovine femoral condyles. Tested in 0.15 M NaCl saline bath at 22 °C under stepwise creep loads until equilibrium strain ε_c is achieved. Linear aggregate slope H_A = 0.6500 MPa across strains 0.05 to 0.30.",
            "apparatus": [
                {"name": "Confined Compression Mechanical Indentation Rig", "purpose": "Applies controlled axial compressive tare and creep step forces with micro-Newton resolution."},
                {"name": "Sintered Porous Titanium Platen (pore size 20 μm)", "purpose": "Allows unhindered one-dimensional axial exudation of interstitial fluid while supporting the solid matrix."},
                {"name": "Precision Stainless Steel Confined Compression Well", "purpose": "Provides rigid radial boundary confinement preventing lateral cartilage expansion (radial strain ε_r = 0)."},
                {"name": "Sub-Micron LVDT Displacement Transducer", "purpose": "Measures creep displacement and equilibrium compressive strain ε_c with 0.05 μm resolution."},
                {"name": "Temperature-Controlled Physiological Saline Chamber", "purpose": "Maintains 0.15 M NaCl osmotic balance preventing abnormal proteoglycan swelling."},
                {"name": "Automated Multi-Hour Data Acquisition System", "purpose": "Records creep transient curves over 3600 seconds per load step until equilibrium is confirmed (dε/dt < 10⁻⁶ s⁻¹)."}
            ],
            "procedure": [
                {"title": "Cartilage Plug Harvest and Thickness Metrology", "text": "Harvest 4.0 mm diameter full-thickness cartilage plugs from bovine femoral condyles and measure initial uncompressed thickness h_0 using a current-sensing micrometer."},
                {"title": "Confined Well Placement and Osmotic Equilibration", "text": "Place the plug snugly into the precision stainless steel confining well, submerge in 0.15 M physiological saline, and allow 30 minutes for osmotic equilibration."},
                {"title": "Tare Load and Zero Baseline Contact", "text": "Lower the porous titanium platen onto the cartilage surface until a small tare load (0.01 N) is registered, establishing the zero reference displacement position."},
                {"title": "Stepwise Creep Load Application", "text": "Apply a static axial compressive stress step and track continuous vertical displacement as fluid exudes through the porous platen."},
                {"title": "Equilibrium Creep Criterion Verification", "text": "Monitor displacement rate until equilibrium is reached (defined as displacement change < 0.2 μm over 15 minutes, typically requiring 45 to 60 minutes per step)."},
                {"title": "Multi-Step Stress-Strain Regression", "text": "Repeat creep equilibration across successive strain levels ε_c = 0.05, 0.10, 0.15, 0.20, 0.25, and 0.30, and determine the equilibrium aggregate modulus H_A."}
            ],
            "topics": [
                {"question": "What is the physical interpretation of the aggregate modulus H_A?", "answer": "The aggregate modulus H_A is the apparent equilibrium compressive stiffness of the porous-permeable solid matrix under zero lateral strain confinement; it quantifies the combined resistance of the collagen network and fixed proteoglycan charge density to compression after fluid flow ceases."},
                {"question": "How does interstitial fluid pressurization protect articular cartilage during joint loading?", "answer": "During rapid physiological loading (e.g., heel strike during running), interstitial water cannot escape immediately due to low matrix permeability; the pressurization of the fluid phase carries over 90% of the joint contact stress, shielding the solid collagen-proteoglycan matrix from destructive shear stresses."},
                {"question": "Why does cartilage require 30 to 60 minutes to reach creep equilibrium in confined compression?", "answer": "Cartilage has extremely low hydraulic permeability (k ≈ 10⁻¹⁵ m⁴/(N·s)). The high frictional drag between flowing interstitial water and the microscopic pore spaces of the dense solid matrix severely slows fluid exudation, creating prolonged viscoelastic creep."},
                {"question": "What causes Donnan osmotic swelling pressure in articular cartilage?", "answer": "Sulfated glycosaminoglycan (GAG) chains on aggrecan molecules possess dense negative carboxyl and sulfate charges (fixed charge density, FCD). To maintain electroneutrality, mobile sodium ions are drawn into the tissue, creating an osmotic pressure that swells and pretensions the collagen network."},
                {"question": "How does osteoarthritis alter cartilage mechanical properties?", "answer": "In early osteoarthritis, superficial collagen fibrils disrupt and proteoglycan content is lost, drastically reducing the aggregate modulus H_A and increasing hydraulic permeability k, impairing fluid pressurization and causing rapid wear."},
                {"question": "Why is confined compression used instead of unconfined compression to measure H_A?", "answer": "Confined compression enforces one-dimensional axial displacement with zero lateral strain (ε_x = ε_y = 0), matching the mathematical boundary conditions of Mow's 1D biphasic equations and allowing direct decoupling of solid matrix aggregate modulus from fluid permeability."}
            ],
            "precautions": [
                "Ensure perfect cylindrical fit of the specimen in the confining well to eliminate lateral fluid leakage around the sample perimeter.",
                "Maintain constant 0.15 M NaCl ionic strength; hypoosmotic solutions cause proteoglycan swelling that alters baseline thickness.",
                "Wait until creep rate satisfies the rigorous equilibrium criterion (dε/dt < 10⁻⁶ s⁻¹) before recording equilibrium stress.",
                "Keep testing temperature stable at 22 °C to avoid thermal expansion drift of the displacement transducer frame."
            ],
            "limitations": [
                "The linear aggregate modulus model applies to infinitesimal to moderate strains (ε_c ≤ 0.30); higher compressions exhibit strain-dependent stiffening.",
                "Assumes homogeneous solid matrix properties through depth, whereas cartilage exhibits depth-dependent zoning (superficial, middle, deep).",
                "Applies to equilibrium conditions after fluid flow ceases; dynamic viscoelastic response requires full biphasic poroelastic modeling.",
                "Testing is performed in simple saline without synovial fluid lubricin or hyaluronic acid boundary lubricants."
            ],
            "quiz": [
                {
                    "question": "What constituent carries the majority of joint contact stress during rapid dynamic impact in articular cartilage?",
                    "options": ["Pressurized interstitial fluid", "The porous titanium platen", "Subchondral cortical bone", "Superficial chondrocyte cells"],
                    "correct": 0,
                    "explanation": "Due to low hydraulic permeability, rapid loading pressurizes interstitial fluid, which bears over 90% of the applied load and protects the solid matrix."
                },
                {
                    "question": "In Mow's biphasic theory, what occurs at creep equilibrium in confined compression?",
                    "options": ["Fluid pressure reaches maximum", "Fluid flow ceases and the solid matrix supports the entire applied compressive load", "The cartilage completely dissolves", "Collagen fibers snap"],
                    "correct": 1,
                    "explanation": "At creep equilibrium, fluid pressure drops to zero, fluid exudation stops, and the porous solid matrix carries the entire compressive stress."
                },
                {
                    "question": "If an equilibrium compressive strain of 0.20 corresponds to an equilibrium stress of 0.1300 MPa, what is H_A?",
                    "options": ["0.3250 MPa", "0.6500 MPa", "1.3000 MPa", "2.6000 MPa"],
                    "correct": 1,
                    "explanation": "H_A = σ_c / ε_c = 0.1300 MPa / 0.20 = 0.6500 MPa."
                },
                {
                    "question": "What molecule imparts the fixed negative electrical charge density in articular cartilage?",
                    "options": ["Aggrecan (sulfated glycosaminoglycans)", "Type-II collagen", "Phospholipids", "Calcium hydroxyapatite"],
                    "correct": 0,
                    "explanation": "Aggrecan proteoglycans contain sulfated GAGs (chondroitin sulfate and keratan sulfate) that carry negative charges, generating Donnan osmotic swelling."
                }
            ],
            "settings": ["Specimen: Bovine femoral condyle cartilage plug (Ø 4.0 mm, h_0 = 1.50 mm)", "Porous filter: Sintered titanium platen (20 μm pore size)", "Bath: 0.15 M NaCl physiological saline at 22 °C"],
            "samples": [0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🔬", "label": "1. Confined Chamber Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Equilibrium Stress-Strain"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Mow Biphasic Sandbox"}
            ]
        },
        {
            "number": 20,
            "slug": "titanium-alloy-orthopaedic-implant-four-point-bending",
            "title": "Titanium Alloy Orthopaedic Bone Plate Four-Point Bending Compliance",
            "shortTitle": "Bone Plate Four-Point Bending",
            "aim": "Evaluate the structural bending compliance C_b and flexural rigidity of a medical Ti-6Al-4V ELI bone fracture fixation plate under standardized ASTM F382 four-point bending.",
            "inputLabel": "Total Bending Load W",
            "shortInput": "Load W",
            "inputUnit": "N",
            "min": 100.0,
            "max": 600.0,
            "step": 100.0,
            "initial": 300.0,
            "inputDecimals": 1,
            "rawLabel": "Centerline Deflection δ",
            "rawUnit": "mm",
            "rawDecimals": 4,
            "xAxis": "Applied bending load W (N)",
            "yAxis": "Mid-span deflection δ (mm)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 350.0,
            "emptyY": 1.5,
            "targetName": "Bending Compliance C_b",
            "target": "0.0042",
            "refValue": 0.0042,
            "resultUnit": "mm/N",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "δ = C_b · W = 0.0042 · W",
            "measureLabel": "Execute Four-Point Flexure Test",
            "intro": "Internal bone fracture fixation plates are medical devices surgically affixed across fractured cortical bone segments to maintain anatomical reduction, stabilize fragments, and facilitate primary or secondary osseous healing. To evaluate the mechanical performance, bending stiffness, and fatigue strength of orthopaedic fracture plates, the American Society for Testing and Materials established the standard specification ASTM F382 ('Standard Specification and Test Method for Metallic Bone Plates'). Four-point bending is universally specified over three-point bending because it creates a region of pure bending between the two inner loading rollers—subjecting the critical plate segment (typically containing screw holes that create stress concentrations) to a constant bending moment M = (W/2) · a without transverse shear forces. Under linear elastic Euler-Bernoulli beam theory, the mid-span deflection δ of a plate supported over outer span L with inner span a is directly proportional to total applied load W: δ = [W·a·(3L² - 4a²) / (48·E·I)] = C_b · W, where C_b is the structural bending compliance (mm/N) and E·I is the flexural rigidity (N·m²). Titanium alloy Ti-6Al-4V ELI (Extra Low Interstitial) is the clinical gold standard due to its excellent biocompatibility, corrosion resistance, and lower modulus (110 GPa vs. 200 GPa for 316L stainless steel), which mitigates stress shielding. In this laboratory investigation, an instrumented ASTM F382 four-point bending fixture evaluates the structural compliance C_b of a medical titanium dynamic compression plate (DCP).",
            "modelExtra": "Evaluated on a 6-hole medical-grade Ti-6Al-4V ELI LC-DCP plate (thickness 3.8 mm, width 11.0 mm) tested in an ASTM F382 fixture with outer span L = 100 mm and inner load span a = 25 mm. Tested from 100 N to 600 N in the linear elastic regime. Structural compliance C_b = 0.0042 mm/N.",
            "apparatus": [
                {"name": "ASTM F382 Precision Four-Point Bending Fixture", "purpose": "Provides hardened steel cylindrical rollers (diameter 10 mm) with outer span L = 100 mm and inner span a = 25 mm."},
                {"name": "Electromechanical Materials Testing Machine", "purpose": "Applies controlled displacement rates from 0.1 to 10 mm/min with high-precision closed-loop encoder."},
                {"name": "Medical Grade Ti-6Al-4V ELI Dynamic Compression Plate", "purpose": "6-hole osteosynthesis plate with staggered screw hole geometry for fracture stabilization."},
                {"name": "Precision 5 kN Low-Profile Load Cell", "purpose": "Measures total applied vertical force W with 0.1% full-scale accuracy."},
                {"name": "High-Accuracy Centerline LVDT Deflectometer", "purpose": "Directly measures bottom-surface mid-span vertical deflection δ independent of machine frame compliance."},
                {"name": "Digital Data Acquisition Console", "purpose": "Digitizes simultaneous force and deflection channels at 1 kHz with 24-bit analog-to-digital resolution."}
            ],
            "procedure": [
                {"title": "Fixture Geometry Calibration", "text": "Set outer roller span to exactly L = 100.0 mm and inner roller span to a = 25.0 mm using precision gauge blocks; verify parallelism of all four cylindrical rollers."},
                {"title": "Plate Centering and Zero Contact", "text": "Position the titanium plate symmetrically across the support rollers so that a central screw hole aligns with the middle of the pure bending span."},
                {"title": "Centerline Deflectometer Positioning", "text": "Position the precision LVDT directly beneath the plate center span and adjust the spring-loaded probe tip to make positive contact."},
                {"title": "Tare Load and Crosshead Zeroing", "text": "Apply a seating tare load of 10 N to eliminate mechanical play and zero both load and deflection readings."},
                {"title": "Stepwise Loading Sequence", "text": "Advance crosshead at 1.0 mm/min through load increments of 100, 200, 300, 400, 500, and 600 N, recording stabilized mid-span deflection δ at each step."},
                {"title": "Structural Compliance Regression", "text": "Plot mid-span deflection δ versus applied load W and compute the structural bending compliance C_b and flexural rigidity E·I via linear regression."}
            ],
            "topics": [
                {"question": "Why does ASTM F382 specify four-point bending rather than three-point bending?", "answer": "Four-point bending generates a constant bending moment and zero shear force across the entire segment between the inner rollers; this ensures that stress concentrations at screw holes are tested in pure bending without confounding shear stresses."},
                {"question": "What is the structural consequence of screw holes in an orthopaedic bone plate?", "answer": "Screw holes act as geometric stress concentrators (K_t ≈ 2.0 to 2.5), significantly increasing local peak tensile stresses on the upper plate surface during bending and serving as primary initiation sites for fatigue cracking."},
                {"question": "Why is Ti-6Al-4V ELI preferred over 316L stainless steel for fracture fixation plates?", "answer": "Ti-6Al-4V ELI has superior biocompatibility, excellent fatigue strength, and an elastic modulus (~110 GPa) roughly half that of stainless steel (~200 GPa), which reduces bone stress shielding and promotes faster callus remodeling."},
                {"question": "What is the relationship between bending compliance C_b and flexural rigidity E·I?", "answer": "Compliance C_b is inversely proportional to flexural rigidity: C_b = a·(3L² - 4a²) / (48·E·I). A stiffer plate has lower compliance C_b and higher flexural rigidity E·I."},
                {"question": "What is the difference between a conventional DCP and a Locking Compression Plate (LCP)?", "answer": "A conventional DCP relies on friction generated by tightening cortical screws into bone to compress the plate against the periosteum, whereas an LCP uses threaded screw heads that lock directly into the plate, forming a rigid fixed-angle internal fixator that preserves periosteal blood supply."},
                {"question": "What is proof load and bending strength according to ASTM F382?", "answer": "The bending proof load is the load at which the force-deflection curve departs from linearity by a 0.2% offset deflection, representing the onset of permanent plastic deformation in the implant."}
            ],
            "precautions": [
                "Verify that the LVDT probe tip contacts the plate bottom surface directly to avoid including roller Hertzian indentation in deflection measurements.",
                "Ensure inner and outer spans are precisely centered and parallel to prevent asymmetrical torsional twisting.",
                "Do not exceed the elastic limit of the titanium plate (650 N) to avoid permanent plastic deformation during calibration.",
                "Verify that roller surfaces are polished and lubricated with light oil to minimize frictional axial binding."
            ],
            "limitations": [
                "The linear compliance model applies strictly within the elastic limit; plastic yielding requires non-linear elastoplastic analysis.",
                "Euler-Bernoulli beam theory neglects transverse shear deformation and local roller contact indentation (Hertzian contact).",
                "Assumes uniform prismatic cross-section, whereas commercial plates feature complex contouring, bevels, and countersunk holes.",
                "Static four-point bending does not account for cyclic fatigue degradation or dynamic in-vivo multi-axial loads."
            ],
            "quiz": [
                {
                    "question": "What is the primary advantage of four-point bending over three-point bending in implant testing?",
                    "options": ["It creates a region of pure bending moment with zero shear force between inner rollers", "It breaks the plate faster", "It requires no calibration", "It uses less electricity"],
                    "correct": 0,
                    "explanation": "Four-point bending creates a uniform bending moment with zero shear force across the inner span, testing screw holes in pure flexure."
                },
                {
                    "question": "Why does Ti-6Al-4V ELI reduce bone stress shielding compared to 316L stainless steel?",
                    "options": ["Its elastic modulus (110 GPa) is closer to cortical bone (18 GPa) than stainless steel (200 GPa)", "It is a radioactive tracer", "It is heavier than steel", "It melts inside the body"],
                    "correct": 0,
                    "explanation": "Titanium's lower modulus transfers a greater proportion of physiological loads back to healing bone, reducing stress shielding bone loss."
                },
                {
                    "question": "If an applied load of 500 N produces a mid-span deflection of 2.100 mm, what is the bending compliance C_b?",
                    "options": ["0.0021 mm/N", "0.0042 mm/N", "0.0084 mm/N", "0.0420 mm/N"],
                    "correct": 1,
                    "explanation": "C_b = δ / W = 2.100 mm / 500 N = 0.0042 mm/N."
                },
                {
                    "question": "Which ASTM international standard defines test methods for metallic bone plates?",
                    "options": ["ASTM F382", "ASTM E8", "ASTM D638", "ASTM G31"],
                    "correct": 0,
                    "explanation": "ASTM F382 is the standard specification and test method for metallic bone plates used in orthopaedic internal fixation."
                }
            ],
            "settings": ["Implant: Ti-6Al-4V ELI 6-hole LC-DCP (11.0 mm × 3.8 mm)", "Fixture: ASTM F382 four-point bending (L = 100 mm, a = 25 mm)", "Loading rate: 1.0 mm/min displacement control"],
            "samples": [100.0, 200.0, 300.0, 400.0, 500.0, 600.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🔩", "label": "1. ASTM F382 Bending Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Load-Deflection Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Beam Compliance Sandbox"}
            ]
        },
        {
            "number": 21,
            "slug": "uhmwpe-artificial-joint-pin-on-disk-wear",
            "title": "UHMWPE Artificial Joint Bearing Pin-on-Disk Wear Factor Testing",
            "shortTitle": "UHMWPE Joint Wear Factor",
            "aim": "Determine the Archard volumetric wear factor k_w of medical-grade ultra-high-molecular-weight polyethylene (UHMWPE) sliding against CoCr alloy in bovine serum.",
            "inputLabel": "Total Sliding Distance L_s",
            "shortInput": "Distance L_s",
            "inputUnit": "km",
            "min": 2.0,
            "max": 12.0,
            "step": 2.0,
            "initial": 6.0,
            "inputDecimals": 1,
            "rawLabel": "Volumetric Wear Loss V_w",
            "rawUnit": "mm³",
            "rawDecimals": 3,
            "xAxis": "Sliding distance L_s (km)",
            "yAxis": "Volumetric wear loss V_w (mm³)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 7.0,
            "emptyY": 15.0,
            "targetName": "Volumetric Wear Rate k_w",
            "target": "2.1500",
            "refValue": 2.1500,
            "resultUnit": "mm³/km",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "V_w = k_w · L_s = 2.1500 · L_s (under constant 200 N normal load)",
            "measureLabel": "Execute Tribological Wear Run",
            "intro": "Total joint arthroplasty (TJA) of the hip and knee is among the most successful surgical interventions in modern medicine, restoring mobility and relieving intractable pain in millions of patients. However, the long-term clinical longevity of artificial joints is fundamentally limited by tribological wear of the bearing surfaces. In metal-on-polyethylene hip prostheses, a cobalt-chromium-molybdenum (CoCrMo) or ceramic femoral head articulates against an ultra-high-molecular-weight polyethylene (UHMWPE) acetabular cup. Over millions of gait cycles, microscopic adhesive and abrasive wear processes release billions of sub-micron polyethylene wear particles into the periprosthetic joint space. Macrophages phagocytose these particles, triggering chronic inflammatory cascades (osteolysis) that lead to aseptic loosening and implant failure. According to Archard's classic wear law, the cumulative volumetric wear loss V_w is directly proportional to normal contact load F_N and sliding distance L_s: V_w = k_w · L_s (under constant load F_N = 200 N), where k_w is the steady-state volumetric wear rate (mm³/km). Highly cross-linked polyethylene (HXLPE) irradiated with gamma or electron-beam radiation substantially reduces k_w compared to conventional UHMWPE. In this laboratory experiment, a multi-station pin-on-disk tribometer submerged in dilute bovine calf serum at 37.0 °C evaluates UHMWPE wear progression across 12 km of articulation.",
            "modelExtra": "Evaluated on medical GUR 1020 UHMWPE cylindrical pins (diameter 9.5 mm, contact area 71 mm²) articulating against mirror-polished CoCrMo disks (Ra = 0.015 μm) in 25% bovine serum at 37 °C. Constant normal load F_N = 200 N at 1.0 Hz cyclic articulation. Linear wear rate k_w = 2.1500 mm³/km.",
            "apparatus": [
                {"name": "Multi-Station Pin-on-Disk Orthopaedic Tribometer", "purpose": "Applies controlled reciprocating motion and normal load with continuous cycle counting."},
                {"name": "Medical Grade GUR 1020 UHMWPE Test Pins", "purpose": "Standardized cylindrical polymer bearing specimens machined from compression-molded rod."},
                {"name": "Mirror-Polished CoCrMo Articulation Disks (Ra < 0.02 μm)", "purpose": "Represents metallic femoral prosthetic counterface meeting ISO 5834 surface standards."},
                {"name": "Thermostatically Controlled Serum Bath (37.0 °C)", "purpose": "Maintains 25% bovine calf serum lubricant with 0.2% sodium azide antibacterial agent."},
                {"name": "Sub-Microgram Ultra-Microbalance (0.1 μg resolution)", "purpose": "Measures gravimetric wear loss before and after sliding intervals with vacuum desiccator drying."},
                {"name": "Soak-Control Unloaded UHMWPE Reference Pin", "purpose": "Corrects for fluid absorption mass gain to isolate true tribological wear mass loss."}
            ],
            "procedure": [
                {"title": "Specimen Cleaning and Initial Mass Metrology", "text": "Clean UHMWPE test pins and unloaded soak-control pins in ultrasonic baths of ethanol and deionized water, vacuum desiccate for 48 hours, and weigh on ultra-microbalance (m_0)."},
                {"title": "Disk Counterface Profilometry", "text": "Measure mirror-polished CoCrMo disk surface roughness using optical profilometry, verifying Ra < 0.02 μm across the circular wear track."},
                {"title": "Lubricant Preparation and Chamber Thermal Equilibration", "text": "Fill tribometer reservoir with 25% bovine calf serum containing 0.2% sodium azide, heat to 37.0 °C, and verify temperature stability."},
                {"title": "Normal Load Application and Kinematic Run", "text": "Mount the UHMWPE pin in the articulated holder, apply 200 N normal force via deadweights, and initiate reciprocating circular motion at 1.0 Hz."},
                {"title": "Periodic Gravimetric Interruption and Soak Correction", "text": "At sliding intervals of 2, 4, 6, 8, 10, and 12 km, remove pins, clean, desiccate, reweigh, and correct for soak fluid absorption: Δm = (m_0 - m_t) + Δm_soak."},
                {"title": "Volumetric Wear Rate Calculation", "text": "Convert corrected mass loss to volume loss V_w = Δm / ρ (UHMWPE density ρ = 0.935 g/cm³), plot V_w versus sliding distance L_s, and calculate wear rate k_w."}
            ],
            "topics": [
                {"question": "Why is bovine serum specified as the lubricant in joint simulator wear testing?", "answer": "Bovine calf serum contains physiological albumin and globulin proteins that adsorb onto bearing surfaces, replicating the boundary lubrication and protein denaturation mechanisms found in human synovial fluid; testing in pure saline produces unphysiological polymer transfer films and false wear rates."},
                {"question": "What is the biological consequence of sub-micron polyethylene wear debris?", "answer": "Particles between 0.1 and 1.0 μm are easily engulfed by tissue macrophages, which cannot digest the polymer. This activates NF-κB inflammatory signaling, releasing TNF-α, IL-1β, and RANKL, stimulating osteoclasts to resorb bone around the implant (periprosthetic osteolysis)."},
                {"question": "How does irradiation cross-linking reduce UHMWPE wear?", "answer": "Ionizing radiation (gamma or electron beam) cleaves polymer chains and generates free radicals that recombine into a dense 3D covalent cross-linked network, preventing molecular orientation and lamellar shear peeling along the sliding path."},
                {"question": "Why must soak-control pins be weighed alongside active wear pins?", "answer": "UHMWPE absorbs moisture and serum lipids over weeks of submerged testing, causing an apparent mass gain that can mask or underestimate true wear loss; subtracting soak-control weight gain isolates true abrasive/adhesive mass loss."},
                {"question": "What is the difference between linear wear and volumetric wear?", "answer": "Linear wear measures the penetration depth (mm) of the femoral head into the acetabular cup, whereas volumetric wear (mm³) reflects the total physical volume of debris particles generated and biologically released into the joint capsule."},
                {"question": "What is Archard's wear law and its dimensionless wear coefficient?", "answer": "Archard's law states V_w = K · F_N · L_s / H, where K is the dimensionless wear coefficient, F_N is normal load, L_s is sliding distance, and H is the indentation hardness of the softer material."}
            ],
            "precautions": [
                "Keep bovine serum continuously refrigerated before use and add sodium azide to prevent bacterial growth and protein breakdown.",
                "Ensure strict vacuum desiccation protocols (minimum 48 hours) before gravimetric weighing to achieve dry equilibrium.",
                "Verify counterface disk surface is pristine and free of scratch ridges that would induce severe abrasive cutting wear.",
                "Maintain constant normal load (200 N) and sliding speed (1.0 Hz) to avoid frictional heating above physiological 37 °C."
            ],
            "limitations": [
                "The simple pin-on-disk geometry does not replicate multi-directional cross-shear kinematics found in clinical hip gait cycles.",
                "Assumes constant steady-state wear rate, neglecting initial running-in bedding wear during early articulation.",
                "Dilute bovine serum (25%) approximates synovial fluid protein concentration but lacks hyaluronic acid lubricity.",
                "Static deadweight loading does not simulate physiological stance-phase and swing-phase dynamic walking cycles."
            ],
            "quiz": [
                {
                    "question": "What is the primary cause of late aseptic loosening in metal-on-polyethylene artificial hips?",
                    "options": ["Macrophage-mediated osteolysis triggered by sub-micron UHMWPE wear debris", "Bone cancer caused by cobalt ions", "Allergic reaction to surgical stitches", "Polyethylene melting from body temperature"],
                    "correct": 0,
                    "explanation": "Macrophages engulfing microscopic UHMWPE wear debris release inflammatory cytokines that activate osteoclasts, causing periprosthetic bone resorption."
                },
                {
                    "question": "Why is bovine calf serum used instead of water or saline in joint wear testing?",
                    "options": ["To replicate the protein boundary lubrication behavior of human synovial fluid", "Because water is too expensive", "To dye the plastic blue", "To speed up testing by 100 times"],
                    "correct": 0,
                    "explanation": "Serum proteins adsorb onto bearing surfaces, replicating the physiological boundary lubrication and preventing unphysiological polymer transfer films."
                },
                {
                    "question": "If a sliding distance of 10.0 km produces a corrected volumetric wear loss of 21.50 mm³, what is the wear rate k_w?",
                    "options": ["1.075 mm³/km", "2.150 mm³/km", "4.300 mm³/km", "21.50 mm³/km"],
                    "correct": 1,
                    "explanation": "k_w = V_w / L_s = 21.50 mm³ / 10.0 km = 2.1500 mm³/km."
                },
                {
                    "question": "What purpose does an unloaded soak-control pin serve during wear testing?",
                    "options": ["It corrects for fluid absorption mass gain during testing", "It acts as a spare specimen in case of breakage", "It holds the thermometer in place", "It measures friction coefficient directly"],
                    "correct": 0,
                    "explanation": "UHMWPE absorbs serum water and lipids; subtracting soak control weight gain is necessary to isolate true mechanical wear mass loss."
                }
            ],
            "settings": ["Material: Medical GUR 1020 UHMWPE pin against CoCrMo disk", "Normal load: 200.0 N (contact pressure ~2.8 MPa)", "Lubricant: 25% bovine calf serum at 37.0 °C with sodium azide"],
            "samples": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "⚙️", "label": "1. Pin-on-Disk Tribometer"},
                {"id": "compare", "icon": "📊", "label": "2. Volumetric Wear vs Distance"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Archard Wear Sandbox"}
            ]
        },
        {
            "number": 22,
            "slug": "hydrogel-scaffold-swelling-degradation-kinetics",
            "title": "Biodegradable Hydrogel Scaffold Hydrolytic Degradation Kinetics",
            "shortTitle": "Hydrogel Scaffold Degradation",
            "aim": "Quantify the hydrolytic degradation rate constant k_d and mass loss kinetics of a poly(lactic-co-glycolic acid) / PEG hydrogel tissue engineering scaffold in PBS at 37.0 °C.",
            "inputLabel": "Incubation Time t",
            "shortInput": "Time t",
            "inputUnit": "days",
            "min": 2.0,
            "max": 12.0,
            "step": 2.0,
            "initial": 6.0,
            "inputDecimals": 1,
            "rawLabel": "Residual Dry Mass Percentage M_res",
            "rawUnit": "%",
            "rawDecimals": 3,
            "xAxis": "Incubation time t (days)",
            "yAxis": "Residual dry mass M_res (%)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 7.0,
            "emptyY": 75.0,
            "targetName": "Degradation Rate Constant k_d",
            "target": "3.2000",
            "refValue": 3.2000,
            "resultUnit": "%/day",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "M_res = -k_d · t + M_0 = -3.2000 · t + 98.0000",
            "measureLabel": "Measure Scaffold Degradation",
            "intro": "In regenerative medicine and tissue engineering, synthetic and natural biodegradable hydrogel scaffolds provide three-dimensional porous architectures that guide cell adhesion, proliferation, differentiation, and extracellular matrix deposition. An ideal tissue engineering scaffold must exhibit synchronized degradation kinetics: as implanted cells synthesize endogenous structural matrix (e.g., collagen and glycosaminoglycans), the artificial scaffold should degrade hydrolytically or enzymatically at an equivalent rate, transferring mechanical load seamlessly to the developing neotissue without inducing toxic degradation products or chronic foreign body reactions. Poly(lactic-co-glycolic acid) (PLGA) and cross-linked poly(ethylene glycol) (PEG) hydrogels degrade primarily via non-enzymatic hydrolytic cleavage of ester bonds in their polymer backbone. In bulk-degrading hydrophilic hydrogel networks, water penetrates the matrix rapidly, causing uniform ester cleavage throughout the entire volume. During the initial linear erosion phase (days 1 to 14), the residual dry mass percentage M_res follows pseudo-zero-order degradation kinetics: M_res(t) = -k_d · t + M_0, where k_d is the daily degradation rate constant (%/day) and M_0 is initial effective dry mass. In this experiment, fabricated porous hydrogel scaffolds incubated in sterile phosphate buffered saline (pH 7.40) at physiological 37.0 °C are evaluated gravimetrically to quantify degradation kinetics and scaffold stability.",
            "modelExtra": "Evaluated on cylindrical 3D porous PLGA-PEG composite hydrogel scaffolds (porosity 85%, diameter 8.0 mm, height 4.0 mm, initial dry mass 50.0 mg) incubated in 10 mL PBS (pH 7.4) at 37 °C under gentle shaking. Linear hydrolytic degradation rate k_d = 3.2000 %/day across days 2 to 12.",
            "apparatus": [
                {"name": "Thermostatically Controlled Orbital Shaker Incubator (37.0 °C)", "purpose": "Maintains physiological temperature and gentle agitation (50 RPM) simulating in-vivo fluid flow."},
                {"name": "Precision Analytical Balance (0.01 mg resolution)", "purpose": "Determines scaffold dry mass before and after degradation incubation intervals."},
                {"name": "Laboratory Freeze Dryer / Lyophilizer (-50 °C, 0.05 mbar)", "purpose": "Sublimates all absorbed water to measure true residual polymer dry mass without collapsing pores."},
                {"name": "Calibrated Digital Micro-pH Electrode", "purpose": "Monitors acidic lactic and glycolic acid by-product accumulation in the PBS incubation medium."},
                {"name": "Milli-Q Ultra-Pure Water Washing Station", "purpose": "Rinses soluble buffer salts from degraded scaffolds prior to freeze drying."},
                {"name": "Vacuum Desiccator with Silica Gel Indication", "purpose": "Prevents ambient moisture reabsorption during post-lyophilization mass determination."}
            ],
            "procedure": [
                {"title": "Scaffold Fabrication and Initial Dry Mass Baseline", "text": "Fabricate porous PLGA-PEG scaffolds via solvent casting/particulate leaching, lyophilize for 24 hours, and record initial dry mass W_0 (~50.00 mg) on analytical balance."},
                {"title": "Sterile Incubation Media Preparation", "text": "Prepare 10 mL sterile phosphate buffered saline (PBS, pH 7.40) aliquots in sealed centrifuge tubes and pre-warm to 37.0 °C in orbital incubator."},
                {"title": "Incubation and Dynamic Agitation", "text": "Submerge individual scaffolds into PBS tubes and incubate at 37.0 °C with continuous orbital shaking at 50 RPM."},
                {"title": "Periodic Destructive Sampling Harvest", "text": "At incubation intervals of 2, 4, 6, 8, 10, and 12 days, harvest duplicate scaffold specimens and record media pH to detect acidic buildup."},
                {"title": "Buffer Salt Rinsing and Lyophilization", "text": "Gently rinse harvested scaffolds three times in deionized water to remove crystallized buffer salts, freeze at -80 °C, and lyophilize for 48 hours to complete dryness."},
                {"title": "Residual Mass Kinetics Regression", "text": "Weigh residual dry mass W_t, calculate residual percentage M_res = (W_t / W_0) · 100%, plot M_res versus time t, and evaluate degradation rate k_d."}
            ],
            "topics": [
                {"question": "What is the difference between bulk erosion and surface erosion in biodegradable polymers?", "answer": "In bulk erosion (typical of hydrophilic PLGA and PEG hydrogels), water penetrates the entire matrix faster than ester bonds hydrolyze, causing uniform degradation throughout the scaffold; in surface erosion (polyanhydrides), hydrolytic cleavage is faster than water ingress, causing the scaffold to erode layer-by-layer from exterior to interior."},
                {"question": "Why does PLGA degradation sometimes cause autocatalysis?", "answer": "Hydrolysis of PLGA ester bonds releases lactic and glycolic acid oligomers. In thick scaffolds where diffusion is restricted, these acidic products accumulate internally, lowering local pH and accelerating the rate of acid-catalyzed ester hydrolysis."},
                {"question": "How does the lactic acid to glycolic acid ratio (L:G) affect PLGA degradation rate?", "answer": "Glycolic acid units are less hydrophobic and more amorphous than lactic acid units; therefore, PLGA 50:50 degrades significantly faster (1 to 2 months) than PLGA 85:15 (5 to 6 months) or pure poly-L-lactic acid (PLLA, > 1 year)."},
                {"question": "Why must harvested scaffolds be washed with deionized water before freeze drying?", "answer": "Phosphate buffered saline contains dissolved sodium chloride and phosphate salts. If not rinsed away, these salts precipitate during lyophilization, adding false mineral mass that leads to underestimation of polymer degradation."},
                {"question": "What is the clinical role of scaffold porosity in tissue regeneration?", "answer": "High interconnecting porosity (> 80%, pore size 100–300 μm) provides surface area for cellular infiltration, vascular neovascularization, nutrient diffusion, and waste clearance; insufficient porosity results in central tissue necrosis."},
                {"question": "How does scaffold degradation influence mechanical load transfer?", "answer": "As the scaffold degrades, its elastic modulus decreases; if coordinated with cellular deposition, nascent extracellular matrix progressively bears more physiological stress, stimulating functional tissue maturation."}
            ],
            "precautions": [
                "Change PBS incubation media weekly or when pH drops below 7.2 to avoid artificial accelerated autocatalytic degradation.",
                "Ensure thorough deionized water rinsing to completely eliminate buffer salt crystallization artifacts.",
                "Verify lyophilizer condenser operates below -45 °C and vacuum below 0.1 mbar to guarantee complete moisture sublimation.",
                "Handle delicate degraded scaffolds with silicone-tipped tweezers to prevent mechanical matrix fragmentation."
            ],
            "limitations": [
                "The linear zero-order degradation model applies to the initial mass loss phase (first 14 days); late-stage fragmentation exhibits non-linear mass loss.",
                "In-vitro PBS testing lacks physiological enzymes (lipases, esterases) that can accelerate degradation in vivo.",
                "Static tube incubation does not reproduce dynamic mechanical loading cycles experienced in weight-bearing joints.",
                "Assumes uniform degradation, whereas thick specimens may develop hollow acidic cores due to autocatalysis."
            ],
            "quiz": [
                {
                    "question": "What chemical bond is cleaved during the non-enzymatic hydrolytic degradation of PLGA scaffolds?",
                    "options": ["Ester bond", "Peptide bond", "Phosphodiester bond", "Disulfide bond"],
                    "correct": 0,
                    "explanation": "PLGA degrades via hydrolytic cleavage of ester bonds in its aliphatic polyester backbone, producing lactic and glycolic acid."
                },
                {
                    "question": "Why must buffer salts be rinsed from scaffolds prior to dry mass determination?",
                    "options": ["Crystallized salts precipitate and falsely increase dry mass", "Salts make the scaffold radioactive", "Salts dissolve the balance pan", "Salts attract insects"],
                    "correct": 0,
                    "explanation": "Dissolved buffer salts precipitate upon freeze drying; failing to wash them away adds artificial mass, underestimating true polymer degradation."
                },
                {
                    "question": "If residual mass is 91.6% at day 2 and 59.6% at day 12, what is the degradation rate constant k_d?",
                    "options": ["1.60 %/day", "3.20 %/day", "6.40 %/day", "9.80 %/day"],
                    "correct": 1,
                    "explanation": "k_d = -ΔM / Δt = -(59.6% - 91.6%) / (12 - 2) days = 32.0% / 10 days = 3.2000 %/day."
                },
                {
                    "question": "What phenomenon occurs when acidic degradation products accumulate within a thick biodegradable implant?",
                    "options": ["Autocatalytic accelerated degradation", "Spontaneous crystallization", "Polymer cross-linking", "Thermal runaway"],
                    "correct": 0,
                    "explanation": "Accumulation of acidic oligomers drops internal pH, catalyzing ester hydrolysis and accelerating degradation inside the core."
                }
            ],
            "settings": ["Polymer: Porous PLGA-PEG composite hydrogel (85% porosity)", "Medium: Sterile PBS (pH 7.40, 10 mL) with 0.02% sodium azide", "Incubation: 37.0 °C orbital shaker (50 RPM)"],
            "samples": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🧫", "label": "1. Hydrogel Incubator"},
                {"id": "compare", "icon": "📊", "label": "2. Residual Mass Kinetics"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Polymer Hydrolysis Sandbox"}
            ]
        },
        {
            "number": 23,
            "slug": "skeletal-muscle-isometric-length-tension-curve",
            "title": "Skeletal Muscle Isometric Active Length-Tension Characteristic",
            "shortTitle": "Muscle Length-Tension Curve",
            "aim": "Record isometric tetanic force in an isolated skeletal muscle preparation across normalized sarcomere lengths to evaluate the ascending active length-tension slope.",
            "inputLabel": "Normalized Muscle Length Ratio λ = L/L₀",
            "shortInput": "Length Ratio λ",
            "inputUnit": "ratio",
            "min": 0.70,
            "max": 0.95,
            "step": 0.05,
            "initial": 0.85,
            "inputDecimals": 2,
            "rawLabel": "Active Isometric Tetanic Force F_act",
            "rawUnit": "N",
            "rawDecimals": 4,
            "xAxis": "Normalized length ratio λ = L/L₀",
            "yAxis": "Active isometric force F_act (N)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 0.82,
            "emptyY": 3.5,
            "targetName": "Ascending Length-Tension Slope k_m",
            "target": "4.8000",
            "refValue": 4.8000,
            "resultUnit": "N/ratio",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "F_act = k_m · λ = 4.8000 · λ (ascending limb, L ≤ L₀)",
            "measureLabel": "Stimulate Muscle Tetanus",
            "intro": "In musculoskeletal biomechanics, motor control, and physiological modeling, skeletal muscle serves as the primary linear biological actuator driving joint movement and posture. The mechanical force generated by contracting muscle is governed by the sliding filament theory formulated by A.F. Huxley and H.E. Huxley. Skeletal muscle sarcomeres comprise interdigitating thick filaments (myosin) and thin filaments (actin). When activated by electrical action potentials, calcium release from the sarcoplasmic reticulum binds troponin-C, exposing actin binding sites and allowing myosin cross-bridge cycling. Under isometric (constant length) tetanic electrical stimulation, the active force F_act generated by the muscle depends strictly on sarcomere length. At optimal resting length L_0 (sarcomere length ~2.2 μm in mammals), cross-bridge overlap is maximal, yielding peak active tension F_0. In the ascending limb of the length-tension curve (where L < L_0, normalized stretch ratio λ = L/L_0 from 0.70 to 0.95), double overlap of opposing actin filaments and steric interference at the M-line progressively reduce the number of productive cross-bridges, causing active isometric force to scale linearly with sarcomere stretch: F_act = k_m · λ. In this laboratory experiment, an isolated amphibian or rodent gastrocnemius muscle mounted in an oxygenated Ringer's organ bath is subjected to supramaximal field stimulation to evaluate the ascending length-tension relationship and determine slope k_m.",
            "modelExtra": "Evaluated on isolated amphibian gastrocnemius muscle (optimal resting length L_0 = 30.0 mm, mass 0.50 g) stimulated at 100 Hz tetanic trains in oxygenated Ringer's solution at 22 °C. Linear ascending limb slope k_m = 4.8000 N/ratio across stretch ratios λ from 0.70 to 0.95.",
            "apparatus": [
                {"name": "Isometric Muscle Physiology Organ Chamber", "purpose": "Maintains isolated muscle bathed in oxygenated (95% O₂, 5% CO₂) physiological Ringer's solution."},
                {"name": "High-Resonance Isometric Force Transducer (0–10 N)", "purpose": "Measures muscle contractile force with sub-millisecond response and negligible compliance."},
                {"name": "Micrometer Translation Stage (10 μm precision)", "purpose": "Sets precise muscle length increments and measures absolute muscle extension L."},
                {"name": "Isolated High-Current Electrical Stimulator", "purpose": "Delivers supramaximal square-wave pulses (0.5 ms, 50 V) and tetanic trains (100 Hz, 500 ms)."},
                {"name": "Parallel Platinum Field Stimulation Electrodes", "purpose": "Provides uniform electric field across entire muscle belly ensuring synchronous fiber activation."},
                {"name": "Dual-Channel Oscilloscope & High-Speed Data Acquisition", "purpose": "Digitizes stimulus pulses and tension waveforms at 10 kHz with active baseline subtraction."}
            ],
            "procedure": [
                {"title": "Muscle Dissection and Organ Bath Mounting", "text": "Dissect gastrocnemius muscle with intact Achilles tendon, mount proximal bone clamp in bath, and tie Achilles tendon rigidly to force transducer with braided silk suture."},
                {"title": "Optimal Length L_0 Determination", "text": "Deliver single twitch pulses while adjusting micrometer stage until maximum twitch force is identified, defining optimal resting length L_0."},
                {"title": "Passive Force Baseline Subtraction", "text": "At each length step, record baseline resting tension (passive force F_pass) prior to electrical stimulation."},
                {"title": "Tetanic Electrical Stimulation", "text": "Deliver a 100 Hz, 500 ms train of supramaximal square-wave pulses (25 V, 1 ms pulse width) and record total peak isometric force F_tot."},
                {"title": "Active Force Computation across Ascending Limb", "text": "Calculate active force F_act = F_tot - F_pass across normalized length ratios λ = L/L_0 of 0.70, 0.75, 0.80, 0.85, 0.90, and 0.95, allowing 2 minutes rest between tetani."},
                {"title": "Ascending Slope Linear Regression", "text": "Plot active isometric force F_act versus length ratio λ and calculate ascending slope k_m via linear regression."}
            ],
            "topics": [
                {"question": "What is the molecular basis of the active length-tension curve in skeletal muscle?", "answer": "The active length-tension curve directly mirrors the physical degree of overlap between myosin cross-bridge heads on thick filaments and actin binding sites on thin filaments within individual sarcomeres."},
                {"question": "Why does active tension decrease when muscle is shortened below optimal length L_0?", "answer": "At lengths below L_0 (ascending limb), actin filaments from opposite ends of the sarcomere overlap in the central H-zone, interfering with cross-bridge attachment; at extreme shortening, thick filaments collide with Z-discs, physically resisting shortening."},
                {"question": "What is the difference between isometric, concentric, and eccentric contractions?", "answer": "In an isometric contraction, muscle length remains fixed as tension develops; in concentric contraction, muscle actively shortens while doing external work; in eccentric contraction, active muscle is lengthened by an external load, generating forces up to 1.5–2 times peak isometric tension."},
                {"question": "Why is active force calculated by subtracting passive force from total force?", "answer": "When muscle is stretched, passive elastic structures (primarily the giant intra-sarcomeric protein titin and extracellular collagenous perimysium) develop passive recoil tension F_pass; active contractile force F_act generated by actomyosin cross-bridges equals total force minus passive force."},
                {"question": "What is the physiological role of the protein titin in muscle biomechanics?", "answer": "Titin is a massive molecular spring that spans from the Z-disc to the M-line, maintaining central myosin alignment, restoring sarcomere resting length after contraction, and generating the majority of passive resting tension at long lengths."},
                {"question": "Why must adequate rest intervals (1 to 2 minutes) be provided between tetanic contractions?", "answer": "Repeated high-frequency stimulation depletes intracellular phosphocreatine and glycogen, accumulates lactic acid and inorganic phosphate (P_i), and impairs sarcoplasmic reticulum Ca²⁺ release, inducing metabolic muscle fatigue that skews length-tension data."}
            ],
            "precautions": [
                "Continuous 95% O₂ / 5% CO₂ gas bubbling is mandatory to maintain muscle oxygenation and physiological bath pH (7.40).",
                "Use non-compliant braided surgical silk or steel wire for transducer ties; compliant suture introduces pseudo-isotonic shortening artifacts.",
                "Verify supramaximal stimulation voltage by confirming that a 20% voltage increase produces no additional force gain.",
                "Enforce a strict 2-minute recovery pause between tetanic trains to avoid contraction-induced metabolic fatigue."
            ],
            "limitations": [
                "The linear model applies strictly to the ascending limb (λ ≤ 0.95); the plateau and descending limbs require piece-wise non-linear modeling.",
                "Assumes uniform sarcomere length throughout all muscle fibers, whereas in-vivo pennate muscles exhibit non-uniform strain distributions.",
                "Isometric conditions do not model force-velocity (Hill's hyperbolic curve) dynamics during active joint movement.",
                "In-vitro amphibian muscle tested at 22 °C exhibits slower cross-bridge kinetics than mammalian muscle at 37 °C."
            ],
            "quiz": [
                {
                    "question": "What molecular mechanism is responsible for active force generation in skeletal muscle?",
                    "options": ["Myosin cross-bridge head binding to actin filaments and power-stroking", "Osmotic swelling of mitochondria", "Collagen fibers twisting", "Sodium ions pushing Z-discs"],
                    "correct": 0,
                    "explanation": "Active force is generated by the cyclic attachment, power stroke, and detachment of myosin heads on actin filaments driven by ATP hydrolysis."
                },
                {
                    "question": "What happens to cross-bridge overlap on the ascending limb of the length-tension curve (L < L_0)?",
                    "options": ["Overlap is optimal", "Thin actin filaments double-overlap and interfere in the H-zone, reducing active force", "Thick filaments pull completely apart", "Titin snaps"],
                    "correct": 1,
                    "explanation": "Below optimal length L_0, overlapping actin filaments cause steric hindrance and cross-bridge interference, reducing active tension."
                },
                {
                    "question": "If active isometric force is 3.840 N at a length ratio λ = 0.80, what is the ascending slope k_m?",
                    "options": ["2.400 N/ratio", "4.800 N/ratio", "9.600 N/ratio", "12.00 N/ratio"],
                    "correct": 1,
                    "explanation": "k_m = F_act / λ = 3.840 N / 0.80 = 4.8000 N/ratio."
                },
                {
                    "question": "Which giant structural protein acts as an elastic spring responsible for passive muscle tension?",
                    "options": ["Titin", "Myoglobin", "Dystrophin", "Tropomyosin"],
                    "correct": 0,
                    "explanation": "Titin is the enormous molecular spring anchoring myosin thick filaments to the Z-disc, providing passive elasticity."
                }
            ],
            "settings": ["Preparation: Isolated gastrocnemius muscle (L_0 = 30.0 mm)", "Stimulation: Supramaximal tetanic trains (100 Hz, 500 ms duration)", "Organ bath: Oxygenated Ringer's solution (95% O₂, 5% CO₂) at 22 °C"],
            "samples": [0.70, 0.75, 0.80, 0.85, 0.90, 0.95],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "💪", "label": "1. Muscle Organ Bath"},
                {"id": "compare", "icon": "📊", "label": "2. Active Length-Tension"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Sarcomere Overlap Sandbox"}
            ]
        },
        {
            "number": 24,
            "slug": "ligament-viscoelastic-stress-relaxation-fung",
            "title": "Viscoelastic Ligament Stress Relaxation & Reduced Relaxation Function",
            "shortTitle": "Ligament Viscoelastic Relaxation",
            "aim": "Determine the continuous relaxation spectrum parameter c_r of an anterior cruciate ligament (ACL) specimen under tensile stress relaxation using Fung's quasi-linear viscoelastic (QLV) theory.",
            "inputLabel": "Relaxation Time t",
            "shortInput": "Time t",
            "inputUnit": "s",
            "min": 5.0,
            "max": 300.0,
            "step": 50.0,
            "initial": 30.0,
            "inputDecimals": 1,
            "rawLabel": "Normalized Stress σ(t)/σ₀",
            "rawUnit": "ratio",
            "rawDecimals": 4,
            "xAxis": "Log relaxation time ln(t) [ln(s)]",
            "yAxis": "Normalized stress σ(t)/σ₀ (ratio)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.5,
            "emptyY": 0.82,
            "targetName": "Fung Relaxation Spectrum Parameter c_r",
            "target": "0.0450",
            "refValue": 0.0450,
            "resultUnit": "ratio/ln(s)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "σ(t)/σ₀ = -c_r · ln(t) + G_0 = -0.0450 · ln(t) + 0.9800",
            "measureLabel": "Record Stress Relaxation",
            "intro": "Ligaments and tendons are dense fibrous connective tissues that mechanically guide joint kinematics, stabilize articulating bones, and prevent abnormal joint subluxation (such as anterior tibial translation resisted by the anterior cruciate ligament, ACL). Structurally composed of hierarchically crimped type-I collagen fibers embedded in a proteoglycan-rich ground substance, biological soft tissues exhibit pronounced time- and history-dependent viscoelastic behaviors, including hysteresis, creep, preconditioning, and stress relaxation. Under a rapid step-strain held constant over time (ε = ε_0 for t > 0), the tensile stress σ(t) peaks immediately upon stretching and then decays asymptotically as internal viscous fluid flow, proteoglycan shearing, and collagen fibril sliding dissipate energy. To mathematically describe this non-linear viscoelasticity, Y.C. Fung formulated the Quasi-Linear Viscoelastic (QLV) theory. In Fung's QLV framework, the reduced relaxation function G(t) = σ(t) / σ_0 characterizes the time-dependent relaxation behavior independently of the non-linear elastic response: G(t) = [1 - c_r · ln(t / τ_1)] / [1 + c_r · ln(τ_2 / τ_1)]. Over intermediate physiological time scales (where τ_1 ≪ t ≪ τ_2, typically 5 s to 300 s), G(t) is linear with respect to the natural logarithm of time: σ(t)/σ_0 = -c_r · ln(t) + G_0, where c_r is the continuous relaxation spectrum parameter. In this laboratory investigation, bone-patellar tendon-bone or ACL specimens tested in a 37.0 °C saline bio-chamber evaluate tensile stress relaxation to determine Fung's parameter c_r.",
            "modelExtra": "Evaluated on porcine bone-ACL-bone complexes mounted in anatomical tensile grips in 37.0 °C saline. Subjected to a rapid ramp-and-hold tensile strain (ε_0 = 0.05 applied in 0.1 s) and held for 300 s. Semi-logarithmic slope c_r = 0.0450 ratio/ln(s) evaluated across times from 5 s to 300 s.",
            "apparatus": [
                {"name": "High-Speed Dynamic Biomechanical Test Frame", "purpose": "Applies rapid ramp-and-hold displacement (rise time < 100 ms) with closed-loop servohydraulic control."},
                {"name": "Anatomical Bone-Block Clamping Fixtures", "purpose": "Rigidly grips femoral and tibial bone blocks preserving natural anatomical ligament insertion angles."},
                {"name": "High-Frequency Piezoelectric Load Cell (0–2 kN)", "purpose": "Captures instantaneous peak tensile force and subtle millinewton relaxation decay without drift."},
                {"name": "Submerged Physiological Bio-Chamber (37.0 °C)", "purpose": "Maintains ligament in continuous 37 °C phosphate buffered saline preventing tissue desiccation."},
                {"name": "Non-Contact Video Tracking Extensometer", "purpose": "Verifies that grip displacement holds mid-substance ligament strain strictly constant during relaxation."},
                {"name": "High-Speed Synchronous Data Acquisition System", "purpose": "Logs time and force channels at 1 kHz during ramp and logarithmically decimate during 300 s hold."}
            ],
            "procedure": [
                {"title": "Specimen Dissection and Anatomical Mounting", "text": "Dissect knee joint leaving intact femur-ACL-tibia complex, pot bone blocks in polymethylmethacrylate (PMMA) cylinders, and clamp in aligned tensile fixtures."},
                {"title": "Saline Bio-Chamber Equilibration", "text": "Submerge the mounted ligament complex in 37.0 °C PBS bath and allow 20 minutes for thermal and osmotic equilibration."},
                {"title": "Preconditioning Cyclic Protocol", "text": "Apply 10 cycles of triangular preconditioning from 0 to 2% strain at 0.5 Hz to achieve repeatable, steady-state viscoelastic cycling."},
                {"title": "Ramp-and-Hold Step Strain Execution", "text": "Apply a rapid tensile displacement step to 5% mid-substance strain within 100 ms, triggering high-speed data acquisition at peak load σ_0."},
                {"title": "Isometric Relaxation Data Collection", "text": "Hold displacement strictly constant for 300 seconds, logging decaying load at standardized intervals: 5, 15, 30, 60, 120, and 300 seconds."},
                {"title": "Fung QLV Semi-Logarithmic Regression", "text": "Normalize stress σ(t)/σ_0, plot against natural logarithm of time ln(t), and extract Fung's relaxation spectrum parameter c_r from the linear slope."}
            ],
            "topics": [
                {"question": "What is the physical interpretation of Fung's parameter c_r?", "answer": "Fung's parameter c_r quantifies the intensity of the continuous relaxation spectrum of the tissue; higher c_r values indicate greater viscous energy dissipation, faster stress relaxation, and more pronounced viscoelastic damping."},
                {"question": "Why does stress relax in a ligament held at constant strain?", "answer": "At constant elongation, water and mobile proteoglycans flow through the collagen fibrillar network, and crimped collagen fibrils undergo microscopic molecular realignment and sliding, dissipating internal strain energy into heat."},
                {"question": "What is the purpose of mechanical preconditioning in soft tissue testing?", "answer": "Unpreconditioned soft tissues exhibit progressive shifting of stress-strain loops due to internal fluid redistribution; cyclically loading 10 to 20 times establishes an internal fluid equilibrium that yields highly repeatable mechanical measurements."},
                {"question": "What are the lower and upper relaxation time limits τ_1 and τ_2 in Fung's QLV theory?", "answer": "τ_1 represents the fast molecular relaxation process of collagen fibrils (milliseconds), while τ_2 represents the slow macroscopic fluid exudation and ground-substance relaxation (hundreds of seconds)."},
                {"question": "How does chemical cross-linking (e.g., glutaraldehyde) affect ligament viscoelasticity?", "answer": "Exogenous cross-linking introduces rigid chemical bonds between collagen molecules, restricting inter-fibrillar sliding and fluid exudation, which significantly decreases c_r and reduces viscoelastic stress relaxation."},
                {"question": "Why is the ramp phase rise time critical in stress relaxation experiments?", "answer": "If the ramp is too slow, significant relaxation occurs during the loading phase before peak strain is reached, violating the mathematical assumption of an instantaneous Heaviside step strain and introducing substantial errors in G(t)."}
            ],
            "precautions": [
                "The rise time of the loading ramp must be under 100 ms to minimize relaxation occurring prior to peak strain.",
                "Verify that mid-substance ligament strain is tracked optically; grip compliance can cause mid-substance strain to creep even when crosshead is held fixed.",
                "Ensure bone blocks are potted rigidly in PMMA to avoid micro-motion at the clamping boundary.",
                "Maintain continuous 37 °C saline immersion; surface drying dramatically alters ligament relaxation kinetics."
            ],
            "limitations": [
                "The linear semi-logarithmic relation applies over the intermediate time window (τ_1 ≪ t ≪ τ_2); it deviates at very short (< 1 s) and very long (> 10⁴ s) times.",
                "Fung's QLV theory assumes time-dependence and strain-dependence are fully separable: σ(ε, t) = G(t) * σ_e(ε), which is an approximation.",
                "Does not account for non-uniform fiber recruitments across the anteromedial and posterolateral bundles of the native ACL.",
                "Assumes 1D uniaxial tension, neglecting complex in-vivo multi-axial twisting and shear kinematics."
            ],
            "quiz": [
                {
                    "question": "What happens to tensile stress in a ligament held at a constant stretched length over time?",
                    "options": ["Stress decays asymptotically over time due to viscoelastic energy dissipation", "Stress increases indefinitely until it breaks", "Stress oscillates like a sine wave", "Stress instantly drops to zero"],
                    "correct": 0,
                    "explanation": "At constant strain, viscous fluid flow and fibril realignment dissipate energy, causing stress to relax asymptotically over time."
                },
                {
                    "question": "In Fung's Quasi-Linear Viscoelastic theory, what does the parameter c_r represent?",
                    "options": ["The continuous relaxation spectrum intensity", "The speed of sound in ligament", "The melting point of collagen", "The atomic weight of calcium"],
                    "correct": 0,
                    "explanation": "Parameter c_r governs the amplitude of the continuous relaxation spectrum, determining the rate of stress relaxation per log-decade of time."
                },
                {
                    "question": "If normalized stress is 0.9076 at t = 5 s (ln(5) = 1.609) and 0.7233 at t = 300 s (ln(300) = 5.704), what is c_r?",
                    "options": ["0.0225 ratio/ln(s)", "0.0450 ratio/ln(s)", "0.0900 ratio/ln(s)", "0.1800 ratio/ln(s)"],
                    "correct": 1,
                    "explanation": "c_r = -Δ[σ/σ_0] / Δ[ln(t)] = -(0.7233 - 0.9076) / (5.704 - 1.609) = 0.1843 / 4.095 = 0.0450 ratio/ln(s)."
                },
                {
                    "question": "Why must soft tissue specimens undergo cyclic preconditioning before mechanical testing?",
                    "options": ["To reach a repeatable, stable viscoelastic equilibrium state", "To soften the bone grips", "To kill bacteria", "To warm up the motor"],
                    "correct": 0,
                    "explanation": "Cyclic preconditioning redistributes fluid and aligns collagen fibrils, yielding stable and reproducible stress-strain and relaxation loops."
                }
            ],
            "settings": ["Specimen: Porcine bone-ACL-bone complex", "Preconditioning: 10 cycles (0 to 2% strain at 0.5 Hz)", "Step strain: ε_0 = 0.05 applied in 100 ms, held for 300 s at 37.0 °C"],
            "samples": [5.0, 15.0, 30.0, 60.0, 120.0, 300.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🦵", "label": "1. ACL Relaxation Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Stress Relaxation Curve"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Fung QLV Sandbox"}
            ]
        },
        {
            "number": 25,
            "slug": "gait-analysis-force-plate-ground-reaction-forces",
            "title": "Instrumented Gait Analysis Force Plate Ground Reaction Force & Velocity Scaling",
            "shortTitle": "Gait Analysis Ground Reaction Force",
            "aim": "Measure multi-axis ground reaction forces (GRF) using an instrumented piezoelectric force plate and evaluate the linear velocity scaling of the peak vertical force F_v/BW.",
            "inputLabel": "Forward Walking Velocity v_w",
            "shortInput": "Velocity v_w",
            "inputUnit": "m/s",
            "min": 0.80,
            "max": 1.80,
            "step": 0.20,
            "initial": 1.20,
            "inputDecimals": 2,
            "rawLabel": "Normalized Peak Vertical GRF F_v/BW",
            "rawUnit": "BW",
            "rawDecimals": 4,
            "xAxis": "Forward walking velocity v_w (m/s)",
            "yAxis": "Normalized peak vertical GRF F_v/BW (BW)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 1.30,
            "emptyY": 1.15,
            "targetName": "Vertical GRF Velocity Scaling Factor k_v",
            "target": "0.2800",
            "refValue": 0.2800,
            "resultUnit": "BW/(m/s)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "F_v/BW = k_v · v_w + F_v0 = 0.2800 · v_w + 0.8200",
            "measureLabel": "Capture Gait Force Plate Trial",
            "intro": "Instrumented human gait analysis provides objective, quantitative biomechanical data essential for diagnosing cerebral palsy crouch gait, evaluating total knee arthroplasty functional recovery, optimizing prosthetic foot design, and assessing athletic performance. When a human walks across a floor, the foot exerts forces against the ground, and by Newton's third law, the ground exerts an equal and opposite Ground Reaction Force (GRF) vector back upon the body. In a gait laboratory, flush-mounted multi-axis force plates equipped with triaxial piezoelectric quartz or strain gauge load cells measure three orthogonal force components: vertical (F_z), anteroposterior braking/propulsion (F_y), and mediolateral (F_x), as well as center of pressure (COP) coordinates. During the stance phase of walking, the vertical GRF displays a characteristic bimodal 'M-shape' profile: an initial peak corresponding to heel strike and weight acceptance, a mid-stance trough during contralateral swing phase, and a second peak during terminal stance push-off. As walking velocity v_w increases, greater downward momentum and leg acceleration elevate the peak vertical ground reaction force. When normalized to subject body weight (BW = m·g), empirical biomechanical data demonstrate that peak vertical GRF F_v/BW scales linearly with walking velocity: F_v/BW = k_v · v_w + F_v0, where k_v is the velocity sensitivity scaling factor (BW/(m/s)). In this laboratory investigation, an instrumented walkway tracks force plate telemetry across controlled walking speeds to quantify vertical force scaling.",
            "modelExtra": "Evaluated on healthy adult human subjects (body mass 70.0 kg, BW = 686.7 N) walking across an instrumented Bertec multi-component piezoelectric force platform (600 mm × 400 mm). Walking velocities from 0.80 to 1.80 m/s tracked via optical timing gates. Linear velocity scaling k_v = 0.2800 BW/(m/s).",
            "apparatus": [
                {"name": "Multi-Component Piezoelectric Force Platform", "purpose": "Measures triaxial forces (Fx, Fy, Fz) and moments (Mx, My, Mz) with 0.1 N resolution and 1000 Hz bandwidth."},
                {"name": "Instrumented 10-Meter Gait Walkway", "purpose": "Provides seamless, flush-mounted level walking surface preventing targeting artifacts."},
                {"name": "Dual Infrared Optical Timing Gates", "purpose": "Accurately measures average walking speed v_w over the middle 3-meter capture zone."},
                {"name": "Multichannel Charge Amplifier & Signal Conditioner", "purpose": "Converts piezoelectric charge outputs into calibrated analog voltage signals with high drift stability."},
                {"name": "Synchronous 16-Bit Data Acquisition Telemetry Console", "purpose": "Digitizes 6-channel force plate signals at 1000 Hz with digital Butterworth low-pass filtering (cutoff 20 Hz)."},
                {"name": "Body Mass Precision Calibration Scale", "purpose": "Determines subject static body weight (BW) to ±0.1 N prior to gait testing."}
            ],
            "procedure": [
                {"title": "Subject Anthropometry and Zero Tare Calibration", "text": "Measure subject body mass on calibrated digital scale, compute static body weight BW = m·g, and zero the force plate charge amplifier."},
                {"title": "Optical Timing Gate Alignment", "text": "Position infrared timing gates 3.0 meters apart centered around the flush-mounted force platform and calibrate electronic timer."},
                {"title": "Familiarization and Baseline Stride Setup", "text": "Allow subject several practice walking passes to establish natural stride length and ensure clean, un-targeted foot strikes onto the platform."},
                {"title": "Controlled Velocity Gait Capture", "text": "Guide subject to walk at a standardized slow velocity (v_w = 0.80 m/s), verified by timing gate readout, and record 1000 Hz triaxial GRF telemetry."},
                {"title": "Velocity Progression Sequence", "text": "Repeat clean foot strike trials across walking speeds of 1.00, 1.20, 1.40, 1.60, and 1.80 m/s, capturing three valid trials per speed step."},
                {"title": "Peak Vertical Force Normalization and Regression", "text": "Extract peak weight-acceptance vertical force F_v, normalize to body weight (F_v/BW), plot versus velocity v_w, and calculate scaling factor k_v."}
            ],
            "topics": [
                {"question": "What is the biomechanical cause of the bimodal 'M-shape' vertical GRF curve in walking?", "answer": "The first peak reflects downward deceleration of the body center of mass during heel strike and weight acceptance; the central dip corresponds to upward center-of-mass elevation during mid-stance vaulting; and the second peak reflects active ankle plantarflexion push-off."},
                {"question": "Why must force plate data be normalized to body weight (BW)?", "answer": "Absolute ground reaction forces scale directly with individual body mass; dividing forces by body weight (BW = m·g) yields dimensionless metrics that enable objective comparison across pediatric, adult, and prosthetic patient populations."},
                {"question": "What is 'targeting' and why does it invalidate gait analysis data?", "answer": "Targeting occurs when a subject visually notices the force plate and artificially alters their natural stride length, cadence, or foot placement to hit the platform, creating unphysiological kinematic and kinetic artifacts."},
                {"question": "What do the anteroposterior (F_y) forces represent during the stance phase?", "answer": "During the first half of stance, the foot pushes forward against the plate, creating a negative braking force that decelerates the body; during the second half, the foot pushes backward, generating a positive propulsion force that accelerates the body forward."},
                {"question": "How does Center of Pressure (COP) inform postural stability and joint moment calculation?", "answer": "COP represents the spatial centroid of all contact pressures beneath the foot sole; combining COP coordinates with the 3D GRF vector allows inverse dynamics calculations of ankle, knee, and hip net muscle moments."},
                {"question": "How does running GRF differ from walking GRF?", "answer": "Running has no double-support phase and exhibits a unimodal vertical GRF profile with a rapid heel-impact transient spike followed by a massive active peak reaching 2.5 to 3.0 times body weight."}
            ],
            "precautions": [
                "Ensure force platform is mounted flush and mechanically isolated from the surrounding walkway floor to avoid foot impact vibrations.",
                "Discard any trial where the foot partially misses the plate or where visible step-targeting occurs.",
                "Filter raw 1000 Hz force data with a low-pass zero-lag 4th-order Butterworth filter (cutoff 20 Hz) to eliminate high-frequency plate resonance.",
                "Verify timing gate alignment and ensure subjects do not accelerate or decelerate within the 3-meter capture zone."
            ],
            "limitations": [
                "The linear velocity model applies across normal walking speeds (0.8 to 1.8 m/s); running involves a discrete gait transition with different mechanics.",
                "Assumes level overground walking, neglecting inclines, stair ambulation, or uneven outdoor terrain.",
                "Force plates capture external kinetics only; calculating internal joint forces requires inverse dynamics with optical motion capture.",
                "Subject footwear (athletic shoes vs. barefoot) alters impact transient magnitude and foot contact mechanics."
            ],
            "quiz": [
                {
                    "question": "What shape does the vertical ground reaction force (F_z) exhibit during normal walking?",
                    "options": ["A bimodal 'M-shape' with two peaks and a mid-stance trough", "A flat horizontal line", "A single triangular spike", "A decaying exponential"],
                    "correct": 0,
                    "explanation": "Normal walking exhibits a classic bimodal M-shaped vertical GRF: the first peak is weight acceptance, followed by a mid-stance dip and push-off peak."
                },
                {
                    "question": "Why are ground reaction forces normalized to body weight (BW) in clinical gait analysis?",
                    "options": ["To allow objective comparisons across individuals of different masses", "To convert kilograms into meters", "Because force plates only read percentages", "To eliminate the need for calibration"],
                    "correct": 0,
                    "explanation": "Normalizing by body weight (BW = m·g) removes mass dependency, allowing clinical comparison between patients."
                },
                {
                    "question": "If walking velocity is 1.40 m/s and peak vertical force is 1.2120 BW, what is the scaling factor k_v (with F_v0 = 0.8200 BW)?",
                    "options": ["0.1400 BW/(m/s)", "0.2800 BW/(m/s)", "0.5600 BW/(m/s)", "0.8200 BW/(m/s)"],
                    "correct": 1,
                    "explanation": "k_v = (F_v/BW - F_v0) / v_w = (1.2120 - 0.8200) / 1.40 = 0.3920 / 1.40 = 0.2800 BW/(m/s)."
                },
                {
                    "question": "What is the primary error introduced when a patient 'targets' the force plate?",
                    "options": ["The patient artificially alters stride length and cadence, producing unrepresentative kinetics", "The force plate battery overheats", "The room lighting flickers", "The computer crashes"],
                    "correct": 0,
                    "explanation": "Step-targeting alters natural gait kinematics and stride parameters, rendering recorded force telemetry invalid."
                }
            ],
            "settings": ["Platform: Bertec piezoelectric multi-component plate (600 mm × 400 mm)", "Subject: Healthy adult (m = 70.0 kg, BW = 686.7 N)", "Sampling: 1000 Hz with 20 Hz low-pass digital filter"],
            "samples": [0.80, 1.00, 1.20, 1.40, 1.60, 1.80],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🚶", "label": "1. Force Plate Walkway"},
                {"id": "compare", "icon": "📊", "label": "2. Peak GRF vs Velocity"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Gait Dynamics Sandbox"}
            ]
        },
        {
            "number": 26,
            "slug": "prosthetic-socket-interface-pressure-mapping",
            "title": "Transtibial Prosthetic Socket Patellar-Tendon Interface Pressure Mapping",
            "shortTitle": "Prosthetic Socket Interface Pressure",
            "aim": "Map the interface contact pressure at the patellar-tendon bar of a patellar-tendon-bearing (PTB) prosthetic socket as a function of axial limb weight-bearing load.",
            "inputLabel": "Applied Axial Limb Load W",
            "shortInput": "Axial Load W",
            "inputUnit": "N",
            "min": 200.0,
            "max": 700.0,
            "step": 100.0,
            "initial": 400.0,
            "inputDecimals": 1,
            "rawLabel": "Patellar-Tendon Interface Pressure P_ptb",
            "rawUnit": "kPa",
            "rawDecimals": 3,
            "xAxis": "Axial limb load W (N)",
            "yAxis": "Patellar tendon interface pressure P_ptb (kPa)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 450.0,
            "emptyY": 100.0,
            "targetName": "Socket Load Sensitivity Constant k_soc",
            "target": "0.2200",
            "refValue": 0.2200,
            "resultUnit": "kPa/N",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "P_ptb = k_soc · W = 0.2200 · W",
            "measureLabel": "Record Socket Interface Pressure",
            "intro": "In lower-limb prosthetics, the mechanical interface between the amputee's residual limb (stump) and the rigid prosthetic socket is the single most critical determinant of clinical comfort, skin integrity, prosthetic control, and successful ambulation. In transtibial (below-knee) amputees, the traditional Patellar-Tendon-Bearing (PTB) socket design intentionally distributes weight-bearing loads onto pressure-tolerant anatomical areas (primarily the patellar tendon, medial tibial flare, and pretibial muscle bulk) while providing relief pockets over pressure-sensitive bony prominences (fibular head, distal tibia crest, and hamstring tendons). To prevent tissue ischemia, skin breakdown, and deep ulceration, interface contact pressures must be rigorously monitored. Sustained pressures exceeding capillary closing pressure (~4.0 kPa or 30 mmHg) cut off capillary microcirculation, leading to tissue hypoxia and pressure necrosis if prolonged. Thin-film piezoresistive sensor arrays (such as Tekscan F-Socket or capacitive sensor matrices) placed inside the socket interface measure dynamic pressure distributions with millimeter spatial resolution. Under quasi-static axial loading, the normal contact pressure P_ptb concentrated over the patellar tendon bar scales linearly with total axial weight-bearing load W: P_ptb = k_soc · W, where k_soc is the socket load transfer coefficient (kPa/N). In this laboratory investigation, an instrumented robotic residual limb model fitted with a custom PTB socket evaluates interface pressure mapping across physiological axial loads.",
            "modelExtra": "Evaluated on an anatomically contoured robotic residual limb mannequin with silicone soft tissue surrogate (Shore 20A durometer) fitted inside a carbon-fiber PTB prosthetic socket. Instrumented with calibrated thin-film piezoresistive pressure sensors at the patellar-tendon bar. Linear sensitivity k_soc = 0.2200 kPa/N across loads from 200 N to 700 N.",
            "apparatus": [
                {"name": "Anatomical Transtibial Residual Limb Mannequin", "purpose": "Provides rigid skeletal core (tibia/fibula) surrounded by elastomeric soft-tissue simulating muscle and skin."},
                {"name": "Carbon-Fiber Patellar-Tendon-Bearing Prosthetic Socket", "purpose": "Custom-laminated below-knee socket with inward patellar-tendon weight-bearing indentation bar."},
                {"name": "Thin-Film Piezoresistive Pressure Sensor Array (Tekscan F-Socket)", "purpose": "Matrix of flexible sensors (thickness 0.15 mm) measuring local interface pressure up to 250 kPa."},
                {"name": "Servohydraulic Biomechanical Axial Loading Ram", "purpose": "Applies controlled vertical limb loads W from 200 N to 700 N with closed-loop force control."},
                {"name": "Multichannel Piezoresistive Digital Interfacing Hub", "purpose": "Scans 96 pressure matrix sensing cells at 100 Hz with 8-bit gray-scale spatial mapping."},
                {"name": "Pneumatic Pressure Sensor Calibration Bladder", "purpose": "Applies uniform hydrostatic pressure steps to calibrate piezoresistive array prior to limb insertion."}
            ],
            "procedure": [
                {"title": "Sensor Matrix Equi-Pressure Calibration", "text": "Place thin-film sensor array inside pneumatic bladder calibration chamber and apply 50, 100, and 150 kPa pressures to generate cell-by-cell calibration lookup tables."},
                {"title": "Sensor Placement along Patellar-Tendon Bar", "text": "Affix calibrated sensor matrix securely along the patellar-tendon bar and medial tibial flare of the residual limb mannequin using skin-safe adhesive film."},
                {"title": "Prosthetic Socket Donning and Alignment", "text": "Carefully don a 6 mm silicone gel prosthetic liner and seat the residual limb into the carbon-fiber PTB socket, verifying anatomical alignment."},
                {"title": "Axial Load Initialization and Seating Tare", "text": "Position the prosthetic assembly under the vertical loading ram and apply a 50 N tare load to bed down the elastomeric liner."},
                {"title": "Stepwise Axial Weight-Bearing Progression", "text": "Increment axial vertical load through 200, 300, 400, 500, 600, and 700 N, recording stabilized mean patellar-tendon contact pressure P_ptb at each step."},
                {"title": "Load Sensitivity Regression Analysis", "text": "Plot patellar-tendon interface pressure P_ptb against total axial load W and compute the socket load transfer constant k_soc via linear regression."}
            ],
            "topics": [
                {"question": "What is the biomechanical rationale behind the Patellar-Tendon-Bearing (PTB) socket concept?", "answer": "The PTB concept concentrates weight-bearing forces onto tough, fibrous, pressure-tolerant tissues (the patellar tendon and broad medial tibial flare) while hollowing relief depressions over fragile bony prominences to avoid skin breakdown."},
                {"question": "What happens physiologically when interface pressure exceeds capillary closing pressure?", "answer": "Normal capillary closing pressure is approximately 30 to 32 mmHg (~4.0 to 4.3 kPa). Pressures significantly exceeding this threshold collapse microvascular arterioles and capillaries, occluding blood flow and leading to local tissue ischemia, edema, and skin necrosis if sustained."},
                {"question": "How do modern Total Surface Bearing (TSB) sockets differ from classic PTB sockets?", "answer": "TSB sockets distribute weight-bearing loads uniformly across the entire surface area of the residual limb utilizing elastomeric silicone or polyurethane liners and vacuum suspension, significantly reducing localized peak pressures compared to PTB sockets."},
                {"question": "Why are thin-film piezoresistive sensors preferred for socket interface pressure measurement?", "answer": "Thin-film sensors are extremely thin (< 0.2 mm) and flexible, allowing them to conform to complex socket curvatures without adding noticeable thickness that would distort natural limb fit or create artificial high-pressure ridges."},
                {"question": "What are sensor curvature and shear artifacts in prosthetic socket measurements?", "answer": "Piezoresistive sensors can register false resistance changes when subjected to out-of-plane bending or in-plane shear forces; proper calibration against known hydrostatic pressures and using low-friction sensor backings minimize these artifacts."},
                {"question": "Why does interface pressure fluctuate dramatically during dynamic walking?", "answer": "During walking, the socket acts as a lever arm resisting knee flexion and extension moments; during early stance, the patellar tendon experiences high pressure to resist knee buckling, while during late stance, pressure shifts to the posterior proximal brim."}
            ],
            "precautions": [
                "Ensure thin-film sensor array is wrinkle-free when donning the socket; sensor creasing creates permanent electrical short circuits.",
                "Calibrate the piezoresistive array using an equi-pressure pneumatic bladder immediately prior to testing to account for sensor temperature drift.",
                "Ensure the loading ram applies purely vertical axial force without introducing unintended off-axis bending moments.",
                "Check for sensor saturation; ensure applied pressures do not exceed the calibrated 250 kPa upper linear limit."
            ],
            "limitations": [
                "The linear sensitivity model applies to static axial loading; dynamic ambulation introduces coupled shear stresses and moment loads.",
                "Synthetic silicone mannequin tissue exhibits uniform elasticity, whereas human residual limbs feature complex heterogeneous soft-tissue layers.",
                "Thin-film sensors measure normal stress only, neglecting frictional interface shear stresses that contribute heavily to skin blisters.",
                "Does not simulate biological fluid volume changes (daily residual limb diurnal volume fluctuations)."
            ],
            "quiz": [
                {
                    "question": "Which anatomical structure is the primary pressure-tolerant weight-bearing region in a transtibial PTB socket?",
                    "options": ["Patellar tendon", "Head of the fibula", "Distal end of the severed tibia", "Hamstring tendon insertion"],
                    "correct": 0,
                    "explanation": "The patellar tendon is a dense, fibrous ligamentous tissue capable of tolerating high compressive forces, making it the primary PTB weight-bearing bar."
                },
                {
                    "question": "What is the typical capillary closing pressure in human dermis?",
                    "options": ["4.0 to 4.3 kPa (approx. 30 to 32 mmHg)", "40 to 43 kPa", "100 to 120 kPa", "0.5 kPa"],
                    "correct": 0,
                    "explanation": "Capillary closing pressure is ~30 to 32 mmHg (~4.0 to 4.3 kPa); pressures exceeding this level cause local tissue ischemia."
                },
                {
                    "question": "If an axial load of 500 N produces a patellar-tendon interface pressure of 110.0 kPa, what is sensitivity k_soc?",
                    "options": ["0.1100 kPa/N", "0.2200 kPa/N", "0.4400 kPa/N", "1.1000 kPa/N"],
                    "correct": 1,
                    "explanation": "k_soc = P_ptb / W = 110.0 kPa / 500 N = 0.2200 kPa/N."
                },
                {
                    "question": "What is the primary advantage of a Total Surface Bearing (TSB) socket over a PTB socket?",
                    "options": ["It distributes load uniformly over the entire limb surface, lowering localized peak pressures", "It is made of wood", "It does not require a liner", "It weighs more than 10 kg"],
                    "correct": 0,
                    "explanation": "TSB sockets distribute contact pressure over the entire residual limb surface using vacuum suspension, eliminating painful localized pressure peaks."
                }
            ],
            "settings": ["Socket: Custom carbon-fiber transtibial PTB socket with silicone liner", "Model: Robotic residual limb mannequin with Shore 20A soft tissue", "Sensor: Tekscan F-Socket thin-film piezoresistive array (calibrated to 250 kPa)"],
            "samples": [200.0, 300.0, 400.0, 500.0, 600.0, 700.0],
            "published": True,
            "simModes": [
                {"id": "bench", "icon": "🦾", "label": "1. Prosthetic Loading Rig"},
                {"id": "compare", "icon": "📊", "label": "2. Interface Pressure vs Load"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Socket Pressure Sandbox"}
            ]
        }
    ]
