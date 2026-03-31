/**
 * Playwright visual audit — captures every OpenQC page at 1440x900.
 * Run: npx playwright test screenshot-audit.mjs (or node with playwright)
 */
import { chromium } from '@playwright/test';
import { mkdirSync } from 'fs';
import { join } from 'path';

const BASE = 'http://localhost:5173';
const OUT = join(import.meta.dirname, 'screenshots');

const pages = [
  { path: '/', name: '01-dashboard' },
  { path: '/qc', name: '02-qc-monitor' },
  { path: '/sigma', name: '03-sigma' },
  { path: '/validation', name: '04-validation' },
  { path: '/audit', name: '05-audit' },
  { path: '/lots', name: '06-lots' },
  { path: '/regulatory', name: '07-regulatory' },
  { path: '/learn', name: '08-learn-intro' },
  { path: '/learn?chapter=westgard', name: '09-learn-westgard' },
  { path: '/learn?chapter=sigma', name: '10-learn-sigma' },
  { path: '/learn?chapter=validation', name: '11-learn-validation' },
  { path: '/learn?chapter=examples', name: '12-learn-examples' },
  { path: '/settings', name: '13-settings' },
];

async function run() {
  mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });

  for (const pg of pages) {
    const page = await ctx.newPage();
    await page.goto(`${BASE}${pg.path}`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(500);
    // Full page screenshot
    await page.screenshot({
      path: join(OUT, `${pg.name}.png`),
      fullPage: true,
    });
    console.log(`✓ ${pg.name}`);
    await page.close();
  }

  await browser.close();
  console.log(`\nDone — ${pages.length} screenshots in ${OUT}`);
}

run().catch(e => { console.error(e); process.exit(1); });
