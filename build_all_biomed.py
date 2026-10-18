# -*- coding: utf-8 -*-
"""Combine all 5 Biomedical Engineering modules into content/biomedical/experiments.json."""
import json
from pathlib import Path

from biomed_module_1 import get_module_1
from biomed_module_2 import get_module_2
from biomed_module_3 import get_module_3
from biomed_module_4 import get_module_4
from biomed_module_5 import get_module_5

def build_all():
    m1 = get_module_1()
    m2 = get_module_2()
    m3 = get_module_3()
    m4 = get_module_4()
    m5 = get_module_5()

    all_labs = m1 + m2 + m3 + m4 + m5
    print(f"Loaded {len(all_labs)} laboratories across 5 modules:")
    print(f"  Module 1: {len(m1)} labs (1–8)")
    print(f"  Module 2: {len(m2)} labs (9–17)")
    print(f"  Module 3: {len(m3)} labs (18–26)")
    print(f"  Module 4: {len(m4)} labs (27–34)")
    print(f"  Module 5: {len(m5)} labs (35–42)")

    # Verify uniqueness and numbering
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

    out_file = Path("content/biomedical/experiments.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(all_labs, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Successfully saved {len(all_labs)} laboratories to {out_file}")

if __name__ == "__main__":
    build_all()
