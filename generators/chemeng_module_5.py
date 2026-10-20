# -*- coding: utf-8 -*-
"""Chemical & Process Engineering Module 5: Chemical Thermodynamics, Phase Equilibria & Solution Properties (Labs 33–39)."""

def get_module_5():
    return [
        {
                "number": 33,
                "slug": "vapor-liquid-equilibrium-vle-wilson-margules",
                "title": "Vapor-Liquid Equilibrium (VLE) & Thermodynamic Consistency via Wilson & Margules Activity Models",
                "shortTitle": "VLE Thermodynamic Consistency",
                "aim": "Operate a precision vapor-recirculating Othmer VLE still for a binary ethanol-water system at 101.325 kPa, determine equilibrium vapor and liquid mole fractions (y_1, x_1) using Abbe refractometry, compute liquid-phase activity coefficients (γ_1, γ_2), and evaluate thermodynamic consistency via the Margules and Wilson excess Gibbs energy models.",
                "inputLabel": "Liquid Phase Ethanol Mole Fraction x_1",
                "shortInput": "Liquid Mole Fraction x_1",
                "inputUnit": "mol/mol",
                "min": 0.1,
                "max": 0.6,
                "step": 0.1,
                "initial": 0.3,
                "inputDecimals": 2,
                "rawLabel": "Margules Activity Factor ln(γ_1) / (1 - x_1)",
                "rawUnit": "dimensionless",
                "rawDecimals": 4,
                "xAxis": "Liquid mole fraction x_1 (mol/mol)",
                "yAxis": "Margules factor ln(γ_1) / (1 - x_1)",
                "xScale": 1.0,
                "yScale": 1.0,
                "emptyX": 0.35,
                "emptyY": 0.25,
                "targetName": "Margules Binary Interaction Parameter A_12",
                "target": "0.7250",
                "refValue": 0.725,
                "resultUnit": "dimensionless",
                "resultDecimals": 4,
                "resultScale": 1.0,
                "fitEquation": "ln(γ_1) / (1 - x_1) = A_12 · x_1 = 0.7250 · x_1",
                "intro": "In chemical engineering thermodynamics, accurate vapor-liquid equilibrium (VLE) data are indispensable for designing, simulating, and optimizing distillation columns, flash drums, and reactive separation units. Ideal solutions follow Raoult's law: P · y_i = x_i · P_i^sat, where total system pressure P and vapor mole fraction y_i are governed purely by liquid mole fraction x_i and pure-component saturation vapor pressure P_i^sat. However, real chemical mixtures—particularly polar, hydrogen-bonding mixtures such as ethanol and water—exhibit pronounced deviations from ideal solution behavior due to molecular size disparities and asymmetric intermolecular forces. These non-idealities are captured through liquid-phase activity coefficients γ_i: P · y_i · Φ_i = x_i · γ_i · P_i^sat · φ_i^sat · exp[V_i^L (P - P_i^sat) / (R T)], where Φ_i is the vapor fugacity coefficient and the exponential term is the Poynting correction factor. At atmospheric pressure (101.325 kPa), vapor-phase non-idealities and Poynting factors are negligible, reducing the equilibrium relation to the modified Raoult's law: P · y_i = x_i · γ_i · P_i^sat(T). The excess Gibbs free energy G^E represents the thermodynamic penalty or gain of mixing relative to an ideal solution: G^E / (R T) = Σ [x_i · ln(γ_i)]. Classical excess Gibbs energy models include the two-suffix Margules equation, the van Laar equation, and local composition formulations such as the Wilson, NRTL (Non-Random Two-Liquid), and UNIQUAC models. In the Margules formulation, the activity coefficient of the volatile solute is expressed as ln(γ_1) = A_12 · (1 - x_1)^2, which rearranges to the linear form ln(γ_1) / (1 - x_1) = A_12 · x_1. Furthermore, experimental VLE datasets must satisfy the Gibbs–Duhem thermodynamic consistency equation: Σ [x_i · d(ln γ_i)] = 0 at constant temperature and pressure. Area tests (such as the Redlich–Kister integral criterion) and point-to-point consistency tests verify whether measured equilibrium compositions are physically sound or distorted by experimental systematic errors. In this laboratory investigation, an all-glass recirculating Othmer VLE still is operated across ethanol liquid mole fractions from 0.10 to 0.60 at 101.325 kPa to determine equilibrium temperatures, vapor compositions, and the Margules interaction parameter A_12 = 0.7250.",
                "modelExtra": "Evaluated using an all-glass Othmer recirculating VLE equilibrium still with platinum RTD temperature sensing (±0.02 °C) and Abbe refractometric composition analysis (±0.0002 n_D). Pure component Antoine parameters: Ethanol (A=16.8958, B=3795.17, C=230.918), Water (A=16.3872, B=3885.70, C=230.170).",
                "apparatus": [
                        {
                                "name": "All-Glass Recirculating Othmer VLE Still",
                                "purpose": "Provides continuous boiling, vapor condensation, and liquid/vapor recirculation until thermodynamic equilibrium is achieved."
                        },
                        {
                                "name": "Precision Digital Abbe Refractometer",
                                "purpose": "Determines ethanol and water mole fractions in condensed liquid and vapor samples with ±0.0002 refractive index accuracy."
                        },
                        {
                                "name": "Calibrated 4-Wire Pt100 RTD Sensor & Digital Indicator",
                                "purpose": "Measures equilibrium mixture boiling temperature with 0.01 °C resolution directly in the liquid-vapor mixing zone."
                        },
                        {
                                "name": "Mantle Heater with Variable Autotransformer (Variac)",
                                "purpose": "Provides uniform, bump-free electrical heating to maintain steady boiling without superheating."
                        },
                        {
                                "name": "Recirculating Chiller & Double-Surface Condenser",
                                "purpose": "Maintains coolant at 10.0 °C to condense vapor effluent completely without volatile loss."
                        },
                        {
                                "name": "Digital Absolute Barometer & Pressure Compensator",
                                "purpose": "Logs barometric pressure with 0.01 kPa accuracy to correct Antoine saturation vapor pressures."
                        }
                ],
                "procedure": [
                        {
                                "title": "Refractometer Calibration & Baseline Verification",
                                "text": "Calibrate the digital Abbe refractometer with HPLC-grade deionized water (n_D = 1.3330 at 20.0 °C) and pure absolute ethanol (n_D = 1.3614); verify calibration curve."
                        },
                        {
                                "title": "Still Charging & Coolant Circulation",
                                "text": "Charge the boiling vessel with 250 mL of prepared binary ethanol-water solution at x_1 = 0.10; start recirculating condenser coolant at 10.0 °C."
                        },
                        {
                                "title": "Boiling Initiation & Recirculation Steady State",
                                "text": "Apply 85 W heating via the Variac until gentle, continuous boiling is established; operate in total recirculation mode for 45 minutes until equilibrium boiling temperature stabilizes within ±0.02 °C."
                        },
                        {
                                "title": "Equilibrium Sampling & Optical Analysis",
                                "text": "Simultaneously withdraw 0.5 mL samples of equilibrium liquid and condensed vapor using pre-chilled microsyringes; measure refractive indices at 20.0 °C to find x_1 and y_1."
                        },
                        {
                                "title": "Composition Step Progression Protocol",
                                "text": "Increment liquid mole fraction x_1 through 0.20, 0.30, 0.40, 0.50, and 0.60 by injecting calculated aliquots of absolute ethanol, repeating equilibrium logging at each step."
                        },
                        {
                                "title": "Thermodynamic Activity & Consistency Regression",
                                "text": "Calculate saturation vapor pressures P_i^sat via Antoine equations, determine activity coefficients γ_1 and γ_2, evaluate ln(γ_1) / (1 - x_1), and perform linear regression to determine A_12."
                        }
                ],
                "topics": [
                        {
                                "question": "What is the difference between positive and negative deviations from Raoult's law?",
                                "answer": "Positive deviations (γ_i > 1) occur when unlike molecular interactions (A-B) are weaker and more repulsive than like interactions (A-A or B-B), promoting volatilization and often forming minimum-boiling azeotropes; negative deviations (γ_i < 1) indicate strong unlike attractions (e.g. hydrogen bonding between chloroform and acetone), reducing volatility and producing maximum-boiling azeotropes."
                        },
                        {
                                "question": "How does the Gibbs–Duhem equation enforce thermodynamic consistency on binary VLE data?",
                                "answer": "At constant T and P, the Gibbs–Duhem relation x_1 d(ln γ_1) + x_2 d(ln γ_2) = 0 requires that changes in the two activity coefficients are strictly coupled; an area or point test integrates this constraint across composition, where any significant non-zero net area reveals systematic experimental measurement error."
                        },
                        {
                                "question": "Why is an Othmer still preferred over a simple batch distillation flask for VLE measurements?",
                                "answer": "Simple distillation produces continuous fractional depletion and shifting liquid composition; an Othmer still recirculates both the condensed vapor and returning liquid, maintaining constant macroscopic liquid composition until true dynamic and phase equilibrium is reached."
                        },
                        {
                                "question": "What is an azeotrope and why cannot it be separated by conventional distillation?",
                                "answer": "An azeotrope is a thermodynamic state where the equilibrium vapor composition is identical to the liquid composition (y_i = x_i) and the relative volatility α_12 = 1.0; at this pinch point, boiling produces vapor of identical composition, preventing further separation by ordinary distillation."
                        },
                        {
                                "question": "How do the Wilson and Margules models differ in handling liquid-liquid immiscibility?",
                                "answer": "The Margules equation is capable of predicting both vapor-liquid and liquid-liquid phase splits; the classic Wilson equation cannot predict liquid-liquid immiscibility (phase separation) because its mathematical form always exhibits positive second derivatives of excess Gibbs energy."
                        },
                        {
                                "question": "How does barometric pressure variation affect measured VLE equilibrium temperatures?",
                                "answer": "Boiling temperatures vary directly with ambient barometric pressure according to the Clausius–Clapeyron equation; deviations of ±1 kPa from standard 101.325 kPa shift ethanol boiling point by ~0.35 °C, requiring continuous barometric pressure logging and Antoine temperature correction."
                        }
                ],
                "precautions": [
                        "Ensure ethanol-water sampling syringes are pre-chilled to prevent flash evaporation of volatile ethanol during transfer to the refractometer.",
                        "Verify condenser coolant flow is established before turning on mantle heating to prevent vapor escape and flammability hazards.",
                        "Maintain steady boiling without rapid boil-up surges to avoid entraining liquid droplets into the vapor condensation chamber.",
                        "Confirm total recirculation equilibrium by ensuring boiling temperature remains strictly constant for at least 15 minutes before sampling."
                ],
                "quiz": [
                        {
                                "question": "For a binary mixture obeying the modified Raoult's law, the liquid-phase activity coefficient γ_1 is calculated as:",
                                "options": [
                                        "γ_1 = (P · y_1) / (x_1 · P_1^sat)",
                                        "γ_1 = (x_1 · P) / (y_1 · P_1^sat)",
                                        "γ_1 = (y_1 · P_1^sat) / (x_1 · P)",
                                        "γ_1 = (P · x_1 · y_1) / P_1^sat"
                                ],
                                "correct": 0,
                                "explanation": "Equating vapor and liquid fugacities at low pressure gives P · y_1 = x_1 · γ_1 · P_1^sat, so γ_1 = (P · y_1) / (x_1 · P_1^sat)."
                        },
                        {
                                "question": "The Redlich–Kister area test for thermodynamic consistency requires that the integral of ln(γ_1/γ_2) dx_1 from 0 to 1 must be:",
                                "options": [
                                        "Equal to 1.0",
                                        "Strictly equal to zero",
                                        "Equal to the enthalpy of vaporization",
                                        "Equal to the total pressure"
                                ],
                                "correct": 1,
                                "explanation": "Thermodynamic consistency under isothermal conditions dictates that the net integral of ln(γ_1/γ_2) across the full mole fraction range (0 to 1) must equal zero."
                        },
                        {
                                "question": "In the Margules 2-suffix model, what is the excess Gibbs energy G^E / (R T) equal to?",
                                "options": [
                                        "A_12 · x_1 · x_2",
                                        "A_12 / (x_1 · x_2)",
                                        "A_12 · (x_1^2 + x_2^2)",
                                        "A_12 · ln(x_1 / x_2)"
                                ],
                                "correct": 0,
                                "explanation": "The symmetric 2-suffix Margules excess Gibbs energy formulation is G^E / (R T) = A_12 · x_1 · x_2 = A_12 · x_1 · (1 - x_1)."
                        },
                        {
                                "question": "At the azeotropic composition of a binary mixture at pressure P, the relative volatility α_12 is:",
                                "options": [
                                        "0.00",
                                        "0.50",
                                        "1.00",
                                        "Infinite"
                                ],
                                "correct": 2,
                                "explanation": "Since relative volatility is α_12 = (y_1 / x_1) / (y_2 / x_2), when y_1 = x_1 and y_2 = x_2, α_12 equals exactly 1.00."
                        }
                ],
                "samples": [
                        0.1,
                        0.2,
                        0.3,
                        0.4,
                        0.5,
                        0.6
                ],
                "measureLabel": "Record equilibrium VLE state",
                "readings": [
                        "x_1",
                        "y_1",
                        "t_boil",
                        "gamma_1",
                        "gamma_2",
                        "margules_factor"
                ],
                "theory": "<h3>Phase Equilibrium Thermodynamics & Chemical Potential Equality</h3>\n<p>Phase equilibrium in multicomponent chemical systems is governed by the second law of thermodynamics. For a closed system containing $C$ chemical species partitioned across vapor ($V$) and liquid ($L$) phases at uniform temperature $T$ and pressure $P$, thermodynamic equilibrium is established when the chemical potential of every species $i$ is identical in both coexisting phases:</p>\n\\[ \\mu_i^L(T, P, \\mathbf{x}) = \\mu_i^V(T, P, \\mathbf{y}), \\quad \\forall i = 1, 2, \\dots, C \\]\n<p>Because absolute chemical potentials diverge logarithmically at infinite dilution, chemical engineers express phase equilibrium through fugacity $\\hat{f}_i$, defined by G. N. Lewis as $d\\mu_i = R T \\, d(\\ln \\hat{f}_i)$ at constant temperature, with the ideal gas reference state $\\lim_{P \\to 0} (\\hat{f}_i / (y_i P)) = 1$. The equilibrium condition is therefore stated as fugacity equality:</p>\n\\[ \\hat{f}_i^L(T, P, \\mathbf{x}) = \\hat{f}_i^V(T, P, \\mathbf{y}) \\]\n\n<h3>Liquid-Phase Activity Coefficients & Modified Raoult's Law</h3>\n<p>In the vapor phase, the fugacity is related to total pressure and vapor composition by the vapor fugacity coefficient $\\hat{\\Phi}_i^V$:</p>\n\\[ \\hat{f}_i^V = y_i \\, P \\, \\hat{\\Phi}_i^V \\]\n<p>In the liquid phase, fugacity is described relative to the pure liquid standard state $f_i^\\circ = P_i^{sat} \\, \\phi_i^{sat} \\, \\exp\\left[ \\frac{V_i^L (P - P_i^{sat})}{R T} \\right]$ by introducing the liquid-phase activity coefficient $\\gamma_i$:</p>\n\\[ \\hat{f}_i^L = x_i \\, \\gamma_i \\, P_i^{sat} \\, \\phi_i^{sat} \\, \\exp\\left[ \\frac{V_i^L (P - P_i^{sat})}{R T} \\right] \\]\n<p>At atmospheric pressure ($P = 101.325\\text{ kPa}$), the vapor behaves as an ideal gas mixture ($\\hat{\\Phi}_i^V \\approx 1$, $\\phi_i^{sat} \\approx 1$), and the Poynting correction factor $\\exp[V_i^L(P - P_i^{sat})/(RT)] \\approx 1.000$, simplifying equilibrium to the modified Raoult's law:</p>\n\\[ y_i \\, P = x_i \\, \\gamma_i \\, P_i^{sat}(T) \\implies \\gamma_i = \\frac{y_i \\, P}{x_i \\, P_i^{sat}(T)} \\]\n<p>Saturation vapor pressure $P_i^{sat}(T)$ is computed from the three-parameter Antoine equation:</p>\n\\[ \\ln P_i^{sat} = A_i - \\frac{B_i}{T + C_i} \\]\n\n<h3>Excess Gibbs Energy Models & Margules Parameter Formulation</h3>\n<p>The non-ideality of the liquid mixture is represented by the molar excess Gibbs free energy $G^E$:</p>\n\\[ \\frac{G^E}{R T} = \\sum_{i=1}^C x_i \\ln \\gamma_i = x_1 \\ln \\gamma_1 + x_2 \\ln \\gamma_2 \\]\n<p>The symmetric two-suffix Margules model represents excess Gibbs energy as a quadratic function of composition:</p>\n\\[ \\frac{G^E}{R T} = A_{12} \\, x_1 \\, x_2 = A_{12} \\, x_1 \\, (1 - x_1) \\]\n<p>Differentiating $n_t G^E / (R T)$ with respect to mole numbers $n_1$ and $n_2$ yields the activity coefficients:</p>\n\\[ \\ln \\gamma_1 = A_{12} \\, x_2^2 = A_{12} \\, (1 - x_1)^2 \\]\n\\[ \\ln \\gamma_2 = A_{12} \\, x_1^2 \\]\n<p>Dividing $\\ln \\gamma_1$ by $(1 - x_1)$ produces the linearized diagnostic expression:</p>\n\\[ \\frac{\\ln \\gamma_1}{1 - x_1} = A_{12} \\, (1 - x_1) \\quad \\text{or directly against composition: } \\frac{\\ln \\gamma_1}{1 - x_1} = A_{12} \\, x_1 \\]\n<p>Plotting the activity factor against liquid mole fraction provides a direct linear regression to extract the binary Margules interaction parameter $A_{12} = 0.7250$.</p>",
                "report": "<h3>1. Objective & Practical Significance</h3>\n<p>This experiment investigates vapor-liquid equilibrium (VLE) in a binary ethanol (1) + water (2) system at atmospheric pressure ($101.325\\text{ kPa}$) using an all-glass recirculating Othmer equilibrium still. By measuring equilibrium boiling temperatures and vapor/liquid mole fractions across $x_1 = 0.10$ to $0.60$ via precision Abbe refractometry, we calculate liquid-phase activity coefficients $\\gamma_1$ and $\\gamma_2$, test thermodynamic consistency, and determine the binary Margules interaction parameter $A_{12} = 0.7250$.</p>\n\n<h3>2. Governing Transport Equations & Phenomenological Relations</h3>\n<p>Phase equilibrium under modified Raoult's law dictates:</p>\n\\[ y_1 P = x_1 \\gamma_1 P_1^{sat}(T), \\quad y_2 P = x_2 \\gamma_2 P_2^{sat}(T) \\]\n<p>The two-suffix Margules excess Gibbs energy model provides:</p>\n\\[ \\ln \\gamma_1 = A_{12} \\cdot (1 - x_1)^2 \\implies \\frac{\\ln \\gamma_1}{1 - x_1} = S \\cdot x_1 = 0.7250 \\cdot x_1 \\]\n<p>where $S = A_{12} = 0.7250\\text{ dimensionless}$.</p>\n\n<h3>3. Experimental Apparatus & Instrumentation Specification</h3>\n<p>The apparatus consists of an all-glass Othmer recirculating VLE still with vacuum-jacketed boiling chamber ($250\\text{ mL}$), a precision 4-wire Pt100 RTD sensor ($\\pm 0.01^\\circ\\text{C}$), a digital Abbe refractometer (ATAGO NAR-1T, $\\pm 0.0002\\, n_D$), a constant-temperature recirculating bath ($10.0^\\circ\\text{C}$), and an electronic digital barometer ($\\pm 0.01\\text{ kPa}$).</p>\n\n<h3>4. Standard Operating Procedure & Measurement Protocols</h3>\n<p>The refractometer was calibrated at $20.0^\\circ\\text{C}$ using deionized water ($n_D = 1.3330$) and pure ethanol ($n_D = 1.3614$). The still was charged with $200\\text{ mL}$ of mixture at $x_1 = 0.10$. Heating was applied until steady total recirculation boiling was maintained. After 45 minutes of thermal equilibrium ($\\Delta T < 0.02^\\circ\\text{C}$ over 15 min), liquid and condensed vapor samples were withdrawn and analyzed. The mixture was stepped through $x_1 = 0.20, 0.30, 0.40, 0.50,$ and $0.60$.</p>\n\n<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>\n<p>Ethanol vapors are flammable. Condenser cooling was interlocked with mantle power to prevent vapor release. Sampling was performed with pre-chilled airtight syringes in a well-ventilated fume hood. Chemical splash goggles, neoprene gloves, and flame-retardant lab coats were worn.</p>\n\n<h3>6. Raw Experimental Observations & Systematic Data Records</h3>\n<p><strong>Simulated demonstration data.</strong> The following equilibrium observations were recorded at $P = 101.325\\text{ kPa}$:</p>\n<table>\n<thead>\n<tr><th>Run</th><th>Liquid $x_1$ (mol/mol)</th><th>Vapor $y_1$ (mol/mol)</th><th>Boiling $T$ (°C)</th><th>$P_1^{sat}$ (kPa)</th><th>Activity $\\gamma_1$</th><th>Margules Factor $\\frac{\\ln \\gamma_1}{1 - x_1}$</th></tr>\n</thead>\n<tbody>\n<tr><td>1</td><td>0.10</td><td>0.5284</td><td>92.65</td><td>184.2</td><td>2.9056</td><td>0.0725</td></tr>\n<tr><td>2</td><td>0.20</td><td>0.6562</td><td>86.82</td><td>145.8</td><td>2.2818</td><td>0.1450</td></tr>\n<tr><td>3</td><td>0.30</td><td>0.7122</td><td>83.74</td><td>128.5</td><td>1.8727</td><td>0.2175</td></tr>\n<tr><td>4</td><td>0.40</td><td>0.7461</td><td>82.05</td><td>119.8</td><td>1.5772</td><td>0.2900</td></tr>\n<tr><td>5</td><td>0.50</td><td>0.7725</td><td>80.95</td><td>114.4</td><td>1.3668</td><td>0.3625</td></tr>\n<tr><td>6</td><td>0.60</td><td>0.7984</td><td>80.12</td><td>110.6</td><td>1.2214</td><td>0.4350</td></tr>\n</tbody>\n</table>\n\n<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>\n<p>Linear regression of the Margules factor $\\frac{\\ln \\gamma_1}{1 - x_1}$ versus liquid mole fraction $x_1$ yields:</p>\n\\[ \\frac{\\ln \\gamma_1}{1 - x_1} = 0.72500 \\cdot x_1 + 0.00000 \\]\n<p>with coefficient of determination $R^2 = 1.000000$ and zero intercept. The experimental slope $S = 0.72500$ exactly matches the target Margules interaction parameter $A_{12} = 0.7250$ with $0.00\\%$ deviation.</p>\n\n<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>\n<p>Refractometer index uncertainty is $\\pm 0.0002$ ($u(x) = \\pm 0.0012$), temperature sensor uncertainty is $\\pm 0.01^\\circ\\text{C}$ ($u(P_1^{sat}) = \\pm 0.12\\text{ kPa}$), and pressure uncertainty is $\\pm 0.01\\text{ kPa}$. Propagating through the activity coefficient gives an overall uncertainty in $A_{12}$ of $\\pm 0.0085$, reporting $A_{12} = 0.7250 \\pm 0.0085$.</p>\n\n<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>\n<p>The positive Margules parameter ($A_{12} = 0.7250 > 0$) confirms positive deviations from Raoult's law ($\\gamma_1 > 1.0$), reflecting endothermic mixing and disruption of strong water-water hydrogen-bonding networks upon ethanol addition. At low ethanol concentrations ($x_1 = 0.10$), the activity coefficient reaches $\\gamma_1 = 2.91$, resulting in sharp vapor enrichment ($y_1 = 0.53$). As composition approaches the binary azeotrope ($x_1 \\approx 0.89$), $\\gamma_1$ asymptotically approaches $1.00$.</p>\n\n<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>\n<p>VLE models and interaction parameters are fundamental for designing industrial bioethanol dehydration columns, pressure-swing distillation trains, extractive distillation using ethylene glycol, and molecular sieve adsorption units.</p>\n\n<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>\n<p><strong>Q1: Why does ethanol-water form an azeotrope while benzene-toluene does not?</strong><br>\n<em>A1:</em> Ethanol and water have highly asymmetric polar and hydrogen-bonding forces, generating strong positive deviations from ideality that elevate vapor pressure until the VLE curves touch ($y=x$); benzene and toluene are similar nonpolar aromatics that form nearly ideal solutions.</p>\n<p><strong>Q2: How can the Redlich–Kister area test verify whether this experimental data set is thermodynamically consistent?</strong><br>\n<em>A2:</em> By plotting $\\ln(\\gamma_1 / \\gamma_2)$ against $x_1$ from 0 to 1, the integral must evaluate to zero within experimental tolerance ($\\le 2\\%$), proving consistency with the Gibbs–Duhem relation.</p>\n\n<h3>12. Concluding Summary & Verified Engineering Metric</h3>\n<p>The Othmer VLE still successfully demonstrated non-ideal vapor-liquid equilibrium for ethanol-water at $101.325\\text{ kPa}$. The experimental data confirmed modified Raoult's law and yielded the binary Margules parameter $A_{12} = 0.7250$, fully validating thermodynamic consistency.</p>"
        },
        {
                "number": 34,
                "slug": "differential-scanning-calorimetry-dsc-glass-transition",
                "title": "Differential Scanning Calorimetry (DSC) Determination of Polymer Glass Transition & Kinetic Activation",
                "shortTitle": "DSC Polymer Glass Transition",
                "aim": "Operate a heat-flux differential scanning calorimeter (DSC) across heating rates from 5.0 to 30.0 °C/min to measure the glass transition temperature (T_g) and specific heat capacity step (ΔC_p) of poly(methyl methacrylate) (PMMA), evaluate thermal relaxation kinetics, and determine the Moynihan glass transition activation slope.",
                "inputLabel": "DSC Heating Scan Rate β",
                "shortInput": "Scan Rate β",
                "inputUnit": "°C/min",
                "min": 5.0,
                "max": 30.0,
                "step": 5.0,
                "initial": 15.0,
                "inputDecimals": 1,
                "rawLabel": "Measured Glass Transition Temperature T_g",
                "rawUnit": "°C",
                "rawDecimals": 2,
                "xAxis": "Natural logarithm of scan rate ln(β)",
                "yAxis": "Glass transition temperature T_g (°C)",
                "xScale": 1.0,
                "yScale": 1.0,
                "emptyX": 2.5,
                "emptyY": 105.0,
                "targetName": "Glass Transition Thermal Shift Slope S",
                "target": "2.1500",
                "refValue": 2.15,
                "resultUnit": "°C",
                "resultDecimals": 4,
                "resultScale": 1.0,
                "fitEquation": "T_g = S · ln(β) + T_g0 = 2.1500 · ln(β) + 100.0000",
                "intro": "Differential Scanning Calorimetry (DSC) is the primary thermal analysis technique employed in chemical, materials, and process engineering to characterize thermodynamic phase transitions, crystallization kinetics, chemical crosslinking, and polymeric glass transitions. When an amorphous polymer is heated, it undergoes a reversible second-order-like kinetic transition from a rigid, glassy state to a compliant, rubbery state known as the glass transition (T_g). At the microscopic level, this transition corresponds to the onset of cooperative segmental mobility of 20 to 50 repeating polymer backbone units. Unlike first-order phase transitions (such as melting or vaporization) which exhibit latent heat and discrete discontinuities in enthalpy and volume, the glass transition exhibits an endothermic step-change in heat capacity: ΔC_p = C_p(rubbery) - C_p(glassy). Because the glass transition is an inherently kinetic phenomenon governed by structural relaxation times, the observed transition temperature T_g shifts systematically toward higher temperatures as the instrumental heating rate β (dT/dt) increases. According to Moynihan, Richardson, and Flynn–Wall–Ozawa kinetic relaxation theories, the scan-rate dependence of the glass transition temperature obeys the logarithmic relation: T_g = T_g0 + S · ln(β), where the thermal shift slope S = R · T_g^2 / ΔH* is inversely proportional to the apparent activation energy for segmental relaxation ΔH*. In this laboratory exercise, high-purity amorphous poly(methyl methacrylate) (PMMA) specimens (10.0 mg) sealed in hermetic aluminum pans are subjected to controlled heating scans from 5.0 to 30.0 °C/min under an inert nitrogen purge to determine the step change in heat capacity ΔC_p, extract the baseline glass transition temperature T_g0 = 100.00 °C, and evaluate the kinetic shift slope S = 2.1500 °C.",
                "modelExtra": "Evaluated using a TA Instruments Q2000 heat-flux DSC with refrigerated cooling system (RCS90) and purge gas flow of 50 mL/min dry N_2. Temperature and heat flow calibrated with high-purity Indium (T_m = 156.60 °C, ΔH_m = 28.57 J/g) and Sapphire specific heat standards.",
                "apparatus": [
                        {
                                "name": "Heat-Flux Differential Scanning Calorimeter (DSC)",
                                "purpose": "Measures differential heat flow between sample and reference pans across -50 to 300 °C with ±0.04 mW sensitivity."
                        },
                        {
                                "name": "Microbalance with 0.001 mg Resolution",
                                "purpose": "Determines PMMA specimen mass (10.000 ± 0.005 mg) for quantitative normalized specific heat capacity measurement."
                        },
                        {
                                "name": "Hermetic Aluminum Pan Encapsulation Press",
                                "purpose": "Crimps sample and reference pans with uniform hermetic seal to prevent volatile mass loss and ensure thermal contact."
                        },
                        {
                                "name": "Ultra-High Purity Nitrogen Gas Purge System",
                                "purpose": "Supplies dry N_2 at 50.0 mL/min to prevent oxidative degradation and moisture condensation inside the cell."
                        },
                        {
                                "name": "Refrigerated Cooling System (RCS)",
                                "purpose": "Maintains linear heating and cooling profiles down to -40 °C with rapid thermal response."
                        },
                        {
                                "name": "High-Purity Indium and Sapphire Calibration Standards",
                                "purpose": "Calibrates DSC temperature scale (Indium T_m = 156.60 °C) and heat capacity baseline (synthetic sapphire)."
                        }
                ],
                "procedure": [
                        {
                                "title": "Instrument Baseline & Temperature Calibration",
                                "text": "Run an empty pan baseline and calibrate temperature and cell constant using standard high-purity indium (156.60 °C, 28.57 J/g)."
                        },
                        {
                                "title": "Sample Preparation & Hermetic Sealing",
                                "text": "Weigh exactly 10.00 ± 0.01 mg of PMMA into an aluminum pan, crimp hermetically with lid, and place on sample sensor next to an identical empty reference pan."
                        },
                        {
                                "title": "Thermal History Erasure Scan",
                                "text": "Heat sample to 160.0 °C at 20 °C/min, hold isothermally for 5 minutes to erase prior processing stress and enthalpy relaxation, and cool at 10 °C/min to 40 °C."
                        },
                        {
                                "title": "First Heating Rate Scan (β = 5.0 °C/min)",
                                "text": "Initiate DSC heating scan from 40.0 °C to 150.0 °C at β = 5.0 °C/min under 50 mL/min N_2 purge; record heat flow signal."
                        },
                        {
                                "title": "Midpoint Glass Transition Evaluation",
                                "text": "Construct pre-transition and post-transition heat capacity baselines; determine midpoint T_g where heat capacity reaches half of the step ΔC_p."
                        },
                        {
                                "title": "Scan Rate Progression & Moynihan Regression",
                                "text": "Repeat heating scans at β = 10.0, 15.0, 20.0, 25.0, and 30.0 °C/min; plot T_g versus ln(β) to evaluate kinetic activation slope S."
                        }
                ],
                "topics": [
                        {
                                "question": "Why is the glass transition classified as a pseudo-second-order thermodynamic transition?",
                                "answer": "In Ehrenfest thermodynamics, first-order transitions exhibit discontinuities in first derivatives of Gibbs energy (entropy and volume), while second-order transitions exhibit discontinuities in second derivatives (heat capacity, thermal expansion, compressibility); because T_g exhibits a finite step in C_p without latent heat, it resembles a second-order transition, but its kinetic dependence on heating rate prevents it from being a true equilibrium transition."
                        },
                        {
                                "question": "How does free volume theory explain the glass transition phenomenon?",
                                "answer": "Free volume theory (Fox–Flory) posits that total volume consists of occupied molecular volume and unoccupied free volume; as a polymer cools, free volume contracts until reaching a critical fraction (approximately 2.5% of total volume at T_g), below which large-scale segmental backbone motion is frozen out."
                        },
                        {
                                "question": "Why must the thermal history of a polymer sample be erased before measuring T_g?",
                                "answer": "Physical aging below T_g allows polymer chains to relax slowly into lower-enthalpy conformations, producing an endothermic enthalpy recovery peak superimposed on the glass transition step; heating above T_g followed by controlled cooling erases this thermal history, restoring an unaged baseline."
                        },
                        {
                                "question": "How does polymer molecular weight affect glass transition temperature?",
                                "answer": "The Fox–Flory equation T_g = T_g(inf) - K / M_n shows that lower molecular weights possess higher concentrations of chain ends, which have greater free volume and mobility, thereby depressing T_g; above a threshold molecular weight (typically ~50,000 g/mol for PMMA), T_g plateaus at T_g(inf)."
                        },
                        {
                                "question": "What is the difference between midpoint T_g, onset T_g, and inflection T_g?",
                                "answer": "Onset T_g is the intersection of the pre-transition baseline with the tangent at maximum slope; inflection T_g is the peak of the derivative heat flow curve; midpoint T_g is the temperature at which the heat flow reaches half the total heat capacity step ΔC_p, providing the most reproducible metric."
                        },
                        {
                                "question": "How does plasticizer addition alter polymer glass transition temperature?",
                                "answer": "Plasticizers are low-molecular-weight compatible diluents that embed between polymer chains, shielding intermolecular polar forces and introducing substantial free volume, which dramatically lowers T_g (described by the Gordon–Taylor equation) to improve flexibility."
                        }
                ],
                "precautions": [
                        "Ensure the aluminum sample pan is crimped hermetically without pinholes to prevent volatilization of residual monomer or moisture during heating.",
                        "Verify steady nitrogen purge gas flow at 50 mL/min to prevent atmospheric oxygen oxidation of PMMA at elevated temperatures.",
                        "Always include an identical empty aluminum pan in the reference cell position to balance instrument baseline heat capacity.",
                        "Perform a thermal history erasure cycle above 150 °C prior to data collection to eliminate physical aging enthalpy relaxation peaks."
                ],
                "quiz": [
                        {
                                "question": "During a DSC heating scan of an amorphous polymer, the glass transition appears as:",
                                "options": [
                                        "A sharp exothermic peak",
                                        "A sharp endothermic peak",
                                        "An endothermic baseline step change in heat capacity",
                                        "A flat baseline with zero heat flow change"
                                ],
                                "correct": 2,
                                "explanation": "The glass transition involves no latent heat of phase change, appearing as an endothermic step increase in specific heat capacity ΔC_p."
                        },
                        {
                                "question": "As the DSC heating scan rate β is increased from 5 to 30 °C/min, the measured glass transition temperature T_g:",
                                "options": [
                                        "Decreases linearly",
                                        "Remains strictly constant",
                                        "Shifts toward higher temperatures",
                                        "Vanishes completely"
                                ],
                                "correct": 2,
                                "explanation": "Because molecular relaxation requires finite time, faster heating rates give polymer segments less time to relax, shifting the observed transition to higher temperatures."
                        },
                        {
                                "question": "The step change in specific heat capacity at the glass transition ΔC_p is defined as:",
                                "options": [
                                        "C_p(rubbery) - C_p(glassy)",
                                        "C_p(glassy) - C_p(rubbery)",
                                        "ΔH_melting / T_g",
                                        "C_p(liquid) + C_p(vapor)"
                                ],
                                "correct": 0,
                                "explanation": "Rubbery polymers have additional vibrational and conformational degrees of freedom, meaning C_p(rubbery) > C_p(glassy), yielding a positive step ΔC_p = C_p(rubbery) - C_p(glassy)."
                        },
                        {
                                "question": "Which equation relates polymer glass transition temperature to number-average molecular weight?",
                                "options": [
                                        "Arrhenius equation",
                                        "Fox–Flory equation",
                                        "Ergun equation",
                                        "Fanning friction equation"
                                ],
                                "correct": 1,
                                "explanation": "The Fox–Flory equation T_g = T_g(inf) - K / M_n models the dependence of glass transition on polymer chain molecular weight."
                        }
                ],
                "samples": [
                        5.0,
                        10.0,
                        15.0,
                        20.0,
                        25.0,
                        30.0
                ],
                "measureLabel": "Record DSC glass transition temperature",
                "readings": [
                        "beta",
                        "ln_beta",
                        "tg_celsius",
                        "delta_cp",
                        "heat_flow_step",
                        "activation_metric"
                ],
                "theory": "<h3>Polymer Viscoelasticity & Molecular Origin of the Glass Transition</h3>\n<p>In amorphous and semi-crystalline polymers, the glass transition temperature ($T_g$) marks the fundamental kinetic boundary between brittle glassy behavior and ductile rubbery behavior. In the glassy state ($T < T_g$), polymer macromolecules are kinetically trapped in non-equilibrium disordered conformations. Chain segments cannot translate; thermal energy is stored exclusively in localized bond stretching, valence angle bending, and restricted side-group librations. As temperature rises to $T_g$, the thermal energy $k_B T$ becomes comparable to the rotational energy barriers governing main-chain torsional angles. Cooperative coordinated rotations of 20 to 50 skeletal backbone bonds (crankshaft motions) become activated, creating macroscopic flexibility, structural relaxation, and a sudden step increase in heat capacity $\\Delta C_p$:</p>\n\\[ \\Delta C_p = C_{p,\\text{rubbery}} - C_{p,\\text{glassy}} = \\left( \\frac{\\partial H}{\\partial T} \\right)_{P,\\text{rubbery}} - \\left( \\frac{\\partial H}{\\partial T} \\right)_{P,\\text{glassy}} \\]\n\n<h3>Differential Scanning Calorimetry Heat Flow Principle</h3>\n<p>In a heat-flux DSC cell, the specimen (mass $m_s$) and an empty reference crucible are mounted on identical thermoelectric sensor platforms surrounded by a heated furnace. The differential heat flow rate $d Q / d t$ is measured via the differential thermoelectric voltage:</p>\n\\[ \\frac{d Q}{d t} = -\\frac{\\Delta T_{\\text{sensor}}}{R_{\\text{sensor}}} = m_s \\, c_p \\, \\frac{d T}{d t} + f(T, t) \\]\n<p>where $\\beta = d T / d t$ is the programmed constant heating scan rate. Under steady heating, baseline heat flow is directly proportional to sample heat capacity: $q = m_s \\, c_p \\, \\beta$. At the glass transition, heat flow shifts downward by $\\Delta q = m_s \\, \\Delta c_p \\, \\beta$.</p>\n\n<h3>Kinetic Shift & Moynihan Activation Formalism</h3>\n<p>Because structural relaxation is governed by a characteristic relaxation time $\\tau(T)$ that follows the Vogel–Fulcher–Tammann (VFT) or Williams–Landel–Ferry (WLF) equation, shifting the instrumental heating rate $\\beta$ alters the observational Deborah number ($De = \\tau / t_{\\text{obs}}$). Faster scan rates force the transition to occur at shorter observation timescales, requiring higher thermal energy and elevating $T_g$. According to Moynihan and Richardson thermal activation theory:</p>\n\\[ \\frac{d \\ln \\beta}{d (1 / T_g)} = -\\frac{\\Delta H^*}{R} \\]\n<p>For small temperature intervals $\\Delta T_g \\ll T_g$, expanding in a first-order Taylor series around baseline heating rate produces the linear logarithmic scaling relation:</p>\n\\[ T_g = T_{g0} + S \\cdot \\ln(\\beta) \\]\n<p>where $S = \\frac{R \\, T_g^2}{\\Delta H^*} = 2.1500^\\circ\\text{C}$ is the glass transition thermal shift slope and $T_{g0} = 100.00^\\circ\\text{C}$ is the extrapolated datum at $\\beta = 1.0^\\circ\\text{C/min}$.</p>",
                "report": "<h3>1. Objective & Practical Significance</h3>\n<p>This laboratory investigation determines the glass transition temperature ($T_g$) and heat capacity step change ($\\Delta C_p$) of amorphous poly(methyl methacrylate) (PMMA) using heat-flux Differential Scanning Calorimetry (DSC). Across heating scan rates $\\beta$ from $5.0$ to $30.0^\\circ\\text{C/min}$, we evaluate structural relaxation kinetics, verify the Moynihan logarithmic scaling relationship $T_g = S \\cdot \\ln(\\beta) + T_{g0}$, determine the thermal shift slope $S = 2.1500^\\circ\\text{C}$, evaluate baseline $T_{g0} = 100.0000^\\circ\\text{C}$, and extract the apparent activation energy for cooperative segmental backbone mobility.</p>\n\n<h3>2. Governing Transport Equations & Phenomenological Relations</h3>\n<p>Differential heat flow is related to heat capacity by: $\\frac{dQ}{dt} = m_s \\, c_p \\, \\beta$. The glass transition thermal shift obeys:</p>\n\\[ T_g = S \\cdot \\ln(\\beta) + T_{g0} = 2.1500 \\cdot \\ln(\\beta) + 100.0000 \\]\n<p>where $S = \\frac{R T_g^2}{\\Delta H^*} = 2.1500^\\circ\\text{C}$ and $T_{g0} = 100.0000^\\circ\\text{C}$. The segmental relaxation activation energy is calculated as: $\\Delta H^* = \\frac{R T_g^2}{S}$.</p>\n\n<h3>3. Experimental Apparatus & Instrumentation Specification</h3>\n<p>Testing was performed on a TA Instruments Q2000 heat-flux DSC equipped with a refrigerated cooling system (RCS90) and purge gas flow of $50.0\\text{ mL/min}$ dry nitrogen. PMMA specimens ($10.000 \\pm 0.005\\text{ mg}$) were weighed on a Mettler Toledo microbalance ($\\pm 0.001\\text{ mg}$) and sealed in hermetic aluminum crucibles. Temperature scale was calibrated using high-purity Indium ($T_m = 156.60^\\circ\\text{C}$, $\\Delta H_m = 28.57\\text{ J/g}$).</p>\n\n<h3>4. Standard Operating Procedure & Measurement Protocols</h3>\n<p>A $10.00\\text{ mg}$ PMMA specimen was sealed in an aluminum pan. To erase thermal history and eliminate physical aging enthalpy recovery endotherms, the sample was heated to $160.0^\\circ\\text{C}$ at $20^\\circ\\text{C/min}$, held for 5 minutes, and cooled at $10^\\circ\\text{C/min}$ to $40.0^\\circ\\text{C}$. Controlled heating scans were then executed from $40.0$ to $150.0^\\circ\\text{C}$ at $\\beta = 5.0, 10.0, 15.0, 20.0, 25.0,$ and $30.0^\\circ\\text{C/min}$. Midpoint $T_g$ was determined using ASTM E1356 half-step height analysis.</p>\n\n<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>\n<p>Aluminum pans were inspected for hermetic seals to prevent outgassing. The nitrogen purge prevented thermo-oxidative degradation. Safety glasses and insulated heat-resistant tweezers were used when handling pans.</p>\n\n<h3>6. Raw Experimental Observations & Systematic Data Records</h3>\n<p><strong>Simulated demonstration data.</strong> The following calorimetric measurements were recorded for PMMA ($m_s = 10.00\\text{ mg}$, $N_2 = 50\\text{ mL/min}$):</p>\n<table>\n<thead>\n<tr><th>Run</th><th>Scan Rate $\\beta$ (°C/min)</th><th>Logarithm $\\ln(\\beta)$</th><th>Measured $T_g$ (°C)</th><th>Step $\\Delta q$ (mW)</th><th>Specific $\\Delta C_p$ (J/(g·K))</th><th>Fitted $T_g$ (°C)</th></tr>\n</thead>\n<tbody>\n<tr><td>1</td><td>5.0</td><td>1.6094</td><td>103.460</td><td>0.258</td><td>0.310</td><td>103.460</td></tr>\n<tr><td>2</td><td>10.0</td><td>2.3026</td><td>104.951</td><td>0.517</td><td>0.310</td><td>104.951</td></tr>\n<tr><td>3</td><td>15.0</td><td>2.7081</td><td>105.822</td><td>0.775</td><td>0.310</td><td>105.822</td></tr>\n<tr><td>4</td><td>20.0</td><td>2.9957</td><td>106.441</td><td>1.033</td><td>0.310</td><td>106.441</td></tr>\n<tr><td>5</td><td>25.0</td><td>3.2189</td><td>106.921</td><td>1.292</td><td>0.310</td><td>106.921</td></tr>\n<tr><td>6</td><td>30.0</td><td>3.4012</td><td>107.313</td><td>1.550</td><td>0.310</td><td>107.313</td></tr>\n</tbody>\n</table>\n\n<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>\n<p>Linear regression of glass transition temperature $T_g$ versus $\\ln(\\beta)$ yields:</p>\n\\[ T_g = 2.15000 \\cdot \\ln(\\beta) + 100.00000 \\]\n<p>with coefficient of determination $R^2 = 1.000000$. The experimental slope $S = 2.15000^\\circ\\text{C}$ and baseline intercept $T_{g0} = 100.00000^\\circ\\text{C}$ match calibration targets ($2.1500$ and $100.0000$) with $0.00\\%$ deviation. Evaluating the apparent activation energy for segmental backbone motion ($T_g = 105.82^\\circ\\text{C} = 378.97\\text{ K}$):</p>\n\\[ \\Delta H^* = \\frac{R T_g^2}{S} = \\frac{8.314 \\cdot (378.97)^2}{2.1500} = 555.2\\text{ kJ/mol} \\]\n\n<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>\n<p>Indium temperature calibration uncertainty is $\\pm 0.05^\\circ\\text{C}$, scan rate precision is $\\pm 0.02^\\circ\\text{C/min}$, and balance uncertainty is $\\pm 0.005\\text{ mg}$. Propagating into the regression slope yields an experimental uncertainty in $S$ of $\\pm 0.025^\\circ\\text{C}$ ($1.16\\%$), reporting $S = 2.150 \\pm 0.025^\\circ\\text{C}$ and $\\Delta H^* = 555 \\pm 12\\text{ kJ/mol}$.</p>\n\n<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>\n<p>The observed increase in $T_g$ from $103.46^\\circ\\text{C}$ to $107.31^\\circ\\text{C}$ across the 6-fold increase in heating rate confirms the kinetic nature of the glass transition. At high scan rates, structural relaxation cannot keep pace with heating, shifting the apparent transition higher. The measured activation energy of $555\\text{ kJ/mol}$ reflects high cooperative barriers associated with bulky methyl and ester side groups on the PMMA backbone.</p>\n\n<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>\n<p>DSC kinetic parameters govern polymer injection molding cooling cycles, blow molding parison inflation windows, thermal stability of packaging films, and curing schedules for aerospace epoxy-carbon fiber composites.</p>\n\n<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>\n<p><strong>Q1: Why is an enthalpy relaxation endotherm observed in physically aged polymers?</strong><br>\n<em>A1:</em> Storage below $T_g$ allows polymer chains to slowly densify toward equilibrium; upon reheating through $T_g$, the recovered enthalpy produces an endothermic peak on top of the heat capacity step.</p>\n<p><strong>Q2: How does the addition of dioctyl phthalate (DOP) plasticizer shift $T_g$?</strong><br>\n<em>A2:</em> Plasticizers increase free volume and space polymer chains apart, lowering intermolecular friction and depressing $T_g$ toward ambient temperatures.</p>\n\n<h3>12. Concluding Summary & Verified Engineering Metric</h3>\n<p>Heat-flux DSC successfully characterized PMMA glass transition kinetics across $\\beta = 5.0$ to $30.0^\\circ\\text{C/min}$. The experimental thermal shift slope $S = 2.1500^\\circ\\text{C}$ and baseline $T_{g0} = 100.00^\\circ\\text{C}$ established an apparent segmental activation energy of $\\Delta H^* = 555.2\\text{ kJ/mol}$.</p>"
        },
        {
                "number": 35,
                "slug": "bomb-calorimeter-heat-of-combustion-hydrocarbons",
                "title": "Oxygen Bomb Calorimetry & Standard Heat of Combustion of Organic Process Hydrocarbons",
                "shortTitle": "Oxygen Bomb Calorimetry",
                "aim": "Operate an isoperibol oxygen bomb calorimeter pressurized to 3.0 MPa with pure O_2, measure the corrected adiabatic temperature rise ΔT_c resulting from complete combustion of standardized benzoic acid and liquid process hydrocarbon pellets (0.40 to 1.40 g), calibrate the effective calorimeter energy equivalent W_cal, and evaluate the specific combustion thermometric slope.",
                "inputLabel": "Combustion Sample Mass m_s",
                "shortInput": "Sample Mass m_s",
                "inputUnit": "g",
                "min": 0.4,
                "max": 1.4,
                "step": 0.2,
                "initial": 0.8,
                "inputDecimals": 2,
                "rawLabel": "Corrected Calorimeter Temperature Rise ΔT_c",
                "rawUnit": "°C",
                "rawDecimals": 4,
                "xAxis": "Sample pellet mass m_s (g)",
                "yAxis": "Corrected temperature rise ΔT_c (°C)",
                "xScale": 1.0,
                "yScale": 1.0,
                "emptyX": 0.9,
                "emptyY": 2.3,
                "targetName": "Specific Combustion Thermometric Slope S",
                "target": "2.6500",
                "refValue": 2.65,
                "resultUnit": "°C/g",
                "resultDecimals": 4,
                "resultScale": 1.0,
                "fitEquation": "ΔT_c = S · m_s = 2.6500 · m_s",
                "intro": "Oxygen bomb calorimetry is the gold standard thermochemical method in chemical, petroleum, and energy engineering for determining standard gross heats of combustion (higher heating values, HHV), internal energies of reaction (ΔU_c^°), and standard enthalpies of formation (ΔH_f^°) of fuels, polymers, foodstocks, and chemical feedstocks. In an isoperibol oxygen bomb calorimeter, a known mass of combustible sample is ignited electrically inside a thick-walled, high-strength stainless steel pressure vessel (bomb) charged with excess pure oxygen gas at 3.0 MPa (30 bar). Complete combustion transforms organic carbon, hydrogen, and oxygen exclusively into gaseous CO_2 and condensed liquid H_2O: C_a H_b O_c (s) + (a + b/4 - c/2) O_2 (g) -> a CO_2 (g) + (b/2) H_2O (l). The bomb is submerged in a precisely weighed bucket of deionized water (2000.0 g) enclosed within a thermostatically jacketed isoperibol air space. Heat released by combustion transfers through the bomb walls into the surrounding water and calorimeter hardware, inducing a temperature rise of 1 to 4 °C. Because the calorimeter is not perfectly adiabatic, heat exchange with the constant-temperature jacket occurs during the rating periods. The Regnault–Pfaundler radiation correction method accounts for this thermal leakage, yielding the corrected temperature rise ΔT_c. Applying the first law of thermodynamics to the closed constant-volume bomb system yields: -ΔU_c = W_cal · ΔT_c - e_fuse - e_acid, where W_cal is the energy equivalent (effective heat capacity) of the calorimeter system, e_fuse is the combustion energy of the nickel-chromium ignition wire, and e_acid is the thermochemical correction for nitric acid formed from residual nitrogen. Standardized benzoic acid pellets (certified gross heat of combustion -Δu_c = 26.434 kJ/g) are combusted across masses from 0.40 to 1.40 g to determine the specific combustion thermometric slope S = (-Δu_c) / W_cal = 2.6500 °C/g, validating the calorimeter energy equivalent W_cal = 9.975 kJ/°C (9975 J/K).",
                "modelExtra": "Evaluated using a Parr 6200 isoperibol oxygen bomb calorimeter with Parr 1108 high-strength stainless steel bomb and precision digital thermistor thermometer (±0.0001 °C resolution). Standardized against NIST SRM 39j benzoic acid (-Δu_c = 26.434 ± 0.003 kJ/g).",
                "apparatus": [
                        {
                                "name": "Parr 1108 High-Strength Oxygen Combustion Bomb",
                                "purpose": "342 mL stainless steel pressure vessel rated to 20 MPa operating at 3.0 MPa pure O_2 for complete sample combustion."
                        },
                        {
                                "name": "Thermostatically Controlled Isoperibol Water Jacket",
                                "purpose": "Maintains jacket temperature constant at 25.000 ± 0.005 °C to establish stable radiative boundary conditions."
                        },
                        {
                                "name": "Precision Electronic Thermistor Thermometer",
                                "purpose": "Measures calorimeter bucket water temperature with 0.0001 °C resolution and zero thermal drift."
                        },
                        {
                                "name": "High-Pressure Oxygen Charging Regulator & Manifold",
                                "purpose": "Safely charges bomb with ultra-pure O_2 (99.99%) to exactly 3.00 ± 0.05 MPa without disturbing sample powder."
                        },
                        {
                                "name": "Electronic Capacitive Ignition Unit",
                                "purpose": "Delivers a 10 cm loop of Ni-Cr fuse wire exactly 23 J of electrical energy to initiate combustion."
                        },
                        {
                                "name": "Pellet Press & Analytical Microbalance",
                                "purpose": "Compacts powder samples into cohesive pellets weighed to 0.0001 g to prevent splattering during deflagration."
                        }
                ],
                "procedure": [
                        {
                                "title": "Calorimeter Jacket Thermal Stabilization",
                                "text": "Turn on the isoperibol jacket circulating bath at 25.00 °C; verify temperature stability within ±0.005 °C for 30 minutes."
                        },
                        {
                                "title": "Pellet Preparation & Fuse Attachment",
                                "text": "Compress benzoic acid into a cohesive pellet (0.4000 g); mount in the fuel capsule and connect 10 cm of Ni-Cr fuse wire touching the pellet top."
                        },
                        {
                                "title": "Deionized Water Charge & Bomb Sealing",
                                "text": "Add 1.0 mL of DI water to the bomb cylinder base to absorb nitric acid; assemble screw cap with sealing ring hand-tight."
                        },
                        {
                                "title": "Oxygen Purge & Pressurization",
                                "text": "Connect charging manifold; purge residual air for 15 s, then pressurize slowly to 3.00 MPa O_2; submerge in water bath to verify leak-tightness."
                        },
                        {
                                "title": "Bucket Installation & Pre-Period Logging",
                                "text": "Place bomb in calorimeter bucket containing exactly 2000.0 g DI water; start stirrer motor and record pre-period temperatures for 5 minutes."
                        },
                        {
                                "title": "Ignition, Post-Period & Regnault–Pfaundler Correction",
                                "text": "Fire electronic ignition; record temperature rise through reaction period and post-period; compute Regnault–Pfaundler ΔT_c and repeat for masses up to 1.40 g."
                        }
                ],
                "topics": [
                        {
                                "question": "Why is 1.0 mL of deionized water added to the bomb cylinder before sealing?",
                                "answer": "The water saturates the interior vapor space, ensuring all water produced by combustion condenses completely into the liquid phase (releasing latent heat of vaporization) and provides an aqueous medium to dissolve and neutralize any nitric acid formed from trace nitrogen."
                        },
                        {
                                "question": "What is the difference between gross heat of combustion (HHV) and net heat of combustion (LHV)?",
                                "answer": "Gross heat of combustion (higher heating value, HHV) includes the latent heat of condensation of water formed during combustion because product water ends as liquid; net heat of combustion (lower heating value, LHV) assumes all product water remains in the vapor phase, subtracting the enthalpy of vaporization (2.442 MJ/kg H2O)."
                        },
                        {
                                "question": "How does the Regnault–Pfaundler correction account for non-adiabatic calorimeter heat leakage?",
                                "answer": "The method integrates Newton's law of cooling across the reaction period using the measured cooling constants from the initial steady pre-period and final post-period, adding a calculated radiation correction ΔT_rad to the raw temperature rise ΔT_raw to yield the true adiabatic ΔT_c."
                        },
                        {
                                "question": "Why must the sample be compacted into a cohesive pellet rather than burned as a loose powder?",
                                "answer": "Loose fine powders tend to be blown out of the combustion crucible by the rapid rush of pressurized oxygen during charging or by the sudden expansion wave upon ignition, leading to incomplete combustion and unburned carbon soot."
                        },
                        {
                                "question": "How is the constant-volume internal energy of combustion ΔU_c converted to constant-pressure enthalpy of combustion ΔH_c?",
                                "answer": "Using the thermodynamic identity ΔH_c = ΔU_c + Δn_g · R T, where Δn_g = n_g(products) - n_g(reactants) is the net change in moles of gaseous species (moles of CO2 produced minus moles of O2 consumed)."
                        },
                        {
                                "question": "Why must pure oxygen be charged to a high pressure of 3.0 MPa (30 bar)?",
                                "answer": "High oxygen pressure ensures a vast stoichiometric excess of O2 (typically 10 to 20 times the stoichiometric requirement), guaranteeing 100% complete combustion to CO2 and H2O without carbon monoxide (CO) or soot formation."
                        }
                ],
                "precautions": [
                        "Never exceed 3.5 MPa oxygen charging pressure, and inspect bomb head threads and sealing O-rings before every pressurization.",
                        "Ensure the bomb is completely submerged in water to test for escaping gas bubbles before placing inside the calorimeter jacket.",
                        "Do not lean over the calorimeter during ignition; maintain electrical firing switch outside the protective blast zone.",
                        "Verify that ignition fuse wire does not touch the stainless steel capsule walls to prevent electrical short-circuiting."
                ],
                "quiz": [
                        {
                                "question": "In bomb calorimetry, the measured combustion reaction occurs under which thermodynamic condition?",
                                "options": [
                                        "Constant pressure and enthalpy",
                                        "Constant volume and internal energy",
                                        "Constant temperature and entropy",
                                        "Constant chemical potential"
                                ],
                                "correct": 1,
                                "explanation": "The rigid stainless steel bomb maintains a strictly constant volume (ΔV = 0), so work done is zero (w = 0) and heat measured equals the change in internal energy (-q_v = ΔU_c)."
                        },
                        {
                                "question": "The certified specific heat of combustion of standard NIST benzoic acid is approximately:",
                                "options": [
                                        "-15.350 kJ/g",
                                        "-26.434 kJ/g",
                                        "-35.820 kJ/g",
                                        "-44.200 kJ/g"
                                ],
                                "correct": 1,
                                "explanation": "NIST SRM 39j benzoic acid has a certified gross heat of combustion of -26.434 kJ/g (-3226.7 kJ/mol)."
                        },
                        {
                                "question": "The Regnault–Pfaundler radiation correction is applied to:",
                                "options": [
                                        "Compensate for incomplete combustion",
                                        "Account for convective and radiative heat leakage with the calorimeter jacket",
                                        "Correct for barometric pressure variations",
                                        "Calculate ignition wire resistance"
                                ],
                                "correct": 1,
                                "explanation": "The Regnault–Pfaundler correction integrates heat transfer between the calorimeter bucket and isoperibol jacket to compute the true adiabatic temperature rise."
                        },
                        {
                                "question": "The relationship between ΔH_c and ΔU_c for an organic fuel combustion reaction is:",
                                "options": [
                                        "ΔH_c = ΔU_c + Δn_g · R T",
                                        "ΔH_c = ΔU_c - Δn_g · R T",
                                        "ΔH_c = ΔU_c / (R T)",
                                        "ΔH_c = ΔU_c · (P / V)"
                                ],
                                "correct": 0,
                                "explanation": "From the definition of enthalpy H = U + P V, for ideal gases Δ(P V) = Δn_g · R T, yielding ΔH_c = ΔU_c + Δn_g · R T."
                        }
                ],
                "samples": [
                        0.4,
                        0.6,
                        0.8,
                        1.0,
                        1.2,
                        1.4
                ],
                "measureLabel": "Record corrected adiabatic temperature rise",
                "readings": [
                        "mass",
                        "raw_dt",
                        "rad_corr",
                        "dt_corrected",
                        "energy_released",
                        "combustion_hhv"
                ],
                "theory": "<h3>First Law of Thermodynamics & Constant-Volume Bomb Calorimetry</h3>\n<p>Bomb calorimetry measures the internal energy of combustion ($\\Delta U_c$) of chemical substances under constant-volume conditions. Applying the First Law of Thermodynamics to the closed, rigid calorimeter bomb system ($d V = 0$):</p>\n\\[ d U = \\delta Q - \\delta W = \\delta Q - P \\, d V = \\delta Q_V \\]\n<p>Because the bomb boundaries are rigid, expansion work is zero ($W = 0$). The total heat released by the combustion reaction ($Q_{\\text{comb}}$) equals the internal energy change of the reacting system:</p>\n\\[ -\\Delta U_c = Q_{\\text{comb}} = W_{\\text{cal}} \\, \\Delta T_c - e_{\\text{fuse}} - e_{\\text{acid}} \\]\n<p>where $W_{\\text{cal}}$ is the effective energy equivalent (heat capacity) of the calorimeter system (bomb, bucket, water, stirrer, and thermometer), $\\Delta T_c$ is the corrected temperature rise, $e_{\\text{fuse}}$ is the combustion energy of the nickel-chromium ignition wire ($e_{\\text{fuse}} = 9.6\\text{ J/cm} \\times L_{\\text{burned}}$), and $e_{\\text{acid}}$ is the thermochemical correction for nitric and sulfuric acid formation.</p>\n\n<h3>Regnault–Pfaundler Radiation Correction Method</h3>\n<p>In an isoperibol calorimeter, the jacket is maintained at constant temperature $T_j$. During the combustion process, heat exchanges with the jacket according to Newton's law of cooling:</p>\n\\[ \\frac{d T}{d t} = -k \\, (T - T_j) + w_{\\text{stir}} \\]\n<p>where $k$ is the calorimeter cooling constant and $w_{\\text{stir}}$ is the thermal dissipation from mechanical stirring. The Regnault–Pfaundler method evaluates the radiation leakage correction $\\Delta T_{\\text{rad}}$ across the reaction period from $t_a$ (ignition) to $t_b$ (start of steady post-period cooling):</p>\n\\[ \\Delta T_{\\text{rad}} = k \\, \\int_{t_a}^{t_b} (T(t) - T_{\\infty}) \\, d t \\]\n\\[ \\Delta T_c = T_b - T_a + \\Delta T_{\\text{rad}} \\]\n\n<h3>Linear Thermometric Scaling & Standard Heat of Combustion</h3>\n<p>For a standardized pure substance (such as benzoic acid, certified specific heat of combustion $-\\Delta u_c = 26.434\\text{ kJ/g}$), the corrected temperature rise scales directly with sample mass $m_s$:</p>\n\\[ \\Delta T_c = S \\cdot m_s = \\left( \\frac{-\\Delta u_c}{W_{\\text{cal}}} \\right) \\cdot m_s \\]\n<p>Linear regression of $\\Delta T_c$ versus $m_s$ extracts the thermometric slope $S = 2.6500^\\circ\\text{C/g}$, from which the calorimeter energy equivalent is determined:</p>\n\\[ W_{\\text{cal}} = \\frac{-\\Delta u_c}{S} = \\frac{26.434\\text{ kJ/g}}{2.6500^\\circ\\text{C/g}} = 9.9751\\text{ kJ/}^\\circ\\text{C} = 9975.1\\text{ J/K} \\]\n<p>The standard enthalpy of combustion $\\Delta H_c^\\circ$ at $298.15\\text{ K}$ is related to $\\Delta U_c^\\circ$ through the gas stoichiometric mole change $\\Delta n_g$:</p>\n\\[ \\Delta H_c^\\circ = \\Delta U_c^\\circ + \\Delta n_g \\, R T \\]",
                "report": "<h3>1. Objective & Practical Significance</h3>\n<p>This laboratory investigation determines the energy equivalent ($W_{\\text{cal}}$) and combustion thermochemistry of standardized benzoic acid pellets ($m_s = 0.40$ to $1.40\\text{ g}$) using an isoperibol oxygen bomb calorimeter pressurized to $3.0\\text{ MPa}$ with pure oxygen. By monitoring pre-period, reaction, and post-period temperatures with a $0.0001^\\circ\\text{C}$ resolution thermistor and applying the Regnault–Pfaundler radiation correction, we evaluate the corrected adiabatic temperature rise $\\Delta T_c$, verify linear thermometric scaling $\\Delta T_c = S \\cdot m_s$, determine slope $S = 2.6500^\\circ\\text{C/g}$, and calculate calorimeter heat capacity $W_{\\text{cal}} = 9.9751\\text{ kJ/K}$.</p>\n\n<h3>2. Governing Transport Equations & Phenomenological Relations</h3>\n<p>First-law energy conservation over the constant-volume bomb gives: $-\\Delta U_c = W_{\\text{cal}} \\, \\Delta T_c - e_{\\text{fuse}} - e_{\\text{acid}}$. The thermometric scaling relationship is:</p>\n\\[ \\Delta T_c = S \\cdot m_s = 2.6500 \\cdot m_s \\]\n<p>where $S = \\frac{-\\Delta u_c}{W_{\\text{cal}}} = 2.6500^\\circ\\text{C/g}$. Calorimeter heat capacity is $W_{\\text{cal}} = \\frac{-\\Delta u_c}{S} = \\frac{26.434}{2.6500} = 9.9751\\text{ kJ/K}$.</p>\n\n<h3>3. Experimental Apparatus & Instrumentation Specification</h3>\n<p>The system comprises a Parr 1108 high-strength stainless steel oxygen combustion bomb ($342\\text{ mL}$ volume, $20\\text{ MPa}$ rating), an isoperibol water jacket held at $25.000 \\pm 0.005^\\circ\\text{C}$, an oval water bucket containing $2000.0 \\pm 0.1\\text{ g}$ deionized water, an electronic thermistor thermometer ($0.0001^\\circ\\text{C}$ resolution), an electronic capacitive ignition unit, and a high-precision analytical balance ($\\pm 0.0001\\text{ g}$).</p>\n\n<h3>4. Standard Operating Procedure & Measurement Protocols</h3>\n<p>Standardized benzoic acid (NIST SRM 39j, $-\\Delta u_c = 26.434\\text{ kJ/g}$) was compacted into pellets. A $10\\text{ cm}$ Ni-Cr fuse wire was attached. The bomb was charged with $1.0\\text{ mL}$ DI water, sealed, purged, and pressurized to $3.00\\text{ MPa}$ with pure oxygen. After leak testing, the bomb was immersed in the $2000.0\\text{ g}$ water bucket inside the isoperibol jacket. Stirring was initiated, pre-period temperatures logged for 5 minutes, fuse ignited, and temperatures tracked until post-period steady cooling was established. Pellets of mass $0.40, 0.60, 0.80, 1.00, 1.20,$ and $1.40\\text{ g}$ were tested.</p>\n\n<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>\n<p>Pressurized oxygen at $3.0\\text{ MPa}$ presents extreme combustion hazards. Oils, greases, and hydrocarbons were strictly excluded from bomb threads and charging manifolds. Bomb closure threads were inspected before every test. Firing was conducted behind a polycarbonate safety shield.</p>\n\n<h3>6. Raw Experimental Observations & Systematic Data Records</h3>\n<p><strong>Simulated demonstration data.</strong> The following bomb calorimetric measurements were recorded at $P_{O2} = 3.0\\text{ MPa}$ ($T_j = 25.000^\\circ\\text{C}$, $m_w = 2000.0\\text{ g}$):</p>\n<table>\n<thead>\n<tr><th>Run</th><th>Sample Mass $m_s$ (g)</th><th>Raw $\\Delta T_{\\text{raw}}$ (°C)</th><th>Regnault Correction $\\Delta T_{\\text{rad}}$ (°C)</th><th>Corrected $\\Delta T_c$ (°C)</th><th>Energy Released $Q_c$ (kJ)</th><th>Effective Heat Capacity $W_{\\text{cal}}$ (kJ/°C)</th></tr>\n</thead>\n<tbody>\n<tr><td>1</td><td>0.40</td><td>1.0425</td><td>+0.0175</td><td>1.0600</td><td>10.574</td><td>9.975</td></tr>\n<tr><td>2</td><td>0.60</td><td>1.5642</td><td>+0.0258</td><td>1.5900</td><td>15.860</td><td>9.975</td></tr>\n<tr><td>3</td><td>0.80</td><td>2.0860</td><td>+0.0340</td><td>2.1200</td><td>21.147</td><td>9.975</td></tr>\n<tr><td>4</td><td>1.00</td><td>2.6078</td><td>+0.0422</td><td>2.6500</td><td>26.434</td><td>9.975</td></tr>\n<tr><td>5</td><td>1.20</td><td>3.1295</td><td>+0.0505</td><td>3.1800</td><td>31.721</td><td>9.975</td></tr>\n<tr><td>6</td><td>1.40</td><td>3.6512</td><td>+0.0588</td><td>3.7100</td><td>37.008</td><td>9.975</td></tr>\n</tbody>\n</table>\n\n<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>\n<p>Linear regression of corrected temperature rise $\\Delta T_c$ versus sample mass $m_s$ yields:</p>\n\\[ \\Delta T_c = 2.65000 \\cdot m_s + 0.00000 \\]\n<p>with coefficient of determination $R^2 = 1.000000$ and zero intercept. The experimental slope $S = 2.65000^\\circ\\text{C/g}$ matches the calibration target ($2.6500$) with $0.00\\%$ deviation. Evaluating the calorimeter energy equivalent:</p>\n\\[ W_{\\text{cal}} = \\frac{-\\Delta u_c}{S} = \\frac{26.434\\text{ kJ/g}}{2.65000^\\circ\\text{C/g}} = 9.9751\\text{ kJ/}^\\circ\\text{C} = 9975.1\\text{ J/K} \\]\n<p>Converting to standard molar enthalpy of combustion for benzoic acid ($C_7H_6O_2$, $M = 122.12\\text{ g/mol}$, $\\Delta n_g = -0.5\\text{ mol}$):</p>\n\\[ \\Delta U_c^\\circ = -26.434 \\times 122.12 = -3228.12\\text{ kJ/mol} \\]\n\\[ \\Delta H_c^\\circ = \\Delta U_c^\\circ + \\Delta n_g R T = -3228.12 + (-0.5)(0.008314)(298.15) = -3229.36\\text{ kJ/mol} \\]\n\n<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>\n<p>Analytical balance uncertainty is $\\pm 0.0001\\text{ g}$, thermistor accuracy is $\\pm 0.0001^\\circ\\text{C}$, and water mass uncertainty is $\\pm 0.1\\text{ g}$. Propagating into $W_{\\text{cal}}$ yields an uncertainty of $\\pm 8.2\\text{ J/K}$ ($0.082\\%$), reporting $W_{\\text{cal}} = 9975 \\pm 8\\text{ J/K}$.</p>\n\n<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>\n<p>The perfect linearity confirms constant heat capacity over the $1.0$ to $3.7^\\circ\\text{C}$ temperature rise window. Regnault–Pfaundler radiation corrections scaled smoothly from $+0.0175^\\circ\\text{C}$ to $+0.0588^\\circ\\text{C}$, reflecting slightly longer reaction periods for larger sample pellets.</p>\n\n<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>\n<p>Bomb calorimetry data establish fuel heating values (ASTM D240, ASTM D4809) for petroleum refining, gas turbine combustion efficiency, biomass power plant boiler design, and thermodynamic process simulation in Aspen Plus.</p>\n\n<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>\n<p><strong>Q1: Why is $\\Delta H_c^\\circ$ more negative than $\\Delta U_c^\\circ$ for benzoic acid?</strong><br>\n<em>A1:</em> The reaction consumes $7.5\\text{ moles}$ of $O_2(g)$ to produce $7.0\\text{ moles}$ of $CO_2(g)$, yielding $\\Delta n_g = -0.5\\text{ mol}$; surrounding atmosphere does $P \\Delta V$ work on the system, releasing an additional $-1.24\\text{ kJ/mol}$ of enthalpy.</p>\n<p><strong>Q2: What is the purpose of performing nitric acid titration after combustion?</strong><br>\n<em>A2:</em> High-temperature oxidation of trace residual atmospheric $N_2$ forms nitric acid ($HNO_3$); titrating the bomb washings with $0.0709\\text{ N } NaOH$ quantifies the exothermic heat of acid formation ($e_{\\text{acid}} = 57.8\\text{ J/mL}$), which is subtracted from raw heat.</p>\n\n<h3>12. Concluding Summary & Verified Engineering Metric</h3>\n<p>Isoperibol oxygen bomb calorimetry successfully established the thermochemical energy equivalent of the calorimeter system. The experimental thermometric slope $S = 2.6500^\\circ\\text{C/g}$ verified the calorimeter energy equivalent $W_{\\text{cal}} = 9.9751\\text{ kJ/K}$ and gross heat of combustion $-\\Delta u_c = 26.434\\text{ kJ/g}$.</p>"
        },
        {
                "number": 36,
                "slug": "partial-molar-volume-binary-solution-dilatometry",
                "title": "Partial Molar Volume & Excess Volume in Binary Solutions via Precision Pycnometry & Dilatometry",
                "shortTitle": "Partial Molar Volume Dilatometry",
                "aim": "Determine the densities of ethanol-water mixtures across ethanol mole fractions x_EtOH from 0.05 to 0.30 at 25.00 °C using Gay-Lussac pycnometry and capillary dilatometry, evaluate the apparent molar volume phi_V, and extract the infinite-dilution partial molar volume and volumetric concentration slope.",
                "inputLabel": "Ethanol Mole Fraction x_EtOH",
                "shortInput": "Ethanol Mole Fraction",
                "inputUnit": "mol/mol",
                "min": 0.05,
                "max": 0.3,
                "step": 0.05,
                "initial": 0.15,
                "inputDecimals": 2,
                "rawLabel": "Apparent Molar Volume phi_V",
                "rawUnit": "cm^3/mol",
                "rawDecimals": 4,
                "xAxis": "Ethanol mole fraction x_EtOH (mol/mol)",
                "yAxis": "Apparent molar volume phi_V (cm^3/mol)",
                "xScale": 1.0,
                "yScale": 1.0,
                "emptyX": 0.18,
                "emptyY": 56.5,
                "targetName": "Apparent Molar Volume Slope S",
                "target": "14.5000",
                "refValue": 14.5,
                "resultUnit": "cm^3/mol",
                "resultDecimals": 4,
                "resultScale": 1.0,
                "fitEquation": "phi_V = S · x_EtOH + phi_V0 = 14.5000 · x_EtOH + 54.2000",
                "intro": "In chemical solution thermodynamics, extensive thermodynamic properties—including total volume V, enthalpy H, entropy S, and Gibbs free energy G—depend not only on temperature and pressure but also on mixture composition. For a non-ideal binary mixture, the total volume is not simply the sum of the pure component volumes due to differences in molecular packing, interstitial cavity filling, and intermolecular hydrogen bonding. The partial molar volume of component i, defined as V_bar_i = (∂V / ∂n_i)_{T, P, n_j≠i}, represents the change in total mixture volume per mole of component i added at constant temperature, pressure, and remaining component amounts. By Euler's theorem for homogeneous functions of degree 1, the total volume of a binary solution containing n_1 moles of solvent (water) and n_2 moles of solute (ethanol) is given by: V = n_1 · V_bar_1 + n_2 · V_bar_2. Dividing by total moles yields the mean molar volume: V_m = x_1 · V_bar_1 + x_2 · V_bar_2. In dilute and moderately concentrated solutions, experimental data are analyzed through the apparent molar volume phi_V: phi_V = (V - n_1 · V_1^*) / n_2 = (M_2 / ρ) - [(ρ - ρ_1^*) / (m · ρ · ρ_1^*)], where M_2 is solute molar mass, m is molality, and ρ and ρ_1^* are solution and pure solvent densities. In the dilute alcohol concentration regime (x_EtOH = 0.05 to 0.30), the apparent molar volume increases linearly with mole fraction according to the Redlich–Meyer and Mason relations: phi_V = phi_V0 + S · x_EtOH, where phi_V0 is the infinite-dilution partial molar volume of ethanol in water (representing an isolated ethanol molecule surrounded purely by a cage of hydrogen-bonded water molecules, often exhibiting hydrophobic hydration) and S is the volumetric interaction slope. In this laboratory investigation, precision Gay-Lussac pycnometers and capillary dilatometers are operated at 25.000 ± 0.005 °C to measure densities across x_EtOH from 0.05 to 0.30, evaluate phi_V, and determine the infinite-dilution volume phi_V0 = 54.2000 cm^3/mol and slope S = 14.5000 cm^3/mol.",
                "modelExtra": "Evaluated using calibrated 25.000 mL Gay-Lussac quartz pycnometers and a constant-temperature immersion bath at 25.000 ± 0.005 °C. Density of pure deionized water at 25.00 °C = 0.997048 g/cm^3; pure ethanol = 0.78506 g/cm^3.",
                "apparatus": [
                        {
                                "name": "Calibrated 25.000 mL Gay-Lussac Quartz Pycnometer",
                                "purpose": "Measures solution liquid density with ±0.00005 g/cm^3 precision via capillary ground stopper."
                        },
                        {
                                "name": "Ultra-Stable Thermostatic Water Bath",
                                "purpose": "Controls temperature at 25.000 ± 0.005 °C to eliminate thermal expansion density drift."
                        },
                        {
                                "name": "High-Precision Analytical Balance (0.0001 g)",
                                "purpose": "Weighs empty, dry, and liquid-filled pycnometer vessels with 0.1 mg accuracy."
                        },
                        {
                                "name": "Capillary Dilatometer Cell",
                                "purpose": "Measures continuous volume contraction upon mixing with 0.001 cm^3 sensitivity."
                        },
                        {
                                "name": "Degassed HPLC-Grade Reagents (Water & Absolute Ethanol)",
                                "purpose": "Eliminates dissolved microbubbles that skew volumetric pycnometric measurements."
                        },
                        {
                                "name": "Digital Quartz Density Meter (Verification Standard)",
                                "purpose": "Provides secondary oscillating U-tube density validation at 25.000 °C."
                        }
                ],
                "procedure": [
                        {
                                "title": "Pycnometer Tare & Volume Calibration",
                                "text": "Thoroughly clean, rinse with acetone, and vacuum-dry the pycnometer; record empty dry weight W_0; fill with degassed DI water at 25.000 °C to find calibrated volume V_pyc."
                        },
                        {
                                "title": "Binary Solution Preparation",
                                "text": "Prepare binary ethanol-water solutions at mole fractions x_EtOH = 0.05, 0.10, 0.15, 0.20, 0.25, and 0.30 by gravimetric dispensing on the analytical balance."
                        },
                        {
                                "title": "Thermal Equilibration in Constant Bath",
                                "text": "Fill pycnometer with x_EtOH = 0.05 solution; immerse in 25.000 °C bath for 30 minutes; seat capillary stopper and wipe exterior dry."
                        },
                        {
                                "title": "Precision Density Determination",
                                "text": "Weigh filled pycnometer W_1; compute solution density ρ = (W_1 - W_0) / V_pyc corrected for air buoyancy."
                        },
                        {
                                "title": "Apparent Molar Volume Calculation",
                                "text": "Compute apparent molar volume phi_V = (M_2 / ρ) - [(ρ - ρ_1^*) / (m · ρ · ρ_1^*)] for each composition."
                        },
                        {
                                "title": "Composition Step & Infinite Dilution Regression",
                                "text": "Repeat density measurements for remaining mixtures; plot phi_V versus x_EtOH to determine infinite-dilution volume phi_V0 and slope S."
                        }
                ],
                "topics": [
                        {
                                "question": "What is the physical meaning of a partial molar property?",
                                "answer": "A partial molar property represents the contribution per mole of that component to the total extensive property of the mixture; it reflects how the thermodynamic property changes when an infinitesimal amount of that component is added at constant T, P, and other compositions."
                        },
                        {
                                "question": "Why is the partial molar volume of ethanol at infinite dilution (54.2 cm^3/mol) smaller than pure ethanol molar volume (58.7 cm^3/mol)?",
                                "answer": "When an ethanol molecule enters pure water, the small water molecules arrange into an ordered, clathrate-like cage around the hydrophobic ethyl tail (hydrophobic hydration), and the hydroxyl group forms strong hydrogen bonds that fit interstitially into the water network, causing net volume contraction."
                        },
                        {
                                "question": "How is the tangent intercept method used to determine both partial molar volumes from mean molar volume data?",
                                "answer": "By plotting mean molar volume V_m versus mole fraction x_2, drawing a tangent line at any composition x_2 intersects the y-axis at x_1=1 (x_2=0) at the partial molar volume V_bar_1, and intersects the vertical line at x_2=1 at the partial molar volume V_bar_2."
                        },
                        {
                                "question": "Why must buoyancy corrections be applied when weighing pycnometers on an analytical balance?",
                                "answer": "Air has a finite density (~0.0012 g/cm^3 at 20 °C); because the volume of the glass pycnometer and brass calibration weights displace air unequally, uncorrected weights introduce errors of 0.1% in density, which severely distorts apparent molar volumes."
                        },
                        {
                                "question": "What is excess molar volume V^E and what sign does it have for ethanol-water?",
                                "answer": "Excess molar volume V^E = V_m - (x_1 V_1^* + x_2 V_2^*) is the difference between actual solution volume and ideal solution volume; for ethanol-water mixtures, V^E is negative across the entire composition range (reaching a minimum of ~-1.1 cm^3/mol at x_EtOH ≈ 0.4) due to strong hydrogen bonding and interstitial packing."
                        },
                        {
                                "question": "How does temperature affect the partial molar volume of water and ethanol?",
                                "answer": "As temperature increases, thermal expansion increases both pure and partial molar volumes; however, because elevated thermal energy disrupts the rigid hydrogen-bonded water structure, the extent of excess volume contraction (|V^E|) decreases with rising temperature."
                        }
                ],
                "precautions": [
                        "Ensure the pycnometer exterior is wiped completely dry with lint-free paper before weighing, avoiding warming the vessel with bare fingers.",
                        "Degas all deionized water and ethanol feedstocks under vacuum sonication to eliminate dissolved air bubbles that adhere to pycnometer walls.",
                        "Seat the capillary ground-glass stopper firmly with a single smooth axial motion to prevent trapping air bubbles inside the capillary bore.",
                        "Maintain the thermostatic water bath strictly within ±0.005 °C, as water-ethanol density changes by ~0.0008 g/cm^3 per degree Celsius."
                ],
                "quiz": [
                        {
                                "question": "The apparent molar volume phi_V of a solute in binary solution is defined as:",
                                "options": [
                                        "phi_V = (V - n_1 · V_1^*) / n_2",
                                        "phi_V = V / (n_1 + n_2)",
                                        "phi_V = n_2 · V_2^*",
                                        "phi_V = (V_2^* - V_1^*) / n_2"
                                ],
                                "correct": 0,
                                "explanation": "Apparent molar volume attributes the entire difference between total solution volume V and pure solvent volume (n_1 · V_1^*) to the solute moles n_2."
                        },
                        {
                                "question": "At infinite dilution (x_2 -> 0), the apparent molar volume phi_V0 is equal to:",
                                "options": [
                                        "Zero",
                                        "Pure solute molar volume V_2^*",
                                        "Infinite-dilution partial molar volume V_bar_2^inf",
                                        "Pure solvent molar volume V_1^*"
                                ],
                                "correct": 2,
                                "explanation": "In the limit of infinite dilution, solute-solute interactions vanish, and apparent molar volume phi_V0 becomes identical to the partial molar volume at infinite dilution V_bar_2^inf."
                        },
                        {
                                "question": "For ethanol-water mixtures at 25 °C, the excess molar volume V^E is:",
                                "options": [
                                        "Strictly positive",
                                        "Strictly zero",
                                        "Negative across all compositions",
                                        "Positive at low ethanol and negative at high ethanol"
                                ],
                                "correct": 2,
                                "explanation": "Strong intermolecular hydrogen bonding and interstitial packing of water around ethyl groups produce net volumetric contraction, making V^E negative across all compositions."
                        },
                        {
                                "question": "Euler's theorem for extensive properties dictates that total solution volume V is:",
                                "options": [
                                        "V = n_1 V_bar_1 + n_2 V_bar_2",
                                        "V = n_1 V_1^* + n_2 V_2^*",
                                        "V = (n_1 + n_2) · (V_bar_1 + V_bar_2)",
                                        "V = n_1 n_2 (V_bar_1 - V_bar_2)"
                                ],
                                "correct": 0,
                                "explanation": "Volume is a homogeneous function of degree 1 in mole numbers, so Euler's theorem requires V = n_1 V_bar_1 + n_2 V_bar_2."
                        }
                ],
                "samples": [
                        0.05,
                        0.1,
                        0.15,
                        0.2,
                        0.25,
                        0.3
                ],
                "measureLabel": "Record pycnometric apparent molar volume",
                "readings": [
                        "x_etoh",
                        "density",
                        "molar_volume",
                        "phi_v",
                        "excess_volume",
                        "partial_v2"
                ],
                "theory": "<h3>Thermodynamic Fundamentals of Partial Molar Quantities</h3>\n<p>An extensive thermodynamic property $Y$ (such as volume $V$, internal energy $U$, enthalpy $H$, entropy $S$, or Gibbs energy $G$) of a multicomponent homogeneous mixture depends on temperature $T$, pressure $P$, and the mole numbers of all constituents $n_1, n_2, \\dots, n_C$. The partial molar property of component $i$ is defined as the partial derivative of $Y$ with respect to $n_i$ at constant $T$, $P$, and other component amounts:</p>\n\\[ \\bar{Y}_i = \\left( \\frac{\\partial Y}{\\partial n_i} \\right)_{T, P, n_{j \\neq i}} \\]\n<p>Because $Y$ is a homogeneous function of degree 1 with respect to mole numbers, Euler's theorem dictates:</p>\n\\[ Y = \\sum_{i=1}^C n_i \\, \\bar{Y}_i \\implies Y_m = \\frac{Y}{n_t} = \\sum_{i=1}^C x_i \\, \\bar{Y}_i \\]\n<p>For a binary solution of solvent 1 (water) and solute 2 (ethanol), the total volume and mean molar volume are:</p>\n\\[ V = n_1 \\, \\bar{V}_1 + n_2 \\, \\bar{V}_2, \\quad V_m = x_1 \\, \\bar{V}_1 + x_2 \\, \\bar{V}_2 \\]\n\n<h3>Apparent Molar Volume $\\phi_V$ Formalism</h3>\n<p>While partial molar volumes are defined differentially, experimentalists evaluate volumetric behavior through the apparent molar volume $\\phi_V$, which assigns all volumetric deviation from pure solvent ($V_1^* = M_1 / \\rho_1^*$) to the solute:</p>\n\\[ \\phi_V = \\frac{V - n_1 V_1^*}{n_2} = \\frac{V_m - x_1 V_1^*}{x_2} \\]\n<p>Expressed in terms of measured solution density $\\rho$, pure solvent density $\\rho_1^*$, solute molar mass $M_2$, and solution molality $m$ (moles solute per kg solvent):</p>\n\\[ \\phi_V = \\frac{M_2}{\\rho} - \\frac{1000 \\, (\\rho - \\rho_1^*)}{m \\, \\rho \\, \\rho_1^*} \\]\n<p>At infinite dilution ($x_2 \\to 0$, $m \\to 0$), apparent molar volume equals the infinite-dilution partial molar volume:</p>\n\\[ \\lim_{x_2 \\to 0} \\phi_V = \\bar{V}_2^\\infty = \\phi_{V0} \\]\n\n<h3>Linear Concentration Dependence & Redlich–Meyer Scaling</h3>\n<p>In dilute and moderately concentrated alcohol-water solutions ($x_{\\text{EtOH}} \\le 0.30$), apparent molar volume increases linearly with mole fraction due to solute-solute hydrophobic pair interactions:</p>\n\\[ \\phi_V = S \\cdot x_{\\text{EtOH}} + \\phi_{V0} = 14.5000 \\cdot x_{\\text{EtOH}} + 54.2000 \\]\n<p>where $\\phi_{V0} = 54.2000\\text{ cm}^3\\text{/mol}$ represents the partial molar volume of ethanol at infinite dilution and $S = 14.5000\\text{ cm}^3\\text{/mol}$ is the volumetric interaction slope.</p>\n<p>The true partial molar volume of ethanol is related to apparent molar volume by:</p>\n\\[ \\bar{V}_2 = \\phi_V + x_2 \\, (1 - x_2) \\left( \\frac{\\partial \\phi_V}{\\partial x_2} \\right)_{T, P} = \\phi_V + S \\, x_2 \\, (1 - x_2) \\]",
                "report": "<h3>1. Objective & Practical Significance</h3>\n<p>This laboratory investigation determines the liquid densities, apparent molar volumes ($\\phi_V$), and partial molar volumes ($\\bar{V}_1, \\bar{V}_2$) of binary ethanol-water solutions across ethanol mole fractions $x_{\\text{EtOH}} = 0.05$ to $0.30$ at $25.000^\\circ\\text{C}$ using Gay-Lussac pycnometry. By evaluating the linear concentration dependence $\\phi_V = S \\cdot x_{\\text{EtOH}} + \\phi_{V0}$, we determine the infinite-dilution partial molar volume $\\phi_{V0} = 54.2000\\text{ cm}^3\\text{/mol}$ and volumetric interaction slope $S = 14.5000\\text{ cm}^3\\text{/mol}$, characterizing solvent-solute and solute-solute hydrophobic interactions.</p>\n\n<h3>2. Governing Transport Equations & Phenomenological Relations</h3>\n<p>Apparent molar volume is calculated from measured densities by: $\\phi_V = \\frac{V_m - x_1 V_1^*}{x_2}$. The linear concentration relationship is:</p>\n\\[ \\phi_V = S \\cdot x_{\\text{EtOH}} + \\phi_{V0} = 14.5000 \\cdot x_{\\text{EtOH}} + 54.2000 \\]\n<p>where $S = 14.5000\\text{ cm}^3\\text{/mol}$ and $\\phi_{V0} = 54.2000\\text{ cm}^3\\text{/mol}$. Partial molar volume of ethanol is: $\\bar{V}_2 = \\phi_V + S \\cdot x_2 \\cdot (1 - x_2)$.</p>\n\n<h3>3. Experimental Apparatus & Instrumentation Specification</h3>\n<p>Measurements utilized three calibrated $25.000\\text{ mL}$ Gay-Lussac quartz pycnometers ($\\pm 0.002\\text{ mL}$), a Mettler Toledo analytical balance ($\\pm 0.0001\\text{ g}$), an ultra-stable thermostatic water bath held at $25.000 \\pm 0.005^\\circ\\text{C}$, and degassed HPLC-grade water ($\\rho_1^* = 0.997048\\text{ g/cm}^3$) and absolute ethanol ($\\rho_2^* = 0.78506\\text{ g/cm}^3$).</p>\n\n<h3>4. Standard Operating Procedure & Measurement Protocols</h3>\n<p>Pycnometers were cleaned with chromic acid, rinsed with deionized water and acetone, and vacuum-dried to constant weight $W_0$. Calibration was performed with degassed DI water at $25.000^\\circ\\text{C}$ to establish pycnometer volume $V_{\\text{pyc}} = 25.042\\text{ cm}^3$. Solutions at $x_{\\text{EtOH}} = 0.05, 0.10, 0.15, 0.20, 0.25,$ and $0.30$ were gravimetrically prepared, equilibrated in the $25.000^\\circ\\text{C}$ bath for 30 minutes, wiped dry, and weighed to determine density $\\rho$ and apparent molar volume $\\phi_V$.</p>\n\n<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>\n<p>Ethanol is volatile and flammable. Gravimetric dispensing was performed inside a ventilated fume hood away from open flames. Pycnometer vessels were handled with lint-free tongs. Safety glasses and nitrile gloves were worn.</p>\n\n<h3>6. Raw Experimental Observations & Systematic Data Records</h3>\n<p><strong>Simulated demonstration data.</strong> The following pycnometric observations were recorded at $T = 25.000^\\circ\\text{C}$ ($P = 101.325\\text{ kPa}$):</p>\n<table>\n<thead>\n<tr><th>Run</th><th>Ethanol $x_{\\text{EtOH}}$ (mol/mol)</th><th>Solution Density $\\rho$ (g/cm³)</th><th>Mean Molar Vol $V_m$ (cm³/mol)</th><th>Apparent Vol $\\phi_V$ (cm³/mol)</th><th>Excess Vol $V^E$ (cm³/mol)</th><th>Partial Molar $\\bar{V}_2$ (cm³/mol)</th></tr>\n</thead>\n<tbody>\n<tr><td>1</td><td>0.05</td><td>0.98187</td><td>19.824</td><td>54.9250</td><td>-0.218</td><td>55.614</td></tr>\n<tr><td>2</td><td>0.10</td><td>0.96864</td><td>21.650</td><td>55.6500</td><td>-0.415</td><td>56.955</td></tr>\n<tr><td>3</td><td>0.15</td><td>0.95501</td><td>23.504</td><td>56.3750</td><td>-0.589</td><td>58.224</td></tr>\n<tr><td>4</td><td>0.20</td><td>0.94056</td><td>25.402</td><td>57.1000</td><td>-0.738</td><td>59.420</td></tr>\n<tr><td>5</td><td>0.25</td><td>0.92534</td><td>27.352</td><td>57.8250</td><td>-0.860</td><td>60.544</td></tr>\n<tr><td>6</td><td>0.30</td><td>0.90956</td><td>29.360</td><td>58.5500</td><td>-0.952</td><td>61.595</td></tr>\n</tbody>\n</table>\n\n<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>\n<p>Linear regression of apparent molar volume $\\phi_V$ versus ethanol mole fraction $x_{\\text{EtOH}}$ yields:</p>\n\\[ \\phi_V = 14.50000 \\cdot x_{\\text{EtOH}} + 54.20000 \\]\n<p>with coefficient of determination $R^2 = 1.000000$. The experimental slope $S = 14.50000\\text{ cm}^3\\text{/mol}$ and infinite-dilution intercept $\\phi_{V0} = 54.20000\\text{ cm}^3\\text{/mol}$ match target parameters ($14.5000$ and $54.2000$) with $0.00\\%$ deviation. Pure ethanol molar volume is $V_2^* = M_2 / \\rho_2^* = 46.069 / 0.78506 = 58.682\\text{ cm}^3\\text{/mol}$. The infinite-dilution volume contraction is:</p>\n\\[ \\Delta \\bar{V}_2^\\infty = \\bar{V}_2^\\infty - V_2^* = 54.200 - 58.682 = -4.482\\text{ cm}^3\\text{/mol} \\]\n\n<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>\n<p>Analytical balance precision is $\\pm 0.0001\\text{ g}$, temperature bath stability is $\\pm 0.005^\\circ\\text{C}$, and pycnometer volume error is $\\pm 0.002\\text{ mL}$. Propagating into apparent molar volume yields an experimental uncertainty of $\\pm 0.045\\text{ cm}^3\\text{/mol}$ ($0.08\\%$), reporting $\\phi_{V0} = 54.200 \\pm 0.045\\text{ cm}^3\\text{/mol}$ and $S = 14.50 \\pm 0.12\\text{ cm}^3\\text{/mol}$.</p>\n\n<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>\n<p>The large negative infinite-dilution volume change ($-4.482\\text{ cm}^3\\text{/mol}$) highlights hydrophobic hydration, wherein bulky water networks accommodate isolated ethanol molecules within clathrate-like cavities. As ethanol concentration increases ($x_{\\text{EtOH}} \\to 0.30$), ethanol molecules share hydration shells and disrupt cooperative water bonding, causing $\\phi_V$ to increase linearly toward pure ethanol molar volume.</p>\n\n<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>\n<p>Accurate partial and excess molar volumes are critical for sizing high-pressure piping, pump head calculations in distillery blending terminals, calibration of custody-transfer mass flowmeters, and equation-of-state parameters in process simulators.</p>\n\n<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>\n<p><strong>Q1: Why is the excess volume $V^E$ negative for ethanol-water mixtures?</strong><br>\n<em>A1:</em> Intermolecular hydrogen bonding between water and ethanol hydroxyl groups combined with the interstitial fitting of water molecules into ethanol voids produces a tighter, more compact molecular packing than the separate pure liquids.</p>\n<p><strong>Q2: How does the tangent-intercept method extract partial molar volumes from a plot of $V_m$ vs $x_2$?</strong><br>\n<em>A2:</em> The tangent line at any composition $x_2$ has equation $y = V_m + (\\partial V_m / \\partial x_2)(x - x_2)$; setting $x=0$ yields the y-intercept $\\bar{V}_1$, and setting $x=1$ yields the intercept $\\bar{V}_2$.</p>\n\n<h3>12. Concluding Summary & Verified Engineering Metric</h3>\n<p>Precision pycnometry successfully quantified binary solution thermodynamics for ethanol-water at $25.000^\\circ\\text{C}$. The calibrated linear model yielded infinite-dilution partial molar volume $\\phi_{V0} = 54.2000\\text{ cm}^3\\text{/mol}$ and volumetric slope $S = 14.5000\\text{ cm}^3\\text{/mol}$, validating thermodynamic excess volume contraction.</p>"
        },
        {
                "number": 37,
                "slug": "solid-liquid-equilibrium-sle-eutectic-phase-diagram",
                "title": "Solid-Liquid Phase Equilibrium (SLE) & Simple Eutectic Phase Diagram Construction",
                "shortTitle": "SLE Eutectic Phase Diagram",
                "aim": "Construct the solid-liquid equilibrium (SLE) phase diagram for a binary naphthalene-biphenyl organic eutectic mixture using thermal analysis cooling curves across solute mole fractions x_B from 0.04 to 0.24, evaluate freezing point depression ΔT_f, determine the cryoscopic limiting slope, and extract the eutectic point coordinates.",
                "inputLabel": "Biphenyl Solute Mole Fraction x_B",
                "shortInput": "Solute Mole Fraction x_B",
                "inputUnit": "mol/mol",
                "min": 0.04,
                "max": 0.24,
                "step": 0.04,
                "initial": 0.12,
                "inputDecimals": 2,
                "rawLabel": "Freezing Point Depression ΔT_f",
                "rawUnit": "°C",
                "rawDecimals": 2,
                "xAxis": "Biphenyl solute mole fraction x_B (mol/mol)",
                "yAxis": "Freezing point depression ΔT_f (°C)",
                "xScale": 1.0,
                "yScale": 1.0,
                "emptyX": 0.14,
                "emptyY": 7.0,
                "targetName": "Cryoscopic Eutectic Limiting Slope S",
                "target": "58.5000",
                "refValue": 58.5,
                "resultUnit": "°C",
                "resultDecimals": 4,
                "resultScale": 1.0,
                "fitEquation": "ΔT_f = S · x_B = 58.5000 · x_B",
                "intro": "Solid-liquid equilibrium (SLE) phase diagrams are foundational to chemical engineering crystallization, melt purification, pharmaceutical co-crystal formulation, metallurgy, and thermal energy storage phase-change materials (PCMs). When two chemical species are completely miscible in the liquid melt but mutually immiscible in the solid crystalline state, they form a simple binary eutectic system. The classic chemical engineering model system is the binary mixture of naphthalene (component A, pure melting point T_mA = 80.20 °C) and biphenyl (component B, pure melting point T_mB = 69.20 °C). In this system, adding solute B to pure liquid A depresses the liquidus temperature—the temperature at which the first pure crystal of component A nucleates from the melt. According to the Schröder–van Laar equation derived from chemical potential equality between pure solid A and liquid solution A: ln(γ_A · x_A) = -[ΔH_fus,A / R] · [1/T - 1/T_mA], where ΔH_fus,A is the standard enthalpy of fusion (18.98 kJ/mol for naphthalene) and γ_A is the liquid-phase activity coefficient. In the dilute solute regime (x_B = 1 - x_A << 1), the liquid behaves nearly ideally (γ_A ≈ 1.00), and expanding the reciprocal temperature term in a first-order series yields the linear cryoscopic freezing point depression relation: ΔT_f = T_mA - T = S · x_B, where the cryoscopic limiting slope is given by S = R · T_mA^2 / ΔH_fus,A = 58.5000 °C (K). Continued addition of solute B depresses the liquidus until it intersects the second liquidus curve of component B at the eutectic point (T_eutectic ≈ 39.4 °C, x_B,eutectic ≈ 0.45), where both solid A and solid B crystallize simultaneously at a unique invariant temperature. In this laboratory experiment, an instrumented thermal analysis freezing point apparatus records time-temperature cooling curves across biphenyl mole fractions from 0.04 to 0.24 to identify the liquidus break temperatures, confirm the linear cryoscopic slope S = 58.5000 °C, and construct the complete SLE phase boundary.",
                "modelExtra": "Evaluated using an automated thermal analysis cooling cell with 4-wire Pt100 RTD sensor (±0.02 °C) and programmable air-jacketed cooling mantle. Pure naphthalene: T_mA = 80.20 °C, ΔH_fus,A = 18.98 kJ/mol; pure biphenyl: T_mB = 69.20 °C, ΔH_fus,B = 18.58 kJ/mol.",
                "apparatus": [
                        {
                                "name": "Thermal Analysis Freezing Point Glass Cell",
                                "purpose": "Double-walled vacuum-jacketed glass tube with internal PTFE mechanical paddle stirrer for controlled cooling."
                        },
                        {
                                "name": "Precision 4-Wire Pt100 RTD Sensor & Data Logger",
                                "purpose": "Measures melt temperature with 0.01 °C resolution and 5 Hz sampling rate to record cooling curve inflection points."
                        },
                        {
                                "name": "Thermostatic Silicone Oil Heating Bath",
                                "purpose": "Melts organic mixtures up to 100.0 °C and maintains uniform liquid temperature before cooling."
                        },
                        {
                                "name": "Controlled Ambient Air-Jacketed Cooling Jacket",
                                "purpose": "Provides steady, reproducible convective heat removal rate of 1.5 to 2.0 °C/min during solidification."
                        },
                        {
                                "name": "Variable-Speed Reciprocating Stirrer Motor",
                                "purpose": "Maintains continuous 120 RPM vertical agitation to eliminate thermal stratification and minimize supercooling."
                        },
                        {
                                "name": "High-Precision Analytical Balance (0.0001 g)",
                                "purpose": "Weighs naphthalene and biphenyl components gravimetrically to establish exact synthetic mole fractions."
                        }
                ],
                "procedure": [
                        {
                                "title": "Sensor Calibration & Pure Component Baseline",
                                "text": "Calibrate the Pt100 RTD sensor against distilled ice point (0.00 °C) and boiling water (100.00 °C); record cooling curve of pure naphthalene to verify T_mA = 80.20 °C."
                        },
                        {
                                "title": "Gravimetric Mixture Preparation",
                                "text": "Weigh exactly 10.000 g of naphthalene and add calculated mass of biphenyl to synthesize x_B = 0.04 into the freezing tube."
                        },
                        {
                                "title": "Complete Liquefaction in Oil Bath",
                                "text": "Immerse sample tube in 95.0 °C silicone oil bath until solids are completely melted; stir gently to ensure homogeneous liquid mixing."
                        },
                        {
                                "title": "Cooling Cell Transfer & Stirring Activation",
                                "text": "Transfer tube to the air-jacketed cooling assembly; start reciprocating stirrer at 120 RPM and begin logging temperature versus time at 2 Hz."
                        },
                        {
                                "title": "Cooling Curve Inflection & Liquidus Determination",
                                "text": "Identify the liquidus freezing point T_f from the cooling curve slope change (inflection from sensible cooling to crystal latent heat plateau); compute ΔT_f = T_mA - T_f."
                        },
                        {
                                "title": "Composition Step Progression & Eutectic Logging",
                                "text": "Add subsequent increments of biphenyl to achieve x_B = 0.08, 0.12, 0.16, 0.20, and 0.24, repeating the melt-cool protocol to determine cryoscopic slope S."
                        }
                ],
                "topics": [
                        {
                                "question": "What is the Gibbs Phase Rule and what degrees of freedom exist at a binary eutectic point?",
                                "answer": "The phase rule is F = C - P + 1 (at constant atmospheric pressure); at the eutectic point of a binary system (C = 2), three phases coexist in equilibrium (liquid melt, solid A, and solid B, so P = 3), resulting in F = 2 - 3 + 1 = 0 degrees of freedom, meaning the eutectic temperature and composition are invariant."
                        },
                        {
                                "question": "How does supercooling affect cooling curves and how can it be distinguished from the true freezing point?",
                                "answer": "Supercooling causes liquid temperature to dip below the equilibrium freezing point before crystal nucleation begins; once nucleation occurs, latent heat rapidly recalesces the melt back up to the true liquidus plateau, which represents the equilibrium freezing point."
                        },
                        {
                                "question": "Why is the simple eutectic model valid for the naphthalene-biphenyl system?",
                                "answer": "Naphthalene (fused bicyclic aromatic ring) and biphenyl (two linked phenyl rings) have different molecular shapes and crystal lattices that prevent substitution into each other's solid crystals, resulting in negligible solid solubility while forming a nearly ideal liquid solution."
                        },
                        {
                                "question": "What is the physical interpretation of the cryoscopic constant K_f?",
                                "answer": "The cryoscopic constant K_f = (R · T_m^2 · M_solvent) / (1000 · ΔH_fus) represents the freezing point depression produced by an ideal solute at 1.0 molal concentration; it is an intrinsic thermodynamic property of the solvent matrix alone."
                        },
                        {
                                "question": "How can the eutectic composition and temperature be calculated theoretically?",
                                "answer": "By solving the two simultaneous Schröder–van Laar equations for component A and component B: ln(x_A) = -[ΔH_fus,A / R] [1/T_e - 1/T_mA] and ln(1 - x_A) = -[ΔH_fus,B / R] [1/T_e - 1/T_mB]; their simultaneous intersection gives T_e and x_A,eutectic."
                        },
                        {
                                "question": "What happens to a liquid mixture at the exact eutectic composition upon cooling?",
                                "answer": "It cools as a single homogeneous liquid until reaching the eutectic temperature, whereupon it solidifies isothermally at constant temperature into a fine, intergrown microstructural lamellar solid mixture of pure A and pure B without any prior liquidus slope break."
                        }
                ],
                "precautions": [
                        "Maintain continuous mechanical stirring during cooling to prevent severe supercooling and ensure uniform temperature throughout the melt.",
                        "Operate inside a ventilated fume hood to avoid inhaling volatile aromatic naphthalene and biphenyl vapors at 95 °C.",
                        "Do not allow cooling water or oil bath fluids to enter the sample tube, as trace moisture forms a ternary system that distorts freezing points.",
                        "Verify complete remelting and homogeneous dissolution of all solid crystals before commencing each cooling curve run."
                ],
                "quiz": [
                        {
                                "question": "According to the Gibbs Phase Rule at constant pressure (F = C - P + 1), the degrees of freedom F at a binary eutectic point are:",
                                "options": [
                                        "0 (invariant)",
                                        "1 (univariant)",
                                        "2 (bivariant)",
                                        "3 (trivariant)"
                                ],
                                "correct": 0,
                                "explanation": "With C = 2 components and P = 3 coexisting phases (liquid, solid A, solid B), F = 2 - 3 + 1 = 0, meaning temperature and compositions are fixed."
                        },
                        {
                                "question": "The Schröder–van Laar equation models solid-liquid equilibrium under which assumption?",
                                "options": [
                                        "Complete solid solubility",
                                        "Pure solid components mutually immiscible in solid phase",
                                        "Vapor pressure equals atmospheric pressure",
                                        "Immiscible liquid phases"
                                ],
                                "correct": 1,
                                "explanation": "The Schröder–van Laar formulation assumes the crystallized solid is 100% pure component with zero solid solution formation."
                        },
                        {
                                "question": "In a cooling curve, the onset of crystallization of the primary component appears as:",
                                "options": [
                                        "An abrupt increase in cooling rate",
                                        "A reduction in cooling rate slope (thermal arrest/break)",
                                        "A sudden drop to zero temperature",
                                        "An explosion of steam"
                                ],
                                "correct": 1,
                                "explanation": "The release of latent heat of fusion slows down convective cooling, producing a distinct slope inflection (liquidus break) on the temperature-time curve."
                        },
                        {
                                "question": "The cryoscopic limiting slope S = dT_f / dx_B in a dilute ideal binary solution is equal to:",
                                "options": [
                                        "R · T_mA^2 / ΔH_fus,A",
                                        "ΔH_fus,A / (R · T_mA)",
                                        "T_mA / ΔH_fus,A",
                                        "R · T_mA / 2"
                                ],
                                "correct": 0,
                                "explanation": "Differentiating the ideal Schröder–van Laar equation ln(1 - x_B) ≈ -x_B = -(ΔH_fus/R)(1/T - 1/T_mA) yields S = R · T_mA^2 / ΔH_fus,A."
                        }
                ],
                "samples": [
                        0.04,
                        0.08,
                        0.12,
                        0.16,
                        0.2,
                        0.24
                ],
                "measureLabel": "Record liquidus freezing point depression",
                "readings": [
                        "x_biphenyl",
                        "liquidus_temp",
                        "delta_tf",
                        "cooling_rate",
                        "eutectic_temp",
                        "ideal_activity"
                ],
                "theory": "<h3>Solid-Liquid Equilibrium & Chemical Potential Equality</h3>\n<p>Solid-liquid equilibrium (SLE) describes phase coexistence between a liquid solution and solid crystalline phases. When a binary liquid mixture of species $A$ and $B$ cools to its liquidus curve, the chemical potential of component $A$ in the liquid solution equals the chemical potential of pure crystalline solid $A$ (assuming negligible solid solubility):</p>\n\\[ \\mu_A^L(T, P, x_A) = \\mu_A^S(T, P) \\]\n<p>Expressing liquid chemical potential through activity $a_A = \\gamma_A x_A$ relative to pure liquid standard state $\\mu_A^{\\circ,L}(T, P)$:</p>\n\\[ \\mu_A^{\\circ,L}(T, P) + R T \\ln(\\gamma_A x_A) = \\mu_A^S(T, P) \\]\n\\[ \\ln(\\gamma_A x_A) = \\frac{\\mu_A^S(T, P) - \\mu_A^{\\circ,L}(T, P)}{R T} = -\\frac{\\Delta G_{\\text{fus},A}(T)}{R T} \\]\n<p>Differentiating with respect to temperature using the Gibbs–Helmholtz relation $\\frac{\\partial(\\Delta G/T)}{\\partial T} = -\\frac{\\Delta H}{T^2}$ and integrating from the pure component melting point $T_{mA}$ where $\\Delta G_{\\text{fus},A}(T_{mA}) = 0$ yields the rigorous Schröder–van Laar equation:</p>\n\\[ \\ln(\\gamma_A x_A) = -\\frac{\\Delta H_{\\text{fus},A}}{R} \\left( \\frac{1}{T} - \\frac{1}{T_{mA}} \\right) + \\frac{\\Delta C_{p,A}}{R} \\left( \\frac{T_{mA} - T}{T} - \\ln\\frac{T_{mA}}{T} \\right) \\]\n\n<h3>Dilute Solution Cryoscopy & Linear Limiting Slope</h3>\n<p>In dilute solutions ($x_B = 1 - x_A \\ll 1$), the heat capacity correction term is negligible, the liquid phase behaves ideally ($\\gamma_A \\approx 1.00$), and the natural logarithm expands as $\\ln(1 - x_B) \\approx -x_B$. Furthermore:</p>\n\\[ \\frac{1}{T} - \\frac{1}{T_{mA}} = \\frac{T_{mA} - T}{T \\, T_{mA}} \\approx \\frac{\\Delta T_f}{T_{mA}^2} \\]\n<p>Substituting into the Schröder–van Laar relation yields the classical linear cryoscopic freezing point depression equation:</p>\n\\[ \\Delta T_f = T_{mA} - T = S \\cdot x_B = \\left( \\frac{R \\, T_{mA}^2}{\\Delta H_{\\text{fus},A}} \\right) \\cdot x_B \\]\n<p>For naphthalene ($T_{mA} = 80.20^\\circ\\text{C} = 353.35\\text{ K}$, $\\Delta H_{\\text{fus},A} = 18.98\\text{ kJ/mol}$):</p>\n\\[ S = \\frac{8.31446 \\cdot (353.35)^2}{18,980} = 54.69\\text{ K (theoretical ideal)} \\]\n<p>With slight real-solution activity coefficient departure (Margules excess energy), the calibrated empirical slope is $S = 58.5000^\\circ\\text{C}$.</p>",
                "report": "<h3>1. Objective & Practical Significance</h3>\n<p>This laboratory investigation constructs the binary solid-liquid equilibrium (SLE) phase diagram for naphthalene (A) + biphenyl (B) across solute mole fractions $x_B = 0.04$ to $0.24$ using thermal analysis cooling curves. By measuring the liquidus freezing point depression $\\Delta T_f = T_{mA} - T_f$, we verify the linear cryoscopic limiting relationship $\\Delta T_f = S \\cdot x_B$, determine the cryoscopic slope $S = 58.5000^\\circ\\text{C}$, evaluate the enthalpy of fusion $\\Delta H_{\\text{fus}}$, and establish the invariant eutectic boundary.</p>\n\n<h3>2. Governing Transport Equations & Phenomenological Relations</h3>\n<p>Phase equilibrium obeys the Schröder–van Laar equation: $\\ln(a_A) = -\\frac{\\Delta H_{\\text{fus},A}}{R} \\left( \\frac{1}{T} - \\frac{1}{T_{mA}} \\right)$. In the dilute regime:</p>\n\\[ \\Delta T_f = S \\cdot x_B = 58.5000 \\cdot x_B \\]\n<p>where $S = 58.5000^\\circ\\text{C}$. The eutectic arrest occurs at constant temperature $T_{\\text{eutectic}} = 39.40^\\circ\\text{C}$.</p>\n\n<h3>3. Experimental Apparatus & Instrumentation Specification</h3>\n<p>The apparatus consists of a vacuum-jacketed glass freezing tube with a reciprocating PTFE paddle stirrer ($120\\text{ RPM}$), a 4-wire Pt100 RTD thermometer connected to an automated data logger ($0.01^\\circ\\text{C}$ resolution, $2\\text{ Hz}$ sampling), a thermostatically controlled silicone oil melting bath ($95.0^\\circ\\text{C}$), and an analytical balance ($\\pm 0.0001\\text{ g}$).</p>\n\n<h3>4. Standard Operating Procedure & Measurement Protocols</h3>\n<p>The pure naphthalene baseline was established ($T_{mA} = 80.20^\\circ\\text{C}$). Binary mixtures of naphthalene and biphenyl were gravimetrically synthesized for $x_B = 0.04, 0.08, 0.12, 0.16, 0.20,$ and $0.24$. Each mixture was heated to $95.0^\\circ\\text{C}$ in the oil bath to ensure complete homogeneous melting, transferred to the air-jacketed cooling mantle, and cooled under continuous stirring. Temperature-time cooling curves were recorded to detect the liquidus inflection break and the eutectic thermal arrest.</p>\n\n<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>\n<p>Naphthalene and biphenyl are volatile aromatic solids with strong odors and moderate toxicity. All melting and transfer operations were conducted inside a certified chemical fume hood. Thermal safety gloves were used when handling heated tubes. Splash goggles and lab coats were worn.</p>\n\n<h3>6. Raw Experimental Observations & Systematic Data Records</h3>\n<p><strong>Simulated demonstration data.</strong> The following cooling curve transition points were logged at $P = 101.325\\text{ kPa}$ ($T_{mA} = 80.20^\\circ\\text{C}$):</p>\n<table>\n<thead>\n<tr><th>Run</th><th>Biphenyl $x_B$ (mol/mol)</th><th>Liquidus $T_f$ (°C)</th><th>Depression $\\Delta T_f$ (°C)</th><th>Cooling Inflection (°C/min)</th><th>Eutectic Arrest $T_e$ (°C)</th><th>Calculated Slope (°C)</th></tr>\n</thead>\n<tbody>\n<tr><td>1</td><td>0.04</td><td>77.860</td><td>2.340</td><td>-1.65</td><td>39.40</td><td>58.50</td></tr>\n<tr><td>2</td><td>0.08</td><td>75.520</td><td>4.680</td><td>-1.62</td><td>39.40</td><td>58.50</td></tr>\n<tr><td>3</td><td>0.12</td><td>73.180</td><td>7.020</td><td>-1.58</td><td>39.40</td><td>58.50</td></tr>\n<tr><td>4</td><td>0.16</td><td>70.840</td><td>9.360</td><td>-1.55</td><td>39.40</td><td>58.50</td></tr>\n<tr><td>5</td><td>0.20</td><td>68.500</td><td>11.700</td><td>-1.52</td><td>39.40</td><td>58.50</td></tr>\n<tr><td>6</td><td>0.24</td><td>66.160</td><td>14.040</td><td>-1.48</td><td>39.40</td><td>58.50</td></tr>\n</tbody>\n</table>\n\n<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>\n<p>Linear regression of freezing point depression $\\Delta T_f$ versus biphenyl mole fraction $x_B$ yields:</p>\n\\[ \\Delta T_f = 58.50000 \\cdot x_B + 0.00000 \\]\n<p>with coefficient of determination $R^2 = 1.000000$ and zero intercept. The experimental slope $S = 58.50000^\\circ\\text{C}$ matches the target calibration parameter ($58.5000$) with $0.00\\%$ deviation. Evaluating the effective enthalpy of fusion of naphthalene:</p>\n\\[ \\Delta H_{\\text{fus},A} = \\frac{R T_{mA}^2}{S} = \\frac{8.31446 \\cdot (353.35)^2}{58.500} = 17.74\\text{ kJ/mol} \\]\n<p>The small difference from the ideal pure literature value ($18.98\\text{ kJ/mol}$) reflects slight positive liquid-phase Margules interaction ($A_{12} \\approx 0.12$).</p>\n\n<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>\n<p>Pt100 RTD sensor uncertainty is $\\pm 0.02^\\circ\\text{C}$, and analytical balance precision is $\\pm 0.0001\\text{ g}$ ($u(x_B) = \\pm 0.0002$). Propagating through the cryoscopic regression yields an uncertainty in $S$ of $\\pm 0.28^\\circ\\text{C}$ ($0.48\\%$), reporting $S = 58.50 \\pm 0.28^\\circ\\text{C}$.</p>\n\n<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>\n<p>The linear freezing point depression verifies ideal cryoscopic behavior up to $x_B = 0.24$. In every trial, following the liquidus crystallization of primary naphthalene crystals, cooling continued until reaching $39.40^\\circ\\text{C}$, where a horizontal isothermal temperature arrest occurred. This arrest marks the simultaneous eutectic solidification of naphthalene and biphenyl.</p>\n\n<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>\n<p>Eutectic SLE phase equilibria govern fractional melt crystallization (Sulzer melt crystallization processes), separation of organic isomer mixtures (ortho/para-dichlorobenzene), metallurgical alloy casting, and formulation of paraffin-fatty acid phase change thermal storage units.</p>\n\n<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>\n<p><strong>Q1: Why does a eutectic mixture exhibit a sharp melting point like a pure compound?</strong><br>\n<em>A1:</em> At the eutectic point, the liquidus curves of both components intersect, and by the Gibbs Phase Rule $F = 2 - 3 + 1 = 0$; with zero degrees of freedom, the system is invariant and solidifies isothermally at constant temperature without a melting range.</p>\n<p><strong>Q2: How can the lever rule be used in the two-phase (liquid + solid A) region?</strong><br>\n<em>A2:</em> The lever rule gives the mass fraction of solid crystals formed: $f_{\\text{solid}} = (x_L - x_{\\text{feed}}) / (x_L - x_S)$, where $x_L$ is the liquidus composition at temperature $T$ and $x_S = 0$ for pure solid A.</p>\n\n<h3>12. Concluding Summary & Verified Engineering Metric</h3>\n<p>Thermal analysis cooling curves successfully established the SLE phase diagram for the binary naphthalene-biphenyl system. The experimental cryoscopic slope $S = 58.5000^\\circ\\text{C}$ and invariant eutectic temperature $T_e = 39.40^\\circ\\text{C}$ confirmed Schröder–van Laar phase equilibrium predictions.</p>"
        },
        {
                "number": 38,
                "slug": "excess-enthalpy-of-mixing-isothermal-titration-calorimetry",
                "title": "Excess Enthalpy of Mixing (H^E) & Heat of Solution via Isothermal Titration Calorimetry (ITC)",
                "shortTitle": "Excess Enthalpy of Mixing ITC",
                "aim": "Operate a power-compensation isothermal titration calorimeter (ITC) at 25.000 °C to measure the heat of mixing during incremental microliter injections of ethanol into water across composition factors x_1·(1 - x_1) from 0.05 to 0.25, evaluate the molar excess enthalpy H^E, and determine the Redlich–Kister excess enthalpy parameter A_0.",
                "inputLabel": "Mixture Composition Product x_1·(1 - x_1)",
                "shortInput": "Composition Factor x_1·x_2",
                "inputUnit": "dimensionless",
                "min": 0.05,
                "max": 0.25,
                "step": 0.04,
                "initial": 0.13,
                "inputDecimals": 2,
                "rawLabel": "Measured Molar Excess Enthalpy H^E",
                "rawUnit": "J/mol",
                "rawDecimals": 1,
                "xAxis": "Composition factor x_1·(1 - x_1)",
                "yAxis": "Molar excess enthalpy H^E (J/mol)",
                "xScale": 1.0,
                "yScale": 1.0,
                "emptyX": 0.15,
                "emptyY": -500.0,
                "targetName": "Redlich–Kister Excess Enthalpy Parameter A_0",
                "target": "-3450.0000",
                "refValue": -3450.0,
                "resultUnit": "J/mol",
                "resultDecimals": 4,
                "resultScale": 1.0,
                "fitEquation": "H^E = A_0 · [x_1 · (1 - x_1)] = -3450.0000 · [x_1 · (1 - x_1)]",
                "intro": "Excess enthalpy of mixing (H^E, also referred to as heat of mixing or excess enthalpy of solution) is a critical thermodynamic property in chemical engineering process design, heat exchanger sizing, reactor thermal management, and flash separation calculations. For an ideal solution, the enthalpy of mixing is strictly zero (ΔH_mix^ideal = 0), meaning mixing pure components at constant temperature and pressure releases or absorbs no heat. In real mixtures, however, breaking like-molecule intermolecular bonds (A-A and B-B) and creating unlike-molecule bonds (A-B) results in an energy imbalance. In the binary ethanol-water system, mixing is exothermic at ambient temperatures (H^E < 0) due to strong cross-association hydrogen bonding between water molecules and ethanol hydroxyl groups, releasing significant heat. The molar excess enthalpy is modeled using the Redlich–Kister polynomial expansion: H^E = x_1 · x_2 · [A_0 + A_1 · (x_1 - x_2) + A_2 · (x_1 - x_2)^2 + ...], where x_1 and x_2 = 1 - x_1 are mole fractions and A_k are temperature-dependent empirical interaction coefficients. In a symmetric first-approximation formulation, excess enthalpy scales directly with the product of the mole fractions: H^E = A_0 · [x_1 · (1 - x_1)], where A_0 is the leading Redlich–Kister parameter. Isothermal Titration Calorimetry (ITC) provides the highest precision method for measuring heats of mixing. Operating under active power-compensation feedback, the ITC sample cell (volume 1.40 mL) is maintained at strictly constant temperature (25.000 ± 0.0001 °C) while automated precision syringe injections (10.0 μL) deliver titrant into the stirred sample cell. Thermal compensation power pulses are integrated to quantify the enthalpy change of each injection with sub-microjoule resolution. In this laboratory experiment, an automated ITC unit measures the heat of mixing across composition products x_1·(1 - x_1) from 0.05 to 0.25 at 25.000 °C to determine the Redlich–Kister parameter A_0 = -3450.0000 J/mol.",
                "modelExtra": "Evaluated using a MicroCal PEAQ-ITC power-compensation isothermal titration calorimeter with 1.40 mL Hastelloy cell, 250 μL injection syringe, and active Peltier feedback control (±0.0001 °C). Calibrated against standard water-water dilution blank and 2-propanol/water heat-of-mixing standards.",
                "apparatus": [
                        {
                                "name": "Power-Compensation Isothermal Titration Calorimeter (ITC)",
                                "purpose": "Maintains sample cell at 25.0000 °C using active thermoelectric feedback, measuring heat pulses down to 0.1 μJ."
                        },
                        {
                                "name": "Coin-Shaped 1.40 mL Hastelloy Sample & Reference Cells",
                                "purpose": "Resists chemical corrosion and provides rapid thermal equilibration with surrounding heat sink."
                        },
                        {
                                "name": "Precision 250 μL Automated Injection Syringe with Integral Stirrer",
                                "purpose": "Dispenses reproducible 10.0 μL liquid titrant pulses while stirring continuously at 750 RPM."
                        },
                        {
                                "name": "Dual Peltier Thermoelectric Cryo-Cooling Jacket",
                                "purpose": "Establishes a steady reference temperature difference of 0.50 °C for power-compensation baseline."
                        },
                        {
                                "name": "Degassing Station with Vacuum and Magnetic Stirring",
                                "purpose": "Degasses all aqueous and organic feedstocks for 15 minutes to prevent injection bubble artifacts."
                        },
                        {
                                "name": "Digital Microbalance and Karl Fischer Coulometer",
                                "purpose": "Verifies moisture content and exact gravimetric purity of feedstock absolute ethanol."
                        }
                ],
                "procedure": [
                        {
                                "title": "Degassing & Cell Thermal Equilibration",
                                "text": "Degas HPLC water and absolute ethanol under vacuum for 15 minutes; fill reference cell with degassed water and establish 25.000 °C baseline."
                        },
                        {
                                "title": "Sample Cell & Syringe Charging",
                                "text": "Load sample cell with 1.40 mL degassed pure water; fill automated injection syringe with 250 μL pure absolute ethanol, purging air bubbles."
                        },
                        {
                                "title": "Injection Parameters Configuration",
                                "text": "Program ITC sequence for 20 successive injections of 10.0 μL with 150 s spacing at 750 RPM stirring speed."
                        },
                        {
                                "title": "Initial Injection & Titration Execution",
                                "text": "Discard initial 0.4 μL pre-injection; initiate automated titration run, logging power compensation response curves (μcal/s) versus time."
                        },
                        {
                                "title": "Peak Integration & Cumulative Enthalpy Calculation",
                                "text": "Integrate power compensation peaks for each injection to determine differential heats of mixing dQ; calculate cumulative molar excess enthalpy H^E."
                        },
                        {
                                "title": "Redlich–Kister Polynomial Regression",
                                "text": "Plot molar excess enthalpy H^E versus composition factor x_1·(1 - x_1); fit linear regression through origin to extract A_0."
                        }
                ],
                "topics": [
                        {
                                "question": "How does power-compensation ITC measure endothermic and exothermic heats of mixing?",
                                "answer": "The ITC applies a small continuous baseline electrical power to the sample cell heater; when an exothermic reaction releases heat, the feedback controller reduces heater power to maintain zero differential temperature, and integrating the power drop yields the heat released."
                        },
                        {
                                "question": "Why is the heat of mixing for ethanol and water exothermic at 25 °C but endothermic at elevated temperatures?",
                                "answer": "At 25 °C, exothermic hydrogen bonding between water and ethanol and hydrophobic hydration dominate; at higher temperatures (above ~60 °C), thermal agitation disrupts hydrogen bonds, and energetic penalties of hydrocarbon disruption dominate, making H^E positive."
                        },
                        {
                                "question": "What is the relationship between excess Gibbs energy G^E and excess enthalpy H^E?",
                                "answer": "The Gibbs–Helmholtz relation states: [∂(G^E / T) / ∂T]_P = -H^E / T^2; this means excess enthalpy is directly responsible for the temperature dependence of liquid-phase activity coefficients."
                        },
                        {
                                "question": "Why must the first injection in an ITC titration experiment be discarded or minimized?",
                                "answer": "During syringe insertion and thermal equilibration, solute diffuses across the needle tip into the cell, making the effective concentration of the initial injection uncertain."
                        },
                        {
                                "question": "How does Redlich–Kister parameter A_0 relate to the infinite-dilution partial molar excess enthalpy?",
                                "answer": "At infinite dilution, the partial molar excess enthalpy of solute 1 in solvent 2 is obtained from the limit H_1^E,inf = lim(x_1->0) [∂(n_t H^E) / ∂n_1] = A_0 + A_1 + A_2 + ...; for a symmetric 1-parameter model, H_1^E,inf = A_0."
                        },
                        {
                                "question": "Why is degassing reagents under vacuum essential before performing ITC measurements?",
                                "answer": "Dissolved air in liquids comes out of solution when heated or mixed, forming microbubbles that create sharp baseline spikes, alter thermal conductivity, and generate severe acoustic cavitation noise."
                        }
                ],
                "precautions": [
                        "Degas all liquids thoroughly prior to loading into the sample cell and syringe to prevent microbubble formation during stirring.",
                        "Inspect the injection needle tip for microscopic burrs or droplets before insertion to ensure accurate injection volumes.",
                        "Verify that the sample cell and syringe are cleaned with ethanol and deionized water and dried between successive runs.",
                        "Allow the calorimeter to achieve a flat, stable baseline drift (< 0.05 μcal/s/h) before initiating automated injection sequences."
                ],
                "quiz": [
                        {
                                "question": "For an ideal solution, the molar excess enthalpy of mixing H^E is:",
                                "options": [
                                        "Equal to R · T",
                                        "Strictly zero",
                                        "Always negative",
                                        "Equal to the enthalpy of vaporization"
                                ],
                                "correct": 1,
                                "explanation": "In an ideal solution, intermolecular interaction energies between all species are identical, meaning no heat is released or absorbed upon mixing (H^E = 0)."
                        },
                        {
                                "question": "An exothermic heat of mixing (H^E < 0) indicates that unlike molecular interactions (A-B) are:",
                                "options": [
                                        "More attractive than the average of like interactions (A-A and B-B)",
                                        "More repulsive than like interactions",
                                        "Completely absent",
                                        "Identical to ideal gas collisions"
                                ],
                                "correct": 0,
                                "explanation": "Exothermic mixing releases thermal energy because forming strong unlike bonds (such as water-ethanol hydrogen bonds) lowers molecular potential energy."
                        },
                        {
                                "question": "The Redlich–Kister expansion models excess enthalpy H^E as a polynomial in:",
                                "options": [
                                        "P / T",
                                        "x_1 · x_2 · Σ [A_k · (x_1 - x_2)^k]",
                                        "ln(x_1 / x_2)",
                                        "exp(-E_a / R T)"
                                ],
                                "correct": 1,
                                "explanation": "The standard Redlich–Kister formulation is H^E = x_1 · x_2 · Σ [A_k · (x_1 - x_2)^k], which automatically satisfies the boundary condition H^E = 0 at pure components."
                        },
                        {
                                "question": "The temperature dependence of liquid-phase activity coefficients is governed by excess enthalpy via:",
                                "options": [
                                        "[∂(ln γ_i) / ∂T]_P = -H_i^E / (R T^2)",
                                        "[∂(ln γ_i) / ∂T]_P = +H_i^E · R T",
                                        "[∂(ln γ_i) / ∂P]_T = H_i^E / (R T)",
                                        "[∂(ln γ_i) / ∂T]_P = 0"
                                ],
                                "correct": 0,
                                "explanation": "From the Gibbs–Helmholtz relation applied to chemical potential, [∂(ln γ_i) / ∂T]_P = -H_i^E / (R T^2)."
                        }
                ],
                "samples": [
                        0.05,
                        0.09,
                        0.13,
                        0.17,
                        0.21,
                        0.25
                ],
                "measureLabel": "Record molar excess enthalpy of mixing",
                "readings": [
                        "comp_factor",
                        "cum_heat",
                        "moles_mixed",
                        "molar_he",
                        "diff_heat",
                        "redlich_kister_term"
                ],
                "theory": "<h3>Thermodynamics of Solution Mixing & Excess Enthalpy</h3>\n<p>The thermodynamic properties of real liquid solutions deviate from ideal solution behavior. For an extensive property $M$, the excess property $M^E$ is defined as the difference between the actual solution property and the property of an ideal solution at the same temperature, pressure, and composition:</p>\n\\[ M^E = M - M^{\\text{ideal}} \\]\n<p>Because an ideal solution exhibits zero enthalpy of mixing ($\\Delta H_{\\text{mix}}^{\\text{ideal}} = 0$), the total enthalpy of mixing is identical to the molar excess enthalpy $H^E$:</p>\n\\[ H^E = \\Delta H_{\\text{mix}} = H_m - \\sum_{i=1}^C x_i H_i^* \\]\n<p>where $H_m$ is the molar enthalpy of the mixture and $H_i^*$ is the molar enthalpy of pure component $i$. From the Gibbs–Helmholtz equation, excess enthalpy directly governs the temperature sensitivity of the excess Gibbs energy and activity coefficients:</p>\n\\[ \\left[ \\frac{\\partial (G^E / T)}{\\partial T} \\right]_P = -\\frac{H^E}{T^2} \\implies \\left[ \\frac{\\partial \\ln \\gamma_i}{\\partial T} \\right]_P = -\\frac{\\bar{H}_i^E}{R T^2} \\]\n<p>where $\\bar{H}_i^E = \\left( \\frac{\\partial(n_t H^E)}{\\partial n_i} \\right)_{T, P, n_{j \\neq i}}$ is the partial molar excess enthalpy of component $i$.</p>\n\n<h3>Redlich–Kister Representation & Power-Compensation ITC</h3>\n<p>The composition dependence of excess enthalpy in binary mixtures is conventionally correlated by the Redlich–Kister expansion:</p>\n\\[ H^E = x_1 \\, x_2 \\sum_{k=0}^{M} A_k (x_1 - x_2)^k = x_1 (1 - x_1) \\left[ A_0 + A_1 (x_1 - x_2) + \\dots \\right] \\]\n<p>For symmetric systems or across moderate composition ranges, the leading parameter $A_0$ captures the predominant magnitude:</p>\n\\[ H^E = A_0 \\cdot [x_1 \\cdot (1 - x_1)] \\]\n<p>In power-compensation ITC, the injection of titrant volume $\\Delta V_{\\text{inj}}$ containing $\\Delta n_i$ moles produces an energy change $q_{\\text{inj}}$ measured by feedback power adjustment:</p>\n\\[ q_{\\text{inj}} = \\int (P_{\\text{baseline}} - P(t)) \\, d t \\]\n<p>Cumulative summation of $q_{\\text{inj}}$ divided by total solution moles yields the molar excess enthalpy $H^E$, allowing direct linear regression against $x_1 (1 - x_1)$ to evaluate $A_0 = -3450.0000\\text{ J/mol}$.</p>",
                "report": "<h3>1. Objective & Practical Significance</h3>\n<p>This laboratory investigation determines the molar excess enthalpy of mixing ($H^E$) for the binary ethanol (1) + water (2) system at $25.000^\\circ\\text{C}$ using power-compensation Isothermal Titration Calorimetry (ITC). Across composition factors $x_1 \\cdot (1 - x_1)$ from $0.05$ to $0.25$, we evaluate exothermic mixing heat pulses, verify the Redlich–Kister linear relationship $H^E = A_0 \\cdot [x_1 (1 - x_1)]$, and determine the leading parameter $A_0 = -3450.0000\\text{ J/mol}$, establishing fundamental enthalpy data for chemical process design.</p>\n\n<h3>2. Governing Transport Equations & Phenomenological Relations</h3>\n<p>The molar excess enthalpy of mixing is modeled by the symmetric Redlich–Kister equation:</p>\n\\[ H^E = A_0 \\cdot [x_1 \\cdot (1 - x_1)] = -3450.0000 \\cdot [x_1 \\cdot (1 - x_1)] \\]\n<p>where $A_0 = -3450.0000\\text{ J/mol}$. The partial molar excess enthalpy of ethanol at infinite dilution is $\\bar{H}_1^{E,\\infty} = A_0 = -3450.0000\\text{ J/mol}$.</p>\n\n<h3>3. Experimental Apparatus & Instrumentation Specification</h3>\n<p>Testing was conducted on a MicroCal PEAQ-ITC power-compensation calorimeter equipped with a $1.40\\text{ mL}$ coin-shaped Hastelloy cell, a $250\\text{ μL}$ precision automated syringe with an integrated paddle stirrer ($750\\text{ RPM}$), and active dual Peltier thermoelectric coolers maintaining cell temperature at $25.0000 \\pm 0.0001^\\circ\\text{C}$.</p>\n\n<h3>4. Standard Operating Procedure & Measurement Protocols</h3>\n<p>HPLC-grade water and absolute ethanol were degassed under vacuum for 15 minutes. The sample cell was filled with $1.40\\text{ mL}$ degassed water, and the syringe was loaded with ethanol. An initial $0.4\\text{ μL}$ pre-injection was executed and discarded. Titrations were conducted via automated $10.0\\text{ μL}$ injections spaced $150\\text{ s}$ apart at $750\\text{ RPM}$. Power compensation thermograms were integrated to determine injection heat pulses and cumulative $H^E$ values across composition factors $0.05, 0.09, 0.13, 0.17, 0.21,$ and $0.25$.</p>\n\n<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>\n<p>Absolute ethanol is flammable. Syringe loading was performed in a well-ventilated enclosure away from spark sources. The Hastelloy calorimeter cell was rinsed with deionized water and methanol after testing. Standard personal protective equipment was worn.</p>\n\n<h3>6. Raw Experimental Observations & Systematic Data Records</h3>\n<p><strong>Simulated demonstration data.</strong> The following calorimetric measurements were recorded at $T = 25.000^\\circ\\text{C}$ ($P = 101.325\\text{ kPa}$):</p>\n<table>\n<thead>\n<tr><th>Run</th><th>Composition Factor $x_1(1-x_1)$</th><th>Equivalent $x_{\\text{EtOH}}$ (mol/mol)</th><th>Cumulative Heat $Q$ (J)</th><th>Solution Moles $n_t$ (mmol)</th><th>Measured $H^E$ (J/mol)</th><th>Fitted $H^E$ (J/mol)</th></tr>\n</thead>\n<tbody>\n<tr><td>1</td><td>0.05</td><td>0.0528</td><td>-13.41</td><td>77.74</td><td>-172.5</td><td>-172.5</td></tr>\n<tr><td>2</td><td>0.09</td><td>0.1011</td><td>-24.16</td><td>77.81</td><td>-310.5</td><td>-310.5</td></tr>\n<tr><td>3</td><td>0.13</td><td>0.1539</td><td>-34.93</td><td>77.88</td><td>-448.5</td><td>-448.5</td></tr>\n<tr><td>4</td><td>0.17</td><td>0.2127</td><td>-45.74</td><td>77.98</td><td>-586.5</td><td>-586.5</td></tr>\n<tr><td>5</td><td>0.21</td><td>0.2811</td><td>-56.59</td><td>78.11</td><td>-724.5</td><td>-724.5</td></tr>\n<tr><td>6</td><td>0.25</td><td>0.5000</td><td>-67.57</td><td>78.34</td><td>-862.5</td><td>-862.5</td></tr>\n</tbody>\n</table>\n\n<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>\n<p>Linear regression of molar excess enthalpy $H^E$ versus composition factor $x_1 \\cdot (1 - x_1)$ yields:</p>\n\\[ H^E = -3450.00000 \\cdot [x_1 \\cdot (1 - x_1)] + 0.00000 \\]\n<p>with coefficient of determination $R^2 = 1.000000$. The experimental slope $A_0 = -3450.00000\\text{ J/mol}$ matches the Redlich–Kister target parameter ($-3450.0000$) with $0.00\\%$ deviation. At equimolar composition ($x_1 = 0.50$, $x_1 (1 - x_1) = 0.25$), the maximum excess enthalpy released is:</p>\n\\[ H^E_{\\text{max}} = -3450.0000 \\times 0.25 = -862.50\\text{ J/mol} \\]\n<p>The negative sign confirms that mixing ethanol and water at $25^\\circ\\text{C}$ is strongly exothermic.</p>\n\n<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>\n<p>ITC power baseline noise is $\\pm 0.005\\text{ μW}$, injection volume reproducibility is $\\pm 0.05\\text{ μL}$ ($0.5\\%$), and cell temperature stability is $\\pm 0.0001^\\circ\\text{C}$. Propagating through peak integration yields an experimental uncertainty in $A_0$ of $\\pm 18.5\\text{ J/mol}$ ($0.54\\%$), reporting $A_0 = -3450 \\pm 19\\text{ J/mol}$.</p>\n\n<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>\n<p>The exothermic excess enthalpy ($H^E < 0$) arises from strong hydrogen bond formation between water protons and ethanol oxygen lone pairs, which releases more energy than is required to disrupt bulk ethanol-ethanol and water-water interactions. Maximum heat release of $-862.5\\text{ J/mol}$ occurs near $x_{\\text{EtOH}} \\approx 0.5$, reflecting optimal stoichiometry for cross-species hydrogen-bonded networks.</p>\n\n<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>\n<p>Accurate $H^E$ data are required for design of blending tank cooling coils in pharmaceutical formulation, heat exchanger design in ethanol distillation columns, and non-ideal thermodynamic enthalpy calculations in chemical flowsheeting software.</p>\n\n<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>\n<p><strong>Q1: Why does the excess enthalpy of mixing influence the temperature dependence of VLE?</strong><br>\n<em>A1:</em> By the Gibbs–Helmholtz relation $[\\partial(\\ln \\gamma_i) / \\partial T]_P = -\\bar{H}_i^E / (R T^2)$; non-zero excess enthalpy dictates how activity coefficients shift with boiling temperature, determining the shape of VLE envelope curves.</p>\n<p><strong>Q2: Why is the sample cell coin-shaped in modern ITC designs?</strong><br>\n<em>A2:</em> A coin-shaped cell maximizes the surface-area-to-volume ratio and reduces path length to the thermoelectric Peltier heat sink, enabling rapid thermal response time ($< 10\\text{ s}$) and sensitive power feedback.</p>\n\n<h3>12. Concluding Summary & Verified Engineering Metric</h3>\n<p>Isothermal Titration Calorimetry successfully quantified the excess enthalpy of mixing for ethanol-water at $25.000^\\circ\\text{C}$. The experimental Redlich–Kister interaction parameter $A_0 = -3450.0000\\text{ J/mol}$ established an equimolar heat release of $-862.50\\text{ J/mol}$, confirming exothermic hydrogen bonding.</p>"
        },
        {
                "number": 39,
                "slug": "gas-solubility-henry-law-pressure-decay",
                "title": "Gas Solubility in Liquids & Henry's Law Constant Evaluation via Pressure-Decay Isochoric Manometry",
                "shortTitle": "Gas Solubility Henry's Law",
                "aim": "Determine the solubility and Henry's law constant for carbon dioxide (CO_2) in pure deionized water at 25.00 °C using a constant-volume isochoric pressure-decay autoclave across initial gas pressures P_0 from 1.0 to 6.0 bar, monitor equilibrium pressure drop ΔP, evaluate the moles of dissolved gas, and extract the Henry's law solubility constant.",
                "inputLabel": "Initial Autoclave Gas Pressure P_0",
                "shortInput": "Initial Pressure P_0",
                "inputUnit": "bar",
                "min": 1.0,
                "max": 6.0,
                "step": 1.0,
                "initial": 3.0,
                "inputDecimals": 1,
                "rawLabel": "Equilibrium Dissolved Gas Content n_d",
                "rawUnit": "mol",
                "rawDecimals": 4,
                "xAxis": "Initial gas pressure P_0 (bar)",
                "yAxis": "Dissolved gas content n_d (mol)",
                "xScale": 1.0,
                "yScale": 1.0,
                "emptyX": 3.5,
                "emptyY": 0.12,
                "targetName": "Henry's Law Solubility Constant K_H·V_L",
                "target": "0.0340",
                "refValue": 0.034,
                "resultUnit": "mol/bar",
                "resultDecimals": 4,
                "resultScale": 1.0,
                "fitEquation": "n_d = S · P_0 = 0.0340 · P_0",
                "intro": "Gas solubility in liquids is a core physical phenomenon across chemical engineering, environmental science, beverage carbonation, bioprocessing, and carbon capture and sequestration (CCS). When a sparingly soluble gas contacts a liquid solvent at constant temperature, gas molecules transport across the liquid-gas interface until thermodynamic equilibrium is established between the chemical potential of the gas species in the vapor phase and its chemical potential in the dissolved liquid phase: μ_i^V(T, P, y_i) = μ_i^L(T, P, x_i). In dilute solutions, this equilibrium is governed by Henry's Law, originally formulated by William Henry in 1803: P_i = H_i · x_i, where P_i is the partial pressure of the gas above the solution, x_i is the equilibrium liquid mole fraction, and H_i is Henry's law volatility constant (bar). Alternatively, in volumetric process engineering, Henry's law is expressed in terms of dissolved molar concentration: C_d = K_H · P_i, where K_H is Henry's law solubility constant (mol/(L·bar)). For a closed isochoric (constant-volume) autoclave cell containing liquid solvent volume V_L (1.00 L) and head-space gas volume V_G, the total moles of gas initially charged at pressure P_0 is: n_0 = (P_0 · V_G) / (z_0 · R T). As gas dissolves into the degassed liquid, the head-space pressure decays until reaching equilibrium pressure P_eq. By mass balance over the closed cell, the moles of dissolved gas n_d equals the difference between initial and final gas-phase moles: n_d = n_0 - n_eq = [V_G / (R T)] · [(P_0 / z_0) - (P_eq / z_eq)]. In the linear Henry's law regime, equilibrium dissolved gas content is directly proportional to initial charging pressure: n_d = S · P_0, where the solubility slope S = K_H · V_L = 0.0340 mol/bar. For CO_2 dissolving into 1.00 L of water at 25.00 °C, K_H = 0.0340 mol/(L·bar) (equivalent to Henry's volatility constant H = 1630 bar). In this laboratory experiment, a 316 stainless steel isochoric pressure-decay cell equipped with a magnetic-drive hollow-shaft gas-entraining impeller and piezoresistive pressure transmitter measures CO_2 dissolution across initial pressures from 1.0 to 6.0 bar to evaluate n_d and determine S = 0.0340 mol/bar.",
                "modelExtra": "Evaluated using a 2.0 L 316SS Buchi high-pressure autoclave reactor with hollow-shaft gas-entrainment Rushton impeller (1000 RPM) and Rosemount 3051S precision pressure transmitter (±0.005 bar). Pure CO_2 (99.99%) dissolving into 1.000 L degassed deionized water at 25.000 ± 0.01 °C.",
                "apparatus": [
                        {
                                "name": "2.0 L 316 Stainless Steel High-Pressure Autoclave",
                                "purpose": "Isochoric cell rated to 10.0 MPa with internal volume calibration (1.00 L liquid, 1.00 L gas)."
                        },
                        {
                                "name": "Magnetic-Drive Hollow-Shaft Gas-Entraining Impeller",
                                "purpose": "Pumps head-space gas continuously into liquid at 1000 RPM to maximize mass transfer area without seals."
                        },
                        {
                                "name": "Precision Piezoresistive Pressure Transmitter (0 to 10 bar)",
                                "purpose": "Logs autoclave head-space pressure decay with ±0.001 bar resolution and 10 Hz sampling rate."
                        },
                        {
                                "name": "Constant-Temperature Water Recirculating Jacket",
                                "purpose": "Maintains reactor temperature strictly at 25.000 ± 0.01 °C to eliminate thermal pressure fluctuations."
                        },
                        {
                                "name": "Ultra-Pure Carbon Dioxide (CO_2) Cylinder & Dual-Stage Regulator",
                                "purpose": "Supplies dry 99.99% CO_2 gas up to 6.00 bar through an automated charging solenoid valve."
                        },
                        {
                                "name": "High-Vacuum Degassing Station with Liquid Nitrogen Trap",
                                "purpose": "Degasses DI water down to < 1.0 kPa prior to charging to ensure zero background dissolved inert gases."
                        }
                ],
                "procedure": [
                        {
                                "title": "Water Degassing & Reactor Priming",
                                "text": "Degas exactly 1000.0 mL of DI water by boiling under vacuum; transfer into autoclave under vacuum; start jacket temperature control at 25.00 °C."
                        },
                        {
                                "title": "System Evacuation & Thermal Baseline",
                                "text": "Evacuate head-space to residual pressure < 0.05 bar; verify isothermal stability at 25.000 ± 0.01 °C for 20 minutes."
                        },
                        {
                                "title": "Gas Injection to Target Initial Pressure (P_0 = 1.0 bar)",
                                "text": "Open CO_2 supply valve to rapidly charge head-space to P_0 = 1.00 bar; isolate charging valve immediately; record initial pressure P_0."
                        },
                        {
                                "title": "Agitation & Pressure Decay Logging",
                                "text": "Engage magnetic hollow-shaft stirrer at 1000 RPM; log pressure decay P(t) until steady equilibrium P_eq is maintained for 15 minutes."
                        },
                        {
                                "title": "Dissolved Moles Calculation via Real Gas EOS",
                                "text": "Compute initial moles n_0 and final vapor moles n_eq using Peng–Robinson or virial compressibility z; calculate dissolved moles n_d."
                        },
                        {
                                "title": "Pressure Progression Protocol",
                                "text": "Repeat evacuation, priming, and charging across P_0 = 2.0, 3.0, 4.0, 5.0, and 6.0 bar; plot n_d versus P_0 to extract Henry's law slope S."
                        }
                ],
                "topics": [
                        {
                                "question": "How does temperature affect the solubility of gases in liquids?",
                                "answer": "For most common gases (CO_2, O_2, N_2) dissolving in water, dissolution is an exothermic process (ΔH_sol < 0); according to Le Chatelier's principle and the van 't Hoff equation d(ln K_H)/dT = -ΔH_sol/(R T^2), increasing temperature decreases gas solubility."
                        },
                        {
                                "question": "What is the difference between Henry's volatility constant H_i and solubility constant K_H?",
                                "answer": "Henry's volatility constant H_i (bar) relates partial pressure to mole fraction via P_i = H_i · x_i (higher H means lower solubility); Henry's solubility constant K_H (mol/(L·bar)) relates concentration to partial pressure via C_i = K_H · P_i (higher K_H means higher solubility); they are reciprocally related by K_H = 1 / (H_i · V_m,solvent)."
                        },
                        {
                                "question": "Why does a hollow-shaft gas-entraining impeller accelerate equilibrium in pressure-decay cells?",
                                "answer": "The high-speed rotation of the hollow impeller generates a localized low-pressure zone at the impeller blades, sucking gas from the head-space through the hollow shaft and dispersing it as millions of microbubbles, creating massive interfacial contact area a (m^2/m^3)."
                        },
                        {
                                "question": "Under what conditions does Henry's Law fail?",
                                "answer": "Henry's Law fails at very high pressures (> 20–50 bar) where gas fugacity deviates strongly from pressure and liquid non-ideality occurs; for highly soluble gases that chemically react and ionize extensively (e.g. HCl or NH_3); and when solute liquid concentrations exceed ~2–3 mol%."
                        },
                        {
                                "question": "How does the chemical hydration of dissolved CO_2 affect its apparent solubility?",
                                "answer": "Dissolved molecular CO_2(aq) undergoes reversible hydration to carbonic acid: CO_2(aq) + H_2O <-> H_2CO_3 <-> H^+ + HCO_3^-; however, at 25 °C and neutral pH, over 99.8% remains as physical dissolved molecular CO_2(aq), making Henry's physical law strictly valid."
                        },
                        {
                                "question": "How does water salinity ('salting-out' effect) alter Henry's law constant?",
                                "answer": "Dissolved ionic salts (e.g. NaCl) attract polar water molecules into tight hydration shells, reducing the concentration of free water molecules available to dissolve nonpolar or weakly polar gas molecules; this increases the gas activity coefficient and decreases solubility (described by the Setchenow equation)."
                        }
                ],
                "precautions": [
                        "Ensure the autoclave closure bolts are tightened in a diametrically opposed cross pattern with a calibrated torque wrench before pressurization.",
                        "Verify all dissolved atmospheric air (O_2 and N_2) is removed by vacuum boiling prior to introducing CO_2 to prevent mixed gas partial pressure errors.",
                        "Operate within the pressure vessel maximum allowable working pressure (MAWP = 10.0 MPa), and verify pressure relief rupture disc integrity.",
                        "Maintain stirring at constant 1000 RPM until pressure remains strictly flat for at least 15 minutes to guarantee complete phase equilibrium."
                ],
                "quiz": [
                        {
                                "question": "Henry's Law states that at constant temperature, the solubility of a gas in a liquid is:",
                                "options": [
                                        "Inversely proportional to gas partial pressure",
                                        "Directly proportional to gas partial pressure",
                                        "Proportional to the square of gas pressure",
                                        "Independent of gas pressure"
                                ],
                                "correct": 1,
                                "explanation": "Henry's law states that at equilibrium, the mass or concentration of dissolved gas is directly proportional to the partial pressure of the gas above the liquid (C = K_H · P)."
                        },
                        {
                                "question": "As water temperature rises from 25 °C to 80 °C, the solubility of CO_2 in water:",
                                "options": [
                                        "Increases exponentially",
                                        "Remains unchanged",
                                        "Decreases significantly",
                                        "Drops to zero at exactly 50 °C"
                                ],
                                "correct": 2,
                                "explanation": "Because gas dissolution in water is exothermic (ΔH_sol < 0), increasing temperature shifts equilibrium toward the gas phase, decreasing solubility."
                        },
                        {
                                "question": "In an isochoric pressure-decay experiment, the moles of gas dissolved are determined by:",
                                "options": [
                                        "Direct gravimetric weighing of the autoclave",
                                        "Subtracting the equilibrium head-space gas moles from initial charged gas moles",
                                        "Measuring the pH shift of the solution",
                                        "Collecting the evolved vapor over mercury"
                                ],
                                "correct": 1,
                                "explanation": "In a closed constant-volume vessel, mass conservation dictates that dissolved gas moles equal initial gas moles minus final vapor head-space moles (n_d = n_0 - n_eq)."
                        },
                        {
                                "question": "The units of Henry's law solubility constant K_H in concentration-pressure form are typically:",
                                "options": [
                                        "bar / mol",
                                        "mol / (L · bar)",
                                        "L / (mol · s)",
                                        "dimensionless"
                                ],
                                "correct": 1,
                                "explanation": "In concentration form C = K_H · P, K_H has units of concentration divided by pressure: mol/(L·bar) or mol/(m^3·Pa)."
                        }
                ],
                "samples": [
                        1.0,
                        2.0,
                        3.0,
                        4.0,
                        5.0,
                        6.0
                ],
                "measureLabel": "Record equilibrium dissolved gas moles",
                "readings": [
                        "p_init",
                        "p_equil",
                        "delta_p",
                        "dissolved_moles",
                        "henry_kh",
                        "liquid_mole_frac"
                ],
                "theory": "<h3>Phase Equilibrium Thermodynamics of Dilute Gas-Liquid Solutions</h3>\n<p>Phase equilibrium between a gas phase ($V$) and a liquid solution ($L$) containing dissolved gas solute $i$ requires equality of chemical potentials:</p>\n\\[ \\mu_i^V(T, P, y_i) = \\mu_i^L(T, P, x_i) \\implies \\hat{f}_i^V(T, P, y_i) = \\hat{f}_i^L(T, P, x_i) \\]\n<p>In the gas phase, fugacity is related to total pressure and vapor composition by the fugacity coefficient $\\hat{\\Phi}_i^V$:</p>\n\\[ \\hat{f}_i^V = y_i \\, P \\, \\hat{\\Phi}_i^V \\]\n<p>In the liquid phase, for a sparingly soluble gas solute ($x_i \\to 0$), fugacity is represented using Henry's law reference state at infinite dilution:</p>\n\\[ \\hat{f}_i^L = x_i \\, \\gamma_i^* \\, H_{i,s}(T, P) \\]\n<p>where $H_{i,s}$ is Henry's law constant of solute $i$ in solvent $s$, and $\\gamma_i^*$ is the asymmetric activity coefficient ($\\lim_{x_i \\to 0} \\gamma_i^* = 1.0$). At moderate pressures ($P \\le 10\\text{ bar}$), $\\hat{\\Phi}_i^V \\approx 1.00$, $\\gamma_i^* \\approx 1.00$, and the Poynting correction is unity, producing Henry's law:</p>\n\\[ P_i = H_{i,s} \\, x_i \\]\n<p>In terms of volumetric liquid molar concentration $C_d = n_d / V_L$:</p>\n\\[ C_d = K_H \\, P_i \\implies n_d = K_H \\, V_L \\, P_i \\]\n\n<h3>Isochoric Pressure-Decay Mass Conservation</h3>\n<p>In an isochoric autoclave of total volume $V_{\\text{cell}}$ containing liquid volume $V_L$ and head-space gas volume $V_G = V_{\\text{cell}} - V_L$, pure gas is initially charged to pressure $P_0$. Initial gas moles charged:</p>\n\\[ n_0 = \\frac{P_0 \\, V_G}{z_0 \\, R T} \\]\n<p>As gas dissolves, head-space pressure decays to equilibrium pressure $P_{\\text{eq}}$. The final equilibrium gas moles remaining in the head-space is:</p>\n\\[ n_{\\text{eq}} = \\frac{P_{\\text{eq}} \\, V_G}{z_{\\text{eq}} \\, R T} \\]\n<p>By total mass conservation within the closed vessel, the equilibrium dissolved gas content $n_d$ is:</p>\n\\[ n_d = n_0 - n_{\\text{eq}} = \\frac{V_G}{R T} \\left( \\frac{P_0}{z_0} - \\frac{P_{\\text{eq}}}{z_{\\text{eq}}} \\right) \\]\n\n<h3>Linear Solubility Regression & Henry's Parameter</h3>\n<p>Because the equilibrium partial pressure $P_{\\text{eq}}$ is related to initial pressure $P_0$ by the system volume ratio and solubility constant ($P_{\\text{eq}} = P_0 / [1 + K_H R T (V_L / V_G)]$), the dissolved gas moles $n_d$ scales linearly with initial charging pressure $P_0$:</p>\n\\[ n_d = S \\cdot P_0 = (K_H \\cdot V_L) \\cdot P_0 = 0.0340 \\cdot P_0 \\]\n<p>Plotting dissolved moles $n_d$ versus initial pressure $P_0$ yields a straight line through the origin with slope $S = 0.0340\\text{ mol/bar}$, confirming Henry's law solubility constant $K_H = 0.0340\\text{ mol/(L}\\cdot\\text{bar)}$ for $V_L = 1.00\\text{ L}$.</p>",
                "report": "<h3>1. Objective & Practical Significance</h3>\n<p>This laboratory investigation determines the solubility and Henry's law constant for carbon dioxide ($CO_2$) in deionized water at $25.00^\\circ\\text{C}$ using an isochoric pressure-decay autoclave ($V_L = 1.000\\text{ L}$, $V_G = 1.000\\text{ L}$). Across initial charging pressures $P_0 = 1.0$ to $6.0\\text{ bar}$, we monitor pressure decay to dynamic equilibrium, calculate dissolved gas moles $n_d$ via real gas mass conservation, verify Henry's linear law $n_d = S \\cdot P_0$, determine the solubility slope $S = 0.0340\\text{ mol/bar}$, and evaluate Henry's solubility constant $K_H = 0.0340\\text{ mol/(L}\\cdot\\text{bar)}$ (volatility constant $H = 1630\\text{ bar}$).</p>\n\n<h3>2. Governing Transport Equations & Phenomenological Relations</h3>\n<p>Mass conservation in the closed isochoric cell dictates: $n_d = n_0 - n_{\\text{eq}} = \\frac{V_G}{R T} \\left( \\frac{P_0}{z_0} - \\frac{P_{\\text{eq}}}{z_{\\text{eq}}} \\right)$. The linear Henry's law model is:</p>\n\\[ n_d = S \\cdot P_0 = 0.0340 \\cdot P_0 \\]\n<p>where $S = K_H \\cdot V_L = 0.0340\\text{ mol/bar}$. Henry's volatility constant on a mole-fraction basis is: $H = \\frac{\\rho_{\\text{water}} / M_{\\text{water}}}{K_H} = \\frac{55.42}{0.0340} = 1630\\text{ bar}$.</p>\n\n<h3>3. Experimental Apparatus & Instrumentation Specification</h3>\n<p>The system comprises a $2.000\\text{ L}$ 316 stainless steel autoclave ($10.0\\text{ MPa}$ rating) fitted with a magnetic-drive hollow-shaft gas-entraining impeller ($1000\\text{ RPM}$), a Rosemount 3051S piezoresistive pressure transmitter ($\\pm 0.001\\text{ bar}$), a thermostatically jacketed bath holding $25.000 \\pm 0.01^\\circ\\text{C}$, and high-purity $CO_2$ ($99.99\\%$) supply cylinder.</p>\n\n<h3>4. Standard Operating Procedure & Measurement Protocols</h3>\n<p>Exactly $1000.0\\text{ mL}$ of vacuum-degassed deionized water was charged into the autoclave. The remaining $1.000\\text{ L}$ head-space was evacuated to $< 0.02\\text{ bar}$. The cell was isolated and charged with pure $CO_2$ to initial pressure $P_0 = 1.00\\text{ bar}$. Agitation was engaged at $1000\\text{ RPM}$, and pressure decay was recorded at $2\\text{ Hz}$ until equilibrium $P_{\\text{eq}}$ was maintained for 15 minutes. The protocol was repeated for $P_0 = 2.0, 3.0, 4.0, 5.0,$ and $6.0\\text{ bar}$.</p>\n\n<h3>5. Safety Analysis, Hazard Mitigation & Personal Protection</h3>\n<p>High-pressure gas vessels present pneumatic hazards. The autoclave was equipped with a burst disc rated to $8.0\\text{ MPa}$ vented to an exterior duct. Pressurization was regulated through a dual-stage stainless steel manifold. Safety glasses, face shields, and steel-toed footwear were mandatory.</p>\n\n<h3>6. Raw Experimental Observations & Systematic Data Records</h3>\n<p><strong>Simulated demonstration data.</strong> The following pressure-decay measurements were logged at $T = 25.000^\\circ\\text{C}$ ($V_L = 1.000\\text{ L}$, $V_G = 1.000\\text{ L}$):</p>\n<table>\n<thead>\n<tr><th>Run</th><th>Initial Pressure $P_0$ (bar)</th><th>Initial Moles $n_0$ (mol)</th><th>Equilibrium $P_{\\text{eq}}$ (bar)</th><th>Final Vapor $n_{\\text{eq}}$ (mol)</th><th>Dissolved Moles $n_d$ (mol)</th><th>Liquid Concentration $C_d$ (mol/L)</th></tr>\n</thead>\n<tbody>\n<tr><td>1</td><td>1.0</td><td>0.0406</td><td>0.1626</td><td>0.0066</td><td>0.0340</td><td>0.0340</td></tr>\n<tr><td>2</td><td>2.0</td><td>0.0813</td><td>0.3252</td><td>0.0133</td><td>0.0680</td><td>0.0680</td></tr>\n<tr><td>3</td><td>3.0</td><td>0.1221</td><td>0.4878</td><td>0.0201</td><td>0.1020</td><td>0.1020</td></tr>\n<tr><td>4</td><td>4.0</td><td>0.1630</td><td>0.6504</td><td>0.0270</td><td>0.1360</td><td>0.1360</td></tr>\n<tr><td>5</td><td>5.0</td><td>0.2040</td><td>0.8130</td><td>0.0340</td><td>0.1700</td><td>0.1700</td></tr>\n<tr><td>6</td><td>6.0</td><td>0.2452</td><td>0.9756</td><td>0.0412</td><td>0.2040</td><td>0.2040</td></tr>\n</tbody>\n</table>\n\n<h3>7. Quantitative Mathematical Analysis & Regression Models</h3>\n<p>Linear regression of dissolved gas moles $n_d$ versus initial pressure $P_0$ yields:</p>\n\\[ n_d = 0.03400 \\cdot P_0 + 0.00000 \\]\n<p>with coefficient of determination $R^2 = 1.000000$ and zero intercept. The experimental slope $S = 0.03400\\text{ mol/bar}$ matches calibration target ($0.0340$) with $0.00\\%$ deviation. Evaluating Henry's law parameters for $V_L = 1.000\\text{ L}$:</p>\n\\[ K_H = \\frac{S}{V_L} = \\frac{0.03400\\text{ mol/bar}}{1.000\\text{ L}} = 0.03400\\text{ mol/(L}\\cdot\\text{bar)} \\]\n<p>Converting to mole-fraction basis ($n_{\\text{water}} = 1000 / 18.015 = 55.51\\text{ mol}$):</p>\n\\[ H = \\frac{P_{\\text{eq}}}{x_{\\text{CO2}}} = \\frac{55.51}{0.0340} = 1632.6\\text{ bar} \\]\n\n<h3>8. Rigorous Error Analysis & Uncertainty Propagation</h3>\n<p>Pressure transmitter uncertainty is $\\pm 0.001\\text{ bar}$, liquid volume measurement error is $\\pm 0.002\\text{ L}$, and temperature stability is $\\pm 0.01^\\circ\\text{C}$. Propagating through real gas EOS mass balances yields an uncertainty in $K_H$ of $\\pm 0.00028\\text{ mol/(L}\\cdot\\text{bar)}$ ($0.82\\%$), reporting $K_H = 0.0340 \\pm 0.0003\\text{ mol/(L}\\cdot\\text{bar)}$.</p>\n\n<h3>9. Engineering Discussion & Phenomenological Interpretation</h3>\n<p>The excellent linearity up to $P_0 = 6.0\\text{ bar}$ demonstrates that $CO_2$ behaves as a classic Henry's law solute in water at $25^\\circ\\text{C}$. Equilibrium pressure decay was rapid (achieving $99\\%$ saturation in $< 8\\text{ minutes}$), demonstrating the exceptional gas dispersion of the hollow-shaft gas-entraining impeller. Dissolved $CO_2$ concentration reached $0.204\\text{ mol/L}$ ($8.98\\text{ g/L}$) at $P_0 = 6.0\\text{ bar}$.</p>\n\n<h3>10. Industrial Scale-Up & Unit Operation Applications</h3>\n<p>Henry's law constants for $CO_2$ govern design of industrial carbonation systems in soft drink bottling, sizing of absorber columns in chemical carbon capture (amine scrubbing and physical solvents like Selexol), and deep saline aquifer sequestration modeling.</p>\n\n<h3>11. Self-Assessment Conceptual Questions & Model Answers</h3>\n<p><strong>Q1: Why does dissolved $CO_2$ concentration depend on the partial pressure rather than total system pressure?</strong><br>\n<em>A1:</em> Dalton's and Henry's laws dictate that chemical potential driving force depends strictly on the partial pressure (fugacity) of the specific gas species, independent of inert background gas pressures.</p>\n<p><strong>Q2: How does the gas compressibility factor $z$ affect mass balance calculations at high pressures?</strong><br>\n<em>A2:</em> At high pressures, repulsive and attractive intermolecular forces cause real gas molar volume to deviate from the ideal gas law ($P V = z n R T$); omitting $z$ introduces errors of several percent in calculated initial and final head-space moles.</p>\n\n<h3>12. Concluding Summary & Verified Engineering Metric</h3>\n<p>Isochoric pressure-decay manometry successfully measured $CO_2$ gas solubility in water at $25.00^\\circ\\text{C}$. The experimental solubility slope $S = 0.0340\\text{ mol/bar}$ confirmed Henry's law solubility constant $K_H = 0.0340\\text{ mol/(L}\\cdot\\text{bar)}$ and volatility constant $H = 1632.6\\text{ bar}$.</p>"
        }
]
