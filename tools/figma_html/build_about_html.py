"""About Us HTML replica → pages/about-us/html/ (index.html + css/styles.css), the same "generated HTML" stage as every other page.

About was built the other way round (straight to native Elementor, page 15, before the "HTML first" rule), so its verified
content + geometry already live in two files: the native tree (pages/about-us/elementor/about.json, copy verbatim from Figma 1:161)
and the theme partial (assets/scss/pages/_about.scss, Figma 1:161 desktop / 1:2237 mobile). This script turns that tree into clean
semantic HTML with the same au-* classes and compiles the partial on its own:
  * container → <div class="box au-…">; heading → <hN class="wgt-title">; text-editor → <div>; image → <img>; button → <a>;
  * Elementor's wrapper classes are renamed to neutral ones in BOTH the markup and the CSS
    (.e-con → .box, .elementor-widget → .wgt, .elementor-heading-title → .wgt-title, .elementor-button → .wbtn …);
  * the two Elementor background images (hero, map) become CSS backgrounds; the Font Awesome arrow becomes an inline SVG.
Header/footer = Home's (chrome.py) with "About Mizuho America" current. Compiled by DevCommand's compiler like the rest.

    python tools/figma_html/build_about_html.py
"""
import json
import os
import re
import subprocess
from html import escape

from chrome import FOOT_CSS, FOOT_HTML, HEADER_CSS, HEADER_HTML, HEADER_JS, ROOT, SHARED, link_pages
from replica_lib import compile_page

SLUG = "about-us"
TREE = json.load(open(os.path.join(ROOT, "pages/about-us/elementor/about.json"), encoding="utf-8"))
MEDIA = json.load(open(os.path.join(ROOT, "pages/about-us/figma/images/wp-media.json"), encoding="utf-8"))
BY_ID = {v["id"]: k for k, v in MEDIA.items()}
BY_ID.update({64: "about-hero-portrait", 87: "about-map-clean", 88: "about-hero-clean"})
IMG_DIR = os.path.join(ROOT, "pages/about-us/figma/images")
LOCAL = {os.path.splitext(f)[0]: f for f in os.listdir(IMG_DIR) if f.lower().endswith((".jpg", ".png"))}
RENAME = [(".elementor-button-content-wrapper", ".wbtn-inner"), (".elementor-button-icon", ".wbtn-icon"), (".elementor-button", ".wbtn"),
          (".elementor-heading-title", ".wgt-title"), (".elementor-widget-image", ".wgt-image"), (".elementor-widget", ".wgt"), (".e-con", ".box")]
ARROW = ('<svg class="wbtn-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" width="12" height="16" aria-hidden="true">'
         '<path fill="currentColor" d="M169.4 470.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 370.8 224 64c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 306.7L54.6 265.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z"/></svg>')
bg_rules = []


def local_img(ref):
    key = BY_ID.get(ref.get("id"))
    if key not in LOCAL:
        key = os.path.splitext(os.path.basename(ref["url"]))[0]
    return "figma/images/" + LOCAL[key]


def helpers(cls):
    """About's show/hide helpers → chrome's shared utilities (.m-only hidden on desktop, .d-only hidden on mobile)."""
    return cls.replace("au-m-only", "au-m-only m-only").replace("au-br-d", "au-br-d d-only").replace("au-qmark", "au-qmark d-only")


def render(n):
    s = n["settings"]
    if n["elType"] == "container":
        cls = helpers(s.get("css_classes", ""))
        idattr = f' id="{s["_element_id"]}"' if s.get("_element_id") else ""
        if s.get("background_image"):
            first = cls.split()[0]
            bg_rules.append(f'.{first} {{ background-image: url("../{local_img(s["background_image"])}"); }}')
        return f'<div class="box {cls}"{idattr}>' + "".join(render(c) for c in n["elements"]) + "</div>"
    t, cls = n["widgetType"], helpers(s.get("_css_classes", ""))
    if t == "heading":
        tag = s.get("header_size", "p")
        return f'<div class="wgt wgt-heading {cls}"><{tag} class="wgt-title">{s["title"]}</{tag}></div>'
    if t == "text-editor":
        return f'<div class="wgt wgt-text {cls}">{s["editor"]}</div>'
    if t == "image":
        src = local_img(s["image"])
        return f'<div class="wgt wgt-image {cls}"><img src="{src}" alt="{escape(s.get("alt", ""))}" loading="lazy"></div>'
    if t == "button":
        icon = f'<span class="wbtn-icon">{ARROW}</span>' if s.get("selected_icon") else ""
        href = s["link"]["url"] or "#"
        return (f'<div class="wgt wgt-button {cls}"><a class="wbtn" href="{escape(href)}"><span class="wbtn-inner">{icon}'
                f'<span class="wbtn-text">{escape(s["text"])}</span></span></a></div>')
    raise ValueError(t)


body = "".join(render(n) for n in TREE)
# the helpers also sit inside heading text (<br class="au-br-d">, <span class="au-qmark">), so map every class attribute
body = re.sub(r'class="([^"]*)"', lambda m_: 'class="' + " ".join(dict.fromkeys(helpers(m_.group(1)).split())) + '"', body)
body = link_pages(body.replace('href="http://task-11.local/about-us/"', 'href="#top"'))
# The tree is one root container; the compiler wants <section>s, so the root becomes the section.
m = re.match(r'<div class="box au"( id="[^"]*")?>', body)
assert m, body[:80]
body = '<section class="box au" id="about-us">' + body[m.end():-len("</div>")] + "</section>"

# ---------------------------------------------------------------- CSS: compile the theme partial alone, rename Elementor classes
scss_dir = os.path.join(ROOT, "wp-content/themes/module11/assets/scss")
entry = os.path.join(ROOT, "cache/tmp/about-standalone.scss")
open(entry, "w", encoding="utf-8").write('@use "abstracts/tokens";\n@use "pages/about";\n')
out = subprocess.run(["sass", "--no-source-map", "--style=expanded", f"--load-path={scss_dir}", entry], capture_output=True, text=True,
                     encoding="utf-8", shell=True)
if out.returncode:
    raise SystemExit(out.stderr)
css = out.stdout
for a, b in RENAME:
    css = re.sub(re.escape(a) + r"(?![\w-])", b, css)
# Tokens: the theme's :root maps --clr-*/--ff-* onto Elementor Kit globals with hex fallbacks. The replica has no Kit and the validator
# only reads the compiler's :root, so each token is replaced by its fallback literal; element-level vars get explicit fallbacks.
root = re.search(r":root\s*\{([^}]*)\}", css)
tokens = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", root.group(1)))
css = css[:root.start()] + css[root.end():]


def lit(v, depth=0):
    v = v.strip()
    m_ = re.fullmatch(r"var\((--[\w-]+)(?:,\s*(.+))?\)(.*)", v)
    if not m_ or depth > 5:
        return v
    name, fb, rest = m_.groups()
    base = lit(tokens[name], depth + 1) if name in tokens else (lit(fb, depth + 1) if fb else v)
    return base + rest


resolved = {k: lit(v) for k, v in tokens.items()}
for k in sorted(resolved, key=len, reverse=True):
    css = re.sub(r"var\(" + re.escape(k) + r"\)", resolved[k], css)
for k, fb in (("--u", "1px"), ("--tu", "1px"), ("--x0", "0px"), ("--mx", "0px")):
    css = re.sub(r"var\(" + re.escape(k) + r"\)", f"var({k}, {fb})", css)


def merge_identical(text):
    """Merge rules with identical bodies inside the same block (top level / one @media), into the first occurrence
    (DevCommand's validator hard-fails 3+ selectors sharing one body). Verified render-neutral by a 0-pixel diff."""
    def props(body):
        return {d.split(":")[0].strip() for d in body.split(";") if ":" in d}

    def merge_block(block):
        # A later rule may only move up into an earlier identical rule when NO rule in between sets any of the same
        # properties (otherwise the move changes the cascade: the first version of this turned the team names black).
        rules = [[sel.strip(), body] for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", block)]
        first = {}
        for i, (sel, body) in enumerate(rules):
            key = " ".join(body.split())
            if key in first:
                j = first[key]
                p = props(body)
                if all(not (props(rules[k][1]) & p) for k in range(j + 1, i) if rules[k][0]):
                    rules[j][0] += ", " + sel
                    rules[i][0] = ""
                    continue
            first[key] = i
        return "\n".join(f"{sel} {{{body}}}" for sel, body in rules if sel)
    out, i = [], 0
    for m_ in re.finditer(r"@media[^{]+\{((?:[^{}]*\{[^{}]*\})*)\s*\}", text):
        out.append(merge_block(text[i:m_.start()]))
        out.append(m_.group(0)[:m_.group(0).index("{") + 1] + "\n" + merge_block(m_.group(1)) + "\n}")
        i = m_.end()
    out.append(merge_block(text[i:]))
    return "\n".join(out)


css = merge_identical(css)
# Two repeats span sections (an About rule with the same body as a Home header/footer rule), so they're handled by hand:
#  * About's own show/hide helpers duplicate chrome's shared .m-only / .d-only utilities → use those, drop the partial's copies;
#  * the lone `.au .au-hero-quote { font-weight: 700 }` joins the later identical group (moving it DOWN is safe: nothing in between
#    matches the hero quote). Both verified render-neutral by a 0-pixel before/after diff at 1440 and 430.
css = re.sub(r"\.au \.au-m-only \{\s*display: none;\s*\}", "", css)
css = re.sub(r"\.au \.au-qmark,\s*\.au \.au-br-d \{\s*display: none;\s*\}", "", css)
css = re.sub(r"\.au \.au-hero-quote \{\s*font-weight: 700;\s*\}", "", css, count=1)
css = css.replace(".au .au-intro-text li,\n.au .au-member-name,", ".au .au-hero-quote,\n.au .au-intro-text li,\n.au .au-member-name,", 1)
assert ".au .au-hero-quote,\n.au .au-intro-text li" in css
# What Elementor's own base CSS gave the partial for free: containers are flex columns, images scale, buttons are inline-flex.
BASE = """
@font-face { font-family: 'Open Sans'; font-style: italic; font-weight: 300; font-stretch: 100%; font-display: swap; src: url(https://fonts.gstatic.com/s/opensans/v44/memtYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWqWuU6F.woff2) format('woff2'); unicode-range: U+0000-00FF, U+2000-206F; }
@media (min-width: 1024px) { .au-hero { margin-top: calc(18 * var(--u, 1px)); } }  /* _about.scss sits under Elementor's 179px header; chrome.py's is 161px */
.box { display: flex; flex-direction: column; box-sizing: border-box; }
.wgt-image img { display: block; max-width: 100%; height: auto; }
.wbtn { display: inline-flex; align-items: center; justify-content: center; text-decoration: none; }
.wbtn-inner { display: inline-flex; align-items: center; gap: 8px; }
.wbtn-svg { width: 12px; height: 16px; }
.au { background-size: cover; background-position: center; }
"""
css = BASE + "\n".join(bg_rules) + "\n" + css

HEAD = HEADER_HTML.replace('<a href="#about-mizuho-america">', '<a class="is-current" aria-current="page" href="#about-mizuho-america">', 1)
assert HEAD != HEADER_HTML
NOTE = ("2026-09-28 About Us HTML replica, generated from the verified native tree (pages/about-us/elementor/about.json) + the theme partial "
        "_about.scss by tools/figma_html/build_about_html.py (About was built in Elementor first; this adds the HTML stage the other pages have).")
SECTIONS = [
    {"id": "site-header", "landmark": "header", "escape_hatch": True, "html": HEAD, "css": SHARED + HEADER_CSS + ".site-head__nav a.is-current { color: #0065B3; }", "js": HEADER_JS},
    {"id": "about-us", "escape_hatch": True, "heading_level": 1, "html": body, "css": css},
    {"id": "site-footer", "landmark": "footer", "escape_hatch": True, "html": FOOT_HTML, "css": FOOT_CSS},
]
for s in SECTIONS:
    s["notes"] = [NOTE]
    s["html"] = link_pages(s["html"])
# keep the unstyled DevConnect-draft input that lives in the same folder
compile_page(SLUG, {"page": SLUG, "meta": {"title": "About Us | Mizuho America",
                                           "description": "Mizuho America: collaborating with neurosurgeons for more than 30 years, with a global presence and a creed built on honesty, solidarity and contribution."},
                    "css_workflow": "scss", "font_source": "google",
                    "notes_for_developer": ["Source of truth for About is the live Elementor page 15; this replica is generated from the same tree and partial."],
                    "sections": SECTIONS},
             extra_images=("logo-mizuho-header-srgb.png", "logo-mizuho-footer-reversed.png"))
