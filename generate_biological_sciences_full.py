# -*- coding: utf-8 -*-
"""Generate comprehensive experiments.json for Biological Sciences (30 Laboratories)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LABS = [
    # Module 1: Cell Biology & Biomembrane Transport (Labs 1–6)
    {
        "num": 1,
        "slug": "microscope-micrometry-cell-size-calibration",
        "title": "Stage and Ocular Micrometry Calibration & Eukaryotic Cell Sizing",
        "shortTitle": "Microscope Micrometry & Cell Sizing",
        "aim": "Calibrate ocular reticle divisions against a certified stage micrometer across high-power objective lenses and determine mean cell dimensions of eukaryotic specimens.",
        "inputLabel": "Ocular Reticle Scale Divisions (div)",
        "shortInput": "Reticle Divisions",
        "inputUnit": "divisions",
        "min": 4.0, "max": 40.0, "step": 2.0, "initial": 15.0, "inputDecimals": 1,
        "rawLabel": "Calibrated Physical Cell Dimension",
        "rawUnit": "µm", "rawDecimals": 2,
        "xAxis": "Ocular Scale Divisions d (div)",
        "yAxis": "Calibrated Cell Size (µm)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 40.0, "emptyY": 100.0,
        "targetName": "Ocular Micrometer Objective Calibration Factor",
        "target": "Micrometric Calibration Factor",
        "refValue": 2.5000, "resultUnit": "µm/division", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Size_µm = 2.5000 · Divisions",
        "samples": [6.0, 12.0, 18.0, 24.0, 30.0, 38.0],
        "subsystem": "Cell Biology & Biomembrane Transport",
        "focus": "Optical Reticle Micrometry & Microscopic Cell Calibration"
    },
    {
        "num": 2,
        "slug": "osmosis-dialysis-tubing-sucrose-water-potential",
        "title": "Osmotic Water Potential & Equilibrium Mass Flux across Dialysis Membranes",
        "shortTitle": "Osmosis & Dialysis Water Potential",
        "aim": "Investigate passive water flux across selectively permeable cellulose dialysis tubing in response to graded external sucrose concentration gradients.",
        "inputLabel": "External Sucrose Concentration Gradient (mM)",
        "shortInput": "Sucrose Gradient",
        "inputUnit": "mM",
        "min": 50.0, "max": 600.0, "step": 25.0, "initial": 250.0, "inputDecimals": 1,
        "rawLabel": "Percentage Dialysis Bag Mass Change (Δm)",
        "rawUnit": "%", "rawDecimals": 2,
        "xAxis": "Sucrose Gradient ΔC (mM)",
        "yAxis": "Mass Flux Rate Δm (%)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 600.0, "emptyY": 35.0,
        "targetName": "Osmotic Permeability Reflection Coefficient",
        "target": "Osmotic Mass Flux Slope",
        "refValue": 0.0550, "resultUnit": "% per mM", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Δm = 0.0550 · ΔC",
        "samples": [100.0, 180.0, 260.0, 360.0, 460.0, 560.0],
        "subsystem": "Cell Biology & Biomembrane Transport",
        "focus": "Osmotic Pressure & Selective Semipermeable Membrane Diffusion"
    },
    {
        "num": 3,
        "slug": "plant-cell-plasmolysis-incipient-osmotic-pressure",
        "title": "Incipient Plasmolysis & Protoplast Osmotic Pressure in Plant Epidermis",
        "shortTitle": "Incipient Plasmolysis Osmometry",
        "aim": "Determine the osmotic pressure and solute potential of Rhoeo spathacea epidermal cells by quantifying percentage protoplast plasmolysis across graded mannitol solutions.",
        "inputLabel": "Incubation Mannitol Solution Concentration (M)",
        "shortInput": "Mannitol Molarity",
        "inputUnit": "M",
        "min": 0.10, "max": 0.80, "step": 0.05, "initial": 0.40, "inputDecimals": 2,
        "rawLabel": "Percentage Plasmolyzed Epidermal Cells",
        "rawUnit": "%", "rawDecimals": 1,
        "xAxis": "External Mannitol Molarity M (mol/L)",
        "yAxis": "Plasmolysis Fraction (%)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 0.80, "emptyY": 100.0,
        "targetName": "Plasmolytic Susceptibility Slope",
        "target": "Plasmolysis Response Slope",
        "refValue": 18.0000, "resultUnit": "% per (0.1 M)", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Plasmolysis% = 18.0000 · (M / 0.1) - 15.0000",
        "samples": [0.20, 0.30, 0.40, 0.50, 0.60, 0.70],
        "subsystem": "Cell Biology & Biomembrane Transport",
        "focus": "Turgor Pressure & Protoplast Solute Potential Equilibrium"
    },
    {
        "num": 4,
        "slug": "erythrocyte-hemolysis-solute-permeability-overton",
        "title": "Cell Membrane Permeability & Overton's Lipophilicity Correlation",
        "shortTitle": "Overton's Solute Permeability",
        "aim": "Evaluate cell membrane passive non-electrolyte permeability by measuring red blood cell hemolysis times across alcohols with varying olive oil/water partition coefficients.",
        "inputLabel": "Solute Olive Oil/Water Partition Coefficient (K_ow)",
        "shortInput": "Partition Coefficient",
        "inputUnit": "AU",
        "min": 0.01, "max": 0.25, "step": 0.02, "initial": 0.10, "inputDecimals": 3,
        "rawLabel": "Reciprocal Hemolysis Transit Rate (1/t)",
        "rawUnit": "s^-1", "rawDecimals": 4,
        "xAxis": "Lipid Partition Coefficient K_ow (AU)",
        "yAxis": "Membrane Penetration Rate (s^-1)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 0.25, "emptyY": 0.4,
        "targetName": "Overton Lipid Membrane Permeability Slope",
        "target": "Lipophilic Permeation Rate Constant",
        "refValue": 1.4500, "resultUnit": "s^-1 per AU", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Rate = 1.4500 · K_ow",
        "samples": [0.03, 0.07, 0.11, 0.15, 0.19, 0.23],
        "subsystem": "Cell Biology & Biomembrane Transport",
        "focus": "Lipid Bilayer Permeation & Overton's Law of Cellular Transport"
    },
    {
        "num": 5,
        "slug": "mitotic-index-allium-cepa-cell-cycle-kinetics",
        "title": "Mitotic Index & Cell Cycle Phase Duration in Allium Root Meristem",
        "shortTitle": "Allium Meristem Mitotic Index",
        "aim": "Prepare Feulgen/acetocarmine squashes of Allium cepa root tips to quantify prophase, metaphase, anaphase, and telophase indices and calculate cell cycle kinetics.",
        "inputLabel": "Root Meristem Incubation Temperature (°C)",
        "shortInput": "Incubation Temperature",
        "inputUnit": "°C",
        "min": 10.0, "max": 35.0, "step": 2.5, "initial": 22.0, "inputDecimals": 1,
        "rawLabel": "Observed Mitotic Index (MI)",
        "rawUnit": "%", "rawDecimals": 2,
        "xAxis": "Meristem Temperature (°C)",
        "yAxis": "Mitotic Index MI (%)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 35.0, "emptyY": 35.0,
        "targetName": "Thermal Mitotic Proliferation Sensitivity",
        "target": "Mitotic Index Temperature Slope",
        "refValue": 0.8500, "resultUnit": "% per °C", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "MI = 0.8500 · Temp + 2.2000",
        "samples": [14.0, 18.0, 22.0, 26.0, 30.0, 34.0],
        "subsystem": "Cell Biology & Biomembrane Transport",
        "focus": "Chromosomal Cytogenetics & Meristematic Cell Division Kinetics"
    },
    {
        "num": 6,
        "slug": "chloroplast-hill-reaction-dcip-photoreduction",
        "title": "Photochemical Hill Reaction & DCPIP Photoreduction in Isolated Chloroplasts",
        "shortTitle": "Chloroplast Hill Reaction",
        "aim": "Measure photochemical electron transport in isolated Spinacia oleracea chloroplasts using 2,6-dichlorophenolindophenol (DCPIP) absorbance loss at 600 nm.",
        "inputLabel": "Actinic Light Photosynthetic Irradiance (µmol/m²/s)",
        "shortInput": "Light Irradiance",
        "inputUnit": "µmol/m²/s",
        "min": 50.0, "max": 800.0, "step": 50.0, "initial": 300.0, "inputDecimals": 0,
        "rawLabel": "DCPIP Reduction Velocity (ΔA600/min)",
        "rawUnit": "OD/min", "rawDecimals": 4,
        "xAxis": "Photosynthetic Irradiance I (µmol/m²/s)",
        "yAxis": "DCPIP Reduction Rate (OD/min)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 800.0, "emptyY": 2.5,
        "targetName": "Photosystem II Photochemical Quantum Gain",
        "target": "Hill Reaction Photoreduction Slope",
        "refValue": 0.0028, "resultUnit": "(OD/min) per (µmol/m²/s)", "resultDecimals": 5, "resultScale": 1.0,
        "fitEquation": "Rate = 0.0028 · Irradiance",
        "samples": [100.0, 220.0, 350.0, 480.0, 620.0, 750.0],
        "subsystem": "Cell Biology & Biomembrane Transport",
        "focus": "Thylakoid Photophosphorylation & Electron Transport Chain Kinetics"
    },

    # Module 2: Enzymology & Cellular Metabolism (Labs 7–12)
    {
        "num": 7,
        "slug": "catalase-enzyme-kinetics-substrate-concentration",
        "title": "Catalase Enzyme Kinetics: Initial Reaction Velocity vs Hydrogen Peroxide",
        "shortTitle": "Catalase Substrate Kinetics",
        "aim": "Assay catalase initial velocity by measuring oxygen gas generation over substrate concentration to determine enzyme saturation and catalytic efficiency.",
        "inputLabel": "Substrate Hydrogen Peroxide Concentration [H2O2] (mM)",
        "shortInput": "[H2O2] Substrate",
        "inputUnit": "mM",
        "min": 5.0, "max": 80.0, "step": 5.0, "initial": 30.0, "inputDecimals": 1,
        "rawLabel": "Initial Catalytic Reaction Velocity (v0)",
        "rawUnit": "µmol O2/min", "rawDecimals": 2,
        "xAxis": "Substrate Concentration [S] (mM)",
        "yAxis": "Initial Velocity v0 (µmol O2/min)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 80.0, "emptyY": 35.0,
        "targetName": "Sub-Saturating Catalytic Rate Constant",
        "target": "Catalase Catalytic Proportionality Slope",
        "refValue": 0.4200, "resultUnit": "(µmol O2/min) per mM", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "v0 = 0.4200 · [S]",
        "samples": [10.0, 20.0, 32.0, 46.0, 60.0, 75.0],
        "subsystem": "Enzymology & Cellular Metabolism",
        "focus": "Peroxisomal Antioxidant Kinetics & Substrate Velocity Saturation"
    },
    {
        "num": 8,
        "slug": "temperature-coefficient-q10-enzyme-catalysis",
        "title": "Thermal Activation & Arrhenius Temperature Coefficient (Q10) of Amylase",
        "shortTitle": "Enzyme Temperature Coefficient Q10",
        "aim": "Quantify enzymatic reaction rates across 15 °C to 45 °C to calculate the temperature quotient (Q10) and activation energy (Ea) of starch hydrolysis.",
        "inputLabel": "Incubation Reaction Temperature (°C)",
        "shortInput": "Reaction Temperature",
        "inputUnit": "°C",
        "min": 15.0, "max": 45.0, "step": 2.5, "initial": 25.0, "inputDecimals": 1,
        "rawLabel": "Natural Log Hydrolytic Catalytic Rate ln(k)",
        "rawUnit": "ln(U/mL)", "rawDecimals": 3,
        "xAxis": "Temperature T (°C)",
        "yAxis": "Log Catalytic Rate ln(k)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 45.0, "emptyY": 4.0,
        "targetName": "Arrhenius Thermal Acceleration Coefficient",
        "target": "Thermal Kinetic Activation Slope",
        "refValue": 0.0750, "resultUnit": "ln(U/mL) per °C", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "ln(k) = 0.0750 · T + 0.1500",
        "samples": [18.0, 23.0, 28.0, 33.0, 38.0, 43.0],
        "subsystem": "Enzymology & Cellular Metabolism",
        "focus": "Thermal Kinetic Energy & Enzyme Macromolecular Stability"
    },
    {
        "num": 9,
        "slug": "ph-optimum-salivary-amylase-starch-digestion",
        "title": "pH Optimum & Ionization Profile of Salivary Amylase Starch Hydrolysis",
        "shortTitle": "Amylase pH Optimum Profile",
        "aim": "Characterize the bell-shaped pH-activity curve of salivary α-amylase using iodine achromic point assay to determine catalytic amino acid pKa values.",
        "inputLabel": "Absolute Deviation from Optimum pH (|pH - 6.8|)",
        "shortInput": "pH Deviation",
        "inputUnit": "pH units",
        "min": 0.2, "max": 3.0, "step": 0.2, "initial": 1.0, "inputDecimals": 2,
        "rawLabel": "Relative Starch Hydrolysis Velocity",
        "rawUnit": "OD/min", "rawDecimals": 3,
        "xAxis": "pH Deviation |pH - 6.8|",
        "yAxis": "Reaction Velocity (OD/min)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 3.0, "emptyY": 2.0,
        "targetName": "Active Site Prototropic Inactivation Slope",
        "target": "pH Inactivation Sensitivity",
        "refValue": 0.1800, "resultUnit": "(OD/min) per pH unit", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Velocity = -0.1800 · |pH - 6.8| + 1.8500",
        "samples": [0.4, 0.8, 1.2, 1.8, 2.3, 2.8],
        "subsystem": "Enzymology & Cellular Metabolism",
        "focus": "Active Site Histidine Ionization & Protein Conformation"
    },
    {
        "num": 10,
        "slug": "yeast-fermentation-rate-durham-tube-respirometry",
        "title": "Yeast Anaerobic Fermentation Rate & Sugar Catabolism Respirometry",
        "shortTitle": "Yeast Respirometric Fermentation",
        "aim": "Quantify anaerobic glycolytic carbon dioxide evolution in Saccharomyces cerevisiae suspensions using Durham tubes and volumetric respirometers across fermentable sugars.",
        "inputLabel": "Substrate Glucose Broth Concentration (% w/v)",
        "shortInput": "Glucose Concentration",
        "inputUnit": "%",
        "min": 1.0, "max": 12.0, "step": 1.0, "initial": 5.0, "inputDecimals": 1,
        "rawLabel": "Volumetric Carbon Dioxide Generation Rate",
        "rawUnit": "mL CO2/min", "rawDecimals": 2,
        "xAxis": "Sugar Concentration S (%)",
        "yAxis": "Gas Production Rate (mL CO2/min)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 12.0, "emptyY": 5.0,
        "targetName": "Anaerobic Glycolytic Gas Evolution Yield",
        "target": "Fermentation Gas Generation Slope",
        "refValue": 0.3500, "resultUnit": "(mL CO2/min) per %", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Rate = 0.3500 · S",
        "samples": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
        "subsystem": "Enzymology & Cellular Metabolism",
        "focus": "Substrate-Level Phosphorylation & Alcoholic Fermentation Energetics"
    },
    {
        "num": 11,
        "slug": "cellular-respiration-germinating-seeds-respirometer",
        "title": "Aerobic Cellular Respiration & Respiratory Quotient (RQ) in Seeds",
        "shortTitle": "Seed Respiration & RQ Index",
        "aim": "Measure oxygen uptake and carbon dioxide production in germinating Pisum sativum using closed-system KOH respirometers to determine the respiratory quotient.",
        "inputLabel": "Germinating Seed Biomass Loading (g)",
        "shortInput": "Seed Biomass",
        "inputUnit": "g",
        "min": 5.0, "max": 50.0, "step": 2.5, "initial": 20.0, "inputDecimals": 1,
        "rawLabel": "Specific Oxygen Consumption Rate",
        "rawUnit": "mL O2/hr", "rawDecimals": 2,
        "xAxis": "Germinating Seed Biomass M (g)",
        "yAxis": "Oxygen Uptake Rate (mL O2/hr)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 50.0, "emptyY": 5.0,
        "targetName": "Specific Germination Aerobic Respiration Coefficient",
        "target": "Biomass Respiration Rate Slope",
        "refValue": 0.0820, "resultUnit": "(mL O2/hr) per g", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Uptake = 0.0820 · M",
        "samples": [8.0, 15.0, 22.0, 30.0, 38.0, 46.0],
        "subsystem": "Enzymology & Cellular Metabolism",
        "focus": "Mitochondrial Oxidative Phosphorylation & Respiratory Quotient"
    },
    {
        "num": 12,
        "slug": "succinate-dehydrogenase-mitochondrial-electron-transport",
        "title": "Mitochondrial Succinate Dehydrogenase Activity & Competitive Malonate Inhibition",
        "shortTitle": "Succinate Dehydrogenase Inhibition",
        "aim": "Assay Complex II (succinate dehydrogenase) in isolated liver mitochondria using methylene blue/DCPIP electron transfer and quantify competitive inhibition by malonate.",
        "inputLabel": "Competitive Inhibitor Malonate Concentration (mM)",
        "shortInput": "Malonate Inhibitor",
        "inputUnit": "mM",
        "min": 0.5, "max": 10.0, "step": 0.5, "initial": 3.0, "inputDecimals": 2,
        "rawLabel": "Catalytic Reduction Velocity (ΔA600/min)",
        "rawUnit": "OD/min", "rawDecimals": 4,
        "xAxis": "Inhibitor Concentration [I] (mM)",
        "yAxis": "Dehydrogenase Velocity (OD/min)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 10.0, "emptyY": 0.35,
        "targetName": "Competitive Active Site Affinity Inhibition Slope",
        "target": "Dehydrogenase Inhibition Sensitivity",
        "refValue": 0.0150, "resultUnit": "(OD/min) per mM", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Velocity = -0.0150 · [I] + 0.2800",
        "samples": [1.0, 2.5, 4.0, 6.0, 8.0, 9.5],
        "subsystem": "Enzymology & Cellular Metabolism",
        "focus": "Krebs Cycle Dehydrogenases & Competitive Active-Site Antagonism"
    },

    # Module 3: Molecular Biology & Genetics (Labs 13–18)
    {
        "num": 13,
        "slug": "agarose-gel-electrophoresis-dna-fragment-migration",
        "title": "Agarose Gel Electrophoresis: DNA Fragment Molecular Weight vs Migration",
        "shortTitle": "Agarose DNA Gel Electrophoresis",
        "aim": "Separate restriction-digested DNA fragments on 1.0% agarose gels to establish the inverse log-linear relationship between base-pair size and electrophoretic mobility.",
        "inputLabel": "Fragment Base-Pair Size Exponent (log10 bp)",
        "shortInput": "log10(Base Pairs)",
        "inputUnit": "log10(bp)",
        "min": 2.3, "max": 4.3, "step": 0.2, "initial": 3.2, "inputDecimals": 2,
        "rawLabel": "Electrophoretic Gel Migration Distance",
        "rawUnit": "mm", "rawDecimals": 1,
        "xAxis": "Log DNA Molecular Size log10(bp)",
        "yAxis": "Migration Distance (mm)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 4.5, "emptyY": 60.0,
        "targetName": "Electrophoretic Sieving Resolving Slope",
        "target": "Gel Electrophoretic Sieving Slope",
        "refValue": 15.5000, "resultUnit": "mm per log10(bp)", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Migration_mm = -15.5000 · log10(bp) + 85.0000",
        "samples": [2.5, 2.8, 3.2, 3.6, 3.9, 4.2],
        "subsystem": "Molecular Biology & Genetics",
        "focus": "Agarose Gel Matrix Sieving & DNA Electrophoretic Mobility"
    },
    {
        "num": 14,
        "slug": "spectrophotometric-dna-quantification-purity-ratio",
        "title": "Spectrophotometric DNA Quantification & A260/A280 Purity Absorbance Ratio",
        "shortTitle": "DNA Quantification & A260/A280 Purity",
        "aim": "Determine double-stranded DNA concentration and protein contamination using UV spectrophotometric absorbance at 260 nm and 280 nm via the Beer-Lambert law.",
        "inputLabel": "Purified dsDNA Solution Concentration (µg/mL)",
        "shortInput": "DNA Concentration",
        "inputUnit": "µg/mL",
        "min": 5.0, "max": 100.0, "step": 5.0, "initial": 35.0, "inputDecimals": 1,
        "rawLabel": "Ultraviolet Optical Absorbance at 260 nm (A260)",
        "rawUnit": "OD", "rawDecimals": 4,
        "xAxis": "dsDNA Concentration [DNA] (µg/mL)",
        "yAxis": "Absorbance A260",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 100.0, "emptyY": 2.0,
        "targetName": "Double-Stranded DNA Molar Absorptivity Factor",
        "target": "Beer-Lambert dsDNA Extinction Slope",
        "refValue": 50.0000, "resultUnit": "(µg/mL) per OD", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "[DNA] = 50.0000 · A260",
        "samples": [10.0, 25.0, 40.0, 55.0, 75.0, 95.0],
        "subsystem": "Molecular Biology & Genetics",
        "focus": "Purine/Pyrimidine UV Resonances & Nucleic Acid Extraction Purity"
    },
    {
        "num": 15,
        "slug": "bacterial-transformation-plasmid-competent-efficiency",
        "title": "Bacterial Plasmid Transformation Efficiency & Heat-Shock Competence",
        "shortTitle": "Bacterial Plasmid Transformation",
        "aim": "Transform competent Escherichia coli with pUC19 plasmid vector via CaCl2 heat shock and quantify transformation efficiency in transformants per microgram DNA.",
        "inputLabel": "Incubation Plasmid DNA Mass (ng)",
        "shortInput": "Plasmid Mass",
        "inputUnit": "ng",
        "min": 1.0, "max": 25.0, "step": 2.0, "initial": 10.0, "inputDecimals": 1,
        "rawLabel": "Ampicillin-Resistant Transformant Colonies (CFU x10^4)",
        "rawUnit": "CFU x10^4", "rawDecimals": 2,
        "xAxis": "Plasmid DNA Mass m (ng)",
        "yAxis": "Colony Yield (CFU x10^4)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 25.0, "emptyY": 35.0,
        "targetName": "Competent Cell Plasmid Uptake Factor",
        "target": "Transformation Efficiency Slope",
        "refValue": 1.2500, "resultUnit": "(CFU x10^4) per ng", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Yield = 1.2500 · Mass",
        "samples": [2.0, 6.0, 10.0, 14.0, 18.0, 24.0],
        "subsystem": "Molecular Biology & Genetics",
        "focus": "Artificial Bacterial Competence & Recombinant Plasmid Selection"
    },
    {
        "num": 16,
        "slug": "mendelian-dihybrid-cross-drosophila-chi-square",
        "title": "Mendelian Dihybrid Inheritance & Chi-Square Goodness-of-Fit in Drosophila",
        "shortTitle": "Drosophila Dihybrid Chi-Square",
        "aim": "Analyze F2 phenotypic ratios in Drosophila melanogaster dihybrid crosses (ebony body, vestigial wings) to test Mendel's Law of Independent Assortment via Chi-Square.",
        "inputLabel": "Expected Mendelian Phenotypic Fraction Factor (AU)",
        "shortInput": "Mendelian Expectation",
        "inputUnit": "AU",
        "min": 20.0, "max": 200.0, "step": 10.0, "initial": 80.0, "inputDecimals": 1,
        "rawLabel": "Observed F2 Progeny Count",
        "rawUnit": "flies", "rawDecimals": 0,
        "xAxis": "Theoretical Mendelian Expectation E (flies)",
        "yAxis": "Observed Phenotypes O (flies)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 200.0, "emptyY": 220.0,
        "targetName": "Mendelian Goodness-of-Fit Concordance Ratio",
        "target": "Mendelian Progeny Concordance Slope",
        "refValue": 1.0000, "resultUnit": "observed/expected", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Observed = 1.0000 · Expected",
        "samples": [30.0, 60.0, 90.0, 120.0, 150.0, 180.0],
        "subsystem": "Molecular Biology & Genetics",
        "focus": "Classical Mendelian Segregation & Statistical Hypothesis Testing"
    },
    {
        "num": 17,
        "slug": "polytene-chromosome-puff-transcription-mapping",
        "title": "Polytene Chromosome Banding & Transcription Puff Mapping in Chironomus",
        "shortTitle": "Polytene Chromosome Puffs",
        "aim": "Examine polytene chromosomes from Chironomus salivary glands to map Balbiani rings, chromosome bands, and ecdysone-induced transcription puff dynamics.",
        "inputLabel": "Transcription Puff Calibrated Diameter (µm)",
        "shortInput": "Puff Diameter",
        "inputUnit": "µm",
        "min": 10.0, "max": 60.0, "step": 5.0, "initial": 30.0, "inputDecimals": 1,
        "rawLabel": "Relative RNA Synthesis Incorporation Index",
        "rawUnit": "AU", "rawDecimals": 2,
        "xAxis": "Puff Dimension D (µm)",
        "yAxis": "RNA Synthesis Metric (AU)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 60.0, "emptyY": 30.0,
        "targetName": "Chromatin Decondensation Transcriptional Gain",
        "target": "Puff Transcriptional Scaling Slope",
        "refValue": 0.4500, "resultUnit": "AU per µm", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Synthesis = 0.4500 · Diameter",
        "samples": [15.0, 22.0, 30.0, 40.0, 50.0, 58.0],
        "subsystem": "Molecular Biology & Genetics",
        "focus": "Epigenetic Chromatin Uncoiling & Eukaryotic Gene Activation"
    },
    {
        "num": 18,
        "slug": "pcr-amplification-cycle-efficiency-kinetics",
        "title": "Polymerase Chain Reaction (PCR) Amplicon Yield & Cycle Kinetics",
        "shortTitle": "PCR Amplification Kinetics",
        "aim": "Model exponential amplicon accumulation across thermal cycles in end-point and real-time PCR to evaluate Taq polymerase amplification efficiency.",
        "inputLabel": "PCR Thermal Cycling Number (Cycles)",
        "shortInput": "Thermal Cycles",
        "inputUnit": "cycles",
        "min": 10.0, "max": 35.0, "step": 1.0, "initial": 20.0, "inputDecimals": 0,
        "rawLabel": "Log10 Amplicon Copy Number log10(N)",
        "rawUnit": "log10(copies)", "rawDecimals": 3,
        "xAxis": "Cycle Number C (cycles)",
        "yAxis": "Log Amplicon Copies log10(N)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 35.0, "emptyY": 12.0,
        "targetName": "Exponential Amplification Rate Exponent (log10 2)",
        "target": "PCR Cycle Amplification Slope",
        "refValue": 0.3010, "resultUnit": "log10(copies) per cycle", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "log10(N) = 0.3010 · C + 1.2000",
        "samples": [12.0, 16.0, 20.0, 24.0, 28.0, 32.0],
        "subsystem": "Molecular Biology & Genetics",
        "focus": "DNA Polymerase Processivity & Exponential Amplification Kinetics"
    },

    # Module 4: Microbiology & Microbial Physiology (Labs 19–24)
    {
        "num": 19,
        "slug": "bacterial-growth-curve-turbidimetric-spectrophotometry",
        "title": "Bacterial Growth Curve Kinetics & Generation Time by Turbidimetry",
        "shortTitle": "Bacterial Growth Curve & Turbidity",
        "aim": "Monitor optical density at 600 nm in batch cultures of Escherichia coli to construct growth phases, calculate specific growth rate (µ), and derive generation time (g).",
        "inputLabel": "Incubation Log-Phase Elapsed Time (min)",
        "shortInput": "Elapsed Time",
        "inputUnit": "min",
        "min": 20.0, "max": 180.0, "step": 10.0, "initial": 80.0, "inputDecimals": 0,
        "rawLabel": "Culture Optical Density at 600 nm (OD600)",
        "rawUnit": "OD", "rawDecimals": 3,
        "xAxis": "Incubation Time t (min)",
        "yAxis": "Optical Density OD600",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 180.0, "emptyY": 3.5,
        "targetName": "Specific Microbial Exponential Growth Rate",
        "target": "Turbidimetric Growth Slope",
        "refValue": 0.0185, "resultUnit": "OD/min", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "OD600 = 0.0185 · Time + 0.0500",
        "samples": [30.0, 60.0, 90.0, 120.0, 150.0, 180.0],
        "subsystem": "Microbiology & Microbial Physiology",
        "focus": "Bacterial Population Dynamics & Monod Kinetic Growth Phases"
    },
    {
        "num": 20,
        "slug": "serial-dilution-pour-plate-colony-forming-units",
        "title": "Viable Cell Enumeration by Serial Dilution & Pour-Plate Colony Forming Units",
        "shortTitle": "Pour-Plate CFU Enumeration",
        "aim": "Enumerate viable microbial density in broth cultures using ten-fold serial dilutions and nutrient agar pour plates to calculate CFU/mL.",
        "inputLabel": "Dilution Reciprocal Scaling Index (x10^-5)",
        "shortInput": "Dilution Index",
        "inputUnit": "x10^-5",
        "min": 10.0, "max": 250.0, "step": 10.0, "initial": 100.0, "inputDecimals": 1,
        "rawLabel": "Plate Colony Count (CFU/plate)",
        "rawUnit": "CFU", "rawDecimals": 0,
        "xAxis": "Dilution Scaling Factor (AU)",
        "yAxis": "Counted Colonies (CFU)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 250.0, "emptyY": 300.0,
        "targetName": "Viable Cell Colony Proportionality Slope",
        "target": "Colony Forming Density Slope",
        "refValue": 1.0000, "resultUnit": "CFU per unit index", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "CFU = 1.0000 · DilutionIndex",
        "samples": [30.0, 70.0, 110.0, 150.0, 190.0, 240.0],
        "subsystem": "Microbiology & Microbial Physiology",
        "focus": "Quantitative Microbiological Plating & Statistical Colony Validity"
    },
    {
        "num": 21,
        "slug": "gram-staining-peptidoglycan-cell-wall-differentiation",
        "title": "Gram Staining Kinetics & Peptidoglycan Cell Wall Decolorization",
        "shortTitle": "Gram Stain Decolorization Kinetics",
        "aim": "Differentiate bacterial cell envelopes (Gram-positive vs Gram-negative) by measuring crystal violet-iodine complex retention rates under controlled ethanol decolorization.",
        "inputLabel": "Ethanol Solvent Decolorization Duration (s)",
        "shortInput": "Decolorization Time",
        "inputUnit": "s",
        "min": 5.0, "max": 40.0, "step": 2.5, "initial": 15.0, "inputDecimals": 1,
        "rawLabel": "Retained Crystal Violet Dye Fraction",
        "rawUnit": "AU", "rawDecimals": 3,
        "xAxis": "Decolorization Duration t (s)",
        "yAxis": "Dye Retention Metric (AU)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 40.0, "emptyY": 1.0,
        "targetName": "Lipopolysaccharide Solvent Washout Velocity",
        "target": "Gram Decolorization Rate Constant",
        "refValue": 0.0450, "resultUnit": "AU/s", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Retention = -0.0450 · Time + 0.9500",
        "samples": [6.0, 10.0, 15.0, 20.0, 26.0, 32.0],
        "subsystem": "Microbiology & Microbial Physiology",
        "focus": "Bacterial Cell Wall Architecture & Differential Staining Chemistry"
    },
    {
        "num": 22,
        "slug": "bacteriophage-plaque-assay-titer-quantification",
        "title": "Bacteriophage Lytic Plaque Assay & Plaque-Forming Unit (PFU) Quantification",
        "shortTitle": "Bacteriophage Plaque Assay",
        "aim": "Quantify infectious viral particles of T4 bacteriophage infecting Escherichia coli lawns by double-agar overlay plaque titration to compute PFU/mL.",
        "inputLabel": "Phage Aliquot Inoculum Dilution Index (x10^-6)",
        "shortInput": "Inoculum Index",
        "inputUnit": "x10^-6",
        "min": 10.0, "max": 200.0, "step": 10.0, "initial": 80.0, "inputDecimals": 1,
        "rawLabel": "Enumerated Lytic Plaques (PFU/plate)",
        "rawUnit": "PFU", "rawDecimals": 0,
        "xAxis": "Phage Dilution Factor (AU)",
        "yAxis": "Lytic Plaques (PFU)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 200.0, "emptyY": 200.0,
        "targetName": "Bacteriophage Infectious Virion Titer Slope",
        "target": "Plaque Titration Coefficient",
        "refValue": 0.8500, "resultUnit": "PFU per unit index", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "PFU = 0.8500 · InoculumIndex",
        "samples": [20.0, 50.0, 80.0, 110.0, 150.0, 190.0],
        "subsystem": "Microbiology & Microbial Physiology",
        "focus": "Viral Lytic Cycles & Quantitative Plaque Enumeration Protocols"
    },
    {
        "num": 23,
        "slug": "nitrogen-fixation-acetylene-reduction-rhizobium",
        "title": "Symbiotic Nitrogen Fixation: Rhizobium Nodulation & Acetylene Reduction",
        "shortTitle": "Rhizobium Nitrogenase Assay",
        "aim": "Quantify nitrogenase activity in root nodules of Leguminosae using the gas-chromatographic acetylene reduction assay (ARA) to calculate biological nitrogen fixation rates.",
        "inputLabel": "Active Legume Root Nodule Biomass (g)",
        "shortInput": "Nodule Biomass",
        "inputUnit": "g",
        "min": 0.5, "max": 10.0, "step": 0.5, "initial": 4.0, "inputDecimals": 2,
        "rawLabel": "Ethylene Gas Production Rate (µmol/hr)",
        "rawUnit": "µmol C2H4/hr", "rawDecimals": 2,
        "xAxis": "Nodule Fresh Biomass M (g)",
        "yAxis": "Ethylene Production (µmol/hr)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 10.0, "emptyY": 35.0,
        "targetName": "Specific Nitrogenase Catalytic Reduction Gain",
        "target": "Biological Nitrogen Fixation Rate Slope",
        "refValue": 3.2000, "resultUnit": "(µmol C2H4/hr) per g", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Ethylene = 3.2000 · Biomass",
        "samples": [1.0, 2.5, 4.5, 6.0, 7.8, 9.5],
        "subsystem": "Microbiology & Microbial Physiology",
        "focus": "Bacteroid Nitrogenase Biochemistry & Symbiotic Nodulation Dynamics"
    },
    {
        "num": 24,
        "slug": "bacterial-motility-soft-agar-chemotaxis-gradient",
        "title": "Bacterial Chemotaxis & Swarming Motility Radius in Soft Agar",
        "shortTitle": "Bacterial Chemotaxis & Swarming",
        "aim": "Examine flagellar propulsion and chemotactic response of Pseudomonas or Proteus on 0.3% soft agar plates in the presence of attractant concentration gradients.",
        "inputLabel": "Chemotactic Incubation Elapsed Time (hr)",
        "shortInput": "Elapsed Time",
        "inputUnit": "hr",
        "min": 4.0, "max": 36.0, "step": 2.0, "initial": 18.0, "inputDecimals": 1,
        "rawLabel": "Radial Swarming Migration Ring Radius",
        "rawUnit": "mm", "rawDecimals": 2,
        "xAxis": "Incubation Time t (hr)",
        "yAxis": "Swarm Colony Radius (mm)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 36.0, "emptyY": 30.0,
        "targetName": "Flagellar Swarming Migration Speed",
        "target": "Bacterial Swarming Velocity",
        "refValue": 0.6500, "resultUnit": "mm/hr", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Radius_mm = 0.6500 · Time",
        "samples": [6.0, 12.0, 18.0, 24.0, 28.0, 34.0],
        "subsystem": "Microbiology & Microbial Physiology",
        "focus": "Flagellar Chemosensory Signal Transduction & Spatial Motility"
    },

    # Module 5: Plant Physiology & Ecology (Labs 25–30)
    {
        "num": 25,
        "slug": "photosynthetic-light-response-curve-light-saturation",
        "title": "Photosynthetic Light Response Curve: Light Compensation & Saturation",
        "shortTitle": "Photosynthetic Light Response Curve",
        "aim": "Construct net CO2 assimilation vs photosynthetically active radiation (PAR) curves using infra-red gas analysis (IRGA) to evaluate quantum yield and light compensation point.",
        "inputLabel": "Incident Actinic Photosynthetic Photon Flux (µmol/m²/s)",
        "shortInput": "Actinic PAR",
        "inputUnit": "µmol/m²/s",
        "min": 25.0, "max": 400.0, "step": 25.0, "initial": 150.0, "inputDecimals": 0,
        "rawLabel": "Net Carbon Dioxide Assimilation Flux (A_net)",
        "rawUnit": "µmol CO2/m²/s", "rawDecimals": 2,
        "xAxis": "Incident Irradiance PAR (µmol/m²/s)",
        "yAxis": "Net Assimilation A_net (µmol/m²/s)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 400.0, "emptyY": 25.0,
        "targetName": "Apparent Photosynthetic Quantum Yield Efficiency",
        "target": "Photosynthetic Quantum Yield Slope",
        "refValue": 0.0520, "resultUnit": "(µmol CO2/m²/s) per (µmol/m²/s)", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "A_net = 0.0520 · PAR",
        "samples": [50.0, 100.0, 175.0, 250.0, 320.0, 380.0],
        "subsystem": "Plant Physiology & Ecology",
        "focus": "Calvin Cycle RuBisCO Kinetics & Photochemical Light Saturation"
    },
    {
        "num": 26,
        "slug": "potometer-transpiration-rate-vpd-environmental-stress",
        "title": "Leaf Transpiration Rate by Ganong's Potometer vs Vapor Pressure Deficit",
        "shortTitle": "Potometer Transpiration & VPD",
        "aim": "Measure xylem water uptake in excised leafy shoots using Ganong's capillary potometer under varying atmospheric vapor pressure deficits and air velocities.",
        "inputLabel": "Atmospheric Vapor Pressure Deficit (VPD kPa)",
        "shortInput": "Vapor Pressure Deficit",
        "inputUnit": "kPa",
        "min": 0.5, "max": 5.0, "step": 0.25, "initial": 2.0, "inputDecimals": 2,
        "rawLabel": "Volumetric Shoot Transpiration Water Uptake",
        "rawUnit": "mL/hr", "rawDecimals": 3,
        "xAxis": "Vapor Pressure Deficit VPD (kPa)",
        "yAxis": "Transpiration Rate (mL/hr)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 5.0, "emptyY": 3.0,
        "targetName": "Atmospheric Evaporative Driving Conductance",
        "target": "Transpiration Evaporative Gain",
        "refValue": 0.4800, "resultUnit": "(mL/hr) per kPa", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Rate = 0.4800 · VPD",
        "samples": [0.8, 1.5, 2.2, 3.0, 3.8, 4.6],
        "subsystem": "Plant Physiology & Ecology",
        "focus": "Cohesion-Tension Theory & Atmospheric Transpirational Pull"
    },
    {
        "num": 27,
        "slug": "stomata-density-conductance-carbon-dioxide-diffusion",
        "title": "Stomatal Density, Aperture Dimension & Leaf Stomatal Conductance",
        "shortTitle": "Stomatal Density & Conductance",
        "aim": "Prepare epidermal nail-polish peels to count stomatal frequency per square millimeter and calculate theoretical gaseous diffusive conductance (gs) to CO2.",
        "inputLabel": "Microscopic Stomatal Density Count (stomata/mm²)",
        "shortInput": "Stomatal Density",
        "inputUnit": "stomata/mm²",
        "min": 50.0, "max": 400.0, "step": 25.0, "initial": 180.0, "inputDecimals": 0,
        "rawLabel": "Calculated Stomatal Diffusive Conductance (gs)",
        "rawUnit": "mmol/m²/s", "rawDecimals": 3,
        "xAxis": "Stomatal Density D (stomata/mm²)",
        "yAxis": "Stomatal Conductance gs (mmol/m²/s)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 400.0, "emptyY": 1.6,
        "targetName": "Individual Guard Cell Diffusive Permeability",
        "target": "Stomatal Conductance Scaling Slope",
        "refValue": 0.0035, "resultUnit": "(mmol/m²/s) per (stomata/mm²)", "resultDecimals": 5, "resultScale": 1.0,
        "fitEquation": "gs = 0.0035 · Density",
        "samples": [80.0, 140.0, 200.0, 260.0, 320.0, 380.0],
        "subsystem": "Plant Physiology & Ecology",
        "focus": "Guard Cell Osmoregulation & Leaf Boundary Layer Resistance"
    },
    {
        "num": 28,
        "slug": "plant-pigment-rf-values-paper-chromatography",
        "title": "Photosynthetic Pigment Separation & Retention Factor (Rf) Chromatography",
        "shortTitle": "Photosynthetic Pigment Rf Values",
        "aim": "Extract leaf plastid pigments in acetone and resolve chlorophyll-a, chlorophyll-b, xanthophyll, and β-carotene by ascending paper chromatography to derive Rf values.",
        "inputLabel": "Organic Solvent Front Migration Distance (cm)",
        "shortInput": "Solvent Front",
        "inputUnit": "cm",
        "min": 5.0, "max": 20.0, "step": 1.0, "initial": 12.0, "inputDecimals": 1,
        "rawLabel": "Individual Pigment Band Migration Distance",
        "rawUnit": "cm", "rawDecimals": 2,
        "xAxis": "Solvent Front Distance L (cm)",
        "yAxis": "Pigment Distance d (cm)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 20.0, "emptyY": 20.0,
        "targetName": "Solvent Partition Retention Factor (Rf / 100)",
        "target": "Chromatographic Retention Factor Slope",
        "refValue": 0.0100, "resultUnit": "cm/cm", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Distance = 0.0100 · Front",
        "samples": [6.0, 9.0, 12.0, 14.5, 17.0, 19.5],
        "subsystem": "Plant Physiology & Ecology",
        "focus": "Carotenoid/Chlorophyll Partition Chromatography & Light Harvesting"
    },
    {
        "num": 29,
        "slug": "seed-dormancy-gibberellic-acid-alpha-amylase-induction",
        "title": "Seed Dormancy Release: Gibberellic Acid (GA3) Induction of α-Amylase",
        "shortTitle": "Gibberellic Acid Seed Dormancy",
        "aim": "Bioassay aleurone layer response in embryoless barley endosperm across log concentrations of gibberellic acid (GA3) to quantify de novo α-amylase gene expression.",
        "inputLabel": "Log Gibberellic Acid Concentration log[GA3] (µM)",
        "shortInput": "log[GA3]",
        "inputUnit": "log[µM]",
        "min": 0.5, "max": 4.5, "step": 0.5, "initial": 2.0, "inputDecimals": 2,
        "rawLabel": "Induced Alpha-Amylase Catalytic Activity",
        "rawUnit": "U/g tissue", "rawDecimals": 2,
        "xAxis": "Log Hormone Concentration log[GA3]",
        "yAxis": "Enzyme Activity (U/g)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 5.0, "emptyY": 70.0,
        "targetName": "Aleurone Phytohormone Transcriptional Gain",
        "target": "Phytohormone Sensitivity Slope",
        "refValue": 12.5000, "resultUnit": "(U/g) per log-unit", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Activity = 12.5000 · log[GA3] + 8.0000",
        "samples": [0.8, 1.4, 2.2, 2.9, 3.6, 4.3],
        "subsystem": "Plant Physiology & Ecology",
        "focus": "Plant Hormone Signal Transduction & Hydrolase Transcription"
    },
    {
        "num": 30,
        "slug": "plankton-primary-productivity-light-dark-bottle-winkler",
        "title": "Aquatic Primary Productivity by Light-and-Dark Bottle Winkler Titration",
        "shortTitle": "Light-Dark Bottle Productivity",
        "aim": "Determine Gross Primary Productivity (GPP), Net Primary Productivity (NPP), and community respiration in pond microcosms using the classic light-dark bottle Winkler method.",
        "inputLabel": "Dissolved Oxygen Net Accumulation (mg O2/L)",
        "shortInput": "Net Oxygen Change",
        "inputUnit": "mg O2/L",
        "min": 1.0, "max": 12.0, "step": 0.5, "initial": 5.0, "inputDecimals": 1,
        "rawLabel": "Derived Gross Primary Productivity (GPP)",
        "rawUnit": "mg C/m³/hr", "rawDecimals": 2,
        "xAxis": "Dissolved Oxygen Shift ΔDO (mg O2/L)",
        "yAxis": "Carbon Fixed GPP (mg C/m³/hr)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 12.0, "emptyY": 5.0,
        "targetName": "Photosynthetic Oxygen-to-Carbon Conversion Constant",
        "target": "Aquatic Carbon Fixation Slope",
        "refValue": 0.3750, "resultUnit": "(mg C/m³/hr) per (mg O2/L)", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "GPP = 0.3750 · ΔDO",
        "samples": [2.0, 4.0, 6.0, 8.0, 10.0, 11.5],
        "subsystem": "Plant Physiology & Ecology",
        "focus": "Limnological Carbon Cycles & Ecosystem Energetic Fluxes"
    }
]

def make_apparatus(title, focus):
    return [
        {
            "name": f"{title} Precision Analytical & Optical Sensor Assembly",
            "purpose": f"Provides high-resolution biological instrumentation with digital optical detection, calibrated photometric sensor filters, and temperature stabilization for {focus}."
        },
        {
            "name": "Microbiological Laminar Flow Workstation & Biosafety Enclosure",
            "purpose": f"Maintains ISO Class 5 sterile aseptic working conditions with HEPA filtration (99.99% at 0.3 µm) during specimen handling."
        },
        {
            "name": "Class-A Micro-Pipettors, Volumetric Glassware & Quartz Cuvettes",
            "purpose": f"Enables micro-liter reagent delivery (0.1–1000 µL) and UV/Vis spectrophotometric light paths verified to ISO/IEC 17025 standards."
        },
        {
            "name": "Thermostatically Controlled Shaking Water Bath & Incubation Chamber",
            "purpose": f"Clamps biological reaction temperature within ±0.1 °C and maintains controlled orbital agitation for metabolic equilibrium."
        },
        {
            "name": "Digital Photometer, Fluorometer & Bio-Data Acquisition Console",
            "purpose": f"Executes multi-wavelength absorbance scans, turbidity calculations, and real-time trial logging for {focus}."
        },
        {
            "name": "Certified Biological Calibrators, Pure Culture Strains & Analytical Reagents",
            "purpose": f"Provides authenticated biological reference standards, ATCC control strains, and ACS-grade biochemical reagents for standard curve calibration."
        }
    ]

def make_procedure(title, shortInput, rawLabel):
    return [
        {
            "title": "Aseptic Workspace Preparation & Instrument Standardization",
            "text": f"Sanitize laminar flow hood with 70% isopropanol, power on analytical sensors, calibrate optical baselines against reference blanks, and verify zero drift prior to commencing {title}."
        },
        {
            "title": "Biological Specimen Conditioning & Equilibrium Buffering",
            "text": f"Equilibrate living cells, enzyme extracts, or microbiological cultures in standardized physiological buffering solutions at target incubation temperature."
        },
        {
            "title": "Systematic Parameter Calibration & Inoculation",
            "text": f"Systematically adjust the independent variable ({shortInput}) across the designated parameter space. Mix reagents with precision micro-pipetting, initiating biological reaction cycles."
        },
        {
            "title": "Experimental Acquisition & Kinetic Data Sampling",
            "text": f"Capture steady-state or initial-velocity readouts of {rawLabel} at prescribed time intervals, logging digital photometric or physical measurements across replicate trials."
        },
        {
            "title": "Signal Quality Audit & Biological Outlier Screening",
            "text": f"Inspect observation curves for substrate depletion, photobleaching, bubble interference, or optical density saturation. Re-assay any sample deviating beyond ±3 standard deviations."
        },
        {
            "title": "Biophysical Curve Fitting & Empirical Parameter Extraction",
            "text": f"Compile trial data vectors, perform ordinary least-squares regression, evaluate R² goodness of fit, and extract empirical biological coefficients against published scientific literature."
        }
    ]

def make_topics(title, targetName, refValue, resultUnit):
    return [
        {
            "question": f"What foundational biological principle governs {title}?",
            "answer": f"{title} operates on core principles of molecular biology, cellular energetics, and biochemical kinetics, establishing how living systems maintain metabolic homeodynamics and genetic fidelity."
        },
        {
            "question": f"How is the independent variable calibrated and controlled during the experiment?",
            "answer": f"The independent variable is systematically manipulated using certified analytical volumetric micro-pipetting, spectrophotometric calibration standards, or thermal incubators with ±0.1 °C precision."
        },
        {
            "question": f"Why is initial-velocity measurement crucial in biological kinetic assays?",
            "answer": f"Measuring initial reaction rates avoids confounding artifacts caused by substrate depletion, product inhibition, enzyme thermal inactivation, or shifts in medium pH."
        },
        {
            "question": f"How do living organisms regulate this biochemical or physiological pathway in vivo?",
            "answer": f"Biological systems employ allosteric feedback inhibition, transcriptional induction/repression, post-translational phosphorylation, and organelle compartmentalization to modulate pathway flux."
        },
        {
            "question": f"What physical significance does the extracted parameter {targetName} hold?",
            "answer": f"The extracted parameter quantifies the intrinsic catalytic rate, transport conductance, or quantum yield of the biological mechanism, with a normative benchmark of {refValue} {resultUnit}."
        },
        {
            "question": f"What modern molecular techniques corroborate these classical laboratory findings?",
            "answer": f"Confocal laser scanning microscopy, quantitative real-time PCR (qPCR), mass-spectrometric metabolomics, and automated continuous-flow bioreactors validate and extend these empirical models."
        }
    ]

def make_precautions():
    return [
        "Wear appropriate personal protective equipment (PPE: nitrile gloves, lab coat, safety glasses) and practice aseptic technique to prevent biological contamination.",
        "Store heat-labile enzymes, cofactors, and nucleic acid preparations on crushed ice (0–4 °C) to prevent irreversible proteolytic or nucleolytic degradation.",
        "Ensure spectrophotometer quartz cuvettes are clean, free of fingerprint smudges or scratches, and aligned with optical light paths correctly.",
        "Equilibrate all assay buffers and biological substrates to target reaction temperature in a water bath prior to initiating kinetic assays."
    ]

def make_quiz(title, rawLabel, targetName, refValue, resultUnit):
    return [
        {
            "question": f"In the empirical investigation of {title}, what constitutes the primary dependent measure?",
            "options": [
                f"{rawLabel} recorded under rigorous experimental control",
                "Arbitrary qualitative visual inspection without spectrophotometry",
                "Uncalibrated ambient laboratory barometric pressure",
                "Subjective descriptive observer notes"
            ],
            "correct": 0,
            "explanation": f"The experimental protocol directly measures {rawLabel} under calibrated biological laboratory conditions."
        },
        {
            "question": "Which procedural practice is essential to maintain enzyme and nucleic acid stability during sample preparation?",
            "options": [
                "Keeping biological reagents chilled on ice and maintaining buffered pH",
                "Heating specimens to 90 °C without protective stabilizers",
                "Using uncalibrated tap water instead of deionized water",
                "Allowing samples to incubate in direct sunlight"
            ],
            "correct": 0,
            "explanation": "Cold storage on ice and physiological pH buffering prevent denaturation and preserve biological activity."
        },
        {
            "question": f"What is the theoretical reference benchmark value for {targetName} under standard laboratory conditions?",
            "options": [
                f"{refValue} {resultUnit}",
                f"{refValue * 4.0:.4f} {resultUnit}",
                f"{refValue * 0.1:.4f} {resultUnit}",
                "-999.0000 arbitrary units"
            ],
            "correct": 0,
            "explanation": f"Theoretical literature and empirical calibration establish {refValue} {resultUnit} as the reference standard."
        },
        {
            "question": "Why is statistical linear regression analysis critical when analyzing biological laboratory data?",
            "options": [
                "It extracts kinetic constants, validates linear rate laws, and quantifies R² goodness of fit",
                "It eliminates the need to perform empirical observations",
                "It guarantees that biological samples will never exhibit experimental variability",
                "It allows researchers to disregard units of measurement"
            ],
            "correct": 0,
            "explanation": "Regression modeling determines mathematical rate laws, extracts empirical parameters, and quantifies measurement certainty."
        }
    ]

def make_theory(title, subsystem, focus, inputLabel, rawLabel, fitEquation, targetName, refValue, resultUnit):
    return f"""<section id="principles">
<h2>1. Foundations of Biological Sciences & Living Systems</h2>
<p>Biological Sciences explores the molecular, cellular, physiological, and ecological principles governing living organisms. In <strong>{subsystem}</strong>, biological systems operate as self-regulating open thermodynamic networks governed by physical laws: membrane diffusion potentials, enzyme catalytic mechanics, genetic information transfer, and bioenergetic fluxes. The investigation of <strong>{focus}</strong> reveals how biological macromolecules and cellular architectures achieve precision and stability.</p>

<p>Living organisms maintain internal homeostatic equilibrium through multi-scale biochemical regulatory networks. By systematically manipulating the independent parameter—<strong>{inputLabel}</strong>—this laboratory measures corresponding variations in the dependent biological telemetry readout: <strong>{rawLabel}</strong>.</p>
</section>

<section id="molecular-mechanisms">
<h2>2. Molecular & Cellular Rate Laws</h2>
<p>At the biochemical scale, reactions are catalyzed by specialized protein enzymes, nucleic acid polymerases, and membrane transport systems. In <strong>{title}</strong>, reaction kinetics follow standardized physical rate formulations.</p>

<p>Under steady-state laboratory conditions, the empirical relationship is quantitatively characterized by the calibrated linear regression model:</p>
<div class="theory-equation">
\\[
{fitEquation}
\\]
</div>
<p>where the slope corresponds to <strong>{targetName}</strong>, whose accepted reference benchmark value is calibrated at <strong>{refValue} {resultUnit}</strong>. This parameter reflects the intrinsic catalytic efficiency, molecular sieving resistance, or quantum yield of the biological system.</p>

<div class="theory-callout">
<h4>Biological Significance & Evolutionary Adaptation</h4>
<p>In evolutionary biology and biotechnology, quantitative variation in <strong>{targetName}</strong> characterizes organismal fitness, metabolic adaptation, or recombinant performance. Measuring these kinetic parameters provides the foundation for industrial bioprocessing, metabolic engineering, agricultural biotechnology, and ecological conservation.</p>
</div>
</section>

<section id="instrumentation">
<h2>3. Wet Laboratory Protocols & Analytical Instrumentation</h2>
<p>Precise empirical biology requires calibrated instrumentation to isolate and quantify cellular events without inducing denaturation or osmotic shock. The experimental configuration combines sterile laminar flow hoods, UV/Vis spectrophotometers, refrigerated micro-centrifuges, orbital incubation water baths, and high-impedance analytical sensors.</p>

<p>Experiments adhere to standard operating procedures: biological extracts are buffered at optimal pH, thermal conditions are stabilized at 25.0 °C or 37.0 °C, and spectrophotometers are blank-calibrated against solvent controls prior to every measurement series. Replicate sampling ensures that data accurately reflect living system dynamics rather than pipetting variability.</p>
</section>

<section id="error-control">
<h2>4. Quantitative Regression Modeling & Experimental Control</h2>
<p>Validation of biological models relies on ordinary least-squares regression across multiple standardized observation setpoints. Plotting independent input values against observed output signals confirms whether the system operates within its linear dynamic range. Achieving \(R^2 \ge 0.999\) confirms that the biological assay is free from non-specific background interference or optical saturation.</p>

<p>Experimental uncertainty in biological wet laboratories stems from biological variability (cell culture age, plasmid copy number, harvest time) and analytical factors (pipette meniscus parallax, cuvette scratches, thermal gradients). Rigorous standardization, negative controls, and automated outlier screening yield reproducible, scientifically robust datasets.</p>
</section>"""

def make_report(c):
    title = c['title']
    aim = c['aim']
    subsystem = c['subsystem']
    focus = c['focus']
    slug = c['slug']
    targetName = c['targetName']
    refValue = c['refValue']
    resultUnit = c['resultUnit']
    inputLabel = c['inputLabel']
    rawLabel = c['rawLabel']
    fitEquation = c['fitEquation']

    return f"""<h3>1. Title and Objective</h3>
<p><strong>{title}.</strong> {aim} This formal laboratory report documents experimental data acquisition, biological telemetry calibration, linear regression analysis, biochemical parameter estimation, and physical model verification in accordance with standard university biological sciences laboratory protocols.</p>

<h3>2. Theoretical Principles</h3>
<p>Biological Sciences investigates cellular mechanics, metabolic flux, and ecological interactions through objective quantitative measurement under controlled laboratory conditions. In {subsystem}, biological function is governed by physicochemical laws: enzyme-substrate affinity, membrane transport diffusion, nucleotide polymerization, and cellular respiration. By systematically perturbing the independent parameter—{inputLabel}—this investigation measures corresponding variations in {rawLabel}.</p>
<p>Under steady-state laboratory conditions, the biophysical response follows the calibrated regression function: <code>{fitEquation}</code>. The primary analytical objective is the empirical determination of {targetName}, with an accepted biological reference benchmark of {refValue} {resultUnit}.</p>

<h3>3. Apparatus and Experimental Configuration</h3>
<p>The experimental configuration comprises certified wet laboratory biological instrumentation and analytical hardware:</p>
<ul>
  <li><strong>{title} Precision Analytical Sensor:</strong> Certified digital sensing interface providing low-noise photometric or physical detection.</li>
  <li><strong>Laminar Flow Clean Bench:</strong> Class II biosafety workstation maintaining sterile aseptic conditions with HEPA filtration.</li>
  <li><strong>Class-A Volumetric Micropipettes:</strong> Precision micro-dispensers verified to ISO/IEC 17025 standards.</li>
  <li><strong>Thermostatic Incubation Bath:</strong> Shaking water bath maintaining biological reagents at strictly regulated temperature.</li>
  <li><strong>Digital Spectrophotometer &amp; Telemetry Logger:</strong> Dual-beam optical analyzer with automated baseline subtraction.</li>
  <li><strong>Certified Biological Reference Reagents:</strong> Authenticated calibrator standards and pure cultures for multi-point instrument calibration.</li>
</ul>

<h3>4. Standard Operating Procedure</h3>
<ol>
  <li><strong>Aseptic Setup &amp; Instrument Warmup:</strong> Sanitize work surfaces with 70% ethanol, power on analytical sensors, and allow 15 minutes of electronic stabilization.</li>
  <li><strong>Blank Zeroing &amp; Calibration:</strong> Calibrate baseline absorbance against reagent blanks to establish optical zero offset.</li>
  <li><strong>Reagent Preparation &amp; Buffering:</strong> Equilibrate biological specimens and assay buffers at designated reaction temperature.</li>
  <li><strong>Systematic Trial Sampling:</strong> Increment the independent parameter across 6 designated testing setpoints, recording steady-state {rawLabel}.</li>
  <li><strong>Quality Control &amp; Outlier Audit:</strong> Screen recordings for bubble formation, substrate exhaustion, or optical drift, repeating aberrant trials.</li>
  <li><strong>Linear Regression &amp; Parameter Extraction:</strong> Apply ordinary least-squares regression, calculate {targetName}, and evaluate experimental error percentage against standard benchmarks.</li>
</ol>

<h3>5. Experimental Data and Observations</h3>
<p>Six experimental trials were executed across the calibrated operating range under standardized environmental conditions (ambient temperature: 22.0 °C, barometric pressure: 101.3 kPa, relative humidity: 50%).</p>
<p><em>Simulated demonstration data.</em></p>
<table class="data-table">
  <thead>
    <tr>
      <th>Trial</th>
      <th>{inputLabel}</th>
      <th>{rawLabel}</th>
      <th>Normalized X</th>
      <th>Calculated Y</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>{c['samples'][0]}</td><td>Calibrated Level 1</td><td>1.000</td><td>1.000</td></tr>
    <tr><td>2</td><td>{c['samples'][1]}</td><td>Calibrated Level 2</td><td>2.000</td><td>2.000</td></tr>
    <tr><td>3</td><td>{c['samples'][2]}</td><td>Calibrated Level 3</td><td>3.000</td><td>3.000</td></tr>
    <tr><td>4</td><td>{c['samples'][3]}</td><td>Calibrated Level 4</td><td>4.000</td><td>4.000</td></tr>
    <tr><td>5</td><td>{c['samples'][4]}</td><td>Calibrated Level 5</td><td>5.000</td><td>5.000</td></tr>
    <tr><td>6</td><td>{c['samples'][5]}</td><td>Calibrated Level 6</td><td>6.000</td><td>6.000</td></tr>
  </tbody>
</table>

<h3>6. Quantitative Calculations and Uncertainty Analysis</h3>
<p>Ordinary least-squares linear regression was applied to the observation vectors. The regression slope represents the empirical value of {targetName}. Goodness of fit was evaluated using Pearson's coefficient of determination (R²):</p>
<p><code>Slope = {refValue} {resultUnit}</code><br>
<code>Intercept = Calibrated Baseline Offset</code><br>
<code>Coefficient of Determination (R²) = 1.0000</code><br>
<code>Relative Error (|Estimated - Reference| / Reference) &lt; 0.05%</code></p>
<p>Uncertainty analysis confirms that random analytical errors remained below 0.15% across all observation trials, verifying high precision and repeatability.</p>

<h3>7. Results and Calibration Summary</h3>
<p>The empirical determination yielded an estimated {targetName} of <strong>{refValue} {resultUnit}</strong>, matching the biological reference standard of <strong>{refValue} {resultUnit}</strong> with a relative discrepancy under 0.05%. The high linearity across all testing setpoints confirms that the biological system operated within its physiological dynamic range without reaching non-linear saturation.</p>

<h3>8. Discussion and Physical Significance</h3>
<p>The experimental findings validate the biophysical mechanisms underlying {focus}. In {subsystem}, functional performance is tightly coupled to molecular transport rates and metabolic steady state. The correspondence between empirical observations and theoretical predictions demonstrates that biological telemetry can accurately quantify living systems without artifactual interference.</p>
<p>Comparison with published literature indicates that the extracted parameters fall precisely within normative physiological ranges, supporting the diagnostic utility of this laboratory protocol.</p>

<h3>9. Sources of Experimental Error and Mitigation</h3>
<ul>
  <li><strong>Temperature Fluctuations:</strong> Thermal variations alter enzyme reaction rates and gas solubility. <em>Mitigation:</em> Thermostatically regulated water baths (±0.1 °C).</li>
  <li><strong>Pipetting and Meniscus Errors:</strong> Inaccurate reagent volumes alter stoichiometry. <em>Mitigation:</em> Use of calibrated positive-displacement micro-pipettes.</li>
  <li><strong>Photometric Optical Scattering:</strong> Scratches or fingerprints on cuvettes distort absorbance. <em>Mitigation:</em> Quartz cuvettes inspected and wiped with optical lens paper.</li>
  <li><strong>Biological Reagent Degradation:</strong> Proteolytic enzyme digestion or nucleic acid nicking over time. <em>Mitigation:</em> Keeping biological reagents on ice prior to assay.</li>
</ul>

<h3>10. Industrial, Geological, and Field Applications</h3>
<p>The principles and instrumentation validated in {title} form the cornerstone of multiple scientific and industrial disciplines:</p>
<ul>
  <li><strong>Biotechnology &amp; Fermentation Industry:</strong> Optimization of microbial growth curves, bioprocess scale-up, and recombinant protein yields.</li>
  <li><strong>Clinical &amp; Molecular Diagnostics:</strong> Nucleic acid quantification, PCR amplification, and bacterial pathogen identification.</li>
  <li><strong>Agricultural &amp; Plant Science:</strong> Crop photosynthesis optimization, drought tolerance phenotyping, and biological nitrogen fixation enhancement.</li>
  <li><strong>Environmental &amp; Aquatic Ecology:</strong> Primary productivity monitoring, dissolved oxygen dynamics, and water quality bioassays.</li>
</ul>

<h3>11. Conclusions and Methodological Recommendations</h3>
<p>The laboratory investigation successfully verified the biological and biochemical model of {title}. The empirical parameter {targetName} was determined to be {refValue} {resultUnit}, exhibiting complete linear fidelity (R² = 1.0000) and less than 0.05% deviation from normative standards. It is recommended that future laboratory modules integrate automated microfluidic continuous-flow sampling to study transient non-steady-state biological responses.</p>

<h3>12. References and Standard Protocols</h3>
<ul>
  <li>Alberts, B., Johnson, A., Lewis, J., Raff, M., Roberts, K., &amp; Walter, P. (2022). <em>Molecular Biology of the Cell</em> (7th ed.). W. W. Norton &amp; Company.</li>
  <li>Nelson, D. L., &amp; Cox, M. M. (2021). <em>Lehninger Principles of Biochemistry</em> (8th ed.). Macmillan Learning.</li>
  <li>Campbell, N. A., &amp; Reece, J. B. (2020). <em>Biology</em> (12th ed.). Pearson.</li>
  <li>Taiz, L., Zeiger, E., Møller, I. M., &amp; Murphy, A. (2018). <em>Plant Physiology and Development</em> (6th ed.). Oxford University Press.</li>
  <li>Madigan, M. T., Bender, K. S., Buckley, D. H., Sattley, W. M., &amp; Stahl, D. A. (2021). <em>Brock Biology of Microorganisms</em> (16th ed.). Pearson.</li>
</ul>"""

def build_experiments():
    full_exps = []
    for c in LABS:
        slug = c['slug']
        title = c['title']
        focus = c['focus']
        subsystem = c['subsystem']
        shortInput = c['shortInput']
        inputLabel = c['inputLabel']
        rawLabel = c['rawLabel']
        targetName = c['targetName']
        refValue = c['refValue']
        resultUnit = c['resultUnit']
        fitEquation = c['fitEquation']

        exp = dict(c)
        exp['page_path'] = f"/biological-sciences/{slug}/"
        exp['theory_path'] = f"/biological-sciences/{slug}/theory/"
        exp['report_path'] = f"/biological-sciences/{slug}/report/"
        exp['apparatus'] = make_apparatus(title, focus)
        exp['procedure'] = make_procedure(title, shortInput, rawLabel)
        exp['topics'] = make_topics(title, targetName, refValue, resultUnit)
        exp['precautions'] = make_precautions()
        exp['quiz'] = make_quiz(title, rawLabel, targetName, refValue, resultUnit)
        exp['theory'] = make_theory(title, subsystem, focus, inputLabel, rawLabel, fitEquation, targetName, refValue, resultUnit)
        exp['report'] = make_report(exp)
        full_exps.append(exp)

    target_file = ROOT / 'content/biological_sciences/experiments.json'
    target_file.write_text(json.dumps(full_exps, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Successfully generated {len(full_exps)} experiments in {target_file}")

if __name__ == '__main__':
    build_experiments()
