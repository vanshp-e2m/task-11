# 11.3 Capstone — Final submission (Vansh Patel)

**Task:** convert the Figma file
[Module-11 figma design](https://www.figma.com/design/jSb9GvLZzl7AFll93svlAE/Module-11-figma-design?node-id=0-1&t=bjxnj2rhJsOuhoBm-1)
(Mizuho America, 11 pages, desktop + mobile) using the **Elementor page builder** and **custom field settings with ACF**.

**Built on:** local practice site **task-11.local** (Local by Flywheel), WordPress + ACF Pro + Elementor Pro, child theme **`module11`**
(parent Hello Elementor). WordPress changes went through **DevConnect** abilities via the **DevCommand** plugin in Claude Code;
every write was read back.

**Single submission index (all links + decision record):** [docs/SUBMISSION.md](docs/SUBMISSION.md)

---

## Deliverables

### 1. The built site — theme, `acf-json/` and a database export
| Item | Where |
|---|---|
| Theme repository | [`wp-content/themes/module11/`](wp-content/themes/module11) — 19 Flexible Content layouts (one template part + one SCSS partial each), product CPT template with 3 variants, Sales Hub gate, Site Settings dynamic tags for Elementor, compiled CSS |
| `acf-json/` | [`wp-content/themes/module11/acf-json/`](wp-content/themes/module11/acf-json) — Page Sections (19 layouts), Product Fields, Resource Fields, Site Settings, shared clones |
| Theme zip | [`dist/module11-theme.zip`](dist/module11-theme.zip) (includes `acf-json/`) — also attached to the submission |
| Database export | `task-11.sql` (3.8 MB) — **attached to the submission separately**, not committed (it contains user emails and password hashes) |

### 2. Flow A evidence — generated HTML, conversion output, final page, and every place the conversion was wrong
Figma → generated HTML → DevCommand HTML→ACF pipeline → editable ACF pages (Home, Resources, Products + 3 product variants,
Sales Hub Login / Dashboard / Resource Library).
| Evidence | Where |
|---|---|
| Generated HTML (every page) | [`pages/<slug>/html/`](pages) (e.g. [`pages/mizuho-home/html/`](pages/mizuho-home/html)) |
| Conversion input/plan | spec [`spec/site-spec.json`](spec), review [docs/spec-review.md](docs/spec-review.md), approved ACF plan [docs/acf-review-table.md](docs/acf-review-table.md) |
| Conversion output (untouched) | [`output/theme/module11/`](output/theme/module11) |
| Final pages vs the generated HTML, per section | [docs/evidence/flow-a/wp-vs-replica/](docs/evidence/flow-a/wp-vs-replica) — 0–5% pixel difference at 1440 on every page, section heights exact |
| **Every place the conversion was wrong + what I did** | [docs/devconnect-conversion-issues.md](docs/devconnect-conversion-issues.md) (C1–C14 ACF, D1–D7 About, E1–E10 Contact) and [docs/issues-log.md](docs/issues-log.md) |

Where the conversion was wrong (main points):
- **Sections merged and dropped:** on Resources the slicer merged Testimonials + Brochures into one block, and on the product pages it dropped Accessories, Related products, Instruments included and Size guide → caught by comparing against the expected sections, slicer rule patched, re-run ([evidence](docs/evidence/flow-a/conversion/slicer-bug)).
- **Wrong field types:** 16 link fields created as ACF URL fields holding `#anchors`, so wp-admin refused to save → changed to text fields, same keys.
- **Missing fields:** the Products hero photo was a CSS background with no field → background image fields added.
- **Name clash:** a clone and its inner repeater both named `buttons`, so product buttons never saved → plain repeater.
- **Deployer couldn't read the assembler's seed** → `tools/seed_acf.py` pushes the same seed through DevConnect, every value read back.
- **Fragile layout:** desktop CSS pinned to Figma coordinates, so longer headings overlapped content → measured row grids, same pixels.
- **Hard-coded colours** in the generated CSS → tokenised so the Elementor Kit drives the ACF pages too.

### 3. Flow B evidence — global settings structure + proof one value updates multiple places
- **Elementor pages:** About Us and Contact Us. DevConnect's draft was HTML widgets only → rebuilt natively (Pro Form, Nested Accordion):
  [docs/evidence/flow-b/about/](docs/evidence/flow-b/about), [docs/evidence/flow-b/contact/](docs/evidence/flow-b/contact).
- **Header and footer:** Elementor Theme Builder templates (public + Sales Hub), shared by both builders.
- **Global settings structure:**
  - **ACF Site Settings** (options page): logo, reversed logo, phone, fax, email, hours, address. Read by Elementor through the
    theme's dynamic tags (`inc/elementor/`) and by the ACF templates through `m11_get_setting()`.
  - **Elementor Kit:** brand colours and fonts. Elementor uses `__globals__`; the theme maps `--e-global-*` → `var(--clr-*)`.
- **Proof:** one phone change and one Kit colour change update **7 pages across both builders**, then revert:
  [docs/evidence/flow-b/global-proof/README.md](docs/evidence/flow-b/global-proof/README.md) (before / after / reverted screenshots + measured table).

### 4. Decision record (1–2 pages)
[docs/decision-record.md](docs/decision-record.md) (also included in full in [docs/SUBMISSION.md](docs/SUBMISSION.md)), covering:
- which sections I coded vs handed to a builder, and why;
- how I structured the fields and what I deliberately did not make editable;
- where the AI tooling was wrong and how I caught it;
- what I would do differently with another day.

### 5. Responsive evidence — three breakpoints side by side with the Figma frame
[docs/evidence/responsive/](docs/evidence/responsive/README.md): every page as **Figma 1440 | WordPress 1440 | 768 | 430 | Figma 430**,
plus overflow checks at 390 and 1920 (no page scrolls sideways). Sheets:
[Home](docs/evidence/responsive/home.png) · [About](docs/evidence/responsive/about-us.png) · [Contact](docs/evidence/responsive/contact-us.png) ·
[Resources](docs/evidence/responsive/resources.png) · [Products](docs/evidence/responsive/products.png) ·
[Product Main](docs/evidence/responsive/product-main.png) · [Variation A](docs/evidence/responsive/product-a.png) ·
[Variation B](docs/evidence/responsive/product-b.png) · [Login](docs/evidence/responsive/sales-hub-login.png) ·
[Dashboard](docs/evidence/responsive/dashboard.png) · [Resource Library](docs/evidence/responsive/resource-library.png)

### 6. Robustness evidence — double-length heading, empty optional field, wrongly-proportioned image
[docs/evidence/robustness/](docs/evidence/robustness/README.md): **all 19 ACF layouts + the product template**, each tested three ways
at 1440 and 430 — 136 automated checks plus a visual review of every screenshot. Screenshots:
[long headings](docs/evidence/robustness/page-long-1440.png) · [empty fields](docs/evidence/robustness/page-empty-1440.png) ·
[wrong-ratio images](docs/evidence/robustness/page-ratio-1440.png) · [product, long, mobile](docs/evidence/robustness/product-long-430.png).
The automated checks passed while the screenshots showed overlaps — fixed, and documented in the README there.

### 7. Final Loom (10–15 minutes)
- https://www.loom.com/share/77595426a8574448b7afb7613b8d408d
- https://www.loom.com/share/2fb37c66df5344dca9e0248f75c36092
- https://www.loom.com/share/8c1202deabc848368f3924c640b24fed

| Asked for | Status |
|---|---|
| Front-end walkthrough | in the Looms |
| Editing content live in wp-admin | in the Looms |
| A global value updating in two places | in the Looms (+ [written proof](docs/evidence/flow-b/global-proof/README.md)) |
| The maintenance change | **no maintenance ticket was issued** for this capstone ([note](docs/evidence/maintenance/README.md)) |
| An honest account of what went wrong | in the Looms (+ [issues log](docs/issues-log.md): the 7 main problems, how each was found, caused and fixed) |

---

## Submission
- **Index file** (all links: repo, Loom, screenshots + the decision record): [docs/SUBMISSION.md](docs/SUBMISSION.md)
- **Attached separately:** theme zip `dist/module11-theme.zip` (194 KB) and database export `task-11.sql` (3.8 MB).
- **Repository:** https://github.com/vanshp-e2m/task-11

## Done when
| Criterion | Status / evidence |
|---|---|
| Flow A produces an editable page from the Figma file | ✅ ACF pages generated through DevCommand's HTML→ACF pipeline; every visible value is a field, no defaults, sections can be hidden/reordered ([wp-admin screenshot](docs/evidence/flow-a/wp-vs-replica/admin-home.png)) |
| Flow B does the same with global settings handled centrally | ✅ About/Contact in Elementor; business data in Site Settings, colours/fonts in the Kit, used by both builders ([proof](docs/evidence/flow-b/global-proof/README.md)) |
| The maintenance ticket is complete, documented, and nothing else regressed | — no ticket was issued. Regression checks after every change: per-section fidelity gate, responsive and robustness scripts ([note](docs/evidence/maintenance/README.md)) |
| You can walk someone through every step and justify the decisions | ✅ [docs/WALKTHROUGH.md](docs/WALKTHROUGH.md), step log [docs/BUILD-NOTES.md](docs/BUILD-NOTES.md), [decision record](docs/decision-record.md) |
| You can explain what DevConnect does and what DevCommand does | ✅ below, and decision record §5 |

## DevConnect vs DevCommand, in my own words
- **DevConnect** is the WordPress plugin on the site. It exposes the site's abilities (create pages, write ACF values, upload media,
  write Elementor data, snapshots/rollback, audit log) as an authenticated MCP server. It is the hands: the only thing that touches WordPress.
- **DevCommand** is the Claude Code plugin on my machine: agents and skills that plan the work, extract the design, generate fields,
  templates and CSS, and call DevConnect to apply them. It is the brain and the workflow.
- Neither can be trusted blindly: several abilities reported success without saving everything, and the conversions needed fixing.
  Every write was read back and every page checked — that is where the findings in the issues log came from.

## Safe working
Local site only (never a client site); a DB snapshot before every destructive step (`backups/00`–`13`, kept locally); credentials only in the
local Claude config; DevCommand's maint-qa run with PASS verdicts and its QA ledger closed.
