# Responsive evidence

Each sheet: **Figma 1440 | WordPress 1440 | WordPress 768 | WordPress 430 | Figma 430**, all at 1/3 scale (heights comparable).
Figma has no tablet frame, so 768 is judged on layout sanity + overflow only. Page heights include the header and footer.
Overflow = `documentElement.scrollWidth > viewport` (horizontal scrollbar), also checked at 390 and 1920.

| Page | Builder | Figma 1440 h | WP 1440 h | WP 768 h | Figma 430 h | WP 430 h | Overflow 390/430/768/1440/1920 | Sheet |
|---|---|---|---|---|---|---|---|---|
| home | ACF | 5716 | 5712 | 10270 | 9748 | 9777 | ✓/✓/✓/✓/✓ | [home.png](home.png) |
| about-us | Elementor | 8700 | 8677 | 13494 | 13580 | 13600 | ✓/✓/✓/✓/✓ | [about-us.png](about-us.png) |
| contact-us | Elementor | 4205 | 4202 | 4687 | 4771 | 4810 | ✓/✓/✓/✓/✓ | [contact-us.png](contact-us.png) |
| resources | ACF | 9948 | 9946 | 17684 | 18420 | 18353 | ✓/✓/✓/✓/✓ | [resources.png](resources.png) |
| products | ACF | 3663 | 4012 | 7168 | 5994 | 7397 | ✓/✓/✓/✓/✓ | [products.png](products.png) |
| product-main | ACF (CPT) | 3342 | 3337 | 5896 | 5789 | 5884 | ✓/✓/✓/✓/✓ | [product-main.png](product-main.png) |
| product-a | ACF (CPT) | 4067 | 4063 | 6819 | 6767 | 6835 | ✓/✓/✓/✓/✓ | [product-a.png](product-a.png) |
| product-b | ACF (CPT) | 3938 | 3933 | 6583 | 6515 | 6494 | ✓/✓/✓/✓/✓ | [product-b.png](product-b.png) |
| sales-hub-login | ACF | 1023 | 1048 | 1066 | 1089 | 1112 | ✓/✓/✓/✓/✓ | [sales-hub-login.png](sales-hub-login.png) |
| dashboard | ACF | 1023 | 1023 | 1994 | 1999 | 2040 | ✓/✓/✓/✓/✓ | [dashboard.png](dashboard.png) |
| resource-library | ACF | 1355 | 1685 | 3965 | 2839 | 3978 | ✓/✓/✓/✓/✓ | [resource-library.png](resource-library.png) |

Notes: Figma frame heights include the drawn header/footer; small height differences come from the shared chrome
(the WordPress footer is one Theme Builder template for every page, the frames differ slightly) and from filter/listing
pages rendering real query results. Per-section pixel diffs against the HTML replicas are in
`docs/evidence/flow-a/wp-vs-replica/report.json` and `docs/evidence/flow-b/contact/wp-vs-replica.txt`.
