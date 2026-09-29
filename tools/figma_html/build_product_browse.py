"""Product Browse replica (Figma 1:3176 desktop 1440 / 1:1152 mobile 430) → pages/product-browse/html/.

Same method as the other replicas (see build_resources.py). The product tiles, filters and search bar are the same
components as the Sales Hub Resource Library (build_resource_library.py), with procedure tags + "View product" and a pager.
Replica links: navbar Products = this page; the Sugita II tile → Product Main; procedure "View product →" → one product page
each (demo mapping, documented in BUILD-NOTES). On the real site this page is the m11_product archive (/products/).

    python tools/figma_html/build_product_browse.py
"""
import os
import shutil
from html import escape

import cv2
import numpy as np

from chrome import D, FOOT_CSS, FOOT_HTML, FR, HEADER_CSS, HEADER_HTML, HEADER_JS, M, MU, OS, ROOT, SHARED, link_pages, u
from chrome_portal import CARET_SVG  # noqa: F401  (kept for parity with the other Sales Hub-style controls)
from replica_lib import Css, Page, compile_page, figma_linear, slug

P = Page("1:3176")
PM = Page("1:1152")
box, y, plain, text = P.box, P.y, P.plain, P.text
SLUG = "product-browse"
IMG = os.path.join(ROOT, "pages", SLUG, "figma", "images")
os.makedirs(IMG, exist_ok=True)
INK, BLUE, SKY = "#090909", "#0065B3", "#00B3F0"
LINK = {"main": "../../product-main/html/", "a": "../../product-variation-a/html/", "b": "../../product-variation-b/html/"}
css = Css()

HERO = dict(h1="1:3316", panel="1:3311", h2="1:3312", sub="1:3315", body="1:3314", link="1:3313")
HERO_M = dict(panel="1:1169", texts=["1:1171", "1:1172", "1:1173", "1:1174"])
PROC = dict(band="1:3301", h2="1:3305", lead="1:3306",
            items=[("1:3307", "1:3302", "a"), ("1:3309", "1:3303", "main"), ("1:3308", "1:3304", "b")],
            icons={"1:3307": "procedure-icon-tumor-removal.png", "1:3309": "procedure-icon-aneurysm.png",
                   "1:3308": "procedure-icon-endoscopic-endonasal.png"})
BP = dict(h2="1:3292", lead="1:3291", filters="1:3262", head="1:3263", groups=[("1:3265", ["1:3267", "1:3268", "1:3271", "1:3266"]),
          ("1:3272", ["1:3273", "1:3274", "1:3275"]), ("1:3276", ["1:3277", "1:3278", "1:3279"])], checked={"1:3268"},
          button="1:3280", button_text="1:3281", panel="1:3191", input="1:3283", placeholder="1:3288", go="1:3289", go_text="1:3290",
          line="1:3192", count="1:3194", chip="1:3196", chip_text="1:3198", clear="1:3199",
          tiles=[("1:3203", "1:3205", "1:3217", ["1:3209", "1:3212", "1:3215"], "main"),
                 ("1:3220", "1:3222", "1:3231", ["1:3229", "1:3226"], None),
                 ("1:3234", "1:3236", "1:3242", ["1:3240"], None),
                 ("1:3245", "1:3247", "1:3259", ["1:3251", "1:3254", "1:3257"], None)],
          pager=("1:3294", "1:3298", "1:3296"))
# Resource Library cleaned the same four product photos (same Figma image refs, tag chip inpainted)
TAG_TEXT = {"1:3217": "1:3218", "1:3231": "1:3232", "1:3242": "1:3243", "1:3259": "1:3260"}
TILE_IMG = ["tile-sugita-ii-head-frame-product-brochure.jpg", "tile-radiolucent-head-frame-spec-sheet.jpg",
            "tile-smart-fix-head-holder-spec-sheet.jpg", "tile-head-frame-accessories.jpg"]
# Same Figma image refs as the Resource Library tiles, but that frame draws them faded: crop this page's own export
# and inpaint the category chip baked onto each photo.
_exp = cv2.imread(os.path.join(ROOT, "pages/_figma/frames/export/Product Browse.png"))
for (rect, _t, tag, _p, _l), f in zip(BP["tiles"], TILE_IMG):
    tx_, ty_ = (int(round(v)) for v in box(rect)[:2])
    im_ = _exp[ty_:ty_ + 195, tx_:tx_ + 307].copy()
    mk = np.zeros(im_.shape[:2], np.uint8)
    cx_, cy_, cw_, ch_ = box(tag)
    cv2.rectangle(mk, (int(cx_ - tx_ - 2), int(cy_ - ty_ - 2)), (int(cx_ - tx_ + cw_ + 2), int(cy_ - ty_ + ch_ + 2)), 255, -1)
    cv2.imwrite(os.path.join(IMG, f), cv2.inpaint(im_, mk, 7, cv2.INPAINT_TELEA), [cv2.IMWRITE_JPEG_QUALITY, 90])
for f in PROC["icons"].values():
    shutil.copy(os.path.join(ROOT, "pages", "mizuho-home", "figma", "images", f), os.path.join(IMG, f))


# ---------------------------------------------------------------- hero backgrounds: export crop with the text inpainted
def clean_hero(export, page, panel, text_ids, out):
    exp = cv2.imread(os.path.join(ROOT, "pages/_figma/frames/export", export))
    x, y_, w, h = (int(round(v)) for v in page.box(panel))
    img = exp[y_:y_ + h, x:x + w].copy()
    m = np.zeros(img.shape[:2], np.uint8)
    for t in text_ids:
        tx, ty, tw, th = (int(round(v)) for v in page.box(t))
        roi = img[ty - y_ - 4:ty - y_ + th + 4, tx - x - 4:tx - x + tw + 30].astype(np.int16)
        blur = cv2.GaussianBlur(roi, (0, 0), 6)
        d = ((blur - roi).max(axis=2) > 25).astype(np.uint8) * 255  # dark text on the light photo
        m[ty - y_ - 4:ty - y_ + th + 4, tx - x - 4:tx - x + tw + 30] = d
    m = cv2.dilate(m, np.ones((7, 7), np.uint8))
    img = cv2.inpaint(img, m, 9, cv2.INPAINT_TELEA)
    cv2.imwrite(os.path.join(IMG, out), img, [cv2.IMWRITE_JPEG_QUALITY, 88])


clean_hero("Product Browse.png", P, HERO["panel"], [HERO["h2"], HERO["sub"], HERO["body"], HERO["link"]], "products-hero.jpg")
clean_hero("Product Browse - m.png", PM, HERO_M["panel"], HERO_M["texts"], "products-hero-m.jpg")

# ================================================================ header
HEAD_HTML = HEADER_HTML.replace('<a href="#products">', '<a class="is-current" aria-current="page" href="#products">', 1)
assert HEAD_HTML != HEADER_HTML
css.add(".site-head__nav a.is-current", f"color: {BLUE};")

# ================================================================ hero (1:3310)
h1x, h1y = box(HERO["h1"])[:2]
px, py, pw, ph = box(HERO["panel"])
h2x, h2y, h2w = box(HERO["h2"])[:3]
HERO_HTML = (f'<section class="rs pbh" id="products-intro"><div class="fx"><h1 class="pbh-h1">{plain(HERO["h1"])}</h1>'
             f'<div class="pbh-panel"><h2 class="pbh-h2">{P.br(HERO["h2"])}</h2><p class="pbh-sub">{plain(HERO["sub"])}</p>'
             f'<p class="pbh-body">{plain(HERO["body"])}</p><a class="pbh-link" href="#browse-by-product">{plain(HERO["link"])}</a></div></div></section>')
css.add(".pbh-h1", f"font-family: {FR}; font-weight: 400; color: {BLUE}; text-transform: uppercase;")
css.add(".pbh-panel", 'box-sizing: border-box; background: #FFFFFF url("../figma/images/products-hero.jpg") no-repeat center / 100% 100%;')
css.add(".pbh-h2", f"font-family: {FR}; font-weight: 400; color: #000000; text-transform: uppercase;")
css.add(".pbh-sub, .pbh-body, .pbh-link", f"font-family: {OS}; color: #000000;")
css.add(".pbh-sub", "font-weight: 700;")
css.add(".pbh-body", "font-weight: 300;")
css.add(".pbh-link", f"display: inline-block; font-weight: 700; color: {BLUE};")
css.add(".pbh > .fx", f"padding: {u(h1y - 161)} 0 {u(y(PROC['band']) - py - ph)} {u(px)};", D)
css.add(".pbh-h1", f"margin-left: {u(h1x - px)}; font-size: {u(45)}; line-height: {u(70)}; min-height: {u(py - h1y)};", D)
css.add(".pbh-panel", f"width: {u(pw)}; height: {u(ph)}; border-radius: {u(20)}; padding: {u(h2y - py)} 0 0 {u(h2x - px)};", D)
css.add(".pbh-h2", f"width: {u(h2w)}; font-size: {u(38)}; line-height: {u(46)}; min-height: {u(y(HERO['sub']) - h2y)};", D)
css.add(".pbh-sub", f"font-size: {u(16)}; line-height: {u(22)}; min-height: {u(y(HERO['body']) - y(HERO['sub']))};", D)
css.add(".pbh-body", f"width: {u(box(HERO['body'])[2])}; font-size: {u(16)}; line-height: {u(22)}; min-height: {u(y(HERO['link']) - y(HERO['body']))};", D)
css.add(".pbh-link", f"font-size: {u(16)}; line-height: {u(22)};", D)
css.add(".pbh-h1", "font-size: 36px; line-height: 41.4px;", M)
css.add(".pbh-panel", 'display: flex; flex-direction: column; gap: 20px; padding: 32px 32px 118px; border-radius: 20px; background-image: url("../figma/images/products-hero-m.jpg");', M)
css.add(".pbh-h2", "font-size: 32px; line-height: 46px;", M)
css.add(".pbh-sub, .pbh-body", "font-size: 14px; line-height: 22px;", M)
css.add(".pbh-link", "font-size: 16px; line-height: 22px;", M)

# ================================================================ browse by procedure (1:3300) - blue band
bx, by, bw, bh = box(PROC["band"])
proc_items = []
for icon, txt, target in PROC["items"]:
    lines = P.fig_lines(txt)
    words = ["".join(t for t, _ in ln).strip() for ln in lines]
    words = [w for w in words if w]
    title, view, more = " ".join(words[:-2]), words[-2], words[-1]
    ix, iy, iw, ih = box(icon)
    tx, ty, tw = box(txt)[:3]
    proc_items.append(f'<article class="pr-item pr-item--{slug(title)[:10]}"><img class="pr-icon" src="figma/images/{PROC["icons"][icon]}" alt="" width="{iw:g}" height="{ih:g}" loading="lazy">'
                      f'<div class="pr-text"><h3 class="pr-title">{escape(title)}</h3><a class="pr-view" href="{LINK[target]}">{escape(view)}</a>'
                      f'<a class="pr-more" href="#browse-by-product">{escape(more)}</a></div></article>')
PROC_HTML = (f'<section class="rs pr" id="browse-by-procedure"><div class="fx"><div class="pr-head"><h2 class="pr-h2">{plain(PROC["h2"])}</h2>'
             f'<p class="pr-lead">{plain(PROC["lead"])}</p></div><div class="pr-items">{"".join(proc_items)}</div></div></section>')
css.add(".pr", f"background: {BLUE}; color: #FFFFFF;")
css.add(".pr > .fx", f"background: {BLUE};")
css.add(".pr-h2", f"font-family: {MU}; font-weight: 700;")
css.add(".pr-lead", f"font-family: {MU}; font-weight: 400;")
css.add(".pr-item", "position: relative;")
css.add(".pr-icon", "display: block; object-fit: cover;")
css.add(".pr-item--endoscopic .pr-icon", "object-fit: fill;")  # Figma STRETCH
css.add(".pr-title, .pr-view, .pr-more", "margin: 0; font-family: 'Montserrat', sans-serif; font-weight: 700;")
css.add(".pr-view", "display: block; color: #FFFFFF;")
css.add(".pr-more", "display: block; color: #77DCFF;")
css.add(".pr", f"height: {u(bh)};", D)
css.add(".pr > .fx", f"padding: {u(y(PROC['h2']) - by)} 0 0 {u(box(PROC['h2'])[0])}; box-sizing: border-box;", D)
css.add(".pr-h2", f"font-size: {u(34)}; line-height: {u(50)}; min-height: {u(y(PROC['lead']) - y(PROC['h2']))};", D)
css.add(".pr-lead", f"width: {u(box(PROC['lead'])[2])}; font-size: {u(18)}; line-height: {u(50)};", D)
css.add(".pr-items", f"position: absolute; left: 0; top: 0; width: {u(1440)}; height: {u(bh)};", D)
for icon, txt, _ in PROC["items"]:
    ix, iy, iw, ih = box(icon)
    tx, ty, tw = box(txt)[:3]
    title = slug(text(txt).split("\n")[0])[:10]
    css.add(f".pr-item--{title}", f"position: absolute; left: {u(ix)}; top: {u(min(iy, ty) - by)};", D)
    css.add(f".pr-item--{title} .pr-icon", f"width: {u(iw)}; height: {u(ih)}; margin-top: {u(iy - min(iy, ty))};", D)
    css.add(f".pr-item--{title} .pr-text", f"position: absolute; left: {u(tx - ix)}; top: {u(ty - min(iy, ty))}; width: {u(tw)};", D)
css.add(".pr-title", f"font-size: {u(20)}; line-height: {u(30)}; padding-top: {u(5)};", D)
css.add(".pr-view", f"font-size: {u(16)}; line-height: {u(36)}; margin-bottom: {u(26)};", D)
css.add(".pr-more", f"font-size: {u(16)}; line-height: {u(26)};", D)
# chrome SHARED paints every mobile section #FCFEFF via .rs:not(.pb):not(.site-foot) (0,3,0); beat it for this blue band
css.add(".rs.pr.pr, .rs.pr.pr > .fx", f"background: {BLUE};", M)
css.add(".pr-head", "display: flex; flex-direction: column; gap: 10px;", M)
css.add(".pr-h2", "font-size: 28px; line-height: 46.54px;", M)
css.add(".pr-lead", "font-size: 18px; line-height: 29.92px;", M)
css.add(".pr-items", "display: flex; flex-direction: column; gap: 36px;", M)
css.add(".pr-item", "display: grid; grid-template-columns: 156px 1fr; align-items: center; min-height: 135px;", M)
css.add(".pr-icon", "width: 119px; height: 119px;", M)
css.add(".pr-item--aneurysm .pr-icon", "width: 83px; height: 115px; margin-left: 24px;", M)
css.add(".pr-item--endoscopic .pr-icon", "width: 113px; height: 103px;", M)
css.add(".pr-title", "font-size: 18px; line-height: 24px;", M)
css.add(".pr-view", "font-size: 14px; line-height: 40px; margin-bottom: 8px;", M)
css.add(".pr-more", "font-size: 14px; line-height: 22px;", M)

# ================================================================ browse by product (1:3190)
fx_, fy_, fw_, fh_ = box(BP["filters"])
hx, hy = box(BP["head"])[:2]


def group(text_id, boxes, name):
    lines = P.fig_lines(text_id)
    heading = "".join(t for t, _ in lines[0]).strip()
    rows = []
    for li, line in enumerate(l for l in lines[1:] if "".join(t for t, _ in l).strip()):
        label = " ".join("".join(t for t, _ in line).replace(" .", " ").split())
        cid = f"pf-{slug(label)}"
        chk = " checked" if boxes[li] in BP["checked"] else ""
        rows.append(f'<li class="fl-row"><input class="fl-box" type="checkbox" id="{cid}" name="{name}" value="{slug(label)}"{chk}>'
                    f'<label class="fl-label" for="{cid}">{escape(label)}</label></li>')
    return f'<fieldset class="fl-group"><legend class="fl-h">{escape(heading)}</legend><ul class="fl-list">{"".join(rows)}</ul></fieldset>'


head_lines = P.fig_lines(BP["head"])
FILTERS = (f'<aside class="pb-filters" aria-label="Filter products"><form class="fl-form" action="#browse-by-product">'
           f'<div class="pbf-head"><h3 class="pbf-h">{escape("".join(t for t, _ in head_lines[0]).strip())}</h3>'
           f'<p class="pbf-sub">{escape("".join(t for t, _ in head_lines[1]).strip())}</p><span class="pbf-chev m-only" aria-hidden="true"></span></div>'
           + "".join(group(t, b, n) for (t, b), n in zip(BP["groups"], ("category", "configuration", "procedure")))
           + f'<button class="fl-clear" type="reset">{plain(BP["button_text"])}</button></form></aside>')
g_tops = [y(t) for t, _ in BP["groups"]]
g_rows = [y(b[0]) - 7 for _, b in BP["groups"]]
g_n = [len(b) for _, b in BP["groups"]]
btn_x, btn_y, btn_w, btn_h = box(BP["button"])
CHECK_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="#000000" stroke-width="2" '
             'stroke-linecap="round"><path d="M4 12l4 4"/><path d="M7 16l10-11.5"/></svg>')
css.add(".pb-filters", "background: rgba(196, 196, 196, 0.1); box-shadow: inset 0 0 0 0.5px rgba(0, 0, 0, 0.35); border-radius: 12px; box-sizing: border-box;")
css.add(".pbf-head", "position: relative;")
css.add(".pbf-h", f"margin: 0; font-family: {OS}; font-weight: 700; color: {INK}; text-transform: uppercase;")
css.add(".pbf-sub", f"margin: 0; font-family: {OS}; font-weight: 300; color: {INK};")
css.add(".pbf-chev", 'position: absolute; right: 0; top: 5.5px; width: 13px; height: 8px; background: url("../figma/images/icon-chevron-down.svg") no-repeat center / contain;')
css.add(".fl-group", "margin: 0; padding: 0; border: 0; min-width: 0;")
css.add(".fl-h", f"padding: 0; font-family: {OS}; font-weight: 700; color: {INK}; text-transform: uppercase;")
css.add(".fl-list", "margin: 0; padding: 0; list-style: none;")
css.add(".fl-row", "display: grid; grid-template-columns: 20px 1fr; align-items: center; column-gap: 8px;")
css.add(".fl-box", "appearance: none; -webkit-appearance: none; width: 20px; height: 20px; margin: 0; background: #FFFFFF no-repeat center / 20px 20px; border: 1px solid rgba(0, 0, 0, 0.5); border-radius: 0; cursor: pointer;")
css.add(".fl-box:checked", 'background-image: url("../figma/images/icon-check.svg");')
css.add(".fl-box:focus-visible", f"outline: 2px solid {SKY}; outline-offset: 2px;")
css.add(".fl-label", f"font-family: {OS}; font-weight: 400; color: {INK}; cursor: pointer;")
css.add(".fl-clear", f"display: block; box-sizing: border-box; background: #FFFFFF; border: 2px solid {SKY}; border-radius: 5px; font-family: {FR}; font-weight: 400; color: {BLUE}; cursor: pointer;")
css.add(".pb-filters", f"width: {u(fw_)}; min-height: {u(fh_)}; padding: {u(hy - fy_)} {u(fx_ + fw_ - btn_x - btn_w)} 0 {u(hx - fx_)};", D)
css.add(".pbf-h", f"font-size: {u(16)}; line-height: {u(22)};", D)
css.add(".pbf-sub", f"font-size: {u(14)}; line-height: {u(24)};", D)
css.add(".pbf-head", f"min-height: {u(g_tops[0] - hy)};", D)
css.add(".fl-h", f"font-size: {u(14)}; line-height: {u(22)};", D)
for i in range(3):
    css.add(f".fl-group:nth-of-type({i + 1}) .fl-h", f"min-height: {u(g_rows[i] - g_tops[i])};", D)
    if i:
        css.add(f".fl-group:nth-of-type({i + 1})", f"margin-top: {u(g_tops[i] - g_rows[i - 1] - 34 * g_n[i - 1])};", D)
css.add(".fl-row", f"height: {u(34)};", D)
css.add(".fl-label", f"font-size: {u(14)}; line-height: {u(22)};", D)
css.add(".fl-clear", f"margin-top: {u(btn_y - g_rows[2] - 34 * g_n[2])}; width: {u(btn_w)}; height: {u(btn_h)}; font-size: {u(16)};", D)
css.add(".pb-filters", "padding: 20px 16px 21px 26px;", M)
css.add(".pbf-h", "font-size: 16px; line-height: 22px;", M)
css.add(".pbf-sub", "font-size: 14px; line-height: 24px;", M)
css.add(".pbf-head", "min-height: 69px;", M)
css.add(".fl-h", "font-size: 14px; line-height: 22px; min-height: 24px;", M)
css.add(".fl-group + .fl-group", "margin-top: 17px;", M)
css.add(".fl-row", "height: 34px;", M)
css.add(".fl-label", "font-size: 14px; line-height: 22px;", M)
css.add(".fl-clear", "margin-top: 22px; width: 100%; height: 50px; font-size: 16px;", M)

# toolbar
tx0, ty0, tw0, th0 = box(BP["panel"])
ix, iy, iw, ih = box(BP["input"])
gx, gy, gw, gh = box(BP["go"])
lx, ly, lw = box(BP["line"])[:3]
cx, cy = box(BP["count"])[:2]
chip_y = y(BP["chip"])
count_html = P.inline(P.fig_lines(BP["count"])[0])
TOOLBAR = (f'<div class="pb-tools"><form class="pb-search" role="search" action="#browse-by-product">'
           f'<label class="visually-hidden" for="pb-q">Search products</label>'
           f'<input class="pb-q" id="pb-q" type="search" name="q" placeholder="{plain(BP["placeholder"])}">'
           f'<button class="pb-go" type="submit">{plain(BP["go_text"])}</button></form><hr class="pb-line">'
           f'<p class="pb-count" aria-live="polite">{count_html}</p><div class="pb-active">'
           f'<button class="chip" type="button" aria-label="Remove filter: {plain(BP["chip_text"])}">{plain(BP["chip_text"])}<span class="chip-x" aria-hidden="true"></span></button>'
           f'<a class="pb-clear-all" href="#browse-by-product">{plain(BP["clear"])}</a></div></div>')
SEARCH_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 25 25" fill="none" stroke="#ADADAD" stroke-width="2">'
              '<circle cx="10.5" cy="10.5" r="9.5"/><path d="M17.4 17.4l6 6" stroke-linecap="round"/></svg>')
X_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="#000000" stroke-width="2">'
         '<path d="M4.5 4.5l9 9M13.5 4.5l-9 9"/></svg>')
css.add(".pb-tools", f"background: {figma_linear(P.node(BP['panel'])['fills'][0], tw0, th0)}; box-shadow: inset 0 0 0 0.5px rgba(0, 0, 0, 0.4); border-radius: 12px; box-sizing: border-box;")
css.add(".pb-search", "display: flex;")
css.add(".pb-q", f'flex: 1; min-width: 0; box-sizing: border-box; background: #FFFFFF url("../figma/images/icon-search.svg") no-repeat; border: 1px solid rgba(0, 0, 0, 0.35); font-family: {OS}; font-weight: 400; color: #000000;')
css.add(".pb-q::placeholder", "color: rgba(0, 0, 0, 0.35); opacity: 1;")
css.add(".pb-go", f"border: 0; border-radius: 5px; background: {BLUE}; color: #FFFFFF; font-family: {FR}; font-weight: 400; cursor: pointer;")
css.add(".pb-line", "margin: 0; border: 0; border-top: 1px solid rgba(0, 0, 0, 0.25);")
css.add(".pb-count", f"margin: 0; font-family: {OS}; color: {INK};")
css.add(".pb-count strong", "font-weight: 700;")
css.add(".pb-count span", "font-weight: 300;")
css.add(".pb-active", "display: flex; align-items: center;")
css.add(".chip", f"position: relative; display: flex; align-items: center; box-sizing: border-box; width: 187px; height: 28px; padding: 0 0 0 9px; background: rgba(119, 220, 255, 0.15); border: 0.5px solid rgba(0, 0, 0, 0.35); border-radius: 5px; font-family: {OS}; font-weight: 700; font-size: 11px; line-height: 22px; color: {INK}; text-align: left; cursor: pointer;")
css.add(".chip-x", 'position: absolute; right: 5px; top: 5px; width: 18px; height: 18px; box-sizing: border-box; background: #FFFFFF url("../figma/images/icon-chip-x.svg") no-repeat center / 18px 18px; border: 0.5px solid rgba(0, 0, 0, 0.35); border-radius: 3px;')
css.add(".pb-clear-all", f"font-family: {OS}; font-weight: 700; font-size: 11px; line-height: 22px; color: {BLUE};")
css.add(".pb-tools", f"padding: {u(iy - ty0)} {u(tx0 + tw0 - gx - gw)} 0 {u(ix - tx0)}; height: {u(th0)};", D)
css.add(".pb-search", f"gap: {u(gx - ix - iw)};", D)
css.add(".pb-q", f"height: {u(ih)}; padding-left: {u(57)}; border-radius: {u(5)}; background-position: {u(17)} {u(10)}; background-size: {u(25)} {u(25)}; font-size: {u(15)}; line-height: {u(20.43)};", D)
css.add(".pb-go", f"width: {u(gw)}; height: {u(gh)}; font-size: {u(16)};", D)
css.add(".pb-line", f"margin: {u(ly - iy - ih)} 0 0 {u(lx - ix)}; width: {u(lw)};", D)
css.add(".pb-count", f"margin: {u(cy - ly - 1)} 0 0 {u(cx - ix)}; font-size: {u(20)}; line-height: {u(22)}; min-height: {u(chip_y - cy)};", D)
css.add(".pb-active", f"margin-left: {u(cx - ix)}; gap: {u(y(BP['clear']) and box(BP['clear'])[0] - box(BP['chip'])[0] - 187)};", D)
css.add(".pb-tools", "display: flex; flex-direction: column; gap: 24px; padding: 25px;", M)
css.add(".pb-search", "flex-direction: column; align-items: flex-end; gap: 21px;", M)
css.add(".pb-q", "align-self: stretch; flex: none; height: 40px; padding-left: 29px; border-radius: 6px; background-position: 12px 12px; background-size: 16px 16px; font-size: 12px; line-height: 16.34px;", M)
css.add(".pb-go", "padding: 6px 20px; font-size: 16px; line-height: 21.28px;", M)
css.add(".pb-count", "font-size: 18px; line-height: 22px; margin-bottom: -10px;", M)
css.add(".pb-active", "gap: 18px;", M)

# tiles
tiles = []
for (rect, tx, tag, procs, target), img in zip(BP["tiles"], TILE_IMG):
    lines = P.fig_lines(tx)
    title = "".join(s for s, _ in lines[0]).strip()
    sub = "".join(s for s, _ in lines[1]).strip() if len(lines) > 1 else ""
    href = LINK[target] if target else f"#product-{slug(title)}"
    tags = "".join(f'<li class="ptag">{plain(p)}</li>' for p in procs)
    tiles.append(f'<li class="tile ptile"><div class="tile-media"><img src="figma/images/{img}" alt="{escape(title)}" width="307" height="195" loading="lazy">'
                 f'<span class="tile-tag">{plain(TAG_TEXT[tag])}</span></div><div class="tile-text"><h3 class="tile-title">{escape(title)}</h3><p class="tile-sub">{escape(sub)}</p></div>'
                 f'<ul class="ptags" aria-label="Procedures">{tags}</ul><a class="tile-view" href="{href}">View product<span class="visually-hidden">: {escape(title)}</span></a></li>')
t0, t1, t3 = box(BP["tiles"][0][0]), box(BP["tiles"][1][0]), box(BP["tiles"][3][0])
pg = [box(r) for r in BP["pager"]]
PAGER = ('<nav class="pager" aria-label="Product pages"><ul class="pager-list"><li><a class="pg pg--nav" href="#browse-by-product" aria-disabled="true">&lt;Prev</a></li>'
         '<li><a class="pg pg--num" href="#browse-by-product" aria-current="page">1</a></li><li><a class="pg pg--nav" href="#browse-by-product" aria-disabled="true">Next&gt;</a></li></ul></nav>')
lx0, ly0, lw0 = box(BP["lead"])[:3]
BP_HTML = (f'<section class="rs pbp" id="browse-by-product"><div class="fx"><div class="pbp-head"><h2 class="pbp-h2">{plain(BP["h2"])}</h2>'
           f'<p class="pbp-lead">{plain(BP["lead"])}</p></div><div class="pbp-layout">{FILTERS}<div class="pbp-results">{TOOLBAR}'
           f'<ul class="tiles">{"".join(tiles)}</ul>{PAGER}</div></div><hr class="rule pbp-end m-only"></div></section>')
css.add(".pbp-h2", f"margin: 0; font-family: {FR}; font-weight: 400; color: {BLUE};")
css.add(".pbp-lead", f"margin: 0; font-family: {OS}; font-weight: 400; color: #000000;")
css.add(".tiles", "margin: 0; padding: 0; list-style: none;")
css.add(".tile", f"position: relative; box-sizing: border-box; overflow: hidden; background: {figma_linear(P.node(BP['tiles'][0][0])['fills'][0], 307, 345)}, #FFFFFF; border: 0.5px solid rgba(0, 0, 0, 0.35);")
css.add(".tile-media", "position: relative; background: #FFFFFF; border-bottom: 0.5px solid rgba(0, 0, 0, 0.35);")
css.add(".tile-media > img", "width: 100%; height: 100%; object-fit: cover;")
css.add(".tile-tag", f"position: absolute; box-sizing: border-box; height: 28px; padding: 3px 9px; background: rgba(231, 249, 255, 0.9); border: 0.5px solid rgba(0, 0, 0, 0.35); border-radius: 5px; white-space: nowrap; font-family: {OS}; font-weight: 400; font-size: 11px; line-height: 22px; color: {INK};")
css.add(".tile-title", f"margin: 0; font-family: {OS}; font-weight: 700; font-size: 14px; line-height: 22px; color: {INK};")
css.add(".tile-sub", f"margin: 0; font-family: {OS}; font-weight: 300; font-size: 14px; line-height: 20px; color: {INK};")
css.add(".ptags", "display: flex; flex-wrap: wrap; gap: 5px; margin: 0; padding: 0; list-style: none;")
css.add(".ptag", f"box-sizing: border-box; height: 28px; padding: 3px 9px; background: rgba(208, 208, 208, 0.15); border: 0.5px solid rgba(0, 0, 0, 0.35); border-radius: 5px; font-family: {OS}; font-weight: 400; font-size: 11px; line-height: 22px; color: {INK};")
css.add(".tile-view", f"display: inline-block; font-family: {OS}; font-weight: 700; font-size: 14px; line-height: 22px; color: {BLUE};")
css.add(".pager-list", "display: flex; justify-content: center; margin: 0; padding: 0; list-style: none;")
css.add(".pg", f"display: flex; align-items: center; justify-content: center; border-radius: 5px; font-family: {FR}; font-weight: 400;")
css.add(".pg--nav", f"background: {BLUE}; color: #FFFFFF; font-size: 14px;")
css.add(".pg--num", f"background: rgba(0, 101, 179, 0.15); color: {BLUE}; font-size: 16px;")
css.add(".pbp > .fx", f"padding: {u(y(BP['h2']) - by - bh)} 0 {u(2703 - pg[0][1] - pg[0][3])} {u(fx_)};", D)
css.add(".pbp-head", f"display: flex; min-height: {u(fy_ - y(BP['h2']))};", D)
css.add(".pbp-h2", f"margin-left: {u(box(BP['h2'])[0] - fx_)}; width: {u(lx0 - box(BP['h2'])[0])}; font-size: {u(34)}; line-height: {u(50)};", D)
css.add(".pbp-lead", f"margin-top: {u(ly0 - y(BP['h2']))}; width: {u(lw0)}; font-size: {u(15)}; line-height: {u(27)};", D)
css.add(".pbp-layout", f"display: grid; grid-template-columns: {u(fw_)} {u(tw0)}; column-gap: {u(tx0 - fx_ - fw_)}; align-items: start;", D)
css.add(".tiles", f"display: grid; grid-template-columns: repeat(3, {u(t0[2])}); gap: {u(t3[1] - t0[1] - t0[3])} {u(t1[0] - t0[0] - t0[2])}; margin-top: {u(t0[1] - ty0 - th0)};", D)
css.add(".tile", f"height: {u(t0[3])}; border-radius: {u(12)};", D)
css.add(".tile-media", f"height: {u(195)}; border-radius: {u(12)} {u(12)} 0 0;", D)
css.add(".tile-tag", f"left: {u(13)}; top: {u(153)}; width: {u(134)};", D)
css.add(".tile-text", f"margin: {u(11)} 0 0 {u(13)}; min-height: {u(52)};", D)
css.add(".ptags", f"margin-left: {u(13)}; min-height: {u(55)};", D)
css.add(".tile-view", f"margin-left: {u(13)};", D)
css.add(".pager", f"margin-top: {u(pg[0][1] - t3[1] - t3[3])}; padding-left: {u(2 * ((pg[0][0] + pg[2][0] + pg[2][2]) / 2 - (tx0 + tw0 / 2)))};", D)
css.add(".pager-list", f"gap: {u(pg[1][0] - pg[0][0] - pg[0][2])};", D)
css.add(".pg", f"width: {u(57)}; height: {u(40)}; line-height: {u(40)};", D)
css.add(".pbp-head", "display: flex; flex-direction: column; gap: 12px;", M)
css.add(".pbp-h2", "font-size: 32px; line-height: 42.56px;", M)
css.add(".pbp-lead", "font-size: 15px; line-height: 27px;", M)
css.add(".pbp-layout, .pbp-results, .tiles", "display: flex; flex-direction: column; gap: 36px;", M)
css.add(".pbp > .fx", "padding-bottom: 0;", M)
css.add(".pbp-end", "margin-top: 8px;", M)
css.add(".tile", "height: 345px; border-radius: 12px;", M)
css.add(".tile-media", "height: 195px; border-radius: 12px 12px 0 0;", M)
css.add(".tile-tag", "left: 16.5px; top: 153px; width: 170px;", M)
css.add(".tile-text", "margin: 11px 0 0 16.5px; min-height: 52px;", M)
css.add(".ptags", "margin-left: 16.5px; min-height: 55px;", M)
css.add(".ptag", "padding: 3px 11.4px;", M)
css.add(".tile-view", "margin-left: 16.5px;", M)
css.add(".pager-list", "gap: 20.6px;", M)
css.add(".pager-list li", "flex: 1;", M)
css.add(".pg", "height: 40px; line-height: 40px;", M)
css.add(".pbh > .fx, .pr > .fx, .pbp > .fx", "max-width: 640px; margin: 0 auto; box-sizing: border-box;", M)

# ================================================================ blueprint + compile
NOTE = ("2026-09-28 Product Browse replica (Flow A, HTML first). Figma 1:3176 / 1:1152. Generated by tools/figma_html/build_product_browse.py; "
        "copy from pages/_figma/file.json by node id.")
SECTIONS = [
    {"id": "site-header", "landmark": "header", "escape_hatch": True, "html": HEAD_HTML, "css": SHARED + HEADER_CSS, "js": HEADER_JS},
    {"id": "products-intro", "escape_hatch": True, "heading_level": 1, "html": HERO_HTML, "css": css.render()},
    {"id": "browse-by-procedure", "escape_hatch": True, "html": PROC_HTML, "css": ""},
    {"id": "browse-by-product", "escape_hatch": True, "html": BP_HTML, "css": ""},
    {"id": "site-footer", "landmark": "footer", "escape_hatch": True, "html": FOOT_HTML, "css": FOOT_CSS},
]
for s in SECTIONS:
    s["notes"] = [NOTE]
    s["html"] = link_pages(s["html"]).replace('href="#products"', 'href="./"')
bp = {"page": SLUG,
      "meta": {"title": "Products | Mizuho America",
               "description": "Browse Mizuho America's neurosurgical products by procedure, category and configuration."},
      "css_workflow": "scss", "font_source": "google",
      "notes_for_developer": ["Real site: this is the m11_product archive; the tiles, counts, filters and pager come from the query.",
                              "The hero photo carries the Shutterstock watermark (issues-log #11) and is a flattened export crop (#28)."],
      "sections": SECTIONS}
CHEV_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="22" height="12" viewBox="0 0 22 12" fill="none" stroke="#000000" stroke-width="3" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="M2 2l9 8 9-8"/></svg>')
compile_page(SLUG, bp, font_weights={"Mukta": [400, 700]}, extra_images=("logo-mizuho-header-srgb.png", "logo-mizuho-footer-reversed.png"),
             svgs={"icon-check.svg": CHECK_SVG, "icon-search.svg": SEARCH_SVG, "icon-chip-x.svg": X_SVG, "icon-chevron-down.svg": CHEV_SVG})
