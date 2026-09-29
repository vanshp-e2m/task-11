// Full-page captures for evidence sheets, one browser for everything.
//   node tools/evidence/shoot_many.js <jobs.json> <results.json>
// jobs: [{ url, out, width, login?: "rep"|"editor" }]. Result per job: final url, page height, horizontal overflow
// (documentElement.scrollWidth vs the viewport) and the widest element that sticks out, so overflow is measured, not eyeballed.
const fs = require('fs');
const { chromium } = require('playwright');

const USERS = { rep: ['qa-rep', 'QaRep-2026-local'], editor: ['qa-editor', 'QaEditor-2026-local'] };

(async () => {
  const [jobsFile, resultsFile] = process.argv.slice(2);
  const jobs = JSON.parse(fs.readFileSync(jobsFile, 'utf8'));
  const browser = await chromium.launch();
  const contexts = {};
  const ctxFor = async (login) => {
    const key = login || 'anon';
    if (contexts[key]) return contexts[key];
    const ctx = await browser.newContext();
    if (login) {
      const p = await ctx.newPage();
      await p.goto('http://task-11.local/wp-login.php');
      await p.fill('#user_login', USERS[login][0]);
      await p.fill('#user_pass', USERS[login][1]);
      await p.click('#wp-submit');
      await p.waitForLoadState('networkidle');
      await p.close();
    }
    contexts[key] = ctx;
    return ctx;
  };
  const results = [];
  for (const j of jobs) {
    const ctx = await ctxFor(j.login);
    const p = await ctx.newPage();
    await p.setViewportSize({ width: j.width, height: 1000 });
    await p.goto(j.url, { waitUntil: 'networkidle', timeout: 90000 });
    await p.evaluate(() => document.fonts.ready);
    await p.evaluate(async () => {
      for (let y = 0; y < document.documentElement.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); }
      window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 400));
    });
    const m = await p.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      let worst = null;
      for (const el of document.querySelectorAll('body *')) {
        const r = el.getBoundingClientRect();
        if (!r.width || getComputedStyle(el).position === 'fixed') continue;
        const over = Math.max(r.right - vw, -r.left);
        if (over > 1 && (!worst || over > worst.over)) {
          let clipped = false;
          for (let a = el.parentElement; a; a = a.parentElement) {
            const o = getComputedStyle(a).overflowX;
            if (o === 'hidden' || o === 'clip' || o === 'auto' || o === 'scroll') { clipped = true; break; }
          }
          if (!clipped) worst = { over: Math.round(over), el: el.tagName.toLowerCase() + '.' + [...el.classList].slice(0, 3).join('.') };
        }
      }
      return { H: document.documentElement.scrollHeight, scrollW: document.documentElement.scrollWidth, vw, worst };
    });
    if (j.out) await p.screenshot({ path: j.out, fullPage: true });
    results.push({ ...j, final: p.url(), ...m, overflow: m.scrollW > m.vw });
    console.log(`${j.width}\t${m.H}\t${m.scrollW > m.vw ? 'OVERFLOW ' + m.scrollW : 'ok'}\t${j.url}`);
    await p.close();
  }
  fs.writeFileSync(resultsFile, JSON.stringify(results, null, 1));
  await browser.close();
})();
