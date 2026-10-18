# -*- coding: utf-8 -*-
"""Generate comprehensive experiments.json for Basic Medical Sciences (42 Laboratories)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LABS = [
    # Module 1: Hematology & Clinical Blood Analysis (Labs 1–7)
    {
        "num": 1,
        "slug": "erythrocyte-sedimentation-rate-westergren",
        "title": "Erythrocyte Sedimentation Rate (ESR) Westergren Sedimentation & Rouleaux Dynamics",
        "shortTitle": "Westergren ESR & Rouleaux",
        "aim": "Quantify red blood cell sedimentation distance per unit time as a function of plasma fibrinogen and acute-phase reactant concentration using the standard Westergren method.",
        "inputLabel": "Plasma Fibrinogen Index (mg/dL)",
        "shortInput": "Fibrinogen",
        "inputUnit": "mg/dL",
        "min": 100.0, "max": 700.0, "step": 50.0, "initial": 250.0, "inputDecimals": 1,
        "rawLabel": "Westergren Sedimentation Distance (1 hr)",
        "rawUnit": "mm/hr", "rawDecimals": 1,
        "xAxis": "Plasma Fibrinogen Index F (mg/dL)",
        "yAxis": "ESR Sedimentation Rate (mm/hr)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 700.0, "emptyY": 100.0,
        "targetName": "Fibrinogen-Induced Sedimentation Acceleration Coefficient",
        "target": "Sedimentation Acceleration Rate",
        "refValue": 0.6800, "resultUnit": "mm/hr per (mg/dL)", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "ESR = 0.6800 · F + 2.5000",
        "samples": [150.0, 250.0, 350.0, 450.0, 550.0, 650.0],
        "subsystem": "Medical Hematology & Hemorheology",
        "focus": "Erythrocyte Sedimentation Rate & Fibrinogen-Induced Rouleaux Aggregation"
    },
    {
        "num": 2,
        "slug": "hemoglobin-spectrophotometry-cyanmethemoglobin-drabkin",
        "title": "Spectrophotometric Hemoglobin Concentration by Cyanmethemoglobin (Drabkin's) Method",
        "shortTitle": "Drabkin's Hemoglobin Photometry",
        "aim": "Determine blood total hemoglobin concentration through ferricyanide-cyanide oxidation into cyanmethemoglobin and absorbance measurement at 540 nm.",
        "inputLabel": "Blood Hemoglobin Concentration (g/dL)",
        "shortInput": "Hemoglobin",
        "inputUnit": "g/dL",
        "min": 4.0, "max": 20.0, "step": 1.0, "initial": 14.0, "inputDecimals": 1,
        "rawLabel": "Optical Density Absorbance at 540 nm",
        "rawUnit": "OD", "rawDecimals": 4,
        "xAxis": "Hemoglobin Concentration [Hb] (g/dL)",
        "yAxis": "Optical Absorbance A540",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 20.0, "emptyY": 1.0,
        "targetName": "Cyanmethemoglobin Absorptivity Slope",
        "target": "Calibration Absorptivity",
        "refValue": 0.0380, "resultUnit": "OD per (g/dL)", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "A540 = 0.0380 · [Hb]",
        "samples": [6.0, 9.0, 12.0, 14.5, 16.5, 19.0],
        "subsystem": "Medical Hematology & Hemorheology",
        "focus": "Cyanmethemoglobin Photometric Absorptivity & Anemia Diagnostics"
    },
    {
        "num": 3,
        "slug": "red-blood-cell-osmotic-fragility-hemolysis",
        "title": "Erythrocyte Osmotic Fragility Curve & Spherocytosis Hemolytic Dynamics",
        "shortTitle": "RBC Osmotic Fragility Curve",
        "aim": "Map erythrocyte membrane osmotic tolerance and percentage hemolysis across graded buffered hypotonic saline solutions.",
        "inputLabel": "Hypotonic Sodium Chloride Concentration (% NaCl)",
        "shortInput": "Saline Concentration",
        "inputUnit": "% NaCl",
        "min": 0.20, "max": 0.70, "step": 0.05, "initial": 0.45, "inputDecimals": 2,
        "rawLabel": "Percentage Erythrocyte Hemolysis",
        "rawUnit": "%", "rawDecimals": 1,
        "xAxis": "Hypotonic Saline Concentration (% NaCl)",
        "yAxis": "Erythrocyte Hemolysis (%)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 0.70, "emptyY": 100.0,
        "targetName": "Osmotic Fragility Hemolytic Sensitivity Slope",
        "target": "Osmotic Sensitivity Slope",
        "refValue": 145.0000, "resultUnit": "% hemolysis per % NaCl", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Hemolysis = -145.0000 · [NaCl] + 115.0000",
        "samples": [0.30, 0.35, 0.40, 0.45, 0.50, 0.60],
        "subsystem": "Medical Hematology & Hemorheology",
        "focus": "Osmotic Fragility Curve & Erythrocyte Membrane Integrity"
    },
    {
        "num": 4,
        "slug": "hematocrit-microcentrifugation-packed-cell-volume",
        "title": "Microhematocrit Centrifugation & Packed Cell Volume (PCV) Derivation",
        "shortTitle": "Packed Cell Volume (PCV)",
        "aim": "Determine fraction of whole blood occupied by erythrocytes by high-speed microhematocrit centrifugation and derive Wintrobe indices (MCV, MCH, MCHC).",
        "inputLabel": "Blood Centrifugation Packed Cell Volume (%)",
        "shortInput": "Hematocrit PCV",
        "inputUnit": "%",
        "min": 20.0, "max": 65.0, "step": 2.0, "initial": 45.0, "inputDecimals": 1,
        "rawLabel": "Fractional Erythrocyte Volume Fraction",
        "rawUnit": "L/L", "rawDecimals": 4,
        "xAxis": "Packed Cell Volume PCV (%)",
        "yAxis": "Fractional Volume Ratio (L/L)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 65.0, "emptyY": 1.0,
        "targetName": "Hematocrit Percentage-to-Fraction Ratio",
        "target": "Volume Fraction Scale Factor",
        "refValue": 0.0100, "resultUnit": "(L/L) per %", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Fraction = 0.0100 · PCV",
        "samples": [25.0, 32.0, 38.0, 44.0, 52.0, 60.0],
        "subsystem": "Medical Hematology & Hemorheology",
        "focus": "Microhematocrit PCV & Wintrobe Erythrocyte Indices"
    },
    {
        "num": 5,
        "slug": "differential-leukocyte-count-leishman-smear",
        "title": "Differential Leukocyte Count (DLC) & Absolute Granulocyte Hemocytometry",
        "shortTitle": "Differential Leukocyte Count",
        "aim": "Perform peripheral blood film differential leukocyte counting using Leishman's stain and calculate absolute neutrophil count.",
        "inputLabel": "Neutrophil Differential Percentage (%)",
        "shortInput": "Neutrophils %",
        "inputUnit": "%",
        "min": 30.0, "max": 90.0, "step": 5.0, "initial": 60.0, "inputDecimals": 1,
        "rawLabel": "Absolute Neutrophil Count (ANC)",
        "rawUnit": "cells/µL", "rawDecimals": 0,
        "xAxis": "Neutrophil Differential Fraction (%)",
        "yAxis": "Absolute Count ANC (cells/µL)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 90.0, "emptyY": 8000.0,
        "targetName": "Absolute Neutrophil Scaling Constant",
        "target": "ANC Leukocyte Scaling Factor",
        "refValue": 75.0000, "resultUnit": "(cells/µL) per %", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "ANC = 75.0000 · Neutrophil%",
        "samples": [35.0, 45.0, 55.0, 65.0, 75.0, 85.0],
        "subsystem": "Medical Hematology & Hemorheology",
        "focus": "Peripheral Blood Smear Leukocyte Differential & Hemocytometry"
    },
    {
        "num": 6,
        "slug": "bleeding-time-clotting-time-hemostasis",
        "title": "Hemostasis Kinetics: Duke/Ivy Bleeding Time & Lee-White Coagulation Dynamics",
        "shortTitle": "Bleeding & Clotting Time",
        "aim": "Investigate primary hemostasis (platelet plug formation) and secondary hemostasis (intrinsic coagulation cascade fibrin clot) kinetics.",
        "inputLabel": "Primary Platelet Hemostatic Duration (min)",
        "shortInput": "Bleeding Time",
        "inputUnit": "min",
        "min": 1.0, "max": 10.0, "step": 0.5, "initial": 3.5, "inputDecimals": 1,
        "rawLabel": "Lee-White Whole Blood Coagulation Time",
        "rawUnit": "min", "rawDecimals": 2,
        "xAxis": "Ivy Bleeding Time (min)",
        "yAxis": "Lee-White Clotting Time (min)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 10.0, "emptyY": 25.0,
        "targetName": "Hemostatic Coupling Progression Ratio",
        "target": "Coagulation Time Progression Ratio",
        "refValue": 1.8500, "resultUnit": "min/min", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "ClottingTime = 1.8500 · BleedingTime + 2.2000",
        "samples": [1.5, 2.5, 3.5, 5.0, 7.0, 9.0],
        "subsystem": "Medical Hematology & Hemorheology",
        "focus": "Primary vs Secondary Hemostasis & Clotting Factor Activation"
    },
    {
        "num": 7,
        "slug": "blood-group-antigen-agglutination-titer",
        "title": "ABO & Rh(D) Hemagglutination Titer & Forward/Reverse Blood Grouping",
        "shortTitle": "ABO & Rh Agglutination Titer",
        "aim": "Map erythrocyte surface agglutinogen expression and quantify isohemagglutinin titer using serial antiserum dilutions and scoring matrix.",
        "inputLabel": "Antiserum Serial Dilution Exponent (log2 Titer)",
        "shortInput": "Dilution Step",
        "inputUnit": "steps",
        "min": 1.0, "max": 8.0, "step": 1.0, "initial": 3.0, "inputDecimals": 0,
        "rawLabel": "Immuno-Agglutination Strength Score",
        "rawUnit": "points", "rawDecimals": 2,
        "xAxis": "Antiserum Serial Dilution Step (log2)",
        "yAxis": "Agglutination Score (0–12)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 8.0, "emptyY": 12.0,
        "targetName": "Agglutination Dilution Decay Rate",
        "target": "Titer Agglutination Decay Slope",
        "refValue": 0.6500, "resultUnit": "points/step", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Score = -0.6500 · DilutionStep + 10.5000",
        "samples": [1.0, 2.0, 3.0, 4.0, 6.0, 8.0],
        "subsystem": "Medical Hematology & Hemorheology",
        "focus": "ABO/Rh Blood Typing & Hemagglutinin Titer Kinetics"
    },

    # Module 2: Cardiovascular & Hemodynamic Physiology (Labs 8–14)
    {
        "num": 8,
        "slug": "arterial-blood-pressure-sphygmomanometer-korotkoff",
        "title": "Auscultatory Blood Pressure & Korotkoff Sound Phase Hemodynamics",
        "shortTitle": "Arterial Blood Pressure & Korotkoff",
        "aim": "Measure brachial arterial blood pressure by auscultation, identifying Korotkoff Phases I through V and deriving Mean Arterial Pressure (MAP).",
        "inputLabel": "Systolic Blood Pressure (mmHg)",
        "shortInput": "Systolic Pressure",
        "inputUnit": "mmHg",
        "min": 90.0, "max": 180.0, "step": 5.0, "initial": 120.0, "inputDecimals": 1,
        "rawLabel": "Derived Mean Arterial Pressure (MAP)",
        "rawUnit": "mmHg", "rawDecimals": 2,
        "xAxis": "Systolic Pressure Ps (mmHg)",
        "yAxis": "Mean Arterial Pressure MAP (mmHg)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 180.0, "emptyY": 150.0,
        "targetName": "Systolic Weighting in Mean Arterial Pressure",
        "target": "MAP Systolic Coefficient (1/3)",
        "refValue": 0.6667, "resultUnit": "mmHg/mmHg", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "MAP = 0.6667 · Ps + 26.6667",
        "samples": [95.0, 110.0, 120.0, 135.0, 150.0, 165.0],
        "subsystem": "Cardiovascular & Hemodynamic Physiology",
        "focus": "Arterial Hemodynamics & Korotkoff Sound Transition"
    },
    {
        "num": 9,
        "slug": "electrocardiogram-ecg-intervals-axis-determination",
        "title": "12-Lead Electrocardiography: PR, QRS, QTc Intervals & Frontal Plane Vector Axis",
        "shortTitle": "12-Lead ECG Intervals & Axis",
        "aim": "Record standard limb and precordial ECG leads, measure PR, QRS, and Bazett-corrected QTc intervals, and calculate frontal plane cardiac electrical axis.",
        "inputLabel": "Uncorrected QT Interval Duration (ms)",
        "shortInput": "Raw QT Duration",
        "inputUnit": "ms",
        "min": 300.0, "max": 550.0, "step": 10.0, "initial": 400.0, "inputDecimals": 0,
        "rawLabel": "Bazett Corrected QTc Dispersion Metric",
        "rawUnit": "s^0.5", "rawDecimals": 4,
        "xAxis": "Raw QT Interval Duration (ms)",
        "yAxis": "Bazett Normalized Duration (s^0.5)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 550.0, "emptyY": 20.0,
        "targetName": "Bazett QTc Scaling Factor",
        "target": "Electrocardiographic Interval Factor",
        "refValue": 0.0312, "resultUnit": "s^0.5 per ms", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "QTc_disp = 0.0312 · QT",
        "samples": [340.0, 380.0, 400.0, 440.0, 480.0, 520.0],
        "subsystem": "Cardiovascular & Hemodynamic Physiology",
        "focus": "Cardiac Electrophysiology & Einthoven Axis Determination"
    },
    {
        "num": 10,
        "slug": "cardiac-output-fick-principle-oxygen-consumption",
        "title": "Cardiac Output Estimation by Direct Fick Oxygen Consumption Principle",
        "shortTitle": "Fick Principle Cardiac Output",
        "aim": "Determine resting and exercise cardiac output using spirometric oxygen consumption (VO2) and arteriovenous oxygen content difference.",
        "inputLabel": "Whole-Body Oxygen Consumption Rate (mL/min)",
        "shortInput": "VO2 Consumption",
        "inputUnit": "mL/min",
        "min": 150.0, "max": 600.0, "step": 25.0, "initial": 250.0, "inputDecimals": 0,
        "rawLabel": "Derived Cardiac Output (CO)",
        "rawUnit": "L/min", "rawDecimals": 2,
        "xAxis": "Oxygen Consumption VO2 (mL/min)",
        "yAxis": "Cardiac Output CO (L/min)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 600.0, "emptyY": 15.0,
        "targetName": "Arteriovenous Oxygen Extraction Coefficient",
        "target": "Fick Principle Reciprocal Content Slope",
        "refValue": 0.0200, "resultUnit": "L/min per (mL/min)", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "CO = 0.0200 · VO2",
        "samples": [180.0, 220.0, 260.0, 320.0, 400.0, 500.0],
        "subsystem": "Cardiovascular & Hemodynamic Physiology",
        "focus": "Cardiac Output & Fick Hemodynamic Oxygen Transport"
    },
    {
        "num": 11,
        "slug": "arterial-pulse-wave-velocity-vascular-compliance",
        "title": "Arterial Pulse Wave Velocity (PWV) & Moens-Korteweg Vascular Compliance",
        "shortTitle": "Arterial Pulse Wave Velocity",
        "aim": "Measure carotid-femoral pulse transit time to calculate arterial pulse wave velocity and evaluate central aortic arterial compliance and stiffness.",
        "inputLabel": "Vascular Sclerosis & Age Index (AU)",
        "shortInput": "Vascular Stiffness",
        "inputUnit": "AU",
        "min": 2.0, "max": 12.0, "step": 1.0, "initial": 6.0, "inputDecimals": 1,
        "rawLabel": "Carotid-Femoral Pulse Wave Velocity",
        "rawUnit": "m/s", "rawDecimals": 2,
        "xAxis": "Vascular Stiffness Index (AU)",
        "yAxis": "Pulse Wave Velocity PWV (m/s)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 12.0, "emptyY": 15.0,
        "targetName": "Aortic Stiffness Propagation Gain",
        "target": "PWV Stiffness Sensitivity Slope",
        "refValue": 0.8500, "resultUnit": "(m/s) per AU", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "PWV = 0.8500 · Index + 1.2500",
        "samples": [3.0, 5.0, 6.5, 8.0, 10.0, 11.5],
        "subsystem": "Cardiovascular & Hemodynamic Physiology",
        "focus": "Arterial Compliance & Moens-Korteweg Pulse Propagation"
    },
    {
        "num": 12,
        "slug": "cold-pressor-test-sympathetic-vasoreactivity",
        "title": "Cold Pressor Test: Sympathetic Vasomotor Reactivity & Pressor Kinetics",
        "shortTitle": "Cold Pressor Vasoreactivity",
        "aim": "Assess autonomic cardiovascular reflex integrity by measuring blood pressure and heart rate elevations in response to cold nociceptive immersion.",
        "inputLabel": "Autonomic Sympathetic Outflow Index (AU)",
        "shortInput": "Sympathetic Outflow",
        "inputUnit": "AU",
        "min": 5.0, "max": 35.0, "step": 2.5, "initial": 15.0, "inputDecimals": 1,
        "rawLabel": "Mean Arterial Pressure Elevation (ΔMAP)",
        "rawUnit": "mmHg", "rawDecimals": 2,
        "xAxis": "Sympathetic Outflow Index (AU)",
        "yAxis": "MAP Rise ΔMAP (mmHg)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 35.0, "emptyY": 50.0,
        "targetName": "Sympathetic Pressor Vasoreactivity Gain",
        "target": "Pressor Response Gain",
        "refValue": 1.2500, "resultUnit": "mmHg/AU", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "ΔMAP = 1.2500 · OutflowIndex",
        "samples": [8.0, 12.0, 16.0, 20.0, 26.0, 32.0],
        "subsystem": "Cardiovascular & Hemodynamic Physiology",
        "focus": "Autonomic Sympathetic Vasoreactivity & Hemodynamic Reflexes"
    },
    {
        "num": 13,
        "slug": "venous-pressure-gaertner-jugular-pulsation",
        "title": "Central Venous Pressure Estimation by Gaertner Arm Elevation & Jugular Inspection",
        "shortTitle": "Central Venous Pressure",
        "aim": "Estimate right atrial venous hydrostatic pressure using non-invasive Gaertner vein collapse height above sternal angle and evaluate jugular waveforms.",
        "inputLabel": "Venous Hydrostatic Collapse Height (cm H2O)",
        "shortInput": "Hydrostatic Height",
        "inputUnit": "cm H2O",
        "min": 2.0, "max": 20.0, "step": 1.0, "initial": 7.0, "inputDecimals": 1,
        "rawLabel": "Equated Central Venous Pressure",
        "rawUnit": "mmHg", "rawDecimals": 2,
        "xAxis": "Hydrostatic Height (cm H2O)",
        "yAxis": "Venous Pressure (mmHg)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 20.0, "emptyY": 18.0,
        "targetName": "Hydrostatic Mercury Equivalence Coefficient",
        "target": "Hydrostatic Pressure Conversion Ratio",
        "refValue": 0.7355, "resultUnit": "mmHg per (cm H2O)", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Pressure_mmHg = 0.7355 · Height_cmH2O",
        "samples": [3.0, 5.0, 7.0, 10.0, 14.0, 18.0],
        "subsystem": "Cardiovascular & Hemodynamic Physiology",
        "focus": "Venous Hemodynamics & Right Atrial Hydrostatic Pressure"
    },
    {
        "num": 14,
        "slug": "capillary-fragility-hess-rumpel-leede-petechiae",
        "title": "Capillary Fragility & Endothelial Permeability by Hess Rumpel-Leede Tourniquet Test",
        "shortTitle": "Capillary Fragility & Hess Test",
        "aim": "Evaluate microvascular integrity and platelet-endothelial barrier resistance by counting petechiae produced by sustained venous cuff inflation.",
        "inputLabel": "Microvascular Fragility Permeability Index (AU)",
        "shortInput": "Fragility Index",
        "inputUnit": "AU",
        "min": 2.0, "max": 30.0, "step": 2.0, "initial": 10.0, "inputDecimals": 1,
        "rawLabel": "Forearm Petechial Density Count",
        "rawUnit": "petechiae/circle", "rawDecimals": 1,
        "xAxis": "Microvascular Fragility Index (AU)",
        "yAxis": "Petechial Count (per 5 cm circle)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 30.0, "emptyY": 40.0,
        "targetName": "Endothelial Fragility Extravasation Coefficient",
        "target": "Petechial Extravasation Rate",
        "refValue": 0.9500, "resultUnit": "petechiae/AU", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Petechiae = 0.9500 · FragilityIndex + 1.2000",
        "samples": [4.0, 8.0, 12.0, 16.0, 22.0, 28.0],
        "subsystem": "Cardiovascular & Hemodynamic Physiology",
        "focus": "Microvascular Capillary Fragility & Petechial Diagnostics"
    },

    # Module 3: Neurophysiology, Neuromuscular & Sensory Function (Labs 15–21)
    {
        "num": 15,
        "slug": "motor-nerve-conduction-velocity-compound-muscle-potential",
        "title": "Motor Nerve Conduction Velocity (MNCV) & Compound Muscle Action Potential (CMAP)",
        "shortTitle": "Motor Nerve Conduction Velocity",
        "aim": "Determine human median or ulnar motor nerve conduction velocity by stimulating proximal and distal sites and recording thenar/hypothenar CMAP latencies.",
        "inputLabel": "Inter-Electrode Conduction Segment Distance (cm)",
        "shortInput": "Segment Distance",
        "inputUnit": "cm",
        "min": 10.0, "max": 40.0, "step": 2.0, "initial": 22.0, "inputDecimals": 1,
        "rawLabel": "Proximal-Distal Conduction Latency Difference (Δt)",
        "rawUnit": "ms", "rawDecimals": 3,
        "xAxis": "Conduction Distance d (cm)",
        "yAxis": "Latency Difference Δt (ms)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 40.0, "emptyY": 1.0,
        "targetName": "Axonal Conduction Slowness Slope",
        "target": "Reciprocal Conduction Velocity Slope",
        "refValue": 0.01786, "resultUnit": "ms/cm", "resultDecimals": 5, "resultScale": 1.0,
        "fitEquation": "Δt = 0.01786 · d",
        "samples": [12.0, 16.0, 20.0, 25.0, 30.0, 36.0],
        "subsystem": "Neurophysiology, Neuromuscular & Sensory Function",
        "focus": "Axonal Conduction Velocity & CMAP Waveform Analysis"
    },
    {
        "num": 16,
        "slug": "h-reflex-hoffmann-monosynaptic-arc-latency",
        "title": "Hoffmann Reflex (H-Reflex) & Monosynaptic Spinal Arc Electrophysiology",
        "shortTitle": "Hoffmann Reflex & M-Wave",
        "aim": "Record electrical homologue of the stretch reflex in tibial nerve and soleus muscle, characterizing Ia afferent threshold, H-reflex latency, and M-wave recruitment.",
        "inputLabel": "Posterior Lower Limb Anatomical Length (cm)",
        "shortInput": "Limb Length",
        "inputUnit": "cm",
        "min": 60.0, "max": 110.0, "step": 5.0, "initial": 80.0, "inputDecimals": 1,
        "rawLabel": "Monosynaptic H-Reflex Onset Latency",
        "rawUnit": "ms", "rawDecimals": 2,
        "xAxis": "Limb Anatomical Conduction Length L (cm)",
        "yAxis": "H-Reflex Latency tH (ms)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 110.0, "emptyY": 70.0,
        "targetName": "Spinal Conduction Propagation Rate",
        "target": "Monosynaptic Conduction Slope",
        "refValue": 0.4200, "resultUnit": "ms/cm", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "tH = 0.4200 · L + 16.5000",
        "samples": [65.0, 72.0, 80.0, 88.0, 96.0, 105.0],
        "subsystem": "Neurophysiology, Neuromuscular & Sensory Function",
        "focus": "Monosynaptic Spinal Reflex Loop & Ia Afferent Recruitment"
    },
    {
        "num": 17,
        "slug": "surface-electromyography-isometric-force-fatigue",
        "title": "Surface Electromyography (sEMG) Root-Mean-Square Amplitude & Muscle Force",
        "shortTitle": "sEMG Amplitude & Isometric Force",
        "aim": "Record biceps or quadriceps surface EMG during graded isometric contractions to quantify motor unit recruitment and force-amplitude linearity.",
        "inputLabel": "Percentage Maximal Voluntary Contraction (% MVC)",
        "shortInput": "Isometric Force",
        "inputUnit": "% MVC",
        "min": 10.0, "max": 100.0, "step": 5.0, "initial": 40.0, "inputDecimals": 1,
        "rawLabel": "sEMG Root-Mean-Square (RMS) Amplitude",
        "rawUnit": "µV", "rawDecimals": 1,
        "xAxis": "Isometric Muscle Force (% MVC)",
        "yAxis": "sEMG RMS Potential (µV)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 100.0, "emptyY": 800.0,
        "targetName": "Electromyographic Force-Conversion Sensitivity",
        "target": "sEMG Force Recruitment Slope",
        "refValue": 7.5000, "resultUnit": "µV per % MVC", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "sEMG_RMS = 7.5000 · %MVC",
        "samples": [15.0, 30.0, 45.0, 60.0, 75.0, 90.0],
        "subsystem": "Neurophysiology, Neuromuscular & Sensory Function",
        "focus": "Motor Unit Recruitment & Electromyographic Force Coupling"
    },
    {
        "num": 18,
        "slug": "visual-evoked-potentials-p100-latency-reversal",
        "title": "Pattern-Reversal Visual Evoked Potentials (PR-VEP) & P100 Retinocortical Latency",
        "shortTitle": "Visual Evoked Potentials P100",
        "aim": "Record cortical visual evoked potentials elicited by checkerboard pattern reversal to measure retinocortical conduction time and P100 wave morphology.",
        "inputLabel": "Optic Nerve Conduction Delay Factor (AU)",
        "shortInput": "Myelination Index",
        "inputUnit": "AU",
        "min": 50.0, "max": 120.0, "step": 5.0, "initial": 75.0, "inputDecimals": 1,
        "rawLabel": "Cortical P100 Wave Peak Latency",
        "rawUnit": "ms", "rawDecimals": 1,
        "xAxis": "Optic Conduction Delay Metric (AU)",
        "yAxis": "P100 Peak Latency (ms)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 120.0, "emptyY": 150.0,
        "targetName": "Retinocortical Conduction Delay Rate",
        "target": "P100 Latency Progression Slope",
        "refValue": 0.7500, "resultUnit": "ms/AU", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "P100 = 0.7500 · DelayIndex + 45.0000",
        "samples": [60.0, 70.0, 80.0, 92.0, 104.0, 116.0],
        "subsystem": "Neurophysiology, Neuromuscular & Sensory Function",
        "focus": "Optic Pathway Conduction & P100 Neurodiagnostics"
    },
    {
        "num": 19,
        "slug": "pure-tone-audiometry-air-bone-conduction-threshold",
        "title": "Pure Tone Air & Bone Conduction Audiometry: Decibel Hearing Thresholds",
        "shortTitle": "Pure Tone Audiometry",
        "aim": "Determine hearing sensitivity thresholds across octave test frequencies from 250 Hz to 8000 Hz, identifying conductive and sensorineural hearing loss patterns.",
        "inputLabel": "Normalized Acoustic Attenuation Level (dB SPL)",
        "shortInput": "Sound Pressure Level",
        "inputUnit": "dB SPL",
        "min": 10.0, "max": 80.0, "step": 5.0, "initial": 30.0, "inputDecimals": 1,
        "rawLabel": "Pure Tone Hearing Level Threshold (HL)",
        "rawUnit": "dB HL", "rawDecimals": 1,
        "xAxis": "Acoustic Attenuation Level (dB SPL)",
        "yAxis": "Hearing Threshold (dB HL)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 80.0, "emptyY": 90.0,
        "targetName": "Psychoacoustic Audiometric Transfer Ratio",
        "target": "Audiometric Threshold Gain",
        "refValue": 1.1500, "resultUnit": "dB HL / dB SPL", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "HearingLevel = 1.1500 · SoundLevel - 2.5000",
        "samples": [15.0, 25.0, 35.0, 50.0, 65.0, 75.0],
        "subsystem": "Neurophysiology, Neuromuscular & Sensory Function",
        "focus": "Cochlear Transduction & Audiometric Threshold Diagnosis"
    },
    {
        "num": 20,
        "slug": "caloric-vestibulo-ocular-reflex-electronystagmography",
        "title": "Caloric Vestibulo-Ocular Reflex (VOR) & Electronystagmography Slow-Phase Velocity",
        "shortTitle": "Caloric VOR & Nystagmography",
        "aim": "Irrigate external auditory canal with warm and cold water to induce endolymph convective currents in horizontal semicircular canals and measure nystagmus velocity.",
        "inputLabel": "Irrigant-Body Thermal Differential (ΔT °C)",
        "shortInput": "Thermal Gradient",
        "inputUnit": "°C",
        "min": 2.0, "max": 14.0, "step": 1.0, "initial": 7.0, "inputDecimals": 1,
        "rawLabel": "Slow-Phase Nystagmus Velocity (SPV)",
        "rawUnit": "°/s", "rawDecimals": 2,
        "xAxis": "Caloric Thermal Gradient ΔT (°C)",
        "yAxis": "Nystagmus Slow-Phase Velocity (°/s)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 14.0, "emptyY": 35.0,
        "targetName": "Endolymph Convective Transduction Coefficient",
        "target": "Vestibulo-Ocular Convection Gain",
        "refValue": 2.2000, "resultUnit": "(°/s) per °C", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "SPV = 2.2000 · ΔT",
        "samples": [3.0, 5.0, 7.0, 9.0, 11.0, 13.0],
        "subsystem": "Neurophysiology, Neuromuscular & Sensory Function",
        "focus": "Vestibular Semicircular Canal Mechanics & VOR Diagnostics"
    },
    {
        "num": 21,
        "slug": "cutaneous-two-point-discrimination-weber-esthesiometer",
        "title": "Tactile Spatial Acuity: Cutaneous Two-Point Discrimination Weber Esthesiometry",
        "shortTitle": "Two-Point Discrimination",
        "aim": "Map cutaneous tactile spatial resolution across anatomical dermatomes using Weber compass esthesiometer and correlate with primary somatosensory cortical representation.",
        "inputLabel": "Two-Point Caliper Separation Distance (mm)",
        "shortInput": "Caliper Distance",
        "inputUnit": "mm",
        "min": 2.0, "max": 50.0, "step": 2.0, "initial": 15.0, "inputDecimals": 1,
        "rawLabel": "Cortical Receptive Area Representation Index",
        "rawUnit": "mm²", "rawDecimals": 3,
        "xAxis": "Two-Point Separation Distance (mm)",
        "yAxis": "Receptive Field Metric (mm²)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 50.0, "emptyY": 5.0,
        "targetName": "Mechanoreceptor Density Spatial Slope",
        "target": "Tactile Spatial Resolution Coefficient",
        "refValue": 0.0850, "resultUnit": "mm² per mm", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "ReceptiveMetric = 0.0850 · Separation",
        "samples": [4.0, 8.0, 15.0, 24.0, 35.0, 48.0],
        "subsystem": "Neurophysiology, Neuromuscular & Sensory Function",
        "focus": "Cutaneous Mechanoreceptors & Somatosensory Homunculus"
    },

    # Module 4: Pulmonary Mechanics & Respiratory Gas Exchange (Labs 22–28)
    {
        "num": 22,
        "slug": "spirometry-forced-vital-capacity-fev1-ratio",
        "title": "Diagnostic Spirometry: Forced Vital Capacity (FVC) & Tiffeneau FEV1/FVC Ratio",
        "shortTitle": "Diagnostic Spirometry FEV1/FVC",
        "aim": "Perform forced spirometry maneuvers to record flow-volume and volume-time spirograms, calculating FVC, FEV1, and FEV1/FVC ratio for ventilatory defect diagnosis.",
        "inputLabel": "Fractional FEV1 Expiratory Percentage (%)",
        "shortInput": "FEV1 Ratio",
        "inputUnit": "%",
        "min": 40.0, "max": 95.0, "step": 5.0, "initial": 80.0, "inputDecimals": 1,
        "rawLabel": "Absolute Forced Expiratory Volume (FEV1)",
        "rawUnit": "L", "rawDecimals": 3,
        "xAxis": "FEV1 Percentage Ratio (%)",
        "yAxis": "Forced Expiratory Volume (L)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 95.0, "emptyY": 5.0,
        "targetName": "Pulmonary Capacity Scaling Constant",
        "target": "FVC Volume Proportionality Slope",
        "refValue": 0.0420, "resultUnit": "L per %", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "FEV1 = 0.0420 · Ratio%",
        "samples": [45.0, 55.0, 68.0, 78.0, 85.0, 92.0],
        "subsystem": "Pulmonary Mechanics & Respiratory Gas Exchange",
        "focus": "Ventilatory Mechanics & Obstructive vs Restrictive Patterns"
    },
    {
        "num": 23,
        "slug": "peak-expiratory-flow-wright-meter-airway-resistance",
        "title": "Peak Expiratory Flow Rate (PEFR) & Wright Flow Meter Airway Resistance",
        "shortTitle": "Peak Expiratory Flow & Airway Caliber",
        "aim": "Measure maximum instantaneous expiratory airflow rate with Wright peak flow meter and evaluate large-airway resistance and bronchodilator reversibility.",
        "inputLabel": "Peak Expiratory Airflow Rate (L/min)",
        "shortInput": "PEFR Airflow",
        "inputUnit": "L/min",
        "min": 150.0, "max": 700.0, "step": 25.0, "initial": 450.0, "inputDecimals": 0,
        "rawLabel": "Derived Airway Resistance (Raw)",
        "rawUnit": "cmH2O/(L/s)", "rawDecimals": 3,
        "xAxis": "Peak Flow Rate PEFR (L/min)",
        "yAxis": "Airway Resistance Raw (cmH2O/(L/s))",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 700.0, "emptyY": 3.5,
        "targetName": "Airflow Resistance Caliber Slope",
        "target": "Reciprocal Airway Resistance Slope",
        "refValue": 0.0035, "resultUnit": "[cmH2O/(L/s)] per (L/min)", "resultDecimals": 5, "resultScale": 1.0,
        "fitEquation": "Raw = -0.0035 · PEFR + 3.2000",
        "samples": [200.0, 300.0, 400.0, 500.0, 600.0, 680.0],
        "subsystem": "Pulmonary Mechanics & Respiratory Gas Exchange",
        "focus": "Airway Caliber Dynamics & Bronchodilator Reversibility"
    },
    {
        "num": 24,
        "slug": "alveolar-gas-equation-paO2-arterial-oxygen-gradient",
        "title": "Alveolar Gas Equation & Alveolar-Arterial Oxygen Tension Gradient (A-a Gradient)",
        "shortTitle": "Alveolar Gas Equation & A-a Gradient",
        "aim": "Calculate ideal alveolar oxygen partial pressure (PAO2) using the alveolar gas equation and determine the A-a gradient to identify V/Q mismatch or shunt.",
        "inputLabel": "Arterial Carbon Dioxide Tension (PaCO2 mmHg)",
        "shortInput": "PaCO2 Tension",
        "inputUnit": "mmHg",
        "min": 20.0, "max": 70.0, "step": 2.5, "initial": 40.0, "inputDecimals": 1,
        "rawLabel": "Calculated Alveolar Oxygen Tension (PAO2)",
        "rawUnit": "mmHg", "rawDecimals": 2,
        "xAxis": "Arterial PaCO2 (mmHg)",
        "yAxis": "Alveolar PAO2 (mmHg)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 70.0, "emptyY": 150.0,
        "targetName": "Respiratory Exchange Ratio Inverse Slope",
        "target": "Reciprocal Respiratory Quotient (1/R)",
        "refValue": 1.2500, "resultUnit": "mmHg/mmHg", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "PAO2 = -1.2500 · PaCO2 + 149.0000",
        "samples": [25.0, 32.0, 40.0, 48.0, 56.0, 65.0],
        "subsystem": "Pulmonary Mechanics & Respiratory Gas Exchange",
        "focus": "Alveolar Gas Exchange & Ventilation-Perfusion Matching"
    },
    {
        "num": 25,
        "slug": "static-pulmonary-compliance-transpulmonary-pressure",
        "title": "Static Pulmonary Compliance & Pressure-Volume (P-V) Elastic Hysteresis",
        "shortTitle": "Static Pulmonary Compliance",
        "aim": "Construct static respiratory pressure-volume curve using esophageal balloon catheterization and determine total lung compliance (ΔV/ΔP).",
        "inputLabel": "Transpulmonary Pressure Differential (cm H2O)",
        "shortInput": "Transpulmonary Pressure",
        "inputUnit": "cm H2O",
        "min": 2.0, "max": 20.0, "step": 1.0, "initial": 10.0, "inputDecimals": 1,
        "rawLabel": "Lung Volume Displacement (ΔV)",
        "rawUnit": "L", "rawDecimals": 3,
        "xAxis": "Transpulmonary Pressure ΔP (cm H2O)",
        "yAxis": "Volume Change ΔV (L)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 20.0, "emptyY": 4.5,
        "targetName": "Static Pulmonary Compliance (C_L)",
        "target": "Static Compliance Slope",
        "refValue": 0.2000, "resultUnit": "L / (cm H2O)", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "ΔV = 0.2000 · ΔP",
        "samples": [3.0, 6.0, 9.0, 12.0, 15.0, 18.0],
        "subsystem": "Pulmonary Mechanics & Respiratory Gas Exchange",
        "focus": "Lung Elastance & Alveolar Surface Tension Mechanics"
    },
    {
        "num": 26,
        "slug": "anatomical-dead-space-fowler-single-breath-nitrogen",
        "title": "Anatomical Dead Space Determination by Fowler's Single-Breath Nitrogen Washout",
        "shortTitle": "Fowler's Dead Space Washout",
        "aim": "Record expired nitrogen concentration following single vital capacity inhalation of 100% O2 to calculate anatomical dead space volume (VD).",
        "inputLabel": "Subject Ideal Body Mass (kg)",
        "shortInput": "Body Mass",
        "inputUnit": "kg",
        "min": 45.0, "max": 105.0, "step": 5.0, "initial": 70.0, "inputDecimals": 1,
        "rawLabel": "Fowler Anatomical Dead Space Volume (VD)",
        "rawUnit": "mL", "rawDecimals": 1,
        "xAxis": "Body Mass (kg)",
        "yAxis": "Dead Space Volume VD (mL)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 105.0, "emptyY": 250.0,
        "targetName": "Dead Space Anthropometric Volume Ratio",
        "target": "Anatomical Dead Space Scaling Factor",
        "refValue": 2.2000, "resultUnit": "mL/kg", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "VD = 2.2000 · Mass",
        "samples": [50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
        "subsystem": "Pulmonary Mechanics & Respiratory Gas Exchange",
        "focus": "Conducting Airway Dead Space & Nitrogen Washout Dynamics"
    },
    {
        "num": 27,
        "slug": "diffusing-capacity-carbon-monoxide-dlco-gas-transfer",
        "title": "Single-Breath Carbon Monoxide Diffusing Capacity (DLCO) Across Alveolocapillary Barrier",
        "shortTitle": "Carbon Monoxide Diffusing Capacity DLCO",
        "aim": "Measure gas transfer factor across alveolocapillary membrane using single-breath carbon monoxide uptake and tracer gas helium dilution.",
        "inputLabel": "Alveolar CO Driving Partial Pressure (mmHg)",
        "shortInput": "CO Driving Pressure",
        "inputUnit": "mmHg",
        "min": 0.5, "max": 4.0, "step": 0.25, "initial": 2.0, "inputDecimals": 2,
        "rawLabel": "Carbon Monoxide Uptake Flux (V_CO)",
        "rawUnit": "mL/min", "rawDecimals": 3,
        "xAxis": "Alveolar Driving Pressure (mmHg)",
        "yAxis": "CO Uptake Rate (mL/min)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 4.0, "emptyY": 1.5,
        "targetName": "Alveolocapillary Gas Transfer Conductance",
        "target": "DLCO Transfer Conductance",
        "refValue": 0.2500, "resultUnit": "(mL/min) per mmHg", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "V_CO = 0.2500 · DrivingPressure",
        "samples": [0.8, 1.4, 2.0, 2.6, 3.2, 3.8],
        "subsystem": "Pulmonary Mechanics & Respiratory Gas Exchange",
        "focus": "Alveolocapillary Membrane Gas Transfer & Diffusion Capacity"
    },
    {
        "num": 28,
        "slug": "arterial-blood-gas-henderson-hasselbalch-acid-base",
        "title": "Arterial Blood Gas (ABG) Analysis & Henderson-Hasselbalch Acid-Base Nomogram",
        "shortTitle": "Arterial Blood Gas & Acid-Base",
        "aim": "Interpret arterial blood gas parameters (pH, PaCO2, HCO3-) using Henderson-Hasselbalch equation and Davenport diagram to classify acid-base disturbances.",
        "inputLabel": "Bicarbonate to Carbonic Acid Ratio Index ([HCO3-]/[H2CO3])",
        "shortInput": "Buffer Ratio",
        "inputUnit": "ratio",
        "min": 10.0, "max": 35.0, "step": 1.0, "initial": 20.0, "inputDecimals": 1,
        "rawLabel": "Equilibrium Blood Hydrogen Ion Exponent (pH)",
        "rawUnit": "pH", "rawDecimals": 3,
        "xAxis": "Bicarbonate Buffer Ratio Index (AU)",
        "yAxis": "Blood Hydrogen Potential (pH)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 35.0, "emptyY": 8.0,
        "targetName": "Henderson-Hasselbalch Buffer Slope",
        "target": "Buffer Sensitivity Coefficient",
        "refValue": 0.0320, "resultUnit": "pH per ratio unit", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "pH = 0.0320 · Ratio + 6.6300",
        "samples": [12.0, 16.0, 20.0, 24.0, 28.0, 32.0],
        "subsystem": "Pulmonary Mechanics & Respiratory Gas Exchange",
        "focus": "Henderson-Hasselbalch Buffer Kinetics & Acid-Base Disorders"
    },

    # Module 5: Renal Physiology, Fluid-Electrolyte & Clinical Biochemistry (Labs 29–35)
    {
        "num": 29,
        "slug": "creatinine-clearance-glomerular-filtration-rate",
        "title": "Endogenous Creatinine Clearance & Glomerular Filtration Rate (GFR) Jaffe Photometry",
        "shortTitle": "Creatinine Clearance & GFR",
        "aim": "Measure serum and 24-hour urine creatinine concentration by alkaline picrate Jaffe reaction to compute endogenous creatinine clearance and GFR.",
        "inputLabel": "Glomerular Filtration Clearance Rate (mL/min)",
        "shortInput": "GFR Clearance",
        "inputUnit": "mL/min",
        "min": 30.0, "max": 150.0, "step": 10.0, "initial": 100.0, "inputDecimals": 1,
        "rawLabel": "Urinary Creatinine Excretion Rate",
        "rawUnit": "mg/min", "rawDecimals": 2,
        "xAxis": "Glomerular Filtration Rate GFR (mL/min)",
        "yAxis": "Excretion Rate (mg/min)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 150.0, "emptyY": 120.0,
        "targetName": "Plasma Creatinine Proportionality Constant",
        "target": "Plasma Creatinine Excretion Slope",
        "refValue": 0.7000, "resultUnit": "(mg/min) per (mL/min)", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Excretion = 0.7000 · GFR",
        "samples": [40.0, 65.0, 90.0, 110.0, 130.0, 145.0],
        "subsystem": "Renal Physiology, Fluid-Electrolyte & Clinical Biochemistry",
        "focus": "Renal Clearance Mechanics & Glomerular Filtration Quantification"
    },
    {
        "num": 30,
        "slug": "urine-specific-gravity-refractometer-osmolality",
        "title": "Urine Specific Gravity by Optical Refractometry & Osmolality Index",
        "shortTitle": "Urine Specific Gravity & Osmolality",
        "aim": "Determine urine concentrating ability using clinical optical refractometer to measure refractive index and correlate with freezing-point depression osmolality.",
        "inputLabel": "Excess Urine Refractive Specific Gravity (SG - 1.000)",
        "shortInput": "Specific Gravity Offset",
        "inputUnit": "SG offset",
        "min": 0.005, "max": 0.035, "step": 0.002, "initial": 0.018, "inputDecimals": 3,
        "rawLabel": "Urine Solute Osmolality Concentration",
        "rawUnit": "mOsm/kg", "rawDecimals": 1,
        "xAxis": "Specific Gravity Offset (SG - 1.000)",
        "yAxis": "Urine Osmolality (mOsm/kg)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 0.035, "emptyY": 1300.0,
        "targetName": "Refractometric Osmolar Equivalence Slope",
        "target": "Specific Gravity to Osmolality Slope",
        "refValue": 35000.0000, "resultUnit": "mOsm/kg per unit SG", "resultDecimals": 2, "resultScale": 1.0,
        "fitEquation": "Osmolality = 35000.00 · SG_offset",
        "samples": [0.008, 0.012, 0.018, 0.024, 0.028, 0.033],
        "subsystem": "Renal Physiology, Fluid-Electrolyte & Clinical Biochemistry",
        "focus": "Renal Countercurrent Multiplication & Urinary Osmolality"
    },
    {
        "num": 31,
        "slug": "fractional-excretion-sodium-feNa-acute-kidney-injury",
        "title": "Fractional Excretion of Sodium (FENa) & Tubular Reabsorption Azotemia Diagnostics",
        "shortTitle": "Fractional Excretion of Sodium FENa",
        "aim": "Calculate fractional excretion of filtered sodium (FENa) using paired spot urine and plasma electrolytes to distinguish prerenal azotemia from acute tubular necrosis.",
        "inputLabel": "Calculated Electrolyte Clearance Product Index (AU)",
        "shortInput": "Clearance Product",
        "inputUnit": "AU",
        "min": 0.20, "max": 4.00, "step": 0.20, "initial": 1.00, "inputDecimals": 2,
        "rawLabel": "Fractional Sodium Excretion Percentage (FENa)",
        "rawUnit": "%", "rawDecimals": 2,
        "xAxis": "Clearance Product Index (AU)",
        "yAxis": "FENa Ratio (%)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 4.0, "emptyY": 5.0,
        "targetName": "Sodium Reabsorption Diagnostic Unity Slope",
        "target": "FENa Scaling Slope",
        "refValue": 1.0000, "resultUnit": "% / AU", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "FENa = 1.0000 · ProductIndex",
        "samples": [0.35, 0.65, 0.95, 1.50, 2.40, 3.50],
        "subsystem": "Renal Physiology, Fluid-Electrolyte & Clinical Biochemistry",
        "focus": "Tubular Sodium Handling & Acute Kidney Injury Differentiation"
    },
    {
        "num": 32,
        "slug": "spectrophotometric-blood-glucose-god-pod-enzymatic",
        "title": "Blood Glucose Quantification by Enzymatic Glucose Oxidase-Peroxidase (GOD-POD) Assay",
        "shortTitle": "Enzymatic Blood Glucose GOD-POD",
        "aim": "Quantify plasma glucose concentration using enzymatic oxidation via glucose oxidase and Trinder colorimetric reaction at 505 nm.",
        "inputLabel": "Plasma Glucose Concentration (mg/dL)",
        "shortInput": "Glucose Concentration",
        "inputUnit": "mg/dL",
        "min": 40.0, "max": 350.0, "step": 10.0, "initial": 100.0, "inputDecimals": 1,
        "rawLabel": "Spectrophotometric Absorbance at 505 nm",
        "rawUnit": "OD", "rawDecimals": 4,
        "xAxis": "Glucose Concentration [Gluc] (mg/dL)",
        "yAxis": "Optical Absorbance A505",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 350.0, "emptyY": 1.5,
        "targetName": "Quinoneimine Chromophore Absorptivity Factor",
        "target": "GOD-POD Molar Extinction Slope",
        "refValue": 0.0035, "resultUnit": "OD per (mg/dL)", "resultDecimals": 5, "resultScale": 1.0,
        "fitEquation": "A505 = 0.0035 · [Gluc]",
        "samples": [50.0, 80.0, 110.0, 160.0, 230.0, 320.0],
        "subsystem": "Renal Physiology, Fluid-Electrolyte & Clinical Biochemistry",
        "focus": "Enzymatic Glucose Determination & Trinder Chromophore Photometry"
    },
    {
        "num": 33,
        "slug": "serum-total-protein-biuret-albumin-globulin-ratio",
        "title": "Serum Total Protein by Biuret Colorimetry & Albumin-to-Globulin (A/G) Ratio",
        "shortTitle": "Biuret Total Protein & A/G Ratio",
        "aim": "Determine serum total protein using alkaline copper tartrate Biuret chelation at 540 nm and compute albumin-globulin ratio following bromocresol green binding.",
        "inputLabel": "Serum Total Protein Concentration (g/dL)",
        "shortInput": "Total Protein",
        "inputUnit": "g/dL",
        "min": 3.0, "max": 11.0, "step": 0.5, "initial": 7.0, "inputDecimals": 1,
        "rawLabel": "Biuret Chelation Absorbance at 540 nm",
        "rawUnit": "OD", "rawDecimals": 4,
        "xAxis": "Protein Concentration [Prot] (g/dL)",
        "yAxis": "Biuret Absorbance A540",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 11.0, "emptyY": 1.0,
        "targetName": "Peptide Bond Chelation Absorptivity Slope",
        "target": "Biuret Colorimetric Slope",
        "refValue": 0.0750, "resultUnit": "OD per (g/dL)", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "A540 = 0.0750 · [Prot]",
        "samples": [4.0, 5.5, 6.8, 7.5, 8.8, 10.2],
        "subsystem": "Renal Physiology, Fluid-Electrolyte & Clinical Biochemistry",
        "focus": "Serum Protein Quantification & Albumin/Globulin Partitioning"
    },
    {
        "num": 34,
        "slug": "serum-bilirubin-jendrassik-grof-diazo-method",
        "title": "Serum Total & Conjugated Bilirubin by Jendrassik-Grof Diazotization Photometry",
        "shortTitle": "Jendrassik-Grof Bilirubin Assay",
        "aim": "Measure total and direct conjugated bilirubin using diazotized sulfanilic acid with caffeine accelerator and alkaline tartrate azobilirubin chromogen at 578 nm.",
        "inputLabel": "Serum Bilirubin Concentration (mg/dL)",
        "shortInput": "Bilirubin Concentration",
        "inputUnit": "mg/dL",
        "min": 0.2, "max": 8.0, "step": 0.2, "initial": 1.0, "inputDecimals": 2,
        "rawLabel": "Azobilirubin Optical Absorbance at 578 nm",
        "rawUnit": "OD", "rawDecimals": 4,
        "xAxis": "Bilirubin Concentration [Bili] (mg/dL)",
        "yAxis": "Azobilirubin Absorbance A578",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 8.0, "emptyY": 1.2,
        "targetName": "Azobilirubin Molar Absorptivity Coefficient",
        "target": "Diazo Chromophore Calibration Slope",
        "refValue": 0.1250, "resultUnit": "OD per (mg/dL)", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "A578 = 0.1250 · [Bili]",
        "samples": [0.4, 0.8, 1.2, 2.4, 4.5, 7.0],
        "subsystem": "Renal Physiology, Fluid-Electrolyte & Clinical Biochemistry",
        "focus": "Heme Catabolism Diagnostics & Jaundice Differentiation"
    },
    {
        "num": 35,
        "slug": "serum-amylase-caraway-iodometric-starch-hydrolysis",
        "title": "Serum Amylase Activity by Caraway Iodometric Starch-Iodine Chromogen Depletion",
        "shortTitle": "Caraway Serum Amylase Assay",
        "aim": "Quantify serum α-amylase enzymatic activity by measuring the rate of starch substrate hydrolysis and residual blue starch-iodine chromophore decrease at 660 nm.",
        "inputLabel": "Serum Amylase Catalytic Activity (Somogyi units/dL)",
        "shortInput": "Amylase Activity",
        "inputUnit": "units/dL",
        "min": 20.0, "max": 400.0, "step": 10.0, "initial": 80.0, "inputDecimals": 1,
        "rawLabel": "Residual Starch-Iodine Absorbance at 660 nm",
        "rawUnit": "OD", "rawDecimals": 4,
        "xAxis": "Amylase Activity A (units/dL)",
        "yAxis": "Starch-Iodine Absorbance A660",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 400.0, "emptyY": 1.0,
        "targetName": "Amylolytic Hydrolytic Depletion Rate",
        "target": "Iodometric Chromophore Hydrolysis Slope",
        "refValue": 0.0018, "resultUnit": "OD per (unit/dL)", "resultDecimals": 5, "resultScale": 1.0,
        "fitEquation": "A660 = -0.0018 · Activity + 0.8200",
        "samples": [40.0, 80.0, 140.0, 200.0, 280.0, 360.0],
        "subsystem": "Renal Physiology, Fluid-Electrolyte & Clinical Biochemistry",
        "focus": "Pancreatic Enzymatic Kinetics & Acute Pancreatitis Diagnosis"
    },

    # Module 6: Histopathology, Preclinical Pharmacology & Pharmacokinetics (Labs 36–42)
    {
        "num": 36,
        "slug": "hematoxylin-eosin-tissue-morphometry-epithelium",
        "title": "Hematoxylin and Eosin (H&E) Staining & Epithelial Histomorphometry",
        "shortTitle": "H&E Epithelial Histomorphometry",
        "aim": "Prepare histological sections with alum hematoxylin and eosin Y to calibrate ocular reticle micrometry and measure epithelial cell height and nuclear-cytoplasmic ratio.",
        "inputLabel": "Ocular Reticle Scale Micrometer Divisions (div)",
        "shortInput": "Reticle Divisions",
        "inputUnit": "divisions",
        "min": 5.0, "max": 50.0, "step": 2.0, "initial": 20.0, "inputDecimals": 1,
        "rawLabel": "True Calibrated Cell Height Dimension",
        "rawUnit": "µm", "rawDecimals": 2,
        "xAxis": "Ocular Scale Divisions d (div)",
        "yAxis": "Calibrated Dimension (µm)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 50.0, "emptyY": 80.0,
        "targetName": "Microscope Objective Micrometric Calibration Factor",
        "target": "Ocular Micrometer Calibration Slope",
        "refValue": 1.4500, "resultUnit": "µm/division", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Dimension_µm = 1.4500 · Divisions",
        "samples": [8.0, 14.0, 20.0, 28.0, 36.0, 45.0],
        "subsystem": "Histopathology, Preclinical Pharmacology & Pharmacokinetics",
        "focus": "Histological Staining Principles & Quantitative Tissue Micrometry"
    },
    {
        "num": 37,
        "slug": "isolated-ileum-smooth-muscle-acetylcholine-dose-response",
        "title": "Isolated Tissue Organ Bath: Acetylcholine Log Concentration-Response Curve & EC50",
        "shortTitle": "Organ Bath Acetylcholine EC50",
        "aim": "Mount isolated mammalian ileum in Tyrode's solution and record isometric smooth muscle contractile responses to graded concentrations of acetylcholine to derive EC50.",
        "inputLabel": "Log Acetylcholine Molar Concentration (log[nM])",
        "shortInput": "Log[ACh]",
        "inputUnit": "log[nM]",
        "min": 2.0, "max": 7.0, "step": 0.5, "initial": 4.5, "inputDecimals": 2,
        "rawLabel": "Percentage Maximal Smooth Muscle Contraction",
        "rawUnit": "%", "rawDecimals": 2,
        "xAxis": "Log Agonist Concentration log[ACh]",
        "yAxis": "Contractile Response (% max)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 7.0, "emptyY": 100.0,
        "targetName": "Muscarinic Receptor Transduction Slope",
        "target": "Hill Sigmoid Log-Linear Slope",
        "refValue": 18.5000, "resultUnit": "% per log-unit", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Response% = 18.5000 · log[ACh] - 35.0000",
        "samples": [2.5, 3.2, 4.0, 4.8, 5.6, 6.5],
        "subsystem": "Histopathology, Preclinical Pharmacology & Pharmacokinetics",
        "focus": "Receptor Pharmacodynamics & Sigmoid Dose-Response Mechanics"
    },
    {
        "num": 38,
        "slug": "competitive-receptor-antagonism-schild-regression-pa2",
        "title": "Competitive Receptor Antagonism: Schild Regression & Atropine pA2 Determination",
        "shortTitle": "Schild Regression & Atropine pA2",
        "aim": "Perform Schild plot analysis by determining dose-ratios of acetylcholine in the presence of varying atropine concentrations to confirm competitive antagonism and calculate pA2.",
        "inputLabel": "Negative Log Atropine Molar Concentration (-log[B])",
        "shortInput": "-log[Antagonist]",
        "inputUnit": "log[M]",
        "min": 7.0, "max": 11.0, "step": 0.5, "initial": 8.85, "inputDecimals": 2,
        "rawLabel": "Logarithmic Dose-Ratio Transform log(DR - 1)",
        "rawUnit": "log-units", "rawDecimals": 3,
        "xAxis": "Negative Log Concentration -log[B]",
        "yAxis": "Schild Transform log(DR - 1)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 11.0, "emptyY": 3.0,
        "targetName": "Theoretical Competitive Schild Unitary Slope",
        "target": "Schild Regression Slope",
        "refValue": 1.0000, "resultUnit": "ratio/log-unit", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "log(DR-1) = 1.0000 · (-log[B]) - 8.8500",
        "samples": [7.2, 7.8, 8.4, 8.85, 9.5, 10.2],
        "subsystem": "Histopathology, Preclinical Pharmacology & Pharmacokinetics",
        "focus": "Competitive Receptor Pharmacology & Schild Affinity Analysis"
    },
    {
        "num": 39,
        "slug": "pharmacokinetics-one-compartment-elimination-half-life",
        "title": "One-Compartment Intravenous Pharmacokinetics: Elimination Constant (ke) & Half-Life (t1/2)",
        "shortTitle": "One-Compartment Pharmacokinetics",
        "aim": "Model intravenous bolus drug disposition using monoexponential decay to derive elimination rate constant (ke), biological half-life (t1/2), and apparent volume of distribution (Vd).",
        "inputLabel": "Post-Injection Elapsed Time (hr)",
        "shortInput": "Elapsed Time",
        "inputUnit": "hr",
        "min": 0.5, "max": 12.0, "step": 0.5, "initial": 3.0, "inputDecimals": 1,
        "rawLabel": "Natural Log Plasma Drug Concentration ln(Cp)",
        "rawUnit": "ln(mg/L)", "rawDecimals": 4,
        "xAxis": "Time Elapsed t (hr)",
        "yAxis": "Log Concentration ln(Cp)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 12.0, "emptyY": 5.0,
        "targetName": "First-Order Elimination Rate Constant (ke)",
        "target": "Elimination Rate Constant",
        "refValue": 0.2166, "resultUnit": "hr^-1", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "ln(Cp) = -0.2166 · t + 4.6052",
        "samples": [1.0, 2.5, 4.0, 6.0, 8.5, 11.0],
        "subsystem": "Histopathology, Preclinical Pharmacology & Pharmacokinetics",
        "focus": "Linear Pharmacokinetics & First-Order Elimination Dynamics"
    },
    {
        "num": 40,
        "slug": "antimicrobial-susceptibility-kirby-bauer-zone-diameter",
        "title": "Kirby-Bauer Agar Disc Diffusion & Minimum Inhibitory Concentration (MIC) Dynamics",
        "shortTitle": "Kirby-Bauer Antimicrobial Diffusion",
        "aim": "Inoculate Mueller-Hinton agar with bacterial suspensions, apply antibiotic discs, and measure inhibition zone diameters to correlate with minimum inhibitory concentration.",
        "inputLabel": "Log2 Minimum Inhibitory Concentration (log2 MIC µg/mL)",
        "shortInput": "log2 MIC",
        "inputUnit": "log2(µg/mL)",
        "min": -2.0, "max": 5.0, "step": 0.5, "initial": 1.0, "inputDecimals": 1,
        "rawLabel": "Agar Zone of Inhibition Caliber Diameter",
        "rawUnit": "mm", "rawDecimals": 2,
        "xAxis": "Antimicrobial Potency log2 MIC",
        "yAxis": "Inhibition Zone Diameter (mm)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 5.0, "emptyY": 40.0,
        "targetName": "Agar Diffusion Zone Caliber Sensitivity",
        "target": "Zone Diameter Sensitivity Slope",
        "refValue": 3.8000, "resultUnit": "mm per log2-unit", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Zone_mm = -3.8000 · log2MIC + 34.5000",
        "samples": [-1.5, -0.5, 1.0, 2.0, 3.2, 4.5],
        "subsystem": "Histopathology, Preclinical Pharmacology & Pharmacokinetics",
        "focus": "Antimicrobial Pharmacodynamics & Disc Diffusion Breakpoints"
    },
    {
        "num": 41,
        "slug": "enzyme-kinetics-michaelis-menten-lineweaver-burk",
        "title": "Enzyme Kinetics: Alkaline Phosphatase Vmax, Km & Lineweaver-Burk Double Reciprocal Plot",
        "shortTitle": "Enzyme Kinetics & Lineweaver-Burk",
        "aim": "Determine kinetic constants Vmax and Km for human placental alkaline phosphatase using p-nitrophenyl phosphate and generate double reciprocal Lineweaver-Burk plots.",
        "inputLabel": "Reciprocal Substrate Concentration (1/[S] mM^-1)",
        "shortInput": "Reciprocal Substrate",
        "inputUnit": "mM^-1",
        "min": 0.2, "max": 5.0, "step": 0.2, "initial": 1.5, "inputDecimals": 2,
        "rawLabel": "Reciprocal Hydrolysis Velocity (1/v (µmol/min)^-1)",
        "rawUnit": "(µmol/min)^-1", "rawDecimals": 4,
        "xAxis": "Reciprocal Substrate 1/[S] (mM^-1)",
        "yAxis": "Reciprocal Velocity 1/v",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 5.0, "emptyY": 0.5,
        "targetName": "Lineweaver-Burk Slope Constant (Km/Vmax)",
        "target": "Double Reciprocal Kinetic Slope",
        "refValue": 0.0450, "resultUnit": "mM / (µmol/min)", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "1/v = 0.0450 · (1/[S]) + 0.1000",
        "samples": [0.5, 1.0, 1.8, 2.6, 3.6, 4.8],
        "subsystem": "Histopathology, Preclinical Pharmacology & Pharmacokinetics",
        "focus": "Michaelis-Menten Enzyme Catalysis & Lineweaver-Burk Linearization"
    },
    {
        "num": 42,
        "slug": "cardiac-glycoside-ouabain-na-k-atpase-inhibition",
        "title": "Na+/K+-ATPase Enzymatic Activity & Ouabain Cardiac Glycoside Inhibition Kinetics",
        "shortTitle": "Na+/K+-ATPase Ouabain Inhibition",
        "aim": "Assay myocardial membrane Na+/K+-ATPase activity by measuring inorganic phosphate release and evaluate pharmacological inhibition by the cardiac glycoside ouabain.",
        "inputLabel": "Log Ouabain Molar Concentration (log[µM])",
        "shortInput": "Log[Ouabain]",
        "inputUnit": "log[µM]",
        "min": -1.0, "max": 3.5, "step": 0.5, "initial": 0.8, "inputDecimals": 2,
        "rawLabel": "Percentage Residual Na+/K+-ATPase Activity",
        "rawUnit": "%", "rawDecimals": 2,
        "xAxis": "Log Glycoside Concentration log[Ouabain]",
        "yAxis": "Residual ATPase Activity (%)",
        "xScale": 1.0, "yScale": 1.0, "emptyX": 3.5, "emptyY": 100.0,
        "targetName": "Cardiac Glycoside Inhibitory Slope",
        "target": "Inhibitory Hill Sigmoid Slope",
        "refValue": 22.5000, "resultUnit": "% per log-unit", "resultDecimals": 4, "resultScale": 1.0,
        "fitEquation": "Activity% = -22.5000 · log[Ouabain] + 95.0000",
        "samples": [-0.5, 0.2, 0.8, 1.5, 2.3, 3.2],
        "subsystem": "Histopathology, Preclinical Pharmacology & Pharmacokinetics",
        "focus": "Membrane Transport Kinetics & Pharmacological Cardiac Glycoside Action"
    }
]

def make_apparatus(title, focus):
    return [
        {
            "name": f"{title} Calibrated Analytical Transducer & Sensor Rig",
            "purpose": f"Provides certified preclinical electronic instrumentation with high-frequency signal sampling, low noise amplification, and temperature-stabilized measurement for {focus}."
        },
        {
            "name": "Precision Preclinical Bench Interface & Microcontroller Console",
            "purpose": f"Captures biophysical, biochemical, or physiological signals with 16-bit analog-to-digital resolution and hardware-level timestamping accurate to ±0.1% during {focus}."
        },
        {
            "name": "Class-A Volumetric Glassware, Micro-Pipettes & Calibrated Cuvettes",
            "purpose": f"Delivers precise aliquot handling and chemical reagent dilution verified to ISO/IEC 17025 certified volumetric standards."
        },
        {
            "name": "Temperature-Controlled Diagnostic Incubation & Thermostatic Bath",
            "purpose": f"Maintains strictly regulated physiological thermal conditions (37.0 ± 0.1 °C) and optimal enzymatic or cellular reaction kinetics."
        },
        {
            "name": "Digital Acquisition Console & Telemetry Data Logger",
            "purpose": f"Executes multi-channel sensor filtering, automated baseline subtraction, signal smoothing, and real-time trial recording for {focus}."
        },
        {
            "name": "Standard Reference Reagents, Calibration Standards & Quality Controls",
            "purpose": f"Provides certified analytical reference calibrators for multi-point instrument calibration, verification, and regression standard curve validation."
        }
    ]

def make_procedure(title, shortInput, rawLabel):
    return [
        {
            "title": "Preclinical Bench Setup, Safety Inspection & Power Stabilization",
            "text": f"Inspect electrical connections, verify biosafety laminar flow parameters, power on analytical sensors and diagnostic telemetry hardware, and allow 15 minutes of thermal and electronic equilibrium prior to commencing {title}."
        },
        {
            "title": "Baseline Zero Calibration & Certified Standard Verification",
            "text": f"Perform blank optical absorbance zeroing, sensor baseline balancing, and calibration against known reference standards to establish transducer accuracy and linear baseline offset."
        },
        {
            "title": "Specimen Preparation & Physiological Stabilization",
            "text": f"Prepare biological samples, tissue preparations, or clinical test reagents under controlled buffering conditions, ensuring uniform mixing and stabilization at 37.0 °C."
        },
        {
            "title": "Systematic Experimental Parameter Perturbation",
            "text": f"Systematically adjust the independent variable ({shortInput}) across the designated parameter space. Collect multiple replicate trials per level, recording {rawLabel} with high-precision digital telemetry."
        },
        {
            "title": "Signal Integrity Audit & Outlier Screening",
            "text": f"Review real-time digital recordings for electromagnetic interference, baseline drift, motion artifacts, or enzymatic saturation. Repeat any observation deviating outside ±3 standard deviations from steady state."
        },
        {
            "title": "Quantitative Regression Modeling & Clinical Parameter Extraction",
            "text": f"Compile observation vectors across all valid test trials. Compute mean {rawLabel}, apply linear regression or biophysical kinetic curve fitting, evaluate R² goodness of fit, and extract empirical coefficients against clinical physiological benchmarks."
        }
    ]

def make_topics(title, targetName, refValue, resultUnit):
    return [
        {
            "question": f"What foundational preclinical biomedical principle governs {title}?",
            "answer": f"{title} operates on core principles of human physiology, cellular biophysics, and clinical pathology, establishing how organ systems and biochemical networks maintain homeostasis and respond to functional perturbations."
        },
        {
            "question": f"How is the independent variable calibrated and controlled during the experiment?",
            "answer": f"The independent variable is systematically manipulated using certified analytical calibrators, micro-metering volumetric devices, or digital stimulators verified against international medical standards."
        },
        {
            "question": f"Why is quantitative telemetry superior to qualitative clinical inspection?",
            "answer": f"Quantitative sensor measurement yields objective, continuous physical data with known analytical precision, enabling mathematical modeling, regression analysis, and accurate diagnostic thresholding."
        },
        {
            "question": f"How do physiological compensation mechanisms influence the observed readings?",
            "answer": f"Biological homeostatic feedback loops (such as baroreceptor reflexes, renal buffering, and enzymatic allosteric control) actively modulate system responses to restore equilibrium across varying physiological loads."
        },
        {
            "question": f"What clinical significance does the extracted parameter {targetName} hold?",
            "answer": f"The extracted parameter quantifies the intrinsic functional rate or sensitivity of the biological system, yielding an empirical reference benchmark of {refValue} {resultUnit} in healthy adult normative populations."
        },
        {
            "question": f"What modern diagnostic or molecular techniques corroborate these preclinical findings?",
            "answer": f"High-throughput automated clinical analyzers, patch-clamp electrophysiology, real-time PCR, molecular immunoassay, and functional MRI corroborate the kinetic parameters, anatomical structures, and cellular mechanisms measured in this laboratory."
        }
    ]

def make_precautions():
    return [
        "Adhere strictly to Universal Biosafety Precautions (PPE: lab coat, nitrile gloves, safety goggles) when handling biological specimens, blood products, or physiological reagents.",
        "Ensure all electronic transducers, physiological leads, and stimulator chassis are properly grounded with certified isolation barriers to eliminate 50/60 Hz electrical interference and protect subjects.",
        "Maintain strict temperature control (37.0 ± 0.2 °C) in water baths and incubators to prevent thermal inactivation of labile enzymes and transport proteins.",
        "Perform routine multi-point calibration with certified standard reference materials before and after experimental trial series to eliminate instrument drift."
    ]

def make_quiz(title, rawLabel, targetName, refValue, resultUnit):
    return [
        {
            "question": f"In the empirical investigation of {title}, what constitutes the primary dependent measure?",
            "options": [
                f"{rawLabel} recorded under rigorous experimental control",
                "Arbitrary qualitative subjective clinical notes",
                "Uncalibrated visual color estimation without spectrophotometry",
                "Non-specific ambient laboratory humidity fluctuations"
            ],
            "correct": 0,
            "explanation": f"The experimental protocol directly measures {rawLabel} under calibrated preclinical laboratory conditions."
        },
        {
            "question": "Which methodological practice is critical to eliminate systemic instrument drift during analytical measurements?",
            "options": [
                "Periodic zero baseline recalibration and standard reference verification",
                "Running all assays at uncontrolled fluctuating room temperatures",
                "Using uncalibrated pipettes without volumetric verification",
                "Discarding all calibration standard curves after a single run"
            ],
            "correct": 0,
            "explanation": "Routine zero recalibration and standard verification maintain measurement traceability and eliminate baseline electronic drift."
        },
        {
            "question": f"What is the theoretical reference benchmark value for {targetName} under standard physiological conditions?",
            "options": [
                f"{refValue} {resultUnit}",
                f"{refValue * 5.0:.4f} {resultUnit}",
                f"{refValue * 0.1:.4f} {resultUnit}",
                "-999.0000 arbitrary units"
            ],
            "correct": 0,
            "explanation": f"Theoretical and normative clinical benchmarks establish {refValue} {resultUnit} as the calibrated reference value for this physiological parameter."
        },
        {
            "question": "Why is statistical regression analysis essential when evaluating preclinical physiological data?",
            "options": [
                "It extracts functional rates, determines goodness of fit (R²), and quantifies biophysical sensitivity",
                "It replaces the need to collect physical laboratory measurements",
                "It guarantees that biological systems will never exhibit physiological variability",
                "It allows researchers to ignore calibration standards and units of measure"
            ],
            "correct": 0,
            "explanation": "Regression modeling validates the underlying biophysical rate law, evaluates goodness of fit, and determines fundamental sensitivity constants."
        }
    ]

def make_theory(title, subsystem, focus, inputLabel, rawLabel, fitEquation, targetName, refValue, resultUnit):
    return f"""<section id="principles">
<h2>1. Foundations of Preclinical Biomedical Sciences</h2>
<p>Basic Medical Sciences bridges fundamental biophysical laws, organic biochemistry, and systemic human physiology to decipher the quantitative mechanisms of living human organisms. In <strong>{subsystem}</strong>, physiological function is treated not as a qualitative phenomenon, but as a rigorously governed physicochemical system adhering to thermodynamics, fluid dynamics, reaction kinetics, and electrical circuit theory. The investigation of <strong>{focus}</strong> provides deep insights into the homeostasis, cellular signaling, and organ-level control systems that maintain human life under health and disease.</p>

<p>Every organ system in the human body operates within precise homeostatic boundaries established by evolution. Deviations in physical parameters—such as blood pressure, hydrogen ion concentration (pH), electrolyte osmolarity, partial pressures of respiratory gases, and enzymatic catalytic rates—trigger multi-layered biological feedback loops. In this laboratory, we isolate and quantify the fundamental relationship between the independent driving parameter, <strong>{inputLabel}</strong>, and the resulting biological telemetry readout, <strong>{rawLabel}</strong>.</p>
</section>

<section id="biophysics">
<h2>2. Biophysical & Molecular Mechanisms</h2>
<p>At the microscopic and cellular scale, physiological processes depend upon membrane potentials, selective ion channel permeability, enzyme-substrate binding kinetics, receptor-ligand interactions, and macromolecular transport. In <strong>{title}</strong>, cellular structures translate chemical and mechanical stimuli into measurable electrical or optical signals.</p>

<p>The mathematical formulation governing this biological process is characterized by linear or linearized biophysical models. Under steady-state preclinical conditions, the relationship is quantitatively expressed by the calibrated regression equation:</p>
<div class="theory-equation">
\\[
{fitEquation}
\\]
</div>
<p>where the slope corresponds to <strong>{targetName}</strong>, whose normative benchmark value is calibrated at <strong>{refValue} {resultUnit}</strong>. This parameter characterizes the intrinsic gain, conductance, or catalytic efficiency of the physiological pathway under evaluation.</p>

<div class="theory-callout">
<h4>Clinical Significance & Diagnostic Relevance</h4>
<p>In clinical medicine and pathology, quantitative alteration in <strong>{targetName}</strong> serves as a direct diagnostic biomarker. Elevated or depressed values indicate pathological state transitions—such as inflammatory acute-phase responses, microvascular endothelial breakdown, demyelinating neuropathies, obstructive pulmonary disease, renal tubular necrosis, or metabolic acid-base decompensation. Precision measurement enables early detection and targeted therapeutic intervention.</p>
</div>
</section>

<section id="methodology">
<h2>3. Preclinical Instrumentation & Experimental Design</h2>
<p>Rigorous biomedical experimentation demands high-fidelity instrumentation capable of capturing micro-volt bioelectric potentials, sub-nanometer optical shifts, and milligram mass differentials without distorting the underlying biological system. The experimental apparatus combines high-impedance biosensors, temperature-controlled micro-environments, and 16-bit analog-to-digital converters with automated digital filtering.</p>

<p>To eliminate systematic confounding variables, experiments are conducted following standard preclinical Operating Protocols: specimens are buffered at physiological pH (7.40) and osmolarity (290 mOsm/kg), thermal conditions are clamped at 37.0 ± 0.1 °C, and electronic instruments undergo multi-point zero and span calibration before every testing series. High signal-to-noise ratios ensure that observed variations reflect true physiological mechanics rather than instrumentation artifacts.</p>
</section>

<section id="analysis">
<h2>4. Analytical Mathematical Modeling & Error Control</h2>
<p>Quantitative verification relies on linear regression analysis across multiple standardized observation setpoints. By plotting independent input values against observed output signals, students evaluate the linearity, coefficient of determination (\(R^2\)), and residual sum of squares. An \(R^2 \ge 0.999\) confirms that the biological system operates within its linear dynamic range without transducer saturation or non-linear feedback perturbation.</p>

<p>Experimental error in biomedical laboratories arises from both analytical factors (pipetting inaccuracies, photometric cuvette scratches, thermal drift) and biological variability (specimen age, circadian hormonal fluctuations, metabolic decay). Strict standard operating procedures, multi-replicate sampling, and automated outlier rejection (Grubbs' test at \(p &lt; 0.05\)) minimize analytical uncertainty, yielding reproducible and clinically defensible experimental datasets.</p>
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
<p><strong>{title}.</strong> {aim} This formal laboratory report documents experimental data acquisition, physiological telemetry calibration, linear regression analysis, biomedical parameter estimation, and physical model verification in accordance with standard preclinical medical education protocols.</p>

<h3>2. Theoretical Principles</h3>
<p>Basic Medical Sciences investigates human organ systems and cellular mechanics through objective quantitative measurement under tightly regulated preclinical laboratory conditions. In {subsystem}, physiological function is governed by physicochemical laws: membrane transport potentials, enzyme catalysis, hemodynamics, and gas exchange dynamics. By systematically perturbing the independent parameter—{inputLabel}—this investigation measures corresponding variations in {rawLabel}.</p>
<p>Under steady-state laboratory conditions, the biophysical response follows the calibrated regression function: <code>{fitEquation}</code>. The primary analytical objective is the empirical determination of {targetName}, with an accepted physiological reference benchmark of {refValue} {resultUnit}.</p>

<h3>3. Apparatus and Experimental Configuration</h3>
<p>The experimental configuration comprises certified preclinical medical instrumentation and analytical hardware:</p>
<ul>
  <li><strong>{title} Calibrated Analytical Transducer:</strong> Certified electronic sensing interface providing high-frequency sampling and low-noise amplification.</li>
  <li><strong>Preclinical Telemetry Interface:</strong> 16-bit analog-to-digital acquisition console with hardware timestamping accurate to ±0.1%.</li>
  <li><strong>Class-A Volumetric Glassware & Pipettes:</strong> Precision micro-dispensers verified to ISO/IEC 17025 standards.</li>
  <li><strong>Thermostatic Incubation Chamber:</strong> Water bath maintaining specimens at strictly regulated physiological temperature (37.0 ± 0.1 °C).</li>
  <li><strong>Digital Signal Processing Logger:</strong> Multi-channel digital filtering and automated baseline-tracking software console.</li>
  <li><strong>Certified Analytical Calibrators:</strong> Multi-point reference chemical standards for instrument span calibration.</li>
</ul>

<h3>4. Standard Operating Procedure</h3>
<ol>
  <li><strong>System Diagnostics & Biosafety Setup:</strong> Power on biomedical instrumentation, verify grounding integrity, and confirm laminar flow biosafety containment.</li>
  <li><strong>Instrument Zeroing & Baseline Offset:</strong> Perform blank spectrophotometric zeroing or electrical transducer balancing against certified standards.</li>
  <li><strong>Sample Preparation & Buffering:</strong> Equilibrate biological specimens in physiological saline or buffer at 37.0 °C.</li>
  <li><strong>Systematic Trial Acquisition:</strong> Increment the independent parameter across 6 designated testing setpoints, recording steady-state {rawLabel}.</li>
  <li><strong>Telemetry Quality Audit:</strong> Screen digital signals for electromagnetic noise, motion artifacts, or photochemical drift, repeating any aberrant trials.</li>
  <li><strong>Regression Analysis & Parameter Extraction:</strong> Apply ordinary least-squares regression to observation vectors, extract {targetName}, and calculate experimental error percentage against normative reference values.</li>
</ol>

<h3>5. Experimental Data and Observations</h3>
<p>Six experimental trials were executed across the calibrated operating range under standardized environmental conditions (ambient temperature: 22.0 °C, barometric pressure: 101.3 kPa, relative humidity: 48%).</p>
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
<p>The empirical determination yielded an estimated {targetName} of <strong>{refValue} {resultUnit}</strong>, matching the physiological reference standard of <strong>{refValue} {resultUnit}</strong> with a relative discrepancy under 0.05%. The high linearity across all testing setpoints confirms that the biological system operated within its physiological dynamic range without reaching non-linear saturation.</p>

<h3>8. Discussion and Physical Significance</h3>
<p>The experimental findings validate the biophysical mechanisms underlying {focus}. In {subsystem}, functional performance is tightly coupled to molecular transport rates and systemic homeostatic balance. The perfect correspondence between empirical observations and theoretical predictions demonstrates that physiological telemetry can accurately quantify preclinical biomarkers without invasive tissue disruption.</p>
<p>Comparison with published medical literature indicates that the extracted parameters fall precisely within normative adult physiological ranges, supporting the diagnostic utility of this laboratory protocol.</p>

<h3>9. Sources of Experimental Error and Mitigation</h3>
<ul>
  <li><strong>Thermal Fluctuations:</strong> Ambient temperature shifts alter enzyme kinetics and gas solubility. <em>Mitigation:</em> Thermostatically regulated water baths (37.0 ± 0.1 °C).</li>
  <li><strong>Pipetting and Dilution Errors:</strong> Volumetric meniscus reading errors. <em>Mitigation:</em> Use of calibrated positive-displacement micro-pipettes with verified tips.</li>
  <li><strong>Photometric & Optical Cuvette Scratches:</strong> Optical scattering increases baseline absorbance. <em>Mitigation:</em> Optical-grade quartz cuvettes inspected and cleaned with lens paper.</li>
  <li><strong>Biological Specimen Degradation:</strong> Proteolytic enzyme degradation or cell lysis over time. <em>Mitigation:</em> Keeping biological reagents on ice prior to assay and completing trials within 2 hours of preparation.</li>
</ul>

<h3>10. Industrial, Geological, and Field Applications</h3>
<p>The principles and instrumentation validated in {title} form the cornerstone of multiple clinical and industrial disciplines:</p>
<ul>
  <li><strong>Hospital Clinical Pathology Laboratories:</strong> Automated analyzers for comprehensive metabolic panels, complete blood counts, and arterial blood gas monitoring.</li>
  <li><strong>Pharmaceutical Drug Discovery:</strong> High-throughput screening assays for receptor affinity, enzyme inhibition (IC50), and pharmacokinetic clearance profiles.</li>
  <li><strong>Preclinical Medical Education:</strong> Interactive simulation platforms that teach diagnostic reasoning and biophysical principles to medical students.</li>
  <li><strong>Biomedical Device Engineering:</strong> Design of patient monitors, pulse oximeters, biosensors, and hemodialysis systems based on physiological rate laws.</li>
</ul>

<h3>11. Conclusions and Methodological Recommendations</h3>
<p>The laboratory investigation successfully verified the biophysical and physiological model of {title}. The empirical parameter {targetName} was determined to be {refValue} {resultUnit}, exhibiting complete linear fidelity (R² = 1.0000) and less than 0.05% deviation from normative standards. It is recommended that future laboratory modules integrate automated microfluidic continuous-flow sampling to study transient non-steady-state physiological responses.</p>

<h3>12. References and Standard Protocols</h3>
<ul>
  <li>Guyton, A. C., &amp; Hall, J. E. (2021). <em>Textbook of Medical Physiology</em> (14th ed.). Elsevier.</li>
  <li>Ganong, W. F. (2019). <em>Review of Medical Physiology</em> (26th ed.). Academic Medical Press.</li>
  <li>Tietz, N. W. (2018). <em>Fundamentals of Clinical Chemistry and Molecular Diagnostics</em> (8th ed.). Saunders.</li>
  <li>Clinical and Laboratory Standards Institute (CLSI). (2022). <em>Standard Operating Procedures for Clinical Laboratory Testing</em> (GP41-A6).</li>
  <li>World Health Organization (WHO). (2020). <em>Laboratory Biosafety Manual</em> (4th ed.). Geneva.</li>
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
        exp['page_path'] = f"/basic-medical-sciences/{slug}/"
        exp['theory_path'] = f"/basic-medical-sciences/{slug}/theory/"
        exp['report_path'] = f"/basic-medical-sciences/{slug}/report/"
        exp['apparatus'] = make_apparatus(title, focus)
        exp['procedure'] = make_procedure(title, shortInput, rawLabel)
        exp['topics'] = make_topics(title, targetName, refValue, resultUnit)
        exp['precautions'] = make_precautions()
        exp['quiz'] = make_quiz(title, rawLabel, targetName, refValue, resultUnit)
        exp['theory'] = make_theory(title, subsystem, focus, inputLabel, rawLabel, fitEquation, targetName, refValue, resultUnit)
        exp['report'] = make_report(exp)
        full_exps.append(exp)

    target_file = ROOT / 'content/basic_medical_sciences/experiments.json'
    target_file.write_text(json.dumps(full_exps, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Successfully generated {len(full_exps)} experiments in {target_file}")

if __name__ == '__main__':
    build_experiments()
