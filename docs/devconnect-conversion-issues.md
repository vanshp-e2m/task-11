# Where DevConnect didn't get it right — per page, per section

How each page is produced: Figma → semantic HTML (`pages/<slug>/html/`) → **DevConnect `dev/convert-html` (builder: elementor)** →
**`dev/build-page`** into the WordPress page = *the DevConnect draft*. Raw outputs are kept in `pages/<slug>/devconnect/`.
Screenshots of each draft are in `docs/evidence/`. Everything below was then fixed by me (how is noted per item).

---

## About Us (page 15, `/about-us/`) — draft built 2026-09-28

**Input:** `pages/about-us/html/about.html` (10,057 chars, 7 `<section>`s, every string verbatim from Figma 1:161).
**Output:** `pages/about-us/devconnect/01-convert-html-output.json`. Draft screenshot: `docs/evidence/flow-b/about-devconnect-draft-1440.png`.

### Page-level problems (affect every section)
| # | What DevConnect did | Why it's wrong | Fix |
|---|---|---|---|
| D1 | `convert-html` returned **7 `html` widgets**, one per `<section>`, and **0 native widgets** | Nothing is editable in the Elementor editor: an editor sees 7 code boxes, not headings/text/images. Fails the brief's editability requirement (25%) and DevCommand's own "no HTML widget" rule | Rebuilt as native Elementor containers + heading / text-editor / image / button widgets |
| D2 | `dev/elementor-validate-conversion` → `valid: true, issues: []` on that tree | The validator only checks structure (ids, JSON), so an all-HTML-widget page "passes" | Don't trust it for quality; count widget types and look at the page |
| D3 | `update-page-settings {template: elementor_header_footer, hide_title}` → reported `updated_fields: [template, hide_title]` | `_wp_page_template` stayed empty; body class still `page-template-default` | The ability wrote `template` **inside `_elementor_page_settings`** instead of the `_wp_page_template` meta. Set the meta with WP-CLI; body class now `elementor-template-full-width` |
| D4 | No styling carried over: no fonts, colours, spacing or layout from the HTML | `convert-html` doesn't read CSS, so the draft is unstyled browser defaults (links in the theme's red, full-width text, stacked lists) | Styling from the Elementor Kit globals + a theme SCSS partial for About |
| D5 | Images placed at natural size, no radius, no crop | Figma crops every photo into fixed boxes with 15–20px radius | Image widgets with fixed boxes + object-fit |

| D6 | `dev-connect/elementor-set-page-data` (my rebuild) → `success: true, node_count: 191` | Front end kept serving the **old 7-HTML-widget draft**: `_elementor_element_cache` wasn't cleared | Deleted the cache meta + `wp elementor flush-css`; now part of `tools/about/publish.sh` |
| D7 | Elementor's lazy background/image loading (not DevConnect, but it hid the result) | A full-page capture without scrolling shows the map, hero and portraits blank, so my first diff said 27% | `tools/about/shoot.js` scrolls the page before capturing |

### Per section
| Section (Figma) | What DevConnect produced | Wrong compared with Figma |
|---|---|---|
| Hero (1:356) | One HTML block: H1, 2 images stacked, blockquote | Quote/portrait must sit **over** the photo in a white→light-sky panel; slider dots missing; H1 not uppercase |
| Intro + stats (1:329) | One HTML block: heading, paragraph, bullet list, 4 stats as `h3`+`p` stacked vertically | Bullets must be centred bold lines; the 4 stats must be a row of coloured cards with white shadow panels; the button isn't a button |
| Mission / creed / team (1:288) | One HTML block; creed + principles as bulleted lists with icons above text; team as 8 stacked figures | Creed/principles need two gradient header bars with icons in a row separated by "+"; the team must be one row of 8 cards |
| Heritage + timeline (1:232) | One HTML block; the 14 years as a plain bulleted list | The timeline is a designed component (gradient header bar, 14 vertical year bars, featured 1993 panel, slider track). A list loses all of it |
| Collaborations (1:206) | One HTML block; 3 collaborator cards stacked | Intro text + Sugita photo side by side; 3 cards in a row with arrows; framed "Request a product demo" |
| Global presence (1:185) | One HTML block; map image, then heading, then stats stacked below the map | Heading and 4 stat cards sit **over** the map on a navy band |
| Closing quote (1:175) | One HTML block; quote + 3 links run together on one line | 3 separate buttons (1 solid, 2 outlined, 1 with an arrow) |

### Environment notes found while making this draft
- Figma token expired (issues-log #28), so images were cropped from the 1x export; the hero photo is a placeholder.
- My `tools/bridge.sh` failed on uploads over ~12KB when launched from Python (WSL `bash` picked up instead of Git Bash);
  replaced by `tools/bridge.py` (issues-log #29).

### What the fixed page is (and how it was checked)
- **Tree:** `tools/elementor/build_about.py` → `pages/about-us/elementor/about.json` → `set-page-data` on page 15.
  **191 nodes: 73 containers, 83 headings, 19 images, 8 text-editors, 8 buttons, 0 HTML widgets.** Stored count = sent count.
  Every string, image and link is editable in the Elementor panel; the container backgrounds (hero photo, map) are Elementor settings.
- **Styling:** `wp-content/themes/module11/assets/scss/pages/_about.scss` (colours only `var(--clr-*)`, so the Kit stays the source).
  Desktop ≥1024 = Figma 1:161 coordinates scaled by `u()`; ≤1023 = Figma mobile 1:2237 auto-layout (column capped at 640px).
- **Images with baked-in text:** the export crops of the map and hero had the heading, quote and portrait in them (they would have
  doubled the live text). `tools/about/clean_images.py` inpaints them out → attachments 87 (map) and 88 (hero).
- **Result, 1440** (per-section pixel diff vs the Figma export, >32 threshold): hero 0.97%, intro 4.1%, mission 2.9%, heritage 3.3%,
  collaborations 3.1%, global 1.2%, closing 1.8%. Every section starts at its exact Figma y.
- **Result, 430:** every section height within 1–6px of Figma mobile; diffs 4–17% (sub-pixel text + a map glow that isn't in the crop).
- **No horizontal overflow** at 1920 / 1440 / 1024 / 768 / 430 / 390. Evidence: `docs/evidence/flow-b/about/`.

### Fixes needed after the rebuild (my own / Elementor, not DevConnect)
| Symptom | Cause | Fix |
|---|---|---|
| Portrait 31px too low | Elementor's `.elementor-widget:not(:last-child)` margin rule has the same specificity as one class and loads later | Stronger selector (`.au-hero-media > .au-hero-portrait`) |
| Numbers "1,800+" / "1993" wider than Figma | Figma tracks single characters ("1" −0.1em, "," −0.05em); my first text dump didn't read `letterSpacing` | Inline spans `au-ls-*` |
| Mission quote wrapped one word early | Chrome's Open Sans Light Italic sets ~1% wider | Box +20px (desktop), −0.012em (mobile) |
| Mobile creed/principles stacked vertically | Elementor containers default to width 100% and wrap below 767px | `width:auto; flex:none`, `flex-wrap:nowrap` |
| Mobile Sugita photo clipped 50px | Chrome sizes the flex item from the image's natural width during intrinsic sizing | Ratio on the wrapper, image absolutely positioned |
| Hero caption jumped to a 2nd column at 390px | Same Elementor mobile `flex-wrap: wrap` on a height-limited box | `flex-wrap: nowrap` on all page containers |
| Team/cards off by 1–2px, collaborations 28px short | Figma uses uneven gaps (10–13px) and fixed-height card frames | Exact per-child gaps; `min-height` 653 / 266 |

### Design inconsistencies followed as drawn
- Figma mobile pairs the team in a different order from desktop (Yamamura+Kritt, Delaney+McCart…): CSS `order` on mobile.
- Figma mobile repeats "Browse the many neurosurgical procedures we support" under the Sugita photo: added as a mobile-only button.
- The mobile hero quote has no opening “ but the desktop one does (a span hidden on mobile).

---

## Contact Us (page 16, `/contact-us/`) — draft + native rebuild 2026-09-28

**Input:** the Flow A replica `pages/contact-us/html/index.html` (`<main>`, 3 `<section>`s, copy verbatim from Figma 1:1740).
**Output:** `pages/contact-us/devconnect/01-convert-html-output.json` (whole `<main>`) and `02-convert-html-per-section.json`
(each section on its own) — copies in `docs/evidence/flow-b/contact/`.

### What DevConnect did
| # | What DevConnect did | Why it's wrong | Fix |
|---|---|---|---|
| E1 | `convert-html` on `<main>` → **1 `html` widget** for the whole page; per section → 1 `html` widget each, 0 native widgets | Same as D1, worse: the form, the FAQ and the contact details would be one code box. Nothing editable, the form wouldn't submit anywhere (`action="#contact-form"`) | Native tree `tools/elementor/build_contact.py` (52 nodes: 28 containers, 15 headings, 2 text-editors, Pro **Form**, **Nested Accordion**, 4 buttons, divider) |
| E2 | A `<form>` is treated as markup | A contact form must be a real form (validation, submissions stored, email to the business) | Elementor Pro Form widget: 9 fields + radio, required marks, submissions saved + emailed to the Site Settings email (dynamic tag); tested with a real submission |
| E3 | `<details>` FAQ treated as markup | Editors must add/remove/reorder questions | Nested Accordion (one container per answer, FAQ schema on) |
| E4 | Phone/fax/email/hours/address copied as literal text | Site-wide values must come from ONE place (brief: global settings) | Site Settings dynamic tags (`m11-setting-text` / `m11-setting-link`) — the same source the header and footer use |
| E5 | `set-page-data` again left `_elementor_element_cache` (D6) | stale render | cache delete + `flush-css` after every write |

### Problems in Elementor / my replica found while rebuilding
| # | Problem | How noticed | Fix |
|---|---|---|---|
| E6 | Nested Accordion can only open the **first** item by default; Figma draws the **2nd** open | Reading the widget controls (`default_state`: expanded = first only) | Editor-set attribute `data-m11-open="2"` (Advanced → Attributes) + 12 lines in `assets/js/main.js`; verified item 2 open on load |
| E7 | Form field gap 5px too big, radio question forced onto its own line, `First Name *` spaced asterisk | Per-section diff vs replica: contact-intro **+101px** at 1440 | Widget `row_gap`/`column_gap` = 0 (Elementor's per-widget CSS outranks the theme at 0,4,0), label `display:flex`, radio `flex:none` → **+1px, 0.43%** |
| E8 | Card values not in link colour; hours/address broke at the wrong word | Same diff, side by side | Label + value split (value = linked dynamic tag), box widths so the one-string Site Settings value wraps where Figma breaks it |
| E9 | FAQ answer box overflowed on mobile | 430 side by side | Elementor containers default to `--width:100%`; margins pushed it out → `width:auto` |
| E10 | Replica "Before you go" buttons pointed at `#bottom-link-1..3` (placeholder hrefs) | Writing the tree | Real pages: /products/, /resources/, /about-us/ (as on Resources) |

**Result (`tools/qa_wp_vs_replica.py contact`):** 1440: 0.43% / 0.91% / 0.68% (heights +1/0/0 px) · 768: 2.6–4.6% ·
430: 1.3–5.0% (heights within 10px). Form submission → "Thank you — we’ll be in touch shortly." (`form-submitted.png`).

## Flow A — ACF pages (Home, Resources, Products, Sales Hub): DevCommand HTML→ACF conversion, run 2026-09-28

**Input:** the generated HTML of the 9 ACF pages packaged as one site (`source/html-site.zip`, `tools/figma_html/package_acf_site.py`).
**Pipeline (all DevCommand):** html-project-extractor → html-parser (`spec/site-spec.json`, 33 fragments) → html-acf-planner
(`spec/acf-plan.json`, `docs/acf-review-table.md`) → html-acf-builder (`output/theme/module11/acf-json/`, 8 groups) →
html-php-writer (`output/theme/module11/`, 33 PHP files). **Conversion output kept untouched in `output/theme/module11/`;** the fixed
version is ported into `wp-content/themes/module11/`. Coverage reports: `docs/evidence/flow-a/conversion/`.

### Where the conversion was wrong (and what I did)
| # | Stage | What it did | Why it's wrong | Fix |
|---|---|---|---|---|
| C1 | extractor | Found ONE header/footer cluster (public) | The Sales Hub has its own portal header/footer; Login has none (#52) | Two chrome sets taken from the markup |
| C2 | extractor | `tokens.json` primary = #FFFFFF, breakpoints [1024, 1023] | Frequency heuristic; one breakpoint read twice (#53) | Brand tokens stay the Elementor Kit |
| C3 | parser | **Merged Resources' testimonials + brochures into one unnamed section; dropped brochures, and accessories / related / size-guide / instruments on the product pages** | Slicer auto-closes `<li>` like `<p>` (#54) | Patched copy (`<p>` only); 33 fragments byte-verified |
| C4 | builder | 11 CTAs got a **label field but no URL** (`cta_label`, `closing_cta_label`, `view_label`, `more_label`, `watch_link_label`, …); php-writer then **hardcoded their hrefs** (`#testimonials`, `#`, `home_url('/about-us/')`) | Links not editable from wp-admin (Editability 25%) | Port: every label gets an ACF **link** field (label + URL + target) |
| C5 | builder | A 16-field "Common Section Options" clone (background, heading, text, button colours + 8 paddings) on **all 19 layouts** | Per-section colour pickers undo Flow B ("change a brand colour in one place") and let editors break the replica | Port: keep only `hide_section` + `section id`; colours stay on the Kit |
| C6 | php-writer | Accessories / Related Products headings and the size-guide / instruments column headers **hardcoded** | Visible copy not editable | Port: heading fields on the product group; column headers as fields |
| C7 | php-writer | Partials in `template-parts/sections/{snake}.php`; page template label "Flexible Page" | House convention is `template-parts/flex-blocks/{kebab}.php` | Port: renamed + dispatcher adjusted |
| C8 | php-writer | Read `site_logo` / `sales_hub_name` (the plan's names) | Real Site Settings fields are `m11_logo` / `m11_hub_name` | Port: real names (the writer caught this itself) |
| C9 | php-writer | Position-based class maps (`pb-item--tumor`, brochure widths `w934…`, `mo-1,3,5…`) keyed to row index | Adding / reordering a row in wp-admin breaks the layout (robustness) | Port: layout driven by modifiers stored per row or by CSS that doesn't depend on position |
| C10 | php-writer | Filters / sort can't submit (no JS, no submit control) | Non-functional archive + library filters | Port: small `m11-filters.js` (submit on change) |
| C11 | coverage checker | Two HIGH `plan_layout_missing` for the CPT groups | Plan lists CPT pointer rows in `layouts[]`; checker diffs every name against FC layouts (#56) | Checker artifact; not "fixed" by adding fake layouts |
| C12 | php-writer | Resources testimonials: design's per-bio line splits, Sauvageau/Hanel shared-caption layout, "Extended Version" caption simplified | Fidelity loss vs the replica | Port + pixel QA against the HTML replica |
| C13 | parser/planner | The Products hero photo got **no field** | It was a CSS `background` in the HTML; only `<img>` becomes a field | Port: `background_image` (+ mobile) fields → CSS variables (9.35% → 0.06%) |
| C14 | builder | Product `buttons` = seamless clone whose inner repeater is also `buttons` | Both write the same meta key; buttons never stored | Port: plain repeater `buttons` → `cta` link |

**Good calls by the tooling (kept):** relationship fields instead of nested repeaters (one record per brochure/video); `has_archive:false`
with the `products` page as the browse experience; computed dashboard counts; `wp_get_attachment_image()` + lazy loading except above the
fold; an offline render harness that diffed every partial against its fragment (and caught its own docblock parse error).
