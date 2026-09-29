"""Resources page replica (Figma 1:2490 desktop 1440 / 1:559 mobile 430) → pages/resources/blueprint.json → DevCommand's
real compiler (run_devcommand_compiler.py) → pages/resources/html/.

Method (the one that worked on Home and About):
  * Desktop >=1024: FLOW layout. Every x/width is the Figma value in u() (= min(1px, 100cqw/1440)); every vertical
    distance is a min-height "to the next element's Figma top", so blocks land on their Figma y even though the page
    flows (and still grow instead of overlapping if an editor writes more text).
  * Mobile <=1023: the Figma 430 frame's auto-layout (padding 44/20, gap 36; testimonials a centred 304px column;
    brochure grids = the desktop card scaled 0.85, as Figma draws them).
  * Every string, colour run and box comes from pages/_figma/file.json by node id (resources_data.py) - nothing retyped.
  * Header/footer are Home's (chrome.py), with "Clinical Resources" marked current as in this frame.

    python tools/figma_html/build_resources.py            # blueprint + compile + copy assets + validate
"""
import json
import os
import shutil
import subprocess
import sys
from collections import OrderedDict
from html import escape

from replica_lib import Css, Page
from chrome import (D, FOOT_CSS, FOOT_HTML, FR, HEADER_CSS, HEADER_HTML, HEADER_JS, I, M, OS, ROOT, SHARED, link_pages, u)
from resources_data import (BOTTOM, BRO_GROUPS, BRO_H2, FACTS, FACTS_H2, INTRO, TESTI_H2, TESTI_LINES, TESTI_ROWS, box, node,
                            runs, slug, text)

PAGE = os.path.join(ROOT, "pages", "resources")
PLUGIN = r"C:\Users\Vansh Patel\.claude\plugins\cache\dev-command\dev-command\fbe821068e44"
BLUE, SKY, INK = "#0065B3", "#00B3F0", "#090909"


# ---------------------------------------------------------------- CSS collector (merges identical bodies: validator rule)
P = Page("1:2490")
y, fig_lines, lh_of, inline, para, plain, br = P.y, P.fig_lines, P.lh_of, P.inline, P.para, P.plain, P.br


css = Css()
SHIFTS = P.shifts
W = set()  # utility width classes used on desktop


def wcls(nid):
    w = round(box(nid)[2])
    W.add(w)
    return f"w{w}"


PLAY = f'<img class="play" src="{I}/icon-play-circle.svg" alt="" width="53" height="53">'
BADGE = f'<img class="badge" src="{I}/icon-download-badge.svg" alt="" width="45" height="45">'


def img_name(prefix, label):
    return f"{prefix}-{slug(label)[:60].strip('-')}.jpg"


# ================================================================ header (Home's, with the current page marked)
HEAD_HTML = HEADER_HTML.replace('<a href="#clinical-resources">', '<a class="is-current" aria-current="page" href="#clinical-resources">')
assert HEAD_HTML != HEADER_HTML
css.add(".site-head__nav a.is-current", f"color: {BLUE};")

# ================================================================ intro (1:2841)  desktop y 161..758 · mobile 1:570
i = INTRO
card_x, card_y, card_w, card_h = box(i["card"])
h1x, h1y = box(i["h1"])[:2]
h2x, h2y = box(i["h2"])[:2]
vx, vy, vw, vh = box(i["video"])
qx, qy, qw = box(i["quote"])[:3]
b1x, b1y, b1w, b1h = box(i["btn1_box"])
b2x, b2y, b2w, b2h = box(i["btn2_box"])
INTRO_HTML = (
    f'<section class="rs ri" id="resources-intro"><div class="fx">'
    f'<h1 class="ri-h1">{plain(i["h1"])}</h1>'
    f'<div class="ri-card"><div class="ri-copy"><h2 class="ri-h2">{plain(i["h2"])}</h2><p class="ri-body">{plain(i["body"])}</p>'
    f'<div class="ri-btns"><a class="ri-btn ri-btn--solid" href="#testimonials">{plain(i["btn1"])}</a>'
    f'<a class="ri-btn ri-btn--line" href="#brochures">{br(i["btn2"])}</a></div></div>'
    f'<figure class="ri-media"><a class="vid ri-vid" href="#video-intro-lawton" aria-label="Play video: Michael T. Lawton, MD">'
    f'<img src="{I}/video-intro-lawton.jpg" alt="Michael T. Lawton, MD" width="{vw:g}" height="{vh:g}">{PLAY}</a>'
    f'<blockquote class="ri-quote"><p>{plain(i["quote"])}</p></blockquote><figcaption class="ri-cite">{plain(i["cite"])}</figcaption></figure>'
    f'</div></div></section>')
css.add(".ri-h1", f"font-family: {FR}; font-weight: 400; color: {BLUE}; text-transform: uppercase;")
css.add(".ri-card", "background: #F6F6F6; border-radius: 20px;")  # Figma #C4C4C4 @ 15% on white = #F6F6F6
css.add(".ri-h2", f"font-family: {FR}; font-weight: 400; color: #000000; text-transform: uppercase;")
css.add(".ri-body", f"font-family: {OS}; font-weight: 400; color: #000000;")
css.add(".ri-btn", f"display: flex; align-items: center; justify-content: center; box-sizing: border-box; text-align: center; font-family: {FR}; font-weight: 400;")
css.add(".ri-btn--solid", "color: #FFFFFF;")
css.add(".ri-btn--line", f"color: {SKY};")
css.add(".ri-quote p, .ri-cite", f"font-family: {OS}; color: #000000; text-align: center;")
css.add(".ri-quote p", "font-weight: 300; font-style: italic;")
css.add(".ri-cite", "font-weight: 400;")
# desktop
css.add(".ri > .fx", f"padding: {u(h1y - 161)} 0 {u(758 - card_y - card_h)};", D)
css.add(".ri-h1", f"margin-left: {u(h1x)}; font-size: {u(45)}; line-height: {u(70)}; min-height: {u(card_y - h1y)};", D)
css.add(".ri-card", f"display: flex; align-items: flex-start; margin-left: {u(card_x)}; width: {u(card_w)}; height: {u(card_h)};", D)
css.add(".ri-copy", f"margin: {u(h2y - card_y)} 0 0 {u(h2x - card_x)}; width: {u(box(i['h2'])[2])};", D)
css.add(".ri-h2", f"font-size: {u(38)}; line-height: {u(32)}; min-height: {u(y(i['body']) - h2y)};", D)
css.add(".ri-body", f"width: {u(box(i['body'])[2])}; font-size: {u(16)}; line-height: {u(22)}; min-height: {u(b1y - y(i['body']))};", D)
css.add(".ri-btns", f"display: flex; gap: {u(b2x - b1x - b1w)};", D)
css.add(".ri-btn", f"height: {u(b1h)}; border-radius: {u(10)}; font-size: {u(20)};", D)
css.add(".ri-btn--solid", f"width: {u(b1w)}; background: #77DCFF; line-height: {u(22)};", D)
css.add(".ri-btn--line", f"width: {u(b2w)}; background: #FFFFFF; border: 1px solid #77DCFF; line-height: {u(26)};", D)
css.add(".ri-media", f"margin: {u(vy - card_y)} 0 0 {u(qx - h2x - box(i['h2'])[2])}; width: {u(qw)};", D)
css.add(".ri-vid", f"margin-left: {u(vx - qx)}; width: {u(vw)}; height: {u(vh)}; border-radius: {u(12)};", D)
css.add(".ri-quote", f"margin-top: {u(qy - vy - vh)};", D)
css.add(".ri-quote p, .ri-cite", f"font-size: {u(14)}; line-height: {u(22)};", D)
css.add(".ri-cite", f"margin-top: {u(y(i['cite']) - qy - 66)};", D)
# mobile (1:570 - card 1:575 p32 gap32; buttons 1:580/1:582; media 1:584 gap12, quote 346 wide = 10px past the card padding)
css.add(".ri-h1", "font-size: 36px; line-height: 41.4px;", M)
css.add(".ri-card", "display: flex; flex-direction: column; gap: 32px; padding: 32px;", M)
css.add(".ri-h2", "font-size: 32px; line-height: 32px; margin-bottom: 32px;", M)
css.add(".ri-body", "font-size: 14px; line-height: 22px; margin-bottom: 32px;", M)
css.add(".ri-btns", "display: flex; flex-direction: column; gap: 18px;", M)
css.add(".ri-btn", "height: 88px; border-radius: 5px; font-size: 18px; line-height: 23.94px; padding: 0 35px;", M)
css.add(".ri-btn--solid", "background: #73D4F6;", M)
css.add(".ri-btn--line", f"border: 2px solid {SKY};", M)
css.add(".ri-media", "display: flex; flex-direction: column; align-items: center; margin: 0 -10px;", M)
css.add(".ri-vid", "width: 335px; max-width: 100%; aspect-ratio: 335 / 219; border-radius: 12px;", M)
css.add(".ri-quote", "margin-top: 12px;", M)
css.add(".ri-quote p, .ri-cite", "font-size: 14px; line-height: 22px;", M)
css.add(".ri-cite", "margin-top: 3px;", M)

# ---------------------------------------------------------------- shared bits: video tile, rule, section heading
css.add(".vid", "position: relative; display: block; overflow: hidden; background: #262626;")
css.add(".vid > img:first-child", "width: 100%; height: 100%; object-fit: cover;")
css.add(".vid .play", "position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);")
css.add(".rule", f"margin: 0; border: 0; border-top: 1px solid {SKY};")
css.add(".sec-h2", f"font-family: {FR}; font-weight: 400; color: {BLUE}; text-transform: uppercase;")
css.add(".more", f"color: {BLUE}; font-weight: 700;")
css.add(".vid .play", f"width: {u(53)}; height: {u(53)};", D)
css.add(".sec-h2", f"font-size: {u(34)}; line-height: {u(50)};", D)
css.add(".vid .play", "width: 53px; height: 53px;", M)

# ================================================================ testimonials (1:2800)  desktop y 758..2452 · mobile 1:592
COLS = [85, 404, 724, 1044]
GAP4 = (1044 - 85 - 3 * 303) / 3
top_line = TESTI_LINES[0]
rows_html = []
row_y = []  # (bio_top, vid_top, cap_top, end)
ends = [y(TESTI_LINES[1]), y(TESTI_LINES[2]), y(FACTS_H2)]
for r, row in enumerate(TESTI_ROWS):
    bio_top = min(y(ex["bio"]) for ex in row)
    vid_top = min(y(v[0]) for ex in row for v in ex["videos"])
    caps = [y(v[1]) for ex in row for v in ex["videos"] if v[1]] + [y(ex["caption"]) for ex in row if ex.get("caption")]
    row_y.append((bio_top, vid_top, min(caps), ends[r]))
    exs = []
    for ex in row:
        n = len(ex["videos"])
        vids = []
        for vi, (rect, cap) in enumerate(ex["videos"]):
            label = text(cap).split("\n")[0] if cap else text(ex["caption"]).split("\n")[0] + f"-{vi + 1}"
            if label.lower().startswith("extended"):
                label = text(ex["videos"][0][1]).split("\n")[0] + " extended"
            name = img_name("video", label.replace("Topic:", ""))
            alt = label.replace("Topic: ", "").replace("-1", "").replace("-2", "")
            vw_, vh_ = box(rect)[2:]
            cap_html = para(cap, f"tx-cap {wcls(cap)}", link_slug="read-more-" + slug(label)) if cap else ""
            vids.append(f'<li class="rt-vid"><a class="vid rt-thumb" href="#{name[:-4]}" aria-label="Play video: {escape(alt)}">'
                        f'<img src="{I}/{name}" alt="{escape(alt)}" width="{vw_:g}" height="{vh_:g}" loading="lazy">{PLAY}</a>{cap_html}</li>')
        shared = para(ex["caption"], f"tx-cap tx-cap--shared {wcls(ex['caption'])}") if ex.get("caption") else ""
        exs.append(f'<article class="rt-ex rt-ex--{n}{" rt-ex--shared" if shared else ""}">'
                   + para(ex["bio"], f"tx-bio {wcls(ex['bio'])}") + '<ul class="rt-vids">' + "".join(vids) + "</ul>" + shared + "</article>")
    rows_html.append(f'<div class="rt-row rt-row--{r + 1}">' + "".join(exs) + "</div>")

TESTI_HTML = ('<section class="rs rt" id="testimonials"><div class="fx"><hr class="rule rule--top">'
              f'<h2 class="sec-h2 rt-h2">{plain(TESTI_H2)}</h2>'
              + '<hr class="rule">'.join(rows_html) + "</div></section>")
css.add(".tx-bio, .tx-cap", f"font-family: {OS}; font-weight: 300; color: #000000;")
css.add(".tx-cap .ln:first-child", f"color: {INK};")
css.add(".tx-bio strong, .tx-cap strong", "font-weight: 700;")
for lh in (20, 22, 24, 26, 28, 30):
    css.add(f".lh{lh}", f"line-height: {lh}px;", M)
    css.add(f".lh{lh}", f"line-height: {u(lh)};", D)
for s in (12, 14, 15, 18):
    css.add(f".tx-bio .s{s}, .tx-cap .s{s}", f"font-size: {s}px;", M)
    css.add(f".tx-bio .s{s}, .tx-cap .s{s}", f"font-size: {u(s)};", D)
css.add(".rt > .fx", f"padding: 0 0 0 {u(85)};", D)
css.add(".rt-h2", f"margin: {u(y(TESTI_H2) - y(top_line) - 1)} 0 {u(row_y[0][0] - y(TESTI_H2) - 50)};", D)
css.add(".rt .rule", f"width: {u(1263)};", D)
css.add(".rt-row", f"display: grid; grid-template-columns: repeat(4, {u(303)}); column-gap: {u(GAP4)};", D)
for r, (bt, vt, ct, end) in enumerate(row_y):
    css.add(f".rt-row--{r + 1}", f"grid-template-rows: {u(vt - bt)} {u(236)} minmax({u(end - vt - 236)}, auto);", D)
    css.add(f".rt-row--{r + 1} .tx-cap", f"margin-top: {u(ct - vt - 236)};", D)
for r in range(2):  # gap under each row rule = next row's bio top - rule y - 1
    css.add(f".rt-row--{r + 1} + .rule", f"margin-bottom: {u(row_y[r + 1][0] - ends[r] - 1)};", D)
for n in (1, 2):
    css.add(f".rt-ex--{n}", f"grid-column: span {n};", D)
css.add(".rt-ex", "display: grid; grid-row: 1 / span 3; grid-template-columns: subgrid; grid-template-rows: subgrid;", D)
css.add(".rt-vids, .rt-vid", "display: contents;", D)
css.add(".tx-bio", f"grid-column: 1 / -1; grid-row: 1; margin-left: {u(4)};", D)
css.add(".rt-thumb", f"grid-row: 2; width: {u(303)}; height: {u(236)}; border-radius: {u(15)};", D)
css.add(".rt .tx-cap", f"grid-row: 3; margin-left: {u(4)};", D)
css.add(".tx-cap--shared", "grid-column: 1 / -1;", D)
# mobile: one centred 304px column (1:592 CEN), rules full width, gap 36 (bio→videos), 14 inside a video frame
css.add(".rt > .fx", "padding-top: 0; align-items: center;", M)
css.add(".rt .rule", "align-self: stretch;", M)
css.add(".rt-h2", "margin-top: 8px;", M)
css.add(".sec-h2", "font-size: 32px; line-height: 36.8px;", M)
css.add(".rt-h2, .rt-row", "width: 304px; max-width: 100%;", M)
css.add(".rt-row, .rt-ex, .rt-vids", "display: flex; flex-direction: column; gap: 36px;", M)
css.add(".rt-vid", "display: flex; flex-direction: column; gap: 12px;", M)
css.add(".rt-thumb", "width: 100%; aspect-ratio: 303 / 236; border-radius: 15px;", M)
css.add(".rt-ex--shared .rt-vids", "gap: 14px;", M)
css.add(".tx-cap--shared", "margin-top: -22px;", M)

# ================================================================ fast facts (1:2785 + 1:2795)  desktop y 2452..3002 · mobile 1:641
f_top = y(FACTS_H2)
t_top = min(y(t) for t, _, _ in FACTS)
fr_top = min(y(fr) for _, fr, _ in FACTS)
items = []
for title, frame, cap in FACTS:
    fx_, fy_, fw_, fh_ = box(frame)
    name = img_name("video-fact", text(title).split("\n")[0])
    items.append(f'<article class="ff-item"><h3 class="ff-title {wcls(title)}">{br(title)}</h3>'
                 f'<a class="vid ff-thumb" href="#{name[:-4]}" aria-label="Play video: {plain(title)}"><img src="{I}/{name}" alt="{plain(title)}" '
                 f'width="{fw_:g}" height="{fh_:g}" loading="lazy">{PLAY}</a><p class="ff-cap {wcls(cap)}">{plain(cap)}</p></article>')
FACTS_HTML = (f'<section class="rs ff" id="fast-facts"><div class="fx"><h2 class="sec-h2 ff-h2">{plain(FACTS_H2)}</h2>'
              '<div class="ff-grid">' + "".join(items) + "</div></div></section>")
css.add(".ff-title", f"margin: 0; font-family: {OS}; font-weight: 700; color: #000000;")
css.add(".ff-cap", f"margin: 0; font-family: {OS}; font-weight: 300; color: {INK};")
css.add(".ff > .fx", f"padding-left: {u(box(FACTS_H2)[0])};", D)
css.add(".ff-h2", f"min-height: {u(t_top - f_top)};", D)
css.add(".ff-grid", f"display: grid; grid-template-columns: repeat(3, {u(303)}); column-gap: {u(20)}; margin-left: {u(box(FACTS[0][1])[0] - box(FACTS_H2)[0])}; "
        f"min-height: {u(y('1:2784') - t_top)};", D)
css.add(".ff-title", f"min-height: {u(fr_top - t_top)}; margin-left: {u(9)}; font-size: {u(15)}; line-height: {u(25)};", D)
css.add(".ff-thumb", f"width: {u(303)}; height: {u(236)}; border-radius: {u(15)};", D)
css.add(".ff-cap", f"margin: {u(16)} 0 0 {u(9)}; font-size: {u(12)}; line-height: {u(22)};", D)
css.add(".ff-item:first-child .ff-cap", f"line-height: {u(20)};", D)
css.add(".ff-item:last-child .ff-cap", f"margin-top: {u(21)};", D)
css.add(".ff > .fx", "align-items: center;", M)
css.add(".ff-h2, .ff-grid", "width: 304px; max-width: 100%;", M)
css.add(".ff-grid", "display: flex; flex-direction: column; gap: 36px;", M)
css.add(".ff-item", "display: flex; flex-direction: column; gap: 16px;", M)
css.add(".ff-title", "margin-bottom: 20px; font-size: 15px; line-height: 30px;", M)
css.add(".ff-thumb", "width: 100%; aspect-ratio: 303 / 236; border-radius: 15px;", M)
css.add(".ff-cap", "font-size: 12px; line-height: 22px;", M)
css.add(".ff-item:first-child .ff-cap", "line-height: 20px;", M)
css.add(".ff-item:last-child .ff-cap", "margin-top: 5px;", M)

# ================================================================ brochures (1:2512)  desktop y 3002..8731 · mobile 1:659…1:921
COL0, PITCH = 95, (1110 - 95) / 4
ROW_H = 245  # covers are bottom-aligned in a 245px row (236px crops sit 9px lower)
gcss_rows = []


def cover_card(rect, cap, g, heading_for_name=None):
    cx, cy, cw, ch = box(rect)
    label = heading_for_name or text(cap).split("\n")[0]
    name = img_name("brochure", label)
    alt = label.strip()
    s = slug(alt)
    return (f'<li class="bc"><div class="bc-cover"><a class="bc-link" href="#download-{s}" aria-label="Download brochure: {escape(alt)}">'
            f'<img class="bc-img" src="{I}/{name}" alt="{escape(alt)} brochure cover" width="{cw:g}" height="{ch:g}" loading="lazy"></a>{BADGE}</div>'
            + para(cap, "bc-cap" + (" bc-cap--excerpt" if g.get("caption") == "excerpt" else ""), link_slug="brochure-" + s,
                   strip_tail=lambda line: [(t, k) for t, k in line if not (t == "ad description")])
            + "</li>"), (cw, ch)


SIZES = set()
groups_html = []
prev_end = y("1:2784")
for gi, g in enumerate(BRO_GROUPS, start=1):
    cls = f"bg bg--{g['kind']} bg--m-{g['mobile']}" + (" bg--inset" if g.get("btn_inset") else "") + f" bg-{gi}"
    line_y = y(g["line"])
    if g["kind"] == "grid":
        cards, sizes = [], []
        for ci, (rect, cap) in enumerate(g["cards"]):
            h, sz = cover_card(rect, cap, g)
            if g.get("mobile_order"):
                h = h.replace('<li class="bc">', f'<li class="bc mo-{g["mobile_order"][ci]}">')
            cards.append(h)
            sizes.append((rect, sz))
        rects = [r for r, _ in g["cards"]]
        rows = sorted({round(y(r) + box(r)[3] - ROW_H) for r in rects})
        caps = sorted({round(y(c)) for _, c in g["cards"]})
        txt = f'<div class="bg-text {wcls(g["text"])}">{para(g["text"], "bg-copy")}</div>' if g["text"] else ""
        groups_html.append(f'<div class="{cls}">{txt}<ul class="bg-cards">' + "".join(cards) + '</ul><hr class="rule"></div>')
        top = y(g["text"]) if g["text"] else rows[0]
        gcss_rows.append((gi, top, rows, caps, line_y, prev_end))
    else:
        halves = []
        rows, caps = [], []
        for heading, (rect, cap) in g["halves"]:
            h, sz = cover_card(rect, cap, g, heading_for_name=text(heading).split("\n")[0])
            halves.append(f'<div class="bg-half"><div class="bg-text {wcls(heading)}">{para(heading, "bg-copy")}</div><ul class="bg-cards">{h}</ul></div>')
            rows.append(round(y(rect) + box(rect)[3] - ROW_H))
            caps.append(round(y(cap)))
        groups_html.append(f'<div class="{cls}"><div class="bg-halves">' + "".join(halves) + '</div><hr class="rule"></div>')
        top = min(y(hh[0]) for hh in g["halves"])
        gcss_rows.append((gi, top, sorted(set(rows)), sorted(set(caps)), line_y, prev_end))
    for rect in (g["cards"] if g["kind"] == "grid" else [hh[1][0] for hh in g["halves"]]):
        if isinstance(rect, tuple):
            rect = rect[0]
        SIZES.add(tuple(int(v) for v in box(rect)[2:]))
    prev_end = line_y

BRO_HTML = (f'<section class="rs br" id="brochures"><div class="fx"><hr class="rule rule--top"><h2 class="sec-h2 br-h2">{plain(BRO_H2)}</h2>'
            + "".join(groups_html) + "</div></section>")
css.add(".bg-copy", f"font-family: {OS}; color: #000000;")
css.add(".bg-copy strong", "font-weight: 700;")
css.add(".bg-copy .s16", "font-weight: 300;")
css.add(".bc-cover", "position: relative; display: flex; align-items: flex-end; justify-content: center;")
css.add(".bc-img", "display: block; height: auto; border-radius: 15px; box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25);")
css.add(".bc-cap", f"font-family: {OS}; font-weight: 700; color: {INK};")
css.add(".bc-cap--excerpt .s14", "font-weight: 300;")
css.add(".badge", "position: absolute; pointer-events: none;")
# desktop
css.add(".br > .fx", f"padding: 0 0 {u(y(BOTTOM['h2']) - y('1:2513') - 1)} {u(89)};", D)
css.add(".br .rule--top", f"margin-left: {u(85 - 89)}; width: {u(1263)};", D)
css.add(".bg .rule", f"width: {u(1259)};", D)
css.add(".bg-9 .rule", f"width: {u(1263)};", D)
css.add(".br-h2", f"margin-top: {u(y(BRO_H2) - y('1:2784') - 1)}; min-height: {u(y(BRO_GROUPS[0]['text']) - y(BRO_H2))};", D)
css.add(".bg-copy", f"font-size: {u(16)}; line-height: {u(26)};", D)
css.add(".bg-cards", f"display: grid; grid-template-columns: repeat(5, {u(210)}); column-gap: {u(PITCH - 210)}; margin-left: {u(COL0 - 89)};", D)
css.add(".bc", f"width: {u(210)};", D)
css.add(".bc-cover", f"height: {u(ROW_H)};", D)
css.add(".bc-img", f"width: auto; height: auto; max-width: none; border-radius: {u(15)};", D)
css.add(".bc-cap", f"margin: {u(21)} 0 0 {u(4)}; width: {u(205)}; font-size: {u(14)}; line-height: {u(22)};", D)
css.add(".badge", f"left: {u(-1)}; top: 0; width: {u(45)}; height: {u(45)};", D)
css.add(".bg--inset .badge", f"left: {u(1)}; top: {u(16)};", D)
css.add(".bg-halves", f"display: grid; grid-template-columns: {u(708 - 89)} auto;", D)
css.add(".bg-half .bg-cards", "display: block;", D)
for gi, top, rows, caps, line_y, prev in gcss_rows:
    sel = f".bg-{gi}"
    row0 = rows[0]
    if gi > 1:
        css.add(f"{sel}", f"margin-top: {u(top - prev - 1)};", D)
    if gi != 9:
        css.add(f"{sel} .bg-text", f"min-height: {u(row0 - top)};", D)
    cap_h = (rows[1] - caps[0]) if len(rows) > 1 else (line_y - caps[-1])
    css.add(f"{sel} .bc-cap", f"min-height: {u(cap_h)};", D)
    if len(rows) > 1:
        css.add(f"{sel} .bg-cards", f"padding-bottom: {u(line_y - caps[-1] - cap_h)};", D)
    if caps[0] != row0 + ROW_H + 21:
        css.add(f"{sel} .bc-cap", f"margin-top: {u(caps[0] - row0 - ROW_H)};", D)
for cw, ch in sorted(SIZES):
    css.add(f'.bc-img[width="{cw}"][height="{ch}"]', f"width: {u(cw)}; height: {u(ch)};", D)
# mobile: 1:659 (h2 28/50), groups p0/20/44/20 gap 36; grid groups 2 columns gap 30.6 with the card scaled 0.85; stack = full size
css.add(".br > .fx", "padding-top: 0;", M)
css.add(".br-h2", "margin-top: 8px; font-size: 28px; line-height: 50px;", M)
css.add(".bg, .bg-half", "display: flex; flex-direction: column; gap: 36px;", M)
css.add(".bg + .bg", "margin-top: 8px;", M)
css.add(".bg-halves", "display: flex; flex-direction: column; gap: 36px;", M)
css.add(".bg-copy", "font-size: 16px; line-height: 26px;", M)
css.add(".bg-copy .lh26", "line-height: 26px;", M)
css.add(".bg--m-grid .bg-cards", "--s: 0.85; display: grid; grid-template-columns: 1fr 1fr; gap: 30.6px;", M)
css.add(".bg--m-stack .bg-cards", "--s: 1; display: flex; flex-direction: column; gap: 36px;", M)
css.add(".bc-cover", "height: calc(245px * var(--s, 1)); justify-content: flex-start;", M)
css.add(".bg--m-grid .bc-cover", "justify-content: center;", M)
css.add(".bc-img", "border-radius: calc(15px * var(--s, 1));", M)
for cw, ch in sorted(SIZES):
    css.add(f'.bc-img[width="{cw}"][height="{ch}"]', f"width: calc({cw}px * var(--s, 1)); height: calc({ch}px * var(--s, 1));", M)
css.add(".bc-cap", "margin-top: calc(21px * var(--s, 1)); font-size: calc(14px * var(--s, 1)); line-height: calc(22px * var(--s, 1));", M)
css.add(".bc-cap .lh22", "line-height: calc(22px * var(--s, 1));", M)
css.add(".bc-cap--excerpt", "padding-left: 23px;", M)
css.add(".badge", "left: 0; top: 0; width: calc(45px * var(--s, 1)); height: calc(45px * var(--s, 1));", M)
css.add(".bg--inset .badge", "left: 13px; top: 15px;", M)
css.add(".bg--m-grid.bg--inset .badge", "left: 10px; top: 13px;", M)
for k in range(1, 8):
    css.add(f".mo-{k}", f"order: {k};", M)

# ================================================================ bottom links (1:2504)  desktop y 8731..8988 · mobile 1:1004
bh_x, bh_y, bh_w = box(BOTTOM["h2"])[:3]
btns = []
for bi, (bx_, tx_) in enumerate(BOTTOM["buttons"]):
    btns.append(f'<a class="bl-btn bl-btn--{bi + 1}" href="#bottom-link-{bi + 1}">{plain(tx_)}</a>')
BOTTOM_HTML = (f'<section class="rs bl" id="continue-your-visit"><div class="fx"><hr class="rule bl-rule m-only"><h2 class="bl-h2">{plain(BOTTOM["h2"])}</h2>'
               '<div class="bl-btns">' + "".join(btns) + "</div></div></section>")
b0 = box(BOTTOM["buttons"][0][0])
css.add(".bl-h2", f"margin: 0; font-family: {FR}; font-weight: 400; color: {BLUE}; text-align: center; text-transform: uppercase;")
css.add(".bl-btn", f"display: flex; align-items: center; justify-content: center; box-sizing: border-box; font-family: {FR}; font-weight: 400;")
css.add(".bl-btn--1", f"background: {BLUE}; color: #FFFFFF;")
css.add(".bl-btn--2", f"color: {SKY};")
css.add(".bl-btn--3", f"color: {BLUE};")
css.add(".bl > .fx", f"padding-bottom: {u(8988 - b0[1] - b0[3])};", D)
css.add(".bl-h2", f"font-size: {u(34)}; line-height: {u(50)}; min-height: {u(b0[1] - bh_y)};", D)
css.add(".bl-btns", f"display: flex; justify-content: center; gap: {u(13)};", D)
css.add(".bl-btn", f"height: {u(50)}; border-radius: {u(5)}; font-size: {u(18)}; line-height: {u(50)};", D)
for bi, (bx_, _) in enumerate(BOTTOM["buttons"]):
    css.add(f".bl-btn--{bi + 1}", f"width: {u(box(bx_)[2])};", D)
css.add(".bl-btn--2, .bl-btn--3", f"border: 2px solid {SKY};", D)
css.add(".bl > .fx", "padding-top: 0;", M)
css.add(".bl-rule", "margin-bottom: 8px;", M)
css.add(".bl-h2", "font-size: 24px; line-height: 31.92px;", M)
css.add(".bl-btns", "display: flex; flex-direction: column; gap: 12px;", M)
css.add(".bl-btn", "height: 50px; border-radius: 5px; font-size: 16px; line-height: 21.28px; padding: 0 20px; text-align: center;", M)
css.add(".bl-btn--2, .bl-btn--3", f"border: 1px solid {SKY};", M)

# ---------------------------------------------------------------- page-level (fonts, mobile column cap, utility widths)
PAGE_CSS = """
@font-face { font-family: 'Open Sans'; font-style: italic; font-weight: 300; font-stretch: 100%; font-display: swap; src: url(https://fonts.gstatic.com/s/opensans/v44/memtYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWqWuU6F.woff2) format('woff2'); unicode-range: U+0000-00FF, U+2000-206F; }
"""
# ^ Google's real 300-italic file (css2 API). The memQYa... file in chrome.py SHARED is a different, bolder face (#26 matched it to 600).
for sh in sorted(SHIFTS):
    if sh:
        n = f"sh{sh:g}".replace("-", "n").replace(".", "_")
        css.add(f".{n}", f"position: relative; top: {u(sh)};", D)
        css.add(f".{n}", f"position: relative; top: {sh:g}px;", M)
for w in sorted(W):
    css.add(f".w{w}", f"width: {u(w)};", D)
css.add(".ri > .fx, .rt > .fx, .ff > .fx, .br > .fx, .bl > .fx", "max-width: 640px; margin: 0 auto; box-sizing: border-box;", M)
css.add(".ri > .fx, .rt > .fx, .ff > .fx, .br > .fx, .bl > .fx", "height: auto;", D)

BADGE_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="45" height="45" viewBox="0 0 45 45" fill="none">'
             '<circle cx="22.5" cy="22.5" r="20.5" fill="#FFFFFF" stroke="#00B3F0" stroke-width="4"/>'
             '<g stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
             '<path d="M23 10v15"/><path d="M18 20.5l5 5 5-5"/><path d="M14 28v3h17v-3"/></g></svg>')

# ================================================================ blueprint + compile
NOTE = ("2026-09-28 Resources replica (Flow A, HTML first; ACF conversion comes after developer review). Figma 1:2490 on desktop "
        "(flow layout, u() units, min-height-to-next-Figma-y), Figma 1:559 auto-layout on mobile. Generated by tools/figma_html/build_resources.py; "
        "copy read from pages/_figma/file.json by node id (tools/figma_html/resources_data.py).")
SECTIONS = [
    {"id": "site-header", "landmark": "header", "escape_hatch": True, "html": HEAD_HTML, "css": SHARED + HEADER_CSS, "js": HEADER_JS},
    {"id": "resources-intro", "escape_hatch": True, "heading_level": 1, "html": INTRO_HTML, "css": PAGE_CSS + css.render()},
    {"id": "testimonials", "escape_hatch": True, "html": TESTI_HTML, "css": ""},
    {"id": "fast-facts", "escape_hatch": True, "html": FACTS_HTML, "css": ""},
    {"id": "brochures", "escape_hatch": True, "html": BRO_HTML, "css": ""},
    {"id": "continue-your-visit", "escape_hatch": True, "html": BOTTOM_HTML, "css": ""},
    {"id": "site-footer", "landmark": "footer", "escape_hatch": True, "html": FOOT_HTML, "css": FOOT_CSS},
]
for s in SECTIONS:
    s["notes"] = [NOTE]
    s["html"] = link_pages(s["html"])

bp = {
    "page": "resources",
    "meta": {"title": "Resources | Mizuho America",
             "description": "The Mizuho America library for neurosurgeons: video testimonials from renowned leaders in the field, fast facts, and downloadable product brochures."},
    "css_workflow": "scss", "font_source": "google",
    "notes_for_developer": [
        "Replica of Figma 1:2490 / 1:559 built the same way as the Home replica (issues-log #27). Header/footer shared with Home via tools/figma_html/chrome.py.",
        "Every string is read from the Figma JSON by node id; two Figma data defects are handled in the generator and logged: a stray 'ad description' run in 1:2744 (not rendered in the export) and a duplicated T2 Clips card on mobile only (1:992).",
    ],
    "sections": SECTIONS,
}
os.makedirs(os.path.join(PAGE, "figma"), exist_ok=True)
json.dump(bp, open(os.path.join(PAGE, "blueprint.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)

# tokens: same design system as Home
tok = json.load(open(os.path.join(ROOT, "pages", "mizuho-home", "figma", "tokens.json"), encoding="utf-8"))
# Home got Gotham->Montserrat from its section-specs.json; Resources has none, so without this the compiler asked Google
# Fonts for "Gotham" (doesn't exist) and never loaded Montserrat (issues-log).
tok["font_substitution"] = {"Gotham": "Montserrat"}
json.dump(tok, open(os.path.join(PAGE, "figma", "tokens.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
img_dir = os.path.join(PAGE, "figma", "images")
open(os.path.join(img_dir, "icon-download-badge.svg"), "w", encoding="utf-8").write(BADGE_SVG)
for f in ("icon-play-circle.svg", "logo-mizuho-header-srgb.png", "logo-mizuho-footer-reversed.png"):
    shutil.copy(os.path.join(ROOT, "pages", "mizuho-home", "figma", "images", f), os.path.join(img_dir, f))

r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "figma_html", "run_devcommand_compiler.py"), "resources"],
                   capture_output=True, text=True, encoding="utf-8")
open(os.path.join(ROOT, "cache", "tmp", "resources-compile.log"), "w", encoding="utf-8").write(r.stdout + r.stderr)
if r.returncode:
    print(r.stdout[-3000:], r.stderr[-3000:])
    raise SystemExit("compile failed")
out_img = os.path.join(PAGE, "html", "figma", "images")
os.makedirs(out_img, exist_ok=True)
for f in os.listdir(img_dir):
    if f != "asset-manifest.json":
        shutil.copy(os.path.join(img_dir, f), os.path.join(out_img, f))
v = subprocess.run([sys.executable, os.path.join(PLUGIN, "scripts", "validate_html_output.py"), "--dir", os.path.join(PAGE, "html")],
                   capture_output=True, text=True, encoding="utf-8")
open(os.path.join(ROOT, "cache", "tmp", "resources-validate.json"), "w", encoding="utf-8").write(v.stdout + v.stderr)
print("compiled; validator exit", v.returncode)
print(v.stdout[:1500])
