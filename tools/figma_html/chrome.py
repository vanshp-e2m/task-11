"""Shared pieces of every public-page replica: unit helpers, fonts, resets, the header (1:117 / 1:401) and the footer
(1:132 / 1:545). Imported by build_replica.py (Home) and build_resources.py (Resources), so the chrome is defined once."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
I = "figma/images"
D = "@media (min-width: 1024px)"
M = "@media (max-width: 1023px)"


def u(n):
    return f"calc({n} * var(--u, 1px))"


def at(x, y, w=None, h=None):
    s = f"position: absolute; left: {u(x)}; top: {u(y)};"
    if w is not None:
        s += f" width: {u(w)};"
    if h is not None:
        s += f" height: {u(h)};"
    return s


def font(fam, wt, size, lh, extra=""):
    return f"font-family: {fam}; font-weight: {wt}; font-size: {u(size)}; line-height: {u(lh)};{extra}"


def mfont(fam, wt, size, lh):
    return f"font-family: {fam}; font-weight: {wt}; font-size: {size}px; line-height: {lh}px;"


FR = "'Freeman', sans-serif"
OS = "'Open Sans', sans-serif"
MO = "'Montserrat', sans-serif"
MU = "'Mukta', sans-serif"
FA = "'Fraunces Full', 'Fraunces', serif"

# ---------------------------------------------------------------- shared
SHARED = f"""
@font-face {{ font-family: 'Open Sans'; font-style: italic; font-weight: 600; font-stretch: 100%; font-display: swap; src: url(https://fonts.gstatic.com/s/opensans/v44/memQYaGs126MiZpBA-UFUIcVXSCEkx2cmqvXlWq8tWZ0Pw86hd0RkxhjWVAewA.woff2) format('woff2'); unicode-range: U+0000-00FF, U+2000-206F; }}
@font-face {{ font-family: 'Fraunces Full'; font-style: normal; font-weight: 100 900; font-display: swap; src: url(https://fonts.gstatic.com/s/fraunces/v38/6NUI8FyLNQOQZAnv9bYEvBjUVG5Ga92uVSQO8Uik.woff2) format('woff2'); unicode-range: U+0000-00FF, U+2000-206F; }}
.visually-hidden {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }}
main, .site-foot {{ container-type: inline-size; }}
.rs {{ --u: min(1px, 100cqw / 1440); position: relative; background: #FFFFFF; }}
/* zero-specificity resets, so every single-class rule below wins (issue #27) */
:where(.rs) :where(p, h1, h2, h3, blockquote, figure) {{ margin: 0; }}
:where(.rs) :where(a) {{ text-decoration: none; }}
:where(.rs) :where(img) {{ display: block; }}
:where(.rs) :where(ul) {{ margin: 0; padding: 0; list-style: none; }}
{D} {{
  .rs > .fx {{ position: relative; width: {u(1440)}; margin: 0 auto; height: 100%; }}
  .m-only {{ display: none !important; }}
}}
{M} {{
  .rs > .fx {{ display: flex; flex-direction: column; gap: 36px; padding: 44px 20px; box-sizing: border-box; }}
  .rs:not(.pb):not(.site-foot), .rs:not(.pb):not(.site-foot) > .fx {{ background: #FCFEFF; }}
  .d-only {{ display: none !important; }}
}}
"""

# ---------------------------------------------------------------- header 1:117 / 1:401
HEADER_HTML = f"""<header class="site-head rs" id="site-header"><div class="fx">
<a class="hd-logo" href="#top"><img src="{I}/logo-mizuho-header-srgb.png" alt="Mizuho America" width="200" height="61"></a>
<nav class="hd-lang" aria-label="Language"><ul><li><a class="is-current" href="#en" hreflang="en">EN</a></li><li><a href="#esp" hreflang="es">ESP</a></li></ul></nav>
<a class="hd-account" href="#find-an-account-manager">Find an Account Manager</a>
<button class="site-head__toggle" type="button" aria-expanded="false" aria-controls="site-primary-nav" aria-label="Menu"><span></span><span></span><span></span></button>
<nav class="site-head__nav" id="site-primary-nav" aria-label="Primary"><ul><li><a href="#products">Products</a></li><li><a href="#about-mizuho-america">About Mizuho America</a></li><li><a href="#clinical-resources">Clinical Resources</a></li><li><a href="#contact-support">Contact &amp; Support</a></li></ul></nav>
<form class="hd-search" role="search" action="#search"><label class="visually-hidden" for="site-search">Search</label><input id="site-search" type="search" placeholder="Search..."></form>
<a class="hd-btn hd-portal" href="#sales-portal">Sales Portal</a>
<a class="hd-btn hd-contact" href="#contact-us">Contact Us</a>
<a class="hd-phone" href="tel:8006992547">800-699-2547</a>
</div></header>"""

HEADER_CSS = f"""
.site-head a {{ color: #000000; }}
.site-head__toggle {{ display: none; flex-direction: column; justify-content: center; gap: 4px; width: 29px; height: 29px; padding: 5px; border: 0; background: none; cursor: pointer; }}
.site-head__toggle span {{ display: block; height: 2px; background: #000000; transition: transform .2s ease, opacity .2s ease; }}
.site-head__toggle[aria-expanded="true" i] span:nth-child(1) {{ transform: translateY(6px) rotate(45deg); }}
.site-head__toggle[aria-expanded="true" i] span:nth-child(2) {{ opacity: 0; }}
.site-head__toggle[aria-expanded="true" i] span:nth-child(3) {{ transform: translateY(-6px) rotate(-45deg); }}
body.nav-open {{ overflow: hidden; }}
.hd-lang ul, .site-head__nav ul {{ display: flex; }}
.hd-lang a.is-current {{ text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 4px; }}
.hd-search input {{ box-sizing: border-box; width: 100%; height: 100%; border: 0; border-radius: 5px; background: rgba(0, 179, 240, 0.2); color: #000000; }}
.hd-search input::placeholder {{ color: #000000; opacity: 1; }}
.hd-btn {{ display: flex; align-items: center; justify-content: center; box-sizing: border-box; border-radius: 5px; }}
.site-head .hd-portal {{ background: #0065B3; color: #FFFFFF; }}
.site-head .hd-contact {{ border: 2px solid #00B3F0; color: #00B3F0; }}
{D} {{
  .site-head {{ container-type: inline-size; height: {u(161)}; }}
  .hd-logo {{ {at(613, 24, 200, 61)} }}
  .hd-logo img {{ width: 100%; height: 100%; }}
  .hd-lang {{ {at(26, 38)} {font(MO, 500, 13, 15.6)} }}
  .hd-lang ul {{ gap: {u(17)}; }}
  .hd-account {{ {at(1244, 40)} {font(MO, 500, 13, 15.6)} }}
  .site-head__nav {{ {at(61, 89)} {font(OS, 600, 13, 17.7)} }}
  .site-head__nav ul {{ gap: {u(24)}; }}
  .hd-search {{ {at(1006, 84, 161, 29)} }}
  .hd-search input {{ padding: 0 {u(12)}; {font(OS, 700, 13, 17.7)} }}
  .hd-btn {{ {font(OS, 700, 13, 17.7)} }}
  .hd-portal {{ {at(1177, 84, 117, 29)} }}
  .hd-contact {{ {at(1305, 84, 109, 29)} }}
  .hd-phone {{ {at(1330, 125)} {font(OS, 700, 13, 17.7)} }}
}}
{M} {{
  .site-head > .fx {{ display: grid; grid-template-columns: 1fr auto; row-gap: 18px; gap: 18px 0; padding: 10px 20px; align-items: center; }}
  .hd-logo img {{ width: 118px; height: 31px; object-fit: cover; }}
  .site-head__toggle {{ display: inline-flex; justify-self: end; position: relative; z-index: 30; }}
  .hd-lang {{ grid-row: 2; min-height: 18px; {mfont(MO, 500, 13, 15.6)} }}
  .hd-lang ul {{ gap: 17px; }}
  .hd-account {{ grid-row: 2; justify-self: end; {mfont(MO, 500, 13, 15.6)} }}
  .hd-search, .hd-btn, .hd-phone {{ display: none; }}
  /* Off-canvas drawer (Figma has no open-menu design). */
  .site-head__nav {{ position: fixed; inset: 0; z-index: 25; padding: 96px 20px 20px; background: #FFFFFF; transform: translateX(100%); transition: transform .3s ease; {mfont(OS, 600, 18, 28)} }}
  .site-head__nav.is-open {{ transform: translateX(0); }}
  .site-head__nav ul {{ flex-direction: column; gap: 16px; }}
}}
"""
HEADER_JS = """(function(){var b=document.querySelector('.site-head__toggle');if(!b)return;b.addEventListener('click',function(){var o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',String(!o));document.getElementById('site-primary-nav').classList.toggle('is-open',!o);document.body.classList.toggle('nav-open',!o);});})();"""


# ---------------------------------------------------------------- footer 1:132 / 1:545   (h=960)
MENU = [("Products", ["By Procedure", "By Category", "Head Holding Systems", "Instruments", "Surgical Tables", "Vascular Management"]),
        ("Clinical", ["Videos", "Clinical Case Studies", "Events"]),
        ("Company", ["About Mizuho", "Careers"]),
        ("Support", ["Find an Account Manager", "Contact Us", "Technical Support", "Customer Service", "FAQs", "Sale Hub"])]


def slug(s):
    return "#" + "".join(ch.lower() if ch.isalnum() else "-" for ch in s).strip("-")


FOOT_HTML = ('<footer class="site-foot rs" id="site-footer"><div class="fx">'
             '<div class="ft-contact"><h2 class="ft-h2">Contact &amp; Support</h2><p class="ft-intro">Interested in a product demo? Have any questions? Want to chat? <a href="#contact-us"><strong>Contact Us.</strong></a></p><p class="ft-hours">Hours: Monday-Friday: 6:30 am–5:00 pm (PST)</p></div>'
             '<div class="ft-reach"><p>Additional ways to reach us:</p><p class="ft-b"><a href="tel:8006992547">Phone: 800-699-2547</a></p><p class="ft-b">Fax: 510-324-4545</p><p class="ft-b"><a href="mailto:customerservice@mizuho.com">Email: customerservice@mizuho.com</a></p><p>Address: 30057 Ahem Avenue, Union City, CA 94587</p></div>'
             '<hr class="ft-rule"><div class="ft-menus">'
             + "".join(f'<nav class="ft-col ft-col--{i+1}" aria-label="{h}"><h3>{h}</h3><ul>' + "".join(f'<li><a href="{slug(l)}">{l}</a></li>' for l in links) + '</ul></nav>' for i, (h, links) in enumerate(MENU))
             + '</div><div class="ft-brand"><img class="ft-logo" src="' + I + '/logo-mizuho-footer-reversed.png" alt="Mizuho America" width="200" height="58" loading="lazy"><p class="ft-copy">© 2026 Mizuho America, Inc. All rights reserved.</p></div>'
             '<nav class="ft-legal" aria-label="Legal"><ul><li><a href="#privacy-policy">Privacy Policy</a></li><li><a href="#terms-of-use">Terms of Use</a></li><li><a href="#cookie-policy">Cookie Policy</a></li><li><a href="#accessibility">Accessibility</a></li></ul></nav>'
             '</div></footer>')

FOOT_CSS = f"""
.site-foot {{ background: #0065B3; color: #FFFFFF; font-family: {MO}; font-weight: 300; }}
.site-foot a {{ color: #FFFFFF; }}
.ft-h2 {{ font-family: {FA}; font-weight: 700; font-optical-sizing: none; font-variation-settings: "opsz" 34, "WONK" 1; }}
.ft-intro strong, .ft-b {{ font-weight: 700; }}
.ft-rule {{ margin: 0; border: 0; border-top: 1px solid #FFFFFF; }}
.ft-col h3 {{ font-family: {MO}; font-weight: 700; }}
.ft-legal ul {{ display: flex; flex-wrap: wrap; }}
.ft-logo {{ height: auto; }}
{D} {{
  .site-foot {{ height: {u(960)}; }}
  .ft-contact {{ {at(78, 70, 927)} }}
  .ft-h2 {{ font-size: {u(34)}; line-height: {u(50)}; }}
  .ft-hours {{ font-size: {u(20)}; line-height: {u(30)}; }}
  .ft-reach {{ {at(79, 221, 1039)} font-size: {u(25)}; line-height: {u(40)}; }}
  .ft-rule {{ {at(79, 480, 1279)} }}
  .ft-menus {{ {at(78, 531, 1280)} display: grid; grid-template-columns: {u(375)} {u(341)} {u(287)} 1fr; }}
  .ft-col h3 {{ font-size: {u(25)}; line-height: {u(50)}; }}
  .ft-brand {{ {at(44, 866)} display: flex; align-items: flex-start; }}
  .ft-logo {{ width: {u(200)}; }}
  .ft-copy {{ margin: {u(24)} 0 0 {u(12)}; font-size: {u(14)}; line-height: {u(40)}; }}
  .ft-legal {{ {at(961, 890)} font-size: {u(14)}; line-height: {u(40)}; }}
  .ft-legal ul {{ gap: {u(29)}; }}
}}
{M} {{
  .ft-h2 {{ font-size: 28px; line-height: 50px; }}
  .ft-intro {{ font-size: 18px; line-height: 40px; }}
  .ft-hours {{ font-size: 18px; line-height: 30px; }}
  .ft-reach {{ font-size: 20px; line-height: 32px; letter-spacing: -0.035em; }} /* Montserrat runs wider than Gotham */
  .ft-menus {{ display: grid; grid-template-columns: 187px 1fr; row-gap: 36px; }}
  .ft-col h3 {{ font-size: 22px; line-height: 50px; }}
  .ft-col ul {{ font-size: 16px; line-height: 40px; letter-spacing: -0.03em; }}
  .ft-brand {{ display: flex; flex-direction: column; gap: 8px; }}
  .ft-logo {{ width: 200px; }}
  .ft-copy, .ft-legal {{ font-size: 12px; line-height: 14.4px; }}
  .ft-legal ul {{ gap: 8px 22px; }}
}}
"""


# The compiler only writes placeholder anchors (href="#about-mizuho-america"), so nothing navigates (issues-log #32).
# Point every link whose WordPress page exists at that page; the rest stay anchors until their pages are built.
SITE = "http://task-11.local"
LINKS = {
    "top": "/", "about-mizuho-america": "/about-us/", "about-mizuho": "/about-us/", "our-story": "/about-us/",
    "clinical-resources": "/resources/", "videos": "/resources/", "clinical-case-studies": "/resources/", "events": "/resources/",
    "contact-support": "/contact-us/", "contact-us": "/contact-us/", "request-a-demo": "/contact-us/",
    "find-an-account-manager": "/contact-us/", "technical-support": "/contact-us/", "customer-service": "/contact-us/", "faqs": "/contact-us/",
    "sales-portal": "/sales-hub/", "sale-hub": "/sales-hub/",
}


def link_pages(html):
    for key, path in LINKS.items():
        html = html.replace(f'href="#{key}"', f'href="{SITE}{path}"')
    return html
