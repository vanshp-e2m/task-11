# Robustness evidence

**Result: 136/136 section checks pass.** Failures are listed per case below and in `docs/issues-log.md` with their fixes.

Real seeded content, three deliberate abuses, every ACF layout (19) + the product template. Built by `tools/evidence/robustness.py` (setup: private test pages/products through DevConnect; check: measured at 1440 and 430).

| Case | What was done to the content |
|---|---|
| **long** | every heading-like field doubled (`X` → `X X`), product title doubled |
| **empty** | every optional field emptied except the section id and the section's first text field |
| **ratio** | every image replaced by a 600×1800 (1:3) or 2400×400 (6:1) test image |

Pass rules: no horizontal page overflow · no clipped text · nothing sticking out of its section · no empty `<h*>`/`<a>`/`<img src="">` in the markup · no PHP notices · (ratio) every image box keeps the size it has on the real page.

## long · all Flexible Content layouts · 1440px
Page overflow: **none** · PHP notices: **0** · screenshot: [page-long-1440.png](page-long-1440.png)

| Section | height (orig → test) | clipped text | sticking out | empty tags | images (box vs real page) | verdict |
|---|---|---|---|---|---|---|
| hero-carousel | 930 → 1048 | — | — | — | 4 images | ✅ |
| intro-statement | 402 → 542 | — | — | — | — | ✅ |
| value-columns | 773 → 817 | — | — | — | 4 images | ✅ |
| procedure-band | 555 → 837 | — | — | — | 4 images | ✅ |
| testimonials | 1190 → 1423 | — | — | — | 6 images | ✅ |
| about-stats | 746 → 826 | — | — | — | — | ✅ |
| resources-intro | 597 → 597 | — | — | — | 2 images | ✅ |
| testimonials | 1697 → 1752 | — | — | — | 20 images | ✅ |
| fast-facts | 550 → 550 | — | — | — | 6 images | ✅ |
| brochures | 5729 → 5729 | — | — | — | 60 images | ✅ |
| continue-your-visit | 257 → 257 | — | — | — | — | ✅ |
| products-intro | 810 → 810 | — | — | — | — | ✅ |
| browse-by-procedure | 435 → 553 | — | — | — | 3 images | ✅ |
| browse-by-product | 2005 → 2005 | — | — | — | 12 images | ✅ |
| sales-hub-login | 818 → 818 | — | — | — | 1 images | ✅ |
| dashboard | 590 → 590 | — | — | — | 3 images | ✅ |
| account | 139 → 139 | — | — | — | — | ✅ |
| resource-library-intro | 105 → 105 | — | — | — | — | ✅ |
| resource-results | 5566 → 5566 | — | — | — | 81 images | ✅ |

## long · all Flexible Content layouts · 430px
Page overflow: **none** · PHP notices: **0** · screenshot: [page-long-430.png](page-long-430.png)

| Section | height (orig → test) | clipped text | sticking out | empty tags | images (box vs real page) | verdict |
|---|---|---|---|---|---|---|
| hero-carousel | 1361 → 1582 | — | — | — | 4 images | ✅ |
| intro-statement | 540 → 747 | — | — | — | — | ✅ |
| value-columns | 1546 → 1573 | — | — | — | 4 images | ✅ |
| procedure-band | 1163 → 1652 | — | — | — | 4 images | ✅ |
| testimonials | 2250 → 2467 | — | — | — | 6 images | ✅ |
| about-stats | 1450 → 1482 | — | — | — | — | ✅ |
| resources-intro | 1049 → 1147 | — | — | — | 2 images | ✅ |
| testimonials | 4822 → 5004 | — | — | — | 20 images | ✅ |
| fast-facts | 1375 → 1646 | — | — | — | 6 images | ✅ |
| brochures | 9317 → 9417 | — | — | — | 60 images | ✅ |
| continue-your-visit | 323 → 355 | — | — | — | — | ✅ |
| products-intro | 845 → 1049 | — | — | — | — | ✅ |
| browse-by-procedure | 822 → 1047 | — | — | — | 3 images | ✅ |
| browse-by-product | 6116 → 6181 | — | — | — | 12 images | ✅ |
| sales-hub-login | 774 → 774 | — | — | — | 1 images | ✅ |
| dashboard | 1278 → 1300 | — | — | — | 3 images | ✅ |
| account | 414 → 414 | — | — | — | — | ✅ |
| resource-library-intro | 270 → 302 | — | — | — | — | ✅ |
| resource-results | 17484 → 17484 | — | — | — | 81 images | ✅ |

## long · product template (variant A) · 1440px
Page overflow: **none** · PHP notices: **0** · screenshot: [product-long-1440.png](product-long-1440.png)

| Section | height (orig → test) | clipped text | sticking out | empty tags | images (box vs real page) | verdict |
|---|---|---|---|---|---|---|
| product-overview | 736 → 736 | — | — | — | 5 images | ✅ |
| instruments-included | 741 → 741 | — | — | — | — | ✅ |
| accessories | 534 → 534 | — | — | — | 4 images | ✅ |
| testimonial | 383 → 437 | — | — | — | — | ✅ |
| related-products | 553 → 553 | — | — | — | 3 images | ✅ |

## long · product template (variant A) · 430px
Page overflow: **none** · PHP notices: **0** · screenshot: [product-long-430.png](product-long-430.png)

| Section | height (orig → test) | clipped text | sticking out | empty tags | images (box vs real page) | verdict |
|---|---|---|---|---|---|---|
| product-overview | 1352 → 1396 | — | — | — | 5 images | ✅ |
| instruments-included | 874 → 896 | — | — | — | — | ✅ |
| accessories | 1507 → 1507 | — | — | — | 4 images | ✅ |
| testimonial | 517 → 777 | — | — | — | — | ✅ |
| related-products | 1119 → 1141 | — | — | — | 3 images | ✅ |

## empty · all Flexible Content layouts · 1440px
Page overflow: **none** · PHP notices: **0** · screenshot: [page-empty-1440.png](page-empty-1440.png)

| Section | height (orig → test) | clipped text | sticking out | empty tags | images (box vs real page) | verdict |
|---|---|---|---|---|---|---|
| hero-carousel | 930 → 207 | — | — | — | — | ✅ |
| intro-statement | 402 → 215 | — | — | — | — | ✅ |
| value-columns | 773 → 205 | — | — | — | — | ✅ |
| procedure-band | 555 → 209 | — | — | — | — | ✅ |
| testimonials | 1190 → 410 | — | — | — | — | ✅ |
| about-stats | 746 → 195 | — | — | — | — | ✅ |
| resources-intro | 597 → 597 | — | — | — | — | ✅ |
| testimonials | 1697 → 138 | — | — | — | — | ✅ |
| fast-facts | 550 → 97 | — | — | — | — | ✅ |
| brochures | 5729 → 304 | — | — | — | — | ✅ |
| continue-your-visit | 257 → 207 | — | — | — | — | ✅ |
| products-intro | 810 → 810 | — | — | — | — | ✅ |
| browse-by-procedure | 435 → 203 | — | — | — | — | ✅ |
| browse-by-product | 2005 → 2005 | — | — | — | 12 images | ✅ |
| sales-hub-login | 818 → 818 | — | — | — | 1 images | ✅ |
| dashboard | 590 → 590 | — | — | — | — | ✅ |
| account | 139 → 139 | — | — | — | — | ✅ |
| resource-library-intro | 105 → 105 | — | — | — | — | ✅ |
| resource-results | 5566 → 5566 | — | — | — | 81 images | ✅ |

## empty · all Flexible Content layouts · 430px
Page overflow: **none** · PHP notices: **0** · screenshot: [page-empty-430.png](page-empty-430.png)

| Section | height (orig → test) | clipped text | sticking out | empty tags | images (box vs real page) | verdict |
|---|---|---|---|---|---|---|
| hero-carousel | 1361 → 327 | — | — | — | — | ✅ |
| intro-statement | 540 → 295 | — | — | — | — | ✅ |
| value-columns | 1546 → 138 | — | — | — | — | ✅ |
| procedure-band | 1163 → 367 | — | — | — | — | ✅ |
| testimonials | 2250 → 184 | — | — | — | — | ✅ |
| about-stats | 1450 → 120 | — | — | — | — | ✅ |
| resources-intro | 1049 → 229 | — | — | — | — | ✅ |
| testimonials | 4822 → 199 | — | — | — | — | ✅ |
| fast-facts | 1375 → 162 | — | — | — | — | ✅ |
| brochures | 9317 → 239 | — | — | — | — | ✅ |
| continue-your-visit | 323 → 113 | — | — | — | — | ✅ |
| products-intro | 845 → 315 | — | — | — | — | ✅ |
| browse-by-procedure | 822 → 135 | — | — | — | — | ✅ |
| browse-by-product | 6116 → 5942 | — | — | — | 12 images | ✅ |
| sales-hub-login | 774 → 774 | — | — | — | 1 images | ✅ |
| dashboard | 1278 → 260 | — | — | — | — | ✅ |
| account | 414 → 94 | — | — | — | — | ✅ |
| resource-library-intro | 270 → 184 | — | — | — | — | ✅ |
| resource-results | 17484 → 17484 | — | — | — | 81 images | ✅ |

## empty · product template (variant A) · 1440px
Page overflow: **none** · PHP notices: **0** · screenshot: [product-empty-1440.png](product-empty-1440.png)

| Section | height (orig → test) | clipped text | sticking out | empty tags | images (box vs real page) | verdict |
|---|---|---|---|---|---|---|
| product-overview | 736 → 676 | — | — | — | — | ✅ |

## empty · product template (variant A) · 430px
Page overflow: **none** · PHP notices: **0** · screenshot: [product-empty-430.png](product-empty-430.png)

| Section | height (orig → test) | clipped text | sticking out | empty tags | images (box vs real page) | verdict |
|---|---|---|---|---|---|---|
| product-overview | 1352 → 406 | — | — | — | — | ✅ |

## ratio · all Flexible Content layouts · 1440px
Page overflow: **none** · PHP notices: **0** · screenshot: [page-ratio-1440.png](page-ratio-1440.png)

| Section | height (orig → test) | clipped text | sticking out | empty tags | images (box vs real page) | verdict |
|---|---|---|---|---|---|---|
| hero-carousel | 930 → 930 | — | — | — | 4/4 boxes unchanged, object-fit cover,fill | ✅ |
| intro-statement | 402 → 402 | — | — | — | — | ✅ |
| value-columns | 773 → 773 | — | — | — | 4/4 boxes unchanged, object-fit cover | ✅ |
| procedure-band | 555 → 555 | — | — | — | 4/4 boxes unchanged, object-fit contain,fill | ✅ |
| testimonials | 1190 → 1190 | — | — | — | 6/6 boxes unchanged, object-fit cover,fill | ✅ |
| about-stats | 746 → 746 | — | — | — | — | ✅ |
| resources-intro | 597 → 597 | — | — | — | 2/2 boxes unchanged, object-fit cover,fill | ✅ |
| testimonials | 1697 → 1697 | — | — | — | 20/20 boxes unchanged, object-fit cover,fill | ✅ |
| fast-facts | 550 → 550 | — | — | — | 6/6 boxes unchanged, object-fit cover,fill | ✅ |
| brochures | 5729 → 5729 | — | — | — | 60/60 boxes unchanged, object-fit fill | ✅ |
| continue-your-visit | 257 → 257 | — | — | — | — | ✅ |
| products-intro | 810 → 810 | — | — | — | — | ✅ |
| browse-by-procedure | 435 → 435 | — | — | — | 3/3 boxes unchanged, object-fit cover,fill | ✅ |
| browse-by-product | 2005 → 2005 | — | — | — | 12/12 boxes unchanged, object-fit cover | ✅ |
| sales-hub-login | 818 → 818 | — | — | — | 1/1 boxes unchanged, object-fit cover | ✅ |
| dashboard | 590 → 590 | — | — | — | 3/3 boxes unchanged, object-fit contain | ✅ |
| account | 139 → 139 | — | — | — | — | ✅ |
| resource-library-intro | 105 → 105 | — | — | — | — | ✅ |
| resource-results | 5566 → 5566 | — | — | — | 81/81 boxes unchanged, object-fit cover,fill | ✅ |

## ratio · all Flexible Content layouts · 430px
Page overflow: **none** · PHP notices: **0** · screenshot: [page-ratio-430.png](page-ratio-430.png)

| Section | height (orig → test) | clipped text | sticking out | empty tags | images (box vs real page) | verdict |
|---|---|---|---|---|---|---|
| hero-carousel | 1361 → 1361 | — | — | — | 4/4 boxes unchanged, object-fit cover,fill | ✅ |
| intro-statement | 540 → 540 | — | — | — | — | ✅ |
| value-columns | 1546 → 1546 | — | — | — | 4/4 boxes unchanged, object-fit cover | ✅ |
| procedure-band | 1163 → 1163 | — | — | — | 4/4 boxes unchanged, object-fit contain,fill | ✅ |
| testimonials | 2250 → 2250 | — | — | — | 6/6 boxes unchanged, object-fit cover,fill | ✅ |
| about-stats | 1450 → 1450 | — | — | — | — | ✅ |
| resources-intro | 1049 → 1049 | — | — | — | 2/2 boxes unchanged, object-fit cover,fill | ✅ |
| testimonials | 4822 → 4822 | — | — | — | 20/20 boxes unchanged, object-fit cover,fill | ✅ |
| fast-facts | 1375 → 1375 | — | — | — | 6/6 boxes unchanged, object-fit cover,fill | ✅ |
| brochures | 9317 → 9317 | — | — | — | 60/60 boxes unchanged, object-fit fill | ✅ |
| continue-your-visit | 323 → 323 | — | — | — | — | ✅ |
| products-intro | 845 → 845 | — | — | — | — | ✅ |
| browse-by-procedure | 822 → 822 | — | — | — | 3/3 boxes unchanged, object-fit cover,fill | ✅ |
| browse-by-product | 6116 → 6116 | — | — | — | 12/12 boxes unchanged, object-fit cover | ✅ |
| sales-hub-login | 774 → 774 | — | — | — | 1/1 boxes unchanged, object-fit cover | ✅ |
| dashboard | 1278 → 1278 | — | — | — | 3/3 boxes unchanged, object-fit contain | ✅ |
| account | 414 → 414 | — | — | — | — | ✅ |
| resource-library-intro | 270 → 270 | — | — | — | — | ✅ |
| resource-results | 17484 → 17484 | — | — | — | 81/81 boxes unchanged, object-fit cover,fill | ✅ |

## ratio · product template (variant A) · 1440px
Page overflow: **none** · PHP notices: **0** · screenshot: [product-ratio-1440.png](product-ratio-1440.png)

| Section | height (orig → test) | clipped text | sticking out | empty tags | images (box vs real page) | verdict |
|---|---|---|---|---|---|---|
| product-overview | 736 → 736 | — | — | — | 5/5 boxes unchanged, object-fit contain,cover | ✅ |
| instruments-included | 741 → 741 | — | — | — | — | ✅ |
| accessories | 534 → 534 | — | — | — | 4/4 boxes unchanged, object-fit cover | ✅ |
| testimonial | 383 → 383 | — | — | — | — | ✅ |
| related-products | 553 → 553 | — | — | — | 3/3 boxes unchanged, object-fit cover | ✅ |

## ratio · product template (variant A) · 430px
Page overflow: **none** · PHP notices: **0** · screenshot: [product-ratio-430.png](product-ratio-430.png)

| Section | height (orig → test) | clipped text | sticking out | empty tags | images (box vs real page) | verdict |
|---|---|---|---|---|---|---|
| product-overview | 1352 → 1352 | — | — | — | 5/5 boxes unchanged, object-fit contain,cover | ✅ |
| instruments-included | 874 → 874 | — | — | — | — | ✅ |
| accessories | 1507 → 1507 | — | — | — | 4/4 boxes unchanged, object-fit cover | ✅ |
| testimonial | 517 → 517 | — | — | — | — | ✅ |
| related-products | 1119 → 1119 | — | — | — | 3/3 boxes unchanged, object-fit cover | ✅ |

## What the numbers did not catch (visual review of the screenshots)

The first run passed every automated check while the **long** page was visibly broken: the automated checks look for
HORIZONTAL problems, and the failure was VERTICAL. The Home layouts (and Browse by procedure) were built from Figma
coordinates with `position:absolute`, so a doubled heading ran over the cards/text under it, and fixed-height
`nowrap` labels (hero pills, value-column kickers, Watch now / Continue your visit / account buttons) spilled out.
Fixes (issues-log #65): `tools/figma_html/flow_desktop.py` turns the measured coordinates into row grids (same pixels
at the drawn content, rows grow with their content; Home stays 0–3.7% vs the replica, heights +0), and
`assets/scss/base/_robustness-guards.scss` lets the fixed labels wrap. Two defects the checks DID catch are fixed
too: the Dashboard icon box stretched to 252px with a 1:3 upload (now a fixed 70×61 box, object-fit contain), and
editors could not preview Sales Hub pages (#64). A layout reused on another page lost its styles (#63).
Accepted as designed: **empty** sections with fixed Figma heights keep their drawn height (clean, just spacious);
the Resources video tiles and product accessories take their images/titles from the linked posts, so those rows
don't change in the long/ratio cases.

## Writes made for this test (listed + read back, CLAUDE.md rule #16)

- dev/upload-media qa-wrong-ratio-600x1800.jpg -> 259
- dev/upload-media qa-wrong-ratio-2400x400.jpg -> 260
- dev/create-page 'QA robustness — long' -> 261 (then WP-CLI: private, slug, Flexible template)
- dev/acf-read-write-values write sections on 261: 19 rows, read back 19
- dev/create-custom-post m11_product 'LawtonElite Skull Base Instrumentation S…' -> 263 (then WP-CLI: private, terms copied)
- dev/acf-read-write-values write x27 on product 263; read-back mismatches: none
- dev/create-page 'QA robustness — empty' -> 264 (then WP-CLI: private, slug, Flexible template)
- dev/acf-read-write-values write sections on 264: 19 rows, read back 19
- dev/create-custom-post m11_product 'LawtonElite Skull Base Instrumentation S…' -> 266 (then WP-CLI: private, terms copied)
- dev/acf-read-write-values write x27 on product 266; read-back mismatches: none
- dev/create-page 'QA robustness — ratio' -> 267 (then WP-CLI: private, slug, Flexible template)
- dev/acf-read-write-values write sections on 267: 19 rows, read back 19
- dev/create-custom-post m11_product 'LawtonElite Skull Base Instrumentation S…' -> 269 (then WP-CLI: private, terms copied)
- dev/acf-read-write-values write x27 on product 269; read-back mismatches: none

The test pages/products are **private** (`qa-robustness-*`), so visitors never see them; an editor can open them to repeat the check.
