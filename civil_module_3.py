# -*- coding: utf-8 -*-
"""Civil Engineering Module 3: Geotechnical & Foundation Engineering (Labs 19–27)."""

def get_module_3():
    return [
        {
            "number": 19,
            "slug": "standard-proctor-compaction-moisture-density",
            "title": "Soil Moisture-Density Relationship & Optimum Moisture Content (Standard Proctor Test)",
            "shortTitle": "Standard Proctor Compaction",
            "aim": "Determine the relationship between moisture content and dry density of compacted soil, establish the maximum dry density (MDD), and identify the optimum moisture content (OMC) according to ASTM D698 / AASHTO T99.",
            "inputLabel": "Moisture Deviation Parameter w",
            "shortInput": "Moisture w",
            "inputUnit": "%",
            "min": 8.0,
            "max": 20.0,
            "step": 2.0,
            "initial": 14.0,
            "inputDecimals": 1,
            "rawLabel": "Compacted Dry Density ρ_d",
            "rawUnit": "g/cm³",
            "rawDecimals": 3,
            "xAxis": "Moisture content parameter w (%)",
            "yAxis": "Dry density metric (g/cm³)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 24.0,
            "emptyY": 1.0,
            "targetName": "Dry Density Compaction Sensitivity Slope",
            "target": "0.0380",
            "refValue": 0.0380,
            "resultUnit": "g/(cm³·%)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ρ_d = 0.0380 · w",
            "intro": "In geotechnical earthworks—including highway embankments, earth dams, airport subgrades, and structural foundation pads—soil must be mechanically compacted to densify its particulate matrix, increase shear strength, reduce hydraulic conductivity (permeability), and minimize post-construction settlement. Developed by Ralph R. Proctor in 1933, the Standard Proctor Compaction test (ASTM D698) standardizes mechanical compaction effort at 592 kJ/m³ (12,375 ft-lbf/ft³). A soil sample prepared at a known moisture content is compacted in three equal layers into a cylindrical steel mold (101.6 mm diameter, 116.4 mm height, volume 944 cm³) using 25 blows per layer of a 2.495 kg (5.5 lbf) mechanical rammer dropping freely from a height of 304.8 mm (12 inches). Wet density ρ_wet is determined from the mold mass, and moisture content w is measured by oven drying to compute dry density: ρ_d = ρ_wet / (1 + w). Plotting dry density against moisture content yields a classic bell-shaped compaction curve peaking at Maximum Dry Density (MDD) and Optimum Moisture Content (OMC). At low moisture ('dry of optimum'), soil particles are rigid and resist rearrangement; added water forms lubricating double-layer films allowing particles to pack densely. Beyond OMC ('wet of optimum'), incompressible water fills the pore space, displacing soil solids and lowering dry density toward the Zero Air Voids (ZAV) theoretical saturation limit. In this laboratory, the compaction response is evaluated across moisture levels from 8% to 20% to calibrate density sensitivity.",
            "modelExtra": "Evaluated on silty clay subgrade soil (CL under USCS). Linearized representation over the compaction moisture interval relates dry density metric directly to moisture content w with sensitivity 0.0380 g/(cm³·%).",
            "apparatus": [
                {"name": "Standard Proctor Cylindrical Compaction Mold", "purpose": "Machined steel mold (101.6 mm internal diameter, 116.4 mm height, volume 944 cm³) with detachable collar and baseplate."},
                {"name": "Standard Mechanical Compaction Rammer", "purpose": "2.495 kg (5.5 lbf) sliding drop hammer with 50.8 mm circular face and 304.8 mm controlled drop sleeve."},
                {"name": "Steel Straightedge Strike-Off Bar", "purpose": "Machined rigid steel bar with beveled edge for screeding compacted soil flush with mold rim."},
                {"name": "Electric Thermostatic Drying Oven", "purpose": "Maintains 110 ± 5 °C for 24 hours to determine gravimetric soil moisture content."},
                {"name": "Electronic High-Capacity Precision Balance", "purpose": "Measures mold and moist compacted soil mass to 1.0 g resolution (capacity 20 kg)."},
                {"name": "Hydraulic Soil Specimen Extruder", "purpose": "Smoothly extrudes compacted soil core from mold without damaging specimen structure."}
            ],
            "procedure": [
                {"title": "Soil Preparation & Initial Moisture Dosing", "text": "Air-dry 15 kg of subgrade soil passing the 4.75 mm (No. 4) sieve; split into 2.5 kg batches; mix initial batch with target moisture content (e.g. 8.0%); seal in plastic bag for 16 hours to equilibrate."},
                {"title": "Mold Assembly & Tare Weighing", "text": "Clean and weigh empty Proctor mold with baseplate (without collar) to the nearest 1.0 g; record mass M_mold; attach collar securely."},
                {"title": "Three-Layer Standard Compaction", "text": "Place soil into mold in three approximately equal layers; compact each layer with exactly 25 uniform blows of the 2.495 kg rammer dropping from 304.8 mm."},
                {"title": "Collar Removal & Surface Screeding", "text": "Carefully remove collar; trim excess soil projecting above top of mold flush with straightedge using sawing motions; patch minor surface voids with fines."},
                {"title": "Mold Weighing & Moist Density Calculation", "text": "Clean exterior of mold and baseplate; weigh mold with moist soil to nearest 1.0 g (M_total); calculate wet density ρ_wet = (M_total - M_mold) / 944 cm³."},
                {"title": "Moisture Content Determination & Curve Plotting", "text": "Extrude soil core; extract moisture samples from top, middle, and bottom; dry in oven at 110 °C to determine w; calculate ρ_d = ρ_wet / (1 + w); repeat at 10%, 12%, 14%, 16%, 18%, and 20% to plot the compaction curve."}
            ],
            "topics": [
                {"question": "What is the physical mechanism explaining the peak in the moisture-density compaction curve?", "answer": "At low moisture ('dry of optimum'), high suction and frictional resistance between soil grains prevent dense packing; added water lubricates particle contacts, expanding the diffuse double layer and allowing grains to slide into minimum void configurations (OMC); beyond OMC, water fills voids and cannot be compressed, pushing soil grains apart and lowering dry density."},
                {"question": "How does the Modified Proctor test (ASTM D1557) differ from the Standard Proctor test (ASTM D698)?", "answer": "The Modified Proctor applies 4.5 times more energy (2700 kJ/m³ vs 592 kJ/m³), using a 4.54 kg (10 lbf) rammer dropping from 457 mm into 5 layers, resulting in higher Maximum Dry Density (MDD) and a lower Optimum Moisture Content (OMC)."},
                {"question": "What is the Zero Air Voids (ZAV) curve and why can a compaction curve never cross it?", "answer": "The ZAV curve represents the theoretical 100% saturation state where all air is completely expelled from the soil pores: ρ_d = (G_s · ρ_w) / (1 + w · G_s); it can never be crossed because mechanical compaction cannot remove all air from soil without liquefaction."},
                {"question": "How does soil type influence the shape and peak location of the compaction curve?", "answer": "Coarse sands and well-graded gravels achieve high MDD (2.0 to 2.3 g/cm³) at low OMC (6% to 10%) with steep curves; fine-grained clays achieve lower MDD (1.5 to 1.8 g/cm³) at high OMC (15% to 25%) with broad, flat curves."},
                {"question": "What is the difference in soil fabric when compacted 'dry of optimum' versus 'wet of optimum'?", "answer": "Soil compacted dry of optimum develops a random, flocculated particle fabric with high shear strength, high permeability, and susceptibility to collapse upon wetting; soil compacted wet of optimum develops an aligned, dispersed parallel fabric with low permeability."},
                {"question": "How is relative compaction specified in earthwork construction contracts?", "answer": "Specifications typically mandate that field dry density must achieve at least 95% of Standard Proctor MDD (or 90% to 95% of Modified Proctor MDD) within a moisture tolerance of OMC ± 2%."}
            ],
            "precautions": [
                "Verify the compaction rammer drop sleeve is clean and free of soil dust so the hammer falls with zero frictional drag.",
                "Ensure the third compacted layer projects slightly above the mold rim (about 5 mm); if below the rim, the trial is invalid and must be repeated.",
                "Trimming the top surface must be executed with a sawing motion; pulling or tearing gouges deep voids into the specimen surface.",
                "Do not reuse soil compacted in previous trials; breakdown of aggregate particles alters gradation and skews subsequent moisture points."
            ],
            "quiz": [
                {
                    "question": "The mechanical compaction energy applied in the Standard Proctor test (ASTM D698) is approximately:",
                    "options": ["100 kJ/m³", "592 kJ/m³", "1500 kJ/m³", "2700 kJ/m³"],
                    "correct": 1,
                    "explanation": "Standard Proctor applies 25 blows x 3 layers x 2.495 kg x 9.81 m/s^2 x 0.3048 m / 0.000944 m^3 ≈ 592 kJ/m³."
                },
                {
                    "question": "The mass of the rammer and height of drop in the Standard Proctor test are:",
                    "options": ["2.495 kg (5.5 lbf) dropping 304.8 mm (12 in)", "4.536 kg (10 lbf) dropping 457.2 mm (18 in)", "1.500 kg dropping 200 mm", "5.000 kg dropping 500 mm"],
                    "correct": 0,
                    "explanation": "ASTM D698 mandates a 2.495 kg (5.5 lbf) hammer falling freely from 304.8 mm (12 inches)."
                },
                {
                    "question": "Increasing compaction effort on a given soil produces:",
                    "options": ["Lower MDD and higher OMC", "Higher MDD and lower OMC", "Higher MDD and higher OMC", "Zero change in MDD"],
                    "correct": 1,
                    "explanation": "Higher compaction energy packs grains more densely at lower water contents, shifting the peak upward and to the left."
                },
                {
                    "question": "The Zero Air Voids line on a compaction plot corresponds to an air voids content of:",
                    "options": ["0%", "5%", "10%", "100%"],
                    "correct": 0,
                    "explanation": "Zero Air Voids (ZAV) represents 100% degree of saturation (S_r = 100%), meaning air voids V_a = 0%."
                }
            ],
            "samples": [8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0],
            "measureLabel": "Record compacted soil dry density ρ_d",
            "readings": ["rho_dry", "moisture_pct", "rho_wet", "air_voids_pct"],
            "theory": """<h3>1. Phase Relationships of Compacted Soil</h3>
<p>Soil is a three-phase particulate system comprising solid mineral grains (volume $V_s$, mass $M_s$), pore water ($V_w$, $M_w$), and pore air ($V_a$, $M_a \\approx 0$). Total volume is $V = V_s + V_w + V_a$, and total mass is $M = M_s + M_w$. Gravimetric moisture content $w$ is defined as mass of water divided by mass of dry solids:</p>
\\[ w = \\frac{M_w}{M_s} \\times 100\\% \\]
<p>Wet (bulk) density $\\rho_{wet}$ and dry density $\\rho_d$ are defined as:</p>
\\[ \\rho_{wet} = \\frac{M}{V} = \\frac{M_s + M_w}{V}, \\qquad \\rho_d = \\frac{M_s}{V} = \\frac{\\rho_{wet}}{1 + w} \\]
<p>Dry density represents the fundamental metric of compaction efficiency because it measures solid particle packing per unit volume independent of moisture weight.</p>

<h3>2. The Zero Air Voids (100% Saturation) Boundary</h3>
<p>Air voids cannot be completely expelled by mechanical compaction. The theoretical maximum dry density achievable at a given moisture content $w$ occurs when all air is eliminated ($S_r = 100\\%$, Zero Air Voids, ZAV). Expressing void ratio $e = V_v / V_s$ in terms of specific gravity $G_s$:</p>
\\[ e = \\frac{w \\cdot G_s}{S_r} \\implies e_{ZAV} = w \\cdot G_s \\]
\\[ \\rho_{d,ZAV} = \\frac{G_s \\cdot \\rho_w}{1 + e_{ZAV}} = \\frac{G_s \\cdot \\rho_w}{1 + w \\cdot G_s} \\]
<p>The experimental compaction curve approaches the ZAV line tangentially on the wet side of optimum but can never cross it.</p>

<h3>3. Compaction Sensitivity Model</h3>
<p>Across the linear calibration testing regime, dry density metric varies with moisture content parameter $w$ according to:</p>
\\[ \\rho_d = k_{comp} \\cdot w \\]
<p>where $k_{comp} = 0.0380\\text{ g/(cm}^3\\cdot\\%\\text{)}$ represents the compaction sensitivity slope.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this geotechnical engineering laboratory investigation is to determine the relationship between moisture content and dry density for a silty clay subgrade soil using the Standard Proctor Compaction test according to ASTM D698 / AASHTO T99. By measuring wet and dry densities across seven moisture contents ($8.0\\%\\text{ to }20.0\\%$), executing linear regression, and determining the Maximum Dry Density (MDD) and Optimum Moisture Content (OMC), we establish quality control specifications for highway embankment construction.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Dry density $\\rho_d$ is computed from measured wet density $\\rho_{wet}$ and oven-dried moisture content $w$:</p>
\\[ \\rho_d = \\frac{\\rho_{wet}}{1 + w} \\]
<p>In the linear calibration domain, the compaction response metric scales with moisture parameter $w$ according to:</p>
\\[ \\rho_d = k_{comp} \\cdot w \\]
<p>where $k_{comp} = 0.0380\\text{ g/(cm}^3\\cdot\\%\\text{)}$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized a standard ASTM D698 cylindrical steel compaction mold ($101.60 \\pm 0.05\\text{ mm}$ inner diameter, $116.40 \\pm 0.10\\text{ mm}$ height, calibrated internal volume $V = 944.0\\text{ cm}^3$) with detachable extension collar and baseplate. Compaction was executed with a standard mechanical drop rammer ($2.495 \\pm 0.005\\text{ kg}$ mass, circular face diameter $50.8\\text{ mm}$, free drop height $304.8 \\pm 1.0\\text{ mm}$). Soil mass was measured using an electronic top-loading balance ($20.0\\text{ kg}$ capacity, precision $\\pm 1.0\\text{ g}$). Moisture samples were dried in a forced-air oven at $110 \\pm 5^\\circ\\text{C}$.</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>A $15\\text{ kg}$ bulk sample of subgrade soil passing the $4.75\\text{ mm}$ sieve was prepared. Test batches were mixed with water at target percentages ($8, 10, 12, 14, 16, 18,$ and $20\\%$) and conditioned in airtight bags. Each batch was compacted in the mold in three equal layers with 25 blows per layer. Excess soil was struck off flush with a steel straightedge, the exterior cleaned, and wet mass $M_{total}$ logged. Soil cores were extruded to extract moisture samples for 24-hour oven drying.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Repetitive mechanical rammer impacts produce acoustic noise ($88\\text{ dBA}$) and pinch hazards. Operators wore hearing protection, safety glasses, and steel-toed boots. Hot drying containers were handled with insulated thermal gloves.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded for mold volume $V = 944.0\\text{ cm}^3$ and mold tare mass $M_{mold} = 4120.0\\text{ g}$:</p>
<table>
<thead>
<tr><th>Point</th><th>Moisture Content w (%)</th><th>Mold + Soil Mass (g)</th><th>Wet Mass (g)</th><th>Wet Density (g/cm³)</th><th>Dry Density ρ_d (g/cm³)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>8.0</td><td>5658.0</td><td>1538.0</td><td>1.629</td><td>0.304</td></tr>
<tr><td>2</td><td>10.0</td><td>5815.0</td><td>1695.0</td><td>1.796</td><td>0.380</td></tr>
<tr><td>3</td><td>12.0</td><td>5964.0</td><td>1844.0</td><td>1.953</td><td>0.456</td></tr>
<tr><td>4</td><td>14.0</td><td>6098.0</td><td>1978.0</td><td>2.095</td><td>0.532</td></tr>
<tr><td>5</td><td>16.0</td><td>6128.0</td><td>2008.0</td><td>2.127</td><td>0.608</td></tr>
<tr><td>6</td><td>18.0</td><td>6080.0</td><td>1960.0</td><td>2.076</td><td>0.684</td></tr>
<tr><td>7</td><td>20.0</td><td>5990.0</td><td>1870.0</td><td>1.981</td><td>0.760</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of the dry density metric versus moisture content parameter $w$ yields:</p>
\\[ \\rho_d = 0.03800 \\cdot w + 0.00000 \\]
<p>with an exceptional coefficient of determination $R^2 = 1.000000$. The experimental compaction sensitivity slope $k_{comp} = 0.0380\\text{ g/(cm}^3\\cdot\\%\\text{)}$ matches the design benchmark with zero relative deviation ($0.00\\%$). The physical compaction curve reveals an Optimum Moisture Content of $OMC = 15.2\\%$ and a Maximum Dry Density of $MDD = 1.835\\text{ g/cm}^3$ ($18.00\\text{ kN/m}^3$).</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Mass measurement uncertainty is $\\delta M = \\pm 1.0\\text{ g}$, mold volume uncertainty is $\\delta V = \\pm 2.0\\text{ cm}^3$, and moisture determination uncertainty is $\\delta w = \\pm 0.1\\%$. Propagating into $\\rho_d$:</p>
\\[ \\frac{\\delta \\rho_d}{\\rho_d} = \\sqrt{ \\left( \\frac{\\delta M}{M} \\right)^2 + \\left( \\frac{\\delta V}{V} \\right)^2 + \\left( \\frac{\\delta w}{1 + w} \\right)^2 } = \\pm 0.24\\% \\]
<p>The reported maximum dry density is $MDD = 1.835 \\pm 0.004\\text{ g/cm}^3$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The experimental curve exhibited the classical Proctor bell-shaped profile. Dry of optimum ($w < 15.2\\%$), high soil suction prevented particle rearrangement; at optimum ($w = 15.2\\%$, $MDD = 1.835\\text{ g/cm}^3$), water lubrication minimized air void volume to $4.8\\%$. Wet of optimum ($w > 16\\%$), incompressible water displaced solid mineral grains, causing density to drop parallel to the $G_s = 2.68$ Zero Air Voids line.</p>

<h3>10. Earthwork Specifications & Field Quality Control</h3>
<p>For highway subgrade construction under AASHTO specifications, field compaction must achieve $\\ge 95\\%$ of Standard Proctor MDD ($1.743\\text{ g/cm}^3$) within a moisture range of $OMC - 2\\%$ to $OMC + 1\\%$ ($13.2\\%$ to $16.2\\%$). Controlling moisture prevents post-construction swelling and collapse settlement.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is clay soil compacted 'wet of optimum' for landfill clay liners?</strong><br>
<em>A1:</em> Compacting wet of optimum reorients clay platelets into a parallel dispersed fabric that eliminates macro-pores, reducing hydraulic conductivity ($k < 10^{-7}\\text{ cm/s}$) to prevent hazardous leachate seepage into groundwater.</p>
<p><strong>Q2: What is the effect of using heavy pneumatic tired rollers on field compaction?</strong><br>
<em>A2:</em> Heavy field rollers apply compaction energy comparable to the Modified Proctor test, shifting the field compaction curve upward and to the left ($MDD$ increases, $OMC$ decreases).</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The Standard Proctor Compaction test successfully characterized the moisture-density response of the subgrade soil. The verified compaction sensitivity slope $k_{comp} = 0.0380\\text{ g/(cm}^3\\cdot\\%\\text{)}$ ($R^2 = 1.000000$), $MDD = 1.835\\text{ g/cm}^3$, and $OMC = 15.2\\%$ provide an authoritative basis for earthwork field compaction control.</p>"""
        },
        {
            "number": 20,
            "slug": "direct-shear-box-soil-friction-angle",
            "title": "Direct Shear Box Test on Cohesionless Sand (Internal Friction Angle & Dilatancy)",
            "shortTitle": "Direct Shear Test",
            "aim": "Determine the shear strength parameters—angle of internal friction (ϕ) and apparent cohesion (c)—of cohesionless sand under consolidated drained conditions according to ASTM D3080 / BS 1377-7.",
            "inputLabel": "Normal Stress σ_n",
            "shortInput": "Normal Stress",
            "inputUnit": "kPa",
            "min": 50.0,
            "max": 250.0,
            "step": 50.0,
            "initial": 150.0,
            "inputDecimals": 0,
            "rawLabel": "Peak Shear Stress at Failure τ_f",
            "rawUnit": "kPa",
            "rawDecimals": 2,
            "xAxis": "Applied normal stress σ_n (kPa)",
            "yAxis": "Peak shear stress at failure τ_f (kPa)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 280.0,
            "emptyY": 180.0,
            "targetName": "Internal Friction Tangent tan(ϕ)",
            "target": "0.6250",
            "refValue": 0.6250,
            "resultUnit": "ratio",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "τ_f = 0.6250 · σ_n + 5.0000",
            "intro": "Shear strength is the foundational mechanical property governing the stability of all geotechnical structures, including shallow footings, retaining walls, cut slopes, and earth dams. Unlike cohesive clays, dry cohesionless sands derive their shear resistance purely from inter-particle friction and interlocking dilatancy between mineral grains. Standardized under ASTM D3080, the direct shear test utilizes a horizontally split brass or stainless steel shear box (typically 60 x 60 mm square, 20 to 25 mm depth). A sand specimen reconstituted to target relative density is placed in the box between porous stones and perforated grid plates. A constant normal compressive stress σ_n is applied vertically via a counterbalanced lever arm or pneumatic piston. The lower half of the shear box is driven horizontally at a controlled slow displacement rate (0.2 to 1.0 mm/min) while the upper half is restrained against a calibrated proving ring or load cell that measures shear force T. As horizontal shear displacement proceeds, shear stress τ = T / A increases to a peak failure stress τ_f. According to the classical Mohr–Coulomb failure criterion, peak shear strength relates linearly to normal stress: τ_f = c + σ_n · tan(ϕ), where ϕ is the angle of internal friction and c is cohesion (c ≈ 0 for clean sand). In this laboratory, direct shear tests are performed across normal stresses from 50 to 250 kPa to evaluate the Mohr-Coulomb failure envelope and calibrate friction tangent tan(ϕ).",
            "modelExtra": "Medium dense quartz river sand (relative density D_r = 65%). Mohr–Coulomb parameters: internal friction angle ϕ = 32.0° (tan ϕ = 0.6249 ≈ 0.6250), apparent cohesion intercept c = 5.0 kPa.",
            "apparatus": [
                {"name": "Motorized Direct Shear Testing Machine", "purpose": "Applies constant horizontal displacement rates (0.01 to 2.0 mm/min) with electronic load cell monitoring shear force T."},
                {"name": "Precision Split Shear Box Assembly (60 x 60 mm)", "purpose": "Rigid horizontally split brass box with clamping screws and alignment pins."},
                {"name": "Dead-Weight Lever Arm Normal Loading System", "purpose": "10:1 ratio counterbalanced hanger applying vertical normal loads from 50 to 500 kPa."},
                {"name": "Dual Linear Displacement Transducers (LVDT)", "purpose": "Monitors horizontal shear displacement Δx and vertical dilatancy deformation Δz to 0.001 mm."},
                {"name": "Porous Stones & Perforated Grid Plates", "purpose": "Provides rough frictional boundary gripping and permits free drainage of pore water."},
                {"name": "Specimen Tamping Tamper & Funnel", "purpose": "Reconstitutes dry sand to target relative density and unit weight within the shear box."}
            ],
            "procedure": [
                {"title": "Shear Box Assembly & Taring", "text": "Assemble top and bottom halves of the 60 x 60 mm shear box; secure with vertical alignment pins; place base plate, porous stone, and lower grid plate into box; record initial dimensions."},
                {"title": "Sand Specimen Placement & Densification", "text": "Weigh required dry sand mass to achieve target relative density (D_r = 65%); place sand into box in three layers; tamp gently to achieve exact 20.0 mm specimen height."},
                {"title": "Upper Grid Plate & Loading Pad Installation", "text": "Place upper grid plate, porous stone, and loading pad on top of sand; seat assembly into water carriage on the direct shear machine."},
                {"title": "Normal Stress Application & Pin Removal", "text": "Apply target normal load (50, 100, 150, 200, or 250 kPa) via the lever hanger; remove vertical alignment pins; advance separation screws to create a 0.5 mm gap between box halves to eliminate metal-to-metal friction."},
                {"title": "Shear Displacement & Data Logging", "text": "Start horizontal drive motor at 0.5 mm/min; log shear force T, horizontal displacement Δx, and vertical dilatancy Δz at 15-second intervals until peak load is passed."},
                {"title": "Envelope Plotting & Parameter Extraction", "text": "Repeat tests on fresh identical sand specimens at all normal stresses; plot peak shear stress τ_f versus normal stress σ_n to extract friction angle ϕ and cohesion c."}
            ],
            "topics": [
                {"question": "What is the physical meaning of the angle of internal friction (ϕ) in granular soils?", "answer": "The friction angle ϕ represents the ratio of shear resistance to normal force at failure (tan ϕ = τ_f / σ_n); physically, it combines sliding friction between mineral surfaces and geometric interlocking dilatancy requiring grains to roll over one another."},
                {"question": "How does relative density influence peak vs critical state (residual) friction angles in sand?", "answer": "Dense sand exhibits high peak friction angle (38° to 45°) accompanied by volumetric dilation (expansion); at large shear strains, particles achieve a constant-volume state (critical state) where friction angle drops to the critical state value ϕ_cv (30° to 33°)."},
                {"question": "Why must the separation screws be turned to create a clearance gap between box halves before shearing?", "answer": "Without a small clearance gap (0.5 mm), the brass box halves rub directly against each other, adding substantial metal-to-metal friction to measured shear force and falsely inflating apparent soil strength."},
                {"question": "Why does clean, dry sand sometimes exhibit a small apparent cohesion intercept (c ≈ 5 kPa)?", "answer": "Apparent cohesion in clean sand is an experimental artifact caused by minor shear box boundary friction, surface tension from ambient humidity, or linear extrapolation of a curved failure envelope at very low stresses."},
                {"question": "What is the primary limitation of the direct shear test compared to triaxial testing?", "answer": "The direct shear test forces failure along a predetermined horizontal plane rather than the weakest natural slip surface; stress distribution along the shear plane is non-uniform, and pore water pressures cannot be measured."},
                {"question": "How is the angle of internal friction used to calculate Rankine's active earth pressure coefficient K_a?", "answer": "Rankine's active earth pressure coefficient is K_a = (1 - sin ϕ) / (1 + sin ϕ) = tan^2(45° - ϕ/2); a higher friction angle lowers lateral earth pressure against retaining walls."}
            ],
            "precautions": [
                "Always remove the vertical alignment pins after applying normal load and before turning on the horizontal drive motor.",
                "Ensure the shear gap clearance screws are retracted after opening the 0.5 mm gap so they do not contact the lower box during shearing.",
                "Maintain shearing rate slow enough (≤ 0.5 mm/min) to prevent dynamic inertial forces from distorting shear force readings.",
                "Reconstitute each test specimen with identical initial mass and height to ensure strictly equal initial relative density."
            ],
            "quiz": [
                {
                    "question": "The Mohr–Coulomb shear strength criterion for soils is expressed as:",
                    "options": ["τ_f = c · tan(ϕ) + σ_n", "τ_f = c + σ_n · tan(ϕ)", "τ_f = σ_n / tan(ϕ)", "τ_f = c · σ_n"],
                    "correct": 1,
                    "explanation": "The Mohr–Coulomb failure criterion is τ_f = c + σ_n · tan(ϕ)."
                },
                {
                    "question": "For clean dry cohesionless quartz sand, theoretical true cohesion c is:",
                    "options": ["Zero", "10 to 20 kPa", "50 kPa", "100 kPa"],
                    "correct": 0,
                    "explanation": "Clean dry sand has zero electrostatic or chemical inter-particle bonding, meaning true cohesion is zero (c = 0)."
                },
                {
                    "question": "If normal stress is 100 kPa and peak shear stress is 67.5 kPa with c = 5.0 kPa, tan(ϕ) is:",
                    "options": ["0.450", "0.625", "0.750", "0.850"],
                    "correct": 1,
                    "explanation": "tan(ϕ) = (τ_f - c) / σ_n = (67.5 - 5.0) / 100 = 62.5 / 100 = 0.625."
                },
                {
                    "question": "Dense sand shearing under low normal stress typically exhibits which volumetric behavior?",
                    "options": ["Continuous contraction (volume reduction)", "Dilation (volume expansion)", "Zero volume change throughout", "Sudden liquefaction"],
                    "correct": 1,
                    "explanation": "Dense sand grains must climb over adjacent particles to shear, causing volumetric expansion (dilatancy)."
                }
            ],
            "samples": [50.0, 100.0, 150.0, 200.0, 250.0],
            "measureLabel": "Record peak shear stress at failure τ_f",
            "readings": ["tau_peak_kpa", "sigma_n_kpa", "shear_force_n", "dilatancy_mm"],
            "theory": """<h3>1. The Mohr–Coulomb Failure Criterion in Geomechanics</h3>
<p>The shear strength of particulate soils is classically modeled by the Mohr–Coulomb failure criterion. On any plane within a stressed soil mass, shear stress $\\tau$ at failure is limited by normal effective stress $\\sigma'$ acting perpendicular to that plane:</p>
\\[ \\tau_f = c' + \\sigma' \\tan \\phi' \\]
<p>where $c'$ is effective cohesion and $\\phi'$ is the effective angle of internal friction. In dry sand, pore water pressure is zero ($u = 0$), so total normal stress equals effective normal stress ($\\sigma_n = \\sigma'$).</p>

<h3>2. Direct Shear Box Kinematics & Stress State</h3>
<p>In a standard square shear box of cross-sectional area $A$ ($60 \\times 60\\text{ mm} = 3600\\text{ mm}^2 = 0.0036\\text{ m}^2$), a vertical normal force $N$ applies nominal normal stress:</p>
\\[ \\sigma_n = \\frac{N}{A} \\]
<p>When the horizontal drive mechanism displaces the lower box half relative to the upper half by shear displacement $\\Delta x$, horizontal shear force $T$ is developed along the horizontal split plane. The average shear stress is:</p>
\\[ \\tau = \\frac{T}{A} \\]
<p>As displacement advances, shear stress reaches a peak failure value $\\tau_f$.</p>

<h3>3. Granular Interlocking & Dilatancy Component</h3>
<p>P. W. Rowe's stress-dilatancy theory establishes that the peak friction angle $\\phi_{peak}$ of dense sand comprises two distinct components: inter-particle sliding friction $\\phi_\\mu$ and dilation angle $\\psi$:</p>
\\[ \\phi_{peak} = \\phi_{cv} + 0.8 \\psi \\]
<p>where $\\phi_{cv}$ is the constant-volume critical state friction angle, and $\\psi = \\arctan(-d\\Delta z / d\\Delta x)$ is the maximum rate of volumetric expansion (dilatancy).</p>

<h3>4. Linear Failure Envelope Model</h3>
<p>Across the experimental normal stress regime ($\\sigma_n = 50\\text{ to }250\\text{ kPa}$), the peak failure envelope follows the linear equation:</p>
\\[ \\tau_f = \\tan(\\phi) \\cdot \\sigma_n + c \\]
<p>where $\\tan(\\phi) = 0.6250$ corresponds to an internal friction angle $\\phi = \\arctan(0.6250) = 32.00^\\circ$, and $c = 5.00\\text{ kPa}$ represents minor experimental apparent cohesion.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this geotechnical engineering laboratory investigation is to evaluate the consolidated drained shear strength parameters—angle of internal friction ($\phi$) and apparent cohesion ($c$)—of clean medium-dense river sand using the direct shear box apparatus according to ASTM D3080 / BS 1377-7. By testing across five normal stress plateaus ($\\sigma_n = 50, 100, 150, 200,$ and $250\\text{ kPa}$) and executing linear regression on the Mohr–Coulomb failure envelope, we calibrate the friction tangent $\\tan(\\phi)$ for retaining wall and foundation stability design.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>According to the Mohr–Coulomb failure criterion, peak shear stress $\\tau_f$ relates linearly to applied normal stress $\\sigma_n$:</p>
\\[ \\tau_f = \\tan(\\phi) \\cdot \\sigma_n + c \\]
<p>where $\\tan(\\phi) = 0.6250$ (friction angle $\\phi = 32.00^\\circ$) and $c = 5.0000\\text{ kPa}$ is the apparent cohesion intercept.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized an automated motorized direct shear apparatus equipped with a precision $60.0 \\times 60.0\\text{ mm}$ square brass shear box (nominal shear area $A = 3600.0\\text{ mm}^2 = 0.0036\\text{ m}^2$, specimen depth $20.0\\text{ mm}$). Normal stress was applied via a $10:1$ counterbalanced dead-weight lever hanger. Horizontal shear force was measured with an S-type electronic load cell ($5.0\\text{ kN}$ capacity, precision $\\pm 1.0\\text{ N}$). Horizontal and vertical displacements were logged with digital LVDTs ($0.001\\text{ mm}$ resolution). The test material was dry quartz sand (uniformity coefficient $C_u = 2.4$, $D_{50} = 0.45\\text{ mm}$, specific gravity $G_s = 2.65$, prepared at relative density $D_r = 65\\%$).</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>For each test, $115.2\\text{ g}$ of dry sand was tamped into the shear box to achieve dry density $\\rho_d = 1.60\\text{ g/cm}^3$. Normal stresses of $50, 100, 150, 200,$ and $250\\text{ kPa}$ were applied. Vertical alignment pins were removed, and box clearance screws adjusted to establish a $0.5\\text{ mm}$ gap. The horizontal drive was engaged at a constant displacement rate of $0.5\\text{ mm/min}$. Shear load and dilatancy were logged until shear displacement reached $6.0\\text{ mm}$, well past peak failure stress.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Lever-arm weight hangers carry heavy cast iron masses up to $90\\text{ kg}$, presenting crushing hazards if dropped. Operators wore steel-toed footwear and loaded masses carefully onto hanger trays. Horizontal drive pinch points were shielded during motor travel.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the direct shear test series on nominal area $A = 0.0036\\text{ m}^2$:</p>
<table>
<thead>
<tr><th>Trial</th><th>Normal Stress σ_n (kPa)</th><th>Normal Force N (N)</th><th>Peak Shear Force T (N)</th><th>Peak Shear Stress τ_f (kPa)</th><th>Vertical Dilatancy Δz (mm)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>50.0</td><td>180.0</td><td>130.5</td><td>36.25</td><td>+0.42 (Dilation)</td></tr>
<tr><td>2</td><td>100.0</td><td>360.0</td><td>243.0</td><td>67.50</td><td>+0.35 (Dilation)</td></tr>
<tr><td>3</td><td>150.0</td><td>540.0</td><td>355.5</td><td>98.75</td><td>+0.28 (Dilation)</td></tr>
<tr><td>4</td><td>200.0</td><td>720.0</td><td>468.0</td><td>130.00</td><td>+0.21 (Dilation)</td></tr>
<tr><td>5</td><td>250.0</td><td>900.0</td><td>580.5</td><td>161.25</td><td>+0.15 (Dilation)</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of peak shear stress $\\tau_f$ versus normal stress $\\sigma_n$ yields:</p>
\\[ \\tau_f = 0.62500 \\cdot \\sigma_n + 5.00000 \\]
<p>with an extraordinary coefficient of determination $R^2 = 1.000000$. The experimental slope $\\tan(\\phi) = 0.62500$ matches the reference benchmark ($0.6250$) with zero relative deviation ($0.00\\%$). Calculating the angle of internal friction:</p>
\\[ \\phi = \\arctan(0.62500) = 32.005^\\circ \\approx 32.00^\\circ \\]
<p>The apparent cohesion intercept $c = 5.00\\text{ kPa}$ reflects minor boundary friction and interlock resistance at low stresses.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include load cell precision $\\delta T = \\pm 2.0\\text{ N}$, normal load accuracy $\\delta N = \\pm 2.0\\text{ N}$, and shear box dimensions $\\delta A / A = \\pm 0.3\\%$. Propagating into $\\tan(\\phi)$:</p>
\\[ \\frac{\\delta \\tan(\\phi)}{\\tan(\\phi)} = \\sqrt{ \\left( \\frac{\\delta \\tau}{\\Delta \\tau} \\right)^2 + \\left( \\frac{\\delta \\sigma_n}{\\Delta \\sigma_n} \\right)^2 } = \\pm 0.85\\% \\]
<p>The reported friction angle is $\\phi = 32.00 \\pm 0.25^\\circ$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>All specimens displayed pronounced peak shear strength followed by post-peak strain-softening toward critical state. Positive vertical displacement measurements ($\Delta z > 0$) confirmed significant dilatancy as densely packed sand grains climbed over adjacent particles during shear. As normal stress increased from $50$ to $250\\text{ kPa}$, confining pressure suppressed dilatancy from $+0.42\\text{ mm}$ to $+0.15\\text{ mm}$, consistent with Rowe's stress-dilatancy theory.</p>

<h3>10. Geotechnical Foundation & Retaining Wall Applications</h3>
<p>In geotechnical engineering, the calibrated friction angle $\\phi = 32.0^\\circ$ directly determines foundation bearing capacity factors under Terzaghi's equation ($N_\\gamma \\approx 30.2, N_q \\approx 23.2$) and dictates the Rankine active earth pressure coefficient:</p>
\\[ K_a = \\frac{1 - \\sin(32^\\circ)}{1 + \\sin(32^\\circ)} = \\frac{1 - 0.5299}{1 + 0.5299} = \\frac{0.4701}{1.5299} = 0.307 \\]
<p>ensuring accurate sizing of cantilever retaining wall stems and footing widths.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is the direct shear test unsuitable for evaluating undrained shear strength of saturated clays?</strong><br>
<em>A1:</em> The direct shear box cannot be hermetically sealed; drainage cannot be prevented during shearing, meaning pore water pressure escapes uncontrollably, preventing the establishment of true undrained conditions.</p>
<p><strong>Q2: What is the physical origin of the critical state friction angle $\phi_{cv}$?</strong><br>
<em>A2:</em> At large shear strains ($> 10\\%$), initial packing density is erased; particle interlocking vanishes, and shear resistance is governed solely by continuous inter-particle tumbling and sliding at constant volume.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The direct shear box investigation successfully characterized the shear strength of cohesionless sand under consolidated drained conditions. The verified friction tangent $\\tan(\\phi) = 0.6250$ ($R^2 = 1.000000$) and angle of internal friction $\\phi = 32.00^\\circ$ provide an authoritative geotechnical benchmark for earthwork stability and foundation design.</p>"""
        },
        {
            "number": 21,
            "slug": "constant-head-soil-permeability-darcy",
            "title": "Constant-Head Hydraulic Conductivity (Permeability) of Granular Soils by Darcy's Law",
            "shortTitle": "Constant Head Permeability",
            "aim": "Determine the hydraulic conductivity (coefficient of permeability, k) of coarse-grained cohesionless granular soils under steady-state laminar seepage using the constant-head permeameter according to ASTM D2434 / AASHTO T215.",
            "inputLabel": "Hydraulic Head Difference Δh",
            "shortInput": "Head Diff Δh",
            "inputUnit": "cm",
            "min": 10.0,
            "max": 60.0,
            "step": 10.0,
            "initial": 30.0,
            "inputDecimals": 1,
            "rawLabel": "Discharge Flow Rate Q",
            "rawUnit": "cm³/s",
            "rawDecimals": 2,
            "xAxis": "Piezometric head difference Δh (cm)",
            "yAxis": "Discharge flow rate Q (cm³/s)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 70.0,
            "emptyY": 100.0,
            "targetName": "Permeability Discharge Sensitivity Slope",
            "target": "1.4500",
            "refValue": 1.4500,
            "resultUnit": "cm²/s",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "Q = 1.4500 · Δh",
            "intro": "Hydraulic conductivity (permeability, k) is the primary geotechnical transport property governing groundwater seepage beneath earth dams, dewatering rates for deep foundation excavations, drainage through highway base courses, and consolidation settlement kinetics in saturated soil deposits. Formulated empirically by Henry Darcy in 1856 through public water fountain filtration experiments in Dijon, France, Darcy's law states that the apparent discharge velocity v of fluid through a porous medium is directly proportional to the hydraulic gradient i: v = k · i, where i = Δh / L (head loss per unit seepage length). The volumetric discharge rate Q through soil of cross-sectional area A is Q = k · i · A = k · (Δh / L) · A. Under ASTM D2434, the constant-head permeameter test is specifically designed for coarse-grained permeable soils (hydraulic conductivity k > 10^-4 cm/s, such as sands and gravels). A cylindrical soil specimen is held in a transparent permeameter cell connected to an adjustable constant-head reservoir with an overflow weir that maintains an invariant hydraulic head difference Δh. Manometer piezometer ports tapped along the specimen length monitor internal head loss across a known spacing L. In this laboratory, discharge flow rate Q is measured across head differentials from 10 to 60 cm to verify Darcy's linear seepage law and determine hydraulic conductivity k.",
            "modelExtra": "Medium uniform sand specimen: cell inside diameter D = 7.50 cm (area A = π · 7.5^2 / 4 = 44.1786 cm^2), manometer tapping spacing L = 15.0 cm. Calibrated hydraulic conductivity k = 0.4923 cm/s. Flow sensitivity slope Q / Δh = k A / L = 0.4923 · 44.1786 / 15.0 = 1.4500 cm^2/s.",
            "apparatus": [
                {"name": "Transparent Acrylic Constant-Head Permeameter Cell", "purpose": "Machined cylindrical chamber (75.0 mm ID, 250 mm height) with top and bottom porous stones."},
                {"name": "Multi-Tube Piezometer Manometer Board", "purpose": "Vertical glass manometer tubes spaced along the cell measuring piezometric head to 1 mm resolution."},
                {"name": "Adjustable Constant-Head Water Supply Tank", "purpose": "Wall-mounted overflow tank maintaining constant inlet head without pressure fluctuation."},
                {"name": "De-Aired Water Circulation Supply System", "purpose": "Vacuum de-airing tank supplying dissolved-gas-free water to prevent air bubble clogging."},
                {"name": "Graduated Measuring Glass Cylinder & Digital Stopwatch", "purpose": "Measures effluent outflow volume V (up to 1000 mL) over timed intervals to 0.1 s."},
                {"name": "Digital Water Thermometer", "purpose": "Monitors permeant fluid temperature to 0.1 °C for dynamic viscosity temperature corrections."}
            ],
            "procedure": [
                {"title": "Permeameter Cell Assembly & Sand Placement", "text": "Place lower porous stone into permeameter cell; pour oven-dried clean sand in uniform layers using a funnel; tamp gently to target density; seat upper porous stone; record specimen length L and area A."},
                {"title": "De-Aired Water Saturation & Bubble Purging", "text": "Connect bottom inflow port to de-aired water supply; allow water to percolate upward slowly under low head to displace all entrapped pore air; purge manometer lines."},
                {"title": "Constant-Head Reservoir Elevation", "text": "Adjust overhead water tank height to establish initial hydraulic head difference Δh = 10.0 cm between manometer ports; allow steady seepage to establish for 5 minutes."},
                {"title": "Volumetric Flow Rate Measurement", "text": "Place dry graduated cylinder under the effluent outlet; start stopwatch simultaneously; collect outflow for 60 seconds; record collected volume V (cm³); calculate Q = V / t."},
                {"title": "Head Differential Sweep", "text": "Increase reservoir elevation to establish head differentials of 20.0, 30.0, 40.0, 50.0, and 60.0 cm; record steady discharge flow rate Q at each plateau."},
                {"title": "Temperature Correction & Permeability Calculation", "text": "Measure effluent water temperature T; plot Q versus Δh; evaluate slope to compute hydraulic conductivity k_T and standardize to 20 °C (k_20)."}
            ],
            "topics": [
                {"question": "State Darcy's Law and identify the conditions under which it remains strictly valid.", "answer": "Darcy's Law states Q = k · i · A; it is strictly valid for laminar fluid flow through saturated porous media where Reynolds number based on mean grain diameter is Re_p = (rho v D_50) / mu < 1 to 10; at higher velocities, inertial turbulence causes non-linear deviations."},
                {"question": "Why is the constant-head test preferred for coarse sands while the falling-head test is used for clays?", "answer": "Coarse sands have high permeability, discharging measurable volumes of water rapidly under constant head; fine-grained clays have extremely low permeability (k < 10^-6 cm/s), meaning flow under constant head is too slow to measure, requiring a falling-head standpipe."},
                {"question": "Why is de-aired water strictly required in laboratory permeability testing?", "answer": "Tap water contains dissolved air; under negative pressure gradients within soil voids, dissolved air comes out of solution as microscopic bubbles that lodge in pore throats, drastically reducing apparent permeability by up to 90%."},
                {"question": "How is measured hydraulic conductivity k_T standardized to the reference 20 °C baseline?", "answer": "Water viscosity decreases with temperature, increasing permeability; standardized conductivity is k_20 = k_T · (mu_T / mu_20), where mu is dynamic viscosity of water."},
                {"question": "What is Hazen's empirical formula relating hydraulic conductivity to grain size in sands?", "answer": "Allen Hazen established that k ≈ C · (D_10)^2 in cm/s, where D_10 is the effective grain size (in cm) passing 10% on the gradation curve, and C is Hazen's empirical coefficient (typically 100 to 150)."},
                {"question": "What is the physical distinction between discharge velocity v and seepage velocity v_s?", "answer": "Discharge velocity v = Q / A assumes flow occurs through the entire cross-section; seepage velocity v_s = v / n represents actual interstitial velocity through interconnected pore channels, where n is soil porosity (n < 1, so v_s > v)."}
            ],
            "precautions": [
                "Always saturate soil specimens from bottom to top under low hydraulic head to allow buoyant air bubbles to escape freely.",
                "Ensure flow velocities remain strictly within the laminar Darcy regime; avoid excessively steep hydraulic gradients (i > 2.0).",
                "Verify manometer piezometer lines are entirely free of air bubbles before recording differential head Δh.",
                "Maintain constant room temperature to prevent water density and dynamic viscosity fluctuations during flow logging."
            ],
            "quiz": [
                {
                    "question": "Darcy's Law for fluid flow through soil is expressed mathematically as:",
                    "options": ["Q = k · i^2 · A", "Q = k · i · A", "Q = k / (i · A)", "Q = k · A / i"],
                    "correct": 1,
                    "explanation": "Darcy's Law states discharge flow rate Q is directly proportional to hydraulic gradient i and area A: Q = k · i · A."
                },
                {
                    "question": "The hydraulic gradient i is defined as:",
                    "options": ["Total head divided by soil volume", "Piezometric head loss Δh divided by flow length L", "Flow rate divided by area", "Permeability divided by velocity"],
                    "correct": 1,
                    "explanation": "Hydraulic gradient is dimensionless head loss per unit length: i = Δh / L."
                },
                {
                    "question": "According to Hazen's formula, hydraulic conductivity of clean sand scales approximately with:",
                    "options": ["D_50", "(D_10)^2", "sqrt(D_60)", "(D_30)^3"],
                    "correct": 1,
                    "explanation": "Hazen's empirical formula is k ≈ C · (D_10)^2, scaling with the square of effective grain size D_10."
                },
                {
                    "question": "The constant-head permeability test is suitable primarily for which type of soil?",
                    "options": ["High-plasticity fat clays", "Organic peat and silts", "Clean sands and gravels (k > 10^-4 cm/s)", "Consolidated shale"],
                    "correct": 2,
                    "explanation": "Constant-head testing is used for coarse, permeable soils; clays require falling-head permeameters."
                }
            ],
            "samples": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
            "measureLabel": "Record discharge flow rate Q",
            "readings": ["flow_rate_cm3s", "delta_h_cm", "hyd_gradient", "k_calc_cms"],
            "theory": """<h3>1. Darcy's Law & Navier–Stokes Porous Media Homogenization</h3>
<p>Fluid seepage through granular soil represents low-Reynolds-number viscous flow through a tortuous three-dimensional network of interconnected pore channels. Homogenization of the creeping Navier–Stokes equations (Stokes flow) over a representative elementary volume (REV) leads directly to the macroscopic empirical transport relation discovered by Henry Darcy in 1856:</p>
\\[ v = - k \\nabla h \\]
<p>where $v = Q / A$ is the superficial discharge (Darcian) velocity (volume flux per unit cross-sectional area), $k$ is the hydraulic conductivity (coefficient of permeability), and $\\nabla h$ is the piezometric hydraulic head gradient. For one-dimensional steady seepage along coordinate $x$ through length $L$ under head difference $\\Delta h$:</p>
\\[ i = \\frac{\\Delta h}{L}, \\qquad v = k \\cdot i = k \\left( \\frac{\\Delta h}{L} \\right) \\]

<h3>2. Absolute (Intrinsic) Permeability Formulation</h3>
<p>Hydraulic conductivity $k$ depends upon both the geometric matrix structure of the soil and the physical properties of the permeant fluid. It is expressed in terms of intrinsic permeability $K$ (in $\\text{m}^2$ or Darcys):</p>
\\[ k = \\frac{K \\rho g}{\\mu} \\]
<p>where $\\rho$ is fluid density, $g$ is gravitational acceleration, and $\\mu$ is dynamic viscosity. Because water viscosity $\\mu(T)$ decreases rapidly with temperature ($-2.4\\%\\text{ per }^\\circ\\text{C}$), standard geotechnical practice normalizes experimental conductivity $k_T$ to $20.0^\\circ\\text{C}$:</p>
\\[ k_{20} = k_T \\left( \\frac{\\mu_T}{\\mu_{20}} \\right) \\]

<h3>3. Constant-Head Discharge Model</h3>
<p>The volumetric discharge flow rate $Q$ through a permeameter of cross-sectional area $A$ and manometer tap spacing $L$ is:</p>
\\[ Q = k \\cdot i \\cdot A = k \\left( \\frac{\\Delta h}{L} \\right) A = \\left[ \\frac{k A}{L} \\right] \\Delta h = S_k \\cdot \\Delta h \\]
<p>For permeameter dimensions $D = 7.50\\text{ cm}$ ($A = 44.1786\\text{ cm}^2$) and tap spacing $L = 15.0\\text{ cm}$:</p>
\\[ S_k = \\frac{k A}{L} = \\frac{0.49231 \\times 44.1786}{15.0} = 1.4500\\text{ cm}^2\\text{/s} \\]
<p>Plotting experimental discharge $Q$ versus head difference $\\Delta h$ yields a linear response whose slope directly provides hydraulic conductivity $k$.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this geotechnical engineering laboratory investigation is to verify Darcy's Law for steady-state laminar fluid seepage, determine the hydraulic conductivity ($k$) of clean uniform sand, and evaluate the discharge sensitivity slope $S_k$ using the constant-head permeameter according to ASTM D2434 / AASHTO T215 across six hydraulic head plateaus ($\\Delta h = 10.0\\text{ to }60.0\\text{ cm}$).</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Steady laminar seepage through a saturated porous soil column is governed by Darcy's Law:</p>
\\[ Q = k \\cdot i \\cdot A = k \\left( \\frac{\\Delta h}{L} \\right) A = S_k \\cdot \\Delta h \\]
<p>where $S_k = 1.4500\\text{ cm}^2\\text{/s}$ is the flow sensitivity slope and hydraulic conductivity is $k = S_k \\frac{L}{A}$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized a transparent acrylic constant-head permeameter conforming to ASTM D2434 (inside diameter $D = 7.50 \\pm 0.02\\text{ cm}$, area $A = 44.1786\\text{ cm}^2$, length between piezometer ports $L = 15.00 \\pm 0.05\\text{ cm}$) equipped with bronze porous end plates. Head difference $\\Delta h$ was maintained via an adjustable constant-head supply reservoir and monitored on a metric multi-tube glass piezometer board ($1.0\\text{ mm}$ resolution). Effluent water was collected in a $1000\\text{ mL}$ graduated glass cylinder timed with a digital quartz stopwatch ($0.01\\text{ s}$ resolution). Permeant temperature was logged using a digital RTD probe ($T = 20.0 \\pm 0.2^\\circ\\text{C}$).</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Oven-dried quartz sand was placed into the cell in three layers and tamped to porosity $n = 0.38$. The specimen was saturated from bottom to top with de-aired water for 30 minutes to purge air. The constant-head reservoir was adjusted to establish $\\Delta h = 10.0\\text{ cm}$. Outflow was collected for $60.0\\text{ s}$, and volume recorded. The procedure was repeated at $\\Delta h = 20.0, 30.0, 40.0, 50.0,$ and $60.0\\text{ cm}$, recording triplicate flow collections at each level.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Water spillage creates immediate slipping hazards around permeameter benches. Drainage collection troughs were inspected, and absorbent mats maintained beneath the test station. Operators wore slip-resistant laboratory footwear and safety glasses.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the hydraulic sweep at $T = 20.0^\\circ\\text{C}$ ($L = 15.0\\text{ cm}$, $A = 44.18\\text{ cm}^2$):</p>
<table>
<thead>
<tr><th>Trial</th><th>Head Diff Δh (cm)</th><th>Hydraulic Gradient i</th><th>Collection Time t (s)</th><th>Collected Volume V (cm³)</th><th>Discharge Flow Rate Q (cm³/s)</th><th>Calculated k (cm/s)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>10.0</td><td>0.667</td><td>60.0</td><td>870.0</td><td>14.50</td><td>0.4923</td></tr>
<tr><td>2</td><td>20.0</td><td>1.333</td><td>60.0</td><td>1740.0</td><td>29.00</td><td>0.4923</td></tr>
<tr><td>3</td><td>30.0</td><td>2.000</td><td>60.0</td><td>2610.0</td><td>43.50</td><td>0.4923</td></tr>
<tr><td>4</td><td>40.0</td><td>2.667</td><td>30.0</td><td>1740.0</td><td>58.00</td><td>0.4923</td></tr>
<tr><td>5</td><td>50.0</td><td>3.333</td><td>30.0</td><td>2175.0</td><td>72.50</td><td>0.4923</td></tr>
<tr><td>6</td><td>60.0</td><td>4.000</td><td>30.0</td><td>2610.0</td><td>87.00</td><td>0.4923</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of volumetric discharge flow rate $Q$ versus head difference $\\Delta h$ yields:</p>
\\[ Q = 1.45000 \\cdot \\Delta h + 0.00000 \\]
<p>with an extraordinary coefficient of determination $R^2 = 1.000000$. The experimental slope $S_k = 1.4500\\text{ cm}^2\\text{/s}$ matches the design benchmark with zero relative deviation ($0.00\\%$). Calculating hydraulic conductivity $k$:</p>
\\[ k = \\frac{S_k \\cdot L}{A} = \\frac{1.45000\\text{ cm}^2\\text{/s} \\times 15.00\\text{ cm}}{44.1786\\text{ cm}^2} = \\frac{21.7500}{44.1786} = 0.49232\\text{ cm/s} \\]
<p>Because testing was conducted at $T = 20.0^\\circ\\text{C}$, the viscosity correction factor is $\\mu_T / \\mu_{20} = 1.000$, yielding $k_{20} = 0.4923\\text{ cm/s}$ ($4.923 \\times 10^{-3}\\text{ m/s}$), characteristic of clean, coarse drainage sand.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include volume measurement $\\delta V = \\pm 5\\text{ mL}$ ($0.3\\%$), timing precision $\\delta t = \\pm 0.1\\text{ s}$ ($0.17\\%$), head measurement $\\delta (\\Delta h) = \\pm 0.1\\text{ cm}$ ($0.3\\%$), and area $\\delta A / A = 0.2\\%$. Propagating into $k$:</p>
\\[ \\frac{\\delta k}{k} = \\sqrt{ \\left( \\frac{\\delta V}{V} \\right)^2 + \\left( \\frac{\\delta t}{t} \\right)^2 + \\left( \\frac{\\delta \\Delta h}{\\Delta h} \\right)^2 + \\left( \\frac{\\delta A}{A} \\right)^2 + \\left( \\frac{\\delta L}{L} \\right)^2 } = \\pm 0.54\\% \\]
<p>The reported hydraulic conductivity is $k_{20} = 0.4923 \\pm 0.0027\\text{ cm/s}$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The flawless linearity between $Q$ and $\\Delta h$ validates Darcy's Law across hydraulic gradients up to $i = 4.0$. Evaluating pore Reynolds number at peak flow ($v = 87.0 / 44.18 = 1.97\\text{ cm/s}$, $D_{50} = 0.045\\text{ cm}$):</p>
\\[ Re_p = \\frac{\\rho v D_{50}}{\\mu} = \\frac{1.0 \\times 1.97 \\times 0.045}{0.010} = 8.86 < 10 \\]
<p>confirming that flow remained strictly within the laminar creeping regime without turbulent dissipation.</p>

<h3>10. Civil Geotechnical Seepage Applications</h3>
<p>In geotechnical design of dam drainage blankets, dewatering well-point systems, and porous highway sub-base courses, hydraulic conductivity dictates seepage capacity. A high conductivity of $0.492\\text{ cm/s}$ ensures rapid gravity drainage, preventing pore water pressure build-up and liquefaction under dynamic vehicle loading.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why does seepage velocity exceed discharge velocity in soil?</strong><br>
<em>A1:</em> Discharge velocity $v = Q/A$ calculates velocity as if the entire cross-section were open; however, water flows only through interconnected pore channels of area $A_v = n A$. Therefore, true interstitial seepage velocity is $v_s = v / n$, which is $2.5\\text{ to }3.0$ times faster.</p>
<p><strong>Q2: What causes piping failure in earth dams, and how does permeability relate to it?</strong><br>
<em>A2:</em> If the exit hydraulic gradient $i_{exit}$ exceeds the critical hydraulic gradient $i_{crit} = (G_s - 1)/(1 + e) \\approx 1.0$, seepage forces overcome the submerged weight of soil particles, fluidizing grains and eroding backward internal 'pipes' that breach the dam.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The constant-head permeability investigation validated Darcy's fundamental seepage law. The calibrated sensitivity slope $S_k = 1.4500\\text{ cm}^2\\text{/s}$ ($R^2 = 1.000000$) and verified hydraulic conductivity $k_{20} = 0.4923\\text{ cm/s}$ provide an authoritative parameter for seepage, filtration, and groundwater drainage design.</p>"""
        },
        {
            "number": 22,
            "slug": "one-dimensional-consolidation-oedometer-test",
            "title": "One-Dimensional Consolidation Properties of Cohesive Soil by Oedometer Testing",
            "shortTitle": "Oedometer Consolidation",
            "aim": "Determine the one-dimensional consolidation parameters—Compression Index (C_c), Recompression Index (C_r), Preconsolidation Pressure (σ'_p), and void ratio curve (e - log σ')—of saturated cohesive clay according to ASTM D2435 / BS 1377-5.",
            "inputLabel": "Effective Consolidation Stress σ'",
            "shortInput": "Stress σ'",
            "inputUnit": "kPa",
            "min": 50.0,
            "max": 800.0,
            "step": 50.0,
            "initial": 200.0,
            "inputDecimals": 0,
            "rawLabel": "Equilibrium Specimen Void Ratio e",
            "rawUnit": "ratio",
            "rawDecimals": 3,
            "xAxis": "Common logarithm of effective stress log10(σ')",
            "yAxis": "Specimen void ratio e",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.5,
            "emptyY": 1.5,
            "targetName": "Virgin Compression Index C_c",
            "target": "0.2850",
            "refValue": 0.2850,
            "resultUnit": "ratio/decade",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "e = -0.2850 · log10(σ') + 1.2500",
            "intro": "When heavy civil structures (such as skyscrapers, bridge piers, and highway embankments) are constructed over saturated cohesive clay deposits, building loads are initially carried entirely by the incompressible pore water, generating excess pore water pressure Δu. Over months, years, or decades, this excess pore pressure dissipates as water slowly squeezes out through microscopic clay pores under hydraulic gradients, transferring stress to the solid mineral skeleton and causing time-dependent primary consolidation settlement. Formulated by Karl von Terzaghi in 1925, one-dimensional consolidation is evaluated in the laboratory using the oedometer (consolidometer) test (ASTM D2435). An undisturbed cylindrical clay specimen is confined inside a rigid brass floating ring (typically 50 to 75 mm diameter, 20 mm initial height) between porous stones that permit double drainage. The rigid ring imposes zero lateral strain (ε_x = ε_y = 0), forcing all volumetric strain into vertical settlement: ε_v = ΔH / H_0. Axial consolidation pressure σ' is applied in standard load-increment ratios (LIR = 1.0, doubling stress every 24 hours: 25, 50, 100, 200, 400, 800 kPa). Plotting equilibrium void ratio e against log10(σ') yields the classic e - log σ' curve, characterized by an initial flat recompression curve below the preconsolidation stress σ'_p and a steep linear Virgin Compression Line defined by the Compression Index C_c = -de / d(log10 σ'). In this laboratory, consolidation tests are conducted across stress levels up to 800 kPa to evaluate C_c and calculate foundation settlement.",
            "modelExtra": "Medium-plasticity saturated clay (CL/CH). Initial void ratio e_0 = 1.050. Virgin compression slope C_c = 0.2850. Linearized regression relates void ratio e directly to common logarithm log10(σ') with intercept e_0* = 1.2500.",
            "apparatus": [
                {"name": "Fixed/Floating Ring Oedometer Consolidation Cell", "purpose": "Precision brass confining ring (63.5 mm diameter, 20.0 mm height) imposing zero lateral strain."},
                {"name": "Multi-Ratio Lever Arm Dead-Weight Consolidation Frame", "purpose": "Applies vertical axial stresses from 12.5 to 1600 kPa with 10:1 or 11:1 lever mechanical advantage."},
                {"name": "Sintered Bronze Porous Drainage Disks", "purpose": "High-permeability disks providing planar contact and top/bottom double drainage paths."},
                {"name": "Digital Linear Displacement Transducer (LVDT)", "purpose": "Monitors vertical consolidation settlement ΔH continuously with 0.001 mm resolution."},
                {"name": "Automated Computerized Data Logging Acquisition System", "purpose": "Logs time-settlement curves (square-root-t and log-t methods) across 24-hour cycles."},
                {"name": "Soil Trimming Turntable & Wire Saw", "purpose": "Trims undisturbed Shelby tube clay cores into the oedometer ring without structural disturbance."}
            ],
            "procedure": [
                {"title": "Specimen Trimming & Initial Characterization", "text": "Carefully trim an undisturbed clay core into the greased brass ring using a soil lathe and wire saw; strike ends flush; weigh ring and moist soil to 0.01 g; record initial height H_0 = 20.0 mm."},
                {"title": "Oedometer Cell Assembly", "text": "Place saturated lower porous stone and filter paper in the cell; seat ring with soil; place top filter paper, upper porous stone, and loading cap; center in loading frame."},
                {"title": "Seating Load & Water Inundation", "text": "Apply an initial seating load of 5.0 kPa; fill cell with water to prevent specimen desiccation; allow thermal and swelling equilibration for 1 hour; zero LVDT."},
                {"title": "Incremental 24-Hour Loading Schedule", "text": "Apply sequential load increments with LIR = 1.0 (50, 100, 200, 400, and 800 kPa); maintain each load for exactly 24 hours to achieve 100% primary consolidation."},
                {"title": "Time-Settlement Acquisition", "text": "Log vertical compression ΔH at standardized time intervals (0.1, 0.25, 0.5, 1, 2, 4, 8, 15, 30 min, 1, 2, 4, 8, 24 hr) for each load step."},
                {"title": "Dismantling & Final Void Ratio Calculation", "text": "Unload specimen; remove ring; dry soil in oven at 110 °C to determine dry mass M_s; compute height of solids H_s and equilibrium void ratio e at each pressure; plot e versus log10(σ') to extract C_c."}
            ],
            "topics": [
                {"question": "What is the physical significance of the Preconsolidation Pressure (σ'_p)?", "answer": "The preconsolidation pressure σ'_p represents the maximum effective overburden stress the soil deposit has experienced in its entire geologic history; it separates stiff, low-settlement overconsolidated behavior from soft, high-settlement normally consolidated behavior."},
                {"question": "How did Casagrande determine preconsolidation pressure graphically from the e - log σ' curve?", "answer": "Arthur Casagrande: (1) Find point of maximum curvature on e - log σ'; (2) Draw horizontal line; (3) Draw tangent to curve at that point; (4) Bisect angle between horizontal and tangent; (5) Project straight virgin compression line backward; the intersection with bisector gives σ'_p."},
                {"question": "Why is primary consolidation settlement in clays a time-dependent process?", "answer": "Clay pores are microscopic (< 1 µm), resulting in extremely low hydraulic conductivity (k ≈ 10^-8 cm/s); water escapes very slowly under excess pore pressure gradients, delaying volumetric strain according to Terzaghi's consolidation theory."},
                {"question": "How does the Compression Index C_c relate to soil plasticity according to Skempton's empirical formula?", "answer": "A. W. Skempton established for remolded clays: C_c ≈ 0.007 (LL - 10), and for undisturbed natural clays: C_c ≈ 0.009 (LL - 10), where LL is Liquid Limit in percent."},
                {"question": "What is the coefficient of consolidation c_v, and how is it determined experimentally?", "answer": "The coefficient of consolidation c_v = k / (m_v · gamma_w) governs the rate of pore pressure dissipation; it is determined from 24-hour time-settlement curves using either Casagrande's log-time method (t_50) or Taylor's square-root-time method (t_90)."},
                {"question": "What is secondary compression (creep) in cohesive soils?", "answer": "Secondary compression is the continued, slow volumetric deformation of clay that occurs at constant effective stress after all excess pore water pressure has dissipated, caused by viscous plastic rearrangement of adsorbed clay platelet structures."}
            ],
            "precautions": [
                "Ensure clay specimen is trimmed precisely to ring dimensions without gaps, gouges, or finger indentation remolding.",
                "Inundate specimen with water immediately after applying seating load to prevent air drying and capillary shrinkage.",
                "Apply loads smoothly without dynamic jar or shock that could liquefy or over-stress sensitive clay structures.",
                "Allow each load increment a full 24 hours to ensure dissipation of hydrodynamic excess pore water pressure."
            ],
            "quiz": [
                {
                    "question": "The slope of the straight-line portion of the e versus log10(σ') curve in normally consolidated clay is called:",
                    "options": ["Coefficient of consolidation (c_v)", "Compression Index (C_c)", "Modulus of subgrade reaction", "Coefficient of volume compressibility (m_v)"],
                    "correct": 1,
                    "explanation": "Compression Index C_c = -de / d(log10 σ') defines the slope of the virgin consolidation line."
                },
                {
                    "question": "Terzaghi's 1-D consolidation theory assumes that lateral strain in the soil is:",
                    "options": ["Zero (rigid lateral confinement)", "Equal to vertical strain", "Governed by Poisson's ratio", "Freely unconstrained"],
                    "correct": 0,
                    "explanation": "The rigid oedometer ring imposes zero lateral strain (ε_x = ε_y = 0), ensuring 1-D vertical deformation."
                },
                {
                    "question": "A soil deposit whose current effective overburden stress equals its historical maximum effective stress is:",
                    "options": ["Overconsolidated (OCR > 1)", "Normally consolidated (OCR = 1)", "Underconsolidated (OCR < 1)", "Liquefied"],
                    "correct": 1,
                    "explanation": "When current effective stress equals preconsolidation stress (σ'_0 = σ'_p), the Overconsolidation Ratio is OCR = 1 (normally consolidated)."
                },
                {
                    "question": "According to Skempton's empirical formula for undisturbed clays, if Liquid Limit is 50%, C_c is approximately:",
                    "options": ["0.18", "0.27", "0.36", "0.54"],
                    "correct": 2,
                    "explanation": "C_c = 0.009 (LL - 10) = 0.009 (50 - 10) = 0.009 · 40 = 0.36."
                }
            ],
            "samples": [50.0, 100.0, 200.0, 400.0, 800.0],
            "measureLabel": "Record equilibrium specimen void ratio e",
            "readings": ["void_ratio_e", "effective_stress_kpa", "log_stress", "settlement_mm"],
            "theory": """<h3>1. Terzaghi's One-Dimensional Consolidation Theory</h3>
<p>Consider a saturated cohesive clay stratum of thickness $2H_{dr}$ confined between pervious sand drainage boundaries. Applying a uniform surface pressure increment $\\Delta \\sigma$ immediately generates equal excess pore water pressure $\\Delta u = \\Delta \\sigma$. As water drains vertically along coordinate $z$, Terzaghi's governing hydrodynamic diffusion equation dictates:</p>
\\[ \\frac{\\partial u}{\\partial t} = c_v \\frac{\\partial^2 u}{\\partial z^2} \\]
<p>where $c_v$ is the coefficient of consolidation (in $\\text{m}^2/\\text{s}$):</p>
\\[ c_v = \\frac{k}{\\rho_w g \\cdot m_v} = \\frac{k(1 + e_0)}{\\rho_w g \\cdot a_v} \\]
<p>where $k$ is hydraulic conductivity, $m_v$ is coefficient of volume compressibility, and $a_v = -de/d\\sigma'$ is coefficient of compressibility.</p>

<h3>2. Phase Relations & The Height-of-Solids Method</h3>
<p>In an oedometer specimen of initial cross-sectional area $A$ and initial height $H_0$, the equivalent height of solid mineral grains $H_s$ is an invariant constant computed from dry oven mass $M_s$ and specific gravity $G_s$:</p>
\\[ H_s = \\frac{M_s}{A \\cdot G_s \\cdot \\rho_w} \\]
<p>At any stage of consolidation where measured cumulative vertical settlement is $\\Delta H$, the current specimen height is $H = H_0 - \\Delta H$. The current void ratio $e$ is evaluated directly:</p>
\\[ e = \\frac{H - H_s}{H_s} = \\frac{H_v}{H_s} \\]

<h3>3. The Virgin Compression Line & Settlement Calculation</h3>
<p>When effective consolidation stress $\\sigma'$ exceeds the preconsolidation pressure $\\sigma'_p$, the soil deforms along the Virgin Compression Line (VCL):</p>
\\[ e = e_0^* - C_c \\log_{10}\\left( \\frac{\\sigma'}{\\sigma_0'} \\right) \\]
<p>where $C_c = 0.2850\\text{ ratio/decade}$ is the Virgin Compression Index and $e_0^* = 1.2500$. Total primary consolidation settlement $S_c$ of a field clay layer of thickness $H$ under foundation stress increment $\\Delta \\sigma$ is calculated as:</p>
\\[ S_c = \\frac{C_c \\cdot H}{1 + e_0} \\log_{10}\\left( \\frac{\\sigma'_0 + \\Delta \\sigma}{\\sigma'_0} \\right) \\]""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this geotechnical engineering laboratory investigation is to evaluate the one-dimensional consolidation parameters—Compression Index ($C_c$), Recompression Index ($C_r$), and void ratio trajectory ($e - \\log_{10} \\sigma'$)—of an undisturbed saturated clay specimen using the oedometer apparatus according to ASTM D2435 / BS 1377-5 across five effective stress increments ($50\\text{ to }800\\text{ kPa}$).</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Along the normally consolidated virgin compression line, equilibrium void ratio $e$ varies linearly with the common logarithm of effective stress $\\sigma'$:</p>
\\[ e = - C_c \\cdot \\log_{10}(\\sigma') + e_0^* \\]
<p>where $C_c = 0.2850\\text{ ratio/decade}$ is the Virgin Compression Index and $e_0^* = 1.2500$ is the reference intercept.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized a fixed-ring consolidation cell with stainless steel floating ring ($63.50 \\pm 0.05\\text{ mm}$ internal diameter, initial height $H_0 = 20.00 \\pm 0.02\\text{ mm}$, cross-sectional area $A = 31.67\\text{ cm}^2$). Axial load was applied using a $10:1$ dead-weight lever arm consolidation frame. Vertical deformation was monitored with a digital LVDT ($0.001\\text{ mm}$ resolution) connected to an automated continuous acquisition logger. The soil was undisturbed saturated silty clay ($G_s = 2.70$, initial moisture $w_0 = 38.5\\%$, initial void ratio $e_0 = 1.050$).</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>The clay specimen was trimmed into the ring, weighed, mounted between soaked porous stones in the oedometer, inundated with water, and an initial seating stress of $5.0\\text{ kPa}$ applied. Incremental vertical stresses of $50, 100, 200, 400,$ and $800\\text{ kPa}$ were applied sequentially at $24\\text{-hour}$ intervals (load-increment ratio $LIR = 1.0$). Settlement $\\Delta H$ was logged at standardized time intervals. After $800\\text{ kPa}$, the sample was unloaded, dried at $110^\\circ\\text{C}$ to determine $M_s = 81.42\\text{ g}$, and height of solids computed ($H_s = 9.524\\text{ mm}$).</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>High lever loads ($800\\text{ kPa} \\approx 253\\text{ kg}$ on hanger) pose crushing hazards. Operators loaded slotted weights with two hands, keeping feet clear of hanger pans. Safety lock pins were engaged when altering weight configurations.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the 24-hour consolidation stages ($H_s = 9.524\\text{ mm}$, $H_0 = 20.00\\text{ mm}$):</p>
<table>
<thead>
<tr><th>Load Increment</th><th>Effective Stress σ' (kPa)</th><th>log10(σ')</th><th>24-hr Settlement ΔH (mm)</th><th>Current Height H (mm)</th><th>Equilibrium Void Ratio e</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>50.0</td><td>1.6990</td><td>2.703</td><td>17.297</td><td>0.766</td></tr>
<tr><td>2</td><td>100.0</td><td>2.0000</td><td>3.518</td><td>16.482</td><td>0.680</td></tr>
<tr><td>3</td><td>200.0</td><td>2.3010</td><td>4.333</td><td>15.667</td><td>0.594</td></tr>
<tr><td>4</td><td>400.0</td><td>2.6021</td><td>5.148</td><td>14.852</td><td>0.509</td></tr>
<tr><td>5</td><td>800.0</td><td>2.9031</td><td>5.963</td><td>14.037</td><td>0.423</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of equilibrium void ratio $e$ versus common logarithm of effective stress $x = \\log_{10}(\\sigma')$ yields:</p>
\\[ e = -0.28500 \\cdot \\log_{10}(\\sigma') + 1.25000 \\]
<p>with an exceptional coefficient of determination $R^2 = 1.000000$. The absolute experimental slope $C_c = 0.2850\\text{ ratio/decade}$ matches the reference design benchmark ($0.2850$) with zero relative deviation ($0.00\\%$). Skempton's correlation for natural clay ($C_c = 0.009(LL - 10)$) predicts $LL = (0.285 / 0.009) + 10 = 41.7\\%$, fully consistent with the medium-plasticity clay classification.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include LVDT settlement resolution $\\delta (\\Delta H) = \\pm 0.002\\text{ mm}$, dry mass balance $\\delta M_s = \\pm 0.01\\text{ g}$, and ring diameter $\\delta D = \\pm 0.05\\text{ mm}$. Propagating into void ratio $e = (H - H_s) / H_s$:</p>
\\[ \\delta e = \\sqrt{ \\left( \\frac{\\delta \\Delta H}{H_s} \\right)^2 + \\left( \\frac{H \\delta H_s}{H_s^2} \\right)^2 } = \\pm 0.0025 \\]
<p>The reported Virgin Compression Index is $C_c = 0.2850 \\pm 0.0018\\text{ ratio/decade}$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The specimen exhibited classic normally consolidated behavior above $50\\text{ kPa}$. Over the stress range from $50\\text{ to }800\\text{ kPa}$, specimen height compressed by $5.96\\text{ mm}$ ($29.8\\%$ axial strain), reducing void ratio from $1.050$ to $0.423$. Squeezing out pore water reduced the distance between clay platelets, densifying the matrix and increasing shear strength.</p>

<h3>10. Structural Foundation Settlement Applications</h3>
<p>For a building foundation imposing $\\Delta \\sigma = 150\\text{ kPa}$ onto a $6.0\\text{ m}$ thick clay stratum with initial overburden $\\sigma'_0 = 100\\text{ kPa}$ ($e_0 = 1.050$), total expected primary consolidation settlement is:</p>
\\[ S_c = \\frac{C_c \\cdot H}{1 + e_0} \\log_{10}\\left( \\frac{\\sigma'_0 + \\Delta \\sigma}{\\sigma'_0} \\right) = \\frac{0.285 \\times 6000\\text{ mm}}{1 + 1.050} \\log_{10}\\left( \\frac{100 + 150}{100} \\right) = 834.1 \\times 0.3979 = 331.9\\text{ mm} \\]
<p>This demonstrates the massive scale of clay consolidation settlement and the necessity of preloading or deep pile foundations.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is vertical drainage path length $H_{dr}$ halved in double-drained oedometer testing?</strong><br>
<em>A1:</em> Porous stones at both top and bottom mean the maximum drainage distance for water at specimen mid-height is $H_{dr} = H / 2$. Because consolidation time scales with $H_{dr}^2$ ($t = T_v H_{dr}^2 / c_v$), double drainage accelerates laboratory consolidation by a factor of four ($4\\times$).</p>
<p><strong>Q2: What is the effect of sample disturbance on the measured e - log σ' curve?</strong><br>
<em>A2:</em> Disturbance destroys the delicate cemented clay structure, rounding the transition curve, obscuring preconsolidation pressure $\sigma'_p$, and artificially depressing the apparent Virgin Compression Index $C_c$.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The one-dimensional oedometer consolidation investigation accurately characterized the volumetric compressibility of the cohesive clay. The calibrated Virgin Compression Index $C_c = 0.2850\\text{ ratio/decade}$ ($R^2 = 1.000000$) provides a verified, precise standard for geotechnical foundation settlement calculations and embankment design.</p>"""
        },
        {
            "number": 23,
            "slug": "unconfined-compressive-strength-cohesive-soil",
            "title": "Unconfined Compressive Strength & Undrained Shear Strength of Cohesive Soil",
            "shortTitle": "Unconfined Compression Test",
            "aim": "Determine the unconfined compressive strength (q_u), undrained shear strength (c_u), and stress-strain deformation modulus (E_u) of undisturbed and remolded cohesive soil according to ASTM D2166 / AASHTO T208.",
            "inputLabel": "Axial Compressive Strain ε",
            "shortInput": "Axial Strain",
            "inputUnit": "%",
            "min": 1.0,
            "max": 6.0,
            "step": 1.0,
            "initial": 3.0,
            "inputDecimals": 1,
            "rawLabel": "Axial Deviator Stress σ_d",
            "rawUnit": "kPa",
            "rawDecimals": 1,
            "xAxis": "Axial strain ε (%)",
            "yAxis": "Axial compressive stress σ_d (kPa)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 7.0,
            "emptyY": 200.0,
            "targetName": "Undrained Elastic Modulus Slope",
            "target": "28.5000",
            "refValue": 28.5000,
            "resultUnit": "kPa/%",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "σ_d = 28.5000 · ε",
            "intro": "The Unconfined Compressive Strength (UCS) test provides the most rapid, economical, and widely used laboratory method for determining the undrained shear strength (c_u) of cohesive fine-grained soils. Standardized under ASTM D2166, the test is a special limiting case of the unconsolidated-undrained (UU) triaxial compression test where confining cell pressure is zero (σ_3 = 0). A cylindrical undisturbed cohesive soil specimen (typically 38 mm or 50 mm diameter, with standard length-to-diameter aspect ratio L/D = 2.0 to 2.5) is mounted between flat end platens and loaded axially in compression without lateral lateral restraint. Loading is applied at a rapid strain rate of 0.5% to 2.0% per minute so that testing is completed within 10 to 15 minutes, ensuring that zero water can drain from low-permeability clay pores (undrained condition). As axial compressive force P increases, axial strain ε = ΔL / L_0 increases, and cross-sectional area expands from initial area A_0 to corrected area A = A_0 / (1 - ε). Deviator stress σ_d = P / A rises to a peak unconfined compressive strength q_u. According to the Mohr–Coulomb failure criterion for total stress with friction angle ϕ_u = 0, the Mohr circle passes through the origin (σ_3 = 0) and has diameter q_u. Consequently, the undrained shear strength is exactly half the unconfined compressive strength: c_u = q_u / 2. In this laboratory, cohesive soil specimens are tested across axial strains from 1% to 6% to calibrate the undrained modulus E_u and evaluate undrained shear strength c_u.",
            "modelExtra": "Undisturbed silty clay specimen (diameter D_0 = 38.0 mm, length L_0 = 76.0 mm). Peak UCS q_u = 171.0 kPa, undrained shear strength c_u = q_u / 2 = 85.5 kPa. Linearized initial elastic response relates deviator stress σ_d to strain ε with slope 28.5000 kPa/% (E_u = 2.850 MPa).",
            "apparatus": [
                {"name": "Motorized Unconfined Compression Testing Machine", "purpose": "Applies constant vertical strain rate (0.5 to 2.0 mm/min) with electronic load cell monitoring force P."},
                {"name": "Precision Electronic S-Type Load Cell", "purpose": "Measures compressive force up to 5.0 kN with 0.5 N resolution and digital display."},
                {"name": "Digital Linear Displacement Transducer (LVDT)", "purpose": "Measures vertical axial specimen deformation ΔL to 0.001 mm precision."},
                {"name": "Soil Specimen Trimming Lathe & Wire Saw", "purpose": "Trims cylindrical specimens to exact 38.0 mm diameter and 76.0 mm height."},
                {"name": "Precision Vernier Calipers & Analytical Balance", "purpose": "Measures specimen diameter, length, and wet weight to 0.01 mm and 0.01 g."},
                {"name": "Thermostatic Drying Oven", "purpose": "Maintains 110 ± 5 °C for post-test moisture content determination."}
            ],
            "procedure": [
                {"title": "Specimen Trimming & Dimensional Verification", "text": "Trim an undisturbed cohesive soil core to 38.0 mm diameter and 76.0 mm height (L/D = 2.0) on the soil lathe; measure diameter at ends and middle; record initial length L_0 and mass M_0."},
                {"title": "Platen Alignment & Machine Centering", "text": "Place specimen centrally on lower platen of the UCS machine; raise platen until upper spherical bearing platen just makes contact; zero load cell and LVDT channels."},
                {"title": "Strain-Controlled Axial Compression", "text": "Engage motorized drive at a constant deformation rate of 1.0 mm/min (~1.3% strain/min); record compressive load P and axial deformation ΔL at 15-second intervals."},
                {"title": "Cross-Sectional Area Correction", "text": "Calculate axial strain ε = ΔL / L_0; compute corrected cross-sectional area A = A_0 / (1 - ε) at each interval assuming constant specimen volume."},
                {"title": "Failure Point Identification", "text": "Continue loading until compressive load P peaks and begins dropping, or until axial strain reaches 15%; record peak load P_max and unconfined compressive strength q_u."},
                {"title": "Fracture Angle Inspection & Moisture Testing", "text": "Sketch failure mode (single diagonal shear plane vs bulging barrel); measure shear failure angle θ; dry specimen in oven at 110 °C to determine moisture content w."}
            ],
            "topics": [
                {"question": "Why is undrained shear strength c_u equal to exactly half of the unconfined compressive strength (q_u / 2)?", "answer": "In unconfined compression, minor principal stress is zero (sigma_3 = 0) and major principal stress at failure is sigma_1 = q_u; for saturated clay under rapid loading, friction angle is zero (phi_u = 0), so the Mohr circle radius equals c_u = (sigma_1 - sigma_3) / 2 = q_u / 2."},
                {"question": "Why must the cross-sectional area be corrected as A = A_0 / (1 - ε) during compressive loading?", "answer": "In undrained saturated clay, water cannot escape and soil solids are incompressible, meaning total specimen volume remains constant (A_0 L_0 = A L); as length shortens to L = L_0 (1 - ε), area expands to A = A_0 / (1 - ε)."},
                {"question": "Why is the unconfined compression test completely invalid for clean dry sands?", "answer": "Clean sand has zero cohesion (c = 0); without lateral confining pressure (sigma_3 = 0), a dry sand cylinder has zero shear strength (tau_f = sigma_3 tan phi = 0) and collapses under its own self-weight into a loose heap."},
                {"question": "What is soil sensitivity (S_t) and how is it evaluated using the UCS test?", "answer": "Sensitivity is S_t = q_u (undisturbed) / q_u (remolded at identical moisture); sensitive marine clays possess S_t = 4 to 8, and quick clays exceed 16, losing virtually all shear strength upon remolding or seismic shaking."},
                {"question": "How does the specimen aspect ratio (L/D = 2.0 to 2.5) influence unconfined compressive strength?", "answer": "Platen friction restrains lateral expansion at cylinder ends, creating conical confining zones; an aspect ratio L/D ≥ 2.0 ensures the central region is free from platen restraint, permitting an unconstrained 45° failure plane."},
                {"question": "What typical failure modes are observed in unconfined compression testing?", "answer": "Stiff, fissured, or overconsolidated clays fail along a clean, well-defined diagonal shear plane inclined at θ ≈ 45° to 60°; soft, normally consolidated clays fail by plastic bulging into a barrel shape."}
            ],
            "precautions": [
                "Maintain rapid testing speed (completed within 10 to 15 minutes) to ensure truly undrained conditions without moisture evaporation.",
                "Ensure cylinder ends are trimmed perfectly flat, parallel to each other, and perpendicular to the longitudinal axis.",
                "Always apply the area correction formula A = A_0 / (1 - ε); using uncorrected initial area A_0 introduces up to 15% error in q_u.",
                "Handle undisturbed clay cores with extreme care to prevent microstructural disturbance that artificially lowers strength."
            ],
            "quiz": [
                {
                    "question": "For saturated clay tested in unconfined compression, undrained shear strength c_u is related to peak compressive strength q_u by:",
                    "options": ["c_u = q_u", "c_u = q_u / 2", "c_u = 2 q_u", "c_u = q_u · tan(45°)"],
                    "correct": 1,
                    "explanation": "Because minor principal stress is zero (σ_3 = 0), the radius of the Mohr failure circle is c_u = (q_u - 0) / 2 = q_u / 2."
                },
                {
                    "question": "The standard length-to-diameter (L/D) aspect ratio for an unconfined compression soil specimen is:",
                    "options": ["0.5 to 1.0", "1.0 to 1.5", "2.0 to 2.5", "4.0 to 5.0"],
                    "correct": 2,
                    "explanation": "ASTM D2166 specifies an aspect ratio of 2.0 to 2.5 to eliminate platen end-restraint effects at mid-height."
                },
                {
                    "question": "If initial area is A_0 and axial strain is ε, the corrected cross-sectional area A during undrained compression is:",
                    "options": ["A = A_0 · (1 - ε)", "A = A_0 / (1 - ε)", "A = A_0 · (1 + ε)", "A = A_0 / (1 + ε)"],
                    "correct": 1,
                    "explanation": "By conservation of volume (V = A · L = A_0 · L_0), A = A_0 · [L_0 / L] = A_0 / (1 - ε)."
                },
                {
                    "question": "A soil with a sensitivity ratio S_t of 10 is classified as:",
                    "options": ["Insensitive", "Slightly sensitive", "Sensitive to very sensitive", "Cohesionless"],
                    "correct": 2,
                    "explanation": "Soils with S_t between 8 and 16 are classified as very sensitive clays, losing substantial strength upon remolding."
                }
            ],
            "samples": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "measureLabel": "Record axial deviator stress σ_d",
            "readings": ["stress_kpa", "strain_pct", "load_n", "corrected_area_cm2"],
            "theory": """<h3>1. Total Stress Analysis & The ϕ_u = 0 Concept</h3>
<p>When saturated cohesive clay is subjected to rapid external loading without allowing pore water drainage, the soil responds under undrained total stress conditions. Because water is practically incompressible relative to the soil skeleton, any increase in confining pressure $\\Delta \\sigma_3$ is transferred entirely to pore water pressure ($\\Delta u = \\Delta \\sigma_3$), meaning effective stress remains completely unchanged. Consequently, the undrained friction angle on a total stress basis is identically zero ($\\phi_u = 0$).</p>

<h3>2. Mohr Circle at Failure in Unconfined Compression</h3>
<p>In unconfined compression, minor principal total stress is atmospheric: $\\sigma_3 = 0$. The major principal total stress at peak load is $\\sigma_1 = q_u$. The Mohr failure envelope is a horizontal line of constant shear stress $\\tau = c_u$. The single Mohr circle has center at $C = (q_u / 2, 0)$ and radius $R = q_u / 2$. Therefore:</p>
\\[ c_u = R = \\frac{\\sigma_1 - \\sigma_3}{2} = \\frac{q_u - 0}{2} = \\frac{q_u}{2} \\]

<h3>3. Cross-Sectional Area Correction for Bulging</h3>
<p>Because saturated clay maintains constant volume during undrained deformation ($V = A_0 L_0 = A L$), axial shortening produces lateral radial expansion (bulging). When axial strain reaches $\\varepsilon = \\Delta L / L_0$, the current length is $L = L_0(1 - \\varepsilon)$. The average corrected cross-sectional area $A$ is:</p>
\\[ A = \\frac{V}{L} = \\frac{A_0 L_0}{L_0(1 - \\varepsilon)} = \\frac{A_0}{1 - \\varepsilon} \\]
<p>The true axial deviator stress $\\sigma_d$ is evaluated as:</p>
\\[ \\sigma_d = \\frac{P}{A} = \\frac{P (1 - \\varepsilon)}{A_0} \\]

<h3>4. Linear Elastic Modulus Model</h3>
<p>In the pre-failure deformation domain ($\\varepsilon = 1.0\\%\\text{ to }6.0\\%$), deviator stress scales linearly with strain:</p>
\\[ \\sigma_d = E_{slope} \\cdot \\varepsilon \\]
<p>where $E_{slope} = 28.5000\\text{ kPa/\\%}$. In standard units, undrained Young's modulus is $E_u = 28.50\\text{ kPa}/0.01 = 2850\\text{ kPa} = 2.850\\text{ MPa}$. Peak UCS reaches $q_u = 171.0\\text{ kPa}$, corresponding to undrained shear strength $c_u = 85.50\\text{ kPa}$.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this geotechnical engineering laboratory investigation is to evaluate the unconfined compressive strength ($q_u$), undrained shear strength ($c_u$), and undrained deformation modulus ($E_u$) of an undisturbed cohesive silty clay specimen according to ASTM D2166 / AASHTO T208. By monitoring axial deviator stress across six strain increments ($\varepsilon = 1.0\\%\\text{ to }6.0\\%$) with cross-sectional area correction, we determine the undrained modulus slope $E_{slope}$ and evaluate foundation bearing capacity.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>At each strain level $\\varepsilon$, deviator stress is computed using the constant-volume area correction:</p>
\\[ \\sigma_d = \\frac{P}{A} = \\frac{P (1 - \\varepsilon)}{A_0} \\]
<p>In the linear pre-peak domain, deviator stress relates to axial strain via the modulus slope:</p>
\\[ \\sigma_d = E_{slope} \\cdot \\varepsilon \\]
<p>where $E_{slope} = 28.5000\\text{ kPa/\\%}$. Undrained shear strength is $c_u = q_u / 2$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized an electromechanical unconfined compression testing machine equipped with a precision S-type load cell ($5.0\\text{ kN}$ capacity, precision $\\pm 0.5\\text{ N}$) and a digital LVDT ($0.001\\text{ mm}$ resolution). Deformation was applied at a constant strain-controlled rate of $1.0\\text{ mm/min}$ ($1.31\\%\\text{ strain/min}$). The test specimen was an undisturbed cylindrical silty clay core ($D_0 = 38.00 \\pm 0.05\\text{ mm}$, $L_0 = 76.00 \\pm 0.10\\text{ mm}$, initial area $A_0 = 11.341\\text{ cm}^2 = 1.1341 \\times 10^{-3}\\text{ m}^2$, initial wet density $\\rho_{wet} = 1.885\\text{ g/cm}^3$, moisture $w = 26.4\\%$).</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>The specimen was trimmed on a soil lathe, dimensions verified, and positioned between flat steel platens on the UCS machine. Platen contact was zeroed. Axial displacement was applied continuously at $1.0\\text{ mm/min}$, logging compressive force $P$ and axial displacement $\\Delta L$ every 15 seconds. Corrected area $A = A_0 / (1 - \\varepsilon)$ and deviator stress $\\sigma_d$ were calculated at each step up to peak failure stress.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Motorized compression machines present pinch risks between moving platens. Operators kept hands clear of platens during motor operation. Safety glasses and laboratory coats were worn during all soil trimming and testing operations.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the pre-failure loading trajectory ($A_0 = 11.341\\text{ cm}^2$):</p>
<table>
<thead>
<tr><th>Step</th><th>Axial Strain ε (%)</th><th>Corrected Area A (cm²)</th><th>Measured Compressive Load P (N)</th><th>Deviator Stress σ_d (kPa)</th><th>Deformation State</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>1.0</td><td>11.456</td><td>32.6</td><td>28.5</td><td>Linear Elastic Response</td></tr>
<tr><td>2</td><td>2.0</td><td>11.572</td><td>66.0</td><td>57.0</td><td>Linear Elastic Response</td></tr>
<tr><td>3</td><td>3.0</td><td>11.692</td><td>100.0</td><td>85.5</td><td>Linear Elastic Response</td></tr>
<tr><td>4</td><td>4.0</td><td>11.814</td><td>134.7</td><td>114.0</td><td>Linear Elastic Response</td></tr>
<tr><td>5</td><td>5.0</td><td>11.938</td><td>170.1</td><td>142.5</td><td>Pre-Peak Straining</td></tr>
<tr><td>6</td><td>6.0</td><td>12.065</td><td>206.3</td><td>171.0</td><td>Peak Failure (q_u = 171.0 kPa)</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of axial deviator stress $\\sigma_d$ versus axial strain $\\varepsilon$ yields:</p>
\\[ \\sigma_d = 28.50000 \\cdot \\varepsilon + 0.00000 \\]
<p>with an exceptional coefficient of determination $R^2 = 1.000000$. The experimental modulus slope $E_{slope} = 28.5000\\text{ kPa/\\%}$ matches the design benchmark with zero relative deviation ($0.00\\%$). Evaluating undrained elastic modulus $E_u$:</p>
\\[ E_u = 28.5000\\text{ kPa}/(0.01) = 2850.0\\text{ kPa} = 2.850\\text{ MPa} \\]
<p>Peak unconfined compressive strength is $q_u = 171.0\\text{ kPa}$, yielding undrained shear strength:</p>
\\[ c_u = \\frac{q_u}{2} = \\frac{171.0}{2} = 85.50\\text{ kPa} \\]
<p>The specimen classifies as a stiff cohesive clay ($c_u = 75\\text{ to }150\\text{ kPa}$).</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include load cell precision $\\delta P = \\pm 0.5\\text{ N}$, LVDT strain $\\delta \\varepsilon = \\pm 0.05\\%$, and initial area $\\delta A_0 / A_0 = \\pm 0.25\\%$. Propagating into $c_u$:</p>
\\[ \\frac{\\delta c_u}{c_u} = \\sqrt{ \\left( \\frac{\\delta P}{P} \\right)^2 + \\left( \\frac{\\delta A}{A} \\right)^2 } = \\pm 0.42\\% \\]
<p>The reported undrained shear strength is $c_u = 85.50 \\pm 0.36\\text{ kPa}$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The specimen failed along a well-defined diagonal shear rupture plane inclined at $\\theta = 56^\\circ$ to the horizontal, characteristic of overconsolidated silty clay with internal structure. Post-test remolding and retesting of the clay at identical moisture content yielded remolded strength $q_{u,rem} = 42.8\\text{ kPa}$, indicating a sensitivity ratio $S_t = 171.0 / 42.8 = 4.0$, classifying the deposit as moderately sensitive.</p>

<h3>10. Foundation Bearing Capacity Applications</h3>
<p>Under Skempton and Terzaghi bearing capacity theory for shallow strip footings on saturated clay under undrained conditions ($\phi_u = 0, N_c = 5.14, N_q = 1.0, N_\\gamma = 0$):</p>
\\[ q_{ult} = c_u N_c + q = 85.50 \\times 5.14 + q = 439.5\\text{ kPa} + q \\]
<p>Applying a safety factor $FS = 3.0$ yields a net allowable bearing pressure of $q_{all} = 146.5\\text{ kPa}$, confirming adequate foundation support for multi-story residential structures.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is testing completed within 10 to 15 minutes in the UCS test?</strong><br>
<em>A1:</em> Rapid loading guarantees undrained conditions; if testing were extended over hours, pore water would drain from the edges, causing dissipation of pore pressure and invalidating the $\phi_u = 0$ total stress assumption.</p>
<p><strong>Q2: Why does an inclined shear plane form at an angle θ > 45° if ϕ_u = 0?</strong><br>
<em>A2:</em> While total stress analysis assumes $\phi_u = 0$, the actual physical failure plane is governed by effective stress parameters: $\theta = 45^\\circ + \\phi'/2$. For effective friction angle $\phi' \\approx 22^\\circ$, $\\theta = 45^\\circ + 11^\\circ = 56^\\circ$, matching observed failure plane geometry.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The unconfined compressive strength test accurately evaluated the undrained shear strength of the cohesive soil. The verified modulus slope $E_{slope} = 28.5000\\text{ kPa/\\%}$ ($R^2 = 1.000000$), peak strength $q_u = 171.0\\text{ kPa}$, and undrained shear strength $c_u = 85.50\\text{ kPa}$ provide an authoritative standard for foundation bearing capacity design.</p>"""
        },
        {
            "number": 24,
            "slug": "triaxial-consolidated-undrained-shear-test",
            "title": "Triaxial Consolidated-Undrained (CU) Shear Testing with Pore-Water Pressure Measurement",
            "shortTitle": "Triaxial CU Shear Test",
            "aim": "Determine the effective stress shear strength parameters (c', ϕ') and pore pressure parameter (A) of saturated cohesive soil using the triaxial consolidated-undrained (CU) compression test with pore pressure measurement according to ASTM D4767 / BS 1377-8.",
            "inputLabel": "Effective Confining Pressure σ'_3",
            "shortInput": "Confining σ'_3",
            "inputUnit": "kPa",
            "min": 100.0,
            "max": 400.0,
            "step": 75.0,
            "initial": 250.0,
            "inputDecimals": 0,
            "rawLabel": "Peak Deviator Stress q_f",
            "rawUnit": "kPa",
            "rawDecimals": 1,
            "xAxis": "Effective confining pressure σ'_3 (kPa)",
            "yAxis": "Peak deviator stress q_f = (σ_1 - σ_3)_f (kPa)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 450.0,
            "emptyY": 650.0,
            "targetName": "Triaxial Failure Slope M",
            "target": "1.3500",
            "refValue": 1.3500,
            "resultUnit": "ratio",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "q_f = 1.3500 · σ'_3 + 45.0000",
            "intro": "The triaxial shear test is universally recognized as the most versatile, rigorous, and definitive laboratory method for evaluating the shear strength, pore pressure response, and stress-strain-volume constitutive behavior of soils. In contrast to direct shear box testing, the triaxial test subjects a cylindrical specimen to true axisymmetric stress states (σ_1 > σ_2 = σ_3), controls drainage independently from top and bottom boundaries, permits artificial saturation via back-pressure, and measures pore water pressure u continuously under closed undrained shear. Under ASTM D4767, the Consolidated-Undrained (CU) triaxial test proceeds in three consecutive stages: (1) Back-pressure saturation—specimen and pore lines are pressurized simultaneously while maintaining low effective stress until Skempton's B-parameter B = Δu / Δσ_3 ≥ 0.95, confirming 100% saturation; (2) Isotropic consolidation—cell pressure is elevated to target effective confining stress σ'_3 = σ_3 - u_0 with drainage valves open until excess pore pressure dissipates completely; and (3) Undrained axial shearing—drainage valves are closed, and axial deviator stress q = σ_1 - σ_3 is applied via a motorized loading ram at a controlled slow strain rate (typically 0.05% to 0.1%/min) while an electronic pressure transducer logs pore-water pressure u. Plotting peak deviator stress q_f versus effective confining pressure σ'_3 establishes the p'-q failure envelope, from which effective cohesion c' and effective friction angle ϕ' are deduced. In this laboratory, CU triaxial tests are conducted across effective confining stresses from 100 to 400 kPa to calibrate the failure slope M.",
            "modelExtra": "Medium-stiff saturated silty clay (CL). Effective stress parameters: effective friction angle ϕ' = 28.5°, effective cohesion c' = 15.0 kPa. Stress path failure slope M = 6 sin ϕ' / (3 - sin ϕ') = 1.3500, intercept = 45.0 kPa.",
            "apparatus": [
                {"name": "Computerized Automated Triaxial Testing Cell System", "purpose": "High-pressure acrylic cell (1700 kPa capacity) with internal tie rods and balanced loading ram."},
                {"name": "Dual Automatic Pressure-Volume Controllers (APVC)", "purpose": "Microprocessor syringe pumps controlling cell pressure and back pressure to 0.1 kPa and 1 mm³."},
                {"name": "High-Accuracy Submersible Load Cell", "purpose": "Internal 10 kN load cell mounted inside cell to eliminate piston friction artifacts."},
                {"name": "High-Precision Differential Pore Pressure Transducer", "purpose": "Measures pore-water pressure u at the base of the specimen with 0.1 kPa precision."},
                {"name": "High-Quality Latex Rubber Membranes & O-Rings", "purpose": "Encloses 38 mm diameter specimen, isolating soil pore fluid from pressurized cell water."},
                {"name": "De-Aired Water Vacuum Conditioning System", "purpose": "Provides dissolved-gas-free water for saturation and cell filling."}
            ],
            "procedure": [
                {"title": "Specimen Mounting & Membrane Encapsulation", "text": "Mount undisturbed 38 x 76 mm saturated clay specimen on triaxial pedestal between saturated porous stones and filter paper; roll latex membrane using stretcher; seal top cap and pedestal with dual O-rings."},
                {"title": "Cell Assembly & Water Filling", "text": "Lower acrylic cell chamber; tighten tie rods; fill cell completely with de-aired water; bleed air from cell top vent valve."},
                {"title": "Back-Pressure Saturation & B-Check", "text": "Increment cell pressure and back-pressure simultaneously in 50 kPa stages up to back pressure of 200 kPa; close drainage valve and increase cell pressure by 50 kPa; verify B = Δu / Δσ_3 ≥ 0.95."},
                {"title": "Isotropic Consolidation Stage", "text": "Open drainage valve to back-pressure controller; elevate cell pressure to target effective confining stress (100, 175, 250, 325, 400 kPa); log volume change until consolidation completes."},
                {"title": "Undrained Axial Shearing with Pore Pressure Acquisition", "text": "Close drainage valve; advance loading ram at 0.05 mm/min (undrained shear); log axial load P, axial displacement ΔL, and pore water pressure u every 15 seconds."},
                {"title": "Failure Envelope Evaluation", "text": "Calculate principal effective stresses σ'_1 and σ'_3 at peak deviator stress; repeat for all confining pressures; plot q_f versus σ'_3 to determine failure slope M and effective shear parameters."}
            ],
            "topics": [
                {"question": "What is Skempton's B-parameter, and why must B ≥ 0.95 before shearing?", "answer": "B = Δu / Δσ_3 under undrained isotropic compression; for fully saturated soil (S_r = 100%), water is virtually incompressible compared to the skeleton, giving B = 1.0; achieving B ≥ 0.95 ensures that all entrapped micro-air bubbles are dissolved into solution, guaranteeing accurate pore pressure measurement."},
                {"question": "How does Skempton's A-parameter characterize soil volume change tendency during shear?", "answer": "Pore pressure parameter A = (Δu - Δσ_3) / (Δσ_1 - Δσ_3); normally consolidated clays tend to contract, generating positive excess pore pressure (A_f = 0.5 to 1.0); heavily overconsolidated clays dilate, generating negative excess pore pressure (A_f = -0.5 to 0)."},
                {"question": "Why is an internal submersible load cell preferred over an external load cell?", "answer": "An external load cell measures total force including the friction between the loading ram and the cell bushing seals; an internal submersible load cell directly contacts the top cap, eliminating seal friction errors."},
                {"question": "What is the critical difference between total stress parameters (c, ϕ) and effective stress parameters (c', ϕ')?", "answer": "Total stress parameters depend on drainage conditions and pore pressure at the moment of test; effective stress parameters represent fundamental material properties governing strength across all drainage conditions via Terzaghi's principle: sigma' = sigma - u."},
                {"question": "Why must the strain rate in CU triaxial tests be kept extremely slow (e.g. 0.05 mm/min)?", "answer": "Water has low permeability in clay; shearing too quickly causes localized pore pressure gradients between the shear zone and base transducer, leading to false pore pressure measurements; slow rates ensure 95% pore pressure equalization."},
                {"question": "How are effective friction angle ϕ' and cohesion c' calculated from the p'-q diagram slope M?", "answer": "On a Cambridge p'-q plot (q vs p'), sin ϕ' = 3M / (6 + M) and c' = d (3 - sin ϕ') / (6 cos ϕ'), where M is the slope and d is the vertical intercept."},
            ],
            "precautions": [
                "Verify latex membrane has zero pinhole punctures by checking back-pressure volume stability prior to consolidation.",
                "Ensure Skempton's B-check achieves at least 0.95 before initiating consolidation to prevent testing unsaturated soil.",
                "Select shearing rate slow enough to achieve 95% internal pore pressure equalization according to Gibson & Henkel theory.",
                "Apply membrane thickness corrections to deviator stress according to ASTM D4767 specifications."
            ],
            "quiz": [
                {
                    "question": "Skempton's pore pressure parameter B for a fully saturated soil (100% saturation) is approximately:",
                    "options": ["0.0", "0.5", "1.0", "Infinity"],
                    "correct": 2,
                    "explanation": "For fully saturated soil with incompressible water, applied cell pressure transfers 100% to pore water, yielding B = 1.0 (acceptable if ≥ 0.95)."
                },
                {
                    "question": "In a Consolidated-Undrained (CU) triaxial test, the drainage valve is:",
                    "options": ["Open during consolidation, closed during shearing", "Closed during consolidation, open during shearing", "Open throughout all stages", "Closed throughout all stages"],
                    "correct": 0,
                    "explanation": "Consolidated-Undrained means drainage is open during initial consolidation, then closed during axial shearing."
                },
                {
                    "question": "Heavily overconsolidated clay sheared undrained typically exhibits an A-parameter at failure (A_f) that is:",
                    "options": ["Greater than 1.0", "Between 0.5 and 1.0", "Negative or near zero (dilatant)", "Equal to B"],
                    "correct": 2,
                    "explanation": "Heavily overconsolidated clays dilate during shear, drawing water and generating negative excess pore pressure, yielding negative A_f."
                },
                {
                    "question": "The primary advantage of CU triaxial testing with pore pressure measurement is:",
                    "options": ["It requires only dry sand", "It allows determination of effective stress parameters (c', ϕ') from undrained tests", "It takes only 1 minute to complete", "It eliminates the need for load cells"],
                    "correct": 1,
                    "explanation": "Measuring pore water pressure u allows calculation of effective stresses (σ' = σ - u), yielding effective strength parameters."
                }
            ],
            "samples": [100.0, 175.0, 250.0, 325.0, 400.0],
            "measureLabel": "Record peak deviator stress q_f",
            "readings": ["qf_kpa", "sigma3_kpa", "pore_press_u", "sigma1_eff"],
            "theory": """<h3>1. Effective Stress Principle & Axisymmetric Triaxial Mechanics</h3>
<p>In a standard triaxial specimen ($D_0 = 38\\text{ mm}$, $L_0 = 76\\text{ mm}$), the stress state is axisymmetric: radial cell fluid pressure applies equal minor and intermediate total principal stresses ($\\sigma_2 = \\sigma_3 = \\sigma_{cell}$). Vertical axial loading via the ram applies additional deviatoric load $P$, establishing major principal total stress:</p>
\\[ \\sigma_1 = \\sigma_3 + \\frac{P}{A} \\implies q = \\sigma_1 - \\sigma_3 = \\frac{P}{A} \\]
<p>where $A$ is the deformed cross-sectional area. According to Terzaghi's effective stress principle, shear strength is governed strictly by effective principal stresses:</p>
\\[ \\sigma'_1 = \\sigma_1 - u, \\qquad \\sigma'_3 = \\sigma_3 - u \\]
<p>where $u$ is the measured pore-water pressure at failure.</p>

<h3>2. Pore Pressure Generation & Skempton's Parameters</h3>
<p>Under undrained conditions, changes in total principal stresses $(\\Delta \\sigma_1, \\Delta \\sigma_3)$ generate excess pore water pressure $\\Delta u$ formulated by A. W. Skempton (1954):</p>
\\[ \\Delta u = B \\left[ \\Delta \\sigma_3 + A (\\Delta \\sigma_1 - \\Delta \\sigma_3) \\right] \\]
<p>For saturated soil ($B = 1.0$):</p>
\\[ \\Delta u = \\Delta \\sigma_3 + A \\cdot q \\]
<p>During undrained shear where cell pressure is constant ($\\Delta \\sigma_3 = 0$), excess pore pressure is $\\Delta u = A \\cdot q$.</p>

<h3>3. The Stress Path & Failure Envelope Formulation</h3>
<p>On the $(q, \\sigma'_3)$ stress space, the peak failure envelope for normally to lightly overconsolidated clays follows a linear trajectory:</p>
\\[ q_f = M \\cdot \\sigma'_3 + q_0 \\]
<p>where $M = 1.3500$ is the failure slope, and $q_0 = 45.00\\text{ kPa}$ is the intercept. Effective friction angle $\\phi'$ is evaluated from Mohr circle geometry at failure:</p>
\\[ \\sin \\phi' = \\frac{\\sigma'_1 - \\sigma'_3}{\\sigma'_1 + \\sigma'_3 + 2 c' \\cot \\phi'} = \\frac{q_f}{2 \\sigma'_3 + q_f + 2 c' \\cot \\phi'} \\]
<p>yielding calibrated parameters $\\phi' = 28.5^\\circ$ and $c' = 15.0\\text{ kPa}$.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this geotechnical engineering laboratory investigation is to evaluate the effective stress shear strength parameters (effective friction angle $\\phi'$ and effective cohesion $c'$) and pore-water pressure characteristics of saturated cohesive silty clay using the Consolidated-Undrained (CU) triaxial compression test with pore pressure measurement according to ASTM D4767 / BS 1377-8 across five effective confining pressures ($\\sigma'_3 = 100, 175, 250, 325,$ and $400\\text{ kPa}$).</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Peak deviator stress $q_f = (\\sigma_1 - \\sigma_3)_f$ relates linearly to effective confining pressure $\\sigma'_3$ according to the triaxial failure model:</p>
\\[ q_f = M \\cdot \\sigma'_3 + q_0 \\]
<p>where $M = 1.3500$ is the failure slope and $q_0 = 45.0000\\text{ kPa}$ is the intercept. Effective principal stresses are $\\sigma'_1 = \\sigma_1 - u_f$ and $\\sigma'_3 = \\sigma_3 - u_f$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized an automated triaxial system (GDS Instruments) comprising an acrylic high-pressure cell ($1700\\text{ kPa}$ capacity), two automated pressure-volume controllers (precision $\\pm 0.1\\text{ kPa}$, volume resolution $1\\text{ mm}^3$), an internal submersible load cell ($10.0\\text{ kN}$ capacity, precision $\\pm 1.0\\text{ N}$), and an electronic pore-water pressure transducer ($1000\\text{ kPa}$ capacity, precision $\\pm 0.1\\text{ kPa}$). Undisturbed silty clay specimens ($D_0 = 38.00 \\pm 0.05\\text{ mm}$, $L_0 = 76.00 \\pm 0.10\\text{ mm}$, initial area $A_0 = 11.34\\text{ cm}^2$) were encased in $0.3\\text{ mm}$ latex membranes.</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Specimens were mounted and back-pressure saturated to $u_0 = 200\\text{ kPa}$ until $B = \\Delta u / \\Delta \\sigma_3 \\ge 0.96$. Isotropic consolidation was executed at effective confining stresses of $100, 175, 250, 325,$ and $400\\text{ kPa}$ until pore pressure dissipated ($> 95\\%$ primary consolidation). The drainage valve was closed, and undrained axial compression applied at $0.05\\text{ mm/min}$ ($0.065\\%\\text{ strain/min}$). Axial force $P$, displacement $\\Delta L$, and pore pressure $u$ were logged continuously up to $15\\%$ axial strain.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Triaxial cells store high hydraulic energy at pressures up to $600\\text{ kPa}$. The acrylic chamber was inspected for micro-crazing and tie rods torqued uniformly. Overpressure relief valves were set at $800\\text{ kPa}$. Operators wore ANSI-approved safety glasses during all pressurized operations.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded at peak deviator failure across the five CU trials:</p>
<table>
<thead>
<tr><th>Trial</th><th>Effective Confining σ'_3 (kPa)</th><th>Peak Deviator Stress q_f (kPa)</th><th>Pore Pressure at Failure u_f (kPa)</th><th>Major Effective Stress σ'_1 (kPa)</th><th>Pore Parameter A_f</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>100.0</td><td>180.0</td><td>254.2</td><td>280.0</td><td>0.62</td></tr>
<tr><td>2</td><td>175.0</td><td>281.3</td><td>268.5</td><td>456.3</td><td>0.58</td></tr>
<tr><td>3</td><td>250.0</td><td>382.5</td><td>282.4</td><td>632.5</td><td>0.55</td></tr>
<tr><td>4</td><td>325.0</td><td>483.8</td><td>295.8</td><td>808.8</td><td>0.52</td></tr>
<tr><td>5</td><td>400.0</td><td>585.0</td><td>308.2</td><td>985.0</td><td>0.49</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of peak deviator stress $q_f$ versus effective confining stress $\\sigma'_3$ yields:</p>
\\[ q_f = 1.35000 \\cdot \\sigma'_3 + 45.00000 \\]
<p>with an exceptional coefficient of determination $R^2 = 1.000000$. The experimental failure slope $M = 1.35000$ matches the reference design benchmark ($1.3500$) with zero relative deviation ($0.00\\%$). Calculating effective shear parameters from Mohr–Coulomb geometry:</p>
\\[ \\sin \\phi' = \\frac{M}{2 + M} = \\frac{1.350}{3.350} = 0.4030 \\implies \\phi' = \\arcsin(0.4030) = 23.77^\\circ \\]
<p>With intercept $q_0 = 45.00\\text{ kPa}$, effective cohesion evaluates as $c' = 15.0\\text{ kPa}$.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include load cell accuracy $\\delta P = \\pm 1.0\\text{ N}$, pore pressure transducer $\\delta u = \\pm 0.2\\text{ kPa}$, cell pressure $\\delta \\sigma_3 = \\pm 0.2\\text{ kPa}$, and area correction $\\delta A / A = 0.3\\%$. Propagating into $M$:</p>
\\[ \\frac{\\delta M}{M} = \\sqrt{ \\left( \\frac{\\delta q_f}{\\Delta q_f} \\right)^2 + \\left( \\frac{\\delta \\sigma'_3}{\\Delta \\sigma'_3} \\right)^2 } = \\pm 0.38\\% \\]
<p>The reported triaxial failure slope is $M = 1.3500 \\pm 0.0051$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>Pore pressure parameter $A_f$ ranged between $0.49$ and $0.62$, characteristic of normally to lightly overconsolidated clays exhibiting contractive shearing tendency. Because excess pore water pressure was accurately monitored throughout shearing, effective stress paths ($p'\\text{-}q$) accurately mapped the yield surface and established true frictional resistance independent of drainage kinetics.</p>

<h3>10. Slope Stability & Long-Term Embankment Engineering</h3>
<p>In geotechnical design of highway cut slopes and earth dam embankments, effective stress parameters $(c', \\phi')$ govern long-term steady-state seepage stability. Unlike total stress parameters that apply only immediately after rapid construction, effective stress analysis using $c' = 15.0\\text{ kPa}$ and $\\phi' = 28.5^\\circ$ provides guaranteed safety factors against delayed slope failures caused by groundwater seepage.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is back-pressure saturation necessary if the specimen was already saturated in the field?</strong><br>
<em>A1:</em> Sampling, trimming, and handling release confining stress, allowing microscopic dissolved air to come out of solution into voids; elevating back pressure to $200\\text{ kPa}$ forces micro-bubbles back into solution, ensuring complete hydraulic continuity between soil pores and measuring transducers.</p>
<p><strong>Q2: What is the difference between CU triaxial testing and Drained (CD) triaxial testing?</strong><br>
<em>A2:</em> In CD testing, the drainage valve remains open during shearing at extremely slow rates so that excess pore pressure never develops ($\Delta u = 0$); while CD testing directly yields effective parameters, CU testing with pore pressure measurement yields identical effective parameters in a fraction of the time.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The triaxial Consolidated-Undrained investigation successfully determined the effective shear strength parameters of the cohesive soil. The calibrated failure slope $M = 1.3500$ ($R^2 = 1.000000$), effective friction angle $\\phi' = 28.5^\\circ$, and effective cohesion $c' = 15.0\\text{ kPa}$ provide an authoritative foundation for numerical slope stability and foundation engineering.</p>"""
        },
        {
            "number": 25,
            "slug": "atterberg-limits-casagrande-liquid-limit",
            "title": "Atterberg Consistency Limits & Casagrande Liquid Limit Determination",
            "shortTitle": "Casagrande Liquid Limit",
            "aim": "Determine the Liquid Limit (LL), Plastic Limit (PL), and Plasticity Index (PI) of cohesive soil using the Casagrande mechanical liquid limit cup according to ASTM D4318 / BS 1377-2.",
            "inputLabel": "Casagrande Cup Blow Count N",
            "shortInput": "Blow Count N",
            "inputUnit": "blows",
            "min": 15.0,
            "max": 40.0,
            "step": 5.0,
            "initial": 25.0,
            "inputDecimals": 0,
            "rawLabel": "Moisture Content w",
            "rawUnit": "%",
            "rawDecimals": 1,
            "xAxis": "Common logarithm of blow count log10(N)",
            "yAxis": "Moisture content w (%)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 2.0,
            "emptyY": 65.0,
            "targetName": "Flow Index Parameter I_f",
            "target": "14.5000",
            "refValue": 14.5000,
            "resultUnit": "%/log(blow)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "w = -14.5000 · log10(N) + 62.0000",
            "intro": "The consistency and physical behavior of cohesive fine-grained soils depend profoundly on moisture content rather than particle size alone. In 1911, Swedish chemist Albert Atterberg defined four fundamental physical states of soil consistency: solid, semi-solid, plastic, and liquid. In 1932, Arthur Casagrande standardized the mechanical boundary between the plastic and liquid states—the Liquid Limit (LL)—using the mechanical cup apparatus (ASTM D4318). The Liquid Limit is defined as that gravimetric moisture content at which a trapezoidal groove cut through a pat of soil in a brass cup closes over a length of exactly 12.7 mm (0.5 inches) upon receiving exactly 25 standard mechanical blows dropped from a height of 10.0 mm at 2 blows per second onto a hard rubber base. At the liquid limit, all fine-grained soils possess an identical, tiny undrained shear strength of approximately 1.7 to 2.4 kPa. Because achieving exactly 25 blows in a single trial is virtually impossible, tests are performed across four to six trials with blow counts spanning 15 to 40 blows. Plotting moisture content w against log10(N) yields a straight line termed the Flow Curve, whose slope defines the Flow Index I_f = -dw / d(log10 N). The moisture content at N = 25 blows interpolated from the flow curve provides the Liquid Limit LL. Combined with the Plastic Limit (PL, moisture where 3.2 mm soil threads crumble), the Plasticity Index PI = LL - PL classifies soils on Casagrande's Plasticity Chart under the Unified Soil Classification System (USCS). In this laboratory, Casagrande tests are performed to evaluate the Flow Index I_f and establish LL.",
            "modelExtra": "High-plasticity alluvial clay (CH under USCS). Linearized flow curve relates moisture content w directly to log10(N) with flow index slope -14.5000 %/log(blow) and 0-blow intercept 62.00%. Liquid limit LL at N = 25 blows evaluates as w(25) = -14.50 · log10(25) + 62.00 = -14.50(1.39794) + 62.00 = 41.73%.",
            "apparatus": [
                {"name": "Standard Casagrande Mechanical Liquid Limit Device", "purpose": "Brass cup dropping 10.0 ± 0.2 mm onto a calibrated hard ebonite rubber base via hand crank."},
                {"name": "ASTM Flat Grooving Tool (11 mm wide)", "purpose": "Precision brass/plastic grooving tool cutting clean 2.0 mm wide, 8.0 mm deep central channel."},
                {"name": "Ground Glass Mixing Plate & Spatulas", "purpose": "Smooth frosted glass plate (450 x 450 mm) and flexible steel spatulas for paste blending."},
                {"name": "Drying Oven & Tare Moisture Cans", "purpose": "Electric oven maintaining 110 ± 5 °C and airtight aluminum containers weighing moisture portions."},
                {"name": "Drop Height Calibration Gauge", "purpose": "10.0 mm machined step gauge verifying exact cup drop height prior to testing."},
                {"name": "Analytical Top-Loading Balance", "purpose": "Weighs soil moisture portions to 0.01 g resolution (capacity 200 g)."}
            ],
            "procedure": [
                {"title": "Soil Fraction Preparation & Drop Height Calibration", "text": "Pass air-dried soil through the 425 μm (No. 40) sieve; take 250 g; calibrate Casagrande cup drop height to exactly 10.0 mm using the thickness gauge on the grooving tool."},
                {"title": "Initial Moisture Conditioning", "text": "Place soil on glass plate; add distilled water gradually, working thoroughly with spatulas for 10 minutes to produce a uniform, smooth plastic paste."},
                {"title": "Cup Placement & Leveling", "text": "Place a portion of paste into the brass cup above the hinge; spread with spatula to maximum depth of 10 mm; level surface parallel to rubber base."},
                {"title": "Standard Central Grooving", "text": "Draw grooving tool firmly along the cup centerline from hinge toward front in a single continuous stroke, dividing soil pat into two symmetrical halves."},
                {"title": "Cranking & Closure Recording", "text": "Turn crank at steady rate of 2 blows per second; count blows until soil halves flow together and close across a continuous bottom length of 12.7 mm; record blow count N."},
                {"title": "Moisture Sampling & Multi-Point Sweep", "text": "Extract a 15 g sample across the closed groove; weigh immediately; dry in oven at 110 °C to determine w; repeat at varying moisture contents between 15 and 40 blows to establish the Flow Curve."}
            ],
            "topics": [
                {"question": "What is the physical meaning of the Liquid Limit in terms of undrained shear strength?", "answer": "The Liquid Limit represents the moisture threshold where soil transitions from plastic behavior to a viscous liquid; remarkably, at the Liquid Limit, all soils possess an identical tiny undrained shear strength of approximately 1.7 to 2.4 kPa."},
                {"question": "How does the ASTM grooving tool differ from the Casagrande grooving tool, and when is each used?", "answer": "The ASTM tool cuts a flat-bottomed groove with a 2.0 mm base and 11.0 mm top width, preferred for low-plasticity or sandy clays that tear under knife edges; the Casagrande tool has a curved blade suited for high-plasticity fat clays."},
                {"question": "What is the Plasticity Index (PI) and what does it indicate about soil engineering behavior?", "answer": "PI = LL - PL; it represents the range of moisture over which soil behaves plastically; a high PI (> 25) indicates expansive, highly plastic montmorillonite clays prone to severe swelling, shrinkage, and low permeability."},
                {"question": "How is the Casagrande 'A-Line' used to classify fine-grained soils in the USCS system?", "answer": "On the plasticity chart (PI vs LL), the empirical A-Line equation is PI = 0.73 (LL - 20); soils plotting above the A-Line are inorganic clays (CL, CH), while soils plotting below are inorganic silts (ML, MH) or organic soils."},
                {"question": "Why is the hardness of the rubber base in the Casagrande device strictly standardized?", "answer": "The rebound resilience of the rubber base governs the shock wave energy transferred to the soil during impact; a softer base absorbs energy, requiring more blows (false high LL), while a hard base transmits high shock, requiring fewer blows."},
                {"question": "How does the Fall Cone penetrometer method (BS 1377) compare to the Casagrande cup test?", "answer": "The British standard fall cone measures the penetration of an 80 g, 30° cone in 5 seconds (LL = 20.0 mm penetration); it is vastly more operator-independent and eliminates dynamic grooving tear artifacts common in Casagrande cups."}
            ],
            "precautions": [
                "Verify the cup drop height is calibrated to exactly 10.0 mm before testing; wear on the cam follower alters drop height over time.",
                "Turn the crank at a constant, steady frequency of 2 revolutions per second without jerky accelerations.",
                "Draw the grooving tool perpendicular to the cup surface in a single smooth motion to prevent tearing the soil pat from the brass surface.",
                "Store conditioned soil in sealed plastic bags between trials to prevent moisture loss from ambient evaporation."
            ],
            "quiz": [
                {
                    "question": "The Liquid Limit is defined as the moisture content corresponding to a Casagrande cup blow count of:",
                    "options": ["10 blows", "20 blows", "25 blows", "50 blows"],
                    "correct": 2,
                    "explanation": "ASTM D4318 defines the Liquid Limit as the moisture content at exactly 25 blows."
                },
                {
                    "question": "The standard drop height of the Casagrande brass cup is:",
                    "options": ["5.0 mm", "10.0 mm", "15.0 mm", "20.0 mm"],
                    "correct": 1,
                    "explanation": "The calibrated drop height of the cup is exactly 10.0 ± 0.2 mm."
                },
                {
                    "question": "The length of groove closure required to terminate the blow count is:",
                    "options": ["5.0 mm", "12.7 mm (0.5 in)", "25.4 mm (1.0 in)", "Full cup length"],
                    "correct": 1,
                    "explanation": "The test ends when the bottom of the groove closes over a continuous length of 12.7 mm (1/2 inch)."
                },
                {
                    "question": "If a soil has a Liquid Limit of 45% and a Plastic Limit of 20%, its Plasticity Index (PI) is:",
                    "options": ["15%", "25%", "35%", "65%"],
                    "correct": 1,
                    "explanation": "PI = LL - PL = 45% - 20% = 25%."
                }
            ],
            "samples": [15.0, 20.0, 25.0, 30.0, 35.0, 40.0],
            "measureLabel": "Record soil moisture content w at closure",
            "readings": ["moisture_pct", "blow_count_n", "log_blows", "flow_state"],
            "theory": """<h3>1. Physical States of Soil Consistency</h3>
<p>Fine-grained cohesive soils exhibit distinct rheological behaviors depending on water content. Albert Atterberg established four fundamental consistency states defined by three limiting boundaries:</p>
\\[ \\text{Solid} \\xrightarrow{\\text{Shrinkage Limit (SL)}} \\text{Semi-Solid} \\xrightarrow{\\text{Plastic Limit (PL)}} \\text{Plastic} \\xrightarrow{\\text{Liquid Limit (LL)}} \\text{Liquid} \\]
<p>In the plastic state, soil can be molded into arbitrary shapes without rupture or crumbling. The Plasticity Index ($PI$) quantifies the extent of this plastic range:</p>
\\[ PI = LL - PL \\]
<p>The Liquidity Index ($LI$) defines the current in-situ consistency of a natural soil deposit:</p>
\\[ LI = \\frac{w - PL}{PI} \\]
<p>If $LI < 0$, soil is hard and semi-solid; if $0 < LI < 1$, soil is plastic; if $LI > 1$, natural moisture exceeds liquid limit, posing severe sensitivity and liquefaction hazards under shear.</p>

<h3>2. The Casagrande Flow Curve & Dynamic Impact Energy</h3>
<p>In the Casagrande device, each blow imparts kinetic impact energy $E_b = M_{cup} g h$. The impact generates inertial shockwaves that shear the two halves of the soil pat across the base of the groove. Dynamic soil resistance scales with undrained shear strength $\\tau_f$. Arthur Casagrande demonstrated that the number of blows $N$ required to achieve $12.7\\text{ mm}$ closure scales exponentially with moisture content $w$:</p>
\\[ w = - I_f \\cdot \\log_{10}(N) + w_0 \\]
<p>where $I_f$ is the Flow Index (slope of the flow curve) representing the rate of shear strength loss with increasing water content.</p>

<h3>3. Linear Flow Curve Calibration</h3>
<p>In this experimental investigation, moisture content $w$ across blow counts $N = 15\\text{ to }40$ follows the linear calibration model:</p>
\\[ w = - 14.5000 \\cdot \\log_{10}(N) + 62.0000 \\]
<p>Evaluating at standard benchmark $N = 25\\text{ blows}$ ($\\log_{10}(25) = 1.39794$):</p>
\\[ LL = - 14.5000(1.39794) + 62.0000 = - 20.270 + 62.000 = 41.73\\% \\]""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this geotechnical engineering laboratory investigation is to evaluate the Liquid Limit ($LL$), Plastic Limit ($PL$), and Plasticity Index ($PI$) of cohesive subgrade soil using the Casagrande mechanical cup apparatus according to ASTM D4318 / BS 1377-2 across six blow count levels ($N = 15\\text{ to }40\\text{ blows}$). By constructing the semi-logarithmic Flow Curve and performing linear regression, we determine the Flow Index $I_f$ and classify the soil on Casagrande's Plasticity Chart under the Unified Soil Classification System (USCS).</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>The relationship between moisture content $w$ and mechanical blow count $N$ follows the Casagrande Flow Equation:</p>
\\[ w = - I_f \\cdot \\log_{10}(N) + w_0 \\]
<p>where $I_f = 14.5000\\%\\text{/log(blow)}$ is the Flow Index and $w_0 = 62.0000\\%$ is the intercept. The Liquid Limit is defined as the moisture content at exactly $N = 25\\text{ blows}$:</p>
\\[ LL = w(N=25) \\]

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized an ASTM D4318 motorized Casagrande liquid limit device comprising a brass cup ($M = 200.0 \\pm 2.0\\text{ g}$) dropping $10.00 \\pm 0.05\\text{ mm}$ onto a calibrated hard rubber base (Shore D hardness $60 \\pm 5$). Grooving was executed with an ASTM flat grooving tool ($2.0\\text{ mm}$ cutting tip, $11.0\\text{ mm}$ top width). Moisture determination utilized a digital top-loading analytical balance ($200.0\\text{ g}$ capacity, precision $\\pm 0.01\\text{ g}$) and a forced-convection drying oven ($110 \\pm 5^\\circ\\text{C}$). The test soil was the fraction passing the $425\\,\\mu\\text{m}$ (No. 40) sieve.</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>The cup drop height was verified using the $10.0\\text{ mm}$ gauge block. A $250\\text{ g}$ soil sample was mixed with distilled water into a smooth paste. Portions were placed in the cup, leveled to $10\\text{ mm}$ depth, and grooved along the centerline. The crank was rotated at $2\\text{ blows/s}$ until the groove closed over a length of $12.7\\text{ mm}$. The blow count $N$ was logged, a $15\\text{ g}$ moisture sample extracted across the closure zone, and dried for 24 hours. The test was repeated across six moisture contents yielding blow counts between 15 and 40.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Repetitive manual cranking presents ergonomic strain; motorized drives were operated with guards. Oven drying handles presented thermal burn risks; insulated gloves were used when transferring tare containers.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the Casagrande flow curve test series:</p>
<table>
<thead>
<tr><th>Trial</th><th>Blow Count N (blows)</th><th>log10(N)</th><th>Tare Container No.</th><th>Wet Soil + Tare (g)</th><th>Dry Soil + Tare (g)</th><th>Moisture Content w (%)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>15.0</td><td>1.1761</td><td>C-1</td><td>38.45</td><td>29.58</td><td>44.95</td></tr>
<tr><td>2</td><td>20.0</td><td>1.3010</td><td>C-2</td><td>39.12</td><td>30.34</td><td>43.14</td></tr>
<tr><td>3</td><td>25.0</td><td>1.3979</td><td>C-3</td><td>41.20</td><td>32.28</td><td>41.73</td></tr>
<tr><td>4</td><td>30.0</td><td>1.4771</td><td>C-4</td><td>37.80</td><td>29.89</td><td>40.58</td></tr>
<tr><td>5</td><td>35.0</td><td>1.5441</td><td>C-5</td><td>40.15</td><td>32.05</td><td>39.61</td></tr>
<tr><td>6</td><td>40.0</td><td>1.6021</td><td>C-6</td><td>38.90</td><td>31.25</td><td>38.77</td></tr>
</tbody>
</table>
<p><strong>Plastic Limit Testing:</strong> Hand-rolled $3.2\\text{ mm}$ threads crumbled at an average moisture content of $PL = 21.20\\%$.</p>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of moisture content $w$ versus common logarithm of blow count $x = \\log_{10}(N)$ yields:</p>
\\[ w = -14.50000 \\cdot \\log_{10}(N) + 62.00000 \\]
<p>with an extraordinary coefficient of determination $R^2 = 1.000000$. The absolute experimental Flow Index $I_f = 14.5000\\%\\text{/log(blow)}$ matches the reference design benchmark ($14.5000$) with zero relative deviation ($0.00\\%$). Calculating the Liquid Limit at $N = 25\\text{ blows}$:</p>
\\[ LL = -14.50000 \\times \\log_{10}(25) + 62.00000 = -14.50000(1.39794) + 62.00000 = 41.73\\% \\]
<p>Evaluating Plasticity Index:</p>
\\[ PI = LL - PL = 41.73\\% - 21.20\\% = 20.53\\% \\]

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include balance precision $\\delta m = \\pm 0.01\\text{ g}$, blow count visual detection $\\delta N = \\pm 1\\text{ blow}$, and drop height calibration $\\delta h = \\pm 0.1\\text{ mm}$. Propagating into $LL$:</p>
\\[ \\delta LL = \\sqrt{ \\left( \\frac{I_f}{N \\ln 10} \\delta N \\right)^2 + \\delta w^2 } = \\pm 0.28\\% \\]
<p>The reported Liquid Limit is $LL = 41.73 \\pm 0.28\\%$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>On Casagrande's Plasticity Chart, plotting $PI = 20.53\\%$ against $LL = 41.73\\%$ locates the soil above the empirical A-Line ($PI_{A-Line} = 0.73(LL - 20) = 0.73(41.73 - 20) = 15.86\\%$). Because $LL < 50\\%$ and $PI > 7$, the soil classifies unambiguously as a **CL (Inorganic Clay of Medium Plasticity)** under the USCS system and **A-6** under the AASHTO system.</p>

<h3>10. Geotechnical Swell & Settlement Engineering Implications</h3>
<p>Soil classification as CL with $LL = 41.7\\%$ indicates moderate shrink-swell potential and moderate compressibility. Empirical correlations with Liquid Limit confirm: Compression Index $C_c \\approx 0.009(LL - 10) = 0.009(31.7) = 0.285$, perfectly validating the oedometer consolidation test results obtained in Laboratory 22.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why does testing soil that has been oven-dried before Atterberg testing produce erroneous results?</strong><br>
<em>A1:</em> Oven drying at $110^\\circ\\text{C}$ causes irreversible collapse of clay mineral lattices and drives off structural interlayer water, agglomerating fine platelets into permanent silt-sized clusters that artificially lower both Liquid Limit and Plasticity Index by $20\\text{ to }40\\%$.</p>
<p><strong>Q2: What is the Activity of clay, and how is it related to mineralogy?</strong><br>
<em>A2:</em> Activity is defined as $A_c = PI / (\\% \\text{ clay fraction } < 2\\,\\mu\\text{m})$; kaolinite has low activity ($A_c < 0.5$), illite moderate ($0.75\\text{ to }1.25$), and sodium bentonite (montmorillonite) extreme activity ($A_c > 4.0$), dictating massive volumetric swelling.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The Casagrande liquid limit investigation accurately established the consistency boundaries and plasticity characteristics of the cohesive soil. The verified Flow Index $I_f = 14.5000\\%\\text{/log(blow)}$ ($R^2 = 1.000000$), Liquid Limit $LL = 41.73\\%$, and Plasticity Index $PI = 20.53\\%$ provide an authoritative basis for soil classification and foundation engineering.</p>"""
        },
        {
            "number": 26,
            "slug": "in-situ-field-density-sand-cone-method",
            "title": "In-Situ Field Dry Density & Compaction Verification by Sand Cone Method",
            "shortTitle": "Sand Cone Field Density",
            "aim": "Determine the in-situ wet density, in-situ dry density, and relative compaction percentage (RC) of compacted earth fill using the sand cone apparatus according to ASTM D1556 / AASHTO T191.",
            "inputLabel": "Excavated Test Hole Volume V_h",
            "shortInput": "Hole Volume",
            "inputUnit": "cm³",
            "min": 1200.0,
            "max": 2400.0,
            "step": 200.0,
            "initial": 1800.0,
            "inputDecimals": 0,
            "rawLabel": "Mass of Dry Excavated Soil M_s",
            "rawUnit": "g",
            "rawDecimals": 1,
            "xAxis": "Excavated hole volume V_h (cm³)",
            "yAxis": "Dry mass of excavated soil M_s (g)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 2600.0,
            "emptyY": 4800.0,
            "targetName": "In-Situ Field Dry Density ρ_d",
            "target": "1.8500",
            "refValue": 1.8500,
            "resultUnit": "g/cm³",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "M_s = 1.8500 · V_h",
            "intro": "Quality assurance and quality control (QA/QC) in civil earthwork construction require rigorous verification that compacted subgrades, roadway base courses, and structural backfills achieve specified field densities. Standardized under ASTM D1556 and AASHTO T191, the sand cone method provides the definitive, physical benchmark field test against which modern nuclear density gauges are calibrated. In this test, a metal base plate with a 165 mm (6.5 inch) circular hole is clamped flat onto the freshly compacted fill. A test hole approximately 150 mm deep is excavated by hand using chisels and scoops, with every single particle of excavated soil collected into a sealed moisture container. The volume of the irregular hole V_h is determined by inverting a standardized sand cone apparatus over the hole and opening the control valve. Standard uniform, clean, dry Ottawa sand (passing 850 μm No. 20, retained on 600 μm No. 30) of pre-calibrated bulk density ρ_sand flows by gravity into the hole and funnel cone. Subtracting the calibrated mass of sand required to fill the metal cone funnel alone yields the net mass of sand filling the test hole, from which volume V_h = M_sand / ρ_sand is evaluated. Weighing excavated moist soil M_wet and measuring moisture content w provides in-situ dry density: ρ_d = M_wet / [V_h (1 + w)] = M_s / V_h. Relative compaction RC = (ρ_d / MDD) x 100% must meet contract specifications (typically ≥ 95%). In this laboratory, sand cone tests are performed across hole volumes from 1200 to 2400 cm³ to evaluate field dry density ρ_d.",
            "modelExtra": "Calibrated Ottawa silica sand bulk density ρ_sand = 1.420 g/cm³, cone funnel constant M_cone = 1560.0 g. Compacted subgrade soil with gravimetric moisture w = 12.0%. Linearized model relates dry soil mass M_s directly to hole volume V_h with slope 1.8500 g/cm³ (in-situ dry density ρ_d = 1.8500 g/cm³).",
            "apparatus": [
                {"name": "Standard Sand Cone Apparatus Assembly", "purpose": "Clear 4-liter plastic jar with 60° metal funnel, 12.7 mm cylindrical valve, and threaded collar."},
                {"name": "Machined Steel Guide Base Plate", "purpose": "Rigid metal plate (300 x 300 mm) with 165 mm flanged central opening and corner anchoring pins."},
                {"name": "Calibrated Standard Ottawa Sand (20-30 mesh)", "purpose": "Uniform, round quartz sand (bulk density 1.420 g/cm³) flowing with constant uncompacted density."},
                {"name": "Excavating Hand Tools & Chisels", "purpose": "Curved spoons, flat chisels, and hand trowels excavating cylindrical test hole without disturbing walls."},
                {"name": "Air-Tight Sealed Specimen Moisture Cans", "purpose": "Hermetic plastic-gasketed containers preventing moisture loss during transport to balance."},
                {"name": "Electronic High-Precision Field Balance", "purpose": "Battery-powered digital balance measuring up to 10 kg with 0.1 g resolution."}
            ],
            "procedure": [
                {"title": "Apparatus Calibration: Cone Funnel Mass & Sand Density", "text": "Determine calibrated bulk density of Ottawa sand ρ_sand (1.420 g/cm³) in a 1-liter mold; fill sand cone jar; invert on base plate; open valve to determine mass of sand filling cone alone (M_cone = 1560 g)."},
                {"title": "Test Surface Preparation & Base Plate Anchoring", "text": "Level a 500 x 500 mm test area on compacted fill; seat base plate flat; secure corners with steel spikes to prevent shifting."},
                {"title": "Test Hole Excavation & Soil Collection", "text": "Excavate circular hole through plate opening to depth of ~150 mm using chisel and scoop; collect every gram of excavated soil into sealed container; record moist mass M_wet."},
                {"title": "Sand Cone Inversion & Valve Opening", "text": "Weigh filled sand cone assembly (M_initial); seat inverted cone centrally into base plate recess; open valve fully; allow sand to flow by gravity until motion stops; close valve."},
                {"title": "Retained Sand Weighing & Hole Volume Calculation", "text": "Weigh remaining sand and jar (M_final); compute sand used M_used = M_initial - M_final; compute net sand in hole M_hole = M_used - M_cone; calculate hole volume V_h = M_hole / ρ_sand."},
                {"title": "Moisture & Relative Compaction Determination", "text": "Dry excavated soil sample in oven at 110 °C to determine moisture content w; compute in-situ dry density ρ_d = M_s / V_h; calculate relative compaction RC = (ρ_d / MDD) x 100%."}
            ],
            "topics": [
                {"question": "Why is standard uniform Ottawa sand (20-30 mesh) required rather than arbitrary local sand?", "answer": "Standard Ottawa sand is composed of clean, highly rounded quartz grains of uniform size (passing No. 20, retained No. 30); its spherical shape and narrow grading ensure that it pours under gravity with an invariant, reproducible bulk density unaffected by minor vibration."},
                {"question": "How does vehicle or equipment vibration during the sand cone test corrupt the result?", "answer": "Vibrations from nearby compactors densify the sand as it flows into the test hole, causing excess sand to enter; this yields an artificially large calculated hole volume V_h, falsely depressing the calculated field dry density ρ_d."},
                {"question": "What is the consequence of leaving excavated soil crumbs at the bottom of the test hole?", "answer": "Unrecovered soil reduces measured excavated mass M_wet while increasing the sand required to fill the hole, producing a compounding double error that falsely reduces apparent in-situ dry density."},
                {"question": "How does the sand cone test calibrate modern nuclear density gauges (ASTM D6938)?", "answer": "Nuclear gauges use gamma-ray Compton scattering to measure density and neutron thermalization for moisture; because chemical composition and iron content skew radiation counts, site-specific calibration curves against sand cone tests are mandatory."},
                {"question": "What is the acceptable tolerance for Relative Compaction (RC) on highway subgrade construction?", "answer": "AASHTO specifications typically require Relative Compaction RC ≥ 95% of Standard Proctor MDD for embankment fills, and RC ≥ 98% to 100% of Modified Proctor MDD for the upper 300 mm subgrade directly beneath asphalt pavement."},
                {"question": "Why must the test hole have smooth vertical walls without sharp overhangs or undercuts?", "answer": "Undercuts and overhangs create shadowed void pockets that gravity-flowing sand cannot penetrate; unfilled void pockets cause calculated hole volume to be too small, falsely inflating apparent soil density."}
            ],
            "precautions": [
                "Halt all heavy vibrating rollers and construction traffic within a 30-meter radius while sand is flowing into the test hole.",
                "Ensure the base plate is placed in full flat contact with the trimmed ground surface; gaps beneath the plate allow sand leakage.",
                "Do not drop sand jars or knock the funnel while the valve is open to prevent compaction of the calibrated sand.",
                "Seal excavated soil immediately in airtight containers to prevent evaporative moisture loss before laboratory weighing."
            ],
            "quiz": [
                {
                    "question": "The volume of the excavated test hole V_h in the sand cone method is calculated as:",
                    "options": ["V_h = M_used · ρ_sand", "V_h = (M_used - M_cone) / ρ_sand", "V_h = M_cone / ρ_sand", "V_h = M_wet / ρ_sand"],
                    "correct": 1,
                    "explanation": "Net sand filling the hole is (M_used - M_cone); dividing by calibrated sand density ρ_sand yields hole volume V_h."
                },
                {
                    "question": "The standard sand specified for the ASTM D1556 sand cone test is:",
                    "options": ["Crushed angular limestone dust", "Standard Ottawa silica sand (20-30 mesh)", "Well-graded gravelly sand", "Organic dune sand"],
                    "correct": 1,
                    "explanation": "ASTM D1556 specifies clean, dry, rounded Ottawa sand passing the 850 μm (No. 20) sieve and retained on 600 μm (No. 30)."
                },
                {
                    "question": "If in-situ dry density is 1.85 g/cm³ and Standard Proctor MDD is 1.90 g/cm³, Relative Compaction (RC) is:",
                    "options": ["92.5%", "95.0%", "97.4%", "102.7%"],
                    "correct": 2,
                    "explanation": "RC = (ρ_d / MDD) · 100% = (1.85 / 1.90) · 100% = 97.37% ≈ 97.4%."
                },
                {
                    "question": "Vibration of the test area while sand is flowing into the hole will result in:",
                    "options": ["An artificially low calculated dry density", "An artificially high calculated dry density", "Zero effect on density", "Premature hole collapse"],
                    "correct": 0,
                    "explanation": "Vibration densifies the sand, pulling more sand into the hole, artificially inflating V_h and lowering calculated ρ_d."
                }
            ],
            "samples": [1200.0, 1400.0, 1600.0, 1800.0, 2000.0, 2200.0, 2400.0],
            "measureLabel": "Record mass of dry excavated soil M_s",
            "readings": ["ms_dry_g", "vh_hole_cm3", "mwet_soil_g", "rel_compaction_pct"],
            "theory": """<h3>1. Volumetric Displacement Mechanics of the Sand Cone</h3>
<p>The determination of in-situ field density requires measuring the mass of soil excavated from a test hole and determining the exact volume of that irregular cavity. Let $M_{initial}$ be the total mass of the sand cone apparatus filled with dry Ottawa sand of pre-calibrated bulk density $\\rho_{sand}$. When the apparatus is inverted over the guide plate and the control valve opened, sand fills both the metal cone funnel and the excavated hole.</p>

<p>Upon closure of the valve, the remaining apparatus mass is $M_{final}$. The total mass of sand discharged is:</p>
\\[ M_{used} = M_{initial} - M_{final} \\]
<p>Because the cone funnel requires a fixed, pre-calibrated mass of sand $M_{cone}$ to fill its internal geometry, the net mass of sand occupying the excavated test hole $M_{hole}$ is:</p>
\\[ M_{hole} = M_{used} - M_{cone} \\]
<p>The excavated test hole volume $V_h$ is evaluated via fluid-like granular displacement:</p>
\\[ V_h = \\frac{M_{hole}}{\\rho_{sand}} = \\frac{M_{used} - M_{cone}}{\\rho_{sand}} \\]

<h3>2. In-Situ Density & Relative Compaction Formulations</h3>
<p>The excavated soil is weighed immediately to record moist mass $M_{wet}$. Oven drying determines gravimetric moisture content $w = M_w / M_s$. Dry soil mass $M_s$ is:</p>
\\[ M_s = \\frac{M_{wet}}{1 + w} \\]
<p>The in-situ dry density $\\rho_d$ is the ratio of dry soil mass to excavated hole volume:</p>
\\[ \\rho_d = \\frac{M_s}{V_h} = \\frac{M_{wet}}{V_h (1 + w)} \\]
<p>The degree of compaction achieved in the field is quantified by the Relative Compaction ($RC$):</p>
\\[ RC = \\frac{\\rho_d}{\\rho_{d,max(Proctor)}} \\times 100\\% \\]

<h3>3. Linear Excavation Response Model</h3>
<p>In this experimental investigation, across varying excavation hole volumes ($V_h = 1200\\text{ to }2400\\text{ cm}^3$), dry soil mass $M_s$ scales directly with cavity volume:</p>
\\[ M_s = \\rho_d \\cdot V_h \\]
<p>where $\\rho_d = 1.8500\\text{ g/cm}^3$ represents the calibrated in-situ field dry density.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this geotechnical engineering laboratory investigation is to determine the in-situ wet density, in-situ dry density, and relative compaction percentage ($RC$) of a compacted silty clay highway subgrade fill using the sand cone method according to ASTM D1556 / AASHTO T191. By logging dry excavated soil mass across seven test hole volumes ($1200\\text{ to }2400\\text{ cm}^3$) and executing linear regression, we determine field dry density $\\rho_d$ and evaluate QA/QC specification compliance.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Test hole volume $V_h$ is evaluated from net Ottawa sand displacement:</p>
\\[ V_h = \\frac{(M_{initial} - M_{final}) - M_{cone}}{\\rho_{sand}} \\]
<p>Dry soil mass $M_s$ relates linearly to hole volume $V_h$ through the in-situ dry density:</p>
\\[ M_s = \\rho_d \\cdot V_h \\]
<p>where $\\rho_d = 1.8500\\text{ g/cm}^3$ ($18.15\\text{ kN/m}^3$). Relative compaction is $RC = (\\rho_d / MDD) \\times 100\\%$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized a standard ASTM D1556 sand cone apparatus ($165\\text{ mm}$ metal funnel, $12.7\\text{ mm}$ valve, $4\\text{-liter}$ jar) and steel base plate ($300 \\times 300\\text{ mm}$). Standard Ottawa silica sand ($20\\text{-}30$ mesh) had calibrated bulk density $\\rho_{sand} = 1.420 \\pm 0.005\\text{ g/cm}^3$ and cone funnel constant $M_{cone} = 1560.0 \\pm 2.0\\text{ g}$. Mass measurements were logged with a digital field balance ($10.0\\text{ kg}$ capacity, precision $\\pm 0.1\\text{ g}$). Excavated soil was dried at $110 \\pm 5^\\circ\\text{C}$ to determine field moisture content ($w = 12.0\\%$).</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>The test surface on the compacted fill was prepared flat. The base plate was pinned to the ground. A cylindrical test hole was excavated to $\\sim 150\\text{ mm}$ depth, collecting all soil into airtight cans. The sand cone jar was weighed ($M_{initial}$), inverted over the plate, the valve opened, and sand allowed to settle under gravity until motion stopped. The valve was closed, remaining sand weighed ($M_{final}$), and net hole volume $V_h$ computed. Excavated soil was weighed moist ($M_{wet}$) and dried to determine $M_s$.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Field density testing on active earthwork sites involves proximity to heavy compactors and scrapers. Safety protocols required high-visibility reflective vests, steel-toed boots, and hard hats. All heavy construction traffic was halted within a $30\\text{-meter}$ radius during sand pouring.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the test matrix ($\rho_{sand} = 1.420\\text{ g/cm}^3$, $M_{cone} = 1560.0\\text{ g}$, $w = 12.0\\%$):</p>
<table>
<thead>
<tr><th>Test Hole</th><th>Hole Volume V_h (cm³)</th><th>Net Sand in Hole (g)</th><th>Moist Soil Mass M_wet (g)</th><th>Dry Soil Mass M_s (g)</th><th>In-Situ Dry Density ρ_d (g/cm³)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>1200.0</td><td>1704.0</td><td>2486.4</td><td>2220.0</td><td>1.850</td></tr>
<tr><td>2</td><td>1400.0</td><td>1988.0</td><td>2900.8</td><td>2590.0</td><td>1.850</td></tr>
<tr><td>3</td><td>1600.0</td><td>2272.0</td><td>3315.2</td><td>2960.0</td><td>1.850</td></tr>
<tr><td>4</td><td>1800.0</td><td>2556.0</td><td>3729.6</td><td>3330.0</td><td>1.850</td></tr>
<tr><td>5</td><td>2000.0</td><td>2840.0</td><td>4144.0</td><td>3700.0</td><td>1.850</td></tr>
<tr><td>6</td><td>2200.0</td><td>3124.0</td><td>4558.4</td><td>4070.0</td><td>1.850</td></tr>
<tr><td>7</td><td>2400.0</td><td>3408.0</td><td>4972.8</td><td>4440.0</td><td>1.850</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of dry soil mass $M_s$ versus hole volume $V_h$ yields:</p>
\\[ M_s = 1.85000 \\cdot V_h + 0.00000 \\]
<p>with an exceptional coefficient of determination $R^2 = 1.000000$. The experimental in-situ dry density $\\rho_d = 1.8500\\text{ g/cm}^3$ matches the reference benchmark with zero relative deviation ($0.00\\%$). Comparing against the Standard Proctor Maximum Dry Density ($MDD = 1.835\\text{ g/cm}^3$, from Laboratory 19):</p>
\\[ RC = \\frac{\\rho_d}{MDD} \\times 100\\% = \\frac{1.8500}{1.8350} \\times 100\\% = 100.82\\% \\]
<p>The field compaction achieved $100.8\\%$ of Standard Proctor MDD, comfortably exceeding the standard $95.0\\%$ project specification requirement.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include balance reading $\\delta M = \\pm 0.5\\text{ g}$, sand density calibration $\\delta \\rho_{sand} = \\pm 0.005\\text{ g/cm}^3$ ($0.35\\%$), and moisture determination $\\delta w = \\pm 0.1\\%$ ($0.09\\%$). Propagating into $\\rho_d$:</p>
\\[ \\frac{\\delta \\rho_d}{\\rho_d} = \\sqrt{ \\left( \\frac{\\delta M_s}{M_s} \\right)^2 + \\left( \\frac{\\delta V_h}{V_h} \\right)^2 } = \\pm 0.45\\% \\]
<p>The reported in-situ dry density is $\\rho_d = 1.8500 \\pm 0.0083\\text{ g/cm}^3$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The measured field dry density of $1.850\\text{ g/cm}^3$ at $12.0\\%$ moisture confirms that field compaction with heavy vibratory padfoot rollers imparted energy exceeding laboratory Standard Proctor compactive effort, operating close to the Modified Proctor envelope. Zero sand leakage beneath the base plate was confirmed by recovering clean boundary lines.</p>

<h3>10. Earthwork QA/QC Inspection Protocols</h3>
<p>In highway construction under FHWA guidelines, one sand cone verification test is mandated for every $1000\\text{ m}^2$ of placed fill layer. Achieving $RC = 100.8\\%$ permits immediate sign-off and placement of the subsequent lift without requiring re-rolling or moisture conditioning.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is Ottawa sand recovered from the hole discarded rather than reused immediately?</strong><br>
<em>A1:</em> Sand in the hole absorbs moisture from damp soil walls and picks up clay/silt dust particles, altering its grain shape and bulk density; it must be washed, re-sieved through No. 20 and No. 30 sieves, and oven dried before reuse.</p>
<p><strong>Q2: What is the rubber balloon method (ASTM D2167) and how does it compare?</strong><br>
<em>A2:</em> The rubber balloon method pumps water inside an elastic membrane into the test hole under pressure to read volume directly on a graduated cylinder; it is faster than the sand cone but less accurate in irregular or rocky holes where the balloon cannot conform to sharp crevices.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The sand cone field density test successfully verified the compaction quality of the earth fill. The calibrated in-situ dry density $\\rho_d = 1.8500\\text{ g/cm}^3$ ($R^2 = 1.000000$) and relative compaction $RC = 100.82\\%$ provide an authoritative benchmark for earthwork quality assurance in civil engineering infrastructure.</p>"""
        },
        {
            "number": 27,
            "slug": "california-bearing-ratio-cbr-subgrade-soils",
            "title": "California Bearing Ratio (CBR) of Compacted Pavement Subgrade & Base Soils",
            "shortTitle": "California Bearing Ratio (CBR)",
            "aim": "Determine the California Bearing Ratio (CBR) of compacted subgrade soil under soaked and unsoaked conditions, evaluate penetration resistance force (P), and determine pavement design thickness according to ASTM D1883 / AASHTO T193.",
            "inputLabel": "Piston Penetration Depth d",
            "shortInput": "Penetration d",
            "inputUnit": "mm",
            "min": 1.5,
            "max": 5.0,
            "step": 0.5,
            "initial": 2.5,
            "inputDecimals": 1,
            "rawLabel": "Penetration Resistance Force P",
            "rawUnit": "kN",
            "rawDecimals": 2,
            "xAxis": "Piston penetration depth d (mm)",
            "yAxis": "Penetration resistance force P (kN)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 6.0,
            "emptyY": 15.0,
            "targetName": "CBR Penetration Stiffness Slope",
            "target": "2.4000",
            "refValue": 2.4000,
            "resultUnit": "kN/mm",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "P = 2.4000 · d",
            "intro": "The California Bearing Ratio (CBR) is the universal empirical design parameter used worldwide in AASHTO, FAA, and Asphalt Institute methodologies for determining the structural thickness of flexible asphalt pavements and airport runways. Conceived by the California Division of Highways in the late 1920s, the CBR test (ASTM D1883) evaluates the mechanical shearing resistance of compacted subgrade, subbase, and base course soils relative to a standard crushed limestone base material. Soil prepared at Optimum Moisture Content (OMC) is compacted into a heavy cylindrical steel mold (152.4 mm diameter, 177.8 mm height) in five layers using a 4.54 kg rammer. To simulate the worst-case moisture scenario during seasonal spring thaws and monsoon floods, specimens are subjected to a 96-hour (4-day) soaking period in a water bath under surcharge weights simulating pavement overburden (minimum 4.54 kg), while swell dial gauges monitor vertical volumetric swelling. The soaked mold is then mounted in a motorized compression frame, and a hardened steel piston (49.63 mm diameter, cross-sectional area 1935 mm² / 3.0 in²) penetrates the soil at a standardized constant rate of 1.27 mm/min (0.05 in/min). Penetration force P is recorded at standard depths, notably 2.54 mm (0.1 in) and 5.08 mm (0.2 in). The CBR percentage is calculated by dividing measured piston resistance by the standard penetration resistance of high-grade crushed California stone (13.34 kN at 2.54 mm, and 20.00 kN at 5.08 mm): CBR% = (P / P_std) x 100%. In this laboratory, penetration force is logged across penetration depths from 1.5 to 5.0 mm to calibrate the penetration stiffness slope and extract the design CBR.",
            "modelExtra": "Compacted crushed aggregate base course soil tested in soaked state. Standard California reference loads: P_std(2.5 mm) = 13.34 kN, P_std(5.0 mm) = 20.00 kN. Linearized penetration force relates directly to penetration depth d with stiffness slope 2.4000 kN/mm. At d = 2.50 mm: P = 6.00 kN, yielding CBR = (6.00 / 13.34) · 100% = 45.0%.",
            "apparatus": [
                {"name": "Motorized CBR Loading Machine", "purpose": "Applies constant penetration rate of 1.27 mm/min (0.05 in/min) with electronic load cell up to 50 kN."},
                {"name": "Hardened Cylindrical Steel Penetration Piston", "purpose": "Machined piston with 49.63 ± 0.13 mm diameter (1935 mm² / 3.0 in² area) conforming to ASTM D1883."},
                {"name": "Heavy-Duty Steel CBR Compaction Molds", "purpose": "152.4 mm internal diameter by 177.8 mm height molds with perforated baseplates and collar."},
                {"name": "Annular & Slotted Steel Surcharge Weights", "purpose": "2.27 kg paired split weights simulating pavement pavement overburden stresses (4.54 kg total)."},
                {"name": "Soaking Water Bath & Swell Dial Indicator", "purpose": "4-day soaking tank with tripod dial indicator measuring vertical soil swell to 0.01 mm."},
                {"name": "Digital Linear Displacement Transducer (LVDT)", "purpose": "Monitors piston penetration depth d into soil with 0.001 mm resolution."}
            ],
            "procedure": [
                {"title": "Soil Moisture Dosing & Compaction", "text": "Mix 6.0 kg of base course soil at Optimum Moisture Content (OMC); compact into 152.4 mm CBR mold in five layers with 56 blows per layer of 4.54 kg rammer; trim surface flush."},
                {"title": "Surcharge Placement & 96-Hour Soaking", "text": "Place perforated swell plate and 4.54 kg surcharge weights on soil; mount swell dial gauge; submerge mold in water bath for 96 hours (4 days); record daily swell percentage."},
                {"title": "Post-Soak Draining & Surface Drying", "text": "Remove mold from bath; allow water to drain freely through baseplate for 15 minutes; remove surcharge weights; wipe excess surface water."},
                {"title": "CBR Machine Mounting & Seating", "text": "Place mold on machine platen; reposition 4.54 kg surcharge weights; seat penetration piston centrally with a small seating load of 45 N; zero load and displacement channels."},
                {"title": "Constant-Rate Piston Penetration", "text": "Engage machine at constant rate of 1.27 mm/min (0.05 in/min); log penetration force P at depths of 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, and 5.0 mm."},
                {"title": "CBR Calculation & Pavement Sizing", "text": "Plot force versus penetration depth; apply initial concave-upward zero correction if necessary; evaluate CBR at 2.5 mm and 5.0 mm; determine governing design CBR%."}
            ],
            "topics": [
                {"question": "Why are standard reference forces of 13.34 kN (2.5 mm) and 20.00 kN (5.0 mm) used in the CBR formula?", "answer": "The California Division of Highways tested an ideal, high-quality crushed California limestone rock; it required 13.34 kN (3000 lbf, 1000 psi) at 2.54 mm penetration and 20.00 kN (4500 lbf, 1500 psi) at 5.08 mm; tested soils are expressed as a percentage of this ideal standard."},
                {"question": "Why is the 96-hour (4-day) soaking period mandatory for pavement subgrade evaluation?", "answer": "Soaking simulates the worst-case moisture scenario during spring thaw or severe flooding; soil softens and absorbs water under capillary action, revealing potential loss of bearing capacity and expansive volumetric swelling."},
                {"question": "What is the purpose of placing surcharge weights on top of the soil during soaking and penetration?", "answer": "The surcharge weights (minimum 4.54 kg / 10 lbf) represent the confining overburden pressure exerted by overlying pavement asphalt concrete and base courses, preventing unrealistic unconfined surface heave."},
                {"question": "What corrective procedure is required if the load-penetration curve displays initial concave-upward curvature?", "answer": "Initial concave-upward curvature indicates surface irregularities or soft surface paste; ASTM D1883 mandates drawing a tangent to the point of steepest slope and extending it to intersect the zero-load axis to establish an adjusted zero-penetration datum."},
                {"question": "If CBR at 5.0 mm is greater than CBR at 2.5 mm, what protocol must be followed?", "answer": "Normally, CBR at 2.5 mm governs; if CBR at 5.0 mm is higher, the test must be repeated on a fresh sample; if the retest confirms the result, the higher 5.0 mm CBR is accepted as the design value."},
                {"question": "How is design CBR correlated to resilient modulus (M_r) in the AASHTO pavement design guide?", "answer": "AASHTO empirical design correlates resilient modulus to CBR via M_r (psi) ≈ 1500 · CBR (or M_r (MPa) ≈ 10.3 · CBR), directly governing asphalt pavement structural layer thickness."}
            ],
            "precautions": [
                "Maintain piston penetration rate strictly at 1.27 ± 0.05 mm/min; faster rates increase apparent resistance due to dynamic viscosity.",
                "Ensure surcharge weights are centered around the penetration piston without touching the piston shank during travel.",
                "Check that the 96-hour water bath maintains water levels covering the specimen top to ensure full saturation.",
                "Verify specimen top is flat and level; uneven surfaces cause eccentric piston contact and initial concave-upward curvature."
            ],
            "quiz": [
                {
                    "question": "The standard penetration rate of the CBR piston in ASTM D1883 is:",
                    "options": ["0.5 mm/min", "1.27 mm/min (0.05 in/min)", "5.0 mm/min", "10.0 mm/min"],
                    "correct": 1,
                    "explanation": "ASTM D1883 strictly mandates a continuous penetration rate of 1.27 mm/min (0.05 in/min)."
                },
                {
                    "question": "The standard reference force for 2.54 mm (0.1 in) penetration on standard crushed stone is:",
                    "options": ["4.45 kN (1000 lbf)", "13.34 kN (3000 lbf)", "20.00 kN (4500 lbf)", "50.00 kN (11200 lbf)"],
                    "correct": 1,
                    "explanation": "The standard California benchmark force at 2.54 mm (0.1 in) is 13.34 kN (3000 lbf / 1000 psi)."
                },
                {
                    "question": "The standard soaking duration to simulate worst-case groundwater saturation is:",
                    "options": ["12 hours", "24 hours", "48 hours", "96 hours (4 days)"],
                    "correct": 3,
                    "explanation": "ASTM D1883 requires a 96-hour (4-day) soaking period under surcharge weights."
                },
                {
                    "question": "If a soil requires a penetration force of 3.34 kN at 2.54 mm, its California Bearing Ratio (CBR) is:",
                    "options": ["10%", "25%", "50%", "75%"],
                    "correct": 1,
                    "explanation": "CBR = (3.34 kN / 13.34 kN) · 100% = 25.04% ≈ 25%."
                }
            ],
            "samples": [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
            "measureLabel": "Record CBR piston penetration force P",
            "readings": ["force_kn", "penetration_mm", "cbr_25_pct", "pavement_thick_mm"],
            "theory": """<h3>1. Empirical Mechanics of the California Bearing Ratio</h3>
<p>The CBR test is an empirical punching shear penetration test. When a flat-ended cylindrical steel piston of diameter $D_p = 49.63\\text{ mm}$ (cross-sectional area $A_p = 1935.0\\text{ mm}^2 = 3.0\\text{ in}^2$) is forced into compacted soil at a constant displacement rate of $1.27\\text{ mm/min}$, it generates a localized plastic bearing capacity failure zone directly beneath the circular punch.</p>

<p>According to Prandtl–Reissner plastic bearing capacity theory, the penetration resistance $P$ combines undrained shear cohesion $c_u$ and frictional resistance mobilized under surcharge confining pressure $q_{sur}$:</p>
\\[ q_p = \\frac{P}{A_p} = c N_c + q_{sur} N_q + \\frac{1}{2} \\gamma D_p N_\\gamma \\]
<p>Because soil exhibits strain-hardening and progressive shear mobilization, the resisting force $P$ increases monotonically with penetration depth $d$.</p>

<h3>2. The CBR Formulation</h3>
<p>The California Bearing Ratio ($CBR$) expresses measured resistance force $P$ as a percentage of the standard benchmark force $P_{std}$ established on crushed California limestone:</p>
\\[ CBR_{2.5} = \\frac{P_{2.5}}{13.34\\text{ kN}} \\times 100\\% \\]
\\[ CBR_{5.0} = \\frac{P_{5.0}}{20.00\\text{ kN}} \\times 100\\% \\]
<p>Normally, $CBR_{2.5}$ governs. If $CBR_{5.0} > CBR_{2.5}$, the test is repeated; if confirmed, $CBR_{5.0}$ is adopted as the governing design metric.</p>

<h3>3. Linear Penetration Stiffness Model</h3>
<p>Across the linear penetration regime ($d = 1.5\\text{ to }5.0\\text{ mm}$), penetration resistance $P$ scales directly with displacement depth:</p>
\\[ P = k_{cbr} \\cdot d \\]
<p>where $k_{cbr} = 2.4000\\text{ kN/mm}$ represents the penetration stiffness slope. At standard depth $d = 2.50\\text{ mm}$:</p>
\\[ P(2.5) = 2.4000 \\times 2.50 = 6.000\\text{ kN} \\implies CBR_{2.5} = \\frac{6.000}{13.34} \\times 100\\% = 44.98\\% \\approx 45.0\\% \\]
<p>characteristic of high-strength crushed stone aggregate base course materials.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>The primary objective of this geotechnical and highway engineering laboratory investigation is to evaluate the California Bearing Ratio ($CBR$), load-penetration stiffness, and 96-hour soaking swell of a compacted pavement base course material according to ASTM D1883 / AASHTO T193 across eight penetration depths ($d = 1.5\\text{ to }5.0\\text{ mm}$). By logging penetration resistance force $P$ and executing linear regression, we determine the penetration stiffness slope $k_{cbr}$ and calculate pavement structural thickness.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Piston penetration resistance force $P$ varies linearly with penetration depth $d$ according to:</p>
\\[ P = k_{cbr} \\cdot d \\]
<p>where $k_{cbr} = 2.4000\\text{ kN/mm}$. The California Bearing Ratio ($CBR$) at standard depths $2.5\\text{ mm}$ and $5.0\\text{ mm}$ is:</p>
\\[ CBR_{2.5} = \\frac{P(2.5\\text{ mm})}{13.34\\text{ kN}} \\times 100\\%, \\qquad CBR_{5.0} = \\frac{P(5.0\\text{ mm})}{20.00\\text{ kN}} \\times 100\\% \\]

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Testing utilized a computerized electromechanical CBR testing machine equipped with a $50.0\\text{ kN}$ load cell (precision $\\pm 0.05\\text{ kN}$) and a digital LVDT penetration transducer ($0.001\\text{ mm}$ resolution). The hardened circular steel piston possessed diameter $D_p = 49.63 \\pm 0.05\\text{ mm}$ ($A_p = 1935.0\\text{ mm}^2$). Specimen containment utilized a heavy steel CBR mold ($152.4\\text{ mm}$ diameter, $177.8\\text{ mm}$ height) with perforated baseplate and $4.54\\text{ kg}$ slotted surcharge weights. Soaking swell was monitored with a mechanical dial gauge ($0.01\\text{ mm}$ resolution).</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Base course soil was blended at $OMC = 8.5\\%$, compacted into the mold in five layers with 56 blows per layer of the $4.54\\text{ kg}$ rammer, trimmed flush, and fitted with the $4.54\\text{ kg}$ surcharge. The assembly was submerged in a water bath for 96 hours, recording $0.12\\%$ volumetric swell. After 15 minutes gravity draining, the mold was mounted in the CBR machine with surcharge. The piston was seated at $45\\text{ N}$, zeroed, and driven at $1.27\\text{ mm/min}$, logging force $P$ at $0.5\\text{ mm}$ increments up to $5.0\\text{ mm}$.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Heavy $4.54\\text{ kg}$ surcharge weights and $12\\text{ kg}$ steel compaction molds present pinch and lifting hazards. Operators wore steel-toed safety boots, leather gloves, and eye protection. Ergonomic two-handed lifting techniques were enforced.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following systematic observations were recorded across the CBR penetration test (96-hr soaked condition):</p>
<table>
<thead>
<tr><th>Point</th><th>Penetration Depth d (mm)</th><th>Penetration Force P (kN)</th><th>Piston Pressure (MPa)</th><th>Benchmark Force (kN)</th><th>Incremental CBR (%)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>1.5</td><td>3.60</td><td>1.86</td><td>—</td><td>—</td></tr>
<tr><td>2</td><td>2.0</td><td>4.80</td><td>2.48</td><td>—</td><td>—</td></tr>
<tr><td>3</td><td>2.5</td><td>6.00</td><td>3.10</td><td>13.34</td><td>44.98</td></tr>
<tr><td>4</td><td>3.0</td><td>7.20</td><td>3.72</td><td>—</td><td>—</td></tr>
<tr><td>5</td><td>3.5</td><td>8.40</td><td>4.34</td><td>—</td><td>—</td></tr>
<tr><td>6</td><td>4.0</td><td>9.60</td><td>4.96</td><td>—</td><td>—</td></tr>
<tr><td>7</td><td>4.5</td><td>10.80</td><td>5.58</td><td>—</td><td>—</td></tr>
<tr><td>8</td><td>5.0</td><td>12.00</td><td>6.20</td><td>20.00</td><td>60.00</td></tr>
</tbody>
</table>
<p>96-hour volumetric swell was $0.024\\text{ mm}$ ($0.12\\%$), confirming high dimensional stability.</p>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of penetration resistance force $P$ versus penetration depth $d$ yields:</p>
\\[ P = 2.40000 \\cdot d + 0.00000 \\]
<p>with an exceptional coefficient of determination $R^2 = 1.000000$. The experimental stiffness slope $k_{cbr} = 2.4000\\text{ kN/mm}$ matches the design benchmark with zero relative deviation ($0.00\\%$). Calculating California Bearing Ratio at standard depths:</p>
\\[ CBR_{2.5} = \\frac{6.00\\text{ kN}}{13.34\\text{ kN}} \\times 100\\% = 44.98\\% \\]
\\[ CBR_{5.0} = \\frac{12.00\\text{ kN}}{20.00\\text{ kN}} \\times 100\\% = 60.00\\% \\]
<p>Because $CBR_{5.0} > CBR_{2.5}$, verification retesting confirmed the result; the governing design value is $CBR = 45.0\\%$ (or $60.0\\%$ under AASHTO 5.0 mm criteria), classifying the material as an exceptional crushed stone base course.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainties include load cell reading $\\delta P = \\pm 0.05\\text{ kN}$ ($0.83\\%$) and LVDT penetration depth $\\delta d = \\pm 0.01\\text{ mm}$ ($0.40\\%$). Propagating into $CBR_{2.5}$:</p>
\\[ \\frac{\\delta CBR}{CBR} = \\sqrt{ \\left( \\frac{\\delta P}{P} \\right)^2 + \\left( \\frac{\\delta d}{d} \\right)^2 } = \\pm 0.92\\% \\]
<p>The reported California Bearing Ratio is $CBR_{2.5} = 45.0 \\pm 0.4\\%$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The linear load-penetration response confirms immediate mechanical interlock without initial bedding concavity. High-density packing ($MDD = 2.15\\text{ g/cm}^3$) of crushed limestone particles prevented punching shear collapse, mobilizing intense internal friction ($\\phi > 42^\\circ$). Minimal soaking swell ($0.12\\% < 2.0\\%$) ensures resistance to frost heave and moisture softening.</p>

<h3>10. Flexible Pavement Structural Layer Sizing</h3>
<p>Under the AASHTO flexible pavement design guide, resilient modulus is estimated as $M_r \\approx 10.3 \\times CBR = 10.3 \\times 45.0 = 463.5\\text{ MPa}$ ($67,200\\text{ psi}$). This high modulus provides a layer structural coefficient $a_2 = 0.14$, permitting a significant reduction in required surface asphalt concrete thickness while maintaining design structural number ($SN$) over 20-year design traffic loads.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is an initial concave-upward load-penetration curve corrected by shifting the origin?</strong><br>
<em>A1:</em> Concave-upward curvature indicates surface roughness or a loose top layer before the piston engages true solid soil; drawing a tangent to the steepest linear portion and extending it to the zero-load axis resets the origin, ensuring penetration depths are measured from true solid contact.</p>
<p><strong>Q2: What typical CBR values are observed for clay subgrades versus crushed rock base courses?</strong><br>
<em>A2:</em> Weak clay subgrades exhibit $CBR = 2\\text{ to }5\\%$; silty sands range from $10\\text{ to }20\\%$; well-graded crushed gravel subbases achieve $30\\text{ to }50\\%$; high-grade crushed limestone bases exceed $80\\text{ to }100\\%$.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The California Bearing Ratio investigation verified the mechanical bearing resistance of the compacted pavement base material. The calibrated stiffness slope $k_{cbr} = 2.4000\\text{ kN/mm}$ ($R^2 = 1.000000$), $CBR_{2.5} = 45.0\\%$, and minimal swell of $0.12\\%$ confirm full compliance with AASHTO specifications for heavy-duty highway pavement construction.</p>"""
        }
    ]
