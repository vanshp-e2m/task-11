"""Rewrite every section of pages/mizuho-home/blueprint.json as an exact Figma replica (desktop 1:9 + mobile 1:400).

Desktop (>=1024px): each section is a 1440-unit frame; every element sits at its Figma coordinate, expressed in `--u`
(= min(1px, container width / 1440)), so the page is pixel-exact at 1440, scales proportionally down to 1024, and centres above 1440.
Mobile (<=1023px): normal flow layout following the Figma 430 frame's auto-layout (44/20 padding, 36 gaps, mobile type scale).
Numbers are Figma geometry (dumps in cache/tmp/geom-desktop.txt / geom-mobile.txt). Compile afterwards with run_devcommand_compiler.py.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BP = os.path.join(ROOT, "pages", "mizuho-home", "blueprint.json")
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

# ---------------------------------------------------------------- hero 1:81 (part) / 1:411   (desktop origin y=161, h=930)
HERO_HTML = f"""<section class="hero rs" id="hero-carousel"><div class="fx">
<h1 class="hero-h1">Neurological success is your mindset. <span>ours, too.</span></h1>
<div class="hero-card hero-card--1"><img class="hero-img" src="{I}/hero-product-sugita-ii-head-frame-card-crop.png" alt="Sugita ll Multi-Purpose Head Frame" width="572" height="592"><span class="hero-pill">Sugita ll Multi-Purpose Head Frame</span><a class="hero-arrow" href="#sugita-ii-head-frame" aria-label="View Sugita ll Multi-Purpose Head Frame"><img src="{I}/icon-arrow-circle-right.svg" alt="" width="55" height="55"></a></div>
<div class="hero-card hero-card--2"><img class="hero-img" src="{I}/hero-product-mst-7300-table-card-crop.png" alt="MST 7300 Series Microneurosurgery Tables" width="572" height="592" loading="lazy"><span class="hero-pill">MST 7300 Series Microneurosurgery Tables</span><a class="hero-arrow" href="#mst-7300-tables" aria-label="View MST 7300 Series Microneurosurgery Tables"><img src="{I}/icon-arrow-circle-right.svg" alt="" width="55" height="55"></a></div>
<div class="hero-meta"><a class="hero-browse" href="#procedure-band"><img src="{I}/icon-arrow-down.svg" alt="" width="12" height="14"><span>Browse by Procedure</span></a><span class="hero-dots" aria-hidden="true"><i class="is-on"></i><i></i><i></i></span></div>
<div class="hero-ctas"><a class="hero-btn hero-btn--solid" href="#products">Explore All Products</a><a class="hero-btn hero-btn--line" href="#request-a-demo">Request a Demo</a></div>
</div></section>"""

HERO_CSS = f"""
.hero-h1, .intro-h2, .ts-h2 {{ font-family: {FR}; font-weight: 400; text-transform: uppercase; color: #0065B3; }}
.hero-h1 span {{ display: block; color: #00B3F0; }}
.hero-card {{ position: relative; overflow: hidden; }}
.hero-img {{ width: 100%; height: 100%; object-fit: cover; }}
.hero-pill {{ position: absolute; display: flex; align-items: center; justify-content: center; box-sizing: border-box; background: #0065B3; color: #FFFFFF; font-family: {FR}; font-weight: 400; white-space: nowrap; }}
.hero-arrow {{ position: absolute; }}
.hero-arrow img {{ width: 100%; height: 100%; }}
.hero-browse {{ display: flex; align-items: center; color: #0065B3; font-family: {FR}; }}
.hero-dots {{ display: flex; }}
.hero-dots i {{ display: block; border-radius: 50%; background: #D9D9D9; }}
.hero-dots i.is-on, .ab-card--blue {{ background: #0065B3; }}
.hero-btn {{ display: flex; align-items: center; justify-content: center; box-sizing: border-box; border-radius: 5px; font-family: {FR}; font-weight: 400; }}
.hero .hero-btn--solid {{ background: #0065B3; color: #FFFFFF; }}
.hero .hero-btn--line {{ border: 2px solid #00B3F0; color: #00B3F0; }}
{D} {{
  .hero {{ height: {u(930)}; }}
  .hero-h1 {{ {at(96, 33, 1247)} font-size: {u(70)}; line-height: {u(70)}; }}
  .hero-card--1 {{ {at(104, 211, 572, 592)} border-radius: {u(51)}; }}
  .hero-card--2 {{ {at(756, 211, 572, 592)} border-radius: {u(50)}; }}
  .hero-pill {{ height: {u(45)}; border-radius: {u(13)}; font-size: {u(19)}; line-height: {u(40)}; }}
  .hero-card--1 .hero-pill {{ left: {u(129)}; top: {u(31)}; width: {u(308)}; }}
  .hero-card--2 .hero-pill {{ left: {u(98)}; top: {u(28)}; width: {u(372)}; }}
  .hero-card--1 .hero-arrow {{ left: {u(481)}; top: {u(498)}; width: {u(55)}; height: {u(55)}; }}
  .hero-card--2 .hero-arrow {{ left: {u(483)}; top: {u(498)}; width: {u(55)}; height: {u(55)}; }}
  .hero-browse {{ {at(684, 844)} height: {u(50)}; gap: {u(20)}; font-size: {u(18)}; line-height: {u(50)}; }}
  .hero-browse img {{ width: {u(12)}; height: {u(14)}; }}
  .hero-dots {{ {at(1220, 851)} gap: {u(8)}; }}
  .hero-dots i {{ width: {u(24)}; height: {u(24)}; }}
  .hero-btn {{ height: {u(50)}; font-size: {u(18)}; line-height: {u(23.94)}; }}
  .hero-btn--solid {{ {at(106, 846, 216)} }}
  .hero-btn--line {{ {at(356, 846, 288)} }}
}}
{M} {{
  .hero-h1 {{ font-size: 48px; line-height: 55.2px; }}
  .hero-card {{ width: 100%; aspect-ratio: 390 / 404; border-radius: 34.77px; }}
  .hero-card--2 {{ margin-top: -18px; }}
  .hero-pill {{ top: 21px; left: 50%; transform: translateX(-50%); height: 31px; padding: 1px 20px 1px 19px; border-radius: 8.86px; font-size: 12px; line-height: 27.27px; }}
  .hero-arrow {{ right: 22px; bottom: 20px; width: 38px; height: 38px; }}
  .hero-meta {{ display: flex; justify-content: space-between; align-items: center; margin-top: -18px; }}
  .hero-browse {{ gap: 8px; font-size: 14px; line-height: 18.62px; }}
  .hero-browse img {{ width: 12px; height: 12px; }}
  .hero-dots {{ gap: 5px; }}
  .hero-dots i {{ width: 15px; height: 15px; }}
  .hero-ctas {{ display: flex; flex-direction: column; gap: 18px; }}
  .hero-btn {{ height: 50px; font-size: 18px; line-height: 23.94px; }}
}}
"""

# ---------------------------------------------------------------- intro 1:81 (part) / 1:439   (origin y=1091, h=402)
INTRO_HTML = """<section class="intro rs" id="intro-statement"><div class="fx">
<h2 class="intro-h2">We are Mizuho AMERICA: delivering world-class collective expertise with a personalized approach</h2>
<p class="intro-p">Singularly focused on neurosurgery, Mizuho America is dedicated to delivering an exceptional experience to help you achieve your surgical goals across a broad range of procedures and patients.</p>
<a class="intro-btn" href="#testimonials">Watch what clinical experts say about us</a>
<hr class="intro-rule">
</div></section>"""

INTRO_CSS = f"""
.intro-p {{ font-family: {OS}; font-weight: 300; color: #090909; }}
.intro .intro-btn, .vc .vc-btn, .ab .ab-btn {{ display: flex; align-items: center; box-sizing: border-box; border-radius: 5px; background: #0065B3; color: #FFFFFF; font-family: {FR}; font-weight: 400; }}
.intro-rule {{ margin: 0; border: 0; border-top: 1px solid #00B3F0; }}
{D} {{
  .intro {{ height: {u(402)}; }}
  .intro-h2 {{ {at(107, 34, 1216)} font-size: {u(45)}; line-height: {u(55)}; }}
  .intro-p {{ {at(107, 167, 1216)} font-size: {u(25)}; line-height: {u(45)}; }}
  .intro-btn {{ {at(107, 281, 303, 50)} padding-left: {u(20)}; font-size: {u(16)}; line-height: {u(40)}; }}
  .intro-rule {{ {at(84, 401, 1262)} }}
}}
{M} {{
  .intro-h2 {{ font-size: 36px; line-height: 41.4px; }}
  .intro-p {{ font-size: 18px; line-height: 24.51px; }}
  .intro-btn, .vc-btn, .ab-btn {{ justify-content: center; height: 50px; font-size: 16px; line-height: 21.28px; }}
  .intro-rule {{ position: absolute; left: 20px; right: 20px; bottom: 0; }}
}}
"""

# ---------------------------------------------------------------- value columns 1:31 / 1:445   (origin y=1492, h=773)
CARDS = [
    ("Surgeon-centric", "value-icon-surgeon-centric.png", (100, 98), (79, 77), "Products designed exclusively<br class=\"d-only\"> for neurosurgeons",
     "With an expansive portfolio of instruments available individually and in convenient, timesaving sets and kits, we are committed to helping you optimize precision, efficiency, and workflow in the OR"),
    ("Consistent quality", "value-icon-consistent-quality.png", (99, 90), (88, 80), "Handcrafted tools for exceptional quality, performance and longevity",
     "Our tools are produced with the utmost care and integrity, adhering to stringent manufacturing protocols, so you can confidently rely on them for your delicate, high-stakes procedures"),
    ("Notable names", "value-icon-notable-names.png", (100, 84), (87, 73), "Longstanding collaborations with renowned neurosurgeons",
     "We’ve become a global leader in the field of neurosurgical tools through our ongoing work with clinical experts to help identify and fill unmet needs in the OR"),
    ("Personal partnership", "value-icon-personal-partnership.png", (100, 72), (96, 69), "Supporting you before, during,<br class=\"d-only\"> and after the sale",
     "We not only stand behind our high-quality products; we stand with you to ensure your questions are answered, your needs are met, and your input and insights are heard"),
]
VC_HTML = ('<section class="vc rs" id="value-columns"><div class="fx">'
           + "".join(f'<article class="vc-card vc-card--{i+1}"><h3 class="vc-title">{t}</h3><img class="vc-icon" src="{I}/{ic}" alt="" width="{dw}" height="{dh}" loading="lazy"><div class="vc-text"><p class="vc-lead">{ld}</p><p class="vc-body">{bd}</p></div></article>'
                     for i, (t, ic, (dw, dh), _m, ld, bd) in enumerate(CARDS))
           + '<a class="vc-btn" href="#downloadable-brochures">Check out our downloadable brochures</a></div></section>')

vc_icon_d = "\n".join(f"  .vc-card--{i+1} .vc-icon {{ width: {u(dw)}; height: {u(dh)}; }}" for i, (_t, _ic, (dw, dh), _m, _l, _b) in enumerate(CARDS))
vc_icon_m = "\n".join(f"  .vc-card--{i+1} .vc-icon {{ width: {mw}px; height: {mh}px; }}" for i, (_t, _ic, _d, (mw, mh), _l, _b) in enumerate(CARDS))
VC_CSS = f"""
.vc-title {{ font-family: {FR}; font-weight: 400; text-transform: uppercase; color: #00B3F0; white-space: nowrap; }}
.vc-icon {{ object-fit: cover; }}
.vc-lead, .vc-body {{ font-family: {OS}; color: #090909; }}
.vc-lead {{ font-weight: 600; font-style: italic; }}
.vc-body {{ font-weight: 300; }}
{D} {{
  .vc {{ height: {u(773)}; }}
  .vc-card {{ position: absolute; top: {u(98)}; height: {u(470)}; box-sizing: border-box; padding-top: {u(4)}; }}
  .vc-card--1 {{ left: {u(114)}; width: {u(253)}; }}
  .vc-card--2, .vc-card--3, .vc-card--4 {{ border-left: 1px solid #00B3F0; }}
  .vc-card--2 {{ left: {u(400)}; padding-left: {u(30.7)}; width: {u(290)}; }}
  .vc-card--3 {{ left: {u(715)}; padding-left: {u(29.7)}; width: {u(289)}; }}
  .vc-card--4 {{ left: {u(1030)}; padding-left: {u(30)}; width: {u(316)}; }}
  .vc-title {{ height: {u(50)}; font-size: {u(24)}; line-height: {u(31.92)}; }}
{vc_icon_d}
  .vc-text {{ position: absolute; top: {u(177)}; width: {u(259.3)}; }}
  .vc-card--1 .vc-text {{ width: {u(253)}; }}
  .vc-card--4 .vc-text {{ margin-left: {u(13.3)}; }}
  .vc-lead, .vc-body {{ font-size: {u(16)}; line-height: {u(30)}; }}
  .vc-lead {{ margin-bottom: {u(30)}; }}
  .vc-btn {{ {at(107, 629, 293, 50)} padding-left: {u(20)}; font-size: {u(16)}; line-height: {u(40)}; }}
}}
{M} {{
  .vc > .fx {{ gap: 28px; }}
  .vc-card + .vc-card {{ border-top: 1px solid #00B3F0; padding-top: 28px; }}
  .vc-title {{ font-size: 20px; line-height: 26.6px; }}
  .vc-icon {{ margin-top: 12px; }}
{vc_icon_m}
  .vc-text {{ margin-top: 28px; }}
  .vc-lead, .vc-body {{ font-size: 14px; line-height: 28px; }}
  .vc-lead {{ margin-bottom: 28px; }}
}}
"""

# ---------------------------------------------------------------- procedure band 1:145 / 1:471   (origin y=2265, h=555)
PROCS = [
    ("tumor", "Tumor Removal", "procedure-icon-tumor-removal-trim.png", "See Malleable Instruments and more →", "#malleable-instruments"),
    ("aneurysm", "Aneurysm", "procedure-icon-aneurysm-trim.png", "See Sugita TII Aneurysm Clips and more →", "#sugita-tii-aneurysm-clips"),
    ("endo", "Endoscopic Endonasal Approach", "procedure-icon-endoscopic-endonasal-trim.png", "See E3 Evans Elite Endoscopic Instrument Set and more →", "#e3-evans-elite-endoscopic-set"),
]
PB_HTML = ('<section class="pb rs" id="procedure-band"><div class="fx"><h2 class="pb-h2">A robust portfolio of instruments, tables, head-holding systems, and vascular management devices for your diverse neurosurgical procedures</h2>'
           + "".join(f'<div class="pb-item pb-item--{k}"><img class="pb-icon" src="{I}/{ic}" alt="" width="146" height="146" loading="lazy"><div class="pb-txt"><h3>{t}</h3><a class="pb-view" href="#{k}-products">View product →</a><a class="pb-more" href="{href}">{more}</a></div></div>'
                     for k, t, ic, more, href in PROCS)
           + '<p class="pb-closing">And beyond—review the full list of supported procedures here</p><a class="pb-btn" href="#supported-procedures"><span>Supported Procedures</span><img src="' + I + '/icon-arrow-down.svg" alt="" width="12" height="14"></a></div></section>')

PB_CSS = f"""
.rs.pb {{ background-color: #0065B3; }} /* beats the shared white .rs background regardless of rule order */
.pb-h2, .pb-closing {{ font-family: {MU}; font-weight: 700; color: #FFFFFF; }}
.pb-icon {{ object-fit: contain; }}
.pb-txt h3, .pb-view, .pb-more {{ font-family: {MO}; font-weight: 700; }}
.pb-txt h3 {{ color: #FFFFFF; }}
.pb .pb-view {{ display: block; color: #FFFFFF; }}
.pb .pb-more {{ display: block; color: #77DCFF; }}
.pb .pb-btn {{ display: flex; align-items: center; box-sizing: border-box; border: 2px solid #00B3F0; border-radius: 5px; background: #FFFFFF; color: #0065B3; font-family: {FR}; font-weight: 400; }}
{D} {{
  .pb {{ height: {u(555)}; }}
  .pb-h2 {{ {at(76, 51, 1137)} font-size: {u(34)}; line-height: {u(50)}; }}
  .pb-item {{ display: contents; }}
  .pb-item--tumor .pb-icon {{ {at(85, 215, 146, 146)} }}
  .pb-item--tumor .pb-txt {{ {at(241, 209, 228)} }}
  .pb-item--aneurysm .pb-icon {{ {at(566, 209, 114, 158)} }}
  .pb-item--aneurysm .pb-txt {{ {at(695, 211, 234)} }}
  .pb-item--endo .pb-icon {{ {at(944, 212, 184, 167)} }}
  .pb-item--endo .pb-txt {{ {at(1134, 212, 270)} }}
  .pb-txt h3, .ft-intro, .ft-col ul {{ font-size: {u(20)}; line-height: {u(40)}; }}
  .pb-item--endo .pb-txt h3 {{ line-height: {u(30)}; }}
  .pb-view {{ font-size: {u(16)}; line-height: {u(40)}; }}
  .pb-more {{ margin-top: {u(26)}; font-size: {u(16)}; line-height: {u(26)}; }}
  .pb-closing {{ {at(76, 446, 962)} font-size: {u(32)}; line-height: {u(50)}; }}
  .pb-btn {{ {at(987, 447, 391, 50)} }}
  .pb-btn span {{ position: absolute; left: {u(-45)}; width: {u(285)}; text-align: center; font-size: {u(18)}; line-height: {u(50)}; }}
  .pb-btn img {{ position: absolute; left: {u(359)}; top: {u(16)}; width: {u(12)}; height: {u(14)}; }}
}}
{M} {{
  .pb-h2 {{ font-size: 28px; line-height: 46.54px; }}
  .pb-item {{ display: grid; grid-template-columns: 156px 1fr; align-items: center; }}
  .pb-item--tumor {{ order: 1; }} .pb-item--endo {{ order: 2; }} .pb-item--aneurysm {{ order: 3; }}
  .pb-h2 {{ order: 0; }} .pb-closing {{ order: 4; }} .pb-btn {{ order: 5; }}
  .pb-item--tumor .pb-icon {{ width: 119px; height: 119px; }}
  .pb-item--endo .pb-icon {{ width: 113px; height: 103px; }}
  .pb-item--aneurysm .pb-icon {{ width: 83px; height: 115px; margin-left: 24px; }}
  .pb-txt h3 {{ font-size: 18px; line-height: 24px; }}
  .pb-view {{ font-size: 14px; line-height: 40px; }}
  .pb-more {{ margin-top: 26px; font-size: 14px; line-height: 22px; }}
  .pb-closing {{ font-size: 28px; line-height: 46.54px; }}
  .pb-btn {{ justify-content: space-between; height: 50px; padding: 0 35px; font-size: 16px; line-height: 21.28px; }}
  .pb-btn img {{ width: 12px; height: 12px; }}
}}
"""

# ---------------------------------------------------------------- testimonials 1:57 / 1:487 + 1:518   (origin y=2820, h=1190)
BIOS = [
    ("lawton", "testimonial-thumb-lawton.jpg", "Michael T. Lawton, MD", "President and CEO,", ["Barrow Neurological Institute", "Professor and Chair, Neurosurgery", "Chief, Neurovascular Surgery"]),
    ("evans", "testimonial-thumb-evans.jpg", "James J. Evans, MD", "Professor, Neurological Surgery &amp; Otolaryngology", ["Division Chief, Brain Tumor and Stereotactic", "Radiosurgery Division", "Director, Cranial Base and Pituitary Surgery", "Director, Cranial Base and Endoscopic Surgery Fellowship"]),
    ("youssef", "testimonial-thumb-youssef.jpg", "A. Samy Youssef, MD, PhD", "Professor &amp; Vice Chairman of Education", ["Departments of Neurosurgery &amp; Otolaryngology", "Director of Skull Base Surgery", "University of Colorado School of Medicine"]),
]
TS_HTML = ('<section class="ts rs" id="testimonials"><div class="fx"><div class="ts-head"><h2 class="ts-h2">Testimonials</h2><p class="ts-intro">Leaders in the field of neurosurgery discuss Mizuho America’s pivotal role in expanding the neurosurgical armamentarium.</p></div>'
           + "".join(f'<article class="ts-card ts-card--{i+1}"><a class="ts-thumb" href="#watch-{k}"><img class="ts-img" src="{I}/{img}" alt="{name}" width="409" height="272" loading="lazy"><img class="ts-play" src="{I}/icon-play-circle.svg" alt="" width="53" height="53"></a>'
                     f'<div class="ts-bio"><p class="ts-name">{name}</p><p class="ts-role">{role}</p><p class="ts-rest">{"<br>".join(rest)}</p><a class="ts-watch" href="#watch-{k}">Watch now</a></div></article>'
                     for i, (k, img, name, role, rest) in enumerate(BIOS))
           + '<a class="ts-mcta m-only" href="#clinical-experts">Watch what clinical experts say about us</a>'
           + '<hr class="ts-rule ts-rule--top"><blockquote class="ts-quote"><p>“I Have found the mizuho america team to be...<br class="d-only"> forward-thinking, and have a genuine interest in the advancement of surgical instrumentation.”</p></blockquote>'
           + '<p class="ts-attr">– James Evans, MD</p><hr class="ts-rule ts-rule--l d-only"><hr class="ts-rule ts-rule--r d-only"><a class="ts-more" href="#more-testimonials">See more testimonials</a><hr class="ts-rule ts-rule--bottom m-only"></div></section>')

TS_CSS = f"""
.ts-intro {{ font-family: {OS}; color: #090909; }}
.ts-thumb {{ position: relative; display: block; }}
.ts-img {{ width: 100%; height: 100%; object-fit: cover; }}
.ts-play {{ position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); }}
.ts-name {{ font-family: {OS}; font-weight: 700; color: #0065B3; }}
.ts-role, .ts-rest {{ font-family: {OS}; font-weight: 300; color: #090909; }}
.ts .ts-watch, .ts .ts-more, .ts .ts-mcta {{ display: flex; align-items: center; justify-content: center; box-sizing: border-box; border-radius: 5px; background: #0065B3; color: #FFFFFF; font-family: {FR}; font-weight: 400; }}
.ts-rule {{ margin: 0; border: 0; border-top: 1px solid #00B3F0; }}
.ts-quote {{ font-family: {FR}; font-weight: 400; text-transform: uppercase; text-align: center; color: #0065B3; }}
.ts-attr {{ font-family: {OS}; font-weight: 300; text-align: center; color: #090909; }}
{D} {{
  .ts {{ height: {u(1190)}; }}
  .ts-head {{ {at(76, 91, 1177)} }}
  .ts-h2 {{ font-size: {u(34)}; line-height: {u(50)}; }}
  .ts-intro {{ margin-top: {u(25)}; font-weight: 400; font-size: {u(20)}; line-height: {u(40)}; }}
  .ts-card {{ position: absolute; top: {u(212)}; }}
  .ts-card--1 {{ left: {u(76)}; width: {u(409)}; }}
  .ts-card--2 {{ left: {u(512)}; width: {u(408)}; }}
  .ts-card--3 {{ left: {u(949)}; width: {u(409)}; }}
  .ts-thumb {{ height: {u(272)}; }}
  .ts-play {{ width: {u(53)}; height: {u(53)}; }}
  .ts-bio {{ margin-top: {u(17)}; }}
  .ts-card--1 .ts-bio {{ padding-left: {u(21)}; }}
  .ts-card--2 .ts-bio {{ padding-left: {u(19)}; }}
  .ts-card--3 .ts-bio {{ padding-left: {u(17)}; }}
  .ts-name {{ font-size: {u(18)}; line-height: {u(30)}; }}
  .ts-role {{ font-size: {u(14)}; line-height: {u(30)}; }}
  .ts-rest {{ font-size: {u(14)}; line-height: {u(22)}; }}
  .ts-watch {{ width: {u(93)}; height: {u(40)}; margin-top: {u(17)}; font-size: {u(14)}; line-height: {u(50)}; }}
  .ts-rule--top {{ {at(76, 788, 1282)} }}
  .ts-quote {{ {at(217, 845, 998)} font-size: {u(34)}; line-height: {u(50)}; }}
  .ts-attr {{ {at(570, 1002, 300)} font-size: {u(24)}; line-height: {u(45)}; }}
  .ts-rule--l {{ {at(76, 1118, 513)} }}
  .ts-rule--r {{ {at(845, 1118, 513)} }}
  .ts-more {{ {at(628, 1091, 179, 50)} font-size: {u(16)}; line-height: {u(40)}; }}
}}
{M} {{
  .ts > .fx {{ padding-bottom: 0; }} /* Figma: the bottom divider is the section's last edge */
  .ts-head {{ display: flex; flex-direction: column; gap: 12px; }}
  .ts-h2 {{ font-size: 28px; line-height: 50px; }}
  .ts-intro {{ font-weight: 300; font-size: 18px; line-height: 24.51px; }}
  .ts-thumb {{ aspect-ratio: 390 / 259; }}
  .ts-play {{ width: 44px; height: 44px; }}
  .ts-bio {{ display: flex; flex-direction: column; gap: 16px; margin-top: 6.67px; padding: 9.54px 9.54px 9.54px 20.02px; }}
  .ts-name {{ font-size: 16px; line-height: 28.61px; }}
  .ts-role {{ margin-top: -16px; font-size: 13px; line-height: 28.61px; }}
  .ts-rest {{ margin-top: -16px; font-size: 13px; line-height: 21px; }}
  .ts-watch {{ width: 140px; height: 50px; font-size: 16px; line-height: 21.28px; }}
  .ts-mcta, .ts-more {{ height: 50px; font-size: 16px; line-height: 21.28px; }}
  .ts-rule--top {{ margin-top: 8px; }}
  .ts-quote {{ margin-top: 8px; font-size: 24px; line-height: 31.92px; }}
  .ts-attr {{ font-size: 20px; line-height: 27.24px; }}
  .ts-rule--bottom {{ margin-top: 8px; }}
}}
"""

# ---------------------------------------------------------------- about + stats 1:10 / 1:524   (origin y=4010, h=746)
STATS = [("30+", "years serving the neurosurgery community", "blue", 37, 217), ("1,800+", "neurosurgical<br>products", "sky", 41, 111), ("1000+", "hospitals served", "blue", 48, 131)]
AB_HTML = ('<section class="ab rs" id="about-stats"><div class="fx"><h2 class="ab-h2">About Mizuho America</h2>'
           '<p class="ab-p">Established in Boston, Massachusetts in 1993, Mizuho America is part of Mizuho Corporation, a global medical products company with more than a century of commitment to providing surgeons with meticulously crafted equipment for their OR needs. With deep expertise in neurosurgical products, Mizuho America has built a legacy of quality, reliability, and trusted partnership with healthcare professionals. From problem-solving instrument sets developed with clinical experts, to ongoing support of neurosurgeons every day, Mizuho America remains committed to solutions that can help facilitate greater control, precision, and efficiency during the procedure with the goal of better outcomes after.</p>'
           '<div class="ab-stats">'
           + "".join(f'<div class="ab-stat ab-stat--{i+1}"><div class="ab-card ab-card--{c}"><span class="ab-num">{n}</span><span class="ab-label">{l}</span></div><span class="ab-panel" aria-hidden="true"></span></div>' for i, (n, l, c, _t, _w) in enumerate(STATS))
           + '</div><a class="ab-btn" href="#our-story">Explore our story</a></div></section>')

ab_d = "\n".join(f"  .ab-stat--{i+1} .ab-num {{ top: {u(t)}; }}\n  .ab-stat--{i+1} .ab-label {{ top: {u(t + 57)}; width: {u(w)}; }}" for i, (_n, _l, _c, t, w) in enumerate(STATS))
ab_m = "\n".join(f"  .ab-stat--{i+1} .ab-num {{ top: {t}px; }}\n  .ab-stat--{i+1} .ab-label {{ top: {t + 57}px; width: {w}px; }}" for i, (_n, _l, _c, t, w) in enumerate(STATS))
AB_CSS = f"""
.ab-h2 {{ font-family: {FR}; font-weight: 400; text-transform: uppercase; text-align: center; color: #0065B3; }}
.ab-p {{ font-family: {OS}; font-weight: 400; text-align: center; color: #090909; }}
.ab-stat {{ position: relative; }}
.ab-stat--1 {{ z-index: 3; }} .ab-stat--2 {{ z-index: 2; }} .ab-stat--3 {{ z-index: 1; }} /* Figma layer order: stat 1 on top */
.ab-card {{ position: absolute; box-sizing: border-box; color: #FFFFFF; font-family: {OS}; font-weight: 700; }}
.ab-card--sky {{ background: #00B3F0; }}
.ab-num, .ab-label {{ position: absolute; }}
.ab-num {{ white-space: nowrap; }}
.ab-panel {{ position: absolute; left: 0; top: 0; background: #FFFFFF; box-shadow: 21px 0 21px -23px #000000; }}
{D} {{
  .ab {{ height: {u(746)}; }}
  .ab-h2 {{ {at(464, 46, 483)} font-size: {u(34)}; line-height: {u(50)}; }}
  .ab-p {{ {at(175, 117, 1090)} font-size: {u(16)}; line-height: {u(36)}; }}
  .ab-stat {{ position: absolute; width: {u(421)}; height: {u(250)}; }}
  .ab-stat--1 {{ left: {u(76)}; top: {u(327)}; }}
  .ab-stat--2 {{ left: {u(446)}; top: {u(323)}; }}
  .ab-stat--3 {{ left: {u(815)}; top: {u(323)}; }}
  .ab-card {{ left: {u(131)}; top: {u(44)}; width: {u(290)}; height: {u(162)}; border-radius: {u(20)}; }}
  .ab-num {{ left: {u(50)}; font-size: {u(64)}; line-height: {u(36)}; }}
  .ab-label {{ left: {u(52)}; font-size: {u(16)}; line-height: {u(18)}; }}
{ab_d}
  .ab-panel {{ width: {u(146)}; height: {u(250)}; border-radius: {u(10)}; }}
  .ab-btn {{ {at(641, 597, 150, 50)} padding-left: {u(19)}; font-size: {u(16)}; line-height: {u(40)}; }}
}}
{M} {{
  .ab-h2 {{ font-size: 24px; line-height: 31.92px; }}
  .ab-p {{ margin-top: -14px; font-size: 14px; line-height: 28px; }}
  .ab-stats {{ display: flex; flex-direction: column; gap: 36px; }}
  .ab-stat {{ width: 350px; height: 250px; }}
  .ab-card {{ left: 60px; top: 43px; width: 290px; height: 162px; border-radius: 20px; }}
  .ab-num {{ left: 50px; font-size: 64px; line-height: 36px; }}
  .ab-label {{ left: 52px; font-size: 16px; line-height: 18px; }}
{ab_m}
  .ab-panel {{ width: 75px; height: 250px; border-radius: 10px; }}
}}
"""

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

SECTIONS = [
    {"id": "site-header", "landmark": "header", "escape_hatch": True, "html": HEADER_HTML, "css": SHARED + HEADER_CSS, "js": HEADER_JS},
    {"id": "hero-carousel", "escape_hatch": True, "heading_level": 1, "html": HERO_HTML, "css": HERO_CSS},
    {"id": "intro-statement", "escape_hatch": True, "html": INTRO_HTML, "css": INTRO_CSS},
    {"id": "value-columns", "escape_hatch": True, "html": VC_HTML, "css": VC_CSS},
    {"id": "procedure-band", "escape_hatch": True, "html": PB_HTML, "css": PB_CSS},
    {"id": "testimonials", "escape_hatch": True, "html": TS_HTML, "css": TS_CSS},
    {"id": "about-stats", "escape_hatch": True, "html": AB_HTML, "css": AB_CSS},
    {"id": "site-footer", "landmark": "footer", "escape_hatch": True, "html": FOOT_HTML, "css": FOOT_CSS},
]
NOTE = ("2026-09-28 replica rebuild (developer: 'perfect replica, desktop + mobile as in Figma'): exact Figma 1:9 coordinates on desktop "
        "(scaled via --u), Figma 1:400 auto-layout on mobile. Generated by tools/figma_html/build_replica.py.")
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
for s in SECTIONS:
    s["notes"] = [NOTE]
    for key, path in LINKS.items():
        s["html"] = s["html"].replace(f'href="#{key}"', f'href="{SITE}{path}"')

bp = json.load(open(BP, encoding="utf-8"))
bp["sections"] = SECTIONS
bp.pop("slider_library", None)
json.dump(bp, open(BP, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("sections:", [s["id"] for s in SECTIONS])
