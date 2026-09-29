// Measure the absolutely-positioned desktop layouts (Figma coordinates) so tools/figma_html/flow_desktop.py can turn them into
// row grids that keep the exact positions but let content push what's below it.
//   node tools/evidence/measure_flow.js <out.json>
// For every positioned container P inside the listed sections: its items (absolute children whose offsetParent is P, plus static
// children with their own box), their boxes relative to P's padding box, and the static wrappers in between (-> display:contents).
const fs = require('fs');
const { chromium } = require('playwright');

const TARGETS = [
  { url: 'http://task-11.local/', scope: 'mizuho-home', sections: ['hero-carousel', 'intro-statement', 'value-columns', 'procedure-band', 'testimonials', 'about-stats'] },
  { url: 'http://task-11.local/products/', scope: 'products', sections: ['browse-by-procedure'] },
];

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const all = [];
  for (const t of TARGETS) {
    await p.goto(t.url, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const res = await p.evaluate(({ ids, scope }) => {
      const DYN = /^(swiper-|is-|lazy|e-lazy|loaded)/;
      const cls = (el) => [...el.classList].filter(c => !DYN.test(c));
      const visible = (el) => el.getClientRects().length > 0 && getComputedStyle(el).display !== 'none';
      const SKIP_P = ['A', 'BUTTON', 'SUMMARY', 'LABEL', 'FORM', 'SELECT'];
      function selOf(el, stop) {
        const parts = [];
        for (let e = el; e && e !== stop; e = e.parentElement) {
          let s = cls(e).length ? '.' + cls(e).join('.') : e.tagName.toLowerCase();
          const sib = [...e.parentElement.children].filter(x => (cls(x).length ? '.' + cls(x).join('.') : x.tagName.toLowerCase()) === s);
          if (sib.length > 1) s += `:nth-child(${[...e.parentElement.children].indexOf(e) + 1})`;
          parts.unshift(s);
        }
        return parts.join(' > ');
      }
      const out = [];
      for (const id of ids) {
        const sec = document.getElementById(id);
        if (!sec) continue;
        const secSel = '.' + cls(sec).filter(c => c !== 'rs')[0];
        const abs = [...sec.querySelectorAll('*')].filter(e => visible(e) && getComputedStyle(e).position === 'absolute' && !e.closest('.visually-hidden'));
        const parents = [...new Set(abs.map(e => e.offsetParent).filter(Boolean))].filter(P => sec.contains(P) && !SKIP_P.includes(P.tagName) && !P.closest('a,button'));
        for (const P of parents) {
          const pr = P.getBoundingClientRect();
          const ox = pr.left + P.clientLeft, oy = pr.top + P.clientTop;
          const items = [], contents = [];
          const walk = (node) => {
            for (const c of node.children) {
              const cs = getComputedStyle(c);
              if (cs.display === 'contents') { walk(c); continue; } // already transparent (e.g. .pb-item links)
              if (!visible(c)) continue;
              if (cs.position === 'absolute' && c.offsetParent === P) { items.push(c); continue; }
              if (cs.position === 'absolute' || cs.position === 'fixed') continue; // positioned against something else
              const holds = [...c.querySelectorAll('*')].some(d => getComputedStyle(d).position === 'absolute' && d.offsetParent === P && visible(d));
              const plain = cs.backgroundImage === 'none' && cs.backgroundColor === 'rgba(0, 0, 0, 0)' && cs.borderTopWidth === '0px' && cs.boxShadow === 'none';
              if (holds && plain && c.tagName !== 'A') { contents.push(c); walk(c); } else items.push(c);
            }
          };
          walk(P);
          const tr = (el) => { const m = getComputedStyle(el).transform; return m !== 'none' && /^matrix\(1, 0, 0, 1,/.test(m); };
          out.push({
            scope, section: id, secSel,
            P: P === sec ? secSel : secSel + ' > ' + selOf(P, sec), isSection: P === sec, isFx: P.classList.contains('fx'),
            H: Math.round(P.clientHeight * 100) / 100,
            contents: contents.map(c => secSel + ' > ' + selOf(c, sec)),
            items: items.map(e => {
              const r = e.getBoundingClientRect();
              const text = e.textContent.trim().length > 0;
              const media = ['IMG', 'SVG', 'VIDEO', 'IFRAME', 'PICTURE', 'HR'].includes(e.tagName) || (!text && e.children.length === 0);
              return { sel: secSel + ' > ' + selOf(e, sec), tag: e.tagName, x: +(r.left - ox).toFixed(2), y: +(r.top - oy).toFixed(2),
                       w: +r.width.toFixed(2), h: +r.height.toFixed(2), media, button: e.tagName === 'A' || e.tagName === 'BUTTON',
                       container: false, translate: tr(e) };
            }),
          });
        }
      }
      return out;
    }, { ids: t.sections, scope: t.scope });
    all.push(...res);
  }
  // mark items that are themselves converted containers
  const Ps = new Set(all.map(c => c.P));
  for (const c of all) for (const it of c.items) it.container = Ps.has(it.sel);
  fs.writeFileSync(process.argv[2], JSON.stringify(all, null, 1));
  console.log(all.map(c => `${c.section}: ${c.P} items=${c.items.length} contents=${c.contents.length}`).join('\n'));
  await b.close();
})();
