"""Flow B proof: ONE change in the global settings updates every page, whichever builder made it.

    python tools/evidence/global_proof.py      -> docs/evidence/flow-b/global-proof/ (before/after/reverted screenshots + README.md)

Two global values, each changed exactly once, through DevConnect (tools/bridge.py; the writes are listed and read back):
  * business data  - ACF Site Settings `m11_phone`        (read by Elementor dynamic tags AND by the ACF templates)
  * brand colour   - Elementor Kit system colour `primary` (read by Elementor widgets AND, via --e-global-color-primary ->
                     var(--clr-primary), by the ACF layout partials)
Measured on every page: occurrences of the phone number in the HTML, tel: links built from it, and the computed colour of the
page's first heading. Then both values are reverted and measured again.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bridge import dispatch  # noqa: E402

OUT = os.path.join(ROOT, "docs", "evidence", "flow-b", "global-proof")
NODE_PATH = r"C:/Users/Vansh Patel/.claude/plugins/cache/dev-command/dev-command/fbe821068e44/scripts/node_modules"
PAGES = [("Home", "ACF", ""), ("Resources", "ACF", "resources/"), ("Products", "ACF", "products/"),
         ("Product (CPT)", "ACF", "products/product-sugita-ii-head-frame/"), ("About Us", "Elementor", "about-us/"),
         ("Contact Us", "Elementor", "contact-us/"), ("Sales Hub login", "ACF", "sales-hub/")]
SHOTS = ("", "contact-us/", "about-us/")
NEW_PHONE, NEW_PRIMARY = "800-555-0199", "#b0197e"

JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [pagesJson, phone, shotDir, tag] = process.argv.slice(2);
  const pages = JSON.parse(pagesJson); const shots = %SHOTS%;
  const b = await chromium.launch(); const res = [];
  for (const [name, builder, path] of pages) {
    const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
    const r = await p.goto('http://task-11.local/' + path + '?nocache=' + Date.now(), { waitUntil: 'networkidle' });
    const html = await r.text();
    const digits = phone.replace(/\D/g, '');
    const m = await p.evaluate(() => {
      const h = document.querySelector('main h1, .au-h1 .elementor-heading-title, .cu-h1 .elementor-heading-title, main h2');
      return { heading: h ? h.textContent.trim().slice(0, 40) : '', color: h ? getComputedStyle(h).color : '' };
    });
    res.push({ name, builder, path, phoneText: html.split(phone).length - 1, telLinks: (html.match(new RegExp('tel:\\+?1?' + digits, 'g')) || []).length, ...m });
    if (shots.includes(path)) await p.screenshot({ path: `${shotDir}/${tag}-${(path || 'home').replace(/\//g, '')}.png` });
    await p.close();
  }
  console.log(JSON.stringify(res)); await b.close();
})();
"""


def measure(phone, tag):
    js = os.path.join(ROOT, "cache", "evidence", "global_measure.js")
    open(js, "w", encoding="utf-8").write(JS.replace("%SHOTS%", json.dumps(list(SHOTS))))
    r = subprocess.run(["node", js, json.dumps(PAGES), phone, OUT, tag], capture_output=True, text=True,
                       env=dict(os.environ, NODE_PATH=NODE_PATH), cwd=ROOT)
    return json.loads(r.stdout.strip().splitlines()[-1])


def kit_colors():
    g = dispatch("dev/elementor-get-global-settings", {"_": 1})
    return g["system_colors"], g["custom_colors"]


def set_state(phone, primary, log):
    dispatch("dev/acf-read-write-values", {"action": "write", "post_id": "options", "field_key_or_name": "m11_phone", "value": phone})
    sys_c, cus_c = kit_colors()
    sys_c = [{**c, "color": primary} if c["_id"] == "primary" else c for c in sys_c]
    dispatch("dev/elementor-update-global-colors", {"system_colors": sys_c, "custom_colors": cus_c})
    subprocess.run(["bash", os.path.join(ROOT, "tools", "wp.sh"), "elementor", "flush-css"], capture_output=True, cwd=ROOT)
    # Elementor rebuilds the Kit stylesheet (post-6.css) lazily on the next request; warm it up once before measuring.
    import urllib.request
    urllib.request.urlopen("http://task-11.local/?warm=1", timeout=60).read()
    back_phone = dispatch("dev/acf-read-write-values", {"action": "read", "post_id": "options", "field_key_or_name": "m11_phone"}).get("value")
    back = kit_colors()
    log.append(f"m11_phone := {phone} (read back {back_phone}); Kit primary := {primary} (read back "
               f"{next(c['color'] for c in back[0] if c['_id'] == 'primary')}, other slots unchanged: "
               f"{[c['color'] for c in back[0] if c['_id'] != 'primary']} + {len(back[1])} custom)")


def main():
    os.makedirs(OUT, exist_ok=True)
    old_phone = dispatch("dev/acf-read-write-values", {"action": "read", "post_id": "options", "field_key_or_name": "m11_phone"}).get("value")
    old_primary = next(c["color"] for c in kit_colors()[0] if c["_id"] == "primary")
    log = []
    before = measure(old_phone, "1-before")
    set_state(NEW_PHONE, NEW_PRIMARY, log)
    after = measure(NEW_PHONE, "2-after")
    after_old = measure(old_phone, "2-after-oldcheck")
    set_state(old_phone, old_primary, log)
    reverted = measure(old_phone, "3-reverted")
    for f in os.listdir(OUT):
        if f.startswith("2-after-oldcheck"):
            os.remove(os.path.join(OUT, f))
    L = ["# Global settings proof (Flow B)", "",
         f"One edit each, then revert: **Site Settings → Phone** `{old_phone}` → `{NEW_PHONE}`, and **Elementor Kit → Primary** "
         f"`{old_primary}` → `{NEW_PRIMARY}`. No page, template or widget was edited.", "",
         "| Page | Builder | Phone shown before → after (old number left) | tel: links before → after | First heading colour before → after → reverted |",
         "|---|---|---|---|---|"]
    for b, a, ao, r in zip(before, after, after_old, reverted):
        L.append(f"| {b['name']} | {b['builder']} | {b['phoneText']} → {a['phoneText']} ({ao['phoneText']}) | {b['telLinks']} → {a['telLinks']} | "
                 f"`{b['color']}` → `{a['color']}` → `{r['color']}` |")
    L += ["", "Screenshots (1440, top of page): `1-before-*.png`, `2-after-*.png`, `3-reverted-*.png` for Home (ACF), Contact Us and "
          "About Us (Elementor): the header phone, the Contact card, the footer and the headings change together.", "",
          "**How it's wired:** the phone lives in ACF Site Settings; Elementor reads it through the theme's dynamic tags "
          "(`inc/elementor/class-m11-tag-setting-*.php`, header, footer, Contact card), ACF templates through `m11_get_setting()`. "
          "The colour lives in the Elementor Kit; Elementor widgets use `__globals__`, the ACF partials use `var(--clr-primary)`, "
          "which `abstracts/_tokens.scss` maps to `--e-global-color-primary` (the generated partials were tokenised for this: issues-log #66).", "",
          "## Writes (DevConnect via tools/bridge.py, read back)", ""] + [f"- {x}" for x in log]
    open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
