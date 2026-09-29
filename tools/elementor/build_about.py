"""Native Elementor tree for About Us (page 15). This replaces the DevConnect draft (7 HTML widgets, see
docs/devconnect-conversion-issues.md).

Every visible string is a native widget (heading / text-editor / image / button), so it's editable in the Elementor editor.
Layout and type come from the theme partial assets/scss/pages/_about.scss via the `au-*` classes: desktop is the Figma
1:161 frame scaled by --u, mobile (<=1023) follows the Figma mobile frame 1:2237 auto-layout. Copy is verbatim from Figma.
Decoration only (divider lines, slider dots, timeline scrubber, carousel arrows) is drawn in CSS.

Run:  python tools/elementor/build_about.py            -> pages/about-us/elementor/about.json
      python tools/elementor/build_about.py --write    -> also writes it to page 15 and counts the stored nodes
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from build_chrome import eid  # noqa: E402  (same stable-id scheme as the header/footer)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEDIA = json.load(open(os.path.join(ROOT, "pages/about-us/figma/images/wp-media.json")))
MEDIA["about-hero-portrait"] = {"id": 64, "url": "http://task-11.local/wp-content/uploads/2026/09/about-hero-portrait.jpg"}
PAGE_ID = 15


def img(key):
    m = MEDIA[key]
    return {"id": m["id"], "url": m["url"], "source": "library"}


def con(name, cls, children, **s):
    settings = {"content_width": "full", "css_classes": cls}
    settings.update(s)
    return {"id": eid("au:" + name), "elType": "container", "isInner": False, "settings": settings, "elements": children}


def w(name, wtype, cls, **s):
    s["_css_classes"] = cls
    return {"id": eid("au:" + name), "elType": "widget", "widgetType": wtype, "settings": s, "elements": []}


def h(name, cls, text, tag="p"):
    return w(name, "heading", cls, title=text, header_size=tag)


def txt(name, cls, html):
    return w(name, "text-editor", cls, editor=html)


def image(name, cls, key, alt=""):
    return w(name, "image", cls, image=img(key), image_size="full", alt=alt)


def btn(name, cls, text, url, icon=None):
    s = {"text": text, "link": {"url": url, "is_external": "", "nofollow": ""}, "size": "sm"}
    if icon:
        s["selected_icon"] = {"value": icon, "library": "fa-solid"}
        s["icon_align"] = "row"
    return w(name, "button", "au-btn " + cls, **s)


def bg(key):
    return {"background_background": "classic", "background_image": img(key)}


# ------------------------------------------------------------------ content (verbatim Figma 1:161)
HERO_QUOTE = ('<span class="au-qmark">“</span>About a decade ago I designed a clip and worked in conjunction with Mizuho '
              'because I saw a need for my practice.”')
HERO_CITE = ("<p>Erol Veznedaroglu, MD, FACS, FAANS, FAHA<br>President and CEO, Global Neuroscience Institute<br>"
             "Professor, Robert A. Groff Chair, Department of Neurosurgery<br class=\"au-br-d\"> Drexel University College of Medicine</p>")

INTRO_TEXT = ("<p>That’s why so many neurosurgeons choose Mizuho America. We’ve built our reputation on high-quality, handcrafted products<br>"
              "with patented features backed by exceptional support. We’ve accomplished this through:</p>"
              "<ul><li>Collaborations with neurosurgical experts to help fill unmet instrumentation needs in the neurosurgery OR</li>"
              "<li>High-performance tools that meet rigorous quality protocols—with no generic designs or mass-production assembly lines</li>"
              "<li>A personalized, dedicated partnership with our customers before, during, and after the sale</li></ul>")
INTRO_CLOSE = ("<p>We’re a global leader in neurosurgery tools, and we’ll continue to maintain the high standards that have earned us the trust<br>"
               "of the neurosurgical community. Because we share your same goal: achieving the best outcomes for patients.</p>")
# (number, label, colour modifier)
# Figma tracks some numbers per character (e.g. "1" -0.1em, "," -0.05em); the spans carry that (classes in _about.scss).
LS1 = '<span class="au-ls-1">1</span>'
INTRO_STATS = [("1993", "Mizuho America, Inc. established in Boston, MA (relocated to Union City, CA, in 2010)", "blue"),
               (LS1 + '<span class="au-ls-c">,</span>800+', "neurosurgical products, including head-holding systems, instruments, microsurgery tables, and vascular management", "sky"),
               ('ISO<span class="au-ls-s"> </span>13485', "for patient safety, regulatory compliance, traceability &amp; documentation, risk management, and supplier control", "blue"),
               (LS1 + '<span class="au-ls-c">,</span>000+', "hospitals served", "sky")]

CREED = [("Honesty", "creed-honesty"), ("Contribution", "creed-contribution"), ("Solidarity", "creed-solidarity")]
PRINCIPLES = [("Customer-focused", "principle-customer"), ("Innovative", "principle-innovative"), ("Professional", "principle-professional")]
TEAM = [("yamamura", "Dean Yamamura", "President and COO"), ("delaney", "William Delaney", "Vice-President – Sales"),
        ("todd", "Bob Todd", "Regional Business Manager – Central"), ("mccart", "Chris McCart", "Regional Business Manager – West"),
        ("wilson", "Chris Wilson", "Regional Business Manager – South"), ("kritt", "Steve Kritt", "Regional Business Manager – Northeast"),
        ("hanson", "Russ Hanson", "Business Development Manager"), ("rivera", "Odriel Rivera", "Manager of Neuro<br>Latin America Sales")]

HERITAGE_TEXT = ("<p>Founded more than 100 years ago, Mizuho Corporation—Mizuho America’s parent company—has grown into a respected global "
                 "powerhouse because of its unceasing commitment to provide dependable, sophisticated, and time-tested technology for "
                 "healthcare professionals.</p><p>Established in 1993, Mizuho America reflects that commitment, becoming a trusted leader in "
                 "neurosurgery devices that you can rely on to help deliver the performance you need for your high-stakes procedures. Our "
                 "expert-driven solutions were designed to overcome barriers and facilitate a high level of surgical precision, helping to "
                 "give you greater freedom and power to evolve surgical techniques for optimal outcomes.</p>")
# (year, colour modifier) in order; 1993 is the featured milestone
YEARS = [("1919", "faint"), ("1939", "faint"), ("1959", "faint"), ("1968", "sky"), ("1976", "deep"), ("1993", "now"),
         ("2002", "deep"), ("2007", "sky"), ("2008", "faint"), ("2010", "faint"), ("2019", "faint"), ("2020", "faint"),
         ("2022", "faint"), ("2025", "faint")]
MILESTONE_1993 = "Mizuho America, Inc. is established in Boston, Massachusetts, as a sales company for neurosurgical products"

COLLAB_TEXT = ("<p>No one knows the unique demands of neurosurgery better than neurosurgeons. That’s why we’ve partnered with renowned "
               "leaders in the field to design and develop handcrafted, expertly engineered tools specially tailored to support control, "
               "efficiency, and workflow during your exacting procedures.</p>"
               "<p><strong>It all started in 1976 with Dr. Kenichiro Sugita</strong><br>That’s when this acclaimed neurosurgeon worked with "
               "Mizuho Corporation to develop the famous Sugita Clip for cerebral aneurysm. This breakthrough product went on to become a "
               "gold standard and continues to be used in countless ORs worldwide.</p>"
               "<p>Dr. Sugita continued partnering with Mizuho Corporation, and today Mizuho America proudly offers a full line of Sugita products.</p>")
EXPERTS = [
    ("lawton", "Michael T. Lawton, MD",
     "President and CEO,<br>Barrow Neurological Institute<br>Professor and Chair, Neurosurgery<br>Chief, Neurovascular Surgery",
     "LawtonElite Series, an intricately crafted, comprehensive micro instrumentation series for neurovascular and skull base procedures"),
    ("evans", "James J. Evans, MD",
     "Professor, Neurological Surgery &amp; Otolaryngology<br>Division Chief, Brain Tumor and Stereotactic Radiosurgery Division<br>"
     "Director, Cranial Base and Pituitary Surgery<br>Director, Cranial Base and Endoscopic Surgery Fellowship",
     "E3 Evans Elite Endoscopic Instruments, designed as a comprehensive set for endoscopic and minimally invasive procedures, featuring "
     "malleable instruments and suctions to provide versatility; and E3 Mithras Bipolar—instrumentation for minimally invasive endonasal surgery"),
    ("youssef", "A. Samy Youssef, MD, PhD",
     "Professor &amp; Vice Chairman for Education<br>Departments of Neurosurgery &amp; Otolaryngology<br>Director of Skull Base Surgery<br>"
     "University of Colorado School of Medicine",
     "Dr. Youssef’s Cranial Nerve Dissection Set, a comprehensive, high-quality, specialized set for nerve dissection"),
]
GLOBAL_STATS = [("15+", "sales dealers in the United States", "light"), ("15+", "distributors in Latin America", "blue"),
                ("65+", "distributors in Europe, the Middle East, and Africa", "light"), ("35+", "distributors in Asia-Pacific", "blue")]


# ------------------------------------------------------------------ sections
def stat(key, n, label, colour, extra=""):
    return con(f"{key}", f"au-stat au-stat--{colour} {extra}".strip(), [
        con(f"{key}:card", "au-stat-card", [h(f"{key}:num", "au-stat-num", n), h(f"{key}:label", "au-stat-label", label)]),
    ])


def hero():
    return con("hero", "au-hero", [
        h("hero:h1", "au-h1", "About us", "h1"),
        con("hero:media", "au-hero-media", [
            image("hero:portrait", "au-hero-portrait", "about-hero-portrait", "Erol Veznedaroglu, MD"),
            h("hero:quote", "au-hero-quote", HERO_QUOTE, "p"),
            txt("hero:cite", "au-hero-cite", HERO_CITE),
        ], **bg("about-hero-clean")),
    ])


def intro():
    return con("intro", "au-intro", [
        h("intro:h2", "au-h2 au-intro-h", "Advanced Neurosurgical tools. Enhanced customer care.", "h2"),
        txt("intro:text", "au-intro-text", INTRO_TEXT),
        con("intro:stats", "au-stats", [stat(f"intro:stat{i}", n, l, c) for i, (n, l, c) in enumerate(INTRO_STATS)]),
        txt("intro:close", "au-intro-close", INTRO_CLOSE),
        btn("intro:btn", "au-intro-btn", "Hear from our clinical collaborators", "#collaborators"),
    ])


def values(key, title, items):
    row = []
    for i, (label, icon) in enumerate(items):
        if i:
            row.append(h(f"{key}:plus{i}", "au-plus", "+"))
        row.append(con(f"{key}:v{i}", "au-value", [h(f"{key}:v{i}:label", "au-value-label", label),
                                                    image(f"{key}:v{i}:icon", "au-value-icon", icon)]))
    return con(key, f"au-value-group au-value-group--{key.split(':')[1]}", [
        h(f"{key}:title", "au-value-title", title, "h3"),
        con(f"{key}:row", "au-value-row", row),
    ])


def mission():
    return con("mission", "au-mission", [
        h("mission:h2", "au-h2 au-mission-h", "Our mission", "h2"),
        h("mission:quote", "au-mission-quote", "<em>“Collaborate with surgeons to provide high-quality neurosurgical devices in order to help "
                                               "advance surgical techniques to benefit patient health</em>.”"),
        h("mission:by", "au-mission-by", "Message from <strong>Hiroshi Nemoto</strong>, Representative Director President &amp; CEO, "
                                         "Mizuho Global Headquarters"),
        con("mission:values", "au-values", [values("mission:creed", "Our corporate creed", CREED),
                                            values("mission:principles", "Our guiding principles", PRINCIPLES)]),
        h("mission:team-h", "au-h2 au-team-h", "Mizuho-America sales team—putting our core values into action", "h2"),
        con("mission:team", "au-team", [
            con(f"team:{k}", "au-member", [image(f"team:{k}:img", "au-member-img", "team-" + k, n),
                                           h(f"team:{k}:name", "au-member-name", n, "h3"),
                                           h(f"team:{k}:role", "au-member-role", r)])
            for k, n, r in TEAM]),
    ])


def heritage():
    years = []
    for y, mod in YEARS:
        if mod == "now":
            years.append(con(f"tl:{y}", "au-yr au-yr--now", [h(f"tl:{y}:year", "au-yr-now-year", LS1 + y[1:]),
                                                              h(f"tl:{y}:text", "au-yr-now-text", MILESTONE_1993)]))
        else:
            years.append(con(f"tl:{y}", f"au-yr au-yr--{mod}", [h(f"tl:{y}:year", "au-yr-year", y)]))
    return con("heritage", "au-heritage", [
        h("heritage:h2", "au-h2 au-heritage-h", "A heritage of excellence", "h2"),
        txt("heritage:text", "au-heritage-text", HERITAGE_TEXT),
        btn("heritage:btn", "au-heritage-btn", "Explore our advanced neurosurgical products", "/products/"),
        h("tl:h2", "au-h2 au-tl-h", "100+ years of making a difference", "h2"),
        h("tl:sub", "au-tl-sub", "Milestones that paved the way for Mizuho America today"),
        con("tl", "au-tl", [
            con("tl:bar", "au-tl-bar", [h("tl:bar:corp", "au-tl-bar-label", "Mizuho Corporation"),
                                        h("tl:bar:america", "au-tl-bar-label", "Mizuho America")]),
            con("tl:years", "au-tl-years", years),
            con("tl:foot", "au-tl-foot", [h("tl:past", "au-tl-end", "Our past"), h("tl:future", "au-tl-end", "Our future")]),
        ]),
        btn("tl:btn", "au-tl-btn", "Browse the many neurosurgical procedures we support", "/products/"),
    ])


def collab():
    return con("collab", "au-collab", [
        h("collab:h2", "au-h2 au-collab-h", "Collaborations that have helped advance instrumentation", "h2"),
        con("collab:row", "au-collab-row", [
            txt("collab:text", "au-collab-text", COLLAB_TEXT),
            con("collab:sugita", "au-sugita", [image("collab:sugita:img", "au-sugita-img", "about-sugita", "Dr. Kenichiro Sugita"),
                                               h("collab:sugita:cap", "au-sugita-cap", "Dr. Kenichiro Sugita")]),
        ]),
        # Figma mobile (1:2422) repeats this CTA under the Sugita photo; desktop doesn't have it.
        btn("collab:btn-m", "au-collab-btn au-m-only", "Browse the many neurosurgical procedures we support", "/products/"),
        h("experts:h2", "au-h2 au-h2--nocase au-experts-h", "Mizuho America’s expert collaborators include:", "h2"),
        con("experts", "au-experts", [
            con(f"expert:{k}", "au-expert", [image(f"expert:{k}:img", "au-expert-img", "about-collab-" + k, n),
                                             h(f"expert:{k}:name", "au-expert-name", n, "h3"),
                                             txt(f"expert:{k}:text", "au-expert-text", f"<p>{role}</p><p><strong>Collaboration:</strong><br>{c}</p>")])
            for k, n, role, c in EXPERTS]),
        con("collab:demo", "au-demo", [btn("collab:demo-btn", "au-demo-btn", "Request a product demo", "/contact-us/")]),
    ], _element_id="collaborators")


def global_band():
    return con("global", "au-global", [
        h("global:h2", "au-global-h", "We’re proud to be an agile, forward thinking company in a trailblazing global organization", "h2"),
        h("global:sub", "au-global-sub", "Mizuho Corporation, founded and headquartered in Japan, has a worldwide presence"),
        con("global:stats", "au-gstats", [stat(f"global:stat{i}", n, l, c, "au-stat--g") for i, (n, l, c) in enumerate(GLOBAL_STATS)]),
    ], **bg("about-map-clean"))


def closing():
    return con("close", "au-close", [
        h("close:quote", "au-close-quote", "“Better instruments help you get the best patient outcome. And that’s really the name of the "
                                           "game is to try and find things, tools, that make you a better surgeon.”"),
        h("close:cite", "au-close-cite", "– Michael Lawton, MD"),
        con("close:btns", "au-close-btns", [
            btn("close:products", "au-close-btn", "Discover our wide range of products", "/products/"),
            btn("close:videos", "au-close-btn au-btn--outline", "Watch video testimonials", "/resources/"),
            btn("close:brochures", "au-close-btn au-btn--outline au-btn--dark", "Download product brochures", "/resources/", "fas fa-arrow-down"),
        ]),
    ])


def tree():
    return [con("page", "au", [hero(), intro(), mission(), heritage(), collab(), global_band(), closing()])]


def count(nodes):
    return sum(1 + count(n.get("elements", [])) for n in nodes)


def widget_types(nodes, acc=None):
    acc = {} if acc is None else acc
    for n in nodes:
        k = n.get("widgetType", n["elType"])
        acc[k] = acc.get(k, 0) + 1
        widget_types(n.get("elements", []), acc)
    return acc


if __name__ == "__main__":
    data = tree()
    out = os.path.join(ROOT, "pages/about-us/elementor/about.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("nodes:", count(data), widget_types(data))
    if "--write" in sys.argv:
        import bridge
        res = bridge.call("dev-connect-elementor-set-page-data", {"post_id": PAGE_ID, "data": data})
        print("write:", json.dumps(res)[:400])
