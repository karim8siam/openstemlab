"""Shared, accessible Open STEM Lab brand lockup and browser icon."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parent
BRAND_HEAD='<link rel="icon" type="image/svg+xml" href="/brand/logo-mark.svg?v=prism-2"><link rel="stylesheet" href="/brand/brand.css">'
def brand_link():
 return '<a class="brand stem-brand" href="/" aria-label="Open STEM Lab home"><img class="stem-mark" src="/brand/logo-mark.svg?v=prism-2" width="42" height="42" alt=""><span class="stem-wordmark"><span class="stem-name">open<b>STEM</b>lab<i>.</i></span><span class="stem-tagline">LEARN · EXPLORE · DISCOVER</span></span></a>'
def copy_brand(out):
 shutil.copytree(ROOT/'content/brand',out/'brand',dirs_exist_ok=True)


def apply_brand(out):
 import re
 copy_brand(out)
 for file in out.rglob('*.html'):
  text=file.read_text()
  text=re.sub(r'<a class="brand"[^>]*>.*?</a>',lambda _:brand_link(),text,flags=re.S)
  if '/brand/brand.css' not in text:text=text.replace('</head>',BRAND_HEAD+'</head>')
  file.write_text(text)
