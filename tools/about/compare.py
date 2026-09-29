"""Side-by-side + pixel diff of live sections vs the Figma export.
python tools/about/compare.py <live.png> <figma.png> <outdir> name:figTop:figH:liveTop:liveH ...
Prints the % of pixels differing by >32 (any channel) per section and writes <name>.png (figma | live | diff)."""
import sys
import os
import numpy as np
from PIL import Image, ImageChops

live, fig, out = Image.open(sys.argv[1]).convert("RGB"), Image.open(sys.argv[2]).convert("RGB"), sys.argv[3]
os.makedirs(out, exist_ok=True)
W = fig.width
for spec in sys.argv[4:]:
    name, ft, fh, lt, lh = spec.split(":")
    ft, fh, lt, lh = map(int, (ft, fh, lt, lh))
    h = max(fh, lh)
    a = fig.crop((0, ft, W, ft + h))
    b = live.crop((0, lt, W, lt + h))
    d = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > 32 else 0)
    pct = 100 * np.count_nonzero(np.asarray(d)) / (W * h)  # numpy: the pixel loop took minutes on 10k-px pages
    sheet = Image.new("RGB", (W * 3 + 20, h), "white")
    sheet.paste(a, (0, 0)); sheet.paste(b, (W + 10, 0)); sheet.paste(Image.merge("RGB", (d, d.point(lambda v: 0), d.point(lambda v: 0))), (2 * W + 20, 0))
    sheet.save(os.path.join(out, name + ".png"))
    print(f"{name:10s} fig {fh:5d} live {lh:5d}  diff {pct:5.2f}%")
