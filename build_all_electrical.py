# -*- coding: utf-8 -*-
"""Combine all 6 Electrical & Electronics Engineering modules into content/electrical/experiments.json."""
import json, subprocess
from pathlib import Path

from electrical_module_1 import get_module_1
from electrical_module_2 import get_module_2
from electrical_module_3 import get_module_3
from electrical_module_4 import get_module_4
from electrical_module_5 import get_module_5
from electrical_module_6 import get_module_6

ROOT = Path(__file__).resolve().parent

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

    out_file = ROOT / "content/electrical/experiments.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(all_labs, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Successfully wrote {len(all_labs)} labs to {out_file.relative_to(ROOT)}")

    # Verify Node.js model regression consistency
    js_test = """
    const fs = require('fs');
    const models = require('./content/electrical/models.js');
    const configs = JSON.parse(fs.readFileSync('content/electrical/experiments.json', 'utf8'));

    let errors = [];
    configs.forEach(c => {
        try {
            const p = models.predict(c.slug, c.initial);
            if (!p || !p.valid) errors.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => models.reading(c.slug, v, models.predict(c.slug, v).raw));
            const fit = models.fit(rows);
            if (!fit || fit.r2 < 0.999) errors.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = models.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errors.push(c.slug + ': diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errors.push(c.slug + ': exception ' + e.message);
        }
    });

    if (errors.length) {
        console.error(JSON.stringify(errors, null, 2));
        process.exit(1);
    }
    console.log('✓ All 50 Electrical & Electronics Engineering models passed regression tests (R² >= 0.999, dev <= 0.3%).');
    """
    proc = subprocess.run(['node', '-e', js_test], cwd=ROOT, capture_output=True, text=True)
    if proc.returncode != 0:
        print("✗ Node.js regression test FAILED:")
        print(proc.stderr)
        raise RuntimeError("Node.js regression test failed.")
    else:
        print(proc.stdout.strip())

if __name__ == '__main__':
    build_all()
