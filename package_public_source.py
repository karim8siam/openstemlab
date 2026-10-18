"""Package only the built public website for the on-site source download."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parent

def package_public_source(directory):
 with zipfile.ZipFile(directory/'openstemlab-source.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
  for py in sorted(ROOT.glob('*.py')):
   archive.write(py,py.name)
  for ext in ['*.json','*.md','LICENSE']:
   for f in sorted(ROOT.glob(ext)):
    archive.write(f,f.name)
  for f in sorted((ROOT/'content').rglob('*')):
   if f.is_file():
    archive.write(f,str(f.relative_to(ROOT)))
  archive.writestr('README.txt','Open STEM Lab — source repository.\nRun python3 build.py --production to generate the full static platform.\nOriginal code and lesson text are MIT licensed.\n')
