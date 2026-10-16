# OpenLab project requirements

The user prioritizes organic Google Search traffic. Preserve this requirement in all future work.

- Production origin: https://openstemlab.online, configured in site-config.json. Domain selection is not evidence of domain ownership or deployment.
- Follow Google's Search Essentials and official Search Central guidance. Prioritize useful, accurate student content, clear provenance and sources; avoid keyword stuffing, invented credentials and ranking guarantees.
- Educational lessons and worked examples must have crawlable links, distinct descriptive titles, canonical URLs and actual HTML content readable without JavaScript.
- Maintain sitemap.xml with absolute canonical production page URLs. Add new public indexable pages to the builder's pages registry. Exclude fragment states, private notebooks, exports and noncanonical duplicates. Do not invent lastmod dates.
- Keep robots.txt's Sitemap declaration consistent with the production domain. Do not block CSS or JavaScript.
- `python3 build.py` creates a noindex localhost preview in dist/. `python3 build.py --production` creates the indexable release/ directory. Never deploy dist/ to production by mistake.
- Do not claim Search Console verification, sitemap submission, indexing or ranking unless actually verified. Public hosting, HTTPS, DNS and Search Console verification are separate launch steps.
- Sample report observations are SIMULATED. Never label them as real student measurements. Show calculations, uncertainty assumptions and simulator limitations.
- The live experiment and recorded student data remain separate from the static example report.

- User requests no visible book names, bibliography/reference sections, or external reference links anywhere in the website. Keep internal navigation and scientific accepted-value comparisons. Research may still be used internally for accuracy.

## Multisubject catalog

- Public site name is Open STEM Lab, at the same configured origin.
- The user supplied 38 distinct subjects. `data/catalog.sqlite3` stores all decisions: 26 retain, 9 conditional specialist tracks, 3 exclude from initial catalog. These are project-fit decisions, not claims about the worth or total research activity of a field.
- Books and source URLs are INTERNAL ONLY. Never publish the SQLite database, research JSON, evidence URLs, ISBNs or book details under dist/ or release/. No copyrighted book text has been acquired.
- Main website shows only retained subjects. Conditional tracks remain in internal research until the user chooses their narrow scope. Planned lessons must not be represented as existing working simulations.
- `create_catalog_db.py` imports research inputs. `build_catalog.py` generates the public catalog from SQLite using an explicit safe projection. Public data must exclude book fields and evidence.
- The original working physics lesson is `/physics/photoelectric-effect/`, with `/theory/` and `/report/` underneath that experiment path. Old short URLs are noindex aliases; configure actual HTTP 301 redirects at production hosting when possible.
- The homepage and Physics subject page can be indexed in production. Other subject landing pages are currently in preparation, noindex and excluded from sitemap.xml. Enable indexing only when substantive lessons are published.
- Preserve local server operation when the user requests localhost. Do not stop it at task completion.

- Physics now has eleven published lessons, including ten defined in content/physics/experiments.json. Keep database counts, catalog links, generated reports and sitemap synchronized through build_physics.py. All ten added lessons have three canonical pages each; with the experiment directory, total sitemap count is currently 36.

- Maintain global and department experiment search in build_search.py and content/lab-search.js. Search only actual published lessons; never imply planned departments have working experiments. Keep filtered query states out of sitemap; the static /experiments/ directory is indexable in production.
