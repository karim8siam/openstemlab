"""Student reading contract for Open STEM Lab.

Check practical reading sizes and stable paper colors without guessing how
every browser renders the interface. Full mobile/device testing remains separate.
"""
from pathlib import Path
import json, re

ROOT=Path(__file__).resolve().parents[2]
css=(ROOT/"content"/"style.css").read_text(encoding="utf-8")
built=(ROOT/"release"/"style.css").read_text(encoding="utf-8")
assert css == built, "Reader stylesheet in release differs from source"
requirements=[
    ".theory-article p, .theory-article li",
    ".lab-report p, .lab-report li",
    "font-size: 1rem;",
    "line-height: 1.82;",
    "max-width: 78ch;",
    ".report-notice p",
    "@media print"
]
for snippet in requirements:
    assert snippet in css, "Missing accessibility typography rule: "+snippet
assert "--paper:#f7f6f0" in css, "Do not replace warm paper without a reader review"
assert "--ink:#23392f" in css, "Do not replace contrast tokens without review"

def rgb(hexcode):
    return [int(hexcode[i:i+2],16)/255 for i in (1,3,5)]
def luminance(code):
    values=rgb(code)
    converted=[v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in values]
    return 0.2126*converted[0]+0.7152*converted[1]+0.0722*converted[2]
def contrast(one,two):
    a,b=sorted([luminance(one),luminance(two)],reverse=True)
    return round((a+0.05)/(b+0.05),2)
ratios={
    "main_text":contrast("#23392f","#f7f6f0"),
    "report_text":contrast("#526a4d","#f7f6f0")
}
for name,value in ratios.items():
    assert value>=4.5,name+" falls below 4.5:1 body text contrast"
output={
    "background":"#f7f6f0",
    "reader_style":"warm paper, unchanged",
    "body_copy_rule":"1rem / 1.82 line height / 78ch max width",
    "contrast":ratios,
    "note":"Stylesheet static QA, not measured real-device visual usability"
}
dir=ROOT/"audit-results"
dir.mkdir(exist_ok=True)
(dir/"reader-comfort.json").write_text(json.dumps(output,indent=2)+"\n")
print(json.dumps(output,indent=2))
