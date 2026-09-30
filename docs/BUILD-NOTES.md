# Build notes: issues, fixes, and how the builder was chosen

Module 11 capstone · Mizuho America design · local site `task-11.local`.
This is the readable summary. The detailed log (every command and check) is in `issues-log.md`; the numbers (#1, #2 …) match.

---

## Part 1: How I chose which builder builds which page

### The question I asked for every page
> "Is this page **structured, repeating, or driven by logic**, or is it a **one-off content/marketing page**?"

- **Structured / repeating / logic → coded ACF** (fields + one template part and one SCSS partial per section).
  Editors fill in fields and can't break the layout. The same data can feed several pages, and the code can be reviewed.
- **One-off content page → Elementor.** It's quicker to build, editors can rearrange it visually, and it's what the lead asked
  for ("convert using Elementor").
- **Site-wide pieces (header, footer, colours, fonts, phone number) → central global settings**, whichever builder the page uses.

### The result
| Page | Builder | Why |
|---|---|---|
| Home | **ACF** (Flow A) | Seven repeating blocks (product slides, value columns, procedures, testimonials, stats). Fields keep them consistent. |
| Product Browse | **ACF** | A filtered list of products. That's a query + filter, not a hand-built page. |
| Product Main / Variation A / Variation B | **ACF**, one template | Three designs of the *same thing*: a product. One "Product" content type + one template. Extra blocks (instruments table, size guide) appear only when their fields are filled. Three hand-built pages would drift apart. |
| Resources | **ACF** | A brochure library. Brochures are stored once and shown here *and* in the Sales Hub. |
| Sales Hub: Login, Dashboard, Resource Library | **ACF** | Needs logic Elementor pages don't provide on their own: a sales-rep role, login, restricted pages, "Hello, <name>". |
| About Us | **Elementor** (Flow B) | A one-off story page with long content. Also proves the globals work on a second build method. |
| Contact Us | **Elementor** | A content page (FAQs + contact options), and Elementor Pro has a ready Form widget. |
| Header + footer | **Elementor Theme Builder** | Built once, shown on every page, including the ACF pages. |
| Colours + fonts | **Elementor Site Settings (Kit)** | One source of truth. The theme's SCSS reads Elementor's colour variables, so ACF pages follow along. |
| Phone, email, address, hours, logo, socials | **ACF "Site Settings" options page** | Used by the Elementor header/footer (dynamic tags) *and* by ACF templates (PHP). Change once → updates everywhere. |

### Alternatives I rejected
- **Everything in Elementor.** It fails the rubric's "template part + SCSS partial per layout", and products/filters/login would
  end up as copy-pasted pages.
- **Everything in ACF.** It ignores the lead's instruction to use Elementor, and the two content pages gain nothing from being coded.
- **Three separate product pages.** Same content type, so it's one template with optional sections.

### Where the tooling didn't fit my plan
- DevCommand's Elementor pipeline is **native widgets only** and never pairs ACF with Elementor. So wiring ACF Site Settings
  into Elementor (dynamic tags) is done **by hand through DevConnect**, outside the automated pipeline.
- DevCommand **refuses to touch a homepage** at all (#8). So Home is built as an inner page (`mizuho-home`) and made the
  front page by hand at the end.

---

## Part 2: Issues we hit and how we resolved them

| # | What went wrong | How I noticed | What I did | Status |
|---|---|---|---|---|
| 1 | Database backup came out **empty (0 bytes)**. The MySQL tools used the default port, but Local runs this site on port 10053. | The file size, then a warning on the retry | Set the host/port for every MySQL tool in `tools/wp.sh`; every snapshot is now checked for size and a "Dump completed" line | ✅ Fixed |
| 2 | The Figma MCP connector had hit its free-plan limit (on task-9) | Carried over from the last project | Switched to the Figma REST API with a personal token | ✅ Avoided |
| 3 | Elementor Pro prints a warning when run from the command line | WP-CLI output | Only happens in CLI context; the front end is clean | 👀 Watching |
| 4 | Figma token was valid but **couldn't read files** (wrong permission) | Error said "requires file_content:read"; a `/me` check showed the token itself worked | New token with *File content: Read* | ✅ Fixed |
| 5 | The DevConnect zip provided would have **reintroduced a Windows bug** (theme files refused as "restricted") | I compared the zip with the installed copy instead of trusting the version number | Kept the already-patched plugin. Must re-patch if ever reinstalled from the zip | ✅ Avoided |
| 6 | Some DevConnect actions reject empty input `{}` | Error "input is not of type object" | Send a harmless placeholder `{"_": 1}`; rule added to CLAUDE.md | ✅ Worked around |
| 7 | DevConnect was "connected" but its tools never loaded in VS Code | The doctor check disagreed with a direct server check | Settings were saved under `C:\…` but VS Code looks up `c:\…` (case). Saved under every spelling | ✅ Fixed |
| 8 | DevCommand's extractor **refused the Home page** (never touches homepages) | Its own safety rule fired on step one | Build Home as the inner page `mizuho-home`; set it as front page by hand at the end | ✅ Resolved (developer decision) |
| 9 | Figma **blocked image exports for ~4.6 days** (rate limit) | 429 errors with "Retry-After: 396406" | Stopped retrying; used saved renders + manual exports. Lesson: one batched request, never parallel | ✅ Worked around |
| 10 | Manual Figma exports **silently dropped frames**, repeated others, and one came out the wrong width | I checked every file against the frame list and sizes, not just the file count | Removed duplicates by file content, cropped the oversized one, re-exported the missing ones → **22/22 verified** | ✅ Fixed |
| 11 | A design image has a **Shutterstock watermark** | Spotted while checking an export | It stays an editable image field; flagged to the lead as a licensing issue | ⚠️ Flagged |
| 12 | DevConnect's "create ACF field group" reported **success but saved zero fields** | I checked the saved JSON file and the database instead of trusting "ok" | Read the plugin source: it never saves fields, and it strips Flexible Content layouts. Field groups are now written as ACF Local JSON (the committed source of truth); the ability is only used to read back and verify | ✅ Fixed |
| 13 | **My mistake:** Elementor type presets written in px (project rule: rem), and the site stylesheet didn't refresh after the fix | Reading DevCommand's Elementor rules before the header; then checking the *compiled* CSS | Converted all 34 values to rem by script, forced a CSS rebuild; verified 4.375rem in the live stylesheet | ✅ Fixed |
| 14 | **My generator bugs:** wrong setting names (menu font, CSS classes, text case), all silently ignored by Elementor | The live screenshot didn't match Figma, even though DevCommand's validator said "valid" | Compared the widget's real schema to what was stored; fixed the three key names in the generator | ✅ Fixed |
| 15 | DevConnect's "build page" **emptied the header and footer** while reporting success | It said 1 node for trees of 20 and 29; I counted what was stored | It expects a different tree format and dropped everything it didn't recognise; rewrote with the native-format ability → 20/29 nodes | ✅ Fixed |
| 16 | **My process gap:** my curl helper's writes weren't recorded by DevCommand's QA ledger | Checked the ledger before closing the step | Rule: writes go through the MCP tool; the helper is for reads and oversized payloads, and any write it makes is listed and verified | ✅ Rule added |
| 17 | DevCommand's planner said the Figma data file was empty and **retyped the text from screenshots** ("Sugita ll" became "II", quotes and case changed) | Diffed all 67 Figma text layers against its plan; the file was actually 430 KB | Sent it back to take every string from the Figma data → 71/71 verbatim | ✅ Fixed |
| 18 | Generated page loaded **no web fonts**: the agent hand-wrote a Google Fonts link in an old format (HTTP 400) | Headings looked wrong; network log showed the failure. Two of *my* checks misled me first (a font API that always says yes, a cached page) | Correct link; verified from the network log, and previews cache-busted from then on | ✅ Fixed |
| 19 | Planner agent **stalled** during its own QA | 10-minute no-progress watchdog | Checked what it had built, then did the QA myself | ✅ Worked around |
| 20 | The improvised compiler ignored edits to the plan (markup hard-coded in its script) | The fixer's edits had no effect | Superseded by #21 | ➡️ See #21 |
| 21 | **Root cause of #17–#20:** the planner **wrote its own compiler**, having wrongly concluded DevCommand's wasn't installed (it looked in the project, not the plugin) | A file header in the fixer's report; I checked, and the real compiler and recipes exist | Real compiler run unchanged through a small Windows wrapper; plan redone against the real recipes; improvised build kept as evidence | ✅ Fixed |
| 22 | DevCommand's HTML compiler **silently dropped the brand colours** (extractor and compiler store tokens in different formats) | Compiled colours were the compiler's placeholders | Token-format shim in the wrapper; compiler untouched | ✅ Fixed |
| 23 | Re-plan agent **stopped by a usage limit**; plan left half-written with a changed section mapping | Checked the file before reusing it | Fresh run finished it, with the mapping change justified (#24) | ✅ Fixed |
| 24 | Two approved recipes **can't hold the design** (DevCommand's templates have only 2 fields) | I read `recipes.json` myself to confirm the agent's claim | Those sections built as escape hatches; validator issues (`href="#"`, repeated CSS) fixed | ✅ Justified |
| 25 | DevCommand's SCSS workflow **can never pass its own validator's** mobile-menu check (Sass removes the quotes it searches for) | The rule kept failing although the CSS was right; I ran the validator's own regex on the output | Left as a documented false positive; the menu was verified working in the browser | ⚠️ Tool bug |
| 26 | Compiler requests fonts by weight only → **fake italic** (wrong line wraps) and Fraunces **without its decorative "&"** | Line-wrap and glyph comparisons with Figma; I needed 3 attempts (width match ≠ glyph match) | Real italic face + full-axis Fraunces at opsz 34 / WONK 1 | ✅ Fixed |
| 27 | Page drifted at non-1440 widths; mobile didn't follow Figma. Rebuilt all sections from Figma geometry (scaled desktop + Figma-mobile flow); two of my own bugs along the way (reset specificity, a refactor that cut rules in half) | Developer screenshots; then per-section pixel diffs after every change | 1440: 0.6–4.6% diff; 430: every section within 7px of Figma | ✅ Fixed |
| 28 | Figma token expired; images cropped from the export (hero photo was a placeholder) | API 401/403 | Crops from the approved export | ⚠️ Waiting on a new token |
| 29 | My bridge helper broke on big uploads (Python picked WSL bash) | `rest_invalid_json` only from Python | `tools/bridge.py` direct client | ✅ Fixed |
| 30 | **About Us: DevConnect draft = 7 HTML widgets**; validator said valid; template + cache writes reported success but didn't apply | Widget-type count, body class, unchanged page height | Native 191-node tree + theme partial; template meta + cache clear via WP-CLI | ✅ Fixed |
| 31 | Map/hero export crops had text baked in | Looked at the crops | Inpainted clean versions (87, 88) | ✅ Fixed |
| 32 | Generated Home HTML links were all `#placeholder` anchors: About didn't navigate | Developer clicked it; I listed every href | Link map in the generator → real WP URLs for existing pages; recompiled | ✅ Fixed |
| 33 | Mixed line-heights drifted 5–7px per line (Figma puts leading above a line and takes its height from the line's first character) | Measured the export's text rows | Per-line first-character heights + a small shift class per line | ✅ Fixed |
| 34 | New pages compiled without Montserrat (compiler asked Google for "Gotham") | Read the compiled font link | Font substitution written into each page's tokens | ✅ Fixed |
| 35 | Italic quote rendered bold (the italic file copied from Home is a bold face) | Side-by-side crop; fonts reported as loaded | Google's real 300-italic file | ✅ Fixed |
| 36 | Gradients wrong: Figma handles are normalised and the 3rd handle sets the direction. **My first two conversions were wrong** | Sampled pixel colours | Exact converter (`figma_linear`) used on every gradient | ✅ Fixed |
| 37 | Design defects: stray text run, duplicated card, "3 resources" over 4 results, duplicated FAQ, phone 888 vs 800, 1 of 9 FAQ answers | Built from the Figma data and compared with the export | Each handled and listed; the phone number needs the client | ⚠️ Flagged |
| 38 | Export images had icons/badges/chips baked in | Looked at the crops | Inpainted clean crops (48 images) | ✅ Fixed |
| 39 | My diff tool took minutes on long pages | It timed out | numpy count | ✅ Fixed |
| 40 | Product generator read a hidden Figma fill | Generator failed; printed raw fills | Visible-fills helper everywhere | ✅ Fixed |
| 41 | Validator: my `.btn` clashed with the compiler's base button | New hard violation | Renamed `.pbtn` | ✅ Fixed |
| 42 | Mobile blue band turned white (shared Home rule outranked it) | Looked at the 430 render | Stronger selector for the band | ✅ Fixed |
| 43 | Same photo is faded on Resource Library, vivid on Product Browse | Browse looked washed out | Crop each page's own export | ✅ Fixed |
| 44 | Table row borders / negative padding / missing padding shifted blocks (mine) | Measured y's vs Figma | Inset shadows, margin, padding | ✅ Fixed |
| 45 | Placeholder copy/images in product designs (FPO thumbs, "Prof Name Here", wrong labels, part number) | Reading the Figma data | Followed as drawn, flagged for the client | ⚠️ Flagged |
| 46 | Login design has a fake browser address bar drawn in | Geometry dump + export | Left out; page shifted up 55px | ✅ Decided |
| 47 | Login lost the shared CSS (it has no header), so links underlined and it overflowed at 1024 (mine) | Mobile look + width check | Shared CSS on the Login section | ✅ Fixed |
| 48 | Validator: 3 identical colour rules (2 were mine in the portal header) | Validator | Merged | ✅ Fixed |
| 49 | Dashboard: "Log in" button on a logged-in page, a different footer, the public header on mobile | Reading the frames | Followed as drawn, flagged | ⚠️ Flagged |
| 50 | About HTML replica (generated from the Elementor tree): token vars, repeated rules (**my first merge changed the cascade**), fake italic, 18px header offset | Validator, 0-pixel before/after diff, section tops | Tokens resolved, cascade-safe merge, real italic, header offset | ✅ Fixed |
| 51 | Resources replica image broken since built (name cut at 60 chars) | DevCommand asset resolver | Name fixed; all replicas scanned, 0 missing | ✅ Fixed |
| 52 | Extractor found only one shared header/footer cluster (public + Sales Hub are different) | Reading shared-regions output | Two chromes built as separate Theme Builder templates | ⚠️ Worked around |
| 53 | Token parser swapped primary/secondary, breakpoints [1024, 1023] | Comparing tokens to the Kit | Kit + Site Settings stay the source; tokens not imported | ⚠️ Worked around |
| 54 | Section slicer **merged Resources Testimonials + Brochures and dropped four product sections** | Compared with the expected section list | Patched slicer copy (IMPLIED_CLOSE), re-sliced, evidence kept | ✅ Fixed |
| 55 | Two dead links in my replicas (#products, #overview) | Parser anchor map | Real targets | ✅ Fixed |
| 56 | Coverage checker: CPT field groups reported as missing FC layouts | Checker HIGH ×2 | False positive explained (CPT groups aren't FC) | ⚠️ Explained |
| 57 | DevCommand deployer can't read the assembler's seed (crash, 0 writes, no CPT phase) | Dry run | `tools/seed_acf.py` pushes the same seed via DevConnect, every write verified | ✅ Worked around |
| 58 | Seed values that never stored: `<br>` markup, un-flattened seamless clone, buttons name clash (C14) | Front end + read-back | Seeder fixes + plain repeater | ✅ Fixed |
| 59 | Hello Elementor/Elementor defaults leaking in (1140 cap, table/cite reset, portal header widths, admin bar for reps) | Per-section diff vs replica | Scoped resets, auto widths, role filter; hero bg fields (C13) | ✅ Fixed |
| 60 | Flexible Content pages opened in the block editor, sections hidden in a collapsed drawer | wp-admin editability screenshot | Classic screen + no content editor on the Flexible template only | ✅ Fixed |
| 61 | Contact Us: DevConnect converted the page (form, FAQ, contact details) into ONE HTML widget | Widget-type count of the conversion output | Native tree: Pro Form, Nested Accordion, Site Settings dynamic tags + scoped SCSS | ✅ Fixed |
| 62 | Site stopped after a reboot: MCP ECONNREFUSED, WP-CLI/replica server down | MCP error at session start, curl 000, no listeners | Started via Local GraphQL `startSite`; bridge.py for writes (listed + verified) | ✅ Fixed |
| 63 | Layouts styled only on their own page (CSS scoped to the slug) — reuse/rename broke them | Planning robustness pages | Origin-scope wrapper when a layout is used elsewhere | ✅ Fixed |
| 64 | Editors couldn't preview Sales Hub pages | Robustness capture showed the login screen | `edit_pages` may view the portal | ✅ Fixed |
| 65 | Longer content overlapped content below (absolute Figma coordinates); labels spilled; icon box stretched | Screenshots (the automated checks missed it) + icon box check | Measured row grids (`flow_desktop.py`), label guards, fixed icon box | ✅ Fixed |
| 66 | Kit colour change never reached any page: literal hex in generated partials + tokens declared on `:root` where `--e-global-*` doesn't exist | Global-settings proof measured heading colours | Generator tokenises brand hex; tokens on `:root, body` | ✅ Fixed |
| 67 | Git Bash rewrote `/%postname%/` into a Windows path (broken term archives, resource links) | Resource link in the markup | `wp.sh` disables MSYS path conversion; structure reset, rules flushed | ✅ Fixed |
| 68 | "Read description" → 404; excerpt cards 22px off on mobile | Section drift probe | Link to the brochure file; mobile rule per Figma mobile | ✅ Fixed |
| 69 | wp-admin refused to save ACF pages: "Value must be a valid URL" (anchors in URL-type fields) | Developer editing live | 16 URL fields → text (same keys), synced | ✅ Fixed |

### Conversion traps found in the design (things a straight copy would get wrong)
1. One Figma group holds **two sections** (hero + intro), so they'd have been merged.
2. One text layer holds **a heading and a paragraph** (footer), so it needs two fields.
3. "Watch now" buttons are **text laid over boxes**, so they're rebuilt as real links.
4. Every mobile frame is called **"hero-m"**, so desktop↔mobile had to be matched by content.
5. **3 carousel dots for 2 slides**, so dots come from the real slide count.
6. Line-heights smaller than the font size, an uneven content width, and an off-centre stats row: normalised on purpose (accepted decisions).

### Mistakes of my own (kept here on purpose)
- I said the extractor was wrong about the footer font (Fraunces). **It was right**: the font was hidden in a per-character style
  override that my check didn't read.
- My first copy of the Figma exports mangled Windows paths and then deleted the temp folder. Nothing was lost; redone safely.
- Kit typography in px instead of rem (#13), three wrong setting names in my header/footer generator (#14), and writes that skipped
  the QA ledger (#16).
- I blamed Elementor's element cache for the missing CSS classes. It was switched off, so that theory was wrong. What actually
  fixed it was a site-wide cache rebuild, and I recorded it that way.

---
## Part 3: Step log

### Step 1a: Global colours, fonts and Site Settings ✅
- **Elementor Kit:** 4 system colours (Mizuho Blue, Sky Blue, Text, Navy) + 3 extras; 4 system + 13 custom type presets from the
  Figma type scale, with Figma's mobile sizes. Tablet sizes are interpolated (no tablet frame).
- **Checked:** Elementor prints its colour variables on pages **not** built with Elementor. So the theme's SCSS reads
  `var(--e-global-color-primary)` etc., and one colour change in Elementor updates ACF pages too.
- **Fonts** load once, from the theme (Elementor's own Google Fonts loading switched off).
- **ACF Site Settings** holds logo, white logo, phone, fax, email, hours, address and the Sales Hub name.
  _(Trimmed in Step 1b, see below.)_
- **Judgement calls:** header black #000 merged into text #090909 (invisible difference); one site container of 1240px instead
  of seven different left edges; the CMYK logo converted to an sRGB PNG.

### Step 1b: Header, footer, pages and menus ✅
- **Pages (shells):** Mizuho Home, About Us, Contact Us, Resources, Sales Hub (+ Dashboard, Resource Library, Cross-Reference,
  Training under `/sales-hub/`). DevConnect can't set a page's parent, so that was done with WP-CLI.
- **Menus (9):** Primary, four footer columns, Legal, Language, Sales Hub, Sales Hub Legal. Links to pages that were never designed
  (Careers, Terms, Cookie Policy, Accessibility, ESP) are `#` placeholders and **flagged**, not invented.
- **Header + footer:** Elementor Theme Builder templates, generated by `tools/elementor/build_chrome.py` and checked by DevCommand's
  validator before every write. Colours and fonts all come from the Kit; phone, fax, email, hours, address and logos come from Site Settings
  through theme-registered "Site Settings" dynamic tags (text, `tel:`/`mailto:` link, logo). The copyright year is Elementor's date tag.
- **Design decision made while building:** Site Settings only holds values used in **two or more places**. Single-use text (header
  links, footer sentences) lives in its one template, so there's never a second place to edit it. Elementor's ACF tags also can't loop a
  repeater or read a link label, which ruled out the EN/ESP repeater and the header-link fields I'd first made.
- **Mobile (no menu design in Figma):** the burger opens the Primary menu. "Sales Portal" was added to that menu as a mobile-only
  item, because the design hides the Sales Portal button on phones and reps would otherwise have no way in.
- **Measured against Figma at 1440:** logo 200×61 at x=612 (Figma 613); nav starts x=61 (Figma 61); search 161×29 (Figma 161×29);
  header 179px tall (Figma 177). The logo colour now matches Figma (converted with its embedded colour profile).
- **Tablet (no Figma frame):** header uses the burger; footer menus become 2×2 and the bottom row stacks.
- **Global value proof:** one Phone edit updated header text + `tel:` link and footer text + `tel:` link, with 0 stale copies
  (`docs/evidence/flow-b/global-phone-proof.md`).
- **Not built yet, on purpose:** the Sales Hub header/footer (it shows the logged-in user and an account menu), built in the Sales Hub step.

### Step 2 (Flow A, re-run): Home page re-planned and compiled against DevCommand's REAL recipe library/compiler ✅
- **Context:** issues #17–#21 found that the first "generated HTML" for `mizuho-home` came from a compiler the planner agent
  wrote itself (`tools/figma_html/compile_blueprint.py`), not DevCommand's real one — it explained the broken font link (#18) and
  hard-coded escape-hatch markup (#20). Issue #22 found and fixed a token-schema mismatch (brand colours silently dropped) via a
  documented shim in `tools/figma_html/run_devcommand_compiler.py`. Issue #23: the re-plan agent hit a usage limit mid-rewrite,
  leaving `blueprint.json` half-finished with an unexplained recipe-mapping change.
- **This step:** verified #23's change wasn't a silent shortcut. Read `card-grid-3col`/`testimonial-grid`'s actual templates in
  the plugin's `recipes.json` — both are 2-field recipes (title+body / quote+author) and genuinely cannot carry this design's
  4-field value columns (title→icon→italic lead→body) or 3 video-bio testimonial cards + a separate pull quote. Kept both as
  escape-hatch, per the "never force a bad match" rule, with the evidence recorded in the blueprint's own section notes and in
  issue #24.
- **Two new defects only DevCommand's real validator catches** (the improvised compiler never checked for either): every
  `"link_url": "#"` placeholder hard-fails as `href_hash_as_button` (fixed: real anchors like `#request-a-demo` instead of a
  bare `#`); four sections independently repeating the identical mobile `padding`/`background` declaration hard-fails as
  `repeated_declaration_set` (fixed: merged into one shared selector list in one section's CSS, removed from the other three).
- **Result:** `python tools/figma_html/run_devcommand_compiler.py mizuho-home` → `ok: true` (6 sections, 1 recipe match
  `intro-statement` → `hero-centered`, 5 escape-hatch). `validate_html_output.py` → **`valid: true`**, 0 violations. Content
  re-verified against `figma/data.json`'s raw TEXT nodes (0 mismatches); G1–G8 (issue #21's own acceptance list) all hold in the
  compiled output. Full detail in issue #24.
- **Left open, reported not fixed:** the asset-manifest's own schema (`file`) doesn't match what the compiler's asset lookup
  expects (`name`/`final_path`) — harmless for this page (every image resolves via its literal `figma/images/...` path, all
  15 files verified present), but the same class of schema drift as #22 and worth a 4th shim if a future page's image path
  ever doesn't fall back cleanly.

### Step 2a: Generated HTML (Flow A, Figma → HTML with DevCommand only) ✅
- **Route:** Figma data → DevCommand planner (blueprint) → **DevCommand's real compiler** → DevCommand validator (`valid: true`) →
  my visual QA at 1440/430 → DevCommand fixer (2 rounds). No WordPress, no DevConnect in this step.
- **Where the conversion was wrong, and what I did:** round 1 (improvised build) G1–G8 · round 2 (real compiler) H1–H6. Every finding
  is in `docs/evidence/flow-a/02-generated-html-fixes.md` with before/after measurements and side-by-side images.
- **Evidence kept:** `00-improvised-build/` (the agent's own compiler, what went wrong), `01-generated-html-raw/` (first output),
  `03-generated-html-final/` (the DevCommand-compiled HTML that goes to the ACF conversion).
- **Known gaps carried into the ACF step, on purpose:** uneven desktop left edges (K1), small procedure icons (K2), value columns
  taller from text wrap (K3). The ACF step rewrites the markup as template parts + SCSS, so fixing them twice would be wasted effort.

_This file is updated at the end of every step._

### Step 3a: About Us (Elementor): DevConnect draft → native rebuild ✅
- **Draft:** Figma copy → semantic HTML (`tools/about/make_about_html.py`) → `dev/convert-html` → `dev/build-page`. Result: 7 HTML
  widgets, unstyled, not editable. Every miss is listed section by section in **`docs/devconnect-conversion-issues.md`** (kept for every
  page from now on).
- **Why rebuild instead of patching:** nothing in the draft was a native widget, so there was nothing to patch. I generated the native
  tree from the Figma geometry and styled it in one theme partial. This keeps the "Elementor for About/Contact" decision: every text,
  image, link and background is editable in the Elementor panel.
- **Result:** desktop matches Figma section by section (0.97–4.1% pixel diff, exact section positions); mobile follows the Figma mobile
  frame (section heights within 1–6px); no overflow from 390 to 1920; the navbar "About Mizuho America" link opens it.
- **Trade-off:** layout lives in the theme stylesheet, not each widget's style panel, so editors change content, not layout. That's
  deliberate for a replica, and it stops the page breaking when edited.
- Evidence: `docs/evidence/flow-b/about/` (draft, native renders at 5 widths, per-section Figma | live | diff sheets).

### Step 4 (Flow A, HTML first): Resources, Resource Library, Contact Us replicas ✅
- **Developer's instruction:** HTML for each page first; the ACF/Elementor conversion comes afterwards. No WordPress writes in this step,
  so no DevConnect draft yet: that happens at each page's conversion step.
- **How:** one generator per page (`tools/figma_html/build_resources.py`, `build_resource_library.py`, `build_contact.py`) writes the
  blueprint; **DevCommand's real compiler** builds `pages/<slug>/html/`, and DevCommand's validator checks the output. Shared pieces:
  `chrome.py` (public header/footer, moved out of the Home generator; Home output verified byte-identical), `chrome_portal.py`
  (Sales Hub header/footer), and `replica_lib.py` (Figma text/line/gradient conversion, CSS merging, compile + validate).
  Every string is read from the Figma JSON by node id; no copy was retyped.
- **Result at 1440:** every section starts at its exact Figma y. Page heights are 9948 / 1355 / 4206 (Figma: 9948 / 1355 / 4205).
  Per-section diff: Resources 2.2–3.9%, Resource Library 1.4–3.2%, Contact Us 1.5–3.7%. Mobile heights: Resource Library 2848 vs 2839,
  Contact Us 4781 vs 4771. No horizontal overflow at 430/768/1024/1920. Validator: only the known #25 false positive (same as Home).
- **Not polished further, on purpose** (the developer asked to move on): Resources mobile and all 768 layouts haven't been diffed section by section.
- Evidence: `docs/evidence/flow-a/{resources,resource-library,contact-us}/` (renders + Figma | live | diff sheets).

### Step 5 (Flow A, HTML first): Product Browse + one product template (Main, Variation A, Variation B) ✅
- **How the pages connect (answered for the developer before building):** navbar Products → Product Browse (the product archive on the
  real site). Every product has its own single page, reached by clicking a product (tiles, procedures, Home hero, accessories/related).
  Main / Variation A / Variation B are three example products on ONE template: A adds the "Instruments Included" table, B the size
  selector + "Size Guide" table. So there is one generator (`tools/figma_html/build_product.py`) that finds each part by its Figma
  name and switches the optional parts on from the frame's data; `build_product_browse.py` builds the archive.
- **Replica links:** navbar Products → Browse; Sugita II tile → Main; procedure "View product" → A / Main / B (demo mapping); breadcrumbs → Browse;
  accessory/related tiles → the other product pages where the names match.
- **Result at 1440:** Browse 3663 (Figma 3663), 2.2–4.3% per band; Main 3342 (3342), 2.3–3.2%; Variation A 4068 (4067), 3.1–5.9%
  (the 5.9% band is the 15-row table: sub-pixel text); Variation B 3938 (3938), 2.3–3.7%. No horizontal overflow at 430/768/1024/1920;
  mobile heights within 16–84px of Figma (tables scroll sideways as drawn). Validator: only the known #25 false positive.
- **Not polished further** (developer's instruction): mobile section-by-section diffs, 768 layouts.
- Evidence: `docs/evidence/flow-a/{product-browse,product-main,product-variation-a,product-variation-b}/`.

### Step 6 (Flow A, HTML first): Sales Hub Login + Dashboard replicas ✅ (every Figma page now has an HTML replica)
- `tools/figma_html/build_sales_hub.py` builds both; portal chrome from `chrome_portal.py` (it now links the replicas together, and has
  the Dashboard's centred-logo footer variant).
- **Click-through verified in a browser:** Log in → Dashboard → Resource Library card → Resource Library → nav Dashboard / Resources.
- **Result at 1440:** Login 968 (Figma 1023 − the 55px browser bar), 0.90% / 2.18%; Dashboard 1023 (1023), 1.3–2.5% per band.
  No horizontal overflow at 430/768/1024/1920. Validator: Login fully valid; Dashboard only the #25 false positive.
- Evidence: `docs/evidence/flow-a/{sales-hub-login,sales-hub-dashboard}/`.

### Step 7: About Us HTML replica ✅ (the HTML stage now exists for all 11 Figma pages)
- Generated from the same tree + SCSS as the live Elementor page (`tools/figma_html/build_about_html.py`), compiled by DevCommand's compiler.
- Result: 8700px at 1440 (Figma 8700), every section at its Figma y, 0.97–4.13% per section; mobile 13582 (13580). Issue #50.
- Evidence: `docs/evidence/flow-a/about-us/`.

### Step 8 (WordPress): ACF pages seeded + Sales Hub chrome + editability ✅
- The 6 Flexible Content pages, 23 products and 47 resources are seeded from DevCommand's assembler output by `tools/seed_acf.py`
  (DevCommand's deployer couldn't read its own seed: #57); every value read back (#58). Per-section diff against the replica: 0–5.75%
  at 1440 on every ACF page. Hello Elementor and Elementor defaults that leaked in are fixed in #59.
- Editors now get the classic screen with the numbered, labelled sections on Flexible Content pages (#60). Product buttons verified by
  DevCommand's maint-qa (**PASS**, ledger closed for posts 230–232).

### Step 9 (Elementor): Contact Us — DevConnect draft → native rebuild ✅
- **Draft:** `dev/convert-html` on the replica → one HTML widget for the whole page (#61). Nothing to patch, so rebuilt natively like About.
- **Why Elementor here:** a form page with a marketing layout the client edits visually. Pro Form gives submissions + email without
  a plugin, and the Nested Accordion lets editors manage FAQs. Contact details are Site Settings dynamic tags, so changing the phone
  number once updates the header, the footer and this page (Flow B).
- **Result:** 0.43–0.91% at 1440 with exact heights; ≤5% at 768/430; working form; evidence in `docs/evidence/flow-b/contact/`.

### Step 10: Final evidence, hardening and packaging ✅
- **Site down after a reboot** (#62): started through Local's GraphQL API; MCP stayed disconnected, so writes went through `tools/bridge.py`
  (same DevConnect endpoint), each listed and read back in the evidence READMEs. Snapshot `12-before-final-evidence`.
- **Front page** set to Mizuho Home (the logo link `/` showed the blog index before).
- **Responsive:** all 11 pages at 1440/768/430 next to Figma, no overflow at 390–1920 (`docs/evidence/responsive/`).
- **Robustness:** all 19 layouts + the product template, doubled headings / emptied fields / wrong-ratio images. The checks found the
  Dashboard icon stretching and the editor gate (#64); **looking at the screenshots** found the real failure — absolute Figma coordinates
  let longer content overlap what's below (#65) — fixed with measured row grids that keep every drawn pixel. Reuse of a layout on another
  page lost its styles (#63) — fixed with an origin-scope wrapper.
- **Global settings proof** caught that a Kit colour reached no page at all (#66): tokenised the generated CSS and declared the tokens on
  `body`. Now one phone edit and one colour edit change all 7 pages across both builders.
- **Found on the way:** Git Bash had mangled the permalink structure (#67); "Read description" linked to a 404 and the replica
  mis-placed it on mobile (#68).
- **Packaged:** theme zip, DB export, decision record, walkthrough, Loom script, submission index. Still open: the maintenance ticket
  (not issued yet) and recording the Loom.
