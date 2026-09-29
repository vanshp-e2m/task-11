"""Shared helpers for the page replicas (build_resources.py, build_resource_library.py, …).

  * Page(frame_id): Figma nodes of one frame, frame-relative boxes, and TEXT → HTML with Figma's line model.
  * Css: collects rules and merges identical bodies (DevCommand's validator hard-fails 3+ selectors sharing one body).
  * compile_page(): blueprint.json → DevCommand's real compiler → copy images → DevCommand's validator.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from collections import OrderedDict
from html import escape

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figma"))
from dump_geometry import DOC, find, runs  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLUGIN = r"C:\Users\Vansh Patel\.claude\plugins\cache\dev-command\dev-command\fbe821068e44"
BLUE = "#0065B3"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("®", "").replace("’", "")).strip("-")


class Css:
    def __init__(self):
        self.blocks = OrderedDict()  # media -> OrderedDict(body -> [selectors])

    def add(self, sel, body, media=""):
        body = " ".join(body.split())
        self.blocks.setdefault(media, OrderedDict()).setdefault(body, [])
        if sel not in self.blocks[media][body]:
            self.blocks[media][body].append(sel)

    def render(self):
        out = []
        for media, rules in self.blocks.items():
            lines = [f"{', '.join(sels)} {{ {body} }}" for body, sels in rules.items()]
            out.append("\n".join(lines) if not media else media + " {\n  " + "\n  ".join(lines) + "\n}")
        return "\n".join(out) + "\n"


class Page:
    def __init__(self, frame_id):
        self.frame = find(DOC, frame_id)
        b = self.frame["absoluteBoundingBox"]
        self.fx, self.fy = b["x"], b["y"]
        self.shifts = set()

    def node(self, nid):
        return find(self.frame, nid)

    def box(self, nid):
        b = self.node(nid)["absoluteBoundingBox"]
        return (round(b["x"] - self.fx, 1), round(b["y"] - self.fy, 1), round(b["width"], 1), round(b["height"], 1))

    def y(self, nid):
        return self.box(nid)[1]

    def text(self, nid):
        return self.node(nid)["characters"]

    def fig_lines(self, nid):
        """TEXT node -> [[(text, key), ...] per line]; key = (family, weight, size, italic, ls, fill, deco, lineHeight)."""
        lines = [[]]
        for t, k in runs(self.node(nid)):
            for i, part in enumerate(t.split("\n")):
                if i:
                    lines.append([])
                if part:
                    lines[-1].append((part, k))
        return lines

    @staticmethod
    def lh_of(line, default):
        """Figma gives a line the line-height of its FIRST character (the trailing newline carries the previous run's)."""
        return round(line[0][1][7]) if line and line[0][1][7] else default

    @staticmethod
    def inline(line, link_slug=""):
        """One Figma line -> HTML: bold runs -> <strong>; blue 'Read …' runs -> links; other runs keep a size class."""
        html = ""
        for t, k in line:
            t = t.replace("\xa0", " ").replace("\u2028", " ")
            e = escape(t)
            wt, size, fill = k[1], k[2], k[5]
            if fill and fill.lower() == BLUE.lower() and t.strip().lower().startswith("read"):
                lead = e[: len(e) - len(e.lstrip())]
                html += f'{lead}<a class="more s{size:g}" href="#{link_slug or slug(t)}">{e.strip()}</a>'
            elif wt and wt >= 700:
                html += f'<strong class="s{size:g}">{e}</strong>' if e.strip() else e
            else:
                html += f'<span class="s{size:g}">{e}</span>' if size not in (None,) and e.strip() else e
        return html

    def para(self, nid, cls, tag="p", link_slug="", strip_tail=None):
        """Each Figma line becomes its own element with that line's line-height class (lh22, lh30 …).
        Figma puts each line's leading ABOVE it (baseline pitch = the next line's height); CSS splits it evenly, so a
        line whose height differs from the first line's sits (F1 - Fm)/2 too low. The shNN classes move it back."""
        out = []
        lines = self.fig_lines(nid)
        f1 = self.lh_of(lines[0], 22)
        for li, line in enumerate(lines):
            if strip_tail and li == len(lines) - 1:
                line = strip_tail(line)
            if not line:
                continue
            lh = self.lh_of(line, 22)
            sh = (lh - f1) / 2
            self.shifts.add(sh)
            cls_sh = f" sh{sh:g}".replace("-", "n").replace(".", "_") if sh else ""
            out.append(f'<{tag} class="ln lh{lh}{cls_sh}">{self.inline(line, link_slug)}</{tag}>')
        return f'<div class="{cls}">' + "".join(out) + "</div>"

    def plain(self, nid):
        return escape(self.text(nid).replace("\xa0", " ").strip())

    def br(self, nid):
        return "<br>".join(escape(s.strip()) for s in self.text(nid).replace("\xa0", " ").split("\n"))

    def shift_css(self, css, u, D, M):
        for sh in sorted(self.shifts):
            if sh:
                n = f"sh{sh:g}".replace("-", "n").replace(".", "_")
                css.add(f".{n}", f"position: relative; top: {u(sh)};", D)
                css.add(f".{n}", f"position: relative; top: {sh:g}px;", M)


def compile_page(slug_, blueprint, extra_images=(), svgs=None, font_weights=None):
    """Write blueprint + tokens, run DevCommand's compiler through the Windows wrapper, copy images, run the validator."""
    page = os.path.join(ROOT, "pages", slug_)
    fig = os.path.join(page, "figma")
    img_dir = os.path.join(fig, "images")
    os.makedirs(img_dir, exist_ok=True)
    json.dump(blueprint, open(os.path.join(page, "blueprint.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    tok = json.load(open(os.path.join(ROOT, "pages", "mizuho-home", "figma", "tokens.json"), encoding="utf-8"))
    tok["font_substitution"] = {"Gotham": "Montserrat"}  # Home gets this from its section-specs.json (issues-log #34)
    for fam, weights in (font_weights or {}).items():  # extra weights a page needs (e.g. Mukta 400 on Product Browse)
        tok["fonts"].setdefault(fam, {"weights": []})["weights"] = sorted(set(tok["fonts"][fam]["weights"]) | set(weights))
    json.dump(tok, open(os.path.join(fig, "tokens.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for name, svg in (svgs or {}).items():
        open(os.path.join(img_dir, name), "w", encoding="utf-8").write(svg)
    for f in extra_images:
        shutil.copy(os.path.join(ROOT, "pages", "mizuho-home", "figma", "images", f), os.path.join(img_dir, f))
    man = os.path.join(img_dir, "asset-manifest.json")
    if not os.path.exists(man):
        json.dump({"page_slug": slug_, "assets": []}, open(man, "w", encoding="utf-8"))
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "figma_html", "run_devcommand_compiler.py"), slug_],
                       capture_output=True, text=True, encoding="utf-8")
    open(os.path.join(ROOT, "cache", "tmp", f"{slug_}-compile.log"), "w", encoding="utf-8").write(r.stdout + r.stderr)
    if r.returncode:
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise SystemExit("compile failed")
    out_img = os.path.join(page, "html", "figma", "images")
    os.makedirs(out_img, exist_ok=True)
    for f in os.listdir(img_dir):
        if f != "asset-manifest.json":
            shutil.copy(os.path.join(img_dir, f), os.path.join(out_img, f))
    v = subprocess.run([sys.executable, os.path.join(PLUGIN, "scripts", "validate_html_output.py"), "--dir", os.path.join(page, "html")],
                       capture_output=True, text=True, encoding="utf-8")
    open(os.path.join(ROOT, "cache", "tmp", f"{slug_}-validate.json"), "w", encoding="utf-8").write(v.stdout)
    res = json.loads(v.stdout)
    print(slug_, "compiled; validator valid:", res["valid"], "violations:", [x["rule"] for x in res["violations"]])
    return res


def figma_linear(paint, w, h):
    """Figma GRADIENT_LINEAR paint → CSS linear-gradient() for a w×h box.

    Figma's handle positions are in NORMALISED box space (0..1 on each axis), so on a wide box the gradient is far
    steeper than the handles look: converting the handles as if they were pixel directions got every gradient on the
    Contact page wrong (issues-log). Here t(X, Y) is computed exactly and mapped onto CSS's gradient line."""
    import math
    p0, p1, p2 = paint["gradientHandlePositions"][:3]
    # handles → pixel vectors; the THIRD handle fixes the direction of the iso-lines (t is affine, not a projection)
    ax, ay = (p1["x"] - p0["x"]) * w, (p1["y"] - p0["y"]) * h
    bx, by = (p2["x"] - p0["x"]) * w, (p2["y"] - p0["y"]) * h
    px_, py_ = -by, bx                                      # perpendicular to the iso-line direction
    k = ax * px_ + ay * py_
    gx, gy = px_ / k, py_ / k                               # dt per pixel (so t(p0)=0, t(p1)=1, constant along B)
    c = -(p0["x"] * w * gx + p0["y"] * h * gy)
    theta = math.degrees(math.atan2(gx, -gy)) % 360
    ux, uy = math.sin(math.radians(theta)), -math.cos(math.radians(theta))
    L = abs(w * ux) + abs(h * uy)
    t_mid = gx * w / 2 + gy * h / 2 + c
    slope = L * (gx * ux + gy * uy)                         # dt per unit of CSS gradient-line position
    op = paint.get("opacity", 1)
    stops = []
    for s in paint["gradientStops"]:
        col = s["color"]
        pct = ((s["position"] - t_mid) / slope + 0.5) * 100
        stops.append(f"rgba({round(col['r'] * 255)}, {round(col['g'] * 255)}, {round(col['b'] * 255)}, {col.get('a', 1) * op:.3g}) {pct:.1f}%")
    return f"linear-gradient({theta:.1f}deg, {', '.join(stops)})"
