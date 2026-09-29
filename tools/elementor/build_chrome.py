"""Generate the Elementor Theme Builder header + footer trees (public site) from the extracted Figma spec.

Output: pages/_global/elementor/{header,footer}.json (native Elementor nodes).
Values come from pages/mizuho-home/figma/spec.md (site_header / site_footer). Every colour and every type style
references an Elementor Kit global (__globals__), and every Site Settings value is a dynamic tag, so nothing
brand-level is hardcoded. Font sizes are rem (DevCommand typography rule). Element ids are derived from a
stable name, so re-running updates the same elements instead of creating new ones.

Run: python tools/elementor/build_chrome.py
"""
import hashlib
import json
import os
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "pages", "_global", "elementor")


def eid(name):
    return hashlib.md5(name.encode()).hexdigest()[:7]


def tag(name, key, **settings):
    enc = urllib.parse.quote(json.dumps(settings, separators=(",", ":")))
    return f'[elementor-tag id="{eid(key)}" name="{name}" settings="{enc}"]'


def rem(px):
    return {"unit": "rem", "size": round(px / 16, 4)}


def px(v):
    return {"unit": "px", "size": v}


def box(t, r, b, l, unit="px"):
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": False}


def container(name, children, **s):
    base = {"content_width": "full", "flex_direction": "column", "padding": box(0, 0, 0, 0), "flex_gap": {"column": "0", "row": "0", "unit": "px", "isLinked": True}}
    base.update(s)
    base.setdefault("css_classes", "")
    return {"id": eid(name), "elType": "container", "isInner": False, "settings": base, "elements": children}


def widget(name, wtype, **s):
    if "css_classes" in s:  # Elementor widgets read "_css_classes"; only containers use "css_classes"
        s["_css_classes"] = s.pop("css_classes")
    return {"id": eid(name), "elType": "widget", "widgetType": wtype, "settings": s, "elements": []}


def g_color(k):
    return f"globals/colors?id={k}"


def g_type(k):
    return f"globals/typography?id={k}"


def custom_type(prefix, family, weight, size_px, lh, size_mobile_px=None, transform=None):
    """Custom typography for a style the Kit has no preset for (rem sizes, unitless line-height)."""
    t = {
        f"{prefix}_typography": "custom",
        f"{prefix}_font_family": family,
        f"{prefix}_font_weight": str(weight),
        f"{prefix}_font_size": rem(size_px),
        f"{prefix}_line_height": {"unit": "em", "size": round(lh, 3)},
    }
    if size_mobile_px:
        t[f"{prefix}_font_size_mobile"] = rem(size_mobile_px)
    t[f"{prefix}_text_transform"] = transform or "none"
    return t


UTILITY = dict(family="Montserrat", weight=500, size_px=13, lh=1.2)  # Gotham Medium 350 -> Montserrat 500


def text_line(name, *, title="", dyn_text=None, dyn_link=None, link=None, typo, color="text", align="left", tag_html="p", **extra):
    """A heading widget used as a single styled line (optionally dynamic text / link)."""
    s = {"title": title, "header_size": tag_html, "align": align, **typo, "__globals__": {"title_color": g_color(color)}}
    dyn = {}
    if dyn_text:
        dyn["title"] = dyn_text
    if dyn_link:
        dyn["link"] = dyn_link
    if dyn:
        s["__dynamic__"] = dyn
    if link:
        s["link"] = {"url": link, "is_external": "", "nofollow": ""}
    s.update(extra)
    return widget(name, "heading", **s)


def nav(name, menu, *, color="text", typo, layout="horizontal", gap=24, dropdown="none", align="left", **extra):
    s = {
        "menu": menu, "layout": layout, "align_items": align, "pointer": "none", "dropdown": dropdown,
        "padding_horizontal_menu_item": px(0), "padding_vertical_menu_item": px(0),
        "menu_space_between": px(gap), **typo,
        "__globals__": {"color_menu_item": g_color(color), "color_menu_item_hover": g_color("secondary"),
                        # the design marks the current page in Mizuho Blue (public 1:2861 "Clinical Resources", portal 1:2990 "Resources")
                        "color_menu_item_active": g_color("primary" if color == "text" else color)},
    }
    s.update(extra)
    return widget(name, "nav-menu", **s)


def logo(name, field, width, width_mobile=None, align="center", align_mobile=None, **extra):
    s = {
        "image": {"url": "", "id": "", "size": "full"}, "image_size": "full", "width": px(width), "align": align,
        "link_to": "custom", "link": {"url": "/", "is_external": "", "nofollow": ""},
        "__dynamic__": {"image": tag("m11-setting-image", f"{name}-tag", field=field)},
    }
    if width_mobile:
        s["width_mobile"] = px(width_mobile)
    if align_mobile:
        s["align_mobile"] = align_mobile
    s.update(extra)
    return widget(name, "image", **s)


def button(name, text, url, *, filled):
    s = {
        "text": text, "link": {"url": url, "is_external": "", "nofollow": ""}, "size": "sm",
        **custom_type("typography", "Open Sans", 700, 13, 1.36),
        "text_padding": box(4, 18, 4, 18), "border_radius": box(5, 5, 5, 5),
        "border_border": "solid", "border_width": box(2, 2, 2, 2),
    }
    if filled:
        s["__globals__"] = {"background_color": g_color("primary"), "border_color": g_color("primary"), "button_text_color": g_color("white"),
                            "button_background_hover_color": g_color("accent"), "button_hover_border_color": g_color("accent")}
    else:
        s["background_color"] = "transparent"
        s["__globals__"] = {"border_color": g_color("secondary"), "button_text_color": g_color("secondary"),
                            "button_background_hover_color": g_color("secondary"), "hover_color": g_color("white")}
    return widget(name, "button", **s)


def header():
    utility = custom_type("typography", **UTILITY)
    lang_typo = custom_type("menu_typography", **UTILITY)
    nav_typo = custom_type("menu_typography", "Open Sans", 600, 13, 1.36)

    row1 = container(
        "h-row1",
        [
            container("h-row1-left", [nav("h-lang", "language", typo=lang_typo, gap=24, css_classes="m11-lang")],
                      flex_direction="row", flex_align_items="center", hide_mobile="hidden-mobile"),
            container("h-row1-centre", [logo("h-logo", "m11_logo", 200, 118, "center", "left")],
                      flex_direction="row", flex_justify_content="center", flex_justify_content_mobile="flex-start", flex_align_items="center"),
            container("h-row1-right", [
                text_line("h-account", title="Find an Account Manager", link="/contact-us/#account-manager", typo=utility, align="right",
                          hide_mobile="hidden-mobile"),
                nav("h-burger", "primary", typo=custom_type("menu_typography", "Open Sans", 600, 16, 1.5), layout="dropdown",
                    **custom_type("dropdown_typography", "Open Sans", 600, 16, 1.5),
                    dropdown="tablet", toggle="burger", toggle_align="right", full_width="stretch",
                    hide_desktop="hidden-desktop", css_classes="m11-burger",
                    toggle_size=px(19), toggle_background_color="transparent", toggle_border_width=px(0),
                    __globals__={"toggle_color": g_color("text"), "color_menu_item": g_color("text"),
                                 "color_dropdown_item": g_color("text"), "color_dropdown_item_hover": g_color("primary")}),
            ], flex_direction="row", flex_justify_content="flex-end", flex_align_items="center", flex_gap={"column": "16", "row": "0", "unit": "px", "isLinked": False}),
        ],
        flex_direction="row", flex_align_items="center", flex_wrap_mobile="nowrap",
    )
    row1_mobile = container(
        "h-row1-mobile",
        [nav("h-lang-m", "language", typo=lang_typo, gap=24, css_classes="m11-lang"),
         text_line("h-account-m", title="Find an Account Manager", link="/contact-us/#account-manager", typo=utility, align="right")],
        flex_direction="row", flex_justify_content="space-between", flex_align_items="center",
        hide_desktop="hidden-desktop", hide_tablet="hidden-tablet", padding=box(18, 0, 0, 0),
    )
    row2 = container(
        "h-row2",
        [
            nav("h-nav", "primary", typo=nav_typo, gap=24, hide_tablet="hidden-tablet", css_classes="m11-nav",
                _flex_size="none", _margin=box(0, 0, 0, 37)),
            container("h-row2-actions", [
                widget("h-search", "search-form", skin="minimal", placeholder="Search...", button_type="none", size=px(29),
                       **custom_type("input_typography", "Open Sans", 700, 13, 1.36),
                       input_background_color="#00B3F033", border_radius=px(5), css_classes="m11-search",
                       __globals__={"input_text_color": g_color("text")}),
                button("h-portal", "Sales Portal", "/sales-hub/", filled=True),
                button("h-contact", "Contact Us", "/contact-us/", filled=False),
            ], flex_direction="row", flex_align_items="center", flex_justify_content="flex-end",
                flex_gap={"column": "10", "row": "0", "unit": "px", "isLinked": False}),
        ],
        flex_direction="row", flex_justify_content="space-between", flex_align_items="center",
        padding=box(18, 0, 0, 0), hide_mobile="hidden-mobile",
    )
    row3 = container(
        "h-row3",
        [text_line("h-phone", dyn_text=tag("m11-setting-text", "h-phone-txt", field="m11_phone"),
                   dyn_link=tag("m11-setting-link", "h-phone-lnk", field="m11_phone"),
                   typo=custom_type("typography", "Open Sans", 700, 13, 1.36), align="right")],
        padding=box(12, 0, 0, 0), hide_mobile="hidden-mobile",
    )
    root = container(
        "h-root", [row1, row1_mobile, row2, row3],
        content_width="full", padding=box(24, 26, 16, 24), padding_mobile=box(10, 20, 10, 20),
        background_background="classic", __globals__={"background_color": g_color("white")},
        css_classes="m11-site-header",
    )
    return [root]


def footer():
    white = "white"
    body = lambda px_, w=300, lh=2, m=None, prefix="typography": custom_type(prefix, "Montserrat", w, px_, lh, m)
    contact = container("f-contact", [
        text_line("f-heading", title="Contact & Support", tag_html="h2", typo={}, color=white,
                  __globals__={"title_color": g_color(white), "typography_typography": g_type("footerhead")}),
        widget("f-intro", "text-editor",
               editor='<p>Interested in a product demo? Have any questions? Want to chat? <strong><a href="/contact-us/">Contact Us.</a></strong></p>',
               **body(20, 300, 2, 18), paragraph_spacing=px(0), css_classes="m11-footer-intro",
               __globals__={"text_color": g_color(white)}),
        text_line("f-hours", dyn_text=tag("m11-setting-text", "f-hours-txt", field="m11_hours", before="Hours: "),
                  typo=body(20, 300, 1.5, 18), color=white),
        text_line("f-reach", title="Additional ways to reach us:", typo=body(25, 300, 1.6, 20), color=white,
                  _margin=box(28, 0, 4, 0)),
        text_line("f-phone", dyn_text=tag("m11-setting-text", "f-phone-txt", field="m11_phone", before="Phone: "),
                  dyn_link=tag("m11-setting-link", "f-phone-lnk", field="m11_phone"), typo=body(25, 700, 1.6, 20), color=white),
        text_line("f-fax", dyn_text=tag("m11-setting-text", "f-fax-txt", field="m11_fax", before="Fax: "),
                  typo=body(25, 700, 1.6, 20), color=white),
        text_line("f-email", dyn_text=tag("m11-setting-text", "f-email-txt", field="m11_email", before="Email: "),
                  dyn_link=tag("m11-setting-link", "f-email-lnk", field="m11_email"), typo=body(25, 700, 1.6, 20), color=white),
        text_line("f-address", dyn_text=tag("m11-setting-text", "f-address-txt", field="m11_address", before="Address: "),
                  typo=body(25, 300, 1.6, 20), color=white),
    ])
    divider = widget("f-divider", "divider", weight=px(1), gap=px(40), __globals__={"color": g_color(white)})

    def menu_col(key, heading, menu):
        return container(f"f-col-{key}", [
            text_line(f"f-col-{key}-h", title=heading, tag_html="h3", typo=body(25, 700, 2, 22), color=white),
            nav(f"f-col-{key}-nav", menu, color=white, layout="vertical", gap=0, typo=body(20, 300, 2, 16, prefix="menu_typography"),
                css_classes="m11-footer-menu"),
        ])

    menus = container("f-menus", [
        menu_col("products", "Products", "footer-products"),
        menu_col("clinical", "Clinical", "footer-clinical"),
        menu_col("company", "Company", "footer-company"),
        menu_col("support", "Support", "footer-support"),
    ], container_type="grid", grid_columns_grid={"unit": "fr", "size": 4}, grid_columns_grid_tablet={"unit": "fr", "size": 2}, grid_columns_grid_mobile={"unit": "fr", "size": 2},
        grid_rows_grid={"unit": "fr", "size": 1}, grid_gaps={"column": "36", "row": "36", "unit": "px", "isLinked": False},
        grid_auto_flow="row")

    legal_typo = body(14, 300, 2.86, 12)
    legal_menu_typo = body(14, 300, 2.86, 12, prefix="menu_typography")
    bottom = container("f-bottom", [
        container("f-bottom-left", [
            logo("f-logo", "m11_logo_reversed", 200, 150, "left", "left", _flex_size="none"),
            text_line("f-copy", dyn_text=tag("current-date-time", "f-year", date_format="custom", time_format="", custom_format="Y",
                                             before="© ", after=" Mizuho America, Inc. All rights reserved."),
                      typo=legal_typo, color=white),
        ], flex_direction="row", flex_direction_mobile="column", flex_align_items="center", flex_align_items_mobile="flex-start",
            flex_gap={"column": "24", "row": "8", "unit": "px", "isLinked": False}),
        nav("f-legal", "legal", color=white, gap=24, typo=legal_menu_typo, align="right", _flex_size="none"),
    ], flex_direction="row", flex_direction_tablet="column", flex_direction_mobile="column", flex_justify_content="space-between",
        flex_align_items="center", flex_align_items_tablet="flex-start", flex_align_items_mobile="flex-start", flex_gap={"column": "24", "row": "24", "unit": "px", "isLinked": False},
        padding=box(56, 0, 0, 0))

    root = container(
        "f-root", [contact, divider, menus, bottom],
        content_width="boxed", boxed_width=px(1240), padding=box(70, 20, 40, 20), padding_mobile=box(44, 20, 32, 20),
        background_background="classic", __globals__={"background_color": g_color("primary")},
        css_classes="m11-site-footer",
    )
    return [root]


def portal_header():
    """Sales Hub header (Figma 1:2988 via the replica): logo | rule | SALES PORTAL | Sales Hub menu | rep name | Account.
    Mobile (Figma draws the public mobile header): logo + burger (Sales Hub menu) / EN-ESP + Find an Account Manager."""
    small = custom_type("typography", "Open Sans", 400, 13, 1.36)
    left = container("ph-left", [
        logo("ph-logo", "m11_logo", 200, 118, "left", "left", _flex_size="none", link={"url": "/sales-hub/dashboard/", "is_external": "", "nofollow": ""}),
        widget("ph-rule", "divider", style="solid", weight=px(1), width=px(1), gap=px(0), css_classes="m11-ph-rule", hide_mobile="hidden-mobile",
               _flex_size="none", __globals__={"color": g_color("dotgrey")}),
        text_line("ph-label", title="Sales Portal", link="/sales-hub/dashboard/", typo=custom_type("typography", "Freeman", 400, 15, 1.33, transform="uppercase"),
                  color="primary", hide_mobile="hidden-mobile", _flex_size="none"),
    ], flex_direction="row", flex_align_items="center", flex_gap={"column": "20", "row": "0", "unit": "px", "isLinked": False}, _flex_size="none",
        css_classes="m11-ph-left")
    right = container("ph-right", [
        nav("ph-nav", "sales-hub", typo=custom_type("menu_typography", "Open Sans", 600, 13, 1.36), gap=24, hide_tablet="hidden-tablet",
            hide_mobile="hidden-mobile", css_classes="m11-nav", _flex_size="none", _margin=box(0, 0, 0, 154)),
        text_line("ph-user", dyn_text=tag("user-info", "ph-user-tag", type="display_name"), typo=small, hide_mobile="hidden-mobile",
                  _flex_size="none", css_classes="m11-ph-user"),
        text_line("ph-account", title="Account", link="/sales-hub/dashboard/#account", typo=small, css_classes="m11-ph-account",
                  hide_mobile="hidden-mobile", _flex_size="none", _margin=box(0, 0, 0, 44)),
        nav("ph-burger", "sales-hub", typo=custom_type("menu_typography", "Open Sans", 600, 16, 1.5), layout="dropdown",
            **custom_type("dropdown_typography", "Open Sans", 600, 16, 1.5), dropdown="tablet", toggle="burger", toggle_align="right",
            full_width="stretch", hide_desktop="hidden-desktop", css_classes="m11-burger", toggle_size=px(19),
            toggle_background_color="transparent", toggle_border_width=px(0),
            __globals__={"toggle_color": g_color("text"), "color_menu_item": g_color("text"), "color_dropdown_item": g_color("text"),
                         "color_dropdown_item_hover": g_color("primary")}),
    ], flex_direction="row", flex_align_items="center", flex_justify_content="flex-start", css_classes="m11-ph-right")
    row = container("ph-row", [left, right], flex_direction="row", flex_align_items="center", flex_justify_content="space-between",
                    flex_wrap_mobile="nowrap")
    utility = custom_type("typography", **UTILITY)
    row_m = container("ph-row-m", [
        nav("ph-lang-m", "language", typo=custom_type("menu_typography", **UTILITY), gap=24, css_classes="m11-lang"),
        text_line("ph-account-m", title="Find an Account Manager", link="/contact-us/#account-manager", typo=utility, align="right"),
    ], flex_direction="row", flex_justify_content="space-between", flex_align_items="center", hide_desktop="hidden-desktop",
        hide_tablet="hidden-tablet", padding=box(18, 0, 0, 0))
    root = container("ph-root", [row, row_m], content_width="full", padding=box(51, 67, 32, 42), padding_mobile=box(10, 20, 10, 20),
                     background_background="classic", __globals__={"background_color": g_color("white")}, css_classes="m11-portal-header")
    return [root]


def portal_footer():
    """Sales Hub footer (replica: Resource Library / Login): logo | Sales Hub • © year … | Sales Hub - Legal menu.
    Mobile: centred stack copy / logo / legal. (Figma's Dashboard footer centres the logo instead: normalised, issues-log.)"""
    typo = custom_type("typography", "Montserrat", 300, 14, 2.86, 12)
    left = container("pf-left", [
        logo("pf-logo", "m11_logo_reversed", 200, 200, "left", "center", _flex_size="none"),
        text_line("pf-copy", dyn_text=tag("current-date-time", "pf-year", date_format="custom", time_format="", custom_format="Y",
                                          before="Sales Hub  •  © ", after=" Mizuho America, Inc. All rights reserved."),
                  typo=typo, color="white", align_mobile="center"),
    ], flex_direction="row", flex_direction_mobile="column-reverse", flex_align_items="center",
        flex_gap={"column": "12", "row": "22", "unit": "px", "isLinked": False})
    legal = nav("pf-legal", "sales-hub-legal", color="white", gap=29, typo=custom_type("menu_typography", "Montserrat", 300, 14, 2.86, 12),
                align="right", align_items_mobile="center", _flex_size="none")
    root = container("pf-root", [left, legal], content_width="full", flex_direction="row", flex_direction_mobile="column",
                     flex_justify_content="space-between", flex_align_items="center", flex_gap={"column": "24", "row": "22", "unit": "px", "isLinked": False},
                     padding=box(45, 63, 47, 44), padding_mobile=box(44, 20, 44, 20),
                     background_background="classic", __globals__={"background_color": g_color("primary")}, css_classes="m11-portal-footer")
    return [root]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, tree in (("header", header()), ("footer", footer()), ("portal-header", portal_header()), ("portal-footer", portal_footer())):
        with open(os.path.join(OUT, f"{name}.json"), "w", encoding="utf-8") as fh:
            json.dump(tree, fh, indent=1, ensure_ascii=False)
        count = sum(1 for _ in json.dumps(tree).split('"elType"')) - 1
        print(f"{name}: {count} nodes -> pages/_global/elementor/{name}.json")
