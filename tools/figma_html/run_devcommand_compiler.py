"""Run DevCommand's real figma-html compiler (scripts/compile_html_blueprint.py) unchanged, on Windows.

Three compatibility shims, nothing else (issues #20, #22):
  1. `subprocess.run(["npx", ...])` can't find `npx.cmd` on Windows ([WinError 2]), so "npx" is resolved to its full path.
  2. The ACF extractor writes tokens.json `fonts` as a {family: {...}} map; the HTML compiler expects a list of
     {family, source, weights}. An adapted copy is written to pages/<slug>/figma/tokens.html.json and passed instead.
  3. (issue #22) The ACF extractor's tokens.json is shaped for the SCSS pipeline, not this compiler:
     `colors.<name>` is `{"hex": "#RRGGBB", "config_token": ..., "use": ...}` (compile_html_blueprint.py's
     `_safe_token_css_value` only unwraps a `"value"` key on a dict, so every one of our real colors would
     silently resolve to None and get dropped -> the compiled :root would fall back to DEFAULT_TOKENS'
     placeholder blue/greys instead of the project's real brand colors). There is also no `spacing`/`radii`/
     `typography`/`interaction` in the shape `merge_tokens()` expects. Remapped here into that exact shape
     (flat hex strings keyed by `config_token` when set, else the source key with underscores turned to
     hyphens), plus a small hand-picked spacing/radii/typography/interaction set matching this design
     (radius-sm 5px = every button's radius in this design; font-body Open Sans / font-heading Freeman).
     `fonts` is also fixed to substitute Gotham -> Montserrat (section-specs.json's own
     `font_substitution` mapping, applied project-wide per project-config.json) instead of asking Google
     Fonts for a family ("Gotham") it doesn't have; the Montserrat entry's weights are the union of any
     literal Montserrat weights and `tokens.json.fonts.Gotham.montserrat_weights`.

Usage: python tools/figma_html/run_devcommand_compiler.py mizuho-home
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

PLUGIN = r"C:\Users\Vansh Patel\.claude\plugins\cache\dev-command\dev-command\fbe821068e44"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

slug = sys.argv[1] if len(sys.argv) > 1 else "mizuho-home"
page = os.path.join(ROOT, "pages", slug)

# Shim 2 + 3: tokens shape.
tokens = json.load(open(os.path.join(page, "figma", "tokens.json"), encoding="utf-8"))

# --- Shim 3: colors/spacing/radii/typography/interaction, into compile_html_blueprint.py's schema ---
raw_colors = tokens.get("colors") or {}
mapped_colors = {}
for key, meta in raw_colors.items():
    if not isinstance(meta, dict) or not meta.get("hex"):
        continue
    name = meta.get("config_token") or key
    name = str(name).replace("_", "-")
    mapped_colors[name] = meta["hex"]
# Brand-accurate overrides for the generic BASE_CSS roles this design actually uses.
mapped_colors.setdefault("on-primary", "#FFFFFF")
mapped_colors.setdefault("surface", "#FFFFFF")
mapped_colors.setdefault("border", mapped_colors.get("sky", "#00B3F0"))  # every divider line in this design is sky
compiler_colors = mapped_colors

compiler_spacing = {"xs": "8px", "sm": "16px", "md": "24px", "lg": "48px", "xl": "96px"}
compiler_radii = {"sm": "5px", "md": "10px", "lg": "20px"}  # 5px = every button; 10px/20px = stat panel/card
compiler_typography = {"body": {"fontFamily": "Open Sans"}, "heading": {"fontFamily": "Freeman"}}
compiler_interaction = {"hover-mix": "85%", "focus-ring": f"0 0 0 3px {mapped_colors.get('sky', '#00B3F0')}59"}

font_substitution = tokens.get("font_substitution") or {}
try:
    section_specs = json.load(open(os.path.join(page, "figma", "section-specs.json"), encoding="utf-8"))
    font_substitution = section_specs.get("font_substitution") or font_substitution
except (OSError, json.JSONDecodeError):
    pass

raw_fonts = tokens.get("fonts") or {}
if isinstance(raw_fonts, dict):
    merged_weights = {}
    for fam, meta in raw_fonts.items():
        target = font_substitution.get(fam, fam)
        weights = list(meta.get("weights", [400]))
        if target != fam:
            weights = list(meta.get("montserrat_weights", weights))
        existing = merged_weights.setdefault(target, [])
        for w in weights:
            if w not in existing:
                existing.append(w)
    tokens["fonts"] = [
        {"family": fam, "source": "google", "weights": sorted(weights)}
        for fam, weights in merged_weights.items()
    ]

tokens["colors"] = compiler_colors
tokens["spacing"] = compiler_spacing
tokens["radii"] = compiler_radii
tokens["typography"] = compiler_typography
tokens["interaction"] = compiler_interaction

tokens_path = os.path.join(page, "figma", "tokens.html.json")
json.dump(tokens, open(tokens_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# Shim 1: resolve npx for subprocess on Windows.
_real_run = subprocess.run
NPX = shutil.which("npx") or "npx"


def _run(cmd, *args, **kwargs):
    if isinstance(cmd, list) and cmd and cmd[0] == "npx":
        cmd = [NPX] + cmd[1:]
    return _real_run(cmd, *args, **kwargs)


subprocess.run = _run

spec = importlib.util.spec_from_file_location("compile_html_blueprint", os.path.join(PLUGIN, "scripts", "compile_html_blueprint.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

sys.argv = [
    "compile_html_blueprint.py",
    "--blueprint", os.path.join(page, "blueprint.json"),
    "--recipes", os.path.join(PLUGIN, "skills", "figma-html-recipes", "recipes.json"),
    "--tokens", tokens_path,
    "--asset-manifest", os.path.join(page, "figma", "images", "asset-manifest.json"),
    "--output-dir", os.path.join(page, "html"),
]
raise SystemExit(mod._main())
