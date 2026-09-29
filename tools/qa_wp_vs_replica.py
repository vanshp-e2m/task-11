"""Flow A fidelity gate: every ACF-built WordPress page vs its generated-HTML replica, section by section.

    python tools/qa_wp_vs_replica.py [page ...] [--widths 1440,430]

Sections are matched by id (the templates print the seeded sec_id = the replica's section id). For each: height delta and the
% of pixels differing by >32 in any channel (same threshold as tools/about/compare.py). Header/footer are excluded: in
WordPress they're the Elementor Theme Builder templates, checked separately. Evidence → docs/evidence/flow-a/wp-vs-replica/.
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "evidence", "flow-a", "wp-vs-replica")
NODE_PATH = r"C:/Users/Vansh Patel/.claude/plugins/cache/dev-command/dev-command/fbe821068e44/scripts/node_modules"
REP = "http://127.0.0.1:8767/{}/html/"
WP = "http://task-11.local/{}"
PAIRS = {  # name: (wp path, replica slug, needs login)
    "home": ("mizuho-home/", "mizuho-home", False),
    "resources": ("resources/", "resources", False),
    "products": ("products/?f_category[]=head-holding-systems", "product-browse", False),  # the drawn filter state
    "product-main": ("products/product-sugita-ii-head-frame/", "product-main", False),
    "product-a": ("products/product-lawtonelite-skull-base-set/", "product-variation-a", False),
    "product-b": ("products/product-feather-blades/", "product-variation-b", False),
    "login": ("sales-hub/", "sales-hub-login", False),
    "dashboard": ("sales-hub/dashboard/", "sales-hub-dashboard", True),
    "contact": ("contact-us/", "contact-us", False),
    "library": ("sales-hub/resource-library/?f_type[]=brochure&f_type[]=spec-sheet&f_category[]=head-holding-systems", "resource-library", True),
}


def shoot(url, path, w, login):
    env = dict(os.environ, NODE_PATH=NODE_PATH)
    r = subprocess.run(["node", os.path.join(ROOT, "tools", "qa_sections.js"), url, path, str(w)] + (["1"] if login else []),
                       capture_output=True, text=True, env=env, cwd=ROOT)
    return json.loads(r.stdout.strip().splitlines()[-1])


def main():
    argv = sys.argv[1:]
    widths = [1440, 430]
    if "--widths" in argv:
        i = argv.index("--widths")
        widths = [int(x) for x in argv[i + 1].split(",")]
        argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith("--")]
    os.makedirs(OUT, exist_ok=True)
    report = {}
    for name in args or PAIRS:
        wp_path, rep_slug, login = PAIRS[name]
        for w in widths:
            a_png, b_png = os.path.join(OUT, f"{name}-{w}-wp.png"), os.path.join(OUT, f"{name}-{w}-replica.png")
            wp = shoot(WP.format(wp_path), a_png, w, login)
            rp = shoot(REP.format(rep_slug), b_png, w, False)
            A, B = Image.open(a_png).convert("RGB"), Image.open(b_png).convert("RGB")
            rsec = {s["id"]: s for s in rp["secs"] if s["id"] not in ("site-header", "site-footer")}
            rows = []
            for s in wp["secs"]:
                if s["id"] not in rsec:
                    continue
                r = rsec[s["id"]]
                h = min(s["h"], r["h"])
                if h <= 0:
                    continue
                ca = A.crop((0, s["top"], min(A.width, B.width), s["top"] + h))
                cb = B.crop((0, r["top"], min(A.width, B.width), r["top"] + h))
                d = np.asarray(ImageChops.difference(ca, cb)).max(axis=2) > 32
                rows.append({"id": s["id"], "dh": s["h"] - r["h"], "diff": round(100 * d.mean(), 2)})
            missing = sorted(set(rsec) - {s["id"] for s in wp["secs"]})
            report[f"{name}@{w}"] = {"wp_width": wp["W"], "url": wp["url"], "sections": rows, "missing_in_wp": missing}
            worst = max((x["diff"] for x in rows), default=0)
            print(f"{name:12s} {w:>4} W={wp['W']:<5} sections={len(rows)} missing={missing} worst={worst}%  "
                  + " ".join(f"{x['id']}:{x['diff']}%/{x['dh']:+d}" for x in rows))
    json.dump(report, open(os.path.join(OUT, "report.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
