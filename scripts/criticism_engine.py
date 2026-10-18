#!/usr/bin/env python3
"""
Open STEM Lab Criticism Engine
Automated benchmark and regression audit system that evaluates newly added
laboratory experiments against historical gold-standard benchmarks across
mathematics, content depth, interactive simulation, SEO, and link integrity.
"""

import sys, json, re, math, sqlite3, subprocess
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent

def run_audit(target_slugs=None, verbose=True):
    configs = json.loads((ROOT / 'content/physics/experiments.json').read_text())
    for c in configs: c['subject'] = 'physics'
    if (ROOT / 'content/cs/experiments.json').exists():
        cs_configs = json.loads((ROOT / 'content/cs/experiments.json').read_text())
        for c in cs_configs: c['subject'] = 'computer-science'
        configs.extend(cs_configs)
    if (ROOT / 'content/chemistry/experiments.json').exists():
        chem_configs = json.loads((ROOT / 'content/chemistry/experiments.json').read_text())
        for c in chem_configs: c['subject'] = 'chemistry'
        configs.extend(chem_configs)
    if (ROOT / 'content/math/experiments.json').exists():
        math_configs = json.loads((ROOT / 'content/math/experiments.json').read_text())
        for c in math_configs: c['subject'] = 'mathematics'
        configs.extend(math_configs)
    if (ROOT / 'content/stats/experiments.json').exists():
        stats_configs = json.loads((ROOT / 'content/stats/experiments.json').read_text())
        for c in stats_configs: c['subject'] = 'statistics-probability'
        configs.extend(stats_configs)
    if (ROOT / 'content/aerospace/experiments.json').exists():
        aero_configs = json.loads((ROOT / 'content/aerospace/experiments.json').read_text())
        for c in aero_configs: c['subject'] = 'aerospace-aeronautical-engineering'
        configs.extend(aero_configs)
    if (ROOT / 'content/agricultural/experiments.json').exists():
        agri_configs = json.loads((ROOT / 'content/agricultural/experiments.json').read_text())
        for c in agri_configs: c['subject'] = 'agricultural-engineering'
        configs.extend(agri_configs)
    if (ROOT / 'content/biomedical/experiments.json').exists():
        biomed_configs = json.loads((ROOT / 'content/biomedical/experiments.json').read_text())
        for c in biomed_configs: c['subject'] = 'biomedical-engineering'
        configs.extend(biomed_configs)
    if (ROOT / 'content/chemeng/experiments.json').exists():
        chemeng_configs = json.loads((ROOT / 'content/chemeng/experiments.json').read_text())
        for c in chemeng_configs: c['subject'] = 'chemical-process-engineering'
        configs.extend(chemeng_configs)
    if (ROOT / 'content/civil/experiments.json').exists():
        civil_configs = json.loads((ROOT / 'content/civil/experiments.json').read_text())
        for c in civil_configs: c['subject'] = 'civil-engineering'
        configs.extend(civil_configs)
    if (ROOT / 'content/electrical/experiments.json').exists():
        electrical_configs = json.loads((ROOT / 'content/electrical/experiments.json').read_text())
        for c in electrical_configs: c['subject'] = 'electrical-electronics-engineering'
        configs.extend(electrical_configs)
    if (ROOT / 'content/ece/experiments.json').exists():
        ece_configs = json.loads((ROOT / 'content/ece/experiments.json').read_text())
        for c in ece_configs: c['subject'] = 'electronics-communication'
        configs.extend(ece_configs)
    if (ROOT / 'content/mechanical/experiments.json').exists():
        mechanical_configs = json.loads((ROOT / 'content/mechanical/experiments.json').read_text())
        for c in mechanical_configs: c['subject'] = 'mechanical-engineering'
        configs.extend(mechanical_configs)
    if (ROOT / 'content/textile/experiments.json').exists():
        textile_configs = json.loads((ROOT / 'content/textile/experiments.json').read_text())
        for c in textile_configs: c['subject'] = 'textile-engineering'
        configs.extend(textile_configs)
    if (ROOT / 'content/archaeology/experiments.json').exists():
        archaeology_configs = json.loads((ROOT / 'content/archaeology/experiments.json').read_text())
        for c in archaeology_configs: c['subject'] = 'archaeology'
        configs.extend(archaeology_configs)
    if (ROOT / 'content/geography/experiments.json').exists():
        geography_configs = json.loads((ROOT / 'content/geography/experiments.json').read_text())
        for c in geography_configs: c['subject'] = 'geography'
        configs.extend(geography_configs)
    if (ROOT / 'content/psychology/experiments.json').exists():
        psychology_configs = json.loads((ROOT / 'content/psychology/experiments.json').read_text())
        for c in psychology_configs: c['subject'] = 'psychology'
        configs.extend(psychology_configs)
    if (ROOT / 'content/agriculture_forestry/experiments.json').exists():
        agriculture_forestry_configs = json.loads((ROOT / 'content/agriculture_forestry/experiments.json').read_text())
        for c in agriculture_forestry_configs: c['subject'] = 'agriculture-forestry'
        configs.extend(agriculture_forestry_configs)
    if (ROOT / 'content/basic_medical_sciences/experiments.json').exists():
        basic_medical_sciences_configs = json.loads((ROOT / 'content/basic_medical_sciences/experiments.json').read_text())
        for c in basic_medical_sciences_configs: c['subject'] = 'basic-medical-sciences'
        configs.extend(basic_medical_sciences_configs)
    if (ROOT / 'content/biological_sciences/experiments.json').exists():
        biological_sciences_configs = json.loads((ROOT / 'content/biological_sciences/experiments.json').read_text())
        for c in biological_sciences_configs: c['subject'] = 'biological-sciences'
        configs.extend(biological_sciences_configs)
    if (ROOT / 'content/dentistry_oral_health/experiments.json').exists():
        dentistry_oral_health_configs = json.loads((ROOT / 'content/dentistry_oral_health/experiments.json').read_text())
        for c in dentistry_oral_health_configs: c['subject'] = 'dentistry-oral-health'
        configs.extend(dentistry_oral_health_configs)
    if (ROOT / 'content/food_nutrition/experiments.json').exists():
        food_nutrition_configs = json.loads((ROOT / 'content/food_nutrition/experiments.json').read_text())
        for c in food_nutrition_configs: c['subject'] = 'food-nutrition'
        configs.extend(food_nutrition_configs)
    if (ROOT / 'content/pharmacy_pharmaceutical_sciences/experiments.json').exists():
        pharmacy_pharmaceutical_sciences_configs = json.loads((ROOT / 'content/pharmacy_pharmaceutical_sciences/experiments.json').read_text())
        for c in pharmacy_pharmaceutical_sciences_configs: c['subject'] = 'pharmacy-pharmaceutical-sciences'
        configs.extend(pharmacy_pharmaceutical_sciences_configs)
    if (ROOT / 'content/veterinary_medicine/experiments.json').exists():
        veterinary_medicine_configs = json.loads((ROOT / 'content/veterinary_medicine/experiments.json').read_text())
        for c in veterinary_medicine_configs: c['subject'] = 'veterinary-medicine'
        configs.extend(veterinary_medicine_configs)
    if (ROOT / 'content/earth_space_sciences/experiments.json').exists():
        earth_space_sciences_configs = json.loads((ROOT / 'content/earth_space_sciences/experiments.json').read_text())
        for c in earth_space_sciences_configs: c['subject'] = 'earth-space-sciences'
        configs.extend(earth_space_sciences_configs)
    if (ROOT / 'content/marine_ocean_sciences/experiments.json').exists():
        marine_ocean_sciences_configs = json.loads((ROOT / 'content/marine_ocean_sciences/experiments.json').read_text())
        for c in marine_ocean_sciences_configs: c['subject'] = 'marine-ocean-sciences'
        configs.extend(marine_ocean_sciences_configs)
    
    # Identify benchmarks vs new targets
    known_benchmarks = [
        'simple-pendulum', 'bifilar-suspension', 'young-modulus',
        'stokes-viscosity', 'convex-lens', 'ohms-law', 'metre-bridge',
        'rc-charging', 'glass-slab', 'diffraction-grating'
    ]
    
    if target_slugs:
        test_configs = [c for c in configs if c['slug'] in target_slugs]
    else:
        test_configs = configs

    db = sqlite3.connect(ROOT / 'data/catalog.sqlite3')
    db_slugs = {row[0] for row in db.execute("SELECT slug FROM experiments WHERE status='live'")}
    db.close()

    search_code = (ROOT / 'build_search.py').read_text()
    aliases_match = re.search(r'aliases\s*=\s*({[^}]+})', search_code, re.S)
    aliases = eval(aliases_match.group(1)) if aliases_match else {}

    dist_sitemap = (ROOT / 'dist/sitemap.xml').read_text() if (ROOT / 'dist/sitemap.xml').exists() else ''
    release_sitemap = (ROOT / 'release/sitemap.xml').read_text() if (ROOT / 'release/sitemap.xml').exists() else ''

    def word_count(p):
        if not p.exists(): return 0
        clean = re.sub(r'<[^>]+>', ' ', p.read_text())
        return len(clean.split())

    overall_passed = True
    audit_results = []

    print('======================================================================')
    print('                    OPEN STEM LAB CRITICISM ENGINE                    ')
    print('======================================================================')

    for c in test_configs:
        slug = c['slug']
        is_bench = slug in known_benchmarks
        tag = '[BENCHMARK]' if is_bench else '[AUDIT TARGET]'
        failures = []
        metrics = {}

        # 1. Artifacts existence
        sub = c.get('subject', 'physics')
        pages_dist = [
            ROOT / f'dist/{sub}/{slug}/index.html',
            ROOT / f'dist/{sub}/{slug}/theory/index.html',
            ROOT / f'dist/{sub}/{slug}/report/index.html',
            ROOT / f'dist/{sub}/{slug}/sample-data.csv'
        ]
        pages_rel = [
            ROOT / f'release/{sub}/{slug}/index.html',
            ROOT / f'release/{sub}/{slug}/theory/index.html',
            ROOT / f'release/{sub}/{slug}/report/index.html',
            ROOT / f'release/{sub}/{slug}/sample-data.csv'
        ]
        missing_dist = [str(p.relative_to(ROOT)) for p in pages_dist if not p.exists()]
        missing_rel = [str(p.relative_to(ROOT)) for p in pages_rel if not p.exists()]
        if missing_dist or missing_rel:
            failures.append(f'Missing artifacts: dist={missing_dist}, rel={missing_rel}')

        # 2. Word Counts vs Benchmark Thresholds
        wb_w = word_count(pages_dist[0])
        th_w = word_count(pages_dist[1])
        rp_w = word_count(pages_dist[2])
        tot_w = wb_w + th_w + rp_w
        metrics['word_count'] = {'workbench': wb_w, 'theory': th_w, 'report': rp_w, 'total': tot_w}

        if wb_w < 2000:
            failures.append(f'Workbench word count too low: {wb_w} < 2000')
        if th_w < 700:
            failures.append(f'Theory word count too low: {th_w} < 700')
        if rp_w < 1100:
            failures.append(f'Report word count too low: {rp_w} < 1100')
        if tot_w < 4000:
            failures.append(f'Total module word count too low: {tot_w} < 4000')

        # 3. 12 Report Sections
        if pages_dist[2].exists():
            report_text = pages_dist[2].read_text()
            missing_secs = [f'Section {i}' for i in range(1, 13) if f'<h3>{i}. ' not in report_text]
            if missing_secs:
                failures.append(f'Missing worked report sections: {missing_secs}')
            if 'Simulated demonstration data.' not in report_text:
                failures.append('Missing simulated demonstration data disclaimer')

        # 4. Content Structure
        app_count = len(c.get('apparatus', []))
        proc_count = len(c.get('procedure', []))
        top_count = len(c.get('topics', []))
        prec_count = len(c.get('precautions', []))
        quiz_count = len(c.get('quiz', []))
        samp_count = len(c.get('samples', []))
        metrics['counts'] = {'apparatus': app_count, 'procedure': proc_count, 'topics': top_count, 'quiz': quiz_count}

        if app_count < 4: failures.append(f'Apparatus count {app_count} < 4')
        if proc_count < 6: failures.append(f'Procedure steps count {proc_count} < 6')
        if top_count < 6: failures.append(f'Topics count {top_count} < 6')
        if prec_count < 4: failures.append(f'Precautions count {prec_count} < 4')
        if quiz_count < 3: failures.append(f'Quiz questions count {quiz_count} < 3')
        if samp_count < 5: failures.append(f'Observation samples {samp_count} < 5')

        # Check quiz validity
        for idx, q in enumerate(c.get('quiz', [])):
            if not (0 <= q.get('correct', -1) < len(q.get('options', []))):
                failures.append(f'Quiz question {idx} has invalid correct index')

        # Check Viva Q&A
        for idx, t in enumerate(c.get('topics', [])):
            if not t.get('question') or not t.get('answer'):
                failures.append(f'Topic {idx} missing Viva Q&A')

        # 5. Database and Search Integration
        if slug not in db_slugs:
            failures.append('Not found in catalog.sqlite3 live experiments')
        if slug not in aliases or len(aliases[slug].split()) < 3:
            failures.append('Missing or insufficient keywords in build_search.py aliases')

        # 6. Sitemap & SEO
        canon = f'https://openstemlab.online/{sub}/{slug}/'
        if canon not in dist_sitemap or f'{canon}theory/' not in dist_sitemap or f'{canon}report/' not in dist_sitemap:
            failures.append('Canonical URLs missing from dist/sitemap.xml')
        if canon not in release_sitemap or f'{canon}theory/' not in release_sitemap or f'{canon}report/' not in release_sitemap:
            failures.append('Canonical URLs missing from release/sitemap.xml')

        if pages_rel[0].exists():
            rel_html = pages_rel[0].read_text()
            if '<meta name="robots" content="index,follow">' not in rel_html:
                failures.append('Release workbench missing robots="index,follow"')
            if f'<link rel="canonical" href="{canon}">' not in rel_html:
                failures.append(f'Release workbench missing canonical link to {canon}')

        # 7. Privacy check: No external book titles/ISBNs in public release
        for p in pages_rel[:3]:
            if p.exists():
                text = p.read_text().lower()
                for forbidden in ['knowlton', 'william watson', 'mcgraw-hill', 'isbn', 'pypdf']:
                    if forbidden in text:
                        failures.append(f'Public page {p.name} contains forbidden reference: "{forbidden}"')

        status = 'PASSED' if not failures else 'FAILED'
        if failures: overall_passed = False

        audit_results.append({
            'slug': slug,
            'status': status,
            'is_bench': is_bench,
            'failures': failures,
            'metrics': metrics
        })

        if verbose:
            stat_icon = '✓' if status == 'PASSED' else '✗'
            print(f'{stat_icon} {tag:14s} {slug:22s} : {status}')
            if failures:
                for f in failures:
                    print(f'    - Issue: {f}')
            else:
                print(f'    - Words: Bench {wb_w} | Theory {th_w} | Report {rp_w} | Total: {tot_w}')
                print(f'    - Content: {app_count} apparatus | {proc_count} steps | {top_count} topics | {quiz_count} quiz')

    # Run JS model tests
    print('\n----------------------------------------------------------------------')
    print('Testing Mathematical & Algorithmic Model Consistency in Node.js...')
    js_test_code = """
    const fs = require('fs');
    const physModels = require('./content/physics/models.js');
    const physConfigs = JSON.parse(fs.readFileSync('content/physics/experiments.json', 'utf8'));
    let csModels = null, csConfigs = [];
    if (fs.existsSync('content/cs/experiments.json') && fs.existsSync('content/cs/models.js')) {
        csModels = require('./content/cs/models.js');
        csConfigs = JSON.parse(fs.readFileSync('content/cs/experiments.json', 'utf8'));
    }
    let chemModels = null, chemConfigs = [];
    if (fs.existsSync('content/chemistry/experiments.json') && fs.existsSync('content/chemistry/models.js')) {
        chemModels = require('./content/chemistry/models.js');
        chemConfigs = JSON.parse(fs.readFileSync('content/chemistry/experiments.json', 'utf8'));
    }
    let mathModels = null, mathConfigs = [];
    if (fs.existsSync('content/math/experiments.json') && fs.existsSync('content/math/models.js')) {
        mathModels = require('./content/math/models.js');
        mathConfigs = JSON.parse(fs.readFileSync('content/math/experiments.json', 'utf8'));
    }
    let statsModels = null, statsConfigs = [];
    if (fs.existsSync('content/stats/experiments.json') && fs.existsSync('content/stats/models.js')) {
        statsModels = require('./content/stats/models.js');
        statsConfigs = JSON.parse(fs.readFileSync('content/stats/experiments.json', 'utf8'));
    }
    let aeroModels = null, aeroConfigs = [];
    if (fs.existsSync('content/aerospace/experiments.json') && fs.existsSync('content/aerospace/models.js')) {
        aeroModels = require('./content/aerospace/models.js');
        aeroConfigs = JSON.parse(fs.readFileSync('content/aerospace/experiments.json', 'utf8'));
    }
    let agriModels = null, agriConfigs = [];
    if (fs.existsSync('content/agricultural/experiments.json') && fs.existsSync('content/agricultural/models.js')) {
        agriModels = require('./content/agricultural/models.js');
        agriConfigs = JSON.parse(fs.readFileSync('content/agricultural/experiments.json', 'utf8'));
    }
    let biomedModels = null, biomedConfigs = [];
    if (fs.existsSync('content/biomedical/experiments.json') && fs.existsSync('content/biomedical/models.js')) {
        biomedModels = require('./content/biomedical/models.js');
        biomedConfigs = JSON.parse(fs.readFileSync('content/biomedical/experiments.json', 'utf8'));
    }
    let chemengModels = null, chemengConfigs = [];
    if (fs.existsSync('content/chemeng/experiments.json') && fs.existsSync('content/chemeng/models.js')) {
        chemengModels = require('./content/chemeng/models.js');
        chemengConfigs = JSON.parse(fs.readFileSync('content/chemeng/experiments.json', 'utf8'));
    }
    let civilModels = null, civilConfigs = [];
    if (fs.existsSync('content/civil/experiments.json') && fs.existsSync('content/civil/models.js')) {
        civilModels = require('./content/civil/models.js');
        civilConfigs = JSON.parse(fs.readFileSync('content/civil/experiments.json', 'utf8'));
    }
    let electricalModels = null, electricalConfigs = [];
    if (fs.existsSync('content/electrical/experiments.json') && fs.existsSync('content/electrical/models.js')) {
        electricalModels = require('./content/electrical/models.js');
        electricalConfigs = JSON.parse(fs.readFileSync('content/electrical/experiments.json', 'utf8'));
    }
    let eceModels = null, eceConfigs = [];
    if (fs.existsSync('content/ece/experiments.json') && fs.existsSync('content/ece/models.js')) {
        eceModels = require('./content/ece/models.js');
        eceConfigs = JSON.parse(fs.readFileSync('content/ece/experiments.json', 'utf8'));
    }
    let mechanicalModels = null, mechanicalConfigs = [];
    if (fs.existsSync('content/mechanical/experiments.json') && fs.existsSync('content/mechanical/models.js')) {
        mechanicalModels = require('./content/mechanical/models.js');
        mechanicalConfigs = JSON.parse(fs.readFileSync('content/mechanical/experiments.json', 'utf8'));
    }
    let textileModels = null, textileConfigs = [];
    if (fs.existsSync('content/textile/experiments.json') && fs.existsSync('content/textile/models.js')) {
        textileModels = require('./content/textile/models.js');
        textileConfigs = JSON.parse(fs.readFileSync('content/textile/experiments.json', 'utf8'));
    }
    let archaeologyModels = null, archaeologyConfigs = [];
    if (fs.existsSync('content/archaeology/experiments.json') && fs.existsSync('content/archaeology/models.js')) {
        archaeologyModels = require('./content/archaeology/models.js');
        archaeologyConfigs = JSON.parse(fs.readFileSync('content/archaeology/experiments.json', 'utf8'));
    }
    let geographyModels = null, geographyConfigs = [];
    if (fs.existsSync('content/geography/experiments.json') && fs.existsSync('content/geography/models.js')) {
        geographyModels = require('./content/geography/models.js');
        geographyConfigs = JSON.parse(fs.readFileSync('content/geography/experiments.json', 'utf8'));
    }
    let psychologyModels = null, psychologyConfigs = [];
    if (fs.existsSync('content/psychology/experiments.json') && fs.existsSync('content/psychology/models.js')) {
        psychologyModels = require('./content/psychology/models.js');
        psychologyConfigs = JSON.parse(fs.readFileSync('content/psychology/experiments.json', 'utf8'));
    }
    let agricultureForestryModels = null, agricultureForestryConfigs = [];
    if (fs.existsSync('content/agriculture_forestry/experiments.json') && fs.existsSync('content/agriculture_forestry/models.js')) {
        agricultureForestryModels = require('./content/agriculture_forestry/models.js');
        agricultureForestryConfigs = JSON.parse(fs.readFileSync('content/agriculture_forestry/experiments.json', 'utf8'));
    }
    let basicMedicalSciencesModels = null, basicMedicalSciencesConfigs = [];
    if (fs.existsSync('content/basic_medical_sciences/experiments.json') && fs.existsSync('content/basic_medical_sciences/models.js')) {
        basicMedicalSciencesModels = require('./content/basic_medical_sciences/models.js');
        basicMedicalSciencesConfigs = JSON.parse(fs.readFileSync('content/basic_medical_sciences/experiments.json', 'utf8'));
    }
    let biologicalSciencesModels = null, biologicalSciencesConfigs = [];
    if (fs.existsSync('content/biological_sciences/experiments.json') && fs.existsSync('content/biological_sciences/models.js')) {
        biologicalSciencesModels = require('./content/biological_sciences/models.js');
        biologicalSciencesConfigs = JSON.parse(fs.readFileSync('content/biological_sciences/experiments.json', 'utf8'));
    }
    let dentistryOralHealthModels = null, dentistryOralHealthConfigs = [];
    if (fs.existsSync('content/dentistry_oral_health/experiments.json') && fs.existsSync('content/dentistry_oral_health/models.js')) {
        dentistryOralHealthModels = require('./content/dentistry_oral_health/models.js');
        dentistryOralHealthConfigs = JSON.parse(fs.readFileSync('content/dentistry_oral_health/experiments.json', 'utf8'));
    }
    let foodNutritionModels = null, foodNutritionConfigs = [];
    if (fs.existsSync('content/food_nutrition/experiments.json') && fs.existsSync('content/food_nutrition/models.js')) {
        foodNutritionModels = require('./content/food_nutrition/models.js');
        foodNutritionConfigs = JSON.parse(fs.readFileSync('content/food_nutrition/experiments.json', 'utf8'));
    }
    let pharmacyPharmaceuticalSciencesModels = null, pharmacyPharmaceuticalSciencesConfigs = [];
    if (fs.existsSync('content/pharmacy_pharmaceutical_sciences/experiments.json') && fs.existsSync('content/pharmacy_pharmaceutical_sciences/models.js')) {
        pharmacyPharmaceuticalSciencesModels = require('./content/pharmacy_pharmaceutical_sciences/models.js');
        pharmacyPharmaceuticalSciencesConfigs = JSON.parse(fs.readFileSync('content/pharmacy_pharmaceutical_sciences/experiments.json', 'utf8'));
    }
    let veterinaryMedicineModels = null, veterinaryMedicineConfigs = [];
    if (fs.existsSync('content/veterinary_medicine/experiments.json') && fs.existsSync('content/veterinary_medicine/models.js')) {
        veterinaryMedicineModels = require('./content/veterinary_medicine/models.js');
        veterinaryMedicineConfigs = JSON.parse(fs.readFileSync('content/veterinary_medicine/experiments.json', 'utf8'));
    }
    let earthSpaceSciencesModels = null, earthSpaceSciencesConfigs = [];
    if (fs.existsSync('content/earth_space_sciences/experiments.json') && fs.existsSync('content/earth_space_sciences/models.js')) {
        earthSpaceSciencesModels = require('./content/earth_space_sciences/models.js');
        earthSpaceSciencesConfigs = JSON.parse(fs.readFileSync('content/earth_space_sciences/experiments.json', 'utf8'));
    }
    let marineOceanSciencesModels = null, marineOceanSciencesConfigs = [];
    if (fs.existsSync('content/marine_ocean_sciences/experiments.json') && fs.existsSync('content/marine_ocean_sciences/models.js')) {
        marineOceanSciencesModels = require('./content/marine_ocean_sciences/models.js');
        marineOceanSciencesConfigs = JSON.parse(fs.readFileSync('content/marine_ocean_sciences/experiments.json', 'utf8'));
    }
    let errs = [];
    physConfigs.forEach(c => {
        try {
            const p = physModels.predict(c.slug, c.initial, 3);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => physModels.reading(c.slug, v, physModels.predict(c.slug, v, 3).raw, 3));
            const fit = physModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = physModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / est.reference * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    csConfigs.forEach(c => {
        try {
            const p = csModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => csModels.reading(c.slug, v, csModels.predict(c.slug, v).raw));
            const fit = csModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = csModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / est.reference * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    chemConfigs.forEach(c => {
        try {
            const p = chemModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => chemModels.reading(c.slug, v, chemModels.predict(c.slug, v).raw));
            const fit = chemModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = chemModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / est.reference * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    mathConfigs.forEach(c => {
        try {
            const p = mathModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => mathModels.reading(c.slug, v, mathModels.predict(c.slug, v).raw));
            const fit = mathModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = mathModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / est.reference * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    statsConfigs.forEach(c => {
        try {
            const p = statsModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => statsModels.reading(c.slug, v, statsModels.predict(c.slug, v).raw));
            const fit = statsModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = statsModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    aeroConfigs.forEach(c => {
        try {
            const p = aeroModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => aeroModels.reading(c.slug, v, aeroModels.predict(c.slug, v).raw));
            const fit = aeroModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = aeroModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    agriConfigs.forEach(c => {
        try {
            const p = agriModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => agriModels.reading(c.slug, v, agriModels.predict(c.slug, v).raw));
            const fit = agriModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = agriModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    biomedConfigs.forEach(c => {
        try {
            const p = biomedModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => biomedModels.reading(c.slug, v, biomedModels.predict(c.slug, v).raw));
            const fit = biomedModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = biomedModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    chemengConfigs.forEach(c => {
        try {
            const p = chemengModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => chemengModels.reading(c.slug, v, chemengModels.predict(c.slug, v).raw));
            const fit = chemengModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = chemengModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    civilConfigs.forEach(c => {
        try {
            const p = civilModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => civilModels.reading(c.slug, v, civilModels.predict(c.slug, v).raw));
            const fit = civilModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = civilModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    electricalConfigs.forEach(c => {
        try {
            const p = electricalModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => electricalModels.reading(c.slug, v, electricalModels.predict(c.slug, v).raw));
            const fit = electricalModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = electricalModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    eceConfigs.forEach(c => {
        try {
            const p = eceModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => eceModels.reading(c.slug, v, eceModels.predict(c.slug, v).raw));
            const fit = eceModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = eceModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    mechanicalConfigs.forEach(c => {
        try {
            const p = mechanicalModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => mechanicalModels.reading(c.slug, v, mechanicalModels.predict(c.slug, v).raw));
            const fit = mechanicalModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = mechanicalModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    textileConfigs.forEach(c => {
        try {
            const p = textileModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => textileModels.reading(c.slug, v, textileModels.predict(c.slug, v).raw));
            const fit = textileModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = textileModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    archaeologyConfigs.forEach(c => {
        try {
            const p = archaeologyModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => archaeologyModels.reading(c.slug, v, archaeologyModels.predict(c.slug, v).raw));
            const fit = archaeologyModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = archaeologyModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    geographyConfigs.forEach(c => {
        try {
            const p = geographyModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => geographyModels.reading(c.slug, v, geographyModels.predict(c.slug, v).raw));
            const fit = geographyModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = geographyModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    psychologyConfigs.forEach(c => {
        try {
            const p = psychologyModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => psychologyModels.reading(c.slug, v, psychologyModels.predict(c.slug, v).raw));
            const fit = psychologyModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = psychologyModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    agricultureForestryConfigs.forEach(c => {
        try {
            const p = agricultureForestryModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => agricultureForestryModels.reading(c.slug, v, agricultureForestryModels.predict(c.slug, v).raw));
            const fit = agricultureForestryModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = agricultureForestryModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    basicMedicalSciencesConfigs.forEach(c => {
        try {
            const p = basicMedicalSciencesModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => basicMedicalSciencesModels.reading(c.slug, v, basicMedicalSciencesModels.predict(c.slug, v).raw));
            const fit = basicMedicalSciencesModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = basicMedicalSciencesModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    biologicalSciencesConfigs.forEach(c => {
        try {
            const p = biologicalSciencesModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => biologicalSciencesModels.reading(c.slug, v, biologicalSciencesModels.predict(c.slug, v).raw));
            const fit = biologicalSciencesModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = biologicalSciencesModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    dentistryOralHealthConfigs.forEach(c => {
        try {
            const p = dentistryOralHealthModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => dentistryOralHealthModels.reading(c.slug, v, dentistryOralHealthModels.predict(c.slug, v).raw));
            const fit = dentistryOralHealthModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = dentistryOralHealthModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    foodNutritionConfigs.forEach(c => {
        try {
            const p = foodNutritionModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => foodNutritionModels.reading(c.slug, v, foodNutritionModels.predict(c.slug, v).raw));
            const fit = foodNutritionModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = foodNutritionModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    pharmacyPharmaceuticalSciencesConfigs.forEach(c => {
        try {
            const p = pharmacyPharmaceuticalSciencesModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => pharmacyPharmaceuticalSciencesModels.reading(c.slug, v, pharmacyPharmaceuticalSciencesModels.predict(c.slug, v).raw));
            const fit = pharmacyPharmaceuticalSciencesModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = pharmacyPharmaceuticalSciencesModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    veterinaryMedicineConfigs.forEach(c => {
        try {
            const p = veterinaryMedicineModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => veterinaryMedicineModels.reading(c.slug, v, veterinaryMedicineModels.predict(c.slug, v).raw));
            const fit = veterinaryMedicineModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = veterinaryMedicineModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    earthSpaceSciencesConfigs.forEach(c => {
        try {
            const p = earthSpaceSciencesModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => earthSpaceSciencesModels.reading(c.slug, v, earthSpaceSciencesModels.predict(c.slug, v).raw));
            const fit = earthSpaceSciencesModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = earthSpaceSciencesModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    marineOceanSciencesConfigs.forEach(c => {
        try {
            const p = marineOceanSciencesModels.predict(c.slug, c.initial);
            if (!p.valid) errs.push(c.slug + ': initial predict invalid');
            const rows = c.samples.map(v => marineOceanSciencesModels.reading(c.slug, v, marineOceanSciencesModels.predict(c.slug, v).raw));
            const fit = marineOceanSciencesModels.fit(rows);
            if (!fit || fit.r2 < 0.999) errs.push(c.slug + ': r2 < 0.999 (' + (fit ? fit.r2 : 'null') + ')');
            const est = marineOceanSciencesModels.estimate(c.slug, fit);
            const diff = Math.abs(est.value - est.reference) / Math.abs(est.reference) * 100;
            if (diff > 0.3) errs.push(c.slug + ': regression diff > 0.3% (' + diff.toFixed(4) + '%)');
        } catch(e) {
            errs.push(c.slug + ': exception ' + e.message);
        }
    });
    if (errs.length) { console.error(JSON.stringify(errs)); process.exit(1); }
    console.log('All ' + (physConfigs.length + csConfigs.length + chemConfigs.length + mathConfigs.length + statsConfigs.length + aeroConfigs.length + agriConfigs.length + biomedConfigs.length + chemengConfigs.length + civilConfigs.length + electricalConfigs.length + eceConfigs.length + mechanicalConfigs.length + textileConfigs.length + archaeologyConfigs.length + geographyConfigs.length + psychologyConfigs.length + agricultureForestryConfigs.length + basicMedicalSciencesConfigs.length + biologicalSciencesConfigs.length + dentistryOralHealthConfigs.length + foodNutritionConfigs.length + pharmacyPharmaceuticalSciencesConfigs.length + veterinaryMedicineConfigs.length + earthSpaceSciencesConfigs.length + marineOceanSciencesConfigs.length) + ' experiment models passed validation.');
    """
    js_proc = subprocess.run(['node', '-e', js_test_code], cwd=ROOT, capture_output=True, text=True)
    if js_proc.returncode != 0:
        overall_passed = False
        print('✗ JS Model Validation FAILED:', js_proc.stderr)
    else:
        print('✓ JS Model Validation:', js_proc.stdout.strip())

    # Check Internal Link Integrity
    print('\n----------------------------------------------------------------------')
    print('Testing Internal Link Integrity across all HTML pages...')
    html_files = list((ROOT / 'release').glob('**/*.html'))
    broken_links = []
    link_count = 0
    for f in html_files:
        content = f.read_text()
        links = re.findall(r'(?:href|src)="(/[^"#?]+)', content)
        for link in links:
            link_count += 1
            target = ROOT / 'release' / link.lstrip('/')
            if target.is_dir(): target = target / 'index.html'
            if not target.exists() and not (ROOT / 'release' / link.lstrip('/')).exists():
                broken_links.append((str(f.relative_to(ROOT)), link))

    if broken_links:
        overall_passed = False
        print(f'✗ Link Integrity FAILED: {len(broken_links)} broken links found!')
        for b in broken_links[:5]:
            print(f'    - {b[0]} -> {b[1]}')
    else:
        print(f'✓ Link Integrity PASSED: {link_count} links checked across {len(html_files)} HTML pages. 0 broken.')

    print('======================================================================')
    print('CRITICISM ENGINE VERDICT:', 'ALL PASSED (100% OK)' if overall_passed else 'REJECTED - FIXES REQUIRED')
    print('======================================================================')

    return overall_passed

if __name__ == '__main__':
    ok = run_audit()
    sys.exit(0 if ok else 1)
