/* =============================================================================
   PERSONAL-POST · EXPORT CONTRACT
   Authority: references/visual-system.md §7
   Usage:  node export.mjs            (run from a post's Visual/ folder)
           PW=/abs/path/to/playwright node export.mjs
   -----------------------------------------------------------------------------
   Produces, from one post folder:
     exports/page-01.png     single-page mode   (2160x2700)
     exports/slide-NN.png    carousel mode      (2160x2700 each)
     exports/carousel.pdf    LinkedIn document post (1080x1350 pages)

   Hard gates (throw, never warn):
     1. FONT   — only Newsreader / Geist / Geist Mono may render.
     2. SIZE   — every .slide and .page must measure exactly 1080x1350 CSS px.
     3. COUNT  — carousel must hold 6..12 slides.
   Adapted from the Sinister company export contract
   (01 Company Idea To Visual/04-sinister-spec-to-visual-post.prompt.md §10).
   ========================================================================== */

import { existsSync } from 'node:fs';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';

const DIR = process.cwd();
const OUT = path.join(DIR, 'exports');

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

const ALLOWED = new Set(['Newsreader', 'Geist', 'Geist Mono']);

await mkdir(OUT, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1240, height: 1500 }, deviceScaleFactor: 2 });

async function settle() {
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1200);
}

async function assertFonts(label) {
  const fams = await page.evaluate(() => {
    const set = new Set();
    const fam = (el) => set.add(getComputedStyle(el).fontFamily.split(',')[0].replace(/["']/g, '').trim());
    // leaf text nodes
    document.querySelectorAll('h1,h2,h3,p,span,div,li,td').forEach((el) => {
      const t = (el.textContent || '').trim();
      if (t.length > 2 && el.children.length === 0) fam(el);
    });
    // display type carries <em>/<br> children, so check it explicitly —
    // otherwise a silent serif fallback would pass unnoticed.
    document.querySelectorAll('.display,.h1,.h2,.pull,.ttl,.lt').forEach((el) => {
      if ((el.textContent || '').trim().length > 2) fam(el);
    });
    return [...set];
  });
  const bad = fams.filter((f) => !ALLOWED.has(f));
  if (bad.length) throw new Error(`[${label}] non-system fonts rendered: ${bad.join(', ')}`);
  console.log(`[${label}] fonts ok: ${fams.join(' / ')}`);
}

async function assertBox(handle, name) {
  const b = await handle.boundingBox();
  if (Math.round(b.width) !== 1080 || Math.round(b.height) !== 1350) {
    throw new Error(`${name} is ${Math.round(b.width)}x${Math.round(b.height)}, expected 1080x1350`);
  }
}

/* ---------- carousel ---------- */
const carouselFile = path.join(DIR, 'carousel.html');
let slideCount = 0;
if (existsSync(carouselFile)) {
  await page.goto('file://' + carouselFile);
  await page.waitForLoadState('networkidle');
  await settle();
  await assertFonts('carousel');

  const slides = await page.$$('section.slide');
  slideCount = slides.length;
  if (slideCount < 6 || slideCount > 12) {
    throw new Error(`carousel has ${slideCount} slides; system allows 6..12`);
  }
  for (let i = 0; i < slides.length; i++) {
    const num = String(i + 1).padStart(2, '0');
    await assertBox(slides[i], `slide-${num}`);
    await slides[i].screenshot({ path: path.join(OUT, `slide-${num}.png`) });
    console.log(`  slide-${num}.png  2160x2700`);
  }

  // LinkedIn document post: PDF is the only format that renders reliably.
  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: path.join(OUT, 'carousel.pdf'),
    width: '1080px',
    height: '1350px',
    printBackground: true,
    pageRanges: `1-${slideCount}`,
  });
  await page.emulateMedia({ media: 'screen' });
  console.log(`  carousel.pdf  ${slideCount} pages @ 1080x1350`);
}

/* ---------- single page ---------- */
const pageFile = path.join(DIR, 'single-page.html');
if (existsSync(pageFile)) {
  await page.goto('file://' + pageFile);
  await page.waitForLoadState('networkidle');
  await settle();
  await assertFonts('single-page');
  const el = await page.$('section.page');
  if (!el) throw new Error('single-page.html has no section.page');
  await assertBox(el, 'page-01');
  await el.screenshot({ path: path.join(OUT, 'page-01.png') });
  console.log('  page-01.png  2160x2700');
}

await browser.close();
console.log(`OK · carousel ${slideCount} slides + single page + pdf`);
