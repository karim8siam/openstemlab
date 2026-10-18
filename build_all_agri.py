# -*- coding: utf-8 -*-
"""Assembles all 5 Agricultural Engineering modules into content/agricultural/experiments.json."""
import json
from pathlib import Path
import agri_module_1
import agri_module_2
import agri_module_3
import agri_module_4
import agri_module_5

ROOT = Path(__file__).resolve().parent

MEASURE_LABELS = {
    1: "Log Drawbar Performance",
    2: "Measure Plow Draft Force",
    3: "Acquire Disc Soil Reaction",
    4: "Sample Rotor PTO Torque",
    5: "Collect Seed Mass Discharge",
    6: "Sample Planter Spacing",
    7: "Sample Spray Flow Rate",
    8: "Measure Knife Travel Speed",
    9: "Measure Threshing Efficiency",
    10: "Sample Chaff Separation",
    11: "Log Water Infiltration",
    12: "Measure Darcy Permeation",
    13: "Sample Matric Water Content",
    14: "Log Parshall Flume Head",
    15: "Measure Weir Discharge",
    16: "Sample Pump Shut-Off Head",
    17: "Measure Emitter Flow Rate",
    18: "Record Christiansen Catch",
    19: "Measure Runoff Soil Loss",
    20: "Sample Oven Mass Loss",
    21: "Measure Equilibrium Moisture",
    22: "Sample Grain Moisture Ratio",
    23: "Log Psychrometric Pickup",
    24: "Measure Terminal Velocity",
    25: "Weigh Grain Bulk Volume",
    26: "Measure Angle of Repose",
    27: "Measure Milling Energy",
    28: "Sample Dehusking Ratio",
    29: "Log Lateral Bin Pressure",
    30: "Measure Heat Loss Flux",
    31: "Log Pad Evaporation Rate",
    32: "Sample Respiration Gas Rate",
    33: "Measure Animal Heat Output",
    34: "Measure Ridge Deflection",
    35: "Log Cumulative Biogas",
    36: "Measure Cone Penetration",
    37: "Log Plate Sinkage Pressure",
    38: "Measure Solar Air Efficiency",
    39: "Sample Syngas Heating Value",
    40: "Sample Ester Conversion",
    41: "Measure Hydraulic Water Power",
    42: "Measure Fertilizer Mass Flow"
}

def assemble():
    all_labs = []
    all_labs.extend(agri_module_1.get_module_1())
    all_labs.extend(agri_module_2.get_module_2())
    all_labs.extend(agri_module_3.get_module_3())
    all_labs.extend(agri_module_4.get_module_4())
    all_labs.extend(agri_module_5.get_module_5())

    print(f"Total experiments aggregated: {len(all_labs)}")
    assert len(all_labs) == 42, f"Expected exactly 42 experiments, got {len(all_labs)}"

    slugs = set()
    for lab in all_labs:
        num = lab["number"]
        slug = lab["slug"]
        assert slug not in slugs, f"Duplicate slug: {slug}"
        slugs.add(slug)
        if "measureLabel" not in lab:
            lab["measureLabel"] = MEASURE_LABELS.get(num, "Execute trial")

    out_file = ROOT / "content/agricultural/experiments.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(all_labs, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Successfully wrote {len(all_labs)} experiments to {out_file}")

if __name__ == "__main__":
    assemble()
