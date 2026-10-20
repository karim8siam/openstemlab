"""Verify produced public release and source archive, without modifying pages."""
from pathlib import Path
from zipfile import ZipFile
import json
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"release"
base="https://openstemlab.org"
tree=ET.parse(OUT/"sitemap.xml")
urls=tree.getroot().findall("{*}url")
assert len(urls)>=2500, "Possible accidental mass loss of public experiment pages"
bad_lastmod=sum(e.find("{*}lastmod") is not None for e in urls)
assert bad_lastmod==0, "Do not use unverified blanket lastmod timestamps"
locations=[e.findtext("{*}loc","") for e in urls]
assert len(set(locations))==len(locations), "Duplicate sitemap entries"
assert all(u.startswith(base+"/") for u in locations), "Bad canonical origin"
assert (OUT/"robots.txt").read_text().find(f"Sitemap: {base}/sitemap.xml")>=0
archive=OUT/"openstemlab-source.zip"
assert archive.is_file(),"Public source archive missing"
with ZipFile(archive) as z:
    members=set(z.namelist())
    assert "build.py" in members,"The public source ZIP must remain buildable"
    assert "tooling/seo/disambiguate_titles.py" in members,"Source ZIP missing relocated SEO module"
    assert "content/style.css" in members,"Source ZIP missing reader stylesheet"
home=(OUT/"index.html").read_text(encoding="utf-8")
assert "<title" in home and "noindex" not in home.lower(),"Production home should be indexable"
report={"checked_sitemap_urls":len(urls),"invented_lastmod_tags":bad_lastmod,
        "unique_canonicals":True,"source_zip_has_builder_and_reader_assets":True,
        "production_home_indexable":True}
(ROOT/"audit-results").mkdir(exist_ok=True)
(ROOT/"audit-results"/"release-integrity.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
