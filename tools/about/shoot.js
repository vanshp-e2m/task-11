// Full-page screenshot of a live URL + optional measurement expression.
// node tools/about/shoot.js <url> <out.png> <width> [js-expression]
const { chromium } = require('playwright');
(async () => {
  const [url, out, w, expr] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: parseInt(w || '1440', 10), height: 1000 } });
  const logs = [];
  page.on('pageerror', e => logs.push('PAGEERROR ' + e.message));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  // Elementor lazy-loads images and container backgrounds: scroll through once so a full-page capture has them.
  await page.evaluate(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 200)); } window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 800)); });
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(400);
  if (out && out !== '-') await page.screenshot({ path: out, fullPage: true });
  if (expr) console.log(JSON.stringify(await page.evaluate(expr), null, 1));
  if (logs.length) console.log(logs.join('\n'));
  await browser.close();
})();
