"""Audit student-accessible chapter and experiment navigation from built HTML.

Checks production release/ files, not source folder names. Never edits output.
HTTP 404 and Google indexing are separate: this checks link targets on disk.
"""
from collections import defaultdict, Counter, deque
from html.parser import HTMLParser
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import json, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"release"
SITE="https://openstemlab.org/"
SITEMAP=OUT/"sitemap.xml"
if not SITEMAP.is_file(): raise SystemExit("Build release/ first")

class Anchors(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]
    def handle_starttag(self, tag, attrs):
        if tag=="a":
            url=dict(attrs).get("href")
            if url:self.links.append(url)

pages=set()
for entry in ET.parse(SITEMAP).getroot().findall("{*}url"):
    url=entry.findtext("{*}loc","")
    if url:pages.add(url)
graph=defaultdict(set)
inbound=Counter()
missing=Counter()
links_scanned=0
for page in sorted(pages):
    rel=page[len(SITE):]
    file=OUT/rel/"index.html"
    if not file.is_file():raise SystemExit("Missing sitemap target "+str(file))
    parser=Anchors()
    parser.feed(file.read_text(encoding="utf-8",errors="replace"))
    for raw in parser.links:
        link=raw.strip()
        if not link or link.startswith("#") or link.startswith(("mailto:","tel:","javascript:","data:")):
            continue
        try:
            normalized=urljoin(page,unescape(link))
            parts=urlsplit(normalized)
        except ValueError: continue
        if parts.hostname not in ("openstemlab.org","www.openstemlab.org"):
            continue
        if parts.scheme not in ("http","https"): continue
        dest=unquote(parts.path)
        if not dest.startswith("/") or ".." in dest.split("/"):continue
        canonical=SITE+dest.lstrip("/")
        if canonical in pages:
            graph[page].add(canonical)
            inbound[canonical]+=1
        else:
            test_path=OUT/dest.lstrip("/")
            if not (test_path.is_file() or (test_path/"index.html").is_file()):
                missing[canonical]+=1
        links_scanned+=1
queue=deque([SITE])
reachable=set([SITE])
while queue:
    current=queue.popleft()
    for other in graph[current]:
        if other not in reachable:
            reachable.add(other)
            queue.append(other)
orphan=sorted(p for p in pages if p!=SITE and inbound[p]==0)
unreachable=sorted(p for p in pages if p not in reachable)
report={
    "sitemap_pages":len(pages),
    "internal_link_occurrences":links_scanned,
    "orphans_without_html_inbound":len(orphan),
    "orphans_examples":orphan[:30],
    "unreachable_from_homepage":len(unreachable),
    "unreachable_examples":unreachable[:30],
    "missing_link_target_count":len(missing),
    "missing_link_occurrences":sum(missing.values()),
    "missing_targets":[{"url":x,"count":n} for x,n in missing.most_common(30)],
    "note":"Repo HTML graph only. Does not check live HTTP, robots, actual Google indexing, or JS-generated links."
}
output=ROOT/"audit-results"/"reader-navigation.json"
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
