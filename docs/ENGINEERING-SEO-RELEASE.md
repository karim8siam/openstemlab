# Open STEM Lab engineering and SEO release guide

## Architecture and where changes belong

| Role | Location |
| --- | --- |
| Subject-specific experiment source | `content/<subject>/` |
| Subject HTML/data generators | `build_*.py` and other build modules |
| Unified page registry, sitemap, robots, release | `build.py` |
| SEO and editorial quality guards | `tooling/seo/` |
| CI checks | `.github/workflows/` |
| Canonical production output | `release/` |

**Important:** The repository currently tracks a large generated `release/` tree in addition to its Python builders. Do not manually restructure or delete generated pages; this may break active hosting, internal links or previews. Changes should first be made in generators, verified with both builds, and only then moved in small batches behind byte/route checks. A future migration can exclude generated files from source control only after confirming hosting rebuilds `release/` on every deployment.

## Release safety checklist

1. Build production with `python3 build.py --production` and verify the result lives in `release/`, not `dist/`.
2. Build local preview with `python3 build.py` and confirm it stays `noindex`.
3. Run `python3 tooling/seo/audit_production_content.py` for sitemap, indexability, canonical tags, unique titles, and student-trust disclosures.
4. Check representative experiment / theory / example report paths across departments, including mobile reading and simulated data labelling.
5. Confirm the live host serves the current output, preserves direct deep-link navigation, and returns genuine 404 responses for missing URLs.
6. Verify the actual sitemap is accessible; submit `https://openstemlab.org/sitemap.xml` to its own Google Search Console property if not already submitted.
7. Judge indexing by Search Console's *Pages* report categories, not by overall excluded count. Do not request indexing for all 2,713 pages individually.
8. Prioritize factual explanations, input labels, simulated-data provenance, comfortable reading width/contrast and mobile controls over generating more URLs.

## SEO evidence boundaries

Automated tests can establish that HTML, canonical tags, titles, sitemap entries, and navigation exist. They cannot determine whether Google will index a URL or whether a simulation is scientifically correct. Google Search Console data and human subject-matter review remain necessary. Preserve subject-specific content and correct faulty information rather than inflating page count.
