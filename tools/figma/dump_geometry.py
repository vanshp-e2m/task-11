"""Dump every node of a Figma frame from pages/_figma/file.json as one line each (frame-relative coordinates).

    python tools/figma/dump_geometry.py 1:2490 > cache/tmp/resources-desktop.txt

Per node: type, id, x,y (relative to the frame), w x h, fill (hex@opacity / IMG / GRAD), stroke, radius, effects,
auto-layout (mode/padding/gap/align), font (family weight size/line-height), letterSpacing (px), case, align,
per-character style overrides, and the full text (newlines shown as ⏎). About Us taught that letterSpacing and
style overrides must be read too (numbers use negative per-character tracking; a footer font hid in an override).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = json.load(open(os.path.join(ROOT, "pages", "_figma", "file.json"), encoding="utf-8"))["document"]


def find(node, nid):
    if node.get("id") == nid:
        return node
    for c in node.get("children", []):
        r = find(c, nid)
        if r:
            return r
    return None


def hexc(c, op=1.0):
    h = "#%02x%02x%02x" % tuple(round(c[k] * 255) for k in "rgb")
    a = c.get("a", 1) * op
    return h if a >= 0.999 else f"{h}@{a:.2f}"


def paint(p):
    if p.get("visible") is False:
        return None
    t = p["type"]
    if t == "SOLID":
        return hexc(p["color"], p.get("opacity", 1))
    if t == "IMAGE":
        return f"IMG({p.get('imageRef', '')[:8]},{p.get('scaleMode', '')})"
    if t.startswith("GRADIENT"):
        stops = ",".join(f"{hexc(s['color'])}:{s['position']:.2f}" for s in p.get("gradientStops", []))
        hp = p.get("gradientHandlePositions") or []
        hs = ";".join(f"{q['x']:.2f}/{q['y']:.2f}" for q in hp[:2])
        return f"{t[9:]}[{stops}|{hs}]"
    return t


def line(n, ox, oy, depth):
    b = n.get("absoluteBoundingBox") or {}
    x, y = round(b.get("x", 0) - ox, 1), round(b.get("y", 0) - oy, 1)
    parts = [" " * depth + n["type"][:4], n["id"], f"{x:g},{y:g}", f"{b.get('width', 0):g}x{b.get('height', 0):g}"]
    if n.get("visible") is False:
        parts.append("HIDDEN")
    fills = [f for f in (paint(p) for p in n.get("fills", [])) if f]
    if fills:
        parts.append("fill=" + "+".join(fills))
    strokes = [f for f in (paint(p) for p in n.get("strokes", [])) if f]
    if strokes:
        parts.append(f"stroke={'+'.join(strokes)}/{n.get('strokeWeight', '')}{n.get('strokeAlign', '')[:1]}")
    if n.get("cornerRadius"):
        parts.append(f"r{n['cornerRadius']:g}")
    if n.get("rectangleCornerRadii"):
        parts.append("r" + "/".join(f"{v:g}" for v in n["rectangleCornerRadii"]))
    if n.get("opacity", 1) < 1:
        parts.append(f"op{n['opacity']:.2f}")
    fx = [e for e in n.get("effects", []) if e.get("visible", True)]
    for e in fx:
        c = hexc(e["color"]) if e.get("color") else ""
        o = e.get("offset", {})
        parts.append(f"fx:{e['type'][:4]}({o.get('x', 0):g},{o.get('y', 0):g},{e.get('radius', 0):g},{e.get('spread', 0):g},{c})")
    if n.get("layoutMode"):
        parts.append("AL:{}(p{:g}/{:g}/{:g}/{:g} gap{:g} {}/{})".format(
            n["layoutMode"][0], n.get("paddingTop", 0), n.get("paddingRight", 0), n.get("paddingBottom", 0), n.get("paddingLeft", 0),
            n.get("itemSpacing", 0), n.get("primaryAxisAlignItems", "MIN")[:3], n.get("counterAxisAlignItems", "MIN")[:3]))
    if n.get("clipsContent"):
        parts.append("clip")
    if n["type"] == "TEXT":
        s = n.get("style", {})
        parts.append(f"{s.get('fontFamily', '')[:6]}{s.get('fontWeight', '')}{'i' if s.get('italic') else ''} "
                     f"{s.get('fontSize', 0):g}/{s.get('lineHeightPx', 0):.4g}")
        if s.get("letterSpacing"):
            parts.append(f"ls{s['letterSpacing']:.3g}")
        if s.get("textCase"):
            parts.append(s["textCase"][:5])
        if s.get("textDecoration"):
            parts.append(s["textDecoration"][:5])
        parts.append(s.get("textAlignHorizontal", "LEFT")[:1])
        ov = n.get("styleOverrideTable") or {}
        if ov:
            o = []
            for k, v in ov.items():
                o.append(k + ":" + ",".join(f"{kk}={vv if not isinstance(vv, (list, dict)) else '…'}" for kk, vv in v.items()
                                         if kk in ("fontFamily", "fontWeight", "fontSize", "italic", "letterSpacing", "textDecoration", "textCase", "fills")))
            parts.append("OV{" + " ; ".join(o) + "}")
        parts.append('"' + n.get("characters", "").replace("\n", "⏎") + '"')
    else:
        parts.append(n.get("name", "")[:40])
    return " ".join(str(p) for p in parts)


def walk(n, ox, oy, depth, out):
    out.append(line(n, ox, oy, depth))
    for c in n.get("children", []):
        walk(c, ox, oy, depth + 1, out)


if __name__ == "__main__":
    frame = find(DOC, sys.argv[1])
    b = frame["absoluteBoundingBox"]
    out = []
    walk(frame, b["x"], b["y"], 0, out)
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(out))


def runs(n):
    """Split a TEXT node into [(text, key)] runs; key = (family, weight, size, italic, letterSpacing, fill, decoration, lineHeightPx)."""
    chars = n.get("characters", "")
    ov = n.get("characterStyleOverrides") or []
    table = n.get("styleOverrideTable") or {}
    base = n.get("style", {})
    base_fill = n.get("fills", [{}])[0].get("color") if n.get("fills") else None
    out = []
    for i, ch in enumerate(chars):
        k = ov[i] if i < len(ov) else 0
        st = dict(base)
        fill = base_fill
        if k and str(k) in table:
            t = table[str(k)]
            st.update({kk: vv for kk, vv in t.items() if kk != "fills"})
            if t.get("fills"):
                fill = t["fills"][0].get("color")
        key = (st.get("fontFamily"), st.get("fontWeight"), st.get("fontSize"), bool(st.get("italic")),
               round(st.get("letterSpacing", 0) or 0, 3), hexc(fill) if fill else None, st.get("textDecoration"),
               st.get("lineHeightPx"))
        if out and out[-1][1] == key:
            out[-1][0] += ch
        else:
            out.append([ch, key])
    return [(t, k) for t, k in out]


def node(nid):
    return find(DOC, nid)
