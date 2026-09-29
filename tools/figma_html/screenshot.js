const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const fileArg = path.resolve(process.argv[2]).split(path.sep).join('/');
  const url = 'file:///' + fileArg;
  const outDir = process.argv[3];
  const width = parseInt(process.argv[4] || '1440', 10);
  const page = await browser.newPage({ viewport: { width: width, height: 1000 } });
  const logs = [];
  page.on('console', function (msg) { logs.push(msg.text()); });
  page.on('pageerror', function (err) { logs.push('PAGEERROR: ' + err.message); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, 'full-' + width + '.png'), fullPage: true });

  const ids = ['hero-carousel', 'intro-statement', 'value-columns', 'procedure-band', 'testimonials', 'about-stats'];
  for (const id of ids) {
    const el = await page.$('#' + id);
    if (el) {
      await el.screenshot({ path: path.join(outDir, id + '-' + width + '.png') });
    } else {
      logs.push('MISSING SECTION: ' + id);
    }
  }
  console.log(JSON.stringify(logs, null, 2));
  await browser.close();
})();
