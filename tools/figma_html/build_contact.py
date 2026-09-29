"""Contact Us replica (Figma 1:3891 desktop 1440 / 1:1027 mobile 430) → pages/contact-us/html/.

HTML first (the Elementor build of Contact Us comes after developer review, like About). Same method as the other
replicas: desktop flow layout in u() with min-height-to-next-Figma-y, mobile = the 430 frame's auto-layout, copy read
from pages/_figma/file.json by node id. Header/footer are Home's (chrome.py) with "Contact & Support" current.
No raster images apart from the logos: chevrons, select carets and radios are CSS/SVG.

    python tools/figma_html/build_contact.py
"""
from html import escape

from chrome import D, FOOT_CSS, FOOT_HTML, FR, HEADER_CSS, HEADER_HTML, HEADER_JS, M, OS, SHARED, link_pages, u
from chrome_portal import CARET_SVG
from replica_lib import Css, Page, compile_page, figma_linear, slug

P = Page("1:3891")
box, y, plain, text = P.box, P.y, P.plain, P.text
SLUG = "contact-us"
INK, BLUE, SKY = "#090909", "#0065B3", "#00B3F0"
css = Css()


def grad(nid):
    b = box(nid)
    return figma_linear(P.node(nid)["fills"][0], b[2], b[3])


INTRO = dict(h1="1:3958", panel="1:3915", h2="1:3916", body="1:3957", card="1:3952", card_h="1:3953",
             card_lines=["1:3954", "1:3956", "1:3955"])
FORM = dict(box="1:3959", intro="1:3961", note="1:3986", submit="1:3962", submit_text="1:3963",
            q="1:3987", yes=("1:3988", "1:3989"), no=("1:3990", "1:3991"),
            fields=[("1:3964", "1:3965", "text"), ("1:3966", "1:3967", "text"), ("1:3968", "1:3969", "text"),
                    ("1:3970", "1:3971", "select"), ("1:3978", "1:3979", "text"), ("1:3972", "1:3973", "select"),
                    ("1:3980", "1:3981", "email"), ("1:3982", "1:3983", "tel"), ("1:3984", "1:3985", "text")])
FAQ = dict(h2="1:3947", items=[("1:3918", "1:3919"), ("1:3921", "1:3924"), ("1:3926", "1:3928"), ("1:3929", "1:3931"),
                               ("1:3932", "1:3934"), ("1:3935", "1:3937"), ("1:3938", "1:3940"), ("1:3941", "1:3943"),
                               ("1:3944", "1:3946")],
           open_index=1, answer="1:3925", answer_panel="1:3922", button="1:3949", button_text="1:3950", line="1:3948")
BOTTOM = dict(h2="1:3912", buttons=[("1:3906", "1:3908"), ("1:3907", "1:3909"), ("1:3910", "1:3911")])


def rich(nid):
    """Runs → inline HTML; bold blue runs become links (mailto: for e-mail, tel: for numbers, #faq otherwise)."""
    out = ""
    for t, k in P.fig_lines_flat(nid) if hasattr(P, "fig_lines_flat") else [(t, k) for line in P.fig_lines(nid) for (t, k) in line + [("\n", None)]]:
        if k is None:
            out += "<br>"
            continue
        e = escape(t.replace("\xa0", " "))
        if k[5] and k[5].lower() == BLUE.lower():
            raw = t.strip().replace("\xa0", "")
            href = f"mailto:{raw}" if "@" in raw else (f"tel:{raw.replace('-', '')}" if raw[:3].isdigit() else "#faq")
            out += f'<a class="cu-link" href="{href}">{e}</a>'
        elif k[1] and k[1] >= 700:
            out += f"<strong>{e}</strong>"
        else:
            out += e
    return out[:-4] if out.endswith("<br>") else out


# ================================================================ header
HEAD_HTML = HEADER_HTML.replace('<a href="#contact-support">', '<a class="is-current" aria-current="page" href="#contact-support">')
assert HEAD_HTML != HEADER_HTML
css.add(".site-head__nav a.is-current", f"color: {BLUE};")

# ================================================================ intro panel + contact card + form  (desktop y 161..1581)
h1x, h1y = box(INTRO["h1"])[:2]
px, py, pw, ph = box(INTRO["panel"])
h2x, h2y, h2w = box(INTRO["h2"])[:3]
bx_, by_, bw_ = box(INTRO["body"])[:3]
cx, cy, cw, ch = box(INTRO["card"])
chx, chy = box(INTRO["card_h"])[:2]
paras = [p.strip("\n") for p in text(INTRO["body"]).split("\n\xa0\n")]
body_html = ""
for p in paras:
    if p.startswith("Get answers now"):
        body_html += f'<p class="cu-p"><a class="cu-link" href="#faq"><strong>{escape(p)}</strong></a></p>'
    else:
        body_html += '<p class="cu-p">' + "<br>".join(escape(s) for s in p.split("\n")) + "</p>"
card_lines = []
for nid in INTRO["card_lines"]:
    card_lines.append(P.para(nid, "cu-card-block").replace('class="more', 'class="cu-link'))
# phone/fax/e-mail values are blue runs in Figma → real links
card_html = ""
for line in P.fig_lines(INTRO["card_lines"][0]):
    label = "".join(t for t, k in line if k[5] != "#0065b3").strip()
    val = "".join(t for t, k in line if k[5] == "#0065b3").strip()
    href = f"mailto:{val}" if "@" in val else f"tel:{val.replace('-', '')}"
    card_html += f'<p class="ln lh32">{escape(label)} <a class="cu-link" href="{href}">{escape(val)}</a></p>'
card_html = (f'<div class="cu-card-block cu-card-reach">{card_html}</div>' + P.para(INTRO["card_lines"][1], "cu-card-block cu-card-hours")
             + P.para(INTRO["card_lines"][2], "cu-card-block cu-card-addr"))

fbx, fby, fbw, fbh = box(FORM["box"])
f0 = box(FORM["fields"][0][0])
fields = []
for rect, label_id, kind in FORM["fields"]:
    label = text(label_id).replace("*", "").strip()
    req = "*" in text(label_id)
    fid = "cu-" + slug(label)
    star = '<span class="req" aria-hidden="true">*</span>' if req else ""
    r = " required" if req else ""
    if kind == "select":
        fields.append(f'<div class="fld fld--select"><label class="visually-hidden" for="{fid}">{escape(label)}</label>'
                      f'<select class="fld-in" id="{fid}" name="{slug(label)}"{r}><option value="" selected disabled>{escape(label)}</option></select></div>')
    else:
        auto = {"First Name": "given-name", "Last Name": "family-name", "Institution": "organization", "ZIP": "postal-code",
                "Email": "email", "Phone": "tel"}.get(label, "off")
        fields.append(f'<div class="fld"><input class="fld-in" id="{fid}" name="{slug(label)}" type="{kind}" placeholder=" " autocomplete="{auto}"{r}>'
                      f'<label class="fld-label" for="{fid}">{escape(label)}{star}</label></div>')
note = P.fig_lines(FORM["note"])[0]
note_html = f'<p class="cu-note"><span class="req">{escape(note[0][0].strip())}</span> {escape(note[1][0])}</p>'
qx, qy = box(FORM["q"])[:2]
yes_x = box(FORM["yes"][0])[0]
sbx, sby, sbw, sbh = box(FORM["submit"])
FORM_HTML = (f'<form class="cu-form" id="contact-form" action="#contact-form" method="post">'
             f'<div class="cu-form-head"><p class="cu-form-intro">{plain(FORM["intro"])}</p>{note_html}</div>'
             f'<div class="cu-fields">{"".join(fields)}</div>'
             f'<fieldset class="cu-radio"><legend class="cu-q">{plain(FORM["q"])}</legend>'
             f'<label class="cu-opt"><input type="radio" name="uses_products" value="yes">{plain(FORM["yes"][1])}</label>'
             f'<label class="cu-opt"><input type="radio" name="uses_products" value="no">{plain(FORM["no"][1])}</label></fieldset>'
             f'<button class="cu-submit" type="submit">{plain(FORM["submit_text"])}</button></form>')
INTRO_HTML = (f'<section class="rs cu" id="contact-intro"><div class="fx"><h1 class="cu-h1">{plain(INTRO["h1"])}</h1>'
              f'<div class="cu-panel"><div class="cu-copy"><h2 class="cu-h2">{plain(INTRO["h2"])}</h2><div class="cu-body">{body_html}</div></div>'
              f'<aside class="cu-card" aria-labelledby="cu-card-h"><h2 class="cu-card-h" id="cu-card-h">{plain(INTRO["card_h"])}</h2>{card_html}</aside></div>'
              f'{FORM_HTML}</div></section>')

css.add(".cu-h1", f"font-family: {FR}; font-weight: 400; color: {BLUE}; text-transform: uppercase;")
# 1:3915: #77DCFF → white at 25% opacity, from the top-left corner towards (31%, 69%) of the box
css.add(".cu-panel", f"background: {grad('1:3915')}, {grad('1:3914')}, #FFFFFF;")  # sky layer over the grey layer (both 25%)
css.add(".cu-h2", f"font-family: {FR}; font-weight: 400; color: {BLUE};")
css.add(".cu-p", f"font-family: {OS}; font-weight: 300; color: {INK};")
css.add(".cu-p strong", "font-weight: 700;")
css.add(".cu-link", f"color: {BLUE};")
css.add(".cu-card", "box-sizing: border-box; background: rgba(217, 217, 217, 0.1); box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.1);")
css.add(".cu-card-h", f"font-family: {FR}; font-weight: 400; color: {BLUE};")
css.add(".cu-card-block", f"font-family: {FR}; font-weight: 400; color: {INK};")
css.add(".cu-form", "box-sizing: border-box; box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.1);")
css.add(".cu-form-head", "display: flex; justify-content: space-between; align-items: flex-start;")
css.add(".cu-form-intro", f"font-family: {OS}; font-weight: 400; color: {INK};")
css.add(".cu-note", f"font-family: {OS}; font-weight: 400; font-style: italic; color: #000000;")
css.add(".req", "color: #FF4346;")
css.add(".fld", "position: relative;")
css.add(".fld-in", f"display: block; box-sizing: border-box; width: 100%; height: 40px; margin: 0; padding: 0 16px; background: #FFFFFF; border: 1px solid rgba(0, 0, 0, 0.1); border-radius: 5px; box-shadow: inset 2px 2px 3.5px rgba(0, 0, 0, 0.2); font-family: {OS}; font-weight: 400; font-size: 14px; color: {INK};")
css.add(".fld-label", f"position: absolute; left: 16px; top: 5px; font-family: {OS}; font-weight: 400; font-size: 14px; line-height: 30px; color: #ADADAD; pointer-events: none;")
css.add(".fld-in:not(:placeholder-shown) + .fld-label", "display: none;")
css.add(".fld--select .fld-in", 'appearance: none; -webkit-appearance: none; border-color: #BEBEBE; box-shadow: none; color: #ADADAD; background: #FFFFFF url("../figma/images/icon-select-caret.svg") no-repeat right 0 center / 42px 40px; cursor: pointer;')
css.add(".fld-in:focus-visible, .cu-opt input:focus-visible", f"outline: 2px solid {SKY}; outline-offset: 1px;")
css.add(".cu-radio", "display: flex; align-items: center; margin: 0; padding: 0; border: 0; min-width: 0;")
css.add(".cu-q", f"float: left; padding: 0; font-family: {OS}; font-weight: 400; font-size: 14px; color: {INK};")
css.add(".cu-opt", f"display: inline-flex; align-items: center; font-family: {OS}; font-weight: 400; font-size: 14px; color: {INK}; cursor: pointer;")
css.add(".cu-opt input", "appearance: none; -webkit-appearance: none; margin: 0; border-radius: 50%; background: #FFFFFF; cursor: pointer;")
css.add(".cu-opt input:checked", f"background: radial-gradient(circle, {BLUE} 0 35%, #FFFFFF 40%);")
css.add(".cu-submit", f"border: 0; border-radius: 5px; background: {BLUE}; color: #FFFFFF; font-family: {FR}; font-weight: 400; font-size: 16px; cursor: pointer;")
# desktop
css.add(".cu > .fx", f"padding: {u(h1y - 161)} 0 {u(y(FAQ['h2']) - fby - fbh)} {u(px)};", D)
css.add(".cu-h1", f"margin-left: {u(h1x - px)}; font-size: {u(45)}; line-height: {u(70)}; min-height: {u(py - h1y)};", D)
css.add(".cu-panel", f"display: flex; align-items: flex-start; width: {u(1243)}; height: {u(ph)}; border-radius: {u(20)}; box-sizing: border-box;", D)
css.add(".cu-copy", f"margin: {u(h2y - py)} 0 0 {u(h2x - px)}; width: {u(h2w)};", D)
css.add(".cu-h2", f"font-size: {u(40)}; line-height: {u(55)}; min-height: {u(by_ - h2y)};", D)
css.add(".cu-body", f"width: {u(bw_)};", D)
css.add(".cu-p", f"font-size: {u(16)}; line-height: {u(26)};", D)
css.add(".cu-p + .cu-p", f"margin-top: {u(26)};", D)
css.add(".cu-card", f"margin: {u(cy - py)} 0 0 {u(cx - h2x - h2w)}; width: {u(cw)}; height: {u(ch)}; padding: {u(chy - cy)} 0 0 {u(chx - cx)}; border-radius: {u(15)};", D)
css.add(".cu-card-h", f"font-size: {u(20)}; line-height: {u(38)}; min-height: {u(y(INTRO['card_lines'][0]) - chy)};", D)
css.add(".cu-card-block", f"font-size: {u(16)};", D)
css.add(".cu-card-reach", f"min-height: {u(y(INTRO['card_lines'][1]) - y(INTRO['card_lines'][0]))};", D)
css.add(".cu-card-hours", f"min-height: {u(y(INTRO['card_lines'][2]) - y(INTRO['card_lines'][1]))};", D)
css.add(".cu-form", f"margin-left: {u(fbx - px)}; width: {u(fbw)}; min-height: {u(fbh)}; padding: {u(y(FORM['intro']) - fby)} {u(15)} {u(fby + fbh - sby - sbh)} {u(f0[0] - fbx)}; border-radius: {u(15)};", D)
css.add(".cu-form-head", f"margin-left: {u(box(FORM['intro'])[0] - f0[0])}; min-height: {u(f0[1] - y(FORM['intro']))};", D)
css.add(".cu-form-intro", f"font-size: {u(16)}; line-height: {u(30)};", D)
css.add(".cu-note", f"margin-top: {u(y(FORM['note']) - y(FORM['intro']))}; width: {u(170)}; font-size: {u(14)}; line-height: {u(30)};", D)
css.add(".cu-fields", f"display: flex; flex-direction: column; gap: {u(20)}; width: {u(f0[2])};", D)
css.add(".fld-in", f"height: {u(40)}; padding: 0 {u(16)}; font-size: {u(14)};", D)
css.add(".fld-label", f"left: {u(16)}; top: {u(5)}; font-size: {u(14)}; line-height: {u(30)};", D)
css.add(".fld--select .fld-in", f"background-size: {u(42)} {u(40)};", D)
css.add(".cu-radio", f"margin: {u(y(FORM['yes'][1]) - f0[1] - 9 * 40 - 8 * 20)} 0 0 {u(qx - f0[0])}; height: {u(30)};", D)
css.add(".cu-q", f"width: {u(yes_x - qx)}; line-height: {u(20)};", D)
css.add(".cu-opt", f"gap: {u(8)}; width: {u(box(FORM['no'][0])[0] - yes_x)}; line-height: {u(30)};", D)
css.add(".cu-opt input", f"width: {u(26)}; height: {u(26)}; box-shadow: inset {u(2)} {u(1)} {u(6)} rgba(0, 0, 0, 0.25);", D)
css.add(".cu-submit", f"margin: {u(sby - y(FORM['yes'][1]) - 30)} 0 0 {u(sbx - f0[0])}; width: {u(sbw)}; height: {u(sbh)}; line-height: {u(40)};", D)
# mobile (1:1038: h1, panel p32 gap32 [h2, body, card], form p14 gap36 directly under the panel)
css.add(".cu > .fx", "gap: 36px;", M)
css.add(".cu-h1", "font-size: 36px; line-height: 41.4px; margin-bottom: 0;", M)
css.add(".cu-panel", "display: flex; flex-direction: column; gap: 32px; padding: 32px; border-radius: 20px;", M)
css.add(".cu-h2", "font-size: 32px; line-height: 42.56px; margin-bottom: 32px;", M)
css.add(".cu-p", "font-size: 14px; line-height: 24px;", M)
css.add(".cu-p + .cu-p", "margin-top: 24px;", M)
css.add(".cu-card", "height: 310px; padding: 16px 0 0 24.5px; border-radius: 15px;", M)
css.add(".cu-card-h", "font-size: 18px; line-height: 38px; min-height: 52px;", M)
css.add(".cu-card-block", "font-size: 14px;", M)
css.add(".cu-card-reach", "min-height: 107px;", M)
css.add(".cu-card-hours", "min-height: 66px;", M)
css.add(".cu-form", "display: flex; flex-direction: column; gap: 36px; margin-top: -36px; padding: 14px; border-radius: 15px;", M)
css.add(".cu-form-head", "gap: 19px;", M)
css.add(".cu-form-intro", "width: 211px; font-size: 14px; line-height: 19.07px;", M)
css.add(".cu-note", "font-size: 12px; line-height: 30px; white-space: nowrap;", M)
css.add(".cu-fields", "display: flex; flex-direction: column; gap: 26px;", M)
css.add(".cu-radio", "flex-wrap: wrap; gap: 24px 15px;", M)
css.add(".cu-q", "width: 100%; line-height: 12.66px;", M)
css.add(".cu-opt", "gap: 5px; line-height: 18.99px;", M)
css.add(".cu-opt input", "width: 16.46px; height: 16.46px; box-shadow: inset 1.27px 0.63px 3.8px rgba(0, 0, 0, 0.25);", M)
css.add(".cu-submit", "align-self: flex-start; padding: 9px 26px; line-height: 21.28px;", M)
for lh in (20, 26, 30, 32):
    css.add(f".cu-card .lh{lh}", f"line-height: {u(lh)};", D)
    css.add(f".cu-card .lh{lh}", f"line-height: {lh}px;", M)
css.add(".cu-card .ln", "margin: 0;")

# ================================================================ FAQ (desktop y 1581..2988)
fh2x, fh2y = box(FAQ["h2"])[:2]
items = []
for i, (rect, q) in enumerate(FAQ["items"]):
    qtext = plain(q)
    if i == FAQ["open_index"]:
        ans = f'<div class="faq-a"><p>{rich(FAQ["answer"])}</p></div>'
        items.append(f'<details class="faq" open><summary class="faq-q">{qtext}<span class="faq-chev" aria-hidden="true"></span></summary>{ans}</details>')
    else:  # Figma draws only this one answer; the others are closed with no copy (not invented)
        items.append(f'<details class="faq"><summary class="faq-q">{qtext}<span class="faq-chev" aria-hidden="true"></span></summary></details>')
it0 = box(FAQ["items"][0][0])
it1 = box(FAQ["items"][1][0])
itl = box(FAQ["items"][-1][0])
apx, apy, apw, aph = box(FAQ["answer_panel"])
fbtn = box(FAQ["button"])
fline = box(FAQ["line"])
FAQ_HTML = (f'<section class="rs faqs" id="faq"><div class="fx"><h2 class="faq-h2">{plain(FAQ["h2"])}</h2><div class="faq-list">{"".join(items)}</div>'
            f'<a class="faq-btn d-only" href="#contact-form">{plain(FAQ["button_text"])}</a><hr class="faq-rule"></div></section>')
CHEV_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="22" height="12" viewBox="0 0 22 12" fill="none" stroke="#000000" stroke-width="3" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="M2 2l9 8 9-8"/></svg>')
CHEV_UP_SVG = CHEV_SVG.replace("#000000", BLUE).replace("M2 2l9 8 9-8", "M2 10l9-8 9 8")
css.add(".faq-h2", f"margin: 0; font-family: {FR}; font-weight: 400; color: {BLUE};")
css.add(".faq", f"box-sizing: border-box; background: {grad('1:3918')}, #FFFFFF;")
css.add(".faq[open]", f"background: {grad('1:3921')}, #FFFFFF;")
css.add(".faq-q", f"display: flex; align-items: center; justify-content: space-between; list-style: none; cursor: pointer; font-family: {OS}; font-weight: 400; color: {INK};")
css.add(".faq-q::-webkit-details-marker", "display: none;")
css.add(".faq-chev", 'flex: none; background: url("../figma/images/icon-chevron-down.svg") no-repeat center / contain;')
css.add(".faq[open] .faq-chev", 'background-image: url("../figma/images/icon-chevron-up.svg");')
css.add(".faq-a", "background: #FFFFFF;")
css.add(".faq-a p", f"margin: 0; font-family: {OS}; font-weight: 300; color: #000000;")
css.add(".faq-a strong, .faq-a a", "font-weight: 700;")
css.add(".faq-a a", f"color: {BLUE}; text-decoration: underline;")
css.add(".faq-btn", f"display: flex; align-items: center; justify-content: center; box-sizing: border-box; border-radius: 5px; background: {BLUE}; color: #FFFFFF; font-family: {FR}; font-weight: 400;")
css.add(".faq-rule", f"margin: 0; border: 0; border-top: 1px solid {BLUE};")
css.add(".faqs > .fx", f"padding: 0 0 {u(y(BOTTOM['h2']) - fline[1] - 1)} {u(fh2x)};", D)
css.add(".faq-h2", f"font-size: {u(32)}; line-height: {u(55)}; min-height: {u(it0[1] - fh2y)};", D)
css.add(".faq-list", f"display: flex; flex-direction: column; gap: {u(it1[1] - it0[1] - it0[3])}; width: {u(it0[2])};", D)
css.add(".faq", f"min-height: {u(it0[3])}; border-radius: {u(12)};", D)
css.add(".faq-q", f"height: {u(it0[3])}; padding: 0 {u(it0[0] + it0[2] - 1251)} 0 {u(box(FAQ['items'][0][1])[0] - it0[0])}; box-sizing: border-box; font-size: {u(20)}; line-height: {u(40)};", D)
css.add(".faq[open] .faq-q", f"height: {u(apy - it1[1])};", D)
css.add(".faq-chev", f"width: {u(22)}; height: {u(12)};", D)
css.add(".faq-a", f"margin: 0 {u(it1[0] + it1[2] - apx - apw)} {u(it1[1] + it1[3] - apy - aph)} {u(apx - it1[0])}; min-height: {u(aph)}; padding: {u(y(FAQ['answer']) - apy)} 0 0 {u(box(FAQ['answer'])[0] - apx)}; border-radius: {u(10)}; box-sizing: border-box;", D)
css.add(".faq-a p", f"width: {u(box(FAQ['answer'])[2])}; font-size: {u(18)}; line-height: {u(32)};", D)
css.add(".faq-btn", f"margin-top: {u(fbtn[1] - itl[1] - itl[3])}; width: {u(fbtn[2])}; height: {u(fbtn[3])}; font-size: {u(16)};", D)
css.add(".faq-rule", f"margin-top: {u(fline[1] - fbtn[1] - fbtn[3])}; width: {u(fline[2])};", D)
# mobile 1:1094: list gap 12; rows #EEEEEE r8 p20/14; open #E6F8FE with a white answer panel r8 p20/14; no button; sky rule
css.add(".faqs > .fx", "padding-bottom: 0;", M)
css.add(".faq-h2", "font-size: 32px; line-height: 42.56px;", M)
css.add(".faq-list", "display: flex; flex-direction: column; gap: 12px;", M)
css.add(".faq", "background: #EEEEEE; border-radius: 8px;", M)
css.add(".faq[open]", "background: #E6F8FE; padding-bottom: 20px;", M)
css.add(".faq-q", "padding: 20px 14px; gap: 10px; font-size: 14px; line-height: 19.07px;", M)
css.add(".faq[open] .faq-q", "padding-bottom: 10px;", M)
css.add(".faq-chev", "width: 13px; height: 8px;", M)
css.add(".faq-a", "margin: 0 14px; padding: 20px 14px; border-radius: 8px;", M)
css.add(".faq-a p", "font-size: 14px; line-height: 24px;", M)
css.add(".faq-rule", f"margin: 8px -20px 0; border-top-color: {SKY};", M)

# ================================================================ bottom links (desktop y 2988..3245)
bh_y = y(BOTTOM["h2"])
b0 = box(BOTTOM["buttons"][0][0])
btns = "".join(f'<a class="bl-btn bl-btn--{i + 1}" href="#bottom-link-{i + 1}">{plain(t)}</a>' for i, (_, t) in enumerate(BOTTOM["buttons"]))
BOTTOM_HTML = (f'<section class="rs bl" id="before-you-go"><div class="fx"><h2 class="bl-h2">{plain(BOTTOM["h2"])}</h2>'
               f'<div class="bl-btns">{btns}</div></div></section>')
css.add(".bl-h2", f"margin: 0; font-family: {FR}; font-weight: 400; color: {BLUE}; text-align: center; text-transform: uppercase;")
css.add(".bl-btn", f"display: flex; align-items: center; justify-content: center; box-sizing: border-box; font-family: {FR}; font-weight: 400; text-align: center;")
css.add(".bl-btn--1", f"background: {BLUE}; color: #FFFFFF;")
css.add(".bl-btn--2", f"color: {SKY};")
css.add(".bl-btn--3", f"color: {BLUE};")
css.add(".bl > .fx", f"padding-bottom: {u(3245 - b0[1] - b0[3])};", D)
css.add(".bl-h2", f"font-size: {u(34)}; line-height: {u(50)}; min-height: {u(b0[1] - bh_y)};", D)
css.add(".bl-btns", f"display: flex; justify-content: center; gap: {u(13)};", D)
css.add(".bl-btn", f"height: {u(50)}; border-radius: {u(5)}; font-size: {u(18)}; line-height: {u(50)};", D)
for i, (bx, _) in enumerate(BOTTOM["buttons"]):
    css.add(f".bl-btn--{i + 1}", f"width: {u(box(bx)[2])};", D)
css.add(".bl-btn--2, .bl-btn--3", f"border: 2px solid {SKY};", D)
css.add(".bl-h2", "font-size: 24px; line-height: 31.92px;", M)
css.add(".bl-btns", "display: flex; flex-direction: column; gap: 12px;", M)
css.add(".bl-btn", "height: 50px; border-radius: 5px; font-size: 16px; line-height: 21.28px; padding: 0 20px;", M)
css.add(".bl-btn--2, .bl-btn--3", f"border: 1px solid {SKY};", M)
css.add(".cu > .fx, .faqs > .fx, .bl > .fx", "max-width: 640px; margin: 0 auto; box-sizing: border-box;", M)
P.shift_css(css, u, D, M)

# ================================================================ blueprint + compile
NOTE = ("2026-09-28 Contact Us replica (HTML first; the Elementor build follows developer review). Figma 1:3891 desktop / 1:1027 mobile. "
        "Generated by tools/figma_html/build_contact.py; copy from pages/_figma/file.json by node id.")
SECTIONS = [
    {"id": "site-header", "landmark": "header", "escape_hatch": True, "html": HEAD_HTML, "css": SHARED + HEADER_CSS, "js": HEADER_JS},
    {"id": "contact-intro", "escape_hatch": True, "heading_level": 1, "html": INTRO_HTML, "css": css.render()},
    {"id": "faq", "escape_hatch": True, "html": FAQ_HTML, "css": ""},
    {"id": "before-you-go", "escape_hatch": True, "html": BOTTOM_HTML, "css": ""},
    {"id": "site-footer", "landmark": "footer", "escape_hatch": True, "html": FOOT_HTML, "css": FOOT_CSS},
]
for s in SECTIONS:
    s["notes"] = [NOTE]
    s["html"] = link_pages(s["html"])
bp = {"page": SLUG,
      "meta": {"title": "Contact Us | Mizuho America",
               "description": "Contact Mizuho America: product demos, service and technical support, and answers to frequently asked questions."},
      "css_workflow": "scss", "font_source": "google",
      "notes_for_developer": ["Only FAQ 2 has an answer in Figma; the other 8 render closed with no copy (to be written by the client).",
                              "Figma's FAQ answer gives 888-699-2547 while Site Settings / header / footer say 800-699-2547: kept as drawn, flagged."],
      "sections": SECTIONS}
compile_page(SLUG, bp, extra_images=("logo-mizuho-header-srgb.png", "logo-mizuho-footer-reversed.png"),
             svgs={"icon-select-caret.svg": CARET_SVG.replace('height="30" viewBox="0 0 38 30"', 'height="40" viewBox="0 0 42 40"')
                   .replace('height="30"/>', 'height="40"/>').replace("M13 10h13l-6.5 10z", "M15 15h13l-6.5 10z"),
                   "icon-chevron-down.svg": CHEV_SVG, "icon-chevron-up.svg": CHEV_UP_SVG})
