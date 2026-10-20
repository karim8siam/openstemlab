# -*- coding: utf-8 -*-
"""Combine all 6 Civil Engineering modules into content/civil/experiments.json."""
import json
from pathlib import Path

from civil_module_1 import get_module_1
from civil_module_2 import get_module_2
from civil_module_3 import get_module_3
from civil_module_4 import get_module_4
from civil_module_5 import get_module_5
from civil_module_6 import get_module_6

def build_all():
    m1 = get_module_1()
    m2 = get_module_2()
    m3 = get_module_3()
    m4 = get_module_4()
    m5 = get_module_5()
    m6 = get_module_6()

    all_labs = m1 + m2 + m3 + m4 + m5 + m6
    print(f"Loaded {len(all_labs)} laboratories across 6 modules:")
    print(f"  Module 1: {len(m1)} labs (1–9)")
    print(f"  Module 2: {len(m2)} labs (10–18)")
    print(f"  Module 3: {len(m3)} labs (19–27)")
    print(f"  Module 4: {len(m4)} labs (28–36)")
    print(f"  Module 5: {len(m5)} labs (37–43)")
    print(f"  Module 6: {len(m6)} labs (44–50)")

    assert len(all_labs) == 50, f"Expected 50 labs, got {len(all_labs)}"

    slugs = set()
    for idx, lab in enumerate(all_labs, 1):
        assert lab["number"] == idx, f"Lab number mismatch: expected {idx}, got {lab['number']}"
        assert lab["slug"] not in slugs, f"Duplicate slug: {lab['slug']}"
        slugs.add(lab["slug"])
        assert len(lab.get("samples", [])) >= 5, f"Insufficient samples in {lab['slug']}"
        assert len(lab.get("apparatus", [])) >= 4, f"Insufficient apparatus in {lab['slug']}"
        assert len(lab.get("procedure", [])) >= 6, f"Insufficient procedure in {lab['slug']}"
        assert len(lab.get("topics", [])) >= 6, f"Insufficient topics in {lab['slug']}"
        assert len(lab.get("precautions", [])) >= 4, f"Insufficient precautions in {lab['slug']}"
        assert len(lab.get("quiz", [])) >= 3, f"Insufficient quiz in {lab['slug']}"
        for s in range(1, 13):
            assert f"<h3>{s}. " in lab["report"], f"Missing section {s} in {lab['slug']}"
        assert "Simulated demonstration data." in lab["report"], f"Missing demo disclaimer in {lab['slug']}"

        lab["published"] = True
        if "settings" not in lab:
            lab["settings"] = [
                f"Civil Engineering Material / Medium: Standard certified structural testing standard at 20.0 °C",
                f"Telemetry: Calibrated high-precision structural transducers (±0.1% accuracy)",
                f"Equilibrium: Steady-state laboratory mechanical stabilization"
            ]
        if "limitations" not in lab:
            lab["limitations"] = [
                f"The civil engineering physical models apply within the specified calibrated operational window ({lab['min']} to {lab['max']} {lab['inputUnit']}).",
                f"Assumes homogeneous, isotropic continuum material behavior without unmodeled micro-fracture anomalies.",
                f"Continuous sensor readings reflect ordinary least-squares regression across successive observations.",
                f"Extreme inelastic yielding or cyclic degradation requires non-linear constitutive continuum damage mechanics."
            ]
        if "simModes" not in lab:
            lab["simModes"] = [
                {"id": "bench", "icon": "🏗️", "label": f"1. {lab['shortTitle']} Bench"},
                {"id": "compare", "icon": "📊", "label": "2. Comparative Telemetry"},
                {"id": "sandbox", "icon": "⚡", "label": "3. Structural Dynamics Sandbox"}
            ]

    out_file = Path("content/civil/experiments.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(all_labs, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Successfully saved {len(all_labs)} laboratories to {out_file}")

if __name__ == "__main__":
    build_all()
