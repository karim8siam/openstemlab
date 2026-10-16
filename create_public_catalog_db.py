"""Bootstrap a local build database from the public subject projection only."""
from pathlib import Path
import json,sqlite3
ROOT=Path(__file__).resolve().parent

def create_public_catalog():
 target=ROOT/'data/catalog.sqlite3'
 if target.exists():return
 target.parent.mkdir(exist_ok=True)
 with sqlite3.connect(target) as db:
  db.executescript('''
CREATE TABLE subjects (
 id INTEGER PRIMARY KEY, slug TEXT NOT NULL UNIQUE, name TEXT NOT NULL,
 selection_status TEXT NOT NULL, category TEXT NOT NULL, practical_type TEXT NOT NULL,
 display_mode TEXT NOT NULL, example_topics_json TEXT NOT NULL, content_status TEXT NOT NULL);
CREATE TABLE experiments (
 id INTEGER PRIMARY KEY, subject_id INTEGER NOT NULL REFERENCES subjects(id),
 slug TEXT NOT NULL UNIQUE, title TEXT NOT NULL, status TEXT NOT NULL,
 page_path TEXT NOT NULL, theory_path TEXT, report_path TEXT);
''')
  for s in json.loads((ROOT/'data/public-catalog.json').read_text()):
   db.execute('INSERT INTO subjects(slug,name,selection_status,category,practical_type,display_mode,example_topics_json,content_status) VALUES(?,?,?,?,?,?,?,?)',(s['slug'],s['name'],'retain',s['category'],s['practical_type'],s['display_mode'],s['example_topics_json'],s['content_status']))
  sid=db.execute("SELECT id FROM subjects WHERE slug='physics'").fetchone()[0]
  home='/physics/photoelectric-effect/'
  db.execute('INSERT INTO experiments(subject_id,slug,title,status,page_path,theory_path,report_path) VALUES(?,?,?,?,?,?,?)',(sid,'photoelectric-effect','The photoelectric effect','live',home,home+'theory/',home+'report/'))

if __name__=='__main__':create_public_catalog()
