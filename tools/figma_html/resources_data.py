"""Resources page (Figma 1:2490 desktop / 1:559 mobile): the page STRUCTURE as Figma node ids.

No copy is typed here. build_resources.py reads every string, colour run and box from pages/_figma/file.json by these ids,
so the HTML can't drift from Figma (issue #17 was screenshot-transcribed copy). Images are cropped from the 1x export by
resources_images.py (Figma token expired, #28), using the same ids for their boxes.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figma"))
from dump_geometry import DOC, find, runs  # noqa: E402

FRAME = find(DOC, "1:2490")
FX, FY = FRAME["absoluteBoundingBox"]["x"], FRAME["absoluteBoundingBox"]["y"]


def node(nid):
    return find(FRAME, nid)


def box(nid):
    """Frame-relative (x, y, w, h) of a node."""
    b = node(nid)["absoluteBoundingBox"]
    return (round(b["x"] - FX, 1), round(b["y"] - FY, 1), round(b["width"], 1), round(b["height"], 1))


def text(nid):
    return node(nid)["characters"]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("®", "").replace("’", "")).strip("-")


# ---------------------------------------------------------------- intro 1:2841
INTRO = dict(h1="1:2851", card="1:2842", h2="1:2843", body="1:2844", btn1_box="1:2847", btn1="1:2848",
             btn2_box="1:2849", btn2="1:2850", video="1:2852", play="1:2854", quote="1:2845", cite="1:2846")

# ---------------------------------------------------------------- testimonials (1:2800 "Case Study section")
# rows (separated by sky lines) -> experts (bio + videos) -> video = (thumbnail rect, caption text or None).
# Sauvageau + Hanel share ONE caption under their two videos (desktop: spans both columns; mobile: after both).
TESTI_H2 = "1:2829"
TESTI_ROWS = [
    [dict(bio="1:2806", videos=[("1:2817", "1:2801"), ("1:2825", "1:2810")]),
     dict(bio="1:2814", videos=[("1:2827", "1:2812")]),
     dict(bio="1:2815", videos=[("1:2830", "1:2805")])],
    [dict(bio="1:2808", videos=[("1:2820", "1:2804")]),
     dict(bio="1:2809", videos=[("1:2826", None), ("1:2831", None)], caption="1:2811"),
     dict(bio="1:2816", videos=[("1:2828", "1:2813")])],
    [dict(bio="1:2807", videos=[("1:2818", "1:2802"), ("1:2819", "1:2803")])],
]
TESTI_LINES = ["1:2840", "1:2838", "1:2839"]  # section top, after row 1, after row 2
PLAY_BY_RECT = {  # play-icon vector drawn over each thumbnail (baked into the export crop)
    "1:2817": "1:2821", "1:2825": "1:2832", "1:2827": "1:2836", "1:2830": "1:2834",
    "1:2820": "1:2824", "1:2826": "1:2833", "1:2831": "1:2835", "1:2828": "1:2837",
    "1:2818": "1:2822", "1:2819": "1:2823",
}

# ---------------------------------------------------------------- fast facts 1:2785 + 1:2795
FACTS_H2 = "1:2786"
FACTS = [("1:2789", "1:2791", "1:2787"), ("1:2790", "1:2793", "1:2788"), ("1:2796", "1:2798", "1:2797")]  # title, frame, caption
FACTS_PLAY = {"1:2791": "1:2792", "1:2793": "1:2794", "1:2798": "1:2799"}
FACTS_END_LINE = "1:2784"

# ---------------------------------------------------------------- downloadable brochures 1:2512
# kind: "grid" (heading + a row of covers) | "pair" (two half-width entries, each heading + one cover).
# btn_inset: the download badge sits 16px lower (groups whose first cover is the wide 237px crop).
# mobile: "grid" (2 columns, card scaled 0.85 as in Figma 1:559) | "stack" (single column, full size).
# caption: "title" (bold title + Read description) | "excerpt" (light excerpt + Read description).
BRO_H2 = "1:2782"
BRO_GROUPS = [
    dict(kind="grid", text="1:2746", line="1:2740", mobile="grid",
         cards=[("1:2747", "1:2741"), ("1:2748", "1:2742"), ("1:2749", "1:2743"), ("1:2750", "1:2744"), ("1:2751", "1:2745")]),
    dict(kind="grid", text="1:2717", line="1:2713", mobile="grid",
         cards=[("1:2718", "1:2714"), ("1:2719", "1:2715"), ("1:2720", "1:2716")]),
    dict(kind="grid", text="1:2690", line="1:2686", mobile="grid", btn_inset=True,
         cards=[("1:2691", "1:2687"), ("1:2692", "1:2688"), ("1:2693", "1:2689")]),
    dict(kind="pair", line="1:2666", mobile="stack", btn_inset=True, caption="excerpt",
         halves=[("1:2669", ("1:2671", "1:2667")), ("1:2670", ("1:2672", "1:2668"))]),
    dict(kind="pair", line="1:2646", mobile="stack", btn_inset=True, caption="excerpt",
         halves=[("1:2649", ("1:2651", "1:2647")), ("1:2650", ("1:2652", "1:2648"))]),
    dict(kind="grid", text="1:2630", line="1:2627", mobile="stack", btn_inset=True,
         cards=[("1:2631", "1:2628"), ("1:2632", "1:2629")]),
    dict(kind="grid", text="1:2597", line="1:2592", mobile="grid",
         cards=[("1:2598", "1:2593"), ("1:2599", "1:2594"), ("1:2600", "1:2595"), ("1:2601", "1:2596")]),
    dict(kind="pair", line="1:2572", mobile="stack", btn_inset=True, caption="excerpt",
         halves=[("1:2575", ("1:2577", "1:2573")), ("1:2576", ("1:2578", "1:2574"))]),
    # No heading. Desktop reads row by row; Figma mobile reads it column by column (mobile_order), and repeats the
    # T2 Clips card as an 8th item (1:992). The duplicate is NOT reproduced (same brochure twice); see issues-log.
    dict(kind="grid", text=None, line="1:2513", mobile="grid", mobile_order=[1, 3, 5, 6, 7, 2, 4],
         cards=[("1:2522", "1:2515"), ("1:2524", "1:2517"), ("1:2526", "1:2519"), ("1:2527", "1:2520"), ("1:2528", "1:2521"),
                ("1:2523", "1:2516"), ("1:2525", "1:2518")]),
]


def badge_for(rect_id):
    """The 'download button' group drawn over a cover: the one whose box starts nearest the cover's top-left."""
    x, y, w, h = box(rect_id)
    best = None
    grp = node("1:2512")

    def walk(n):
        nonlocal best
        if n.get("name") == "download button":
            b = n["absoluteBoundingBox"]
            bx, by = b["x"] - FX, b["y"] - FY
            if x - 20 <= bx <= x + 20 and y - 20 <= by <= y + 30:
                d = abs(bx - x) + abs(by - y)
                if best is None or d < best[0]:
                    best = (d, (round(bx, 1), round(by, 1), round(b["width"], 1), round(b["height"], 1)))
        for c in n.get("children", []):
            walk(c)
    walk(grp)
    return best[1] if best else None


# ---------------------------------------------------------------- bottom links 1:2504
BOTTOM = dict(h2="1:2511", buttons=[("1:2505", "1:2507"), ("1:2506", "1:2508"), ("1:2509", "1:2510")])
