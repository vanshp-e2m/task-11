"""Blueprint patch: static header + footer (landmark sections) and an exact-geometry value-columns section.

Every number is Figma geometry at 1440 (frame 1:9): header group 1:117, value columns 1:31, footer 1:132.
The header/footer here exist only so the static HTML replica is complete; on WordPress they are the Elementor Theme
Builder templates. Edits blueprint.json only; compile with run_devcommand_compiler.py afterwards.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BP = os.path.join(ROOT, "pages", "mizuho-home", "blueprint.json")
IMG = "figma/images"

HEADER_HTML = f"""<header class="site-head" id="site-header">
  <div class="site-head__inner">
    <div class="site-head__row1">
      <nav class="site-head__lang" aria-label="Language"><ul><li><a class="is-current" href="#en" hreflang="en">EN</a></li><li><a href="#esp" hreflang="es">ESP</a></li></ul></nav>
      <a class="site-head__logo" href="#top"><img src="{IMG}/logo-mizuho-header-srgb.png" alt="Mizuho America" width="200" height="61"></a>
      <a class="site-head__account" href="#find-an-account-manager">Find an Account Manager</a>
      <button class="site-head__toggle" type="button" aria-expanded="false" aria-controls="site-primary-nav" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
    <div class="site-head__row2">
      <nav class="site-head__nav" id="site-primary-nav" aria-label="Primary"><ul><li><a href="#products">Products</a></li><li><a href="#about-mizuho-america">About Mizuho America</a></li><li><a href="#clinical-resources">Clinical Resources</a></li><li><a href="#contact-support">Contact &amp; Support</a></li></ul></nav>
      <div class="site-head__actions">
        <form class="site-head__search" role="search" action="#search"><label class="visually-hidden" for="site-search">Search</label><input id="site-search" type="search" placeholder="Search..."></form>
        <a class="site-head__btn site-head__btn--portal" href="#sales-portal">Sales Portal</a>
        <a class="site-head__btn site-head__btn--contact" href="#contact-us">Contact Us</a>
      </div>
    </div>
    <div class="site-head__row3"><a class="site-head__phone" href="tel:8006992547">800-699-2547</a></div>
  </div>
</header>"""

# 1:117 — row1 = logo box y24..85; row2 = buttons y84..113; phone y125 (13/17.7). Right visual edge 1414.
HEADER_CSS = """
.visually-hidden { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.site-head { position: relative; background: #FFFFFF; }
.site-head__inner { max-width: 1440px; margin: 0 auto; padding: 24px 26px 0 24px; box-sizing: border-box; height: 161px; }
.site-head a { color: #000000; text-decoration: none; }
.site-head__row1 { display: grid; grid-template-columns: 589px 200px 1fr; height: 61px; }
.site-head ul, .site-foot__legal ul { display: flex; margin: 0; padding: 0; list-style: none; }
.site-head__lang ul { gap: 24px; }
.site-head__nav ul { gap: 24px; }
.site-foot__legal ul { gap: 26px; }
.site-head__lang { display: flex; gap: 24px; padding-top: 14px; font-family: 'Montserrat', sans-serif; font-weight: 500; font-size: 0.8125rem; line-height: 0.975rem; }
.site-head__lang a { padding-left: 2px; }
.site-head__lang a.is-current { padding-left: 0; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 3px; }
.site-head__logo img { display: block; width: 200px; height: 61px; }
.site-head__account { justify-self: end; align-self: start; margin-top: 16px; font-family: 'Montserrat', sans-serif; font-weight: 500; font-size: 0.8125rem; line-height: 0.975rem; }
.site-head__row2 { display: flex; align-items: center; justify-content: space-between; height: 29px; margin-top: -1px; }
.site-head__nav { display: flex; gap: 24px; padding-left: 37px; font-family: 'Open Sans', sans-serif; font-weight: 600; font-size: 0.8125rem; line-height: 1.10625rem; }
.site-head__actions { display: flex; align-items: center; }
.site-head__search input { width: 161px; height: 29px; box-sizing: border-box; border: 0; border-radius: 5px; background: rgba(0, 179, 240, 0.2); padding: 0 12px; font-family: 'Open Sans', sans-serif; font-weight: 700; font-size: 0.8125rem; color: #000000; }
.site-head__search input::placeholder { color: #000000; opacity: 1; }
.site-head__btn { display: inline-flex; align-items: center; justify-content: center; height: 29px; box-sizing: border-box; border-radius: 5px; font-family: 'Open Sans', sans-serif; font-weight: 700; font-size: 0.8125rem; }
.site-head__btn--portal { width: 117px; margin-left: 10px; background: #0065B3; color: #FFFFFF !important; }
.site-head__btn--contact { width: 109px; margin-left: 11px; border: 2px solid #00B3F0; color: #00B3F0 !important; }
.site-head__toggle { display: none; flex-direction: column; justify-content: center; gap: 4px; width: 29px; height: 29px; padding: 5px; border: 0; background: none; cursor: pointer; justify-self: end; }
.site-head__toggle span { display: block; height: 2px; background: #000000; transition: transform .2s ease, opacity .2s ease; }
.site-head__toggle[aria-expanded="true" i] span:nth-child(1) { transform: translateY(6px) rotate(45deg); }
.site-head__toggle[aria-expanded="true" i] span:nth-child(2) { opacity: 0; }
.site-head__toggle[aria-expanded="true" i] span:nth-child(3) { transform: translateY(-6px) rotate(-45deg); }
body.nav-open { overflow: hidden; }
@media (max-width: 1024px) {
  .site-head__toggle { display: inline-flex; position: relative; z-index: 30; }
  /* Off-canvas drawer (Figma has no open-menu design). Full responsive pass comes later. */
  .site-head__nav { position: fixed; inset: 0; z-index: 25; padding: 96px 20px 20px; background: #FFFFFF; transform: translateX(100%); transition: transform .3s ease; }
  .site-head__nav.is-open { transform: translateX(0); }
  .site-head__nav ul { flex-direction: column; gap: 16px; }
}
.site-head__row3 { display: flex; justify-content: flex-end; margin-top: 12px; }
.site-head__phone { font-family: 'Open Sans', sans-serif; font-weight: 700; font-size: 0.8125rem; line-height: 1.10625rem; }
"""

CARDS = [
    ("Surgeon-centric", "value-icon-surgeon-centric.png", 100, 98, "Products designed exclusively<br>for neurosurgeons",
     "With an expansive portfolio of instruments available individually and in convenient, timesaving sets and kits, we are committed to helping you optimize precision, efficiency, and workflow in the OR"),
    ("Consistent quality", "value-icon-consistent-quality.png", 99, 90, "Handcrafted tools for exceptional quality, performance and longevity",
     "Our tools are produced with the utmost care and integrity, adhering to stringent manufacturing protocols, so you can confidently rely on them for your delicate, high-stakes procedures"),
    ("Notable names", "value-icon-notable-names.png", 100, 84, "Longstanding collaborations with renowned neurosurgeons",
     "We’ve become a global leader in the field of neurosurgical tools through our ongoing work with clinical experts to help identify and fill unmet needs in the OR"),
    ("Personal partnership", "value-icon-personal-partnership.png", 100, 72, "Supporting you before, during,<br>and after the sale",
     "We not only stand behind our high-quality products; we stand with you to ensure your questions are answered, your needs are met, and your input and insights are heard"),
]


def card(i, c):
    title, icon, w, h, lead, body = c
    return (f'<article class="value-columns__card value-columns__card--{i}"><h3 class="value-columns__title">{title}</h3>'
            f'<div class="value-columns__icon"><img src="{IMG}/{icon}" alt="" width="{w}" height="{h}" loading="lazy"></div>'
            f'<div class="value-columns__text"><p class="value-columns__lead">{lead}</p><p class="value-columns__body">{body}</p></div></article>')


VC_HTML = ('<section class="value-columns" id="value-columns"><div class="value-columns__inner"><div class="value-columns__grid">'
           + "".join(card(i + 1, c) for i, c in enumerate(CARDS))
           + '</div><a class="value-columns__button" href="#downloadable-brochures">Check out our downloadable brochures</a></div></section>')

# 1:31 — group x107..1346, dividers x400/715/1030 (h470), card text x114/430.7/744.7/1060 (+13.3 text inset on card 4),
# title box h50 (24/31.92), icon at y54, text at y177, 16/30; button 293x50 r5 at y531, label inset 20px.
# Section padding: intro divider (y1492) → group top (y1590) = 98; group bottom (2172) → procedure band (2265) = 93.
VC_CSS = """
/* DevCommand's compiler requests Open Sans without the italic axis (issue #26), so the lead lines would be a synthesised, wider oblique. */
@font-face { font-family: 'Open Sans'; font-style: italic; font-weight: 600; font-stretch: 100%; font-display: swap; src: url(https://fonts.gstatic.com/s/opensans/v44/memQYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWq8tWZ0Pw86hd0RkxhjWVAewA.woff2) format('woff2'); unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }
.value-columns { background: #FFFFFF; padding: 98px 0 93px; }
.value-columns__inner { max-width: 1440px; margin: 0 auto; padding-left: 107px; box-sizing: border-box; }
.value-columns__grid { display: grid; grid-template-columns: 293px 315px 315px 316px; }
.value-columns__card { min-height: 470px; box-sizing: border-box; padding-top: 4px; }
.value-columns__card--1 { padding-left: 7px; padding-right: 33px; }
.value-columns__card--2 { border-left: 1px solid #00B3F0; padding-left: 29.7px; padding-right: 25px; }
.value-columns__card--3 { border-left: 1px solid #00B3F0; padding-left: 28.7px; padding-right: 26px; }
.value-columns__card--4 { border-left: 1px solid #00B3F0; padding-left: 29px; }
.value-columns__card--4 .value-columns__text { padding-left: 13.3px; width: 272.6px; } /* border-box: 13.3 inset + Figma's 259.3 text box */
.value-columns__title { margin: 0; height: 50px; font-family: 'Freeman', sans-serif; font-weight: 400; font-size: 1.5rem; line-height: 1.995rem; text-transform: uppercase; color: #00B3F0; white-space: nowrap; }
.value-columns__icon { height: 123px; }
.value-columns__icon img { display: block; object-fit: cover; }
.value-columns__lead, .value-columns__body { margin: 0; font-family: 'Open Sans', sans-serif; font-size: 1rem; line-height: 1.875rem; color: #090909; }
.value-columns__lead { font-weight: 600; font-style: italic; margin-bottom: 30px; }
.value-columns__body { font-weight: 300; }
.value-columns__button { display: inline-flex; align-items: center; width: 293px; height: 50px; margin-top: 61px; padding-left: 20px; box-sizing: border-box; border-radius: 5px; background: #0065B3; color: #FFFFFF; font-family: 'Freeman', sans-serif; font-weight: 400; font-size: 1rem; line-height: 2.5rem; text-decoration: none; }
"""

MENU = [
    ("Products", ["By Procedure", "By Category", "Head Holding Systems", "Instruments", "Surgical Tables", "Vascular Management"], 375),
    ("Clinical", ["Videos", "Clinical Case Studies", "Events"], 341),
    ("Company", ["About Mizuho", "Careers"], 287),
    ("Support", ["Find an Account Manager", "Contact Us", "Technical Support", "Customer Service", "FAQs", "Sale Hub"], None),
]


def slug(s):
    return "#" + "".join(ch.lower() if ch.isalnum() else "-" for ch in s).strip("-")


FOOTER_HTML = (
    '<footer class="site-foot" id="site-footer"><div class="site-foot__inner">'
    '<div class="site-foot__contact"><h2 class="site-foot__heading">Contact &amp; Support</h2>'
    '<p class="site-foot__intro">Interested in a product demo? Have any questions? Want to chat? <a href="#contact-us"><strong>Contact Us.</strong></a></p>'
    '<p class="site-foot__hours">Hours: Monday-Friday: 6:30 am–5:00 pm (PST)</p></div>'
    '<div class="site-foot__reach"><p class="site-foot__reach-label">Additional ways to reach us:</p>'
    '<p class="site-foot__strong"><a href="tel:8006992547">Phone: 800-699-2547</a></p>'
    '<p class="site-foot__strong">Fax: 510-324-4545</p>'
    '<p class="site-foot__strong"><a href="mailto:customerservice@mizuho.com">Email: customerservice@mizuho.com</a></p>'
    '<p>Address: 30057 Ahem Avenue, Union City, CA 94587</p></div>'
    '<hr class="site-foot__rule"><div class="site-foot__menus">'
    + "".join(
        f'<nav class="site-foot__col" aria-label="{h}"><h3>{h}</h3><ul>' + "".join(f'<li><a href="{slug(l)}">{l}</a></li>' for l in links) + "</ul></nav>"
        for h, links, _ in MENU
    )
    + '</div><div class="site-foot__bottom"><img class="site-foot__logo" src="figma/images/logo-mizuho-footer-reversed.png" alt="Mizuho America" width="200" height="58" loading="lazy">'
    '<p class="site-foot__copy">© 2026 Mizuho America, Inc. All rights reserved.</p>'
    '<nav class="site-foot__legal" aria-label="Legal"><ul><li><a href="#privacy-policy">Privacy Policy</a></li><li><a href="#terms-of-use">Terms of Use</a></li><li><a href="#cookie-policy">Cookie Policy</a></li><li><a href="#accessibility">Accessibility</a></li></ul></nav>'
    "</div></div></footer>"
)

# 1:132 — bg #0065B3 1440x960. Heading y+70 (Fraunces 700 34/50) x78; intro 20/40, hours 20/30; reach block y+221 (25/40);
# rule y+480 x79..1358; menus y+531 at x78/453/794/1081 (heading 700 25/50, links 300 20/40);
# bottom: logo 200x58 x44 y+866; copyright x256 y+890 (14/40); legal x961 y+890, right edge ~1405.
FOOTER_CSS = """
/* Figma's "Contact & Support" uses Fraunces' decorative ampersand = the WONK alternate, which exists only in the full-axis
   variable file and only from ~opsz 34 (tested opsz 9/34/144 x WONK 0/1: opsz 34 + WONK 1 = 315px, Figma ink 313px, same glyph).
   DevCommand's compiler requests Fraunces by weight axis only (issue #26), so the full-axis file is declared here. */
@font-face { font-family: 'Fraunces Full'; font-style: normal; font-weight: 100 900; font-display: swap; src: url(https://fonts.gstatic.com/s/fraunces/v38/6NUI8FyLNQOQZAnv9bYEvBjUVG5Ga92uVSQO8Uik.woff2) format('woff2'); unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+2000-206F; }
.site-foot { background: #0065B3; color: #FFFFFF; }
.site-foot__inner { max-width: 1440px; height: 960px; margin: 0 auto; padding: 70px 82px 0 78px; box-sizing: border-box; font-family: 'Montserrat', sans-serif; font-weight: 300; }
.site-foot a { color: #FFFFFF; text-decoration: none; }
.site-foot p { margin: 0; }
.site-foot__heading { margin: 0; font-family: 'Fraunces Full', 'Fraunces', serif; font-optical-sizing: none; font-variation-settings: \"opsz\" 34, \"WONK\" 1; font-weight: 700; font-size: 2.125rem; line-height: 3.125rem; }
.site-foot__intro { font-size: 1.25rem; line-height: 2.5rem; }
.site-foot__intro strong { font-weight: 700; }
.site-foot__hours { font-size: 1.25rem; line-height: 1.875rem; }
.site-foot__reach { margin-top: 31px; padding-left: 1px; font-size: 1.5625rem; line-height: 2.5rem; }
.site-foot__strong { font-weight: 700; }
.site-foot__rule { width: 1279px; margin: 59px 0 0 1px; border: 0; border-top: 1px solid #FFFFFF; }
.site-foot__menus { display: grid; grid-template-columns: 375px 341px 287px 1fr; margin-top: 50px; }
.site-foot__col h3 { margin: 0; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 1.5625rem; line-height: 3.125rem; }
.site-foot__col ul { margin: 0; padding: 0; list-style: none; font-size: 1.25rem; line-height: 2.5rem; }
.site-foot__bottom { display: flex; align-items: flex-start; margin-top: 45px; margin-left: -34px; }
.site-foot__logo { display: block; width: 200px; height: 58px; }
.site-foot .site-foot__copy { margin: 24px 0 0 12px; font-size: 0.875rem; line-height: 2.5rem; }
.site-foot__legal { display: flex; margin: 24px -47px 0 auto; font-size: 0.875rem; line-height: 2.5rem; }
"""

bp = json.load(open(BP, encoding="utf-8"))
secs = [s for s in bp["sections"] if s["id"] not in ("site-header", "site-footer")]
for s in secs:
    if s["id"] == "value-columns":
        s["html"], s["css"] = VC_HTML, VC_CSS
        s.pop("content_source", None)
        s["notes"] = s.get("notes", []) + ["2026-09-28: rewritten as literal HTML at exact Figma 1:31 geometry (developer asked for a perfect replica). Lead lines keep Figma's hard breaks; card 4 keeps Figma's 13.3px text inset."]
HEADER_JS = """(function(){var b=document.querySelector('.site-head__toggle');if(!b)return;b.addEventListener('click',function(){var o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',String(!o));document.getElementById('site-primary-nav').classList.toggle('is-open',!o);document.body.classList.toggle('nav-open',!o);});})();"""
header = {"id": "site-header", "landmark": "header", "escape_hatch": True, "html": HEADER_HTML, "css": HEADER_CSS, "js": HEADER_JS,
          "notes": ["Static replica of Figma 1:117 for the HTML deliverable; on WordPress the header is Elementor Theme Builder template 61."]}
footer = {"id": "site-footer", "landmark": "footer", "escape_hatch": True, "html": FOOTER_HTML, "css": FOOTER_CSS,
          "notes": ["Static replica of Figma 1:132; on WordPress the footer is Elementor Theme Builder template 62."]}
bp["sections"] = [header] + secs + [footer]
json.dump(bp, open(BP, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("sections:", [s["id"] for s in bp["sections"]])
