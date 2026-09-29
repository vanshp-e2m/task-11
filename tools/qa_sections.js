// Capture a page + its section boxes. node tools/qa_sections.js <url> <out.png> <width> [login]
// Sections = <section> children of <main> (WP) or of <body> (replica). Logs in as the local QA sales rep when asked.
const { chromium } = require('playwright');
(async () => {
  const [url, out, w, login] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: parseInt(w, 10), height: 1000 } });
  if (login) {
    await p.goto('http://task-11.local/wp-login.php');
    await p.fill('#user_login', 'qa-rep'); await p.fill('#user_pass', 'QaRep-2026-local'); await p.click('#wp-submit');
    await p.waitForLoadState('networkidle');
  }
  await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 500)); });
  const secs = await p.evaluate(() => [...document.querySelectorAll('section[id], main > section, section.rs')].filter((s, i, a) => a.indexOf(s) === i)
    .map(s => { const r = s.getBoundingClientRect(); return { id: s.id || s.className.split(' ').slice(0, 2).join('.'), top: Math.round(r.top + scrollY), h: Math.round(r.height) }; }));
  await p.screenshot({ path: out, fullPage: true });
  console.log(JSON.stringify({ url: p.url(), H: await p.evaluate(() => document.documentElement.scrollHeight), W: await p.evaluate(() => document.documentElement.scrollWidth), secs }));
  await b.close();
})();
