# Module 11 capstone — submission index (Vansh Patel)

Mizuho America, built from Figma on the local WordPress site **task-11.local** (Hello Elementor child theme `module11`,
ACF Pro, Elementor Pro, DevConnect + DevCommand in Claude Code). ACF for the structured pages, Elementor for About/Contact,
global settings in ACF Site Settings + the Elementor Kit.

## Links

| What | Link |
|---|---|
| **Repository** | https://github.com/vanshp-e2m/task-11 |
| **Figma file** | https://www.figma.com/design/jSb9GvLZzl7AFll93svlAE/Module-11-figma-design?node-id=0-1 |
| **Loom — part 1** | https://www.loom.com/share/77595426a8574448b7afb7613b8d408d |
| **Loom — part 2** | https://www.loom.com/share/2fb37c66df5344dca9e0248f75c36092 |
| **Loom — part 3** | https://www.loom.com/share/8c1202deabc848368f3924c640b24fed |
| Theme zip (incl. `acf-json/`) | attached · also in the repo: [dist/module11-theme.zip](https://github.com/vanshp-e2m/task-11/blob/main/dist/module11-theme.zip) |
| Database export | attached separately (`task-11.sql`, 3.8 MB — kept out of the public repo: it holds user emails and password hashes) |

Local test logins (only valid on a local import of the DB): `qa-editor` / `QaEditor-2026-local` (editor), `qa-rep` / `QaRep-2026-local` (Sales Hub rep).

## Deliverables

| Deliverable | Evidence |
|---|---|
| **Built site** | theme source [wp-content/themes/module11/](https://github.com/vanshp-e2m/task-11/tree/main/wp-content/themes/module11) · field groups [acf-json/](https://github.com/vanshp-e2m/task-11/tree/main/wp-content/themes/module11/acf-json) · zip + DB export attached |
| **Flow A** — Figma → generated HTML → ACF | generated HTML [pages/<slug>/html/](https://github.com/vanshp-e2m/task-11/tree/main/pages) · spec [spec-review.md](https://github.com/vanshp-e2m/task-11/blob/main/docs/spec-review.md) · approved ACF plan [acf-review-table.md](https://github.com/vanshp-e2m/task-11/blob/main/docs/acf-review-table.md) · untouched conversion output [output/theme/module11/](https://github.com/vanshp-e2m/task-11/tree/main/output/theme/module11) · final pages vs the generated HTML, per section [wp-vs-replica/](https://github.com/vanshp-e2m/task-11/tree/main/docs/evidence/flow-a/wp-vs-replica) · **every place the conversion was wrong** [devconnect-conversion-issues.md](https://github.com/vanshp-e2m/task-11/blob/main/docs/devconnect-conversion-issues.md) (C1–C14, D1–D7, E1–E10) + [slicer bug evidence](https://github.com/vanshp-e2m/task-11/tree/main/docs/evidence/flow-a/conversion/slicer-bug) |
| **Flow B** — global settings + proof | structure: decision record §1 below · proof (one phone change + one Kit colour change → 7 pages, both builders, reverted) [global-proof/README.md](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/flow-b/global-proof/README.md) · screenshots [before](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/flow-b/global-proof/1-before-home.png) / [after](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/flow-b/global-proof/2-after-home.png) / [after, Contact](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/flow-b/global-proof/2-after-contact-us.png) |
| Elementor pages (About, Contact) | DevConnect draft vs native rebuild [about/](https://github.com/vanshp-e2m/task-11/tree/main/docs/evidence/flow-b/about) · [contact/](https://github.com/vanshp-e2m/task-11/tree/main/docs/evidence/flow-b/contact) |
| **Responsive** — 3 breakpoints next to Figma | [responsive/README.md](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/responsive/README.md) · sheets: [Home](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/responsive/home.png) · [About](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/responsive/about-us.png) · [Contact](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/responsive/contact-us.png) · [Resources](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/responsive/resources.png) · [Products](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/responsive/products.png) · [Product Main](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/responsive/product-main.png) · [Variation A](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/responsive/product-a.png) · [Variation B](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/responsive/product-b.png) · [Login](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/responsive/sales-hub-login.png) · [Dashboard](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/responsive/dashboard.png) · [Resource Library](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/responsive/resource-library.png) |
| **Robustness** — double heading / empty field / wrong ratio, every section | [robustness/README.md](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/robustness/README.md) (19 layouts + product template, 136 checks + visual review) · [long 1440](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/robustness/page-long-1440.png) · [empty 1440](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/robustness/page-empty-1440.png) · [ratio 1440](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/robustness/page-ratio-1440.png) · [product, long 430](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/robustness/product-long-430.png) |
| Editability (wp-admin) | [Home edit screen](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/flow-a/wp-vs-replica/admin-home.png) · [product](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/flow-a/wp-vs-replica/admin-product.png) · [resource](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/flow-a/wp-vs-replica/admin-resource.png) |
| Maintenance ticket | change note: [maintenance/README.md](https://github.com/vanshp-e2m/task-11/blob/main/docs/evidence/maintenance/README.md) (to be completed with the ticket details) |
| Walkthrough (repeatable) | [WALKTHROUGH.md](https://github.com/vanshp-e2m/task-11/blob/main/docs/WALKTHROUGH.md) · [00-setup-walkthrough.md](https://github.com/vanshp-e2m/task-11/blob/main/docs/00-setup-walkthrough.md) · step log [BUILD-NOTES.md](https://github.com/vanshp-e2m/task-11/blob/main/docs/BUILD-NOTES.md) |
| What went wrong, and how it was caught | [issues-log.md](https://github.com/vanshp-e2m/task-11/blob/main/docs/issues-log.md) — 69 issues, each: symptom → how noticed → cause → fix → verified |

## Done-when checklist
- **Flow A produces an editable page from the Figma file** — Home, Resources, Products (+ 3 product variants) and the Sales Hub pages are
  ACF Flexible Content / CPT pages generated through DevCommand's HTML→ACF pipeline; every visible value is a field.
- **Flow B does the same with global settings handled centrally** — About/Contact in Elementor; logo, phone, email, address in Site
  Settings and colours/fonts in the Kit, used by both builders (proof above).
- **You can walk someone through every step** — WALKTHROUGH.md + the Looms; **DevConnect vs DevCommand** — decision record §5.

## Known, accepted residuals
Listing pages are taller than Figma because they list the real 23 products / 47 resources. At 430px: Resources testimonials −18px,
Product A/B overview −33/−22px vs the generated HTML. No brochure PDFs are seeded, so "Read description" falls back to the
Resources brochures section. Robustness test posts `qa-robustness-*` are private.

---

## Decision record

### 1. What was coded, what was handed to a builder, and why

| Part | Built with | Why |
|---|---|---|
| Home, Resources, Products browse, Sales Hub (Login, Dashboard, Resource Library) | **ACF Flexible Content** (`sections`, 19 layouts) produced by DevCommand's **HTML→ACF** pipeline from the generated HTML (Flow A) | Repeating, structured content (slides, cards, testimonials, tiles, filters). Fields keep editors inside the design; the markup is reviewable code; the listings are real queries. |
| Products (one template, three variants) | **CPT `m11_product`** + one `single-m11_product.php`; the variant follows the content (instruments table → A, size guide → B, else Main) | 23 products share one template: a new product is data entry, not a page build. |
| Resources data | **CPT `m11_resource`** (not public) + taxonomies, surfaced on Resources and the Resource Library | One brochure/video is entered once and appears everywhere it is listed. |
| About Us, Contact Us | **Elementor** (native widgets only; Pro Form, Nested Accordion) | Marketing pages the client edits visually; the form needs submissions + email without another plugin. |
| Header / footer (public + Sales Hub) | **Elementor Theme Builder** templates from a generator (`tools/elementor/build_chrome.py`) | Built once, shared by both builders; display conditions pick the public or portal chrome. |
| Colours, fonts | **Elementor Kit** | One source for both builders: Elementor via `__globals__`, the theme via `--e-global-*` → `var(--clr-*)`. |
| Business data (logo, phone, fax, email, hours, address) | **ACF Site Settings** (options page) | Read by Elementor through the theme's dynamic tags and by ACF templates through `m11_get_setting()`. |

Rejected: building everything in Elementor (listings and 23 products would be hand-built pages, not data); building everything
in ACF (About/Contact gain nothing from code and lose visual editing); DevCommand's direct Figma→ACF pipeline (Flow A was
agreed as Figma → generated HTML → ACF so the conversion step itself could be inspected).

### 2. Field structure, and what I deliberately did not make editable

- **One Flexible Content field, 19 layouts**, each = one template part + one SCSS partial. Every layout starts with
  **Section Settings** (hide section, anchor id) then **Section Content**. **No field has a default value and none is required**:
  the robustness test empties every optional field and each section still renders cleanly.
- **Relationships instead of copies:** testimonials/videos/brochures/related products are relationship fields to the CPTs.
- **Editable:** every visible string, image, link and list item, the order of sections, which products/resources appear.
- **Not editable, on purpose:** layout geometry (column widths, spacing, the Figma grid) lives in SCSS, so an editor can change
  content but not break the design; decoration without content (rules, slider dots, carousel arrows); the product *variant*
  (it follows the content, so it can't disagree with it); Site-wide values are **only** editable in Site Settings / the Kit, never per page.
- **Editor experience:** Flexible Content pages open in the classic screen with numbered, labelled sections (#60); editors can
  preview Sales Hub pages (#64); a layout keeps its design on any page it is added to (#63).

### 3. Where the AI tooling was wrong, and how I caught it (full list: `issues-log.md` #1–#69)

- **The conversion merged and dropped sections** — DevCommand's slicer turned 9 Resources sections into 5 (#54). Caught by counting
  sections against the spec; patched the slicer's implied-close rule; evidence kept.
- **DevConnect's HTML→Elementor conversion** produced HTML widgets only (About: 7, Contact: 1 for the whole page with its form) (#30, #61).
  Caught by counting widget types; rebuilt natively.
- **The deployer couldn't read the assembler's own seed** (#57) → wrote `tools/seed_acf.py`; **seed values that never stored**
  (seamless clone, `<br>` markup, a name clash) (#58) → caught by reading every value back.
- **Pixel-perfect but fragile:** the generated desktop CSS used Figma's absolute coordinates; a longer heading overlapped the content
  below (#65). **The automated checks passed; the screenshots didn't** — fixed with measured row grids that keep every pixel.
- **Global settings that only looked global:** a Kit colour change reached no page (literal hex in generated CSS + tokens declared
  where Elementor's variables don't exist) (#66). Caught only because the proof measured colours instead of assuming them.
- **Environment traps:** Git Bash rewrote `/%postname%/` into a Windows path (#67); the site stopped after a reboot (#62).

### 4. What I'd do differently with another day

- Generate the desktop CSS as flow/grid from the start instead of converting absolute coordinates afterwards.
- Seed real brochure PDFs so "Read description"/download links point at files, and add a resource single view if the client wants one.
- Close the last mobile residuals (Resources testimonials −18px, Product A/B overview −33/−22px at 430) and the replica's own
  deviations from Figma mobile (bold group titles on Resources).
- Put the fidelity, robustness and global-proof scripts in CI so every change re-runs them.

### 5. DevConnect vs DevCommand, in my own words

- **DevConnect** is the WordPress plugin: it exposes the site's abilities (create pages, write ACF values, upload media, Elementor
  data, snapshots/rollback) as an authenticated MCP server. It's the hands — the only thing that touches WordPress, with
  permissions, audit log and a QA ledger.
- **DevCommand** is the Claude Code plugin: agents and skills that plan, extract, generate fields/templates/SCSS and call DevConnect.
  It's the brain and the workflow. Its output still needs checking: every stage here was verified by measurement, and the
  places it was wrong are the most useful part of this submission.
