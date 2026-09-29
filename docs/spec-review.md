# Spec Review — Mizuho America (task-11.local), HTML → ACF pipeline, step 1

Source: `source/html/_extracted/` (9 pages), seeded from `source/html/pages.json` /
`tokens.json` / `assets.json` / `shared-regions.json` (shared extraction layer).
Output: `spec/site-spec.json` (single source of truth for all downstream agents) +
`spec/fragments/**` (verbatim per-section HTML) + this review doc.

**This is the developer review gate.** Nothing downstream (classification, ACF field
groups, PHP templates) should start until the open questions below are resolved or
explicitly accepted.

---

## 1. Pages (9) and their sections (33 total)

| # | Slug | File | Sections |
|---|------|------|----------|
| 1 | `home` | index.html | hero-carousel, intro-statement, value-columns, procedure-band, testimonials, about-stats |
| 2 | `product-feather-blades` | product-feather-blades.html | product-overview, **size-guide**, accessories, testimonial, related-products |
| 3 | `product-lawtonelite-skull-base-set` | product-lawtonelite-skull-base-set.html | product-overview, **instruments-included**, accessories, testimonial, related-products |
| 4 | `product-sugita-ii-head-frame` | product-sugita-ii-head-frame.html | product-overview, accessories, testimonial, related-products |
| 5 | `products` | products.html | products-intro, browse-by-procedure, browse-by-product |
| 6 | `resources` | resources.html | resources-intro, testimonials, fast-facts, brochures, continue-your-visit |
| 7 | `sales-hub-dashboard` | sales-hub-dashboard.html | dashboard, account |
| 8 | `sales-hub-login` | sales-hub-login.html | sales-hub-login (no header on this page — see §3) |
| 9 | `sales-hub-resource-library` | sales-hub-resource-library.html | resource-library-intro, resource-results |

Homepage note: developer-confirmed to be built in WordPress as inner page slug
`mizuho-home`, not the literal WP front-page slug `home`.

Every one of the 33 fragments was verified to be a byte-exact substring of its source
page (`fragment in source_html == True` for all 33 + all 6 shared chrome fragments).

## 2. The product-detail template (known fact, confirmed)

`product-sugita-ii-head-frame` / `product-feather-blades` / `product-lawtonelite-skull-base-set`
are **one single-product template with three example instances**, not three different
designs:

- **Base** (Sugita II): overview + accessories + testimonial + related-products only.
- **Variation A** (LawtonElite): base + an **instruments-included** parts-list table (15 rows).
- **Variation B** (Feather Blades): base + a **size selector** (6 options) + a **size-guide**
  table (6 rows), and the size-guide table's "selected" row is hard-pinned to match the
  select's default option (static, no live JS).

`products.html` is the archive/listing shell for this same product family (filters +
result tiles + pager, all statically hardcoded to one filtered state: "Head Holding
Systems, 4 products").

`resources.html`'s **testimonials** (7 expert/video entries) and **brochures** (9
collaborator groups × 1–7 cards = 30 brochure cards) sections, and
`sales-hub-resource-library`'s tile grid, are likewise repeating records, not hand-built
one-offs. All of this is recorded as evidence in `site-spec.json` (repeats,
nested-repeat flags) — **classification into CPTs/relationship fields is
html-acf-planner's job**, not decided here.

## 3. Two chrome sets — confirmed, and a gap in the auto-detector

`shared-regions.json` only detected ONE header/footer pair (consistency 0.75 / 0.67
across 6 pages) — it completely missed the Sales Hub chrome because its detector only
sampled the 6 public pages. I verified both sets directly against the markup:

- **Public chrome** (`header.site-head` / `footer.site-foot`) — on home, resources,
  products, and all 3 product-detail pages.
- **Sales Hub chrome** (`header.site-head.portal-head` / `footer.site-foot.portal-foot`)
  — on `sales-hub-dashboard` and `sales-hub-resource-library` only.
- **`sales-hub-login` has NO header at all** — `<body>` goes straight into `<main>`, and
  it's the only page that doesn't load `js/main.js` (no mobile-nav toggle to wire up,
  since there's no header). Confirmed by direct inspection, not an extraction gap.

Both sets are recorded in `site-spec.json.shared` as global chrome (matching the
existing Elementor Theme Builder templates 61/62), not as page sections.

Byte-diff results (all 6 public-page headers/footers, all 3 sales-hub headers/footers):
the **only** differences between instances of the "same" header/footer are (a) which
per-page duplicated asset-folder copy the logo `<img src>` points at (same file,
9 different folders — a static-export artifact, not 9 real logos), and (b) which nav
item carries `is-current`/`aria-current`. **One exception**: `sales-hub-dashboard`'s
`<footer>` carries an extra class `pf--center` that neither `sales-hub-resource-library`
nor `sales-hub-login`'s footer has — content is otherwise identical. **Open question**:
intentional one-off, or a class missing from the other two?

## 4. Tokens

- **Brand colors** (developer-confirmed, verified against every stylesheet's `:root`
  block, byte-identical across all 9 CSS files): primary `#0065B3`, sky `#00B3F0`, navy
  `#002842`, text `#090909`, light sky `#77DCFF`. `source/html/tokens.json`'s top-level
  `colors.primary`/`secondary` (`#FFFFFF`/`#0065B3`) are a frequency-heuristic misread
  (`#FFFFFF` is just the page background) — not used.
- **Breakpoints**: `[1024, 1023]` is recorded verbatim from the extraction layer but is
  **one boundary**, not two — desktop `min-width:1024px` / mobile `max-width:1023px`.
  No tablet breakpoint exists anywhere. QA/audit viewports should use two widths
  straddling this single boundary (e.g. 1440/390), not a hardcoded 3-viewport default.
- **Fonts**: `--font-heading: Freeman`, `--font-body: Open Sans` are the two custom
  properties, but Montserrat and Mukta are also used directly (not via custom property)
  for nav-adjacent UI and stat numerals. A `Fraunces Full` @font-face is loaded on every
  page but a CSS comment ("Montserrat runs wider than Gotham") implies the *real*
  intended display font is a licensed **Gotham** not present in this export. **Open
  question for design**: confirm the true display typeface before finalizing the
  Elementor Kit.
- **No section-level canvas/background class system** (no `s-paper`/`s-cream`
  equivalents) — every section shares one `.rs` reset utility that auto-swaps to
  `#FCFEFF` on mobile for every section *except* home's procedure-band and the footer.
  This CSS-only exception list must be replicated by the theme build, not flattened.
- `.d-only` / `.m-only` utility classes toggle desktop-only/mobile-only **content**
  (not just layout) at the 1024px boundary — some copy differs by breakpoint, not just
  visibility. Must be preserved verbatim in markup.

## 5. JS hooks

The entire site has exactly **one** JS behavior: the mobile-nav toggle
(`.site-head__toggle` → `#site-primary-nav.is-open` + `body.nav-open`), in `js/main.js`
(9 lines). **Zero `data-*` attributes exist anywhere** in the 9 pages. Every other
interactive-looking element — product filters, search, pager, tabs, the blade-size
selector, the size-guide "selected" row, all video/download/"read more" triggers — is
static markup with no JS wiring. Treat all of it as a visual prototype of intended
behavior, not an implemented feature, when planning ACF/PHP.

## 6. Anchor map — and a real navigation defect

Full detail in `site-spec.json.anchors`. Headline findings:

- **DEFECT, site-wide**: the header "Products" nav link is inconsistent. On `home` and
  `resources` it's `href="#products"` (no such id exists anywhere). On the 3
  product-detail pages + `products.html` itself it's `href="products.html"` (real,
  marked current). Same label, two different behaviors depending which page you're on.
- **DEFECT, systematic (all 3 product-detail pages)**: the "Overview" tab always links
  to `#overview`, which never exists (the real section id is `product-overview`). The
  other tab(s) on each page correctly resolve.
- **Pattern comparison**: home's procedure-band block (3 procedures) and
  `products.html`'s "Browse by procedure" block (same 3 procedures, same copy pattern)
  are near-duplicates, but home's links are all broken hash anchors while
  `products.html`'s are real cross-page links to the 3 example products.
  `products.html` is the working version — home should probably match it.
- **Dozens of decorative placeholder anchors** (`#video-*`, `#watch-*`, `#brochure-*`,
  `#download-*`, `#read-more-topic-*`, `#product-<slug>`, footer/legal boilerplate,
  language switcher, header search) never resolve anywhere in the export. Treated as
  intended-but-unbuilt behavior (video modals, PDF downloads, future product pages),
  not literal bugs — grouped once each in `anchors[]` rather than listed individually.

## 7. Forms

6 forms captured in full (`site-spec.json.forms`), **none have real delivery** — all
`action="#..."` or non-standard placeholder routes:
1. Header search (decorative, all 8 pages with a header).
2. Products archive: filter form (category/configuration/procedure checkboxes) + separate search form.
3. Sales Hub Resource Library: filter form (resource type/product category, with hardcoded counts) + separate search+sort form.
4. **Sales Hub login** (real auth form — email + password, `required`) — `action="../../sales-hub-dashboard/html/" method="get"`, which is not a real WP route and would additionally leak the password into the URL via GET. **Needs a real login mechanism before build**; never model as an ACF form.

## 8. Content placeholders / defects to confirm

- **"– Prof Name Here, MD PhD" / "Department of Neurosurgery, Institution Here"** —
  identical unfilled testimonial attribution on **all 3** product-detail pages (quotes
  themselves are real, unique copy). Highest-priority content gap.
- **"FPO IMAGE" thumbnail placeholders** — 3 of 4 gallery-thumb slots on
  `product-feather-blades` and `product-sugita-ii-head-frame`. The LawtonElite page has
  real thumbnail images in the same slots — inconsistent completeness across the 3
  example instances, not a site-wide issue.
- **"Sales HUb - REP Portal"** — verbatim capitalization typo in the login page's only
  heading. Recorded as-is; flag for a copy fix.
- **Dashboard "Log in" button** (developer-confirmed known issue) — the dashboard header
  already shows a logged-in identity ("Hello, John Q." / "John Q. Public") yet the
  Account panel has a prominent "Log in" button pointing at the login page.
- No literal `[CONFIRM ...]` / `[TBD ...]` bracket markers or lorem-ipsum text exist
  anywhere in the 9 pages (grepped explicitly) — the placeholders above are the complete
  list.

## 9. Nested repetition (flag for html-acf-planner — exceeds ACF one-level nesting)

- **resources.html `testimonials`**: expert entries (7) each contain a nested list of
  1–2 videos. One entry (Sauvageau/Hanel, co-credited) breaks the per-item shape
  entirely — its 2 videos share ONE caption block as a sibling of the video list,
  instead of each video owning its own caption.
- **resources.html `brochures`**: 9 collaboration groups, each containing 1–7 brochure
  cards (30 cards total). Card shape also varies (title+link vs. excerpt-only+link).
- **products.html `browse-by-product` tiles**: each product tile contains its own
  nested list of 1–3 procedure tags (plus an occasional "+N" overflow chip).

All three need a flattening/relationship decision before ACF field groups are built.

## 10. Tooling bug found and worked around (for the issues log)

**Symptom**: the skill's `slice_sections.py` silently truncated/merged sections on
`resources.html` — `testimonials` and `brochures` collapsed into one mis-bounded
fragment starting mid-`<article>`, and `size-guide`/`accessories`/`related-products`
went missing entirely on all 3 product-detail pages on the first run.

**Root cause**: the script's `IMPLIED_CLOSE = {"p","li","dt","dd","option"}` set is
meant to auto-close an unclosed `<p>` before a new block/sectioning tag starts (a real
browser behavior). But it also fires for `<li>`, and browsers do **not** auto-close an
open `<li>` just because a `<div>`/`<section>` starts inside it — `<li><a>…</a><div
class="tx-cap">…</div></li>` (very common in this site's testimonial/brochure card
markup) is perfectly valid nesting. The script wrongly popped the still-open `<li>`
off its stack the moment the nested `<div>` began, which cascaded into popping the
`<li>`'s ancestors too (`<ul>`, `<article>`, and eventually the enclosing `<section
id="testimonials">` itself), silently ending the section's capture mid-document.

**Fix**: built a locally-patched copy of the script (`IMPLIED_CLOSE = {"p"}` only,
`li`/`dt`/`dd` removed) in the session scratchpad — the shared plugin file itself was
left untouched. Re-ran the slicer for all 9 pages with the patch.

**Verification**: re-diffed the patched output's section id list against a full manual
read of every page (all 33 expected section ids now present, in the right order, on
every page); re-ran the byte-exact substring check for all 33 fragments; `resources.html`
specifically went from 4 mis-bounded main sections to the correct 5
(resources-intro/testimonials/fast-facts/brochures/continue-your-visit).
**Recommend logging this as a pipeline issue** (`docs/issues-log.md`, per project
convention) since the same bug will resurface on any future page with `<li><div>`
nesting.

## 11. Validation performed

- `site-spec.json` parses as valid JSON.
- All 33 page-section fragment paths + 6 shared chrome fragment paths exist on disk and
  are byte-exact substrings of their source HTML page.
- `meta.sections_count` (33) == sum of `pages[].sections` (33) == fragment files on disk (33).
- `meta.pages_count` (9) == `pages.length` (9).
- Every section object has `id`/`index`/`fragment`/`tag`/`classes`/`anchor_target`/`fields`/`repeats`/`js_hooks`.
- Spot-checked all 22 unique `type:"image"` sample paths referenced in `fields[]` against
  `source/html/assets.json`'s inventory — all resolve, 0 missing.
