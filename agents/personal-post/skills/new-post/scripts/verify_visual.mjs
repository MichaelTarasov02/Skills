/* =============================================================================
   VISUAL QA — run from a post's Visual/ folder, after `node export.mjs`

     node /path/to/verify_visual.mjs            # human-readable
     node /path/to/verify_visual.mjs --json     # machine-readable

   Exists because the export gates only prove the artboards are the right size
   with the right fonts. They say nothing about whether a slide is composed.
   Three consecutive runs re-wrote this measurement by hand and each time missed
   a different defect, so it is bundled and identical every run.

   What it catches that the export gates do not:
     · content escaping the 90px frame (silent crop on .page — the endnote goes)
     · a separator left pointing past the last node of a wrapped pipeline
     · a theme that disagrees with the specification
     · a slide filling under ~40% of its band, or a stretched component
     · word counts past the theme's density budget

   What it CANNOT catch: whether a stretched component is hollow inside. A
   hollow stretch reports 100% fill because it touches both edges. Open the
   PNGs. This script narrows where to look; it does not replace looking.
   ========================================================================== */

import { existsSync, readFileSync, readdirSync } from 'node:fs';
import path from 'node:path';

const DIR = process.cwd();
const JSON_OUT = process.argv.includes('--json');

const { createRequire } = await import('node:module');
const { fileURLToPath } = await import('node:url');
const require_ = createRequire(import.meta.url);
const HERE = path.dirname(fileURLToPath(import.meta.url));

/* Resolve Playwright without depending on where this script was launched from.
   Order: explicit override, normal Node resolution, resolution relative to THIS
   file, then an upward walk from it. cwd is deliberately not used — it is a
   content folder that will never hold node_modules. */
async function loadPlaywright() {
  if (process.env.PW && existsSync(process.env.PW)) return import(process.env.PW);
  try { return await import('playwright'); } catch {}
  try { return await import(require_.resolve('playwright')); } catch {}
  for (let d = HERE; d !== path.dirname(d); d = path.dirname(d)) {
    const p = path.join(d, 'node_modules/playwright/index.mjs');
    if (existsSync(p)) return import(p);
  }
  console.error(
    ['Playwright not found. From the plugin root run:',
     '  npm install playwright && npx playwright install chromium',
     'Or point at an existing install: PW=/abs/path/to/playwright/index.mjs'
    ].join(String.fromCharCode(10)));
  process.exit(1);
}
const { chromium } = await loadPlaywright();

/* the spec is the authority on theme — find it next to the Visual/ folder */
function specTheme() {
  const spec = path.join(DIR, '..', 'Post Specification.md');
  if (!existsSync(spec)) return null;
  const m = readFileSync(spec, 'utf8').match(/Visual theme:\s*([a-z]+)/i);
  return m ? m[1].toLowerCase() : null;
}

/* The profile filename, newest first. `founder-post.yaml` is the pre-rename name,
   kept so an older content repo keeps working instead of silently losing its budgets. */
const PROFILE_NAMES = ['personal-post.yaml', 'founder-post.yaml'];

function parseBudgets(file) {
  const out = {};
  for (const m of readFileSync(file, 'utf8')
       .matchAll(/^\s*([A-Za-z0-9_]+)_words:\s*(\d+)\s*-\s*(\d+)/gm)) {
    out[m[1].toLowerCase()] = [Number(m[2]), Number(m[3])];
  }
  return Object.keys(out).length ? out : null;
}

/* density budgets per theme, overridable in personal-post.yaml */
function budgets() {
  for (let d = DIR; d !== path.dirname(d); d = path.dirname(d)) {
    for (const n of PROFILE_NAMES) {
      const p = path.join(d, n);
      if (existsSync(p)) {
        const out = parseBudgets(p);
        if (out) return out;
      }
    }
  }
  /* documented fallback: a profile kept in the home directory */
  for (const n of PROFILE_NAMES) {
    const home = path.join(process.env.HOME || '', `.${n}`);
    if (existsSync(home)) {
      const out = parseBudgets(home);
      if (out) return out;
    }
  }
  return {};                       // unknown theme → skip the word check
}

const wantTheme = specTheme();
const BUDGET = budgets();
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1240, height: 1500 } });

async function measure(file) {
  await page.goto('file://' + path.join(DIR, file), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(700);

  return page.evaluate(() => {
    const sel = document.querySelectorAll('.slide').length ? '.slide' : '.page';
    return [...document.querySelectorAll(sel)].map((s, i) => {
      const frame = s.querySelector('.frame');
      const body = s.querySelector('.fill') || s.querySelector('.sheet');
      /* Malformed markup is exactly what this script exists to catch, so it
         must report the missing element rather than throw an opaque error. */
      if (!frame) return { n: i + 1, malformed: 'no .frame element' };
      if (!body) return { n: i + 1, malformed: 'no .fill or .sheet element' };
      const fr = frame.getBoundingClientRect();
      const fl = body.getBoundingClientRect();

      let top = Infinity, bot = -Infinity;
      body.querySelectorAll(':scope > *').forEach((c) => {
        const b = c.getBoundingClientRect();
        if (b.height > 0) { top = Math.min(top, b.top); bot = Math.max(bot, b.bottom); }
      });

      const overflow = [...frame.querySelectorAll('*')].filter((e) => {
        const b = e.getBoundingClientRect();
        return b.right > fr.right + 1 || b.bottom > fr.bottom + 1 || b.left < fr.left - 1;
      }).map((e) => e.className || e.tagName).slice(0, 4);

      /* a separator whose following node sits on another line points at nothing */
      let dangling = 0;
      s.querySelectorAll('.strip').forEach((st) => {
        const kids = [...st.children];
        kids.forEach((c, j) => {
          if (!c.classList.contains('sep')) return;
          const next = kids[j + 1];
          if (!next) { dangling++; return; }
          const a = c.getBoundingClientRect(), b = next.getBoundingClientRect();
          if (Math.abs((b.top + b.bottom) / 2 - (a.top + a.bottom) / 2) > 12) dangling++;
        });
      });

      /* the single page silently crops its last block, which is the sign-off */
      const en = s.querySelector('.endnote');
      const endnoteInside = en ? en.getBoundingClientRect().bottom <= fr.bottom + 1 : null;

      return {
        n: i + 1,
        theme: s.getAttribute('data-theme'),
        fillPct: Math.round(((bot - top) / fl.height) * 100),
        words: (body.innerText || '').trim().split(/\s+/).filter(Boolean).length,
        overflow,
        dangling,
        endnoteInside,
        centred: body.className.includes('centre'),
      };
    });
  });
}

const report = {};
for (const f of ['carousel.html', 'single-page.html']) {
  if (existsSync(path.join(DIR, f))) report[f] = await measure(f);
}
await browser.close();

/* ---------------------------------------------------------------- verdict */
const problems = [];
const warnings = [];

for (const [file, rows] of Object.entries(report)) {
  for (const r of rows) {
    const id = `${file} slide ${r.n}`;
    if (r.malformed) { problems.push(`${id}: ${r.malformed}`); continue; }
    if (r.overflow.length)
      problems.push(`${id}: content escapes the frame → ${r.overflow.join(', ')}`);
    if (r.dangling)
      problems.push(`${id}: ${r.dangling} separator(s) point past the last node — use .strip.nowrap`);
    if (r.endnoteInside === false)
      problems.push(`${id}: the .endnote is cropped off the artboard — cut content, do not shrink type`);
    if (wantTheme && r.theme !== wantTheme)
      problems.push(`${id}: theme "${r.theme}" disagrees with the spec ("${wantTheme}")`);

    /* The density budget is a per-SLIDE rule. The single page deliberately
       carries the whole post on one artboard, so the budget does not apply —
       checking it there produces a warning that is always wrong and trains
       the reader to ignore the warnings that are not. */
    const band = BUDGET[r.theme];
    if (file !== 'single-page.html' && band && (r.words < band[0] || r.words > band[1]))
      warnings.push(`${id}: ${r.words} words, budget ${band[0]}-${band[1]} (rows-not-prose slides may exceed)`);
    if (r.fillPct < 40)
      warnings.push(`${id}: fills ${r.fillPct}% — reads as a small block in a void`);
    if (r.fillPct >= 99)
      warnings.push(`${id}: fills ${r.fillPct}% — verify by eye that it is not a hollow stretch`);
  }
}

/* the PDF is the upload artifact, so confirm it exists and has a page per slide */
const pdf = path.join(DIR, 'exports', 'carousel.pdf');
if (existsSync(pdf)) {
  const buf = readFileSync(pdf);
  const pages = (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
  const slides = (report['carousel.html'] || []).length;
  if (slides && pages !== slides)
    problems.push(`carousel.pdf has ${pages} pages but the deck has ${slides} slides`);
  report._pdf = { pages };
} else if (report['carousel.html']) {
  problems.push('exports/carousel.pdf is missing — run `node export.mjs`');
}

if (JSON_OUT) {
  console.log(JSON.stringify({ ok: !problems.length, problems, warnings, report }, null, 2));
} else {
  for (const [file, rows] of Object.entries(report)) {
    if (file.startsWith('_')) continue;
    console.log(`\n${file}`);
    for (const r of rows) {
      console.log(
        `  ${String(r.n).padStart(2)}  theme=${r.theme}  fill=${String(r.fillPct).padStart(3)}%  ` +
        `words=${String(r.words).padStart(3)}  ${r.centred ? 'centred' : 'top-flow'}` +
        `${r.overflow.length ? '  OVERFLOW' : ''}${r.dangling ? '  DANGLING-ARROW' : ''}` +
        `${r.endnoteInside === false ? '  ENDNOTE-CROPPED' : ''}`);
    }
  }
  if (report._pdf) console.log(`\ncarousel.pdf: ${report._pdf.pages} pages`);

  if (warnings.length) {
    console.log(`\n${warnings.length} warning(s) — judgement call, look at the render:`);
    warnings.forEach((w) => console.log(`  ~ ${w}`));
  }
  if (problems.length) {
    console.log(`\nFAIL — ${problems.length} problem(s):`);
    problems.forEach((p) => console.log(`  ✗ ${p}`));
  } else {
    console.log('\nPASS — no overflow, no dangling arrows, theme matches the spec');
  }
  console.log('\nNow open exports/*.png. This script measures geometry; it cannot');
  console.log('see a component stretched hollow. That still needs your eyes.');
}

process.exit(problems.length ? 1 : 0);
