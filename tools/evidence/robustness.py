"""Robustness evidence: double-length headings, empty optional fields and wrong-ratio images, for every ACF layout and the product template.

    python tools/evidence/robustness.py setup     # test images + private test pages/products, filled from the REAL seeded content
    python tools/evidence/robustness.py check     # capture originals + test pages at 1440 / 430, measure, write the report

How the three test cases are made (all through DevConnect, tools/bridge.py; every write is read back and listed in the report):
  long   every heading-like text field (heading/title/label/name/kicker/quote/…) doubled: "X" -> "X X"
  empty  every field emptied except the section id and the section's FIRST text field (so each section is still identifiable)
  ratio  every image swapped for a deliberately wrong-ratio image: 600x1800 (1:3 portrait) and 2400x400 (6:1 banner), alternating
Pages: the rows of all six Flexible Content pages (19 layouts) in one private page per case. Products: variant A (the richest:
gallery, specs, instruments table, accessories, related) cloned into one private product per case.
Checks (tools/evidence/robust_check.js): horizontal page overflow, clipped text, elements sticking out of their section, empty
headings/links/images in the markup, PHP notices, and — for "ratio" — whether every image box kept the size it has on the real page.
"""
import base64
import io
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bridge import dispatch  # noqa: E402

OUT = os.path.join(ROOT, "docs", "evidence", "robustness")
CACHE = os.path.join(ROOT, "cache", "evidence", "robustness")
STATE_F = os.path.join(CACHE, "state.json")
NODE_PATH = r"C:/Users/Vansh Patel/.claude/plugins/cache/dev-command/dev-command/fbe821068e44/scripts/node_modules"
ACF = os.path.join(ROOT, "wp-content", "themes", "module11", "acf-json")
SOURCE_PAGES = {14: "", 17: "resources/", 89: "products/", 18: "sales-hub/", 19: "sales-hub/dashboard/", 20: "sales-hub/resource-library/"}
LOGIN = {18: None, 19: "rep", 20: "rep"}
SOURCE_PRODUCT = 231
CASES = ("long", "empty", "ratio")
HEAD = re.compile(r"(head|title|label|name|kicker|eyebrow|quote|caption|pill|badge|h1|h2|cta)", re.I)

state = json.load(open(STATE_F)) if os.path.exists(STATE_F) else {}


def save():
    os.makedirs(CACHE, exist_ok=True)
    json.dump(state, open(STATE_F, "w"), indent=1)


def wp(*a):
    return subprocess.run(["bash", os.path.join(ROOT, "tools", "wp.sh"), *a], capture_output=True, text=True, cwd=ROOT).stdout.strip()


# ------------------------------------------------------------------ field map (key and name -> field definition)
FIELDS = {}


def index(fields):
    for f in fields:
        if f.get("key"):
            FIELDS[f["key"]] = f
        if f.get("name"):
            FIELDS.setdefault("name:" + f["name"], f)
        index(f.get("sub_fields", []))
        lays = f.get("layouts", [])
        for lay in (lays.values() if isinstance(lays, dict) else lays):
            index(lay.get("sub_fields", []))


for fn in os.listdir(ACF):
    if fn.endswith(".json"):
        index(json.load(open(os.path.join(ACF, fn), encoding="utf-8")).get("fields", []))


def fdef(key):
    """Resolve a raw row key: plain field key, seamless-clone composite key (<clone>_field_<inner>), or a top-level name."""
    if key in FIELDS:
        return FIELDS[key]
    if "_field_" in key:
        inner = "field_" + key.rsplit("_field_", 1)[1]
        if inner in FIELDS:
            return FIELDS[inner]
    return FIELDS.get("name:" + key, {})


def is_id(key, f):
    n = f.get("name", key)
    return n in ("sec_id", "hide_section") or key.endswith("sec_id") or key.endswith("hide_section") or key == "acf_fc_layout"


# ------------------------------------------------------------------ mutations
def mutate(case, value, key="", imgs=None, keep=None):
    f = fdef(key) if key else {}
    t = f.get("type")
    if isinstance(value, list):
        if case == "empty" and t in ("repeater", "relationship", "gallery"):
            return []
        return [mutate(case, v, key, imgs, keep) for v in value]
    if isinstance(value, dict):
        if case == "empty" and t == "link":
            return ""
        if case == "long" and t == "link" and value.get("title"):
            return {**value, "title": value["title"] + " " + value["title"]}
        return {k: mutate(case, v, k, imgs, keep) for k, v in value.items()}
    if key == "acf_fc_layout" or is_id(key, f):
        return value
    if case == "long" and t in ("text", "textarea") and isinstance(value, str) and value and HEAD.search(f.get("name", key)):
        return value + " " + value
    if case == "empty" and t in ("text", "textarea", "url", "image", "link", "wysiwyg", "email", "file"):
        return value if keep is not None and key in keep else ""
    if case == "ratio" and t in ("image", "file") and value:
        imgs["n"] += 1
        return imgs["ids"][imgs["n"] % 2]
    return value


def first_text_keys(row):
    for k, v in row.items():
        if fdef(k).get("type") in ("text", "textarea") and isinstance(v, str) and v and not is_id(k, fdef(k)):
            return {k}
    return set()


def test_image(w, h, label):
    im = Image.new("RGB", (w, h), (255, 196, 0))
    d = ImageDraw.Draw(im)
    for i in range(0, max(w, h) * 2, 80):
        d.line([(i, 0), (i - h, h)], fill=(20, 20, 20), width=18)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", max(28, min(w, h) // 6))
    except OSError:
        font = ImageFont.load_default()
    d.rectangle([w // 2 - min(w, h) // 1.2, h // 2 - min(w, h) // 5, w // 2 + min(w, h) // 1.2, h // 2 + min(w, h) // 5], fill=(255, 255, 255))
    d.text((w // 2, h // 2), label, fill=(200, 0, 0), font=font, anchor="mm")
    b = io.BytesIO()
    im.save(b, "JPEG", quality=85)
    return base64.b64encode(b.getvalue()).decode()


def setup():
    state.setdefault("writes", [])
    if "images" not in state:
        ids = []
        for w, h, lab in ((600, 1800, "1:3"), (2400, 400, "6:1")):
            r = dispatch("dev/upload-media", {"filename": f"qa-wrong-ratio-{w}x{h}.jpg", "data": test_image(w, h, lab), "alt": f"QA wrong-ratio test image {lab}"})
            ids.append(str(r.get("attachment_id") or r.get("id") or r.get("media_id")))
            state["writes"].append(f"dev/upload-media qa-wrong-ratio-{w}x{h}.jpg -> {ids[-1]}")
        state["images"] = ids
        save()
    rows = []
    for pid in SOURCE_PAGES:
        got = dispatch("dev/acf-read-write-values", {"action": "read", "post_id": pid, "field_key_or_name": "sections", "format_value": False})
        rows += got.get("value") or []
    src_product = dispatch("dev/acf-read-write-values", {"action": "read_all", "post_id": SOURCE_PRODUCT, "format_value": False}).get("fields", {})
    src_title = wp("post", "get", str(SOURCE_PRODUCT), "--field=post_title")
    terms = {tax: wp("post", "term", "list", str(SOURCE_PRODUCT), tax, "--field=slug").split() for tax in ("product_category", "procedure", "product_configuration")}
    for case in CASES:
        imgs = {"ids": state["images"], "n": -1}
        # ---- page
        key = f"page:{case}"
        if key not in state:
            r = dispatch("dev/create-page", {"title": f"QA robustness — {case}", "status": "draft"})
            pid = r.get("page_id")
            wp("post", "update", str(pid), "--post_status=private", f"--post_name=qa-robustness-{case}")
            wp("post", "meta", "update", str(pid), "_wp_page_template", "templates/page-flexible.php")
            state[key] = pid
            state["writes"].append(f"dev/create-page 'QA robustness — {case}' -> {pid} (then WP-CLI: private, slug, Flexible template)")
            save()
        pid = state[key]
        mrows = [mutate(case, row, "", imgs, first_text_keys(row) if case == "empty" else None) for row in rows]
        dispatch("dev/acf-read-write-values", {"action": "write", "post_id": pid, "field_key_or_name": "field_m11_sections", "value": mrows})
        back = dispatch("dev/acf-read-write-values", {"action": "read", "post_id": pid, "field_key_or_name": "sections", "format_value": False}).get("value") or []
        state[f"verify:{key}"] = {"rows_written": len(mrows), "rows_read_back": len(back), "layouts": sorted({r["acf_fc_layout"] for r in back})}
        state["writes"].append(f"dev/acf-read-write-values write sections on {pid}: {len(mrows)} rows, read back {len(back)}")
        # ---- product
        key = f"product:{case}"
        title = src_title + " " + src_title if case == "long" else src_title
        if key not in state:
            r = dispatch("dev/create-custom-post", {"post_type": "m11_product", "title": title, "slug": f"qa-robustness-{case}", "status": "publish"})
            ppid = r.get("post_id") or r.get("id")
            wp("post", "update", str(ppid), "--post_status=private")
            for tax, slugs in terms.items():
                if slugs:
                    wp("post", "term", "set", str(ppid), tax, *slugs, "--by=slug")
            state[key] = ppid
            state["writes"].append(f"dev/create-custom-post m11_product '{title[:40]}…' -> {ppid} (then WP-CLI: private, terms copied)")
            save()
        ppid = state[key]
        bad = []
        for name, value in src_product.items():
            if case == "empty" and name in ("has_instruments_table", "has_size_guide"):
                v = value  # the variant switch is structure, not content
            else:
                v = mutate(case, value, name, imgs, {"instruments_heading"} if case == "empty" else None)
            dispatch("dev/acf-read-write-values", {"action": "write", "post_id": ppid, "field_key_or_name": name, "value": v})
        back = dispatch("dev/acf-read-write-values", {"action": "read_all", "post_id": ppid, "format_value": False}).get("fields", {})
        for name in src_product:
            want = src_product[name]
            if case == "empty" and fdef(name).get("type") in ("text", "textarea", "image") and name not in ("instruments_heading",) and back.get(name):
                bad.append(name)
            if case == "long" and fdef(name).get("type") == "text" and HEAD.search(name) and want and back.get(name) != want + " " + want:
                bad.append(name)
        state[f"verify:{key}"] = {"fields_written": len(src_product), "mismatches": bad}
        state["writes"].append(f"dev/acf-read-write-values write x{len(src_product)} on product {ppid}; read-back mismatches: {bad or 'none'}")
        save()
    print(json.dumps({k: v for k, v in state.items() if k != "writes"}, indent=1))


def check():
    os.makedirs(OUT, exist_ok=True)
    jobs = []
    for pid, path in SOURCE_PAGES.items():
        for w in (1440, 430):
            jobs.append({"kind": "orig", "src": pid, "url": f"http://task-11.local/{path}", "width": w, "login": LOGIN.get(pid)})
    for w in (1440, 430):
        jobs.append({"kind": "orig", "src": "product", "url": "http://task-11.local/?p=%d" % SOURCE_PRODUCT, "width": w})
    for case in CASES:
        for w in (1440, 430):
            jobs.append({"kind": case, "src": "page", "url": "http://task-11.local/?page_id=%d" % state[f"page:{case}"], "width": w,
                         "login": "editor", "out": os.path.join(OUT, f"page-{case}-{w}.png")})
            jobs.append({"kind": case, "src": "product", "url": "http://task-11.local/?p=%d" % state[f"product:{case}"], "width": w,
                         "login": "editor", "out": os.path.join(OUT, f"product-{case}-{w}.png")})
    jf, rf = os.path.join(CACHE, "jobs.json"), os.path.join(CACHE, "results.json")
    json.dump(jobs, open(jf, "w"), indent=1)
    subprocess.run(["node", os.path.join(ROOT, "tools", "evidence", "robust_check.js"), jf, rf], check=True,
                   env=dict(os.environ, NODE_PATH=NODE_PATH), cwd=ROOT)
    res = json.load(open(rf))
    # originals in the same order as the test page's rows (Home, Resources, Products, Login, Dashboard, Library); section ids repeat
    # across pages (Home and Resources both have #testimonials), so match by (id, occurrence), not by id alone
    orig, seen = {}, {}
    for r in res:
        if r["kind"] == "orig":
            src = "product" if r["src"] == "product" else "page"
            for s in r["secs"]:
                n = seen.get((src, r["width"], s["id"]), 0)
                seen[(src, r["width"], s["id"])] = n + 1
                orig[(src, r["width"], s["id"], n)] = s
    lines = ["# Robustness evidence", "",
             "Real seeded content, three deliberate abuses, every ACF layout (19) + the product template. Built by "
             "`tools/evidence/robustness.py` (setup: private test pages/products through DevConnect; check: measured at 1440 and 430).", "",
             "| Case | What was done to the content |", "|---|---|",
             "| **long** | every heading-like field doubled (`X` → `X X`), product title doubled |",
             "| **empty** | every optional field emptied except the section id and the section's first text field |",
             "| **ratio** | every image replaced by a 600×1800 (1:3) or 2400×400 (6:1) test image |", "",
             "Pass rules: no horizontal page overflow · no clipped text · nothing sticking out of its section · no empty "
             "`<h*>`/`<a>`/`<img src=\"\">` in the markup · no PHP notices · (ratio) every image box keeps the size it has on the real page.", ""]
    summary = []
    for case in CASES:
        for src in ("page", "product"):
            for w in (1440, 430):
                r = next(x for x in res if x["kind"] == case and x["src"] == src and x["width"] == w)
                lines.append(f"## {case} · {'all Flexible Content layouts' if src == 'page' else 'product template (variant A)'} · {w}px")
                lines.append(f"Page overflow: **{'YES ' + str(r['scrollW']) if r['scrollW'] > r['vw'] else 'none'}** · PHP notices: **{r['php']}** · "
                             f"screenshot: [{src}-{case}-{w}.png]({src}-{case}-{w}.png)")
                lines.append("")
                lines.append("| Section | height (orig → test) | clipped text | sticking out | empty tags | images (box vs real page) | verdict |")
                lines.append("|---|---|---|---|---|---|---|")
                occ = {}
                for s in r["secs"]:
                    n = occ.get(s["id"], 0)
                    occ[s["id"]] = n + 1
                    o = orig.get((src, w, s["id"], n))
                    img_note, img_ok = "—", True
                    if s["imgs"]:
                        if case == "ratio" and o and o["imgs"]:
                            same = sum(1 for a, b in zip(s["imgs"], o["imgs"]) if abs(a["w"] - b["w"]) <= 2 and abs(a["h"] - b["h"]) <= 2)
                            n = min(len(s["imgs"]), len(o["imgs"]))
                            fits = sorted({i["fit"] for i in s["imgs"]})
                            img_ok = same == n
                            img_note = f"{same}/{n} boxes unchanged, object-fit {','.join(fits)}"
                        else:
                            img_note = f"{len(s['imgs'])} images"
                    e = s["empty"]
                    empties = e["headings"] + e["links"] + e["imgs"]
                    ok = not s["clipped"] and not s["sticking"] and empties == 0 and img_ok
                    summary.append((case, src, w, s["id"], ok))
                    lines.append(f"| {s['id']} | {o['h'] if o else '—'} → {s['h']} | {', '.join(s['clipped']) or '—'} | "
                                 f"{', '.join(s['sticking']) or '—'} | {empties or '—'} | {img_note} | {'✅' if ok else '❌'} |")
                lines.append("")
    fails = [x for x in summary if not x[4]]
    lines[2:2] = [f"**Result: {len(summary) - len(fails)}/{len(summary)} section checks pass.** Failures are listed per case below and in "
                  "`docs/issues-log.md` with their fixes.", ""]
    lines += ["## What the numbers did not catch (visual review of the screenshots)", "",
              "The first run passed every automated check while the **long** page was visibly broken: the automated checks look for",
              "HORIZONTAL problems, and the failure was VERTICAL. The Home layouts (and Browse by procedure) were built from Figma",
              "coordinates with `position:absolute`, so a doubled heading ran over the cards/text under it, and fixed-height",
              "`nowrap` labels (hero pills, value-column kickers, Watch now / Continue your visit / account buttons) spilled out.",
              "Fixes (issues-log #65): `tools/figma_html/flow_desktop.py` turns the measured coordinates into row grids (same pixels",
              "at the drawn content, rows grow with their content; Home stays 0–3.7% vs the replica, heights +0), and",
              "`assets/scss/base/_robustness-guards.scss` lets the fixed labels wrap. Two defects the checks DID catch are fixed",
              "too: the Dashboard icon box stretched to 252px with a 1:3 upload (now a fixed 70×61 box, object-fit contain), and",
              "editors could not preview Sales Hub pages (#64). A layout reused on another page lost its styles (#63).",
              "Accepted as designed: **empty** sections with fixed Figma heights keep their drawn height (clean, just spacious);",
              "the Resources video tiles and product accessories take their images/titles from the linked posts, so those rows",
              "don't change in the long/ratio cases.", ""]
    lines += ["## Writes made for this test (listed + read back, CLAUDE.md rule #16)", ""] + [f"- {w}" for w in state.get("writes", [])]
    lines += ["", "The test pages/products are **private** (`qa-robustness-*`), so visitors never see them; an editor can open them to repeat the check."]
    open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"{len(summary) - len(fails)}/{len(summary)} pass")
    for f in fails:
        print("FAIL", f)


if __name__ == "__main__":
    {"setup": setup, "check": check}[sys.argv[1]]()
