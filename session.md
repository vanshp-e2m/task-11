# Session log — task-11 (Module 11 capstone · Mizuho America design)

- 2026-09-25 — Step 0: environment set up. Snapshots 00 (fresh) and 01 (stack installed); plugins DevConnect 0.3.5 (Windows-patched build, issue #5), ACF Pro 6.8.5, Elementor 4.3.1, Elementor Pro 4.0.0; `module11` child theme of Hello Elementor; git repo initialised (not yet committed). See docs/00-setup-walkthrough.md.
- 2026-09-25 — Figma file `jSb9GvLZzl7AFll93svlAE` read via REST (new token with file_content:read, issue #4); 11 desktop + 11 mobile frames, no tablet. Approach written: docs/01-approach.md.
- 2026-09-25 — dev-command connected with the developer's application password; MCP path-case fix (issue #7); `/dev-doctor` passed (219 abilities baselined in cache/ability-baseline.json; smoke + integrity OK); `{}` → `{"_":1}` workaround (issue #6).
- 2026-09-25 — `/dev-start`: warm start from project-config.json (hand-written in Step 0, builder `acf`). Drift check clean (only default WP pages). Awaiting scope decisions before extraction.
- 2026-09-25 — Decisions: Home = ACF (Flow A), About Us = Elementor (Flow B); globals = Theme Builder header/footer + Elementor Kit + ACF Site Settings; Gotham → Montserrat; hero = Swiper slider from a repeater; brief defaults (no CSS framework, Google Fonts, Swiper via CDN). Recorded in project-config.json + docs/decision-record.md.
- 2026-09-25 — Extractor refused 'home' (homepage guard, issue #8). Decision: build Home as inner page `mizuho-home`; front-page switch is a manual step at the end. Re-running extraction.
- 2026-09-25 — Step 1 extraction (mizuho-home) done by acf-figma-design-extractor: 8 sections (2 global), validator valid. Verified claims myself (docs/02-extraction-review.md); one of my own checks was wrong (Fraunces run hidden in style overrides). Figma render endpoint locked ~4.6 days (issue #9): cached full-frame renders are the QA reference. Awaiting design-flag decisions.
- 2026-09-25 — Developer accepted all extraction recommendations. SCOPE EXPANDED: build every page in the Figma file, linked through the navigation (not only Home + About). Inventory → docs/03-site-inventory.md.
- 2026-09-25 — Manual Figma exports collected: 18/22 frames (deduped by hash, 1 overflow cropped). Missing 4 mobile frames. Issues #10, #11.
- 2026-09-25 — All 22 Figma frames exported manually and verified (pages/_figma/frames/export/). QA reference complete.
- 2026-09-25 — Step 1a done: Elementor Kit colours+typography; theme tokens read --e-global-*; fonts enqueued once; ACF Site Settings as Local JSON (issue #12: bridge create drops fields) + values written & read back. Snapshot 03.
- 2026-09-25 — Step 1b done: 9 page shells, 9 menus, Theme Builder header (61) + footer (62) via generator + validator; Site Settings trimmed to shared values; custom Site Settings dynamic tags; measured vs Figma 1440/768/430; phone global proof. Issues #13–#16. Snapshot 05.
- 2026-09-25 — Step 2a: figma-html-planner blueprint approved by developer (+ procedure_band even columns). Planner's copy was screenshot-transcribed (issue #17) → planner resumed to re-source all strings from Figma JSON, then compile + QA.
- 2026-09-25 — Step 2a: HTML compiled (dist/); raw archived; copy 71/71 verbatim; fixed broken font URL (#18); planner stalled (#19); own QA → findings G1–G8 → figma-html-targeted-fixer running.
- 2026-09-25 — Found root cause #21: planner wrote its own compiler (tools/figma_html/compile_blueprint.py); real DevCommand compiler runs via wrapper but validator: 69 violations + 31 placeholders on current blueprint. Awaiting developer decision to re-plan against the real recipes.
- 2026-09-28 — Developer: Flow A stays on Figma→HTML (no direct Figma→ACF). Re-plan agent hit usage limit (#23); #22 logged. Site 502 (Local stopped) — not needed for the HTML step.
- 2026-09-28 — Step 2a DONE: DevCommand real compiler, validator valid:true; round-2 fixes H1–H5; K1–K3 carried to ACF step. Frozen: docs/evidence/flow-a/03-generated-html-final/.
- 2026-09-28 — Round 3 (developer review): static header+footer added, value columns rebuilt to exact Figma geometry, footer spacing + fonts (#25 validator false positive, #26 compiler font axes). Awaiting next section issues from developer.
- 2026-09-28 — Round 4: full replica rebuild of the generated HTML (desktop exact + scaled, mobile per Figma 1:400); verified 1440/1024/768/430; issue #27. Frozen: docs/evidence/flow-a/04-generated-html-replica/.

## About Us (Elementor, page 15)
- DevConnect draft (convert-html → build-page): 7 HTML widgets → logged per section in docs/devconnect-conversion-issues.md.
- Snapshot backups/07-before-about-native.sql. Rebuilt natively: tools/elementor/build_about.py (191 nodes, 0 HTML widgets)
  + theme/assets/scss/pages/_about.scss; publish with tools/about/publish.sh (build CSS, set-page-data, clear element cache).
- Clean images 87 (map) / 88 (hero) via tools/about/clean_images.py. _wp_page_template = elementor_header_footer.
- Verified 1440 (0.97–4.1% per section), 430 (heights ±6px), no overflow 390–1920, navbar link OK. Issues-log #30, #31.
- 2026-09-28 — Step 4: HTML replicas of Resources, Resource Library, Contact Us (DevCommand compiler; shared chrome/lib). Issues #33–#39. Awaiting developer review before the ACF/Elementor conversions.
- 2026-09-28 — Step 5: HTML replicas of Product Browse + Product Main / Variation A / Variation B (one template generator). Issues #40–#45.
- 2026-09-28 — Step 6: Sales Hub Login + Dashboard HTML replicas; all 11 Figma pages now have HTML. Issues #46–#49.
- 2026-09-28 — Step 7: About Us HTML replica generated from the Elementor tree + _about.scss. Issue #50. HTML stage complete for all pages.

## 2026-09-28
- Maintenance verified on **product-buttons** (ACF) — content_update, pass 1, 0 open findings. Agent: maint-qa.
- Maintenance verified on **products** (ACF) — content_update, pass 1, 0 open findings. Agent: maint-qa.

## 2026-09-29
- Site restarted via Local GraphQL (#62). Front page → Mizuho Home. Evidence: responsive (11 pages), robustness (136 checks + visual
  review → #63–#65 fixed), global proof (→ #66 fixed), permalinks (#67), brochure links (#68).
- Packaged: `dist/module11-theme.zip`, `docs/db-export/task-11.sql`; docs: decision record, WALKTHROUGH, LOOM-SCRIPT, SUBMISSION.
- Open: maintenance ticket (not received), Loom recording, git commit (awaiting the developer's go-ahead).
