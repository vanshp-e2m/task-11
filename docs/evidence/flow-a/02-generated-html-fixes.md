# Flow A — where the generated HTML was wrong, and what was done

Source: DevCommand `figma-html-planner` blueprint → compiled package `pages/mizuho-home/dist/`.
Raw, untouched output: `01-generated-html-raw/`. Reference: Figma section crops `pages/mizuho-home/figma/screenshots/{desktop,mobile}/`.
Method: served `dist/` on 127.0.0.1:8765, captured it with Playwright at 1440 and 430, compared each section side by side with the Figma crop
(`compare-generated-*.png`), and measured section heights and element boxes in the browser.

## Found before QA (fixed by me)
| # | Defect | How found | Fix | Verified |
|---|---|---|---|---|
| G0a | **Copy transcribed from screenshots** ("Sugita ll"→"II", straight quotes, Title Case) | Diffed 67 Figma text layers vs blueprint | Planner re-sourced every string from the Figma JSON | 71/71 strings verbatim in the rendered page |
| G0b | **No web fonts at all**: `<link>` used Google Fonts v1 syntax (`family=A\|B`) on the v2 `css2` endpoint → HTTP **400** | Headings rendered in a fallback face; network log showed the request blocked | Replaced with the theme's verified URL (one `family=` per font + italic 600) | Network: request OK; `h1` computed font Freeman; Freeman face `loaded` |

The compiler (`compile_html_blueprint.py`, line 434–439) builds this URL correctly with `&`. The broken link was **hand-written by the
agent**, bypassing its own compiler.

**My own verification mistakes along the way** (kept on purpose):
- I first "confirmed" the fonts with `document.fonts.check()`. It returns `true` when *no* matching font face exists, so it proved nothing.
- The next screenshots came from the **browser's cached** `index.html` (the fix was on disk and on the server, as `curl` showed). Fixed by
  reloading with `?v=2` and verifying against the network log, not the Font Loading API.

## QA findings on the correctly rendered page (sent to `figma-html-targeted-fixer`)
Section heights, Figma → generated. Desktop: hero 914→920 · intro 450→411 · value columns 678→794 · procedure band 555→711 ·
testimonials 1190→1036 · about 746→809. Mobile: intro 541→850 · value columns 1544→1843 · procedure 1170→1231 · testimonials 2245→2160.

| # | Sev | Section | Defect (Figma → generated) |
|---|---|---|---|
| G1 | HIGH | hero_carousel | CTA row collapses: "Request a Demo" wraps to 2 lines, "Browse by Procedure" drops below, **pagination dots missing** on desktop. Figma: one row: 2 buttons + link left, dots right. |
| G2 | HIGH | value_columns | **Order wrong**: Figma is title → icon → italic lead → body; generated is icon → title (desktop and mobile). |
| G3 | HIGH | procedure_band | **Restructured**: Figma puts the icon **left of** its text block (row per item, icon ~90px); generated stacks the icon above at ~45px. The `→` arrows on "View product →" / "See … and more →" are gone. |
| G4 | HIGH | testimonials | Pull quote far too small: Figma Freeman 34px / 3 lines centred; generated ~12px / 2 lines. "TESTIMONIALS" eyebrow undersized. |
| G5 | HIGH | all (mobile) | **Mobile type scale not applied**: headings/body keep desktop sizes (intro h2 ~52px vs Figma 36px; body 20 vs 18) → intro +309px, value columns +299px on mobile. |
| G6 | MED | about_stats | Stat label on card 1 spills outside the card; labels centred instead of left-aligned as in Figma. |
| G7 | MED | intro_statement | Paragraph line-height ~1.5; spec is 20/40 (2.0). |
| G8 | MED | page (mobile) | Horizontal overflow: document 486px wide at 430 viewport, caused by `.site-header-placeholder__cta`. |

Status: sent to the fixer (pass 1 of max 3). Results appended below.

## Pass 1 result (figma-html-targeted-fixer), and what I found when checking it
- Fixer reports G1–G8 fixed. Section heights 1440 after: hero 896 · intro 488 · value 798 · procedure 697 · testimonials 1170 · about 809;
  mobile scroll width 486 → 430.
- **My error in G7:** I quoted "20/40" for the intro paragraph. That's the *testimonials* intro. The intro body is **25/45**
  (`section-specs.json → intro_statement.elements.body`). The fixer used the correct value and flagged my mistake.
- **Bigger finding while checking the report (issue #21):** the page was compiled by `tools/figma_html/compile_blueprint.py`, a compiler
  the planner wrote itself after wrongly concluding DevCommand's wasn't installed. With DevCommand's real compiler (via
  `tools/figma_html/run_devcommand_compiler.py`), the same blueprint fails DevCommand's validator: 69 violations, 31 unfilled placeholders.
  So these fixes apply to an improvised build, not to DevCommand's output.

---
# Round 2 — DevCommand's real compiler (`pages/mizuho-home/html/`), QA by me on 2026-09-28

**Build facts (verified, not taken from the agent's report):** DevCommand `validate_html_output.py` → `valid: true`, 0 violations,
12 warnings. 0 `{{` placeholders. `:root` has #0065B3 / #00B3F0. Every Figma text string is present verbatim (my first diff script flagged
one false "missing" string: it didn't split on the Unicode line separator U+2028). Freeman loads, no broken images.
**Recipe deviation checked:** the planner kept value_columns and testimonials as escape hatches. I read `recipes.json`: `card-grid-3col`
renders only `title` + `body`, and `testimonial-grid` only `quote` + `author`. Neither can hold an icon, lead line, thumbnail, role lines or
CTA, so the deviation is justified (issue #24).

G1–G8 from round 1: fixed in this build, except G6 (below).

## Section heights, Figma → DevCommand HTML
| Section | Desktop 1440 | Mobile 430 |
|---|---|---|
| hero | 914 → 896 | 1360 → 1337 |
| intro | 450 → 429 | 541 → 594 |
| value columns | 678 → 780 | 1544 → **2127** |
| procedure band | 555 → 637 | 1170 → 1159 |
| testimonials | 1190 → 1152 | 2245 → **2457** |
| about stats | 746 → **1138** | 1450 → **1700** |

## New findings (round 2)
| # | Sev | Section | Defect | Evidence |
|---|---|---|---|---|
| H1 | HIGH | value_columns, testimonials, about_stats (mobile) | Sections keep **Figma's desktop absolute insets as side padding** on phones: 107/94px, 76/82px, 76/76px → content 229–278px wide instead of 390. Also breaks the accepted single-container rule (20px gutters). | computed `padding-left/right` at 430 |
| H2 | HIGH | about_stats (desktop) | The 3 stat cards wrap to **2 rows** (2 + 1); Figma is one row of 3 → +392px. | `compare-dc-07-about-stats.png` |
| H3 | MED | about_stats | Stat label still spills out of card 1 (label bottom 3px below the card) → G6 only half fixed | measured at 430 |
| H4 | MED | procedure_band (desktop) | Item text column too narrow: "Endoscopic Endonasal Approach" wraps to 3 lines (Figma 2), secondary links wrap more → +82px; icon ~45px vs Figma ~90px | `compare-dc-05-procedure-band.png` |
| H5 | MED | testimonials (mobile) | Missing the mobile-only "Watch what clinical experts say about us" button after the cards (in Figma 1:487) | not in DOM |
| H6 | LOW | value_columns (desktop) | ~100px extra height: larger top padding and body line-height than Figma | `compare-dc-04-value-columns.png` |

## Round 2 result (fixer, 1 pass), re-measured by me
Validator `valid: true`, 0 violations, 0 `{{`. No horizontal overflow at 430. Mobile: 2 slider dots, H5 button visible.
| Section | Desktop Figma → r1 → **r2** | Mobile Figma → r1 → **r2** |
|---|---|---|
| hero | 914 → 896 → **896** | 1360 → 1337 → **1337** |
| intro | 450 → 429 → **429** | 541 → 594 → **594** |
| value columns | 678 → 780 → **810** | 1544 → 2127 → **1763** |
| procedure band | 555 → 637 → **571** | 1170 → 1159 → **1159** |
| testimonials | 1190 → 1152 → **1152** | 2245 → 2457 → **2286** |
| about stats | 746 → 1138 → **809** (one row) | 1450 → 1700 → **1560** |
H1–H5 fixed. H6 not changed: the fixer showed every value already matches the spec, and the extra height comes from normal text wrapping in the 1240 container.

## Known gaps carried into the ACF build (not re-sent to the fixer)
Stopping the HTML fix loop here is deliberate. The ACF step rewrites this markup as template parts + SCSS partials anyway, so these get fixed there:
- **K1** desktop content left edges still differ: hero 96 · intro 107 · procedure 76 · others 120 (single-container rule only applied to 3 sections).
- **K2** procedure icons render ~45px (Figma ~90px).
- **K3** value columns +132px (desktop) / +219px (mobile) from line wrap.

**Status: Flow A step 1 (generated HTML) done.** Frozen copy: `docs/evidence/flow-a/03-generated-html-final/`.

---
# Round 3 — developer review (2026-09-28): header/footer missing + value columns "2–3 mistakes per section"
Developer compared the HTML with Figma and asked for (1) the header and footer and (2) value columns as an exact replica.
Fixed by me in `blueprint.json` (via `tools/figma_html/patch_chrome_and_value_columns.py`), compiled with DevCommand's compiler, measured at a true
1440 content width (viewport 1455, because of the 15px scrollbar: my earlier 1440-viewport checks were 15px short on right-aligned items).

| # | Where | Was wrong | Fix | Measured vs Figma |
|---|---|---|---|---|
| R1 | page | **No header / footer** (placeholders dropped) | Static replicas of 1:117 / 1:132 as `landmark` escape-hatch sections; off-canvas drawer (validator requirement) | header 161px; H1 at y194 = Figma |
| R2 | value cols | Content started at x120 (shared 1240/20 container) | Figma's own geometry: inset 107, tracks 293/315/315/316, dividers x400/715/1030 | titles/icons/text x,y exact to 0.1px |
| R3 | value cols | Leads wrapped at wrong words | Figma's hard line breaks kept (`<br>`) | all 4 leads = 2 lines |
| R4 | value cols | Icons all 100×98 | Per-icon Figma sizes 100×98, 99×90, 100×84, 100×72 in a 123px slot | text starts y177 in every card |
| R5 | value cols | Fake italic (wider) | Real Open Sans 600 italic (#26) | card 2 lead 3 → 2 lines |
| R6 | value cols | Card 4 text 246px wide | 13.3px inset is inside a border-box → width 272.6 | wraps "…our high-" like Figma |
| R7 | value cols | Card/button spacing | cards 470px, button 61px below, 293×50 r5 | button y531, section 772 (Figma 773) |
| R8 | footer | Rule/menus 14px low | Figma coordinates, not summed line heights | reach 221, rule 480, menus 531, logo 866, copyright 256/890: all = Figma |
| R9 | footer | Plain "&" | Fraunces WONK alternate (#26) | same glyph, 315px |
Validator: `valid: false`, **1 violation = the documented false positive #25** (Sass strips the quotes the validator looks for). Drawer verified in the browser:
aria-expanded toggles, lines rotate ±45°, panel slides 1009 → 0, body scroll locked, closes cleanly.
Comparisons: `compare-r3-header.png`, `compare-r3-value-columns.png`, `compare-r3-footer.png`.

---
# Round 4 — full replica rebuild (developer: "perfect replica, desktop + mobile as in Figma, fast")
All 8 sections regenerated from Figma geometry by `tools/figma_html/build_replica.py` → DevCommand compiler → validator (1 known false positive, #25).
| Width | Result |
|---|---|
| 1440 | pixel diff vs Figma export per section: 0.6–4.6% (anti-aliasing + Montserrat for Gotham) |
| 1024 | proportional scale of the 1440 layout, no overflow |
| 768 | mobile flow layout, no overflow |
| 430 | every section y/height within 7px of Figma 1:400; page 9759 vs 9748 |
Evidence: `compare-replica-desktop-1440.png`, `compare-replica-mobile-430.png`, `replica-1024.png`. Frozen build: `04-generated-html-replica/`.
Details, including two mistakes of my own, are in issues-log #27.
