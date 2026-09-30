# Loom script (10–15 min)

Have open: http://task-11.local (logged out), wp-admin as `qa-editor` in a second window, VS Code on this repo,
`docs/evidence/` in the file explorer.

| Min | Show | Say |
|---|---|---|
| 0:00–1:00 | Home at 1440, scroll | Mizuho America from Figma, on a local site only. Two builders on purpose: ACF for structured content, Elementor for two marketing pages. |
| 1:00–2:30 | `docs/decision-record.md` §1 table | Which page is built how and why; header/footer are Theme Builder; colours in the Kit; business data in Site Settings. |
| 2:30–4:30 | `pages/resources/html/` (replica) → `spec/acf-plan.json` → `output/theme/module11/` → `docs/evidence/flow-a/conversion/slicer-bug/` | Flow A: Figma → generated HTML → DevCommand HTML→ACF. **The conversion merged two Resources sections and dropped four product sections** (#54): I noticed by comparing its sections with the ones I expected; patched the slicer, re-ran. |
| 4:30–6:00 | wp-admin → Home: numbered sections, Section Settings / Content tabs; add a Hero Carousel slide; Products → a product | Editability: everything visible is a field, no defaults, sections can be hidden or reordered; products are data, one template, three variants. |
| 6:00–7:00 | About + Contact in Elementor editor | DevConnect's conversion gave HTML widgets only (#30, #61) — rebuilt natively: Pro Form (submit it), Nested Accordion. |
| 7:00–8:30 | `docs/evidence/flow-b/global-proof/` before/after images + README table | Flow B: one phone change in Site Settings, one colour change in the Kit → 7 pages across both builders. The first attempt changed nothing: the proof caught it (#66). |
| 8:30–10:00 | `docs/evidence/responsive/home.png`, `contact-us.png` + README table | 1440/768/430 next to Figma, no overflow 390–1920. Listing pages are taller because they show the real 23 products. |
| 10:00–12:00 | `docs/evidence/robustness/page-long-1440.png`, README | Double-length headings, empty fields, wrong-ratio images on every layout. **The automated checks passed but the screenshots showed overlaps** (#65) — measured row grids fixed it without moving a pixel of the real pages. |
| 12:00–13:30 | `docs/issues-log.md` (#1–#69), `backups/`, `CLAUDE.md` | Safe working: snapshot before every destructive step, only task-11.local, credentials only in local config, every write read back. |
| 13:30–14:30 | `docs/decision-record.md` §4–5 | What I'd do with another day; DevConnect vs DevCommand. |

Record at 1440 wide; zoom the browser to 67% for the side-by-side sheets.
