# ACF architecture review — sign-off table

**Status: APPROVED.** All 21 rows approved as proposed, no changes. All 12 open questions answered
(see Decision record below). `spec/acf-plan.json` now has `"approved": true`. Approved per the
developer's instruction to the main session: implement the HTML→ACF conversion end to end ("whatever
DevConnect does HTML to ACF is the job; a perfect replica is the goal").

Source: `spec/site-spec.json` (HTML→ACF pipeline, Flow A). Scope per CLAUDE.md's builder split: **Home,
Products (CPT + archive), Resources, Sales Hub = ACF** (this table). About Us + Contact Us are Elementor
(Flow B) and are not part of this 9-page HTML extraction. Header/footer = existing Elementor Theme
Builder templates 61/62 (public); a new Sales Hub portal pair is DECIDED below (build step B4, not built
yet).

Machine-readable companion: `spec/acf-plan.json` (`"approved": true`, `decision_record` +
`build_steps` added). Coverage gate: `python3 .../check_acf_coverage.py --stage plan` → **0 HIGH / 0 MED
/ 0 LOW**, 221/221 spec fields accounted for (editable or explicitly waived in `static_content`) —
re-verified after this approval pass, unchanged.

**Prefix note:** the spec's `meta.prefix` suggests `mizuho`, flagged there for confirmation. This plan
uses `m11` instead, because CLAUDE.md (already-approved, checked-in) fixes ACF Local JSON keys as
`group_m11_*` / `field_m11*` and the theme function prefix as `m11_`. Not an open question.

## Page/section → layout sign-off table — all 21 rows APPROVED as proposed

| # | Component | Proposed structure | Classification | Reuse verdict | Reasoning | Developer decision |
|---|---|---|---|---|---|---|
| 1 | Home / hero-carousel | FC layout `hero_carousel`: headline, browse_link_label + `hero_cards` repeater (image/label/link, max 3) + `hero_ctas` repeater (label/url) | Local | NEW (0.15) | Unique Swiper hero, single-page evidence, not a generic pattern. 2 cards is correct content; 3rd dot is a known design inconsistency (q4). | ✅ Approved |
| 2 | Home / intro-statement | FC layout `intro_statement`, built from `section_heading` + `cta` clones only (heading, body, cta_label) | Global (provisional) | NEW (0.30) | Generic text/CTA band, built entirely from house clones — Global by pattern even on single-page evidence. | ✅ Approved |
| 3 | Home / value-columns | FC layout `value_columns`: closing_cta_label + `value_cards` repeater (icon/title/lead/body, 4) | Local | NEW (0.10) | Home-specific value-prop grid. | ✅ Approved |
| 4 | Home / procedure-band | FC layout `procedure_band`: heading, closing_text, closing_cta_label + `procedure_items` repeater (icon/title/view_label/more_label, 3) | Local | COMPATIBLE (0.80) vs `browse_by_procedure` (#8) | Same repeater shape as Products' browse-by-procedure, but 2 extra fields fail the strict merge test. **Kept SEPARATE (q1, decided): the two bands differ in height, type and layout in the design — pixel replica is the goal, not acted on.** | ✅ Approved — kept separate |
| 5 | Home / testimonials | FC layout `testimonial_home`: heading, intro, mobile_cta_label, featured_quote, featured_quote_attribution, more_link_label + `testimonial_cards` repeater (thumbnail/name/role/rest/watch_link_label, 3) | Local | NEW (0.25) | Field set matches neither the product CPT testimonial nor Resources' expert/video pattern — fails merge test against both. | ✅ Approved |
| 6 | Home / about-stats | FC layout `about_stats`: heading, body, cta_label + `stats` repeater (number/label, 3) | Local (provisional) | NEW (0.20) | Site inventory notes a stats-band twin on About Us, but About is Elementor (out of ACF scope) — no cross-ACF-page evidence yet. | ✅ Approved |
| 7 | Products / products-intro | FC layout `products_intro`: page_title, heading, subheading, body, cta_label | Local | EXTEND (0.62) vs `intro_statement` (#2) | 5-field superset of intro_statement's 3 fields. **Kept SEPARATE (q2, decided): fidelity-first, not folded.** | ✅ Approved — kept separate |
| 8 | Products / browse-by-procedure | FC layout `browse_by_procedure`: heading, lead + `procedure_items` repeater (icon/title/view_link/more_label, 3) | Local | COMPATIBLE (0.80) vs `procedure_band` (#4) | Near-twin of Home's procedure_band, missing its 2 extra fields. **Kept SEPARATE (q1, decided).** | ✅ Approved — kept separate |
| 9 | Products / browse-by-product | FC layout `browse_by_product`: heading, lead, filters_heading, filters_subheading (editable); result_count, active_filter_chip, product_tiles = **live m11_product query, not ACF content** | Local | NEW (0.10) | Editorial copy is a layout; the tile grid renders from the CPT query so product data has one home (the product post), not two. Also resolves the spec's flagged `procedure_tags` nesting-limit concern — it was never modeled as an ACF repeater. | ✅ Approved |
| 10 | Resources / resources-intro | FC layout `resources_intro`: page_title, heading, body, featured_video_thumbnail, featured_quote, featured_quote_attribution + `intro_ctas` repeater (2) | Local | NEW (0.40) | Richer than #2/#7 (adds video+quote); merging would be the "variant toggling a large field block" over-merge the standards skill warns against. | ✅ Approved |
| 11 | Resources / testimonials (expert videos) | FC layout `resources_testimonials`: heading + `expert_entries` repeater (bio richtext, `videos` **relationship → m11_resource** type=video, optional `shared_caption`) | Local | NEW (0.15) | Distinct from #5 and the product CPT testimonial. Nested-repeater flag in the spec (expert→videos) resolved via a relationship field instead of a sub-repeater — no one-level-nesting violation. `shared_caption` covers the one documented exception row (Sauvageau/Hanel). | ✅ Approved |
| 12 | Resources / fast-facts | FC layout `fast_facts`: heading + `fact_items` repeater (title/video_thumbnail/caption, 3) | Local | NEW (0.20) | Only 3 fixed curated items — fails the CPT test (not an ongoing catalogue). **Kept as a plain repeater (q5, decided) — not converted to a relationship.** | ✅ Approved |
| 13 | Resources / brochures | FC layout `resources_brochures`: heading + `collaboration_groups` repeater (optional collaborator_text, `brochure_cards` **relationship → m11_resource** type in [brochure, spec_sheet], 1–7/group, 9 groups) | Local | NEW (0.20) | Developer-confirmed CPT candidate (30 cards). Nested-repeater flag resolved via relationship field, same pattern as #11. Fixes the spec's broken `#download-<slug>` anchors once resource files are uploaded. | ✅ Approved |
| 14 | Resources / continue-your-visit | FC layout `bottom_links_band`: heading + `links` repeater (label/url, 3) | Global (provisional) | NEW (0.25) | Generic "Before you go" pattern also used on Elementor-built About/Contact (unreachable from this ACF layout) — Global by pattern, single ACF-page evidence today. | ✅ Approved |
| 15 | Sales Hub Dashboard / dashboard | FC layout `sh_dashboard`: lead (editable); heading = **computed** (logged-in user greeting); `stats` repeater — label editable, number = **computed** (query counts); `tools` repeater — icon/title/**link**/description, all editable | Local | NEW (0.15) | Matches given project fact exactly. `link` field added beyond the spec's narrow field list — evidenced in the spec's own notes annotation, not invented. **Stat mapping DECIDED (q6): row1=product_category terms with ≥1 published product; row2=published m11_resource where resource_type∈{brochure,spec_sheet}; row3=published m11_resource where resource_type=video.** | ✅ Approved — stat mapping fixed |
| 16 | Sales Hub Dashboard / account | FC layout `sh_account`: heading + `account_actions` repeater (label/url, 3) | Local | NEW (0.10) | Single-page evidence. **"Log in" copy KEPT exactly as drawn (q7, decided) — flagged as a design defect for the client (docs/issues-log.md #49), not silently changed.** | ✅ Approved — seeded as drawn |
| 17 | Sales Hub Login | FC layout `sh_login`: heading, forgot_password_label, note (editable); logo = **static** (from Site Settings); login form = `wp_login_form()`, not ACF | Local | NEW (0.10) | Maps onto existing WP page id 18 ("sales-hub") as the unauthenticated portal landing/login screen. **Mapping CONFIRMED: 18=Login, 19=Dashboard, 20=Resource Library.** Genuine auth form excluded from ACF per house rule. | ✅ Approved |
| 18 | Sales Hub Resource Library / resource-library-intro | FC layout `sh_resource_library_intro`: heading, body | Local | EXTEND (0.68) vs `intro_statement` (#2) | Strict subset of intro_statement (no CTA). **Kept SEPARATE (q3, decided): fidelity-first, not folded.** | ✅ Approved — kept separate |
| 19 | Sales Hub Resource Library / resource-results | FC layout `sh_resource_results`: no unique content fields; result_count, resource_tiles = **live m11_resource query** | Local | COMPATIBLE (0.72) vs `browse_by_product` (#9) | Structural query/filter layout, same role as #9 for the Resource Library. | ✅ Approved |
| 20 | Product CPT (`m11_product`) | Field group across 4 tabs (Overview / Configurator / Accessories & Related / Testimonial & CTAs) attached to `post_type == m11_product`, covers all 3 example product-detail pages (14 spec sections total) | Custom Post Type | N/A (CPT) | Textbook CPT test: 3 "page" designs are one template with optional blocks (`has_size_guide`, `has_instruments_table` booleans). **has_archive:false CONFIRMED (q8) — WP page `products` is the browse experience; that page does not exist yet (build step B1). FC-convention deviation ACCEPTED (q9).** | ✅ Approved |
| 21 | Resource CPT (`m11_resource`) | Field group (cover_image, resource_file, video via `media` clone, excerpt) attached to `post_type == m11_resource`; taxonomies resource_type + shared product_category | Custom Post Type | N/A (CPT) | Developer-confirmed repeating record shown on both the public Resources page and the Sales Hub Resource Library — one source of truth via relationship fields (#11, #13) and CPT queries (#19). No single-resource template built this phase. FC-convention deviation accepted (q9). | ✅ Approved |

## "Not editable — confirm" (static_content) — confirmed unchanged

| Section | Field | Why it's not an ACF field |
|---|---|---|
| product-overview (all 3 product pages) | `page_kicker` | Identical literal "Products" label everywhere — promoted to ONE Options field (`product_page_kicker` on `m11-site-settings`) instead of duplicating the same string on every product post. Still editable, just not per-post. |
| product-overview (all 3 product pages) | `breadcrumbs.label` / `.url` | Generated from the product's assigned `product_category` term + page hierarchy — structural nav, not authored copy. |
| product-overview (feather-blades, sugita) | `thumbnails.type` | "FPO IMAGE" is the template's fallback label for an empty gallery slot; the editable surface is the thumbnail image field. (LawtonElite's real thumbnails stay editable/claimed.) |
| product-overview (all 3 product pages) | `tags.label` | Rendered from the assigned `procedure` taxonomy terms. |
| product-overview (all 3 product pages) | `product_tabs.label` / `.url` | Tab bar is template-generated logic (Overview always, Size Guide/Instruments Included only when filled, Accessories always) — also fixes the spec's systematic `#overview` anchor defect by construction. |
| product-overview (feather-blades) | `size_options.label` | Derived from the `size_rows` repeater's own width values — one source instead of duplicating the same 6 sizes twice. |
| products/browse-by-product | `result_count`, `active_filter_chip`, `product_tiles.*` | Live `m11_product` query output (filtered by taxonomy + search) — editors manage this by editing product posts, not the archive page. |
| sales-hub-dashboard/dashboard | `heading` | Computed greeting from the logged-in user's display name (given project fact), not editor content. |
| sales-hub-dashboard/dashboard | `stats.number` | Computed live from queries — mapping decided (q6): row1 = product_category terms in use, row2 = published brochure/spec-sheet resources, row3 = published video resources. The row's `label` stays editable. |
| sales-hub-login/sales-hub-login | `logo` | Sourced from the existing `m11-site-settings` `site_logo` field — one logo source of truth. |
| sales-hub-resource-library/resource-results | `result_count`, `resource_tiles.*` | Live `m11_resource` query output, same pattern as the Products archive. |

**Not JSON-waived but worth noting:** the decorative/non-functional filter and search forms (`.fl-form`,
`.pb-search`, `.rl-search`/`#rl-sort`, header `.hd-search`) are recorded in `spec/acf-plan.json` under
`forms.decorative_non_functional` rather than as `static_content` entries — they're `forms[]` items in
the spec, not section `fields`, so they sit outside the coverage checker's field-level scope, but the
narrative is there for transparency (filter labels come from taxonomy term names, not ACF content).

## Decision record — all 12 open questions, answered

Attributed to: **main session, on the developer's end-to-end conversion instruction** ("whatever
DevConnect does HTML to ACF is the job; a perfect replica is the goal"). Date: 2026-09-28. Full detail
also written into `spec/acf-plan.json` → `decision_record`.

| # | Topic | Decision |
|---|---|---|
| 1 | `procedure_band` vs `browse_by_procedure` | **Kept SEPARATE.** The two procedure bands differ in height, type and layout in the design — pixel replica is the goal, so the COMPATIBLE (0.80) score is not acted on. |
| 2 | `products_intro` vs `intro_statement` | **Kept SEPARATE.** Same fidelity-first reasoning as #1 — EXTEND (0.62) not acted on. |
| 3 | `sh_resource_library_intro` vs `intro_statement` | **Kept SEPARATE.** Same fidelity-first reasoning — EXTEND (0.68) not acted on. |
| 4 | Hero-carousel dot count vs card count | **2 hero cards is correct content.** The 3rd dot is a known, already-decided design inconsistency (dots are drawn from the real slide count in the source, not content this build controls). `hero_cards.max` stays 3. |
| 5 | `fast_facts` sourcing | **Kept as its own plain repeater** (3 curated items) — not converted to an `m11_resource` relationship. |
| 6 | `sh_dashboard.stats` computed-number mapping | Row 1 "Product categories available" = count of non-empty `product_category` terms (≥1 published `m11_product`). Row 2 "Brochures & spec sheets" = count of published `m11_resource` with `resource_type` in (brochure, spec_sheet). Row 3 "Training videos" = count of published `m11_resource` with `resource_type` = video. Labels stay editable; numbers stay computed, keyed by row index. |
| 7 | `sh_account` "Log in" defect | **Kept editable and seeded exactly as drawn, INCLUDING "Log in."** Flagged as a design defect for the client in `docs/issues-log.md` **#49** ("Sales Hub design defects (flagged, followed as drawn)") — not silently corrected. |
| 8 | `m11_product` archive mechanism | **Confirmed `has_archive:false`**; WP page `products` (page-flexible.php, sections FC) is the browse experience, rewrite slug `products` so singles are `/products/<slug>/`. The `products` page does **not exist yet** (current pages: 14 mizuho-home, 15 about-us, 16 contact-us, 17 resources, 18 sales-hub, 19 dashboard, 20 resource-library, 21 cross-reference, 22 training) — creation is build step **B1**. |
| 9 | CPT field-group FC-convention deviation | **Accepted.** Plain field groups, admin tabs allowed, no common_settings/two-tab convention. |
| 10 | Sales Hub portal chrome mechanism | **Elementor Theme Builder templates** ("Sales Hub Header", "Sales Hub Footer") with Display Conditions on the sales-hub page tree (18 + descendants 19–22), matching the existing public 61/62 mechanism. Header condition **excludes** page 18 (Login has no `<header>` per spec); footer condition **includes** pages 18/19/20 (Login uses the portal footer). Build step **B4**. |
| 11 | `sales-hub/cross-reference` (21) / `sales-hub/training` (22) | **Left as placeholder pages, NO layouts planned.** No page-flexible.php/sections work until a design exists. Build step **B6**. |
| 12 | Header "Products" nav link defect (spec `anchors[]`) | **Fixed via a native Primary menu (id 2) edit** — point the existing "Products" item at the new `products` page's permalink once created. Not an ACF field; fixes the header on every page at once. Build step **B5**. |
| — | Sales Hub page-id mapping (restated, not a question) | sales-hub-login.html → WP page **18** (`sales-hub`, portal root/login). sales-hub-dashboard.html → page **19**. sales-hub-resource-library.html → page **20**. Kept exactly as originally proposed. |

## Build steps (implementation order, per `spec/acf-plan.json` → `build_steps`)

| ID | Step |
|---|---|
| B1 | Create WP page `products` (`page_template` = page-flexible.php) — does not exist yet. Attach layouts `products_intro`, `browse_by_procedure`, `browse_by_product` in that order. |
| B2 | Register `m11_product` (has_archive:false, rewrite slug `products`) and `m11_resource` CPTs + taxonomies (`product_category` shared, `procedure`, `product_configuration`, `resource_type`) before seeding any product/resource content. |
| B3 | Build ACF field groups: `m11-site-settings` addition (`product_page_kicker`), `m11_product` CPT group (4 tabs), `m11_resource` CPT group, and the 19 FC layouts (acf-json Local JSON, `group_m11_*`/`field_m11*` keys). |
| B4 | Build the 2 new Elementor Theme Builder templates ("Sales Hub Header" excl. page 18, "Sales Hub Footer" incl. pages 18/19/20) with Display Conditions on the sales-hub page tree, matching the 61/62 pattern. |
| B5 | Edit the existing Primary menu (id 2) "Products" item to point at the new `products` page permalink — fixes the spec's `#products` / `products.html` inconsistency (anchors[] defect) site-wide in one edit, no template change needed. |
| B6 | Leave `sales-hub/cross-reference` (21) and `sales-hub/training` (22) as plain placeholder pages — no sections FC, no layouts, per decision #11. |

## Architecture summary

- **19 FC layouts** on the shared `sections` field (project contract: ONE flexible field, `page_template
  == page-flexible.php`), built from the **house clone library**: `common_settings` on all 19,
  `section_heading`/`page_heading`/`cta` partials on the intro-band layouts, `button_group` reused inside
  the product CPT's shared CTA field. 19 layouts + 2 CPT groups reuse 4 house source components instead
  of hand-declaring heading/media/CTA/button fields ~20+ separate times.
- **2 CPTs**: `m11_product` (has_archive:false — the WP page `products` is the browse experience,
  decided q8, build step B1) and `m11_resource` (no single template this phase, surfaced only via
  relationship fields + queries). **4 taxonomies**: `product_category` (shared by both CPTs), `procedure`,
  `product_configuration`, `resource_type`.
- **Two spec-flagged nesting-limit violations resolved** (expert→videos on Resources, and
  collaboration_groups→brochure_cards) by using **relationship fields to `m11_resource`** instead of
  nested repeaters — zero one-level-nesting violations in the final structure, and a single source of
  truth for every brochure/spec-sheet/video shown on both the public Resources page and the Sales Hub
  Resource Library.
- **Reuse scoring, decided**: all 4 near-twin/subset layout pairs (2 scored COMPATIBLE 0.80, 2 scored
  EXTEND 0.62/0.68) were kept SEPARATE per the developer's fidelity-first instruction — the design draws
  these sections with real differences (height/type/layout), so no layouts were merged despite the
  favourable reuse scores. 19 layouts stands as the final count.
- **Options page**: reuses the existing `m11-site-settings` (`group_m11_site_settings`) as-is for
  logo/contact/hours/socials/sales-hub-name; adds ONE new field (`product_page_kicker`). No new
  Header/Footer/SEO options pages — the existing Theme Builder header/footer + this group already cover
  everything the design needs.
- **Menus**: reuses the 8 already-registered native WP menus (Primary, 4 footer columns, Legal, Language,
  Sales Hub, Sales Hub - Legal); the Primary menu's Products item gets a native edit (build step B5, not
  ACF work) to fix the spec's header link defect site-wide.
- **Sales Hub portal chrome** (header/footer): DECIDED — 2 new Elementor Theme Builder templates with
  Display Conditions on the sales-hub page tree, matching the existing public 61/62 mechanism (build step
  B4).
- **Coverage**: `check_acf_coverage.py --stage plan` → 0 HIGH / 0 MED / 0 LOW across all 9 spec pages,
  221 fields checked, 100% accounted for (editable or explicitly waived above) — re-verified after this
  approval pass.

---
**Approved.** `spec/acf-plan.json` has `"approved": true` with a full `decision_record` and
`build_steps`. Next: html-acf-builder generates the ACF Local JSON (acf-json/) per this plan, followed by
html-php-writer (template parts + single-m11_product.php) and the remaining build steps (B1–B6) above.
