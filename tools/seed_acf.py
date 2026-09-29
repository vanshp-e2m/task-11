"""Push DevCommand's seed content (output/theme/module11/seed/, html-theme-assembler) into WordPress through DevConnect.

    python tools/seed_acf.py [--phase media|posts|terms|fields|pages|options|verify|all]

Why this script exists: DevCommand's own deployer (skills/html-deploy/scripts/deploy_theme.py) can't consume the assembler's
seed — its media phase crashes on the assembler's list-shaped media-manifest.json and its pages/seed phases plan 0 writes (and
it has no custom-post-type phase) — see issues-log #57. So the SAME seed is pushed here with DevConnect abilities:
  media   dev/upload-media (base64)                      → attachment ids
  posts   dev/create-custom-post (m11_resource, m11_product, publish, slug)
  terms   WP-CLI `wp post term set` (the bridge has no term-assignment ability)
  fields  dev/acf-read-write-values write, one field per call (CPT posts)
  pages   page template via WP-CLI (_wp_page_template), then ONE acf write of the whole `sections` array per page
  options dev/acf-read-write-values write on "options"
  verify  dev/acf-read-write-values read_all + compare every written value (list printed; issues-log rule #16)
Writes go through tools/bridge.py (the payloads — 92 base64 images, whole FC arrays — are the "oversized" case in CLAUDE.md);
every call is appended to cache/seed-log.jsonl and the ids to cache/seed-state.json, so re-runs are idempotent.
"""
import base64
import re
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from bridge import dispatch  # noqa: E402

SEED = os.path.join(ROOT, "output", "theme", "module11", "seed")
STATE_F = os.path.join(ROOT, "cache", "seed-state.json")
LOG_F = os.path.join(ROOT, "cache", "seed-log.jsonl")
PAGES = {"home": 14, "resources": 17, "products": 89, "sales-hub-login": 18, "sales-hub-dashboard": 19, "sales-hub-resource-library": 20}
REL_KEYS = {"videos", "brochure_cards", "product", "product_object"}
TAX = ("product_category", "procedure", "product_configuration", "resource_type")
SKIP = {"slug", "title"} | set(TAX)

state = json.load(open(STATE_F, encoding="utf-8")) if os.path.exists(STATE_F) else {"media": {}, "posts": {}, "fields": {}, "pages": {}}


def save():
    json.dump(state, open(STATE_F, "w", encoding="utf-8"), indent=1)


def call(ability, params, note=""):
    for attempt in range(3):
        try:
            res = dispatch(ability, params)
            break
        except Exception as e:  # noqa: BLE001
            if attempt == 2:
                raise
            time.sleep(1.5)
    with open(LOG_F, "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": time.strftime("%H:%M:%S"), "ability": ability, "note": note,
                            "params": {k: (v if k != "data" else f"<{len(v)} b64>") for k, v in params.items() if k != "value"},
                            "result": res if not isinstance(res, dict) or len(json.dumps(res)) < 400 else "<ok>"}) + "\n")
    return res


def load(name):
    return json.load(open(os.path.join(SEED, "content", name), encoding="utf-8"))


def wp(*args):
    return subprocess.run(["bash", os.path.join(ROOT, "tools", "wp.sh"), *args], capture_output=True, text=True, cwd=ROOT).stdout.strip()


def resolve(v, key=None):
    """seed image paths → attachment ids; relationship slugs → post ids (recursively)."""
    if isinstance(v, dict):
        return {k: resolve(x, k) for k, x in v.items()}
    if isinstance(v, list):
        return [resolve(x, key) for x in v]
    if isinstance(v, str):
        # The assembler seeded the replica's inline <br class="d-only"> markup; the templates build those line breaks from
        # NEWLINES (m11_multiline) and escape everything else, so the field value must carry a newline (issues-log #58).
        v = re.sub(r"<br\b[^>]*>", "\n", v)
        if v.startswith("seed/images/"):
            return state["media"].get(v, "")
        if key in REL_KEYS and v in state["posts"]:
            return state["posts"][v]
    return v


def media():
    mm = json.load(open(os.path.join(SEED, "media-manifest.json"), encoding="utf-8"))
    for e in mm:
        rel = e["file"]
        if rel in state["media"]:
            continue
        data = base64.b64encode(open(os.path.join(os.path.dirname(SEED), rel.replace("/", os.sep)) if not os.path.isabs(rel) else rel, "rb").read()).decode()
        r = call("dev/upload-media", {"filename": os.path.basename(rel), "data": data, "alt": e.get("alt", "")}, rel)
        state["media"][rel] = r.get("attachment_id") or r.get("id") or r.get("media_id")
        save()
    print("media:", len(state["media"]))


def posts():
    for fname, ptype in (("cpt-m11_resource.json", "m11_resource"), ("cpt-m11_product.json", "m11_product")):
        for p in load(fname):
            if p["slug"] in state["posts"]:
                continue
            r = call("dev/create-custom-post", {"post_type": ptype, "title": p["title"], "slug": p["slug"], "status": "publish"}, p["slug"])
            state["posts"][p["slug"]] = r.get("post_id") or r.get("id")
            save()
    print("posts:", len(state["posts"]))


def terms():
    for fname in ("cpt-m11_resource.json", "cpt-m11_product.json"):
        for p in load(fname):
            pid = str(state["posts"][p["slug"]])
            for tax in TAX:
                val = p.get(tax)
                if val:
                    wp("post", "term", "set", pid, tax, *(val if isinstance(val, list) else [val]), "--by=slug")
    print("terms assigned")


def fields():
    for fname in ("cpt-m11_resource.json", "cpt-m11_product.json"):
        for p in load(fname):
            pid = state["posts"][p["slug"]]
            for k, v in p.items():
                if k in SKIP or k.startswith("_"):
                    continue
                tag = f"{p['slug']}:{k}"
                if state["fields"].get(tag):
                    continue
                call("dev/acf-read-write-values", {"action": "write", "post_id": pid, "field_key_or_name": k, "value": resolve(v, k)}, tag)
                state["fields"][tag] = True
            save()
    print("fields written:", len(state["fields"]))


def pages():
    for spec_slug, pid in PAGES.items():
        wp("post", "meta", "update", str(pid), "_wp_page_template", "templates/page-flexible.php")
        rows = resolve(load(f"{spec_slug}.json"))
        # common_settings is a SEAMLESS clone: ACF stores its sub-fields directly on the row, and silently ignores a nested
        # {"common_settings": {...}} object — so sec_id / hide_section were never saved (issues-log #58). Flatten it.
        for row in rows:
            if isinstance(row.get("common_settings"), dict):
                row.update(row.pop("common_settings"))
        call("dev/acf-read-write-values", {"action": "write", "post_id": pid, "field_key_or_name": "field_m11_sections", "value": rows}, f"page {pid} sections")
        state["pages"][spec_slug] = {"id": pid, "rows": len(rows)}
        save()
    print("pages:", state["pages"])


def options():
    for k, v in load("options.json").items():
        call("dev/acf-read-write-values", {"action": "write", "post_id": "options", "field_key_or_name": k, "value": v}, f"options:{k}")
    print("options written")


def verify():
    bad = []
    for spec_slug, pid in PAGES.items():
        got = dispatch("dev/acf-read-write-values", {"action": "read", "post_id": pid, "field_key_or_name": "sections", "format_value": False})
        val = got.get("value") if isinstance(got, dict) else got
        n = len(val) if isinstance(val, list) else 0
        want = len(load(f"{spec_slug}.json"))
        print(f"page {pid:>3} {spec_slug:28s} rows stored {n} / seeded {want}")
        if n != want:
            bad.append(spec_slug)
    for fname in ("cpt-m11_product.json", "cpt-m11_resource.json"):
        for p in load(fname):
            pid = state["posts"][p["slug"]]
            got = dispatch("dev/acf-read-write-values", {"action": "read_all", "post_id": pid, "format_value": False})
            vals = got.get("fields", got) if isinstance(got, dict) else {}
            miss = [k for k, v in p.items() if k not in SKIP and not k.startswith("_") and v not in ("", [], None, False)
                    and not vals.get(k)]
            if miss:
                bad.append(f"{p['slug']}: {miss}")
    print("verify problems:", bad or "none")
    return bad


if __name__ == "__main__":
    phase = sys.argv[sys.argv.index("--phase") + 1] if "--phase" in sys.argv else "all"
    steps = {"media": media, "posts": posts, "terms": terms, "fields": fields, "pages": pages, "options": options, "verify": verify}
    for name in (steps if phase == "all" else [phase]):
        steps[name]()
