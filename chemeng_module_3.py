# -*- coding: utf-8 -*-
"""Chemical & Process Engineering Module 3: Mass Transfer, Distillation & Separation Processes (Labs 17–24)."""

def get_module_3():
    return [
        {
            "number": 17,
            "slug": "fractional-distillation-mccabe-thiele-reflux",
            "title": "Fractional Distillation Column Reflux Ratio & McCabe–Thiele Tray Efficiency",
            "shortTitle": "Fractional Distillation Column",
            "aim": "Operate a continuous sieve-tray distillation column separating an ethanol–water mixture across variable external reflux ratios R, determine distillate purity x_D, and calculate overall Murphree plate efficiency via McCabe–Thiele graphical construction.",
            "inputLabel": "External Reflux Ratio R",
            "shortInput": "Reflux R",
            "inputUnit": "ratio",
            "min": 1.0,
            "max": 6.0,
            "step": 1.0,
            "initial": 3.0,
            "inputDecimals": 1,
            "rawLabel": "Distillate Enrichment Factor 1/(1 - x_D)",
            "rawUnit": "ratio",
            "rawDecimals": 2,
            "xAxis": "External reflux ratio R (L/D)",
            "yAxis": "Distillate enrichment factor 1/(1 - x_D)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.5,
            "emptyY": 11.2,
            "targetName": "Reflux Separation Enrichment Slope S",
            "target": "2.8500",
            "refValue": 2.8500,
            "resultUnit": "ratio",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "1/(1 - x_D) = S · R + c_0 = 2.8500 · R + 1.2500",
            "intro": "Fractional distillation is the most widely deployed thermal separation process in the chemical, petrochemical, and pharmaceutical industries, responsible for purifying petroleum fractions, petrochemical intermediates, and alcoholic spirits. In a staged tray column, liquid flows downward across horizontal perforated trays while vapor bubbles upward through perforations or bubble caps, facilitating intimate vapor-liquid mass transfer. On each tray, the more volatile component (ethanol) preferentially vaporizes into the ascending vapor stream, while the less volatile component (water) condenses into the descending liquid stream. Warren L. McCabe and Ernest W. Thiele (1925) formulated the seminal graphical method for determining the theoretical number of equilibrium stages required for a specified separation. Crucially, column performance is governed by the external reflux ratio R = L / D (liquid returned to the column divided by overhead distillate product withdrawn). Increasing the reflux ratio steepens the rectifying operating line (slope = R / (R + 1)), expanding the driving force between the operating line and the vapor-liquid equilibrium (VLE) curve. Consequently, distillate overhead purity x_D increases systematically toward the ethanol-water azeotrope (89.4 mol% ethanol at 1 atm), causing the enrichment factor 1 / (1 - x_D) to scale linearly with reflux ratio R. In this laboratory investigation, an instrumented 10-sieve-tray glass distillation column is operated across reflux ratios from 1.0 to 6.0 to evaluate distillate enrichment slope S and calculate overall Murphree tray efficiency.",
            "modelExtra": "Evaluated using a 10-tray Oldershaw sieve column (internal diameter 50 mm, tray spacing 50 mm) separating a 15.0 mol% ethanol-water feed at atmospheric pressure. Linear regression models 1/(1 - x_D) versus reflux ratio R to extract slope S = 2.8500.",
            "apparatus": [
                {"name": "10-Tray Oldershaw Sieve Column with Vacuum Silvered Jacket", "purpose": "Provides 10 visual sieve trays with downcomers inside vacuum-jacketed adiabatic glass column."},
                {"name": "Thermostatically Controlled Reboiler Mantle", "purpose": "1.5 kW electric heating mantle boiling bottoms liquid with internal quartz temperature sensor."},
                {"name": "Solenoid-Actuated Dividing Reflux Head", "purpose": "Automated magnetic liquid dividing funnel providing digital reflux ratio control from 0.5 to total reflux."},
                {"name": "Shell-and-Tube Overhead Total Condenser", "purpose": "Condenses 100% of overhead vapor at 15.0 °C to provide subcooled liquid reflux and distillate product."},
                {"name": "Precision Digital Density Meter (Oscillating U-Tube)", "purpose": "Measures sample density at 20.000 °C to determine ethanol mole fraction with 0.0001 resolution."},
                {"name": "Thermocouple Array at Reboiler, Feed, and Overhead", "purpose": "Continuously logs column thermal profile (T_reb, T_feed, T_top) with 0.05 °C accuracy."}
            ],
            "procedure": [
                {"title": "Feed Preparation & Column Priming", "text": "Charge the reboiler with 2.0 L of 15.0 mol% (30.8 wt%) ethanol-water mixture; turn on cooling water to the overhead condenser at 5.0 L/min."},
                {"title": "Total Reflux Boil-Up Equilibration", "text": "Energize reboiler at 800 W and operate under total reflux (R = ∞) for 30 minutes until all 10 trays are actively bubbling and temperatures stabilize."},
                {"title": "Initial Reflux Ratio Setting", "text": "Set the magnetic reflux timer to R = 1.0 (5 s reflux, 5 s distillate withdrawal); maintain steady reboiler heat duty."},
                {"title": "Distillate & Bottoms Sampling", "text": "Allow 20 minutes to reach compositional steady state; draw 5 mL samples of overhead distillate and bottoms liquor through septum ports."},
                {"title": "Reflux Ratio Progression Protocol", "text": "Step reflux ratio through 2.0, 3.0, 4.0, 5.0, and 6.0, allowing 20 minutes of steady-state equilibration before sampling at each plateau."},
                {"title": "McCabe–Thiele & Tray Efficiency Analysis", "text": "Measure sample ethanol mole fractions x_D and x_B using the density meter, plot 1/(1 - x_D) versus R to extract slope S, and construct McCabe–Thiele stage steps."}
            ],
            "topics": [
                {"question": "What is the physical meaning of minimum reflux ratio R_min and total reflux R = ∞?", "answer": "At minimum reflux ratio R_min, an infinite number of trays is required to achieve the desired separation because the operating line touches the equilibrium curve (pinch point); at total reflux (R = ∞, D = 0), the minimum number of theoretical stages (Fenske limit) is required."},
                {"question": "How is the Murphree vapor tray efficiency E_MV defined and calculated?", "answer": "Murphree vapor efficiency is E_MV = (y_n - y_n+1) / (y*_n - y_n+1), comparing the actual vapor enrichment across tray n to the ideal enrichment that would occur if exiting vapor were in thermodynamic equilibrium with exiting liquid."},
                {"question": "What is the ethanol–water azeotrope and why can it not be separated by conventional distillation?", "answer": "At 89.4 mol% (95.6 wt%) ethanol at 1 atm (boiling point 78.15 °C), the liquid and vapor equilibrium compositions become identical (x = y); relative volatility α = 1.0, rendering further separation by standard distillation thermodynamically impossible."},
                {"question": "How does feed thermal condition (the q-value) affect distillation column operation?", "answer": "The feed quality q represents the fraction of liquid in the feed; q > 1 is subcooled liquid, q = 1 is saturated liquid, 0 < q < 1 is two-phase, q = 0 is saturated vapor, and q < 0 is superheated vapor, determining the slope of the feed line (-q / (1 - q))."},
                {"question": "What are weeping and entrainment (flooding) in sieve tray distillation columns?", "answer": "Weeping occurs at low vapor velocity when liquid drains prematurely through tray perforations instead of flowing down downcomers; flooding occurs at excessive vapor velocity when liquid droplets are carried upward into the tray above, destroying separation."},
                {"question": "Why is the McCabe–Thiele method based on the assumption of Constant Molar Overflow (CMO)?", "answer": "CMO assumes molar heats of vaporization of both components are equal and sensible heat/heat of mixing effects are negligible, meaning one mole of vapor condensing evaporates exactly one mole of liquid, keeping liquid and vapor molar flow rates constant in each section."}
            ],
            "precautions": [
                "Ethanol vapors are flammable; ensure all joints are gas-tight and conduct testing inside a certified fume hood.",
                "Verify cooling water is circulating through the overhead condenser before turning on the reboiler heating mantle.",
                "Allow at least 20 minutes of steady operation after altering reflux ratio to establish true compositional equilibrium.",
                "Cool drawn samples to exactly 20.0 °C before injecting into the digital density meter."
            ],
            "quiz": [
                {
                    "question": "At total reflux (R = ∞), the rectifying operating line on a McCabe–Thiele diagram:",
                    "options": ["Has a slope equal to 0", "Coincides exactly with the 45° diagonal line (y = x)", "Becomes completely vertical", "Intersects the equilibrium curve at the pinch point"],
                    "correct": 1,
                    "explanation": "The rectifying operating line slope is R / (R + 1); as R → ∞, R / (R + 1) → 1, making the operating line identical to the 45° diagonal line."
                },
                {
                    "question": "The ethanol–water system at atmospheric pressure forms a minimum-boiling azeotrope at approximately:",
                    "options": ["50.0 mol% ethanol", "89.4 mol% ethanol (95.6 wt%)", "99.9 mol% ethanol", "No azeotrope forms"],
                    "correct": 1,
                    "explanation": "Ethanol and water form a celebrated minimum-boiling azeotrope at 89.4 mol% (95.6 wt%) ethanol, boiling at 78.15 °C."
                },
                {
                    "question": "If a distillation column experiences severe weeping on its sieve trays, the Murphree tray efficiency will:",
                    "options": ["Increase dramatically", "Remain completely unaffected", "Drop significantly due to liquid bypassing without contacting vapor", "Exceed 100%"],
                    "correct": 2,
                    "explanation": "Weeping causes liquid to dump directly through perforations, bypassing the vapor bubble contact zone and severely degrading tray efficiency."
                },
                {
                    "question": "The Fenske equation is used in distillation column design to calculate:",
                    "options": ["The maximum allowable column diameter to avoid flooding", "The minimum number of theoretical stages at total reflux", "The reboiler heating duty", "The Murphree tray efficiency"],
                    "correct": 1,
                    "explanation": "The Fenske equation calculates the absolute minimum number of theoretical equilibrium stages required for a binary separation under total reflux (R = ∞)."
                }
            ],
            "samples": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "measureLabel": "Record distillate composition and reflux ratio",
            "readings": ["enrichment_factor", "reflux_ratio", "distillate_xd", "tray_efficiency"],
            "theory": """<h3>1. Principles of Staged Vapor-Liquid Equilibrium Separations</h3>
<p>Distillation exploits differences in relative volatility $\\alpha_{AB} = (y_A / x_A) / (y_B / x_B)$ to separate liquid mixtures through repeated vaporization and condensation. In a continuous fractionating column, descending liquid reflux scrubs heavier components from ascending vapor, while ascending vapor strips volatile components from descending liquid.</p>

<h3>2. The McCabe–Thiele Graphical Method</h3>
<p>Under the assumption of Constant Molar Overflow (CMO), the molar liquid flow rate $L$ and vapor flow rate $V$ remain constant within the rectifying section. An envelope mass balance around the top of the column yields the rectifying operating line:</p>
\\[ y_{n+1} = \\frac{L}{V} x_n + \\frac{D}{V} x_D = \\frac{R}{R + 1} x_n + \\frac{1}{R + 1} x_D \\]
<p>where $R = L / D$ is the external reflux ratio. As $R$ increases, the slope $R / (R + 1)$ approaches unity, shifting the operating line closer to the $45^\\circ$ diagonal line ($y = x$) and widening the vertical driving force $(y^* - y)$ between the operating line and the vapor-liquid equilibrium (VLE) curve.</p>

<h3>3. Distillate Enrichment & Reflux Ratio Modeling</h3>
<p>As reflux ratio $R$ increases, distillate overhead purity $x_D$ approaches the thermodynamic azeotropic limit ($x_{az} \\approx 0.894$ for ethanol-water at $1\\text{ atm}$). The remaining impurity $(1 - x_D)$ decreases inversely with reflux ratio. Defining the enrichment factor $Y = 1 / (1 - x_D)$:</p>
\\[ Y = \\frac{1}{1 - x_D} = S \\cdot R + c_0 \\]
<p>where $S$ is the reflux separation enrichment slope and $c_0$ is the minimum enrichment intercept. Plotting $1 / (1 - x_D)$ versus $R$ yields a straight line whose slope $S$ quantifies column rectifying performance.</p>

<h3>4. Overall Murphree Tray Efficiency</h3>
<p>The overall column efficiency $E_o$ compares the number of theoretical equilibrium stages $N_{theor}$ stepped off on the McCabe–Thiele diagram to the actual physical number of trays $N_{act}$ ($10\\text{ trays}$):</p>
\\[ E_o = \\frac{N_{theor}}{N_{act}} \\]
<p>For industrial sieve trays in ethanol-water service, overall tray efficiency typically ranges between $65\\%$ and $80\\%$.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>This laboratory investigation evaluates the rectifying performance of a 10-tray Oldershaw sieve-plate distillation column ($D = 50.0\\text{ mm}$) separating a $15.0\\text{ mol}\\%$ ethanol-water feed at atmospheric pressure ($1.013\\text{ bar}$). By varying external reflux ratio $R = L/D$ from $1.0$ to $6.0$ at constant reboiler boil-up duty ($800\\text{ W}$), we measure distillate ethanol mole fraction $x_D$, verify the enrichment model $1 / (1 - x_D) = S \\cdot R + c_0$, determine the separation slope $S = 2.8500$, and evaluate Murphree tray efficiency via McCabe–Thiele construction.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Material balance across the rectifying section defines the operating line $y = \\frac{R}{R+1} x + \\frac{1}{R+1} x_D$. Distillate overhead enrichment obeys:</p>
\\[ \\frac{1}{1 - x_D} = S \\cdot R + c_0 \\]
<p>where $S = 2.8500$ represents the experimental reflux sensitivity slope and $c_0 = 1.2500$ is the intercept. Overall column efficiency is computed via $E_o = N_{theor} / N_{actual}$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>The column comprises a vacuum-silvered, adiabatic glass Oldershaw column containing 10 sieve trays (perforated hole diameter $1.0\\text{ mm}$, free hole area $8.5\\%$, tray spacing $50\\text{ mm}$) with downcomers. The reboiler consists of a $2.0\\text{ L}$ spherical flask heated by an electric mantle ($800\\text{ W}$). Reflux is controlled by a solenoid-operated magnetic tilting funnel. Sample densities are measured using an Anton Paar DMA 4500 oscillating U-tube density meter ($\pm 0.00005\\text{ g/cm}^3$ at $20.000^\\circ\\text{C}$) to determine ethanol mole fractions.</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>The column was charged with $15.0\\text{ mol}\\%$ ethanol-water and brought to steady boil-up under total reflux for 30 minutes. Reflux ratio was set to $R = 1.0$. After 20 minutes of steady state, distillate and bottoms samples were collected. Reflux ratio was stepped through $2.0, 3.0, 4.0, 5.0,$ and $6.0$. Trays were visually inspected for weeping and entrainment. Temperatures at the reboiler ($T_{reb}$), feed tray ($T_{feed}$), and column top ($T_{top}$) were logged continuously.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Ethanol vapors form explosive mixtures with air (flash point $13^\\circ\\text{C}$). The apparatus was operated in a certified walk-in fume hood with grounded electrical connections. Safety splash goggles, lab coats, and fire extinguishers were immediately accessible.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following measurements were recorded at steady boil-up rate ($V = 1.85\\text{ kmol/h}$, feed $x_F = 0.1500$, atmospheric pressure $1.013\\text{ bar}$):</p>
<table>
<thead>
<tr><th>Run</th><th>Reflux Ratio $R$</th><th>Top Temp $T_{top}$ (°C)</th><th>Distillate $x_D$ (mol/mol)</th><th>Distillate (wt%)</th><th>Enrichment $1/(1 - x_D)$</th><th>Theoretical Stages $N_{theor}$</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>1.0</td><td>79.45</td><td>0.7561</td><td>87.42</td><td>4.10</td><td>4.8</td></tr>
<tr><td>2</td><td>2.0</td><td>78.82</td><td>0.8561</td><td>93.58</td><td>6.95</td><td>6.2</td></tr>
<tr><td>3</td><td>3.0</td><td>78.48</td><td>0.8980</td><td>95.78</td><td>9.80</td><td>7.1</td></tr>
<tr><td>4</td><td>4.0</td><td>78.30</td><td>0.9210</td><td>96.86</td><td>12.65</td><td>7.6</td></tr>
<tr><td>5</td><td>5.0</td><td>78.22</td><td>0.9355</td><td>97.50</td><td>15.50</td><td>7.9</td></tr>
<tr><td>6</td><td>6.0</td><td>78.18</td><td>0.9455</td><td>97.92</td><td>18.35</td><td>8.1</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of enrichment factor $1 / (1 - x_D)$ versus reflux ratio $R$ yields:</p>
\\[ \\frac{1}{1 - x_D} = 2.85000 \\cdot R + 1.25000 \\]
<p>with coefficient of determination $R^2 = 0.999999$. The experimental slope $S = 2.85000$ exactly matches the design calibration target ($2.8500$). Stepping theoretical stages on the McCabe–Thiele diagram at $R = 3.0$ yielded $N_{theor} = 7.1\\text{ stages}$. The overall column efficiency is:</p>
\\[ E_o = \\frac{N_{theor}}{N_{act}} = \\frac{7.1}{10} = 0.710 = 71.0\\% \\]
<p>which is within the standard expected range for Oldershaw sieve plates ($70\\%$ to $75\\%$).</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Digital density measurement error is $\\pm 0.0001\\text{ g/cm}^3$, corresponding to $\\delta x_D = \\pm 0.0002$. Timing accuracy of the magnetic reflux divider is $\\pm 0.05\\text{ s}$ ($\delta R / R = \\pm 0.8\\%$). Propagating errors into enrichment slope $S$ yields an experimental uncertainty of $\\pm 1.1\\%$, reporting $S = 2.8500 \\pm 0.0314$ and $E_o = 71.0 \\pm 1.5\\%$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>As reflux ratio increased from $1.0$ to $6.0$, overhead purity $x_D$ improved from $75.6\\text{ mol}\\%$ to $94.6\\text{ mol}\\%$ (close to the $89.4\\text{ mol}\\%$ azeotrope; note that small non-ideal vapor carryover or local subcooling can shift apparent optical concentrations). The diminishing returns in purity above $R = 4.0$ illustrate the economic trade-off: higher reflux ratios require substantially larger reboiler energy consumption ($q_{reb} \\propto R + 1$) for marginal gains in purity.</p>

<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>
<p>In petrochemical fractionation columns (e.g., ethylene/ethane splitters with $> 120\\text{ trays}$), reflux ratio is optimized around $1.1 R_{min}$ to $1.2 R_{min}$ to minimize total annualized capital and energy costs. Advanced control systems utilize online composition analyzers to trim reflux ratio dynamically against feed composition fluctuations.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is an Oldershaw column vacuum-jacketed with silvering?</strong><br>
<em>A1:</em> Small-diameter laboratory columns have very high surface-area-to-volume ratios; without vacuum silvering, ambient heat loss would cause uncontrolled vapor condensation along column walls, violating the Constant Molar Overflow (CMO) assumption.</p>
<p><strong>Q2: How can ethanol be purified beyond the $89.4\\text{ mol}\\%$ azeotrope in industrial plants?</strong><br>
<em>A2:</em> By breaking the azeotrope using pressure-swing distillation (exploiting azeotropic shift with pressure), extractive distillation with entrainers (e.g., ethylene glycol), or passing overhead vapor through zeolite 3A molecular sieve adsorption beds.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The fractional distillation experiment validated staged separation theory and the McCabe–Thiele method. The calibrated enrichment slope $S = 2.8500$ ($1/(1-x_D) = 2.8500 \\cdot R + 1.2500$) and measured overall tray efficiency $E_o = 71.0\\%$ provide precise empirical metrics for chemical distillation design.</p>"""
        },
        {
            "number": 18,
            "slug": "gas-absorption-packed-column-mass-transfer-kga",
            "title": "Packed Column Gas Absorption & Volumetric Mass Transfer Coefficient K_G a",
            "shortTitle": "Gas Absorption in Packed Column",
            "aim": "Operate a continuous counter-current packed absorption column absorbing carbon dioxide from air into water, measure inlet and outlet gas concentrations, and evaluate the volumetric overall mass transfer coefficient K_G a and Height of a Transfer Unit (HTU).",
            "inputLabel": "Liquid Solvent Irrigation Rate L",
            "shortInput": "Liquid Rate L",
            "inputUnit": "L/(min·m^2)",
            "min": 10.0,
            "max": 60.0,
            "step": 10.0,
            "initial": 30.0,
            "inputDecimals": 1,
            "rawLabel": "Mass Transfer Factor (K_G a)",
            "rawUnit": "kmol/(m^3·h·bar)",
            "rawDecimals": 3,
            "xAxis": "Liquid irrigation factor L^0.7 ((L/(min·m^2))^0.7)",
            "yAxis": "Volumetric mass transfer coefficient K_G a (kmol/(m^3·h·bar))",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 12.0,
            "emptyY": 1.4,
            "targetName": "Absorption Mass Transfer Slope S",
            "target": "0.0820",
            "refValue": 0.0820,
            "resultUnit": "kmol/(m^3·h·bar)/(L/(min·m^2))^0.7",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "K_G a = S · L^0.7 = 0.0820 · L^0.7",
            "intro": "Gas absorption (scrubbing) is a fundamental mass transfer separation operation in chemical plants, environmental emissions control, and synthesis gas purification, responsible for removing acid gases (CO_2, H_2S, SO_2) from gas streams by dissolving them into a liquid solvent. In a counter-current packed tower, gas enters at the bottom and ascends through packing, while liquid solvent is distributed over the top and trickles downward over packing elements (such as Raschig rings or structured gauze). Interfacial mass transfer is described by the two-film theory of Whitman (1923), which posits stagnant gas and liquid films on either side of the phase interface. The volumetric mass transfer rate is N_A · a = K_G a · (P_A - P_A*), where K_G a is the overall volumetric gas-phase mass transfer coefficient, 'a' is the effective gas-liquid interfacial area per unit packed volume, P_A is solute partial pressure in the bulk gas, and P_A* is equilibrium partial pressure over the liquid. For physical absorption of sparingly soluble gases like carbon dioxide in water, liquid film resistance dominates overall transport: 1 / K_G a = 1 / (k_G a) + H / (k_L a), where H is Henry's law constant. According to Onda's classic packed bed mass transfer correlations, liquid-side mass transfer coefficient k_L and wetted specific area 'a' scale with liquid mass velocity as L^0.7. In this laboratory investigation, an instrumented 1.5-meter packed tower absorbing CO_2 into water is operated across liquid irrigation rates from 10.0 to 60.0 L/(min·m^2) to measure K_G a, verify L^0.7 scaling, and determine the Height of a Transfer Unit (HTU).",
            "modelExtra": "Evaluated using a 100 mm ID acrylic column packed to 1.50 m with 10 mm ceramic Raschig rings (specific area a_p = 440 m^2/m^3). Gas feed contains 5.0 mol% CO_2 in air at constant flow G = 25.0 kg/(h·m^2). Linear regression models K_G a versus L^0.7.",
            "apparatus": [
                {"name": "Counter-Current Packed Absorption Column", "purpose": "100 mm ID clear acrylic column packed to 1.50 m with 10 mm ceramic Raschig rings."},
                {"name": "Multi-Point Liquid Spray Distributor", "purpose": "Provides uniform liquid irrigation over column cross-section without wall channeling."},
                {"name": "Gas Mixing & Blending Manifold", "purpose": "Blends industrial compressed air with CO_2 from cylinder to maintain stable 5.0 mol% feed."},
                {"name": "Non-Dispersive Infrared (NDIR) CO_2 Gas Analyzer", "purpose": "Measures inlet and outlet gas CO_2 volume concentrations from 0 to 10.0% with 0.01% precision."},
                {"name": "Positive-Displacement Liquid Solvent Pump", "purpose": "Delivers deionized water solvent across liquid irrigation rates L = 10 to 60 L/(min·m^2)."},
                {"name": "U-Tube Water Manometer Array", "purpose": "Monitors gas-side pressure drop across the 1.5 m packed bed to verify operation below flooding."}
            ],
            "procedure": [
                {"title": "Gas Blending & Baseline Calibration", "text": "Start air blower and open CO_2 cylinder; adjust rotameters to establish 5.00 mol% CO_2 in air at total gas flux G = 25.0 kg/(h·m^2); calibrate NDIR analyzer zero and span."},
                {"title": "Liquid Distributor Priming", "text": "Start water pump at moderate flow to pre-wet the Raschig ring packing completely for 10 minutes to eliminate dry spots."},
                {"title": "Initial Irrigation Rate Setting", "text": "Adjust water flow to establish liquid irrigation rate L = 10.0 L/(min·m^2); verify gas pressure drop across bed is stable."},
                {"title": "Steady-State Concentration Logging", "text": "Allow 15 minutes to establish mass transfer steady state; sample column inlet gas y_in and top exit gas y_out via NDIR analyzer."},
                {"title": "Liquid Rate Progression Protocol", "text": "Step liquid irrigation rate through 20.0, 30.0, 40.0, 50.0, and 60.0 L/(min·m^2), logging inlet and exit CO_2 concentrations at each plateau."},
                {"title": "Mass Transfer & HTU Regression Analysis", "text": "Compute log mean concentration driving force, calculate K_G a for each run, plot K_G a versus L^0.7, and evaluate the scaling slope S."}
            ],
            "topics": [
                {"question": "What is the difference between physical absorption and chemical absorption?", "answer": "Physical absorption (e.g., CO_2 in water) relies purely on physical solubility governed by Henry's law with low solvent capacity; chemical absorption (e.g., CO_2 in aqueous monoethanolamine MEA) involves rapid chemical reaction that converts solute into non-volatile ionic species, dramatically accelerating mass transfer and capacity."},
                {"question": "How are the Height of a Transfer Unit (HTU) and Number of Transfer Units (NTU) defined?", "answer": "Total packed height is Z = HTU × NTU; NTU represents the separation difficulty (dimensionless change in concentration divided by average driving force), while HTU characterizes mass transfer efficiency (smaller HTU means a more efficient packing requiring less height)."},
                {"question": "Why does liquid irrigation rate L have a strong effect on effective interfacial area 'a'?", "answer": "At low liquid rates, liquid trickles in narrow rivulets, leaving large portions of packing dry; increasing L wets more of the packing surface, converting dry area into thin liquid films and increasing effective contact area 'a' towards total geometric area a_p."},
                {"question": "What is the loading point and flooding point in packed column hydrodynamics?", "answer": "The loading point is the gas velocity where ascending gas starts to hold up descending liquid, increasing liquid holdup and pressure drop slope; the flooding point occurs when upward drag halts liquid drainage entirely, causing liquid to fill the column and spit out the top."},
                {"question": "Why does liquid film resistance control mass transfer in CO_2–water absorption?", "answer": "Carbon dioxide has low solubility in water (large Henry's constant H ≈ 1400 bar at 20 °C); according to two-film theory 1/K_G a = 1/(k_G a) + H/(k_L a), the second term accounts for > 95% of total resistance, making liquid film transport rate-limiting."},
                {"question": "How does Henry's law constant H vary with solvent temperature?", "answer": "Gas dissolution is an exothermic process (ΔH_sol < 0); increasing solvent temperature decreases gas solubility, increasing Henry's constant H and degrading absorption driving force and capacity."}
            ],
            "precautions": [
                "Carbon dioxide is an asphyxiant; vent column exhaust gases safely through a dedicated laboratory exhaust duct.",
                "Ensure liquid distributor holes are clear to prevent localized liquid channeling and dry zones along the wall.",
                "Monitor column pressure drop continuously; if pressure drop spikes rapidly, decrease gas flow to prevent column flooding.",
                "Verify water temperature remains at 20.0 ± 0.5 °C, as CO_2 solubility is sensitive to temperature."
            ],
            "quiz": [
                {
                    "question": "For absorption of a sparingly soluble gas like CO_2 in water, the controlling mass transfer resistance lies in:",
                    "options": ["The gas film exclusively", "The liquid film", "The solid packing core", "Equally shared between gas and liquid films"],
                    "correct": 1,
                    "explanation": "Because CO_2 has low solubility in water (very high Henry's constant H), liquid film resistance H / (k_L a) overwhelmingly dominates the overall mass transfer resistance."
                },
                {
                    "question": "The total required packing height Z of an absorption column is calculated as:",
                    "options": ["Z = HTU / NTU", "Z = HTU × NTU", "Z = NTU / HTU", "Z = sqrt(HTU × NTU)"],
                    "correct": 1,
                    "explanation": "Packed height is the product of the Height of a Transfer Unit (HTU) and the Number of Transfer Units (NTU): Z = HTU × NTU."
                },
                {
                    "question": "In a packed tower operating below the loading point, increasing liquid irrigation rate L causes the effective interfacial area 'a' to:",
                    "options": ["Decrease to zero", "Remain unchanged", "Increase as more packing surface is wetted", "Oscillate chaotically"],
                    "correct": 2,
                    "explanation": "Higher liquid flow rates spread liquid across previously dry packing surfaces, increasing the wetted fractional area and effective interfacial area 'a'."
                },
                {
                    "question": "The flooding point in a packed absorption tower represents:",
                    "options": ["The maximum gas velocity above which upward gas drag prevents downward liquid drainage", "The point of zero mass transfer", "The point where liquid boils", "The optimum operating point for minimum pressure drop"],
                    "correct": 0,
                    "explanation": "At flooding, upward gas drag supports the liquid column, causing liquid holdup to expand catastrophically, choking gas flow and spitting liquid from the top."
                }
            ],
            "samples": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
            "measureLabel": "Record absorption column mass transfer rate",
            "readings": ["kga_coeff", "liquid_pow", "outlet_co2", "htu_height"],
            "theory": """<h3>1. Fundamentals of Gas Absorption in Packed Towers</h3>
<p>Gas absorption involves the selective dissolution of one or more soluble gas components into a non-volatile liquid solvent. In chemical manufacturing, absorption columns recover valuable synthesis products (e.g., ammonia, methanol) and capture hazardous environmental contaminants (e.g., $\\text{CO}_2, \\text{SO}_2, \\text{NO}_x$).</p>

<h3>2. Two-Film Mass Transfer Theory</h3>
<p>According to Walter G. Whitman's two-film model (1923), mass transfer between gas and liquid phases is resisted by laminar fluid films adjacent to the interface. The steady molar transfer flux $N_A$ of solute gas is expressed as:</p>
\\[ N_A = k_G (P_{A,b} - P_{A,i}) = k_L (C_{A,i} - C_{A,b}) \\]
<p>where $k_G$ and $k_L$ are individual film coefficients, $P_{A,b}$ is bulk gas partial pressure, and $C_{A,b}$ is bulk liquid concentration. Thermodynamic phase equilibrium at the interface is governed by Henry's law: $P_{A,i} = H C_{A,i}$. Defining the overall volumetric mass transfer coefficient $K_G a$ based on gas-phase driving force:</p>
\\[ N_A a = K_G a (P_{A,b} - P_A^*) \\]
\\[ \\frac{1}{K_G a} = \\frac{1}{k_G a} + \\frac{H}{k_L a} \\]
<p>For sparingly soluble gases like $\\text{CO}_2$ in water, $H$ is large ($H \\approx 1400\\text{ bar}\\cdot\\text{L/mol}$), meaning liquid film resistance $H / (k_L a)$ accounts for $> 95\\%$ of total resistance, establishing liquid-film control: $K_G a \\approx k_L a / H$.</p>

<h3>3. Onda Correlation & Liquid Irrigation Scaling</h3>
<p>Kakusaburo Onda et al. (1968) correlated mass transfer coefficients and wetted area in packed beds: wetted area $a_w / a_t$ and liquid film coefficient $k_L$ scale with liquid mass flux $L$ as $L^{0.7}$. Combining these gives the volumetric mass transfer model:</p>
\\[ K_G a = S \\cdot L^{0.7} \\]
<p>where $S$ is the absorption scaling slope in $\\text{kmol/(m}^3\\cdot\\text{h}\\cdot\\text{bar)/(L/(min}\\cdot\\text{m}^2))^{0.7}$.</p>

<h3>4. Design Integration: HTU and NTU</h3>
<p>Integrating the differential mass balance along column height $Z$:</p>
\\[ Z = \\left[ \\frac{G}{K_G a P} \\right] \\int_{y_{out}}^{y_{in}} \\frac{dy}{y - y^*} = HOG \\cdot NOG \\]
<p>where $HOG = \\frac{G}{K_G a P}$ is the Height of an Overall Gas Transfer Unit, and $NOG$ is the Number of Transfer Units.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>This laboratory investigation determines the volumetric overall mass transfer coefficient $K_G a$ and Height of an Overall Transfer Unit ($HOG$) for the absorption of carbon dioxide into water in a counter-current packed column ($D = 100\\text{ mm}$, packed height $Z = 1.50\\text{ m}$, $10\\text{ mm}$ ceramic Raschig rings). Across liquid irrigation rates $L$ from $10.0$ to $60.0\\text{ L/(min}\\cdot\\text{m}^2)$ at constant gas flux ($G = 25.0\\text{ kg/(h}\\cdot\\text{m}^2)$, $5.0\\text{ mol}\\%$ inlet $\\text{CO}_2$), we evaluate $K_G a$, verify the $L^{0.7}$ Onda scaling model, and determine the absorption slope $S = 0.0820\\text{ kmol/(m}^3\\cdot\\text{h}\\cdot\\text{bar)/(L/(min}\\cdot\\text{m}^2))^{0.7}$.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Total $\\text{CO}_2$ absorbed is $\\dot{n}_A = \\frac{G A_{col}}{M_{air}} (y_{in} - y_{out}) = K_G a V_{bed} \\Delta P_{lm}$. The volumetric mass transfer coefficient follows the Onda power-law model:</p>
\\[ K_G a = S \\cdot L^{0.7} \\]
<p>where $S = 0.0820$ represents the experimental mass transfer coefficient slope. The height of a transfer unit is computed via $HOG = \\frac{G}{K_G a P_{atm}}$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>The column consists of a transparent acrylic tube ($D = 100.0\\text{ mm}$, cross-sectional area $A_{col} = 7.854 \\times 10^{-3}\\text{ m}^2$) packed to $Z = 1.50\\text{ m}$ with $10\\text{ mm}$ ceramic Raschig rings (specific area $a_p = 440\\text{ m}^2/\\text{m}^3$, voidage $\\varepsilon = 0.72$, packed volume $V_{bed} = 0.01178\\text{ m}^3$). An NDIR optical sensor logs inlet and outlet gas $\\text{CO}_2$ concentrations ($0\\text{--}10.0\\%$, accuracy $\\pm 0.01\\%$). Liquid flow is metered by a calibrated variable-area rotameter.</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Air and $\\text{CO}_2$ flows were blended to establish $y_{in} = 5.00\\text{ mol}\\%$ at total gas rate $G = 25.0\\text{ kg/(h}\\cdot\\text{m}^2)$. Water was turned on at $L = 10.0\\text{ L/(min}\\cdot\\text{m}^2)$ ($T = 20.0^\\circ\\text{C}$). The system was operated for 15 minutes to reach steady mass transfer equilibrium. Inlet and exit gas concentrations ($y_{in}, y_{out}$) and bed pressure drop were recorded. Liquid flow was incremented through $20.0, 30.0, 40.0, 50.0,$ and $60.0\\text{ L/(min}\\cdot\\text{m}^2)$.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Carbon dioxide is a colorless, odorless asphyxiant gas. The absorption column exhaust was vented directly into the laboratory exhaust system. Ambient $\\text{CO}_2$ room monitors were active with audible alarms set at $5,000\\text{ ppm}$. Safety glasses and lab coats were worn.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following measurements were recorded at constant gas feed $G = 25.0\\text{ kg/(h}\\cdot\\text{m}^2)$, $y_{in} = 5.00\\text{ mol}\\%$, and water temperature $T = 20.0^\\circ\\text{C}$:</p>
<table>
<thead>
<tr><th>Run</th><th>Liquid Rate $L$ (L/(min·m$^2$))</th><th>$L^{0.7}$</th><th>Exit Gas $y_{out}$ (mol%)</th><th>$\\text{CO}_2$ Removed (%)</th><th>$K_G a$ (kmol/(m$^3$·h·bar))</th><th>$HOG$ (m)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>10.0</td><td>5.012</td><td>4.32</td><td>13.6</td><td>0.411</td><td>2.08</td></tr>
<tr><td>2</td><td>20.0</td><td>8.140</td><td>3.95</td><td>21.0</td><td>0.667</td><td>1.28</td></tr>
<tr><td>3</td><td>30.0</td><td>10.825</td><td>3.68</td><td>26.4</td><td>0.888</td><td>0.96</td></tr>
<tr><td>4</td><td>40.0</td><td>13.238</td><td>3.46</td><td>30.8</td><td>1.086</td><td>0.79</td></tr>
<tr><td>5</td><td>50.0</td><td>15.460</td><td>3.28</td><td>34.4</td><td>1.268</td><td>0.67</td></tr>
<tr><td>6</td><td>60.0</td><td>17.534</td><td>3.12</td><td>37.6</td><td>1.438</td><td>0.59</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of volumetric mass transfer coefficient $K_G a$ versus $L^{0.7}$ yields:</p>
\\[ K_G a = 0.08200 \\cdot L^{0.7} + 0.00000 \\]
<p>with coefficient of determination $R^2 = 0.999999$. The experimental slope $S = 0.08200\\text{ kmol/(m}^3\\cdot\\text{h}\\cdot\\text{bar)/(L/(min}\\cdot\\text{m}^2))^{0.7}$ matches the design target ($0.0820$) with $0.00\\%$ deviation. As liquid irrigation rate expanded from $10$ to $60\\text{ L/(min}\\cdot\\text{m}^2)$, $K_G a$ grew from $0.411$ to $1.438\\text{ kmol/(m}^3\\cdot\\text{h}\\cdot\\text{bar)}$, while transfer unit height $HOG$ contracted from $2.08\\text{ m}$ to $0.59\\text{ m}$.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainty in NDIR gas analysis is $\\pm 0.01\\text{ mol}\\%$, rotameter liquid flow error is $\\pm 1.0\\%$, and packed volume uncertainty is $\\pm 0.5\\%$. Propagating errors into $K_G a$ yields an experimental uncertainty of $\\pm 1.4\\%$, reporting $S = 0.0820 \\pm 0.0011$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The $L^{0.7}$ dependence confirms Onda's wetted area formulation. At low irrigation rates, substantial portions of the ceramic Raschig rings remain un-wetted. Increasing liquid flow spreads liquid into continuous thin films over packing surfaces, multiplying interfacial contact area $a$ and thinning the liquid diffusion sublayer.</p>

<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>
<p>Packed absorption columns are central to natural gas sweetening (acid gas scrubbing) and post-combustion carbon capture. In commercial amine scrubbers, structured packings (Mellapak) are chosen over random rings to provide higher specific surface area ($> 250\\text{ m}^2/\\text{m}^3$) and lower pressure drop.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is water a poor solvent for industrial $\\text{CO}_2$ capture from flue gas?</strong><br>
<em>A1:</em> Water relies purely on physical solubility, which is low at atmospheric pressure and flue gas temperatures ($40\\text{--}50^\\circ\\text{C}$); huge liquid circulation rates would be required, whereas chemical solvents like $30\\text{ wt}\\%$ MEA react chemically with $\\text{CO}_2$, providing orders of magnitude higher capacity.</p>
<p><strong>Q2: What is the effect of gas maldistribution on absorption column efficiency?</strong><br>
<em>A2:</em> Maldistribution causes gas and liquid to flow through separate cross-sectional channels (bypassing), reducing local contact area and causing the apparent HTU to increase dramatically.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The packed column absorption experiment confirmed two-film mass transfer and Onda liquid-film scaling. The measured coefficient slope $S = 0.0820\\text{ kmol/(m}^3\\cdot\\text{h}\\cdot\\text{bar)/(L/(min}\\cdot\\text{m}^2))^{0.7}$ ($K_G a = 0.0820 \\cdot L^{0.7}$) validated liquid irrigation rate enhancement for chemical absorption processes.</p>"""
        },
        {
            "number": 19,
            "slug": "liquid-liquid-extraction-ternary-tie-lines",
            "title": "Liquid–Liquid Extraction Ternary Phase Equilibria & Distribution Coefficient K_D",
            "shortTitle": "Liquid–Liquid Extraction Equilibrium",
            "aim": "Determine the binodal solubility curve and conjugate liquid–liquid tie lines for the ternary system water – acetic acid – ethyl acetate, evaluate the distribution coefficient K_D and selectivity β, and verify Nernst partition equilibrium.",
            "inputLabel": "Raffinate Acetic Acid Conc x_A",
            "shortInput": "Raffinate x_A",
            "inputUnit": "wt%",
            "min": 5.0,
            "max": 30.0,
            "step": 5.0,
            "initial": 15.0,
            "inputDecimals": 1,
            "rawLabel": "Extract Acetic Acid Conc y_A",
            "rawUnit": "wt%",
            "rawDecimals": 2,
            "xAxis": "Raffinate phase concentration x_A (wt%)",
            "yAxis": "Extract phase concentration y_A (wt%)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 17.5,
            "emptyY": 15.5,
            "targetName": "Liquid-Liquid Distribution Coeff K_D",
            "target": "0.8850",
            "refValue": 0.8850,
            "resultUnit": "wt%/wt%",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "y_A = K_D · x_A = 0.8850 · x_A",
            "intro": "Liquid–liquid extraction (solvent extraction) is a key chemical engineering separation technology used when distillation is economically or thermodynamically impractical—such as separating close-boiling mixtures, recovering heat-sensitive bioproducts, breaking azeotropes, or purifying dilute specialty chemicals. In extraction, an immiscible or partially miscible liquid solvent (ethyl acetate) is mixed with a liquid feed mixture (water and acetic acid). Solute (acetic acid) distributes between the two liquid phases based on chemical potential and activity coefficient differences until thermodynamic phase equilibrium is achieved. The solute-rich solvent phase is termed the extract, and the remaining solute-depleted feed phase is termed the raffinate. Phase equilibria for ternary liquid systems are represented on equilateral or right-triangular coordinates featuring a binodal solubility curve that separates the single-phase homogeneous region from the two-phase immiscible envelope. Within the two-phase region, straight tie lines connect conjugate liquid phases in mutual thermodynamic equilibrium. According to Nernst's distribution law for dilute-to-moderate concentrations, the equilibrium distribution coefficient K_D = y_A / x_A (ratio of solute mass fraction in extract to raffinate) remains constant: y_A = K_D · x_A. In this laboratory investigation, ternary mixtures of water, acetic acid, and ethyl acetate are equilibrated in a jacketed separatory cell across raffinate concentrations from 5.0 to 30.0 wt% to construct tie lines, determine distribution coefficient K_D, and evaluate extraction selectivity β.",
            "modelExtra": "Evaluated using the ternary system water (carrier) – acetic acid (solute) – ethyl acetate (solvent) at 25.0 °C and 1.0 atm. Linear partition model relates extract mass fraction y_A directly to raffinate mass fraction x_A to extract K_D = 0.8850.",
            "apparatus": [
                {"name": "Thermostated Liquid-Liquid Equilibrium Extraction Cell", "purpose": "500 mL jacketed Pyrex mixing cell equipped with Teflon bottom drain valve and magnetic stirrer."},
                {"name": "Circulating Constant-Temperature Water Bath", "purpose": "Maintains equilibrium cell jacket temperature at exactly 25.00 ± 0.05 °C."},
                {"name": "Automatic Digital Potentiometric Titrator", "purpose": "Titrates acetic acid in extract and raffinate phases with standardized 0.100 M NaOH with 0.01 mL resolution."},
                {"name": "Precision Analytical Balance (0.1 mg resolution)", "purpose": "Gravimetrically prepares synthetic feed and solvent mixtures with 0.0001 g accuracy."},
                {"name": "Abbe High-Precision Optical Refractometer", "purpose": "Measures refractive index n_D of conjugate phases to cross-verify ternary compositions."},
                {"name": "Vortex Laboratory Mixer & Centrifuge", "purpose": "Accelerates phase disengagement and ensures complete liquid-liquid droplet separation."}
            ],
            "procedure": [
                {"title": "Equilibrium Cell Thermostating", "text": "Set circulating water bath to 25.00 °C; circulate water through the equilibrium cell jacket for 15 minutes before charging chemicals."},
                {"title": "Ternary Feed Preparation", "text": "Gravimetrically prepare a 200 g binary mixture of water and acetic acid containing 5.0 wt% solute; charge into the cell with 200 g of pure ethyl acetate."},
                {"title": "Intense Agitation & Equilibration", "text": "Agitate the two-phase mixture vigorously with a magnetic stirrer at 600 RPM for 20 minutes to generate high interfacial contact area."},
                {"title": "Phase Quiescence & Disengagement", "text": "Halt stirring and allow 30 minutes for complete gravitational phase separation into a clear bottom aqueous raffinate and clear top organic extract."},
                {"title": "Conjugate Phase Sampling & Titration", "text": "Draw 5.0 mL of bottom raffinate and 5.0 mL of top extract; titrate each phase against standardized 0.100 M NaOH to determine acetic acid concentrations x_A and y_A."},
                {"title": "Concentration Progression Protocol", "text": "Repeat procedure for initial aqueous feed concentrations yielding raffinate concentrations of 10.0, 15.0, 20.0, 25.0, and 30.0 wt% acetic acid."},
                {"title": "Distribution Coefficient Regression", "text": "Plot extract concentration y_A versus raffinate concentration x_A, and fit a linear regression through the origin to evaluate K_D."}
            ],
            "topics": [
                {"question": "What is the physical significance of the distribution coefficient K_D in liquid extraction?", "answer": "The distribution coefficient K_D = y_A / x_A measures the affinity of the solute for the extract solvent relative to the raffinate carrier; K_D > 1 indicates favorable extraction requiring less solvent, while K_D < 1 requires higher solvent-to-feed ratios."},
                {"question": "How is extraction selectivity (separation factor) β defined and why must β > 1?", "answer": "Selectivity is β = (y_A / x_A) / (y_B / x_B) = K_D,A / K_D,B, where B is the carrier solvent; if β = 1, solute and carrier distribute equally with zero separation, meaning an effective solvent must have β substantially greater than 1."},
                {"question": "What is the plait point on a ternary liquid-liquid binodal solubility curve?", "answer": "The plait point is the unique point on the binodal curve where the tie line length shrinks to zero, meaning the compositions of the conjugate extract and raffinate phases become identical and two-phase separation ceases."},
                {"question": "Why does acetic acid dimerize in non-polar organic solvents and how does it affect distribution?", "answer": "Acetic acid molecules form cyclic hydrogen-bonded dimers in non-polar solvents (e.g., benzene); dimerization causes K_D to vary with concentration (y_A ∝ x_A^2), whereas in polar solvents like ethyl acetate, hydrogen bonding with solvent maintains monomer distribution."},
                {"question": "What are the key criteria for selecting an industrial extraction solvent?", "answer": "High distribution coefficient K_D, high selectivity β, low miscibility with carrier, sufficient density difference (Δρ > 100 kg/m^3) for rapid settling, ease of solvent recovery (boiling point difference for distillation), low toxicity, and low cost."},
                {"question": "How does temperature affect the two-phase binodal envelope?", "answer": "Increasing temperature generally increases mutual solubility between carrier and solvent, shrinking the two-phase immiscible region and shifting the binodal curve until the Upper Critical Solution Temperature (UCST) is reached, where miscible single-phase behavior occurs."}
            ],
            "precautions": [
                "Ethyl acetate is volatile and flammable; perform all mixing and sampling inside an active fume hood.",
                "Ensure sufficient settling time (at least 30 minutes) to eliminate microscopic haze droplets before sampling.",
                "Maintain cell temperature strictly at 25.00 ± 0.05 °C, as liquid-liquid phase equilibria are sensitive to temperature.",
                "Pipette sample aliquots carefully without disturbing the liquid-liquid meniscus interface."
            ],
            "quiz": [
                {
                    "question": "The distribution coefficient K_D in liquid-liquid extraction is defined as:",
                    "options": ["x_A / y_A (raffinate / extract)", "y_A / x_A (extract / raffinate)", "y_A × x_A", "Mass of solvent / mass of feed"],
                    "correct": 1,
                    "explanation": "By standard definition, K_D is the ratio of solute mass or mole fraction in the extract phase to that in the raffinate phase: K_D = y_A / x_A."
                },
                {
                    "question": "A liquid-liquid extraction separation is thermodynamically feasible only if the selectivity β is:",
                    "options": ["Less than 1.0", "Equal to 1.0", "Greater than 1.0", "Equal to 0"],
                    "correct": 2,
                    "explanation": "Selectivity measures preferential dissolution of solute over carrier; separation requires β > 1.0 (if β = 1.0, no separation is possible)."
                },
                {
                    "question": "On a triangular ternary phase diagram, the plait point represents:",
                    "options": ["The maximum boiling point of the mixture", "The point where the extract and raffinate phase compositions become identical", "The pure solute vertex", "The zero-solubility limit"],
                    "correct": 1,
                    "explanation": "At the plait point on the binodal curve, tie line length vanishes and the two conjugate phases merge into a single critical phase."
                },
                {
                    "question": "In the water – acetic acid – ethyl acetate system, the organic extract phase floats on top of the aqueous raffinate because:",
                    "options": ["Ethyl acetate has a higher boiling point than water", "Ethyl acetate has a lower density (ρ ≈ 900 kg/m^3) than water (ρ ≈ 1000 kg/m^3)", "Water is more volatile than ethyl acetate", "Acetic acid repels ethyl acetate"],
                    "correct": 1,
                    "explanation": "Ethyl acetate has a density of ~900 kg/m^3, while the aqueous phase has a density near 1000 kg/m^3, causing the organic extract to float on top."
                }
            ],
            "samples": [5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
            "measureLabel": "Record extract and raffinate equilibrium concentrations",
            "readings": ["extract_ya", "raffinate_xa", "distrib_kd", "selectivity_beta"],
            "theory": """<h3>1. Thermodynamic Foundations of Liquid–Liquid Extraction</h3>
<p>Liquid–liquid extraction separates chemical components based on their relative solubilities in two immiscible or partially miscible liquid phases. Extraction is preferred when distillation is energy-intensive (e.g., dilute recovery of high-boiling acids from water) or hindered by close boiling points or azeotrope formation.</p>

<h3>2. Phase Equilibrium & The Nernst Distribution Law</h3>
<p>At thermodynamic equilibrium, the chemical potential $\\mu_i$ of each component $i$ is identical in both extract ($E$) and raffinate ($R$) phases:</p>
\\[ \\mu_{i,E} = \\mu_{i,R} \\implies \\gamma_{i,E} y_i = \\gamma_{i,R} x_i \\]
<p>where $\\gamma$ represents the liquid-phase activity coefficient. The distribution coefficient $K_D$ is defined as the ratio of solute mass fractions:</p>
\\[ K_D = \\frac{y_A}{x_A} = \\frac{\\gamma_{A,R}}{\\gamma_{A,E}} \\]
<p>In dilute-to-moderate concentration regimes where activity coefficients remain relatively stable, Nernst's distribution law dictates a linear partition equilibrium:</p>
\\[ y_A = K_D \\cdot x_A \\]
<p>where $K_D$ is the slope of the equilibrium distribution curve.</p>

<h3>3. Ternary Phase Diagrams & Selectivity</h3>
<p>On a ternary phase diagram, the binodal curve bounds the two-phase immiscible zone. Straight tie lines connect conjugate extract ($y_A, y_B, y_S$) and raffinate ($x_A, x_B, x_S$) compositions. The separation effectiveness is quantified by the dimensionless selectivity (separation factor) $\\beta$:</p>
\\[ \\beta = \\frac{y_A / x_A}{y_B / x_B} = \\frac{K_{D,A}}{K_{D,B}} \\]
<p>where $B$ is the carrier solvent (water). A viable extraction solvent requires $\\beta \\gg 1.0$.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>This laboratory investigation determines the liquid–liquid phase equilibrium for the ternary system water (carrier $B$) – acetic acid (solute $A$) – ethyl acetate (solvent $S$) at $25.00^\\circ\\text{C}$ and $1.0\\text{ atm}$. By equilibrating mixtures across raffinate concentrations $x_A$ from $5.0$ to $30.0\\text{ wt}\\%$ and analyzing conjugate phase compositions via potentiometric titration, we construct tie lines, determine distribution coefficient $K_D = 0.8850$, and evaluate extraction selectivity $\\beta$.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Liquid–liquid partition equilibrium obeys Nernst's distribution law:</p>
\\[ y_A = K_D \\cdot x_A \\]
<p>where $x_A$ is the solute weight fraction in the aqueous raffinate, $y_A$ is the solute weight fraction in the organic extract, and $K_D = 0.8850\\text{ wt}\\%/\\text{wt}\\%$ represents the equilibrium distribution coefficient. Selectivity is computed via $\\beta = (y_A / x_A) / (y_B / x_B)$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>The equilibrium cell is a $500\\text{ mL}$ jacketed Pyrex vessel with a water jacket connected to a circulating thermostatic bath ($25.00 \\pm 0.05^\\circ\\text{C}$). Reagent-grade glacial acetic acid ($> 99.7\\%$) and ethyl acetate ($> 99.5\\%$) were used. Acetic acid concentrations in both phases are determined by potentiometric titration using an automated titrator with standardized $0.100\\text{ M}$ $\\text{NaOH}$ (accuracy $\\pm 0.01\\text{ mL}$). Phase separation is accelerated in a laboratory centrifuge.</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Six mixtures of water, acetic acid, and ethyl acetate were prepared gravimetrically. Each mixture was charged into the cell at $25.00^\\circ\\text{C}$, stirred vigorously at $600\\text{ RPM}$ for 20 minutes, and allowed 30 minutes of quiescence to achieve complete phase disengagement. Samples of the lower aqueous raffinate and upper organic extract were withdrawn using separate glass pipettes and titrated with $0.100\\text{ M}$ $\\text{NaOH}$ to determine $x_A$ and $y_A$.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Glacial acetic acid is corrosive, and ethyl acetate is flammable. All operations were conducted in an active chemical fume hood. Nitrile gloves, safety goggles, and lab coats were worn. Waste solvent was collected in designated non-halogenated organic waste drums.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following equilibrium compositions were determined at $T = 25.00^\\circ\\text{C}$ and $P = 1.013\\text{ bar}$:</p>
<table>
<thead>
<tr><th>Run</th><th>Raffinate $x_A$ (wt%)</th><th>Extract $y_A$ (wt%)</th><th>Raffinate Water $x_B$ (wt%)</th><th>Extract Water $y_B$ (wt%)</th><th>Distribution $K_D$</th><th>Selectivity $\\beta$</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>5.0</td><td>4.43</td><td>89.5</td><td>4.8</td><td>0.886</td><td>16.5</td></tr>
<tr><td>2</td><td>10.0</td><td>8.85</td><td>83.2</td><td>6.2</td><td>0.885</td><td>11.9</td></tr>
<tr><td>3</td><td>15.0</td><td>13.28</td><td>76.5</td><td>8.1</td><td>0.885</td><td>8.4</td></tr>
<tr><td>4</td><td>20.0</td><td>17.70</td><td>69.1</td><td>10.5</td><td>0.885</td><td>5.8</td></tr>
<tr><td>5</td><td>25.0</td><td>22.13</td><td>61.2</td><td>13.8</td><td>0.885</td><td>3.9</td></tr>
<tr><td>6</td><td>30.0</td><td>26.55</td><td>52.4</td><td>18.2</td><td>0.885</td><td>2.5</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of extract phase concentration $y_A$ versus raffinate phase concentration $x_A$ yields:</p>
\\[ y_A = 0.88500 \\cdot x_A + 0.00000 \\]
<p>with coefficient of determination $R^2 = 0.999999$. The experimental distribution coefficient $K_D = 0.88500$ matches the calibration benchmark ($0.8850$) with $0.00\\%$ deviation. Selectivity $\\beta$ remained well above unity across all runs, ranging from $16.5$ in dilute solutions to $2.5$ at $30\\text{ wt}\\%$ solute.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainty in potentiometric titration volume is $\\pm 0.02\\text{ mL}$, corresponding to $\\delta x_A = \\pm 0.05\\text{ wt}\\%$. Temperature uncertainty is $\\pm 0.05^\\circ\\text{C}$. Propagating into $K_D$ yields an experimental uncertainty of $\\pm 0.85\\%$, reporting $K_D = 0.8850 \\pm 0.0075$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The distribution coefficient $K_D = 0.8850$ indicates that acetic acid has slightly higher affinity for water than ethyl acetate, reflecting strong hydrogen bonding with the aqueous matrix. However, because water solubility in the organic extract is low ($4.8\\%$ to $18.2\\%$), selectivity $\\beta$ is very high in dilute solutions ($\beta = 16.5$), making ethyl acetate an effective extraction solvent.</p>

<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>
<p>Liquid–liquid extraction is implemented in agitated columns (Kühni, Scheibel, rotating disc contactors) or mixer-settler cascades for recovering acetic acid from dilute cellulose acetate waste streams, recovering aromatics (BTX) from reformates (UOP Sulfolane process), and purifying antibiotics in pharmaceutical fermentation broths.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why does extraction selectivity $\beta$ decrease as solute concentration increases?</strong><br>
<em>A1:</em> Acetic acid acts as a mutual solubilizer (hydrotrope) between water and ethyl acetate; as its concentration rises, water solubility in the organic phase expands rapidly, increasing $y_B$ and lowering selectivity $\beta$.</p>
<p><strong>Q2: How is the solvent recovered after liquid-liquid extraction?</strong><br>
<em>A2:</em> The extract stream leaving the extraction column is sent to a solvent recovery distillation column where volatile ethyl acetate (b.p. $77.1^\\circ\\text{C}$) is distilled overhead and recycled, leaving concentrated acetic acid (b.p. $118.1^\\circ\\text{C}$) as the bottoms product.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The ternary liquid–liquid extraction experiment validated Nernst distribution equilibrium. The measured distribution coefficient $K_D = 0.8850$ ($y_A = 0.8850 \\cdot x_A$) and high dilute selectivity ($\beta = 16.5$) confirm the viability of ethyl acetate for industrial acetic acid recovery.</p>"""
        },
        {
            "number": 20,
            "slug": "batch-rotary-drum-vacuum-filtration-cake-resistance",
            "title": "Constant-Pressure Cake Filtration & Ruth Specific Cake Resistance Determination",
            "shortTitle": "Cake Filtration & Specific Resistance",
            "aim": "Perform constant-pressure vacuum filtration on an aqueous calcium carbonate suspension, record filtrate volume V as a function of time t, and determine the specific cake resistance α and filter medium resistance R_m using Ruth's parabolic filtration model.",
            "inputLabel": "Cumulative Filtrate Volume V",
            "shortInput": "Volume V",
            "inputUnit": "L",
            "min": 0.5,
            "max": 3.0,
            "step": 0.5,
            "initial": 1.5,
            "inputDecimals": 1,
            "rawLabel": "Filtration Time-to-Volume Ratio t/V",
            "rawUnit": "s/L",
            "rawDecimals": 2,
            "xAxis": "Cumulative filtrate volume V (L)",
            "yAxis": "Filtration ratio t/V (s/L)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 1.75,
            "emptyY": 36.5,
            "targetName": "Ruth Specific Cake Resistance Slope S",
            "target": "18.5000",
            "refValue": 18.5000,
            "resultUnit": "s/L^2",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "t/V = S · V + B = 18.5000 · V + 4.2000",
            "intro": "Solid–liquid filtration is an indispensable mechanical separation unit operation in chemical processing, mineral ore beneficiation, water clarification, and pharmaceutical crystallizer product recovery. In cake filtration, a slurry of insoluble solid particles is forced under pressure across a porous filter medium (woven cloth or membrane). While the medium initially captures particles, a porous permeable bed of accumulated solids—the filter cake—rapidly builds up on the cloth surface, becoming the dominant filtration medium. Flow of filtrate liquid through the growing porous cake obeys Darcy's law applied in series with the filter cloth. Burrows F. Ruth (1933) formulated the foundational parabolic filtration model for constant-pressure operation: dV/dt = [A^2 · ΔP] / [μ · (c · α · V + R_m · A)], where V is cumulative filtrate volume, A is filter area, ΔP is applied pressure drop, μ is filtrate dynamic viscosity, c is dry cake mass per unit filtrate volume, α is the average specific cake resistance (m/kg), and R_m is filter medium resistance (m^-1). Integrating this differential equation under constant differential pressure ΔP yields Ruth's celebrated linear relation: t / V = (K_p / 2) · V + B, where slope S = K_p / 2 = (μ · c · α) / (2 · A^2 · ΔP) and intercept B = (μ · R_m) / (A · ΔP). In this laboratory experiment, a constant vacuum (-60.0 kPa) is applied to filter an aqueous calcium carbonate slurry across a 150 mm circular filter leaf, logging t vs V across 0.5 to 3.0 L to evaluate slope S and determine specific cake resistance α.",
            "modelExtra": "Evaluated using a 5.0 wt% CaCO_3 slurry (dry cake mass c = 52.6 g/L filtrate) filtered across a circular leaf filter (diameter 150 mm, area A = 0.01767 m^2) under constant vacuum ΔP = 60.0 kPa. Linear regression models t/V versus V to extract S = 18.5000 s/L^2 and B = 4.2000 s/L.",
            "apparatus": [
                {"name": "Constant-Vacuum Leaf Filtration Assembly", "purpose": "150 mm diameter circular test leaf with stainless steel support grid and vacuum sealing gasket."},
                {"name": "Calibrated Woven Polypropylene Filter Cloth", "purpose": "Precision 20 μm pore size monofilament filter cloth providing reproducible clean medium resistance R_m."},
                {"name": "Regulated Vacuum Receiver Vessel & Pump", "purpose": "Maintains constant vacuum differential ΔP = 60.0 ± 0.2 kPa with surge damping chamber."},
                {"name": "Graduated Filtrate Collection Cylinder & Electronic Balance", "purpose": "Logs cumulative filtrate volume V and mass in real-time with 0.001 L resolution."},
                {"name": "Slurry Agitation Vessel with Variable-Speed Stirrer", "purpose": "Maintains 5.0 wt% CaCO_3 slurry in homogeneous suspension without settling before filtration."},
                {"name": "Digital Chronometer & Slurry Temperature Sensor", "purpose": "Records elapsed filtration time t to 0.01 s and slurry temperature at 20.0 ± 0.2 °C."}
            ],
            "procedure": [
                {"title": "Slurry Preparation & Homogenization", "text": "Prepare 10.0 L of 5.0 wt% calcium carbonate slurry in deionized water; agitate at 400 RPM for 20 minutes to achieve uniform particle dispersion."},
                {"title": "Vacuum System Stabilization", "text": "Start the vacuum pump and adjust the vacuum regulator until receiver differential pressure reads exactly ΔP = 60.0 kPa."},
                {"title": "Filter Leaf Pre-Wetting & Positioning", "text": "Pre-wet the polypropylene cloth with clean water; immerse the leaf vertically into the agitated slurry tank and simultaneously open the vacuum valve (t = 0)."},
                {"title": "Filtrate Volume & Time Logging", "text": "Record elapsed time t at cumulative filtrate volume intervals of 0.5, 1.0, 1.5, 2.0, 2.5, and 3.0 L on the graduated cylinder."},
                {"title": "Cake Recovery & Moisture Determination", "text": "Extract the leaf from the slurry, apply dry vacuum for 60 seconds to dewater the cake, scrape the cake into a tared dish, and dry in an oven at 105 °C to determine dry mass c."},
                {"title": "Ruth Parabolic Regression Analysis", "text": "Calculate t/V for each volume interval, plot t/V versus V, and extract slope S and intercept B to evaluate specific cake resistance α and medium resistance R_m."}
            ],
            "topics": [
                {"question": "What is the physical meaning of specific cake resistance α and what are its units?", "answer": "Specific cake resistance α (units m/kg) represents the hydraulic resistance to fluid flow per unit dry mass of deposited cake per unit filtration area; it depends on particle size, shape, packing voidage, and cake compressibility."},
                {"question": "How do compressible and incompressible filter cakes differ under increasing filtration pressure?", "answer": "For an incompressible cake (e.g., sand, rigid CaCO_3), cake voidage and resistance α remain constant regardless of pressure (α = α_0); for a compressible cake (e.g., sewage sludge, protein precipitates), increasing pressure crushes pores, escalating α according to α = α_0 (ΔP)^s, where s is compressibility."},
                {"question": "What is the role of filter aids (such as diatomaceous earth or perlite) in industrial filtration?", "answer": "Filter aids consist of rigid, highly porous, microscopic particles added to gelatinous or compressible slurries to build an open, incompressible cake matrix, preventing cloth blinding and drastically reducing specific cake resistance."},
                {"question": "Why does the Ruth plot (t/V versus V) have a non-zero intercept B?", "answer": "The intercept B = (μ R_m) / (A ΔP) represents the initial hydraulic resistance of the clean filter cloth and support piping before any cake layer has accumulated (at V = 0)."},
                {"question": "How does a continuous rotary drum vacuum filter (RDVF) utilize the cake filtration model?", "answer": "An RDVF submerges a rotating drum in a slurry trough, dividing the cycle into cake formation, cake washing, vacuum dewatering, and knife blade cake discharge; the Ruth equation governs the formation zone cycle time."},
                {"question": "What causes filter cloth blinding and how is it mitigated?", "answer": "Blinding occurs when fine particles penetrate into the pores of the filter cloth and lodge permanently, causing cloth resistance R_m to spike; it is mitigated by selecting proper cloth weave, pre-coating with filter aid, or periodic backwashing."}
            ],
            "precautions": [
                "Maintain continuous slurry agitation to prevent particle sedimentation from altering feed concentration during filtration.",
                "Ensure vacuum receiver pressure remains strictly constant at 60.0 kPa throughout the run.",
                "Seat the filter cloth tightly under the clamp ring to prevent edge bypass leakage.",
                "Record filtrate volume exactly at eye level to eliminate parallax errors."
            ],
            "quiz": [
                {
                    "question": "In Ruth's constant-pressure cake filtration equation, the plot of t / V versus V yields:",
                    "options": ["A horizontal line", "A straight line with positive slope and positive intercept", "A parabola passing through the origin", "An exponential decay curve"],
                    "correct": 1,
                    "explanation": "Integrating the constant-pressure filtration equation yields t / V = (K_p / 2) V + B, which is a straight line with slope S = K_p / 2 and intercept B."
                },
                {
                    "question": "In the Ruth equation t / V = S · V + B, the intercept B is directly proportional to:",
                    "options": ["The specific cake resistance α", "The filter medium resistance R_m", "The dry cake mass c", "The filtrate volume V"],
                    "correct": 1,
                    "explanation": "The intercept represents medium resistance at zero cake volume: B = (μ R_m) / (A ΔP)."
                },
                {
                    "question": "If the specific cake resistance α is independent of applied pressure ΔP (compressibility exponent s = 0), the cake is classified as:",
                    "options": ["Fully compressible", "Incompressible", "Viscoelastic", "Super-porous"],
                    "correct": 1,
                    "explanation": "Incompressible filter cakes (such as rigid crystalline minerals) maintain constant voidage and constant specific resistance regardless of pressure."
                },
                {
                    "question": "The units of specific cake resistance α in the SI system are:",
                    "options": ["kg/m", "m/kg", "m^2/s", "Pa·s"],
                    "correct": 1,
                    "explanation": "In Darcy's law formulation for cake filtration, specific cake resistance α has SI units of meters per kilogram (m/kg)."
                }
            ],
            "samples": [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
            "measureLabel": "Record filtration elapsed time and volume",
            "readings": ["t_over_v", "cum_volume", "time_sec", "specific_alpha"],
            "theory": """<h3>1. Mechanical Theory of Cake Filtration</h3>
<p>Cake filtration is a pressure-driven separation process where solid particles in a slurry are arrested by a permeable medium, forming an expanding porous bed (filter cake). Subsequent filtrate liquid must percolate through both the accumulated cake and the underlying cloth medium.</p>

<h3>2. Darcy's Law Applied to Cake and Medium Resistances</h3>
<p>Flow of filtrate through the porous cake obeys Darcy's filtration law in series with the filter medium resistance:</p>
\\[ \\frac{dV}{dt} = \\frac{A \\Delta P}{\\mu (R_{cake} + R_m)} \\]
<p>where $V$ is cumulative filtrate volume, $A$ is filter area, $\\Delta P$ is total pressure drop, and $\\mu$ is filtrate viscosity. The resistance of the cake layer $R_{cake}$ is proportional to the dry cake mass per unit area:</p>
\\[ R_{cake} = \\frac{\\alpha m_c}{A} = \\frac{\\alpha c V}{A} \\]
<p>where $\\alpha$ is the average specific cake resistance ($\\text{m/kg}$) and $c$ is dry cake mass deposited per unit filtrate volume ($\\text{kg/m}^3$).</p>

<h3>3. Derivation of Ruth's Constant-Pressure Filtration Equation</h3>
<p>Substituting $R_{cake}$ into Darcy's law yields:</p>
\\[ \\frac{dV}{dt} = \\frac{A \\Delta P}{\\mu \\left( \\frac{\\alpha c V}{A} + R_m \\right)} = \\frac{A^2 \\Delta P}{\\mu c \\alpha V + \\mu A R_m} \\]
<p>Separating variables and integrating from $t = 0, V = 0$ to time $t$ and volume $V$ under constant pressure $\\Delta P$:</p>
\\[ \\int_0^V (\\mu c \\alpha V + \\mu A R_m) dV = \\int_0^t A^2 \\Delta P dt \\]
\\[ \\frac{\\mu c \\alpha}{2} V^2 + \\mu A R_m V = A^2 \\Delta P \\cdot t \\]
<p>Dividing both sides by $A^2 \\Delta P \\cdot V$ yields Ruth's linear equation:</p>
\\[ \\frac{t}{V} = \\left[ \\frac{\\mu c \\alpha}{2 A^2 \\Delta P} \\right] V + \\left[ \\frac{\\mu R_m}{A \\Delta P} \\right] = S \\cdot V + B \\]
<p>where slope $S = \\frac{\\mu c \\alpha}{2 A^2 \\Delta P}$ and intercept $B = \\frac{\\mu R_m}{A \\Delta P}$. Specific cake resistance $\\alpha$ and medium resistance $R_m$ are directly determined from regression parameters $S$ and $B$:</p>
\\[ \\alpha = \\frac{2 S A^2 \\Delta P}{\\mu c}, \\quad R_m = \\frac{B A \\Delta P}{\\mu} \\]""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>This laboratory investigation determines the filtration characteristics of an aqueous calcium carbonate slurry ($5.0\\text{ wt}\\%$, dry cake concentration $c = 52.6\\text{ kg/m}^3$) under constant vacuum ($\Delta P = 60.0\\text{ kPa}$) using a circular leaf filter ($D = 150\\text{ mm}$, area $A = 0.01767\\text{ m}^2$). By recording cumulative filtrate volume $V$ versus time $t$ over $0.5$ to $3.0\\text{ L}$, we verify Ruth's parabolic filtration model ($t/V = S \\cdot V + B$), evaluate the cake resistance slope $S = 18.5000\\text{ s/L}^2$, and determine specific cake resistance $\\alpha$ and medium resistance $R_m$.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Constant-pressure cake filtration follows Ruth's linear equation:</p>
\\[ \\frac{t}{V} = S \\cdot V + B = \\left[ \\frac{\\mu c \\alpha}{2 A^2 \\Delta P} \\right] V + \\left[ \\frac{\\mu R_m}{A \\Delta P} \\right] \\]
<p>where $S = 18.5000\\text{ s/L}^2$ is the cake resistance slope and $B = 4.2000\\text{ s/L}$ is the cloth resistance intercept. Specific cake resistance is computed via $\\alpha = \\frac{2 S A^2 \\Delta P}{\\mu c}$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>The filter assembly consists of a $150.0\\text{ mm}$ diameter circular stainless steel leaf ($A = 0.01767\\text{ m}^2$) fitted with a monofilament polypropylene cloth ($20\\,\\mu\\text{m}$ pore rating). Vacuum is maintained at $\\Delta P = 60.0\\text{ kPa}$ by an oil-sealed rotary vane pump with a $50\\text{ L}$ receiver ballast vessel. Cumulative filtrate volume is logged using an electronic load cell ($\pm 0.001\\text{ kg}$) under a graduated receiver. The slurry was agitated at $400\\text{ RPM}$ to maintain uniform solids dispersion.</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>The $5.0\\text{ wt}\\%$ $\\text{CaCO}_3$ slurry was homogenized. Vacuum was set to $60.0\\text{ kPa}$. The pre-wetted leaf was plunged into the slurry tank, opening the vacuum line simultaneously ($t = 0$). Cumulative times $t$ were recorded at volume increments of $0.5, 1.0, 1.5, 2.0, 2.5,$ and $3.0\\text{ L}$. The resulting cake was recovered, weighed wet, and dried at $105^\\circ\\text{C}$ to determine $c = 52.6\\text{ g/L}$.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Vacuum receivers present implosion hazards; acrylic shielding enclosed the glass receiver vessel. Calcium carbonate dust during slurry preparation requires dust respirators. Safety goggles, lab coats, and nitrile gloves were worn.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following measurements were recorded at constant vacuum $\Delta P = 60.0\\text{ kPa}$ and slurry temperature $T = 20.0^\\circ\\text{C}$ (filtrate viscosity $\\mu = 1.002 \\times 10^{-3}\\text{ Pa}\\cdot\\text{s}$):</p>
<table>
<thead>
<tr><th>Run</th><th>Filtrate Volume $V$ (L)</th><th>Elapsed Time $t$ (s)</th><th>Ratio $t/V$ (s/L)</th><th>Incremental Time $\\Delta t$ (s)</th><th>Filtration Rate $dV/dt$ (mL/s)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>0.5</td><td>6.73</td><td>13.45</td><td>6.73</td><td>74.3</td></tr>
<tr><td>2</td><td>1.0</td><td>22.70</td><td>22.70</td><td>15.97</td><td>44.1</td></tr>
<tr><td>3</td><td>1.5</td><td>47.93</td><td>31.95</td><td>25.23</td><td>31.3</td></tr>
<tr><td>4</td><td>2.0</td><td>82.40</td><td>41.20</td><td>34.47</td><td>24.3</td></tr>
<tr><td>5</td><td>2.5</td><td>126.13</td><td>50.45</td><td>43.73</td><td>19.8</td></tr>
<tr><td>6</td><td>3.0</td><td>179.10</td><td>59.70</td><td>52.97</td><td>16.7</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of $t/V$ versus $V$ yields:</p>
\\[ \\frac{t}{V} = 18.50000 \\cdot V + 4.20000 \\]
<p>with coefficient of determination $R^2 = 0.999999$. Converting slope $S = 18.5000\\text{ s/L}^2$ into SI units: $S_{SI} = 18.5000 / (10^{-3}\\text{ m}^3)^2 = 1.8500 \\times 10^7\\text{ s/m}^6$. Evaluating specific cake resistance $\\alpha$:</p>
\\[ \\alpha = \\frac{2 S_{SI} A^2 \\Delta P}{\\mu c} = \\frac{2 \\cdot (1.8500 \\times 10^7) \\cdot (0.01767)^2 \\cdot 60,000}{1.002 \\times 10^{-3} \\cdot 52.6} = \\frac{6.932 \\times 10^8}{0.0527} = 1.315 \\times 10^{11}\\text{ m/kg} \\]
<p>Evaluating medium resistance $R_m$ from intercept $B = 4.2000\\text{ s/L} = 4200\\text{ s/m}^3$:</p>
\\[ R_m = \\frac{B A \\Delta P}{\\mu} = \\frac{4200 \\cdot 0.01767 \\cdot 60,000}{1.002 \\times 10^{-3}} = 4.444 \\times 10^9\\text{ m}^{-1} \\]
<p>The experimental slope matches the design benchmark ($18.5000\\text{ s/L}^2$) with $0.00\\%$ deviation.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Uncertainty in filtrate volume is $\\pm 0.005\\text{ L}$, timing error is $\\pm 0.1\\text{ s}$, and vacuum control is $\\pm 0.2\\text{ kPa}$. Propagating into $\\alpha$ yields an experimental uncertainty of $\\pm 1.8\\%$, reporting $\\alpha = (1.315 \\pm 0.024) \\times 10^{11}\\text{ m/kg}$ and $S = 18.5000 \\pm 0.12\\text{ s/L}^2$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The excellent linear fit of $t/V$ versus $V$ confirms that the calcium carbonate cake behaves as a rigid, incompressible porous medium under $60\\text{ kPa}$ vacuum. The medium resistance $R_m = 4.44 \\times 10^9\\text{ m}^{-1}$ contributed significantly during initial filtration, but cake resistance surpassed cloth resistance after just $0.23\\text{ L}$ of filtrate, demonstrating cake-controlled kinetics.</p>

<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>
<p>Specific cake resistance $\\alpha$ is the critical parameter for sizing industrial rotary drum vacuum filters, horizontal belt filters, and plate-and-frame filter presses. Knowledge of $\\alpha$ allows engineers to calculate optimal cycle times, wash liquor volumes, and vacuum pump displacement capacities.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why does the filtration rate $dV/dt$ decline progressively as filtration proceeds?</strong><br>
<em>A1:</em> As filtrate passes through the filter, solid particles deposit on the surface, increasing cake thickness $L_{cake}$ linearly with volume; this continuously expands hydraulic resistance, causing flow rate to decrease under constant pressure.</p>
<p><strong>Q2: How does adding a coagulant or flocculant affect specific cake resistance?</strong><br>
<em>A2:</em> Flocculants bind microscopic fine particles into large porous aggregates (flocs), increasing the effective pore diameter of the cake and reducing specific cake resistance $\\alpha$ by several orders of magnitude.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The experiment fully validated Ruth's constant-pressure parabolic filtration model. The calibrated resistance slope $S = 18.5000\\text{ s/L}^2$ established a specific cake resistance $\\alpha = 1.315 \\times 10^{11}\\text{ m/kg}$ and clean cloth resistance $R_m = 4.444 \\times 10^9\\text{ m}^{-1}$ for the calcium carbonate process slurry.</p>"""
        },
        {
            "number": 21,
            "slug": "solid-liquid-leaching-crosscurrent-stage-efficiency",
            "title": "Solid–Liquid Leaching Kinetics & Crosscurrent Extraction Stage Efficiency",
            "shortTitle": "Solid–Liquid Leaching Kinetics",
            "aim": "Study the crosscurrent batch leaching of soluble solute from a porous solid matrix using an organic solvent, measure residual solute concentration as a function of solvent-to-solid ratio S/F, and evaluate leaching solvation rate constant k and stage efficiency.",
            "inputLabel": "Solvent-to-Solid Ratio S/F",
            "shortInput": "Ratio S/F",
            "inputUnit": "kg/kg",
            "min": 1.0,
            "max": 6.0,
            "step": 1.0,
            "initial": 3.0,
            "inputDecimals": 1,
            "rawLabel": "Log Residual Solute Fraction ln(x_R)",
            "rawUnit": "ln(ratio)",
            "rawDecimals": 3,
            "xAxis": "Solvent-to-solid mass ratio S/F (kg/kg)",
            "yAxis": "Log residual solute fraction ln(x_R)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 3.5,
            "emptyY": -1.6,
            "targetName": "Leaching Solvation Rate Constant k",
            "target": "0.4200",
            "refValue": 0.4200,
            "resultUnit": "kg/kg",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "ln(x_R) = -k · (S/F) + c = -0.4200 · (S/F) - 0.1500",
            "intro": "Solid–liquid extraction (leaching) is a fundamental separation operation utilized in metallurgical hydrometallurgy (copper and gold cyanidation), food processing (oil extraction from soybeans, coffee and tea brewing, sucrose extraction from sugar beets), and pharmaceutical botanical drug extraction. In leaching, a liquid solvent contacts a porous solid matrix, dissolving soluble solute species and transferring them into the bulk liquid extract. Leaching mechanisms involve three sequential rate-limiting steps: (1) solvent penetration and dissolution of solute within internal pores, (2) molecular intra-particle diffusion of dissolved solute through tortuous fluid-filled pores to the solid surface, and (3) convective mass transfer across the external fluid boundary layer into the bulk solvent. When leaching is performed in crosscurrent stages with fresh solvent additions, the residual solute mass fraction remaining in the underflow solid matrix x_R decreases exponentially with cumulative solvent-to-solid mass ratio S/F: x_R = x_0 · exp[-k · (S/F)], where k is the characteristic solvation and washing rate constant. In this laboratory investigation, oil extraction from flaked oilseed meal using food-grade hexane solvent is studied in a benchtop jacketed stirred extractor across solvent-to-solid ratios from 1.0 to 6.0 kg/kg to measure residual solute fraction x_R and evaluate the solvation rate constant k.",
            "modelExtra": "Evaluated using crushed oilseed meal (initial oil content x_0 = 20.0 wt%) leached with n-hexane at 40.0 °C. Linearized logarithmic model relates ln(x_R) to S/F to extract solvation rate constant k = 0.4200.",
            "apparatus": [
                {"name": "Thermostatically Jacketed Agitated Leaching Vessel", "purpose": "1.0 L glass vessel with Teflon paddle impeller operating at 300 RPM and 40.0 ± 0.2 °C."},
                {"name": "Solvent Reflux Condenser & Nitrogen Purge", "purpose": "Recovers boiled solvent vapor and prevents air ingress into volatile organic extraction cell."},
                {"name": "Rotary Vacuum Filter Nutsche", "purpose": "Rapidly separates pregnant miscella extract from underflow solid meal cake with minimal hold-up."},
                {"name": "Rotary Evaporator (Rotovap) & Vacuum Pump", "purpose": "Evaporates hexane from extract samples to determine dissolved solute mass gravimetrically."},
                {"name": "Analytical Laboratory Balance (0.1 mg precision)", "purpose": "Weighs initial dry solids, solvent charges, and recovered extracted oil fractions."},
                {"name": "Soxhlet Extraction Reference Apparatus", "purpose": "Determines total exhaustively extractable initial oil content x_0 = 20.0 wt% for baseline normalization."}
            ],
            "procedure": [
                {"title": "Solid Meal Preparation & Moisture Check", "text": "Weigh 100.0 g of flaked oilseed meal (initial extractable oil x_0 = 20.0 wt%); verify moisture content < 8.0 wt%."},
                {"title": "Extractor Thermostating & Inerting", "text": "Set jacket temperature to 40.0 °C; purge vessel headspace with nitrogen to eliminate oxygen."},
                {"title": "Initial Solvent Charge & Leaching", "text": "Charge 100.0 g of pure n-hexane (S/F = 1.0 kg/kg) into the vessel; agitate at 300 RPM for 30 minutes to achieve dissolution equilibrium."},
                {"title": "Phase Separation & Miscella Sampling", "text": "Filter slurry through the vacuum Nutsche; record underflow cake mass and evaporate miscella to gravimetrically determine extracted oil mass."},
                {"title": "Solvent Ratio Stepping Protocol", "text": "Repeat leaching with fresh meal batches using cumulative solvent ratios of S/F = 2.0, 3.0, 4.0, 5.0, and 6.0 kg/kg, logging residual solute fraction x_R."},
                {"title": "Solvation Rate Constant Regression", "text": "Compute ln(x_R) for each run, plot ln(x_R) versus S/F, and fit a linear regression to extract rate constant k."}
            ],
            "topics": [
                {"question": "What is the difference between leaching and liquid–liquid extraction?", "answer": "In leaching, the solute is dissolved or dispersed within an insoluble solid porous matrix, requiring intra-particle solid diffusion; in liquid-liquid extraction, all components are initially in the liquid phase."},
                {"question": "Why is particle size reduction (milling or flaking) critical prior to leaching?", "answer": "Milling increases specific surface area and ruptures cellular walls, dramatically shortening the intra-particle diffusion path length and accelerating extraction rates."},
                {"question": "What is the underflow and overflow in industrial leaching circuits?", "answer": "Overflow (miscella) is the clear pregnant solvent containing dissolved solute; underflow is the wet solid slurry containing insoluble inert solids and entrained solvent liquor."},
                {"question": "How does counter-current leaching compare to crosscurrent leaching in solvent consumption?", "answer": "Counter-current leaching uses solvent in series against solids moving in reverse, achieving high solute recovery with minimal fresh solvent; crosscurrent uses fresh solvent in each stage, consuming much larger solvent volumes."},
                {"question": "What is residual solute retention in leached solid cakes?", "answer": "Capillary forces retain a fraction of solute-laden solution in the porous spaces of the cake (solution holdup); thorough cake washing is required to displace this entrained solute."},
                {"question": "Why is hexane universally used for commercial vegetable oil leaching?", "answer": "Hexane has high selectivity for triglycerides, low boiling point (69 °C) for easy distillation recovery, low latent heat of vaporization, and does not dissolve water-soluble gums."}
            ],
            "precautions": [
                "Hexane is highly volatile and flammable; operate all equipment under nitrogen purge in an explosion-proof hood.",
                "Ensure reflux condensers are chilled to < 5.0 °C to prevent solvent vapor release.",
                "Do not overheat the dry meal; thermal degradation degrades oil quality.",
                "Allow complete solvent evaporation before final gravimetric weighing of extracted oil."
            ],
            "quiz": [
                {
                    "question": "Leaching is defined as the separation of a soluble solute from:",
                    "options": ["A gas stream", "An insoluble solid matrix using a liquid solvent", "An immiscible liquid phase", "A molten metal slag"],
                    "correct": 1,
                    "explanation": "Leaching (solid-liquid extraction) selectively dissolves soluble components from an insoluble solid matrix into a liquid solvent."
                },
                {
                    "question": "The rate of leaching of biological materials is predominantly governed by:",
                    "options": ["Intra-particle diffusion through pore fluid", "Surface chemical reaction kinetics", "Electromagnetic radiation", "Sonic cavitation"],
                    "correct": 0,
                    "explanation": "In porous solid leaching, molecular diffusion through internal pores is usually the slowest, rate-limiting step."
                },
                {
                    "question": "In a crosscurrent leaching system, as the solvent-to-solid ratio S/F increases, the residual solute fraction in the solid:",
                    "options": ["Increases linearly", "Decreases exponentially", "Remains constant", "Drops instantly to zero"],
                    "correct": 1,
                    "explanation": "Successive dilution and washing steps remove solute exponentially with cumulative solvent ratio: x_R = x_0 exp[-k (S/F)]."
                },
                {
                    "question": "In oilseed extraction, the mixture of dissolved oil and solvent is termed:",
                    "options": ["Raffinate", "Miscella", "Leachate", "Slag"],
                    "correct": 1,
                    "explanation": "In vegetable oil processing, the pregnant liquid solution of vegetable oil dissolved in hexane is universally called miscella."
                }
            ],
            "samples": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "measureLabel": "Record leaching residual solute fraction",
            "readings": ["ln_xr", "solvent_ratio", "residual_xr", "extraction_yield"],
            "theory": """<h3>1. Transport Mechanics of Solid–Liquid Leaching</h3>
<p>Solid–liquid leaching extracts soluble target components from an insoluble solid matrix. Key industrial examples include vegetable oil extraction from crushed seeds, caffeine extraction from coffee beans, and leaching gold from ore slurries using cyanide solutions.</p>

<h3>2. Rate-Limiting Transport Steps</h3>
<p>The overall extraction process comprises three steps in series:</p>
<ol>
<li><strong>Internal Dissolution:</strong> Solvent penetrates capillary pores, dissolving soluble solid species.</li>
<li><strong>Intra-Particle Diffusion:</strong> Solute diffuses through the tortuous pore network to the external particle boundary:
\\[ J_A = -D_{eff} \\frac{dC_A}{dr} \\]
where $D_{eff} = \\frac{\\varepsilon_{pore}}{\\tau} D_{AB}$ is the effective pore diffusivity.</li>
<li><strong>External Boundary Layer Mass Transfer:</strong> Solute transfers across the external hydrodynamic film into bulk solvent:
\\[ N_A = k_c (C_{A,surf} - C_{A,bulk}) \\]
</li>
</ol>

<h3>3. Crosscurrent Leaching Model & Solvation Decay</h3>
<p>In crosscurrent leaching with fresh solvent additions, the mass balance across stage $n$ with solvent ratio $(S/F)$ dictates exponential solute depletion:</p>
\\[ x_R = x_0 \\exp\\left[-k \\left(\\frac{S}{F}\\right)\\right] \\]
<p>Taking natural logarithms yields the linear model:</p>
\\[ \\ln(x_R) = -k \\left(\\frac{S}{F}\\right) + c \\]
<p>where $k$ is the leaching solvation rate constant and $c = \\ln(x_0)$. Plotting $\\ln(x_R)$ versus $(S/F)$ yields a straight line with slope $-k$, from which the required solvent consumption for a target residual purity is evaluated.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>This laboratory investigation determines the extraction kinetics and stage efficiency for leaching vegetable oil from flaked oilseed meal ($100\\text{ g}$ batches, initial oil content $x_0 = 20.0\\text{ wt}\\%$) using n-hexane solvent at $40.0^\\circ\\text{C}$. Across solvent-to-solid mass ratios $S/F$ from $1.0$ to $6.0\\text{ kg/kg}$, we record residual oil fraction in the meal $x_R$, verify the exponential solvation model $\\ln(x_R) = -k (S/F) + c$, determine the rate constant $k = 0.4200\\text{ kg/kg}$, and evaluate oil recovery yield.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Residual solute fraction in the extracted meal cake follows exponential decay:</p>
\\[ \\ln(x_R) = -k \\left(\\frac{S}{F}\\right) + c \\]
<p>where $S/F$ is the solvent-to-solid mass ratio, $k = 0.4200$ is the characteristic leaching rate constant, and $c = -0.1500$ accounts for initial wetting hold-up. Extraction yield is computed via $Y = (1 - x_R / x_0) \\times 100\\%$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>The extractor is a $1.0\\text{ L}$ jacketed glass vessel equipped with a four-blade PTFE paddle stirrer ($300\\text{ RPM}$) and water jacket connected to a thermostatic bath ($40.00 \\pm 0.05^\\circ\\text{C}$). Slurry separation is performed using a laboratory vacuum Nutsche filter with Whatman No. 1 paper. Hexane solvent is evaporated from miscella using a Buchi R-300 rotary evaporator ($45^\\circ\\text{C}$, $300\\text{ mbar}$). Extracted oil is dried to constant weight on an analytical balance ($\pm 0.1\\text{ mg}$).</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Six $100.0\\text{ g}$ batches of flaked meal were prepared. Solvent charges of $100, 200, 300, 400, 500,$ and $600\\text{ g}$ of n-hexane were added to respective runs ($S/F = 1.0$ to $6.0$). Each batch was stirred at $40.0^\\circ\\text{C}$ for 30 minutes. The slurry was filtered under vacuum, underflow cakes were washed and desolventized, and miscella was evaporated to measure recovered oil mass and calculate residual solute fraction $x_R$.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>n-Hexane is neurotoxic and highly flammable (flash point $-22^\\circ\\text{C}$). The apparatus was operated inside an explosion-proof fume hood with continuous nitrogen inerting. Chemical splash goggles, thick nitrile gloves, and antistatic lab coats were worn.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following measurements were recorded at $T = 40.0^\\circ\\text{C}$ and $P = 1.013\\text{ bar}$ (initial oil content $x_0 = 20.0\\text{ wt}\\%$):</p>
<table>
<thead>
<tr><th>Run</th><th>Solvent Ratio $S/F$ (kg/kg)</th><th>Residual Oil $x_R$ (wt%)</th><th>Residual Fraction $x_R/x_0$</th><th>$\\ln(x_R)$</th><th>Oil Extracted (g)</th><th>Recovery Yield (%)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>1.0</td><td>11.36</td><td>0.568</td><td>-0.570</td><td>8.64</td><td>43.2</td></tr>
<tr><td>2</td><td>2.0</td><td>7.46</td><td>0.373</td><td>-0.990</td><td>12.54</td><td>62.7</td></tr>
<tr><td>3</td><td>3.0</td><td>4.90</td><td>0.245</td><td>-1.410</td><td>15.10</td><td>75.5</td></tr>
<tr><td>4</td><td>4.0</td><td>3.22</td><td>0.161</td><td>-1.830</td><td>16.78</td><td>83.9</td></tr>
<tr><td>5</td><td>5.0</td><td>2.11</td><td>0.106</td><td>-2.250</td><td>17.89</td><td>89.4</td></tr>
<tr><td>6</td><td>6.0</td><td>1.39</td><td>0.069</td><td>-2.670</td><td>18.61</td><td>93.1</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of $\\ln(x_R)$ versus solvent-to-solid ratio $S/F$ yields:</p>
\\[ \\ln(x_R) = -0.42000 \\cdot \\left(\\frac{S}{F}\\right) - 0.15000 \\]
<p>with coefficient of determination $R^2 = 0.999999$. The experimental slope $k = 0.42000$ matches the target calibration benchmark ($0.4200$) with $0.00\\%$ deviation. Oil recovery yield expanded from $43.2\\%$ at $S/F = 1.0$ to $93.1\\%$ at $S/F = 6.0$.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Gravimetric balance uncertainty is $\\pm 0.1\\text{ mg}$, and solvent volume error is $\\pm 0.2\\text{ mL}$. Propagating into rate constant $k$ yields an experimental uncertainty of $\\pm 1.2\\%$, reporting $k = 0.4200 \\pm 0.0050$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The exponential decline in residual oil confirms washing-controlled diffusion kinetics. In early stages ($S/F = 1$ to $2$), free surface oil is rapidly dissolved into hexane. In later stages ($S/F > 4$), intra-particle pore diffusion from deep cellular matrices controls extraction, requiring large solvent ratios to extract residual oil.</p>

<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>
<p>Continuous counter-current extractors (Crown iron works, De Smet basket extractors) are specified in industrial oilseed processing plants, achieving $> 99\\%$ oil recovery with solvent ratios $S/F \\approx 1.2$ by staging solvent washes counter-currently, avoiding the high solvent consumption of batch crosscurrent extraction.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is flaking preferred over fine grinding for oilseed extraction?</strong><br>
<em>A1:</em> Flaking crushes cell walls while producing coherent flakes ($0.25\\text{ mm}$ thick) that form a highly permeable bed in the extractor; fine grinding produces fines that blind filter screens and block solvent percolation.</p>
<p><strong>Q2: How is solvent recovered from the extracted meal cake in industrial plants?</strong><br>
<em>A2:</em> The wet meal is passed through a Desolventizer-Toaster (DT) where direct and indirect steam strips residual hexane down to $< 500\\text{ ppm}$, simultaneously toasting the meal to deactivate anti-nutritional enzymes for animal feed.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The solid–liquid leaching experiment verified exponential extraction kinetics. The measured solvation rate constant $k = 0.4200\\text{ kg/kg}$ establishes the fundamental mass transfer parameter governing solvent consumption and recovery yields in process extraction circuits.</p>"""
        },
        {
            "number": 22,
            "slug": "adsorption-isotherm-activated-carbon-langmuir-freundlich",
            "title": "Aqueous Adsorption Isotherms on Granular Activated Carbon & Langmuir Monolayer Modeling",
            "shortTitle": "Activated Carbon Adsorption Isotherm",
            "aim": "Determine equilibrium adsorption isotherms of aqueous organic acid onto granular activated carbon (GAC), fit the Langmuir and Freundlich models to experimental data, and evaluate monolayer capacity q_max and affinity constant K_L.",
            "inputLabel": "Equilibrium Concentration C_e",
            "shortInput": "Equil Conc C_e",
            "inputUnit": "mmol/L",
            "min": 2.0,
            "max": 12.0,
            "step": 2.0,
            "initial": 6.0,
            "inputDecimals": 1,
            "rawLabel": "Langmuir Ratio C_e / q_e",
            "rawUnit": "g/L",
            "rawDecimals": 3,
            "xAxis": "Equilibrium liquid concentration C_e (mmol/L)",
            "yAxis": "Langmuir linearized ratio C_e / q_e (g/L)",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 7.0,
            "emptyY": 3.4,
            "targetName": "Langmuir Reciprocal Capacity Slope S",
            "target": "0.4500",
            "refValue": 0.4500,
            "resultUnit": "g/mmol",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "C_e / q_e = S · C_e + B = 0.4500 · C_e + 0.2200",
            "intro": "Fixed-bed adsorption onto porous solid adsorbents is a vital chemical engineering unit operation for tertiary wastewater treatment, solvent vapor recovery, trace pharmaceutical removal, and gas dehydration. Granular activated carbon (GAC) is the premier industrial adsorbent due to its immense internal specific surface area (typically 800 to 1200 m^2/g) provided by a hierarchical network of micropores (< 2 nm), mesopores (2 to 50 nm), and macropores (> 50 nm). When an aqueous solution of an organic solute contacts activated carbon particles, solute molecules diffuse into the pores and adhere to the carbon surface via physical adsorption (van der Waals dispersion forces). At constant temperature, the equilibrium relationship between the amount of solute adsorbed per unit mass of adsorbent q_e (mmol/g) and the residual equilibrium solute concentration in solution C_e (mmol/L) defines the adsorption isotherm. Irving Langmuir (1918) derived the foundational theoretical isotherm model based on three postulates: (1) adsorption is limited to a monolayer of solute molecules, (2) all surface adsorption sites are energetically identical and independent, and (3) no lateral interactions occur between adjacent adsorbed molecules: q_e = (q_max · K_L · C_e) / (1 + K_L · C_e), where q_max is the maximum monolayer saturation capacity (mmol/g) and K_L is the Langmuir affinity constant (L/mmol). Linearizing the Langmuir model yields: C_e / q_e = (1 / q_max) · C_e + 1 / (K_L · q_max) = S · C_e + B. In this laboratory investigation, batch equilibrium adsorption of aqueous acetic acid on GAC is measured across equilibrium concentrations from 2.0 to 12.0 mmol/L to determine slope S = 1 / q_max = 0.4500 g/mmol (q_max = 2.222 mmol/g) and evaluate adsorption thermodynamics.",
            "modelExtra": "Evaluated using bituminous coal-based GAC (12×40 mesh, specific area 950 m^2/g) adsorbing acetic acid at 25.0 °C. Linear regression models C_e / q_e versus C_e to extract slope S = 0.4500 g/mmol and intercept B = 0.2200 g/L (K_L = 2.045 L/mmol).",
            "apparatus": [
                {"name": "Thermostatically Controlled Orbital Shaker Incubator", "purpose": "Agitates batch equilibrium flasks at 150 RPM and constant temperature 25.0 ± 0.1 °C for 24 hours."},
                {"name": "Calibrated Granular Activated Carbon (GAC)", "purpose": "Bituminous coal GAC (12×40 mesh, surface area 950 m^2/g) dried at 110 °C before weighing."},
                {"name": "Automatic Digital Potentiometric Titrator", "purpose": "Titrates equilibrium solution aliquots against standardized 0.050 M NaOH to 0.005 mL precision."},
                {"name": "Precision Analytical Balance (0.1 mg accuracy)", "purpose": "Accurately weighs dry GAC adsorbent aliquots (m = 1.0000 g ± 0.0002 g)."},
                {"name": "High-Recovery 0.45 μm PTFE Syringe Filters", "purpose": "Rapidly filters carbon fines from equilibrium solution without adsorbing dissolved organic acid."},
                {"name": "Borosilicate Glass Erlenmeyer Flasks with PTFE Stoppers", "purpose": "250 mL batch reactors providing sealed, non-adsorptive containers for equilibrium testing."}
            ],
            "procedure": [
                {"title": "GAC Activation & Weighing", "text": "Dry bituminous GAC in an oven at 110 °C for 2 hours; cool in a desiccator, and weigh exactly 1.000 g into each of six 250 mL flasks."},
                {"title": "Initial Standard Solution Dosing", "text": "Prepare six acetic acid solutions of known initial concentrations C_0 (5 to 40 mmol/L); add exactly 100.0 mL of solution to each respective flask."},
                {"title": "Orbital Shaker Incubation", "text": "Seal flasks with PTFE stoppers, mount on the orbital shaker at 25.0 °C, and agitate at 150 RPM for 24 hours to achieve true adsorption equilibrium."},
                {"title": "Phase Separation & Filtration", "text": "Withdraw 15 mL aliquots from each flask and filter through 0.45 μm PTFE syringe filters to remove all suspended carbon particles."},
                {"title": "Equilibrium Concentration Titration", "text": "Titrate 10.0 mL of filtered solution against standardized 0.050 M NaOH to determine equilibrium concentration C_e."},
                {"title": "Langmuir Isotherm Regression Analysis", "text": "Calculate equilibrium loading q_e = (C_0 - C_e) V / m, compute C_e / q_e, plot C_e / q_e versus C_e, and fit a linear regression to evaluate q_max and K_L."}
            ],
            "topics": [
                {"question": "What are the three fundamental assumptions of the Langmuir adsorption isotherm?", "answer": "(1) Monolayer coverage (adsorption stops once all sites are occupied), (2) homogeneous surface (all adsorption sites have identical activation energy), and (3) no lateral interactions between adjacent adsorbed molecules."},
                {"question": "How does the empirical Freundlich isotherm differ conceptually from the Langmuir model?", "answer": "The Freundlich model (q_e = K_F C_e^(1/n)) assumes a heterogeneous surface with an exponential distribution of site adsorption energies, allowing multilayer formation without saturation plateau at high concentrations."},
                {"question": "What is the dimensionless separation factor (equilibrium parameter) R_L in Langmuir modeling?", "answer": "R_L = 1 / (1 + K_L C_0); adsorption is irreversible if R_L = 0, favorable if 0 < R_L < 1, linear if R_L = 1, and unfavorable if R_L > 1."},
                {"question": "Why is 24 hours of shaking required to reach adsorption equilibrium on GAC?", "answer": "While external film transfer occurs in minutes, intra-particle Knudsen and surface diffusion through the tortuous micropore network (< 2 nm) is extremely slow, requiring hours for molecules to reach internal adsorption sites."},
                {"question": "What causes activated carbon pore clogging and how is spent carbon regenerated?", "answer": "Adsorption of large humic macromolecules blocks pore entrances (pore blinding); spent GAC is regenerated thermally in rotary kilns at 850 °C with steam to pyrolyze and oxidize adsorbed organics, restoring surface area."},
                {"question": "How does solution pH affect organic acid adsorption on activated carbon?", "answer": "At pH below the pKa of acetic acid (4.76), the acid is predominantly in its neutral molecular form (CH3COOH), which adsorbs strongly via hydrophobic interactions; at pH > pKa, the dissociated acetate ion (CH3COO-) experiences electrostatic repulsion from negatively charged carbon surface groups, reducing capacity."}
            ],
            "precautions": [
                "Filter equilibrium aliquots immediately through 0.45 μm filters to prevent continued adsorption by suspended carbon fines.",
                "Ensure flasks are tightly sealed with PTFE stoppers to prevent evaporation of volatile organic acids over the 24-hour run.",
                "Maintain constant incubation temperature at 25.0 ± 0.1 °C, as adsorption is an exothermic equilibrium process.",
                "Pre-dry carbon to ensure accurate dry mass determinations."
            ],
            "quiz": [
                {
                    "question": "In the Langmuir adsorption isotherm, the plateau at high equilibrium concentrations represents:",
                    "options": ["Capillary condensation", "Complete monolayer coverage of all active surface sites", "Multilayer crystallization", "Desorption runaway"],
                    "correct": 1,
                    "explanation": "Langmuir's model assumes adsorption terminates once a complete single molecular monolayer occupies all surface active sites."
                },
                {
                    "question": "If the Langmuir separation factor R_L = 1 / (1 + K_L C_0) is between 0 and 1, the adsorption is classified as:",
                    "options": ["Unfavorable", "Linear", "Favorable", "Irreversible"],
                    "correct": 2,
                    "explanation": "Values of R_L between 0 and 1 indicate favorable adsorption isotherms where the adsorbent exhibits high affinity for the solute."
                },
                {
                    "question": "In the linearized Langmuir equation C_e / q_e = (1 / q_max) C_e + 1 / (K_L q_max), the maximum monolayer capacity q_max is obtained from:",
                    "options": ["The y-intercept directly", "The reciprocal of the slope (1 / S)", "The slope times the intercept", "The square of the slope"],
                    "correct": 1,
                    "explanation": "The slope of the plot is S = 1 / q_max; therefore, the monolayer saturation capacity is calculated as q_max = 1 / S."
                },
                {
                    "question": "Adsorption of organic molecules from liquid solutions onto activated carbon is generally:",
                    "options": ["Endothermic (capacity increases with temperature)", "Exothermic (capacity decreases with temperature)", "Athermal (independent of temperature)", "Nuclear"],
                    "correct": 1,
                    "explanation": "Physical adsorption is driven by attractive van der Waals forces, making it inherently exothermic; increasing temperature shifts equilibrium toward desorption."
                }
            ],
            "samples": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
            "measureLabel": "Record equilibrium adsorption capacity",
            "readings": ["ce_over_qe", "equil_ce", "loading_qe", "langmuir_rl"],
            "theory": """<h3>1. Surface Chemistry & Adsorption Phenomena</h3>
<p>Adsorption is a phase-interface phenomenon where atoms, ions, or molecules of a fluid (adsorbate) adhere to the surface of an insoluble solid (adsorbent). In environmental and chemical process engineering, activated carbon adsorption removes toxic pollutants, volatile organic compounds (VOCs), dyes, and heavy metals from industrial effluents.</p>

<h3>2. The Langmuir Adsorption Isotherm Model</h3>
<p>Irving Langmuir (1918) derived the classic isotherm equation by equating the rate of adsorption onto vacant surface sites to the rate of desorption from occupied sites:</p>
\\[ r_{ads} = k_a C_e (1 - \\theta), \\quad r_{des} = k_d \\theta \\]
<p>where $\\theta = q_e / q_{max}$ is fractional surface coverage, $C_e$ is equilibrium fluid concentration, and $k_a, k_d$ are kinetic rate constants. At dynamic equilibrium ($r_{ads} = r_{des}$):</p>
\\[ k_a C_e (1 - \\theta) = k_d \\theta \\implies \\theta = \\frac{K_L C_e}{1 + K_L C_e} \\]
<p>where $K_L = k_a / k_d$ is the Langmuir adsorption equilibrium affinity constant. Expressing in terms of equilibrium solid loading $q_e$ ($\\text{mmol/g}$):</p>
\\[ q_e = \\frac{q_{max} K_L C_e}{1 + K_L C_e} \\]

<h3>3. Linearization of the Langmuir Equation</h3>
<p>Dividing $C_e$ by $q_e$ yields the primary linear form:</p>
\\[ \\frac{C_e}{q_e} = \\frac{1 + K_L C_e}{q_{max} K_L} = \\left( \\frac{1}{q_{max}} \\right) C_e + \\frac{1}{K_L q_{max}} = S \\cdot C_e + B \\]
<p>where slope $S = 1 / q_{max}$ and intercept $B = 1 / (K_L q_{max})$. Plotting $C_e / q_e$ versus $C_e$ yields a straight line from which monolayer saturation capacity $q_{max}$ and affinity constant $K_L$ are directly determined:</p>
\\[ q_{max} = \\frac{1}{S}, \\quad K_L = \\frac{S}{B} \\]""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>This laboratory investigation determines the equilibrium adsorption isotherm of aqueous acetic acid on bituminous coal granular activated carbon (GAC, $12 \\times 40\\text{ mesh}$, surface area $950\\text{ m}^2/\\text{g}$) at $25.00^\\circ\\text{C}$. Across equilibrium concentrations $C_e$ from $2.0$ to $12.0\\text{ mmol/L}$, we record solid phase loading $q_e$, fit the linearized Langmuir model ($C_e / q_e = S \\cdot C_e + B$), evaluate calibration slope $S = 0.4500\\text{ g/mmol}$ and intercept $B = 0.2200\\text{ g/L}$, and determine maximum monolayer capacity $q_{max} = 2.2222\\text{ mmol/g}$ and affinity constant $K_L = 2.0455\\text{ L/mmol}$.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Solid-phase equilibrium loading is calculated from mass balance: $q_e = \\frac{(C_0 - C_e) V}{m_{GAC}}$, where $V = 0.100\\text{ L}$ and $m_{GAC} = 1.000\\text{ g}$. The Langmuir linearized model is:</p>
\\[ \\frac{C_e}{q_e} = S \\cdot C_e + B = 0.4500 \\cdot C_e + 0.2200 \\]
<p>where $S = 1 / q_{max} = 0.4500\\text{ g/mmol}$ and $B = 1 / (K_L q_{max}) = 0.2200\\text{ g/L}$. Monolayer saturation capacity is $q_{max} = 1/S = 2.2222\\text{ mmol/g}$.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>Batch tests were conducted in $250\\text{ mL}$ Erlenmeyer flasks agitated in a New Brunswick Innova 40 orbital shaker ($150\\text{ RPM}$, $25.00 \\pm 0.05^\\circ\\text{C}$) for $24\\text{ hours}$. Bituminous coal GAC ($m = 1.0000\\text{ g}$, dried at $110^\\circ\\text{C}$) was contacted with $100.0\\text{ mL}$ solutions. Aqueous samples were filtered through $0.45\\,\\mu\\text{m}$ PTFE syringe filters. Equilibrium concentrations were determined using an automated potentiometric titrator ($0.050\\text{ M}$ $\\text{NaOH}$, accuracy $\\pm 0.005\\text{ mL}$).</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>Six flasks were charged with $1.000\\text{ g}$ of GAC and $100.0\\text{ mL}$ of acetic acid solutions with initial concentrations $C_0$ ranging from $5.0$ to $40.0\\text{ mmol/L}$. Flasks were agitated for 24 hours to achieve thermodynamic equilibrium. Solution aliquots were filtered, and $10.0\\text{ mL}$ samples were titrated with standardized $0.050\\text{ M}$ $\\text{NaOH}$ to determine residual equilibrium concentration $C_e$.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Dilute acetic acid presents minor skin/eye irritation hazards. Activated carbon dust during dry weighing requires dust masks. Safety goggles, lab coats, and nitrile gloves were worn throughout testing.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following equilibrium data were obtained at $T = 25.00^\\circ\\text{C}$ ($V = 0.100\\text{ L}$, $m_{GAC} = 1.000\\text{ g}$):</p>
<table>
<thead>
<tr><th>Run</th><th>Equilibrium $C_e$ (mmol/L)</th><th>Initial $C_0$ (mmol/L)</th><th>Equilibrium $q_e$ (mmol/g)</th><th>Langmuir Ratio $C_e/q_e$ (g/L)</th><th>Separation Factor $R_L$</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>2.0</td><td>19.85</td><td>1.785</td><td>1.120</td><td>0.196</td></tr>
<tr><td>2</td><td>4.0</td><td>23.80</td><td>1.980</td><td>2.020</td><td>0.109</td></tr>
<tr><td>3</td><td>6.0</td><td>26.68</td><td>2.068</td><td>2.920</td><td>0.075</td></tr>
<tr><td>4</td><td>8.0</td><td>29.13</td><td>2.113</td><td>3.820</td><td>0.057</td></tr>
<tr><td>5</td><td>10.0</td><td>31.42</td><td>2.142</td><td>4.720</td><td>0.046</td></tr>
<tr><td>6</td><td>12.0</td><td>33.62</td><td>2.162</td><td>5.620</td><td>0.039</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of Langmuir ratio $C_e / q_e$ versus equilibrium concentration $C_e$ yields:</p>
\\[ \\frac{C_e}{q_e} = 0.45000 \\cdot C_e + 0.22000 \\]
<p>with coefficient of determination $R^2 = 0.999999$. The experimental slope $S = 0.45000\\text{ g/mmol}$ matches the calibration target ($0.4500$) with $0.00\\%$ deviation. Maximum monolayer capacity is:</p>
\\[ q_{max} = \\frac{1}{S} = \\frac{1}{0.45000} = 2.2222\\text{ mmol/g} = 133.45\\text{ mg/g} \\]
<p>The Langmuir affinity constant is evaluated as:</p>
\\[ K_L = \\frac{S}{B} = \\frac{0.45000}{0.22000} = 2.0455\\text{ L/mmol} \\]
<p>The separation factor $R_L$ ranged between $0.039$ and $0.196$, rigorously confirming favorable adsorption ($0 < R_L < 1$).</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Titration volume uncertainty is $\\pm 0.005\\text{ mL}$, and balance uncertainty is $\\pm 0.0002\\text{ g}$. Propagating into $q_{max}$ yields an experimental uncertainty of $\\pm 1.1\\%$, reporting $q_{max} = 2.222 \\pm 0.024\\text{ mmol/g}$ and $K_L = 2.046 \\pm 0.032\\text{ L/mmol}$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The outstanding linear correlation confirms Langmuir monolayer adsorption. At low concentrations ($C_e < 2\\text{ mmol/L}$), rapid uptake occurs as solute molecules occupy highly energetic micropore sites. As concentration approaches $12\\text{ mmol/L}$, surface loading asymptotes toward the saturation capacity $q_{max} = 2.222\\text{ mmol/g}$ as active sites become saturated.</p>

<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>
<p>Isotherm parameters $q_{max}$ and $K_L$ are directly utilized in the Bohart–Adams and Thomas breakthrough models to size industrial fixed-bed carbon contactors for drinking water purification, tertiary sewage polishing, and VOC adsorption from chemical reactor vents.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why does granular activated carbon (GAC) exhibit a much higher surface area than non-activated charcoal?</strong><br>
<em>A1:</em> High-temperature activation with steam or carbon dioxide selectively gasifies internal carbon atoms, excavating an extensive network of sub-nanometer micropores that multiplies internal surface area up to $1200\\text{ m}^2/\\text{g}$.</p>
<p><strong>Q2: What is the significance of the Freundlich parameter $1/n < 1$?</strong><br>
<em>A2:</em> The exponent $1/n$ reflects adsorption intensity; $1/n < 1$ indicates favorable adsorption where affinity remains strong even at low solute concentrations.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The batch adsorption experiment validated the Langmuir monolayer adsorption isotherm. The measured regression slope $S = 0.4500\\text{ g/mmol}$ and intercept $B = 0.2200\\text{ g/L}$ established a maximum monolayer saturation capacity $q_{max} = 2.2222\\text{ mmol/g}$ ($133.45\\text{ mg/g}$) and affinity constant $K_L = 2.0455\\text{ L/mmol}$ for the GAC-acetic acid system.</p>"""
        },
        {
            "number": 23,
            "slug": "crossflow-membrane-ultrafiltration-gel-polarization",
            "title": "Crossflow Membrane Ultrafiltration Permeate Flux & Concentration Polarization",
            "shortTitle": "Crossflow Ultrafiltration",
            "aim": "Operate a crossflow membrane ultrafiltration module separating aqueous bovine serum albumin (BSA) protein, measure permeate flux J as a function of transmembrane pressure (TMP), and evaluate membrane hydraulic permeability L_p and gel polarization resistance R_g.",
            "inputLabel": "Transmembrane Pressure TMP",
            "shortInput": "Pressure TMP",
            "inputUnit": "bar",
            "min": 0.5,
            "max": 3.0,
            "step": 0.5,
            "initial": 1.5,
            "inputDecimals": 1,
            "rawLabel": "Permeate Flux J",
            "rawUnit": "L/(m^2·h)",
            "rawDecimals": 2,
            "xAxis": "Transmembrane pressure TMP (bar)",
            "yAxis": "Permeate flux J (L/(m^2·h))",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 1.75,
            "emptyY": 74.0,
            "targetName": "Pure Water Permeability L_p",
            "target": "42.5000",
            "refValue": 42.5000,
            "resultUnit": "L/(m^2·h·bar)",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "J = L_p · TMP = 42.5000 · TMP",
            "intro": "Membrane separation processes—including microfiltration, ultrafiltration, nanofiltration, and reverse osmosis—are premier pressure-driven unit operations in biotechnology, water desalination, dairy processing, and wastewater reclamation. In crossflow ultrafiltration (UF), pressurized feed slurry recirculates tangentially across the membrane surface at high velocity, while pure solvent permeates perpendicularly through the porous polymeric or ceramic skin (pore size 1 to 100 nm, molecular weight cut-off MWCO 1,000 to 100,000 Da). Retained macromolecular solutes (e.g., proteins, polysaccharides, colloids) accumulate at the membrane boundary layer, forming a concentrated solute layer termed concentration polarization. At low transmembrane pressures (TMP = (P_feed + P_ret - 2 P_perm) / 2), permeate flux J obeys Darcy's law: J = TMP / [μ · R_m] = L_p · TMP, where R_m is clean membrane hydraulic resistance and L_p is pure water permeability. However, as TMP increases, the solute concentration at the membrane surface reaches a critical gel concentration C_g, forming a viscous gel layer that adds dynamic resistance R_g. Beyond this threshold, permeate flux enters the pressure-independent (limiting flux) regime governed by convective-diffusive back-transport: J_lim = k_bl · ln(C_g / C_b), where k_bl is the boundary layer mass transfer coefficient. In this laboratory investigation, an instrumented crossflow flat-sheet ultrafiltration cell with a 30 kDa polyethersulfone (PES) membrane is operated across TMPs from 0.5 to 3.0 bar to measure clean water permeability L_p = 42.5000 L/(m^2·h·bar) and observe the onset of gel polarization.",
            "modelExtra": "Evaluated using a 30 kDa MWCO polyethersulfone (PES) flat-sheet membrane (effective area A = 0.0140 m^2) filtering deionized water and 1.0 wt% BSA solution at crossflow velocity v = 1.5 m/s. Linear model relates clean permeate flux J directly to TMP.",
            "apparatus": [
                {"name": "Crossflow Flat-Sheet Membrane Test Cell", "purpose": "Stainless steel SEPA cell housing flat-sheet membrane (effective active area A = 0.0140 m^2)."},
                {"name": "High-Pressure Positive Displacement Diaphragm Pump", "purpose": "Delivers feed flow up to 5.0 L/min and pressures up to 10.0 bar with pulsation damper."},
                {"name": "Digital Transmembrane Pressure Transducers", "purpose": "Logs feed pressure P_in, retentate pressure P_out, and permeate pressure P_perm with 0.01 bar accuracy."},
                {"name": "30 kDa Polyethersulfone (PES) Ultrafiltration Membrane", "purpose": "Asymmetric UF membrane with 30,000 Da MWCO for quantitative BSA protein retention."},
                {"name": "Digital Analytical Permeate Balance & Data Logger", "purpose": "Weighs cumulative permeate discharge at 1 Hz with 0.01 g precision to compute real-time flux J."},
                {"name": "Thermostatically Controlled Feed Reservoir with Heat Exchanger", "purpose": "Maintains feed solution at constant temperature 25.0 ± 0.1 °C during recirculation."}
            ],
            "procedure": [
                {"title": "Membrane Compaction & Pre-Conditioning", "text": "Install a new 30 kDa PES membrane; compact with deionized water at 4.0 bar for 30 minutes until pure water flux stabilizes."},
                {"title": "Baseline Clean Water Flux Calibration", "text": "Set crossflow velocity to 1.5 m/s; record pure water permeate flux J at TMP = 0.5 bar at 25.0 °C."},
                {"title": "Pressure Stepping Protocol", "text": "Step TMP through 1.0, 1.5, 2.0, 2.5, and 3.0 bar, recording steady-state permeate flux J after 10 minutes at each plateau."},
                {"title": "Protein Solution Introduction", "text": "Drain water and charge 2.0 L of 1.0 wt% BSA solution; circulate at TMP = 1.0 bar to establish protein concentration polarization."},
                {"title": "Flux Decline & Limiting Flux Observation", "text": "Measure permeate flux vs TMP for the BSA feed; identify the transition from Darcy linear regime to pressure-independent limiting flux J_lim."},
                {"title": "Permeability Regression Analysis", "text": "Plot clean water permeate flux J versus TMP, fit a linear regression through the origin, and determine membrane permeability L_p."}
            ],
            "topics": [
                {"question": "What is the difference between dead-end filtration and crossflow filtration?", "answer": "In dead-end filtration, slurry flow is perpendicular to the membrane, causing all retained solids to accumulate in a rapidly thickening cake that blinds the filter; in crossflow filtration, fluid sweeps tangentially across the membrane at high velocity, continuously scouring away accumulated foulants and maintaining high steady flux."},
                {"question": "How does concentration polarization differ from membrane fouling?", "answer": "Concentration polarization is a reversible thermodynamic accumulation of rejected solute in the liquid boundary layer that dissipates immediately when flow or pressure stops; membrane fouling is an irreversible deposition (pore blocking, adsorption, gel formation) requiring chemical cleaning to restore permeability."},
                {"question": "What is Molecular Weight Cut-Off (MWCO) in membrane specification?", "answer": "MWCO is the molecular weight of a globular solute (in Daltons) that is 90% rejected by the membrane; a 30 kDa membrane rejects > 90% of molecules larger than 30,000 g/mol (such as BSA, MW ≈ 66.5 kDa)."},
                {"question": "Why does permeate flux become independent of transmembrane pressure at high TMP?", "answer": "At high TMP, convective solute transport toward the membrane balances back-diffusion, forcing surface solute concentration to reach its maximum packing limit (gel concentration C_g); further pressure increases merely compress this gel layer, adding hydraulic resistance that exactly cancels the increased pressure driving force."},
                {"question": "How does crossflow velocity affect the limiting permeate flux J_lim?", "answer": "Higher crossflow velocity enhances turbulence and thins the boundary layer, increasing the mass transfer coefficient k_bl; according to the film model J_lim = k_bl ln(C_g / C_b), limiting flux scales with shear rate (v^0.8 in turbulent flow)."},
                {"question": "How are fouled polymeric membranes restored in industrial bioprocessing?", "answer": "Membranes undergo Clean-in-Place (CIP) sequences consisting of forward flush, alkaline wash (0.1 M NaOH with sodium hypochlorite to hydrolyze proteins), acid wash (citric or phosphoric acid to dissolve inorganic scale), and enzymatic detergent cleaning."}
            ],
            "precautions": [
                "Compact new membranes at 4.0 bar prior to acquiring calibration data to eliminate permanent polymer deformation artifacts.",
                "Maintain feed temperature strictly at 25.0 ± 0.1 °C, as water viscosity drops by ~2.5% per °C, causing apparent flux drift.",
                "Ensure feed is pre-filtered through 5 μm cartridge filters to prevent particulate scoring of the membrane surface.",
                "Do not allow membranes to dry out; store in sodium metabisulfite preservative solution when not in service."
            ],
            "quiz": [
                {
                    "question": "In crossflow ultrafiltration, the transmembrane pressure (TMP) is defined as:",
                    "options": ["(P_feed + P_retentate) / 2 - P_permeate", "P_feed - P_retentate", "P_permeate - P_feed", "(P_feed · P_retentate) / P_permeate"],
                    "correct": 0,
                    "explanation": "TMP is the average fluid pressure across the membrane channel minus the downstream permeate pressure: TMP = (P_in + P_out)/2 - P_perm."
                },
                {
                    "question": "The primary advantage of crossflow filtration over dead-end filtration is:",
                    "options": ["Lower equipment cost", "Tangential fluid shear scours the membrane surface, preventing rapid cake buildup", "Zero energy consumption", "Complete retention of all dissolved salts"],
                    "correct": 1,
                    "explanation": "Tangential crossflow velocity creates high wall shear that sweeps away deposited solutes, maintaining sustainable steady-state permeate flux."
                },
                {
                    "question": "In the pressure-independent limiting flux regime of ultrafiltration, increasing TMP causes permeate flux to:",
                    "options": ["Increase linearly", "Drop to zero", "Remain essentially constant as gel layer resistance expands", "Double instantaneously"],
                    "correct": 2,
                    "explanation": "At limiting flux, increasing TMP simply thickens or compresses the boundary gel layer, adding resistance that exactly offsets the added pressure."
                },
                {
                    "question": "A membrane with a Molecular Weight Cut-Off (MWCO) of 30 kDa will reject approximately what percentage of a 66.5 kDa protein (BSA)?",
                    "options": ["10%", "50%", "> 95%", "0%"],
                    "correct": 2,
                    "explanation": "Because BSA (66.5 kDa) is more than double the MWCO of 30 kDa, it is nearly completely rejected (> 95% to 99%)."
                }
            ],
            "samples": [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
            "measureLabel": "Record membrane permeate flux",
            "readings": ["permeate_flux", "tmp_press", "mass_perm", "resistance_m"],
            "theory": """<h3>1. Principles of Crossflow Membrane Ultrafiltration</h3>
<p>Ultrafiltration (UF) is a pressure-driven membrane separation process utilizing semi-permeable asymmetric polymeric or ceramic membranes with pore diameters of $1$ to $100\\text{ nm}$. It effectively retains macromolecules, proteins, viruses, and colloidal silica while permitting solvent and small dissolved salts to pass freely.</p>

<h3>2. Darcy's Law & Clean Water Permeability</h3>
<p>In clean water filtration, fluid transport across the porous membrane matrix is governed by Darcy's law:</p>
\\[ J = \\frac{\\Delta P}{\\mu R_m} = L_p \\cdot \\text{TMP} \\]
<p>where $J$ is permeate flux ($\\text{L/(m}^2\\cdot\\text{h)}$), $\\text{TMP}$ is transmembrane pressure, $\\mu$ is permeate viscosity, $R_m$ is intrinsic membrane hydraulic resistance ($\\text{m}^{-1}$), and $L_p = 1 / (\\mu R_m)$ is the pure water permeability coefficient in $\\text{L/(m}^2\\cdot\\text{h}\\cdot\\text{bar)}$.</p>

<h3>3. Concentration Polarization & Film Theory</h3>
<p>During macromolecular filtration, rejected solute accumulates at the membrane surface. At steady state, convective solute transport toward the membrane is balanced by Fickian diffusion back into the bulk crossflow stream:</p>
\\[ J C - D \\frac{dC}{dy} = 0 \\]
<p>Integrating across boundary layer thickness $\\delta$ with boundary conditions $C(0) = C_w$ (wall concentration) and $C(\\delta) = C_b$ (bulk concentration):</p>
\\[ J = k_{bl} \\ln\\left( \\frac{C_w}{C_b} \\right) \\]
<p>where $k_{bl} = D / \\delta$ is the mass transfer coefficient. When wall concentration reaches saturation gel concentration $C_g$, a viscous gel layer forms ($R_g$), and flux plateaus at the limiting flux:</p>
\\[ J_{lim} = k_{bl} \\ln\\left( \\frac{C_g}{C_b} \\right) \\]
<p>In the pre-gel linear Darcy regime, plotting pure water flux $J$ versus $\\text{TMP}$ yields a straight line through the origin whose slope directly provides membrane permeability $L_p$:</p>
\\[ J = L_p \\cdot \\text{TMP} \\]""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>This laboratory investigation determines the clean water hydraulic permeability $L_p$ and investigates concentration polarization in a crossflow membrane ultrafiltration module ($A = 0.0140\\text{ m}^2$) fitted with a $30\\text{ kDa}$ polyethersulfone (PES) flat-sheet membrane. Operating across transmembrane pressures $\\text{TMP}$ from $0.5$ to $3.0\\text{ bar}$ at crossflow velocity $v = 1.5\\text{ m/s}$ and $25.0^\\circ\\text{C}$, we record permeate flux $J$, evaluate membrane permeability $L_p = 42.5000\\text{ L/(m}^2\\cdot\\text{h}\\cdot\\text{bar)}$, calculate intrinsic resistance $R_m$, and examine the transition to limiting flux using a $1.0\\text{ wt}\\%$ bovine serum albumin (BSA) solution.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>In the linear Darcy regime, pure water permeate flux is proportional to transmembrane pressure:</p>
\\[ J = L_p \\cdot \\text{TMP} = \\frac{\\text{TMP}}{\\mu R_m} \\]
<p>where $L_p = 42.5000\\text{ L/(m}^2\\cdot\\text{h}\\cdot\\text{bar)}$ is the membrane permeability slope, $\\text{TMP} = (P_{in} + P_{out})/2 - P_{perm}$, and $R_m = \\frac{1}{\\mu L_p}$ is the clean membrane resistance.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>The test rig features a 316 stainless steel crossflow flat-sheet cell with active membrane area $A = 0.0140\\text{ m}^2$ ($140\\text{ mm} \\times 100\\text{ mm}$, channel height $1.0\\text{ mm}$). Feed is pressurized by a variable-speed diaphragm pump. A $30\\text{ kDa}$ MWCO polyethersulfone (PES) membrane was pre-compacted at $4.0\\text{ bar}$. Pressure transmitters (accuracy $\\pm 0.01\\text{ bar}$) monitor inlet, retentate, and permeate pressures. Permeate discharge is logged on an analytical balance ($\pm 0.01\\text{ g}$) with automatic chronometer recording.</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>The membrane was compacted with deionized water for 30 minutes at $4.0\\text{ bar}$. Crossflow velocity was set to $1.5\\text{ m/s}$ ($T = 25.00^\\circ\\text{C}$). Transmembrane pressure was set to $\\text{TMP} = 0.5\\text{ bar}$. Permeate mass was recorded for 10 minutes to compute steady flux $J$. Pressure was stepped through $1.0, 1.5, 2.0, 2.5,$ and $3.0\\text{ bar}$. The reservoir was subsequently charged with $1.0\\text{ wt}\\%$ BSA solution to observe protein flux decline.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Pressurized membrane circuits ($> 4\\text{ bar}$) present potential high-pressure spray hazards. Overpressure relief valves were set at $5.0\\text{ bar}$. Protective eye shields, lab coats, and gloves were mandatory.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following measurements were recorded for pure deionized water at $T = 25.00^\\circ\\text{C}$ (permeate viscosity $\\mu = 0.890 \\times 10^{-3}\\text{ Pa}\\cdot\\text{s}$):</p>
<table>
<thead>
<tr><th>Run</th><th>$\\text{TMP}$ (bar)</th><th>$\\text{TMP}$ (kPa)</th><th>Permeate Mass $\\Delta m$ (g/10 min)</th><th>Flux $J$ (L/(m$^2$·h))</th><th>Flux $J$ ($10^{-5}\\text{ m/s}$)</th><th>Hydraulic Res $R_m$ ($10^{12}\\text{ m}^{-1}$)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>0.5</td><td>50.0</td><td>49.58</td><td>21.25</td><td>0.590</td><td>9.51</td></tr>
<tr><td>2</td><td>1.0</td><td>100.0</td><td>99.17</td><td>42.50</td><td>1.181</td><td>9.51</td></tr>
<tr><td>3</td><td>1.5</td><td>150.0</td><td>148.75</td><td>63.75</td><td>1.771</td><td>9.51</td></tr>
<tr><td>4</td><td>2.0</td><td>200.0</td><td>198.33</td><td>85.00</td><td>2.361</td><td>9.51</td></tr>
<tr><td>5</td><td>2.5</td><td>250.0</td><td>247.92</td><td>106.25</td><td>2.951</td><td>9.51</td></tr>
<tr><td>6</td><td>3.0</td><td>300.0</td><td>297.50</td><td>127.50</td><td>3.542</td><td>9.51</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of permeate flux $J$ versus transmembrane pressure $\\text{TMP}$ yields:</p>
\\[ J = 42.50000 \\cdot \\text{TMP} + 0.00000 \\]
<p>with coefficient of determination $R^2 = 0.999999$. The experimental slope $L_p = 42.5000\\text{ L/(m}^2\\cdot\\text{h}\\cdot\\text{bar)}$ matches the calibration target ($42.5000$) with $0.00\\%$ deviation. Converting permeability into SI units:</p>
\\[ L_{p,SI} = \\frac{42.5000 \\times 10^{-3} / 3600}{10^5\\text{ Pa}} = 1.1806 \\times 10^{-10}\\text{ m/(s}\\cdot\\text{Pa)} \\]
<p>The clean membrane hydraulic resistance is computed as:</p>
\\[ R_m = \\frac{1}{\\mu \\cdot L_{p,SI}} = \\frac{1}{0.890 \\times 10^{-3}\\text{ Pa}\\cdot\\text{s} \\cdot 1.1806 \\times 10^{-10}\\text{ m/(s}\\cdot\\text{Pa)}} = 9.514 \\times 10^{12}\\text{ m}^{-1} \\]
<p>When filtering $1.0\\text{ wt}\\%$ BSA, flux plateaued at $J_{lim} = 34.2\\text{ L/(m}^2\\cdot\\text{h)}$ above $\\text{TMP} = 1.8\\text{ bar}$, confirming gel polarization formation.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Pressure transducer uncertainty is $\\pm 0.01\\text{ bar}$, and permeate mass resolution is $\\pm 0.01\\text{ g}$. Propagating into $L_p$ yields an experimental uncertainty of $\\pm 0.9\\%$, reporting $L_p = 42.5000 \\pm 0.38\\text{ L/(m}^2\\cdot\\text{h}\\cdot\\text{bar)}$ and $R_m = (9.514 \\pm 0.085) \\times 10^{12}\\text{ m}^{-1}$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The clean water flux displayed perfect Darcy linearity up to $3.0\\text{ bar}$, proving that pre-compaction prevented pressure-dependent pore collapse. During BSA testing, the formation of an impermeable protein gel layer created additional resistance $R_g$, transitioning the system into the film-theory limiting flux regime where higher pressure failed to enhance throughput.</p>

<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>
<p>Crossflow ultrafiltration is widely used in downstream biopharmaceutical processing (protein concentration and buffer exchange via diafiltration), dairy processing (whey protein concentration), and industrial enzyme recovery. In commercial spiral-wound or hollow-fiber systems, operating slightly below the limiting flux maximizes throughput while minimizing irreversible fouling.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is diafiltration used in conjunction with ultrafiltration for protein purification?</strong><br>
<em>A1:</em> While ultrafiltration concentrates macromolecules, diafiltration continuously adds pure buffer to wash permeable microsolutes (salts, unwanted metabolites) through the membrane, purifying the retained protein solution.</p>
<p><strong>Q2: How does ionic strength and pH influence protein ultrafiltration flux?</strong><br>
<em>A2:</em> At the isoelectric point (pI ≈ 4.7 for BSA), protein net charge is zero, minimizing intermolecular electrostatic repulsion; this produces a dense, tightly packed gel layer with low hydraulic permeability, whereas operating away from pI maintains open, porous boundary layers and higher flux.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The crossflow ultrafiltration experiment verified Darcy flow and concentration polarization dynamics. The calibrated clean water permeability $L_p = 42.5000\\text{ L/(m}^2\\cdot\\text{h}\\cdot\\text{bar)}$ ($J = 42.5000 \\cdot \\text{TMP}$) and membrane resistance $R_m = 9.514 \\times 10^{12}\\text{ m}^{-1}$ establish foundational transport parameters for membrane separation unit operations.</p>"""
        },
        {
            "number": 24,
            "slug": "tray-dryer-drying-rate-curve-constant-falling-rate",
            "title": "Convective Tray Drying Kinetics & Constant-to-Falling Drying Rate Transition",
            "shortTitle": "Convective Tray Drying Kinetics",
            "aim": "Determine drying rate curves for a wet porous granular slab in a convective hot-air tray dryer, evaluate the constant drying rate R_c as a function of air velocity v_a, and identify critical moisture content X_c.",
            "inputLabel": "Hot Air Drying Velocity v_a",
            "shortInput": "Air Velocity v_a",
            "inputUnit": "m/s",
            "min": 1.0,
            "max": 6.0,
            "step": 1.0,
            "initial": 3.0,
            "inputDecimals": 1,
            "rawLabel": "Constant Drying Flux R_c",
            "rawUnit": "kg/(m^2·h)",
            "rawDecimals": 3,
            "xAxis": "Air velocity factor (v_a)^0.8 ((m/s)^0.8)",
            "yAxis": "Constant drying rate flux R_c (kg/(m^2·h))",
            "xScale": 1.0,
            "yScale": 1.0,
            "emptyX": 2.8,
            "emptyY": 1.8,
            "targetName": "Convective Drying Velocity Slope S",
            "target": "0.6500",
            "refValue": 0.6500,
            "resultUnit": "kg/(m^2·h)/(m/s)^0.8",
            "resultDecimals": 4,
            "resultScale": 1.0,
            "fitEquation": "R_c = S · (v_a)^0.8 = 0.6500 · (v_a)^0.8",
            "intro": "Drying of moist solids is an energy-intensive simultaneous heat and mass transfer unit operation in chemical engineering, encompassing the manufacturing of pharmaceuticals, pigments, fertilizers, catalysts, polymers, and food products. In convective tray drying, hot dry air sweeps across exposed wet granular slabs placed in shallow trays. Heat conducts and convects from the air stream to the wet solid surface, providing the latent heat required to evaporate moisture, while evaporated water vapor diffuses across the hydrodynamic boundary layer into the bulk air. Plotting the drying rate flux R = - (L_s / A) · (dX / dt) against moisture content X (dry basis, kg water/kg dry solid) reveals characteristic drying periods. In the initial constant-rate drying period (X > X_c), the solid surface is completely saturated with free liquid water, and vaporization proceeds at a constant rate R_c governed purely by external boundary layer heat and mass transfer. Because convective mass transfer across a flat plate scales with air velocity as v_a^0.8 (Reynolds analogy), the constant drying rate follows: R_c = S · v_a^0.8. When moisture drops to the critical moisture content X_c, capillary action can no longer replenish surface water, dry spots appear, and drying enters the falling-rate period where internal moisture diffusion governs drying. In this laboratory investigation, a wet sand slab is dried in a benchtop tunnel tray dryer across air velocities from 1.0 to 6.0 m/s at 50.0 °C to determine the constant drying rate scaling slope S and identify critical moisture content X_c.",
            "modelExtra": "Evaluated using a 200 mm × 200 mm tray (active area A = 0.040 m^2, dry sand mass L_s = 1.20 kg, initial moisture X_0 = 0.25 kg/kg) in a 50.0 °C drying tunnel. Linear regression models constant drying rate R_c versus (v_a)^0.8 to extract S = 0.6500 kg/(m^2·h)/(m/s)^0.8.",
            "apparatus": [
                {"name": "Benchtop Recirculating Tunnel Tray Dryer", "purpose": "Insulated drying duct with variable-speed blower and 3.0 kW electrical finned air heaters."},
                {"name": "Continuous Under-Pan Digital Electronic Balance", "purpose": "Continuously records total tray mass in real-time with 0.01 g precision during drying."},
                {"name": "Instrumented Drying Tray with Insulated Edges", "purpose": "200 mm × 200 mm × 15 mm stainless steel tray (area 0.040 m^2) insulated on sides and bottom."},
                {"name": "Digital Hot-Wire Anemometer Probe", "purpose": "Measures parallel air sweep velocity v_a from 0.5 to 8.0 m/s with 0.05 m/s precision."},
                {"name": "Digital Wet-and-Dry Bulb Psychrometer Array", "purpose": "Measures inlet and outlet air dry-bulb temperature (50.0 °C) and wet-bulb temperature (28.0 °C)."},
                {"name": "Moisture Analyzer & Convection Drying Oven", "purpose": "Oven dries final solids at 105 °C to establish absolute dry solid mass L_s = 1.200 kg."}
            ],
            "procedure": [
                {"title": "Tunnel Warm-Up & Psychrometric Equilibrium", "text": "Set air heater to 50.0 °C and blower to moderate speed; circulate air for 20 minutes until dry-bulb (50.0 °C) and wet-bulb (28.0 °C) steady state is achieved."},
                {"title": "Wet Slab Preparation & Placement", "text": "Mix 1.200 kg of dry quartz sand with 300 g of water (X_0 = 0.250 kg/kg); pack into the tray flush with the rim and place onto the balance cradle."},
                {"title": "Initial Air Velocity Setpoint", "text": "Adjust blower speed to establish air velocity v_a = 1.0 m/s across the tray surface; record initial mass at t = 0."},
                {"title": "Continuous Mass Loss Logging", "text": "Log tray mass every 60 seconds over 40 minutes; compute moisture content X(t) and instantaneous drying rate flux R = -(L_s/A) · (dX/dt)."},
                {"title": "Velocity Progression Protocol", "text": "Repeat tests with fresh identical wet slabs at air velocities v_a = 2.0, 3.0, 4.0, 5.0, and 6.0 m/s, recording the constant drying rate plateau R_c for each run."},
                {"title": "Drying Rate Curve & Scaling Regression", "text": "Plot R versus X to locate critical moisture X_c, plot R_c versus (v_a)^0.8, and fit a linear regression through the origin to determine S."}
            ],
            "topics": [
                {"question": "Why does the drying rate remain strictly constant during the constant-rate period?", "answer": "The solid surface remains completely covered by a continuous film of free water fed by capillary action from the porous interior; the rate is governed entirely by external convective heat and mass transfer across the air boundary layer, functioning like a wet-bulb thermometer."},
                {"question": "What is the critical moisture content X_c and what parameters influence its value?", "answer": "X_c is the average moisture content at which the constant-rate period ends and the falling-rate period begins; it depends on particle size, pore structure, slab thickness, and drying rate (higher drying rates cause earlier surface dryout, increasing X_c)."},
                {"question": "What mechanisms govern moisture transport during the falling-rate drying period?", "answer": "Internal liquid movement occurs via liquid capillary flow in pores, vapor diffusion through unsaturated pores, and surface adsorption diffusion; as moisture drops toward equilibrium moisture X_e, internal diffusion becomes severely rate-limiting."},
                {"question": "Why does the temperature of the wet solid equal the wet-bulb temperature during the constant-rate period?", "answer": "All heat conducted and convected from the air to the solid is consumed as latent heat of vaporization (h (T_air - T_s) = R_c λ); dynamic thermal equilibrium naturally stabilizes the surface at the adiabatic saturation (wet-bulb) temperature."},
                {"question": "How does relative humidity of the drying air affect drying rate?", "answer": "The mass transfer driving force is the humidity difference (Y_sat - Y_air); higher ambient humidity reduces this gradient, decreasing the constant drying rate and elevating equilibrium moisture content X_e."},
                {"question": "What is case hardening (surface crusting) in food and ceramic drying?", "answer": "Excessively rapid early drying evaporates surface moisture faster than internal water can diffuse, causing colloidal shrinkage, pore collapse, and formation of an impermeable hard crust that traps internal moisture and causes cracking."}
            ],
            "precautions": [
                "Insulate the bottom and sides of the tray to ensure heat transfer occurs strictly across the top exposed horizontal surface.",
                "Maintain constant air dry-bulb and wet-bulb temperatures throughout the drying cycle.",
                "Ensure the sand surface is packed smooth and flush with tray edges to avoid aerodynamic trip edges.",
                "Calibrate the under-pan balance with test weights before each run."
            ],
            "quiz": [
                {
                    "question": "During the constant-rate drying period of a wet solid, the surface temperature of the solid equals:",
                    "options": ["The ambient dry-bulb temperature", "The psychrometric wet-bulb temperature", "The boiling point of water (100 °C)", "Absolute zero"],
                    "correct": 1,
                    "explanation": "Because all convective heat arriving at the surface is consumed by latent heat of evaporation, the surface naturally stays at the wet-bulb temperature."
                },
                {
                    "question": "The transition point separating the constant-rate drying period from the falling-rate period is called:",
                    "options": ["Equilibrium moisture content", "Critical moisture content (X_c)", "Bound moisture limit", "Saturated vapor point"],
                    "correct": 1,
                    "explanation": "The critical moisture content X_c is the specific moisture level where surface liquid films break and the drying rate begins to decline."
                },
                {
                    "question": "Convective mass transfer over a flat tray surface dictates that the constant drying rate R_c scales with air velocity v_a as:",
                    "options": ["v_a^0.2", "v_a^0.8", "v_a^2.0", "Independent of velocity"],
                    "correct": 1,
                    "explanation": "Turbulent boundary layer transport over flat surfaces (Reynolds analogy) dictates convective heat/mass transfer coefficients scale with v_a^0.8."
                },
                {
                    "question": "Moisture that cannot be removed by contact with air of given temperature and humidity is termed:",
                    "options": ["Free moisture", "Unbound moisture", "Equilibrium moisture content (X_e)", "Critical moisture"],
                    "correct": 2,
                    "explanation": "Equilibrium moisture content X_e is the residual moisture in thermodynamic equilibrium with the humidity of the ambient drying air."
                }
            ],
            "samples": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "measureLabel": "Record constant drying rate flux",
            "readings": ["drying_flux", "velocity_pow", "moisture_xc", "wetbulb_temp"],
            "theory": """<h3>1. Heat and Mass Transfer Mechanisms in Convective Drying</h3>
<p>Drying involves simultaneous thermal energy transfer from a heated drying gas to a wet solid and mass transfer of vaporized moisture from the solid back into the gas stream. In tray drying, warm air at temperature $T_a$ and humidity $Y_a$ flows over a horizontal wet porous slab.</p>

<h3>2. The Constant-Rate Drying Period</h3>
<p>When the solid contains abundant moisture ($X > X_c$), capillary forces pump liquid water from internal pores to the surface as rapidly as it evaporates. The surface behaves as a continuous pool of water. Equating convective heat supply to latent heat vaporization flux:</p>
\\[ q = h A (T_a - T_w) = R_c A \\lambda_w \\]
<p>where $h$ is the convective heat transfer coefficient, $T_w$ is the wet-bulb surface temperature, $\\lambda_w$ is latent heat of vaporization, and $R_c$ is drying flux ($\\text{kg/(m}^2\\cdot\\text{h)}$). Expressing in terms of mass transfer:</p>
\\[ R_c = k_y (Y_w - Y_a) \\]
<p>where $k_y$ is the gas-phase mass transfer coefficient and $Y_w$ is saturation humidity at $T_w$.</p>

<h3>3. Velocity Scaling & Boundary Layer Analogy</h3>
<p>From the Chilton–Colburn $j_H$ and $j_D$ analogies for turbulent flow over flat plates, convective heat and mass transfer coefficients scale with Reynolds number as $Re^{0.8} \\propto v_a^{0.8}$. Therefore, constant drying rate flux follows the power-law relation:</p>
\\[ R_c = S \\cdot (v_a)^{0.8} \\]
<p>where $S$ is the convective drying velocity slope in $\\text{kg/(m}^2\\cdot\\text{h)/(m/s)}^{0.8}$.</p>

<h3>4. Critical Moisture Content & The Falling-Rate Period</h3>
<p>At the critical moisture content $X_c$, internal capillary flow can no longer maintain surface saturation. Dry spots develop, and the drying rate declines. In the first falling-rate period, unsaturated surface drying occurs; in the second falling-rate period, the evaporation plane recedes into the interior, and internal vapor diffusion governs drying kinetics.</p>""",
            "report": """<h3>1. Objective & Practical Significance</h3>
<p>This laboratory investigation determines the drying kinetics of a wet granular quartz sand slab ($A = 0.040\\text{ m}^2$, dry mass $L_s = 1.200\\text{ kg}$, initial moisture $X_0 = 0.250\\text{ kg/kg}$) in a tunnel tray dryer operating at $50.0^\\circ\\text{C}$ air temperature ($T_{wb} = 28.0^\\circ\\text{C}$). Across air velocities $v_a$ from $1.0$ to $6.0\\text{ m/s}$, we record drying curves, verify the $v_a^{0.8}$ convective scaling model for constant drying flux $R_c$, determine the velocity sensitivity slope $S = 0.6500\\text{ kg/(m}^2\\cdot\\text{h)/(m/s)}^{0.8}$, and identify the critical moisture content $X_c = 0.120\\text{ kg/kg}$.</p>

<h3>2. Governing Transport Equations & Phenomenological Relations</h3>
<p>Instantaneous drying rate flux is defined as $R = -\\frac{L_s}{A} \\frac{dX}{dt}$. In the constant-rate period, drying flux follows the turbulent convective boundary layer model:</p>
\\[ R_c = S \\cdot (v_a)^{0.8} \\]
<p>where $S = 0.6500\\text{ kg/(m}^2\\cdot\\text{h)/(m/s)}^{0.8}$ represents the empirical convective velocity sensitivity. Critical moisture content $X_c$ marks the departure from constant rate.</p>

<h3>3. Experimental Apparatus & Instrumentation Specification</h3>
<p>The drying tunnel features an aerodynamic test duct ($200\\text{ mm} \\times 200\\text{ mm}$) with an isolated tray cradle ($200\\text{ mm} \\times 200\\text{ mm}$, depth $15\\text{ mm}$, active surface area $A = 0.0400\\text{ m}^2$) suspended above an electronic load cell ($\pm 0.01\\text{ g}$). Air velocity is monitored by a hot-wire anemometer (accuracy $\\pm 0.05\\text{ m/s}$). Platinum RTD probes log dry-bulb ($50.0 \\pm 0.1^\\circ\\text{C}$) and wet-bulb ($28.0 \\pm 0.1^\\circ\\text{C}$) temperatures.</p>

<h3>4. Standard Operating Procedure & Measurement Protocols</h3>
<p>The drying tunnel was preheated to $50.0^\\circ\\text{C}$ at $v_a = 1.0\\text{ m/s}$. Wet sand slabs ($1.200\\text{ kg}$ dry sand with $300\\text{ g}$ water, $X_0 = 0.250$) were packed into the tray and mounted on the balance. Mass loss was logged continuously over 40 minutes. The procedure was repeated for air velocities $v_a = 2.0, 3.0, 4.0, 5.0,$ and $6.0\\text{ m/s}$. The constant-rate plateau $R_c$ was evaluated for each velocity.</p>

<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>
<p>Tunnel air heaters reach high temperatures. High-temperature limit switches interlocked heaters with blower operation. Safety glasses and thermal gloves were worn.</p>

<h3>6. Raw Experimental Observations & Systematic Data Records</h3>
<p><strong>Simulated demonstration data.</strong> The following observations were recorded at constant air temperature $T_{db} = 50.0^\\circ\\text{C}$ and wet-bulb $T_{wb} = 28.0^\\circ\\text{C}$ (dry solid mass $L_s = 1.200\\text{ kg}$, area $A = 0.040\\text{ m}^2$):</p>
<table>
<thead>
<tr><th>Run</th><th>Air Velocity $v_a$ (m/s)</th><th>$(v_a)^{0.8}$ ((m/s)$^{0.8}$)</th><th>Constant Flux $R_c$ (kg/(m$^2$·h))</th><th>Mass Loss Rate $dm/dt$ (g/min)</th><th>Critical Moisture $X_c$ (kg/kg)</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>1.0</td><td>1.000</td><td>0.650</td><td>0.433</td><td>0.108</td></tr>
<tr><td>2</td><td>2.0</td><td>1.516</td><td>0.985</td><td>0.657</td><td>0.115</td></tr>
<tr><td>3</td><td>3.0</td><td>1.933</td><td>1.256</td><td>0.838</td><td>0.120</td></tr>
<tr><td>4</td><td>4.0</td><td>2.297</td><td>1.493</td><td>0.995</td><td>0.124</td></tr>
<tr><td>5</td><td>5.0</td><td>2.627</td><td>1.708</td><td>1.138</td><td>0.128</td></tr>
<tr><td>6</td><td>6.0</td><td>2.930</td><td>1.905</td><td>1.270</td><td>0.131</td></tr>
</tbody>
</table>

<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>
<p>Linear regression of constant drying rate flux $R_c$ versus $(v_a)^{0.8}$ yields:</p>
\\[ R_c = 0.65000 \\cdot (v_a)^{0.8} + 0.00000 \\]
<p>with coefficient of determination $R^2 = 0.999999$. The experimental slope $S = 0.65000\\text{ kg/(m}^2\\cdot\\text{h)/(m/s)}^{0.8}$ matches the benchmark calibration target ($0.6500$) with $0.00\\%$ deviation. The constant drying rate nearly tripled from $0.650\\text{ kg/(m}^2\\cdot\\text{h)}$ at $1.0\\text{ m/s}$ to $1.905\\text{ kg/(m}^2\\cdot\\text{h)}$ at $6.0\\text{ m/s}$.</p>

<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>
<p>Load cell mass uncertainty is $\\pm 0.01\\text{ g}$, timer resolution is $\\pm 0.1\\text{ s}$, and air velocity error is $\\pm 0.05\\text{ m/s}$. Propagating into drying flux $R_c$ yields an experimental uncertainty of $\\pm 1.3\\%$, reporting $S = 0.6500 \\pm 0.0085\\text{ kg/(m}^2\\cdot\\text{h)/(m/s)}^{0.8}$. Critical moisture content averaged $X_c = 0.120 \\pm 0.008\\text{ kg/kg}$.</p>

<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>
<p>The exact agreement with $v_a^{0.8}$ confirms that external turbulent boundary layer mass transfer governs the constant-rate period. As air velocity increased, the critical moisture content $X_c$ shifted slightly upward (from $0.108$ to $0.131\\text{ kg/kg}$) because rapid surface evaporation outpaced capillary liquid replenishment, initiating surface dryout earlier.</p>

<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>
<p>Convective drying kinetics govern the design of industrial conveyor belt dryers, fluidized bed dryers, and spray dryers. Knowing $R_c$ and $X_c$ allows chemical engineers to calculate total drying cycle time and thermal duty, optimizing air recirculation ratios to minimize fuel consumption.</p>

<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>
<p><strong>Q1: Why is increasing air velocity ineffective at accelerating drying during the late falling-rate period?</strong><br>
<em>A1:</em> In the late falling-rate period, the evaporation front has receded into the interior of the porous matrix; internal molecular diffusion controls the drying rate, rendering external air velocity almost completely irrelevant.</p>
<p><strong>Q2: How does elevating air temperature accelerate both constant-rate and falling-rate drying?</strong><br>
<em>A2:</em> In the constant-rate period, higher temperature increases the psychrometric driving force $(T_a - T_w)$ and saturation humidity $Y_w$; in the falling-rate period, higher solid temperature increases internal liquid diffusivity and water vapor vapor pressure.</p>

<h3>12. Concluding Summary & Verified Engineering Metric</h3>
<p>The convective tray drying experiment confirmed boundary layer transport and drying kinetics. The measured velocity sensitivity slope $S = 0.6500\\text{ kg/(m}^2\\cdot\\text{h)/(m/s)}^{0.8}$ ($R_c = 0.6500 \\cdot v_a^{0.8}$) and critical moisture content $X_c = 0.120\\text{ kg/kg}$ establish essential engineering metrics for convective solids drying equipment design.</p>"""
        }
    ]
