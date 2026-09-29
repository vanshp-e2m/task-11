# mizuho-home: Figma design spec (ACF Flexible Content)

- **Figma file:** `jSb9GvLZzl7AFll93svlAE`, version `2403008669101368304` (lastModified 2026-09-25T05:08:30Z). The cached `pages/_figma/file.json` is the same version.
- **Desktop frame:** `1:9` "HP with Copy - Approved", 1440 x 5716, white. **Mobile frame:** `1:400` "HP - m", 430 x 9747.6. **Tablet:** none (derive 768/1024).
- **Scope:** this is an INNER page (slug `mizuho-home`, issue #8). Extraction was read-only and nothing was written to WordPress.
- **Machine-readable data:** `section-specs.json` (primary, CSS-ready), `tokens.json`, `images/asset-manifest.json`, `data.json` (raw node trees).
- **Font substitution:** Gotham becomes **Montserrat** (Gotham 300→300, 350 "Medium"→500, 700→700). The specs already use Montserrat, and `figmaFontFamily` records the original.

> **Spacing source.** Every desktop section is a plain Figma GROUP with absolute positioning, so all desktop spacing is
> `[ABSOLUTE POSITIONING: spacing derived from coordinates, exact values preserved, verify manually]`.
> The mobile frame is 100% auto-layout, so every `responsive["430"]` value is `[AUTO-LAYOUT: exact CSS values]`.

---

## Section map

| # | Layout (snake_case) | Desktop node | Mobile node | y-range (desktop) | Description |
|---|---|---|---|---|---|
| 0 | `site_header` **GLOBAL** | 1:117 Top Nav | 1:401 nav-m | 24-161 | Language switch, centred logo, account-manager link, nav, search, Sales Portal / Contact Us buttons, phone |
| 1 | `hero_carousel` | 1:81 (part) | 1:411 | 194-1057 | Two-line display heading (second sentence in sky), 2 product slide cards, 2 CTAs, "Browse by Procedure" anchor, 3 pager dots |
| 2 | `intro_statement` | 1:81 (part) | 1:439 + line 1:444 | 1125-1492 | "We are Mizuho America…" heading, lead paragraph, "Watch what clinical experts…" button, full-width sky divider |
| 3 | `value_columns` | 1:31 Why Mizuho | 1:445 | 1591-2172 | 4 value columns (title, icon, italic lead, body) with vertical dividers, brochures button |
| 4 | `procedure_band` | 1:145 Browse by procedure | 1:471 | 2265-2820 | Blue band: heading, 3 procedure items (icon + links), closing line + "Supported Procedures" button |
| 5 | `testimonials` | 1:57 Case Study | 1:487 + 1:518 (+ lines 1:517, 1:523) | 2911-3961 | Eyebrow + intro, 3 video cards (thumb, play, bio, Watch now), divider, pull quote + attribution, "See more testimonials" with flanking rules |
| 6 | `about_stats` | 1:10 About Mizuho v3 | 1:524 | 4056-4657 | Centred heading + paragraph, 3 stat cards (white shadow panel + blue/sky card), "Explore our story" button |
| 7 | `site_footer` **GLOBAL** | 1:132 Footer | 1:545 | 4756-5716 | Blue footer: Contact & Support, contact details, divider, 4 menu columns, logo + copyright + legal links |

### Where Figma group boundaries don't match the visual sections
1. **`Main Intro Section` (1:81) contains two sections.** It holds the hero (1:111 heading, 1:94/1:99 cards, 1:82/1:87/1:90 CTA row, 1:113/1:114 arrows) **and** the intro statement (1:108, 1:109, 1:105/1:106 button). I split them at y=1091. The mobile file confirms the split: they are two separate frames (1:411 and 1:439).
2. **The divider isn't where the brief assumed.** `Line 3` (1:104) is at y=1492, the bottom of the Main Intro group. It separates the intro from **Why Mizuho**, not the hero from the intro. There is no line between the hero and the intro.
3. **Testimonials and the pull quote** are one group on desktop (1:57). Mobile splits the quote into its own frame (1:518) with dividers above and below. I kept them as one layout with a `quote` sub-group, but it could become two layouts.
4. **A hidden line in About** (`Line 2` 1:11, y=-91 relative, i.e. 3965 on the page) sits in the gap *between* testimonials and About.
5. **The Watch-now buttons** in testimonials are text runs *inside* the bio text layers (1:64-1:66), placed over separate rectangles (1:61-1:63). They are not components.
6. **Every mobile section frame is named `hero-m`**, so the names carry no meaning. The mapping above is by content.

---

## 0. site_header (GLOBAL, 1:117 → 1:401)
Build as an Elementor Pro Theme Builder header. Logo, phone and links come from Site Settings.

| Element | Spec |
|---|---|
| Lang switch "EN    ESP" | Gotham 350 (Gotham-Medium) → **Montserrat 500** 13/15.6 #000000; one text layer with 4 typed spaces; EN underlined by a 22x1 #000000 line |
| Logo | 200x61 raster (CMYK JPEG), x=613..813 (centre 713, **7px left of page centre**) |
| Find an Account Manager | Montserrat 500 13/15.6 #000000, top right (y=40) |
| Primary nav | Open Sans 600 13/17.7 #000000 at x=61, y=89; **4 items in one text layer separated by 7 spaces** (~24px gap in the render) |
| Search | 161x29, bg #00B3F0 @ 20% (`#00B3F033`), r5, "Search..." Open Sans 700 13 #000000, 12px left inset |
| Sales Portal | 117x29 #0065B3 r5, Open Sans 700 13 #FFFFFF centred; 10px after search |
| Contact Us | 109x29, 2px #00B3F0 border, transparent, r5, Open Sans 700 13 #00B3F0; 11px after Sales Portal |
| Phone | Open Sans 700 13/17.7 #000000, right-aligned at y=125 (12px under buttons) |
| Edges | left 24px, visual right edge 1414 (26px) |

**Mobile (430, auto-layout):** bg #FCFEFF, padding 10/20, gap 18. Row 1: logo 118x31 + hamburger 19x19 (`icon-menu.svg`, space-between). Row 2: EN/ESP + Find an Account Manager.
**Hidden on mobile:** nav, search, Sales Portal, Contact Us, phone. **There is no drawer/menu-open design.**

## 1. hero_carousel (1:81 part → 1:411)
| Element | Desktop |
|---|---|
| Heading | Freeman 400 **70/70** UPPER #0065B3; "ours, too." is a colour span #00B3F0; x=96, box w1247 (2 lines) |
| Slide card | 572x592, image radius 51 (left) / 50 (right), object-fit cover; gap 80; x=104 and 756; 38px below heading lines |
| Card border | 3px #00B3F0 r48, **visible on the right card only** (left border 1:95 hidden) |
| Slide label pill | #0065B3 r13, h45, fixed widths 308/372, centred; Freeman 19/40 (right card 19/45) #FFFFFF; top offset 31 / 28 |
| Slide arrow | 55x55 white circle with the arrow cut out (`icon-arrow-circle-right.svg`), right 36/34, bottom 39 |
| CTA row | 43px below cards, auto-layout Frame 11 gap 34 |
| Explore All Products | 216x50 #0065B3 r5, padding 0 35, Freeman 18/23.94 #FFFFFF |
| Request a Demo | 288x50, 2px #00B3F0 r5, transparent, padding 0 88/84 (asymmetric), Freeman 18/23.94 #00B3F0 |
| Browse by Procedure | 46px after CTAs, down arrow (`icon-arrow-down.svg`, 14px, 2px #0065B3) + 32px gap + Freeman 18/50 #0065B3 |
| Pager | 3 dots 24px, gap 8, active #0065B3, inactive #D9D9D9, right edge 1308 |

**Repeater:** `slides` (image, title, link) with 2 designed. The **3 dots imply 3 slides** (Swiper per project-config).
**Mobile (1:411):** padding 44/20, gap 36. Heading Freeman **48/55.2** with a hard break after "mindset.". **Cards stack** at 390x403.6, gap 18, r34.77, both borders hidden. Pill Freeman 12/27.27, h30.7, r8.86, padding 1/20/1/19. Arrow 38px. Then the row "Browse by Procedure" (Freeman 14/18.62, 12px arrow, gap 8.15) + dots 15px gap 5. **Then** the buttons, full width 390x50, stacked with gap 18 → **order change** vs desktop (desktop shows the buttons before the link and dots).

## 2. intro_statement (1:81 part → 1:439)
| Element | Desktop |
|---|---|
| Heading | Freeman 400 **45/55** UPPER #0065B3, w1216, x=107, 68px below the CTA row |
| Body | Open Sans **300 25/45** #090909, w1216, 23px below heading lines |
| Button | 303x50 #0065B3 r5, label Freeman 16/40 #FFFFFF, 20px left inset. Rect and label are separate layers, and the label box (355) is wider than the rect (303). 24px below body |
| Divider | 1px #00B3F0, 1262 wide (x=84..1346), 70px below the button, 103px above Why Mizuho |

**Mobile (1:439):** padding 44/20, gap 36; heading Freeman 36/41.4; body Open Sans 300 18/24.51; button full width, centred label Freeman 16/21.28; line 1:444 (390px) after the frame.

## 3. value_columns (1:31 → 1:445)
| Element | Desktop |
|---|---|
| Columns | 4, pitch ~315 (x=114 / 430.7 / 744.7 / 1060), text width 253-259; 1px #00B3F0 vertical dividers 470px tall at x=400/715/1030; ~30px text inset after each divider |
| Title | Freeman 400 24/31.92 UPPER #00B3F0 |
| Icon | raster, ~100px wide, heights 98/90/84/72, 18px below title. Figma compensates with auto-layout gaps 25/33/39/51 so every lead starts at +173 from the title top → use a fixed 98px icon box + 25px gap |
| Lead | Open Sans **600 italic** 16/30 #090909 |
| Body | Open Sans 300 16/30 #090909, after an empty 30px paragraph |
| Button | 293x50 #0065B3 r5, Freeman 16/40 #FFFFFF, 20px inset, 61px below dividers, x=107 |

**Repeater:** `columns` (title, icon, lead, body), 4 designed.
**Mobile (1:445):** padding 44/20, gap 28; columns stack; **horizontal** 1px #00B3F0 390px dividers replace the vertical ones; title Freeman 20/26.6 with icon 12px below (79x77 / 88x80 / 87x73 / 96x69); lead/body 14/28; button full width.

## 4. procedure_band (1:145 → 1:471)
| Element | Desktop |
|---|---|
| Band | full width, 555 tall, #0065B3; content x=76, top 51, bottom 58 |
| Heading | **Mukta 700 34/50** #FFFFFF, w1137, 2 lines (text box h72 is smaller than its 100px content) |
| Items | 3 at y=+209: icon + text. Item x = 85 / 566 / 944; icons 146x146 / 114x158 / 184x167; icon-text gap 10 / 15 / 6 |
| Item title | Montserrat (Gotham) 700 20/40 #FFFFFF (item 3 wraps, 20/30) |
| View product → | Montserrat 700 16/40 #FFFFFF |
| Secondary link | Montserrat 700 16/26 **#77DCFF**, after an empty 26px line |
| Closing line | **Mukta 700 32/50** #FFFFFF at y=+446 |
| Supported Procedures | 391x50 white, 2px #00B3F0 border, r5; label Freeman 18/50 #0065B3 left (~19px inset), `icon-arrow-down.svg` right (24px inset); right edge 1378 (62px margin vs 76px left) |

**Repeater:** `procedures` (icon, title, product link, secondary link text + URL), 3 designed.
**Mobile (1:471):** padding 44/20, gap 36; heading and closing line both Mukta 28/46.54; items stack as rows (icon left, text always at +156px); title 18/24, links 14/40 and 14/22; button full width **without a border**, Freeman 16/21.28, 12px arrow.

## 5. testimonials (1:57 → 1:487 + 1:518)
| Element | Desktop |
|---|---|
| Eyebrow | "TESTIMONIALS" Freeman 34/50 UPPER #0065B3 (x=76, 91px below band) |
| Intro | Open Sans **400** 20/40 #090909 (same text layer as the eyebrow) |
| Video cards | 3 thumbs 409x272 (middle 408), no radius, gaps 27 / 29, 6px below intro |
| Play icon | 53x53 `icon-play-circle.svg`, centred |
| Bio | 17px below thumb, inset 21/19/17. Name Open Sans 700 18/30 #0065B3; first role line Open Sans 300 14/30; rest 14/22 #090909 |
| Watch now | 93x40 #0065B3 r5, Freeman 14 #FFFFFF, 17px after bio (flows with the bio length, so the middle button is 22px lower) |
| Divider | 1px #00B3F0 1282 wide, 82px below the lowest button |
| Quote | Freeman 34/50 UPPER #0065B3 centred, max-width 998, 57px below divider |
| Attribution | Open Sans 300 24/45 #090909 centred, 8px below quote |
| See more testimonials | 179x50 #0065B3 r5, Freeman 16/40, 44px below attribution; flanked by two 513px 1px #00B3F0 rules |

**Repeaters:** `videos` (thumbnail, video URL, name, role lines, button label), 3 designed; `quote` (single: quote, attribution).
**Mobile:** padding 44/20, gap 36. Eyebrow Freeman 28/50; intro Open Sans **300** 18/24.51 (weight changes from 400). Cards stack: image 390x259.4, bio frame padding 9.54/9.54/9.54/20.02, gap 16, name 16/28.61, roles 13/28.61 and 13/21. **Watch now becomes a real 140x50 button with Freeman 16.** **Mobile adds a full-width "Watch what clinical experts say about us" button** after the cards. The quote is a separate frame: Freeman 24/31.92, attribution Open Sans 300 20/27.24, full-width button, 390px dividers above and below; the flanking rules are removed.

## 6. about_stats (1:10 → 1:524)
| Element | Desktop |
|---|---|
| Heading | "ABOUT MIZUHO AMERICA" Freeman 34/50 #0065B3, **typed in caps** (no textCase), centred; **14.5px left of page centre**; 95px below testimonials |
| Body | Open Sans 400 16/36 #090909 centred, max-width 1090 (x=175..1265), ~21px below heading. The text layer starts with 2 empty lines to clear the heading |
| Stat | 421x250 composite, pitch 370: white panel 146x250 r10, `box-shadow: 21px 0 21px -23px #000000`, drawn **on top of** the card's left 15px; card 290x162 r20 at +131/+44 |
| Card colours | #0065B3 / #00B3F0 / #0065B3 |
| Number | Open Sans 700 **64/36** #FFFFFF, 50px inset |
| Label | Open Sans 700 16/18 #FFFFFF, 21px below number box |
| Button | "Explore our story" 150x50 #0065B3 r5, Freeman 16/40, 20px below cards; 99px above footer |

**Repeater:** `stats` (number, label, colour variant), 3 designed.
**Mobile (1:524):** padding 44/20, gap 36; heading Freeman 24/31.92 (textCase UPPER here); body Open Sans 400 14/28; stats stack (350x250, panel 75/75/71 wide, card offset 60/60/56); number/label sizes unchanged; button full width.

## 7. site_footer (GLOBAL, 1:132 → 1:545)
| Element | Desktop |
|---|---|
| Background | #0065B3 1440x960 (the group is 974 tall: the copyright text box overflows the frame by 14px) |
| Contact & Support | **Fraunces 700 34/50** #FFFFFF (x=78, y=+70) |
| Intro / hours | Montserrat 300 20/40 ("Contact Us." 700); hours 300 20/30 |
| Details | "Additional ways to reach us:" Montserrat 300 25/40; Phone / Fax / Email lines **700 25/40 (label + value)**; Address **300** |
| Divider | 1px #FFFFFF, x=79..1358, y=+480 |
| Menus | 4 columns at x=78 / 453 / 794 / 1081 (pitch 375/341/287), y=+531; heading Montserrat 700 25/50; links 300 20/40 |
| Bottom row | logo 200x58 at **x=44** (content edge is 78); copyright Montserrat 300 14/40 at x=256; legal links 300 14/40 in one layer separated by 6 spaces, right edge ~1405 |

**Mobile (1:545):** padding 44/20, gap 36; heading Fraunces 28; texts 18/40, 18/30; details 20/32; menus in a **2x2 grid** (column gap 36), heading 22/50, links 16/40; logo stacked above copyright (gap 8), both Montserrat 12/14.4; legal links 12/14.4.

---

## Design-quality flags (listed only; nothing was fixed)

### A. Line-height smaller than font-size
- **Open Sans 700 64/36**: every stat number (1:14, 1:19, 1:24; mobile 1:530, 1:535, 1:540).
- Open Sans 700 27/21: a whitespace-only run in the About body (1:27, a spacer line, not visible).
- Freeman 70/70 (1.0) in the hero heading: not below font-size, but zero leading.
- **The "48/20" style from the brief does not occur on this page.** The mobile hero is 48/55.2. It may be on another page.
- Text boxes smaller than their content: the band heading 1:147 box is h72 for 100px of lines; the intro heading 1:108 box overlaps the body box 1:109 (1106 > 1064).

### B. Mixed fonts
- **Body copy uses two families at identical sizes:** Open Sans 20/40 (testimonials intro) vs Gotham 20/40 (band items, footer); Open Sans 16 (body) vs Gotham 16 (band links); Open Sans 14 (bios) vs Gotham 14 (footer legal).
- **Headings use three families:** Freeman everywhere, **Mukta** only in the band, **Fraunces** only in the footer heading. Fraunces is a 5th font and is not in the project-config font list.
- The header utility text uses Gotham 350 (PostScript "Gotham-Medium"), an unusual weight value; I mapped it to Montserrat 500.
- Header text is #000000 while the body is #090909.
- The testimonials intro weight changes from 400 (desktop) to 300 (mobile).

### C. Inconsistent spacing between similar blocks
- **No common container:** left edges are 76 (band, testimonials, about), 78 (footer), 96 (hero heading), 104 (cards), 106 (CTAs), 107 (intro, why button), 114 (why column 1 text). Right margins vary from 62 to 117.
- **Hero cards:** pill top 31 vs 28, pill line-height 40 vs 45, arrow right inset 36 vs 34; the border is visible on one card only.
- **Request a Demo** padding 88/84 (asymmetric).
- **Value columns:** icon heights 98/90/84/72, compensated by gaps 25/33/39/51; the column-4 body is inset 13.3px from its title.
- **Procedure items:** icon sizes 146 / 114x158 / 184x167, icon-text gaps 10/15/6, column pitch 481 vs 378; the closing button's right margin is 62 vs the 76 left.
- **Testimonials:** column gaps 27/29, bio insets 21/19/17, Watch-now buttons at different heights.
- **Stats:** stat 1 is 4px lower; number offsets 37/41/48; **the stat row is not centred** (76 left vs 204 right on desktop, 20 vs 60 on mobile); mobile panel widths 75/75/71.
- **Off-centre items:** the About heading (-14.5px), the header logo (-7px), the footer logo at x=44 vs content 78, and the legal links' right edge 1405 vs divider end 1358.
- **Section gaps:** 33, 68, 70/103, 93, 91, 95, 99, with no rhythm (nearest 8px grid: 32, 72, 72/104, 96, 88/96, 96, 96/104).
- Nav items and legal links are spaced with typed spaces instead of real gaps.

### D. Hidden or invisible layers
- `1:95` left-card border rect (hidden), so the two cards differ.
- `1:110` hidden alternate hero heading (Freeman 56/70) and `1:112` (70/70 at x=-8), both duplicates of the visible 1:111.
- `1:107` hidden alternate button label (Gotham 700 16/40 #0065B3 "... →").
- `1:11` hidden full-width divider in About (sits between testimonials and About).
- **`1:113` "arrow-right-circle-fill" frame:** its fill is hidden but it has a **visible 1px #000000 stroke**, so it renders as a **stray black 66px square** around the right card's arrow. It is visible in the render.
- Mobile `1:415` / `1:421` hidden card borders.
- **Stacked stale fills:** mobile card 2 (`1:422`, named "Surita Screenshot") carries the Sugita image under the MST image, and mobile testimonial thumbs 2 and 3 (`1:501`, `1:509`) carry the Lawton thumbnail underneath.

### E. Things that look like they belong elsewhere or are ambiguous
- The **"Watch what clinical experts say about us"** button sits in the intro statement but links to testimonials. On mobile it appears **twice** (intro and end of testimonials).
- The **"Browse by Procedure"** link in the hero is an anchor to the procedure band.
- The band's "Supported Procedures" button shape is a vector named "Find an account button", copied from the header.
- **The carousel is under-specified:** 3 pager dots but only 2 slides; on mobile both slides are stacked *and* the dots remain.
- Mobile section frames all use the same name, `hero-m`.

### F. Copy and asset issues
- "Sugita **ll**" uses two lowercase L's, not the Roman numeral II (1:98, 1:419).
- Footer address "30057 **Ahem** Avenue" (likely "Ahern"); "**Sale** Hub" vs "Sales Portal"; "1000+" vs "1,800+" (inconsistent thousands separator); "Mizuho AMERICA" is typed mixed-case under an uppercase transform.
- The header logo is a **CMYK JPEG** (no transparency, colour-shift risk in browsers; a faint box is visible behind it). **There is no vector logo in the file.**
- **Value-column icons are tiny rasters** (56x55 … 60x43 px shown at ~100px, so ~1.8x upscaled and blurry) with a light frame baked into the pixels.
- The endoscopic procedure icon is 4096x4096 / 595 KB (oversized).
- Testimonial thumbnails are 409x272 only (no 2x) and contain **burned-in lower-third name graphics** (photo pixels, not live text, so they were safe to export).
- The hero photos are screenshots (1499x878, 1581x898), cropped by Figma image transforms; I produced `-card-crop` derivatives.

---

## Mobile mapping summary (desktop → 430)
| Section | What changes |
|---|---|
| header | Nav, search, Sales Portal, Contact Us and phone are hidden → hamburger (no drawer design); 2 rows |
| hero | Heading 70→48; cards stack; **browse link + dots move above the CTAs**; CTAs full width stacked |
| intro | 45→36, 25→18; button full width, centred |
| values | 4 columns → stacked; vertical dividers → horizontal; 16→14 |
| band | 34/32 → 28/28; items become rows; button loses its border |
| testimonials | 3 cards stacked; Watch now 93x40/14 → 140x50/16; **extra "Watch what clinical experts…" CTA**; quote split into its own block with dividers; flanking rules removed; intro 400→300 |
| about | 34→24 heading, 16/36→14/28 body; stats stacked (not centred) |
| footer | 4 menu columns → 2x2; sizes 25/20 → 22/16; logo above copyright |
| all | Section bg #FFFFFF → **#FCFEFF**; section padding 44/20; gap 36 (values 28) |

---

## Figma design quality check
```
Typography: 14 unique desktop sizes (70, 64, 45, 34, 32, 25, 24, 20, 19, 18, 16, 14, 13 + a 27px spacer)
  ⚠ More than 8 sizes; near-duplicates 34/32 (Mukta band), 25/24 (Open Sans lead vs attribution), 19/18 (Freeman pill vs CTA)
  ⚠ Same size with different line-heights: Freeman 18 (23.94 / 50), Freeman 19 (40 / 45)
Spacing: exact values preserved; non-grid: 33 (→32), 38 (→40), 43 (→44), 23 (→24), 51 (→52), 57 (→56), 58 (→56), 61 (→60), 70 (→72), 91 (→92), 95 (→96), 99 (→100), 103 (→104)
Colors: 9 unique (incl. #00B3F033)
  ⚠ Near-duplicates: #FFFFFF / #FCFEFF (mobile bg), #000000 / #090909 (header vs body text)
  ⚠ Config token "divider" = #D9D9D9, but every divider in the design is #00B3F0; #D9D9D9 is only the inactive pager dot
Layout: desktop 0% auto-layout (all 7 top-level GROUPs); mobile 100% auto-layout
Breakpoints: ✓ Desktop 1440  ✗ Tablet (none)  ✓ Mobile 430
Recommendation: PROCEED, but REVIEW flags C/D/F with the designer (carousel slide count, stray black frame 1:113, icon resolution, vector logo, copy typos)
```

---

## Extraction notes and limits
- **Screenshots:** the Figma image-render endpoint returned **HTTP 429 with Retry-After 396406 s (~4.6 days), rate-limit type "low"** after 5 successful section renders. Available files:
  - `screenshots/desktop/2x/`: real node renders at scale 2 for header, hero, intro, values, band, about (composited onto #FFFFFF).
  - `screenshots/desktop/*.png` and `screenshots/mobile/*.png`: **1x** full-width crops of the cached full-frame renders (`pages/_figma/frames/home-desktop.png`, `home-mobile.png`). **The testimonials and footer (desktop) and all mobile sections have no 2x render.**
- **SVG icons** were built locally from vector geometry (`/nodes?geometry=paths`, which was not rate-limited) and checked visually by rasterising them. The logo and all value/procedure icons are raster fills in Figma and **cannot** be exported as SVG.
- Values marked `null` in section-specs.json could not be read from Figma data (e.g. pill padding on fixed-width rects, the footer menu gap).
- A few horizontal insets (nav gap 24, button label right insets, Supported Procedures left inset 19) were **measured from the render**, because the label is a separate text box wider than its text. These are noted in the specs.
