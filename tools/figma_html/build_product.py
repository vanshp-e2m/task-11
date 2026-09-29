"""Single-product replicas: Product Page Main (1:3504), Variation A (1:3721), Variation B (1:3332) → pages/<slug>/html/.

ONE generator for all three, because on the real site they are ONE template (m11_product single): the frames differ only in
optional parts, which this script switches on when the frame has them:
  * "Included Instruments chart" group → a table (Variation A: instruments, Variation B: size guide with the selected row);
  * a "Selection" group in the factoids → the blade-size selector (Variation B);
  * the category pill above the title (A, B; hidden in Main), real thumbnails (A) vs FPO boxes (Main, B).
Components are found by their Figma NAMES ("Main Intro Section", "Midsection Nav", "Accessories section", "Testimonial",
"Product Tile", "Overview chart"), so the three frames share one code path. Copy is read from the Figma JSON.
Desktop = flow layout in u() with min-height-to-next-Figma-y; mobile = the 430 frames' auto-layout (tables scroll sideways).

    python tools/figma_html/build_product.py [main|a|b]      (default: all three)
"""
import os
import re
import sys
from html import escape

import cv2

from chrome import D, FOOT_CSS, FOOT_HTML, FR, HEADER_CSS, HEADER_HTML, HEADER_JS, I, M, OS, ROOT, SHARED, link_pages, u
from replica_lib import Css, Page, compile_page, figma_linear, slug

INK, BLUE, SKY = "#090909", "#0065B3", "#00B3F0"
PRODUCTS = {
    "main": dict(slug="product-main", frame="1:3504", export="Product Page Main.png"),
    "a": dict(slug="product-variation-a", frame="1:3721", export="Product Page Variation A.png"),
    "b": dict(slug="product-variation-b", frame="1:3332", export="Product Page Variation B.png"),
}
BROWSE = "../../product-browse/html/"
# replica cross-links (the real site links every tile to its own product post)
TILE_LINKS = {"LawtonElite Bypass Instrumentation Set": "../../product-variation-a/html/", "Scalpel Handles": "../../product-variation-b/html/",
              "Sugita Multipurpose Head Frame Classic": "../../product-main/html/", "Skull Base Instrumentation Set": "../../product-variation-a/html/",
              "Microscissors": "../../product-variation-a/html/", "K-6420 Micro Blade System": "../../product-variation-b/html/"}


def kids(n, name=None, typ=None, visible=True):
    out = []
    for c in n.get("children", []):
        if visible and c.get("visible") is False:
            continue
        if (name is None or c.get("name") == name) and (typ is None or c["type"] == typ):
            out.append(c)
    return out


def vf(n):
    """Visible fills only (Figma keeps hidden fills in the list)."""
    return [f for f in n.get("fills", []) if f.get("visible", True)]


def descend(n, name):
    out = []
    for c in n.get("children", []):
        if c.get("visible") is False:
            continue
        if c.get("name") == name:
            out.append(c)
        else:
            out += descend(c, name)
    return out


def texts(n):
    out = []
    for c in n.get("children", []):
        if c.get("visible") is False:
            continue
        if c["type"] == "TEXT":
            out.append(c)
        out += texts(c)
    return out


def build(key):
    cfg = PRODUCTS[key]
    P = Page(cfg["frame"])
    F = P.frame
    box = lambda n: P.box(n["id"])  # noqa: E731
    y = lambda n: box(n)[1]  # noqa: E731
    SLUG = cfg["slug"]
    IMG = os.path.join(ROOT, "pages", SLUG, "figma", "images")
    os.makedirs(IMG, exist_ok=True)
    EXP = cv2.imread(os.path.join(ROOT, "pages/_figma/frames/export", cfg["export"]))
    css = Css()

    def crop(n, name):
        x, y_, w, h = (int(round(v)) for v in box(n))
        cv2.imwrite(os.path.join(IMG, name), EXP[y_:y_ + h, x:x + w], [cv2.IMWRITE_JPEG_QUALITY, 90])
        return name

    groups = {}
    for c in kids(F):
        groups.setdefault(c.get("name"), []).append(c)
    intro = groups["Main Intro Section"][0]
    nav = groups["Midsection Nav"][0]
    table_g = (groups.get("Included Instruments chart") or [None])[0]
    acc, rel = sorted(groups["Accessories section"], key=y)
    testi = groups["Testimonial"][0]
    footer_y = y(groups["Footer Section"][0]) + 70 if "Footer Section" in groups else None
    footer_y = min(y(r) for r in descend(groups["Footer Section"][0], "Rectangle 21")) if footer_y else F["absoluteBoundingBox"]["height"] - 960

    # ================================================================ header ("Products" current)
    head = HEADER_HTML.replace('<a href="#products">', f'<a class="is-current" aria-current="page" href="{BROWSE}">', 1)
    css.add(".site-head__nav a.is-current", f"color: {BLUE};")

    # ================================================================ intro
    it = texts(intro)
    by_text = lambda pred: next(t for t in it if pred(t["characters"]))  # noqa: E731
    h1 = by_text(lambda s: s.strip().lower() == "products")
    panel = next(r for r in kids(intro, typ="RECTANGLE") if vf(r) and vf(r)[0]["type"] == "GRADIENT_LINEAR")
    crumb = by_text(lambda s: s.startswith("Products  >"))
    facts = by_text(lambda s: "Quick Facts" in s)
    gallery = next(r for r in kids(intro, typ="RECTANGLE") if abs(box(r)[2] - 580) < 2)
    thumbs_g = next(g for g in kids(intro, typ="GROUP") if len(kids(g, typ="RECTANGLE")) == 4)
    rule = next(l for l in kids(intro, typ="LINE"))
    fact = kids(intro, "Factoids")[0]
    chart = descend(fact, "Overview chart")[0]
    selection = (descend(fact, "Selection") or [None])[0]
    pill = next((g for g in kids(fact, typ="GROUP") if g.get("name") == "label"), None)
    tags_frame = next(fr for fr in descend(fact, None) if False) if False else None
    tag_groups = [g for g in descend(fact, "label") if g is not pill and 395 < y(g) < 460]
    title_t = next(t for t in texts(fact) if t["style"].get("fontWeight") == 700 and t["style"].get("fontSize") == 16)
    desc_t = next(t for t in texts(fact) if t["style"].get("fontSize") == 14 and t["style"].get("fontWeight") == 300)
    ctas_rect = [r for r in kids(intro, typ="RECTANGLE") if box(r)[3] == 45]
    cta_btn = next(v for v in kids(intro, typ="VECTOR") if v.get("name") == "button")
    cta_y = box(cta_btn)[1]
    px, py, pw, ph = box(panel)
    gx, gy, gw, gh = box(gallery)

    gname = crop(gallery, f"{key}-gallery.jpg")
    thumbs = []
    for i, r in enumerate(sorted(kids(thumbs_g, typ="RECTANGLE"), key=lambda r: box(r)[0])):
        fills = [f["type"] for f in vf(r)]
        if i == 3:
            thumbs.append('<li><button class="thumb thumb--video" type="button" aria-label="Play product video"><img src="figma/images/icon-play-circle.svg" alt="" width="28" height="28"></button></li>')
        elif fills[-1] == "SOLID":  # white laid over the image in Figma = an unfinished placeholder box
            thumbs.append('<li><button class="thumb thumb--fpo" type="button">FPO IMAGE</button></li>')
        else:
            thumbs.append(f'<li><button class="thumb" type="button" aria-label="Show image {i + 1}"><img src="figma/images/{crop(r, f"{key}-thumb-{i + 1}.jpg")}" alt="" width="106" height="59"></button></li>')
    # breadcrumb: "Products  >  By Category  >  X  >  Name"
    parts = [p.strip() for p in crumb["characters"].split(">")]
    crumb_html = '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(
        f'<li><a href="{BROWSE}">{escape(p)}</a></li>' if i < len(parts) - 1 else f'<li aria-current="page">{escape(p)}</li>'
        for i, p in enumerate(parts)) + "</ol></nav>"
    tl = P.fig_lines(title_t["id"])
    title_html = f'<h2 class="pd-title">{escape("".join(t for t, _ in tl[0]).strip())}</h2><p class="pd-model">{P.inline(tl[1])}</p>'
    tags_html = '<ul class="pd-tags">' + "".join(f'<li>{escape(texts(g)[0]["characters"])}</li>' for g in sorted(tag_groups, key=lambda g: box(g)[0])) + "</ul>"
    pill_html = f'<p class="pd-pill">{escape(texts(pill)[0]["characters"])}</p>' if pill else ""
    # spec chart: labels column (optional bold heading line) + values column
    ctexts = sorted(texts(chart), key=lambda t: box(t)[0])
    lab_lines = [ln for ln in ctexts[0]["characters"].split("\n")]
    heading = lab_lines[0].strip() if lab_lines[0].strip() and lab_lines[0].strip().upper() == lab_lines[0].strip() else ""
    labels = [s.strip() for s in lab_lines[1:] if s.strip()] if lab_lines[0].strip() == "" or heading else [s.strip() for s in lab_lines if s.strip()]
    values = [s.strip() for s in ctexts[1]["characters"].split("\n") if s.strip()]
    rows = "".join(f'<tr><th scope="row">{escape(a)}</th><td>{escape(b)}</td></tr>' for a, b in zip(labels, values))
    chart_html = (f'<div class="pd-chart"><table class="pd-spec">' + (f'<caption>{escape(heading)}</caption>' if heading else "")
                  + f"<tbody>{rows}</tbody></table></div>")
    sel_html = ""
    if selection:
        st = texts(selection)
        lab = next(t for t in st if t["characters"].isupper())
        cur = next(t for t in st if t["characters"].endswith("mm") and len(t["characters"]) < 10)
        partno = next(t for t in st if "Part no" in t["characters"])
        sizes = []
        if table_g:
            first_col = sorted([t for t in texts(table_g) if t["style"].get("lineHeightPx") == 34], key=lambda t: box(t)[0])[0]
            sizes = [s.strip() for s in first_col["characters"].split("\n") if s.strip()]
        opts = "".join(f'<option{" selected" if s == cur["characters"].strip() else ""}>{escape(s)}</option>' for s in sizes)
        sel_html = (f'<div class="pd-select"><label class="pd-select-h" for="{key}-size">{escape(lab["characters"])}</label>'
                    f'<div class="pd-select-row"><select class="pd-size selectish" id="{key}-size" name="size">{opts}</select>'
                    f'<p class="pd-part">{P.inline(P.fig_lines(partno["id"])[0])}</p></div></div>')
    dl = next(t for t in it if t["characters"].startswith("Download product"))
    sched = next(t for t in it if t["characters"].startswith("Schedule"))
    ctas = (f'<div class="pd-ctas"><a class="pbtn pbtn--solid" href="http://task-11.local/contact-us/">{escape(sched["characters"])}</a>'
            f'<a class="pbtn pbtn--line" href="#download-brochure"><span class="dl-arrow" aria-hidden="true"></span>{escape(dl["characters"])}</a></div>')
    fl = P.fig_lines(facts["id"])[0]
    facts_html = f'<p class="pd-facts">{P.inline(fl)}</p>'
    INTRO_HTML = (f'<section class="rs pd" id="product-overview"><div class="fx"><h1 class="pd-h1">{escape(h1["characters"])}</h1>'
                  f'<div class="pd-panel">{crumb_html}<div class="pd-cols"><div class="pd-media"><div class="pd-gallery"><img src="figma/images/{gname}" '
                  f'alt="{escape("".join(t for t, _ in tl[0]).strip())}" width="580" height="328"></div><ul class="pd-thumbs">{"".join(thumbs)}</ul>'
                  f'<hr class="pd-rule">{facts_html}</div><div class="pd-info">{pill_html}{title_html}{tags_html}<p class="pd-desc">{escape(desc_t["characters"])}</p>'
                  f'{sel_html}{chart_html}{ctas}</div></div></div>')
    # tabs (inside the same section: it is the panel's bottom edge)
    nt = sorted(texts(nav), key=lambda t: box(t)[0])
    under = next(r for r in kids(nav, typ="RECTANGLE") if box(r)[3] == 3)
    cur_tab = next(t for t in nt if box(t)[0] <= box(under)[0] + 30 and box(t)[0] + box(t)[2] >= box(under)[0])
    tabs = "".join(f'<li><a class="tab{" is-current" if t is cur_tab else ""}" href="#{slug(t["characters"])}"'
                   f'{" aria-current=\"true\"" if t is cur_tab else ""}>{escape(t["characters"])}</a></li>' for t in nt)
    INTRO_HTML += f'<nav class="pd-tabs" aria-label="Product sections"><ul>{tabs}</ul></nav></div></section>'

    css.add(".pd-h1", f"font-family: {FR}; font-weight: 400; color: {BLUE}; text-transform: uppercase;")
    css.add(".pd-panel", f"box-sizing: border-box; background: {figma_linear(vf(panel)[0], pw, ph)}, #FFFFFF;")
    css.add(".crumbs ol", f"display: flex; flex-wrap: wrap; margin: 0; padding: 0; list-style: none; font-family: {OS}; font-size: 12px; line-height: 22px; color: #000000;")
    css.add(".crumbs li + li::before", 'content: ">"; margin: 0 8px;')
    css.add(".crumbs a", "color: #000000; font-weight: 400;")
    css.add(".crumbs [aria-current]", "font-weight: 300;")
    css.add(".pd-gallery", "overflow: hidden; background: #FFFFFF; box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.1);")
    css.add(".pd-gallery img", "width: 100%; height: 100%; object-fit: cover;")
    css.add(".pd-thumbs", "display: flex; margin: 0; padding: 0; list-style: none;")
    css.add(".thumb", f"display: flex; align-items: center; justify-content: center; box-sizing: border-box; padding: 0; overflow: hidden; background: #FFFFFF; border: 1px solid rgba(0, 0, 0, 0.1); cursor: pointer; font-family: {OS}; font-weight: 300; font-size: 14px; color: {SKY};")
    css.add(".thumb img", "width: 100%; height: 100%; object-fit: cover;")
    css.add(".thumb--video", "background: #A8A8A8;")
    css.add(".thumb--video img", "width: 28px; height: 28px; object-fit: contain;")
    css.add(".pd-rule", "margin: 0; border: 0; border-top: 1px solid rgba(0, 0, 0, 0.2);")
    css.add(".pd-facts", f"margin: 0; font-family: {OS}; font-weight: 400; font-size: 12px; line-height: 22px; color: #000000;")
    css.add(".pd-facts strong", "font-weight: 700;")
    css.add(".pd-pill", f"display: inline-block; margin: 0; box-sizing: border-box; height: 28px; padding: 3px 12px 3px 9px; background: rgba(231, 249, 255, 0.9); border: 0.5px solid rgba(0, 0, 0, 0.35); border-radius: 5px; font-family: {OS}; font-weight: 400; font-size: 11px; line-height: 22px; color: {INK};")
    css.add(".pd-title", f"margin: 0; font-family: {OS}; font-weight: 700; font-size: 18px; line-height: 22px; color: #000000;")
    css.add(".pd-model", f"margin: 0; font-family: {OS}; font-weight: 400; font-size: 14px; line-height: 24px; color: #000000;")
    css.add(".pd-model strong", "font-weight: 700;")
    css.add(".pd-tags", "display: flex; flex-wrap: wrap; gap: 5px; margin: 0; padding: 0; list-style: none;")
    css.add(".pd-tags li", f"box-sizing: border-box; height: 28px; padding: 3px 9px; background: rgba(249, 255, 67, 0.25); border: 0.5px solid rgba(0, 0, 0, 0.35); border-radius: 5px; font-family: {OS}; font-weight: 400; font-size: 11px; line-height: 22px; color: {INK};")
    css.add(".pd-desc", f"margin: 0; font-family: {OS}; font-weight: 300; font-size: 14px; line-height: 22px; color: #000000;")
    css.add(".pd-chart, .pd-select", "box-sizing: border-box; background: #FFFFFF; box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.1); border-radius: 10px;")
    css.add(".pd-spec", f"width: 100%; border-collapse: collapse; font-family: {OS}; font-size: 12px; color: #000000;")
    css.add(".pd-spec caption", "text-align: left; font-weight: 700; line-height: 22px;")
    css.add(".pd-spec th", "text-align: left; font-weight: 300; padding: 0;")
    css.add(".pd-spec td", "font-weight: 400; padding: 0;")
    css.add(".pd-spec tr + tr > *", "box-shadow: inset 0 1px 0 rgba(0, 0, 0, 0.1);")
    css.add(".pd-select-h", f"display: block; font-family: {OS}; font-weight: 700; font-size: 12px; line-height: 22px; color: #000000;")
    css.add(".pd-select-row", "display: flex; align-items: center;")
    css.add(".pd-size", f"appearance: none; -webkit-appearance: none; box-sizing: border-box; height: 40px; padding-left: 15px; border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 5px; background: #FFFFFF url(\"../figma/images/icon-select-caret.svg\") no-repeat right 0 center / 41px 40px; font-family: {OS}; font-size: 14px; color: #000000; cursor: pointer;")
    css.add(".pd-part", f"margin: 0; font-family: {OS}; font-weight: 400; font-size: 14px; line-height: 28px; color: #000000; white-space: pre;")
    css.add(".pd-part strong", "font-weight: 700;")
    css.add(".pbtn", f"display: flex; align-items: center; justify-content: center; gap: 8px; box-sizing: border-box; border-radius: 5px; font-family: {FR}; font-weight: 400; font-size: 16px;")
    css.add(".pbtn--solid", f"background: {BLUE}; color: #FFFFFF;")
    css.add(".pbtn--line", f"background: #FFFFFF; color: {BLUE}; border: 2px solid {SKY};")
    css.add(".dl-arrow", 'width: 12px; height: 14px; background: url("../figma/images/icon-arrow-down-blue.svg") no-repeat center / contain;')
    css.add(".pd-tabs", f"background: {BLUE};")
    css.add(".pd-tabs ul", "display: flex; margin: 0; padding: 0; list-style: none;")
    css.add(".tab", f"display: block; box-sizing: border-box; font-family: {OS}; font-weight: 700; font-size: 16px; line-height: 22px; color: #FFFFFF;")
    css.add(".tab.is-current", "color: #77DCFF; box-shadow: inset 0 -3px 0 #77DCFF;")
    # desktop geometry
    nx, ny, nw, nh = box(nav)
    info_x = min(box(t)[0] for t in [title_t, desc_t]) - 4
    blocks = [(pill, "pd-pill"), (title_t, "pd-title"), (tag_groups[0], "pd-tags"), (desc_t, "pd-desc")]
    if selection:
        blocks.append((selection, "pd-select"))
    blocks.append((chart, "pd-chart"))
    blocks = [(n, c) for n, c in blocks if n is not None]
    css.add(".pd > .fx", f"padding: {u(y(h1) - 161)} 0 0 {u(px)};", D)
    css.add(".pd-h1", f"margin-left: {u(box(h1)[0] - px)}; font-size: {u(45)}; line-height: {u(70)}; min-height: {u(py - y(h1))};", D)
    css.add(".pd-panel", f"width: {u(pw)}; height: {u(ph)}; border-radius: {u(12)} {u(12)} 0 0; padding: {u(y(crumb) - py)} 0 0 {u(box(crumb)[0] - px)};", D)
    css.add(".crumbs", f"min-height: {u(gy - y(crumb))};", D)
    css.add(".crumbs ol", f"font-size: {u(12)}; line-height: {u(22)};", D)
    css.add(".crumbs li + li::before", f"margin: 0 {u(8)};", D)
    css.add(".pd-cols", "display: flex; align-items: flex-start;", D)
    css.add(".pd-media", f"width: {u(gw)};", D)
    css.add(".pd-gallery", f"width: {u(gw)}; height: {u(gh)}; border-radius: {u(10)};", D)
    tb = sorted(kids(thumbs_g, typ="RECTANGLE"), key=lambda r: box(r)[0])
    css.add(".pd-thumbs", f"margin-top: {u(box(tb[0])[1] - gy - gh)}; gap: {u(box(tb[1])[0] - box(tb[0])[0] - box(tb[0])[2])};", D)
    css.add(".thumb", f"width: {u(106)}; height: {u(59)}; border-radius: {u(8)}; font-size: {u(14)};", D)
    css.add(".pd-rule", f"margin-top: {u(y(rule) - box(tb[0])[1] - 59)}; width: {u(box(rule)[2])};", D)
    css.add(".pd-facts", f"margin-top: {u(y(facts) - y(rule))}; font-size: {u(12)}; line-height: {u(22)};", D)
    css.add(".pd-info", f"margin-left: {u(info_x - gx - gw)}; width: {u(555)}; margin-top: {u((y(pill) if pill else y(title_t)) - gy)};", D)
    # each block's gap = its Figma top - the previous block's Figma bottom; text blocks count whole lines only
    def fig_h(n, c):
        if c == "pd-title":
            return 22 + 24
        if c == "pd-desc":
            return int(box(n)[3] // 22) * 22
        if c == "pd-chart":
            return box(next(r for r in chart["children"] if r["type"] == "RECTANGLE"))[3]
        return box(n)[3]

    def fig_top(n, c):
        if c == "pd-chart":
            return box(next(r for r in chart["children"] if r["type"] == "RECTANGLE"))[1]
        return y(n)
    for (n, c), (n2, c2) in zip(blocks, blocks[1:]):
        sel_ = ".pd-info > .pd-model" if c == "pd-title" else f".pd-info > .{c}"
        css.add(sel_, f"margin-bottom: {u(fig_top(n2, c2) - fig_top(n, c) - fig_h(n, c))};", D)
    css.add(".pd-info > .pd-title", "margin-bottom: 0;", D)
    info_top = fig_top(*blocks[0])
    css.add(".pd-desc", f"font-size: {u(14)}; line-height: {u(22)}; width: {u(box(desc_t)[2])};", D)
    cx, cy_, cw, ch = box(chart)
    lines = sorted(descend(chart, None) if False else [l for l in chart["children"] if l["type"] == "LINE"], key=lambda l: box(l)[1])
    crect = next(r for r in chart["children"] if r["type"] == "RECTANGLE")
    first_row_top = box(lines[0])[1] - 28
    css.add(".pd-chart", f"width: {u(box(crect)[2])}; height: {u(box(crect)[3])}; padding: {u((ctexts[0]['absoluteBoundingBox']['y'] - P.fy) - box(crect)[1] + (0 if heading else 0))} {u(26)} {u(8)} {u(25)};", D)
    css.add(".pd-spec", f"width: {u(500)}; font-size: {u(12)};", D)
    css.add(".pd-spec caption", f"line-height: {u(22)}; padding-bottom: {u(first_row_top - (ctexts[0]['absoluteBoundingBox']['y'] - P.fy) - 22)};", D)
    css.add(".pd-spec th, .pd-spec td", f"height: {u(28)}; line-height: {u(28)};", D)
    css.add(".pd-spec th", f"width: {u(255)};", D)
    if not heading:
        css.add(".pd-chart", f"padding-top: {u(first_row_top - box(crect)[1])};", D)
    if selection:
        sx, sy_, sw_, sh_ = box(selection)
        css.add(".pd-select", f"width: {u(sw_)}; height: {u(sh_)}; padding: {u(10)} {u(25)} 0;", D)
        css.add(".pd-select-h", f"font-size: {u(12)}; line-height: {u(22)}; margin-bottom: {u(5)};", D)
        css.add(".pd-select-row", f"gap: {u(26)};", D)
        css.add(".pd-size", f"width: {u(194)}; height: {u(40)}; padding-left: {u(15)}; font-size: {u(14)}; background-size: {u(41)} {u(40)};", D)
        css.add(".pd-part", f"font-size: {u(14)}; line-height: {u(28)};", D)
    css.add(".pd-ctas", f"display: flex; gap: {u(box(cta_btn)[0] - box(ctas_rect[0])[0] - 270)}; margin-top: {u(cta_y - box(crect)[1] - box(crect)[3])};", D)
    css.add(".pbtn", f"height: {u(45)}; font-size: {u(16)}; border-radius: {u(5)};", D)
    css.add(".pd-ctas .pbtn", f"width: {u(270)};", D)
    css.add(".pd-tabs", f"width: {u(nw)}; height: {u(nh)}; border-radius: 0 0 {u(12)} {u(12)};", D)
    css.add(".pd-tabs ul", f"padding-left: {u(box(nt[0])[0] - nx - 27)};", D)
    css.add(".tab", f"height: {u(nh)}; padding: {u(box(nt[0])[1] - ny)} {u(27)} 0; font-size: {u(16)}; line-height: {u(22)};", D)
    css.add(".tab.is-current", f"box-shadow: inset 0 {u(-3)} 0 #77DCFF;", D)
    # position the thumbs/rule/facts relative to the media column's own top and cap the panel
    # mobile (1:1330: panel p32 gap20 inside a clipped gradient card; tabs at its bottom; Quick Facts after the description)
    css.add(".pd-h1", "font-size: 36px; line-height: 41.4px;", M)
    css.add(".pd-panel", "padding: 32px 32px 0; border-radius: 12px 12px 0 0;", M)
    css.add(".pd-cols, .pd-media, .pd-info", "display: contents;", M)
    css.add(".pd-panel", "display: flex; flex-direction: column; gap: 20px; padding-bottom: 32px;", M)
    css.add(".pd-gallery", "aspect-ratio: 580 / 328; border-radius: 10px;", M)
    css.add(".pd-thumbs", "gap: 6px; margin-top: -14px;", M)
    css.add(".pd-thumbs li", "flex: 1;", M)
    css.add(".thumb", "width: 100%; aspect-ratio: 106 / 59; border-radius: 8px; font-size: 9px;", M)
    css.add(".pd-pill", "align-self: flex-start;", M)
    css.add(".pd-rule", "order: 10; margin: 0;", M)
    css.add(".pd-facts", "order: 11;", M)
    css.add(".pd-select", "order: 12; padding: 10px 20px 14px;", M)
    css.add(".pd-chart", "order: 13; overflow-x: auto; padding: 10px 20px; margin-right: -32px; border-radius: 10px 0 0 10px;", M)
    css.add(".pd-spec", "min-width: 500px;", M)
    css.add(".pd-spec th, .pd-spec td", "height: 28px; line-height: 28px;", M)
    css.add(".pd-spec th", "width: 255px;", M)
    css.add(".pd-select-row", "gap: 20px; flex-wrap: wrap; margin-top: 6px;", M)
    css.add(".pd-size", "width: 100%;", M)
    css.add(".pd-ctas", "order: 14; display: flex; flex-direction: column; gap: 18px;", M)
    css.add(".pbtn", "height: 45px;", M)
    css.add(".pd-tabs", "border-radius: 0 0 12px 12px;", M)
    css.add(".pd-tabs ul", "justify-content: space-around;", M)
    css.add(".tab", "height: 60px; padding: 19px 10px 0; font-size: 16px;", M)

    # ================================================================ optional table (A: instruments, B: size guide)
    TABLE_HTML = ""
    if table_g:
        tt = texts(table_g)
        h2 = next(t for t in tt if t["style"].get("fontFamily") == "Freeman" and t["style"].get("fontSize") == 26)
        badge = next(g for g in kids(table_g, "label"))
        dlb = next((g for g in kids(table_g, "button")), None)
        filt = kids(table_g, "Filters")[0]
        head_t = next(t for t in texts(filt) if t["style"].get("fontWeight") == 700 and "\n" not in t["characters"])
        cols = sorted([t for t in texts(filt) if t["style"].get("lineHeightPx") == 34], key=lambda t: box(t)[0])
        labels = [s for s in re.split(r"\s{2,}", head_t["characters"].strip()) if s]
        colvals = [[s for s in c["characters"].split("\n")] for c in cols]
        n = max(len(v) for v in colvals)
        hi = next((r for r in kids(filt, typ="RECTANGLE") if vf(r) and vf(r)[0].get("color", {}).get("b", 0) > 0.9
                   and abs(vf(r)[0].get("opacity", 1) - 0.1) < 0.01), None)
        hi_row = round((box(hi)[1] - box(cols[0])[1]) / 34) if hi else -1
        body = ""
        for r in range(n):
            cells = ""
            for ci, v in enumerate(colvals):
                val = v[r].strip() if r < len(v) else ""
                cls = ' class="is-part"' if vf(cols[ci])[0]["color"]["b"] > 0.6 and vf(cols[ci])[0]["color"]["r"] < 0.1 else ""
                if ci == 0:
                    mark = '<span class="sel-mark" aria-label="selected"></span>' if r == hi_row else ""
                    cells += f'<th scope="row"{cls}>{escape(val)}{mark}</th>'
                else:
                    cells += f"<td{cls}>{escape(val)}</td>"
            body += f'<tr{" class=\"is-selected\"" if r == hi_row else ""}>{cells}</tr>'
        thead = "".join(f'<th scope="col">{escape(l)}</th>' for l in labels)
        tid = slug(h2["characters"])
        dl_html = (f'<a class="pbtn pbtn--line tb-dl" href="#download-parts-list"><span class="dl-arrow" aria-hidden="true"></span>{escape(texts(dlb)[0]["characters"])}</a>' if dlb else "")
        TABLE_HTML = (f'<section class="rs tb" id="{tid}"><div class="fx"><div class="tb-head"><h2 class="sec-h">{escape(h2["characters"])}</h2>'
                      f'<p class="tb-badge">{escape(texts(badge)[0]["characters"])}</p>{dl_html}</div>'
                      f'<div class="tb-scroll"><table class="tb-table"><thead><tr>{thead}</tr></thead><tbody>{body}</tbody></table></div>'
                      f'<hr class="sec-rule"></div></section>')
        fx0, fy0, fw0, fh0 = box(filt)
        line_t = next(l for l in kids(table_g, typ="LINE"))
        col_x = [box(c)[0] for c in cols]
        widths = [b - a for a, b in zip(col_x, col_x[1:])] + [fx0 + fw0 - col_x[-1]]
        css.add(".tb-head", "display: flex; align-items: center;")
        css.add(".tb-badge", f"margin: 0; box-sizing: border-box; height: 28px; padding: 3px 9px; background: rgba(249, 255, 67, 0.25); border: 0.5px solid rgba(0, 0, 0, 0.35); border-radius: 5px; font-family: {OS}; font-weight: 400; font-size: 11px; line-height: 22px; color: {INK}; white-space: nowrap;")
        css.add(".tb-table", f"border-collapse: separate; border-spacing: 0; font-family: {OS}; font-size: 14px; color: {INK};")
        css.add(".tb-table thead th", "background: rgba(119, 220, 255, 0.5); font-weight: 700; text-align: left; line-height: 22px;")
        css.add(".tb-table tbody th", "font-weight: 400; text-align: left;")
        css.add(".tb-table td", "font-weight: 400;")
        css.add(".tb-table .is-part", f"color: {BLUE};")
        css.add(".tb-table tbody tr:nth-child(even) > *", "background-color: rgba(196, 196, 196, 0.08);")
        css.add(".tb-table tbody tr > *", "box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.15);")  # a border would add 1px per row
        css.add(".tb-table tbody tr.is-selected > *", "background: rgba(0, 179, 240, 0.1);")
        css.add(".sel-mark", "display: inline-block; width: 0; height: 0; margin-left: 12px; border-style: solid; border-width: 5px 8px 5px 0; border-color: transparent #000000 transparent transparent; vertical-align: 1px;")
        css.add(".tb > .fx", f"padding: {u(y(h2) - ny - nh)} 0 0 {u(fx0)};", D)
        css.add(".tb-head", f"margin-left: {u(box(h2)[0] - fx0)}; width: {u(box(dlb)[0] + 230 - box(h2)[0] if dlb else 1168)}; min-height: {u(fy0 - y(h2))}; align-items: flex-start; gap: {u(box(badge)[0] - box(h2)[0] - box(h2)[2])};", D)
        css.add(".tb-badge", f"margin-top: {u(y(badge) - y(h2))};", D)
        if dlb:
            css.add(".tb-dl", f"margin: {u(box(dlb)[1] + 3 - y(h2))} 0 0 auto; width: {u(230)};", D)
        css.add(".tb-table", f"width: {u(fw0)}; font-size: {u(14)};", D)
        css.add(".tb-table thead th", f"height: {u(50)}; padding: 0; border-radius: 0; line-height: {u(22)};", D)
        css.add(".tb-table thead th:first-child", f"border-radius: {u(8)} 0 0 {u(8)}; padding-left: {u(col_x[0] - fx0)};", D)
        css.add(".tb-table thead th:last-child", f"border-radius: 0 {u(8)} {u(8)} 0;", D)
        css.add(".tb-table tbody th:first-child", f"padding-left: {u(col_x[0] - fx0)};", D)
        for ci, w in enumerate(widths):
            css.add(f".tb-table tr > :nth-child({ci + 1})", f"width: {u(w if ci else w + col_x[0] - fx0)};", D)
        css.add(".tb-table tbody tr > *", f"height: {u(34)}; padding: 0; line-height: {u(34)};", D)
        css.add(".tb-table tbody tr:first-child > *", f"border-top: {u(box(cols[0])[1] - fy0 - 50)} solid #FFFFFF;", D)
        css.add(".sec-rule", f"margin: {u(y(line_t) - fy0 - fh0)} 0 0 {u(box(line_t)[0] - fx0)}; width: {u(box(line_t)[2])};", D)
        css.add(".tb-head", "flex-wrap: wrap; gap: 14px 12px; align-items: center;", M)
        css.add(".tb-dl", "flex-basis: 100%; height: 45px; margin-top: 22px;", M)
        css.add(".tb-scroll", "overflow-x: auto; margin-right: -20px;", M)
        css.add(".tb-table", f"min-width: {round(fw0 * 0.75)}px;", M)
        css.add(".tb-table thead th", "height: 50px; padding: 0 0 0 10px;", M)
        css.add(".tb-table thead th:first-child", "border-radius: 8px 0 0 8px; padding-left: 20px;", M)
        css.add(".tb-table tbody th:first-child", "padding-left: 20px;", M)
        css.add(".tb-table tbody tr > *", "height: 34px; padding: 0 0 0 10px;", M)

    # ================================================================ tile grids (accessories + related), testimonial
    def tiles_section(g, sid, rule_after):
        tiles = [t for t in kids(g, "Product Tile")]
        tiles.sort(key=lambda t: box(t)[0])
        h = next(t for t in texts(g) if t["style"].get("fontFamily") == "Freeman" and t["parent"] if False) if False else \
            next(t for t in kids(g, typ="TEXT"))
        items = []
        for t in tiles:
            img = next(r for r in kids(t, typ="RECTANGLE") if any(f["type"] == "IMAGE" for f in vf(r)))
            tx = next(x for x in kids(t, typ="TEXT") if not x["characters"].startswith("View"))
            lines = P.fig_lines(tx["id"])
            title = "".join(s for s, _ in lines[0]).strip()
            sub = "".join(s for s, _ in lines[1]).strip() if len(lines) > 1 else ""
            name = crop(img, f"{key}-{sid}-{slug(title)[:40]}.jpg")
            href = TILE_LINKS.get(title, f"#product-{slug(title)}")
            items.append(f'<li class="tile"><div class="tile-media"><img src="figma/images/{name}" alt="{escape(title)}" width="307" height="195" loading="lazy"></div>'
                         f'<div class="tile-text"><h3 class="tile-title">{escape(title)}</h3><p class="tile-sub">{escape(sub)}</p></div>'
                         f'<a class="tile-view" href="{href}">View product<span class="visually-hidden">: {escape(title)}</span></a></li>')
        line_ = next((l for l in kids(g, typ="LINE")), None)
        html = (f'<section class="rs ts ts--{sid}" id="{sid}"><div class="fx"><h2 class="sec-h">{escape(h["characters"])}</h2>'
                f'<ul class="tiles">{"".join(items)}</ul>' + ('<hr class="sec-rule">' if line_ else "") + "</div></section>")
        return html, h, tiles, line_

    ACC_HTML, acc_h, acc_tiles, acc_line = tiles_section(acc, "accessories", True)
    REL_HTML, rel_h, rel_tiles, _ = tiles_section(rel, "related-products", False)
    tq = texts(testi)
    quote = next(t for t in tq if t["style"].get("fontFamily") == "Freeman" and t["style"].get("fontSize") == 24)
    cite = next(t for t in tq if t["characters"].startswith("–"))
    cl = cite["characters"].split("\n")
    tsched = next(t for t in tq if t["characters"].startswith("Schedule"))
    tlines = sorted(kids(testi, typ="LINE"), key=lambda l: box(l)[0])
    TESTI_HTML = (f'<section class="rs tq" id="testimonial"><div class="fx"><figure class="tq-fig"><blockquote class="tq-quote"><p>{escape(quote["characters"])}</p></blockquote>'
                  f'<figcaption class="tq-cite"><span class="tq-name">{escape(cl[0])}</span><span class="tq-dept">{escape(cl[1]) if len(cl) > 1 else ""}</span></figcaption></figure>'
                  f'<div class="tq-ctas"><a class="pbtn pbtn--solid" href="http://task-11.local/contact-us/">{escape(tsched["characters"])}</a>'
                  f'<a class="pbtn pbtn--line" href="#download-brochure"><span class="dl-arrow" aria-hidden="true"></span>{escape(dl["characters"])}</a></div></div></section>')
    css.add(".sec-h", "margin: 0; font-family: 'Freeman', sans-serif; font-weight: 400; color: #000000; text-transform: uppercase;")
    css.add(".sec-rule", f"margin: 0; border: 0; border-top: 1px solid {BLUE};")
    css.add(".tiles", "margin: 0; padding: 0; list-style: none;")
    T0 = acc_tiles[0]
    css.add(".tile", f"position: relative; display: flex; flex-direction: column; box-sizing: border-box; overflow: hidden; background: {figma_linear(vf(kids(T0, typ='RECTANGLE')[0])[0], 307, 300)}, #FFFFFF; border: 0.5px solid rgba(0, 0, 0, 0.35);")
    css.add(".tile-media", "background: #FFFFFF; border-bottom: 0.5px solid rgba(0, 0, 0, 0.35);")
    css.add(".tile-media > img", "width: 100%; height: 100%; object-fit: cover;")
    css.add(".tile-title", f"margin: 0; font-family: {OS}; font-weight: 700; font-size: 14px; line-height: 22px; color: {INK};")
    css.add(".tile-sub", f"margin: 0; font-family: {OS}; font-weight: 300; font-size: 14px; line-height: 20px; color: {INK};")
    css.add(".tile-view", f"margin-top: auto; font-family: {OS}; font-weight: 700; font-size: 14px; line-height: 22px; color: {BLUE};")
    css.add(".tq-fig", "margin: 0; text-align: center;")
    css.add(".tq-quote", "margin: 0;")
    css.add(".tq-quote p", f"margin: 0; font-family: {FR}; font-weight: 400; color: {BLUE}; text-transform: uppercase;")
    css.add(".tq-cite", f"display: flex; flex-direction: column; font-family: {OS}; font-weight: 300; color: {INK};")
    css.add(".tq-ctas", "display: flex; justify-content: center;")
    # desktop geometry: each section's padding-top = its heading's y - the previous block's end
    prev_end = ny + nh if not table_g else y(next(l for l in kids(table_g, typ="LINE"))) + 1
    ax0 = box(acc_tiles[0])
    css.add(".ts--accessories > .fx", f"padding: {u(y(acc_h) - prev_end)} 0 0 {u(ax0[0])};", D)
    css.add(".sec-h", f"font-size: {u(26)}; line-height: {u(22)};", D)
    css.add(".ts .sec-h", f"margin-left: {u(box(acc_h)[0] - ax0[0])}; min-height: {u(ax0[1] - y(acc_h))};", D)
    css.add(".tiles", f"display: grid; grid-template-columns: repeat(4, {u(307)}); column-gap: {u(box(acc_tiles[1])[0] - ax0[0] - 307)};", D)
    css.add(".tile", f"border-radius: {u(12)}; padding-bottom: {u(12)};", D)
    css.add(".ts--accessories .tile", f"height: {u(ax0[3])};", D)
    css.add(".ts--related-products .tile", f"height: {u(box(rel_tiles[0])[3])};", D)
    css.add(".tile-media", f"height: {u(195)}; border-radius: {u(12)} {u(12)} 0 0;", D)
    css.add(".tile-text, .tile-view", f"margin-left: {u(13)};", D)
    css.add(".tile-text", f"margin-top: {u(11)};", D)
    if acc_line:
        css.add(".ts--accessories .sec-rule", f"margin: {u(y(acc_line) - ax0[1] - ax0[3])} 0 0 {u(box(acc_line)[0] - ax0[0])}; width: {u(box(acc_line)[2])};", D)
    qx, qy, qw = box(quote)[:3]
    css.add(".tq > .fx", f"padding: {u(qy - y(acc_line) - 1)} 0 0 {u(box(tlines[0])[0])}; box-sizing: border-box;", D)
    css.add(".tq-fig", f"margin-left: {u(qx - box(tlines[0])[0])}; width: {u(qw)}; min-height: {u(box(tsched)[1] - 2 - qy)};", D)
    css.add(".tq-quote p", f"font-size: {u(24)}; line-height: {u(40)}; min-height: {u(y(cite) - qy)};", D)
    css.add(".tq-name", f"font-size: {u(24)}; line-height: {u(45)};", D)
    css.add(".tq-dept", f"font-size: {u(18)}; line-height: {u(34)};", D)
    sch_rect = next(r for r in kids(testi, typ="RECTANGLE"))
    css.add(".tq-ctas", f"width: {u(box(tlines[1])[0] + box(tlines[1])[2] - box(tlines[0])[0])}; gap: {u(20)}; background: linear-gradient({BLUE}, {BLUE}) left center / {u(box(tlines[0])[2])} 1px no-repeat, linear-gradient({BLUE}, {BLUE}) right center / {u(box(tlines[1])[2])} 1px no-repeat;", D)
    css.add(".tq-ctas .pbtn", f"width: {u(280)};", D)
    rx0 = box(rel_tiles[0])
    css.add(".ts--related-products > .fx", f"padding: {u(y(rel_h) - box(sch_rect)[1] - 45)} 0 {u(footer_y - rx0[1] - rx0[3])} {u(rx0[0])};", D)
    css.add(".ts--related-products .sec-h", f"min-height: {u(rx0[1] - y(rel_h))};", D)
    # mobile
    css.add(".sec-h", "font-size: 26px; line-height: 22px;", M)
    css.add(".tiles", "display: flex; flex-direction: column; gap: 36px;", M)
    css.add(".tile", "min-height: 300px; border-radius: 12px; padding-bottom: 12px;", M)
    css.add(".ts--related-products .tile", "min-height: 315px;", M)
    css.add(".tile-media", "height: 195px; border-radius: 12px 12px 0 0;", M)
    css.add(".tile-text, .tile-view", "margin-left: 16.5px;", M)
    css.add(".tile-text", "margin-top: 11px; margin-bottom: 18px;", M)
    css.add(".sec-rule", f"margin: 8px -20px 0; border-top-color: {SKY};", M)
    css.add(".ts--related-products > .fx, .tq > .fx", "padding-top: 0;", M)
    css.add(".tq-quote p", "font-size: 24px; line-height: 31.92px;", M)
    css.add(".tq-name", "font-size: 20px; line-height: 35.96px;", M)
    css.add(".tq-dept", "font-size: 16px; line-height: 28px;", M)
    css.add(".tq-ctas", "flex-direction: column; gap: 18px;", M)
    css.add(".tq-ctas .pbtn", "height: 50px;", M)
    css.add(".pd > .fx, .tb > .fx, .ts > .fx, .tq > .fx", "max-width: 640px; margin: 0 auto; box-sizing: border-box;", M)
    css.add(".tq > .fx", "border-top: 0;", M)

    NOTE = (f"2026-09-28 {SLUG} replica (Flow A, HTML first). Figma {cfg['frame']}. Generated by tools/figma_html/build_product.py "
            "(one generator for Main / Variation A / Variation B = one product template on the real site).")
    SECTIONS = [
        {"id": "site-header", "landmark": "header", "escape_hatch": True, "html": head, "css": SHARED + HEADER_CSS, "js": HEADER_JS},
        {"id": "product-overview", "escape_hatch": True, "heading_level": 1, "html": INTRO_HTML, "css": css.render()},
    ]
    if TABLE_HTML:
        SECTIONS.append({"id": "product-table", "escape_hatch": True, "html": TABLE_HTML, "css": ""})
    SECTIONS += [
        {"id": "accessories", "escape_hatch": True, "html": ACC_HTML, "css": ""},
        {"id": "testimonial", "escape_hatch": True, "html": TESTI_HTML, "css": ""},
        {"id": "related-products", "escape_hatch": True, "html": REL_HTML, "css": ""},
        {"id": "site-footer", "landmark": "footer", "escape_hatch": True, "html": FOOT_HTML, "css": FOOT_CSS},
    ]
    for s in SECTIONS:
        s["notes"] = [NOTE]
        s["html"] = link_pages(s["html"]).replace('href="#products"', f'href="{BROWSE}"')
    ptitle = "".join(t for t, _ in tl[0]).strip()
    bp = {"page": SLUG, "meta": {"title": f"{ptitle} | Mizuho America", "description": desc_t["characters"][:155]},
          "css_workflow": "scss", "font_source": "google",
          "notes_for_developer": ["Real site: one m11_product single template; this frame's optional parts are switched on by its data."],
          "sections": SECTIONS}
    ARROW = ('<svg xmlns="http://www.w3.org/2000/svg" width="12" height="14" viewBox="0 0 12 14" fill="none" stroke="#0065B3" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M6 1v12"/><path d="M1 8l5 5 5-5"/></svg>')
    CARET = ('<svg xmlns="http://www.w3.org/2000/svg" width="41" height="40" viewBox="0 0 41 40"><rect x="0" y="0" width="1" height="40" fill="#000000" '
             'fill-opacity="0.2"/><path d="M14 15h12l-6 10z" fill="#000000"/></svg>')
    compile_page(SLUG, bp, extra_images=("logo-mizuho-header-srgb.png", "logo-mizuho-footer-reversed.png", "icon-play-circle.svg"),
                 svgs={"icon-arrow-down-blue.svg": ARROW, "icon-select-caret.svg": CARET})
    return P


if __name__ == "__main__":
    for k in (sys.argv[1:] or ["main", "a", "b"]):
        build(k)
