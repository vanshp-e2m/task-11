"""Package the ACF pages' generated HTML (Flow A replicas) as ONE static site ZIP for DevCommand's HTML→ACF pipeline.

    python tools/figma_html/package_acf_site.py   -> source/html-site/ (+ source/html-site.zip)

The pipeline (html-project-extractor → html-parser → html-acf-planner → …) takes an HTML site archive. Each replica lives in
pages/<slug>/html/ with its own css/styles.css and figma/images/, so the site is flattened to <page>.html at the root with
per-page assets (css/<slug>.css, assets/<slug>/…): some image names repeat across pages with different content (the
Resource Library draws the product photos faded, Product Browse at full strength). Inter-page links are rewritten from the
replica server's ../../<slug>/html/ form to <page>.html. About Us and Contact Us are Elementor pages, so they're left out.
"""
import os
import re
import shutil
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "source", "html-site")
PAGES = {  # replica slug -> file name in the site
    "mizuho-home": "index.html", "resources": "resources.html", "product-browse": "products.html",
    "product-main": "product-sugita-ii-head-frame.html", "product-variation-a": "product-lawtonelite-skull-base-set.html",
    "product-variation-b": "product-feather-blades.html", "sales-hub-login": "sales-hub-login.html",
    "sales-hub-dashboard": "sales-hub-dashboard.html", "resource-library": "sales-hub-resource-library.html",
}

if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "css"))
for slug, fname in PAGES.items():
    src = os.path.join(ROOT, "pages", slug, "html")
    html = open(os.path.join(src, "index.html"), encoding="utf-8").read()
    css = open(os.path.join(src, "css", "styles.css"), encoding="utf-8").read()
    html = html.replace('href="css/styles.css"', f'href="css/{slug}.css"')
    html = html.replace("figma/images/", f"assets/{slug}/")
    css = css.replace("../figma/images/", f"../assets/{slug}/")
    for other, ofile in PAGES.items():
        html = html.replace(f'href="../../{other}/html/"', f'href="{ofile}"').replace(f'href="../../{other}/html/#', f'href="{ofile}#')
    html = html.replace('href="./"', f'href="{fname}"')
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(html)
    open(os.path.join(OUT, "css", f"{slug}.css"), "w", encoding="utf-8").write(css)
    if os.path.exists(os.path.join(src, "js")):
        os.makedirs(os.path.join(OUT, "js"), exist_ok=True)
        for f in os.listdir(os.path.join(src, "js")):
            shutil.copy(os.path.join(src, "js", f), os.path.join(OUT, "js", f))  # identical header/drawer JS on every page
    shutil.copytree(os.path.join(src, "figma", "images"), os.path.join(OUT, "assets", slug))
    leftover = re.findall(r'href="\.\./\.\./[^"]+"', html)
    assert not leftover, (slug, leftover[:3])

zpath = os.path.join(ROOT, "source", "html-site.zip")
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for base, _dirs, files in os.walk(OUT):
        for f in files:
            full = os.path.join(base, f)
            z.write(full, os.path.relpath(full, OUT))
print(len(PAGES), "pages ->", zpath, f"({os.path.getsize(zpath) // 1024} KB)")
