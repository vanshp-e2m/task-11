"""Native Elementor tree for Contact Us (page 16). Replaces DevConnect's draft: `dev/convert-html` turned each of the three
sections of the replica (pages/contact-us/html/) into ONE HTML widget (docs/devconnect-conversion-issues.md, Contact).

Every visible string is a native widget. The form is Elementor Pro's Form widget (real submissions, editable fields); the FAQ is
the Nested Accordion (one container per answer, FAQ schema on); the "Additional ways to contact us" lines are Site Settings
dynamic tags, so phone / fax / email / hours / address change in ONE place (Flow B) and update here, in the header and the footer.
Layout and type come from the theme partial assets/scss/pages/_contact-us.scss: the class names are the replica's (cu-*, faq-*,
bl-*), and its values are the replica's (Figma frame 1:1740, mobile 1:3157) scaled by --u.

Run:  python tools/elementor/build_contact.py            -> pages/contact-us/elementor/contact.json
      python tools/elementor/build_contact.py --write    -> also writes it to page 16 (MCP-equivalent set-page-data; see step note)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from build_chrome import eid, tag  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGE_ID = 16


def con(name, cls, children, **s):
    settings = {"content_width": "full", "css_classes": cls}
    settings.update(s)
    return {"id": eid("cu:" + name), "elType": "container", "isInner": False, "settings": settings, "elements": children}


def w(name, wtype, cls, **s):
    s["_css_classes"] = cls
    return {"id": eid("cu:" + name), "elType": "widget", "widgetType": wtype, "settings": s, "elements": []}


def h(name, cls, text, tag_html="p", **s):
    return w(name, "heading", cls, title=text, header_size=tag_html, **s)


def txt(name, cls, html):
    return w(name, "text-editor", cls, editor=html)


def setting_line(name, cls, field, before="", link=False):
    """One line of the contact card, bound to Site Settings (m11_get_setting) through the theme's dynamic tags."""
    dyn = {"title": tag("m11-setting-text", f"cu-{name}-txt", field=field, before=before)}
    if link:
        dyn["link"] = tag("m11-setting-link", f"cu-{name}-lnk", field=field)
    return w(name, "heading", cls, title="", header_size="p", __dynamic__=dyn)


def reach_line(name, label, field):
    """"Phone: <number>" — static label (text colour) + the Site Settings value as a tel:/mailto: link (link colour), as drawn."""
    return con(f"card:{name}", "ln lh32 cu-line", [h(f"{name}:label", "cu-line-label", label),
                                                   setting_line(name, "cu-line-value cu-link", field, "", True)])


def btn(name, cls, text, url):
    return w(name, "button", cls, text=text, link={"url": url, "is_external": "", "nofollow": ""}, size="sm")


# ------------------------------------------------------------------ content (verbatim Figma 1:1740, as in the replica)
BODY = ("<p class=\"cu-p\">At Mizuho America, we are committed to providing innovative tools designed to help neurosurgeons achieve the "
        "best outcomes. But our commitment extends even further. It includes unparalleled support every step of the way.</p>"
        "<p class=\"cu-p\">Want a product demo? Just ask. Have questions? We have answers. Got ideas? We’re listening.</p>"
        "<p class=\"cu-p\"><a class=\"cu-link\" href=\"#faq\"><strong>Get answers now to some of the most common questions</strong></a></p>"
        "<p class=\"cu-p\">Since opening our doors in 1993, we’ve become a trusted partner for countless neurosurgeons across the country."
        "<br>We hope to become the same for you.</p>")

STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii",
          "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
          "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
          "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
          "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
COUNTRIES = ["United States", "Canada", "Mexico", "Other"]

# (custom_id, type, label, required, autocomplete-ish extra)
FIELDS = [("first_name", "text", "First Name", True), ("last_name", "text", "Last Name", True), ("institution", "text", "Institution", False),
          ("state", "select", "State", False), ("zip", "text", "ZIP", False), ("country", "select", "Country", False),
          ("email", "email", "Email", True), ("phone", "tel", "Phone", True), ("area_of_interest", "text", "Area of interest", False)]

FAQ = [("Are your products available internationally?", None),
       ("How do I obtain service or technical support?",
        "<p>Contact our customer service or technical support team at <a class=\"cu-link\" href=\"mailto:customerservice@mizuho.com\">"
        "customerservice@mizuho.com</a> or call <a class=\"cu-link\" href=\"tel:8886992547\">888-699-2547</a> with the product name, "
        "model, and a description of the issue. We will help determine the appropriate next steps.</p>"),
       ("Where can I find product documentation?", None), ("Is my clip MRI compatible?", None),
       ("How do I place an order or request a quote?", None), ("Can I try out instruments before buying?", None),
       ("Where are these instruments made?", None), ("What are these instruments used for?", None),
       ("Where is Mizuho America based?", None)]
FAQ_OPEN = 2  # Figma draws the 2nd question expanded; the accordion only opens the FIRST by default -> data-m11-open (theme JS)

# The replica had placeholder hrefs (#bottom-link-N); the same band on Resources links to these pages.
BOTTOM = [("Discover our wide range of products", "/products/"), ("Access informative videos and brochures", "/resources/"),
          ("Learn why we’re a global leader in neurosurgical tools", "/about-us/")]


def form_widget():
    fields = []
    for cid, ftype, label, req in FIELDS:
        f = {"_id": eid("cu:f:" + cid), "custom_id": cid, "field_type": ftype, "field_label": label, "width": "100",
             "required": "true" if req else "", "css_classes": f"fld fld--{ftype}"}
        if ftype == "select":
            opts = STATES if cid == "state" else COUNTRIES
            f["field_options"] = "\n".join([f"{label}|"] + opts)  # first option = the drawn placeholder ("State" / "Country")
        else:
            f["placeholder"] = " "  # label floats inside the input (CSS :placeholder-shown), as drawn
        fields.append(f)
    fields.append({"_id": eid("cu:f:uses"), "custom_id": "uses_products", "field_type": "radio", "width": "100",
                   "field_label": "Do you currently use any Mizuho America products?", "field_options": "Yes\nNo",
                   "inline_list": "elementor-subgroup-inline", "css_classes": "cu-radio"})
    return w("form", "form", "cu-fields", form_name="Contact Us", form_fields=fields, show_labels="true", mark_required="true",
             input_size="sm", column_gap={"unit": "px", "size": 0}, row_gap={"unit": "px", "size": 0},
             button_text="Submit form", button_size="sm", button_width="", button_align="start",
             submit_actions=["email", "save-to-database"], email_subject="Contact Us form — task-11.local",
             custom_messages="yes", success_message="Thank you — we’ll be in touch shortly.",
             __dynamic__={"email_to": tag("m11-setting-text", "cu-form-mailto", field="m11_email")})


def intro():
    card = con("card", "cu-card", [
        h("card:h", "cu-card-h", "Additional ways to contact us:", "h2"),
        con("card:reach", "cu-card-block cu-card-reach", [
            reach_line("phone", "Phone:", "m11_phone"),
            reach_line("fax", "Fax:", "m11_fax"),
            reach_line("email", "Email:", "m11_email"),
        ]),
        con("card:hours", "cu-card-block cu-card-hours", [setting_line("hours", "ln lh-hours", "m11_hours", "Hours: ")]),
        con("card:addr", "cu-card-block cu-card-addr", [setting_line("addr", "ln lh-addr", "m11_address", "Address: ")]),
    ])
    return con("intro", "rs cu", [con("intro:fx", "fx", [
        h("h1", "cu-h1", "Contact us", "h1"),
        con("panel", "cu-panel", [
            con("copy", "cu-copy", [h("h2", "cu-h2", "We’re here for you before, during and after the sale", "h2"),
                                    txt("body", "cu-body", BODY)]),
            card,
        ]),
        con("formbox", "cu-form", [
            con("formhead", "cu-form-head", [h("form:intro", "cu-form-intro", "Ready to meet us? Just complete the fast form below."),
                                             h("form:note", "cu-note", '<span class="req">*</span> Indicates required field')]),
            form_widget(),
        ], _element_id="contact-form"),
    ])], _element_id="contact-intro", html_tag="section")


def faq():
    items = [{"_id": eid(f"cu:faq:{i}"), "item_title": q} for i, (q, _) in enumerate(FAQ)]
    panes = [con(f"faq:{i}:a", "faq-a" if a else "faq-a faq-a--empty", [txt(f"faq:{i}:text", "faq-a-text", a)] if a else [])
             for i, (_, a) in enumerate(FAQ)]
    acc = w("faq:list", "nested-accordion", "faq-list", items=items, default_state="all_collapsed", max_items_expended="one",
            title_tag="h3", faq_schema="yes",
            accordion_item_title_icon={"value": "", "library": ""}, accordion_item_title_icon_active={"value": "", "library": ""},
            _attributes=f"data-m11-open|{FAQ_OPEN}")
    acc["elType"] = "widget"
    acc["elements"] = panes
    return con("faq", "rs faqs", [con("faq:fx", "fx", [
        h("faq:h2", "faq-h2", "While you’re here, get answers to Frequently Asked Questions:", "h2"),
        acc,
        btn("faq:btn", "faq-btn d-only", "Complete our contact form", "#contact-form"),
        w("faq:rule", "divider", "faq-rule"),
    ])], _element_id="faq", html_tag="section")


def bottom():
    return con("bl", "rs bl", [con("bl:fx", "fx", [
        h("bl:h2", "bl-h2", "BEFORE YOU GO...", "h2"),
        con("bl:btns", "bl-btns", [btn(f"bl:{i}", f"bl-btn bl-btn--{i + 1}", t, u) for i, (t, u) in enumerate(BOTTOM)]),
    ])], _element_id="before-you-go", html_tag="section")


def tree():
    return [con("page", "m11-page-contact-us", [intro(), faq(), bottom()])]


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
    out = os.path.join(ROOT, "pages/contact-us/elementor/contact.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("nodes:", count(data), widget_types(data))
