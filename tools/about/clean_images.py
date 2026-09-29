"""Rebuild the two About background images from the approved 1x export, with the live text removed.

The Figma token expired (issues-log #28), so images are cropped from the export. Two of those crops had
page text baked into them, which would duplicate the live (editable) widgets on top:
  * about-map   (node 1:186, 1440x960): heading + subtitle, and the tops of the 4 stat cards
  * about-hero  (node 1:357, 1247x600): portrait, quote and attribution over the left gradient
The text/portrait pixels are masked and inpainted (OpenCV Telea); the stat-card band fades to the navy band.
"""
import os
import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXP = cv2.imread(os.path.join(ROOT, "pages/_figma/frames/export/About Us with Copy - Approved.png"))
OUT = os.path.join(ROOT, "pages/about-us/figma/images")


def text_mask(img, box, bright=True, thr=40, grow=4):
    x0, y0, x1, y1 = box
    roi = img[y0:y1, x0:x1].astype(np.int16)
    blur = cv2.GaussianBlur(roi, (0, 0), 6)
    d = (roi - blur).max(axis=2) if bright else (blur - roi).max(axis=2)
    m = np.zeros(img.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = (d > thr).astype(np.uint8) * 255
    return cv2.dilate(m, np.ones((grow * 2 + 1, grow * 2 + 1), np.uint8))


# ---- map: frame y 6130..7090
mp = EXP[6130:7090, 0:1440].copy()
m = text_mask(mp, (80, 40, 1360, 185), bright=True, thr=35, grow=5)
mp = cv2.inpaint(mp, m, 9, cv2.INPAINT_TELEA)
navy = np.array([0x42, 0x28, 0x00], np.float32)  # BGR #002842
top = 790
for y in range(top, 960):
    t = min(1.0, (y - top) / (883 - top))
    mp[y] = (mp[top - 1].astype(np.float32) * (1 - t) + navy * t).astype(np.uint8)
cv2.imwrite(os.path.join(OUT, "about-map-clean.jpg"), mp, [cv2.IMWRITE_JPEG_QUALITY, 88])

# ---- hero: frame x 94..1341, y 277..877
hr = EXP[277:877, 94:1341].copy()
m = text_mask(hr, (25, 340, 560, 575), bright=False, thr=30, grow=4)
m[140:333, 45:212] = 255          # portrait 145..299 x 422..603 (+ shadow)
hr = cv2.inpaint(hr, m, 12, cv2.INPAINT_TELEA)
cv2.imwrite(os.path.join(OUT, "about-hero-clean.jpg"), hr, [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok")
