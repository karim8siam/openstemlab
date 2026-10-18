# -*- coding: utf-8 -*-
"""Generate high-rigor experiments.json for Agriculture & Forestry."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LABS = [
    # Module 1: Agronomy, Crop Physiology & Seed Science (Labs 1–4)
    {
        "num": 1,
        "slug": "seed-germination-vigor-tetrazolium-viability",
        "title": "Seed Germination Rate, Vigour Index & Tetrazolium Biochemical Viability",
        "shortTitle": "Seed Germination & Vigour",
        "aim": "Determine standard germination energy, germination rate index (GRI), and dehydrogenase enzyme viability using 2,3,5-triphenyl tetrazolium chloride (TTC).",
        "inputLabel": "Incubation Chamber Temperature (°C)",
        "shortInput": "Temperature",
        "inputUnit": "°C",
        "min": 10.0,
        "max": 35.0,
        "step": 2.5,
        "initial": 20.0,
        "inputDecimals": 1,
        "rawLabel": "Germination Speed Index (GRI)",
        "rawUnit": "seeds/day",
        "rawDecimals": 1,
        "xAxis": "Germination Temperature T (°C)",
        "yAxis": "Germination Rate Index GRI (seeds/day)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 38.0,
        "emptyY": 100.0,
        "targetName": "Thermal Germination Response Slope",
        "target": "Germination Thermal Sensitivity",
        "refValue": 2.4500,
        "resultUnit": "seeds/day/°C",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "GRI = 2.4500 · T + 12.0000",
        "samples": [10.0, 15.0, 20.0, 25.0, 30.0, 35.0],
        "subsystem": "Agronomy, Crop Physiology & Seed Science",
        "focus": "Seed Vigour & Biochemical Embryo Viability",
        "page_path": "/agriculture-forestry/seed-germination-vigor-tetrazolium-viability/",
        "theory_path": "/agriculture-forestry/seed-germination-vigor-tetrazolium-viability/theory/",
        "report_path": "/agriculture-forestry/seed-germination-vigor-tetrazolium-viability/report/"
    },
    {
        "num": 2,
        "slug": "soil-moisture-neutron-probe-calibration",
        "title": "Soil Moisture Volumetric Neutron Moderation Probe Calibration",
        "shortTitle": "Neutron Probe Moisture",
        "aim": "Calibrate downhole thermal neutron thermalization count ratios against volumetric soil water content theta_v across agricultural soil horizons.",
        "inputLabel": "Volumetric Soil Water Content (m³/m³)",
        "shortInput": "Theta_v",
        "inputUnit": "m³/m³",
        "min": 0.08,
        "max": 0.38,
        "step": 0.02,
        "initial": 0.20,
        "inputDecimals": 2,
        "rawLabel": "Neutron Probe Count Ratio (CR)",
        "rawUnit": "ratio",
        "rawDecimals": 3,
        "xAxis": "Volumetric Water Content θv (m³/m³)",
        "yAxis": "Thermal Neutron Count Ratio CR (ratio)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 0.42,
        "emptyY": 1.30,
        "targetName": "Neutron Moderation Calibration Slope (m)",
        "target": "Neutron Calibration Sensitivity",
        "refValue": 2.8500,
        "resultUnit": "ratio/(m³/m³)",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "CR = 2.8500 · θv + 0.1200",
        "samples": [0.08, 0.14, 0.20, 0.26, 0.32, 0.38],
        "subsystem": "Agronomy, Crop Physiology & Seed Science",
        "focus": "Downhole Fast Neutron Hydrogen Thermalization",
        "page_path": "/agriculture-forestry/soil-moisture-neutron-probe-calibration/",
        "theory_path": "/agriculture-forestry/soil-moisture-neutron-probe-calibration/theory/",
        "report_path": "/agriculture-forestry/soil-moisture-neutron-probe-calibration/report/"
    },
    {
        "num": 3,
        "slug": "crop-water-stress-index-infrared-thermometry",
        "title": "Crop Water Stress Index (CWSI) & Canopy-Air Temperature Differential",
        "shortTitle": "Crop Water Stress CWSI",
        "aim": "Determine non-water-stressed baseline (NWSB) relationships relating canopy-air temperature differential (Tc - Ta) to atmospheric vapor pressure deficit (VPD).",
        "inputLabel": "Atmospheric Vapor Pressure Deficit (kPa)",
        "shortInput": "VPD",
        "inputUnit": "kPa",
        "min": 1.0,
        "max": 3.5,
        "step": 0.5,
        "initial": 2.0,
        "inputDecimals": 1,
        "rawLabel": "Canopy-Air Temperature Difference (Tc - Ta)",
        "rawUnit": "°C",
        "rawDecimals": 2,
        "xAxis": "Vapor Pressure Deficit VPD (kPa)",
        "yAxis": "Canopy Depression (Tc - Ta) (°C)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 4.0,
        "emptyY": 4.0,
        "targetName": "Canopy Transpiration Cooling Rate",
        "target": "NWSB Temperature-VPD Slope",
        "refValue": 1.6500,
        "resultUnit": "°C/kPa",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "(Tc - Ta) = -1.6500 · VPD + 2.1000",
        "samples": [1.0, 1.5, 2.0, 2.5, 3.0, 3.5],
        "subsystem": "Agronomy, Crop Physiology & Seed Science",
        "focus": "Infrared Thermography & Stomatal Conductance",
        "page_path": "/agriculture-forestry/crop-water-stress-index-infrared-thermometry/",
        "theory_path": "/agriculture-forestry/crop-water-stress-index-infrared-thermometry/theory/",
        "report_path": "/agriculture-forestry/crop-water-stress-index-infrared-thermometry/report/"
    },
    {
        "num": 4,
        "slug": "chlorophyll-spad-meter-nitrogen-status",
        "title": "Chlorophyll Optical SPAD Meter & Leaf Total Nitrogen Concentration",
        "shortTitle": "Chlorophyll SPAD Nitrogen",
        "aim": "Calibrate non-destructive dual-wavelength optical absorbance index (SPAD-502) against destructive Kjeldahl foliar nitrogen concentration.",
        "inputLabel": "Optical Leaf Chlorophyll Index (SPAD units)",
        "shortInput": "SPAD",
        "inputUnit": "units",
        "min": 20.0,
        "max": 60.0,
        "step": 4.0,
        "initial": 36.0,
        "inputDecimals": 0,
        "rawLabel": "Kjeldahl Leaf Nitrogen Concentration",
        "rawUnit": "g/kg",
        "rawDecimals": 2,
        "xAxis": "Chlorophyll Meter Index SPAD (units)",
        "yAxis": "Leaf Total Nitrogen N (g/kg)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 65.0,
        "emptyY": 5.0,
        "targetName": "Foliar Nitrogen Conversion Factor",
        "target": "SPAD Nitrogen Conversion Slope",
        "refValue": 0.0650,
        "resultUnit": "(g/kg)/unit",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "N = 0.0650 · SPAD + 0.4500",
        "samples": [20.0, 28.0, 36.0, 44.0, 52.0, 60.0],
        "subsystem": "Agronomy, Crop Physiology & Seed Science",
        "focus": "Non-Destructive Crop Nitrogen Nutrition Diagnostics",
        "page_path": "/agriculture-forestry/chlorophyll-spad-meter-nitrogen-status/",
        "theory_path": "/agriculture-forestry/chlorophyll-spad-meter-nitrogen-status/theory/",
        "report_path": "/agriculture-forestry/chlorophyll-spad-meter-nitrogen-status/report/"
    },

    # Module 2: Soil Science, Plant Nutrition & Fertilizer Dynamics (Labs 5–8)
    {
        "num": 5,
        "slug": "soil-cation-exchange-capacity-ammonium-acetate",
        "title": "Soil Cation Exchange Capacity (CEC) & Exchangeable Bases by 1M NH4OAc",
        "shortTitle": "Soil CEC Ammonium Acetate",
        "aim": "Quantify colloidal cation adsorption capacity and exchangeable Ca2+, Mg2+, K+, and Na+ across soils with varying clay content at pH 7.0.",
        "inputLabel": "Soil Clay Fraction Percentage (%)",
        "shortInput": "Clay",
        "inputUnit": "%",
        "min": 10.0,
        "max": 50.0,
        "step": 4.0,
        "initial": 26.0,
        "inputDecimals": 0,
        "rawLabel": "Cation Exchange Capacity (CEC)",
        "rawUnit": "cmol_c/kg",
        "rawDecimals": 2,
        "xAxis": "Soil Clay Content (%)",
        "yAxis": "Cation Exchange Capacity CEC (cmol_c/kg)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 55.0,
        "emptyY": 40.0,
        "targetName": "Clay Mineral Colloid Exchange Capacity Rate",
        "target": "Clay CEC Contribution Slope",
        "refValue": 0.5800,
        "resultUnit": "(cmol_c/kg)/%",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "CEC = 0.5800 · Clay + 4.2000",
        "samples": [10.0, 18.0, 26.0, 34.0, 42.0, 50.0],
        "subsystem": "Soil Science, Plant Nutrition & Fertilizer Dynamics",
        "focus": "Soil Mineral Colloids & Exchangeable Nutrients",
        "page_path": "/agriculture-forestry/soil-cation-exchange-capacity-ammonium-acetate/",
        "theory_path": "/agriculture-forestry/soil-cation-exchange-capacity-ammonium-acetate/theory/",
        "report_path": "/agriculture-forestry/soil-cation-exchange-capacity-ammonium-acetate/report/"
    },
    {
        "num": 6,
        "slug": "bray-curtis-soil-available-phosphorus",
        "title": "Bray-1 Acid Fluoride Extraction & Spectrophotometric Available Phosphorus",
        "shortTitle": "Bray-1 Available Phosphorus",
        "aim": "Determine plant-available orthophosphate in acidic agricultural soils using 0.03M NH4F + 0.025M HCl extraction and ascorbic acid molybdate blue spectrophotometry.",
        "inputLabel": "Available Soil Phosphorus Concentration (mg/kg)",
        "shortInput": "P_avail",
        "inputUnit": "mg/kg",
        "min": 5.0,
        "max": 30.0,
        "step": 2.5,
        "initial": 15.0,
        "inputDecimals": 1,
        "rawLabel": "Spectrophotometric Optical Absorbance (882 nm)",
        "rawUnit": "AU",
        "rawDecimals": 3,
        "xAxis": "Soil Available Phosphorus P (mg/kg)",
        "yAxis": "Optical Absorbance at 882 nm (AU)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 35.0,
        "emptyY": 1.0,
        "targetName": "Phosphomolybdate Chromophore Molar Absorptivity",
        "target": "Beer-Lambert Colorimetric P Slope",
        "refValue": 0.0280,
        "resultUnit": "AU/(mg/kg)",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "A = 0.0280 · P + 0.0120",
        "samples": [5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
        "subsystem": "Soil Science, Plant Nutrition & Fertilizer Dynamics",
        "focus": "Soil Phosphorus Fertility & Colorimetric Calibration",
        "page_path": "/agriculture-forestry/bray-curtis-soil-available-phosphorus/",
        "theory_path": "/agriculture-forestry/bray-curtis-soil-available-phosphorus/theory/",
        "report_path": "/agriculture-forestry/bray-curtis-soil-available-phosphorus/report/"
    },
    {
        "num": 7,
        "slug": "soil-salinity-electrical-conductivity-extract",
        "title": "Soil Saturated Paste Electrical Conductivity (ECe) & Osmotic Salinity",
        "shortTitle": "Soil Salinity ECe",
        "aim": "Determine soil electrolyte concentration and root-zone osmotic potential from saturated soil paste vacuum extract electrical conductivity.",
        "inputLabel": "Standard KCl Calibration Concentration (mol/L)",
        "shortInput": "KCl",
        "inputUnit": "mol/L",
        "min": 0.01,
        "max": 0.06,
        "step": 0.005,
        "initial": 0.03,
        "inputDecimals": 3,
        "rawLabel": "Electrolytic Specific Conductance (EC)",
        "rawUnit": "dS/m",
        "rawDecimals": 2,
        "xAxis": "Electrolyte Concentration C (mol/L)",
        "yAxis": "Electrical Conductivity EC (dS/m)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 0.07,
        "emptyY": 0.90,
        "targetName": "Molar Electrolyte Conductance Factor",
        "target": "Conductivity Cell Molar Slope",
        "refValue": 12.8000,
        "resultUnit": "(dS/m)/(mol/L)",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "EC = 12.8000 · C",
        "samples": [0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
        "subsystem": "Soil Science, Plant Nutrition & Fertilizer Dynamics",
        "focus": "USDA Salinity Laboratory Saturated Paste Protocols",
        "page_path": "/agriculture-forestry/soil-salinity-electrical-conductivity-extract/",
        "theory_path": "/agriculture-forestry/soil-salinity-electrical-conductivity-extract/theory/",
        "report_path": "/agriculture-forestry/soil-salinity-electrical-conductivity-extract/report/"
    },
    {
        "num": 8,
        "slug": "plant-tissue-potassium-flame-photometry",
        "title": "Plant Tissue Nitric-Perchloric Digestion & Flame Photometric Potassium",
        "shortTitle": "Tissue Potassium Photometry",
        "aim": "Quantify foliar K+ macronutrient status via wet acid digestion and optical atomic emission flame photometry at 766.5 nm.",
        "inputLabel": "Standard Potassium Concentration (mg/L)",
        "shortInput": "K_conc",
        "inputUnit": "mg/L",
        "min": 2.0,
        "max": 12.0,
        "step": 1.0,
        "initial": 6.0,
        "inputDecimals": 1,
        "rawLabel": "Flame Photometer Emission Intensity",
        "rawUnit": "emission-units",
        "rawDecimals": 1,
        "xAxis": "Potassium Concentration K (mg/L)",
        "yAxis": "Atomic Emission Intensity I (units)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 13.0,
        "emptyY": 110.0,
        "targetName": "Atomic Emission Calibration Responsivity",
        "target": "Flame Photometric Potassium Slope",
        "refValue": 7.8500,
        "resultUnit": "units/(mg/L)",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "I = 7.8500 · K + 1.2000",
        "samples": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
        "subsystem": "Soil Science, Plant Nutrition & Fertilizer Dynamics",
        "focus": "Foliar Macronutrient Atomic Emission Spectroscopy",
        "page_path": "/agriculture-forestry/plant-tissue-potassium-flame-photometry/",
        "theory_path": "/agriculture-forestry/plant-tissue-potassium-flame-photometry/theory/",
        "report_path": "/agriculture-forestry/plant-tissue-potassium-flame-photometry/report/"
    },

    # Module 3: Irrigation, Agrohydrology & Drainage Engineering (Labs 9–12)
    {
        "num": 9,
        "slug": "subsurface-drip-irrigation-emitter-discharge-uniformity",
        "title": "Subsurface Drip Irrigation Emitter Operating Pressure & Christiansen Uniformity",
        "shortTitle": "Subsurface Drip Emitter Uniformity",
        "aim": "Evaluate pressure-discharge exponent x and Christiansen coefficient of uniformity (CU) along a micro-irrigation drip lateral.",
        "inputLabel": "Lateral Operating Pressure Head (kPa)",
        "shortInput": "Pressure",
        "inputUnit": "kPa",
        "min": 50.0,
        "max": 175.0,
        "step": 12.5,
        "initial": 100.0,
        "inputDecimals": 0,
        "rawLabel": "Mean Emitter Discharge Rate (q)",
        "rawUnit": "L/h",
        "rawDecimals": 2,
        "xAxis": "Lateral Operating Pressure P (kPa)",
        "yAxis": "Emitter Discharge Rate q (L/h)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 190.0,
        "emptyY": 6.5,
        "targetName": "Emitter Orifice Hydraulic Discharge Gradient",
        "target": "Pressure Discharge Sensitivity Slope",
        "refValue": 0.0240,
        "resultUnit": "(L/h)/kPa",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "q = 0.0240 · P + 1.1500",
        "samples": [50.0, 75.0, 100.0, 125.0, 150.0, 175.0],
        "subsystem": "Irrigation, Agrohydrology & Drainage Engineering",
        "focus": "Micro-Irrigation Hydraulic Distribution Uniformity",
        "page_path": "/agriculture-forestry/subsurface-drip-irrigation-emitter-discharge-uniformity/",
        "theory_path": "/agriculture-forestry/subsurface-drip-irrigation-emitter-discharge-uniformity/theory/",
        "report_path": "/agriculture-forestry/subsurface-drip-irrigation-emitter-discharge-uniformity/report/"
    },
    {
        "num": 10,
        "slug": "penman-monteith-reference-evapotranspiration",
        "title": "FAO-56 Penman-Monteith Reference Crop Evapotranspiration (ET0)",
        "shortTitle": "FAO-56 Penman-Monteith ET0",
        "aim": "Calculate standardized grass reference evapotranspiration ET0 combining surface energy balance net radiation Rn and aerodynamic vapor transfer.",
        "inputLabel": "Net Surface Solar Radiation Rn (MJ/m²/day)",
        "shortInput": "Rn",
        "inputUnit": "MJ/m²/day",
        "min": 10.0,
        "max": 30.0,
        "step": 2.0,
        "initial": 18.0,
        "inputDecimals": 1,
        "rawLabel": "Reference Evapotranspiration (ET0)",
        "rawUnit": "mm/day",
        "rawDecimals": 2,
        "xAxis": "Net Radiation Rn (MJ/m²/day)",
        "yAxis": "Reference Evapotranspiration ET0 (mm/day)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 33.0,
        "emptyY": 7.5,
        "targetName": "Radiation-Driven Evaporative Conversion Efficiency",
        "target": "Penman-Monteith Radiation Slope",
        "refValue": 0.1850,
        "resultUnit": "(mm/day)/(MJ/m²/day)",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "ET0 = 0.1850 · Rn + 0.6500",
        "samples": [10.0, 14.0, 18.0, 22.0, 26.0, 30.0],
        "subsystem": "Irrigation, Agrohydrology & Drainage Engineering",
        "focus": "FAO-56 Agro-Meteorological Water Balance Modeling",
        "page_path": "/agriculture-forestry/penman-monteith-reference-evapotranspiration/",
        "theory_path": "/agriculture-forestry/penman-monteith-reference-evapotranspiration/theory/",
        "report_path": "/agriculture-forestry/penman-monteith-reference-evapotranspiration/report/"
    },
    {
        "num": 11,
        "slug": "furrow-irrigation-advance-infiltration-kostiakov",
        "title": "Furrow Irrigation Water Advance & Kostiakov Cumulative Infiltration",
        "shortTitle": "Furrow Advance Infiltration",
        "aim": "Parameterize water advance rate and Kostiakov cumulative infiltration depth Z = k · t^a along graded agricultural furrow irrigation runs.",
        "inputLabel": "Ponding Opportunity Time (min)",
        "shortInput": "Time",
        "inputUnit": "min",
        "min": 10.0,
        "max": 60.0,
        "step": 5.0,
        "initial": 30.0,
        "inputDecimals": 0,
        "rawLabel": "Cumulative Infiltration Depth (Z)",
        "rawUnit": "mm",
        "rawDecimals": 1,
        "xAxis": "Infiltration Opportunity Time t (min)",
        "yAxis": "Cumulative Infiltrated Depth Z (mm)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 65.0,
        "emptyY": 70.0,
        "targetName": "Steady-State Furrow Infiltration Velocity",
        "target": "Furrow Infiltration Advance Slope",
        "refValue": 0.8500,
        "resultUnit": "mm/min",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "Z = 0.8500 · t + 8.5000",
        "samples": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
        "subsystem": "Irrigation, Agrohydrology & Drainage Engineering",
        "focus": "Surface Irrigation Water Infiltration Dynamics",
        "page_path": "/agriculture-forestry/furrow-irrigation-advance-infiltration-kostiakov/",
        "theory_path": "/agriculture-forestry/furrow-irrigation-advance-infiltration-kostiakov/theory/",
        "report_path": "/agriculture-forestry/furrow-irrigation-advance-infiltration-kostiakov/report/"
    },
    {
        "num": 12,
        "slug": "tensiometer-soil-matric-potential-retention",
        "title": "Soil Matric Suction Tensiometry & Van Genuchten Water Retention",
        "shortTitle": "Tensiometer Water Retention",
        "aim": "Construct soil water characteristic curves (SWCC) correlating mercury-manometer ceramic tensiometer suction head with volumetric soil moisture depletion.",
        "inputLabel": "Tensiometer Soil Matric Suction (kPa)",
        "shortInput": "Suction",
        "inputUnit": "kPa",
        "min": 10.0,
        "max": 60.0,
        "step": 5.0,
        "initial": 30.0,
        "inputDecimals": 0,
        "rawLabel": "Volumetric Soil Moisture Content",
        "rawUnit": "m³/m³",
        "rawDecimals": 3,
        "xAxis": "Soil Matric Suction Head ψ (kPa)",
        "yAxis": "Volumetric Moisture Content θ (m³/m³)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 65.0,
        "emptyY": 0.45,
        "targetName": "Specific Moisture Capacity Retention Slope",
        "target": "Tensiometric Desorption Slope",
        "refValue": 0.0035,
        "resultUnit": "(m³/m³)/kPa",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "θ = -0.0035 · ψ + 0.4200",
        "samples": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
        "subsystem": "Irrigation, Agrohydrology & Drainage Engineering",
        "focus": "Capillary Soil Suction & Unsaturated Water Transport",
        "page_path": "/agriculture-forestry/tensiometer-soil-matric-potential-retention/",
        "theory_path": "/agriculture-forestry/tensiometer-soil-matric-potential-retention/theory/",
        "report_path": "/agriculture-forestry/tensiometer-soil-matric-potential-retention/report/"
    },

    # Module 4: Plant Pathology, Entomology & Crop Protection (Labs 13–16)
    {
        "num": 13,
        "slug": "fungicide-bioassay-mycelial-growth-inhibition",
        "title": "Fungicide Poisoned Food Bioassay, Mycelial Growth & EC50 Dosage",
        "shortTitle": "Fungicide Bioassay EC50",
        "aim": "Determine median effective concentration (EC50) of systemic triazole fungicides against phytopathogenic fungi using radial agar colony inhibition assays.",
        "inputLabel": "Active Fungicide Dosage Concentration (mg/L)",
        "shortInput": "Dosage",
        "inputUnit": "mg/L",
        "min": 4.0,
        "max": 24.0,
        "step": 2.0,
        "initial": 16.0,
        "inputDecimals": 1,
        "rawLabel": "Radial Mycelial Growth Inhibition",
        "rawUnit": "%",
        "rawDecimals": 1,
        "xAxis": "Fungicide Concentration C (mg/L)",
        "yAxis": "Mycelial Inhibition Rate I (%)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 26.0,
        "emptyY": 95.0,
        "targetName": "Dose-Response Fungitoxic Inhibition Rate",
        "target": "Fungicide Bioassay Slope",
        "refValue": 2.8500,
        "resultUnit": "%/(mg/L)",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "I = 2.8500 · C + 8.2000",
        "samples": [4.0, 8.0, 12.0, 16.0, 20.0, 24.0],
        "subsystem": "Plant Pathology, Entomology & Crop Protection",
        "focus": "Fungicide Toxicological Bioassays & Pathogen Resistance",
        "page_path": "/agriculture-forestry/fungicide-bioassay-mycelial-growth-inhibition/",
        "theory_path": "/agriculture-forestry/fungicide-bioassay-mycelial-growth-inhibition/theory/",
        "report_path": "/agriculture-forestry/fungicide-bioassay-mycelial-growth-inhibition/report/"
    },
    {
        "num": 14,
        "slug": "insect-population-sweep-net-economic-threshold",
        "title": "Field Sweep-Net Insect Pest Sampling & Economic Injury Level (EIL)",
        "shortTitle": "Insect Sweep-Net EIL",
        "aim": "Calculate Economic Injury Level (EIL) and action threshold from standard sweep-net population counts and crop yield loss regressions.",
        "inputLabel": "Pest Population Density (insects/sweep)",
        "shortInput": "Pest Density",
        "inputUnit": "insects/sweep",
        "min": 5.0,
        "max": 30.0,
        "step": 2.5,
        "initial": 15.0,
        "inputDecimals": 0,
        "rawLabel": "Crop Foliar Damage / Yield Loss",
        "rawUnit": "%",
        "rawDecimals": 1,
        "xAxis": "Insect Pest Density P (insects/sweep)",
        "yAxis": "Estimated Crop Yield Loss ΔY (%)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 35.0,
        "emptyY": 35.0,
        "targetName": "Yield Damage Coefficient per Pest Insect",
        "target": "Pest Yield Damage Slope",
        "refValue": 0.8500,
        "resultUnit": "%/(insects/sweep)",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "ΔY = 0.8500 · P + 1.5000",
        "samples": [5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
        "subsystem": "Plant Pathology, Entomology & Crop Protection",
        "focus": "Integrated Pest Management (IPM) & Economic Injury Levels",
        "page_path": "/agriculture-forestry/insect-population-sweep-net-economic-threshold/",
        "theory_path": "/agriculture-forestry/insect-population-sweep-net-economic-threshold/theory/",
        "report_path": "/agriculture-forestry/insect-population-sweep-net-economic-threshold/report/"
    },
    {
        "num": 15,
        "slug": "herbicide-spray-droplet-spectrum-water-sensitive-paper",
        "title": "Hydraulic Spray Nozzle Orifice, Droplet Size Spectrum & VMD Coverage",
        "shortTitle": "Spray Droplet Spectrum VMD",
        "aim": "Quantify volume median diameter (VMD D_v0.5) and drift risk across agricultural spray boom pressures using water-sensitive paper (WSP) image analysis.",
        "inputLabel": "Nozzle Operating Boom Pressure (kPa)",
        "shortInput": "Pressure",
        "inputUnit": "kPa",
        "min": 150.0,
        "max": 400.0,
        "step": 25.0,
        "initial": 250.0,
        "inputDecimals": 0,
        "rawLabel": "Volume Median Diameter (VMD Dv0.5)",
        "rawUnit": "μm",
        "rawDecimals": 1,
        "xAxis": "Spray Operating Pressure P (kPa)",
        "yAxis": "Droplet VMD Dv0.5 (μm)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 420.0,
        "emptyY": 400.0,
        "targetName": "Hydraulic Atomization Pressure Sensitivity",
        "target": "Droplet Size Pressure Decay Slope",
        "refValue": 0.4200,
        "resultUnit": "μm/kPa",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "VMD = -0.4200 · P + 380.0000",
        "samples": [150.0, 200.0, 250.0, 300.0, 350.0, 400.0],
        "subsystem": "Plant Pathology, Entomology & Crop Protection",
        "focus": "Agrochemical Atomization & Spray Drift Control",
        "page_path": "/agriculture-forestry/herbicide-spray-droplet-spectrum-water-sensitive-paper/",
        "theory_path": "/agriculture-forestry/herbicide-spray-droplet-spectrum-water-sensitive-paper/theory/",
        "report_path": "/agriculture-forestry/herbicide-spray-droplet-spectrum-water-sensitive-paper/report/"
    },
    {
        "num": 16,
        "slug": "seed-borne-pathogen-blotter-infection-incidence",
        "title": "ISTA Standard Blotter Seed Health Assay & Pathogen Infection Incidence",
        "shortTitle": "Seed Health Blotter Assay",
        "aim": "Identify and quantify fungal seed-borne phytopathogens (Fusarium, Alternaria, Bipolaris) using ISTA standard deep-freezing blotter protocols.",
        "inputLabel": "Seed Sample Incubation Density (seeds/dish)",
        "shortInput": "Density",
        "inputUnit": "seeds/dish",
        "min": 5.0,
        "max": 30.0,
        "step": 2.5,
        "initial": 15.0,
        "inputDecimals": 0,
        "rawLabel": "Colony Forming Infection Count",
        "rawUnit": "colonies",
        "rawDecimals": 1,
        "xAxis": "Seed Plating Batch Size N (seeds)",
        "yAxis": "Pathogen Infection Count (colonies)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 35.0,
        "emptyY": 45.0,
        "targetName": "Seed-Borne Pathogen Transmission Incidence",
        "target": "Pathogen Infection Incidence Slope",
        "refValue": 1.2500,
        "resultUnit": "colonies/seed",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "Colonies = 1.2500 · N + 3.5000",
        "samples": [5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
        "subsystem": "Plant Pathology, Entomology & Crop Protection",
        "focus": "International Seed Testing Association Health Diagnostics",
        "page_path": "/agriculture-forestry/seed-borne-pathogen-blotter-infection-incidence/",
        "theory_path": "/agriculture-forestry/seed-borne-pathogen-blotter-infection-incidence/theory/",
        "report_path": "/agriculture-forestry/seed-borne-pathogen-blotter-infection-incidence/report/"
    },

    # Module 5: Silviculture, Forest Mensuration & Agroforestry (Labs 17–20)
    {
        "num": 17,
        "slug": "forest-stand-basal-area-wedge-prism-relascope",
        "title": "Bitterlich Relascope Angle Gauge & Forest Stand Basal Area (BA)",
        "shortTitle": "Bitterlich Relascope Basal Area",
        "aim": "Determine forest timber stand basal area (m²/ha) using optical wedge prisms and Bitterlich variable radius point sampling theory.",
        "inputLabel": "In-Count Tally Tree Count (Z)",
        "shortInput": "Tally Trees",
        "inputUnit": "trees",
        "min": 6.0,
        "max": 21.0,
        "step": 1.0,
        "initial": 12.0,
        "inputDecimals": 0,
        "rawLabel": "Stand Basal Area (BA)",
        "rawUnit": "m²/ha",
        "rawDecimals": 1,
        "xAxis": "Bitterlich In-Count Tally Z (trees)",
        "yAxis": "Stand Basal Area BA (m²/ha)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 24.0,
        "emptyY": 50.0,
        "targetName": "Basal Area Factor (BAF)",
        "target": "Wedge Prism BAF Multiplier",
        "refValue": 2.0000,
        "resultUnit": "(m²/ha)/tree",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "BA = 2.0000 · Z",
        "samples": [6.0, 9.0, 12.0, 15.0, 18.0, 21.0],
        "subsystem": "Silviculture, Forest Mensuration & Agroforestry",
        "focus": "Forest Inventory & Variable Radius Point Sampling",
        "page_path": "/agriculture-forestry/forest-stand-basal-area-wedge-prism-relascope/",
        "theory_path": "/agriculture-forestry/forest-stand-basal-area-wedge-prism-relascope/theory/",
        "report_path": "/agriculture-forestry/forest-stand-basal-area-wedge-prism-relascope/report/"
    },
    {
        "num": 18,
        "slug": "tree-height-clinometer-hypsometer-allometry",
        "title": "Suunto Optical Clinometer Trigonometric Tree Height & Canopy Allometry",
        "shortTitle": "Tree Height Clinometry",
        "aim": "Measure total timber tree height and merchantable bole length using trigonometric optical clinometers at standardized baseline distances.",
        "inputLabel": "Top Sighting Tangent Angle tan(θ)",
        "shortInput": "tan(θ)",
        "inputUnit": "ratio",
        "min": 0.35,
        "max": 1.10,
        "step": 0.05,
        "initial": 0.65,
        "inputDecimals": 2,
        "rawLabel": "Computed Tree Total Height (H)",
        "rawUnit": "m",
        "rawDecimals": 2,
        "xAxis": "Clinometer Tangent tan(θ) (ratio)",
        "yAxis": "Total Tree Height H (m)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 1.25,
        "emptyY": 30.0,
        "targetName": "Horizontal Baseline Distance (D)",
        "target": "Clinometer Baseline Scaling Distance",
        "refValue": 20.0000,
        "resultUnit": "m",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "H = 20.0000 · tan(θ) + 1.6500",
        "samples": [0.35, 0.50, 0.65, 0.80, 0.95, 1.10],
        "subsystem": "Silviculture, Forest Mensuration & Agroforestry",
        "focus": "Forest Mensuration & Trigonometric Hypsometry",
        "page_path": "/agriculture-forestry/tree-height-clinometer-hypsometer-allometry/",
        "theory_path": "/agriculture-forestry/tree-height-clinometer-hypsometer-allometry/theory/",
        "report_path": "/agriculture-forestry/tree-height-clinometer-hypsometer-allometry/report/"
    },
    {
        "num": 19,
        "slug": "tree-ring-growth-increment-borer-site-index",
        "title": "Pressler Increment Borer Core Annual Growth Ring & Forest Site Index",
        "shortTitle": "Increment Borer Site Index",
        "aim": "Extract tree radial increment cores, measure annual ring width increments, and fit dominant height growth curves to determine forest site quality index (SI).",
        "inputLabel": "Stand Breast-Height Cambial Age (years)",
        "shortInput": "Age",
        "inputUnit": "years",
        "min": 15.0,
        "max": 65.0,
        "step": 5.0,
        "initial": 35.0,
        "inputDecimals": 0,
        "rawLabel": "Dominant Canopy Tree Height",
        "rawUnit": "m",
        "rawDecimals": 2,
        "xAxis": "Stand Age t (years)",
        "yAxis": "Dominant Stand Height H (m)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 70.0,
        "emptyY": 35.0,
        "targetName": "Mean Annual Height Increment Rate",
        "target": "Site Index Growth Slope",
        "refValue": 0.3800,
        "resultUnit": "m/year",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "H = 0.3800 · t + 4.5000",
        "samples": [15.0, 25.0, 35.0, 45.0, 55.0, 65.0],
        "subsystem": "Silviculture, Forest Mensuration & Agroforestry",
        "focus": "Dendrochronology & Forest Stand Productivity Modeling",
        "page_path": "/agriculture-forestry/tree-ring-growth-increment-borer-site-index/",
        "theory_path": "/agriculture-forestry/tree-ring-growth-increment-borer-site-index/theory/",
        "report_path": "/agriculture-forestry/tree-ring-growth-increment-borer-site-index/report/"
    },
    {
        "num": 20,
        "slug": "forest-fuel-moisture-timelag-fire-danger",
        "title": "Forest Fuel Moisture Stick Timelag & National Fire Danger Rating System",
        "shortTitle": "Fuel Moisture Fire Danger",
        "aim": "Calibrate 10-hour ponderosa pine fuel moisture indicator stick equilibria under dynamic atmospheric relative humidity for wildland fire spread prediction.",
        "inputLabel": "Ambient Equilibrium Relative Humidity (%)",
        "shortInput": "RH",
        "inputUnit": "%",
        "min": 20.0,
        "max": 70.0,
        "step": 5.0,
        "initial": 40.0,
        "inputDecimals": 0,
        "rawLabel": "10-Hour Dead Fuel Moisture Content",
        "rawUnit": "%",
        "rawDecimals": 2,
        "xAxis": "Relative Humidity RH (%)",
        "yAxis": "Fuel Moisture Content MC (%)",
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 75.0,
        "emptyY": 18.0,
        "targetName": "Equilibrium Moisture Adsorption Gradient",
        "target": "Fuel Moisture RH Sensitivity Slope",
        "refValue": 0.1750,
        "resultUnit": "%/%",
        "resultDecimals": 4,
        "resultScale": 1.0,
        "fitEquation": "MC = 0.1750 · RH + 2.2000",
        "samples": [20.0, 30.0, 40.0, 50.0, 60.0, 70.0],
        "subsystem": "Silviculture, Forest Mensuration & Agroforestry",
        "focus": "Wildland Fire Physics & Timelag Fuel Dynamics",
        "page_path": "/agriculture-forestry/forest-fuel-moisture-timelag-fire-danger/",
        "theory_path": "/agriculture-forestry/forest-fuel-moisture-timelag-fire-danger/theory/",
        "report_path": "/agriculture-forestry/forest-fuel-moisture-timelag-fire-danger/report/"
    }
]

def make_apparatus(title, focus):
    return [
        {
            "name": f"{title} Calibrated Agricultural Field & Laboratory Testing Station",
            "purpose": f"Provides standardized environmental chamber regulation, precision micro-lysimeter containment, and digital sensor interfacing for {focus}."
        },
        {
            "name": "Precision Analytical Balance & Micro-Moisture Determination Oven",
            "purpose": f"Weighs soil cores, plant tissues, and fuel sticks to ±0.0001 g before and after convective forced-air drying at 105°C during {focus}."
        },
        {
            "name": "Multi-Parameter Soil & Canopy Agro-Meteorological Sensor Array",
            "purpose": f"Monitors matric potential, stomatal conductance, thermal infrared canopy radiance, or volumetric moisture content at high temporal frequencies."
        },
        {
            "name": "Atomic Emission Flame Photometer & UV-Vis Spectrophotometer Unit",
            "purpose": f"Analyzes nutrient extract absorbances and ionic concentrations across certified NIST standard fertilizer and plant tissue digests."
        },
        {
            "name": "Digital Data Acquisition Console & Agro-Hydrological Logger",
            "purpose": f"Records real-time transducer voltage, downhole neutron thermalization counts, or Christiansen micro-irrigation catches."
        },
        {
            "name": "Certified Calibration Buffers, Soil Standards & Field Hypsometers",
            "purpose": f"Ensures sensor zero-drift verification, pH electrode calibration, and optical baseline tracking in compliance with USDA and FAO guidelines."
        }
    ]

def make_procedure(title, shortInput, rawLabel):
    return [
        {
            "title": "Field Sensor Calibration & Environmental Baseline Stabilization",
            "text": f"Inspect all electrode interfaces, ceramic tensiometer cups, or optical sensors. Zero instruments against certified standard solutions or clear sky radiation baselines before commencing {title}."
        },
        {
            "title": "Representative Soil Core / Biological Specimen Sampling",
            "text": f"Extract undisturbed soil cores, representative crop canopy leaves, seed batches, or wood cores according to stratified random sampling guidelines across experimental plots."
        },
        {
            "title": "Instrument Setup & Equilibrium Conditioning",
            "text": f"Mount samples within the testing chamber or attach in-situ probes. Allow 15 minutes of thermal and hydraulic equilibration to achieve steady-state boundary conditions."
        },
        {
            "title": "Systematic Setpoint Execution & Replicated Acquisition",
            "text": f"Systematically adjust {shortInput} across the calibrated operational range. Record steady-state {rawLabel} across at least three replicated determinations per level."
        },
        {
            "title": "Quality Audit & Environmental Interference Correction",
            "text": f"Verify temperature compensation, check for boundary preferential flow or optical scattering artifacts, and confirm that all sensor signals fall within certified calibration envelopes."
        },
        {
            "title": "Data Regression, Parameter Extraction & Scientific Reporting",
            "text": f"Compile observation matrices. Perform ordinary least-squares regression, calculate R² goodness of fit, extract empirical agronomic coefficients against theoretical standards, and verify reproducibility."
        }
    ]

def make_topics(title, targetName, refValue, resultUnit):
    return [
        {
            "question": f"What foundational agro-ecological law or biological principle governs {title}?",
            "answer": f"{title} is governed by soil physics, plant physiological transport, thermodynamics, and ecological energetics, describing how energy, water, and nutrients transfer between soil, vegetation, and the atmosphere."
        },
        {
            "question": f"How is the independent variable calibrated and controlled during the experiment?",
            "answer": f"The independent variable is controlled using regulated environmental growth chambers, certified calibration solutions, precision pressure heads, or optical hypsometers calibrated against traceable standards."
        },
        {
            "question": "Why is quantitative soil and canopy monitoring vital for sustainable agriculture?",
            "answer": "Accurate agronomic modeling prevents waterlogging, excessive fertilizer leaching, and groundwater contamination while optimizing crop yields and timber volume under climate variability."
        },
        {
            "question": "How do boundary layer dynamics and atmospheric humidity affect crop transpiration?",
            "answer": "Vapor pressure deficit (VPD) drives the atmospheric evaporative demand; higher VPD increases transpirational pull until stomatal closure occurs to prevent xylem cavitation."
        },
        {
            "question": f"What biological or physical significance is attributed to {targetName}?",
            "answer": f"The parameter quantifies the fundamental rate or response sensitivity of the agro-ecosystem, exhibiting a benchmark empirical value of {refValue} {resultUnit} under standard field conditions."
        },
        {
            "question": "How are these laboratory measurements scaled up to regional forest or agricultural catchment levels?",
            "answer": "Point measurements are integrated with multispectral satellite remote sensing (Landsat, Sentinel), GIS spatial modeling, and eddy covariance flux towers for regional watershed management."
        }
    ]

def make_precautions():
    return [
        "Avoid soil core compaction and disturbance of natural soil macropores and root channels during cylinder extraction.",
        "Ensure tensiometer ceramic cups are thoroughly de-aired using boiled deionized water to prevent air bubble vapor lock.",
        "Wear protective chemical splash goggles, nitrile gloves, and acid-resistant aprons when handling concentrated nitric and perchloric acid digests.",
        "Perform optical clinometer sightings and leaf stomatal conductance readings under uniform ambient illumination avoiding direct sun glint."
    ]

def make_quiz(title, rawLabel, targetName, refValue, resultUnit):
    return [
        {
            "question": f"In the empirical evaluation of {title}, what represents the primary measured dependent variable?",
            "options": [
                f"{rawLabel} measured under controlled laboratory or field conditions",
                "Uncalibrated visual color estimation of dry topsoil",
                "Arbitrary non-standardized farm worker impressions",
                "Uncontrolled ambient barometric pressure drift"
            ],
            "correct": 0,
            "explanation": f"The experimental protocol directly measures {rawLabel} under calibrated field and laboratory conditions."
        },
        {
            "question": "Which standard sampling strategy is essential to capture spatial heterogeneity in agronomic and forest soils?",
            "options": [
                "Replicated composite sampling across randomized representative field plots",
                "Collecting a single grab sample from the access road entrance",
                "Testing only heavily eroded gullies without vegetative cover",
                "Sampling exclusively during severe nocturnal thunderstorm flooding"
            ],
            "correct": 0,
            "explanation": "Composite sampling across replicated plots averages out fine-scale spatial variability in soil properties."
        },
        {
            "question": f"The standard reference benchmark value for {targetName} is approximately:",
            "options": [
                f"{refValue} {resultUnit}",
                f"{refValue * 10} {resultUnit}",
                f"{refValue * 0.05:.3f} {resultUnit}",
                f"-{refValue * 5} {resultUnit}"
            ],
            "correct": 0,
            "explanation": f"Standard agro-ecological reference benchmarks establish {targetName} at approximately {refValue} {resultUnit}."
        },
        {
            "question": "What does an experimental coefficient of determination R² ≥ 0.999 demonstrate in agricultural calibration models?",
            "options": [
                "Outstanding mathematical linearity and predictive reliability across the investigated operational range",
                "Significant sensor calibration breakdown and severe systemic error",
                "Total absence of correlation between independent treatment and crop response",
                "That physical boundary conditions were violated during observation"
            ],
            "correct": 0,
            "explanation": "An R² ≥ 0.999 demonstrates near-perfect linear fidelity between mathematical models and empirical observations."
        }
    ]

def make_theory(lab):
    t = lab['title']
    aim = lab['aim']
    sub = lab['subsystem']
    eq = lab['fitEquation']
    target = lab['targetName']
    ref = lab['refValue']
    unit = lab['resultUnit']

    return f"""<h3>1. Theoretical Principles of {t}</h3>
<p>Agricultural science, crop physiology, and silviculture constitute the empirical foundation of terrestrial bio-resource management, food security, and forest stewardship. In this university laboratory practical on <strong>{t}</strong>, students explore the biophysical interactions linking soil mineralogy, hydrology, plant nutrition, and forest stand dynamics. The formal objective of this laboratory investigation is to {aim.lower()}</p>

<p>Historically, agronomic and forestry science transitioned from descriptive cultivation lore into exact quantitative disciplines through the foundational work of Justus von Liebig (Law of the Minimum), Henry Darcy (unsaturated porous media flow), and John Monteith (canopy surface energy balance). Modern agricultural systems operate under strict ecological and economic imperatives: maximizing crop water-use efficiency (WUE), nutrient-use efficiency (NUE), and carbon sequestration while mitigating soil salinization, erosion, and pesticide drift. By measuring calibrated physical and biological responses—such as downhole neutron thermalization, canopy infrared thermography, Bray-1 available phosphorus, or Bitterlich relascope basal area—students validate mechanistic models against empirical agricultural reality.</p>

<h3>2. Mathematical Formulation and Governing Relationships</h3>
<p>The mathematical formalism underlying {t} is derived from {sub}. The quantitative relationship governing the observed experimental response is expressed by the fundamental linear and affine regression relationship:</p>
<p style="text-align:center;font-size:16px;font-weight:600;margin:18px 0;color:var(--accent);">
  {eq}
</p>
<p>In this governing equation, the independent setpoint represents the controlled agronomic condition ({lab['shortInput']} in {lab['inputUnit']}), while the dependent variable represents the empirical field measurement ({lab['rawLabel']} in {lab['rawUnit']}). The regression slope directly isolates the critical functional parameter: <strong>{target}</strong>, which possesses a standard empirical benchmark reference value of <code>{ref} {unit}</code> under calibrated standard conditions.</p>

<p>In soil-water-plant continuum (SPAC) theory, water transport from the soil through roots, xylem vessels, mesophyll cells, and stomata to the atmosphere is governed by gradients in total water potential: <em>Ψ = Ψ_p + Ψ_s + Ψ_m + Ψ_g</em> (pressure, solute, matric, and gravitational components). Similarly, the FAO-56 Penman-Monteith equation synthesizes aerodynamic vapor transfer and radiative net energy exchange: <em>ET₀ = [0.408 Δ(R_n - G) + γ (900 / (T + 273)) u₂ (e_s - e_a)] / [Δ + γ(1 + 0.34 u₂)]</em>. In forest inventory, Bitterlich point sampling exploits proportional angles to measure stand basal area without measuring individual tree diameters: <em>BA = BAF · Z</em>, where BAF is the prism basal area factor (m²/ha) and Z is the tally count.</p>

<h3>3. Biophysical Substrates and Ecosystem Processes</h3>
<p>The physical and biological phenomena investigated in this practical are governed by distinct cellular, pedological, and micrometeorological mechanisms:</p>
<ul>
  <li><strong>Colloidal Surface Exchange and Diffuse Double Layer:</strong> Soil clay phyllosilicates (smectite, illite, kaolinite) and humus possess permanent structural charge (isomorphous substitution) and pH-dependent charge (deprotonated carboxyl/phenolic groups) that adsorb exchangeable cations (Ca²⁺, Mg²⁺, K⁺, Na⁺) in equilibrium with soil solution.</li>
  <li><strong>Stomatal Conductance and Canopy Energetics:</strong> Guard cells regulate aperture in response to light, internal CO₂ concentration, and abscisic acid (ABA) xylem signals. Latent heat flux cools the foliage below air temperature; water stress restricts transpiration, elevating leaf temperature detectable via infrared radiometry.</li>
  <li><strong>Porous Media Capillary Suction and Unsaturated Conductivity:</strong> Unsaturated water movement obeys the Richards equation: <em>∂θ/∂t = ∇ · [K(ψ) ∇H]</em>, where hydraulic conductivity K drops precipitously across several orders of magnitude as soil desaturates and drainage empties structural macropores.</li>
  <li><strong>Cambial Increment and Forest Allometry:</strong> Vascular cambium produces seasonal rings composed of wide, thin-walled earlywood (water conduction) and dense, thick-walled latewood (structural support), providing a continuous historical archive of climate sensitivity and stand competition.</li>
</ul>

<h3>4. Experimental Design, Sampling Protocol, and Data Integrity</h3>
<p>To eliminate sampling bias and field variance, rigorous experimental protocols must be enforced:</p>
<ul>
  <li><strong>Spatial Stratification and Composite Sampling:</strong> Field plots must be sampled across representative topographic positions, avoiding headlands, wheel tracks, and fence rows. Subsamples must be combined and homogenized to yield representative composite analytical batches.</li>
  <li><strong>Sample Preservation and Moisture Equilibration:</strong> Soil cores must be trimmed flush with sampling cylinders, sealed against evaporative loss, and stored at 4°C prior to moisture determination or pressure plate analysis.</li>
  <li><strong>Analytical Reagents and Spectrophotometric Blanks:</strong> All reagents (molybdate, ascorbic acid, ammonium acetate) must be prepared with analytical grade deionized water (conductivity < 1 μS/cm), with matrix-matched calibration standards and reagent blanks measured in every analytical run.</li>
  <li><strong>Quality Control Envelopes:</strong> Coefficients of variation among analytical replicates must not exceed 3.0%. Any determination deviating beyond certified quality boundaries must be systematically re-assayed.</li>
</ul>
<p>Through systematic execution of this laboratory practical, students develop essential professional skills in agronomic data acquisition, precision nutrient management, irrigation scheduling, and quantitative silvicultural inventory.</p>"""

def make_report(lab):
    t = lab['title']
    aim = lab['aim']
    sub = lab['subsystem']
    eq = lab['fitEquation']
    target = lab['targetName']
    ref = lab['refValue']
    unit = lab['resultUnit']
    samples = lab['samples']

    return f"""<h3>1. Title and Objective</h3>
<p><strong>{t}.</strong> {aim} This formal laboratory report documents experimental data acquisition, field sensor calibration, ordinary least-squares regression modeling, uncertainty estimation, and parameter verification in accordance with standard agricultural, soil science, and forest inventory protocols.</p>

<h3>2. Theoretical Principles</h3>
<p>Agronomy, soil science, and silviculture rely on rigorous empirical measurements to understand the biophysical dynamics of agro-ecosystems. In {sub}, biological growth, water movement, and nutrient availability follow deterministic physical and chemical laws. By systematically manipulating the independent setpoint—{lab['shortInput']} across a calibrated span from {lab['min']} to {lab['max']} {lab['inputUnit']}—this investigation measures corresponding variations in {lab['rawLabel']} ({lab['rawUnit']}).</p>
<p>The empirical relationship is characterized by the governing regression equation: <code>{eq}</code>. The slope parameter directly yields <strong>{target}</strong>, with a theoretical reference value of <strong>{ref} {unit}</strong>. By tracking physiological rates, chemical extract concentrations, and physical field metrics, this study evaluates the validity of formal agronomic and silvicultural models against empirical field performance data.</p>

<h3>3. Apparatus and Experimental Configuration</h3>
<p>The experimental apparatus consists of a certified agro-ecological laboratory and field testing suite equipped with precision micro-lysimeters, temperature-controlled incubation chambers (±0.2°C stability), and digital sensor interfaces. Soil moisture was monitored via downhole neutron moderation probes and mercury-manometer ceramic tensiometers. Foliar nutrient concentrations were quantified using atomic emission flame photometry (766.5 nm) and UV-Vis spectrophotometry (882 nm) following wet acid digestion. Forest stand parameters were acquired using certified Suunto optical clinometers and precision Bitterlich optical wedge prisms calibrated to a basal area factor of 2.0 m²/ha.</p>

<h3>4. Standard Operating Procedure</h3>
<p>Prior to formal data collection, all electrodes, photometers, and pressure transducers were calibrated against certified analytical reference standards. Undisturbed soil core samples were extracted using standard stainless-steel core rings (100 cm³ volume) and trimmed to exact dimensions. Biological tissue samples were oven-dried at 65°C to constant weight and ground through a 40-mesh stainless-steel sieve. During formal acquisition, the independent variable was tested across 6 calibrated setpoints: {', '.join(str(s) for s in samples)} {lab['inputUnit']}. Each setpoint was sampled across replicated determinations with continuous baseline monitoring to confirm environmental steady-state equilibrium.</p>

<h3>5. Experimental Data and Observations</h3>
<p>The table below summarizes empirical observation values obtained across the complete parameter space under calibrated laboratory and field conditions:</p>
<table class="data-table">
  <thead>
    <tr>
      <th>Sample Run</th>
      <th>{lab['inputLabel']} (x)</th>
      <th>Raw {lab['rawLabel']} (y)</th>
      <th>Transformed x'</th>
      <th>Transformed y'</th>
      <th>Verification Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>{samples[0]} {lab['inputUnit']}</td><td>Calibrated Observation</td><td>{samples[0]:.3f}</td><td>Empirical</td><td>Verified (Valid)</td></tr>
    <tr><td>2</td><td>{samples[1]} {lab['inputUnit']}</td><td>Calibrated Observation</td><td>{samples[1]:.3f}</td><td>Empirical</td><td>Verified (Valid)</td></tr>
    <tr><td>3</td><td>{samples[2]} {lab['inputUnit']}</td><td>Calibrated Observation</td><td>{samples[2]:.3f}</td><td>Empirical</td><td>Verified (Valid)</td></tr>
    <tr><td>4</td><td>{samples[3]} {lab['inputUnit']}</td><td>Calibrated Observation</td><td>{samples[3]:.3f}</td><td>Empirical</td><td>Verified (Valid)</td></tr>
    <tr><td>5</td><td>{samples[4]} {lab['inputUnit']}</td><td>Calibrated Observation</td><td>{samples[4]:.3f}</td><td>Empirical</td><td>Verified (Valid)</td></tr>
    <tr><td>6</td><td>{samples[5]} {lab['inputUnit']}</td><td>Calibrated Observation</td><td>{samples[5]:.3f}</td><td>Empirical</td><td>Verified (Valid)</td></tr>
  </tbody>
</table>

<h3>6. Quantitative Calculations and Uncertainty Analysis</h3>
<p>Ordinary least-squares (OLS) linear regression was performed on the six paired observation coordinates. Sum of squares decomposition yielded: <em>SS_tot = Σ(y_i - ȳ)²</em>, <em>SS_res = Σ(y_i - ŷ_i)²</em>, and <em>R² = 1 - (SS_res / SS_tot)</em>. The empirical slope was computed via: <em>m = [N Σ(x_i y_i) - (Σx_i)(Σy_i)] / [N Σ(x_i²) - (Σx_i)²]</em>. Standard errors for slope and intercept were determined using the residual variance: <em>s² = SS_res / (N - 2)</em>, yielding <em>SE_m = sqrt(s² / Σ(x_i - x̄)²)</em>. The resulting empirical parameter was compared against standard reference values via relative percentage deviation: <em>% Dev = |m_obs - m_ref| / m_ref × 100%</em>.</p>

<h3>7. Results and Calibration Summary</h3>
<p>The linear regression model achieved an exceptional goodness-of-fit correlation coefficient of <strong>R² ≥ 0.9995</strong> across all tested levels, demonstrating remarkable agreement between theoretical mathematical predictions and empirical field data. The calculated value for <strong>{target}</strong> is <strong>{ref:.4f} {unit}</strong>, matching the published agronomic reference standard of <strong>{ref} {unit}</strong> with a relative discrepancy below 0.1%. Residual analysis confirmed zero systematic curvature or heteroscedasticity across the independent variable continuum.</p>

<h3>8. Discussion and Physical Significance</h3>
<p>The experimental findings confirm the foundational validity of biophysical transport and allometric scaling models in agriculture and forestry. The robust linear relationship demonstrates that agricultural processes—such as seed germination energetics, soil moisture neutron thermalization, canopy evaporative cooling, nutrient adsorption, and forest timber accumulation—follow predictable physical mechanics. In {t}, the observed parameter highlights the critical role of standardized calibration in precision farming, preventing resource over-application and maximizing ecological efficiency.</p>

<h3>9. Sources of Experimental Error and Mitigation</h3>
<p>Potential sources of variance in agronomic and forest measurements include: (a) soil structural heterogeneity and natural stone/gravel fractions altering core dry bulk density; (b) localized preferential flow and macropore channeling along tensiometer shafts; (c) temperature fluctuations during colorimetric spectrophotometer equilibration; and (d) optical clinometer sighting errors caused by dense understory foliage. These factors were systematically mitigated by: employing stratified composite core extraction, thorough de-airing of ceramic porous cups, temperature-controlled water baths, and laser rangefinder distance verification.</p>

<h3>10. Industrial, Geological, and Field Applications</h3>
<p>The quantitative principles elucidated by this laboratory investigation have direct applied relevance in precision agriculture, irrigation engineering, watershed hydrological modeling, commercial timber inventory, and wildland wildfire risk management. Agricultural extension services, commercial agribusinesses, and forestry departments utilize these exact mathematical models (e.g., FAO-56 Penman-Monteith, Kostiakov infiltration, Bitterlich variable radius sampling) to optimize variable-rate fertilizer prescriptions, design drip irrigation distribution networks, and forecast forest timber yield tables.</p>

<h3>11. Conclusions and Methodological Recommendations</h3>
<p>The laboratory practical successfully verified the quantitative laws governing {t}. The empirical parameter {target} was determined to high statistical precision (R² ≥ 0.9995, deviation < 0.1% vs reference standard). For future experimental extensions, it is recommended to integrate multispectral drone remote sensing (NDVI/NDRE), automated sap-flow thermal dissipation probes, and wireless IoT soil capacitance arrays to monitor crop water dynamics in real-time under fluctuating field microclimates.</p>

<h3>12. References and Standard Protocols</h3>
<p>1. Allen, R. G., Pereira, L. S., Raes, D., & Smith, M. (1998). <em>Crop evapotranspiration: Guidelines for computing crop water requirements</em>. FAO Irrigation and Drainage Paper 56, Rome.<br>
2. Sparks, D. L. (Ed.). (1996). <em>Methods of Soil Analysis, Part 3: Chemical Methods</em>. Soil Science Society of America, Madison, WI.<br>
3. Avery, T. E., & Burkhart, H. E. (2015). <em>Forest Measurements</em> (5th ed.). Waveland Press, Long Grove, IL.<br>
4. International Seed Testing Association (ISTA). (2021). <em>International Rules for Seed Testing</em>. Bassersdorf, Switzerland.<br>
5. USDA Natural Resources Conservation Service (NRCS). (2014). <em>Soil Survey Field and Laboratory Methods Manual</em>. Soil Survey Investigations Report No. 51.</p>
<p><em>Simulated demonstration data.</em></p>"""

full_labs = []
for lab in LABS:
    entry = dict(lab)
    entry["apparatus"] = make_apparatus(lab['title'], lab['focus'])
    entry["procedure"] = make_procedure(lab['title'], lab['shortInput'], lab['rawLabel'])
    entry["topics"] = make_topics(lab['title'], lab['targetName'], lab['refValue'], lab['resultUnit'])
    entry["precautions"] = make_precautions()
    entry["quiz"] = make_quiz(lab['title'], lab['rawLabel'], lab['targetName'], lab['refValue'], lab['resultUnit'])
    entry["theory"] = make_theory(lab)
    entry["report"] = make_report(lab)
    full_labs.append(entry)

out_file = ROOT / 'content/agriculture_forestry/experiments.json'
out_file.write_text(json.dumps(full_labs, indent=2, ensure_ascii=False), encoding='utf-8')
print(f"Successfully wrote {len(full_labs)} agriculture & forestry experiments to {out_file}")
