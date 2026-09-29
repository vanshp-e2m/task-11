# Walkthrough — rebuild and re-verify this project

For a colleague repeating the build on **their own local copy**. Every command runs from the site root
(`…/Local Sites/task-11/app/public`) in Git Bash. **Only ever target `http://task-11.local`** — never a client site.

## 0. Environment (details: `00-setup-walkthrough.md`)
1. Start the site in Local (or `mutation { startSite(id:"PXH8o8TpS") }` on Local's GraphQL API, see issues-log #62).
2. `tools/wp.sh option get siteurl` → `http://task-11.local`. (The wrapper disables Git Bash path conversion — issues-log #67.)
3. Connect DevConnect: `/dev-connect` in Claude Code (credentials stay in the local Claude config), then `/dev-doctor`.
4. Snapshot before anything destructive: `tools/snapshot.sh <label>` → `backups/NN-<label>.sql`.

## 1. Restore the finished site instead of rebuilding
- Theme: unzip `dist/module11-theme.zip` into `wp-content/themes/` and activate **Module 11** (child of Hello Elementor).
- Database: `tools/wp.sh db import docs/db-export/task-11.sql` (local test users: `qa-rep` / `QaRep-2026-local` = sales rep,
  `qa-editor` / `QaEditor-2026-local` = editor).
- Plugins: ACF Pro 6.8.5, Elementor 4.3.1, Elementor Pro 4.0.0, DevConnect 0.3.5.

## 2. Flow A — Figma → generated HTML → ACF (Home, Resources, Products, Sales Hub)
1. **Generated HTML** per page: `python tools/figma_html/build_<page>.py` → DevCommand's compiler → `pages/<slug>/html/`
   (open them with `cd pages && python -m http.server 8767`).
2. **Package + parse:** `python tools/figma_html/package_acf_site.py` → `source/html-site.zip`; run DevCommand's
   `html-project-extractor` → `html-parser` (review `docs/spec-review.md`) → `html-acf-planner` (sign-off: `docs/acf-review-table.md`,
   `spec/acf-plan.json`) → `html-acf-builder` → `html-php-writer` → `html-theme-assembler` (output kept untouched in `output/theme/module11/`).
3. **Into the theme:** field groups as Local JSON (`acf-json/`, never via `dev/acf-manage-field-groups` — issue #12); templates in
   `template-parts/flex-blocks/`; CSS: `python tools/figma_html/split_replica_css.py` then `python tools/figma_html/flow_desktop.py`
   (after `node tools/evidence/measure_flow.js cache/evidence/flow-measure.json`), then `cd wp-content/themes/module11 && npm run build`.
4. **Content:** `python tools/seed_acf.py --phase all` (media, CPT posts, terms, fields, pages, options, verify — every value read back).

## 3. Flow B — Elementor pages + global settings
- About: `bash tools/about/publish.sh` · Contact: `python tools/elementor/build_contact.py`, write the tree with
  `dev-connect-elementor-set-page-data`, delete `_elementor_element_cache`, `tools/wp.sh elementor flush-css`, count stored nodes.
- Chrome: `python tools/elementor/build_chrome.py` → Theme Builder templates 61/62 (public) and 255/256 (Sales Hub).
- Global values: Site Settings (ACF options) for business data; Elementor Kit for colours/fonts.

## 4. Verify (each writes its own evidence)
| Check | Command | Evidence |
|---|---|---|
| Fidelity vs the generated HTML, per section | `python tools/qa_wp_vs_replica.py --widths 1440,768,430` | `docs/evidence/flow-a/wp-vs-replica/` |
| Responsive vs Figma (1440/768/430 + overflow 390/1920) | `python tools/evidence/responsive.py` | `docs/evidence/responsive/` |
| Robustness (long / empty / wrong ratio) | `python tools/evidence/robustness.py setup` then `… check` — **and look at the screenshots** (#65) | `docs/evidence/robustness/` |
| One global change → every page | `python tools/evidence/global_proof.py` (changes and reverts) | `docs/evidence/flow-b/global-proof/` |
| Editability | log in as `qa-editor`, open Home: classic screen, numbered sections | `docs/evidence/flow-a/wp-vs-replica/admin-*.png` |

Whenever a tool or conversion gets something wrong: add it to `docs/issues-log.md` (symptom → how noticed → cause → fix →
verified) and the matching row in `docs/BUILD-NOTES.md`.
