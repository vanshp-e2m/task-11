// Robustness measurements per section.  node tools/evidence/robust_check.js <jobs.json> <results.json>
// jobs: [{ url, out, width, login? }]. For every <section> in <main>: its box, every image box (rendered size, natural size,
// object-fit), text that is clipped (overflow hidden and scrollWidth > clientWidth), descendants sticking out of the section
// horizontally, and empty headings / links / images. Plus page-level: horizontal overflow and PHP notices in the HTML.
const fs = require('fs');
const { chromium } = require('playwright');

const USERS = { rep: ['qa-rep', 'QaRep-2026-local'], editor: ['qa-editor', 'QaEditor-2026-local'] };

(async () => {
  const [jobsFile, resultsFile] = process.argv.slice(2);
  const jobs = JSON.parse(fs.readFileSync(jobsFile, 'utf8'));
  const browser = await browser_();
  async function browser_() { return chromium.launch(); }
  const ctxs = {};
  const ctxFor = async (login) => {
    const k = login || 'anon';
    if (ctxs[k]) return ctxs[k];
    const c = await browser.newContext();
    if (login) {
      const p = await c.newPage();
      await p.goto('http://task-11.local/wp-login.php');
      await p.fill('#user_login', USERS[login][0]); await p.fill('#user_pass', USERS[login][1]);
      await p.click('#wp-submit'); await p.waitForLoadState('networkidle'); await p.close();
    }
    return (ctxs[k] = c);
  };
  const out = [];
  for (const j of jobs) {
    const p = await (await ctxFor(j.login)).newPage();
    await p.setViewportSize({ width: j.width, height: 1000 });
    const resp = await p.goto(j.url, { waitUntil: 'networkidle', timeout: 90000 });
    const html = await resp.text();
    await p.addStyleTag({ content: '#wpadminbar{display:none!important} html{margin-top:0!important}' });
    await p.evaluate(() => document.fonts.ready);
    await p.evaluate(async () => {
      for (let y = 0; y < document.documentElement.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); }
      window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 400));
    });
    const m = await p.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      const secs = [...document.querySelectorAll('main section')].filter(s => !s.parentElement.closest('main section'));
      return {
        scrollW: document.documentElement.scrollWidth, vw, H: document.documentElement.scrollHeight,
        secs: secs.map(s => {
          const sr = s.getBoundingClientRect();
          const imgs = [...s.querySelectorAll('img')].map(i => {
            const r = i.getBoundingClientRect();
            return { w: Math.round(r.width), h: Math.round(r.height), nw: i.naturalWidth, nh: i.naturalHeight, fit: getComputedStyle(i).objectFit, src: (i.currentSrc || i.src).split('/').pop() };
          }).filter(i => i.w > 0);
          const clipped = [], sticking = [];
          for (const el of s.querySelectorAll('*')) {
            const cs = getComputedStyle(el);
            if (!el.getClientRects().length || el.closest('.visually-hidden,.screen-reader-text,.elementor-screen-only,.sr-only')) continue;
            if (el.childElementCount === 0 && el.textContent.trim() && (cs.overflowX === 'hidden' || cs.overflow === 'hidden' || cs.textOverflow === 'ellipsis') && el.scrollWidth > el.clientWidth + 1 && !['IMG', 'SVG'].includes(el.tagName)) {
              clipped.push(el.tagName.toLowerCase() + '.' + [...el.classList].slice(0, 2).join('.'));
            }
            const r = el.getBoundingClientRect();
            if (r.width && (r.right > Math.min(sr.right, vw) + 1 || r.left < Math.max(sr.left, 0) - 1)) {
              let hidden = false;
              for (let a = el.parentElement; a && a !== s.parentElement; a = a.parentElement) {
                const o = getComputedStyle(a).overflowX;
                if (o !== 'visible') { hidden = true; break; }
              }
              if (!hidden && cs.position !== 'absolute') sticking.push(el.tagName.toLowerCase() + '.' + [...el.classList].slice(0, 2).join('.'));
            }
          }
          const empty = {
            headings: [...s.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(h => !h.textContent.trim()).length,
            links: [...s.querySelectorAll('a')].filter(a => !a.textContent.trim() && !a.querySelector('img,svg') && !a.getAttribute('aria-label')).length,
            imgs: [...s.querySelectorAll('img')].filter(i => !i.getAttribute('src')).length,
          };
          return { id: s.id || s.className.split(' ').slice(0, 2).join('.'), top: Math.round(sr.top + scrollY), h: Math.round(sr.height), imgs, clipped: [...new Set(clipped)], sticking: [...new Set(sticking)].slice(0, 5), empty };
        }),
      };
    });
    m.php = (html.match(/(Warning|Notice|Deprecated|Fatal error)<\/b>:/g) || []).length;
    if (j.out) await p.screenshot({ path: j.out, fullPage: true });
    out.push({ ...j, ...m });
    console.log(`${j.width}\t${m.secs.length} sections\toverflow=${m.scrollW > m.vw}\tphp=${m.php}\t${j.url}`);
    await p.close();
  }
  fs.writeFileSync(resultsFile, JSON.stringify(out, null, 1));
  await browser.close();
})();
