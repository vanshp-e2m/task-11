"""Replica CSS → theme SCSS partials: one assets/scss/layouts/_<layout>.scss per ACF layout (+ one page partial for each page's
shared helpers), so the WordPress pages render exactly like the generated HTML the conversion transplanted.

    python tools/figma_html/split_replica_css.py

Per page (pages/<slug>/html/css/styles.css = DevCommand-compiled replica CSS):
  * dropped: :root (compiler tokens — the theme's own tokens + Elementor Kit are the source), the header/footer chrome
    (.site-head/.hd-*/.site-foot/.ft-*/.ph-*/.pf-* — those are the Elementor Theme Builder templates in WordPress);
  * kept unscoped: @font-face (the real italic faces, issues #35);
  * everything else is SCOPED to the page (`.m11-page-<scope> …`), because the replicas reuse class names with different rules
    (.tile, .fl-*, .sec-h …); `main`/`body`/`html` selectors become the scope itself (the scope class sits on <main>);
  * split by class prefix into the layout partials; whatever no layout claims goes to pages/_<scope>.scss.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCSS = os.path.join(ROOT, "wp-content", "themes", "module11", "assets", "scss")
# Brand colours -> theme tokens. The tokens read the Elementor Kit (--e-global-color-*), so one Kit change reaches the ACF pages
# too, and the house rule "colours only via var(--clr-*)" holds for the generated partials (issues-log #66).
TOKENS = {"#0065b3": "var(--clr-primary)", "#00b3f0": "var(--clr-sky)", "#090909": "var(--clr-text)", "#002842": "var(--clr-navy)",
          "#77dcff": "var(--clr-light-sky)", "#ffffff": "var(--clr-white)", "#d9d9d9": "var(--clr-dot)"}
HEX = re.compile("(" + "|".join(re.escape(k) for k in TOKENS) + r")(?![0-9a-f])", re.I)


def tokenise(body):
    return HEX.sub(lambda m: TOKENS[m.group(1).lower()], body)


CHROME = re.compile(r"(^|[\s,>+~(])\.(site-head|site-foot|hd-|ft-|ph-|pf-|portal-|selectish)")

# page scope -> (replica slug, {layout: [class prefixes]})
PAGES = {
    "mizuho-home": ("mizuho-home", {"hero_carousel": ["hero"], "intro_statement": ["intro"], "value_columns": ["vc"],
                                    "procedure_band": ["pb"], "testimonial_home": ["ts"], "about_stats": ["ab"]}),
    "resources": ("resources", {"resources_intro": ["ri"], "resources_testimonials": ["rt", "tx-"], "fast_facts": ["ff"],
                                "resources_brochures": ["br", "bg", "bc", "badge", "mo-"], "bottom_links_band": ["bl"]}),
    "products": ("product-browse", {"products_intro": ["pbh"], "browse_by_procedure": ["pr"],
                                    "browse_by_product": ["pbp", "pb-", "pbf", "fl-", "tile", "ptag", "pager", "pg", "chip"]}),
    "sales-hub": ("sales-hub-login", {"sh_login": ["lg"]}),
    "dashboard": ("sales-hub-dashboard", {"sh_dashboard": ["db"], "sh_account": ["db-acc", "db-btn"]}),
    "resource-library": ("resource-library", {"sh_resource_library_intro": ["rl-band", "rlb"],
                                              "sh_resource_results": ["rl-", "fl-", "tile", "chip"]}),
    "product--main": ("product-main", {"single_product_main": [""]}),
    "product--a": ("product-variation-a", {"single_product_a": [""]}),
    "product--b": ("product-variation-b", {"single_product_b": [""]}),
}


def top_level(css):
    """Split CSS into top-level (head, body) pairs by brace depth (robust to any selector/body content)."""
    out, depth, start, head = [], 0, 0, ""
    for i, ch in enumerate(css):
        if ch == "{":
            if depth == 0:
                head, start = css[start:i].strip(), i + 1
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                out.append((head, css[start:i]))
                start = i + 1
    return out


def blocks(css):
    """Yield (media_or_None, selector, body); @media one level deep; ('@font-face', head, body) for font faces."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for head, body in top_level(css):
        if head.startswith("@media"):
            for sel, inner in top_level(body):
                yield head, sel, inner.strip()
        elif head.startswith("@font-face"):
            yield "@font-face", head, body.strip()
        elif head.startswith("@"):
            continue
        else:
            yield None, head, body.strip()


def scope_selector(sel, scope):
    out = []
    for part in sel.split(","):
        p = part.strip()
        if not p:
            continue
        p = re.sub(r"^(html|body)\b", "", p).strip()
        if re.match(r"^main\b", p):
            p = scope + p[4:]
        elif p.startswith(":where(") and ".rs" in p or not p:
            p = f"{scope} {p}".strip()
        else:
            p = f"{scope} {p}"
        out.append(p)
    return ", ".join(out)


def owner(sel, prefixes):
    for layout, pre in prefixes.items():
        for pf in pre:
            if pf == "":
                return layout
            if re.search(r"\.(%s)" % re.escape(pf), sel):
                return layout
    return None


written = {}
fonts = set()
for scope_name, (slug, prefixes) in PAGES.items():
    css = open(os.path.join(ROOT, "pages", slug, "html", "css", "styles.css"), encoding="utf-8").read()
    scope = f".m11-page-{scope_name}"
    buckets = {}
    for media, sel, body in blocks(css):
        if media == "@font-face":
            fonts.add("@font-face { " + " ".join(body.split()) + " }")
            continue
        if sel.startswith(":root"):
            buckets.setdefault(f"page:{scope_name}", []).append((media, scope, tokenise(body)))  # compiler tokens, scoped (vars inherit)
            continue
        if CHROME.search(" " + sel):
            continue
        if sel.startswith("@"):
            continue
        # Decorative UI icons move to the theme (assets/css/main.css → ../images/icons/). The Products hero photo is CONTENT:
        # it comes from the products_intro background fields through CSS variables (conversion issue C13).
        body = body.replace('url("../figma/images/products-hero.jpg")', "var(--pbh-bg, none)")
        body = body.replace('url("../figma/images/products-hero-m.jpg")', "var(--pbh-bg-m, var(--pbh-bg, none))")
        body = body.replace('url("../figma/images/', 'url("../images/icons/')
        body = tokenise(body)
        target = owner(sel, prefixes) or f"page:{scope_name}"
        buckets.setdefault(target, []).append((media, scope_selector(sel, scope), body))
    for target, rules in buckets.items():
        lines, cur = [], None
        for media, sel, body in rules:
            if media != cur:
                if cur:
                    lines.append("}")
                if media:
                    lines.append(media + " {")
                cur = media
            lines.append(("  " if media else "") + f"{sel} {{ {' '.join(body.split())} }}")
        if cur:
            lines.append("}")
        written.setdefault(target, []).append(f"// from pages/{slug}/html/css/styles.css (generated replica) — scoped to {scope}\n" + "\n".join(lines))

os.makedirs(os.path.join(SCSS, "layouts"), exist_ok=True)
os.makedirs(os.path.join(SCSS, "pages"), exist_ok=True)
uses = []
HEAD = "// GENERATED by tools/figma_html/split_replica_css.py from the Flow A replica CSS — edit the generator or the replica, not this file.\n"
for target, parts in sorted(written.items()):
    if target.startswith("page:"):
        name = f"pages/_{target[5:].replace('--', '-')}.scss"
        use = f"pages/{target[5:].replace('--', '-')}"
    else:
        kebab = target.replace("_", "-")
        name, use = f"layouts/_{kebab}.scss", f"layouts/{kebab}"
    open(os.path.join(SCSS, name), "w", encoding="utf-8").write(HEAD + "\n\n".join(parts) + "\n")
    uses.append(use)
open(os.path.join(SCSS, "base", "_replica-fonts.scss"), "w", encoding="utf-8").write(HEAD + "\n".join(sorted(fonts)) + "\n")
main = os.path.join(SCSS, "main.scss")
src = open(main, encoding="utf-8").read()
src = re.sub(r"\n// >>> replica partials.*?// <<< replica partials\n", "\n", src, flags=re.S)
block = "// >>> replica partials (tools/figma_html/split_replica_css.py)\n@use \"base/replica-fonts\";\n" + "".join(f'@use "{u}";\n' for u in uses) + "// <<< replica partials\n"
# The hand-written guards (robustness, flow grids) must load AFTER the generated partials: same specificity, later wins.
GUARDS = "// Hand-written guards"
src = src.replace(GUARDS, block + GUARDS, 1) if GUARDS in src else src.rstrip() + "\n" + block
open(main, "w", encoding="utf-8").write(src)
print(len(uses), "partials:", ", ".join(uses))
