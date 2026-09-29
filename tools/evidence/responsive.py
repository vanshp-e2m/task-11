"""Responsive evidence: every page at 1440 / 768 / 430 next to its Figma frame (+ overflow checks at 390 and 1920).

    python tools/evidence/responsive.py            -> docs/evidence/responsive/<page>.png + README.md + results.json

Sheet columns: Figma desktop (1440) | WordPress 1440 | WordPress 768 | WordPress 430 | Figma mobile (430), all at the same scale (1/3),
so a height difference is a real height difference. Figma has no tablet frame, so 768 has no reference column (it is checked for
overflow and layout sanity only). 390 and 1920 are captured for overflow only (CLAUDE.md verification widths).
"""
import json
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "docs", "evidence", "responsive")
SHOTS = os.path.join(ROOT, "cache", "evidence", "responsive")
FIG = os.path.join(ROOT, "pages", "_figma", "frames", "export")
NODE_PATH = r"C:/Users/Vansh Patel/.claude/plugins/cache/dev-command/dev-command/fbe821068e44/scripts/node_modules"
BASE = "http://task-11.local/"

# name: (path, figma desktop, figma mobile, login, builder)
PAGES = {
    "home": ("", "HP with Copy - Approved", "HP - m", None, "ACF"),
    "about-us": ("about-us/", "About Us with Copy - Approved", "About Us - m", None, "Elementor"),
    "contact-us": ("contact-us/", "Contact Us", "Contact Us - m", None, "Elementor"),
    "resources": ("resources/", "Resources", "Resources - m", None, "ACF"),
    "products": ("products/?f_category[]=head-holding-systems", "Product Browse", "Product Browse - m", None, "ACF"),
    "product-main": ("products/product-sugita-ii-head-frame/", "Product Page Main", "Product Page Main - m", None, "ACF (CPT)"),
    "product-a": ("products/product-lawtonelite-skull-base-set/", "Product Page Variation A", "Product Page Variation A - m", None, "ACF (CPT)"),
    "product-b": ("products/product-feather-blades/", "Product Page Variation B", "Product Page Variation B - m", None, "ACF (CPT)"),
    "sales-hub-login": ("sales-hub/", "Login Screen", "Login Screen - m", None, "ACF"),
    "dashboard": ("sales-hub/dashboard/", "Dashboard", "Dashboard - m", "rep", "ACF"),
    "resource-library": ("sales-hub/resource-library/?f_type[]=brochure&f_type[]=spec-sheet&f_category[]=head-holding-systems",
                         "Resource Library", "Resource Library- m", "rep", "ACF"),
}
SHEET_W = (1440, 1440, 768, 430, 430)
SCALE = 1 / 3


def font(size):
    for f in ("C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def sheet(name, cols, labels):
    ims = []
    for path, w in zip(cols, SHEET_W):
        im = Image.open(path).convert("RGB")
        ims.append(im.resize((round(w * SCALE), round(im.height * w / im.width * SCALE)), Image.LANCZOS))
    gap, head = 16, 56
    W = sum(i.width for i in ims) + gap * (len(ims) + 1)
    H = max(i.height for i in ims) + head + gap
    s = Image.new("RGB", (W, H), (236, 239, 243))
    d = ImageDraw.Draw(s)
    x = gap
    for im, lab in zip(ims, labels):
        d.text((x, 10), lab, fill=(0, 40, 66), font=font(15))
        s.paste(im, (x, head))
        x += im.width + gap
    s.save(os.path.join(OUT, f"{name}.png"), optimize=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(SHOTS, exist_ok=True)
    jobs = []
    for name, (path, _, _, login, _) in PAGES.items():
        for w in (1440, 768, 430):
            jobs.append({"url": BASE + path, "out": os.path.join(SHOTS, f"{name}-{w}.png"), "width": w, "login": login, "page": name})
        for w in (390, 1920):
            jobs.append({"url": BASE + path, "out": None, "width": w, "login": login, "page": name})
    jf, rf = os.path.join(SHOTS, "jobs.json"), os.path.join(OUT, "results.json")
    json.dump(jobs, open(jf, "w"), indent=1)
    subprocess.run(["node", os.path.join(ROOT, "tools", "evidence", "shoot_many.js"), jf, rf], check=True,
                   env=dict(os.environ, NODE_PATH=NODE_PATH), cwd=ROOT)
    res = json.load(open(rf))
    rows = []
    for name, (path, fd, fm, _, builder) in PAGES.items():
        figd, figm = os.path.join(FIG, fd + ".png"), os.path.join(FIG, fm + ".png")
        cols = [figd] + [os.path.join(SHOTS, f"{name}-{w}.png") for w in (1440, 768, 430)] + [figm]
        sheet(name, cols, ["Figma 1440", "WordPress 1440", "WordPress 768 (no Figma frame)", "WordPress 430", "Figma 430"])
        r = {x["width"]: x for x in res if x["page"] == name}
        fh = (Image.open(figd).height, Image.open(figm).height)
        rows.append((name, builder, fh, r))
    lines = ["# Responsive evidence", "",
             "Each sheet: **Figma 1440 | WordPress 1440 | WordPress 768 | WordPress 430 | Figma 430**, all at 1/3 scale (heights comparable).",
             "Figma has no tablet frame, so 768 is judged on layout sanity + overflow only. Page heights include the header and footer.",
             "Overflow = `documentElement.scrollWidth > viewport` (horizontal scrollbar), also checked at 390 and 1920.", "",
             "| Page | Builder | Figma 1440 h | WP 1440 h | WP 768 h | Figma 430 h | WP 430 h | Overflow 390/430/768/1440/1920 | Sheet |",
             "|---|---|---|---|---|---|---|---|---|"]
    for name, builder, (fd, fm), r in rows:
        ov = "/".join("✗ " + str(r[w]["scrollW"]) if r[w]["overflow"] else "✓" for w in (390, 430, 768, 1440, 1920))
        lines.append(f"| {name} | {builder} | {fd} | {r[1440]['H']} | {r[768]['H']} | {fm} | {r[430]['H']} | {ov} | [{name}.png]({name}.png) |")
    lines += ["", "Notes: Figma frame heights include the drawn header/footer; small height differences come from the shared chrome",
              "(the WordPress footer is one Theme Builder template for every page, the frames differ slightly) and from filter/listing",
              "pages rendering real query results. Per-section pixel diffs against the HTML replicas are in",
              "`docs/evidence/flow-a/wp-vs-replica/report.json` and `docs/evidence/flow-b/contact/wp-vs-replica.txt`."]
    open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines[7:]))


if __name__ == "__main__":
    main()
