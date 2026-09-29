"""Sales Hub › Resource Library replica (Figma 1:2871 desktop 1440 / 1:1971 mobile 430) → pages/resource-library/html/.

Same method as build_resources.py: desktop = flow layout in u() with Figma x/widths and min-height-to-next-Figma-y;
mobile = the 430 frame's auto-layout. Copy from pages/_figma/file.json by node id. Images cropped from the 1x export
(token expired, #28) with the label chip + PDF badge that the export baked onto each product photo inpainted out.

Built as a static replica of the drawn state (2 filters active, 4 results). Filtering/sorting/search are real form
controls but inert here; the ACF step wires them to the m11_resource records.

    python tools/figma_html/build_resource_library.py
"""
import os
from html import escape

import cv2
import numpy as np

from chrome import D, FR, I, M, OS, ROOT, u
from chrome_portal import CARET_SVG, PORTAL_FOOTER_CSS, PORTAL_FOOTER_HTML, PORTAL_HEADER_CSS, PORTAL_HEADER_JS, portal_header
from replica_lib import Css, Page, compile_page, figma_linear, slug

P = Page("1:2871")
box, y, plain = P.box, P.y, P.plain
SLUG = "resource-library"
IMG = os.path.join(ROOT, "pages", SLUG, "figma", "images")
os.makedirs(IMG, exist_ok=True)
INK, BLUE, SKY = "#090909", "#0065B3", "#00B3F0"
css = Css()

# ---------------------------------------------------------------- Figma ids
BAND = dict(rect="1:2877", h1="1:2986", body="1:2987")
FILTERS = dict(panel="1:2963", type_text="1:2965", cat_text="1:2970", button="1:2977", button_text="1:2978",
               checked={"1:2966", "1:2971"}, type_boxes=["1:2966", "1:2967"], cat_boxes=["1:2971", "1:2972", "1:2973", "1:2974"])
TOOL = dict(panel="1:2879", input="1:2979", placeholder="1:2982", button="1:2983", button_text="1:2984", line="1:2884",
            count="1:2897", chips=[("1:2886", "1:2888"), ("1:2891", "1:2893")], clear="1:2894", sort="1:2880", sort_text="1:2882")
TILES = [  # tile rect, image rect, text, label rect, label text, pdf badge rect, pdf icon rect
    ("1:2899", "1:2900", "1:2901", "1:2904", "1:2905", "1:2912", "1:2913"),
    ("1:2915", "1:2916", "1:2917", "1:2926", "1:2927", "1:2928", "1:2929"),
    ("1:2931", "1:2932", "1:2933", "1:2942", "1:2943", "1:2944", "1:2945"),
    ("1:2947", "1:2948", "1:2949", "1:2959", "1:2960", "1:2961", "1:2962"),
]

# ---------------------------------------------------------------- images (crop + inpaint the overlays)
EXP = cv2.imread(os.path.join(ROOT, "pages/_figma/frames/export/Resource Library.png"))


def crop(nid):
    x, y_, w, h = (int(round(v)) for v in box(nid))
    return EXP[y_:y_ + h, x:x + w].copy(), (x, y_)


names = []
for t, im, tx, lab, _lt, badge, icon in TILES:
    img, (ox, oy) = crop(im)
    m = np.zeros(img.shape[:2], np.uint8)
    for r, pad in ((lab, 2), (badge, 6)):
        x, y_, w, h = box(r)
        cv2.rectangle(m, (int(x - ox - pad), int(y_ - oy - pad)), (int(x - ox + w + pad), int(y_ - oy + h + pad)), 255, -1)
    img = cv2.inpaint(img, m, 7, cv2.INPAINT_TELEA)
    name = "tile-" + slug(P.text(tx).split("\n")[0])[:50].strip("-") + ".jpg"
    cv2.imwrite(os.path.join(IMG, name), img, [cv2.IMWRITE_JPEG_QUALITY, 90])
    names.append(name)
pdf, _ = crop(TILES[0][6])
cv2.imwrite(os.path.join(IMG, "icon-pdf.png"), pdf)

# ================================================================ header / band
HEAD_HTML = portal_header("Resources")
bx, by, bw, bh = box(BAND["rect"])
h1x, h1y = box(BAND["h1"])[:2]
BAND_HTML = (f'<section class="rs rl-band" id="resource-library-intro"><div class="fx"><div class="rlb-box">'
             f'<h1 class="rlb-h1">{plain(BAND["h1"])}</h1><p class="rlb-body">{plain(BAND["body"])}</p></div></div></section>')
css.add(".rlb-box", f"background: {BLUE}; color: #FFFFFF;")
css.add(".rlb-h1", f"font-family: {FR}; font-weight: 400; text-transform: uppercase;")
css.add(".rlb-body", f"font-family: {OS}; font-weight: 400;")
css.add(".rl-band > .fx", f"padding-top: 0;", D)
css.add(".rlb-box", f"margin-left: {u(bx)}; width: {u(bw)}; height: {u(bh)}; border-radius: {u(15)}; padding: {u(h1y - by)} 0 0 {u(h1x - bx)}; box-sizing: border-box;", D)
css.add(".rlb-h1", f"font-size: {u(24)}; line-height: {u(32)}; min-height: {u(y(BAND['body']) - h1y)};", D)
css.add(".rlb-body", f"width: {u(box(BAND['body'])[2])}; font-size: {u(14)}; line-height: {u(22)};", D)
css.add(".rlb-box", "display: flex; flex-direction: column; gap: 20px; padding: 32px; border-radius: 12px;", M)
css.add(".rlb-h1", "font-size: 24px; line-height: 32px;", M)
css.add(".rlb-body", "font-size: 14px; line-height: 22px;", M)

# ================================================================ filters aside (1:2963)
fx_, fy_, fw_, fh_ = box(FILTERS["panel"])


def filter_group(text_id, boxes, name):
    lines = P.fig_lines(text_id)
    heading = "".join(t for t, _ in lines[0]).strip()
    rows = []
    for li, line in enumerate(l for l in lines[1:] if "".join(t for t, _ in l).strip()):
        raw = "".join(t for t, _ in line).replace(".", " ").split()
        count = raw[-1]
        label = " ".join(raw[:-1])
        bid = boxes[li]
        cid = f"f-{slug(label)}"
        chk = " checked" if bid in FILTERS["checked"] else ""
        rows.append(f'<li class="fl-row"><input class="fl-box" type="checkbox" id="{cid}" name="{name}" value="{slug(label)}"{chk}>'
                    f'<label class="fl-label" for="{cid}">{escape(label)}</label><span class="fl-count">{count}</span></li>')
    return f'<fieldset class="fl-group"><legend class="fl-h">{escape(heading)}</legend><ul class="fl-list">{"".join(rows)}</ul></fieldset>'


type_top, cat_top = y(FILTERS["type_text"]), y(FILTERS["cat_text"])
btn_x, btn_y, btn_w, btn_h = box(FILTERS["button"])
row0 = y(FILTERS["type_boxes"][0]) - 7  # 20px box centred in a 34px row
cat_row0 = y(FILTERS["cat_boxes"][0]) - 7
ASIDE = (f'<aside class="rl-filters" aria-label="Filter resources"><form class="fl-form" action="#resource-results">'
         + filter_group(FILTERS["type_text"], FILTERS["type_boxes"], "resource_type")
         + filter_group(FILTERS["cat_text"], FILTERS["cat_boxes"], "product_category")
         + f'<button class="fl-clear" type="reset">{plain(FILTERS["button_text"])}</button></form></aside>')
CHECK_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="#000000" stroke-width="2" '
             'stroke-linecap="round"><path d="M4 12l4 4"/><path d="M7 16l10-11.5"/></svg>')
css.add(".rl-filters", "background: rgba(196, 196, 196, 0.1); box-shadow: inset 0 0 0 0.5px rgba(0, 0, 0, 0.35); border-radius: 12px; box-sizing: border-box;")  # Figma INSIDE stroke
css.add(".fl-group", "margin: 0; padding: 0; border: 0; min-width: 0;")
css.add(".fl-h", f"padding: 0; font-family: {OS}; font-weight: 700; color: {INK}; text-transform: uppercase;")
css.add(".fl-list", "margin: 0; padding: 0; list-style: none;")
css.add(".fl-row", "display: grid; grid-template-columns: 20px 1fr auto; align-items: center; column-gap: 8px;")
css.add(".fl-box", f"appearance: none; -webkit-appearance: none; width: 20px; height: 20px; margin: 0; background: #FFFFFF no-repeat center / 20px 20px; border: 1px solid rgba(0, 0, 0, 0.5); border-radius: 0; cursor: pointer;")
css.add(".fl-box:checked", f'background-image: url("../{I}/icon-check.svg");')
css.add(".fl-box:focus-visible", f"outline: 2px solid {SKY}; outline-offset: 2px;")
css.add(".fl-label, .fl-count", f"font-family: {OS}; font-weight: 400; color: {INK}; cursor: pointer;")
css.add(".fl-clear", f"display: block; box-sizing: border-box; background: #FFFFFF; border: 2px solid {SKY}; border-radius: 5px; font-family: {FR}; font-weight: 400; color: {BLUE}; cursor: pointer;")
css.add(".rl-filters", f"width: {u(fw_)}; min-height: {u(fh_)}; padding: {u(type_top - fy_)} {u(21)} {u(fy_ + fh_ - btn_y - btn_h)} {u(btn_x - fx_)};", D)
css.add(".fl-h", f"font-size: {u(14)}; line-height: {u(22)}; min-height: {u(row0 - type_top)};", D)
css.add(".fl-group + .fl-group", f"margin-top: {u(cat_top - row0 - 2 * 34)};", D)
css.add(".fl-group + .fl-group .fl-h", f"min-height: {u(cat_row0 - cat_top)};", D)
css.add(".fl-list", f"width: {u(255)};", D)
css.add(".fl-row", f"height: {u(34)};", D)
css.add(".fl-label, .fl-count", f"font-size: {u(14)}; line-height: {u(22)};", D)
css.add(".fl-clear", f"margin-top: {u(btn_y - cat_row0 - 4 * 34)}; width: {u(btn_w)}; height: {u(btn_h)}; font-size: {u(16)};", D)
css.add(".rl-filters", "padding: 29px 27px 23px;", M)
css.add(".fl-h", "font-size: 14px; line-height: 22px; min-height: 24px;", M)
css.add(".fl-group + .fl-group", "margin-top: 27px;", M)
css.add(".fl-list", "width: 253px;", M)
css.add(".fl-row", "height: 34px;", M)
css.add(".fl-label, .fl-count", "font-size: 14px; line-height: 22px;", M)
css.add(".fl-clear", "margin-top: 32px; width: 100%; height: 50px; font-size: 16px;", M)

# ================================================================ toolbar (1:2879)
tx0, ty0, tw0, th0 = box(TOOL["panel"])
ix, iy, iw, ih = box(TOOL["input"])
sbx, sby, sbw, sbh = box(TOOL["button"])
lx, ly, lw = box(TOOL["line"])[:3]
cx, cy = box(TOOL["count"])[:2]
chip_y = y(TOOL["chips"][0][0])
sx, sy_, sw, sh = box(TOOL["sort"])
count_html = P.inline(P.fig_lines(TOOL["count"])[0]).replace(">3 </strong>", ">4 </strong>")  # 4 results are drawn (issues-log)
chips = "".join(f'<button class="chip" type="button" aria-label="Remove filter: {plain(t)}">{plain(t)}<span class="chip-x" aria-hidden="true"></span></button>'
                for _, t in TOOL["chips"])
TOOLBAR = (f'<div class="rl-tools"><form class="rl-search" role="search" action="#resource-results">'
           f'<label class="visually-hidden" for="rl-q">Search resources</label>'
           f'<input class="rl-q" id="rl-q" type="search" name="q" placeholder="{plain(TOOL["placeholder"])}">'
           f'<button class="rl-go" type="submit">{plain(TOOL["button_text"])}</button></form><hr class="rl-line">'
           f'<div class="rl-meta"><p class="rl-count" aria-live="polite">{count_html}</p><div class="rl-active">{chips}'
           f'<a class="rl-clear-all" href="#resource-results">{plain(TOOL["clear"])}</a></div>'
           f'<label class="visually-hidden" for="rl-sort">Sort</label><select class="rl-sort selectish" id="rl-sort" name="sort">'
           f'<option>{plain(TOOL["sort_text"])}</option><option>Sort: Z-A</option><option>Sort: Newest</option></select></div></div>')
SEARCH_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 25 25" fill="none" stroke="#ADADAD" stroke-width="2">'
              '<circle cx="10.5" cy="10.5" r="9.5"/><path d="M17.4 17.4l6 6" stroke-linecap="round"/></svg>')
X_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="#000000" stroke-width="2">'
         '<path d="M4.5 4.5l9 9M13.5 4.5l-9 9"/></svg>')
css.add(".rl-tools", f"background: {figma_linear(P.node(TOOL['panel'])['fills'][0], tw0, th0)}; box-shadow: inset 0 0 0 0.5px rgba(0, 0, 0, 0.4); border-radius: 12px; box-sizing: border-box;")
css.add(".rl-search", "display: flex;")
css.add(".rl-q", f"flex: 1; min-width: 0; box-sizing: border-box; background: #FFFFFF url(\"../{I}/icon-search.svg\") no-repeat; border: 1px solid rgba(0, 0, 0, 0.35); font-family: {OS}; font-weight: 400; color: #000000;")
css.add(".rl-q::placeholder", "color: rgba(0, 0, 0, 0.35); opacity: 1;")
css.add(".rl-go", f"border: 0; border-radius: 5px; background: {SKY}; color: #FFFFFF; font-family: {FR}; font-weight: 400; cursor: pointer;")
css.add(".rl-line", "margin: 0; border: 0; border-top: 1px solid rgba(0, 0, 0, 0.25);")
css.add(".rl-count", f"margin: 0; font-family: {OS}; color: {INK};")
css.add(".rl-count strong", "font-weight: 700;")
css.add(".rl-count span", "font-weight: 300;")
css.add(".rl-active", "display: flex; align-items: center;")
css.add(".chip", f"position: relative; display: flex; align-items: center; box-sizing: border-box; height: 28px; padding: 0 0 0 9px; background: rgba(119, 220, 255, 0.15); border: 0.5px solid rgba(0, 0, 0, 0.35); border-radius: 5px; font-family: {OS}; font-weight: 700; font-size: 11px; line-height: 22px; color: {INK}; text-align: left; cursor: pointer;")
css.add(".chip-x", f"position: absolute; right: 5px; top: 5px; width: 18px; height: 18px; box-sizing: border-box; background: #FFFFFF url(\"../{I}/icon-chip-x.svg\") no-repeat center / 18px 18px; border: 0.5px solid rgba(0, 0, 0, 0.35); border-radius: 3px;")
css.add(".rl-clear-all", f"font-family: {OS}; font-weight: 700; font-size: 11px; line-height: 22px; color: {BLUE};")
css.add(".rl-sort", "appearance: none; -webkit-appearance: none; cursor: pointer;")
css.add(".rl-tools", f"padding: {u(iy - ty0)} {u(tx0 + tw0 - sbx - sbw)} {u(ty0 + th0 - chip_y - 30)} {u(ix - tx0)};", D)
css.add(".rl-search", f"gap: {u(sbx - ix - iw)};", D)
css.add(".rl-q", f"height: {u(ih)}; padding-left: {u(57)}; border-radius: {u(5)}; background-position: {u(17)} {u(9)}; background-size: {u(25)} {u(25)}; font-size: {u(15)}; line-height: {u(30)};", D)
css.add(".rl-go", f"width: {u(sbw)}; height: {u(sbh)}; font-size: {u(16)};", D)
css.add(".rl-line", f"margin: {u(ly - iy - ih)} 0 0 {u(lx - ix)}; width: {u(lw)};", D)
css.add(".rl-meta", f"display: grid; grid-template-columns: 1fr auto; align-items: start; padding: {u(cy - ly - 1)} 0 0 {u(cx - ix)};", D)
css.add(".rl-count", f"grid-column: 1 / -1; font-size: {u(20)}; line-height: {u(22)}; min-height: {u(chip_y - cy)};", D)
css.add(".rl-active", f"margin-left: {u(box(TOOL['chips'][0][0])[0] - cx)}; gap: {u(12)};", D)
css.add(".chip", f"width: {u(187)};", D)
css.add(".rl-clear-all", f"margin-left: {u(18 - 12)};", D)
css.add(".rl-sort", f"width: {u(sw)}; height: {u(sh)}; padding-left: {u(12)}; {''}font-size: {u(13)}; line-height: {u(17.7)};", D)
css.add(".rl-tools", "display: flex; flex-direction: column; gap: 24px; padding: 25px;", M)
css.add(".rl-search", "flex-direction: column; align-items: flex-end; gap: 21px;", M)
css.add(".rl-q", "align-self: stretch; flex: none; height: 40px; padding-left: 29px; border-radius: 6px; background-position: 12px 12px; background-size: 16px 16px; font-size: 12px; line-height: 16.34px;", M)
css.add(".rl-go", "padding: 6px 20px; font-size: 16px; line-height: 21.28px;", M)
css.add(".rl-meta", "display: flex; flex-direction: column; gap: 14px;", M)
css.add(".rl-count", "font-size: 18px; line-height: 22px;", M)
css.add(".rl-active", "display: grid; grid-template-columns: 187px 1fr; gap: 9px 9px; align-items: end;", M)
css.add(".rl-clear-all", "grid-column: 2; grid-row: 2; justify-self: end;", M)
css.add(".rl-active .chip", "grid-column: 1; width: 187px;", M)
css.add(".rl-sort", "display: none;", M)

# ================================================================ result tiles
tiles = []
for (t, im, tx, lab, lt, badge, icon), name in zip(TILES, names):
    lines = P.fig_lines(tx)
    title = "".join(s for s, _ in lines[0]).strip()
    sub = "".join(s for s, _ in lines[1]).strip() if len(lines) > 1 else ""
    s = slug(title)
    tiles.append(f'<li class="tile"><div class="tile-media"><img src="{I}/{name}" alt="{escape(title)}" width="307" height="195" loading="lazy">'
                 f'<span class="tile-tag">{plain(lt)}</span><span class="tile-pdf"><img src="{I}/icon-pdf.png" alt="PDF" width="36" height="50"></span></div>'
                 f'<div class="tile-text"><h2 class="tile-title">{escape(title)}</h2><p class="tile-sub">{escape(sub)}</p></div>'
                 f'<a class="tile-dl" href="#download-{s}" aria-label="Download: {escape(title)}"><img src="{I}/icon-download-circle.svg" alt="" width="30" height="30">Download</a></li>')
t0 = box(TILES[0][0])
t1 = box(TILES[1][0])
t3 = box(TILES[3][0])
MAIN_HTML = (f'<section class="rs rl-main" id="resource-results"><div class="fx"><div class="rl-layout">{ASIDE}<div class="rl-results">{TOOLBAR}'
             f'<ul class="tiles">{"".join(tiles)}</ul></div></div><hr class="rule rl-end m-only"></div></section>')
DL_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 30 30" fill="none">'
          '<circle cx="15" cy="15" r="14" fill="#FFFFFF" stroke="#0065B3" stroke-width="2"/>'
          '<g stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15.3 7.7v10"/><path d="M11.8 14.5l3.5 3.5 3.5-3.5"/><path d="M9.3 19.7v2h11.3v-2"/></g></svg>')
css.add(".tiles", "margin: 0; padding: 0; list-style: none;")
css.add(".tile", f"position: relative; box-sizing: border-box; overflow: hidden; background: {figma_linear(P.node(TILES[0][0])['fills'][0], 307, 320)}, #FFFFFF; border: 0.5px solid rgba(0, 0, 0, 0.35);")
css.add(".tile-media", "position: relative; background: #FFFFFF; border-bottom: 0.5px solid rgba(0, 0, 0, 0.35);")
css.add(".tile-media > img", "width: 100%; height: 100%; object-fit: cover;")
css.add(".tile-tag", f"position: absolute; box-sizing: border-box; height: 28px; padding: 3px 9px; background: rgba(231, 249, 255, 0.9); border: 0.5px solid rgba(0, 0, 0, 0.35); border-radius: 5px; white-space: nowrap; font-family: {OS}; font-weight: 400; font-size: 11px; line-height: 22px; color: {INK};")
css.add(".tile-pdf", "position: absolute; box-sizing: border-box; width: 69px; height: 69px; padding: 10px 0 0 17px; background: #FDFFD0; border: 1px solid rgba(0, 0, 0, 0.15); border-radius: 10px; box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.1);")
css.add(".tile-title", f"margin: 0; font-family: {OS}; font-weight: 700; font-size: 14px; line-height: 22px; color: {INK};")
css.add(".tile-sub", f"margin: 0; font-family: {OS}; font-weight: 300; font-size: 14px; line-height: 20px; color: {INK};")
css.add(".tile-dl", f"display: inline-flex; align-items: center; gap: 8px; font-family: {OS}; font-weight: 700; font-size: 14px; line-height: 22px; color: {BLUE};")
css.add(".rl-main > .fx", f"padding: 0 0 {u(1205 - t3[1] - t3[3])};", D)
css.add(".rl-layout", f"display: grid; grid-template-columns: {u(fw_)} {u(tw0)}; column-gap: {u(tx0 - fx_ - fw_)}; align-items: start; margin: {u(fy_ - by - bh)} 0 0 {u(fx_)};", D)
css.add(".tiles", f"display: grid; grid-template-columns: repeat(3, {u(t0[2])}); gap: {u(t3[1] - t0[1] - t0[3])} {u(t1[0] - t0[0] - t0[2])}; margin-top: {u(t0[1] - ty0 - th0)};", D)
css.add(".tile", f"height: {u(t0[3])}; border-radius: {u(12)};", D)
css.add(".tile-media", f"height: {u(195)}; border-radius: {u(12)} {u(12)} 0 0;", D)
css.add(".tile-tag", f"left: {u(13)}; top: {u(153)}; width: {u(134)};", D)
css.add(".tile-pdf", f"left: {u(223)}; top: {u(112)};", D)
css.add(".tile-text", f"margin: {u(11)} 0 0 {u(13)}; min-height: {u(72)};", D)
css.add(".tile-dl", f"margin-left: {u(13)};", D)
css.add(".rl-layout, .rl-results, .tiles", "display: flex; flex-direction: column; gap: 36px;", M)
css.add(".rl-main > .fx", "padding-top: 0; padding-bottom: 0;", M)
css.add(".rl-end", "margin-top: 8px;", M)
css.add(".tile", "height: 320px; border-radius: 12px;", M)
css.add(".tile-media", "height: 195px; border-radius: 12px 12px 0 0;", M)
css.add(".tile-tag", "left: 16.5px; top: 153px; width: 170px;", M)
css.add(".tile-pdf", "right: 16px; top: 112px;", M)
css.add(".tile-text", "margin: 11px 0 0 16.5px; min-height: 72px;", M)
css.add(".tile-dl", "margin-left: 16.5px;", M)
css.add(".rl-band > .fx, .rl-main > .fx", "max-width: 640px; margin: 0 auto; box-sizing: border-box;", M)

# ================================================================ blueprint + compile
NOTE = ("2026-09-28 Resource Library replica (Flow A, HTML first). Figma 1:2871 desktop (flow, u(), min-height-to-next-Figma-y) and 1:1971 mobile "
        "auto-layout. Generated by tools/figma_html/build_resource_library.py; copy from pages/_figma/file.json by node id.")
SECTIONS = [
    {"id": "site-header", "landmark": "header", "escape_hatch": True, "html": HEAD_HTML, "css": PORTAL_HEADER_CSS, "js": PORTAL_HEADER_JS},
    {"id": "resource-library-intro", "escape_hatch": True, "heading_level": 1, "html": BAND_HTML, "css": css.render()},
    {"id": "resource-results", "escape_hatch": True, "html": MAIN_HTML, "css": ""},
    {"id": "site-footer", "landmark": "footer", "escape_hatch": True, "html": PORTAL_FOOTER_HTML, "css": PORTAL_FOOTER_CSS},
]
for s in SECTIONS:
    s["notes"] = [NOTE]
bp = {"page": SLUG,
      "meta": {"title": "Resource Library | Sales Hub | Mizuho America",
               "description": "Sales Hub resource library: downloadable brochures, spec sheets and videos for Mizuho America sales representatives."},
      "css_workflow": "scss", "font_source": "google",
      "notes_for_developer": ["Portal chrome from tools/figma_html/chrome_portal.py (shared by the Sales Hub pages).",
                              "Figma shows '3 resources' above 4 results; the count shows 4 (issues-log). Figma's mobile frame uses the public header; followed as drawn."],
      "sections": SECTIONS}
compile_page(SLUG, bp, extra_images=("logo-mizuho-header-srgb.png", "logo-mizuho-footer-reversed.png"),
             svgs={"icon-select-caret.svg": CARET_SVG, "icon-check.svg": CHECK_SVG, "icon-search.svg": SEARCH_SVG,
                   "icon-chip-x.svg": X_SVG, "icon-download-circle.svg": DL_SVG})
