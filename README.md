# Open STEM Lab

[![Website Status](https://img.shields.io/website?url=https%3A%2F%2Fopenstemlab.org&label=openstemlab.org)](https://openstemlab.org)
[![Experiments](https://img.shields.io/badge/experiments-894%20interactive-blue)](https://openstemlab.org/experiments/)
[![Faculties](https://img.shields.io/badge/faculties-26%20disciplines-emerald)](https://openstemlab.org/#subjects)
[![Sitemap](https://img.shields.io/badge/canonical%20urls-2%2C713-purple)](https://openstemlab.org/sitemap.xml)
[![Audit](https://img.shields.io/badge/criticism%20engine-100%25%20passed-success)](https://openstemlab.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](LICENSE)

**Open STEM Lab** ([https://openstemlab.org](https://openstemlab.org)) is a free, open-access university laboratory platform featuring **894 interactive simulations, guided experimental methods, observation notebooks, and worked laboratory reports across 26 STEM disciplines**.

The entire platform is built with **zero external dependencies** — running entirely on standard HTML5, Canvas, SVG, and ES6 JavaScript. All student data and lab observations are saved locally in the visitor's browser with zero tracking, zero accounts, and zero paywalls.

---

## 🏛️ 26 Academic Faculties & 894 Completed Labs

| Faculty / Department | Completed Labs | Direct Link |
| :--- | :---: | :--- |
| **Physics** | 62 | [Browse Physics Labs](https://openstemlab.org/subjects/physics/) |
| **Chemistry** | 62 | [Browse Chemistry Labs](https://openstemlab.org/subjects/chemistry/) |
| **Mathematics** | 42 | [Browse Mathematics Labs](https://openstemlab.org/subjects/mathematics/) |
| **Computer Science** | 62 | [Browse Computer Science Labs](https://openstemlab.org/subjects/computer-science/) |
| **Statistics & Probability** | 45 | [Browse Statistics Labs](https://openstemlab.org/subjects/statistics-probability/) |
| **Electrical & Electronics Engineering** | 52 | [Browse Electrical Labs](https://openstemlab.org/subjects/electrical-electronics-engineering/) |
| **Electronics & Communication (ECE)** | 32 | [Browse ECE Labs](https://openstemlab.org/subjects/electronics-communication/) |
| **Mechanical Engineering** | 53 | [Browse Mechanical Labs](https://openstemlab.org/subjects/mechanical-engineering/) |
| **Civil Engineering** | 42 | [Browse Civil Labs](https://openstemlab.org/subjects/civil-engineering/) |
| **Chemical & Process Engineering** | 42 | [Browse Chemical Engineering Labs](https://openstemlab.org/subjects/chemical-process-engineering/) |
| **Aerospace & Aeronautical Engineering** | 22 | [Browse Aerospace Labs](https://openstemlab.org/subjects/aerospace-aeronautical-engineering/) |
| **Biomedical Engineering** | 33 | [Browse Biomedical Labs](https://openstemlab.org/subjects/biomedical-engineering/) |
| **Agricultural Engineering** | 33 | [Browse Agricultural Labs](https://openstemlab.org/subjects/agricultural-engineering/) |
| **Agriculture & Forestry** | 23 | [Browse Agriculture Labs](https://openstemlab.org/subjects/agriculture-forestry/) |
| **Basic Medical Sciences** | 33 | [Browse Medical Labs](https://openstemlab.org/subjects/basic-medical-sciences/) |
| **Biological Sciences** | 23 | [Browse Biology Labs](https://openstemlab.org/subjects/biological-sciences/) |
| **Dentistry & Oral Health** | 23 | [Browse Dentistry Labs](https://openstemlab.org/subjects/dentistry-oral-health/) |
| **Pharmacy & Pharmaceutical Sciences** | 33 | [Browse Pharmacy Labs](https://openstemlab.org/subjects/pharmacy-pharmaceutical-sciences/) |
| **Veterinary Medicine** | 33 | [Browse Veterinary Labs](https://openstemlab.org/subjects/veterinary-medicine/) |
| **Food & Nutrition** | 23 | [Browse Nutrition Labs](https://openstemlab.org/subjects/food-nutrition/) |
| **Earth & Space Sciences** | 23 | [Browse Earth & Space Labs](https://openstemlab.org/subjects/earth-space-sciences/) |
| **Marine & Ocean Sciences** | 23 | [Browse Marine Labs](https://openstemlab.org/subjects/marine-ocean-sciences/) |
| **Textile Engineering** | 34 | [Browse Textile Labs](https://openstemlab.org/subjects/textile-engineering/) |
| **Psychology & Cognitive Science** | 22 | [Browse Psychology Labs](https://openstemlab.org/subjects/psychology/) |
| **Geography & Geospatial Sciences** | 22 | [Browse Geography Labs](https://openstemlab.org/subjects/geography/) |
| **Archaeology & Material Culture** | 22 | [Browse Archaeology Labs](https://openstemlab.org/subjects/archaeology/) |
| **Total Platform** | **894** | [**Search All 894 Experiments**](https://openstemlab.org/experiments/) |

---

## 🔍 SEO & Googlebot Crawler Architecture

The repository is structured following **Google Search Central Guidelines**, **Core Web Vitals standards**, and **W3C canonical practices**:

1. **2,713 Canonical HTML Pages**: Every experiment contains 3 distinct crawlable URLs:
   - `https://openstemlab.org/<subject>/<experiment-slug>/` — Interactive laboratory simulation & observation bench
   - `https://openstemlab.org/<subject>/<experiment-slug>/theory/` — Mathematical derivations, equations, and background theory
   - `https://openstemlab.org/<subject>/<experiment-slug>/report/` — Worked undergraduate lab report with observation tables & analysis
2. **Standard Sitemap (`sitemap.xml`)**:
   - 2,713 URLs declaring canonical `https://openstemlab.org` origins, valid `<lastmod>`, `<changefreq>`, and search `<priority>` weights.
3. **Optimized Crawl Directives (`robots.txt`)**:
   - `Allow: /` for search bots (Googlebot, Bingbot, etc.).
   - Explicitly disallows `/release/`, `/dist/`, `/scratch/`, and `/data/` to conserve Googlebot crawl budget and prevent duplicate content indexing.
   - Declares `Sitemap: https://openstemlab.org/sitemap.xml`.
4. **Cloudflare Pages Canonical Redirects (`_redirects`)**:
   - `301 Permanent Redirects` redirecting `/release/*` to `/:splat` and preserving backwards compatibility for legacy aliases (`/theory/`, `/sample-lab-report/`).
5. **HTTP Response Caching & Security Headers (`_headers`)**:
   - 1-year immutable caching (`max-age=31536000, immutable`) for static assets (`catalog.css`, `style.css`, `*.js`, `brand/*`) to maximize Google PageSpeed / Core Web Vitals score.
   - Strict security headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy: strict-origin-when-cross-origin`.
6. **Real HTTP 404 Handling (`404.html`)**:
   - A branded 404 page that returns a real `404 Not Found` status code to Googlebot (eliminating Soft-404 warnings in Google Search Console) and provides instant recovery navigation across all 26 faculties.
7. **Structured Schema.org JSON-LD**:
   - Every page injects structured `WebPage` and `WebSite` metadata for Google Knowledge Graph and rich search snippets.

---

## 📂 Repository Directory Structure

```text
openstemlab/
├── 404.html                          # Branded error page (returns genuine HTTP 404)
├── _headers                          # Cloudflare Pages Core Web Vitals & security headers
├── _redirects                        # Cloudflare Pages 301 canonical redirects
├── index.html                        # Main platform homepage & faculty showcase
├── robots.txt                        # Search crawler instructions & sitemap reference
├── sitemap.xml                       # 2,713 canonical URLs with lastmod dates
├── site-config.json                  # Production domain origin configuration
├── catalog.css                       # Catalog and faculty styling
├── style.css                         # Core workbench simulation styling
├── lab-search.js                     # Instant client-side search across 894 experiments
├── openstemlab-source.zip            # Public source code archive (~4MB, MIT licensed)
│
├── build.py                          # Primary site build orchestrator (stdlib only)
├── build_<subject>.py                # 26 dedicated faculty static builders
├── build_catalog.py                  # Subject directory and homepage builder
├── build_search.py                   # Global 894-experiment search index generator
├── branding.py                       # Visual identity injector
├── package_public_source.py          # Public source code zip packager
│
├── <subject-directories>/            # 26 faculties (physics/, chemistry/, etc.)
│   └── <experiment-slug>/
│       ├── index.html                # Simulation workbench
│       ├── theory/index.html         # Derivations & equations
│       ├── report/index.html         # Worked lab report
│       └── sample-data.csv           # Experimental demonstration data
│
├── brand/                            # SVG logos, wordmarks, and visual identity
├── content/                          # Templates, base CSS, and core configs
├── data/                             # Public catalog definitions (public-catalog.json)
├── generators/                       # Data seeders & module generation scripts
├── release/                          # Standalone production distribution mirror
└── scripts/
    └── criticism_engine.py           # Automated audit engine (verifies models & 160k links)
```

---

## 🚀 Local Development & Build

Open STEM Lab is engineered to build in under 3 seconds using **Python 3 standard library only** (no `npm`, `pip`, or build frameworks required).

### 1. Build Local Development Preview
```sh
python3 build.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```
Navigate to `http://127.0.0.1:8765/` to preview changes locally with `noindex` headers.

### 2. Build Production Platform
```sh
python3 build.py --production
```
Generates all 2,713 canonical HTML pages, updates `sitemap.xml`, generates `robots.txt`, packages `openstemlab-source.zip`, and syncs production files to the deployment root.

### 3. Run Quality & Integrity Audit
```sh
python3 scripts/criticism_engine.py
```
Validates:
- All 894 mathematical and physical JavaScript simulation models in Node.js.
- 160,000+ internal cross-links across all 2,715 HTML files (verifies 0 broken links).
- Word counts, apparatus items, procedures, and quiz data for every lab.

---

## 🌐 Cloudflare Pages & Server Configuration

Open STEM Lab is deployed on **Cloudflare Pages** backed by the `main` branch of this repository.

- **Production URL**: [https://openstemlab.org](https://openstemlab.org)
- **SSL/TLS**: Universal HTTPS with automatic edge certificate renewal.
- **Routing**: Static directory-index routing handled natively by Cloudflare edge.
- **Permanent Redirects**: Governed by `_redirects` (301 status).
- **Core Web Vitals**: Governed by `_headers` (1-year immutable asset caching).

---

## 📊 Google Search Console Verification

To verify `openstemlab.org` in Google Search Console:

1. **Option A (Recommended — DNS TXT)**:
   - Add the Google verification TXT record to your Cloudflare DNS dashboard (`openstemlab.org`).
2. **Option B (HTML Meta Tag)**:
   - Add `<meta name="google-site-verification" content="YOUR_CODE">` to the `<head>` of `index.html`.
3. **Option C (HTML File)**:
   - Drop your Google verification file (e.g., `google1234567890abcdef.html`) into the repository root.
4. **Submit Sitemap**:
   - Go to **Sitemaps** in Google Search Console and submit:
     `https://openstemlab.org/sitemap.xml`

---

## 🎓 The OpenSTEM Ecosystem

Open STEM Lab is part of the non-profit OpenSTEM educational network:

- **Open STEM Lab**: [openstemlab.org](https://openstemlab.org) — 894 Virtual Laboratories
- **Open STEM Library**: [openstemlibrary.com](https://openstemlibrary.com) — 62 Open-Access University Textbooks
- **Open STEM Field**: [openstemfield.org](https://openstemfield.org) — Field Research & Observational Network
- **Student Community**: [Discord Server](https://discord.com/invite/tBBKtvFJzW) — 24/7 International Study & Research Network

---

## 📜 Scientific Scope & License

- **Simulated Demonstrations**: Sample laboratory reports utilize simulated demonstration observations to teach data analysis, uncertainty treatment, and linear regression without physical apparatus risk.
- **License**: Code, lesson texts, and simulation engines are released under the [MIT License](LICENSE).
