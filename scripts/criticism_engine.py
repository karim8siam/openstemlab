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
    if (errs.length) { console.error(JSON.stringify(errs)); process.exit(1); }
    console.log('All ' + (physConfigs.length + csConfigs.length + chemConfigs.length + mathConfigs.length + statsConfigs.length) + ' experiment models passed validation.');
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
