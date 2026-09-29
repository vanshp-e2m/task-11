# Step 1 — Figma extraction review (mizuho-home, Flow A)

**Tool:** DevCommand `acf-figma-design-extractor`, Figma REST API. **Output (raw, unedited = evidence):** `pages/mizuho-home/figma/`
(`section-specs.json`, `spec.md`, `tokens.json`, `images/`, `screenshots/desktop|mobile/`). Validator: `valid: true`, 0 errors,
8 warnings ("spacing derived from absolute coordinates": the desktop frame uses no auto-layout).

## Attempt 1 was refused
The extractor stopped on its homepage guard (issue #8). Re-run as the inner page `mizuho-home`.

## Sections the extractor found (desktop → mobile node)
| # | Layout | Desktop → mobile | Notes |
|---|---|---|---|
| 0 | `site_header` (global) | 1:117 → 1:401 | Mobile = hamburger; no design for the open menu |
| 1 | `hero_carousel` | 1:81 (part) → 1:411 | 2 slides, 3 dots |
| 2 | `intro_statement` | 1:81 (part) → 1:439 | **Split out of the same Figma group as the hero** |
| 3 | `value_columns` | 1:31 → 1:445 | 4 columns + brochures button |
| 4 | `procedure_band` | 1:145 → 1:471 | Blue band, 3 procedures |
| 5 | `testimonials` | 1:57 → 1:487 + 1:518 | Mobile splits the pull quote into its own frame |
| 6 | `about_stats` | 1:10 → 1:524 | 3 stat cards |
| 7 | `site_footer` (global) | 1:132 → 1:545 | Contact block + 4 menu columns + legal |

## What I verified myself (not taken on trust)
| Claim | How I checked | Result |
|---|---|---|
| "Main Intro Section" (1:81) is two visual sections | Figma render + mobile file has two frames | ✅ correct, split at y≈1091 |
| The divider sits at the bottom of the intro, not between hero and intro | `1:104` y = 1492 = bottom of group 1:81 | ✅ correct (my own outline had assumed otherwise) |
| Stray black square around the right card's arrow | `1:113` has a visible 1px #000 stroke | ✅ correct → a design artefact; won't be reproduced |
| Hidden divider above About | `1:11` `visible: false` | ✅ correct |
| Stat row not centred | cards at x 76 / 446 / 815, width 421 → 76px left vs 204px right | ✅ correct |
| Footer heading is Fraunces | Every text node in the footer is Gotham… **but** node 1:144 carries per-character style overrides: run 1 = Fraunces 700/34 "Contact & Support" | ✅ correct. **My first check was wrong**: I only read each layer's base style. |

## Conversion traps found here (things a naive converter would get wrong)
1. **One Figma group = two sections** (hero + intro). A one-group-one-layout conversion would merge them.
2. **One text layer = heading + paragraph** (footer 1:144, mixed-style runs). It has to become two fields.
3. **"Watch now" buttons are text runs laid over rectangles**, not real buttons → they become real link fields.
4. **All mobile frames are named "hero-m"**, so name-based desktop↔mobile matching would pair them wrongly. They were mapped by content.
5. **3 dots for 2 slides.** Dots must come from the real slide count, not the design.

## Tooling problem found
- **#9 Figma render endpoint rate-limited (~4.6 days).** Parallel render calls exhausted a "low"-tier budget. The full-frame
  renders already cached in `pages/_figma/frames/` (Home + About, desktop + mobile) are the QA reference from now on.

## Design decisions (flags from the extractor): all recommendations ACCEPTED by the developer, 2026-09-25
| Flag | Recommendation |
|---|---|
| No common container (left edges 76–114px), stat row off-centre, uneven gaps | Normalise to **one container** and a consistent section spacing scale; centre the stat row |
| Line-height < font-size (stat numbers 64/36) | Use ~1.1 line-height; record the deviation |
| Five font families (Freeman, Open Sans, Mukta, Gotham→Montserrat, Fraunces) | Keep all as designed (all free except Gotham); Fraunces only for the footer heading |
| Stray black stroke, hidden duplicates, stacked old fills | Ignore (designer leftovers) |
| Copy typos ("Sugita ll", "Ahem Avenue", "Sale Hub") | Enter the content as in the design, but list the typos for the lead. Content is editable, so the fix is a wp-admin edit, not code |
| Logo is a CMYK JPEG, no vector | Convert to an sRGB PNG for now; ask the lead for an SVG |
| Value icons are ~56px rasters shown at 100px (blurry) | Use them as supplied for now, ask for originals; the icon field is an image, so they're swappable later |
| No open-menu design for mobile | Standard off-canvas menu using the design's colours; documented as our decision |
| Mobile hero stacks both slides with the dots underneath | Real one-slide-at-a-time slider on mobile (dots become functional) |

**Status:** accepted as a set. These are deliberate deviations from the Figma; each one is listed in the decision record under
"what I deliberately changed".
| Procedure band items unevenly spaced (481px then 378px) | **Accepted in Step 2a:** three equal columns |
