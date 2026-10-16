"""Package only the built public website for the on-site source download."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parent

def package_public_source(directory):
 with zipfile.ZipFile(directory/'openstemlab-source.zip','w',zipfile.ZIP_DEFLATED) as archive:
  for file in sorted(directory.rglob('*')):
   if file.is_file() and file.suffix in {'.html','.css','.js','.json','.csv','.xml','.txt'}:
    archive.write(file,file.relative_to(directory))
  archive.write(ROOT/'LICENSE','LICENSE')
  archive.writestr('README.txt','Open STEM Lab — editable public website.\nServe this folder with python3 -m http.server 8000.\nOriginal code and lesson text are MIT licensed; external fonts retain their own licenses.\n')
