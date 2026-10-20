"""Correct unsupported claims in generated *simulated* lab reports.

The generator supplies example data for teaching, not independently measured,
calibrated laboratory observations. Keep student copy unambiguous in all subjects.
"""
from pathlib import Path

OLD = '<span><strong>Status:</strong> Calibrated &amp; Verified</span>'
NEW = '<span><strong>Data provenance:</strong> Simulated teaching example — not independently verified physical measurements</span>'

def clarify_reports(out: Path) -> int:
    count = 0
    for page in out.rglob('report/index.html'):
        html = page.read_text(encoding='utf-8')
        if OLD not in html:
            continue
        updated = html.replace(OLD, NEW)
        page.write_text(updated, encoding='utf-8')
        count += html.count(OLD)
    return count
