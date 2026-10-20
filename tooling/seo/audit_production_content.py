"""Read-only SEO and student-content audit of production build.

Run after: python3 build.py --production. Inspects release/, not the
intentionally noindex local preview dist/.
"""
from collections import Counter, defaultdict
from html import unescape
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "release"
BASE = "https://openstemlab.org/"
if not (OUT / "sitemap.xml").is_file():
    raise SystemExit("Missing production sitemap. Build first.")

tree = ET.parse(OUT / "sitemap.xml")
urls = [x.findtext("{*}loc", "") for x in tree.getroot().findall("{*}url")]
all_titles = defaultdict(list)
missing_files = []
metadata_problems = []
short_pages = []
report_disclosures_missing = []
types = Counter()
sitemap_duplicates = [url for url, count in Counter(urls).items() if count > 1]
h1_re = re.compile(r"<h1\b", re.I)
title_re = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
canonical_re = re.compile(r'<link\b[^>]*rel=["\x27]canonical["\x27][^>]*href=["\x27]([^"\x27]+)', re.I)
robot_re = re.compile(r'<meta\b[^>]*name=["\x27]robots["\x27][^>]*content=["\x27]([^"\x27]+)', re.I)
strip_re = re.compile(r"<[^>]+>")

for url in urls:
    if not url.startswith(BASE) or not url.endswith("/"):
        metadata_problems.append(["noncanonical_sitemap_url", url])
        continue
    rel = url[len(BASE):]
    page = OUT / rel / "index.html"
    if not page.exists():
        missing_files.append(url)
        continue
    content = page.read_text(encoding="utf-8", errors="replace")
    title_match = title_re.search(content)
    title = unescape(title_match.group(1).strip()) if title_match else ""
    if not title:
        metadata_problems.append(["missing_title", url])
    else:
        all_titles[title].append(url)
    canonical = canonical_re.search(content)
    if not canonical or canonical.group(1) != url:
        metadata_problems.append(["bad_canonical", url, canonical.group(1) if canonical else None])
    robots = robot_re.search(content)
    if robots and "noindex" in robots.group(1).lower():
        metadata_problems.append(["noindex_in_sitemap", url])
    if not h1_re.search(content):
        metadata_problems.append(["missing_h1", url])
    text = unescape(strip_re.sub(" ", content))
    if len(text.split()) < 125:
        short_pages.append([url, len(text.split())])
    if "/report/" in url:
        types["report"] += 1
        if not re.search(r"\bsimulat(?:ed|ion|ions|ing)\b", text, re.I):
            report_disclosures_missing.append(url)
    elif "/theory/" in url:
        types["theory"] += 1
    else:
        types["experiment_or_directory"] += 1

dupe_titles = {title: pages[:4] for title, pages in all_titles.items() if len(pages) > 1}
report = {
    "published_sitemap_urls": len(urls),
    "page_types": dict(types),
    "missing_html": missing_files[:25],
    "duplicate_sitemap_url_count": len(sitemap_duplicates),
    "duplicate_title_count": len(dupe_titles),
    "duplicate_title_examples": dict(list(dupe_titles.items())[:15]),
    "metadata_issue_count": len(metadata_problems),
    "metadata_issue_examples": metadata_problems[:25],
    "pages_below_125_words_count": len(short_pages),
    "pages_below_125_words_examples": short_pages[:25],
    "report_pages_missing_simulated_keyword": len(report_disclosures_missing),
    "report_disclosure_examples": report_disclosures_missing[:25],
    "scope": "Repository production-build audit only; not a Google Search Console indexing report."
}
report_file = ROOT / "audit-results" / "production-content.json"
report_file.parent.mkdir(exist_ok=True)
report_file.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
# Do not publish an accidentally broken production sitemap or duplicate titles.
if missing_files or sitemap_duplicates or metadata_problems or dupe_titles:
    raise SystemExit(1)
