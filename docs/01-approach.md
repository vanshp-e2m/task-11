# Approach — Module 11 capstone (Mizuho America design)

## 1. What the Figma file contains
File `jSb9GvLZzl7AFll93svlAE`: 11 desktop pages (1440 px), each with a mobile frame (430 px). **No tablet frames.**
Only **Home** and **About Us** are marked *"with Copy - Approved"*; the rest (Resources, Contact, Product Browse,
3 product-page variations, Login, Dashboard, Resource Library) are unapproved or portal screens.

**Home (1:9), 7 blocks:** Top Nav · Hero (heading + 2-card product carousel + 3 CTAs + intro text) ·
"Why Mizuho" (4 value columns with icons) · Browse by Procedure (blue band, 3 procedures + dropdown CTA) ·
Testimonials (3 video cards + pull quote) · About Mizuho (text + 3 stat cards) · Footer (contact block + 4 link columns + legal bar).

**About Us (1:161):** shares Top Nav, Footer and the stats block with Home, and adds Leadership, Milestone map,
Collaborations, Global map and Bottom links.

**Tokens:** blue `#0065b3`, sky `#00b3f0`, navy `#002842`, text `#090909`.
Fonts: **Freeman** (headings), **Open Sans**, **Mukta**, which are all on Google Fonts, and **Gotham**, which is commercial.

## 2. Proposed scope and split
| | Page | How | Why |
|---|---|---|---|
| **Flow A** | Home | Figma → generated HTML → DevCommand ACF pipeline → **ACF Flexible Content**, one template part + one SCSS partial per layout, page populated through DevConnect | Matches the rubric's "structure and conventions". Repeating, structured content (cards, stats, testimonials) is safest as fields. |
| **Flow B** | About Us | DevCommand **Elementor** pipeline, native widgets only (no HTML widget) | The lead asked for Elementor. A second page proves the globals work across two build methods. |
| **Global (both)** | Header + Footer | **Elementor Theme Builder** templates, applied site-wide | Built once, updated everywhere, including on the ACF-coded page |
| **Global (both)** | Colours + typography | **Elementor Site Settings (Kit)**. SCSS reads Elementor's `--e-global-color-*` variables | One source of truth for brand values |
| **Global (both)** | Phone, fax, email, address, hours, socials, logo, CTA links | **ACF options page "Site Settings"**, read in Elementor through dynamic tags and in PHP through `m11_get_setting()` | Change the phone once → header + footer + any CTA update |

The phone `800-699-2547` appears in both the header and the footer, which makes it the natural "one value updates many places" demo.

## 3. Build order (one step at a time, with a check at each gate)
0. ✅ Environment, tooling, repo, docs
1. **Extraction**: section inventory, tokens, assets, mobile frames → `pages/home/figma/`. Save the raw output as evidence.
2. **Generated HTML** (Flow A input) → `pages/home/html/` + QA against the Figma frame. Save it *before* fixing anything.
3. **Foundation**: Elementor Kit (colours, fonts), ACF Site Settings fields, Theme Builder header + footer, menus
4. **Flow A**: ACF field groups (Local JSON committed) → template parts + SCSS → Home page assembled via DevConnect
5. **Flow B**: About Us in Elementor, consuming the same globals
6. **Robustness pass**: double-length heading, empty optional fields, wrong-ratio images, per section
7. **Responsive pass**: 1440 / 768 / 430 next to the Figma frames (tablet has no frame, so it's judged on layout sanity)
8. **Maintenance ticket** on a different-builder site, *once received*
9. Packaging: theme zip, DB export, evidence index, decision record, submission index, Loom script

Snapshot before every destructive step; log every tooling mistake in `issues-log.md` as it happens.

## 4. Constraints (from the brief)
- Claude Code with CLAUDE.md + skills doing real work throughout
- Never point tooling at a client site (only `task-11.local`)
- Snapshot before destructive operations
- Commit ACF Local JSON

## 5. What is assessed, and how each item gets proven
| Area (weight) | What we must be able to show |
|---|---|
| Editability (25) | Every text, image, link and button editable in wp-admin; nothing hardcoded in templates |
| Fidelity & responsiveness (20) | Matches at desktop/tablet/mobile; survives long headings, empty optional fields, wrong-ratio images |
| Structure & conventions (20) | Template part + SCSS partial per layout, Local JSON committed, `m11_` prefix, escaped output |
| Global settings (10) | One change → multiple places, shown live |
| Safe working (15) | Snapshots, verification, no regressions, a usable change note |
| Explanation (10) | Walkthrough, decision record, issues log: where the tooling was wrong and how it was fixed |

Done when: Flow A and Flow B each produce an editable page · the maintenance ticket is done with no regressions ·
every step can be walked through · DevConnect vs DevCommand explained in my own words.

## 6. Open decisions
1. Confirm the scope: Home = Flow A (ACF), About Us = Flow B (Elementor).
2. Gotham substitute: a free lookalike (e.g. **Montserrat**) unless a licence and font files are provided.
3. Maintenance ticket and its site: not received yet.
4. The hero "carousel" shows 2 cards and 3 dots: build it as a real slider (Swiper) or as static cards?

## 7. Design problems already spotted (to handle, not to copy blindly)
- Several text layers have a **line-height smaller than the font size** (Open Sans 64/36, 48/20). Copying them literally would make lines overlap → use sensible line-heights and note it.
- Body copy mixes **Open Sans and Gotham** at similar sizes. Probably designer drift → consolidate to one body stack and note it.
- There are no tablet frames, so tablet behaviour is our own decision and gets documented.
