"""Give related experiments distinct student-facing search titles by subject.

Only affects pages with duplicate <title> values in the generated production
build. Preserves URLs, simulations, sample results, metadata and page text.
"""
from collections import defaultdict
from pathlib import Path
from html import unescape
import re

TITLE = re.compile(r"(<title[^>]*>)(.*?)(</title>)", re.I | re.S)


def disambiguate_titles(output, public_paths):
    by_title = defaultdict(list)
    for route in public_paths:
        filepath = output / route.strip("/") / "index.html"
        if not filepath.exists():
            continue
        html = filepath.read_text(encoding="utf-8")
        match = TITLE.search(html)
        if match:
            by_title[unescape(match.group(2).strip())].append((route, filepath, html, match))
    count = 0
    for title, pages in by_title.items():
        if len(pages) < 2:
            continue
        for route, filepath, html, match in pages:
            chunks = route.strip("/").split("/")
            department = chunks[0].replace("-", " ").title()
            if len(chunks) > 1 and all(p[0].split("/")[1] == chunks[0] for p in pages):
                department += ": " + chunks[1].replace("-", " ").title()
            raw_title = match.group(2)
            if " | " in raw_title:
                beginning, ending = raw_title.rsplit(" | ", 1)
                new_title = beginning + " — " + department + " | " + ending
            else:
                new_title = raw_title + " — " + department
            updated = html[:match.start(2)] + new_title + html[match.end(2):]
            filepath.write_text(updated, encoding="utf-8")
            count += 1
    return count
