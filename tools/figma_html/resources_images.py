"""Crop every Resources image from the approved 1x export (Figma token expired, issues-log #28) and remove what the
export baked on top of it, because the page draws those itself:
  * video thumbnails + the intro video: the white play-circle icon (only its white strokes are masked, so the
    photo under the transparent middle of the icon survives);
  * brochure covers: the white/sky "download" badge in the top-left corner (whole disc masked).
Masked pixels are inpainted with OpenCV Telea (same approach as tools/about/clean_images.py).

    python tools/figma_html/resources_images.py        -> pages/resources/figma/images/*.jpg + asset-manifest.json
"""
import json
import os

import cv2
import numpy as np

from resources_data import (BRO_GROUPS, FACTS, FACTS_PLAY, INTRO, PLAY_BY_RECT, TESTI_ROWS, badge_for, box, slug, text)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXP = cv2.imread(os.path.join(ROOT, "pages/_figma/frames/export/Resources.png"))
OUT = os.path.join(ROOT, "pages/resources/figma/images")
os.makedirs(OUT, exist_ok=True)


def crop(rect):
    x, y, w, h = box(rect)
    x0, y0 = int(round(x)), int(round(y))
    return EXP[y0:y0 + int(round(h)), x0:x0 + int(round(w))].copy(), (x0, y0)


def mask_play(img, origin, vec):
    """White strokes of the play icon inside its box (+3px), grown by 2px."""
    vx, vy, vw, vh = box(vec)
    x0, y0 = int(vx - origin[0]) - 3, int(vy - origin[1]) - 3
    x1, y1 = x0 + int(vw) + 7, y0 + int(vh) + 7
    roi = img[max(0, y0):y1, max(0, x0):x1]
    white = (roi.min(axis=2) > 185).astype(np.uint8) * 255
    m = np.zeros(img.shape[:2], np.uint8)
    m[max(0, y0):y1, max(0, x0):x1] = white
    return cv2.dilate(m, np.ones((5, 5), np.uint8))


def mask_badge(img, origin, badge):
    bx, by, bw, bh = badge
    cx, cy = bx - origin[0] + bw / 2, by - origin[1] + bh / 2
    m = np.zeros(img.shape[:2], np.uint8)
    cv2.circle(m, (int(round(cx)), int(round(cy))), int(bw / 2) + 3, 255, -1)
    return m


def first_line(nid):
    return text(nid).split("\n")[0].strip()


assets = []


def save(img, name, rect, role, m=None):
    if m is not None and m.any():
        img = cv2.inpaint(img, m, 5, cv2.INPAINT_TELEA)
    cv2.imwrite(os.path.join(OUT, name), img, [cv2.IMWRITE_JPEG_QUALITY, 90])
    x, y, w, h = box(rect)
    assets.append({"file": name, "name": name, "type": "raster", "method": "crop of the approved 1x export (#28)",
                   "figmaNodes": [f"{rect} ({w:g}x{h:g})"], "role": role, "containsLiveText": False,
                   "cleaned": "play icon removed" if "video" in name else ("download badge removed" if m is not None else "none")})


# intro video (1:2852) + its play icon (1:2854)
img, o = crop(INTRO["video"])
save(img, "video-intro-lawton.jpg", INTRO["video"], "intro video thumbnail", mask_play(img, o, INTRO["play"]))

# testimonial thumbnails
for row in TESTI_ROWS:
    for ex in row:
        for i, (rect, cap) in enumerate(ex["videos"]):
            label = first_line(cap) if cap else first_line(ex.get("caption")) + f"-{i + 1}"
            if label.lower() == "extended version":
                label = first_line(ex["videos"][0][1]) + " extended"
            img, o = crop(rect)
            save(img, "video-" + slug(label.replace("Topic:", "")) + ".jpg", rect, "testimonial video thumbnail",
                 mask_play(img, o, PLAY_BY_RECT[rect]))

# fast facts
for title, frame, _cap in FACTS:
    img, o = crop(frame)
    save(img, "video-fact-" + slug(first_line(title))[:60].strip("-") + ".jpg"  # same 60-char cut as build_resources.img_name (issues-log #51)
         , frame, "fast-facts video thumbnail", mask_play(img, o, FACTS_PLAY[frame]))

# brochure covers
for g in BRO_GROUPS:
    cards = g["cards"] if g["kind"] == "grid" else [h[1] for h in g["halves"]]
    for rect, cap in cards:
        name = first_line(cap)
        if g.get("caption") == "excerpt":  # excerpt captions: name the file after the entry heading instead
            heading = [h[0] for h in g["halves"] if h[1][0] == rect][0]
            name = first_line(heading)
        img, o = crop(rect)
        save(img, "brochure-" + slug(name)[:60].strip("-") + ".jpg", rect, "brochure cover", mask_badge(img, o, badge_for(rect)))

json.dump({"page_slug": "resources", "assets": assets}, open(os.path.join(OUT, "asset-manifest.json"), "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
names = [a["file"] for a in assets]
assert len(names) == len(set(names)), "duplicate image names"
print(len(assets), "images")
