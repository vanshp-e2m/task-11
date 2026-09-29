"""Sales Hub Login (Figma 1:3150 / 1:2210) and Dashboard (1:3095 / 1:1903) replicas → pages/sales-hub-login|sales-hub-dashboard/html/.

Same method as the other replicas. Portal chrome from chrome_portal.py (Dashboard uses the centred-logo footer variant drawn in
its frame). The Login frame draws a fake browser address bar ("www.mizuho.com/sales-hub/login") across the top: that's
mock-up chrome, not page content, so it's left out and every Login y is shifted up by its 55px.
Replica links: Log in → Dashboard; the Resource Library tool card and the portal nav → the Resource Library replica.
On the real site Login is a styled wp_login_form() and "John Q." / the counts come from the user and the queries.

    python tools/figma_html/build_sales_hub.py
"""
import os
from html import escape

import cv2

from chrome import D, FR, I, M, OS, ROOT, SHARED, u
from chrome_portal import CARET_SVG, PORTAL_FOOTER_CSS, PORTAL_FOOTER_HTML, PORTAL_HEADER_CSS, PORTAL_HEADER_JS, portal_header
from replica_lib import Css, Page, compile_page

INK, BLUE, SKY = "#090909", "#0065B3", "#00B3F0"
DASH = "../../sales-hub-dashboard/html/"
LIB = "../../resource-library/html/"
FOOT_SECTION = {"id": "site-footer", "landmark": "footer", "escape_hatch": True, "html": PORTAL_FOOTER_HTML, "css": PORTAL_FOOTER_CSS}


# ================================================================ LOGIN
def login():
    P = Page("1:3150")
    box, y, plain = P.box, P.y, P.plain
    css = Css()
    SHIFT = 55  # the drawn browser bar
    cx, cy, cw, ch = box("1:3158")
    cy -= SHIFT
    rel = lambda nid: (box(nid)[0] - cx, box(nid)[1] - SHIFT - cy)  # noqa: E731
    lx, ly = rel("1:3163")
    tx, ty = rel("1:3162")
    el, ely = rel("1:3167")
    ix, iy = rel("1:3166")
    pl, ply = rel("1:3171")
    px_, pyy = rel("1:3169")
    bx, by = rel("1:3164")
    fy = rel("1:3160")[1]
    liy = rel("1:3161")[1]
    ny = rel("1:3159")[1]
    note = "<br>".join(escape(s.strip()) for s in P.text("1:3159").split("\n"))
    HTML = (f'<section class="rs lg" id="sales-hub-login"><div class="fx"><div class="lg-card">'
            f'<img class="lg-logo" src="{I}/logo-mizuho-header-srgb.png" alt="Mizuho America" width="200" height="61">'
            f'<h1 class="lg-h1">{plain("1:3162")}</h1>'
            f'<form class="lg-form" action="{DASH}" method="get">'
            f'<label class="lg-label" for="lg-email">{plain("1:3167")}</label><input class="lg-in" id="lg-email" type="email" name="log" placeholder="{plain("1:3168")}" autocomplete="username" required>'
            f'<label class="lg-label" for="lg-pass">{plain("1:3171")}</label><input class="lg-in" id="lg-pass" type="password" name="pwd" placeholder="{plain("1:3170")}" autocomplete="current-password" required>'
            f'<button class="lg-go" type="submit">{plain("1:3165")}</button></form>'
            f'<a class="lg-forgot" href="http://task-11.local/wp-login.php?action=lostpassword">{plain("1:3160")}</a><hr class="lg-rule"><p class="lg-note">{note}</p></div></div></section>')
    css.add(".lg", "background: #D9D9D9;")
    css.add(".lg > .fx", "background: #D9D9D9;")
    css.add(".rs.lg.lg, .rs.lg.lg > .fx", "background: #D9D9D9;", M)  # beat chrome's mobile #FCFEFF section rule (issues-log #42)
    css.add(".lg-card", "box-sizing: border-box; background: #FFFFFF; border-radius: 10px; box-shadow: 0 5px 13px rgba(0, 0, 0, 0.18); text-align: center;")
    css.add(".lg-logo", "display: block; margin: 0 auto; width: 200px; height: 61px; object-fit: cover;")
    css.add(".lg-h1", f"margin: 0; font-family: {FR}; font-weight: 400; font-size: 15px; line-height: 19.95px; color: {BLUE}; text-transform: uppercase;")
    css.add(".lg-form", "display: flex; flex-direction: column; text-align: left;")
    css.add(".lg-label", f"font-family: {OS}; font-weight: 400; font-size: 13px; line-height: 30px; color: {INK};")
    css.add(".lg-in", f"box-sizing: border-box; height: 40px; padding: 0 15px; border: 0; border-radius: 5px; background: #FFFFFF; box-shadow: inset 2px 2px 6px rgba(0, 0, 0, 0.17); font-family: {OS}; font-size: 13px; color: #000000;")
    css.add(".lg-in::placeholder", "color: rgba(0, 0, 0, 0.35); opacity: 1;")
    css.add(".lg-in:focus-visible, .lg-go:focus-visible", f"outline: 2px solid {SKY}; outline-offset: 1px;")
    css.add(".lg-go", f"height: 45px; border: 0; border-radius: 5px; background: {BLUE}; color: #FFFFFF; font-family: {FR}; font-weight: 400; font-size: 16px; cursor: pointer;")
    css.add(".lg-forgot", f"display: block; font-family: {OS}; font-weight: 700; font-size: 13px; line-height: 18px; color: {BLUE};")
    css.add(".lg-rule", "margin: 0; border: 0; border-top: 1px solid rgba(0, 0, 0, 0.2);")
    css.add(".lg-note", "margin: 0; font-family: 'Open Sans', sans-serif; font-weight: 400; font-size: 12px; line-height: 18px; color: rgba(0, 0, 0, 0.5);")
    # desktop: the card sits at Figma y 230-55; the grey page runs to the footer (Figma 873-55)
    css.add(".lg > .fx", f"height: {u(873 - SHIFT)}; padding-top: {u(cy)}; box-sizing: border-box;", D)
    css.add(".lg-card", f"margin-left: {u(cx)}; width: {u(cw)}; height: {u(ch)}; padding: {u(ly)} {u(ix)} 0;", D)
    css.add(".lg-h1", f"margin-top: {u(ty - ly - 61)}; min-height: {u(ely - ty)};", D)
    css.add(".lg-label", f"line-height: {u(30)}; height: {u(iy - ely)}; font-size: {u(13)};", D)  # Figma: 30px line box, input 27px below the label top
    css.add(".lg-in", f"height: {u(40)}; margin-bottom: {u(ply - iy - 40)}; font-size: {u(13)};", D)
    css.add(".lg-in[type=password]", f"margin-bottom: {u(by - pyy - 40)};", D)
    css.add(".lg-go", f"height: {u(45)}; font-size: {u(16)};", D)
    css.add(".lg-forgot", f"margin-top: {u(fy - by - 45)};", D)
    css.add(".lg-rule", f"margin-top: {u(liy - fy - 18)};", D)
    css.add(".lg-note", f"margin: {u(ny - liy)} auto 0; width: {u(294)};", D)
    # mobile 1:2216: grey p132/20 around a 374px card (x28), inner width 312
    css.add(".lg > .fx", "padding: 132px 28px; align-items: center;", M)
    css.add(".lg-card", f"width: 100%; max-width: 374px; height: 510px; padding: {ly}px 31px 0;", M)
    css.add(".lg-h1", f"margin-top: {ty - ly - 61}px; min-height: {ely - ty}px;", M)
    css.add(".lg-label", f"height: {iy - ely}px;", M)
    css.add(".lg-in", f"margin-bottom: {ply - iy - 40}px;", M)
    css.add(".lg-in[type=password]", f"margin-bottom: {by - pyy - 40}px;", M)
    css.add(".lg-forgot", f"margin-top: {fy - by - 45}px;", M)
    css.add(".lg-rule", f"margin-top: {liy - fy - 18}px;", M)
    css.add(".lg-note", f"margin: {ny - liy}px auto 0; max-width: 275px;", M)
    # Login has no header section, and the shared resets + the --u unit ride on the header's CSS everywhere else (issues-log)
    SECTIONS = [{"id": "sales-hub-login", "escape_hatch": True, "heading_level": 1, "html": HTML, "css": SHARED + css.render()}, FOOT_SECTION]
    note = "2026-09-28 Sales Hub Login replica. Figma 1:3150 / 1:2210 (drawn browser bar left out). Generated by tools/figma_html/build_sales_hub.py."
    for s in SECTIONS:
        s["notes"] = [note]
    compile_page("sales-hub-login", {"page": "sales-hub-login",
                                     "meta": {"title": "Log in | Sales Hub | Mizuho America", "description": "Sales Hub rep portal login for registered Mizuho America sales representatives."},
                                     "css_workflow": "scss", "font_source": "google",
                                     "notes_for_developer": ["Real site: styled wp_login_form(); access limited to the sales_rep role."],
                                     "sections": SECTIONS},
                 extra_images=("logo-mizuho-header-srgb.png", "logo-mizuho-footer-reversed.png"))


# ================================================================ DASHBOARD
def dashboard():
    P = Page("1:3095")
    box, y, plain = P.box, P.y, P.plain
    IMG = os.path.join(ROOT, "pages", "sales-hub-dashboard", "figma", "images")
    os.makedirs(IMG, exist_ok=True)
    EXP = cv2.imread(os.path.join(ROOT, "pages/_figma/frames/export/Dashboard.png"))
    css = Css()
    px, py, pw, ph = box("1:3111")
    STATS = [("1:3114", "1:3120", "1:3117"), ("1:3115", "1:3121", "1:3118"), ("1:3116", "1:3122", "1:3119")]
    TOOLS = [("1:3123", "1:3132", "1:3133", "1:3129", "1:3126", LIB), ("1:3124", "1:3134", "1:3136", "1:3130", "1:3127", "http://task-11.local/sales-hub/cross-reference/"),
             ("1:3125", "1:3135", "1:3137", "1:3131", "1:3128", "http://task-11.local/sales-hub/training/")]
    stats = "".join(f'<li class="db-stat"><span class="db-num">{plain(n)}</span><span class="db-label">{plain(l)}</span></li>' for _, n, l in STATS)
    tools = ""
    for card, tile, icon, title, desc, href in TOOLS:
        x, y_, w, h = (int(round(v)) for v in box(icon))
        name = f"icon-tool-{plain(title).lower().replace(' ', '-')}.png"
        cv2.imwrite(os.path.join(IMG, name), EXP[y_:y_ + h, x:x + w])
        tools += (f'<li class="db-tool"><span class="db-icon"><img src="figma/images/{name}" alt="" width="{w}" height="{h}"></span>'
                  f'<div class="db-tool-text"><h2 class="db-tool-h"><a href="{href}">{plain(title)}</a></h2><p class="db-tool-p">{plain(desc)}</p></div></li>')
    ax = box("1:3103")
    HTML = (f'<section class="rs db" id="dashboard"><div class="fx"><div class="db-panel"><h1 class="db-h1">{plain("1:3112")}</h1><p class="db-lead">{plain("1:3113")}</p>'
            f'<div class="db-grid"><ul class="db-stats" aria-label="At a glance">{stats}</ul><ul class="db-tools">{tools}</ul></div></div></div></section>'
            f'<section class="rs db-acc" id="account"><div class="fx"><h2 class="db-acc-h">{plain("1:3109")}</h2><div class="db-acc-btns">'
            f'<a class="db-btn db-btn--1" href="../../sales-hub-login/html/">{plain("1:3104")}</a>'
            f'<a class="db-btn db-btn--2" href="#account-details">{plain("1:3106")}</a>'
            f'<a class="db-btn db-btn--3" href="http://task-11.local/wp-login.php?action=lostpassword">{plain("1:3108")}</a></div></div></section>')
    s0, s1 = box(STATS[0][0]), box(STATS[1][0])
    t0 = box(TOOLS[0][0])
    tl = box(TOOLS[0][1])
    css.add(".db-panel", "box-sizing: border-box; background: rgba(196, 196, 196, 0.15);")
    css.add(".db-h1", f"margin: 0; font-family: {FR}; font-weight: 400; font-size: 24px; line-height: 32px; color: #000000; text-transform: uppercase;")
    css.add(".db-lead", f"margin: 0; font-family: {OS}; font-weight: 400; color: #000000;")
    css.add(".db-stats, .db-tools", "margin: 0; padding: 0; list-style: none;")
    css.add(".db-stat", f"position: relative; box-sizing: border-box; background: {SKY}; border-radius: 8px; color: #FFFFFF;")
    css.add(".db-num", f"position: absolute; font-family: {FR}; font-weight: 400; font-size: 68px; line-height: 46px;")
    css.add(".db-label", f"position: absolute; font-family: {OS}; font-weight: 700; font-size: 14px; line-height: 22px;")
    css.add(".db-tool", "display: flex; box-sizing: border-box; background: #FFFFFF; box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.15); border-radius: 10px;")
    css.add(".db-icon", "display: flex; align-items: center; justify-content: center; flex: none; width: 84px; height: 85px; background: rgba(249, 255, 67, 0.25); border-radius: 5px; box-shadow: 2px 0 4px rgba(0, 0, 0, 0.35);")
    css.add(".db-icon img", "display: block; border-radius: 10px;")
    css.add(".db-tool-h", f"margin: 0; font-family: {OS}; font-weight: 700; font-size: 14px; line-height: 22px;")
    css.add(".db-tool-h a", f"color: {BLUE}; text-decoration: none;")
    css.add(".db-tool-p", f"margin: 0; font-family: {OS}; font-weight: 300; font-size: 14px; color: #000000;")
    css.add(".db-acc-h", f"margin: 0; font-family: {FR}; font-weight: 400; font-size: 20px; line-height: 50px; color: #000000; text-transform: uppercase;")
    css.add(".db-acc-btns", "display: flex;")
    css.add(".db-btn", f"display: flex; align-items: center; justify-content: center; box-sizing: border-box; border-radius: 5px; font-family: {FR}; font-weight: 400; font-size: 16px;")
    css.add(".db-btn--1", f"background: {BLUE}; color: #FFFFFF;")
    css.add(".db-btn--2", f"color: {SKY};")
    css.add(".db-btn--3", f"color: {BLUE};")
    css.add(".rs.db-acc.db-acc, .rs.db-acc.db-acc > .fx", "background: #F6F6F6;", M)
    # desktop
    css.add(".db > .fx", f"padding: 0 0 {u(734 - py - ph)} {u(px)};", D)
    css.add(".db-panel", f"width: {u(pw)}; height: {u(ph)}; border-radius: {u(15)}; padding: {u(y('1:3112') - py)} 0 0 {u(box('1:3112')[0] - px)};", D)
    css.add(".db-h1", f"min-height: {u(y('1:3113') - y('1:3112'))};", D)
    css.add(".db-lead", f"font-size: {u(14)}; line-height: {u(22)}; min-height: {u(s0[1] - y('1:3113'))};", D)
    css.add(".db-grid", f"display: flex; gap: {u(t0[0] - s0[0] - s0[2])};", D)
    css.add(".db-stats, .db-tools", f"display: flex; flex-direction: column; gap: {u(s1[1] - s0[1] - s0[3])};", D)
    css.add(".db-stat", f"width: {u(s0[2])}; height: {u(s0[3])};", D)
    css.add(".db-num", f"left: {u(box(STATS[0][1])[0] - s0[0])}; top: {u(box(STATS[0][1])[1] - s0[1] - 12)}; font-size: {u(68)}; line-height: {u(46)};", D)
    css.add(".db-label", f"left: {u(box(STATS[0][2])[0] - s0[0])}; top: {u(box(STATS[0][2])[1] - s0[1])}; font-size: {u(14)}; line-height: {u(22)};", D)
    css.add(".db-tool", f"width: {u(t0[2])}; height: {u(t0[3])}; padding: {u(tl[1] - t0[1])} 0 0 {u(tl[0] - t0[0])}; gap: {u(box(TOOLS[0][3])[0] - tl[0] - 84)};", D)
    css.add(".db-tool-text", f"padding-top: {u(y(TOOLS[0][3]) - tl[1] - 15)};", D)
    css.add(".db-tool-p", f"line-height: {u(22)};", D)
    css.add(".db-acc", "background: linear-gradient(#F6F6F6, #F6F6F6) top / 100% 50px no-repeat;", D)
    css.add(".db-acc > .fx", f"height: {u(873 - 734)}; padding-left: {u(box('1:3109')[0])}; box-sizing: border-box;", D)
    css.add(".db-acc-h", f"height: {u(50)}; font-size: {u(20)}; line-height: {u(50)}; margin-bottom: {u(ax[1] - 734 - 50)};", D)
    css.add(".db-acc-btns", f"gap: {u(20)};", D)
    css.add(".db-btn", f"height: {u(45)}; font-size: {u(16)};", D)
    for i, nid in enumerate(("1:3103", "1:3105", "1:3107")):
        css.add(f".db-btn--{i + 1}", f"width: {u(box(nid)[2])};", D)
    css.add(".db-btn--2, .db-btn--3", f"border: 2px solid {SKY};", D)
    # mobile 1:1914: panel p32 gap20; stats and tools stacked; account band grey p22; buttons 390x50 gap12
    css.add(".db-panel", "display: flex; flex-direction: column; gap: 20px; padding: 32px; border-radius: 12px;", M)
    css.add(".db-lead", "font-size: 11px; line-height: 18px;", M)
    css.add(".db-grid, .db-stats, .db-tools", "display: flex; flex-direction: column; gap: 20px;", M)
    css.add(".db-stat", "height: 115px;", M)
    css.add(".db-num", "left: 35px; top: 35px;", M)
    css.add(".db-label", "left: 92px; top: 71px;", M)
    css.add(".db-tool", "flex-direction: column; gap: 24px; padding: 15px;", M)
    css.add(".db-tool-p", "line-height: 18px;", M)
    css.add(".db-acc > .fx", "padding: 22px 20px;", M)
    css.add(".db-acc-btns", "flex-direction: column; gap: 12px; margin: 22px -20px 0; padding: 44px 20px; background: #FCFEFF;", M)
    css.add(".db-btn", "height: 50px;", M)
    css.add(".db-btn--2, .db-btn--3", f"border: 1px solid {SKY};", M)
    css.add(".db > .fx, .db-acc > .fx", "max-width: 640px; margin: 0 auto; box-sizing: border-box;", M)
    SECTIONS = [
        {"id": "site-header", "landmark": "header", "escape_hatch": True, "html": portal_header("Dashboard"), "css": PORTAL_HEADER_CSS, "js": PORTAL_HEADER_JS},
        {"id": "dashboard", "escape_hatch": True, "heading_level": 1, "html": HTML, "css": css.render()},
        dict(FOOT_SECTION, html=PORTAL_FOOTER_HTML.replace('class="site-foot portal-foot rs"', 'class="site-foot portal-foot pf--center rs"')),
    ]
    note = "2026-09-28 Sales Hub Dashboard replica. Figma 1:3095 / 1:1903. Generated by tools/figma_html/build_sales_hub.py."
    for s in SECTIONS:
        s["notes"] = [note]
    compile_page("sales-hub-dashboard", {"page": "sales-hub-dashboard",
                                         "meta": {"title": "Dashboard | Sales Hub | Mizuho America", "description": "Sales Hub dashboard: resource library, cross-reference tool and training hub."},
                                         "css_workflow": "scss", "font_source": "google",
                                         "notes_for_developer": ["Real site: 'John Q.' = the logged-in rep; the three counts come from the product/resource queries.",
                                                                 "Figma shows a 'Log in' button in the Account band of a logged-in page; followed as drawn, flagged."],
                                         "sections": SECTIONS},
                 extra_images=("logo-mizuho-header-srgb.png", "logo-mizuho-footer-reversed.png"), svgs={"icon-select-caret.svg": CARET_SVG})


if __name__ == "__main__":
    login()
    dashboard()
