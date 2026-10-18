"""Build crawlable HTML and a canonical production sitemap; stdlib only."""
from pathlib import Path
import argparse, json, re, shutil, xml.etree.ElementTree as ET
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--production',action='store_true');args=parser.parse_args()
config=json.loads((ROOT/'site-config.json').read_text());base=config['base_url'].rstrip('/')
assert urlparse(base).scheme=='https' and urlparse(base).netloc and not urlparse(base).path,'Use one HTTPS production origin.'
out=ROOT/('release' if args.production else 'dist');out.mkdir(exist_ok=True)
if not (ROOT/'data/catalog.sqlite3').exists():
 from create_public_catalog_db import create_public_catalog
 create_public_catalog()
source=ROOT/'content';template=(source/'index.template.html').read_text();css=(source/'style.css').read_text()
template=re.sub(r'<section id="report" class="tab-panel">.*?</section>',lambda _: '<section id="report" class="tab-panel">'+(source/'report.html').read_text()+'</section>',template,flags=re.S)
for name in ['style.css','app.js']:(out/name).write_text((source/name).read_text())
shutil.copyfile(source/'sample-report-data.csv',out/'sample-report-data.csv')
# All public content is present in initial HTML. Simulation remains browser-interactive.
sections={m.group(2):m.group(1) for m in re.finditer(r'(<section id="([^"]+)" class="tab-panel[^\"]*".*?</section>)',template,re.S)}
sidebar=re.search(r'<aside class="sidebar">.*?</aside>',template,re.S).group()
sidebar=re.sub(r'<button data-tab="([^"]+)" class="nav-item([^"]*)">(.*?)</button>',lambda m:f'<a href="/#{m[1]}" class="nav-item{m[2]}">{m[3]}</a>',sidebar,flags=re.S)
sidebar=sidebar.replace('href="#experiment"','href="/"')
sidebar=re.sub(r'<b id="readingBadge">.*?</b>','',sidebar)
footer=re.search(r'<footer>.*?</footer>',template,re.S).group()
pages=[('/physics/photoelectric-effect/', 'Photoelectric Effect Experiment & Simulation | OpenLab','Explore the photoelectric effect with an interactive undergraduate experiment, guided stopping-potential measurements and Planck constant analysis.','experiment','The photoelectric effect.'),('/physics/photoelectric-effect/theory/','Photoelectric Effect Theory: Equations & Stopping Potential | OpenLab','Understand photons, work function, threshold frequency, stopping potential and the equations used to determine Planck’s constant.','theory','Photoelectric effect theory'),('/physics/photoelectric-effect/report/','Photoelectric Effect Lab Report: Data, Calculations & Results | OpenLab','A worked photoelectric-effect lab report with simulated observation tables, a stopping-potential graph, calculations of Planck’s constant and uncertainty.','report','Photoelectric effect lab report')]

def head(path,title,desc):
 robots='index,follow' if args.production else 'noindex,follow'
 data={'@context':'https://schema.org','@type':'WebPage','name':title,'description':desc,'url':base+path,'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'OpenLab','url':base+'/'}}
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="{robots}"><meta name="theme-color" content="#f7f6f0"><link rel="canonical" href="{base+path}"><meta property="og:type" content="website"><meta property="og:site_name" content="OpenLab"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{base+path}"><link rel="stylesheet" href="/style.css"><script type="application/ld+json">{json.dumps(data)}</script></head>'''

def lesson_links(text):
 return text.replace('href="/theory/"','href="/physics/photoelectric-effect/theory/"').replace('href="/sample-lab-report/"','href="/physics/photoelectric-effect/report/"').replace('href="/"','href="/physics/photoelectric-effect/"').replace('href="/#','href="/physics/photoelectric-effect/#')

for path,title,desc,key,h1 in pages:
 if key=='experiment':
  body=template[template.index('<body>'):]
  body=body.replace('<link rel="stylesheet" href="style.css">','<link rel="stylesheet" href="/style.css">').replace('src="app.js"','src="/app.js"')
  body=body.replace('<a class="brand" href="#experiment">','<a class="brand" href="/">')
  body=body.replace('<p>When light meets metal, something remarkable happens.','<p>Practise the undergraduate photoelectric effect experiment.<br>When light meets metal, something remarkable happens.')
 else:
  section=sections[key].replace('class="tab-panel"','class="tab-panel active"',1)
  section=section.replace('<button class="text-button back-to-bench">Try it on the workbench →</button>','<a class="text-button" href="/">Try it on the workbench →</a>')
  nav=re.sub(r' class="nav-item active"',' class="nav-item"',sidebar)
  nav=nav.replace('href="'+path+'" class="nav-item"','href="'+path+'" class="nav-item active" aria-current="page"')
  body=f'''<body class="standalone-lesson">{nav}<main><header class="topbar"><div><a href="/">Physics laboratory</a> / {h1}</div><span class="free-label">FREE TO EXPLORE</span></header><section class="page-heading"><div class="eyebrow">PHYSICS · UNDERGRADUATE LABORATORY</div><h1>{h1}</h1><p>{desc}</p><div class="content-links"><a href="/">Interactive experiment</a><a href="/theory/">Theory</a><a href="/sample-lab-report/">Sample report</a></div></section>{section}{footer}</main></body></html>'''
 body=lesson_links(body)
 body=re.sub(r'(<a class="brand" href=")[^"]+',r'\1/',body)
 body=body.replace('<div class="side-label">YOUR OPEN LABORATORY</div>','<a href="/" class="text-button" style="margin-top:18px">← All subjects</a><a href="/experiments/" class="text-button">Search all experiments</a><div class="side-label">YOUR OPEN LABORATORY</div>')
 target=out/path.strip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(head(path,title,desc)+body)
from build_physics import build_physics
physics_urls=build_physics(out,base,args.production)
from build_cs import build_cs
cs_urls=build_cs(out,base,args.production)
from build_chemistry import build_chemistry
chemistry_urls=build_chemistry(out,base,args.production)
from build_math import build_math
math_urls=build_math(out,base,args.production)
from build_stats import build_stats
stats_urls=build_stats(out,base,args.production)
from build_aerospace import build_aerospace
aerospace_urls=build_aerospace(out,base,args.production)
from build_agricultural import build_agricultural
agricultural_urls=build_agricultural(out,base,args.production)
from build_biomedical import build_biomedical
biomedical_urls=build_biomedical(out,base,args.production)
from build_chemeng import build_chemeng
chemeng_urls=build_chemeng(out,base,args.production)
from build_civil import build_civil
civil_urls=build_civil(out,base,args.production)
from build_electrical import build_electrical
electrical_urls=build_electrical(out,base,args.production)
from build_ece import build_ece
ece_urls=build_ece(out,base,args.production)
from build_mechanical import build_mechanical
mechanical_urls=build_mechanical(out,base,args.production)
from build_textile import build_textile
textile_urls=build_textile(out,base,args.production)
from build_archaeology import build_archaeology
archaeology_urls=build_archaeology(out,base,args.production)
from build_geography import build_geography
geography_urls=build_geography(out,base,args.production)
from build_psychology import build_psychology
psychology_urls=build_psychology(out,base,args.production)
from build_agriculture_forestry import build_agriculture_forestry
agriculture_forestry_urls=build_agriculture_forestry(out,base,args.production)
from build_basic_medical_sciences import build_basic_medical_sciences
basic_medical_sciences_urls=build_basic_medical_sciences(out,base,args.production)
from build_biological_sciences import build_biological_sciences
biological_sciences_urls=build_biological_sciences(out,base,args.production)
from build_catalog import build_catalog
catalog_urls=build_catalog(out,base,args.production)
# Keep old report/theory bookmarks working, but exclude aliases from the sitemap.
for old,new in [('/theory/','/physics/photoelectric-effect/theory/'),('/sample-lab-report/','/physics/photoelectric-effect/report/')]:
 target=out/old.strip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
 target.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><link rel="canonical" href="'+base+new+'"><meta http-equiv="refresh" content="0;url='+new+'"><title>Lesson moved | Open STEM Lab</title></head><body><a href="'+new+'">Continue to the lesson</a></body></html>')
ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns);urlset=ET.Element('{'+ns+'}urlset')
seen_paths=set()
for path in [p[0] for p in pages]+physics_urls+cs_urls+chemistry_urls+math_urls+stats_urls+aerospace_urls+agricultural_urls+biomedical_urls+chemeng_urls+civil_urls+electrical_urls+ece_urls+mechanical_urls+textile_urls+archaeology_urls+geography_urls+psychology_urls+agriculture_forestry_urls+basic_medical_sciences_urls+biological_sciences_urls+catalog_urls:
 if path in seen_paths:continue
 seen_paths.add(path)
 url=ET.SubElement(urlset,'{'+ns+'}url')
 ET.SubElement(url,'{'+ns+'}loc').text=base+path
 ET.SubElement(url,'{'+ns+'}lastmod').text='2026-10-17'
 if path in ['/','/experiments/']:
  ET.SubElement(url,'{'+ns+'}changefreq').text='daily'
  ET.SubElement(url,'{'+ns+'}priority').text='1.0'
 elif path.startswith('/subjects/'):
  ET.SubElement(url,'{'+ns+'}changefreq').text='weekly'
  ET.SubElement(url,'{'+ns+'}priority').text='0.9'
 elif path.endswith('/theory/'):
  ET.SubElement(url,'{'+ns+'}changefreq').text='weekly'
  ET.SubElement(url,'{'+ns+'}priority').text='0.8'
 elif path.endswith('/report/'):
  ET.SubElement(url,'{'+ns+'}changefreq').text='monthly'
  ET.SubElement(url,'{'+ns+'}priority').text='0.7'
 else:
  ET.SubElement(url,'{'+ns+'}changefreq').text='weekly'
  ET.SubElement(url,'{'+ns+'}priority').text='0.9'
ET.ElementTree(urlset).write(out/'sitemap.xml',encoding='utf-8',xml_declaration=True)
(out/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+base+'/sitemap.xml\n')
print(('Production' if args.production else 'Local noindex')+' build: '+str(out)+'; '+str(len(seen_paths))+' sitemap URLs for '+base)

from branding import apply_brand
apply_brand(out)

from package_public_source import package_public_source
package_public_source(out)
