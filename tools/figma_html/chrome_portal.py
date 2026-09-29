"""Sales Hub (portal) chrome: header 1:2988 and footer 1:2872 of the Resource Library frame (1:2871), shared by the three
Sales Hub pages (Login, Dashboard, Resource Library).

Desktop header: logo | rule | SALES PORTAL | Dashboard · Resources · Cross-Reference · Training | John Q. Public | Account.
Figma's MOBILE frame (1:1972) draws the PUBLIC mobile header instead (logo + burger, EN/ESP, Find an Account Manager);
followed as drawn (issues-log), with the portal links in the burger drawer. The burger, drawer and JS are Home's
(chrome.py HEADER_CSS/HEADER_JS), so the validator's mobile-nav contract is the same as on the public pages.
"""
from chrome import D, FR, HEADER_CSS, HEADER_JS, I, M, MO, OS, SHARED, at, font, u  # noqa: F401

SITE = "http://task-11.local"


# Replica links: pages that have an HTML replica link to it (so the Sales Hub can be clicked through locally); the two tools
# without a design (Cross-Reference, Training) stay on their WordPress placeholder pages.
REPLICA = {"Dashboard": "../../sales-hub-dashboard/html/", "Resources": "../../resource-library/html/"}


def portal_header(current="Resources"):
    links = [("Dashboard", "/sales-hub/dashboard/"), ("Resources", "/sales-hub/resource-library/"),
             ("Cross-Reference", "/sales-hub/cross-reference/"), ("Training", "/sales-hub/training/")]
    nav = "".join(f'<li><a{" class=\"is-current\" aria-current=\"page\"" if t == current else ""} href="{REPLICA.get(t, SITE + h)}">{t}</a></li>' for t, h in links)
    return (f'<header class="site-head portal-head rs" id="site-header"><div class="fx">'
            f'<a class="hd-logo" href="{REPLICA['Dashboard']}"><img src="{I}/logo-mizuho-header-srgb.png" alt="Mizuho America" width="200" height="61"></a>'
            f'<span class="ph-rule d-only" aria-hidden="true"></span><a class="ph-portal d-only" href="{REPLICA['Dashboard']}">Sales Portal</a>'
            f'<nav class="hd-lang m-only" aria-label="Language"><ul><li><a class="is-current" href="#en" hreflang="en">EN</a></li><li><a href="#esp" hreflang="es">ESP</a></li></ul></nav>'
            f'<a class="hd-account m-only" href="{SITE}/contact-us/">Find an Account Manager</a>'
            '<button class="site-head__toggle" type="button" aria-expanded="false" aria-controls="site-primary-nav" aria-label="Menu"><span></span><span></span><span></span></button>'
            f'<nav class="site-head__nav" id="site-primary-nav" aria-label="Sales Hub"><ul>{nav}</ul></nav>'
            '<span class="ph-user d-only">John Q. Public</span>'
            f'<a class="ph-account selectish d-only" href="{REPLICA['Dashboard']}#account">Account</a>'
            '</div></header>')


PORTAL_HEADER_CSS = SHARED + HEADER_CSS + f"""
.ph-portal {{ font-family: {FR}; font-weight: 400; color: #0065B3; text-transform: uppercase; text-align: center; }}
.site-head__nav a.is-current, .site-head a.ph-portal {{ color: #0065B3; }}
.ph-user {{ font-family: {OS}; font-weight: 400; color: #000000; }}
.selectish {{ display: flex; align-items: center; box-sizing: border-box; background: #FFFFFF url("../{I}/icon-select-caret.svg") no-repeat right center; border: 1px solid rgba(0, 0, 0, 0.15); border-radius: 5px; font-family: {OS}; font-weight: 400; color: #000000; }}
{D} {{
  .portal-head {{ height: {u(144)}; }}
  .portal-head .hd-logo {{ {at(42, 51, 200, 61)} }}
  .ph-rule {{ {at(260, 69, 1, 36)} background: rgba(0, 0, 0, 0.2); }}
  .ph-portal {{ {at(281, 77, 117)} font-size: {u(15)}; line-height: {u(19.95)}; }}
  .portal-head .site-head__nav {{ left: {u(552)}; top: {u(78)}; }}
  .ph-user {{ {at(1083, 79)} {font(OS, 400, 13, 17.7)} }}
  .ph-account {{ {at(1212, 74, 161, 30)} padding-left: {u(12)}; background-size: {u(38)} {u(30)}; {font(OS, 400, 13, 17.7)} }}
  .selectish {{ background-size: {u(38)} {u(30)}; }}
}}
{M} {{
  .selectish {{ background-size: 38px 30px; }}
}}
"""
PORTAL_HEADER_JS = HEADER_JS

# caret for the select-look controls: 1px divider at x=123 of a 161px control + 13x10 triangle at x=136 (1:2995/1:2997)
CARET_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="38" height="30" viewBox="0 0 38 30">'
             '<rect x="0" y="0" width="1" height="30" fill="#000000" fill-opacity="0.2"/><path d="M13 10h13l-6.5 10z" fill="#000000"/></svg>')

PORTAL_FOOTER_HTML = (f'<footer class="site-foot portal-foot rs" id="site-footer"><div class="fx">'
                      f'<img class="pf-logo" src="{I}/logo-mizuho-footer-reversed.png" alt="Mizuho America" width="200" height="58" loading="lazy">'
                      f'<p class="pf-copy"><a href="{SITE}/sales-hub/">Sales Hub</a><span class="pf-dot" aria-hidden="true">•</span>© 2026 Mizuho America, Inc. All rights reserved.</p>'
                      '<nav class="pf-legal" aria-label="Legal"><ul><li><a href="#privacy-policy">Privacy Policy</a></li><li><a href="#terms-of-use">Terms of Use</a></li></ul></nav>'
                      '</div></footer>')
PORTAL_FOOTER_CSS = f"""
.site-foot {{ background: #0065B3; color: #FFFFFF; font-family: {MO}; font-weight: 300; }}
.site-foot a {{ color: #FFFFFF; }}
.pf-legal ul {{ display: flex; margin: 0; padding: 0; list-style: none; }}
.pf-logo {{ height: auto; }}
{D} {{
  .portal-foot {{ height: {u(150)}; }}
  .pf-logo {{ {at(44, 45, 200, 58)} }}
  .pf-copy {{ {at(256, 69)} font-size: {u(14)}; line-height: {u(40)}; }}
  .pf-dot {{ margin: 0 {u(15)} 0 {u(13)}; }}
  .pf-legal {{ {at(1166, 69)} font-size: {u(14)}; line-height: {u(40)}; }}
  .pf-legal ul {{ gap: {u(29)}; }}
  .pf--center .pf-logo {{ left: {u(594)}; }}
  .pf--center .pf-copy {{ left: {u(64)}; top: {u(57)}; }}
  .pf--center .pf-legal {{ top: {u(57)}; }}
}}
{M} {{
  .portal-foot > .fx {{ align-items: center; gap: 22px; text-align: center; }}
  .pf-copy {{ order: 1; font-size: 12px; line-height: 40px; }}
  .pf-dot {{ margin: 0 8px; }}
  .pf-logo {{ order: 2; width: 200px; }}
  .pf-legal {{ order: 3; font-size: 12px; line-height: 40px; }}
  .pf-legal ul {{ gap: 22px; }}
}}
"""
