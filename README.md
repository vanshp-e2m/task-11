# 11.3 Capstone — Mizuho America, Figma → WordPress (Elementor + ACF, DevConnect + DevCommand)

Local practice site **task-11.local** (Local by Flywheel), WordPress + ACF Pro + Elementor Pro, custom child theme **`module11`**
(parent: Hello Elementor). Built from the Figma file
[Module-11 figma design](https://www.figma.com/design/jSb9GvLZzl7AFll93svlAE/Module-11-figma-design?node-id=0-1): 11 pages, desktop + mobile.
WordPress changes were made through DevConnect abilities via the DevCommand plugin in Claude Code (WP-CLI for page templates,
terms and cache flushes; every write read back).

## Loom videos

- https://www.loom.com/share/77595426a8574448b7afb7613b8d408d
- https://www.loom.com/share/2fb37c66df5344dca9e0248f75c36092
- https://www.loom.com/share/8c1202deabc848368f3924c640b24fed

Covered: a front-end walkthrough, editing content live in wp-admin, a global value updating in several places, and an honest
account of what went wrong along the way.

## Written notes

**[docs/SUBMISSION.md](docs/SUBMISSION.md)** is the single submission index: every link (repo, Loom, screenshots) plus the decision record.

- [docs/decision-record.md](docs/decision-record.md): what was coded vs built in a builder and why, the field structure and what is
  deliberately not editable, where the AI tooling was wrong, what I'd do with another day, and DevConnect vs DevCommand.
- [docs/issues-log.md](docs/issues-log.md): **69 issues**, each as symptom → how it was noticed → root cause → fix → how it was verified.
- [docs/devconnect-conversion-issues.md](docs/devconnect-conversion-issues.md): every place a conversion was wrong, per page and section.
- [docs/WALKTHROUGH.md](docs/WALKTHROUGH.md): how a colleague rebuilds and re-verifies everything. [docs/BUILD-NOTES.md](docs/BUILD-NOTES.md): the step log.

## Repository contents

| Path | What it is |
|---|---|
| `docs/SUBMISSION.md` | The submission index: all links + the decision record. |
| `wp-content/themes/module11/` | The theme: 19 Flexible Content layouts (one template part + one SCSS partial each), the product CPT template (3 variants), Sales Hub gate, Site Settings dynamic tags for Elementor, compiled CSS. |
| `wp-content/themes/module11/acf-json/` | ACF field groups (Local JSON): Page Sections (19 layouts), Product Fields, Resource Fields, Site Settings, shared clones. |
| `dist/module11-theme.zip` | The theme as an installable zip (includes `acf-json/`). |
| `pages/<slug>/html/` | **Flow A input** — the generated HTML for every Figma page (DevCommand compiler). `pages/_figma/` = Figma exports. |
| `spec/`, `output/theme/module11/` | **Flow A conversion** — DevCommand's site spec, the approved ACF plan, and the untouched HTML→ACF conversion output. |
| `docs/evidence/flow-a/` | Final pages vs the generated HTML, per section, at 1440 / 430; conversion evidence (slicer bug); wp-admin screenshots. |
| `docs/evidence/flow-b/` | Elementor pages (DevConnect draft vs native rebuild) and the **global settings proof** (`global-proof/`). |
| `docs/evidence/responsive/` | Every page at 1440 / 768 / 430 next to its Figma frame, plus overflow checks at 390 and 1920. |
| `docs/evidence/robustness/` | Every layout with a double-length heading, empty optional fields and wrong-ratio images (136 checks + visual review). |
| `tools/` | The scripts behind everything: HTML generators, WP-CLI wrapper, snapshots, seeding, Elementor tree builders, QA and evidence scripts. |
| `project-config.json`, `design-system/`, `CLAUDE.md` | DevCommand project config, registries, and the project rules Claude Code worked under. |

## Flows

**Flow A — Figma → generated HTML → editable ACF pages** (Home, Resources, Products + 3 product variants, Sales Hub Login /
Dashboard / Resource Library):
1. Figma → HTML for every page (`tools/figma_html/`, DevCommand compiler), checked against the Figma frames.
2. DevCommand HTML→ACF pipeline: extractor → parser (spec review) → ACF planner (sign-off table) → field builder → PHP writer →
   theme assembler.
3. Field groups as Local JSON, templates + SCSS in the theme; content seeded through `dev/upload-media`, `dev/create-custom-post`
   and `dev/acf-read-write-values`, every value read back.
4. Edited in wp-admin to prove the pages are editable: numbered sections, Section Settings / Section Content tabs, no defaults.

**Flow B — Elementor pages + global settings** (About Us, Contact Us, header, footer):
- DevConnect draft (`dev/convert-html`) → native Elementor rebuild (Pro Form, Nested Accordion), written with
  `dev-connect/elementor-set-page-data`, stored nodes counted.
- Header/footer as Elementor Theme Builder templates (public + Sales Hub).
- **Global settings:** business data (logo, phone, fax, email, hours, address) in ACF **Site Settings**, read by Elementor through the
  theme's dynamic tags and by ACF templates through `m11_get_setting()`; colours and fonts in the **Elementor Kit**, used by both builders.
  One phone change and one colour change update 7 pages across both builders
  ([proof](docs/evidence/flow-b/global-proof/README.md)).

**Safe working:** local site only; a DB snapshot before every destructive step (`backups/00`–`13`); credentials only in the local
Claude config; writes through DevConnect and read back; DevCommand's maint-qa ran with PASS verdicts and its QA ledger was closed.

## Major findings

1. **DevConnect's HTML→Elementor conversion made code boxes, not pages.** About Us came out as 7 HTML widgets, Contact Us as one widget for
   the whole page (the form included). Caught by counting widget types → rebuilt natively; every text/image is now an Elementor widget.
2. **The HTML→ACF conversion merged and dropped sections.** DevCommand's slicer turned the 9 Resources sections into 5. Caught by counting
   against the page → patched the slicer rule, re-ran, evidence kept.
3. **"Success" that wasn't.** `dev/acf-manage-field-groups` saved the Site Settings group with 0 of 26 fields; `dev/build-page` stored
   1 node of the header/footer (20/29); `dev/acf-read-write-values` accepted values ACF silently ignored (section ids, product buttons);
   `set-page-data` left the old page cached. Fix: never trust the success flag — read back and look at the live page.
4. **The pipeline didn't fit together.** DevCommand's deployer couldn't read its own assembler's seed → `tools/seed_acf.py` pushes the same
   seed through DevConnect.
5. **Pixel-perfect but fragile.** The generated desktop CSS pinned everything to Figma coordinates, so a longer heading overlapped the
   content below. **The automated checks passed; the screenshots didn't.** Fixed with measured row grids that keep every drawn pixel.
6. **Global settings that only looked global.** A Kit colour change reached no page: the generated CSS had literal hex values, and the
   theme tokens were declared where Elementor's variables don't exist. Found only because the proof measured the colours.
7. **Editing broke on save.** 16 link fields were typed as ACF URL fields but hold anchors (`#section`), so wp-admin refused to save →
   changed to text fields with the same keys; the API seed had never run the form validation.
8. **Editability gaps found by testing, not by the tools.** A layout lost its styles on any other page; editors couldn't preview Sales Hub
   pages; Flexible Content pages opened in an empty block editor with the sections hidden — all fixed.
9. **Environment traps.** Git Bash rewrote `/%postname%/` into a Windows path (broken archives); the site stopped after a reboot
   (MCP `ECONNREFUSED`). Fixed in the WP-CLI wrapper / started through Local's API.
10. **Takeaway.** DevCommand and DevConnect save a lot of time, but their output has to be verified: every finding above was caught by
    measuring or looking, not by the tools' own checks. Full list: [docs/issues-log.md](docs/issues-log.md).

## Maintenance ticket

No maintenance ticket was issued for this capstone, so there is no maintenance change to document
([note](docs/evidence/maintenance/README.md)).

## Not included

- WordPress core, plugins (ACF Pro and Elementor Pro are licensed), uploads and DB snapshots.
- The database export: attached to the submission separately (it contains user emails and password hashes).
- Credentials: no application passwords or tokens are committed.
