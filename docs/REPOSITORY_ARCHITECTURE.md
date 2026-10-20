# Open STEM Lab — source and deployment architecture

This project produces **static public pages**. GitHub tracks the source; Python builds the deployable site; Cloudflare serves HTML. Google does **not** crawl Python files or GitHub folder names.

## Current workflow

```text
content/                      educational templates, models and warm-paper styles
data/public-catalog.json      public experiment catalog (no private planning data)
build.py                      production/preview build orchestrator
build_*.py                    department-specific build modules (legacy root layout)
tooling/seo/                  search metadata and sitemap quality modules
tooling/quality/              student accessibility, source/navigation checks
release/                      generated production HTML, JS, CSS, sitemap
dist/                         generated local preview, deliberately noindex
.github/workflows/            automated checks before releasing changes
```

### Important safety distinction

- `python3 build.py --production` regenerates **release/** with canonical `https://openstemlab.org` URLs.
- `python3 build.py` makes a local **dist/** preview that is `noindex`. Never deploy the preview.
- Keep public URLs such as `/physics/photoelectric-effect/theory/` unchanged when moving Python sources. Google evaluates the delivered page, not the GitHub source path.
- `release/` and much of the older generated site are **currently tracked** in Git. Do not mass-delete or move these pages until the actual Cloudflare build/output settings and published asset parity have been established in a separate migration.
- The `tooling/` move in this release covers the independent SEO/build-audit modules only. The department-specific builders remain at their existing import paths to avoid breaking thousands of pages and student simulations.

## SEO and student quality gates

1. `python3 build.py --production`
2. `python3 tooling/seo/audit_production_content.py`
3. `python3 tooling/quality/verify_navigation.py`
4. `python3 tooling/quality/verify_reader_comfort.py`
5. `python3 tooling/quality/verify_release_integrity.py`

The sitemap includes only the intended public canonical pages. `lastmod` is intentionally omitted until each page has a reliably maintained *significant content update* timestamp; changing a header or running a deployment is not sufficient.

A passing CI run demonstrates build-level route correctness and basic text readability **not** Google Search Console verification, real-world academic correctness, or measured mobile browser performance.

## Safe next restructuring stages

1. Inventory dependencies of the root `build_*.py` modules and distinguish *source generators* from generated website files.
2. Move one independent department builder to `tooling/builders/` with a compatibility import on a branch, then compare **release/** files and canonical routes before and after.
3. If output parity holds, migrate additional builders in small reviewable batches. Do not move `release/` or change Cloudflare output directory during that phase.
4. Only after validating Cloudflare's real production build settings, assess untracking generated files while keeping their production deployment and student access intact.

## Search Console workflow

Use the verified domain property for `openstemlab.org`; submit `https://openstemlab.org/sitemap.xml` once and inspect actual Page indexing exclusions. For any *Discovered – currently not indexed* pages, compare representative pages, sitemap visibility, normal anchor navigation, and content usefulness. Indexing is Google's decision; do not send fake modification dates or promise all 2,713 pages will be indexed.
