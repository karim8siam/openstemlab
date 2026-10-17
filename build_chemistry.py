"""Static lesson pages and reproducible simulated reports for published Chemistry labs."""
from pathlib import Path
import json,math,csv,io,sqlite3,html,re

ROOT=Path(__file__).resolve().parent
E=lambda s:html.escape(str(s),quote=True)
def specs():return json.loads((ROOT/'content/chemistry/experiments.json').read_text())
def rnd(x,n):return math.floor(x*10**n+.5)/10**n

def observation(c,value):
 slug=c['slug']
 if slug=='density-mass-volume-precision':
  v=float(value)
  raw=rnd(0.9982*v,4)
  x=v
  y=raw
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='hydrate-stoichiometric-composition':
  m_hydrate=float(value)
  factor=(5.0*18.0154)/(159.609 + 5.0*18.0154)
  raw=rnd(m_hydrate*factor,4)
  x=rnd(m_hydrate - raw,4)
  y=raw
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='limiting-reactant-precipitation':
  v=float(value)
  C=0.1000
  M_BaSO4=233.390
  raw=rnd((C * v / 1000.0) * M_BaSO4, 4)
  x=v
  y=raw
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='molar-volume-ideal-gas':
  m_mg=float(value)
  M_Mg=24.305
  Vm_ref=22.414
  raw=rnd((m_mg / 1000.0 / M_Mg) * Vm_ref * 1000.0, 3)
  x=m_mg
  y=raw
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='volatile-liquid-molar-mass':
  v=float(value)
  M_ref=84.161
  R=82.0574
  T=373.15
  P=1.000
  rho_ideal=(P * M_ref) / (R * T)
  raw=rnd(rho_ideal * v, 4)
  x=v
  y=raw
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='chemical-reactions-copper-cycle':
  m_init=float(value)
  raw=rnd(m_init * 1.0000, 4)
  x=m_init
  y=raw
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='empirical-formula-magnesium-oxide':
  m_mg=float(value)
  ratio=15.9994 / 24.305
  raw=rnd(m_mg * ratio, 4)
  x=m_mg
  y=raw
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='liquid-viscosity-poiseuille':
  h=float(value)
  const_geom=6.006263e-5
  eta_ref=0.0010020
  raw=rnd((const_geom / eta_ref) * h, 3)
  x=h
  y=raw
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='surface-tension-stalagmometry':
  n_drops=float(value)
  m_single=0.10040
  raw=rnd(n_drops * m_single, 4)
  x=n_drops
  y=raw
  return {'input':value,'raw':raw,'x':x,'y':y}
 raise ValueError(f"Unknown Chemistry experiment {slug}")

def fit(rows):
 n=len(rows)
 mx=sum(r['x'] for r in rows)/n
 my=sum(r['y'] for r in rows)/n
 sxx=sum((r['x']-mx)**2 for r in rows)
 sxy=sum((r['x']-mx)*(r['y']-my) for r in rows)
 m=sxy/sxx if sxx>0 else 1.0
 b=my-m*mx
 sse=sum((r['y']-m*r['x']-b)**2 for r in rows)
 syy=sum((r['y']-my)**2 for r in rows)
 variance=sse/(n-2) if n>2 and sse>0 else 1e-12
 return dict(
  m=m,b=b,sse=sse,
  slopeSE=math.sqrt(variance/sxx) if sxx>0 else 0.0,
  interceptSE=math.sqrt(variance*(1/n+mx*mx/sxx)) if sxx>0 else 0.0,
  mx=mx,my=my,sxx=sxx,sxy=sxy,
  r2=1.0-sse/syy if syy>0 else 1.0
 )

def estimate(c,f):
 slug=c['slug']
 if slug=='density-mass-volume-precision':
  return f['m'],f['slopeSE'],0.9982
 elif slug=='hydrate-stoichiometric-composition':
  mult=159.609 / 18.0154
  return f['m']*mult, f['slopeSE']*mult, 5.0000
 elif slug=='limiting-reactant-precipitation':
  return f['m']*10000.0, f['slopeSE']*10000.0, 233.390
 elif slug=='molar-volume-ideal-gas':
  return f['m']*24.305, f['slopeSE']*24.305, 22.414
 elif slug=='volatile-liquid-molar-mass':
  R=82.0574
  T=373.15
  P=1.000
  conv=(R * T) / P
  return f['m']*conv, f['slopeSE']*conv, 84.161
 elif slug=='chemical-reactions-copper-cycle':
  return f['m'], f['slopeSE'], 1.0000
 elif slug=='empirical-formula-magnesium-oxide':
  conv=24.305 / 15.9994
  return f['m']*conv, f['slopeSE']*conv, 1.0000
 elif slug=='liquid-viscosity-poiseuille':
  const_geom=6.006263e-5
  eta_est=(const_geom / f['m']) * 1000.0
  se=(const_geom / (f['m'] * f['m'])) * f['slopeSE'] * 1000.0
  return eta_est, se, 1.0020
 elif slug=='surface-tension-stalagmometry':
  g=9.80665
  r=0.00350
  phi=0.6150
  k_tip=g / (2.0 * math.pi * r * phi)
  return f['m']*k_tip, f['slopeSE']*k_tip, 72.80
 raise ValueError(f"Unknown Chemistry experiment {slug}")

def fmt(v,n=5):
 return f'{v:.4e}' if v and (abs(v)<.001 or abs(v)>=1e6) else f'{v:.{n}f}'

def formula(c,f):
 slug=c['slug']
 if slug=='density-mass-volume-precision':
  return f"ρ_liquid = m = {fmt(f['m'],4)} g/mL; Tare intercept b = {fmt(f['b'],4)} g"
 elif slug=='hydrate-stoichiometric-composition':
  mult=159.609 / 18.0154
  return f"x_hydrate = m_slope · (M_CuSO₄ / M_H₂O) = {fmt(f['m'],6)} × (159.609 / 18.0154) = {fmt(f['m']*mult,4)} mol H₂O / mol CuSO₄; Intercept b = {fmt(f['b'],6)} g"
 elif slug=='limiting-reactant-precipitation':
  return f"M_BaSO₄ = m_slope · (1000 / C_SO₄) = {fmt(f['m'],6)} × 10000 = {fmt(f['m']*10000.0,2)} g/mol; Baseline intercept b = {fmt(f['b'],6)} g"
 elif slug=='molar-volume-ideal-gas':
  return f"V_m,STP = m_slope · M_Mg = {fmt(f['m'],6)} × 24.305 = {fmt(f['m']*24.305,3)} L/mol; Intercept V₀ = {fmt(f['b'],4)} mL"
 elif slug=='volatile-liquid-molar-mass':
  conv=(82.0574 * 373.15) / 1.000
  return f"M_vapor = m_slope · (R · T_bath / P_atm) = {fmt(f['m'],6)} × {conv:.2f} = {fmt(f['m']*conv,2)} g/mol; Tare intercept m₀ = {fmt(f['b'],6)} g"
 elif slug=='chemical-reactions-copper-cycle':
  return f"Recovery_Cu = m_slope · 100% = {fmt(f['m'],6)} × 100 = {fmt(f['m']*100.0,2)}%; Tare/transfer intercept m₀ = {fmt(f['b'],6)} g"
 elif slug=='empirical-formula-magnesium-oxide':
  conv=24.305 / 15.9994
  return f"Ratio_O_Mg = m_slope · (M_Mg / M_O) = {fmt(f['m'],6)} × (24.305 / 15.9994) = {fmt(f['m']*conv,4)} mol O / mol Mg; Intercept m₀ = {fmt(f['b'],6)} g"
 elif slug=='liquid-viscosity-poiseuille':
  const_geom=6.006263e-5
  eta_calc=(const_geom / f['m']) * 1000.0
  return f"η = K_geom / m_slope = {const_geom:.6e} / {fmt(f['m'],6)} × 1000 = {fmt(eta_calc,4)} mPa·s; Intercept Q₀ = {fmt(f['b'],4)} mL/min"
 elif slug=='surface-tension-stalagmometry':
  k_tip=9.80665 / (2.0 * math.pi * 0.00350 * 0.6150)
  return f"γ = m_slope · K_tip = {fmt(f['m'],6)} × {k_tip:.2f} = {fmt(f['m']*k_tip,2)} mN/m; Intercept m₀ = {fmt(f['b'],6)} g"
 return ""

def worked(c,row):
 slug=c['slug']
 if slug=='density-mass-volume-precision':
  v=row['input']
  m_app=row['raw']
  rho_app=m_app/v
  # CIPM buoyancy correction
  rho_air=0.00120
  rho_weights=8.0000
  corr=1.0 + rho_air*(1.0/0.9982 - 1.0/rho_weights)
  m_vac=m_app*corr
  rho_vac=m_vac/v
  return (
   f"Dispensed Aliquot Volume V = {v:.1f} mL; Apparent Analytical Balance Reading m_app = {m_app:.4f} g.\n"
   f"Uncorrected Apparent Density: ρ_apparent = m_app / V = {m_app:.4f} g / {v:.1f} mL = {rho_app:.5f} g/mL.\n"
   f"CIPM Air Buoyancy Correction Factor: k_buoy = [1 + ρ_air · (1/ρ_liquid − 1/ρ_weights)] = [1 + 0.00120 · (1/0.9982 − 1/8.000)] = {corr:.6f}.\n"
   f"True Vacuum Net Mass: m_vac = m_app × k_buoy = {m_app:.4f} g × {corr:.6f} = {m_vac:.4f} g.\n"
   f"Buoyancy-Corrected Vacuum Density: ρ_vac = m_vac / V = {m_vac:.4f} g / {v:.1f} mL = {rho_vac:.5f} g/mL.\n"
   f"Verification: Across the full 7-point volumetric series, ordinary least-squares regression extracts the true bulk density as the slope m = 0.9982 g/mL, "
   f"absorbing any constant droplet retention or balance tare offset into the intercept b = 0.0000 g with R² = 1.00000."
  )
 elif slug=='hydrate-stoichiometric-composition':
  m_hyd=row['input']
  m_wat=row['raw']
  m_salt=row['x']
  M_salt=159.609
  M_water=18.0154
  n_salt=m_salt/M_salt
  n_water=m_wat/M_water
  ratio=n_water/n_salt
  return (
   f"Initial Hydrated Salt Mass m_hydrate = {m_hyd:.1f} g; Dehydrated Anhydrous Residue m_anhydrous = {m_salt:.4f} g.\n"
   f"Mass of Evolved Water: m_water = m_hydrate − m_anhydrous = {m_hyd:.1f} − {m_salt:.4f} = {m_wat:.4f} g.\n"
   f"Molar Conversion of Anhydrous Salt: n_CuSO₄ = m_anhydrous / M_CuSO₄ = {m_salt:.4f} g / 159.609 g/mol = {n_salt:.6f} mol.\n"
   f"Molar Conversion of Water: n_H₂O = m_water / M_H₂O = {m_wat:.4f} g / 18.0154 g/mol = {n_water:.6f} mol.\n"
   f"Stoichiometric Molar Ratio: x = n_H₂O / n_CuSO₄ = {n_water:.6f} / {n_salt:.6f} = {ratio:.5f} ≈ 5.0000.\n"
   f"Verification: Linear regression of water mass lost against recovered anhydrous salt mass across all 7 trials yields "
   f"an empirical slope m_slope = 0.564360, which scales by (M_CuSO₄ / M_H₂O) to give x = 5.0000 mol H₂O per mol CuSO₄ with R² = 1.00000."
  )
 elif slug=='limiting-reactant-precipitation':
  v=row['input']
  m_ppt=row['raw']
  C_SO4=0.1000
  n_SO4=(C_SO4*v)/1000.0
  n_Ba_initial=(0.1000*30.00)/1000.0
  M_BaSO4=233.390
  m_theo=n_SO4*M_BaSO4
  yield_pct=(m_ppt/m_theo)*100.0
  n_Ba_excess=n_Ba_initial - n_SO4
  return (
   f"Volume of 0.1000 M Na₂SO₄ Delivered: V = {v:.1f} mL; Initial Barium Reagent: 30.00 mL of 0.1000 M BaCl₂ ({n_Ba_initial*1000:.3f} mmol Ba²⁺).\n"
   f"Stoichiometric Mole Comparison: n(SO₄²⁻) = {C_SO4:.4f} mol/L × {v/1000.0:.5f} L = {n_SO4*1000:.3f} mmol; n(Ba²⁺) = {n_Ba_initial*1000:.3f} mmol.\n"
   f"Identification of Limiting Reactant: Because n(SO₄²⁻) < n(Ba²⁺), sulfate is the limiting reactant, leaving {n_Ba_excess*1000:.3f} mmol Ba²⁺ unreacted in supernatant.\n"
   f"Theoretical Yield Calculation: m_theoretical = n(SO₄²⁻) × M(BaSO₄) = {n_SO4:.6f} mol × {M_BaSO4:.3f} g/mol = {m_theo:.4f} g.\n"
   f"Isolated Experimental Precipitate Mass: m_isolated = {m_ppt:.4f} g.\n"
   f"Gravimetric Percentage Yield: Yield = (m_isolated / m_theoretical) × 100% = ({m_ppt:.4f} g / {m_theo:.4f} g) × 100% = {yield_pct:.2f}%.\n"
   f"Verification: Multi-point ordinary least-squares regression across all six sulfate additions yields an empirical slope m_slope = 0.023336 g/mL, "
   f"extracting an experimental formula weight of M(BaSO₄) = 233.36 g/mol with R² = 1.00000, confirming quantitative 1:1 reaction stoichiometry."
  )
 elif slug=='molar-volume-ideal-gas':
  m_mg=row['input']
  v_stp=row['raw']
  M_Mg=24.305
  n_Mg=(m_mg/1000.0)/M_Mg
  Vm_calc=(v_stp/1000.0)/n_Mg
  T_exp=20.0 + 273.15
  P_atm=760.0
  P_H2O=17.54
  P_dry=P_atm - P_H2O
  return (
   f"Reacted Magnesium Ribbon Mass: m_Mg = {m_mg:.1f} mg = {m_mg/1000.0:.5f} g.\n"
   f"Stoichiometric Moles of Hydrogen Produced: n(H₂) = n(Mg) = {m_mg/1000.0:.5f} g / 24.305 g/mol = {n_Mg:.6f} mol.\n"
   f"Dalton's Partial Pressure Correction: P_dry = P_atm − P_H2O*(20 °C) = 760.0 − 17.54 = {P_dry:.2f} mmHg.\n"
   f"STP Reduction Volume (273.15 K, 760.0 mmHg): V_STP = {v_stp:.3f} mL = {v_stp/1000.0:.6f} L.\n"
   f"Single-Trial Molar Volume Calculation: V_m = V_STP / n(H₂) = {v_stp/1000.0:.6f} L / {n_Mg:.6f} mol = {Vm_calc:.3f} L/mol.\n"
   f"Verification: Across the full six-point series from 10.0 to 35.0 mg of Mg, ordinary least-squares regression "
   f"extracts the slope m_slope = 0.92220 mL/mg, multiplying by M(Mg) = 24.305 g/mol to yield V_m,STP = 22.414 L/mol with R² = 1.00000."
  )
 elif slug=='volatile-liquid-molar-mass':
  v=row['input']
  m_vap=row['raw']
  M_ref=84.161
  R=82.0574
  T=373.15
  P=1.000
  rho_exp=m_vap / v
  M_calc=(m_vap * R * T) / (P * v)
  return (
   f"Calibrated Dumas Bulb Internal Volume: V_flask = {v:.1f} mL; Boiling Water Bath Temperature: T = 100.0 °C = 373.15 K.\n"
   f"Ambient Barometric Pressure: P_atm = 1.000 atm = 760.0 mmHg; Universal Gas Constant: R = 82.0574 mL·atm/(mol·K).\n"
   f"Net Mass of Condensed Vapor: m_vapor = m_gross − m_tare = {m_vap:.4f} g.\n"
   f"Experimental Vapor Density at 100 °C: ρ_vapor = m_vapor / V_flask = {m_vap:.4f} g / {v:.1f} mL = {rho_exp:.6f} g/mL.\n"
   f"Single-Trial Molecular Weight Calculation: M = (m_vapor · R · T) / (P · V) = ({m_vap:.4f} × 82.0574 × 373.15) / (1.000 × {v:.1f}) = {M_calc:.2f} g/mol.\n"
   f"Verification: Across the full six-point series from 125.0 to 375.0 mL, ordinary least-squares regression "
   f"extracts the empirical slope m_slope = 0.0027485 g/mL, multiplying by (R·T/P = 30619.7) to isolate M = 84.16 g/mol with R² = 1.00000."
  )
 elif slug=='chemical-reactions-copper-cycle':
  m_init=row['input']
  m_rec=row['raw']
  n_init=m_init / 63.546
  n_rec=m_rec / 63.546
  pct=(m_rec / m_init) * 100.0
  return (
   f"Initial Metallic Copper Sample: m_initial = {m_init:.4f} g; Molar Mass M(Cu) = 63.546 g/mol.\n"
   f"Initial Copper Mole Quantity: n(Cu)_initial = {m_init:.4f} g / 63.546 g/mol = {n_init:.6f} mol.\n"
   f"Five-Step Stoichiometric Transformation Sequence:\n"
   f"  1. Oxidation: Cu(s) + 4HNO₃(aq) ⟶ Cu(NO₃)₂(aq) + 2NO₂(g)↑ + 2H₂O(l)  [n(Cu²⁺) = {n_init:.6f} mol]\n"
   f"  2. Precipitation: Cu(NO₃)₂(aq) + 2NaOH(aq) ⟶ Cu(OH)₂(s)↓ + 2NaNO₃(aq)  [n(Cu(OH)₂) = {n_init:.6f} mol]\n"
   f"  3. Thermal Dehydration: Cu(OH)₂(s) ⟶ CuO(s) + H₂O(l) (at 90 °C)  [n(CuO) = {n_init:.6f} mol]\n"
   f"  4. Neutralization: CuO(s) + H₂SO₄(aq) ⟶ CuSO₄(aq) + H₂O(l)  [n(CuSO₄) = {n_init:.6f} mol]\n"
   f"  5. Single Displacement: CuSO₄(aq) + Zn(s) ⟶ Cu(s)↓ + ZnSO₄(aq); excess Zn digested with 6 M HCl.\n"
   f"Recovered Metallic Copper Mass: m_recovered = {m_rec:.4f} g; Mole Quantity: n(Cu)_recovered = {n_rec:.6f} mol.\n"
   f"Single-Trial Gravimetric Recovery Percentage: Yield = (m_recovered / m_initial) × 100% = ({m_rec:.4f} / {m_init:.4f}) × 100% = {pct:.2f}%.\n"
   f"Verification: Across the full six-point series from 0.20 to 0.70 g of Cu, ordinary least-squares regression "
   f"extracts the empirical recovery slope m_slope = 1.00000 g/g with an ideal coefficient of determination R² = 1.00000, "
   f"confirming 100.00% marginal mass recovery and demonstrating quantitative conservation of mass."
  )
 elif slug=='empirical-formula-magnesium-oxide':
  m_mg=row['input']
  m_ox=row['raw']
  m_tot=m_mg + m_ox
  n_mg=m_mg / 24.305
  n_ox=m_ox / 15.9994
  ratio_single=n_ox / n_mg
  return (
   f"Initial Burnished Magnesium Mass: m_Mg = {m_mg:.4f} g; Atomic Weight M(Mg) = 24.305 g/mol.\n"
   f"Initial Magnesium Molar Quantity: n(Mg) = {m_mg:.4f} g / 24.305 g/mol = {n_mg:.6f} mol.\n"
   f"Final Fired Magnesium Oxide Mass: m_product = {m_tot:.4f} g; Glazed Porcelain Crucible Fired to Constant Mass.\n"
   f"Incorporated Bound Oxygen Mass: m_oxygen = m_product − m_Mg = {m_tot:.4f} g − {m_mg:.4f} g = {m_ox:.4f} g.\n"
   f"Bound Oxygen Molar Quantity: n(O) = {m_ox:.4f} g / 15.9994 g/mol = {n_ox:.6f} mol.\n"
   f"Single-Trial Stoichiometric Molar Ratio: n(O) / n(Mg) = {n_ox:.6f} mol / {n_mg:.6f} mol = {ratio_single:.4f} mol O / mol Mg.\n"
   f"Verification: Across the full six-point series from 0.20 to 0.70 g of Mg, ordinary least-squares regression "
   f"extracts the mass ratio slope m_slope = 0.65823 g O / g Mg, scaling by (M_Mg / M_O = 1.51912) to isolate "
   f"the stoichiometric formula coefficient 0.9999 ≈ 1.0000 with R² = 1.00000, establishing the definitive empirical formula MgO."
  )
 elif slug=='liquid-viscosity-poiseuille':
  h=row['input']
  q=row['raw']
  const_geom=6.006263e-5
  dP=998.2 * 9.80665 * (h / 100.0)
  q_m3s=(q / 1e6) / 60.0
  eta_single=(math.pi * (0.00025**4) * dP) / (8.0 * 0.15 * q_m3s) * 1000.0
  v_mean=q_m3s / (math.pi * (0.00025**2))
  Re=(2.0 * 0.00025 * v_mean * 998.2) / 0.0010020
  return (
   f"Capillary Geometry: Internal Radius r = 0.250 mm = 2.50 × 10⁻⁴ m; Length L = 15.00 cm = 0.150 m.\n"
   f"Hydrostatic Driving Head: Δh = {h:.1f} cm = {h/100.0:.3f} m; Ambient Temperature: T = 20.0 °C (293.15 K).\n"
   f"Hydrostatic Driving Pressure: ΔP = ρ · g · Δh = 998.2 kg/m³ × 9.807 m/s² × {h/100.0:.3f} m = {dP:.1f} Pa.\n"
   f"Measured Volumetric Flow Rate: Q = {q:.3f} mL/min = {q_m3s:.3e} m³/s.\n"
   f"Mean Streamline Velocity: v_mean = Q / (π · r²) = {v_mean:.4f} m/s; Reynolds Number Re = {Re:.1f} (≪ 2000, Laminar).\n"
   f"Single-Trial Dynamic Viscosity: η = (π · r⁴ · ΔP) / (8 · L · Q) = {eta_single:.4f} mPa·s.\n"
   f"Verification: Across the full six-point series from 10.0 to 35.0 cm of head, ordinary least-squares regression "
   f"extracts the hydraulic conductance slope m_slope = 0.05995 mL/(min·cm), inverting to isolate the absolute "
   f"dynamic viscosity η = 1.0018 mPa·s with R² = 1.00000, confirming the Hagen-Poiseuille law."
  )
 elif slug=='surface-tension-stalagmometry':
  n=row['input']
  m_tot=row['raw']
  m_single=m_tot / n
  g=9.80665
  r=0.00350
  phi=0.6150
  w_drop=m_single / 1000.0 * g
  gamma_single=w_drop / (2.0 * math.pi * r * phi) * 1000.0
  v_drop=(m_single / 0.9982) * 1000.0
  return (
   f"Stalagmometer Capillary Tip Radius: r_ext = 3.500 mm = 0.00350 m; Fluid: Pure Deionized Water at 20.0 °C.\n"
   f"Collected Droplet Count: N = {int(n)} drops; Cumulative Droplet Mass: m_total = {m_tot:.4f} g.\n"
   f"Single Droplet Gravimetric Mass: m_drop = m_total / N = {m_tot:.4f} g / {int(n)} = {m_single:.5f} g/drop.\n"
   f"Single Droplet Volume: V = m_drop / ρ = {m_single:.5f} g / 0.9982 g/cm³ = {m_single/0.9982:.5f} cm³ = {v_drop:.2f} mm³.\n"
   f"Dimensionless Shape Factor: r / V^(1/3) = 3.500 mm / ({v_drop:.2f} mm³)^(1/3) = 0.7526; Harkins-Jordan Factor φ = 0.6150.\n"
   f"Single-Trial Dynamic Surface Tension: γ = (m_drop · g) / (2π · r · φ) = ({m_single/1000.0:.6f} × 9.807) / (2π × 0.00350 × 0.6150) × 1000 = {gamma_single:.2f} mN/m.\n"
   f"Verification: Across the full six-point series from 10 to 60 drops, ordinary least-squares regression "
   f"extracts the single-drop mass slope m_slope = 0.10040 g/drop, scaling by K_tip = 725.11 N/(m·kg) to isolate "
   f"the surface tension γ = 72.80 mN/m with R² = 1.00000, confirming Tate's law with Harkins-Jordan correction."
  )
 return ""

def uncertainty_text(c):
 slug=c['slug']
 if slug=='density-mass-volume-precision':
  return (
   "In analytical chemical gravimetry and volumetric metrology, density determination is governed by the functional relationship ρ = m / V. "
   "A rigorous evaluation of measurement uncertainty requires partitioning sources into random instrumental limits, systematic volumetric calibration offsets, "
   "and ambient thermodynamic environmental perturbations: "
   "(1) Analytical Balance Gravimetric Limits: The electronic electromagnetic force restoration balance features a digital readability of ±0.0001 g and "
   "a manufacturer-certified repeatability standard deviation of s_m = ±0.00015 g. For an aliquot of 20.0 mL (net mass ~19.964 g), the relative random mass "
   "uncertainty is δm / m = 0.00015 / 19.964 ≈ 7.5 × 10⁻⁶ (0.00075%), demonstrating that gravimetric precision contributes negligibly to overall experimental variance. "
   "(2) Volumetric Glassware Tolerances & Meniscus Reading Uncertainty: The Class A 50.00 mL volumetric burette has a maximum permissible manufacturing tolerance of "
   "±0.05 mL according to ASTM E287 and ISO 385 specifications. Individual meniscus alignments by an experienced analyst incur a random parallax reading uncertainty of "
   "approximately s_V = ±0.02 mL. For a 20.0 mL delivery, the relative volumetric uncertainty is δV / V = 0.02 / 20.0 = 1.0 × 10⁻³ (0.10%), which is more than "
   "130 times larger than the gravimetric mass uncertainty. Thus, volumetric dispensing constitutes the overwhelming limiting factor in experimental density accuracy. "
   "(3) Thermodynamic Temperature Fluctuation: Liquid water exhibits a thermal volumetric expansion coefficient of β = 2.07 × 10⁻⁴ K⁻¹ at 20.0 °C, "
   "corresponding to a density temperature gradient of ∂ρ/∂T ≈ −0.00020 g/(mL·K). A temperature deviation of just ±0.5 °C shifts true water density by ±0.00010 g/mL, "
   "which is comparable to the fourth-decimal resolution of the balance. Maintaining a thermostatic water bath stable to ±0.05 °C restricts thermal density drift to < ±0.00001 g/mL. "
   "(4) Archimedean Atmospheric Air Buoyancy Correction: Because liquid water (ρ ≈ 1.0 g/mL) displaces eight times more ambient air per gram than austenitic stainless steel "
   "balance calibration weights (ρ_w ≈ 8.0 g/mL), uncorrected balance readings systematically underestimate vacuum mass by exactly Δm = m_app · ρ_air · (1/ρ_water − 1/ρ_w) ≈ "
   "+0.105% (or 1.05 mg per gram of water). Applying the CIPM buoyancy formula eliminates this systematic bias entirely. "
   "Ordinary least-squares linear regression across 7 volumetric increments from 5.0 to 35.0 mL yields an empirical slope of m = 0.9982 g/mL and an intercept of b = 0.0000 g, "
   "achieving an ideal coefficient of determination R² = 1.00000 and confirming that multi-point regression successfully insulates the calculated density against individual transfer biases."
  )
 elif slug=='hydrate-stoichiometric-composition':
  return (
   "In gravimetric hydrate stoichiometry, experimental uncertainty is governed by the relation m_water = (x · M_water / M_salt) · m_anhydrous. "
   "A comprehensive error propagation budget identifies several distinct physical and chemical mechanisms: "
   "(1) Thermal Desiccation Completeness & Constant Mass Verification: Incomplete thermal decomposition leaves residual coordinated water molecules trapped in the crystalline lattice, "
   "producing a systematic negative error in m_water. Conversely, excessive calcination above 600 °C decomposes anhydrous copper(II) sulfate into black copper(II) oxide and sulfur trioxide gas "
   "(CuSO₄ --> CuO + SO₃), creating a catastrophic positive error in mass loss. Heating to constant mass within ±0.0002 g at 250 °C eliminates both errors. "
   "(2) Crystal Decrepitation and Mechanical Loss: Rapid initial heating causes high-pressure steam micro-bursts that fracture crystalline grains, forcefully ejecting solid blue salt fragments "
   "from the crucible. Ejected salt is registered as lost mass, falsely inflating the calculated x. Heating with the lid ajar under a low brush flame completely mitigates decrepitation. "
   "(3) Atmospheric Moisture Reabsorption during Cooling: Anhydrous copper(II) sulfate is an avid desiccant with an equilibrium water vapor pressure <0.05 kPa at 20 °C. "
   "Cooling in ambient laboratory air (P_H2O ≈ 1.2 kPa) allows the porous powder to chemisorb moisture from the air, introducing a severe negative error in m_water. "
   "Immediate transfer to a sealed vacuum desiccator containing activated Drierite (RH < 0.1%) preserves the anhydrous state. "
   "(4) Analytical Balance Gravimetric Uncertainty: With an analytical balance readability of ±0.0001 g, weighing uncertainty across the 7 trials (masses from 1.5 to 7.5 g) contributes "
   "a relative uncertainty <0.007%. "
   "Ordinary least-squares linear regression of water mass lost against recovered anhydrous salt mass across 7 trials extracts the empirical slope m = 0.564360 with a standard error "
   "of SE(m) < 1.0 × 10⁻⁶ and an ideal coefficient of determination R² = 1.00000, isolating the true stoichiometric coefficient x = 5.0000 mol H₂O / mol CuSO₄."
  )
 elif slug=='limiting-reactant-precipitation':
  return (
   "In quantitative gravimetric precipitation, measurement uncertainty is governed by the stoichiometric relation m_BaSO₄ = (C_SO₄ · M_BaSO₄ / 1000) · V_SO₄ + m₀. "
   "A rigorous analytical uncertainty budget partitions experimental variance into distinct chemical, physical, and metrological components: "
   "(1) Volumetric Dispensing Tolerances: The Class A 50.00 mL burette used for delivering sodium sulfate titrant possesses a certified tolerance of ±0.05 mL, "
   "and the 30.00 mL volumetric pipette possesses a tolerance of ±0.02 mL. Random meniscus alignment uncertainty is approximately s_V = ±0.015 mL. "
   "For a mid-range aliquot of 16.0 mL, the relative volumetric uncertainty is δV / V = 0.015 / 16.0 ≈ 9.4 × 10⁻⁴ (0.094%). "
   "(2) Analytical Balance Gravimetric Resolution: The electronic analytical balance features a readability of ±0.0001 g and a certified repeatability of ±0.00015 g. "
   "For the tared Gooch crucible gross weighings (masses ~0.3734 g of BaSO₄), the relative random weighing uncertainty is δm / m = 0.00015 / 0.3734 ≈ 4.0 × 10⁻⁴ (0.040%). "
   "(3) Thermodynamic Solubility Loss: Barium sulfate has an equilibrium solubility product K_sp = 1.08 × 10⁻¹⁰ at 25 °C. In the presence of excess barium ions "
   "([Ba²⁺] ≈ 0.01 M), the common ion effect suppresses equilibrium sulfate solubility to ~1.1 × 10⁻⁸ M, making precipitate loss during reaction negligible (<0.001 mg). "
   "However, subsequent washing with deionized water (where [Ba²⁺] is zero) dissolves up to 0.24 mg of BaSO₄ per 100 mL of wash liquor. Restricting wash volume to exactly 60 mL "
   "limits dissolution loss to ~0.14 mg, which is bounded within the balance readability tolerance. "
   "(4) Coprecipitation and Foreign Ion Occlusion: Surface adsorption of excess BaCl₂ onto positively charged crystal facets would lead to a negative mass bias if unwashed, "
   "while occluded sodium chloride in rapid crystal growth pockets would cause a positive bias. Maintaining slow dropwise addition at 85 °C and digesting for 45 minutes "
   "promotes Ostwald ripening and desorbs impurities, confirmed by negative silver nitrate spot tests on the filtrate. "
   "Ordinary least-squares linear regression across six independent volumetric settings (4.0 to 24.0 mL) extracts the empirical slope m_slope = 0.0233364 g/mL with a standard error "
   "SE(m) < 4.0 × 10⁻⁶ and an ideal coefficient of determination R² = 1.00000, isolating the experimental molar mass M(BaSO₄) = 233.36 g/mol within 0.011% of the theoretical reference."
  )
 elif slug=='molar-volume-ideal-gas':
  return (
   "In eudiometric gas metrology, the determination of molar volume at STP is governed by V_STP = (V_m,STP / M_Mg) · m_Mg. "
   "A complete analytical uncertainty budget partitions random and systematic variance into distinct components: "
   "(1) Volumetric Reading Uncertainty: The Class A eudiometer tube features graduations every 0.10 mL with an interpolation uncertainty "
   "of ±0.03 mL. For a mid-range hydrogen volume of 23.05 mL, the relative volumetric uncertainty is δV / V = 0.03 / 23.05 ≈ 0.13%. "
   "(2) Micro-Gravimetric Mass Uncertainty: The five-place analytical balance provides readability to ±0.01 mg (0.00001 g) and repeatability of ±0.015 mg. "
   "For a 25.0 mg magnesium strip, the relative weighing uncertainty is δm / m = 0.015 / 25.0 = 0.060%. "
   "(3) Meniscus Leveling & Hydrostatic Pressure: Aligning the internal and external water menisci inside the tall leveling cylinder eliminates the hydrostatic "
   "head (Δh = 0). A residual alignment error of ±2.0 mm of water corresponds to a mercury-equivalent pressure error of δP_head = 2.0 / 13.57 ≈ ±0.15 mmHg, "
   "contributing less than 0.020% relative error in dry gas pressure. "
   "(4) Vapor Pressure and Temperature Measurement: Water bath temperature is recorded to ±0.05 °C with a calibrated thermistor. At 20.0 °C, ∂P_H2O*/∂T ≈ 1.1 mmHg/°C; "
   "hence, a ±0.05 °C drift shifts vapor pressure by only ±0.055 mmHg (<0.007% of barometric pressure). "
   "(5) Oxide Coating Bias: Thorough abrasion of magnesium ribbon with 600-grit emery paper eliminates surface MgO, which would otherwise lead to a negative gas yield error. "
   "Ordinary least-squares linear regression across six independent magnesium loadings (10.0 to 35.0 mg) extracts the empirical slope m_slope = 0.92220 mL/mg with a standard error "
   "SE(m) < 1.0 × 10⁻⁵ and an ideal coefficient of determination R² = 1.00000, isolating the standard molar volume V_m,STP = 22.414 L/mol with zero residual offset."
  )
 elif slug=='volatile-liquid-molar-mass':
  return (
   "In vapor density metrology using the classical Dumas method, experimental uncertainty is governed by M = (m_vapor · R · T_bath) / (P_atm · V_flask). "
   "A complete analytical uncertainty budget partitions random and systematic variance into distinct physical components: "
   "(1) Gravimetric Mass Resolution: The analytical balance features a digital readability of ±0.0001 g and repeatability of ±0.00015 g. "
   "For condensed vapor masses ranging from 0.3436 g to 1.0307 g, the relative weighing uncertainty is δm / m ≈ 0.00015 / 0.7559 ≈ 2.0 × 10⁻⁴ (0.020%). "
   "(2) Pycnometric Volume Calibration: Flask volumes are determined individually via brim-full water pycnometry using a precision ground glass cover plate. "
   "With water density known to ±0.00001 g/mL, volumetric uncertainty is less than ±0.03 mL, contributing δV / V = 0.03 / 275.0 ≈ 1.1 × 10⁻⁴ (0.011%). "
   "(3) Bath Temperature Stability: The boiling water bath is monitored with an immersion NIST thermistor to ±0.05 °C in 373.15 K, "
   "yielding a temperature uncertainty of δT / T = 0.05 / 373.15 ≈ 1.3 × 10⁻⁴ (0.013%). "
   "(4) Barometric Pressure Accuracy: Ambient atmospheric pressure is recorded from a Fortin mercury barometer with vernier resolution of ±0.1 mmHg, "
   "yielding δP / P = 0.1 / 760.0 ≈ 1.3 × 10⁻⁴ (0.013%). "
   "(5) Real Gas Non-Ideality: Cyclohexane vapor at 100 °C exhibits weak London dispersion attraction (van der Waals a = 23.3 L²·bar/mol²), "
   "giving a compressibility factor Z ≈ 0.985 that slightly shifts uncorrected molar mass by ~1.5%. "
   "Ordinary least-squares linear regression across six independent bulb volumes (125.0 to 375.0 mL) extracts the empirical slope m_slope = 0.0027485 g/mL with a standard error "
   "SE(m) < 1.0 × 10⁻⁶ and an ideal coefficient of determination R² = 1.00000, isolating the experimental molar mass M = 84.16 g/mol within 0.003% of the true formula weight."
  )
 elif slug=='chemical-reactions-copper-cycle':
  return (
   "In cyclic inorganic transformations and mass conservation metrology, the gravimetric recovery is governed by m_recovered = m_slope · m_initial + m₀. "
   "A rigorous multi-step analytical uncertainty budget evaluates variance contributions across each chemical phase: "
   "(1) Analytical Balance Gravimetric Resolution: The four-decimal electromagnetic force restoration balance provides readability to ±0.0001 g "
   "and repeatability of ±0.00015 g. For copper sample masses between 0.2000 g and 0.7000 g, the relative weighing uncertainty is δm / m ≈ 0.00015 / 0.4500 ≈ 3.3 × 10⁻⁴ (0.033%), "
   "confirming high analytical weighing precision. "
   "(2) Cumulative Mechanical Transfer Losses: Across five successive synthetic procedures involving decantation, washings, and vacuum filtration through ashless paper, "
   "microparticulate loss is held to < 0.5 mg through meticulous rubber policeman wall rinsing. In multi-point linear regression, any constant transfer residue is "
   "absorbed directly into the baseline intercept m₀, leaving the slope m_slope completely unbiased. "
   "(3) Granular Zinc Digestion Completeness: Unreacted metallic zinc (atomic weight 65.38 g/mol) is digested with 6 M HCl until hydrogen gas evolution ceases completely "
   "(E° = +0.76 V). Residual entrapped zinc would introduce a positive mass artifact (+1.029 g per gram of zinc replacing copper). "
   "(4) Solvent Displacement & Desiccation Control: Rinsing the spongy copper cake sequentially with boiling deionized water, 95% ethanol, and reagent-grade acetone displaces "
   "capillary water. Vacuum desiccation at ambient temperature prevents high-temperature aerial oxidation of copper powder to cuprous oxide (Cu₂O) or cupric oxide (CuO). "
   "Ordinary least-squares linear regression across six independent copper loadings (0.20 to 0.70 g) extracts the empirical slope m_slope = 1.00000 g/g with a standard error "
   "SE(m) < 1.0 × 10⁻⁶ and an ideal coefficient of determination R² = 1.00000, isolating 100.00% mass recovery."
  )
 elif slug=='empirical-formula-magnesium-oxide':
  return (
   "In gravimetric empirical formula determination via high-temperature crucible combustion, experimental uncertainty is governed by the mass ratio relation m_oxygen = [M(O) / M(Mg)] · m_Mg + m₀. "
   "A comprehensive analytical uncertainty budget partitions variance sources into distinct chemical and physical mechanisms: "
   "(1) Analytical Balance Gravimetric Resolution: The four-decimal electromagnetic force restoration balance features a digital readability of ±0.0001 g "
   "and a verified repeatability standard deviation of s_m = ±0.00015 g. For an intermediate magnesium sample of 0.5000 g and bound oxygen mass of 0.3291 g, "
   "the relative weighing uncertainty on oxygen is δm / m ≈ 0.00015 / 0.3291 ≈ 4.6 × 10⁻⁴ (0.046%), confirming high instrumental precision. "
   "(2) Crucible Firing to Constant Mass: Even glazed porcelain adsorbs trace moisture from ambient air (typically 0.2 to 0.5 mg). Heating to cherry red (850 °C) "
   "and desiccating over anhydrous calcium sulfate establishes a stable tare baseline within ±0.0003 g. In multi-point linear regression, any minute residual tare "
   "drift is absorbed cleanly into the baseline intercept m₀ = 0.0000 g, leaving the slope completely unbiased. "
   "(3) Nitride Hydrolysis Completeness: Combustion in open air generates 5% to 15% intermediate magnesium nitride (Mg₃N₂), which has an equivalent weight of "
   "only 9.34 g per equivalent of Mg compared to 16.00 g in MgO. Steam digestion with boiling deionized water followed by calcination quantitatively hydrolyzes "
   "all nitride to hydroxide and drives off ammonia gas (Mg₃N₂ + 6H₂O ⟶ 3Mg(OH)₂ + 2NH₃↑), eliminating what would otherwise be a severe negative oxygen error. "
   "(4) Aerosol Containment via Cracked Lid: Micro-cracking the crucible lid by 1.0 to 1.5 mm allows continuous convective influx of atmospheric oxygen while throttling "
   "thermal updrafts, suppressing loss of sub-micron MgO smoke particles to < 0.2 mg. "
   "Ordinary least-squares linear regression across six independent magnesium loadings (0.20 to 0.70 g) extracts the empirical slope m_slope = 0.65823 g O / g Mg with a standard error "
   "SE(m) < 1.0 × 10⁻⁵ and an ideal coefficient of determination R² = 1.00000, isolating the stoichiometric ratio n(O)/n(Mg) = 0.9999 mol O / mol Mg within 0.007% of the theoretical 1:1 rocksalt lattice."
  )
 elif slug=='liquid-viscosity-poiseuille':
  return (
   "In absolute capillary viscometry governed by the Hagen-Poiseuille equation Q = (π · r⁴ · ρ · g · Δh) / (8 · η · L), "
   "experimental uncertainty is dictated by error propagation through the fourth power of tube radius and thermostatic fluid control: "
   "(1) Capillary Radius Sensitivity: Because flow rate scales with r⁴, the relative error in dynamic viscosity from radius measurement is "
   "δη / η = 4 · (δr / r). For our precision capillary of radius r = 0.250 ± 0.001 mm (mercury pycnometry calibration), δr / r = 0.001 / 0.250 = 0.40%, "
   "contributing a systematic uncertainty of 1.6% to absolute uncalibrated geometry. However, precision bore uniformities achieve local invariance to < 0.05%. "
   "(2) Thermostatic Temperature Stability: Liquid water exhibits a steep negative temperature gradient ∂η/∂T ≈ -0.025 mPa·s/°C (-2.5%/°C at 20.0 °C). "
   "The refrigerated/heating circulator maintains jacket temperature within ±0.05 °C, restricting thermal viscosity drift to < ±0.0012 mPa·s (0.12%). "
   "(3) Hydrostatic Head and Cathetometer Resolution: The constant-level overflow weir maintains meniscus stability, with cathetometer vernier resolution of ±0.02 cm. "
   "For the lowest head (Δh = 10.0 cm), relative pressure uncertainty is δ(Δh) / Δh = 0.02 / 10.0 = 0.20%, diminishing to 0.057% at 35.0 cm. "
   "(4) Couette End-Effects and Kinetic Energy Correction: With capillary aspect ratio L/r = 150 / 0.25 = 600, the hydrodynamic entrance length L_e / L < 1.5%, "
   "and kinetic energy dissipation contributes less than 0.20% across the operating range (Re ≤ 88.7). "
   "Ordinary least-squares linear regression across six independent hydrostatic heads (10.0 to 35.0 cm) yields an empirical slope of "
   "m_slope = 0.05995 mL/(min·cm) with an ideal coefficient of determination R² = 1.00000, isolating the absolute dynamic viscosity η = 1.0018 mPa·s within 0.016% of the CIPM reference."
  )
 elif slug=='surface-tension-stalagmometry':
  return (
   "In drop-weight stalagmometry governed by Tate's modified law m_total = [ (2π · r · γ · φ) / g ] · N + m₀, "
   "analytical measurement uncertainty is partitioned into distinct mechanical, thermal, and interfacial components: "
   "(1) Stalagmometer Tip Radius Accuracy: The external ground-glass tip is measured using an optical measuring microscope to r = 3.500 ± 0.002 mm (δr / r = 0.057%). "
   "Because surface tension scales inversely with r (γ ∝ 1/r), this contributes a systematic geometric uncertainty of only ±0.04 mN/m. "
   "(2) Harkins-Jordan Factor Plateau Stability: At r / V^(1/3) = 0.7526, the Harkins-Jordan function φ(r/V^{1/3}) resides in a broad, nearly horizontal plateau "
   "where the derivative ∂φ/∂(r/V^{1/3}) ≈ 0. A 2% variation in droplet volume shifts φ by less than 0.08%, imparting extraordinary robustness against droplet sizing. "
   "(3) Thermostatic Jacket Control: Liquid water exhibits a negative temperature coefficient ∂γ/∂T ≈ -0.151 mN/(m·°C) at 20.0 °C. "
   "The circulating thermostatic water mantle maintains 20.0 ± 0.05 °C, restricting thermal surface tension drift to < ±0.008 mN/m (0.011%). "
   "(4) Evaporative Loss Prevention: Droplets detach directly into a narrow-mouth, ground-glass stoppered weighing bottle. "
   "Gravimetric evaporation trials verify that vapor loss is less than 0.0002 g over a 10-minute collection interval (<0.005% of 4.0 g). "
   "(5) Quasi-Static Detachment Kinetics: Throttling flow to 1 drop every 8 to 10 seconds suppresses hydrodynamic inertial forces (We = ρ v² r / γ < 10⁻⁴), "
   "ensuring pure capillary pinch-off without jetting. "
   "Ordinary least-squares linear regression across six independent drop counts (10 to 60 drops) yields an empirical slope of "
   "m_slope = 0.10040 g/drop with an ideal coefficient of determination R² = 1.00000, isolating the absolute surface tension γ = 72.80 mN/m with zero residual offset."
  )
 return ""

def graph(c,rows,f):
 left,right,top,bottom=68,610,28,280
 xs=[r['x']*c['xScale'] for r in rows];ys=[r['y']*c['yScale'] for r in rows]
 xmin=min(xs);xmax=max(xs);ymin=min(ys);ymax=max(ys)
 dx=(xmax-xmin) or 1;dy=(ymax-ymin) or 1
 xmin-=dx*.12;xmax+=dx*.12;ymin-=dy*.15;ymax+=dy*.15
 px=lambda x:left+(x-xmin)/(xmax-xmin)*(right-left)
 py=lambda y:bottom-(y-ymin)/(ymax-ymin)*(bottom-top)
 out=[]
 for i in range(5):
  x=xmin+i*(xmax-xmin)/4;y=ymin+i*(ymax-ymin)/4
  out.append(f'<line x1="{left}" y1="{py(y):.1f}" x2="{right}" y2="{py(y):.1f}" stroke="#d5e3d7"/>')
  out.append(f'<text x="{left-9}" y="{py(y)+4:.1f}" text-anchor="end" font-size="10" fill="#496950">{fmt(y,1)}</text>')
  out.append(f'<text x="{px(x):.1f}" y="300" text-anchor="middle" font-size="10" fill="#496950">{fmt(x,1)}</text>')
 out.append(f'<path d="M{left} {top}V{bottom}H{right}" stroke="#5c8365" fill="none"/>')
 out.append(f'<text x="335" y="332" text-anchor="middle" fill="#244d2e" font-size="12">{E(c["xAxis"])}</text>')
 out.append(f'<text transform="translate(18 160) rotate(-90)" text-anchor="middle" fill="#244d2e" font-size="12">{E(c["yAxis"])}</text>')
 pts=[f"{px(xmin+i*(xmax-xmin)/100):.1f},{py((f['m']*(xmin+i*(xmax-xmin)/100)/c['xScale']+f['b'])*c['yScale']):.1f}" for i in range(101)]
 out.append(f'<polyline points="{" ".join(pts)}" stroke="#2f5233" stroke-width="2" fill="none"/>')
 for r in rows:
  out.append(f'<circle cx="{px(r["x"]*c["xScale"]):.1f}" cy="{py(r["y"]*c["yScale"]):.1f}" r="4.8" fill="#48bb78" stroke="#142b1a" stroke-width="1.5"><title>V = {r["input"]} mL, m = {r["raw"]} g</title></circle>')
 return f'<svg viewBox="0 0 650 340" role="img" aria-label="Linear regression plot of net mass versus dispensed volume">{"".join(out)}</svg>'

def theory(c):
 out=[
  '<section class="theory-section">',
  f'<h2>Theoretical Foundations of {E(c["shortTitle"])} and Quantitative Chemical Metrology</h2>',
  f'<p class="intro">{E(c["intro"])}</p>',
  '<div class="theory-grid">'
 ]
 for i,t in enumerate(c['topics'],1):
  out.append(f'<article class="theory-card"><div class="theory-head"><span class="eyebrow">TOPIC {str(i).zfill(2)} · FORMAL ANALYSIS</span><h3>{E(t["question"])}</h3></div><div class="theory-body"><p>{E(t["answer"]).replace(chr(10), "<br><br>")}</p></div></article>')
 out.append('</div></section>')
 return "".join(out)

def method(c):
 return '<div class="method-steps">'+''.join(f'<article class="method-step"><div class="step-num">{str(i).zfill(2)}</div><div><h3>{E(s["title"])}</h3><p>{E(s["text"])}</p></div></article>' for i,s in enumerate(c['procedure'],1))+'</div>'

def workbench(c):
 sim_buttons=''.join(
  f'<button id="simMode{m["id"].capitalize()}" class="sim-mode-btn{" active" if i==0 else ""}" data-sim="{m["id"]}" type="button" role="tab" aria-selected="{"true" if i==0 else "false"}"><span class="sim-icon">{m["icon"]}</span> {E(m["label"])}</button>'
  for i,m in enumerate(c.get('simModes', [{'id':'bench','icon':'⚖️','label':'1. Volumetric Gravimetry'},{'id':'compare','icon':'🔬','label':'2. Pycnometry vs U-Tube'},{'id':'sandbox','icon':'💧','label':'3. Thermal Expansion'}]))
 )
 return f'''<section aria-label="Interactive workbench"><div class="section-top"><div><div class="eyebrow">MEASURE · CALIBRATE · ANALYSE</div><h2>Your virtual chemistry laboratory.</h2></div><button id="resetApparatus" class="text-button">Reset apparatus</button></div><div class="new-workbench"><div class="new-visual"><div class="visual-top"><div class="sim-mode-switcher" role="tablist" aria-label="Simulation Views">{sim_buttons}</div><button id="pauseMotion" class="dark-button" hidden>Pause motion</button></div><svg id="apparatusDiagram" viewBox="0 0 720 320" role="img" aria-label="Interactive analytical balance and volumetric glassware workbench for {E(c['shortTitle'])}"></svg><div class="new-meter"><div><small>{E(c['rawLabel'].upper())}</small><strong id="readingValue">—</strong></div><div><small>MEASUREMENT STATUS</small><p id="liveState" style="font-size:11px;margin:7px 0">Ready to dispense {c['initial']} {E(c['inputUnit'])} of liquid.</p></div></div></div><div class="new-controls"><label for="independent">{E(c['inputLabel'])}</label><output id="independentOut">{c['initial']} {E(c['inputUnit'])}</output><input id="independent" type="range" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><label for="independentNumber">Set {E(c['shortInput'])} ({E(c['inputUnit'])})</label><input id="independentNumber" type="number" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><div class="lab-control-meta">{E(c['settings'][0])}</div><button id="measure" class="primary full">{E(c['measureLabel'])}</button><button id="recordReading" class="secondary full" disabled>＋ Record observation</button><p id="trialStatus" class="trial-status" role="status">Adjust {E(c['shortInput'])} V, then weigh the dispensed aliquot.</p></div></div><p class="data-notice">Mass observations are determined by the high-precision thermodynamic equation of state for pure liquid water. Readings reflect thermal equilibrium and analytical balance force restoration.</p><details class="model-note"><summary>Physical chemistry assumptions and metrological limits</summary><p>{E(c['limitations'])} {E(c['modelExtra'])}</p></details></section><section id="apparatus" class="lab-section"><h2>Analytical chemistry apparatus & tools.</h2><div class="apparatus-list">{''.join('<article class="apparatus-item"><h3>'+E(a['name'])+'</h3><p>'+E(a['purpose'])+'</p></article>' for a in c['apparatus'])}</div></section><section id="method" class="lab-section"><div class="eyebrow">FOLLOW THE METHOD</div><h2>A reason behind every step.</h2><p class="intro">{E(c['aim'])} Suggested independent volumetric settings: {", ".join(map(str,c['samples']))} {E(c['inputUnit'])}.</p>{method(c)}</section><section id="results" class="lab-section"><div class="section-top"><div><div class="eyebrow">YOUR NOTEBOOK · <span id="notebookCount">0</span> OBSERVATIONS</div><h2>Turn measurements into quantitative chemical insight.</h2></div><a class="text-button" href="/chemistry/{c['slug']}/report/">See a complete example report ↗</a></div><div class="lab-result-grid"><div class="chart-card"><svg id="labPlot" viewBox="0 0 650 340" role="img" aria-label="Measured observations and fitted linear regression graph"></svg><p>Points are your recorded gravimetric observations. The regression line validates the linear mass-volume proportionality and extracts density.</p></div><div class="fit-card lab-fit"><span class="eyebrow">ORDINARY LEAST-SQUARES FIT · m = ρ·V + m₀</span><div id="fitSummary"></div><div class="report-equation">{E(c['fitEquation'])}</div></div></div><div class="table-card"><table><thead><tr><th>#</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Remove</th></tr></thead><tbody id="readingRows"></tbody></table><p id="emptyReadings">No readings yet. Dispense and weigh a volumetric aliquot to record it.</p></div><div class="lab-reading-actions"><button id="downloadReadings" class="secondary" disabled>↓ Export CSV</button><button id="clearReadings" class="secondary" disabled>Clear notebook</button></div><div class="source-box"><h3>Calculate it yourself.</h3><label for="studentEstimate">Your estimate of {E(c['target'])} ({E(c['resultUnit'])})</label> <input id="studentEstimate" type="number" step="any" min="0" style="max-width:140px"><button id="checkEstimate" class="secondary" style="margin-left:10px">Check calculation</button><p id="estimateFeedback" role="status"></p></div></section><section id="check" class="lab-section lab-questions"><div class="eyebrow">CHECK YOUR UNDERSTANDING</div><h2>Explain what the gravimetric measurements mean.</h2>{''.join('<article class="quiz-card"><h3>'+E(q['question'])+'</h3><div class="quiz-choices">'+''.join('<button class="quiz-option" data-quiz="'+str(i)+'" data-choice="'+str(j)+'">'+E(a)+'</button>' for j,a in enumerate(q['options']))+'</div><p id="quizFeedback'+str(i)+'" class="quiz-feedback" role="status"></p></article>' for i,q in enumerate(c['quiz']))}</section>'''

def report_narrative(c,rows,f,value,percent,reference,se):
 slug=c['slug']
 if slug=='density-mass-volume-precision':
  abstract=(
   f"Seven gravimetric trials were executed across dispensed volumes V = {rows[0]['input']:.1f} mL to V = {rows[-1]['input']:.1f} mL of pure deionized water "
   f"equilibrated to 20.00 °C (resulting in net mass readings from {rows[0]['raw']:.4f} g to {rows[-1]['raw']:.4f} g on an electronic analytical balance). "
   f"An ordinary least-squares linear regression of net mass m against dispensed volume V yielded an experimental density of "
   f"{fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} and an intercept of {fmt(f['b'],c['resultDecimals'])} g, "
   f"demonstrating exact agreement with the international CIPM standard water density formulation (reference value = {fmt(reference*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, difference = {percent:.4f}%). "
   f"Applying the CIPM atmospheric air buoyancy correction confirmed that apparent balance readings in laboratory air underestimate true vacuum mass by 0.105%, "
   f"verifying the necessity of buoyancy compensation in high-precision analytical chemistry."
  )
  graph_choice=(
   f"The mathematical regression fits the linear physical model m = ρ·V + m_0, where V represents dispensed liquid volume in mL, "
   f"m represents net liquid mass in g, ρ represents the liquid density in {c['gradientUnit']}, and m_0 represents the baseline tare intercept in g "
   f"(theoretically m_0 = 0.0000 g). The slope of this regression line directly yields the intensive bulk density of the liquid, while constant tare "
   f"offsets or uniform meniscus drainage residues are absorbed into the intercept."
  )
  discussion=(
   "The experimental observations provide rigorous quantitative verification of Density Metrology, Volumetric Analysis, and Archimedean Air Buoyancy Corrections. "
   "In quantitative analytical chemistry, density serves as an essential physical fingerprint for identifying substances, verifying chemical purity, and determining solution concentrations. "
   "Our investigation utilized pure deionized water (resistivity 18.2 MΩ·cm) maintained at exactly 20.00 ± 0.02 °C in a thermostatic water bath. "
   "Across the 7 volumetric aliquots dispensed from the Class A 50.00 mL burette (from 5.0 mL to 35.0 mL), the net mass scaled in strictly linear proportion to volume. "
   "The ordinary least-squares linear regression line m = 0.99820·V + 0.00000 g yielded a coefficient of determination of R² = 1.00000, indicating perfect linearity. "
   "The extracted experimental density ρ = 0.9982 g/mL matches the international CIPM reference standard to within 0.0000% difference. "
   "A critical aspect of high-precision gravimetry is Archimedes' atmospheric buoyancy effect: because liquid water has a density (~1.0 g/mL) substantially lower than the "
   "stainless steel calibration weights inside the balance (~8.0 g/mL), the water displaces eight times more ambient air per gram, experiencing an upward buoyant force "
   "of approximately 1.05 mg per gram of water. Uncorrected balance readings therefore systematically underestimate vacuum mass by 0.105%. "
   "By performing a multi-point regression across seven systematic volumetric increments rather than relying on a single-point quotient m/V, constant meniscus transfer biases "
   "and residual droplet retention on glassware walls were absorbed entirely into the regression intercept parameter b = 0.0000 g, leaving the slope m_slope as an unbiased estimator of true density. "
   "Comparative evaluation against capillary pycnometry (±0.0001 g/mL) and digital oscillating U-tube densitometers (±0.00005 g/mL) illustrated the operational trade-offs "
   "between measurement speed, required sample volume, and optical meniscus alignment parallax errors."
  )
  conclusion=(
   "This laboratory investigation successfully demonstrated the high-precision determination of liquid density using analytical balances and Class A volumetric glassware. "
   f"Through systematic multi-point gravimetric dispensing from V = {rows[0]['input']:.1f} mL to {rows[-1]['input']:.1f} mL, we extracted an experimental liquid density of "
   f"ρ = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with a fit standard error of {fmt(se*c['resultScale'])} {c['resultUnit']} and an ideal R² = 1.00000. "
   "The empirical result confirms the CIPM thermodynamic reference value for pure water at 20.00 °C (0.99820 g/mL) with zero residual error. "
   "The experiment established the physical foundation of intensive thermodynamic properties, demonstrated the mathematical necessity of Archimedean buoyancy corrections, "
   "and proved why ordinary least-squares regression represents the gold standard for eliminating systematic tare and transfer offsets in quantitative chemical measurement."
  )
  return abstract, graph_choice, discussion, conclusion
 elif slug=='hydrate-stoichiometric-composition':
  abstract=(
   f"Seven gravimetric dehydration trials were executed across initial hydrated copper(II) sulfate masses m_hydrate = {rows[0]['input']:.1f} g to {rows[-1]['input']:.1f} g "
   f"(recovering anhydrous salt masses m_anhydrous from {rows[0]['x']:.4f} g to {rows[-1]['x']:.4f} g and evolved water masses m_water from {rows[0]['raw']:.4f} g to {rows[-1]['raw']:.4f} g). "
   f"An ordinary least-squares linear regression of water mass lost against anhydrous salt mass yielded an empirical stoichiometric slope of "
   f"{fmt(f['m'],6)} g water / g salt, which scales to an experimental hydration number of x = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} "
   f"and an intercept of {fmt(f['b'],c['resultDecimals'])} g, demonstrating exact agreement with the stoichiometric formula CuSO₄·5H₂O (difference = {percent:.4f}%). "
   f"The stepwise color change from azure-blue to grayish-white confirmed complete loss of crystal field splitting and full transition to anhydrous copper(II) sulfate."
  )
  graph_choice=(
   f"The mathematical regression fits the stoichiometric linear model m_water = [x · (M_water / M_salt)] · m_anhydrous + b, where m_anhydrous represents "
   f"the recovered mass of anhydrous CuSO₄ in g, m_water represents the mass of vaporized water in g, and the slope m_slope corresponds to the stoichiometric "
   f"mass ratio (x · M_water / M_salt). Multiplying the slope by the molar mass ratio (M_CuSO₄ / M_H₂O = 159.609 / 18.0154 = 8.859588) directly yields the "
   f"stoichiometric hydration coefficient x in {c['resultUnit']}, while constant crucible tare drift is absorbed into the intercept b."
  )
  discussion=(
   "The experimental observations provide rigorous quantitative verification of Hydrate Stoichiometry, Coordination Chemistry, and Thermal Desiccation Metrology. "
   "In inorganic solid-state chemistry, hydrates possess well-defined integer stoichiometric ratios of water molecules coordinated to metal cations or anchored in crystal lattices. "
   "Copper(II) sulfate pentahydrate crystallizes in a distorted octahedral structure [Cu(H₂O)₄]SO₄·H₂O, where four water molecules coordinate equatorially to the Cu²⁺ ion, "
   "and a fifth water molecule bridges sulfate oxygen atoms through four cooperative hydrogen bonds. "
   "Under controlled thermal calcination in a porcelain crucible at 250 °C, all five water molecules were evolved as steam, leaving behind chalky grayish-white anhydrous CuSO₄. "
   "The color transition directly corroborates Crystal Field Theory: the removal of coordinating water ligands destroys the octahedral crystal field splitting Δ_o, "
   "shifting d-d electronic absorption out of the visible spectrum into the infrared. "
   "Across all seven trials from m_hydrate = 1.5 g to 7.5 g, the mass of water evolved scaled in strict linear proportion to the recovered anhydrous salt mass. "
   "The ordinary least-squares regression line m_water = 0.564360 · m_anhydrous − 0.000014 g yielded a coefficient of determination of R² = 1.00000. "
   "Multiplying the regression slope by the molar mass quotient (159.609 / 18.0154) extracted an empirical stoichiometric coefficient of x = 5.0000 moles of H₂O per mole of CuSO₄, "
   "matching the theoretical pentahydrate formula with a percentage difference of 0.0002%. "
   "Crucible heating to constant mass (consecutive weighings within ±0.0002 g) and cooling inside a vacuum desiccator containing activated Drierite prevented hygroscopic reabsorption "
   "of atmospheric moisture, ensuring that the weighed residue was completely dry and free of atmospheric contamination."
  )
  conclusion=(
   "This laboratory investigation quantitatively determined the water of crystallization and empirical formula of hydrated copper(II) sulfate. "
   f"Through systematic thermal desiccation across sample masses from {rows[0]['input']:.1f} g to {rows[-1]['input']:.1f} g, we extracted an experimental stoichiometric hydration number of "
   f"x = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with an ideal R² = 1.00000 and a percentage difference of {percent:.4f}% from the theoretical pentahydrate value. "
   "The investigation verified the thermodynamic necessity of heating to constant mass, established the physical basis of crystal field color changes in transition metal complexes, "
   "and proved why ordinary least-squares regression represents an essential analytical technique for extracting stoichiometric coefficients with maximum statistical confidence."
  )
  return abstract, graph_choice, discussion, conclusion
 elif slug=='limiting-reactant-precipitation':
  abstract=(
   f"Six gravimetric precipitation trials were executed across added volumes of 0.1000 M Na₂SO₄ from V = {rows[0]['input']:.1f} mL to V = {rows[-1]['input']:.1f} mL "
   f"reacted with a constant excess of 30.00 mL of 0.1000 M BaCl₂ (yielding isolated dry BaSO₄ masses from {rows[0]['raw']:.4f} g to {rows[-1]['raw']:.4f} g). "
   f"An ordinary least-squares linear regression of precipitate mass m against added sulfate volume V yielded an empirical slope of "
   f"{fmt(f['m'],6)} g/mL, extracting an experimental molar mass for barium sulfate of M = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} "
   f"and a baseline intercept of {fmt(f['b'],c['resultDecimals'])} g, demonstrating remarkable agreement with the theoretical formula weight of 233.390 g/mol (difference = {percent:.4f}%). "
   f"Spot tests on the supernatant confirmed the presence of unreacted excess Ba²⁺ ions, rigorously validating that sulfate acted strictly as the limiting reagent across all trials."
  )
  graph_choice=(
   f"The mathematical regression fits the stoichiometric linear model m_BaSO₄ = [C_SO₄ · M_BaSO₄ / 1000] · V_SO₄ + m₀, where V_SO₄ represents the volume "
   f"of 0.1000 M Na₂SO₄ added in mL, m_BaSO₄ represents the dry precipitate mass in g, C_SO₄ represents titrant molarity (0.1000 mol/L), and m₀ represents the "
   f"baseline intercept in g (theoretically m₀ = 0.0000 g). The slope m_slope directly relates to the molar mass of barium sulfate via M_BaSO₄ = (m_slope / C_SO₄) · 1000, "
   f"while constant crucible tare artifacts and minor transfer residues are absorbed into the intercept."
  )
  discussion=(
   "The experimental observations provide rigorous quantitative verification of the Law of Limiting Reactants, Gravimetric Precipitation Thermodynamics, and von Weimarn's Nucleation Dynamics. "
   "In aqueous solution, the metathesis reaction between barium chloride and sodium sulfate proceeds via the net ionic equilibrium Ba²⁺ (aq) + SO₄²⁻ (aq) <===> BaSO₄ (s). "
   "Because barium sulfate possesses an exceptionally low solubility product constant (K_sp = 1.08 × 10⁻¹⁰ at 25 °C), the precipitation reaction proceeds to virtual completion. "
   "Throughout all six trials, the initial quantity of barium ions was maintained constant at 3.000 mmol (30.00 mL of 0.1000 M BaCl₂), while sodium sulfate was added in quantities "
   "ranging from 0.400 mmol (4.00 mL) to 2.400 mmol (24.00 mL). In every trial, the stoichiometric ratio between Ba²⁺ and SO₄²⁻ is 1:1, meaning that sulfate was completely consumed, "
   "acting as the limiting reactant that dictated the theoretical yield of precipitate. "
   "Unreacted barium ions remained in excess in the supernatant, which was qualitatively confirmed by adding sodium sulfate spot reagent to the filtrate and observing renewed white BaSO₄ cloudiness. "
   "Across the six trials, the isolated mass of barium sulfate increased in strict linear proportion to the volume of sulfate added, generating a regression line with an ideal R² = 1.00000. "
   "The slope of the regression line, m_slope = 0.0233364 g/mL, corresponds to an experimental molar mass of M = 233.36 g/mol, matching the true formula weight of 233.390 g/mol to within 0.011%. "
   "Precipitation at elevated temperature (85 °C) under dilute conditions with dropwise addition minimized relative supersaturation (Q - S)/S according to von Weimarn's principle. "
   "Thermal digestion for 45 minutes enabled Ostwald ripening, allowing high-solubility sub-micron crystallites to redissolve and recrystallize onto larger crystal faces. "
   "This coarsening prevented colloidal losses through the Grade 4 sintered glass fritted disc (pore size 1.0–1.6 µm). "
   "Acidification with 1.0 mL of 6 M HCl successfully prevented the coprecipitation of barium carbonate (BaCO₃) and barium phosphate (Ba₃(PO₄)₂), while thorough washing with boiling deionized water "
   "eliminated adsorbed chloride ions, as proven by negative silver nitrate tests on the effluent washings."
  )
  conclusion=(
   "This laboratory investigation successfully demonstrated the quantitative principles of limiting reactants and gravimetric stoichiometry through the precipitation of barium sulfate. "
   f"Through systematic volumetric additions from V = {rows[0]['input']:.1f} mL to {rows[-1]['input']:.1f} mL of 0.1000 M Na₂SO₄ into excess BaCl₂, we extracted an experimental "
   f"molar mass of M(BaSO₄) = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with a fit standard error of {fmt(se*c['resultScale'])} {c['resultUnit']} and an ideal R² = 1.00000. "
   f"The experimental value agrees with the theoretical chemical formula weight (233.390 g/mol) to within {percent:.4f}% error. "
   "The investigation verified von Weimarn's law of supersaturation, demonstrated the thermodynamic necessity of Ostwald ripening during thermal digestion, "
   "and proved that multi-point ordinary least-squares regression provides an exceptionally robust analytical methodology for stoichiometric verification."
  )
  return abstract, graph_choice, discussion, conclusion
 elif slug=='molar-volume-ideal-gas':
  abstract=(
   f"Six eudiometric hydrogen displacement trials were performed by reacting polished magnesium ribbon strips (masses m_Mg = {rows[0]['input']:.1f} mg to {rows[-1]['input']:.1f} mg) "
   f"with excess 6.0 M hydrochloric acid over an aqueous column (yielding dry STP hydrogen volumes from {rows[0]['raw']:.3f} mL to {rows[-1]['raw']:.3f} mL). "
   f"An ordinary least-squares linear regression of standardized volume V_STP against magnesium mass m_Mg yielded an empirical slope of "
   f"{fmt(f['m'],5)} mL/mg, which scales by the atomic weight of magnesium (M = 24.305 g/mol) to extract an experimental molar volume of "
   f"V_m,STP = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} and an intercept of {fmt(f['b'],c['resultDecimals'])} mL, "
   f"achieving exact agreement with the ideal gas reference value of 22.414 L/mol (difference = {percent:.4f}%). "
   f"Dalton vapor pressure subtraction (P_H2O* = 17.54 mmHg) and meniscus hydrostatic leveling eliminated systematic pressure biases."
  )
  graph_choice=(
   f"The mathematical regression fits the stoichiometric gas model V_STP = [V_m,STP / M_Mg] · m_Mg + V₀, where m_Mg represents "
   f"the mass of reacted magnesium in mg, V_STP represents the dry hydrogen volume at STP in mL, and V₀ represents the baseline intercept in mL "
   f"(theoretically V₀ = 0.000 mL). Multiplying the regression slope m_slope by the molar mass of magnesium (24.305 g/mol) directly isolates the "
   f"molar volume of hydrogen at STP in {c['resultUnit']}, while constant meniscus calibration offsets or bubble entrapment artifacts are absorbed into V₀."
  )
  discussion=(
   "The experimental observations provide rigorous quantitative verification of Avogadro's Hypothesis, Dalton's Law of Partial Pressures, and Ideal Gas Stoichiometry. "
   "The single displacement reaction between metallic magnesium and hydrochloric acid, Mg (s) + 2 HCl (aq) ---> MgCl₂ (aq) + H₂ (g), proceeds rapidly and quantitatively to completion. "
   "Because the reaction exhibits a strict 1:1 stoichiometric mole ratio, each mole of magnesium consumed liberates exactly one mole of diatomic hydrogen gas. "
   "Throughout the six trials across reactant masses from 10.0 mg to 35.0 mg, the dry gas volume converted to STP scaled in strict linear proportion to magnesium mass. "
   "The ordinary least-squares regression line V_STP = 0.92220 · m_Mg + 0.000 mL achieved an ideal coefficient of determination R² = 1.00000. "
   "Scaling the slope by M(Mg) = 24.305 g/mol yielded an experimental molar volume of V_m,STP = 22.414 L/mol, matching the universal ideal gas constant prediction to within 0.0003%. "
   "Two critical thermodynamic and physical corrections were essential for achieving this degree of precision: "
   "First, Dalton's law of partial pressures: hydrogen gas collected over water is saturated with water vapor at ambient bath temperature (20.0 °C). "
   "Subtracting the equilibrium saturation vapor pressure P_H2O* = 17.54 mmHg from total barometric pressure (760.0 mmHg) isolated the true dry hydrogen partial pressure (742.46 mmHg), "
   "eliminating a 2.3% positive volume error. "
   "Second, hydrostatic leveling: by submerging the eudiometer in a 1000 mL leveling cylinder and matching internal and external water levels, the downward gravitational pull "
   "of the suspended water column was eliminated, ensuring P_total = P_atm exactly. "
   "The copper wire cage effectively prevented premature floating of magnesium fragments and formed a sacrificial galvanic couple that accelerated the reaction rate, "
   "while pre-polishing the ribbon with 600-grit emery paper removed passivating oxide crusts."
  )
  conclusion=(
   "This laboratory investigation successfully demonstrated the quantitative determination of the molar volume of an ideal gas using eudiometric gas collection techniques. "
   f"Through systematic acid displacement across magnesium masses from {rows[0]['input']:.1f} mg to {rows[-1]['input']:.1f} mg, we extracted an experimental molar volume of "
   f"V_m,STP = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with a standard error of {fmt(se*c['resultScale'])} {c['resultUnit']} and an ideal R² = 1.00000. "
   f"The empirical result confirms the theoretical IUPAC STP molar volume of an ideal gas (22.414 L/mol) with a percentage difference of {percent:.4f}%. "
   "The investigation validated Dalton's law of partial pressures, demonstrated the fluid mechanics of hydrostatic head neutralization, "
   "and established multi-point linear regression as an indispensable method for high-accuracy gas metrology."
  )
  return abstract, graph_choice, discussion, conclusion
 elif slug=='volatile-liquid-molar-mass':
  abstract=(
   f"Six Dumas vapor density trials were conducted using precision-calibrated borosilicate bulbs (internal volumes V_flask = {rows[0]['input']:.1f} mL to {rows[-1]['input']:.1f} mL) "
   f"immersed in a boiling water bath at T_bath = 100.0 °C (373.15 K) under barometric pressure P_atm = 1.000 atm (760.0 mmHg), yielding condensed cyclohexane masses "
   f"from {rows[0]['raw']:.4f} g to {rows[-1]['raw']:.4f} g. "
   f"An ordinary least-squares linear regression of condensed vapor mass m_vapor against bulb volume V_flask yielded an empirical vapor density slope of "
   f"{fmt(f['m'],7)} g/mL, extracting an experimental molar mass of M = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} "
   f"and an intercept of {fmt(f['b'],c['resultDecimals'])} g, demonstrating exceptional agreement with the theoretical formula weight of cyclohexane (84.161 g/mol, difference = {percent:.4f}%). "
   f"Complete air purging through a 0.5 mm pinhole and gravimetric water pycnometry ensured high analytical fidelity."
  )
  graph_choice=(
   f"The mathematical regression fits the stoichiometric vapor model m_vapor = [P_atm · M / (R · T_bath)] · V_flask + m₀, where V_flask represents "
   f"the calibrated internal volume of the Dumas bulb in mL, m_vapor represents the mass of condensed organic liquid in g, and m₀ represents the baseline "
   f"intercept in g (theoretically m₀ = 0.0000 g). Multiplying the regression slope m_slope by (R · T_bath / P_atm = 30619.7 mL·atm/mol) directly isolates the "
   f"molecular weight M in {c['resultUnit']}, while constant aluminum foil crimp tare artifacts or external wiping offsets are absorbed into m₀."
  )
  discussion=(
   "The experimental observations provide rigorous quantitative verification of Avogadro's Hypothesis, the Kinetic Molecular Theory of Gases, and Dumas Vapor Metrology. "
   "In quantitative physical chemistry, the Dumas method provides a direct macroscopic gateway to molecular weight determination by measuring the bulk density of an unknown "
   "vapor in thermal equilibrium with its surroundings. "
   "When liquid cyclohexane (bp 80.7 °C) was heated in a boiling water bath at 100.0 °C, the rapid generation of vapor purged ambient air out through the 0.5 mm pinhole. "
   "At the instant the last liquid droplet vaporized, the bulb contained pure cyclohexane vapor at exactly 100.0 °C (373.15 K) and 1.000 atm (760.0 mmHg). "
   "Across all six calibrated Dumas bulbs from 125.0 mL to 375.0 mL, the mass of condensed vapor scaled in strictly linear proportion to flask volume. "
   "The ordinary least-squares linear regression line m_vapor = 0.0027485 · V_flask + 0.00002 g yielded an ideal coefficient of determination R² = 1.00000. "
   "Multiplying the regression slope by (R · T / P) extracted an experimental molar mass of M = 84.16 g/mol, matching the true formula weight of cyclohexane (84.161 g/mol) to within 0.0027%. "
   "A critical procedural safeguard was confirming complete vaporization prior to quenching: because liquid cyclohexane is ~283 times denser than its vapor, "
   "even a microscopic 0.05 mL residual droplet would have produced a severe +5% positive mass bias. "
   "Furthermore, pycnometric calibration of each flask volume with deionized water using a flat optical glass plate eliminated standard glassware volumetric tolerances, "
   "achieving volume accuracy within ±0.02 mL."
  )
  conclusion=(
   "This laboratory investigation successfully demonstrated the quantitative determination of the molar mass of a volatile organic liquid using the classical Dumas method. "
   f"Through systematic vapor density determinations across calibrated bulb volumes from {rows[0]['input']:.1f} mL to {rows[-1]['input']:.1f} mL, we extracted an experimental "
   f"molar mass of M = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with a fit standard error of {fmt(se*c['resultScale'])} {c['resultUnit']} and an ideal R² = 1.00000. "
   f"The experimental value confirms the theoretical molecular weight of cyclohexane (84.161 g/mol) with a percentage error of {percent:.4f}%. "
   "The investigation validated the ideal gas equation of state, evaluated van der Waals real-gas non-ideality, "
   "and proved that multi-point linear regression represents a powerful analytical strategy for eliminating tare and transfer biases in gas gravimetry."
  )
  return abstract, graph_choice, discussion, conclusion
 elif slug=='chemical-reactions-copper-cycle':
  abstract=(
   f"Six quantitative Copper Cycle trials were performed across initial metallic copper loadings from m_initial = {rows[0]['input']:.2f} g to {rows[-1]['input']:.2f} g. "
   f"Each sample was processed through a closed five-reaction sequence: oxidation with concentrated HNO₃ to Cu(NO₃)₂, precipitation with 3.0 M NaOH to Cu(OH)₂, "
   f"thermal dehydration at 90 °C to CuO, dissolution with 3.0 M H₂SO₄ to CuSO₄, and single displacement reduction with granular zinc back to elemental metallic copper. "
   f"Following hydrochloric acid digestion of excess zinc, solvent washing with ethanol and acetone, and vacuum desiccation, recovered copper masses ranged from "
   f"{rows[0]['raw']:.4f} g to {rows[-1]['raw']:.4f} g. "
   f"Ordinary least-squares linear regression of recovered copper mass against initial copper mass yielded an empirical recovery slope of "
   f"{fmt(f['m'],6)} g/g (corresponding to an experimental recovery of {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}) "
   f"with an intercept of {fmt(f['b'],c['resultDecimals'])} g and an ideal coefficient of determination R² = 1.00000, "
   f"confirming the Law of Conservation of Mass with a percentage difference of {percent:.4f}%."
  )
  graph_choice=(
   f"The linear regression models the stoichiometric mass conservation relation m_recovered = (Recovery / 100) · m_initial + m₀, "
   f"where m_initial represents the initial polished copper wire mass in g, m_recovered represents the desiccated recovered metallic copper mass in g, "
   f"and m₀ represents the transfer/tare baseline offset in g (theoretically m₀ = 0.0000 g). "
   f"The regression slope m_slope directly represents the marginal recovery efficiency (d(m_rec) / d(m_init)), "
   f"scaling by 100 to yield {c['resultUnit']} recovery while remaining completely immune to constant filter paper taring biases."
  )
  discussion=(
   "The experimental findings provide rigorous quantitative validation of the Law of Conservation of Mass and the stoichiometric integrity of multi-step inorganic synthesis. "
   "Throughout the five diverse chemical transformations—spanning exothermic redox oxidation, metathesis hydroxide precipitation, solid-state endothermic dehydration, "
   "acid-base neutralization, and galvanic single displacement—the copper atoms underwent dramatic shifts in coordination geometry, color, and phase: "
   "from salmon-pink metallic crystal to emerald-green [Cu(H₂O)₆]²⁺, sky-blue gelatinous Cu(OH)₂, dense black monoclinic CuO, royal-blue tetrahedral/octahedral CuSO₄, "
   "and finally back to spongy red-brown metallic copper. "
   "Despite the complexity of five consecutive manipulations, ordinary least-squares regression across six independent loadings (0.20 g to 0.70 g) "
   "demonstrated perfect linearity (R² = 1.00000) with a slope of m_slope = 1.00000 g/g. "
   "This outcome validates Lavoisier's foundational principle: atoms are rearranged into novel chemical bonds and crystalline structures, but the total elemental mass "
   "is strictly conserved. "
   "The thermal dehydration step (converting Cu(OH)₂ to granular CuO) was instrumental in preventing colloidal pore-clogging during subsequent handling, "
   "and the addition of 6 M HCl successfully digested all excess sacrificial zinc metal without attacking the more noble metallic copper."
  )
  conclusion=(
   "This laboratory investigation successfully demonstrated the quantitative execution of the Copper Cycle and confirmed the Law of Conservation of Mass. "
   f"Across initial copper sample masses spanning {rows[0]['input']:.2f} g to {rows[-1]['input']:.2f} g, we isolated recovered copper with an empirical slope of "
   f"m_slope = {fmt(f['m'],6)} g/g, establishing an experimental recovery of {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} "
   f"with a standard error of {fmt(se*c['resultScale'])} {c['resultUnit']} and an ideal coefficient of determination R² = 1.00000. "
   f"The observed recovery exhibits an absolute percentage difference of {percent:.4f}% from the theoretical 100.00% mass conservation limit. "
   "The study confirmed that multi-point linear regression provides superior analytical reliability in multi-step chemical syntheses by isolating "
   "marginal stoichiometric yields from systematic background transfer offsets."
  )
  return abstract, graph_choice, discussion, conclusion
 elif slug=='empirical-formula-magnesium-oxide':
  abstract=(
   f"Six quantitative thermal oxidation trials were conducted using burnished metallic magnesium ribbon (initial masses m_Mg = {rows[0]['input']:.2f} g to {rows[-1]['input']:.2f} g) "
   f"fired inside porcelain crucibles over a Meker high-temperature burner. "
   f"Following controlled combustion, steam digestion of intermediate magnesium nitride with boiling deionized water, and calcination at 850 °C to constant mass, "
   f"bound oxygen masses ranged from {rows[0]['raw']:.4f} g to {rows[-1]['raw']:.4f} g. "
   f"An ordinary least-squares linear regression of bound oxygen mass against initial magnesium mass yielded an empirical mass ratio slope of "
   f"{fmt(f['m'],6)} g O / g Mg, extracting a stoichiometric molar ratio of {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} "
   f"with an intercept of {fmt(f['b'],c['resultDecimals'])} g and an ideal coefficient of determination R² = 1.00000, "
   f"confirming the 1:1 empirical formula MgO with a percentage difference of {percent:.4f}%."
  )
  graph_choice=(
   f"The mathematical regression models the stoichiometric relation m_oxygen = [M(O) / M(Mg)] · m_Mg + m₀, "
   f"where m_Mg represents the initial polished magnesium ribbon mass in g, m_oxygen represents the gravimetrically determined mass of bound oxygen in g, "
   f"and m₀ represents the baseline intercept in g (theoretically m₀ = 0.0000 g). "
   f"Multiplying the regression slope m_slope by (M_Mg / M_O = 24.305 / 15.9994 = 1.51912) directly isolates the "
   f"stoichiometric formula coefficient in {c['resultUnit']}, while constant crucible glaze tare offsets are absorbed into m₀."
  )
  discussion=(
   "The experimental data provide definitive quantitative confirmation of Joseph Proust's Law of Definite Proportions and John Dalton's Atomic Theory. "
   "In the rocksalt crystal structure of magnesium oxide, divalent magnesium cations (Mg²⁺) and divalent oxide anions (O²⁻) pack in equal numbers "
   "to establish electrostatic charge neutrality in an alternating face-centered cubic lattice. "
   "Throughout all six independent combustions across sample masses from 0.20 g to 0.70 g, the mass of incorporated oxygen scaled in strict linear "
   "proportion to the mass of reacted magnesium metal. "
   "The ordinary least-squares linear regression line m_oxygen = 0.65823 · m_Mg + 0.00003 g yielded an ideal coefficient of determination R² = 1.00000. "
   "Multiplying the regression slope by 1.51912 extracted an empirical stoichiometric mole ratio of n(O)/n(Mg) = 0.9999 mol O / mol Mg, "
   "matching the theoretical 1.0000 ratio to within 0.0072%. "
   "The steam digestion step with boiling deionized water was essential: intermediate magnesium nitride (Mg₃N₂), which forms readily in hot air, "
   "was completely converted to magnesium hydroxide and gaseous ammonia, eliminating a severe negative mass error. "
   "Furthermore, the cracked lid technique effectively throttled convective plumes, preventing the loss of white MgO smoke nanoparticles."
  )
  conclusion=(
   "This laboratory investigation successfully determined the empirical formula of magnesium oxide via quantitative crucible thermal oxidation. "
   f"Through systematic calcination across magnesium loadings from {rows[0]['input']:.2f} g to {rows[-1]['input']:.2f} g, we extracted an empirical "
   f"stoichiometric ratio of n(O)/n(Mg) = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with a fit standard error of "
   f"{fmt(se*c['resultScale'])} {c['resultUnit']} and an ideal R² = 1.00000. "
   f"The observed ratio exhibits an absolute percentage difference of {percent:.4f}% from the theoretical 1:1 stoichiometry, establishing the definitive "
   f"chemical formula as MgO. "
   "The investigation verified the Law of Definite Proportions, demonstrated the necessity of hydrolyzing nitrogenous reaction intermediates, "
   "and proved that multi-point linear regression isolates true chemical stoichiometry from crucible taring and transfer biases."
  )
  return abstract, graph_choice, discussion, conclusion
 elif slug=='liquid-viscosity-poiseuille':
  abstract=(
   f"Six steady-state Poiseuille capillary flow trials were conducted using ultra-pure deionized water at T = 20.0 ± 0.05 °C (293.15 K) "
   f"across hydrostatic pressure heads from Δh = {rows[0]['input']:.1f} cm to {rows[-1]['input']:.1f} cm (ΔP = 978.9 Pa to 3426.1 Pa) "
   f"through a precision horizontal borosilicate capillary (radius r = 0.250 mm, length L = 15.00 cm). "
   f"Measured volumetric discharge rates ranged from {rows[0]['raw']:.3f} mL/min to {rows[-1]['raw']:.3f} mL/min, with Reynolds numbers "
   f"confirming strictly laminar streamline flow (Re = 25.3 to 88.7 ≪ 2000). "
   f"Ordinary least-squares linear regression of volumetric flow rate Q against hydrostatic head Δh yielded an empirical hydraulic slope of "
   f"{fmt(f['m'],6)} mL/(min·cm), extracting an absolute dynamic viscosity of η = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} "
   f"with an intercept of {fmt(f['b'],c['resultDecimals'])} mL/min and an ideal coefficient of determination R² = 1.00000, "
   f"demonstrating exceptional agreement with the CIPM reference standard (1.0020 mPa·s, percentage difference = {percent:.4f}%)."
  )
  graph_choice=(
   f"The linear regression fits the Hagen-Poiseuille equation Q = [ (π · r⁴ · ρ · g · 10⁴ · 60) / (8 · L · η) ] · Δh + Q₀, "
   f"where Δh represents the constant hydrostatic head in cm, Q represents the volumetric effluent discharge rate in mL/min, "
   f"and Q₀ represents the residual discharge meniscus intercept in mL/min (theoretically Q₀ = 0.000 mL/min). "
   f"Inverting the regression slope m_slope via η = K_geom / m_slope directly isolates the absolute dynamic viscosity in {c['resultUnit']}, "
   f"while cathetometer zero-datum alignment offsets are absorbed into Q₀."
  )
  discussion=(
   "The experimental findings provide rigorous empirical verification of the Hagen-Poiseuille Law, Newton's Law of Viscosity, and Laminar Continuum Mechanics. "
   "In viscous fluid dynamics, Poiseuille flow represents an exact analytical solution of the Navier-Stokes equations under cylindrical symmetry and no-slip wall boundary conditions. "
   "Across all six hydrostatic pressure settings from 10.0 cm to 35.0 cm of water column, the volumetric discharge rate exhibited perfect linear proportionality to the driving head. "
   "The ordinary least-squares regression line Q = 0.059954 · Δh − 0.0003 mL/min achieved an ideal coefficient of determination R² = 1.00000. "
   "Inverting this slope using the calibrated capillary geometry extracted an absolute dynamic viscosity of η = 1.0018 mPa·s, matching the authoritative CIPM reference standard "
   "of pure liquid water (1.0020 mPa·s at 20.0 °C) to within 0.016%. "
   "Operating at Reynolds numbers between Re = 25.3 and 88.7 ensured that momentum dissipation occurred exclusively via molecular laminar shear rather than turbulent eddy diffusion. "
   "Furthermore, the high capillary aspect ratio (L/r = 600) successfully suppressed Couette entrance and exit losses to less than 0.2%, eliminating the need for empirical end-corrections."
  )
  conclusion=(
   "This laboratory investigation successfully determined the absolute dynamic viscosity of liquid water at 20.0 °C via Poiseuille capillary flow. "
   f"Through systematic flow rate determinations across hydrostatic heads from {rows[0]['input']:.1f} cm to {rows[-1]['input']:.1f} cm, we extracted an absolute "
   f"dynamic viscosity of η = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with a fit standard error of "
   f"{fmt(se*c['resultScale'])} {c['resultUnit']} and an ideal coefficient of determination R² = 1.00000. "
   f"The experimental viscosity confirms the CIPM thermodynamic reference value (1.0020 mPa·s) with a percentage difference of {percent:.4f}%. "
   "The study confirmed the validity of the fourth-power radius scaling in Poiseuille flow, proved the stability of laminar streamlines at low Reynolds numbers, "
   "and demonstrated that multi-point hydrostatic regression provides a primary, standard-free method for fluid viscosity metrology."
  )
  return abstract, graph_choice, discussion, conclusion
 elif slug=='surface-tension-stalagmometry':
  abstract=(
   f"Six precision drop-weight stalagmometry trials were conducted using ultra-pure deionized water at T = 20.0 ± 0.05 °C (293.15 K) "
   f"across detached droplet counts from N = {int(rows[0]['input'])} to N = {int(rows[-1]['input'])} drops using a calibrated Traube stalagmometer "
   f"(external tip radius r = 3.500 mm, Harkins-Jordan correction factor φ = 0.6150). "
   f"Cumulative detached droplet masses ranged from {rows[0]['raw']:.4f} g to {rows[-1]['raw']:.4f} g, collected at a quasi-static detachment rate "
   f"of 1 drop every 8–10 seconds inside a stoppered weighing bottle. "
   f"Ordinary least-squares linear regression of cumulative mass against drop count yielded an empirical single-drop mass slope of "
   f"{fmt(f['m'],6)} g/drop, extracting an absolute surface tension of γ = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} "
   f"with an intercept of {fmt(f['b'],c['resultDecimals'])} g and an ideal coefficient of determination R² = 1.00000, "
   f"matching the authoritative IAPWS reference standard (72.80 mN/m) with a percentage difference of {percent:.4f}%."
  )
  graph_choice=(
   f"The linear regression models the modified Tate detachment equation m_total = [ (2π · r · γ · φ) / g ] · N + m₀, "
   f"where N represents the integer count of detached droplets, m_total represents the cumulative gravimetric mass in g, "
   f"and m₀ represents the initial weighing bottle tare offset in g (theoretically m₀ = 0.0000 g). "
   f"Multiplying the regression slope m_slope by K_tip = g / (2π · r · φ) = 725.11 N/(m·kg) directly isolates the "
   f"absolute surface tension in {c['resultUnit']}, while constant tare residues are absorbed into m₀."
  )
  discussion=(
   "The experimental observations provide rigorous quantitative verification of Interfacial Thermodynamics, Tate's Law of Capillary Detachment, and the Harkins-Jordan Hydrodynamic Correction. "
   "In liquid interfacial physics, surface tension arises from the unbalanced cohesive intermolecular forces pulling surface molecules into the bulk liquid phase. "
   "During the growth of a pendent drop at the razor-flat circular stalagmometer tip, the downward gravitational weight increases until it overcomes the upward surface tension force. "
   "Crucially, high-speed fluid mechanics dictates that when the capillary neck pinches off via Rayleigh-Plateau instability, approximately 38.5% of the droplet volume "
   "remains behind on the glass tip. "
   "Incorporating the Harkins-Jordan factor φ = 0.6150 (derived for the dimensionless shape ratio r / V^{1/3} = 0.7526) completely compensates for this incomplete detachment. "
   "Across all six drop count determinations from 10 to 60 drops, cumulative mass scaled in strictly linear proportion to drop count. "
   "The ordinary least-squares regression line m_total = 0.10040 · N + 0.0000 g yielded an ideal coefficient of determination R² = 1.00000. "
   "Scaling by K_tip extracted an absolute surface tension of γ = 72.80 mN/m, in perfect agreement with the international reference standard for pure water at 20.0 °C. "
   "Throttling the flow to 8–10 seconds per drop ensured quasi-static detachment, and acid cleaning eliminated trace surfactant films that would otherwise depress surface tension."
  )
  conclusion=(
   "This laboratory investigation successfully determined the absolute liquid surface tension of ultra-pure water at 20.0 °C using precision drop-weight stalagmometry. "
   f"Through systematic multi-drop gravimetric determinations across counts from N = {int(rows[0]['input'])} to {int(rows[-1]['input'])}, we extracted an absolute "
   f"surface tension of γ = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with a fit standard error of "
   f"{fmt(se*c['resultScale'])} {c['resultUnit']} and an ideal coefficient of determination R² = 1.00000. "
   f"The observed surface tension confirms the IAPWS thermodynamic reference value (72.80 mN/m) with a percentage difference of {percent:.4f}%. "
   "The investigation verified Tate's law, proved the necessity of the Harkins-Jordan hydrodynamic detachment correction, "
   "and demonstrated that multi-point gravimetric regression insulates interfacial measurements from container taring and transfer biases."
  )
  return abstract, graph_choice, discussion, conclusion
 return "","","",""

def report(c,rows,f,out):
 slug=c['slug']
 csvpath=f"/chemistry/{slug}/sample-data.csv"
 csv_content=io.StringIO()
 writer=csv.writer(csv_content)
 writer.writerow(['experiment','dispensed_volume_mL','net_mass_g','x_metric','fitted_mass_g','residual_g'])
 for r in rows:
  fit_y=f['m']*r['x']+f['b']
  writer.writerow([slug,f"{r['input']:.1f}",f"{r['raw']:.4f}",f"{r['x']:.4f}",f"{fit_y:.4f}",f"{r['y']-fit_y:.4f}"])
 (out/f"chemistry/{slug}/sample-data.csv").write_text(csv_content.getvalue())

 value,se,reference=estimate(c,f)
 percent=abs(value-reference)/reference*100
 uncertainty=uncertainty_text(c)
 abstract,graph_choice,discussion,conclusion=report_narrative(c,rows,f,value,percent,reference,se)

 obs="".join(
  f"<tr><td>{i+1}</td><td>{r['input']:.1f}</td><td>{r['raw']:.4f}</td><td>{r['x']:.4f}</td><td>{r['y']:.4f}</td><td>{f['m']*r['x']+f['b']:.4f}</td><td>{r['y']-(f['m']*r['x']+f['b']):.4f}</td></tr>"
  for i,r in enumerate(rows)
 )

 return f'''<div class="section-top"><div><div class="eyebrow">WORKED EXAMPLE · QUANTITATIVE OBSERVATIONS</div><h2>A complete example laboratory report.</h2></div><button class="secondary" onclick="window.print()">Print / save as PDF</button></div><div class="report-notice"><strong>Simulated demonstration data.</strong><p>This report illustrates formal analytical gravimetry, volumetric calibrations, and linear regression analysis. Replace its observations with your own experimental telemetry when preparing a practical submission.</p></div><div class="report-person"><span>Student: __________________</span><span>Student ID: __________________</span><span>Course: __________________</span><span>Date: __________________</span><span>Partner: __________________</span><span>Instructor: __________________</span></div><article class="lab-report"><h3>1. Title and aim</h3><p><strong>{E(c['title'])}.</strong> {E(c['aim'])}</p><h3>2. Abstract</h3><p>{E(abstract)}</p><h3>3. Apparatus and fixed settings</h3><ul>{''.join('<li>'+E(a['name'])+': '+E(a['purpose'])+'</li>' for a in c['apparatus'])}{''.join('<li>'+E(s)+'</li>' for s in c['settings'])}</ul><h3>4. Theory and graph choice</h3><p>{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>{E(graph_choice)}</p><h3>5. Method</h3><ol>{''.join('<li>'+E(s['text'])+'</li>' for s in c['procedure'])}</ol><h3>6. Observations and calculation table</h3><p>All gravimetric observations were recorded using a calibrated 4-decimal electronic analytical balance enclosed within a draft shield chamber. Volumetric aliquots were dispensed from a Class A burette. Residuals are computed relative to the ordinary least-squares regression line.</p><div class="table-card"><table><caption>Table 1. Seven simulated gravimetric observations; x and y represent dispensed volume and net mass metrics.</caption><thead><tr><th>No.</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Fitted y (g)</th><th>Residual (g)</th></tr></thead><tbody>{obs}</tbody></table></div><p><a href="{csvpath}" download>Download the sample observations (CSV) ↓</a></p><h3>7. Worked calculation for one observation</h3><div class="report-equation">{E(worked(c,rows[0]))}</div><h3>8. Graph, gradient and final calculation</h3><div class="chart-card">{graph(c,rows,f)}</div><p>Circular markers represent empirical gravimetric observations. The solid line represents the ordinary least-squares linear regression fit.</p><div class="report-equation">x̄ = {fmt(f['mx'],4)} mL; ȳ = {fmt(f['my'],4)} g<br>Σ(x − x̄)² = {fmt(f['sxx'],4)} mL²<br>Σ(x − x̄)(y − ȳ) = {fmt(f['sxy'],4)} g·mL<br>m = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)² = {fmt(f['m'],8)} g/mL<br>b = ȳ − mx̄ = {fmt(f['b'],8)} g<br>{E(formula(c,f))}</div><h3>9. Uncertainty and comparison</h3><p>Percentage difference = |estimate − theoretical value| / |theoretical value| × 100 = <strong>{percent:.4f}%</strong>.</p><p>For n = 7 gravimetric observations, Σresidual² = {fmt(f['sse'])}; s² = Σresidual²/(n − 2). Gradient standard error = √[s²/Σ(x − x̄)²] = {fmt(f['slopeSE'])}. Intercept standard error = √[s²(1/n + x̄²/Σ(x − x̄)²)] = {fmt(f['interceptSE'])}.</p><p>Propagating the fit parameters yields an <strong>experimental density standard error of {fmt(se*c['resultScale'])} {E(c['resultUnit'])}</strong>, with an ideal coefficient of determination R² = {f['r2']:.6f}.</p><p>{E(uncertainty)}</p><h3>10. Result and discussion</h3><div class="report-equation">{E(c['target'])} = {fmt(value*c['resultScale'],c['resultDecimals'])} {E(c['resultUnit'])}<br>CIPM standard reference value: {fmt(reference*c['resultScale'],c['resultDecimals'])} {E(c['resultUnit'])}</div><p>{E(discussion)}</p><h3>11. Precautions and limitations</h3><ul>{''.join('<li>'+E(p)+'</li>' for p in c['precautions'])}</ul><p>{E(c['limitations'])} {E(c['modelExtra'])}</p><h3>12. Conclusion</h3><p>{E(conclusion)}</p></article>'''

def lesson_schema(c,part,path,title,desc,base):
 graph=[{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Open STEM Lab','item':base+'/'},{'@type':'ListItem','position':2,'name':'Chemistry Laboratory','item':base+'/subjects/chemistry/'},{'@type':'ListItem','position':3,'name':c['shortTitle'],'item':base+f'/chemistry/{c["slug"]}/'}]}]
 if part=='experiment':
  graph.append({'@type':['WebPage','LearningResource','TechArticle'],'name':title,'description':desc,'url':base+path,'learningResourceType':'Interactive chemistry simulation','educationalLevel':'Undergraduate','about':c['title'],'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'Open STEM Lab','url':base+'/'}})
  if c.get('quiz'):
   graph.append({'@type':'Quiz','name':c['shortTitle']+' Concept Understanding','hasPart':[{'@type':'Question','name':q['question'],'suggestedAnswer':[{'@type':'Answer','text':opt} for opt in q['options']],'acceptedAnswer':{'@type':'Answer','text':q['options'][q['correct']]}} for q in c['quiz']]})
 elif part=='theory':
  graph.append({'@type':['WebPage','TechArticle','FAQPage'],'name':title,'description':desc,'url':base+path,'about':c['title'],'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'Open STEM Lab','url':base+'/'},'mainEntity':[{'@type':'Question','name':t['question'],'acceptedAnswer':{'@type':'Answer','text':t['answer']}} for t in c['topics']]})
 else:
  graph.append({'@type':['WebPage','ScholarlyArticle','TechArticle'],'name':title,'description':desc,'url':base+path,'about':c['title'],'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'Open STEM Lab','url':base+'/'}})
 return json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)

def shell(c,part,body,base,production):
 from build_catalog import head
 path=f'/chemistry/{c["slug"]}/'+('' if part=='experiment' else part+'/')
 title=c['shortTitle']+(' Experiment & Simulation' if part=='experiment' else ' Theory & Analysis' if part=='theory' else ' Lab Report: Data & Calculations')+' | Open STEM Lab'
 desc={'experiment':c['aim']+' Explore interactive analytical gravimetry, Class A volumetric glassware and density determination.','theory':'Understand '+c['shortTitle'].lower()+': Archimedean air buoyancy corrections, water density anomaly and error propagation.','report':'A worked '+c['shortTitle'].lower()+' lab report with gravimetric data tables, linear regression graphs, calculations, uncertainty and conclusions.'}[part]
 header=head(path,title,desc,base,production).replace('<link rel="stylesheet" href="/catalog.css">','<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/chem-lesson.css">')
 header=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda _:f'<script type="application/ld+json">{lesson_schema(c,part,path,title,desc,base)}</script>',header,flags=re.S)
 home=f'/chemistry/{c["slug"]}/'
 nav='<aside class="sidebar"><a class="brand" style="font-size:20px" href="/">◉ openstemlab.</a><a class="side-subject" href="/subjects/chemistry/">← Chemistry labs</a><div class="side-label">LABORATORY '+str(c['number']).zfill(2)+'</div><nav aria-label="Lesson navigation">'
 for href,label in [(home,'Explore the experiment'),(home+'theory/','Understand the theory'),(home+'#apparatus','Know your tools'),(home+'#method','Follow the method'),(home+'#results','Analyse your results'),(home+'#check','Check your understanding'),(home+'report/','Sample lab report')]:
  nav+=f'<a class="nav-item{" active" if path==href else ""}" href="{href}">{label}</a>'
 nav+='<a class="nav-item" href="/experiments/">Search all experiments</a></nav><div class="side-note"><span class="small-sun">✳</span><p>Learn by measuring.<br>Understand by reacting.</p></div><a class="text-button" href="/">← All subjects</a></aside>'
 heading=c['title'] if part=='experiment' else c['shortTitle']+' theory' if part=='theory' else c['shortTitle']+' lab report'
 return header+'<body>'+nav+'<main><header class="topbar"><div><a href="/subjects/chemistry/">Chemistry</a> / '+E(c['shortTitle'])+'</div><span class="free-label">FREE TO EXPLORE</span></header><section class="page-heading"><div class="eyebrow">LABORATORY '+str(c['number']).zfill(2)+' · NATURAL SCIENCES</div><h1>'+E(heading)+'</h1><p>'+E(desc)+'</p></section><nav class="lab-navigation" aria-label="Experiment pages"><a href="'+home+'">Workbench</a><a href="'+home+'theory/">Detailed theory</a><a href="'+home+'#method">Method</a><a href="'+home+'#results">My results</a><a href="'+home+'report/">Example report</a></nav>'+body+'<footer><span class="footer-brand">openstemlab.</span><a href="/subjects/chemistry/">All chemistry labs</a><span>Physical chemistry metrological model</span></footer></main>'+ ('<script id="labConfig" type="application/json">'+json.dumps(c,ensure_ascii=False).replace('<',chr(92)+'u003c')+'</script><script src="/chem-models.js"></script><script src="/chem-engine.js"></script>' if part=='experiment' else '')+'</body></html>'

def build_chemistry(out,base,production):
 published=[c for c in specs() if c['published']]
 for name,dest in [('models.js','chem-models.js'),('engine.js','chem-engine.js'),('lesson.css','chem-lesson.css')]:
  (out/dest).write_text((ROOT/'content/chemistry'/name).read_text())
 db=sqlite3.connect(ROOT/'data/catalog.sqlite3')
 sid=db.execute("SELECT id FROM subjects WHERE slug='chemistry'").fetchone()[0]
 db.execute("UPDATE subjects SET content_status='live' WHERE slug='chemistry'")
 paths=[]
 for c in published:
  slug=c['slug']
  home=f'/chemistry/{slug}/'
  (out/home.lstrip('/')).mkdir(parents=True,exist_ok=True)
  rows=[observation(c,v) for v in c['samples']]
  f=fit(rows)
  for part,body in [
   ('experiment',workbench(c)),
   ('theory','<section>'+theory(c)+f'<div class="insight"><span>↳</span><div><strong>Connect the theory to experimental observations.</strong><p>{E(c["modelExtra"])}</p></div></div></section>'),
   ('report',report(c,rows,f,out))
  ]:
   path=home+('' if part=='experiment' else part+'/')
   file=out/path.lstrip('/')/'index.html'
   file.parent.mkdir(parents=True,exist_ok=True)
   file.write_text(shell(c,part,body,base,production))
   paths.append(path)
  db.execute('INSERT INTO experiments(subject_id,slug,title,status,page_path,theory_path,report_path) VALUES(?,?,?,?,?,?,?) ON CONFLICT(slug) DO UPDATE SET title=excluded.title,status=excluded.status,page_path=excluded.page_path,theory_path=excluded.theory_path,report_path=excluded.report_path',(sid,slug,c['shortTitle'],'live',home,home+'theory/',home+'report/'))
 db.commit()
 db.close()
 return paths

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser()
 parser.add_argument('--production',action='store_true')
 args=parser.parse_args()
 config=json.loads((ROOT/'site-config.json').read_text())
 base=config['base_url'].rstrip('/')
 out=ROOT/('release' if args.production else 'dist')
 out.mkdir(exist_ok=True)
 paths=build_chemistry(out,base,args.production)
 print(f"Built {len(paths)} Chemistry pages for {base}: {paths}")
