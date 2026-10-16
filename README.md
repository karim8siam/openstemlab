# Open STEM Lab

Free undergraduate laboratory learning with eleven interactive Physics experiments, detailed theory, step-by-step methods, observation notebooks, graphs, CSV downloads, quizzes and worked reports. Search experiments across departments or within a department. The catalog contains 26 subject collections; subjects without completed lessons are clearly marked as being prepared.

## Run locally

Requires Python 3.10 or newer; no third-party Python packages or Node build step.

```sh
python3 build.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Open [localhost](http://127.0.0.1:8765/), [Physics](http://127.0.0.1:8765/subjects/physics/), or [experiment search](http://127.0.0.1:8765/experiments/).

The first build creates a local SQLite catalog from `data/public-catalog.json`. Generated files and the local database are ignored by Git. A fresh clone needs no private planning data.

## Production build

```sh
python3 build.py --production
```

Deploy the **contents of `release/`** over HTTPS with directory-index support and genuine 404 responses. `dist/` is a localhost preview with `noindex` directives and must not be deployed to production.

The configured production origin is `https://openstemlab.online`, in `site-config.json`. Change this before deploying to another domain. Building does not configure DNS, hosting or Google Search Console.

The sitemap currently contains 36 canonical HTML pages: the homepage, experiment directory, Physics collection and three pages for each of eleven experiments. Planned department pages remain `noindex` and outside the sitemap. Search filtering does not generate indexable query URLs. Lessons and reports are rendered as crawlable HTML, with descriptive titles, canonical URLs and internal links.

After public deployment, verify DNS/HTTPS and every canonical page, verify domain ownership in Google Search Console, and submit `https://openstemlab.online/sitemap.xml`. Submission does not guarantee indexing or rankings.

## Physics experiments

- Photoelectric effect
- Simple pendulum
- Bifilar suspension
- Young’s modulus of a wire
- Stokes’ falling-sphere viscosity
- Convex lens focal length
- Ohm’s law
- Metre bridge
- RC charging time constant
- Glass-slab refractive index
- Diffraction-grating wavelength

## Edit the project

- `content/physics/experiments.json`: ten lesson configurations and original educational text.
- `content/physics/models.js`: numerical models and regression calculations.
- `content/physics/engine.js`: apparatus interactions, local notebooks, plots and quizzes.
- `content/index.template.html`, `content/app.js`, `content/report.html`: original photoelectric lesson.
- `build_physics.py`: static lesson/theory/report generation and reproducible example data.
- `build_catalog.py` and `build_search.py`: public catalog and experiment directory.
- `content/lab-search.js`: filtering by experiment, topic, apparatus and department.
- `build.py`: preview/production generation, metadata, robots.txt and sitemap.xml.

Notebooks are stored in the visitor’s browser. No account or backend service is required. Optional Google Fonts have system-font fallbacks.

## Scientific scope and license

All sample reports use **simulated demonstration observations**, not physical student measurements. The website explains model assumptions, idealisations, scale rounding and uncertainty limits. Fit standard errors are not complete experimental uncertainties. Use real apparatus measurements and appropriate supervision for physical practical work.

Original code and lesson text use the MIT license. Public source downloads contain only public site assets. Private research records, credentials and local hosting identity are excluded from this repository and from the website.
