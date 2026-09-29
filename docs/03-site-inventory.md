# Step 1b — Full site inventory (every page in the Figma file)

Scope expanded by the developer: build **every** page in the file, linked through the navigation. "Page Headers" (1:381) is
**not a design**. It holds only the canvas labels above each frame ("Home Page", "About Us Page", …).

## Pages (desktop 1440 → mobile 430; no tablet frames)
| # | Page | Desktop / mobile node | What it is | Reached from |
|---|---|---|---|---|
| 1 | Home | 1:9 / 1:400 | Marketing homepage (8 sections, extracted) | Logo |
| 2 | About Us | 1:161 / 1:2237 | Story: intro quote, stats, leadership team, milestone map, collaborations, global map, bottom links | Nav "About Mizuho America" |
| 3 | Resources | 1:2490 / 1:559 | Public library: intro + quote, "Fast facts" featured videos, 5,554px brochure grid, bottom links | Nav "Clinical Resources" |
| 4 | Contact Us | 1:3891 / 1:1027 | FAQ list (accordion) + contact options/form, bottom links | Nav "Contact & Support", header "Contact Us" |
| 5 | Product Browse | 1:3176 / 1:1152 | Product catalogue: intro, browse-by-procedure, **filterable** product grid ("4 products found · Head Holding Systems · Clear all") | Nav "Products" |
| 6 | Product Page Main | 1:3504 / 1:1317 | Single product (Sugita II): gallery, breadcrumb, key specs, in-page nav, accessories, testimonial, related | Product cards |
| 7 | Product Variation A | 1:3721 / 1:1538 | Single product that is an **instrument set**: + "Instruments included" table + parts-list download | Product cards |
| 8 | Product Variation B | 1:3332 / 1:1719 | Single product with **sizes**: + "Size guide" table + selected-size spec | Product cards |
| 9 | Login (Sales Hub) | 1:3150 / 1:2210 | Rep login form (email, password, forgot password) | Header "Sales Portal" |
| 10 | Dashboard (Sales Hub) | 1:3095 / 1:1903 | Logged-in rep home: "Hello, John Q.", 3 tool cards with counts, account links | After login |
| 11 | Resource Library (Sales Hub) | 1:2871 / 1:1971 | Logged-in, **filterable/sortable** list of downloadable brochures & spec sheets | Dashboard |

**Two different chromes:** pages 1–8 share the public Top Nav + big footer. Pages 9–11 (Sales Hub) have their **own** slim
portal nav (Dashboard · Resources · Cross-Reference · Training · user menu) and a one-line footer.

## Sections that repeat across pages (build once, reuse)
| Section | Appears on |
|---|---|
| Public header / footer | 1–8 (site-wide templates) |
| Sales Hub header / footer | 9–11 |
| Stats band ("About Mizuho") | Home, About (different variants: "Version 3" vs "Version 1") |
| Browse by procedure | Home, Product Browse |
| Bottom page links ("Before you go…") | About, Resources, Contact |
| Testimonial quote | Home, all 3 product pages |
| Product card grid ("Accessories", "Related products") | All 3 product pages |
| Filter bar + card list | Product Browse, Resource Library |

## Architecture this implies (proposal)
- **Products are data, not pages.** Three "product page" designs = **one `m11_product` post type + one single template** with
  optional sections: an instruments table only when filled in (Variation A), a size guide only when filled in (Variation B).
  Product Browse = the product archive, filtered by a **product category** taxonomy (+ a **procedure** taxonomy for
  "Browse by procedure"). Accessories/related = ACF relationship fields, so cards update themselves.
- **Brochures are data.** `m11_resource` post type (title, category, file download). The public Resources page and the Sales Hub
  Resource Library both list the same records, so an editor uploads a brochure once.
- **Sales Hub is real.** A `sales_rep` role; Dashboard and Resource Library are restricted to logged-in reps; the login page is
  a styled `wp_login_form()`; "Hello, John Q." comes from the logged-in user. Cross-Reference and Training appear in the portal
  nav but **have no designs**, so they stay as menu items pointing to placeholder pages (documented).
- **Build method per page:**
  - ACF coded: Home (Flow A), Product Browse, the product single template, Resources, Sales Hub. These are
    structured, repeating or logic-driven (filters, auth), where fields + templates are safest.
  - Elementor: About Us (Flow B) and Contact Us. These are content/marketing pages, and Contact gets Elementor Pro's
    Form widget.
  - Header/footer: Elementor Theme Builder (public set) + a portal set for the Sales Hub.
- **Out of scope / not designed:** EN/ESP switch (no Spanish content; it stays as an editable link), mobile open-menu
  (our own design), Cross-Reference and Training tools, "Find an Account Manager" (links to Contact).

## Proposed order (core deliverables first, so they are safe even if time runs short)
1. **Foundation:** Elementor Kit (colours, fonts), ACF Site Settings, public + portal header/footer, menus
2. **Home** (Flow A: ACF)
3. **About Us** (Flow B: Elementor + globals)
4. **Products:** CPT + taxonomies + single template (3 variants) + Browse archive
5. **Resources:** CPT + public page
6. **Contact Us** (Elementor + form)
7. **Sales Hub:** role, login, dashboard, resource library
8. Robustness + responsive passes across everything, maintenance ticket, packaging

## Reference screenshots: RESOLVED (all 22 frames in `pages/_figma/frames/export/`, verified against Figma frame sizes)

_Original blocker:_
The Figma render endpoint is locked (~4.6 days, issue #9), so there are **no reference screenshots** for 9 of the 11 pages
(only Home + About full-frame renders are cached). Fastest fix: the developer exports the frames manually from Figma
(select all frames → Export → PNG 1x) into `pages/_figma/frames/export/`.
