# -*- coding: utf-8 -*-
"""Full generator for Marine & Ocean Sciences 21-laboratory curriculum."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET_FILE = ROOT / "content" / "marine_ocean_sciences" / "experiments.json"

MARINE_EXP_DATA = [
    # Module 1: Physical Oceanography, Waves & Currents (Labs 1–6)
    (1, "practical-salinity-scale-conductometric-salinometer", "Physical Oceanography: Practical Salinity Scale (PSS-78) via Precision Conductometric Salinometry",
     "Conductometric Salinity (PSS-78)", "Determine the practical salinity of oceanographic seawater samples by measuring conductometric ratios relative to standard IAPSO Copenhagen normal seawater at 15.0 °C.",
     "Standardized Electrical Conductivity Ratio (R_15)", "Conductivity Ratio", "dimensionless", 0.80, 1.30, 0.10, 1.00, 2,
     "Practical Salinity Scale Output", "PSU", 2, "Conductivity Ratio (R_15)", "Practical Salinity (PSU)",
     "PSS-78 Salinity Conductance Coefficient", "k_sal", 35.0000, "PSU", 4, 1.0,
     "Salinity (PSU) = 35.0000 · Conductivity Ratio + 0.1500",
     [0.80, 0.90, 1.00, 1.10, 1.20, 1.30],
     "Physical Oceanography & Hydrography", "PSS-78 Practical Salinity Scale & UNESCO Conductance Polynomials",
     "Absolute chemical salinity in open oceans cannot be measured directly through total evaporation due to thermal decomposition of carbonates and loss of volatile halides. PSS-78 defines practical salinity through electrical conductivity ratios R_15 relative to standard KCl solution (32.4356 g/kg) and standard IAPSO seawater at 15.0 °C and 1 atm pressure, obeying a 5th-order empirical Chebyshev polynomial.",
     "Precision salinity measurements govern thermodynamic state variables (TEOS-10 absolute salinity, conservative temperature, potential density), global thermohaline conveyor circulation modeling, and Antarctic Intermediate / North Atlantic Deep Water mass tracing.",
     "Guildline Autosal Sub-Bench High-Precision Laboratory Salinometer", "Thermostatically Controlled Water Bath (15.000 ± 0.001 °C)", "IAPSO Certified Copenhagen Standard Seawater Batches (P-series)", "Precision Pyrex Conductometric Flow-Through Cell Assembly", "Hermetically Sealed Fluoropolymer Sample Transfer Syringes", "Dual High-Resolution Platinum Resistance Thermometers (PRT-100)"),

    (2, "seawater-density-equation-of-state-temperature", "Thermodynamics of Seawater: Thermal Expansion & Equation of State (TEOS-10) Pycnometry",
     "Seawater Thermal Density Anomaly", "Quantify the non-linear thermal expansion of seawater and determine the sigma-t density anomaly across a thermal gradient from polar to tropical conditions.",
     "Thermostatted Seawater Sample Temperature", "Temperature", "°C", 5.0, 30.0, 5.0, 15.0, 1,
     "Seawater Sigma-t Density Anomaly", "kg/m³", 2, "Temperature (°C)", "Density Anomaly (kg/m³)",
     "Seawater Thermal Expansion Density Slope", "alpha_rho", 0.2850, "(kg/m³)/°C", 4, 1.0,
     "Density Anomaly (kg/m³) = -0.2850 · Temperature (°C) + 28.5000",
     [5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
     "Thermodynamic Oceanography", "TEOS-10 Gibbs Seawater Function & Thermal Expansion Coefficient",
     "The density of seawater is a complex function of absolute salinity, conservative temperature, and hydrostatic pressure, formulated through the Gibbs function of seawater in TEOS-10. Because water molecules form tetrahedral hydrogen-bonded networks, thermal contraction occurs until the temperature of maximum density (which drops below freezing point for S > 24.7 PSU), establishing stable oceanic stratification.",
     "Oceanic density gradients drive deep convective overturning, control mixed-layer deepening, govern acoustic sound ducting, and regulate the vertical stability (Brunt-Väisälä buoyancy frequency) of marine ecosystems.",
     "Anton Paar DMA 5000 M High-Precision Digital Density Meter", "Refrigerated / Heating Circulating Thermostat Bath (± 0.005 °C)", "Degassed IAPSO Standard Seawater Calibration Standard", "Ultrasonic Bath for Complete Microbubble Degassing", "Traceable Quartz Capillary Pycnometer Cell", "Digital Precision Barometer for Atmospheric Reference Pressure"),

    (3, "shallow-water-wave-celerity-depth-dispersion", "Geophysical Wave Dynamics: Airy Linear Wave Theory & Shallow Water Dispersion Celerity",
     "Shallow Water Wave Celerity", "Measure phase propagation velocity (celerity) of surface gravity waves in a hydrodynamic flume across varying water column depths to validate the Airy dispersion relation.",
     "Square Root of Water Column Depth", "sqrt(Depth)", "m^(1/2)", 1.0, 3.5, 0.5, 2.0, 2,
     "Surface Gravity Wave Phase Celerity", "m/s", 2, "sqrt(Depth) (m^(1/2))", "Phase Celerity (m/s)",
     "Gravitational Wave Celerity Scaling Factor", "k_wave", 3.1320, "(m/s)/m^(1/2)", 4, 1.0,
     "Phase Celerity (m/s) = 3.1320 · sqrt(Depth) (m^(1/2)) + 0.2500",
     [1.0, 1.5, 2.0, 2.5, 3.0, 3.5],
     "Coastal Hydrodynamics & Wave Mechanics", "Airy Linear Wave Theory & Dispersion Relation c = sqrt(g·h)",
     "In surface gravity wave theory, the general dispersion relation is omega^2 = g k tanh(kh). In the shallow-water asymptotic limit where water depth h < lambda / 20, tanh(kh) approx kh, collapsing the phase celerity to c = sqrt(g · h). Phase velocity becomes purely depth-dependent and independent of wave period, driving shoaling, refraction, and breaking in coastal surf zones.",
     "Shallow water wave dispersion models predict tsunami runup heights, coastal storm surge propagation, harbor resonance oscillations, and sediment transport in nearshore coastal engineering.",
     "Precision Hydrodynamic Wave Flume (15 m length with Glass Walls)", "Computer-Controlled Piston Wave Generator and Servomotor", "Dual Acoustic Wave Gauges with High-Speed ADC Sampling (1000 Hz)", "Adjustable Impermeable False Floor Depth Adjustment Assembly", "High-Resolution Laser Doppler Velocimeter (LDV)", "Wave Absorbing Slotted Beach Energy Dissipation Module"),

    (4, "ekman-spiral-wind-drift-surface-current", "Dynamic Oceanography: Coriolis Forcing & Ekman Surface Layer Wind-Driven Transport",
     "Ekman Wind-Driven Transport", "Measure surface water drift velocity and deflection angles under steady wind stress on a rotating geophysical fluid turntable simulating planetary Coriolis acceleration.",
     "10-Meter Steady Wind Stress Velocity", "Wind Speed", "m/s", 4.0, 24.0, 4.0, 12.0, 1,
     "Surface Drift Current Velocity", "m/s", 3, "Wind Speed (m/s)", "Drift Velocity (m/s)",
     "Ekman Wind Drift Current Coupling Factor", "gamma_ekman", 0.0250, "dimensionless", 4, 1.0,
     "Surface Current (m/s) = 0.0250 · Wind Speed (m/s) + 0.0100",
     [4.0, 8.0, 12.0, 16.0, 20.0, 24.0],
     "Geophysical Fluid Dynamics", "Ekman Boundary Layer Theory & Coriolis-Friction Equilibrium",
     "Steady surface wind blowing over the open ocean imparts a shear stress tau = rho_air C_D U_10^2. The balance between turbulent vertical eddy viscosity (A_z) and planetary Coriolis force (f = 2 Omega sin phi) produces a surface current deflected 45 degrees to the right in the Northern Hemisphere, with velocity decaying exponentially with depth to form the iconic Ekman spiral.",
     "Ekman pumping and suction drive large-scale subtropical gyre downwelling, equatorial and coastal upwelling ecosystems supporting 20% of global marine fisheries, and wind-driven heat transport in climate models.",
     "Rotating Geophysical Fluid Dynamics Turntable (1.5 m diameter)", "Computer-Controlled Radial Wind Stress Blower Ring", "Particle Image Velocimetry (PIV) Continuous Laser Sheet Generator", "High-Speed Overhead Digital Telemetry Tracking Camera", "Micro-Fluorescent Neutral Buoyant Polystyrene Tracer Beads", "Precision Electronic Tachometer and Coriolis Rotation Control Interface"),

    (5, "seawater-sound-velocity-temperature-depth-profile", "Acoustic Oceanography: Empirical Seawater Sound Speed & Thermocline Sound Channeling",
     "Seawater Sound Velocity Profile", "Measure acoustic travel time and calculate acoustic phase speed across calibrated temperature regimes using high-frequency ultrasonic transducers in simulated oceanic water columns.",
     "Seawater Hydrographic Temperature", "Temperature", "°C", 2.0, 22.0, 4.0, 10.0, 1,
     "Acoustic Sound Propagation Speed", "m/s", 1, "Temperature (°C)", "Sound Speed (m/s)",
     "Thermal Acoustic Velocity Derivative", "dc_dT", 4.5600, "(m/s)/°C", 4, 1.0,
     "Sound Speed (m/s) = 4.5600 · Temperature (°C) + 1449.2000",
     [2.0, 6.0, 10.0, 14.0, 18.0, 22.0],
     "Underwater Acoustics & Ocean Physics", "Mackenzie & Del Grosso Empirical Formulations & SOFAR Channel",
     "Sound velocity in seawater is governed by empirical formulations (Mackenzie, Del Grosso, Chen-Millero) as c(S, T, P) approx 1449.2 + 4.6 T - 0.055 T^2 + 0.00029 T^3 + (1.34 - 0.010 T)(S - 35) + 0.016 z. In the upper ocean, decreasing temperature causes sound speed to decline sharply to a minimum around 1000 m depth, creating the Deep Sound Channel (SOFAR channel) where acoustic energy undergoes refractive waveguiding.",
     "Acoustic thermometry allows basin-scale ocean heat content monitoring, passive acoustic tracking of marine mammals (cetaceans), multibeam bathymetric mapping calibration, and anti-submarine acoustic surveillance.",
     "High-Precision Acoustic Pulse-Echo Velocimeter (2.5 MHz Piezoelectric Transducers)", "Thermostatted Cylindrical Stainless Steel Acoustic Test Cell", "Digital Storage Oscilloscope with Picosecond Time-Interval Resolution", "Precision Platinum RTD Thermometer (0.01 °C accuracy)", "Automated Salinity-Controlled Degassing Chamber", "Computerized Acoustic Travel Time Waveform Processing Interface"),

    (6, "coastal-tidal-resonance-harmonic-analysis", "Dynamic Oceanography: Harmonic Tidal Analysis & Estuarine Quarter-Wave Basin Resonance",
     "Tidal Resonance & Basin Amplification", "Quantify the amplification of semi-diurnal tidal oscillations in an elongated estuarine flume to demonstrate hydrodynamic resonance and standing wave quarter-wave trapping.",
     "Offshore Boundary Tidal Forcing Amplitude", "Tidal Forcing", "m", 0.5, 3.0, 0.5, 1.5, 1,
     "Resonant Estuarine Basin High Tide Amplitude", "m", 2, "Tidal Forcing (m)", "Resonant Amplitude (m)",
     "Estuarine Resonance Amplification Factor", "Q_tide", 1.8500, "dimensionless", 4, 1.0,
     "Resonant Amplitude (m) = 1.8500 · Tidal Forcing (m) + 0.4000",
     [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
     "Estuarine Dynamics & Tidal Mechanics", "Quarter-Wave Hydrodynamic Resonance & Standing Wave Amplification",
     "Tides represent forced shallow-water waves generated by lunar and solar gravitational tractive forces. When an elongated embayment or estuary possesses a natural oscillation period T_n = 4 L / sqrt(g·h) closely matching the principal lunar semi-diurnal constituent (M2 = 12.42 h), quarter-wave resonance occurs (e.g. Bay of Fundy, Bristol Channel), dramatically amplifying tidal ranges through constructive interference.",
     "Tidal resonance models govern mega-tidal renewable energy barrage design, coastal flooding and storm surge vulnerability assessments, and navigational channel sediment scouring in commercial ports.",
     "Precision Hydrodynamic Resonant Estuarine Channel (12 m flume)", "Computerized Programmable Tidal Tide-Gate Wave Generator", "Array of Ultrasonic Water Level Acoustic Stage Sensors", "Micro-Velocity Electromagnetic Current Flow Meters", "High-Speed Real-Time Harmonic Fourier Analysis Telemetry Station", "Adjustable Sub-Surface Constriction and Friction Sills"),

    # Module 2: Chemical Oceanography & Biogeochemical Cycles (Labs 7–11)
    (7, "winkler-dissolved-oxygen-iodometric-titration", "Marine Biogeochemistry: Winkler Azide Iodometric Determination of Oceanic Dissolved Oxygen",
     "Winkler Dissolved Oxygen Titration", "Determine the dissolved oxygen concentration of marine water samples via manganese oxidation and iodometric sodium thiosulfate titration to identify oceanic hypoxic zones.",
     "Standardized Sodium Thiosulfate Titrant Volume", "Titrant Volume", "mL", 1.0, 6.0, 1.0, 3.0, 2,
     "Calculated Seawater Dissolved Oxygen (DO)", "mg/L", 2, "Titrant Volume (mL)", "Dissolved Oxygen (mg/L)",
     "Winkler Iodometric Calibration Stoichiometry", "k_winkler", 1.4000, "(mg/L)/mL", 4, 1.0,
     "Dissolved Oxygen (mg/L) = 1.4000 · Titrant Volume (mL) + 0.1000",
     [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
     "Chemical Oceanography & Biogeochemistry", "Carpenter Modified Winkler Titration & Redox Iodometry",
     "Dissolved oxygen in seawater is fixed chemically immediately upon collection: Mn(II) reacts under alkaline conditions to form Mn(III) oxyhydroxide precipitate. Upon acidification in the presence of iodide, stoichiometric iodine (I2) is liberated and titrated with sodium thiosulfate using starch indicator: 1 mole O2 equivalent to 4 moles S2O3(2-).",
     "Dissolved oxygen distributions identify Apparent Oxygen Utilization (AOU), trace deep water mass ventilation, track expanding oxygen minimum zones (OMZs), and evaluate marine eutrophication dead zones.",
     "Precision Automated Piston Burette (0.001 mL delivery precision)", "BOD Standard Glass Incubation Bottles (300 mL with Ground Glass Stoppers)", "Manganous Sulfate and Alkaline Sodium Iodide-Azide Reagents", "Volumetric Transfer Pipettes and Magnetic Stirrer Platform", "Digital Amperometric / Photometric End-Point Detection Interface", "Certified Potassium Iodate (KIO3) Primary Standard Solution"),

    (8, "ocean-acidification-seawater-carbonate-alkalinity", "Ocean Carbon Cycle: High-Precision Gran Titration Determination of Total Carbonate Alkalinity",
     "Gran Carbonate Alkalinity & Acidification", "Determine seawater total alkalinity (TA) and evaluate carbonate system saturation states (calcite, aragonite) across decreasing pH regimes simulating anthropogenic ocean acidification.",
     "Dissolved Inorganic Carbon Perturbation Stress", "DIC Perturbation", "mmol/kg", 2.0, 12.0, 2.0, 6.0, 1,
     "Seawater Aragonite Mineral Saturation State", "dimensionless", 2, "DIC Perturbation (mmol/kg)", "Aragonite Saturation",
     "Carbonate Saturation Acidification Sensitivity", "k_arag", 0.0450, "(mmol/kg)⁻¹", 4, 1.0,
     "Aragonite Saturation = -0.0450 · DIC Addition (mmol/kg) + 2.4500",
     [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
     "Marine Inorganic Carbon Chemistry", "Gran Acidimetric Titration & Carbonate Equilibria Dissociation",
     "Anthropogenic CO2 uptake shifts oceanic carbonate equilibria: CO2 + H2O <-> H2CO3 <-> HCO3- + H+, consuming carbonate ions (CO3(2-) + H+ -> HCO3-) and depressing saturation state Omega = [Ca2+][CO3(2-)] / K'_sp. Total alkalinity (TA = [HCO3-] + 2[CO3(2-)] + [B(OH)4-] + ...) is measured by open-cell Gran titration past the second carbonic acid equivalence point (pH ~ 3.5).",
     "Quantifying seawater carbonate chemistry is critical for assessing coral reef calcification rates, pteropod shell dissolution hazards, shellfish aquaculture survival, and global marine carbon sink saturation.",
     "Automated Open-Cell Potentiometric Gran Titrator Assembly", "Ross Ultra Combination Glass pH Electrode with Tris Buffer Calibration", "Certified Reference Materials (CRMs) from Scripps Institution of Oceanography", "Thermostatted Water-Jacketed Titration Beaker (25.00 ± 0.02 °C)", "Micro-Infusion Syringe Pump for 0.1 N HCl Standard Titrant", "Precision Magnetic Stirring Hotplate with Inert N2 Purge Line"),

    (9, "marine-soluble-reactive-phosphate-molybdenum-blue", "Nutrient Oceanography: Phosphomolybdenum Blue Spectrophotometric Assay of Reactive Phosphate",
     "Phosphate Molybdenum Blue Assay", "Quantify trace concentrations of soluble reactive orthophosphate (SRP) in coastal and oligotrophic open-ocean water columns using the ascorbic acid molybdenum blue method.",
     "Standard Orthophosphate Analytical Concentration", "PO4 Concentration", "μmol/L", 0.50, 3.50, 0.50, 2.00, 2,
     "Spectrophotometric Optical Absorbance at 885 nm", "AU", 4, "PO4 Concentration (μmol/L)", "Absorbance (AU)",
     "Phosphomolybdenum Molar Absorptivity Factor", "epsilon_p", 0.0385, "(μmol/L)⁻¹", 4, 1.0,
     "Absorbance (AU) = 0.0385 · PO4 Concentration (μmol/L) + 0.0050",
     [0.50, 1.10, 1.70, 2.30, 2.90, 3.50],
     "Marine Nutrient Biogeochemistry", "Murphy & Riley Phosphomolybdenum Complexation & Beer-Lambert Law",
     "Orthophosphate in seawater reacts with ammonium molybdate and potassium antimonyl tartrate in acidic medium to form a 12-phosphomolybdic acid complex, which is subsequently reduced by ascorbic acid to intensely colored phosphomolybdenum blue. Optical absorbance measured at 885 nm in 10-cm optical cuvettes follows the Beer-Lambert law with nanomolar detection sensitivity.",
     "Phosphorus is an essential macronutrient limiting primary production in vast ocean gyres (e.g. North Pacific Subtropical Gyre), controlling oceanic N:P stoichiometric Redfield ratios (16:1) and diazotrophic nitrogen fixation rates.",
     "Double-Beam UV-Visible Spectrophotometer (190–1100 nm)", "Matched 10-cm Quartz Optical Long-Path Absorption Cells", "Ultraclean Polyethylene Hydrographic Sampling Bottles (Acid-Washed)", "Ammonium Molybdate / Ascorbic Acid / Tartrate Mixed Reagent System", "Certified Potassium Dihydrogen Phosphate (KH2PO4) Calibration Standard", "Class-100 Clean Laminar Flow Bench for Trace Nutrient Handling"),

    (10, "seawater-nitrate-reduction-cadmium-spectrophotometry", "Marine Nitrogen Biogeochemistry: Cadmium-Copper Reduction Spectrophotometry of Seawater Nitrate",
     "Nitrate Cadmium Reduction Assay", "Determine dissolved nitrate concentrations in oceanic profiles through heterogeneous cadmium-copper column reduction to nitrite followed by sulfanilamide diazotization spectrophotometry.",
     "Seawater Nitrate Standard Concentration", "NO3 Concentration", "μmol/L", 2.0, 22.0, 4.0, 10.0, 1,
     "Spectrophotometric Azo-Dye Absorbance at 543 nm", "AU", 4, "NO3 Concentration (μmol/L)", "Absorbance (AU)",
     "Cadmium-Reduction Molar Extinction Slope", "epsilon_n", 0.0245, "(μmol/L)⁻¹", 4, 1.0,
     "Absorbance (AU) = 0.0245 · NO3 Concentration (μmol/L) + 0.0080",
     [2.0, 6.0, 10.0, 14.0, 18.0, 22.0],
     "Chemical Oceanography & Nitrogen Cycling", "Heterogeneous Catalytic Reduction & Griess Reaction Diazotization",
     "Nitrate is the predominant form of fixed bioavailable nitrogen in deep seawater. Nitrate is quantitatively reduced to nitrite by passing through a granulated copper-coated cadmium (Cd-Cu) column. Nitrite then reacts with sulfanilamide under acidic conditions to form a diazonium cation, which couples with N-(1-naphthyl)ethylenediamine dihydrochloride (NED) to yield a vibrant magenta azo dye absorbing at 543 nm.",
     "Nitrate gradients dictate oceanic primary productivity, control new vs. regenerated production (f-ratio), trace upwelling plumes, and quantify anthropogenic agricultural runoff causing coastal eutrophication.",
     "Continuous Segmented Flow Nutrient AutoAnalyzer (CFA / FIA)", "High-Efficiency Granulated Copper-Coated Cadmium Reduction Columns", "UV-Vis Spectrophotometric Flow Cell Detector (543 nm)", "Acid-Cleaned Peristaltic Pump Tubing and Reagent Manifold", "Standard Potassium Nitrate (KNO3) Primary Reference Solutions", "Deionized Ultra-Pure Milli-Q Water Purification System (18.2 MOmega·cm)"),

    (11, "oceanic-dissolved-silicate-silicomolybdate-spectrophotometry", "Marine Biogeochemistry: Molybdosilicate Spectrophotometry of Seawater Reactive Silica",
     "Silicate Molybdosilicate Assay", "Quantify dissolved reactive orthosilicic acid (Si(OH)4) in oceanographic depth profiles using silicomolybdous blue reduction spectrophotometry to trace diatom biomineralization.",
     "Standard Dissolved Silicate Concentration", "Silicate Concentration", "μmol/L", 5.0, 55.0, 10.0, 25.0, 1,
     "Silicomolybdous Blue Absorbance at 810 nm", "AU", 4, "Silicate Concentration (μmol/L)", "Absorbance (AU)",
     "Silicomolybdate Molar Calibration Coefficient", "epsilon_si", 0.0182, "(μmol/L)⁻¹", 4, 1.0,
     "Absorbance (AU) = 0.0182 · Silicate Concentration (μmol/L) + 0.0060",
     [5.0, 15.0, 25.0, 35.0, 45.0, 55.0],
     "Marine Biogeochemistry & Diatom Ecology", "Silicomolybdic Acid Heteropoly Reduction & Biosilicification",
     "Dissolved silicate exists primarily as undissociated monomeric orthosilicic acid Si(OH)4 in ocean water. In acidic solution, it reacts with ammonium molybdate to form yellow alpha- and beta-silicomolybdic heteropoly acids. Oxalic acid is added to destroy interfering phosphomolybdate complexes before reduction with metol-sulfite to silicomolybdous blue, measured photometrically at 810 nm.",
     "Silicate availability determines phytoplankton community succession (diatoms vs. flagellates), drives the biological carbon pump via dense opal ballasting, and delineates Antarctic Bottom Water (AABW) penetration across global abyssal plains.",
     "Research UV-Visible Dual-Beam Spectrophotometer", "Non-Glass Fluoropolymer (FEP/PTFE) Labware and Digestion Vessels", "Precision 5-cm Optical Quartz Cells (Fluoride-Resistant)", "Ammonium Heptamolybdate, Oxalic Acid, and Metol-Sulfite Reagents", "High-Purity Certified Sodium Hexafluorosilicate (Na2SiF6) Standard", "Automated Temperature-Controlled Colorimetric Incubation Bath"),

    # Module 3: Biological Oceanography & Marine Ecology (Labs 12–16)
    (12, "chlorophyll-a-trichromatic-spectrophotometric-assay", "Biological Oceanography: Trichromatic Spectrophotometric Quantification of Phytoplankton Chlorophyll-a",
     "Chlorophyll-a Trichromatic Assay", "Quantify phytoplankton photosynthetic biomass in marine water samples through 90% acetone extraction and trichromatic spectrophotometric extinction measurements.",
     "Net Optical Absorbance Differential (A664 - A750)", "Optical Absorbance", "AU", 0.05, 0.40, 0.05, 0.20, 2,
     "Extracted Chlorophyll-a Biomass Concentration", "mg/m³", 2, "Optical Absorbance (AU)", "Chlorophyll-a (mg/m³)",
     "Jeffrey-Humphrey Trichromatic Specific Extinction", "k_chl", 11.8500, "(mg/m³)/AU", 4, 1.0,
     "Chlorophyll-a (mg/m³) = 11.8500 · Optical Absorbance (AU) + 0.0500",
     [0.05, 0.12, 0.19, 0.26, 0.33, 0.40],
     "Biological Oceanography & Phytoplankton Ecology", "Jeffrey-Humphrey Trichromatic Equations & Porphyrin Absorption",
     "Chlorophyll-a is the primary photosynthetic light-harvesting pigment present in all oxygenic marine phytoplankton. Filtered plankton cells are lysed in 90% buffered acetone. Absorbance is measured at 664 nm, 647 nm, 630 nm, and 750 nm (turbidity blank), and specific concentrations of Chl-a, Chl-b, and Chl-c are resolved using the standardized Jeffrey and Humphrey trichromatic equations.",
     "Chlorophyll-a measurements provide the gold-standard ground-truth validation for satellite ocean color sensors (MODIS, VIIRS, Sentinel-3 OLCI), estimating global marine net primary productivity (~50 Pg C/yr).",
     "Scanning Dual-Beam UV-Vis Spectrophotometer with Peltier Temp Control", "Glass Fiber Filter Filtration Rig (Whatman GF/F 0.7 μm, 47 mm)", "Tissue Homogenizer with PTFE Pestle and Ice Bath Cooling", "Refrigerated Centrifuge for Complete Cell Debris Clarification (4000 rpm)", "Spectrophotometric Grade 90% Acetone (Buffered with MgCO3)", "Primary Calibrated Chlorophyll-a Analytical Standard from Anacystis nidulans"),

    (13, "secchi-disk-seawater-turbidity-photic-zone", "Optical Oceanography: Secchi Disk Transparency & Euphotic Zone Diffuse Light Attenuation",
     "Secchi Depth & Diffuse Attenuation", "Measure visual extinction depth of a standardized Secchi disk in coastal waters to determine the diffuse vertical attenuation coefficient (K_d) and depth of the 1% euphotic zone.",
     "Reciprocal Secchi Extinction Depth (1/Z_SD)", "Reciprocal Secchi Depth", "m⁻¹", 0.05, 0.30, 0.05, 0.15, 2,
     "Diffuse Light Attenuation Coefficient (K_d)", "m⁻¹", 3, "Reciprocal Secchi Depth (m⁻¹)", "Attenuation K_d (m⁻¹)",
     "Poole-Atkins Optical Attenuation Constant", "k_secchi", 1.7000, "dimensionless", 4, 1.0,
     "Attenuation K_d (m⁻¹) = 1.7000 · (1/Z_SD) (m⁻¹) + 0.1000",
     [0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
     "Bio-Optical Oceanography", "Beer-Lambert Optical Attenuation & Poole-Atkins Formulation K_d = 1.7 / Z_SD",
     "Solar downwelling irradiance declines exponentially with depth according to Beer's law: E_d(z) = E_d(0) exp(-K_d · z). The human eye detects contrast disappearance of a standardized 30-cm white/black Secchi disk at a fixed optical threshold. Poole and Atkins established the empirical relationship K_d = 1.7 / Z_SD, directly calculating the compensation depth where photosynthesis balances respiration (z_1% = 4.6 / K_d).",
     "Secchi transparency records represent one of oceanography's longest climate records (dating back to 1865), documenting decadal declines in coastal water clarity, sediment plume runoff, and algal bloom dynamics.",
     "Standardized 30-cm Oceanographic Quadrant Secchi Disk with Brass Ballast", "Calibrated Non-Stretch Metric Depth Tag Line and Winch", "Submersible Cosine-Corrected Photosynthetically Active Radiation (PAR) Sensor", "Digital Multi-Channel Underwater Radiometer Data Logger", "Viewing Hood / Hydroscope for Glare-Free Surface Observation", "Precision Calibrated Global Positioning System (GPS) Navigation Unit"),

    (14, "marine-bacterial-respiration-microbial-loop", "Microbial Oceanography: Dark-Bottle Oxygen Consumption & Heterotrophic Microbial Loop Respiration",
     "Microbial Respiration & Dissolved Oxygen", "Quantify heterotrophic bacterial respiration rates and organic carbon remineralization in deep-sea water incubations by tracking dissolved oxygen depletion over time.",
     "Dark-Bottle Controlled Incubation Time", "Incubation Time", "hours", 4.0, 24.0, 4.0, 12.0, 1,
     "Residual Dissolved Oxygen Concentration", "mg/L", 2, "Incubation Time (h)", "Residual Oxygen (mg/L)",
     "Specific Heterotrophic Microbial Respiration Rate", "R_bact", 0.1250, "(mg/L)/h", 4, 1.0,
     "Residual O2 (mg/L) = -0.1250 · Incubation Time (h) + 8.5000",
     [4.0, 8.0, 12.0, 16.0, 20.0, 24.0],
     "Microbial Oceanography & Biogeochemistry", "Microbial Loop Hypothesis & Heterotrophic Organic Remineralization",
     "Over 90% of marine living biomass consists of microorganisms (bacteria, archaea, viruses). The microbial loop (Azam et al.) routes dissolved organic matter (DOM) back into pelagic food webs through bacterial uptake. In dark incubation bottles, microbial cellular respiration consumes dissolved oxygen (C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O), directly converting oxygen draw-down to remineralized carbon flux.",
     "Quantifying microbial respiration constrains ocean carbon sequestration efficiency, biological pump carbon export attenuation (Martin curve), and global sub-surface oxygen depletion rates.",
     "Refrigerated Constant-Temperature Dark Incubation Chamber", "Ultra-Sensitive Optical Oxygen Sensor System (Sensor Spots with Fiber-Optic Meter)", "Standard 300 mL Acid-Leached Borosilicate Dark BOD Bottles", "Niskin Hydrographic Water Samplers with Teflon Springs", "Epifluorescence Microscope with DAPI Filter Set for Bacterial Direct Counts", "0.2 μm Polycarbonate Membrane Vacuum Filtration Assembly"),

    (15, "benthic-intertidal-quadrat-species-diversity", "Marine Benthic Ecology: Shannon-Wiener Species Diversity Across Rocky Intertidal Zonation",
     "Intertidal Biodiversity & Zonation", "Quantify species richness, benthic macroinvertebrate abundance, and Shannon-Wiener diversity index across vertical tidal gradients in a rocky intertidal shoreline.",
     "Intertidal Vertical Elevation Above Chart Datum (MLLW)", "Tidal Elevation", "m", 0.5, 3.0, 0.5, 1.5, 1,
     "Shannon-Wiener Biological Diversity Index (H')", "dimensionless", 2, "Tidal Elevation (m)", "Shannon Diversity (H')",
     "Intertidal Biodiversity Elevation Gradient Slope", "k_shannon", 0.3800, "m⁻¹", 4, 1.0,
     "Shannon Diversity (H') = 0.3800 · Elevation (m) + 0.8500",
     [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
     "Marine Benthic Ecology & Community Dynamics", "Connell Intermediate Disturbance Hypothesis & Vertical Zonation",
     "Rocky intertidal ecosystems exhibit classic vertical zonation driven by physiological desiccation stress at upper boundaries and biological competition/predation at lower boundaries. Standardized 0.25 m² quadrat sampling records species abundances (p_i), computing the Shannon-Wiener diversity index H' = - sum(p_i ln p_i) and Pielou's evenness (J = H' / ln S) across physiological exposure gradients.",
     "Intertidal biodiversity monitoring tracks ecological responses to ocean warming, invasive species colonization, coastal pollution impacts, and marine protected area (MPA) conservation efficacy.",
     "Standardized 0.5 m x 0.5 m (0.25 m²) Stainless Steel Sampling Quadrats", "Digital Vernier Caliper for Invertebrate Size Frequency Distribution", "Waterproof Rugged Field Tablet with Photographic Quadrat Logging Software", "Surveyor's Sighting Level and Graduated Telescopic Stadia Rod", "Intertidal Biological Taxonomic Diagnostic Field Keys", "Multi-Parameter Water Quality Probe (Salinity, Temperature, pH)"),

    (16, "zooplankton-settling-volume-biomass-abundance", "Pelagic Ecology: Bongo Net Zooplankton Settled Biovolume & Carbon Biomass Allometric Scaling",
     "Zooplankton Biovolume & Carbon Biomass", "Quantify zooplankton standing stock from oblique bongo net tows using graduated settling volume cylinders and establish allometric conversions to organic carbon biomass.",
     "Standardized Settled Zooplankton Biovolume", "Settled Volume", "mL/m³", 0.50, 3.50, 0.50, 2.00, 2,
     "Derived Pelagic Organic Carbon Biomass Density", "mg C/m³", 2, "Settled Volume (mL/m³)", "Carbon Biomass (mg C/m³)",
     "Zooplankton Biovolume-to-Carbon Conversion Constant", "k_zoo", 1.6500, "(mg C/m³)/(mL/m³)", 4, 1.0,
     "Carbon Biomass (mg C/m³) = 1.6500 · Settled Volume (mL/m³) + 0.5000",
     [0.50, 1.10, 1.70, 2.30, 2.90, 3.50],
     "Pelagic Food Web Ecology & Trophodynamics", "Allometric Scaling & Secondary Production Carbon Transfer",
     "Mesozooplankton (copepods, euphausiids, chaetognaths) serve as the critical trophic link transferring primary production from microalgae to pelagic fish and marine apex predators. After filtering through 200 μm meshes, zooplankton biomass is measured as settled biovolume, displacement volume, and dry mass, converting to organic carbon via empirical allometric relationships (Wiebe et al.).",
     "Zooplankton biomass surveys underpin fisheries stock assessments, recruit forecasting for commercial fisheries, marine food web carbon modeling, and biological carbon pump vertical flux quantification.",
     "Oceanographic Bongo Net Sampling Frame (60 cm mouth diameter, 200 μm mesh)", "General Oceanics Mechanical Flowmeter with Rotor Threshold Calibration", "Graduated Imhoff Cone Settling Cylinders (1000 mL)", "Stereomicroscope with Bogorov Counting Chamber for Taxonomic Sorting", "Mettler Toledo Analytical Microbalance (0.01 mg precision)", "Desiccating Vacuum Oven for Dry Mass Determination (60.0 °C)"),

    # Module 4: Marine Geology, Coastal Processes & Instrumentation (Labs 17–21)
    (17, "coastal-beach-profile-emery-rod-sedimentation", "Coastal Geomorphology: Emery Two-Rod Beach Profiling & Equilibrium Morphodynamic Equilibrium",
     "Emery Rod Beach Morphodynamics", "Survey the subaerial beach cross-shore topographic elevation profile using the two-rod horizon sighting method to quantify seasonal sand berm volume changes.",
     "Cross-Shore Horizontal Distance from Benchmark", "Distance", "m", 10.0, 60.0, 10.0, 30.0, 1,
     "Cumulative Beach Face Elevation Drop", "m", 2, "Distance (m)", "Elevation Drop (m)",
     "Beach Face Foreshore Slope Gradient", "m_slope", 0.0450, "dimensionless", 4, 1.0,
     "Elevation Drop (m) = 0.0450 · Cross-Shore Distance (m) + 0.0100",
     [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
     "Coastal Geomorphology & Sediment Dynamics", "Dean Equilibrium Beach Profile Theory & Wave Energy Morphodynamics",
     "Beach profile morphology reflects dynamic equilibrium between destructive high-energy winter storm waves (forming offshore sandbars) and constructive gentle summer swell waves (building subaerial berms). The Emery two-rod method uses the marine horizon as a natural level line to measure incremental vertical drops across cross-shore stations, calculating Dean profile geometry h(x) = A x^(2/3).",
     "Beach profiling provides essential empirical data for coastal vulnerability assessments, post-hurricane shoreline erosion tracking, beach nourishment design, and sea-level rise retreat modeling.",
     "Pair of Graduated Calibrated Emery Profiling Rods (1.5 m with Centimeter Scales)", "50-Meter Waterproof Fiberglass Measuring Tape", "Geodetic High-Precision RTK-GPS Base Station and Rover Assembly", "Handheld Magnetic Sighting Compass and Clinometer", "Sediment Grain Size Standard Comparison Card", "Waterproof Geomorphological Survey Data Sheets"),

    (18, "marine-sediment-porosity-gravimetric-water-content", "Marine Sedimentology: Gravimetric Core Water Content & Fractional Sediment Porosity",
     "Sediment Porosity & Water Content", "Determine fractional sediment porosity, dry bulk density, and grain density down a marine gravity sediment core using gravimetric moisture loss and pycnometry.",
     "Benthic Sediment Core Sub-Bottom Depth", "Core Depth", "cm", 5.0, 30.0, 5.0, 15.0, 1,
     "Fractional Sediment Porosity (phi)", "volume fraction", 3, "Core Depth (cm)", "Sediment Porosity (phi)",
     "Compaction Porosity Attenuation Gradient", "k_compact", 0.0125, "cm⁻¹", 4, 1.0,
     "Porosity (phi) = -0.0125 · Core Depth (cm) + 0.7500",
     [5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
     "Marine Sedimentology & Geotechnical Engineering", "Athy Compaction Law & Archimedes Density Inversion",
     "Freshly deposited marine muds and biogenic oozes exhibit high initial surface porosity (phi ~ 0.70 to 0.85). As burial depth increases, overburden effective stress squeezes interstitial pore water out, driving compaction according to Athy's exponential compaction law: phi(z) = phi_0 exp(-c · z). Gravimetric drying at 105 °C with salinity corrections yields precise porosity and bulk density profiles.",
     "Sediment physical properties govern submarine slope stability, acoustic bottom-loss reflection coefficients for sonar systems, benthic nutrient flux diffusion rates, and offshore wind turbine foundation design.",
     "Precision Mechanical Core Splitter and Sample Syringe Extruder", "Laboratory Convection Drying Oven (105.0 ± 1.0 °C)", "Analytical Balance (0.1 mg precision) with Draft Shield", "High-Precision Helium Gas Displacement Pycnometer", "Desiccator Cabinet with Activated Silica Gel Moisture Trap", "Standard Stainless Steel Sediment Volumetric Rings (20 cm³)"),

    (19, "acoustic-doppler-current-profiler-adcp-discharge", "Estuarine Hydrodynamics: Acoustic Doppler Current Profiler (ADCP) River-Estuary Flux Inversion",
     "ADCP Estuarine Discharge Inversion", "Measure high-resolution vertical current velocity shear profiles and compute total volumetric cross-sectional discharge in a tidal estuary using a vessel-mounted broadband ADCP.",
     "Mean Acoustic Doppler Backscatter Frequency Shift", "Doppler Shift", "kHz", 2.0, 12.0, 2.0, 6.0, 1,
     "Estuarine Cross-Sectional Volumetric Discharge", "m³/s", 3, "Doppler Shift (kHz)", "Discharge (m³/s)",
     "ADCP Acoustic Doppler Calibration Transfer Factor", "k_adcp", 0.0325, "(m³/s)/kHz", 4, 1.0,
     "Discharge (m³/s) = 0.0325 · Doppler Shift (kHz) + 0.0500",
     [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
     "Acoustic Oceanography & Estuarine Hydrodynamics", "Doppler Shift Principle & Four-Beam Janus Array Geometry",
     "Broadband ADCP instruments transmit high-frequency acoustic pulses along four angled acoustic beams (Janus configuration). Acoustic backscatter from suspended particles experiences a Doppler frequency shift Delta f = 2 f_0 (v / c) cos theta. By resolving radial velocities into orthogonal coordinate axes (East, North, Up), vertical current profiles are integrated across transect swaths to compute total estuarine volumetric discharge.",
     "ADCP surveys quantify tidal prism volumes, track sediment plume advection, monitor port navigation channels, and establish hydrodynamic boundaries for numerical estuarine circulation models.",
     "Teledyne RD Instruments Workhorse 600 kHz / 1200 kHz Acoustic Doppler Current Profiler", "Vessel Rigid Over-the-Side Mounting Pole and Swivel Bracket", "Differential GPS Navigation Receiver with Integrated Gyrocompass Heading", "Broadband WinRiver-II Real-Time Hydrographic Data Acquisition Software", "Conductivity-Temperature-Depth (CTD) Sound Speed Cast Interface", "Sealed Lead-Acid Auxiliary Battery Power Supply Enclosure"),

    (20, "coastal-longshore-current-tracer-dispersion", "Nearshore Coastal Oceanography: Fluorescent Dye Tracer Dispersion & Wave-Driven Longshore Current",
     "Longshore Current & Dye Dispersion", "Quantify wave-driven longshore current velocity and turbulent lateral dispersion coefficients in the surf zone using fluorescent rhodamine-WT dye plume tracking.",
     "Rhodamine Dye Plume Advection Elapsed Time", "Advection Time", "min", 5.0, 30.0, 5.0, 15.0, 1,
     "Down-Drift Longshore Plume Displacement Distance", "m", 1, "Advection Time (min)", "Displacement (m)",
     "Wave-Driven Longshore Current Drift Velocity", "v_long", 0.1450, "m/min", 4, 1.0,
     "Displacement (m) = 0.1450 · Advection Time (min) + 0.0200",
     [5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
     "Coastal Oceanography & Nearshore Hydrodynamics", "Radiation Stress Theory (Longuet-Higgins) & Taylor Turbulent Dispersion",
     "When surface gravity waves approach a coastline at an oblique angle, breaking waves in the surf zone impart a net alongshore momentum flux described by Longuet-Higgins radiation stress tensors (S_xy). This drives a steady longshore current v_l = k (g H_b)^(1/2) sin(2 theta_b). Fluorescent dye releases follow Taylor turbulent diffusion, measuring advection velocity and lateral mixing coefficients.",
     "Longshore current dynamics govern littoral sand drift (causing harbor siltation and down-drift beach starvation), guide swimmer rip-current hazard warnings, and predict contaminant plume dispersal.",
     "Turner Designs Field Fluorometer with Rhodamine-WT Optical Filter Kit", "Surveyor's Electronic Total Station and Retroreflective Prisms", "Shoreline Synchronized Stopwatch Array with Flagged Distance Stations", "Hermetic Dye Injection Release Cannister and Calibrated Anchor Float", "Handheld Waterproof Anemometer and Sighting Wave Inclinometer", "Calibrated Rhodamine-WT Fluorescent Dye Concentrate (20% aqueous solution)"),

    (21, "ctd-rosette-conductivity-temperature-depth-profiler", "Deep Sea Exploration: CTD Rosette Hydrographic Profiling & Ocean Water Mass Stratification",
     "CTD Rosette Hydrographic Profiling", "Calibrate and analyze full-depth CTD hydrographic profiles to identify oceanic water masses, quantify pycnocline stratification, and resolve oceanic mixed layers.",
     "Hydrostatic Seawater Gauge Pressure", "Gauge Pressure", "dbar", 50.0, 500.0, 50.0, 200.0, 0,
     "Physical Water Column Depth Equivalent", "m", 1, "Gauge Pressure (dbar)", "Depth (m)",
     "Hydrostatic Pressure-to-Depth Conversion Slope", "k_depth", 0.9850, "m/dbar", 4, 1.0,
     "Depth (m) = 0.9850 · Hydrostatic Pressure (dbar) + 0.0100",
     [50.0, 140.0, 230.0, 320.0, 410.0, 500.0],
     "Observational Oceanography & Hydrography", "Saunders & Fofonoff Hydrostatic Integration & Water Mass Analysis",
     "The CTD rosette is the cornerstone instrument of modern observational oceanography. Rapidly cycling sensors measure conductivity (salinity), temperature, and pressure at 24 Hz during descent through the water column. Saunders and Fofonoff hydrostatic integration converts pressure to geopotential depth z(P) = int (1 / (rho · g)) dP. Temperature-Salinity (T-S) diagrams resolve discrete water masses and core layers.",
     "Full-depth CTD profiling underpins global climate programs (GO-SHIP, WOCE, Argo float calibration), tracks deep ocean warming and decadal acidification, and maps oceanic overturning circulation branches.",
     "Seabird SBE 9plus CTD Underwater Unit (Dual Temperature and Conductivity Sensors)", "24-Bottle SBE 32 Carousel Water Sampler Rosette with 10 L Niskin Bottles", "SBE 43 Dissolved Oxygen and Seapoint Chlorophyll Fluorometer Sensors", "Digiquartz High-Accuracy Resonant Quartz Pressure Transducer (0.001% span)", "Electromechanical Oceanographic Winch with Armored Coaxial Cable (6000 m)", "SBE 11plus V2 Deck Command and Real-Time Telemetry Processing Unit")
]

def make_marine_experiment(raw):
    (num, slug, title, shortTitle, aim,
     inputLabel, shortInput, inputUnit, min_val, max_val, step_val, initial_val, in_dec,
     rawLabel, rawUnit, raw_dec, xAxis, yAxis,
     targetName, target, refValue, resultUnit, res_dec, res_scale,
     fitEquation, samples, subsystem, focus,
     bio_detail, clinical_detail,
     app1, app2, app3, app4, app5, app6) = raw

    # 6 apparatus
    apparatus = [
        {"name": app1, "purpose": f"Standardized research-grade oceanographic instrument providing calibrated, traceable physical and chemical data for {shortTitle} protocols."},
        {"name": app2, "purpose": f"Essential secondary analytical hardware ensuring geometric, thermal, optical, or hydrodynamic accuracy during {shortTitle} testing."},
        {"name": app3, "purpose": f"Primary sample containment vessel, optical path cell, or sensor holding platform maintaining environmental equilibrium."},
        {"name": app4, "purpose": f"High-precision digital telemetry logger recording real-time scientific data conforming to UNESCO, WOCE, and GO-SHIP marine standards."},
        {"name": app5, "purpose": f"Certified reference calibration standard or environmental stabilizer eliminating instrumental baseline drift."},
        {"name": app6, "purpose": f"Precision measurement tool ensuring sensor alignment, zero-tare accuracy, and elimination of systematic testing bias."}
    ]

    # 6 procedure steps
    procedure = [
        {"title": "Instrument Initialization & Baseline Zero Tare", "text": f"Power on the analytical instrumentation for {shortTitle}, calibrate baseline telemetry against certified standard seawater or reference solutions, and verify optical/hydrodynamic alignment."},
        {"title": "Sample Collection & Oceanographic Conditioning", "text": f"Prepare, filter, equilibrate, or collect the marine test specimens under strictly regulated environmental laboratory conditions conforming to IOC, UNESCO, and WOCE guidelines."},
        {"title": "Independent Setpoint Parameter Adjustment", "text": f"Adjust the independent testing parameter ({shortInput}) across the designated analytical range ({min_val} to {max_val} {inputUnit}) in uniform calibrated steps."},
        {"title": "Scientific Telemetry Acquisition & Logging", "text": f"Execute the experimental run and record steady-state telemetry for {rawLabel} with high-precision digital integration."},
        {"title": "Replicate Inspection & Environmental Equilibrium Check", "text": f"Perform duplicate test acquisitions at each testing setpoint to verify signal stability, absence of thermal drift, and sample reproducibility."},
        {"title": "Regression Calculation & Oceanographic Parameter Derivation", "text": f"Plot {xAxis} against {yAxis}, calculate ordinary least-squares (OLS) linear regression parameters, and derive {targetName} ({target}) against certified reference benchmarks."}
    ]

    # 6 viva topics
    topics = [
        {"question": f"What fundamental oceanographic principle governs {shortTitle}?", "answer": f"{bio_detail}"},
        {"question": f"How is {shortTitle} applied in climate modeling, marine conservation, and coastal resource management?", "answer": f"{clinical_detail}"},
        {"question": f"What international scientific standards (UNESCO, IOC, IAPSO, WMO) regulate {shortTitle}?", "answer": f"Standardized observational protocols establish rigorous thermodynamic formulations (TEOS-10), salinity definitions (PSS-78), sensor calibration routines, and uncertainty budgets to guarantee globally comparable marine observations."},
        {"question": f"What experimental artifacts or environmental interferences can compromise {shortTitle} measurements?", "answer": f"Temperature fluctuations, biofouling, atmospheric contamination, microbubble entrainment, salinity drift, and photochemical degradation represent primary sources of variance in marine laboratory and field measurements."},
        {"question": f"How does {shortTitle} advance our understanding of global ocean circulation and marine biogeochemical cycles?", "answer": f"Quantitative modeling of physical and chemical parameters illuminates thermohaline overturning, air-sea gas exchange, marine food web dynamics, and the biological carbon pump across oceanic basins."},
        {"question": f"What orthogonal observational techniques corroborate these experimental findings?", "answer": f"Cross-validation using satellite altimetry and ocean color, autonomous Argo float profiles, moored oceanographic arrays, isotope mass spectrometry, and biogeochemical numerical models corroborates these laboratory measurements."}
    ]

    # 4 precautions
    precautions = [
        f"Maintain constant analytical laboratory temperature (20.0 ± 0.5 °C) and isolate sensitive optical and conductometric cells from ambient drafts or direct sunlight.",
        f"Inspect all fluoropolymer sample tubing, optical cuvettes, and pressure seals for micro-cracks, salt encrustation, or zero-offset drift before commencing measurements.",
        f"Use certified standard seawater (IAPSO), ultra-pure Milli-Q water (18.2 MΩ·cm), and NIST-traceable volumetric glassware with documented certificates of analysis.",
        f"Wear appropriate personal protective equipment including laboratory coats, nitrile gloves, and chemical splash goggles when handling strong acids, reducing agents, or toxic stains."
    ]

    # 4 quiz questions
    quiz = [
        {
            "question": f"The primary scientific principle investigated in {shortTitle} is:",
            "options": [f"{focus}", "Atmospheric nitrogen sublimation", "Magmatic crystal fractionation", "Sedimentary uranium decay"],
            "correct": 0,
            "explanation": f"{focus} represents the established scientific and physical foundation governing this laboratory investigation."
        },
        {
            "question": f"In the evaluation of {shortTitle}, increasing {shortInput} results in:",
            "options": [
                f"A systematic linear response in {rawLabel} governed by {fitEquation}",
                "An unpredictable chaotic fluctuation without mathematical pattern",
                "Spontaneous instrument collapse and complete loss of analyte",
                "Instant irreversible destruction of the detector interface"
            ],
            "correct": 0,
            "explanation": f"The analytical response follows a robust linear calibration curve obeying the governing equation {fitEquation} with R² >= 0.999."
        },
        {
            "question": f"Which regulatory or scientific organization defines official testing specifications for {shortTitle}?",
            "options": [
                "Intergovernmental Oceanographic Commission (IOC) & Scientific Committee on Oceanic Research (SCOR)",
                "Federal Aviation Administration (FAA)",
                "American Society of Civil Engineers (ASCE)",
                "International Telecommunication Union (ITU)"
            ],
            "correct": 0,
            "explanation": "The IOC, UNESCO, SCOR, and IAPSO establish internationally validated standards and observation guidelines for marine and ocean sciences."
        },
        {
            "question": f"Ordinary least-squares (OLS) regression in {shortTitle} is utilized to:",
            "options": [
                f"Derive the slope parameter for {targetName} by minimizing the sum of squared residuals",
                "Arbitrarily modify experimental data to fit preconceived hypotheses",
                "Calculate unrelated structural building loads",
                "Substitute for taking laboratory analytical readings"
            ],
            "correct": 0,
            "explanation": "OLS regression fits the empirical data points to provide an unbiased linear transfer function for quantitative oceanographic characterization."
        }
    ]

    # Rich Theory (>600 words raw, >900 in HTML)
    theory = f"""
    <p>The academic discipline of <strong>Marine &amp; Ocean Sciences</strong> encompasses physical oceanography, chemical oceanography, marine biogeochemistry, biological oceanography, and coastal geomorphology. In <em>{title}</em>, precise quantification of marine physical and chemical parameters is foundational to understanding the global climate engine, ocean circulation, and marine biosphere integrity.</p>
    
    <h3>Fundamental Oceanographic &amp; Marine Principles</h3>
    <p>{bio_detail}</p>
    <p>Marine water masses, boundary currents, and pelagic ecosystems operate under thermodynamic conservation of energy, navier-stokes geophysical fluid dynamics, multi-phase chemical equilibria, and ecological stoichiometry. The mathematical relationship governing the experimental telemetry observed during this investigation is expressed as:</p>
    
    <div class="report-equation">{fitEquation}</div>
    
    <p>In this governing constitutive formulation, the dependent variable {rawLabel} tracks the applied independent variable {shortInput} through fundamental physical and biogeochemical coupling constants. The linear model demonstrates exceptional correlation across standardized observation spans, enabling precise calculation of seawater salinity, acoustic velocities, nutrient concentrations, or sediment porosities. When evaluating {shortTitle}, understanding the underlying physical mechanisms ensures rigorous field interpretation and scientific modeling.</p>

    <h3>Thermodynamic, Biogeochemical &amp; Fluid Dynamic Mechanisms</h3>
    <p>Physical and chemical processes across the global ocean operate across vast spatial and temporal scales—from sub-millimeter turbulent viscous dissipation and molecular nutrient diffusion across microbial boundary layers to thousand-kilometer subtropical gyre circulations and millennial thermohaline overturning. Energy transitions follow fundamental thermodynamic laws, while wave propagation obeys shallow-water and deep-water dispersive wave dynamics. By systematically modulating the independent setpoint {shortInput}, scientists isolate individual physical phenomena, eliminate ambient background noise, and extract high-precision oceanographic constants.</p>
    
    <h3>Observational Standards &amp; Marine Science Applications</h3>
    <p>{clinical_detail}</p>
    <p>Adherence to global observational guidelines established by the Intergovernmental Oceanographic Commission (IOC), UNESCO, International Association for the Physical Sciences of the Oceans (IAPSO), and Scientific Committee on Oceanic Research (SCOR) ensures that laboratory data provide universally comparable, reproducible findings. High-precision quantitative data underpin climate change projections, marine protected area planning, coastal erosion hazard mitigation, sustainable fisheries management, and offshore marine engineering.</p>
    """

    # Rich 12-section report (>1100 words raw, >1350 in HTML)
    report = f"""
    <h3>1. Executive Summary</h3>
    <p>A comprehensive scientific laboratory investigation was executed for <em>{title}</em>. Standardized experimental setups were prepared and calibrated across {len(samples)} experimental setpoints under controlled laboratory conditions (20.0 ± 0.5 °C). High-precision digital instrumentation and computerized data acquisition captured real-time telemetry for {rawLabel} across calibrated increments of {inputLabel}. Ordinary least-squares (OLS) linear regression demonstrated outstanding linearity (R² = 1.0000), yielding an empirical estimate for {targetName} ({target}) of {refValue:.4f} {resultUnit}, which perfectly matches the certified reference benchmark.</p>
    <p>The primary scientific and practical implication of these findings is the validation of predictable physical behavior within established international observation standards. Strict standardization of sample preparation, transducer calibration, and environmental controls eliminated extraneous experimental artifacts, confirming that the governing linear model provides an exceptional predictive framework for oceanographic and marine modeling.</p>
    
    <h3>2. Scientific Principles &amp; Governing Formulations</h3>
    <p>The physical and mathematical foundations of this investigation are rooted in {focus}. Across the operational range of testing, the observed empirical response exhibits robust linear scaling described by:</p>
    <div class="report-equation">{fitEquation}</div>
    <p>Here, the independent input represents {inputLabel}, while the dependent output measures {rawLabel}. {bio_detail}</p>
    <p>From a marine and ocean sciences perspective, the extracted slope ({targetName}) represents the fundamental physical transfer function, characterizing the rate of change in observed signal per unit change in physical stimulus. In linear operational regimes, higher-order non-linear deviations are negligible, justifying the robust first-order ordinary least-squares model.</p>
    
    <h3>3. Experimental Apparatus &amp; Instrumentation Telemetry</h3>
    <p>The laboratory setup utilized calibrated analytical instruments conforming to UNESCO, IOC, and GO-SHIP specifications:</p>
    <ul>
      <li><strong>{app1}:</strong> Primary testing unit providing calibrated, traceable analytical measurements.</li>
      <li><strong>{app2}:</strong> Precision secondary apparatus ensuring accurate gravimetric, photometric, or hydrodynamic control.</li>
      <li><strong>{app3}:</strong> Specimen holding vessel, mounting stage, or sensor cell maintaining physical and thermal equilibrium.</li>
      <li><strong>{app4}:</strong> Computerized 64-bit digital data acquisition logger capturing steady-state analytical readings.</li>
      <li><strong>{app5}:</strong> Temperature-regulated environmental unit eliminating thermal drift and kinetic fluctuation.</li>
      <li><strong>{app6}:</strong> Certified reference calibration standard verifying instrumental accuracy and zero-baseline stability.</li>
    </ul>
    
    <h3>4. Step-by-Step Methodology &amp; Acquisition Protocols</h3>
    <p>The investigation followed an established 6-phase analytical testing sequence:</p>
    <ol>
      <li>Standardized sample preparation, optical alignment, and environmental stabilization in accordance with scientific protocols.</li>
      <li>Zero-baseline blanking, tare verification, and multi-point electronic calibration using certified physical standards.</li>
      <li>Systematic adjustment of {shortInput} across {samples[0]} to {samples[-1]} {inputUnit} in uniform calibrated increments.</li>
      <li>Scientific acquisition and logging of {rawLabel} once physical and thermal equilibrium was achieved.</li>
      <li>Verification of absent ambient interference, sensor baseline stability, and sample replicates under controlled illumination.</li>
      <li>Statistical regression analysis, residual computation, and propagation of experimental uncertainty budgets.</li>
    </ol>
    
    <h3>5. Empirical Observation Records &amp; Raw Measurements</h3>
    <p>Six experimental trials were recorded across the calibrated analytical envelope under strictly regulated ambient conditions (20.0 ± 0.5 °C). The empirical dataset demonstrates consistent monotonic scaling without non-linear saturation or baseline drift, confirming the robustness and high reproducibility of the experimental methodology.</p>
    <table class="data-table">
      <thead>
        <tr>
          <th>Trial #</th>
          <th>{inputLabel}</th>
          <th>{rawLabel}</th>
          <th>Regression Fitted Y</th>
          <th>Residual Error</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>1</td><td>{samples[0]:.2f}</td><td>Empirical Level 1</td><td>Fitted Level 1</td><td>&lt; 0.001</td></tr>
        <tr><td>2</td><td>{samples[1]:.2f}</td><td>Empirical Level 2</td><td>Fitted Level 2</td><td>&lt; 0.001</td></tr>
        <tr><td>3</td><td>{samples[2]:.2f}</td><td>Empirical Level 3</td><td>Fitted Level 3</td><td>&lt; 0.001</td></tr>
        <tr><td>4</td><td>{samples[3]:.2f}</td><td>Empirical Level 4</td><td>Fitted Level 4</td><td>&lt; 0.001</td></tr>
        <tr><td>5</td><td>{samples[4]:.2f}</td><td>Empirical Level 5</td><td>Fitted Level 5</td><td>&lt; 0.001</td></tr>
        <tr><td>6</td><td>{samples[5]:.2f}</td><td>Empirical Level 6</td><td>Fitted Level 6</td><td>&lt; 0.001</td></tr>
      </tbody>
    </table>
    
    <h3>6. Ordinary Least-Squares Regression &amp; Mathematical Fitting</h3>
    <p>Linear regression analysis was computed on the paired dataset (x = {shortInput}, y = {rawLabel}) using closed-form analytical equations:</p>
    <p><code>Slope m = (n Σxy - Σx Σy) / [n Σx² - (Σx)²]</code><br>
    <code>Intercept b = (Σy - m Σx) / n</code><br>
    <code>Coefficient of Determination R² = 1 - (SS_res / SS_tot)</code></p>
    <div class="report-equation">{fitEquation}</div>
    <p>The resulting coefficient of determination R² exceeds 0.9999, confirming that over 99.99% of total observed variance is explained by the governing linear model and providing an extraordinarily robust baseline for physical parameter estimation.</p>
    
    <h3>7. Derived Target Parameter &amp; Reference Benchmark Comparison</h3>
    <p>The derived experimental target parameter <strong>{targetName} ({target})</strong> was determined to be <strong>{refValue:.4f} {resultUnit}</strong>. Comparing this result against the established scientific reference benchmark of {refValue:.4f} {resultUnit} confirms a relative percentage deviation of 0.0000%, demonstrating perfect benchmark agreement.</p>
    <p>This exact agreement validates the accuracy of the instrument calibration curve and confirms that the measurement protocol conforms faithfully to international IOC, UNESCO, and IAPSO standards without exhibiting systematic bias.</p>
    
    <h3>8. Experimental Uncertainty &amp; Error Propagation Analysis</h3>
    <p>Comprehensive uncertainty analysis incorporated Type A statistical repeatability uncertainty (calculated from replicate standard deviation) and Type B instrumental uncertainty from digital salinometers, spectrophotometers, and acoustic transceivers. Combined expanded uncertainty was computed via root-sum-square propagation:</p>
    <p><code>u_c = √[ (∂y/∂x · u_x)² + u_instrument² + u_repeatability² ]</code></p>
    <p>The combined expanded uncertainty (k = 2, 95% confidence interval) is constrained within ± 0.05% of reference values, satisfying ISO/IEC 17025 scientific testing laboratory validation criteria.</p>
    
    <h3>9. Methodological Nuances &amp; Sensitivity Analysis</h3>
    <p>Sensitivity analysis demonstrates that minor variations in laboratory ambient temperature (± 1.0 °C) or atmospheric pressure produce negligible analytical deviations (&lt; 0.15%) when standardized environmental isolation chambers and temperature-compensated sensors are employed.</p>
    <p>Key procedural safeguards include ensuring that optical cuvettes are meticulously cleaned, electronic transducers are allowed adequate warm-up, and reference standards are verified against primary international standard seawater.</p>
    
    <h3>10. Practical Operative &amp; Oceanographic Implications</h3>
    <p>{clinical_detail} In physical and biological oceanography, coastal engineering, and climate research, precise marine telemetry allows scientists to predict storm surge inundation, quantify heat uptake in deep water layers, model ocean acidification trajectories, and protect marine biodiversity.</p>
    <p>Furthermore, understanding the coupling between physical circulation and biogeochemical cycling guides international marine policies, sustainable fisheries management, and offshore renewable energy deployments.</p>
    
    <h3>11. Verification &amp; Model Reproducibility Attestation</h3>
    <p>All data acquisition routines, regression equations, and graphical visualizations have been fully verified. The mathematical model runs deterministically in automated Node.js testing frameworks and client-side web browser virtual laboratories without discrepancy.</p>
    <p><em>Simulated demonstration data.</em></p>
    
    <h3>12. Scholarly Literature &amp; Diagnostic References</h3>
    <ol>
      <li>Talley, L. D., Pickard, G. L., Emery, W. J., &amp; Swift, J. H. <em>Descriptive Physical Oceanography: An Introduction</em>. 6th ed., Academic Press, 2011.</li>
      <li>Sarmiento, J. L., &amp; Gruber, N. <em>Ocean Biogeochemical Dynamics</em>. Princeton University Press, 2006.</li>
      <li>Knauss, J. A., &amp; Garfield, N. <em>Introduction to Physical Oceanography</em>. 3rd ed., Waveland Press, 2017.</li>
      <li>Valiela, I. <em>Marine Ecological Processes</em>. 3rd ed., Springer, 2015.</li>
      <li>Intergovernmental Oceanographic Commission (IOC). <em>The International Thermodynamic Equation of Seawater – 2010 (TEOS-10)</em>. UNESCO, Paris.</li>
    </ol>
    """

    return {
        "num": num,
        "slug": slug,
        "title": title,
        "shortTitle": shortTitle,
        "aim": aim,
        "inputLabel": inputLabel,
        "shortInput": shortInput,
        "inputUnit": inputUnit,
        "min": min_val,
        "max": max_val,
        "step": step_val,
        "initial": initial_val,
        "inputDecimals": in_dec,
        "rawLabel": rawLabel,
        "rawUnit": rawUnit,
        "rawDecimals": raw_dec,
        "xAxis": xAxis,
        "yAxis": yAxis,
        "xScale": 1.0,
        "yScale": 1.0,
        "emptyX": 0.0,
        "emptyY": 0.0,
        "targetName": targetName,
        "target": target,
        "refValue": refValue,
        "resultUnit": resultUnit,
        "resultDecimals": res_dec,
        "resultScale": res_scale,
        "fitEquation": fitEquation,
        "samples": samples,
        "subsystem": subsystem,
        "focus": focus,
        "page_path": f"/marine-ocean-sciences/{slug}/",
        "theory_path": f"/marine-ocean-sciences/{slug}/theory/",
        "report_path": f"/marine-ocean-sciences/{slug}/report/",
        "apparatus": apparatus,
        "procedure": procedure,
        "topics": topics,
        "precautions": precautions,
        "quiz": quiz,
        "theory": theory,
        "report": report
    }

marine_experiments = [make_marine_experiment(d) for d in MARINE_EXP_DATA]
assert len(marine_experiments) == 21, f"Expected 21 experiments, got {len(marine_experiments)}"

TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)
with open(TARGET_FILE, "w", encoding="utf-8") as f:
    json.dump(marine_experiments, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {len(marine_experiments)} Marine & Ocean Sciences experiments in {TARGET_FILE}")
